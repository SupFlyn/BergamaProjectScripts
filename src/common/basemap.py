# ---- Shared basemap (revision 29 Oct 2026, brief 02 §1, WO-T2a-1) -------------------------------------------------
# ONE base for every map of the booklet (site board, water board, city link, masterplan, agriculture): the same
# stream, streets, buildings, green, tree cover, fields and contours, switched on and off per page by its MODE, with a
# per-drawing override (D5: Zones a, Feeling b stream only, Sound b stream + main roads, Smell b stream only ...).
#
# WHERE THE DATA COMES FROM (decided 29 Oct, T2a): not from the open Rhino file. The site board already builds the
# whole site model once (survey of Bergama_Altlik.3dm + OpenStreetMap + WorldCover, cached); it calls
# basemap_export(S) once a run and writes Downloads/Bergama/cached/basemap/basemap.json. Every other script reads that
# file with basemap_load(). Inside the analysis frame (site_alan) the layers are the site board's own (survey quality,
# exactly as p.06 draws them); between the frame and the wider EXTENT they are OpenStreetMap's (Data/bergama_osm.osm),
# so p.21 reaches the Asklepion, the Akropol, the cable car and the museum, and p.16's frames can widen. Scripts that
# run before the site board in the chain (zone base, masterplan, water balance) read the file of the last run; before
# the very first site board run there is no file: basemap_load() returns None, logs it, and every draw call draws
# nothing (the caller's own drawing goes on).
#
# GEOMETRY: survey metres everywhere. Line widths and marker sizes are PRINT mm on the booklet page, so a call needs
# the drawing's scale denominator only where a size in mm becomes metres (cut-line markers). Colours: hex 'RRGGBB'.
# A draw call returns ITEMS, bottom first; the caller turns them into its own page calls (basemap_draw does that
# through two or three small functions the caller gives). Items:
#   ("fill", rings, hex, alpha, nonzero)        rings = [[(x, y), ...], ...] (outlines and their holes)
#   ("line", pts, hex, width_mm, dash_mm, alpha) dash_mm = None or [on, off, ...] in print mm
#   ("text", s, (x, y), size_mm, hex, bold, align)   align as the scripts' text calls ("MC" = middle centre)
# M3 (revision 30 Oct 2026, H-A): the 29 Oct modes and switches are kept as they were; added the layers study_area
# (calisma_alan, ONE outline reused on every map, R28_STUDY_LINE), names (place names) and the building styles "plan" /
# "plan_faint" (M11: block outlines + roof reading, no stripes), the modes "base" (the faint base of a map page) and
# "key" (key maps, M4), the water drawn by M5 (water_plan, when included) and keymap_items (M4). The data carries per
# building its height (h, floors) and a "blocks" layer (buildings sharing a wall merged: no fake division lines).
import os as _bm_os
import json as _bm_json
import math as _bm_math

BASEMAP_FILE = _bm_os.path.join(_bm_os.path.expanduser("~"), "Downloads", "Bergama", "cached", "basemap",
                                "basemap.json")
BASEMAP_FORMAT = 1
BASEMAP_MARGIN = 250.0           # m: the extent reaches this far beyond the farthest REACH place
# the places the extent must hold (survey m; the heritage loop's positions, selinus_board parts/15j_r28_heritage.py)
BASEMAP_REACH = ((u"Asklepion", (29077.3, 31867.3)),          # OSM ticket building
                 (u"Akropol", (30209.0, 33177.0)),            # Trajaneum, OSM way 1410335587
                 (u"Teleferik", (30720.4, 32370.1)),          # valley station, OSM node 2295928011
                 (u"Bergama Müzesi", (29560.0, 31358.0)))

# tones: the p.06 stream edge plan's (selinus_board MPL, R28E_*) so the detailed mode is p.06's base
BM_COL = dict(bld="A7A299", bld_osm_edge="736A62", her="E4CAC9", her_edge="AF7474", water="91ADB4",
              water_edge="5D7F8D", tree="C4CCB5", park="DFEBC0", grass="DFEBC0", field="C6C08D", road="CFCCC5",
              road_edge="847E75", ink="2C2219", contour="BDB7B0", cut="2C2219")
BM_FAINT = dict(bld="D3D0CB", bld_veryfaint="E9E7E3", road="E2E0DB", road_line="B9B4AC")
# round 4 (S2, G-R4-4, PLAN §4.3): the MUTED base under every map page: light houses with a closed block outline,
# light streets with their edges, every outline after every fill (CHK-3 §1.5-1.6); heritage a pale rose.
BM_MUTED = dict(bld="EDEBE6", bld_edge="C9C5BC", her="F1E6E5", her_edge="CDAAAA", road="F4F2EE", road_edge="CFCBC2",
                name="9A948A", lw=0.12)
# contours coloured to the relief (G-R4-4, U48): green tones, lighter = lower (palette 3C4733 and its 89986A tints)
BM_HEIGHT_RAMP = ("C9D6B0", "A7B68C", "89986A", "3C4733")
BM_LW = dict(contour=(0.07, 0.13), contour_topo=(0.08, 0.14), water_edge=0.18, covered=0.30, bridge=0.30,
             road_edge=0.12, osm_edge=0.08, her_edge=0.12, main=0.45, lane=0.22, path=0.10, river_osm=0.6,
             stream_osm=0.35, cut=0.35)
BM_COVERED_DASH = (1.6, 0.9)     # mm: the covered course

