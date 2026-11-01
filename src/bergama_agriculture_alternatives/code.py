# r: pymupdf==1.26.5
# CURRENT VERSION: bergama_agriculture_alternatives_v9.py = v9 (1 Nov 2026, round 4; what changed: the NEW IN / VERSION notes below)
# bergama_agriculture_alternatives_v8.py (v8, 31 Oct: round 3, p18 + p19 merged on ONE booklet page) · Thread 3 of the 22 Oct batch: three alternatives for the agriculture analysis
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

VERSION = "v9"  # v9 (round 4, S6b: booklet p19 rebuilt as story groups, real Arial text check, one trigger file); v8.3 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v8.2 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v8.1 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
# NEW IN v9 (round 4, 1 Nov, session S6b; P19.1, K4, G-R4-1/2/7/11; spec revision_2026-11-01_round4/handover/
#   S6b_p19_design_spec.md): booklet p19 "Where the clean water goes, and what it grows" is rebuilt as story groups,
#   each with ONE heading inside its first crop, the crops of a row sharing their top and bottom edges; every figure,
#   source and photo kept (K4), only the layout and the duplicate titles changed:
#   * ag1_stream 260 x 40 (group 2 "HOW MUCH WATER REACHES THE FARMS", was "THE STREAM COMES FIRST"); ag1_bars
#     194 x 72 (group 3 "HECTARES ONE STORAGE IRRIGATES, BY CROP"); ag1_context 194 x 72 (group 4 "WHY CROP CHOICE
#     IS THE LEVER": the reading's squares and 2.2-4.4 x on top, the four tiles under it); ag1_history 260 x 34 (group
#     5 "THE CROPS, THEN AND NOW"); ag1_crops 128 x 34 (the photos at the one booklet photo size). ag1_reading is no
#     crop any more (drawn inside ag1_context). Booklet captions of these crops are empty (the heading says it).
#   * G-R4-1: text widths from the real Arial (text_w = font_metrics.fm_width; common/text_w.py and the Helvetica
#     table gone); one TextPage per booklet crop (common/text_place.py): every text registered, the drawings no text
#     may touch (icons, bars, photos, squares) are keeps, a collision RAISES; log "overlap p19 <crop> checked n,
#     collisions 0" (lp_overlap_flag / ag_flags gone). ² and ³ are the embedded font's own glyphs (the raised 0.6 x
#     digit printed under 6 pt).
#   * G-R4-2: wrap and Page.para never leave a one-word last line. G-R4-7: the step chips' numbers through
#     common/marker.py mk_marker. G-R4-11: the timeline's "Red Hall" is Kızıl Avlu from the shared names table.
#   * Trigger: the script's own copies (common/chain_fire.py, gh_in_items.py, the globals scan) are replaced by
#     common/trigger.py trig_should_run (a press of the Button or a new done text on its own inputs); the log says
#     "trigger: <why>". results.json keys and the other crop ids are unchanged.
# NEW IN v8 (round 3, B4 · P18.1-P18.4, D8, G2, G3, G4, G17; spec revision_2026-10-31_round3/handover/B4_work/
#   spec_p18_merged.md): page 1's five booklet crops are drawn at 1:1 for ONE merged booklet page and carry "bk_w"
#   (the booklet keeps them 1:1): ag1_stream 260 x 40 mm (the to-farms headline folded in: ag1_headline is gone),
#   ag1_bars 227 x 66 (direct labels, no key row), ag1_context 161 x 66 (tiles 2 x 2), ag1_reading 128 x 31 (two
#   squares by area + the ratio), ag1_history 128 x 31 (no leader lines), ag1_crops 128 x 31. No strokes around tiles
#   or photos (G17). P18.2: the photos go in as plain images (common/plant_photos.py, A2) and the log says
#   "photos: n of m placed as images"; "FLAG overlap p18 <crop> n" per crop (label_place.py).
# NEW IN v7 (round 2, Aras 31 Oct 11:13: p18 + p19 on one page if legible, PG2 p18-19, M10): ag1_bars compact (rows
#   14 mm apart, bars 5 mm, grid 165 mm wide: about 239 x 98 mm, was 264 x 113); ag1_reading one strip 252 x 28 mm
#   (was 244 x 48): the two dry-year bars it repeated from ag1_bars are gone (a fact once), the ratio and the lever stay.
# Revision 30 Oct (T5, booklet p.19; M10, G4): every fact once in the booklet. Storage (p.10) is no longer printed
#   here (headline, store legend); the olive area is facts.py "8,705 ha", printed once (the olive bar row; the
#   cotton tile and the timeline no longer repeat the 2025 areas: "8,700" gone); the olive full-irrigation row prints
#   its normal-year need from facts.py (the dry-year need and 1.25 ha are p.18's); "what it replaces" (1.25 ha again,
#   and a note on an older board version) is gone with its crop ag1_replaces.
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
#@include ../common/grid.py
#@include ../common/text_place.py
#@include ../common/marker.py
#@include ../common/data/NAMES.py
#@include ../common/names.py
#@include ../common/data/FACTS.py
#@include ../common/facts.py
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
_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
# v9 (round 4, G-R4-1): ² and ³ are the embedded Arial's own glyphs again (pdf_fonts.py since 28 Oct): the v3 raised
# 0.6 x digit printed at 4.2-4.5 pt, under the booklet's 6 pt minimum the text placer enforces; the unembedded
# Helvetica that lost them in some viewers is gone. (v3's SUP, SUP_K, SUP_UP and sup_runs deleted.)


def text_w(s, size, bold=False):
    """v9 (round 4, G-R4-1): the REAL Arial advance width (font_metrics.fm_width) of s at size pt, in mm; the
    Helvetica table (common/text_w.py) is gone (a missing font raises FontMissing, no estimate)"""
    return fm_width(s, size, bold)


#@include ../common/pdf_fonts.py
#@include ../common/font_metrics.py

