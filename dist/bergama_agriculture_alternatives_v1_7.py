# r: pymupdf==1.26.5
# bergama_agriculture_alternatives_v1_7.py · Thread 3 of the 22 Oct batch: three alternatives for the agriculture analysis
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Makes the folder Downloads/Bergama/output/Bergama_agriculture_alternatives by itself and saves ONE
# all-vector A3 PDF there, one page per alternative:
#   1 WHAT EACH CUBIC METRE GROWS   chart: hectares the stored water irrigates, per crop, normal and 1-in-5 dry year
#   2 THE FARMS WE FEED             the site board's plan 01 "What is there" at a round scale with the fields and orchards fed
#   3 ONE PLANT LADDER              the one-way chain and its programme; the ladder by season: water, what people do, plants
#   4 SOURCES                       the numbered key of the [n] marks on pages 1-3
# Storage, water to the farms and the farm areas are read on every run from the water balance script's output
# (bergama_water_balance), so they follow its cost cut-off; the fallback is the shared key-figures file (flagged).
# Notes for Aras: batch_2026-10-22/thread3_agriculture/NOTES.md.
import os, time, json, zlib, math

VERSION = "v1.7"
# v1.7 (bugfix, Aras 27 Oct 16:05): page 3 crashed ("too many values to unpack": the sketch engine's items now
# carry a 4th value, the label group); the text under the component shows a newly pasted version at once, idle.
# v1.6 (Aras 27 Oct 11:07, booklet p24-26; revision_2026-10-27/PHASE2_SPEC.md): white pages (the beige paper goes); no
# source footers or credit lines on the pages: the [n] marks are numbered once for the sheet and their key is a 4th
# page "Sources" (the booklet's sources page reads it there). Page 1 adds "why the stored water goes to farms": a
# cotton / olive timeline in card h01's words and years, labels placed by measured width. Page 3 rebuilt for option A:
# the one-way chain upstream entry -> K4 -> K3 -> İstiklal -> K5 -> K6 -> downstream -> farmland outside the site,
# hubs and in-bed sub-hubs, programme and historic roots; the ladder drawn three times (high water, low water, olive
# harvest) with what people do on each step; the species under each step. Every label is placed by a collision check
# (Placer): a label with no free place is left out and named in the log.
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
# ---- Bergama folders (Aras 24 Oct 08:28 + 27 Oct 11:07; SCRIPT_STANDARD §9). Every script uses ONLY these. ----
#   Downloads/Bergama/output/<name>/          final PDFs only
#   Downloads/Bergama/logs/                    every log file and log folder
#   Downloads/Bergama/cached/<name>/           caches, results other scripts read, any other working file
#   Downloads/Bergama/cached/booklet/<name>/   the script's booklet assets (blocks.json, results, images);
#                                              the booklet's own leftovers in cached/booklet/
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_booklet(name):
    return os.path.join(BERGAMA_ROOT, "cached", "booklet", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


def bg_first(paths):
    """The first path that exists (new place first, then where older versions wrote it), else the first."""
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[0]


def bg_tidy_output(name, cache_dir=None):
    """output/<name>/ keeps PDFs only: log files and anything in a log folder move to logs/<name>/, every other
    non-PDF file to cached/<name>/from_output/ (or cache_dir: the booklet uses cached/booklet/; moved, never deleted;
    same sub-folders). Empty folders go.
    Returns short log lines (counts, not one line per file)."""
    import shutil as _sh
    root, moved, fail = bg_output(name), {}, []
    if not os.path.isdir(root):
        return []
    for d, subs, files in os.walk(root, topdown=False):
        rel = os.path.relpath(d, root)
        rel = "" if rel == "." else rel
        for fn in files:
            if fn.lower().endswith(".pdf"):
                continue
            is_log = "log" in fn.lower() or any("log" in p.lower() for p in rel.split(os.sep) if p)
            dst = os.path.join(bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output")), rel, fn)
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(dst):
                    os.remove(dst)
                _sh.move(os.path.join(d, fn), dst)
                top = bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output"))
                moved[top] = moved.get(top, 0) + 1
            except Exception as ex:
                fail.append(u"%s (%s)" % (os.path.join(rel, fn), type(ex).__name__))
        if d != root:
            try:
                os.rmdir(d)                       # only when empty
            except Exception:
                pass
    return ([u"output/%s: %d non-PDF file(s) moved to %s" % (name, n, d) for d, n in sorted(moved.items())] +
            ([u"output/%s: could not move %s" % (name, ", ".join(fail[:5]))] if fail else []))
LOG_DIR = bg_logs()                        # Aras 25 Oct 09:34-09:35: every script's log here


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, "bergama_agriculture_alternatives_log.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text

# v1 24 Oct: all files under Downloads/Bergama/ (Aras rule)
OUT_DIR = bg_output("Bergama_agriculture_alternatives")       # final PDFs only (27 Oct)
OUT_PDF = "Bergama_agriculture_alternatives_A3.pdf"
# built-in geometry and tables (survey coordinates, m): around2 extent, site frame, WorldCover classes clipped to the
# extent (outside / inside the site), Selinos and other streams, FAO-56 net irrigation per water year (C1), corridor cover
def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_agriculture_alternatives_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_agriculture_alternatives_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_agriculture_alternatives_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'GEO': '8db5c86b0c11c98efb00cbe4dffb2aff', 'STEPS': 'f93b7721014f77d23de683007261e984', 'SKETCH_SRC': 'be6387ed413e463564bc894cacde2764'}.get(name):
        raise RuntimeError("Data file bergama_agriculture_alternatives_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_agriculture_alternatives_data.py:" + name, "exec"), globals())


bergama_data("GEO")

