def vis_ring(B, cx, cy, r, pct, col, back, L, order=30):
    """v38: a share as a ring (pct of 100, from twelve o'clock clockwise)."""
    B.fill([annulus(cx, cy, 0.62 * r, r, 0.0, 2.0 * math.pi)], back, L, order)
    if pct > 0.0:
        a0 = math.pi / 2.0
        B.fill([annulus(cx, cy, 0.62 * r, r, a0, a0 - 2.0 * math.pi * min(1.0, pct / 100.0))], col, L, order + 1)


def tech_frame(S, B, X, Y, U, num, title, subtitle, sources):
    L = "LU_TECH::Frame"
    B.fill([rect(X, Y - PH * U, X + PW * U, Y)], T_BG, L, 0)
    m = 1.2 * U
    B.line(rect(X + m, Y - PH * U + m, X + PW * U - m, Y - m) + [(X + m, Y - PH * U + m)], T_RULE, L, 2, 0.25)
    B.fit("SELINUS · BERGAMA — TECHNICAL ANALYSIS", X + PM * U, Y - 2.4 * U, 0.42 * U, 60 * U, T_GREY, L)
    B.fit(title, X + PM * U, Y - 4.1 * U, 1.25 * U, 70 * U, T_INK, L, font=FONT_TITLE, bold=True)
    B.fit(subtitle, X + PM * U, Y - 5.2 * U, 0.4 * U, 70 * U, T_GREY, L)
    yb = Y - PH * U + m + 3.0 * U                                    # title block
    B.line([(X + m, yb), (X + PW * U - m, yb)], T_RULE, L, 2, 0.18)
    B.line([(X + PW * U - m - 26 * U, yb), (X + PW * U - m - 26 * U, Y - PH * U + m)], T_RULE, L, 2, 0.18)
    if isinstance(sources, (list, tuple)):              # v38: the method and sources as the sheet's numbered [n] key
        sources = src_key_text(sources)
    B.para_fit(sources, X + PM * U, yb - 0.75 * U, PW * U - 2 * m - 29 * U, 0.26 * U, Y - PH * U + m + 0.35 * U, T_GREY, L)
    bx = X + PW * U - m - 25 * U
    B.fit(CREDIT, bx, yb - 0.9 * U, 0.34 * U, 18 * U, T_INK, L)
    B.fit("Yaşar University · site analysis", bx, yb - 1.6 * U, 0.3 * U, 18 * U, T_GREY, L)
    B.fit("Analyses: survey + open data", bx, yb - 2.2 * U, 0.3 * U, 18 * U, T_GREY, L)
    B.text(num, X + PW * U - m - 0.8 * U, yb - 2.3 * U, 1.6 * U, T_INK, L, font=FONT_TITLE, bold=True, align="R")
    return Y - 6.4 * U, yb + 0.8 * U


def tech_map(S, B, frame, path, x, ytop, wmax, hmax, U, L, scale=True, north=True, crop_bar=True):
    """Place a rendered top view with its north arrow and scale bar; returns (view, width, height). v40: registers
    the map as a booklet crop (with its scale bar unless crop_bar is False: other panels share its strip)."""
    asp = frame.w / frame.h
    wv = min(wmax, hmax * asp)
    hv = wv / asp
    B.image(path, x, ytop - hv, x + wv, ytop, L, 5)
    V, mw, mh = view_fit(frame, x, ytop, wv, hv)
    if north:
        draw_north_small(B, V, mw, mh, U, L, size=0.6)
    if scale:
        draw_scalebar(B, x, ytop - hv - 1.25 * U, V.s, nice_floor(frame.w / 6.0), U, L, h=0.3)
    key = os.path.splitext(os.path.basename(path))[0]    # v40: one booklet crop per map, e.g. T2_surface_heat_summer
    num, per = key.split("_")[0], key.split("_")[-1]
    crop_panel(per, x, ytop - hv - (1.35 * U if scale and crop_bar else 0.0), x + wv, ytop,
               u"{} · {} · {}".format(num, CROP_T.get(num, ""), CROP_PER.get(per, per)), crop_scale(V.s))
    return V, wv, hv


CROP_T = {"T1": u"road noise", "T2": u"ground surface temperature", "T3": u"hours in shade", "T4": u"solar radiation",
          "T5": u"wind at 1.5 m", "T6": u"air temperature", "T7": u"felt temperature (UTCI)",
          "T8": u"comfortable hours, UTCI 9-26 °C"}       # v40: booklet captions of the technical maps
CROP_PER = {"lden": u"Lden, day-evening-night", "day": u"day 06-18", "evening": u"evening 18-22", "night": u"night 22-06",
            "year": u"the whole year", "spring": u"spring", "summer": u"summer", "autumn": u"autumn", "winter": u"winter"}


def tech_bands(B, x, y, w, cols, labels, U, L, title=None, sub=None, h=0.32):
    if title:
        B.fit(title, x, y, 0.34 * U, w, T_INK, L)
        y -= 0.8 * U
    n = len(cols)
    cw = w / float(n)
    for k, c in enumerate(cols):
        c = hexrgb(c) if isinstance(c, str) else c
        B.fill([rect(x + k * cw, y - 0.6 * U, x + (k + 1) * cw - 0.05 * U, y)], c, L, 30)
        B.fit(labels[k], x + (k + 0.5) * cw, y - 1.2 * U, h * U, cw * 0.96, T_INK, L, align="C")
        if sub:
            B.fit(sub[k], x + (k + 0.5) * cw, y - 1.75 * U, h * 0.9 * U, cw * 0.96, T_GREY, L, align="C")
    return y - (2.3 if sub else 1.7) * U


def tech_colorbar(B, x, y, w, hexes, vmin, vmax, U, L, title=None, unit=""):
    if title:
        B.fit(title, x, y, 0.34 * U, w, T_INK, L)
        y -= 0.8 * U
    lut = lut_ramp(vmin, vmax, hexes, 256)
    n = 64
    for k in range(n):
        v = vmin + (vmax - vmin) * (k + 0.5) / n
        B.fill([rect(x + w * k / n, y - 0.6 * U, x + w * (k + 1) / n + 0.01 * U, y)], lut(v), L, 30)
    step = nice_step(vmax - vmin, 6)
    t = math.ceil(vmin / step) * step
    while t <= vmax + 1e-9:
        tx = x + w * (t - vmin) / (vmax - vmin)
        B.line([(tx, y - 0.6 * U), (tx, y - 0.8 * U)], T_INK, L, 31, 0.05)
        B.text(VAL_FMT % t + unit, tx, y - 1.35 * U, 0.3 * U, T_INK, L,
               align="C")
        t += step
    return y - 1.8 * U


def key_plan(S, B, x, ytop, w, focus, U, L):
    """Where the focus area sits in the corridor."""
    V, mw, mh = view_fit(S.F, x, ytop, w, w * S.F.h / S.F.w)
    B.fill([V.P(S.F.P)], (244, 244, 246), L, 3)
    for lp in building_blocks(S):
        B.fill(V.Ps(lp), (205, 205, 210), L, 4)
    for P in getattr(S, "water_outline", []):
        B.line(V.P(P), (90, 140, 180), L, 5, 0.05)
    B.line(V.P(focus.P + [focus.P[0]]), (200, 30, 30), L, 6, 0.18)
    B.line(V.P(S.F.P + [S.F.P[0]]), T_RULE, L, 6, 0.06)
    draw_north_small(B, V, mw, mh, U, L, size=0.45)
    return ytop - mh


# ------------------------------------------------------------ renders for each analysis
# ------------------------------------------------------------ the four sheets
def tech_profile(S, B, x, y, w, h, U, L, who_ref=""):
    nm = S.env["noise"]
    main = max(S.selinus, key=pl_length)
    Lm = pl_length(main)
    pts = []
    s = 0.0
    while s <= Lm:
        q = pl_point_at(main, s)[0]
        v = noise_at(nm, S.F, q[0], q[1])
        if v is not None:
            pts.append((s, v))
        s += 10.0
    lo, hi = 40.0, 80.0
    X_ = lambda s_: x + 2.6 * U + (w - 2.6 * U) * s_ / Lm
    Y_ = lambda v_: y - h + h * (max(lo, min(hi, v_)) - lo) / (hi - lo)
    col = lut_classes([35, 40, 45, 50, 55, 60, 65, 70, 75, 80], noise_pal())
    for k in range(len(pts) - 1):
        (s0, v0), (s1, v1) = pts[k], pts[k + 1]
        if s1 - s0 > 30.0:
            continue
        B.fill([[(X_(s0), y - h), (X_(s1), y - h), (X_(s1), Y_(v1)), (X_(s0), Y_(v0))]], col((v0 + v1) / 2.0), L, 3)
    for db in (45, 55, 65, 75):
        B.line([(x + 2.6 * U, Y_(db)), (x + w, Y_(db))], (200, 200, 205), L, 4, 0.03)
        B.text("%d" % db, x + 2.2 * U, Y_(db) - 0.15 * U, 0.3 * U, T_GREY, L, align="R")
    for dd in dashes([(x + 2.6 * U, Y_(53.0)), (x + w, Y_(53.0))], 0.5 * U, 0.3 * U):
        B.line(dd, T_INK, L, 5, 0.1)
    if who_ref:                                           # v38: the limit named on the chart where it is drawn
        B.text("WHO 53 dB " + who_ref, x + w - 0.1 * U, Y_(53.0) + 0.15 * U, 0.28 * U, T_INK, L, align="R")
    km = 0.0
    while km * 1000.0 <= Lm:
        B.text("%.1f km" % km if km else "0", X_(km * 1000.0), y - h - 0.7 * U, 0.3 * U, T_GREY, L, align="C")
        km += 0.5
    B.line([(x + 2.6 * U, y - h), (x + w, y - h)], T_INK, L, 6, 0.06)


