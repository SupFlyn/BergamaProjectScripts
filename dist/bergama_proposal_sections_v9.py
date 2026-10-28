# -*- coding: utf-8 -*-
"""BERGAMA PROPOSAL SECTIONS v4 (2026-10-25): Group 6's four proposals in section, upstream to downstream, in the
water board's hand-drawn section style (Aras 25 Oct 11:38-11:45: "we want section from each proposal just like our
water board sections"; "the style of waterboard sections were really really good you can do it somewhere else").
For the studio session of 26.10.2026: "Sections: Illustrating the spatial relationships and key design decisions."

NEW IN v9 (MIRAQUA 28 Oct, booklet revision v4: F4, F7, F14, G5, G8, F5; bank depth research 28 Oct §4.6; a feature
  change, so the next whole number):
  * A key map of the four measured cuts under the upstream sketch (study area, Selinos, K4 and Üç Kemer bridges, north
    arrow, no scale), with the measured note that the K4 and K5 cuts lie about 114 m and 119 m downstream of the
    bridges their sketches draw.
  * Upstream: the right bank is the channel wall about 5 m above the bed (site photos 1 Oct 2026), so Q500 stays inside
    the banks as its label says. K4: Q500 drawn under the street and wall top. No level value changed.
  * Sub-hub floor and boardwalk drawn soft; legend entries for the yellow bands, the dashed route, the soft paving and
    the study area; bold keywords in the notes; [n] marks for public online sources only.

NEW IN v8.1 (bugfix, Aras 27 Oct, Prompt 8 final check): K5's winter crop row (herbs, greens, Cabbage (Lahana), Citrus
  (Narenciye), Quince (Ayva)) sits 2.2 lines under the summer row (was 1.5): at 1.5 its pictogram touched the summer
  row, and with no free place inside the drawing's reach declutter left the whole row out. The booklet caption of
  ps_all keys the numbered roundels (1-11 as in Collect, clean, hold; the sheet header that says so is outside the
  crop). The source key names public sources where the entry rested on a public one (levels, rain, olive and
  lavender: no internal file names). Nothing else changed.
NEW IN v8 (Aras 27 Oct 17:34, booklet Prompt 5 rule 8: "plants: English name (Turkish name), no Latin"): the plants and
  crops the sections name read "English (Turkish)": Oriental plane (Doğu çınarı), Olive (Zeytin), Stone pine (Fıstık
  çamı), French lavender (Karabaş otu), and Demeter's Garden's crops (Bean (Fasulye), Tomato (Domates) ...). The text
  under the component shows a newly pasted version at once, idle (Aras 27 Oct 15:35). Nothing else changed.
NEW IN v7 (Aras 27 Oct 11:07, revision_2026-10-27/PHASE2_SPEC.md): booklet p.18-19 become ONE page: the four
  sections sit in one 2 x 2 block shaped like the booklet's panel area (new crop ps_all), all at ONE common factor;
  words drawn large enough that the smallest prints >= 7 pt on that page (TXT_K, measured); titles short, keyword
  chips and long context paragraphs gone (one short note under each title); no source footer or credit line (the [n]
  key is written to the log). Labels never overlap: declutter() measures every label (text_w) and moves it to the
  nearest free place, or leaves it out and logs it. History (D8, D10, H4; Aras 12:05): K4 and K5 are walking hubs, a
  dry step-free hub square at street level above Q500 with plane trees (irrigated from storage) + a floodable sub-hub
  in the bed at the strip level, a walk down the steps between; K4 names Tabaklar Hamamı (~56 m downstream, card h02
  E08) on the terrace that faces it. Single crops ps_upstream, ps_k4, ps_k5, ps_downstream kept (tight).
OLDER VERSIONS: their notes are in HISTORY.md (repo SupFlyn/BergamaProjectScripts, src/bergama_proposal_sections/).

WHAT IT DRAWS: one A0 landscape sheet per form option (A = organic only where the project meets the water, B = no
organic forms), all vector, whole-string text, four panels:
  1 UPSTREAM ENTRY                     reed-basin cascade (water board v1.3's sketch)
  2 K4 BRIDGE · WALKING HUB            tiers W / F / D; hub square on D, sub-hub in the bed (v7)
  3 K5 BRIDGE · DEMETER'S GARDEN       garden on the dry top of the south-west bank (card i01, DG 1-2); hub square
                + WALKING HUB          on the other bank top, steps down, commons in the bed = sub-hub (v7)
  4 DOWNSTREAM REACH                   floodable planting WP 1-2 and the floodable boardwalk (ZONES.md)
  Sketch code, PDF writer and palette are copied from bergama_water_board_v1_3.py (its SKETCH_SRC); element numbers
  1-11 are the water board's. Levels printed on panels 3-4: surveyed cuts, research/rain_river_levels/README.md v1.1
  table (K5 Q500 +58.75 m, 2.79 m above the bed, inside the banks; NIL +48.00 m, 2.33 m, inside; flat end 1.54 m,
  banks about 114 m apart). Not drawn (not in any source): Demeter's Garden intake, lift and basin volume.
  OVERLAP (SCRIPT_STANDARD §5): panels 1-2 are also on the water board (W3a); to be merged after 26 Oct.

COMPONENT: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file. Input run (Button), outputs log and done.
Writes Downloads/Bergama/output/bergama_proposal_sections/Bergama_proposal_sections_{A,B}.pdf; log in
Downloads/Bergama/logs/bergama_proposal_sections_log.txt. Reads nothing from other scripts; palette from
Downloads/Bergama/Data/bergama_palette.py if there (else the built-in colours).
HOW WE KNOW IT WORKS: the text under the component reads "ProposalSections v1 · HH:MM · N s" and the log lists the
two PDFs; each opens as one A0 page with four sections.
"""
import os
import json
import math
import time
import zlib
import tempfile
import datetime
import types as _types

# ---- SETTINGS ----
VERSION = "v9"
GH_LABEL = "ProposalSections"
OUT_FOLDER = "bergama_proposal_sections"
LOG_NAME = "bergama_proposal_sections_log.txt"
OUT_NAME = "Bergama_proposal_sections_{}.pdf"

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
BERGAMA = BERGAMA_ROOT
OUT_DIR = bg_output(OUT_FOLDER)                    # final PDFs only (27 Oct)
LOG_DIR = bg_logs()


BOARD_W, BOARD_H = 1189.0, 841.0     # A0 landscape, mm

M = 14.0                             # board margin, mm

OPTIONS = ("A",)                     # v2: option A only (organic only where the project meets the water), Aras 16:43

COL = {
    "sheet": "F4F3EE", "paper": "EFEDE6", "faint": "D8D5CC", "structure": "B0AC9C", "ink2": "847E75",
    "ink": "4A3F35", "ink_dark": "2C2219", "white": "FFFFFF", "lane": "FAF8F1",
    "river": "91ADB4", "river_mid": "5D7F8D", "river_dark": "32525F", "bank": "C1D3DB",
    "lit": "D7D3C2", "shade": "BFBBAB", "edge3d": "949081", "ground": "E4E1D6", "soil": "CFC6B2",
    "soil_dk": "B5AA93", "accent": "8B3A3F",
    "aras_alan": "5C48A2", "begum_alan": "7F3902", "nil_alan": "107C73",
}

MP = {"storage": ("CBD9F8", "92A3C9", "3E4C6E"), "discharge": ("90C5D2", "4B92A3", "1B535E"),
      "wetland": ("CBEDE5", "8DB8AF", "2D564E"), "amphibious": ("C1D3DB", "889EA8", "3C5159"),
      "agriculture": ("C6C08D", "948B49", "534E25"), "park": ("DFEBC0", "A7B67F", "49522B")}

# ---------------------------------------------------------------- sources (short names printed on the board)
# v3: sources as [n] on the drawings, the numbered key in the footer (water board v1.6 cite() / SRC_KEY). Fixed
# order, so the numbers stay the same on every press.
# v9 (MIRAQUA 28 Oct, F5: public online sources only): the [n] of the concept record, Aras's tier text, card i01, the
# zone base, the course survey's road edges and the hub decisions are gone (with their entries); plane and hamam keep
# only their public sources; levels read as the water balance's (method + the DSİ design flow). In reading order.
SRC_KEY = [
    ("levels", u"levels: Manning normal depth, n 0.050, on the surveyed cross-sections; DSİ Q500 263.3 m³/s "
               u"(Danıştay 6. D. 2021/9521 E.)"),
    ("rain", u"MGM 17742 normals 1991-2020, seasonal shares of the year's rain (arithmetic)"),
    ("plane", u"Ottoman squares with plane trees: ICOMOS 2014, Evaluation No 1457, Pergamon and its Multi-Layered "
              u"Cultural Landscape, p. 281"),
    ("hamam", u"Tabaklar Hamamı across the stream from Ulu Cami: Köylü H., Ege Telgraf, 31 Dec 2025; KTB İzmir, Baths "
              u"(Hamams) in İzmir; about 56 m from K4: calculated on the survey"),
    ("plants", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter); FAO Ecocrop, olive (will not "
               u"tolerate waterlogged soils)"),          # v8.1: the public pages of BK_SOURCES, not the internal register
    ("gauges", u"DSİ gauge yearbooks 2016-2021"),
]


def cite(key):
    """v3: the number of a source in the footer key, as "[n]"."""
    return u"[{}]".format([k for k, _ in SRC_KEY].index(key) + 1)

# ---------------------------------------------------------------- text metrics, page and PDF writer (water loop v2)
_MCH = u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

_MW0 = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556,
        556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278,
        500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469,
        556, 333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500,
        278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584]

_MW1 = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556,
        556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278,
        556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584,
        556, 333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556,
        333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584]

_W = [dict(zip(_MCH, _MW0)), dict(zip(_MCH, _MW1))]

_WX = {u"·": 278, u"³": 333, u"²": 333, u"µ": 556, u"§": 556, u"İ": 278, u"ı": 278, u"–": 556, u"°": 400}

PT = 25.4 / 72.0

CAP = 0.716

def text_w(s, size, bold=False):
    w = _W[1 if bold else 0]
    return sum(w.get(c, _WX.get(c, 600 if c.isupper() else 556)) for c in s) / 1000.0 * size

