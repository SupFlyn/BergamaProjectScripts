# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE01 FREE v1.1 (14 Nov 2026; v1.1 = run 2 check: WorldCover's 10 m squares showed as stair-stepped blocks over the 2023 image's 0.5 m classes: WorldCover is now used only outside the 2023 image's extent), slide 1 (analysis): where the ground is free and where it is not,
with the site photos. Redoes SUBMISSION_SON p6 ("The stream edge and where we can build") on the one MapBase.

What Aras asked (14 Nov 2026 12:33 UTC): "p6 that we can benefit off however it should be corrected with the latest
basemap info. From there we gonna get more clear which areas are more free and which are not. We gonna include site
photos aswell"; 12:38 UTC: "use same basemap ... don't ever redraw anything ... cache it and make it usable".

Method (all from the MapBase cache, nothing redrawn): every 2 m cell of the frame gets ONE ground class, the first of
this order that covers its centre: building, street, water (MapBase survey + OSM), car park (OSM), grounds in use
(school, mosque, cemetery, archaeological, sports: OSM), park (OSM + survey), fields and orchards (OSM + WorldCover),
tree cover (2023 image + OSM woods + WorldCover outside the image), bare ground (2023 image), grass and loose ground (2023 image + OSM
grass + WorldCover grass / shrubs), else unbuilt with no recorded use (yards, courts, plots). Areas = cells x 4 m2,
counted inside the study area. FREE = car parks + bare + grass / loose ground; its 8 largest joined pieces inside the
study area get a letter. The map shows the same classes as vector fills under MapBase's buildings, streets and water.
Photos: the 8 site photos of 1 Oct 2026 (selinus_board_data SEAM_PACK, 640 x 480, GPS points; ring = GPS error).

