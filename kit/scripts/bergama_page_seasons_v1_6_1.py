# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE SEASONS v1 (14 Nov 2026), Panel Review II page element: FOUR SEASONS ON ONE CUT.
One script per page (Aras 14 Nov 10:46 UTC). Output: output/bergama_page_seasons/Seasons.pdf + review/ PNGs, copy
output/presentation/<SLIDE>.pdf.

Aras 14 Nov 13:02 UTC: "we can merge p15 and 16 remove the width dimensions." (SUBMISSION_SON p15 "Four seasons on one
cut" + p16 "The S4 cut, north-east bank" with its year calendar: CONTENT reference only.)
Aras 14 Nov 13:01 UTC: "remove these markings we gonna have a new diagram for that" (the level marker stack): none here.
Aras 14 Nov 13:06 UTC: "create those four season on one cut drawing from the section creator that we have in our hand
currently. So all sections are in the same language these four seasons in one cut should show the bank water depth
throughout the year. and the thing to change is the assets colours ... the base of that section gonna be drawn from the
section script so you dont really need to redraw it. you can reuse it with different assets".
Aras 14 Nov 12:55 UTC: never import or trace old PDF pages; 12:38: one job done once, cached, chained.

So, CHAINED after Sections v1.6.9+ (its cache, nothing of the base redrawn):
  BASE     cached/bergama_sections/cuts.json + cuts/<cut>.json: the cut's page items at a cached scale; the items on
           the layers the cache names "layers_season" (water, levels, planting, people, trees, callouts) and the
           title layer are left out, the rest (sky, ground behind, houses, cut ground, walls, roads, land-use band) is
           the shared base, placed with the cache's map (x = X0 + (s - lo) K, y = Y0 + (z - zb) K).
  SEASONS  the same cut four times, winter / spring / summer / autumn, each with its own assets:
           water   the season's levels from the cache (levels "season|Q": Sections SEASON_WATER, calculated on this
                   cut), filled water joined to the bed (Sections joined_level), the high-end line dashed; the summer
                   strip held in spring, summer, autumn (Sections STRIP_HELD, design); Q100 / Q500 lines dashed
           planting the cache's grass, reeds, iris drawn by the section engine in the season's colours (engine
                   SEASON_LOOK, read live)
           trees   the asset-library cutouts (Data/cutouts) as Sections places them, TINTED per season (TINT below,
                   drawing values, ours); tinted copies cached in cached/bergama_page_seasons/cutouts/<season>/
           people  the cache's people as cutouts, never in the season's water (Aras 31 Oct 11:28)
           no level signs or values, no dimensions (engine layers "levels" texts / signs, "dimensions", "callouts")
  RAIN     v1.6: left of each cut, the season's months: rain mm (WaterBoard RAIN) and the mean water over the bed
           m (Data/bergama_water_board_data.py LEVELS row of the cut, depth_month, larger gauge figure)
  LEVELS   v1.6: strip floor to promenade on a stepped half-bed, where the water fills, planting bands A-F with days
           under water (WaterBoard PLANT_BANDS / BAND_DAYS / BAND_COL); S4 zones and plants from the engine SECTIONS
  KEY      EXISTING / PROPOSAL MARKS (proposal orange C07A2E, as the node pages and PageTransit), season asset colours
