# r: pymupdf==1.26.5
# bergama_agriculture_alternatives_v1_5.py · Thread 3 of the 22 Oct batch: three alternatives for the agriculture analysis
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Makes the folder Downloads/Bergama/output/Bergama_agriculture_alternatives by itself and saves ONE
# all-vector A3 PDF there, one page per alternative:
#   1 WHAT EACH CUBIC METRE GROWS   chart: hectares the stored water irrigates, per crop, normal and 1-in-5 dry year
#   2 THE FARMS WE FEED             the site board's plan 01 "What is there" at a round scale with the fields and orchards fed
#   3 ONE PLANT LADDER              hand-sketched section diagram: streambed to farm, water, what grows today, what we plant
# Storage, water to the farms and the farm areas are read on every run from the water balance script's output
# (bergama_water_balance), so they follow its cost cut-off; the fallback is the shared key-figures file (flagged).
# Notes for Aras: batch_2026-10-22/thread3_agriculture/NOTES.md.
import os, time, json, zlib, math

VERSION = "v1.5"
# v1.5 (Aras 26 Oct 07:06, review of the deck, p.33-34): page 2's map is the site board's own plan 01 ("What is there",
# board v42+, cut from its sheet PDF with PyMuPDF and scaled by one factor, never redrawn) at the largest round scale
# that fits, with only the farms layer drawn on it (fields and orchards fed, their extent), the plan's own key, the
# figures beside it and a context line; v1.4's land cover drawing stays only as a flagged fallback. Page 3's ladder is
# drawn by the proposal sections' sketch engine (the p.23 upstream entry's language): hand ground, washes, winter
# water and summer strip, the faint design-flood reach, level marks, sketch plants and people, rain and sun marks.
# The "# r: pymupdf" line installs PyMuPDF in Rhino 8 on the first run (as the booklet).
# v1.4 (Aras 25 Oct 21:47-22:02, booklet stage 3): the booklet shows crops of this sheet (booklet/CROP_SPEC.md):
# blocks.json lists one crop per panel of the three pages and results.json keeps v1.3's keys; the v1.3 booklet redraws
# are gone. Caveat notes taken off the sheet (labels kept); "stream", never "river". Page 3's ladder drawn in the site
# board's section language (src/common/section_style.py): cut ground with sloped banks, the strip hatched, whole plants,
# one size across and up.
# v1.3 (25 Oct, booklet stage 2, SCRIPT_STANDARD §8): also writes output/<folder>/booklet/: c7_hero.pdf (plant ladder +
# the water board's planting bands A-F), c8_b.pdf (hectares per crop bars), blocks.json (every word a label) and
# results.json (hectares per crop). The A3 sheet is unchanged.
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
DEFAULT_NOTE = "water balance default-lands copy, 24 Oct"   # v1.4: the log says when it is used

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

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"

#@include ../common/text_w.py

class Page:
    def __init__(self, w, h):
        self.w, self.h, self.ops, self.alphas = w, h, [], set()
    def _c(self, h, stroke=False):
        r, g, b = rgb(h); return "%.3f %.3f %.3f %s" % (r, g, b, "RG" if stroke else "rg")
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)
    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None, alpha=None):
        self.path([P], fill, stroke, lw, closed, dash, alpha)
    def path(self, rings, fill=None, stroke=None, lw=0.2, closed=True, dash=None, alpha=None):
        """several rings in one path; a fill uses even-odd, so holes stay open. v1.5: alpha = opacity 0-1 (sketch washes)"""
        k = 72 / 25.4; o = ["q"]
        if alpha is not None and alpha < 0.995:
            a_ = max(1, int(round(alpha * 100))); self.alphas.add(a_); o.append("/GA%d gs" % a_)
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
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", halo=None):
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        k = 72 / 25.4
        b = b"".join(bytes([_ENC_EXTRA[ch]]) if ch in _ENC_EXTRA else ch.encode("cp1252", "replace") for ch in s)   # 25 Oct: ı İ ğ Ğ ş Ş spelt right
        b = b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
        if halo:                                   # v1.5: the sketches' text mask, a halo in the ground's colour
            self.ops.append("q %s %.2f w 1 j BT 2 Tr /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET Q" % (
                self._c(halo, True), size * 0.35, "F2" if bold else "F1", size, self._c(halo), x * k, y * k, b.decode("latin-1")))
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
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding << /Type /Encoding /BaseEncoding /WinAnsiEncoding %s >> >>" % _DIFF,
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding << /Type /Encoding /BaseEncoding /WinAnsiEncoding %s >> >>" % _DIFF]
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
    for i, o in enumerate(objs):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (i + 1, o)).encode("latin-1")
    for i, pg in enumerate(pages):
        content = zlib.compress("\n".join(pg.ops).encode("latin-1"))
        offs.append(len(out))
        gs = "".join("/GA%d << /Type /ExtGState /ca %.2f /CA %.2f >> " % (a, a / 100.0, a / 100.0) for a in sorted(pg.alphas))
        out += ("%d 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.2f %.2f] /Resources << /Font << /F1 3 0 R /F2 4 0 R >>%s >> /Contents %d 0 R >>\nendobj\n"
                % (5 + 2 * i, pg.w * k, pg.h * k, (" /ExtGState << %s>>" % gs) if gs else "", 6 + 2 * i)).encode("latin-1")
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

