# -*- coding: utf-8 -*-
"""Bergama Group 6: BASEMAP v1 (12 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.
Aras 12 Nov 2026 10:53 UTC: "we need a fresh basemap and keymap style. For basemap every road should be outlined as well
as the buildings and all should be outlined aswell. Heritage buildings should be marked. Our site_alan should be our
frame for that basemap and keymap for that matter".

ONE read of the open survey model (Bergama_Altlik.3dm), cut at site_alan, turned so the frame's long side lies flat
(its eastern end to the right, as his plan), kept by layer in a cache that the other new scripts copy from:
  Basemap.pdf   outline drawing at 1:scale: every building, road edge, kerb, bridge, stream bank, pond, park, wall and
                shed as its own outline; heritage buildings marked (filled in the palette red, heavier outline);
                frame = site_alan, north arrow, scale bar, legend of what is drawn
  Keymap.pdf    the key map style at 1:keymap_scale: buildings as light solid blocks, heritage solid red, road edges
                faint, stream banks blue, the frame; section lines of the model layer "section_lines" with their names
  heritage      a building is heritage when it is on BINA_TARIHI / BINA_HARABE, or a survey name text (YAZI_YAPI) with a
                heritage or sacred word (HERITAGE_WORDS, the site board's list) stands inside it; walls on
                SINIR_TARIHI_SUR are drawn in the heritage colour. Nothing else decides it; the log lists them by name.
Aras 10:54 UTC: "we need to see our calisma_alan, and inside calisma_alan it'll be colourful just as the published svg
and outside it should be black and white".
  Basemap.pdf / Keymap.pdf are black and white (heritage = dark grey fill, black outline); calisma_alan is outlined.
  Basemap_colour.svg = his plan SVG (Data/assets/masterlastversion.svg, unchanged, nothing redrawn) shown only inside
                calisma_alan (a clip path) and outside the plan frame (his legend and texts), over the black and white
                survey outlines, which therefore show everywhere else in the frame. Placed by the plan frame = site_alan
                (the frame-size clip rectangle of his Selinos group). Groups: existing_basemap_bw/<layer>,
                plan_inside_calisma_alan, calisma_alan_outline. Open it in Illustrator.
Line weights and the grey tones are drawing values (ours).

Component: Rhino 8 > Grasshopper > Python 3 Script (the board builder places it from the cloud kit).
  input  run            Button (or the previous script's done text)
  input  scale          sheet scale 1:n of Basemap.pdf (default 2000)
  input  keymap_scale   sheet scale 1:n of Keymap.pdf (default 10000)
  output log / done     as every Bergama script
Reads  the open Rhino model's survey layers (once; the same model = the cache is used, nothing read again)
       ~/Downloads/Bergama/Data/assets/masterlastversion.svg (his plan, for Basemap_colour.svg)
Writes ~/Downloads/Bergama/output/bergama_basemap/Basemap.pdf, Keymap.pdf   (PDF layers existing_<thing>)
       ~/Downloads/Bergama/output/bergama_basemap/Basemap_colour.svg
       ~/Downloads/Bergama/cached/bergama_basemap/basemap_layers.json   every layer in survey m, the frame, the turn
       ~/Downloads/Bergama/logs/bergama_basemap_log.txt
"""
import os, time, json, math, re

# ---- SETTINGS ----
VERSION = "v1"
GH_LABEL = "Basemap"
OUT_FOLDER = "bergama_basemap"
LOG_NAME = "bergama_basemap_log.txt"
GH_INPUTS = {"scale": "int 500..10000 = 2000", "keymap_scale": "int 2000..50000 = 10000"}

FRAME_LAYER = "site_alan"
FRAME_COPY = [(29388.015, 32540.503), (31220.325, 30364.153), (31625.069, 30704.915), (29792.759, 32881.264)]
SECTION_LAYER = "section_lines"
WORK_LAYER = "calisma_alan"
PLAN_SVG = os.path.join("Data", "assets", "masterlastversion.svg")
BLD_LAYERS = ["BINA_MESKEN", "BINA", "BINA_RESMI", "BINA_OKUL", "BINA_DINI_TESIS", "BINA_DINITESIS", "BINA_TARIHI",
              "BINA_HARABE", "BINA_FABRIKA", "BINA_SERA", "BINA_SPOR_TESISLERI", "BINA_AKARYAKIT", "BINA_INS_HALINDE"]
