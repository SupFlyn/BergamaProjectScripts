# bergama_water_balance_v2_4.py (v2.4, visual-first sheet 25 Oct; compute and JSON unchanged) · Thread 2 of the 22 Oct batch: water balance (demand, collection, storage, cost cut-off)
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Every press RECOMPUTES the balance from the current lands (Aras 24 Oct 08:13):
#   1. lands: optional GH inputs > objects in the open Rhino file > built-in defaults (see LANDS below);
#   2. 34 water years 1991-2025, daily: FAO-56 soil water balance on the farms, river + site catch into storage,
#      strip first, nothing stored over 365 days, cost ladder; the cost cut-off sets the size and the % covered;
#   3. writes Downloads/Bergama/output/Bergama_water_balance_analysis/Bergama_water_balance_A3.pdf (one all-vector A3 sheet) and
#      water_balance_results.json there, which other scripts read instead of fixed numbers (read_results() below).
# Built-in inputs (weather, river, Kc) come from research/water_balance/scripts/water_balance_v2.py, 24 Oct 2026;
# sources and methods: research/water_balance/NOTES.md.
#
# Lands read from the open Rhino file (zone base layers, option A only since v2.3):
#   Option_A::INT_ZONE_WS  -> terrace_m2 (retention terraces)     Option_A::INT_ZONE_GR -> walk_m2 (walk tops)
#   Option_A::INT_WATER_strip -> strip_m2 (the low-flow strip)
# Any closed curve with the user text  water_balance = <key>  adds its area to that key instead (keys: roof, walk,
# riverside_walk, terrace, strip, pond_land, cropland, orchard). So a new storage plot or roof only needs a closed
# curve with that user text. GH inputs with these names override both: cropland_ha, orchard_ha, pond_land_ha,
# roof_m2, walk_m2, riverside_walk_m2, terrace_m2, strip_m2, cropland_crops (text "cotton,tomato"), option.
import os, time, json, zlib, base64, math, datetime as dt
from collections import deque, defaultdict

VERSION = "v2.4"
# v2.3 (Aras 25 Oct 16:43: "the selection of A should be remember in the whole project so all scripts should drop B alternatives"): option A only; the option input is ignored.
# v2.2 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_water_balance_log.txt (next to cached/ and output/), overwritten by each press.
LOG_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "logs")   # Aras 25 Oct 09:34-09:35: every script's log here


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, "bergama_water_balance_log.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text

# v2 24 Oct: all files under Downloads/Bergama/ (Aras rule). v2.1 (Thread 5): riverside_walk_m2 read live from the
# masterplan (v11) results when no GH input or Rhino curve gives it
OUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "Bergama_water_balance_analysis")
OLD_OUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis")   # read fallback only
OUT_PDF = "Bergama_water_balance_A3.pdf"
OUT_JSON = "water_balance_results.json"
MP_FILE = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "bergama_masterplan", "masterplan_results.json")

# ------------------------------------------------------------------ lands: defaults (used when nothing else is given)
LANDS = dict(
    cropland_ha=34.9,          # around2.pdf farm extent, ESA WorldCover 2021 cropland (satellite)
    orchard_ha=1.34,           # same, orchards inferred within 35 m of survey olive/fruit symbols; grown as olive
    pond_land_ha=2.81,         # vacant flat land in the around2.pdf land-use table, for open ponds
    roof_m2=20110.0,           # survey roofs in the four study areas (rain_river s.2, lower bound)
    walk_m2=2682.0,            # zone base v5 GR 1-3 walk tops, grated paving
    riverside_walk_m2=17694.0, # DESIGN placeholder: 2 x 2,949 m x 3 m; v2.1 reads the masterplan's walks instead (MP_FILE)
    terrace_m2=3490.0,         # zone base v5 WS 1 retention terraces (overflow only)
    strip_m2=4.0 * 2949.0,     # rain_river s.4 reference strip 4 m x 2,949 m (DESIGN)
    cropland_crops="cotton,maize,tomato",  # run as each; design = larger size. Bergama's main irrigated crops, TÜİK 2025
                                           # (library/research/crops_2026-10-24 §1.25); fields' own crops not mapped
)
ZONE_LAYERS = {"INT_ZONE_WS": "terrace_m2", "INT_ZONE_GR": "walk_m2", "INT_WATER_strip": "strip_m2"}
TAG_KEYS = {"roof": "roof_m2", "walk": "walk_m2", "riverside_walk": "riverside_walk_m2", "terrace": "terrace_m2",
            "strip": "strip_m2", "pond_land": "pond_land_ha", "cropland": "cropland_ha", "orchard": "orchard_ha"}

# ------------------------------------------------------------------ method constants (sources: NOTES.md)
TAW_M = 0.13                 # FAO-56 Table 19, nearest row to the SoilGrids clay loam, low end (safe side)
CROP_SOIL = dict(olive=dict(Zr=1.2, p=0.65), cotton=dict(Zr=1.0, p=0.65), maize=dict(Zr=1.0, p=0.55),
                 tomato=dict(Zr=0.7, p=0.40))      # FAO-56 Table 22, lower end of root depth
FALLOW_KC = 0.30             # FLAG: bare soil between annual crops
INFIL_MAX = 50.0             # FLAG: mm/day that can soak in
DRIP_EFF = 0.90              # FAO Training Manual 4 ch.3
STRIP_SEEP = 5.0             # mm/day, clay-sealed bed (rain_river s.4)
EVAP_OW = 1.05               # FAO-56 open water
SEEP_LINED = 0.5             # FLAG: mm/day through a pond liner
POND_DEPTH, POND_USE = 3.0, 0.7   # DESIGN / FLAG
CRATE_DEPTH, CRATE_VOID = 1.5, 0.95  # FLAG / Wavin
INTAKE_DAYS = 60.0           # intake fills at most V/60 per day
MAX_AGE = 365                # Aras 07:59: no water sits in storage more than a year; older water goes to the strip/river
SURF = dict(roof=(0.90, 1.0, 1.00), walk=(0.75, 1.5, 0.90), terrace=(0.04, 10.0, 1.00))  # C, Ia mm, capture (FLAG)
STRIP_TODAY = 26675.0        # today's storage, the strip only (rain_river A6, sealed worst case)
# costs: Ross & Hasnain 2018 (MAR, levelised USD); UK EA 2015 / Royal Haskoning 2012 SuDS capital GBP x 1.25 (FLAG)
RECHARGE_USD = (0.19, 0.45)
ALTERNATIVE_USD = (0.74, 1.89)  # recycled water through aquifer recharge
GBP, RATE = 1.25, 0.05
BUILT = [("pond", "Ponds, vacant land", (15, 55), 25), ("crates", "Crates under walks", (200, 350), 30),
         ("cistern", "Cisterns, plazas", (449, 590), 50)]
CASES = (("strict", RECHARGE_USD[1], ALTERNATIVE_USD[0]), ("central", sum(RECHARGE_USD) / 2, sum(ALTERNATIVE_USD) / 2),
         ("loose", RECHARGE_USD[0], ALTERNATIVE_USD[1]))
