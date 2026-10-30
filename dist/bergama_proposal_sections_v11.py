# -*- coding: utf-8 -*-
"""BERGAMA PROPOSAL SECTIONS v4 (2026-10-25): Group 6's four proposals in section, upstream to downstream, in the
water board's hand-drawn section style (Aras 25 Oct 11:38-11:45: "we want section from each proposal just like our
water board sections"; "the style of waterboard sections were really really good you can do it somewhere else").
For the studio session of 26.10.2026: "Sections: Illustrating the spatial relationships and key design decisions."

NEW IN v11: assets_2 high-res silhouettes (Aras 30 Oct 06:11, a feature change): the detailed sections draw the
  PhyloPic trees (plane, ash, olive, stone pine) and crops (maize, tomato) of common/hires.py in each section's own
  colours, roots cut at the ground, uniform scale (needs Data/assets_hires.json; without it the old primitives). Page
  13 (W1-W4).
NEW IN v10 (revision 29 Oct, WO-T3b-3, booklet page 13; package C "Page 13", brief 02 §3-§6; a feature change):
  * The four sections are redrawn true to their cuts W1-W4 at 1:500 on the booklet page (parts/70_sections.py): bed,
    bed width, DSİ walls (5.00 m), embankments at their surveyed angle, the loose earth bank, the SW shelf, Q100 and
    Q500 all from the level module (common/levels.py), banks, hatches and steps from section_parts, every species at
    its true size from plants (D6: chaste tree + plane in the café beds, no fig or citrus; D2: common reed only in
    lined basins above Q500), figures placed by what they do (_p13_fig, the one swap point). Scale bar beside each.
  * The key map is a strip across the top of the page, outside every section's panel, showing only W1-W4 on the
    topographic basemap, each cut named with its section's badge and name. The sketch engine is no longer included.
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

WHAT IT DRAWS (v10): one A0 landscape sheet, all vector, whole-string text; the block on it is booklet page 13:
  KEY MAP strip   the four cuts W1-W4 only, on the topographic basemap
  1 W1 UPSTREAM ENTRY       DSİ walls; three lined reed basins behind the SW wall clean street runoff, summer release
  2 W2 K4 WALKING HUB       SW wall replaced by a sub-hub floor and seating steps; hub square with planes on top
  3 W3 K5 DEMETER'S GARDEN  steps seated into the NE loose earth bank; stream commons on the SW shelf; garden raised
                            above Q500 (olive, lavender, tomato, café beds with chaste tree and plane)
  4 W4 DOWNSTREAM REACH     planting bands by flood level on the 8.9° NE embankment, floodable boardwalk, field SW
  Every section looks downstream (NE left), 1:500 on the booklet page. Not drawn (not in any source): the garden's
  intake and lift, basin volumes.

COMPONENT: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file. Input run (Button), outputs log and done.
Writes Downloads/Bergama/output/bergama_proposal_sections/Bergama_proposal_sections_A.pdf; log in
Downloads/Bergama/logs/bergama_proposal_sections_log.txt. Reads Downloads/Bergama/cached/basemap/basemap.json (the site
board writes it; without it the key map draws the stream line only) and its Data file (level table); palette from
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
VERSION = "v11"
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
# v10: no [n] marks on the drawings any more (cite() removed); the key goes to the booklet's sources page and the log.
# Rain, hamam and gauges went with the sketches; the bed width's public source comes from the level module.
SRC_KEY = [
    ("levels", u"Q100, Q500: DSİ design flows, Q500 263.3 m³/s (Danıştay 6. D. 2021/9521 E.)"),
    ("plane", u"Ottoman squares with plane trees: ICOMOS 2014, Evaluation No 1457, Pergamon and its Multi-Layered "
              u"Cultural Landscape, p. 281"),
    ("plants", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter); FAO Ecocrop, olive (will not "
               u"tolerate waterlogged soils)"),          # v8.1: the public pages of BK_SOURCES, not the internal register
]


def ps_sources():
    """SRC_KEY plus the public sources the level module gives for the four cuts (today: the DSİ bed width, SYGM)"""
    out, seen = list(SRC_KEY), set()
    for _, cid, _, _, _ in PS_CUTS:
        s = level_public_source(cid, "bed_width_cm")
        if s and s not in seen:
            seen.add(s)
            out.append(("bed_" + cid, u"DSİ bed width: " + s))
    return out

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

# ---------------------------------------------------------------- composing the board from drawn parts
# v10: the page block is drawn in booklet print mm and placed on the board at 1 / BK_S (xform). Text, lines and
# dashes scale with it, as a reduced print does.
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

# ---------------------------------------------------------------- drawing helpers (page mm, y up)
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

# ---------------------------------------------------------------- shared modules (revision 29 Oct, T2a / T2b)
# v10: the level table (data first), the section parts before the plants, the legacy figures (through _p13_fig
# only), the basemap for the key map. Names checked: no module name is defined by this script.
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
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'LEVELS': 'a217c1d07ff06bcb3cd55255c619aa7c'}.get(name):
        raise RuntimeError("Data file bergama_proposal_sections_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_proposal_sections_data.py:" + name, "exec"), globals())


bergama_data("LEVELS")

# ---- Level table reader (H-levels 29 Oct 2026; WO-T2a-2) ------------------------------------------------------------
# Reads LEVELS (../common/data/LEVELS.py: one row per cut crossing, every number a {value, status, source[, public]}
# dict; the row schema and how to add a row are at the top of that file). Include the data first:
#   #@include ../common/data/LEVELS.py
#   #@include ../common/levels.py
# Values come back as floats rounded to 2 decimals (levels and heights m, widths cm), None where a field is absent or
# has no value (a bank with no crest). No drawing and no label text here: nothing about a status is ever printed on a
# page (Aras); level_public_source() gives the one source text a page may print, and only for a published source.
# A cut id with one crossing names its row ("S4", "W1"); S5 and S6 have rows "S5-1".."S5-3", "S6-1".."S6-3", and
# their bare id ("S5") is accepted only where the answer is the same on every crossing (ends, end labels).

def _lv_rows():
    """the LEVELS rows, or a clear stop when the data part was not included"""
    rows = globals().get("LEVELS")
    if rows is None:
        raise RuntimeError("LEVELS data missing: include ../common/data/LEVELS.py before ../common/levels.py")
    return rows


def level_ids():
    """the row ids in table order"""
    return [r["id"] for r in _lv_rows()]


def _lv_cut_rows(cid):
    """the rows of a bare cut id ("S5" -> its crossing rows), [] when there are none"""
    return [r for r in _lv_rows() if r.get("cut") == cid]


def level_cut(cid):
    """the row dict of cut (crossing) cid; KeyError naming the known ids"""
    for r in _lv_rows():
        if r["id"] == cid:
            return r
    many = _lv_cut_rows(cid)
    if len(many) == 1:
        return many[0]
    if many:
        raise KeyError("level cut %s crosses the stream %d times: use one of %s"
                       % (cid, len(many), ", ".join(r["id"] for r in many)))
    raise KeyError("no level cut %r; known: %s" % (cid, ", ".join(level_ids())))


def _lv_value(cid, key, side=None):
    """the {value, status, source} dict of a field (side "NE"/"SW" for a bank field), None if absent"""
    r = level_cut(cid)
    if side is not None:
        if side not in ("NE", "SW"):
            raise KeyError("level side must be 'NE' or 'SW', not %r" % (side,))
        r = r.get(side) or {}
    v = r.get(key)
    return v if isinstance(v, dict) and "value" in v else None


def _lv_r2(x):
    return None if x is None else round(float(x), 2)


def level(cid, key, side=None):
    """the value of a field as a float (level("S4", "bed"), level("W1", "top", "NE"), level("S4", "q500")); None if
    the field is absent or has no value"""
    v = _lv_value(cid, key, side)
    return None if v is None else _lv_r2(v["value"])


def level_status(cid, key, side=None):
    """"s" surveyed / "i" interpolated / "a" assumed / "c" calculated; internal tracking only, never printed"""
    v = _lv_value(cid, key, side)
    return None if v is None else v.get("status")


def level_public_source(cid, key, side=None):
    """the source to print, only when it is publicly available (e.g. the SYGM 2019 report); else None. Internal
    sources (the survey, scripts, decisions, "calculated", "assumed", ...) are never returned (Aras 29 Oct)"""
    v = _lv_value(cid, key, side)
    return None if v is None else (v.get("public") or None)


def _lv_ends_row(cid):
    """the row holding the cut line: a bare S5/S6 id takes its first crossing (all crossings share the line)"""
    try:
        return level_cut(cid)
    except KeyError:
        many = _lv_cut_rows(cid)
        if not many:
            raise
        return many[0]


def level_ends(cid):
    """((x1, y1), (x2, y2)): the cut's two ends in survey m, unprimed end first"""
    (a, b) = _lv_ends_row(cid)["ends"]["value"]
    return (float(a[0]), float(a[1])), (float(b[0]), float(b[1]))


def level_end_labels(cid):
    """(label1, label2) of the ends, e.g. ("S1", "S1'"); ("SW", "NE") on the W cuts"""
    a, b = _lv_ends_row(cid)["ends"]["labels"]
    return a, b


def level_depth(cid, side):
    """bank (or wall) top minus bed on side "NE"/"SW" (m, 2 decimals); None where the bank has no crest"""
    top, bed = level(cid, "top", side), level(cid, "bed")
    return None if top is None or bed is None else round(top - bed, 2)


def level_flood_depth(cid, which):
    """flood level minus bed (m, 2 decimals); which = "q100" or "q500" (100 / 500 and "Q100" also accepted)"""
    k = str(which).lower()
    k = k if k.startswith("q") else "q" + k
    if k not in ("q100", "q500"):
        raise KeyError("level flood must be q100 or q500, not %r" % (which,))
    q, bed = level(cid, k), level(cid, "bed")
    return None if q is None or bed is None else round(q - bed, 2)

# ---- section language of the main site board (selinus_board draw_section_strip), shared by the water board and the
# agriculture alternatives (Aras 25 Oct 21:52: their sections drawn "such as we draw in the site sections"): the cut
# ground a shade darker than the page with a fine ink line, water hatched in blue from the bed to its surface, the
# channel above it in a pale wash, whole trees and plants at their stated size. One scale for x and y (Aras 22:02:
# "not stretch anything ever"). Pure geometry: each helper returns shapes, the script's sec_put() draws them.
#   ("poly", ring, fill, stroke, lw)    ("line", pts, colour, lw)          page mm, y up


def _sec_mix(a, b, t):
    """hex a -> hex b by t (the board's mix(), on hex strings)."""
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


# palette roles of the board's sections (selinus_board parts 01 and 14: slide khaki, paper, ink, the Selinus' blue)
SEC = dict(paper="F1EDDF", ink="4A3F35", ink2="7A6E60", khaki="BCB794", water="7FA4B3", hatch="3E7DAE",
           tree="7E8A57", pine="5F6B43", olive="8E9A6C", trunk="7A6E60", reed="8E9466", reed_head="B49A6C",
           lav="9F86C0", grass="8F9A68")
SEC["soil"] = _sec_mix(SEC["khaki"], SEC["paper"], 0.42)          # SEC_SOIL: the cut ground
SEC["channel"] = _sec_mix(SEC["water"], SEC["paper"], 0.5)        # SEC_CHANNEL: the water body
SEC["wash"] = _sec_mix(SEC["water"], SEC["paper"], 0.72)          # the channel above the water
SEC["crown"] = _sec_mix(SEC["tree"], SEC["paper"], 0.15)          # SEC_CROWN
SEC["crown_lt"] = _sec_mix(SEC["tree"], SEC["paper"], 0.45)
SEC["shrub"] = _sec_mix(SEC["olive"], SEC["paper"], 0.25)
SEC["beyond"] = _sec_mix(SEC["tree"], SEC["paper"], 0.62)         # things beyond the cut: paler


def sec_hatch(ring, spacing, ang_deg=45.0):
    """The hatch lines of a closed ring (page mm) at ang_deg, spacing apart: [(p, q), ...] (even-odd scan)."""
    import math as _m
    a = _m.radians(ang_deg)
    ca, sa = _m.cos(a), _m.sin(a)
    R = [(ca * x + sa * y, -sa * x + ca * y) for x, y in ring]       # hatch direction along u
    vs = [p[1] for p in R]
    out = []
    k = _m.ceil(min(vs) / spacing)
    while k * spacing < max(vs):
        v = k * spacing
        us = []
        for i in range(len(R)):
            (u0, v0), (u1, v1) = R[i], R[(i + 1) % len(R)]
            if (v0 <= v < v1) or (v1 <= v < v0):
                us.append(u0 + (u1 - u0) * (v - v0) / (v1 - v0))
        us.sort()
        for j in range(0, len(us) - 1, 2):
            p = (ca * us[j] - sa * v, sa * us[j] + ca * v)
            q = (ca * us[j + 1] - sa * v, sa * us[j + 1] + ca * v)
            out.append((p, q))
        k += 1
    return out


def sec_ellipse(cx, cy, rx, ry, n=28):
    import math as _m
    return [(cx + rx * _m.cos(2 * _m.pi * i / n), cy + ry * _m.sin(2 * _m.pi * i / n)) for i in range(n)]


def sec_water(ring, spacing=0.6, lw=0.1):
    """A water body (ring, page mm): channel blue, 45-degree blue hatch, the water line on top (as draw_stream)."""
    sh = [("poly", ring, SEC["channel"], None, 0.1)]
    sh += [("line", [p, q], SEC["hatch"], lw) for p, q in sec_hatch(ring, spacing)]
    top = max(p[1] for p in ring)
    xs = [p[0] for p in ring if abs(p[1] - top) < 1e-6]
    if len(xs) >= 2:
        sh.append(("line", [(min(xs), top), (max(xs), top)], SEC["hatch"], 0.3))
    return sh


def sec_tree(x, gy, h, r, k, tone="crown", lo=None):
    """A whole tree in section at its stated size: h tall, crown r wide each side (m), k page mm per m, ground at
    (x, gy). Trunk to the crown base (35 % of the top, at least 1.5 m: the board's crown_lo), crown as overlapping
    lobes in two tones, a few branches."""
    import math as _m
    lo = max(1.5, 0.35 * h) if lo is None else lo
    lo = min(lo, h * 0.6)
    tw = max(0.12, 0.05 * r * k)
    cy = gy + (lo + (h - lo) / 2.0) * k
    rx, ry = r * k, max(0.5 * r, (h - lo) / 2.0) * k            # a crown never flatter than half its radius (board)
    sh = [("poly", [(x - tw, gy), (x + tw, gy), (x + tw * 0.6, gy + lo * k + ry * 0.4),
                    (x - tw * 0.6, gy + lo * k + ry * 0.4)], SEC["trunk"], None, 0.1)]
    col = SEC.get(tone, SEC["crown"])
    lobes = [(0.0, 0.0, 1.0, 1.0), (-0.42, -0.18, 0.62, 0.7), (0.44, -0.12, 0.6, 0.72), (-0.2, 0.36, 0.6, 0.6),
             (0.26, 0.3, 0.58, 0.62)]
    for i, (dx, dy, fx, fy) in enumerate(lobes):
        sh.append(("poly", sec_ellipse(x + dx * rx, cy + dy * ry, fx * rx, fy * ry, 24),
                   col if i == 0 else (SEC["crown_lt"] if i % 2 else col), SEC["ink2"] if i == 0 else None, 0.08))
    for s_, ang in ((-1, 50.0), (1, 40.0), (-1, 70.0)):
        a = _m.radians(ang)
        b0 = (x, gy + lo * k)
        sh.append(("line", [b0, (x + s_ * _m.cos(a) * rx * 0.55, gy + lo * k + _m.sin(a) * ry * 0.9)], SEC["trunk"],
                   max(0.08, tw * 0.6)))
    return sh


def sec_shrub(x, gy, h, w, k, col=None):
    """A shrub h tall, w wide (m): a dome on the ground with a lighter top lobe."""
    rx, ry = w / 2.0 * k, h / 2.0 * k
    return [("poly", sec_ellipse(x, gy + ry, rx, ry, 24), col or SEC["shrub"], SEC["ink2"], 0.06),
            ("poly", sec_ellipse(x - rx * 0.25, gy + ry * 1.2, rx * 0.45, ry * 0.4, 16), SEC["crown_lt"], None, 0.1)]


def sec_reeds(x0, x1, gy, h, k, step=0.35):
    """Reeds h tall (m) from x0 to x1 (page mm); gy(x) = ground y. Stems with seed heads."""
    sh, i = [], 0
    x = x0
    while x <= x1:
        hh = h * (0.78 + 0.22 * ((i * 7) % 5) / 4.0) * k
        g = gy(x)
        lean = 0.12 * hh * (1 if i % 2 else -1) * 0.3
        sh.append(("line", [(x, g), (x + lean, g + hh)], SEC["reed"], 0.12))
        if i % 3 == 0:
            sh.append(("poly", sec_ellipse(x + lean, g + hh, 0.18 * k * 0.6 + 0.12, 0.45 * k * 0.6 + 0.25, 10),
                       SEC["reed_head"], None, 0.1))
        x += step * k
        i += 1
    return sh


def sec_tufts(x0, x1, gy, h, k, step=0.25, col=None):
    """Grass and meadow tufts h tall (m) from x0 to x1 (page mm)."""
    sh, i = [], 0
    x = x0
    while x <= x1:
        g = gy(x)
        hh = h * k * (0.7 + 0.3 * ((i * 3) % 4) / 3.0)
        for d in (-0.35, 0.0, 0.35):
            sh.append(("line", [(x, g), (x + d * hh * 0.6, g + hh * (1.0 - abs(d) * 0.4))], col or SEC["grass"], 0.1))
        x += step * k
        i += 1
    return sh


def sec_lavender(x0, x1, gy, k, h=0.5):
    """Lavender mounds about h tall (m) with flower spikes."""
    sh = []
    w = 0.8 * k
    x = x0 + w / 2.0
    while x <= x1 - w / 2.0 + 1e-6:
        g = gy(x)
        sh += sec_shrub(x, g, h, 0.8, k, col=_sec_mix(SEC["olive"], SEC["paper"], 0.1))
        for d in (-0.25, 0.0, 0.25):
            sh.append(("line", [(x + d * w, g + h * k * 0.8), (x + d * w * 1.3, g + h * k * 1.3)], SEC["lav"], 0.25))
        x += w
    return sh


# ---- section parts (WO-T2b-3, 29 Oct 2026; section_style.py now includes this file): the river bank as it is at the
# cut (brief 02 §4): DSİ stone walls at 5.00 m, embankments at their surveyed angle, loose earth banks, railings and
# parapets; stone, concrete, earth and the gravel bed in their own hatch; terraces and steps cut into the bank.
# Real sizes in m placed by k (page mm per m); a bank's surface runs from its toe at the bed landward.

SCT_DSI_WALL_H_M = 5.00   # revision_2026-10-29/T1/levels/RESULT.md line 18: "DSİ stone walls at bed + 5.00 m" (Aras 28 Oct)

# material fills (palette v1.4, palette/bergama_palette.py; lines in the section_style inks)
SCT = dict(stone=_sec_mix("B0AC9C", "EFEDE6", 0.35),   # CORE structure toward CORE paper
           concrete="D8D5CC",                         # CORE faint
           earth=SEC["soil"],                         # section_style cut ground
           gravel="CFCCC5",                           # CORE street
           line=SEC["ink2"],                          # VARIANTS 0.0 ink2: hatch lines
           cut=SEC["ink"])                            # CORE ink: the cut line


def _sct_rnd(i, j):
    """A fixed pseudo-random number in [0, 1) for grid cell (i, j)."""
    import math as _m
    v = _m.sin(i * 12.9898 + j * 78.233) * 43758.5453
    return v - _m.floor(v)