HER_LAYERS = ("BINA_TARIHI", "BINA_HARABE")
NAME_LAYER = "YAZI_YAPI"
HERITAGE_WORDS = ("tarihi", "harabe", "harap", "kalıntı", "kalinti", "hamam", " han ", "bedesten", "arasta", "türbe",
                  "turbe", "medrese", "kızıl avlu", "kizil avlu", "tapınağı", "tapinagi", "kilise", "sinagog", "çeşme",
                  "cesme", "sebil", "kervansaray", "müze", "muze", "cami", "mescit", "mescid", "cemevi", "tekke", "zaviye")
# cache layer -> (survey layers, closed shapes?)
SURVEY = [
    ("sheds", ["BINA_SUNDURMA"]),
    ("road_edges", ["YOL_SOSE", "YOL_TOPRAK"]),
    ("kerbs", ["YOL_BORDUR"]),
    ("bridges", ["YOL_KOPRU"]),
    ("stream_banks", ["HIDRO_DERE_SULU", "HIDRO_DERE_KURU"]),
    ("ponds", ["HIDRO_HAVUZ", "HIDRO_GOL"]),
    ("parks", ["ORMAN_PARK_BAHCE"]),
    ("walls", ["SINIR_DUVAR", "SINIR_HARAP_DUVAR"]),
    ("heritage_walls", ["SINIR_TARIHI_SUR"]),
]
INK, GREY, PALE = "1A1A1A", "6F6C67", "B5B2AC"
HER, WATER, PARK = "1A1A1A", "4A4A4A", "8A8A8A"      # black and white outside calisma_alan
HER_FILL = "8F8F8F"
# Basemap.pdf: cache layer -> (PDF layer, stroke, line width mm, fill, alpha)
STYLE = [
    ("parks", "existing_parks", PARK, 0.10, None),
    ("ponds", "existing_water", WATER, 0.18, None),
    ("stream_banks", "existing_water", WATER, 0.22, None),
    ("road_edges", "existing_roads", GREY, 0.15, None),
    ("kerbs", "existing_roads", GREY, 0.08, None),
    ("bridges", "existing_bridges", INK, 0.22, None),
    ("walls", "existing_walls", GREY, 0.08, None),
    ("heritage_walls", "existing_heritage", HER, 0.25, None),
    ("sheds", "existing_buildings", GREY, 0.08, None),
    ("buildings", "existing_buildings", INK, 0.13, "FFFFFF"),
    ("heritage", "existing_heritage", HER, 0.30, HER_FILL),
]
KEY_STYLE = [
    ("road_edges", "existing_roads", PALE, 0.05, None),
    ("stream_banks", "existing_water", WATER, 0.25, None),
    ("ponds", "existing_water", WATER, 0.15, None),
    ("bridges", "existing_bridges", GREY, 0.15, None),
    ("buildings", "existing_buildings", None, 0.0, "D9D6CF"),
    ("heritage", "existing_heritage", None, 0.0, "3A3A3A"),
]
# Basemap_colour.svg: stroke widths in metres on the ground (the SVG has no sheet scale)
SVG_W = {"parks": 0.2, "ponds": 0.3, "stream_banks": 0.4, "road_edges": 0.3, "kerbs": 0.15, "bridges": 0.4, "walls": 0.15,
         "heritage_walls": 0.5, "sheds": 0.15, "buildings": 0.25, "heritage": 0.5}
LEGEND = [("buildings", u"Building"), ("heritage", u"Heritage building"), ("road_edges", u"Road edge"),
          ("kerbs", u"Kerb"), ("bridges", u"Bridge"), ("stream_banks", u"Stream bank"), ("parks", u"Park"),
          ("walls", u"Wall")]

# ---- folders (same in every script) ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
CACHE_FILE = os.path.join(CACHE_DIR, "basemap_layers.json")
CACHE_FORMAT = 2


# ================================================================ the open Rhino model
def _layer_objs(doc, name):
    idx = doc.Layers.FindByFullPath(name, -1)
    if idx < 0:
        for lay in doc.Layers:
            if not lay.IsDeleted and lay.Name == name:
                idx = lay.Index
                break
    if idx < 0:
        return []
    return list(doc.Objects.FindByLayer(doc.Layers[idx]) or [])


def _curve_pts(g):
    """(closed?, [(x, y)]) of a curve: its own corners when it is a polyline, else a point every metre"""
    try:
        ok, pl = g.TryGetPolyline()
        if ok:
            P = [(p.X, p.Y) for p in pl]
            cl = bool(g.IsClosed)
            if cl and len(P) > 1 and math.hypot(P[0][0] - P[-1][0], P[0][1] - P[-1][1]) < 1e-6:
                P = P[:-1]
            return cl, P
    except Exception:
        pass
    try:
        ts = g.DivideByLength(1.0, True) or []
        P = [(g.PointAt(t).X, g.PointAt(t).Y) for t in ts]
        cl = bool(g.IsClosed)
        if not cl and P:
            P.append((g.PointAtEnd.X, g.PointAtEnd.Y))
        return cl, P
    except Exception:
        return False, []


