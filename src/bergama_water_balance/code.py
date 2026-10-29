# bergama_water_balance_v6.py (v6, 29 Oct: revision T3b, the year as one G7 chart, the zones for p.12; v5, 28 Oct: MIRAQUA revision, the sheet in reading order; v4.1, 27 Oct: m² / m³ / hm³ drawn as raised digits; v4: the design store's normal and dry year in the results; v3 sheet kept) · Thread 2 of the 22 Oct batch: water balance (demand, collection, storage, cost cut-off)
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

VERSION = "v6"
# NEW IN v6 (revision 29 Oct 2026, T3b WO-T3b-2, package C items 1-4 and G7; a feature change, so the next whole
#   number). Pages 11-12 are one story: p.12 (water board) is now one diagrammatic water map, so the analysis it shows
#   left this sheet, and what stays is drawn per G7 (R31: every user its own row, one common time axis, bars):
#   * block 1 "One year of water": the stream, the site catch, the store, the summer strip and the farms as five rows of
#     icons.py pictograms and bars on ONE month axis (replaces the question, the farm tiles, the monthly chart with its
#     number rows, and the stream's monthly flow). The store's monthly level is new: results key
#     design.store_month_m3 (run_storage now records the level, `lev`; store_months()).
#   * gone from the sheet: the site-catch bars (block 4; its figures are on the p.12 map, results keys unchanged), the
#     1:500 flood cut (the flood levels belong to the sections, p.13), the open-pond curves, the claims column.
#   * blocks 2 storage curve, 3 cost, 4 the answer with ONE short conclusion paragraph; icons from common/icons.py
#     (the sheet's own icon() and tile() are gone); crops wb_year, wb_curve, wb_store, wb_answer (wb_tiles,
#     wb_timing, wb_catch, wb_stream removed).
#   * results key "zones" (new): the Option A zones and water links in survey m (zone base layers of the open Rhino file,
#     else the built-in copy data/ZONE_COPY.py), read by the water board's p.12 map. Every other key unchanged.
# NEW IN v5 (MIRAQUA 28 Oct, booklet revision v4: P11.1, P11.2, G3/G5/G11/G13; bank depth research 28 Oct §4.3; a
#   feature change, so the next whole number):
#   * The sheet re-laid in reading order: 1 the question, 2 how the stream behaves, 3 what the farms need, 4 what the
#     site can catch, 5 storage size, 6 cost, 7 the answer (a light water-tint band, not the dark block).
#   * Bold keywords in every block line; DSİ with its İ; corn (not maize); heights with 2 decimals; the 1:500 cut's
#     scale bar in cm; land areas in ha on the whole sheet (Aras 28 Oct 13:21), the cistern's land per m³ in m².
#   * "K4: right bank floods from Q100" left out (the survey shows K4 before the DSİ walls); no internal file name in
#     the sources. Every number is computed as before.
# NEW IN v4.1 (bugfix, Aras 27 Oct, Prompt 8 final check): ² and ³ on the sheet are drawn as a raised small 2 or 3
#   (0.6 x the size, as the water board v3.1 and agriculture v3 do; see SUP): the unembedded Helvetica's ²/³ glyph was
#   missing in some viewers ("hm" for "hm³"). The invisible source key names only public sources (no internal research
#   file names: "Calculations: research/water_balance/NOTES.md", "rain_river_levels README / table A2 / A3s" gone).
#   Layout, figures and the results JSON unchanged.
# v4 (Aras 27 Oct 17:35, booklet Prompt 6 "water, part 3", p24: "show the defence ON the board ... normal year vs dry
#   year as two stacked bars"): the results JSON gains design.year_split, the design store through two real water years
#   of the same daily run: "normal" = the year whose farm need is nearest the median, "dry5" = the 1-in-5 dry year
#   (farm_demand_m3 dry5_year). Each: carried in (Oct 1), filled that year (stream + site catch), the strip's draw and
#   need, the farms' draw and need, released after 365 days, carried out (Sep 30), and the stream's winter water that
#   year as % of a median year. run_storage also counts per water year what it lets go after 365 days and the store
#   at the year's end (the store is closed, no evaporation: carried in + filled = strip + farms + released + carried
#   out). The agriculture sheet draws it. The sheet and every other key are unchanged.
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
#@include ../common/bergama_paths.py
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
# v6 (T3b): the 1:500 upstream-entry flood cut (STREAM_CUT, CUT_Q500, K4_RIGHT_BANK, K4_Q100, STREAM_DEN) left the
# sheet: flood levels belong to the sections (p.13, the level table), not to the water balance

#@include data/INPUT_DATA.py
# v6 (T3b WO-T3b-2): ZONE_COPY = the Option A zones and links of zone base v7 (the masterplan's data/ZONE_COPY.py,
# md5 7c7d4a4a21af391460ac0701ae5e3902, Option A only, rings thinned to 10 cm), JSON {zones: [{code, label, id,
# study_area, zone, ring}], links: [{kind, label, P}]}, zlib + base64; used when the open Rhino file has no zones
#@include data/ZONE_COPY.py

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

# ------------------------------------------------------------------ v6: the project's zones and links, for p.12's map
ZONE_CODES = ("WS", "WT", "WD", "GR", "WA", "WP", "DG")    # retention terraces, reed basins, spillway, walks / dry tops,
                                                          # bed + flood terraces, streamside planting, Demeter's Garden

def ring_area(P):
    return abs(sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))) / 2.0