def _sct_inside(ring, p):
    """Even-odd test: is page point p inside the ring."""
    x, y = p
    c = False
    n = len(ring)
    for i in range(n):
        (x0, y0), (x1, y1) = ring[i], ring[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (x1 - x0) * (y - y0) / (y1 - y0):
            c = not c
    return c


def _sct_clip(ring, p, q):
    """The parts of segment p-q inside the ring: [(a, b), ...]."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ts = [0.0, 1.0]
    n = len(ring)
    for i in range(n):
        (x0, y0), (x1, y1) = ring[i], ring[(i + 1) % n]
        ex, ey = x1 - x0, y1 - y0
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((x0 - p[0]) * ey - (y0 - p[1]) * ex) / den
        s = ((x0 - p[0]) * dy - (y0 - p[1]) * dx) / den
        if 0.0 < t < 1.0 and 0.0 <= s <= 1.0:
            ts.append(t)
    ts.sort()
    out = []
    for a, b in zip(ts[:-1], ts[1:]):
        if b - a < 1e-9:
            continue
        m = (a + b) / 2.0
        if _sct_inside(ring, (p[0] + dx * m, p[1] + dy * m)):
            out.append(((p[0] + dx * a, p[1] + dy * a), (p[0] + dx * b, p[1] + dy * b)))
    return out


def sct_hatch_fill(ring, material, k, outline=None, lw=0.25):
    """A cut ring (page mm) in its material's fill and standard hatch: stone, concrete, earth, gravel or water."""
    import math as _m
    if material == "water":
        return sec_water(ring)
    if material not in ("stone", "concrete", "earth", "gravel"):
        raise ValueError("sct_hatch_fill: unknown material %r" % material)
    g = max(0.7, min(1.4, k / 5.0))           # patterns are page-mm conventions (1:200 size), eased with k; no real sizes
    ln = SCT["line"]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    sh = [("poly", ring, SCT[material], None, 0.1)]
    if material == "stone":                   # coursed masonry: bed joints and staggered head joints
        c = 1.4 * g
        for p, q in sec_hatch(ring, c, 0.0):
            sh.append(("line", [p, q], ln, 0.08))
        j = int(_m.floor(min(ys) / c))
        while j * c < max(ys):
            i = int(_m.floor(min(xs) / (2 * c))) - 1
            while (2 * i + (j % 2)) * c <= max(xs):
                x = (2 * i + (j % 2)) * c
                for a, b in _sct_clip(ring, (x, j * c), (x, (j + 1) * c)):
                    sh.append(("line", [a, b], ln, 0.08))
                i += 1
            j += 1
    elif material == "concrete":              # aggregate: dots and small open triangles
        d = 1.1 * g
        for i in range(int(_m.floor(min(xs) / d)), int(_m.floor(max(xs) / d)) + 1):
            for j in range(int(_m.floor(min(ys) / d)), int(_m.floor(max(ys) / d)) + 1):
                px, py = (i + _sct_rnd(i, j)) * d, (j + _sct_rnd(j, i + 7)) * d
                if not _sct_inside(ring, (px, py)):
                    continue
                if (i + j) % 3 == 0:
                    s, a = 0.28 * g, _sct_rnd(i + 3, j) * 6.283
                    tri = [(px + s * _m.cos(a + t * 2.094), py + s * _m.sin(a + t * 2.094)) for t in range(3)]
                    sh.append(("line", tri + [tri[0]], ln, 0.07))
                else:
                    sh.append(("poly", sec_ellipse(px, py, 0.09 * g, 0.09 * g, 6), ln, None, 0.1))
    elif material == "earth":                 # earth: broken 45-degree hatch
        dash, gap = 0.9 * g, 0.55 * g
        for p, q in sec_hatch(ring, 1.3 * g, 45.0):
            L = _m.hypot(q[0] - p[0], q[1] - p[1])
            if L < 1e-6:
                continue
            ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
            s = 0.0
            while s < L:
                e = min(L, s + dash)
                sh.append(("line", [(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)], ln, 0.07))
                s = e + gap
    else:                                     # gravel: small rounded stones, open
        d = 0.9 * g
        for i in range(int(_m.floor(min(xs) / d)), int(_m.floor(max(xs) / d)) + 1):
            for j in range(int(_m.floor(min(ys) / d)), int(_m.floor(max(ys) / d)) + 1):
                px, py = (i + 0.2 + 0.6 * _sct_rnd(i, j)) * d, (j + 0.2 + 0.6 * _sct_rnd(j, i + 3)) * d
                r = (0.14 + 0.16 * _sct_rnd(i + 5, j + 1)) * g
                if _sct_inside(ring, (px, py)):
                    sh.append(("poly", sec_ellipse(px, py, r, r * 0.8, 8), None, ln, 0.06))
    if outline:
        sh.append(("poly", ring, None, outline, lw))
    return sh


def sct_ground(surface, bottom_y, k, material="earth", lw=0.35):
    """Cut ground under a surface polyline (page mm, left to right) down to bottom_y: hatch and the cut line."""
    ring = list(surface) + [(surface[-1][0], bottom_y), (surface[0][0], bottom_y)]
    return sct_hatch_fill(ring, material, k) + [("line", list(surface), SCT["cut"], lw)]


def sct_bed(x0, x1, bed_y, k, depth_m=1.0, material="gravel"):
    """The stream bed from x0 to x1 (page mm) as a cut band depth_m deep (drawing rule, not a surveyed depth)."""
    return sct_ground([(x0, bed_y), (x1, bed_y)], bed_y - depth_m * k, k, material)


def _sct_w(x, side, pts):
    """Local bank points (u landward from x, page y) -> page points."""
    return [(x + side * u, v) for u, v in pts]


def _sct_v_at(S, u):
    """Page y of a local surface S (u rising) at u; on a vertical face the upper end."""
    v = S[0][1] if u <= S[0][0] else S[-1][1]
    for (u0, v0), (u1, v1) in zip(S[:-1], S[1:]):
        if u1 > u0 and u0 <= u <= u1:
            v = v0 + (v1 - v0) * (u - u0) / (u1 - u0)
    return v


def _sct_terr(S, u0, steps, k, t):
    """Local: surface S with a flight of (rise_m, tread_m) steps cut in from u0 landward -> (new S, step rings)."""
    u, v = u0, _sct_v_at(S, u0)
    P, blocks = [(u, v)], []
    for rise, tread in steps:
        v2, u2 = v + rise * k, u + tread * k
        P += [(u, v2), (u2, v2)]
        blocks.append([(u, v - t), (u, v2), (u2, v2), (u2, v - t)])      # each step on its own bed, t below
        u, v = u2, v2
    g = _sct_v_at(S, u)
    if g > v + 1e-6:                          # ground still higher: a retaining face closes the flight
        blocks.append([(u, v - t), (u, g), (u + t, g), (u + t, v - t)])
    if abs(g - v) > 1e-6:
        P.append((u, g))
    S2 = [p for p in S if p[0] < u0 - 1e-9] + P + [p for p in S if p[0] > u + 1e-9]
    return S2, blocks


def sct_terraces(surface, x0, steps, side, k, t_m=0.15, material="concrete"):
    """Steps or terraces [(rise_m, tread_m), ...] cut into a bank surface from page x0, climbing landward (side +1 =
    to the right). Returns (new surface, step shapes); fill the ground under the new surface (sct_ground)."""
    xr = surface[0][0]
    S = [(side * (px - xr), py) for px, py in surface]
    S2, blocks = _sct_terr(S, side * (x0 - xr), steps, k, t_m * k)   # t_m: slab bed, drawing rule (not sourced)
    sh = []
    for b in blocks:
        sh += sct_hatch_fill(_sct_w(xr, side, b), material, k, SCT["cut"], 0.25)
    return _sct_w(xr, side, S2), sh


def _sct_need(p, name, kind):
    if p.get(name) is None:
        raise ValueError("sct_bank %s: %s is required (no sourced value)" % (kind, name))
    return float(p[name])


def sct_bank(kind, x, top_y, bed_y, side, k, **p):
    """One river bank at the cut: kind dsi_wall | embankment | earth | railing | parapet. x = toe (water face of a
    wall), side +1 = land to the right of x. Returns (shapes, surface: page points from the toe landward)."""
    import math as _m
    reach = p.get("reach_m", 4.0) * k        # drawing rule: land drawn 4 m behind the crest
    bot = bed_y - p.get("depth_m", 1.0) * k   # drawing rule: cut ground drawn 1 m below the bed
    sh = []
    if kind == "railing":                     # post with the handrail and mid rail in cut (symbols, no sourced sizes)
        h = _sct_need(p, "h_m", kind) * k
        r = max(0.35, 0.03 * k)
        sh = [("line", [(x, top_y), (x, top_y + h)], SCT["cut"], 0.25),
              ("poly", sec_ellipse(x, top_y + h, r, r, 10), SCT["cut"], None, 0.1),
              ("poly", sec_ellipse(x, top_y + h * 0.5, r * 0.6, r * 0.6, 8), SCT["cut"], None, 0.1)]
        return sh, []
    if kind == "parapet":                     # solid wall on the crest, from x landward
        h, t = _sct_need(p, "h_m", kind) * k, _sct_need(p, "t_m", kind) * k
        ring = [(0.0, top_y), (0.0, top_y + h), (t, top_y + h), (t, top_y)]
        sh = sct_hatch_fill(_sct_w(x, side, ring), p.get("material", "stone"), k, SCT["cut"], 0.35)
        return sh, _sct_w(x, side, [(0.0, top_y + h), (t, top_y + h)])
    if kind == "dsi_wall":                    # the DSİ stone wall; thickness t_m not sourced: required
        t = _sct_need(p, "t_m", kind) * k
        if top_y is None:
            top_y = bed_y + SCT_DSI_WALL_H_M * k
        wall = [(0.0, bed_y), (0.0, top_y), (t, top_y), (t, bed_y)]
        back = [(t, top_y), (t + reach, top_y), (t + reach, bot), (0.0, bot), (0.0, bed_y), (t, bed_y)]
        S = [(0.0, bed_y), (0.0, top_y), (t + reach, top_y)]
        sh += sct_hatch_fill(_sct_w(x, side, back), "earth", k)
        sh += sct_hatch_fill(_sct_w(x, side, wall), p.get("material", "stone"), k, SCT["cut"], 0.35)
        W = _sct_w(x, side, S)
        sh.append(("line", W, SCT["cut"], 0.35))
        return sh, W
    if kind in ("embankment", "earth"):       # angle_deg (toe to crest) or run_m required
        if p.get("run_m") is not None:
            run = float(p["run_m"]) * k
        else:
            run = (top_y - bed_y) / _m.tan(_m.radians(_sct_need(p, "angle_deg", kind)))
        if kind == "embankment":
            S = [(0.0, bed_y), (run, top_y), (run + reach, top_y)]
        else:                                 # loose earth: soft toe and rounded crest, same toe, crest and run
            n = 12
            S = [(run * i / n, bed_y + (top_y - bed_y) * (3 * (i / float(n)) ** 2 - 2 * (i / float(n)) ** 3))
                 for i in range(n + 1)] + [(run + reach, top_y)]
        blocks = []
        if p.get("steps"):
            S, blocks = _sct_terr(S, p.get("steps_from_m", 0.0) * k, p["steps"], k, p.get("step_t_m", 0.15) * k)
        sh += sct_hatch_fill(_sct_w(x, side, S + [(S[-1][0], bot), (0.0, bot)]), p.get("material", "earth"), k)
        if p.get("revet") and kind == "embankment" and not blocks:   # pitching on the slope, revet_t_m thick
            tt = _sct_need(p, "revet_t_m", kind) * k
            L = _m.hypot(run, top_y - bed_y)
            nx, ny = (top_y - bed_y) / L * tt, -run / L * tt              # into the bank
            ring = [(0.0, bed_y), (run, top_y), (run + nx, top_y + ny), (nx, bed_y + ny)]
            sh += sct_hatch_fill(_sct_w(x, side, ring), p["revet"], k, SCT["cut"], 0.2)
        for b in blocks:
            sh += sct_hatch_fill(_sct_w(x, side, b), p.get("step_material", "concrete"), k, SCT["cut"], 0.25)
        W = _sct_w(x, side, S)
        sh.append(("line", W, SCT["cut"], 0.35))
        return sh, W
    raise ValueError("sct_bank: unknown kind %r" % kind)


def sct_profile(left, right):
    """One cross-section line, left to right, from the left bank surface (side -1) and the right one (side +1)."""
    return list(reversed(left)) + list(right)


def sct_channel(profile, wl_y, spacing=0.6):
    """The water standing at page y wl_y in a profile (left to right): sec_water shapes, one per wet stretch."""
    sh, run = [], []
    P = list(profile)
    for i, a in enumerate(P):
        if a[1] < wl_y:
            if not run:
                if i > 0:
                    b = P[i - 1]
                    t = (wl_y - b[1]) / (a[1] - b[1])
                    run.append((b[0] + (a[0] - b[0]) * t, wl_y))
                else:
                    run.append((a[0], wl_y))
            run.append(a)
        elif run:
            b = P[i - 1]
            t = (wl_y - b[1]) / (a[1] - b[1])
            run.append((b[0] + (a[0] - b[0]) * t, wl_y))
            sh += sec_water(run, spacing)
            run = []
    if run:
        run.append((P[-1][0], wl_y))
        sh += sec_water(run, spacing)
    return sh

# ---- plants (WO-T2b-3, 29 Oct 2026): every species of the revised planting as ONE primitive with two matching views,
# pla_section() (silhouette on the ground) and pla_plan() (top-view crown): same crown width, form and colour. Crops
# as rows at their spacing. Common reed and water mint only inside lined, off-line cells (D2 a, D6), never free.
# Needs section_parts.py (SEC, sec_ellipse, sec_water, _sec_mix, sct_hatch_fill) included before this file.
# Data: revision_2026-10-29/T1/ecology/species.json "species_data" (S-numbers as there) and RESULT.md §A-B.
# Removed by D6 and not offered: yellow flag iris, oleander, broadleaf cattail, white poplar, fig, citrus (and elm).
# Drawing size rules (the sources give ranges or only a maximum; data comments only, never printed):
#   height h_m  = middle of the sourced mature range; half of it where only a maximum is sourced.
#   crown crown_m = middle of the sourced spread; half of a sourced maximum; where no spread is sourced,
#                 h_m x PLA_FORM_RATIO[form] (rule read from the crown words in species.json).
#   clear stem, trunk width, lobes and stem counts: form rules in _pla_sec (drawing rules).
#   ("poly", ring, fill, stroke, lw)    ("line", pts, colour, lw)          page mm, y up; k = page mm per m

PLA_FORM_RATIO = dict(dome=1.0, oval=0.7, weeping=0.7, gnarled=0.9, umbrella=0.55, feathery=0.8, clump=0.6,
                      tussock=1.0, mound=1.2)   # crown / height where no spread is sourced (drawing rule)

PLA_LEAF_SITE = [4, 5, 6, 7, 8, 9, 10, 11]   # leaf-out 16 Apr, leaf-fall 14 Nov: site Sentinel-2 2019-2025 for all
                                             # broadleaved deciduous crowns (selinus_board_v50 LEAF_DOY; RESULT §B)
PLA_ALL_YEAR = list(range(1, 13))

PLA_PURPLE = "8C7088"     # palette SCHEMES D1 institutional / D5 civic: loosestrife purple (RESULT §A "purple, Jun-Sep")
PLA_REMOVE = "8B3A3F"     # palette CORE accent: the 'remove' cross on giant reed
PLA_FIELD = "C6C08D"      # palette MASTERPLAN agriculture light: field ground
PLA_ROW = "948B49"        # palette MASTERPLAN agriculture mid: crop rows
PLA_WET = "CBEDE5"        # palette MASTERPLAN wetland light: lined cell in plan
PLA_BOLL = "FAF8F1"       # palette CORE road: cotton bolls
PLA_FRUIT = "BC6F45"      # palette SCHEMES D1 commercial: tomato fruit


def _pla_c(fill, accent=None, stem=None):
    """The colour set of one species: fill, edge, lighter lobes, stem, accent (same in both views)."""
    return dict(fill=fill, edge=SEC["ink2"], lt=_sec_mix(fill, SEC["paper"], 0.35), stem=stem or SEC["trunk"],
                accent=accent)


# one entry per species (species.json species_data + giant reed from the screening); h_range = sourced (lo, hi) m
PLA_SPECIES = {
    "plane": dict(name="Oriental plane", turkish="Doğu çınarı", latin="Platanus orientalis", layer="tree",
                  form="dome", foliage="deciduous (S26)", status="keep",
                  h_range=(None, 30.0), h_m=15.0,            # "up to 30 m" S68, S69
                  crown_m=15.0,                              # "wider than 8 metres" S70: form rule 1.0 x h (>= 8)
                  bloom=[4, 5], leaf=PLA_LEAF_SITE,          # Apr-May S69 (secondary)
                  colours=_pla_c(SEC["crown"])),             # section_style SEC crown
    "ash": dict(name="Narrow-leaved ash", turkish="Dişbudak", latin="Fraxinus angustifolia", layer="tree",
                form="oval", foliage="deciduous (S7)", status="keep",
                h_range=(None, 40.0), h_m=20.0,              # "40-45m" maximum S7 (lower figure)
                crown_m=14.0,                                # "dense, irregular and dome shaped" S7: rule 0.7 x h
                bloom=[], leaf=PLA_LEAF_SITE,                # "early spring or even in autumn" S7: no months
                colours=_pla_c(_sec_mix("727A4E", SEC["paper"], 0.15))),   # CORE green_mid
    "willow": dict(name="White willow", turkish="Ak söğüt", latin="Salix alba", layer="tree",
                   form="weeping", foliage="deciduous (not quoted)", status="keep",
                   h_range=(None, 30.0), h_m=15.0,           # "up to 30 m" S4
                   crown_m=10.5,                             # crown not found: rule 0.7 x h
                   bloom=[], leaf=PLA_LEAF_SITE,             # "spring" catkins S4: no months
                   colours=_pla_c(_sec_mix("8C9969", SEC["paper"], 0.3))),  # CORE green_light, silvered
    "olive": dict(name="Olive", turkish="Zeytin", latin="Olea europaea", layer="tree",
                  form="gnarled", foliage="evergreen (S72)", status="keep",
                  h_range=(8.0, 15.0), h_m=11.5,             # "8-15 m" S72
                  crown_m=10.35,                             # crown not found: rule 0.9 x h
                  bloom=[4], leaf=PLA_ALL_YEAR,              # full bloom 21-24 Apr, ends 29 Apr-1 May S73 (Ege Univ.)
                  colours=_pla_c(SEC["olive"])),             # section_style SEC olive
    "stone_pine": dict(name="Stone pine", turkish="Fıstık çamı", latin="Pinus pinea", layer="tree",
                       form="umbrella", foliage="evergreen conifer (S74)", status="keep (processionary caterpillar)",
                       h_range=(25.0, 30.0), h_m=27.5,       # "25-30 m" S74
                       crown_m=15.1,                         # "umbrella-shaped ... flat and broad" S74: rule 0.55 x h
                       bloom=[], leaf=PLA_ALL_YEAR,          # pollen months not found
                       colours=_pla_c(SEC["pine"])),         # section_style SEC pine
    "tamarisk": dict(name="Tamarisk", turkish="Ilgın", latin="Tamarix smyrnensis", layer="tree",
                     form="feathery", foliage="deciduous (S9b, genus)", status="keep (replaces oleander)",
                     h_range=(4.0, 15.0), h_m=9.5,           # "4-15 m" S9b (genus)
                     crown_m=7.6,                            # "broad, bushy" S9b: rule 0.8 x h
                     bloom=[], leaf=PLA_LEAF_SITE,           # bloom not found for T. smyrnensis
                     colours=_pla_c(_sec_mix("8C9969", SEC["paper"], 0.45))),  # CORE green_light, pale
    "chaste": dict(name="Chaste tree", turkish="Hayıt", latin="Vitex agnus-castus", layer="shrub",
                   form="multistem", foliage="deciduous (S58)", status="keep (replaces oleander, fig, citrus)",
                   h_range=(1.0, 3.0), h_m=2.0,              # "1-3 m" S58
                   crown_m=2.0,                              # "1.5-2.5 m" S67 (RHS, UK)
                   bloom=[6, 7, 8, 9], leaf=PLA_LEAF_SITE,   # "(Apr-)Jun-Sep" S58 (Crete); Apr-May occasional
                   colours=_pla_c(SEC["shrub"], SEC["lav"])),  # flower colour not sourced: section_style lav
    "rosemary": dict(name="Rosemary", turkish="Biberiye", latin="Salvia rosmarinus", layer="shrub",
                     form="mound", foliage="evergreen (S58, S71)", status="keep",
                     h_range=(0.5, 1.0), h_m=0.75,           # "50-100 cm" S58 (Crete)
                     crown_m=0.75,                           # "1.5-2.5 m" S71 for 1.5-2.5 m plants: scaled to h
                     bloom=[1, 2, 3, 4, 5], leaf=PLA_ALL_YEAR,  # "Jan-May, intermittently to Dec" S58
                     colours=_pla_c(_sec_mix("495338", SEC["paper"], 0.35))),  # CORE green_deep
    "lavender": dict(name="French lavender", turkish="Karabaş otu", latin="Lavandula stoechas", layer="ground",
                     form="mound", foliage="evergreen (UNVERIFIED)", status="keep",
                     h_range=(0.3, 0.8), h_m=0.55,           # "30-80 cm" S58
                     crown_m=0.66,                           # crown not found: rule 1.2 x h
                     bloom=[3, 4, 5], leaf=[],               # "Mar-May" S58; evergreen unverified: no leaf months
                     colours=_pla_c(_sec_mix(SEC["olive"], SEC["paper"], 0.1), SEC["lav"])),  # as sec_lavender
    "loosestrife": dict(name="Purple loosestrife", turkish="Aklar otu", latin="Lythrum salicaria", layer="emergent",
                        form="clump", foliage="herbaceous perennial", status="keep, flower heads cut in Sep (D6)",
                        h_range=(0.3, 2.4), h_m=1.35,        # "0.3-2.4 m" S19
                        crown_m=0.75,                        # "5 feet (1.5 m) wide" mature S19: half the maximum
                        bloom=[6, 7, 8, 9], leaf=[],         # "June ... September" S19; cut Sep (D6)
                        colours=_pla_c(SEC["grass"], PLA_PURPLE)),
    "soft_rush": dict(name="Soft rush", turkish="UNVERIFIED", latin="Juncus effusus", layer="emergent",
                      form="clump", foliage="not found", status="new (replaces iris and cattail)",
                      h_range=(0.5, 1.5), h_m=1.0,           # "5-15 dm tall" S59
                      crown_m=0.6,                           # "tufted, cespitose" S59: rule 0.6 x h
                      bloom=[5, 6, 7, 8], leaf=[],           # "late May-Aug, occasionally Sep" S59 (USA)
                      colours=_pla_c(SEC["reed"])),          # section_style SEC reed
    "rush": dict(name="Sharp rush", turkish="Kofa", latin="Juncus acutus", layer="emergent",
                 form="tussock", foliage="not found", status="keep, away from paths and the wading strip",
                 h_range=(0.6, 1.0), h_m=0.8,                # "(40-)60-100 cm" S65
                 crown_m=0.8,                                # "dense tussock" S60, S65: rule 1.0 x h
                 bloom=[], leaf=[],                          # "summer" S65 (NZ): no months
                 colours=_pla_c(_sec_mix(SEC["reed"], "495338", 0.3))),   # SEC reed toward CORE green_deep
    "reed": dict(name="Common reed", turkish="Kamış", latin="Phragmites australis", layer="emergent",
                 form="stand", foliage="deciduous (S2)", status="lined off-line basins only (D2 a): pla_reed_basin",
                 h_range=(None, 6.0), h_m=3.0,               # "may reach 20 feet (6 m)" S2 (booklet drew 1.9-2.2 m)
                 crown_m=None,                               # clonal stand, no crown
                 bloom=[7, 8, 9, 10, 11], leaf=[],           # "July to November" S2 (range-wide); plumes cut before Nov
                 colours=_pla_c(SEC["reed"], SEC["reed_head"])),
    "mint": dict(name="Water mint", turkish="Su nanesi", latin="Mentha aquatica", layer="emergent",
                 form="mound", foliage="deciduous (S57)", status="lined basin cells only (D6): pla_mint_cell",
                 h_range=(0.3, 0.8), h_m=0.55,               # "30-80 cm" S58
                 crown_m=0.75,                               # "spread 0.5-1 m" S57
                 bloom=[5, 6, 7, 8, 9], leaf=[],             # "May-Sep" S58
                 colours=_pla_c(SEC["grass"])),              # section_style SEC grass
    "giant_reed": dict(name="Giant reed", turkish="Kargı", latin="Arundo donax", layer="emergent",
                       form="cane", foliage="not found", status="REMOVE (raises flood risk, S36)",
                       h_range=(None, None), h_m=None, crown_m=None,   # not in species_data: pass h_m and crown_m
                       bloom=[], leaf=[],
                       colours=_pla_c(SEC["beyond"], PLA_REMOVE)),
}

# crops: row spacing only where sourced (library/research/crops_2026-10-24, card f506; no other spacing in library/)
PLA_CROPS = {
    "olive": dict(name="Olive orchard", row_m=7.0, plant_m=5.0,   # Kaya et al. 2017 Irrig. Drain. 66(5) p.821:
                  h_m=None, crown_m=None),     # Memecik "planted 5 × 7 m apart" (order of the pair not stated)
    "cotton": dict(name="Cotton", row_m=None, plant_m=None, h_m=None, crown_m=None),   # not found: pass spacing
    "maize": dict(name="Maize (corn)", row_m=None, plant_m=None, h_m=None, crown_m=None),   # not found
    "tomato": dict(name="Tomato (processing)", row_m=None, plant_m=None, h_m=None, crown_m=None),   # not found
}


def pla_months(key):
    """Sourced months (1-12) of a species: bloom, in leaf and flower-head cut (empty lists where not sourced)."""
    sp = PLA_SPECIES[key]
    return dict(bloom=list(sp["bloom"]), leaf=list(sp["leaf"]), cut=[9] if key == "loosestrife" else [])


def _pla_rnd(i, s=0):
    """A fixed pseudo-random number in [0, 1)."""
    import math as _m
    v = _m.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - _m.floor(v)


def _pla_crown(cx, cy, rx, up, dn, seed=0, wob=0.08, n=40):
    """A lobed crown outline: rx each side, up above and dn below cy; its widest points stay at cx +- rx."""
    import math as _m
    L = 2 * (3 + int(_pla_rnd(seed, 1) * 3))       # even lobe count: full width kept at a = 0 and pi
    out = []
    for i in range(n):
        a = 2 * _m.pi * i / n
        f = 1.0 - wob * _m.sin(L * a / 2.0) ** 2
        s = _m.sin(a)
        out.append((cx + rx * f * _m.cos(a), cy + (up if s > 0 else dn) * f * s))
    return out


def _pla_cols(sp, beyond):
    c = dict(sp["colours"])
    if beyond:                                  # beyond the cut: paler (as SEC beyond)
        c = dict((k_, _sec_mix(v, SEC["paper"], 0.55) if v else v) for k_, v in c.items())
    return c


def _pla_sec(form, x, gy, h, w, k, c, seed=0):
    """Section silhouette of one form, h tall and w crown wide (m), ground at (x, gy) page mm."""
    import math as _m
    H, R = h * k, w / 2.0 * k
    f, e, lt, st, ac = c["fill"], c["edge"], c["lt"], c["stem"], c.get("accent")
    sh = []
    if form in ("dome", "oval", "weeping", "gnarled", "umbrella"):
        lo = dict(dome=0.3, oval=0.3, weeping=0.25, gnarled=0.3, umbrella=0.65)[form] * H   # clear stem (rule)
        tw = max(0.15, h / 60.0 * k)            # half trunk width: trunk 1/30 of the height (rule)
        yb, yt = gy + lo, gy + H
        Hc = yt - yb
        if form == "gnarled":                   # two twisting stems
            for s_ in (-1, 1):
                sh.append(("poly", [(x + s_ * 0.2 * tw, gy), (x + s_ * 1.6 * tw, gy),
                                    (x + s_ * (0.35 * R + tw * 0.5), yb + 0.3 * Hc),
                                    (x + s_ * (0.35 * R - tw * 0.5), yb + 0.3 * Hc)], st, None, 0.1))
        else:
            lean = 0.03 * H if form == "umbrella" else 0.0
            sh.append(("poly", [(x - tw, gy), (x + tw, gy), (x + lean + tw * 0.6, yb + 0.4 * Hc),
                                (x + lean - tw * 0.6, yb + 0.4 * Hc)], st, None, 0.1))
        if form == "weeping":                   # the hanging curtain behind the crown
            c0 = yb + 0.45 * Hc
            sh.append(("poly", [(x - R, c0), (x - 0.9 * R, gy + 0.2 * H), (x + 0.9 * R, gy + 0.2 * H), (x + R, c0)],
                       lt, None, 0.1))
        if form == "gnarled":                   # low and wide: three irregular masses
            for cx_, cy_, rx_, up_, i in ((x - 0.5 * R, yb + 0.4 * Hc, 0.5 * R, 0.4 * Hc, 0),
                                          (x + 0.5 * R, yb + 0.45 * Hc, 0.5 * R, 0.4 * Hc, 1),
                                          (x, yb + 0.62 * Hc, 0.55 * R, 0.38 * Hc, 2)):
                dn_ = cy_ - yb if i < 2 else 0.38 * Hc
                sh.append(("poly", _pla_crown(cx_, cy_, rx_, up_, dn_, seed + i, 0.18), f, e, 0.08))
        else:
            fr = dict(dome=(0.3, 0.06), oval=(0.5, 0.08), weeping=(0.45, 0.05), umbrella=(0.35, 0.04))[form]
            c0 = yb + fr[0] * Hc
            sh.append(("poly", _pla_crown(x, c0, R, yt - c0, c0 - yb, seed, fr[1]), f, e, 0.08))
            for i, (dx, dy, s_) in enumerate(((-0.4, 0.3, 0.32), (0.35, 0.15, 0.3), (-0.05, 0.6, 0.26))):
                sh.append(("poly", _pla_crown(x + dx * R, c0 + dy * (yt - c0), s_ * R, s_ * (yt - c0) * 0.8,
                                              s_ * (yt - c0) * 0.6, seed + i + 1, 0.1), lt, None, 0.1))
        if form == "weeping":                   # strands
            for i in range(9):
                xs = x - 0.85 * R + i * 1.7 * R / 8.0
                s_ = -1 if xs < x else 1
                yh = gy + (0.2 + 0.08 * _pla_rnd(i, seed)) * H
                y0 = yb + 0.3 * Hc
                sh.append(("line", [(xs, y0), (xs + s_ * 0.04 * R, (y0 + yh) / 2.0), (xs + s_ * 0.06 * R, yh)], e, 0.1))
        if form in ("dome", "oval"):            # a few branches
            for s_, a in ((-1, 55.0), (1, 45.0), (1, 75.0)):
                r_ = _m.radians(a)
                sh.append(("line", [(x, yb + 0.3 * Hc), (x + s_ * _m.cos(r_) * R * 0.5, yb + (0.3 + 0.4 * _m.sin(r_))
                                                         * Hc)], st, max(0.08, tw * 0.5)))
        return sh
    if form == "feathery":                      # tamarisk: slender stems, an airy crown, hanging wisps
        for i in range(4):
            sh.append(("line", [(x + (i - 1.5) * 0.04 * R, gy), (x + (i - 1.5) * 0.3 * R, gy + 0.55 * H)], st, 0.15))
        c0 = gy + 0.55 * H
        ring = _pla_crown(x, c0, R, 0.45 * H, 0.4 * H, seed, 0.14)
        sh.append(("poly", ring, f, None, 0.1))
        for i in range(0, len(ring), 2):
            px, py = ring[i]
            if py > c0 - 0.3 * H:
                sh.append(("line", [(px, py), (px + (px - x) * 0.04, py - 0.1 * H)], e, 0.08))
        return sh
    if form == "multistem":                     # chaste tree: stems fanning from the ground, heads at their ends
        heads = ((-0.7, 0.6, 0.25), (-0.35, 0.68, 0.27), (0.0, 0.72, 0.28), (0.35, 0.66, 0.27), (0.7, 0.58, 0.25))
        for dx, cy_, ry_ in heads:
            sh.append(("line", [(x + dx * 0.1 * R, gy), (x + dx * R, gy + cy_ * H)], st, 0.15))
        for i, (dx, cy_, ry_) in enumerate(heads):
            sh.append(("poly", _pla_crown(x + dx * R, gy + cy_ * H, 0.3 * R, ry_ * H, ry_ * H * 0.8, seed + i, 0.12),
                       f, e, 0.06))
        if ac:
            for dx, cy_, ry_ in heads:
                top = gy + (cy_ + ry_) * H
                sh.append(("line", [(x + dx * R, top - 0.14 * H), (x + dx * R, top - 0.01 * H)], ac, 0.3))
        return sh
    if form == "mound":                         # lavender, rosemary, water mint: a low dome on the ground
        sh.append(("poly", _pla_crown(x, gy + 0.35 * H, R, 0.65 * H, 0.35 * H, seed, 0.1), f, e, 0.06))
        if ac:                                  # flower spikes in the top of the mound
            for d in (-0.5, -0.2, 0.15, 0.45):
                sh.append(("line", [(x + d * R, gy + 0.72 * H), (x + d * R * 1.1, gy + 0.97 * H)], ac, 0.25))
        else:
            for d in (-0.55, -0.25, 0.05, 0.35, 0.6):
                sh.append(("line", [(x + d * R, gy + 0.35 * H), (x + d * R * 1.05, gy + 0.7 * H)], lt, 0.1))
        return sh
    if form in ("clump", "tussock", "cane"):    # rushes and loosestrife: stems from one base; giant reed: canes
        n = dict(clump=13, tussock=21, cane=7)[form]
        for i in range(n):
            t = i / float(n - 1)
            hh = H * (0.82 + 0.18 * _pla_rnd(i, seed + 3))
            bx, tx = x + (2 * t - 1) * R * 0.15, x + (2 * t - 1) * R
            if form == "clump":                 # soft arch
                mx = bx + (tx - bx) * 0.35
                sh.append(("line", [(bx, gy), (mx, gy + 0.55 * hh), (tx, gy + hh)], f, 0.12))
                if ac and i % 2 == 0:           # loosestrife flower spike on the upper stem
                    sh.append(("line", [(mx + (tx - mx) * 0.3, gy + 0.69 * hh), (tx, gy + hh)], ac, 0.35))
            else:
                sh.append(("line", [(bx, gy), (tx, gy + hh)], f, 0.15 if form == "cane" else 0.1))
                if form == "cane":              # leaf blades along the cane
                    for j in range(1, 5):
                        py = gy + hh * j / 5.0
                        px = bx + (tx - bx) * j / 5.0
                        s_ = 1 if (i + j) % 2 else -1
                        sh.append(("line", [(px, py), (px + s_ * 0.35 * R, py - 0.06 * hh)], f, 0.1))
        if form == "cane" and ac:               # marked for removal
            sh.append(("line", [(x - R, gy), (x + R, gy + H)], ac, 0.35))
            sh.append(("line", [(x - R, gy + H), (x + R, gy)], ac, 0.35))
        return sh
    raise ValueError("_pla_sec: unknown form %r" % form)


def _pla_scallop(cx, cy, r, m, depth, n=72):
    """A scalloped circle of radius r (its bumps reach r), m bumps."""
    import math as _m
    return [(cx + r * (1.0 - depth * _m.sin(m * a / 2.0) ** 2) * _m.cos(a),
             cy + r * (1.0 - depth * _m.sin(m * a / 2.0) ** 2) * _m.sin(a))
            for a in [2 * _m.pi * i / n for i in range(n)]]


def _pla_plan(form, cx, cy, w, k, c, seed=0):
    """Top view of one form, crown w wide (m), centre (cx, cy) page mm."""
    import math as _m
    r = w / 2.0 * k
    f, e, lt, st, ac = c["fill"], c["edge"], c["lt"], c["stem"], c.get("accent")
    sh = []
    dot = ("poly", sec_ellipse(cx, cy, max(0.2, 0.04 * r), max(0.2, 0.04 * r), 10), st, None, 0.1)
    if form in ("dome", "oval"):
        m, dp, s_ = (10, 0.1, 0.3) if form == "dome" else (16, 0.06, 0.22)
        sh.append(("poly", _pla_scallop(cx, cy, r, m, dp), f, e, 0.08))
        for i in range(3 if form == "dome" else 4):
            a = 2 * _m.pi * (i / (3.0 if form == "dome" else 4.0) + _pla_rnd(seed, 4))
            sh.append(("poly", _pla_scallop(cx + 0.45 * r * _m.cos(a), cy + 0.45 * r * _m.sin(a), s_ * r, 6, 0.12),
                       lt, None, 0.1))
        return sh + [dot]
    if form == "weeping":
        sh.append(("poly", _pla_scallop(cx, cy, r, 24, 0.04), f, e, 0.08))
        for i in range(20):
            a = 2 * _m.pi * i / 20.0
            sh.append(("line", [(cx + 0.25 * r * _m.cos(a), cy + 0.25 * r * _m.sin(a)),
                                (cx + 0.95 * r * _m.cos(a), cy + 0.95 * r * _m.sin(a))], e, 0.08))
        return sh + [dot]
    if form == "gnarled":                       # three masses, as in section
        for i in range(3):
            a = 2 * _m.pi * (0.25 + i / 3.0)
            sh.append(("poly", _pla_crown(cx + 0.45 * r * _m.cos(a), cy + 0.45 * r * _m.sin(a), 0.55 * r, 0.55 * r,
                                          0.55 * r, seed + i, 0.18), f, e, 0.08))
        return sh + [dot]
    if form == "umbrella":                      # flat disc with needle tufts at the rim
        sh.append(("poly", _pla_scallop(cx, cy, r, 30, 0.03), f, e, 0.08))
        for i in range(30):
            a = 2 * _m.pi * i / 30.0
            sh.append(("line", [(cx + 0.75 * r * _m.cos(a), cy + 0.75 * r * _m.sin(a)),
                                (cx + 0.96 * r * _m.cos(a), cy + 0.96 * r * _m.sin(a))], lt, 0.1))
        return sh + [dot]
    if form == "feathery":
        sh.append(("poly", _pla_crown(cx, cy, r, r, r, seed, 0.14), f, None, 0.1))
        for i in range(28):
            a = 2 * _m.pi * i / 28.0
            sh.append(("line", [(cx + 0.82 * r * _m.cos(a), cy + 0.82 * r * _m.sin(a)),
                                (cx + 0.82 * r * _m.cos(a + 0.12), cy + 0.82 * r * _m.sin(a + 0.12))], e, 0.08))
        return sh + [dot]
    if form == "multistem":                     # five heads, as in section
        for i in range(5):
            a = 2 * _m.pi * (i / 5.0 + 0.05)
            hx, hy = cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a)
            sh.append(("poly", _pla_crown(hx, hy, 0.45 * r, 0.45 * r, 0.45 * r, seed + i, 0.12), f, e, 0.06))
            if ac:
                sh.append(("poly", sec_ellipse(hx, hy, 0.08 * r, 0.08 * r, 8), ac, None, 0.1))
        return sh
    if form == "mound":
        sh.append(("poly", _pla_crown(cx, cy, r, r, r, seed, 0.1), f, e, 0.06))
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + _pla_rnd(seed, 6))
            px, py = cx + 0.5 * r * _m.cos(a), cy + 0.5 * r * _m.sin(a)
            if ac:
                sh.append(("poly", sec_ellipse(px, py, 0.12 * r, 0.12 * r, 8), ac, None, 0.1))
            else:
                sh.append(("line", [(px, py), (px + 0.2 * r * _m.cos(a), py + 0.2 * r * _m.sin(a))], lt, 0.1))
        return sh
    if form in ("clump", "tussock", "cane"):    # stems seen from above: a starburst
        n = dict(clump=13, tussock=21, cane=9)[form]
        for i in range(n):
            a = 2 * _m.pi * (i / float(n) + 0.3 * _pla_rnd(i, seed))
            ll = r * (0.8 + 0.2 * _pla_rnd(i, seed + 2))
            sh.append(("line", [(cx, cy), (cx + ll * _m.cos(a), cy + ll * _m.sin(a))], f, 0.12))
            if ac and form == "clump" and i % 2 == 0:
                sh.append(("poly", sec_ellipse(cx + ll * _m.cos(a), cy + ll * _m.sin(a), 0.08 * r + 0.1,
                                               0.08 * r + 0.1, 8), ac, None, 0.1))
        if form == "cane" and ac:
            d = r * 0.7
            sh += [("line", [(cx - d, cy - d), (cx + d, cy + d)], ac, 0.35),
                   ("line", [(cx - d, cy + d), (cx + d, cy - d)], ac, 0.35)]
        return sh
    raise ValueError("_pla_plan: unknown form %r" % form)