# the modes of 02 §1; a value per layer: False = off, True = on, "faint" / "veryfaint" = buildings or streets faint,
# a tuple of street classes ("main", "lane", "path") = only those as centrelines, "height" = contours by height
BASEMAP_MODES = {
    "detailed": dict(stream=True, streets=True, buildings=True, green=True, trees=True, fields=True, contours=True,
                     study_area=False, names=False),
    "simple": dict(stream=True, streets="faint", buildings="faint", green=False, trees=False, fields=False,
                   contours=False, study_area=False, names=False),
    "minimal": dict(stream=True, streets=("main", "lane"), buildings="veryfaint", green=False, trees=False,
                    fields=False, contours=False, study_area=False, names=False),
    "topographic": dict(stream=True, streets=False, buildings="faint", green=False, trees=False, fields=False,
                        contours="height", study_area=False, names=False),
    # M3 (30 Oct): the faint base under a map page's message (G5), and the key map's base (M4)
    "base": dict(stream=True, streets="faint", buildings="plan_faint", green=False, trees=False, fields=False,
                 contours=False, study_area=True, names=False),
    "key": dict(stream=True, streets=("main",), buildings="veryfaint", green=False, trees=False, fields=False,
                contours=False, study_area=True, names=False),
    # round 4 (S2, G-R4-4): the muted base of map_layers.ml_base; the study line is drawn by map_draw in its own
    # layer (above the project fills), so it is off here; contours are switched on by the call ("height")
    "muted": dict(stream=True, streets="muted", buildings="muted", green=False, trees=False, fields=False,
                  contours=False, study_area=False, names=False),
}
# M3 layer list -> switches: basemap_layers accepts these names too (buildings, streets, water, topography,
# study_area, names; green, trees, fields as before)
BM_LAYER_ALIAS = dict(water="stream", topography="contours")
# round 4 (S2, G-R4-4, U18/U19): ONE study-area line everywhere: violet long-dash-dot, its own hue (never ink, grey
# or a road colour); r28_style.py R28_STUDY_LINE holds the same values (either file may be included first)
BM_STUDY_LINE = dict(colour="6A4C93", width_mm=0.35, dash_mm=(3.0, 0.8, 0.6, 0.8))
BM_NAME_MM = 2.47                  # place names: the M1 label size (7 pt)
_BM_MEMO = {}
_BM_WARN = []


# ------------------------------------------------------------------------------------------- reading
def basemap_load(path=None, log=None):
    """the basemap data (dict) written by the site board's basemap_export, read once a run; None when the file is
    missing or of another format (a line goes to log, a list, when given)"""
    p = path or BASEMAP_FILE
    if p in _BM_MEMO:
        return _BM_MEMO[p]
    d = None
    try:
        with open(p, "r", encoding="utf-8") as fh:
            d = _bm_json.load(fh)
        if not isinstance(d, dict) or d.get("format") != BASEMAP_FORMAT:
            if log is not None:
                log.append(u"WARNING: {} is of another format: the shared basemap is left out (run the site board "
                           u"once).".format(p))
            d = None
        elif log is not None:
            log.append(u"Shared basemap: {} ({}).".format(p, d.get("source", "")))
    except Exception as ex:
        if log is not None:
            log.append(u"WARNING: the shared basemap {} could not be read ({}): maps are drawn without it until the "
                       u"site board has run once.".format(p, type(ex).__name__))
    _BM_MEMO[p] = d
    return d


def basemap_frame(D=None):
    """the analysis frame (site_alan) as four survey corners, upstream end first, from the data; None without data"""
    D = D if D is not None else basemap_load()
    return [tuple(p) for p in D["frame"]] if D else None


def basemap_extent(D=None):
    """the whole basemap's rectangle as four survey corners (frame axes); None without data"""
    D = D if D is not None else basemap_load()
    return [tuple(p) for p in D["extent"]] if D else None


def basemap_layers(mode, override=None):
    """the layer switches of a mode (BASEMAP_MODES) with a drawing's own changes laid over them, e.g.
    basemap_layers("minimal", {"streets": ("main",), "buildings": False}) for D5 Sound b (stream + main roads).
    M3 (30 Oct): override may also be a LIST of layer names = only those on (the others off), each at the mode's
    own value, e.g. basemap_layers("base", ["buildings", "water", "study_area"]); "water" = stream, "topography" =
    contours. buildings: True / "faint" / "veryfaint" / "plan" / "plan_faint" (M11) / False."""
    if mode not in BASEMAP_MODES:
        raise ValueError(u"basemap mode '{}' unknown: one of {}".format(mode, ", ".join(sorted(BASEMAP_MODES))))
    lay = dict(BASEMAP_MODES[mode])
    if isinstance(override, (list, tuple, set, frozenset)):
        want = set(BM_LAYER_ALIAS.get(k, k) for k in override)
        for k in want:
            if k not in lay:
                raise ValueError(u"basemap layer '{}' unknown: one of {}".format(k, ", ".join(sorted(lay))))
        on = dict(BASEMAP_MODES["detailed"], study_area=True, names=True)
        override = dict((k, (lay[k] or on[k]) if k in want else False) for k in lay)
    for k, v in (override or {}).items():
        k = BM_LAYER_ALIAS.get(k, k)
        if k not in lay:
            raise ValueError(u"basemap layer '{}' unknown: one of {}".format(k, ", ".join(sorted(lay))))
        lay[k] = v
    return lay


def _bm_bb(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return min(xs), min(ys), max(xs), max(ys)


def _bm_hit(P, box):
    if box is None:
        return True
    b = _bm_bb(P)
    return not (b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3])


def _bm_ramp(t):
    """BM_HEIGHT_RAMP at t in 0..1 (hex)"""
    t = min(1.0, max(0.0, t))
    n = len(BM_HEIGHT_RAMP) - 1
    i = min(n - 1, int(t * n))
    f = t * n - i
    a, b = BM_HEIGHT_RAMP[i], BM_HEIGHT_RAMP[i + 1]
    return "".join("%02X" % int(round(int(a[j:j + 2], 16) + (int(b[j:j + 2], 16) - int(a[j:j + 2], 16)) * f))
                   for j in (0, 2, 4))