def model_key(doc):
    try:
        p = doc.Path or ""
        st = os.stat(p) if p and os.path.isfile(p) else None
        return u"%d|%s|%s|%s|%d" % (CACHE_FORMAT, VERSION, p, (u"%d|%d" % (st.st_size, st.st_mtime_ns)) if st else u"unsaved",
                                    doc.Objects.Count)
    except Exception:
        return None


def read_model(doc, log):
    """every layer as [[closed, [(x, y)]]] in survey m, uncut; names = [(text, x, y)]"""
    import Rhino
    rg = Rhino.Geometry
    out, cnt = {}, {}

    def curves(names):
        L = []
        for nm in names:
            for o in _layer_objs(doc, nm):
                g = o.Geometry
                if isinstance(g, rg.Curve):
                    cl, P = _curve_pts(g)
                    if len(P) >= 2:
                        L.append((nm, o, cl, P))
        return L
    fr = [P for _, _, cl, P in curves([FRAME_LAYER]) if len(P) >= 4]
    if fr:
        frame = max(fr, key=lambda P: abs(g_area(P)))[:4]
    else:
        frame = list(FRAME_COPY)
        log.append(u"FLAG frame: no closed curve on layer %s in the open model: the built-in copy of site_alan used"
                   % FRAME_LAYER)
    work = [P for _, _, cl, P in curves([WORK_LAYER]) if len(P) >= 3]
    if not work:
        log.append(u"FLAG calisma_alan: no curve on layer %s in the open model: no working-area outline, and "
                   u"Basemap_colour.svg is not written" % WORK_LAYER)
    names = []
    for o in _layer_objs(doc, NAME_LAYER):
        g = o.Geometry
        try:
            if isinstance(g, rg.TextEntity):
                names.append((g.PlainText.strip(), g.Plane.Origin.X, g.Plane.Origin.Y))
            elif isinstance(g, rg.TextDot):
                names.append((g.Text.strip(), g.Point.X, g.Point.Y))
        except Exception:
            pass
    bld, her = [], []
    for nm, o, cl, P in curves(BLD_LAYERS):
        if len(P) < 3:
            continue
        inside = [t for t, x, y in names if g_pip(x, y, P)]
        word = next((t for t in inside if any(w in u" %s " % t.lower() for w in HERITAGE_WORDS)), None)
        if nm in HER_LAYERS or word:
            her.append({"ring": P, "layer": nm, "name": word or (inside[0] if inside else u"")})
        else:
            bld.append([True, P])
    out["buildings"] = bld
    out["heritage"] = [[True, h["ring"]] for h in her]
    cnt["buildings"], cnt["heritage"] = len(bld), len(her)
    for key, layers in SURVEY:
        out[key] = [[cl, P] for _, _, cl, P in curves(layers)]
        cnt[key] = len(out[key])
    sec = []
    for i, (_, o, cl, P) in enumerate(curves([SECTION_LAYER])):
        nm = u""
        try:
            nm = (o.Attributes.Name or u"").strip()
        except Exception:
            pass
        sec.append({"name": nm or u"L%d" % (i + 1), "line": [P[0], P[-1]]})
    log.append(u"model read: " + u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())) +
               u"; name texts %d; section lines %d" % (len(names), len(sec)))
    for h in her:
        c = (sum(p[0] for p in h["ring"]) / len(h["ring"]), sum(p[1] for p in h["ring"]) / len(h["ring"]))
        log.append(u"  heritage: %s (%s) at %.0f, %.0f" % (h["name"] or u"no name text inside", h["layer"], c[0], c[1]))
    return {"frame": frame, "layers": out, "sections": sec, "calisma": work,
            "heritage_names": [[h["name"], h["layer"]] for h in her]}


# ================================================================ plane geometry
def g_area(P):
    return 0.5 * sum(P[k - 1][0] * P[k][1] - P[k][0] * P[k - 1][1] for k in range(len(P)))


def g_pip(x, y, P):
    ins, n = False, len(P)
    for i in range(n):
        a, b = P[i - 1], P[i]
        if (a[1] > y) != (b[1] > y) and x < a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]):
            ins = not ins
    return ins