class Page:
    def __init__(self, w, h):
        self.w, self.h, self.ops, self.alphas = w, h, [], set()
        self.tp, self.tg = None, None    # v9 (G-R4-1): the open TextPage (one per booklet crop) and the text group
    def tgroup(self, start=True):
        """v9: start (or with False end) one text group: the lines of one word block may touch each other, never
        another text (TextPage pad)"""
        self.tg = ((self.tp._group() if self.tp is not None else "g") if start else None)
        return self.tg
    def keep(self, box, name, kind="drawing"):
        """v9: a drawing box (x0, y0, x1, y1, page mm y up) no text may touch, in the open TextPage"""
        if self.tp is not None:
            self.tp.keep(tuple(box), kind, name)
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
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", halo=None, allow=()):
        """one text, size in pt; v9: measured with the real Arial (text_w = fm_width) and, while a booklet crop's
        TextPage is open, registered in it (collisions raise at its check; allow = keep names / kinds it may sit on);
        ² / ³ are the font's own glyphs"""
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        if self.tp is not None and s.strip():
            self.tp.put(s, x, y, size, bold, "L", 0.0, group=self.tg, emit=False, allow=allow)
        k = 72 / 25.4
        b = b"".join(bytes([_ENC_EXTRA[ch]]) if ch in _ENC_EXTRA else ch.encode("cp1252", "replace") for ch in s)   # 25 Oct: ı İ ğ Ğ ş Ş spelt right
        b = b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
        if halo:                                   # v1.5: the sketches' text mask, a halo in the ground's colour
            self.ops.append("q %s %.2f w 1 j BT 2 Tr /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET Q" % (
                self._c(halo, True), size * 0.35, "F2" if bold else "F1", size, self._c(halo), x * k, y * k, b.decode("latin-1")))
        self.ops.append("BT /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET" % ("F2" if bold else "F1", size, self._c(col), x * k, y * k, b.decode("latin-1")))
    def para(self, s, x, y, w, size, col="4A3F35", bold=False, lead=1.3):
        """v9: wrapped by the no-widow wrap (G-R4-2), one text group (its lines may touch each other)"""
        g0 = self.tg
        self.tgroup()
        yy = y
        for ln in wrap(s, size, w, bold):
            self.text(ln, x, yy, size, col, bold); yy -= size * 0.3528 * lead
        self.tg = g0
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
    """greedy wrap at real widths (size pt, w mm); v9 (G-R4-2): never a one-word last line: the last word of the
    line before moves down while that line keeps two words or more and the last line still fits"""
    out, line = [], ""
    for word in s.split(" "):
        t = (line + " " + word).strip()
        if text_w(t, size, bold) > w and line: out.append(line); line = word
        else: line = t
    if line: out.append(line)
    while len(out) >= 2 and len(out[-1].split()) < 2 and len(out[-2].split()) >= 3:
        a = out[-2].split()
        t = a[-1] + " " + out[-1]
        if text_w(t, size, bold) > w:
            break
        out[-2], out[-1] = " ".join(a[:-1]), t
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


def photo_frame(pg, pi, key, x, top, boxes=None):
    """v2: the frame of a plant's photo, PHOTO_W x PHOTO_H mm, its top-left at (x, top) on page index pi: the photo
    recorded for put_photos, or "no photo" inside the frame. boxes: the frame is added (overlap test).
    v4 (MIRAQUA 28 Oct, G12): an empty frame says why, as the water board's cards: "no photo: " + the loader's reason
    (common/plant_photos.py: offline, Wikimedia refused (HTTP 429) press again later, file not found, licence ...),
    7 pt (the booklet's smallest), top left in the frame. v8 (G17): no outline; an empty frame is a pale fill."""
    p, _cr, why = photo_get(key)
    PHOTO_N[0] += 1
    if p:
        PHOTO_FR.append((pi, x, top - PHOTO_H, x + PHOTO_W, top, p))
    else:
        pg.rect(x, top - PHOTO_H, PHOTO_W, PHOTO_H, fill=C["paper"])
        pg.para(u"no photo: " + (why or u"not loaded"), x + 1.5, top - 4.0, PHOTO_W - 3.0, 7, C["ink2"], lead=1.2)
    if boxes is not None and p:                  # an empty frame carries its own words: no drawing box then
        boxes.append((x, top - PHOTO_H, x + PHOTO_W, top))
    if p:                                        # v9 (G-R4-1): no text on a photo
        pg.keep((x, top - PHOTO_H, x + PHOTO_W, top), "photo " + key, "photo")


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
    # v8 (P18.2, DATA-2): plant_photos.py's line "photos: n of m placed as images" (+ FLAG k missing); the booklet's
    # crop copy keeps plain images (A2), the photos went missing on p19 while they sat in Form XObjects
    out = ["%s · %d frame(s) drawn (cached/plant_photos)%s" % (photo_flag_line(), PHOTO_N[0], err)]
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
            "drip": ("drip", False)}


def _ag_put(pg, shapes):
    """icons.py / marker.py house shapes ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) / ("text", s, x,
    baseline y, size mm, colour, bold, align), page mm y up, on this Page (v9: text for the markers' glyphs)"""
    for sh in shapes:
        if sh[0] == "poly":
            pg.poly(sh[1], fill=sh[2], stroke=sh[3], lw=sh[4] or 0.2, closed=True)
        elif sh[0] == "text":
            pg.text(sh[1], sh[2], sh[3], sh[4] / 0.3528, sh[5], sh[6] if len(sh) > 6 else False,
                    sh[7] if len(sh) > 7 else "L")
        else:
            pg.line(sh[1], sh[2], sh[3])


def _ag_icon(pg, kind, x, y, sz):
    """the icon set's pictogram for a tile key in the square (x, y - sz)-(x + sz, y)"""
    name, crossed = AG_ICONS.get(kind, (kind, False))
    _ag_put(pg, ico_draw(name, x + sz / 2.0, y - sz / 2.0, sz))
    if crossed:
        _ag_put(pg, ico_cross(x + sz / 2.0, y - sz / 2.0, sz))