# ============================================================ WIND, AIR TEMPERATURE AND FELT TEMPERATURE
# Climate of the site, embedded so these sheets need no extra file: the PVGIS typical meteorological year 2005-2020 for
# 39.1195 N 27.1838 E (EU JRC): air temperature, humidity and 10 m wind from ERA5, sun from SARAH-2. Per season:
#   hourly  [local hour 0..23] -> [mean dry bulb, 10th percentile, 90th percentile, RH %, wind m/s, sky long-wave W/m2,
#                                  global horizontal, direct normal, diffuse horizontal W/m2]
#   prevailing [hour] -> [direction the wind comes from (deg, 16 sectors), mean speed from it (m/s), share of the hours]
#   rose [16 sectors from N, clockwise][speed class] = share of all hours; classes start at 0.5, 2, 4, 6, 8, 10 m/s
#@include ../data/CLIMATE.py

#@include ../data/UTCI_COEF.py


# Colour scales after windy.com (wind in m/s, temperature in deg C), so the sheets read like the Windy app.
WINDY_WIND = ((0.0, (98, 113, 183)), (1.0, (57, 97, 159)), (3.0, (74, 148, 169)), (5.0, (77, 141, 123)), (7.0, (83, 165, 83)),
              (9.0, (53, 159, 53)), (11.0, (167, 157, 81)), (13.0, (159, 127, 58)), (15.0, (161, 108, 92)),
              (17.0, (129, 58, 78)), (19.0, (175, 80, 136)), (21.0, (117, 74, 147)), (24.0, (109, 97, 163)),
              (27.0, (68, 105, 141)), (29.0, (92, 144, 152)), (36.0, (125, 68, 165)), (46.0, (231, 215, 215)))
WINDY_TEMP = ((-40.0, (162, 70, 145)), (-25.0, (143, 89, 169)), (-15.0, (157, 219, 217)), (-8.0, (106, 191, 181)),
              (-4.0, (100, 166, 189)), (0.0, (93, 133, 198)), (1.0, (68, 125, 99)), (10.0, (128, 147, 24)),
              (21.0, (243, 183, 4)), (30.0, (232, 83, 25)), (47.0, (71, 14, 0)))
KT = 1.943844                                        # knots per m/s
LAPSE = -0.0065                                      # K per m of height (standard atmosphere)
PED_WIND = math.log(1.5 / 0.1) / math.log(10.0 / 0.1)  # wind at 1.5 m over open ground / wind at 10 m (log law, z0 0.1 m)
# Projected area factor of a standing person, averaged over all orientations to the sun, solar altitude 0..90 deg in
# 5 deg steps (ASHRAE 55 SolarCal table as implemented in Ladybug).
FP_STAND = (0.2216, 0.2216, 0.2218, 0.2198, 0.215, 0.2078, 0.1985, 0.1874, 0.175, 0.1628, 0.1513, 0.1405, 0.1294, 0.1171,
            0.1042, 0.0913, 0.0792, 0.0687, 0.0602)
UTCI_STRESS = ((46.0, "extreme heat stress"), (38.0, "very strong heat stress"), (32.0, "strong heat stress"),
               (26.0, "moderate heat stress"), (9.0, "no thermal stress"), (0.0, "slight cold stress"),
               (-13.0, "moderate cold stress"), (-27.0, "strong cold stress"), (-40.0, "very strong cold stress"),
               (-1e9, "extreme cold stress"))
# Relative wind speed behind an obstacle against distance in obstacle heights (x / H), after the windbreak wake
# measurements summarised by Heisler & DeWalle (1988): solid (buildings), dense porous (crowns in leaf), open porous (bare).
WAKE_SOLID = ((0.0, 0.25), (3.0, 0.25), (6.0, 0.4), (10.0, 0.55), (15.0, 0.72), (20.0, 0.85), (30.0, 0.97), (40.0, 1.0))
WAKE_LEAFY = ((0.0, 0.5), (5.0, 0.5), (10.0, 0.7), (15.0, 0.85), (25.0, 0.97), (35.0, 1.0))
WAKE_BARE = ((0.0, 0.75), (5.0, 0.75), (10.0, 0.88), (20.0, 0.98), (25.0, 1.0))


def es_hpa(t):
    """Saturation vapour pressure over water, hPa (Hardy 1998, as used with UTCI)."""
    g = (-2836.5744, -6028.076559, 19.54263612, -0.02737830188, 0.000016261698, 7.0229056e-10, -1.8680009e-13)
    tk = t + 273.15
    es = 2.7150305 * math.log(tk)
    for k, c in enumerate(g):
        es += c * tk ** (k - 2)
    return math.exp(es) * 0.01


def utci(ta, tr, va, pa):
    """Universal Thermal Climate Index (Broede et al. 2012, sixth-order approximation). pa: vapour pressure in kPa,
    va: wind at 10 m (0.5..17 m/s)."""
    va = min(17.0, max(0.5, va))
    d = tr - ta
    T, V, D, P = [1.0], [1.0], [1.0], [1.0]
    for _ in range(6):
        T.append(T[-1] * ta)
        V.append(V[-1] * va)
        D.append(D[-1] * d)
        P.append(P[-1] * pa)
    return sum(c * T[a] * V[b] * D[e] * P[f] for c, a, b, e, f in UTCI_COEF)


def stops_table(stops, vmin, vmax, n=1024):
    """Colour lookup over [vmin, vmax] from value stops (fast enough for every pixel)."""
    table = []
    for k in range(n):
        v = vmin + (vmax - vmin) * k / float(n - 1)
        c = stops[-1][1]
        if v <= stops[0][0]:
            c = stops[0][1]
        else:
            for q in range(len(stops) - 1):
                a, ca = stops[q]
                b, cb = stops[q + 1]
                if v <= b:
                    t = (v - a) / (b - a)
                    c = tuple(int(round(ca[r] + (cb[r] - ca[r]) * t)) for r in range(3))
                    break
        table.append(c)
    span = max(1e-9, vmax - vmin)

    def g(v):
        k = int((v - vmin) / span * (n - 1))
        return table[0 if k < 0 else (n - 1 if k >= n else k)]
    g._lut = ("ramp", vmin, span, n, table)
    return g


# ------------------------------------------------------------ drawing helpers
def page_north(F):
    return math.atan2(math.cos(F.ang), math.sin(F.ang))


def frame_dir(frame, vec):
    o = frame.local(0.0, 0.0)
    e = frame.local(vec[0], vec[1])
    return e[0] - o[0], e[1] - o[1]


def wind_streaks(frame, res, field, nx, ny, cell, to_local, seed=7, spacing=15):
    """Windy-like flow streaks: white strokes along the wind, longer where it blows harder, broken by buildings."""
    def post(rgb, w, h, TB):
        rnd = random.Random(seed)
        bid = TB["bid"]
        dx, dy = to_local[0], -to_local[1]
        for gy in range(0, h, spacing):
            for gx in range(0, w, spacing):
                px, py = gx + rnd.uniform(0, spacing), gy + rnd.uniform(0, spacing)
                ix, iy = int(px), int(py)
                if ix >= w or iy >= h or bid[iy * w + ix]:
                    continue
                i = int((px * res) / cell)
                j = int((frame.h - py * res) / cell)
                if not (0 <= i < nx and 0 <= j < ny) or field[j][i] is None:
                    continue
                U = field[j][i]
                L_ = max(3.0, U * 8.0 / res)
                n = int(L_ * 2.0) + 1
                strength = min(1.0, 0.3 + U / 2.5)
                for k in range(n, -1, -1):           # head first, stop at the first building behind it
                    t = k / float(n)
                    qx, qy = px - dx * L_ * (1.0 - t), py - dy * L_ * (1.0 - t)
                    qi, qj = int(qx), int(qy)
                    if not (0 <= qi < w and 0 <= qj < h) or bid[qj * w + qi]:
                        break
                    a = 0.8 * strength * t * t
                    for oi, oj, wgt in ((qi, qj, 1.0), (qi, qj + 1, 0.4)):
                        if 0 <= oj < h:
                            o = (oj * w + oi) * 3
                            for c in range(3):
                                rgb[o + c] = int(rgb[o + c] + (255 - rgb[o + c]) * a * wgt)
    post._key = repr((frame.P, res, nx, ny, cell, to_local, seed, spacing))
    return post