def clip_ring(P, box):
    """Sutherland-Hodgman: a closed ring cut at box (x0, y0, x1, y1)"""
    x0, y0, x1, y1 = box
    for axis, lim, keep_ge in ((0, x0, True), (0, x1, False), (1, y0, True), (1, y1, False)):
        Q = []
        n = len(P)
        for i in range(n):
            a, b = P[i - 1], P[i]
            ia = (a[axis] >= lim) if keep_ge else (a[axis] <= lim)
            ib = (b[axis] >= lim) if keep_ge else (b[axis] <= lim)
            if ia != ib:
                t = (lim - a[axis]) / (b[axis] - a[axis])
                Q.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t))
            if ib:
                Q.append(b)
        P = Q
        if len(P) < 3:
            return []
    return P


def clip_line(P, box):
    """an open polyline cut at box: the runs inside"""
    x0, y0, x1, y1 = box
    runs, cur = [], []
    for a, b in zip(P[:-1], P[1:]):
        t0, t1 = 0.0, 1.0
        dx, dy = b[0] - a[0], b[1] - a[1]
        ok = True
        for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if abs(p) < 1e-12:
                if q < 0:
                    ok = False
                    break
            else:
                t = q / p
                if p < 0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
        if not ok or t0 > t1:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        pa = (a[0] + dx * t0, a[1] + dy * t0)
        pb = (a[0] + dx * t1, a[1] + dy * t1)
        if not cur or math.hypot(cur[-1][0] - pa[0], cur[-1][1] - pa[1]) > 1e-6:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [pa]
        cur.append(pb)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


class Frame(object):
    """site_alan turned flat: survey (x, y) -> local (u, v) m, u along the long side with its eastern end right"""

    def __init__(self, corners):
        best = None
        for a, b in zip(corners, corners[1:] + corners[:1]):
            L = math.hypot(b[0] - a[0], b[1] - a[1])
            if best is None or L > best[0]:
                best = (L, b[0] - a[0], b[1] - a[1])
        _, vx, vy = best
        if vx < 0:
            vx, vy = -vx, -vy
        self.rot = -math.atan2(vy, vx)
        self.ca, self.sa = math.cos(self.rot), math.sin(self.rot)
        T = [self.raw(p) for p in corners]
        self.u0, self.v0 = min(p[0] for p in T), min(p[1] for p in T)
        self.w = max(p[0] for p in T) - self.u0
        self.h = max(p[1] for p in T) - self.v0

    def raw(self, p):
        return (self.ca * p[0] - self.sa * p[1], self.sa * p[0] + self.ca * p[1])

    def local(self, p):
        q = self.raw(p)
        return (q[0] - self.u0, q[1] - self.v0)

    def north(self):
        """the page direction of survey north (0, 1)"""
        return (-self.sa, self.ca)


# ================================================================ drawing (items: the Sections page format)
def draw(D, F, den, styles, x0, y0, sections=False):
    """items of the map at 1:den, the frame's lower-left corner at page (x0, y0) mm"""
    k = 1000.0 / den
    box = (0.0, 0.0, F.w, F.h)
    items, cnt = [], {}

    def pg(p):
        return (x0 + p[0] * k, y0 + p[1] * k)
    for key, layer, stroke, lw, fill in styles:
        n = 0
        for cl, P in D["layers"].get(key, []):
            Q = [F.local(p) for p in P]
            if min(q[0] for q in Q) > F.w or max(q[0] for q in Q) < 0 or min(q[1] for q in Q) > F.h or max(q[1] for q in Q) < 0:
                continue
            if cl and len(Q) >= 3:
                R = clip_ring(Q, box)
                if len(R) >= 3:
                    items.append(("poly", [[pg(q) for q in R]], fill, stroke, lw, None, layer, 1, None, None))
                    n += 1
            else:
                for run in clip_line(Q, box):
                    items.append(("line", [pg(q) for q in run], stroke or PALE, lw or 0.05, None, layer, 1))
                    n += 1
        cnt[key] = n
    fr = [pg(q) for q in ((0, 0), (F.w, 0), (F.w, F.h), (0, F.h))]
    items.append(("poly", [fr], None, INK, 0.3, None, "frame", 0, None, None))
    for P in D.get("calisma", []):                         # the working area, a heavy line
        R = [pg(F.local(p)) for p in P]
        items.append(("line", R + R[:1], INK, 0.45, None, "calisma_alan", 1))
    if sections:
        for s in D.get("sections", []):
            a, b = F.local(s["line"][0]), F.local(s["line"][1])
            for run in clip_line([a, b], box):
                items.append(("line", [pg(q) for q in run], INK, 0.35, None, "section_lines", 1))
                for q, al in ((run[0], "R"), (run[-1], "L")):
                    X, Y = pg(q)
                    items.append(("text", s["name"], X + (-1.0 if al == "R" else 1.0), Y + 0.8, 2.2, INK, True, al,
                                  "section_lines", None, None))
    return items, cnt


