# ------------------------------------------------------------ sun positions of the analyses
SEASON_OF_MONTH = dict((m, sd["key"]) for sd in SEASONS for m in sd["months"])
SEASON_INDEX = dict((sd["key"], k) for k, sd in enumerate(SEASONS))
MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def by_month(f, dtype=None):
    """f(month) as an array indexed by month 1-12 (index 0 repeats January)."""
    return np.array([f(1)] + [f(m) for m in range(1, 13)], dtype)


def sun_bin(az):
    """The degree of azimuth each sun position falls in."""
    return np.minimum(SUN_BINS - 1, ((np.asarray(az, float) % 360.0) / (360.0 / SUN_BINS)).astype(np.int64))


def minute_sun(E):
    """The sun every minute of every day of 2025 (UTC+3, each minute at its middle), while above the horizon:
    azimuth, elevation, tan(elevation), day of the year (0-364), month, day, local time (h), leaf state."""
    import datetime as _dt
    lat, lon = E["location"]["lat"], E["location"]["lon"]
    days = [_dt.date(2025, 1, 1) + _dt.timedelta(days=k) for k in range(365)]
    MO = np.repeat(np.array([d.month for d in days]), 1440)
    DD = np.repeat(np.array([d.day for d in days]), 1440)
    DAY = np.repeat(np.arange(365), 1440)
    TL = np.tile((np.arange(1440) + 0.5) / 60.0, 365)
    az, el = sun_np(2025, MO, DD, TL - 3.0, lat, lon)
    up = el > 0.0
    mo = MO[up]
    return dict(az=az[up], el=el[up], tau=np.tan(np.radians(el[up])), day=DAY[up], mo=mo, dd=DD[up], tl=TL[up],
                leaf=leaf_on_doy(DAY[up] + 1))


def tmy_offset_h(E):
    """Hours after the time stamp at which the typical year's irradiance applies (PVGIS: the satellite's time, about
    hh:10 UTC); the weather columns apply at the time stamp."""
    if E.get("tmy_offset_h") is not None:
        return float(E["tmy_offset_h"])
    return float(E.get("tmy_minute", 0)) / 60.0


def tmy_table(E):
    """Every hour of the typical year as columns (numpy), with the sun position at the irradiance time and the
    Perez split of the sky: beam (direct + circumsolar, W/m2 normal to the sun), isotropic and horizon-band diffuse."""
    if E.get("tmy_full"):
        cols, A = E["tmy_full_cols"], np.array(E["tmy_full"], float)
    else:
        cols = E.get("tmy_cols") or ["month", "day", "hour_utc", "minute_utc", "ghi", "dni", "dhi", "t2m"]
        A = np.array(E["tmy"], float)
    T = dict((c, A[:, k]) for k, c in enumerate(cols))
    lat, lon = E["location"]["lat"], E["location"]["lon"]
    mo = T["month"].astype(np.int64)
    dd = T["day"].astype(np.int64)
    hu = T["hour_utc"] + T.get("minute_utc", np.zeros(len(A))) / 60.0 + tmy_offset_h(E)
    az, el = sun_np(2021, mo, dd, hu, lat, lon)
    cum = np.concatenate([[0], np.cumsum(MONTH_DAYS)])
    doy = (cum[mo - 1] + dd).astype(float)
    zen = 90.0 - el
    dni, dhi, ghi = T["dni"], T["dhi"], T["ghi"]
    F1, F2 = perez_np(dhi, dni, zen, doy)
    Bv = np.maximum(math.cos(math.radians(85.0)), np.cos(np.radians(zen)))
    up = (el > 0.0) & (ghi > 0.0)
    T.update(mo=mo, dd=dd, az=az, el=el, tau=np.tan(np.radians(np.maximum(el, 0.0))), up=up,
             beam=np.where(up, dni + F1 * dhi / Bv, 0.0), iso=np.where(up, (1.0 - F1) * dhi, 0.0),
             hor=np.where(up, F2 * dhi, 0.0), local=np.round(T["hour_utc"] + 3.0).astype(np.int64) % 24,
             si=by_month(lambda m: SEASON_INDEX[SEASON_OF_MONTH[m]], np.int64)[mo],
             leaf=leaf_on_doy(doy))
    T["full"] = all(c in T for c in ("rh", "ws10", "wd10", "ir"))
    return T


def window_mask(T):
    """The hours of the comfort averaging window (input hours)."""
    kind, rng = hours_window()
    if kind == "daylight":
        return T["el"] > 0.0
    if kind == "all":
        return np.ones(T["el"].size, bool)
    h0, h1 = rng
    return ((T["local"] - h0) % 24) < (h1 - h0)


def days_in_season(key):
    return sum(MONTH_DAYS[m - 1] for m in [sd for sd in SEASONS if sd["key"] == key][0]["months"])


# ------------------------------------------------------------ integrals over the obstruction of one direction
def count_le(ts, x):
    """Number of sorted values ts <= x (x an array)."""
    return np.searchsorted(ts, x, side="right")


def _H(e):
    """int_0^e cos^2 x dx"""
    return e / 2.0 + np.sin(2.0 * e) / 4.0


def _Z(e):
    """int_0^e sin x cos x dx"""
    return np.sin(e) ** 2 / 2.0


def sky_terms(crit, segs, tom, eb=None):
    """For one sector: the blocked part of int cos e de (its solid angle), of int cos^2 e de (horizontal cosine
    weight) and of int sin e cos e de (vertical), terrain, buildings and crowns (by what they block, 1 - tau)
    together; with eb also the last two below elevation eb (the horizon band)."""
    ec = np.arctan(crit)
    out = [np.sin(ec), _H(ec), _Z(ec)]
    if eb is not None:
        ecb = np.minimum(ec, eb)
        out += [_H(ecb), _Z(ecb)]
    sc, slo, shi, sm = segs
    if sc.size:
        n = crit.size
        el_, eh_ = np.arctan(slo), np.arctan(shi)
        f = 1.0 - tom[sm]
        out[0] += np.bincount(sc, f * (np.sin(eh_) - np.sin(el_)), minlength=n)
        out[1] += np.bincount(sc, f * (_H(eh_) - _H(el_)), minlength=n)
        out[2] += np.bincount(sc, f * (_Z(eh_) - _Z(el_)), minlength=n)
        if eb is not None:
            elb, ehb = np.minimum(el_, eb), np.minimum(eh_, eb)
            out[3] += np.bincount(sc, f * (_H(ehb) - _H(elb)), minlength=n)
            out[4] += np.bincount(sc, f * (_Z(ehb) - _Z(elb)), minlength=n)
    return out


HOR_BAND = 12.0                   # deg: the horizon band of the Perez model (sky below 12 deg, as v15)


