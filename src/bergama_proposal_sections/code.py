# -*- coding: utf-8 -*-
"""BERGAMA PROPOSAL SECTIONS v4 (2026-10-25): Group 6's four proposals in section, upstream to downstream, in the
water board's hand-drawn section style (Aras 25 Oct 11:38-11:45: "we want section from each proposal just like our
water board sections"; "the style of waterboard sections were really really good you can do it somewhere else").
For the studio session of 26.10.2026: "Sections: Illustrating the spatial relationships and key design decisions."

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
VERSION = "v7"
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
    ("garden", u"card i01: Demeter's Garden, page and crop list (zones DG 1-2)"),
    ("zones", u"zone base ZONES.md: WP 1-2 and the floodable boardwalk"),
    ("plants", u"DATA_REGISTER PL-11, PL-12: olive and lavender, waterlogging"),
    ("gauges", u"DSİ gauge yearbooks 2016-2021"),
    ("survey", u"main survey: road edges YOL_SOSE"),
    ("plane", u"plane trees at the dry hub squares: decision D8 (Ottoman squares with plane trees, ICOMOS s13 p281, "
              u"card h02); drought-sensitive, so irrigated from storage (card h03 Q4)"),
    ("hamam", u"card h02 E08 (s32, s63): Tabaklar Hamamı on the right bank opposite Ulu Cami, survey labels at "
              u"(29890, 32244); K4 at (29846, 32278): about 56 m apart (calculated)"),
    ("hubs", u"history decisions D10 + Aras 27 Oct 12:05: K4 and K5 are walking hubs, a dry step-free square above "
             u"Q500 and a floodable sub-hub in the bed at the strip level"),
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


def cell(pg, box, title, note_txt, ts, ns):
    """v7: one section's panel: white ground, a coloured rule on top, the title (ts mm) and one short note (ns mm)
    under it, both measured (wrap). Returns (drawing box under the note, right end of the note), mm."""
    x0, y0, x1, y1 = box
    pg.poly([rect(x0, y0, x1, y1)], fill=COL["white"], stroke=COL["faint"], lw=0.25)
    pg.poly([rect(x0, y1 - 1.2, x1, y1)], fill=MP["discharge"][1])
    pg.text(title, x0 + 5.0, y1 - 1.2 - 3.0 - ts * CAP, ts, COL["ink_dark"], bold=True)
    top = y1 - 1.2 - 3.0 - ts * (CAP + 0.25) - 3.0     # under the title row (the single crops start here)
    w = x1 - x0 - 10.0
    yn = para(pg, x0 + 5.0, top, w, note_txt, ns, COL["ink"])
    nr = x0 + 5.0 + max(text_w(ln, ns) for ln in wrap(note_txt, ns, w))
    return (x0 + 5.0, y0 + 4.0, x1 - 5.0, yn - 0.25 * ns - 4.0), top, nr


# ---------------------------------------------------------------- W3a  concept sections (pr1 v3.1 idea sketches)
# SKETCH_SRC (end of this file) is pr1's sketch code; it runs in its own namespace and draws page items in pr1's
# order. The element numbers come from node() of this board.
_SK = []

#@include ../common/sketch_engine.py

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
#@include ../common/load_palette.py

DATA_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data")   # 25 Oct: every data file here

# ================================================================ embedded engines
# SKETCH_SRC: pr1_drawings v3.1's concept sketches (SKETCH style) with a page-item layer instead of Rhino baking;
# owner names, working-area bars and figures printed elsewhere taken out (24 Oct). Run by sketch_engine().
#@include data/SKETCH_SRC.py

#@include ../common/booklet_assets.py

#@include parts/90_booklet.py


# ================================================================ the sheet (v7: one 2 x 2 block = one booklet page)
# v7 (Aras 27 Oct 11:07 "p18-19: merge into one page"; spec §5 q3): the four sections sit in one 2 x 2 block whose
# shape is the booklet's panel area, so the booklet shows the whole block (crop ps_all) on ONE A3 page at one factor;
# every section is placed at ONE common factor (the sketches carry relative levels, so the booklet prints no scale).
# Titles short, one short note under each title, no source footer (the [n] key goes to the log).
PROPOSALS = [("up", u"1 · UPSTREAM ENTRY",
              u"Winter runoff: cleaned in reed basins, held in the terrace basins, given back in summer as the strip"),
             ("k4", u"2 · K4 BRIDGE · WALKING HUB",
              u"Q500 tops today's bank: dry hub square above it, floodable sub-hub in the bed, steps between"),
             ("k5", u"3 · K5 BRIDGE · DEMETER'S GARDEN + WALKING HUB",
              u"Bank tops stay dry: garden and hub square · bed: stream commons = sub-hub, floods in winter"),
             ("down", u"4 · DOWNSTREAM REACH",
              u"Clean water arrives from upstream: floodable planting + boardwalk, surplus to farmland")]
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
    for key, _, _ in PROPOSALS:
        bx = boxes[key]
        b = items_bbox(parts[key].items)
        dx = (bx[0] + bx[2]) / 2.0 - s * (b[0] + b[2]) / 2.0     # centred across, at the top of its box
        dy = bx[3] - s * b[3]
        pg.items += xform(parts[key].items, s, dx, dy)
        tp, nr = heads[key]                           # single crop: note + sketch, tight (the title is the caption)
        SHEET_BOXES[key] = (min(bx[0], dx + s * b[0]) - 2.0, dy + s * b[1] - 3.0,
                            max(nr, dx + s * b[2]) + 2.0, tp)
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
