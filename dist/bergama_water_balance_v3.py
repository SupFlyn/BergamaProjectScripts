# bergama_water_balance_v3.py (v3, 27 Oct: the stream on the sheet; v2.7 layout kept) · Thread 2 of the 22 Oct batch: water balance (demand, collection, storage, cost cut-off)
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

VERSION = "v3"
# v3 (Aras 27 Oct 17:34, booklet Prompt 4 "water, part 1"; v2.7's layout kept, nothing moved):
#   * panel 2 "What the site can catch" adds what the STREAM gives, same units and bars: the Selinos winter flow the
#     store takes (Nov-Apr, the worst-case gauge series the storage already runs on, at the design store) and the share
#     of that winter flow left in the stream (mean year and the driest year). Computed live: run_storage now also counts
#     the stream's part of what enters the store (site catch first, the stream tops up: the stream's part is the low
#     side); results JSON gains design.river_take_m3_per_year, river_take_share_pct, river_left_pct, river_avail_m3_per_year.
#   * "How the stream behaves" (was the booklet page before this one, the water board's wb_water) leads the sheet as a
#     band beside the title: the natural flow past the site by month (Jul-Sep marked dry), and how high the stream rises
#     on the surveyed upstream-entry cut at 1:500 (Jan-Feb, max 2017, Q100, Q500), its scale bar under the label column.
#     Only what carries the argument; its figures from rain_river_levels A2 / A3s (constants below, sourced).
#   * the text under the component shows a newly pasted version at once, idle (Aras 27 Oct 15:35).
# v2.7 (Aras 27 Oct 11:07, booklet p10; PHASE2_SPEC §6 "p9-10"): white sheet; no source footer (the numbered key is now an
#   invisible text layer the booklet's sources page still reads; [n] marks stay); NEW LAYOUT read top-left -> bottom-right:
#   THE ANSWER (focal: store m³ -> % of the farms carried -> cost cut-off, our claims under it), farm tiles, then
#   1 timing | 2 site catch, 3 storage curve | 4 cost per m³; sentences -> keywords; labels placed with measured boxes
#   (text_w) and an overlap check (the log names any overlap). Computation and results JSON unchanged (script name only).
# v2.6 (Aras 25 Oct 21:47-21:51, booklet/CROP_SPEC.md): the booklet shows this sheet's own drawings: booklet/blocks.json
#   lists one crop per panel (1-5 and the header tiles; rects from PANELS / TILES below); the separate booklet redraws
#   (bk_timing, bk_catch, bk_curve, bk_store and their PDFs) are gone. Sheet words: the Selinos is a stream ("Stream"
#   row, "Streamside walks"), no "(FLAG)" caveat. Layout, look and the results JSON keys unchanged.
# v2.5 (25 Oct, booklet stage 2, SCRIPT_STANDARD §8): also writes output/Bergama_water_balance_analysis/booklet/ (4 text-free
#   drawing PDFs at their booklet frame size + blocks.json with every word as a label); results JSON gains
#   jun_sep_share_of_need_pct and site_catch_share_of_need_pct. The A3 sheet is unchanged.
# v2.3 (Aras 25 Oct 16:43: "the selection of A should be remember in the whole project so all scripts should drop B alternatives"): option A only; the option input is ignored.
# v2.2 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_water_balance_log.txt (next to cached/ and output/), overwritten by each press.
# ---- Bergama folders (Aras 24 Oct 08:28 + 27 Oct 11:07; SCRIPT_STANDARD §9). Every script uses ONLY these. ----
#   Downloads/Bergama/output/<name>/          final PDFs only
#   Downloads/Bergama/logs/                    every log file and log folder
#   Downloads/Bergama/cached/<name>/           caches, results other scripts read, any other working file
#   Downloads/Bergama/cached/booklet/<name>/   the script's booklet assets (blocks.json, results, images);
#                                              the booklet's own leftovers in cached/booklet/
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_booklet(name):
    return os.path.join(BERGAMA_ROOT, "cached", "booklet", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


def bg_first(paths):
    """The first path that exists (new place first, then where older versions wrote it), else the first."""
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[0]


def bg_tidy_output(name, cache_dir=None):
    """output/<name>/ keeps PDFs only: log files and anything in a log folder move to logs/<name>/, every other
    non-PDF file to cached/<name>/from_output/ (or cache_dir: the booklet uses cached/booklet/; moved, never deleted;
    same sub-folders). Empty folders go.
    Returns short log lines (counts, not one line per file)."""
    import shutil as _sh
    root, moved, fail = bg_output(name), {}, []
    if not os.path.isdir(root):
        return []
    for d, subs, files in os.walk(root, topdown=False):
        rel = os.path.relpath(d, root)
        rel = "" if rel == "." else rel
        for fn in files:
            if fn.lower().endswith(".pdf"):
                continue
            is_log = "log" in fn.lower() or any("log" in p.lower() for p in rel.split(os.sep) if p)
            dst = os.path.join(bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output")), rel, fn)
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(dst):
                    os.remove(dst)
                _sh.move(os.path.join(d, fn), dst)
                top = bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output"))
                moved[top] = moved.get(top, 0) + 1
            except Exception as ex:
                fail.append(u"%s (%s)" % (os.path.join(rel, fn), type(ex).__name__))
        if d != root:
            try:
                os.rmdir(d)                       # only when empty
            except Exception:
                pass
    return ([u"output/%s: %d non-PDF file(s) moved to %s" % (name, n, d) for d, n in sorted(moved.items())] +
            ([u"output/%s: could not move %s" % (name, ", ".join(fail[:5]))] if fail else []))
LOG_DIR = bg_logs()                        # Aras 25 Oct 09:34-09:35: every script's log here


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
OUT_DIR = bg_output("Bergama_water_balance_analysis")        # final PDFs only (27 Oct)
RES_DIR = bg_cache("Bergama_water_balance_analysis")         # 27 Oct: the results JSON other scripts read
OLD_OUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis")   # read fallback only
OUT_PDF = "Bergama_water_balance_A3.pdf"
OUT_JSON = "water_balance_results.json"
MP_FILE = bg_first([os.path.join(bg_cache("bergama_masterplan"), "masterplan_results.json"),      # 27 Oct: cached/
                    os.path.join(bg_output("bergama_masterplan"), "masterplan_results.json")])    # masterplan v24 and older

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

# v3: how the stream behaves (the band beside the title). Natural flow past the site, m³ a month Jan-Dec:
# rain_river_levels/tables/A2_rain_to_river_monthly_m3.csv "from_catchment_m3" (DSİ gauges D04A053 + D04A063,
# Oct 2015-Sep 2021, each area-scaled to 101 km², mean of the two; the upper case, the Kestel diversion not counted).
STREAM_MONTH_M3 = [7073107, 4466564, 3692654, 2319752, 917943, 427462, 154468, 39136, 37531, 208432, 513967, 1101169]
STREAM_DRY_DAYS = (0, 111)   # measured: days a year both gauges were completely dry, 2016-2021 (rain_river README §1)
# The surveyed upstream-entry cut (water board CUTS "up" = rain_river_levels A3s, v1.1 24 Oct): ground every 1 m from
# u0 (m from the centreline; - = right bank), m above the bed low point; depths (m above the bed, Manning n 0.050) and
# the width each covers (from, to). max 2017 = the highest day of 2016-2021, 6 Jan 2017 (43.9 m³/s area-scaled).
STREAM_CUT = dict(u0=-42, ground=[
    5.45, 5.24, 5.17, 5.11, 5.05, 4.99, 4.92, 4.86, 4.55, 4.18, 3.82, 3.45, 3.01, 2.57, 2.21, 2.14, 2.07, 2.0, 1.93,
    1.86, 1.8, 1.73, 1.66, 1.59, 1.52, 1.45, 1.38, 1.32, 1.25, 1.19, 1.12, 1.06, 0.99, 0.93, 0.87, 0.8, 0.74, 0.67,
    0.61, 0.54, 0.48, 0.41, 0.35, 0.29, 0.22, 0.16, 0.09, 0.03, 0.02, 0.39, 0.75, 1.1, 1.46, 1.82, 2.19, 2.54, 2.86,
    3.16, 3.46, 3.75, 3.97, 4.05, 4.24, 4.46, 4.7, 4.94, 5.07, 5.08, 5.12, 5.14],
    levels=[("Jan-Feb", 0.64, (-4.0, 7.5)), ("max 2017", 1.69, (-20.0, 10.5)), ("Q100", 2.99, (-29.5, 14.0)),
            ("Q500", 3.30, (-30.5, 15.0))])
CUT_Q500 = dict(upstream=3.30, K4=2.84, K5=2.79, downstream=2.33, flat_end=1.54)   # A3s, m above the bed, the five cuts
K4_RIGHT_BANK, K4_Q100 = 2.08, 2.56     # A3s: K4's lower (right) bank top and its Q100 depth, m above the bed
STREAM_DEN = 500.0                      # the cut at 1:500, true proportions (a standard scale)

def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_water_balance_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_water_balance_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_water_balance_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'INPUT_DATA': '1c4b3056c69043ddf2d0e860039d5e8b'}.get(name):
        raise RuntimeError("Data file bergama_water_balance_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_water_balance_data.py:" + name, "exec"), globals())