def sky_pass(G, C, want_k=False):
    """The sky each receiver sees, over 72 sectors of 5 degrees, integrated exactly in elevation: the sky view
    (share of the vault's solid angle) with crowns in and out of leaf, and with want_k the cosine-weighted sky vectors
    (isotropic diffuse on any tilt: n . K) and those of the horizon band. The ground's own slope hides the sky below
    its plane."""
    n = G.n
    ns = SKY_BINS
    dphi = 2.0 * math.pi / ns
    s2 = 2.0 * math.sin(dphi / 2.0)
    eb = math.radians(HOR_BAND) if want_k else None
    states = (True, False)
    toms = dict((lf, tau_mask_table(lf)) for lf in states)
    sa = dict((lf, np.zeros(n)) for lf in states)
    K = dict((lf, np.zeros((3, n))) for lf in states)
    KB = dict((lf, np.zeros((3, n))) for lf in states)
    KB0 = np.zeros((3, n))
    Hb = float(_H(eb)) if want_k else 0.0
    Zb = float(_Z(eb)) if want_k else 0.0
    def obstr(s):
        az = (s + 0.5) * 360.0 / ns
        return G.obstruction(C, az, tau_floor(G, C, az), self_shade=True)

    def use(s, r):                                        # v16.6: the sectors' obstructions found on parallel threads
        crit, segs, d = r
        az = (s + 0.5) * 360.0 / ns
        vx, vy = C.CP.vec(az)
        for lf in states:
            r = sky_terms(crit, segs, toms[lf], eb)
            sa[lf] += r[0]
            if want_k:
                h_ = math.pi / 4.0 - r[1]
                K[lf][0] += (s2 * vx) * h_
                K[lf][1] += (s2 * vy) * h_
                K[lf][2] += dphi * (0.5 - r[2])
                hb = Hb - r[3]
                KB[lf][0] += (s2 * vx) * hb
                KB[lf][1] += (s2 * vy) * hb
                KB[lf][2] += dphi * (Zb - r[4])
        if want_k:
            es = np.minimum(np.arctan(G.self_tau(d)), eb)
            hb = Hb - _H(es)
            KB0[0] += (s2 * vx) * hb
            KB0[1] += (s2 * vy) * hb
            KB0[2] += dphi * (Zb - _Z(es))
    par_ordered(obstr, range(ns), use)
    out = dict(svf=dict((lf, 1.0 - sa[lf] / ns) for lf in states))
    if want_k:
        out.update(K=dict((lf, K[lf] / math.pi) for lf in states), KB=dict((lf, KB[lf] / math.pi) for lf in states),
                   KB0=KB0 / math.pi)
    return out


class Binned(object):
    """Sun positions sorted by degree of azimuth, then group, then tan(elevation), with running sums of weights."""

    def __init__(self, b, g, tau, ng, wts=None):
        o = np.lexsort((tau, g, b))
        self.tau = np.asarray(tau, float)[o]
        self.ng = ng
        self.st = np.searchsorted(np.asarray(b)[o] * ng + np.asarray(g)[o], np.arange(SUN_BINS * ng + 1))
        self.cum = dict((k, np.concatenate([[0.0], np.cumsum(np.asarray(v, float)[o])])) for k, v in (wts or {}).items())

    def span(self, b, g):
        return int(self.st[b * self.ng + g]), int(self.st[b * self.ng + g + 1])

    def trange(self, b):
        a, z = int(self.st[b * self.ng]), int(self.st[(b + 1) * self.ng])
        if z <= a:
            return None
        t = self.tau[a:z]
        return float(t.min()), float(t.max())


class ShadeJob(object):
    """Minutes in shade, every minute the sun is up: of every day of the year (deciduous crowns in leaf between the
    measured leaf-out and leaf-fall days) and of the four key days; crowns count by what they block (1 - tau). v47:
    with july=True also every minute of every July day (group 6; the plan's shade strip along the stream)."""

    def __init__(self, G, MS, july=False):
        n = G.n
        b = sun_bin(MS["az"])
        parts = [(b, np.where(MS["leaf"], 0, 1), MS["tau"])]
        self.days = []
        for k, sd in enumerate(SEASONS):
            mo, dd = sd["day"]
            m = (MS["mo"] == mo) & (MS["dd"] == dd)
            parts.append((b[m], np.full(int(m.sum()), 2 + k), MS["tau"][m]))
            tl = MS["tl"][m]
            self.days.append(dict(daylight=float(m.sum()) / 60.0,
                                  sunrise=(float(tl.min()) - 1.0 / 120.0) if tl.size else None,
                                  sunset=(float(tl.max()) + 1.0 / 120.0) if tl.size else None))
        self.toms = [tau_mask_table(True), tau_mask_table(False)] + [tau_mask_table(leaf_key(sd["key"])) for sd in SEASONS]
        self.july = None
        if july:                                          # v47: July (days 182-212) lies inside the leaf period
            m = MS["mo"] == 7                             # (LEAF_DOY), so crowns in leaf, as the summer key day
            parts.append((b[m], np.full(int(m.sum()), 6), MS["tau"][m]))
            self.toms.append(tau_mask_table(True))
            self.july = dict(daylight=float(m.sum()) / 60.0 / 31.0)      # mean hours of sun up per July day
        self.ng = len(parts)                              # v47: 6 groups, 7 with July
        self.bs = Binned(np.concatenate([p[0] for p in parts]), np.concatenate([p[1] for p in parts]),
                         np.concatenate([p[2] for p in parts]), self.ng)
        self.acc = np.zeros((self.ng, n))
        self.year_daylight = MS["tau"].size / 60.0 / 365.0

    def trange(self, b):
        return self.bs.trange(b)

    def run(self, b, crit, segs):
        par_all([(lambda g_=g: self._run_g(b, g_, crit, segs)) for g in range(self.ng)])   # v17: each g its own sum

    def _run_g(self, b, g, crit, segs):
        sc, slo, shi, sm = segs
        n = crit.size
        if True:
            a, z = self.bs.span(b, g)
            if z <= a:
                return
            ts = self.bs.tau[a:z]
            acc = self.acc[g]
            m = np.flatnonzero(crit >= ts[0])
            if m.size:
                acc[m] += count_le(ts, crit[m])
            if sc.size:
                k = count_le(ts, shi) - count_le(ts, slo)
                q = k > 0
                if q.any():
                    acc += np.bincount(sc[q], (1.0 - self.toms[g][sm[q]]) * k[q], minlength=n)


class RadJob(object):
    """Beam (direct + circumsolar) energy of every hour of the typical year, per season: running sums of beam x sun
    vector over the hours in each degree of azimuth, sorted by elevation; a receiver collects those its obstruction
    lets through (crowns by their transmission)."""

    def __init__(self, G, TT, CP):
        n = G.n
        idx = np.flatnonzero(TT["up"])
        az, el = TT["az"][idx], TT["el"][idx]
        r = np.radians(az)
        ce, se = np.cos(np.radians(el)), np.sin(np.radians(el))
        vx = np.sin(r) * CP.E[0] + np.cos(r) * CP.N[0]
        vy = np.sin(r) * CP.E[1] + np.cos(r) * CP.N[1]
        w = TT["beam"][idx]
        g = TT["si"][idx] * 2 + np.where(TT["leaf"][idx], 0, 1)
        self.bs = Binned(sun_bin(az), g, TT["tau"][idx], 8, dict(x=w * ce * vx, y=w * ce * vy, z=w * se))
        self.V = np.zeros((4, 3, n))
        self.toms = (tau_mask_table(True), tau_mask_table(False))

    def trange(self, b):
        return self.bs.trange(b)

    def run(self, b, crit, segs):
        par_all([(lambda si_=si: self._run_si(b, si_, crit, segs)) for si in range(4)])  # v17: each season its sum

    def _run_si(self, b, si_, crit, segs):
        sc, slo, shi, sm = segs
        n = crit.size
        for g in (2 * si_, 2 * si_ + 1):                 # the season's two groups, in their v16 order
            a, z = self.bs.span(b, g)
            if z <= a:
                continue
            si, tom = g // 2, self.toms[g % 2]
            ts = self.bs.tau[a:z]
            k = count_le(ts, crit)
            if sc.size:
                klo, khi = count_le(ts, slo), count_le(ts, shi)
                q = khi > klo
                f = 1.0 - tom[sm[q]]
            for ci, c in enumerate("xyz"):
                C_ = self.bs.cum[c]
                V = self.V[si, ci]
                V += C_[z] - C_[a + k]
                if sc.size and q.any():
                    V -= np.bincount(sc[q], f * (C_[a + khi[q]] - C_[a + klo[q]]), minlength=n)