def draw_wind_rose(B, cx, cy, R, rose, calm, north, U, L):
    """Wind rose in the maps' orientation: where the wind comes from, stacked by speed (Windy colours)."""
    tot = [sum(r) for r in rose]
    fmax = max(tot) if tot else 0.1
    ring = 0.05 if fmax <= 0.3 else 0.1
    rmax = ring * math.ceil(fmax / ring)
    mids = (1.25, 3.0, 5.0, 7.0, 9.0, 11.0)
    cols = [stops_table(WINDY_WIND, 0.0, 12.0)(m) for m in mids]
    B.fill([circle_pts(cx, cy, R, 48)], (247, 247, 249), L, 20)
    r_ = ring
    while r_ <= rmax + 1e-9:
        B.line(circle_pts(cx, cy, R * r_ / rmax, 48) + [circle_pts(cx, cy, R * r_ / rmax, 48)[0]], (200, 200, 206), L, 21, 0.03)
        B.text("%d%%" % round(100 * r_), cx + 0.15 * U, cy + R * r_ / rmax + 0.08 * U, 0.22 * U, T_GREY, L)
        r_ += ring
    for k in range(16):
        a_mid = north - math.radians(k * 22.5)
        a0, a1 = a_mid - math.radians(9.0), a_mid + math.radians(9.0)
        cum = 0.0
        for c, f in enumerate(rose[k]):
            if f <= 0:
                continue
            r0, r1 = R * cum / rmax, R * (cum + f) / rmax
            arc1 = [(cx + r1 * math.cos(a0 + (a1 - a0) * q / 4.0), cy + r1 * math.sin(a0 + (a1 - a0) * q / 4.0)) for q in range(5)]
            arc0 = [(cx + r0 * math.cos(a1 - (a1 - a0) * q / 4.0), cy + r0 * math.sin(a1 - (a1 - a0) * q / 4.0)) for q in range(5)]
            B.fill([arc1 + arc0], cols[c], L, 22)
            cum += f
    for k, lab in ((0, "N"), (4, "E"), (8, "S"), (12, "W")):
        a = north - math.radians(k * 22.5)
        B.text(lab, cx + (R + 0.45 * U) * math.cos(a), cy + (R + 0.45 * U) * math.sin(a), 0.3 * U, T_INK, L,
               font=FONT_TITLE, bold=True, align="MC")
    B.line(circle_pts(cx, cy, R, 48) + [circle_pts(cx, cy, R, 48)[0]], T_RULE, L, 23, 0.04)
    B.text("calm %.0f%%" % (100 * calm), cx, cy - R - 0.85 * U, 0.24 * U, T_GREY, L, align="C")


def utci_band_marks(B, x, y, w, lo, hi, U, L):
    """The official UTCI stress categories under a temperature bar."""
    for k in range(len(UTCI_STRESS) - 1):
        top_, name = UTCI_STRESS[k - 1][0] if k > 0 else 99.0, UTCI_STRESS[k][1]
        b0, b1 = UTCI_STRESS[k][0], top_
        a0, a1 = max(lo, b0), min(hi, b1)
        if a1 <= a0:
            continue
        xa, xb = x + w * (a0 - lo) / (hi - lo), x + w * (a1 - lo) / (hi - lo)
        B.line([(xa, y), (xb, y)], T_INK, L, 31, 0.05)
        B.line([(xa, y - 0.1 * U), (xa, y + 0.1 * U)], T_INK, L, 31, 0.04)
        B.fit(name if name.startswith("no ") else name.replace(" stress", ""), (xa + xb) / 2.0, y - 0.42 * U, 0.2 * U,
              max(0.5 * U, xb - xa - 0.1 * U), T_GREY, L, align="C")
    return y - 0.75 * U


# ------------------------------------------------------------ v16.3: close extremes get stretched colours
# When the values of one picture cover only a small part of the shared scale (the air temperature of a section, which
# only height changes, spans a few tenths of a degree on a 40-degree scale), the picture's colours are stretched so the
# differences can be seen: the values' own range takes a wide window of the palette, placed where the values sit on the
# shared scale (warm stays warm, calm stays calm). Each stretched legend draws the shared scale as a thin bar with the
# stretched part bracketed, then its own bar with ticks in true units: the colours exaggerate, the numbers stay exact.
# v16.4: every picture whose values do not fill the shared scale is stretched, and the closer its extremes the more:
# the values' range always gets at least STRETCH_TO of the palette, so the gain is STRETCH_TO x scale / range (v16.3
# stretched only below 40 % of the scale, so wind, spread over about half of its scale, kept its close blues)
STRETCH_BELOW = 1.0     # stretch when the values (min-max, or 1st-99th percentile) span less than this share of the scale
STRETCH_TO = 0.75       # and give them at least this share of the palette
WIND_SCALE_HI = 15.0    # m/s: v16.4: wind takes Windy's colours from calm (0) to 15 m/s (blue, teal, green, olive, brown),
#                         all of them spread over the picture's own range; Windy's colours below the mean winds of the
#                         site (0-5 m/s) are only blues, which is why v16.3's wind pictures read as one colour
WIND_STRETCH_TO = 1.0   # the whole of that part of the palette


def finite_values(vals):
    """Every finite number in a field: a numpy array, or nested lists with None for no value."""
    if isinstance(vals, np.ndarray) and vals.dtype != object:
        v = vals.astype(float).ravel()
        return v[np.isfinite(v)]
    out = []
    stack = [vals]
    while stack:
        x = stack.pop()
        if x is None:
            continue
        if isinstance(x, (list, tuple, np.ndarray)):
            stack.extend(x)
            continue
        f = float(x)
        if math.isfinite(f):
            out.append(f)
    return np.asarray(out, float)


def analysis_window(S, kind):
    """v16.5: ONE colour window per analysis (kind "wind", "ta" or "utci"), shared by its plan's four seasons and every
    section of every line and season, so pictures compare with each other (v16.4 stretched each picture to its own
    values). The window is the 0.5th-99.5th percentile of all their values pooled; values beyond it take the end
    colours. Returns (a, b)."""
    CF = S.env["comfort"]
    lines = tsec_lines(S)
    sec_key = {"wind": "wind_sections", "ta": "air_sections", "utci": "felt_sections"}[kind]
    plan_k = {"wind": "uped", "ta": "ta", "utci": "utci"}[kind]
    memo = env_memo(S)
    mk = ("analysis_window", kind, S.env["keys"].get("comfort"), repr(lines.get(sec_key, [])), WINDOW_PCT)
    r = memo.get(mk)
    if r is not None:
        return r
    parts = []
    for sd in SEASONS:
        v = np.asarray(CF["seasons"][sd["key"]][plan_k], float).ravel()
        parts.append(v[np.isfinite(v)])
    for k, a, b in lines.get(sec_key, []):
        cf = tsec_comfort(S, tsec_geom(S, a, b))
        for sd in SEASONS:
            parts.append(finite_values(cf["seasons"][sd["key"]][kind]))
    v = np.concatenate([q for q in parts if q.size]) if any(q.size for q in parts) else np.zeros(0)
    if v.size < 2:
        r = None
    else:
        a, b = (float(q) for q in np.percentile(v, [WINDOW_PCT, 100.0 - WINDOW_PCT]))
        r = (a, b) if b > a else None
    memo[mk] = r
    return r


WINDOW_PCT = 0.5          # v16.5: the shared window leaves out this percentage of the values at either end


def stretch_scale(stops, lo, hi, vals, below=STRETCH_BELOW, to=STRETCH_TO, ab=None):
    """(lut, a, b, gain) for one picture. Not stretched: the shared [lo, hi] scale, gain 1.0. Stretched: the values'
    range [a, b] (min-max; the 1st-99th percentile when a few outliers alone make it wide) takes the colours of a window
    to x (hi - lo) wide on the shared palette, centred on where the values sit (kept inside the scale); gain = how many
    times the colours are stretched. Values beyond [a, b] (only the outer 1 % when percentiles were used) take the end
    colours."""
    plain = (stops_table(stops, lo, hi), lo, hi, 1.0)
    span = float(hi - lo)
    if ab is not None:                                # v16.5: the analysis' shared window (analysis_window)
        a, b = max(lo, ab[0]), min(hi, ab[1])
        if span <= 0 or b - a <= 1e-6 * span or b - a >= below * span:
            return plain
        v = None
    else:
        v = finite_values(vals)
        if v.size < 2 or span <= 0:
            return plain
        a, b = float(v.min()), float(v.max())
    if v is not None and b - a >= below * span:
        a, b = (float(q) for q in np.percentile(v, [1.0, 99.0]))
        if b - a >= below * span:
            return plain
    if b - a <= 1e-6 * span:                          # one value only: nothing to tell apart
        return plain
    width = max(to * span, b - a)                     # v16.4: never compressed (gain >= 1)
    gain = width / (b - a)
    c = min(max(0.5 * (a + b), lo + 0.5 * width), hi - 0.5 * width)
    pa = c - 0.5 * width
    st = [(a + (x - pa) / gain, col) for x, col in stops]     # the palette's stops in this picture's units
    return stops_table(st, a, b), a, b, gain


