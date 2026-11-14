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
  YEAR     water over the bed through the year on one month axis, from the same cached levels (calculated), the
           summer strip as the design's held water (orange = proposal)
  KEY      EXISTING / PROPOSAL MARKS (proposal orange C07A2E, as the node pages and PageTransit), season asset colours
Reads Data/bergama_pages_common.py (review PNGs, presentation copy), the newest scripts/bergama_sections_v*.py (code
only: engine, writer, cutouts, joined_level), Data/bergama_sections_engine.py, Data/cutouts/, the Sections cache.
Grasshopper: a Button on any input runs it; inputs `cut` (text, a section name of Data/section_lines.json, default
N6-B = the cut nearest the old S4 line of p15/p16: midpoints about 100 m apart, calculated) and `scale` (int, 0 = the
largest cached scale that fits).
"""
import os, re, glob, json, math, time, zlib, struct

VERSION = "v1"
SLIDE = 3                            # slide 3 (main + design idea); presentation/3.pdf
GH_LABEL = "PageSeasons"
OUT_FOLDER = "bergama_page_seasons"
LOG_NAME = "bergama_page_seasons_log.txt"
GH_INPUTS = {"cut": "text = N6-B", "scale": "int 0..3000 = 0"}
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
SEC_CACHE = os.path.join(BERGAMA_ROOT, "cached", "bergama_sections")
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "Seasons"
CUT_DEFAULT = "N6-B"
PAGE_W, PAGE_H = 420.0, 297.0
ROWS_BOX = (14.0, 22.0, 262.0, 266.0)      # mm: x0, y0, x1, y1 of the four cuts
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
        return self._surf(self, s)


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
    base = [it for it in cut_its if il(it) not in skip]
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
    # planting from the cache in the season's look (engine SEASON_LOOK)
    for a, b in S.d["grass"]:
        a, b = max(a, S.lo + 1.2 / K), min(b, S.hi - 1.2 / K)
        if b > a:
            E["tufts"](pg, S, a, b)
    for a, b, h in S.d["reeds"]:
        E["reeds"](pg, S, a, b, h)
    for a, b in S.d["iris"]:
        E["iris"](pg, S, a, b)
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
    it.append(T_(u"m above the lowest bed point of the cut · calculated on this cut (Sections)", x0, ytop - 4.2, 2.0,
                 GREY, False, "L", "year"))
    ch_top, ch_bot = ytop - 9.0, ytop - 9.0 - 34.0
    lab_w = 8.0
    mw = (x1 - x0 - lab_w) / 12.0
    xa = x0 + lab_w
    k = (ch_top - ch_bot - 4.0) / dmax

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
        it.append(R_(X_(m) + 0.6, ch_bot, X_(m + 1) - 0.6, ch_bot + strip_d * k, "F3E3CF", ORANGE, 0.3, "year"))
    it.append(T_(u"%.2f strip (design)" % strip_d, (X_(STRIP_MONTHS[0]) + X_(STRIP_MONTHS[-1] + 1)) / 2.0,
                 ch_bot + strip_d * k + 1.0, 1.9, ORANGE, True, "C", "year"))
    for m in range(12):
        if not any(m in ms for ms in WATER_MONTHS.values()) and m not in STRIP_MONTHS:
            it.append(T_(u"no figure", X_(m + 0.5), ch_bot + 1.2, 1.5, GREY, False, "C", "year"))
    it.append(L_([(xa, ch_bot), (x1, ch_bot)], INK, 0.3, "year"))
    yb = ch_bot - 4.0                                              # months and the four seasons under them
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
    row("box", X["GROUND_FILL"], u"cut ground (survey TIN, Bergama_Altlik.3dm)")
    row("box", X["BACK_FILL"], u"ground behind the cut (survey)")
    row("box", X["H_WALL"], u"houses behind the cut, toned with distance")
    row("box", X["BLD_CUT_FILL"], u"buildings the cut passes through")
    row("box", X["ROAD_FILL"], u"road surface")
    row("box", E["WATER"], u"water of the season over the bed (calculated)", "7DB3D3")
    row("line", E["WATER_LINE"], u"the season's high end (calculated)", (1.6, 0.6, 0.3, 0.6))
    row("line", E["FLOOD"], u"Q100 (short dash) · Q500 (long dash), DSİ flows", (2.0, 1.0))
    y[0] -= 1.0
    hdr(u"PROPOSAL MARKS", ORANGE)
    row("box", "F3E3CF", u"summer strip at the bed low point, held water (design)", ORANGE)
    row("box", "B9CC83", u"planting by rule: reeds and iris on the wet bed, meadow above (ours)", ORANGE)
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
    J, per, idx = load_cut(name, log)
    sea_look = dict((s, dict(E["SEASON_LOOK"][s])) for s in SEASONS)
    keep_sea = dict(E["SEA"])

    # the largest cached scale whose four cuts fit the rows box
    want = int(globals().get("scale") or 0)
    dens = sorted((int(d) for d in per), key=int)
    if want:
        dens = [d for d in dens if d == want] or dens
        if want not in dens:
            log.append(u"FLAG scale 1:%d is not cached (cached: %s): the fitting one used" % (
                want, u"/".join(str(d) for d in sorted(int(d) for d in per))))
    rw, rh = ROWS_BOX[2] - ROWS_BOX[0], ROWS_BOX[3] - ROWS_BOX[1]
    cnt = {}
    rows, den = None, None
    try:
        for d in dens:
            M = per[str(d)]["map"]
            cut_its = per[str(d)]["items"]
            cand = []
            for sea in SEASONS:
                its, S = season_cut(X, E, name, J, cut_its, M, sea, log, cnt)
                cand.append((sea, its, S))
            bbs = [X["items_bbox"](its) for _, its, _ in cand]
            w = max(b[2] - b[0] for b in bbs)
            h = sum(b[3] - b[1] for b in bbs) + ROW_GAP * 3 + 4 * 4.0
            if w <= rw and h <= rh:
                rows, den = (cand, bbs), d
                break
            log.append(u"1:%d: four cuts %.0f x %.0f mm, rows box %.0f x %.0f mm: too big" % (d, w, h, rw, rh))
            rows, den = (cand, bbs), d
    finally:
        E["SEA"].clear()
        E["SEA"].update(keep_sea)
    cand, bbs = rows
    if any(b[2] - b[0] > rw for b in bbs):
        log.append(u"FLAG even 1:%d is wider than the rows box: the page runs past it" % den)
    log.append(u"scale 1:%d (cached by Sections; the largest that fits)" % den)
    log.append(u"tinted cutouts made this press: %s (cached in %s)" % (
        u", ".join(u"%s %d" % (k, v) for k, v in sorted(cnt.items())) or u"none, all cached", CACHE_DIR))

    items = []
    y = ROWS_BOX[3]
    for (sea, its, S), b in zip(cand, bbs):
        y -= 4.0
        items.append(T_(sea.upper(), ROWS_BOX[0], y, 3.2, SEA_COL[sea], True, "L", "seasons"))
        tw = X["text_w_any"](sea.upper(), 3.2, True)
        sw = season_water(X, J, sea)
        word = {"winter": u"Jan–Feb mean over the bed · high end dashed", "spring": u"Mar–Apr low end · high end dashed",
                "summer": u"no flow figure · the strip holds stored water (design)",
                "autumn": u"Oct–Dec high end"}[sea] if (sw or sea == "summer") else u"no level cached"
        items.append(T_(u"%s · %s" % (SEA_MONTHS[sea], word), ROWS_BOX[0] + tw + 2.0, y, 2.2, GREY, False, "L",
                        "seasons"))
        y -= 1.5
        dx, dy = ROWS_BOX[0] - b[0], y - b[3]
        items += [X["_shift"](it, dx, dy) for it in its]
        y -= (b[3] - b[1]) + ROW_GAP
    # one scale bar for the four cuts (same scale)
    K = 1000.0 / den
    bar = 10.0 if den <= 500 else 20.0 if den <= 1500 else 50.0
    xb, yb = ROWS_BOX[0], max(12.0, y + ROW_GAP - 4.0)
    items.append(L_([(xb, yb), (xb + bar * K, yb)], INK, 0.3, "scale"))
    for i in (0.0, 0.5, 1.0):
        items.append(L_([(xb + bar * K * i, yb), (xb + bar * K * i, yb + 1.2)], INK, 0.2, "scale"))
    items.append(T_(u"0", xb, yb - 3.0, 2.0, INK, False, "C", "scale"))
    items.append(T_(u"%d m" % bar, xb + bar * K, yb - 3.0, 2.0, INK, False, "C", "scale"))
    items.append(T_(u"1:%d · section %s, both banks, looking along the stream as Sections draws it" % (den, name),
                    xb + bar * K + 6.0, yb - 0.6, 2.0, GREY, False, "L", "scale"))

    # ---- title, the year chart and the key in the right column
    items.append(T_(u"FOUR SEASONS ON ONE CUT", 14.0, 284.0, 7.0, INK, True, "L", "title"))
    items.append(T_(u"Section %s: the same cut in every season. The ground stays; the water over the bed and the "
                    u"planting change." % name, 14.0, 277.0, 2.8, GREY, False, "L", "title"))
    yc, ybot = year_chart(X, J, COL_X0, 266.0, COL_X1, log)
    items += yc
    yk, yend = key_rows(E, X, COL_X0, ybot - 4.0, COL_X1 - COL_X0, sea_look)
    items += yk
    src = (u"Sources: section base, cut ground, buildings and water levels: Sections %s cache, %s (survey "
           u"Bergama_Altlik.3dm; Manning n 0.050; DSİ Q100 / Q500 and gauge flows 2016-2021 area-scaled, "
           u"research/rain_river_levels). Planting colours: section engine SEASON_LOOK. Trees and people: asset "
           u"library Data/cutouts; season tints of the trees are drawing values (ours)." % (
               idx.get("version"), idx.get("run")))
    yy = max(yend - 3.0, 14.0)
    for ln in _wrap(X, src, 1.8, COL_X1 - COL_X0):
        items.append(T_(ln, COL_X0, yy, 1.8, GREY, False, "L", "credit"))
        yy -= 2.5
    if yy < 6.0:
        log.append(u"FLAG the key and sources run below y 6 mm (to %.0f mm)" % yy)

    bb = X["items_bbox"](items)
    if bb[0] < -0.5 or bb[1] < -0.5 or bb[2] > PAGE_W + 0.5 or bb[3] > PAGE_H + 0.5:
        log.append(u"FLAG drawing runs past the page: ink from x %.0f to %.0f, y %.0f to %.0f mm (page %.0f x %.0f)" % (
            bb[0], bb[2], bb[1], bb[3], PAGE_W, PAGE_H))
    over = [b for b in bbs if b[2] - b[0] + ROWS_BOX[0] > COL_X0 - 2.0]
    if over:
        log.append(u"FLAG a cut reaches into the right column (x > %.0f mm)" % (COL_X0 - 2.0))
    os.makedirs(OUT_DIR, exist_ok=True)
    pdf = X["write_pdf"](os.path.join(OUT_DIR, NAME + u".pdf"), [(PAGE_W, PAGE_H, items)],
                         u"Four seasons on one cut, %s, 1:%d" % (name, den))
    log.append(u"%s  %s" % (pdf, time.strftime("%H:%M:%S")))
    G["pc_present"](pdf, SLIDE, log)
    G["pc_review"](pdf, os.path.join(OUT_DIR, "review"), log)
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, cut %s, 1:%d, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, name, den,
                                                                  len(flags), time.time() - t0)


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