# v9 (MIRAQUA 28 Oct, G5): the notes are wrapped and drawn by ps_rich_para (parts/80_key_map.py), with bold keywords

# ---------------------------------------------------------------- page and PDF writer (v1; see-through fills as bergama_diagrams v1.8)
class Page(object):
    def __init__(self, W, H):
        self.W, self.H, self.items = W, H, []

    def poly(self, rings, fill=None, stroke=None, lw=0.1, dash=None, stripes=None, layer=None, alpha=None):
        """alpha: opacity 0-1 of fill and stroke (steps of 0.05; None = opaque). layer: unused (tree block API)."""
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            self.items.append(("poly", rings, fill, stroke, lw, dash, stripes, alpha))

    def line(self, pts, stroke, lw=0.1, dash=None, cap=1, layer=None):
        if len(pts) >= 2:
            self.items.append(("line", pts, stroke, lw, dash, cap))

    def circle(self, cx, cy, r, fill=None, stroke=None, lw=0.1):
        self.items.append(("circle", cx, cy, r, fill, stroke, lw))

    def text(self, s, x, y, size, color, bold=False, align="L", mat=None, halo=None):
        if s:
            self.items.append(("text", s, x, y, size, color, bold, align, mat, halo))

def hex_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}

_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"

def pdf_str(s):
    out = bytearray()
    for ch in s:
        if ch in _ENC_EXTRA:
            out.append(_ENC_EXTRA[ch])
            continue
        try:
            b = ch.encode("cp1252")
        except Exception:
            b = b"?"
        if b in (b"\x9e",):
            b = b"?"
        out += b
    s2 = bytes(out).replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
    return b"(" + s2 + b")"

def _f(v):
    s = "{:.3f}".format(v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s

def page_stream(pg):
    o = []
    A = o.append
    A("2.834646 0 0 2.834646 0 0 cm 1 J 1 j")
    cur = {}

    def col(c, stroke):
        k = "S" if stroke else "f"
        if cur.get(k) == c:
            return
        cur[k] = c
        r, g, b = hex_rgb(c)
        A("{} {} {} {}".format(_f(r), _f(g), _f(b), "RG" if stroke else "rg"))

    def path(pts, close):
        A("{} {} m".format(_f(pts[0][0]), _f(pts[0][1])))
        for p in pts[1:]:
            A("{} {} l".format(_f(p[0]), _f(p[1])))
        if close:
            A("h")

    def lw_dash(lw, dash, cap=1):
        A("{} w {} J 1 j [{}] 0 d".format(_f(lw), cap, " ".join(_f(d) for d in (dash or []))))

    for it in pg.items:
        kind = it[0]
        if kind == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            if alpha is not None and alpha < 0.975:                 # see-through: an ExtGState of write_pdf
                A("q /A{:02d} gs".format(max(1, int(round(alpha * 20)))))
                cur.clear()
            if fill:
                col(fill, False)
            if stroke:
                col(stroke, True)
                lw_dash(lw, dash)
            for r in rings:
                path(r, True)
            A("B*" if fill and stroke else ("f*" if fill else "S"))
            if stripes:                       # (colour, spacing mm, width mm[, angle deg, wavy])
                sc_, sp_, w_ = stripes[:3]
                ang = math.radians(stripes[3] if len(stripes) > 3 else 45.0)
                wavy = len(stripes) > 4 and stripes[4]
                A("q")
                for r in rings:
                    path(r, True)
                A("W* n")
                col(sc_, True)
                lw_dash(w_, None, 1)
                dx_, dy_ = math.cos(ang), math.sin(ang)
                nx_, ny_ = -dy_, dx_
                allp = [p for r in rings for p in r]
                ns = [p[0] * nx_ + p[1] * ny_ for p in allp]
                ds = [p[0] * dx_ + p[1] * dy_ for p in allp]
                s_ = min(ns)
                while s_ < max(ns):
                    if wavy:
                        t_, pts_ = min(ds), []
                        while t_ <= max(ds) + 0.5:
                            o_ = s_ + sp_ * 0.22 * math.sin(t_ * 2.0 * math.pi / 3.2)
                            pts_.append((dx_ * t_ + nx_ * o_, dy_ * t_ + ny_ * o_))
                            t_ += 0.5
                        path(pts_, False)
                    else:
                        A("{} {} m {} {} l".format(_f(dx_ * min(ds) + nx_ * s_), _f(dy_ * min(ds) + ny_ * s_),
                                                   _f(dx_ * max(ds) + nx_ * s_), _f(dy_ * max(ds) + ny_ * s_)))
                    s_ += sp_
                A("S Q")
                cur.pop("S", None)
            if alpha is not None and alpha < 0.975:
                A("Q")
                cur.clear()
        elif kind == "line":
            _, pts, stroke, lw, dash, cap = it
            col(stroke, True)
            lw_dash(lw, dash, cap)
            path(pts, False)
            A("S")
        elif kind == "circle":
            _, cx, cy, r, fill, stroke, lw = it
            kk = 0.5523 * r
            if fill:
                col(fill, False)
            if stroke:
                col(stroke, True)
                lw_dash(lw, None)
            A("{} {} m".format(_f(cx + r), _f(cy)))
            for (a1, a2, a3) in (((cx + r, cy + kk), (cx + kk, cy + r), (cx, cy + r)),
                                 ((cx - kk, cy + r), (cx - r, cy + kk), (cx - r, cy)),
                                 ((cx - r, cy - kk), (cx - kk, cy - r), (cx, cy - r)),
                                 ((cx + kk, cy - r), (cx + r, cy - kk), (cx + r, cy))):
                A("{} {} {} {} {} {} c".format(_f(a1[0]), _f(a1[1]), _f(a2[0]), _f(a2[1]), _f(a3[0]), _f(a3[1])))
            A("h " + ("B" if fill and stroke else ("f" if fill else "S")))
        elif kind == "text":
            _, s, x, y, size, color, bold, align, mat, halo = it
            w = text_w(s, size, bold)
            reps = [(halo, True), (color, False)] if halo else [(color, False)]
            for c_, hal in reps:
                if hal:
                    r_, g_, b_ = hex_rgb(c_)
                    A("q {} {} {} RG {} w 1 j 1 Tr".format(_f(r_), _f(g_), _f(b_), _f(size * 0.16)))
                else:
                    col(color, False)
                    A("0 Tr")
                _text_ops(A, s, x, y, size, bold, align, mat, w)
                if hal:
                    A("Q")
    return "\n".join(o).encode("latin-1")

def _text_ops(A, s, x, y, size, bold, align, mat, w):
    if mat is None:
        dx = {"L": 0.0, "C": -w / 2, "R": -w}[align]
        A("BT /F{} {} Tf 1 0 0 1 {} {} Tm".format(2 if bold else 1, _f(size), _f(x + dx), _f(y)))
    else:
        (a, b), (c, d) = mat
        f = {"L": 0.0, "C": -w / 2 / size, "R": -w / size}[align]
        A("BT /F{} 1 Tf {} {} {} {} {} {} Tm".format(2 if bold else 1, _f(a * size), _f(b * size), _f(c * size),
                                                    _f(d * size), _f(x + f * a * size), _f(y + f * b * size)))
    A(pdf_str(s).decode("latin-1") + " Tj ET")

# ---- G2/G3 (MIRAQUA round, 28 Oct 2026): Arial EMBEDDED in every sheet PDF -------------------------------------
# The sheets wrote the PDF standard fonts without embedding (Helvetica, Courier) with the Turkish letters in unused
# WinAnsi slots: the text was right (it copies and searches as İ ğ ş), but viewers without those glyphs drew nothing
# ("stiklal", "De irmen"). Now each font slot is Arial, embedded as a simple TrueType font with the SAME encoding
# (WinAnsi + the six Turkish letters in slots 129/141/143/144/157/158), so the strings, their measuring and the
# booklet's reading of the sheets stay as they were. Arial has Helvetica's widths, so nothing moves; text measured
# as Courier (the old monospace captions) comes out a little shorter. Text stays live for Illustrator.
# The font files are the system's (C:\Windows\Fonts\arial*.ttf, or the user's font folder): read and packed once per
# run. If a file is missing, that slot falls back to the old standard font and PDF_FONT_NOTE says so (for the log).
_PF_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}
_PF_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
_PF_FILES = {"R": ("arial.ttf", "ArialMT", "Helvetica"), "B": ("arialbd.ttf", "Arial-BoldMT", "Helvetica-Bold"),
             "I": ("ariali.ttf", "Arial-ItalicMT", "Helvetica-Oblique"),
             "BI": ("arialbi.ttf", "Arial-BoldItalicMT", "Helvetica-BoldOblique")}
_PF_CACHE = {}
PDF_FONT_NOTE = []