def rhino_zones(option):
    """v6: (zones, links) of Option_<option> in the open Rhino file, survey m: closed curves on INT_ZONE_<code> and
    INT_WATER_strip (code "STRIP"), with the zone base's user text (label, id, study_area, zone); INT_LINK_<kind>
    curves as start -> end. None when not in Rhino or the file has none."""
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
    except Exception:
        return None
    if doc is None:
        return None
    s = Rhino.RhinoMath.UnitScale(doc.ModelUnitSystem, Rhino.UnitSystem.Meters)
    parent = "Option_" + option + "::"
    zones, links = [], []
    for o in doc.Objects.GetObjectList(Rhino.DocObjects.ObjectType.Curve):
        path = doc.Layers[o.Attributes.LayerIndex].FullPath
        if not path.startswith(parent):
            continue
        lay = path[len(parent):].split("::")[0]
        g, a = o.Geometry, o.Attributes
        meta = dict((k, a.GetUserString(k)) for k in ("label", "id", "study_area", "zone") if a.GetUserString(k))
        meta.setdefault("label", a.Name or "")
        if lay.startswith("INT_LINK_"):
            p0, p1 = g.PointAtStart, g.PointAtEnd
            links.append(dict(kind=lay[len("INT_LINK_"):], label=meta["label"],
                              P=[[round(p0.X * s, 2), round(p0.Y * s, 2)], [round(p1.X * s, 2), round(p1.Y * s, 2)]]))
            continue
        code = "STRIP" if lay == "INT_WATER_strip" else (lay[len("INT_ZONE_"):][:2].upper() if lay.startswith("INT_ZONE_") else None)
        if code not in ZONE_CODES + ("STRIP",) or not g.IsClosed:
            continue
        pts = None
        try:
            ok, pl = g.TryGetPolyline()
            if ok:
                pts = [(p.X, p.Y) for p in pl]
        except Exception:
            pts = None
        if not pts:                                     # a smooth curve: points about every 50 cm
            ts = g.DivideByCount(max(8, min(800, int(g.GetLength() * s / 0.5))), True) or []
            pts = [(g.PointAt(t).X, g.PointAt(t).Y) for t in ts]
        if len(pts) > 1 and pts[0] == pts[-1]:
            pts = pts[:-1]
        if len(pts) < 3:
            continue
        ring = [[round(x * s, 2), round(y * s, 2)] for x, y in pts]
        zones.append(dict(meta, code=code, ring=ring, m2=round(ring_area(ring), 1)))
    return (zones, links) if zones else None

def get_zones(option="A"):
    """v6: the results key "zones": the open Rhino file's Option A zones when it has the reed basins, else the
    built-in copy (data/ZONE_COPY.py); the water board's p.12 water map reads it."""
    rz = rhino_zones(option)
    if rz and any(z["code"] == "WT" for z in rz[0]):
        zs, ls, src = rz[0], rz[1], "rhino option " + option
    else:
        d = json.loads(zlib.decompress(base64.b64decode("".join(ZONE_COPY))).decode("utf-8"))
        zs, ls, src = d["zones"], d["links"], "built-in copy (zone base v7, option A)"
        for z in zs:
            z["m2"] = round(ring_area(z["ring"]), 1)
    return dict(source=src, option=option, zones=zs, links=ls,
                note="survey m; zones: INT_ZONE_<code> and INT_WATER_strip (code STRIP); links: INT_LINK_<kind>, start -> end")

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

def run_storage(V, A, demand, strip, inflow, et0, days, reserve, max_age=MAX_AGE, site=None, lev=None):
    """v3: with site (the site catch each day) also counts per water year the stream's part of what enters the
    store (per[y][4]) and all that enters it (per[y][5]): the site catch fills first, the stream tops up.
    v6: with lev (a list) the store's level at the end of every day is appended to it."""
    Q = deque(); S = 0.0; flushed = 0.0; oldest = 0
    per = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])   # v4: [6] released after max_age, [7] store at the end
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
            flushed += Q[0][1]; per[wy(d)][6] += Q[0][1]; S -= Q[0][1]; Q.popleft()
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
        r = per[wy(d)]; r[0] += demand[i]; r[1] += gf; r[2] += strip[i]; r[3] += gs; r[7] = S
        if lev is not None: lev.append(S)
    return per, flushed, oldest

def store_months(V, demand, strip, R, site, et0, days, reserve):
    """v6 (T3b, G7): the closed design store V through the same daily run as year_split: its mean level at the end of
    each calendar month, m3, Jan-Dec (the first water year, the spin-up, left out). Sheet block 1, the store's row."""
    inflow = [min(V / INTAKE_DAYS, r) + s for r, s in zip(R, site)]
    lev = []
    run_storage(V, 0.0, demand, strip, inflow, et0, days, reserve, lev=lev)
    y0 = wy(days[0]); acc = defaultdict(list)
    for i, d in enumerate(days):
        if wy(d) == y0: continue
        if i + 1 == len(days) or days[i + 1].month != d.month: acc[d.month].append(lev[i])
    return [round(sum(acc[m]) / len(acc[m])) if acc[m] else 0 for m in range(1, 13)]

def crf(r, n): return r * (1 + r) ** n / ((1 + r) ** n - 1)