Outputs (Downloads/Bergama/output/bergama_page01_free/): FreeGround.pdf, FreeGround.svg, review/ PNGs; the class
raster cache cached/bergama_page01_free/free_ground.json (areas, sites) for later pages.
Reads: Data/bergama_pages_common.py (v3.5+), Data/bergama_access_heritage.json (frame), Data/selinus_board_data.py
(photos), the newest MapBase script and its cache. Grasshopper: a Button on any input runs it; input scale (1:2,500).
"""
import os, time, math, json, re, base64, zlib

VERSION = "v1.1"
GH_LABEL = "Page01Free"
OUT_FOLDER = "bergama_page01_free"
LOG_NAME = "bergama_page01_free_log.txt"
GH_INPUTS = {"scale": "int 1000..10000 = 2500"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
PHOTO_DATA = os.path.join("Data", "selinus_board_data.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "FreeGround"
CELL = 2.0                         # m: the counting raster
N_SITES = 8                        # lettered free pieces
PHOTO_W = 120.0                    # mm: the photo column
# class key, legend group, words, fill (palette refs of the project; warm = free, greens = kept, greys = built)
CLASSES = [
    ("building", "BUILT", u"Buildings (MapBase: survey, OSM, 2023 image)", "8E8F8A"),
    ("street", "BUILT", u"Streets and roads (survey; OSM widths beyond it)", "FFFFFF"),
    ("water", "BUILT", u"Stream and water (survey, OSM)", "A2B6B5"),
    ("parking", "FREE", u"Car parks (OSM)", "C2703D"),
    ("used", "IN USE", u"Grounds in use: schools, mosques, cemeteries, archaeological, sports (OSM)", "BDB3C9"),
    ("park", "GREEN", u"Parks and gardens (OSM, survey)", "89986A"),
    ("farm", "GREEN", u"Fields and orchards (OSM, WorldCover)", "C3C49A"),
    ("trees", "GREEN", u"Tree cover (2023 image, OSM woods, WorldCover)", "70754C"),
    ("bare", "FREE", u"Bare ground (2023 image)", "D9A55B"),
    ("grass", "FREE", u"Grass and loose ground (2023 image, OSM, WorldCover)", "EAD8A0"),
    ("other", "OPEN", u"Unbuilt, no recorded use: yards, courts, plots", "F3F0E8")]
GROUPS = [("BUILT", u"NOT FREE: BUILT"), ("IN USE", u"NOT FREE: IN USE"), ("GREEN", u"GREEN, KEPT"),
          ("FREE", u"FREE TO CHANGE"), ("OPEN", u"OPEN, USE NOT RECORDED")]
FREE = ("parking", "bare", "grass")


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


class Raster(object):
    """bit rows over the frame box (bit i of row j = cell i, j; row 0 at the south)"""
    def __init__(self, b, c):
        self.b, self.c = b, c
        self.nx, self.ny = int(math.ceil((b[2] - b[0]) / c)), int(math.ceil((b[3] - b[1]) / c))

    def empty(self):
        return [0] * self.ny

    def fill(self, rows, rings, xor=False):
        """rings (survey m) into rows: each ring its own even-odd span fill (cell centres), OR'd (xor: XOR'd, so
        holes punch); crossings gathered edge by edge (each edge only touches its own rows)"""
        b, c, nx, ny = self.b, self.c, self.nx, self.ny
        for R in rings:
            if len(R) < 3:
                continue
            Q = [((p[0] - b[0]) / c, (p[1] - b[1]) / c) for p in R]
            X = {}
            for i in range(len(Q)):
                a, e = Q[i - 1], Q[i]
                if a[1] == e[1]:
                    continue
                lo, hi = (a, e) if a[1] < e[1] else (e, a)
                j0, j1 = max(0, int(math.ceil(lo[1] - 0.5))), min(ny - 1, int(math.ceil(hi[1] - 0.5)) - 1)
                if j1 < j0:
                    continue
                sl = (hi[0] - lo[0]) / (hi[1] - lo[1])
                for j in range(j0, j1 + 1):
                    X.setdefault(j, []).append(lo[0] + (j + 0.5 - lo[1]) * sl)
            for j, xs in X.items():
                xs.sort()
                m = 0
                for xa, xb in zip(xs[0::2], xs[1::2]):
                    i0, i1 = max(0, int(math.ceil(xa - 0.5))), min(nx - 1, int(math.floor(xb - 0.5)))
                    if i1 >= i0:
                        m |= ((1 << (i1 - i0 + 1)) - 1) << i0
                if m:
                    rows[j] = (rows[j] ^ m) if xor else (rows[j] | m)
        return rows

    def lines(self, rows, runs, w):
        """polylines (survey m) of width w m as rectangles per segment"""
        rings = []
        for P in runs:
            for a, e in zip(P, P[1:]):
                dx, dy = e[0] - a[0], e[1] - a[1]
                L = math.hypot(dx, dy)
                if L < 1e-6:
                    continue
                nx_, ny_ = -dy / L * w / 2.0, dx / L * w / 2.0
                rings.append([(a[0] + nx_, a[1] + ny_), (e[0] + nx_, e[1] + ny_), (e[0] - nx_, e[1] - ny_),
                              (a[0] - nx_, a[1] - ny_)])
        return self.fill(rows, rings)


def photos_of(log):
    p = os.path.join(BERGAMA_ROOT, PHOTO_DATA)
    with open(p, encoding="utf-8") as f:
        s = f.read()
    i = s.index("SEAM_PACK = (")
    blob = u"".join(re.findall(r'"([^"]*)"', s[i:s.index("\n)", i)]))
    P = json.loads(zlib.decompress(base64.b64decode(blob)))["photos"]["items"]
    d = os.path.join(CACHE_DIR, "photos")
    os.makedirs(d, exist_ok=True)
    out = []
    for it in P:
        fp = os.path.join(d, it["file"])
        with open(fp, "wb") as f:
            f.write(base64.b64decode(it["jpeg_b64"]))
        out.append(dict(it, path=fp))
    log.append(u"photos: %d from %s (taken %s)" % (len(out), p, u", ".join(sorted(set(o["taken"][:10] for o in out)))))
    return out


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    D = G["pc_data"](log)
    K = D["key"]
    den = int(globals().get("scale") or K["scale"])
    M = G["Map"](D, den)
    M.w += PHOTO_W + 8.0                                 # the photo column right of the legend column
    MB, C = G["pc_mb_data"](log)
    P_, L_, T_, circle, wrap, tw = G["P_"], G["L_"], G["T_"], G["circle"], G["wrap"], lib["text_w"]
    tm, INK = K["text_mm"], K["ink"]
    col = dict((k_, c_) for k_, g_, w_, c_ in CLASSES)

    # ---- the class sources (survey m rings), straight from the MapBase cache
    A = C["areas"]
    src = {"parking": [R for R, cl, sub, nm in A if cl == "parking"],
           "used": [R for R, cl, sub, nm in A if cl in ("grounds", "worship", "cemetery", "archaeo", "sport")],
           "park": [R for R, cl, sub, nm in A if cl == "park"] + list(C["polys"].get("parks", [])),
           "farm": [R for R, cl, sub, nm in A if cl == "farm"],
           "trees": [R for R, cl, sub, nm in A if cl == "wood"],
           "grass": [R for R, cl, sub, nm in A if cl == "green"]}
    xsrc = {"farm": [C["lc"].get("farmland", []), C["lc"].get("orchard", [])],     # XOR sets (rings with holes)
            "trees": [C["veg"].get("trees", []), C["lc"].get("trees", [])],
            "bare": [C["veg"].get("bare", [])],
            "grass": [C["veg"].get("grass", []), C["lc"].get("grass", []), C["lc"].get("shrub", [])]}

    # ---- v1.1: the 2023 image's extent (its rings' box); WorldCover only outside it
    vp = [q for v in C["veg"].values() for R in v for q in R]
    ib = (min(q[0] for q in vp), min(q[1] for q in vp), max(q[0] for q in vp), max(q[1] for q in vp)) if vp else None
    wc_sets = [id(C["lc"].get(k_)) for k_ in ("farmland", "orchard", "trees", "grass", "shrub") if C["lc"].get(k_)]

    # ---- the raster: one class per cell
    RS = Raster(D["box"], CELL)
    ny = RS.ny
    full = (1 << RS.nx) - 1
    m = {}
    m["building"] = RS.fill(RS.empty(), [R for R, fab, com, s_, nm in C["bld"]])
    st_ = RS.fill(RS.empty(), C["polys"].get("streets", []), xor=True)
    for P, w, hw, nm in C["osm_streets"]:
        RS.lines(st_, [P], w)
    m["street"] = st_
    wa = RS.fill(RS.empty(), C["polys"].get("river", []), xor=True)
    RS.fill(wa, [R for R, cl, sub, nm in A if cl == "water"])
    m["water"] = RS.lines(wa, C["osm_waterways"], 2.0)
    img = RS.fill(RS.empty(), [[(ib[0], ib[1]), (ib[2], ib[1]), (ib[2], ib[3]), (ib[0], ib[3])]]) if ib else RS.empty()
    for k_ in ("parking", "used", "park", "farm", "trees", "bare", "grass"):
        r_ = RS.fill(RS.empty(), src.get(k_, []))
        for S_ in xsrc.get(k_, []):
            x_ = RS.fill(RS.empty(), S_, xor=True)
            if id(S_) in wc_sets:
                x_ = [a & ~b for a, b in zip(x_, img)]
            r_ = [a | b for a, b in zip(r_, x_)]
        m[k_] = r_
    study = RS.fill(RS.empty(), C.get("calisma") or [], xor=True)
    if not any(study):
        log.append(u"FLAG: no study area in the MapBase cache: areas counted over the whole frame")
        study = [full] * ny
    rem, own = list(study), {}
    remf = [full] * ny
    for k_, g_, w_, c_ in CLASSES:
        if k_ == "other":
            own[k_] = rem
            break
        own[k_] = [a & b for a, b in zip(m[k_], rem)]
        rem = [a & ~b for a, b in zip(rem, m[k_])]
        remf = [a & ~b for a, b in zip(remf, m[k_])]
    a2 = CELL * CELL
    area = dict((k_, sum(bin(r_).count("1") for r_ in own[k_]) * a2) for k_ in own)
    tot = sum(area.values()) or 1.0
    log.append(u"study area %.1f ha (%d m cells, each once): %s" % (tot / 1e4, CELL, u", ".join(
        u"%s %.2f ha %.1f%%" % (k_, area[k_] / 1e4, 100.0 * area[k_] / tot) for k_, g_, w_, c_ in CLASSES)))

    # ---- the free pieces: joined cells of car park + bare + grass inside the study area
    fr = [own["parking"][j] | own["bare"][j] | own["grass"][j] for j in range(ny)]
    cells = set()
    for j, r_ in enumerate(fr):
        while r_:
            lsb = r_ & -r_
            cells.add((lsb.bit_length() - 1, j))
            r_ ^= lsb
    comps = []
    while cells:
        st0 = cells.pop()
        comp, todo = [st0], [st0]
        while todo:
            i, j = todo.pop()
            for q in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
                if q in cells:
                    cells.remove(q)
                    comp.append(q)
                    todo.append(q)
        comps.append(comp)
    comps.sort(key=lambda c_: -len(c_))
    sites = []
    for comp in comps[:N_SITES]:
        mx, my = sum(q[0] for q in comp) / float(len(comp)), sum(q[1] for q in comp) / float(len(comp))
        ci, cj = min(comp, key=lambda q: (q[0] - mx) ** 2 + (q[1] - my) ** 2)
        share = dict((k_, sum(1 for i, j in comp if own[k_][j] >> i & 1) / float(len(comp))) for k_ in FREE)
        sites.append(dict(a=len(comp) * a2, x=D["box"][0] + (ci + 0.5) * CELL, y=D["box"][1] + (cj + 0.5) * CELL,
                          main=max(FREE, key=lambda k_: share[k_]), share=share))
    sites.sort(key=lambda s_: (s_["x"], -s_["y"]))
    for n_, s_ in enumerate(sites):
        s_["id"] = u"ABCDEFGHIJKL"[n_]
    log.append(u"free pieces: %d joined pieces; lettered: %s" % (len(comps), u"; ".join(
        u"%s %.0f m2 (%s)" % (s_["id"], s_["a"], s_["main"]) for s_ in sites)))
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(os.path.join(CACHE_DIR, "free_ground.json"), "w", encoding="utf-8") as f:
        json.dump({"version": VERSION, "made": time.strftime("%Y-%m-%d %H:%M"), "cell_m": CELL,
                   "area_m2": area, "sites": sites}, f, ensure_ascii=False, indent=1)

    # ---- the map: unbuilt ground, the classes (lowest first), then MapBase's water, streets, walls, buildings
    clip = G["PC_CLIP"]
    bx = M.box
    items = [("poly", [[(bx[0], bx[1]), (bx[2], bx[1]), (bx[2], bx[3]), (bx[0], bx[3])]], col["other"], None, 0.0,
              None, "ground_other", 1, None, clip)]
    for k_ in ("grass", "bare", "trees", "farm", "park", "used", "parking"):
        sets = [src.get(k_, [])] + xsrc.get(k_, [])
        for si, S_ in enumerate(sets):                   # OSM areas one by one; image / WorldCover sets even-odd
            rr = [[M.T(p) for p in R] for R in S_ if len(R) >= 3]
            if si == 0:
                for R in rr:
                    items.append(("poly", [R], col[k_], None, 0.0, None, "ground_" + k_, 1, None, clip))
            elif rr:
                items.append(("poly", rr, col[k_], None, 0.0, None, "ground_" + k_, 1, "eo",
                              "wc" if (id(S_) in wc_sets and ib) else clip))
    st = {"street": col["street"], "street_edge": "B9B4AA", "water": col["water"], "water_line": "5C7A86",
          "fab": dict((k_, col["building"]) for k_ in MB["MB_STYLE"]["fab"]),
          "fab_com": dict((k_, col["building"]) for k_ in MB["MB_STYLE"]["fab_com"]), "edge_dark": 0.4}
    mbi, _rows, cnt = G["pc_mapbase"](M, K, log, {"water", "streets", "walls", "buildings", "bridges"}, st)
    items += mbi
    items += G["pc_study"](M, K, log)

    # ---- site letters and photo points
    lab = G["Labels"](M, lib)
    R0 = 2.6
    for s_ in sites:
        q = M.T((s_["x"], s_["y"]))
        items.append(P_([circle(q[0], q[1], R0, 32)], INK, "FFFFFF", 0.3, "free_sites"))
        items.append(T_(s_["id"], q[0], q[1] - 1.1, 3.0, "FFFFFF", "free_sites", True, "C"))
        lab.block_pt(q, R0)
    ph = photos_of(log)
    for n_, p_ in enumerate(ph):
        q = M.T((p_["x"], p_["y"]))
        if not M.inside(q):
            log.append(u"FLAG: photo %d lies outside the frame" % (n_ + 1))
            continue
        r_ = p_["gps_err_m"] * M.k
        if r_ > 2.0:
            items.append(L_(circle(q[0], q[1], r_, 48) + [circle(q[0], q[1], r_, 48)[0]], INK, 0.15, "photo_points",
                            (0.6, 0.6)))
        s = 1.7
        items.append(P_([[(q[0] - s, q[1] - s), (q[0] + s, q[1] - s), (q[0] + s, q[1] + s), (q[0] - s, q[1] + s)]],
                        "FFFFFF", INK, 0.3, "photo_points"))
        items.append(T_(str(n_ + 1), q[0], q[1] - 0.9, 2.6, INK, "photo_points", True, "C"))
        lab.block_pt(q, s)
    items += lab.items

    # ---- legend: groups, each class with its area in the study area
    def sw(c_):
        return lambda x, y: [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0), (x + 4.5, y + 2.0), (x - 4.5, y + 2.0)]],
                                c_, K["grey_line"], 0.1, "legend")]
    legend = []
    for g_, head in GROUPS:
        legend.append((None, head))
        for k_, gg, w_, c_ in CLASSES:
            if gg == g_:
                legend.append((sw(c_), u"%s: %s m2, %.1f%%" % (w_, format(int(round(area[k_])), ",d"),
                                                             100.0 * area[k_] / tot)))
    legend += [(None, u"THE %d LARGEST FREE PIECES IN THE STUDY AREA" % len(sites))]
    def site_sw(t):
        return lambda x, y: [P_([circle(x, y, R0, 32)], INK, "FFFFFF", 0.3, "legend"),
                             T_(t, x, y - 1.1, 3.0, "FFFFFF", "legend", True, "C")]
    legend += [(site_sw(s_["id"]), u"%s m2, mostly %s" % (format(int(round(s_["a"])), ",d"), {
        "parking": u"car park", "bare": u"bare ground", "grass": u"grass and loose ground"}[s_["main"]]))
        for s_ in sites]
    legend += [(lambda x, y: [P_([[(x - 1.7, y - 1.7), (x + 1.7, y - 1.7), (x + 1.7, y + 1.7), (x - 1.7, y + 1.7)]],
                                 "FFFFFF", INK, 0.3, "legend")], u"Site photo point (dashed ring: GPS error)"),
               (lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], K["study"][0], K["study"][1], "legend", (2.4, 0.8))],
                u"Study area (areas above are counted inside it: %.1f ha)" % (tot / 1e4))]
    notes = [u"Each %.0f m cell counted once, in the order of the legend's groups (built first). Free = car parks, "
             u"bare ground, grass and loose ground: no building, street or recorded use on it today." % CELL]
    credit = (u"Sources: survey (Bergama municipality DWG); © OpenStreetMap contributors (ODbL); 2023 satellite image "
              u"classes; ESA WorldCover 2021 (CC BY 4.0). Photos: site visit 1 Oct 2026.")
    items += G["pc_sheet"](M, K, lib, u"Where the ground is free", u"Built, in use, green, and free to change: the "
                           u"study area cell by cell", legend, notes, credit)

    # ---- the photo column: the share bar, then the photos with their numbers and notes
    x0 = M.box[2] + 8.0 + G["PC_SIDE_MM"] + 8.0
    y = M.box[3] - tm["title"]
    items.append(T_(u"STUDY AREA, %.1f HA" % (tot / 1e4), x0, y, tm["legend"], INK, "legend", True))
    y -= 9.0
    xx = x0
    for k_, g_, w_, c_ in CLASSES:
        wk = PHOTO_W * area[k_] / tot
        if wk <= 0:
            continue
        items.append(P_([[(xx, y), (xx + wk, y), (xx + wk, y + 6.0), (xx, y + 6.0)]], c_, K["grey_line"], 0.1, "legend"))
        if wk >= 9.0:
            items.append(T_(u"%.0f%%" % (100.0 * area[k_] / tot), xx + wk / 2.0, y + 1.9, tm["small"],
                            "FFFFFF" if k_ in ("building", "trees", "parking") else INK, "legend", True, "C"))
        xx += wk
    y -= 10.0
    photos = []
    pw, phh = PHOTO_W, PHOTO_W * 0.75
    for n_, p_ in enumerate(ph):
        y -= phh
        photos.append((p_["path"], x0, y, pw, phh))
        y -= 1.0
        lines = wrap(u"%d  %s" % (n_ + 1, p_["description"]), tm["small"], pw, tw)
        for ln in lines:
            y -= tm["small"] * 1.4
            items.append(T_(ln, x0, y, tm["small"], INK, "notes"))
        y -= 4.0
    if y < M.box[1]:
        log.append(u"FLAG: the photo column runs %.0f mm below the map frame" % (M.box[1] - y))
    box_r = [(bx[0], bx[1]), (bx[2], bx[1]), (bx[2], bx[3]), (bx[0], bx[3])]
    clips = {clip: [[box_r]]}
    if ib:
        i0, i1 = M.T((ib[0], ib[1])), M.T((ib[2], ib[3]))
        clips["wc"] = [[box_r, [(i0[0], i0[1]), (i1[0], i0[1]), (i1[0], i1[1]), (i0[0], i1[1])]]]   # box minus image
        log.append(u"WorldCover only outside the 2023 image's extent (survey x %.0f-%.0f, y %.0f-%.0f)" % ib)
    G["pc_write"](lib, M, items, OUT_DIR, NAME, u"Where the ground is free, 1:%d" % den, log, photos=photos,
                  clips=clips)
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


# ---- Grasshopper wiring (same in every script) ----
def chain_fire(v, key):
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
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed = any(v is True for k, v in list(globals().items())
                   if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done")) or \
        any(chain_fire(v, _k + "_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-900:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to export to " + OUT_DIR)
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
