# -*- coding: utf-8 -*-
"""BERGAMA PROPOSAL SECTIONS v4 (2026-10-25): Group 6's four proposals in section, upstream to downstream, in the
water board's hand-drawn section style (Aras 25 Oct 11:38-11:45: "we want section from each proposal just like our
water board sections"; "the style of waterboard sections were really really good you can do it somewhere else").
For the studio session of 26.10.2026: "Sections: Illustrating the spatial relationships and key design decisions."

NEW IN v5 (Aras 25 Oct 21:47-21:51, booklet/CROP_SPEC.md): the booklet shows this sheet's own four sections:
  booklet/blocks.json lists one crop per section (the drawing box each panel frame leaves under its title and chips,
  kept in SHEET_BOXES); the separate booklet redraw (parts/90_booklet.py drawers, c4_s1..c5_s2.pdf) is gone. Sheet
  words: the Selinos is a stream (never river), no caveat notes ("schematic", "not to scale", ": not designed",
  "route not designed", "volume: not in the idea", "bridge not modelled"), no personal name inside the K5 drawing.
  Layout and look unchanged.
NEW IN v4 (A3 booklet, SCRIPT_STANDARD §8; booklet/STAGE2_BRIEF.md): after the sheet, booklet_export() writes
  output/bergama_proposal_sections/booklet/: c4_s1, c4_s2, c5_s1, c5_s2 .pdf (the four sections re-laid natively for
  the booklet's 392 x 111 mm frames, same hand-sketch engine, no text inside) + blocks.json (every word a label from the
  plan's list; no personal names, no flood heights: Q500 a named level line). The sheet is unchanged.
NEW IN v3 (Aras 25 Oct 17:00, SCRIPT_STANDARD §5b visual first; audit batch_2026-10-25_visual_first/VISUAL_AUDIT.md §1):
  sentence callouts in the sketches -> short keyword callouts with hand pictograms (winter cloud, summer sun,
  fail-safe mark); garden crops as two season rows; sheet subtitle -> keyword row with the 1-11 flow; panel
  subtitles -> keyword chips with pictograms; source notes -> [n] marks with one numbered key in the footer;
  the four "Schematic section..." notes -> one header tag. Fix (audit accuracy problem 3): the upstream Q500
  label said "lowest terrace floods"; the surveyed ARAS cut keeps Q500 inside the banks (rain_river_levels
  README v1.1 line 21: 3.30 m (+73.66), "inside; the cut is about 5 m deep"), so it now reads
  "Q500 +73.66 m · 3.30 m" and the terrace floods only if set below it. Layout, colours and frames unchanged.
NEW IN v2 (Aras 25 Oct 16:43: "the selection of A should be remember in the whole project so all scripts should drop B alternatives"): option A only, so one sheet per press. Nothing else changed.

WHAT IT DRAWS: one A0 landscape sheet per form option (A = organic only where the project meets the water, B = no
organic forms), all vector, whole-string text, four panels:
  1 UPSTREAM ENTRY · collect, clean and hold   reed-basin cascade (water board v1.3's sketch, unchanged)
  2 K4 BRIDGE · amphibious heritage threshold  tiers W / F / D (water board v1.3's sketch, unchanged)
  3 K5 BRIDGE · Demeter's Garden (idea: Begum) NEW: garden on the dry top of the south-west bank (card i01, DG 1-2)
  4 DOWNSTREAM REACH · give back               NEW: floodable planting WP 1-2 and the floodable boardwalk (ZONES.md)
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
VERSION = "v5"
GH_LABEL = "ProposalSections"
OUT_FOLDER = "bergama_proposal_sections"
LOG_NAME = "bergama_proposal_sections_log.txt"
OUT_NAME = "Bergama_proposal_sections_{}.pdf"

BERGAMA = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA, "logs")


BOARD_W, BOARD_H = 1189.0, 841.0     # A0 landscape, mm

M = 14.0                             # board margin, mm

OPTIONS = ("A",)                     # v2: option A only (organic only where the project meets the water), Aras 16:43

CREDIT = u"Group 6 · Aras Özkaymakcı · Begüm Arslan · Nil Çetin"

COURSE = u"ARCH 4410 Architectural Design Studio V · Yaşar University · Fall 2026"

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
RR = u"rain_river_levels/README"

CR = u"CONCEPT_RECORD v2.4"

# v3: sources as [n] on the drawings, the numbered key in the footer (water board v1.6 cite() / SRC_KEY). Fixed
# order, so the numbers stay the same on every press.
SRC_KEY = [
    ("levels", RR + u" v1.1 table: levels calculated on the surveyed stream-height cuts (Manning, main survey TIN)"),
    ("rain", u"water_data/README: MGM 17742 normals 1991-2020, seasonal shares of the year's rain (arithmetic)"),
    ("concept", CR + u" (Q1: east channel wall kept, default)"),
    ("tiers", u"Aras's concept text: tiers, level 1 / 2 / 3"),
    ("garden", u"card i01: Demeter's Garden, Begüm's idea, page and crop list (zones DG 1-2)"),
    ("zones", u"zone base ZONES.md: WP 1-2 and the floodable boardwalk"),
    ("plants", u"DATA_REGISTER PL-11, PL-12: olive and lavender, waterlogging"),
    ("gauges", u"DSİ gauge yearbooks 2016-2021"),
    ("survey", u"main survey: road edges YOL_SOSE"),
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

#@include ../common/wrap.py

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

#@include ../common/hex_rgb.py

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}

_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"

#@include ../common/pdf_str.py

#@include ../common/_f.py

#@include ../common/page_stream.py

#@include ../common/_text_ops.py

#@include ../common/write_pdf.py

#@include ../common/_tree_rand.py

# ---------------------------------------------------------------- composing the board from drawn parts
# Every drawing is drawn on its own Page at its natural size (page mm), then placed on the board at one uniform
# scale that fits its box (place). Text, lines and dashes scale with it, as a reduced print does.
#@include ../common/items_bbox.py

#@include ../common/xform.py

#@include ../common/place.py

# ---------------------------------------------------------------- drawing helpers (page mm, y up)
#@include ../common/rect.py

#@include ../common/node.py

#@include ../common/para.py

def flow_arrow(pg, x0, x1, y, col, lw=0.3, head=1.2):
    """v3: a straight arrow from x0 to x1 at height y (the keyword row's links)."""
    pg.line([(x0, y), (x1 - head * 0.8, y)], col, lw)
    pg.poly([[(x1, y), (x1 - head, y + head * 0.45), (x1 - head, y - head * 0.45)]], fill=col)


def pict(pg, kind, x, y, sz):
    """v3: a small pictogram in the square (x, y - sz)-(x + sz, y), on a 10 x 10 grid (after water board v1.6
    icon()). Graphic only."""
    u = sz / 10.0
    lw = 0.07 * sz
    ink, ink2 = COL["ink_dark"], COL["ink2"]
    w1, w2, w3 = MP["discharge"][0], MP["discharge"][1], MP["discharge"][2]

    def P(pts):
        return [(x + a * u, y - sz + b * u) for a, b in pts]

    def R(a0, b0, a1, b1):
        return P([(a0, b0), (a1, b0), (a1, b1), (a0, b1)])

    def drop(a, b, r, col):
        pg.poly([P([(a - r * 0.85, b + r * 0.45), (a, b + r * 2.2), (a + r * 0.85, b + r * 0.45)])], fill=col)
        pg.circle(x + a * u, y - sz + b * u, r * u, fill=col)
    if kind == "reed":
        pg.poly([R(0, 0, 10, 2.2)], fill=w2)
        for k_ in range(4):
            a = 1.8 + k_ * 2.1
            t = 6.6 + (k_ % 2) * 2.2
            pg.line(P([(a, 0.8), (a + 0.3, t)]), MP["wetland"][2], lw)
            pg.poly([R(a - 0.25, t - 1.8, a + 0.85, t + 0.2)], fill=MP["agriculture"][1])
    elif kind == "cascade":
        for a, b in ((0.4, 6.4), (3.6, 3.6), (6.8, 0.8)):
            pg.poly([R(a, b, a + 2.8, b + 1.4)], fill=MP["storage"][1])
        pg.line(P([(0.2, 9.4), (0.2, 6.2), (3.4, 6.2), (3.4, 3.4), (6.6, 3.4), (6.6, 0.6), (9.8, 0.6)]), ink, lw)
    elif kind == "strip":
        pg.poly([R(0, 3.6, 10, 6.4)], fill=w2)
        flow_arrow(pg, x + 0.8 * u, x + 9.4 * u, y - sz + 5.0 * u, COL["white"], lw, 1.8 * u)
    elif kind in ("steps", "climb"):
        pg.poly([R(0.4, 0.6, 9.6, 3.0)], fill=w1)
        pg.line(P([(0.2, 0.6), (3.4, 0.6), (3.4, 3.8), (6.6, 3.8), (6.6, 7.0), (9.8, 7.0)]), ink, lw)
        if kind == "climb":                           # the river climbing the steps
            pg.line(P([(1.6, 3.4), (5.0, 7.4)]), w3, lw * 1.2)
            pg.poly([P([(5.6, 8.2), (3.9, 7.3), (5.3, 6.1)])], fill=w3)
    elif kind == "level":                             # a block (the street level) above a dashed flood line
        pg.poly([R(1.0, 6.0, 9.0, 9.4)], fill=COL["structure"])
        for a in (0.4, 3.0, 5.6, 8.2):
            pg.line(P([(a, 3.6), (a + 1.6, 3.6)]), w3, lw)
        pg.poly([P([(4.2, 4.9), (5.8, 4.9), (5.0, 3.6)])], stroke=w3, lw=lw * 0.7)
        pg.poly([R(0.4, 0.4, 9.6, 2.4)], fill=w1)
    elif kind == "bridge":
        arc = [(5 + 4.2 * math.cos(math.pi * i / 16.0), 1.0 + 4.2 * math.sin(math.pi * i / 16.0)) for i in range(17)]
        pg.line(P(arc), ink2, lw)
        pg.line(P([(0.2, 6.8), (9.8, 6.8)]), ink2, lw * 1.4)
        pg.poly([R(0.6, 0.4, 9.4, 1.6)], fill=w1)
    elif kind == "olive":
        pg.poly([R(4.5, 0.4, 5.5, 4.4)], fill=ink2)
        pg.circle(x + 5.0 * u, y - sz + 6.2 * u, 3.4 * u, fill=MP["agriculture"][0])
        for a, b in ((3.8, 6.8), (6.0, 5.4), (5.4, 7.8)):
            pg.circle(x + a * u, y - sz + b * u, 0.5 * u, fill=ink)
    elif kind == "sun":
        for k_ in range(8):
            a = math.radians(k_ * 45.0)
            pg.line(P([(5 + 3.0 * math.cos(a), 5 + 3.0 * math.sin(a)), (5 + 4.6 * math.cos(a), 5 + 4.6 * math.sin(a))]),
                    ink2, lw)
        pg.circle(x + 5.0 * u, y - sz + 5.0 * u, 2.5 * u, fill="E8C64A")
    elif kind in ("drop", "notreat"):
        drop(5.0, 2.8, 2.2, w2)
        if kind == "notreat":
            pg.line(P([(1.2, 8.8), (8.8, 1.2)]), COL["accent"], lw * 1.4)
            pg.line(P([(1.2, 1.2), (8.8, 8.8)]), COL["accent"], lw * 1.4)
    elif kind == "deck":
        pg.poly([R(0.4, 0.4, 9.6, 2.6)], fill=w1)
        pg.poly([R(0.4, 5.4, 9.6, 6.8)], fill=COL["soil_dk"])
        for a in (2.0, 5.0, 8.0):
            pg.line(P([(a, 5.4), (a, 1.0)]), ink2, lw)


def chips(pg, x, ytop, items, size=2.0):
    """v3: keyword chips in one row, each a pictogram and a keyword (the panel subtitles). Returns the right end."""
    ch = size * 1.8
    sz = ch - 0.8
    for kind, lab in items:
        w = 0.5 + sz + 0.8 + text_w(lab, size, True) + 1.2
        pg.poly([rect(x, ytop - ch, x + w, ytop)], fill=COL["lane"], stroke=COL["faint"], lw=0.2)
        pict(pg, kind, x + 0.5, ytop - 0.4, sz)
        pg.text(lab, x + 0.5 + sz + 0.8, ytop - ch / 2 - size * CAP / 2, size, COL["ink"], bold=True)
        x += w + 2.0
    return x


def frame(pg, box, title, sub=None):
    """A drawing's panel on the board: white ground, a coloured rule on top, the title and one line under it.
    v3: sub may be a list of (pictogram, keyword) chips instead of a sentence. Returns the box left for the drawing."""
    x0, y0, x1, y1 = box
    pg.poly([rect(x0, y0, x1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    pg.poly([rect(x0, y1 - 1.2, x1, y1)], fill=MP["discharge"][1])
    pg.text(title, x0 + 4.0, y1 - 7.6, 4.0, COL["ink_dark"], bold=True)
    y = y1 - 9.0
    if isinstance(sub, list):
        chips(pg, x0 + 4.0, y - 0.4, sub)
        y -= 2.6                                      # the same drawing box as a one-line subtitle (layout kept)
    elif sub:
        for ln in wrap(sub, 2.0, x1 - x0 - 8.0)[:2]:
            y -= 2.6
            pg.text(ln, x0 + 4.0, y, 2.0, COL["ink2"])
    return (x0 + 4.0, y0 + 3.0, x1 - 4.0, y - 2.5)

# ---------------------------------------------------------------- W3a  concept sections (pr1 v3.1 idea sketches)
# SKETCH_SRC (end of this file) is pr1's sketch code; it runs in its own namespace and draws page items in pr1's
# order. The element numbers come from node() of this board.
_SK = []

#@include ../common/sketch_engine.py

def draw_concept(which, opt):
    """which: "up", "k4", "k5" or "down" (SKETCH_FN); opt: form A (organic at the water) or B (no curves)."""
    E = sketch_engine()
    E["FORM"] = opt
    del E["ZP"][:]
    E["ORDER"][0] = 0

    def NODE(o, x, y, n):
        tmp = Page(0, 0)
        node(tmp, o[0] + x, o[1] + y, n, opt, 2.6)
        for it in tmp.items:
            E["_put"](it, E["Z_TEXT"])
    E["NODE"] = NODE
    E["CITE"] = cite                                  # v3: source numbers [n] inside the sketches
    E[SKETCH_FN[which]]()
    pg = Page(0, 0)
    pg.items = [it for _, _, it in sorted(E["ZP"], key=lambda e: (e[0], e[1]))]
    return pg

# ---------------------------------------------------------------- the board (A0 landscape, one page)
#@include ../common/load_palette.py

DATA_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data")   # 25 Oct: every data file here

# ================================================================ embedded engines
# SKETCH_SRC: pr1_drawings v3.1's concept sketches (SKETCH style) with a page-item layer instead of Rhino baking;
# owner names, working-area bars and figures printed elsewhere taken out (24 Oct). Run by sketch_engine().
#@include data/SKETCH_SRC.py

#@include ../common/booklet_assets.py

#@include parts/90_booklet.py


# ================================================================ the sheet (v1)
PROPOSALS = [("up", u"1 · UPSTREAM ENTRY · COLLECT, CLEAN AND HOLD",        # v3: subtitles as keyword chips
              [("reed", u"CLEAN · stream + held runoff"), ("cascade", u"STORE · winter water"),
               ("strip", u"SUMMER STRIP")]),
             ("k4", u"2 · K4 BRIDGE · AMPHIBIOUS HERITAGE THRESHOLD",
              [("steps", u"TIERS W / F / D"), ("climb", u"stream may climb the steps"),
               ("level", u"street level above Q500"), ("bridge", u"Roman bridge stays as it is")]),
             ("k5", u"3 · K5 BRIDGE · DEMETER'S GARDEN (idea: Begüm)",
              [("olive", u"PRODUCTIVE HERITAGE GARDEN"), ("sun", u"dry top · south-west bank"),
               ("drop", u"watered by the clean stream")]),
             ("down", u"4 · DOWNSTREAM REACH · GIVE BACK",
              [("reed", u"FLOODABLE PLANTING · clean-stream fed"), ("deck", u"floodable boardwalk"),
               ("notreat", u"no treatment here")])]
SHEET_BOXES = {}                                      # v5: key -> drawing box (x0, y0, x1, y1), mm, y up; set by build_sheet
SKETCH_FN = {"up": "concept_aras_sketch", "k4": "concept_begum_sketch", "k5": "concept_k5_sketch",
             "down": "concept_nil_sketch"}


def build_sheet(opt, log):
    """The four proposals in section on one A0 landscape sheet, upstream to downstream (2 x 2)."""
    pg = Page(BOARD_W, BOARD_H)
    pg.poly([rect(0, 0, BOARD_W, BOARD_H)], fill=COL["sheet"])
    X0, X1, G = M, BOARD_W - M, 4.0
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
    pg.text(u"PanelReview1A · organic forms only where it meets the water" if opt == "A" else
            u"PanelReview1B · no organic forms anywhere", X0, top - 22.5, 2.4, COL["ink"])
    y1 = top - 26.0
    pg.line([(X0, y1), (X1, y1)], COL["structure"], 0.3)
    y0 = M + 16.0
    cw, ch = (X1 - X0 - G) / 2.0, (y1 - G - y0 - G) / 2.0
    for i, (key, ttl, sub) in enumerate(PROPOSALS):
        cx = X0 + (i % 2) * (cw + G)
        cy = y1 - G - (i // 2 + 1) * ch - (i // 2) * G
        b = frame(pg, (cx, cy, cx + cw, cy + ch), ttl, sub)
        SHEET_BOXES[key] = b                          # v5: the section's drawing box = its booklet crop
        place(pg, draw_concept(key, opt), b, 3.0, "C", log, "section " + key)
    t = (u"Sources by number: " + u"  ".join(u"[{}] {}".format(i + 1, v) for i, (_, v) in enumerate(SRC_KEY)) +
         u"  ·  sketch style: water board v1.3")       # v3: the numbered source key (the [n] on the sketches)
    y = para(pg, X0, M + 13.0, X1 - X0, t, 1.9, COL["ink2"])
    pg.text(u"{} · {} · bergama_proposal_sections {}".format(CREDIT, COURSE, VERSION), X0, y - 2.6, 1.9, COL["ink2"])
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
    if _pressed:
        _t0 = time.time()
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