def year_split(V, demand, strip, R, site, et0, days, reserve, avail, fd):
    """v4 (Aras 27 Oct, Prompt 6): the closed store V (no open water, so no evaporation) through two water years of one
    daily run: "normal" = the year whose farm need is nearest the median, "dry5" = the 1-in-5 dry year of the farm need
    (fd["dry5_year"]; the nearest year when that is the spin-up year). m3 per water year (Oct-Sep):
    carried in + filled = strip + farms + released + carried out."""
    inflow = [min(V / INTAKE_DAYS, r) + s for r, s in zip(R, site)]
    per, _, _ = run_storage(V, 0.0, demand, strip, inflow, et0, days, reserve, site=site)
    ys = sorted(per)
    start = {y: (per[ys[k - 1]][7] if k else 0.0) for k, y in enumerate(ys)}
    ys = ys[1:]                                             # the first water year is the spin-up (the store starts empty)
    near = lambda v: min(ys, key=lambda y: abs(per[y][0] - v))
    yd = fd["dry5_year"] if fd.get("dry5_year") in ys else near(fd["dry5"])
    yn = near(fd["median"])
    a_med = sorted(avail[y] for y in ys)[len(ys) // 2]
    out = {}
    for k, y in (("normal", yn), ("dry5", yd)):
        r = per[y]
        out[k] = dict(water_year="%d-%02d" % (y - 1, y % 100), carried_in_m3=round(start[y]), filled_m3=round(r[5]),
                      strip_m3=round(r[3]), strip_need_m3=round(r[2]), farms_m3=round(r[1]), farm_need_m3=round(r[0]),
                      released_m3=round(r[6]), carried_out_m3=round(r[7]),
                      winter_flow_pct_of_median=round(100.0 * avail[y] / max(a_med, 1.0), 1))
    out["storage_m3"] = int(V)
    out["note"] = "closed store, one daily run; normal = median farm-need year, dry5 = 1-in-5 dry year of the farm need"
    return out

def compute(L):
    I = load_inputs(); days, P, E, R = I["days"], I["P"], I["E"], I["R"]
    nY = len(set(wy(d) for d in days))
    crops = ["olive"] + [c.strip().lower() for c in L["cropland_crops"].split(",") if c.strip().lower() in CROP_SOIL and c.strip().lower() != "olive"]
    crops = list(dict.fromkeys(crops))
    if len(crops) == 1: crops.append("cotton")
    irr = {c: soil_irrigation(c, I) for c in set(crops) | set(CROP_SOIL)}
    res = dict(script="bergama_water_balance_v6.py", version=VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
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
    # v4 (Prompt 6): the design store through a normal and the 1-in-5 dry water year, from the same daily run
    res["design"]["year_split"] = year_split(dc["storage_m3"], dem[design], strip, R, site, E, days, RES, avail,
                                             res["farm_demand_m3"][design])
    res["design"]["store_month_m3"] = store_months(dc["storage_m3"], dem[design], strip, R, site, E, days, RES)   # v6
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
C["water_tint"] = "".join("%02X" % int(round(255 - 0.40 * (255 - int(C["water_light"][i:i + 2], 16)))) for i in (0, 2, 4))  # v5 (MIRAQUA 28 Oct, P11.1): water_light at 40 % on white, the answer's field
CROP_NAME = dict(maize="corn")            # v5 (MIRAQUA 28 Oct, G11): the name printed for a crop key (keys unchanged)

#@include ../common/rgb.py

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]

#@include ../common/text_w.py


#@include ../common/units.py


#@include ../common/icons.py


#@include ../common/pdf_fonts.py

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
# v4.1 (Aras 27 Oct, Prompt 8: "hm" for "hm³"): ² and ³ are drawn as the digit at 0.6 x the size, raised 0.28 x the
# size (then as wide as the ²/³ glyph, 333/1000), as water board v3.1: the unembedded Helvetica's ²/³ was missing in some viewers
SUP = {u"²": u"2", u"³": u"3"}
SUP_K, SUP_UP = 0.6, 0.28


def sup_runs(s):
    """v4.1: s cut into (text, raised) runs at ² and ³, which become a plain 2 or 3"""
    out, cur = [], u""
    for ch in s:
        if ch in SUP:
            if cur: out.append((cur, False))
            out.append((SUP[ch], True)); cur = u""
        else:
            cur += ch
    if cur: out.append((cur, False))
    return out


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
        if not hidden and any(ch in SUP for ch in s):   # v4.1 (Prompt 8): m² / m³ as a raised small digit (see SUP);
            runs = sup_runs(s)                          # the invisible source key keeps the glyph (the booklet reads it)
            ws = [text_w(t, size * (SUP_K if up else 1.0), bold) for t, up in runs]
            x0 = x - {"L": 0.0, "C": sum(ws) / 2.0, "R": sum(ws)}[align]; xx, n = x0, len(self.boxes)
            for (t, up), w_ in zip(runs, ws):
                self.text(t, xx, y + (size * SUP_UP * 0.3528 if up else 0.0), size * (SUP_K if up else 1.0), col, bold)
                xx += w_
            del self.boxes[n:]                          # one box for the whole label in the overlap check, as before
            self.boxes.append(tbox(s, x0, y, size, bold) + (s,))
            return
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
            "", ""]
    extra = []                                            # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py):

    def add(b):                                           # font file + descriptor go after the content (7, 8 ...)
        extra.append(b.decode("latin-1"))
        return 6 + len(extra)
    fid = pdf_fonts(add, ("R", "B"))
    objs[3], objs[4] = extra[fid[0] - 7], extra[fid[1] - 7]   # the font dicts themselves stay objects 4, 5
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
    for i, o in enumerate(objs):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (i + 1, o)).encode("latin-1")
    offs.append(len(out))
    out += ("6 0 obj\n<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(content)).encode("latin-1") + content + b"\nendstream\nendobj\n"
    for j, o in enumerate(extra):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (7 + j, o)).encode("latin-1")
    x = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(offs) + 1) + "".join("%010d 00000 n \n" % o for o in offs) +
            "trailer\n<< /Size %d /Root 1 0 R /Info << /Title (Bergama water balance) >> >>\nstartxref\n%d\n%%%%EOF\n" % (len(offs) + 1, x)).encode("latin-1")
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
    """v2.7: a supporting panel's head: a rule over the panel's width, number, title, keyword line.
    v5 (MIRAQUA 28 Oct, G5): the keyword line's **...** runs are set bold (rich_parts)"""
    pg.line([(x, y + 4.5), (x + w, y + 4.5)], C["structure"], 0.3)
    pg.text(n, x, y, 11, C["accent"], True)
    pg.text(title, x + 6.5, y, 11, C["ink"], True)
    if sub: inline(pg, x + 6.5, y - 4.8, rich_parts(sub, 7.5, C["ink2"], C["ink"]))


