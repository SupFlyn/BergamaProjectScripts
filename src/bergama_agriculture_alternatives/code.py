# bergama_agriculture_alternatives_v1_2.py · Thread 3 of the 22 Oct batch: three alternatives for the agriculture analysis
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Makes the folder Downloads/Bergama/output/Bergama_agriculture_alternatives by itself and saves ONE
# all-vector A3 PDF there, one page per alternative:
#   1 WHAT EACH CUBIC METRE GROWS   chart: hectares the stored water irrigates, per crop, normal and 1-in-5 dry year
#   2 THE FARMS WE FEED             plan 1:10,000: the around2 extent, its fields, orchards and their water need
#   3 ONE PLANT LADDER              schematic section: riverbed to farm, water depth, what grows today, what we plant
# Storage, water to the farms and the farm areas are read on every run from the water balance script's output
# (bergama_water_balance), so they follow its cost cut-off; the fallback is the shared key-figures file (flagged).
# Notes for Aras: batch_2026-10-22/thread3_agriculture/NOTES.md.
import os, time, json, zlib, math

VERSION = "v1.2"
# v1.2 (Aras 25 Oct 17:00, SCRIPT_STANDARD §5b visual first): sentences become pictogram tiles, callouts and tags; method
# and source sentences become [n] marks with one numbered source key in each page's footer; layout and colours kept.
# Flood figures corrected to the surveyed sections (research/rain_river_levels/README.md, v1.1 correction and line 49).
# v1.1 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_agriculture_alternatives_log.txt (next to cached/ and output/), overwritten by each press.
LOG_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "logs")   # Aras 25 Oct 09:34-09:35: every script's log here


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, "bergama_agriculture_alternatives_log.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text

# v1 24 Oct: all files under Downloads/Bergama/ (Aras rule)
OUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "Bergama_agriculture_alternatives")
OUT_PDF = "Bergama_agriculture_alternatives_A3.pdf"
# built-in geometry and tables (survey coordinates, m): around2 extent, site frame, WorldCover classes clipped to the
# extent (outside / inside the site), Selinos and other streams, FAO-56 net irrigation per water year (C1), corridor cover
#@include data/GEO.py

# ------------------------------------------------------------------ live numbers from the water balance (Thread 2)
# The water balance script writes its results on every run; this script reads them, so storage and the share covered
# are never typed in here. Searched in this order; the first file found wins.
LIVE_FILES = [os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "Bergama_water_balance_analysis", "water_balance_results.json"),
              os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis", "water_balance_results.json")]   # old place, read fallback
# fallback: the cloud copy research/water_balance/water_balance_results_default.json (default lands, 24 Oct 08:23)
DEFAULT = json.loads('{"cutoff":{"orchard olive + cropland cotton":{"central":{"storage_m3":375000,"covered_pct_1in5_dry":99.2,"delivered_m3_per_year":336093}},"orchard olive + cropland tomato":{"central":{"storage_m3":350000,"covered_pct_1in5_dry":99.7,"delivered_m3_per_year":310094}}},"farm_demand_m3":{"orchard olive + cropland cotton":{"mean":339980,"median":348773,"wet5":315782,"dry5":356580,"dry10":382453,"min":278845,"max":393001,"dry5_year":2006},"orchard olive + cropland tomato":{"mean":311982,"median":319136,"wet5":288317,"dry5":334143,"dry10":343054,"min":251458,"max":362453,"dry5_year":2021}},"net_irrigation_mm":{"olive":{"mean":614.3,"median":619.5,"wet5":519.6,"dry5":720.1,"dry10":725.2,"min":415.2,"max":822.7},"cotton":{"mean":853.2,"median":875.6,"wet5":789.5,"dry5":891.8,"dry10":962.6,"min":703.1,"max":981.9},"maize":{"mean":722.7,"median":740.8,"wet5":675.4,"dry5":761.8,"dry10":816.2,"min":605.7,"max":835.7},"tomato":{"mean":781.0,"median":801.3,"wet5":719.7,"dry5":837.0,"dry10":860.8,"min":632.5,"max":903.1}},"lands":{"cropland_ha":34.9,"orchard_ha":1.34,"cropland_crops":"cotton,tomato"}}')
DEFAULT_NOTE = "FLAG: water balance results file not found in Downloads; default-lands copy of 24 Oct used"

def live():
    """storage, share covered and need per mix (cost cut-off, central case), farm areas, crops and net need per crop"""
    d, src = None, DEFAULT_NOTE
    for p in LIVE_FILES:
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            src = "water balance results of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
            break
        except Exception:
            d = None
    if d is None: d = DEFAULT
    mixes = [m for m in d["cutoff"] if m in d["farm_demand_m3"]]
    L = dict(storage_m3=[d["cutoff"][m]["central"]["storage_m3"] for m in mixes],
             farm_share_dry5_pct=[d["cutoff"][m]["central"]["covered_pct_1in5_dry"] for m in mixes],
             farm_need_dry5_m3=[d["farm_demand_m3"][m]["dry5"] for m in mixes],
             cropland_ha=d["lands"]["cropland_ha"], orchard_ha=d["lands"]["orchard_ha"],
             crops=[c.strip() for c in str(d["lands"].get("cropland_crops", "")).split(",") if c.strip()],
             net=d["net_irrigation_mm"])
    return L, src

def span(v):
    return (min(v), max(v)) if isinstance(v, (list, tuple)) else (v, v)

# ------------------------------------------------------------------ colours (palette v1.4 core roles)
C = dict(ground="E2E0D4", paper="EFEDE6", faint="D8D5CC", structure="B0AC9C", ink2="847E75", ink="4A3F35",
         green_deep="495338", green_mid="727A4E", green_light="8C9969", water_deep="5D7F8D", water="91ADB4",
         water_light="C1D3DB", accent="8B3A3F", accent_deep="633131", white="FFFFFF",
         field="BDB57A", orchard="70754C", tree="89986A", grass="C9CDB0", shrub="A2B6B5", olive="5C7A86")

#@include ../common/rgb.py

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]

_TR = str.maketrans(u"ıİğĞşŞ", u"iIgGsS")

#@include ../common/text_w.py