def _pf_path(fn):
    import os as _o
    dirs = [_o.path.join(_o.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
            _o.path.join(_o.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"),
            "/Library/Fonts", "/System/Library/Fonts/Supplemental", "/usr/share/fonts/truetype/msttcorefonts"]
    for d in dirs:
        for nm in (fn, fn.capitalize(), fn.upper()):
            p = _o.path.join(d, nm)
            if _o.path.isfile(p):
                return p
    return None


def _pf_metrics(data):
    """widths of codes 32-255 (1000 units per em) and the descriptor numbers, read from the TrueType tables"""
    import struct as _s
    n = _s.unpack(">H", data[4:6])[0]
    tab = {}
    for i in range(n):
        tag, _c, off, ln = _s.unpack(">4sIII", data[12 + 16 * i:28 + 16 * i])
        tab[tag.decode("latin-1")] = (off, ln)
    h = tab["head"][0]
    upm = _s.unpack(">H", data[h + 18:h + 20])[0]
    bbox = _s.unpack(">hhhh", data[h + 36:h + 44])
    hh = tab["hhea"][0]
    asc, desc = _s.unpack(">hh", data[hh + 4:hh + 8])
    nhm = _s.unpack(">H", data[hh + 34:hh + 36])[0]
    hm = tab["hmtx"][0]
    adv = [_s.unpack(">H", data[hm + 4 * i:hm + 4 * i + 2])[0] for i in range(nhm)]
    cm = tab["cmap"][0]
    sub = None
    for i in range(_s.unpack(">H", data[cm + 2:cm + 4])[0]):
        pid, eid, off = _s.unpack(">HHI", data[cm + 4 + 8 * i:cm + 12 + 8 * i])
        if pid == 3 and eid == 1:
            sub = cm + off
    seg = _s.unpack(">H", data[sub + 6:sub + 8])[0] // 2
    ends = _s.unpack(">%dH" % seg, data[sub + 14:sub + 14 + 2 * seg])
    p = sub + 16 + 2 * seg
    starts = _s.unpack(">%dH" % seg, data[p:p + 2 * seg])
    deltas = _s.unpack(">%dh" % seg, data[p + 2 * seg:p + 4 * seg])
    ro_at = p + 4 * seg
    ros = _s.unpack(">%dH" % seg, data[ro_at:ro_at + 2 * seg])

    def gid(u):
        for k in range(seg):
            if starts[k] <= u <= ends[k]:
                if ros[k] == 0:
                    return (u + deltas[k]) & 0xFFFF
                a = ro_at + 2 * k + ros[k] + 2 * (u - starts[k])
                g = _s.unpack(">H", data[a:a + 2])[0]
                return (g + deltas[k]) & 0xFFFF if g else 0
        return 0
    inv = dict((v, k) for k, v in _PF_EXTRA.items())
    widths = []
    for code in range(32, 256):
        try:
            ch = inv.get(code) or bytes([code]).decode("cp1252")
        except Exception:
            ch = None
        g = gid(ord(ch)) if ch else 0
        widths.append(int(round(adv[min(g, nhm - 1)] * 1000.0 / upm)) if g else 0)
    cap, ital, weight = 0.716 * upm, 0.0, 400
    if "OS/2" in tab:
        o = tab["OS/2"][0]
        weight = _s.unpack(">H", data[o + 4:o + 6])[0]
        if _s.unpack(">H", data[o:o + 2])[0] >= 2:
            cap = _s.unpack(">h", data[o + 88:o + 90])[0]
    if "post" in tab:
        o = tab["post"][0]
        ital = _s.unpack(">i", data[o + 4:o + 8])[0] / 65536.0
    k = 1000.0 / upm
    return dict(widths=widths, bbox=[int(round(v * k)) for v in bbox], asc=int(round(asc * k)),
                desc=int(round(desc * k)), cap=int(round(cap * k)), ital=ital, bold=weight >= 600)


def _pf_style(st):
    """(compressed font file, its length, metrics, PostScript name) of one style, or None: read once per run"""
    if st not in _PF_CACHE:
        fn, ps, _std = _PF_FILES[st]
        p, got = _pf_path(fn), None
        if p:
            try:
                import zlib as _z
                with open(p, "rb") as fh:
                    raw = fh.read()
                got = (_z.compress(raw, 6), len(raw), _pf_metrics(raw), ps)
            except Exception as e:
                PDF_FONT_NOTE.append("font %s not read (%s): standard font used" % (fn, e))
        else:
            PDF_FONT_NOTE.append("font %s not found: standard font %s used (Turkish letters may not show)" % (fn, _std))
        _PF_CACHE[st] = got
    return _PF_CACHE[st]


def pdf_fonts(add, styles, content=None):
    """Font objects for a PDF writer: styles = one of "R", "B", "I", "BI" per font slot /F1, /F2 ... in order (a slot
    may repeat a style: the same objects are used). add(bytes) -> object number, as the writers' own add().
    content: the page content (str or bytes); when given, a slot it never uses gets the light standard-font object
    instead of an embedded file. Returns the object numbers, one per slot."""
    if isinstance(content, bytes):
        content = content.decode("latin-1")
    made, out = {}, []
    for i, st in enumerate(styles):
        used = content is None or ("/F%d " % (i + 1)) in content
        key = st if used else "std-" + st
        if key not in made:
            got = _pf_style(st) if used else None
            if got is None:
                made[key] = add(("<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding << /Type /Encoding "
                                 "/BaseEncoding /WinAnsiEncoding %s >> >>" % (_PF_FILES[st][2], _PF_DIFF)).encode("latin-1"))
            else:
                data, n, m, ps = got
                ff = add(("<< /Length %d /Length1 %d /Filter /FlateDecode >>\nstream\n" % (len(data), n)).encode("latin-1")
                         + data + b"\nendstream")
                flags = 32 + (64 if "I" in st else 0)
                fd = add(("<< /Type /FontDescriptor /FontName /%s /Flags %d /FontBBox [%s] /ItalicAngle %s /Ascent %d "
                          "/Descent %d /CapHeight %d /StemV %d /FontFile2 %d 0 R >>" % (
                              ps, flags, " ".join(str(v) for v in m["bbox"]), ("%.1f" % m["ital"]), m["asc"], m["desc"],
                              m["cap"], 140 if m["bold"] else 80, ff)).encode("latin-1"))
                made[key] = add(("<< /Type /Font /Subtype /TrueType /BaseFont /%s /FirstChar 32 /LastChar 255 "
                                 "/Widths [%s] /FontDescriptor %d 0 R /Encoding << /Type /Encoding /BaseEncoding "
                                 "/WinAnsiEncoding %s >> >>" % (ps, " ".join(str(w) for w in m["widths"]), fd, _PF_DIFF)
                                 ).encode("latin-1"))
        out.append(made[key])
    return out


def write_pdf(pg, path, title):
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    font = pdf_fonts(add, ("R", "B"))                     # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py)
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 20.0)).encode("latin-1")) for i in range(1, 20)]
    gs_res = " ".join("/A{:02d} {} 0 R".format(i + 1, o_) for i, o_ in enumerate(gs))
    pages_id = add(b"")
    data = zlib.compress(page_stream(pg), 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data +
              b"\nendstream")
    kid = add("<< /Type /Page /Parent {} 0 R /MediaBox [0 0 {} {}] /Contents {} 0 R /Resources << /Font "
              "<< /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >> >> >>".format(pages_id, _f(pg.W / PT), _f(pg.H / PT), cid,
                                                                                    font[0], font[1], gs_res).encode("latin-1"))
    objs[pages_id - 1] = "<< /Type /Pages /Kids [{} 0 R] /Count 1 >>".format(kid).encode("latin-1")
    cat = add("<< /Type /Catalog /Pages {} 0 R >>".format(pages_id).encode("latin-1"))
    info = add(b"<< /Title " + pdf_str(title) + b" /Producer " + pdf_str(VERSION) + b" >>")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += "{} 0 obj\n".format(i + 1).encode() + b + b"\nendobj\n"
    x = len(out)
    out += "xref\n0 {}\n0000000000 65535 f \n".format(len(objs) + 1).encode()
    for o_ in offs:
        out += "{:010d} 00000 n \n".format(o_).encode()
    out += "trailer\n<< /Size {} /Root {} 0 R /Info {} 0 R >>\nstartxref\n{}\n%%EOF\n".format(
        len(objs) + 1, cat, info, x).encode()
    with open(path, "wb") as fh:
        fh.write(bytes(out))

def _tree_rand(x, y):
    """A small repeatable random stream from the tree's position (the same in every Python)."""
    s = [(int(round(x * 100.0)) * 73856093 ^ int(round(y * 100.0)) * 19349663) & 0x7FFFFFFF or 1]

    def nxt():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7FFFFFFF
        return s[0] / 2147483648.0
    return nxt

# ---------------------------------------------------------------- composing the board from drawn parts
# Every drawing is drawn on its own Page at its natural size (page mm), then placed on the board at one uniform
# scale that fits its box (place). Text, lines and dashes scale with it, as a reduced print does.
def items_bbox(items):
    xs, ys = [], []
    for it in items:
        k = it[0]
        if k == "poly":
            for r in it[1]:
                xs += [p[0] for p in r]
                ys += [p[1] for p in r]
        elif k == "line":
            xs += [p[0] for p in it[1]]
            ys += [p[1] for p in it[1]]
        elif k == "circle":
            _, cx, cy, r = it[:4]
            xs += [cx - r, cx + r]
            ys += [cy - r, cy + r]
        elif k == "text":
            _, s, x, y, size, color, bold, align, mat, halo = it
            w = text_w(s, size, bold)
            f = {"L": 0.0, "C": -0.5, "R": -1.0}.get(align, 0.0)
            (a, b), (c, d) = mat if mat else ((1.0, 0.0), (0.0, 1.0))
            for u, v in ((f * w, -0.25 * size), ((f + 1) * w, -0.25 * size), (f * w, CAP * size),
                         ((f + 1) * w, CAP * size)):
                xs.append(x + a * u + c * v)
                ys.append(y + b * u + d * v)
    if not xs:
        return (0.0, 0.0, 0.0, 0.0)
    return (min(xs), min(ys), max(xs), max(ys))

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

def place(pg, part, box, max_s=1.0, align="C", log=None, name=""):
    """Puts part (a Page) into box (x0, y0, x1, y1) at the largest scale up to max_s that fits, centred (align C) or
    at the top left (align TL). Returns (scale, placed bbox)."""
    b = items_bbox(part.items)
    bw, bh = max(b[2] - b[0], 1e-6), max(b[3] - b[1], 1e-6)
    s = min(max_s, (box[2] - box[0]) / bw, (box[3] - box[1]) / bh)
    if align == "TL":
        dx, dy = box[0] - s * b[0], box[3] - s * b[3]
    else:
        dx = (box[0] + box[2]) / 2.0 - s * (b[0] + b[2]) / 2.0
        dy = (box[1] + box[3]) / 2.0 - s * (b[1] + b[3]) / 2.0
    pg.items += xform(part.items, s, dx, dy)
    small = min([it[4] for it in part.items if it[0] == "text"] or [9.0]) * s
    if log is not None and small < 1.25:
        log.append(u"NOTE {}: placed at {:.0%} of its drawn size; smallest text {:.1f} mm".format(name, s, small))
    return s, (dx + s * b[0], dy + s * b[1], dx + s * b[2], dy + s * b[3])

# ---------------------------------------------------------------- drawing helpers (page mm, y up)
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