def furniture(F, den, x0, y0, title, legend):
    """title, scale bar, north arrow and legend under the frame"""
    k = 1000.0 / den
    it = []
    y = y0 - 8.0
    it.append(("text", title, x0, y, 4.0, INK, True, "L", "title", None, None))
    it.append(("text", u"1:%s" % format(den, ",d"), x0, y - 5.0, 3.0, INK, False, "L", "title", None, None))
    bar = 100.0 if den <= 2500 else 500.0
    xb, yb = x0 + 40.0, y - 4.2
    it.append(("line", [(xb, yb), (xb + bar * k, yb)], INK, 0.3, None, "title", 0))
    for i in (0.0, 0.5, 1.0):
        it.append(("line", [(xb + bar * k * i, yb), (xb + bar * k * i, yb + 1.4)], INK, 0.2, None, "title", 0))
    it.append(("text", u"0", xb, yb - 3.2, 2.2, INK, False, "C", "title", None, None))
    it.append(("text", u"%d m" % bar, xb + bar * k, yb - 3.2, 2.2, INK, False, "C", "title", None, None))
    nx, ny = F.north()
    cx, cy = xb + bar * k + 22.0, y - 3.0
    tip, tail = (cx + nx * 7.0, cy + ny * 7.0), (cx - nx * 5.0, cy - ny * 5.0)
    it.append(("line", [tail, tip], INK, 0.3, None, "title", 0))
    it.append(("poly", [[tip, (tip[0] - nx * 3.0 - ny * 1.4, tip[1] - ny * 3.0 + nx * 1.4),
                         (tip[0] - nx * 3.0 + ny * 1.4, tip[1] - ny * 3.0 - nx * 1.4)]], INK, None, 0.1, None, "title",
               1, None, None))
    it.append(("text", u"N", tip[0] + nx * 2.2 - 0.8, tip[1] + ny * 2.2 - 0.8, 2.6, INK, True, "L", "title", None, None))
    x = cx + 20.0
    for key, layer, stroke, lw, fill, lab in legend:
        if fill or key in ("buildings", "heritage", "parks"):
            it.append(("poly", [[(x, y - 4.6), (x + 6.0, y - 4.6), (x + 6.0, y - 1.4), (x, y - 1.4)]], fill, stroke, lw,
                       None, "legend", 1, None, None))
        else:
            it.append(("line", [(x, y - 3.0), (x + 6.0, y - 3.0)], stroke, lw, None, "legend", 1))
        it.append(("text", lab, x + 7.5, y - 3.8, 2.4, INK, False, "L", "legend", None, None))
        x += 7.5 + 0.5 * 2.4 * len(lab) + 7.0
    return it


# ================================================================ PDF (vector, layers as PDF layers)
PT = 25.4 / 72.0
_TR = {u"Ğ": 129, u"ğ": 141, u"İ": 143, u"ı": 144, u"Ş": 157, u"ş": 158, u"–": 150, u"—": 151, u"’": 146}
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
_HELV = {" ": 278, "1": 556, ":": 278, ",": 278, ".": 278, "i": 222, "l": 222, "t": 278, "f": 278, "r": 333, "m": 833,
         "w": 722, "M": 833, "W": 944, "I": 278, "j": 222}


def text_w(s, size, bold=False):
    """mm: Helvetica widths for the narrow and wide letters, 556/1000 em for the rest (labels are short)"""
    return sum(_HELV.get(ch, 667 if ch.isupper() else 556) for ch in s) / 1000.0 * size * (1.05 if bold else 1.0)


def _pdf_txt(s):
    out = bytearray()
    for ch in s:
        c = _TR.get(ch)
        if c is None:
            o = ord(ch)
            c = o if (32 <= o < 127 or 160 <= o < 256) else 63
        if c in (40, 41, 92):
            out += b"\\"
        out.append(c)
    return bytes(out)


def _col(h):
    h = (h or "000000").lstrip("#")
    return "%.3f %.3f %.3f" % (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)


def _f(v):
    return ("%.3f" % v).rstrip("0").rstrip(".")