class Page:
    def __init__(self, w, h):
        self.w, self.h, self.ops = w, h, []
    def _c(self, h, stroke=False):
        r, g, b = rgb(h); return "%.3f %.3f %.3f %s" % (r, g, b, "RG" if stroke else "rg")
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)
    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None):
        self.path([P], fill, stroke, lw, closed, dash)
    def path(self, rings, fill=None, stroke=None, lw=0.2, closed=True, dash=None):
        """several rings in one path; a fill uses even-odd, so holes stay open"""
        k = 72 / 25.4; o = ["q"]
        if fill: o.append(self._c(fill))
        if stroke: o.append(self._c(stroke, True)); o.append("%.3f w 1 J 1 j" % (lw * k))
        if dash: o.append("[%.2f %.2f] 0 d" % (dash[0] * k, dash[1] * k))
        for P in rings:
            o.append("%.2f %.2f m" % (P[0][0] * k, P[0][1] * k))
            o += ["%.2f %.2f l" % (x * k, y * k) for x, y in P[1:]]
            if closed: o.append("h")
        o.append("B*" if fill and stroke else ("f*" if fill else "S")); o.append("Q")
        self.ops.append(" ".join(o))
    def line(self, P, col, lw=0.25, dash=None): self.path([P], None, col, lw, False, dash)
    def circle(self, x, y, r, fill=None, stroke=None, lw=0.2):          # v1.2: for the pictograms
        self.poly([(x + r * math.cos(k * math.pi / 12), y + r * math.sin(k * math.pi / 12)) for k in range(24)], fill, stroke, lw, True)
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L"):
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        k = 72 / 25.4
        s = s.translate(_TR)                       # Helvetica WinAnsi has no ı İ ğ Ğ ş Ş: written as i I g G s S
        b = s.encode("cp1252", "replace").replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
        self.ops.append("BT /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET" % ("F2" if bold else "F1", size, self._c(col), x * k, y * k, b.decode("latin-1")))
    def para(self, s, x, y, w, size, col="4A3F35", bold=False, lead=1.3):
        line, yy = "", y
        for word in s.split(" "):
            t = (line + " " + word).strip()
            if text_w(t, size, bold) > w and line:
                self.text(line, x, yy, size, col, bold); yy -= size * 0.3528 * lead; line = word
            else: line = t
        if line: self.text(line, x, yy, size, col, bold); yy -= size * 0.3528 * lead
        return yy

def write_pdf(pages, path):
    k = 72 / 25.4
    n = len(pages)
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % (5 + 2 * i) for i in range(n)), n),
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>"]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
    for i, o in enumerate(objs):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (i + 1, o)).encode("latin-1")
    for i, pg in enumerate(pages):
        content = zlib.compress("\n".join(pg.ops).encode("latin-1"))
        offs.append(len(out))
        out += ("%d 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.2f %.2f] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents %d 0 R >>\nendobj\n"
                % (5 + 2 * i, pg.w * k, pg.h * k, 6 + 2 * i)).encode("latin-1")
        offs.append(len(out))
        out += ("%d 0 obj\n<< /Length %d /Filter /FlateDecode >>\nstream\n" % (6 + 2 * i, len(content))).encode("latin-1") + content + b"\nendstream\nendobj\n"
    x = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(offs) + 1) + "".join("%010d 00000 n \n" % o for o in offs) +
            "trailer\n<< /Size %d /Root 1 0 R /Info << /Title (Bergama agriculture alternatives) >> >>\nstartxref\n%d\n%%%%EOF\n" % (len(offs) + 1, x)).encode("latin-1")
    with open(path, "wb") as f: f.write(out)

# ------------------------------------------------------------------ shared helpers
#@include ../common/fmt.py
def fmt1(v): return "{:,.1f}".format(v)
def rnd(v, step=1000): return int(round(v / step) * step)
EFF = 0.90          # drip application efficiency, as the water balance (key figures "basis": "drip 90 %")

NET = {}            # net irrigation mm per crop from the water balance results (mean, dry5 = 1-in-5 dry year), set in build()

def gross_m3_ha(crop, year):
    if crop == "mix":                  # field crops weighted by their 2025 Bergama areas
        w = {c: TUIK_2025_DA[c] for c in ("cotton", "maize", "tomato") if c in NET}
        return sum(gross_m3_ha(c, year) * v for c, v in w.items()) / sum(w.values())
    return NET[crop]["mean" if year == "normal" else "dry5"] / EFF * 10.0     # 1 mm on 1 ha = 10 m3

SRC_KEY = []          # v1.2: sources printed as [n] on the page; the numbered key is in that page's footer

def cite(src):
    """v1.2 (water board v1.6 method): the number of a source in this page's footer key, as "[n]"."""
    if src not in SRC_KEY: SRC_KEY.append(src)
    return "[%d]" % (SRC_KEY.index(src) + 1)

def wrap(s, size, w, bold=False):
    out, line = [], ""
    for word in s.split(" "):
        t = (line + " " + word).strip()
        if text_w(t, size, bold) > w and line: out.append(line); line = word
        else: line = t
    if line: out.append(line)
    return out

def header(pg, n, title, sub):
    del SRC_KEY[:]                                 # v1.2: each page numbers its own sources from [1]
    pg.rect(0, 0, 420, 297, fill=C["ground"])
    pg.text(n, 14, 279, 22, C["accent"], True)
    pg.text(title, 26, 279, 22, C["ink"], True)
    pg.text(sub, 26, 271.5, 11, C["ink2"])
    pg.text("ALTERNATIVE %s OF 3 · AGRICULTURE ANALYSIS · GROUP 6" % n, 406, 281, 7, C["ink2"], True, "R")

def footer(pg, credit):
    """v1.2: the page's numbered source key (small text), then the credit line"""
    key = "Sources by number: " + "  ".join("[%d] %s" % (i + 1, k) for i, k in enumerate(SRC_KEY))
    lead = 6 * 0.3528 * 1.3
    y = pg.para(key, 14, min(15.0, 4.0 + len(wrap(key, 6, 392)) * lead), 392, 6, C["ink2"])
    pg.text(credit, 14, y, 6, C["ink2"])

CREDIT = "Script bergama_agriculture_alternatives %s · Group 6" % VERSION