Reads Data/bergama_pages_common.py (review PNGs, presentation copy), the newest scripts/bergama_sections_v*.py (code
only: engine, writer, cutouts, joined_level), Data/bergama_sections_engine.py, Data/cutouts/, the Sections cache.
Grasshopper: a Button on any input runs it; inputs `cut` (text, an A cut of Data/section_lines.json, square to the
stream; default S4 (v1.6), N3-A when the cache has no S4; B cuts run along the bank since section_lines v2 and have no water) and `scale` (int, 0 = the
largest cached scale that fits).
"""
import os, re, glob, json, math, time, zlib, struct

VERSION = "v1.6.1"   # v1.6.1: Sh.ex no longer calls the Sections surf (it falls back to ex outside the surface: endless recursion, Rhino crashed on S4); v1.6, Aras 14 Nov 16:37-16:38 UTC ("we dont have these diagrams ... humans or trees or background assets"; "create this as a diagram that shows in lowest river bed depth and shows on it where it fills up to etc. and plug that into one of the pages"): default cut S4 (the engine's designed banks, cached by Sections v1.10, trees, people, houses, shrubs, lavender), the RAIN · WATER columns per season, numbered zone bar + ZONES key, PLANTS key, the LEVELS diagram with planting bands A-F (slide 3 design concept), the main idea under the title; the four cuts fitted to the rows box (scale not important, Aras 15:27); the year chart left out (the columns carry it); v1.5: default cut N3-A (section_lines v2, 14 Nov 16:14 UTC: B cuts run along the bank, N6-B no longer crosses the stream); v1.4   # v1.4, Aras 14 Nov 15:28 UTC "the grass is too long please be careful about the proportions": the planting drawn at the engine's own 1:75 and scaled down as a whole to the page scale (blade widths, plumes and culms were fixed page mm, oversized at 1:500); the base's soil root hairs (fixed 1-3 mm lines) left out; v1.3   # v1.3, Aras 14 Nov 15:23-15:24 UTC: "dont give sources in the drawings at all", "no sources for nothing": no source or status brackets on the page, the sources go to the log only; v1.2   # v1.2 (run 2 check): the four cuts spread over the rows box height (half the page was empty); taller year chart; the strip label inside its bars (it ran over "no figure"); no false FLAG on a cropped cut exactly the box wide; v1.1   # v1.1 (run 1 check): the cuts cropped to a window round the stream at the largest cached scale that fits (1:1000 read flat); the summer strip in the year chart hangs below the bed (it is cut 0.30 m into it)
SLIDE = 3                            # slide 3 (main + design idea); presentation/3.pdf
GH_LABEL = "PageSeasons"
OUT_FOLDER = "bergama_page_seasons"
LOG_NAME = "bergama_page_seasons_log.txt"
GH_INPUTS = {"cut": "text = S4", "scale": "int 0..3000 = 0"}
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
SEC_CACHE = os.path.join(BERGAMA_ROOT, "cached", "bergama_sections")
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "Seasons"
CUT_DEFAULT = "S4"                  # v1.6: the designed cut (Sections v1.10 caches it every run, not on its sheet)
CUT_FALLBACK = "N3-A"               # when the cache has no S4 yet (FLAG)
RAIN_X0, RAIN_W = 14.0, 30.0        # v1.6: the RAIN · WATER column left of each cut
MAIN_IDEA = u"A landscape that can be lived in all four seasons and joins river life with city life."   # Aras 14 Nov 10:55 UTC
DESIGN_IDEA = (u"The Selinos becomes a stepped, amphibious bed whose terraces flood one level at a time, so every "
               u"season lives on the levels the water leaves dry.")     # Aras chose, 14 Nov 10:59 UTC
PAGE_W, PAGE_H = 420.0, 297.0
ROWS_BOX = (48.0, 22.0, 262.0, 266.0)      # mm: x0, y0, x1, y1 of the four cuts (v1.6: the rain columns left of them)
COL_X0, COL_X1 = 276.0, 406.0              # mm: the right column (year chart, key)
ROW_GAP = 7.0                              # mm between two season cuts (their title sits in it)
SEASONS = ("winter", "spring", "summer", "autumn")
SEA_MONTHS = {"winter": u"Dec–Feb", "spring": u"Mar–May", "summer": u"Jun–Aug", "autumn": u"Sep–Nov"}
SEA_IDX = {"winter": (11, 0, 1), "spring": (2, 3, 4), "summer": (5, 6, 7), "autumn": (8, 9, 10)}
SEA_COL = {"winter": "5C7A86", "spring": "89986A", "summer": "3C4733", "autumn": "8B2D2D"}   # project palette
MONTHS = (u"J", u"F", u"M", u"A", u"M", u"J", u"J", u"A", u"S", u"O", u"N", u"D")
# the months each season's water figure stands for (Sections SEASON_WATER labels: "Jan-Feb mean", "Mar-Apr, low
# end", "Oct-Dec high end"; summer: no flow figure, the held strip)
WATER_MONTHS = {"winter": (0, 1), "spring": (2, 3), "autumn": (9, 10, 11)}
STRIP_MONTHS = (5, 6, 7)
# season tint of the tree cutouts (drawing values, ours): duotone from the pixel's lightness (dark, light) or a mix
# toward one colour; summer = the asset as it is
TINT = {"winter": ("duo", "6E675C", "DAD5CB"), "spring": ("mix", "D7E8A0", 0.30), "summer": None,
        "autumn": ("duo", "7C4F2B", "EAD08E")}
INK, GREY, ORANGE = "2C2219", "6E675E", "C07A2E"
PLANT_DEN = 75.0                     # v1.4: the engine's planting pieces are sized for 1:75 (bergama_sections_engine SCALE)
BACK_LAYERS = ("sky", "ground behind", "houses behind", "context buildings")
DROP_LAYERS = ("title", "callouts", "dimensions")


# ================================================================ loading (code of the Sections script, its cache)
def _newest(pat):
    found = glob.glob(os.path.join(BERGAMA_ROOT, "scripts", pat))
    if not found:
        raise RuntimeError(u"no scripts/%s in %s: run Bergama.bat once (the kit copies it)" % (pat, BERGAMA_ROOT))
    return max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])


def _exec(path, name):
    with open(path, encoding="utf-8") as f:
        code = f.read()
    ns = {"__name__": name}                   # no ghenv here: the script's Grasshopper block does not run
    exec(compile(code, path, "exec"), ns)
    return ns


def load_cut(name, log):
    pj = os.path.join(SEC_CACHE, "cuts.json")
    if not os.path.isfile(pj):
        raise RuntimeError(u"%s missing: press Sections (v1.6.9 or newer) first, then this" % pj)
    with open(pj, encoding="utf-8") as f:
        idx = json.load(f)
    cuts = idx.get("cuts", {})
    if name not in cuts:
        raise RuntimeError(u"cut %s is not in %s (it has: %s)" % (name, pj, u", ".join(sorted(cuts))))
    J = cuts[name]
    for k in ("surface", "layers_season", "planting", "people", "levels"):
        if k not in J:
            raise RuntimeError(u"%s has no '%s' for %s: press Sections v1.6.9 or newer again" % (pj, k, name))
    with open(os.path.join(SEC_CACHE, J["items_file"]), encoding="utf-8") as f:
        per = json.load(f)
    log.append(u"Sections cache: %s (Sections %s, run %s), cut %s, scales %s" % (
        pj, idx.get("version"), idx.get("run"), name, u"/".join(sorted(per, key=int))))
    return J, per, idx


class Sh(object):
    """the cut on the page from the cache alone (what the engine pieces and joined_level ask of a section)"""

    def __init__(self, X, E, name, J, M):
        self.E, self.K = E, float(M["K"])
        self.X0, self.Y0, self.lo, self.zb = float(M["X0"]), float(M["Y0"]), float(M["lo"]), float(M["zb"])
        self.hi = float(J["window"][1])
        self.V = [tuple(p) for p in J["surface"]]
        self._xs = None
        self.walled = tuple(J["walled"]) if J.get("walled") else None
        self.channel = tuple(J.get("channel") or (0.0, 0.0))
        self.has_strip = bool(J.get("strip"))
        self.strip = tuple(J["strip"]) if J.get("strip") else (-1e9, -1e9, 0.0)
        pl = J["planting"]
        self.d = dict(key=u"seasons_%s" % name, s_from=self.lo, s_to=self.hi, grass=pl.get("grass", []),
                      reeds=pl.get("reeds", []), iris=pl.get("iris", []), trees=pl.get("trees", []))

        class _C(object):
            pass
        self.C = _C()
        self.C.z_th = float(J["z_th"])
        if self.has_strip:                    # Sections: the strip is centred on the bed low point
            self.C.s_th = (self.strip[0] + self.strip[1]) / 2.0
        else:
            self.C.s_th = min(self.V, key=lambda p: p[1])[0]
        self._surf = X["Sec"].surf

    def X(self, s):
        return self.X0 + (s - self.lo) * self.K

    def Y(self, z):
        return self.Y0 + (z - self.zb) * self.K

    def P(self, s, z):
        return (self.X(s), self.Y(z))

    def surf(self, s):
        return self._surf(self, s)

    def ex(self, s):
        """v1.6.1: the cached surface's height at s, s held inside its ends. Sections' surf falls back to ex outside the
        surface, so ex must never call surf (v1.6 did: endless recursion, Rhino stack overflow on S4, laptop 22:47)"""
        V = self.V
        lo_ = min(V, key=lambda p: p[0])
        hi_ = max(V, key=lambda p: p[0])
        if s <= lo_[0]:
            return lo_[1]
        if s >= hi_[0]:
            return hi_[1]
        best = None
        for a, b in zip(V, V[1:]):
            x0, x1 = sorted((a[0], b[0]))
            if x0 <= s <= x1:
                z = min(a[1], b[1]) if x1 - x0 < 1e-9 else a[1] + (b[1] - a[1]) * (s - a[0]) / (b[0] - a[0])
                best = z if best is None else min(best, z)
        return best if best is not None else min(lo_[1], hi_[1])


# ================================================================ tinted tree cutouts
def _png_write(path, w, h, rgb, alpha):
    rgba = bytearray(w * h * 4)
    rgba[0::4], rgba[1::4], rgba[2::4] = rgb[0::3], rgb[1::3], rgb[2::3]
    rgba[3::4] = alpha if alpha is not None else b"\xff" * (w * h)
    st = w * 4
    raw = b"".join(b"\x00" + bytes(rgba[y * st:(y + 1) * st]) for y in range(h))

    def chunk(t, c):
        return struct.pack(">I", len(c)) + t + c + struct.pack(">I", zlib.crc32(t + c) & 0xffffffff)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) +
                chunk(b"IDAT", zlib.compress(raw, 6)) + chunk(b"IEND", b""))


def _hx(c):
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def tinted(X, src, sea, log, cnt):
    """the season copy of one cutout PNG (cached; made again when the source is newer)"""
    tn = TINT.get(sea)
    if not tn:
        return src
    dst = os.path.join(CACHE_DIR, "cutouts", sea, os.path.basename(src))
    if os.path.isfile(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return dst
    r_ = X["_png"](src)
    if not r_:
        log.append(u"FLAG %s: not an 8-bit RGB(A) PNG, drawn untinted in %s" % (src, sea))
        return src
    w, h, rgb, al = r_
    R, G, B = rgb[0::3], rgb[1::3], rgb[2::3]
    if tn[0] == "duo":
        d, l_ = _hx(tn[1]), _hx(tn[2])
        lum = bytes((r * 77 + g * 150 + b * 29) >> 8 for r, g, b in zip(R, G, B))
        ch = [lum.translate(bytes(int(round(d[i] + (l_[i] - d[i]) * v / 255.0)) for v in range(256)))
              for i in range(3)]
    else:
        c, t = _hx(tn[1]), tn[2]
        ch = [src_.translate(bytes(int(round(v + (c[i] - v) * t)) for v in range(256)))
              for i, src_ in enumerate((R, G, B))]
    out = bytearray(w * h * 3)
    out[0::3], out[1::3], out[2::3] = ch
    _png_write(dst, w, h, bytes(out), al)
    cnt[sea] = cnt.get(sea, 0) + 1
    return dst


# ================================================================ one season cut
def season_cut(X, E, name, J, cut_its, M, sea, log, cnt):
    """the season's items at the cache's origin (mm): shared base + the season's assets"""
    K = float(M["K"])
    E["K"] = K
    X["_ENGINE_K"][0] = K
    E["SEA"].clear()
    E["SEA"].update(E["SEASON_LOOK"][sea])
    S = Sh(X, E, name, J, M)
    il = X["_item_layer"]
    skip = set(J["layers_season"]) | set(DROP_LAYERS)
    base = [it for it in cut_its if il(it) not in skip and not (il(it) == "soft ground" and it[0] == "line")]
    back = [it for it in base if il(it) in BACK_LAYERS]
    front = [it for it in base if il(it) not in BACK_LAYERS]
    pg = E["Page"](u"seasons_%s" % sea, u"")
    pg.items += [tuple(it) for it in back]
    # trees (behind the cut ground, as Sections draws them), the asset cutouts tinted for the season
    n_tree = 0
    for t in S.d["trees"]:
        s, r_, h = t[0], t[1], t[2]
        g = S.surf(s)
        Xp, Yp = S.P(s, g)
        n0 = len(pg.items)
        if X["cutout"](pg, "plane", Xp, Yp, h * K, int(s * 7) % 6, (int(s) % 2) == 1, "trees"):
            it = list(pg.items[n0])
            it[5] = tinted(X, it[5], sea, log, cnt)
            pg.items[n0] = tuple(it)
        else:
            E["veg_tree"](pg, Xp, Yp, h * K, 2 * r_ * K, (S.d["key"], round(s, 2)))
        n_tree += 1
    q100 = J["levels"].get("q100", [None])[0]
    q500 = J["levels"].get("q500", [None])[0]
    jl = X["joined_level"]
    if q500 is not None:
        jl(E, pg, S, q500, u"", [2.0, 1.0])
    if q100 is not None:
        jl(E, pg, S, q100, u"", [0.8, 0.8])
    sw = season_water(X, J, sea)
    for z, fill_, dash in sw:
        if not fill_:
            jl(E, pg, S, z, u"", dash, colour=E["WATER_LINE"])
    pg.items += [tuple(it) for it in front]
    # planting from the cache in the season's look (engine SEASON_LOOK), v1.4: drawn at the engine's own scale
    # PLANT_DEN on a page of its own, then every point (and line width, circle radius) scaled by K / K75 onto the cut
    K75 = 1000.0 / PLANT_DEN
    S75 = Sh(X, E, name, J, dict(M, K=K75, X0=0.0, Y0=0.0))
    pp = E["Page"](u"plants_%s" % sea, u"")
    E["K"] = K75
    try:
        for a, b in S.d["grass"]:
            a, b = max(a, S.lo + 0.3), min(b, S.hi - 0.3)
            if b > a:
                E["tufts"](pp, S75, a, b)
        for a, b, h in S.d["reeds"]:
            E["reeds"](pp, S75, a, b, h)
        for a, b in S.d["iris"]:
            E["iris"](pp, S75, a, b)
        if name == "S4":                             # v1.6: the design's shrubs and lavender (engine SECTIONS, as Sections)
            for dsec in E["SECTIONS"]:
                for a, b in dsec.get("lavender", []):
                    E["lavender"](pp, S75, a, b)
                for s_, h_, w_ in dsec.get("shrubs", []):
                    E["shrub"](pp, S75, s_, h_, w_)
    finally:
        E["K"] = K
    f = K / K75
    pg.items += [scaled(it, f, S.X0, S.Y0) for it in pp.items]
    filled = [w for w in sw if w[1]]
    for z, fill_, dash in filled:
        jl(E, pg, S, z, u"", None, colour=E["FLOOD"], fill=True)
    held = X["STRIP_HELD"].get(sea) and S.has_strip
    if held:
        jl(E, pg, S, S.C.z_th, u"", None, colour=E["FLOOD"], fill=True, line=not filled)
    wl = max([S.C.z_th if held else -99.0] + [w[0] for w in filled])
    n_p = 0
    keys = X["PEOPLE_KEYS"]
    for s, kind, flip in J["people"]:
        g = S.surf(s)
        if g < wl + 0.02 and kind != 8:
            continue                                        # never a person in the water (Aras 31 Oct 11:28)
        if not X["cutout"](pg, keys[kind % len(keys)], *S.P(s, g), h_mm=None, n=kind, flip=flip, layer="people"):
            E["figure"](pg, S, s, kind, flip)
        n_p += 1
    # no level signs or values (Aras 13:01 UTC): of the "levels" layer only the level lines stay
    its = []
    for it in pg.items:
        ly = il(it)
        if ly in DROP_LAYERS:
            continue
        if ly == "levels" and not (it[0] == "line" and abs(it[1][-1][0] - it[1][0][0]) > 2.0):
            continue
        its.append(it)
    log.append(u"%s: %d trees (cutouts, %s), %d people, %d water level(s) filled, strip %s, grass %d, reeds %d, "
               u"iris %d" % (sea, n_tree, u"tinted" if TINT.get(sea) else u"as drawn", n_p, len(filled),
                            u"held" if held else u"not held", len(S.d["grass"]), len(S.d["reeds"]), len(S.d["iris"])))
    return its, S