def tiles(pg, x, y, w, items, cols=1, s=1.0, boxes=None):
    """v1.2 (water board v1.6): facts as tiles: pictogram, keyword heading, the key figure large, short keyword lines and
    the source number. items = [(pictogram, heading, figure or None, [keyword lines], source or None)]. Returns the bottom y.
    v8 (G17): no frame and no fill: the tiles stand apart by whitespace on the grid; boxes gets each pictogram's square."""
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
            _ag_icon(pg, kind, tx + pad, yy - pad, ic)
            if boxes is not None:
                boxes.append((tx + pad, yy - pad - ic, tx + pad + ic, yy - pad))
            pg.keep((tx + pad, yy - pad - ic, tx + pad + ic, yy - pad), "tile icon " + kind, "icon")   # v9
            pg.tgroup()                              # v9 (G-R4-1): the tile's lines are one word block
            lx, ly = tx + 2 * pad + ic, yy - pad
            for ln in L3[0]:
                ly -= fh * 1.25 * k; pg.text(ln, lx, ly + fh * 0.25 * k, fh, C["ink"], True)
            if L3[1]: ly -= fh * 0.3 * k
            for ln in L3[1]:
                ly -= fb * 1.15 * k
                pg.text(ln, lx, ly + fb * 0.2 * k, fb, C["accent"] if big in FLAGGED else C["green_deep"], True)
            for ln in L3[2]:
                ly -= ft * 1.3 * k; pg.text(ln, lx, ly + ft * 0.3 * k, ft, C["ink"])
            pg.tgroup(False)
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
    ("cotton", name_caps("cotton") + ": BERGAMA'S BIGGEST CROP", "37 %",
     ["of 26,800 ha field crops · 2025"], TUIK),
    ("olive", name_caps("olive") + " CAN TAKE LESS · MEMECIK, DRIP", "-72 % water",
     ["İzmir station 2008-10 · 175 vs 622 mm a season", "24.9 vs 27.8 kg a tree: no significant loss",
      "highest oil content"], KAYA),
    ("drip", "TODAY'S IRRIGATION ON THE FARMS", None, ["some Bergama growers moved to drip"], ITB),
]
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
           ("olive", u"19th-c. olive-oil machinery · %s S rotunda" % landmark_name("kizil_avlu"), 1800, 1900, OLIVE_H)]
# v9 (round 4, G-R4-11): the landmark's Turkish name from the shared names table (was "Red Hall"); OLIVE_H keeps the
# card's own words (a record, never printed: F5_OFF)


def history_line(pg, x, top, w, h):
    """a timeline 1500-2030 with the cotton (above) and olive (below) history, labels placed by measured width (no
    overlaps), inside the box x..x + w, top..top - h. v8 (round 3, G3): no leader lines (a label that takes a higher
    lane stands there alone, in its line's colour). v9 (round 4, P19.1): booklet p19 group 5's first block (crop
    ag1_history, AG_HIST_W x AG_HIST_H): the group's heading in the band on top, the line "Bergama's cotton and olive"
    under it, the timeline AG_HIST_YA under the top (cotton labels one lane above it, olive labels under the years);
    its old title "WHY THE STORED WATER GOES TO FARMS" is the group heading's job now. Returns its bottom y."""
    P = Placer()
    ag_heading(pg, "THE CROPS, THEN AND NOW", x, top)
    P.text(pg, "Bergama's %s and %s" % (name_lc("cotton"), name_lc("olive")), x, top - 9.0, 7, C["ink"])   # v2
    ya = top - AG_HIST_YA
    X = lambda yr: x + 2.0 + (w - 4.0) * (yr - 1500) / 530.0
    pg.line([(X(1500), ya), (X(2030), ya)], C["ink"], 0.3)
    for yr in range(1500, 2001, 100):
        pg.line([(X(yr), ya - 0.8), (X(yr), ya + 0.8)], C["ink"], 0.3)
        P.text(pg, str(yr), X(yr) - text_w(str(yr), 7) / 2.0, ya - 3.4, 7, C["ink2"])
    reg = (x, top - h + 0.5, x + w, top - 10.4)
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
                 gap=1.2, up=up, lanes=3, leader=False) is None:
            raise TextError(u"p19 ag1_history: the label %r finds no free place on the timeline (shorten it)" % lab)
    return top - h


CROP_ROW = ("olive", "cotton", "maize", "tomato")   # v2 (Aras 27 Oct, Prompt 5): the crops page 1 compares


def crop_row(pg, x, top, w, boxes=None):
    """v2 (Aras 27 Oct, Prompt 5): "THE CROPS": page 1's crops as photos in one row (PHOTO_W x PHOTO_H each, the one
    photo size of the booklet, spread over w), the name "English (Turkish)" and the photo's credit [n] under each.
    v9 (round 4, P19.1): booklet p19 group 5's second block (crop ag1_crops, AG_CROPS_W x AG_CROPS_H) beside the
    timeline, which carries the group's heading: its heading band stays empty, the photos start on the shared content
    top AG_HEAD under the top; a name of two lines is one text group; the photos are keeps. boxes: the photo frames.
    Returns its bottom y."""
    n = len(CROP_ROW)
    gx = max(PH_GAP, (w - n * PHOTO_W) / (n - 1.0))
    pt = top - AG_HEAD
    low = pt - PHOTO_H
    for i, key in enumerate(CROP_ROW):
        px = x + i * (PHOTO_W + gx)
        photo_frame(pg, 0, key, px, pt, boxes)
        yy = pt - PHOTO_H - 2.6
        nl = name_lines(key, photo_mark(key), 6.5, PHOTO_W + gx - 1.0)
        pg.tgroup()
        for q in nl:
            pg.text(q, px, yy, 6.5, C["ink"], True)
            low = min(low, yy - 0.6); yy -= 2.5
        pg.tgroup(False)
    return low