# v5 (MIRAQUA 28 Oct, G5): one or two bold keywords per explanatory line, written "a **key** word"
def rich_tokens(s):
    """'a **key** word.' -> [(text, bold)] cut at the spaces (each space its own token)"""
    out = []
    for i, t in enumerate(s.split("**")):
        for k, piece in enumerate(t.split(" ")):
            if k: out.append((" ", bool(i % 2)))
            if piece: out.append((piece, bool(i % 2)))
    return out


def rich_parts(toks, size, col, bcol=None):
    """tokens [(text, bold)] or a '**' string -> inline() parts, runs of one weight merged; bold runs in bcol"""
    if isinstance(toks, str): toks = rich_tokens(toks)
    parts = []
    for t, b in toks:
        if parts and parts[-1][3] == b:
            parts[-1] = (parts[-1][0] + t, size, parts[-1][2], b)
        else:
            parts.append((t, size, (bcol or col) if b else col, b))
    return parts


def rich_para(pg, s, x, y, w, size, col, bcol=None, lead=1.3):
    """a '**' string wrapped to w mm, line by line from baseline y; returns the next line's baseline"""
    words, cur = [], []
    for t in rich_tokens(s):
        if t[0] == " ":
            if cur: words.append(cur); cur = []
        else:
            cur.append(t)
    if cur: words.append(cur)
    lines, ln = [], []
    for wd in words:
        trial = ln + ([(" ", wd[0][1])] if ln else []) + wd
        if ln and inline_w(rich_parts(trial, size, col, bcol)) > w:
            lines.append(ln); ln = list(wd)
        else:
            ln = trial
    if ln: lines.append(ln)
    for ln in lines:
        inline(pg, x, y, rich_parts(ln, size, col, bcol)); y -= size * 0.3528 * lead
    return y

def arrow(pg, x0, x1, y, col, lw=0.6):
    pg.line([(x0, y), (x1 - 2.2, y)], col, lw)
    pg.poly([(x1 - 2.6, y + 1.5), (x1, y), (x1 - 2.6, y - 1.5)], fill=col, closed=True)

# ------------------------------------------------------------------ v2.4 visual first (SCRIPT_STANDARD 5b): [n] marks, pictograms, tiles
SOURCES = dict(    # every source and method sentence of the v2.3 sheet; v2.7: an invisible text layer (the booklet's sources page reads it)
    esa="ESA WorldCover 2021: farms = analysis area of the land-use map, unless changed",
    mgm="MGM/WMO 17742 normals 1991-2020",
    era5="Open-Meteo ERA5 daily 1991-2025 (scaled to the station)",
    dsi=u"DSİ gauges D04A053, D04A063 2016-2021, area-scaled",      # v5 (MIRAQUA 28 Oct, G3): DSİ with its İ
    fao56="FAO-56 (Allen et al. 1998): daily soil water balance, Penman-Monteith ET0",
    fao_t="FAO-56 Tables 19 and 22",
    fao_tm4="FAO Training Manual 4 (drip)",
    rg="RG 30802 minimum flow: stream counted above the legal minimum, worst case",
    ross="Ross & Hasnain 2018",
    suds="UK EA 2015 and Royal Haskoning 2012 SuDS costs (GBP x 1.25)",
    flow=u"Natural flow past the site = DSİ gauges D04A053 + D04A063, Oct 2015-Sep 2021, "   # v4.1 (Prompt 8): no internal file names
         u"each area-scaled to 101 km², mean of the two (upper case: the Kestel diversion not counted); both gauges fully dry 0-111 days a year")
# v6 (T3b): "dwa", "abu" (the site-catch block) and "lev" (the flood cut) left with what cited them
SRC_KEY = []

def cite(*keys):
    """v2.4: "[n]" (or "[n,m]") for sources in SOURCES; the numbered key is the sheet's hidden source layer (v2.7)."""
    for k in keys:
        if k not in SRC_KEY: SRC_KEY.append(k)
    return "[" + ",".join(str(SRC_KEY.index(k) + 1) for k in keys) + "]"

def ico(pg, name, cx, cy, size):
    """v6 (T3b, 02 §2): an icon of the booklet's one set (common/icons.py) centred on (cx, cy), size mm square; the
    sheet's own 10 x 10 pictograms (icon, tile) are gone"""
    for sh in ico_draw(name, cx, cy, size):
        if sh[0] == "poly":
            if sh[2] or sh[3]:
                pg.poly(sh[1], sh[2], sh[3], sh[4], True)
        else:
            pg.line(sh[1], sh[2], sh[3])

def inline(pg, x, y, parts):
    """v2.4: a keyword row: parts = [(text, size, colour, bold)] set one after another; returns the end x."""
    for s, size, col, bold in parts:
        pg.text(s, x, y, size, col, bold); x += text_w(s, size, bold)
    return x

def inline_w(parts):
    return sum(text_w(s, size, bold) for s, size, col, bold in parts)