STEP = 5000.0                # m3, storage sweep step
ET0_NORMAL = 1369.1          # mm/yr, FAO-56 Penman-Monteith on WMO 17742 normals (v1 table B1)

#@include data/INPUT_DATA.py

# ------------------------------------------------------------------ lands: GH inputs > Rhino objects > defaults
def _num(v):
    try:
        return float(v) if v is not None and str(v).strip() != "" else None
    except (TypeError, ValueError):
        return None

def rhino_lands(option):
    """Areas from the open Rhino file (m2, or ha for land keys); {} when not in Rhino or nothing is found."""
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
    except Exception:
        return {}
    if doc is None:
        return {}
    s2 = Rhino.RhinoMath.UnitScale(doc.ModelUnitSystem, Rhino.UnitSystem.Meters) ** 2
    out = {}
    for o in doc.Objects.GetObjectList(Rhino.DocObjects.ObjectType.Curve):
        g = o.Geometry
        if not g.IsClosed:
            continue
        tag = (o.Attributes.GetUserString("water_balance") or "").strip().lower()
        if tag:
            key = TAG_KEYS.get(tag)
        else:
            path = doc.Layers[o.Attributes.LayerIndex].FullPath
            key = ZONE_LAYERS.get(path.split("::")[-1]) if path.startswith("Option_" + option + "::") else None
        if not key:
            continue
        amp = Rhino.Geometry.AreaMassProperties.Compute(g)
        if amp is None:
            continue
        a = amp.Area * s2
        out[key] = out.get(key, 0.0) + (a / 1e4 if key.endswith("_ha") else a)
    return out

def masterplan_lands(option):
    """v2.1: {riverside_walk_m2: ...} and its source from bergama_masterplan v11's masterplan_results.json."""
    try:
        with open(MP_FILE, "r", encoding="utf-8") as f:
            v = json.load(f)["options"][option]["riverside_walk_m2"]
        return {"riverside_walk_m2": float(v)}, "masterplan v11 results of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(MP_FILE)))
    except Exception:
        return {}, None

def get_lands(g):
    option = "A"                                         # v2.3: option A only, project-wide (Aras 25 Oct 16:43)
    rh = rhino_lands(option)
    mp, mp_src = masterplan_lands(option)
    L, src = {}, {}
    for k, v in LANDS.items():
        gv = g.get(k)
        if k == "cropland_crops":
            L[k] = str(gv) if gv else v; src[k] = "gh" if gv else "default"
        elif _num(gv) is not None:
            L[k] = _num(gv); src[k] = "gh"
        elif k in rh:
            L[k] = rh[k]; src[k] = "rhino option " + option
        elif k in mp:
            L[k] = mp[k]; src[k] = mp_src + " option " + option
        else:
            L[k] = v; src[k] = "default"
    L["option"] = option
    return L, src

# ------------------------------------------------------------------ built-in daily inputs
def load_inputs():
    d = json.loads(zlib.decompress(base64.b64decode("".join(INPUT_DATA))).decode("utf-8"))
    d0 = dt.date.fromisoformat(d["start"])
    d["days"] = [d0 + dt.timedelta(i) for i in range(d["n"])]
    d["P"] = [x / 100.0 for x in d["P"]]; d["E"] = [x / 100.0 for x in d["E"]]
    d["KC"] = {c: [x / 1000.0 for x in k] for c, k in d["KC"].items()}
    return d

def wy(d): return d.year + 1 if d.month >= 10 else d.year

# ------------------------------------------------------------------ farms: FAO-56 ch.8 daily soil water balance
def soil_irrigation(crop, I, use_rain=True):
    """Daily net irrigation (mm): Dr = Dr - Pe + Kc ET0; refill to field capacity when Dr > RAW (in season)."""
    s = CROP_SOIL[crop]; TAW = 1000 * TAW_M * s["Zr"]; RAW = s["p"] * TAW
    kc, ever = I["KC"][crop], I["EVERGREEN"][crop]
    Dr, out = 0.0, []
    for d, P, E in zip(I["days"], I["P"], I["E"]):
        k = kc[min(d.timetuple().tm_yday - 1, 364)]
        Pe = min(P if (use_rain and P >= 0.2 * E) else 0.0, INFIL_MAX)
        Dr = max(0.0, Dr - Pe) + (k if k > 0 else FALLOW_KC) * E
        x = 0.0
        if (ever or k > 0) and Dr > RAW:
            x = Dr; Dr = 0.0
        elif Dr > TAW:
            Dr = TAW
        out.append(x)
    return out