def basemap_items(mode="detailed", override=None, box=None, D=None, split_buildings=False, scale_den=None):
    """the basemap of a drawing as items (bottom first; see the head of this file), in survey m. mode: "detailed",
    "simple", "minimal", "topographic" (02 §1), "base", "key" (M3, 30 Oct); override: layer changes for this drawing,
    a dict or a list of the layers to show (basemap_layers); box = (x0, y0, x1, y1) survey m: only what touches it
    (the caller clips to its frame); split_buildings=True gives every building its own fill item (for a page that
    fills even-odd only; default: nonzero fills in chunks); scale_den: the drawing's scale (1:scale_den) for the
    M11 roof marks of buildings "plan" / "plan_faint" (default 1:5,000). [] without data."""
    D = D if D is not None else basemap_load()
    if not D:
        return []
    # the same request in one run is made once and copied (Aras 29 Oct 19:18: build once, cache, copy the layers)
    ov = sorted(override) if isinstance(override, (list, tuple, set, frozenset)) else sorted((override or {}).items())
    mk = ("items", id(D), mode, repr(ov), tuple(box) if box else None, bool(split_buildings), scale_den)
    if mk in _BM_MEMO:
        return list(_BM_MEMO[mk])
    _BM_MEMO[mk] = _bm_items(D, mode, override, box, split_buildings, scale_den)
    return list(_BM_MEMO[mk])


def basemap_water_rings(items):
    """M3: the stream's rings (survey m) in an item list, whether drawn plain (fill items of the water colour) or by
    M5 (the "water" item): for a page that clips or measures by the water"""
    out = []
    for it in items:
        if it[0] == "water":
            out += [R for g in it[1] for R in g if len(R) >= 3]
        elif it[0] == "fill" and it[2] == BM_COL["water"]:
            out += [R for R in it[1] if len(R) >= 3]
    return out


def basemap_warnings():
    """M3: what the basemap could not draw as asked this run (e.g. the M5 water drawing failed): log lines, emptied"""
    out = list(_BM_WARN)
    del _BM_WARN[:]
    return out


def basemap_study(D=None):
    """M3: the study area (calisma_alan, two closed parts worked as one) as rings in survey m: the basemap's study
    layer, else the recorded copy a script includes (R28_STUDY_COPY, CALISMA_COPY, CL_STUDY); [] without either"""
    D = D if D is not None else basemap_load()
    st = ((D or {}).get("layers") or {}).get("study")
    if st:
        return [[tuple(p) for p in R] for R in st]
    for nm in ("R28_STUDY_COPY", "CALISMA_COPY", "CL_STUDY"):
        v = globals().get(nm)
        if v:
            return [[tuple(p) for p in R] for R in v]
    return []


def basemap_study_items(D=None, style=None):
    """M3: the study-area outline as line items (survey m), one style everywhere (R28_STUDY_LINE when included)"""
    st = style or globals().get("R28_STUDY_LINE") or BM_STUDY_LINE
    return [("line", list(R) + [R[0]], st["colour"], st["width_mm"], list(st["dash_mm"]), 1.0)
            for R in basemap_study(D) if len(R) >= 3]


def basemap_names(box=None, D=None):
    """M3: the place names [(name, (x, y))] in survey m (the extent's landmarks and named heritage buildings), for a
    page to place with M2 (lp_place) so no name collides"""
    D = D if D is not None else basemap_load()
    if not D:
        return []
    nm = (D.get("layers") or {}).get("names") or [[n, list(p)] for n, p in (D.get("reach") or BASEMAP_REACH)]
    out = []
    for n, p in nm:
        if box is None or (box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]):
            out.append((n, (p[0], p[1])))
    return out


def basemap_street_names(box=None, D=None, classes=("main",), min_len_m=0.0):
    """round 4 (S2, G-R4-9 U55): the street names of OpenStreetMap's `name` tags (Turkish as mapped), one per name
    at the middle of its longest run: [(name, (x, y), angle_deg, class, run_m)] in survey m, longest first; classes
    = the street classes kept ("main", "lane"); [] when the basemap file predates round 4 (run the site board)"""
    D = D if D is not None else basemap_load()
    out = []
    for n, p, a, cl, ln in ((D or {}).get("layers") or {}).get("street_names") or []:
        if cl in classes and ln >= min_len_m and (box is None or (box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3])):
            out.append((n, (p[0], p[1]), a, cl, ln))
    out.sort(key=lambda r: -r[4])
    return out