def span(a, b, f=fmt):
    return f(a) if a == b else "%s-%s" % (f(a), f(b))

# ------------------------------------------------------------------ 7 THE ANSWER: the conclusion (store -> carries -> cut-off)
def panel_answer(pg, R, x, y, w, h):
    """The answer, read left to right: how much storage, what it carries, where cost stops it; our claims beside it.
    Every figure from R (results JSON): design.central_range_m3 / _pct_1in5_dry, full_range_*, need_for_target_1in5_dry_m3,
    today_strip_storage; prices RECHARGE_USD / ALTERNATIVE_USD (Ross & Hasnain 2018).
    v5 (MIRAQUA 28 Oct, P11.1/P11.2): block 7, the sheet's last: its numbered title, then a LIGHT tint field (water_tint;
    was the dark water_light block at the top); one row: store -> carries -> cost cut-off | our claims.
    v6 (T3b): block 4; "our claims" became the one short conclusion paragraph (G7); the store's icon from icons.py."""
    d = R["design"]
    panel_title(pg, x, y + h, w, "4", "The answer")
    top = y + h - 7.0                                           # the tint field under the title
    pg.rect(x, y, w, top - y, fill=C["water_tint"])
    lo_, hi_ = d["central_range_m3"]; plo, phi = d["central_range_pct_1in5_dry"]
    ky, big_y, l1, l2 = top - 5.0, top - 13.5, top - 18.5, top - 22.5
    wa, wb, wc, gap = 84.0, 62.0, 62.0, 12.0
    # A: the store
    ax = x + 6; ico(pg, "storage", ax + 6.5, top - 10.5, 13)
    tx = ax + 17; tw = wa - 17
    pg.text("STORE", tx, ky, 8, C["ink2"], True)
    s = "%s" % span(lo_, hi_); fs = fit_size(s, tw, 22.0, True)
    pg.text(s, tx, big_y, fs, C["ink"], True)
    pg.text("m³ · aquifer recharge", tx, l1, 8.5, C["ink"], True)
    inline(pg, tx, l2, rich_parts("if **borehole tests** accept it", 7.5, C["ink2"], C["ink"]))
    arrow(pg, ax + wa + 1.5, ax + wa + gap - 1.5, big_y + 2.5, C["water_deep"])
    # B: what it carries
    bx = ax + wa + gap
    pg.text("CARRIES", bx, ky, 8, C["ink2"], True)
    s = "%s %%" % span(round(plo), round(phi)); fs = fit_size(s, wb, 24.0, True)
    pg.text(s, bx, big_y, fs, C["water_deep"], True)
    s = "of the farms' need"; pg.text(s, bx, l1, fit_size(s, wb, 8.5, True), C["ink"], True)
    inline(pg, bx, l2, rich_parts("**1 in 5 dry** year", 7.5, C["ink2"], C["ink"]))
    by = l2 - 4.0                                               # a 100 % bar filled to the lower % of the range
    pg.rect(bx, by, wb, 2.4, fill=C["white"], stroke=C["structure"], lw=0.2)
    pg.rect(bx, by, wb * min(plo, 100.0) / 100.0, 2.4, fill=C["water_deep"])
    arrow(pg, bx + wb + 1.5, bx + wb + gap - 1.5, big_y + 2.5, C["water_deep"])
    # C: the cost cut-off
    cx = bx + wb + gap
    pg.text("COST CUT-OFF", cx, ky, 8, C["ink2"], True)
    s = "$%g-%g /m³" % RECHARGE_USD; fs = fit_size(s, wc, 18.0, True)
    pg.text(s, cx, big_y, fs, C["green_deep"], True)
    s = "recharge " + cite("ross"); pg.text(s, cx, l1, 8.5, C["green_deep"], True)
    s = "recycled water $%g-%g" % ALTERNATIVE_USD; pg.text(s, cx, l2, fit_size(s, wc, 7.5, True), C["accent"], True)
    vm = ALTERNATIVE_USD[1] * 1.02                              # the two price ranges on one linear US$ scale
    for i, (rng, col) in enumerate(((RECHARGE_USD, C["green_mid"]), (ALTERNATIVE_USD, C["accent"]))):
        yy = l2 - 4.0 - i * 2.6
        pg.line([(cx, yy + 0.9), (cx + wc, yy + 0.9)], C["water_light"], 0.3)
        pg.rect(cx + wc * rng[0] / vm, yy, wc * (rng[1] - rng[0]) / vm, 1.8, fill=col)
    # D (v6, T3b, G7: "one short paragraph states the conclusion"): right of the cut-off (was "our claims": the 25 / 50 %
    # sizes and the cost cases stay in the results JSON)
    qx = cx + wc + 12.0
    pg.line([(qx - 6.0, y + 3.0), (qx - 6.0, top - 3.0)], C["water_light"], 0.4)
    pg.text("So", qx, ky, 8, C["ink2"], True)
    tc = max(t["covered_pct_1in5_dry"] for t in R["today_strip_storage"].values())
    s_ = ("Winter brings the water, summer needs it. Held in the ground, **%s m³** of winter water carries the farms "
          "through a **1 in 5 dry** year; past that, each more m³ costs more than recycled water. Today the strip "
          "alone holds %s m³: **%.0f %%** of the need." % (span(lo_, hi_), fmt(STRIP_TODAY), tc))
    rich_para(pg, s_, qx, ky - 5.0, x + w - 4.0 - qx, 8.5, C["ink"], C["ink"], 1.35)

# ------------------------------------------------------------------ the question (v6: the sheet's subtitle, under the title)
QUESTION = u"How much **winter water** can we hold for the farms' **dry summer**, and at what **cost**?"