# ------------------------------------------------------------------ v1.2 pictograms and tiles (from water board v1.6/v1.7)
def icon(pg, kind, x, y, sz):
    """a pictogram in the square (x, y - sz)-(x + sz, y), drawn on a 10 x 10 grid. Graphic only."""
    u = sz / 10.0; lw = 0.07 * sz
    P = lambda pts: [(x + a * u, y - sz + b * u) for a, b in pts]
    Q = lambda a0, b0, a1, b1: P([(a0, b0), (a1, b0), (a1, b1), (a0, b1)])
    O = lambda a, b, r, **kw: pg.circle(x + a * u, y - sz + b * u, r * u, **kw)
    pt = lambda mm: mm / 0.3528

    def drop(a, b, r, col):
        pg.poly(P([(a - r * 0.85, b + r * 0.45), (a, b + r * 2.2), (a + r * 0.85, b + r * 0.45)]), fill=col, closed=True)
        O(a, b, r, fill=col)
    ink, ink2, acc = C["ink"], C["ink2"], C["accent"]
    if kind == "nowater":                       # no water-hungry crops
        drop(5.0, 2.6, 2.3, C["water"])
        pg.line(P([(1.2, 1.0), (8.8, 9.2)]), acc, lw * 1.4)
    elif kind == "cotton":
        pg.line(P([(5.0, 0.4), (5.0, 5.0)]), C["green_deep"], lw)
        for a, b in ((3.3, 5.9), (6.7, 5.9), (5.0, 8.1)): O(a, b, 1.9, fill=C["white"], stroke=ink2, lw=lw * 0.6)
    elif kind == "olive":
        pg.poly(Q(4.5, 0.4, 5.5, 4.4), fill=ink2, closed=True)
        O(5.0, 6.2, 3.4, fill=C["green_mid"])
        for a, b in ((3.8, 6.8), (6.0, 5.4), (5.4, 7.8)): O(a, b, 0.5, fill=ink)
    elif kind == "drip":
        pg.poly(Q(0, 7.0, 10, 8.4), fill=ink2, closed=True)
        for a in (2.0, 5.0, 8.0): drop(a, 3.4, 0.8, C["water_deep"])
        pg.poly(Q(0, 0.4, 10, 1.6), fill=C["field"], closed=True)
    elif kind == "cube":                        # storage
        pg.poly(P([(5, 9.8), (9.2, 7.6), (5, 5.4), (0.8, 7.6)]), fill=C["water_light"], closed=True)
        pg.poly(P([(0.8, 7.6), (5, 5.4), (5, 0.4), (0.8, 2.6)]), fill=C["water"], closed=True)
        pg.poly(P([(5, 5.4), (9.2, 7.6), (9.2, 2.6), (5, 0.4)]), fill=C["water_deep"], closed=True)
    elif kind in ("inside", "outside"):         # fields inside / outside the site frame
        if kind == "inside":
            pg.poly(Q(0.6, 0.6, 9.4, 9.4), fill="E8E5DA", stroke=ink, lw=lw, closed=True)
            pg.poly(P([(2.0, 2.0), (6.6, 2.0), (8.0, 6.4), (3.4, 6.4)]), fill=C["field"], closed=True)
        else:
            pg.poly(Q(0.4, 3.4, 5.4, 9.4), fill="E8E5DA", stroke=ink, lw=lw, closed=True)
            pg.poly(P([(4.6, 0.4), (8.6, 0.4), (9.8, 3.6), (5.8, 3.6)]), fill=C["field"], closed=True)
            pg.poly(P([(6.6, 4.6), (9.0, 4.6), (9.8, 8.2), (7.4, 8.2)]), fill=C["field"], closed=True)
    elif kind == "extent":
        pg.poly(P([(0.4, 3.0), (7.4, 0.4), (9.6, 7.0), (2.6, 9.6)]), fill=C["paper"], stroke=ink, lw=lw, closed=True)
        pg.poly(P([(2.4, 3.6), (5.0, 2.6), (5.8, 5.0), (3.2, 6.0)]), fill=C["field"], closed=True)
        O(6.6, 6.4, 1.2, fill=C["orchard"])
    elif kind == "route":                       # a route not drawn yet
        pg.line(P([(0.6, 1.4), (4.0, 4.6), (6.2, 3.6), (9.4, 8.6)]), C["water_deep"], lw, (lw * 2.0, lw * 1.6))
        pg.text("?", x + 7.6 * u, y - sz + 1.0 * u, pt(4.2 * u), acc, True, "C")
    elif kind == "clean":                       # reeds in water
        pg.poly(Q(0, 0, 10, 2.4), fill=C["water"], closed=True)
        for k_ in range(5):
            a = 1.6 + k_ * 1.7; t = 6.4 + (k_ % 2) * 2.4
            pg.line(P([(a, 0.8), (a + 0.3, t)]), C["green_deep"], lw)
            pg.poly(Q(a - 0.25, t - 1.8, a + 0.85, t + 0.2), fill=C["green_mid"], closed=True)
    elif kind == "hold":                        # roots holding the bank
        pg.poly(P([(0, 0.4), (10, 0.4), (10, 6.0), (0, 2.0)]), fill=C["structure"], closed=True)
        for a in (3.0, 6.6):
            b = 2.0 + a * 0.4
            pg.line(P([(a, b), (a, b + 3.2)]), C["green_deep"], lw)
            pg.line(P([(a, b), (a - 1.4, b - 1.6)]), ink, lw * 0.7)
            pg.line(P([(a, b), (a + 1.2, b - 1.8)]), ink, lw * 0.7)
            pg.line(P([(a, b), (a, b - 1.6)]), ink, lw * 0.7)
            O(a, b + 3.6, 1.0, fill=C["green_mid"])
    elif kind == "shade":                       # tree and its shade
        pg.poly(Q(0.6, 0.4, 9.4, 1.4), fill=C["ink2"], closed=True)
        pg.poly(Q(4.5, 1.4, 5.5, 5.2), fill=ink2, closed=True)
        O(5.0, 6.8, 3.0, fill=C["green_deep"])
    elif kind == "scent":                       # flowering shrub and scent lines
        for a in (3.2, 5.0, 6.8):
            pg.line(P([(5.0, 0.4), (a, 5.0)]), C["green_deep"], lw)
            O(a, 5.6, 0.8, fill=acc)
        for a in (2.6, 5.0, 7.4):
            pg.line(P([(a + (0.5 if j % 2 else -0.5), 6.8 + j * 0.8) for j in range(4)]), ink2, lw * 0.7)
    elif kind == "nose":                        # odour, effect not measured
        for k_ in range(3):
            a = 2.0 + k_ * 2.6
            pg.line(P([(a + (0.7 if j % 2 else -0.7), 0.8 + j * 1.6) for j in range(6)]), ink2, lw)
        pg.text("?", x + 8.8 * u, y - sz + 0.6 * u, pt(3.4 * u), acc, True, "C")