def _pla_get(key):
    if key not in PLA_SPECIES:
        raise ValueError("plants: unknown species %r (removed by D6, or not in species.json)" % key)
    if key in ("reed", "mint"):
        raise ValueError("plants: %s grows only in lined cells: use pla_reed_basin / pla_mint_cell" % key)
    return PLA_SPECIES[key]


def _pla_size(key, sp, h_m, crown_m):
    h, w = h_m or sp["h_m"], crown_m or sp["crown_m"]
    if h is None or w is None:
        raise ValueError("plants: %s has no sourced size: pass h_m and crown_m" % key)
    return h, w


# species / crops with a high-res silhouette (hires.py, assets_2 30 Oct): same genus stand-ins per GAPS.md A
PLA_HIRES = dict(plane="plane", ash="ash", olive="olive", stone_pine="stone_pine", maize="maize", tomato="tomato")


def _pla_hr(key, x, gy, h, w, c, seed):
    """the high-res silhouette in the species' own fill (this section's colours, paler beyond), mirrored on odd
    seeds; None -> the primitive"""
    return hr_side(PLA_HIRES.get(key), x, gy, 1.0, h, w, c["fill"], facing=-1 if seed % 2 else 1) if key in PLA_HIRES \
        else None


def pla_section(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0, hires=True):
    """A species in section at true size: ground at (x, gy) page mm (gy may be a function of x). hires: the high-res
    silhouette where the library has one (detailed sections); False for sketchy drawings and diagrams."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    g, c = gy(x) if callable(gy) else gy, _pla_cols(sp, beyond)
    sh = _pla_hr(key, x, g, h * k, w * k, c, seed) if hires else None
    return sh or _pla_sec(sp["form"], x, g, h, w, k, c, seed)


def pla_plan(key, cx, cy, k, crown_m=None, beyond=False, seed=0):
    """The same species from above: crown crown_m wide (m) centred on (cx, cy) page mm, same form and colour."""
    sp = _pla_get(key)
    w = crown_m or sp["crown_m"]
    if w is None:
        raise ValueError("plants: %s has no sourced crown: pass crown_m" % key)
    return _pla_plan(sp["form"], cx, cy, w, k, _pla_cols(sp, beyond), seed)


def _pla_crop_size(crop, h_m, crown_m):
    if crop == "olive":                         # orchard trees kept to their in-row spacing (rule); h by the olive ratio
        w = crown_m or PLA_CROPS["olive"]["plant_m"]
        return h_m or w / PLA_FORM_RATIO["gnarled"], w
    if h_m is None or crown_m is None:
        raise ValueError("plants: %s plant size is not sourced: pass h_m and crown_m" % crop)
    return h_m, crown_m


def _pla_crop_sec(crop, x, gy, h, w, k, i, beyond):
    """One crop plant in section."""
    if crop == "olive":
        c = _pla_cols(PLA_SPECIES["olive"], beyond)
        return _pla_hr("olive", x, gy, h * k, w * k, c, i) or _pla_sec("gnarled", x, gy, h, w, k, c, i)
    H, R = h * k, w / 2.0 * k
    c = _pla_cols(dict(colours=_pla_c(SEC["grass"])), beyond)
    sh = _pla_hr(crop, x, gy, H, 2.0 * R, c, i)
    if sh:
        return sh
    if crop == "maize":                         # stalk, arching leaves, tassel
        sh = [("line", [(x, gy), (x, gy + H)], c["fill"], 0.2)]
        for j in range(1, 7):
            py, s_ = gy + H * (0.15 + 0.11 * j), (1 if j % 2 else -1)
            sh.append(("line", [(x, py), (x + s_ * R * 0.6, py + 0.08 * H), (x + s_ * R, py - 0.02 * H)], c["fill"],
                       0.12))
        sh.append(("line", [(x, gy + 0.92 * H), (x, gy + H)], SEC["reed_head"], 0.35))
        return sh
    if crop == "cotton":                        # small branched bush with open bolls
        sh = [("line", [(x, gy), (x, gy + 0.5 * H)], c["stem"], 0.12),
              ("poly", _pla_crown(x, gy + 0.55 * H, R, 0.45 * H, 0.3 * H, i, 0.15), c["fill"], c["edge"], 0.06)]
        for d, e_ in ((-0.5, 0.6), (0.1, 0.85), (0.55, 0.55)):
            sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.1 * R + 0.1, 0.1 * R + 0.1, 8), PLA_BOLL,
                       c["edge"], 0.05))
        return sh
    if crop == "tomato":                        # low sprawling plant with fruit
        sh = [("poly", _pla_crown(x, gy + 0.3 * H, R, 0.7 * H, 0.3 * H, i, 0.15), c["fill"], c["edge"], 0.06)]
        for d, e_ in ((-0.45, 0.35), (0.2, 0.5), (0.6, 0.3)):
            sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.08 * R + 0.1, 0.08 * R + 0.1, 8), PLA_FRUIT,
                       None, 0.1))
        return sh
    raise ValueError("plants: unknown crop %r" % crop)


def pla_crop_rows(crop, x0, x1, gy, k, spacing=None, h_m=None, crown_m=None, beyond=False):
    """Crop plants along a cut from x0 to x1 (page mm), spacing m apart (the row spacing for a cut across the rows;
    sourced default only for olive), centred in the stretch; gy a number or a function of x."""
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    sp = spacing or PLA_CROPS[crop]["row_m"]
    if sp is None:
        raise ValueError("plants: %s row spacing is not sourced: pass spacing (m)" % crop)
    h, w = _pla_crop_size(crop, h_m, crown_m)
    n = int((x1 - x0) / (sp * k) + 1e-9)
    off = ((x1 - x0) - n * sp * k) / 2.0
    sh = []
    for i in range(n + 1):
        x = x0 + off + i * sp * k
        sh += _pla_crop_sec(crop, x, gy(x) if callable(gy) else gy, h, w, k, i, beyond)
    return sh


def _pla_ring(rr):
    """A ring from a ring or an (x0, y0, x1, y1) rectangle (page mm)."""
    if len(rr) == 4 and not isinstance(rr[0], (tuple, list)):
        x0, y0, x1, y1 = rr
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return list(rr)


def pla_crop_plan(crop, ring_or_rect, k, row_spacing=None, plant_spacing=None, ang_deg=0.0, crown_m=None,
                  field=True):
    """A field or orchard block in plan: rows at row_spacing (m) at ang_deg; with plant_spacing, single plants along
    each row (true crown with crown_m or for olive, else a fixed 0.25 mm dot). Sourced defaults only for olive."""
    import math as _m
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    ring = _pla_ring(ring_or_rect)
    rs = row_spacing or PLA_CROPS[crop]["row_m"]
    ps = plant_spacing or PLA_CROPS[crop]["plant_m"]
    if rs is None:
        raise ValueError("plants: %s row spacing is not sourced: pass row_spacing (m)" % crop)
    sh = [("poly", ring, PLA_FIELD, None, 0.1)] if field else []
    w = crown_m or (PLA_CROPS["olive"]["plant_m"] if crop == "olive" else None)   # olive: crown = in-row spacing
    for i, (p, q) in enumerate(sec_hatch(ring, rs * k, ang_deg)):
        if ps is None:
            sh.append(("line", [p, q], PLA_ROW, 0.15))
            continue
        L = _m.hypot(q[0] - p[0], q[1] - p[1])
        if L < 1e-6:
            continue
        ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
        n = int(L / (ps * k) + 1e-9)
        s0 = (L - n * ps * k) / 2.0
        for j in range(n + 1):
            px, py = p[0] + ux * (s0 + j * ps * k), p[1] + uy * (s0 + j * ps * k)
            if crop == "olive":
                sh += _pla_plan("gnarled", px, py, w, k, _pla_cols(PLA_SPECIES["olive"], False), i * 31 + j)
            elif w:
                sh.append(("poly", _pla_crown(px, py, w / 2.0 * k, w / 2.0 * k, w / 2.0 * k, i * 31 + j, 0.12),
                           SEC["grass"], SEC["ink2"], 0.05))
            else:
                sh.append(("poly", sec_ellipse(px, py, 0.125, 0.125, 8), PLA_ROW, None, 0.1))
    return sh


def _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y):
    """A lined, off-line cell in section: walls with a raised kerb, liner closing floor and walls (RESULT §A D2:
    liner on floor and walls, kerb above the rim: our inference there), optional gravel media and water.
    Returns (shapes, planting y)."""
    if kerb_h_m is None:
        raise ValueError("plants: kerb_h_m is required (kerb height not sourced)")
    t, top = kerb_t_m * k, rim_y + kerb_h_m * k
    sh = []
    for a, b in ((x0 - t, x0), (x1, x1 + t)):
        sh += sct_hatch_fill([(a, bed_y), (a, top), (b, top), (b, bed_y)], "concrete", k, SCT["cut"], 0.25)
    sh += sct_hatch_fill([(x0 - t, bed_y - t), (x1 + t, bed_y - t), (x1 + t, bed_y), (x0 - t, bed_y)], "concrete", k,
                         SCT["cut"], 0.25)
    g = bed_y
    if media_m:
        g = bed_y + media_m * k
        sh += sct_hatch_fill([(x0, bed_y), (x1, bed_y), (x1, g), (x0, g)], "gravel", k)
    if wl_y is not None and wl_y > g:
        sh += sec_water([(x0, g), (x1, g), (x1, wl_y), (x0, wl_y)])
    return sh, g


def _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m):
    top = rim_y + kerb_h_m * k
    return [("line", [(x0, top), (x0, bed_y), (x1, bed_y), (x1, top)], SEC["ink"], 0.4)]


def pla_reed_basin(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, step_m=None):
    """Common reed in a lined, root-contained, off-line basin (D2 a) in section: inside x0-x1, floor bed_y, rim rim_y
    (page mm). kerb_t_m 0.15 m and floor slab = drawing rule; stems step_m apart."""
    sp = PLA_SPECIES["reed"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h = h_m or sp["h_m"]
    st = (step_m or 1.0 / 3.0) * k              # 9 seedlings/m² (Korkusuz et al. 2004, S20) = 1/3 m apart
    c = sp["colours"]
    i, x = 0, x0 + st / 2.0
    while x < x1:
        hh = h * k * (0.8 + 0.2 * _pla_rnd(i, 5))
        lean = 0.04 * hh * (1 if i % 2 else -1)
        sh.append(("line", [(x, g), (x + lean, g + hh)], c["fill"], 0.12))
        if i % 3 == 0:                          # plume (cut before seed release in Nov, S11)
            ry = 0.2 * k + 0.2
            sh.append(("poly", sec_ellipse(x + lean, g + hh - ry, 0.06 * k + 0.1, ry, 10), c["accent"], None, 0.1))
        x += st
        i += 1
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_mint_cell(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, crown_m=None):
    """Water mint only in a lined basin cell (D6) in section, same build as pla_reed_basin; mounds side by side."""
    sp = PLA_SPECIES["mint"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h, w = h_m or sp["h_m"], crown_m or sp["crown_m"]
    n = max(1, int((x1 - x0) / (w * k)))
    for i in range(n):
        sh += _pla_sec("mound", x0 + (i + 0.5) * (x1 - x0) / n, g, h, min(w, (x1 - x0) / n / k), k,
                       sp["colours"], i)
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_cell_plan(kind, ring_or_rect, k, kerb_t_m=0.15):
    """A lined cell in plan, kind 'reed' or 'mint': wet ground, the kerb as a band kerb_t_m wide, the plants."""
    import math as _m
    if kind not in ("reed", "mint"):
        raise ValueError("pla_cell_plan: kind is 'reed' or 'mint'")
    ring = _pla_ring(ring_or_rect)
    sp = PLA_SPECIES[kind]
    sh = [("poly", ring, PLA_WET, None, 0.1)]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    if kind == "reed":                          # stems on the 1/3 m grid, never denser than 0.9 mm on the page
        d = max(0.9, k / 3.0)
        c = sp["colours"]["fill"]
        for i in range(int((max(xs) - min(xs)) / d) + 1):
            for j in range(int((max(ys) - min(ys)) / d) + 1):
                px = min(xs) + (i + 0.5 * (j % 2) + 0.25) * d
                py = min(ys) + (j + 0.5) * d
                if _sct_inside(ring, (px, py)):
                    sh.append(("line", [(px - 0.2 * d, py - 0.25 * d), (px + 0.2 * d, py + 0.25 * d)], c, 0.1))
    else:
        w = sp["crown_m"] * k
        for i in range(int((max(xs) - min(xs)) / w) + 1):
            for j in range(int((max(ys) - min(ys)) / w) + 1):
                px, py = min(xs) + (i + 0.5) * w, min(ys) + (j + 0.5) * w
                if _sct_inside(ring, (px, py)):
                    sh += _pla_plan("mound", px, py, sp["crown_m"] * 0.9, k, sp["colours"], i * 7 + j)
    sh.append(("poly", ring, None, SCT["line"], max(0.15, kerb_t_m * k)))
    return sh
# ---- high-res silhouettes (assets_2, Aras 30 Oct 2026): PhyloPic trees, crops and animals as filled vector rings,
# drawn only in the detailed (true-to-cut) sections and recoloured there with that section's own colours. The
# sketchy sections and diagrams keep their own drawing (an abstract set comes later).
# Library: Downloads/Bergama/Data/assets_hires.json (run kit Data/), built in the cloud by
# tools/assets2/build_hires.py from revision_2026-10-29/assets_2_2026-10/ (roots cut at the ground, height 1.0,
# ground / feet at y = 0, y up). Each part = one keyhole ring for the even-odd fill + its outer and hole rings for
# outlines. Uniform scale only (never stretched). No JSON on the PC -> callers fall back to their own drawing.
# The sources are listed once on the booklet's Sources page under ASSETS (Aras 30 Oct 06:20), never beside a drawing.

HR_LOG = []
_HR_LIB = {}


def hr_library():
    """the high-res library (dict key -> asset) or {} when Downloads/Bergama/Data/assets_hires.json is missing"""
    import os as _o
    import json as _j
    if "lib" in _HR_LIB:
        return _HR_LIB["lib"]
    lib = {}
    p = _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", "Data", "assets_hires.json")
    if _o.path.exists(p):
        try:
            with open(p, "r") as fh:
                lib = _j.load(fh).get("lib", {})
            HR_LOG.append(u"High-res assets: %d from %s" % (len(lib), p))
        except Exception as ex:
            HR_LOG.append(u"High-res assets: %s unreadable (%s); own drawings used" % (p, type(ex).__name__))
    else:
        HR_LOG.append(u"High-res assets: Data/assets_hires.json not found; own drawings used")
    _HR_LIB["lib"] = lib
    return lib


def _hr_draw(a, T, fill, edge, lw):
    out = []
    for part in a.get("parts", []):
        out.append(("poly", [T(q) for q in part["fill"]], fill, None, 0.0))   # lw 0.0 marks a high-res fill
        if edge:
            for r in part["lines"]:
                pts = [T(q) for q in r]
                out.append(("line", pts + [pts[0]], edge, lw))
    return out


def hr_side(key, x, gy, k, h_m, w_m=None, fill="000000", edge=None, lw=0.08, facing=1):
    """house shapes of one high-res plant: ground at (x, gy) page mm, h_m tall (m), k page mm per m; when w_m is given
    and the silhouette would be wider, the whole drawing is scaled down until it is w_m wide (uniform). facing -1 =
    mirrored. None when the library or the key is missing."""
    a = hr_library().get(key) if key else None
    if not a or not h_m:
        return None
    s = h_m * k
    wd = float(a["x1"] - a["x0"])
    if w_m and wd * h_m > w_m:
        s = w_m / wd * k
    f = -1.0 if facing < 0 else 1.0
    return _hr_draw(a, lambda q: (x + f * q[0] * s, gy + q[1] * s), fill, edge, lw)


def hr_fauna(key, x, y, size, fill="000000", edge=None, lw=0.05, facing=1, foot=None):
    """house shapes of one high-res animal in a size-mm square centred on (x, y), head to the left (facing -1: to the
    right, PhyloPic draws most animals facing left; the library's face tells which way each one looks); with foot
    the feet sit foot x size below y (the pictograms' ground rule), otherwise the animal is centred. None when
    missing."""
    a = hr_library().get(key) if key else None
    if not a:
        return None
    wd = float(a["x1"] - a["x0"])
    s = size / max(wd, 1.0)
    cx = (a["x0"] + a["x1"]) / 2.0
    f = (-1.0 if facing < 0 else 1.0) * (-1.0 if a.get("face", 1) < 0 else 1.0)
    y0 = y - foot * size if foot is not None else y - s / 2.0
    return _hr_draw(a, lambda q: (x + f * (q[0] - cx) * s, y0 + q[1] * s), fill, edge, lw)


def hr_sources():
    """one line per asset used from the library, for the booklet's Sources page (ASSETS)"""
    out = []
    for key, a in sorted(hr_library().items()):
        out.append(u"%s silhouette, %s, PhyloPic (%s), %s" % (a.get("what", key), a.get("author", ""),
                                                              a.get("url", ""), a.get("licence", "")))
    return out

# ---- P19.2 / P15.2 (MIRAQUA round 28 Oct 2026): ONE set of architectural human figures ---------------------------
# Silhouettes at true scale (an adult 1.75 m) for every section and diagram that shows people (pp.14, 15, 19 and the
# p.15 occupancy diagram), replacing the stick figures and pictograms. Each pose is a skeleton (joints in metres,
# feet at y = 0, facing +x); fig_polys() turns it into filled outlines: a round-ended band per limb, the torso, the
# head. Draw every outline of a figure filled in one opaque colour (the section's ink or a lane colour), no stroke:
# the overlaps then read as one silhouette. Coordinates in metres; the caller scales them like the drawing.
FIG_LIMB = dict(arm=0.085, fore=0.07, thigh=0.15, shin=0.105, foot=0.07, neck=0.10)
FIG_POSES = {
    # standing, seen from the front
    "stand": dict(head=(0.0, 1.635, 0.105), torso=[(-0.2, 1.46), (0.2, 1.46), (0.17, 1.2), (0.155, 0.93), (-0.155, 0.93), (-0.17, 1.2)],
                  limbs=[("arm", (-0.185, 1.42), (-0.215, 1.13)), ("fore", (-0.215, 1.13), (-0.225, 0.84)),
                         ("arm", (0.185, 1.42), (0.215, 1.13)), ("fore", (0.215, 1.13), (0.225, 0.84)),
                         ("thigh", (-0.085, 0.95), (-0.095, 0.5)), ("shin", (-0.095, 0.5), (-0.095, 0.07)),
                         ("foot", (-0.095, 0.035), (-0.16, 0.035)),
                         ("thigh", (0.085, 0.95), (0.095, 0.5)), ("shin", (0.095, 0.5), (0.095, 0.07)),
                         ("foot", (0.095, 0.035), (0.16, 0.035)), ("neck", (0.0, 1.44), (0.0, 1.54))]),
    # walking, side view
    "walk": dict(head=(0.035, 1.635, 0.105), torso=[(-0.1, 1.45), (0.11, 1.45), (0.12, 1.2), (0.1, 0.92), (-0.12, 0.92), (-0.12, 1.2)],
                 limbs=[("thigh", (0.0, 0.95), (-0.09, 0.53)), ("shin", (-0.09, 0.53), (-0.27, 0.13)),
                        ("foot", (-0.29, 0.1), (-0.13, 0.035)),
                        ("thigh", (0.0, 0.95), (0.13, 0.52)), ("shin", (0.13, 0.52), (0.19, 0.08)),
                        ("foot", (0.15, 0.035), (0.33, 0.035)),
                        ("arm", (0.0, 1.41), (-0.1, 1.15)), ("fore", (-0.1, 1.15), (-0.17, 0.9)),
                        ("arm", (0.0, 1.41), (0.1, 1.15)), ("fore", (0.1, 1.15), (0.2, 0.92)),
                        ("neck", (0.0, 1.44), (0.02, 1.54))]),
    # standing, side view, pointing / watching forward
    "watch": dict(head=(0.03, 1.635, 0.105), torso=[(-0.11, 1.45), (0.11, 1.45), (0.12, 1.2), (0.1, 0.92), (-0.12, 0.92), (-0.12, 1.2)],
                  limbs=[("thigh", (0.0, 0.95), (0.02, 0.5)), ("shin", (0.02, 0.5), (0.0, 0.08)),
                         ("foot", (-0.03, 0.035), (0.16, 0.035)),
                         ("thigh", (-0.02, 0.95), (-0.06, 0.5)), ("shin", (-0.06, 0.5), (-0.08, 0.08)),
                         ("foot", (-0.11, 0.035), (0.08, 0.035)),
                         ("arm", (0.0, 1.41), (0.02, 1.13)), ("fore", (0.02, 1.13), (0.05, 0.86)),
                         ("arm", (0.02, 1.41), (0.22, 1.42)), ("fore", (0.22, 1.42), (0.45, 1.5)),
                         ("neck", (0.0, 1.44), (0.02, 1.54))]),
    # sitting on a step or bench (seat at 0.45 m under the hip), side view
    "sit": dict(head=(0.03, 1.215, 0.105), torso=[(-0.1, 1.03), (0.11, 1.03), (0.12, 0.8), (0.11, 0.48), (-0.12, 0.48), (-0.12, 0.8)],
                limbs=[("thigh", (0.0, 0.52), (0.44, 0.52)), ("shin", (0.44, 0.52), (0.47, 0.08)),
                       ("foot", (0.44, 0.035), (0.62, 0.035)),
                       ("arm", (0.0, 0.99), (0.08, 0.74)), ("fore", (0.08, 0.74), (0.3, 0.62)),
                       ("neck", (0.0, 1.02), (0.02, 1.12))]),
    # crouching at the edge, a hand down to the water, side view
    "touch": dict(head=(0.36, 1.0, 0.105), torso=[(0.12, 0.98), (0.3, 0.9), (0.24, 0.66), (0.02, 0.42), (-0.12, 0.5), (-0.02, 0.8)],
                  limbs=[("thigh", (-0.04, 0.47), (0.24, 0.5)), ("shin", (0.24, 0.5), (0.14, 0.08)),
                         ("foot", (0.1, 0.035), (0.29, 0.035)),
                         ("arm", (0.2, 0.9), (0.36, 0.64)), ("fore", (0.36, 0.64), (0.48, 0.3)),
                         ("neck", (0.22, 0.92), (0.3, 0.96))]),
    # wading: short steps, arms out for balance, side view
    "wade": dict(head=(0.03, 1.635, 0.105), torso=[(-0.11, 1.45), (0.11, 1.45), (0.12, 1.2), (0.1, 0.92), (-0.12, 0.92), (-0.12, 1.2)],
                 limbs=[("thigh", (0.0, 0.95), (0.07, 0.51)), ("shin", (0.07, 0.51), (0.1, 0.08)),
                        ("foot", (0.06, 0.035), (0.24, 0.035)),
                        ("thigh", (0.0, 0.95), (-0.05, 0.51)), ("shin", (-0.05, 0.51), (-0.12, 0.09)),
                        ("foot", (-0.15, 0.04), (0.02, 0.035)),
                        ("arm", (0.0, 1.41), (0.15, 1.2)), ("fore", (0.15, 1.2), (0.32, 1.12)),
                        ("arm", (0.0, 1.41), (-0.15, 1.2)), ("fore", (-0.15, 1.2), (-0.3, 1.1)),
                        ("neck", (0.0, 1.44), (0.02, 1.54))]),
    # cycling (bike way), side view; wheels as rings
    "bike": dict(head=(0.3, 1.56, 0.105), torso=[(0.05, 1.42), (0.23, 1.46), (0.18, 1.2), (-0.12, 0.95), (-0.26, 1.02), (-0.08, 1.28)],
                 limbs=[("thigh", (-0.2, 0.98), (0.12, 0.8)), ("shin", (0.12, 0.8), (0.02, 0.38)),
                        ("foot", (-0.02, 0.36), (0.12, 0.36)),
                        ("arm", (0.15, 1.42), (0.3, 1.2)), ("fore", (0.3, 1.2), (0.45, 1.06)),
                        ("neck", (0.18, 1.44), (0.26, 1.5)),
                        ("frame", (-0.55, 0.34), (-0.2, 0.9)), ("frame", (-0.2, 0.9), (0.0, 0.34)),
                        ("frame", (0.0, 0.34), (-0.55, 0.34)), ("frame", (-0.2, 0.9), (0.42, 0.92)),
                        ("frame", (0.0, 0.34), (0.42, 0.92)), ("frame", (0.42, 0.92), (0.55, 0.34)),
                        ("frame", (0.42, 0.92), (0.46, 1.06))],
                 rings=[(-0.55, 0.34, 0.34), (0.55, 0.34, 0.34)]),
}
FIG_ORDER = ("stand", "walk", "watch", "sit", "touch", "wade", "bike")


def _fig_band(p, q, w, n=5):
    """the outline of a band of width w from p to q with round ends"""
    import math as _m
    dx, dy = q[0] - p[0], q[1] - p[1]
    a = _m.atan2(dy, dx)
    r = w / 2.0
    out = []
    for c, a0 in ((q, a - _m.pi / 2), (p, a + _m.pi / 2)):
        for i in range(n + 1):
            t = a0 + _m.pi * i / n
            out.append((c[0] + r * _m.cos(t), c[1] + r * _m.sin(t)))
    return out


def _fig_circle(cx, cy, r, n=16):
    import math as _m
    return [(cx + r * _m.cos(2 * _m.pi * i / n), cy + r * _m.sin(2 * _m.pi * i / n)) for i in range(n)]


def fig_polys(pose, height=1.75, facing=1):
    """filled outlines of one figure, in metres, feet at (0, 0): pose = a FIG_POSES key; height 1.75 = adult (a child
    about 1.15, the head kept a little larger); facing -1 = mirrored (looking left)"""
    P = FIG_POSES[pose]
    k = height / 1.75
    hk = k ** 0.7 / k if k < 1.0 else 1.0               # a child's head is relatively larger
    f = 1.0 if facing >= 0 else -1.0

    def T(pt):
        return (f * pt[0] * k, pt[1] * k)
    out = [[T(p) for p in P["torso"]]]
    for kind, p, q in P["limbs"]:
        w = FIG_LIMB.get(kind, 0.035)
        out.append(_fig_band(T(p), T(q), w * k))
    for cx, cy, r in P.get("rings", ()):
        ring = _fig_circle(cx, cy, r, 20)
        for i in range(len(ring)):
            out.append(_fig_band(T(ring[i]), T(ring[(i + 1) % len(ring)]), 0.035 * k, 2))
    hx, hy, hr = P["head"]
    out.append(_fig_circle(f * hx * k, hy * k, hr * k * hk))
    return out


# ---- A1 scale figures (29 Oct 2026, Aras: family A1 "gestural pen", the R20 language) --------------------------------
# ONE figure API for every drawing: fig_side / fig_top / fig_meta. Shapes are house shapes ("poly", ring, fill, stroke,
# lw) in the caller's units (k units per metre, y up), feet at (x, y). Two sources:
#  1. the curated A1 library (24 figures of the R20 sheet and Studio Articulation Sketchy Human Figures 2 + 3) read
#     from Downloads/Bergama/Data/figures_A1.json. Licences forbid redistributing those drawings, so they are NOT in
#     this public repo; the file ships in the run kit's Data/ folder (project library/figures_A1/).
#  2. figures drawn here in the same pen language for the poses the sets lack (wade, sit_step, bike, adult_child,
#     stall, railing, olive, touch, and every plan view). Each one is posed by its contact: the step, rail, counter,
#     water or branch it touches is a parameter, and the limbs are solved to reach it.
# Adult 1.70 m. Body proportions = Drillis & Contini (1966) segment ratios of stature (as reproduced in Winter,
# Biomechanics and Motor Control of Human Movement, Fig. 4.1; page not re-checked): FIG_DC below.
# No library file -> the drawn figures stand in for stand/walk/watch/lean/sit_chair (never nothing).
FIG_A1_H = 1.70
FIG_A1_INK = "2B2B2B"
FIG_A1_PEN = 0.019              # m: pen width = the median stroke of the curated library at 1.70 m
FIG_PEN_MIN_MM = 0.10           # page mm: no figure line prints thinner (small scales get an outline)
FIG_DC = dict(chin=0.870, shoulder=0.818, elbow=0.630, wrist=0.485, hip=0.530, knee=0.285, ankle=0.039,
              upper_arm=0.186, forearm=0.146, hand=0.108, thigh=0.245, shank=0.246, foot=0.152,
              shoulder_w=0.259, hip_w=0.191)
FIG_CHILD_H = 1.15              # m, the project's child figure (fig_polys docstring)
FIG_BIKE = dict(wheel_r=0.336,  # 622 mm rim (ISO 5775 "700C") + 2 x 25 mm tyre = 672 mm: calculated
                wheelbase=1.00, crank=0.17, bb_h=0.27)  # drawing values (typical city bike), not sourced
FIG_LOG = []
_FIG_LIB = {}


def fig_library():
    """the curated A1 library (dict id -> figure) or {} when Downloads/Bergama/Data/figures_A1.json is missing"""
    import os as _o
    import json as _j
    if "lib" in _FIG_LIB:
        return _FIG_LIB["lib"]
    lib = {}
    root = _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", "Data")
    for p in (_o.path.join(root, "figures_A1.json"), _o.path.join(root, "figures", "figures_A1.json")):
        if _o.path.exists(p):
            try:
                with open(p, "r") as fh:
                    lib = _j.load(fh).get("figures", {})
                FIG_LOG.append(u"Figures: %d A1 figures from %s" % (len(lib), p))
                break
            except Exception as ex:
                FIG_LOG.append(u"Figures: %s unreadable (%s); drawn figures used" % (p, type(ex).__name__))
    if not lib:
        FIG_LOG.append(u"Figures: Data/figures_A1.json not found; drawn A1 figures used for every pose")
    _FIG_LIB["lib"] = lib
    return lib


def _fa_rand(seed):
    s = [int(seed * 7919 + 17) & 0x7fffffff]

    def r():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7fffffff
        return s[0] / float(0x7fffffff) - 0.5
    return r


def _fa_smooth(P, n=2):
    for _ in range(n):
        if len(P) < 3:
            return P
        Q = [P[0]]
        for a, b in zip(P[:-1], P[1:]):
            Q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        Q.append(P[-1])
        P = Q
    return P


def _fa_stroke(P, rnd, w=FIG_A1_PEN, over=0.06, wob=0.008, smooth=True):
    """one pen stroke through P (m) as a closed ring: a little overshoot at both ends, a slight wobble, the width
    tapering to a third at the ends (the expanded-brush look of the A1 sets)"""
    import math as _m
    P = [(p[0] + wob * rnd(), p[1] + wob * rnd()) for p in P]
    if len(P) >= 2:
        for i0, i1 in ((0, 1), (-1, -2)):
            a, b = P[i0], P[i1]
            d = _m.hypot(a[0] - b[0], a[1] - b[1]) or 1.0
            e = over * (0.6 + rnd())
            P[i0] = (a[0] + (a[0] - b[0]) * e, a[1] + (a[1] - b[1]) * e)     # overshoot = e x the end segment
    if smooth:
        P = _fa_smooth(P)
    n = len(P)
    if n < 2:
        return None
    L, R = [], []
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = _m.hypot(dx, dy) or 1.0
        t = i / float(n - 1)
        h = 0.5 * w * (0.33 + 0.67 * _m.sin(_m.pi * t) ** 0.5)
        L.append((P[i][0] - dy / d * h, P[i][1] + dx / d * h))
        R.append((P[i][0] + dy / d * h, P[i][1] - dx / d * h))
    return L + R[::-1]


def _fa_oval(cx, cy, rx, ry, rnd, gap=0.9, a0=1.9, w=FIG_A1_PEN):
    """an open pen oval (head, wheel): starts at a0 rad, stops gap rad short of closing"""
    import math as _m
    n = 16
    P = [(cx + rx * _m.cos(a0 + (2 * _m.pi - gap) * i / n), cy + ry * _m.sin(a0 + (2 * _m.pi - gap) * i / n))
         for i in range(n + 1)]
    return _fa_stroke(P, rnd, w, over=0.02, wob=0.004, smooth=False)


def _fa_ik(a, b, l1, l2, bend):
    """2-link reach from a to b (segment lengths l1, l2): the middle joint, bent to the side bend (+1 left of a->b);
    out of reach -> straight towards b"""
    import math as _m
    dx, dy = b[0] - a[0], b[1] - a[1]
    d = _m.hypot(dx, dy) or 1e-9
    if d >= l1 + l2:
        return (a[0] + dx / d * l1, a[1] + dy / d * l1), (a[0] + dx / d * (l1 + l2), a[1] + dy / d * (l1 + l2))
    c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    t = _m.acos(max(-1.0, min(1.0, c)))
    a0 = _m.atan2(dy, dx) + bend * t
    return (a[0] + l1 * _m.cos(a0), a[1] + l1 * _m.sin(a0)), b


class _FaBody(object):
    """a side-view body facing +x, h tall: joints from FIG_DC; hip/shoulder positions set by the pose"""

    def __init__(self, h=FIG_A1_H, hip=None, lean=0.0):
        import math as _m
        self.h, D = h, FIG_DC
        self.L = dict((k, v * h) for k, v in D.items())
        self.hip = hip or (0.0, D["hip"] * h)
        t = (D["shoulder"] - D["hip"]) * h
        self.sho = (self.hip[0] + t * _m.sin(lean), self.hip[1] + t * _m.cos(lean))
        self.lean = lean
        hh = (1.0 - D["shoulder"]) * h
        self.hr = (0.040 * h, 0.060 * h)      # the A1 head: a small upright oval; its top at stature when upright
        self.head = (self.sho[0] + 0.45 * hh * _m.sin(lean) + 0.02 * h,
                     self.sho[1] + (hh - self.hr[1]) * _m.cos(lean))

    def leg(self, ankle, bend=1):
        return _fa_ik(self.hip, ankle, self.L["thigh"], self.L["shank"], bend)

    def arm(self, hand, bend=-1, s=None):
        return _fa_ik(s or self.sho, hand, self.L["upper_arm"], self.L["forearm"] + 0.3 * self.L["hand"], bend)


def _fa_clip(P, cut_y):
    """the part of polyline P above cut_y (from its first point down)"""
    if cut_y is None:
        return P
    Q = []
    for a, b in zip(P[:-1], P[1:]):
        if a[1] < cut_y:
            break
        Q.append(a)
        if b[1] < cut_y:
            t = (a[1] - cut_y) / (a[1] - b[1])
            Q.append((a[0] + t * (b[0] - a[0]), cut_y))
            return Q
    else:
        Q.append(P[-1])
    return Q


def _fa_off(P, d):
    """P offset sideways by d (left of its direction), point by point"""
    import math as _m
    out = []
    for i in range(len(P)):
        a, b = P[max(0, i - 1)], P[min(len(P) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = _m.hypot(dx, dy) or 1.0
        dd = d[i] if isinstance(d, (list, tuple)) else d
        out.append((P[i][0] - dy / n * dd, P[i][1] + dx / n * dd))
    return out


def _fa_draw(B, legs, arms, rnd, w=FIG_A1_PEN, hatch=True, hem=None, coat=0.0, cut_y=None):
    """pen strokes of one body in the R20 manner: small open head oval; the coat as two contour strokes falling from
    the neck over round shoulders to the hem, a hem/belt stroke overshooting both sides; each leg as two contour
    strokes tapering to the ankle with a short foot tick; arms as single strokes; one-sided diagonal hatch on the
    back. legs/arms: [(knee, ankle)], [(elbow, hand)]. cut_y: nothing below it (water)."""
    import math as _m
    out = []
    hx, hy = B.head
    out.append(_fa_oval(hx, hy, B.hr[0], B.hr[1], rnd, w=w))
    s, p = B.sho, B.hip
    c, sn = _m.cos(B.lean), _m.sin(B.lean)
    dep = 0.095 * B.h                                   # half chest depth, side view
    hem_y = hem if hem is not None else p[1] - coat
    neck = (s[0] - 0.02 * sn + 0.01, s[1] + 0.035 * B.h * c)

    def T(u, v):                                        # torso frame: u across (+ = front), v up from the hip
        return (p[0] + u * c + v * sn, p[1] - u * sn + v * c)
    tl = (s[1] - p[1]) / max(c, 0.3)
    hv = (hem_y - p[1]) / max(c, 0.3)
    back = [neck, T(-0.75 * dep, tl - 0.01), T(-1.0 * dep, tl - 0.10), T(-0.95 * dep, 0.45 * tl), T(-0.92 * dep, hv)]
    front = [(neck[0] + 0.03, neck[1] - 0.01), T(0.70 * dep, tl - 0.03), T(0.95 * dep, tl - 0.16), T(0.80 * dep, 0.45 * tl),
             T(0.90 * dep, hv)]
    out += [_fa_stroke(back, rnd, w), _fa_stroke(front, rnd, w * 0.85)]
    out.append(_fa_stroke([T(-1.15 * dep, hv + 0.01), T(1.20 * dep, hv - 0.005)], rnd, w * 0.9, over=0.12))
    if hatch:
        for i in range(5):
            v = tl - 0.12 - (tl - 0.12 - hv) * (0.12 + 0.17 * i)
            a0 = T(-0.88 * dep, v)
            out.append(_fa_stroke([a0, (a0[0] + 0.08, a0[1] + 0.12)], rnd, w * 0.6, over=0.0, wob=0.003, smooth=False))
    for e, hnd in arms:
        out.append(_fa_stroke([(s[0] + 0.01, s[1] - 0.03), e, hnd], rnd, w))
    lw0 = 0.055 * B.h                                   # half leg width at the hip
    for i, (kn, an) in enumerate(legs):
        P = [p, kn, an]
        for side in ((1, -1) if i == 0 else (-1,)):     # the far leg: its back contour only
            Q = _fa_off(P, [side * lw0, side * 0.6 * lw0, side * 0.12 * lw0])
            Q = _fa_clip(Q, cut_y)
            if len(Q) >= 2:
                out.append(_fa_stroke(Q, rnd, w * (1.0 if side > 0 else 0.85)))
        if cut_y is None or an[1] > cut_y:
            out.append(_fa_stroke([(an[0] - 0.02, an[1] - B.L["ankle"] * 0.6), (an[0] + 0.6 * B.L["foot"], an[1] - B.L["ankle"])],
                                  rnd, w, over=0.1, smooth=False))
    return [r for r in out if r]


def _fa_side(pose, seed=0, **p):
    """(rings in m, feet at (0, 0), facing +x; anchors) of a drawn pose"""
    import math as _m
    rnd = _fa_rand(seed + 3)
    H = p.get("h_m", FIG_A1_H)
    D = FIG_DC
    an = {}
    if pose in ("stand", "watch", "walk", "wade"):
        st = 0.0 if pose in ("stand", "watch") else 0.32 * H * (0.7 if pose == "wade" else 1.0)
        B = _FaBody(H, lean=0.03 if pose == "walk" else 0.0)
        A = D["ankle"] * H
        legs = [B.leg((0.5 * st, A)), B.leg((-0.5 * st, A))]
        w_ = D["wrist"] * H
        if pose == "watch":
            arms = [B.arm((0.05, w_)), B.arm((0.42 * H * 0.6, D["shoulder"] * H + 0.02))]
        elif pose == "wade":
            arms = [B.arm((0.20, w_ + 0.10)), B.arm((-0.12, w_ + 0.08))]
        else:
            arms = [B.arm((0.18 * st, w_)), B.arm((-0.25 * st, w_))]
        cut = None
        if pose == "wade":
            cut = p.get("depth_m", D["knee"] * H)
            an["water_y"] = cut
        R = _fa_draw(B, legs, arms, rnd, coat=0.05, cut_y=cut)
        if cut is not None:                         # the water closing round the legs: two short ripple strokes
            for lx_ in (-0.5 * st, 0.5 * st):
                R.append(_fa_stroke([(lx_ - 0.14, cut), (lx_ + 0.16, cut)], rnd, FIG_A1_PEN * 0.7, over=0.1))
        return R, an
    if pose == "sit_step":
        seat = p.get("seat_h", 0.45)                # step riser the figure sits on (m above the tread the feet rest on)
        hip = (0.0, seat + 0.09)                    # hip joint about 9 cm above the seat (drawing value)
        B = _FaBody(H, hip=hip, lean=0.10)
        A = D["ankle"] * H
        kn, ank = B.leg((0.40 * H * 0.62, A), bend=1)
        legs = [(kn, ank), B.leg((0.36 * H * 0.62, A), bend=1)]
        arms = [B.arm((kn[0] - 0.04, kn[1] - 0.02)), B.arm((kn[0] - 0.10, kn[1] - 0.06))]
        R = _fa_draw(B, legs, arms, rnd, hem=seat + 0.02)
        an.update(seat_x=0.15, seat_y=seat)         # the step nosing: under the thighs, in front of the hip
        return R, an
    if pose == "touch":                             # crouching at the edge, one hand down to the water
        A = D["ankle"] * H
        hip = (-0.12, 0.30 * H * 0.75)
        B = _FaBody(H, hip=hip, lean=0.85)
        legs = [B.leg((0.12, A), bend=1), B.leg((0.02, A), bend=1)]
        reach = p.get("reach_y", -0.10)             # hand height (m; below the feet = over the edge)
        arms = [B.arm((B.sho[0] + 0.25, reach), bend=1), B.arm((hip[0] + 0.30, hip[1] + 0.05))]
        an["hand"] = arms[0][1]
        return _fa_draw(B, legs, arms, rnd, hatch=False, coat=0.0), an
    if pose in ("stall", "railing", "olive"):
        A = D["ankle"] * H
        if pose == "railing":
            rh = p.get("rail_h", 1.10)
            sh_y = rh + D["upper_arm"] * H * 0.92     # forearms flat on the rail, upper arm nearly vertical
            t = (D["shoulder"] - D["hip"]) * H
            lean = _m.acos(max(0.4, min(1.0, (sh_y - D["hip"] * H) / t)))
            B = _FaBody(H, lean=lean)
            el = (B.sho[0] + 0.05, rh + 0.02)
            hand = (el[0] + D["forearm"] * H + 0.04, rh + 0.03)
            arms = [(el, hand), ((el[0] - 0.03, el[1] - 0.01), (hand[0] - 0.05, hand[1] - 0.01))]
            legs = [B.leg((-0.04, A)), B.leg((-0.16, A))]
            an.update(rail_x=el[0] + 0.12, rail_y=rh)
            return _fa_draw(B, legs, arms, rnd, coat=0.04), an
        if pose == "stall":
            ch = p.get("counter_h", 0.90)
            B = _FaBody(H, lean=0.12)
            arms = [B.arm((B.sho[0] + 0.48, ch + 0.06), bend=-1), B.arm((-0.02, D["wrist"] * H))]
            legs = [B.leg((0.06, A)), B.leg((-0.12, A))]
            an.update(counter_x=0.30, counter_y=ch)
            R = _fa_draw(B, legs, arms, rnd, coat=0.06)
            bx, by = arms[1][1]                     # a market bag in the other hand
            R.append(_fa_stroke([(bx - 0.10, by), (bx - 0.12, by - 0.30), (bx + 0.12, by - 0.31), (bx + 0.10, by)], rnd,
                                FIG_A1_PEN * 0.8, over=0.05))
            return R, an
        bh = p.get("branch_h", 1.90)                # olive picking: both hands up to the branch (top reach ~1.92 m)
        B = _FaBody(H, lean=-0.06)
        rl = (D["upper_arm"] + D["forearm"] + 0.3 * D["hand"]) * H
        top = B.sho[1] + (max(0.0, rl ** 2 - 0.32 ** 2)) ** 0.5
        hy = min(bh, top)
        arms = [B.arm((B.sho[0] + 0.32, hy), bend=-1), B.arm((B.sho[0] + 0.22, hy - 0.06), bend=-1)]
        legs = [B.leg((0.10, A)), B.leg((-0.14, A))]
        an.update(hand_x=arms[0][1][0], hand_y=arms[0][1][1], reached=arms[0][1][1] >= bh - 0.02)
        return _fa_draw(B, legs, arms, rnd, coat=0.04), an
    if pose == "bike":
        F = FIG_BIKE
        r, wb, cr, bb = F["wheel_r"], F["wheelbase"], F["crank"], F["bb_h"]
        rear, front, bbp = (-0.5 * wb, r), (0.5 * wb, r), (-0.05, bb)
        legl = (D["thigh"] + D["shank"]) * H
        # saddle: the leg reaches 96 % of its length to the lowest pedal (nearly straight at the bottom of the stroke)
        hip = (bbp[0] - 0.24, bb - cr + 0.04 + _m.sqrt((0.96 * legl) ** 2 - 0.24 ** 2))
        bar = (front[0] - 0.12, hip[1] + 0.06)
        B = _FaBody(H, hip=hip, lean=0.62)
        out = [_fa_oval(rear[0], rear[1], r, r, rnd, gap=0.5, a0=0.3), _fa_oval(front[0], front[1], r, r, rnd, gap=0.5, a0=3.4)]
        out += [_fa_stroke(P, rnd, FIG_A1_PEN * 0.75, over=0.04) for P in (
            [rear, bbp, (hip[0] + 0.02, hip[1] - 0.08)], [(hip[0] + 0.02, hip[1] - 0.10), (bar[0] - 0.05, bar[1] - 0.10), front],
            [bbp, (bar[0] - 0.05, bar[1] - 0.10)], [rear, (hip[0] + 0.02, hip[1] - 0.10)],
            [(hip[0] - 0.10, hip[1] - 0.04), (hip[0] + 0.10, hip[1] - 0.03)], [(bar[0] - 0.05, bar[1] - 0.10), bar])]
        ang = 0.5
        pa = (bbp[0] + cr * _m.cos(ang), bbp[1] - cr * _m.sin(ang) * 1.0)
        pb = (bbp[0] - cr * _m.cos(ang), bbp[1] + cr * _m.sin(ang))
        legs = [B.leg((pa[0] - 0.05, pa[1] + 0.04), bend=1), B.leg((pb[0] - 0.05, pb[1] + 0.04), bend=1)]
        arms = [B.arm(bar, bend=-1)]
        out += _fa_draw(B, legs, arms, rnd, hatch=False, coat=0.0)
        an.update(length=wb + 2 * r)
        return [o for o in out if o], an
    if pose == "adult_child":                       # walking hand in hand: the hands meet where both reach
        ch = p.get("child_h", FIG_CHILD_H)
        A = FIG_DC["ankle"]
        Ba = _FaBody(H, lean=0.03)
        st = 0.30 * H
        hand = (0.20, D["wrist"] * H + 0.06)
        legs = [Ba.leg((0.5 * st, A * H)), Ba.leg((-0.5 * st, A * H))]
        R = _fa_draw(Ba, legs, [Ba.arm(hand, bend=-1), Ba.arm((-0.12, D["wrist"] * H))], rnd, coat=0.05)
        Bc = _FaBody(ch, hip=(0.42, D["hip"] * ch), lean=0.02)
        stc = 0.30 * ch
        legs = [Bc.leg((0.42 + 0.5 * stc, A * ch)), Bc.leg((0.42 - 0.5 * stc, A * ch))]
        R += _fa_draw(Bc, legs, [Bc.arm(hand, bend=1), Bc.arm((0.46, D["wrist"] * ch))], _fa_rand(seed + 11),
                      w=FIG_A1_PEN * 0.85, hatch=False, coat=0.03)
        an.update(hand=hand, child_h=ch)
        return R, an
    return None, an


def _fa_top(pose, seed=0, **p):
    """plan figures, m, centred on (0, 0), heading +x: open shoulder oval, small head oval, one-sided hatch"""
    rnd = _fa_rand(seed + 5)
    H = p.get("h_m", FIG_A1_H)
    sw, dp = FIG_DC["shoulder_w"] * H, 0.15 * H

    def one(cx, cy, s=1.0, hatch=True):
        o = [_fa_oval(cx, cy, 0.5 * dp * s, 0.5 * sw * s, rnd, gap=0.7, a0=2.4),
             _fa_oval(cx + 0.03 * s, cy, 0.07 * s, 0.065 * s, rnd, gap=1.0, a0=0.5)]
        if hatch:
            for i in range(3):
                y = cy - 0.12 * s + 0.08 * s * i
                o.append(_fa_stroke([(cx - 0.10 * s, y), (cx - 0.04 * s, y + 0.06 * s)], rnd, FIG_A1_PEN * 0.6, over=0.0, smooth=False))
        return o
    if pose in ("stand", "watch"):
        R = one(0.0, 0.0)
    elif pose == "walk":
        R = one(0.0, 0.0) + [_fa_stroke([(0.18, 0.08), (0.30, 0.09)], rnd), _fa_stroke([(-0.20, -0.08), (-0.10, -0.08)], rnd)]
    elif pose in ("sit", "sit_step", "sit_chair"):
        t = FIG_DC["thigh"] * H
        R = one(-0.05, 0.0) + [_fa_stroke([(0.02, 0.09), (0.02 + t, 0.10)], rnd), _fa_stroke([(0.02, -0.09), (0.02 + t, -0.10)], rnd)]
    elif pose == "bike":
        F = FIG_BIKE
        L = 0.5 * F["wheelbase"]
        R = one(-0.05, 0.0, hatch=False) + [_fa_stroke([(-L - F["wheel_r"], 0.0), (-L + F["wheel_r"], 0.0)], rnd, FIG_A1_PEN * 1.6),
                                            _fa_stroke([(L - F["wheel_r"], 0.0), (L + F["wheel_r"], 0.0)], rnd, FIG_A1_PEN * 1.6),
                                            _fa_stroke([(-L, 0.0), (L - 0.12, 0.0)], rnd, FIG_A1_PEN * 0.8),
                                            _fa_stroke([(L - 0.12, -0.24), (L - 0.12, 0.24)], rnd, FIG_A1_PEN * 0.8)]
    elif pose == "adult_child":
        ch = p.get("child_h", FIG_CHILD_H) / H
        R = one(0.0, 0.20) + one(0.0, -0.22, s=ch, hatch=False) + [_fa_stroke([(0.02, 0.0), (0.04, -0.06)], rnd, FIG_A1_PEN * 0.8)]
    else:
        return None
    return [r for r in R if r]


FIG_DRAWN_SIDE = ("stand", "walk", "watch", "wade", "sit_step", "touch", "stall", "railing", "olive", "bike", "adult_child")
FIG_DRAWN_TOP = ("stand", "watch", "walk", "sit", "sit_step", "sit_chair", "bike", "adult_child")
FIG_POSE_ALIAS = {"sit": "sit_step"}


def _fig_pick(pose, pick):
    lib = fig_library()
    if pose in lib:
        return lib[pose]
    ids = sorted(k for k, f in lib.items() if f.get("pose") == pose)
    return lib[ids[pick % len(ids)]] if ids else None


def fig_meta(pose, facing=1, pick=0, **p):
    """anchors of a figure in m relative to its feet (x mirrored for facing -1): wade water_y; sit_step seat_x,
    seat_y; railing rail_x, rail_y; stall counter_x, counter_y; olive hand_x, hand_y, reached; touch hand;
    adult_child hand, child_h; bike length; lean (library) ledge_y_m. Use them to place the step, rail, counter or
    water the figure touches."""
    pose = FIG_POSE_ALIAS.get(pose, pose)
    f = None if pose in ("wade", "sit_step", "touch", "stall", "railing", "olive", "bike", "adult_child") else _fig_pick(pose, pick)
    an = dict(f.get("anchor") or {}) if f else _fa_side(pose, pick, **p)[1]
    s = 1.0 if facing >= 0 else -1.0
    for k_ in list(an):
        v = an[k_]
        if k_.endswith("_x"):
            an[k_] = s * v
        elif isinstance(v, tuple):
            an[k_] = (s * v[0], v[1])
    return an


def fig_side(pose, x, y, k, facing=1, ink=None, pick=None, mm_per_m=None, pen_min_mm=FIG_PEN_MIN_MM, **p):
    """side-view figure, feet at (x, y), k units per m, facing -1 = mirrored. pose: a library id (e.g.
    "a1_group_child"), a library pose (stand, walk, watch, lean, sit_chair; pick (default: from x, y) = which one, cycling),
    or a drawn pose (wade depth_m, sit_step seat_h, touch reach_y, stall counter_h, railing rail_h, olive branch_h,
    bike, adult_child child_h = hand in hand; the library's family group is "a1_group_child"). Library figures face as drawn (their "facing" in the file); facing flips them so they
    look the asked way. mm_per_m: printed page mm per metre (default k, the house convention); where the pen
    (0.019 m) would print thinner than pen_min_mm, every stroke gets an outline of the difference (lw in page mm).
    Returns house shapes ("poly", ring, ink, stroke, lw)."""
    pose = FIG_POSE_ALIAS.get(pose, pose)
    ink = ink or FIG_A1_INK
    if pick is None:                                   # variety: the place picks the figure, the same every run
        pick = int(abs(x * 7.31 + y * 3.17) * 10.0) % 997
    rings, flip = None, 1.0 if facing >= 0 else -1.0
    drawn_only = ("wade", "sit_step", "touch", "stall", "railing", "olive", "bike", "adult_child")
    if pose not in drawn_only:
        f = _fig_pick(pose, pick)
        if f:
            rings = f["rings"]
            if f.get("facing", 0) < 0:
                flip = -flip
    if rings is None:
        rings = _fa_side(pose if pose in FIG_DRAWN_SIDE else ("watch" if pose == "lean" else "stand"), pick, **p)[0]
    if not rings:                                      # never nothing: the legacy silhouette
        rings = fig_polys(pose if pose in FIG_POSES else "stand", FIG_A1_H, 1)
    add = max(0.0, pen_min_mm - FIG_A1_PEN * (mm_per_m or k))
    return [("poly", [(x + flip * px * k, y + py * k) for px, py in r], ink, ink if add > 0 else None, add)
            for r in rings]


def fig_top(pose, x, y, k, ang=0.0, ink=None, pick=0, mm_per_m=None, pen_min_mm=FIG_PEN_MIN_MM, **p):
    """plan figure centred on (x, y), heading ang (radians, 0 = +x), k units per m: stand, watch, walk, sit,
    sit_step, sit_chair, bike, adult_child (child_h). Same pen and mm_per_m rule as fig_side."""
    import math as _m
    ink = ink or FIG_A1_INK
    rings = _fa_top(FIG_POSE_ALIAS.get(pose, pose), pick, **p) or _fa_top("stand", pick)
    ca, sa = _m.cos(ang), _m.sin(ang)
    add = max(0.0, pen_min_mm - FIG_A1_PEN * (mm_per_m or k))
    return [("poly", [(x + (px * ca - py * sa) * k, y + (px * sa + py * ca) * k) for px, py in r], ink,
             ink if add > 0 else None, add) for r in rings]

# ---- Shared basemap (revision 29 Oct 2026, brief 02 §1, WO-T2a-1) -------------------------------------------------
# ONE base for every map of the booklet (site board, water board, city link, masterplan, agriculture): the same
# stream, streets, buildings, green, tree cover, fields and contours, switched on and off per page by its MODE, with a
# per-drawing override (D5: Zones a, Feeling b stream only, Sound b stream + main roads, Smell b stream only ...).
#
# WHERE THE DATA COMES FROM (decided 29 Oct, T2a): not from the open Rhino file. The site board already builds the
# whole site model once (survey of Bergama_Altlik.3dm + OpenStreetMap + WorldCover, cached); it calls
# basemap_export(S) once a run and writes Downloads/Bergama/cached/basemap/basemap.json. Every other script reads that
# file with basemap_load(). Inside the analysis frame (site_alan) the layers are the site board's own (survey quality,
# exactly as p.06 draws them); between the frame and the wider EXTENT they are OpenStreetMap's (Data/bergama_osm.osm),
# so p.21 reaches the Asklepion, the Akropol, the cable car and the museum, and p.16's frames can widen. Scripts that
# run before the site board in the chain (zone base, masterplan, water balance) read the file of the last run; before
# the very first site board run there is no file: basemap_load() returns None, logs it, and every draw call draws
# nothing (the caller's own drawing goes on).
#
# GEOMETRY: survey metres everywhere. Line widths and marker sizes are PRINT mm on the booklet page, so a call needs
# the drawing's scale denominator only where a size in mm becomes metres (cut-line markers). Colours: hex 'RRGGBB'.
# A draw call returns ITEMS, bottom first; the caller turns them into its own page calls (basemap_draw does that
# through two or three small functions the caller gives). Items:
#   ("fill", rings, hex, alpha, nonzero)        rings = [[(x, y), ...], ...] (outlines and their holes)
#   ("line", pts, hex, width_mm, dash_mm, alpha) dash_mm = None or [on, off, ...] in print mm
#   ("text", s, (x, y), size_mm, hex, bold, align)   align as the scripts' text calls ("MC" = middle centre)
import os as _bm_os
import json as _bm_json
import math as _bm_math

BASEMAP_FILE = _bm_os.path.join(_bm_os.path.expanduser("~"), "Downloads", "Bergama", "cached", "basemap",
                                "basemap.json")
BASEMAP_FORMAT = 1
BASEMAP_MARGIN = 250.0           # m: the extent reaches this far beyond the farthest REACH place
# the places the extent must hold (survey m; the heritage loop's positions, selinus_board parts/15j_r28_heritage.py)
BASEMAP_REACH = ((u"Asklepion", (29077.3, 31867.3)),          # OSM ticket building
                 (u"Akropol", (30209.0, 33177.0)),            # Trajaneum, OSM way 1410335587
                 (u"Teleferik", (30720.4, 32370.1)),          # valley station, OSM node 2295928011
                 (u"Bergama Müzesi", (29560.0, 31358.0)))

# tones: the p.06 stream edge plan's (selinus_board MPL, R28E_*) so the detailed mode is p.06's base
BM_COL = dict(bld="A7A299", bld_osm_edge="736A62", her="E4CAC9", her_edge="AF7474", water="91ADB4",
              water_edge="5D7F8D", tree="C4CCB5", park="DFEBC0", grass="DFEBC0", field="C6C08D", road="CFCCC5",
              road_edge="847E75", ink="2C2219", contour="BDB7B0", cut="2C2219")
BM_FAINT = dict(bld="D3D0CB", bld_veryfaint="E9E7E3", road="E2E0DB", road_line="B9B4AC")
# topographic mode: contours coloured by height, very faint (palette references 5C7A86 -> 89986A -> 70754C -> 4C2528,
# each mixed 55 % towards white; low = blue-grey, high = dark brown)
BM_HEIGHT_RAMP = ("ADBCC2", "C4CAB1", "B7B9A2", "A39092")
BM_LW = dict(contour=(0.07, 0.13), contour_topo=(0.08, 0.14), water_edge=0.18, covered=0.30, bridge=0.30,
             road_edge=0.12, osm_edge=0.08, her_edge=0.12, main=0.45, lane=0.22, path=0.10, river_osm=0.6,
             stream_osm=0.35, cut=0.35)
BM_COVERED_DASH = (1.6, 0.9)     # mm: the covered course

# the modes of 02 §1; a value per layer: False = off, True = on, "faint" / "veryfaint" = buildings or streets faint,
# a tuple of street classes ("main", "lane", "path") = only those as centrelines, "height" = contours by height
BASEMAP_MODES = {
    "detailed": dict(stream=True, streets=True, buildings=True, green=True, trees=True, fields=True, contours=True),
    "simple": dict(stream=True, streets="faint", buildings="faint", green=False, trees=False, fields=False,
                   contours=False),
    "minimal": dict(stream=True, streets=("main", "lane"), buildings="veryfaint", green=False, trees=False,
                    fields=False, contours=False),
    "topographic": dict(stream=True, streets=False, buildings="faint", green=False, trees=False, fields=False,
                        contours="height"),
}
_BM_MEMO = {}


# ------------------------------------------------------------------------------------------- reading
def basemap_load(path=None, log=None):
    """the basemap data (dict) written by the site board's basemap_export, read once a run; None when the file is
    missing or of another format (a line goes to log, a list, when given)"""
    p = path or BASEMAP_FILE
    if p in _BM_MEMO:
        return _BM_MEMO[p]
    d = None
    try:
        with open(p, "r", encoding="utf-8") as fh:
            d = _bm_json.load(fh)
        if not isinstance(d, dict) or d.get("format") != BASEMAP_FORMAT:
            if log is not None:
                log.append(u"WARNING: {} is of another format: the shared basemap is left out (run the site board "
                           u"once).".format(p))
            d = None
        elif log is not None:
            log.append(u"Shared basemap: {} ({}).".format(p, d.get("source", "")))
    except Exception as ex:
        if log is not None:
            log.append(u"WARNING: the shared basemap {} could not be read ({}): maps are drawn without it until the "
                       u"site board has run once.".format(p, type(ex).__name__))
    _BM_MEMO[p] = d
    return d


def basemap_frame(D=None):
    """the analysis frame (site_alan) as four survey corners, upstream end first, from the data; None without data"""
    D = D if D is not None else basemap_load()
    return [tuple(p) for p in D["frame"]] if D else None


def basemap_extent(D=None):
    """the whole basemap's rectangle as four survey corners (frame axes); None without data"""
    D = D if D is not None else basemap_load()
    return [tuple(p) for p in D["extent"]] if D else None


def basemap_layers(mode, override=None):
    """the layer switches of a mode (BASEMAP_MODES) with a drawing's own changes laid over them, e.g.
    basemap_layers("minimal", {"streets": ("main",), "buildings": False}) for D5 Sound b (stream + main roads)"""
    if mode not in BASEMAP_MODES:
        raise ValueError(u"basemap mode '{}' unknown: one of {}".format(mode, ", ".join(sorted(BASEMAP_MODES))))
    lay = dict(BASEMAP_MODES[mode])
    for k, v in (override or {}).items():
        if k not in lay:
            raise ValueError(u"basemap layer '{}' unknown: one of {}".format(k, ", ".join(sorted(lay))))
        lay[k] = v
    return lay


def _bm_bb(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return min(xs), min(ys), max(xs), max(ys)


def _bm_hit(P, box):
    if box is None:
        return True
    b = _bm_bb(P)
    return not (b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3])


def _bm_ramp(t):
    """BM_HEIGHT_RAMP at t in 0..1 (hex)"""
    t = min(1.0, max(0.0, t))
    n = len(BM_HEIGHT_RAMP) - 1
    i = min(n - 1, int(t * n))
    f = t * n - i
    a, b = BM_HEIGHT_RAMP[i], BM_HEIGHT_RAMP[i + 1]
    return "".join("%02X" % int(round(int(a[j:j + 2], 16) + (int(b[j:j + 2], 16) - int(a[j:j + 2], 16)) * f))
                   for j in (0, 2, 4))


def basemap_items(mode="detailed", override=None, box=None, D=None, split_buildings=False):
    """the basemap of a drawing as items (bottom first; see the head of this file), in survey m. mode: "detailed",
    "simple", "minimal", "topographic" (02 §1); override: layer changes for this drawing (basemap_layers); box =
    (x0, y0, x1, y1) survey m: only what touches it (the caller clips to its frame); split_buildings=True gives
    every building its own fill item (for a page that fills even-odd only; default: nonzero fills in chunks).
    [] without data."""
    D = D if D is not None else basemap_load()
    if not D:
        return []
    # the same request in one run is made once and copied (Aras 29 Oct 19:18: build once, cache, copy the layers)
    mk = ("items", id(D), mode, repr(sorted((override or {}).items())), tuple(box) if box else None,
          bool(split_buildings))
    if mk in _BM_MEMO:
        return list(_BM_MEMO[mk])
    _BM_MEMO[mk] = _bm_items(D, mode, override, box, split_buildings)
    return list(_BM_MEMO[mk])


def _bm_items(D, mode, override, box, split_buildings):
    """basemap_items without the memo"""
    lay = basemap_layers(mode, override)
    L = D["layers"]
    out = []

    def fills(groups, col, alpha=1.0, nonzero=True, chunk=300):
        cur = []
        for g in groups:
            g = [R for R in g if len(R) >= 3]
            if not g or not _bm_hit(g[0], box):
                continue
            if split_buildings:
                out.append(("fill", g, col, alpha, nonzero))
                continue
            cur.extend(g)
            if len(cur) >= chunk:
                out.append(("fill", cur, col, alpha, nonzero))
                cur = []
        if cur:
            out.append(("fill", cur, col, alpha, nonzero))

    def lines(Ps, col, w, dash=None, alpha=1.0):
        for P in Ps:
            if len(P) >= 2 and _bm_hit(P, box):
                out.append(("line", P, col, w, list(dash) if dash else None, alpha))

    # ground: tree cover, fields, parks / grass (satellite first, mapped areas over it)
    if lay["trees"]:
        fills(L["lc"].get("trees", []), BM_COL["tree"])
    if lay["fields"]:
        fills(L["lc"].get("farmland", []) + L["lc"].get("orchard", []), BM_COL["field"])
        fills([z["rings"] for z in L["zones"] if z["kind"] == "agri"], BM_COL["field"])
    if lay["green"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") != "wood"], BM_COL["park"])
    if lay["trees"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") == "wood"], BM_COL["tree"])
    # contours
    if lay["contours"]:
        cs = L["contours"]
        if lay["contours"] == "height":
            zs = [c[1] for c in cs if c[1] is not None]
            z0, z1 = (min(zs), max(zs)) if zs else (0.0, 1.0)
            for major, z, P in cs:
                col = _bm_ramp((z - z0) / max(1.0, z1 - z0)) if z is not None else BM_COL["contour"]
                lines([P], col, BM_LW["contour_topo"][1 if major else 0])
        else:
            for major, z, P in cs:
                lines([P], BM_COL["contour"], BM_LW["contour"][1 if major else 0])
    # streets
    st = lay["streets"]
    if st is True or st == "faint":
        faint = st == "faint"
        fills(L["street_areas"], BM_FAINT["road"] if faint else BM_COL["road"], nonzero=False)
        for cl, P in L["streets_out"]:                    # beyond the frame: OpenStreetMap centrelines
            lines([P], BM_FAINT["road_line"] if faint else BM_COL["road"], BM_LW[cl] * (1.6 if cl != "path" else 1.0))
        if not faint:
            lines(L["street_edges"], BM_COL["road_edge"], BM_LW["road_edge"])
    elif st:
        for cl, P in L["streets_in"] + L["streets_out"]:
            if cl in st:
                lines([P], BM_FAINT["road_line"] if cl != "main" else BM_COL["road_edge"], BM_LW[cl])
    # the stream: ONE drawing (the site board's water and its edge inside the frame, OpenStreetMap's course beyond)
    if lay["stream"]:
        fills(L["water"], BM_COL["water"], nonzero=False)
        lines(L["water_edge"], BM_COL["water_edge"], BM_LW["water_edge"])
        if st is True or st == "faint":
            fills([[R] for R in L["decks"]], BM_FAINT["road"] if st == "faint" else BM_COL["road"])
        for P in L["covered"]:
            lines([P], BM_COL["water_edge"], BM_LW["covered"], BM_COVERED_DASH)
        fills(L["water_out"], BM_COL["water"], nonzero=False)
        for kind, P in L["waterways_out"]:
            lines([P], BM_COL["water"], BM_LW["river_osm" if kind == "river" else "stream_osm"])
    # buildings
    bl = lay["buildings"]
    if bl:
        if bl is True:
            fills([b["rings"] for b in L["buildings"] if not b.get("her")], BM_COL["bld"])
            fills([b["rings"] for b in L["buildings"] if b.get("her")], BM_COL["her"])
            for b in L["buildings"]:
                if b.get("her") or b.get("osm"):
                    lines([R + R[:1] for R in b["rings"][:b.get("np", len(b["rings"]))]],
                          BM_COL["her_edge"] if b.get("her") else BM_COL["bld_osm_edge"],
                          BM_LW["her_edge"] if b.get("her") else BM_LW["osm_edge"])
        else:
            fills([b["rings"] for b in L["buildings"]],
                  BM_FAINT["bld_veryfaint"] if bl == "veryfaint" else BM_FAINT["bld"])
    if lay["stream"] and (st is True or bl is True):
        lines(L["bridges"], BM_COL["ink"], BM_LW["bridge"])
    return out


def basemap_draw(items, T, fill_fn, line_fn, text_fn=None):
    """draws items through the caller's page: T(p) survey m -> page point; fill_fn(rings, hex, alpha, nonzero);
    line_fn(pts, hex, width_mm, dash_mm, alpha); text_fn(s, (x, y), size_mm, hex, bold, align) (texts are left out
    without it). Returns the number of items drawn."""
    n = 0
    for it in items:
        if it[0] == "fill":
            fill_fn([[T(p) for p in R] for R in it[1]], it[2], it[3], it[4])
        elif it[0] == "line":
            line_fn([T(p) for p in it[1]], it[2], it[3], it[4], it[5])
        elif it[0] == "text" and text_fn is not None:
            text_fn(it[1], T(it[2]), it[3], it[4], it[5], it[6])
        else:
            continue
        n += 1
    return n


# ------------------------------------------------------------------------------------------- key-map cut lines
def _bm_clip_convex(a, b, poly):
    """the part of segment a-b inside the convex polygon poly (any turn), or None"""
    t0, t1 = 0.0, 1.0
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = len(poly)
    s = sum((poly[(i + 1) % n][0] - poly[i][0]) * (poly[(i + 1) % n][1] + poly[i][1]) for i in range(n))
    ccw = s < 0
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        ex, ey = q[0] - p[0], q[1] - p[1]
        nx, ny = (-ey, ex) if ccw else (ey, -ex)          # inward normal
        den = nx * dx + ny * dy
        num = nx * (a[0] - p[0]) + ny * (a[1] - p[1])
        if abs(den) < 1e-12:
            if num < 0:
                return None
            continue
        t = -num / den
        if den > 0:
            t0 = max(t0, t)
        else:
            t1 = min(t1, t)
        if t0 > t1:
            return None
    return (a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)


def basemap_cut_items(cuts, scale_den, frame=None, inset_mm=3.0, tri_mm=2.6, text_mm=2.4, col=None, D=None):
    """the section lines of ONE page's key map (D11: only that page's cuts) as items, kept inside the frame: a line
    per cut, an architectural triangle at each end pointing the way the section looks, the end's name beyond it.
    cuts = [(end1, end2, (name1, name2)[, look])], survey m, end1 = the section's left end; look = +1 (default:
    the viewer stands so end1 is on the left, end2 on the right) or -1 (the other way). scale_den: the key map's
    scale (1:scale_den) for the mm sizes; frame: the polygon to stay in (default the analysis frame), the ends are
    pulled in by inset_mm so the markers and names stay inside it. With the level module, basemap_cut_ids() makes
    cuts from cut ids."""
    frame = frame or basemap_frame(D)
    col = col or BM_COL["cut"]
    m = scale_den / 1000.0                               # survey m per print mm
    out = []
    for c in cuts:
        a, b, names = c[0], c[1], c[2]
        look = c[3] if len(c) > 3 else 1
        L0 = _bm_math.hypot(b[0] - a[0], b[1] - a[1])
        if L0 < 1e-6:
            continue
        ux, uy = (b[0] - a[0]) / L0, (b[1] - a[1]) / L0
        if frame:
            ab = _bm_clip_convex(a, b, frame)
            if ab is None:
                continue
            a, b = ab
        pull = inset_mm * m + tri_mm * m                    # room for the marker and the name inside the frame
        L = _bm_math.hypot(b[0] - a[0], b[1] - a[1])
        if L <= 2.0 * pull:
            continue
        a = (a[0] + ux * pull, a[1] + uy * pull)
        b = (b[0] - ux * pull, b[1] - uy * pull)
        fx, fy = -uy * look, ux * look                      # the way the section looks (left normal of end1 -> end2)
        out.append(("line", [a, b], col, BM_LW["cut"], [3.0, 0.8], 1.0))
        h = tri_mm * m
        for p, nm, sgn in ((a, names[0], -1.0), (b, names[1], 1.0)):
            out.append(("fill", [[(p[0] - ux * h * 0.5, p[1] - uy * h * 0.5),     # the triangle stands on the
                                  (p[0] + ux * h * 0.5, p[1] + uy * h * 0.5),     # line's end, its apex the way
                                  (p[0] + fx * h, p[1] + fy * h)]], col, 1.0, True))   # the section looks
            out.append(("line", [(p[0] - ux * h * 0.6, p[1] - uy * h * 0.6), (p[0] + ux * h * 0.6, p[1] + uy * h * 0.6)],
                        col, BM_LW["cut"] * 1.6, None, 1.0))
            q = (p[0] + ux * sgn * (h * 0.6 + text_mm * m * 0.9) - fx * text_mm * m * 0.2,
                 p[1] + uy * sgn * (h * 0.6 + text_mm * m * 0.9) - fy * text_mm * m * 0.2)
            out.append(("text", nm, q, text_mm, col, True, "MC"))
    return out


def basemap_cut_ids(ids, looks=None):
    """cuts for basemap_cut_items from the level module (common/levels.py, its data included before it): the ends
    and their names of each cut id; looks = {id: -1} to turn a marker round"""
    ends, labs = globals().get("level_ends"), globals().get("level_end_labels")
    if not callable(ends) or not callable(labs):
        raise RuntimeError("basemap_cut_ids needs the level module: include ../common/data/LEVELS.py and "
                           "../common/levels.py")
    out = []
    for cid in ids:
        a, b = ends(cid)
        out.append((a, b, labs(cid), (looks or {}).get(cid, 1)))
    return out


# ------------------------------------------------------------------------------------------- writing (site board)
def _bm_r(P, nd=1):
    return [[round(p[0], nd), round(p[1], nd)] for p in P]


def _bm_clip_rect(P, closed, r):
    """P clipped to the axis-aligned rectangle r = (u0, v0, u1, v1) (frame-local): a polygon (Sutherland-Hodgman,
    one ring or None) or a polyline (its runs inside)"""
    u0, v0, u1, v1 = r
    if closed:
        R = list(P)
        for k_, lim, keep_ge in ((0, u0, True), (0, u1, False), (1, v0, True), (1, v1, False)):
            if not R:
                return None
            nxt = []
            for i in range(len(R)):
                p, q = R[i - 1], R[i]
                pin = p[k_] >= lim if keep_ge else p[k_] <= lim
                qin = q[k_] >= lim if keep_ge else q[k_] <= lim
                if qin:
                    if not pin:
                        t = (lim - p[k_]) / (q[k_] - p[k_])
                        nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                    nxt.append(q)
                elif pin:
                    t = (lim - p[k_]) / (q[k_] - p[k_])
                    nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            R = nxt
        return R if len(R) >= 3 else None
    runs, cur = [], []
    for a, b in zip(P, P[1:]):
        t0, t1 = 0.0, 1.0
        d = (b[0] - a[0], b[1] - a[1])
        ok = True
        for k_, lim, sgn in ((0, u0, 1), (0, u1, -1), (1, v0, 1), (1, v1, -1)):
            den = d[k_] * sgn
            num = (a[k_] - lim) * sgn
            if abs(den) < 1e-12:
                if num < 0:
                    ok = False
                    break
                continue
            t = -num / den
            if den > 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
            continue
        p0 = (a[0] + d[0] * t0, a[1] + d[1] * t0)
        p1 = (a[0] + d[0] * t1, a[1] + d[1] * t1)
        if cur and (abs(cur[-1][0] - p0[0]) > 1e-9 or abs(cur[-1][1] - p0[1]) > 1e-9):
            if len(cur) > 1:
                runs.append(cur)
            cur = []
        if not cur:
            cur = [p0]
        cur.append(p1)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def basemap_export(S, log=None):
    """SITE BOARD ONLY, once a run after the site model and its land cover are made (S = the site model; S.osm the
    parsed OpenStreetMap file): writes BASEMAP_FILE. Inside the analysis frame the site board's own layers (the
    ones p.06 draws), between the frame and the extent OpenStreetMap's, cut at the frame's edge so nothing is drawn
    twice; contours (survey, frame only) carry their height. Returns the path, or None (a WARNING in log)."""
    import time as _t
    log = log if log is not None else []
    # unchanged site model (same build_site key, S.site_key) = the file on disk is kept, not made again
    kf = BASEMAP_FILE + ".key"
    key = u"{}|{}|{}".format(BASEMAP_FORMAT, globals().get("SCRIPT_VERSION", ""), getattr(S, "site_key", None) or "")
    try:
        if getattr(S, "site_key", None) and _bm_os.path.isfile(BASEMAP_FILE) and _bm_os.path.isfile(kf):
            with open(kf, "r", encoding="utf-8") as fh:
                if fh.read().strip() == key:
                    log.append(u"Shared basemap unchanged (same site model): {} kept.".format(BASEMAP_FILE))
                    return BASEMAP_FILE
    except Exception:
        pass
    try:
        F = S.F
        loc = lambda p: F.local(p[0], p[1])
        wld = lambda q: F.world(q[0], q[1])
        fr = (F.u0, F.v0, F.u1, F.v1)
        us = [loc(p)[0] for _, p in BASEMAP_REACH] + [F.u0, F.u1]
        vs = [loc(p)[1] for _, p in BASEMAP_REACH] + [F.v0, F.v1]
        ex = (min(us) - BASEMAP_MARGIN, min(vs) - BASEMAP_MARGIN, max(us) + BASEMAP_MARGIN, max(vs) + BASEMAP_MARGIN)
        # the ring between frame and extent as four rectangles that do not overlap (frame-local)
        ring = [(ex[0], ex[1], ex[2], fr[1]), (ex[0], fr[3], ex[2], ex[3]),
                (ex[0], fr[1], fr[0], fr[3]), (fr[2], fr[1], ex[2], fr[3])]

        def outside_poly(P):
            Q = [loc(p) for p in P]
            res = []
            for r in ring:
                c = _bm_clip_rect(Q, True, r)
                if c:
                    res.append(_bm_r([wld(q) for q in c]))
            return res

        def outside_line(P):
            Q = [loc(p) for p in P]
            return [_bm_r([wld(q) for q in run]) for r in ring for run in _bm_clip_rect(Q, False, r)]

        def in_ring(p):
            u, v = loc(p)
            return ex[0] <= u <= ex[2] and ex[1] <= v <= ex[3] and not (fr[0] <= u <= fr[2] and fr[1] <= v <= fr[3])
        L = dict(lc={}, zones=[], contours=[], street_areas=[], street_edges=[], streets_in=[], streets_out=[],
                 water=[], water_edge=[], decks=[], covered=[], water_out=[], waterways_out=[], buildings=[],
                 bridges=[])
        mains = set(globals().get("MAIN_ROADS") or ("motorway", "trunk", "primary", "secondary", "tertiary"))
        peds = set(globals().get("PED") or ("footway", "path", "pedestrian", "steps", "cycleway", "bridleway",
                                             "track", "corridor"))
        skip = set(globals().get("SKIP_HW") or ("proposed", "construction", "platform", "bus_stop", "elevator"))
        ccls = lambda hw: "path" if hw in peds else ("main" if hw in mains else "lane")
        # ---- inside the frame: the site board's layers
        lcf = globals().get("r28e_lc")
        for key in ("trees", "farmland", "orchard"):
            try:
                groups = lcf(S, key) if callable(lcf) else [[P] for P in (getattr(S, "lc", None) or {}).get(key) or []]
            except Exception:
                groups = [[P] for P in (getattr(S, "lc", None) or {}).get(key) or []]
            L["lc"][key] = [[_bm_r(P) for P in g if len(P) >= 3] for g in groups]
        for z in getattr(S, "zones", None) or []:
            if z["kind"] in ("green", "agri"):
                L["zones"].append(dict(kind=z["kind"], sub=z.get("sub"), rings=[_bm_r(P) for P in z["Ps"] + z["Hs"]]))
        z_at = getattr(S, "z_at", None)
        for major, P in getattr(S, "contours", None) or []:
            z = None
            if callable(z_at):
                try:
                    zs = sorted(z_at(p[0], p[1]) for p in P[::max(1, len(P) // 9)])
                    z = round(zs[len(zs) // 2] / 5.0) * 5.0
                except Exception:
                    z = None
            L["contours"].append([bool(major), z, _bm_r(P)])
        for rg in getattr(S, "road_net", None) or []:
            L["street_areas"].append([_bm_r(rg["P"])] + [_bm_r(H) for H in rg.get("H", [])])
        L["street_edges"] = [_bm_r(P) for P in getattr(S, "road_lines_net", None) or []] + \
            [_bm_r(r_["P"]) for r_ in S.roads if not r_.get("w")]
        L["streets_in"] = [[ccls((r_.get("tags") or {}).get("highway")), _bm_r(r_["P"])] for r_ in S.roads] + \
            [["path", _bm_r(r_["P"])] for r_ in getattr(S, "paths", None) or []]
        L["water"] = [[_bm_r(wt["P"])] + [_bm_r(H) for H in wt.get("H", [])] for wt in S.water]
        L["water_edge"] = [_bm_r(P) for P in getattr(S, "water_outline", None) or []]
        L["decks"] = [_bm_r(P) for P in getattr(S, "decks", None) or []]
        L["covered"] = [_bm_r(P) for P in getattr(S, "covered", None) or []]
        L["bridges"] = [_bm_r(P) for P in getattr(S, "bridges", None) or []]
        for u in S.bld:
            parts = [_bm_r(P) for P in u["parts"] if len(P) >= 3]
            if parts:
                L["buildings"].append(dict(rings=parts + [_bm_r(H) for H in (u.get("holes") or [])], np=len(parts),
                                           her=u.get("fabric") in ("monument", "sacred"),
                                           osm=u.get("src") in ("osm", "osm+label")))
        n_in = len(L["buildings"])
        # ---- the ring between frame and extent: OpenStreetMap
        osm = getattr(S, "osm", None)
        n_out = 0
        if osm:
            Pj = osm.get("P")
            zc = globals().get("zone_class")
            chain = globals().get("chain_segments")
            for refs, tags in osm["ways"].values():
                if len(refs) < 2:
                    continue
                P = [p for p in (Pj(r) for r in refs) if p]
                if len(P) < 2:
                    continue
                closed = refs[0] == refs[-1] and len(P) >= 4
                if "building" in tags:
                    if closed:
                        c = (sum(p[0] for p in P[:-1]) / (len(P) - 1), sum(p[1] for p in P[:-1]) / (len(P) - 1))
                        if in_ring(c):
                            her = bool(tags.get("historic")) or tags.get("amenity") == "place_of_worship" or \
                                tags.get("building") in ("mosque", "church", "synagogue", "temple")
                            L["buildings"].append(dict(rings=[_bm_r(P[:-1])], np=1, her=her, osm=True))
                            n_out += 1
                    continue
                hw = tags.get("highway")
                if hw and hw not in skip and tags.get("area") != "yes":
                    L["streets_out"].extend([ccls(hw), run] for run in outside_line(P))
                    continue
                ww = tags.get("waterway")
                if ww in ("river", "stream", "canal"):
                    L["waterways_out"].extend(["river" if ww == "river" else "stream", run] for run in outside_line(P))
                    continue
                if closed:
                    if tags.get("natural") == "water" or tags.get("waterway") == "riverbank":
                        L["water_out"].extend([R] for R in outside_poly(P[:-1]))
                        continue
                    k = zc(tags) if callable(zc) else None
                    if k and k[0] in ("green", "agri"):
                        rs = outside_poly(P[:-1])
                        if rs:
                            L["zones"].append(dict(kind=k[0], sub=k[1], rings=rs))
            for mem, tags in osm.get("rels") or []:
                if tags.get("type") != "multipolygon" or "building" in tags or tags.get("ref:whc") or \
                        not callable(zc) or not callable(chain):
                    continue
                k = zc(tags)
                if not k or k[0] not in ("green", "agri"):
                    continue
                outer = []
                for ref, role in mem:
                    if role != "inner" and ref in osm["ways"]:
                        P = [p for p in (Pj(r) for r in osm["ways"][ref][0]) if p]
                        if len(P) >= 2:
                            outer.append([(p[0], p[1]) for p in P])
                for c in chain(outer, 0.05):
                    if len(c) >= 4:
                        rs = outside_poly(c[:-1] if c[0] == c[-1] else c)
                        if rs:
                            L["zones"].append(dict(kind=k[0], sub=k[1], rings=rs))
        else:
            log.append(u"WARNING: shared basemap: no OpenStreetMap in the site model, so it ends at the analysis frame.")
        corners = lambda b: [_bm_r([wld(q)])[0] for q in ((b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3]))]
        out = dict(format=BASEMAP_FORMAT, source=u"{} · {}".format(globals().get("SCRIPT_VERSION", "site board"),
                                                                  _t.strftime("%Y-%m-%d %H:%M")),
                   frame=_bm_r(globals().get("SITE_FRAME_LK") or [wld(q) for q in ((fr[0], fr[1]), (fr[2], fr[1]),
                                                                                    (fr[2], fr[3]), (fr[0], fr[3]))]),
                   extent=corners(ex), reach=[[n, list(p)] for n, p in BASEMAP_REACH], layers=L,
                   note=u"survey m (0.1 m); inside the analysis frame the site board's layers (survey, OpenStreetMap, "
                        u"ESA WorldCover 2021), beyond it OpenStreetMap (Data/bergama_osm.osm, ODbL); contours from "
                        u"the survey, frame only, height = the terrain at their points to the nearest 5 m")
        _bm_os.makedirs(_bm_os.path.dirname(BASEMAP_FILE), exist_ok=True)
        with open(BASEMAP_FILE, "w", encoding="utf-8") as fh:
            _bm_json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        for k_ in list(_BM_MEMO):
            if k_ == BASEMAP_FILE or (isinstance(k_, tuple) and k_[0] == "items"):
                _BM_MEMO.pop(k_, None)
        if getattr(S, "site_key", None):
            with open(kf, "w", encoding="utf-8") as fh:
                fh.write(key)
        log.append(u"Shared basemap written ({}): {:,} buildings in the frame, {:,} beyond it, {:,} contours, extent "
                   u"{:,.0f} x {:,.0f} m.".format(BASEMAP_FILE, n_in, n_out, len(L["contours"]), ex[2] - ex[0],
                                                 ex[3] - ex[1]))
        return BASEMAP_FILE
    except Exception as ex_:
        import traceback as _tb
        log.append(u"WARNING: the shared basemap was not written ({}):\n{}".format(ex_, _tb.format_exc()))
        return None


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

# v10: the sketch engine and data/SKETCH_SRC.py are no longer included (the sections are drawn to the level table in
# parts/70_sections.py); data/SKETCH_SRC.py stays in the repo because bergama_agriculture_alternatives includes it.
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

# ================================================================ v10 the four proposal sections, true to the cut
# v10 (revision 29 Oct, WO-T3b-3; package C "Page 13", brief 02 §3-§6): the sketches are gone. Each section is drawn
# at 1:500 on the booklet page from the level table (common/levels.py: bed, bed width, bank and wall tops, bank type
# and angle, terraces, Q100, Q500) with the shared section parts (DSİ walls, embankments, loose earth, railings,
# stone / concrete / earth / gravel hatches, steps seated into the bank) and the plants module (every species at its
# true size and form; D6: no fig, citrus, iris, oleander, white poplar; D2: common reed only in lined basins the flood
# passes by). Figures through ONE helper, _p13_fig (figures.py paused: swap the new set in there). All four sections
# look downstream: the NE bank (left bank) on the left, the SW bank on the right, as the key map's triangles show.
# Drawn in booklet print mm (k = PS_K mm per m); build_sheet() places the block on the A0 sheet at 1 / BK_S.
PS_SCALE = 500                        # 1:500 on the booklet page (standard scales, SCRIPT_STANDARD §8)
PS_K = 1000.0 / PS_SCALE              # print mm per m (k of section_parts and plants)
PS_DEPTH = 1.0                        # m of cut ground drawn under the bed (section_parts drawing rule)
PS_WALL_T = 0.60                      # m: DSİ wall thickness: no sourced value; the same 0.60 m as p.04-05 (site board P45_WALL_T_M, G2)
PS_RAIL_H = 1.10                      # m: railing height on the wall and bank tops: drawing value
PS_KERB_H = 0.15                      # m: basin kerb above the ground: drawing value
PS_STRIP = (3.00, 0.40)               # m: the summer strip channel in the bed (proposal): width, depth
PS_FREEBOARD = 0.30                   # m: a dry proposed floor sits at least this far above Q500 (design rule)
PS_LBL = BK_MIN_PT * PT               # print mm: the smallest word on the page (7.5 pt)
PS_TTL = 9.5 * PT                     # section titles
PS_NOTE = 8.0 * PT                    # the key line under a title, the key map title
PS_ROW = PS_LBL * 1.35                # one label row
PS_FIG = "5E5650"                     # figures
PS_TIMBER = "AA8148"                  # boardwalk timber (icons palette: timber)
PS_FLOOD = "C1D3DB"                   # the reach of Q500 (wash, see-through)
PS_FLOOD_A = 0.55
# where each cut crosses the stream axis (survey m; the cut centres of the level table's W rows): the drawn span runs
# from it to the cut's two ends (level_ends), NE end on the left
PS_AXIS = {"W1": (29693.022, 32569.176), "W2": (29959.774, 32264.566), "W3": (30354.663, 31689.671),
           "W4": (30991.856, 31039.404)}
# (sheet key, cut id, number on the page, name, takeaway in the title)
PS_CUTS = [("up", "W1", 1, u"Upstream entry", u"runoff cleaned in lined reed basins, given back in summer"),
           ("k4", "W2", 2, u"K4 walking hub", u"seating steps down to the summer strip, the hub square stays dry"),
           ("k5", "W3", 3, u"K5 Demeter's Garden", u"garden above Q500, stream commons below it"),
           ("down", "W4", 4, u"Downstream reach", u"planting bands and a boardwalk that follow the flood levels")]
PS_BREAK = {"W2": ("SW", 50.0)}       # W2's SW land (flat street level to the cut end 80 m out) drawn to 50 m, broken


def ps_lv(z):
    return u"+%.2f" % z


def ps_put(pg, shapes):
    """house shapes ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) of the shared modules -> page items"""
    for s in shapes:
        if not s or len(s) < 3 or not s[1]:
            continue
        if s[0] == "poly":
            r = s[1]
            rings = r if isinstance(r[0][0], (list, tuple)) else [r]
            pg.poly(rings, fill=s[2], stroke=s[3] if len(s) > 3 else None, lw=(s[4] if len(s) > 4 and s[4] else 0.1))
        elif s[0] == "line":
            pg.line(s[1], s[2], s[3] if len(s) > 3 and s[3] else 0.1)


class PsSec(object):
    """One section: its own page in print mm, (0, 0) = (left end u0, PS_DEPTH under the bed); u = m across the stream
    from the axis (NE negative), z = m a.s.l."""

    def __init__(self, cid, u0, u1, d):
        self.cid, self.u0, self.u1, self.d = cid, float(u0), float(u1), d
        self.bed = level(cid, "bed")
        self.z0 = self.bed - PS_DEPTH
        self.k = PS_K
        self.hw = level(cid, "bed_width_cm") / 200.0          # half the bed width (m), the bed centred on the axis
        self.pg = Page(0, 0)
        self.labels = []                                      # (text, u, z of the thing's top, proposal?)
        self.prof = []                                        # the cut line (u, z), left to right, for the flood
        self.w = (self.u1 - self.u0) * self.k

    def X(self, u):
        return (u - self.u0) * self.k

    def Y(self, z):
        return (z - self.z0) * self.k

    def P(self, pts):
        return [(self.X(u), self.Y(z)) for u, z in pts]

    def put(self, shapes):
        ps_put(self.pg, shapes)

    def lab(self, text, u, z, prop=False):
        self.labels.append((text, u, z, prop))


def ps_kind(cid, side):
    return (level_cut(cid).get(side) or {}).get("type")


def ps_extent(cid):
    """(u0, u1, {"NE": m, "SW": m} from the axis to each cut end): the cut's span, widened to show a whole bank
    (embankment crest + 3 m, wall + 4 m, loose earth crest + 4 m), W2's SW cut short (PS_BREAK)"""
    c = PS_AXIS[cid]
    d = dict((nm, math.hypot(p[0] - c[0], p[1] - c[1])) for p, nm in zip(level_ends(cid), level_end_labels(cid)))
    hw = level(cid, "bed_width_cm") / 200.0
    ext = {}
    for side in ("NE", "SW"):
        kind, e = ps_kind(cid, side), d[side]
        if kind == "dsi_wall":
            e = max(e, hw + PS_WALL_T + 4.0)
        elif kind == "embankment":
            h = level(cid, "top", side) - level(cid, "bed")
            e = max(e, hw + h / math.tan(math.radians(level(cid, "angle_deg", side))) + 3.0)
        elif kind == "loose_earth":
            e = e + 4.0
        ext[side] = e
    br = PS_BREAK.get(cid)
    if br:
        ext[br[0]] = min(ext[br[0]], br[1])
    return -ext["NE"], ext["SW"], d


def _p13_fig(S, pose, u, z, height=1.75, facing=1):
    """page 13's ONE figure helper (figures.py paused: the new silhouette set goes in here): the legacy fig_polys
    at true height for the section's scale, feet at (u, z)"""
    for ring in fig_polys(pose, height, facing):
        S.pg.poly([[(S.X(u + px), S.Y(z + py)) for px, py in ring]], fill=PS_FIG)


def ps_name(key):
    sp = PLA_SPECIES[key]
    tr = sp.get("turkish")
    return sp["name"] if not tr or tr == "UNVERIFIED" else u"%s (%s)" % (sp["name"], tr)


def ps_plant(S, key, u, z, label=True, **kw):
    """a species at true size on the ground at (u, z); labelled at its top once per section"""
    S.put(pla_section(key, S.X(u), S.Y(z), S.k, **kw))
    if label:
        S.lab(ps_name(key), u, z + (kw.get("h_m") or PLA_SPECIES[key]["h_m"]))


def ps_land(S, pts, material="earth"):
    """cut ground under a surface [(u, z)] left to right, down to the drawing's bottom"""
    S.put(sct_ground(S.P(pts), 0.0, S.k, material))


def ps_bed(S, uL, uR):
    """the gravel bed from uL to uR with the summer strip channel (PS_STRIP) on the axis, water in it"""
    w, dp = PS_STRIP
    b = S.bed
    pts = [(uL, b), (-w / 2.0, b), (-w / 2.0 + 0.6, b - dp), (w / 2.0 - 0.6, b - dp), (w / 2.0, b), (uR, b)]
    S.put(sct_ground(S.P(pts), 0.0, S.k, "gravel"))
    S.put(sec_water(S.P(pts[1:5])))
    S.lab(u"summer strip", 0.0, b, True)


def ps_wall(S, u_face, side, top, rail=True):
    """the DSİ stone wall with its water face at u_face (side -1: land to the left), bed to top; a railing on it"""
    sh, _ = sct_bank("dsi_wall", S.X(u_face), S.Y(top), S.Y(S.bed), side, S.k, t_m=PS_WALL_T, reach_m=0.05,
                     depth_m=PS_DEPTH)
    S.put(sh)
    if rail:
        ps_rail(S, u_face + side * 0.15, top)


def ps_rail(S, u, z):
    sh, _ = sct_bank("railing", S.X(u), S.Y(z), S.Y(S.bed), 1, S.k, h_m=PS_RAIL_H)
    S.put(sh)


def ps_block_ring(S, u0, u1, z0, z1, material):
    S.put(sct_hatch_fill(S.P([(u0, z0), (u1, z0), (u1, z1), (u0, z1)]), material, S.k, SCT["cut"], 0.25))


def ps_steps(u, z, n, rise, tread, side):
    """a flight of n steps from (u, z) climbing landward (side +1 = to the right): (surface points after the
    start, [(ua, ub, z_under, z_top)] one block per step, its slab 0.15 m under the step below)"""
    pts, blocks = [], []
    for _ in range(n):
        z2, u2 = z + rise, u + side * tread
        pts += [(u, z2), (u2, z2)]
        blocks.append((min(u, u2), max(u, u2), z - 0.15, z2))
        u, z = u2, z2
    return pts, blocks


def ps_wet(prof, wl):
    """the stretches of the cut line prof [(u, z)] under the water level wl, each closed along the water line"""
    runs, cur = [], []
    for i, a in enumerate(prof):
        if a[1] < wl:
            if not cur:
                if i > 0:
                    p = prof[i - 1]
                    t = (wl - p[1]) / (a[1] - p[1])
                    cur.append((p[0] + (a[0] - p[0]) * t, wl))
                else:
                    cur.append((a[0], wl))
            cur.append(a)
        elif cur:
            p = prof[i - 1]
            t = (wl - p[1]) / (a[1] - p[1])
            cur.append((p[0] + (a[0] - p[0]) * t, wl))
            runs.append(cur)
            cur = []
    if cur:
        cur.append((cur[-1][0], wl))
        runs.append(cur)
    return runs


def ps_flood_wash(S):
    """the reach of Q500 as a see-through wash behind everything (call first)"""
    for r in ps_wet(S.prof, level(S.cid, "q500")):
        S.pg.poly([S.P(r)], fill=PS_FLOOD, alpha=PS_FLOOD_A)


def ps_flood_lines(S):
    """Q500 dashed and Q100 dotted across every wet stretch; one label over the widest, at its left end"""
    q1, q5 = level(S.cid, "q100"), level(S.cid, "q500")
    for wl, dash in ((q5, [1.2, 0.6]), (q1, [0.3, 0.45])):
        for r in ps_wet(S.prof, wl):
            S.pg.line([(S.X(r[0][0]), S.Y(wl)), (S.X(r[-1][0]), S.Y(wl))], COL["river_mid"], 0.22, dash=dash)
    runs = [r_ for r_ in ps_wet(S.prof, q5) if r_[0][0] <= -S.hw + 0.01 <= r_[-1][0]]
    if runs:                                                    # in the channel, from its NE side: Q500 over its
        x = S.X(max(runs[0][0][0], -S.hw)) + 0.8                # line, Q100 under its own (clear of the strip)
        S.pg.text(u"Q500 %s" % ps_lv(q5), x, S.Y(q5) + 0.6, PS_LBL, COL["river_dark"])
        S.pg.text(u"Q100 %s" % ps_lv(q1), x, S.Y(q1) - 0.6 - PS_LBL * CAP, PS_LBL, COL["river_dark"])


def ps_arrow(S, pts, col, lw=0.3, dash=None):
    P = S.P(pts)
    S.pg.line(P, col, lw, dash=dash)
    (ax, ay), (bx, by) = P[-2], P[-1]
    L = math.hypot(bx - ax, by - ay) or 1e-9
    ux, uy, h = (bx - ax) / L, (by - ay) / L, 1.1
    S.pg.poly([[(bx, by), (bx - ux * h - uy * h * 0.45, by - uy * h + ux * h * 0.45),
                (bx - ux * h + uy * h * 0.45, by - uy * h - ux * h * 0.45)]], fill=col)


def ps_bank_text(S, side):
    """what the level table says about a bank, as printed under the section"""
    c = S.cid
    kind, top = ps_kind(c, side), level(c, "top", side)
    h = level(c, "height", side) or level_depth(c, side)
    if kind == "dsi_wall":
        s = u"DSİ stone wall %.2f m · top %s" % (h, ps_lv(top))
    elif kind == "embankment":
        s = u"embankment %.1f° · %.2f m · top %s" % (level(c, "angle_deg", side), h, ps_lv(top))
    elif kind == "loose_earth":
        s = u"loose earth bank %.2f m · top %s" % (h, ps_lv(top))
    else:
        s = u"no crest: the ground keeps rising"
    return u"%s today: %s" % (side, s)


# ---------------------------------------------------------------- W1 upstream entry
def ps_sec_w1(S):
    c, b, hw = S.cid, S.bed, S.hw
    tN, tS = level(c, "top", "NE"), level(c, "top", "SW")
    S.prof = [(S.u0, tN), (-hw, tN), (-hw, b), (hw, b), (hw, tS), (S.u1, tS)]
    ps_flood_wash(S)
    ps_land(S, [(S.u0, tN), (-hw, tN)])                         # NE: the street behind the wall
    # SW: three lined reed basins sunk into the land (D2 a: lined, root-contained, the flood passes by above Q500),
    # floors stepping down toward the stream: street runoff in at the far one, cleaned water out through the wall
    kt = 0.15                                                   # basin kerb / slab (plants module drawing rule)
    bas = [(23.0, 28.0, 1.10), (29.5, 34.5, 0.90), (36.0, 41.0, 0.70)]   # (u from, u to, floor under the ground m)
    surf = [(hw, tS)]
    for u0, u1, dp in bas:
        f = tS - dp - kt
        surf += [(u0 - kt, tS), (u0 - kt, f), (u1 + kt, f), (u1 + kt, tS)]
    surf.append((S.u1, tS))
    ps_land(S, surf)
    ps_bed(S, -hw, hw)
    ps_wall(S, -hw, -1, tN)
    ps_wall(S, hw, 1, tS)
    for i, (u0, u1, dp) in enumerate(bas):
        f = tS - dp
        S.put(pla_reed_basin(S.X(u0), S.X(u1), S.Y(f), S.Y(tS), S.k, PS_KERB_H, media_m=0.50,
                             wl_y=S.Y(f + 0.65)))
    S.lab(u"lined reed basins · above Q500", 32.0, tS + 2.9, True)
    S.lab(ps_name("reed"), 25.5, tS + 1.9)
    f_near, f_far = tS - bas[0][2], tS - bas[2][2]
    ps_arrow(S, [(S.u1 - 0.2, tS + 2.6), (41.4, tS + 1.4), (39.5, f_far + 0.85)], COL["river_mid"], 0.3)
    S.lab(u"street and roof runoff in", S.u1 - 0.6, tS + 2.6, True)
    ps_arrow(S, [(bas[0][0] - 0.3, f_near + 0.45), (hw + PS_WALL_T, f_near + 0.45), (hw - 0.1, f_near + 0.45),
                 (hw - 1.4, b + 0.25)], COL["river_dark"], 0.3, dash=[0.8, 0.4])
    S.lab(u"summer release to the strip", hw - 0.7, f_near + 0.6, True)
    # planting and people, each where it happens
    ps_plant(S, "plane", -21.5, tN, seed=1)
    ps_plant(S, "chaste", 20.2, tS, seed=2)
    for i, u in enumerate((-4.6, -3.7, 3.6, 4.5)):
        ps_plant(S, "soft_rush", u, b, label=(i == 0), seed=i)
    _p13_fig(S, "watch", -hw - 1.3, tN, facing=1)               # at the railing, looking into the channel
    _p13_fig(S, "walk", 18.6, tS, facing=1)                     # along the basins
    _p13_fig(S, "wade", 0.5, b - PS_STRIP[1], facing=-1)        # in the summer strip


# ---------------------------------------------------------------- W2 K4 walking hub
def ps_sec_w2(S):
    c, b, hw = S.cid, S.bed, S.hw
    tN, tS = level(c, "top", "NE"), level(c, "top", "SW")
    plat = b + 0.30                                             # sub-hub floor: just above the summer strip
    n, tread = 10, 0.80
    rise = (tS - plat) / n
    u_st = hw + 4.0                                             # the steps start 4.00 m behind today's wall line
    steps, blocks = ps_steps(u_st, plat, n, rise, tread, 1)
    u_sq = u_st + n * tread                                     # the hub square from here, at the wall top level
    S.prof = [(S.u0, tN), (-hw, tN), (-hw, b), (hw, b), (hw, plat), (u_st, plat)] + steps + [(S.u1, tS)]
    ps_flood_wash(S)
    ps_land(S, [(S.u0, tN), (-hw, tN)])
    ps_land(S, [(hw, plat), (u_st, plat)] + steps + [(S.u1, tS)])
    ps_bed(S, -hw, hw)
    ps_wall(S, -hw, -1, tN)
    ps_block_ring(S, hw, u_st, plat - 0.25, plat, "concrete")   # sub-hub floor slab
    for ua, ub, z0, z1 in blocks:                               # steps seated into the cut-back bank
        ps_block_ring(S, ua, ub, z0, z1, "stone")
    ps_block_ring(S, u_sq, S.u1, tS - 0.25, tS, "stone")        # hub square paving
    S.pg.poly([S.P([(hw, b), (hw + PS_WALL_T, b), (hw + PS_WALL_T, tS), (hw, tS)])], stroke=COL["ink2"], lw=0.18,
              dash=[0.8, 0.5])                                  # today's DSİ wall, replaced by the steps
    S.lab(u"today's wall line", hw + PS_WALL_T / 2.0, tS)
    S.lab(u"sub-hub floor %s" % ps_lv(plat), (hw + u_st) / 2.0, plat, True)
    S.lab(u"seating steps %d × %d cm" % (n, round(rise * 100)), u_st + 0.5 * n * tread, plat + 0.5 * n * rise + 0.6,
          True)
    S.lab(u"hub square %s" % ps_lv(tS), u_sq + 3.0, tS + 0.1, True)
    xb = S.X(S.u1)                                              # break line: the land goes on to the cut end
    yb, yt = S.Y(S.z0), S.Y(tS)
    S.pg.line([(xb, yb - 0.6), (xb, yb + 0.35 * (yt - yb)), (xb - 0.7, yb + 0.45 * (yt - yb)),
               (xb + 0.7, yb + 0.6 * (yt - yb)), (xb, yb + 0.7 * (yt - yb)), (xb, yt + 0.8)], COL["ink"], 0.2)
    ps_plant(S, "plane", u_sq + 7.0, tS, seed=3)
    ps_plant(S, "plane", u_sq + 21.0, tS, label=False, seed=4)
    for i, u in enumerate((hw + 0.4, hw + 1.0)):
        ps_plant(S, "soft_rush", u, plat, label=(i == 0), seed=5 + i)
    _p13_fig(S, "watch", -hw - 1.3, tN, facing=1)
    _p13_fig(S, "bike", -22.0, tN, facing=1)
    _p13_fig(S, "touch", hw + 1.8, plat, facing=-1)            # at the strip's edge
    for i in (3, 7):                                           # sitting on the steps, facing the stream
        ua, ub, _, z1 = blocks[i]
        _p13_fig(S, "sit", (ua + ub) / 2.0, z1, facing=-1)
    _p13_fig(S, "stand", u_sq + 1.0, tS, facing=-1)            # at the top of the steps, the viewing edge
    _p13_fig(S, "walk", u_sq + 15.0, tS, facing=1)
    _p13_fig(S, "sit", u_sq + 9.0, tS, facing=1)               # in the plane's shade


# ---------------------------------------------------------------- W3 K5 Demeter's Garden
def ps_sec_w3(S):
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, q5 = level(c, "top", "NE"), level(c, "q500")
    sh_ = [t for t in (level_cut(c).get("terraces") or []) if t.get("side") == "SW"]
    if not sh_:
        raise RuntimeError("W3: the SW shelf (terraces) is missing in ../common/data/LEVELS.py")
    lv = sh_[0]["level"]
    shelf = float(lv["value"] if isinstance(lv, dict) else lv)
    s0, s1 = float(sh_[0]["from_m"]), float(sh_[0]["to_m"])
    gf = math.ceil((q5 + PS_FREEBOARD) * 20.0) / 20.0          # garden floor: dry above Q500
    run = S.d["NE"] - hw                                        # NE loose earth: toe to the crest at the cut end
    n = max(1, int(round((tN - b) / 0.45)))
    rise, tread = (tN - b) / n, run / n
    crest = -hw - run
    steps, _ = ps_steps(-hw, b, n, rise, tread, -1)
    S.prof = list(reversed([(-hw, b)] + steps)) + [(hw, b), (s0, shelf), (s1, shelf), (s1, gf), (S.u1, gf)]
    S.prof = [(S.u0, tN)] + S.prof
    ps_flood_wash(S)
    # NE: today's loose earth bank (dashed) and the steps seated into it (section_parts earth bank with steps)
    sh, _ = sct_bank("earth", S.X(-hw), S.Y(tN), S.Y(b), -1, k, run_m=run, reach_m=crest - S.u0, depth_m=PS_DEPTH,
                     steps=[(rise, tread)] * n, steps_from_m=0.0, step_material="stone")
    ps_land(S, [(hw, b), (s0, shelf), (s1, shelf), (s1, gf), (S.u1, gf)])   # the garden: fill above the shelf
    S.put(sh)
    old = [(-hw - run * i / 12.0, b + (tN - b) * (3 * (i / 12.0) ** 2 - 2 * (i / 12.0) ** 3)) for i in range(13)]
    S.pg.line(S.P(old), COL["ink2"], 0.18, dash=[0.8, 0.5])
    ps_bed(S, -hw, hw)
    ps_rail(S, crest - 0.2, tN)
    # SW: the stream commons on the shelf (floods in winter), the garden raised above Q500 behind a stone wall
    ps_block_ring(S, s1, s1 + 0.40, shelf - 0.30, gf + 0.15, "stone")
    S.lab(u"steps down the bank %d × %d cm" % (n, round(rise * 100)), -hw - run * 0.45, b + (tN - b) * 0.45 + 2.0,
          True)
    S.lab(u"stream commons %s" % ps_lv(shelf), (s0 + s1) / 2.0, shelf, True)
    S.lab(u"Demeter's Garden %s" % ps_lv(gf), s1 + 1.5, gf + 0.3, True)
    gy = lambda u: shelf + (b - shelf) * max(0.0, min(1.0, (s0 - u) / (s0 - hw)))
    for i, u in enumerate((s0 - 3.2, s0 - 2.4, s0 - 1.6, s0 - 0.8)):
        ps_plant(S, "loosestrife" if i % 2 else "soft_rush", u, gy(u), label=(i < 2), seed=10 + i)
    for i in range(3):
        u = s1 + 0.9 + i * 0.6
        ps_plant(S, "lavender", u, gf, label=(i == 0), seed=20 + i)
    S.put(pla_crop_rows("tomato", S.X(s1 + 2.6), S.X(s1 + 7.0), S.Y(gf), k, spacing=1.0, h_m=1.0, crown_m=0.8))
    S.lab(u"Tomato (Domates)", s1 + 4.8, gf + 1.0)
    ps_plant(S, "plane", s1 + 14.5, gf, beyond=True, seed=30)  # café shade, a step behind the cut
    ps_plant(S, "olive", s1 + 10.0, gf, seed=31)
    ps_plant(S, "chaste", s1 + 8.0, gf, seed=32)
    S.lab(u"café beds", s1 + 13.0, gf + 2.1, True)
    _p13_fig(S, "watch", crest - 1.2, tN, facing=1)
    i = n // 2
    _p13_fig(S, "walk", -hw - tread * (i + 0.5), b + rise * (i + 1), facing=1)
    _p13_fig(S, "wade", -0.4, b - PS_STRIP[1], height=1.15, facing=1)
    _p13_fig(S, "sit", s0 + 5.0, shelf, facing=-1)
    _p13_fig(S, "walk", s0 + 10.5, shelf, facing=1)
    _p13_fig(S, "touch", s1 + 5.2, gf, facing=-1)             # picking tomatoes
    _p13_fig(S, "sit", s1 + 13.6, gf, facing=-1)              # café under the plane


# ---------------------------------------------------------------- W4 downstream reach
def ps_sec_w4(S):
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, aN = level(c, "top", "NE"), level(c, "angle_deg", "NE")
    tS, aS = level(c, "top", "SW"), level(c, "angle_deg", "SW")
    q1, q5 = level(c, "q100"), level(c, "q500")
    gN, gS = math.tan(math.radians(aN)), math.tan(math.radians(aS))
    cN, cS = -hw - (tN - b) / gN, hw + (tS - b) / gS            # crests (u)
    S.prof = [(S.u0, tN), (cN, tN), (-hw, b), (hw, b), (cS, tS), (S.u1, tS)]
    ps_flood_wash(S)
    zN = lambda u: b + (-hw - u) * gN                           # the NE slope's level at u
    sh, _ = sct_bank("embankment", S.X(-hw), S.Y(tN), S.Y(b), -1, k, angle_deg=aN, reach_m=cN - S.u0,
                     depth_m=PS_DEPTH)
    S.put(sh)
    sh, _ = sct_bank("embankment", S.X(hw), S.Y(tS), S.Y(b), 1, k, angle_deg=aS, reach_m=S.u1 - cS,
                     depth_m=PS_DEPTH)
    S.put(sh)
    ps_bed(S, -hw, hw)
    # NE: planting in bands by flood level: wet edge under Q100, the boardwalk in the Q100 band, trees above Q500
    dk = round((q1 - 0.40) * 20.0) / 20.0                       # boardwalk deck: floods at Q100 (design rule)
    ub = -hw - (dk - b) / gN                                    # where the deck meets the slope
    ua = ub + 6.0
    S.pg.poly([S.P([(ua, dk - 0.20), (ua, dk), (ub, dk), (ub, dk - 0.20)])], fill=PS_TIMBER, stroke=SCT["cut"],
              lw=0.25)
    u = ua - 0.3
    while u > ub + 0.5:                                         # piles down into the bank
        S.pg.line(S.P([(u, dk - 0.20), (u, zN(u) - 0.6)]), PS_TIMBER, 0.35)
        u -= 2.0
    ps_rail(S, ua - 0.1, dk)
    S.lab(u"boardwalk %s" % ps_lv(dk), (ua + ub) / 2.0, dk + PS_RAIL_H, True)
    u_q1 = -hw - (q1 - b) / gN
    for i, u in enumerate([-hw - 0.6 - 0.9 * j for j in range(5)]):
        ps_plant(S, "soft_rush" if i % 2 else "loosestrife", u, zN(u), label=(i < 2), seed=40 + i)
    S.lab(u"floodable planting", (-hw + u_q1) / 2.0 - 1.0, zN(-hw - 2.0) + 1.6, True)
    u_q5 = -hw - (q5 - b) / gN
    ps_plant(S, "tamarisk", (u_q5 + ub) / 2.0, zN((u_q5 + ub) / 2.0), seed=46)
    ps_plant(S, "ash", u_q5 - 4.0, zN(u_q5 - 4.0), seed=47)
    ps_plant(S, "plane", cN + 1.5, zN(cN + 1.5), seed=48)
    # SW: grass slope, rush at the toe, the field behind the crest takes the surplus water
    for i, u in enumerate((hw + 0.6, hw + 1.5)):
        ps_plant(S, "soft_rush", u, b + (u - hw) * gS, label=False, seed=50 + i)
    S.put(pla_crop_rows("cotton", S.X(cS + 1.0), S.X(S.u1 - 0.4), S.Y(tS), k, spacing=0.9, h_m=1.0, crown_m=0.6))
    S.lab(u"Cotton (Pamuk) · surplus water", (cS + S.u1) / 2.0, tS + 1.0, True)
    _p13_fig(S, "bike", S.u0 + 1.4, tN, facing=1)
    _p13_fig(S, "walk", (ua + ub) / 2.0 + 1.0, dk, facing=1)
    _p13_fig(S, "wade", 0.3, b - PS_STRIP[1], height=1.15, facing=-1)
    _p13_fig(S, "stand", S.u1 - 1.2, tS, facing=-1)


PS_DRAW = {"W1": ps_sec_w1, "W2": ps_sec_w2, "W3": ps_sec_w3, "W4": ps_sec_w4}


# ---------------------------------------------------------------- labels over the section, data rows under it
def ps_pack(items, xmin, xmax, rows=3, gap=1.2):
    """items [(w, ax)]: each label set over its anchor x (the leader drops straight down), in the lowest row where it
    touches no other label and no leader of a higher row crosses it. Returns [(row, x0) or None]."""
    placed = [[] for _ in range(rows)]
    leaders, out = [], [None] * len(items)
    for i in sorted(range(len(items)), key=lambda j: items[j][1]):
        w, ax = items[i]
        cands = [ax - w * f for f in (0.5, 0.35, 0.65, 0.2, 0.8, 0.05, 0.95)]
        for r in range(rows):
            ok = None
            for x0 in cands:
                x0 = max(xmin, min(xmax - w, x0))
                if not (x0 - 0.05 <= ax <= x0 + w + 0.05):
                    continue
                if any(x0 < b_ + gap and a_ < x0 + w + gap for a_, b_ in placed[r]):
                    continue
                if any(rr > r and x0 - gap < lx < x0 + w + gap for lx, rr in leaders):
                    continue
                if any(a_ - gap < ax < b_ + gap for q in range(r) for a_, b_ in placed[q]):
                    continue
                ok = x0
                break
            if ok is not None:
                placed[r].append((ok, ok + w))
                leaders.append((ax, r))
                out[i] = (r, ok)
                break
    return out


def ps_scale_bar(pg, x, y, k):
    """0-5-10-20 m at k mm per m from (x, y), its numbers over it, the round scale after it"""
    h, col = 0.9, COL["ink"]
    marks = (0, 5, 10, 20)
    for i, (a, b_) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * k, y, x + b_ * k, y + h)], fill=(col if i % 2 == 0 else COL["white"]), stroke=col,
                lw=0.15)
    for m_ in marks:
        pg.text(str(m_), x + m_ * k, y + h + 0.6, PS_LBL, col, align="C")
    pg.text(u"m · 1:%d" % PS_SCALE, x + 20 * k + text_w(u"20", PS_LBL) / 2.0 + 1.2, y + h + 0.6, PS_LBL, col)


def ps_finish(S, log):
    """flood levels, the labels over the drawing, the bank / bed rows under it, the scale bar"""
    pg = S.pg
    ps_flood_lines(S)
    top = items_bbox(pg.items)[3]
    seen, labs = set(), []
    for t, u, z, prop in S.labels:
        if t not in seen:
            seen.add(t)
            labs.append((t, u, z, prop))
    got = ps_pack([(text_w(t, PS_LBL), S.X(u)) for t, u, z, prop in labs], -4.0, S.w + 4.0)
    base = top + 1.6 + PS_LBL * 0.25
    for (t, u, z, prop), g in zip(labs, got):
        if g is None:
            log.append(u"NOTE section %s: label '%s' left out (no free place over the drawing)" % (S.cid, t))
            continue
        r, x0 = g
        yb = base + r * PS_ROW
        ax, ay = S.X(u), S.Y(z) + 0.5
        if yb - 0.8 > ay + 0.4:
            pg.line([(ax, yb - 0.8), (ax, ay)], COL["ink2"], 0.12)
        pg.text(t, x0, yb, PS_LBL, COL["accent"] if prop else COL["ink"])
    # under the drawing: the bed width as a dimension, each bank as the level table has it
    hw = S.hw
    y = -1.0
    xa, xb = S.X(-hw), S.X(hw)
    pg.line([(xa, y), (xb, y)], COL["ink"], 0.15)
    for x_ in (xa, xb):
        pg.line([(x_, y - 0.5), (x_, y + 0.6)], COL["ink"], 0.15)
    rows = []
    under = [(u"bed {:,.0f} cm · {}".format(level(S.cid, "bed_width_cm"), ps_lv(S.bed)), "C", (xa + xb) / 2.0),
             (ps_bank_text(S, "NE"), "L", 0.0), (ps_bank_text(S, "SW"), "R", S.w)]
    last = 0
    for t, al, x_ in under:
        w = text_w(t, PS_LBL)
        x0 = x_ - (w / 2.0 if al == "C" else (w if al == "R" else 0.0))
        r = 0
        while any(x0 < b_ + 2.0 and a_ < x0 + w + 2.0 for rr, a_, b_ in rows if rr == r):
            r += 1
        rows.append((r, x0, x0 + w))
        last = max(last, r)
        pg.text(t, x0, -1.6 - PS_LBL * CAP - r * PS_ROW, PS_LBL, COL["ink"])
    ps_scale_bar(pg, 0.0, -1.6 - PS_LBL * CAP - last * PS_ROW - 4.8, S.k)


def ps_section(cid, log):
    """one cut as a Page in print mm (see PsSec)"""
    u0, u1, d = ps_extent(cid)
    S = PsSec(cid, u0, u1, d)
    PS_DRAW[cid](S)
    ps_finish(S, log)
    return S.pg


# ---------------------------------------------------------------- the page block: key map strip + 2 x 2 sections
PS_GAP = 4.0                           # print mm between the panels


def ps_badge(pg, x, y, n, r=2.0):
    """the cut's number on the page (section titles and key map alike)"""
    pg.circle(x, y, r, fill=COL["accent"])
    fs = r * 1.15
    pg.text(str(n), x, y - fs * CAP / 2.0, fs, COL["white"], bold=True, align="C")


def ps_cell(pg, box, n, cid, name, take, note):
    """one section's panel: white ground, a coloured rule, the badge, the title (cut and name bold, the takeaway) and
    the key line under it. Returns the box left for the drawing (print mm)."""
    x0, y0, x1, y1 = box
    pg.poly([rect(x0, y0, x1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    pg.poly([rect(x0, y1 - 0.8, x1, y1)], fill=MP["discharge"][1])
    yt = y1 - 0.8 - 2.0 - PS_TTL * CAP                         # the title's baseline
    ps_badge(pg, x0 + 4.5, yt + PS_TTL * CAP / 2.0, n)
    yb, _ = ps_rich_para(pg, x0 + 8.0, yt + PS_TTL * 1.28, x1 - x0 - 11.0, u"**%s · %s** %s" % (cid, name, take),
                         PS_TTL, COL["ink_dark"])
    yb, _ = ps_rich_para(pg, x0 + 8.0, yb - 0.6, x1 - x0 - 11.0, note, PS_NOTE, COL["ink"])
    return (x0 + 3.0, y0 + 2.5, x1 - 3.0, yb - PS_NOTE * 0.25 - 2.0)


def ps_note(cid):
    """the key line of a section, from the level table"""
    q5 = level(cid, "q500")
    if cid == "W1":
        return u"Q500 %s stays **%.2f m** under the DSİ walls · reeds only in lined basins the flood passes by" % (
            ps_lv(q5), level(cid, "top", "SW") - q5)
    if cid == "W2":
        return u"Q500 %s stays **%.2f m** under the hub square · the steps flood, the square stays dry" % (
            ps_lv(q5), level(cid, "top", "SW") - q5)
    if cid == "W3":
        return u"Q500 %s · garden floor **%s** stays dry: olive and lavender need soil that never waterlogs" % (
            ps_lv(q5), ps_lv(math.ceil((q5 + PS_FREEBOARD) * 20.0) / 20.0))
    return u"Q500 %s stays **%.2f m** under the NE bank top · wet edge, boardwalk and trees by flood level" % (
        ps_lv(q5), level(cid, "top", "NE") - q5)


def ps_block(log):
    """page 13: the key map strip across the top (it serves all four sections), the four sections under it in
    reading order, all at 1:500, in print mm (0, 0)-(BK_W, BK_H). Returns (Page, {sheet key: panel box})."""
    pg = Page(BK_W, BK_H)
    yk = BK_H - PS_KEY_H
    ps_key_strip(pg, (0.0, yk, BK_W, BK_H), log)
    cw = (BK_W - PS_GAP) / 2.0
    ch = (yk - 2.0 * PS_GAP) / 2.0
    boxes = {}
    for i, (key, cid, n, name, take) in enumerate(PS_CUTS):
        x0 = (i % 2) * (cw + PS_GAP)
        y1 = yk - PS_GAP - (i // 2) * (ch + PS_GAP)
        box = (x0, y1 - ch, x0 + cw, y1)
        boxes[key] = box
        inner = ps_cell(pg, box, n, cid, name, take, ps_note(cid))
        sec = ps_section(cid, log)
        b = items_bbox(sec.items)
        if b[2] - b[0] > inner[2] - inner[0] + 0.01 or b[3] - b[1] > inner[3] - inner[1] + 0.01:
            log.append(u"NOTE section %s: %.0f x %.0f mm at 1:%d, room %.0f x %.0f mm (kept to scale)" % (
                cid, b[2] - b[0], b[3] - b[1], PS_SCALE, inner[2] - inner[0], inner[3] - inner[1]))
        dx = (inner[0] + inner[2]) / 2.0 - (b[0] + b[2]) / 2.0
        dy = inner[1] - b[1]
        pg.items += xform(sec.items, 1.0, dx, dy)
    log.append(u"sections (v10): W1-W4 at 1:%d on the booklet page, looking downstream" % PS_SCALE)
    return pg, boxes

# ================================================================ v10 key map strip: the four cuts of this page (WO-T3b-3)
# v10 (package C "Page 13": "today it sits inside section 1's box, so it reads as belonging to that drawing only"):
# the key map is a strip across the top of the page block, outside every section's panel, inside ps_all. It shows ONLY
# page 13's four cut lines W1-W4 (basemap_cut_items with basemap_cut_ids, D11 / brief: each key map its own cuts) on
# the shared basemap in mode "topographic", each labelled with the badge and name of its section title. A key map, so
# no scale bar (SCRIPT_STANDARD §8); the frame axis turned horizontal, upstream on the left, a north arrow. The two
# bridges (site board data/DIAG_SRC.py BRIDGES_K) name the places; PS_KEY_SELINOS (agriculture data/GEO.py
# "selinos", survey m) orients the bridge bars and is the stream when no basemap.json exists yet.
PS_KEY_BRIDGES = [("k4", u"K4 köprüsü", (29846.40, 32277.71)),
                  ("k5", u"Üç Kemer Köprüsü", (30293.63, 31792.25))]
PS_KEY_H = 50.0                       # print mm: the strip's height on the booklet page
PS_KEY_MARGIN = (60.0, 46.0)          # m around the four cuts in the turned frame (along, across)
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


def ps_key_unturn(q):
    """key map m -> survey m (the inverse of ps_key_turn)"""
    a = math.radians(PS_KEY_TURN)
    return (q[0] * math.cos(a) + q[1] * math.sin(a), -q[0] * math.sin(a) + q[1] * math.cos(a))


def ps_clip_ring(ring, R):
    """a ring cut to the rectangle R (x0, y0, x1, y1) (Sutherland-Hodgman); [] when nothing is left"""
    x0, y0, x1, y1 = R
    out = list(ring)
    for e in range(4):
        if not out:
            break
        inp, out = out, []
        for i in range(len(inp)):
            p, q = inp[i - 1], inp[i]
            ip = (p[0] >= x0, p[0] <= x1, p[1] >= y0, p[1] <= y1)[e]
            iq = (q[0] >= x0, q[0] <= x1, q[1] >= y0, q[1] <= y1)[e]
            if ip != iq:
                if e < 2:
                    xe = x0 if e == 0 else x1
                    out.append((xe, p[1] + (q[1] - p[1]) * (xe - p[0]) / (q[0] - p[0])))
                else:
                    ye = y0 if e == 2 else y1
                    out.append((p[0] + (q[0] - p[0]) * (ye - p[1]) / (q[1] - p[1]), ye))
            if iq:
                out.append(q)
    return out if len(out) >= 3 else []


def ps_clip_line(pts, R):
    """a polyline cut to the rectangle R: the pieces inside (Liang-Barsky per segment)"""
    x0, y0, x1, y1 = R
    runs, cur = [], []
    for p, q in zip(pts[:-1], pts[1:]):
        dx, dy = q[0] - p[0], q[1] - p[1]
        t0, t1, ok = 0.0, 1.0, True
        for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
            if pp == 0:
                if qq < 0:
                    ok = False
                    break
                continue
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if cur:
                runs.append(cur)
            cur = []
            continue
        a, b = (p[0] + dx * t0, p[1] + dy * t0), (p[0] + dx * t1, p[1] + dy * t1)
        if not cur or t0 > 0.0:
            if cur:
                runs.append(cur)
            cur = [a]
        cur.append(b)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return [r for r in runs if len(r) >= 2]


def ps_key_strip(pg, area, log):
    """v10: the key map strip in area (x0, y0, x1, y1), print mm: frame, title row with the north arrow, the
    topographic basemap cut to the map window, the bridges, page 13's four cuts W1-W4 (triangles point the way each
    section looks: downstream), each with its section's badge and name. Returns the area."""
    x0, y0, x1, y1 = area
    pad, ls, ts = 2.5, PS_LBL, PS_NOTE
    pg.poly([rect(x0, y0, x1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    pg.poly([rect(x0, y1 - 0.8, x1, y1)], fill=MP["discharge"][1])
    yt = y1 - 0.8 - 1.8 - ts * CAP
    ps_rich_para(pg, x0 + pad, yt + ts * 1.28, x1 - x0 - 20.0,
                 u"**KEY MAP** · the four cuts drawn on this page, upstream to downstream; the triangles point the "
                 u"way each section looks", ts, COL["ink_dark"])
    # north arrow at the title row's right end
    nx, ny = ps_key_turn((0.0, 1.0))
    L = 4.0
    cx, cy = x1 - pad - 3.0, yt + ts * CAP / 2.0
    tail, tip = (cx - nx * L / 2.0, cy - ny * L / 2.0), (cx + nx * L / 2.0, cy + ny * L / 2.0)
    hd = 0.3 * L
    pg.line([tail, tip], COL["ink"], 0.3)
    pg.poly([[tip, (tip[0] - nx * hd - ny * hd * 0.45, tip[1] - ny * hd + nx * hd * 0.45),
              (tip[0] - nx * hd + ny * hd * 0.45, tip[1] - ny * hd - nx * hd * 0.45)]], fill=COL["ink"])
    pg.text(u"N", tip[0] - 1.2, tip[1] - ls * CAP / 2.0, ls, COL["ink"], bold=True, align="R")
    # the map window: the four cuts in the turned frame plus PS_KEY_MARGIN, widened to fill the strip
    R = (x0 + pad, y0 + pad, x1 - pad, yt - 0.25 * ts - 1.5)
    ids = [cid for _, cid, _, _, _ in PS_CUTS]
    cuts = basemap_cut_ids(ids, looks=dict((cid, -1) for cid in ids))   # the viewer looks downstream: SW on the right
    tq = [ps_key_turn(p) for c in cuts for p in c[:2]]
    wx0, wx1 = min(q[0] for q in tq) - PS_KEY_MARGIN[0], max(q[0] for q in tq) + PS_KEY_MARGIN[0]
    wy0, wy1 = min(q[1] for q in tq) - PS_KEY_MARGIN[1], max(q[1] for q in tq) + PS_KEY_MARGIN[1]
    km = min((R[2] - R[0]) / (wx1 - wx0), (R[3] - R[1]) / (wy1 - wy0))      # print mm per m
    mx, my = (wx0 + wx1) / 2.0, (wy0 + wy1) / 2.0
    wx0, wx1 = mx - (R[2] - R[0]) / km / 2.0, mx + (R[2] - R[0]) / km / 2.0
    wy0, wy1 = my - (R[3] - R[1]) / km / 2.0, my + (R[3] - R[1]) / km / 2.0
    frame = [ps_key_unturn(q) for q in ((wx0, wy0), (wx1, wy0), (wx1, wy1), (wx0, wy1))]

    def T(p):                                                  # survey m -> print mm
        q = ps_key_turn(p)
        return (R[0] + (q[0] - wx0) * km, R[1] + (q[1] - wy0) * km)

    def fill_fn(rings, hx, alpha, nonzero):
        rr = [r_ for r_ in (ps_clip_ring(r, R) for r in rings) if r_]
        if rr:
            pg.poly(rr, fill=hx, alpha=(alpha if alpha is not None and alpha < 0.975 else None))

    def line_fn(pts, hx, w, dash, alpha):
        for piece in ps_clip_line(pts, R):
            pg.line(piece, hx, w, dash=list(dash) if dash else None)
    taken = []

    def text_fn(s, xy, size, hx, bold, align):
        w = text_w(s, size, bold)
        pg.text(s, xy[0], xy[1] - size * CAP / 2.0, size, hx, bold=bold, align="C")
        taken.append((xy[0] - w / 2.0, xy[1] - size * 0.6, xy[0] + w / 2.0, xy[1] + size * 0.6))
    bx = (min(p[0] for p in frame), min(p[1] for p in frame), max(p[0] for p in frame), max(p[1] for p in frame))
    items = basemap_items("topographic", box=bx)
    if items:
        basemap_draw(items, T, fill_fn, line_fn)
    else:                                                      # no basemap.json yet: the stream line only
        log.append(u"NOTE key map: no basemap (run the site board once); the stream line alone is drawn")
        line_fn([T(p) for p in PS_KEY_SELINOS], COL["river"], 0.8, None, 1.0)
    # the bridges: short bars across the stream, named
    lab = []
    for _, nm, p in PS_KEY_BRIDGES:
        _, (dx, dy) = ps_key_chain(p)
        tx, ty = ps_key_turn((dx, dy))
        c = T(p)
        a_, b_ = (c[0] - ty * 1.6, c[1] + tx * 1.6), (c[0] + ty * 1.6, c[1] - tx * 1.6)
        pg.line([a_, b_], COL["ink"], 0.6, cap=0)
        taken.append((min(a_[0], b_[0]) - 0.3, min(a_[1], b_[1]) - 0.3, max(a_[0], b_[0]) + 0.3, max(a_[1], b_[1]) + 0.3))
        lab.append((c, nm, False, None))
    # page 13's cuts only, then each cut's badge and name as in its section title
    ci = basemap_cut_items(cuts, 1000.0 / km, frame=frame, inset_mm=0.6, tri_mm=1.6, text_mm=ls, col=COL["accent"])
    basemap_draw(ci, T, fill_fn, line_fn, text_fn)
    segs = []
    for it in ci:
        if it[0] == "line":
            P = [T(p) for p in it[1]]
            segs += list(zip(P[:-1], P[1:]))
    for (key, cid, n, name, _), c in zip(PS_CUTS, cuts):
        m = ((c[0][0] + c[1][0]) / 2.0, (c[0][1] + c[1][1]) / 2.0)
        lab.append((T(m), u"%s · %s" % (cid, name), True, n))
    lab.append((T(PS_KEY_SELINOS[int(len(PS_KEY_SELINOS) * 0.8)]), u"Selinos", False, None))
    r = 1.6
    items_l = []
    for c, s_, bold, n in lab:
        w = text_w(s_, ls, bold) + (2 * r + 0.8 if n else 0.0)
        hb = 2 * r if n else 0.0
        items_l.append(dict(x=c[0], y=c[1], rank=0 if n else 1,
                            wh=lambda f, w_=w, h_=hb: (w_ * f, max(ls * f * (CAP + 0.25), h_))))
    got = place_labels_all(items_l, taken, R, segs, sizes=(1.0,), pad=0.6)
    for i, (c, s_, bold, n) in enumerate(lab):
        if i not in got:
            log.append(u"NOTE key map: label '{}' left out (no free place)".format(s_))
            continue
        b, leader, _ = got[i]
        if leader:
            pg.line([c, lp_leader_end(b, c)], COL["ink2"], 0.15)
        tx_ = b[0]
        if n:
            ps_badge(pg, b[0] + r, (b[1] + b[3]) / 2.0, n, r)
            tx_ += 2 * r + 0.8
        yb = (b[1] + b[3]) / 2.0 - ls * CAP / 2.0
        pg.text(s_, tx_, yb, ls, COL["ink_dark"] if bold else COL["ink2"], bold=bold)
    log.append(u"key map (v10): strip across the top of ps_all, about 1:{:,.0f}; cuts W1-W4 only".format(1000.0 / km))
    return area

# ================================================================ A3 booklet = crops of this sheet (v5, booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own sections (SHEET_BOXES, set by build_sheet).
# v7 (Aras 27 Oct 11:07: p.18-19 merged into one page): ps_all = the whole 2 x 2 block (titles, notes, the four
# sections) shaped like the booklet's panel area, for ONE booklet page; the four single crops stay (note + sketch,
# tight; the title is the booklet caption).
BK_SOURCES = [("rhs_lavender", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter)",
               u"https://www.rhs.org.uk/Advice/profile?pid=127"),
              ("ecocrop_olive", u"FAO Ecocrop, Olea europaea (will not tolerate waterlogged soils)",
               u"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1553"),
              # v9 (MIRAQUA 28 Oct, F5): the public page behind SRC_KEY plane (v10: the hamam is no longer drawn)
              ("icomos_2014", u"ICOMOS 2014, Evaluation No 1457, Pergamon and its Multi-Layered Cultural Landscape",
               u"https://whc.unesco.org/document/152724")]
# v10: ps_all = page 13 (key map strip + the four sections at 1:500, scale_den set so the booklet prints "1:500");
# the single crops are the four panels (unused by the booklet today, kept for other pages)
BK_CROPS = [("ps_all", "all", u"Proposal sections W1-W4, upstream to downstream, each looking downstream"),
            ("ps_upstream", "up", u"W1 · Upstream entry, looking downstream"),
            ("ps_k4", "k4", u"W2 · K4 walking hub, looking downstream"),
            ("ps_k5", "k5", u"W3 · K5 Demeter's Garden, looking downstream"),
            ("ps_downstream", "down", u"W4 · Downstream reach, looking downstream")]
BK_DROP = [u"^\\[\\d+\\]$"]                           # the sheet's source numbers: the booklet has its own source list


def _ps_mix(a, b, t):
    """hex a seen at opacity t over hex b"""
    A, B = hex_rgb(a), hex_rgb(b)
    return "%02X%02X%02X" % tuple(int(round(255.0 * (B[i] + (A[i] - B[i]) * t))) for i in range(3))


def booklet_export(log):
    """booklet/blocks.json: one crop per section of the sheet + ps_all (rect in mm from the sheet's top-left, y down)."""
    bk = BkBlocks(OUT_DIR, GH_LABEL, VERSION)
    for k, t, u in BK_SOURCES:
        bk.source(k, t, u)
    bk.d["sheet_sources"] = {"0": [u"[{}] {}".format(i + 1, v) for i, (_, v) in enumerate(ps_sources())]}   # v7: the booklet's sources page
    # v10: drawn samples of what the sections draw (fills as they show on white; hatches by their ground colour)
    legend = [dict(kind="fill", colour=_ps_mix(PS_FLOOD, "FFFFFF", PS_FLOOD_A), label=u"reach of the 500-year flood (Q500)"),
              dict(kind="dash", colour=COL["river_mid"], label=u"Q500 (dashed) and Q100 (dotted) water levels"),
              dict(kind="fill", colour=SEC["channel"], label=u"summer strip, basin water"),
              dict(kind="fill", colour=SCT["stone"], label=u"stone: DSİ walls, steps, garden wall"),
              dict(kind="fill", colour=SCT["concrete"], label=u"concrete: basins, floors"),
              dict(kind="fill", colour=SCT["earth"], label=u"earth"),
              dict(kind="fill", colour=SCT["gravel"], label=u"gravel bed"),
              dict(kind="fill", colour=PS_TIMBER, label=u"timber boardwalk"),
              dict(kind="fill", colour=COL["accent"], label=u"proposal (labels), cut lines on the key map")]
    for bid, key, cap in BK_CROPS:
        if key not in SHEET_BOXES:
            log.append(u"booklet %s: section %s not on the sheet" % (bid, key))
            continue
        x0, y0, x1, y1 = SHEET_BOXES[key]
        bk.crop(bid, OUT_NAME.format("A"), (x0, BOARD_H - y1, x1, BOARD_H - y0), caption=cap,
                scale_den=PS_SCALE * BK_S, legend=legend, drop=BK_DROP)
    return bk.save()


# ================================================================ the sheet (v10: one block = booklet page 13)
# v7 (Aras 27 Oct 11:07): one block shaped like the booklet's panel area, so the booklet shows it whole (crop ps_all)
# on ONE A3 page at the factor BK_S. v10 (WO-T3b-3): the block is drawn in booklet print mm (parts/70_sections.py:
# the key map strip across the top, the four sections W1-W4 at 1:500 in a 2 x 2 under it) and placed here at 1 / BK_S,
# so ps_all prints every section at exactly 1:500.
SHEET_BOXES = {}                                      # key -> crop box (x0, y0, x1, y1), mm, y up; set by build_sheet
# The booklet's panel area (bergama_booklet code.py: AREA = 392 x 243 mm, less the 5 mm caption band CAP_H)
BK_W, BK_H = 392.0, 238.0
GRID_W = BOARD_W - 2 * M                              # the block on the A0 sheet, mm
GRID_H = GRID_W * BK_H / BK_W                         # same shape as the booklet area: it fills the page, never stretched
BK_S = BK_W / GRID_W                                  # booklet print factor of ps_all (0.338)


def build_sheet(opt, log):
    """v10: the page-13 block (key map strip + the four sections at 1:500) on one A0 landscape sheet."""
    pg = Page(BOARD_W, BOARD_H)
    pg.poly([rect(0, 0, BOARD_W, BOARD_H)], fill=COL["sheet"])
    X0, X1 = M, BOARD_W - M
    top = BOARD_H - M
    pg.text(u"The Proposals in Section", X0, top - 12.0, 12.0, COL["ink_dark"], bold=True)
    pg.text(u"four cuts W1-W4, upstream to downstream, each looking downstream · the block below is booklet page 13",
            X0, top - 18.0, 3.6, MP["discharge"][2], bold=True)
    y1 = top - 22.0
    pg.line([(X0, y1), (X1, y1)], COL["structure"], 0.3)
    gy1 = y1 - 4.0
    gy0 = gy1 - GRID_H
    blk, boxes = ps_block(log)
    s = 1.0 / BK_S
    pg.items += xform(blk.items, s, X0, gy0)
    for key, b in boxes.items():                      # single crops: one section panel each
        SHEET_BOXES[key] = (X0 + s * b[0], gy0 + s * b[1], X0 + s * b[2], gy0 + s * b[3])
    SHEET_BOXES["all"] = (X0, gy0, X0 + GRID_W, gy1)  # ps_all: the whole block = page 13
    log.append(u"sources: " + u"  ".join(u"[{}] {}".format(i + 1, v) for i, (_, v) in enumerate(ps_sources())))
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
