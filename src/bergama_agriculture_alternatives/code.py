# r: pymupdf==1.26.5
# bergama_agriculture_alternatives_v5.py · Thread 3 of the 22 Oct batch: three alternatives for the agriculture analysis
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Makes the folder Downloads/Bergama/output/Bergama_agriculture_alternatives by itself and saves ONE
# all-vector A3 PDF there, one page per alternative:
#   1 WHAT EACH CUBIC METRE GROWS   chart: hectares the stored water irrigates, per crop, normal and 1-in-5 dry year
#   2 THE FARMS WE FEED             the site board's plan 01 "What is there" at a round scale with the fields and orchards fed
#   3 SOURCES                       the numbered key of the [n] marks on pages 1-2
# T4a (revision 29 Oct, WO-T4a-4): D9 a: the plant ladder page (booklet p20) is gone with everything only it used (its
#   content lives on the water board's p17 and p14-15); pictograms and step markers from common/icons.py (02 §2); D13:
#   sources naming our own model run or method and status words never reach the printed key (cite).
# Storage, water to the farms and the farm areas are read on every run from the water balance script's output
# (bergama_water_balance), so they follow its cost cut-off; the fallback is the shared key-figures file (flagged).
# Notes for Aras: batch_2026-10-22/thread3_agriculture/NOTES.md.
import os, time, json, zlib, math, re

VERSION = "v5.1"
# NEW IN v5.1 (bugfix, revision 29 Oct T5 fix pass, Aras 22:08): p.19 "10,000 m³ = N ha olive" is computed live, the
# same way as the water board's p.18 (10,000 / gross m³ a ha of olive in a dry year, from water_balance_results.json);
# it was the fixed text "1.22 ha".
# v4 (MIRAQUA 28 Oct, booklet revision v4, pages 18-19; a feature change, so the next whole number):
#   * P18.1 / P19.3 / P19.4 / G11 / G12: every photo through common/plant_photos.py; corn printed as "Corn (Mısır)"
#     (data key "maize" and the Wikimedia file kept); an empty frame says "no photo: <reason>".
#   * P19.1 / G5 / F10: the kicker top left; page 3's top-right corner on the booklet grid (column 8, 4 rows 5.2 mm
#     apart, 7.5 pt): steps 1-5, NEXT -> D The heritage loop (title bold), the chain key; no big page numbers.
#   * P19.2: the ladder's people from common/figures.py at true scale (1.75 m), one colour, no stroke.
#   * G4 / F13: ladder labels placed by common/label_place.py clear of figures, lines, plants and each other;
#     "hub square: dry, step-free" and "wade the strip" now print.
#   * G13: flood heights in m with 2 decimals (values unchanged). Bank depth research 28 Oct §4.5: over the bank top
#     only at S4 (left); K4 before the DSİ walls.
#   * F5: [n] marks only for public online sources; internal pointers out of the printed source list.
#   * G1: page 2's group line removed; page 1's left column on the 14 mm margin.
# v3.1 (bugfix, Aras 27 Oct, booklet Prompt 8 "final check of every page"): plant and crop names "English (Turkish)"
#   from the shared table where pages 1 and 3 still had the English alone: page 3's season row OLIVE (ZEYTİN) HARVEST,
#   its labels (hub square: oriental plane (Doğu çınarı) shade; common reed (Kamış) gold; olive (Zeytin) harvest;
#   olive (Zeytin) trees on the fields) and page 1's "what it replaces" figure. Page 3: "stored winter water" and
#   "site edge: farmland outside" sit at the row's top edge, so they found no free place above it and were left out on
#   every run: they now go under their anchors. The h01 timeline quotes stay word for word. Page 1's "THE STREAM COMES
#   FIRST" block and the step chips: its 6.5 pt words are 7 pt, the smallest size on a booklet page.
# v3 (Aras 27 Oct 17:35, Prompt 6 "water, part 3"; the booklet's p.24-25):
#   * page 1, "THE STREAM COMES FIRST" between the headline and the bars (task 1: "show the defence ON the board"): the
#     priority 1 stream: summer strip -> 2 on-site planting -> 3 farms (the model has no draw of its own for the
#     planting: it lives on the strip's water, so it shares the strip's bar); the design store through a normal and the
#     1-in-5 dry water year as two stacked bars on one scale (strip, farms, left over; the store size dashed across
#     both), read live from the water balance v4 results (design.year_split, one daily run); and the double squeeze in
#     one line, computed: water left for the farms after the strip, the need per hectare and the hectares that water
#     serves, dry year against normal, then why deficit-irrigated olive is the lever. Without year_split (water balance
#     v3 or older) only the priority row is drawn (logged). The bars move down to make room: rows 16.5 mm apart (were
#     19.5), the reading box ends at the 14 mm margin.
#   * pages 1 and 3 say where they sit in the booklet: "C WATER · WHAT WE DO WITH IT" (was "AGRICULTURE ANALYSIS");
#     page 3, the last page of the water theme, closes it top right: what we do with the water in five steps and NEXT
#     D HISTORY AND HERITAGE (rule 7, task 3).
#   * m² and m³ are written as a raised small 2 or 3 (0.6 x the size, as wide as the glyph), which every PDF viewer
#     shows (task 2: "325,000-375,000 m" in some viewers).
# v2 (Aras 27 Oct, Prompt 5, rule 8: "Plant names: English first, Turkish in brackets, no Latin ... Every plant AND every
# crop in the booklet gets a photo of the plant itself ... openly licensed photos ... credited in the sources ... Same
# crop ratio and size for every photo"): every plant and crop name on pages 1 and 3 is "English (Turkish)" from the
# shared table (src/common/plant_photos.py), no Latin names on the pages. Page 3's step columns show each step's plants
# as photos (PHOTO_W x PHOTO_H mm, two side by side) with the name and the photo's [n] credit under each; the giant reed
# under REMOVE. Page 1 adds "THE CROPS" under the timeline: olive, cotton, corn, tomato as photos. The photos come
# from the shared cache Downloads/Bergama/cached/plant_photos/ (the water board shows the same photo of the same
# plant) and go into their frames with PyMuPDF after the PDF is written; a missing one is an empty frame saying "no
# photo", never an error; the log says how many were placed. Room on page 3: the chain sits 4 mm higher, the season rows
# are 50 mm (were 52; 4.5 mm stay above the tallest tree); the plants' reasons are left out under the photos when the
# column would not fit (logged). The Data file changes (STEPS: plant keys instead of botanical names): copy the new one.
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
#@include ../common/bergama_paths.py
#@include ../common/plant_photos.py
#@include ../common/icons.py
LOG_DIR = bg_logs()                       # Aras 25 Oct 09:34-09:35: every script's log here


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
#@include data/GEO.py

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
    L["year_split"] = (d.get("design") or {}).get("year_split")      # v3: water balance v4 and newer
    L["design_mix"] = (d.get("design") or {}).get("mix", "")
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
# v3 (Aras 27 Oct, Prompt 6: "325,000-375,000 m"): ² and ³ are drawn as the digit at 0.6 x the size, raised 0.28 x the
# size (then as wide as the ²/³ glyph, 333/1000): the unembedded Helvetica's ²/³ was missing in some viewers
SUP = {u"²": u"2", u"³": u"3"}
SUP_K, SUP_UP = 0.6, 0.28