def ranked(vals):
    s = sorted(vals); n = len(s)
    q = lambda f: s[int(round(f * (n - 1)))]
    return dict(mean=sum(s) / n, median=s[n // 2], wet5=q(0.2), dry5=q(0.8), dry10=q(0.9), min=s[0], max=s[-1])

# ------------------------------------------------------------------ storage: daily, first in first out
def strip_reserve(strip, days):
    rem = [0.0] * len(days); acc = 0.0
    for i in range(len(days) - 1, -1, -1):
        d = days[i]
        acc = 0.0 if (d.month == 10 and d.day == 31) or d.month in (11, 12, 1, 2, 3, 4) else acc
        acc += strip[i]; rem[i] = acc if 5 <= d.month <= 10 else 0.0
    best = defaultdict(float)
    for d, r in zip(days, rem): best[(d.month, d.day)] = max(best[(d.month, d.day)], r)
    return [best[(d.month, d.day)] for d in days]

def run_storage(V, A, demand, strip, inflow, et0, days, reserve, max_age=MAX_AGE):
    Q = deque(); S = 0.0; flushed = 0.0; oldest = 0
    per = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    i = 0
    def take(n, keep=0.0):
        nonlocal S, oldest
        n = min(n, max(0.0, S - keep)); got = 0.0
        while n > 1e-9 and Q:
            t = min(n, Q[0][1]); oldest = max(oldest, i - Q[0][0])
            Q[0][1] -= t; n -= t; got += t
            if Q[0][1] <= 1e-9: Q.popleft()
        S -= got
        return got
    for i, d in enumerate(days):
        while Q and i - Q[0][0] >= max_age:
            flushed += Q[0][1]; S -= Q[0][1]; Q.popleft()
        x = min(V - S, inflow[i])
        if x > 0: Q.append([i, x]); S += x
        if A and S > 0:
            loss = min(S, A * min(1.0, S / max(V, 1.0)) * (et0[i] * EVAP_OW + SEEP_LINED) / 1000)
            S -= loss
            while loss > 1e-9 and Q:
                t = min(loss, Q[0][1]); Q[0][1] -= t; loss -= t
                if Q[0][1] <= 1e-9: Q.popleft()
        gs = take(strip[i]); gf = take(demand[i], reserve[i])
        r = per[wy(d)]; r[0] += demand[i]; r[1] += gf; r[2] += strip[i]; r[3] += gs
    return per, flushed, oldest

def crf(r, n): return r * (1 + r) ** n / ((1 + r) ** n - 1)

def compute(L):
    I = load_inputs(); days, P, E, R = I["days"], I["P"], I["E"], I["R"]
    nY = len(set(wy(d) for d in days))
    crops = ["olive"] + [c.strip().lower() for c in L["cropland_crops"].split(",") if c.strip().lower() in CROP_SOIL and c.strip().lower() != "olive"]
    crops = list(dict.fromkeys(crops))
    if len(crops) == 1: crops.append("cotton")
    irr = {c: soil_irrigation(c, I) for c in set(crops) | set(CROP_SOIL)}
    res = dict(script="bergama_water_balance_v2_4.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
               lands={k: (round(v, 3) if isinstance(v, float) else v) for k, v in L.items()})
    # net irrigation per crop (mm a water year) and the rain the fields hold
    res["net_irrigation_mm"] = {}; res["rain_credit_pct"] = {}
    for c in CROP_SOIL:
        by = defaultdict(float)
        for d, x in zip(days, irr[c]): by[wy(d)] += x
        res["net_irrigation_mm"][c] = {k: round(v, 1) for k, v in ranked(list(by.values())).items()}
        dry = sum(soil_irrigation(c, I, use_rain=False))
        res["rain_credit_pct"][c] = round(100.0 * (1 - sum(irr[c]) / dry), 1) if dry else 0.0
    # supplies and the strip
    sa = [("roof", L["roof_m2"]), ("walk", L["walk_m2"] + L["riverside_walk_m2"]), ("terrace", L["terrace_m2"])]
    site = [sum(a * SURF[s][2] * SURF[s][0] * max(0.0, p - SURF[s][1]) / 1000 for s, a in sa) for p in P]
    strip = [(L["strip_m2"] * (e * EVAP_OW + STRIP_SEEP) / 1000) if 5 <= d.month <= 10 else 0.0 for d, e in zip(days, E)]
    RES = strip_reserve(strip, days)
    mon = lambda series: [round(sum(x for d, x in zip(days, series) if d.month == m + 1) / nY) for m in range(12)]
    res["river_month_m3"] = mon(R); res["strip_month_m3"] = mon(strip); res["site_month_m3"] = mon(site)
    res["strip_m3_per_year"] = round(sum(strip) / nY)
    steps = [("Roofs", "roof", L["roof_m2"]), ("Walk tops", "walk", L["walk_m2"]),
             ("Riverside walks", "walk", L["riverside_walk_m2"]), ("Retention terraces", "terrace", L["terrace_m2"])]
    res["site_catch_steps"] = [dict(name=n, m2=round(a), m3_per_year=round(sum(a * SURF[s][2] * SURF[s][0] * max(0.0, p - SURF[s][1]) / 1000 for p in P) / nY))
                               for n, s, a in steps]
    res["site_catch_m3_per_year"] = round(sum(site) / nY)
    # farm demand per mix (m3 at the intake, drip)
    res["farm_demand_m3"] = {}; res["farm_demand_month_m3"] = {}; dem = {}
    for c in crops[1:]:
        mix = "orchard olive + cropland " + c
        dem[mix] = [(L["orchard_ha"] * irr["olive"][i] + L["cropland_ha"] * irr[c][i]) / DRIP_EFF * 10 for i in range(len(days))]
        by = defaultdict(float)
        for d, x in zip(days, dem[mix]): by[wy(d)] += x
        rk = ranked(list(by.values()))
        y5 = min(by, key=lambda y: abs(by[y] - rk["dry5"]))
        res["farm_demand_m3"][mix] = dict({k: round(v) for k, v in rk.items()}, dry5_year=y5)
        res["farm_demand_month_m3"][mix] = dict(mean=mon(dem[mix]),
                                                dry5=[round(sum(x for d, x in zip(days, dem[mix]) if wy(d) == y5 and d.month == m + 1)) for m in range(12)])
    def stats(V, mix, Vopen=0.0):
        inflow = [min(V / INTAKE_DAYS, r) + s for r, s in zip(R, site)]
        per, fl, old = run_storage(V, Vopen / POND_DEPTH, dem[mix], strip, inflow, E, days, RES)
        per.pop(min(per))                                   # first water year = spin-up (storage starts empty)
        cov = sorted(per[y][1] / per[y][0] for y in per if per[y][0] > 0)
        n = len(cov)
        return dict(median=cov[n // 2], dry5=cov[int(round(0.2 * (n - 1)))], dry10=cov[int(round(0.1 * (n - 1)))],
                    delivered=sum(per[y][1] for y in per) / len(per), released=fl / len(per), oldest=old,
                    strip_min=min(per[y][3] / per[y][2] for y in per if per[y][2] > 0) if any(per[y][2] for y in per) else 1.0)
    pct = lambda x: round(100.0 * x, 1)
    # closed storage swept in steps until one more step is not worth even the cheapest recharge (loose case)
    res["curve_closed"] = {}; res["cutoff"] = {}; res["need_for_target_1in5_dry_m3"] = {}; res["today_strip_storage"] = {}
    for mix in dem:
        rows = []; V = 0.0; low = 0; started = False; lim = 6.0 * res["farm_demand_m3"][mix]["max"] + 1e5
        while V <= lim:
            st = stats(V, mix); rows.append((V, st))
            if len(rows) > 1:
                md = (st["delivered"] - rows[-2][1]["delivered"]) / STEP
                started = started or st["delivered"] > 0
                low = low + 1 if started and md < CASES[2][1] / CASES[2][2] else 0
                if low >= 3 or (started and st["dry5"] >= 0.9999 and low >= 1): break
            V += STEP
        res["curve_closed"][mix] = [[int(v), pct(s["median"]), pct(s["dry5"]), pct(s["dry10"]), round(s["delivered"]), round(s["released"]), s["oldest"]] for v, s in rows]
        cut = {}
        for case, c, alt in CASES:
            ok = [rows[j][0] for j in range(1, len(rows)) if (rows[j][1]["delivered"] - rows[j - 1][1]["delivered"]) / STEP >= c / alt]
            Vc = max(ok) if ok else 0.0
            s = dict(rows)[Vc]
            cut[case] = dict(storage_m3=int(Vc), recharge_usd_m3=round(c, 3), alternative_usd_m3=round(alt, 3),
                             covered_pct_1in5_dry=pct(s["dry5"]), covered_pct_median=pct(s["median"]), covered_pct_1in10_dry=pct(s["dry10"]),
                             delivered_m3_per_year=round(s["delivered"]), released_365d_m3_per_year=round(s["released"]),
                             oldest_days=s["oldest"], strip_served_pct_worst_year=pct(s["strip_min"]))
        res["cutoff"][mix] = cut
        nt = {}
        for t in (25, 50, 75, 100):
            hit = None
            for j in range(1, len(rows)):
                a, b = rows[j - 1], rows[j]
                if b[1]["dry5"] * 100 >= t - 1e-6:
                    f = (t / 100.0 - a[1]["dry5"]) / max(b[1]["dry5"] - a[1]["dry5"], 1e-9)
                    hit = int(round((a[0] + f * STEP) / 1000.0) * 1000); break
            nt[str(t)] = hit
        res["need_for_target_1in5_dry_m3"][mix] = nt
        s = stats(STRIP_TODAY, mix)
        res["today_strip_storage"][mix] = dict(storage_m3=STRIP_TODAY, covered_pct_1in5_dry=pct(s["dry5"]), strip_served_pct_worst_year=pct(s["strip_min"]))
    design = max(dem, key=lambda m: res["cutoff"][m]["central"]["storage_m3"])
    allc = [res["cutoff"][m][k] for m in dem for k in res["cutoff"][m]]
    dc = res["cutoff"][design]["central"]
    res["design"] = dict(mix=design, case="central", storage_m3=dc["storage_m3"], covered_pct_1in5_dry=dc["covered_pct_1in5_dry"],
                         covered_pct_median=dc["covered_pct_median"],
                         central_range_m3=[min(res["cutoff"][m]["central"]["storage_m3"] for m in dem), dc["storage_m3"]],
                         central_range_pct_1in5_dry=[min(res["cutoff"][m]["central"]["covered_pct_1in5_dry"] for m in dem), max(res["cutoff"][m]["central"]["covered_pct_1in5_dry"] for m in dem)],
                         full_range_m3=[min(x["storage_m3"] for x in allc), max(x["storage_m3"] for x in allc)],
                         full_range_pct_1in5_dry=[min(x["covered_pct_1in5_dry"] for x in allc), max(x["covered_pct_1in5_dry"] for x in allc)],
                         note="aquifer recharge sized by cost; valid only if borehole tests accept recharge (arsenic, DSI rights)")
    # open ponds for comparison (design mix) and the built-storage ladder without recharge (US$ per m3 delivered)
    vmax = res["curve_closed"][design][-1][0]
    res["curve_open"] = [[int(v), pct(s["median"]), pct(s["dry5"])] for v in [vmax * k / 8.0 for k in range(9)] for s in [stats(v, design, v)]]
    caps = dict(pond=L["pond_land_ha"] * 1e4 * POND_DEPTH * POND_USE, crates=(L["walk_m2"] + L["riverside_walk_m2"]) * CRATE_DEPTH * CRATE_VOID,
                cistern=150000.0)
    lad = []; Vc = Vo = 0.0; prev = stats(0.0, design)["delivered"]
    for key, name, gbp, life in BUILT:
        cap = caps[key]
        if cap <= 0: continue
        if key == "pond": Vo += cap
        else: Vc += cap
        st = stats(Vc + Vo, design, Vo)
        dd = max(st["delivered"] - prev, 1e-6); prev = st["delivered"]
        f = crf(RATE, life) * GBP * cap / dd
        lad.append(dict(key=key, step=name, from_m3=round(Vc + Vo - cap), to_m3=round(Vc + Vo), added_delivery_m3_per_year=round(dd),
                        usd_per_m3_low=round(gbp[0] * f, 2), usd_per_m3_high=round(gbp[1] * f, 2), covered_pct_1in5_dry=pct(st["dry5"])))
    res["ladder_no_recharge"] = lad
    res["recharge_usd_m3"] = list(RECHARGE_USD); res["alternative_usd_m3"] = list(ALTERNATIVE_USD)
    return res

def read_results(path=None):
    """For other scripts: the latest results dict (design storage and % under res['design']), or None."""
    p = path or os.path.join(OUT_DIR, OUT_JSON)
    if not path and not os.path.isfile(p): p = os.path.join(OLD_OUT_DIR, OUT_JSON)
    try:
        with open(p, encoding="utf-8") as f: return json.load(f)
    except Exception:
        return None

# ------------------------------------------------------------------ colours (palette v1.4 core roles)
C = dict(ground="E2E0D4", paper="EFEDE6", faint="D8D5CC", structure="B0AC9C", ink2="847E75", ink="4A3F35",
         green_deep="495338", green_mid="727A4E", green_light="8C9969", water_deep="5D7F8D", water="91ADB4",
         water_light="C1D3DB", accent="8B3A3F", accent_deep="633131", white="FFFFFF")

#@include ../common/rgb.py

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]

#@include ../common/text_w.py

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"


class Page:
    def __init__(self, w, h):
        self.w, self.h, self.ops = w, h, []
    def _c(self, h, stroke=False):
        r, g, b = rgb(h); return "%.3f %.3f %.3f %s" % (r, g, b, "RG" if stroke else "rg")
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)
    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None):
        k = 72 / 25.4; o = ["q"]
        if fill: o.append(self._c(fill))
        if stroke: o.append(self._c(stroke, True)); o.append("%.3f w 1 J 1 j" % (lw * k))
        if dash: o.append("[%.2f %.2f] 0 d" % (dash[0] * k, dash[1] * k))
        o.append("%.2f %.2f m" % (P[0][0] * k, P[0][1] * k))
        o += ["%.2f %.2f l" % (x * k, y * k) for x, y in P[1:]]
        if closed: o.append("h")
        o.append("B" if fill and stroke else ("f" if fill else "S")); o.append("Q")
        self.ops.append(" ".join(o))
    def line(self, P, col, lw=0.25, dash=None): self.poly(P, None, col, lw, False, dash)
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L"):
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        k = 72 / 25.4
        b = b"".join(bytes([_ENC_EXTRA[ch]]) if ch in _ENC_EXTRA else ch.encode("cp1252", "replace") for ch in s)   # 25 Oct: ı İ ğ Ğ ş Ş spelt right
        b = b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
        self.ops.append("BT /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET" % ("F2" if bold else "F1", size, self._c(col), x * k, y * k, b.decode("latin-1")))
    def para(self, s, x, y, w, size, col="4A3F35", bold=False, lead=1.3):
        line, yy = "", y
        for word in s.split(" "):
            t = (line + " " + word).strip()
            if text_w(t, size, bold) > w and line:
                self.text(line, x, yy, size, col, bold); yy -= size * 0.3528 * lead; line = word
            else: line = t
        if line: self.text(line, x, yy, size, col, bold); yy -= size * 0.3528 * lead
        return yy