def _bm_items(D, mode, override, box, split_buildings, scale_den=None):
    """basemap_items without the memo"""
    lay = basemap_layers(mode, override)
    L = D["layers"]
    out = []
    outl = []          # round 4 (S2, CHK-3 §1.6): outlines (street, building, bridge edges) come after EVERY fill

    def fills(groups, col, alpha=1.0, nonzero=True, chunk=300):
        cur = []
        for g in groups:
            g = [R for R in g if len(R) >= 3]
            if not g or not _bm_hit(g[0], box):
                continue
            if split_buildings:
                out.append(("fill", g, col, alpha, nonzero))
                continue
            cur.extend(g)
            if len(cur) >= chunk:
                out.append(("fill", cur, col, alpha, nonzero))
                cur = []
        if cur:
            out.append(("fill", cur, col, alpha, nonzero))

    def lines(Ps, col, w, dash=None, alpha=1.0, outline=False):
        for P in Ps:
            if len(P) >= 2 and _bm_hit(P, box):
                (outl if outline else out).append(("line", P, col, w, list(dash) if dash else None, alpha))

    # ground: tree cover, fields, parks / grass (satellite first, mapped areas over it)
    if lay["trees"]:
        fills(L["lc"].get("trees", []), BM_COL["tree"])
    if lay["fields"]:
        fills(L["lc"].get("farmland", []) + L["lc"].get("orchard", []), BM_COL["field"])
        fills([z["rings"] for z in L["zones"] if z["kind"] == "agri"], BM_COL["field"])
    if lay["green"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") != "wood"], BM_COL["park"])
    if lay["trees"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") == "wood"], BM_COL["tree"])
    # contours
    if lay["contours"]:
        cs = L["contours"]
        if lay["contours"] == "height":
            zs = [c[1] for c in cs if c[1] is not None]
            z0, z1 = (min(zs), max(zs)) if zs else (0.0, 1.0)
            for major, z, P in cs:
                col = _bm_ramp((z - z0) / max(1.0, z1 - z0)) if z is not None else BM_COL["contour"]
                lines([P], col, BM_LW["contour_topo"][1 if major else 0])
        else:
            for major, z, P in cs:
                lines([P], BM_COL["contour"], BM_LW["contour"][1 if major else 0])
    # streets
    st = lay["streets"]
    if st == "muted":                                     # round 4 (S2): light fill, light closed edges, after fills
        fills(L["street_areas"], BM_MUTED["road"], nonzero=False)
        for cl, P in L["streets_out"]:
            lines([P], BM_MUTED["road_edge"], BM_LW[cl] * (1.6 if cl != "path" else 1.0))
        for g in L["street_areas"]:                       # every ring of a street area closed (no open survey run)
            lines([list(R) + [R[0]] for R in g if len(R) >= 3], BM_MUTED["road_edge"], BM_MUTED["lw"], outline=True)
    elif st is True or st == "faint":
        faint = st == "faint"
        fills(L["street_areas"], BM_FAINT["road"] if faint else BM_COL["road"], nonzero=False)
        for cl, P in L["streets_out"]:                    # beyond the frame: OpenStreetMap centrelines
            lines([P], BM_FAINT["road_line"] if faint else BM_COL["road"], BM_LW[cl] * (1.6 if cl != "path" else 1.0))
        if faint:                                         # round 4 (S2, CHK-3 §1.6): faint modes keep their edges
            for g in L["street_areas"]:
                lines([list(R) + [R[0]] for R in g if len(R) >= 3], BM_FAINT["road_line"], 0.08, outline=True)
        else:
            lines(L["street_edges"], BM_COL["road_edge"], BM_LW["road_edge"], outline=True)
    elif st:
        for cl, P in L["streets_in"] + L["streets_out"]:
            if cl in st:
                lines([P], BM_FAINT["road_line"] if cl != "main" else BM_COL["road_edge"], BM_LW[cl])
    # the stream: ONE drawing (the site board's water and its edge inside the frame, OpenStreetMap's course beyond).
    # M3 (30 Oct): drawn by M5 (common/water.py water_plan, page mm) when the script includes it: one "water" item
    # that basemap_draw hands to water_plan after the map's T (else the plain fill and edge, as before)
    if lay["stream"]:
        if callable(globals().get("water_plan")):
            ws = [g for g in L["water"] if g and len(g[0]) >= 3 and _bm_hit(g[0], box)]
            if ws:
                out.append(("water", ws, [P for P in L["water_edge"] if len(P) >= 2 and _bm_hit(P, box)], 1.0))
        else:
            fills(L["water"], BM_COL["water"], nonzero=False)
            lines(L["water_edge"], BM_COL["water_edge"], BM_LW["water_edge"])
        if st is True or st in ("faint", "muted"):
            fills([[R] for R in L["decks"]], BM_MUTED["road"] if st == "muted" else
                  (BM_FAINT["road"] if st == "faint" else BM_COL["road"]))
        for P in L["covered"]:
            lines([P], BM_COL["water_edge"], BM_LW["covered"], BM_COVERED_DASH, outline=True)
        fills(L["water_out"], BM_COL["water"], nonzero=False)
        for kind, P in L["waterways_out"]:
            lines([P], BM_COL["water"], BM_LW["river_osm" if kind == "river" else "stream_osm"])
    # buildings
    bl = lay["buildings"]
    if bl == "muted" and not callable(globals().get("bld_plan_items")):
        _BM_WARN.append(u"WARNING: basemap buildings 'muted' need common/buildings.py (M11): drawn as plain light "
                        u"fills with their outlines instead.")
        fills([b["rings"] for b in L["buildings"]], BM_MUTED["bld"])
        for bk in L.get("blocks") or []:
            lines([list(R) + [R[0]] for R in bk["rings"] if len(R) >= 3], BM_MUTED["bld_edge"], BM_MUTED["lw"],
                  outline=True)
    elif bl == "muted":                                   # round 4 (S2, G-R4-4): light houses, ONE closed outline per
        for it in bld_plan_items(L["buildings"], blocks=L.get("blocks"), scale_den=scale_den or 5000.0, box=box,
                                 roof="none", fill=BM_MUTED["bld"], edge=BM_MUTED["bld_edge"],   # block, no roof marks
                                 her_fill=BM_MUTED["her"], her_edge=BM_MUTED["her_edge"], lw=BM_MUTED["lw"]):
            (outl if it[0] == "line" else out).append(it)
    elif bl in ("plan", "plan_faint"):                      # M11: outline per block + roof reading, no stripes
        pf = globals().get("bld_plan_items")
        if callable(pf):
            faint = bl == "plan_faint"
            blocks = L.get("blocks")
            for it in pf(L["buildings"], blocks=blocks, scale_den=scale_den or 5000.0, box=box,
                         fill=BM_FAINT["bld_veryfaint"] if faint else None,
                         edge=BM_FAINT["road_line"] if faint else None,
                         roof_col=BM_FAINT["bld"] if faint else None,
                         her_fill=BM_COL["her"] if not faint else "F1E6E5",
                         her_edge=BM_COL["her_edge"] if not faint else "CDAAAA"):
                (outl if it[0] == "line" else out).append(it)   # roof marks and outlines after every fill
        else:
            _BM_WARN.append(u"WARNING: basemap buildings '{}' need common/buildings.py (M11): drawn faint "
                            u"instead.".format(bl))
            fills([b["rings"] for b in L["buildings"]], BM_FAINT["bld"])
    elif bl:
        if bl is True:
            fills([b["rings"] for b in L["buildings"] if not b.get("her")], BM_COL["bld"])
            fills([b["rings"] for b in L["buildings"] if b.get("her")], BM_COL["her"])
            for b in L["buildings"]:
                if b.get("her") or b.get("osm"):
                    lines([R + R[:1] for R in b["rings"][:b.get("np", len(b["rings"]))]],
                          BM_COL["her_edge"] if b.get("her") else BM_COL["bld_osm_edge"],
                          BM_LW["her_edge"] if b.get("her") else BM_LW["osm_edge"], outline=True)
            for bk in L.get("blocks") or []:                # round 4 (S2, CHK-3 §1.5): survey houses get their edge too
                if not bk.get("her"):
                    lines([list(R) + [R[0]] for R in bk["rings"] if len(R) >= 3], BM_COL["bld_osm_edge"],
                          BM_LW["osm_edge"], outline=True)
        else:
            fills([b["rings"] for b in L["buildings"]],
                  BM_FAINT["bld_veryfaint"] if bl == "veryfaint" else BM_FAINT["bld"])
    if lay["stream"] and (st is True or bl is True or bl == "plan"):
        lines(L["bridges"], BM_COL["ink"], BM_LW["bridge"], outline=True)
    elif lay["stream"] and bl == "muted":                 # round 4: bridges in the muted edge tone, a little heavier
        lines(L["bridges"], BM_MUTED["bld_edge"], 2.0 * BM_MUTED["lw"], outline=True)
    out.extend(outl)                                      # round 4 (S2): every outline after every fill
    # M3 (30 Oct): the study area (one outline, one style, on top of the base) and the place names
    if lay.get("study_area"):
        for it in basemap_study_items(D):
            if _bm_hit(it[1], box):
                out.append(it)
    if lay.get("names"):
        for n, p in basemap_names(box, D):
            out.append(("text", n, p, BM_NAME_MM, BM_MUTED["name"] if mode == "muted" else BM_COL["ink"], False,
                        "MC"))
    return out


def basemap_draw(items, T, fill_fn, line_fn, text_fn=None, water_opts=None):
    """draws items through the caller's page: T(p) survey m -> page point; fill_fn(rings, hex, alpha, nonzero);
    line_fn(pts, hex, width_mm, dash_mm, alpha); text_fn(s, (x, y), size_mm, hex, bold, align) (texts are left out
    without it). Returns the number of items drawn. M3 (30 Oct): a "water" item (the stream, when the script includes
    M5 common/water.py) is drawn by water_plan(ring in page mm, k, holes=its islands, **water_opts) through the same
    three functions (k = page mm per survey m, from T); if M5 fails, the plain fill and bank line (a WARNING in
    basemap_warnings())."""
    import math as _m
    n = 0
    for it in items:
        if it[0] == "fill":
            fill_fn([[T(p) for p in R] for R in it[1]], it[2], it[3], it[4])
        elif it[0] == "line":
            line_fn([T(p) for p in it[1]], it[2], it[3], it[4], it[5])
        elif it[0] == "text" and text_fn is not None:
            text_fn(it[1], T(it[2]), it[3], it[4], it[5], it[6])
        elif it[0] == "water":
            p0 = it[1][0][0][0][0], it[1][0][0][0][1]          # first point of the first ring of the first group
            a, b = T(p0), T((p0[0] + 100.0, p0[1]))
            k = _m.hypot(b[0] - a[0], b[1] - a[1]) / 100.0
            try:
                wp = globals()["water_plan"]                # M5 (common/water.py), present: _bm_items checked it
                for g in it[1]:
                    hs = [[T(p) for p in R] for R in g[1:] if len(R) >= 3]     # islands: open, untextured (A2 fix)
                    wl = wp([T(p) for p in g[0]], k, holes=hs, **(water_opts or {}))
                    for s_ in wl.shapes():
                        if s_[0] == "poly" and len(s_[1]) >= 3:
                            al = s_[5] if len(s_) > 5 and s_[5] is not None else 1.0
                            ho = [list(R) for R in (s_[6] if len(s_) > 6 and s_[6] else ())]
                            if s_[2]:
                                fill_fn([list(s_[1])] + ho, s_[2], al, not ho)          # even-odd with holes
                            if s_[3]:
                                line_fn(list(s_[1]) + [s_[1][0]], s_[3], s_[4] or 0.1, None, al)
                        elif s_[0] == "line" and len(s_[1]) >= 2:
                            line_fn(list(s_[1]), s_[2], s_[3], s_[4] if len(s_) > 4 else None, 1.0)
                        elif s_[0] == "text" and text_fn is not None:
                            text_fn(s_[1], (s_[2], s_[3]), s_[4], s_[5], s_[6] if len(s_) > 6 else False,
                                    s_[7] if len(s_) > 7 else "L")
            except Exception as ex_:
                _BM_WARN.append(u"WARNING: basemap: the M5 water drawing failed ({}: {}); the stream is drawn as the "
                                u"base map's own fill.".format(type(ex_).__name__, ex_))
                fill_fn([[T(p) for p in R] for g in it[1] for R in g], BM_COL["water"], 1.0, False)
                for P in it[2]:
                    line_fn([T(p) for p in P], BM_COL["water_edge"], BM_LW["water_edge"], None, 1.0)
        else:
            continue
        n += 1
    return n


# ------------------------------------------------------------------------------------------- key-map cut lines
def _bm_clip_convex(a, b, poly):
    """the part of segment a-b inside the convex polygon poly (any turn), or None"""
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = len(poly)
    s = sum((poly[(i + 1) % n][0] - poly[i][0]) * (poly[(i + 1) % n][1] + poly[i][1]) for i in range(n))
    ccw = s < 0
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        ex, ey = q[0] - p[0], q[1] - p[1]
        nx, ny = (-ey, ex) if ccw else (ey, -ex)          # inward normal
        den = nx * dx + ny * dy
        num = nx * (a[0] - p[0]) + ny * (a[1] - p[1])
        if abs(den) < 1e-12:
            if num < 0:
                return None
            continue
        t = -num / den
        if den > 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return (a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)


def basemap_cut_ids(ids, looks=None):
    """cuts for basemap_cut_items from the level module (common/levels.py, its data included before it): the ends
    and their names of each cut id; looks = {id: -1} to turn a marker round"""
    ends, labs = globals().get("level_ends"), globals().get("level_end_labels")
    if not callable(ends) or not callable(labs):
        raise RuntimeError("basemap_cut_ids needs the level module: include ../common/data/LEVELS.py and "
                           "../common/levels.py")
    out = []
    for cid in ids:
        a, b = ends(cid)
        out.append((a, b, labs(cid), (looks or {}).get(cid, 1)))
    return out


# M4 key map: keymap_items and basemap_cut_items moved to keymap.py (round 4 S2: R01 red symbol, names, muted base)


# ------------------------------------------------------------------------------------------- writing (site board)
def _bm_r(P, nd=1):
    return [[round(p[0], nd), round(p[1], nd)] for p in P]


def _bm_clip_rect(P, closed, r):
    """P clipped to the axis-aligned rectangle r = (u0, v0, u1, v1) (frame-local): a polygon (Sutherland-Hodgman,
    one ring or None) or a polyline (its runs inside)"""
    u0, v0, u1, v1 = r
    if closed:
        R = list(P)
        for k_, lim, keep_ge in ((0, u0, True), (0, u1, False), (1, v0, True), (1, v1, False)):
            if not R:
                return None
            nxt = []
            for i in range(len(R)):
                p, q = R[i - 1], R[i]
                pin = p[k_] >= lim if keep_ge else p[k_] <= lim
                qin = q[k_] >= lim if keep_ge else q[k_] <= lim
                if qin:
                    if not pin:
                        t = (lim - p[k_]) / (q[k_] - p[k_])
                        nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                    nxt.append(q)
                elif pin:
                    t = (lim - p[k_]) / (q[k_] - p[k_])
                    nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            R = nxt
        return R if len(R) >= 3 else None
    runs, cur = [], []
    for a, b in zip(P, P[1:]):
        t0, t1 = 0.0, 1.0
        d = (b[0] - a[0], b[1] - a[1])
        ok = True
        for k_, lim, sgn in ((0, u0, 1), (0, u1, -1), (1, v0, 1), (1, v1, -1)):
            den = d[k_] * sgn
            num = (a[k_] - lim) * sgn
            if abs(den) < 1e-12:
                if num < 0:
                    ok = False
                    break
                continue
            t = -num / den
            if den > 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
            continue
        p0 = (a[0] + d[0] * t0, a[1] + d[1] * t0)
        p1 = (a[0] + d[0] * t1, a[1] + d[1] * t1)
        if cur and (abs(cur[-1][0] - p0[0]) > 1e-9 or abs(cur[-1][1] - p0[1]) > 1e-9):
            if len(cur) > 1:
                runs.append(cur)
            cur = []
        if not cur:
            cur = [p0]
        cur.append(p1)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def basemap_export(S, log=None):
    """SITE BOARD ONLY, once a run after the site model and its land cover are made (S = the site model; S.osm the
    parsed OpenStreetMap file): writes BASEMAP_FILE. Inside the analysis frame the site board's own layers (the
    ones p.06 draws), between the frame and the extent OpenStreetMap's, cut at the frame's edge so nothing is drawn
    twice; contours (survey, frame only) carry their height. Returns the path, or None (a WARNING in log)."""
    import time as _t
    log = log if log is not None else []
    # unchanged site model (same build_site key, S.site_key) = the file on disk is kept, not made again
    kf = BASEMAP_FILE + ".key"
    key = u"{}|{}|{}".format(BASEMAP_FORMAT, globals().get("SCRIPT_VERSION", ""), getattr(S, "site_key", None) or "")
    try:
        if getattr(S, "site_key", None) and _bm_os.path.isfile(BASEMAP_FILE) and _bm_os.path.isfile(kf):
            with open(kf, "r", encoding="utf-8") as fh:
                if fh.read().strip() == key:
                    log.append(u"Shared basemap unchanged (same site model): {} kept.".format(BASEMAP_FILE))
                    return BASEMAP_FILE
    except Exception:
        pass
    try:
        F = S.F
        loc = lambda p: F.local(p[0], p[1])
        wld = lambda q: F.world(q[0], q[1])
        fr = (F.u0, F.v0, F.u1, F.v1)
        us = [loc(p)[0] for _, p in BASEMAP_REACH] + [F.u0, F.u1]
        vs = [loc(p)[1] for _, p in BASEMAP_REACH] + [F.v0, F.v1]
        ex = (min(us) - BASEMAP_MARGIN, min(vs) - BASEMAP_MARGIN, max(us) + BASEMAP_MARGIN, max(vs) + BASEMAP_MARGIN)
        # the ring between frame and extent as four rectangles that do not overlap (frame-local)
        ring = [(ex[0], ex[1], ex[2], fr[1]), (ex[0], fr[3], ex[2], ex[3]),
                (ex[0], fr[1], fr[0], fr[3]), (fr[2], fr[1], ex[2], fr[3])]

        def outside_poly(P):
            Q = [loc(p) for p in P]
            res = []
            for r in ring:
                c = _bm_clip_rect(Q, True, r)
                if c:
                    res.append(_bm_r([wld(q) for q in c]))
            return res

        def outside_line(P):
            Q = [loc(p) for p in P]
            return [_bm_r([wld(q) for q in run]) for r in ring for run in _bm_clip_rect(Q, False, r)]

        def in_frame_name(u):
            u_, v_ = loc((u["cx"], u["cy"]))
            return fr[0] <= u_ <= fr[2] and fr[1] <= v_ <= fr[3]

        def in_ring(p):
            u, v = loc(p)
            return ex[0] <= u <= ex[2] and ex[1] <= v <= ex[3] and not (fr[0] <= u <= fr[2] and fr[1] <= v <= fr[3])
        L = dict(lc={}, zones=[], contours=[], street_areas=[], street_edges=[], streets_in=[], streets_out=[],
                 water=[], water_edge=[], decks=[], covered=[], water_out=[], waterways_out=[], buildings=[],
                 bridges=[], blocks=[], study=[], names=[], street_names=[])
        sn_best = {}                                      # round 4 (S2, G-R4-9 U55): street name -> longest run

        def street_name(tags, P, cl):
            nm_ = ((tags or {}).get("name") or u"").strip()
            if not nm_ or cl == "path" or len(P) < 2:
                return
            Ln = sum(_bm_math.hypot(b_[0] - a_[0], b_[1] - a_[1]) for a_, b_ in zip(P, P[1:]))
            if nm_ not in sn_best or Ln > sn_best[nm_][0]:
                sn_best[nm_] = (Ln, cl, P)
        mains = set(globals().get("MAIN_ROADS") or ("motorway", "trunk", "primary", "secondary", "tertiary"))
        peds = set(globals().get("PED") or ("footway", "path", "pedestrian", "steps", "cycleway", "bridleway",
                                             "track", "corridor"))
        skip = set(globals().get("SKIP_HW") or ("proposed", "construction", "platform", "bus_stop", "elevator"))
        ccls = lambda hw: "path" if hw in peds else ("main" if hw in mains else "lane")
        # ---- inside the frame: the site board's layers
        lcf = globals().get("r28e_lc")
        for key in ("trees", "farmland", "orchard"):
            try:
                groups = lcf(S, key) if callable(lcf) else [[P] for P in (getattr(S, "lc", None) or {}).get(key) or []]
            except Exception:
                groups = [[P] for P in (getattr(S, "lc", None) or {}).get(key) or []]
            L["lc"][key] = [[_bm_r(P) for P in g if len(P) >= 3] for g in groups]
        for z in getattr(S, "zones", None) or []:
            if z["kind"] in ("green", "agri"):
                L["zones"].append(dict(kind=z["kind"], sub=z.get("sub"), rings=[_bm_r(P) for P in z["Ps"] + z["Hs"]]))
        z_at = getattr(S, "z_at", None)
        for major, P in getattr(S, "contours", None) or []:
            z = None
            if callable(z_at):
                try:
                    zs = sorted(z_at(p[0], p[1]) for p in P[::max(1, len(P) // 9)])
                    z = round(zs[len(zs) // 2], 1)     # round 3 (B2, P11.1 relief): median to 0.1 m (was 5 m steps)
                except Exception:
                    z = None
            L["contours"].append([bool(major), z, _bm_r(P)])
        for rg in getattr(S, "road_net", None) or []:
            L["street_areas"].append([_bm_r(rg["P"])] + [_bm_r(H) for H in rg.get("H", [])])
        L["street_edges"] = [_bm_r(P) for P in getattr(S, "road_lines_net", None) or []] + \
            [_bm_r(r_["P"]) for r_ in S.roads if not r_.get("w")]
        L["streets_in"] = [[ccls((r_.get("tags") or {}).get("highway")), _bm_r(r_["P"])] for r_ in S.roads] + \
            [["path", _bm_r(r_["P"])] for r_ in getattr(S, "paths", None) or []]
        for r_ in S.roads:
            street_name(r_.get("tags"), r_["P"], ccls((r_.get("tags") or {}).get("highway")))
        L["water"] = [[_bm_r(wt["P"])] + [_bm_r(H) for H in wt.get("H", [])] for wt in S.water]
        L["water_edge"] = [_bm_r(P) for P in getattr(S, "water_outline", None) or []]
        L["decks"] = [_bm_r(P) for P in getattr(S, "decks", None) or []]
        L["covered"] = [_bm_r(P) for P in getattr(S, "covered", None) or []]
        L["bridges"] = [_bm_r(P) for P in getattr(S, "bridges", None) or []]
        # buildings: one outline per building (build_site merged its pieces: revision 30 Oct, G7) with its height,
        # and the blocks (buildings sharing a wall as ONE outline, S.blocks): the plan's outline layer, so no party
        # wall, survey tick or label split is ever drawn as a line
        idx_of = {}
        for i_u, u in enumerate(S.bld):
            parts = [_bm_r(P) for P in u["parts"] if len(P) >= 3]
            if parts:
                idx_of[i_u] = len(L["buildings"])
                tg = u.get("tags") or {}
                her = u.get("fabric") in ("monument", "sacred") or bool(tg.get("historic")) or \
                    tg.get("amenity") == "place_of_worship"
                L["buildings"].append(dict(rings=parts + [_bm_r(H) for H in (u.get("holes") or [])], np=len(parts),
                                           her=her, osm=u.get("src") in ("osm", "osm+label"),
                                           h=round(float(u.get("h") or 0.0), 2), floors=int(u.get("floors") or 0)))
                if her and (u.get("name") or "").strip() and in_frame_name(u):
                    L["names"].append([u["name"].strip(), [round(u["cx"], 1), round(u["cy"], 1)]])
        blocks = getattr(S, "blocks", None)
        if blocks is None and callable(globals().get("bld_blocks")):
            blocks = bld_blocks(S.bld)
        for bk in blocks or []:
            mem = [idx_of[i] for i in bk.get("units", []) if i in idx_of]
            L["blocks"].append(dict(rings=[_bm_r(bk["outer"])] + [_bm_r(H) for H in bk.get("holes") or []],
                                    her=bool(mem) and all(L["buildings"][i]["her"] for i in mem)))
        L["study"] = [_bm_r(P) for P in (getattr(S, "r28_study", None) or globals().get("R28_STUDY_COPY") or [])]
        L["names"] = [[n, [round(p[0], 1), round(p[1], 1)]] for n, p in BASEMAP_REACH] + L["names"]
        n_in = len(L["buildings"])
        # ---- the ring between frame and extent: OpenStreetMap
        osm = getattr(S, "osm", None)
        n_out = 0
        if osm:
            Pj = osm.get("P")
            zc = globals().get("zone_class")
            chain = globals().get("chain_segments")
            for refs, tags in osm["ways"].values():
                if len(refs) < 2:
                    continue
                P = [p for p in (Pj(r) for r in refs) if p]
                if len(P) < 2:
                    continue
                closed = refs[0] == refs[-1] and len(P) >= 4
                if "building" in tags:
                    if closed:
                        c = (sum(p[0] for p in P[:-1]) / (len(P) - 1), sum(p[1] for p in P[:-1]) / (len(P) - 1))
                        if in_ring(c):
                            her = bool(tags.get("historic")) or tags.get("amenity") == "place_of_worship" or \
                                tags.get("building") in ("mosque", "church", "synagogue", "temple")
                            lv = tags.get("building:levels")
                            try:
                                lv = int(float(lv)) if lv else 0
                            except ValueError:
                                lv = 0
                            L["buildings"].append(dict(rings=[_bm_r(P[:-1])], np=1, her=her, osm=True, h=0.0,
                                                       floors=lv))
                            L["blocks"].append(dict(rings=[_bm_r(P[:-1])], her=her))
                            n_out += 1
                    continue
                hw = tags.get("highway")
                if hw and hw not in skip and tags.get("area") != "yes":
                    runs_ = outside_line(P)
                    L["streets_out"].extend([ccls(hw), run] for run in runs_)
                    for run in runs_:
                        street_name(tags, run, ccls(hw))
                    continue
                ww = tags.get("waterway")
                if ww in ("river", "stream", "canal"):
                    L["waterways_out"].extend(["river" if ww == "river" else "stream", run] for run in outside_line(P))
                    continue
                if closed:
                    if tags.get("natural") == "water" or tags.get("waterway") == "riverbank":
                        L["water_out"].extend([R] for R in outside_poly(P[:-1]))
                        continue
                    k = zc(tags) if callable(zc) else None
                    if k and k[0] in ("green", "agri"):
                        rs = outside_poly(P[:-1])
                        if rs:
                            L["zones"].append(dict(kind=k[0], sub=k[1], rings=rs))
            for mem, tags in osm.get("rels") or []:
                if tags.get("type") != "multipolygon" or "building" in tags or tags.get("ref:whc") or \
                        not callable(zc) or not callable(chain):
                    continue
                k = zc(tags)
                if not k or k[0] not in ("green", "agri"):
                    continue
                outer = []
                for ref, role in mem:
                    if role != "inner" and ref in osm["ways"]:
                        P = [p for p in (Pj(r) for r in osm["ways"][ref][0]) if p]
                        if len(P) >= 2:
                            outer.append([(p[0], p[1]) for p in P])
                for c in chain(outer, 0.05):
                    if len(c) >= 4:
                        rs = outside_poly(c[:-1] if c[0] == c[-1] else c)
                        if rs:
                            L["zones"].append(dict(kind=k[0], sub=k[1], rings=rs))
        else:
            log.append(u"WARNING: shared basemap: no OpenStreetMap in the site model, so it ends at the analysis frame.")
        for nm_, (Ln, cl, P) in sn_best.items():           # the label point: the run's middle, along its direction
            half, acc = Ln / 2.0, 0.0
            for a_, b_ in zip(P, P[1:]):
                d_ = _bm_math.hypot(b_[0] - a_[0], b_[1] - a_[1])
                if acc + d_ >= half and d_ > 1e-9:
                    t_ = (half - acc) / d_
                    ang = _bm_math.degrees(_bm_math.atan2(b_[1] - a_[1], b_[0] - a_[0]))
                    L["street_names"].append([nm_, [round(a_[0] + (b_[0] - a_[0]) * t_, 1),
                                                    round(a_[1] + (b_[1] - a_[1]) * t_, 1)], round(ang, 1), cl,
                                              round(Ln, 1)])
                    break
                acc += d_
        corners = lambda b: [_bm_r([wld(q)])[0] for q in ((b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3]))]
        out = dict(format=BASEMAP_FORMAT, source=u"{} · {}".format(globals().get("SCRIPT_VERSION", "site board"),
                                                                  _t.strftime("%Y-%m-%d %H:%M")),
                   frame=_bm_r(globals().get("SITE_FRAME_LK") or [wld(q) for q in ((fr[0], fr[1]), (fr[2], fr[1]),
                                                                                    (fr[2], fr[3]), (fr[0], fr[3]))]),
                   extent=corners(ex), reach=[[n, list(p)] for n, p in BASEMAP_REACH], layers=L,
                   note=u"survey m (0.1 m); inside the analysis frame the site board's layers (survey, OpenStreetMap, "
                        u"ESA WorldCover 2021), beyond it OpenStreetMap (Data/bergama_osm.osm, ODbL); contours from "
                        u"the survey, frame only, height = the terrain at their points to the nearest 5 m")
        _bm_os.makedirs(_bm_os.path.dirname(BASEMAP_FILE), exist_ok=True)
        with open(BASEMAP_FILE, "w", encoding="utf-8") as fh:
            _bm_json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        for k_ in list(_BM_MEMO):
            if k_ == BASEMAP_FILE or (isinstance(k_, tuple) and k_[0] == "items"):
                _BM_MEMO.pop(k_, None)
        if getattr(S, "site_key", None):
            with open(kf, "w", encoding="utf-8") as fh:
                fh.write(key)
        log.append(u"Shared basemap written ({}): {:,} buildings in the frame, {:,} beyond it, {:,} contours, extent "
                   u"{:,.0f} x {:,.0f} m.".format(BASEMAP_FILE, n_in, n_out, len(L["contours"]), ex[2] - ex[0],
                                                 ex[3] - ex[1]))
        return BASEMAP_FILE
    except Exception as ex_:
        import traceback as _tb
        log.append(u"WARNING: the shared basemap was not written ({}):\n{}".format(ex_, _tb.format_exc()))
        return None


# ---- round 4 (S2, 1 Nov 2026): the study clip, the map-layer draw order and the key-map module ride with the basemap,
# so every script that includes basemap.py has them (never include them a second time)
#@include study_clip.py
#@include map_layers.py
#@include keymap.py