def write_pdf(path, w, h, items, title):
    """one page w x h mm; items in page mm, y up; each item's layer becomes a PDF layer"""
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)

    def lay(it):
        t = it[0]
        return it[6] if t == "poly" else it[5] if t == "line" else it[8]
    layers = []
    for it in items:
        if lay(it) not in layers:
            layers.append(lay(it))
    ocg = dict((ly, add(("<< /Type /OCG /Name (%s) >>" % _pdf_txt(ly).decode("latin-1")).encode("latin-1")))
               for ly in layers)
    f_r = add(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding << /Type /Encoding /BaseEncoding "
               "/WinAnsiEncoding %s >> >>" % _DIFF).encode())
    f_b = add(("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding << /Type /Encoding /BaseEncoding "
               "/WinAnsiEncoding %s >> >>" % _DIFF).encode())
    k = 72.0 / 25.4
    body = bytearray(("%s 0 0 %s 0 0 cm\n1 J 1 j\n" % (_f(k), _f(k))).encode())
    for ly in layers:                                    # one marked block per layer, in first-use order
        body += ("/OC /oc%d BDC\n" % ocg[ly]).encode()
        for it in items:
            if lay(it) != ly:
                continue
            t = it[0]
            if t == "poly":
                rings, fill, stroke, lw = it[1:5]
                if not fill and not stroke:
                    continue
                A = ["q"]
                for r in rings:
                    A.append("%s %s m" % (_f(r[0][0]), _f(r[0][1])))
                    A += ["%s %s l" % (_f(p[0]), _f(p[1])) for p in r[1:]]
                    A.append("h")
                if fill:
                    A.append("%s rg" % _col(fill))
                if stroke:
                    A.append("%s RG %s w" % (_col(stroke), _f(lw or 0.1)))
                A.append("B" if (fill and stroke) else "f" if fill else "S")
                A.append("Q")
                body += ("\n".join(A) + "\n").encode()
            elif t == "line":
                pts, stroke, lw = it[1:4]
                A = ["q %s RG %s w" % (_col(stroke), _f(lw or 0.1)), "%s %s m" % (_f(pts[0][0]), _f(pts[0][1]))]
                A += ["%s %s l" % (_f(p[0]), _f(p[1])) for p in pts[1:]]
                A.append("S Q")
                body += ("\n".join(A) + "\n").encode()
            elif t == "text":
                s, x, y, size, color, bold, align = it[1:8]
                wmm = text_w(s, size, bold)
                xx = x - {"L": 0.0, "C": wmm / 2.0, "R": wmm}.get(align, 0.0)
                body += ("BT /%s %s Tf %s rg %s 0 0 %s %s %s Tm (" % ("F2" if bold else "F1", _f(size / PT), _col(color),
                                                                     _f(PT), _f(PT), _f(xx), _f(y))).encode()
                body += _pdf_txt(s) + b") Tj ET\n"
        body += b"EMC\n"
    cid = add(b"<< /Length %d >>\nstream\n" % len(body) + bytes(body) + b"\nendstream")
    props = " ".join("/oc%d %d 0 R" % (i, i) for i in ocg.values())
    res = add(("<< /Font << /F1 %d 0 R /F2 %d 0 R >> /Properties << %s >> >>" % (f_r, f_b, props)).encode())
    pages_id = len(objs) + 2
    page = add(("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %s %s] /Contents %d 0 R /Resources %d 0 R >>" % (
        pages_id, _f(w / PT), _f(h / PT), cid, res)).encode())
    assert add(("<< /Type /Pages /Kids [%d 0 R] /Count 1 >>" % page).encode()) == pages_id
    oc = " ".join("%d 0 R" % i for i in ocg.values())
    cat = add(("<< /Type /Catalog /Pages %d 0 R /OCProperties << /OCGs [%s] /D << /Order [%s] /ON [%s] >> >> >>" % (
        pages_id, oc, oc, oc)).encode())
    info = add(b"<< /Title (" + _pdf_txt(title) + b") /Producer (Bergama Basemap) >>")
    out = bytearray(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += b"%d 0 obj\n" % (i + 1) + b + b"\nendobj\n"
    x = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    for o in offs:
        out += b"%010d 00000 n \n" % o
    out += b"trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, cat, info, x)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    try:
        with open(path, "wb") as f:
            f.write(bytes(out))
    except PermissionError:                              # open in a viewer: a timed name
        path = path[:-4] + time.strftime("_%H%M%S") + ".pdf"
        with open(path, "wb") as f:
            f.write(bytes(out))
    return path


# ================================================================ Basemap_colour.svg (his plan inside calisma_alan)
def plan_frame(txt, F):
    """the plan frame in his SVG (x, y, w, h units): the frame-shaped clip rectangle his Selinos group uses, else the
    commonest clip rectangle of the frame's proportions"""
    rects = {}
    for m in re.finditer(r'<clipPath id="([^"]+)">\s*<rect([^>]*)>', txt):
        a = dict(re.findall(r'([\w:-]+)="([^"]*)"', m.group(2)))
        try:
            r = (float(a.get("x", 0)), float(a.get("y", 0)), float(a["width"]), float(a["height"]))
        except Exception:
            continue
        if r[3] > 0 and abs(r[2] / r[3] - F.w / F.h) / (F.w / F.h) < 0.01 and "transform" not in a:
            rects[m.group(1)] = r
    if not rects:
        return None, u"no clip rectangle of the frame's proportions"
    i = txt.find('id="Selinos"')
    if i >= 0:
        for cid in re.findall(r'clip-path="url\(#([^)]+)\)"', txt[i:i + 600]):
            if cid in rects:
                return rects[cid], u"the Selinos group's frame clip %s" % cid
    cnt = {}
    for r in rects.values():
        cnt[r] = cnt.get(r, 0) + 1
    return max(cnt, key=cnt.get), u"the commonest frame-shaped clip rectangle (no Selinos group clip found)"


def write_colour_svg(D, F, log):
    src = os.path.join(BERGAMA_ROOT, PLAN_SVG)
    if not D.get("calisma"):
        return
    if not os.path.isfile(src):
        log.append(u"FLAG Basemap_colour.svg not written: %s not found" % src)
        return
    with open(src, encoding="utf-8") as f:
        txt = f.read()
    fr, how = plan_frame(txt, F)
    if fr is None:
        log.append(u"FLAG Basemap_colour.svg not written: %s in %s" % (how, src))
        return
    rx, ry, rw, rh = fr
    s = rw / F.w
    m0 = re.search(r"<svg\b[^>]*>", txt)
    m1 = txt.rfind("</svg>")
    vb = re.search(r'viewBox="([^"]+)"', m0.group(0)) if m0 else None
    if not m0 or m1 < 0 or not vb:
        log.append(u"FLAG Basemap_colour.svg not written: %s has no svg root with a viewBox" % src)
        return
    vx, vy, vw, vh = [float(v) for v in vb.group(1).replace(",", " ").split()]

    def U(p):
        u, v = F.local(p)
        return "%.2f,%.2f" % (rx + u * s, ry + rh - v * s)

    def UL(q):
        return "%.2f,%.2f" % (rx + q[0] * s, ry + rh - q[1] * s)
    box = (0.0, 0.0, F.w, F.h)
    out = [m0.group(0), u"<defs><clipPath id=\"bg_calisma_clip\"><path clip-rule=\"evenodd\" d=\"M%s,%s h%s v%s h%s Z "
           u"M%s,%s h%s v%s h%s Z %s\"/></clipPath></defs>" % (
               vx, vy, vw, vh, -vw, rx, ry, rw, rh, -rw,
               u" ".join(u"M" + u" L".join(U(p) for p in P) + u" Z" for P in D["calisma"])),
           u"<g id=\"existing_basemap_bw\">",
           u"<rect id=\"white_ground\" x=\"%s\" y=\"%s\" width=\"%s\" height=\"%s\" fill=\"#ffffff\"/>" % (rx, ry, rw, rh)]
    n = 0
    for key, layer, stroke, lw, fill in STYLE:
        out.append(u"<g id=\"%s_%s\" fill=\"%s\" stroke=\"#%s\" stroke-width=\"%.3f\" stroke-linejoin=\"round\">" % (
            layer, key, (u"#" + fill) if fill else u"none", stroke, SVG_W.get(key, 0.2) * s))
        for cl, P in D["layers"].get(key, []):
            Q = [F.local(p) for p in P]
            if cl and len(Q) >= 3:
                R = clip_ring(Q, box)
                if len(R) >= 3:
                    out.append(u"<polygon points=\"%s\"/>" % u" ".join(UL(q) for q in R))
                    n += 1
            else:
                for run in clip_line(Q, box):
                    out.append(u"<polyline fill=\"none\" points=\"%s\"/>" % u" ".join(UL(q) for q in run))
                    n += 1
        out.append(u"</g>")
    out.append(u"</g>")
    out.append(u"<g id=\"plan_inside_calisma_alan\" clip-path=\"url(#bg_calisma_clip)\">")
    head = u"\n".join(out)
    tail = [u"</g>", u"<g id=\"calisma_alan_outline\" fill=\"none\" stroke=\"#1a1a1a\" stroke-width=\"%.3f\" "
            u"stroke-dasharray=\"%.2f %.2f\">" % (1.0 * s, 6.0 * s, 3.0 * s)]
    tail += [u"<polygon points=\"%s\"/>" % u" ".join(U(p) for p in P) for P in D["calisma"]]
    tail += [u"</g>", u"<rect id=\"site_alan_frame\" x=\"%s\" y=\"%s\" width=\"%s\" height=\"%s\" fill=\"none\" "
             u"stroke=\"#1a1a1a\" stroke-width=\"%.3f\"/>" % (rx, ry, rw, rh, 0.6 * s), u"</svg>"]
    dst = os.path.join(OUT_DIR, "Basemap_colour.svg")
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt[:m0.start()])
        f.write(head)
        f.write(txt[m0.end():m1])
        f.write(u"\n".join(tail))
    log.append(u"%s  %s (his plan %s, %.1f MB, inside calisma_alan; frame = %s at (%.2f, %.2f) %.2f x %.2f units, %.4f "
               u"units per m; %d black and white outlines under it)" % (
                   dst, time.strftime("%H:%M:%S"), os.path.basename(src), os.path.getsize(src) / 1048576.0, how, rx, ry, rw,
                   rh, s, n))