# ------------------------------------------------------------------ v6 (T3b, G7): 1 one year of water, five rows, one month axis
STORE_COL = ("CBD9F8", "92A3C9", "3E4C6E")       # the masterplan's storage tones (light, mid, dark), as on p.12's map
YEAR_RH = 16.5                                   # one row of block 1, mm
YEAR_LAB_W, YEAR_TOT_W = 68.0, 40.0              # the label column before the month axis, the year column after it


def panel_year(pg, R, x, y, w, h):
    """v6 (revision 29 Oct, T3b WO-T3b-2; G7 after R31: every user its own row with its pictogram, one common time
    axis drawn as bars, figures read as charts): block 1, the whole balance through one year. Five rows share the
    month axis J-D: the Selinos stream (natural flow, Dec-Apr dark), the site catch, the design store's level, the
    summer strip and the farms (mean year and 1 in 5 dry). Each row has its own scale: its peak month carries its
    figure, its year total sits at the right. One band marks Jun-Sep across all rows and says what it means. Replaces
    v5's question block, farm tiles, monthly chart with its number rows, and the stream's monthly flow."""
    mix = R["design"]["mix"]; L = R["lands"]; crop = mix.split()[-1]
    q = STREAM_MONTH_M3; yr = float(sum(q)); win = (0, 1, 2, 3, 11)
    dn = R["farm_demand_month_m3"][mix]["mean"]; dd = R["farm_demand_month_m3"][mix]["dry5"]
    sm = R["design"].get("store_month_m3") or [0] * 12
    panel_title(pg, x, y + h, w, "1", "One year of water: it comes in winter, it is needed in summer",
                "**one month axis** for every user · each row to its own scale: its peak month and its year are written")
    lx, rx = x + YEAR_LAB_W, x + w - YEAR_TOT_W
    bw = (rx - lx) / 12.0
    top = y + h - 10.0                                        # the first row's top
    rows = [
        ("stream", "Selinos stream", "natural flow past the site " + cite("flow"), (q,),
         lambda m: C["water_deep"] if m in win else C["water"], "%.1f million m³" % (yr / 1e6),
         "a year, %d %% in Dec-Apr" % round(100.0 * sum(q[m] for m in win) / yr)),
        ("rain", "Site catch", "roofs, walks, terraces " + cite("era5", "mgm"), (R["site_month_m3"],),
         lambda m: C["green_mid"], "%s m³" % fmt(R["site_catch_m3_per_year"]), "a year"),
        ("storage", "The store", "winter water held in the ground, level at month end " + cite("dsi", "rg"), (sm,),
         lambda m: STORE_COL[1], "%s m³" % fmt(max(sm)), "at its fullest"),
        ("water", "Summer strip", "%s, sealed: evaporation + seepage" % u_area(L["strip_m2"], "ha"),
         (R["strip_month_m3"],), lambda m: C["water"], "%s m³" % fmt(R["strip_m3_per_year"]), "a year, May-Oct"),
        ("olive", "Farms", "%s %s + %s olives, drip %s" % (u_area(L["cropland_ha"] * 1e4, "ha"), CROP_NAME.get(crop, crop),
                                                           u_area(L["orchard_ha"] * 1e4, "ha"),
                                                           cite("fao56", "fao_t", "fao_tm4", "esa")),
         (dn, dd), None, "%s m³" % fmt(R["farm_demand_m3"][mix]["dry5"]), "a year, 1 in 5 dry")]
    yb_rows = top - len(rows) * YEAR_RH
    bx0, bx1 = lx + 5 * bw, lx + 9 * bw                      # Jun-Sep: one band behind every row
    pg.rect(bx0, yb_rows - 13.0, bx1 - bx0, top + 1.0 - (yb_rows - 13.0), fill=C["accent_tint"])
    for i, (ic, name, sub, series, colf, tot, tot2) in enumerate(rows):
        ty = top - i * YEAR_RH
        by, bh = ty - YEAR_RH + 2.6, YEAR_RH - 7.0
        ico(pg, ic, x + 5.0, ty - YEAR_RH / 2.0 + 0.6, 9.0)
        pg.text(name, x + 12.0, ty - 5.0, 9, C["ink"], True)
        pg.para(sub, x + 12.0, ty - 8.8, YEAR_LAB_W - 14.0, 7, C["ink2"])
        pg.line([(lx, by), (rx, by)], C["structure"], 0.2)
        vmax = float(max(max(s) for s in series)) or 1.0
        pk = None
        for m in range(12):
            x0 = lx + m * bw
            if len(series) == 1:
                v = series[0][m]; hh = bh * v / vmax
                if v > 0: pg.rect(x0 + bw * 0.2, by, bw * 0.6, max(0.3, hh), fill=colf(m))
                if pk is None or v > pk[1]: pk = (x0 + bw / 2.0, v, hh)
            else:                                             # the farms: mean year and 1 in 5 dry side by side
                for j, (s, col) in enumerate(((series[0], C["accent"]), (series[1], C["accent_deep"]))):
                    v = s[m]; hh = bh * v / vmax
                    if v > 0: pg.rect(x0 + bw * (0.16 + 0.35 * j), by, bw * 0.33, max(0.3, hh), fill=col)
                    if j == 1 and (pk is None or v > pk[1]): pk = (x0 + bw * 0.675, v, hh)
        if pk and pk[1] > 0 and ic != "storage":              # (the store's peak is its year figure, at the right)
            s_ = ("%.2f million m³" % (pk[1] / 1e6)) if ic == "stream" else "%s m³" % fmt(pk[1])
            pg.text(s_, pk[0], by + pk[2] + 0.9, 7, C["ink"], True, "C")
        pg.text(tot, x + w, ty - 5.0, 9, C["ink"], True, "R")
        pg.text(tot2, x + w, ty - 8.6, 7, C["ink2"], False, "R")
        if len(series) == 2:                                  # the farms' two bars, named in the year column
            ex = x + w - inline_w([("mean", 7, 0, False), ("1 in 5 dry", 7, 0, False)]) - 2 * 3.6 - 4.0
            pg.rect(ex, ty - 12.6, 2.4, 2.4, fill=C["accent"]); ex = inline(pg, ex + 3.6, ty - 12.3, [("mean", 7, C["ink"], False)])
            pg.rect(ex + 4.0, ty - 12.6, 2.4, 2.4, fill=C["accent_deep"]); pg.text("1 in 5 dry", ex + 7.6, ty - 12.3, 7)
    for m in range(12):
        pg.text(MON[m], lx + (m + 0.5) * bw, yb_rows - 1.4, 7.5, C["ink"], True, "C")
    js = round(100.0 * sum(dn[5:9]) / max(sum(dn), 1))
    pg.text("JUN-SEP: %d %% of the farms' need" % js, (bx0 + bx1) / 2.0, yb_rows - 7.0, 8, C["accent_deep"], True, "C")
    pg.text("%.0f %% of the stream's flow" % (100.0 * sum(q[5:9]) / yr), (bx0 + bx1) / 2.0, yb_rows - 10.6, 7.5, C["ink"],
            False, "C")