# ------------------------------------------------------------------ v3 (Prompt 6): the stream comes first
AG_BAR_RP, AG_BAR_H, AG_BAR_O = 9.3, 3.8, 4.4   # v8: bars' largest row pitch, bar, dry bar offset, mm (v7 14, 5, 6)
# v9 (round 4, P19.1; spec revision_2026-11-01_round4/handover/S6b_p19_design_spec.md): booklet p19 is rebuilt as
# story groups, one heading each (GRID_TYPE heading, in a band AG_HEAD tall on top of every block, so the blocks of a
# booklet row share the content top). The crops' sizes, mm, drawn at 1:1 ("bk_w"; page columns in brackets):
#   row 2  ag1_stream 260 x 40 (8)  "HOW MUCH WATER REACHES THE FARMS"  | the water board's wb_decision (4)
#   row 3  ag1_bars   194 x 72 (6)  "HECTARES ONE STORAGE IRRIGATES, BY CROP" | ag1_context 194 x 72 (6) "WHY CROP CHOICE
#          IS THE LEVER": the reading (ag1_reading's squares and ratio, no crop of its own now) on top, the 4 tiles under
#   row 4  ag1_history 260 x 34 (8) "THE CROPS, THEN AND NOW" | ag1_crops 128 x 34 (4), the photos at the one booklet
#          photo size
# Each crop has ONE TextPage (common/text_place.py, real Arial widths): every text of the crop is registered, the
# drawings no text may touch are keeps, and a collision RAISES (log "overlap p19 <crop> checked n, collisions 0").
AG_HEAD = 6.0                        # v9: the group heading band, mm
AG_STREAM_W, AG_STREAM_H = grid_w(8), 40.0
AG_BARS_W, AG_BARS_H = grid_w(6), 72.0
AG_CTX_W, AG_CTX_H = grid_w(6), 72.0
AG_HIST_W, AG_HIST_H = grid_w(8), 34.0
AG_CROPS_W, AG_CROPS_H = grid_w(4), 34.0
AG_HIST_YA = 23.0                    # v9: the timeline's line under the block's top, mm
AG_READ_H = 18.0                     # v9: the reading's strip under the heading band in ag1_context, mm
AG_ST_LW = 76.0                      # ag1_stream: the left column (headline, key), mm
AG_ST_RW = 60.0                      # ag1_stream: room after the bars for the through-the-store lines, mm (v8 57)
AG_DBOX = {}                         # v8 (G3): crop id -> drawing boxes (page mm y up), page 1
PRIORITY =[(1, "stream: summer strip"), (2, "on-site planting, on the strip's water"), (3, "farms outside the site")]
AG_STEP_MM = 4.0                     # the flow-step marker's least size (marker.py), mm


def ag_heading(pg, text, x, top):
    """v9 (P19.1): a story group's ONE heading (GRID_TYPE heading: 10 pt bold, ink) in the block's heading band"""
    sz, _b, _ld, col = grid_style("heading")
    pg.text(text, x, top - 4.0, sz, col, True)


def ag_open(pg, cid, x0, top, W, H):
    """v9 (G-R4-1): the TextPage of booklet crop cid (x0..x0 + W, top - H..top, page mm y up): every text drawn until
    ag_close is registered in it"""
    pg.tp, pg.tg = TextPage(u"p19 " + cid, (x0, top - H, x0 + W, top), y_down=False), None
    AG_DBOX[cid] = AG_DBOX.get(cid, [])


def ag_close(pg, cid, x0, top, W, H):
    """v9: the crop's collision test (RAISES TextCollision on any hit; logs "overlap p19 <cid> checked n, collisions
    0"), then the crop itself (drawn at 1:1 for the booklet page)"""
    tp, pg.tp, pg.tg = pg.tp, None, None
    tp.check(True)
    ag_crop(cid, 0, x0, top - H, x0 + W, top, bk_w=W)


def chip(pg, x, y, n, label, size=7.5):
    """v3: a numbered step, the label after it (baseline y). Returns x after it. v9 (round 4, G-R4-7): the marker is
    the shared marker.py mk_marker (glyph centred on its ink box, 7 pt, at least AG_STEP_MM across, accent)."""
    s = AG_STEP_MM
    sh, _box, r = mk_marker(x + s / 2.0, y + 1.1, str(n), C["accent"], size_pt=7.0, r_min=s / 2.0)
    _ag_put(pg, sh)
    lx = x + s / 2.0 + r + 1.2
    pg.text(label, lx, y, size, C["ink"])
    return lx + text_w(label, size)


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