bergama_data("INPUT_DATA")

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

def run_storage(V, A, demand, strip, inflow, et0, days, reserve, max_age=MAX_AGE, site=None):
    """v3: with site (the site catch each day) also counts per water year the stream's part of what enters the
    store (per[y][4]) and all that enters it (per[y][5]): the site catch fills first, the stream tops up."""
    Q = deque(); S = 0.0; flushed = 0.0; oldest = 0
    per = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
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
        if x > 0:
            Q.append([i, x]); S += x
            if site is not None: r_ = per[wy(d)]; r_[4] += max(0.0, x - site[i]); r_[5] += x
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
    res = dict(script="bergama_water_balance_v3.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
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
             ("Streamside walks", "walk", L["riverside_walk_m2"]), ("Retention terraces", "terrace", L["terrace_m2"])]
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
    avail = defaultdict(float)                              # v3: the stream's winter water an intake may take, per water year
    for d, r in zip(days, R): avail[wy(d)] += r
    def stats(V, mix, Vopen=0.0):
        inflow = [min(V / INTAKE_DAYS, r) + s for r, s in zip(R, site)]
        per, fl, old = run_storage(V, Vopen / POND_DEPTH, dem[mix], strip, inflow, E, days, RES, site=site)
        per.pop(min(per))                                   # first water year = spin-up (storage starts empty)
        cov = sorted(per[y][1] / per[y][0] for y in per if per[y][0] > 0)
        n = len(cov)
        tk = [per[y][4] / avail[y] for y in per if avail[y] > 0]     # v3: share of each year's winter water taken
        return dict(median=cov[n // 2], dry5=cov[int(round(0.2 * (n - 1)))], dry10=cov[int(round(0.1 * (n - 1)))],
                    delivered=sum(per[y][1] for y in per) / len(per), released=fl / len(per), oldest=old,
                    strip_min=min(per[y][3] / per[y][2] for y in per if per[y][2] > 0) if any(per[y][2] for y in per) else 1.0,
                    river_in=sum(per[y][4] for y in per) / len(per), stored=sum(per[y][5] for y in per) / len(per),
                    river_share=sum(per[y][4] for y in per) / max(sum(avail[y] for y in per), 1.0),
                    river_share_max=max(tk) if tk else 0.0, avail=sum(avail[y] for y in per) / len(per))
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
    # v3: what the stream gives at the design store (mean of the water years after the spin-up year)
    st = stats(dc["storage_m3"], design)
    res["design"].update(river_take_m3_per_year=round(st["river_in"]),
                         river_take_share_pct=round(100.0 * st["river_in"] / max(st["stored"], 1.0), 1),
                         river_left_pct=[round(100.0 * (1.0 - st["river_share_max"]), 1), round(100.0 * (1.0 - st["river_share"]), 1)])
    res["river_avail_m3_per_year"] = round(st["avail"])
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
    p = path or bg_first([os.path.join(RES_DIR, OUT_JSON), os.path.join(OUT_DIR, OUT_JSON), os.path.join(OLD_OUT_DIR, OUT_JSON)])
    try:
        with open(p, encoding="utf-8") as f: return json.load(f)
    except Exception:
        return None

# ------------------------------------------------------------------ colours (palette v1.4 core roles)
C = dict(ground="E2E0D4", paper="EFEDE6", faint="D8D5CC", structure="B0AC9C", ink2="847E75", ink="4A3F35",
         green_deep="495338", green_mid="727A4E", green_light="8C9969", water_deep="5D7F8D", water="91ADB4",
         water_light="C1D3DB", accent="8B3A3F", accent_deep="633131", white="FFFFFF")
C["accent_tint"] = "".join("%02X" % int(round(255 - 0.12 * (255 - int(C["accent"][i:i + 2], 16)))) for i in (0, 2, 4))   # v2.7: accent at 12 % on white (the Jun-Sep band)

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

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"


class Page:
    def __init__(self, w, h):
        self.w, self.h, self.ops = w, h, []
        self.boxes = []          # v2.7: (x0, y0, x1, y1, text) of every visible label, for the overlap check
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
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", hidden=False):
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        k = 72 / 25.4
        b = b"".join(bytes([_ENC_EXTRA[ch]]) if ch in _ENC_EXTRA else ch.encode("cp1252", "replace") for ch in s)   # 25 Oct: ı İ ğ Ğ ş Ş spelt right
        b = b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
        self.ops.append("BT /%s %.2f Tf%s %s %.2f %.2f Td (%s) Tj ET" % ("F2" if bold else "F1", size, " 3 Tr" if hidden else "",
                                                                       self._c(col), x * k, y * k, b.decode("latin-1")))
        if not hidden:           # v2.7: hidden = invisible text (render mode 3): kept in the PDF, not seen, not in the overlap check
            self.boxes.append(tbox(s, x, y, size, bold) + (s,))
    def para(self, s, x, y, w, size, col="4A3F35", bold=False, lead=1.3, hidden=False):
        line, yy = "", y
        for word in s.split(" "):
            t = (line + " " + word).strip()
            if text_w(t, size, bold) > w and line:
                self.text(line, x, yy, size, col, bold, hidden=hidden); yy -= size * 0.3528 * lead; line = word
            else: line = t
        if line: self.text(line, x, yy, size, col, bold, hidden=hidden); yy -= size * 0.3528 * lead
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

# ------------------------------------------------------------------ v2.7 labels: measured boxes, no label on another
def tbox(s, x, y, size, bold=False, align="L"):
    """the box (x0, y0, x1, y1) mm a text line takes: width from text_w, height from the font's descender and caps"""
    w = text_w(s, size, bold); x0 = x - (w / 2.0 if align == "C" else w if align == "R" else 0.0)
    return (x0, y - 0.21 * size * 0.3528, x0 + w, y + 0.72 * size * 0.3528)

def hit(a, b, pad=0.25):
    return a[0] < b[2] - pad and b[0] < a[2] - pad and a[1] < b[3] - pad and b[1] < a[3] - pad

def place(pg, s, cands, size, col, bold=False, halo=False):
    """v2.7: label s at the first candidate (x, y, align) whose box touches no label set so far; else the last one
    (overlaps() then names it in the log). halo: a white field under the words, over the lines drawn before."""
    for x, y, al in cands:
        b = tbox(s, x, y, size, bold, al)
        if not any(hit(b, o) for o in pg.boxes): break
    if halo: pg.rect(b[0] - 0.7, b[1] - 0.5, b[2] - b[0] + 1.4, b[3] - b[1] + 1.0, fill=C["white"])
    pg.text(s, x, y, size, col, bold, al)
    return b

def overlaps(pg):
    """v2.7: every pair of sheet labels whose boxes overlap (the log lists them; none expected)"""
    B = pg.boxes
    return ["'%s' / '%s'" % (B[i][4], B[j][4]) for i in range(len(B)) for j in range(i + 1, len(B)) if hit(B[i], B[j])]

def fit_size(s, w, size, bold=False, low=7.0):
    """the largest size <= size (down to low) at which s fits w mm"""
    while size > low and text_w(s, size, bold) > w: size -= 0.5
    return size

def panel_title(pg, x, y, w, n, title, sub=None):
    """v2.7: a supporting panel's head: a rule over the panel's width, number, title, keyword line"""
    pg.line([(x, y + 4.5), (x + w, y + 4.5)], C["structure"], 0.3)
    pg.text(n, x, y, 11, C["accent"], True)
    pg.text(title, x + 6.5, y, 11, C["ink"], True)
    if sub: pg.text(sub, x + 6.5, y - 4.8, 7.5, C["ink2"])

def arrow(pg, x0, x1, y, col, lw=0.6):
    pg.line([(x0, y), (x1 - 2.2, y)], col, lw)
    pg.poly([(x1 - 2.6, y + 1.5), (x1, y), (x1 - 2.6, y - 1.5)], fill=col, closed=True)

# ------------------------------------------------------------------ v2.4 visual first (SCRIPT_STANDARD 5b): [n] marks, pictograms, tiles
SOURCES = dict(    # every source and method sentence of the v2.3 sheet; v2.7: an invisible text layer (the booklet's sources page reads it)
    esa="ESA WorldCover 2021: farms = analysis area of the land-use map, unless changed",
    mgm="MGM/WMO 17742 normals 1991-2020",
    era5="Open-Meteo ERA5 daily 1991-2025 (scaled to the station)",
    dsi="DSI gauges D04A053, D04A063 2016-2021, area-scaled",
    fao56="FAO-56 (Allen et al. 1998): daily soil water balance, Penman-Monteith ET0",
    fao_t="FAO-56 Tables 19 and 22",
    fao_tm4="FAO Training Manual 4 (drip)",
    rg="RG 30802 minimum flow: stream counted above the legal minimum, worst case",
    dwa="DWA-A 117",
    abu="Abu Hammad et al. 2004: runoff 20 % without terraces, 4 % terraced",
    ross="Ross & Hasnain 2018",
    suds="UK EA 2015 and Royal Haskoning 2012 SuDS costs (GBP x 1.25)",
    flow="rain_river_levels README §1-2, table A2: natural flow past the site = DSI gauges D04A053 + D04A063, Oct 2015-Sep 2021, "
         "each area-scaled to 101 km², mean of the two (upper case: the Kestel diversion not counted); both gauges fully dry 0-111 days a year",
    lev="rain_river_levels table A3s (v1.1): Manning normal depth, n 0.050 (worst), on the surveyed cuts of Bergama Müdahele Alanları (1).dxf; "
        "DSI Q100 205.2 / Q500 263.3 m³/s (Danıştay 6. D. 2021/9521 E.); max 2017 = highest day 2016-2021, 6 Jan 2017, 43.9 m³/s area-scaled")
SRC_KEY = []

def cite(*keys):
    """v2.4: "[n]" (or "[n,m]") for sources in SOURCES; the numbered key is the sheet's hidden source layer (v2.7)."""
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
    """v2.4: pictogram tile: icon, keyword heading, ONE big figure, a short foot with [n]. v2.7: no fill (white sheet), 7 pt words."""
    pg.rect(x, y - h, w, h, stroke=C["faint"], lw=0.3)
    sz = min(h - 6.0, 11.0); icon(pg, kind, x + 2.5, y - (h - sz) / 2.0, sz)
    lx = x + 5.0 + sz; tw = x + w - 1.5 - lx; fs = fit_size(big, tw, 13.0, True)
    pg.text(head, lx, y - 5.4, 7, C["ink2"], True)
    pg.text(big, lx, y - 5.4 - 1.6 - fs * 0.3528, fs, C["ink"], True)
    pg.text(foot, lx, y - h + 3.0, 7, C["ink2"])

def inline(pg, x, y, parts):
    """v2.4: a keyword row: parts = [(text, size, colour, bold)] set one after another; returns the end x."""
    for s, size, col, bold in parts:
        pg.text(s, x, y, size, col, bold); x += text_w(s, size, bold)
    return x

def inline_w(parts):
    return sum(text_w(s, size, bold) for s, size, col, bold in parts)

def span(a, b, f=fmt):
    return f(a) if a == b else "%s-%s" % (f(a), f(b))

# ------------------------------------------------------------------ v2.7 THE ANSWER: the focal block (store -> carries -> cut-off)
def panel_answer(pg, R, x, y, w, h):
    """The headline answer, read left to right: how much storage, what it carries, where cost stops it; our claims under it.
    Every figure from R (results JSON): design.central_range_m3 / _pct_1in5_dry, full_range_*, need_for_target_1in5_dry_m3,
    today_strip_storage; prices RECHARGE_USD / ALTERNATIVE_USD (Ross & Hasnain 2018)."""
    d = R["design"]
    pg.rect(x, y, w, h, fill=C["water_light"])
    pg.text("THE ANSWER", x + 6, y + h - 7, 8, C["accent"], True)
    lo_, hi_ = d["central_range_m3"]; plo, phi = d["central_range_pct_1in5_dry"]
    top = y + h - 14; big_y = top - 10; l1, l2 = top - 16.5, top - 21.5
    wa, wb, wc, gap = 84.0, 66.0, w - 12.0 - 84.0 - 66.0 - 2 * 12.0, 12.0
    # A: the store
    ax = x + 6; icon(pg, "cube", ax, top + 2, 18)
    tx = ax + 22; tw = wa - 22
    pg.text("STORE", tx, top - 1, 8, C["ink2"], True)
    s = "%s" % span(lo_, hi_); fs = fit_size(s, tw, 22.0, True)
    pg.text(s, tx, big_y, fs, C["ink"], True)
    pg.text("m³ · aquifer recharge", tx, l1, 8.5, C["ink"], True)
    pg.text("if borehole tests accept it", tx, l2, 7.5, C["ink2"])
    arrow(pg, ax + wa + 1.5, ax + wa + gap - 1.5, big_y + 2.5, C["water_deep"])
    # B: what it carries
    bx = ax + wa + gap
    pg.text("CARRIES", bx, top - 1, 8, C["ink2"], True)
    s = "%s %%" % span(round(plo), round(phi)); fs = fit_size(s, wb, 24.0, True)
    pg.text(s, bx, big_y, fs, C["water_deep"], True)
    s = "of the farms' need"; pg.text(s, bx, l1, fit_size(s, wb, 8.5, True), C["ink"], True)
    s = "1 in 5 dry year"; pg.text(s, bx, l2, 7.5, C["ink2"])
    by = l2 - 5.5                                               # a 100 % bar filled to the lower % of the range
    pg.rect(bx, by, wb, 2.4, fill=C["white"], stroke=C["structure"], lw=0.2)
    pg.rect(bx, by, wb * min(plo, 100.0) / 100.0, 2.4, fill=C["water_deep"])
    arrow(pg, bx + wb + 1.5, bx + wb + gap - 1.5, big_y + 2.5, C["water_deep"])
    # C: the cost cut-off
    cx = bx + wb + gap
    pg.text("COST CUT-OFF", cx, top - 1, 8, C["ink2"], True)
    s = "$%g-%g /m³" % RECHARGE_USD; fs = fit_size(s, wc, 18.0, True)
    pg.text(s, cx, big_y, fs, C["green_deep"], True)
    s = "recharge " + cite("ross"); pg.text(s, cx, l1, 8.5, C["green_deep"], True)
    s = "recycled water $%g-%g" % ALTERNATIVE_USD; pg.text(s, cx, l2, fit_size(s, wc, 7.5, True), C["accent"], True)
    vm = ALTERNATIVE_USD[1] * 1.02                              # the two price ranges on one linear US$ scale
    for i, (rng, col) in enumerate(((RECHARGE_USD, C["green_mid"]), (ALTERNATIVE_USD, C["accent"]))):
        yy = l2 - 4.6 - i * 3.0
        pg.line([(cx, yy + 0.9), (cx + wc, yy + 0.9)], C["white"], 0.3)
        pg.rect(cx + wc * rng[0] / vm, yy, wc * (rng[1] - rng[0]) / vm, 1.8, fill=col)
    # claims row
    sy = y + 15.0
    pg.line([(x + 6, sy), (x + w - 6, sy)], C["white"], 0.6)
    parts = [("Our claims, 1 in 5 dry year:  ", 7.5, C["ink2"], True)]
    for pct in ("25", "50"):
        v = [t[pct] for t in R["need_for_target_1in5_dry_m3"].values()]
        parts += [("%s %% " % pct, 9, C["accent"], True), ("= " + ("not reached" if None in v else "%s m³" % span(min(v), max(v))), 8, C["ink"], True),
                  ("     ", 8, C["ink"], False)]
    tc = [t["covered_pct_1in5_dry"] for t in R["today_strip_storage"].values()]
    parts += [("today ", 7.5, C["ink2"], False), ("%s m³ = %.0f %%" % (fmt(STRIP_TODAY), max(tc)), 8, C["ink"], True),
              (" (the strip's own)", 7.5, C["ink2"], False)]
    inline(pg, x + 6, sy - 5.5, parts)
    inline(pg, x + 6, sy - 11.0, [("All cost cases:  ", 7.5, C["ink2"], True),
                                  ("%s m³ = %s %%" % (span(*d["full_range_m3"]), span(*[round(v) for v in d["full_range_pct_1in5_dry"]])), 8, C["ink"], True)])

# ------------------------------------------------------------------ panel 1: when water comes, when the farms need it
def panel_timing(pg, R, x, y, w, h):
    L = R["lands"]; mix = R["design"]["mix"]
    rc = R["rain_credit_pct"]; rv = [rc[c] for c in ["olive"] + [m.split()[-1] for m in R["farm_demand_m3"]]]
    panel_title(pg, x, y + h, w, "1", "When water comes, when the farms need it",
                "need m³/month · %.1f ha · drip %s · rain held %.0f-%.0f %% of crop use %s"
                % (L["cropland_ha"] + L["orchard_ha"], cite("fao_tm4"), min(rv), max(rv), cite("fao56", "fao_t")))
    cx, cw = x + 16, w - 24
    cy = y + 31; ch = (y + h - 14) - cy
    dem_n = R["farm_demand_month_m3"][mix]["mean"]; dem_d = R["farm_demand_month_m3"][mix]["dry5"]
    vmax = nice(max(dem_n + dem_d) * 1.05)
    bw = cw / 12.0
    yr = max(sum(dem_n), 1); jun_sep = sum(dem_n[5:9])
    # the four summer months: one band through the chart and the stream / site / strip rows
    bx0, bx1 = cx + 5 * bw, cx + 9 * bw
    pg.rect(bx0, y + 1.0, bx1 - bx0, cy + ch + 5.5 - (y + 1.0), fill=C["accent_tint"])
    for j in range(6):
        t = vmax * j / 5.0; yy = cy + ch * t / vmax
        pg.line([(cx, yy), (cx + cw, yy)], C["faint"], 0.15)
        pg.text(fmt(t), cx - 1.5, yy - 1, 7, C["ink2"], align="R")
    for m in range(12):
        x0 = cx + m * bw
        pg.rect(x0 + bw * 0.14, cy, bw * 0.34, ch * dem_n[m] / vmax, fill=C["accent"])
        pg.rect(x0 + bw * 0.50, cy, bw * 0.34, ch * dem_d[m] / vmax, fill=C["accent_deep"])
        pg.text(MON[m], x0 + bw / 2, cy - 4, 7.5, C["ink"], True, "C")
    inline(pg, (bx0 + bx1) / 2.0 - inline_w([("%d %%" % round(100.0 * jun_sep / yr), 10, 0, True), (" of the need", 7.5, 0, True)]) / 2.0,
           cy + ch + 1.6, [("%d %%" % round(100.0 * jun_sep / yr), 10, C["accent_deep"], True), (" of the need", 7.5, C["accent_deep"], True)])
    ry = cy - 12
    pg.text("Stream", cx - 1.5, ry + 1, 7.5, C["water_deep"], True, "R")
    pg.text(cite("dsi", "rg"), cx + cw + 1, ry + 0.3, 7, C["water_deep"])
    for m in range(12):
        v = R["river_month_m3"][m]; x0 = cx + m * bw
        if v > 0:
            pg.rect(x0 + 0.6, ry - 1.2, bw - 1.2, 5.2, fill=C["water"])
            pg.text("%.1fM" % (v / 1e6), x0 + bw / 2, ry + 0.3, 7, C["white"], True, "C")
        else:
            pg.text("0", x0 + bw / 2, ry + 0.3, 7, C["ink2"], False, "C")
    sy = ry - 7; ty = sy - 6
    pg.text("Site", cx - 1.5, sy + 0.3, 7.5, C["green_mid"], True, "R")
    pg.text("Strip", cx - 1.5, ty + 0.3, 7.5, C["water_deep"], True, "R")
    for m in range(12):
        x0 = cx + m * bw
        pg.text(k_(R["site_month_m3"][m]), x0 + bw / 2, sy + 0.3, 7, C["green_mid"], False, "C")
        v = R["strip_month_m3"][m]
        pg.text(k_(v) if v else "stream", x0 + bw / 2, ty + 0.3, 7, C["water_deep"], False, "C")
    lx = x + w - 2 - inline_w([("mean year", 7, 0, False), ("1 in 5 dry", 7, 0, False)]) - 2 * 4.5 - 6
    pg.rect(lx, y + h - 0.4, 3, 3, fill=C["accent"]); ex = inline(pg, lx + 4.5, y + h, [("mean year", 7, C["ink"], False)])
    pg.rect(ex + 6, y + h - 0.4, 3, 3, fill=C["accent_deep"]); pg.text("1 in 5 dry", ex + 10.5, y + h, 7)

# ------------------------------------------------------------------ panel 2: what the site can catch
def panel_catch(pg, R, x, y, w, h):
    panel_title(pg, x, y + h, w, "2", "What the site can catch", "m³ a year · mean of 34 years · cumulative %s" % cite("era5", "mgm"))
    steps = R["site_catch_steps"]; total = sum(s["m3_per_year"] for s in steps)
    take = R["design"].get("river_take_m3_per_year") or 0           # v3: the stream's part, on the same bar scale
    cum_prev = 0; bx = x + 44; bw = w - 44 - 20; vmax = nice(max(total + take, 1) * 1.1); yy = y + h - 15
    for s in steps:
        add = s["m3_per_year"]; cum = cum_prev + add
        pg.text(s["name"], x, yy + 1.2, 7.5, C["ink"], True)
        sk = {"Walk tops": " " + cite("dwa"), "Streamside walks": " " + cite("dwa"), "Retention terraces": " " + cite("abu")}.get(s["name"], "")
        lab = "%s m², %.2f m³/m²%s" % (fmt(s["m2"]), add / s["m2"] if s["m2"] else 0.0, sk)
        pg.text(lab, x, yy - 2.6, fit_size(lab, bx - x - 1.5, 7.0), C["ink2"])
        pg.rect(bx, yy - 2, bw * cum_prev / vmax, 6, fill=C["faint"])
        pg.rect(bx + bw * cum_prev / vmax, yy - 2, max(0.4, bw * add / vmax), 6, fill=C["green_mid"])
        pg.text("+" + fmt(add), bx + bw * cum / vmax + 1.5, yy - 0.2, 7.5, C["green_deep"], True)
        cum_prev = cum; yy -= 8                             # v3: rows 8 mm apart (were 10) to make room for the stream
    sh = [100.0 * total / d["mean"] for d in R["farm_demand_m3"].values() if d["mean"]]
    p1 = [("= %s m³ a year" % fmt(total), 11, C["green_deep"], True), (" from the site", 8.5, C["green_deep"], True)]
    p2 = [("= %.1f-%.1f %% of the farms' need" % (min(sh or [0]), max(sh or [0])), 8.5, C["green_deep"], True)]
    ey = yy + 0.5                                           # v3: was + 1.5 (rows 8 mm apart)
    if inline_w(p1 + p2) + 2 <= w:
        inline(pg, x, ey, p1 + [("  ", 8.5, C["ink"], False)] + p2); ey -= 8.5
    else:
        inline(pg, x, ey, p1); inline(pg, x, ey - 4.6, p2); ey -= 12.5
    if take:      # v3 (Aras 27 Oct, Prompt 4): what the STREAM gives, same units and bars; then the share left in it
        d = R["design"]; yy = ey + 1.0; xe = bx + bw * (total + take) / vmax
        pg.text("Selinos: winter flow we take", x, yy + 1.2, 7.5, C["water_deep"], True)
        lab = "Nov-Apr · %s m³ store %s" % (fmt(d["storage_m3"]), cite("dsi", "rg"))
        pg.text(lab, x, yy - 2.6, fit_size(lab, bx - x - 1.5, 7.0), C["ink2"])
        pg.rect(bx, yy - 2, bw * total / vmax, 6, fill=C["faint"])
        pg.rect(bx + bw * total / vmax, yy - 2, max(0.4, bw * take / vmax), 6, fill=C["water_deep"])
        pg.text("+" + fmt(take), xe + 1.5, yy - 0.2, 7.5, C["water_deep"], True)
        s_ = "%d %% of the water stored" % math.floor(d["river_take_share_pct"])
        if text_w(s_, 7, True) + 3.0 <= bw * take / vmax:          # inside the stream's bar, else after its figure
            pg.text(s_, xe - 1.5, yy + 0.2, 7, C["white"], True, "R")
        elif xe + 3.5 + text_w("+" + fmt(take), 7.5, True) + text_w(s_, 7, True) <= x + w:
            pg.text(s_, xe + 3.5 + text_w("+" + fmt(take), 7.5, True), yy - 0.2, 7, C["water_deep"], True)
        lo_l, mean_l = d["river_left_pct"]; yy -= 8
        pg.text("Left in the Selinos", x, yy + 1.2, 7.5, C["water_deep"], True)
        lab = "winter flow, worst case " + cite("dsi", "rg")
        pg.text(lab, x, yy - 2.6, fit_size(lab, bx - x - 1.5, 7.0), C["ink2"])
        sw = bw * 0.5                                               # 100 % of the stream's winter flow
        pg.rect(bx, yy - 1.0, sw, 4.0, fill=C["water_light"])
        pg.rect(bx, yy - 1.0, max(0.4, sw * (100.0 - mean_l) / 100.0), 4.0, fill=C["water_deep"])
        xd = bx + sw * (100.0 - lo_l) / 100.0                       # the driest year's take: a tick
        pg.line([(xd, yy - 1.8), (xd, yy + 3.8)], C["accent_deep"], 0.4)
        inline(pg, bx + sw + 1.5, yy + 0.2, [("%d %% stays" % math.floor(mean_l), 7.5, C["water_deep"], True),
                                            ("  driest year %d %%" % math.floor(lo_l), 7, C["accent_deep"], True)])
        ey = yy - 8.5
    # terraces: two drawn runoff bars (same figures, same source)
    icon(pg, "terrace", x, ey + 3.0, 6.0)
    inline(pg, x + 8, ey, [("Terraces: for the plants, not a supply ", 7.5, C["green_deep"], True), (cite("abu"), 7, C["ink2"], False)])
    for i, (lab, v, col) in enumerate((("without terraces", 20, C["structure"]), ("terraced slope", 4, C["green_mid"]))):
        ry = ey - 5.5 - i * 4.8
        pg.text(lab, x + 8, ry + 0.4, 7, C["ink"])
        pg.rect(bx, ry - 0.2, bw * 0.4 * v / 20.0, 3.0, fill=col)
        pg.text("%d %% let out" % v, bx + bw * 0.4 * v / 20.0 + 1.5, ry + 0.4, 7.5, C["ink"], True)

# ------------------------------------------------------------------ v3: how the stream behaves (the band beside the title)
STREAM_BAND = (116.0, 262.0, 272.0, 406.0, 289.0)   # chart x0 (the CARRIES column) - x1 (left column's edge), cut x0 - x1, heading y

def panel_stream(pg):
    """v3 (Aras 27 Oct, Prompt 4): the analysis that leads the sheet, read right after the title: the natural flow
    past the site by month, J-D as panel 1 (Dec-Apr dark; Jul-Sep marked dry, in panel 1's summer tint), and how high
    the stream rises on the surveyed upstream-entry cut at 1:500, true proportions (ground, Jan-Feb water, max 2017,
    Q100, Q500), a label column with leaders, the scale bar under it, the five cuts' Q500 range under the cut."""
    cx0, cx1, kx0, kx1, hy = STREAM_BAND
    pg.text("HOW THE STREAM BEHAVES", cx0, hy, 8, C["accent"], True)
    q = STREAM_MONTH_M3; yr = float(sum(q)); win = (0, 1, 2, 3, 11); dry = (6, 7, 8)
    inline(pg, cx0, hy - 3.7, [("natural flow past the site, million m³ a month · %.0f hm³ a year · " % (yr / 1e6), 7, C["ink2"], False),
                               ("Dec-Apr %.0f %%" % (100.0 * sum(q[m] for m in win) / yr), 7, C["water_deep"], True),
                               (" " + cite("flow"), 7, C["ink2"], False)])
    bw = (cx1 - cx0) / 12.0; by = 270.0; bh = 12.0; vmax = max(q) * 1.06
    pg.rect(cx0 + 6 * bw, by - 4.4, 3 * bw, bh + 6.4, fill=C["accent_tint"])        # Jul-Sep, as panel 1's summer band
    for m in range(12):
        x0 = cx0 + m * bw; hh = max(0.25, bh * q[m] / vmax)
        pg.rect(x0 + bw * 0.2, by, bw * 0.6, hh, fill=C["water_deep"] if m in win else C["water"])
        pg.text("%.2f" % (q[m] / 1e6), x0 + bw / 2, by + hh + 0.8, 7, C["ink2"], False, "C")
        pg.text(MON[m], x0 + bw / 2, by - 3.4, 7.5, C["ink"], True, "C")
    pg.line([(cx0, by), (cx1, by)], C["ink2"], 0.25)
    mx = cx0 + 7.5 * bw
    pg.text("JUL-SEP: TRICKLE OR DRY", mx, by + 11.6, 7, C["accent_deep"], True, "C")
    pg.text("%.0f %% of the year's flow" % (100.0 * sum(q[m] for m in dry) / yr), mx, by + 8.6, 7, C["ink"], False, "C")
    pg.text("gauges dry %d-%d days a year" % STREAM_DRY_DAYS, mx, by + 5.6, 7, C["ink2"], False, "C")
    # the cut: crisp analysis, true proportions, crop 4 m outside where Q500 meets the ground
    g, u0, lv = STREAM_CUT["ground"], STREAM_CUT["u0"], STREAM_CUT["levels"]
    kx = 1000.0 / STREAM_DEN; a5, b5 = lv[-1][2]
    i0 = max(0, int(math.floor(a5 - 4.0 - u0))); i1 = min(len(g) - 1, int(math.ceil(b5 + 4.0 - u0)))
    xl, xr = float(u0 + i0), float(u0 + i1); top = lv[-1][1] + 0.8
    inline(pg, kx0, hy - 3.7, [("how high it rises · upstream entry, surveyed cut · 1:%s · true proportions " % fmt(STREAM_DEN), 7, C["ink2"], False),
                               (cite("lev"), 7, C["ink2"], False)])
    oy = hy - 5.6 - top * kx                                 # the bed's y
    T = lambda u, v: (kx0 + (u - xl) * kx, oy + v * kx)
    pts = [T(u0 + i, min(g[i], top)) for i in range(i0, i1 + 1)]
    pg.poly(pts + [T(xr, -0.6), T(xl, -0.6)], fill=C["structure"], closed=True)      # cut ground (poché)
    d0, (a0, b0) = lv[0][1], lv[0][2]                        # Jan-Feb water in the bed
    wr = [T(u0 + i, min(g[i], d0)) for i in range(i0, i1 + 1) if a0 - 0.5 <= u0 + i <= b0 + 0.5]
    if len(wr) >= 2:
        pg.poly([(wr[0][0], T(0, d0)[1])] + wr + [(wr[-1][0], T(0, d0)[1])], fill=C["water_light"], closed=True)
    pg.line(pts, C["ink"], 0.35)
    cols = [(C["water"], 0.3, None, False), (C["water_deep"], 0.35, None, False), (C["accent"], 0.35, (1.2, 0.6), True),
            (C["accent_deep"], 0.45, None, True)]
    X1 = kx0 + (xr - xl) * kx; ly = -1e9
    for (nm, dv, (a, b)), (col, lw, dash, bold) in zip(lv, cols):
        pg.line([T(max(a, xl), dv), T(min(b, xr), dv)], col, lw, dash)
        yl = max(T(0, dv)[1] - 0.9, ly + 3.0); ly = yl                         # the label column, 3 mm apart
        pg.line([T(min(b, xr), dv), (X1 + 1.2, yl + 0.9), (X1 + 2.2, yl + 0.9)], col, 0.15)
        pg.text("%.2f %s" % (dv, nm), X1 + 2.6, yl, 7, col, bold)
    yb = T(0, -0.6)[1] - 3.4
    pg.text("right bank", kx0, yb, 7, C["ink2"], True)
    pg.text("left bank", X1, yb, 7, C["ink2"], True, "R")
    sx = X1 + 2.0                                            # scale bar 0-5-10 m under the label column
    for a, b, f in ((0, 5, C["ink"]), (5, 10, C["white"])):
        pg.rect(sx + a * kx, yb + 0.4, (b - a) * kx, 1.2, fill=f, stroke=C["ink"], lw=0.15)
    for v in (0, 5, 10):
        pg.text("%d" % v, sx + v * kx, yb - 2.6, 7, C["ink2"], False, "C")
    pg.text("m", sx + 10 * kx + 2.0, yb - 2.6, 7, C["ink2"])
    s_ = "Q500 %.1f-%.1f m above the bed at five surveyed cuts" % (min(CUT_Q500.values()), max(CUT_Q500.values()))
    if K4_Q100 > K4_RIGHT_BANK: s_ += " · K4: right bank floods from Q100"
    pg.text(s_ + " " + cite("lev"), kx0, yb - 3.8, 7, C["ink"])

# ------------------------------------------------------------------ panel 3: the sizing curve
def panel_curve(pg, R, x, y, w, h):
    mix = R["design"]["mix"]; crop = mix.split()[-1]
    panel_title(pg, x, y + h, w, "3", "Storage size against the farm need covered",
                "34 water years 1991-2025 · daily · cropland as %s %s · in: winter stream + site catch, strip first %s"
                % (crop, cite("era5", "fao56"), cite("dsi")))
    lgx = x + w - 52                                         # legend column right of the plot
    cx, cy = x + 16, y + 12; cw = lgx - 6 - cx; ch = (y + h - 10) - cy
    cc = R["curve_closed"][mix]; tick = nice(cc[-1][0] / 8.0); nt = int(math.ceil(cc[-1][0] / tick)); vmax = tick * nt
    for t in range(0, 101, 25):
        yy = cy + ch * t / 100.0; hl = t in (25, 50)
        pg.line([(cx, yy), (cx + cw, yy)], C["structure"] if hl else C["faint"], 0.3 if hl else 0.15, (1.2, 0.8) if hl else None)
        pg.text("%d %%" % t, cx - 1.5, yy - 1, 7, C["ink2"], hl, "R")
    for j in range(nt + 1):
        v = tick * j
        pg.text(fmt(v / 1000) + "k" if v else "0", cx + cw * v / vmax, cy - 4.5, 7, C["ink2"], False, "C")
    pg.text("storage, m³", cx + cw, cy - 9, 7, C["ink2"], False, "R")
    series = [(cc, 1, C["water_deep"], None, "closed store: median year"),
              (cc, 2, C["accent"], None, "closed store: 1 in 5 dry"),
              (R["curve_open"], 1, C["water_deep"], (1.4, 0.9), "open pond: median year"),
              (R["curve_open"], 2, C["accent"], (1.4, 0.9), "open pond: 1 in 5 dry")]
    for rows, col, colr, dash, lab in series:
        pg.line([(cx + cw * r[0] / vmax, cy + ch * min(r[col], 100.0) / 100.0) for r in rows], colr, 0.7, dash)
    xs = cx + cw * STRIP_TODAY / vmax
    pg.line([(xs, cy), (xs, cy + ch)], C["ink2"], 0.25, (0.6, 0.6))
    d = R["design"]
    xr = cx + cw * d["storage_m3"] / vmax; yr_ = cy + ch * min(d["covered_pct_1in5_dry"], 100.0) / 100.0
    pg.line([(xr, cy), (xr, yr_)], C["accent_deep"], 0.4, (0.8, 0.6))
    pg.poly([(xr - 1.8, yr_), (xr, yr_ + 1.8), (xr + 1.8, yr_), (xr, yr_ - 1.8)], fill=C["accent_deep"], closed=True)
    # labels last, each at the first free place (white field under it over the curves)
    place(pg, "today %s m³: the strip only" % fmt(STRIP_TODAY), [(xs + 1.2, cy + ch - 3, "L"), (xs + 1.2, cy + ch - 7, "L")], 7, C["ink2"], halo=True)
    s1 = "cost cut-off " + cite("ross"); s2 = "%s m³ = %.0f %%" % (fmt(d["storage_m3"]), d["covered_pct_1in5_dry"])
    for dx, al, dy in ((-2.5, "R", -5.0), (2.5, "L", -5.0), (-2.5, "R", -14.0)):
        b1 = tbox(s1, xr + dx, yr_ + dy, 8, True, al); b2 = tbox(s2, xr + dx, yr_ + dy - 3.8, 8.5, True, al)
        if not any(hit(b, o) for b in (b1, b2) for o in pg.boxes) and b1[3] < cy + ch and b2[1] > cy: break
    place(pg, s1, [(xr + dx, yr_ + dy, al)], 8, C["accent_deep"], True, halo=True)
    place(pg, s2, [(xr + dx, yr_ + dy - 3.8, al)], 8.5, C["accent_deep"], True, halo=True)
    for i, (rows, col, colr, dash, lab) in enumerate(series):
        lyy = y + h - 13 - i * 4.6
        pg.line([(lgx, lyy + 1), (lgx + 6, lyy + 1)], colr, 0.7, dash); pg.text(lab, lgx + 7.5, lyy, 7)
    icon(pg, "clock", lgx, y + h - 34, 5.5)
    pg.text("max 365 days", lgx + 7.5, y + h - 36.5, 8, C["ink"], True)
    pg.text("in store, then to the strip", lgx + 7.5, y + h - 40.3, 7, C["ink2"])

# ------------------------------------------------------------------ panel 4: cost per m3, where to stop
def panel_store(pg, R, x, y, w, h):
    L = R["lands"]
    panel_title(pg, x, y + h, w, "4", "Cost per m³: cheapest first, then stop",
                "US$/m³ delivered · log scale · capital 5 %/yr " + cite("suds"))
    na = {r["key"]: r for r in R["ladder_no_recharge"]}
    rows = [("Aquifer recharge", "winter water into the alluvium " + cite("ross"), RECHARGE_USD[0], RECHARGE_USD[1])]
    lab = dict(pond="%.1f ha, %s m³ at most" % (L["pond_land_ha"], fmt(L["pond_land_ha"] * 1e4 * POND_DEPTH * POND_USE)),
               crates="%s m² of walks" % fmt(L["walk_m2"] + L["riverside_walk_m2"]), cistern="0.12 m² of land per m³")
    for key, name, _, _ in BUILT:
        if key in na: rows.append((name, lab[key], na[key]["usd_per_m3_low"], na[key]["usd_per_m3_high"]))
    bx = x + 48; bw = w - 50
    lg = lambda v: (math.log10(min(max(v, 0.1), 100.0)) + 1) / 3.0          # 0.1 .. 100 US$ on a log axis
    top = y + h - 16; rh = 8.5; n = len(rows)
    for t in (0.1, 1, 10, 100):
        xx = bx + bw * lg(t)
        pg.line([(xx, top + 3), (xx, top - n * rh + 1)], C["faint"], 0.15)
        pg.text(("$%g" % t), xx, top - n * rh - 2.5, 7, C["ink2"], False, "R" if t == 100 else "C")
    a0, a1 = ALTERNATIVE_USD
    pg.rect(bx + bw * lg(a0), top - n * rh + 1, bw * (lg(a1) - lg(a0)), n * rh + 2, fill=C["water_light"])
    pg.text("recycled water " + cite("ross"), bx + bw * lg(a0), top + 4.2, 7, C["water_deep"], True)
    for i, (nm, ld, lo, hi) in enumerate(rows):
        yy = top - i * rh
        pg.text(nm, x, yy, 7.5, C["ink"], True); pg.text(ld, x, yy - 3.2, fit_size(ld, bx - x - 1.5, 7.0), C["ink2"])
        pg.rect(bx + bw * lg(lo), yy - 1.5, max(0.8, bw * (lg(hi) - lg(lo))), 4, fill=C["green_mid"] if hi < a0 else C["accent"])
    ky = top - n * rh - 7.5                                  # colour key, then the result
    pg.rect(x, ky - 0.4, 3, 3, fill=C["green_mid"]); ex = inline(pg, x + 4.5, ky, [("cheaper than recycled", 7, C["ink"], False)])
    pg.rect(ex + 5, ky - 0.4, 3, 3, fill=C["accent"]); pg.text("dearer", ex + 9.5, ky, 7)
    lo_, hi_ = R["design"]["central_range_m3"]
    cheap = [r[0] for r in rows if r[3] < a0]
    inline(pg, x, ky - 6.0, ([] if cheap else [("nothing cheaper · ", 7.5, C["accent_deep"], True)]) +
           [("recharge pays up to ", 7.5, C["accent_deep"], True), ("%s m³" % span(lo_, hi_), 9, C["accent_deep"], True)])
    icon(pg, "cube", x, ky - 8.6, 4.5)
    pg.text("recharge fails tests: built > recycled, every step " + cite("suds"), x + 6, ky - 11.8, 7, C["ink2"])

# v2.7: layout of the sheet (x, y bottom, w, h in mm, y up), shared with the booklet crops (booklet_export).
# Reading order: header -> THE ANSWER (focal, top left) -> the farms (top right) -> 1 timing | 2 catch -> 3 curve | 4 cost.
FARMS = (272.0, 262.0, 134.0, 60.0)              # the farm tiles (2 x 2): x, y top, w, h
PANELS = dict(answer=(14, 202, 248, 60), timing=(14, 100, 248, 82), catch=(272, 100, 134, 82),
              curve=(14, 14, 248, 72), store=(272, 14, 134, 72))


def build(path, R):
    """The A3 sheet; returns the list of overlapping labels (empty = none)."""
    L = R["lands"]
    pg = Page(420.0, 297.0)
    pg.rect(0, 0, 420, 297, fill=C["white"])               # v2.7: white sheet (Aras 27 Oct 11:07)
    del SRC_KEY[:]                                        # v2.4: [n] numbers restart on every run
    pg.text("THE WATER BALANCE", 14, 280, 22, C["ink"], True)
    pg.text("Farm water · what our system can carry", 14, 272.5, 11, C["ink2"])
    pg.text("lands option %s · run %s" % (L["option"], R["run_time"]), 14, 266.5, 7, C["ink2"])
    panel_answer(pg, R, *PANELS["answer"])
    fx, fyt, fw, fh = FARMS
    tw_, th_ = (fw - 3.0) / 2.0, (fh - 3.0) / 2.0
    for i, (kind, head, big, foot) in enumerate((
            ("field", "Cropland", "%.1f ha" % L["cropland_ha"], "satellite " + cite("esa")),
            ("olive", "Orchard", "%.1f ha" % L["orchard_ha"], "satellite " + cite("esa")),
            ("sun", "Need: ET0, normal", "%s mm/yr" % fmt(ET0_NORMAL), "daily · drip " + cite("fao56", "mgm")),
            ("strip", "Strip, sealed", "%s m²" % fmt(L["strip_m2"]), "low-flow strip"))):
        tile(pg, kind, fx + (i % 2) * (tw_ + 3.0), fyt - (i // 2) * (th_ + 3.0), tw_, th_, head, big, foot)
    panel_timing(pg, R, *PANELS["timing"])
    panel_catch(pg, R, *PANELS["catch"])
    panel_curve(pg, R, *PANELS["curve"])
    panel_store(pg, R, *PANELS["store"])
    panel_stream(pg)                                      # v3: drawn last, so the [n] of panels 1-4 stay as in v2.7
    for k in SOURCES:                                     # v2.4: one numbered source key (no source can drop out)
        if k not in SRC_KEY: SRC_KEY.append(k)
    # v2.7: no source footer on the sheet (Aras 27 Oct 11:07); the key stays as INVISIBLE text so the booklet's
    # sources page (bergama_booklet sheet_sources: "Sources by number:") still lists what the [n] marks refer to
    pg.para("Sources by number: " + "  ".join("[%d] %s" % (i + 1, SOURCES[k]) for i, k in enumerate(SRC_KEY)) +
            "  Calculations: research/water_balance/NOTES.md.", 14, 8, 392, 6, C["ink2"], hidden=True)
    write_pdf(pg, path)
    return overlaps(pg)

# ------------------------------------------------------------------ v2.6: A3 booklet = crops of this sheet (booklet/CROP_SPEC.md)
# ---- A3 booklet assets (SCRIPT_STANDARD §8; booklet/ASSET_SPEC.md) ----
# Each booklet frame = one text-free vector PDF drawn at the frame's size + its words as labels in blocks.json.
# The assembler (bergama_booklet) sets every label as live text in the booklet font, never below 7 pt.
BK_MIN_PT = 7.5                              # labels and captions on the booklet (brief: 7-8 pt, minimum 7)
BK_CAPTION_MM = 5.0                          # caption line under every drawing frame


def bk_frame(key, w_default, h_default):
    """(w, h) mm a drawing for asset key "<folder>/<block>" is drawn at: the assembler's booklet_slots.json if it has
    run once, else the defaults given (the plan's frame size). h excludes the caption line."""
    try:
        import json as _j
        with open(bg_first([os.path.join(bg_booklet(""), "booklet_slots.json"),        # 27 Oct: cached/booklet/
                            os.path.join(bg_output("bergama_booklet"), "booklet_slots.json")]), encoding="utf-8") as f:
            s = _j.load(f)[key]
        return float(s["w_mm"]), float(s["h_mm"]) - BK_CAPTION_MM
    except Exception:
        return float(w_default), float(h_default) - BK_CAPTION_MM


def bk_take_text(items, H):
    """Page items (poly/line/circle/text tuples, y up from the bottom, mm) -> (items without text, labels).
    Labels: x, y in mm from the top-left (y to the baseline), size raised to BK_MIN_PT, colour hex."""
    keep, labels = [], []
    for it in items:
        if it[0] != "text":
            keep.append(it)
            continue
        _, s, x, y, size, color, bold, align = it[:8]
        labels.append({"x": round(x, 2), "y": round(H - y, 2), "text": s, "size": max(float(size), BK_MIN_PT),
                       "bold": bool(bold), "anchor": align or "L", "colour": color if isinstance(color, str) else "4A3F35"})
    return keep, labels


class BkBlocks(object):
    """Collects one script's booklet blocks and writes cached/booklet/<folder>/blocks.json (27 Oct, Aras: output/ holds
    final PDFs only; was output/<folder>/booklet/). out_dir = the script's output folder; its name is the folder key."""
    def __init__(self, out_dir, script, version):
        self.dir = bg_booklet(os.path.basename(os.path.normpath(out_dir)))
        os.makedirs(self.dir, exist_ok=True)
        self.d = {"script": script, "version": version, "sources": {}, "blocks": {}}

    def path(self, name):
        return os.path.join(self.dir, name)

    def source(self, key, text, url):
        """A public source: used in any text as {src:key}; numbered once for the whole booklet."""
        self.d["sources"][key] = {"text": text, "url": url}

    def drawing(self, bid, pdf_name, labels, caption="", scale_den=None, legend=None):
        self.d["blocks"][bid] = {"type": "drawing", "pdf": pdf_name, "page": 0, "labels": labels, "caption": caption,
                                 "scale_den": scale_den, "legend": legend or []}

    def crop(self, bid, pdf_name, rect_mm, caption="", scale_den=None, legend=None, page=0, drop=None):
        """A booklet drawing taken from this script's own sheet (Aras 25 Oct 21:47: the booklet shows the sheet's
        drawing, re-laid): pdf_name = the sheet PDF in this script's output folder, rect_mm = (x0, y0, x1, y1) of the
        panel in mm from the sheet page's top-left (y down), scale_den = the sheet's scale at 1:1 print (None if not to
        scale). The assembler scales the crop to its frame and resets the sheet's words inside it as live labels;
        drop = regexes of sheet texts not to carry."""
        self.d["blocks"][bid] = {"type": "crop", "pdf": pdf_name, "page": page,
                                 "rect_mm": [round(float(v), 2) for v in rect_mm], "caption": caption,
                                 "scale_den": scale_den, "legend": legend or [], "drop": drop or []}

    def tiles(self, bid, tiles):
        self.d["blocks"][bid] = {"type": "tiles", "tiles": tiles}

    def text(self, bid, heading="", body="", bullets=None):
        self.d["blocks"][bid] = {"type": "text", "heading": heading, "body": body, "bullets": bullets or []}

    def save(self):
        import json as _j
        p = os.path.join(self.dir, "blocks.json")
        with open(p, "w", encoding="utf-8") as f:
            _j.dump(self.d, f, ensure_ascii=False, indent=1)
        return p

BK_DROP = [r"^\[\d+(,\d+)*\]$"]                      # the sheet's source numbers: the booklet has its own source list


def booklet_figures(R):
    """v2.5: figures the booklet prints that the sheet only computed inline (results JSON keys, read live)."""
    dn = R["farm_demand_month_m3"][R["design"]["mix"]]["mean"]
    R["jun_sep_share_of_need_pct"] = round(100.0 * sum(dn[5:9]) / max(sum(dn), 1), 1)
    sh = [100.0 * R["site_catch_m3_per_year"] / d["mean"] for d in R["farm_demand_m3"].values() if d["mean"]]
    R["site_catch_share_of_need_pct"] = [round(min(sh), 1), round(max(sh), 1)] if sh else [0.0, 0.0]


def booklet_export(R):
    """v2.6 (Aras 25 Oct 21:47): one crop per sheet panel in booklet/blocks.json; the assembler cuts each rect out of
    the sheet PDF (the booklet v9 places the whole sheet on p10; these crops stay for any re-laid page). v2.7: rects
    from the new FARMS / PANELS: each panel under its title and keyword line (7.5 mm under the title baseline)."""
    bk = BkBlocks(OUT_DIR, "WaterBalance", VERSION)
    H = 297.0

    def crop(bid, x0, y0, x1, y1, caption, legend=None):
        bk.crop(bid, OUT_PDF, (x0, H - y1, x1, H - y0), caption=caption, scale_den=None, legend=legend, drop=BK_DROP)
    x, y, w, h = PANELS["answer"]
    crop("wb_answer", x - 0.5, y - 0.5, x + w + 0.5, y + h + 0.5, "The answer: storage, what it carries, the cost cut-off")
    fx, fyt, fw, fh = FARMS
    crop("wb_tiles", fx - 0.5, fyt - fh - 0.5, fx + fw + 0.5, fyt + 0.5, "Farms, need and strip")
    x, y, w, h = PANELS["timing"]
    crop("wb_timing", x - 0.5, y - 0.5, x + w + 0.5, y + h - 7.5, "When water comes, when the farms need it",
         [dict(kind="fill", colour=C["accent"], label="need, mean year"), dict(kind="fill", colour=C["accent_deep"], label="need, 1 in 5 dry year"),
          dict(kind="fill", colour=C["water"], label="stream water")])
    x, y, w, h = PANELS["catch"]
    crop("wb_catch", x - 0.5, y - 0.5, x + w + 0.5, y + h - 7.5, "What the site can catch",
         [dict(kind="fill", colour=C["green_mid"], label="added by this surface"), dict(kind="fill", colour=C["faint"], label="caught so far"),
          dict(kind="fill", colour=C["water_deep"], label="taken from the stream")])
    cx0, cx1, kx0, kx1, hy = STREAM_BAND                  # v3: the stream band beside the title
    crop("wb_stream", cx0 - 0.5, 264.0, kx1 + 0.5, hy + 3.5, "How the stream behaves: the year, and how high it rises",
         [dict(kind="fill", colour=C["water_deep"], label="Dec-Apr"), dict(kind="fill", colour=C["water"], label="May-Nov"),
          dict(kind="fill", colour=C["accent_tint"], label="Jul-Sep, dry")])
    x, y, w, h = PANELS["curve"]
    crop("wb_curve", x - 0.5, y - 0.5, x + w + 0.5, y + h - 7.5, "Storage size against the farm need covered")
    x, y, w, h = PANELS["store"]
    crop("wb_store", x - 0.5, y - 0.5, x + w + 0.5, y + h - 7.5, "Cost per m³ delivered, log scale")
    return bk.save()

# ------------------------------------------------------------------ run (GH Button on any input, ScriptEditor, or python)
def main(g):
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    L, src = get_lands(g)
    R = compute(L); R["lands_source"] = src
    bk_err = None
    try:
        booklet_figures(R)                                # v2.5: new results keys for the booklet
    except Exception as ex:
        bk_err = "%s: %s" % (type(ex).__name__, ex)
    path = os.path.join(OUT_DIR, OUT_PDF)
    try:
        ov = build(path, R)                               # v2.7: labels whose boxes overlap (none expected)
    except PermissionError:
        return "The PDF is open in another program. Close it and press again: " + path
    os.makedirs(RES_DIR, exist_ok=True)
    with open(os.path.join(RES_DIR, OUT_JSON), "w", encoding="utf-8") as f:
        json.dump(R, f, indent=1, ensure_ascii=False)
    if bk_err is None:
        try:
            booklet_export(R)                             # v2.5: a booklet error never breaks the sheet; it goes in the log
        except Exception as ex:
            import traceback as _tb
            bk_err = "%s: %s %s" % (type(ex).__name__, ex, _tb.format_exc()[-300:])
    d = R["design"]; tm = time.strftime("%H:%M:%S")
    return "%s  %s\n%s  %s\ncut-off %s m3 = %.1f %% (1 in 5 dry)\nstream: %s m3 a year taken = %.1f %% of the water stored; %.1f %% of its winter flow left (driest year %.1f %%)\n%s %s, %.1f s" % (
        OUT_PDF, tm, OUT_JSON, tm, fmt(d["storage_m3"]), d["covered_pct_1in5_dry"], fmt(d["river_take_m3_per_year"]),
        d["river_take_share_pct"], d["river_left_pct"][1], d["river_left_pct"][0], "water balance", VERSION, time.time() - t0) + (
        "\nbooklet ERROR: " + bk_err if bk_err else "") + (
        "\nLABEL OVERLAP (%d): %s" % (len(ov), "; ".join(ov[:6])) if ov else "\nlabels: no overlaps") + "".join(
        "\n" + t for t in bg_tidy_output("Bergama_water_balance_analysis"))     # 27 Oct: output/ = PDFs only

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
        _sc.sticky["bergama_water_balance_log_ver" + _ik] = VERSION
    if _sc.sticky.get("bergama_water_balance_log_ver" + _ik) != VERSION:   # v3 (Aras 27 Oct 15:35): a newly pasted version
        for _s in ("", "_status", "_done"):                                 # shows itself at once, idle, without the old
            _sc.sticky.pop("bergama_water_balance_log" + _s + _ik, None)     # run's time or log
    done = _sc.sticky.get("bergama_water_balance_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_water_balance_log" + _ik, "Press the Button to compute and export to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "WaterBalance " + VERSION + " · " + _sc.sticky.get("bergama_water_balance_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main(globals())))