VAL_DEC = 2              # v16.6: values with decimals (temperatures, wind, kWh, dB) are printed with at least 2
VAL_FMT = "%.2f"         # (Nil: "we need at least 2 decimals"); counts, percentages, heights and distances unchanged


def tick_fmt(step, dec=None):
    """'%.Nf' with as many decimals as a tick step needs (v16.6: at least dec)."""
    d = dec or 0
    while d < 4 and abs(step * 10 ** d - round(step * 10 ** d)) > 1e-6:
        d += 1
    return "%." + str(d) + "f"


def stretch_bar(B, x, y, w, stops, lo, hi, sc, U, L, title, k=1.0, th=0.3, vals=None, dec=VAL_DEC):
    """Colour bar for a picture coloured with stretch_scale (sc). Stretched: the shared [lo, hi] scale as a thin bar with
    the stretched part bracketed, then the stretched bar with ticks in true units. k converts values to the unit shown
    (KT for knots). v16.5: the zoomed bar's two ends carry their numbers (the minimum and maximum of the analysis'
    shared window), and with vals this picture's own lowest and highest values are marked on it. Returns the y below
    it."""
    lut, a, b, gain = sc
    f10 = tick_fmt(nice_step((b - a) * k, 4) / 10.0, dec)
    if gain > 1.0:
        title += " · window {}-{}, plan + sections · colours x{}".format(          # v38: keywords (was a clause)
            f10 % (a * k), f10 % (b * k), ("%.1f" % gain) if gain < 9.95 else ("%.0f" % gain))
    B.fit(title, x, y, th * U, w, T_INK, L)
    y -= (0.35 + th) * U
    n = 60
    if gain > 1.0:
        full = stops_table(stops, lo, hi, 256)
        for q in range(n):
            B.fill([rect(x + w * q / n, y - 0.16 * U, x + w * (q + 1) / n + 0.01 * U, y)], full(lo + (hi - lo) * (q + 0.5) / n),
                   L, 30)
        f_ = tick_fmt(nice_step((hi - lo) * k, 4), dec)
        B.text(f_ % (lo * k), x - 0.12 * U, y - 0.15 * U, 0.18 * U, T_GREY, L, align="R")
        B.text(f_ % (hi * k), x + w + 0.12 * U, y - 0.15 * U, 0.18 * U, T_GREY, L)
        xa = x + w * (max(lo, a) - lo) / (hi - lo)
        xb = x + w * (min(hi, b) - lo) / (hi - lo)
        B.line([(xa, y + 0.06 * U), (xa, y - 0.22 * U), (xb, y - 0.22 * U), (xb, y + 0.06 * U)], T_INK, L, 31, 0.04)
        B.line([(xa, y - 0.22 * U), (x, y - 0.55 * U)], T_GREY, L, 31, 0.02)
        B.line([(xb, y - 0.22 * U), (x + w, y - 0.55 * U)], T_GREY, L, 31, 0.02)
        y -= 0.6 * U
        if vals is not None:                          # v16.5: room for the picture's min / max marks
            y -= 0.45 * U
    vv = finite_values(vals) if vals is not None else np.zeros(0)
    if vv.size and gain > 1.0:                        # v16.5: this picture's own lowest and highest values, above the bar
        for v_, lab_ in ((float(vv.min()), "min"), (float(vv.max()), "max")):
            tx = x + w * (min(b, max(a, v_)) - a) / (b - a)
            B.fill([[(tx, y + 0.02 * U), (tx - 0.12 * U, y + 0.22 * U), (tx + 0.12 * U, y + 0.22 * U)]], T_INK, L, 31)
            B.text("{} {}".format(lab_, f10 % (v_ * k)), tx, y + 0.3 * U, 0.2 * U, T_INK, L,
                   align="R" if lab_ == "min" else "L")
    for q in range(n):
        B.fill([rect(x + w * q / n, y - 0.45 * U, x + w * (q + 1) / n + 0.01 * U, y)], lut(a + (b - a) * (q + 0.5) / n), L, 30)
    step = nice_step((b - a) * k, 4)
    f_ = tick_fmt(step, dec)
    ends = gain > 1.0                                 # v16.5: the zoomed bar's ends carry their own numbers
    t = math.ceil(a * k / step - 1e-9) * step
    while t <= b * k + 1e-9:
        tx = x + w * (t / k - a) / (b - a)
        if not ends or min(tx - x, x + w - tx) > 0.9 * U:
            B.line([(tx, y - 0.45 * U), (tx, y - 0.62 * U)], T_INK, L, 31, 0.04)
            B.text(f_ % t, tx, y - 1.0 * U, 0.24 * U, T_INK, L, align="C")
        t += step
    if ends:
        for tx, v_, al in ((x, a, "L"), (x + w, b, "R")):
            B.line([(tx, y - 0.45 * U), (tx, y - 0.7 * U)], T_INK, L, 31, 0.06)
            B.text(f10 % (v_ * k), tx, y - 1.0 * U, 0.26 * U, T_INK, L, align=al, bold=True)
    return y - 1.45 * U


def stretch_levels(sc, base):
    """Contour levels for a stretched picture (about five inside its range); the given ones when not stretched."""
    lut, a, b, gain = sc
    if gain <= 1.0:
        return base
    step = nice_step(b - a, 5)
    v = math.ceil(a / step + 1e-9) * step
    out = []
    while v < b - 1e-9:
        out.append(round(v, 6))
        v += step
    return out


# ------------------------------------------------------------ the three sheets
# ============================================================ SECTION ART: a small raster engine (numpy only)
# Anti-aliased polygons, strokes and soft discs on a float RGB canvas, composited with "over". Used to draw the soft
# part of every section (trees at their measured size, buildings beyond the cut, ground beyond, scale figures, the
# analysis wash); the crisp part (the cut, the ground line, text) stays vector on top of the picture.


class SArt(object):
    """A canvas in pixels: x to the right, y down. rgb is float32 0..1."""

    def __init__(self, W, H, bg=(1.0, 1.0, 1.0)):
        self.W, self.H = int(W), int(H)
        self.rgb = np.empty((self.H, self.W, 3), np.float32)
        self.rgb[:] = np.asarray(bg, np.float32)

    def over(self, x0, y0, cov, col, alpha=1.0):
        """Composite colour col (rgb 0..1, or an (h, w, 3) array) with coverage cov (h, w) at (x0, y0)."""
        h, w = cov.shape
        xa, ya = max(0, x0), max(0, y0)
        xb, yb = min(self.W, x0 + w), min(self.H, y0 + h)
        if xb <= xa or yb <= ya:
            return
        c = cov[ya - y0:yb - y0, xa - x0:xb - x0]
        a = (c * alpha)[..., None]
        dst = self.rgb[ya:yb, xa:xb]
        if isinstance(col, np.ndarray) and col.ndim == 3:
            src = col[ya - y0:yb - y0, xa - x0:xb - x0]
        else:
            src = np.asarray(col, np.float32)
        dst *= (1.0 - a)
        dst += a * src

    def to_bytes(self):
        return (np.clip(self.rgb, 0.0, 1.0) * 255.0 + 0.5).astype(np.uint8)