# ------------------------------------------------------------------ 5 storage size: the sizing curve (v5: was panel 3)
def panel_curve(pg, R, x, y, w, h):
    mix = R["design"]["mix"]; crop = mix.split()[-1]
    panel_title(pg, x, y + h, w, "2", "How much to hold: the farm need covered, by store size",   # v6: block 2
                "34 water years 1991-2025 · daily · cropland as %s %s · in: **winter stream + site catch**, strip first %s"
                % (CROP_NAME.get(crop, crop), cite("era5", "fao56"), cite("dsi")))     # v5 (G11): "corn", the key stays maize
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
    series = [(cc, 1, C["water_deep"], None, "median year"),          # v6 (T3b): the open-pond curves left the sheet
              (cc, 2, C["accent"], None, "1 in 5 dry year")]          # (results key curve_open unchanged)
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
    ico(pg, "storage", lgx + 2.75, y + h - 36.75, 5.5)
    pg.text("max 365 days", lgx + 7.5, y + h - 36.5, 8, C["ink"], True)
    pg.text("in store, then to the strip", lgx + 7.5, y + h - 40.3, 7, C["ink2"])

# ------------------------------------------------------------------ 6 cost per m3, where to stop (v5: was panel 4)
def panel_store(pg, R, x, y, w, h):
    L = R["lands"]
    panel_title(pg, x, y + h, w, "3", "Cost per m³: cheapest first, then stop",   # v6: block 3
                "**US$/m³ delivered** · log scale · capital 5 %/yr " + cite("suds"))
    na = {r["key"]: r for r in R["ladder_no_recharge"]}
    rows = [("Aquifer recharge", "winter water into the alluvium " + cite("ross"), RECHARGE_USD[0], RECHARGE_USD[1])]
    # v5 (MIRAQUA 28 Oct, G13 + Aras 13:21 "if a page uses ha for areas try to keep ha for everywhere"): land areas in
    # ha like block 3's farm land (same values); the cistern's land per m³ stays a m² ratio
    lab = dict(pond="%s, %s m³ at most" % (u_area(L["pond_land_ha"] * 1e4, "ha"), fmt(L["pond_land_ha"] * 1e4 * POND_DEPTH * POND_USE)),
               crates="%s of walks" % u_area(L["walk_m2"] + L["riverside_walk_m2"], "ha"), cistern="0.12 m² of land per m³")
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
    ico(pg, "storage", x + 2.25, ky - 10.85, 4.5)
    inline(pg, x + 6, ky - 11.8, rich_parts("**recharge fails tests**: built > recycled, every step " + cite("suds"), 7, C["ink2"], C["ink"]))

# v5 (MIRAQUA 28 Oct, P11.2): the sheet re-laid in Aras's reading order, top-left -> bottom-right, a rule and a numbered
# title over every block and 8-10 mm between the rows:
#   [title + 1 the question] [2 how the stream behaves: monthly flow | the flood cut at 1:500]
#   [3 what the farms need: tiles | monthly need]           [4 what the site can catch]
#   [5 storage size]                                         [6 cost]
#   [7 the answer: a light band across the foot, the bottom-right corner left free for the booklet's page number]
# (x, y bottom, w, h) in mm, y up; a block's title sits on y + h, its rule 4.5 mm above (panel_title). Shared with the
# booklet crops (booklet_export). Replaces v2.7's FARMS / PANELS / STREAM_BAND.
# v6 (T3b WO-T3b-2, G7): four blocks in reading order, the question as the sheet's subtitle:
#   [title + the question, the run line at the right]
#   [1 one year of water: five rows on one month axis, across the sheet (the focal block)]
#   [2 how much to hold: the storage curve]                 [3 cost per m³]
#   [4 the answer: store -> carries -> cost cut-off | the conclusion, the bottom-right corner free for the page number]
BLOCKS = dict(year=(14.0, 148.0, 392.0, 112.0),
              curve=(14.0, 66.0, 248.0, 70.0), store=(272.0, 66.0, 134.0, 70.0),
              answer=(14.0, 18.5, 392.0, 39.0))


