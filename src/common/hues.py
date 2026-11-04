# ---- Category -> hue table (round 6 S1, 4 Nov 2026; G6-6, Q5, Q7; PLAN.md §2.6) ------------------------------------
# ONE table every legend reads (Aras 4 Nov 09:44-10:08: "categorize the legends like heritage is categorized under
# heritage with similar shades of the same colour. The darker the shade is the more important it is"): each category
# one hue, items inside it = its ranks, r1 darkest = most important; never a separate hue per item. Subtle set on
# every plan, section, chart and legend; strong set (HUE_KEY) on key maps only. Values: PLAN.md §2.6 ->
# revision_2026-11-04_round6/plan_findings/hues_and_proposals.md H2 (method and contrast checks there).
# Included by common/keymap.py (so every script that includes basemap.py has it); a script without basemap.py (the
# booklet) includes it itself, once.
#   HUE[code][rank] hex      HUE_KEY[name] hex      hue(code, rank, strong=False)      HER_RANK[name] -> 1/2/3
#   legend_group(entries)    entries sorted by category (table order) then rank
#   hue_log(page, log=None)  the line `legend <page> hues=table`
HUE_CATS = ("CTX", "HER", "WAT", "WW", "GRN", "AGR", "MOV", "PUB")          # legend order: context first
HUE_NAMES = {"CTX": u"Existing context", "HER": u"Heritage", "WAT": u"The Selinos stream",
             "WW": u"Water works: collect, clean, hold", "GRN": u"Planting", "AGR": u"Farms",
             "MOV": u"Streets, shops and movement", "PUB": u"Public life and hubs"}
HUE = {
    # existing context: ground, buildings, streets, bridges, existing green (with tree symbols), workshops, vacant
    "CTX": {1: "4A3F35", 2: "847E75", 3: "B0AC9C", 4: "D8D5CC", 5: "EFEDE6"},
    # heritage (Q5): r1 inside the UNESCO World Heritage listing, r2 registered monument, r3 other historic or no
    # sourced status, r4 heritage area tint
    "HER": {1: "512E1A", 2: "84573E", 3: "B08870", 4: "E7CABB"},
    "WAT": {1: "32525F", 2: "5D7F8D", 3: "91ADB4", 4: "C1D3DB"},
    # water works: reed basins, spillway, winter store, dry-top terraces, side arm, widened wetland
    "WW": {1: "2D564E", 2: "54857D", 3: "87BBAA", 4: "CBEDE5"},
    # proposed planting: bands wet -> dry, forest corridor, designed green (plant swatches: tree r1, shrub r2,
    # ground / emergent r3, P-3)
    "GRN": {1: "3C4733", 2: "70754C", 3: "89986A", 4: "C2CCB3"},
    "AGR": {1: "534E25", 2: "948B49", 3: "C6C08D", 4: "E6E3C5"},
    # streets and movement: pedestrian r1, calmed r2, shared r3; commerce r1, mixed r2, residential r3
    "MOV": {1: "734C17", 2: "A67628", 3: "CCA363", 4: "EAD1A4"},
    # public life: walking hubs, transit hub, sub-hubs, hub squares, market, civic, people groups by headcount
    "PUB": {1: "452842", 2: "7F5B7B", 3: "AE90AA", 4: "DECFDC"},
}
# annotations (not a category): study area line, plan cut marks (G6-4), text ink
HUE_ANN = {"study": "6A4C93", "cut": "8E8F8A", "ink": "2C2219"}
# strong set: key maps only (G6-5, the p08 "Where each street is cut" look)
HUE_KEY = {"fabric_mix": 0.40, "her1": "663214", "her2": "965630", "her3": "C18A65",
           "trees": "A0A681", "park": "B1B792", "grass": "C4C7A6", "farmland": "CFC99D",
           "stream": "7FA4B3", "stream_edge": "5E8494", "road": "FAF8F1", "road_edge": "DCD5C2",
           "street_names": "A4A1A3", "cut": "C0392B", "study": "6A4C93"}
HUE_NAME_PT = 4.0                    # key-map street names: exactly the 4 pt floor (PLAN §2.7)
# heritage ranks of the heritage-loop places (Q5; H3): Kızıl Avlu r1 is a reading (ICOMOS names its tunnels; the
# boundary is not stated): set it to 2 if Aras reads it as registered only. Teleferik is context (CTX), not heritage.
HER_RANK = {u"Akropol": 1, u"Kızıl Avlu": 1, u"Tabak Köprüsü": 3, u"Ulucami Önü Köprüsü": 3, u"Ulucami": 3,
            u"Ulu Cami": 3, u"Tabaklar Hamamı": 3, u"Arasta": 3, u"Üç Kemer Köprüsü": 3, u"Bergama Müzesi": 3,
            u"Asklepion": 3}
HUE_LOG = []


def hue(code, rank, strong=False):
    """the hex of category `code` at `rank` (1 = darkest, most important); strong=True on key maps: heritage ranks
    from HUE_KEY (her1-3), every other name of HUE_KEY by itself (hue("trees", 0, True)). An unknown code or rank
    raises (a legend never invents a colour); a rank past the ramp takes its lightest step with a WARNING line"""
    if strong:
        if code == "HER":
            return HUE_KEY["her%d" % min(3, max(1, int(rank)))]
        if code in HUE_KEY:
            return HUE_KEY[code]
    if code == "ANN":
        return HUE_ANN[rank]
    ramp = HUE[code]
    r = int(rank)
    if r not in ramp:
        HUE_LOG.append(u"WARNING legend: %s has no rank %s; its lightest step used" % (code, rank))
        r = max(ramp)
    return ramp[r]


def her_rank(name, default=3):
    """the heritage rank of a place name (HER_RANK; no sourced status = 3)"""
    return HER_RANK.get(name, default)


def legend_group(entries):
    """legend entries sorted by category (HUE_CATS order) then rank, darkest first. An entry is a dict with "cat"
    and "rank" (other keys kept), or a tuple (cat, rank, ...). Each dict gets "hex" (its table colour) and
    "cat_name" (the category's heading) when missing, so a legend draws only table hues"""
    def key(e):
        c, r = (e.get("cat"), e.get("rank")) if isinstance(e, dict) else (e[0], e[1])
        return (HUE_CATS.index(c) if c in HUE_CATS else len(HUE_CATS), r if isinstance(r, int) else 9)
    out = sorted(entries, key=key)
    for e in out:
        if isinstance(e, dict) and e.get("cat") in HUE:
            e.setdefault("hex", hue(e["cat"], e.get("rank") or 1))
            e.setdefault("cat_name", HUE_NAMES[e["cat"]])
    return out


def hue_log(page, log=None):
    """the done-when line of a legend drawn from this table: `legend <page> hues=table`"""
    ln = u"legend %s hues=table" % page
    (log if log is not None else HUE_LOG).append(ln)
    return ln