def sa_poly_cov(polys, ss=4, clip=None):
    """Even-odd coverage of one or more rings (lists of (x, y) pixel points): exact across x, ss samples per pixel down y.
    Returns (x0, y0, cov) or None. clip = (W, H) limits the box."""
    rings = [np.asarray(P, np.float64) for P in polys if P is not None and len(P) >= 3]
    if not rings:
        return None
    allp = np.concatenate(rings)
    x0 = int(math.floor(allp[:, 0].min()))
    y0 = int(math.floor(allp[:, 1].min()))
    x1 = int(math.ceil(allp[:, 0].max())) + 1
    y1 = int(math.ceil(allp[:, 1].max())) + 1
    if clip is not None:
        x0, y0 = max(x0, 0), max(y0, 0)
        x1, y1 = min(x1, clip[0]), min(y1, clip[1])
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0:
        return None
    ax, ay, bx, by = [], [], [], []
    for R in rings:
        S_ = np.roll(R, -1, axis=0)
        ax.append(R[:, 0]); ay.append(R[:, 1]); bx.append(S_[:, 0]); by.append(S_[:, 1])
    ax = np.concatenate(ax) - x0
    ay = np.concatenate(ay) - y0
    bx = np.concatenate(bx) - x0
    by = np.concatenate(by) - y0
    keep = ay != by
    ax, ay, bx, by = ax[keep], ay[keep], bx[keep], by[keep]
    if ax.size == 0:
        return None
    ys = (np.arange(h * ss) + 0.5) / ss                          # sample rows
    # crossings of every edge with every sample row (half-open in y so vertices count once)
    lo = np.minimum(ay, by)
    hi = np.maximum(ay, by)
    out_cov = np.zeros((h, w + 2), np.float64)
    # process sample rows in chunks to bound memory
    E = ax.size
    chunk = max(1, int(4_000_000 // max(1, E)))
    for r0 in range(0, ys.size, chunk):
        yy = ys[r0:r0 + chunk][:, None]
        m = (yy >= lo) & (yy < hi)
        if not m.any():
            continue
        t = (yy - ay) / (by - ay)
        xs = np.where(m, ax + t * (bx - ax), np.inf)
        xs.sort(axis=1)
        k = m.sum(axis=1)
        kmax = int(k.max())
        if kmax < 2:
            continue
        xs = xs[:, :kmax - (kmax % 2)]
        a_ = xs[:, 0::2]
        b_ = xs[:, 1::2]
        ok = np.isfinite(a_) & np.isfinite(b_)
        rows = np.broadcast_to(((np.arange(r0, r0 + yy.shape[0])) // ss)[:, None], a_.shape)[ok]
        a_ = np.clip(a_[ok], 0.0, w)
        b_ = np.clip(b_[ok], 0.0, w)
        good = b_ > a_
        if not good.any():
            continue
        rows, a_, b_ = rows[good], a_[good], b_[good]
        # integral F(i) = sum over spans of clip(i - a, 0, b - a); pixel i covers F(i + 1) - F(i)
        W2 = w + 2
        for v, sgn in ((a_, 1.0), (b_, -1.0)):
            ci = np.ceil(v).astype(np.int64)
            idx = rows * W2 + np.clip(ci, 0, W2 - 1)
            cnt = np.bincount(idx, minlength=h * W2).reshape(h, W2)
            sm = np.bincount(idx, weights=v, minlength=h * W2).reshape(h, W2)
            c = np.cumsum(cnt, axis=1)
            s = np.cumsum(sm, axis=1)
            i = np.arange(W2)[None, :]
            out_cov += sgn * (i * c - s)
    cov = (out_cov[:, 1:w + 1] - out_cov[:, :w]) / ss
    return x0, y0, np.clip(cov, 0.0, 1.0).astype(np.float32)


def sa_fill(art, polys, col, alpha=1.0, ss=4):
    r = sa_poly_cov(polys, ss, clip=(art.W, art.H))
    if r is not None:
        art.over(r[0], r[1], r[2], col, alpha)


def sa_stroke_polys(P, w):
    """Quads (and small square joints) covering a polyline of width w (pixels)."""
    out = []
    hw = 0.5 * w
    for i in range(len(P) - 1):
        (x0, y0), (x1, y1) = P[i], P[i + 1]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        if L < 1e-9:
            continue
        nx, ny = -dy / L * hw, dx / L * hw
        ex, ey = dx / L * hw * 0.5, dy / L * hw * 0.5           # a short cap so joints close
        out.append([(x0 - ex + nx, y0 - ey + ny), (x1 + ex + nx, y1 + ey + ny), (x1 + ex - nx, y1 + ey - ny),
                    (x0 - ex - nx, y0 - ey - ny)])
    return out


def sa_line_cov(P, w, clip, ss=4):
    """Coverage of a stroked polyline (union of its segment quads, max-combined)."""
    quads = sa_stroke_polys(P, w)
    if not quads:
        return None
    allp = np.asarray([p for q in quads for p in q])
    x0 = max(0, int(math.floor(allp[:, 0].min())))
    y0 = max(0, int(math.floor(allp[:, 1].min())))
    x1 = min(clip[0], int(math.ceil(allp[:, 0].max())) + 1)
    y1 = min(clip[1], int(math.ceil(allp[:, 1].max())) + 1)
    if x1 <= x0 or y1 <= y0:
        return None
    acc = np.zeros((y1 - y0, x1 - x0), np.float32)
    for q in quads:
        r = sa_poly_cov([q], ss, clip=clip)
        if r is None:
            continue
        qx, qy, c = r
        h, w_ = c.shape
        sub = acc[qy - y0:qy - y0 + h, qx - x0:qx - x0 + w_]
        np.maximum(sub, c[:sub.shape[0], :sub.shape[1]], out=sub)
    return x0, y0, acc


def sa_stroke(art, P, w, col, alpha=1.0):
    r = sa_line_cov(P, w, (art.W, art.H))
    if r is not None:
        art.over(r[0], r[1], r[2], col, alpha)


def sa_blob_cov(cx, cy, r, soft=0.8, wob=None, clip=None):
    """A disc of radius r (pixels) with an edge softened over `soft` pixels; wob = [(amplitude, frequency, phase)]
    makes the edge irregular (leaf clumps)."""
    R = r * (1.0 + (sum(abs(a) for a, f, p in wob) if wob else 0.0)) + soft + 1.0
    x0, y0 = int(math.floor(cx - R)), int(math.floor(cy - R))
    x1, y1 = int(math.ceil(cx + R)) + 1, int(math.ceil(cy + R)) + 1
    if clip is not None:
        x0, y0 = max(0, x0), max(0, y0)
        x1, y1 = min(clip[0], x1), min(clip[1], y1)
    if x1 <= x0 or y1 <= y0:
        return None
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    dx, dy = xx + 0.5 - cx, yy + 0.5 - cy
    d = np.sqrt(dx * dx + dy * dy)
    rr = np.float32(r)
    if wob:
        th = np.arctan2(dy, dx)
        m = np.ones_like(th)
        for a, f, p in wob:
            m += a * np.sin(f * th + p)
        rr = r * m
    cov = np.clip((rr - d) / max(0.5, soft) + 0.5, 0.0, 1.0)
    return x0, y0, cov.astype(np.float32)


def sa_blob(art, cx, cy, r, col, alpha=1.0, soft=0.8, wob=None):
    b = sa_blob_cov(cx, cy, r, soft, wob, (art.W, art.H))
    if b is not None:
        art.over(b[0], b[1], b[2], col, alpha)


def sa_mix(a, b, t):
    return tuple(float(a[i]) * (1.0 - t) + float(b[i]) * t for i in range(3))


# ============================================================ SECTION ART: trees and scale figures

# foliage palettes (light, mid, shadow), 0..255: deciduous by season, evergreen broadleaf (olive), needle-leaved
SA_TREE_PAL = {
    "tree": ((178, 196, 132), (140, 164, 102), (104, 128, 82)),
    "tree_spring": ((198, 214, 146), (168, 192, 114), (132, 158, 94)),
    "tree_autumn": ((196, 190, 124), (166, 160, 100), (128, 128, 84)),
    "olive": ((190, 196, 166), (154, 164, 132), (116, 128, 104)),
    "pine": ((132, 158, 124), (100, 128, 102), (74, 98, 82)),
}
SA_TRUNK = (110, 98, 90)


class SASprite(object):
    """A small premultiplied RGBA buffer a tree is drawn into before it is laid on the canvas as one piece."""

    def __init__(self, x0, y0, w, h):
        self.x0, self.y0, self.w, self.h = int(x0), int(y0), int(w), int(h)
        self.c = np.zeros((self.h, self.w, 3), np.float32)
        self.a = np.zeros((self.h, self.w), np.float32)

    def over(self, x0, y0, cov, col, alpha=1.0):
        h, w = cov.shape
        xa, ya = max(self.x0, x0), max(self.y0, y0)
        xb, yb = min(self.x0 + self.w, x0 + w), min(self.y0 + self.h, y0 + h)
        if xb <= xa or yb <= ya:
            return
        s = (cov[ya - y0:yb - y0, xa - x0:xb - x0] * alpha)
        dc = self.c[ya - self.y0:yb - self.y0, xa - self.x0:xb - self.x0]
        da = self.a[ya - self.y0:yb - self.y0, xa - self.x0:xb - self.x0]
        k = (1.0 - s)
        dc *= k[..., None]
        dc += s[..., None] * np.asarray(col, np.float32)
        da *= k
        da += s

    def onto(self, art, alpha=1.0, toward=None, fade=0.0):
        """Lay the sprite on the canvas; fade > 0 mixes its colours toward `toward` (atmosphere)."""
        xa, ya = max(0, self.x0), max(0, self.y0)
        xb, yb = min(art.W, self.x0 + self.w), min(art.H, self.y0 + self.h)
        if xb <= xa or yb <= ya:
            return
        c = self.c[ya - self.y0:yb - self.y0, xa - self.x0:xb - self.x0]
        a = self.a[ya - self.y0:yb - self.y0, xa - self.x0:xb - self.x0]
        if fade > 0.0 and toward is not None:
            c = c * (1.0 - fade) + a[..., None] * np.asarray(toward, np.float32) * fade
        k = (a * alpha)[..., None]
        dst = art.rgb[ya:yb, xa:xb]
        dst *= (1.0 - k)
        dst += c * alpha


#@include ../../common/_sa_c.py


def _sa_mix(a, b, t):
    return tuple(a[i] * (1.0 - t) + b[i] * t for i in range(3))


def sa_tree(kind, px, gy, yb, yt, hw, seed, leaf=1.0, season=""):
    """One tree in elevation at its measured size, pixels: trunk from the ground (gy) to the crown base (yb), crown
    from yb up to yt, hw wide each side. leaf: share of foliage for deciduous crowns (0 = bare)."""
    rnd = random.Random(seed)
    hh = 0.5 * (yb - yt)                       # crown half height (pixels, y down)
    if hh < 0.6 or hw < 0.6:
        return None
    cy = 0.5 * (yb + yt)
    pad = 2.0
    x0 = int(math.floor(px - hw * 1.3 - pad))
    y0 = int(math.floor(yt - hh * 0.3 - pad))
    x1 = int(math.ceil(px + hw * 1.3 + pad))
    y1 = int(math.ceil(gy + pad))
    sp = SASprite(x0, y0, x1 - x0, y1 - y0)
    clip = None
    size = max(hw, hh)
    if kind == "pine":
        pal = SA_TREE_PAL["pine"]
    elif kind == "olive":
        pal = SA_TREE_PAL["olive"]
    else:
        pal = SA_TREE_PAL.get("tree_" + season, SA_TREE_PAL["tree"])
    lt, md, sh = _sa_c(pal[0]), _sa_c(pal[1]), _sa_c(pal[2])
    trunk = _sa_c(SA_TRUNK)
    lean = rnd.uniform(-0.06, 0.06) * hh
    # ---- trunk: tapered, a little leaning, into the lower crown
    tb = max(0.7, min(0.16 * hw, 0.05 * (gy - yt) + 0.6))        # trunk width at the ground (pixels)
    tt = max(0.5, 0.55 * tb)
    ytop_tr = yb - (0.35 if kind != "pine" else 0.9) * (yb - yt) * (0.5 if leaf > 0.3 or kind != "tree" else 1.0)
    tr = [(px - tb / 2, gy), (px + tb / 2, gy), (px + lean + tt / 2, ytop_tr), (px + lean - tt / 2, ytop_tr)]
    r = sa_poly_cov([tr], 4)
    if r is not None:
        sp.over(r[0], r[1], r[2], trunk, 0.95)
    # ---- branches: a few limbs into the crown; for a bare deciduous crown the whole structure, finer and finer
    if kind != "pine":
        nb = 3 + rnd.randint(0, 2)
        depth = 4 if (kind == "tree" and leaf < 0.5) else 2
        stack = []
        for k in range(nb):
            ang = math.radians(rnd.uniform(-58, 58) + (k - (nb - 1) / 2.0) * 10.0)
            ln = (0.55 + 0.35 * rnd.random()) * hh * 1.25
            stack.append((px + lean * 0.8, yb - 0.05 * (yb - yt), ang, ln, max(0.5, tt * 0.75), depth))
        while stack:
            bx, by, ang, ln, wd, dp = stack.pop()
            ex, ey = bx + math.sin(ang) * ln * (hw / max(hh, 1e-6)) ** 0.5, by - math.cos(ang) * ln
            # keep inside the crown envelope
            nx_, ny_ = (ex - px) / max(hw, 1e-6), (ey - cy) / max(hh, 1e-6)
            m = math.hypot(nx_, ny_)
            lim = 0.92 if (kind == "tree" and leaf < 0.5) else 0.62
            if m > lim:
                ex, ey = px + nx_ / m * lim * hw, cy + ny_ / m * lim * hh
            rr = sa_line_cov([(bx, by), (ex, ey)], wd, (10 ** 9, 10 ** 9))
            if rr is not None:
                sp.over(rr[0], rr[1], rr[2], trunk, 0.85 if leaf < 0.5 or kind != "tree" else 0.7)
            if dp > 1 and wd > 0.35:
                for sgn in (-1, 1):
                    stack.append((ex * 0.4 + bx * 0.6, ey * 0.4 + by * 0.6, ang + sgn * math.radians(rnd.uniform(22, 38)),
                                  ln * rnd.uniform(0.5, 0.68), wd * 0.62, dp - 1))
                stack.append((ex, ey, ang + math.radians(rnd.uniform(-18, 18)), ln * 0.55, wd * 0.6, dp - 1))
    # ---- foliage
    if kind == "tree" and leaf <= 0.02:
        return sp
    dens = leaf if kind == "tree" else 1.0
    if kind == "pine" and hw < 0.42 * hh:
        _sa_cypress(sp, rnd, px + lean, yb, yt, hw, lt, md, sh)
        return sp
    if kind == "pine":
        _sa_pine(sp, rnd, px + lean, yb, yt, hw, hh, lt, md, sh)
        return sp
    # rounded crowns (deciduous, olive): a mass, then leaf clumps over it, lit from the upper left
    _sa_round(sp, rnd, px + lean * 0.6, cy, hw, hh, lt, md, sh, dens, kind)
    return sp


def _sa_lumpy(rnd, cx, cy, rx, ry, n=28, amp=0.06):
    ph = [rnd.uniform(0, 6.3) for _ in range(3)]
    P = []
    for q in range(n):
        a = 2 * math.pi * q / n
        k = 1.0 + amp * (math.sin(5 * a + ph[0]) + 0.6 * math.sin(8 * a + ph[1]) + 0.4 * math.sin(13 * a + ph[2])) / 2.0
        P.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
    return P


def _sa_round(sp, rnd, cx, cy, hw, hh, lt, md, sh, dens, kind):
    olive = kind == "olive"
    a_mass = (0.88 if not olive else 0.82) * (0.35 + 0.65 * dens)
    # the mass: slightly smaller than the envelope so the clumps make the edge
    P = _sa_lumpy(rnd, cx, cy + 0.04 * hh, hw * 0.86, hh * 0.84, amp=0.08)
    r = sa_poly_cov([P], 4)
    if r is not None:
        sp.over(r[0], r[1], r[2], _sa_mix(md, sh, 0.25), a_mass)
    m = min(hw, hh)
    rc = max(0.9, (0.22 if olive else 0.26) * m + 0.04 * max(hw, hh))
    area = math.pi * hw * hh
    n = int(max(8, min(90, 2.2 * area / (math.pi * rc * rc))))
    n = max(4, int(round(n * (0.35 + 0.65 * dens))))
    pts = []
    nr = int(n * 0.5)
    for k in range(n):
        if k < nr:                                          # the rim: a scalloped silhouette
            th = 2 * math.pi * (k + rnd.random() * 0.7) / max(1, nr)
            rr_ = 0.80 + 0.12 * rnd.random()
            sz = rnd.uniform(0.7, 1.0)
        else:
            th = rnd.uniform(0, 2 * math.pi)
            rr_ = math.sqrt(rnd.random()) * 0.75
            sz = rnd.uniform(0.85, 1.25)
        pts.append((cx + math.cos(th) * rr_ * (hw - rc * 0.5), cy + math.sin(th) * rr_ * (hh - rc * 0.5), sz))

    def light(p):
        return -((p[0] - cx) / max(hw, 1e-6)) * 0.55 - ((p[1] - cy) / max(hh, 1e-6)) * 0.85
    pts.sort(key=light)
    alpha = (0.9 if not olive else 0.86) * (0.5 + 0.5 * dens)
    for (x_, y_, sz) in pts:
        lv = max(0.0, min(1.0, 0.5 + 0.55 * light((x_, y_))))
        col = _sa_mix(sh, md, min(1.0, lv * 1.9)) if lv < 0.52 else _sa_mix(md, lt, (lv - 0.52) / 0.48)
        j = rnd.uniform(-0.03, 0.03)
        col = tuple(max(0.0, min(1.0, c_ + j)) for c_ in col)
        rk = rc * sz
        wob = [(rnd.uniform(0.06, 0.13), rnd.choice((5, 6, 7)), rnd.uniform(0, 6.3)),
               (rnd.uniform(0.03, 0.06), rnd.choice((9, 11, 13)), rnd.uniform(0, 6.3))]
        b = sa_blob_cov(x_, y_, rk, soft=0.85, wob=wob)
        if b is not None:
            sp.over(b[0], b[1], b[2], col, alpha)
    # a few bright touches on the lit side
    for k in range(max(2, n // 8)):
        th = rnd.uniform(math.pi * 1.05, math.pi * 1.6)
        rr_ = rnd.uniform(0.35, 0.7)
        b = sa_blob_cov(cx + math.cos(th) * rr_ * hw, cy + math.sin(th) * rr_ * hh, rc * rnd.uniform(0.45, 0.7), soft=0.9)
        if b is not None:
            sp.over(b[0], b[1], b[2], _sa_mix(lt, (1.0, 1.0, 1.0), 0.18), 0.55 * alpha)


def _sa_cypress(sp, rnd, px, yb, yt, hw, lt, md, sh):
    """A narrow needle-leaved crown (cypress-like flame) at its measured width and height, with a scalloped edge."""
    H = yb - yt
    n = max(12, int(H / 1.5))
    left, right = [], []
    ph = rnd.uniform(0, 6.3)
    for k in range(n + 1):
        t = k / float(n)                                    # 0 = top, 1 = crown base
        w = hw * (math.sin(min(1.0, t * 1.2) * math.pi * 0.5) ** 0.75) * (1.0 - 0.25 * max(0.0, t - 0.88) / 0.12)
        bump = 1.0 + 0.10 * math.sin(t * 23.0 + ph) + rnd.uniform(-0.05, 0.05)
        y = yt + t * H
        left.append((px - w * bump, y))
        right.append((px + w * (2.0 - bump) * 0.98, y))
    P = right + left[::-1]
    r = sa_poly_cov([P], 4)
    if r is not None:
        sp.over(r[0], r[1], r[2], md, 0.95)
    P2 = [(x * 0.5 + (px - 0.05 * hw) * 0.5, y) for x, y in left[1:-1]] + [(px - 0.05 * hw, yb - 0.08 * H), (px - 0.05 * hw, yt + 0.08 * H)]
    r = sa_poly_cov([P2], 4)
    if r is not None:
        sp.over(r[0], r[1], r[2], lt, 0.5)
    P3 = [(x * 0.55 + (px + 0.25 * hw) * 0.45, y) for x, y in right[2:-1]][::-1] + [(px + 0.25 * hw, yt + 0.15 * H), (px + 0.25 * hw, yb - 0.1 * H)]
    r = sa_poly_cov([P3], 4)
    if r is not None:
        sp.over(r[0], r[1], r[2], sh, 0.45)


def _sa_pine(sp, rnd, px, yb, yt, hw, hh, lt, md, sh):
    """A needle-leaved crown: flat tufts on bare limbs, the widest near the top, at its measured width and height."""
    H = yb - yt
    trunk = _sa_c(SA_TRUNK)
    pads = []
    # the canopy: a broad, lumpy top layer
    ntop = 3 + rnd.randint(0, 2)
    for k in range(ntop):
        tx = px + (k - (ntop - 1) / 2.0) / max(1.0, (ntop - 1) / 2.0) * hw * 0.55 + rnd.uniform(-0.08, 0.08) * hw
        ty = yt + H * rnd.uniform(0.16, 0.32)
        pads.append((tx, ty, hw * rnd.uniform(0.42, 0.58), H * rnd.uniform(0.15, 0.22)))
    # lower tufts, alternating sides, smaller downwards
    nlow = max(1, min(5, int(H / max(3.0, hw * 0.7))))
    for k in range(nlow):
        t = 0.42 + 0.5 * (k + 0.5) / nlow
        side = -1 if (k + rnd.randint(0, 1)) % 2 else 1
        sc = 1.0 - 0.45 * t
        tx = px + side * hw * rnd.uniform(0.25, 0.5) * sc
        ty = yt + t * H
        pads.append((tx, ty, hw * rnd.uniform(0.3, 0.45) * sc, H * rnd.uniform(0.09, 0.14)))
        rr = sa_line_cov([(px, ty + 0.12 * H), (tx, ty)], max(0.45, hw * 0.045), (10 ** 9, 10 ** 9))
        if rr is not None:
            sp.over(rr[0], rr[1], rr[2], trunk, 0.85)
    for k in range(ntop):
        tx, ty = pads[k][0], pads[k][1]
        rr = sa_line_cov([(px, yt + 0.55 * H), (tx, ty + 0.05 * H)], max(0.45, hw * 0.05), (10 ** 9, 10 ** 9))
        if rr is not None:
            sp.over(rr[0], rr[1], rr[2], trunk, 0.85)
    pads.sort(key=lambda p: -p[1])
    for tx, ty, rx, ry in pads:
        P = _sa_lumpy(rnd, tx, ty, rx, ry, n=24, amp=0.14)
        P = [(x, y if y < ty else ty + (y - ty) * 0.75) for x, y in P]          # flatter underside
        r = sa_poly_cov([P], 4)
        if r is not None:
            sp.over(r[0], r[1], r[2], _sa_mix(md, sh, 0.35), 0.93)
        P2 = _sa_lumpy(rnd, tx - rx * 0.12, ty - ry * 0.25, rx * 0.72, ry * 0.55, n=20, amp=0.12)
        r = sa_poly_cov([P2], 4)
        if r is not None:
            sp.over(r[0], r[1], r[2], _sa_mix(md, lt, 0.55), 0.75)


# ---- scale figures: simple silhouettes in metres (feet at 0, 0; y up), 1.75 m tall before scaling
SA_FIGS = [
    # standing
    [(-0.10, 0.0), (-0.06, 0.0), (-0.03, 0.82), (0.03, 0.82), (0.06, 0.0), (0.10, 0.0), (0.12, 0.85), (0.16, 1.38),
     (0.10, 1.47), (0.05, 1.50), (0.05, 1.53), (-0.05, 1.53), (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.12, 0.85)],
    # walking
    [(-0.30, 0.0), (-0.24, 0.0), (-0.02, 0.78), (0.18, 0.0), (0.25, 0.0), (0.11, 0.86), (0.18, 1.12), (0.12, 1.40),
     (0.06, 1.48), (0.05, 1.53), (-0.05, 1.53), (-0.07, 1.47), (-0.14, 1.38), (-0.20, 1.10), (-0.12, 0.86)],
    # in a dress / long coat
    [(-0.20, 0.0), (0.20, 0.0), (0.13, 0.62), (0.11, 1.08), (0.15, 1.36), (0.09, 1.45), (0.05, 1.49), (0.05, 1.52),
     (-0.05, 1.52), (-0.05, 1.49), (-0.09, 1.45), (-0.15, 1.36), (-0.11, 1.08), (-0.13, 0.62)],
    # with a bag
    [(-0.11, 0.0), (-0.06, 0.0), (-0.02, 0.80), (0.04, 0.80), (0.08, 0.0), (0.13, 0.0), (0.12, 0.86), (0.30, 0.86),
     (0.30, 0.55), (0.40, 0.55), (0.40, 0.95), (0.17, 1.38), (0.10, 1.47), (0.05, 1.51), (0.05, 1.53), (-0.05, 1.53),
     (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.13, 0.86)],
]
SA_HEAD = (0.0, 1.64, 0.105)


def sa_figure(kind, x, gz, scale, flip, ppm, x_px, y_px):
    """A figure's body and head in pixels: x along the line (m), gz ground level (m); x_px, y_px map (s, z) -> px."""
    body = SA_FIGS[kind % len(SA_FIGS)]
    sg = -1.0 if flip else 1.0
    P = [x_px(x + sg * bx * scale) for bx, by in body]
    P = [(x_px(x + sg * bx * scale), y_px(gz + by * scale)) for bx, by in body]
    hx, hy, hr = SA_HEAD
    return P, (x_px(x + sg * hx * scale), y_px(gz + hy * scale), hr * scale * ppm)


# ============================================================ SECTION ART: what a section sees beyond its cut
# Everything here is measured: the ground beyond (survey terrain), the buildings beyond (survey footprints at their
# heights), the trees (canopy height map: crown radius, height, leaf type). Only the scale figures are not data: they
# stand on the walkable ground of the cut to give the scale, as in any architectural section.
SA_DEPTH_B = 120.0          # m: buildings beyond the cut are drawn up to this distance
SA_DEPTH_T = 90.0           # m: trees beyond the cut
SA_BANDS = (5.0, 10.0, 16.0, 24.0, 34.0, 46.0, 60.0, 76.0, 95.0, 118.0)    # m: the ground beyond, seen at these depths


def sa_crowns(S):
    """Every crown of the canopy height map near the frame as (x, y, radius, height, kind), on a grid; crowns standing on
    a roof are misreadings and left out, as in the analyses."""
    g = getattr(S, "g_sacrown", None)
    if g is not None:
        return g
    E = (getattr(S, "env", None) or {}).get("E")
    if E is None and ENV_PATH:
        try:
            E, _ = load_env(ENV_PATH)
        except Exception:
            E = None
    fb = S.F.bb
    g = Grid(20.0)
    for row in (E or {}).get("trees", []):
        x, y, r, h = row[:4]
        if h < 3.0 or not (fb[0] - 150 <= x <= fb[2] + 150 and fb[1] - 150 <= y <= fb[3] + 150):
            continue
        if any(in_unit(x, y, u) for u in S.g_bld.query((x, y, x, y))):
            continue
        kind = LEAF_KIND.get(int(row[4]), "tree") if len(row) > 5 else "tree"
        g.add((x, y, r, h, kind), (x - r, y - r, x + r, y + r))
    S.g_sacrown = g
    return g


def sa_scene(S, a, b):
    """The view beyond the cut a -> b, looking to its left (as every section of this script): ground at SA_BANDS depths,
    buildings and crowns beyond, bridges, and where scale figures may stand on the cut. Absolute heights (m a.s.l.)."""
    memo = getattr(S, "_sa_memo", None)
    if memo is None:
        memo = S._sa_memo = {}
    mk = (tuple(a), tuple(b))
    if mk in memo:
        return memo[mk]
    (x0, y0), (x1, y1) = a, b
    L = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    nx, ny = -uy, ux
    F = S.F
    # ---- the ground beyond: one profile per depth, cut where it leaves the surveyed terrain (frame + 40 m)
    ns = max(2, int(L / 1.5) + 1)
    ss_ = np.linspace(0.0, L, ns)
    bands = []
    for d in SA_BANDS:
        X = x0 + ux * ss_ + nx * d
        Y = y0 + uy * ss_ + ny * d
        Z = z_np(S, X, Y)
        lu = F._lc * (X - F.cx) - F._ls * (Y - F.cy)
        lv = F._ls * (X - F.cx) + F._lc * (Y - F.cy)
        ok = (lu >= F.u0 - 40.0) & (lu <= F.u1 + 40.0) & (lv >= F.v0 - 40.0) & (lv <= F.v1 + 40.0)
        bands.append((d, ss_.copy(), np.where(ok, Z, np.nan)))
    # ---- buildings beyond: the survey footprint seen from the cut, from its lowest ground to its roof
    band = (min(x0, x1, x0 + nx * SA_DEPTH_B, x1 + nx * SA_DEPTH_B) - 5.0,
            min(y0, y1, y0 + ny * SA_DEPTH_B, y1 + ny * SA_DEPTH_B) - 5.0,
            max(x0, x1, x0 + nx * SA_DEPTH_B, x1 + nx * SA_DEPTH_B) + 5.0,
            max(y0, y1, y0 + ny * SA_DEPTH_B, y1 + ny * SA_DEPTH_B) + 5.0)
    bld = []
    for u in S.g_bld.query(band):
        if u.get("h", 0.0) <= 0.0:
            continue
        pts = [p for P in u["parts"] for p in P]
        if not pts:
            continue
        dv = [(px - x0) * nx + (py - y0) * ny for px, py in pts]
        if min(dv) < 0.0 or min(dv) > SA_DEPTH_B:           # cut by the plane (drawn as cut) or behind the viewer
            continue
        sv = [(px - x0) * ux + (py - y0) * uy for px, py in pts]
        s0, s1 = max(0.0, min(sv)), min(L, max(sv))
        if s1 - s0 < 0.8:
            continue
        zc = S.z_at(u["cx"], u["cy"])
        zv = z_np(S, [p[0] for p in pts], [p[1] for p in pts])
        zb = float(min(zv.min(), zc))
        uf_ = unit_flags(u)
        bld.append(dict(s0=s0, s1=s1, zb=zb, base=zc, zt=zc + u["h"], d=min(dv), cat=u.get("cat", "residential"),
                        fabric=u.get("fabric", "regular"), floors=int(u.get("floors") or 1), annex=bool(u.get("annex")),
                        fsrc=u.get("floors_src", ""), mosque=uf_[0], ruin=uf_[2],
                        minaret=minaret_s(u, x0, y0, ux, uy, s0, s1) if u.get("fabric") == "sacred" else None))
    # ---- crowns: cut by the plane and beyond it (canopy height map)
    trees = []
    g = sa_crowns(S)
    tb = (band[0] - 10, band[1] - 10, band[2] + 10, band[3] + 10)
    for (tx, ty, tr, th, kind) in g.query(tb):
        d = (tx - x0) * nx + (ty - y0) * ny
        s = (tx - x0) * ux + (ty - y0) * uy
        if not (-tr < s < L + tr) or d < -0.5 * tr or d > SA_DEPTH_T:
            continue
        zg = S.z_at(tx, ty)
        trees.append(dict(s=s, zg=zg, lo=max(1.5, 0.35 * th), hi=th, r=tr, d=max(0.0, d), kind=kind,
                          seed=int(abs(tx * 7.31 + ty * 3.17) * 10) % 2147483647))
    # ---- bridges beyond (surveyed decks, at the level of the ground at their middle)
    bridges = []
    for P in getattr(S, "bridges", []) or []:
        if len(P) < 2:
            continue
        mx, my = sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
        d = (mx - x0) * nx + (my - y0) * ny
        if not 1.0 < d < SA_DEPTH_B:
            continue
        sv = [(px - x0) * ux + (py - y0) * uy for (px, py) in P]
        s0, s1 = max(0.0, min(sv)), min(L, max(sv))
        if s1 - s0 > 2.0:
            bridges.append(dict(s0=s0, s1=s1, z=S.z_at(mx, my), d=d))
    # ---- where scale figures may stand: walkable ground of the cut (streets, open ground, parks, parking)
    walk = []
    cur = None
    step = 1.0
    for k in range(int(L / step) + 1):
        s = k * step
        kd = classify_point(S, x0 + ux * s, y0 + uy * s)[0]
        ok = kd in ("road", "void", "green", "parking")
        if ok and cur is None:
            cur = [s, s, kd]
        elif ok:
            cur[1] = s
        elif cur is not None:
            walk.append(tuple(cur))
            cur = None
    if cur is not None:
        walk.append(tuple(cur))
    sc = dict(a=tuple(a), b=tuple(b), L=L, ux=ux, uy=uy, nx=nx, ny=ny, bands=bands, bld=bld, trees=trees,
              bridges=bridges, walk=walk)
    memo[mk] = sc
    return sc


def sa_people(sc, ground_at, seed):
    """Scale figures on the walkable ground of the cut: a few groups, never on slopes steeper than 1:4."""
    rnd = random.Random(seed)
    out = []
    for s0, s1, kd in sc["walk"]:
        if s1 - s0 < 3.0:
            continue
        s = s0 + rnd.uniform(1.0, min(14.0, s1 - s0))
        while s < s1 - 1.0:
            g0, g1 = ground_at(s - 1.0), ground_at(s + 1.0)
            if abs(g1 - g0) / 2.0 < 0.25:
                n = rnd.choice((1, 1, 2, 2, 3))
                x = s
                for q in range(n):
                    if x > s1 - 0.5:
                        break
                    child = rnd.random() < 0.1
                    out.append((x, rnd.randint(0, 3), (0.62 if child else rnd.uniform(0.95, 1.06)), rnd.random() < 0.5))
                    x += rnd.uniform(0.55, 1.1)
            s += rnd.uniform(26.0, 64.0)
    return out


# ============================================================ SECTION ART: the picture behind the cut
SA_STYLE_TECH = dict(bg=(255, 255, 255), ground=(232, 230, 226), ground_edge=(196, 192, 186), bld=(246, 246, 246),
                     bld_edge=(150, 150, 154), storey=(206, 206, 210), fade_to=(255, 255, 255), tree_alpha=0.78,
                     tree_wash=0.28, people=(118, 118, 124), bridge=(170, 170, 176), tint=None)


def sa_fade(d, dmax, lo=0.08, hi=0.8):
    return min(hi, lo + (hi - lo) * (max(0.0, d) / dmax) ** 0.8)


def sa_leaf(season):
    """Share of the season's days a deciduous crown is in leaf (leaf-out and leaf-fall measured over the site)."""
    if season in (None, "", "summer", "year", "lden", "board"):
        return 1.0 if season != "year" else float(np.mean(leaf_on_doy(np.arange(1, 366))))
    months = {"spring": (3, 4, 5), "autumn": (9, 10, 11), "winter": (12, 1, 2)}.get(season)
    if months is None:
        return 1.0
    md = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    doys = []
    for m in months:
        start = sum(md[:m - 1])
        doys += list(range(start + 1, start + md[m - 1] + 1))
    return float(np.mean(leaf_on_doy(np.array(doys))))


def sa_leaf_day(month, day):
    md = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    return 1.0 if bool(leaf_on_doy(np.array([sum(md[:month - 1]) + day]))[0]) else 0.0


# ============================================================ v16.4 · BUILDING TYPES IN SECTION
# Every building a section cuts or sees is drawn with the silhouette of its type, so its fabric type and its use read in
# the section as on the plan. v16.4 draws each type in its own material tone (v16.3 tinted every cut building by its use,
# so the old town and the planned low-rise houses, both mostly homes with pitched tile roofs, came out alike) and gives
# each type the features that tell it apart:
#   old town house (Ottoman type, as Bergama's Kale and Kurtulus quarters): a stone ground floor, a timber-framed upper
#     floor jutting out over it on brackets (cikma), close-set tall windows, a deep-eaved hipped roof of Turkish tile;
#   planned low-rise house (reinforced concrete frame): concrete floor bands, wide windows, a cantilevered balcony with a
#     rail, a low-pitched tile roof with short eaves, rendered walls;
#   apartment block: flat roof and parapet, balconies on every floor, window bands;
#   small irregular house / shack: low, a lean-to corrugated sheet roof, small windows;
#   civic and school hall: flat roof and cornice, tall window grid; industrial hall: sawtooth roof, high band windows;
#   mosque: a masonry hall with arched windows under a lead-grey dome on a drum; a minaret (shaft, balcony (serefe),
#     conical cap) where the survey's minaret symbol marks the mosque (at the symbol's place) or the name says cami;
#   monument: masonry in stone and brick bands, round-arched openings, a cornice; a ruin with a broken top;
#   under construction: a frame in scaffolding.
# Shops (commerce and mixed use) show a glazed shopfront and an awning on the ground floor; the use stays in the
# colour ribbon under each land-use section and in the tag of each cut building.
# WHAT IS MEASURED AND WHAT IS NOT: the footprint, the use, the fabric type, the floor count and the minaret symbol's
# place come from the survey and the data as before, and the eaves (the top of the walls) stay at floors x storey
# height. The roof forms, jetties, windows, balconies, shopfronts, domes and minaret heights are GENERIC drawings of the
# type (typical Turkish small-town building types, drawn to the proportions below), not surveyed: the legend of every
# section says so. The analyses keep using the measured prisms.
#@include ../data/TYPO.py