def node(pg, x, y, n, opt, r=3.2):
    """Element number (the old card numbers, 1-11, on every drawing): a roundel in A, a square in B."""
    d = COL["river_dark"] if n != 10 else COL["ink"]
    if opt == "A":
        pg.circle(x, y, r, fill=COL["white"], stroke=d, lw=0.3)
        pg.circle(x, y, r * 0.74, fill=d)
    else:
        s = r * 0.92
        pg.poly([[(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)]], fill=COL["white"], stroke=d,
                lw=0.3)
        s *= 0.74
        pg.poly([[(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)]], fill=d)
    fs = r * (0.82 if n < 10 else 0.66)
    pg.text(str(n), x, y - fs * CAP / 2, fs, COL["white"], bold=True, align="C")
    return (x - r, y - r, x + r, y + r)

def flow_arrow(pg, x0, x1, y, col, lw=0.3, head=1.2):
    """v3: a straight arrow from x0 to x1 at height y (the keyword row's links)."""
    pg.line([(x0, y), (x1 - head * 0.8, y)], col, lw)
    pg.poly([[(x1, y), (x1 - head, y + head * 0.45), (x1 - head, y - head * 0.45)]], fill=col)


def cell(pg, box, title, note_txt, ts, ns):
    """v7: one section's panel: white ground, a coloured rule on top, the title (ts mm) and one short note (ns mm)
    under it, both measured. Returns (drawing box under the note, right end of the note), mm.
    v9 (MIRAQUA 28 Oct, G5): the note's **keywords** bold (ps_rich_para)."""
    x0, y0, x1, y1 = box
    pg.poly([rect(x0, y0, x1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    pg.poly([rect(x0, y1 - 1.2, x1, y1)], fill=MP["discharge"][1])
    pg.text(title, x0 + 5.0, y1 - 1.2 - 3.0 - ts * CAP, ts, COL["ink_dark"], bold=True)
    top = y1 - 1.2 - 3.0 - ts * (CAP + 0.25) - 3.0     # under the title row (the single crops start here)
    w = x1 - x0 - 10.0
    yn, nr = ps_rich_para(pg, x0 + 5.0, top, w, note_txt, ns, COL["ink"])
    return (x0 + 5.0, y0 + 4.0, x1 - 5.0, yn - 0.25 * ns - 4.0), top, nr


# ---------------------------------------------------------------- W3a  concept sections (pr1 v3.1 idea sketches)
# SKETCH_SRC (end of this file) is pr1's sketch code; it runs in its own namespace and draws page items in pr1's
# order. The element numbers come from node() of this board.
_SK = []

def sketch_engine():
    if not _SK:
        ns = {"__name__": "pr1_sketches", "_tree_rand": _tree_rand}   # reeds use the trees' random stream
        exec(compile(SKETCH_SRC, "pr1_sketches", "exec"), ns)
        _SK.append(ns)
    return _SK[0]

def draw_concept(which, opt, log):
    """which: "up", "k4", "k5" or "down" (SKETCH_FN); opt: form A (organic at the water) or B (no curves).
    v7: texts at the engine's TXT_K; labels kept apart by declutter (notes to log)."""
    E = sketch_engine()
    E["FORM"] = opt
    del E["ZP"][:]
    E["ORDER"][0] = 0
    E["GROUP"][0] = 0
    E["NEXT_G"][0] = 0
    k = E["TXT_K"][0]

    def NODE(o, x, y, n):
        tmp = Page(0, 0)
        node(tmp, o[0] + x, o[1] + y, n, opt, 2.6 * k)
        E["NEXT_G"][0] += 1
        E["GROUP"][0] = -E["NEXT_G"][0]                # v7: an element number never moves; labels keep off it
        for it in tmp.items:
            E["_put"](it, E["Z_TEXT"])
        E["GROUP"][0] = 0
    E["NODE"] = NODE
    E["CITE"] = cite                                  # v3: source numbers [n] inside the sketches
    E[SKETCH_FN[which]]()
    ent = [(it, g) for _, _, it, g in sorted(E["ZP"], key=lambda e: (e[0], e[1]))]
    pg = Page(0, 0)
    pg.items = declutter(ent, log, which)
    return pg


DECLUTTER_R = 18                                      # sketch units: how far a label may move to find a free place


def declutter(entries, log, name):
    """v7 (rule: no text over another, measured): entries = [(item, label group)] in drawing order. Label groups
    (> 0: a text, or a pictogram with its words) are set in drawing order; one whose box (text_w widths, a margin of
    0.2 x its size) would touch a label already set or an element number (group < 0) moves to the nearest free place
    (1-unit steps, sideways counted 1.5 x, at most DECLUTTER_R away, inside the drawing's reach); with no free place
    it is left out and logged. Returns the items."""
    groups, order = {}, []
    for i, (it, g) in enumerate(entries):
        if g:
            if g not in groups:
                groups[g] = []
                order.append(g)
            groups[g].append(i)
    items = [it for it, _ in entries]

    def box(ix, pad):
        b = items_bbox([items[i] for i in ix])
        return (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)

    def hit(b, others):
        return any(b[0] < o[2] and o[0] < b[2] and b[1] < o[3] and o[1] < b[3] for o in others)
    art = items_bbox([it for it, g in entries if not g])
    lim = (art[0] - 8.0, art[1] - 8.0, art[2] + 8.0, art[3] + 8.0)
    placed = [box(groups[g], 0.0) for g in order if g < 0]
    R = DECLUTTER_R
    cand = sorted(((dx, dy) for dx in range(-R, R + 1) for dy in range(-R, R + 1) if dx or dy),
                  key=lambda d: (abs(d[0]) * 1.5 + abs(d[1]), abs(d[0])))
    gone = set()
    for g in order:
        if g < 0:
            continue
        ix = groups[g]
        txt = [items[i] for i in ix if items[i][0] == "text"]
        b = box(ix, 0.2 * max([t[4] for t in txt] or [1.0]))
        if not hit(b, placed):
            placed.append(b)
            continue
        for dx, dy in cand:
            nb = (b[0] + dx, b[1] + dy, b[2] + dx, b[3] + dy)
            if lim[0] <= nb[0] and nb[2] <= lim[2] and lim[1] <= nb[1] and nb[3] <= lim[3] and not hit(nb, placed):
                for i in ix:
                    items[i] = xform([items[i]], 1.0, float(dx), float(dy))[0]
                placed.append(nb)
                break
        else:
            gone.update(ix)
            log.append(u"NOTE section {}: label '{}' left out (no free place near it)".format(
                name, txt[0][1] if txt else g))
    return [it for i, it in enumerate(items) if i not in gone]

# ---------------------------------------------------------------- the board (A0 landscape, one page)
def load_palette(dirs, log):
    for d in dirs:
        for p in (os.path.join(d, "bergama_palette.py"), os.path.join(d, "palette", "bergama_palette.py")):
            if not os.path.isfile(p):
                continue
            try:
                m = _types.ModuleType("bergama_palette")
                exec(compile(open(p, encoding="utf-8").read(), p, "exec"), m.__dict__)
                for k in ("paper", "faint", "structure", "ink2", "ink"):
                    COL[k] = m.CORE.get(k, COL[k])
                for k, a in MP.items():
                    e = m.MASTERPLAN.get(k)
                    if e:
                        MP[k] = (e["light"], e["mid"], e["dark"])
                riv = m.MASTERPLAN.get("river")
                if riv:
                    COL["river"], COL["river_mid"], COL["river_dark"] = riv["light"], riv["mid"], riv["dark"]
                for k in ("aras_alan", "begum_alan", "nil_alan"):
                    COL[k] = m.STUDY_AREA.get(k, {}).get("line", COL[k])
                log.append(u"Palette read from " + p)
                return u"palette {} (version {})".format(os.path.basename(p), getattr(m, "VERSION", "?"))   # 25 Oct: no local path on the sheet
            except Exception as ex:
                log.append(u"WARNING: palette file {} not read ({}); embedded v1.4 colours used".format(p, ex))
    return u"embedded palette v1.4 colours"

DATA_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data")   # 25 Oct: every data file here

# ================================================================ embedded engines
# SKETCH_SRC: pr1_drawings v3.1's concept sketches (SKETCH style) with a page-item layer instead of Rhino baking;
# owner names, working-area bars and figures printed elsewhere taken out (24 Oct). Run by sketch_engine().
def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_proposal_sections_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_proposal_sections_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_proposal_sections_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'SKETCH_SRC': 'd8187f7176a997246aa983a6fdc66cdc'}.get(name):
        raise RuntimeError("Data file bergama_proposal_sections_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_proposal_sections_data.py:" + name, "exec"), globals())


bergama_data("SKETCH_SRC")

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

# ---- MIRAQUA round 28 Oct 2026: ONE set of shared definitions for every script (revision_2026-10-28/PLAN.md) ----
# Colours chosen in OKLCH next to palette v1.4 (palette/README.md) and checked by CIEDE2000 (dE00) against each other
# and the base map colours (method and numbers: PLAN.md "Shared definitions"). Same meaning = same colour on every
# page. Hex without '#'.

# G8: the study area (layer calisma_alan, two parts, worked as ONE area) on every map, one line style, one name.
# The rectangle site_alan is the analysis frame (the strip map's own edge); where a figure is counted over it, it is
# named R28_FRAME_NAME.
R28_STUDY_NAME = u"Study area · çalışma alanı"
R28_FRAME_NAME = u"Analysis frame"
R28_STUDY_LINE = dict(colour="262626", width_mm=0.45, dash_mm=(3.0, 0.8, 0.4, 0.8))   # dash-dot, print mm

# G7: one strip per map; standard scales only (SCRIPT_STANDARD §8)
R28_SCALES = (200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000)


def r28_scale(length_m, avail_mm, height_m=0.0, avail_h_mm=1e9):
    """the largest standard scale (smallest denominator) at which length_m x height_m fits avail_mm x avail_h_mm"""
    for d in R28_SCALES:
        if length_m * 1000.0 / d <= avail_mm and height_m * 1000.0 / d <= avail_h_mm:
            return d
    return R28_SCALES[-1]


def r28_axis(frame):
    """frame = the four site_alan corners [A, B, C, D] (A->B the long side, A = upstream end): (A, u, v, L, W):
    unit vector u along the stream (upstream -> downstream), v across it (towards D), the side lengths in m"""
    import math as _m
    (ax, ay), (bx, by), (cx, cy) = frame[0], frame[1], frame[2]
    L = _m.hypot(bx - ax, by - ay)
    W = _m.hypot(cx - bx, cy - by)
    u = ((bx - ax) / L, (by - ay) / L)
    v = (-u[1], u[0])
    if (frame[3][0] - ax) * v[0] + (frame[3][1] - ay) * v[1] < 0:
        v = (-v[0], -v[1])
    return (ax, ay), u, v, L, W


def r28_to_strip(p, axis):
    """survey point -> (s, t) in m: s along the stream from the upstream end, t across it"""
    (ax, ay), u, v = axis[0], axis[1], axis[2]
    dx, dy = p[0] - ax, p[1] - ay
    return dx * u[0] + dy * u[1], dx * v[0] + dy * v[1]


# P06.2 / P22.1 "where we can build": three hatches, apart from the base map and from each other (dE00 >= 19.6 to the
# base colours, >= 24.4 between them)
R28_BUILD_HATCH = (("open", u"Vacant ground", "BD5833", 45.0),         # (key, legend name, line colour, hatch angle);
                   # 28 Oct: "Vacant ground", not "Open ground" (that is the masterplan's open ground, P21.2)
                   ("parking", u"Parking & yards", "6C5594", -45.0),
                   ("loose", u"Loose ground", "BF8F34", 0.0))

# P21.1 open ground: every category apart (dE00 >= 11.4)
R28_OPEN = dict(open_fill="EDDDB1", noplant_hatch="7E522C", stream="91ADB4", building="6B645B", road="CFCCC5",
                bridge="4A3F35")

# P09.1 / P10.1 reach on foot from a hub, three classes (thin streets or light rings, never a glow over the plan)
R28_REACH = ((100, u"0-100 m", "216253"), (400, u"100-400 m", "569484"), (800, u"400-800 m", "A0C8BC"))

# P23.1 / P23.2 masterplan marker groups (number circles and list numbers)
R28_MARKERS = (("roads", u"Roads: kept, calmed, pedestrian, shared", "6E675F"),
               ("hubs", u"Hubs and transit", "A25E2B"),
               ("water", u"Water and ecology", "327382"),
               ("crossings", u"Crossings", "695A85"),
               ("heritage", u"Heritage and views", "8B3A3F"))

# P24 + S1 programme zones (fade-out fields): ONE set for the 1:1,000 plans and the senses page, same colours
R28_ZONES = (("reed", u"Reed basins · cleaning", "58B292"),
             ("terraces", u"Terraces · holding rain", "ADA052"),
             ("hub", u"Hub square", "D4896E"),
             ("subhub", u"Sub-hub in the bed", "6AA4DA"),
             ("demeter", u"Demeter's Garden", "AD8ED1"),
             ("forest", u"Forest corridor", "83AD6D"),
             ("wetland", u"Widened stream · wetland", "41B0BC"),
             ("cafe", u"Café", "D084A1"))
R28_ZONE = dict((k, (lab, hx)) for k, lab, hx in R28_ZONES)

# ---- G4 (MIRAQUA round 28 Oct 2026): labels never overlap each other, symbols or important linework ----------------
# Geometry only (page mm, any y direction): the caller measures its text and draws. Order of tries for each label:
# the spots round its point, then farther out on a thin leader (the leader may not cross a placed label), then the
# same at the smaller sizes in `sizes`; a label still without a spot is dropped if its rank allows it (secondary
# labels), else it gets the nearest free spot anywhere in bounds, on a leader. Boxes are (x0, y0, x1, y1).
def lp_hit(a, b, pad=0.0):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def _lp_seg_box(p, q, b):
    """True when the segment p-q passes through box b (Liang-Barsky)"""
    x0, y0 = p
    dx, dy = q[0] - x0, q[1] - y0
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - b[0]), (dx, b[2] - x0), (-dy, y0 - b[1]), (dy, b[3] - y0)):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def lp_leader_end(b, p):
    """the point of box b nearest p (where a leader from p meets the label)"""
    return (min(max(p[0], b[0]), b[2]), min(max(p[1], b[1]), b[3]))


