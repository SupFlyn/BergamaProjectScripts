# -*- coding: utf-8 -*-
"""BERGAMA PROPOSAL SECTIONS v4 (2026-10-25): Group 6's four proposals in section, upstream to downstream, in the
water board's hand-drawn section style (Aras 25 Oct 11:38-11:45: "we want section from each proposal just like our
water board sections"; "the style of waterboard sections were really really good you can do it somewhere else").
For the studio session of 26.10.2026: "Sections: Illustrating the spatial relationships and key design decisions."

NEW IN (revision 30 Oct, T6, booklet p12; the version number is set at the end of the revision):
  * D6: the block sits on the A0 sheet at exactly 1:200 (BK_S = 0.4), so the booklet prints it at 1:500 and its scale
    bars read 1:500 (they read 1:1,481: the sheet's words said 1:500 at a non-standard sheet factor).
  * M7 figures at 1.75 m doing what each zone is for, M6 species at sourced heights in mixed wet-to-dry planting, the
    G6 ratios checked (sf_assert_g6, log), the M5 water at average yearly flow with Q100 / Q500, stepping stones.
  * W1: a stone stair down the NE wall into the bed, life in the wet bed, an edge walk and a bike lane. W2: walk, bike
    lane, tree band, people on the steps and at the water. W3: a mixed wet edge up to the commons, herbs at the
    garden wall. W4: crest walk, bike lane and tree corridor, a ramp on a berm to a viewing terrace above Q500, steps
    to the boardwalk. Faded trees behind every cut (R16). Key map on the M4 base with the study area.
  * D1: two sheets from one geometry: Bergama_proposal_sections_A.pdf (style b, vector) and ..._A_style_a.pdf (style
    a, cutouts from Downloads/Bergama/Data/cutouts/); crops suffixed _a / _b (unsuffixed = b). Legend inside ps_all.
    v13 (Aras 31 Oct, booklet p12): style a only, ONE sheet Bergama_proposal_sections_A.pdf, plain crop ids.
NEW IN v14 (round 2 critique, Aras 31 Oct, booklet p12; R2-A modules): nobody in the water except on stepping stones,
  back trees on the cut ground and never over the water, mixed planting groups on depth layers, designed sky, all
  labels as "Element: reason" callouts with one purpose callout per planting group, the Q500 wash gone (lines stay).
NEW IN v15 (Aras 31 Oct 12:01): W1 redrawn to p.17 F1's layout (path and bike lane under the trees SW, view terrace
  on the NE wall top, reed basins beyond), a way down by sitting steps in three flights with planted landings to a
  railed floor at the water's edge (no straight stair), no blocks in the bed; background houses behind W1-W4; people as
  scenes facing the water.
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
VERSION = "v15"
GH_LABEL = "ProposalSections"
OUT_FOLDER = "bergama_proposal_sections"
LOG_NAME = "bergama_proposal_sections_log.txt"
OUT_NAME = "Bergama_proposal_sections_{}.pdf"
STYLES = (("a", "A"),)                                # v13 (Aras 31 Oct): style a only, one sheet ..._A.pdf

#@include ../common/bergama_paths.py
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

#@include ../common/hex_rgb.py

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}

_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"

#@include ../common/pdf_str.py

#@include ../common/_f.py

#@include ../common/page_stream.py

#@include ../common/_text_ops.py

#@include ../common/pdf_fonts.py


#@include ../common/write_pdf.py

# ---------------------------------------------------------------- composing the board from drawn parts
# v10: the page block is drawn in booklet print mm and placed on the board at 1 / BK_S (xform). Text, lines and
# dashes scale with it, as a reduced print does.
#@include ../common/items_bbox.py

#@include ../common/xform.py

# ---------------------------------------------------------------- drawing helpers (page mm, y up)
#@include ../common/rect.py

# ---------------------------------------------------------------- shared modules (revision 29 Oct, T2a / T2b)
# v10: the level table (data first), the section parts before the plants, the figures (M7, through ps_fig
# and ps_people), the basemap for the key map. Names checked: no module name is defined by this script.
#@include ../common/data/LEVELS.py

#@include ../common/levels.py

#@include ../common/section_parts.py

#@include ../common/plants.py
#@include ../common/hires.py

#@include ../common/figures.py

#@include ../common/basemap.py
#@include ../common/grid.py
#@include ../common/buildings.py


# ---------------------------------------------------------------- the board (A0 landscape, one page)
#@include ../common/load_palette.py

DATA_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data")   # 25 Oct: every data file here

# v10: the sketch engine and data/SKETCH_SRC.py are no longer included (the sections are drawn to the level table in
# parts/70_sections.py); data/SKETCH_SRC.py stays in the repo because bergama_agriculture_alternatives includes it.
#@include ../common/booklet_assets.py

#@include ../common/label_place.py
#@include ../common/water.py
#@include ../common/section_frame.py

#@include parts/70_sections.py

#@include parts/80_key_map.py

#@include parts/90_booklet.py


# ================================================================ the sheet (v10: one block = booklet page 13)
# v7 (Aras 27 Oct 11:07): one block shaped like the booklet's panel area, so the booklet shows it whole (crop ps_all)
# on ONE A3 page at the factor BK_S. v10 (WO-T3b-3): the block is drawn in booklet print mm (parts/70_sections.py:
# the key map strip across the top, the four sections W1-W4 at 1:500 in a 2 x 2 under it) and placed here at 1 / BK_S,
# so ps_all prints every section at exactly 1:500.
SHEET_BOXES = {}                                      # style -> {key -> crop box (x0, y0, x1, y1), mm, y up}; build_sheet
# The booklet's panel area (bergama_booklet code.py: AREA = 392 x 243 mm, less the 5 mm caption band CAP_H); revision
# 30 Oct: a little under it (390 x 234), so 1:500 fits whatever the grid takes, the legend inside the block
BK_W, BK_H = 390.0, 234.0
BK_S = 0.4                                            # booklet print factor of ps_all: the sheet at 1:200 prints 1:500
GRID_W = BK_W / BK_S                                  # the block on the A0 sheet, mm (975 x 585)
GRID_H = BK_H / BK_S


def build_sheet(opt, log, style="b"):
    """v10: the page-12 block (key map strip + the four sections at 1:500 on the booklet, 1:200 here) on one A0
    landscape sheet, in style b (vector) or a (cutouts, D1)."""
    pg = Page(BOARD_W, BOARD_H)
    pg.poly([rect(0, 0, BOARD_W, BOARD_H)], fill=COL["sheet"])
    X0, X1 = M, BOARD_W - M
    top = BOARD_H - M
    pg.text(u"The Proposals in Section", X0, top - 12.0, 12.0, COL["ink_dark"], bold=True)
    pg.text(u"four cuts W1-W4, upstream to downstream, each looking downstream · 1:200 on this sheet",
            X0, top - 18.0, 3.6, MP["discharge"][2], bold=True)
    y1 = top - 22.0
    pg.line([(X0, y1), (X1, y1)], COL["structure"], 0.3)
    gy1 = y1 - 4.0
    gy0 = gy1 - GRID_H
    blk, boxes = ps_block(log, style)
    s = 1.0 / BK_S
    pg.items += ps_xform(blk.items, s, X0, gy0)
    sb = SHEET_BOXES.setdefault(style, {})
    for key, b in boxes.items():                      # single crops: one section panel each
        sb[key] = (X0 + s * b[0], gy0 + s * b[1], X0 + s * b[2], gy0 + s * b[3])
    sb["all"] = (X0, gy0, X0 + GRID_W, gy1)           # ps_all: the whole block = page 12
    log.append(u"sources: " + u"  ".join(u"[{}] {}".format(i + 1, v) for i, (_, v) in enumerate(ps_sources())))
    return pg



def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    log = []
    pal = load_palette([DATA_DIR], log)
    lines = []
    for opt in OPTIONS:
        for style, part in STYLES:                    # revision 30 Oct (D1): one sheet per style, same geometry
            t1 = time.time()
            pg = build_sheet(opt, log, style)
            path = os.path.join(OUT_DIR, OUT_NAME.format(part))
            try:
                write_pdf(pg, path, u"Bergama proposal sections {} {} style {}".format(VERSION, opt, style))
            except (IOError, OSError):
                path = path.replace(".pdf", datetime.datetime.now().strftime("_%H%M%S.pdf"))
                write_pdf(pg, path, u"Bergama proposal sections {} {} style {}".format(VERSION, opt, style))
            lines.append(u"{}  {}  {:.1f} s".format(os.path.basename(path), time.strftime("%H:%M:%S"),
                                                     time.time() - t1))
    log.append(cut_log_line())
    log += [u"PDF images: " + x for x in WP_IMG_LOG[:5]]
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