# ================================================================ main
def load_or_read(log):
    import Rhino
    doc = Rhino.RhinoDoc.ActiveDoc
    key = model_key(doc)
    if key and os.path.isfile(CACHE_FILE):
        try:
            with open(CACHE_FILE, encoding="utf-8") as f:
                D = json.load(f)
            if D.get("key") == key:
                log.append(u"same model as the cache: %s used, the model not read again" % CACHE_FILE)
                return D
        except Exception:
            pass
    t0 = time.time()
    D = read_model(doc, log)
    D["key"] = key
    D["made_by"] = u"%s %s" % (GH_LABEL, VERSION)
    D["made_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    D["what"] = (u"survey layers of the open model in survey m, uncut; frame = site_alan corners; draw with the frame "
                 u"turned flat (long side horizontal, eastern end right)")
    for k_, L in D["layers"].items():
        D["layers"][k_] = [[bool(cl), [[round(p[0], 2), round(p[1], 2)] for p in P]] for cl, P in L]
    D["frame"] = [[round(p[0], 3), round(p[1], 3)] for p in D["frame"]]
    D["calisma"] = [[[round(p[0], 3), round(p[1], 3)] for p in P] for P in D.get("calisma", [])]
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(D, f, ensure_ascii=False)
    log.append(u"%s  %s (model read in %.1f s)" % (CACHE_FILE, time.strftime("%H:%M:%S"), time.time() - t0))
    return D