PAR_THREADS = 0          # threads for the obstructions and sums (0: one per logical core, v17: all of them; 1: none)
PAR_MAX = 0              # v17 (Nil): every logical core the computer reports (0 = no cap; v16.6: at most 8)


def n_cores():
    """v17: the logical cores to use: all that the operating system reports (PAR_MAX caps it when set)."""
    try:
        n = max(1, int(os.cpu_count() or 1))
    except Exception:
        n = 1
    return min(n, PAR_MAX) if PAR_MAX and PAR_MAX > 0 else n


def _ram_gb():
    """v17: the computer's memory in GB (Windows, macOS, Linux), or None when it cannot be read."""
    try:
        if os.name == "nt":
            import ctypes

            class _MS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]
            m = _MS()
            m.dwLength = ctypes.sizeof(_MS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
            return m.ullTotalPhys / 1e9
        if hasattr(os, "sysconf") and "SC_PHYS_PAGES" in os.sysconf_names:
            return os.sysconf("SC_PHYS_PAGES") * os.sysconf("SC_PAGE_SIZE") / 1e9
        import subprocess
        return int(subprocess.check_output(["sysctl", "-n", "hw.memsize"]).strip()) / 1e9
    except Exception:
        return None


def big_grid_cap():
    """v17: threads for a big grid's sun pass (about 0.7 GB per obstruction in flight): as many as half the memory
    holds (v16.6: always 4)."""
    r = _ram_gb()
    return 4 if r is None else max(2, int(0.5 * r / 0.75))


def par_ordered(fn, items, use, cap=None):
    """v16.6: fn(item) for every item on several threads at once (numpy works outside Python's lock, so the
    obstructions of different sun azimuths run side by side), use(item, result) on this thread in the items' order,
    so every sum is added in the same order as before and the results are identical. At most threads + 1 results are
    held at a time (memory). Falls back to one thread if threads are not available."""
    import os as _os
    n = PAR_THREADS or n_cores()
    if cap:
        n = min(n, cap)
    items = list(items)
    if n > 1 and len(items) > 1:
        try:
            from concurrent.futures import ThreadPoolExecutor
            ex = ThreadPoolExecutor(n)
        except Exception:
            ex = None
        if ex is not None:
            try:
                pend = []
                k = 0
                while k < len(items) and len(pend) < n + 1:
                    pend.append((items[k], ex.submit(fn, items[k])))
                    k += 1
                while pend:
                    it, f = pend.pop(0)
                    r = f.result()
                    if k < len(items):
                        pend.append((items[k], ex.submit(fn, items[k])))
                        k += 1
                    use(it, r)
                    r = None
            finally:
                ex.shutdown(wait=True)
            return
    for it in items:
        use(it, fn(it))


PAR_JOBS = True          # v17: the sums of each sun degree on several threads too (False: on one thread, as v16.7)
_JOB_POOL = []
_JOB_TLS = _threading.local()


def par_all(fns):
    """v17: run independent pieces of work (each writing only its own sums) at once and wait for all of them; one
    after the other when threads are off. Each piece does exactly what it did before, in the same order, so the
    results are identical; only pieces that share no sum ever run side by side. v18: a piece that itself runs pieces
    (a job's own groups) uses a second set of threads, so no thread ever waits for a piece queued behind it (v17 could
    stall that way on a computer with 2 cores)."""
    fns = list(fns)
    if not PAR_JOBS or len(fns) < 2:
        for f in fns:
            f()
        return
    lev = getattr(_JOB_TLS, "level", 0)
    while len(_JOB_POOL) <= lev and lev < 2:
        try:
            from concurrent.futures import ThreadPoolExecutor
            _JOB_POOL.append(ThreadPoolExecutor(PAR_THREADS or n_cores()))
        except Exception:
            _JOB_POOL.append(None)
    ex = _JOB_POOL[lev] if lev < 2 else None
    if ex is None:
        for f in fns:
            f()
        return

    def run(f):
        _JOB_TLS.level = lev + 1
        try:
            f()
        finally:
            _JOB_TLS.level = lev
    futs = [ex.submit(run, f) for f in fns]
    for f in futs:
        f.result()


def sun_pass(G, C, jobs, log=None):
    """One obstruction per degree of sun azimuth, shared by every job (each integrates its own sun positions in that
    degree). Degrees whose every sun position lies below every terrain horizon need only the horizon. v16.6: the
    obstructions of several degrees are found at once on parallel threads (par_ordered); identical results, about
    3.3 times faster on 4 cores."""
    import time as _t
    t0 = _t.time()
    todo = []
    for b in range(SUN_BINS):
        rr = [r for r in (j.trange(b) for j in jobs) if r is not None]
        if not rr:
            continue
        todo.append((b, min(r[0] for r in rr), max(r[1] for r in rr)))

    def obstr(t):
        b, tmin, tmax = t
        az = (b + 0.5) * 360.0 / SUN_BINS
        hmin = tau_floor(G, C, az)
        return G.obstruction(C, az, max(tmin, hmin), self_shade=True, cheap=tmax <= hmin)

    def use(t, r):                                       # v17: the jobs (shade, comfort ...) side by side
        par_all([(lambda j_=j: j_.run(t[0], r[0], r[1])) for j in jobs])
    par_ordered(obstr, todo, use, cap=big_grid_cap() if G.n > 1000000 else None)    # big grids: ~0.7 GB each
    nb = len(todo)
    if log is not None:
        log.append(("sun pass", nb, _t.time() - t0))


# ------------------------------------------------------------ wind shelter (numpy)
WIND_BINS = 36                    # 10-degree sectors of the wind direction, centred on N, 10, 20 ... degrees


def wind_bin(wd):
    return np.round(np.asarray(wd, float) / (360.0 / WIND_BINS)).astype(np.int64) % WIND_BINS


def wind_rasters(solids, F, cell, pad):
    """Obstacle heights above their own ground on the frame's grid widened by pad cells on every side: buildings
    (footprints with their courtyards), evergreen crowns and deciduous crowns (discs of their measured radius)."""
    bl, gB, trees = solids
    nx, ny = int(math.ceil(F.w / cell)), int(math.ceil(F.h / cell))
    nxp, nyp = nx + 2 * pad, ny + 2 * pad
    u0, v0 = F.u0 - pad * cell, F.v0 - pad * cell
    R = pad * cell + 10.0
    fb = F.bb
    box = (fb[0] - R, fb[1] - R, fb[2] + R, fb[3] + R)
    groups, vals = [], []
    for b in bl:
        if not bb_hit(b["bb"], box):
            continue
        rings = [[F.local(x, y) for x, y in b["P"]]] + [[F.local(x, y) for x, y in h] for h in (b.get("holes") or ())]
        groups.append(rings)
        vals.append(b["H"])
    HB = footprint_values(groups, vals, u0, v0, cell, nxp, nyp)
    out = [np.maximum(HB, 0.0)]
    for ever in (True, False):
        tr = [t for t in trees if (t["kind"] in EVERGREEN) == ever and box[0] <= t["x"] <= box[2] and box[1] <= t["y"] <= box[3]]
        loc = [F.local(t["x"], t["y"]) for t in tr]
        H_ = disc_values([p[0] for p in loc], [p[1] for p in loc], [t["r"] for t in tr], [t["hi"] for t in tr],
                         u0, v0, cell, nxp, nyp)
        out.append(np.maximum(H_, 0.0))
    return np.stack(out).reshape(3, nyp, nxp).astype(np.float32)


def wake_np(curve, xh):
    xs = np.array([c[0] for c in curve])
    fs = np.array([c[1] for c in curve])
    return np.interp(xh, xs, fs, left=fs[0], right=1.0)


def shelter_all(solids, F, cell, C, idx, fetch=300.0):
    """Share of the open-ground wind left at the receivers idx for every wind sector, crowns in and out of leaf: the
    strongest wake of any building or crown upwind within the fetch (also beyond the frame), from the windbreak wake
    curves (Heisler & DeWalle 1988), at the obstacle's distance in its own heights."""
    nx, ny = int(math.ceil(F.w / cell)), int(math.ceil(F.h / cell))
    K = int(fetch / cell)
    pad = K + 1
    R3 = wind_rasters(solids, F, cell, pad)
    have = [bool(R3[q].any()) for q in range(3)]
    out = np.ones((WIND_BINS, 2, idx.size), np.float32)
    for k in range(WIND_BINS):
        ux, uy = C.dir_local(k * 360.0 / WIND_BINS)        # unit vector toward where the wind comes from
        Sm = np.zeros((3, ny, nx), np.float32)
        tmp = np.empty((3, ny, nx), np.float32)
        for st in range(1, K + 1):
            di, dj = int(round(st * ux)), int(round(st * uy))
            src = R3[:, pad + dj:pad + dj + ny, pad + di:pad + di + nx]
            np.multiply(src, np.float32(1.0 / (st * cell)), out=tmp)
            np.maximum(Sm, tmp, out=Sm)
        Sm = Sm.reshape(3, -1)[:, idx].astype(float)
        with np.errstate(divide="ignore"):
            xh = np.where(Sm > 0.0, 1.0 / np.where(Sm > 0.0, Sm, 1.0), np.inf)
        fB = wake_np(WAKE_SOLID, xh[0]) if have[0] else 1.0
        fE = wake_np(WAKE_LEAFY, xh[1]) if have[1] else 1.0
        fD_on = wake_np(WAKE_LEAFY, xh[2]) if have[2] else 1.0
        fD_off = wake_np(WAKE_BARE, xh[2]) if have[2] else 1.0
        base = np.minimum(fB, fE)
        out[k, 0] = np.minimum(base, fD_on)
        out[k, 1] = np.minimum(base, fD_off)
    return out


# ------------------------------------------------------------ felt temperature, hour by hour (numpy)
F_EFF = 0.725                     # SolarCal: fraction of the body's surface exchanging radiation (standing)
MRT_K = (0.7 / 0.95) / (F_EFF * 6.012)   # SolarCal: absorbed short-wave flux (W/m2) -> mean radiant temperature (K)
MRT_ALBEDO = 0.25
UTCI_EDGES = np.array([-40.0, -27.0, -13.0, 0.0, 9.0, 26.0, 32.0, 38.0, 46.0]) if HAVE_NP else None
UTCI_NAMES = ("extreme cold", "very strong cold", "strong cold", "moderate cold", "slight cold", "no thermal stress",
              "moderate heat", "strong heat", "very strong heat", "extreme heat")
_P7 = np.arange(7) if HAVE_NP else None


def es_hpa_np(t):
    """es_hpa for arrays (the same formula)."""
    g = (-2836.5744, -6028.076559, 19.54263612, -0.02737830188, 0.000016261698, 7.0229056e-10, -1.8680009e-13)
    tk = np.asarray(t, float) + 273.15
    es = 2.7150305 * np.log(tk)
    for k, c in enumerate(g):
        es = es + c * tk ** (k - 2)
    return np.exp(es) * 0.01


def utci_K(ta, pa):
    """For each hour: the UTCI polynomial (Broede et al. 2012) at that hour's air temperature and vapour pressure as a
    polynomial in wind (b) and mrt - ta (e), with its first and second derivatives in air temperature (the second
    halved): K[h, 0..2, b, e]. Exact rearrangements of the published coefficients."""
    ta = np.asarray(ta, float)
    pa = np.asarray(pa, float)
    H = ta.size
    TA = np.ones((H, 7))
    PA = np.ones((H, 7))
    for k in range(1, 7):
        TA[:, k] = TA[:, k - 1] * ta
        PA[:, k] = PA[:, k - 1] * pa
    K = np.zeros((H, 3, 7, 7))
    for c, a, b, e, f in UTCI_COEF:
        K[:, 0, b, e] += c * TA[:, a] * PA[:, f]
        if a > 0:
            K[:, 1, b, e] += (c * a) * TA[:, a - 1] * PA[:, f]
        if a > 1:
            K[:, 2, b, e] += (c * a * (a - 1) / 2.0) * TA[:, a - 2] * PA[:, f]
    return K


def utci_eval(Kh, va, D, dl, dv=0.1, dd=0.25):
    """UTCI of many points of one hour: the hour's polynomial tabulated over the wind (0.1 m/s) and mrt - ta (0.25 K)
    present in that hour and read bilinearly, corrected to each point's own air temperature (dl: its difference from
    the hour's, a fraction of a kelvin) to second order. Within 0.01 K of the polynomial."""
    v0 = 0.5
    nv = int((float(va.max()) - v0) / dv) + 2
    d0 = math.floor(float(D.min()))
    nd = int((float(D.max()) - d0) / dd) + 2
    Vp = (v0 + np.arange(nv) * dv)[:, None] ** _P7
    Dp = (d0 + np.arange(nd) * dd)[:, None] ** _P7
    T0, T1, T2 = [(Vp @ Kh[q] @ Dp.T).ravel() for q in range(3)]
    fp_ = (va - v0) * (1.0 / dv)
    p = np.minimum(nv - 2, fp_.astype(np.int64))
    a = fp_ - p
    fq = (D - d0) * (1.0 / dd)
    q = np.minimum(nd - 2, fq.astype(np.int64))
    b = fq - q
    i = p * nd + q
    out = None
    for j, w in ((i, (1.0 - a) * (1.0 - b)), (i + nd, a * (1.0 - b)), (i + 1, (1.0 - a) * b), (i + nd + 1, a * b)):
        V = T2[j]
        V *= dl
        V += T1[j]
        V *= dl
        V += T0[j]
        V *= w
        out = V if out is None else out + V
    return out


def proj_np(alt):
    return np.interp(np.clip(alt, 0.0, 90.0), np.arange(19) * 5.0, np.array(FP_STAND))


class ComfortJob(object):
    """Felt temperature (UTCI) every hour of the averaging window on every open receiver: air temperature at the
    receiver's height, wind of that hour's sector through the shelter of the buildings and crowns upwind, mean radiant
    temperature from SolarCal with the receiver's sun (from the obstruction of that hour's sun azimuth) and sky view.
    Summed per season: mean UTCI, hours in sun, the stress categories, the mean by hour of the day."""

    def __init__(self, G, TT, win, svf, shel):
        self.idx = np.flatnonzero(G.open)
        no = self.idx.size
        self.no = no
        self.svf = dict((lf, svf[lf][self.idx]) for lf in (True, False))
        self.shel = shel
        self.dl = LAPSE * (G.zair[self.idx] - CLIMATE["elevation"])
        self.wf = None if G.wf is None else G.wf[self.idx]
        hrs = np.flatnonzero(win)
        self.hrs = hrs
        ta, rh, ir = TT["t2m"], TT["rh"], TT["ir"]
        el = TT["el"]
        self.ta, self.u10 = ta, TT["ws10"]
        self.wb = wind_bin(TT["wd10"])
        self.leaf, self.si, self.local = TT["leaf"], TT["si"], TT["local"]
        self.tau = TT["tau"]
        self.pa = es_hpa_np(ta) * rh / 1000.0
        sun = el >= 2.0
        self.c1 = np.where(sun, MRT_K * proj_np(el) * TT["dni"], 0.0)
        self.c2 = np.where(sun, MRT_K * 0.5 * F_EFF * (TT["dhi"] + TT["ghi"] * MRT_ALBEDO), 0.0)
        tsky = (np.maximum(1.0, ir) / (0.95 * 5.6697e-8)) ** 0.25 - 273.15
        self.B = self.c2 + 0.5 * (tsky - ta)
        self.K = utci_K(ta, self.pa)
        sh = hrs[sun[hrs] & (TT["dni"][hrs] > 0.0)]
        self.dark = np.setdiff1d(hrs, sh)
        bb = sun_bin(TT["az"][sh])
        o = np.lexsort((self.tau[sh], bb))
        self.sh, self.sh_b = sh[o], bb[o]
        self.st = np.searchsorted(self.sh_b, np.arange(SUN_BINS + 1))
        self.pos = np.full(G.n, -1, np.int64)
        self.pos[self.idx] = np.arange(no)
        self.toms = {True: tau_mask_table(True), False: tau_mask_table(False)}
        self.su = np.zeros((4, no))
        self.sT = np.zeros((4, no))
        self.nh = np.zeros(4, np.int64)
        self.hist = np.zeros((4, 10))
        self.split = np.zeros((4, 4))                         # sum and count in sun, sum and count in shade
        self.lh = np.zeros((4, 24, 2))                        # by local hour: sum of the site means, hours
        self.nc = np.zeros((4, no))                           # v33: hours with no thermal stress, UTCI 9 to 26 °C
        self.nz = np.zeros((4, no))                           # v33: hours in the 18 to 26 °C part of that band

    def trange(self, b):
        a, z = int(self.st[b]), int(self.st[b + 1])
        if z <= a:
            return None
        return float(self.tau[self.sh[a]]), float(self.tau[self.sh[z - 1]])

    def run(self, b, crit, segs):
        a, z = int(self.st[b]), int(self.st[b + 1])
        if z <= a:
            return
        co = crit[self.idx]
        sc, slo, shi, sm = segs
        ps = self.pos[sc] if sc.size else sc
        k = ps >= 0
        ps, slo, shi, sm = ps[k], slo[k], shi[k], sm[k]
        def one(h):
            tau = self.tau[h]
            T = (tau > co).astype(float)
            if ps.size:
                m = (slo < tau) & (shi >= tau)
                if m.any():
                    T[ps[m]] = self.toms[bool(self.leaf[h])][sm[m]]
            return T, self.felt(h, T)
        # v17: the hours' felt temperatures on several threads, their sums added here in the hours' order
        self._hours(list(self.sh[a:z]), one)

    def finish(self):
        self._hours(list(self.dark), lambda h: (None, self.felt(h, None)))

    def _hours(self, hs, one):
        if PAR_JOBS:
            par_ordered(one, hs, lambda h, r: self.hour(h, r[0], r[1]))
        else:
            for h in hs:
                T, U = one(h)
                self.hour(h, T, U)

    def felt(self, h, T):
        """UTCI of every open receiver in hour h (T: its sun, 0..1; None: no direct sun)."""
        lf = bool(self.leaf[h])
        sv = self.svf[lf]
        sh = self.shel[self.wb[h], 0 if lf else 1]
        va = np.clip(self.u10[h] * (sh if self.wf is None else sh * self.wf), 0.5, 17.0)
        D = sv * (self.B[h] - 0.5 * self.dl)
        if T is not None:
            D = D + self.c1[h] * T
        return utci_eval(self.K[h], va, D, self.dl)

    def hour(self, h, T, U=None):
        if U is None:
            U = self.felt(h, T)
        si = self.si[h]
        self.su[si] += U
        self.nh[si] += 1
        ge = [U.size] + [np.count_nonzero(U >= e) for e in UTCI_EDGES] + [0]
        self.hist[si] += [ge[k] - ge[k + 1] for k in range(10)]
        self.nc[si] += (U >= 9.0) & (U < 26.0)                # the histogram's own band edges (UTCI_EDGES)
        self.nz[si] += (U >= 18.0) & (U < 26.0)
        if T is not None:                                     # an hour with direct sun: in sun or in shade
            self.sT[si] += T
            ins = T > 0.5
            ns_ = int(ins.sum())
            us = float(U[ins].sum()) if ns_ else 0.0
            self.split[si] += (us, ns_, float(U.sum()) - us, U.size - ns_)
        self.lh[si, self.local[h]] += (float(U.mean()), 1)


# ------------------------------------------------------------ the analyses of one frame
def env16_frame(S, E, solids, F, cell=3.0, want_shade=True, want_comfort=True, log=None):
    """Shade (key days and the mean day of the year) and the felt-temperature, wind and air-temperature means of
    every season over the averaging window, on one grid of the frame: one obstruction per degree of sun azimuth
    serves both."""
    import time as _t
    log = log if log is not None else []
    t0 = _t.time()
    C = Casters16(S, E, solids, F)
    G = Grid16(S, F, cell, C)
    log.append(("grid", G.nx * G.ny, _t.time() - t0))
    TT = tmy_table(E)
    jobs = []
    SJ = CJ = None
    if want_shade:
        SJ = ShadeJob(G, minute_sun(E), july=True)       # v47: + the July mean day
        jobs.append(SJ)
    if want_comfort:
        t1 = _t.time()
        sky = sky_pass(G, C)
        log.append(("sky", SKY_BINS, _t.time() - t1))
        t1 = _t.time()
        idx = np.flatnonzero(G.open)
        shel = shelter_all(solids, F, cell, C, idx)
        log.append(("shelter", WIND_BINS, _t.time() - t1))
        win = window_mask(TT)
        CJ = ComfortJob(G, TT, win, sky["svf"], shel)
        jobs.append(CJ)
    sun_pass(G, C, jobs, log)
    out = dict(cell=cell, nx=G.nx, ny=G.ny, frame=list(F.P), open=G.open.copy(), z=G.z.astype(np.float32))
    if SJ is not None:
        days = {}
        for k, sd in enumerate(SEASONS):
            h = (SJ.acc[2 + k] / 60.0).astype(np.float32)
            h[~G.open] = np.nan
            days[sd["key"]] = dict(SJ.days[k], hours=h)
        yr = ((SJ.acc[0] + SJ.acc[1]) / 60.0 / 365.0).astype(np.float32)
        yr[~G.open] = np.nan
        out["shade"] = dict(days=days, year=dict(hours=yr, daylight=SJ.year_daylight))
        if SJ.july is not None:                           # v47: hours in shade on the mean July day (31 days)
            jl = (SJ.acc[6] / 60.0 / 31.0).astype(np.float32)
            jl[~G.open] = np.nan
            out["shade"]["july"] = dict(hours=jl, daylight=SJ.july["daylight"])
    if CJ is not None:
        t1 = _t.time()
        CJ.finish()
        log.append(("dark hours", CJ.dark.size, _t.time() - t1))
        out["comfort"] = comfort_results(G, TT, win, CJ, sky["svf"], shel)
    log.append(("frame total", 0, _t.time() - t0))
    return out


def comfort_results(G, TT, win, CJ, svf, shel):
    """Per season over the window hours: mean UTCI, air temperature, wind at head height and share of the hours in
    direct sun on every open receiver; the stress categories over all open receiver-hours; the climate of those hours
    (rose, typical day)."""
    n = G.nx * G.ny
    idx = CJ.idx
    res = dict(window=hours_window(), label=window_label(), label_short=window_label(True), seasons={})
    ta, u10, wd = TT["t2m"], TT["ws10"], TT["wd10"]
    for si, sd in enumerate(SEASONS):
        hs = np.flatnonzero(win & (TT["si"] == si))
        N = max(1, hs.size)

        def grid(v):
            g = np.full(n, np.nan, np.float32)
            g[idx] = v
            return g
        W = np.zeros((WIND_BINS, 2))
        np.add.at(W, (wind_bin(wd[hs]), np.where(TT["leaf"][hs], 0, 1)), u10[hs])
        uped = np.zeros(idx.size)
        for k, l in zip(*np.nonzero(W)):
            uped += W[k, l] * shel[k, l]
        uped *= PED_WIND / N
        sun_h = int(((TT["el"][hs] >= 2.0) & (TT["dni"][hs] > 0.0)).sum())
        sp = CJ.split[si]
        # the climate of the window hours: wind rose (16 sectors x the classes of CLIMATE), typical day
        cls = CLIMATE["classes"]
        rose = np.zeros((16, len(cls)))
        calm = 0
        for h in hs:
            if u10[h] < cls[0]:
                calm += 1
                continue
            k = int(round(wd[h] / 22.5)) % 16
            c = max(q for q in range(len(cls)) if u10[h] >= cls[q])
            rose[k, c] += 1
        allh = np.flatnonzero(TT["si"] == si)
        day = []
        for lh in range(24):
            q = allh[TT["local"][allh] == lh]
            v = np.sort(ta[q])
            day.append((float(v.mean()), float(v[int(0.1 * (v.size - 1))]), float(v[int(0.9 * (v.size - 1))])) if v.size else (None, None, None))
        res["seasons"][sd["key"]] = dict(
            hours=int(hs.size), sun_hours=sun_h,
            utci=grid(CJ.su[si] / N), sun=grid(CJ.sT[si] / max(1, sun_h)), ta=grid(float(ta[hs].mean()) + CJ.dl),
            uped=grid(uped), hist=CJ.hist[si].tolist(),
            utci_sun=(sp[0] / sp[1]) if sp[1] else None, utci_shade=(sp[2] / sp[3]) if sp[3] else None,
            by_hour=[((CJ.lh[si, k, 0] / CJ.lh[si, k, 1]) if CJ.lh[si, k, 1] else None) for k in range(24)],
            ta_mean=float(ta[hs].mean()) if hs.size else None, rh_mean=float(TT["rh"][hs].mean()) if hs.size else None,
            u10_mean=float(u10[hs].mean()) if hs.size else None,
            rose=(rose / N).tolist(), calm=calm / float(N), day=day)
    # v33 (T8): the whole year's window hours on every open receiver, the share with no thermal stress
    Ny = sum(res["seasons"][sd["key"]]["hours"] for sd in SEASONS)
    if Ny:
        def ygrid(v):
            g = np.full(n, np.nan, np.float32)
            g[idx] = v
            return g
        res["year"] = dict(hours=int(Ny), comfort=ygrid(100.0 * CJ.nc.sum(0) / Ny),
                           comfort18=ygrid(100.0 * CJ.nz.sum(0) / Ny), utci=ygrid(CJ.su.sum(0) / Ny),
                           share={sd["key"]: 100.0 * float(CJ.nc[si].mean()) / max(1, res["seasons"][sd["key"]]["hours"])
                                  for si, sd in enumerate(SEASONS)})
    return res


def rad_totals(G, TT, sky, RJ):
    """Mean kWh/m2 per day of each season on every receiver: direct and circumsolar collected through its obstruction
    (RadJob), isotropic sky through its cosine-weighted sky (n . K), the horizon band on tilted surfaces and the
    ground's reflection, from every hour of the typical year."""
    nwx, nwy, nz = G.nwx, G.nwy, G.nz
    sinb = np.sqrt(np.maximum(0.0, 1.0 - nz * nz))
    out = {}
    for si, sd in enumerate(SEASONS):
        up = TT["up"] & (TT["si"] == si)
        V = RJ.V[si]
        tot = nwx * V[0] + nwy * V[1] + nz * V[2]
        for lf in (True, False):
            mm = up & (TT["leaf"] == lf)
            if not mm.any():
                continue
            K, KB, KB0 = sky["K"][lf], sky["KB"][lf], sky["KB0"]
            kiso = np.maximum(0.0, nwx * K[0] + nwy * K[1] + nz * K[2])
            nb = nwx * KB[0] + nwy * KB[1] + nz * KB[2]
            nb0 = nwx * KB0[0] + nwy * KB0[1] + nz * KB0[2]
            khor = np.where(nb0 > 1e-9, sinb * np.clip(nb / np.where(nb0 > 1e-9, nb0, 1.0), 0.0, 1.0), 0.0)
            tot = tot + float(TT["iso"][mm].sum()) * kiso + float(TT["hor"][mm].sum()) * khor
        tot = tot + ALBEDO * float(TT["ghi"][up].sum()) * (1.0 - nz) / 2.0
        out[sd["key"]] = tot / days_in_season(sd["key"]) / 1000.0
    return out


def env16_focus(S, E, solids, F, cell=1.5, log=None):
    """Incident solar radiation on the ground and on every roof of the focus area, mean kWh/m2 per day of each season:
    every hour of the typical year, direct + circumsolar through the obstruction of its sun position, isotropic
    diffuse through the cosine-weighted sky each receiver sees, Perez horizon band and ground reflection on slopes."""
    import time as _t
    log = log if log is not None else []
    t0 = _t.time()
    C = Casters16(S, E, solids, F)
    G = Grid16(S, F, cell, C, roofs=True)
    TT = tmy_table(E)
    t1 = _t.time()
    sky = sky_pass(G, C, want_k=True)
    log.append(("focus sky", SKY_BINS, _t.time() - t1))
    RJ = RadJob(G, TT, C.CP)
    sun_pass(G, C, [RJ], log)
    vals = rad_totals(G, TT, sky, RJ)
    seasons = {}
    yr = np.zeros(G.n)
    for sd in SEASONS:
        nd = days_in_season(sd["key"])
        v = vals[sd["key"]].astype(np.float32)
        yr += vals[sd["key"]] * nd
        up = TT["up"] & (TT["si"] == SEASON_INDEX[sd["key"]])
        seasons[sd["key"]] = dict(kwh=v, ghi=float(TT["ghi"][up].sum()) / nd / 1000.0,
                                  ground_mean=float(np.mean(v[G.open])) if G.open.any() else None,
                                  roof_mean=float(np.mean(v[G.inside])) if G.inside.any() else None)
    yr /= 365.0
    out = dict(cell=cell, nx=G.nx, ny=G.ny, frame=list(F.P), roof=G.inside.copy(), seasons=seasons,
               year=yr.astype(np.float32), ghi_year=float(TT["ghi"][TT["up"]].sum()) / 365.0 / 1000.0,
               svf=sky["svf"][True].astype(np.float32))
    log.append(("focus total", G.nx * G.ny, _t.time() - t0))
    return out


class TerrainRaster(TRCore):
    """The survey terrain sampled every 5 m over a box (numpy, the exact z_at values at the nodes), read
    bilinearly: the ground under a sound path. With a frame F and a reach pad only the nodes within pad of the frame
    (plus two cells, for the bilinear reads at its edge) are computed: a sound path runs from a receiver in the frame
    to a road piece at most R away, so it never leaves the frame grown by R; the corners of a turned frame's box
    lie far from every survey sample and cost most of the time."""

    def __init__(self, S, box, cell=5.0, F=None, pad=None):
        self.x0, self.y0, self.c = box[0], box[1], cell
        self.nx = int(math.ceil((box[2] - box[0]) / cell)) + 1
        self.ny = int(math.ceil((box[3] - box[1]) / cell)) + 1
        X = self.x0 + np.arange(self.nx) * cell
        Y = self.y0 + np.arange(self.ny) * cell
        XX, YY = np.meshgrid(X, Y)
        xs, ys = XX.ravel(), YY.ravel()
        Z = np.zeros(xs.size)
        if F is not None and pad is not None:
            uu, vv = f_local(F, xs, ys)
            g = pad + 2.0 * cell
            need = (uu >= F.u0 - g) & (uu <= F.u1 + g) & (vv >= F.v0 - g) & (vv <= F.v1 + g)
        else:
            need = np.ones(xs.size, bool)
        Z[need] = z_np(S, xs[need], ys[need])
        self.Z = Z.reshape(self.ny, self.nx).tolist()


NOISE_TOUCH = 0.5        # m: v16.4: buildings closer than this (party walls, shared gables) are one block for the sound
#                          that bends around a building's sides: the way round goes round the whole block


def noise_blocks(bl, grid):
    """v16.4: the buildings that touch (within NOISE_TOUCH) joined into blocks, each block's convex hull kept on its
    buildings as b["_hull"] (counter-clockwise): the outline sound has to bend around at the block's ends."""
    par = list(range(len(bl)))

    def root(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i
    idx = dict((id(b), k) for k, b in enumerate(bl))
    t2 = NOISE_TOUCH * NOISE_TOUCH

    def near(P, Q):
        n = len(Q)
        for px, py in P:
            for q in range(n):
                ax, ay = Q[q]
                bx, by = Q[(q + 1) % n]
                dx, dy = bx - ax, by - ay
                L2 = dx * dx + dy * dy
                t = 0.0 if L2 <= 0.0 else max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / L2))
                ex, ey = ax + dx * t - px, ay + dy * t - py
                if ex * ex + ey * ey <= t2:
                    return True
        return False
    for k, b in enumerate(bl):
        bb = b["bb"]
        for c in grid.query((bb[0] - NOISE_TOUCH, bb[1] - NOISE_TOUCH, bb[2] + NOISE_TOUCH, bb[3] + NOISE_TOUCH)):
            j = idx.get(id(c))
            if j is None or j <= k:
                continue
            cb = c["bb"]
            if cb[0] > bb[2] + NOISE_TOUCH or cb[2] < bb[0] - NOISE_TOUCH or cb[1] > bb[3] + NOISE_TOUCH or \
                    cb[3] < bb[1] - NOISE_TOUCH:
                continue
            if root(k) != root(j) and (near(b["P"], c["P"]) or near(c["P"], b["P"]) or pip(c["P"][0][0], c["P"][0][1], b["P"])):
                par[root(k)] = root(j)
    groups = {}
    for k in range(len(bl)):
        groups.setdefault(root(k), []).append(bl[k])
    for g_ in groups.values():
        H = convex_hull([tuple(p) for b in g_ for p in b["P"]])
        for b in g_:
            b["_hull"] = H
    return len(groups)