def clip_x(X, items, xa, xb):
    """v1.1: the items cut to the vertical strip xa..xb (mm): polygons (Sutherland-Hodgman), lines in runs; texts,
    circles and images only when wholly inside"""
    def cut_ring(R, x, keep_ge):
        out = []
        n = len(R)
        for i in range(n):
            p, q = R[i], R[(i + 1) % n]
            pin, qin = (p[0] >= x) == keep_ge or p[0] == x, (q[0] >= x) == keep_ge or q[0] == x
            if pin:
                out.append((p[0], p[1]))
            if pin != qin and q[0] != p[0]:
                t = (x - p[0]) / (q[0] - p[0])
                out.append((x, p[1] + (q[1] - p[1]) * t))
        return out
    res = []
    for it in items:
        t = it[0]
        if t == "poly":
            rings = []
            for R in it[1]:
                r2 = cut_ring(cut_ring([tuple(p) for p in R], xa, True), xb, False)
                if len(r2) >= 3:
                    rings.append(r2)
            if rings:
                res.append((t, rings) + tuple(it[2:]))
        elif t == "line":
            pts = [tuple(p) for p in it[1]]
            run = []
            for p, q in zip(pts[:-1], pts[1:]):
                a, b = (p, q) if p[0] <= q[0] else (q, p)
                if b[0] < xa or a[0] > xb:
                    if len(run) >= 2:
                        res.append((t, run) + tuple(it[2:]))
                    run = []
                    continue
                def at(x):
                    return (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])) if b[0] != a[0] else (x, a[1])
                p2 = p if xa <= p[0] <= xb else at(xa if p[0] < xa else xb)
                q2 = q if xa <= q[0] <= xb else at(xa if q[0] < xa else xb)
                if run and run[-1] == p2:
                    run.append(q2)
                else:
                    if len(run) >= 2:
                        res.append((t, run) + tuple(it[2:]))
                    run = [p2, q2]
                if not (xa <= q[0] <= xb):
                    res.append((t, run) + tuple(it[2:]))
                    run = []
            if len(run) >= 2:
                res.append((t, run) + tuple(it[2:]))
        else:
            b = X["items_bbox"]([it])
            if b[0] >= xa - 1e-6 and b[2] <= xb + 1e-6:
                res.append(it)
    return res