def tiles(pg, x, y, w, items, cols=1, s=1.0, fill=None):
    """v1.2 (water board v1.6): facts as tiles: pictogram, keyword heading, the key figure large, short keyword lines and
    the source number. items = [(pictogram, heading, figure or None, [keyword lines], source or None)]. Returns the bottom y."""
    k = 0.3528
    fh, fb, ft = 8.5 * s, 15.0 * s, 7.0 * s
    ic, pad, g = 12.0 * s, 2.2 * s, 2.4 * s
    tw = (w - (cols - 1) * g) / cols
    txw = tw - ic - 3 * pad
    lay = []
    for kind, head, big, lines, ref in items:
        lines = list(lines or [])
        if ref: lines = lines[:-1] + [((lines[-1] + " ") if lines else "") + cite(ref)]
        L3 = (wrap(head, fh, txw, True), wrap(big, fb, txw, True) if big else [], [q for ln in lines for q in wrap(ln, ft, txw)])
        hh = pad * 2 + (len(L3[0]) * fh * 1.25 + len(L3[1]) * fb * 1.15 + len(L3[2]) * ft * 1.3 + (fh * 0.3 if L3[1] else 0)) * k
        lay.append((kind, big, L3, max(hh, ic + 2 * pad)))
    yy = y
    for r0 in range(0, len(lay), cols):
        row = lay[r0:r0 + cols]
        rh = max(t[3] for t in row)
        for c_, (kind, big, L3, _) in enumerate(row):
            tx = x + c_ * (tw + g)
            pg.rect(tx, yy - rh, tw, rh, fill=fill or C["paper"], stroke=C["faint"], lw=0.2)
            icon(pg, kind, tx + pad, yy - pad, ic)
            lx, ly = tx + 2 * pad + ic, yy - pad
            for ln in L3[0]:
                ly -= fh * 1.25 * k; pg.text(ln, lx, ly + fh * 0.25 * k, fh, C["ink"], True)
            if L3[1]: ly -= fh * 0.3 * k
            for ln in L3[1]:
                ly -= fb * 1.15 * k
                pg.text(ln, lx, ly + fb * 0.2 * k, fb, C["accent"] if big in FLAGGED else C["green_deep"], True)
            for ln in L3[2]:
                ly -= ft * 1.3 * k; pg.text(ln, lx, ly + ft * 0.3 * k, ft, C["ink"])
        yy -= rh + g
    return yy + g

FLAGGED = ("NOT KNOWN", "not designed")         # big figures that say "no data": in the accent colour

def north(pg, x, y, ang_deg, r=7.0):
    a = math.radians(ang_deg)
    ux, uy = -math.sin(a), math.cos(a)
    px, py = -uy, ux
    tip = (x + ux * r, y + uy * r); bl = (x - ux * r * 0.6 + px * r * 0.45, y - uy * r * 0.6 + py * r * 0.45)
    br = (x - ux * r * 0.6 - px * r * 0.45, y - uy * r * 0.6 - py * r * 0.45)
    pg.poly([tip, bl, (x, y), br], fill=C["ink"], closed=True)
    pg.text("N", tip[0] + ux * 3.0, tip[1] + uy * 3.0 - 1.2, 8, C["ink"], True, "C")

# ------------------------------------------------------------------ page 1: what each cubic metre grows
NEWS = "news: Ajans Bakırçay 19.03.2025 (research/water_data/03 §3)"
TUIK = "TÜİK Bitkisel Üretim, Bergama 2025 (library/research/crops_2026-10-24 §1.24-1.25)"
KAYA = "Kaya et al. 2017, Irrig. Drain. 66(5):820-827, Tables II, III, VI, pp.823-826 (deficit saving: Table II, S0.50 and S0.25 vs control)"
ITB = "İzmir Ticaret Borsası cotton report 2025, p.5"
NET_REF = ("net irrigation: research/water_balance/tables/C1 (FAO-56, Allen et al. 1998; MGM/WMO 17742 normals; ERA5 1991-2025 "
           "scaled); per ha = FAO-56 daily soil balance net need (34 water years, Bergama climate) / 0.90 drip (calculated)")
TAGEM = ("check: TAGEM/DSİ 2017 §12 Bergama 17742 station tables (net = ETc - 0.8 rain, our arithmetic): cotton 829 vs our 853 mm, "
         "maize 765 vs 723, tomato 606-825 vs 781, olive 502-603 vs 614")
# v1.2: the context sentences as tiles (pictogram, heading, big figure, keyword lines, source)
CONTEXT = [
    ("nowater", "DROUGHT 2025: NO WATER-HUNGRY CROPS", "7,500 ha",
     ["maize, cotton, fodder · Bergama villages", "no water for second crops · DSİ + Ministry"], NEWS),
    ("cotton", "COTTON: BERGAMA'S BIGGEST CROP", "10,000 ha",
     ["2025 · 37 % of 26,800 ha field crops", "maize 6,000 · tomato 2,500 · olive 8,700 ha"], TUIK),
    ("olive", "OLIVES CAN TAKE LESS · MEMECIK, DRIP", "-72 % water",
     ["İzmir station 2008-10 · 175 vs 622 mm a season", "24.9 vs 27.8 kg a tree: no significant loss",
      "highest oil content"], KAYA),
    ("drip", "TODAY'S IRRIGATION ON THE FARMS", "NOT KNOWN", ["some Bergama growers moved to drip"], ITB),
]
REPLACES = [("cube", "THE WATER BOARD LINE IT REPLACES", "10,000 m³ = 1.22 ha olive",
             ["was: İzmir crop water use", "now: Bergama climate · rain in the soil · live storage"], None)]
