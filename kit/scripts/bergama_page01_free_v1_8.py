# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE01 FREE v1.8 (14 Nov 2026; v1.8 = Aras 16:17 UTC "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN" and the slide01 run 2 layout (tiny map, title over the scale, captions in narrow columns): the map is site_alan turned flat as the Basemap draws it (pages_common SiteMap), across the page top; the legend in as many columns as the page height needs, right of it (north and scale at the page foot); the photos in a grid UNDER the map (full captions, else short ones); v1.7 = slide01 run 2: in the slide panel no grid of full captions fitted (11 FLAGs): at each scale the full captions are tried, then the short ones (the description up to its first ";", camera words dropped); site letters kept inside the frame; v1.6 = slide01 run 1: photo 8's caption ran into the next row and the grid 1 mm past the frame: the grid now measures each caption at the photo width before choosing the photo size; v1.5 = Aras 15:25 UTC "fit every drawing into A3's like the scale is not important": scale 0 (default) = the largest round scale at which map, legend and a photo grid (photos at least PHOTO_MIN mm wide) fit A3 landscape (or the slide sheet's page_mm), centred; v1.4 = the photos are a grid as tall as the map at any scale (1 to 4 columns, the largest photos that fit), so the slide-1 sheet can draw this page at 1:6,000; and Aras 15:23 UTC "dont give sources in the drawings at all": legend words, notes and credit carry no sources, the sources go to the log only; v1.3 = Aras 13:02 UTC "make sure nothing repeats in the slides": the built / green shares live on Page02's land-use ring, so this page gives m2 only for the FREE classes and the lettered pieces, no share bar, no %; v1.2 = run 3 check: the WorldCover clip leaked past the map frame (box XOR image box): now box AND (box minus image); the image edge drawn dashed and keyed (v1.4: not drawn, it is a source line); v1.1 = run 2 check: WorldCover's 10 m squares showed as stair-stepped blocks over the 2023 image's 0.5 m classes: WorldCover is now used only outside the 2023 image's extent), slide 1 (analysis): where the ground is free and where it is not,
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