def scaled(it, f, ox, oy):
    """v1.4: one engine item from the 1:PLANT_DEN planting page onto the cut: p -> (ox + f x, oy + f y)"""
    t = it[0]
    P = lambda p: (ox + f * p[0], oy + f * p[1])
    if t == "poly":
        return (t, [[P(p) for p in r] for r in it[1]], it[2], it[3], (it[4] or 0.0) * f) + tuple(it[5:])
    if t == "line":
        return (t, [P(p) for p in it[1]], it[2], (it[3] or 0.0) * f) + tuple(it[4:])
    if t == "circle":
        x, y = P((it[1], it[2]))
        return (t, x, y, it[3] * f, it[4], it[5], (it[6] or 0.0) * f) + tuple(it[7:])
    if t == "text":
        x, y = P((it[2], it[3]))
        return (t, it[1], x, y, it[4] * f) + tuple(it[5:])
    if t == "image":
        x, y = P((it[1], it[2]))
        return (t, x, y, it[3] * f, it[4] * f) + tuple(it[5:])
    return it


def season_water(X, J, sea):
    """[(level, filled, dash)] of the season on this cut: Sections SEASON_WATER read against the cached levels"""
    out = []
    lv = {}
    for k, v in J["levels"].items():
        if u"|" in k:
            a, q = k.split(u"|")
            lv[(a, float(q))] = v[0]
    for Q, fill, _lab in X["SEASON_WATER"][sea]:
        z = next((v for (a, q), v in lv.items() if a == sea and abs(q - Q) < 1e-6), None)
        if z is not None:
            out.append((z, fill, None if fill else [1.6, 0.6, 0.3, 0.6]))
    return out


# ================================================================ page helpers
def T_(s, x, y, size, col=INK, bold=False, align="L", layer="text"):
    return ("text", s, x, y, size, col, bold, align, layer, None, None)


def L_(pts, col, lw, layer, dash=None):
    return ("line", [tuple(p) for p in pts], col, lw, list(dash) if dash else None, layer, 1)


