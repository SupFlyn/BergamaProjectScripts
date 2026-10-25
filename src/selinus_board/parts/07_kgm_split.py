def kgm_split(P, tags):
    """A road of KGM_SPLIT cut at its section boundary: [(points, tags with "_kgm_section")]; other roads unchanged."""
    sp = KGM_SPLIT.get(tags.get("name") or "")
    if not sp or len(P) < 2:
        return [(P, tags)]
    a, b = to_dwg(*sp[0]), to_dwg(*sp[1])
    if not a or not b:
        return [(P, tags)]
    mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
    tx, ty = b[0] - a[0], b[1] - a[1]
    side = [(p[0] - mx) * tx + (p[1] - my) * ty >= 0.0 for p in P]
    out, run = [], [P[0]]
    for i in range(1, len(P)):
        if side[i] != side[i - 1]:
            p0, p1 = P[i - 1], P[i]
            d0 = (p0[0] - mx) * tx + (p0[1] - my) * ty
            d1 = (p1[0] - mx) * tx + (p1[1] - my) * ty
            f = d0 / (d0 - d1)
            q = (p0[0] + (p1[0] - p0[0]) * f, p0[1] + (p1[1] - p0[1]) * f)
            out.append((run + [q], side[i - 1]))
            run = [q]
        run.append(P[i])
    out.append((run, side[-1]))
    return [(r, dict(tags, _kgm_section=sp[3] if east else sp[2])) for r, east in out if len(r) >= 2]
# GPG v2 Tool 2.5 default flows by road category, as NoiseModelling 4.0.5 sets them (vehicles in the period, two-way):
#   category        0 motorway  1 trunk  2 primary  3 secondary  4 tertiary/unclassified  5 residential  6 service/living
GPG_D = (26103.0, 17936.0, 7124.0, 1400.0, 700.0, 350.0, 175.0)       # day, 12 h
GPG_E = (7458.0, 3826.0, 1069.0, 400.0, 200.0, 100.0, 50.0)            # evening, 4 h
GPG_N = (3729.0, 2152.0, 712.0, 200.0, 100.0, 50.0, 25.0)              # night, 8 h
GPG_HV = ((0.25, 0.35, 0.45), (0.2, 0.2, 0.2), (0.2, 0.15, 0.1), (0.15, 0.10, 0.05), (0.10, 0.06, 0.03),
          (0.05, 0.02, 0.01), (0.02, 0.01, 0.0))                        # heavy share day, evening, night
GPG_CAT = {"motorway": 0, "motorway_link": 0, "trunk": 1, "trunk_link": 1, "primary": 2, "primary_link": 2,
           "secondary": 3, "secondary_link": 3, "tertiary": 4, "tertiary_link": 4, "unclassified": 4,
           "residential": 5, "service": 6, "living_street": 6}
GPG_NAMES = ("motorway", "trunk road", "primary road", "secondary road", "tertiary / unclassified street",
             "residential street", "service road / living street")
GPG_SRC = ("WG-AEN Good Practice Guide v2 (2006), Toolkit 2 Tool 2.5 default flows, OSM types mapped as NoiseModelling "
           "4.0.5 (Import_OSM.groovy)")
URBAN_LIMIT = 50.0      # km/h: legal limit inside settlements (Karayollari Trafik Yonetmeligi art. 100) unless signed
# Hourly share of the daily traffic per period for a COUNTED road: VBUS Table 2, row 3 (provincial roads): day 0.062,
# evening 0.042, night 0.008 x AADT; KGM publishes no hourly counts. Heavy share: the counted daily share in every period.
PERIODS = (("day", 12.0, 0.062, 1.0, 0.0), ("evening", 4.0, 0.042, 1.0, 5.0), ("night", 8.0, 0.008, 1.0, 10.0))


def road_count(tags):
    """The official count of a road from its OSM ref (and name where KGM counts one ref in sections), or None."""
    for k_ in (tags.get("ref") or "").replace(" ", "").split(";"):
        lst = COUNTED.get(k_)
        if not lst:
            continue
        if len(lst) == 1:
            return lst[0]
        nm = tags.get("name") or ""
        sec = tags.get("_kgm_section")
        for c_ in lst:
            if c_.get("name") == nm and c_.get("section") in (None, sec):
                return c_
        return lst[0]
    return None


def is_oneway(tags):
    return (tags.get("oneway") or "").lower() in ("yes", "1", "true", "-1")


