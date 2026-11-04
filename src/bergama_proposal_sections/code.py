# -*- coding: utf-8 -*-
# CURRENT VERSION: bergama_proposal_sections_v21.py = v21 (4 Nov 2026, layout rework L5: every sketch label goes to the booklet as an item, nothing left out, see NEW IN v21); v20 (4 Nov 2026, round 6 S6: page p12 = the 28 Oct 4-in-1 SKETCH page restored as booklet items, see NEW IN v20); v19.1 fix 2 Nov: key map run warnings; v19 (2 Nov 2026, round 5 S9: booklet items, see NEW IN v19; v18.1 1 Nov 2026: every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v18: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v17: what changed: the NEW IN / VERSION notes below)
"""BERGAMA PROPOSAL SECTIONS v4 (2026-10-25): Group 6's four proposals in section, upstream to downstream, in the
water board's hand-drawn section style (Aras 25 Oct 11:38-11:45: "we want section from each proposal just like our
water board sections"; "the style of waterboard sections were really really good you can do it somewhere else").
For the studio session of 26.10.2026: "Sections: Illustrating the spatial relationships and key design decisions."

NEW IN v21 (layout rework L5, 4 Nov 2026; Aras 19:17-19:18 "make all the scripts just produce the drawings and
  booklet script ... places them"; LAYOUT_PLAN_booklet_places_all.md §3.1; a feature change):
  * declutter() is gone: the script no longer moves a label or leaves one out ("label ... left out (no free place
    near it)" warnings end). Every line of every sketch label is a label item of its panel (role "label", anchor = its
    drawn point in the panel's mm, drawn alignment first), ids ps_panel_<n>_lbl_<g>_<line>; the booklet places them and
    fixes collisions (move, short form, number + side row, smaller). Element numbers (circles 1-11): circle drawn,
    digit = role "badge" (ps_panel_<n>_num_<digit>, the booklet keeps it on its circle).
  * Log per panel: "p12 ps_panel_<n>: labels L (N lines) exported at their drawn points; the booklet places them".
  * SKETCH_SRC.py (shared with agriculture) unchanged.
NEW IN v20 (round 6, S6, 4 Nov 2026; BRIEF row 12, Q9, G6-1..G6-10, P-1, P-7, P-12; a feature change):
  * Booklet page p12 "The proposals in section" = refs/targets/r06_S02: four SKETCH panels (1 upstream entry, 2 K4
    bridge · walking hub, 3 K5 bridge · Demeter's Garden + walking hub, 4 downstream reach) restored from the 28 Oct
    code (commit f93d84b, v8.1: draw_concept, declutter, sections + data/SKETCH_SRC.py), exported as items ps_panel_1-4
    (scale-free drawings, one common factor, same extent), titles + purpose lines, one legend strip (hue table, G6-6),
    a small W1-W4 key map (keymap.py v3, P-1), caption "1-11 as in Collect, clean, hold" (CCH_STEPS numbers).
  * 28 Oct values replaced: Q500 words read live from the level table (W1, W3, W4); the rain shares (59.1 %, 7.4 %)
    left out (no shared data file holds the MGM monthly rain); "[n]" -> {src:key} for public sources only.
  * The target's overlaps moved apart (SUB-HUB caption under the cut, steps label short lines, Q500 words over the
    line, panel 3 number 9, panel 4 labels); no hatches (flat water, flat soil, flat tier bands); trees named by species
    in their groups (G6-9, G6-10); every element its own group inside its kind (S2 grp tags).
  * Gone: the true-scale W1-W4 sections, insets, lists and material legend of v17-v19 (parts/70_sections.py).
NEW IN v19 (round 5, S9, 2 Nov 2026; G-R5-12, D9, N3 a, P13.1-P13.4, G-R5-4.6, G-R5-5, D8, A17, C1; a feature change):
  * Produce, the booklet composes: no A0 sheet, no PDF, no page layout. W1-W4 go to ONE booklet page "p13" (p13 + p14
    merged) at 1:500, each cut one true-scale drawing in metres (x across the stream from the cut axis, NE left;
    y level m a.s.l.) with its numbers as badges, its numbered list "Name · reason", its heading, scenario and water-
    level note, its level column (the booklet draws the U04 markers), its zoom inset drawn AGAIN at the inset scale
    (framed on the action by sf_inset_frame) as its own drawing; one key map (key-map module v2: fitted, turned, own
    north), one material legend (solid colours), title, intro, sources. File: Downloads/Bergama/cached/booklet/
    bergama_proposal_sections/items.json. No folder is made under output/.
  * Spans to the cut ends (no 50 m / 38 m breaks at 1:500), never beyond the level table's ends.
  * Widths gone (P13.4): no "8 × 40 cm" steps, no bed width in cm. Bridges the cut sees (common/bridges.py, D8).
  * Log head "<n> warnings" = the WARNING lines; plant log lines printed once (A17).
NEW IN v17 (round 4, S7, 1 Nov 2026; booklet p13 -> p13a + p13b: P13.1-P13.5, D2, D11, G-R4-1..11; a feature change):
  * Two booklet pages at 1:250 (was one at 1:500): crop ps_p1 = p13a (W1, W2), ps_p2 = p13b (W3, W4), one full row
    per cut; the sheet is drawn at the booklet scale (BK_S 1), so every scale word is the printed one; zoom insets at
    1:100 (D11, 2.5 x) with their own scale bars. W3's bazaar side broken at 50 m, W4's at 38 m (break lines).
  * One block per cut (common/block.py): title strip (cut and name, scenario, look direction by place name), the
    drawing, a side column (W1-W3: key map on one row of each page, the "today" line from the level table, the
    numbered list) or a strip under it (W4); level marks outside the drawing's right edge with the 1:250 scale bar.
  * Every zone and element is one marker (common/marker.py) in the colour of what it names, numbered in reading
    order; the list beside repeats them "Name · reason"; the zone strip, bank rows and callout key are gone.
  * One TextPage per page (common/text_place.py): every text registered with the real Arial widths, a collision
    RAISES ("overlap p13a ... collisions 0" in the log). Key map: only the page's two cuts, red R01 symbol, north arrow
    without a plate. Low planting layer on every soft bank; ash left the back mix (lower sky); one people set
    (pen_black). Start-up: common/trigger.py (only a Button press or a new done text starts it).
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
NEW IN v16 (round 3, Aras 31 Oct, booklet p12: P12.1-P12.5, G2, G3, G15, G16, G17, DATA-1): the key map shows the
  whole study area (fitted, 0.25 pt neatline, labels without leaders: numbers + key) with the material legend beside
  it; cut ends W1 / W1' on the map and under each section (banks by place: Kale side · north bank / bazaar side ·
  south bank); real bridge names, no K-codes; each section measured before it is placed (hard fit inside its cell,
  FLAG when shrunk); no cell frames, white block ground; per cut a scenario in its title, zones named under the
  drawing with a reason (R07), people in front incl. fishing, lying, running, dog walking, trees pushed back and paler,
  street elements (lamps, bollards, bike racks), a quiet sky per cut with a few birds, a 1:200 zoom inset; the
  walled beds (W1, W2) from the surveyed sections (water board data/CUTS.py) with the summer strip on the survey low
  point; log lines FLAG overlap p12, sky variants, plants, fauna, water.
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
  Every section looks downstream (NE left), 1:250 on the booklet page (v17). Not drawn (not in any source): the garden's
  intake and lift, basin volumes.

COMPONENT: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file. Input run (Button), outputs log and done.
v20 NEEDS the new Data file: copy bergama_proposal_sections_data.py (holds SKETCH_SRC) to Downloads/Bergama/Data/.
Writes Downloads/Bergama/cached/booklet/bergama_proposal_sections/items.json (v19; no PDF); log in
Downloads/Bergama/logs/bergama_proposal_sections_log.txt. Reads Downloads/Bergama/cached/basemap/basemap.json (the site
board writes it; without it the key map draws the stream line only) and its Data file (level table); palette from
Downloads/Bergama/Data/bergama_palette.py if there (else the built-in colours).
HOW WE KNOW IT WORKS (v21): the text under the component reads "ProposalSections v21 · HH:MM · N s"; the log has
"p12 ps_panel_1: labels ... none left out" for each panel and no "left out (no free place" warning; it also has
"section p12 P1 W1 SKETCH" ... "P4", "keymap p12 module cuts=W1,W2,W3,W4 study_closed=1", "legend p12 hues=table",
"trees p12 species=...", "p12 numbers 1-11 as CCH_STEPS: ..." and "items bergama_proposal_sections: drawing 5, ...";
the booklet v31 shows p12.
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
VERSION = "v21"  # v21 4 Nov (layout L5): sketch labels exported as label items, none moved or left out (booklet places them); v20 4 Nov (round 6 S6): p12 = the 28 Oct 4-in-1 SKETCH page (f93d84b) as booklet items, hue table, key map v3, groups; v19.1 2 Nov: key map run warnings; v19 2 Nov (round 5 S9): W1-W4 on one page at 1:500 as booklet items (no sheet PDF), insets drawn again at their own scale, key map v2, bridges, no widths, warnings head; v18.1 v18.1 1 Nov 21:40 (Aras 19:33): every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v18 1 Nov 20:55: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v17 (round 4 S7): p13a + p13b at 1:250, one text placer, markers, one trigger file; v16.4 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v16.3 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v16.2 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
GH_LABEL = "ProposalSections"
OUT_FOLDER = "bergama_proposal_sections"
LOG_NAME = "bergama_proposal_sections_log.txt"
OUT_NAME = "Bergama_proposal_sections_{}.pdf"
STYLES = (("a", "A"),)                                # v13 (Aras 31 Oct): style a only, one sheet ..._A.pdf

#@include ../common/bergama_paths.py
BERGAMA = BERGAMA_ROOT
OUT_DIR = bg_output(OUT_FOLDER)                    # v19: nothing is written there any more (no sheet PDF; C2)
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
SRC_KEY = [   # v20: public sources only; the sketches cite them as {src:key} (PS_CITE, parts/90_booklet.py)
    ("levels", u"Q100, Q500: DSİ design flows, Q500 263.3 m³/s (Danıştay 6. D. 2021/9521 E.)"),
    ("plane", u"Ottoman squares with plane trees: ICOMOS 2014, Evaluation No 1457, Pergamon and its Multi-Layered "
              u"Cultural Landscape, p. 281"),
    ("plants", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter); FAO Ecocrop, olive (will not "
               u"tolerate waterlogged soils)"),          # v8.1: the public pages of BK_SOURCES, not the internal register
]


def ps_sources():
    """v20: SRC_KEY (the sketch page prints no bed width, so the DSİ bed-width rows of v19 are gone)"""
    return list(SRC_KEY)

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
    """v17 (G-R4-1): the real Arial width (font_metrics.fm_width) of s at size mm"""
    return fm_width(s, size / PT, bold)

# v17: notes are wrapped by the page's TextPage (text_place.py tp.para), bold keywords between *stars*

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

#@include ../common/_tree_rand.py

# ---------------------------------------------------------------- composing the board from drawn parts
# v10: the page block is drawn in booklet print mm and placed on the board at 1 / BK_S (xform). Text, lines and
# dashes scale with it, as a reduced print does.
#@include ../common/items_bbox.py

#@include ../common/xform.py

# ---------------------------------------------------------------- drawing helpers (page mm, y up)
#@include ../common/rect.py

#@include ../common/node.py

# ---------------------------------------------------------------- shared modules (revision 29 Oct, T2a / T2b)
# v10: the level table (data first), the section parts before the plants, the figures (M7, through ps_fig
# and ps_people), the basemap for the key map. Names checked: no module name is defined by this script.
#@include ../common/data/LEVELS.py

#@include ../common/levels.py

# v16 (G16, D9): one spelling per bridge and place (bridge_name, place_name, cut_end_labels); DATA-1: the surveyed
# sections of the four cuts (ground every 1 m), the water board's data part, read as data (no code copied)
#@include ../common/data/NAMES.py
#@include ../common/names.py

# v20: basemap.py brings keymap.py v3 with hues.py, annot.py, cch_points.py (round 6, S1): never included again here
#@include ../common/basemap.py
#@include ../common/grid.py
#@include ../common/buildings.py


# ---------------------------------------------------------------- the board (A0 landscape, one page)
#@include ../common/load_palette.py

DATA_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data")   # 25 Oct: every data file here

# v20 (round 6, Q9): the sketch engine and data/SKETCH_SRC.py are back (restored from f93d84b); the agriculture
# script's p17 plant ladder includes the same SKETCH_SRC read-only.
_SK = []
#@include ../common/sketch_engine.py
#@include data/SKETCH_SRC.py

# v17 (round 4 S1 modules): the real font widths, ONE text placer (a collision RAISES), ONE marker, ONE block template
#@include ../common/font_metrics.py
#@include ../common/warn.py
#@include ../common/text_place.py
#@include ../common/item_export.py

#@include parts/80_key_map.py

#@include parts/90_booklet.py


# ================================================================ v19: no sheet; the booklet items (parts/90_booklet.py)
def main():
    t0 = time.time()
    wn_reset()                                        # v19 (C1): one warning sink, counted in the log head
    log = []
    pal = load_palette([DATA_DIR], log)
    ix = Ix("bergama_proposal_sections", "bergama_proposal_sections", VERSION)
    ps_items(ix, log)
    path = ix.save()
    log.append(ix.summary())
    log.append(u"trigger: " + (TRIG_WHY[0] or u"-"))     # what started this run
    if pal is None:
        log.append(u"palette: built-in colours (no bergama_palette.py in Downloads/Bergama/Data)")
    head = [u"%s %s · %s · %.1f s" % (GH_LABEL, VERSION, time.strftime("%H:%M"), time.time() - t0),
            u"Items: %s (no sheet PDF: the booklet composes p12)" % path]
    return u"\n".join(wn_compose(tp_log_lines() + [x for x in log if x], head=head))


#@include ../common/trigger.py
TRIG_WHY = [None]                                     # v17: what started this run (trig_should_run), for the log


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
    _pressed, _why, _btn = trig_should_run("bergama_proposal_sections_chain")   # v17 (round 4 S1): one trigger file
    TRIG_WHY[0] = _why
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
    log = _sc.sticky.get(_k + "_log", "Press the Button to export the proposal sections to " + bg_booklet(OUT_FOLDER))
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
else:
    print(write_log(main()))