def sup_runs(s):
    """v3: s cut into (text, raised) runs at ² and ³, which become a plain 2 or 3"""
    out, cur = [], u""
    for ch in s:
        if ch in SUP:
            if cur: out.append((cur, False))
            out.append((SUP[ch], True)); cur = u""
        else:
            cur += ch
    if cur: out.append((cur, False))
    return out

#@include ../common/text_w.py


#@include ../common/pdf_fonts.py

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
        if any(ch in SUP for ch in s):             # v3 (Prompt 6): m² / m³ as a raised small digit (see SUP)
            runs = sup_runs(s)
            ws = [text_w(t, size * (SUP_K if up else 1.0), bold) for t, up in runs]
            x -= {"L": 0.0, "C": sum(ws) / 2.0, "R": sum(ws)}[align]
            for (t, up), w_ in zip(runs, ws):
                self.text(t, x, y + (size * SUP_UP * 0.3528 if up else 0.0), size * (SUP_K if up else 1.0), col, bold,
                          "L", halo)
                x += w_
            return
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
            "", ""]
    extra, first = [], 5 + 2 * n                          # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py):

    def add(b):                                           # font file + descriptor go after the pages
        extra.append(b.decode("latin-1"))
        return first + len(extra) - 1
    fid = pdf_fonts(add, ("R", "B"))
    objs[2], objs[3] = extra[fid[0] - first], extra[fid[1] - first]   # the font dicts themselves stay objects 3, 4
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
    for j, o in enumerate(extra):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (first + j, o)).encode("latin-1")
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

SRC_KEY = []          # v1.6: sources printed as [n] on pages 1-3, numbered once for the sheet; the key is page 4
LOG_NOTES = []        # v1.6: what the layout left out (log)

def cite(src):
    """v1.2 (water board v1.6 method): the number of a source in the sheet's key (v1.6: page 4), as "[n]".
    v4 (MIRAQUA 28 Oct, F5): "" for a source that is not public online (F5_OFF): no mark, not in the key.
    v5 (T4a, D13): also "" for a source naming our own model run or method (F5_INTERNAL); status words cut (F5_STATUS)."""
    if not src or src in F5_OFF or any(t in src for t in F5_INTERNAL):
        return ""
    src = F5_STATUS.sub("", src).strip()
    if src not in SRC_KEY: SRC_KEY.append(src)
    return "[%d]" % (SRC_KEY.index(src) + 1)


def cited(s, *srcs):
    """v4 (F5): s with its [n] marks after one space, or s alone when none of its sources is public"""
    mk = "".join(cite(q) for q in srcs if q)
    return s + (" " + mk if mk else "")

def wrap(s, size, w, bold=False):
    out, line = [], ""
    for word in s.split(" "):
        t = (line + " " + word).strip()
        if text_w(t, size, bold) > w and line: out.append(line); line = word
        else: line = t
    if line: out.append(line)
    return out

# ------------------------------------------------------------------ v2 (Aras 27 Oct, Prompt 5): plant and crop photos
# The photos and the "English (Turkish)" names come from src/common/plant_photos.py (one cache folder for every script,
# every photo PHOTO_W x PHOTO_H mm). This PDF writer draws only the frame (thin, faint; "no photo" inside when there is
# none); the JPEGs go into the frames after write_pdf (put_photos, PyMuPDF). Each photo's credit is a [n] mark after its
# name, its key on the sources page.
PH_GAP = 2.0                         # mm between two photos side by side
PHOTO_GOT = {}                       # key -> (jpeg path or None, credit or None, why not), read once a press
PHOTO_LOG, PHOTO_STATE = [], {}      # plant_photos' own notes (web fetch) and its offline flag
PHOTO_FR = []                        # frames with a photo: (page index, x0, y0, x1, y1 mm y up, jpeg path)
PHOTO_N = [0]                        # frames drawn, with or without a photo


def photo_get(key):
    """v2: (jpeg path or None, credit or None, why not) of a plant in PLANTS, once a press; never raises"""
    if key not in PHOTO_GOT:
        try:
            PHOTO_GOT[key] = plant_photo_of(key, PHOTO_LOG, PHOTO_STATE)
        except Exception as ex:
            PHOTO_GOT[key] = (None, None, "%s: %s" % (type(ex).__name__, ex))
    return PHOTO_GOT[key]


def photo_mark(key):
    """v2: the [n] of a plant photo's credit (its key on the sources page); "" when there is no photo"""
    p, credit, _ = photo_get(key)
    return cite(credit) if p and credit else ""