class NoiseModel(NoiseCore):
    """Road traffic noise at any receiver: RLS-90 emission per road piece (noise_sources), segment method with
    divergence and air absorption over the 3D distance, ground (Dbm) and building screening (Dz). In each of 36 directions the buildings
    crossed by the ray are taken in order up to the first one whose roof reaches the receiver's height; the most
    effective of them screens each source behind it. The plan map (receivers 4 m above ground) and the sections
    (receivers at every height) use this same model. v16.4: a building block screens by the way over its roof AND the
    two ways round its sides (lateral diffraction, ISO 9613-2 7.4), combined by energy: a detached house no longer
    casts a sharp, deep sound shadow as if it were an endless wall (lateral_db)."""

    def __init__(self, S, solids, R=300.0, h_src=0.5, nbin=36):
        self.S, self.R, self.h_src, self.nbin = S, R, h_src, nbin
        bl = solids[0]
        src = noise_sources(S)
        gS = Grid(50.0)
        for s in src:
            mx, my = (s["a"][0] + s["b"][0]) / 2.0, (s["a"][1] + s["b"][1]) / 2.0
            s["m"] = (mx, my)
            s["lgL"] = 10.0 * math.log10(s["L"])
            s["zs"] = s["z"] + h_src
            gS.add(s, (mx, my, mx, my))
        gR = Grid(15.0)
        for b in bl:
            gR.add(b, b["bb"])
        self.src, self.gS, self.gR = src, gS, gR
        self.n_blocks = noise_blocks(bl, gR)
        self.wbin = 2.0 * math.pi / nbin
        fb = S.F.bb
        self.TR = TerrainRaster(S, (fb[0] - R - 20.0, fb[1] - R - 20.0, fb[2] + R + 20.0, fb[3] + R + 20.0), F=S.F,
                                pad=R + 20.0)