def ag_stream_block(pg, L, src, x0, top, hl):
    """v3 (Aras 27 Oct 17:35, Prompt 6 task 1: "the board sends LESS water to farms in a 1-in-5 dry year than storage
    holds ... show the defence ON the board"): the priority as numbered steps; the design store through a normal and the
    1-in-5 dry water year, two stacked bars on one scale: strip (it also waters the bed planting: the model has no draw
    of its own for it), farms (light normal, deep dry, as the hectare bars), left over (carried on, or back to the
    stream after 365 days), the store size dashed across both; then the double squeeze. All from the water balance
    results (design.year_split); without them only the priority row.
    v8 (round 3, was stream_first; the merged booklet page): crop ag1_stream, AG_STREAM_W x AG_STREAM_H at 1:1 from
    (x0, top): the left column (AG_ST_LW) holds the title, the to-farms headline hl = (value, line) (was its own crop
    ag1_headline) and the bars' key; the right column the steps, the two bars and the squeeze.
    v9 (round 4, P19.1): booklet p19 group 2's first block: the group heading "HOW MUCH WATER REACHES THE FARMS"
    (was the title "THE STREAM COMES FIRST") on the steps' line; one TextPage for the crop (ag_open / ag_close: a
    collision raises); the outside values never run under the row labels or into the through-the-store lines."""
    W, H = AG_STREAM_W, AG_STREAM_H
    xl, xr = x0, x0 + AG_ST_LW + 5.0
    ag_open(pg, "ag1_stream", x0, top, W, H)
    ag_heading(pg, "HOW MUCH WATER REACHES THE FARMS", xl, top)
    pg.text(hl[0], xl, top - 11.5, 16, C["green_deep"], True)
    yk = top - 16.0
    pg.tgroup()                                    # the headline's line(s): one word block
    for ln in wrap(hl[1], 7.5, AG_ST_LW):
        pg.text(ln, xl, yk, 7.5, C["ink"])
        yk -= 3.3
    pg.tgroup(False)
    chips(pg, xr, top - 4.0, PRIORITY)
    ys = L.get("year_split")
    if not (ys and "normal" in ys and "dry5" in ys):
        LOG_NOTES.append("FLAG p1: the water balance results have no year_split (water balance v4 has not run): the "
                         "normal and dry-year bars and the squeeze line are left out")
        ag_close(pg, "ag1_stream", x0, top, W, H)
        return
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
    xb = xr + 28.0                                 # v8: the bars' origin (their labels right-aligned before it)
    BW = x0 + W - 1.0 - AG_ST_RW - 4.0 - xb        # AG_ST_RW mm for the through-the-store lines after the bars
    BH, BP = 5.0, 9.5                              # v8: bar height, pitch (v3 6, 11)
    kx = BW / max(max(tot.values()), V, 1.0)
    v_t = lambda v: fmt(rnd(v, 1000 if v >= 10000 else 100))
    b1 = top - 10.0                                # the normal bar's top; the dry bar BP under it
    for j, (k, lab, fcol, fink) in enumerate(YRS):
        d = ys[k]
        bt = b1 - BP * j; bot = bt - BH
        segs = [(d["strip_m3"], C["water_deep"], C["white"]), (d["farms_m3"], fcol, fink),
                (max(0.0, tot[k] - d["strip_m3"] - d["farms_m3"]), C["faint"], C["ink"])]
        xs, out_x = xb, -1e9                       # out_x: where the last outside value ended (pushed right past it)
        for v, col, ink in segs:
            w_ = kx * v
            if w_ > 0.05:
                pg.rect(xs, bot, w_, BH, fill=col)
            t = v_t(v)
            if v >= 0.5:                           # v3.1: the block's small words 7 pt, the smallest size (were 6.5)
                tw_ = text_w(t, 7, True)
                if tw_ + 1.6 <= w_:                # inside, centred
                    pg.text(t, xs + w_ / 2.0, bot + 1.6, 7, ink, True, "C")
                else:                              # outside: over the normal bar, under the dry bar; v9: never left
                    # of the bars' origin (the row labels end 3 mm before it) nor into the through-the-store lines
                    tx = max(xs + w_ / 2.0 - tw_ / 2.0, out_x + 1.5, xb)
                    tx = min(tx, xb + BW + 3.0 - tw_)
                    pg.text(t, tx, bt + 0.9 if j == 0 else bot - 2.9, 7, C["ink"], True)
                    out_x = tx + tw_
            xs += w_
        pg.tgroup()                                # v9: the row's label and its water year: one word block
        pg.text(lab, xb - 3.0, bt - 2.2, 8, C["ink"], True, "R")
        pg.text("water year " + d["water_year"], xb - 3.0, bt - 5.3, 7, C["ink2"], align="R")
        pg.tgroup()                                # v9: the two lines after the bars: one word block
        pg.text("%s m³ through the store" % v_t(tot[k]), xb + BW + 4.0, bt - 2.2, 7.5, C["ink"], True)
        pg.text("stream's winter flow: %.0f %% of a median year" % d["winter_flow_pct_of_median"], xb + BW + 4.0,
                bt - 5.3, 7, C["ink2"])
        pg.tgroup(False)
    if V > 0:                                      # the store size, dashed across both bars
        xv = xb + kx * V
        pg.line([(xv, b1 - BP - BH - 0.8), (xv, b1 + 0.8)], C["ink"], 0.35, (1.0, 0.7))
    lg = yk - 1.1                                  # v8: the key in the left column, one row each
    for kind, cols, lab in (("fill", (C["water_deep"],), "strip, also waters the bed planting"),
                            ("fill", (C["green_light"], C["green_deep"]), "farms: normal · dry year"),
                            ("fill", (C["faint"],), "left: carried on, or back to the stream after a year"),
                            ("dash", (C["ink"],), ("store size " + mk).strip())):
        xx = xl
        for c_ in cols:
            if kind == "fill":
                pg.rect(xx, lg - 0.3, 3.5, 2.6, fill=c_); xx += 4.0
            else:
                pg.line([(xx + 1.7, lg - 0.6), (xx + 1.7, lg + 2.6)], c_, 0.35, (1.0, 0.7)); xx += 4.0
        pg.text(lab, xx + 0.8, lg, 7, C["ink"])           # v3.1: 7 pt (was 6.5)
        lg -= 3.6                                         # v9: 3.6 mm rows (was 3.4: the boxes kept 0.6 mm apart)
    a, b, c = squeeze(ys)
    pg.tgroup()                                    # v9: the squeeze and what it means: one word block
    pg.text("1-in-5 dry year vs normal year: left for farms after the strip %s · need per hectare %s · hectares %s %s" % (
        pc(a), pc(b), pc(c), mk), xr, top - 32.0, 7.5, C["accent"], True)
    if b > 0.0 and a <= 0.0:                       # what the run shows, said as it is (the log flags the other cases)
        t2 = "so the hectares fall faster than the volume: why deficit-irrigated %s is the lever" % name_lc("olive")
    elif b > 0.0 and c < 0.0:
        t2 = "the need per hectare outgrows the water left: why deficit-irrigated %s is the lever" % name_lc("olive")
    else:
        t2 = "the hectares hold in this dry year: the store covers it"
    pg.text(t2, xr, top - 35.6, 7.5, C["ink"])
    pg.tgroup(False)
    ag_close(pg, "ag1_stream", x0, top, W, H)
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


