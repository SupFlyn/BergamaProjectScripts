# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE01 AXO v3.0 (15 Nov 2026; v3.0 = Aras 13:39-13:41 UTC "change the trees on axonometric drawing use it from assets and make those 2d representations 3d", "the trees in the middle of the river is so stupid", "river drawing in axonometric is fucked fix it according to the basemap", "make axonometric get produced by basemap": the whole drawing is now drawn from the MapBase cache, draped on the terrain: the slab (site_alan), parks and green ground, the river (MapBase river, its fill, bank line and water hatch, drawn over the streets as mb_draw does), the street region, the historic walls, the buildings, and the trees (one every 8 m in the 2023 canopy patches MapBase reads, plus its OSM trees; none in the river or on a roof), each tree the asset library cutout (Data/cutouts, traced live) stood up as two crossed copies with a ground shadow; of the booklet drawing only its view, the use class each building stands in and the numbered markers stay; the drawing and its view cached in cached/bergama_page01_axo/axo_model.json for slide 2's node axos; v2.9 = Aras 10:31 UTC "the thickness of the ground is subject to review": the slab as slide 2's node axonometrics draw it (one system): its cut faces a constant SLAB_MM band under the ground edge (was about 5 mm, deeper at the low end), soil hairline hatching on them, a 0.3 base line; v2.8 = run 18 review: buildings across the site_alan edge (the long sheds at the front) hung over the slab: every footprint is now cut to site_alan before it is raised; v2.7 (15 Nov 2026; v2.7 = v2.6 undone: Aras 10:31-10:32 UTC wants every building coloured by this axo's classes (slide 2's node axos copy them), so the residential mass keeps its palette colour (FAB regular) again; v2.6 = Aras 12:10 UTC "review the drawings yourself and compare with the examples": as the liked axo diagrams (F03, D12: context = white volumes, colour only where it means something; Aras 12 Nov "lighter more soft colours"), the residential fabric (the mass of the town) is drawn as the A05 white houses (roof FFFFFF, walls the A05 wall tone CDC8BC and a lighter lit face, outline the A05 street edge 9E9889) instead of mid grey; the coloured uses stand out on it; v2.5 = Aras 10:34 UTC "axo drawing has mistakes how road is drawn and also the buildings doesnt seem right in many places": the booklet's 212 loose road strips are replaced by MapBase's one closed street region (cut to site_alan, draped on the terrain), and its buildings (the 9 Nov board site model: merged blocks, boxes with no survey footprint) by the MapBase footprints, drawn the booklet engine's way (its view, fitted to the slab it drew; halo, lit / shaded walls, roof) with the class of the booklet building each stands in and its surveyed floors as height; trees keep their place among the buildings; legend counts recounted; v2.4 = Aras 05:55 UTC "same goes for this axo" (too cramped, extend it from most left to most right): the numbered list leaves the drawing's right side and joins the legend (a numbered disc per row), the drawing's box is cut to the drawing itself, so the axo runs the whole page width; v2.3 = Aras 04:58 UTC approved cleaning the numbered list (booklet content): "Les Pergamon Boutique Hotel" was listed twice (5 and 6, two buildings): one row, both markers 5, rows 7-12 renumbered 6-11 and moved up; the "· 5.00 m" notes (a default height, not a measure) dropped; "most enclosed stretch" kept only on the lowest sky view, the others "enclosed stretch"; "Kızıl Avlu" (the name was in broken order); list words up to 1.25 x larger (as far as the widest row stays in the extent), notes placed after their names; v2.2 = slide 1 run 7: a tall empty band between the legend and the drawing: the drawing now sits 6 mm under the legend, the empty space left at the page foot; v2.1 = slide 1 review (run 5): the title "What is there" repeated Plan 01's title: now "Heights, heritage, water, green" (the booklet caption's own words), and the title + legend sit ABOVE the drawing), slide 1 (analysis): the booklet's page-3 axonometric ("What is
there · heights, heritage, water, green", selinus_board v65+ / its axonometric engine), only scaled down and recoloured.