def R_(x0, y0, x1, y1, fill, stroke, lw, layer, alpha=None):
    return ("poly", [[(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], fill, stroke, lw, None, layer, 1, None, alpha)


def year_chart(X, J, x0, ytop, x1, log):
    """water over the bed through the year: one month axis, the cut's calculated depths, the strip (design)"""
    it = []
    zt = float(J["z_th"])
    lv = {}
    for k, v in J["levels"].items():
        if u"|" in k:
            a, q = k.split(u"|")
            lv[(a, float(q))] = v[0] - zt
    SW = X["SEASON_WATER"]
    fill_d = {}
    line_d = {}
    for sea in SEASONS:
        for Q, fill, lab in SW[sea]:
            d = next((v for (a, q), v in lv.items() if a == sea and abs(q - Q) < 1e-6), None)
            if d is None:
                continue
            (fill_d if fill else line_d)[sea] = (d, lab.split(u" %")[0])
    strip_d = X["STRIP_D"]
    dmax = max([v[0] for v in fill_d.values()] + [v[0] for v in line_d.values()] + [strip_d, 0.1])
    it.append(T_(u"WATER OVER THE BED, THROUGH THE YEAR", x0, ytop, 3.0, INK, True, "L", "year"))
    it.append(T_(u"m above the lowest bed point of the cut", x0, ytop - 4.2, 2.0,
                 GREY, False, "L", "year"))
    ch_top, ch_bot = ytop - 9.0, ytop - 9.0 - 50.0             # v1.1: ch_bot = the bed low point; v1.2 taller
    lab_w = 8.0
    mw = (x1 - x0 - lab_w) / 12.0
    xa = x0 + lab_w
    k = (ch_top - ch_bot - 4.0) / dmax
    k = min(k, 14.0 / max(strip_d, 0.01))                      # the strip below the bed: at most 14 mm

    def X_(m):
        return xa + m * mw
    for i in range(0, int(dmax * 10) + 1):                       # 0.1 m grid
        y = ch_bot + i * 0.1 * k
        if i % 2 == 0 or dmax < 0.6:
            it.append(L_([(xa, y), (x1, y)], "E4E0D8", 0.12, "year"))
            it.append(T_(u"%.1f" % (i * 0.1), xa - 1.0, y - 0.6, 1.8, GREY, False, "R", "year"))
    n_bar = 0
    for sea, ms in WATER_MONTHS.items():
        if sea not in fill_d:
            continue
        d, lab = fill_d[sea]
        for m in ms:
            it.append(R_(X_(m) + 0.6, ch_bot, X_(m + 1) - 0.6, ch_bot + d * k, "7DB3D3", None, 0.0, "year"))
        it.append(T_(u"%.2f" % d, (X_(ms[0]) + X_(ms[-1] + 1)) / 2.0, ch_bot + d * k + 1.0, 1.9, INK, True, "C", "year"))
        n_bar += 1
    for sea, (d, lab) in line_d.items():                          # the season's high end (dashed on the cut)
        ms = WATER_MONTHS.get(sea, ())
        if not ms:
            continue
        y = ch_bot + d * k
        it.append(L_([(X_(ms[0]) + 0.6, y), (X_(ms[-1] + 1) - 0.6, y)], "3F86B8", 0.3, "year", (1.6, 0.6, 0.3, 0.6)))
        it.append(T_(u"%.2f %s" % (d, lab), X_(ms[0]) + 0.6, y + 0.8, 1.7, "3F86B8", False, "L", "year"))
    for m in STRIP_MONTHS:                                         # the summer strip: the design's held water
        it.append(R_(X_(m) + 0.6, ch_bot - strip_d * k, X_(m + 1) - 0.6, ch_bot, "F3E3CF", ORANGE, 0.3, "year"))
    xm = (X_(STRIP_MONTHS[0]) + X_(STRIP_MONTHS[-1] + 1)) / 2.0    # v1.2: inside the strip bars, under the bed line
    it.append(T_(u"strip %.2f m" % strip_d, xm, ch_bot - strip_d * k / 2.0 - 0.2, 1.7, ORANGE, True, "C",
                 "year"))
    it.append(T_(u"cut into the bed, held water", xm, ch_bot - strip_d * k / 2.0 - 2.6, 1.5, ORANGE, False, "C",
                 "year"))
    for m in range(12):
        if not any(m in ms for ms in WATER_MONTHS.values()) and m not in STRIP_MONTHS:
            it.append(T_(u"no figure", X_(m + 0.5), ch_bot + 1.2, 1.5, GREY, False, "C", "year"))
    it.append(L_([(xa, ch_bot), (x1, ch_bot)], INK, 0.3, "year"))
    yb = ch_bot - strip_d * k - 4.0                                # months and the four seasons under them
    for m in range(12):
        it.append(T_(MONTHS[m], X_(m + 0.5), yb, 2.0, INK, False, "C", "year"))
    for sea in SEASONS:
        for m in SEA_IDX[sea]:
            it.append(R_(X_(m) + 0.15, yb - 4.0, X_(m + 1) - 0.15, yb - 2.2, SEA_COL[sea], None, 0.0, "year"))
        ms = sorted(SEA_IDX[sea])
        mid = (X_(ms[0]) + X_(ms[-1] + 1)) / 2.0 if sea != "winter" else (X_(0) + X_(2)) / 2.0
        it.append(T_(sea, mid, yb - 7.0, 1.9, SEA_COL[sea], True, "C", "year"))
    log.append(u"year chart: %d water figure(s) filled, %d high end(s), strip %.2f m Jun-Aug (design), deepest "
               u"%.2f m" % (n_bar, len(line_d), strip_d, dmax))
    return it, yb - 10.0


def key_rows(E, X, x0, ytop, w, sea_look):
    """EXISTING / PROPOSAL MARKS (orange, as the node pages) / the season assets"""
    it = []
    y = [ytop]

    def hdr(s, col=INK):
        it.append(T_(s, x0, y[0], 2.4, col, True, "L", "legend"))
        y[0] -= 3.6

    def row(kind, col, words, col2=None):
        yy = y[0]
        if kind == "box":
            it.append(R_(x0, yy - 0.4, x0 + 5.0, yy + 2.0, col, col2 or "9A948C", 0.12, "legend"))
        elif kind == "line":
            it.append(L_([(x0, yy + 0.8), (x0 + 5.0, yy + 0.8)], col, 0.35, "legend", col2))
        it.append(T_(words, x0 + 7.0, yy, 2.0, INK, False, "L", "legend"))
        y[0] -= 3.3
    hdr(u"EXISTING")
    row("box", X["GROUND_FILL"], u"cut ground")
    row("box", X["BACK_FILL"], u"ground behind the cut")
    row("box", X["H_WALL"], u"houses behind the cut, toned with distance")
    row("box", X["BLD_CUT_FILL"], u"buildings the cut passes through")
    row("box", X["ROAD_FILL"], u"road surface")
    row("box", E["WATER"], u"water of the season over the bed", "7DB3D3")
    row("line", E["WATER_LINE"], u"the season's high end", (1.6, 0.6, 0.3, 0.6))
    row("line", E["FLOOD"], u"Q100 short dash · Q500 long dash", (2.0, 1.0))
    y[0] -= 1.0
    hdr(u"PROPOSAL MARKS", ORANGE)
    row("box", "F3E3CF", u"summer strip at the bed low point, held water", ORANGE)
    row("box", "B9CC83", u"planting: reeds and iris on the wet bed, meadow above", ORANGE)
    y[0] -= 1.0
    hdr(u"SEASON ASSETS · same cut, own colours")
    for sea in SEASONS:
        L = sea_look[sea]
        xx = x0
        for c in (L["grass_tones"][1], L["reed_tones"][0], L["iris_tones"][0]):
            it.append(R_(xx, y[0] - 0.4, xx + 3.0, y[0] + 2.0, c, None, 0.0, "legend"))
            xx += 3.4
        tn = TINT.get(sea)
        tc = (tn[1] if tn[0] == "mix" else tn[2]) if tn else None
        if tc:
            it.append(R_(xx, y[0] - 0.4, xx + 3.0, y[0] + 2.0, tc, None, 0.0, "legend"))
        it.append(T_(u"%s · grass, reeds, iris%s" % (sea, u", trees tinted" if tn else u", trees as the asset"),
                     x0 + 15.0, y[0], 2.0, SEA_COL[sea], True, "L", "legend"))
        y[0] -= 3.3
    return it, y[0]


# ================================================================ v1.6: live data, rain / water columns, levels diagram, zones
def _lit(src, name):
    """the Python literal assigned to `name` at the start of a line of src (only that literal is evaluated)"""
    import ast
    m = re.search(r"^%s = " % name, src, re.M)
    if not m:
        raise RuntimeError(u"%s not found" % name)
    lines = src[m.end():].split(u"\n")
    for n in range(1, 60):
        try:
            return ast.literal_eval(u"\n".join(lines[:n]))
        except (SyntaxError, ValueError):
            continue
    raise RuntimeError(u"%s is not a plain literal" % name)


def wb_data(name, log):
    """the cut's levels from Data/bergama_water_board_data.py (its LEVELS literal only; the whole file needs the board)
    and RAIN, PLANT_BANDS, BAND_DAYS, BAND_COL from the newest WaterBoard script (their literals only)"""
    p = os.path.join(BERGAMA_ROOT, "Data", "bergama_water_board_data.py")
    with open(p, encoding="utf-8") as f:
        src = f.read()
    a = src.index(u"LEVELS = [")
    ns = {}
    exec(src[a:src.index(u"\nBRIDGES = {", a)], ns)
    rows = dict((r.get("id"), r) for r in ns["LEVELS"])
    r = rows.get(name) or rows["S4"]
    if r["id"] != name:
        log.append(u"levels: cut %s has no row in %s: the levels diagram shows S4, the month columns rain only" % (
            name, p))

    def v(k):
        return r[k]["value"] if isinstance(r.get(k), dict) else None
    dm = v("depth_month") or {}
    terr = [t for t in r.get("terraces", []) if t.get("side") == "NE"]
    Lv = dict(id=r["id"], bed=v("bed"), avg=v("avg_flow"), q100=v("q100"), q500=v("q500"),
              bank=(r.get("NE") or {}).get("top", {}).get("value"),
              terrace=terr[0]["level"]["value"] if terr else None,
              depth=[max(t) for t in zip(*dm.values())] if dm and r["id"] == name else None,
              gauges=sorted(dm))
    wp = _newest("bergama_water_board_v*.py")
    with open(wp, encoding="utf-8") as f:
        ws = f.read()
    W = dict((k, _lit(ws, k)) for k in ("RAIN", "PLANT_BANDS", "BAND_DAYS", "BAND_COL"))
    log.append(u"levels and monthly depths: %s, row %s (monthly depth = the larger of gauges %s); rain, planting "
               u"bands, days under water, band colours: %s (RAIN, PLANT_BANDS, BAND_DAYS, BAND_COL)" % (
                   p, r["id"], u" / ".join(Lv["gauges"]), wp))
    return Lv, W


MON3 = (u"Jan", u"Feb", u"Mar", u"Apr", u"May", u"Jun", u"Jul", u"Aug", u"Sep", u"Oct", u"Nov", u"Dec")
RAIN_COL = "9AA6AE"


def rain_col(E, x0, ytop, h, sea, rain, depth):
    """v1.6 (Aras 16:37 UTC, the RAIN · WATER columns he liked): the season's three months, rain in mm (bars up, the
    year's wettest month = full height) and the mean water over the bed in m (bars down, blue)"""
    it = []
    it.append(T_(u"RAIN mm" + (u" · WATER m" if depth else u""), x0, ytop - 2.0, 1.7, GREY, True, "L", "rain"))
    room = max(8.0, h - 13.0)
    rh_ = room * (0.62 if depth else 1.0)
    dh_ = room - rh_
    yb = ytop - 6.0 - rh_
    cw = RAIN_W / 3.0
    rmax, dmax = max(rain), (max(depth) if depth else 1.0)
    it.append(L_([(x0, yb), (x0 + RAIN_W - 1.0, yb)], INK, 0.15, "rain"))
    for j, m in enumerate(SEA_IDX[sea]):
        xc = x0 + cw * (j + 0.5) - 0.5
        hr = rain[m] / rmax * rh_
        it.append(R_(xc - 2.2, yb, xc + 2.2, yb + hr, RAIN_COL, None, 0.0, "rain"))
        it.append(T_(u"%d" % int(round(rain[m])), xc, yb + hr + 0.7, 1.7, INK, False, "C", "rain"))
        it.append(T_(MON3[m], xc, yb - 2.5, 1.7, INK, True, "C", "rain"))
        if depth:
            hd = depth[m] / dmax * dh_
            y1 = yb - 3.4
            it.append(R_(xc - 2.2, y1 - hd, xc + 2.2, y1, E["FLOOD"], None, 0.0, "rain"))
            it.append(T_(u"%.2f" % depth[m], xc, y1 - hd - 2.3, 1.7, E["FLOOD"], False, "C", "rain"))
    return it


def levels_diagram(X, E, Lv, W, x0, ytop, x1):
    """v1.6 (Aras 16:38 UTC "create this as a diagram that shows in lowest river bed depth and shows on it where it
    fills up to"): the cut's levels from the strip floor to the promenade on a stepped half-bed (heights true, widths a
    diagram), the water it holds, and the planting bands A-F with their days under water a year"""
    it = []
    bed = Lv["bed"]
    floor = bed - X["STRIP_D"]
    prom = E["DRY"]
    dmax = max(Lv["depth"]) if Lv["depth"] else None
    it.append(T_(u"LEVELS · WHERE THE WATER FILLS", x0, ytop, 2.6, INK, True, "L", "levels"))
    it.append(T_(u"cut %s, from the lowest bed to the promenade; heights true, widths a diagram" % Lv["id"],
                 x0, ytop - 3.4, 1.9, GREY, False, "L", "levels"))
    kz = 19.0
    yt = ytop - 9.0

    def Y(z):
        return yt - (prom - z) * kz
    terr = Lv["terrace"] if Lv["terrace"] is not None else bed + 0.5
    # the stepped half-bed: strip, bed, flood terrace, steps up to the promenade (bed centre on the left)
    xs = [x0, x0 + 6.0, x0 + 24.0, x0 + 30.0, x0 + 42.0, x0 + 60.0, x0 + 70.0]
    prof = [(xs[0], Y(floor)), (xs[1], Y(floor)), (xs[1], Y(bed)), (xs[2], Y(bed)), (xs[3], Y(terr)), (xs[4], Y(terr))]
    n = 5
    for i in range(n):
        xa = xs[4] + (xs[5] - xs[4]) * i / n
        xb_ = xs[4] + (xs[5] - xs[4]) * (i + 1) / n
        za = terr + (prom - terr) * (i + 1) / n
        prof += [(xa, Y(za)), (xb_, Y(za))]
    prof += [(xs[6], Y(prom))]
    ybot = Y(floor) - 2.5
    it.append(("poly", [prof + [(xs[6], ybot), (xs[0], ybot)]], X["GROUND_FILL"], None, 0.0, None, "levels", 1,
               None, None))
    # water: the strip full to the bed, the mean yearly flow over the bed, the months' range dashed
    it.append(R_(xs[0], Y(floor), xs[1], Y(bed), E["WATER"], None, 0.0, "levels"))
    if Lv["avg"] is not None:
        it.append(R_(xs[0], Y(bed), xs[2] + (xs[3] - xs[2]) * (Lv["avg"] - bed) / max(terr - bed, 0.01), Y(Lv["avg"]),
                     E["WATER"], None, 0.0, "levels"))
    it.append(L_(prof, INK, 0.3, "levels"))
    for z, dash in ((Lv["q100"], (0.8, 0.8)), (Lv["q500"], (2.0, 1.0))):
        if z is not None:
            it.append(L_([(xs[0], Y(z)), (xs[6], Y(z))], E["FLOOD"], 0.25, "levels", dash))
    if Lv["bank"] is not None:
        it.append(L_([(xs[2], Y(Lv["bank"])), (xs[6], Y(Lv["bank"]))], GREY, 0.2, "levels", (0.4, 0.6)))
    # the values on the right, spread 2.6 mm apart
    lab = [(prom, u"promenade"), (Lv["q500"], u"Q500 flood"), (Lv["q100"], u"Q100 flood"), (Lv["bank"], u"bank today"),
           (terr if Lv["terrace"] is not None else None, u"flood terrace"),
           (bed + dmax if dmax else None, u"wettest month's mean"), (Lv["avg"], u"average flow"),
           (bed, u"lowest bed · strip full"), (floor, u"strip floor")]
    lab = sorted([t for t in lab if t[0] is not None], key=lambda t: -t[0])
    yl = []
    for z, s in lab:
        y = Y(z) - 0.7
        if yl and y > yl[-1] - 2.6:
            y = yl[-1] - 2.6
        yl.append(y)
    xl = xs[6] + 3.0
    for (z, s), y in zip(lab, yl):
        it.append(L_([(xs[6] + 0.5, Y(z)), (xl - 0.6, y + 0.7)], GREY, 0.12, "levels"))
        it.append(T_(u"+%.2f" % z, xl, y, 1.9, INK, True, "L", "levels"))
        it.append(T_(s, xl + 9.5, y, 1.9, INK, False, "L", "levels"))
    # planting bands A-F as a bar (WaterBoard band rule: A strip; B up to the wettest month; C below the flood terrace;
    # D up to Q100; E up to Q500; F above)
    bx0, bx1 = x1 - 8.0, x1 - 3.0
    tops = [("A", floor, bed), ("B", bed, bed + (dmax or 0.0)), ("C", bed + (dmax or 0.0), terr),
            ("D", terr, Lv["q100"]), ("E", Lv["q100"], Lv["q500"]), ("F", Lv["q500"], prom)]
    for k, za, zb_ in tops:
        if za is None or zb_ is None or zb_ <= za:
            continue
        it.append(R_(bx0, Y(za), bx1, Y(zb_), W["BAND_COL"].get(k, "DDDDDD"), "FFFFFF", 0.1, "levels"))
        it.append(T_(k, (bx0 + bx1) / 2.0, (Y(za) + Y(zb_)) / 2.0 - 0.7, 1.9, INK, True, "C", "levels"))
    it.append(T_(u"bands", (bx0 + bx1) / 2.0, yt + 1.5, 1.7, GREY, False, "C", "levels"))
    # the list under it
    y = ybot - 5.0
    it.append(T_(u"PLANTING BANDS · days under water a year", x0, y, 2.2, INK, True, "L", "levels"))
    y -= 3.4
    names = dict((b[0], b[1]) for b in W["PLANT_BANDS"])
    days = W["BAND_DAYS"]
    for k in ("F", "E", "D", "C", "B", "A"):
        if k == "A":
            d = u"under water all year"
            nm = u"Summer strip"
        else:
            a_, b_ = days.get(k, (None, None))
            d = (u"under %g days" % b_) if not a_ else (u"%g–%g days" % (a_, b_))
            nm = names.get(k, k)
        it.append(R_(x0, y - 0.4, x0 + 4.0, y + 1.9, W["BAND_COL"].get(k, "DDDDDD"), "9A948C", 0.1, "levels"))
        it.append(T_(k, x0 + 2.0, y, 1.8, INK, True, "C", "levels"))
        it.append(T_(u"%s · %s" % (nm, d), x0 + 6.0, y, 1.9, INK, False, "L", "levels"))
        y -= 2.9
    return it, y


ZONE_SKIP = (u"Handrail", u"Column", u"Balcony", u"Shading")


def s4_zones(E):
    """v1.6 (the old cut's numbered zones): the S4 design's parts, south-west to north-east, from the section engine's
    own SECTIONS (surfaces, regrade + band_more), each named by the engine's callout inside it, else its surface"""
    parts = []
    for d in E["SECTIONS"]:
        cos = [c for c in d.get("callouts", []) if u"(" not in c[2] and not c[2].startswith(ZONE_SKIP)]
        for t in d["surfaces"]:
            a, b, lab = (t[1], t[2], t[7]) if t[0] == "steps" else (t[0], t[1], t[4])
            a, b = min(a, b), max(a, b)
            nm = next((c[2] for c in sorted(cos) if a <= c[0] <= b), lab)
            parts.append((a, b, nm))
        ra, rb = sorted(d["regrade"])
        for a, b, m, lab in d["band_more"]:
            a, b = min(a, b), max(a, b)
            if m == "gravel":
                a, b = min(a, ra), max(b, rb)
            parts.append((a, b, lab))
    out = []
    for p in sorted(parts):
        if not any(abs(p[0] - q[0]) < 1e-6 and abs(p[1] - q[1]) < 1e-6 for q in out):
            out.append(p)
    return out


def plant_names(E, name):
    """the species named on the cut: S4 from the engine's callouts "Name (Turkish)", other cuts the Sections words"""
    if name == "S4":
        seen = []
        for d in E["SECTIONS"]:
            for c in d.get("callouts", []):
                if u"(" in c[2] and not c[2].startswith(ZONE_SKIP) and c[2] not in seen:
                    seen.append(c[2])
        return [s.replace(u" (", u" · ").rstrip(u")") for s in seen]
    return [u"Common reed · Kamış", u"Yellow flag iris · Sarı süsen", u"Meadow, native grasses"]


# ================================================================ main
def main():
    t0 = time.time()
    log = []
    name = globals().get("cut")
    if not isinstance(name, str) or not name.strip() or name.startswith("done "):
        name = CUT_DEFAULT
    name = name.strip()
    xp = _newest("bergama_sections_v*.py")
    X = _exec(xp, "bergama_sections_lib")
    log.append(u"section code: %s (%s %s)" % (xp, X.get("GH_LABEL"), X.get("VERSION")))
    E = X["load_engine"](log)
    E["_DRY0"] = E["DRY"]
    X["_ENGINE_W"][:] = [E["text_w"]]
    gp = os.path.join(BERGAMA_ROOT, "Data", "bergama_pages_common.py")
    G = _exec(gp, "bergama_pages_common")
    try:
        J, per, idx = load_cut(name, log)
    except RuntimeError as ex:
        if name != CUT_DEFAULT:
            raise
        log.append(u"FLAG %s; cut %s drawn instead (press Sections v1.10 or newer once: it caches S4)" % (
            ex, CUT_FALLBACK))
        name = CUT_FALLBACK
        J, per, idx = load_cut(name, log)
    Lv, W = wb_data(name, log)
    zones = s4_zones(E) if name == "S4" else []
    sea_look = dict((s, dict(E["SEASON_LOOK"][s])) for s in SEASONS)
    keep_sea = dict(E["SEA"])

    # v1.6: the smallest cached scale number whose four cuts fit the rows box after a uniform fit (f >= 0.75; the
    # scale is not important, Aras 15:27 UTC); S4 is cut to its designed banks, other cuts to 1.25 rows widths
    want = int(globals().get("scale") or 0)
    dens = sorted((int(d) for d in per), key=int)
    if want:
        dens = [d for d in dens if d == want] or dens
        if want not in dens:
            log.append(u"FLAG scale 1:%d is not cached (cached: %s): the fitting one used" % (
                want, u"/".join(str(d) for d in sorted(int(d) for d in per))))
    rw, rh = ROWS_BOX[2] - ROWS_BOX[0], ROWS_BOX[3] - ROWS_BOX[1]
    extra = 4 * 5.5 + ROW_GAP * 3 + (7.0 if zones else 0.0) + 10.0     # titles, gaps, zone bar, scale bar
    cnt = {}
    rows = None
    try:
        for d in dens:
            M = per[str(d)]["map"]
            cut_its = per[str(d)]["items"]
            cand = []
            for sea in SEASONS:
                its, S = season_cut(X, E, name, J, cut_its, M, sea, log, cnt)
                b0 = X["items_bbox"](its)
                if zones:
                    xa, xb = S.X(zones[0][0] - 2.0), S.X(zones[-1][1] + 2.0)
                elif b0[2] - b0[0] > rw * 1.25:
                    xc = S.X(S.C.s_th)
                    xa = min(max(b0[0], xc - rw * 0.625), b0[2] - rw * 1.25)
                    xb = xa + rw * 1.25
                else:
                    xa, xb = b0[0], b0[2]
                if xa > b0[0] + 0.01 or xb < b0[2] - 0.01:
                    its = clip_x(X, its, xa, xb)
                cand.append((sea, its, S))
            bbs = [X["items_bbox"](its) for _, its, _ in cand]
            w = max(b[2] - b[0] for b in bbs)
            h = sum(b[3] - b[1] for b in bbs)
            f = min(1.0, rw / w, (rh - extra) / h)
            rows = (cand, d, f)
            if f >= 0.75:
                break
            log.append(u"1:%d: four cuts %.0f x %.0f mm, rows box %.0f x %.0f mm: fit %.2f, too small" % (
                d, w, h + extra, rw, rh, f))
    finally:
        E["SEA"].clear()
        E["SEA"].update(keep_sea)
    cand, den, f = rows
    if f < 0.75:
        log.append(u"FLAG even 1:%d needs a fit of %.2f: the cuts are small on the page" % (den, f))
    cand = [(sea, [scaled(it, f, 0.0, 0.0) for it in its], S) for sea, its, S in cand]
    bbs = [X["items_bbox"](its) for _, its, _ in cand]
    log.append(u"scale: Sections 1:%d cache fitted by %.3f = about 1:%d on the page%s" % (
        den, f, int(round(den / f)), u", cut to the designed banks" if zones else u""))
    log.append(u"tinted cutouts made this press: %s (cached in %s)" % (
        u", ".join(u"%s %d" % (k, v) for k, v in sorted(cnt.items())) or u"none, all cached", CACHE_DIR))

    items = []
    y = ROWS_BOX[3]
    gap = max(ROW_GAP, (rh - sum(b[3] - b[1] for b in bbs) - extra + ROW_GAP * 3) / 3.0)
    dx_last = None
    for (sea, its, S), b in zip(cand, bbs):
        y -= 4.0
        items.append(T_(sea.upper(), RAIN_X0, y, 3.2, SEA_COL[sea], True, "L", "seasons"))
        tw = X["text_w_any"](sea.upper(), 3.2, True)
        sw = season_water(X, J, sea)
        word = {"winter": u"Jan–Feb mean over the bed · high end dashed", "spring": u"Mar–Apr low end · high end dashed",
                "summer": u"no flow figure · the strip holds stored water",
                "autumn": u"Oct–Dec high end"}[sea] if (sw or sea == "summer") else u"no level cached"
        items.append(T_(u"%s · %s" % (SEA_MONTHS[sea], word), RAIN_X0 + tw + 2.0, y, 2.2, GREY, False, "L",
                        "seasons"))
        y -= 1.5
        dx, dy = ROWS_BOX[0] - b[0], y - b[3]
        items += [X["_shift"](it, dx, dy) for it in its]
        items += rain_col(E, RAIN_X0, y, b[3] - b[1], sea, W["RAIN"], Lv["depth"])
        dx_last = dx
        y -= (b[3] - b[1]) + gap
    y += gap
    # v1.6: the numbered zones under the last cut (the S4 design, south-west to north-east)
    if zones:
        S = cand[-1][2]
        yz = y - 5.0
        for i, (a, b_, nm) in enumerate(zones):
            xa_, xb_ = S.X(a) * f + dx_last, S.X(b_) * f + dx_last
            items.append(R_(xa_, yz, xb_, yz + 1.3, "E6E1D6" if i % 2 else "CFC8B8", "FFFFFF", 0.1, "zones"))
            items.append(T_(u"%d" % (i + 1), (xa_ + xb_) / 2.0, yz + 2.0, 1.8, INK, True, "C", "zones"))
        items.append(T_(u"SW", S.X(zones[0][0]) * f + dx_last - 1.5, yz, 1.8, GREY, True, "R", "zones"))
        items.append(T_(u"NE", S.X(zones[-1][1]) * f + dx_last + 1.5, yz, 1.8, GREY, True, "L", "zones"))
        y = yz - 1.0
    # one scale bar for the four cuts (same scale)
    K = 1000.0 / den * f
    bar = 10.0 if den <= 500 else 20.0 if den <= 1500 else 50.0
    xb, yb = ROWS_BOX[0], max(12.0, y - 5.0)
    items.append(L_([(xb, yb), (xb + bar * K, yb)], INK, 0.3, "scale"))
    for i in (0.0, 0.5, 1.0):
        items.append(L_([(xb + bar * K * i, yb), (xb + bar * K * i, yb + 1.2)], INK, 0.2, "scale"))
    items.append(T_(u"0", xb, yb - 3.0, 2.0, INK, False, "C", "scale"))
    items.append(T_(u"%d m" % bar, xb + bar * K, yb - 3.0, 2.0, INK, False, "C", "scale"))
    items.append(T_(u"section %s, both banks" % name, xb + bar * K + 6.0, yb - 0.6, 2.0, GREY, False, "L", "scale"))

    # ---- title, the main idea, and the right column: levels diagram, zones, plants, key
    items.append(T_(u"FOUR SEASONS ON ONE CUT", RAIN_X0, 284.0, 7.0, INK, True, "L", "title"))
    items.append(T_(MAIN_IDEA, RAIN_X0, 277.0, 2.8, GREY, False, "L", "title"))
    yy = 266.0
    for ln in _wrap(X, DESIGN_IDEA, 2.2, COL_X1 - COL_X0):
        items.append(T_(ln, COL_X0, yy, 2.2, INK, False, "L", "concept"))
        yy -= 3.0
    yl, yy = levels_diagram(X, E, Lv, W, COL_X0, yy - 3.0, COL_X1)
    items += yl
    if zones:
        yy -= 2.5
        items.append(T_(u"ZONES · %s, south-west to north-east" % name, COL_X0, yy, 2.2, INK, True, "L", "zones"))
        yy -= 3.2
        half = (len(zones) + 1) // 2
        for i, (a, b_, nm) in enumerate(zones):
            cx = COL_X0 + (0.0 if i < half else (COL_X1 - COL_X0) / 2.0)
            cy = yy - (i % half) * 2.7
            items.append(T_(u"%d" % (i + 1), cx + 2.5, cy, 1.8, INK, True, "R", "zones"))
            items.append(T_(nm, cx + 4.0, cy, 1.8, INK, False, "L", "zones"))
        yy -= half * 2.7
    pn = plant_names(E, name)
    yy -= 2.5
    items.append(T_(u"PLANTS ON THE CUT", COL_X0, yy, 2.2, INK, True, "L", "plants"))
    yy -= 3.2
    half = (len(pn) + 1) // 2
    for i, nm in enumerate(pn):
        cx = COL_X0 + (0.0 if i < half else (COL_X1 - COL_X0) / 2.0)
        items.append(T_(nm, cx, yy - (i % half) * 2.7, 1.8, INK, False, "L", "plants"))
    yy -= half * 2.7
    yk, yend = key_rows(E, X, COL_X0, yy - 3.0, COL_X1 - COL_X0, sea_look)
    items += yk
    src = (u"Sources: section base, cut ground, buildings and water levels: Sections %s cache, %s (survey "
           u"Bergama_Altlik.3dm; Manning n 0.050; DSİ Q100 / Q500 and gauge flows 2016-2021 area-scaled, "
           u"research/rain_river_levels). Rain: WaterBoard RAIN (WMO 1991-2020 normals, MGM 17742). Planting bands "
           u"and days: WaterBoard PLANT_BANDS / BAND_DAYS (Rijkswaterstaat memo 2023, pp. 8-16). Zones and plants of "
           u"S4: section engine SECTIONS (27 Oct design). Planting colours: engine SEASON_LOOK. Trees and people: "
           u"asset library Data/cutouts; season tints of the trees are drawing values (ours)." % (
               idx.get("version"), idx.get("run")))
    log.append(src)                                   # v1.3: sources in the log only (Aras 15:23 UTC)
    if yend < 8.0:
        log.append(u"FLAG the right column runs below y 8 mm (to %.0f mm)" % yend)

    bb = X["items_bbox"](items)
    if bb[0] < -0.5 or bb[1] < -0.5 or bb[2] > PAGE_W + 0.5 or bb[3] > PAGE_H + 0.5:
        log.append(u"FLAG drawing runs past the page: ink from x %.0f to %.0f, y %.0f to %.0f mm (page %.0f x %.0f)" % (
            bb[0], bb[2], bb[1], bb[3], PAGE_W, PAGE_H))
    if any(b[2] - b[0] + ROWS_BOX[0] > COL_X0 - 2.0 for b in bbs):
        log.append(u"FLAG a cut reaches into the right column (x > %.0f mm)" % (COL_X0 - 2.0))
    os.makedirs(OUT_DIR, exist_ok=True)
    pdf = X["write_pdf"](os.path.join(OUT_DIR, NAME + u".pdf"), [(PAGE_W, PAGE_H, items)],
                         u"Four seasons on one cut, %s" % name)
    log.append(u"%s  %s" % (pdf, time.strftime("%H:%M:%S")))
    G["pc_present"](pdf, SLIDE, log)
    G["pc_review"](pdf, os.path.join(OUT_DIR, "review"), log)
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, cut %s, 1:%d fitted %.2f, %d FLAG line(s), %.1f s" % (
        u"\n".join(log), GH_LABEL, VERSION, name, den, f, len(flags), time.time() - t0)


def _wrap(X, s, size, width):
    out, ln = [], u""
    for wd in s.split(u" "):
        if ln and X["text_w_any"](ln + u" " + wd, size, False) > width:
            out.append(ln)
            ln = wd
        else:
            ln = (ln + u" " + wd).strip()
    if ln:
        out.append(ln)
    return out


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