def traffic_plan(S):
    """Traffic of every street that carries any (v16.3), once per bake: per road of S.roads_noise its hourly flows
    (day, evening, night), heavy shares, how they were found ("counted", "correlated" or "default"), k and source."""
    tp = getattr(S, "_traffic", None)
    if tp is not None:
        return tp
    roads = getattr(S, "roads_noise", [])
    counted = []                                          # (category, k, p, src, points) of every counted road
    for r in roads:
        c_ = road_count(r["tags"])
        cat = GPG_CAT.get(r["tags"].get("highway"))
        if c_ is not None and cat is not None:
            k = c_["aadt"] / (GPG_D[cat] + GPG_E[cat] + GPG_N[cat])
            counted.append((cat, k, c_["p_kgm"], c_["src"], r["P"][::max(1, len(r["P"]) // 40)]))   # v22: p_kgm
    plan = []
    for r in roads:
        tags = r["tags"]
        cat = GPG_CAT.get(tags.get("highway"))
        if cat is None:
            plan.append(None)
            continue
        half = 0.5 if is_oneway(tags) else 1.0
        c_ = road_count(tags)
        if c_ is not None:
            M = tuple(c_["aadt"] * share * half for name, hrs, share, pf, pen in PERIODS)
            plan.append(dict(kind="counted", M=M, p=(c_["p"],) * 3, k=None, cat=cat, src=c_["src"]))
            continue
        mx, my = r["P"][len(r["P"]) // 2]
        best = None
        for (cc, k, p, src, pts) in counted:
            if cc != cat:
                continue
            d = min(math.hypot(px - mx, py - my) for px, py in pts)
            if best is None or d < best[0]:
                best = (d, k, p, src)
        if best is not None:
            k, p = best[1], (best[2],) * 3
            kind, src = "correlated", best[3] + "; heavy share kept at KGM's {:.0f} %".format(best[2])
        else:
            k, p = 1.0, tuple(100.0 * v for v in GPG_HV[cat])
            kind, src = "default", None
        M = (k * GPG_D[cat] / 12.0 * half, k * GPG_E[cat] / 4.0 * half, k * GPG_N[cat] / 8.0 * half)
        plan.append(dict(kind=kind, M=M, p=p, k=k, cat=cat, src=src))
    for r, t in zip(roads, plan):
        r["traffic"] = t
    S._traffic = plan
    return plan


def traffic_key(S):
    """Fingerprint of the traffic model (for the result store)."""
    return fp(sorted((k_, [sorted(c_.items()) for c_ in v_]) for k_, v_ in COUNTED.items()), GPG_D, GPG_E, GPG_N, GPG_HV,
              sorted(GPG_CAT.items()), URBAN_LIMIT, PERIODS, sorted(KGM_SPLIT.items()), "v16.3")


def rls90_emission(M, p, v):
    """RLS-90 emission level L_m,E (dB(A) at 25 m) of M vehicles/h with p % heavy, cars at v km/h (30-130) and
    heavy vehicles at v but at most 80 km/h (30-80)."""
    if M <= 0:
        return None
    v = float(v)
    vp = max(30.0, min(v, 130.0))
    vl = max(30.0, min(v, 80.0))
    Lpkw = 27.7 + 10.0 * math.log10(1.0 + (0.02 * vp) ** 3)
    D = 23.1 + 12.5 * math.log10(vl) - Lpkw
    Dv = Lpkw - 37.3 + 10.0 * math.log10((100.0 + (10.0 ** (0.1 * D) - 1.0) * p) / (100.0 + 8.23 * p))
    return 37.3 + 10.0 * math.log10(M * (1.0 + 0.082 * p)) + Dv


def surface_corr(tags, v):
    """RLS-90 Table 4 road surface correction D_StrO for the speed limit v: columns 30, 40 and >= 50 km/h."""
    s = (tags.get("surface") or "").lower()
    col = 0 if v < 35.0 else (1 if v < 45.0 else 2)
    if s in ("sett", "cobblestone", "unhewn_cobblestone", "cobblestone:flattened"):
        return (3.0, 4.5, 6.0)[col]                     # other paving
    if s in ("paving_stones", "paving_stones:30", "paving_stones:lanes"):
        return (2.0, 2.5, 3.0)[col]                     # paving with an even surface
    if s in ("concrete", "concrete:plates", "concrete:lanes"):
        return (1.0, 1.5, 2.0)[col]                     # concrete
    return 0.0


def noise_sources(S, R=300.0):
    """Centrelines of the counted roads within R of the frame (not cut at it: receivers near the edge hear the road
    beyond it) in pieces of at most 10 m, with RLS-90 emission per period. Road gradient for D_Stg: over 50 m
    along the road (at most 12 %). v18: the pieces are listed first, their terrain heights found together (on the
    worker processes), then the sources made from them, in the same order with the same arithmetic."""
    pieces = []
    fb = S.F.bb
    box = (fb[0] - R, fb[1] - R, fb[2] + R, fb[3] + R)
    plan = traffic_plan(S)
    for r, tr in zip(getattr(S, "roads_noise", []), plan):
        if tr is None:
            continue
        v = URBAN_LIMIT
        try:
            v = float(str(r["tags"].get("maxspeed")).split()[0])          # the signed limit, where mapped
        except Exception:
            pass
        sc = surface_corr(r["tags"], v)
        P = r["P"]
        for k in range(len(P) - 1):
            a, b = P[k], P[k + 1]
            L_ = math.hypot(b[0] - a[0], b[1] - a[1])
            if L_ < 0.5 or not bb_hit((min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])), box):
                continue
            ux_, uy_ = (b[0] - a[0]) / L_, (b[1] - a[1]) / L_
            n = max(1, int(math.ceil(L_ / 10.0)))
            for q in range(n):
                t0, t1 = q / float(n), (q + 1) / float(n)
                x0, y0 = a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0
                x1, y1 = a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1
                mx_, my_ = (x0 + x1) / 2.0, (y0 + y1) / 2.0
                pieces.append((tr, v, sc, x0, y0, x1, y1, L_ / n, (mx_ + ux_ * 25.0, my_ + uy_ * 25.0),
                               (mx_ - ux_ * 25.0, my_ - uy_ * 25.0), (mx_, my_)))
    zs = z_at_many(S, [p_[k_] for p_ in pieces for k_ in (8, 9, 10)], "road gradients")
    src = []
    for j, (tr, v, sc, x0, y0, x1, y1, Ln, pa, pb, pm) in enumerate(pieces):
        za, zb, zm = zs[3 * j], zs[3 * j + 1], zs[3 * j + 2]
        g_ = abs(za - zb) / 50.0 * 100.0
        g_ = min(g_, 12.0)
        dstg = 0.6 * g_ - 3.0 if g_ > 5.0 else 0.0
        em = []
        for q_ in range(3):
            e_ = rls90_emission(tr["M"][q_], tr["p"][q_], v)
            em.append(e_ + sc + dstg if e_ is not None else None)
        src.append(dict(a=(x0, y0), b=(x1, y1), L=Ln, em=em, z=zm))
    return src


NOISE_MEAS_H = 1.5        # m above ground: the height of a hand-held sound level meter


def calibrate_noise(S, nm, pts, dbs):
    """Shift the whole map so it agrees, on median, with LAeq (day) measured at your points: the model is
    evaluated at each point itself, 1.5 m above the ground (where a hand-held meter measures)."""
    if not pts or not dbs:
        return 0.0, 0
    NM = noise_model(S)
    diffs = []
    for (x, y), m in zip(pts, dbs):
        if NM.inside(x, y):
            LOG.append("WARNING: a noise point lies inside a building and was not used for the calibration.")
            continue
        r = NM.column(x, y, S.z_at(x, y), (NOISE_MEAS_H,))[0]
        if r is not None and r[0] is not None:
            diffs.append(float(m) - r[0])
    if not diffs:
        return 0.0, 0
    diffs.sort()
    n_ = len(diffs)
    off = diffs[n_ // 2] if n_ % 2 else 0.5 * (diffs[n_ // 2 - 1] + diffs[n_ // 2])
    off = max(-12.0, min(12.0, off))
    for row in nm["grid"]:
        for c in row:
            if c and c["lden"] is not None:
                for k in ("day", "evening", "night", "lden"):
                    c[k] += off
    return off, len(diffs)


# ------------------------------------------------------------ surface heat: Landsat grids on the survey
def lst_sample(L_, x, y):
    i = (x - L_["x0"]) / L_["dx"] - 0.5
    j = (y - L_["y0"]) / L_["dx"] - 0.5
    i0, j0 = int(math.floor(i)), int(math.floor(j))
    vals, wts = [], []
    for di in (0, 1):
        for dj in (0, 1):
            ii, jj = i0 + di, j0 + dj
            if 0 <= jj < L_["ny"] and 0 <= ii < L_["nx"]:
                v_ = L_["values"][jj][ii]
                if v_ is not None:
                    vals.append(v_)
                    wts.append((1 - abs(i - ii)) * (1 - abs(j - jj)))
    if not vals or sum(wts) <= 0:
        return None
    return sum(v_ * w_ for v_, w_ in zip(vals, wts)) / sum(wts)


NOISE_PTS_SURVEY = []
NOISE_PTS_USER = []
NOISE_DB_PAIRED = []                      # the measured dB of each noise point kept (same order)
FOCUS_PTS_USER = []

# ------------------------------------------------------------ tree canopies: measured transmissivity of direct sun
# Konarska et al. 2014 (Theor. Appl. Climatol. 117:363-376), one coniferous and four deciduous urban trees measured:
# crowns in leaf pass 1.3-5.3 % of the direct beam, leafless crowns 40.2-51.9 %. Every needle-leaved crown (all year)
# and deciduous crown in leaf passes 3 % (SOLWEIG's default, inside the measured range; no needle-leaved measurement of
# its own: unverified), a leafless deciduous crown 46 % (the middle of the measured range).
# v24 (R03-04): olive crowns (evergreen broadleaf) pass 15 % all year. Castillo-Ruiz et al. 2016, Sensors 16(5):723,
# doi:10.3390/s16050723, Table 3: olive crown porosity along the sun beam (PAR transmittance) 13.3-24.6 % (nine variety
# x date x pruning means, mean 18.5 %); Konarska et al. measured no olive.
TAU_LEAFY, TAU_BARE, TAU_OLIVE = 0.03, 0.46, 0.15


def canopy_tau(kind, leaf_on):
    if kind == "olive":
        return TAU_OLIVE
    return TAU_LEAFY if (kind in EVERGREEN or leaf_on) else TAU_BARE


# ============================================================ ENVIRONMENT v16 · period averages (numpy engine)
# Every map and section of the technical sheets is an average over a period:
#   shade      hours in shade over the whole day (sunrise to sunset, every minute) on the four key days, and the mean
#              day of the year (every minute of all 365 days)
#   radiation  mean kWh/m2 per day of each season, from every hour of the typical year
#   wind, air temperature, felt temperature   means over every hour of each season's window (default: daylight)
# The sun and sky are cast through the surveyed buildings (exact footprints, roof heights over the surveyed terrain),
# the 3D tree crowns and the terrain horizon. For each degree of sun azimuth the obstruction of every receiver is found
# exactly (the steepest roof edge between it and the sun, and the elevation bands where crowns stand in the way); the
# time integrals over the sun's positions in that degree are then exact in elevation. The sky is integrated
# analytically in elevation over 5-degree sectors.
try:
    import numpy as np
    HAVE_NP = True
except Exception:
    np = None
    HAVE_NP = False

SUN_BINS = 360                    # 1 degree of azimuth
SKY_BINS = 72                     # 5 degrees of azimuth for the sky
ENV_REACH = 250.0                 # m: obstacles further away are not searched (as v15)
KIND_CLASS = {"pine": 0, "olive": 1, "tree": 2}
_h_in = inp("hours", "daylight")
if isinstance(_h_in, (list, tuple)):
    _h_in = _h_in[0] if _h_in else "daylight"
HOURS_IN = str(_h_in if _h_in is not None else "daylight").strip().lower()
if inp("hour", None) is not None:
    LOG.append("The input hour is no longer used: every wind, air and felt temperature map is a mean over the season's "
               "hours (input hours: daylight, all, or a local range such as 10-17).")


def hours_window():
    """The comfort averaging window: ("daylight", None), ("all", None) or ("range", (h0, h1)) in local hours."""
    h = HOURS_IN.replace(" ", "")
    if h in ("", "daylight", "day", "sun", "daytime"):
        return ("daylight", None)
    if h in ("all", "24", "24h", "allday", "0-24"):
        return ("all", None)
    try:
        a, b = h.replace("–", "-").split("-")
        a, b = int(round(float(a))) % 24, int(round(float(b)))
        if b <= a:
            b += 24
        return ("range", (a, b))
    except Exception:
        LOG.append("hours input '{}' not understood: daylight hours used.".format(HOURS_IN))
        return ("daylight", None)


def window_label(short=False):
    kind, rng = hours_window()
    if kind == "daylight":
        return "daylight hours" if short else "every daylight hour (sun above the horizon)"
    if kind == "all":
        return "all hours" if short else "every hour of the day and night"
    return "{:02d}:00-{:02d}:00".format(rng[0], rng[1] % 24) if short else "every hour from {:02d}:00 to {:02d}:00 local".format(rng[0], rng[1] % 24)


def tau_mask_table(leaf_on):
    """Transmission for each set of crown classes standing in the way (bit 0 needle-leaved, 1 evergreen broadleaf,
    2 deciduous): the most opaque one counts, as on the v15 plan."""
    tc = (canopy_tau("pine", leaf_on), canopy_tau("olive", leaf_on), canopy_tau("tree", leaf_on))
    t = np.ones(8)
    for m in range(1, 8):
        t[m] = min(tc[q] for q in range(3) if m >> q & 1)
    return t


# ------------------------------------------------------------ sun, vectorised (the formulas of sun_position)
def sun_np(y, mo, d, hour_utc, lat, lon):
    mo = np.asarray(mo, np.int64)
    d = np.asarray(d, np.int64)
    h = np.asarray(hour_utc, float)
    yy = np.where(mo <= 2, y - 1, y)
    mm = np.where(mo <= 2, mo + 12, mo)
    A_ = yy // 100
    jd = (np.floor(365.25 * (yy + 4716)) + np.floor(30.6001 * (mm + 1)) + d + (2 - A_ + A_ // 4) - 1524.5
          + h / 24.0)
    T = (jd - 2451545.0) / 36525.0
    L0 = (280.46646 + T * (36000.76983 + 0.0003032 * T)) % 360.0
    M = np.radians(357.52911 + T * (35999.05029 - 0.0001537 * T))
    e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T)
    Cc = (np.sin(M) * (1.914602 - T * (0.004817 + 0.000014 * T)) + np.sin(2 * M) * (0.019993 - 0.000101 * T)
          + np.sin(3 * M) * 0.000289)
    om = np.radians(125.04 - 1934.136 * T)
    lam = np.radians(L0 + Cc - 0.00569 - 0.00478 * np.sin(om))
    eps = np.radians(23.0 + (26.0 + (21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60.0) / 60.0
                     + 0.00256 * np.cos(om))
    dec = np.arcsin(np.sin(eps) * np.sin(lam))
    yv = np.tan(eps / 2.0) ** 2
    L0r = np.radians(L0)
    eqt = 4.0 * np.degrees(yv * np.sin(2 * L0r) - 2 * e * np.sin(M) + 4 * e * yv * np.sin(M) * np.cos(2 * L0r)
                           - 0.5 * yv * yv * np.sin(4 * L0r) - 1.25 * e * e * np.sin(2 * M))
    ha = np.radians(((h * 60.0 + eqt + 4.0 * lon) % 1440.0) / 4.0 - 180.0)
    lr = math.radians(lat)
    cz = math.sin(lr) * np.sin(dec) + math.cos(lr) * np.cos(dec) * np.cos(ha)
    zen = np.arccos(np.clip(cz, -1.0, 1.0))
    el = 90.0 - np.degrees(zen)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        te = np.tan(np.radians(el))
        r = np.where(el > 85.0, 0.0,
                     np.where(el > 5.0, 58.1 / te - 0.07 / te ** 3 + 0.000086 / te ** 5,
                              np.where(el > -0.575, 1735.0 + el * (-518.2 + el * (103.4 + el * (-12.79 + el * 0.711))),
                                       -20.774 / te)))     # v21: NOAA (R04-02)
        sz = np.sin(zen)
        a = np.degrees(np.arccos(np.clip((math.sin(lr) * cz - np.sin(dec)) / (math.cos(lr) * sz), -1.0, 1.0)))
    az = np.where(ha > 0, (a + 180.0) % 360.0, (540.0 - a) % 360.0)
    az = np.where(sz < 1e-9, 180.0, az)
    return az, el + r / 3600.0


def perez_np(dhi, dni, zen_deg, doy):
    """perez_f vectorised: circumsolar F1 and horizon F2."""
    z = np.radians(zen_deg)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        am = 1.0 / (np.cos(z) + 0.50572 * (96.07995 - zen_deg) ** -1.6364)
        k = 1.041 * z ** 3
        eps = ((dhi + dni) / dhi + k) / (1.0 + k)
        b_ = 2.0 * np.pi * (doy - 1) / 365.0               # v21: Spencer, day 0 = 1 January (R04-16)
        ext = 1366.1 * (1.00011 + 0.034221 * np.cos(b_) + 0.00128 * np.sin(b_) + 0.000719 * np.cos(2 * b_)
                        + 0.000077 * np.sin(2 * b_))
        delta = dhi * am / ext
    b = np.zeros(np.shape(eps), np.int64)
    for t in PEREZ_EPS:
        b += (eps >= t)
    F1c, F2c = np.array(PEREZ_F1), np.array(PEREZ_F2)
    f1 = np.maximum(0.0, F1c[b, 0] + F1c[b, 1] * delta + F1c[b, 2] * z)
    f2 = F2c[b, 0] + F2c[b, 1] * delta + F2c[b, 2] * z
    ok = (dhi > 0.0) & (zen_deg < 90.0)
    return np.where(ok, f1, 0.0), np.where(ok, f2, 0.0)


# ------------------------------------------------------------ terrain heights, vectorised (the rule of S.z_at)
def _ring_offsets(r):
    """The cells z_at visits up to ring r, in its order."""
    offs = [(0, 0)]
    for rr in range(1, int(r) + 1):
        offs += [(-rr, j) for j in range(-rr, rr + 1)]
        for i in range(-rr + 1, rr):
            offs += [(i, -rr), (i, rr)]
        offs += [(rr, j) for j in range(-rr, rr + 1)]
    return offs


_RING_CACHE = {}


def _ring_np(r):
    o = _RING_CACHE.get(r)
    if o is None:
        offs = _ring_offsets(r)
        o = _RING_CACHE[r] = (np.array([q[0] for q in offs], np.int64), np.array([q[1] for q in offs], np.int64))
    return o


def z_np(S, X, Y, k=8):
    """S.z_at for many points at once: the same samples (the 8 nearest, rings of 25 m cells until no nearer one can
    lie outside), the same ranking (distance, ties in the order found) and the same weights. Points are taken
    bucket by bucket, each bucket's candidates once for all its points."""
    X = np.asarray(X, float).ravel()
    Y = np.asarray(Y, float).ravel()
    out = np.zeros(X.size)
    if not getattr(S, "terrain_ok", False) or X.size == 0:
        return out
    if X.size >= POOL_MIN_PTS and k == 8 and not getattr(S, "_no_pool", False) and pool_live():
        # v18: on the worker processes, in contiguous pieces (each point's height depends on that point alone)
        res = pool_map("_pool_z_np", [(X[a:b], Y[a:b]) for a, b in _pool_chunks(X.size, 5000)], pool_terrain(S),
                       "terrain heights")
        return np.concatenate(res)
    T = getattr(S, "_tnp", None)
    Cc = 25.0
    if T is None:
        smp = S.terrain_smp
        SX = np.array([p[0] for p in smp], float)
        SY = np.array([p[1] for p in smp], float)
        SZ = np.array([p[2] for p in smp], float)
        bi = np.floor(SX / Cc).astype(np.int64)
        bj = np.floor(SY / Cc).astype(np.int64)
        i_lo, j_lo = int(bi.min()) - 61, int(bj.min()) - 61
        W = int(bi.max()) - i_lo + 62
        H = int(bj.max()) - j_lo + 62
        key = (bj - j_lo) * W + (bi - i_lo)
        order = np.argsort(key, kind="stable")              # within a bucket: the order the samples were added
        cnt = np.bincount(key, minlength=W * H)
        start = np.concatenate([[0], np.cumsum(cnt)])
        T = S._tnp = dict(SX=SX[order], SY=SY[order], SZ=SZ[order], i_lo=i_lo, j_lo=j_lo, W=W, H=H, start=start)
    SX, SY, SZ, i_lo, j_lo, W, H, start = (T[q] for q in ("SX", "SY", "SZ", "i_lo", "j_lo", "W", "H", "start"))
    i0 = np.floor(X / Cc).astype(np.int64) - i_lo
    j0 = np.floor(Y / Cc).astype(np.int64) - j_lo
    qk = (j0 + 4096) * (W + 8192) + (i0 + 4096)
    order = np.argsort(qk, kind="stable")
    qs_ = qk[order]
    cut = np.flatnonzero(np.r_[True, qs_[1:] != qs_[:-1], True])
    for u in range(cut.size - 1):
        pend = order[cut[u]:cut[u + 1]]
        ci, cj = int(i0[pend[0]]), int(j0[pend[0]])
        r = 1
        while pend.size:
            oi, oj = _ring_np(r)
            ii, jj = ci + oi, cj + oj
            ok_c = (ii >= 0) & (ii < W) & (jj >= 0) & (jj < H)          # cells beyond the samples' area are empty
            cells = np.where(ok_c, jj * W + ii, 0)
            s0 = np.where(ok_c, start[cells], 0)
            n_ = np.where(ok_c, start[cells + 1] - start[cells], 0)
            tot = int(n_.sum())
            if tot >= k or r >= 60:
                cand = np.repeat(s0, n_) + (np.arange(tot) - np.repeat(np.cumsum(n_) - n_, n_))
                if tot == 0:
                    out[pend] = 0.0
                    break
                D = (SX[cand][None, :] - X[pend][:, None]) ** 2 + (SY[cand][None, :] - Y[pend][:, None]) ** 2
                kk = min(k, tot)
                o = np.argsort(D, axis=1, kind="stable")[:, :kk]
                Dk = np.take_along_axis(D, o, 1)
                ok = (Dk[:, kk - 1] <= (r * Cc) ** 2) if (tot >= k and r < 60) else np.ones(pend.size, bool)
                if ok.any():
                    Do, oo = Dk[ok], o[ok]
                    zc = SZ[cand][oo]
                    ws = np.zeros(Do.shape[0])
                    zs = np.zeros(Do.shape[0])
                    for j in range(kk):                       # summed in rank order, as z_at
                        w = 1.0 / np.where(Do[:, j] > 0.0, Do[:, j], 1.0)
                        ws += w
                        zs += w * zc[:, j]
                    out[pend[ok]] = np.where(Do[:, 0] < 0.01, zc[:, 0], zs / ws)
                pend = pend[~ok]
            r += 1
    return out


# ------------------------------------------------------------ frames, footprints, crowns
def f_world(F, u, v):
    c, s = F._wc, F._ws
    return F.cx + c * u - s * v, F.cy + s * u + c * v


def f_local(F, x, y):
    c, s = F._lc, F._ls
    dx, dy = x - F.cx, y - F.cy
    return c * dx - s * dy, s * dx + c * dy


class Casters16(object):
    """What stands between a receiver and the sun or sky, in one frame's local coordinates: every wall of every
    surveyed footprint (counter-clockwise, with the building's roof height above sea level), the tree crowns (circles
    of their measured radius between their lowest and highest leaves) and the terrain horizon profiles."""

    def __init__(self, S, E, solids, F, reach=ENV_REACH):
        bl, gB, trees = solids
        fb = F.bb
        fbx = (fb[0] - reach, fb[1] - reach, fb[2] + reach, fb[3] + reach)
        AX, AY, BX, BY, TOP, OWN, HB = [], [], [], [], [], [], []
        self.rings, self.tops, self.blds = [], [], []        # per building: outline (anticlockwise) + courtyards
        for bi, b in enumerate(bl):
            if not bb_hit(b["bb"], fbx):
                continue
            P = [F.local(x, y) for x, y in dict.fromkeys(b["P"])]
            if len(P) < 3:
                continue
            if signed_area(P) < 0:
                P = P[::-1]
            rings = [P]
            for h in b.get("holes") or ():
                Hl = [F.local(x, y) for x, y in dict.fromkeys(h)]
                if len(Hl) >= 3:
                    rings.append(Hl if signed_area(Hl) < 0 else Hl[::-1])      # courtyards clockwise
            self.rings.append(rings)
            self.tops.append(b["top"])
            self.blds.append(bi)
            for R_ in rings:                                 # outward normals point away from the solid for both
                n = len(R_)
                for q in range(n):
                    (ax, ay), (bx, by) = R_[q], R_[(q + 1) % n]
                    if ax == bx and ay == by:
                        continue
                    AX.append(ax); AY.append(ay); BX.append(bx); BY.append(by); TOP.append(b["top"]); OWN.append(bi)
                    HB.append(b["H"])
        self.AX, self.AY, self.BX, self.BY = (np.array(v, float) for v in (AX, AY, BX, BY))
        self.top = np.array(TOP, float)
        self.own = np.array(OWN, np.int64)
        self.HB = np.array(HB, float)                         # the building's height above its own ground
        ex, ey = self.BX - self.AX, self.BY - self.AY
        le = np.hypot(ex, ey)
        self.NX, self.NY = ey / le, -ex / le
        tr = [t for t in trees if fbx[0] <= t["x"] <= fbx[2] and fbx[1] <= t["y"] <= fbx[3]]
        loc = [F.local(t["x"], t["y"]) for t in tr]
        self.CU = np.array([p[0] for p in loc], float)
        self.CV = np.array([p[1] for p in loc], float)
        self.CR = np.array([t["r"] for t in tr], float)
        self.CLO = np.array([t["base"] + t["lo"] for t in tr], float)
        self.CHI = np.array([t["base"] + t["hi"] for t in tr], float)
        self.CK = np.array([KIND_CLASS.get(t["kind"], 2) for t in tr], np.int64)
        self.CHR = np.array([t["hi"] for t in tr], float)     # crown tops above their own ground
        HG = E.get("horizon_grid")
        HZ = Horizons(E.get("horizons", []))
        self.HG = HG
        if HG:                                                 # profiles on a grid: interpolated between its nodes
            self.HN = np.array(HG["h"], float).reshape(HG["nu"] * HG["nv"], -1)
            self.step = float(HG["step"])
        else:                                                  # a few profiles: the nearest one
            self.HN = np.array(HZ.H, float) if HZ.H else np.zeros((0, 48))
            self.step = HZ.step
        self.HPX = np.array([p[0] for p in HZ.P], float)
        self.HPY = np.array([p[1] for p in HZ.P], float)
        lat, lon = E["location"]["lat"], E["location"]["lon"]
        self.CP = Compass(lon, lat)
        o = F.local(0.0, 0.0)
        ex_, ey_ = F.local(1.0, 0.0), F.local(0.0, 1.0)
        self.M = (ex_[0] - o[0], ey_[0] - o[0], ex_[1] - o[1], ey_[1] - o[1])
        self.F = F
        self.reach = reach

    def dir_local(self, az):
        """Unit vector toward azimuth az, in the frame's coordinates."""
        sv = self.CP.vec(az)
        m = self.M
        dx, dy = m[0] * sv[0] + m[1] * sv[1], m[2] * sv[0] + m[3] * sv[1]
        dl = math.hypot(dx, dy)
        return dx / dl, dy / dl

    def hz_nodes(self, az):
        """Terrain horizon (deg) of every profile or grid node at azimuth az, linear between its 7.5-degree steps."""
        if self.HN.shape[0] == 0:
            return np.zeros(0)
        nh = self.HN.shape[1]
        f = (az % 360.0) / self.step
        k = int(f) % nh
        t = f - int(f)
        return self.HN[:, k] * (1 - t) + self.HN[:, (k + 1) % nh] * t

    def tau_min(self, az):
        """tan of the lowest terrain horizon anywhere at azimuth az (a bound below every receiver's)."""
        a = self.hz_nodes(az)
        return math.tan(math.radians(float(a.min()))) if a.size else 0.0

    def tau_at(self, az, hw):
        """tan of the terrain horizon at azimuth az of points with horizon weights hw (hz_weights)."""
        a = self.hz_nodes(az)
        idx, w = hw
        if a.size == 0:
            return np.zeros(idx.shape[0])
        return np.tan(np.radians((a[idx] * w).sum(1)))

    def hz_weights(self, X, Y):
        """How each point takes its horizon: bilinear between the four grid nodes around it (points beyond the grid
        take its edge), or the nearest of the profiles. (node indices, weights), each (n, k)."""
        X = np.asarray(X, float).ravel()
        Y = np.asarray(Y, float).ravel()
        HG = self.HG
        if HG:
            c, s = math.cos(HG["ang"]), math.sin(HG["ang"])
            dx, dy = X - HG["cx"], Y - HG["cy"]
            fi = np.clip((c * dx + s * dy - HG["u0"]) / HG["du"], 0.0, HG["nu"] - 1.0)
            fj = np.clip((-s * dx + c * dy - HG["v0"]) / HG["du"], 0.0, HG["nv"] - 1.0)
            i0 = np.minimum(fi.astype(np.int64), HG["nu"] - 2)
            j0 = np.minimum(fj.astype(np.int64), HG["nv"] - 2)
            ti, tj = fi - i0, fj - j0
            n0 = j0 * HG["nu"] + i0
            idx = np.stack([n0, n0 + 1, n0 + HG["nu"], n0 + HG["nu"] + 1], 1)
            w = np.stack([(1 - ti) * (1 - tj), ti * (1 - tj), (1 - ti) * tj, ti * tj], 1)
            return idx, w
        if self.HPX.size == 0:
            return np.zeros((X.size, 1), np.int64), np.zeros((X.size, 1))
        d2 = (X[:, None] - self.HPX[None, :]) ** 2 + (Y[:, None] - self.HPY[None, :]) ** 2
        return np.argmin(d2, axis=1)[:, None], np.ones((X.size, 1))


# ------------------------------------------------------------ v16.3: the terrain horizon above the ground
# PVGIS gives the terrain horizon of a point ON THE GROUND. v16.2 used that ground horizon unchanged at every height of a
# section, so a point 20 m up kept the horizon of the ground under it: the whole sky of a section took the ground's
# horizon hours, in full-height bands whose edges fall where those hours cross a whole hour (the colour classes).
# v16.3 lowers the horizon with height by what the terrain itself shows: for each point and each of the PVGIS azimuths
# the terrain is marched from HZ_D0 out to the edge of the horizon grid (the survey's own terrain inside the frame, the
# PVGIS DEM heights of the 100 m grid nodes around it), and the terrain beyond the grid is the PVGIS horizon of the
# grid's edge point in that direction, taken as far away (so it does not fall with height). The point's horizon at
# height h is then its PVGIS ground horizon minus how much that terrain model's horizon falls between the ground and h.
# At the ground nothing changes (the plan, T3, and the section's ground row stay as they were).
HZ_D0 = 50.0                    # m: the march starts at half the PVGIS grid spacing (nearer ground: the slope's own plane)
HZ_GROW = 1.04                  # each march step 4 % longer than the last (50 m, 52 m, 54 m ... to the grid's edge)
HZ_HTS = (0.0, 1.0, 2.5, 5.0, 10.0, 20.0, 40.0, 80.0, 160.0)    # m above the ground where the fall is computed
HZ_CELL = 10.0                  # m: the terrain raster the march reads (bilinear)


def hz_terrain(S, HG):
    """Terrain heights on a HZ_CELL raster over the horizon grid, in the grid's own axes: the survey's terrain inside
    the frame (+40 m, as the section drawings use it), the grid nodes' PVGIS DEM heights (bilinear) elsewhere."""
    memo = env_memo(S)
    r = memo.get("hz_terrain")
    if r is not None:
        return r
    nu, nv, du = HG["nu"], HG["nv"], float(HG["du"])
    u0, v0 = float(HG["u0"]), float(HG["v0"])
    Lu, Lv = (nu - 1) * du, (nv - 1) * du
    ni, nj = int(math.ceil(Lu / HZ_CELL)) + 1, int(math.ceil(Lv / HZ_CELL)) + 1
    uu = u0 + np.arange(ni) * HZ_CELL
    vv = v0 + np.arange(nj) * HZ_CELL
    UU, VV = np.meshgrid(uu, vv)
    el = np.array(HG["elev"], float)                          # [j][i], like the profiles
    fi = np.clip((UU - u0) / du, 0.0, nu - 1.0)
    fj = np.clip((VV - v0) / du, 0.0, nv - 1.0)
    i0 = np.minimum(fi.astype(np.int64), nu - 2)
    j0 = np.minimum(fj.astype(np.int64), nv - 2)
    ti, tj = fi - i0, fj - j0
    Z = ((el[j0, i0] * (1 - ti) + el[j0, i0 + 1] * ti) * (1 - tj) + (el[j0 + 1, i0] * (1 - ti) + el[j0 + 1, i0 + 1] * ti) * tj)
    c, s = math.cos(HG["ang"]), math.sin(HG["ang"])
    X = HG["cx"] + c * UU - s * VV
    Y = HG["cy"] + s * UU + c * VV
    F = S.F
    lu, lv = f_local(F, X.ravel(), Y.ravel())
    ins = (lu >= F.u0 - 40.0) & (lu <= F.u1 + 40.0) & (lv >= F.v0 - 40.0) & (lv <= F.v1 + 40.0)
    Zr = Z.ravel()
    if getattr(S, "terrain_ok", False) and ins.any():
        Zr[ins] = z_np(S, X.ravel()[ins], Y.ravel()[ins])
    r = memo["hz_terrain"] = dict(Z=Zr.reshape(Z.shape), u0=u0, v0=v0, ni=ni, nj=nj, Lu=Lu, Lv=Lv, c=c, s=s,
                                  n_survey=int(ins.sum()), n_all=int(ins.size))
    return r


def _hz_z(T, U, V):
    fi = np.clip((U - T["u0"]) / HZ_CELL, 0.0, T["ni"] - 1.0)
    fj = np.clip((V - T["v0"]) / HZ_CELL, 0.0, T["nj"] - 1.0)
    i0 = np.minimum(fi.astype(np.int64), T["ni"] - 2)
    j0 = np.minimum(fj.astype(np.int64), T["nj"] - 2)
    ti, tj = fi - i0, fj - j0
    Z = T["Z"]
    return (Z[j0, i0] * (1 - ti) + Z[j0, i0 + 1] * ti) * (1 - tj) + (Z[j0 + 1, i0] * (1 - ti) + Z[j0 + 1, i0 + 1] * ti) * tj


def hz_fall_table(S, C, X, Y, Zg):
    """How far (in tan) the terrain horizon of each point falls between its ground (Zg) and each height of HZ_HTS, at
    each PVGIS azimuth: array (points, azimuths, heights), 0 at the ground. None without a horizon grid."""
    HG = C.HG
    if not HG or C.HN.shape[0] == 0:
        return None
    T = hz_terrain(S, HG)
    X = np.asarray(X, float)
    Y = np.asarray(Y, float)
    Zg = np.asarray(Zg, float)
    c, s = T["c"], T["s"]
    U = c * (X - HG["cx"]) + s * (Y - HG["cy"])
    V = -s * (X - HG["cx"]) + c * (Y - HG["cy"])
    nh = C.HN.shape[1]
    step = C.step
    dmax = math.hypot(T["Lu"], T["Lv"]) + 10.0
    d = [HZ_D0]
    while d[-1] < dmax:
        d.append(d[-1] * HZ_GROW)
    d = np.array(d)
    hts = np.array(HZ_HTS)
    out = np.zeros((X.size, nh, hts.size))
    u_lo, u_hi, v_lo, v_hi = T["u0"], T["u0"] + T["Lu"], T["v0"], T["v0"] + T["Lv"]
    for k in range(nh):
        az = k * step
        wx, wy = C.CP.vec(az)                                    # survey axes
        du_, dv_ = c * wx + s * wy, -s * wx + c * wy               # the grid's axes
        for a in range(0, X.size, 256):
            b = min(X.size, a + 256)
            Us = U[a:b, None] + du_ * d[None, :]
            Vs = V[a:b, None] + dv_ * d[None, :]
            ins = (Us >= u_lo) & (Us <= u_hi) & (Vs >= v_lo) & (Vs <= v_hi)
            zt = _hz_z(T, Us, Vs)
            # the edge point: the last march step still on the grid (the point itself when the first step leaves it)
            last = np.where(ins.any(1), ins.shape[1] - 1 - np.argmax(ins[:, ::-1], axis=1), -1)
            dl = np.where(last >= 0, d[np.maximum(last, 0)], 0.0)
            Ue, Ve = U[a:b] + du_ * dl, V[a:b] + dv_ * dl
            Xe = HG["cx"] + c * Ue - s * Ve
            Ye = HG["cy"] + s * Ue + c * Ve
            hw = C.hz_weights(Xe, Ye)
            tanE = np.tan(np.radians((C.HN[hw[0], k] * hw[1]).sum(1)))
            prev = None
            for q, h in enumerate(hts):
                tn = np.where(ins, (zt - (Zg[a:b, None] + h)) / d[None, :], -np.inf).max(1)
                tm = np.maximum(tn, tanE)
                if prev is None:
                    prev = tm
                out[a:b, k, q] = np.maximum(0.0, prev - tm)
    return out


class HzFall(object):
    """The horizon's fall with height for receivers of one Points16: per receiver its point's row of the table and its
    height above the ground, read linearly between the azimuths and the heights of the table."""

    def __init__(self, table, step, pid, hg):
        self.T = table
        self.step = step
        self.pid = np.asarray(pid, np.int64)
        hts = np.array(HZ_HTS)
        hg = np.clip(np.asarray(hg, float), 0.0, hts[-1])
        q = np.clip(np.searchsorted(hts, hg, side="right") - 1, 0, hts.size - 2)
        self.q = q
        self.wq = (hg - hts[q]) / (hts[q + 1] - hts[q])
        self._az = None

    def _slice(self, az):
        last = self._az                                   # v16.6: read once (the sun pass runs on several threads)
        if last is not None and last[0] == az:
            return last[1]
        nh = self.T.shape[1]
        f = (az % 360.0) / self.step
        k = int(f) % nh
        t = f - int(f)
        A = self.T[:, k, :] * (1 - t) + self.T[:, (k + 1) % nh, :] * t
        self._az = (az, A)
        return A

    def at(self, az):
        A = self._slice(az)
        r = A[self.pid]
        q = self.q
        idx = np.arange(q.size)
        return r[idx, q] * (1.0 - self.wq) + r[idx, q + 1] * self.wq

    def most(self, az):
        A = self._slice(az)
        return float(A.max()) if A.size else 0.0


def tau_floor(G, C, az):
    """The lowest terrain horizon any receiver of G can have at azimuth az (a bound for the sweeps): the frame's lowest
    ground horizon, lowered by the largest fall with height among G's receivers (v16.3)."""
    hz = getattr(G, "hzf", None)
    return C.tau_min(az) - (hz.most(az) if hz is not None else 0.0)


def footprint_values(groups, vals, u0, v0, cell, nx, ny):
    """Per cell whose centre lies inside a footprint (groups of rings: outline and courtyards, even-odd per group)
    the largest value of the groups covering it; -inf elsewhere."""
    EA, EB, PID = [], [], []
    for k, rings in enumerate(groups):
        for P in rings:
            n = len(P)
            for q in range(n):
                EA.append(P[q]); EB.append(P[(q + 1) % n]); PID.append(k)
    out = np.full(nx * ny, -np.inf)
    if not EA:
        return out
    ax = np.array([p[0] for p in EA]); ay = np.array([p[1] for p in EA])
    bx = np.array([p[0] for p in EB]); by = np.array([p[1] for p in EB])
    pid = np.array(PID, np.int64)
    ylo, yhi = np.minimum(ay, by), np.maximum(ay, by)
    j0 = np.clip(np.ceil((ylo - v0) / cell - 0.5).astype(np.int64), 0, ny)        # rows with ylo <= yc < yhi
    j1 = np.clip(np.ceil((yhi - v0) / cell - 0.5).astype(np.int64), 0, ny)
    cnt = np.maximum(j1 - j0, 0)
    tot = int(cnt.sum())
    if tot == 0:
        return out
    e = np.repeat(np.arange(ax.size), cnt)
    row = j0[e] + (np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt))
    yc = v0 + (row + 0.5) * cell
    keep = (ay[e] <= yc) != (by[e] <= yc)
    e, row, yc = e[keep], row[keep], yc[keep]
    xc = ax[e] + (yc - ay[e]) * (bx[e] - ax[e]) / (by[e] - ay[e])
    o = np.lexsort((xc, row, pid[e]))
    e, row, xc = e[o], row[o], xc[o]
    key = pid[e] * (ny + 1) + row
    first = np.flatnonzero(np.r_[True, key[1:] != key[:-1]])
    pos = np.arange(key.size) - np.repeat(first, np.diff(np.r_[first, key.size]))
    a_i = np.flatnonzero(pos % 2 == 0)
    a_i = a_i[(a_i + 1 < key.size)]
    a_i = a_i[key[a_i + 1] == key[a_i]]
    lo, hi, rr, gg = xc[a_i], xc[a_i + 1], row[a_i], pid[e[a_i]]
    a0 = np.clip(np.ceil((lo - u0) / cell - 0.5).astype(np.int64), 0, nx)
    a1 = np.clip(np.floor((hi - u0) / cell - 0.5).astype(np.int64) + 1, 0, nx)
    ok = a1 > a0
    a0, a1, rr, gg = a0[ok], a1[ok], rr[ok], gg[ok]
    c = a1 - a0
    t2 = int(c.sum())
    rep = np.repeat(np.arange(c.size), c)
    idx = (rr * nx + a0)[rep] + (np.arange(t2) - np.repeat(np.cumsum(c) - c, c))
    np.maximum.at(out, idx, np.asarray(vals, float)[gg][rep])
    return out


def disc_values(cu, cv, r, vals, u0, v0, cell, nx, ny):
    """Per cell whose centre lies within a disc (crown) the largest value of the discs covering it; -inf elsewhere."""
    out = np.full(nx * ny, -np.inf)
    if np.size(cu) == 0:
        return out
    cu, cv, r, vals = (np.asarray(x, float) for x in (cu, cv, r, vals))
    j0 = np.clip(np.ceil((cv - r - v0) / cell - 0.5).astype(np.int64), 0, ny)
    j1 = np.clip(np.floor((cv + r - v0) / cell - 0.5).astype(np.int64) + 1, 0, ny)
    cnt = np.maximum(j1 - j0, 0)
    tot = int(cnt.sum())
    if tot == 0:
        return out
    q = np.repeat(np.arange(cu.size), cnt)
    row = j0[q] + (np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt))
    dv = v0 + (row + 0.5) * cell - cv[q]
    hw = np.sqrt(np.maximum(r[q] ** 2 - dv ** 2, 0.0))
    inn = r[q] ** 2 - dv ** 2 > 0.0
    a0 = np.clip(np.ceil((cu[q] - hw - u0) / cell - 0.5).astype(np.int64), 0, nx)
    a1 = np.clip(np.floor((cu[q] + hw - u0) / cell - 0.5).astype(np.int64) + 1, 0, nx)
    ok = inn & (a1 > a0)
    q, row, a0, a1 = q[ok], row[ok], a0[ok], a1[ok]
    c = a1 - a0
    t2 = int(c.sum())
    rep = np.repeat(np.arange(c.size), c)
    idx = (row * nx + a0)[rep] + (np.arange(t2) - np.repeat(np.cumsum(c) - c, c))
    ux = u0 + (idx % nx + 0.5) * cell
    keep = (ux - cu[q][rep]) ** 2 + (v0 + (idx // nx + 0.5) * cell - cv[q][rep]) ** 2 < r[q][rep] ** 2
    np.maximum.at(out, idx[keep], vals[q][rep][keep])
    return out


# ------------------------------------------------------------ the obstruction kernel
class Coarse16(object):
    """Lowest receiver height per 30 m block (blocks without receivers: no height), each block also covering its 8
    neighbours: a lower bound of the height of every receiver near a point, used to stop sweeps early."""

    def __init__(self, zr_eff, u0, v0, cell, nx, ny, C=30.0):
        self.C, self.u0, self.v0 = C, u0, v0
        bx = int(math.ceil(nx * cell / C))
        by = int(math.ceil(ny * cell / C))
        idx = np.arange(nx * ny)
        ii = ((idx % nx) * cell // C).astype(np.int64)
        jj = ((idx // nx) * cell // C).astype(np.int64)
        Z = np.full(bx * by, np.inf)
        ok = np.isfinite(zr_eff)
        np.minimum.at(Z, (jj * bx + ii)[ok], zr_eff[ok])
        Z = Z.reshape(by, bx)
        Pd = np.pad(Z, 1, constant_values=np.inf)
        D = np.full_like(Z, np.inf)
        for dj in (0, 1, 2):
            for di in (0, 1, 2):
                D = np.minimum(D, Pd[dj:dj + by, di:di + bx])
        self.D = np.pad(D, 1, constant_values=np.inf)
        self.bx, self.by = bx, by

    def zlow(self, u, v):
        i = np.clip(np.floor((u - self.u0) / self.C).astype(np.int64) + 1, 0, self.bx + 1)
        j = np.clip(np.floor((v - self.v0) / self.C).astype(np.int64) + 1, 0, self.by + 1)
        return self.D[j, i]


def k_sweep_len(Co, AU, AV, BU, BV, top, d, tau_min, reach, slack=None):
    """Longest useful sweep away from the sun for segments A-B whose top is `top`: no receiver further than this along
    the sweep can see the segment above tan(elevation) = tau_min (exact bound from the coarse lowest heights)."""
    dx, dy = d
    C = Co.C
    n = AU.size
    if n == 0:
        return np.zeros(0)
    sl = np.zeros(n) if slack is None else slack
    ns = int(math.ceil((reach + float(sl.max())) / (0.5 * C))) + 2
    wid = np.hypot(BU - AU, BV - AV)
    nl = np.maximum(2, np.ceil(wid / C).astype(np.int64) + 1)
    obj = np.repeat(np.arange(n), nl)
    kk = np.arange(obj.size) - np.repeat(np.cumsum(nl) - nl, nl)
    s = kk / (nl[obj] - 1).astype(float)
    pu = AU[obj] + s * (BU - AU)[obj]
    pv = AV[obj] + s * (BV - AV)[obj]
    t = np.arange(ns) * (0.5 * C)
    z = Co.zlow(pu[:, None] - t[None, :] * dx, pv[:, None] - t[None, :] * dy)
    t_lo = np.maximum(np.maximum(t - 0.5 * C, 0.0)[None, :] - sl[obj][:, None], 0.0)
    useful = (top[obj][:, None] - z) >= tau_min * t_lo
    tt = np.where(useful, np.minimum(reach + sl[obj][:, None], t[None, :] + 0.5 * C), 0.0)
    out = np.zeros(n)
    np.maximum.at(out, obj, tt.max(1))
    return out


def k_strip_rows(v_lo, v_hi, b_lo, b_hi, p0, pu, pv, t_lo, t_hi, d, u0, v0, cell, nx, ny, eps=1e-7):
    """Rows and column intervals of the cells whose centres satisfy b_lo <= -u dy + v dx <= b_hi and
    t_lo <= p0 + pu u + pv v <= t_hi (one parallelogram per object). Returns (object, row, a0, a1)."""
    dx, dy = d
    j0 = np.clip(np.ceil((v_lo - eps - v0) / cell - 0.5).astype(np.int64), 0, ny)
    j1 = np.clip(np.floor((v_hi + eps - v0) / cell - 0.5).astype(np.int64) + 1, 0, ny)
    cnt = np.maximum(j1 - j0, 0)
    tot = int(cnt.sum())
    if tot == 0:
        e = np.zeros(0, np.int64)
        return e, e, e, e
    q = np.repeat(np.arange(cnt.size), cnt)
    row = j0[q] + (np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt))
    v = v0 + (row + 0.5) * cell
    lo = np.full(tot, -np.inf)
    hi = np.full(tot, np.inf)
    if abs(dy) > 1e-12:
        x1 = (v * dx - b_hi[q]) / dy
        x2 = (v * dx - b_lo[q]) / dy
        lo = np.maximum(lo, np.minimum(x1, x2))
        hi = np.minimum(hi, np.maximum(x1, x2))
    else:
        bv = v * dx
        hi = np.where((bv < b_lo[q] - eps) | (bv > b_hi[q] + eps), -np.inf, hi)
    c = p0[q] + pv[q] * v
    s = pu[q]
    nzs = np.abs(s) > 1e-12
    ss = np.where(nzs, s, 1.0)
    y1 = (t_lo[q] - c) / ss
    y2 = (t_hi[q] - c) / ss
    lo = np.where(nzs, np.maximum(lo, np.minimum(y1, y2)), lo)
    hi = np.where(nzs, np.minimum(hi, np.maximum(y1, y2)), hi)
    hi = np.where(~nzs & ((c < t_lo[q] - eps) | (c > t_hi[q] + eps)), -np.inf, hi)
    a0 = np.clip(np.ceil((lo - eps - u0) / cell - 0.5).astype(np.int64), 0, nx)
    a1 = np.clip(np.floor((hi + eps - u0) / cell - 0.5).astype(np.int64) + 1, 0, nx)
    m = a1 > a0
    return q[m], row[m], a0[m], a1[m]


def k_expand(q, r, a0, a1, nx):
    cnt = a1 - a0
    tot = int(cnt.sum())
    rep = np.repeat(np.arange(q.size), cnt)
    a = np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt) + a0[rep]
    return rep, a


def k_buildings(C, G, d, tau_min, crit):
    """crit = max(crit, (roof - receiver height) / distance to the first wall met toward the sun) on a grid."""
    dx, dy = d
    face = (C.NX * dx + C.NY * dy) < 0.0                     # walls facing away from the sun: where a ray enters
    AU, AV, BU, BV, top = C.AX[face], C.AY[face], C.BX[face], C.BY[face], C.top[face]
    aA, bA = AU * dx + AV * dy, -AU * dy + AV * dx
    aB, bB = BU * dx + BV * dy, -BU * dy + BV * dx
    ok = bA != bB
    AU, AV, BU, BV, top, aA, bA, aB, bB = (x[ok] for x in (AU, AV, BU, BV, top, aA, bA, aB, bB))
    T = k_sweep_len(G.Co, AU, AV, BU, BV, top, d, tau_min, C.reach)
    ok = T > 0
    AU, AV, BU, BV, top, aA, bA, aB, bB, T = (x[ok] for x in (AU, AV, BU, BV, top, aA, bA, aB, bB, T))
    if T.size == 0:
        return 0
    ke = (aB - aA) / (bB - bA)
    p0 = aA - bA * ke                                        # distance to the wall: t = p0 + pu u + pv v
    pu = -dy * ke - dx
    pv = dx * ke - dy
    vs = np.stack([AV, BV, AV - T * dy, BV - T * dy], 1)
    q, r, a0, a1 = k_strip_rows(vs.min(1), vs.max(1), np.minimum(bA, bB), np.maximum(bA, bB), p0, pu, pv,
                                np.zeros(T.size), T, d, G.u0, G.v0, G.cell, G.nx, G.ny)
    if q.size == 0:
        return 0
    t_row = p0[q] + pv[q] * (G.v0 + (r + 0.5) * G.cell) + pu[q] * (G.u0 + 0.5 * G.cell)
    rep, a = k_expand(q, r, a0, a1, G.nx)
    t = t_row[rep] + (pu[q] * G.cell)[rep] * a
    c = r[rep] * G.nx + a
    with np.errstate(divide="ignore", invalid="ignore"):
        val = np.where(t > 0.0, (top[q][rep] - G.zr_eff[c]) / t, np.inf)
    np.maximum.at(crit, c, val)
    return c.size


def k_crowns(C, G, d, tau_min):
    """Elevation bands (in tan) where a crown stands between each receiver and the sun: (receiver, lo, hi, class)."""
    dx, dy = d
    n = C.CU.size
    e = np.zeros(0)
    ei = np.zeros(0, np.int64)
    if n == 0:
        return ei, e, e, ei, 0
    px, py = -dy, dx
    r = C.CR
    AU, AV = C.CU - r * px + r * dx, C.CV - r * py + r * dy     # the crown's side toward the sun
    BU, BV = C.CU + r * px + r * dx, C.CV + r * py + r * dy
    T = k_sweep_len(G.Co, AU, AV, BU, BV, C.CHI, d, tau_min, C.reach, slack=2.0 * r)
    ok = T > 0
    cu, cv, r, zlo, zhi, cls, T = C.CU[ok], C.CV[ok], r[ok], C.CLO[ok], C.CHI[ok], C.CK[ok], T[ok]
    if T.size == 0:
        return ei, e, e, ei, 0
    ac, bc = cu * dx + cv * dy, -cu * dy + cv * dx
    # receivers with |b - bc| < r and ac + r - T <= a <= ac + r  (a = u dx + v dy)
    p0 = -(ac + r) + T * 0.0
    q, rr, a0, a1 = k_strip_rows(np.minimum(cv - r - T * np.maximum(dy, 0) - r, cv - r) - 2 * r,
                                 np.maximum(cv + r - T * np.minimum(dy, 0) + r, cv + r) + 2 * r,
                                 bc - r, bc + r, -(ac + r), np.full(T.size, dx), np.full(T.size, dy),
                                 -T, np.zeros(T.size), d, G.u0, G.v0, G.cell, G.nx, G.ny)
    if q.size == 0:
        return ei, e, e, ei, 0
    rep, a = k_expand(q, rr, a0, a1, G.nx)
    k = q[rep]
    row = rr[rep]
    c = row * G.nx + a
    uu = G.u0 + (a + 0.5) * G.cell
    vv = G.v0 + (row + 0.5) * G.cell
    perp = (-uu * dy + vv * dx) - bc[k]
    m = (np.abs(perp) < r[k]) & np.isfinite(G.zr_eff[c])
    k, c, perp, uu, vv = k[m], c[m], perp[m], uu[m], vv[m]
    hw = np.sqrt(r[k] * r[k] - perp * perp)
    along = ac[k] - (uu * dx + vv * dy)
    ta, tb = along - hw, along + hw
    m = (tb > 0.0) & (ta <= np.minimum(T[k], C.reach))
    k, c, ta, tb = k[m], c[m], ta[m], tb[m]
    ta = np.maximum(ta, 0.0)
    z = G.zr_eff[c]
    with np.errstate(divide="ignore", invalid="ignore"):
        lo = np.maximum((zlo[k] - z) / tb, 0.0)
        hi = np.where(ta > 0.0, (zhi[k] - z) / np.where(ta > 0.0, ta, 1.0), np.where(zhi[k] > z, np.inf, -1.0))
    m = (hi > lo) & (hi >= tau_min)
    return c[m], lo[m], hi[m], cls[k[m]], k.size


def k_segments(c, lo, hi, cls, crit, ncls=3):
    """The crown bands above crit merged per receiver: elementary segments (receiver, lo, hi, class bit mask)."""
    lo = np.maximum(lo, crit[c])
    m = hi > lo
    c, lo, hi, cls = c[m], lo[m], hi[m], cls[m]
    e = np.zeros(0)
    if c.size == 0:
        return np.zeros(0, np.int64), e, e, np.zeros(0, np.int64)
    n_per = np.bincount(c)
    single = n_per[c] == 1
    oc, olo, ohi, om = [c[single]], [lo[single]], [hi[single]], [(np.int64(1) << cls[single]).astype(np.int64)]
    mul = ~single
    if mul.any():
        c2, lo2, hi2, k2 = c[mul], lo[mul], hi[mul], cls[mul]
        n = c2.size
        ev_c = np.concatenate([c2, c2])
        ev_t = np.concatenate([lo2, hi2])
        ev_d = np.concatenate([np.ones(n, np.int64), -np.ones(n, np.int64)])
        ev_k = np.concatenate([k2, k2])
        o = np.lexsort((ev_t, ev_c))
        ev_c, ev_t, ev_d, ev_k = ev_c[o], ev_t[o], ev_d[o], ev_k[o]
        mask = np.zeros(ev_c.size, np.int64)
        for q in range(ncls):
            mask |= (np.cumsum(np.where(ev_k == q, ev_d, 0)) > 0).astype(np.int64) << q
        same = ev_c[1:] == ev_c[:-1]
        s_c, s_lo, s_hi, s_m = ev_c[:-1][same], ev_t[:-1][same], ev_t[1:][same], mask[:-1][same]
        keep = (s_m > 0) & (s_hi > s_lo)
        oc.append(s_c[keep]); olo.append(s_lo[keep]); ohi.append(s_hi[keep]); om.append(s_m[keep])
    return np.concatenate(oc), np.concatenate(olo), np.concatenate(ohi), np.concatenate(om)


class Grid16(object):
    """Receivers on a frame-aligned grid of `cell` metres: cell centres on the surveyed terrain, the terrain slope over
    6 m (capped at 35 degrees, as v15) and the nearest horizon profile. Cells inside a footprint are no receivers, or
    with roofs=True receivers on the roof (5 cm above it, facing up)."""

    def __init__(self, S, F, cell, C, height=0.0, roofs=False):
        self.F, self.cell = F, cell
        self.nx, self.ny = int(math.ceil(F.w / cell)), int(math.ceil(F.h / cell))
        self.u0, self.v0 = F.u0, F.v0
        u = F.u0 + (np.arange(self.nx) + 0.5) * cell
        v = F.v0 + (np.arange(self.ny) + 0.5) * cell
        UU, VV = np.meshgrid(u, v)
        self.uu, self.vv = UU.ravel(), VV.ravel()
        self.xx, self.yy = f_world(F, self.uu, self.vv)
        self.z = z_np(S, self.xx, self.yy)
        self.top = footprint_values(C.rings, C.tops, F.u0, F.v0, cell, self.nx, self.ny)
        self.inside = self.top > -np.inf
        self.roofs = roofs
        if roofs:
            self.zr_eff = np.where(self.inside, self.top + 0.05, self.z + height)
        else:
            self.zr_eff = np.where(self.inside, np.inf, self.z + height)
        h = 6.0
        zx = (z_np(S, self.xx + h, self.yy) - z_np(S, self.xx - h, self.yy)) / (2.0 * h)
        zy = (z_np(S, self.xx, self.yy + h) - z_np(S, self.xx, self.yy - h)) / (2.0 * h)
        sl = np.hypot(zx, zy)
        f = np.where(sl > 0.7, 0.7 / np.where(sl > 0, sl, 1.0), 1.0)
        zx, zy = zx * f, zy * f
        if roofs:
            zx, zy = np.where(self.inside, 0.0, zx), np.where(self.inside, 0.0, zy)     # roofs are flat
        n_ = np.sqrt(zx * zx + zy * zy + 1.0)
        self.nwx, self.nwy, self.nz = -zx / n_, -zy / n_, 1.0 / n_      # normal: world x, y and up
        m = C.M
        self.nlu = m[0] * self.nwx + m[1] * self.nwy                   # the same normal in frame coordinates
        self.nlv = m[2] * self.nwx + m[3] * self.nwy
        self.hw = C.hz_weights(self.xx, self.yy)
        self.Co = Coarse16(self.zr_eff, F.u0, F.v0, cell, self.nx, self.ny)
        self.open = ~self.inside
        self.recv = self.open | self.inside if roofs else self.open
        self.n = self.nx * self.ny
        self.zair = self.z                                     # air temperature at 2 m above this ground
        self.wf = None                                         # wind at head height (the plan's shelter as it is)

    def self_tau(self, d):
        """tan of the elevation of the receiver's own ground plane toward d (0 where the ground falls away)."""
        nd = self.nlu * d[0] + self.nlv * d[1]
        return np.where(nd < 0.0, -nd / self.nz, 0.0)

    def obstruction(self, C, az, tau_min, self_shade=False, cheap=False):
        """crit (tan of the elevation up to which the receiver is shut off: terrain, buildings, its own slope when
        self_shade) and the crown segments above it, for the sun at azimuth az (sun positions above tau_min).
        cheap=True: terrain and own slope only (every sun position of the degree is below every horizon)."""
        d = C.dir_local(az)
        crit = np.zeros(self.nx * self.ny)
        if not cheap:
            k_buildings(C, self, d, tau_min, crit)
        crit = np.maximum(crit, C.tau_at(az, self.hw))
        if self_shade:
            crit = np.maximum(crit, self.self_tau(d))
        if cheap:
            e = np.zeros(0)
            ei = np.zeros(0, np.int64)
            return crit, (ei, e, e, ei), d
        c, lo, hi, cls, _ = k_crowns(C, self, d, tau_min)
        segs = k_segments(c, lo, hi, cls, crit)
        return crit, segs, d


class Points16(object):
    """Receivers standing at points of the plan, each point with one or more heights: the columns of a section plane,
    points on cut roofs and facades. Receivers are given sorted by point, then height. For a direction the ray of
    every point is cast through the walls and crowns of the casters (exactly, as on the grid): crit per receiver is the
    steepest roof edge above it, crowns give their elevation bands. Normals (world x, y, up) make the receiver's own
    plane block the sky behind it: a facade sees nothing behind its wall; ground receivers hg metres above a slope see
    past the slope's plane once they stand above it (the slope taken over 6 m, as on the plan)."""

    BIG = 1.0e5

    def __init__(self, C, X, Y, pid, Z, nrm=None, hg=None, zair=None, wf=None):
        F = C.F
        X = np.asarray(X, float)
        Y = np.asarray(Y, float)
        self.np_ = X.size
        self.pu, self.pv = f_local(F, X, Y)
        self.pid = np.asarray(pid, np.int64)
        self.z = np.asarray(Z, float)
        self.n = self.pid.size
        key = self.pid * self.BIG + self.z
        assert self.n == 0 or np.all(np.diff(key) >= 0), "receivers must be sorted by point and height"
        self.zkey = key
        self.r0 = np.searchsorted(self.pid, np.arange(self.np_), side="left")
        self.r1 = np.searchsorted(self.pid, np.arange(self.np_), side="right")
        zmin = np.full(self.np_, np.inf)
        if self.n:
            np.minimum.at(zmin, self.pid, self.z)
        self.zmin = zmin
        self.hw = C.hz_weights(X, Y)
        if nrm is None:
            nrm = (np.zeros(self.n), np.zeros(self.n), np.ones(self.n))
        self.nwx, self.nwy, self.nz = (np.asarray(q, float) for q in nrm)
        m = C.M
        self.nlu = m[0] * self.nwx + m[1] * self.nwy
        self.nlv = m[2] * self.nwx + m[3] * self.nwy
        self.hg = np.zeros(self.n) if hg is None else np.asarray(hg, float)
        self.open = np.ones(self.n, bool)
        self.zair = self.z - 2.0 if zair is None else np.asarray(zair, float)
        self.wf = wf
        # the walls and crowns that can matter for these points at all
        if self.np_:
            lo_u, hi_u = self.pu.min() - C.reach, self.pu.max() + C.reach
            lo_v, hi_v = self.pv.min() - C.reach, self.pv.max() + C.reach
            ke = ((np.maximum(C.AX, C.BX) >= lo_u) & (np.minimum(C.AX, C.BX) <= hi_u) &
                  (np.maximum(C.AY, C.BY) >= lo_v) & (np.minimum(C.AY, C.BY) <= hi_v))
            kc = (C.CU + C.CR >= lo_u) & (C.CU - C.CR <= hi_u) & (C.CV + C.CR >= lo_v) & (C.CV - C.CR <= hi_v)
        else:
            ke = np.zeros(C.AX.size, bool)
            kc = np.zeros(C.CU.size, bool)
        self.E = dict(AX=C.AX[ke], AY=C.AY[ke], BX=C.BX[ke], BY=C.BY[ke], top=C.top[ke], NX=C.NX[ke], NY=C.NY[ke])
        self.Cw = dict(CU=C.CU[kc], CV=C.CV[kc], CR=C.CR[kc], CLO=C.CLO[kc], CHI=C.CHI[kc], CK=C.CK[kc])
        self.reach = C.reach

    def self_tau(self, d):
        nd = self.nlu * d[0] + self.nlv * d[1]
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(self.nz > 1e-9, -nd / np.where(self.nz > 1e-9, self.nz, 1.0) - self.hg / 6.0,
                         np.where(nd < 0.0, np.inf, 0.0))
        return np.maximum(t, 0.0)

    def _pairs(self, d, blo, bhi):
        """(object, point) pairs whose ray (toward d) meets the across-range [blo, bhi] of each object."""
        dx, dy = d
        bp = -self.pu * dy + self.pv * dx
        ob = np.argsort(bp, kind="stable")
        bs = bp[ob]
        i0 = np.searchsorted(bs, blo - 1e-9, side="left")
        i1 = np.searchsorted(bs, bhi + 1e-9, side="right")
        cnt = np.maximum(i1 - i0, 0)
        tot = int(cnt.sum())
        e = np.repeat(np.arange(cnt.size), cnt)
        p = ob[np.repeat(i0, cnt) + (np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt))]
        return e, p, bp

    def _below(self, p, zz):
        """For each pair: the receivers of its point up to height zz (first index, count)."""
        k1 = np.searchsorted(self.zkey, p * self.BIG + zz, side="right")
        k0 = self.r0[p]
        return k0, np.maximum(k1 - k0, 0)

    def obstruction(self, C, az, tau_min, self_shade=False, cheap=False):
        d = C.dir_local(az)
        dx, dy = d
        n = self.n
        crit = np.zeros(n)
        e0 = np.zeros(0)
        i0_ = np.zeros(0, np.int64)
        segs = (i0_, e0, e0, i0_)
        if n and not cheap:
            E = self.E
            face = (E["NX"] * dx + E["NY"] * dy) < 0.0
            AU, AV, BU, BV, top = E["AX"][face], E["AY"][face], E["BX"][face], E["BY"][face], E["top"][face]
            aA, bA = AU * dx + AV * dy, -AU * dy + AV * dx
            aB, bB = BU * dx + BV * dy, -BU * dy + BV * dx
            ok = bA != bB
            aA, bA, aB, bB, top = aA[ok], bA[ok], aB[ok], bB[ok], top[ok]
            e, p, bp = self._pairs(d, np.minimum(bA, bB), np.maximum(bA, bB))
            if e.size:
                ap = self.pu[p] * dx + self.pv[p] * dy
                t = aA[e] + (bp[p] - bA[e]) * (aB[e] - aA[e]) / (bB[e] - bA[e]) - ap
                tp = top[e]
                k = (t > 0.0) & (t <= self.reach) & (tp - self.zmin[p] >= tau_min * t)
                p, t, tp = p[k], t[k], tp[k]
                k0, cnt = self._below(p, tp - tau_min * t)
                tot = int(cnt.sum())
                if tot:
                    q = np.repeat(np.arange(p.size), cnt)
                    r = np.repeat(k0, cnt) + (np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt))
                    np.maximum.at(crit, r, (tp[q] - self.z[r]) / t[q])
        if n:
            th = C.tau_at(az, self.hw)[self.pid]
            if getattr(self, "hzf", None) is not None:
                th = th - self.hzf.at(az)                 # v16.3: the terrain horizon falls with height
            crit = np.maximum(crit, th)
            if self_shade:
                crit = np.maximum(crit, self.self_tau(d))
        if n and not cheap and self.Cw["CU"].size:
            W = self.Cw
            ac, bc = W["CU"] * dx + W["CV"] * dy, -W["CU"] * dy + W["CV"] * dx
            e, p, bp = self._pairs(d, bc - W["CR"], bc + W["CR"])
            if e.size:
                perp = bp[p] - bc[e]
                rr = W["CR"][e]
                k = np.abs(perp) < rr
                e, p, perp, rr = e[k], p[k], perp[k], rr[k]
                hw = np.sqrt(rr * rr - perp * perp)
                along = ac[e] - (self.pu[p] * dx + self.pv[p] * dy)
                ta, tb = along - hw, along + hw
                k = (tb > 0.0) & (ta <= self.reach)
                e, p, ta, tb = e[k], p[k], np.maximum(ta[k], 0.0), tb[k]
                zhi = W["CHI"][e]
                k0, cnt = self._below(p, zhi - tau_min * ta)
                tot = int(cnt.sum())
                if tot:
                    q = np.repeat(np.arange(p.size), cnt)
                    r = np.repeat(k0, cnt) + (np.arange(tot) - np.repeat(np.cumsum(cnt) - cnt, cnt))
                    z = self.z[r]
                    ta_, tb_ = ta[q], tb[q]
                    lo = np.maximum((W["CLO"][e][q] - z) / tb_, 0.0)
                    with np.errstate(divide="ignore", invalid="ignore"):
                        hi = np.where(ta_ > 0.0, (zhi[q] - z) / np.where(ta_ > 0.0, ta_, 1.0),
                                      np.where(zhi[q] > z, np.inf, -1.0))
                    k = (hi > lo) & (hi >= tau_min)
                    segs = k_segments(r[k], lo[k], hi[k], W["CK"][e][q][k], crit)
        return crit, segs, d