def photo_frame(pg, pi, key, x, top, P=None):
    """v2: the frame of a plant's photo, PHOTO_W x PHOTO_H mm, its top-left at (x, top) on page index pi: a thin faint
    outline, and the photo recorded for put_photos, or "no photo" inside the frame. P: a Placer that keeps the frame.
    v4 (MIRAQUA 28 Oct, G12): an empty frame says why, as the water board's cards: "no photo: " + the loader's reason
    (common/plant_photos.py: offline, Wikimedia refused (HTTP 429) press again later, file not found, licence ...),
    7 pt (the booklet's smallest), top left in the frame."""
    p, _cr, why = photo_get(key)
    pg.rect(x, top - PHOTO_H, PHOTO_W, PHOTO_H, stroke=C["faint"], lw=0.2)
    PHOTO_N[0] += 1
    if p:
        PHOTO_FR.append((pi, x, top - PHOTO_H, x + PHOTO_W, top, p))
    else:
        pg.para(u"no photo: " + (why or u"not loaded"), x + 1.5, top - 4.0, PHOTO_W - 3.0, 7, C["ink2"], lead=1.2)
    if P is not None:
        P.boxes.append((x, top - PHOTO_H, x + PHOTO_W, top))


def name_lines(key, mark, size, w, bold=True):
    """v2: a plant's name under its photo: "English (Turkish) [n]" on one line when it fits in w, else the English name
    and "(Turkish) [n]" on two (each wrapped to w if it is longer still)"""
    t = plant_name(key) + ((" " + mark) if mark else "")
    if text_w(t, size, bold) <= w:
        return [t]
    en, _, tr = plant_name(key).partition(" (")
    if not tr:
        return wrap(t, size, w, bold)
    return wrap(en, size, w, bold) + wrap("(" + tr + ((" " + mark) if mark else ""), size, w, bold)


def name_lc(key):
    """v2: a plant's name in running text: "olive (Zeytin)" """
    s = plant_name(key)
    return s[:1].lower() + s[1:]


def name_caps(key):
    """v2: a plant's name in a capitals heading, the Turkish part with the dotted İ: "OLIVE (ZEYTİN)" """
    en, _, tr = plant_name(key).partition(" (")
    return en.upper() + ((" (" + tr.replace(u"i", u"İ").upper()) if tr else "")


def crop_word(key):
    """v4 (MIRAQUA 28 Oct, G11): a crop key as a short printed word, the English name of the shared table: "maize" ->
    "corn", "cotton" -> "cotton"; a key the table does not have stays as it is"""
    return plant_name(key).partition(" (")[0].lower() if key in PLANTS else key


def put_photos(path):
    """v2: the plant and crop photos into their frames on pages 1 and 3 (PyMuPDF, after write_pdf and put_base); a photo
    error never stops the sheet. Returns the log lines: how many were placed, and why each missing one is missing."""
    n, err = 0, ""
    try:
        if PHOTO_FR:
            n = fitz_add_photos(path, PHOTO_FR)
    except Exception as ex:
        err = " · FLAG not placed: %s: %s" % (type(ex).__name__, ex)
    if not err and n < len(PHOTO_FR):
        err = " · %d JPEG(s) could not be read" % (len(PHOTO_FR) - n)
    out = ["photos: %d of %d placed (cached/plant_photos)%s" % (n, PHOTO_N[0], err)]
    out += ["  no photo: %s (%s)" % (plant_name(k), v[2] or "not loaded") for k, v in PHOTO_GOT.items() if not v[0]]
    out += ["  " + t for t in PHOTO_LOG]
    return "\n".join(out)

STAGE_TAG = u"C  WATER  ·  WHAT WE DO WITH IT"   # v3 (Prompt 6, rule 7): the booklet's theme and stage of pages 1 and 3


HEAD_Y = (285.0, 276.5, 269.5)       # v4 (MIRAQUA 28 Oct, P19.1): baselines of the kicker, the title and the subtitle