Aras 14 Nov 16:15 UTC: "you had the proper axonometric drawing before why did you fucked it up only thing you needed to
do is to scale it down and change the colours". So v1-v1.6 (an axo of our own) are dropped and this script draws the
booklet drawing itself, from selinus_board's own cache of it (nothing redrawn, nothing read from a PDF):
  ~/Downloads/Bergama/cached/booklet/selinus_board/items.json, page p03, drawing sb_axo_what_is_there (mm, y up):
  every face, tree, road, label and the legend exactly as selinus_board exported them (Aras 12:38 UTC "if one script
  does that job cache it and make it usable by the next script"). Its p03 part is cached once in
  cached/bergama_page01_axo/p03_axo.json (re-read when items.json changes).
The two changes:
  SCALE: the drawing and its words scaled as one to the page (A3 landscape, or the slide's page_mm), legend under it.
  COLOURS: each building use class of the booklet (roof, its two wall shades and outline) takes a colour of the current
  palette (MapBase FAB / FAB_COM, the one palette source); the wall shades keep the booklet's light-to-dark steps.
  The purples (sacred, civic) are gone. Everything else (ground, water, trees, people) keeps its booklet colour.
No sources in the drawing (Aras 15:23 UTC). Outputs: output/bergama_page01_axo/WhatIsThereAxo.pdf / .svg, review PNGs.
Reads: Data/bergama_pages_common.py, the newest MapBase script (palette) and its cache (streets, buildings, floors),
Data/bergama_dem_glo30.json (terrain), selinus_board's items.json (above).
"""
import os, re, time, json

VERSION = "v3.0"
GH_LABEL = "Page01Axo"
OUT_FOLDER = "bergama_page01_axo"
LOG_NAME = "bergama_page01_axo_log.txt"
GH_INPUTS = {}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
SRC = os.path.join(BERGAMA_ROOT, "cached", "booklet", "selinus_board", "items.json")
CACHE = os.path.join(BERGAMA_ROOT, "cached", "bergama_page01_axo", "p03_axo.json")
DID = "sb_axo_what_is_there"
NAME = "WhatIsThereAxo"
A3 = (420.0, 297.0)
PT = 25.4 / 72.0                   # mm per pt
GROUND = "FAF8F1"
SLAB_MM = 1.4                      # v2.9: page mm, the ground slab's cut face (slide 2 spine AXO_SLAB)
WHITE_RES = ("FFFFFF", "E9E6DF", "CDC8BC", "9E9889")   # v2.6: roof, lit wall, shaded wall, outline (MapBase A05 look)                  # the booklet axo's ground colour: a see-through fill is mixed onto it
# booklet use class: (roof, lit wall, shaded wall, outline) as exported (read from items.json, 9 Nov run) -> the
# current palette entry (table, key) of MapBase
USE = [("residential", ("CCA363", "B9872F", "705426", "8F6304"), ("FAB", "regular")),
       ("commerce", ("734C17", "653E00", "3C2300", "4A2C01"), ("FAB_COM", "regular")),
       ("mixed", ("A67628", "926202", "593B01", "6C4803"), ("FAB_COM", "construction")),
       ("industry", ("847E75", "726B60", "44403A", "554E43"), ("FAB", "large")),
       ("civic", ("7F5B7B", "73476E", "432B41", "5A2E56"), ("FAB_COM", "large")),
       ("sacred", ("452842", "3F1B3C", "220E20", "310C2E"), ("FAB", "sacred")),
       ("ruins", ("84573E", "7A4423", "472917", "622B04"), ("FAB", "monument"))]


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


class Sheet(object):
    """what pc_sheet / pc_write need: box (page mm), w, h, den, k"""
    def __init__(self, box, w, h):
        self.box, self.w, self.h, self.den, self.k = box, w, h, 1.0, 1.0


def p03(log):
    """selinus_board's p03 axonometric: (drawing, texts, legend, caption), cached apart from the 104 MB items.json"""
    if not os.path.isfile(SRC):
        raise RuntimeError(u"%s missing: press selinus_board once (it writes the booklet items), then this" % SRC)
    mt = os.path.getmtime(SRC)
    try:
        with open(CACHE, encoding="utf-8") as f:
            c = json.load(f)
        if c.get("src_mtime") == mt:
            log.append(u"booklet p03 axo: cache %s (items.json of %s)" % (CACHE, c.get("run")))
            return c
    except Exception:
        pass
    with open(SRC, encoding="utf-8") as f:
        d = json.load(f)
    P = d["pages"]["p03"]
    dr = [it for it in P if it.get("id") == DID][0]
    tx = dict((it["id"], it) for it in P if it.get("kind") == "text")
    lg = [it for it in P if it.get("kind") == "legend" and it.get("drawing") == DID]
    c = {"src_mtime": mt, "run": d.get("run"), "version": d.get("version"), "extent": dr["extent"],
         "shapes": [s for L in dr["layers"] for s in L["shapes"]],
         "texts": [t for t in tx.values() if (t.get("anchor") or {}).get("drawing") == DID],
         "legend": [(e["swatch"], tx.get(e["text"], {}).get("string", u"")) for e in (lg[0]["entries"] if lg else [])],
         "caption": next((t["string"] for t in tx.values() if t.get("role") == "caption"), u"")}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False)
    log.append(u"booklet p03 axo: read from %s (%s, run %s), cached in %s" % (SRC, d.get("version"), d.get("run"),
                                                                            CACHE))
    return c


def clean_list(c, tw, log):
    """v2.3: the numbered list (booklet coords): merge the duplicate hotel rows, renumber, drop default heights"""
    T = c["texts"]
    X0, Y0 = 314.0, 120.0                                # the list block (booklet mm); marker 12 sits at y 26
    inl = lambda t: t["anchor"]["pt"][0] >= X0 and t["anchor"]["pt"][1] >= Y0
    num = lambda t: t["string"].strip().isdigit()
    badges = dict((int(t["string"]), t) for t in T if inl(t) and num(t))
    names = sorted([t for t in T if inl(t) and not num(t) and not t["string"].startswith(u"\u00b7")
                    and t["string"] != u"NUMBERED ON THE DRAWING"], key=lambda t: -t["anchor"]["pt"][1])
    rowy = lambda t: t["anchor"]["pt"][1]
    name_of = lambda n: next((t for t in names if abs(rowy(t) - rowy(badges[n])) < 1.0), None)
    dup = [n for n in sorted(badges) if n > 1 and name_of(n) and name_of(n - 1) and
           name_of(n)["string"] == name_of(n - 1)["string"]]
    if not dup:
        log.append(u"list: no duplicate rows found")
        return c
    d = dup[0]
    yd, dy = rowy(badges[d]), rowy(badges[d - 1]) - rowy(badges[d])
    shapes, texts = [], []
    for sh in c["shapes"]:
        g = sh.get("grp") or u""
        pts = [q for R in sh.get("rings", []) for q in R] or sh.get("pts", [])
        if g.startswith(u"labels") and pts and min(q[0] for q in pts) >= X0 - 2.0 and min(q[1] for q in pts) >= Y0:
            cy = sum(q[1] for q in pts) / len(pts)
            if abs(cy - yd) < dy * 0.45:
                continue                                 # the duplicate row's badge
            if cy < yd - dy * 0.45:
                sh = dict(sh, rings=[[(q[0], q[1] + dy) for q in R] for R in sh["rings"]]) if "rings" in sh else \
                    dict(sh, pts=[(q[0], q[1] + dy) for q in sh["pts"]])
        shapes.append(sh)
    for t in T:
        x, y = t["anchor"]["pt"]
        if inl(t):
            if abs(y - yd) < 1.0:
                continue                                 # the duplicate row's words
            if y < yd - 1.0:
                t = dict(t, anchor=dict(t["anchor"], pt=[x, y + dy]))
        if num(t):
            n = int(t["string"])
            if n >= d:
                t = dict(t, string=str(n - 1))           # the drawing's marker d becomes d-1, the rest renumbered
        texts.append(t)
    c = dict(c, shapes=shapes, texts=texts)
    log.append(u"list: rows %d and %d were the same place (%s): merged, %d markers renumbered" % (
        d - 1, d, name_of(d - 1)["string"], len([b for b in badges if b >= d])))
    # notes: no default heights, one "most enclosed", names in full, words larger, notes after their names
    T = c["texts"]
    rows = [t for t in T if inl(t) and not num(t)]
    sky = [(int(re.search(r"(\d+)", t["string"]).group(1)), t) for t in rows if t["string"].startswith(u"Sky view")]
    lo = min(v for v, t in sky) if sky else None
    out = []
    for t in T:
        st = t["string"]
        if inl(t):
            if st == u"\u00b7 most open stretch of the bed":
                st = u"\u00b7 most open stretch"                 # shorter notes, so the list words can grow
            if st.strip() == u"\u00b7 5.00 m":
                continue
            if st == u"Kızıl Avlu Tapınağı Mısır Tanrıları":
                st = u"Kızıl Avlu"
            elif st == u"\u00b7 most enclosed stretch of the bed":
                nm = next((r for r in rows if r["string"].startswith(u"Sky view") and
                           abs(r["anchor"]["pt"][1] - t["anchor"]["pt"][1]) < 1.0), None)
                v = int(re.search(r"(\d+)", nm["string"]).group(1)) if nm else lo
                st = u"\u00b7 most enclosed stretch" if v == lo else u"\u00b7 enclosed stretch"
            t = dict(t, string=st)
        out.append(t)
    # the larger list words: up to 1.25 x, as far as the widest row stays inside the booklet's extent
    nm_ = lambda t: inl(t) and not num(t) and not t["string"].startswith(u"\u00b7")
    wrow = 0.0
    for r in out:
        if nm_(r):
            nt = next((t for t in out if inl(t) and t["string"].startswith(u"\u00b7") and
                       abs(t["anchor"]["pt"][1] - r["anchor"]["pt"][1]) < 1.0), None)
            w = tw(r["string"], r["size_pt"] * PT, True) + (1.2 + tw(nt["string"], nt["size_pt"] * PT, False)
                                                             if nt else 0.0)
            wrow = max(wrow, r["anchor"]["pt"][0] + w)
    x0 = min(r["anchor"]["pt"][0] for r in out if nm_(r))
    f = max(1.0, min(1.25, (c["extent"][2] - x0) / max(wrow - x0, 1.0)))
    out = [dict(t, size_pt=t["size_pt"] * f) if inl(t) and not num(t) else t for t in out]
    log.append(u"list: words x %.2f (widest row %.0f mm)" % (f, (wrow - x0) * f))
    for t in out:                                        # each note right after its row's name
        if inl(t) and t["string"].startswith(u"\u00b7"):
            nm = next((r for r in out if inl(r) and not num(r) and not r["string"].startswith(u"\u00b7") and
                       abs(r["anchor"]["pt"][1] - t["anchor"]["pt"][1]) < 1.0), None)
            if nm:
                t["anchor"] = dict(t["anchor"], pt=[nm["anchor"]["pt"][0] + tw(nm["string"], nm["size_pt"] * PT,
                                                                                True) + 1.2, t["anchor"]["pt"][1]])
    return dict(c, texts=out)


# ---------------------------------------------------------------- v2.5: roads and buildings from MapBase
# Aras 15 Nov 10:34 UTC: "axo drawing has mistakes how road is drawn and also the buildings doesnt seem right in many
# places". The booklet's roads were 212 separate strips (gaps at junctions, loose pieces) and its buildings came from
# the 9 Nov board site model. Both are redrawn from the one base map (MapBase cache, survey m) in the booklet
# engine's own way: its view (fitted to the booklet's slab, below), its terrain, its building faces and colours.
PHI = 32.9                         # deg: the booklet engine's view angle below the horizontal (DIAG_SRC PHI)
DEM = os.path.join("Data", "bergama_dem_glo30.json")
STOREY = {"civic": 3.5, "sacred": 5.0, "industry": 4.5}   # m per floor (Aras 12 Nov), else 3.0
CTX = ("FAF8F1", "D7D3C2", "BFBBAB", "949081")             # the engine's context building: roof, lit, shade, outline
SLAB_TOP = "EFEDE6"                # the slab's top face (fill) in the booklet drawing
ROAD = ("FAF8F1", "949081", 0.142)  # the booklet's street fill, edge colour, edge width (pt)
LEGEND_CLS = (("Workshops", "industry"), ("Commerce", "commerce"), ("Mixed use", "mixed"),
              ("Residential", "residential"), ("Sacred", "sacred"), ("Civic", "civic"), ("Ruins", "ruins"))


def _pip(x, y, R):
    ins, n = False, len(R)
    for i in range(n):
        (ax, ay), (bx, by) = R[i - 1], R[i]
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            ins = not ins
    return ins


def _clip(R, H):
    """ring R cut to the convex window H (half-planes (a, b, c): a x + b y + c >= 0), Sutherland-Hodgman"""
    for a, b, c0 in H:
        out, n = [], len(R)
        for i in range(n):
            p, q = R[i - 1], R[i]
            fp, fq = a * p[0] + b * p[1] + c0, a * q[0] + b * q[1] + c0
            if fq >= 0:
                if fp < 0:
                    t = fp / (fp - fq)
                    out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                out.append(q)
            elif fp >= 0:
                t = fp / (fp - fq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
        R = out
        if len(R) < 3:
            return []
    return R


class AxoView(object):
    """the booklet engine's view, fitted to the slab it drew (X = c0 + c1 x + c2 y; Y = oy + s (-c2 x + c1 y) +
    k cos(phi) z(x, y)), z = the DEM above the booklet's lowest node (offset fitted on the slab edge)"""

    def __init__(self, ring, corners, log):
        import math as m_
        self.m = m_
        E = []
        for i in range(4):
            p, q = corners[i], corners[(i + 1) % 4]
            L = m_.hypot(q[0] - p[0], q[1] - p[1])
            n = max(1, int(L / 15.0))                    # the engine's TERRAIN_CELL edge points
            E += [(p[0] + (q[0] - p[0]) * j / n, p[1] + (q[1] - p[1]) * j / n) for j in range(n)]
        if len(E) != len(ring):
            raise RuntimeError(u"the booklet slab has %d edge points, site_alan gives %d: not the same frame" % (
                len(ring), len(E)))
        # least squares X = c0 + c1 x + c2 y (3 x 3 normal equations)
        mx, my = sum(e[0] for e in E) / len(E), sum(e[1] for e in E) / len(E)
        mX = sum(r[0] for r in ring) / len(ring)
        sxx = sum((e[0] - mx) ** 2 for e in E)
        syy = sum((e[1] - my) ** 2 for e in E)
        sxy = sum((e[0] - mx) * (e[1] - my) for e in E)
        sxX = sum((e[0] - mx) * (r[0] - mX) for e, r in zip(E, ring))
        syX = sum((e[1] - my) * (r[0] - mX) for e, r in zip(E, ring))
        det = sxx * syy - sxy * sxy
        self.c1 = (sxX * syy - syX * sxy) / det
        self.c2 = (syX * sxx - sxX * sxy) / det
        self.c0 = mX - self.c1 * mx - self.c2 * my
        res = max(abs(self.c0 + self.c1 * e[0] + self.c2 * e[1] - r[0]) for e, r in zip(E, ring))
        self.k = m_.hypot(self.c1, self.c2)
        ph = m_.radians(PHI)
        self.s, self.kz = m_.sin(ph), self.k * m_.cos(ph)
        self.dem(log)
        fl = [self.s * (-self.c2 * e[0] + self.c1 * e[1]) for e in E]
        rr = [r[1] - f for r, f in zip(ring, fl)]
        self.oy = min(rr)
        zE = [(v - self.oy) / self.kz for v in rr]
        zD = [self.zdem(e[0], e[1]) for e in E]
        self.z0 = sum(a - b for a, b in zip(zD, zE)) / len(E)
        rms = (sum((a - b - self.z0) ** 2 for a, b in zip(zD, zE)) / len(E)) ** 0.5
        log.append(u"view: fitted to the booklet slab (%d edge points): across %.4f mm off at most, %.4f mm per m; "
                   u"terrain = elevation model - %.1f m, %.1f m rms on the slab edge" % (len(E), res, self.k, self.z0,
                                                                                      rms))
        if res > 0.02:
            log.append(u"FLAG view: the slab does not fit site_alan (%.3f mm): roads and buildings may be misplaced"
                       % res)
        if rms > 8.0:
            log.append(u"FLAG view: terrain %.1f m rms off the booklet's on its edge" % rms)
        a, b, c = self.c1, self.c2, self.s
        self.inv = (a * a * c + b * b * c)               # determinant of [[c1, c2], [-s c2, s c1]]

    def dem(self, log):
        p = os.path.join(BERGAMA_ROOT, DEM)
        with open(p, encoding="utf-8") as f:
            J = json.load(f)
        nr, nc, P = int(J["rows"]), int(J["cols"]), J["pts"]
        self.Z = [P[r * nc:(r + 1) * nc] for r in range(nr)]
        self.Z = [[q[2] for q in row] for row in self.Z]
        self.gx0, self.gy0 = P[0][0], P[0][1]
        self.gdx = (P[nc - 1][0] - P[0][0]) / float(nc - 1)
        self.gdy = (P[(nr - 1) * nc][1] - P[0][1]) / float(nr - 1)
        self.nr, self.nc = nr, nc

    def zdem(self, x, y):
        fi = min(self.nc - 1.000001, max(0.0, (x - self.gx0) / self.gdx))
        fj = min(self.nr - 1.000001, max(0.0, (y - self.gy0) / self.gdy))
        i, j = int(fi), int(fj)
        a, b = fi - i, fj - j
        Z = self.Z
        return (Z[j][i] * (1 - a) + Z[j][i + 1] * a) * (1 - b) + (Z[j + 1][i] * (1 - a) + Z[j + 1][i + 1] * a) * b

    def z(self, x, y):
        return max(0.0, self.zdem(x, y) - self.z0)

    def depth(self, x, y):
        return -self.c2 * x + self.c1 * y               # larger = farther (drawn first)

    def P(self, x, y, h=0.0):
        return (self.c0 + self.c1 * x + self.c2 * y,
                self.oy + self.s * self.depth(x, y) + self.kz * (self.z(x, y) + h))

    def back(self, X, Y):
        """plan point of a screen point on the ground (the terrain iterated)"""
        z = 0.0
        x = y = 0.0
        for _ in range(4):
            A, B = X - self.c0, Y - self.oy - self.kz * z
            # c1 x + c2 y = A ; s (-c2 x + c1 y) = B
            x = (A * self.c1 * self.s - self.c2 * B) / self.inv
            y = (self.c2 * self.s * A + self.c1 * B) / self.inv
            z = self.z(x, y)
        return x, y

    def facing(self, nx, ny):
        """outward normal (nx, ny): visible, lit (the engine's View.facing, in its own sin / cos)"""
        st, ct = self.c1 / self.k, -self.c2 / self.k
        return nx * ct + ny * st < -1e-9, (nx * st - ny * ct) < 0


def _bld_shapes(V, P, h, cols, topic):
    """the engine's draw_building for one footprint P (survey m, ccw) of height h: halo, walls far to near, roof"""
    roof, lit, shade, outline = cols
    walls = []
    n = len(P)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = (dx * dx + dy * dy) ** 0.5
        if L < 1e-6:
            continue
        vis, lt = V.facing(dy / L, -dx / L)
        if vis:
            walls.append((V.depth((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0),
                          [V.P(p[0], p[1]), V.P(q[0], q[1]), V.P(q[0], q[1], h), V.P(p[0], p[1], h)],
                          lit if lt else shade))
    rf = [V.P(x, y, h) for x, y in P]
    walls.sort(key=lambda t: -t[0])
    sh = lambda rings, fi, st, w: {"t": "poly", "rings": rings, "fill": fi, "stroke": st, "width_pt": w,
                                   "dash_pt": None, "opacity": None, "grp": u"buildings/mb"}
    out = []
    if topic:
        out.append(sh([w_[1] for w_ in walls] + [rf], None, outline, 0.34))
    out += [sh([R_], c_, c_, 0.113) for _, R_, c_ in walls]
    out.append(sh([rf], roof, roof if topic else outline, 0.113 if topic else 0.142))
    return out


# ================================================================ AXO_LIB_END (v3.0: slide 2's spine execs everything above)
# ---------------------------------------------------------------- v3.0: trees from the asset cutouts, stood up in 3D
# Aras 15 Nov 13:39 UTC: "change the trees on axonometric drawing use it from assets and make those 2d representations 3d
# with rotating or raying or something". Each tree is the asset library's own cutout (Data/cutouts, the sections'
# trees), read live: its PNG decoded here (pure Python, no add-ons), its silhouette and its darkest third traced on a
# coarse grid (TREE_ROWS rows; a tree is about 1 mm tall on the page) in the cutout's own colours, cached in
# cached/bergama_page01_axo/tree_traces.json (re-traced when a PNG changes). In the drawing each tree stands as TWO
# copies crossed at 90 degrees (a billboard cross, each turned 45 degrees off the view), the back halves in the
# cutout's lighter depth tone (_d1), the front halves in its own colours, with a ground shadow: the 2D cutout reads as
# a volume, as the section trees and the axo share one asset.
TREE_ROWS = 16                     # grid rows a cutout is traced on
TREE_SET = ("plane_1", "plane_2", "plane_3", "plane_4", "plane_5", "plane_6", "ash_1", "ash_2", "ash_3", "ash_4")
TREE_SP = 8.0                      # m: one tree every TREE_SP m (hex grid) in a 2023 canopy patch (a drawing rule)
TREE_MIN_A = 10.0                  # m2: canopy patches smaller than this are left out (shrubs, image noise)
TREE_D = (3.5, 8.5)                # m: crown width drawn, from the patch area per tree, clamped
SHADOW = "DDD9CC"                  # the tree's ground shadow (drawing value)
PARK_C = "C2CCB3"                  # parks and green ground (the booklet legend's colour)
WALL_C = "84573E"                  # historic wall lines (the booklet legend's colour)
PARK_KINDS = ("park", "green", "wood", "cemetery")
TREE_KEY = "6E7A4C"                 # the legend dot for trees (drawing value)


def _png_rgba(path):
    """an 8-bit RGBA / RGB PNG (not interlaced) as (w, h, rows of bytes, bytes per pixel), pure Python"""
    import struct, zlib
    with open(path, "rb") as f:
        b = f.read()
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(u"not a PNG")
    i, idat, w = 8, [], None
    while i < len(b):
        n, typ = struct.unpack(">I4s", b[i:i + 8])
        d = b[i + 8:i + 8 + n]
        if typ == b"IHDR":
            w, h, bd, ct, _, _, il = struct.unpack(">IIBBBBB", d)
            if bd != 8 or ct not in (2, 6) or il:
                raise ValueError(u"PNG type %d/%d/%d not read" % (bd, ct, il))
            bpp = 4 if ct == 6 else 3
        elif typ == b"IDAT":
            idat.append(d)
        i += 12 + n
    raw = zlib.decompress(b"".join(idat))
    st = w * bpp
    rows, prev = [], bytearray(st)
    p = 0
    for _ in range(h):
        ft = raw[p]
        line = bytearray(raw[p + 1:p + 1 + st])
        p += 1 + st
        if ft == 1:
            for x in range(bpp, st):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif ft == 2:
            for x in range(st):
                line[x] = (line[x] + prev[x]) & 255
        elif ft == 3:
            for x in range(st):
                a = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif ft == 4:
            for x in range(st):
                a = line[x - bpp] if x >= bpp else 0
                c_ = prev[x - bpp] if x >= bpp else 0
                b_ = prev[x]
                pa, pb, pc = abs(b_ - c_), abs(a - c_), abs(a + b_ - 2 * c_)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b_ if pb <= pc else c_)) & 255
        rows.append(line)
        prev = line
    return w, h, rows, bpp


def _cells_rings(S):
    """the outline rings (grid corners, region on the left) of a set S of (col, row) cells"""
    E = {}
    for (i, j) in S:
        for a, b, nb in (((i, j + 1), (i + 1, j + 1), (i, j + 1)), ((i + 1, j + 1), (i + 1, j), (i + 1, j)),
                         ((i + 1, j), (i, j), (i, j - 1)), ((i, j), (i, j + 1), (i - 1, j))):
            if nb not in S:
                E.setdefault(a, []).append(b)
    rings = []
    while E:
        a = next(iter(E))
        R = [a]
        cur = a
        while True:
            nx_ = E[cur].pop()
            if not E[cur]:
                del E[cur]
            if nx_ == a:
                break
            R.append(nx_)
            cur = nx_
            if cur not in E:
                break
        out = [R[k] for k in range(len(R)) if not (
            (R[k - 1][0] == R[k][0] == R[(k + 1) % len(R)][0]) or (R[k - 1][1] == R[k][1] == R[(k + 1) % len(R)][1]))]
        if len(out) >= 3:
            rings.append(out)
    return rings


def _trace_png(path):
    """a cutout traced: {"wr": width / height, "sil": (colour, rings), "dark": (colour, rings)}; rings in (u, v),
    u across from the trunk and v up from the foot, both in tree heights"""
    w, h, rows, bpp = _png_rgba(path)
    cell = h / float(TREE_ROWS)
    nc = int(w / cell + 0.999)
    stp = max(1, int(cell / 4))
    cells = {}
    for j in range(TREE_ROWS):
        for i in range(nc):
            n = cov = r = g = b = 0
            for y in range(int(j * cell), min(h, int((j + 1) * cell)), stp):
                L = rows[y]
                for x in range(int(i * cell), min(w, int((i + 1) * cell)), stp):
                    n += 1
                    if bpp == 3 or L[x * 4 + 3] > 128:
                        k = x * bpp
                        cov += 1
                        r += L[k]
                        g += L[k + 1]
                        b += L[k + 2]
            if n and cov >= 0.45 * n:
                cells[(i, TREE_ROWS - 1 - j)] = (r / cov, g / cov, b / cov)
    if not cells:
        raise ValueError(u"no opaque cells")
    foot = [i for (i, j) in cells if j <= 1] or [i for (i, j) in cells]
    tx = (sum(foot) / float(len(foot)) + 0.5) * cell
    lum = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    ls = sorted(lum(c) for c in cells.values())
    t1 = ls[len(ls) // 3]
    hexc = lambda cs: u"%02X%02X%02X" % tuple(int(sum(c[k] for c in cs) / len(cs)) for k in range(3))
    dk = dict((q, c) for q, c in cells.items() if lum(c) <= t1)
    uv = lambda R: [((q[0] * cell - tx) / h, q[1] * cell / h) for q in R]
    return {"wr": w / float(h), "sil": (hexc(list(cells.values())), [uv(R) for R in _cells_rings(set(cells))]),
            "dark": (hexc(list(dk.values())) if dk else None, [uv(R) for R in _cells_rings(set(dk))])}


def tree_traces(log):
    """{name: {"main": trace, "d1": trace}} for TREE_SET, from Data/cutouts (cached until a PNG changes)"""
    src = os.path.join(BERGAMA_ROOT, "Data", "cutouts")
    cp = os.path.join(os.path.dirname(CACHE), "tree_traces.json")
    try:
        with open(cp, encoding="utf-8") as f:
            T = json.load(f)
    except Exception:
        T = {}
    out, made = {}, 0
    for nm in TREE_SET:
        for key, fn in (("main", nm + ".png"), ("d1", nm + "_d1.png")):
            p = os.path.join(src, fn)
            if not os.path.isfile(p):
                continue
            mt = os.path.getmtime(p)
            e = T.get(fn)
            if not e or e.get("mtime") != mt or e.get("rows") != TREE_ROWS:
                try:
                    e = dict(_trace_png(p), mtime=mt, rows=TREE_ROWS)
                except Exception as ex:
                    log.append(u"FLAG trees: %s not traced (%s: %s)" % (fn, type(ex).__name__, ex))
                    continue
                T[fn] = e
                made += 1
            out.setdefault(nm, {})[key] = e
    out = dict((k, v) for k, v in out.items() if "main" in v)
    for v in out.values():
        v.setdefault("d1", v["main"])
    if made:
        try:
            os.makedirs(os.path.dirname(cp), exist_ok=True)
            with open(cp, "w", encoding="utf-8") as f:
                json.dump(T, f)
        except Exception as ex:
            log.append(u"trees: traces not cached (%s)" % ex)
    log.append(u"trees: %d asset cutouts from %s (%d traced this press, the rest from %s)" % (
        len(out), src, made, cp))
    if not out:
        log.append(u"FLAG trees: no tree cutouts found in %s: no trees drawn" % src)
    return out


def _tree_shapes(V, x, y, D, tr, anchor):
    """one tree: ground shadow, the two crossed cutouts' back halves (depth tone), then their front halves"""
    m_ = V.m
    k = V.k
    e = (V.c1 / k, V.c2 / k)                             # across the view (screen right)
    f = (-V.c2 / k, V.c1 / k)                            # into the view (farther)
    r2 = 2 ** -0.5
    d1 = ((e[0] + f[0]) * r2, (e[1] + f[1]) * r2)
    d2 = ((e[0] - f[0]) * r2, (e[1] - f[1]) * r2)
    sv = lambda d: (V.c1 * d[0] + V.c2 * d[1], V.s * (-V.c2 * d[0] + V.c1 * d[1]))
    B = V.P(x, y)
    Hm = min(12.0, max(4.0, D / max(tr["main"]["wr"], 0.3)))
    sh = lambda rings, fi, grp=u"trees/mb": {"t": "poly", "rings": rings, "fill": fi, "stroke": None, "width_pt": 0.0,
                                             "dash_pt": None, "opacity": None, "grp": grp, "anchor": anchor,
                                             "bld": None}
    se, sf = sv(e), sv(f)
    rs = D * 0.45
    out = [sh([[(B[0] + rs * (m_.cos(t) * se[0] + m_.sin(t) * sf[0]) + 0.15 * rs * se[0],
                 B[1] + rs * (m_.cos(t) * se[1] + m_.sin(t) * sf[1])) for t in
                [i * m_.pi / 8.0 for i in range(16)]]], SHADOW)]

    def put(R, d):
        s_ = sv(d)
        return [(B[0] + u * Hm * s_[0], B[1] + u * Hm * s_[1] + v * Hm * V.kz) for u, v in R]

    def half(rings, sign):
        H = [(sign, 0.0, 0.0)]                           # u * sign >= 0
        return [Q for Q in (_clip(R, H) for R in rings) if len(Q) >= 3]
    back = [put(R, d1) for R in half(tr["d1"]["sil"][1], 1.0)] + [put(R, d2) for R in half(tr["d1"]["sil"][1], -1.0)]
    if back:
        out.append(sh(back, tr["d1"]["sil"][0]))
    front = [put(R, d1) for R in half(tr["main"]["sil"][1], -1.0)] + \
            [put(R, d2) for R in half(tr["main"]["sil"][1], 1.0)]
    if front:
        out.append(sh(front, tr["main"]["sil"][0]))
    if tr["main"]["dark"][0]:
        dk = [put(R, d1) for R in half(tr["main"]["dark"][1], -1.0)] + \
             [put(R, d2) for R in half(tr["main"]["dark"][1], 1.0)]
        if dk:
            out.append(sh(dk, tr["main"]["dark"][0]))
    return out


def rebuild(c, G, log):
    """c (the booklet p03 drawing, booklet mm) with its roads and buildings redrawn from MapBase"""
    import math as m_
    S = c["shapes"]
    slab = next((i for i, s in enumerate(S[:6]) if s["t"] == "poly" and s.get("fill") == SLAB_TOP), None)
    if slab is None:
        log.append(u"FLAG rebuild: the booklet slab not found: roads and buildings kept as the booklet drew them")
        return c, None
    corners = [tuple(q[:2]) for q in G["pc_site_map"](1000.0, log).ring]
    V = AxoView([tuple(q) for q in S[slab]["rings"][0]], corners, log)
    ns_, C = G["pc_mb_data"](log)
    # ---- the site_alan window as half-planes (inside >= 0)
    cx_, cy_ = sum(q[0] for q in corners) / 4.0, sum(q[1] for q in corners) / 4.0
    H = []
    for i in range(4):
        p, q = corners[i], corners[(i + 1) % 4]
        a, b = -(q[1] - p[1]), q[0] - p[0]
        c0 = -(a * p[0] + b * p[1])
        if a * cx_ + b * cy_ + c0 < 0:
            a, b, c0 = -a, -b, -c0
        nn = m_.hypot(a, b)
        H.append((a / nn, b / nn, c0 / nn))
    inside = lambda x, y: all(a * x + b * y + c0 >= 0 for a, b, c0 in H)

    # ---- the booklet's buildings: halo, walls, roof per building; class, height, ground footprint (screen)
    USE_ROOF = dict((u[1][0], (u[0], u[1])) for u in USE)
    USE_ROOF[CTX[0]] = ("context", CTX)
    isb = lambda s: (s.get("grp") or u"").startswith(u"buildings")
    first = next(i for i in range(slab + 1, len(S)) if isb(S[i]))
    last = max(i for i in range(len(S)) if isb(S[i]))
    old, cur = [], []
    runs, run = [], []                                   # tree / other runs between buildings: (after building n, shapes)
    for i in range(first, last + 1):
        s = S[i]
        if not isb(s):
            run.append(s)
            continue
        if run:
            runs.append((len(old), run))
            run = []
        cur.append(s)
        if s["t"] == "poly" and s.get("fill") in USE_ROOF and s.get("fill") == s.get("stroke") or \
                s.get("fill") == CTX[0] and s.get("stroke") == CTX[3]:
            old.append(cur)
            cur = []
    tail = S[last + 1:]
    for b in old:
        roof = b[-1]
        cls = USE_ROOF.get(roof.get("fill"), ("context", CTX))[0]
        hs = [(w["rings"][0][3][1] - w["rings"][0][0][1]) / V.kz for w in b[:-1]
              if w.get("fill") is not None and len(w["rings"][0]) == 4]
        h = max(hs) if hs else None
        R = roof["rings"][0]
        foot = [(q[0], q[1] - V.kz * (h or 0.0)) for q in R]
        gx, gy = sum(q[0] for q in foot) / len(foot), sum(q[1] for q in foot) / len(foot)
        x, y = V.back(gx, gy)
        b[:] = [dict(cls=cls, h=h, foot=foot, bb=(min(q[0] for q in foot), min(q[1] for q in foot),
                                                   max(q[0] for q in foot), max(q[1] for q in foot)),
                     d=V.depth(x, y), n=0)]
    old = [b[0] for b in old]
    grid = {}
    for k_, b in enumerate(old):
        for gi in range(int(b["bb"][0] // 2), int(b["bb"][2] // 2) + 1):
            for gj in range(int(b["bb"][1] // 2), int(b["bb"][3] // 2) + 1):
                grid.setdefault((gi, gj), []).append(k_)

    def match(X, Y):
        for dy in (0.0, 0.25, -0.25, 0.5, -0.5):
            for k_ in grid.get((int(X // 2), int((Y + dy) // 2)), ()):
                b = old[k_]
                if b["bb"][0] <= X <= b["bb"][2] and b["bb"][1] <= Y + dy <= b["bb"][3] and _pip(X, Y + dy, b["foot"]):
                    return k_
        return None

    # ---- MapBase buildings inside site_alan: class + height from the booklet building they stand in
    stor = dict(STOREY)
    new, n_fl, n_bk, n_def, n_new = [], 0, 0, 0, 0
    cnt = {}
    foots = []
    for bi, (row, x_) in enumerate(zip(C["bld"], C["bld_x"])):
        P = [tuple(q) for q in row[0]]
        if len(P) > 1 and P[0] == P[-1]:
            P = P[:-1]
        if len(P) < 3:
            continue
        ar = sum(P[i - 1][0] * P[i][1] - P[i][0] * P[i - 1][1] for i in range(len(P))) / 2.0
        gx = sum(q[0] for q in P) / len(P)
        gy = sum(q[1] for q in P) / len(P)
        if not inside(gx, gy) or abs(ar) < 4.0:
            continue
        if ar < 0:
            P = P[::-1]
        P = _clip(P, H)                                  # v2.8: cut to site_alan, nothing hangs over the slab
        if len(P) < 3:
            continue
        X, Y = V.P(gx, gy)
        k_ = match(X, Y)
        fab = row[1]
        if k_ is not None:
            old[k_]["n"] += 1
            cls = old[k_]["cls"]
        else:
            n_new += 1
            cls = "ruins" if fab == "monument" else "sacred" if fab == "sacred" else "context"
        fl = int(x_[0] or 0)
        if fl > 0:
            h = fl * stor.get(cls, 3.0)
            n_fl += 1
        elif k_ is not None and old[k_]["h"]:
            h = old[k_]["h"]
            n_bk += 1
        else:
            h = 3.0
            n_def += 1
        cnt[cls] = cnt.get(cls, 0) + 1
        cols = dict((u[0], u[1]) for u in USE).get(cls, CTX)
        foots.append(P)
        new.append((V.depth(gx, gy), [dict(sh_, anchor=(gx, gy), bld=bi) for sh_ in
                                      _bld_shapes(V, P, h, cols, cls != "context")]))
    gone = [b for b in old if b["n"] == 0]
    merged = [b for b in old if b["n"] >= 2]
    log.append(u"buildings: %d from MapBase %s in site_alan (booklet had %d): class from the booklet building they "
               u"stand in for %d, %d not in the booklet (class from MapBase: ruins / sacred, else context)" % (
                   len(new), C.get("version"), len(old), len(new) - n_new, n_new))
    log.append(u"buildings: heights from surveyed floors %d (x 3.0 m; civic 3.5, sacred 5.0, industry 4.5), from the "
               u"booklet %d, not recorded (one floor, 3.0 m) %d" % (n_fl, n_bk, n_def))
    log.append(u"buildings: %d booklet buildings stand on no MapBase footprint (dropped), %d booklet blocks held "
               u"2+ MapBase buildings (now drawn one by one)" % (len(gone), len(merged)))
    log.append(u"buildings per class: %s" % u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())))

    # ---- v3.0 (Aras 13:40-13:41 UTC "river drawing in axonometric is fucked fix it according to the basemap", "make
    # axonometric get produced by basemap"): the slab, ground, water, streets, walls, buildings and trees are ALL drawn
    # from the MapBase cache (and the 2023 canopy patches MapBase reads), draped on the terrain; of the booklet drawing
    # only the view (fitted to its slab), the use class each building stands in and the numbered markers stay.
    S_ = ns_["MB_STYLE"]
    WATER, WATER_LINE = S_["water"], S_["water_line"]
    on_edge = lambda p: any(abs(a * p[0] + b * p[1] + c0) < 0.05 for a, b, c0 in H)

    def dens(Q, step=5.0, closed=True):
        D = [] if closed else [Q[0]]
        rng = range(len(Q)) if closed else range(1, len(Q))
        for i in rng:
            p, q = Q[i - 1], Q[i]
            L = m_.hypot(q[0] - p[0], q[1] - p[1])
            n = max(1, int(L / step))
            D += [(p[0] + (q[0] - p[0]) * t / n, p[1] + (q[1] - p[1]) * t / n) for t in range(1, n + 1)]
        return D

    def region(rings_in, fill, edge, w_pt, grp, one=True):
        """closed plan rings cut to site_alan, draped: one fill (even-odd) or one per ring; edges not along the cut"""
        rr = []
        for R in rings_in:
            Q = _clip([tuple(q[:2]) for q in R], H)
            if len(Q) >= 3:
                D = dens(Q)
                rr.append(([V.P(x, y) for x, y in D], D))
        if not rr:
            return [], 0
        mk = lambda rings, a: {"t": "poly", "rings": rings, "fill": fill, "stroke": None, "width_pt": 0.0,
                               "dash_pt": None, "opacity": None, "grp": grp, "anchor": a, "bld": None}
        out = [mk([r[0] for r in rr], rr[0][1][0])] if one else [mk([r[0]], r[1][0]) for r in rr]
        if edge:
            for scr, D in rr:
                cur_ = []
                for i in range(len(D)):
                    p, q = D[i - 1], D[i]
                    if on_edge(p) and on_edge(q):
                        if len(cur_) > 1:
                            out.append({"t": "line", "pts": cur_, "fill": None, "stroke": edge, "width_pt": w_pt,
                                        "dash_pt": None, "opacity": None, "grp": grp, "anchor": D[0], "bld": None})
                        cur_ = []
                        continue
                    if not cur_:
                        cur_ = [scr[i - 1]]
                    cur_.append(scr[i])
                if len(cur_) > 1:
                    out.append({"t": "line", "pts": cur_, "fill": None, "stroke": edge, "width_pt": w_pt,
                                "dash_pt": None, "opacity": None, "grp": grp, "anchor": D[0], "bld": None})
        return out, len(rr)

    # the slab: its top = site_alan draped, its two cut faces toward the viewer (the band is drawn in main)
    E = dens([tuple(q) for q in corners], 15.0)
    slab_top = {"t": "poly", "rings": [[V.P(x, y) for x, y in E]], "fill": SLAB_TOP, "stroke": None, "width_pt": 0.0,
                "dash_pt": None, "opacity": None, "grp": u"slab/mb", "anchor": corners[0], "bld": None}
    sides = []
    for i in range(4):
        p, q = corners[i], corners[(i + 1) % 4]
        L = m_.hypot(q[0] - p[0], q[1] - p[1])
        nx, ny = (q[1] - p[1]) / L, -(q[0] - p[0]) / L
        if (p[0] + q[0]) / 2.0 * nx + (p[1] + q[1]) / 2.0 * ny < cx_ * nx + cy_ * ny:
            nx, ny = -nx, -ny
        vis, lt = V.facing(nx, ny)
        if vis:
            run = [V.P(x, y) for x, y in dens([p, q], 15.0, False)]
            sides.append({"t": "poly", "rings": [run + [(run[-1][0], run[-1][1] - 1.0), (run[0][0], run[0][1] - 1.0)]],
                          "fill": "B0AC9C" if lt else "847E75", "stroke": None, "width_pt": 0.0, "dash_pt": None,
                          "opacity": None, "grp": u"slab/mb", "anchor": p, "bld": None})
    if len(sides) != 2:
        log.append(u"FLAG slab: %d cut faces face the viewer (2 expected)" % len(sides))

    # parks and green ground: MapBase parks + its OSM areas of park / green / wood / cemetery
    pr = list(C["polys"].get("parks", [])) + [a[0] for a in C.get("areas", []) if len(a) > 1 and a[1] in PARK_KINDS]
    parks, n_pk = region(pr, PARK_C, None, 0.0, u"plants/mb", one=False)
    # the water: MapBase's river (the Selinos and its banks, as every base map draws it)
    riv = [[tuple(q[:2]) for q in R] for R in C["polys"].get("river", [])]
    water, n_wr = region(riv, WATER, WATER_LINE, 0.45, u"water/mb")
    rbb = [(min(q[0] for q in R), min(q[1] for q in R), max(q[0] for q in R), max(q[1] for q in R)) for R in riv]
    in_water = lambda x, y: sum(1 for R, b in zip(riv, rbb) if b[0] <= x <= b[2] and b[1] <= y <= b[3] and
                                _pip(x, y, R)) % 2 == 1
    # historic walls: MapBase's heritage walls and city walls, draped, cut to site_alan
    walls, n_wl = [], 0
    for P in [w_[1] for w_ in C["lines"].get("heritage_walls", [])] + list(C.get("osm_citywalls", [])):
        P = [tuple(q[:2]) for q in P]   # lines rows: (closed, points)
        if len(P) < 2:
            continue
        cur_ = []
        for q in dens(P, 2.0, False) + [None]:
            if q is not None and inside(q[0], q[1]):
                cur_.append(V.P(q[0], q[1], 0.3))
                continue
            if len(cur_) > 1:
                walls.append({"t": "line", "pts": cur_, "fill": None, "stroke": WALL_C, "width_pt": 0.6,
                              "dash_pt": (4.5, 2.5), "opacity": None, "grp": u"heritage/mb", "anchor": P[0],
                              "bld": None})
                n_wl += 1
            cur_ = []
    log.append(u"ground: slab from site_alan, %d park / green area(s), river %d ring(s), %d historic wall piece(s), "
               u"all from MapBase %s" % (n_pk, n_wr, n_wl, C.get("version")))

    # ---- trees: the 2023 canopy patches MapBase reads (C["veg"]["trees"]) and its OSM trees; never in the water
    trs = tree_traces(log)
    names = sorted(trs)
    bgrid = {}
    for k_, P in enumerate(foots):
        for gi in range(int(min(q[0] for q in P) // 20), int(max(q[0] for q in P) // 20) + 1):
            for gj in range(int(min(q[1] for q in P) // 20), int(max(q[1] for q in P) // 20) + 1):
                bgrid.setdefault((gi, gj), []).append(k_)
    in_bld = lambda x, y: any(_pip(x, y, foots[k_]) for k_ in bgrid.get((int(x // 20), int(y // 20)), ()))
    pts, n_small, n_wat, n_bl = [], 0, 0, 0
    patches = (C.get("veg") or {}).get("trees", [])
    if not patches:
        log.append(u"FLAG trees: MapBase carries no 2023 canopy patches (Data/veg2023.json): only OSM trees drawn")
    ys_ = TREE_SP * 0.8660254
    for R in patches:
        R = [tuple(q[:2]) for q in R]
        x0, y0 = min(q[0] for q in R), min(q[1] for q in R)
        x1, y1 = max(q[0] for q in R), max(q[1] for q in R)
        if not (inside(x0, y0) or inside(x1, y1) or inside(x0, y1) or inside(x1, y0)):
            continue
        a = abs(sum(R[i - 1][0] * R[i][1] - R[i][0] * R[i - 1][1] for i in range(len(R)))) / 2.0
        if a < TREE_MIN_A:
            n_small += 1
            continue
        got = []
        for j in range(int(y0 // ys_), int(y1 // ys_) + 1):
            off = TREE_SP / 2.0 if j % 2 else 0.0
            for i in range(int((x0 - off) // TREE_SP), int((x1 - off) // TREE_SP) + 1):
                x, y = i * TREE_SP + off, j * ys_
                if x0 <= x <= x1 and y0 <= y <= y1 and _pip(x, y, R):
                    got.append((x, y))
        if not got:
            got = [(sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R))]
        D = 2.0 * (a / len(got) / m_.pi) ** 0.5
        for x, y in got:
            pts.append((x, y, min(TREE_D[1], max(TREE_D[0], D))))
    for q in C.get("trees", []):
        if not any(abs(q[0] - p[0]) < TREE_SP / 2 and abs(q[1] - p[1]) < TREE_SP / 2 for p in pts):
            pts.append((q[0], q[1], 6.0))
    trees = []
    for x, y, D in pts:
        if not inside(x, y):
            continue
        if in_water(x, y):
            n_wat += 1
            continue
        if in_bld(x, y):
            n_bl += 1
            continue
        if names:
            tr = trs[names[(int(x * 7.0) + int(y * 13.0)) % len(names)]]
            trees.append((V.depth(x, y), _tree_shapes(V, x, y, D, tr, (x, y))))
    cnt["_trees"] = len(trees)
    log.append(u"trees: %d drawn (one every %.0f m in the 2023 canopy patches over %.0f m2, crowns %.1f-%.1f m; OSM "
               u"trees where no patch); left out: %d in the river, %d on a building roof, %d patches under %.0f m2" % (
                   len(trees), TREE_SP, TREE_MIN_A, TREE_D[0], TREE_D[1], n_wat, n_bl, n_small, TREE_MIN_A))

    objs = [(d_, sh_) for d_, sh_ in new] + trees
    objs.sort(key=lambda o: -o[0])
    body = [s for o in objs for s in o[1]]

    # ---- the streets: MapBase's one closed street region, cut to site_alan, draped on the terrain
    road, n_rd = region(C["polys"].get("street_net", []), ROAD[0], ROAD[1], ROAD[2], u"roads/mb")
    log.append(u"streets: MapBase's street region (%d ring(s) in site_alan, one fill, edges not drawn along the frame "
               u"cut)" % n_rd)
    labels = [dict(s, anchor=None, bld=None) for s in S if (s.get("grp") or u"").startswith(u"labels")]
    nold = len(S) - len(labels)
    log.append(u"booklet drawing: %d shapes left out (its slab, ground, water, trees, people, roads, buildings); its %d "
               u"numbered marker shape(s) kept" % (nold, len(labels)))
    S2 = sides + [slab_top] + parks + road + water + walls + body + labels   # water over the streets (mb_draw order)
    return dict(c, shapes=S2, view=V), cnt


def _hatch(rings, step, ang):
    """v3.0: even-odd hatch segments (page mm) of rings at ang degrees every step mm"""
    import math as m_
    a = m_.radians(ang)
    dv, nv = (m_.cos(a), m_.sin(a)), (-m_.sin(a), m_.cos(a))
    E = [(R[i - 1], R[i]) for R in rings for i in range(len(R))]
    ts = [q[0] * nv[0] + q[1] * nv[1] for R in rings for q in R]
    if not ts:
        return []
    out = []
    t = (int(min(ts) / step) + 1) * step
    while t < max(ts):
        xs = []
        for p, q in E:
            fp, fq = p[0] * nv[0] + p[1] * nv[1] - t, q[0] * nv[0] + q[1] * nv[1] - t
            if (fp < 0) != (fq < 0):
                r = fp / (fp - fq)
                xs.append((p[0] + (q[0] - p[0]) * r, p[1] + (q[1] - p[1]) * r))
        xs.sort(key=lambda z: z[0] * dv[0] + z[1] * dv[1])
        out += [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]
        t += step
    return out


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    K = G["pc_data"](log)["key"]
    MB = G["pc_mb_lib"](log)
    mix = MB["mixh"]
    page = tuple(globals().get("page_mm") or A3)
    c = clean_list(p03(log), lib["text_w"], log)    # v2.3: the numbered list cleaned (Aras 04:58 UTC)
    c, bcnt = rebuild(c, G, log)                      # v2.5: roads and buildings from MapBase (Aras 10:34 UTC)

    # ---- the colours: each old shade -> the palette colour darkened by the booklet's own step (luminance ratio)
    lum = lambda h: 0.2126 * int(h[0:2], 16) + 0.7152 * int(h[2:4], 16) + 0.0722 * int(h[4:6], 16) + 1.0
    RE = {}
    for nm, old, (tab, key) in USE:
        new = MB[tab][key]
        for sh in old:
            RE[sh] = new if sh == old[0] else mix(new, "000000", max(0.0, 1.0 - lum(sh) / lum(old[0])))
        log.append(u"colours: %s %s -> %s %s (%s)" % (nm, old[0], tab, key, new))
    rc = lambda h: RE.get(h, h) if h else h

    # ---- the legend rows (the booklet's, recoloured) and the page layout: legend columns under the drawing
    P_, L_, circle = G["P_"], G["L_"], G["circle"]
    rows = []
    leg = list(c["legend"])
    if bcnt is not None:                                 # v2.5: the building rows recounted, context row added
        out_ = []
        for sw, txt in leg:
            cl_ = next((v for k_, v in LEGEND_CLS if txt.startswith(k_)), None)
            if cl_ is not None:
                if not bcnt.get(cl_):
                    continue
                txt = re.sub(r"\(\d[\d,]*\)\s*$", u"(%d)" % bcnt[cl_], txt)
            out_.append((sw, txt))
        if bcnt.get("context"):
            k_ = max([i_ for i_, (sw, txt) in enumerate(out_) if any(txt.startswith(k__) for k__, v in LEGEND_CLS)]
                     or [-1]) + 1
            out_.insert(k_, ({"kind": "fill", "colour": CTX[0], "edge": CTX[3]},
                             u"Other buildings, use not recorded (%d)" % bcnt["context"]))
        leg = out_
        out_ = []                                        # v3.0: water, trees from MapBase
        for sw, txt in leg:
            if txt.startswith(u"Trees: Stone pine"):
                continue
            if txt.startswith(u"Trees"):
                sw, txt = dict(sw, colour=TREE_KEY), u"Trees (%d)" % bcnt.get("_trees", 0)
            elif txt.startswith(u"Stream channel"):
                sw = dict(sw, colour=MB["MB_STYLE"]["water"])
            out_.append((sw, txt))
        leg = out_
    for sw, txt in leg:
        col = rc(sw.get("colour"))
        if sw.get("kind") == "dash":
            rows.append((lambda x, y, col=col: [L_([(x - 4.5, y), (x + 4.5, y)], col, 0.25, "legend", (1.6, 0.9))],
                         txt))
        elif sw.get("kind") == "dot":
            rows.append((lambda x, y, col=col: [P_([circle(x, y, 1.2, 16)], col, None, 0.0, "legend")], txt))
        else:
            rows.append((lambda x, y, col=col, ed=sw.get("edge"): [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0),
                                                                        (x + 4.5, y + 2.0), (x - 4.5, y + 2.0)]],
                                                                      col, ed, 0.15 if ed else 0.0, "legend")], txt))
    # ---- v2.4: the numbered list out of the drawing, into the legend; the drawing's box = the drawing itself
    X0, Y0 = 314.0, 120.0
    inl = lambda t: t["anchor"]["pt"][0] >= X0 and t["anchor"]["pt"][1] >= Y0
    num = lambda t: t["string"].strip().isdigit()
    lt = [t for t in c["texts"] if inl(t)]
    badge_fill = {}
    keep = []
    for sh in c["shapes"]:
        pts = [q for R in sh.get("rings", []) for q in R] or sh.get("pts", [])
        if (sh.get("grp") or u"").startswith(u"labels") and pts and min(q[0] for q in pts) >= X0 - 2.0 and \
                min(q[1] for q in pts) >= Y0:
            badge_fill[round(sum(q[1] for q in pts) / len(pts), 0)] = rc(sh.get("fill"))
            continue
        keep.append(sh)
    if lt:
        lrows = [(None, u"NUMBERED ON THE DRAWING")]
        for b in sorted([t for t in lt if num(t)], key=lambda t: int(t["string"])):
            y = b["anchor"]["pt"][1]
            words = sorted([t for t in lt if not num(t) and abs(t["anchor"]["pt"][1] - y) < 1.0],
                           key=lambda t: t["anchor"]["pt"][0])
            label = u" ".join(t["string"] for t in words)
            fill = badge_fill[min(badge_fill, key=lambda yy: abs(yy - y))] if badge_fill else "4A3F35"
            lrows.append((lambda x, y, n=b["string"], f_=fill: [P_([circle(x, y, 2.0, 32)], f_, "FFFFFF", 0.2,
                                                                     "legend"),
                                                                  G["T_"](n, x, y - 0.8, 2.2, "FFFFFF", "legend",
                                                                          True, "C")], label))
        rows = lrows + rows
        c = dict(c, shapes=keep, texts=[t for t in c["texts"] if not inl(t)])
        P = [q for sh in c["shapes"] for q in ([q for R in sh.get("rings", []) for q in R] or sh.get("pts", []))]
        P += [tuple(t["anchor"]["pt"]) for t in c["texts"]]
        ext = (max(c["extent"][0], min(q[0] for q in P) - 1.0), max(c["extent"][1], min(q[1] for q in P) - 1.0),
               min(c["extent"][2], max(q[0] for q in P) + 1.0), min(c["extent"][3], max(q[1] for q in P) + 1.0))
        log.append(u"list: %d rows moved into the legend; drawing box %.0f x %.0f mm (was %.0f x %.0f)" % (
            len(lrows) - 1, ext[2] - ext[0], ext[3] - ext[1], c["extent"][2] - c["extent"][0],
            c["extent"][3] - c["extent"][1]))
        c = dict(c, extent=ext)
    title, sub = u"Heights, heritage, water, green", u""      # v2.1: not Plan 01's "What is there" again
    W0, H0 = c["extent"][2] - c["extent"][0], c["extent"][3] - c["extent"][1]
    dry = Sheet((0.0, -5000.0, 0.0, 0.0), 0.0, 0.0)
    ncol, need = 1, 0.0
    for n_ in (4, 3, 2, 1):
        if n_ * G["PC_SIDE_MM"] + (n_ - 1) * 6.0 <= page[0] - 24.0:
            ys = [it[3] for it in G["pc_sheet"](dry, K, lib, title, sub, rows, [], u"", cols=n_)
                  if it[0] == "text" and it[8] in ("title", "legend")]
            ncol, need = n_, -min(ys) + 3.0
            break
    sd = min((page[0] - 24.0) / W0, (page[1] - 24.0 - need - 6.0) / H0)
    ox = (page[0] - W0 * sd) / 2.0 - c["extent"][0] * sd
    oy = page[1] - 12.0 - need - 6.0 - c["extent"][3] * sd   # v2.2: right under the legend
    T = lambda q: (ox + q[0] * sd, oy + q[1] * sd)
    box = (ox + c["extent"][0] * sd, oy + c["extent"][1] * sd, ox + c["extent"][2] * sd, oy + c["extent"][3] * sd)
    log.append(u"layout: page %.0f x %.0f mm, drawing %.0f x %.0f mm at %.2f of the booklet's, legend %d column(s)"
               % (page[0], page[1], W0 * sd, H0 * sd, sd, ncol))

    # ---- the drawing: every shape as exported, in its order, recoloured; see-through fills mixed onto the ground
    items, n_re = [], 0
    for i_s, s in enumerate(c["shapes"]):
        if i_s < 2 and s["t"] == "poly" and s.get("fill") in ("B0AC9C", "847E75") and len(s["rings"][0]) > 3:
            run = [T(q) for q in s["rings"][0][:-2]]      # v2.9: the cut face = a constant band under the edge
            low = [(q[0], q[1] - SLAB_MM) for q in run]
            items.append(("poly", [run + low[::-1]], rc(s["fill"]), None, 0.0, None, u"axo_slab", 1, None, None))
            P0, P1 = run[0], run[-1]
            Ln = ((P1[0] - P0[0]) ** 2 + (P1[1] - P0[1]) ** 2) ** 0.5
            for j in range(1, int(Ln / 0.9)):            # soil hatching, as slide 2's axo tiles (B08)
                t_ = j * 0.9 / Ln
                k_ = min(len(run) - 1, int(t_ * (len(run) - 1)))
                q = (P0[0] + (P1[0] - P0[0]) * t_, run[k_][1] + (run[min(k_ + 1, len(run) - 1)][1] - run[k_][1]) *
                     (t_ * (len(run) - 1) - k_))
                items.append(("line", [(q[0], q[1] - 0.15), (q[0] - 0.9, q[1] - SLAB_MM + 0.15)], "8E877C", 0.06,
                              None, u"axo_slab", 1))
            items.append(("line", low, "6E675E", 0.3, None, u"axo_slab", 1))
            continue
        lay = u"axo_" + (s.get("grp") or u"other/0").split(u"/")[0]
        lw = (s.get("width_pt") or 0.0) * PT * sd
        st = rc(s.get("stroke"))
        if s["t"] == "line":
            ds = s.get("dash_pt")
            items.append(("line", [T(q) for q in s["pts"]], st, lw, None, lay,
                          tuple(v * PT * sd for v in ds) if ds else 1))
            continue
        fi = rc(s.get("fill"))
        n_re += fi != s.get("fill") or st != s.get("stroke")
        op = s.get("opacity")
        if fi and op is not None and op < 1.0:
            fi = mix(fi, GROUND, 1.0 - op)
        items.append(("poly", [[T(q) for q in R] for R in s["rings"]], fi, st, lw, None, lay, 1, None, None))
        if s.get("grp") == u"water/mb" and MB["MB_STYLE"].get("water_hatch"):   # v3.0: the base map's water hatch
            hs, ha, hc, hw = MB["MB_STYLE"]["water_hatch"]
            for a_, b_ in _hatch([[T(q) for q in R] for R in s["rings"]], hs, ha):
                items.append(("line", [a_, b_], hc, hw, None, u"axo_water_hatch", 1))
    model = [dict((k_, v) for k_, v in s.items() if k_ != "opacity") for s in c["shapes"]]
    for s in model:                                      # v3.0: slide 2's node axos cut from this (spine thread)
        s["fill"], s["stroke"] = rc(s.get("fill")), rc(s.get("stroke"))
    V = c.get("view")
    try:
        mp = os.path.join(os.path.dirname(CACHE), "axo_model.json")
        with open(mp, "w", encoding="utf-8") as f:
            json.dump({"version": VERSION, "units": u"drawing mm (y up); page mm = (ox + x * sd, oy + y * sd)",
                       "view": dict(c0=V.c0, c1=V.c1, c2=V.c2, oy=V.oy, s=V.s, k=V.k, kz=V.kz, phi=PHI, z0=V.z0)
                       if V else None, "page": dict(ox=ox, oy=oy, sd=sd, w=page[0], h=page[1]),
                       "shapes": model}, f, ensure_ascii=False)
        log.append(u"model: %d shapes + view written to %s (slide 2 node axos)" % (len(model), mp))
    except Exception as ex:
        log.append(u"FLAG model: %s not written (%s: %s)" % (mp, type(ex).__name__, ex))
    for t in c["texts"]:
        x, y = T(t["anchor"]["pt"])
        al = (t.get("positions") or [u"=L"])[0].replace(u"=", u"")
        items.append(("text", t["string"], x, y, t["size_pt"] * PT * sd, rc(t.get("colour") or "4A3F35"),
                      bool(t.get("bold")), al if al in (u"L", u"C", u"R") else u"L", u"axo_labels", None, None))
    log.append(u"drawing: %d shapes (%d recoloured), %d words, legend %d rows; booklet run %s (%s)" % (
        len(c["shapes"]), n_re, len(c["texts"]), len(rows), c.get("run"), c.get("version")))
    M = Sheet(box, page[0], page[1])
    Mc = Sheet((0.0, box[3] + 6.0, 4.0, page[1] - 12.0), page[0], page[1])
    items += [it for it in G["pc_sheet"](Mc, K, lib, title, sub, rows, [], u"", cols=ncol)
              if it[8 if it[0] == "text" else 6 if it[0] == "poly" else 5] not in ("north_scale", "frame")]
    G["pc_write"](lib, M, items, OUT_DIR, NAME, u"What is there, axonometric", log)
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