def page_cubic(L, src):
    pg = Page(420, 297)
    header(pg, "WHAT EACH CUBIC METRE GROWS",
           "Same storage, different crops: hectares irrigated a season", tag=STAGE_TAG)
    p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0          # m3 the storage gives the farms in the 1-in-5 dry year
    fed = L["cropland_ha"] + L["orchard_ha"]
    SRC1 = "storage, need and share: " + src + "; water to farms = 1-in-5 dry-year need x share covered (calculated)"
    MIX = ("Bergama mix = cotton, corn and tomato weighted by their 2025 district areas; no map shows what the 34.9 ha grow, "
           "so the mix stands in; water balance crops: %s" % (", ".join(crop_word(c) for c in L["crops"]) or "not set"))
    # the to-farms headline (v8: drawn in ag1_stream's left column); T5 (30 Oct, M10): the storage figure is p.10's
    hl = ("%s-%s m³" % (fmt(rnd(w_lo)), fmt(rnd(w_hi))), "to farms · 1-in-5 dry year · %s %% of need · strip first %s" % (
        ("%.0f" % p_lo) if "%.0f" % p_lo == "%.0f" % p_hi else "%.0f-%.0f" % (p_lo, p_hi), cite(SRC1)))
    # bars: hectares served by W, per crop (v2, Prompt 5: the crop names "English (Turkish)")
    rows = [(plant_name("olive") + ", full irrigation", "olive", None), (plant_name("olive") + ", deficit irrigation", "olive", DEFICIT)] + \
           [(plant_name(c) if c in PLANTS else c.capitalize(), c, None) for c in sorted(NET) if c != "olive"] + [("Bergama mix (TÜİK 2025)", "mix", None)]
    vals = []
    for lab, crop, d in rows:
        for yr in ("normal", "dry"):
            g = gross_m3_ha(crop, yr)
            if d: lo, hi = w_lo / (g * (1 - d[0])), w_hi / (g * (1 - d[1]))
            else: lo, hi = w_lo / g, w_hi / g
            vals.append((lab, crop, yr, g, lo, hi, d))
    # v9 (round 4, P19.1): the sheet holds the five crops as booklet p19 shows them (rows 2-4 of the page; row 1 and
    # row 2's right block are the water board's), each at its booklet size (1:1, "bk_w"), at their p19 x positions:
    #   row 2  ag1_stream (14, top 262)
    #   row 3  ag1_bars (14, top 216) | ag1_context (212, top 216)
    #   row 4  ag1_history (14, top 138) | ag1_crops (278, top 138)
    AG_DBOX.clear()
    ag_stream_block(pg, L, src, 14.0, 262.0, (hl[0], hl[1].strip()))
    ag_bars_block(pg, 14.0, 216.0, rows, vals, fed, MIX)
    best = [q for q in vals if q[1] == "olive" and q[6] and q[2] == "dry"][0]     # v2: olive with deficit (not by its label)
    worst = max((q for q in vals if q[1] not in ("olive", "mix") and q[2] == "dry"), key=lambda q: q[3])     # the thirstiest field crop
    ag_context_block(pg, 14.0 + AG_BARS_W + 4.0, 216.0, best, worst)
    ag_open(pg, "ag1_history", 14.0, 138.0, AG_HIST_W, AG_HIST_H)
    history_line(pg, 14.0, 138.0, AG_HIST_W, AG_HIST_H)       # v1.6: why the stored water goes to farms
    ag_close(pg, "ag1_history", 14.0, 138.0, AG_HIST_W, AG_HIST_H)
    cx = 14.0 + AG_HIST_W + 4.0
    ag_open(pg, "ag1_crops", cx, 138.0, AG_CROPS_W, AG_CROPS_H)
    crop_row(pg, cx, 138.0, AG_CROPS_W, AG_DBOX["ag1_crops"])   # v2 (Prompt 5): the crops as photos
    ag_close(pg, "ag1_crops", cx, 138.0, AG_CROPS_W, AG_CROPS_H)
    return pg