def main():
    t0 = time.time()
    log = []
    den = int(globals().get("scale") or 2000)
    kden = int(globals().get("keymap_scale") or 10000)
    D = load_or_read(log)
    F = Frame([tuple(p) for p in D["frame"]])
    D["turn_deg"] = round(math.degrees(F.rot), 4)
    log.append(u"frame: site_alan %.2f x %.2f m, turned %.2f deg; north on the page points (%.3f, %.3f)" % (
        F.w, F.h, math.degrees(F.rot), F.north()[0], F.north()[1]))
    for name, d, styles, sec, title in ((u"Basemap", den, STYLE, False, u"BASEMAP · existing"),
                                        (u"Keymap", kden, KEY_STYLE, True, u"KEY MAP")):
        m = 15.0
        items, cnt = draw(D, F, d, styles, m, m + 16.0, sections=sec)
        by = dict((s[0], s) for s in styles)
        leg = [by[k_] + (lab,) for k_, lab in LEGEND if k_ in by and cnt.get(k_)]
        items += furniture(F, d, m, m + 16.0, title, leg)
        w = F.w * 1000.0 / d + 2 * m
        h = F.h * 1000.0 / d + 2 * m + 16.0
        p = write_pdf(os.path.join(OUT_DIR, name + u".pdf"), w, h, items, u"%s, site_alan, 1:%d" % (name, d))
        log.append(u"%s  %s (%.0f x %.0f mm, 1:%d; %s)" % (p, time.strftime("%H:%M:%S"), w, h, d, u", ".join(
            u"%s %d" % kv for kv in sorted(cnt.items()))))
    write_colour_svg(D, F, log)
    if not D.get("sections"):
        log.append(u"no curves on layer %s in the model: the key map has no section lines yet" % SECTION_LAYER)
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