def header(pg, n, title, sub, hole=None):
    del SRC_KEY[:]                                 # v1.2: each page numbers its own sources from [1]
    if hole:                                       # v1.5: a window left open for a plan placed under the page
        x0, y0, x1, y1 = hole
        pg.path([[(0, 0), (420, 0), (420, 297), (0, 297)], [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], fill=C["ground"])
    else:
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
    ("drip", "TODAY'S IRRIGATION ON THE FARMS", None, ["some Bergama growers moved to drip"], ITB),
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
           "so the mix stands in; water balance crops: %s" % (", ".join(L["crops"]) or "not set"))
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
    ag_crop("ag1_bars", 0, 13.0, y0 - len(rows) * 19.5 + 0.5, 277.0, y0 + 11.0,
            legend=[{"kind": "fill", "colour": C["green_light"], "label": "normal year"},
                    {"kind": "fill", "colour": C["green_deep"], "label": "1-in-5 dry year"},
                    {"kind": "line", "colour": C["accent"], "label": "farms we feed"}])
    ag_crop("ag1_headline", 0, 24.0, 239.0, 262.0, 261.0)
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
    ag_crop("ag1_reading", 0, 18.0, 33.0, 262.0, 81.0)
    # context column
    cx, cy = 280, 250
    pg.text("WHY CROP CHOICE IS THE LEVER", cx, cy, 11, C["ink"], True)
    yb_ = tiles(pg, cx, cy - 6, 126, CONTEXT)
    ag_crop("ag1_context", 0, cx - 1.0, yb_ - 1.0, cx + 127.0, cy - 5.0)
    pg.text("WHAT IT REPLACES", cx, 60, 9, C["accent"], True)
    yb_ = tiles(pg, cx, 57, 126, REPLACES)
    ag_crop("ag1_replaces", 0, cx - 1.0, yb_ - 1.0, cx + 127.0, 58.0)
    footer(pg, CREDIT)
    return pg

# ------------------------------------------------------------------ page 2: the farms we feed, on the site board's plan 01
# v1.5 (Aras 26 Oct 07:06, deck p.33): "build this map from the 'What is there' plan (p.02): same base, same palette and
# legend". The base is the site board's own plan 01, cut from its sheet PDF and scaled by one factor (never redrawn,
# never stretched; Aras 25 Oct 22:07); this page draws only the farms layer on it. The board (v42+) writes the plan's
# georeference into output/selinus_board/booklet/blocks.json. Without it (or without PyMuPDF) the page falls back to
# v1.4's land cover drawing in the same window, flagged on the page and in the log.
CLS = [("farmland", "Fields (cropland)", C["field"]), ("orchard", "Orchards", C["orchard"]),
       ("trees", "Tree cover", C["tree"]), ("shrub", "Shrubland", C["shrub"]), ("grass", "Grassland", C["grass"])]
BOARD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "selinus_board")
ROUND_DENS = (5000, 10000, 20000, 25000, 50000)    # Aras 26 Oct 06:35: round scales only, the largest that fits
FARM_WIN = (13.0, 20.0, 373.0, 262.0)              # the map window, page mm (x0, y0, x1, y1), y up
FARM_COL = 377.0                                   # the key column, x from here to 406
BASE = {}                                          # the plan 01 cut put under page 2 after write_pdf (put_base)
BASE_OFF = [False]                                 # True: draw the fallback (the base could not be placed)