# ------------------------------------------------------------------ live numbers from the water balance (Thread 2)
# The water balance script writes its results on every run; this script reads them, so storage and the share covered
# are never typed in here. Searched in this order; the first file found wins.
LIVE_FILES = [os.path.join(bg_cache("Bergama_water_balance_analysis"), "water_balance_results.json"),   # 27 Oct: cached/
              os.path.join(bg_output("Bergama_water_balance_analysis"), "water_balance_results.json"),  # v2.6 and older
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

def rgb(h): return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"

def text_w(s, size, bold=False):
    w = sum(_HW[ord(ch) - 32] if 32 <= ord(ch) < 127 else 556 for ch in s)
    return w / 1000.0 * size * (1.06 if bold else 1.0) * 0.3528      # size in pt -> width in mm

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
def fmt(v): return "{:,.0f}".format(v)
def fmt1(v): return "{:,.1f}".format(v)
def rnd(v, step=1000): return int(round(v / step) * step)
EFF = 0.90          # drip application efficiency, as the water balance (key figures "basis": "drip 90 %")

NET = {}            # net irrigation mm per crop from the water balance results (mean, dry5 = 1-in-5 dry year), set in build()

def gross_m3_ha(crop, year):
    if crop == "mix":                  # field crops weighted by their 2025 Bergama areas
        w = {c: TUIK_2025_DA[c] for c in ("cotton", "maize", "tomato") if c in NET}
        return sum(gross_m3_ha(c, year) * v for c, v in w.items()) / sum(w.values())
    return NET[crop]["mean" if year == "normal" else "dry5"] / EFF * 10.0     # 1 mm on 1 ha = 10 m3

SRC_KEY = []          # v1.6: sources printed as [n] on pages 1-3, numbered once for the sheet; the key is page 4
LOG_NOTES = []        # v1.6: what the layout left out (log)

def cite(src):
    """v1.2 (water board v1.6 method): the number of a source in the sheet's key (v1.6: page 4), as "[n]"."""
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
    if hole:                                       # v1.5: a window left open for a plan placed under the page
        x0, y0, x1, y1 = hole
        pg.path([[(0, 0), (420, 0), (420, 297), (0, 297)], [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], fill=C["white"])
    else:                                          # v1.6 (Aras 27 Oct): white, the beige paper goes
        pg.rect(0, 0, 420, 297, fill=C["white"])
    pg.text(n, 14, 279, 22, C["accent"], True)
    pg.text(title, 26, 279, 22, C["ink"], True)
    pg.text(sub, 26, 271.5, 11, C["ink2"])
    pg.text("AGRICULTURE ANALYSIS · GROUP 6", 406, 281, 7, C["ink2"], True, "R")

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
            pg.rect(tx, yy - rh, tw, rh, fill=fill or C["white"], stroke=C["faint"], lw=0.2)
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

COTTON_H = ("h01 §3 'Then vs now', cotton / textiles: \"Tersane cotton (16th c.); ginning 1861; Sümerbank (1954/60–2008)\" "
            "(s18, s106; library/research/selinos_bergama_history_context_v1.md line 111)")
OLIVE_H = ("h01 §2 + §5 P04: \"19th-c. olive-oil machinery in the Red Hall S rotunda\" (s25; "
           "selinos_bergama_history_context_v1.md lines 77, 139)")
# v1.6 (Aras 27 Oct, p24 + spec §3): the farm history behind the farms the water serves, as a timeline, in the
# card's own words and years (h01 §3 line 111, §2 line 77, §5 P04 line 139); today's areas from TÜİK 2025 (above)
HISTORY = [("cotton", "Tersane cotton (16th c.)", 1500, 1600, COTTON_H),
           ("cotton", "ginning 1861", 1861, None, COTTON_H),
           ("cotton", "Sümerbank (1954/60–2008)", 1954, 2008, COTTON_H),
           ("cotton", "2025: %s ha" % fmt(rnd(TUIK_2025_DA["cotton"] / 10.0, 100)), 2025, None, TUIK),
           ("olive", "19th-c. olive-oil machinery · Red Hall S rotunda", 1800, 1900, OLIVE_H),
           ("olive", "2025: %s ha" % fmt(rnd(TUIK_2025_DA["olive"] / 10.0, 100)), 2025, None, TUIK)]


def history_line(pg, x, top, w, floor):
    """a timeline 1500-2030 with the cotton (above) and olive (below) history, labels placed by measured width (no
    overlaps). Left out (and logged) when it does not fit above `floor`. Returns its bottom y or None."""
    if top - 35.0 < floor:
        LOG_NOTES.append("p1 history timeline left out: no room above the 'what it replaces' tile")
        return None
    P = Placer()
    P.text(pg, "WHY THE STORED WATER GOES TO FARMS", x, top, 9, C["accent"], True)
    P.text(pg, "Bergama's cotton and olives", x, top - 3.8, 7.5, C["ink"])
    ya = top - 20.0
    X = lambda yr: x + 2.0 + (w - 4.0) * (yr - 1500) / 530.0
    pg.line([(X(1500), ya), (X(2030), ya)], C["ink"], 0.3)
    for yr in range(1500, 2001, 100):
        pg.line([(X(yr), ya - 0.8), (X(yr), ya + 0.8)], C["ink"], 0.3)
        P.text(pg, str(yr), X(yr) - text_w(str(yr), 7) / 2.0, ya - 3.6, 7, C["ink2"])
    reg = (x, ya - 15.0, x + w, top - 5.5)
    for lane, lab, a, b, ref in HISTORY:
        col, up = (C["accent"], True) if lane == "cotton" else (C["green_deep"], False)
        yb = ya + (1.0 if up else -1.0)
        if b:
            if lab.startswith("Sümerbank"):           # 1954 vs 1960 (card: conflicting dates): dashed until 1960
                pg.line([(X(1954), yb), (X(1960), yb)], col, 1.0, (0.6, 0.4))
                pg.line([(X(1960), yb), (X(2008), yb)], col, 1.0)
            else:
                pg.line([(X(a), yb), (X(b), yb)], col, 1.0)
        else:
            pg.circle(X(a), yb, 0.8, fill=col)
        if P.put(pg, lab + " " + cite(ref), X((a + b) / 2.0 if b else a), yb + (0.6 if up else -0.6), 7, col, False, region=reg,
                 gap=2.0, up=up, lanes=4, lead_col=col, stick=True) is None:
            LOG_NOTES.append("p1 history label left out (no free place): " + lab)
    return ya - 15.0


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
            pg.text("Bergama 2025: %s ha %s" % (fmt(TUIK_2025_DA[crop] / 10.0), cite(TUIK)), x0 - 3, yy - 13.6, 7, C["accent"], align="R")
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
        mk = cite(NET_REF) + (cite(TAGEM) if i == 0 else "") + (cite(KAYA) if d else "") + (cite(MIX) if crop == "mix" else "")
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
    pg.rect(14, 32, 250, 60, stroke=C["faint"], lw=0.3)       # v1.6: white page, the box only outlined
    pg.text("THE READING", 20, 84, 10, C["accent"], True)
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
    hb = history_line(pg, cx, yb_ - 7.0, 126.0, 64.0)          # v1.6: why the stored water goes to farms
    if hb:
        ag_crop("ag1_history", 0, cx - 1.0, hb - 1.0, cx + 127.0, yb_ - 3.0)
    pg.text("WHAT IT REPLACES", cx, 60, 9, C["accent"], True)
    yb_ = tiles(pg, cx, 57, 126, REPLACES)
    ag_crop("ag1_replaces", 0, cx - 1.0, yb_ - 1.0, cx + 127.0, 58.0)
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
        with open(bg_first([os.path.join(bg_booklet("selinus_board"), "blocks.json"),        # board v44+
                            os.path.join(BOARD_DIR, "booklet", "blocks.json")]), encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return None, "site board output not found (cached/booklet/selinus_board/blocks.json): run the site board first"
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

# ------------------------------------------------------------------ page 3: one plant ladder, streambed to field
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
# v1.6 (Aras 27 Oct 11:07, p26 "update to match the current project ... how the program changes people's
# interactions"): the programme of option A and its historic roots, each from the project's own record
CHAIN_REF = ("option A water chain: one way, cleaned once upstream in the reed basins, held in the terrace cascade, "
             "summer strip from storage, surplus to existing farmland outside the site (proposal sections v6, "
             "masterplan v23 detail notes)")
PROG = ("MIRAQUA programme and its historic roots: hubs at the Roman bridges K3, K4, K5 (H1) with floodable in-bed "
        "sub-hubs, hidden-stream square at İstiklal Meydanı (H2), tanning reach at K3 (H3), Tabaklar Hamamı at K4 (H4), "
        "Late Antique workshops downstream (H7), plane-tree squares (D8): history decisions D1-D12 / H1-H7, "
        "revision 27 Oct PHASE2_SPEC §3 (cards h01 §5, h02 §5, t02)")
GARDEN = ("card i01: Demeter's Garden (Begüm's page, 25 Oct): Demeter 'the ancient symbol of abundance'; olives; "
          "summer farm-to-table use; winter herbs and greens; seasonal production, education; south-west bank at K5")
KERMES = "h01 §2.8: Kermes first 1937 (s100, s60); 90th edition 29.06-05.07.2026 (s60); in the low-water season"
WB_YEAR = ("water board v1.13, S4 season rows: storage fills (winter), full by end of April (spring), low until the "
           "rains (autumn); reeds gold, seed heads; first-flush cleaning")
HARVEST = ("olive harvest month: Kaya et al. 2017, Memecik trees hand-harvested 6 Nov 2008, 10 Nov 2009, 14 Nov 2010 "
           "(library/research/crops_2026-10-24/bergama_crops_irrigation_v1.md §4.19)")
JOB_ICON = [("CLEAN", "clean"), ("HOLD", "hold"), ("SHADE", "shade"), ("SCENT", "scent"), ("HARVEST", "olive")]   # v1.2 job pictograms
bergama_data("STEPS")
# v1.6: the bank top as the project has it now (kept here so the Data file stays the v1.5 one): hub squares with plane
# trees at the bridges (spec §3 D8; water board band E) and Demeter's Garden's olives at K5 (card i01; olive "will not
# tolerate waterlogged soils", DATA_REGISTER PL-11)
STEPS[3].update(sub="hub squares at the bridges · Demeter's Garden at K5", job="SHADE + SCENT",
                plant=[("Platanus orientalis", "hub squares: Ottoman squares with plane trees (D8)")] + STEPS[3]["plant"] +
                      [("Olive", "Demeter's Garden (K5): dry top only, no waterlogged soil")])


class Placer:
    """v1.6 (spec §2: no text on another text): every label's box is measured with text_w and kept; a new label takes
    the first free place over its anchor, lane by lane upwards (or downwards), left-, centre- or right-aligned on the
    anchor, inside its region; lifted labels get a hair leader down to the anchor. No free place: the label is left
    out and named in the log (never drawn over another)."""
    def __init__(self):
        self.boxes, self.dropped = [], []

    def free(self, b):
        return all(b[2] <= q[0] or b[0] >= q[2] or b[3] <= q[1] or b[1] >= q[3] for q in self.boxes)

    def box(self, s, x, y, size, bold):
        h = size * 0.3528
        return (x - 0.5, y - 0.28 * h - 0.4, x + text_w(s, size, bold) + 0.5, y + 0.8 * h + 0.4)

    def text(self, pg, s, x, y, size, col, bold=False, halo=None):
        """a fixed label (titles, columns): drawn and blocked"""
        self.boxes.append(self.box(s, x, y, size, bold))
        pg.text(s, x, y, size, col, bold, halo=halo)

    def put(self, pg, s, ax, ay, size, col, bold=False, region=None, gap=1.4, up=True, lanes=9, halo="FFFFFF",
            lead_col=None, stick=False):
        w, lane = text_w(s, size, bold), size * 0.3528 * 1.45
        for k in range(lanes):
            y = ay + (gap + k * lane if up else -gap - size * 0.3528 - k * lane)
            for x in (ax - 0.6, ax - w / 2.0, ax - w + 0.6):
                b = self.box(s, x, y, size, bold)
                if region and (b[0] < region[0] or b[2] > region[2] or b[1] < region[1] or b[3] > region[3]):
                    continue
                if not self.free(b):
                    continue
                end = b[1] + 0.3 if up else b[3] - 0.3
                seg = (ax - 0.25, min(ay, end), ax + 0.25, max(ay, end))
                lead = bool(k) or stick
                if lead and not self.free(seg):
                    continue                           # the leader would cross another label
                self.boxes.append(b)
                if lead:
                    pg.line([(ax, ay), (ax, end)], lead_col or C["ink2"], 0.15)
                    self.boxes.append(seg)
                pg.text(s, x, y, size, col, bold, halo=halo)
                return x, y
        self.dropped.append(s)
        return None


# v1.6: the ladder is drawn three times, one row a season (as the water board's season pages): the same cut, the
# season's water, and what people do on each step, by the proposal sections' sketch engine (p.23 language: hand
# ground, washes, people). A diagram: one size across and up; heights not to scale.
_SK = []
def _tree_rand(x, y):
    """A small repeatable random stream from the tree's position (the same in every Python)."""
    s = [(int(round(x * 100.0)) * 73856093 ^ int(round(y * 100.0)) * 19349663) & 0x7FFFFFFF or 1]

    def nxt():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7FFFFFFF
        return s[0] / 2147483648.0
    return nxt
def sketch_engine():
    if not _SK:
        ns = {"__name__": "pr1_sketches", "_tree_rand": _tree_rand}   # reeds use the trees' random stream
        exec(compile(SKETCH_SRC, "pr1_sketches", "exec"), ns)
        _SK.append(ns)
    return _SK[0]
def xform(items, s, dx, dy):
    """The items scaled by s about the origin, then moved by (dx, dy)."""
    def T(p):
        return (dx + s * p[0], dy + s * p[1])
    out = []
    for it in items:
        k = it[0]
        if k == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            st = (stripes[0], stripes[1] * s, stripes[2] * s) + tuple(stripes[3:]) if stripes else None
            out.append(("poly", [[T(p) for p in r] for r in rings], fill, stroke, lw * s,
                        [d * s for d in dash] if dash else dash, st, alpha))
        elif k == "line":
            _, pts, stroke, lw, dash, cap = it
            out.append(("line", [T(p) for p in pts], stroke, lw * s, [d * s for d in dash] if dash else dash, cap))
        elif k == "circle":
            _, cx, cy, r, fill, stroke, lw = it
            out.append(("circle", dx + s * cx, dy + s * cy, r * s, fill, stroke, lw * s))
        elif k == "text":
            _, t, x, y, size, color, bold, align, mat, halo = it
            out.append(("text", t, dx + s * x, dy + s * y, size * s, color, bold, align, mat, halo))
    return out
bergama_data("SKETCH_SRC")

LAD_W = 200.0                        # sketch units across: 5 steps of 40
LAD_S = LAD_W / 5.0
LAD_X0, LAD_X1 = 106.0, 406.0        # the cut on the page, mm (left of it: the season column)
LAD_F = (LAD_X1 - LAD_X0) / LAD_W    # mm a sketch unit, the same across and up
LAD_GB = 12.0                        # the bottom of the cut ground, sketch units
LAD_GY = (16.0, 21.0, 26.0, 30.0, 33.0)   # ground of each step (bed, lower bank, terrace, bank top, farms)
LAD_Q100, LAD_Q500 = 30.8, 31.6      # over the bank top only at K4 / S4 (README v1.1 line 49), under the farms
ROW_H = 52.0                         # mm a season row
SUBHUB = (27.0, 36.0)                # the floodable sub-hub in the bed (spec §3 D2/D3/D10), sketch x
HUB = (3 * LAD_S + 2.0, 3 * LAD_S + 17.0)   # the dry hub square on the bank top at the bridges (D2), sketch x
SIT_FIG = [(-0.14, 0.0), (0.30, 0.0), (0.30, -0.42), (0.42, -0.42), (0.42, 0.13), (0.10, 0.14), (0.12, 0.62),
           (0.05, 0.70), (-0.10, 0.70), (-0.17, 0.58)]   # a seated figure (m, as the board's SA_FIGS), seat at (0, 0)


def _bed(i):
    """the bed's water from STEPS (research/rain_river_levels): 0 = Jul-Sep, 1 = Jan-Apr"""
    return STEPS[0]["water"][i].split(": ", 1)[1]


# the season rows: what the water does (left column) and what people do where (on the cut). acts: (figure kind or
# "sit" / None, sketch x, sketch y, flip, label, source). Sources: STEPS (water), spec §3 (programme), card i01
# (garden), h01 (Kermes), Kaya 2017 (olive harvest), the water board's season words.
def seasons():
    g0, g1, g2, g3, g4 = LAD_GY
    return [
        dict(key="high", name="HIGH WATER", months="Jan-Apr", mark="winter",
             side=[("bed " + _bed(1) + " deep", DEPTH), ("lower bank under water", None), ("sub-hubs closed", PROG),
                   ("storage fills", WB_YEAR)],
             acts=[("sit", 2 * LAD_S + 1.0, g2, True, "sit at the edge · watch the water", PROG),
                   (0, HUB[0] + 4.0, g3, False, "hub square: dry, step-free", PROG),
                   (2, HUB[0] + 8.5, g3, True, None, None),
                   (None, sum(SUBHUB) / 2.0, g1 + 1.8, False, "sub-hub under water: closed", PROG)]),
        dict(key="low", name="LOW WATER", months="Jul-Sep", mark="summer",
             side=[("bed " + _bed(0), DEPTH), ("strip 0.30 m all summer (design)", None), ("sub-hubs open", PROG),
                   (STEPS[4]["water"][0], None)],
             acts=[(1, 10.5, g0, False, "walk in the bed", PROG),
                   (0, 19.0, g0 - 2.0, False, "wade the strip", None),
                   (2, SUBHUB[0] + 3.0, g0 + 0.7, False, "sub-hub open", PROG),
                   (None, 6.0, g0 + 6.0, False, "Kermes (since 1937) in the dry bed", KERMES),
                   (1, 2 * LAD_S + 20.0, g2, False, "shade under the trees", None),
                   (0, HUB[0] + 4.0, g3, False, "hub square: plane-tree shade", PROG),
                   (None, 3 * LAD_S + 25.0, g3 + 2.0, False, "at K5: Demeter's Garden · café, summer beds", GARDEN),
                   (3, 4 * LAD_S + 19.0, g4, False, "fields + olives watered from storage", None)]),
        dict(key="harvest", name="OLIVE HARVEST", months="Nov", mark="olive",
             side=[("olives hand-picked in Nov", HARVEST), ("storage low until the rains", WB_YEAR),
                   ("first-flush cleaning", WB_YEAR)],
             acts=[(None, 5.0, g0 + 3.0, False, "reeds gold · seed heads", WB_YEAR),
                   (0, 3 * LAD_S + 30.0, g3, False, "Demeter's Garden: winter herbs + greens · education", GARDEN),
                   (3, 4 * LAD_S + 12.0, g4, False, "olive harvest", HARVEST),
                   (1, 4 * LAD_S + 23.0, g4, True, None, None)])]


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


def ladder_row(sea, mark_xy):
    """One season of the plant ladder in the p.23 sketch language: [(z, order, item)] in sketch units (0..LAD_W
    across). mark_xy: where the season's sun / rain mark goes, sketch units (in the season column)."""
    E = sketch_engine()
    E["FORM"] = "A"                                   # organic only where the project meets the water
    del E["ZP"][:]
    E["ORDER"][0] = 0
    o, w, gy = (0.0, 0.0), LAD_S, LAD_GY
    g = [(0.0, LAD_GB), (0.0, gy[0])]
    for i in range(1, 5):
        xa = i * w
        if i == 1:                                    # the water's edge: the bank in form A (organic)
            g += E["bank"]((xa - 3.0, gy[0]), (xa + 3.0, gy[1]))
        elif i == 2:                                  # the terrace edge: a sitting step (straight riser)
            g += [(xa - 0.5, gy[1]), (xa + 0.5, gy[2])]
        else:                                         # elsewhere faceted, straight slopes
            g += [(xa - 2.0, gy[i - 1]), (xa + 2.0, gy[i])]
    g += [(LAD_W, gy[4]), (LAD_W, LAD_GB)]
    gs = E["sketch_ground"](o, E["notch"](g, [(13.0, 25.0, gy[0], 2.0)]))   # the summer strip's low-flow channel
    pave = E["SEC_PAVE"]
    E["fill"](o, [(HUB[0], gy[3] - 0.6), (HUB[1], gy[3] - 0.6), (HUB[1], gy[3]), (HUB[0], gy[3])], "paving", pave,
              boundary=False, hand_=False)        # the dry hub square at street level (D2)
    slab = [(SUBHUB[0], gy[0]), (SUBHUB[1], gy[0]), (SUBHUB[1], gy[0] + 0.7), (SUBHUB[0], gy[0] + 0.7)]
    E["fill"](o, slab, "paving", pave, boundary=False, hand_=False)   # the floodable sub-hub in the bed
    if sea["key"] == "high":
        pc = E["under_level"](gs, 0.0, LAD_W, LAD_Q500)   # the design flood's reach (faint, as on p.23)
        if pc:
            E["wash"](o, pc, "flood", E["FLOOD_WASH"], E["FLOOD_ALPHA"])
        E["water_level"](o, gs, 19.0, gy[1] + 1.8, E["W_WIN"], bed_hatch=True)   # winter highs: bed + lower bank
        E["sketch"](o, slab, "paving", E["SKINK"], E["PEN_HAIR"], closed=True, over=0.0, retrace=False,
                    dashed=True, z=E["Z_LINE"])       # the sub-hub under the water
    elif sea["key"] == "low":
        E["water_level"](o, gs, 19.0, gy[0] - 0.8, E["W_EXT"], line=False)       # the summer strip in its channel
    else:
        E["water_level"](o, gs, 19.0, gy[0] - 1.2, E["W_SUM"], line=False)       # autumn: water back in the channel
    # plants by step (graphic sizes): reeds in the bed, rushes and shrubs on the lower bank, trees on the terrace,
    # plane tree + lavender on the bank top, olives and a field crop on the farms
    E["reeds"](o, 1.5, 8.0, gy[0] - 0.2, 4.2)
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
    E["sketch_tree"](o, 2 * w + 14.0, gy[2], 11.0)
    E["sketch_tree"](o, 2 * w + 30.0, gy[2], 9.0)
    E["sketch_tree"](o, HUB[0] + 7.0, gy[3], 11.0)   # the hub square's plane tree (D8)
    x_ = 3 * w + 20.0
    while x_ < 3 * w + 31.0:                          # lavender mounds with flower spikes
        mound = [(x_ + 1.2 * math.cos(math.pi * i / 10.0), gy[3] + 1.0 * math.sin(math.pi * i / 10.0)) for i in range(11)]
        E["wash"](o, mound, "planting", E["hx"](C["olive"]), 0.6, z=E["Z_TREE"])
        for d in (-0.5, 0.0, 0.5):
            E["sketch"](o, [(x_ + d, gy[3] + 0.8), (x_ + d * 1.3, gy[3] + 1.9)], "planting", E["hx"]("8E7CC3"), 0.3,
                        over=0.0, amp=0.02, retrace=False, z=E["Z_TREE"])
        x_ += 2.8
    E["sketch_tree"](o, 3 * w + 34.5, gy[3], 6.0)     # Demeter's Garden olive (K5)
    for xs in (4 * w + 6.0, 4 * w + 15.0):            # olives
        E["sketch_tree"](o, xs, gy[4], 7.0)
    x_ = 4 * w + 26.0
    while x_ < LAD_W - 1.0:                           # field crop rows
        E["sketch"](o, [(x_, gy[4]), (x_, gy[4] + 1.6)], "planting", E["hx"](C["field"]), 0.35, over=0.0, amp=0.02,
                    retrace=False, z=E["Z_TREE"])
        x_ += 1.4
    # the site edge: farmland only outside the site
    E["sketch"](o, [(4 * w, gy[3] + 1.5), (4 * w, gy[4] + 11.0)], "site edge", E["INK2"], E["PEN_FINE"], over=0.0,
                retrace=False, dashed=True, z=E["Z_LINE"])
    s_ = 4.5 / 1.745                                  # people: the season's activities
    for kind, x, y, flip, _lab, _src in sea["acts"]:
        if kind == "sit":
            sg = -1.0 if flip else 1.0
            E["fill"](o, [(x + sg * a * s_, y + b * s_) for a, b in SIT_FIG], "people", E["SITE_PEOPLE"], alpha=0.9,
                      boundary=False, z=E["Z_PEOPLE"], hand_=False)
            hx_, hy_, hr = E["SA_HEAD"][0] - 0.02, 0.84, E["SA_HEAD"][2]
            E["fill"](o, [(x + sg * hx_ * s_ + hr * s_ * math.cos(6.283 * i / 12), y + hy_ * s_ + hr * s_ * math.sin(6.283 * i / 12))
                          for i in range(12)], "people", E["SITE_PEOPLE"], alpha=0.9, boundary=False, z=E["Z_PEOPLE"],
                      hand_=False)
        elif kind is not None:
            E["sketch_person"](o, x, y, kind=kind, flip=flip)
    if sea["key"] == "high":                          # the design flood levels, hand dashed lines and level marks
        xe = 4 * w - 2.0 + 4.0 * (LAD_Q500 - gy[3]) / (gy[4] - gy[3])
        for lv in (LAD_Q500, LAD_Q100):
            E["sketch"](o, [(0.0, lv), (xe, lv)], "flood lines", E["HERITAGE"], E["PEN_FINE"], over=0.0, retrace=False,
                        dashed=True, z=E["Z_LINE"])
            E["level_mark"](o, 3 * w + 26.0 if lv == LAD_Q500 else 3 * w + 20.0, lv, E["HERITAGE"], "flood lines")
    if sea["key"] == "low":                           # the farms are watered from storage in summer: the one arrow
        E["hand_arrow"](o, (3 * w + 22.0, gy[4] + 10.0), (4 * w + 9.0, gy[4] + 8.0), E["SITE_WATER_D"], bend=-0.15)
    if sea["mark"] == "winter":
        E["cloud_rain"](o, mark_xy[0], mark_xy[1], 2.0)
    elif sea["mark"] == "summer":
        E["sun"](o, mark_xy[0], mark_xy[1], 1.7)
    E["sketch"](o, gs, "ground lines", E["SKINK"], E["PEN_BOLD"], z=E["Z_LINE"])   # the cut: the gesture
    return sorted(E["ZP"], key=lambda e: (e[0], e[1]))


# v1.6: the one-way chain along the stream, upstream to the farms: (name, marker, programme, historic root, sources).
# Spec §3 / Aras 27 Oct: option A only; hubs at the bridges with in-bed sub-hubs; Demeter's Garden on the SW bank at
# K5; farmland only outside the site.
CHAIN = [("UPSTREAM ENTRY", "reeds", "reed basins clean once · terraces hold", None, (CHAIN_REF,)),
         ("K4", "hub", "hub + sub-hub · water-touching step", "Roman bridge · Tabaklar Hamamı", (PROG,)),
         ("K3", "hub", "hub + sub-hub · craft workshops", "tanning quarter (Tabakhane)", (PROG,)),
         (u"İSTİKLAL MEYDANI", "small", "hidden-stream square", "over the Red Hall tunnels", (PROG,)),
         ("K5", "hub", "hub + sub-hub · Demeter's Garden", "Roman bridge · Demeter, abundance", (PROG, GARDEN)),
         ("K6", "gate", "gateway out", None, (PROG,)),
         ("DOWNSTREAM REACH", "reeds", "floodable planting · boardwalk", "Late Antique workshops", (CHAIN_REF, PROG)),
         ("FARMLAND", "farm", "outside the site · water from storage", "Tersane cotton (16th c.)", (COTTON_H,))]
HUB_COL = "BC6F45"                                   # the sketch engine's walkable edge (terracotta)


def chain_strip(pg, P, y_top):
    """the chain across the page: node names, the one-way water ribbon with hubs and sub-hubs, programme and root
    keywords. Returns the lowest y used."""
    n = len(CHAIN)
    x0, dx = 16.0, (404.0 - 16.0) / n
    yr = y_top - 6.0                                 # the ribbon
    xs = [x0 + 2.0 + i * dx for i in range(n)]
    pg.line([(xs[0], yr), (xs[2], yr)], C["water"], 1.6)
    pg.line([(xs[2], yr), (xs[3] + dx * 0.5, yr)], C["water"], 1.6, (1.6, 1.1))   # the covered reach (H2)
    pg.line([(xs[3] + dx * 0.5, yr), (xs[-1] - 4.0, yr)], C["water"], 1.6)
    pg.poly([(xs[-1] - 4.0, yr + 1.8), (xs[-1] - 0.6, yr), (xs[-1] - 4.0, yr - 1.8)], fill=C["water"], closed=True)
    for i in range(n - 2):                           # one way, with the stream
        ax = (xs[i] + xs[i + 1]) / 2.0 + 4.0
        pg.poly([(ax - 1.2, yr + 1.1), (ax + 0.6, yr), (ax - 1.2, yr - 1.1)], fill=C["water_deep"], closed=True)
    low = yr
    for i, (name, mk, prog, root, refs) in enumerate(CHAIN):
        x = xs[i]
        if mk == "hub":
            pg.rect(x - 1.6, yr - 1.6, 3.2, 3.2, fill=HUB_COL, stroke=C["ink"], lw=0.2)
            pg.circle(x, yr - 3.4, 0.8, fill=C["water_deep"])
        elif mk == "small":
            pg.rect(x - 1.1, yr - 1.1, 2.2, 2.2, fill=C["white"], stroke=HUB_COL, lw=0.4)
        elif mk == "gate":
            pg.line([(x - 1.2, yr + 1.8), (x + 0.8, yr), (x - 1.2, yr - 1.8)], C["ink"], 0.4)
        elif mk == "reeds":
            icon(pg, "clean", x - 2.5, yr + 2.3, 5.0)
        else:
            icon(pg, "outside", x - 2.0, yr + 2.8, 5.6)
        tx = x - 1.5
        P.text(pg, name, tx, yr + 3.6, 8.5, C["ink"], True)
        y = yr - 7.0                               # clear of the sub-hub dot
        mark = "".join(cite(r) for r in refs)
        lines = [(q, C["ink"]) for q in wrap(prog + ("" if root else " " + mark), 7, dx - 3.0)]
        if root:
            lines += [(q, C["accent"]) for q in wrap(root + " " + mark, 7, dx - 3.0)]
        for q, col in lines:
            P.text(pg, q, tx, y, 7, col)
            y -= 2.9
        low = min(low, y + 2.9 - 1.2)
    # key to the markers, top right
    kx, ky = 406.0, y_top + 2.5
    items = [("ribbon", "one way, with the stream"), ("dash", "covered reach"), ("dot", "sub-hub in the bed, floodable"),
             ("hub", "hub square, dry")]
    for kind, lab in items:
        kx -= text_w(lab, 7)
        P.text(pg, lab, kx, ky, 7, C["ink"])
        kx -= 5.0
        if kind == "hub":
            pg.rect(kx + 0.6, ky - 0.2, 2.6, 2.6, fill=HUB_COL, stroke=C["ink"], lw=0.2)
        elif kind == "dot":
            pg.circle(kx + 1.9, ky + 1.1, 0.8, fill=C["water_deep"])
        elif kind == "dash":
            pg.line([(kx, ky + 1.1), (kx + 4.0, ky + 1.1)], C["water"], 1.4, (1.2, 0.8))
        else:
            pg.line([(kx, ky + 1.1), (kx + 4.0, ky + 1.1)], C["water"], 1.4)
        kx -= 4.0
    return low


def page_ladder(L, src):
    pg = Page(420, 297)
    P = Placer()
    header(pg, "3", "ONE PLANT LADDER, STREAMBED TO FIELD",
           "One cut from the stream to the farms, through the year: what the water does and what people do on each step")
    # 1 the chain: where the ladder sits along the stream, the programme and its roots
    y_chain = chain_strip(pg, P, 260.0)
    ag_crop("ag3_chain", 2, 13.0, y_chain - 1.0, 407.0, 266.0)
    # 2 the ladder, one row a season
    top = y_chain - 2.0
    for r, sea in enumerate(seasons()):
        T, B = top - r * ROW_H, top - (r + 1) * ROW_H
        y0 = B + 2.0 - LAD_GB * LAD_F                  # page y of the sketch's 0
        mark = ((19.0 - LAD_X0) / LAD_F, (T - 6.0 - y0) / LAD_F)
        sk_draw(pg, xform([e[2] for e in ladder_row(sea, mark)], LAD_F, LAD_X0, y0))   # v1.7: (z, order, item, group)
        if sea["mark"] == "olive":
            icon(pg, "olive", 14.0, T - 1.5, 9.0)
        P.text(pg, sea["name"], 26.0, T - 8.0, 12, C["ink"], True)
        P.text(pg, sea["months"], 26.0, T - 13.0, 9, C["accent"], True)
        y = T - 18.5
        for t, ref in sea["side"]:
            for q in wrap(t + ((" " + cite(ref)) if ref else ""), 7.5, LAD_X0 - 30.0):
                P.text(pg, q, 26.0, y, 7.5, C["ink"])
                y -= 3.2
        reg = (LAD_X0, B + 1.0, LAD_X1, T - 0.8)
        Y = lambda v: y0 + v * LAD_F
        X = lambda v: LAD_X0 + v * LAD_F
        if sea["key"] == "high":                       # flood levels first: they sit at their lines
            for lv, lab, up in ((LAD_Q500, "Q500 · 263 m³/s · 2.3-3.3 m above the bed " + cite(DEPTH), True),
                                (LAD_Q100, "Q100 · 205 m³/s · 2.0-3.0 m", False)):
                P.put(pg, lab, X(1.5), Y(lv), 7, "8B2D2D", region=reg, gap=0.8, up=up, lanes=3)
            P.put(pg, "over the bank top only at K4 (right bank) and S4 (left)", X(3 * LAD_S + 3.0), Y(LAD_Q500) + 3.0,
                  7, "8B2D2D", region=reg, gap=0.5)
            P.put(pg, "site edge: farmland outside", X(4 * LAD_S), Y(LAD_GY[4] + 11.0), 7, C["ink2"], region=reg, gap=0.6)
        if sea["key"] == "low":
            P.put(pg, "stored winter water", X(3 * LAD_S + 22.0), Y(LAD_GY[4] + 10.0), 7, C["water_deep"], True,
                  region=reg, gap=1.0)
        for kind, x, yv, flip, lab, ref in sea["acts"]:
            if lab:
                hgt = 0.0 if kind is None else (3.2 if kind == "sit" else 4.9)
                P.put(pg, lab + ((" " + cite(ref)) if ref else ""), X(x), Y(yv + hgt), 7, C["ink"], True, region=reg)
        if r < 2:
            pg.line([(14.0, B), (406.0, B)], C["faint"], 0.3)
    bot = top - 3 * ROW_H
    ag_crop("ag3_seasons", 2, 13.0, bot - 0.5, 407.0, top + 0.5)
    # 3 what grows on each step (one column under each step) and, left, what goes and the odour
    yt = bot - 4.0
    w = LAD_S * LAD_F
    for i, st in enumerate(STEPS):
        xa = LAD_X0 + i * w + 1.0
        for brief in (False, True):                  # the species' reasons left out if the column would not fit
            y, ops = yt, []
            ops.append((st["name"], xa, y, 8.5, C["ink"], True)); y -= 3.4
            ops.append((st["sub"], xa, y, 7, C["ink2"], False)); y -= 6.4
            tag_y = y
            y -= 4.0
            if st["band"]:
                l_, r_ = GEO["corridor"]["left " + st["band"]], GEO["corridor"]["right " + st["band"]]
                v = [(l_[k] + r_[k]) / 2.0 for k in ("trees", "grass", "farmland")]
                t = "today: trees %.0f %% · grass %.0f %% · fields %.0f %% %s" % (v[0], v[1], v[2], cite(TODAY))
                for q in wrap(t, 7, w - 4.0):
                    ops.append((q, xa, y, 7, C["ink2"], False)); y -= 2.9
            if st["name"] == "FARMS":
                for q in wrap(STEPS[4]["water"][1].replace("{reuse}", cite(REUSE)), 7, w - 4.0):
                    ops.append((q, xa, y, 7, C["ink2"], False)); y -= 2.9
            y -= 1.2
            ops.append(("WE PLANT " + cite(SPECIES) if st["name"] != "FARMS" else "THEY GROW", xa, y, 7, C["accent"], True))
            y -= 3.6
            for sp, why in st["plant"]:
                ops.append((sp, xa, y, 7.5, C["ink"], True)); y -= 3.0
                if not brief:
                    for q in wrap(why, 7, w - 4.0):
                        ops.append((q, xa, y, 7, C["ink2"], False)); y -= 2.8
                y -= 0.6
            if y > 15.0:
                break
        for s_, x_, y_, sz, col, b in ops:
            P.text(pg, s_, x_, y_, sz, col, b)
        pg.rect(xa, tag_y, text_w(st["job"], 8, True) + 4, 5.2, fill=C["accent"])
        pg.text(st["job"], xa + 2, tag_y + 1.5, 8, C["white"], True)
        jx = xa + text_w(st["job"], 8, True) + 6
        for word, kind in JOB_ICON:                  # the job as pictograms beside the tag
            if word in st["job"]:
                pg.rect(jx, tag_y - 0.4, 6.0, 6.0, fill=C["white"], stroke=C["faint"], lw=0.2)
                icon(pg, kind, jx + 0.5, tag_y + 5.1, 5.0); jx += 7.0
    # left column: what goes, the odour, how to read the steps
    y = yt
    for t, sz, col, b in (("REMOVE: Arundo donax", 8, C["accent"], True), ("giant reed: raises flood risk, blocks bridges", 7, C["accent"], False)):
        for q in wrap(t, sz, LAD_X0 - 18.0, b):
            P.text(pg, q, 14.0, y, sz, col, b); y -= sz * 0.3528 * 1.35
    y -= 3.0
    icon(pg, "nose", 14.0, y + 3.0, 6.0)
    for t, b in (("ODOUR: no measured plant effect " + cite(SPECIES), True), ("keep sewage out", False),
                 ("clean once, at the upstream end", False), ("plants: clean nutrients, give scent", False)):
        for q in wrap(t, 7.5, LAD_X0 - 30.0, b):
            P.text(pg, q, 22.0, y, 7.5, C["ink"], b); y -= 3.2
    y -= 3.0
    for t in ("steps = planting bands " + cite(BANDS), "depths above the bed " + cite(DEPTH), "a diagram, not to scale",
              "downstream flat end: Q100 1.4 m, Q500 1.5 m"):
        for q in wrap(t, 7, LAD_X0 - 18.0):
            P.text(pg, q, 14.0, y, 7, C["ink2"]); y -= 2.9
    ag_crop("ag3_plants", 2, 13.0, 14.0, 407.0, yt + 4.0)
    LOG_NOTES.extend("p3 label left out (no free place): " + s for s in P.dropped)
    return pg

# ------------------------------------------------------------------ v1.6: the sources page (Aras 27 Oct: no source footers)
def page_sources():
    """the sheet's one numbered source key, on its own page: the [n] marks on pages 1-3 refer to it, and the
    booklet's sources page reads it from here ("Sources by number:", as the old page footers)."""
    pg = Page(420, 297)
    pg.rect(0, 0, 420, 297, fill=C["white"])
    pg.text("SOURCES", 14, 279, 22, C["ink"], True)
    pg.text("Numbered as the [n] marks on pages 1-3", 14, 271.5, 11, C["ink2"])
    key = "Sources by number: " + "  ".join("[%d] %s" % (i + 1, k) for i, k in enumerate(SRC_KEY))
    pg.para(key, 14, 260, 392, 8, C["ink"], lead=1.35)
    return pg

# ------------------------------------------------------------------ v1.4: A3 booklet = crops of this sheet (booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own drawings. Each page function records its panels' rects
# (from the same numbers it lays them out with) in AG_CROPS; booklet_export writes them to blocks.json, with
# booklet/results.json (hectares per crop, same keys as v1.3). The v1.3 booklet redraws are gone.
# ---- A3 booklet assets (SCRIPT_STANDARD §8; booklet/ASSET_SPEC.md) ----
# Each booklet frame = one text-free vector PDF drawn at the frame's size + its words as labels in blocks.json.
# The assembler (bergama_booklet) sets every label as live text in the booklet font, never below 7 pt.
BK_MIN_PT = 7.5                              # labels and captions on the booklet (brief: 7-8 pt, minimum 7)
BK_CAPTION_MM = 5.0                          # caption line under every drawing frame


def bk_frame(key, w_default, h_default):
    """(w, h) mm a drawing for asset key "<folder>/<block>" is drawn at: the assembler's booklet_slots.json if it has
    run once, else the defaults given (the plan's frame size). h excludes the caption line."""
    try:
        import json as _j
        with open(bg_first([os.path.join(bg_booklet(""), "booklet_slots.json"),        # 27 Oct: cached/booklet/
                            os.path.join(bg_output("bergama_booklet"), "booklet_slots.json")]), encoding="utf-8") as f:
            s = _j.load(f)[key]
        return float(s["w_mm"]), float(s["h_mm"]) - BK_CAPTION_MM
    except Exception:
        return float(w_default), float(h_default) - BK_CAPTION_MM


def bk_take_text(items, H):
    """Page items (poly/line/circle/text tuples, y up from the bottom, mm) -> (items without text, labels).
    Labels: x, y in mm from the top-left (y to the baseline), size raised to BK_MIN_PT, colour hex."""
    keep, labels = [], []
    for it in items:
        if it[0] != "text":
            keep.append(it)
            continue
        _, s, x, y, size, color, bold, align = it[:8]
        labels.append({"x": round(x, 2), "y": round(H - y, 2), "text": s, "size": max(float(size), BK_MIN_PT),
                       "bold": bool(bold), "anchor": align or "L", "colour": color if isinstance(color, str) else "4A3F35"})
    return keep, labels


class BkBlocks(object):
    """Collects one script's booklet blocks and writes cached/booklet/<folder>/blocks.json (27 Oct, Aras: output/ holds
    final PDFs only; was output/<folder>/booklet/). out_dir = the script's output folder; its name is the folder key."""
    def __init__(self, out_dir, script, version):
        self.dir = bg_booklet(os.path.basename(os.path.normpath(out_dir)))
        os.makedirs(self.dir, exist_ok=True)
        self.d = {"script": script, "version": version, "sources": {}, "blocks": {}}

    def path(self, name):
        return os.path.join(self.dir, name)

    def source(self, key, text, url):
        """A public source: used in any text as {src:key}; numbered once for the whole booklet."""
        self.d["sources"][key] = {"text": text, "url": url}

    def drawing(self, bid, pdf_name, labels, caption="", scale_den=None, legend=None):
        self.d["blocks"][bid] = {"type": "drawing", "pdf": pdf_name, "page": 0, "labels": labels, "caption": caption,
                                 "scale_den": scale_den, "legend": legend or []}

    def crop(self, bid, pdf_name, rect_mm, caption="", scale_den=None, legend=None, page=0, drop=None):
        """A booklet drawing taken from this script's own sheet (Aras 25 Oct 21:47: the booklet shows the sheet's
        drawing, re-laid): pdf_name = the sheet PDF in this script's output folder, rect_mm = (x0, y0, x1, y1) of the
        panel in mm from the sheet page's top-left (y down), scale_den = the sheet's scale at 1:1 print (None if not to
        scale). The assembler scales the crop to its frame and resets the sheet's words inside it as live labels;
        drop = regexes of sheet texts not to carry."""
        self.d["blocks"][bid] = {"type": "crop", "pdf": pdf_name, "page": page,
                                 "rect_mm": [round(float(v), 2) for v in rect_mm], "caption": caption,
                                 "scale_den": scale_den, "legend": legend or [], "drop": drop or []}

    def tiles(self, bid, tiles):
        self.d["blocks"][bid] = {"type": "tiles", "tiles": tiles}

    def text(self, bid, heading="", body="", bullets=None):
        self.d["blocks"][bid] = {"type": "text", "heading": heading, "body": body, "bullets": bullets or []}

    def save(self):
        import json as _j
        p = os.path.join(self.dir, "blocks.json")
        with open(p, "w", encoding="utf-8") as f:
            _j.dump(self.d, f, ensure_ascii=False, indent=1)
        return p
AG_CROPS = []                        # (id, page index, (x0, y0, x1, y1) mm from the page's top-left, y down, den, legend, drop)
AG_CAPTIONS = {"ag1_headline": "Storage and water to the farms", "ag1_bars": "Hectares one storage irrigates, by crop",
               "ag1_reading": "Same storage: how much more land", "ag1_context": "Why crop choice is the lever",
               "ag1_replaces": "What it replaces", "ag2_plan": "The farms we feed, on the site plan",
               "ag3_chain": "One way along the stream: the programme and its roots",
               "ag3_seasons": "One plant ladder through the year: what people do", "ag3_plants": "What grows on each step"}


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
        del AG_CROPS[:], SRC_KEY[:], LOG_NOTES[:]      # v1.6: one source numbering for the whole sheet
        pages = [page_cubic(L, src), page_farms(L, src), page_ladder(L, src)]
        write_pdf(pages + [page_sources()], path)
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
    bk = "\n".join([bk] + bg_tidy_output("Bergama_agriculture_alternatives"))   # 27 Oct: output/ = PDFs only
    flag = "".join("\n" + t for t in LOG_NOTES)
    flag += "\nFLAG: water balance results file not found in Downloads; its default-lands copy was used" if src == DEFAULT_NOTE else ""
    return "%s  %s\nfigures: %s%s\n%s\nagriculture alternatives %s, %.1f s\n%s" % (OUT_PDF, time.strftime("%H:%M:%S"), src, flag, base, VERSION, time.time() - t0, bk)

def chain_fire(v, key):
    """25 Oct 10:20 (one-click chain): the previous script's done output is a text "done HH:MM:SS.ss ..." that stays
    after the Button is released; each NEW text fires this script once (the Button still works as before)."""
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
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


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
        _sc.sticky["bergama_agri_alt_log_ver" + _ik] = VERSION
    if _sc.sticky.get("bergama_agri_alt_log_ver" + _ik) != VERSION:   # v1.7 (Aras 27 Oct 15:35): a newly pasted version
        for _s in ("", "_status", "_done"):                            # shows itself at once, idle, no old time or log
            _sc.sticky.pop("bergama_agri_alt_log" + _s + _ik, None)
    done = _sc.sticky.get("bergama_agri_alt_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_agri_alt_log" + _ik, "Press the Button to export to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "AgriCulture " + VERSION + " · " + _sc.sticky.get("bergama_agri_alt_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main()))
