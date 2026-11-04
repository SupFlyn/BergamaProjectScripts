# ---- Collect, clean, hold: the numbered elements 1-11 and their places (round 6 S1, 4 Nov 2026; PLAN.md §2.8, §5) --
# ONE source for the numbers of the water chain, so p11 (Collect, clean, hold), p12 (the proposals in section,
# "1-11 as in Collect, clean, hold"), p17 (the plant ladder) and p20 (the masterplan) give the same element the same
# number (BRIEF §6 rows 11, 12, 20; P7). Numbering = the 28 Oct chain, the one Aras judged best:
# -> f93d84b:src/bergama_water_board/code.py:724-737 (CHAIN). Places = the zone base zones (dicts with "code",
# "ring" survey m, "study_area"), as the water board p11 map picks them -> src/bergama_water_board/pages/
# p12_system.py:552 (_p12_pick), 1611-1617 (the winter store point), 1851-1868 (the step markers).
# Included by common/keymap.py (every script that includes basemap.py has it).
#   CCH_STEPS                      {n: (name, zone code or None)} for n = 1..11
#   cch_points(zones, area="aras", log=None)   {n: (x, y) survey m or None, "store": xy, "spill": xy}
#   cch_name(n)                    the element's short name
CCH_STEPS = {
    1: (u"Stream in · mostly winter", None),                       # the upstream entry (CCH_ENTRY)
    2: (u"Reed beds clean it", "WT"),
    3: (u"Terraces hold street + roof runoff", "WS"),
    4: (u"Planted basins store winter water", "store"),            # the winter store: middle of WS + WT
    5: (u"Spillway: overflow back to the stream", "WD"),
    6: (u"Summer strip 4 m x 0.30 m", None),                       # in the bed: no zone of its own
    7: (u"Strip waters the bank planting", "WP"),
    8: (u"Floods spread onto terraces", "WA"),
    9: (u"People on the raised dry top", "DG"),
    10: (u"The clean stream leaves the site", None),               # the downstream end (CCH_EXIT)
    11: (u"Existing farmland outside the site", None),             # outside the study area: a page arrow, no point
}
# the chain's two ends, survey m: the surveyed cut centres of the upstream entry and the downstream end (as
# p12_system.py P12_PLACES, from masterplan parts/02b_detail.py CUT_AT = water board CUTS)
CCH_ENTRY = (29693.022, 32569.176)
CCH_EXIT = (30991.856, 31039.404)
CCH_LOG = []


def cch_name(n):
    return CCH_STEPS[int(n)][0]


def _cch_cen(R):
    """the area centroid of a ring (the water board's _p12_cen)"""
    a = cx = cy = 0.0
    n = len(R)
    for i in range(n):
        (xa, ya), (xb, yb) = R[i][:2], R[(i + 1) % n][:2]
        f = xa * yb - xb * ya
        a += f
        cx += (xa + xb) * f
        cy += (ya + yb) * f
    if abs(a) < 1e-12:
        return (sum(p[0] for p in R) / n, sum(p[1] for p in R) / n)
    return (cx / (3.0 * a), cy / (3.0 * a))


def cch_points(zones, area="aras", log=None):
    """the place of each numbered element (survey m): the centroid of the first zone of its code in `area` (a
    study_area prefix; None = any area); 4 = the winter store = the mean centroid of every WS and WT zone of that
    area (as the p11 map's HOLD point); 1 / 10 = the chain's entry / exit points; 6 and 11 have no place (None: a
    page draws them as a strip / arrow or leaves them out). Also "store" (= 4) and "spill" (= 5). Logs
    `cch points <found>/<11> missing=<numbers>`; a number whose zone is missing is None, never guessed."""
    log = log if log is not None else CCH_LOG

    def pick(code):
        return [z for z in zones or () if z.get("code") == code and z.get("ring") and
                (area is None or (z.get("study_area") or u"").startswith(area))]
    out = {}
    for n, (_nm, code) in CCH_STEPS.items():
        if code is None or code == "store":
            out[n] = None
            continue
        zs = pick(code)
        out[n] = _cch_cen(zs[0]["ring"]) if zs else None
    up = pick("WS") + pick("WT")
    out[4] = (sum(_cch_cen(z["ring"])[0] for z in up) / len(up), sum(_cch_cen(z["ring"])[1] for z in up) / len(up)) \
        if up else None
    out[1], out[10] = CCH_ENTRY, CCH_EXIT
    out["store"], out["spill"] = out[4], out[5]
    miss = [n for n in CCH_STEPS if out[n] is None and n not in (6, 11)]
    log.append(u"cch points %d/11 missing=%s" % (sum(1 for n in CCH_STEPS if out[n] is not None),
                                                 u",".join(str(n) for n in miss) or u"-"))
    return out