def label_spot(ax, ay, w, h, taken, bounds=None, segs=(), pad=0.5,
               rings=(0.8, 2.5, 5.0, 8.0, 12.0, 17.0, 24.0), n_ang=16):
    """a free box w x h near (ax, ay): (box, leader) or None. taken: placed boxes and symbol boxes; segs: important
    lines [(p, q)] a label may not sit on. leader = True when the box sits off the point (draw a thin leader)."""
    import math as _m

    def free(b):
        if bounds and not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
            return False
        if any(lp_hit(b, t, pad) for t in taken):
            return False
        return not any(_lp_seg_box(p, q, b) for p, q in segs)

    for i_r, d in enumerate(rings):
        for i in range(n_ang):
            a = 2 * _m.pi * (i + 0.5) / n_ang
            cx, cy = ax + _m.cos(a) * (d + w / 2.0), ay + _m.sin(a) * (d + h / 2.0)
            b = (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)
            if not free(b):
                continue
            far = i_r >= 2
            if far:
                e = lp_leader_end(b, (ax, ay))
                if any(_lp_seg_box((ax, ay), e, t) for t in taken
                       if not (t[0] <= ax <= t[2] and t[1] <= ay <= t[3])):     # the point's own symbol is passed
                    continue
            return b, far
    return None


def place_labels_all(items, taken, bounds=None, segs=(), sizes=(1.0, 0.9), pad=0.5):
    """items: dicts with x, y (anchor), wh (function size_factor -> (w, h)), rank (0 = must show, 1 = may be
    dropped). Places rank 0 first, then rank 1, each nearest its point. Returns {index: (box, leader, size_factor)}
    for the placed ones; dropped rank-1 labels are left out (the caller may list them in a key). taken grows."""
    out = {}
    order = sorted(range(len(items)), key=lambda i: items[i].get("rank", 0))
    for i in order:
        it = items[i]
        got = None
        for f in sizes:
            w, h = it["wh"](f)
            got = label_spot(it["x"], it["y"], w, h, taken, bounds, segs, pad)
            if got:
                got = (got[0], got[1], f)
                break
        if got is None and it.get("rank", 0) == 0 and bounds:
            w, h = it["wh"](sizes[-1])
            cands = []
            gx = bounds[0]
            while gx + w <= bounds[2]:
                gy = bounds[1]
                while gy + h <= bounds[3]:
                    cands.append((gx, gy))
                    gy += 2.0
                gx += 2.0
            cands.sort(key=lambda c: (c[0] + w / 2.0 - it["x"]) ** 2 + (c[1] + h / 2.0 - it["y"]) ** 2)
            for gx, gy in cands:
                b = (gx, gy, gx + w, gy + h)
                if not any(lp_hit(b, t, pad) for t in taken) and not any(_lp_seg_box(p, q, b) for p, q in segs):
                    got = (b, True, sizes[-1])
                    break
        if got:
            taken.append(got[0])
            out[i] = got
    return out

# ================================================================ v9 key map: where the four sections are cut (F4, G8)
# v9 (MIRAQUA 28 Oct, F4; P8 fault table F row 4): the page had no key map, and the K4 and K5 cuts lie downstream of
# the bridges their sketches draw behind them. The key map shows the four surveyed cuts (centres as the masterplan's
# parts/02b_detail.py CUT_AT), the two bridges (site board data/DIAG_SRC.py BRIDGES_K), the Selinos (agriculture
# data/GEO.py "selinos", survey m) and the study area (calisma_alan of Bergama_Altlik.3dm, the recorded copy the site
# board keeps as R28_STUDY_COPY) in R28_STUDY_LINE, named in the booklet legend by R28_STUDY_NAME (G8). A key map, so no
# scale bar (SCRIPT_STANDARD §8); the frame axis horizontal, upstream on the left (G7), a north arrow. It sits in the
# free band under the upstream sketch: inside ps_all, outside the single crops. The note's distances are measured
# here, every press (K4 cut 114.1 m and K5 cut 119.4 m from the bridges, both downstream along the stream line).
PS_KEY_CUTS = [("up", u"1 · UPSTREAM ENTRY", (29693.022, 32569.176)),
               ("k4", u"2 · K4 CUT", (29959.774, 32264.566)),
               ("k5", u"3 · K5 CUT", (30354.663, 31689.671)),
               ("down", u"4 · DOWNSTREAM REACH", (30991.856, 31039.404))]
PS_KEY_BRIDGES = [("k4", u"K4 bridge", (29846.40, 32277.71)),
                  ("k5", u"K5 bridge (Üç Kemer)", (30293.63, 31792.25))]