def plan01_geo():
    """(plan dict, note) of the site board's plan 01: its sheet PDF, crop rect (mm from the sheet's top-left) and the
    survey -> sheet similarity a * w + b (complex, sheet mm with y up, from the four frame corners); (None, why) when
    it is missing."""
    if BASE_OFF[0]:
        return None, "the site board's plan could not be placed under the farms (see the log)"
    try:
        import fitz                                 # PyMuPDF (the "# r:" line at the top installs it in Rhino 8)
    except Exception:
        return None, "PyMuPDF missing: Rhino installs it from the '# r: pymupdf' line on the first run (needs internet)"
    try:
        with open(os.path.join(BOARD_DIR, "booklet", "blocks.json"), encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return None, "site board output not found (output/selinus_board/booklet/blocks.json): run the site board first"
    blk = next((v for k, v in sorted(d.get("blocks", {}).items()) if k.lower().endswith("_plan01") and v.get("geo")), None)
    if not blk:
        return None, "the site board output has no plan 01 georeference: run the site board v42 or later"
    nm, pdf = os.path.basename(blk.get("pdf", "")), None
    for dd, _, names in sorted(os.walk(BOARD_DIR)):
        if nm in names:
            pdf = os.path.join(dd, nm)
            break
    if not pdf:
        return None, "the site board sheet %s is not in %s" % (nm, BOARD_DIR)
    r = [float(v) for v in blk["rect_mm"]]
    W = [complex(g[0], g[1]) for g in blk["geo"]["points"]]
    Z = [complex(r[0] + g[2], -(r[1] + g[3])) for g in blk["geo"]["points"]]
    wm, zm = sum(W) / len(W), sum(Z) / len(Z)
    a = sum((z - zm) * (w - wm).conjugate() for w, z in zip(W, Z)) / sum(abs(w - wm) ** 2 for w in W)
    err = max(abs(a * (w - wm) + zm - z) for w, z in zip(W, Z))
    return (dict(pdf=pdf, page=int(blk.get("page", 0)), rect=r, a=a, b=zm - a * wm, err=err, legend=blk.get("legend") or []),
            "site board plan 01 of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(pdf))))


def key_sample(pg, kind, col, x, y):
    """a legend sample 4 x 2.4 mm, its top-left at (x, y): fill, line, dash, dot or outline"""
    if kind == "fill": pg.rect(x, y - 2.4, 4.0, 2.4, fill=col)
    elif kind == "dot": pg.circle(x + 2.0, y - 1.2, 0.8, fill=col)
    elif kind == "dash": pg.line([(x, y - 1.2), (x + 4.0, y - 1.2)], col, 0.4, (1.0, 0.6))
    elif kind == "outline": pg.rect(x + 0.2, y - 2.2, 3.6, 2.0, stroke=col, lw=0.35)
    elif kind == "outline2": pg.rect(x + 0.3, y - 2.1, 3.4, 1.8, stroke=col, lw=0.7)
    else: pg.line([(x, y - 1.2), (x + 4.0, y - 1.2)], col, 0.5)


def page_farms(L, src):
    pg = Page(420, 297)
    BASE.clear()
    G, gnote = plan01_geo()
    fed = [(key, poly) for key in ("farmland", "orchard") for side in ("out", "in") for poly in GEO["lc"][key][side]]
    F = GEO["frame"]
    rotu = G["a"] / abs(G["a"]) if G else complex(math.cos(-math.atan2(F[1][1] - F[0][1], F[1][0] - F[0][0])),
                                                  math.sin(-math.atan2(F[1][1] - F[0][1], F[1][0] - F[0][0])))
    Q = [complex(p[0], p[1]) * rotu for _, poly in fed for ring in poly for p in ring]   # the plan's own turn
    bx0, bx1 = min(q.real for q in Q), max(q.real for q in Q)
    by0, by1 = min(q.imag for q in Q), max(q.imag for q in Q)
    wx0, wy0, wx1, wy1 = FARM_WIN
    den = next((d_ for d_ in ROUND_DENS if (bx1 - bx0) * 1000.0 / d_ + 4.0 <= wx1 - wx0 and
                (by1 - by0) * 1000.0 / d_ + 4.0 <= wy1 - wy0), ROUND_DENS[-1])
    m = 1000.0 / den                              # page mm per metre
    c = rotu * m
    t = complex((wx0 + wx1) / 2.0, (wy0 + wy1) / 2.0) - complex((bx0 + bx1) / 2.0, (by0 + by1) / 2.0) * m

    def T(p):
        z = complex(p[0], p[1]) * c + t
        return (z.real, z.imag)
    hole = (wx0, wy0, wx1, wy1)
    if G:                                          # the window on the board's sheet, cut to plan 01's own crop
        kk = abs(G["a"]) / m

        def S(x, y):
            z = kk * (complex(x, y) - t) + G["b"]
            return z.real, -z.imag
        (sx0, sy1), (sx1, sy0) = S(wx0, wy0), S(wx1, wy1)
        r = G["rect"]
        cx0, cy0, cx1, cy1 = max(sx0, r[0]), max(sy0, r[1]), min(sx1, r[2]), min(sy1, r[3])
        if cx1 - cx0 > 20.0 * kk and cy1 - cy0 > 20.0 * kk:
            hole = (wx0 + (cx0 - sx0) / kk, wy0 + (sy1 - cy1) / kk, wx1 - (sx1 - cx1) / kk, wy1 - (cy0 - sy0) / kk)
            BASE.update(pdf=G["pdf"], page=G["page"], clip=(cx0, cy0, cx1, cy1), rect=hole, err=G["err"], den=den)
        else:
            G, gnote = None, "the farms lie outside the site board's plan 01"
    BASE["note"] = gnote
    header(pg, "2", "THE FARMS WE FEED", "Fields and orchards the stored water serves, on the site plan \"What is there\"",
           hole=hole if G else None)
    WC = "ESA WorldCover 2021 v200, 10 m (CC BY 4.0), data/landcover"
    ORCH = "orchards inferred from survey symbols SEMBOL_ZEYTINLIK / SEMBOL_MEYVA_BAH"
    EXT = "extent = around2.pdf registered to the survey (research/water_balance)"
    NEED2 = "need: FAO-56 soil balance / 0.90 drip, normal and 1-in-5 dry years"
    SRC2 = "farm areas from " + src
    PLAN = "base: site board plan 01 'What is there' (selinus_board, its own sheet PDF, cut and scaled, not redrawn)"
    # context line (review global rule 4): what it shows, why it is here, what to take from it
    pg.text("The site plan \"What is there\" with the fields and orchards our stored water serves outlined: the farms read "
            "off the same base, colours and key as the site " + cite(PLAN if G else WC),
            14, 265.5, 8.5, C["ink"])
    hx0, hy0, hx1, hy1 = hole
    if not G:                                      # fallback: v1.4's land cover drawing in the window, flagged
        A = GEO["around2"]
        pg.rect(wx0, wy0, wx1 - wx0, wy1 - wy0, fill=C["paper"])
        pg.path([[T(p) for p in A]], fill="E8E5DA")
        pg.path([[T(p) for p in GEO["frame"]]], fill="E8E5DA")
        for side in ("out", "in"):
            for key, lab, col in CLS[::-1]:
                for poly in GEO["lc"][key][side]:
                    pg.path([[T(p) for p in r] for r in poly], fill=col if (side == "out" or key in ("farmland", "orchard")) else "D9D6C8")
        for ln in GEO["streams"]: pg.line([T(p) for p in ln], C["water"], 0.5)
        for ln in GEO["selinos"]: pg.line([T(p) for p in ln], C["water_deep"], 1.1)
        pg.text("FLAG: " + gnote + " · land cover drawn from WorldCover instead", wx0 + 2, wy0 + 2, 7, C["accent"], True)
    # the farms layer: the extent, the fields and orchards we feed as outlines over the plan's own colours
    pg.poly([T(p) for p in GEO["around2"]], stroke=C["ink"], lw=0.35, closed=True, dash=(2.0, 1.2))
    for key, poly in fed:
        pg.path([[T(p) for p in r] for r in poly], stroke=C["accent"] if key == "farmland" else C["accent_deep"],
                lw=0.35 if key == "farmland" else 0.7)
    pg.rect(hx0, hy0, hx1 - hx0, hy1 - hy0, stroke=C["ink"], lw=0.25)
    # key column: north, scale, the farms layer with its figures, then plan 01's own key
    x, y = FARM_COL, 262.0
    north(pg, x + 6.0, y - 9.0, math.degrees(math.atan2(rotu.imag, rotu.real)), 5.0)
    bar = max(v for v in (50, 100, 200, 250, 500, 1000) if v * m <= 27.0)
    pg.rect(x, y - 21.0, bar * m / 2.0, 1.2, fill=C["ink"])
    pg.rect(x + bar * m / 2.0, y - 21.0, bar * m / 2.0, 1.2, stroke=C["ink"], lw=0.25)
    pg.text("0", x, y - 24.0, 6, C["ink"], align="C")
    pg.text("%d m" % bar, x + bar * m, y - 24.0, 6, C["ink"], align="R")
    pg.text("1:{:,} at A3".format(den), x, y - 27.5, 6.5, C["ink"], True)
    y -= 34.0
    fed_c, fed_o = L["cropland_ha"], L["orchard_ha"]
    o_lo = min(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    o_hi = max(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    cc = [c_ for c_ in L["crops"] if c_ in NET] or [c_ for c_ in NET if c_ != "olive"]
    c_lo = min(gross_m3_ha(c_, y_) for c_ in cc for y_ in ("normal", "dry"))
    c_hi = max(gross_m3_ha(c_, y_) for c_ in cc for y_ in ("normal", "dry"))
    f_in, f_out = GEO["area_ha"]["farmland"][1], GEO["area_ha"]["farmland"][0]
    pg.text("WE FEED", x, y, 8, C["accent"], True)
    y -= 3.0
    rows = [("outline", C["accent"], "fields " + cite(SRC2), "%s ha" % fmt1(fed_c),
             ["%s-%s m³ a season %s" % (fmt(rnd(fed_c * c_lo)), fmt(rnd(fed_c * c_hi)), cite(NEED2)),
              "as " + " / ".join(cc) + " " + cite(TUIK), "inside the site %s ha · outside %s ha %s" % (fmt1(f_in), fmt1(f_out), cite(WC))]),
            ("outline2", C["accent_deep"], "orchards " + cite(ORCH), "%s ha" % fmt1(fed_o),
             ["%s-%s m³ a season" % (fmt(rnd(fed_o * o_lo, 100)), fmt(rnd(fed_o * o_hi, 100))), "as olive"]),
            ("dash", C["ink"], "the extent they lie in " + cite(EXT), "%s ha" % fmt(L.get("extent_ha", 455.0)), [])]
    for kind, col, lab, big, lines in rows:
        key_sample(pg, kind, col, x, y)
        pg.text(lab, x + 5.5, y - 2.1, 6.5, C["ink"], True)
        y -= 7.0
        pg.text(big, x, y, 12, C["green_deep"], True)
        y -= 3.4
        for ln in lines:
            y = pg.para(ln, x, y, 29.0, 6, C["ink2"], lead=1.2)
        y -= 2.0
    pg.line([(x, y + 0.5), (406.0, y + 0.5)], C["faint"], 0.3)
    y -= 4.0
    if G:
        pg.text("THE SITE PLAN'S KEY", x, y, 7, C["ink"], True)
        y -= 2.5
        for it in G["legend"]:
            key_sample(pg, it.get("kind", "fill"), it.get("colour", "B0AC9C"), x, y)
            y = min(pg.para(it.get("label", ""), x + 5.5, y - 2.0, 23.5, 5.5, C["ink"], lead=1.15) + 0.3, y - 3.4)
    else:
        for key, lab, col in CLS:
            key_sample(pg, "fill", col, x, y)
            pg.text(lab, x + 5.5, y - 2.0, 5.5, C["ink"]); y -= 3.6
    ag_crop("ag2_plan", 1, 13.0, min(y, wy0) - 1.0, 407.0, 269.0, den)
    footer(pg, CREDIT)
    return pg


def put_base(path):
    """v1.5: the site board's plan 01 under page 2's farms layer, as the booklet places sheets (PyMuPDF
    show_pdf_page): the window cut from its sheet, one scale factor both ways. Returns a log line."""
    if not BASE.get("pdf"):
        return "farms map: FLAG fallback drawing, " + BASE.get("note", "")
    import fitz
    K = 72 / 25.4
    hx0, hy0, hx1, hy1 = BASE["rect"]
    cx0, cy0, cx1, cy1 = BASE["clip"]
    doc, src = fitz.open(path), fitz.open(BASE["pdf"])
    doc[1].show_pdf_page(fitz.Rect(hx0 * K, (297.0 - hy1) * K, hx1 * K, (297.0 - hy0) * K), src, BASE["page"],
                         clip=fitz.Rect(cx0 * K, cy0 * K, cx1 * K, cy1 * K), overlay=False)
    tmp = path + ".tmp"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close(); src.close()
    os.replace(tmp, path)
    return "farms map on %s at 1:{:,} (georeference fit {:.2f} mm)".format(BASE["den"], BASE["err"]) % BASE["note"]

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

# v1.5 (Aras 26 Oct 07:06, deck p.34: "develop the section further ... the hand-sketched, idea-explaining style of page
# 23"): the ladder is drawn by the same sketch engine as the proposal sections' upstream entry (p.23): hand ground with
# the cut poché, washes, the winter water and the summer strip, the design flood's faint reach, hand level lines,
# sketch reeds, shrubs, trees, lavender and olives, people, sun and rain marks. A diagram: one size across and up.
_SK = []
#@include ../common/_tree_rand.py
#@include ../common/sketch_engine.py
#@include ../common/xform.py
#@include ../bergama_proposal_sections/data/SKETCH_SRC.py

LAD_W = 200.0                        # sketch units across (5 steps of 40); printed x LAD_F on the page
LAD_F = 392.0 / LAD_W                # mm on the page per sketch unit, the same across and up
LAD_Y0 = 112.0                       # page y of the sketch's 0 (bottom of the cut ground)
LAD_GY = (16.0, 23.0, 31.0, 38.0, 45.0)   # ground of each step (bed, lower bank, terrace, bank top, farms), sketch units
LAD_Q100, LAD_Q500 = 39.5, 41.5      # over the bank top (the K4 / S4 case, README v1.1 line 49), under the farms


def sk_draw(pg, items):
    """sketch-engine page items (already placed with xform) on this script's Page"""
    for it in items:
        if it[0] == "poly":
            _, rings, fill, stroke, lw, dash, _st, alpha = it
            pg.path(rings, fill, stroke, lw, True, dash, alpha)
        elif it[0] == "line":
            _, pts, stroke, lw, dash, _cap = it
            pg.line(pts, stroke, lw, dash)
        elif it[0] == "text":
            _, s, x, y, h, col, bold, align, _m, halo = it
            pg.text(s, x, y, h / 0.3528, col, bool(bold), align or "L", halo)


def ladder_sketch():
    """The plant ladder in the p.23 sketch language: [(z, order, item)] in sketch units (0..LAD_W across)."""
    E = sketch_engine()
    E["FORM"] = "A"                                   # organic only where the project meets the water
    del E["ZP"][:]
    E["ORDER"][0] = 0
    o, w, gy = (0.0, 0.0), LAD_W / 5.0, LAD_GY
    g = [(0.0, 0.0), (0.0, gy[0])]
    for i in range(1, 5):
        xa = i * w
        if i == 1:                                    # the water's edge: the bank in form A (organic)
            g += E["bank"]((xa - 3.0, gy[0]), (xa + 3.0, gy[1]))
        else:                                         # elsewhere faceted, straight slopes
            g += [(xa - 2.0, gy[i - 1]), (xa + 2.0, gy[i])]
    g += [(LAD_W, gy[4]), (LAD_W, 0.0)]
    gs = E["sketch_ground"](o, E["notch"](g, [(13.0, 25.0, gy[0], 2.0)]))   # the summer strip's low-flow channel
    pc = E["under_level"](gs, 0.0, LAD_W, LAD_Q500)  # the design flood's reach (faint, as on p.23)
    if pc:
        E["wash"](o, pc, "flood", E["FLOOD_WASH"], E["FLOOD_ALPHA"])
    E["water_level"](o, gs, 19.0, gy[1] + 1.8, E["W_WIN"], bed_hatch=True)   # winter highs: bed + lower bank
    E["water_level"](o, gs, 19.0, gy[0] - 0.8, E["W_EXT"], line=False)       # the summer strip in its channel
    # plants by step (graphic sizes): reeds in the bed, rushes and shrubs on the lower bank, trees on the terrace,
    # lavender on the bank top, olives and a field crop on the farms
    E["reeds"](o, 2.0, 11.0, gy[0] - 0.2, 4.2)
    E["reeds"](o, 27.0, 35.0, gy[0] - 0.2, 4.2)
    x_ = w + 4.0
    while x_ < w + 18.0:                              # rushes: short hand tufts
        for d in (-0.5, 0.0, 0.5):
            E["sketch"](o, [(x_, gy[1]), (x_ + d * 0.9, gy[1] + 2.0 - abs(d))], "planting", E["REED"], E["LW_FINE"],
                        over=0.0, amp=0.03, retrace=False, z=E["Z_TREE"])
        x_ += 1.6
    for xs, hs, ws in ((w + 24.0, 5.0, 6.0), (w + 33.0, 4.2, 5.0)):   # shrubs: Tamarix, Salix (domes, washes)
        dome = [(xs + ws / 2.0 * math.cos(math.pi * i / 14.0), gy[1] + hs * math.sin(math.pi * i / 14.0) ** 0.7) for i in range(15)]
        E["wash"](o, dome, "planting", E["SITE_TREE"][1], 0.6, z=E["Z_TREE"])
        E["sketch"](o, dome, "planting", E["SITE_TREE"][2], E["LW_FINE"], closed=True, over=0.0, amp=0.12, retrace=False,
                    z=E["Z_TREE"])
    E["sketch_tree"](o, 2 * w + 10.0, gy[2], 16.0)
    E["sketch_tree"](o, 2 * w + 28.0, gy[2], 13.0)
    x_ = 3 * w + 4.0
    while x_ < 4 * w - 6.0:                           # lavender mounds with flower spikes
        mound = [(x_ + 1.2 * math.cos(math.pi * i / 10.0), gy[3] + 1.0 * math.sin(math.pi * i / 10.0)) for i in range(11)]
        E["wash"](o, mound, "planting", E["hx"](C["olive"]), 0.6, z=E["Z_TREE"])
        for d in (-0.5, 0.0, 0.5):
            E["sketch"](o, [(x_ + d, gy[3] + 0.8), (x_ + d * 1.3, gy[3] + 1.9)], "planting", E["hx"]("8E7CC3"), 0.3,
                        over=0.0, amp=0.02, retrace=False, z=E["Z_TREE"])
        x_ += 2.8
    for xs in (4 * w + 6.0, 4 * w + 16.0):            # olives
        E["sketch_tree"](o, xs, gy[4], 8.0)
    x_ = 4 * w + 25.0
    while x_ < LAD_W - 1.0:                           # field crop rows
        E["sketch"](o, [(x_, gy[4]), (x_, gy[4] + 1.6)], "planting", E["hx"](C["field"]), 0.35, over=0.0, amp=0.02,
                    retrace=False, z=E["Z_TREE"])
        x_ += 1.4
    E["sketch_person"](o, 2 * w + 19.0, gy[2], kind=1)                    # the terrace in summer: dry, shaded
    E["sketch_person"](o, 4 * w + 21.0, gy[4], kind=3)                    # on the farm
    E["sketch"](o, gs, "ground lines", E["SKINK"], E["PEN_BOLD"], z=E["Z_LINE"])   # the cut: the gesture
    # the design flood levels: hand dashed lines and level marks, over the bank top only at K4 / S4
    xe = 4 * w - 2.0 + 4.0 * (LAD_Q500 - gy[3]) / (gy[4] - gy[3])
    for lv, lab in ((LAD_Q500, "Q500 · 263 m³/s · 2.3-3.3 m above the bed " + cite(DEPTH)),
                    (LAD_Q100, "Q100 · 205 m³/s · 2.0-3.0 m")):
        E["sketch"](o, [(0.0, lv), (xe, lv)], "flood lines", E["HERITAGE"], E["PEN_FINE"], over=0.0, retrace=False,
                    dashed=True, z=E["Z_LINE"])
        E["level_mark"](o, 3 * w + 26.0 if lv == LAD_Q500 else 3 * w + 20.0, lv, E["HERITAGE"], "flood lines")
        E["text"](o, lab, 1.0, lv + (0.8 if lv == LAD_Q500 else -2.4), 3.6,
                  E["HERITAGE"], "flood")
    E["text"](o, "over the bank top only at K4 (right bank) and S4 (left)", 3 * w + 2.0, LAD_Q500 + 4.0, 3.4,
              E["HERITAGE"], "flood")
    E["keyed"](o, "winter", "winter highs", 1.0, gy[1] + 2.6, 4.0, E["W_EXT"], "water")
    E["keyed"](o, "summer", "strip", 13.0, gy[0] - 4.6, 3.6, E["W_EXT"], "water", mask=E["SEC_POCHE"])
    # the farms are watered from storage in summer: the one arrow (a logical link, not a decoration)
    E["hand_arrow"](o, (4 * w - 10.0, gy[4] + 15.0), (4 * w + 8.0, gy[4] + 10.5), E["SITE_WATER_D"], bend=-0.2)
    E["keyed"](o, "summer", "stored winter water", 4 * w - 32.0, gy[4] + 15.5, 4.0, E["W_EXT"], "water")
    # each step's water facts in the sky above it, a rain mark for winter, the sun for summer
    for i, st in enumerate(STEPS):
        yy = 72.0
        for t in st["water"]:
            t = t.replace("{reuse}", cite(REUSE))
            kind = "summer" if any(k_ in t for k_ in ("Jul", "Jun", "summer")) else \
                   ("winter" if any(k_ in t for k_ in ("Jan", "winter")) else None)
            for j, ln in enumerate(wrap(t, 3.8, w - 7.0)):
                if kind and j == 0:
                    E["keyed"](o, kind, ln, i * w + 0.5, yy, 3.8, E["INK"], "water")
                else:
                    E["text"](o, ln, i * w + 0.5 + 3.2, yy, 3.8, E["INK"], "water")
                yy -= 1.9
        # the step's name and what it is, in the cut ground under its surface
        top = gy[i] - (2.0 if i == 0 else 0.0) - 2.6
        E["text"](o, st["name"], i * w + (3.5 if i else 1.0), top, 5.0, E["SKINK"], "name", bold=True, mask=E["SEC_POCHE"])
        E["text"](o, st["sub"], i * w + (3.5 if i else 1.0), top - 2.4, 3.6, E["INK2"], "name", mask=E["SEC_POCHE"])
    E["text"](o, "wetter steps clean and hold the water,\ndrier steps shade, scent and feed", 1.0, 56.0, 6.0,
              E["SKINK"], "idea")
    return sorted(E["ZP"], key=lambda e: (e[0], e[1]))


def page_ladder(L, src):
    pg = Page(420, 297)
    header(pg, "3", "ONE PLANT LADDER, STREAMBED TO FIELD",
           "Every plant on one gradient: water, today's cover, job")
    pg.text("One cut from the streambed to the farms: each planting step sits where the water reaches it, so what grows "
            "there follows how often it is wet " + cite(BANDS), 14, 265.5, 8.5, C["ink"])
    n = len(STEPS); x0, x1 = 14, 406; w = (x1 - x0) / n
    sk_draw(pg, xform([it for _, _, it in ladder_sketch()], LAD_F, x0, LAD_Y0))
    for i, st in enumerate(STEPS):
        xa = x0 + i * w
        # job tag in the cut ground
        pg.rect(xa + 3, 116, text_w(st["job"], 8, True) + 4, 5.5, fill=C["accent"])
        pg.text(st["job"], xa + 5, 117.6, 8, C["white"], True)
        jx = xa + 3 + text_w(st["job"], 8, True) + 6                # v1.2: the job as pictograms beside the tag
        for word, kind in JOB_ICON:
            if word in st["job"]:
                pg.rect(jx, 115.6, 6.5, 6.5, fill=C["paper"]); icon(pg, kind, jx + 0.5, 121.6, 5.5); jx += 7.5
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
        if st["name"] == "BED":
            yy = pg.para("REMOVE: Arundo donax (giant reed)", xa + 3, yy - 1, w - 6, 7, C["accent"], True)
            yy = pg.para("raises flood risk, blocks bridges", xa + 3, yy, w - 6, 7, C["accent"])
        # what we plant
        yy = min(yy, 66) - 2
        pg.text("WE PLANT " + cite(SPECIES) if st["name"] != "FARMS" else "THEY GROW", xa + 3, yy, 7, C["accent"], True); yy -= 4.5
        for sp, why in st["plant"]:
            pg.text(sp, xa + 3, yy, 8, C["ink"], True); yy -= 3.6
            yy = pg.para(why, xa + 3, yy, w - 6, 6.5, C["ink2"]) - 1.2
    pg.text("steps = planting bands " + cite(BANDS) + " · depths above the bed · a diagram, not to scale", x0, 108.5, 6.5, C["ink2"])
    pg.text("Nil's flat end: Q100 1.4 m, Q500 1.5 m " + cite(DEPTH), x1, 108.5, 6.5, C["ink2"], align="R")
    ag_crop("ag3_ladder", 2, x0 - 1.0, 107.0, x1 + 1.0, 269.0, drop=[r"^steps = planting bands", r"^Nil's flat end"])
    ag_crop("ag3_plants", 2, x0 - 1.0, 26.0, x1 + 1.0, 106.0)
    pg.rect(14, 18, 392, 6, fill=C["paper"])
    icon(pg, "nose", 15.5, 23.6, 5.2)                 # v1.2: odour as a tag and keywords
    ox = 22.0
    for t, b in (("ODOUR: no measured plant effect " + cite(SPECIES), True), ("keep sewage out", False),
                 ("clean at the upstream end", False), ("plants: clean nutrients, give scent", False)):
        if ox > 22.0:
            pg.circle(ox - 3.0, 21.2, 0.7, fill=C["accent"])
        pg.text(t, ox, 20, 7.5, C["ink"], b); ox += text_w(t, 7.5, b) + 6.0
    ag_crop("ag3_odour", 2, 13.0, 17.0, 407.0, 25.0)
    footer(pg, CREDIT)
    return pg

# ------------------------------------------------------------------ v1.4: A3 booklet = crops of this sheet (booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own drawings. Each page function records its panels' rects
# (from the same numbers it lays them out with) in AG_CROPS; booklet_export writes them to blocks.json, with
# booklet/results.json (hectares per crop, same keys as v1.3). The v1.3 booklet redraws are gone.
#@include ../common/booklet_assets.py
AG_CROPS = []                        # (id, page index, (x0, y0, x1, y1) mm from the page's top-left, y down, den, legend, drop)
AG_CAPTIONS = {"ag1_headline": "Storage and water to the farms", "ag1_bars": "Hectares one storage irrigates, by crop",
               "ag1_reading": "Same storage: how much more land", "ag1_context": "Why crop choice is the lever",
               "ag1_replaces": "What it replaces", "ag2_plan": "The farms we feed, on the site plan",
               "ag3_ladder": "One plant ladder, streambed to field", "ag3_plants": "Today's cover and what we plant",
               "ag3_odour": "Odour"}


def ag_crop(cid, page, x0, y0, x1, y1, den=None, legend=None, drop=None):
    """a panel of page `page` (0-2), given as the page's own y-up mm (x0, y0)-(x1, y1)"""
    AG_CROPS.append((cid, page, (round(x0, 2), round(297.0 - y1, 2), round(x1, 2), round(297.0 - y0, 2)), den,
                     legend or [], drop or []))


def ha_results(L):
    """hectares the storage irrigates per crop (page 1's bars): normal year and 1-in-5 dry year, lo-hi over the storage
    span (and the deficit saving range for olive), plus the dry-year ratio olive deficit / cotton."""
    p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0
    rows = [("olive_deficit", "olive", DEFICIT), ("olive_full", "olive", None)] + \
           [(c, c, None) for c in ("maize", "tomato", "cotton") if c in NET]
    out = {}
    for key, crop, dfc in rows:
        if crop not in NET: continue
        out[key] = {}
        for yr, yk in (("normal", "normal"), ("dry", "dry5")):
            g = gross_m3_ha(crop, yr)
            lo, hi = (w_lo / (g * (1 - dfc[0])), w_hi / (g * (1 - dfc[1]))) if dfc else (w_lo / g, w_hi / g)
            out[key][yk] = {"lo": round(lo, 1), "hi": round(hi, 1), "m3_per_ha": round(g, 0)}
    R = {"ha_per_crop": out, "to_farms_dry5_m3": [round(w_lo), round(w_hi)],
         "farms_fed_ha": round(L["cropland_ha"] + L["orchard_ha"], 2)}
    if "olive_deficit" in out and "cotton" in out:
        a, b = out["olive_deficit"]["dry5"], out["cotton"]["dry5"]
        R["ratio_olive_deficit_vs_cotton_dry5"] = {"lo": round(a["lo"] / b["lo"], 2), "hi": round(a["hi"] / b["hi"], 2)}
    return R


def booklet_export(L):
    """blocks.json: one crop per panel of the A3 sheet; results.json: hectares per crop. Returns a log line."""
    bk = BkBlocks(OUT_DIR, "AgriCulture", VERSION)
    for cid, page, r, den, legend, drop in AG_CROPS:
        bk.crop(cid, OUT_PDF, r, caption=AG_CAPTIONS.get(cid, ""), scale_den=den, legend=legend, page=page, drop=drop)
    bk.save()
    R = ha_results(L)
    R.update(script="AgriCulture", version=VERSION)
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    return "booklet: %d crops, results.json" % len(AG_CROPS)

# ------------------------------------------------------------------ build and run
def build(path):
    BASE_OFF[0] = False
    L, src = live()
    NET.clear(); NET.update(L["net"])
    for _ in range(2):
        del AG_CROPS[:]
        write_pdf([page_cubic(L, src), page_farms(L, src), page_ladder(L, src)], path)
        try:                                       # v1.5: the site board's plan 01 under the farms layer
            return src, put_base(path)
        except PermissionError:
            raise
        except Exception as ex:                    # never an empty window: once more with the fallback drawing
            BASE_OFF[0] = True
            err = "farms map: FLAG the site plan could not be placed (%s: %s), fallback drawing" % (type(ex).__name__, ex)
    return src, err

def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_PDF)
    try:
        src, base = build(path)
    except PermissionError:
        return "The PDF is open in another program. Close it and press again: " + path
    try:                                           # v1.3: the A3 booklet frames; an error here never breaks the sheet
        bk = booklet_export(live()[0])
    except Exception as ex:
        bk = "booklet ERROR (sheet saved): %s: %s" % (type(ex).__name__, ex)
    flag = "\nFLAG: water balance results file not found in Downloads; its default-lands copy was used" if src == DEFAULT_NOTE else ""
    return "%s  %s\nfigures: %s%s\n%s\nagriculture alternatives %s, %.1f s\n%s" % (OUT_PDF, time.strftime("%H:%M:%S"), src, flag, base, VERSION, time.time() - t0, bk)

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