DEFICIT = (1 - 350.0 / 622, 1 - 175.0 / 622)   # olive water saved: S0.50 and S0.25 against the control SC, Kaya et al. 2017 Table II
# Bergama district areas 2025, da (TÜİK MEDAS export, library/research/crops_2026-10-24/bergama_crops_irrigation_v1.md §1.25):
# the share of each crop the water balance models, used for the district mix row
TUIK_2025_DA = dict(cotton=99963, maize=24532 + 35491, tomato=13740 + 11268, olive=65978 + 21068)

def page_cubic(L, src):
    pg = Page(420, 297)
    header(pg, "1", "WHAT EACH CUBIC METRE GROWS",
           "Same storage, different crops: hectares irrigated a season")
    s_lo, s_hi = span(L["storage_m3"]); p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0          # m3 the storage gives the farms in the 1-in-5 dry year
    fed = L["cropland_ha"] + L["orchard_ha"]
    SRC1 = "storage, need and share: " + src + "; water to farms = 1-in-5 dry-year need x share covered (calculated)"
    MIX = ("Bergama mix = cotton, maize and tomato weighted by their 2025 district areas; no map shows what the 34.9 ha grow, "
           "so the mix stands in (FLAG); water balance crops: %s" % (", ".join(L["crops"]) or "not set"))
    # key line
    pg.text("%s-%s m³" % (fmt(rnd(s_lo)), fmt(rnd(s_hi))) if rnd(s_lo) != rnd(s_hi) else "%s m³" % fmt(rnd(s_lo)), 26, 250, 26, C["water_deep"], True)
    pg.text("storage · cost cut-off " + cite(SRC1), 26, 242, 9, C["ink"])
    pg.text("%s-%s m³" % (fmt(rnd(w_lo)), fmt(rnd(w_hi))), 120, 250, 26, C["green_deep"], True)
    pg.text("to farms · 1-in-5 dry year · %s %% of need · strip first" % (("%.0f" % p_lo) if "%.0f" % p_lo == "%.0f" % p_hi else "%.0f-%.0f" % (p_lo, p_hi)), 120, 242, 9, C["ink"])
    # bars: hectares served by W, per crop
    rows = [("Olive, full irrigation", "olive", None), ("Olive, deficit irrigation", "olive", DEFICIT)] + \
           [(c.capitalize(), c, None) for c in sorted(NET) if c != "olive"] + [("Bergama mix (TÜİK 2025)", "mix", None)]
    x0, y0, gw = 70, 214, 190
    vals = []
    for lab, crop, d in rows:
        for yr in ("normal", "dry"):
            g = gross_m3_ha(crop, yr)
            if d: lo, hi = w_lo / (g * (1 - d[0])), w_hi / (g * (1 - d[1]))
            else: lo, hi = w_lo / g, w_hi / g
            vals.append((lab, crop, yr, g, lo, hi, d))
    vmax = max(v[5] for v in vals) * 1.08
    step = 25 if vmax < 160 else (50 if vmax < 400 else 100)
    for t in range(0, int(vmax) + 1, step):
        xx = x0 + gw * t / vmax
        pg.line([(xx, y0 - len(rows) * 19.5 + 6), (xx, y0 + 6)], C["faint"], 0.2)
        pg.text("%d ha" % t, xx, y0 - len(rows) * 19.5 + 1.5, 7, C["ink2"], align="C")
    xf = x0 + gw * fed / vmax
    pg.line([(xf, y0 - len(rows) * 19.5 + 6), (xf, y0 + 9)], C["accent"], 0.5, (1.5, 1.0))
    pg.text("farms we feed: %s ha" % fmt1(fed), xf + 1.2, y0 + 7.5, 7.5, C["accent"], True)
    for i, (lab, crop, d) in enumerate(rows):
        yy = y0 - i * 19.5
        pg.text(lab, x0 - 3, yy - 4.5, 10, C["ink"], True, "R")
        if crop in TUIK_2025_DA:
            pg.text("Bergama 2025: %s ha %s" % (fmt(TUIK_2025_DA[crop] / 10.0), cite(TUIK)), x0 - 3, yy - 13.5, 6.5, C["accent"], align="R")
        for j, yr in enumerate(("normal", "dry")):
            v = [q for q in vals if q[0] == lab and q[2] == yr][0]
            by = yy - j * 7.5
            col = C["green_light"] if yr == "normal" else C["green_deep"]
            pg.rect(x0, by - 6, gw * v[4] / vmax, 6, fill=col)
            if v[5] > v[4] * 1.01:
                pg.rect(x0 + gw * v[4] / vmax, by - 6, gw * (v[5] - v[4]) / vmax, 6, fill=None, stroke=col, lw=0.35)
            t = "%s-%s ha" % (fmt(v[4]), fmt(v[5])) if fmt(v[4]) != fmt(v[5]) else "%s ha" % fmt(v[4])
            pg.text(t, x0 + gw * v[5] / vmax + 2, by - 4.4, 8, C["ink"], True)
        g_n, g_d = gross_m3_ha(crop, "normal"), gross_m3_ha(crop, "dry")
        if d: g_n, g_d = g_n * (1 - d[1]), g_d * (1 - d[0])
        mk = cite(NET_REF) + (cite(KAYA) if d else "") + (cite(MIX) if crop == "mix" else "")
        pg.text("%s-%s m³ per ha a season %s" % (fmt(rnd(min(g_n, g_d), 10)), fmt(rnd(max(g_n, g_d), 10)), mk), x0 - 3, yy - 10, 7, C["ink2"], align="R")
    # key to the two bars
    ky = y0 - len(rows) * 19.5 - 4
    pg.rect(x0, ky, 6, 3, fill=C["green_light"]); pg.text("normal year (mean of 34)", x0 + 8, ky + 0.5, 7, C["ink"])
    pg.rect(x0 + 52, ky, 6, 3, fill=C["green_deep"]); pg.text("1-in-5 dry year", x0 + 60, ky + 0.5, 7, C["ink"])
    pg.rect(x0 + 92, ky, 6, 3, stroke=C["green_deep"], lw=0.35); pg.text("open bar: range (storage span; deficit 44-72 % saving)", x0 + 100, ky + 0.5, 7, C["ink"])
    # reading
    best = [q for q in vals if q[0] == "Olive, deficit irrigation" and q[2] == "dry"][0]
    worst = max((q for q in vals if q[1] not in ("olive", "mix") and q[2] == "dry"), key=lambda q: q[3])     # the thirstiest field crop
    pg.rect(14, 32, 250, 60, fill=C["paper"])
    pg.text("THE READING", 20, 84, 10, C["accent"], True)
    pg.text("per ha checked vs TAGEM/DSİ 2017 " + cite(TAGEM), 258, 84, 7, C["ink2"], align="R")
    # v1.2: the conclusion as the two dry-year bars (same scale) and the big ratio between them
    bmax, bx0, bw = best[5] * 1.05, 20, 150
    for k_, (q, lab) in enumerate(((worst, "%s, 1-in-5 dry year" % worst[1].capitalize()), (best, "Olive, deficit irrigation, 1-in-5 dry year"))):
        yb = 70 - k_ * 18
        pg.text(lab, bx0, yb + 1.5, 8, C["ink"], True)
        pg.rect(bx0, yb - 7, bw * q[4] / bmax, 7, fill=C["green_deep"])
        if q[5] > q[4] * 1.01:
            pg.rect(bx0 + bw * q[4] / bmax, yb - 7, bw * (q[5] - q[4]) / bmax, 7, fill=None, stroke=C["green_deep"], lw=0.35)
        pg.text("%s-%s ha" % (fmt(q[4]), fmt(q[5])), bx0 + bw * q[5] / bmax + 2, yb - 5.2, 9, C["ink"], True)
    bkx = 192
    pg.line([(bkx - 2, 66.5), (bkx, 66.5), (bkx, 48.5), (bkx - 2, 48.5)], C["accent"], 0.5)
    pg.text("%.1f-%.1f x" % (best[4] / worst[4], best[5] / worst[5]), bkx + 3, 55, 24, C["accent"], True)
    pg.text("as much land, same storage", bkx + 3, 49.5, 7.5, C["ink"])
    pg.text("lever: crop + irrigation method, more than storage", 20, 39, 8, C["ink"], True)
    pg.text("same water: more farmland · same farms: less storage", 20, 35, 8, C["ink"])
    # context column
    cx, cy = 280, 250
    pg.text("WHY CROP CHOICE IS THE LEVER", cx, cy, 11, C["ink"], True)
    tiles(pg, cx, cy - 6, 126, CONTEXT)
    pg.text("WHAT IT REPLACES", cx, 60, 9, C["accent"], True)
    tiles(pg, cx, 57, 126, REPLACES)
    footer(pg, CREDIT + " · news items flagged as news")
    return pg