VERSION = "v1.8"
GH_LABEL = "Page01Free"
OUT_FOLDER = "bergama_page01_free"
LOG_NAME = "bergama_page01_free_log.txt"
GH_INPUTS = {"scale": "int 0..30000 = 0"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
PHOTO_DATA = os.path.join("Data", "selinus_board_data.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "FreeGround"
TITLE = u"Where the ground is free"
SUB = u"Built, in use, green, and free to change: the study area cell by cell"
CELL = 2.0                         # m: the counting raster
N_SITES = 8                        # lettered free pieces
PHOTO_MIN = 30.0                  # v1.5: mm, the smallest photo width when the page is fitted
PHOTO_W = 120.0                    # mm: the photo column
# class key, legend group, words, fill (palette refs of the project; warm = free, greens = kept, greys = built)
CLASSES = [
    ("building", "BUILT", u"Buildings", "8E8F8A"),
    ("street", "BUILT", u"Streets and roads", "FFFFFF"),
    ("water", "BUILT", u"Stream and water", "A2B6B5"),
    ("parking", "FREE", u"Car parks", "C2703D"),
    ("used", "IN USE", u"Grounds in use: schools, mosques, cemeteries, archaeological, sports", "BDB3C9"),
    ("park", "GREEN", u"Parks and gardens", "89986A"),
    ("farm", "GREEN", u"Fields and orchards", "C3C49A"),
    ("trees", "GREEN", u"Tree cover", "70754C"),
    ("bare", "FREE", u"Bare ground", "D9A55B"),
    ("grass", "FREE", u"Grass and loose ground", "EAD8A0"),
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
    den = int(globals().get("scale") or 0)
    page = tuple(globals().get("page_mm") or G["PC_A3"])     # v1.5: A3, or the slide sheet's panel
    ph = photos_of(log)
    tm_, tw_ = K["text_mm"], lib["text_w"]

    def short(d):                                        # v1.7: the description up to its first ";", no camera words
        d = re.sub(r"^[^:;]*ultra-wide[^:;]*:\s*", u"", d).split(u";")[0].strip().rstrip(u".")
        return d[:1].upper() + d[1:] + u"."
    F = G["pc_site_map"](1000.0, [])                     # v1.8: strictly site_alan, turned flat (pages_common)
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
    RS = Raster(F.b, CELL)                               # v1.8: over site_alan
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
        sites.append(dict(a=len(comp) * a2, x=F.b[0] + (ci + 0.5) * CELL, y=F.b[1] + (cj + 0.5) * CELL,
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

    R0 = 2.6
    # ---- legend: groups, each class with its area in the study area
    def sw(c_):
        return lambda x, y: [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0), (x + 4.5, y + 2.0), (x - 4.5, y + 2.0)]],
                                c_, K["grey_line"], 0.1, "legend")]
    legend = []
    for g_, head in GROUPS:
        legend.append((None, head))
        for k_, gg, w_, c_ in CLASSES:
            if gg == g_:
                legend.append((sw(c_), u"%s: %s m2" % (w_, format(int(round(area[k_])), ",d")) if gg == "FREE"
                               else w_))                 # v1.3: areas of the free classes only (shares: Page02)
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
                u"Study area (the free areas are counted inside it)")]
    notes = [u"Each %.0f m cell counted once, in the order of the legend's groups (built first). Free = car parks, "
             u"bare ground, grass and loose ground: no building, street or recorded use on it today." % CELL]
    # ---- v1.8 layout: the legend columns the page height needs, the scale that fits, the photo grid under the map
    class _Dry(object):
        pass
    dry = _Dry()
    dry.box, dry.k, dry.den = (0.0, -5000.0, 0.0, 0.0), 1.0, 1000.0
    blank = [(None if d_ is None else (lambda x, y: []), t_) for d_, t_ in legend]
    for ncol in (1, 2, 3, 4):
        ys = [it[3] for it in G["pc_sheet"](dry, K, lib, TITLE, SUB, blank, notes, u"", cols=ncol)
              if it[0] == "text" and it[8] in ("title", "legend", "notes")]
        if -min(ys) + 48.0 <= page[1] - 24.0:
            break
    else:
        log.append(u"FLAG: the legend does not fit the page height in 4 columns")
    side = ncol * G["PC_SIDE_MM"] + (ncol - 1) * 6.0

    def cap_h(pw_, cs):                                  # the tallest caption at photo width pw_ (mm)
        return 1.0 + max(len(wrap(u"%d  %s" % (i_ + 1, c_), tm_["small"], pw_, tw_)) for i_, c_ in enumerate(cs)) * \
            tm_["small"] * 1.4 + 1.0

    def photo_fit(mw, band_):                            # (rows, cols, photo width, captions) or None
        for cs in ([p_["description"] for p_ in ph], [short(p_["description"]) for p_ in ph]):
            best = None
            for r_ in (1, 2, 3, 4):
                c_ = -(-len(ph) // r_)
                pw_ = min(PHOTO_W, (mw - (c_ - 1) * 4.0) / c_)
                while pw_ > 5.0 and pw_ * 0.75 + cap_h(pw_, cs) > band_ / r_:
                    pw_ -= 1.0
                if best is None or pw_ > best[2]:
                    best = (r_, c_, pw_, cs)
            if best and best[2] >= PHOTO_MIN:
                return best
        return best
    d_ = den if den > 0 else G["pc_site_den"](F, page, side, PHOTO_MIN * 0.75 + 20.0)
    while True:
        M = G["pc_site_map"](d_, [])
        band = page[1] - 24.0 - M.mh - 6.0
        pfit = photo_fit(M.mw, band)
        if den > 0 or pfit[2] >= PHOTO_MIN or d_ > 60000:
            break
        d_ += 500
    if pfit[2] < PHOTO_MIN:
        log.append(u"FLAG: the photos under the map are only %.0f mm wide" % pfit[2])
    caps = pfit[3]
    M.x0 = max(12.0, (page[0] - M.mw - 8.0 - side) / 2.0)
    M.y0 = page[1] - 12.0 - M.mh                         # the map along the page top
    M.box = (M.x0, M.y0, M.x0 + M.mw, M.y0 + M.mh)
    M.w, M.h = page
    if M.x0 + M.mw + 8.0 + side > page[0] - 11.9:
        log.append(u"FLAG: map and legend are %.0f mm wider than the page" % (M.x0 + M.mw + 20.0 + side - page[0]))
    log.append(u"layout: site_alan %.0f x %.0f m at 1:%s, %d legend column(s), photos %d x %d at %.0f mm (%s captions)"
               % (F.F.w, F.F.h, format(int(M.den), ",d"), ncol, pfit[0], pfit[1], pfit[2],
                  u"full" if caps[0] == ph[0]["description"] else u"short"))

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
        q = (min(max(q[0], M.box[0] + R0 + 0.4), M.box[2] - R0 - 0.4),     # v1.7: the disc inside the frame
             min(max(q[1], M.box[1] + R0 + 0.4), M.box[3] - R0 - 0.4))
        items.append(P_([circle(q[0], q[1], R0, 32)], INK, "FFFFFF", 0.3, "free_sites"))
        items.append(T_(s_["id"], q[0], q[1] - 1.1, 3.0, "FFFFFF", "free_sites", True, "C"))
        lab.block_pt(q, R0)
    for n_, p_ in enumerate(ph):
        q = M.T((p_["x"], p_["y"]))
        if not M.inside(q):
            log.append(u"photo %d lies outside site_alan: its point is not drawn" % (n_ + 1))
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

    credit = u""                                         # v1.4: no sources in the drawing (Aras 15:23 UTC)
    log.append(u"sources (log only): survey (Bergama municipality DWG); OpenStreetMap (ODbL); 2023 satellite image "
               u"classes inside its extent, ESA WorldCover 2021 (CC BY 4.0) outside it; photos: site visit 1 Oct 2026")
    items += G["pc_sheet"](M, K, lib, TITLE, SUB, legend, notes, credit, north=G["pc_north_deg"](M.north), cols=ncol,
                           span=(12.0, page[1] - 12.0))

    # ---- v1.8: the photos in a grid under the map, across then down, each with its number and caption
    photos = []
    rows_, cols_, pw = pfit[0], pfit[1], pfit[2]
    phh = pw * 0.75
    rh = band / float(rows_)
    ytop = M.box[1] - 6.0
    for n_, p_ in enumerate(ph):
        r_, c_ = n_ // cols_, n_ % cols_
        xx, yy = M.box[0] + c_ * (pw + 4.0), ytop - r_ * rh - phh
        photos.append((p_["path"], xx, yy, pw, phh))
        yy -= 1.0
        for ln in wrap(u"%d  %s" % (n_ + 1, caps[n_]), tm["small"], pw, tw):
            yy -= tm["small"] * 1.4
            items.append(T_(ln, xx, yy, tm["small"], INK, "notes"))
        if yy < ytop - (r_ + 1) * rh - 0.5:
            log.append(u"FLAG: photo %d's caption runs into the next row" % (n_ + 1))
    box_r = [(bx[0], bx[1]), (bx[2], bx[1]), (bx[2], bx[3]), (bx[0], bx[3])]
    clips = {clip: [[box_r]]}
    if ib:
        ir = [M.T(q) for q in ((ib[0], ib[1]), (ib[2], ib[1]), (ib[2], ib[3]), (ib[0], ib[3]))]   # v1.8: turned
        clips["wc"] = [[box_r], [box_r, ir]]             # v1.2
        log.append(u"WorldCover only outside the 2023 image's extent (survey x %.0f-%.0f, y %.0f-%.0f)" % (
            ib[0], ib[2], ib[1], ib[3]))
    G["pc_write"](lib, M, items, OUT_DIR, NAME, u"Where the ground is free, 1:%d" % M.den, log, photos=photos,
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