PS_KEY_STUDY = [
    [(29696.903, 32800.562), (29872.423, 32572.84), (29880.693, 32496.334), (29818.865, 32475.301), (29825.821, 32398.074),
     (29923.185, 32344.348), (29904.985, 32311.252), (29997.056, 32290.092), (30053.417, 32139.667), (30004.049, 32108.006),
     (29954.803, 32210.611), (29792.114, 32247.062), (29761.684, 32302.735), (29754.016, 32451.383), (29678.437, 32447.696),
     (29632.398, 32496.591), (29665.339, 32526.253), (29612.859, 32696.506), (29600.496, 32719.394)],
    [(30178.18, 31923.887), (30138.072, 31887.655), (30257.694, 31773.217), (30389.686, 31405.252), (30701.152, 30991.252),
     (30840.053, 31053.865), (31044.852, 30781.877), (31014.2, 30757.409), (31373.442, 30493.066), (31453.175, 30560.194),
     (31332.978, 30864.179), (31012.679, 31323.349), (30737.856, 31286.66), (30712.87, 31331.891), (30556.09, 31450.103),
     (30454.629, 31577.301), (30434.156, 31607.332), (30313.613, 31812.92)],
]
PS_KEY_SELINOS = [
    (29642.6, 32739.4), (29633.1, 32660.6), (29643.3, 32638.1), (29645.7, 32633.8), (29652.9, 32627.1),
    (29660.7, 32621.7), (29671.3, 32612.4), (29681.0, 32595.6), (29690.4, 32573.6), (29710.7, 32540.0),
    (29713.6, 32536.0), (29733.9, 32514.1), (29754.5, 32493.6), (29765.8, 32484.3), (29769.1, 32480.8),
    (29776.7, 32468.2), (29784.7, 32450.4), (29788.6, 32436.6), (29789.1, 32431.9), (29777.7, 32369.0),
    (29781.7, 32325.3), (29795.2, 32299.4), (29798.1, 32295.6), (29818.1, 32281.3), (29822.6, 32279.6),
    (29865.9, 32271.5), (29920.8, 32274.0), (29974.1, 32261.0), (29985.8, 32252.3), (29991.8, 32239.0),
    (30000.2, 32215.9), (30005.5, 32176.9), (30015.3, 32144.5), (30022.8, 32126.7), (30025.2, 32122.5),
    (30052.7, 32087.9), (30102.5, 32002.2), (30148.1, 31931.0), (30166.5, 31908.3), (30177.3, 31892.6),
    (30200.4, 31867.1), (30235.2, 31839.1), (30275.6, 31802.4), (30315.8, 31746.3), (30345.9, 31706.8),
    (30378.4, 31640.0), (30405.5, 31555.5), (30444.1, 31464.0), (30493.0, 31382.7), (30496.2, 31379.0),
    (30593.4, 31294.4), (30649.6, 31262.4), (30682.7, 31240.2), (30717.2, 31212.8), (30733.6, 31194.9),
    (30753.5, 31180.3), (30757.8, 31177.9), (30833.2, 31152.0), (30931.7, 31093.4), (30935.6, 31090.4),
    (30987.4, 31044.7), (31015.8, 31010.8), (31103.4, 30896.4), (31137.6, 30847.4), (31140.0, 30843.1),
    (31154.8, 30764.8), (31158.1, 30761.4), (31193.6, 30733.8), (31242.2, 30700.3), (31308.9, 30668.1),
    (31393.4, 30634.5)]
PS_KEY_TURN = 49.905                  # degrees: turns the frame axis horizontal, downstream to the right (PLAN §1, G7)
PS_KEY_PANEL = "up"                   # the panel whose free band under its sketch holds the key map
PS_KEY_GAP = 8.0                      # mm (sheet) between a single crop's bottom and the key map
PS_KEY_MIN_H = 60.0                   # mm (sheet): with less room there, the panel with the most room takes it (logged)
PS_KEY_PRINT = dict(cut=(6.0, 0.9), bridge=(3.2, 0.6), river=0.8, leader=0.15, arrow=4.0, pad=2.0)   # booklet print mm


def ps_rich_lines(s, size, width):
    """v9 (MIRAQUA 28 Oct, G5): a text with **bold** runs wrapped to width (mm): lines of [(word, bold, glued)];
    glued = no space before it (punctuation right after a bold run)."""
    toks = []
    for i, part in enumerate(s.split(u"**")):
        for j, wd in enumerate(part.split()):
            toks.append((wd, i % 2 == 1, j == 0 and bool(toks) and not part[:1].isspace()))
    lines, cur, cw = [], [], 0.0
    sp = text_w(u" ", size)
    for wd, b, glued in toks:
        w = text_w(wd, size, b) + (0.0 if glued or not cur else sp)
        if cur and not glued and cw + w > width:
            lines.append(cur)
            cur, cw, w = [], 0.0, text_w(wd, size, b)
        cur.append((wd, b, glued and bool(cur)))
        cw += w
    if cur:
        lines.append(cur)
    return lines


def ps_rich_para(pg, x, y, w, s, size, colour, lh=1.28, halo=None):
    """v9 (G5): para() for a text with **bold** runs, each run one whole string; every line one baseline (size x lh)
    lower than y. Returns (the last baseline, the right end of the longest line), mm."""
    right, sp = x, text_w(u" ", size)
    for ln in ps_rich_lines(s, size, w):
        y -= size * lh
        runs = []
        for i, (wd, b, g) in enumerate(ln):
            if runs and runs[-1][1] == b:
                runs[-1][0] += (u"" if g else u" ") + wd
            else:
                runs.append([wd, b, bool(i) and not g])          # [text, bold, a space before it]
        xx = x
        for t, b, spc in runs:
            xx += sp if spc else 0.0
            pg.text(t, xx, y, size, colour, bold=b, halo=halo)
            xx += text_w(t, size, b)
        right = max(right, xx)
    return y, right


def ps_key_turn(p):
    """survey m -> key map m: turned by PS_KEY_TURN (the frame axis horizontal, downstream to the right)"""
    a = math.radians(PS_KEY_TURN)
    return (p[0] * math.cos(a) - p[1] * math.sin(a), p[0] * math.sin(a) + p[1] * math.cos(a))


def ps_key_chain(p):
    """(chainage along PS_KEY_SELINOS from its upstream end, m; the line's unit direction there) at the point of the
    line nearest p"""
    best, acc = None, 0.0
    for a, b in zip(PS_KEY_SELINOS[:-1], PS_KEY_SELINOS[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1e-9
        t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (L * L)))
        d = math.hypot(a[0] + dx * t - p[0], a[1] + dy * t - p[1])
        if best is None or d < best[0]:
            best = (d, acc + t * L, (dx / L, dy / L))
        acc += L
    return best[1], best[2]


def ps_key_note():
    """The key map's note, measured: how far (m, straight) and which way along the stream each of the K4 and K5 cuts
    lies from the bridge its sketch draws. Returns (text with **bold** runs, {key: m})."""
    at = dict((k, p) for k, _, p in PS_KEY_CUTS)
    bits, dist, ways = [], {}, set()
    for k, nm, b in PS_KEY_BRIDGES:
        c = at[k]
        dist[k] = math.hypot(c[0] - b[0], c[1] - b[1])
        way = u"downstream" if ps_key_chain(c)[0] > ps_key_chain(b)[0] else u"upstream"
        ways.add(way)
        bits.append(u"**%s cut**%s about %.0f m %s of the %s" % (k.upper(), u"" if bits else u" lies", dist[k], way, nm))
    if len(ways) == 1:                                         # today: both downstream (one short line)
        return (u"The **K4 cut** lies about %.0f m and the **K5 cut** about %.0f m %s of the bridges their sketches draw "
                u"behind them" % (dist["k4"], dist["k5"], ways.pop()), dist)
    return u"The " + u", the ".join(bits) + u": the sketches draw these bridges behind the cut", dist


def ps_key_map(pg, boxes, low, log):
    """v9 (F4): the key map in the free band under a sketch (boxes: the panels' drawing boxes; low: each sketch's
    bottom, mm on the sheet), under PS_KEY_PANEL unless it has less than PS_KEY_MIN_H there. Returns its box."""
    room = dict((k, low[k] - 3.0 - PS_KEY_GAP - boxes[k][1]) for k in low)
    key = PS_KEY_PANEL
    if room.get(key, 0.0) < PS_KEY_MIN_H:
        key = max(room, key=lambda k_: room[k_])
        log.append(u"NOTE key map: {:.0f} mm free under the {} sketch, so it sits under the {} sketch ({:.0f} mm)".format(
            room.get(PS_KEY_PANEL, 0.0), PS_KEY_PANEL, key, room[key]))
    bx = boxes[key]
    return draw_key_map(pg, (bx[0], bx[1], bx[2], bx[1] + room[key]), key, log)