def header(pg, title, sub, hole=None, tag=None):
    """v4 (MIRAQUA 28 Oct, F10 decision 3, default remove; P19.1): the sheet's big page number before the title is
    gone (it read as a booklet page number); the booklet stage tag (pages 1 and 3) is the kicker over the title, top
    left, where the booklet's own pages carry theirs (8 pt, 12 mm from the top edge); title and subtitle on the 14 mm
    margin (were at 26 behind the number). G1: no "AGRICULTURE ANALYSIS · GROUP 6" line (page 2 had it)."""
    if hole:                                       # v1.5: a window left open for a plan placed under the page
        x0, y0, x1, y1 = hole
        pg.path([[(0, 0), (420, 0), (420, 297), (0, 297)], [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], fill=C["white"])
    else:                                          # v1.6 (Aras 27 Oct): white, the beige paper goes
        pg.rect(0, 0, 420, 297, fill=C["white"])
    if tag:                                        # v3: pages 1 and 3 name their booklet stage (accent, as its kicker)
        pg.text(tag, 14, HEAD_Y[0], 8, C["accent"], True)
    pg.text(title, 14, HEAD_Y[1], 22, C["ink"], True)
    pg.text(sub, 14, HEAD_Y[2], 11, C["ink2"])

# ------------------------------------------------------------------ pictograms and tiles
# v5 (T4a, 29 Oct, 02 §2): every pictogram comes from the shared icon set (common/icons.py); the script's own icon()
# with its 10 x 10 grid drawings is gone. AG_ICONS: tile key -> (icons.py name, crossed out).
AG_ICONS = {"nowater": ("drought", False), "cotton": ("field", False), "olive": ("olive", False),
            "drip": ("drip", False), "cube": ("storage", False)}


def _ag_put(pg, shapes):
    """icons.py house shapes ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw), page mm y up, on this Page"""
    for sh in shapes:
        if sh[0] == "poly":
            pg.poly(sh[1], fill=sh[2], stroke=sh[3], lw=sh[4] or 0.2, closed=True)
        else:
            pg.line(sh[1], sh[2], sh[3])


def _ag_icon(pg, kind, x, y, sz):
    """the icon set's pictogram for a tile key in the square (x, y - sz)-(x + sz, y)"""
    name, crossed = AG_ICONS.get(kind, (kind, False))
    _ag_put(pg, ico_draw(name, x + sz / 2.0, y - sz / 2.0, sz))
    if crossed:
        _ag_put(pg, ico_cross(x + sz / 2.0, y - sz / 2.0, sz))

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
            _ag_icon(pg, kind, tx + pad, yy - pad, ic)
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
# v4 (MIRAQUA 28 Oct, F5: public online sources only): the public sources keep their words, the project's own file
# pointers go from the printed key (kept here: NEWS research/water_data/03 §3; TUIK library/research/crops_2026-10-24
# §1.24-1.25; NET_REF research/water_balance/tables/C1). G11: corn, not maize, where printed (data keys stay "maize").
NEWS = "news: Ajans Bakırçay 19.03.2025"
TUIK = "TÜİK Bitkisel Üretim, Bergama 2025"
KAYA = "Kaya et al. 2017, Irrig. Drain. 66(5):820-827, Tables II, III, VI, pp.823-826 (deficit saving: Table II, S0.50 and S0.25 vs control)"
ITB = "İzmir Ticaret Borsası cotton report 2025, p.5"
NET_REF = ("net irrigation: FAO-56 (Allen et al. 1998), MGM/WMO 17742 normals, ERA5 1991-2025 scaled; per ha = FAO-56 "
           "daily soil balance net need (34 water years, Bergama climate) / 0.90 drip")
TAGEM = ("TAGEM/DSİ 2017 §12, Bergama station 17742 tables (net = ETc - 0.8 rain): cotton 829 mm, corn 765, "
         "tomato 606-825, olive 502-603")   # v5 (D13): was our check against our own figures
# v1.2: the context sentences as tiles (pictogram, heading, big figure, keyword lines, source)
# v2 (Aras 27 Oct, Prompt 5): the crops they name as "English (Turkish)"; figures and sources as they were
CONTEXT = [
    ("nowater", "DROUGHT 2025: NO WATER-HUNGRY CROPS", "7,500 ha",
     ["%s, %s, fodder · Bergama villages" % (name_lc("maize"), name_lc("cotton")),
      "no water for second crops · DSİ + Ministry"], NEWS),
    ("cotton", name_caps("cotton") + ": BERGAMA'S BIGGEST CROP", "10,000 ha",
     ["2025 · 37 % of 26,800 ha field crops",
      "%s 6,000 · %s 2,500 · %s 8,700 ha" % (name_lc("maize"), name_lc("tomato"), name_lc("olive"))], TUIK),
    ("olive", name_caps("olive") + " CAN TAKE LESS · MEMECIK, DRIP", "-72 % water",
     ["İzmir station 2008-10 · 175 vs 622 mm a season", "24.9 vs 27.8 kg a tree: no significant loss",
      "highest oil content"], KAYA),
    ("drip", "TODAY'S IRRIGATION ON THE FARMS", None, ["some Bergama growers moved to drip"], ITB),
]
def replaces():
    """v5.1: the "what it replaces" tile, its hectares live (NET is filled by build() before page_cubic runs)"""
    return [("cube", "THE WATER BOARD LINE IT REPLACES", u"10,000 m³ = {:.2f} ha {}".format(
        10000.0 / gross_m3_ha("olive", "dry"), name_lc("olive")),   # v3.1: (Zeytin)
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
    P.text(pg, "Bergama's %s and %s" % (name_lc("cotton"), name_lc("olive")), x, top - 3.8, 7.5, C["ink"])   # v2
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
        if P.put(pg, cited(lab, ref), X((a + b) / 2.0 if b else a), yb + (0.6 if up else -0.6), 7, col, False, region=reg,
                 gap=2.0, up=up, lanes=4, lead_col=col, stick=True) is None:
            LOG_NOTES.append("p1 history label left out (no free place): " + lab)
    return ya - 15.0


CROP_ROW = ("olive", "cotton", "maize", "tomato")   # v2 (Aras 27 Oct, Prompt 5): the crops page 1 compares


def crop_row(pg, x, top, w, floor):
    """v2 (Aras 27 Oct, Prompt 5): "THE CROPS": page 1's crops as photos in one row (PHOTO_W x PHOTO_H each, spread
    over w), the name "English (Turkish)" and the photo's credit [n] under each. Left out (and logged) when it would not
    fit above `floor` with two name lines. Returns its bottom y or None."""
    n = len(CROP_ROW)
    gx = (w - n * PHOTO_W) / (n - 1.0)
    if top - 3.0 - PHOTO_H - 2.5 - 2.6 - 0.6 < floor or gx < PH_GAP:
        LOG_NOTES.append("p1 crop photos left out: no room above the 'what it replaces' tile")
        return None
    pg.text("THE CROPS", x, top, 9, C["accent"], True)
    low = top
    for i, key in enumerate(CROP_ROW):
        px = x + i * (PHOTO_W + gx)
        photo_frame(pg, 0, key, px, top - 3.0)
        yy = top - 3.0 - PHOTO_H - 2.5
        for q in name_lines(key, photo_mark(key), 7, PHOTO_W):
            pg.text(q, px, yy, 7, C["ink"], True)
            low = min(low, yy - 0.6); yy -= 2.6
    ag_crop("ag1_crops", 0, x - 1.0, low - 1.0, x + w + 1.0, top + 4.0)
    return low


# ------------------------------------------------------------------ v3 (Prompt 6): the stream comes first
P1_X = 14.0                          # v4 (MIRAQUA 28 Oct, F10): page 1's left column on the 14 mm margin with the title
                                     # (was 26, behind the page number that is gone)
PRIORITY =[(1, "stream: summer strip"), (2, "on-site planting, on the strip's water"), (3, "farms outside the site")]
AG_STEP_MM = 4.0                     # v5 (T4a): the flow-step marker (icons.py ico_step), mm


def chip(pg, x, y, n, label, size=7.5):
    """v3: a numbered step, the label after it (baseline y). Returns x after it. v5 (T4a, 02 §2): the marker is the
    icon set's flow-step marker (icons.py ico_step), its number written in it, never under 7 pt."""
    s = AG_STEP_MM
    sh, (ax, ay), th, cap = ico_step(x + s / 2.0, y + 1.1, s, "solid", C["accent"])
    _ag_put(pg, sh)
    pg.text(str(n), ax, ay - cap / 2.0, max(7.0, cap / 0.716 / 0.3528), th, True, "C")
    pg.text(label, x + s + 1.2, y, size, C["ink"])
    return x + s + 1.2 + text_w(label, size)


def step_arrow(pg, x, y):
    """v3: a small arrow, 4 mm long, at the mid-height of a label on baseline y. Returns x after it."""
    ym = y + 1.1
    pg.line([(x, ym), (x + 3.0, ym)], C["ink2"], 0.3)
    pg.poly([(x + 2.9, ym + 0.8), (x + 4.0, ym), (x + 2.9, ym - 0.8)], fill=C["ink2"], closed=True)
    return x + 4.0


def chips(pg, x, y, steps, size=7.5):
    """v3: numbered steps in one row, an arrow between two, from x on baseline y"""
    for i, (n, lab) in enumerate(steps):
        if i: x = step_arrow(pg, x + 1.5, y) + 1.5
        x = chip(pg, x, y, n, lab, size)
    return x


def squeeze(ys):
    """v3: the double squeeze, dry year against normal, from the water balance's year_split (one daily run of the
    design store): water left for the farms after the strip (carried in + filled - strip), the farms' need per hectare
    (the same fields both years, so their need) and the hectares that water serves = left / need per ha. Fractions."""
    n, d = ys["normal"], ys["dry5"]
    left = lambda q: q["carried_in_m3"] + q["filled_m3"] - q["strip_m3"]
    a = left(d) / max(left(n), 1.0) - 1.0
    b = d["farm_need_m3"] / max(n["farm_need_m3"], 1.0) - 1.0
    return a, b, (1.0 + a) / (1.0 + b) - 1.0


def pc(v):
    """v3: a change as a signed whole percent, "+11 %", "-2 %", "0 %" """
    return "0 %" if abs(v) < 0.005 else "%+.0f %%" % (100.0 * v)


def stream_first(pg, L, src, y_top):
    """v3 (Aras 27 Oct 17:35, Prompt 6 task 1: "the board sends LESS water to farms in a 1-in-5 dry year than storage
    holds ... show the defence ON the board"): the priority as numbered steps; the design store through a normal and the
    1-in-5 dry water year, two stacked bars on one scale from x 70 (the hectare bars' origin): strip (it also waters the
    bed planting: the model has no draw of its own for it), farms (light normal, deep dry, as the bars below), left over
    (carried on, or back to the stream after 365 days), the store size dashed across both; then the double squeeze.
    All from the water balance results (design.year_split); without them only the priority row. Returns the bottom y."""
    yA = y_top - 3.5
    pg.text("THE STREAM COMES FIRST", P1_X, yA, 9, C["accent"], True)
    chips(pg, P1_X + text_w("THE STREAM COMES FIRST", 9, True) + 5.0, yA, PRIORITY)
    ys = L.get("year_split")
    if not (ys and "normal" in ys and "dry5" in ys):
        LOG_NOTES.append("FLAG p1: the water balance results have no year_split (water balance v4 has not run): the "
                         "normal and dry-year bars and the squeeze line are left out")
        ag_crop("ag1_stream", 0, P1_X - 2.0, yA - 2.0, 266.0, y_top + 1.0)
        return yA - 1.0
    mix = L.get("design_mix") or "design mix"
    mix_t = " + ".join(name_lc(w.split()[-1]) if w.split() and w.split()[-1] in PLANTS else w for w in mix.split(" + "))
    SRC_Y = ("normal and 1-in-5 dry year: " + src + "; design store, " + mix_t + "; one daily run of the store over 34 "
             "water years: normal = the year of median farm need, dry = the 1-in-5 dry year of farm need; carried in + "
             "filled = strip + farms + left over; left for farms = carried in + filled - strip; hectares = left for farms "
             "/ need per hectare (calculated)")
    mk = cite(SRC_Y)
    V = float(ys.get("storage_m3") or 0.0)
    YRS = (("normal", "normal year", C["green_light"], C["ink"]), ("dry5", "1-in-5 dry year", C["green_deep"], C["white"]))
    tot = dict((k, ys[k]["carried_in_m3"] + ys[k]["filled_m3"]) for k, _, _, _ in YRS)
    x0, BW = 70.0, 140.0
    kx = BW / max(max(tot.values()), V, 1.0)
    v_t = lambda v: fmt(rnd(v, 1000 if v >= 10000 else 100))
    b1 = yA - 7.0                                  # the normal bar's top; the dry bar 11 mm under it
    for j, (k, lab, fcol, fink) in enumerate(YRS):
        d = ys[k]
        top = b1 - 11.0 * j; bot = top - 6.0
        segs = [(d["strip_m3"], C["water_deep"], C["white"]), (d["farms_m3"], fcol, fink),
                (max(0.0, tot[k] - d["strip_m3"] - d["farms_m3"]), C["faint"], C["ink"])]
        xs, out_x = x0, -1e9                       # out_x: where the last outside value ended (pushed right past it)
        for v, col, ink in segs:
            w_ = kx * v
            if w_ > 0.05:
                pg.rect(xs, bot, w_, 6.0, fill=col)
            t = v_t(v)
            if v >= 0.5:                           # v3.1: the block's small words 7 pt, the smallest size (were 6.5)
                tw_ = text_w(t, 7, True)
                if tw_ + 1.6 <= w_:                # inside, centred
                    pg.text(t, xs + w_ / 2.0, bot + 2.2, 7, ink, True, "C")
                else:                              # outside: over the normal bar, under the dry bar
                    tx = max(xs + w_ / 2.0 - tw_ / 2.0, out_x + 1.5)
                    pg.text(t, tx, top + 0.9 if j == 0 else bot - 2.9, 7, C["ink"], True)
                    out_x = tx + tw_
            xs += w_
        pg.text(lab, x0 - 3.0, top - 2.6, 8, C["ink"], True, "R")
        pg.text("water year " + d["water_year"], x0 - 3.0, bot + 0.6, 7, C["ink2"], align="R")
        pg.text("%s m³ through the store" % v_t(tot[k]), x0 + BW + 4.0, top - 2.4, 7.5, C["ink"], True)
        pg.text("stream's winter flow: %.0f %% of a median year" % d["winter_flow_pct_of_median"], x0 + BW + 4.0,
                bot + 0.6, 7, C["ink2"])
    if V > 0:                                      # the store size, dashed across both bars
        xv = x0 + kx * V
        pg.line([(xv, b1 - 17.8), (xv, b1 + 0.8)], C["ink"], 0.35, (1.0, 0.7))
    lg = b1 - 17.0 - 7.0                           # the legend row, then the squeeze in two lines
    xx = P1_X
    for kind, cols, lab in (("fill", (C["water_deep"],), "strip, also waters the bed planting"),
                            ("fill", (C["green_light"], C["green_deep"]), "farms: normal · dry year"),
                            ("fill", (C["faint"],), "left: carried on, or back to the stream after a year"),
                            ("dash", (C["ink"],), "store %s m³ %s" % (fmt(V), mk))):
        for c_ in cols:
            if kind == "fill":
                pg.rect(xx, lg - 0.3, 3.5, 2.6, fill=c_); xx += 4.0
            else:
                pg.line([(xx + 1.7, lg - 0.6), (xx + 1.7, lg + 2.6)], c_, 0.35, (1.0, 0.7)); xx += 4.0
        pg.text(lab, xx + 0.8, lg, 7, C["ink"])           # v3.1: 7 pt (was 6.5)
        xx += 0.8 + text_w(lab, 7) + 5.0
    a, b, c = squeeze(ys)
    pg.text("1-in-5 dry year vs normal year: left for farms after the strip %s · need per hectare %s · hectares %s %s" % (
        pc(a), pc(b), pc(c), mk), P1_X, lg - 4.0, 7.5, C["accent"], True)
    if b > 0.0 and a <= 0.0:                       # what the run shows, said as it is (the log flags the other cases)
        t2 = "so the hectares fall faster than the volume: why deficit-irrigated %s is the lever" % name_lc("olive")
    elif b > 0.0 and c < 0.0:
        t2 = "the need per hectare outgrows the water left: why deficit-irrigated %s is the lever" % name_lc("olive")
    else:
        t2 = "the hectares hold in this dry year: the store covers it"
    pg.text(t2, P1_X, lg - 7.4, 7.5, C["ink"])
    if a > 0.0 or b <= 0.0:
        LOG_NOTES.append("MODEL p1: the dry year (%s) leaves the farms %s water after the strip and needs %s per hectare: "
                         "the squeeze is %s" % (ys["dry5"]["water_year"], pc(a), pc(b),
                                                "the need per hectare only" if b > 0.0 else "not there this time"))
    n_, d_ = ys["normal"], ys["dry5"]
    LOG_NOTES.append("p1 stream first (%s, store %s m3): normal %s / dry %s: in %s / %s m3 (filled %s / %s), strip %s / %s, "
                     "farms %s / %s of need %s / %s; left for farms %s, need per ha %s, hectares %s; winter flow %.0f / %.0f %% "
                     "of median" % (mix, fmt(V), n_["water_year"], d_["water_year"], fmt(tot["normal"]), fmt(tot["dry5"]),
                                    fmt(n_["filled_m3"]), fmt(d_["filled_m3"]), fmt(n_["strip_m3"]), fmt(d_["strip_m3"]),
                                    fmt(n_["farms_m3"]), fmt(d_["farms_m3"]), fmt(n_["farm_need_m3"]),
                                    fmt(d_["farm_need_m3"]), pc(a), pc(b), pc(c), n_["winter_flow_pct_of_median"],
                                    d_["winter_flow_pct_of_median"]))
    ag_crop("ag1_stream", 0, P1_X - 2.0, lg - 9.0, 266.0, y_top + 1.0)
    return lg - 8.2


def page_cubic(L, src):
    pg = Page(420, 297)
    header(pg, "WHAT EACH CUBIC METRE GROWS",
           "Same storage, different crops: hectares irrigated a season", tag=STAGE_TAG)
    s_lo, s_hi = span(L["storage_m3"]); p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0          # m3 the storage gives the farms in the 1-in-5 dry year
    fed = L["cropland_ha"] + L["orchard_ha"]
    SRC1 = "storage, need and share: " + src + "; water to farms = 1-in-5 dry-year need x share covered (calculated)"
    MIX = ("Bergama mix = cotton, corn and tomato weighted by their 2025 district areas; no map shows what the 34.9 ha grow, "
           "so the mix stands in; water balance crops: %s" % (", ".join(crop_word(c) for c in L["crops"]) or "not set"))
    # key line (v4, F10: on the 14 mm margin with the title, was 26)
    pg.text("%s-%s m³" % (fmt(rnd(s_lo)), fmt(rnd(s_hi))) if rnd(s_lo) != rnd(s_hi) else "%s m³" % fmt(rnd(s_lo)), P1_X, 250, 26, C["water_deep"], True)
    pg.text("storage · cost cut-off " + cite(SRC1), P1_X, 242, 9, C["ink"])
    pg.text("%s-%s m³" % (fmt(rnd(w_lo)), fmt(rnd(w_hi))), 120, 250, 26, C["green_deep"], True)
    pg.text("to farms · 1-in-5 dry year · %s %% of need · strip first" % (("%.0f" % p_lo) if "%.0f" % p_lo == "%.0f" % p_hi else "%.0f-%.0f" % (p_lo, p_hi)), 120, 242, 9, C["ink"])
    # bars: hectares served by W, per crop (v2, Prompt 5: the crop names "English (Turkish)")
    rows = [(plant_name("olive") + ", full irrigation", "olive", None), (plant_name("olive") + ", deficit irrigation", "olive", DEFICIT)] + \
           [(plant_name(c) if c in PLANTS else c.capitalize(), c, None) for c in sorted(NET) if c != "olive"] + [("Bergama mix (TÜİK 2025)", "mix", None)]
    stream_first(pg, L, src, 236.0)                 # v3 (Prompt 6): between the headline and the bars
    x0, y0, gw = 70, 181, 190                       # v3: y0 was 214, the stream-first block sits above
    RP = 16.5                                       # v3: rows 16.5 mm apart (were 19.5)
    yb_ = y0 - (len(rows) - 1) * RP - 13.5           # the last row's dry bar bottom (= the grid's foot, as before)
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
        pg.line([(xx, yb_), (xx, y0 + 6)], C["faint"], 0.2)
        pg.text("%d ha" % t, xx, yb_ - 4.5, 7, C["ink2"], align="C")
    xf = x0 + gw * fed / vmax
    pg.line([(xf, yb_), (xf, y0 + 9)], C["accent"], 0.5, (1.5, 1.0))
    pg.text("farms we feed: %s ha" % fmt1(fed), xf + 1.2, y0 + 7.5, 7.5, C["accent"], True)
    for i, (lab, crop, d) in enumerate(rows):
        yy = y0 - i * RP
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
    ag_crop("ag1_bars", 0, 13.0, yb_ - 5.5, 277.0, y0 + 11.0,
            legend=[{"kind": "fill", "colour": C["green_light"], "label": "normal year"},
                    {"kind": "fill", "colour": C["green_deep"], "label": "1-in-5 dry year"},
                    {"kind": "line", "colour": C["accent"], "label": "farms we feed"}])
    ag_crop("ag1_headline", 0, P1_X - 2.0, 239.0, 262.0, 261.0)
    # key to the two bars
    ky = yb_ - 10.0
    pg.rect(x0, ky, 6, 3, fill=C["green_light"]); pg.text("normal year (mean of 34)", x0 + 8, ky + 0.5, 7, C["ink"])
    pg.rect(x0 + 52, ky, 6, 3, fill=C["green_deep"]); pg.text("1-in-5 dry year", x0 + 60, ky + 0.5, 7, C["ink"])
    pg.rect(x0 + 92, ky, 6, 3, stroke=C["green_deep"], lw=0.35); pg.text("open bar: range (storage span; deficit 44-72 % saving)", x0 + 100, ky + 0.5, 7, C["ink"])
    # reading
    best = [q for q in vals if q[1] == "olive" and q[6] and q[2] == "dry"][0]     # v2: olive with deficit (not by its label)
    worst = max((q for q in vals if q[1] not in ("olive", "mix") and q[2] == "dry"), key=lambda q: q[3])     # the thirstiest field crop
    pg.rect(14, 14, 250, 59, stroke=C["faint"], lw=0.3)       # v1.6: white page, the box only outlined (v3: 14-73)
    pg.text("THE READING", 20, 65, 10, C["accent"], True)    # v3: the reading 19 mm lower (was 32-92), as the bars
    # v1.2: the conclusion as the two dry-year bars (same scale) and the big ratio between them
    bmax, bx0, bw = best[5] * 1.05, 20, 150
    for k_, (q, lab) in enumerate(((worst, "%s, 1-in-5 dry year" % (plant_name(worst[1]) if worst[1] in PLANTS else worst[1].capitalize())),
                                   (best, best[0] + ", 1-in-5 dry year"))):         # v2: names "English (Turkish)"
        yb = 51 - k_ * 18
        pg.text(lab, bx0, yb + 1.5, 8, C["ink"], True)
        pg.rect(bx0, yb - 7, bw * q[4] / bmax, 7, fill=C["green_deep"])
        if q[5] > q[4] * 1.01:
            pg.rect(bx0 + bw * q[4] / bmax, yb - 7, bw * (q[5] - q[4]) / bmax, 7, fill=None, stroke=C["green_deep"], lw=0.35)
        pg.text("%s-%s ha" % (fmt(q[4]), fmt(q[5])), bx0 + bw * q[5] / bmax + 2, yb - 5.2, 9, C["ink"], True)
    bkx = 192
    pg.line([(bkx - 2, 47.5), (bkx, 47.5), (bkx, 29.5), (bkx - 2, 29.5)], C["accent"], 0.5)
    pg.text("%.1f-%.1f x" % (best[4] / worst[4], best[5] / worst[5]), bkx + 3, 36, 24, C["accent"], True)
    pg.text("as much land, same storage", bkx + 3, 30.5, 7.5, C["ink"])
    pg.text("lever: crop + irrigation method, more than storage", 20, 21, 8, C["ink"], True)
    pg.text("same water: more farmland · same farms: less storage", 20, 17, 8, C["ink"])
    ag_crop("ag1_reading", 0, 18.0, 14.5, 262.0, 62.0)
    # context column
    cx, cy = 280, 250
    pg.text("WHY CROP CHOICE IS THE LEVER", cx, cy, 11, C["ink"], True)
    yb_ = tiles(pg, cx, cy - 6, 126, CONTEXT)
    ag_crop("ag1_context", 0, cx - 1.0, yb_ - 1.0, cx + 127.0, cy - 5.0)
    hb = history_line(pg, cx, yb_ - 7.0, 126.0, 64.0)          # v1.6: why the stored water goes to farms
    if hb:
        ag_crop("ag1_history", 0, cx - 1.0, hb - 1.0, cx + 127.0, yb_ - 3.0)
    crop_row(pg, cx, (hb or yb_) - 7.0, 126.0, 64.0)           # v2 (Prompt 5): the crops as photos, above "what it replaces"
    pg.text("WHAT IT REPLACES", cx, 60, 9, C["accent"], True)
    yb_ = tiles(pg, cx, 57, 126, replaces())
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
    header(pg, "THE FARMS WE FEED", "Fields and orchards the stored water serves, on the site plan \"What is there\"",
           hole=hole if G else None)
    WC = "ESA WorldCover 2021 v200, 10 m (CC BY 4.0)"                # v4 (F5): read from Data/landcover
    NEED2 = "need: FAO-56 soil balance / 0.90 drip, normal and 1-in-5 dry years"
    SRC2 = "farm areas from " + src
    # v4 (MIRAQUA 28 Oct, F5): no [n] for what is not public online: the orchards (course survey symbols
    # SEMBOL_ZEYTINLIK / SEMBOL_MEYVA_BAH), the extent (around2.pdf registered to the survey) and the base (the site
    # board's own plan 01, cut and scaled, not redrawn) are said on the page without a mark
    # context line (review global rule 4): what it shows, why it is here, what to take from it; v4: 0.7 mm lower, under
    # the subtitle's new baseline (header)
    pg.text(cited("The site plan \"What is there\" with the fields and orchards our stored water serves outlined: the "
                  "farms read off the same base, colours and key as the site", None if G else WC),
            14, 264.8, 8.5, C["ink"])
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
              "as " + " / ".join(crop_word(c_) for c_ in cc) + " " + cite(TUIK),   # v4 (G11): corn, not maize
              "inside the site %s ha · outside %s ha %s" % (fmt1(f_in), fmt1(f_out), cite(WC))]),
            ("outline2", C["accent_deep"], "orchards", "%s ha" % fmt1(fed_o),             # v4 (F5): survey, no mark
             ["%s-%s m³ a season" % (fmt(rnd(fed_o * o_lo, 100)), fmt(rnd(fed_o * o_hi, 100))), "as olive"]),
            ("dash", C["ink"], "the extent they lie in", "%s ha" % fmt(L.get("extent_ha", 455.0)), [])]
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
    ag_crop("ag2_plan", 1, 13.0, min(y, wy0) - 1.0, 407.0, 267.6, den)   # v4: under the subtitle (269.5 now)
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