def write_pdf(pg, path):
    k = 72 / 25.4
    content = zlib.compress("\n".join(pg.ops).encode("latin-1"))
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.2f %.2f] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>" % (pg.w * k, pg.h * k),
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding << /Type /Encoding /BaseEncoding /WinAnsiEncoding %s >> >>" % _DIFF,
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding << /Type /Encoding /BaseEncoding /WinAnsiEncoding %s >> >>" % _DIFF]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
    for i, o in enumerate(objs):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (i + 1, o)).encode("latin-1")
    offs.append(len(out))
    out += ("6 0 obj\n<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(content)).encode("latin-1") + content + b"\nendstream\nendobj\n"
    x = len(out)
    out += ("xref\n0 7\n0000000000 65535 f \n" + "".join("%010d 00000 n \n" % o for o in offs) +
            "trailer\n<< /Size 7 /Root 1 0 R /Info << /Title (Bergama water balance) >> >>\nstartxref\n%d\n%%%%EOF\n" % x).encode("latin-1")
    with open(path, "wb") as f: f.write(out)

# ------------------------------------------------------------------ helpers on the live results
MON = "J F M A M J J A S O N D".split()

def fmt(v):
    return "{:,.0f}".format(v)

def k_(v):
    return "%.1fk" % (v / 1000.0) if v >= 1000 else fmt(v)

def nice(v):
    """the next round number above v (1, 2, 2.5, 5 x 10^n)"""
    if v <= 0: return 1.0
    e = 10 ** math.floor(math.log10(v))
    return next(m * e for m in (1, 2, 2.5, 5, 10) if m * e >= v)

def panel_title(pg, x, y, n, title, sub=None):
    pg.text(n, x, y, 13, C["accent"], True)
    pg.text(title, x + 8, y, 13, C["ink"], True)
    if sub: pg.text(sub, x + 8, y - 5.2, 7.5, C["ink2"])

# ------------------------------------------------------------------ v2.4 visual first (SCRIPT_STANDARD 5b): [n] marks, pictograms, tiles
SOURCES = dict(    # every source and method sentence of the v2.3 sheet, now printed once in the footer key
    esa="ESA WorldCover 2021: farms = analysis area of the land-use map, unless changed",
    mgm="MGM/WMO 17742 normals 1991-2020",
    era5="Open-Meteo ERA5 daily 1991-2025 (scaled to the station)",
    dsi="DSI gauges D04A053, D04A063 2016-2021, area-scaled",
    fao56="FAO-56 (Allen et al. 1998): daily soil water balance, Penman-Monteith ET0",
    fao_t="FAO-56 Tables 19 and 22",
    fao_tm4="FAO Training Manual 4 (drip)",
    rg="RG 30802 minimum flow: river counted above the legal minimum, worst case",
    dwa="DWA-A 117",
    abu="Abu Hammad et al. 2004: runoff 20 % without terraces, 4 % terraced",
    ross="Ross & Hasnain 2018",
    suds="UK EA 2015 and Royal Haskoning 2012 SuDS costs (GBP x 1.25, FLAG)")
SRC_KEY = []

def cite(*keys):
    """v2.4: "[n]" (or "[n,m]") for sources in SOURCES; the numbered key is printed in the footer."""
    for k in keys:
        if k not in SRC_KEY: SRC_KEY.append(k)
    return "[" + ",".join(str(SRC_KEY.index(k) + 1) for k in keys) + "]"

def circle(pg, cx, cy, r, fill=None, stroke=None, lw=0.2):
    pg.poly([(cx + r * math.cos(a * math.pi / 10), cy + r * math.sin(a * math.pi / 10)) for a in range(20)], fill, stroke, lw, True)

def icon(pg, kind, x, y, sz):
    """v2.4: a pictogram in the square (x, y - sz)-(x + sz, y), on a 10 x 10 grid. Graphic only."""
    u = sz / 10.0; lw = 0.06 * sz
    P = lambda pts: [(x + a * u, y - sz + b * u) for a, b in pts]
    if kind == "field":
        pg.poly(P([(0, 1), (7, 1), (10, 6), (3, 6)]), fill=C["green_light"], closed=True)
        for b in (2.2, 3.5, 4.8):
            f = (b - 1) / 5.0; pg.line(P([(0.6 + 3 * f, b), (6.6 + 3 * f, b)]), C["green_deep"], lw * 0.6)
    elif kind == "olive":
        pg.rect(x + 4.5 * u, y - sz + 0.6 * u, u, 4 * u, fill=C["ink2"])
        circle(pg, x + 5 * u, y - sz + 6.4 * u, 3.4 * u, fill=C["green_mid"])
        for a, b in ((3.8, 7.0), (6.0, 5.6), (5.4, 8.0)): circle(pg, x + a * u, y - sz + b * u, 0.5 * u, fill=C["ink"])
    elif kind == "sun":
        for k in range(8):
            a = k * math.pi / 4
            pg.line(P([(5 + 3.0 * math.cos(a), 5 + 3.0 * math.sin(a)), (5 + 4.6 * math.cos(a), 5 + 4.6 * math.sin(a))]), C["accent"], lw)
        circle(pg, x + 5 * u, y - sz + 5 * u, 2.3 * u, fill=C["accent"])
    elif kind == "strip":
        pg.rect(x, y - sz + 3.4 * u, sz, 3.2 * u, fill=C["water"])
        for a in (1.5, 4.5, 7.5): pg.line(P([(a, 6.6), (a + 0.3, 9.2)]), C["green_mid"], lw)
    elif kind == "drop":
        pg.poly(P([(5 - 2.6, 4.6), (5, 9.6), (5 + 2.6, 4.6)]), fill=C["water_deep"], closed=True)
        circle(pg, x + 5 * u, y - sz + 3.6 * u, 3.0 * u, fill=C["water_deep"])
    elif kind == "clock":
        circle(pg, x + 5 * u, y - sz + 5 * u, 4.2 * u, fill=C["white"], stroke=C["ink"], lw=lw)
        pg.line(P([(5, 8.0), (5, 5), (7.2, 5)]), C["ink"], lw)
    elif kind == "cube":
        pg.poly(P([(5, 9.8), (9.2, 7.6), (5, 5.4), (0.8, 7.6)]), fill=C["faint"], closed=True)
        pg.poly(P([(0.8, 7.6), (5, 5.4), (5, 0.4), (0.8, 2.6)]), fill=C["structure"], closed=True)
        pg.poly(P([(5, 5.4), (9.2, 7.6), (9.2, 2.6), (5, 0.4)]), fill=C["ink2"], closed=True)
    elif kind == "terrace":
        pg.poly(P([(0, 0.6), (10, 0.6), (10, 3.2), (6.6, 3.2), (6.6, 5.8), (3.3, 5.8), (3.3, 8.4), (0, 8.4)]), fill=C["green_mid"], closed=True)

def tile(pg, kind, x, y, w, h, head, big, foot):
    """v2.4: pictogram tile (water board v1.6 method): icon, keyword heading, ONE big figure, a short foot with [n]."""
    pg.rect(x, y - h, w, h, fill=C["paper"], stroke=C["structure"], lw=0.2)
    sz = min(h - 4.0, 9.0); icon(pg, kind, x + 1.8, y - (h - sz) / 2.0, sz)
    lx = x + 3.6 + sz; tw = x + w - 1.5 - lx; fs = 12.0
    while fs > 7 and text_w(big, fs, True) > tw: fs -= 0.5
    pg.text(head, lx, y - 4.4, 6.5, C["ink2"], True)
    pg.text(big, lx, y - 4.4 - 1.2 - fs * 0.3528, fs, C["ink"], True)
    pg.text(foot, lx, y - h + 2.2, 6, C["ink2"])

def inline(pg, x, y, parts):
    """v2.4: a keyword row: parts = [(text, size, colour, bold)] set one after another; returns the end x."""
    for s, size, col, bold in parts:
        pg.text(s, x, y, size, col, bold); x += text_w(s, size, bold)
    return x

# ------------------------------------------------------------------ panel 1: when water comes, when the farms need it
def panel_timing(pg, R, x, y, w, h):
    L = R["lands"]; mix = R["design"]["mix"]
    panel_title(pg, x, y + h, "1", "When water comes, when the farms need it",
                "need m³/month · %.1f ha · drip %s · net of rain held %s"
                % (L["cropland_ha"] + L["orchard_ha"], cite("fao_tm4"), cite("fao56")))
    cx, cy, cw, ch = x + 14, y + 30, w - 18, h - 50
    dem_n = R["farm_demand_month_m3"][mix]["mean"]; dem_d = R["farm_demand_month_m3"][mix]["dry5"]
    vmax = nice(max(dem_n + dem_d) * 1.05)
    for j in range(6):
        t = vmax * j / 5.0; yy = cy + ch * t / vmax
        pg.line([(cx, yy), (cx + cw, yy)], C["faint"], 0.15)
        pg.text(fmt(t), cx - 1.5, yy - 1, 6.5, C["ink2"], align="R")
    bw = cw / 12.0
    for m in range(12):
        x0 = cx + m * bw
        pg.rect(x0 + bw * 0.14, cy, bw * 0.34, ch * dem_n[m] / vmax, fill=C["accent"])
        pg.rect(x0 + bw * 0.50, cy, bw * 0.34, ch * dem_d[m] / vmax, fill=C["accent_deep"])
        pg.text(MON[m], x0 + bw / 2, cy - 4, 7.5, C["ink"], True, "C")
    ry = cy - 12
    pg.text("River", cx - 1.5, ry + 1, 7, C["water_deep"], True, "R")
    pg.text("worst case", cx - 1.5, ry - 2, 5.5, C["water_deep"], False, "R")
    pg.text(cite("dsi", "rg"), cx + cw + 1, ry + 0.3, 6, C["water_deep"])
    for m in range(12):
        v = R["river_month_m3"][m]; x0 = cx + m * bw
        if v > 0:
            pg.rect(x0 + 0.6, ry - 1.2, bw - 1.2, 5.2, fill=C["water"])
            pg.text("%.1fM" % (v / 1e6), x0 + bw / 2, ry + 0.3, 6.5, C["white"], True, "C")
        else:
            pg.text("0", x0 + bw / 2, ry + 0.3, 6.5, C["ink2"], False, "C")
    sy = ry - 8; ty = sy - 7
    pg.text("Site", cx - 1.5, sy + 1, 7, C["green_mid"], True, "R")
    pg.text("Strip", cx - 1.5, ty + 1, 7, C["water_deep"], True, "R")
    for m in range(12):
        x0 = cx + m * bw
        pg.text(k_(R["site_month_m3"][m]), x0 + bw / 2, sy + 0.3, 6.5, C["green_mid"], False, "C")
        v = R["strip_month_m3"][m]
        pg.text(k_(v) if v else "river", x0 + bw / 2, ty + 0.3, 6.5, C["water_deep"], False, "C")
    lx = x + w - 62
    pg.rect(lx, y + h - 13, 3, 3, fill=C["accent"]); pg.text("mean year", lx + 4.5, y + h - 12.5, 7)
    pg.rect(lx + 28, y + h - 13, 3, 3, fill=C["accent_deep"]); pg.text("1 in 5 dry", lx + 32.5, y + h - 12.5, 7)
    yr = max(sum(dem_n), 1); jun_sep = sum(dem_n[5:9])
    # v2.4: the Jun-Sep share as a big figure on a bracket under those four months (was a sentence)
    bx0, bx1, byy = cx + 5 * bw + 0.6, cx + 9 * bw - 0.6, y + 0.6
    pg.line([(bx0, byy + 1.6), (bx0, byy), (bx1, byy), (bx1, byy + 1.6)], C["accent_deep"], 0.35)
    inline(pg, bx0, y - 5.0, [("%d %%" % round(100.0 * jun_sep / yr), 11, C["accent_deep"], True),
                             (" of the need · river 0 · strip draws first", 7.5, C["ink"], True)])

# ------------------------------------------------------------------ panel 2: what the site can catch
def panel_catch(pg, R, x, y, w, h):
    panel_title(pg, x, y + h, "2", "What the site itself can catch", "m³ a year · mean of 34 water years · cumulative %s" % cite("era5", "mgm"))
    steps = R["site_catch_steps"]; total = sum(s["m3_per_year"] for s in steps)
    cum_prev = 0; bx, bw = x + 44, w - 70; vmax = nice(max(total, 1) * 1.1); yy = y + h - 20
    for s in steps:
        add = s["m3_per_year"]; cum = cum_prev + add
        pg.text(s["name"], x, yy + 1.2, 8.5, C["ink"], True)
        sk = {"Walk tops": " " + cite("dwa"), "Riverside walks": " " + cite("dwa"), "Retention terraces": " " + cite("abu")}.get(s["name"], "")
        pg.text("%s m², %.2f m³/m²%s" % (fmt(s["m2"]), add / s["m2"] if s["m2"] else 0.0, sk), x, yy - 2.6, 6.5, C["ink2"])
        pg.rect(bx, yy - 2, bw * cum_prev / vmax, 6, fill=C["faint"])
        pg.rect(bx + bw * cum_prev / vmax, yy - 2, max(0.4, bw * add / vmax), 6, fill=C["green_mid"])
        pg.text("+" + fmt(add), bx + bw * cum / vmax + 1.5, yy - 0.2, 8, C["green_deep"], True)
        cum_prev = cum; yy -= 13
    sh = [100.0 * total / d["mean"] for d in R["farm_demand_m3"].values() if d["mean"]]
    inline(pg, x, yy + 1, [("= %s m³ a year" % fmt(total), 12, C["green_deep"], True),
                           ("  = %.1f-%.1f %% of the farms' need" % (min(sh or [0]), max(sh or [0])), 9, C["green_deep"], True)])
    # v2.4: the terrace point as two drawn runoff bars (was a paragraph); same figures, same source
    ty = yy - 6.5; icon(pg, "terrace", x, ty + 3.2, 6.5)
    pg.text("Terraces: for the plants, not a supply", x + 8.5, ty, 8, C["green_deep"], True)
    pg.text("rain let out " + cite("abu"), x + 8.5, ty - 3.4, 6.5, C["ink2"])
    for i, (lab, v, col) in enumerate((("without terraces", 20, C["structure"]), ("terraced slope", 4, C["green_mid"]))):
        ry = ty - 8.5 - i * 5.0
        pg.text(lab, x + 8.5, ry + 0.4, 6.5, C["ink"])
        pg.rect(bx, ry - 0.4, bw * 0.4 * v / 20.0, 3.4, fill=col)
        pg.text("%d %%" % v, bx + bw * 0.4 * v / 20.0 + 1.5, ry + 0.4, 8, C["ink"], True)
    pg.text("past the walks: each further surface adds little", x, ty - 20.0, 6.8, C["ink2"])

# ------------------------------------------------------------------ panel 3: the sizing curve
def panel_curve(pg, R, x, y, w, h):
    mix = R["design"]["mix"]; crop = mix.split()[-1]
    panel_title(pg, x, y + h, "3", "Storage size against the farm need covered",
                "34 water years 1991-2025 · daily · cropland as %s %s" % (crop, cite("era5", "fao56")))
    pg.text("in: winter river (worst case) + site catch · strip first " + cite("dsi"), x + 8, y + h - 9.6, 7, C["ink2"])
    cx, cy, cw, ch = x + 14, y + 14, w - 22, h - 38
    cc = R["curve_closed"][mix]; tick = nice(cc[-1][0] / 8.0); nt = int(math.ceil(cc[-1][0] / tick)); vmax = tick * nt
    for t in range(0, 101, 25):
        yy = cy + ch * t / 100.0; hl = t in (25, 50)
        pg.line([(cx, yy), (cx + cw, yy)], C["structure"] if hl else C["faint"], 0.3 if hl else 0.15, (1.2, 0.8) if hl else None)
        pg.text("%d %%" % t, cx - 1.5, yy - 1, 7, C["ink2"], hl, "R")
    for j in range(nt + 1):
        v = tick * j
        pg.text(fmt(v / 1000) + "k" if v else "0", cx + cw * v / vmax, cy - 4.5, 7, C["ink2"], False, "C")
    pg.text("storage, m³", cx + cw, cy - 9, 7, C["ink2"], False, "R")
    series = [(cc, 1, C["water_deep"], None, "closed (aquifer, tank): median year"),
              (cc, 2, C["accent"], None, "closed: 1 in 5 dry year"),
              (R["curve_open"], 1, C["water_deep"], (1.4, 0.9), "open pond: median year"),
              (R["curve_open"], 2, C["accent"], (1.4, 0.9), "open pond: 1 in 5 dry")]
    for rows, col, colr, dash, lab in series:
        pg.line([(cx + cw * r[0] / vmax, cy + ch * min(r[col], 100.0) / 100.0) for r in rows], colr, 0.7, dash)
    xs = cx + cw * STRIP_TODAY / vmax
    pg.line([(xs, cy), (xs, cy + ch)], C["ink2"], 0.25, (0.6, 0.6))
    pg.text("today %s m³:" % fmt(STRIP_TODAY), xs + 1, cy + ch - 3, 6.5, C["ink2"]); pg.text("the strip only", xs + 1, cy + ch - 6, 6.5, C["ink2"])
    d = R["design"]
    xr = cx + cw * d["storage_m3"] / vmax; yr_ = cy + ch * min(d["covered_pct_1in5_dry"], 100.0) / 100.0
    pg.line([(xr, cy), (xr, yr_)], C["accent_deep"], 0.4, (0.8, 0.6))
    pg.poly([(xr - 1.8, yr_), (xr, yr_ + 1.8), (xr + 1.8, yr_), (xr, yr_ - 1.8)], fill=C["accent_deep"], closed=True)
    pg.text("cost cut-off " + cite("ross"), xr - 2.5, yr_ - 5, 8, C["accent_deep"], True, "R")
    pg.text("%s m³ = %.0f %%" % (fmt(d["storage_m3"]), d["covered_pct_1in5_dry"]), xr - 2.5, yr_ - 8.6, 8, C["accent_deep"], True, "R")
    ly = y + h - 15
    for i, (rows, col, colr, dash, lab) in enumerate(series):
        lx = cx + 2 + (i % 2) * 78; lyy = ly - (i // 2) * 4.2
        pg.line([(lx, lyy + 1), (lx + 6, lyy + 1)], colr, 0.7, dash); pg.text(lab, lx + 7.5, lyy, 6.8)

# ------------------------------------------------------------------ panel 4: where to store
def panel_store(pg, R, x, y, w, h):
    L = R["lands"]
    panel_title(pg, x, y + h, "4", "Cost per m³ delivered: cheapest first, then stop",
                "US$/m³ delivered · capital 5 % a year (FLAG) · own land " + cite("suds"))
    na = {r["key"]: r for r in R["ladder_no_recharge"]}
    rows = [("Aquifer recharge", "winter water into the alluvium " + cite("ross"), RECHARGE_USD[0], RECHARGE_USD[1])]
    lab = dict(pond="%.1f ha, %s m³ at most" % (L["pond_land_ha"], fmt(L["pond_land_ha"] * 1e4 * POND_DEPTH * POND_USE)),
               crates="%s m² of walks" % fmt(L["walk_m2"] + L["riverside_walk_m2"]), cistern="0.12 m² of land per m³")
    for key, name, _, _ in BUILT:
        if key in na: rows.append((name, lab[key], na[key]["usd_per_m3_low"], na[key]["usd_per_m3_high"]))
    bx, bw = x + 50, w - 56
    lg = lambda v: (math.log10(min(max(v, 0.1), 100.0)) + 1) / 3.0          # 0.1 .. 100 US$ on a log axis
    top = y + h - 14; rh = 8.0; n = len(rows)
    for t in (0.1, 1, 10, 100):
        xx = bx + bw * lg(t)
        pg.line([(xx, top + 3), (xx, top - n * rh + 1)], C["faint"], 0.15)
        pg.text(("$%g" % t), xx, top - n * rh - 2.5, 6.5, C["ink2"], False, "C")
    a0, a1 = ALTERNATIVE_USD
    pg.rect(bx + bw * lg(a0), top - n * rh + 1, bw * (lg(a1) - lg(a0)), n * rh + 2, fill=C["water_light"])
    pg.text("recycled water " + cite("ross"), bx + bw * lg(a1) + 1, top + 4.2, 6.5, C["water_deep"], True)
    for i, (nm, ld, lo, hi) in enumerate(rows):
        yy = top - i * rh
        pg.text(nm, x, yy, 7.5, C["ink"], True); pg.text(ld, x, yy - 3, 6, C["ink2"])
        pg.rect(bx + bw * lg(lo), yy - 1.5, max(0.8, bw * (lg(hi) - lg(lo))), 4, fill=C["green_mid"] if hi < a0 else C["accent"])
        if hi < a0:        # v2.4: "cheaper than recycled" sits on the bar itself (was a sentence naming the rows)
            pg.text("cheaper than recycled", bx + bw * lg(lo) - 1.5, yy - 0.6, 6, C["green_deep"], True, "R")
    lo_, hi_ = R["design"]["central_range_m3"]
    cheap = [r[0] for r in rows if r[3] < a0]
    inline(pg, x, y + 3.5, ([] if cheap else [("nothing cheaper than recycled · ", 7.2, C["accent_deep"], True)]) +
           [("recharge pays up to ", 7.2, C["accent_deep"], True), ("%s-%s m³" % (fmt(lo_), fmt(hi_)), 10, C["accent_deep"], True),
            ("  past that: storage exceeds the need, water ages out", 7.2, C["accent_deep"], False)])

# ------------------------------------------------------------------ panel 5: our claims, honestly
def panel_claims(pg, R, x, y, w, h):
    panel_title(pg, x, y + h, "5", "What the cost cut-off gives, and our claims")
    d = R["design"]; bw = (w - 6) / 2.0; by = y + 8; bh = h - 18
    for i in range(2):
        pg.rect(x + i * (bw + 6), by, bw, bh, fill=C["paper"] if i else C["water_light"], stroke=C["structure"], lw=0.2)
    lo_, hi_ = d["central_range_m3"]; plo, phi = d["central_range_pct_1in5_dry"]
    span = lambda a, b, f=fmt: f(a) if a == b else "%s-%s" % (f(a), f(b))
    pg.text("Size set by cost", x + 3, by + bh - 7, 10, C["accent"], True)
    pg.text("%s m³" % span(lo_, hi_), x + 3, by + bh - 14.5, 14, C["ink"], True)
    pg.text("= %s %% of the farms, 1 in 5 dry year" % span(round(plo), round(phi)), x + 3, by + bh - 19.5, 7.5, C["ink"], True)
    pg.text("range %s m³ = %s %%" % (span(*d["full_range_m3"]), span(*[round(v) for v in d["full_range_pct_1in5_dry"]])), x + 3, by + bh - 24, 6.8, C["ink2"])
    pg.text("if borehole tests accept recharge", x + 3, by + 3, 6.8, C["ink2"])
    bx = x + bw + 6
    pg.text("Our 25 % / 50 % claims", bx + 3, by + bh - 7, 10, C["accent"], True)
    for j, pct in enumerate(("25", "50")):
        v = [t[pct] for t in R["need_for_target_1in5_dry_m3"].values()]
        txt = "not reached" if None in v else "%s m³" % span(min(v), max(v))
        pg.text("%s %%: %s" % (pct, txt), bx + 3, by + bh - 14.5 - j * 6, 10, C["ink"], True)
    tc = [t["covered_pct_1in5_dry"] for t in R["today_strip_storage"].values()]
    pg.text("today %s m³ gives %.0f %% (it is the strip's)" % (fmt(STRIP_TODAY), max(tc)), bx + 3, by + 3, 6.8, C["ink2"])
    rc = R["rain_credit_pct"]; crops = ["olive"] + [m.split()[-1] for m in R["farm_demand_m3"]]
    rv = [rc[c] for c in crops]
    # v2.4: three keyword items with pictograms (was a three-sentence paragraph)
    ty, ic = y + 2.6, 4.6; xx = x
    for kind, parts in (("drop", [("rain held ", 6.5, C["ink2"], False), ("%.0f-%.0f %%" % (min(rv), max(rv)), 9, C["water_deep"], True),
                                  (" of crop use, rest stored " + cite("fao56", "fao_t"), 6.5, C["ink2"], False)]),
                        ("clock", [("max ", 6.5, C["ink2"], False), ("365 days", 9, C["ink"], True), (", then to the strip", 6.5, C["ink2"], False)]),
                        ("cube", [("recharge fails tests: built > recycled, every step " + cite("suds"), 6.5, C["ink2"], False)])):
        icon(pg, kind, xx, ty + ic - 0.6, ic)
        xx = inline(pg, xx + ic + 1.2, ty, parts) + 4.0

def build(path, R):
    L = R["lands"]
    pg = Page(420.0, 297.0)
    pg.rect(0, 0, 420, 297, fill=C["ground"])
    pg.text("THE WATER BALANCE", 14, 280, 22, C["ink"], True)
    del SRC_KEY[:]                                        # v2.4: [n] numbers restart on every run
    pg.text("Farm water · what our system can carry", 14, 272.5, 11, C["ink2"])
    pg.text("lands option %s · run %s" % (L["option"], R["run_time"]), 14, 266.5, 6.8, C["ink2"])
    # v2.4: the farms paragraph as four pictogram tiles (same place, same figures)
    tw_ = (156.0 - 3 * 2.5) / 4.0
    for i, (kind, head, big, foot) in enumerate((
            ("field", "Cropland", "%.1f ha" % L["cropland_ha"], "satellite " + cite("esa")),
            ("olive", "Orchard", "%.1f ha" % L["orchard_ha"], "satellite " + cite("esa")),
            ("sun", "Need: ET0, normal", "%s mm/yr" % fmt(ET0_NORMAL), "daily · drip " + cite("fao56", "mgm")),
            ("strip", "Strip, sealed", "%s m²" % fmt(L["strip_m2"]), "low-flow strip"))):
        tile(pg, kind, 250 + i * (tw_ + 2.5), 291.0, tw_, 19.0, head, big, foot)
    panel_timing(pg, R, 14, 160, 190, 100)
    panel_catch(pg, R, 220, 160, 186, 100)
    panel_curve(pg, R, 14, 30, 190, 118)
    panel_store(pg, R, 220, 88, 186, 60)
    panel_claims(pg, R, 220, 22, 186, 56)
    for k in SOURCES:                                     # v2.4: one numbered source key (no source can drop out)
        if k not in SRC_KEY: SRC_KEY.append(k)
    pg.para("Sources by number: " + "  ".join("[%d] %s" % (i + 1, SOURCES[k]) for i, k in enumerate(SRC_KEY)) +
            "  Calculations: research/water_balance/NOTES.md.", 14, 12, 392, 6, C["ink2"])
    write_pdf(pg, path)

# ------------------------------------------------------------------ run (GH Button on any input, ScriptEditor, or python)
def main(g):
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    L, src = get_lands(g)
    R = compute(L); R["lands_source"] = src
    path = os.path.join(OUT_DIR, OUT_PDF)
    try:
        build(path, R)
    except PermissionError:
        return "The PDF is open in another program. Close it and press again: " + path
    with open(os.path.join(OUT_DIR, OUT_JSON), "w", encoding="utf-8") as f:
        json.dump(R, f, indent=1, ensure_ascii=False)
    d = R["design"]; tm = time.strftime("%H:%M:%S")
    return "%s  %s\n%s  %s\ncut-off %s m3 = %.1f %% (1 in 5 dry)\n%s %s, %.1f s" % (
        OUT_PDF, tm, OUT_JSON, tm, fmt(d["storage_m3"]), d["covered_pct_1in5_dry"], "water balance", VERSION, time.time() - t0)

#@include ../common/chain_fire.py


#@include ../common/done_text.py


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    _pressed = any(v is True for k, v in list(globals().items()) if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done")) or \
        any(chain_fire(v, "bergama_water_balance_log_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main(globals())
        except Exception as _ex:   # 25 Oct: the error goes into the log panel, the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_water_balance_log" + _ik] = write_log(_res)
        _sc.sticky["bergama_water_balance_log_status" + _ik] = ("ERROR" if _sc.sticky["bergama_water_balance_log" + _ik].startswith(("ERROR", "The PDF is open")) else time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky["bergama_water_balance_log_done" + _ik] = done_text(True, not _sc.sticky["bergama_water_balance_log_status" + _ik].startswith("ERROR"), time.time() - _t0)
    done = _sc.sticky.get("bergama_water_balance_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_water_balance_log" + _ik, "Press the Button to compute and export to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "WaterBalance " + VERSION + " · " + _sc.sticky.get("bergama_water_balance_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main(globals())))