# ------------------------------------------------------------ v17: the sound model on every core
# Rhino's Python runs Python code on one core at a time (its global lock), so threads cannot speed up the sound model,
# which is plain Python. v17 hands the receivers to separate worker processes of Rhino 8's own Python (the python
# executable Rhino installs under .rhinocode, the same version as Rhino's), one per core. Each worker runs the same
# code (NOISE_KERNEL) on the same data, and every receiver is computed whole by one worker, so the levels are the
# same numbers, to the last digit, as computing them one by one in Rhino:
#   * the worker's Python must give exactly the same results as Rhino's on a battery of the maths it uses
#     (_math_probe), and
#   * the first receivers of every worker are also computed in Rhino and must match exactly;
# otherwise, or when no worker Python is found or anything fails, everything is computed in Rhino as in v16.7, and
# the log says why.
PAR_PROCS = 0              # v17: worker processes for the sound model: 0 = one per core, 1 = none (as v16.7)
PY_WORKER = ""             # v17: a python executable to use for them ("" = Rhino 8's own, found by itself)
_NOISE_PY = {}


def _cores():
    return n_cores()


def _py_candidates():
    import sys
    home = os.path.expanduser("~")
    c = []
    if PY_WORKER:
        c.append(PY_WORKER)
    exe = getattr(sys, "executable", "") or ""
    if os.path.basename(exe).lower().startswith("python"):
        c.append(exe)
    base = getattr(sys, "base_prefix", "") or getattr(sys, "prefix", "")
    for b in (base, os.path.join(home, ".rhinocode", "py39-rh8")):
        if b:
            c += [os.path.join(b, "python.exe"), os.path.join(b, "bin", "python3"), os.path.join(b, "bin", "python3.9"),
                  os.path.join(b, "python3"), os.path.join(b, "bin", "python")]
    out = []
    for x in c:
        if x and x not in out and os.path.isfile(x):
            out.append(x)
    return out