# ------------------------------------------------------------------ sources that are not public (F5, D13)
# v4 (MIRAQUA 28 Oct, F5, Aras 28 Oct 11:38 "remove non-public citations"): the project's own record or internal
# research cards are not public online: cite() gives them no [n] and they leave the key; their words stay on the page
# as our own design statement. Facts now without a public source (reported): Tersane cotton (16th c.), ginning 1861,
# Sümerbank (1954/60-2008), the 19th-c. olive-oil machinery in the Red Hall S rotunda.
# v5 (T4a, 29 Oct, D13): also every source that names our own model run or method (F5_INTERNAL, by its words), and no
# status word (calculated, assumed ...) is ever printed in a source (F5_STATUS); page 3 (the plant ladder) is gone (D9 a).
F5_OFF = (COTTON_H, OLIVE_H)
F5_INTERNAL = ("water balance results", "default-lands copy", "farm areas from", "Bergama mix = ", "our arithmetic")
F5_STATUS = re.compile(r"\s*\((?:calculated|assumed|estimated|interpolated|indicative|design value)\)|"
                       r"\s*\b(?:calculated|assumed|estimated|interpolated|indicative)\b", re.I)


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


# ------------------------------------------------------------------ v1.6: the sources page (Aras 27 Oct: no source footers)
def page_sources():
    """the sheet's one numbered source key, on its own page: the [n] marks on pages 1-3 refer to it, and the
    booklet's sources page reads it from here ("Sources by number:", as the old page footers)."""
    pg = Page(420, 297)
    pg.rect(0, 0, 420, 297, fill=C["white"])
    pg.text("SOURCES", 14, 279, 22, C["ink"], True)
    pg.text("Numbered as the [n] marks on pages 1-2", 14, 271.5, 11, C["ink2"])
    key = "Sources by number: " + "  ".join("[%d] %s" % (i + 1, k) for i, k in enumerate(SRC_KEY))
    pg.para(key, 14, 260, 392, 8, C["ink"], lead=1.35)
    return pg