def ag_bars_block(pg, x0, top, rows, vals, fed, MIX):
    """page 1's main chart: hectares the storage irrigates per crop, a light (normal year) and a deep (1-in-5 dry
    year) bar each, the open end = the range (storage span; olive deficit saving 44-72 %), the values at the bar ends,
    "farms we feed" dashed. v8 (round 3, A3_3's bars with direct labels): crop ag1_bars, AG_BARS_W x AG_BARS_H at 1:1
    from (x0, top); no key row: the first row's values say "normal year" / "1-in-5 dry year", the open end is said on
    the top line; each row's name, need and Bergama area right-aligned before its bars.
    v9 (round 4, P19.1): booklet p19 group 3 (6 page columns, AG_BARS_W x AG_BARS_H): the group heading "HECTARES ONE
    STORAGE IRRIGATES, BY CROP" in the band on top, the top line under it; one TextPage (a collision raises); a row's
    three label lines are one word block, a value and its direct label too; the bars are keeps."""
    W, H = AG_BARS_W, AG_BARS_H
    BH, BO = AG_BAR_H, AG_BAR_O
    n = len(rows)
    ag_open(pg, "ag1_bars", x0, top, W, H)
    ag_heading(pg, "HECTARES ONE STORAGE IRRIGATES, BY CROP", x0, top)
    y0 = top - AG_HEAD - 6.0                         # the first row's top; the top line (farms we feed) above it
    RP = min(AG_BAR_RP, (y0 - (top - H + 4.5) - BO - BH) / max(n - 1, 1))
    yb_ = y0 - (n - 1) * RP - BO - BH                # the last row's dry bar bottom (= the grid's foot)
    texts = []                                       # per row: (name, need line, area line or None)
    for i, (lab, crop, d) in enumerate(rows):
        area = fact_num("olive_area_ha") if crop == "olive" else (fmt(TUIK_2025_DA[crop] / 10.0) if crop in TUIK_2025_DA else None)
        area_t = "Bergama 2025: %s ha %s" % (area, cite(TUIK)) if area and not (crop == "olive" and d) else None
        g_n, g_d = gross_m3_ha(crop, "normal"), gross_m3_ha(crop, "dry")
        if d: g_n, g_d = g_n * (1 - d[1]), g_d * (1 - d[0])
        mk = cite(NET_REF) + (cite(TAGEM) if i == 0 else "") + (cite(KAYA) if d else "") + (cite(MIX) if crop == "mix" else "")
        if crop == "olive" and not d:                 # T5 (M10): facts.py; the 1-in-5 dry-year need prints on p.18
            need_t = fact_text("olive_need_normal_m3_ha")
            need_t = "%s %s" % (need_t, mk) if need_t else None
        else:
            need_t = "%s-%s m³ per ha a season %s" % (fmt(rnd(min(g_n, g_d), 10)), fmt(rnd(max(g_n, g_d), 10)), mk)
        texts.append((lab, need_t, area_t))
    lw = max([text_w(t[0], 7.5, True) for t in texts] + [text_w(q, 6.5) for t in texts for q in t[1:] if q])
    xb = x0 + lw + 3.0                               # the bars' origin
    vmax = max(v[5] for v in vals) * 1.08
    DIRECT = {"normal": "  normal year (mean of 34)", "dry": "  1-in-5 dry year"}   # the first row's direct labels

    def vtext(v, first):
        t = "%s-%s ha" % (fmt(v[4]), fmt(v[5])) if fmt(v[4]) != fmt(v[5]) else "%s ha" % fmt(v[4])
        return t, (DIRECT[v[2]] if first else "")
    avail = x0 + W - 1.0 - xb                        # the grid as wide as the longest bar + its words allow
    gw = min((avail - 1.5 - text_w(t, 7.5, True) - text_w(e, 7)) / (v[5] / vmax)
             for v in vals for t, e in [vtext(v, v[0] == rows[0][0])])
    step = 25 if vmax < 160 else (50 if vmax < 400 else 100)
    for t in range(0, int(vmax) + 1, step):
        xx = xb + gw * t / vmax
        pg.line([(xx, yb_), (xx, y0 + 0.5)], C["faint"], 0.2)
        pg.text("%d ha" % t, xx, yb_ - 3.5, 7, C["ink2"], align="C")
    xf = xb + gw * fed / vmax
    pg.line([(xf, yb_), (xf, y0 + 2.0)], C["accent"], 0.5, (1.5, 1.0))
    ff = "farms we feed: %s ha" % fmt1(fed)
    pg.text(ff, xf + 1.2, top - AG_HEAD - 3.5, 7.5, C["accent"], True)
    rng = "open bar end: range (storage span; deficit 44-72 % saving)"
    pg.text(rng, x0 + W - 1.0, top - AG_HEAD - 3.5, 7, C["ink2"], align="R")
    boxes = AG_DBOX.setdefault("ag1_bars", [])
    for i, (lab, crop, d) in enumerate(rows):
        yy = y0 - i * RP
        name, need_t, area_t = texts[i]
        pg.tgroup()                                  # v9: the row's name, need and area: one word block
        pg.text(name, xb - 3.0, yy - 2.8, 7.5, C["ink"], True, "R")
        if need_t:
            pg.text(need_t, xb - 3.0, yy - 5.5, 6.5, C["ink2"], align="R")
        if area_t:
            pg.text(area_t, xb - 3.0, yy - 8.0, 6.5, C["accent"], align="R")
        pg.tgroup(False)
        for j, yr in enumerate(("normal", "dry")):
            v = [q for q in vals if q[0] == lab and q[2] == yr][0]
            by = yy - j * BO
            col = C["green_light"] if yr == "normal" else C["green_deep"]
            pg.rect(xb, by - BH, gw * v[4] / vmax, BH, fill=col)
            if v[5] > v[4] * 1.01:
                pg.rect(xb + gw * v[4] / vmax, by - BH, gw * (v[5] - v[4]) / vmax, BH, fill=None, stroke=col, lw=0.35)
            boxes.append((xb, by - BH, xb + gw * v[5] / vmax, by))
            pg.keep((xb, by - BH, xb + gw * v[5] / vmax, by), "bar %d %s" % (i, yr))
            t, e = vtext(v, i == 0)
            tx = xb + gw * v[5] / vmax + 1.5
            pg.tgroup()                              # v9: the value and its direct label: one word block
            pg.text(t, tx, by - BH + 0.9, 7.5, C["ink"], True)
            if e:
                pg.text(e, tx + text_w(t, 7.5, True), by - BH + 0.9, 7, C["ink2"])
            pg.tgroup(False)
    ag_close(pg, "ag1_bars", x0, top, W, H)