def build(path, R):
    """The A3 sheet; returns the list of overlapping labels (empty = none).
    v5 (MIRAQUA 28 Oct, P11.2): the blocks of BLOCKS drawn in reading order 1-7, so the [n] marks count up that way.
    v6 (T3b): four blocks (1 the year, 2 the curve, 3 the cost, 4 the answer); the question under the title."""
    pg = Page(420.0, 297.0)
    pg.rect(0, 0, 420, 297, fill=C["white"])               # v2.7: white sheet (Aras 27 Oct 11:07)
    del SRC_KEY[:]                                        # v2.4: [n] numbers restart on every run
    pg.text("THE WATER BALANCE", 14, 281.5, 22, C["ink"], True)
    rich_para(pg, QUESTION, 14, 273.5, 300, 11, C["ink2"], C["ink"])
    pg.text("lands option %s · run %s" % (R["lands"]["option"], R["run_time"]), 406, 281.5, 7, C["ink2"], align="R")
    panel_year(pg, R, *BLOCKS["year"])                    # 1: the five users of the water on one month axis
    panel_curve(pg, R, *BLOCKS["curve"])                  # 2
    panel_store(pg, R, *BLOCKS["store"])                  # 3
    panel_answer(pg, R, *BLOCKS["answer"])                # 4
    for k in SOURCES:                                     # v2.4: one numbered source key (no source can drop out)
        if k not in SRC_KEY: SRC_KEY.append(k)
    # v2.7: no source footer on the sheet (Aras 27 Oct 11:07); the key stays as INVISIBLE text so the booklet's
    # sources page (bergama_booklet sheet_sources: "Sources by number:") still lists what the [n] marks refer to
    pg.para("Sources by number: " + "  ".join("[%d] %s" % (i + 1, SOURCES[k]) for i, k in enumerate(SRC_KEY)),
            14, 8, 392, 6, C["ink2"], hidden=True)       # v4.1 (Prompt 8): public sources only, no internal notes file
    write_pdf(pg, path)
    return overlaps(pg)

# ------------------------------------------------------------------ v2.6: A3 booklet = crops of this sheet (booklet/CROP_SPEC.md)
#@include ../common/booklet_assets.py

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
    from the new FARMS / PANELS: each panel under its title and keyword line (7.5 mm under the title baseline).
    v5 (MIRAQUA 28 Oct, P11.2): the same seven crop ids, rects from BLOCKS (the answer = its tint field; the tiles = the
    column of block 3; the timing chart = block 3 right of the tiles; the stream = block 2 under its title)."""
    bk = BkBlocks(OUT_DIR, "WaterBalance", VERSION)
    H = 297.0

    def crop(bid, x0, y0, x1, y1, caption, legend=None):
        bk.crop(bid, OUT_PDF, (x0, H - y1, x1, H - y0), caption=caption, scale_den=None, legend=legend, drop=BK_DROP)
    x, y, w, h = BLOCKS["answer"]
    crop("wb_answer", x - 0.5, y - 0.5, x + w + 0.5, y + h - 6.5, "The answer: storage, what it carries, the cost cut-off")
    # v6 (T3b): wb_year = block 1 under its title (the five rows, the months, the Jun-Sep line); wb_tiles, wb_timing,
    # wb_catch and wb_stream are gone with their blocks
    x, y, w, h = BLOCKS["year"]
    crop("wb_year", x - 0.5, y - 0.5, x + w + 0.5, y + h - 7.5, "One year of water: it comes in winter, it is needed in summer")
    x, y, w, h = BLOCKS["curve"]
    crop("wb_curve", x - 0.5, y - 0.5, x + w + 0.5, y + h - 7.5, "Storage size against the farm need covered")
    x, y, w, h = BLOCKS["store"]
    crop("wb_store", x - 0.5, y - 0.5, x + w + 0.5, y + h - 7.5, "Cost per m³ delivered, log scale")
    return bk.save()

# ------------------------------------------------------------------ run (GH Button on any input, ScriptEditor, or python)
def main(g):
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    L, src = get_lands(g)
    R = compute(L); R["lands_source"] = src
    try:                                                  # v6 (T3b): the zones for the water board's p.12 map; never
        R["zones"] = get_zones(L["option"])               # breaks the balance (no key = p.12 shows the places only)
        zone_line = "zones for p.12: %d zones, %d links (%s)" % (len(R["zones"]["zones"]), len(R["zones"]["links"]), R["zones"]["source"])
    except Exception as ex:
        zone_line = "zones for p.12 NOT WRITTEN: %s: %s" % (type(ex).__name__, ex)
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
        "\nbooklet ERROR: " + bk_err if bk_err else "") + "\n" + zone_line + (
        "\nLABEL OVERLAP (%d): %s" % (len(ov), "; ".join(ov[:6])) if ov else "\nlabels: no overlaps") + "".join(
        "\n" + t for t in bg_tidy_output("Bergama_water_balance_analysis")) + "".join(     # 27 Oct: output/ = PDFs only
        "\nyear %s (%s): in %s + %s m3, strip %s, farms %s of %s, released %s, out %s; winter flow %.0f %% of median" % (
            k, v["water_year"], fmt(v["carried_in_m3"]), fmt(v["filled_m3"]), fmt(v["strip_m3"]), fmt(v["farms_m3"]),
            fmt(v["farm_need_m3"]), fmt(v["released_m3"]), fmt(v["carried_out_m3"]), v["winter_flow_pct_of_median"])
        for k, v in ((yk, d["year_split"][yk]) for yk in ("normal", "dry5")))     # v4 (Prompt 6)

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