# ------------------------------------------------------------------ v1.4: A3 booklet = crops of this sheet (booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own drawings. Each page function records its panels' rects
# (from the same numbers it lays them out with) in AG_CROPS; booklet_export writes them to blocks.json, with
# booklet/results.json (hectares per crop, same keys as v1.3). The v1.3 booklet redraws are gone.
#@include ../common/booklet_assets.py
AG_CROPS = []                        # (id, page index, (x0, y0, x1, y1) mm from the page's top-left, y down, den, legend, drop)
AG_CAPTIONS = {"ag1_headline": "Storage and water to the farms", "ag1_bars": "Hectares one storage irrigates, by crop",
               "ag1_reading": "Same storage: how much more land", "ag1_context": "Why crop choice is the lever",
               "ag1_replaces": "What it replaces", "ag1_crops": "The crops",   # v2: the crop photos
               "ag1_stream": "The stream comes first: a normal and a 1-in-5 dry year",   # v3 (Prompt 6)
               "ag2_plan": "The farms we feed, on the site plan"}   # v5 (D9 a): ag3_* gone with the ladder page


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
    ys = L.get("year_split")
    if ys and "normal" in ys and "dry5" in ys:      # v3 (Prompt 6): page 1's double squeeze, dry year against normal
        a_, b_, c_ = squeeze(ys)
        R["stream_first"] = {"water_years": [ys["normal"]["water_year"], ys["dry5"]["water_year"]],
                             "left_for_farms_change_pct": round(100.0 * a_, 1), "need_per_ha_change_pct": round(100.0 * b_, 1),
                             "hectares_change_pct": round(100.0 * c_, 1)}
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
    PHOTO_GOT.clear(); PHOTO_STATE.clear(); del PHOTO_LOG[:]   # v2: the plant photos, read once a press
    for _ in range(2):
        del AG_CROPS[:], SRC_KEY[:], LOG_NOTES[:], PHOTO_FR[:]      # v1.6: one source numbering for the whole sheet
        PHOTO_N[0] = 0
        pages = [page_cubic(L, src), page_farms(L, src)]       # v5 (D9 a): the plant ladder page is gone
        write_pdf(pages + [page_sources()], path)
        try:                                       # v1.5: the site board's plan 01 under the farms layer
            return src, put_base(path) + "\n" + put_photos(path)   # v2: then the photos (never raises)
        except PermissionError:
            raise
        except Exception as ex:                    # never an empty window: once more with the fallback drawing
            BASE_OFF[0] = True
            err = "farms map: FLAG the site plan could not be placed (%s: %s), fallback drawing" % (type(ex).__name__, ex)
    return src, err + "\n" + put_photos(path)

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