def draw_key_map(pg, area, where, log):
    """v9 (F4, G4, G5, G8): the key map hung from the top of area (x0, y0, x1, y1), mm on the sheet: a frame, the
    title row with the north arrow, the map (study area, Selinos, bridges, the four cuts; labels kept apart by
    place_labels_all), the measured note. Print sizes (booklet mm, pt) are turned into sheet mm by 1 / BK_S."""
    x0, y0, x1, y1 = area
    P = dict((k, (tuple(v_ / BK_S for v_ in v) if isinstance(v, tuple) else v / BK_S)) for k, v in PS_KEY_PRINT.items())
    pad, ts, ls = P["pad"], pt_mm(7.5), pt_mm(LBL_PT)
    note, dist = ps_key_note()
    nlines = ps_rich_lines(note, ls, x1 - x0 - 2 * pad)
    note_n = len(nlines)
    title_h, note_h = ts * 1.3, ls * 1.28 * note_n
    polys = [[ps_key_turn(p) for p in R] for R in PS_KEY_STUDY]
    river = [ps_key_turn(p) for p in PS_KEY_SELINOS]
    ext = [p for R in polys for p in R] + river
    ex0, ey0 = min(p[0] for p in ext), min(p[1] for p in ext)
    ex1, ey1 = max(p[0] for p in ext), max(p[1] for p in ext)
    k = min((x1 - x0 - 2 * pad) / (ex1 - ex0), (y1 - y0 - 4 * pad - title_h - note_h) / (ey1 - ey0))
    if k <= 0:
        log.append(u"NOTE key map: no room under the {} sketch, left out".format(where))
        return None
    w, h = (ex1 - ex0) * k, (ey1 - ey0) * k
    ox, oy = x0 + pad, y1 - 2 * pad - title_h - h              # the map's lower left

    def T(q):                                                  # turned m -> sheet mm
        return (ox + (q[0] - ex0) * k, oy + (q[1] - ey0) * k)
    title = u"**KEY MAP** · where the four sections are cut, upstream to downstream"
    tw = text_w(title.replace(u"**", u""), ts, True)
    nw = max(text_w(u" ".join(t for t, _, _ in ln), ls, True) for ln in nlines)
    fx1 = min(x1, x0 + 2 * pad + max(w, tw + 3.0 * P["arrow"], nw))
    yn0 = oy - pad - ls * CAP                                  # the note's first baseline
    fy0 = max(y0, yn0 - (note_n - 1) * ls * 1.28 - 0.25 * ls - pad)
    pg.poly([rect(x0, fy0, fx1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    # title row (G5: the keyword bold) and the north arrow at its right end
    ps_rich_para(pg, x0 + pad, y1 - pad - ts * CAP + ts * 1.28, fx1 - x0, title, ts, COL["ink_dark"])
    nx, ny = ps_key_turn((0.0, 1.0))
    cx, cy = fx1 - pad - P["arrow"], y1 - pad - title_h / 2.0
    tail = (cx - nx * P["arrow"] / 2.0, cy - ny * P["arrow"] / 2.0)
    tip = (cx + nx * P["arrow"] / 2.0, cy + ny * P["arrow"] / 2.0)
    hd = 0.3 * P["arrow"]
    pg.line([tail, tip], COL["ink"], P["leader"] * 2.0)
    pg.poly([[tip, (tip[0] - nx * hd - ny * hd * 0.45, tip[1] - ny * hd + nx * hd * 0.45),
              (tip[0] - nx * hd + ny * hd * 0.45, tip[1] - ny * hd - nx * hd * 0.45)]], fill=COL["ink"])
    pg.text(u"N", tip[0] - 0.6 * ls, tip[1] - ls * CAP / 2.0, ls, COL["ink"], bold=True, align="R")
    # the map: study area (light ground + R28_STUDY_LINE), the Selinos, then the bridges and the cuts across it
    st = R28_STUDY_LINE
    for R in polys:
        pg.poly([[T(q) for q in R]], fill=COL["paper"])
    river_s = [T(q) for q in river]
    pg.line(river_s, COL["river"], P["river"])
    rings = [[T(q) for q in R] + [T(R[0])] for R in polys]
    for r_ in rings:
        pg.line(r_, st["colour"], st["width_mm"] / BK_S, dash=[d / BK_S for d in st["dash_mm"]], cap=0)
    taken, items, anchors = [], [], []

    def bar(p, L, lw, col):                                    # a short bar across the stream at survey point p
        _, (dx, dy) = ps_key_chain(p)
        tx, ty = ps_key_turn((dx, dy))
        c = T(ps_key_turn(p))
        a_, b_ = (c[0] - ty * L / 2.0, c[1] + tx * L / 2.0), (c[0] + ty * L / 2.0, c[1] - tx * L / 2.0)
        pg.line([a_, b_], col, lw, cap=0)
        taken.append((min(a_[0], b_[0]) - lw, min(a_[1], b_[1]) - lw, max(a_[0], b_[0]) + lw, max(a_[1], b_[1]) + lw))
        return c
    for key_, nm, p in PS_KEY_BRIDGES:
        c = bar(p, P["bridge"][0], P["bridge"][1], COL["ink"])
        items.append(dict(x=c[0], y=c[1], rank=0, wh=lambda f, s_=nm: (text_w(s_, ls * f), ls * f * (CAP + 0.25))))
        anchors.append((c, nm, False))
    for key_, nm, p in PS_KEY_CUTS:
        c = bar(p, P["cut"][0], P["cut"][1], COL["accent"])
        items.append(dict(x=c[0], y=c[1], rank=0, wh=lambda f, s_=nm: (text_w(s_, ls * f, True), ls * f * (CAP + 0.25))))
        anchors.append((c, nm, True))
    c = river_s[int(len(river_s) * 0.8)]                       # the stream's name, between cuts 3 and 4 (may drop)
    items.append(dict(x=c[0], y=c[1], rank=1, wh=lambda f: (text_w(u"Selinos", ls * f), ls * f * (CAP + 0.25))))
    anchors.append((c, u"Selinos", None))
    segs = list(zip(river_s[:-1], river_s[1:])) + [s_ for r_ in rings for s_ in zip(r_[:-1], r_[1:])]
    bounds = (x0 + 0.5 * pad, oy - 0.5 * pad, fx1 - 0.5 * pad, oy + h + 0.5 * pad)
    got = place_labels_all(items, taken, bounds, segs, sizes=(1.0,), pad=0.6 / BK_S)
    for i, (c, s_, bold) in enumerate(anchors):
        if i not in got:
            log.append(u"NOTE key map: label '{}' left out (no free place)".format(s_))
            continue
        b, leader, _ = got[i]
        if leader:
            pg.line([c, lp_leader_end(b, c)], COL["ink2"], P["leader"])
        col = COL["river_mid"] if bold is None else (COL["ink_dark"] if bold else COL["ink2"])
        pg.text(s_, b[0], b[1] + 0.25 * ls, ls, col, bold=bool(bold), halo=COL["white"])
    # the measured note (G5: the two cuts bold)
    ps_rich_para(pg, x0 + pad, yn0 + ls * 1.28, fx1 - x0 - 2 * pad, note, ls, COL["ink"])
    log.append(u"key map (F4): under the {} sketch, {:.0f} x {:.0f} mm on the sheet; K4 cut {:.1f} m and K5 cut {:.1f} m "
               u"from the bridges the sketches draw".format(where, fx1 - x0, y1 - fy0, dist["k4"], dist["k5"]))
    return (x0, fy0, fx1, y1)

# ================================================================ A3 booklet = crops of this sheet (v5, booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own sections (SHEET_BOXES, set by build_sheet).
# v7 (Aras 27 Oct 11:07: p.18-19 merged into one page): ps_all = the whole 2 x 2 block (titles, notes, the four
# sections) shaped like the booklet's panel area, for ONE booklet page; the four single crops stay (note + sketch,
# tight; the title is the booklet caption).
BK_SOURCES = [("rhs_lavender", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter)",
               u"https://www.rhs.org.uk/Advice/profile?pid=127"),
              ("ecocrop_olive", u"FAO Ecocrop, Olea europaea (will not tolerate waterlogged soils)",
               u"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1553"),
              # v9 (MIRAQUA 28 Oct, F5): the public pages behind SRC_KEY plane and hamam
              ("icomos_2014", u"ICOMOS 2014, Evaluation No 1457, Pergamon and its Multi-Layered Cultural Landscape",
               u"https://whc.unesco.org/document/152724"),
              ("egetelgraf_2025", u"Köylü H., Ege Telgraf, 31 Dec 2025: Roma'dan Osmanlı'ya uzanan geçmiş: Bergama Çayı "
                                  u"kıyısında unutulan tarihi yapı",
               u"https://www.egetelgraf.com/romadan-osmanliya-uzanan-gecmis-bergama-cayi-kiyisinda-unutulan-tarihi-yapi"),
              ("ktb_tabaklar", u"KTB İzmir İl Kültür ve Turizm Müdürlüğü, Baths (Hamams) in İzmir: Tabaklar Hamam",
               u"https://izmir.ktb.gov.tr/EN-243130/turkiye-baths-hamams-in-izmir.html")]
BK_CROPS = [("ps_all", "all", u"Proposal sections, upstream to downstream · relative levels · 1-11 as in Collect, clean, hold"),
            # v8.1 (Prompt 8): the roundels' key; the sheet header that says "1-11 as on the water board" is outside ps_all
            ("ps_upstream", "up", u"1 · Upstream entry: collect, clean and hold"),
            ("ps_k4", "k4", u"2 · K4 bridge: walking hub"),
            ("ps_k5", "k5", u"3 · K5 bridge: Demeter's Garden and walking hub"),
            ("ps_downstream", "down", u"4 · Downstream reach: give back")]
BK_DROP = [u"^\\[\\d+\\]$"]                           # the sheet's source numbers: the booklet has its own source list


def _bk_hex(c):
    return "%02X%02X%02X" % tuple(int(v) for v in c)


def booklet_export(log):
    """booklet/blocks.json: one crop per section of the sheet + ps_all (rect in mm from the sheet's top-left, y down)."""
    bk = BkBlocks(OUT_DIR, GH_LABEL, VERSION)
    for k, t, u in BK_SOURCES:
        bk.source(k, t, u)
    bk.d["sheet_sources"] = {"0": [u"[{}] {}".format(i + 1, v) for i, (_, v) in enumerate(SRC_KEY)]}   # v7: the booklet's sources page
    E = sketch_engine()                               # the sheet's own colours for the legend samples
    wash = E["mix"]((255, 255, 255), E["FLOOD_WASH"], E["FLOOD_ALPHA"])   # the Q500 wash as it shows on white
    legend = [dict(kind="fill", colour=_bk_hex(E["W_WIN"]), label=u"winter water"),
              dict(kind="fill", colour=_bk_hex(E["W_EXT"]), label=u"summer strip"),
              dict(kind="fill", colour=_bk_hex(wash), label=u"reach of the design flood (Q500)"),
              dict(kind="fill", colour=_bk_hex(E["REED"]), label=u"reeds and planting")]
    # v9 (MIRAQUA 28 Oct, F14): the yellow marker bands (strokes at 0.5 on white), the route as dashed as drawn, the
    # soft paving wash as it shows on white; G8: the key map's study-area outline (in ps_all only)
    sun_ = dict(kind="fill", colour=_bk_hex(E["mix"]((255, 255, 255), E["SUN"], 0.5)),
                label=u"proposal: terraces, steps, squares, garden")
    route = dict(kind="dash", colour=_bk_hex(E["ACCENT"]), label=u"walk from the hub square to the sub-hub")
    deck = dict(kind="fill", colour=_bk_hex(E["mix"]((255, 255, 255), E["SEC_PAVE"], E["PAVE_SOFT"])),
                label=u"boardwalk, sub-hub floor")
    study = dict(kind="dashdot", colour=R28_STUDY_LINE["colour"], label=R28_STUDY_NAME)
    extra = {"all": [sun_, route, deck, study], "up": [sun_], "k4": [sun_, route, deck], "k5": [sun_, route],
             "down": [deck]}
    for bid, key, cap in BK_CROPS:
        if key not in SHEET_BOXES:
            log.append(u"booklet %s: section %s not on the sheet" % (bid, key))
            continue
        x0, y0, x1, y1 = SHEET_BOXES[key]
        bk.crop(bid, OUT_NAME.format("A"), (x0, BOARD_H - y1, x1, BOARD_H - y0), caption=cap, scale_den=None,
                legend=legend + extra.get(key, []), drop=BK_DROP)
    return bk.save()


# ================================================================ the sheet (v7: one 2 x 2 block = one booklet page)
# v7 (Aras 27 Oct 11:07 "p18-19: merge into one page"; spec §5 q3): the four sections sit in one 2 x 2 block whose
# shape is the booklet's panel area, so the booklet shows the whole block (crop ps_all) on ONE A3 page at one factor;
# every section is placed at ONE common factor (the sketches carry relative levels, so the booklet prints no scale).
# Titles short, one short note under each title, no source footer (the [n] key goes to the log).
# v9 (MIRAQUA 28 Oct): G5 keywords in **bold**; K4 (bank-depth research §4.6, Aras 14:12): the walls stand about 5 m
# above the bed, so Q500 stays under the street (was "Q500 tops today's bank", the survey before the DSİ walls)
PROPOSALS = [("up", u"1 · UPSTREAM ENTRY",
              u"Winter runoff: cleaned in **reed basins**, held in the terrace basins, given back in **summer** as the strip"),
             ("k4", u"2 · K4 BRIDGE · WALKING HUB",
              u"Q500 stays **under the street**: dry **hub square** above it, floodable sub-hub in the bed, steps between"),
             ("k5", u"3 · K5 BRIDGE · DEMETER'S GARDEN + WALKING HUB",
              u"Bank tops stay **dry**: garden and hub square · bed: **stream commons** = sub-hub, floods in winter"),
             ("down", u"4 · DOWNSTREAM REACH",
              u"Clean water arrives from upstream: **floodable planting** + boardwalk, surplus to farmland")]
SHEET_BOXES = {}                                      # key -> crop box (x0, y0, x1, y1), mm, y up; set by build_sheet
SKETCH_FN = {"up": "concept_aras_sketch", "k4": "concept_begum_sketch", "k5": "concept_k5_sketch",
             "down": "concept_nil_sketch"}
# The booklet's panel area (bergama_booklet code.py: AREA = 392 x 243 mm, less the 5 mm caption band CAP_H)
BK_W, BK_H = 392.0, 238.0
GRID_W = BOARD_W - 2 * M                              # the 2 x 2 block on the A0 sheet, mm
GRID_H = GRID_W * BK_H / BK_W                         # same shape as the booklet area: it fills the page, never stretched
BK_S = BK_W / GRID_W                                  # booklet print factor of ps_all (0.338)
LBL_PT, TITLE_PT, NOTE_PT = 7.0, 9.0, 9.0             # smallest word / titles / notes as printed on that booklet page


def pt_mm(pt):
    """The sheet text size (mm) that prints at pt points on the one-page booklet panel ps_all."""
    return pt * PT / BK_S


def fit_s(part, box):
    b = items_bbox(part.items)
    return min((box[2] - box[0]) / max(b[2] - b[0], 1e-6), (box[3] - box[1]) / max(b[3] - b[1], 1e-6))


def sections(opt, boxes, log):
    """v7: the four sketches at ONE common factor s (the largest at which each fits its box). Their words are drawn
    at TXT_K x their size, raised (up to 4 tries) until the smallest prints >= LBL_PT on the booklet page.
    Returns ({key: Page}, s)."""
    E = sketch_engine()
    E["TXT_K"][0] = 1.0
    for _ in range(4):
        notes = []
        parts = dict((k, draw_concept(k, opt, notes)) for k in SKETCH_FN)
        s = min(fit_s(parts[k], boxes[k]) for k in parts)
        small = min(it[4] for p in parts.values() for it in p.items
                    if it[0] == "text" and it[5] != COL["white"])        # white = digits inside the element numbers
        pt = small * s * BK_S / PT
        if pt >= LBL_PT - 0.05:
            break
        E["TXT_K"][0] *= LBL_PT / pt * 1.02
    log.extend(notes)
    log.append(u"sections: one factor {:.2f} mm per sketch unit; words x{:.2f}; smallest word on the booklet page "
               u"{:.1f} pt".format(s, E["TXT_K"][0], pt))
    return parts, s


def build_sheet(opt, log):
    """The four proposals in section on one A0 landscape sheet, upstream to downstream (2 x 2)."""
    pg = Page(BOARD_W, BOARD_H)
    pg.poly([rect(0, 0, BOARD_W, BOARD_H)], fill=COL["sheet"])
    X0, X1, G = M, BOARD_W - M, 8.0
    top = BOARD_H - M
    pg.text(u"The Proposals in Section", X0, top - 12.0, 12.0, COL["ink_dark"], bold=True)
    # v3: the subtitle sentence as a keyword row: problem -> one move | 1 -> 11 upstream to downstream | the tag
    fs, yc, dk = 2.9, top - 16.96, MP["discharge"][2]
    yb = yc - fs * CAP / 2
    x = X0
    for i_, wd in enumerate((u"PROBLEM", u"ONE MOVE")):
        pg.text(wd, x, yb, fs, dk, bold=True)
        x += text_w(wd, fs, True) + 1.5
        if i_ == 0:
            flow_arrow(pg, x, x + 6.0, yc, dk, 0.35, 1.4)
            x += 7.5
    x += 8.0
    pg.text(u"upstream", x, yb, fs, dk, bold=True)
    x += text_w(u"upstream", fs, True) + 2.5
    flow_arrow(pg, x - 1.0, x + 11 * 4.6 + 4.0, yc, dk, 0.35, 1.4)   # under the roundels: one way, with the stream
    for n_ in range(1, 12):
        node(pg, x + 1.6, yc, n_, opt, 1.6)
        x += 4.6
    x += 5.5
    for wd in (u"downstream · one way, with the stream", u"1-11 as on the water board"):
        pg.text(wd, x, yb, fs, dk, bold=True)
        x += text_w(wd, fs, True) + 8.0
    tag = u"relative levels"                          # v5: no caveat words
    pg.poly([rect(x, yc - 2.2, x + text_w(tag, 2.4) + 3.0, yc + 2.2)], fill=COL["lane"], stroke=COL["structure"],
            lw=0.25)
    pg.text(tag, x + 1.5, yc - 2.4 * CAP / 2, 2.4, COL["ink"])
    y1 = top - 22.0
    pg.line([(X0, y1), (X1, y1)], COL["structure"], 0.3)
    gy1 = y1 - 4.0
    gy0 = gy1 - GRID_H
    cw, ch = (GRID_W - G) / 2.0, (GRID_H - G) / 2.0
    boxes, heads = {}, {}
    for i, (key, ttl, txt) in enumerate(PROPOSALS):
        cx = X0 + (i % 2) * (cw + G)
        cy = gy1 - (i // 2 + 1) * ch - (i // 2) * G
        boxes[key], tp, nr = cell(pg, (cx, cy, cx + cw, cy + ch), ttl, txt, pt_mm(TITLE_PT), pt_mm(NOTE_PT))
        heads[key] = (tp, nr)
    parts, s = sections(opt, boxes, log)
    low = {}                                          # v9: each sketch's bottom on the sheet (the key map goes under one)
    for key, _, _ in PROPOSALS:
        bx = boxes[key]
        b = items_bbox(parts[key].items)
        dx = (bx[0] + bx[2]) / 2.0 - s * (b[0] + b[2]) / 2.0     # centred across, at the top of its box
        dy = bx[3] - s * b[3]
        pg.items += xform(parts[key].items, s, dx, dy)
        tp, nr = heads[key]                           # single crop: note + sketch, tight (the title is the caption)
        SHEET_BOXES[key] = (min(bx[0], dx + s * b[0]) - 2.0, dy + s * b[1] - 3.0,
                            max(nr, dx + s * b[2]) + 2.0, tp)
        low[key] = dy + s * b[1]
    ps_key_map(pg, boxes, low, log)                   # v9 (MIRAQUA 28 Oct, F4): inside ps_all, outside the single crops
    SHEET_BOXES["all"] = (X0, gy0, X0 + GRID_W, gy1)  # v7: the one-page block (titles + notes + sketches)
    log.append(u"sources by number (the sheet's [n]): " +
               u"  ".join(u"[{}] {}".format(i + 1, v) for i, (_, v) in enumerate(SRC_KEY)))
    return pg



def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    log = []
    pal = load_palette([DATA_DIR], log)
    lines = []
    for opt in OPTIONS:
        t1 = time.time()
        pg = build_sheet(opt, log)
        path = os.path.join(OUT_DIR, OUT_NAME.format(opt))
        try:
            write_pdf(pg, path, u"Bergama proposal sections {} {}".format(VERSION, opt))
        except (IOError, OSError):
            path = path.replace(".pdf", datetime.datetime.now().strftime("_%H%M%S.pdf"))
            write_pdf(pg, path, u"Bergama proposal sections {} {}".format(VERSION, opt))
        lines.append(u"{}  {}  {:.1f} s".format(os.path.basename(path), time.strftime("%H:%M:%S"), time.time() - t1))
    try:                                              # v4: A3 booklet assets; an error here never stops the sheet
        booklet_export(log)
    except Exception as ex:
        log.append(u"booklet assets not written: {}: {}".format(type(ex).__name__, ex))
    log += bg_tidy_output(OUT_FOLDER)              # 27 Oct: output/ = PDFs only
    head = [u"Output: {}".format(OUT_DIR)] + lines + [x for x in log if x]
    if pal is None:
        head.append(u"palette: built-in colours (no bergama_palette.py in Downloads/Bergama/Data)")
    return u"\n".join(head + [u"{} {}, {:.1f} s".format(GH_LABEL, VERSION, time.time() - t0)])


def chain_fire(v, key):
    """25 Oct 10:20 (one-click chain): a NEW "done ..." text from the previous script fires this script once."""
    if isinstance(v, (list, tuple)):                 # several wires (e.g. a Button and a done): take the done text
        v = next((x for x in v if str(x).startswith("done ")), None)
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


# ---- Grasshopper wiring (template; never define a function named run: it would hide the input) ----
if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed = any(v is True for k, v in list(globals().items())
                   if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "rhino_bake", "done")) or \
        any(chain_fire(v, _k + "_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _sc.sticky.get(_k + "_ver") != VERSION:     # v8: a newly pasted version shows itself at once, idle
        for _s in ("_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    if _pressed:
        _t0 = time.time()
        _sc.sticky[_k + "_ver"] = VERSION
        try:
            _res = main()
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to write the proposal sections to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
else:
    print(write_log(main()))
