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

INPUT_DATA = (
    "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"
    "0q8qOfc6UoWeidC26/kcl5NiXBvqk6pSNDXam7S4n2IAqKunr75bSLEoZNTLbznVsxepEm9NybduA2Y8FALjtf/ZbbNcne+Tw/GS"
    "sm2bj5Zx9eor7ebi0S49RJikxqknd3oaNjUdElPy/k1L9sKdm3YwpwyxX1uB5sr2XfEdLjShhrm401LhLsKqRbnO+ZEMV0HSujPb"
    "DqXIR6oXE84769AvqfOwgUV0L+PddkGZ5HPul9aeOe5qn33X6qtb9ZDAaLprA9gN7NgYSnXJhNZZnSmkZbZtQd057XxZ3NKZfKl4"
    "O0v0x7wLvRmVJyS8SeHiwXIWWFNzgTxiSNsqzYSd0zHdh/Nnw8wwGYfqriG7c3VRp4yhThxg2OmMXpRzZFhfLiSr6l7PmhKEcrrm"
    "d+9eVegtO2ZreoeLr6G9DVnwUNxVzDzTub5Lh0DBXVM7wGaWN1QIzXDoxqViR7JrSpJ/XgzHQ4w1Nnxs+jAIbYPFeDAGn9QsM892"
    "hlA1iJJ1s4qwlVuchudm04dymrTQo/it2KLZTU9ZTGl9Mf05rbUY1rDU6ZaCjUwx85PTTvtgssF+ZAnqKGS01ZvuVxFkxrGchyW7"
    "VMptqU1iJfAM3MVENlOLmguGti7ql3AE8GLaBnd0W20VQQKMueoC17ouTUXIXpyQw6YH6mptiMHCPhdVc35KXEY5jI3humWv1W2Q"
    "uztZuNd8665KKW7laV/03b1ouAlr2mpbyy7CTkV9XkUVc10KhOV+KEOWPJbJVUuQmxmNHaJs/5520N3eF8Kzy1G9y8soJHlITuzl"
    "OFXXYflaSVd54c4NJoqXmUw9qWiV9qlUcZ9W2hIKtS5EDsO1zqfSQsuQPId2e9TSTzmHpNnD8mKtUMzrtdNvUnFbZdnL+u7ponlb"
    "5XNJ7fN0/RQztTXSzar0aQGyOtaoFGTHYW+N5nBa1/1IGF9lYa82jbvr0pSAuanrjQqzxZJJ8+FeKLupXlbcZEylILkrblJ7ZOs3"
    "11+pQ49qq2ibWNx1CdTHtF0m2GPEyB6umxuXpT5Fou5isgTnZSNnK6O8xdRDELmrvkC+uk3HJvVhSqQq109rM+or1Emqsq9Ld+2C"
    "bOwJ01hb0gVDy65vmxI3Y/5Th2fre2TBdjaKFu/N3aFMabA5nRli6CPYpLpIQ0erH+kV0M6U0H045lH3ts0w4mSDCZspqF5ikeml"
    "MskuTzcDZByHHq1YTA0WurgmcJi+QIMfJGCmG18XsdGE5qAu2JVqKHZ2d6wqMgFRI+6uzBs9mF0HwhYA6mTF7iZmkVnXU+z33EVH"
    "UCczbWEX00YlagZOIbMZfbLKuzF1F/tP+oJtdeOyq0t+HiGdHZ9p0naMFrOGrmSZOWbUnlXN/1zjtOEzBM/DOk0av1SZw8ywl3Iy"
    "pnDDiSZ8wQR7cieT7GJr0hfLJjfLRhmNompV9bkX0TIFkoShGKuYfuqEe1o72llaJuvfbqNmVwzSS65emo26GdB8xj4FM7lVuFN2"
    "XNXSDLvef+6eJRu75rl7p+6Cvmyu4gTPW2A8ds01qwlFd1RFxdwVttNZlBKym1MnJ3SxwkCw9bxsAYPC60H0zp6BrmjpVks05vNi"
    "9+9zZO+u716m2SNd6kBWnJuan86Jzq2JcUrOZlJqGdMlPK42qp5Wn2MZGHImEpW/lOSbThnUW0+Qpv4h8rhTTXbZPQlJsewOq+ac"
    "lwaGxHHDFSBZgxPgmA5zcidimpoeXhIy0yw86tXvF58VFh/TZFwTqVDUbIPyKhcNCfUsgehW9lPioaoN7kspkrMYuUvUK483BfJt"
    "ii7ANF0hMtwPOSR0C3ET3fxFocezfChxPO758ftdgYLFIGty0peZbYIE2Nr2oSN/rUoaFqvt/su8RvmgUdw87IU5FByHHRto0E+n"
    "h3L1vubos5fnsOOPgXBQENTILYOvkKORi6izDO2DHXrk/RbIonTxCwygWXKPkZ2ic5Hh6uaMqdFP3qgMgn3JKsp1Tr2ZR+kK5NmL"
    "BD6HBYwSRqsT7BLYZwGfu842+YtygcTv2JZKhYwC7buxgAF62LkIC22oqJ5ixQj7Y9srbjsY0blKBX90LaJPa1KAHiqyb+7Nrqqm"
    "rLFLbsIuKRjzSTWzDNjVfB3Hcj57SbBdVN8p7OlKKrcz3H165jT3UuU6xnlhYDqTu6m6AQS5jGSZ1C7/i1Nml92/Qp673l/P3eEz"
    "n2pn/hxz3I1IVligbJu1kb1dx9okawxTwaOeSHrv/XfMONOF69YScFxAeVGhsfLpg8GHaQ4iThXcZEMnkAxxqpqxL2TAFcljmXap"
    "p7hDZqPdEZetFiweMcEAUzlp74Zpi6WWMKpi3/0OzSpP90vdIbtZPmcOIk8VThbLD2ffJeRSJnYpz4e7uzSLN5Y9mDbHTL99P7xq"
    "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")

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

def rgb(h): return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]

def text_w(s, size, bold=False):
    w = sum(_HW[ord(ch) - 32] if 32 <= ord(ch) < 127 else 556 for ch in s)
    return w / 1000.0 * size * (1.06 if bold else 1.0) * 0.3528      # size in pt -> width in mm

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
        b = s.encode("cp1252", "replace").replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
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
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"]
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

def chain_fire(v, key):
    """25 Oct 10:20 (one-click chain): the previous script's done output is a text "done HH:MM:SS.ss ..." that stays
    after the Button is released; each NEW text fires this script once (the Button still works as before)."""
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if x is not None), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done "):
        return False
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid)              # noqa: F821
        except Exception:
            pass
        if _scx.sticky.get(key) == s:
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


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