# ------------------------------------------------------------------ page 2: the farms we feed (plan 1:10,000)
CLS = [("farmland", "Fields (cropland)", C["field"]), ("orchard", "Orchards (inferred)", C["orchard"]),
       ("trees", "Tree cover", C["tree"]), ("shrub", "Shrubland", C["shrub"]), ("grass", "Grassland", C["grass"])]

def page_farms(L, src):
    pg = Page(420, 297)
    header(pg, "2", "THE FARMS WE FEED",
           "Fields and orchards the stored water serves · dry-year need")
    WC = "ESA WorldCover 2021 v200, 10 m (CC BY 4.0), data/landcover"
    ORCH = "orchards inferred from survey symbols SEMBOL_ZEYTINLIK / SEMBOL_MEYVA_BAH"
    EXT = "extent = around2.pdf registered to the survey (research/water_balance)"
    NEED2 = "need: FAO-56 soil balance / 0.90 drip, normal and 1-in-5 dry years"
    SRC2 = "farm areas from " + src
    A = GEO["around2"]
    ax, ay = A[1][0] - A[0][0], A[1][1] - A[0][1]
    ang = math.atan2(ay, ax)                     # long edge of the extent, rotated to horizontal
    ca, sa = math.cos(-ang), math.sin(-ang)
    S = 0.1                                       # 1:10,000 -> 1 m = 0.1 mm
    rot = lambda p: ((p[0] - A[0][0]) * ca - (p[1] - A[0][1]) * sa, (p[0] - A[0][0]) * sa + (p[1] - A[0][1]) * ca)
    R = [rot(p) for p in A]
    mnx, mny = min(p[0] for p in R), min(p[1] for p in R)
    mxx, mxy = max(p[0] for p in R), max(p[1] for p in R)
    ox, oy = 30 - mnx * S, 112 - mny * S
    T = lambda p: (ox + rot(p)[0] * S, oy + rot(p)[1] * S)
    pg.path([[T(p) for p in A]], fill=C["paper"])
    pg.path([[T(p) for p in GEO["frame"]]], fill="E8E5DA")             # the site (drawn on the site board): tint only
    for side in ("out", "in"):
        for key, lab, col in CLS[::-1]:
            for poly in GEO["lc"][key][side]:
                c = col if (side == "out" or key in ("farmland", "orchard")) else "D9D6C8"
                pg.path([[T(p) for p in r] for r in poly], fill=c)
    for ln in GEO["streams"]: pg.line([T(p) for p in ln], C["water"], 0.5)
    for ln in GEO["selinos"]: pg.line([T(p) for p in ln], C["water_deep"], 1.1)
    fr = [T(p) for p in GEO["frame"]]
    fx, fy = sum(p[0] for p in fr) / len(fr), sum(p[1] for p in fr) / len(fr)
    pg.text("THE SITE", fx, fy + 1, 9, C["ink2"], True, "C")
    pg.text("land cover inside it: site board, plan 01", fx, fy - 3.2, 6.5, C["ink2"], align="C")
    north(pg, 398, 228, math.degrees(-ang))
    # scale bar 0-500 m
    pg.rect(330, 104, 25, 1.4, fill=C["ink"]); pg.rect(355, 104, 25, 1.4, fill=None, stroke=C["ink"], lw=0.3)
    for t, xx in ((0, 330), (250, 355), (500, 380)): pg.text("%d" % t, xx, 100.5, 6.5, C["ink"], align="C")
    pg.text("m · 1:10,000 at A3", 383, 100.5, 6.5, C["ink"])
    pg.text("land cover %s · orchards %s · extent %s" % (cite(WC), cite(ORCH), cite(EXT)), 406, 96.5, 6, C["ink2"], align="R")
    pg.text("Selinos %s · site frame %s" % (cite("Selinos centreline OSM"), cite("site frame from the course survey")), 406, 93.5, 6, C["ink2"], align="R")
    # numbers per class
    fed_c, fed_o = L["cropland_ha"], L["orchard_ha"]
    o_lo = min(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    o_hi = max(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    cc = [c for c in L["crops"] if c in NET] or [c for c in NET if c != "olive"]
    c_lo = min(gross_m3_ha(c, y) for c in cc for y in ("normal", "dry"))
    c_hi = max(gross_m3_ha(c, y) for c in cc for y in ("normal", "dry"))
    bx, by = 14, 92
    pg.text("WHAT THE FARMS ARE, AND WHAT THEY NEED", bx, by, 11, C["ink"], True)
    cols = [("Fields (cropland)", C["field"], fed_c, "%s-%s m³ a season" % (fmt(rnd(fed_c * c_lo)), fmt(rnd(fed_c * c_hi))),
             "as " + " / ".join(cc) + " · Bergama's main irrigated crops " + cite(TUIK)),
            ("Orchards (inferred)", C["orchard"], fed_o, "%s-%s m³ a season" % (fmt(rnd(fed_o * o_lo, 100)), fmt(rnd(fed_o * o_hi, 100))),
             "as olive · within 35 m of surveyed olive / fruit trees " + cite(ORCH)),
            ("Tree cover", C["tree"], sum(GEO["area_ha"]["trees"]), "not irrigated", "groves and woods: not counted as farms"),
            ("Grassland", C["grass"], sum(GEO["area_ha"]["grass"]), "not irrigated", "largest class · dry pasture or fallow (satellite can't tell)")]
    for i, (lab, col, ha, need, note) in enumerate(cols):
        x = bx + i * 98
        pg.rect(x, by - 12, 5, 5, fill=col)
        pg.text(lab + " " + cite(SRC2 if i < 2 else WC), x + 7, by - 11, 9, C["ink"], True)
        pg.text("%s ha" % fmt1(ha), x + 7, by - 21, 16, C["green_deep"] if i < 2 else C["ink2"], True)
        pg.text(need + (" " + cite(NEED2) if i < 2 else ""), x + 7, by - 27, 8.5, C["ink"], i < 2)
        pg.para(note, x + 7, by - 32, 88, 7, C["ink2"])
    pg.rect(bx + 3 * 98 + 7, by - 39.4, 3, 3, fill=C["paper"], stroke=C["ink2"], lw=0.2)       # v1.2: drawn legend sample
    pg.text("blank = built-up or bare", bx + 3 * 98 + 12, by - 39, 7, C["ink2"])
    pg.rect(14, 22, 392, 26, fill=C["paper"])
    pg.text("THE READING", 20, 41, 10, C["accent"], True)
    pg.text("small and close", 20, 35.5, 8, C["ink"], True)           # v1.2: the reading as figure tiles and tags
    f_in, f_out = GEO["area_ha"]["farmland"][1], GEO["area_ha"]["farmland"][0]
    tiles(pg, 52, 46, 350, [
        ("inside", "FIELDS INSIDE THE SITE", "%s ha" % fmt1(f_in), ["existing fields, not proposed farmland"], WC),
        ("outside", "FIELDS OUTSIDE THE SITE", "%s ha" % fmt1(f_out), ["much of the fields: a few 100 m from the Selinus"], WC),
        ("extent", "THE EXTENT THEY LIE IN", "%s ha" % fmt(L.get("extent_ha", 455.0)),
         ["%s ha fields · %s ha orchards" % (fmt1(fed_c), fmt1(fed_o))], SRC2),
        ("route", "WATER ROUTE TO THE FARMS", "not designed", ["crops: not known (satellite class only)"], None)],
        cols=4, s=0.8, fill=C["white"])
    footer(pg, CREDIT)
    return pg

# ------------------------------------------------------------------ page 3: one plant ladder, riverbed to field
# zones: interpretation of research/water_data/04 §3 (MITECO bands, 92D0 thickets, USDA NRCS TN-38 zones); depths
# from research/rain_river_levels/README.md "The answers in short" and (Q100/Q500, v1.2) its v1.1 correction of 24 Oct
# (surveyed sections, line 49); today's cover from the satellite corridor bands
SPECIES = ("species, flood and cleaning evidence: research/water_data/04 (POWO, FEIS, JRC Atlas, Korkusuz et al. 2004, "
           "Aydın Temel et al. 2017, Xie et al. 2021, RHS)")
BANDS = "bands = our reading of MITECO, Salinas & Cueto 2009 (92D0), USDA NRCS TN-38"
DEPTH = ("depths: research/rain_river_levels (DSİ Q100/Q500, calculated; Q100/Q500 on the surveyed sections, v1.1 "
         "correction of 24 Oct)")
TODAY = "today's cover: ESA WorldCover 2021 by distance from the OSM Selinos centreline"
REUSE = "reuse class B: 2010 communiqué as quoted (EN-E1)"
JOB_ICON = [("CLEAN", "clean"), ("HOLD", "hold"), ("SHADE", "shade"), ("SCENT", "scent"), ("HARVEST", "olive")]   # v1.2 job pictograms
#@include data/STEPS.py

def page_ladder(L, src):
    pg = Page(420, 297)
    header(pg, "3", "ONE PLANT LADDER, RIVERBED TO FIELD",
           "Every plant on one gradient: water, today's cover, job")
    n = len(STEPS); x0, x1 = 14, 406; w = (x1 - x0) / n
    base, rise = 168, 13.0                         # schematic steps: not to scale
    gy = [base + i * rise for i in range(n)]
    # Q500, Q100 and strip lines (schematic)
    pg.rect(x0, base - 6, w * 0.5, 6 + 3.5, fill=C["water"])
    q100, q500 = base + 3.25 * rise, base + 3.6 * rise    # drawn over the bank top: the K4 / S4 case (README v1.1, line 49)
    pg.line([(x0, q500), (x0 + w * 4.0, q500)], C["water_deep"], 0.4, (2.0, 1.2))
    pg.text("Q500, 263 m³/s: 2.3-3.3 m " + cite(DEPTH), x0 + 2, q500 + 1.5, 7, C["water_deep"], True)
    pg.text("over the banks only at K4 and S4 " + cite(DEPTH), x0 + w * 4.0 - 2, q500 + 1.5, 6.5, C["water_deep"], align="R")
    pg.line([(x0, q100), (x0 + w * 4.0, q100)], C["water"], 0.4, (2.0, 1.2))
    pg.text("Q100, 205 m³/s: 2.0-3.0 m", x0 + 2, q100 - 3.5, 7, C["water_deep"])
    pg.text("strip 0.30 m", x0 + 2, base - 4.5, 7, C["white"], True)
    for i, st in enumerate(STEPS):
        xa = x0 + i * w
        pg.rect(xa, 112, w, gy[i] - 112, fill=C["structure"] if i < n - 1 else C["field"])
        pg.text(st["name"], xa + 3, gy[i] - 6, 11, C["white"], True)
        pg.text(st["sub"], xa + 3, gy[i] - 10.5, 7.5, C["white"])
        # job tag on the ground
        pg.rect(xa + 3, 116, text_w(st["job"], 8, True) + 4, 5.5, fill=C["accent"])
        pg.text(st["job"], xa + 5, 117.6, 8, C["white"], True)
        jx = xa + 3 + text_w(st["job"], 8, True) + 6                # v1.2: the job as pictograms beside the tag
        for word, kind in JOB_ICON:
            if word in st["job"]:
                pg.rect(jx, 115.6, 6.5, 6.5, fill=C["paper"]); icon(pg, kind, jx + 0.5, 121.6, 5.5); jx += 7.5
        # water text above
        yy = 258
        pg.text("WATER", xa + 3, yy, 7, C["water_deep"], True); yy -= 4.5
        for t in st["water"]:
            yy = pg.para(t.replace("{reuse}", cite(REUSE)), xa + 3, yy, w - 6, 7.5, C["ink"])
        # today: satellite cover in the matching corridor band, both sides
        yy = 104
        pg.text("TODAY", xa + 3, yy, 7, C["green_deep"], True); yy -= 4.5
        if st["band"]:
            l, r = GEO["corridor"]["left " + st["band"]], GEO["corridor"]["right " + st["band"]]
            tr = (l["trees"] + r["trees"]) / 2; gr = (l["grass"] + r["grass"]) / 2; fa = (l["farmland"] + r["farmland"]) / 2
            for lab, v, col in (("trees", tr, C["tree"]), ("grass", gr, C["grass"]), ("fields", fa, C["field"])):
                pg.rect(xa + 3, yy - 2.2, (w - 30) * v / 100.0, 3.0, fill=col)
                pg.text("%s %.0f %%" % (lab, v), xa + 3 + (w - 30) * v / 100.0 + 1.5, yy - 1.9, 7, C["ink"])
                yy -= 5
            pg.text("satellite, %s m from the centreline %s" % (st["band"], cite(TODAY)), xa + 3, yy - 0.5, 6, C["ink2"])
            yy -= 6
        else:
            yy = pg.para("summer: dry gravel or a trickle", xa + 3, yy, w - 6, 7, C["ink"])
            yy = pg.para("no plant data in the channel", xa + 3, yy, w - 6, 7, C["ink2"]) - 2
        if st["name"] == "BED":
            yy = pg.para("REMOVE: Arundo donax (giant reed)", xa + 3, yy - 1, w - 6, 7, C["accent"], True)
            yy = pg.para("raises flood risk, blocks bridges", xa + 3, yy, w - 6, 7, C["accent"])
        # what we plant
        yy = min(yy, 66) - 2
        pg.text("WE PLANT " + cite(SPECIES) if st["name"] != "FARMS" else "THEY GROW", xa + 3, yy, 7, C["accent"], True); yy -= 4.5
        for sp, why in st["plant"]:
            pg.text(sp, xa + 3, yy, 8, C["ink"], True); yy -= 3.6
            yy = pg.para(why, xa + 3, yy, w - 6, 6.5, C["ink2"]) - 1.2
    pg.text("steps = planting bands " + cite(BANDS) + " · depths above the bed", x0, 109, 6.5, C["ink2"])
    pg.text("not to scale · Nil's flat end: Q100 1.4 m, Q500 1.5 m " + cite(DEPTH), x1, 109, 6.5, C["ink2"], align="R")
    pg.rect(14, 18, 392, 6, fill=C["paper"])
    icon(pg, "nose", 15.5, 23.6, 5.2)                 # v1.2: odour as a tag and keywords
    ox = 22.0
    for t, b in (("ODOUR: no measured plant effect " + cite(SPECIES), True), ("keep sewage out", False),
                 ("clean at the upstream end", False), ("plants: clean nutrients, give scent", False)):
        if ox > 22.0:
            pg.circle(ox - 3.0, 21.2, 0.7, fill=C["accent"])
        pg.text(t, ox, 20, 7.5, C["ink"], b); ox += text_w(t, 7.5, b) + 6.0
    footer(pg, CREDIT)
    return pg

# ------------------------------------------------------------------ build and run
def build(path):
    L, src = live()
    NET.clear(); NET.update(L["net"])
    write_pdf([page_cubic(L, src), page_farms(L, src), page_ladder(L, src)], path)
    return src

def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_PDF)
    try:
        src = build(path)
    except PermissionError:
        return "The PDF is open in another program. Close it and press again: " + path
    return "%s  %s\nfigures: %s\nagriculture alternatives %s, %.1f s" % (OUT_PDF, time.strftime("%H:%M:%S"), src, VERSION, time.time() - t0)

#@include ../common/chain_fire.py


#@include ../common/done_text.py


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    _pressed = any(v is True for k, v in list(globals().items()) if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done")) or \
        any(chain_fire(v, "bergama_agri_alt_log_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:   # 25 Oct: the error goes into the log panel, the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_agri_alt_log" + _ik] = write_log(_res)
        _sc.sticky["bergama_agri_alt_log_status" + _ik] = ("ERROR" if _sc.sticky["bergama_agri_alt_log" + _ik].startswith(("ERROR", "The PDF is open")) else time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky["bergama_agri_alt_log_done" + _ik] = done_text(True, not _sc.sticky["bergama_agri_alt_log_status" + _ik].startswith("ERROR"), time.time() - _t0)
    done = _sc.sticky.get("bergama_agri_alt_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_agri_alt_log" + _ik, "Press the Button to export to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "AgriCulture " + VERSION + " · " + _sc.sticky.get("bergama_agri_alt_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main()))