def _kernel_file():
    import tempfile, hashlib
    h = hashlib.sha1(NOISE_KERNEL.encode("utf-8")).hexdigest()[:12]
    d = os.path.join(tempfile.gettempdir(), "selinus_workers")
    if not os.path.isdir(d):
        os.makedirs(d)
    f = os.path.join(d, "selinus_noise_kernel_%s.py" % h)
    if not os.path.isfile(f):
        with open(f + ".tmp", "w", encoding="utf-8") as fh:
            fh.write(NOISE_KERNEL + "\n\nif __name__ == '__main__':\n    import sys\n    _noise_worker_main(sys.argv)\n")
        os.replace(f + ".tmp", f)
    return f, d


def _popen_kw():
    kw = {}
    if os.name == "nt":
        kw["creationflags"] = 0x08000000             # no console window per worker
    return kw


def noise_worker_python():
    """The python executable the sound workers use, or None (with the reason in _NOISE_PY["why"])."""
    if "py" in _NOISE_PY:
        return _NOISE_PY["py"]
    import subprocess
    _NOISE_PY["py"], _NOISE_PY["why"] = None, "no python executable found beside Rhino"
    try:
        kf, _ = _kernel_file()
    except Exception as ex:
        _NOISE_PY["why"] = "cannot write to the temp folder ({})".format(ex)
        return None
    want = _math_probe()
    for py in _py_candidates():
        try:
            r = subprocess.run([py, "-I", kf, "--probe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120,
                               **_popen_kw())
            got = r.stdout.decode("utf-8", "replace").strip()
            if r.returncode == 0 and got == want:
                _NOISE_PY["py"], _NOISE_PY["why"] = py, ""
                return py
            _NOISE_PY["why"] = "{} does not compute exactly like Rhino's Python".format(py)
        except Exception as ex:
            _NOISE_PY["why"] = "{} could not be started ({})".format(py, type(ex).__name__)
    return None


def _noise_model_data(NM):
    """The sound model as plain data (lists, dicts, numbers) for the workers: only what a receiver reads."""
    b_ = {}
    gR = {}
    for k, lst in NM.gR.d.items():
        row = []
        for b in lst:
            sb = b_.get(id(b))
            if sb is None:
                sb = dict(P=b["P"], bb=b["bb"], top=b["top"])
                if b.get("holes") is not None:
                    sb["holes"] = b["holes"]
                if "_hull" in b:
                    sb["_hull"] = b["_hull"]
                sb = b_[id(b)] = sb
            row.append(sb)
        gR[k] = row
    s_ = {}
    gS = {}
    for k, lst in NM.gS.d.items():
        row = []
        for s in lst:
            ss = s_.get(id(s))
            if ss is None:
                ss = s_[id(s)] = dict(m=s["m"], L=s["L"], zs=s["zs"], z=s["z"], em=s["em"], lgL=s["lgL"])
            row.append(ss)
        gS[k] = row
    T = NM.TR
    return dict(R=NM.R, wbin=NM.wbin, TR=(T.x0, T.y0, T.c, T.nx, T.ny, T.Z), gS=(NM.gS.c, gS), gR=(NM.gR.c, gR))


def noise_par_start(NM, tasks, mode, label):
    """Hand the receivers to the worker processes and return at once (they run while Rhino works on other
    analyses); noise_par_collect waits for them. Without workers nothing starts here and collect computes in Rhino."""
    import pickle, subprocess
    import time as _tm
    h = dict(NM=NM, tasks=tasks, mode=mode, label=label, procs=[], files=[], t0=_tm.time(), err=None)
    n = min(_cores() if PAR_PROCS <= 0 else int(PAR_PROCS), len(tasks) // 8)
    py = noise_worker_python() if n >= 2 else None
    if py is None:
        if n >= 2:
            h["err"] = "computed on one core: {}".format(_NOISE_PY.get("why", ""))
        return h
    try:
        kf, d = _kernel_file()
        tag = "%d_%d_%s" % (os.getpid(), int(h["t0"] * 1000) % 100000000, mode)
        mf = os.path.join(d, "model_%s.bin" % tag)
        md = getattr(NM, "_par_data", None)
        if md is None:
            md = NM._par_data = pickle.dumps(_noise_model_data(NM), protocol=4)
        with open(mf, "wb") as fh:
            fh.write(md)
        h["files"].append(mf)
        parts = [list(range(w, len(tasks), n)) for w in range(n)]      # interleaved: every worker gets a fair share
        for w, idx in enumerate(parts):
            tf, of = os.path.join(d, "tasks_%s_%d.bin" % (tag, w)), os.path.join(d, "out_%s_%d.bin" % (tag, w))
            with open(tf, "wb") as fh:
                pickle.dump((mode, [tasks[i] for i in idx]), fh, protocol=4)
            h["files"] += [tf, of]
            h["procs"].append((subprocess.Popen([py, "-I", kf, mf, tf, of], stdout=subprocess.DEVNULL,
                                                stderr=subprocess.PIPE, **_popen_kw()), of, idx))
        h["n"] = n
    except Exception as ex:
        _noise_par_stop(h)
        h["procs"], h["err"] = [], "worker processes not used ({}: {}); computed on one core".format(type(ex).__name__, ex)
    return h


def _noise_par_stop(h):
    for pr, _, _ in h["procs"]:
        try:
            if pr.poll() is None:
                pr.kill()
        except Exception:
            pass
    for f_ in h["files"]:
        try:
            os.remove(f_)
        except Exception:
            pass


def noise_par_collect(h):
    import pickle
    import time as _tm
    NM, tasks, label = h["NM"], h["tasks"], h["label"]
    fn = NM.column_multi if h["mode"] == "multi" else NM.column
    if not h["procs"]:
        if h["err"]:
            LOG.append("Sound {}: {}.".format(label, h["err"]))
        return [fn(*t) for t in tasks]
    try:
        # Rhino computes the first receiver of every worker itself: the check
        check = dict((idx[0], fn(*tasks[idx[0]])) for _, _, idx in h["procs"] if idx)
        out = [None] * len(tasks)
        for pr, of, idx in h["procs"]:
            err = pr.communicate()[1]
            if pr.returncode != 0:
                last = err.decode("utf-8", "replace").strip().splitlines()[-1:] if err else []
                raise RuntimeError("a worker stopped" + (": " + last[0] if last else ""))
            with open(of, "rb") as fh:
                res = pickle.load(fh)
            if len(res) != len(idx):
                raise RuntimeError("a worker returned {} of {} receivers".format(len(res), len(idx)))
            for i, r in zip(idx, res):
                out[i] = r
        bad = [i for i, r in check.items() if r != out[i]]
        if bad:
            raise RuntimeError("{} checked receiver(s) differ from Rhino's own result".format(len(bad)))
        LOG.append("Sound {}: {} receivers on {} worker processes (checked against Rhino).".format(
            label, len(tasks), h["n"]))
        return out
    except Exception as ex:
        LOG.append("Sound {}: worker processes not used ({}: {}); computed on one core.".format(
            label, type(ex).__name__, ex))
        _noise_par_stop(h)
        return [fn(*t) for t in tasks]
    finally:
        _noise_par_stop(h)