def ag_context_block(pg, x0, top, best, worst):
    """v9 (round 4, P19.1): booklet p19 group 4 "WHY CROP CHOICE IS THE LEVER" (crop ag1_context, AG_CTX_W x
    AG_CTX_H at 1:1 from (x0, top), 6 page columns, one TextPage): the lever first, then why.
      the reading (v1.2 THE READING; v8 its own crop ag1_reading, now the strip AG_READ_H under the heading band): the
        land one storage irrigates in the 1-in-5 dry year as squares by area: the thirstiest field crop = 1 (deep),
        deficit-irrigated olive = the ratio (deep up to its low end, open up to its high end, as the bars' open ends);
        beside them the ratio with what it compares (one word block), then the lever (one word block)
      the four context tiles 2 x 2 under it (v1.2 tiles at 0.9, no frames; each tile one word block, icons keeps)"""
    W, H = AG_CTX_W, AG_CTX_H
    ag_open(pg, "ag1_context", x0, top, W, H)
    ag_heading(pg, "WHY CROP CHOICE IS THE LEVER", x0, top)
    # the reading
    lo, hi = best[4] / worst[4], best[5] / worst[5]
    rt = "%.1f-%.1f x" % (lo, hi)
    st = top - AG_HEAD                               # the strip's top
    gy = st - AG_READ_H + 0.5                        # the squares stand on one line
    a = min(11.0, (AG_READ_H - 1.5) / math.sqrt(max(hi, 1.0)))   # 1 unit of land (a drawing size, not printed)
    xs = x0
    s_lo, s_hi = a * math.sqrt(max(lo, 0.0)), a * math.sqrt(max(hi, 0.0))
    xo = xs + a + 3.0
    pg.rect(xs, gy, a, a, fill=C["green_deep"])
    pg.rect(xo, gy, s_hi, s_hi, stroke=C["green_deep"], lw=0.35)
    pg.rect(xo, gy, s_lo, s_lo, fill=C["green_deep"])
    pg.keep((xs, gy, xs + a, gy + a), "reading square " + worst[1], "reading")
    pg.keep((xo, gy, xo + max(s_hi, s_lo), gy + max(s_hi, s_lo)), "reading square " + best[1], "reading")
    for cx_, side, key in ((xs, a, worst[1]), (xo, s_lo, best[1])):      # the crop's word in its deep square
        w_ = crop_word(key)
        sz = 6.5 if text_w(w_, 6.5, True) + 1.0 <= side else 6.0
        if text_w(w_, sz, True) + 1.0 <= side:
            pg.text(w_, cx_ + side / 2.0, gy + side / 2.0 - 0.8, sz, C["white"], True, "C", allow=("reading",))
        else:
            LOG_NOTES.append("FLAG p1 ag1_context: '%s' does not fit its %.1f mm square; the line beside the squares "
                             "names both crops" % (w_, side))
    tx = xo + max(s_hi, s_lo) + 5.0
    cwa = 60.0                                       # the ratio's column; the lever's column after it
    wname = plant_name(worst[1]) if worst[1] in PLANTS else worst[1].capitalize()
    pg.tgroup()                                      # the ratio, what it means and what it compares: one word block
    pg.text(rt, tx, st - 6.0, 18, C["accent"], True)
    pg.text("as much land, same storage", tx, st - 9.6, 7, C["ink"])
    yy = st - 12.6
    for ln in wrap("%s against %s, 1-in-5 dry year" % (best[0], wname), 6.5, cwa):
        pg.text(ln, tx, yy, 6.5, C["ink2"])
        yy -= 2.7
    pg.tgroup(False)
    lx = tx + cwa + 4.0
    pg.tgroup()                                      # the lever: one word block
    yy = st - 3.0
    for ln, b in [(q, True) for q in wrap("lever: crop + irrigation method, more than storage", 7, x0 + W - lx, True)] + \
                 [(q, False) for q in wrap("same water: more farmland · same farms: less storage", 7, x0 + W - lx)]:
        pg.text(ln, lx, yy, 7, C["ink"], b)
        yy -= 3.2
    pg.tgroup(False)
    # the four tiles 2 x 2 (v8: tiles at 0.9, no frames)
    AG_DBOX["ag1_context"] = []
    tiles(pg, x0, st - AG_READ_H - 1.5, W, CONTEXT, cols=2, s=0.9, boxes=AG_DBOX["ag1_context"])
    ag_close(pg, "ag1_context", x0, top, W, H)


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
# Sümerbank (1954/60-2008), the 19th-c. olive-oil machinery in the Kızıl Avlu S rotunda.
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
    out and named in the log (never drawn over another). v8: put(leader=False) for no leaders (G3)."""
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
            lead_col=None, stick=False, leader=True):
        """v8 (round 3, G3): leader=False draws no hair leader (a lifted label stands in its lane alone)"""
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
                lead = (bool(k) or stick) and leader
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
AG_CROPS = []                        # (id, page index, (x0, y0, x1, y1) mm from the page's top-left, y down, den, legend, drop,
#                                      bk_w or None)
# v8: ag1_headline gone (the to-farms headline is part of ag1_stream)
# v9 (round 4, P19.1): the p19 crops carry their group heading inside, so their booklet captions are empty;
# ag1_reading is drawn inside ag1_context and is no crop of its own any more
AG_CAPTIONS = {"ag1_bars": "", "ag1_context": "", "ag1_crops": "", "ag1_stream": "", "ag1_history": "",
               "ag2_plan": "The farms we feed, on the site plan"}   # v5 (D9 a): ag3_* gone with the ladder page


def ag_crop(cid, page, x0, y0, x1, y1, den=None, legend=None, drop=None, bk_w=None):
    """a panel of page `page` (0-2), given as the page's own y-up mm (x0, y0)-(x1, y1). v8: bk_w = the width (mm) it is
    drawn for on the booklet page (the booklet then prints it at that size, 1:1)"""
    AG_CROPS.append((cid, page, (round(x0, 2), round(297.0 - y1, 2), round(x1, 2), round(297.0 - y0, 2)), den,
                     legend or [], drop or [], bk_w))


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
    for cid, page, r, den, legend, drop, bk_w in AG_CROPS:
        bk.crop(cid, OUT_PDF, r, caption=AG_CAPTIONS.get(cid, ""), scale_den=den, legend=legend, page=page, drop=drop)
        if bk_w:                                   # v8: drawn for the booklet page at 1:1 (as city link, site board)
            bk.d["blocks"][cid]["bk_w"] = round(bk_w, 3)
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
        tp_log_lines()                             # v9: a second pass logs its own "overlap p19 ..." lines only
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
    flag = "".join("\n" + t for t in LOG_NOTES + tp_log_lines())   # v9 (G-R4-1): "overlap p19 <crop> checked n, collisions 0"
    flag += "\nFLAG: water balance results file not found in Downloads; its default-lands copy was used" if src == DEFAULT_NOTE else ""
    return "%s  %s\ntrigger: %s\nfigures: %s%s\n%s\nagriculture alternatives %s, %.1f s\n%s" % (
        OUT_PDF, time.strftime("%H:%M:%S"), TRIG_WHY[0], src, flag, base, VERSION, time.time() - t0, bk)

#@include ../common/trigger.py
TRIG_WHY = ["run outside Grasshopper"]   # v9 (round 4): what started this run, for the log ("trigger: <why>")


#@include ../common/done_text.py


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    # v9 (round 4): the one trigger file (common/trigger.py): a press of the Button (its rising edge) or a NEW done
    # text from the script before in the chain; the script's own trigger copies are gone
    _pressed, _why, _btn = trig_should_run("bergama_agri_alt_log_chain")
    TRIG_WHY[0] = _why
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
