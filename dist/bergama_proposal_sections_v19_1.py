# -*- coding: utf-8 -*-
# CURRENT VERSION: bergama_proposal_sections_v19_1.py = v19.1 (fix 2 Nov: key map run warnings); v19 (2 Nov 2026, round 5 S9: booklet items, see NEW IN v19; v18.1 1 Nov 2026: every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v18: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v17: what changed: the NEW IN / VERSION notes below)
"""BERGAMA PROPOSAL SECTIONS v4 (2026-10-25): Group 6's four proposals in section, upstream to downstream, in the
water board's hand-drawn section style (Aras 25 Oct 11:38-11:45: "we want section from each proposal just like our
water board sections"; "the style of waterboard sections were really really good you can do it somewhere else").
For the studio session of 26.10.2026: "Sections: Illustrating the spatial relationships and key design decisions."

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
Writes Downloads/Bergama/cached/booklet/bergama_proposal_sections/items.json (v19; no PDF); log in
Downloads/Bergama/logs/bergama_proposal_sections_log.txt. Reads Downloads/Bergama/cached/basemap/basemap.json (the site
board writes it; without it the key map draws the stream line only) and its Data file (level table); palette from
Downloads/Bergama/Data/bergama_palette.py if there (else the built-in colours).
HOW WE KNOW IT WORKS (v19): the text under the component reads "ProposalSections v19 · HH:MM · N s"; the log starts
with "ProposalSections v19 · HH:MM", the items path, "<n> warnings" and the WARNING lines, and has the line
"items bergama_proposal_sections: drawing 9, ... -> ...items.json" (4 cuts + 4 insets + the key map); no PDF is
written (the booklet v30+ shows p13).
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
VERSION = "v19.1"  # v19.1 fix 2 Nov (run warnings): p13 key map cuts W1-W4 too short for their end names are drawn without them (first name beside the middle) instead of left out; key maps fill their frames (margin per axis), north arrow tries the edges and smaller sizes; v19 2 Nov (round 5 S9): W1-W4 on one page at 1:500 as booklet items (no sheet PDF), insets drawn again at their own scale, key map v2, bridges, no widths, warnings head; v18.1 v18.1 1 Nov 21:40 (Aras 19:33): every layout check that stopped the run (text size, lines, column width, rows, legend room) is a WARNING line and an orange warning; 6.00 pt no longer counts as under 6.0; v18 1 Nov 20:55: text collisions are orange warnings with one WARNING line each, the run goes on (Aras 1 Nov 17:11 + 18:52); v17 (round 4 S7): p13a + p13b at 1:250, one text placer, markers, one trigger file; v16.4 fix 1 Nov 08:30: only the component's own inputs can start it (a True setting inside the script no longer does); v16.3 fix 1 Nov 08:20: chain trigger keyed to each solve (Rhino keeps globals), so the chain continues after ZoneBase; v16.2 fix 1 Nov: a pasted or rewired component no longer runs by itself (chain trigger notes the wire on its first solve)
GH_LABEL = "ProposalSections"
OUT_FOLDER = "bergama_proposal_sections"
LOG_NAME = "bergama_proposal_sections_log.txt"
OUT_NAME = "Bergama_proposal_sections_{}.pdf"
STYLES = (("a", "A"),)                                # v13 (Aras 31 Oct): style a only, one sheet ..._A.pdf

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


def bg_out_dir(name):
    """round 5 (C2): output/<name>/ made only now, just before a file is written into it (a run that stops early, or a
    solve that never runs, leaves no empty folder). Returns the path."""
    p = bg_output(name)
    os.makedirs(p, exist_ok=True)
    return p


def bg_result(script, fn):
    """round 5 (C10): where another script's result file `fn` is: cached/<script>/fn, then cached/<script>/from_output/
    fn (moved there by bg_tidy_output), then output/<script>/fn (older versions); the first that exists, else the
    first path (shade_july.json was looked for in output/ after the site board had moved it to cached/)."""
    return bg_first([os.path.join(bg_cache(script), fn), os.path.join(bg_cache(script), "from_output", fn),
                     os.path.join(bg_output(script), fn)])


def bg_this_run(path):
    """round 5 (C10): (fresh, note) for a result file another script wrote: fresh = written at or after the start of
    this chain run (the Button press that started the chain, sticky "bergama_chain_t0" from trigger.py); note = a short
    log text ("this run 23:01" / "from an earlier run 22:40" / "missing" / "no chain start known"). A reader logs the
    note and, when not fresh, a WARNING (the value is from the run before: one press must give one answer)."""
    import time as _t
    if not os.path.isfile(path):
        return False, u"missing"
    m = os.path.getmtime(path)
    hm = _t.strftime("%d %b %H:%M", _t.localtime(m))
    try:
        import scriptcontext as _scx
        t0 = _scx.sticky.get("bergama_chain_t0")
    except Exception:
        t0 = None
    if t0 is None:
        return True, u"no chain start known (file of %s)" % hm
    if m + 1.0 >= t0:
        return True, u"this run %s" % hm
    return False, u"from an earlier run %s" % hm


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


def _pf_tables(data):
    """Round 4 (S1, 1 Nov 2026): the TrueType tables both the embedding (_pf_metrics) and the measuring
    (font_metrics.py) read, parsed once: upm, gid(char code) -> glyph id, adv (advance per glyph id), glyph_box(gid)
    -> (xMin, yMin, xMax, yMax) in font units or None (empty glyph), and the table offsets"""
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
    ng = _s.unpack(">H", data[tab["maxp"][0] + 4:tab["maxp"][0] + 6])[0] if "maxp" in tab else 0
    lfmt = _s.unpack(">h", data[h + 50:h + 52])[0]

    def glyph_box(g):
        if "loca" not in tab or "glyf" not in tab or not (0 <= g < ng):
            return None
        lo = tab["loca"][0]
        if lfmt == 0:
            a, b = (2 * v for v in _s.unpack(">HH", data[lo + 2 * g:lo + 2 * g + 4]))
        else:
            a, b = _s.unpack(">II", data[lo + 4 * g:lo + 4 * g + 8])
        if b <= a:
            return None
        o = tab["glyf"][0] + a
        return _s.unpack(">hhhh", data[o + 2:o + 10])
    return dict(tab=tab, upm=upm, bbox=bbox, asc=asc, desc=desc, adv=adv, nhm=nhm, gid=gid, glyph_box=glyph_box)


def _pf_metrics(data):
    """widths of codes 32-255 (1000 units per em) and the descriptor numbers, read from the TrueType tables"""
    import struct as _s
    T = _pf_tables(data)
    tab, upm, bbox, asc, desc, adv, nhm, gid = (T[k] for k in ("tab", "upm", "bbox", "asc", "desc", "adv", "nhm",
                                                               "gid"))
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
    xo_res = ""
    if any(it[0] == "image" for it in pg.items):          # D1 a (30 Oct): raster cutouts between the vector items
        stream, xo = _wp_image_stream(pg, add)
        xo_res = " /XObject << {} >>".format(" ".join("/{} {} 0 R".format(n_, o_) for n_, o_ in xo)) if xo else ""
    else:
        stream = page_stream(pg)
    data = zlib.compress(stream, 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data +
              b"\nendstream")
    kid = add("<< /Type /Page /Parent {} 0 R /MediaBox [0 0 {} {}] /Contents {} 0 R /Resources << /Font "
              "<< /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >>{} >> >>".format(pages_id, _f(pg.W / PT), _f(pg.H / PT), cid,
                                                                                font[0], font[1], gs_res, xo_res).encode("latin-1"))
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


# ---- images in the page (H-B, 30 Oct 2026; D1 a: layered raster collage) ------------------------------------------
# A page item ("image", x, y, w, h, path, alpha, flip, clip) puts a PNG (with or without alpha) or a JPEG at x, y
# (lower left, page mm, y up), w x h mm (the caller keeps the proportions), alpha 0-1 or None, flip True = mirrored,
# clip None or (x0, y0, x1, y1) mm. figures.py cut_image() makes these items; section_frame.py shp_put() puts them on
# a page (pg.items). The items are drawn in their place among the vector items (the order of pg.items = the layer
# order). Pages without an image item are written exactly as before. An unreadable image is skipped (WP_IMG_LOG).
# PNG: 8 or 16 bit, grey / grey+alpha / RGB / RGBA / palette (+tRNS), not interlaced; the alpha becomes an SMask.
WP_IMG_LOG = []


def _wp_png(path):
    """(w, h, colour bytes, n colours 1|3, alpha bytes or None) of a PNG, or None"""
    import struct as _st
    with open(path, "rb") as f:
        d = f.read()
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    pos, idat, plte, trns, hdr = 8, [], None, None, None
    while pos + 8 <= len(d):
        n = _st.unpack(">I", d[pos:pos + 4])[0]
        t, c = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + n]
        pos += 12 + n
        if t == b"IHDR":
            hdr = _st.unpack(">IIBBBBB", c[:13])
        elif t == b"PLTE":
            plte = c
        elif t == b"tRNS":
            trns = c
        elif t == b"IDAT":
            idat.append(c)
        elif t == b"IEND":
            break
    if not hdr:
        return None
    w, h, bd, ct, _cm, _fm, il = hdr
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ct)
    if ch is None or il or bd not in (8, 16) or (ct == 3 and bd != 8):
        return None
    bpp = ch * bd // 8
    raw = zlib.decompress(b"".join(idat))
    stride = w * bpp
    out = bytearray(h * stride)
    prev = bytearray(stride)
    i = 0
    for y in range(h):
        ft = raw[i]
        ln = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if ft == 1:
            for x in range(bpp, stride):
                ln[x] = (ln[x] + ln[x - bpp]) & 255
        elif ft == 2:
            for x in range(stride):
                ln[x] = (ln[x] + prev[x]) & 255
        elif ft == 3:
            for x in range(stride):
                ln[x] = (ln[x] + (((ln[x - bpp] if x >= bpp else 0) + prev[x]) >> 1)) & 255
        elif ft == 4:
            for x in range(stride):
                a = ln[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                ln[x] = (ln[x] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
        out[y * stride:(y + 1) * stride] = ln
        prev = ln
    if bd == 16:                                          # keep the high byte of every sample
        out = out[0::2]
    n = w * h
    if ct == 3:
        pal = bytes(plte or b"") + b"\x00" * (768 - len(plte or b""))
        rgb = bytearray(n * 3)
        for k_ in range(3):
            rgb[k_::3] = bytes(out).translate(bytes(pal[3 * j + k_] for j in range(256)))
        alpha = bytes(out).translate(bytes(trns or b"") + b"\xff" * (256 - len(trns or b""))) if trns else None
        return w, h, bytes(rgb), 3, alpha
    if ct == 0:
        return w, h, bytes(out), 1, None
    if ct == 4:
        return w, h, bytes(out[0::2]), 1, bytes(out[1::2])
    if ct == 2:
        return w, h, bytes(out), 3, None
    rgb = bytearray(n * 3)
    rgb[0::3], rgb[1::3], rgb[2::3] = out[0::4], out[1::4], out[2::4]
    alpha = bytes(out[3::4])
    return w, h, bytes(rgb), 3, (None if alpha.count(b"\xff") == n else alpha)


def _wp_jpeg(d):
    """(w, h, n colours) of a baseline / progressive JPEG, or None"""
    if d[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(d):
        if d[i] != 0xFF:
            return None
        m = d[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            return (d[i + 7] << 8) | d[i + 8], (d[i + 5] << 8) | d[i + 6], d[i + 9]
        i += 2 + ((d[i + 2] << 8) | d[i + 3])
    return None


def _wp_image_obj(path, add):
    """the XObject id of one image file (PNG with its SMask, or JPEG), or None"""
    try:
        with open(path, "rb") as f:
            head = f.read(4)
        if head == b"\x89PNG":
            r = _wp_png(path)
            if not r:
                WP_IMG_LOG.append(u"image %s: PNG type not supported (interlaced or < 8 bit)" % path)
                return None
            w, h, col, nc, alpha = r
            sm = ""
            if alpha is not None:
                a = zlib.compress(alpha, 6)
                sid = add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /DeviceGray "
                           "/BitsPerComponent 8 /Filter /FlateDecode /Length {} >>\nstream\n".format(w, h, len(a))
                           ).encode("latin-1") + a + b"\nendstream")
                sm = " /SMask {} 0 R".format(sid)
            c = zlib.compress(col, 6)
            return add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /{} /BitsPerComponent 8"
                        "{} /Filter /FlateDecode /Length {} >>\nstream\n".format(
                            w, h, "DeviceRGB" if nc == 3 else "DeviceGray", sm, len(c))).encode("latin-1") + c +
                       b"\nendstream")
        with open(path, "rb") as f:
            d = f.read()
        info = _wp_jpeg(d)
        if not info:
            WP_IMG_LOG.append(u"image %s: neither PNG nor JPEG" % path)
            return None
        w, h, nc = info
        return add(("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /{} /BitsPerComponent 8 "
                    "/Filter /DCTDecode /Length {} >>\nstream\n".format(
                        w, h, {1: "DeviceGray", 4: "DeviceCMYK"}.get(nc, "DeviceRGB"), len(d))).encode("latin-1") + d +
                   b"\nendstream")
    except Exception as ex:
        WP_IMG_LOG.append(u"image %s: %s" % (path, type(ex).__name__))
        return None


def _wp_image_stream(pg, add):
    """(content stream, [(name, id)]): runs of vector items through page_stream (each in q ... Q), the images
    between them in their order; one XObject per file"""
    class _Run(object):
        pass
    parts, run, names, xo = [], [], {}, []

    def flush():
        if run:
            r = _Run()
            r.W, r.H, r.items = pg.W, pg.H, list(run)
            parts.append(b"q\n" + page_stream(r) + b"\nQ")
            del run[:]
    for it in pg.items:
        if it[0] != "image":
            run.append(it)
            continue
        flush()
        x, y, w, h, p = it[1:6]
        alpha = it[6] if len(it) > 6 else None
        flip = it[7] if len(it) > 7 else False
        clip = it[8] if len(it) > 8 else None
        if p not in names:
            oid = _wp_image_obj(p, add)
            names[p] = None if oid is None else "Im%d" % (len(xo) + 1)
            if oid is not None:
                xo.append((names[p], oid))
        if names[p] is None or w <= 0 or h <= 0:
            continue
        ops = ["q 2.834646 0 0 2.834646 0 0 cm"]
        if alpha is not None and alpha < 0.975:
            ops.append("/A{:02d} gs".format(max(1, min(19, int(round(alpha * 20))))))
        if clip:
            ops.append("{} {} {} {} re W n".format(_f(clip[0]), _f(clip[1]), _f(clip[2] - clip[0]), _f(clip[3] - clip[1])))
        ops.append("{} 0 0 {} {} {} cm /{} Do Q".format(_f(-w if flip else w), _f(h), _f(x + w if flip else x), _f(y),
                                                       names[p]))
        parts.append(" ".join(ops).encode("latin-1"))
    flush()
    return b"\n".join(parts), xo

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
# v10: the level table (data first), the section parts before the plants, the figures (M7, through ps_fig
# and ps_people), the basemap for the key map. Names checked: no module name is defined by this script.
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
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'LEVELS': '3cc5394beb1de45118b6226d608a766b', 'NAMES': '0ec3cbab34964fea25289ca36d8bd453', 'CUTS': '5fb9ed44bfa605770a04af08b74b2ac9', 'BRIDGES': '75e4c182b7d1f921c16948c690b7dae4'}.get(name):
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
    """the row dict of cut (crossing) cid (an alias such as F1 -> W1, F3 -> S4 is accepted); KeyError naming the
    known ids"""
    for r in _lv_rows():
        if r["id"] == cid:
            return r
    for r in _lv_rows():
        if cid in (r.get("aliases") or ()):
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


LV_ENDS_OVERRIDE = {}     # round 4 (S4, N4 b): {cut: ((x1, y1), (x2, y2))} a script that draws a cut on another line
                          # than the table's (site board: S5 across the stream at one crossing) sets it each run;
                          # empty in every other script, so nothing changes there


def level_ends(cid):
    """((x1, y1), (x2, y2)): the cut's two ends in survey m, unprimed end first (LV_ENDS_OVERRIDE first)"""
    r_ = _lv_ends_row(cid)
    ov = LV_ENDS_OVERRIDE.get(r_.get("cut") or cid) or LV_ENDS_OVERRIDE.get(cid)
    if ov:
        return (float(ov[0][0]), float(ov[0][1])), (float(ov[1][0]), float(ov[1][1]))
    (a, b) = r_["ends"]["value"]
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


# ---- cut registry (H-B 30 Oct 2026, M8): one entry per LEVELS row; every section on every page reads its levels here,
# never types them. Printed name = the row id (W1, never F1: PLAN T1).
def level_name(cid):
    """the one printed name of a cut: the row id ("F1" -> "W1", "F3" -> "S4")"""
    return level_cut(cid)["id"]


def level_avg_flow(cid):
    """water level at the mean yearly flow (m a.s.l., 2 decimals): the level a section draws its water at (G8)"""
    return level(cid, "avg_flow")


def level_month_depth(cid, month):
    """(round 3, A2, DATA-1) the mean water depth above the bed (m) in month 1-12 at a cut with a depth_month row (S4):
    the higher of the two gauge routes (Kömürcü, Ilıca), as the water board's DEPTH rule; None without the row"""
    v = _lv_value(cid, "depth_month")
    if v is None:
        return None
    d = v["value"]
    m = (int(month) - 1) % 12
    return max(float(d["komurcu"][m]), float(d["ilica"][m]))


def level_season_depth(cid, months):
    """the mean of level_month_depth over months (1-12, e.g. (12, 1, 2) for winter); None without the row"""
    ds = [level_month_depth(cid, m) for m in months]
    if not ds or any(d is None for d in ds):
        return None
    return sum(ds) / float(len(ds))


def level_registry(cid):
    """the registry entry of a cut: dict(id, name, location, chainage_m, walled, bed, avg_flow, avg_flow_depth, q100,
    q500, walls={NE: (type, top), SW: (type, top)}, bed_width_cm, pages (booklet), aliases); levels m a.s.l."""
    r = level_cut(cid)
    i = r["id"]
    return dict(id=i, name=r.get("name"), location=r.get("location"), chainage_m=level(i, "chainage_m"),
                walled=bool(r.get("walled")), bed=level(i, "bed"), avg_flow=level(i, "avg_flow"),
                avg_flow_depth=level(i, "avg_flow_depth"), q100=level(i, "q100"), q500=level(i, "q500"),
                walls=dict((s_, ((r.get(s_) or {}).get("type"), level(i, "top", s_))) for s_ in ("NE", "SW")),
                bed_width_cm=level(i, "bed_width_cm"), pages=list(r.get("booklet_pages") or []),
                aliases=list(r.get("aliases") or []))


def level_registry_all(page=None):
    """every registry entry in table order; page = a booklet page number ("12") keeps only the cuts drawn there"""
    out = [level_registry(i) for i in level_ids()]
    return [e for e in out if page is None or str(page) in e["pages"]]

# v16 (G16, D9): one spelling per bridge and place (bridge_name, place_name, cut_end_labels); DATA-1: the surveyed
# sections of the four cuts (ground every 1 m), the water board's data part, read as data (no code copied)
bergama_data("NAMES")
# ---- Names (round 3, A2, 31 Oct 2026; G16 / D9): every printed bridge or place name comes from data/NAMES.py ---------
#   bridge_name(code, short=False)   "K3" -> "Tabak Köprüsü" (short: "Tabak", only where the full name is in the
#                                     same drawing's key or title); unknown code -> KeyError (never print a K-code)
#   bridges_in_order()               the codes upstream first: K1, K2, K4, K3, K5, K6 (lists, keys, rulers)
#   place_name(key)                  "bank_NE" -> "Kale side · north bank", "stream" -> "Selinos stream"
#   cut_end_labels(cid)              ("W3", "W3'") the cut id + prime at its ends (D6)
#   landmark_name(key, descr=None)   round 4 (S1, G-R4-11): "kizil_avlu" -> "Kızıl Avlu"; descr=True adds the table's
#                                     English descriptor ("Kızıl Avlu · Hadrian's temple"), descr="text" adds that text;
#                                     unknown key -> KeyError (never type a landmark name locally)
#   landmark_keys()                  the landmark keys in the table
#   name_key(s)                      round 5 (S2): a name as a match key (single spaces, lower case, İ as i)
#   landmark_match(raw, p=None, r_m=60.0, near_m=150.0)   round 5 (S2, A11): the table key a survey / OSM / typed name
#                                     stands for, or None: the table name or an "alias" (whole name); a joined survey
#                                     label that starts with a table name ("Kızıl Avlu Tapınağı Mısır Tanrıları") when
#                                     p lies within near_m of the row's "at"; an "alias_near" word ("Hamam") only
#                                     within r_m of "at"
#   place_label(raw, p=None)         round 5 (S2): the table's one spelling for raw, or None when the table has no row
#                                     (the caller leaves the name out and logs it: never print an unchecked name)
#   street_label(raw)                round 5 (S2): an OpenStreetMap street name as printed: the table's spelling when
#                                     the table has the street (Kınık Caddesi ...), else the OSM tag as mapped
#   keymap_places(box=None)          round 5 (S2, G-R5-3): [(name, (x, y), key)] the table's key-map places ("at" +
#                                     "km"), best first, inside box (survey m) when given
# Needs data/NAMES.py included before it.


def bridge_name(code, short=False):
    """the one spelling of a bridge by its internal code (K1-K6, any case)"""
    row = NAMES["bridges"][str(code).strip().upper()]
    return row["short"] if short else row["name"]


def bridges_in_order():
    """the bridge codes in stream order, upstream first"""
    b = NAMES["bridges"]
    return sorted(b, key=lambda c: b[c]["order"])


def place_name(key):
    """the one spelling of a place (stream, banks, sides)"""
    return NAMES["places"][key]


def cut_end_labels(cid):
    """D6: the labels at a cut's two ends: the cut id and the id with a prime ("W3", "W3'")"""
    c = str(cid).strip()
    return c, c + u"'"


def landmark_name(key, descr=None):
    """the one (Turkish) spelling of a landmark, optionally followed by an English descriptor"""
    row = NAMES["landmarks"][str(key).strip().lower()]
    if descr is True:
        d = row.get("descr")
        if not d:
            raise KeyError(u"landmark %s has no descriptor in the names table" % key)
    else:
        d = descr or None
    return row["name"] + (u" · " + d if d else u"")


def landmark_keys():
    """the landmark keys in the names table"""
    return sorted(NAMES["landmarks"])


def name_key(s):
    """round 5 (S2): a name as a match key: single spaces, lower case, Turkish İ / I handled (İ -> i, I -> ı)"""
    s = u" ".join((s or u"").split()).replace(u"\u0130", u"i").replace(u"I", u"\u0131")
    return s.lower().replace(u"i\u0307", u"i")


def landmark_match(raw, p=None, r_m=60.0, near_m=150.0):
    """round 5 (S2, A11): the names-table key that raw (a survey label, an OSM tag, a typed literal) stands for, or
    None. Rules, in order: (1) the table name or one of its "alias" forms, whole name; (2) raw starts with the table
    name and p (survey m) lies within near_m of the row's "at" (survey labels inside one footprint are joined, e.g.
    "Kızıl Avlu Tapınağı Mısır Tanrıları"); (3) raw is one of the row's "alias_near" words and p lies within r_m of
    "at" (survey "Hamam" -> Tabaklar Hamamı)."""
    k = name_key(raw)
    if not k:
        return None
    rows = NAMES["landmarks"]
    for key, row in rows.items():
        if k == name_key(row["name"]) or k in [name_key(a) for a in row.get("alias") or ()]:
            return key

    def near(row, r):
        at = row.get("at")
        return p is not None and at is not None and (p[0] - at[0]) ** 2 + (p[1] - at[1]) ** 2 <= r * r
    for key, row in rows.items():
        nk = name_key(row["name"])
        if k.startswith(nk + u" ") and near(row, near_m):
            return key
    for key, row in rows.items():
        if k in [name_key(a) for a in row.get("alias_near") or ()] and near(row, r_m):
            return key
    return None


def place_label(raw, p=None):
    """round 5 (S2, G-R5-11): the table's one spelling for a place name, or None when the table has no row for it"""
    key = landmark_match(raw, p)
    return landmark_name(key) if key else None


def street_label(raw):
    """round 5 (S2, G-R4-11): a street name as printed: the table's spelling when the table records the street, else
    the OpenStreetMap tag as mapped (a public source, Turkish as tagged)"""
    key = landmark_match(raw)
    return landmark_name(key) if key else u" ".join((raw or u"").split())


def keymap_places(box=None):
    """round 5 (S2, G-R5-3): the places a key map may name: [(name, (x, y), key)] for every table row with "at" and
    "km", in "km" order, inside box = (x0, y0, x1, y1) survey m when given"""
    out = []
    for key, row in NAMES["landmarks"].items():
        at, rk = row.get("at"), row.get("km")
        if at is None or rk is None:
            continue
        if box is None or (box[0] <= at[0] <= box[2] and box[1] <= at[1] <= box[3]):
            out.append((rk, row["name"], (float(at[0]), float(at[1])), key))
    out.sort(key=lambda r: r[0])
    return [(n, p, k) for _, n, p, k in out]
bergama_data("CUTS")

# ---- section language of the main site board (selinus_board draw_section_strip), shared by the water board and the
# agriculture alternatives (Aras 25 Oct 21:52: their sections drawn "such as we draw in the site sections"): the cut
# ground a shade darker than the page with a fine ink line, water hatched in blue from the bed to its surface, the
# channel above it in a pale wash, whole trees and plants at their stated size. One scale for x and y (Aras 22:02:
# "not stretch anything ever"). Pure geometry: each helper returns shapes, the script's sec_put() draws them.
# Round 5 (S3, section kit v2, G-R5-4.1/4.2): every cut material and the water ONE flat colour (SCT, SCT_WATER), the
# soil in lighter layers going down (SCT_SOIL), no hatch pattern drawn by any function here.
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
# round 4 (S2, G-R4-6): the greenery keys above (tree, pine, olive, reed, reed_head, lav, grass, crown, crown_lt, shrub,
# beyond) are NOT plant colours any more: every plant colour comes from plants.py pla_colours (S3). They stay only
# because plants.py (S3) and masterplan p24_detail.py:1836 (S8) still read them; those sessions remove the reads and
# the closing step deletes these keys. The legacy greenery helpers sec_tree / sec_shrub / sec_reeds / sec_tufts /
# sec_lavender were deleted here (no caller left).


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
    """A water body (ring, page mm). Round 5 (S3, G-R5-4.1, PLAN §3): ONE flat colour SCT_WATER["body"] and the
    surface line SCT_WATER["surface"] on top; no hatch (spacing / lw kept so old calls run, unused)."""
    sh = [("poly", ring, SCT_WATER["body"], None, 0.0)]
    top = max(p[1] for p in ring)
    xs = [p[0] for p in ring if abs(p[1] - top) < 1e-6]
    if len(xs) >= 2:
        sh.append(("line", [(min(xs), top), (max(xs), top)], SCT_WATER["surface"], SCT_WATER["surface_lw"]))
    return sh


# Round 5 (S3, G-R5-4.1, PLAN §3 "Section materials"): design values, solid colours only. Q100 / Q500 lines in the
# surface colour, dashed (water.py reads these).
SCT_WATER = dict(body="A2B6B5", surface="5C7A86", surface_lw=0.25, flood="5C7A86")


# ---- section parts (WO-T2b-3, 29 Oct 2026; section_style.py now includes this file): the river bank as it is at the
# cut (brief 02 §4): DSİ stone walls at 5.00 m, embankments at their surveyed angle, loose earth banks, railings and
# parapets; stone, concrete, earth and the gravel bed in their own hatch; terraces and steps cut into the bank.
# Real sizes in m placed by k (page mm per m); a bank's surface runs from its toe at the bed landward.

SCT_DSI_WALL_H_M = 5.00   # revision_2026-10-29/T1/levels/RESULT.md line 18: "DSİ stone walls at bed + 5.00 m" (Aras 28 Oct)

# material fills. Round 5 (S3, G-R5-4.1, U23-U25 "dont have hatches in the sections just give proper colours to the
# things that we cut"): every cut material ONE flat true colour (PLAN §3 design values); no hatch pattern anywhere.
# Material key = colour swatches (sct_material_key).
SCT = dict(stone="A4A1A3",                            # stone / masonry
           concrete="D5D3CE",                         # concrete / deck
           earth="C2A383",                            # = SCT_SOIL top layer (G-R5-4.2)
           gravel="B9B6AC",                           # gravel bed
           timber="9C8466",                           # timber deck
           line=SEC["ink2"],                          # joint lines (insets at 1:100-1:250 only, G-R5-5)
           cut=SEC["ink"])                            # the cut line
SCT_NAMES = dict(stone=u"Stone, masonry", concrete=u"Concrete", earth=u"Earth", gravel=u"Gravel bed",
                 timber=u"Timber deck", water=u"Water")
SCT_LOG = dict(solid=0, detail=0)                     # cut rings drawn flat / with inset joint detail this run


def sct_material_key(materials=("earth", "stone", "concrete", "gravel", "timber", "water")):
    """the material key of a section as colour swatches (G-R5-4.1: the hatch legend becomes a colour key):
    [(swatch dict for item_export Ix.legend, name)]"""
    out = []
    for m in materials:
        col = SCT_WATER["body"] if m == "water" else SCT[m]
        out.append((dict(kind="fill", colour=col, stroke=None), SCT_NAMES.get(m, m)))
    return out


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


SCT_DETAIL_K = 4.0                    # page mm per m from which a ring gets real joints: 1:250 and larger (G-R5-5 insets)
SCT_COURSE_M = 0.50                   # stone course height (drawing rule, as water.py water_axo course_m; not surveyed)
SCT_BOARD_M = 0.14                    # deck board width (drawing rule, as sf_lane timber; not surveyed)


def sct_hatch_fill(ring, material, k, outline=None, lw=0.25, fill=True, hatch_lw=None):
    """A cut ring (page mm) in its material: stone, concrete, earth, gravel, timber or water. Round 5 (S3, G-R5-4.1):
    ONE flat colour (SCT), no hatch pattern; the name stays so every caller gets solid colours unchanged. At
    1:250 and larger (k >= SCT_DETAIL_K, the zoom insets, G-R5-5) stone shows its courses and timber its boards as
    real joints at drawing-rule sizes (SCT_COURSE_M, SCT_BOARD_M): construction lines, not a hatch. fill=False:
    nothing but the outline (the soil gradient under it is the fill). hatch_lw: kept for old calls, unused."""
    if material == "water":
        return sec_water(ring)
    if material not in SCT or material in ("line", "cut"):
        raise ValueError("sct_hatch_fill: unknown material %r" % material)
    sh = [("poly", ring, SCT[material], None, 0.0)] if fill else []
    SCT_LOG["solid"] += 1
    if fill and k >= SCT_DETAIL_K and material in ("stone", "timber"):
        SCT_LOG["detail"] += 1
        ln = _sec_mix(SCT[material], SEC["ink"], 0.35)
        if material == "stone":                   # bed joints every course, head joints staggered (real size)
            c = SCT_COURSE_M * k
            for p, q in sec_hatch(ring, c, 0.0):
                sh.append(("line", [p, q], ln, 0.06))
            ys = [p[1] for p in ring]
            xs = [p[0] for p in ring]
            import math as _m
            j = int(_m.floor(min(ys) / c))
            while j * c < max(ys):
                x = min(xs) + (0.5 * c if j % 2 else 0.0) + 1.6 * c
                while x < max(xs):
                    for a_, b_ in _sct_clip(ring, (x, j * c), (x, (j + 1) * c)):
                        sh.append(("line", [a_, b_], ln, 0.05))
                    x += 1.6 * c                  # stone length 0.80 m (drawing rule)
                j += 1
        else:                                     # deck boards: vertical joints SCT_BOARD_M apart
            for p, q in sec_hatch(ring, SCT_BOARD_M * k, 90.0):
                sh.append(("line", [p, q], ln, 0.04))
    if outline:
        sh.append(("poly", ring, None, outline, lw))
    return sh


# Soil v2 (round 5, S3, G-R5-4.2, U34/U36/U40/U56/U61/U65: "the top layer a lighter brown, each deeper layer lighter
# still; the layering logic stays"): drawing rules, not measured soil data. A topsoil band SCT_SOIL["top_m"] thick
# in layers[0] at the surface, then the other layers in equal bands following the surface down to the cut bottom,
# each lighter (PLAN §3 values). No hatch over the soil (G-R5-4.1). top / bottom / steps / hatch_lw kept for old reads.
SCT_SOIL = dict(layers=("C2A383", "D0B699", "DDC9B0", "E9DDCB"), top="C2A383", bottom="E9DDCB", top_m=0.30, steps=3,
                hatch_lw=0.053)


def sct_soil_gradient(surface, bottom_y, k):
    """G-R5-4.2 soil under a surface polyline (page mm, left to right) down to bottom_y: the topsoil band (SCT_SOIL
    top_m x k deep under every point of the surface) in layers[0], then one band per further layer, each parallel to
    the surface, lighter going down, the last reaching bottom_y. Opaque fills only, no strokes. Returns shapes."""
    S = [(float(x), float(y)) for x, y in surface]
    if len(S) < 2:
        return []
    t = SCT_SOIL["top_m"] * k
    cols = list(SCT_SOIL["layers"])
    n = len(cols) - 1
    b = float(bottom_y)

    def depth_at(y, f):                       # f = 0 at the topsoil's underside .. 1 at the cut bottom
        top = max(b, y - t)
        return top - (top - b) * f

    sh = [("poly", [(x, y) for x, y in S] + [(x, max(b, y - t)) for x, y in reversed(S)], cols[0], None, 0.0)]
    for i in range(n):
        fa, fb = i / float(n), (i + 1) / float(n)
        ring = [(x, depth_at(y, fa)) for x, y in S] + [(x, depth_at(y, fb)) for x, y in reversed(S)]
        sh.append(("poly", ring, cols[i + 1], None, 0.0))
    return sh


def sct_ground(surface, bottom_y, k, material="earth", lw=0.35):
    """Cut ground under a surface polyline (page mm, left to right) down to bottom_y: its solid material and the cut
    line. material "earth": the soil v2 layers (sct_soil_gradient, G-R5-4.2), no hatch (round 5)."""
    ring = list(surface) + [(surface[-1][0], bottom_y), (surface[0][0], bottom_y)]
    if material == "earth":
        return sct_soil_gradient(surface, bottom_y, k) + [("line", list(surface), SCT["cut"], lw)]
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

# ---- silhouette.py (round 5 S4, 1 Nov 2026; G-R5-4.4, G-R5-6, N1, D4): one small raster engine, pure Python 3 ------
# Used by figures.py (solid dark bodies of the library people) and plants.py (toned plant images). Included by
# plants.py (#@include), so every script that draws plants or people has it. No Rhino, no PIL; numpy only if present.
#   sil_png_size(path) -> (w, h) | None             PNG / JPEG pixel size from the header only
#   sil_png_read(path) -> (w, h, rgb bytes, n colours 1|3, alpha bytes | None) | None   (8/16 bit, not interlaced)
#   sil_png_write(path, w, h, rgb, alpha)           RGBA (or RGB) 8 bit PNG, filter 0
#   sil_body(rings_m, px_m, close_m, key) -> [ring m]   the filled outline of a pen drawing: rings rasterised,
#                                                   closed (dilate + erode close_m), holes filled, traced, smoothed
#   sil_alpha_body(path, h_m, px_m, close_m, thr) -> ([ring m], w_m)   the same from a PNG's alpha (feet = bottom row)
#   sil_tone(src, dst, shade, mid, light, keep, paper, fade) -> (ok, how)   a plant image toned to its species
#                                                   colours (luminance -> shade/mid/light ramp, keep = share of the
#                                                   photo's own colour kept, then faded toward the paper by fade)
# Bitmaps are lists of Python ints, one per row (bit i = column i), row 0 at the bottom (y up).
import os as _sil_os
import zlib as _sil_zlib
import struct as _sil_st

SIL_LOG = []
_SIL_BODY = {}          # key -> rings (m), one run
_SIL_PNG = {}           # path -> decoded PNG, one run


def sil_png_size(path):
    """(w, h) in pixels of a PNG or JPEG, read from the header; None if unreadable"""
    try:
        with open(path, "rb") as f:
            d = f.read(65536)
    except Exception:
        return None
    if d[:8] == b"\x89PNG\r\n\x1a\n" and d[12:16] == b"IHDR":
        return _sil_st.unpack(">II", d[16:24])
    if d[:2] == b"\xff\xd8":
        i = 2
        while i + 9 < len(d):
            if d[i] != 0xFF:
                return None
            m = d[i + 1]
            if m in (0xC0, 0xC1, 0xC2):
                return (d[i + 7] << 8) | d[i + 8], (d[i + 5] << 8) | d[i + 6]
            i += 2 + ((d[i + 2] << 8) | d[i + 3])
    return None


def sil_png_read(path):
    """(w, h, rgb bytes, n colours 1|3, alpha bytes or None) of a PNG (8 or 16 bit, grey/RGB/palette, +alpha,
    not interlaced), or None. Rows top to bottom as in the file. Kept in memory for the run."""
    if path in _SIL_PNG:
        return _SIL_PNG[path]
    try:
        with open(path, "rb") as f:
            d = f.read()
    except Exception:
        return None
    if d[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    pos, idat, plte, trns, hdr = 8, [], None, None, None
    while pos + 8 <= len(d):
        n = _sil_st.unpack(">I", d[pos:pos + 4])[0]
        t, c = d[pos + 4:pos + 8], d[pos + 8:pos + 8 + n]
        pos += 12 + n
        if t == b"IHDR":
            hdr = _sil_st.unpack(">IIBBBBB", c[:13])
        elif t == b"PLTE":
            plte = c
        elif t == b"tRNS":
            trns = c
        elif t == b"IDAT":
            idat.append(c)
        elif t == b"IEND":
            break
    if not hdr:
        return None
    w, h, bd, ct, _cm, _fm, il = hdr
    ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ct)
    if ch is None or il or bd not in (8, 16) or (ct == 3 and bd != 8):
        return None
    bpp = ch * bd // 8
    raw = _sil_zlib.decompress(b"".join(idat))
    stride = w * bpp
    out = bytearray(h * stride)
    prev = bytearray(stride)
    i = 0
    for y in range(h):
        ft = raw[i]
        ln = bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        if ft == 1:
            for x in range(bpp, stride):
                ln[x] = (ln[x] + ln[x - bpp]) & 255
        elif ft == 2:
            for x in range(stride):
                ln[x] = (ln[x] + prev[x]) & 255
        elif ft == 3:
            for x in range(stride):
                ln[x] = (ln[x] + (((ln[x - bpp] if x >= bpp else 0) + prev[x]) >> 1)) & 255
        elif ft == 4:
            for x in range(stride):
                a = ln[x - bpp] if x >= bpp else 0
                b = prev[x]
                c = prev[x - bpp] if x >= bpp else 0
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                ln[x] = (ln[x] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
        out[y * stride:(y + 1) * stride] = ln
        prev = ln
    if bd == 16:
        out = out[0::2]
    n = w * h
    if ct == 3:
        pal = bytes(plte or b"") + b"\x00" * (768 - len(plte or b""))
        rgb = bytearray(n * 3)
        for k_ in range(3):
            rgb[k_::3] = bytes(out).translate(bytes(pal[3 * j + k_] for j in range(256)))
        alpha = bytes(out).translate(bytes(trns or b"") + b"\xff" * (256 - len(trns or b""))) if trns else None
        r = (w, h, bytes(rgb), 3, alpha)
    elif ct == 0:
        r = (w, h, bytes(out), 1, None)
    elif ct == 4:
        r = (w, h, bytes(out[0::2]), 1, bytes(out[1::2]))
    elif ct == 2:
        r = (w, h, bytes(out), 3, None)
    else:
        rgb = bytearray(n * 3)
        rgb[0::3], rgb[1::3], rgb[2::3] = out[0::4], out[1::4], out[2::4]
        r = (w, h, bytes(rgb), 3, bytes(out[3::4]))
    _SIL_PNG[path] = r
    return r


def sil_png_write(path, w, h, rgb, alpha=None):
    """writes an 8 bit RGB(A) PNG (rows top to bottom, filter 0); the folder is made"""
    if alpha is not None:
        px = bytearray(w * h * 4)
        px[0::4], px[1::4], px[2::4], px[3::4] = rgb[0::3], rgb[1::3], rgb[2::3], alpha
        bpp, ct = 4, 6
    else:
        px, bpp, ct = bytes(rgb), 3, 2
    stride = w * bpp
    raw = b"".join(b"\x00" + bytes(px[y * stride:(y + 1) * stride]) for y in range(h))

    def chunk(t, c):
        return _sil_st.pack(">I", len(c)) + t + c + _sil_st.pack(">I", _sil_zlib.crc32(t + c) & 0xffffffff)
    d = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", _sil_st.pack(">IIBBBBB", w, h, 8, ct, 0, 0, 0)) +
         chunk(b"IDAT", _sil_zlib.compress(raw, 6)) + chunk(b"IEND", b""))
    _sil_os.makedirs(_sil_os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(d)


# ---- bitmaps (rows of ints) -------------------------------------------------------------------------------------------
def _sil_fill_ring(rows, ring, x0, y0, px, W):
    """ORs the inside of one closed ring (m) into rows (even-odd scanline at each row's centre)"""
    n = len(ring)
    if n < 3:
        return
    ys = [p[1] for p in ring]
    r0 = max(0, int((min(ys) - y0) / px) - 1)
    r1 = min(len(rows) - 1, int((max(ys) - y0) / px) + 1)
    full = (1 << W) - 1
    for r in range(r0, r1 + 1):
        yc = y0 + (r + 0.5) * px
        xs = []
        for i in range(n):
            ax, ay = ring[i]
            bx, by = ring[(i + 1) % n]
            if (ay <= yc < by) or (by <= yc < ay):
                xs.append(ax + (yc - ay) * (bx - ax) / (by - ay))
        xs.sort()
        m = 0
        for a, b in zip(xs[0::2], xs[1::2]):
            c0 = max(0, int(round((a - x0) / px)))
            c1 = min(W, int(round((b - x0) / px)))
            if c1 <= c0 and b - a > 0:                  # a sliver thinner than a pixel still marks one
                c0 = min(W - 1, max(0, int((0.5 * (a + b) - x0) / px)))
                c1 = c0 + 1
            if c1 > c0:
                m |= ((1 << (c1 - c0)) - 1) << c0
        rows[r] |= m & full


def _sil_dilate(rows, W, r):
    full = (1 << W) - 1
    hz = []
    for v in rows:
        a = v
        for i in range(1, r + 1):
            a |= (v << i) | (v >> i)
        hz.append(a & full)
    H = len(rows)
    out = []
    for y in range(H):
        a = 0
        for yy in range(max(0, y - r), min(H, y + r + 1)):
            a |= hz[yy]
        out.append(a)
    return out


def _sil_erode(rows, W, r):
    full = (1 << W) - 1
    inv = [(~v) & full for v in rows]
    # outside the grid counts as empty: pad so the border erodes (the grid has a margin > r, so this never bites)
    d = _sil_dilate(inv, W, r)
    return [(~v) & full for v in d]


def _sil_fill_holes(rows, W):
    """every empty region not connected to the grid border becomes filled"""
    full = (1 << W) - 1
    H = len(rows)
    emp = [(~v) & full for v in rows]
    edge = 1 | (1 << (W - 1))
    ext = [emp[y] if y in (0, H - 1) else (emp[y] & edge) for y in range(H)]
    changed = True
    while changed:
        changed = False
        for y in list(range(H)) + list(range(H - 1, -1, -1)):
            a = ext[y]
            b = a | (a << 1) | (a >> 1)
            if y > 0:
                b |= ext[y - 1]
            if y < H - 1:
                b |= ext[y + 1]
            b &= emp[y]
            while True:                                 # run along the row at once
                c = (b | (b << 1) | (b >> 1)) & emp[y]
                if c == b:
                    break
                b = c
            if b != a:
                ext[y] = b
                changed = True
    return [full & ~e for e in ext]


def _sil_bits(v):
    i = 0
    while v:
        if v & 1:
            yield i
        v >>= 1
        i += 1


def _sil_trace(rows, W):
    """outer outlines (lattice points, counter-clockwise) of the filled cells; holes must be filled before"""
    H = len(rows)
    full = (1 << W) - 1
    nxt = {}

    def add(a, b):
        nxt.setdefault(a, []).append(b)
    for y in range(H):
        v = rows[y]
        if not v:
            continue
        below = rows[y - 1] if y > 0 else 0
        above = rows[y + 1] if y < H - 1 else 0
        for x in _sil_bits(v & ~below & full):
            add((x, y), (x + 1, y))
        for x in _sil_bits(v & ~(v >> 1) & full):           # right neighbour empty
            add((x + 1, y), (x + 1, y + 1))
        for x in _sil_bits(v & ~above & full):
            add((x + 1, y + 1), (x, y + 1))
        for x in _sil_bits(v & ~(v << 1) & full):           # left neighbour empty
            add((x, y + 1), (x, y))
    loops = []
    while nxt:
        start = next(iter(nxt))
        loop, cur, prev_d = [start], start, None
        while True:
            outs = nxt.get(cur)
            if not outs:
                break
            if len(outs) > 1 and prev_d is not None:        # a pinch: turn right first (keeps the parts apart)
                def turn(b, _c=cur, _d=prev_d):
                    d = (b[0] - _c[0], b[1] - _c[1])
                    return _d[0] * d[1] - _d[1] * d[0]       # < 0 right, 0 straight, > 0 left
                outs.sort(key=turn)
            b = outs.pop(0)
            if not outs:
                del nxt[cur]
            prev_d = (b[0] - cur[0], b[1] - cur[1])
            cur = b
            if cur == start:
                break
            loop.append(cur)
        if len(loop) >= 4:
            loops.append(loop)
    return loops


def _sil_area(P):
    return 0.5 * sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P)))


def _sil_dp(P, tol):
    """Douglas-Peucker on a closed ring"""
    if len(P) < 5:
        return P
    i_far = max(range(len(P)), key=lambda i: (P[i][0] - P[0][0]) ** 2 + (P[i][1] - P[0][1]) ** 2)

    def dp(Q):                                          # iterative (long staircases never hit the recursion limit)
        keep = [False] * len(Q)
        keep[0] = keep[-1] = True
        st = [(0, len(Q) - 1)]
        while st:
            i0, i1 = st.pop()
            if i1 - i0 < 2:
                continue
            (ax, ay), (bx, by) = Q[i0], Q[i1]
            L = ((bx - ax) ** 2 + (by - ay) ** 2) ** 0.5 or 1e-9
            dm, im = -1.0, i0
            for i in range(i0 + 1, i1):
                d = abs((bx - ax) * (ay - Q[i][1]) - (ax - Q[i][0]) * (by - ay)) / L
                if d > dm:
                    dm, im = d, i
            if dm > tol:
                keep[im] = True
                st += [(i0, im), (im, i1)]
        return [q for q, k_ in zip(Q, keep) if k_]
    a = dp(P[:i_far + 1])
    b = dp(P[i_far:] + [P[0]])
    return a[:-1] + b[:-1]


def _sil_chaikin(P, n=2):
    for _ in range(n):
        Q = []
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            Q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        P = Q
    return P


def _sil_outline(rows, W, x0, y0, px, close_px, min_px=6):
    """closed, hole-filled, traced and smoothed outlines (m) of a bitmap"""
    if close_px > 0:
        rows = _sil_erode(_sil_dilate(rows, W, close_px), W, close_px)
    rows = _sil_fill_holes(rows, W)
    out = []
    for L in _sil_trace(rows, W):
        if abs(_sil_area(L)) < min_px:
            continue
        P = _sil_chaikin(_sil_dp([(float(a), float(b)) for a, b in L], 0.6), 2)
        out.append([(x0 + a * px, y0 + b * px) for a, b in P])
    return out


def sil_body(rings_m, px_m=0.01, close_m=0.05, key=None):
    """the solid outline(s) of a drawing made of closed rings (m, y up): rasterised at px_m, closed by close_m
    (gaps between pen strokes up to about 2 x close_m fill), inner holes filled, outer edge traced and smoothed.
    Returns [ring (m)]; [] for nothing. key: memo for the run."""
    if key is not None and key in _SIL_BODY:
        return _SIL_BODY[key]
    pts = [p for r in rings_m for p in r]
    if not pts:
        return []
    cp = max(0, int(round(close_m / px_m)))
    pad = (cp + 3) * px_m
    x0, y0 = min(p[0] for p in pts) - pad, min(p[1] for p in pts) - pad
    W = int((max(p[0] for p in pts) + pad - x0) / px_m) + 1
    H = int((max(p[1] for p in pts) + pad - y0) / px_m) + 1
    rows = [0] * H
    for r in rings_m:
        _sil_fill_ring(rows, r, x0, y0, px_m, W)
    out = _sil_outline(rows, W, x0, y0, px_m, cp)
    if key is not None:
        _SIL_BODY[key] = out
    return out


def sil_alpha_body(path, h_m, px_m=0.01, close_m=0.02, thr=128):
    """([ring m], w_m): the solid outline of a cutout PNG from its alpha (alpha > thr), scaled so the image is h_m
    tall, feet = the bottom row at y 0, x centred. ([], 0) if unreadable or with no alpha."""
    key = ("alpha", path, round(h_m, 3), px_m, close_m, thr)
    if key in _SIL_BODY:
        return _SIL_BODY[key]
    r = sil_png_read(path)
    if not r or r[4] is None:
        SIL_LOG.append(u"silhouette: %s has no alpha" % _sil_os.path.basename(path))
        _SIL_BODY[key] = ([], 0.0)
        return _SIL_BODY[key]
    w, h, _rgb, _nc, al = r
    m_px = h_m / float(h)                                    # m per image pixel
    step = max(1, int(px_m / m_px))
    W, H = (w + step - 1) // step + 6, (h + step - 1) // step + 6
    rows = [0] * H
    for yy in range(0, h, step):
        ln = al[yy * w:(yy + 1) * w:step]
        v = 0
        for i, a in enumerate(ln):
            if a > thr:
                v |= 1 << (i + 3)
        rows[(h - 1 - yy) // step + 3] = v                   # image top row -> highest bitmap row
    px = m_px * step
    cp = max(0, int(round(close_m / px)))
    out = _sil_outline(rows, W, -(w * m_px) / 2.0 - 3 * px, -3 * px, px, cp)
    if out:                                                  # feet exactly on y 0
        y_min = min(p[1] for R in out for p in R)
        out = [[(a, b - y_min) for a, b in R] for R in out]
    _SIL_BODY[key] = (out, w * m_px)
    return _SIL_BODY[key]


# ---- the cutout library (Data/cutouts/cutouts.json; recovered from a936d62:src/common/figures.py:747-792, round 5) --------
# {"cutouts": {key: entry or [entries]}}, entry = {"file", "h_m" (true height of what the PNG shows, bottom edge =
# ground/feet), "kind", "facing" (-1 = looks left; default +1), "depth": {"1": file, "2": file}, ...}. Keys: plants =
# the plants.py species key ("olive"), people = "person_<pose>", "stall". Read once per run.
_SIL_CUT = {}


def sil_cut_dir():
    return _sil_os.path.join(_sil_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "cutouts")


def sil_cut_library():
    """{key: [entry, ...]} from cutouts.json (entries whose file exists), {} when the folder or file is missing"""
    import json as _j
    if "lib" in _SIL_CUT:
        return _SIL_CUT["lib"]
    lib = {}
    p = _sil_os.path.join(sil_cut_dir(), "cutouts.json")
    try:
        with open(p, "r", encoding="utf-8") as fh:
            js = _j.load(fh)
        js = js.get("cutouts", js) if isinstance(js, dict) else {}
        for k_, v in js.items():
            vs = v if isinstance(v, list) else [v]
            ok = [e for e in vs if isinstance(e, dict) and e.get("file") and e.get("h_m") and
                  _sil_os.path.isfile(_sil_os.path.join(sil_cut_dir(), e["file"]))]
            if ok:
                lib[k_] = ok
        SIL_LOG.append(u"cutouts: %d keys from %s" % (len(lib), p))
    except Exception as ex:
        SIL_LOG.append(u"FLAG cutouts: %s not read (%s)" % (p, type(ex).__name__))
    _SIL_CUT["lib"] = lib
    return lib


# ---- toning (plants) ----------------------------------------------------------------------------------------------------
def _sil_hex(c):
    return [int(c[i:i + 2], 16) for i in (0, 2, 4)]


def sil_tone(src, dst, shade, mid, light, keep=0.25, paper="F1EDDF", fade=0.0):
    """writes dst: the PNG src toned to a species' colours. Each pixel's luminance (stretched between the 2nd and
    98th percentile of the opaque pixels) maps onto the ramp shade -> mid -> light; keep (0-1) of the photo's own
    colour is mixed back (flowers stay visible); then everything is mixed toward the paper by fade (depth). Alpha
    unchanged. With numpy: as above; without: the ramp from the green channel only (keep ignored).
    Returns (True, "numpy"|"lut") or (False, why)."""
    r = sil_png_read(src)
    if not r:
        return False, "unreadable PNG"
    w, h, rgb, nc, al = r
    S, M_, L_, P = _sil_hex(shade), _sil_hex(mid), _sil_hex(light), _sil_hex(paper)
    try:
        import numpy as _np
    except Exception:
        _np = None
    if _np is not None:
        a = _np.frombuffer(rgb, dtype=_np.uint8).reshape(-1, nc).astype(_np.float32)
        if nc == 1:
            a = _np.repeat(a, 3, axis=1)
        lum = 0.2126 * a[:, 0] + 0.7152 * a[:, 1] + 0.0722 * a[:, 2]
        op = lum if al is None else lum[_np.frombuffer(al, dtype=_np.uint8) > 128]
        if op.size < 10:
            op = lum
        lo, hi = _np.percentile(op, 2), _np.percentile(op, 98)
        t = _np.clip((lum - lo) / max(1.0, hi - lo), 0.0, 1.0)[:, None]
        S_, M2, L2 = (_np.array(c, dtype=_np.float32)[None, :] for c in (S, M_, L_))
        duo = _np.where(t < 0.5, S_ + (M2 - S_) * (t / 0.5), M2 + (L2 - M2) * ((t - 0.5) / 0.5))
        out = duo * (1.0 - keep) + a * keep
        out = out + (_np.array(P, dtype=_np.float32)[None, :] - out) * fade
        sil_png_write(dst, w, h, _np.clip(out + 0.5, 0, 255).astype(_np.uint8).tobytes(), al)
        return True, "numpy"
    g = rgb[1::3] if nc == 3 else rgb
    gs = sorted(g[::97]) or [0, 255]
    lo, hi = gs[int(0.02 * (len(gs) - 1))], gs[int(0.98 * (len(gs) - 1))]
    lut = [bytearray(256) for _ in range(3)]
    for v in range(256):
        t = min(1.0, max(0.0, (v - lo) / float(max(1, hi - lo))))
        for c in range(3):
            x = S[c] + (M_[c] - S[c]) * t / 0.5 if t < 0.5 else M_[c] + (L_[c] - M_[c]) * (t - 0.5) / 0.5
            x = x + (P[c] - x) * fade
            lut[c][v] = int(max(0, min(255, round(x))))
    out = bytearray(w * h * 3)
    for c in range(3):
        out[c::3] = bytes(g).translate(bytes(lut[c]))
    sil_png_write(dst, w, h, bytes(out), al)
    return True, "lut"
# ---- round 5 (S4, 1 Nov 2026; G-R5-6, D4, D10, N2 a): PLANT MODULE v3. Every pla_section / pla_plan / pla_axo /
# pla_bare / crop call draws the species from a real image per species x state (see "plant module v3" above
# pla_section), toned to its colours; the round 4 vector drawing below stays only as the counted, FLAGged fallback
# where no image exists yet (pla_missing), so the pages never go blank before the asset project delivers
# Data/plants/. Interfaces unchanged. silhouette.py (included above) holds the PNG reader/writer and the toning.
# ---- round 4 (S3, 1 Nov 2026; D1, D4, D6 states, D7, G-R4-5.2, G-R4-5.8, G-R4-6): ONE vector drawing per species for
# every plan, section, view, axo (pla_axo) and the p17 catalogue: white willow v2, print-quality crowns of two-tone
# leaf masses with gaps, a shrub/flower low layer (pla_low_section / pla_low_plan), season= on every call (None =
# general; month= alias), crops and cells in their season state. Colours = round 3 values, all pending
# research/plant_colours.md (PLA_COLOUR_SRC; log FLAG). No cutouts or high-res silhouettes for plants any more.
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
# round 4 (S3, G-R4-6): the greenery colours plants.py read from section_parts SEC, copied here with the same values so
# that no greenery colour lives outside this module (SEC's greenery keys can go at closing). Pending research as all.
PLA_LAV = "9F86C0"        # = SEC lav: chaste tree / French lavender flowers
PLA_REED_HEAD = "B49A6C"  # = SEC reed_head: reed plumes, rush tufts, maize tassels
PLA_CROP_LEAF = "8F9A68"  # = SEC grass: cotton, maize, tomato leaves
PLA_TRUNK = "7A6E60"      # = SEC trunk: stems and trunks
PLA_BEYOND = _sec_mix("7E8A57", SEC["paper"], 0.62)   # = SEC beyond (tree 7E8A57 toward paper): giant reed


def _pla_c(fill, accent=None, stem=None):
    """The colour set of one species: fill, edge, lighter lobes, stem, accent (same in both views)."""
    return dict(fill=fill, edge=SEC["ink2"], lt=_sec_mix(fill, SEC["paper"], 0.35), stem=stem or PLA_TRUNK,
                accent=accent)


# one entry per species (species.json species_data + giant reed from the screening); h_range = sourced (lo, hi) m
PLA_SPECIES = {
    "plane": dict(name="Oriental plane", turkish="Doğu çınarı", latin="Platanus orientalis", layer="tree",
                  form="dome", foliage="deciduous (S26)", status="keep",
                  h_range=(None, 30.0), h_m=15.0,            # "up to 30 m" S68, S69
                  crown_m=15.0,                              # "wider than 8 metres" S70: form rule 1.0 x h (>= 8)
                  bloom=[4, 5], leaf=PLA_LEAF_SITE,          # Apr-May S69 (secondary)
                  colours=_pla_c("637F48")),                  # round 3 species colour (D7; ΔE00 >= 12.7); every colour: PLA_COLOUR_SRC
    "ash": dict(name="Narrow-leaved ash", turkish="Dişbudak", latin="Fraxinus angustifolia", layer="tree",
                form="oval", foliage="deciduous (S7)", status="keep",
                h_range=(None, 40.0), h_m=20.0,              # "40-45m" maximum S7 (lower figure)
                crown_m=14.0,                                # "dense, irregular and dome shaped" S7: rule 0.7 x h
                bloom=[], leaf=PLA_LEAF_SITE,                # "early spring or even in autumn" S7: no months
                colours=_pla_c("3E6C5D")),                # round 3: blue-green
    "willow": dict(name="White willow", turkish="Ak söğüt", latin="Salix alba", layer="tree",
                   form="weeping", foliage="deciduous (not quoted)", status="keep",
                   h_range=(None, 30.0), h_m=15.0,           # "up to 30 m" S4
                   crown_m=10.5,                             # crown not found: rule 0.7 x h
                   bloom=[], leaf=PLA_LEAF_SITE,             # "spring" catkins S4: no months
                   colours=_pla_c("A9B88A")),                   # round 3: silvery light green
    "olive": dict(name="Olive", turkish="Zeytin", latin="Olea europaea", layer="tree",
                  form="gnarled", foliage="evergreen (S72)", status="keep",
                  h_range=(8.0, 15.0), h_m=11.5,             # "8-15 m" S72
                  crown_m=10.35,                             # crown not found: rule 0.9 x h
                  bloom=[4], leaf=PLA_ALL_YEAR,              # full bloom 21-24 Apr, ends 29 Apr-1 May S73 (Ege Univ.)
                  colours=_pla_c("7D8C80")),                  # round 3: grey-green
    "stone_pine": dict(name="Stone pine", turkish="Fıstık çamı", latin="Pinus pinea", layer="tree",
                       form="umbrella", foliage="evergreen conifer (S74)", status="keep (processionary caterpillar)",
                       h_range=(25.0, 30.0), h_m=27.5,       # "25-30 m" S74
                       crown_m=15.1,                         # "umbrella-shaped ... flat and broad" S74: rule 0.55 x h
                       bloom=[], leaf=PLA_ALL_YEAR,          # pollen months not found
                       colours=_pla_c("31432E")),              # round 3: deep green
    "tamarisk": dict(name="Tamarisk", turkish="Ilgın", latin="Tamarix smyrnensis", layer="tree",
                     form="feathery", foliage="deciduous (S9b, genus)", status="keep (replaces oleander)",
                     h_range=(4.0, 15.0), h_m=9.5,           # "4-15 m" S9b (genus)
                     crown_m=7.6,                            # "broad, bushy" S9b: rule 0.8 x h
                     bloom=[], leaf=PLA_LEAF_SITE,           # bloom not found for T. smyrnensis
                     colours=_pla_c("9AA9B3")),                # round 3: glaucous blue-grey
    "chaste": dict(name="Chaste tree", turkish="Hayıt", latin="Vitex agnus-castus", layer="shrub",
                   form="multistem", foliage="deciduous (S58)", status="keep (replaces oleander, fig, citrus)",
                   h_range=(1.0, 3.0), h_m=2.0,              # "1-3 m" S58
                   crown_m=2.0,                              # "1.5-2.5 m" S67 (RHS, UK)
                   bloom=[6, 7, 8, 9], leaf=PLA_LEAF_SITE,   # "(Apr-)Jun-Sep" S58 (Crete); Apr-May occasional
                   colours=_pla_c("928955", PLA_LAV)),       # round 3: khaki; flower colour not sourced: section_style lav
    "rosemary": dict(name="Rosemary", turkish="Biberiye", latin="Salvia rosmarinus", layer="shrub",
                     form="mound", foliage="evergreen (S58, S71)", status="keep",
                     h_range=(0.5, 1.0), h_m=0.75,           # "50-100 cm" S58 (Crete)
                     crown_m=0.75,                           # "1.5-2.5 m" S71 for 1.5-2.5 m plants: scaled to h
                     bloom=[1, 2, 3, 4, 5], leaf=PLA_ALL_YEAR,  # "Jan-May, intermittently to Dec" S58
                     colours=_pla_c("5E6356")),                # round 3: dark grey-green
    "lavender": dict(name="French lavender", turkish="Karabaş otu", latin="Lavandula stoechas", layer="ground",
                     form="mound", foliage="evergreen (UNVERIFIED)", status="keep",
                     h_range=(0.3, 0.8), h_m=0.55,           # "30-80 cm" S58
                     crown_m=0.66,                           # crown not found: rule 1.2 x h
                     bloom=[3, 4, 5], leaf=[],               # "Mar-May" S58; evergreen unverified: no leaf months
                     colours=_pla_c("B6AFC3", PLA_LAV)),      # round 3: lilac grey; flowers as sec_lavender
    "loosestrife": dict(name="Purple loosestrife", turkish="Aklar otu", latin="Lythrum salicaria", layer="emergent",
                        form="clump", foliage="herbaceous perennial", status="keep, flower heads cut in Sep (D6)",
                        h_range=(0.3, 2.4), h_m=1.35,        # "0.3-2.4 m" S19
                        crown_m=0.75,                        # "5 feet (1.5 m) wide" mature S19: half the maximum
                        bloom=[6, 7, 8, 9], leaf=[],         # "June ... September" S19; cut Sep (D6)
                        colours=_pla_c("5C9D74", PLA_PURPLE)),     # round 3: fresh blue-green
    "soft_rush": dict(name="Soft rush", turkish="UNVERIFIED", latin="Juncus effusus", layer="emergent",
                      form="clump", foliage="not found", status="new (replaces iris and cattail)",
                      h_range=(0.5, 1.5), h_m=1.0,           # "5-15 dm tall" S59
                      crown_m=0.6,                           # "tufted, cespitose" S59: rule 0.6 x h
                      bloom=[5, 6, 7, 8], leaf=[],           # "late May-Aug, occasionally Sep" S59 (USA)
                      colours=_pla_c("7C9A2E")),               # round 3: rush green
    "rush": dict(name="Sharp rush", turkish="Kofa", latin="Juncus acutus", layer="emergent",
                 form="tussock", foliage="not found", status="keep, away from paths and the wading strip",
                 h_range=(0.6, 1.0), h_m=0.8,                # "(40-)60-100 cm" S65
                 crown_m=0.8,                                # "dense tussock" S60, S65: rule 1.0 x h
                 bloom=[], leaf=[],                          # "summer" S65 (NZ): no months
                 colours=_pla_c("515B26")),                # round 3: dark olive
    "reed": dict(name="Common reed", turkish="Kamış", latin="Phragmites australis", layer="emergent",
                 form="stand", foliage="deciduous (S2)", status="lined off-line basins only (D2 a): pla_reed_basin",
                 h_range=(None, 6.0), h_m=3.0,               # "may reach 20 feet (6 m)" S2 (booklet drew 1.9-2.2 m)
                 crown_m=None,                               # clonal stand, no crown
                 bloom=[7, 8, 9, 10, 11], leaf=[],           # "July to November" S2 (range-wide); plumes cut before Nov
                 colours=_pla_c("C2A873", PLA_REED_HEAD)),   # round 3: straw (ΔE00 12.4 to the free-planted species)
    "mint": dict(name="Water mint", turkish="Su nanesi", latin="Mentha aquatica", layer="emergent",
                 form="mound", foliage="deciduous (S57)", status="lined basin cells only (D6): pla_mint_cell",
                 h_range=(0.3, 0.8), h_m=0.55,               # "30-80 cm" S58
                 crown_m=0.75,                               # "spread 0.5-1 m" S57
                 bloom=[5, 6, 7, 8, 9], leaf=[],             # "May-Sep" S58
                 colours=_pla_c("5F9C9E")),                # round 3: blue mint green (ΔE00 12.8)
    "giant_reed": dict(name="Giant reed", turkish="Kargı", latin="Arundo donax", layer="emergent",
                       form="cane", foliage="not found", status="REMOVE (raises flood risk, S36)",
                       h_range=(None, None), h_m=None, crown_m=None,   # not in species_data: pass h_m and crown_m
                       bloom=[], leaf=[],
                       colours=_pla_c(PLA_BEYOND, PLA_REMOVE)),
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


# ---- round 4 (S3, D6, G-R4-6; PLAN §4.9, §2.1): seasons, states and colours ------------------------------------------
# Every plant call takes season= (None = the general state; "winter" Dec-Feb, "spring" Mar-May, "summer" Jun-Aug,
# "autumn" Sep-Nov); month= (1-12) is kept as an alias that maps to its season. The STATE of a species in a season
# comes from its sourced months only (leaf list, bloom list, flower heads cut; CHK5_6 §4): a deciduous species with no
# leaf month in the season is bare (winter: branches with open gaps, round 3 D7); spring = after leaf-out (fresh
# tint); autumn = before leaf-fall (warm tint); flowers where a bloom month falls in the season and is not a cut
# month. The general state = the species in leaf with its flowers (U69). COLOURS: the round 3 values are kept as they
# are (Aras 1 Nov 11:42, N2 halted till 2 Nov): none is sourced yet, every colour entry carries src = PLA_COLOUR_SRC
# and the log prints "FLAG plant colours pending research". Next round fills PLA_SPECIES colours, the two tints and
# the crop colours from research/plant_colours.md (one data edit here). Never alpha.
PLA_COLOUR_SRC = "pending research/plant_colours.md"
PLA_SEASONS = ("winter", "spring", "summer", "autumn")
PLA_SEASON_MONTHS = dict(winter=(12, 1, 2), spring=(3, 4, 5), summer=(6, 7, 8), autumn=(9, 10, 11))
PLA_SPRING = "B8C77A"      # fresh leaf tint (round 3 drawing rule, kept; colour pending research)
PLA_AUTUMN = "C29A55"      # autumn tint (round 3 drawing rule, kept; colour pending research)
PLA_TINT = dict(spring=PLA_SPRING, autumn=PLA_AUTUMN)
PLA_TINT_T = dict(spring=0.22, autumn=0.35)   # round 3 month tints (Apr .30 May .15 / Sep .15 Oct .35 Nov .55) averaged
PLA_SEASON = dict(season=None)   # pla_season(s): every plant call without season= / month= draws season s
PLA_BARE_DRAWN = set()
# where each species' STATES come from (colours: PLA_COLOUR_SRC for all); the S-numbers as in species.json
PLA_STATE_SRC = dict(
    plane="leaf: site Sentinel-2 leaf-out 16 Apr, leaf-fall 14 Nov (RESULT §B); bloom Apr-May S69",
    ash="leaf: site Sentinel-2; bloom 'early spring or even in autumn' S7 (no months: no flowers drawn)",
    willow="leaf: site Sentinel-2; catkins 'spring' S4 (no months: none drawn)",
    olive="evergreen S72; full bloom 21-24 Apr S73; harvest 6-14 Nov (Kaya 2017)",
    stone_pine="evergreen conifer S74",
    tamarisk="leaf: site Sentinel-2 (deciduous S9b, genus); bloom not sourced",
    chaste="leaf: site Sentinel-2 (deciduous S58); bloom (Apr-)Jun-Sep S58",
    rosemary="evergreen S58, S71; bloom Jan-May S58",
    lavender="evergreen UNVERIFIED; bloom Mar-May S58",
    loosestrife="herbaceous perennial; bloom Jun-Sep S19; heads cut Sep (D6); winter state not sourced",
    soft_rush="bloom late May-Aug S59; winter state not sourced",
    rush="bloom 'summer' S65 (no months); winter state not sourced",
    reed="deciduous S2; plumes Jul-Nov S2, cut before Nov S11",
    mint="deciduous S57; bloom May-Sep S58 (no flower colour)",
    giant_reed="remove (S36)",
)
PLA_SOURCES = dict((k_, dict((s_, dict(colour=PLA_COLOUR_SRC, state=PLA_STATE_SRC.get(k_, "")))
                             for s_ in (None,) + PLA_SEASONS)) for k_ in PLA_SPECIES)


def pla_season_of(season=None, month=None):
    """the season name of season= or month= (a month 1-12 maps to its season); None = the general state"""
    if season is not None:
        if season not in PLA_SEASONS:
            raise ValueError("plants: season is None or one of %s, not %r" % (", ".join(PLA_SEASONS), season))
        return season
    if month:
        m = int(month)
        for s_ in PLA_SEASONS:
            if m in PLA_SEASON_MONTHS[s_]:
                return s_
        raise ValueError("plants: month %r is not 1-12" % month)
    return None


def pla_season(season=None):
    """sets the season (a name, or a month 1-12 = its season; None = general) every plant call without its own
    season= / month= draws in; returns the previous season (pla_season(old) restores it)"""
    old = PLA_SEASON["season"]
    if isinstance(season, (int, float)) and not isinstance(season, bool):
        PLA_SEASON["season"] = pla_season_of(month=season) if season else None
    else:
        PLA_SEASON["season"] = pla_season_of(season or None)
    return old


def _pla_s(season=None, month=None):
    """the season of one call: its own season= / month=, else the one set by pla_season"""
    if season is not None or month:
        return pla_season_of(season, month)
    return PLA_SEASON["season"]


def _pla_deciduous(sp):
    return sp["foliage"].startswith("deciduous") and bool(sp["leaf"])


def pla_state(key, season=None):
    """the sourced state of species `key` in a season: dict(bare, tint, bloom, season) (PLA_STATE_SRC)"""
    sp = PLA_SPECIES[key]
    if season is None:
        return dict(bare=False, tint=None, bloom=bool(sp["colours"].get("accent")), season=None)
    ms = PLA_SEASON_MONTHS[season]
    cut = pla_months(key)["cut"]
    dec = _pla_deciduous(sp)
    bare = dec and not any(m in sp["leaf"] for m in ms)
    tint = season if dec and not bare and season in PLA_TINT else None
    bloom = any(m in sp["bloom"] and m not in cut for m in ms)
    return dict(bare=bare, tint=tint, bloom=bloom, season=season)


def pla_colours(key, season=None, beyond=False, layer=0, month=None):
    """THE plant colour call (G-R4-6): the colour set of species `key` in `season` (None = general; month= alias):
    fill (lit face), shade (mass body), lt (light fleck), edge, stem, bark, accent (flowers; None out of bloom; giant
    reed keeps its 'remove' cross), plus bare (draw the winter structure), bloom, season and src (the colour source:
    PLA_COLOUR_SRC until research/plant_colours.md). beyond / layer: paler beyond the cut and with depth (fig_fade).
    Opaque colours only."""
    sp = PLA_SPECIES[key]
    s_ = _pla_s(season, month)
    st = pla_state(key, s_)
    c = dict(sp["colours"])
    if st["tint"]:
        c["fill"] = _sec_mix(c["fill"], PLA_TINT[st["tint"]], PLA_TINT_T[st["tint"]])
        c["lt"] = _sec_mix(c["fill"], SEC["paper"], 0.35)
    if key != "giant_reed" and c.get("accent") and not st["bloom"]:
        c["accent"] = None
    c["shade"] = _sec_mix(c["fill"], c["edge"], 0.25)
    if beyond:
        c = dict((k_, _sec_mix(v, SEC["paper"], 0.55) if v else v) for k_, v in c.items())
    c = _pla_layer_cols(c, layer)
    bark = _sec_mix(sp["colours"]["fill"], sp["colours"]["stem"] or PLA_TRUNK, 0.6)   # species-tinted twigs
    if beyond:
        bark = _sec_mix(bark, SEC["paper"], 0.55)
    c["bark"] = _pla_layer_cols(dict(b=bark), layer)["b"]
    c.update(bare=st["bare"], bloom=st["bloom"], season=s_, src=PLA_COLOUR_SRC)
    return c


def pla_colour(key, month=None, beyond=False, layer=0, season=None):
    """round 3 name, kept for its callers: = pla_colours(key, season, beyond, layer, month)"""
    return pla_colours(key, season, beyond=beyond, layer=layer, month=month)


def _pla_status(bare_key=None):
    """keeps the one plants status line in PLA_LOG: "plants: no alpha; bare n species (keys)" """
    if bare_key:
        PLA_BARE_DRAWN.add(bare_key)
    ln = u"plants: no alpha; bare %d species%s" % (len(PLA_BARE_DRAWN), (u" (%s)" % u", ".join(sorted(PLA_BARE_DRAWN)))
                                                    if PLA_BARE_DRAWN else u"")
    for i, s_ in enumerate(PLA_LOG):
        if s_.startswith(u"plants: no alpha"):
            PLA_LOG[i] = ln
            return
    PLA_LOG.append(ln)


# bare branch architecture per form (drawing rules): clear stem (fraction of h), main limbs (count, spread deg),
# upward pull, child count, length ratio, pendulous whips
PLA_BARE_FORM = dict(
    dome=dict(lo=0.30, limbs=4, spread=110.0, up=0.15, kids=(2, 3), ratio=(0.62, 0.76)),
    oval=dict(lo=0.30, limbs=3, spread=55.0, up=0.45, kids=(2, 3), ratio=(0.64, 0.78)),
    feathery=dict(lo=0.0, limbs=4, spread=45.0, up=0.35, kids=(2, 2), ratio=(0.60, 0.72)),
    multistem=dict(lo=0.0, limbs=5, spread=70.0, up=0.40, kids=(2, 2), ratio=(0.55, 0.70)),
)


def _pla_bare_sec(form, x, gy, h, w, k, c, seed=0):
    """winter section of a deciduous tree: trunk and recursive branches as tapering lines inside the crown
    envelope, the open gaps between them showing (D7); the willow's winter state is _pla_willow2_sec(bare=True)"""
    import math as _m
    F = PLA_BARE_FORM.get(form, PLA_BARE_FORM["dome"])
    H, R = h * k, w / 2.0 * k
    rnd = _pla_rng(seed * 13 + 5)
    col = c["bark"]
    tw = max(0.12, h / 60.0 * k)
    lo = F["lo"] * H
    ex, ey = x, gy + lo + 0.5 * (H - lo) if lo else gy + 0.55 * H
    erx, ery = R, (0.5 * (H - lo) if lo else 0.45 * H)
    D = 3 if H < 8.0 else (4 if H < 20.0 else 5)
    sh = []

    def inside(px, py):
        return py <= gy + H and ((px - ex) / erx) ** 2 + ((py - ey) / ery) ** 2 <= 1.0 or py < ey and abs(px - ex) <= erx

    def grow(px, py, ang, L, wd, d):
        tx, ty = px + L * _m.cos(ang), py + L * _m.sin(ang)
        n_ = 0
        while not inside(tx, ty) and n_ < 6:
            L *= 0.8
            tx, ty = px + L * _m.cos(ang), py + L * _m.sin(ang)
            n_ += 1
        j = 0.08 * L * (rnd() - 0.5)
        mx, my = px + 0.5 * L * _m.cos(ang) - j * _m.sin(ang), py + 0.5 * L * _m.sin(ang) + j * _m.cos(ang)
        sh.append(("line", [(px, py), (mx, my), (tx, ty)], col, max(0.05, wd)))
        if d >= D:
            return
        nk = F["kids"][0] + (1 if rnd() < 0.4 and F["kids"][1] > F["kids"][0] else 0)
        for i in range(nk):
            off = (i - 0.5 * (nk - 1)) / max(1.0, 0.5 * (nk - 1) + 0.5) * _m.radians(28.0 + 14.0 * rnd())
            a = ang + off
            a = a + F["up"] * (_m.pi / 2.0 - a) * 0.5        # pull toward upright
            r_ = F["ratio"][0] + (F["ratio"][1] - F["ratio"][0]) * rnd()
            grow(tx, ty, a, L * r_, wd * 0.62, d + 1)

    if lo:                                           # trunk up to the first fork, tapering
        fy = gy + lo + 0.08 * (H - lo)
        sh.append(("poly", [(x - tw, gy), (x + tw, gy), (x + 0.6 * tw, fy), (x - 0.6 * tw, fy)], col, None, 0.0))
        base, L0 = (x, fy), 0.42 * (H - lo)
    else:                                            # stems from the ground
        base, L0 = (x, gy), 0.50 * H
    nl = F["limbs"]
    for i in range(nl):
        t = (i / float(nl - 1)) - 0.5 if nl > 1 else 0.0
        a = _m.pi / 2.0 + _m.radians(F["spread"]) * t + _m.radians(10.0) * (rnd() - 0.5)
        grow(base[0] + (0.15 * tw * t if lo else 0.12 * R * t), base[1], a, L0 * (0.85 + 0.25 * rnd()),
             (1.1 * tw if lo else 0.5 * tw), 1)
    return sh


def _pla_bare_plan(cx, cy, r, c, seed=0):
    """winter plan of a deciduous crown: main branches radiating and forking, open between them, the trunk dot"""
    import math as _m
    rnd = _pla_rng(seed * 17 + 3)
    col = c["bark"]
    sh = []

    def grow(px, py, ang, L, wd, d):
        tx, ty = px + L * _m.cos(ang), py + L * _m.sin(ang)
        if _m.hypot(tx - cx, ty - cy) > r:
            s_ = r / _m.hypot(tx - cx, ty - cy)
            tx, ty = cx + (tx - cx) * s_, cy + (ty - cy) * s_
        sh.append(("line", [(px, py), (tx, ty)], col, max(0.05, wd)))
        if d < 3:
            for o in (-0.45, 0.4):
                grow(tx, ty, ang + o + 0.2 * (rnd() - 0.5), L * 0.62, wd * 0.6, d + 1)
    n = 5 + int(rnd() * 2.999)
    for i in range(n):
        grow(cx, cy, 2 * _m.pi * (i + 0.3 * rnd()) / n, 0.45 * r, max(0.08, 0.05 * r), 1)
    sh.append(("poly", sec_ellipse(cx, cy, max(0.2, 0.06 * r), max(0.2, 0.06 * r), 10), col, None, 0.0))
    return sh


def _pla_bare_draw(key, sp, x, g, h, w, k, c, seed, plan=False):
    """the winter structure of a species (willow v2 skeleton or the form's branch architecture), counted bare"""
    _pla_status(key)
    if key == "willow":
        return _pla_willow2_plan(x, g, w / 2.0 * k, c, seed, bare=True) if plan else \
            _pla_willow2_sec(x, g, h, w, k, c, seed, bare=True)
    if plan:
        return _pla_bare_plan(x, g, w / 2.0 * k, c, seed)
    return _pla_bare_sec(sp["form"], x, g, h, w, k, c, seed)


def pla_bare(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0, layer=0, month=None, plan=False,
             season=None):
    """D7 winter tree: species `key` without leaves as its branch structure with the open gaps between branches, in
    its species-tinted bark colour, true size (section: ground at (x, gy); plan=True: crown centred on (x, gy) page
    mm), paler beyond / with depth. season / month default winter. Opaque lines and the trunk only. Returns shapes."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    if h_m is not None:
        h = pla_height_ok(key, h)
    s_ = _pla_s(season, month) or "winter"
    c = pla_colours(key, s_, beyond=beyond, layer=layer)
    _pla_count(key, s_)
    c0 = pla_colours(key, s_)
    if plan:
        img = _pla_img_draw(key, s_, "top", x, gy, h, w, k, c0, seed, beyond, 0, True) or \
            _pla_missing_draw(key, s_, "top", x, gy, w, w, k)
        return img if img is not None else _pla_bare_draw(key, sp, x, gy, h, w, k, c, seed, plan=True)
    sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
    g = gy(x) if callable(gy) else gy
    img = _pla_img_draw(key, s_, "side", x, g, h, w, k * sc, c0, seed, beyond, layer, True) or \
        _pla_missing_draw(key, s_, "side", x, g, h, w, k * sc)
    return img if img is not None else _pla_bare_draw(key, sp, x, g, h, w, k * sc, c, seed)


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


# ---- round 4 (S3, D4, G-R4-6): print-quality crowns. Every crown = several overlapping, irregular leaf masses with
# open gaps between them; each mass in tones of its species (shade body with a fine edge, lit face toward the upper
# left, a small light fleck); trunk and main limbs drawn first so they show in the gaps. Plan and section are built
# from the same masses. Counts, sizes, offsets and the light direction are drawing rules, not data.
def _pla_mass(mx, my, rx, up, dn, c, seed, wob=0.2, edge=True):
    """one leaf mass centred (mx, my), rx each side, up above, dn below: shade body, lit face, light fleck"""
    sh = [("poly", _pla_crown(mx, my, rx, up, dn, seed, wob), c["shade"], c["edge"] if edge else None,
           0.06 if edge else 0.0)]
    sh.append(("poly", _pla_crown(mx - 0.12 * rx, my + 0.10 * up, 0.74 * rx, 0.78 * up, 0.55 * dn, seed + 1, wob),
               c["fill"], None, 0.0))
    sh.append(("poly", _pla_crown(mx - 0.30 * rx, my + 0.34 * up, 0.30 * rx, 0.30 * up, 0.24 * dn, seed + 2, wob),
               c["lt"], None, 0.0))
    return sh


def _pla_cloud(cx, cy, rx, ry, n, c, seed, wob=0.2, size=0.46, flat=1.0):
    """a crown of n leaf masses inside the ellipse (cx, cy, rx, ry) (page mm), the upper masses first so the lower
    ones overlap them; returns (shapes, masses [(x, y, rx, ry)])"""
    rnd = _pla_rng(seed * 19 + 7)
    pts = _pla_marks_in(cx, cy, (1.0 - 1.1 * size) * rx, (1.0 - 1.1 * size) * ry, n, rnd)
    ms = []
    for i, (px, py) in enumerate(pts):
        f = 0.82 + 0.36 * rnd()
        ms.append((px, py, size * rx * f, size * ry * f * flat, i))
    ms.sort(key=lambda m_: -m_[1])
    sh = []
    for px, py, mrx, mry, i in ms:
        sh += _pla_mass(px, py, mrx, mry, 0.85 * mry, c, seed * 7 + 3 * i, wob)
    return sh, [(m_[0], m_[1], m_[2], m_[3]) for m_ in ms]


# ---- white willow v2 (round 4, D1, S3): ONE drawing for every section, plan, axo, the p17 catalogue and winter, from
# the p17 catalogue photo (Commons "A big white willow tree (Salix alba) at the bay of lake Juojärvi in Tuusniemi,
# Finland, 2018 September": a massive leaning trunk forking low into heavy spreading limbs). One skeleton
# (_pla_willow2_skel): a stout leaning trunk, four arching limbs, two branches per limb, twigs. In leaf: a leaf mass at
# every branch end (_pla_mass), open gaps where the limbs show, the weeping fringe hanging from each mass. Winter: the
# same skeleton bare with fine hanging whips. Height: drawing size 15 m inside the sourced "up to 30.00 m" [35];
# crown 0.7 x h (rule: no sourced width, flagged). Proportions are drawing rules. Replaces the round 3 willow
# (its section, plan, mass table and the bare "weeping" whips), all deleted.
PLA_WILLOW_LIMBS = ((-0.72, 0.60), (-0.30, 0.84), (0.18, 0.90), (0.68, 0.64))   # limb tips (dx / R, y / H)


def _pla_willow2_skel(x, gy, H, R, seed):
    """the willow skeleton in section, page mm, mirrored on odd seeds: (trunk ring, branches [(pts, lw)],
    ends [(x, y, depth)], twigs [(pts, lw)])"""
    import math as _m
    rnd = _pla_rng(seed * 7 + 11)
    s = -1.0 if seed % 2 else 1.0
    tw = max(0.2, H / 36.0)                         # stout trunk: 1/18 of the height wide at the foot (rule)
    fx, fy = x + s * 0.12 * R, gy + 0.24 * H        # the low fork the trunk leans to
    trunk = [(x - 1.35 * tw, gy), (x + 1.35 * tw, gy), (x + tw + s * 0.04 * R, gy + 0.10 * H),
             (fx + 0.8 * tw, fy), (fx - 0.8 * tw, fy), (x - tw + s * 0.04 * R, gy + 0.10 * H)]

    def cx_(v):
        return max(x - 0.97 * R, min(x + 0.97 * R, v))
    br, ends, twigs = [], [], []
    for dx, ty in PLA_WILLOW_LIMBS:
        lx = cx_(x + s * dx * R * (0.94 + 0.12 * rnd()))
        ly = min(gy + ty * H * (0.95 + 0.08 * rnd()), gy + 0.93 * H)
        mx, my = 0.5 * (fx + lx), 0.5 * (fy + ly) + 0.06 * H     # limbs arch upward
        br.append(([(fx, fy), (mx, my)], 1.1 * tw))
        br.append(([(mx, my), (lx, ly)], 0.65 * tw))
        ends.append((lx, ly, 1))
        o = 1.0 if lx >= fx else -1.0
        px, py = mx + 0.6 * (lx - mx), my + 0.6 * (ly - my)
        for ax, ay in ((0.18, -0.08), (-0.12, 0.10)):           # one branch out and down, one up and in
            bx = cx_(lx + o * ax * R * (0.8 + 0.4 * rnd()))
            by = min(gy + 0.96 * H, ly + ay * H * (0.8 + 0.4 * rnd()))
            br.append(([(px, py), (0.5 * (px + bx), 0.5 * (py + by) + 0.02 * H), (bx, by)], 0.35 * tw))
            ends.append((bx, by, 2))
    for ex, ey, _d in ends:                         # twigs: two or three short ones from every end
        for j in range(2 + int(rnd() * 1.999)):
            a = 1.2 + 0.75 * j + 0.4 * rnd()
            L = (0.07 + 0.06 * rnd()) * R
            twigs.append(([(ex, ey), (cx_(ex + L * (1.0 if j % 2 else -1.0) * abs(_m.cos(a))),
                                     min(gy + H, ey + 0.6 * L))], 0.06))
    return trunk, br, ends, twigs


def _pla_willow2_sec(x, gy, h, w, k, c, seed=0, bare=False):
    """white willow v2 in section, h tall and w wide (m), ground at (x, gy) page mm; bare = the winter state"""
    H, R = h * k, w / 2.0 * k
    trunk, br, ends, twigs = _pla_willow2_skel(x, gy, H, R, seed)
    rnd = _pla_rng(seed * 5 + 3)
    col = c["bark"] if bare else c["stem"]
    sh = [("poly", trunk, col, None, 0.0)] + [("line", p, col, max(0.06, lw)) for p, lw in br]
    if bare:                                        # winter: twigs and fine hanging whips, open gaps between them
        sh += [("line", p, col, lw) for p, lw in twigs]
        for p, _lw in twigs:
            tx, ty = p[-1]
            yb = max(gy + 0.15 * H, ty - (0.15 + 0.15 * rnd()) * H)
            o = 1.0 if tx >= x else -1.0
            sh.append(("line", [(tx, ty), (tx + o * 0.02 * R, 0.5 * (ty + yb)), (tx + o * 0.03 * R, yb)], col, 0.05))
        return sh
    strand = _sec_mix(c["shade"], c["edge"], 0.35)
    ms = []
    for i, (ex, ey, d) in enumerate(ends):
        f = 0.85 + 0.30 * rnd()
        mrx = (0.24 if d == 1 else 0.18) * R * f
        up = (0.11 if d == 1 else 0.09) * H * f
        ey = min(ey, gy + H - up)
        ms.append((ex, ey, mrx, up, i))
    ms.sort(key=lambda m_: -m_[1])                  # upper masses first: the lower ones overlap them
    for mx, my, mrx, up, i in ms:
        sh += _pla_mass(mx, my, mrx, up, 0.8 * up, c, seed * 13 + 3 * i, 0.22)
        n_ = max(4, int(mrx / max(0.3, 0.04 * R)))   # the weeping fringe hanging from the mass
        for j in range(n_):
            t = -0.85 + 1.7 * (j + 0.5 * rnd()) / n_
            px = mx + t * mrx
            top = my - 0.55 * up * (1.0 - t * t) ** 0.5
            yb = max(gy + 0.18 * H, top - (0.10 + 0.15 * rnd()) * H)
            lean = (0.02 + 0.02 * rnd()) * R * (1.0 if px >= x else -1.0)
            if j % 2 == 0:
                wd = 0.05 * mrx + 0.05
                sh.append(("poly", [(px - wd, top), (px + wd, top), (px + lean + 0.15 * wd, yb),
                                    (px + lean - 0.15 * wd, yb)], c["shade"] if j % 4 == 0 else c["fill"], None, 0.0))
            else:
                sh.append(("line", [(px, top), (px + 0.5 * lean, 0.5 * (top + yb)), (px + lean, yb)], strand, 0.06))
    return sh


def _pla_willow2_plan(cx, cy, r, c, seed=0, bare=False):
    """white willow v2 from above, crown radius r (page mm) on (cx, cy): the same four limbs and their branches
    radiating, a leaf mass at every end (outer first, the crown top last), strand ticks round the rim; bare = winter"""
    import math as _m
    rnd = _pla_rng(seed * 5 + 9)
    a0 = 2 * _m.pi * rnd()
    col = c["bark"] if bare else c["stem"]
    lw0 = max(0.10, 0.05 * r)
    sh, ends = [], []
    for i in range(4):
        a = a0 + 2 * _m.pi * (i / 4.0 + 0.10 * (rnd() - 0.5))
        lx, ly = cx + 0.62 * r * _m.cos(a), cy + 0.62 * r * _m.sin(a)
        sh.append(("line", [(cx, cy), (lx, ly)], col, lw0))
        ends.append((lx, ly, 1, a))
        for o in (-0.38, 0.38):
            b = a + o + 0.1 * (rnd() - 0.5)
            bx, by = lx + 0.24 * r * _m.cos(b), ly + 0.24 * r * _m.sin(b)
            sh.append(("line", [(lx, ly), (bx, by)], col, 0.6 * lw0))
            ends.append((bx, by, 2, b))
    if bare:
        for ex, ey, _d, a in ends:
            for o in (-0.3, 0.3):
                sh.append(("line", [(ex, ey), (ex + 0.08 * r * _m.cos(a + o), ey + 0.08 * r * _m.sin(a + o))], col,
                           0.06))
        sh.append(("poly", sec_ellipse(cx, cy, max(0.2, 0.06 * r), max(0.2, 0.06 * r), 10), col, None, 0.0))
        return sh
    for ex, ey, d, a in sorted(ends, key=lambda e_: -e_[2]):     # outer branch ends first
        mr = (0.26 if d == 1 else 0.20) * r * (0.85 + 0.3 * rnd())
        sh += _pla_mass(ex, ey, mr, mr, mr, c, seed * 11 + int(100 * a), 0.22)
        if d == 2:                                  # the fringe seen from above: short ticks past the mass
            for j in range(4):
                b = a + 0.35 * (j - 1.5)
                p0 = (ex + 0.75 * mr * _m.cos(b), ey + 0.75 * mr * _m.sin(b))
                sh.append(("line", [p0, (p0[0] + 0.12 * r * _m.cos(b), p0[1] + 0.12 * r * _m.sin(b))], c["shade"],
                           0.07))
    sh += _pla_mass(cx, cy, 0.30 * r, 0.30 * r, 0.30 * r, c, seed + 7, 0.2)
    return sh


# tree crowns per form (drawing rules): clear stem / h, masses in section, masses in plan, mass size, flatness, limbs
PLA_CROWN = dict(dome=(0.30, 9, 7, 0.44, 1.0, 4), oval=(0.28, 8, 6, 0.46, 1.0, 3),
                 gnarled=(0.30, 7, 6, 0.46, 0.85, 3), umbrella=(0.65, 8, 7, 0.36, 0.80, 4),
                 feathery=(0.0, 9, 8, 0.38, 1.0, 4))


def _pla_tree_sec(form, x, gy, h, w, k, c, seed=0):
    """a tree in section (round 4, D4): trunk and main limbs, then the crown of overlapping two-tone leaf masses
    with open gaps (_pla_cloud); h tall, w crown wide (m), ground at (x, gy) page mm"""
    lo_f, n, _np, size, flat, nl = PLA_CROWN[form]
    H, R = h * k, w / 2.0 * k
    st = c["stem"]
    tw = max(0.15, h / 60.0 * k)                    # half trunk width: trunk 1/30 of the height (rule)
    sh = []
    if form == "feathery":                          # tamarisk: slender stems from the ground into an airy crown
        cy, ry = gy + 0.62 * H, 0.38 * H
        for i in range(4):
            t = (i - 1.5) / 1.5
            sh.append(("line", [(x + t * 0.05 * R, gy), (x + t * 0.25 * R, gy + 0.35 * H),
                                (x + t * 0.55 * R, cy)], st, max(0.08, 0.6 * tw)))
    else:
        yb = gy + lo_f * H
        y0 = yb - 0.05 * (gy + H - yb)              # the crown starts a little below the first fork
        cy, ry = 0.5 * (y0 + gy + H), 0.5 * (gy + H - y0)
        if form == "gnarled":                       # olive: two twisting stems
            for s_ in (-1, 1):
                sh.append(("poly", [(x + s_ * 0.2 * tw, gy), (x + s_ * 1.6 * tw, gy),
                                    (x + s_ * (0.35 * R + 0.5 * tw), cy), (x + s_ * (0.35 * R - 0.5 * tw), cy)],
                           st, None, 0.0))
        else:
            lean = 0.03 * H if form == "umbrella" else 0.0
            sh.append(("poly", [(x - tw, gy), (x + tw, gy), (x + lean + 0.6 * tw, yb), (x + lean - 0.6 * tw, yb)],
                       st, None, 0.0))
        for i in range(nl):                         # main limbs into the crown, a side branch on each
            t = (2.0 * i / (nl - 1) - 1.0) if nl > 1 else 0.0
            ex, ey = x + 0.72 * R * t, cy + 0.45 * ry * (1.0 - abs(t))
            sh.append(("line", [(x, yb), (0.5 * (x + ex), 0.5 * (yb + ey) + 0.1 * ry), (ex, ey)], st,
                       max(0.08, 0.7 * tw)))
            o = 1.0 if t >= 0 else -1.0
            sh.append(("line", [(0.5 * (x + ex), 0.5 * (yb + ey) + 0.1 * ry),
                                (0.5 * (x + ex) + o * 0.2 * R, min(gy + H, ey + 0.4 * ry))], st, max(0.06, 0.4 * tw)))
    cl, ms = _pla_cloud(x, cy, R, ry, n, c, seed, size=size, flat=flat)
    sh += cl
    if form == "feathery":                          # hanging wisps under the masses
        for mx, my, mrx, mry in ms:
            for d in (-0.5, 0.0, 0.5):
                px, py = mx + d * mrx, my - 0.7 * mry
                sh.append(("line", [(px, py), (px + 0.04 * (px - x), py - 0.09 * H)], c["edge"], 0.06))
    return sh


def _pla_sec(form, x, gy, h, w, k, c, seed=0):
    """Section of one form, h tall and w crown wide (m), ground at (x, gy) page mm (round 4: print quality, D4)."""
    H, R = h * k, w / 2.0 * k
    f, e, ac = c["fill"], c["edge"], c.get("accent")
    sh = []
    if form == "weeping":                           # white willow v2 (D1)
        return _pla_willow2_sec(x, gy, h, w, k, c, seed)
    if form in PLA_CROWN:
        return _pla_tree_sec(form, x, gy, h, w, k, c, seed)
    rnd = _pla_rng(seed * 29 + 5)
    if form == "multistem":                         # chaste tree: stems fanning from the ground, a mass on each
        heads = ((-0.68, 0.58), (-0.36, 0.70), (0.0, 0.76), (0.34, 0.69), (0.68, 0.57))
        for dx, cy_ in heads:
            sh.append(("line", [(x + dx * 0.1 * R, gy), (x + dx * 0.55 * R, gy + 0.4 * cy_ * H),
                                (x + dx * R, gy + cy_ * H)], c["stem"], 0.15))
        for i, (dx, cy_) in sorted(enumerate(heads), key=lambda t_: -t_[1][1]):
            up = 0.22 * H * (0.9 + 0.2 * rnd())
            sh += _pla_mass(x + dx * R, gy + cy_ * H, 0.32 * R, up, 0.85 * up, c, seed * 5 + i, 0.16)
        if ac:                                      # flower spikes upright from the top of each mass
            for dx, cy_ in heads:
                top = gy + (cy_ + 0.20) * H
                for d in (-0.12, 0.0, 0.12):
                    px = x + (dx + d) * R
                    sh.append(("line", [(px, top - 0.14 * H), (px + 0.02 * R, top + 0.04 * H)], ac, 0.3))
        return sh
    if form == "mound":                             # lavender, rosemary, water mint: overlapping low masses
        for i, d in enumerate((-0.45, 0.42, 0.0)):
            up = (0.62 if d == 0.0 else 0.52) * H * (0.9 + 0.2 * rnd())
            sh += _pla_mass(x + d * R, gy + 0.36 * H, (0.52 if d == 0.0 else 0.50) * R, up, 0.36 * H, c,
                            seed * 3 + i, 0.12)
        if ac:                                      # flower spikes above the mound, a bract head on each
            for d in (-0.55, -0.25, 0.05, 0.32, 0.58):
                px, top = x + d * R, gy + (0.95 + 0.12 * rnd()) * H
                sh.append(("line", [(px, gy + 0.70 * H), (px + 0.05 * d * R, top)], c["stem"], 0.08))
                sh.append(("poly", sec_ellipse(px + 0.05 * d * R, top, 0.05 * R + 0.08, 0.08 * H + 0.1, 8), ac,
                           None, 0.0))
        else:                                       # needle-leaf strokes in the edge tone
            for d in (-0.55, -0.25, 0.05, 0.35, 0.6):
                sh.append(("line", [(x + d * R, gy + 0.45 * H), (x + d * R * 1.05, gy + 0.78 * H)], e, 0.07))
        return sh
    if form in ("clump", "tussock", "cane"):        # rushes and loosestrife: stems from one base; giant reed: canes
        n = dict(clump=15, tussock=23, cane=7)[form]
        for i in range(n):
            t = i / float(n - 1)
            hh = H * (0.80 + 0.20 * _pla_rnd(i, seed + 3))
            bx, tx = x + (2 * t - 1) * R * 0.15, x + (2 * t - 1) * R
            col = f if i % 3 else c["shade"]        # two tones through the clump
            if form == "clump":                     # soft arch
                mx = bx + (tx - bx) * 0.35
                sh.append(("line", [(bx, gy), (mx, gy + 0.55 * hh), (tx, gy + hh)], col, 0.12))
                if ac and i % 2 == 0:               # loosestrife flower spike on the upper stem
                    sh.append(("line", [(mx + (tx - mx) * 0.3, gy + 0.69 * hh), (tx, gy + hh)], ac, 0.35))
            else:
                sh.append(("line", [(bx, gy), (tx, gy + hh)], col, 0.15 if form == "cane" else 0.1))
                if form == "cane":                  # leaf blades along the cane
                    for j in range(1, 5):
                        py = gy + hh * j / 5.0
                        px = bx + (tx - bx) * j / 5.0
                        s_ = 1 if (i + j) % 2 else -1
                        sh.append(("line", [(px, py), (px + s_ * 0.35 * R, py - 0.06 * hh)], f, 0.1))
        if form == "cane" and ac:                   # marked for removal
            sh.append(("line", [(x - R, gy), (x + R, gy + H)], ac, 0.35))
            sh.append(("line", [(x - R, gy + H), (x + R, gy)], ac, 0.35))
        return sh
    raise ValueError("_pla_sec: unknown form %r" % form)


def _pla_plan(form, cx, cy, w, k, c, seed=0):
    """Top view of one form, crown w wide (m), centre (cx, cy) page mm: the same masses as the section (round 4)."""
    import math as _m
    r = w / 2.0 * k
    f, e, ac = c["fill"], c["edge"], c.get("accent")
    sh = []
    if form == "weeping":                           # white willow v2 (D1)
        return _pla_willow2_plan(cx, cy, r, c, seed)
    if form in PLA_CROWN:
        _lo, _n, n, size, _fl, nl = PLA_CROWN[form]
        for i in range(nl + 1):                     # limbs, seen in the gaps between the masses
            a = 2 * _m.pi * (i / float(nl + 1) + 0.2 * _pla_rnd(seed, 5))
            sh.append(("line", [(cx, cy), (cx + 0.7 * r * _m.cos(a), cy + 0.7 * r * _m.sin(a))], c["stem"],
                       max(0.08, 0.04 * r)))
        cl, _ms = _pla_cloud(cx, cy, r, r, n, c, seed, size=size + 0.04)
        sh += cl
        if form == "umbrella":                      # needle tufts round the flat crown
            for i in range(30):
                a = 2 * _m.pi * i / 30.0
                sh.append(("line", [(cx + 0.80 * r * _m.cos(a), cy + 0.80 * r * _m.sin(a)),
                                    (cx + 0.98 * r * _m.cos(a), cy + 0.98 * r * _m.sin(a))], c["lt"], 0.08))
        elif form == "feathery":                    # feathery sprays at the rim
            for i in range(24):
                a = 2 * _m.pi * i / 24.0
                sh.append(("line", [(cx + 0.82 * r * _m.cos(a), cy + 0.82 * r * _m.sin(a)),
                                    (cx + 0.82 * r * _m.cos(a + 0.12), cy + 0.82 * r * _m.sin(a + 0.12))], e, 0.07))
        return sh
    if form == "multistem":                         # five heads, as in section
        for i in range(5):
            a = 2 * _m.pi * (i / 5.0 + 0.05)
            hx, hy = cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a)
            sh += _pla_mass(hx, hy, 0.45 * r, 0.45 * r, 0.45 * r, c, seed + i, 0.12)
            if ac:
                for d in ((-0.15, 0.1), (0.12, 0.18), (0.0, -0.12)):
                    sh.append(("poly", sec_ellipse(hx + d[0] * r, hy + d[1] * r, 0.07 * r + 0.05, 0.07 * r + 0.05, 8),
                               ac, None, 0.0))
        return sh
    if form == "mound":
        for i, (dx, dy, s_) in enumerate(((-0.35, -0.2, 0.62), (0.32, -0.15, 0.6), (0.0, 0.25, 0.62))):
            sh += _pla_mass(cx + dx * r, cy + dy * r, s_ * r, s_ * r, s_ * r, c, seed + i, 0.1)
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + _pla_rnd(seed, 6))
            px, py = cx + 0.5 * r * _m.cos(a), cy + 0.5 * r * _m.sin(a)
            if ac:
                sh.append(("poly", sec_ellipse(px, py, 0.12 * r, 0.12 * r, 8), ac, None, 0.0))
            else:
                sh.append(("line", [(px, py), (px + 0.2 * r * _m.cos(a), py + 0.2 * r * _m.sin(a))], e, 0.07))
        return sh
    if form in ("clump", "tussock", "cane"):        # stems seen from above: a starburst in two tones
        n = dict(clump=15, tussock=23, cane=9)[form]
        for i in range(n):
            a = 2 * _m.pi * (i / float(n) + 0.3 * _pla_rnd(i, seed))
            ll = r * (0.8 + 0.2 * _pla_rnd(i, seed + 2))
            sh.append(("line", [(cx, cy), (cx + ll * _m.cos(a), cy + ll * _m.sin(a))], f if i % 3 else c["shade"],
                       0.12))
            if ac and form == "clump" and i % 2 == 0:
                sh.append(("poly", sec_ellipse(cx + ll * _m.cos(a), cy + ll * _m.sin(a), 0.08 * r + 0.1,
                                               0.08 * r + 0.1, 8), ac, None, 0.0))
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


PLA_LOG = []
# round 4 (S3) counters for the log lines (pla_log_lines): plants drawn per species / crop, species per season
PLA_COUNT = {}
PLA_SEASON_KEYS = {}


def _pla_count(key, season):
    PLA_COUNT[key] = PLA_COUNT.get(key, 0) + 1
    PLA_SEASON_KEYS.setdefault(season or "general", set()).add(key)


def pla_log_lines():
    """the plant log lines of this run (sec_look_lines prints them): willow v2 drawn n; plants drawn by species;
    plants season=<season> species n (one per season drawn; 'general' = no season); FLAG plant colours pending
    research (n species: every species and crop, until research/plant_colours.md fills the colours)"""
    wf = sorted(set(v for (k_, _s, _v), v in PLA_IMG_FILE.items() if k_ == "willow"))
    out = [u"willow v3 image=%s (drawn %d)" % (u", ".join(wf) if wf else
                                               u"none (pending Data/plants/willow_<state>_side.png)",
                                               PLA_COUNT.get("willow", 0)),
           u"plants drawn by species: " + (u", ".join(u"%s %d" % kv for kv in sorted(PLA_COUNT.items())) or u"none")]
    by = {}
    for sk, src in PLA_SRC.items():                       # round 5: species x state (x view) per image source
        by.setdefault(src or "vector_fallback", set()).add(sk)
    out.append(u"plants source=" + u", ".join(u"%s %d" % (k_, len(v)) for k_, v in sorted(by.items())) +
               u" species×state" if by else u"plants source=none drawn")
    miss = sorted(by.get("vector_fallback", set()) | by.get("placeholder", set()))
    if miss:
        out.append(u"FLAG plants without image %d species×state (view): %s" % (
            len(miss), u", ".join(u"%s %s (%s)" % m for m in miss[:40]) + (u" ..." if len(miss) > 40 else u"")))
    if PLA_TONE_LOG:
        out.append(u"plants toned: " + u", ".join(u"%s %d" % kv for kv in sorted(PLA_TONE_LOG.items())))
    for s_ in ("general",) + PLA_SEASONS:
        if s_ in PLA_SEASON_KEYS:
            out.append(u"plants season=%s species %d" % (s_, len(PLA_SEASON_KEYS[s_])))
    n = len(PLA_SPECIES) + len([c_ for c_ in PLA_CROPS if c_ != "olive"])
    out.append(u"FLAG plant colours pending research (%d species): %s" % (n, PLA_COLOUR_SRC))
    return out


def pla_height_ok(key, h_m):
    """h_m (m) moved into the species' sourced range (G6; T1: the olive was drawn 5.0 m against 8-15 m); a change is
    logged once per species and value"""
    lo, hi = PLA_SPECIES[key]["h_range"]
    v = h_m
    if lo is not None and v < lo:
        v = lo
    if hi is not None and v > hi:
        v = hi
    if v != h_m:
        msg = u"Plants: %s asked at %.2f m, drawn %.2f m (sourced %s-%s m)" % (key, h_m, v, lo or "", hi or "")
        if msg not in PLA_LOG:
            PLA_LOG.append(msg)
    return v


def _pla_layer_cols(c, layer):
    f = globals().get("fig_fade")
    if not layer or f is None:
        return c
    return dict((k_, f(v, layer) if v else v) for k_, v in c.items())


# ---- round 5 (S4, G-R5-6, D4, D10, N2 a; PLAN §3 Plants): plant module v3, every plant from a real image ---------------
# One image per species x state (states: general, spring, summer, autumn, winter), cut out and toned to the
# species' colours (pla_colours: the colours stay "pending research/plant_colours.md" until that file arrives; one
# data edit then re-tones every image, because the toned copies are cached under a key that holds the colours).
# Where an image comes from, first found wins (side views; plan views use 1 only):
#   1. asset_png  Downloads/Bergama/Data/plants/<key>_<state>_<view>.png (view side | top; the asset-library project
#                 delivers them: handover/ASSET_PROMPT_plants.md; transparent, plant standing on the bottom edge).
#                 A seasonal state with no own file but a <key>_general_ file uses that one tinted for the season
#                 (never for a bare winter state).
#   2. cutout     Data/cutouts/<species key> (watercolour sheet, species assigned by look, in leaf only: CHK-4 §4.2)
#   3. hires      Data/assets_hires.json PhyloPic silhouettes (plane, plane_bare, ash, olive, stone_pine, maize,
#                 tomato; plane and ash are stand-in species: CHK-4 §4.1), flat in the species colour
#   4. none       pla_missing("vector") = the round 4 drawing (default, so no page goes blank; counted and FLAGged),
#                 pla_missing("placeholder") = a labelled dashed box (the D4 sample sheet shows what is missing)
# Images keep their own proportions (never stretched): height = the species' drawing height, width from the image.
# pla_images(False) turns raster images off for pages that cannot place images (CHK-3 §3.5: site board p02/p03,
# masterplan p17/p24): hires silhouettes and the fallback are used there.
# Logs (pla_log_lines): "plants source=<image> species×state n" per source, "willow v3 image=<file>|none",
# "FLAG plants without image ..." while any species x state has none.
PLA_IMG = dict(on=True, missing="vector")
PLA_IMG_TONE_KEEP = 0.25          # share of the photo's own colour kept when toning (0.45 in bloom): drawing rule
PLA_IMG_HIRES = dict(plane=("plane", "plane_bare"), ash=("ash", None), olive=("olive", "olive"),
                     stone_pine=("stone_pine", "stone_pine"), maize=("maize", None), tomato=("tomato", None))
PLA_SRC = {}                      # (key, state, view) -> source of the last drawing ("asset_png", "cutout", ...)
PLA_IMG_FILE = {}                 # (key, state, view) -> file used
PLA_TONE_LOG = {}                 # "numpy" / "lut" / failure -> count


def pla_img_dir():
    import os as _o
    return _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", "Data", "plants")


def pla_images(on=True):
    """raster plant images on (True) or off (False: hires silhouettes and the fallback only); returns the old value"""
    old = PLA_IMG["on"]
    PLA_IMG["on"] = bool(on)
    return old


def pla_missing(mode="vector"):
    """what is drawn where no image exists: "vector" (round 4 drawing, FLAGged) or "placeholder" (labelled box)"""
    old = PLA_IMG["missing"]
    PLA_IMG["missing"] = "placeholder" if mode == "placeholder" else "vector"
    return old


def _pla_img_find(key, state, view, bare):
    """(source, ref) of the image for key x state x view: ("asset_png", path) / ("cutout", entries) / ("hires", key)
    / (None, None). state None = general."""
    import os as _o
    st = state or "general"
    if PLA_IMG["on"]:
        d = pla_img_dir()
        for s_ in [st] + ([] if (bare or st == "general") else ["general"]):
            f = _o.path.join(d, "%s_%s_%s.png" % (key, s_, view))
            if _o.path.isfile(f):
                return "asset_png", f
        if view == "side" and not bare:
            lib = sil_cut_library().get(key)
            if lib:
                return "cutout", lib
    if view == "side":
        hk = PLA_IMG_HIRES.get(key, (None, None))[1 if bare else 0]
        hl = globals().get("hr_library")
        if hk and hl and hk in hl():
            return "hires", hk
    return None, None


def _pla_toned(path, c, fade, keep):
    """the toned copy of an image (cached under Downloads/Bergama/cached/plants_toned/), or the image itself"""
    import os as _o
    import hashlib as _h
    try:
        stt = _o.stat(path)
        sig = "%s|%d|%d|%s|%s|%s|%.3f|%.2f|v3" % (path, stt.st_size, int(stt.st_mtime), c["shade"], c["fill"], c["lt"],
                                                 fade, keep)
        root = bg_cache("plants_toned") if "bg_cache" in globals() else _o.path.join(
            _o.path.expanduser("~"), "Downloads", "Bergama", "cached", "plants_toned")
        dst = _o.path.join(root, _h.md5(sig.encode("utf-8")).hexdigest()[:16] + ".png")
        if _o.path.isfile(dst):
            return dst
        ok, how = sil_tone(path, dst, c["shade"], c["fill"], c["lt"], keep, SEC["paper"], fade)
        PLA_TONE_LOG[how] = PLA_TONE_LOG.get(how, 0) + 1
        return dst if ok else path
    except Exception as ex:
        PLA_TONE_LOG["failed " + type(ex).__name__] = PLA_TONE_LOG.get("failed " + type(ex).__name__, 0) + 1
        return path


def _pla_fade(beyond, layer):
    f = fig_depth(layer)[1] if layer and globals().get("fig_depth") else 0.0
    return 1.0 - (1.0 - (0.55 if beyond else 0.0)) * (1.0 - f)


def _pla_img_draw(key, state, view, x, g, h, w, k, c0, seed, beyond, layer, bare):
    """the image drawing of one plant (section: ground at (x, g); plan: crown centred on (x, g)), or None.
    c0 = the species' colours at layer 0, not beyond (pla_colours); h, w in m; k page mm per m (layer-scaled)."""
    src, ref = _pla_img_find(key, state, view, bare)
    sk = (key, state or "general", view)
    if src is None:
        PLA_SRC[sk] = PLA_SRC.get(sk) or None
        return None
    fade = _pla_fade(beyond, layer)
    flip = bool(seed % 2)                                 # variety: mirrored every other plant
    if src == "hires":
        fill = c0["bark"] if bare else c0["fill"]
        if fade > 0:
            fill = _sec_mix(fill, SEC["paper"], fade)
        sh = hr_side(ref, x, g, k, h, w_m=None, fill=fill, edge=None, lw=0.0, facing=-1 if flip else 1)
        if sh:
            PLA_SRC[sk], PLA_IMG_FILE[sk] = src, "assets_hires.json:" + ref
        return sh
    if src == "cutout":
        import os as _o
        e = ref[int(seed) % len(ref)]
        path = _o.path.join(sil_cut_dir(), e["file"])
    else:
        path = ref
    px = sil_png_size(path)
    if not px or not px[1]:
        return None
    keep = 0.45 if c0.get("bloom") else PLA_IMG_TONE_KEEP
    tp = _pla_toned(path, c0, fade, keep)
    PLA_SRC[sk], PLA_IMG_FILE[sk] = src, _o_base(path)
    if view == "top":
        W = w * k
        H = W * px[1] / float(px[0])
        return [("image", x - W / 2.0, g - H / 2.0, W, H, tp, None, flip, None)]
    H = h * k
    W = H * px[0] / float(px[1])
    return [("image", x - W / 2.0, g, W, H, tp, None, flip, None)]


def _o_base(p):
    import os as _o
    return _o.path.basename(p)


def _pla_placeholder(key, state, view, x, g, h, w, k):
    """a labelled dashed box where no image exists (pla_missing("placeholder"); the D4 sample sheet)"""
    W = max(w * k, 4.0)
    H = (h * k) if view == "side" else W
    y0 = g if view == "side" else g - H / 2.0
    ring = [(x - W / 2.0, y0), (x + W / 2.0, y0), (x + W / 2.0, y0 + H), (x - W / 2.0, y0 + H), (x - W / 2.0, y0)]
    sz = 1.6
    return [("line", ring, "8E8F8A", 0.2, [1.0, 0.8]),
            ("text", u"no image", x, y0 + H / 2.0 + 0.2, sz, "8B2D2D", True, "C"),
            ("text", u"%s %s" % (key, state or "general"), x, y0 + H / 2.0 - 1.8, sz, "8B2D2D", False, "C")]


def _pla_missing_draw(key, state, view, x, g, h, w, k):
    """None (draw the round 4 vector) or the placeholder; counts the species x state as without image"""
    sk = (key, state or "general", view)
    if PLA_IMG["missing"] == "placeholder":
        PLA_SRC[sk] = "placeholder"
        return _pla_placeholder(key, state, view, x, g, h, w, k)
    PLA_SRC[sk] = "vector_fallback"
    return None



# round 5 (S4, BRIEF G-R5-6 row A1): every greenery colour of the other scripts' local palettes comes from here (S6-S9
# replace their own SEC/BM_COL/ICO_PAL/COL/... greenery values by pla_green(role)); pending research like all.
def pla_green(role):
    """a greenery colour by role: tree, tree_wet, tree_dry, shrub, flower, grass, meadow, crop, field, row,
    wetland, reed, trunk (hex, from the species colours of this module)"""
    f = lambda k_: PLA_SPECIES[k_]["colours"]["fill"]
    t = dict(tree=f("plane"), tree_wet=f("willow"), tree_dry=f("olive"), shrub=f("chaste"), flower=PLA_LAV,
             grass=PLA_CROP_LEAF, meadow=_sec_mix(PLA_CROP_LEAF, SEC["paper"], 0.45), crop=PLA_CROP_LEAF,
             field=PLA_FIELD, row=PLA_ROW, wetland=PLA_WET, reed=PLA_REED_HEAD, trunk=PLA_TRUNK)
    if role not in t:
        raise KeyError("pla_green: role %r; known: %s" % (role, ", ".join(sorted(t))))
    return t[role]


def pla_section(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0, hires=True, style="b", layer=0,
                detail=True, month=None, season=None):
    """A species in section at true size: ground at (x, gy) page mm (gy may be a function of x). h_m outside the
    sourced range is moved into it (pla_height_ok). layer: D9 depth layer (0 true size; 1, 2 smaller and paler).
    Round 4 (S3, D4, G-R4-6): ONE vector drawing per species everywhere (print quality: two-tone leaf masses with
    gaps, trunk and limbs); `hires` and `style` are accepted and no longer change the drawing (no cutouts, no
    high-res silhouettes). season (None = general; month= alias) = the season's state and colours (pla_colours), a
    deciduous species out of leaf drawn bare. detail: leaf texture and flower marks (_pla_detail). Never alpha."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    if h_m is not None:
        h = pla_height_ok(key, h)
    g = gy(x) if callable(gy) else gy
    s_ = _pla_s(season, month)
    _pla_status()
    _pla_count(key, s_)
    c = pla_colours(key, s_, beyond=beyond, layer=layer)
    sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
    k = k * sc
    img = _pla_img_draw(key, s_, "side", x, g, h, w, k, pla_colours(key, s_), seed, beyond, layer, c["bare"])
    if img is None:                                     # round 5: no image -> placeholder or the round 4 drawing
        img = _pla_missing_draw(key, s_, "side", x, g, h, w, k)
    if img is not None:
        return img
    if c["bare"]:
        return _pla_bare_draw(key, sp, x, g, h, w, k, c, seed)
    sh = _pla_sec(sp["form"], x, g, h, w, k, c, seed)
    if detail:
        sh += _pla_detail(key, sp["form"], x, g, h, w, k, c, seed)
    return sh


def pla_plan(key, cx, cy, k, crown_m=None, beyond=False, seed=0, distinct=True, style="b", month=None, season=None):
    """The same species from above: crown crown_m wide (m) centred on (cx, cy) page mm, built from the same masses
    and colours as its section; distinct: the species' own mark on top (no two species share a plan symbol, M6).
    season (month= alias) = the season's colours, deciduous out of leaf = bare branches. Always opaque."""
    sp = _pla_get(key)
    w = crown_m or sp["crown_m"]
    if w is None:
        raise ValueError("plants: %s has no sourced crown: pass crown_m" % key)
    s_ = _pla_s(season, month)
    _pla_status()
    _pla_count(key, s_)
    c = pla_colours(key, s_, beyond=beyond)
    img = _pla_img_draw(key, s_, "top", cx, cy, sp["h_m"] or w, w, k, pla_colours(key, s_), seed, beyond, 0, c["bare"])
    if img is None:                                     # round 5: no top-view image -> placeholder or round 4 drawing
        img = _pla_missing_draw(key, s_, "top", cx, cy, w, w, k)
    if img is not None:
        return img
    if c["bare"]:
        return _pla_bare_draw(key, sp, cx, cy, sp["h_m"] or w, w, k, c, seed, plan=True)
    sh = _pla_plan(sp["form"], cx, cy, w, k, c, seed)
    return sh + (_pla_plan_mark(key, cx, cy, w / 2.0 * k, c, seed) if distinct else [])


def pla_axo(key, x, y, k, h_m=None, crown_m=None, beyond=False, seed=0, layer=0, season=None, month=None,
            detail=False):
    """A species standing in an axo (p12, D1 'one drawing everywhere'): the section drawing of the module set upright
    at the projected base point (x, y) page mm, k = page mm per m of height at that point (a billboard, as an axo
    tree is drawn). Same willow v2 / species drawing as every section. Returns shapes (y up)."""
    return pla_section(key, x, y, k, h_m=h_m, crown_m=crown_m, beyond=beyond, seed=seed, layer=layer,
                       detail=detail, season=season, month=month)


# round 4 (S3, D4, D6): crop states by season from the sourced crop calendars (TAGEM region 28, PLA_CROP_SRC):
# cotton sown mid-Apr, to 21 Oct; maize sown Apr III / 1 May, to 2 Sep (TAGEM to Eki I); tomato (processing) planted
# Apr II / 15 May, to 27 Aug; olive orchard evergreen, harvest 6-14 Nov. Reading taken (drawing states, not data):
# spring = young plants; summer = grown (tomato with fruit, harvest to Aug); autumn = cotton ripe with open bolls
# (harvest to 21 Oct), maize and tomato harvested (stubble); winter = bare field; general = the crop in its character.
PLA_CROP_SRC = ("library/research/crops_2026-10-24/bergama_crops_irrigation_v1.md:388-400, 426-441 (TAGEM region 28);"
                " olive harvest :258 (Kaya 2017)")
PLA_CROP_STATE = dict(
    cotton=dict(general="ripe", winter="bare", spring="seedling", summer="growing", autumn="ripe"),
    maize=dict(general="growing", winter="bare", spring="seedling", summer="growing", autumn="harvested"),
    tomato=dict(general="fruit", winter="bare", spring="seedling", summer="fruit", autumn="harvested"),
    olive=dict(general="tree", winter="tree", spring="tree", summer="tree", autumn="tree"))


def pla_crop_state(crop, season=None, month=None):
    """the drawn state of a crop in a season: tree / bare / seedling / growing / ripe / fruit / harvested"""
    return PLA_CROP_STATE[crop][_pla_s(season, month) or "general"]


def _pla_crop_cols(beyond=False):
    """the crop leaf colours (one set for cotton, maize, tomato; pending research like all plant colours)"""
    c = _pla_c(PLA_CROP_LEAF)
    c["shade"] = _sec_mix(c["fill"], c["edge"], 0.25)
    if beyond:
        c = dict((k_, _sec_mix(v, SEC["paper"], 0.55) if v else v) for k_, v in c.items())
    return c


def _pla_crop_size(crop, h_m, crown_m):
    if crop == "olive":                         # orchard trees kept to their in-row spacing (rule); h by the olive ratio
        w = crown_m or PLA_CROPS["olive"]["plant_m"]
        return pla_height_ok("olive", h_m or w / PLA_FORM_RATIO["gnarled"]), w   # G6: never below the sourced 8 m
    if h_m is None or crown_m is None:
        raise ValueError("plants: %s plant size is not sourced: pass h_m and crown_m" % crop)
    return h_m, crown_m


def _pla_crop_sec(crop, x, gy, h, w, k, i, beyond, state="growing", season=None):
    """One crop plant in section, in its season's state (bare: nothing; harvested: stubble; seedling: young)."""
    if crop == "olive":
        c = pla_colours("olive", season, beyond=beyond)
        img = _pla_img_draw("olive", season, "side", x, gy, h, w, k, pla_colours("olive", season), i, beyond, 0, False)
        if img is None:
            img = _pla_missing_draw("olive", season, "side", x, gy, h, w, k)
        return img if img is not None else _pla_sec("gnarled", x, gy, h, w, k, c, i)
    c = _pla_crop_cols(beyond)
    if state == "bare":
        return []
    if state != "harvested":                     # round 5: crop image (asset png / hires), else placeholder / vector
        hh, ww = (0.30 * h, 0.40 * w) if state == "seedling" else (h, w)
        c0 = _pla_crop_cols(False)
        img = _pla_img_draw(crop, season, "side", x, gy, hh, ww, k, c0, i, beyond, 0, False)
        if img is None:
            img = _pla_missing_draw(crop, season, "side", x, gy, hh, ww, k)
        if img is not None:
            return img
    if state == "harvested":                    # stubble: short cut stems (rule 12 % of the height)
        return [("line", [(x + d * w * k * 0.3, gy), (x + d * w * k * 0.32, gy + 0.12 * h * k)], PLA_ROW, 0.1)
                for d in (-0.5, 0.0, 0.5)]
    if state == "seedling":                     # young plant (drawing rule: 30 % height, 40 % width)
        h, w = 0.30 * h, 0.40 * w
    H, R = h * k, w / 2.0 * k
    if crop == "maize":                         # stalk, arching leaves in two tones, tassel when grown
        sh = [("line", [(x, gy), (x, gy + H)], c["shade"], 0.2)]
        for j in range(1, 7):
            py, s_ = gy + H * (0.15 + 0.11 * j), (1 if j % 2 else -1)
            sh.append(("line", [(x, py), (x + s_ * R * 0.6, py + 0.08 * H), (x + s_ * R, py - 0.02 * H)],
                       c["fill"] if j % 2 else c["shade"], 0.14))
        if state != "seedling":
            sh.append(("line", [(x, gy + 0.92 * H), (x, gy + H)], PLA_REED_HEAD, 0.35))
        return sh
    if crop == "cotton":                        # small branched bush (two masses), open bolls when ripe
        sh = [("line", [(x, gy), (x, gy + 0.5 * H)], c["stem"], 0.12)]
        sh += _pla_mass(x - 0.35 * R, gy + 0.55 * H, 0.6 * R, 0.4 * H, 0.3 * H, c, i, 0.15)
        sh += _pla_mass(x + 0.35 * R, gy + 0.6 * H, 0.6 * R, 0.38 * H, 0.3 * H, c, i + 5, 0.15)
        if state == "ripe":
            for d, e_ in ((-0.5, 0.6), (0.1, 0.85), (0.55, 0.55)):
                sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.1 * R + 0.1, 0.1 * R + 0.1, 8), PLA_BOLL,
                           c["edge"], 0.05))
        return sh
    if crop == "tomato":                        # low sprawling plant (two masses), fruit in summer
        sh = _pla_mass(x - 0.3 * R, gy + 0.3 * H, 0.7 * R, 0.6 * H, 0.3 * H, c, i, 0.15)
        sh += _pla_mass(x + 0.35 * R, gy + 0.28 * H, 0.65 * R, 0.55 * H, 0.28 * H, c, i + 5, 0.15)
        if state == "fruit":
            for d, e_ in ((-0.45, 0.35), (0.2, 0.5), (0.6, 0.3)):
                sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.08 * R + 0.1, 0.08 * R + 0.1, 8), PLA_FRUIT,
                           None, 0.0))
        return sh
    raise ValueError("plants: unknown crop %r" % crop)


def pla_crop_rows(crop, x0, x1, gy, k, spacing=None, h_m=None, crown_m=None, beyond=False, season=None, month=None):
    """Crop plants along a cut from x0 to x1 (page mm), spacing m apart (the row spacing for a cut across the rows;
    sourced default only for olive), centred in the stretch; gy a number or a function of x. season (month= alias):
    the crop's state that season (pla_crop_state; winter = bare ground: no plants)."""
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    sp = spacing or PLA_CROPS[crop]["row_m"]
    if sp is None:
        raise ValueError("plants: %s row spacing is not sourced: pass spacing (m)" % crop)
    s_ = _pla_s(season, month)
    state = pla_crop_state(crop, s_)
    _pla_count("crop_" + crop, s_)
    h, w = _pla_crop_size(crop, h_m, crown_m)
    n = int((x1 - x0) / (sp * k) + 1e-9)
    off = ((x1 - x0) - n * sp * k) / 2.0
    sh = []
    for i in range(n + 1):
        x = x0 + off + i * sp * k
        sh += _pla_crop_sec(crop, x, gy(x) if callable(gy) else gy, h, w, k, i, beyond, state, s_)
    return sh


def _pla_ring(rr):
    """A ring from a ring or an (x0, y0, x1, y1) rectangle (page mm)."""
    if len(rr) == 4 and not isinstance(rr[0], (tuple, list)):
        x0, y0, x1, y1 = rr
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return list(rr)


def pla_crop_plan(crop, ring_or_rect, k, row_spacing=None, plant_spacing=None, ang_deg=0.0, crown_m=None,
                  field=True, season=None, month=None):
    """A field or orchard block in plan: rows at row_spacing (m) at ang_deg; with plant_spacing, single plants along
    each row (true crown with crown_m or for olive, else a fixed 0.25 mm dot). Sourced defaults only for olive.
    season (month= alias): bare / harvested fields show their furrows only, young crops small dots."""
    import math as _m
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    ring = _pla_ring(ring_or_rect)
    rs = row_spacing or PLA_CROPS[crop]["row_m"]
    ps = plant_spacing or PLA_CROPS[crop]["plant_m"]
    if rs is None:
        raise ValueError("plants: %s row spacing is not sourced: pass row_spacing (m)" % crop)
    s_ = _pla_s(season, month)
    state = pla_crop_state(crop, s_)
    _pla_count("crop_" + crop, s_)
    cc = _pla_crop_cols()
    sh = [("poly", ring, PLA_FIELD, None, 0.1)] if field else []
    w = crown_m or (PLA_CROPS["olive"]["plant_m"] if crop == "olive" else None)   # olive: crown = in-row spacing
    oc = pla_colours("olive", s_) if crop == "olive" else None
    for i, (p, q) in enumerate(sec_hatch(ring, rs * k, ang_deg)):
        if ps is None or state in ("bare", "harvested"):
            sh.append(("line", [p, q], PLA_ROW, 0.08 if state in ("bare", "harvested") else 0.15))
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
                sh += _pla_plan("gnarled", px, py, w, k, oc, i * 31 + j)
            elif w and state != "seedling":
                r = w / 2.0 * k
                sh += _pla_mass(px, py, r, r, r, cc, i * 31 + j, 0.12, edge=False)
            else:
                sh.append(("poly", sec_ellipse(px, py, 0.125, 0.125, 8), cc["fill"], None, 0.0))
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


def pla_reed_basin(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, step_m=None,
                   season=None, month=None):
    """Common reed in a lined, root-contained, off-line basin (D2 a) in section: inside x0-x1, floor bed_y, rim rim_y
    (page mm). kerb_t_m 0.15 m and floor slab = drawing rule; stems step_m apart in two tones; plumes only in the
    season's state (Jul-Nov S2, cut before Nov S11; general: with plumes)."""
    sp = PLA_SPECIES["reed"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h = h_m or sp["h_m"]
    st = (step_m or 1.0 / 3.0) * k              # 9 seedlings/m² (Korkusuz et al. 2004, S20) = 1/3 m apart
    s_ = _pla_s(season, month)
    _pla_count("reed", s_)
    c = pla_colours("reed", s_)
    i, x = 0, x0 + st / 2.0
    while x < x1:
        hh = h * k * (0.8 + 0.2 * _pla_rnd(i, 5))
        lean = 0.04 * hh * (1 if i % 2 else -1)
        sh.append(("line", [(x, g), (x + lean, g + hh)], c["fill"] if i % 3 else c["shade"], 0.12))
        if i % 3 == 0 and c["accent"]:          # plume
            ry = 0.2 * k + 0.2
            sh.append(("poly", sec_ellipse(x + lean, g + hh - ry, 0.06 * k + 0.1, ry, 10), c["accent"], None, 0.0))
        x += st
        i += 1
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_mint_cell(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, crown_m=None,
                  season=None, month=None):
    """Water mint only in a lined basin cell (D6) in section, same build as pla_reed_basin; mounds side by side in
    the season's colours."""
    sp = PLA_SPECIES["mint"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h, w = h_m or sp["h_m"], crown_m or sp["crown_m"]
    s_ = _pla_s(season, month)
    _pla_count("mint", s_)
    c = pla_colours("mint", s_)
    n = max(1, int((x1 - x0) / (w * k)))
    for i in range(n):
        sh += _pla_sec("mound", x0 + (i + 0.5) * (x1 - x0) / n, g, h, min(w, (x1 - x0) / n / k), k, c, i)
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_cell_plan(kind, ring_or_rect, k, kerb_t_m=0.15, season=None, month=None):
    """A lined cell in plan, kind 'reed' or 'mint': wet ground, the kerb as a band kerb_t_m wide, the plants in the
    season's colours."""
    if kind not in ("reed", "mint"):
        raise ValueError("pla_cell_plan: kind is 'reed' or 'mint'")
    ring = _pla_ring(ring_or_rect)
    sp = PLA_SPECIES[kind]
    s_ = _pla_s(season, month)
    _pla_count(kind, s_)
    c = pla_colours(kind, s_)
    sh = [("poly", ring, PLA_WET, None, 0.1)]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    if kind == "reed":                          # stems on the 1/3 m grid, never denser than 0.9 mm on the page
        d = max(0.9, k / 3.0)
        for i in range(int((max(xs) - min(xs)) / d) + 1):
            for j in range(int((max(ys) - min(ys)) / d) + 1):
                px = min(xs) + (i + 0.5 * (j % 2) + 0.25) * d
                py = min(ys) + (j + 0.5) * d
                if _sct_inside(ring, (px, py)):
                    sh.append(("line", [(px - 0.2 * d, py - 0.25 * d), (px + 0.2 * d, py + 0.25 * d)],
                               c["fill"] if (i + j) % 3 else c["shade"], 0.1))
    else:
        w = sp["crown_m"] * k
        for i in range(int((max(xs) - min(xs)) / w) + 1):
            for j in range(int((max(ys) - min(ys)) / w) + 1):
                px, py = min(xs) + (i + 0.5) * w, min(ys) + (j + 0.5) * w
                if _sct_inside(ring, (px, py)):
                    sh += _pla_plan("mound", px, py, sp["crown_m"] * 0.9, k, c, i * 7 + j)
    sh.append(("poly", ring, None, SCT["line"], max(0.15, kerb_t_m * k)))
    return sh


# ---- purpose tags (G9, M6; H-B 30 Oct 2026): what each plant group does. From the species roles of the water board
# (SPECIES.py role: shade, hold the bank, clean, scent, flower, harvest) mapped onto M6's six words, plus plain
# riparian ecology (marked "?" in PLA_PURPOSE_UNSURE: not from a project source; check before printing as a claim).
PLA_TAGS = ("wind", "noise", "shade", "corridor", "cleaning", "perception")
PLA_PURPOSE = {
    "plane": ("shade", "corridor"),
    "ash": ("shade", "corridor"),
    "willow": ("shade", "cleaning", "corridor"),
    "olive": ("shade", "perception"),
    "stone_pine": ("shade", "wind", "perception"),
    "tamarisk": ("shade", "wind", "corridor"),
    "chaste": ("perception", "corridor"),
    "rosemary": ("perception",),
    "lavender": ("perception",),
    "loosestrife": ("cleaning", "perception", "corridor"),
    "soft_rush": ("cleaning", "corridor"),
    "rush": ("cleaning", "corridor"),
    "reed": ("cleaning", "noise", "corridor"),
    "mint": ("cleaning", "perception"),
}
PLA_PURPOSE_UNSURE = {   # tags assigned from general ecology, not from a project source
    "plane": ("corridor",), "ash": ("corridor",), "willow": ("corridor",), "olive": ("perception",),
    "stone_pine": ("shade", "wind", "perception"), "tamarisk": ("wind", "corridor"), "chaste": ("corridor",),
    "loosestrife": ("corridor",), "soft_rush": ("corridor",), "rush": ("cleaning", "corridor"),
    "reed": ("noise", "corridor"),
}


def pla_purpose(key, sure_only=False):
    """the purpose tags of a species (PLA_TAGS words); sure_only drops the ones from general ecology"""
    t = PLA_PURPOSE.get(key, ())
    return tuple(x for x in t if not (sure_only and x in PLA_PURPOSE_UNSURE.get(key, ())))


# ---- ecological bands (G9): t = 0 at the water's edge (wet, low) to 1 on the dry upper ground (high). Each species
# grows around its niche centre (t, half width, weight): drawing rules from the species' habitat words in
# species.json (emergent / bank / dry slope), not measured distances. Reed and water mint: lined cells only (D2, D6).
PLA_NICHE = {
    "soft_rush": (0.04, 0.12, 1.0), "loosestrife": (0.10, 0.14, 0.9), "rush": (0.14, 0.12, 0.6),
    "willow": (0.24, 0.17, 0.8), "tamarisk": (0.36, 0.22, 0.7), "ash": (0.46, 0.20, 0.6), "plane": (0.52, 0.20, 0.5),
    "chaste": (0.55, 0.24, 0.8), "olive": (0.80, 0.20, 0.6), "rosemary": (0.86, 0.17, 0.8), "lavender": (0.90, 0.15, 0.8),
    "stone_pine": (0.92, 0.12, 0.3),
}


def _pla_canopy(key):
    return PLA_SPECIES[key]["layer"] == "tree"


def _pla_pick(t, rnd, keys, mix, canopy):
    """a species for band position t (weighted by niche), or None for an open gap"""
    import math as _m
    ws = []
    for k_ in keys:
        if _pla_canopy(k_) != canopy:
            continue
        tc, hw, w0 = PLA_NICHE[k_]
        w = (mix.get(k_, w0) if isinstance(mix, dict) else w0) * _m.exp(-((t - tc) / hw) ** 2)
        if w > 0.02:
            ws.append((k_, w))
    tot = sum(w for _k, w in ws)
    if tot < 0.12:                                 # nothing at home here: leave the ground open
        return None
    r = rnd() * tot
    for k_, w in ws:
        r -= w
        if r <= 0:
            return k_
    return ws[-1][0]


def _pla_size_var(key, rnd):
    """(h, crown) of one plant: the drawing size x 0.88-1.08, kept inside the sourced height range"""
    sp = PLA_SPECIES[key]
    f = 0.88 + 0.20 * rnd()
    return pla_height_ok(key, sp["h_m"] * f), sp["crown_m"] * f


def _pla_keys(mix):
    # round 4 (D1, PLAN §4.9): mix=None no longer draws the willow; it is planted only where a mix names it
    keys = list(mix) if mix else [k_ for k_ in PLA_NICHE if k_ != "willow"]
    bad = [k_ for k_ in keys if k_ not in PLA_NICHE]
    if bad:
        raise ValueError("plants scatter: %s not free-planted (cells only, removed or unknown)" % ", ".join(bad))
    return keys


def pla_scatter_section(x0, x1, gy, k, t0=0.0, t1=1.0, mix=None, seed=0, layer=0, style="b", density=1.0,
                        hires=True, avoid=None, detail=True, month=None, season=None, water=None):
    """a mixed, naturalistic planting along a cut from x0 to x1 (page mm), ground gy (number or function of x): the
    band position runs from t0 at x0 to t1 at x1 (0 = water's edge, 1 = dry upper ground; or pass t0 as a function
    of x). Canopy trees and the low layer are spaced independently (crowns overlap, shrubs stand under tree edges),
    each gap random and never equal to the one before (no rows, no repeated clusters). mix: species keys (list) or
    {key: weight}. avoid: [(xa, xb)] page mm where nothing is planted (paths, water, steps). water: page y (or a
    function of x) of the water: where the ground lies under it only emergent species grow. season (month= alias):
    pla_section. Returns (shapes,
    placed [(key, x, h_m, crown_m)]), drawn tall first so the low layer reads in front."""
    keys = _pla_keys(mix)
    rnd = _pla_rng(seed * 7 + 3)
    sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
    K = k * sc

    def tt(x):
        if callable(t0):
            return t0(x)
        return t0 + (t1 - t0) * (x - x0) / float(max(1e-9, x1 - x0))

    def blocked(x, key):
        if any(a <= x <= b for a, b in (avoid or ())):
            return True
        if water is None or PLA_SPECIES[key]["layer"] == "emergent":
            return False
        g_ = gy(x) if callable(gy) else gy
        return g_ < (water(x) if callable(water) else water)
    placed = []
    for canopy in (True, False):
        x, last_gap = x0 + rnd() * 1.5 * K, None
        while x < x1:
            key = _pla_pick(tt(x), rnd, keys, mix, canopy)
            if key is None or blocked(x, key):
                x += (0.8 + rnd()) * K
                continue
            h, w = _pla_size_var(key, rnd)
            placed.append((key, x, h, w))
            f = 0.85 if canopy else 0.75
            gap = f * w * (0.7 + 1.1 * rnd()) / max(0.2, density) * K
            if last_gap is not None and abs(gap - last_gap) < 0.15 * gap:     # never an even rhythm
                gap *= 1.35 if rnd() > 0.5 else 0.72
            last_gap = gap
            x += max(0.3 * K, gap)
    placed.sort(key=lambda p_: -p_[2])
    sh = []
    for i, (key, x, h, w) in enumerate(placed):
        sh += pla_section(key, x, gy, k, h_m=h, crown_m=w, seed=seed + i, hires=hires, style=style, layer=layer,
                          detail=detail, month=month, season=season)
    return sh, placed


# ---- round 4 (S3, D7, G-R4-5.2): the low layer of shrubs and flowers. Only the sourced species already in the
# booklet (D7): chaste tree, rosemary, French lavender, purple loosestrife, soft rush, placed by wetness band
# (PLA_NICHE: loosestrife and soft rush at the water, chaste tree on the moist ground, rosemary and lavender on the
# dry tops). Every section gets one (BRIEF G-R4-5.2), and every undefined planted area in plan (pla_low_plan).
PLA_LOW = ("chaste", "rosemary", "lavender", "loosestrife", "soft_rush")


def pla_low_section(x0, x1, gy, k, t0=0.0, t1=1.0, seed=0, layer=0, density=1.2, avoid=None, water=None,
                    season=None, month=None, mix=None, detail=True):
    """the shrub and flower layer along a cut x0..x1 (page mm), band t0 -> t1 (0 = water's edge, 1 = dry top; or t0
    a function of x), mixed by wetness, never in rows (pla_scatter_section with the PLA_LOW species or `mix`, a
    subset); water / avoid as there. Returns (shapes, placed [(key, x, h_m, crown_m)])."""
    return pla_scatter_section(x0, x1, gy, k, t0, t1, mix=mix or PLA_LOW, seed=seed, layer=layer, density=density,
                               avoid=avoid, detail=detail, month=month, season=season, water=water)


def pla_low_plan(ring, k, gradient, seed=0, density=1.2, avoid=None, season=None, month=None, mix=None, max_n=3000):
    """the shrub and flower layer in an undefined planted area in plan (ring page mm; gradient as pla_scatter_plan),
    the PLA_LOW species (or `mix`, a subset) by wetness. Returns (shapes, placed [(key, x, y, crown_m)])."""
    return pla_scatter_plan(ring, k, gradient, mix=mix or PLA_LOW, seed=seed, density=density, avoid=avoid,
                            max_n=max_n, month=month, season=season)


# ---- G9 mixed groups in section (R2-A 31 Oct 2026) -------------------------------------------------------------------
# Drawing rules (not data): a group is 5-16 m wide with 2-12 m open gaps between groups (both / density), canopy
# trees step 35-75 % of a crown apart (crowns overlap), each plant's height = its drawing size x 0.70-1.10 kept
# inside the sourced range (pla_height_ok); the low layer stands under and around the tree edges.
PLA_GROUP = dict(group_m=(5.0, 16.0), gap_m=(2.0, 12.0), step=(0.35, 0.75), size=(0.70, 1.10))


def _pla_group_size(key, rnd):
    sp = PLA_SPECIES[key]
    lo, hi = PLA_GROUP["size"]
    f = lo + (hi - lo) * rnd()
    return pla_height_ok(key, sp["h_m"] * f), sp["crown_m"] * f


def _pla_other(t, rnd, keys, mix, canopy, not_key):
    """a species other than not_key for band position t (None if nothing else grows here)"""
    for _i in range(8):
        k_ = _pla_pick(t, rnd, keys, mix, canopy)
        if k_ is not None and k_ != not_key:
            return k_
    return None


def pla_group_section(x0, x1, gy, k, t0=0.0, t1=1.0, mix=None, seed=0, layers=(2, 1, 0), style="a", density=1.0,
                      avoid=None, hires=True, detail=True, ground=None, water=None, month=None, season=None):
    """G9 planting in section: mixed groups, never rows. Along x0..x1 (page mm), band t0 -> t1 (0 = water's edge,
    1 = dry upper ground; or t0 = a function of x), each depth layer of `layers` (D9, back first: 2, 1, 0) gets
    groups at irregular places; in a group the canopy trees overlap their crowns and the low layer (shrubs,
    emergent, ground) stands under and around them; species interpenetrate by band (wet to dry, low to high: the
    niche weights of PLA_NICHE) and a group always holds two or more species and three or more plants (never one
    species standing alone, never an identical cluster: sizes and gaps vary). Each plant: a varied height inside its
    sourced range, a cutout variant picked by its seed (style a), mirrored on odd seeds, seated on the lowest ground
    under its base (G14 sf_seat_x). ground = {layer: gy} gives a depth layer its own ground (else gy); water = page
    y or function of x: where the ground lies under the water only emergent species grow; avoid = [(xa, xb)] page
    mm kept free (paths, steps, lanes). Returns (shapes back to front, placed [(key, x, h_m, crown_m, layer)],
    groups [(layer, xa, xb, [keys], purpose tags)]): use groups to say what each group does (G9) and placed for
    sf_assert_g6."""
    keys = _pla_keys(mix)
    rnd = _pla_rng(seed * 11 + 5)
    seat = globals().get("sf_seat_x")
    gfn = globals().get("_sf_fn")

    def tt(x):
        if callable(t0):
            return t0(x)
        return t0 + (t1 - t0) * (x - x0) / float(max(1e-9, x1 - x0))

    def blocked(x):
        return any(a <= x <= b for a, b in (avoid or ()))
    sh, placed, groups, n = [], [], [], 0
    for layer in layers:
        g_ = (ground or {}).get(layer, gy)
        g_ = gfn(g_) if gfn else g_
        sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
        K = k * sc

        def wet(x):
            if water is None:
                return False
            w_ = water(x) if callable(water) else water
            return (g_(x) if callable(g_) else g_) < w_

        def ok(key, x):
            return not blocked(x) and (not wet(x) or PLA_SPECIES[key]["layer"] == "emergent")
        x = x0 + rnd() * PLA_GROUP["gap_m"][1] * 0.5 * K
        while x < x1:
            gw = (PLA_GROUP["group_m"][0] + (PLA_GROUP["group_m"][1] - PLA_GROUP["group_m"][0]) * rnd()) * K
            xa, xb = x, min(x1, x + gw)
            mem = []
            xx = xa + 0.1 * rnd() * gw                     # canopy: overlapping crowns
            while xx < xb:
                key = _pla_pick(tt(xx), rnd, keys, mix, True)
                if key is not None and mem and all(m[0] == key for m in mem) and rnd() < 0.6:
                    key = _pla_other(tt(xx), rnd, keys, mix, True, key) or key
                if key is None or not ok(key, xx):
                    xx += (0.6 + rnd()) * K
                    continue
                h, w = _pla_group_size(key, rnd)
                mem.append((key, xx, h, w, True))
                xx += (PLA_GROUP["step"][0] + (PLA_GROUP["step"][1] - PLA_GROUP["step"][0]) * rnd()) * w * K
            nl = 2 + int(rnd() * 4.999)                     # low layer: 2-6, under and around the crowns
            for _i in range(nl):
                xl = xa - 0.1 * gw + 1.2 * gw * rnd()
                if xl < x0 or xl > x1:
                    continue
                key = _pla_pick(tt(xl), rnd, keys, mix, False)
                if key is None or not ok(key, xl):
                    continue
                h, w = _pla_group_size(key, rnd)
                mem.append((key, xl, h, w, False))
            sp = set(m[0] for m in mem)
            if len(sp) == 1 and mem:                       # one species alone: add another that grows here
                for _i in range(3):
                    xl = xa + gw * rnd()
                    for canopy in (False, True):
                        key = _pla_other(tt(xl), rnd, keys, mix, canopy, mem[0][0])
                        if key is not None and ok(key, xl) and xl <= x1:
                            h, w = _pla_group_size(key, rnd)
                            mem.append((key, xl, h, w, canopy))
                            break
                    if len(set(m[0] for m in mem)) > 1:
                        break
            if len(mem) >= 3 and len(set(m[0] for m in mem)) >= 2:
                mem.sort(key=lambda m: -m[2])              # tall first: the low layer reads in front
                ks = sorted(set(m[0] for m in mem))
                tags = sorted(set(t_ for k_ in ks for t_ in pla_purpose(k_, sure_only=True)))
                groups.append((layer, xa, xb, ks, tags))
                for key, xp, h, w, canopy in mem:
                    half = (0.12 if canopy else 0.35) * w * K
                    gyp = seat(g_, xp, half) if seat else (g_(xp) if callable(g_) else g_)
                    sh += pla_section(key, xp, gyp, k, h_m=h, crown_m=w, seed=seed * 1000 + n, hires=hires,
                                      style=style, layer=layer, detail=detail, month=month, season=season)
                    placed.append((key, xp, h, w, layer))
                    n += 1
            x = xb + (PLA_GROUP["gap_m"][0] + (PLA_GROUP["gap_m"][1] - PLA_GROUP["gap_m"][0]) * rnd()) / \
                max(0.2, density) * K
    if not groups:
        msg = u"Plants: no mixed group fits %s (a group needs two or more species growing in its band)" % (
            u", ".join(keys))
        if msg not in PLA_LOG:
            PLA_LOG.append(msg)
    return sh, placed, groups


def _pla_rng(seed):
    s = [int(seed * 2654435761 + 97) & 0x7fffffff]

    def r():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7fffffff
        return s[0] / float(0x7fffffff)
    return r


def _pla_seg_d(p, a, b):
    import math as _m
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return _m.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _pla_grad_fn(gradient, k):
    """t(x, y) from a function, or from {"wet": polyline page mm, "width_m": band width}: distance to the wet line
    over the band width, 0..1"""
    if callable(gradient):
        return gradient
    wet, wd = gradient["wet"], float(gradient["width_m"]) * k

    def f(x, y):
        d = min(_pla_seg_d((x, y), a, b) for a, b in zip(wet[:-1], wet[1:]))
        return max(0.0, min(1.0, d / wd))
    return f


def _pla_rowlike(c, pts, d_lim):
    """True when c continues a straight, evenly spaced line of two neighbours (a row in the making)"""
    import math as _m
    near = sorted((q for q in pts if _m.hypot(q[0] - c[0], q[1] - c[1]) < d_lim),
                  key=lambda q: (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2)[:8]     # the 8 nearest are enough
    for b in near:
        dbc = _m.hypot(c[0] - b[0], c[1] - b[1])
        for a in near:
            if a is b:
                continue
            dab = _m.hypot(b[0] - a[0], b[1] - a[1])
            if dab < 1e-9 or abs(dab - dbc) > 0.2 * dbc:
                continue
            u = ((b[0] - a[0]) / dab, (b[1] - a[1]) / dab)
            v = ((c[0] - b[0]) / dbc, (c[1] - b[1]) / dbc)
            if u[0] * v[0] + u[1] * v[1] > 0.985:        # within about 10 degrees of straight on
                return True
    return False


def pla_scatter_plan(ring, k, gradient, mix=None, seed=0, density=1.0, avoid=None, max_n=3000, month=None,
                     season=None):
    """a mixed planting in plan inside ring (page mm): Poisson-disc style dart throwing, canopy trees first then the
    low layer, each species picked by its niche at t = gradient(x, y) (a function, or {"wet": polyline, "width_m":
    m}); same-layer plants keep 0.8 x (r1 + r2) apart, shrubs may stand under tree edges (0.3 x), candidates that
    would extend a straight evenly spaced line are thrown away: no rows, grids, axes or repeated clusters. avoid:
    rings (page mm) left empty. month: seasonal colours / bare (pla_plan). Returns (shapes, placed [(key, x, y,
    crown_m)]); canopy crowns drawn opaque over the low layer (round 3 D7: no alpha anywhere)."""
    import math as _m
    keys = _pla_keys(mix)
    rnd = _pla_rng(seed * 11 + 5)
    tf = _pla_grad_fn(gradient, k)
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    bx0, by0, bw, bh = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    area = abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:] + ring[:1]))) / 2.0
    placed = {True: [], False: []}
    grids = {True: {}, False: {}}
    rmax = {c_: max([PLA_SPECIES[k_]["crown_m"] * 1.08 / 2.0 * k for k_ in keys if _pla_canopy(k_) == c_] or [0.5 * k])
            for c_ in (True, False)}

    def cell(c_, x, y):
        s_ = 2.0 * rmax[c_]
        return int(_m.floor(x / s_)), int(_m.floor(y / s_))

    def near(c_, x, y, dist):
        s_ = 2.0 * rmax[c_]
        n = int(_m.ceil(dist / s_))
        i0, j0 = cell(c_, x, y)
        out = []
        for i in range(i0 - n, i0 + n + 1):
            for j in range(j0 - n, j0 + n + 1):
                out += grids[c_].get((i, j), ())
        return out
    total = 0
    for canopy in (True, False):
        r_typ = (sum(PLA_SPECIES[k_]["crown_m"] for k_ in keys if _pla_canopy(k_) == canopy) /
                 max(1, sum(1 for k_ in keys if _pla_canopy(k_) == canopy))) / 2.0 * k
        if r_typ <= 0:
            continue
        tries = int(min(30000, 6.0 * density * area / (_m.pi * r_typ * r_typ) + 50))
        for _i in range(tries):
            if total >= max_n:
                break
            x, y = bx0 + rnd() * bw, by0 + rnd() * bh
            if not _sct_inside(ring, (x, y)) or any(_sct_inside(a, (x, y)) for a in (avoid or ())):
                continue
            key = _pla_pick(tf(x, y), rnd, keys, mix, canopy)
            if key is None:
                continue
            h, w = _pla_size_var(key, rnd)
            r = w / 2.0 * k
            ok = True
            for (qx, qy, qr, _qk) in near(canopy, x, y, 0.8 * (r + rmax[canopy])):
                if _m.hypot(qx - x, qy - y) < 0.8 * (r + qr) / max(0.3, density) ** 0.5:
                    ok = False
                    break
            if ok and not canopy:
                for (qx, qy, qr, _qk) in near(True, x, y, 0.3 * (r + rmax[True])):
                    if _m.hypot(qx - x, qy - y) < 0.3 * (r + qr):
                        ok = False
                        break
            if ok and canopy:
                for (qx, qy, qr, _qk) in near(False, x, y, 0.3 * (r + rmax[False])):
                    if _m.hypot(qx - x, qy - y) < 0.3 * (r + qr):
                        ok = False
                        break
            if ok and _pla_rowlike((x, y), [(q[0], q[1]) for q in near(canopy, x, y, 3.0 * (r + rmax[canopy]))],
                                   3.0 * (r + rmax[canopy])):
                ok = False
            if not ok:
                continue
            e = (x, y, r, key)
            placed[canopy].append(e)
            grids[canopy].setdefault(cell(canopy, x, y), []).append(e)
            total += 1
    sh, out = [], []
    for canopy in (False, True):
        for i, (x, y, r, key) in enumerate(placed[canopy]):
            sh += pla_plan(key, x, y, k, crown_m=2.0 * r / k, seed=seed + i * 3 + (7 if canopy else 0), month=month,
                           season=season)
            out.append((key, x, y, 2.0 * r / k))
    return sh, out


# ---- field / orchard tile (D7 a, D2 a): one texture + one representative symbol in the middle of the area ----------
def _pla_inner_point(ring):
    """a point well inside the ring: the grid point farthest from the edge (12 x 12 search)"""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    best, bd = None, -1.0
    for i in range(1, 12):
        for j in range(1, 12):
            p = (min(xs) + (max(xs) - min(xs)) * i / 12.0, min(ys) + (max(ys) - min(ys)) * j / 12.0)
            if not _sct_inside(ring, p):
                continue
            d = min(_pla_seg_d(p, a, b) for a, b in zip(ring, ring[1:] + ring[:1]))
            if d > bd:
                best, bd = p, d
    return best or (sum(xs) / len(xs), sum(ys) / len(ys))


def pla_field_tile(ring_or_rect, k, crop="olive", symbol_mm=None, seed=0, fill=None, texture=True, season=None,
                   month=None):
    """a farm or orchard area simplified (D7 a, r3 #31): the field fill, an even scatter of short furrow marks (one
    texture, no rows) and ONE symbol of the crop in the middle, drawn at print quality in the crop's season state
    (olive: the olive plan symbol; other crops: a two-tone crop tuft, bolls / fruit when ripe, stubble when
    harvested, bare furrows in winter). symbol_mm = the symbol's width on the page (default the true olive crown 5 m
    x k, at least 6 mm: a symbol, not to scale). Returns shapes."""
    import math as _m
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    ring = _pla_ring(ring_or_rect)
    s_ = _pla_s(season, month)
    state = pla_crop_state(crop, s_)
    _pla_count("crop_" + crop, s_)
    sh = [("poly", ring, fill or PLA_FIELD, None, 0.1)]
    if texture:
        rnd = _pla_rng(seed + 17)
        xs, ys = [p[0] for p in ring], [p[1] for p in ring]
        d = 1.6                                      # page mm between marks (texture, not a size)
        nx, ny = int((max(xs) - min(xs)) / d) + 1, int((max(ys) - min(ys)) / d) + 1
        for i in range(nx):
            for j in range(ny):
                px = min(xs) + (i + 0.15 + 0.7 * rnd()) * d
                py = min(ys) + (j + 0.15 + 0.7 * rnd()) * d
                if not _sct_inside(ring, (px, py)):
                    continue
                a = _m.radians(20.0 + 40.0 * rnd())
                L = 0.35 + 0.3 * rnd()
                sh.append(("line", [(px, py), (px + L * _m.cos(a), py + L * _m.sin(a))], PLA_ROW, 0.08))
    cx, cy = _pla_inner_point(ring)
    sm = symbol_mm or max(6.0, PLA_CROPS["olive"]["plant_m"] * k)
    if crop == "olive":
        oc = pla_colours("olive", s_)
        sh += _pla_plan("gnarled", cx, cy, sm / k, k, oc, seed)
        sh += _pla_plan_mark("olive", cx, cy, sm / 2.0, oc, seed)
        return sh
    r = sm / 2.0
    if state in ("bare", "harvested"):              # furrows (and stubble ticks when harvested)
        for j in (-1, 0, 1):
            sh.append(("line", [(cx - r, cy + 0.35 * j * r), (cx + r, cy + 0.35 * j * r)], PLA_ROW, 0.25))
            if state == "harvested":
                for i in range(-3, 4):
                    px = cx + 0.28 * i * r
                    sh.append(("line", [(px, cy + 0.35 * j * r), (px + 0.05 * r, cy + 0.35 * j * r + 0.14 * r)],
                               PLA_ROW, 0.12))
        return sh
    cc = _pla_crop_cols()
    if state == "seedling":
        r *= 0.5
    for i, (dx, dy, s_m) in enumerate(((-0.35, -0.2, 0.6), (0.32, -0.15, 0.58), (0.0, 0.25, 0.6))):
        sh += _pla_mass(cx + dx * r, cy + dy * r, s_m * r, s_m * r, s_m * r, cc, seed + i, 0.12)
    acc = {"ripe": PLA_BOLL, "fruit": PLA_FRUIT}.get(state)
    if crop == "maize" and state == "growing":
        acc = PLA_REED_HEAD                          # tassels
    if acc:
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + 0.08)
            sh.append(("poly", sec_ellipse(cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a), 0.14 * r, 0.14 * r, 8),
                       acc, cc["edge"] if acc == PLA_BOLL else None, 0.05 if acc == PLA_BOLL else 0.0))
    return sh


# ---- species detail (M6 style b: "detailed from the species' photo"): leaf texture and flower marks in the crown, and
# a mark per species in plan so that no two species share a symbol. Mark sizes are page-mm conventions eased with
# the crown size; colours only from the species' own set (flower colours: only where the species row has one).
def _pla_marks_in(cx, cy, rx, ry, n, rnd):
    """n points spread inside an ellipse (jittered sunflower spiral: even, never a grid)"""
    import math as _m
    out = []
    for i in range(n):
        rr = _m.sqrt((i + 0.5) / n)
        a = i * 2.39996 + 0.6 * rnd()
        out.append((cx + rx * rr * _m.cos(a), cy + ry * rr * _m.sin(a)))
    return out


def _pla_detail(key, form, x, gy, h, w, k, c, seed):
    """leaf texture / flower marks of one species in section, over its _pla_sec silhouette"""
    import math as _m
    rnd = _pla_rng(seed * 3 + 1)
    H, R = h * k, w / 2.0 * k
    if R < 0.8:                                     # too small on the page for a texture
        return []
    lo = dict(dome=0.3, oval=0.3, weeping=0.25, gnarled=0.3, umbrella=0.65, feathery=0.55).get(form, 0.0) * H
    cx, cy = x, gy + lo + (H - lo) * (0.55 if form != "mound" else 0.45)
    rx, ry = 0.62 * R, 0.30 * (H - lo) if form != "umbrella" else 0.24 * (H - lo)   # round 4: on the masses, not gaps
    m = max(0.25, min(1.2, 0.045 * R))              # mark length, page mm
    n = int(max(6, min(70, (_m.pi * rx * ry) / (m * m * 9.0))))
    e, lt, ac = c["edge"], c["lt"], c.get("accent")
    sh = []
    pts = _pla_marks_in(cx, cy, rx, ry, n, rnd)
    for i, (px, py) in enumerate(pts):
        if key == "plane":                          # palmate leaves: three short spokes
            for a in (90.0, 30.0, 150.0):
                r_ = _m.radians(a + 20.0 * rnd())
                sh.append(("line", [(px, py), (px + m * _m.cos(r_), py + m * _m.sin(r_))], e, 0.06))
        elif key == "ash":                          # pinnate leaves: a stalk with leaflet pairs
            a = _m.radians(70.0 + 40.0 * rnd())
            ux, uy = _m.cos(a), _m.sin(a)
            sh.append(("line", [(px, py), (px + 1.4 * m * ux, py + 1.4 * m * uy)], e, 0.05))
            for t in (0.45, 0.9):
                bx_, by_ = px + t * 1.4 * m * ux, py + t * 1.4 * m * uy
                sh.append(("line", [(bx_ - 0.35 * m * uy, by_ + 0.35 * m * ux), (bx_ + 0.35 * m * uy, by_ - 0.35 * m * ux)],
                           e, 0.05))
        elif key == "willow":                       # round 3: its streamers and strands are the texture (marks
            pass                                    # spread over the envelope would float in the gaps, G14)
        elif key == "olive":                        # small lance leaves, silver above, dark below
            a = _m.radians(rnd() * 180.0)
            col = lt if i % 3 else e
            sh.append(("line", [(px, py), (px + 0.9 * m * _m.cos(a), py + 0.9 * m * _m.sin(a))], col, 0.08))
        elif key == "stone_pine":                   # needle tufts on the flat crown
            if py > cy - 0.2 * ry:
                for a in (60.0, 90.0, 120.0):
                    r_ = _m.radians(a)
                    sh.append(("line", [(px, py), (px + 0.8 * m * _m.cos(r_), py + 0.8 * m * _m.sin(r_))], lt, 0.05))
        elif key == "tamarisk":                     # scale-leaf sprays: fine stipple
            sh.append(("poly", sec_ellipse(px, py, 0.12 * m + 0.05, 0.12 * m + 0.05, 6), e, None, 0.1))
        elif key == "rosemary":                     # needle leaves
            a = _m.radians(45.0 + 90.0 * (i % 2))
            sh.append(("line", [(px, py), (px + 0.7 * m * _m.cos(a), py + 0.7 * m * _m.sin(a))], e, 0.06))
        elif key in ("lavender", "chaste", "loosestrife") and ac:
            if i % 2 == 0:                          # flowers in the species' own accent
                sh.append(("poly", sec_ellipse(px, py, 0.18 * m + 0.06, 0.28 * m + 0.08, 8), ac, None, 0.1))
        elif key == "soft_rush":                    # brown flower tufts on the side of the stems, near the top
            if py > cy and i % 3 == 0:
                sh.append(("poly", sec_ellipse(px, py, 0.25 * m + 0.08, 0.2 * m + 0.06, 8), PLA_REED_HEAD, None, 0.1))
        elif key == "rush":                         # sharp stem tips
            if py > cy and i % 2 == 0:
                sh.append(("line", [(px, py), (px, py + 0.8 * m)], e, 0.05))
        elif key == "mint":                         # small rounded leaves
            sh.append(("poly", sec_ellipse(px, py, 0.22 * m + 0.05, 0.18 * m + 0.05, 8), lt, None, 0.1))
    return sh


def _pla_plan_mark(key, cx, cy, r, c, seed):
    """the species' own mark on its plan symbol (M6: every species distinct in plan)"""
    import math as _m
    rnd = _pla_rng(seed * 5 + 2)
    e, lt, ac = c["edge"], c["lt"], c.get("accent")
    m = max(0.2, 0.18 * r)
    sh = []
    if key == "plane":                              # palmate stars
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 5, rnd):
            for a in (90.0, 18.0, 162.0, 234.0, 306.0):
                ra = _m.radians(a)
                sh.append(("line", [(px, py), (px + 0.5 * m * _m.cos(ra), py + 0.5 * m * _m.sin(ra))], e, 0.06))
    elif key == "ash":                              # pinnate marks
        for (px, py) in _pla_marks_in(cx, cy, 0.55 * r, 0.55 * r, 4, rnd):
            sh.append(("line", [(px - 0.6 * m, py), (px + 0.6 * m, py)], e, 0.06))
            for t in (-0.3, 0.1, 0.5):
                sh.append(("line", [(px + t * m, py - 0.25 * m), (px + t * m, py + 0.25 * m)], e, 0.05))
    elif key == "olive":                            # silver leaf speckle
        for (px, py) in _pla_marks_in(cx, cy, 0.75 * r, 0.75 * r, 9, rnd):
            sh.append(("poly", sec_ellipse(px, py, 0.12 * m + 0.05, 0.12 * m + 0.05, 6), lt, None, 0.1))
    elif key == "stone_pine":                       # dark ring inside the rim tufts
        sh.append(("poly", sec_ellipse(cx, cy, 0.55 * r, 0.55 * r, 30), None, e, 0.08))
    elif key == "willow":                           # narrow lance leaves, pale side up
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 8, rnd):
            a = _m.radians(rnd() * 180.0)
            sh.append(("line", [(px, py), (px + 0.7 * m * _m.cos(a), py + 0.7 * m * _m.sin(a))], lt, 0.06))
    elif key == "tamarisk":                         # stipple
        for (px, py) in _pla_marks_in(cx, cy, 0.7 * r, 0.7 * r, 14, rnd):
            sh.append(("poly", sec_ellipse(px, py, 0.06 * m + 0.04, 0.06 * m + 0.04, 6), e, None, 0.1))
    elif key == "rosemary":                         # needle crosses
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 6, rnd):
            sh += [("line", [(px - 0.3 * m, py - 0.3 * m), (px + 0.3 * m, py + 0.3 * m)], e, 0.05),
                   ("line", [(px - 0.3 * m, py + 0.3 * m), (px + 0.3 * m, py - 0.3 * m)], e, 0.05)]
    elif key == "soft_rush":                        # an open centre and brown tufts on a ring
        sh.append(("poly", sec_ellipse(cx, cy, 0.25 * r, 0.25 * r, 14), SEC["paper"], None, 0.1))
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + 0.1)
            sh.append(("poly", sec_ellipse(cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a), 0.1 * r + 0.05,
                                           0.1 * r + 0.05, 6), PLA_REED_HEAD, None, 0.1))
    elif key == "rush":                             # spiny tips across the ray ends
        for i in range(8):
            a = 2 * _m.pi * (i / 8.0)
            px, py = cx + 0.9 * r * _m.cos(a), cy + 0.9 * r * _m.sin(a)
            sh.append(("line", [(px - 0.2 * m * _m.sin(a), py + 0.2 * m * _m.cos(a)),
                                (px + 0.2 * m * _m.sin(a), py - 0.2 * m * _m.cos(a))], e, 0.05))
    elif key == "mint":                             # small round leaves
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 5, rnd):
            sh.append(("poly", sec_ellipse(px, py, 0.14 * r, 0.14 * r, 8), None, e, 0.05))
    # chaste, lavender, loosestrife: their accent flowers (in _pla_plan) already set them apart
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
# ROUND 5 (S4, 1 Nov 2026): the round 4 note below is superseded where it says "one drawn set pen_black": people now
# come from the A1 library and the cutouts first, every figure as a solid body in one dark tone (FIG_SET
# "library_dark"; see "round 5 (S4 ..." above fig_side). The drawn poses below stay as the A1-language drawings the
# library lacks (wade, fishing, sit_step, ...), turned into the same solid body.
# ONE figure API for every drawing: fig_side / fig_top / fig_meta. Shapes are house shapes ("poly", ring, fill, stroke,
# lw) in the caller's units (k units per metre, y up), feet at (x, y).
# ROUND 4 (S1, 1 Nov 2026; G-R4-5.1, PLAN §4.8, decision N1 a): ONE people set, FIG_SET = "pen_black": the figures
# drawn here in the pen language (17 side poses, 14 plan poses incl. wade, fishing, dog walk), every body filled
# black (FIG_BODY_FILL, ink the same), on dark ground FIG_DARK_FILL with a thin white rim (dark=True). The raster
# cutouts (the "white" people, style a), the curated A1 library (figures_A1.json: pen strokes with no body, so it
# could not carry a black body and would be see-through) and the legacy silhouettes (fig_polys) are no longer
# reachable from fig_side / fig_top / fig_activity / fig_place_zones / fig_group / fig_stall; the `style` and `ink`
# arguments are still accepted and ignored, so no page can mix two sets or colour people (no white people, no people
# in the water colour). Each pose is posed by its contact: the step, rail, counter, water or branch it touches is a
# parameter, and the limbs are solved to reach it. fig_set_line() gives the log line "figures set=pen_black n".
# Adult 1.75 m (G6), cyclist 1.80 m overall (FIG_CYCLIST_H), child 1.15 m. Body proportions = Drillis & Contini (1966) segment ratios of stature (as reproduced in Winter,
# Biomechanics and Motor Control of Human Movement, Fig. 4.1; page not re-checked): FIG_DC below.
FIG_ADULT_H = 1.75             # m, G6 (brief 00 G6; PLAN D9)
FIG_A1_H = FIG_ADULT_H         # m, the drawn poses' stature
FIG_CYCLIST_H = 1.80           # m, G6 "cyclists about 1.8 m": ground to the top of the head of the riding figure
FIG_SET = "library_dark"       # round 5 (S4, G-R5-4.4, N1): the A1 library first, then the cutouts, then poses drawn
                               # in the A1 language; every one a solid body in ONE dark tone (was "pen_black")
FIG_A1_INK = "3A3A38"          # round 5 (PLAN §3 People): the one dark tone 3A3A38, opaque (was 1F1B18)
FIG_A1_LIB_H = 1.70            # m, the stature the A1 library JSON is drawn at (its "adult_m"; library/figures_A1/INDEX.md)
FIG_DARK_FILL = "2E2A27"       # body and pen on dark ground (dark=True), with a white rim
FIG_DARK_RIM = ("FFFFFF", 0.15)   # (colour, page mm) round the body on dark ground
FIG_COUNT = [0]                # figures drawn since the last fig_set_line(reset=True)
FIG_A1_PEN = 0.019              # m: pen width = the median stroke of the curated library at 1.70 m
FIG_PEN_MIN_MM = 0.10           # page mm: no figure line prints thinner (small scales get an outline)
FIG_DC = dict(chin=0.870, shoulder=0.818, elbow=0.630, wrist=0.485, hip=0.530, knee=0.285, ankle=0.039,
              upper_arm=0.186, forearm=0.146, hand=0.108, thigh=0.245, shank=0.246, foot=0.152,
              shoulder_w=0.259, hip_w=0.191)
FIG_CHILD_H = 1.15              # m, the project's child figure (fig_polys docstring)
FIG_BIKE = dict(wheel_r=0.336,  # 622 mm rim (ISO 5775 "700C") + 2 x 25 mm tyre = 672 mm: calculated
                wheelbase=1.00, crank=0.17, bb_h=0.27)  # drawing values (typical city bike), not sourced


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


class _FaFill(list):
    """a body fill ring (opaque, under the pen strokes): the drawn figures are never see-through (Aras 31 Oct)"""


class _FaProp(list):
    """round 5 (S4): a thin prop ring (fishing rod and line, ripples, bike wheels and frame, bag, leash): drawn as it
    is in the body colour, never merged into the solid body (sil_body would thicken or lose it)"""


def _fa_prop(r):
    return _FaProp(r) if r else None


def _fa_ellipse(cx, cy, rx, ry, n=16):
    import math as _m
    return [(cx + rx * _m.cos(2 * _m.pi * i / n), cy + ry * _m.sin(2 * _m.pi * i / n)) for i in range(n)]


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
    fills = [_FaFill(_fa_ellipse(hx, hy, B.hr[0], B.hr[1])), _FaFill(back + list(reversed(front)))]   # R2-A 31 Oct
    for e, hnd in arms:
        fills += [_FaFill(_fig_band((s[0] + 0.01, s[1] - 0.03), e, 0.05 * B.h, 3)), _FaFill(_fig_band(e, hnd, 0.04 * B.h, 3))]
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
        q1 = _fa_clip(_fa_off(P, [lw0, 0.6 * lw0, 0.12 * lw0]), cut_y)
        q2 = _fa_clip(_fa_off(P, [-lw0, -0.6 * lw0, -0.12 * lw0]), cut_y)
        if len(q1) >= 2 and len(q2) >= 2:
            fills.append(_FaFill(q1 + list(reversed(q2))))
        for side in ((1, -1) if i == 0 else (-1,)):     # the far leg: its back contour only
            Q = _fa_off(P, [side * lw0, side * 0.6 * lw0, side * 0.12 * lw0])
            Q = _fa_clip(Q, cut_y)
            if len(Q) >= 2:
                out.append(_fa_stroke(Q, rnd, w * (1.0 if side > 0 else 0.85)))
        if cut_y is None or an[1] > cut_y:
            out.append(_fa_stroke([(an[0] - 0.02, an[1] - B.L["ankle"] * 0.6), (an[0] + 0.6 * B.L["foot"], an[1] - B.L["ankle"])],
                                  rnd, w, over=0.1, smooth=False))
    return fills + [r for r in out if r]


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
                R.append(_fa_prop(_fa_stroke([(lx_ - 0.14, cut), (lx_ + 0.16, cut)], rnd, FIG_A1_PEN * 0.7, over=0.1)))
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
            R.append(_fa_prop(_fa_stroke([(bx - 0.10, by), (bx - 0.12, by - 0.30), (bx + 0.12, by - 0.31), (bx + 0.10, by)],
                                         rnd, FIG_A1_PEN * 0.8, over=0.05)))
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
        lean = p.get("lean", 0.30)                  # upright city-bike posture (drawing value)
        if "h_m" not in p:                          # G6: the rider's stature so the figure stands FIG_CYCLIST_H tall
            H = _fig_rider_h(FIG_CYCLIST_H, lean)
        legl = (D["thigh"] + D["shank"]) * H
        # saddle: the leg reaches 96 % of its length to the lowest pedal (nearly straight at the bottom of the stroke)
        hip = (bbp[0] - 0.24, bb - cr + 0.04 + _m.sqrt((0.96 * legl) ** 2 - 0.24 ** 2))
        bar = (front[0] - 0.12, hip[1] + 0.06)
        B = _FaBody(H, hip=hip, lean=lean)
        out = [_fa_prop(_fa_oval(rear[0], rear[1], r, r, rnd, gap=0.5, a0=0.3)),
               _fa_prop(_fa_oval(front[0], front[1], r, r, rnd, gap=0.5, a0=3.4))]
        out += [_fa_prop(_fa_stroke(P, rnd, FIG_A1_PEN * 0.75, over=0.04)) for P in (
            [rear, bbp, (hip[0] + 0.02, hip[1] - 0.08)], [(hip[0] + 0.02, hip[1] - 0.10), (bar[0] - 0.05, bar[1] - 0.10), front],
            [bbp, (bar[0] - 0.05, bar[1] - 0.10)], [rear, (hip[0] + 0.02, hip[1] - 0.10)],
            [(hip[0] - 0.10, hip[1] - 0.04), (hip[0] + 0.10, hip[1] - 0.03)], [(bar[0] - 0.05, bar[1] - 0.10), bar])]
        ang = 0.5
        pa = (bbp[0] + cr * _m.cos(ang), bbp[1] - cr * _m.sin(ang) * 1.0)
        pb = (bbp[0] - cr * _m.cos(ang), bbp[1] + cr * _m.sin(ang))
        legs = [B.leg((pa[0] - 0.05, pa[1] + 0.04), bend=1), B.leg((pb[0] - 0.05, pb[1] + 0.04), bend=1)]
        arms = [B.arm(bar, bend=-1)]
        out += _fa_draw(B, legs, arms, rnd, hatch=False, coat=0.0)
        an.update(length=wb + 2 * r, rider_h=H)
        return [o for o in out if o], an
    if pose == "child_play":                        # a child running / hopping, arms up (children playing)
        ch = p.get("child_h", FIG_CHILD_H)
        A = D["ankle"] * ch
        B = _FaBody(ch, lean=0.10)
        st = 0.42 * ch
        legs = [B.leg((0.5 * st, A + 0.10 * ch)), B.leg((-0.5 * st, A))]
        arms = [B.arm((B.sho[0] + 0.18 * ch, D["shoulder"] * ch + 0.16 * ch), bend=-1),
                B.arm((B.sho[0] - 0.20 * ch, D["shoulder"] * ch + 0.05 * ch), bend=1)]
        return _fa_draw(B, legs, arms, rnd, w=FIG_A1_PEN * 0.85, hatch=False, coat=0.03), dict(child_h=ch)
    if pose == "vendor":                            # behind the counter, both hands on it, facing the buyer (+x)
        ch = p.get("counter_h", FIG_STALL["counter_h"])
        A = D["ankle"] * H
        B = _FaBody(H, lean=0.08)
        arms = [B.arm((B.sho[0] + 0.40, ch + 0.04), bend=-1), B.arm((B.sho[0] + 0.32, ch + 0.03), bend=-1)]
        legs = [B.leg((0.04, A)), B.leg((-0.10, A))]
        an.update(counter_x=0.30, counter_y=ch)
        return _fa_draw(B, legs, arms, rnd, coat=0.06, hem=ch - 0.05), an
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
    if pose == "running":                           # round 3 G15: a runner, forward lean, long stride, arms bent
        A = D["ankle"] * H
        B = _FaBody(H, lean=0.20)
        legs = [B.leg((0.30 * H * 0.62, A + 0.02), bend=1), B.leg((-0.34 * H * 0.62, A + 0.16 * H * 0.62), bend=1)]
        s = B.sho
        arms = [B.arm((s[0] + 0.20, s[1] - 0.22), bend=-1), B.arm((s[0] - 0.22, s[1] - 0.30), bend=1)]
        return _fa_draw(B, legs, arms, rnd, coat=0.0, hem=B.hip[1] - 0.04), an
    if pose == "lying":                             # round 3 G15: lying on the lawn on the back, one knee up, a hand
        A = D["ankle"] * H                          # under the head; drawn upright, then laid down (head toward +x)
        B = _FaBody(H)
        legs = [B.leg((0.06, 0.26 * H), bend=1), B.leg((0.0, A))]
        arms = [B.arm((B.head[0] - 0.08, B.head[1] + 0.02), bend=-1), B.arm((0.04, D["wrist"] * H))]
        R = _fa_draw(B, legs, arms, rnd, hatch=False, coat=0.0)

        def lay(r):                                 # (x, y) upright -> (y, x): head to +x, front (x > 0) up
            q = [(py, px) for px, py in r]
            return _FaFill(q) if isinstance(r, _FaFill) else q
        R = [lay(r) for r in R if r]
        y0 = min(py for r in R for _px, py in r)
        R = [(_FaFill([(px, py - y0) for px, py in r]) if isinstance(r, _FaFill) else [(px, py - y0) for px, py in r])
             for r in R]
        L = max(px for r in R for px, _py in r)
        R = [(_FaFill([(px - 0.5 * L, py) for px, py in r]) if isinstance(r, _FaFill) else
              [(px - 0.5 * L, py) for px, py in r]) for r in R]      # centred on x: lies inside its footprint
        an.update(length=L)
        return R, an
    if pose == "fishing":                           # round 3 G15: standing at the edge, rod out over the water, the
        A = D["ankle"] * H                          # line down to it. water_dy = the water level in m relative to
        B = _FaBody(H, lean=0.04)                   # the feet (negative = below); rod 3.0 m at 35 deg: drawing rule
        legs = [B.leg((0.06, A)), B.leg((-0.14, A))]
        grip = (B.sho[0] + 0.30, D["wrist"] * H + 0.18)
        arms = [B.arm(grip, bend=-1), B.arm((grip[0] - 0.12, grip[1] - 0.08), bend=-1)]
        R = _fa_draw(B, legs, arms, rnd, coat=0.05)
        rod_l, ang = p.get("rod_m", 3.0), _m.radians(p.get("rod_deg", 35.0))
        butt = (grip[0] - 0.25 * _m.cos(ang), grip[1] - 0.25 * _m.sin(ang))
        tip = (grip[0] + (rod_l - 0.25) * _m.cos(ang), grip[1] + (rod_l - 0.25) * _m.sin(ang))
        R.append(_fa_prop(_fa_stroke([butt, tip], rnd, FIG_A1_PEN * 0.6, over=0.0, wob=0.002, smooth=False)))
        wy = p.get("water_dy", -0.5)
        if wy < tip[1]:
            R.append(_fa_prop(_fa_stroke([tip, (tip[0] + 0.05, wy)], rnd, FIG_A1_PEN * 0.3, over=0.0, wob=0.0,
                                         smooth=False)))
        an.update(rod_tip=tip, line_end=(tip[0] + 0.05, wy), reach_x=tip[0])
        return [r for r in R if r], an
    if pose == "dog_walk":                          # round 3 G15: walking with a dog on a leash ahead of the walker;
        A = D["ankle"] * H                          # dog 0.55 m at the shoulder, 0.80 m long: drawing rule (a
        B = _FaBody(H, lean=0.03)                   # medium-sized dog), not data
        st = 0.30 * H
        legs = [B.leg((0.5 * st, A)), B.leg((-0.5 * st, A))]
        hand = (0.30, D["wrist"] * H + 0.08)
        arms = [B.arm(hand, bend=-1), B.arm((-0.16, D["wrist"] * H))]
        R = _fa_draw(B, legs, arms, rnd, coat=0.05)
        dh, dl = p.get("dog_h", 0.55), p.get("dog_l", 0.80)
        x0 = p.get("dog_ahead", 1.10)               # the dog's hind end, m ahead of the walker's feet
        back = dh * 0.92
        body = [(x0, back - 0.02), (x0 + 0.10, back + 0.02), (x0 + 0.62 * dl, back + 0.03), (x0 + 0.80 * dl, back),
                (x0 + 0.80 * dl, back - 0.20), (x0 + 0.62 * dl, back - 0.26), (x0 + 0.10, back - 0.24), (x0, back - 0.16)]
        head = [(x0 + 0.78 * dl, back - 0.04), (x0 + 0.86 * dl, dh + 0.12), (x0 + 0.98 * dl, dh + 0.14),
                (x0 + 1.12 * dl, dh + 0.04), (x0 + 1.10 * dl, dh - 0.02), (x0 + 0.92 * dl, dh - 0.05), (x0 + 0.84 * dl, back - 0.16)]
        R += [_FaFill(body), _FaFill(head)]
        R.append(_fa_stroke(body + [body[0]], rnd, FIG_A1_PEN * 0.8, over=0.0, wob=0.003, smooth=False))
        R.append(_fa_stroke(head, rnd, FIG_A1_PEN * 0.8, over=0.0, wob=0.003, smooth=False))
        for lx_, sw in ((0.06, -0.06), (0.18, 0.06), (0.66 * dl, 0.06), (0.74 * dl, -0.05)):   # four legs, mid-trot
            R.append(_fa_stroke([(x0 + lx_, back - 0.20), (x0 + lx_ + 0.5 * sw, 0.25), (x0 + lx_ + sw, 0.02)], rnd,
                                FIG_A1_PEN * 0.9, over=0.02))
        R.append(_fa_stroke([(x0 + 0.01, back - 0.03), (x0 - 0.12, back + 0.12)], rnd, FIG_A1_PEN * 0.7, over=0.0))   # tail
        collar = (x0 + 0.86 * dl, back - 0.02)
        R.append(_fa_prop(_fa_stroke([arms[0][1], ((hand[0] + collar[0]) / 2.0, min(hand[1], collar[1]) - 0.12), collar],
                                     rnd, FIG_A1_PEN * 0.4, over=0.0, wob=0.002)))
        an.update(length=x0 + 1.12 * dl + 0.2, dog_x=x0, dog_h=dh)
        return [r for r in R if r], an
    return None, an


def _fa_top(pose, seed=0, **p):
    """plan figures, m, centred on (0, 0), heading +x: open shoulder oval, small head oval, one-sided hatch"""
    rnd = _fa_rand(seed + 5)
    H = p.get("h_m", FIG_A1_H)
    sw, dp = FIG_DC["shoulder_w"] * H, 0.15 * H

    def one(cx, cy, s=1.0, hatch=True):
        o = [_FaFill(_fa_ellipse(cx, cy, 0.5 * dp * s, 0.5 * sw * s)),          # round 4: black body (shoulders,
             _FaFill(_fa_ellipse(cx + 0.03 * s, cy, 0.07 * s, 0.065 * s)),       # head), nothing see-through
             _fa_oval(cx, cy, 0.5 * dp * s, 0.5 * sw * s, rnd, gap=0.7, a0=2.4),
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
    elif pose == "child_play":
        R = one(0.0, 0.0, s=p.get("child_h", FIG_CHILD_H) / H, hatch=False)
    elif pose in ("vendor", "fishing"):
        R = one(0.0, 0.0)
        if pose == "fishing":
            R.append(_fa_stroke([(0.15, 0.05), (2.6, 0.10)], rnd, FIG_A1_PEN * 0.6, over=0.0, smooth=False))
    elif pose == "running":
        R = one(0.0, 0.0) + [_fa_stroke([(0.25, 0.08), (0.45, 0.10)], rnd), _fa_stroke([(-0.40, -0.08), (-0.22, -0.08)], rnd)]
    elif pose == "lying":
        R = [_FaFill(_fa_ellipse(0.0, 0.0, 0.85, 0.22)), _FaFill(_fa_ellipse(0.72, 0.0, 0.08, 0.075)),
             _fa_oval(0.0, 0.0, 0.85, 0.22, rnd, gap=0.5, a0=2.4), _fa_oval(0.72, 0.0, 0.08, 0.075, rnd, gap=1.0, a0=0.5)]
    elif pose == "dog_walk":
        R = one(0.0, 0.0) + [_FaFill(_fa_ellipse(1.45, 0.0, 0.40, 0.12)), _fa_oval(1.45, 0.0, 0.40, 0.12, rnd, gap=0.6, a0=2.4),
                             _fa_stroke([(0.10, 0.10), (1.80, 0.02)], rnd, FIG_A1_PEN * 0.4, over=0.0)]
    elif pose == "adult_child":
        ch = p.get("child_h", FIG_CHILD_H) / H
        R = one(0.0, 0.20) + one(0.0, -0.22, s=ch, hatch=False) + [_fa_stroke([(0.02, 0.0), (0.04, -0.06)], rnd, FIG_A1_PEN * 0.8)]
    else:
        return None
    return [r for r in R if r]


FIG_DRAWN_SIDE = ("stand", "walk", "watch", "wade", "sit_step", "touch", "stall", "railing", "olive", "bike", "adult_child",
                  "child_play", "vendor", "running", "lying", "fishing", "dog_walk")
FIG_DRAWN_TOP = ("stand", "watch", "walk", "sit", "sit_step", "sit_chair", "bike", "adult_child", "child_play", "vendor",
                 "running", "lying", "fishing", "dog_walk")
FIG_POSE_ALIAS = {"sit": "sit_step", "cycle": "bike", "trade": "stall", "buy": "stall", "children": "child_play",
                  "play": "child_play", "sell": "vendor", "run": "running", "jog": "running", "lie": "lying",
                  "fish": "fishing", "dog": "dog_walk"}
FIG_SIDE_ALIAS = {"lean": "watch", "sit_chair": "sit_step"}   # round 4: side poses the drawn set lacks -> nearest drawn
FIG_BODY_FILL = FIG_A1_INK   # round 5: the body = the one dark tone 3A3A38, opaque; nothing see-through


def _fig_rider_h(top, lean):
    """the stature whose bike pose reaches `top` m (head top above the ground) at this lean (fixed-point solve on
    the pose's own geometry: saddle from the leg length, then hip-shoulder-head at the lean)"""
    import math as _m
    D, F = FIG_DC, FIG_BIKE
    c = _m.cos(lean)
    H = FIG_ADULT_H
    for _ in range(8):
        legl = (D["thigh"] + D["shank"]) * H
        hip = F["bb_h"] - F["crank"] + 0.04 + _m.sqrt(max(0.0, (0.96 * legl) ** 2 - 0.24 ** 2))
        t = hip + (D["shoulder"] - D["hip"]) * H * c + (1.0 - D["shoulder"]) * H * c + 0.060 * H * (1.0 - c)
        H += (top - t) / 0.95
    return H


def fig_meta(pose, facing=1, pick=0, **p):
    """anchors of a figure in m relative to its feet (x mirrored for facing -1): wade water_y; sit_step seat_x,
    seat_y; railing rail_x, rail_y; stall counter_x, counter_y; olive hand_x, hand_y, reached; touch hand;
    adult_child hand, child_h; bike length; lean (library) ledge_y_m. Use them to place the step, rail, counter or
    water the figure touches."""
    pose = _fig_side_pose(FIG_POSE_ALIAS.get(pose, pose))
    an = dict(_fa_side(pose, pick, **p)[1] or {})
    s = 1.0 if facing >= 0 else -1.0
    for k_ in list(an):
        v = an[k_]
        if k_.endswith("_x"):
            an[k_] = s * v
        elif isinstance(v, tuple):
            an[k_] = (s * v[0], v[1])
    return an


def _fig_side_pose(pose):
    """the drawn side pose for a pose name (aliases, then the nearest drawn pose)"""
    pose = FIG_SIDE_ALIAS.get(pose, pose)
    return pose if pose in FIG_DRAWN_SIDE else "stand"


def fig_set_line(reset=True):
    """the log line proving the one people set ran (round 5, PLAN §2 N1): "figures source=asset_library n,
    drawn_A1_style n" (since the last reset; asset_library = A1 library + cutouts, drawn_A1_style = poses neither
    has, drawn in the A1 language with the same solid body; plan views count as drawn_A1_style)"""
    a, d = FIG_SRC_COUNT.get("asset_library", 0), FIG_SRC_COUNT.get("drawn_A1_style", 0)
    if reset:
        FIG_COUNT[0] = 0
        FIG_SRC_COUNT.clear()
    return u"figures source=asset_library %d, drawn_A1_style %d" % (a, d)


def _fig_body(layer=0, dark=False):
    """(body fill, pen, rim stroke, rim lw) of the one set at a depth layer: nearer stronger, farther paler, opaque"""
    col = FIG_DARK_FILL if dark else FIG_BODY_FILL
    c = fig_fade(col, layer)
    return c, c, (FIG_DARK_RIM[0] if dark else None), (FIG_DARK_RIM[1] if dark else 0.0)


# ---- round 5 (S4, G-R5-4.4, N1 answered 1 Nov 22:44, PLAN §2a.1): people from the asset library, solid dark ------
# Order per pose: (1) the A1 library (Data/figures_A1.json: stand, walk, watch, lean), (2) the cutouts
# (Data/cutouts: market buyer, vendor, children playing), (3) the poses neither holds (wade, fishing, sit_step, touch,
# railing, olive, bike, adult_child, running, lying, dog_walk) drawn anew in the A1 language: the A1 pen drawing of
# the pose (_fa_side, solved to its contact: step, water, rail, counter, branch) given the SAME solid body as the
# library figures. Every body = sil_body: the drawing's strokes rasterised, closed, holes filled, the outline traced
# (silhouette.py), so library and drawn people read as one set: one dark tone FIG_BODY_FILL, opaque, no face, no
# hatch. Thin props (rod, fishing line, wheels, bag, leash, ripples) stay as their pen rings in the same tone.
# Recovered from be9c3fb (fig_library, _fig_lib_k, _fig_pick, FIG_LOG) and a936d62 (the cutout reader, now
# silhouette.py sil_cut_library). Sitting on a chair, the A1 sit_chair and the cutouts' step-sitters carry their seat
# in the drawing (it would turn dark too), so seated people are drawn (sit_step) and sit on the real step/bench.
FIG_LOG = []
_FIG_LIB = {}
FIG_SRC_COUNT = {}
FIG_LIB_POSES = ("stand", "walk", "watch", "lean")                 # poses the A1 library holds and pages use
FIG_CUT_POSES = {"stall": "person_stall", "vendor": "person_vendor", "child_play": "person_child_play"}
FIG_BODY_CLOSE_M = (0.04, 0.08, 0.14)   # m: closing radii tried in turn until the body fills >= FIG_BODY_MIN_FILL of
FIG_BODY_MIN_FILL = 0.30                # its box (pen drawings with open contours need more; drawing rule)
FIG_BODY_PX_M = 0.01                    # m per raster cell (1 cm: 0.1 mm at 1:100, below print resolution)
FIG_FLAGS = {}                          # FLAG counters (fishing refused where no water is drawn ...)


def fig_library():
    """the curated A1 library (dict id -> figure) or {} when Downloads/Bergama/Data/figures_A1.json is missing
    (recovered from be9c3fb:src/common/figures.py:143-165)"""
    import os as _o
    import json as _j
    if "lib" in _FIG_LIB:
        return _FIG_LIB["lib"]
    lib = {}
    root = _o.path.join(_o.path.expanduser("~"), "Downloads", "Bergama", "Data")
    for p in (_o.path.join(root, "figures_A1.json"), _o.path.join(root, "figures", "figures_A1.json")):
        if _o.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    js = _j.load(fh)
                lib = js.get("figures", {})
                _FIG_LIB["adult_m"] = float(js.get("adult_m") or FIG_A1_LIB_H)
                FIG_LOG.append(u"Figures: %d A1 figures from %s" % (len(lib), p))
                break
            except Exception as ex:
                FIG_LOG.append(u"FLAG Figures: %s unreadable (%s); drawn A1-style figures used" % (p, type(ex).__name__))
    if not lib:
        FIG_LOG.append(u"FLAG Figures: Data/figures_A1.json not found; drawn A1-style figures used for every pose")
    _FIG_LIB["lib"] = lib
    return lib


def _fig_lib_k():
    """factor from the library's drawn stature to FIG_ADULT_H (1.75 / 1.70)"""
    fig_library()
    return FIG_ADULT_H / float(_FIG_LIB.get("adult_m") or FIG_A1_LIB_H)


def _fig_pick(pose, pick):
    """a library figure of this pose (by id, else the pick-th of the sorted ids with that pose), or None"""
    lib = fig_library()
    if pose in lib:
        return lib[pose]
    ids = sorted(k_ for k_, f in lib.items() if f.get("pose") == pose)
    return lib[ids[int(pick) % len(ids)]] if ids else None


def _fig_solid(key, rings):
    """the solid body of pen rings (m): closing radius stepped up until the body fills its box enough"""
    if key in _SIL_BODY:
        return _SIL_BODY[key]
    pts = [q for r in rings for q in r]
    if not pts:
        return []
    bw = (max(q[0] for q in pts) - min(q[0] for q in pts)) * (max(q[1] for q in pts) - min(q[1] for q in pts)) or 1.0
    out, used = [], None
    for cm in FIG_BODY_CLOSE_M:
        out = sil_body(rings, FIG_BODY_PX_M, cm)
        used = cm
        if sum(abs(_sil_area(R)) for R in out) >= FIG_BODY_MIN_FILL * bw:
            break
    if used != FIG_BODY_CLOSE_M[0]:
        FIG_LOG.append(u"figures: %s body closed at %.2f m" % (key[1] if isinstance(key, tuple) else key, used))
    _SIL_BODY[key] = out
    return out


def _fig_side_dark(pose, pick, p):
    """(source, body rings m, prop rings m, anchors) of one side figure, feet at (0, 0), facing +x"""
    lib_pose = "lean" if pose == "railing" else pose
    if lib_pose in FIG_LIB_POSES:
        f = _fig_pick(lib_pose, pick)
        ok = f is not None
        if ok and pose == "railing":                   # the A1 leaner fits only a rail at its ledge height
            ledge = float((f.get("anchor") or {}).get("ledge_y_m", 0.0)) * _fig_lib_k()
            ok = abs(p.get("rail_h", 1.10) - ledge) <= 0.10
        if ok:
            lk = _fig_lib_k()
            fl = -1.0 if (f.get("facing") or 0) < 0 else 1.0     # the file's facing -> +x
            rings = [[(fl * a * lk, b * lk) for a, b in r] for r in f["rings"]]
            an = dict(_fa_side(_fig_side_pose(pose), pick, **p)[1] or {})
            if pose == "railing":
                an.update(rail_y=float(f["anchor"]["ledge_y_m"]) * lk)
            fid = [k_ for k_, v in fig_library().items() if v is f]
            return "asset_library", _fig_solid(("a1", fid[0] if fid else lib_pose), rings), [], an
    ck = FIG_CUT_POSES.get(pose)
    if ck:
        lib = sil_cut_library().get(ck)
        if lib:
            import os as _o
            e = lib[int(pick) % len(lib)]
            body, _w = sil_alpha_body(_o.path.join(sil_cut_dir(), e["file"]), float(e["h_m"]), FIG_BODY_PX_M, 0.02)
            if body:
                if (e.get("facing", 1) or 1) < 0:
                    body = [[(-a, b) for a, b in r][::-1] for r in body]
                an = dict(_fa_side(_fig_side_pose(pose), pick, **p)[1] or {})
                return "asset_library", body, [], an
    dp = _fig_side_pose(pose)
    p = dict((k_, (round(v / 0.02) * 0.02 if isinstance(v, float) else v)) for k_, v in p.items())   # 2 cm steps:
    rings, an = _fa_side(dp, pick % 3, **p)                                                         # bodies reused
    if not rings:
        rings, an = _fa_side("stand", pick % 3)
    rings = [r for r in rings if r]
    props = [r for r in rings if isinstance(r, _FaProp)]
    key = ("drawn", dp, pick % 3) + tuple(sorted((k_, round(v, 2)) for k_, v in p.items()
                                                 if isinstance(v, (int, float)) and not isinstance(v, bool)))
    body = _fig_solid(key, [r for r in rings if not isinstance(r, _FaProp)])
    return "drawn_A1_style", body, props, dict(an or {})


def fig_side(pose, x, y, k, facing=1, ink=None, pick=None, mm_per_m=None, pen_min_mm=FIG_PEN_MIN_MM, layer=0, style="b",
             dark=False, **p):
    """side-view figure of the one set (FIG_SET "library_dark", round 5), feet at (x, y), k units per m, facing -1 =
    mirrored. pose: stand, walk, watch, lean (A1 library); stall, vendor, child_play (cutouts); wade depth_m,
    fishing water_dy, sit_step seat_h, touch reach_y, railing rail_h, olive branch_h, bike, adult_child child_h,
    running, lying, dog_walk (drawn in the A1 language); aliases FIG_POSE_ALIAS (sit_chair -> sit_step,
    touch_water -> touch). pick (default: from x, y) picks the variant. layer: depth layer 0 / 1 / 2 (smaller and
    paler, opaque: fig_depth). dark=True on dark ground (FIG_DARK_FILL + white rim). ink and style are ignored (one
    set, one dark tone). mm_per_m / pen_min_mm: props (rod, line, wheels) never print thinner than pen_min_mm.
    Returns house shapes ("poly", ring, fill, stroke, lw): the solid body, then the props."""
    pose = FIG_POSE_ALIAS.get(pose, pose)
    if pose == "touch_water":                          # R2-C: bending to the water
        pose = "touch"
    if pose == "sit_chair":
        pose = "sit_step"
    if pose == "fishing" and p.get("water_dy") is None:   # round 5 (U36): no water given = no fishing line into soil
        pose = "watch"
        FIG_FLAGS["fishing -> watch (no water_dy)"] = FIG_FLAGS.get("fishing -> watch (no water_dy)", 0) + 1
    sc, _fade = fig_depth(layer)
    k = k * sc
    body, _ink, rim, rim_lw = _fig_body(layer, dark)
    if pick is None:                                   # variety: the place picks the figure, the same every run
        pick = int(abs(x * 7.31 + y * 3.17) * 10.0) % 997
    src, B, P, _an = _fig_side_dark(pose, pick, p)
    flip = 1.0 if facing >= 0 else -1.0
    add = max(0.0, pen_min_mm - FIG_A1_PEN * (mm_per_m or k))
    FIG_COUNT[0] += 1
    FIG_SRC_COUNT[src] = FIG_SRC_COUNT.get(src, 0) + 1
    out = [("poly", [(x + flip * a * k, y + b * k) for a, b in r], body, rim, rim_lw) for r in B]
    out += [("poly", [(x + flip * a * k, y + b * k) for a, b in r], body, body if add > 0 else None, add) for r in P]
    return out


def fig_top(pose, x, y, k, ang=0.0, ink=None, pick=0, mm_per_m=None, pen_min_mm=FIG_PEN_MIN_MM, style="b", dark=False,
            **p):
    """plan figure of the one set centred on (x, y), heading ang (radians, 0 = +x), k units per m: FIG_DRAWN_TOP
    (stand, watch, walk, sit, sit_step, sit_chair, bike, adult_child child_h, child_play, vendor, running, lying,
    fishing, dog_walk). Black body (shoulders and head filled), same pen and mm_per_m rule as fig_side; dark=True on
    dark ground; ink and style are ignored (round 4: one set)."""
    import math as _m
    body, ink, rim, rim_lw = _fig_body(0, dark)
    rings = _fa_top(FIG_POSE_ALIAS.get(pose, pose), pick, **p) or _fa_top("stand", pick)
    rings = [r for r in rings if isinstance(r, _FaFill)] + [r for r in rings if not isinstance(r, _FaFill)]
    FIG_SRC_COUNT["drawn_A1_style"] = FIG_SRC_COUNT.get("drawn_A1_style", 0) + 1   # round 5: plan views (no library)
    ca, sa = _m.cos(ang), _m.sin(ang)
    add = max(0.0, pen_min_mm - FIG_A1_PEN * (mm_per_m or k))
    FIG_COUNT[0] += 1
    return [("poly", [(x + (px * ca - py * sa) * k, y + (px * sa + py * ca) * k) for px, py in r], body, rim, rim_lw)
            if isinstance(r, _FaFill) else
            ("poly", [(x + (px * ca - py * sa) * k, y + (px * sa + py * ca) * k) for px, py in r], ink,
             ink if add > 0 else None, add) for r in rings]


# ---- D9 depth layers (H-B 30 Oct 2026): 0 = the cut plane (true size, G6 asserts here), 1 = mid, 2 = back --------
# (scale, tone mix toward the paper, raster alpha: no longer used, cutouts are opaque toned copies since R2-A 31 Oct).
FIG_DEPTH = {0: (1.00, 0.00, 1.00), 1: (0.80, 0.40, 0.70), 2: (0.62, 0.62, 0.45)}


def fig_depth(layer=0):
    """(scale, fade) of a D9 depth layer: 0 -> (1.00, 0.0), 1 -> (0.80, 0.40), 2 -> (0.62, 0.62)"""
    s, f, _a = FIG_DEPTH.get(int(layer or 0), FIG_DEPTH[0])
    return s, f


def _fig_mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


def fig_fade(col, layer=0, paper=None):
    """a hex colour faded toward the paper for depth layer `layer` (unchanged at layer 0 or for None)"""
    f = fig_depth(layer)[1]
    if not col or f <= 0.0:
        return col
    return _fig_mix(col, paper or (globals().get("SEC") or {}).get("paper", "F1EDDF"), f)


# ---- D1 style a: raster cutouts (PNG with alpha) -------------------------------------------------------------------
# Round 4 (S1, N1 a): PEOPLE no longer use cutouts. Round 4 closing: cut_image and its reader (cut_dir, cut_library,
# _cut_px, CUT_LOG, _CUT_LIB) deleted: no caller anywhere in src/ (closing part C grep B). cut_log_line stays for its
# callers (proposal sections, site board p07, water board p12/p14/p18, masterplan): with no cutout drawn it returns
# None.
CUT_MISSING = {}
CUT_USED = {}


def cut_log_line():
    """one log line: cutouts drawn, and the items drawn in style b because their cutout is missing"""
    n_ok, n_miss = sum(CUT_USED.values()), sum(CUT_MISSING.values())
    if not n_ok and not n_miss:
        return None
    s = u"Cutouts (style a): %d drawn" % n_ok
    if n_miss:
        s += u"; %d drawn in style b, no cutout for: %s" % (n_miss, u", ".join(sorted(CUT_MISSING)))
    return s


# ---- market stall / canopy (G6 true size) --------------------------------------------------------------------------
# counter_h 0.90 m = the repo's stall pose value (fig_side "stall" counter_h); every other size is DRAWN TO TYPE (a
# typical open-market trestle stall), not data: never print them as measured.
FIG_STALL = dict(counter_h=0.90, depth_m=1.00, width_m=2.00, canopy_h=2.30, canopy_top=2.60, canopy_over=0.35,
                 post_m=0.05, top_m=0.05)


def fig_stall(x, gy, k, facing=1, layer=0, vendor=True, buyer=True, seed=0, ink=None, fill=None, canopy=None,
              style="b"):
    """a market stall in section at true size, its counter's front edge at x (page mm), ground gy, k mm per m:
    trestle counter (FIG_STALL), two posts and a sloped canopy, a vendor behind and a buyer in front (facing = the
    side the buyers stand on). Drawn in vector always (round 4: no cutout; style is ignored). Returns house shapes."""
    sc, _fd = fig_depth(layer)
    K = k * sc
    g = gy(x) if callable(gy) else gy
    S, f = FIG_STALL, (1.0 if facing >= 0 else -1.0)
    ink = fig_fade(ink or FIG_A1_INK, layer)
    fill = fig_fade(fill or "E9E2D0", layer)
    can = fig_fade(canopy or "C9B48A", layer)
    d, ch = S["depth_m"] * K, S["counter_h"] * K
    xb = x - f * d                                     # the back edge (the vendor's side)
    sh = []
    if True:
        x0, x1 = min(x, xb), max(x, xb)
        sh.append(("poly", [(x0, g + ch - S["top_m"] * K), (x1, g + ch - S["top_m"] * K), (x1, g + ch), (x0, g + ch)],
                   fill, ink, 0.12))
        xm = (x0 + x1) / 2.0                                             # trestle: two crossed legs
        sh.append(("line", [(x0 + 0.1 * K, g), (x1 - 0.1 * K, g + ch - S["top_m"] * K)], ink, 0.12))
        sh.append(("line", [(x1 - 0.1 * K, g), (x0 + 0.1 * K, g + ch - S["top_m"] * K)], ink, 0.12))
        sh.append(("line", [(xm - 0.25 * K, g + 0.5 * ch), (xm + 0.25 * K, g + 0.5 * ch)], ink, 0.08))
        sh.append(("poly", [(x0 + 0.1 * K, g + ch + 0.02 * K), (x1 - 0.1 * K, g + ch + 0.02 * K),
                            (x1 - 0.18 * K, g + ch + 0.16 * K), (x0 + 0.18 * K, g + ch + 0.16 * K)],
                   fig_fade("B98E5A", layer), None, 0.1))                # goods on the counter
        pb, pf = xb - f * 0.05 * K, x + f * S["canopy_over"] * 0.2 * K
        for px_ in (pb, pf):
            sh.append(("line", [(px_, g), (px_, g + S["canopy_h"] * K)], ink, max(0.12, S["post_m"] * K)))
        cb, cf = xb - f * 0.15 * K, x + f * S["canopy_over"] * K
        sh.append(("poly", [(cb, g + S["canopy_top"] * K), (cf, g + S["canopy_h"] * K),
                            (cf, g + (S["canopy_h"] - 0.12) * K), (cb, g + (S["canopy_top"] - 0.12) * K)], can, ink, 0.12))
        for i in range(3):                             # scalloped valance on the front
            vx = cf - f * (i + 0.5) * 0.12 * K
            sh.append(("poly", [(vx - 0.06 * K, g + (S["canopy_h"] - 0.12) * K), (vx + 0.06 * K, g + (S["canopy_h"] - 0.12) * K),
                                (vx, g + (S["canopy_h"] - 0.22) * K)], can, None, 0.1))
    if vendor:
        sh += fig_side("vendor", xb - f * 0.35 * k * sc, g, k, facing=facing, ink=ink, layer=layer, style=style,
                       pick=seed)
    if buyer:
        sh += fig_side("stall", x + f * 0.45 * k * sc, g, k, facing=-facing, ink=ink, layer=layer, style=style,
                       pick=seed + 1)
    return sh


# ---- groups and activity sets per zone type (G10) ------------------------------------------------------------------
def fig_group(x, gy, k, n=3, seed=0, layer=0, ink=None, style="b"):
    """2-4 people standing together in conversation (drawn stand / watch figures of the one set, one hand-in-hand pair
    when n >= 3), turned toward each other; x = the group's centre. Returns house shapes."""
    rnd = _fa_rand(seed + 41)
    g = gy(x) if callable(gy) else gy
    sc = fig_depth(layer)[0]
    n = max(2, min(4, int(n)))
    sh, off = [], -0.5 * (n - 1) * 0.55
    for i in range(n):
        xi = x + (off + i * 0.55 + 0.08 * rnd()) * k * sc
        pose = ("adult_child" if (i == n - 1 and n >= 3) else ("watch" if i % 2 else "stand"))
        sh += fig_side(pose, xi, gy(xi) if callable(gy) else g, k, facing=(1 if i < n / 2.0 else -1), ink=ink,
                       layer=layer, style=style, pick=seed + i)
    return sh


# zone type -> [(pose, weight, footprint m along the cut)]; "market" = a stall with vendor and buyer, "group" =
# fig_group. Only poses that fit the zone (G10); "bed" is for the wet bed only (pass water=), never a dry bed (p12).
FIG_ACTIVITY = {
    "bike_lane": [("bike", 1.0, 1.9)],
    "walkway": [("walk", 3.0, 0.8), ("adult_child", 1.5, 1.0), ("group", 1.0, 1.7), ("watch", 0.6, 0.6),
                ("running", 1.0, 1.2), ("dog_walk", 1.0, 2.4)],                    # round 3 G15: runners, dogs
    "viewing_terrace": [("watch", 2.0, 0.7), ("railing", 2.0, 0.8), ("sit_step", 1.0, 0.8), ("group", 1.0, 1.7)],
    "wading_strip": [("wade", 3.0, 0.8), ("touch_water", 1.5, 0.9), ("child_play", 1.5, 0.8)],   # R2-C: water actions
    "market_ground": [("market", 3.0, 3.2), ("walk", 1.0, 0.8), ("adult_child", 1.0, 1.0), ("group", 1.0, 1.7)],
    "sun_steps": [("sit_step", 4.0, 0.8), ("watch", 0.5, 0.7), ("touch", 0.5, 0.9)],
    "bridge_crossing": [("walk", 3.0, 0.8), ("railing", 1.5, 0.8), ("bike", 0.7, 1.9), ("watch", 1.0, 0.7),
                        ("dog_walk", 0.6, 2.4), ("running", 0.5, 1.2)],
    "bed": [("wade", 2.0, 0.8), ("touch", 1.0, 0.9), ("child_play", 1.0, 0.8)],
    "stepping_stones": [("walk", 2.0, 0.8), ("adult_child", 1.5, 1.0), ("stand", 0.6, 0.6)],   # R2-A: on the stones
    "lawn": [("child_play", 1.5, 0.8), ("group", 1.0, 1.7), ("walk", 1.0, 0.8), ("adult_child", 1.0, 1.0),
             ("lying", 1.2, 2.0), ("dog_walk", 0.8, 2.4)],                         # round 3 G15: sunbathing, dogs
    "water_edge": [("fishing", 2.0, 1.0), ("watch", 1.0, 0.7), ("touch", 0.6, 0.9)],   # round 3: the dry bank edge
}
FIG_FOCUS_POSES = ("watch", "railing", "sit_step", "touch", "touch_water", "stand", "adult_child", "fishing")   # R2-C scenes
FIG_PAIR_POSES = ("wade", "child_play")        # R2-C scenes: playing together in the water or on the lawn
FIG_ZONE_ALIAS = {"bike": "bike_lane", "walk": "walkway", "terrace": "viewing_terrace", "wading": "wading_strip",
                  "market": "market_ground", "steps": "sun_steps", "bridge": "bridge_crossing",
                  "stream_bed": "bed", "stones": "stepping_stones", "open_ground": "lawn", "edge": "water_edge",
                  "fishing": "water_edge", "bank_edge": "water_edge"}


def fig_activity(zone, x0, x1, gy, k, layer=0, seed=0, density=1.0, ink=None, style="b", water=None, max_n=None,
                 acts=None, focus=None, **p):
    """people doing what the zone is for, placed along x0..x1 (page mm) on the ground gy (number or function of x),
    k mm per m: poses drawn from FIG_ACTIVITY[zone] by weight, never the same pose twice in a row (when the zone has
    two or more), irregular gaps (0.6-3.2 m / density), at least two people where two fit. water = the water level
    (page y, or a function of x) for wading figures (their depth). p goes to every figure (seat_h, rail_h, ...).
    acts: this zone's [(pose, weight, footprint m)] instead of FIG_ACTIVITY's (fig_place_zones filters it).
    focus (page x, R2-C scenes, Aras 31 Oct 12:01 "they look like they are just put there"): people who stay look at
    it (the water, a stall, a view), people playing in the water turn to each other in pairs, walkers and riders
    keep their own way. Returns (shapes, placed [(pose, x page mm)])."""
    zone = FIG_ZONE_ALIAS.get(zone, zone)
    if zone not in FIG_ACTIVITY:
        raise KeyError("fig_activity: zone %r; known: %s" % (zone, ", ".join(sorted(FIG_ACTIVITY))))
    acts = acts or FIG_ACTIVITY[zone]
    rnd = _fa_rand(seed * 13 + 7)
    sc = fig_depth(layer)[0]
    K = k * sc
    sh, placed, last = [], [], None
    x = x0 + (0.3 + 0.8 * (rnd() + 0.5)) * K
    while True:
        cand = [a for a in acts if a[0] != last] or acts
        tot = sum(a[1] for a in cand)
        t, pick = (rnd() + 0.5) * tot, cand[-1]
        for a in cand:
            t -= a[1]
            if t <= 0:
                pick = a
                break
        pose, _w, foot = pick
        if x + foot * K > x1:
            if len(placed) < 2:                        # try the narrowest pose before giving up
                pose, _w, foot = min(acts, key=lambda a: a[2])
                if x + foot * K > x1:
                    break
            else:
                break
        cx = x + 0.5 * foot * K
        g = gy(cx) if callable(gy) else gy
        fac = 1 if rnd() > 0 else -1
        if focus is not None and pose in FIG_FOCUS_POSES:
            fac = 1 if focus >= cx else -1
        elif focus is not None and pose in FIG_PAIR_POSES:
            fac = 1 if len(placed) % 2 == 0 else -1    # pairs turned to each other (left looks right, right looks left)
        if pose == "market":
            sh += fig_stall(cx + 0.5 * FIG_STALL["depth_m"] * K, gy, k, facing=fac, layer=layer, seed=seed + len(placed),
                            ink=ink, style=style)
        elif pose == "group":
            sh += fig_group(cx, gy, k, n=2 + int((rnd() + 0.5) * 2.99), seed=seed + len(placed), layer=layer, ink=ink,
                            style=style)
        else:
            q = dict(p)
            if pose == "wade" and water is not None:
                wl = water(cx) if callable(water) else water
                q["depth_m"] = max(0.05, min(globals().get("FIG_WADE_MAX_M", FIG_DC["knee"] * FIG_A1_H * 1.4),
                                             (wl - g) / K))
            if pose == "fishing":                           # the line drops to the water below the bank
                wl = None if water is None else (water(cx) if callable(water) else water)
                if wl is None or (wl - g) / K > 0.05 or (wl - g) / K < -4.0:
                    pose = "watch"                          # round 5 (U36, PLAN §3 People): no drawn water within
                    FIG_FLAGS["fishing -> watch (no water at the edge)"] = FIG_FLAGS.get(   # reach, nobody fishes
                        "fishing -> watch (no water at the edge)", 0) + 1
                else:
                    q["water_dy"] = (wl - g) / K
            sh += fig_side(pose, cx, g, k, facing=fac, ink=ink, layer=layer, style=style, pick=seed + len(placed), **q)
        placed.append((pose, cx))
        last = pose
        if max_n and len(placed) >= max_n:
            break
        x += foot * K + (0.6 + 2.6 * (rnd() + 0.5)) / max(0.2, density) * K
    return sh, placed


# ---- G10 + G14 people by zone (R2-A 31 Oct 2026) ------------------------------------------------------------------
# People stand only where a zone is walkable; in the water only on a wading strip or stepping stones (U26: nobody in
# the stream for no reason); bikes only on bike lanes; every figure on the lowest ground under its feet (G14).
FIG_WALKABLE = ("walkway", "bike_lane", "viewing_terrace", "sun_steps", "market_ground", "bridge_crossing",
                "wading_strip", "stepping_stones", "lawn", "water_edge")
FIG_FOOT_HALF_M = 0.30       # m, half the ground a standing figure covers (drawing rule for G14 seating)
_FIG_NPICK = [0]
FIG_WADE_MAX_M = FIG_DC["knee"] * FIG_ADULT_H   # m: water at most knee deep where people wade (Aras 31 Oct: a
# person in a channel drawn full of water reads wrong); drawing rule from the figure's own proportions


def _fig_dry_runs(xa, xb, g, water, k, limit_m):
    """the parts of [xa, xb] where the water stands at most limit_m above the ground g (page y functions)"""
    n = max(2, int((xb - xa) / max(1e-6, 0.25 * k)))
    runs, a = [], None
    for i in range(n + 1):
        x = xa + (xb - xa) * i / float(n)
        w = water(x) if callable(water) else water
        ok = (w - g(x)) / k <= limit_m + 1e-6
        if ok and a is None:
            a = x
        if (not ok or i == n) and a is not None:
            b = x if ok else xa + (xb - xa) * (i - 1) / float(n)
            if b > a:
                runs.append((a, b))
            a = None
    return runs


def fig_place_zones(zones, gy, k, seed=0, layer=0, style="a", density=1.0, water=None, ink=None, max_per_zone=None,
                    focus=None, **p):
    """G10 people in a section, zone by zone: zones = [(kind, x0, x1)] or [(kind, x0, x1, ground)] left to right
    (page mm; ground = that zone's own walking surface: stone tops, a terrace deck, a bridge deck; else gy). kind =
    a FIG_ACTIVITY zone (walkway, bike_lane, viewing_terrace, sun_steps, market_ground, bridge_crossing,
    wading_strip, stepping_stones, lawn, water_edge (round 3: fishing at a dry bank edge; pass water), or an alias);
    any other kind (water, bed, planting, slope, wall ...) gets
    nobody and is counted in the G14 log line. Groups, adult with child, sitting, walking, trading, children
    playing by the zone's set; bikes only on bike lanes; wading figures take their depth from water (page y or
    function of x) on a wading strip only; cutout variants vary across the whole run (a running pick); every figure
    seated on the higher ground across its feet (sf_seat_feet, S3; sf_seat_x where absent). Pass water whenever a zone reaches the channel: nobody
    stands where the drawn water is deeper than FIG_WADE_MAX_M (knee) on a wading strip, or above the ground at all
    on any other zone (refused parts counted in the G14 log line as "<kind> (too deep)"). p goes to every figure
    (seat_h, rail_h ...). focus = page x everyone who stays looks at (R2-C scenes: the water; see fig_activity), or
    a function of (kind, x0, x1) -> page x or None per zone. Returns (shapes, placed [(kind, pose, x)])."""
    seat = globals().get("sf_seat_feet") or globals().get("sf_seat_x")   # round 5 (S3): the HIGHER ground across
                                                                          # the feet (S3 section_frame); old: lowest
    gfn = globals().get("_sf_fn")
    sc = fig_depth(layer)[0]
    sh, placed = [], []
    for i, z in enumerate(zones):
        kind, xa, xb = z[0], min(z[1], z[2]), max(z[1], z[2])
        kz = FIG_ZONE_ALIAS.get(kind, kind)
        if kz not in FIG_WALKABLE:
            rf = globals().get("SF_G14", {}).get("refused")
            if rf is not None:
                rf[kind] = rf.get(kind, 0) + 1
            continue
        g = z[3] if len(z) > 3 and z[3] is not None else gy
        g = gfn(g) if gfn else g
        gs = (lambda x, _g=g: seat(_g, x, FIG_FOOT_HALF_M * k * sc)) if seat else g
        acts = [a for a in FIG_ACTIVITY[kz] if a[0] != "bike" or kz == "bike_lane"]
        runs = [(xa, xb)]
        if water is not None:
            runs = _fig_dry_runs(xa, xb, g, water, k * sc, FIG_WADE_MAX_M if kz == "wading_strip" else 0.0)
            if sum(b - a for a, b in runs) < (xb - xa) - 0.3 * k * sc:
                rf = globals().get("SF_G14", {}).get("refused")
                if rf is not None:
                    rf[kind + " (too deep)"] = rf.get(kind + " (too deep)", 0) + 1
        fz = focus(kind, xa, xb) if callable(focus) else focus
        for ra, rb in runs:
            _FIG_NPICK[0] += 1
            s_, p_ = fig_activity(kz, ra, rb, gs, k, layer=layer, seed=seed * 101 + i * 17 + _FIG_NPICK[0] * 7,
                                  density=density, ink=ink, style=style,
                                  water=water if kz in ("wading_strip", "water_edge") else None, max_n=max_per_zone,
                                  acts=acts,
                                  focus=fz, **p)
            sh += s_
            placed += [(kind, pose, x) for pose, x in p_]
    return sh, placed


# ---- fauna (round 3 G15): only species sourced in research/fauna.md, drawn small where their habitat is. The file
# does not exist yet (31 Oct 2026): FIG_FAUNA stays empty, birds are generic silhouettes (section_frame.py sf_birds)
# and every page that draws them logs the FLAG below. Fill FIG_FAUNA {key: (habitat, source)} from the file later.
FIG_FAUNA = {}
FIG_FAUNA_DRAWN = [0]        # generic birds / animals drawn this run (sf_birds counts them)


def fig_flag_lines():
    """the figures' FLAG lines for a page log: ["FLAG fauna pending research"] while FIG_FAUNA is empty and any bird
    or animal was drawn"""
    out = [u"FLAG figures %s %d" % kv for kv in sorted(FIG_FLAGS.items())]     # round 5: refused scenes
    out += [ln for ln in FIG_LOG if ln.startswith(u"FLAG")]
    if FIG_FAUNA_DRAWN[0] and not FIG_FAUNA:
        out.append(u"FLAG fauna pending research (%d generic birds drawn; research/fauna.md missing)" % FIG_FAUNA_DRAWN[0])
    return out


# ---- speech bubbles (D4 a: p8 street sections, marked "illustrative scenario") -------------------------------------
FIG_BUBBLE_TAG = u"Illustrative scenario"


def fig_bubble(text, x, y, size=2.0, side=1, ink=None, fill="FFFFFF", lw=0.15, pad=None, tag=False, width_fn=None):
    """a speech bubble whose tail touches (x, y) (page mm, above a figure's head) and whose box sits above, to the
    right (side 1) or left (-1); text: lines split at "\\n", size = the font size in the page's text unit (mm on
    the common Page). width_fn(s, size) = the script's text width in page mm (default 0.52 x size per letter, Arial).
    tag: the "Illustrative scenario" line under the box (D4; once per drawing is enough). Returns shapes incl.
    ("text", s, x, y, size, colour, bold, align)."""
    import math as _m
    ink = ink or FIG_A1_INK
    lines = [ln for ln in u"{}".format(text).split(u"\n") if ln.strip()]
    wid = max((width_fn(ln, size) if width_fn else 0.52 * size * len(ln)) for ln in lines) if lines else size
    pad = 0.45 * size if pad is None else pad
    lh = 1.2 * size
    bw, bh = wid + 2 * pad, len(lines) * lh + 2 * pad - 0.2 * size
    bx0 = x + (0.4 * size if side >= 0 else -0.4 * size - bw)
    by0 = y + 1.2 * size
    r = min(0.6 * size, bh / 2.0)
    ring = []
    for cx_, cy_, a0 in ((bx0 + bw - r, by0 + r, -90), (bx0 + bw - r, by0 + bh - r, 0), (bx0 + r, by0 + bh - r, 90),
                         (bx0 + r, by0 + r, 180)):
        for i in range(7):
            a = _m.radians(a0 + 15 * i)
            ring.append((cx_ + r * _m.cos(a), cy_ + r * _m.sin(a)))
    tb = bx0 + (0.25 * bw if side >= 0 else 0.75 * bw)
    tail = [(tb - 0.35 * size, by0 + 0.05), (x, y), (tb + 0.35 * size, by0 + 0.05)]
    sh = [("poly", ring, fill, ink, lw), ("poly", tail, fill, None, 0.1), ("line", tail, ink, lw)]
    for i, ln in enumerate(lines):
        sh.append(("text", ln, bx0 + pad, by0 + bh - pad - (i + 0.8) * lh + 0.2 * size, size, ink, False, "L"))
    if tag:
        sh += fig_bubble_tag(bx0, by0 - 0.9 * size, 0.75 * size, ink)
    return sh


def fig_bubble_tag(x, y, size=1.6, ink=None):
    """the D4 mark "Illustrative scenario" as a text shape at (x, y) (page mm, left aligned)"""
    return [("text", FIG_BUBBLE_TAG, x, y, size, ink or FIG_A1_INK, False, "L")]


# ---- scale assertion (G6, against M8's unit: k = page mm per m) ----------------------------------------------------
def _fig_top_y(rings):
    return max(py for r in rings for _px, py in r), min(py for r in rings for _px, py in r)


def fig_check_scale(k, layer=0, tol=0.04):
    """asserts that an adult prints FIG_ADULT_H x k x layer scale tall (drawn stand pose), a cyclist FIG_CYCLIST_H and a child FIG_CHILD_H (same tolerance). Returns {name: page mm}.
    AssertionError naming the figure otherwise."""
    sc = fig_depth(layer)[0]
    out = {}
    drawn = [[(px * k * sc, py * k * sc) for px, py in r] for r in _fa_side("stand", 0)[0]]
    bike = [[(px * k * sc, py * k * sc) for px, py in r] for r in _fa_side("bike", 0)[0]]
    child = [[(px * k * sc, py * k * sc) for px, py in r] for r in _fa_side("child_play", 0)[0]]
    items = [("adult (drawn)", drawn, FIG_ADULT_H, True), ("cyclist", bike, FIG_CYCLIST_H, True),
             ("child", child, FIG_CHILD_H, False)]
    for name, rings, h, top_only in items:
        hi, lo = _fig_top_y(rings)
        got = hi if top_only else hi - lo
        want = h * k * sc
        out[name] = got
        if name == "child":                            # a hopping child: its top is below its stature
            if not (0.80 * want <= got <= (1.0 + tol) * want):
                raise AssertionError("G6 scale: %s prints %.2f mm, expected about %.2f mm (k %.3f, layer %s)"
                                     % (name, got, want, k, layer))
            continue
        if abs(got - want) > tol * want:
            raise AssertionError("G6 scale: %s prints %.2f mm, expected %.2f mm (%.2f m x k %.3f x %.2f, layer %s)"
                                 % (name, got, want, h, k, sc, layer))
    return out

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
# M3 (revision 30 Oct 2026, H-A): the 29 Oct modes and switches are kept as they were; added the layers study_area
# (calisma_alan, ONE outline reused on every map, R28_STUDY_LINE), names (place names) and the building styles "plan" /
# "plan_faint" (M11: block outlines + roof reading, no stripes), the modes "base" (the faint base of a map page) and
# "key" (key maps, M4), the water drawn by M5 (water_plan, when included) and keymap_items (M4). The data carries per
# building its height (h, floors) and a "blocks" layer (buildings sharing a wall merged: no fake division lines).
import os as _bm_os
import json as _bm_json
import math as _bm_math

BASEMAP_FILE = _bm_os.path.join(_bm_os.path.expanduser("~"), "Downloads", "Bergama", "cached", "basemap",
                                "basemap.json")
BASEMAP_FORMAT = 2               # round 5 (S2): 2 = buildings carry "fabric" and "annex", land cover adds grass / shrub
BASEMAP_FORMATS_READ = (1, 2)    # a format 1 file (written before round 5) still reads: key maps then draw one house
#                                  tone and log a FLAG until the site board has written format 2
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
# round 4 (S2, G-R4-4, PLAN §4.3): the MUTED base under every map page: light houses with a closed block outline,
# light streets with their edges, every outline after every fill (CHK-3 §1.5-1.6); heritage a pale rose.
BM_MUTED = dict(bld="EDEBE6", bld_edge="C9C5BC", her="F1E6E5", her_edge="CDAAAA", road="F4F2EE", road_edge="CFCBC2",
                name="9A948A", lw=0.12)
# round 5 (S2, G-R5-3, D3, U69 "just draw it like page 2"): the key-map look = the p02 map (site board plan 01) at
# small scale. BM_FABRIC is the site board's FABRIC_PLAN (selinus_board/parts/14_tsec_wind_arrows.py v40) moved to
# common as hex (the site board keeps its own name for it until its round 5 pass reads this table). BM_KEY: the p02
# ground tones (site board parts/01__gh_inputs.py CAT, GREEN_SUB, TREE_COLS, PAPER, BLUE_D; parts/17_board_fits.py
# LC_CLASSES), lightened toward the paper by "light" (greens) and "fabric_light" (houses, = p02 P02_IN_LIGHT 0.40)
# so the red cut symbols lead; design values.
BM_FABRIC = {"monument": "AF7474", "sacred": "8B3A3F", "traditional": "4A3F35", "block": "7A6E60",
             "regular": "BCB794", "selfbuilt": "DCD5C2", "large": "FAF8F1", "construction": "E6E0C8"}
BM_KEY = dict(paper="F1EDDF", grass="ABB287", shrub=("8F9A68", "F1EDDF", 0.3), trees="74804F", farmland="BDB57A",
              orchard=("98A271", "4A3F35", 0.12), park="8F9A68", wood="74804F", agri="BDB57A", water="7FA4B3",
              water_edge="5E8494", road="FAF8F1", road_line="DCD5C2", bridge="4A3F35", light=0.35, fabric_light=0.40,
              annex=0.45, lw=0.12)


def _bm_mix(a, b, t):
    """hex a mixed t of the way toward hex b (the site board's mix on hex)"""
    return "".join("%02X" % int(round(int(a[j:j + 2], 16) + (int(b[j:j + 2], 16) - int(a[j:j + 2], 16)) * t))
                   for j in (0, 2, 4))


def bm_key_col(name, light=None):
    """round 5 (S2): a BM_KEY tone as hex ('shrub' / 'orchard' are mixes), mixed light (default BM_KEY['light'] for
    ground tones, none for paper / water / road / bridge) toward the paper"""
    v = BM_KEY[name]
    c = _bm_mix(*v) if isinstance(v, tuple) else v
    if light is None:
        light = 0.0 if name in ("paper", "water", "water_edge", "road", "road_line", "bridge") else BM_KEY["light"]
    return _bm_mix(c, BM_KEY["paper"], light) if light else c


def bm_fabric_col(b, light=None):
    """round 5 (S2): a basemap building's key-map colour by its urban fabric (format 2 "fabric"; "regular" when the
    file has none), annexes paler (the p02 rule), mixed BM_KEY['fabric_light'] toward the paper"""
    c = BM_FABRIC.get(b.get("fabric") or "regular", BM_FABRIC["regular"])
    if b.get("annex"):
        c = _bm_mix(c, BM_KEY["paper"], BM_KEY["annex"])
    return _bm_mix(c, BM_KEY["paper"], BM_KEY["fabric_light"] if light is None else light)


class _BmIt(tuple):
    """round 5 (S2, G-R5-8): a basemap item that knows its map layer (.layer, a map_layers ML_LAYERS name): reads as
    the plain tuple everywhere; map_draw files a flat base list by it, so the stream is drawn above every tint"""
    pass


def _bm_tag(t, layer):
    o = _BmIt(t)
    o.layer = layer
    return o


# contours coloured to the relief (G-R4-4, U48): green tones, lighter = lower (palette 3C4733 and its 89986A tints)
BM_HEIGHT_RAMP = ("C9D6B0", "A7B68C", "89986A", "3C4733")
BM_LW = dict(contour=(0.07, 0.13), contour_topo=(0.08, 0.14), water_edge=0.18, covered=0.30, bridge=0.30,
             road_edge=0.12, osm_edge=0.08, her_edge=0.12, main=0.45, lane=0.22, path=0.10, river_osm=0.6,
             stream_osm=0.35, cut=0.35)
BM_COVERED_DASH = (1.6, 0.9)     # mm: the covered course

# the modes of 02 §1; a value per layer: False = off, True = on, "faint" / "veryfaint" = buildings or streets faint,
# a tuple of street classes ("main", "lane", "path") = only those as centrelines, "height" = contours by height
BASEMAP_MODES = {
    "detailed": dict(stream=True, streets=True, buildings=True, green=True, trees=True, fields=True, contours=True,
                     study_area=False, names=False),
    "simple": dict(stream=True, streets="faint", buildings="faint", green=False, trees=False, fields=False,
                   contours=False, study_area=False, names=False),
    "minimal": dict(stream=True, streets=("main", "lane"), buildings="veryfaint", green=False, trees=False,
                    fields=False, contours=False, study_area=False, names=False),
    "topographic": dict(stream=True, streets=False, buildings="faint", green=False, trees=False, fields=False,
                        contours="height", study_area=False, names=False),
    # M3 (30 Oct): the faint base under a map page's message (G5), and the key map's base (M4)
    "base": dict(stream=True, streets="faint", buildings="plan_faint", green=False, trees=False, fields=False,
                 contours=False, study_area=True, names=False),
    "key": dict(stream=True, streets=("main",), buildings="veryfaint", green=False, trees=False, fields=False,
                contours=False, study_area=True, names=False),
    # round 4 (S2, G-R4-4): the muted base of map_layers.ml_base; the study line is drawn by map_draw in its own
    # layer (above the project fills), so it is off here; contours are switched on by the call ("height")
    "muted": dict(stream=True, streets="muted", buildings="muted", green=False, trees=False, fields=False,
                  contours=False, study_area=False, names=False),
    # round 5 (S2, G-R5-3): the key map = the p02 look at small scale: land cover and green ground, houses by urban
    # fabric (fills only, no outlines at key-map scales), the stream blue (a flat fill: legible at 1:50,000+), light
    # street areas, bridges; the study line and names are the key map's own
    "keymap": dict(stream=True, streets="key", buildings="fabric", green=True, trees=True, fields=True,
                   contours=False, study_area=False, names=False),
}
# M3 layer list -> switches: basemap_layers accepts these names too (buildings, streets, water, topography,
# study_area, names; green, trees, fields as before)
BM_LAYER_ALIAS = dict(water="stream", topography="contours")
# round 4 (S2, G-R4-4, U18/U19): ONE study-area line everywhere: violet long-dash-dot, its own hue (never ink, grey
# or a road colour); r28_style.py R28_STUDY_LINE holds the same values (either file may be included first)
BM_STUDY_LINE = dict(colour="6A4C93", width_mm=0.35, dash_mm=(3.0, 0.8, 0.6, 0.8))
BM_NAME_MM = 2.47                  # place names: the M1 label size (7 pt)
_BM_MEMO = {}
_BM_WARN = []


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
        if not isinstance(d, dict) or d.get("format") not in BASEMAP_FORMATS_READ:
            if log is not None:
                log.append(u"WARNING: {} is of another format: the shared basemap is left out (run the site board "
                           u"once).".format(p))
            d = None
        elif log is not None:
            log.append(u"Shared basemap: {} ({}).".format(p, d.get("source", "")))
            if d.get("format") != BASEMAP_FORMAT:
                log.append(u"FLAG basemap format {} (no urban fabric per house): key maps draw one house tone until "
                           u"the site board writes format {}.".format(d.get("format"), BASEMAP_FORMAT))
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
    basemap_layers("minimal", {"streets": ("main",), "buildings": False}) for D5 Sound b (stream + main roads).
    M3 (30 Oct): override may also be a LIST of layer names = only those on (the others off), each at the mode's
    own value, e.g. basemap_layers("base", ["buildings", "water", "study_area"]); "water" = stream, "topography" =
    contours. buildings: True / "faint" / "veryfaint" / "plan" / "plan_faint" (M11) / False."""
    if mode not in BASEMAP_MODES:
        raise ValueError(u"basemap mode '{}' unknown: one of {}".format(mode, ", ".join(sorted(BASEMAP_MODES))))
    lay = dict(BASEMAP_MODES[mode])
    if isinstance(override, (list, tuple, set, frozenset)):
        want = set(BM_LAYER_ALIAS.get(k, k) for k in override)
        for k in want:
            if k not in lay:
                raise ValueError(u"basemap layer '{}' unknown: one of {}".format(k, ", ".join(sorted(lay))))
        on = dict(BASEMAP_MODES["detailed"], study_area=True, names=True)
        override = dict((k, (lay[k] or on[k]) if k in want else False) for k in lay)
    for k, v in (override or {}).items():
        k = BM_LAYER_ALIAS.get(k, k)
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


def basemap_items(mode="detailed", override=None, box=None, D=None, split_buildings=False, scale_den=None):
    """the basemap of a drawing as items (bottom first; see the head of this file), in survey m. mode: "detailed",
    "simple", "minimal", "topographic" (02 §1), "base", "key" (M3, 30 Oct); override: layer changes for this drawing,
    a dict or a list of the layers to show (basemap_layers); box = (x0, y0, x1, y1) survey m: only what touches it
    (the caller clips to its frame); split_buildings=True gives every building its own fill item (for a page that
    fills even-odd only; default: nonzero fills in chunks); scale_den: the drawing's scale (1:scale_den) for the
    M11 roof marks of buildings "plan" / "plan_faint" (default 1:5,000). [] without data."""
    D = D if D is not None else basemap_load()
    if not D:
        return []
    # the same request in one run is made once and copied (Aras 29 Oct 19:18: build once, cache, copy the layers)
    ov = sorted(override) if isinstance(override, (list, tuple, set, frozenset)) else sorted((override or {}).items())
    mk = ("items", id(D), mode, repr(ov), tuple(box) if box else None, bool(split_buildings), scale_den)
    if mk in _BM_MEMO:
        return list(_BM_MEMO[mk])
    _BM_MEMO[mk] = _bm_items(D, mode, override, box, split_buildings, scale_den)
    return list(_BM_MEMO[mk])


def basemap_water_rings(items):
    """M3: the stream's rings (survey m) in an item list, whether drawn plain (fill items of the water colour) or by
    M5 (the "water" item): for a page that clips or measures by the water"""
    out = []
    for it in items:
        if it[0] == "water":
            out += [R for g in it[1] for R in g if len(R) >= 3]
        elif it[0] == "fill" and it[2] == BM_COL["water"]:
            out += [R for R in it[1] if len(R) >= 3]
    return out


def basemap_warnings():
    """M3: what the basemap could not draw as asked this run (e.g. the M5 water drawing failed): log lines, emptied"""
    out = list(_BM_WARN)
    del _BM_WARN[:]
    return out


def basemap_study(D=None):
    """M3: the study area (calisma_alan, two closed parts worked as one) as rings in survey m: the basemap's study
    layer, else the recorded copy a script includes (R28_STUDY_COPY, CALISMA_COPY, CL_STUDY); [] without either"""
    D = D if D is not None else basemap_load()
    st = ((D or {}).get("layers") or {}).get("study")
    if st:
        return [[tuple(p) for p in R] for R in st]
    for nm in ("R28_STUDY_COPY", "CALISMA_COPY", "CL_STUDY"):
        v = globals().get(nm)
        if v:
            return [[tuple(p) for p in R] for R in v]
    return []


def basemap_study_items(D=None, style=None):
    """M3: the study-area outline as line items (survey m), one style everywhere (R28_STUDY_LINE when included)"""
    st = style or globals().get("R28_STUDY_LINE") or BM_STUDY_LINE
    return [("line", list(R) + [R[0]], st["colour"], st["width_mm"], list(st["dash_mm"]), 1.0)
            for R in basemap_study(D) if len(R) >= 3]


def basemap_names(box=None, D=None):
    """M3: the place names [(name, (x, y))] in survey m (the extent's landmarks and named heritage buildings), for a
    page to place with M2 (lp_place) so no name collides"""
    D = D if D is not None else basemap_load()
    if not D:
        return []
    nm = (D.get("layers") or {}).get("names") or [[n, list(p)] for n, p in (D.get("reach") or BASEMAP_REACH)]
    out = []
    for n, p in nm:
        if box is None or (box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3]):
            out.append((n, (p[0], p[1])))
    return out


def basemap_street_names(box=None, D=None, classes=("main",), min_len_m=0.0):
    """round 4 (S2, G-R4-9 U55): the street names of OpenStreetMap's `name` tags (Turkish as mapped), one per name
    at the middle of its longest run: [(name, (x, y), angle_deg, class, run_m)] in survey m, longest first; classes
    = the street classes kept ("main", "lane"); [] when the basemap file predates round 4 (run the site board)"""
    D = D if D is not None else basemap_load()
    out = []
    for n, p, a, cl, ln in ((D or {}).get("layers") or {}).get("street_names") or []:
        if cl in classes and ln >= min_len_m and (box is None or (box[0] <= p[0] <= box[2] and box[1] <= p[1] <= box[3])):
            out.append((n, (p[0], p[1]), a, cl, ln))
    out.sort(key=lambda r: -r[4])
    return out


def _bm_items(D, mode, override, box, split_buildings, scale_den=None):
    """basemap_items without the memo"""
    lay = basemap_layers(mode, override)
    L = D["layers"]
    out = []
    outl = []          # round 4 (S2, CHK-3 §1.6): outlines (street, building, bridge edges) come after EVERY fill
    # round 5 (S2, G-R5-8): every item carries its map layer (_BmIt.layer): ground, houses and streets "base_fills",
    # contours "base_contours", outlines "base_outlines", the stream "water", decks / covered course / bridges
    # "structures" (map_draw draws "water" above every project tint, then "structures")

    def fills(groups, col, alpha=1.0, nonzero=True, chunk=300, layer="base_fills"):
        cur = []
        for g in groups:
            g = [R for R in g if len(R) >= 3]
            if not g or not _bm_hit(g[0], box):
                continue
            if split_buildings:
                out.append(_bm_tag(("fill", g, col, alpha, nonzero), layer))
                continue
            cur.extend(g)
            if len(cur) >= chunk:
                out.append(_bm_tag(("fill", cur, col, alpha, nonzero), layer))
                cur = []
        if cur:
            out.append(_bm_tag(("fill", cur, col, alpha, nonzero), layer))

    def lines(Ps, col, w, dash=None, alpha=1.0, outline=False, layer=None):
        for P in Ps:
            if len(P) >= 2 and _bm_hit(P, box):
                (outl if outline else out).append(_bm_tag(("line", P, col, w, list(dash) if dash else None, alpha),
                                                          layer or ("base_outlines" if outline else "base_fills")))
    key = mode == "keymap"

    # ground: tree cover, fields, parks / grass (satellite first, mapped areas over it)
    if key:                                               # round 5 (S2, G-R5-3): the p02 ground (draw_landuse_map
        if lay["green"]:                                  # order: satellite classes, then mapped zones)
            fills(L["lc"].get("grass", []), bm_key_col("grass"))
            fills(L["lc"].get("shrub", []), bm_key_col("shrub"))
        if lay["trees"]:
            fills(L["lc"].get("trees", []), bm_key_col("trees"))
        if lay["fields"]:
            fills(L["lc"].get("farmland", []), bm_key_col("farmland"))
            fills(L["lc"].get("orchard", []), bm_key_col("orchard"))
            fills([z["rings"] for z in L["zones"] if z["kind"] == "agri"], bm_key_col("agri"))
        if lay["green"]:
            fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") == "grass"],
                  bm_key_col("grass"))
            fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") not in ("grass", "wood")],
                  bm_key_col("park"))
        if lay["trees"]:
            fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") == "wood"],
                  bm_key_col("wood"))
    if not key and lay["trees"]:
        fills(L["lc"].get("trees", []), BM_COL["tree"])
    if not key and lay["fields"]:
        fills(L["lc"].get("farmland", []) + L["lc"].get("orchard", []), BM_COL["field"])
        fills([z["rings"] for z in L["zones"] if z["kind"] == "agri"], BM_COL["field"])
    if not key and lay["green"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") != "wood"], BM_COL["park"])
    if not key and lay["trees"]:
        fills([z["rings"] for z in L["zones"] if z["kind"] == "green" and z.get("sub") == "wood"], BM_COL["tree"])
    # contours
    if lay["contours"]:
        cs = L["contours"]
        if lay["contours"] == "height":
            zs = [c[1] for c in cs if c[1] is not None]
            z0, z1 = (min(zs), max(zs)) if zs else (0.0, 1.0)
            for major, z, P in cs:
                col = _bm_ramp((z - z0) / max(1.0, z1 - z0)) if z is not None else BM_COL["contour"]
                lines([P], col, BM_LW["contour_topo"][1 if major else 0], layer="base_contours")
        else:
            for major, z, P in cs:
                lines([P], BM_COL["contour"], BM_LW["contour"][1 if major else 0], layer="base_contours")
    # streets
    st = lay["streets"]
    if st == "key":                                       # round 5 (S2): light street areas, no edges; main roads
        fills(L["street_areas"], bm_key_col("road"), nonzero=False)       # beyond the frame as light centrelines
        for cl, P in L["streets_out"]:
            if cl == "main":
                lines([P], bm_key_col("road_line"), BM_LW["main"])
    elif st == "muted":                                     # round 4 (S2): light fill, light closed edges, after fills
        fills(L["street_areas"], BM_MUTED["road"], nonzero=False)
        for cl, P in L["streets_out"]:
            lines([P], BM_MUTED["road_edge"], BM_LW[cl] * (1.6 if cl != "path" else 1.0))
        for g in L["street_areas"]:                       # every ring of a street area closed (no open survey run)
            lines([list(R) + [R[0]] for R in g if len(R) >= 3], BM_MUTED["road_edge"], BM_MUTED["lw"], outline=True)
    elif st is True or st == "faint":
        faint = st == "faint"
        fills(L["street_areas"], BM_FAINT["road"] if faint else BM_COL["road"], nonzero=False)
        for cl, P in L["streets_out"]:                    # beyond the frame: OpenStreetMap centrelines
            lines([P], BM_FAINT["road_line"] if faint else BM_COL["road"], BM_LW[cl] * (1.6 if cl != "path" else 1.0))
        if faint:                                         # round 4 (S2, CHK-3 §1.6): faint modes keep their edges
            for g in L["street_areas"]:
                lines([list(R) + [R[0]] for R in g if len(R) >= 3], BM_FAINT["road_line"], 0.08, outline=True)
        else:
            lines(L["street_edges"], BM_COL["road_edge"], BM_LW["road_edge"], outline=True)
    elif st:
        for cl, P in L["streets_in"] + L["streets_out"]:
            if cl in st:
                lines([P], BM_FAINT["road_line"] if cl != "main" else BM_COL["road_edge"], BM_LW[cl])
    # the stream: ONE drawing (the site board's water and its edge inside the frame, OpenStreetMap's course beyond).
    # M3 (30 Oct): drawn by M5 (common/water.py water_plan, page mm) when the script includes it: one "water" item
    # that basemap_draw hands to water_plan after the map's T (else the plain fill and edge, as before)
    if lay["stream"]:
        wc, we = (bm_key_col("water"), bm_key_col("water_edge")) if key else (BM_COL["water"], BM_COL["water_edge"])
        if callable(globals().get("water_plan")) and not key:
            ws = [g for g in L["water"] if g and len(g[0]) >= 3 and _bm_hit(g[0], box)]
            if ws:
                out.append(_bm_tag(("water", ws, [P for P in L["water_edge"] if len(P) >= 2 and _bm_hit(P, box)],
                                    1.0), "water"))
        else:
            fills(L["water"], wc, nonzero=False, layer="water")
            lines(L["water_edge"], we, BM_LW["water_edge"], layer="water")
        if st is True or st in ("faint", "muted", "key"):
            fills([[R] for R in L["decks"]], BM_MUTED["road"] if st == "muted" else
                  (BM_FAINT["road"] if st == "faint" else (bm_key_col("road") if st == "key" else BM_COL["road"])),
                  layer="structures")
        for P in L["covered"]:
            lines([P], we, BM_LW["covered"], BM_COVERED_DASH, outline=True, layer="structures")
        fills(L["water_out"], wc, nonzero=False, layer="water")
        for kind, P in L["waterways_out"]:
            lines([P], wc, BM_LW["river_osm" if kind == "river" else "stream_osm"], layer="water")
    # buildings
    bl = lay["buildings"]
    if bl == "fabric":                                    # round 5 (S2, G-R5-3): houses by urban fabric, fills only
        groups = {}
        for b in L["buildings"]:
            groups.setdefault(bm_fabric_col(b), []).append(b["rings"][:b.get("np", len(b["rings"]))])
        for col in sorted(groups):
            fills(groups[col], col)
    elif bl == "muted" and not callable(globals().get("bld_plan_items")):
        _BM_WARN.append(u"WARNING: basemap buildings 'muted' need common/buildings.py (M11): drawn as plain light "
                        u"fills with their outlines instead.")
        fills([b["rings"] for b in L["buildings"]], BM_MUTED["bld"])
        for bk in L.get("blocks") or []:
            lines([list(R) + [R[0]] for R in bk["rings"] if len(R) >= 3], BM_MUTED["bld_edge"], BM_MUTED["lw"],
                  outline=True)
    elif bl == "muted":                                   # round 4 (S2, G-R4-4): light houses, ONE closed outline per
        for it in bld_plan_items(L["buildings"], blocks=L.get("blocks"), scale_den=scale_den or 5000.0, box=box,
                                 roof="none", fill=BM_MUTED["bld"], edge=BM_MUTED["bld_edge"],   # block, no roof marks
                                 her_fill=BM_MUTED["her"], her_edge=BM_MUTED["her_edge"], lw=BM_MUTED["lw"]):
            (outl if it[0] == "line" else out).append(_bm_tag(it, "base_outlines" if it[0] == "line" else
                                                              "base_fills"))
    elif bl in ("plan", "plan_faint"):                      # M11: outline per block + roof reading, no stripes
        pf = globals().get("bld_plan_items")
        if callable(pf):
            faint = bl == "plan_faint"
            blocks = L.get("blocks")
            for it in pf(L["buildings"], blocks=blocks, scale_den=scale_den or 5000.0, box=box,
                         fill=BM_FAINT["bld_veryfaint"] if faint else None,
                         edge=BM_FAINT["road_line"] if faint else None,
                         roof_col=BM_FAINT["bld"] if faint else None,
                         her_fill=BM_COL["her"] if not faint else "F1E6E5",
                         her_edge=BM_COL["her_edge"] if not faint else "CDAAAA"):
                (outl if it[0] == "line" else out).append(_bm_tag(it, "base_outlines" if it[0] == "line" else
                                                                  "base_fills"))   # roof marks, outlines after fills
        else:
            _BM_WARN.append(u"WARNING: basemap buildings '{}' need common/buildings.py (M11): drawn faint "
                            u"instead.".format(bl))
            fills([b["rings"] for b in L["buildings"]], BM_FAINT["bld"])
    elif bl:
        if bl is True:
            fills([b["rings"] for b in L["buildings"] if not b.get("her")], BM_COL["bld"])
            fills([b["rings"] for b in L["buildings"] if b.get("her")], BM_COL["her"])
            for b in L["buildings"]:
                if b.get("her") or b.get("osm"):
                    lines([R + R[:1] for R in b["rings"][:b.get("np", len(b["rings"]))]],
                          BM_COL["her_edge"] if b.get("her") else BM_COL["bld_osm_edge"],
                          BM_LW["her_edge"] if b.get("her") else BM_LW["osm_edge"], outline=True)
            for bk in L.get("blocks") or []:                # round 4 (S2, CHK-3 §1.5): survey houses get their edge too
                if not bk.get("her"):
                    lines([list(R) + [R[0]] for R in bk["rings"] if len(R) >= 3], BM_COL["bld_osm_edge"],
                          BM_LW["osm_edge"], outline=True)
        else:
            fills([b["rings"] for b in L["buildings"]],
                  BM_FAINT["bld_veryfaint"] if bl == "veryfaint" else BM_FAINT["bld"])
    if lay["stream"] and key:                             # round 5 (S2): bridges over the blue stream (p02 order 18)
        lines(L["bridges"], bm_key_col("bridge"), BM_LW["bridge"], outline=True, layer="structures")
    elif lay["stream"] and (st is True or bl is True or bl == "plan"):
        lines(L["bridges"], BM_COL["ink"], BM_LW["bridge"], outline=True, layer="structures")
    elif lay["stream"] and bl == "muted":                 # round 4: bridges in the muted edge tone, a little heavier
        lines(L["bridges"], BM_MUTED["bld_edge"], 2.0 * BM_MUTED["lw"], outline=True, layer="structures")
    out.extend(outl)                                      # round 4 (S2): every outline after every fill
    # M3 (30 Oct): the study area (one outline, one style, on top of the base) and the place names
    if lay.get("study_area"):
        for it in basemap_study_items(D):
            if _bm_hit(it[1], box):
                out.append(_bm_tag(it, "base_outlines"))
    if lay.get("names"):
        for n, p in basemap_names(box, D):
            out.append(_bm_tag(("text", n, p, BM_NAME_MM, BM_MUTED["name"] if mode == "muted" else BM_COL["ink"],
                                False, "MC"), "base_names"))
    return out


def basemap_draw(items, T, fill_fn, line_fn, text_fn=None, water_opts=None):
    """draws items through the caller's page: T(p) survey m -> page point; fill_fn(rings, hex, alpha, nonzero);
    line_fn(pts, hex, width_mm, dash_mm, alpha); text_fn(s, (x, y), size_mm, hex, bold, align) (texts are left out
    without it). Returns the number of items drawn. M3 (30 Oct): a "water" item (the stream, when the script includes
    M5 common/water.py) is drawn by water_plan(ring in page mm, k, holes=its islands, **water_opts) through the same
    three functions (k = page mm per survey m, from T); if M5 fails, the plain fill and bank line (a WARNING in
    basemap_warnings())."""
    import math as _m
    n = 0
    for it in items:
        if it[0] == "fill":
            fill_fn([[T(p) for p in R] for R in it[1]], it[2], it[3], it[4])
        elif it[0] == "line":
            line_fn([T(p) for p in it[1]], it[2], it[3], it[4], it[5])
        elif it[0] == "text" and text_fn is not None:
            text_fn(it[1], T(it[2]), it[3], it[4], it[5], it[6])
        elif it[0] == "water":
            p0 = it[1][0][0][0][0], it[1][0][0][0][1]          # first point of the first ring of the first group
            a, b = T(p0), T((p0[0] + 100.0, p0[1]))
            k = _m.hypot(b[0] - a[0], b[1] - a[1]) / 100.0
            try:
                wp = globals()["water_plan"]                # M5 (common/water.py), present: _bm_items checked it
                for g in it[1]:
                    hs = [[T(p) for p in R] for R in g[1:] if len(R) >= 3]     # islands: open, untextured (A2 fix)
                    wl = wp([T(p) for p in g[0]], k, holes=hs, **(water_opts or {}))
                    for s_ in wl.shapes():
                        if s_[0] == "poly" and len(s_[1]) >= 3:
                            al = s_[5] if len(s_) > 5 and s_[5] is not None else 1.0
                            ho = [list(R) for R in (s_[6] if len(s_) > 6 and s_[6] else ())]
                            if s_[2]:
                                fill_fn([list(s_[1])] + ho, s_[2], al, not ho)          # even-odd with holes
                            if s_[3]:
                                line_fn(list(s_[1]) + [s_[1][0]], s_[3], s_[4] or 0.1, None, al)
                        elif s_[0] == "line" and len(s_[1]) >= 2:
                            line_fn(list(s_[1]), s_[2], s_[3], s_[4] if len(s_) > 4 else None, 1.0)
                        elif s_[0] == "text" and text_fn is not None:
                            text_fn(s_[1], (s_[2], s_[3]), s_[4], s_[5], s_[6] if len(s_) > 6 else False,
                                    s_[7] if len(s_) > 7 else "L")
            except Exception as ex_:
                _BM_WARN.append(u"WARNING: basemap: the M5 water drawing failed ({}: {}); the stream is drawn as the "
                                u"base map's own fill.".format(type(ex_).__name__, ex_))
                fill_fn([[T(p) for p in R] for g in it[1] for R in g], BM_COL["water"], 1.0, False)
                for P in it[2]:
                    line_fn([T(p) for p in P], BM_COL["water_edge"], BM_LW["water_edge"], None, 1.0)
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


# M4 key map: keymap_items and basemap_cut_items moved to keymap.py (round 4 S2: R01 red symbol, names, muted base)


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

        def in_frame_name(u):
            u_, v_ = loc((u["cx"], u["cy"]))
            return fr[0] <= u_ <= fr[2] and fr[1] <= v_ <= fr[3]

        def in_ring(p):
            u, v = loc(p)
            return ex[0] <= u <= ex[2] and ex[1] <= v <= ex[3] and not (fr[0] <= u <= fr[2] and fr[1] <= v <= fr[3])
        L = dict(lc={}, zones=[], contours=[], street_areas=[], street_edges=[], streets_in=[], streets_out=[],
                 water=[], water_edge=[], decks=[], covered=[], water_out=[], waterways_out=[], buildings=[],
                 bridges=[], blocks=[], study=[], names=[], street_names=[])
        sn_best = {}                                      # round 4 (S2, G-R4-9 U55): street name -> longest run
        unnamed = []                                      # round 5 (S2, A11): survey names with no names-table row

        def street_name(tags, P, cl):
            nm_ = ((tags or {}).get("name") or u"").strip()
            if not nm_ or cl == "path" or len(P) < 2:
                return
            Ln = sum(_bm_math.hypot(b_[0] - a_[0], b_[1] - a_[1]) for a_, b_ in zip(P, P[1:]))
            if nm_ not in sn_best or Ln > sn_best[nm_][0]:
                sn_best[nm_] = (Ln, cl, P)
        mains = set(globals().get("MAIN_ROADS") or ("motorway", "trunk", "primary", "secondary", "tertiary"))
        peds = set(globals().get("PED") or ("footway", "path", "pedestrian", "steps", "cycleway", "bridleway",
                                             "track", "corridor"))
        skip = set(globals().get("SKIP_HW") or ("proposed", "construction", "platform", "bus_stop", "elevator"))
        ccls = lambda hw: "path" if hw in peds else ("main" if hw in mains else "lane")
        # ---- inside the frame: the site board's layers
        lcf = globals().get("r28e_lc")
        for key in ("trees", "farmland", "orchard", "grass", "shrub"):       # round 5 (S2): grass, shrub for key maps
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
                    z = round(zs[len(zs) // 2], 1)     # round 3 (B2, P11.1 relief): median to 0.1 m (was 5 m steps)
                except Exception:
                    z = None
            L["contours"].append([bool(major), z, _bm_r(P)])
        for rg in getattr(S, "road_net", None) or []:
            L["street_areas"].append([_bm_r(rg["P"])] + [_bm_r(H) for H in rg.get("H", [])])
        L["street_edges"] = [_bm_r(P) for P in getattr(S, "road_lines_net", None) or []] + \
            [_bm_r(r_["P"]) for r_ in S.roads if not r_.get("w")]
        L["streets_in"] = [[ccls((r_.get("tags") or {}).get("highway")), _bm_r(r_["P"])] for r_ in S.roads] + \
            [["path", _bm_r(r_["P"])] for r_ in getattr(S, "paths", None) or []]
        for r_ in S.roads:
            street_name(r_.get("tags"), r_["P"], ccls((r_.get("tags") or {}).get("highway")))
        L["water"] = [[_bm_r(wt["P"])] + [_bm_r(H) for H in wt.get("H", [])] for wt in S.water]
        L["water_edge"] = [_bm_r(P) for P in getattr(S, "water_outline", None) or []]
        L["decks"] = [_bm_r(P) for P in getattr(S, "decks", None) or []]
        L["covered"] = [_bm_r(P) for P in getattr(S, "covered", None) or []]
        L["bridges"] = [_bm_r(P) for P in getattr(S, "bridges", None) or []]
        # buildings: one outline per building (build_site merged its pieces: revision 30 Oct, G7) with its height,
        # and the blocks (buildings sharing a wall as ONE outline, S.blocks): the plan's outline layer, so no party
        # wall, survey tick or label split is ever drawn as a line
        idx_of = {}
        for i_u, u in enumerate(S.bld):
            parts = [_bm_r(P) for P in u["parts"] if len(P) >= 3]
            if parts:
                idx_of[i_u] = len(L["buildings"])
                tg = u.get("tags") or {}
                her = u.get("fabric") in ("monument", "sacred") or bool(tg.get("historic")) or \
                    tg.get("amenity") == "place_of_worship"
                L["buildings"].append(dict(rings=parts + [_bm_r(H) for H in (u.get("holes") or [])], np=len(parts),
                                           her=her, osm=u.get("src") in ("osm", "osm+label"),
                                           h=round(float(u.get("h") or 0.0), 2), floors=int(u.get("floors") or 0),
                                           fabric=u.get("fabric") or "regular", annex=bool(u.get("annex"))))
                if her and (u.get("name") or "").strip() and in_frame_name(u):
                    # round 5 (S2, A11): only names the names table records, in its one spelling (place_label);
                    # a survey name with no table row is left out and listed (never print an unchecked name)
                    pl = globals().get("place_label")
                    raw, pc = u["name"].strip(), (u["cx"], u["cy"])
                    nm_ = pl(raw, pc) if callable(pl) else None
                    if nm_ and nm_ not in [n_ for n_, _ in L["names"]]:
                        L["names"].append([nm_, [round(u["cx"], 1), round(u["cy"], 1)]])
                    elif not nm_ and raw not in unnamed:
                        unnamed.append(raw)
        blocks = getattr(S, "blocks", None)
        if blocks is None and callable(globals().get("bld_blocks")):
            blocks = bld_blocks(S.bld)
        for bk in blocks or []:
            mem = [idx_of[i] for i in bk.get("units", []) if i in idx_of]
            L["blocks"].append(dict(rings=[_bm_r(bk["outer"])] + [_bm_r(H) for H in bk.get("holes") or []],
                                    her=bool(mem) and all(L["buildings"][i]["her"] for i in mem)))
        L["study"] = [_bm_r(P) for P in (getattr(S, "r28_study", None) or globals().get("R28_STUDY_COPY") or [])]
        pl = globals().get("place_label")                 # round 5 (S2, A11): REACH literals by the table's spelling
        L["names"] = [[(pl(n, p) if callable(pl) else None) or n, [round(p[0], 1), round(p[1], 1)]]
                      for n, p in BASEMAP_REACH] + L["names"]
        if unnamed:
            log.append(u"FLAG basemap names not in the names table, left out ({}): {} [ask Aras for the spelling and a "
                       u"source]".format(len(unnamed), u", ".join(unnamed[:20])))
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
                            lv = tags.get("building:levels")
                            try:
                                lv = int(float(lv)) if lv else 0
                            except ValueError:
                                lv = 0
                            L["buildings"].append(dict(rings=[_bm_r(P[:-1])], np=1, her=her, osm=True, h=0.0,
                                                       floors=lv))
                            L["blocks"].append(dict(rings=[_bm_r(P[:-1])], her=her))
                            n_out += 1
                    continue
                hw = tags.get("highway")
                if hw and hw not in skip and tags.get("area") != "yes":
                    runs_ = outside_line(P)
                    L["streets_out"].extend([ccls(hw), run] for run in runs_)
                    for run in runs_:
                        street_name(tags, run, ccls(hw))
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
        stl = globals().get("street_label")               # round 5 (S2): the table's spelling where it has the street
        for nm_, (Ln, cl, P) in sn_best.items():           # the label point: the run's middle, along its direction
            half, acc = Ln / 2.0, 0.0
            for a_, b_ in zip(P, P[1:]):
                d_ = _bm_math.hypot(b_[0] - a_[0], b_[1] - a_[1])
                if acc + d_ >= half and d_ > 1e-9:
                    t_ = (half - acc) / d_
                    ang = _bm_math.degrees(_bm_math.atan2(b_[1] - a_[1], b_[0] - a_[0]))
                    L["street_names"].append([stl(nm_) if callable(stl) else nm_, [round(a_[0] + (b_[0] - a_[0]) * t_, 1),
                                                    round(a_[1] + (b_[1] - a_[1]) * t_, 1)], round(ang, 1), cl,
                                              round(Ln, 1)])
                    break
                acc += d_
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


# ---- round 4 (S2, 1 Nov 2026): the study clip, the map-layer draw order and the key-map module ride with the basemap,
# so every script that includes basemap.py has them (never include them a second time)
# ---- Study clip (round 4 S2, 1 Nov 2026; G-R4-4 "proposals clipped to the study area", U40, S14; PLAN §4.3) --------
# ONE clip to the study area (calisma_alan of Bergama_Altlik.3dm, two closed parts worked as one area) for every
# proposal a script draws or exports: nothing designed outside it ("we cant do any adjustments outside the study
# area", U40). Clip at the SOURCE (where a proposal is generated) so every page that reads it inherits the clip.
# Included by common/basemap.py (its last lines): every script that includes basemap.py has these functions; do not
# include this file again. Geometry: survey m; rings = [[(x, y), ...], ...] (closed implicitly).
# Counts: every call with page= adds what it removed to SC_COUNT[page]; map_layers.map_draw prints it in the G-R4-4
# done-when line "layers base→project ok, n_outside_clipped <n>"; sc_lines_log() gives the per-page lines.
#   sc_rings(D=None, areas=None)                        the study rings (areas dict values, else the basemap's study)
#   sc_inside(p, rings, margin_m=0.0)                   point inside (margin_m > 0: at least that far inside)
#   sc_points(items, rings, get=None, r_frac=0.0, page=None)    keep point symbols inside (their crown too)
#   sc_lines(P, rings, page=None)                       polyline -> its runs inside (exact edge crossings)
#   sc_rings_clip(R, rings, page=None)                  polygon ∩ study (Greiner-Hormann, non-convex) -> [rings]
#   sc_items(items, rings, page=None)                   basemap-format items clipped ("fill", "line", "text")
#   sc_cell_mask(G, V, rings=None)                      bytearray per grid cell (masterplan Grid) inside the study
#   sc_lines_log()                                      "study clip <page>: n_outside_clipped=<n> (points a, lines
#                                                       b, rings c)" per page, then emptied
import math as _sc_m

SC_COUNT = {}                       # page -> dict(points=, lines=, rings=) removed this run
SC_EPS = 1e-9


def _sc_add(page, kind, n):
    if page is None or n <= 0:
        return
    c = SC_COUNT.setdefault(page, dict(points=0, lines=0, rings=0))
    c[kind] += n


def sc_count(page):
    """n_outside_clipped of a page this run (points + lines + rings removed or cut)"""
    c = SC_COUNT.get(page) or {}
    return int(c.get("points", 0) + c.get("lines", 0) + c.get("rings", 0))


def sc_rings(D=None, areas=None):
    """the study area as rings (survey m): the values of an areas dict (the masterplan's calisma_alan parts, as
    read from Bergama_Altlik.3dm), else basemap_study(D) (the basemap file's study layer, or a script's recorded
    copy); [] when neither exists (then every clip keeps everything and logs a FLAG once)"""
    if areas:
        R = areas.values() if isinstance(areas, dict) else areas
        return [[(float(p[0]), float(p[1])) for p in r] for r in R if len(r) >= 3]
    st = basemap_study(D) if callable(globals().get("basemap_study")) else []
    if not st:
        SC_COUNT.setdefault(u"_flag", dict(points=0, lines=0, rings=0))
    return [[(float(p[0]), float(p[1])) for p in r] for r in st if len(r) >= 3]


def _sc_open(r):
    return r[:-1] if len(r) > 1 and abs(r[0][0] - r[-1][0]) < SC_EPS and abs(r[0][1] - r[-1][1]) < SC_EPS else r


def _sc_pip(x, y, R):
    c, n = False, len(R)
    j = n - 1
    for i in range(n):
        xi, yi, xj, yj = R[i][0], R[i][1], R[j][0], R[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            c = not c
        j = i
    return c


def _sc_dist(p, R):
    best = float("inf")
    n = len(R)
    for i in range(n):
        a, b = R[i], R[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2)) if L2 > 0 else 0.0
        best = min(best, _sc_m.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy))
    return best


def sc_inside(p, rings, margin_m=0.0):
    """True when p lies inside one of the study rings (the parts are separate areas: inside ANY); margin_m > 0: and
    at least margin_m from that ring's outline; margin_m < 0: or within -margin_m outside it. No rings: True."""
    if not rings:
        return True
    for R in rings:
        R = _sc_open(R)
        ins = _sc_pip(p[0], p[1], R)
        if margin_m == 0.0:
            if ins:
                return True
        elif margin_m > 0.0:
            if ins and _sc_dist(p, R) >= margin_m:
                return True
        elif ins or _sc_dist(p, R) <= -margin_m:
            return True
    return False


def sc_points(items, rings, get=None, r_frac=0.0, page=None):
    """the point items inside the study area. get(item) -> (x, y) or (x, y, r) (default: the item itself, a point or
    (x, y, r)); r_frac: the share of a symbol's radius that must lie inside too (1.0 = the whole crown inside, 0 =
    its centre). Removed items are counted for the page. Returns the kept items (same objects, same order)."""
    if not rings:
        return list(items)
    get = get or (lambda it: it)
    kept, n = [], 0
    for it in items:
        q = get(it)
        r = float(q[2]) if len(q) > 2 and q[2] is not None else 0.0
        if sc_inside((q[0], q[1]), rings, margin_m=r * r_frac):
            kept.append(it)
        else:
            n += 1
    _sc_add(page, "points", n)
    return kept


def _sc_seg_ts(a, b, rings):
    """the parameters t in (0, 1) where segment a-b crosses any study ring edge"""
    ts = []
    dx, dy = b[0] - a[0], b[1] - a[1]
    for R in rings:
        R = _sc_open(R)
        n = len(R)
        for i in range(n):
            p, q = R[i], R[(i + 1) % n]
            ex, ey = q[0] - p[0], q[1] - p[1]
            den = dx * ey - dy * ex
            if abs(den) < 1e-15:
                continue
            t = ((p[0] - a[0]) * ey - (p[1] - a[1]) * ex) / den
            s = ((p[0] - a[0]) * dy - (p[1] - a[1]) * dx) / den
            if SC_EPS < t < 1.0 - SC_EPS and -SC_EPS <= s <= 1.0 + SC_EPS:
                ts.append(t)
    return sorted(ts)


def sc_lines(P, rings, page=None):
    """a polyline (survey m) -> its runs inside the study area: every segment split at its exact crossings of the
    study outlines (not a vertex test), the pieces whose middle lies inside kept and joined where they touch.
    A polyline with a part outside counts once for the page. Returns [run, ...] (each >= 2 points)."""
    P = [tuple(p[:2]) for p in P]
    if not rings or len(P) < 2:
        return [P] if len(P) >= 2 else []
    runs, cur, cut = [], [], False
    for a, b in zip(P, P[1:]):
        ts = [0.0] + _sc_seg_ts(a, b, rings) + [1.0]
        for t0, t1 in zip(ts, ts[1:]):
            if t1 - t0 < 1e-12:
                continue
            tm = 0.5 * (t0 + t1)
            pa = (a[0] + (b[0] - a[0]) * t0, a[1] + (b[1] - a[1]) * t0)
            pb = (a[0] + (b[0] - a[0]) * t1, a[1] + (b[1] - a[1]) * t1)
            if sc_inside((a[0] + (b[0] - a[0]) * tm, a[1] + (b[1] - a[1]) * tm), rings):
                if cur and abs(cur[-1][0] - pa[0]) < 1e-7 and abs(cur[-1][1] - pa[1]) < 1e-7:
                    cur.append(pb)
                else:
                    if len(cur) >= 2:
                        runs.append(cur)
                    cur = [pa, pb]
            else:
                cut = True
                if len(cur) >= 2:
                    runs.append(cur)
                cur = []
    if len(cur) >= 2:
        runs.append(cur)
    if cut:
        _sc_add(page, "lines", 1)
    return runs


# ---- Greiner-Hormann polygon intersection (subject ∩ clip; both simple, any shape) ----------------------------------
class _ScNode(object):
    __slots__ = ("x", "y", "nxt", "prv", "inter", "entry", "nb", "alpha", "seen")

    def __init__(self, x, y, inter=False, alpha=0.0):
        self.x, self.y = x, y
        self.nxt = self.prv = self.nb = None
        self.inter, self.entry, self.alpha, self.seen = inter, False, alpha, False


def _sc_list(R):
    nodes = [_ScNode(p[0], p[1]) for p in R]
    n = len(nodes)
    for i in range(n):
        nodes[i].nxt = nodes[(i + 1) % n]
        nodes[i].prv = nodes[i - 1]
    return nodes


def _sc_next_orig(v):
    v = v.nxt
    while v.inter:
        v = v.nxt
    return v


def _sc_gh(S, C):
    """S ∩ C as rings, or None when a vertex lies on the other's edge (the caller perturbs and retries)"""
    sl, cl = _sc_list(S), _sc_list(C)
    hits = []
    for i, s0 in enumerate(sl):
        s1 = sl[(i + 1) % len(sl)]
        for j, c0 in enumerate(cl):
            c1 = cl[(j + 1) % len(cl)]
            dx, dy = s1.x - s0.x, s1.y - s0.y
            ex, ey = c1.x - c0.x, c1.y - c0.y
            den = dx * ey - dy * ex
            if abs(den) < 1e-15:
                continue
            a = ((c0.x - s0.x) * ey - (c0.y - s0.y) * ex) / den
            b = ((c0.x - s0.x) * dy - (c0.y - s0.y) * dx) / den
            if -1e-9 <= a <= 1.0 + 1e-9 and -1e-9 <= b <= 1.0 + 1e-9:
                if a < 1e-7 or a > 1.0 - 1e-7 or b < 1e-7 or b > 1.0 - 1e-7:
                    return None                           # degenerate (vertex on an edge)
                hits.append((i, a, j, b, s0.x + dx * a, s0.y + dy * a))
    if not hits:
        if _sc_pip(S[0][0], S[0][1], C):
            return [list(S)]
        if _sc_pip(C[0][0], C[0][1], S):
            return [list(C)]
        return []
    # insert the intersections into both lists, sorted by alpha along each edge
    by_s, by_c = {}, {}
    for h in hits:
        i, a, j, b, x, y = h
        ns, nc = _ScNode(x, y, True, a), _ScNode(x, y, True, b)
        ns.nb, nc.nb = nc, ns
        by_s.setdefault(i, []).append(ns)
        by_c.setdefault(j, []).append(nc)
    for base, groups in ((sl, by_s), (cl, by_c)):
        for i, grp in groups.items():
            grp.sort(key=lambda nd: nd.alpha)
            v, end = base[i], base[(i + 1) % len(base)]
            for nd in grp:
                nd.prv, nd.nxt = v, end
                v.nxt = nd
                end.prv = nd
                v = nd
    # entry / exit flags
    for start, other in ((sl[0], C), (cl[0], S)):
        status = not _sc_pip(start.x, start.y, other)    # True: the next intersection is an entry
        v = start
        while True:
            if v.inter:
                v.entry = status
                status = not status
            v = v.nxt
            if v is start:
                break
    # trace: from an unvisited intersection, forward along an entry, backward along an exit, switch lists at each
    # intersection, until the walk reaches a visited one (the start)
    out = []
    for h0 in [nd for grp in by_s.values() for nd in grp]:
        if h0.seen:
            continue
        ring, v, guard = [(h0.x, h0.y)], h0, 0
        while True:
            v.seen = True
            v.nb.seen = True
            fwd = v.entry                                # the direction is the starting intersection's
            while True:
                v = v.nxt if fwd else v.prv
                ring.append((v.x, v.y))
                if v.inter:
                    break
            v = v.nb
            guard += 1
            if v.seen or guard > 10000:
                break
        if len(ring) > 1 and abs(ring[0][0] - ring[-1][0]) < 1e-9 and abs(ring[0][1] - ring[-1][1]) < 1e-9:
            ring.pop()
        if len(ring) >= 3:
            out.append(ring)
    return out


def _sc_poly_and(S, C):
    """S ∩ C, perturbing S by a hair when a vertex falls on an edge (at most 6 tries)"""
    S = [tuple(p[:2]) for p in _sc_open(S)]
    C = [tuple(p[:2]) for p in _sc_open(C)]
    for k in range(6):
        r = _sc_gh(S, C)
        if r is not None:
            return r
        d = 1e-6 * (k + 1)
        S = [(p[0] + d * ((i * 7919) % 13 - 6) / 6.0, p[1] + d * ((i * 104729) % 11 - 5) / 5.0)
             for i, p in enumerate(S)]
    # last resort: keep the ring when its centre lies inside (logged by the caller's count)
    cx = sum(p[0] for p in S) / len(S)
    cy = sum(p[1] for p in S) / len(S)
    return [S] if _sc_pip(cx, cy, C) else []


def _sc_area(R):
    n = len(R)
    return 0.5 * sum(R[i][0] * R[(i + 1) % n][1] - R[(i + 1) % n][0] * R[i][1] for i in range(n))


def sc_rings_clip(R, rings, page=None):
    """a polygon (one ring, survey m) ∩ the study area: [ring, ...] (the study parts are separate: one result per
    part it reaches; Greiner-Hormann, non-convex both ways). A polygon that loses any area counts once for the page;
    one wholly outside returns []."""
    R = [tuple(p[:2]) for p in _sc_open(list(R))]
    if not rings or len(R) < 3:
        return [R] if len(R) >= 3 else []
    out = []
    for S in rings:
        out += [r for r in _sc_poly_and(R, S) if abs(_sc_area(r)) > 1e-6]
    a0 = abs(_sc_area(R))
    a1 = sum(abs(_sc_area(r)) for r in out)
    if a0 - a1 > max(1e-6, 1e-6 * a0):
        _sc_add(page, "rings", 1)
    return out


def sc_items(items, rings, page=None):
    """basemap-format items (common/basemap.py head) clipped to the study area: "fill" -> each ring through
    sc_rings_clip (holes clipped the same way, so an even-odd fill keeps them), "line" -> sc_lines runs, "text" ->
    kept only when its point is inside; "water" and anything else pass unchanged (they are base, not proposals).
    Returns the new item list."""
    if not rings:
        return list(items)
    out = []
    for it in items:
        k = it[0]
        if k == "fill":
            rs = [r for R in it[1] if len(R) >= 3 for r in sc_rings_clip(R, rings, page)]
            if rs:
                out.append(("fill", rs) + tuple(it[2:]))
        elif k == "line":
            for run in sc_lines(it[1], rings, page):
                out.append(("line", run) + tuple(it[2:]))
        elif k == "text":
            if sc_inside(it[2], rings):
                out.append(it)
            else:
                _sc_add(page, "points", 1)
        else:
            out.append(it)
    return out


def sc_cell_mask(G, V=None, rings=None):
    """a bytearray over the masterplan Grid G (G.nx x G.ny): 1 where the cell's centre lies in the study area
    (rings, else V.study); every grid-traced proposal requires mask[n] (PLAN §3 CHK-7 call sites)"""
    rings = rings if rings is not None else (getattr(V, "study", None) or sc_rings())
    m = bytearray(G.nx * G.ny)
    for R in rings or ():
        for n in G.poly_cells([tuple(p[:2]) for p in _sc_open(list(R))]):
            m[n] = 1
    return m


def sc_lines_log():
    """this run's per-page clip lines, then emptied: "study clip <page>: n_outside_clipped=<n> (points a, lines b,
    rings c)"; a FLAG line when no study area was found"""
    out = []
    for pg in sorted(SC_COUNT):
        c = SC_COUNT[pg]
        if pg == u"_flag":
            out.append(u"FLAG study clip: no study area (calisma_alan) in the basemap file or the script: nothing was "
                       u"clipped (run the site board once)")
            continue
        out.append(u"study clip %s: n_outside_clipped=%d (points %d, lines %d, rings %d)"
                   % (pg, c["points"] + c["lines"] + c["rings"], c["points"], c["lines"], c["rings"]))
    SC_COUNT.clear()
    return out
# ---- Map layers (round 4 S2, 1 Nov 2026; G-R4-4 "base map back, our drawings in front", D9 tint; PLAN §4.3) ---------
# ONE draw-order function for every map, plan and axo (p02, p06, p08, p10, p12, p16, p17, p20, p21, p22 and every key
# map): the base map muted, light and at the bottom; our drawings saturated and on top; the study line in its own
# layer above the project fills; proposals clipped to the study area at draw time too (study_clip.py) and counted.
# Included by common/basemap.py (its last lines, after study_clip.py); do not include it again.
# Items: the basemap format (common/basemap.py head), survey m (or already projected, e.g. an axo: then T = identity).
# Round 5 (S2, 1 Nov 2026; G-R5-8 "water drawn above every zone tint", G-R5-10 "base muted and cropped"): two layers
# after the project tints, "water" (the base stream) and "structures" (decks, covered course, bridges over it); a flat
# base list is filed by each item's layer (basemap _BmIt) so the stream lands in "water"; a base dict's "base_water"
# is drawn as "water" too; map_draw logs `zones <page> over_water_area <m2>, unlabeled_fields <n>`; ml_base crops.
#   ML_LAYERS                                   the 15 layers, bottom first
#   ml_base(box, scale_den, D=None, contours=False, names=False, override=None, crop=True)  the muted base (basemap
#                                               "muted"), cut to box (round 5, G-R5-10)
#   ml_crop(items, ring)                        round 5: items cut to a convex ring (survey m): fills, lines, water
#   ml_layer_of(item)                           round 5: the ML layer a base item belongs to
#   ml_tint(rings, colour=None, alpha=None, study=None, page=None)    D9 footprint tint items (clipped to the study)
#   ml_study_items(rings=None, D=None)          the study-area line items (BM_STUDY_LINE, one style everywhere)
#   map_draw(page, T, fill_fn, line_fn, text_fn, base, project, study=None, clip=True, order_fn=None, log=None,
#            water_opts=None, study_line=True, legend_cols=None, water_ok=None)
#                                               draws base -> project strictly in ML_LAYERS order; logs the done-when
#                                               line "layers base→project ok, n_outside_clipped <n> (<page>)" and
#                                               round 5 "zones <page> over_water_area <m2>, unlabeled_fields <n>"
# round 5 (S2, G-R5-8; PLAN §3 draw order: base fills -> tints / zone fields -> WATER -> structures over water ->
# planting -> people -> labels): "water" and "structures" follow "proj_tint"; the old names keep their places so
# stage lists that check the order (water board p12) still pass
ML_LAYERS = ("base_ground", "base_contours", "base_fills", "base_water", "base_outlines", "base_names",
             "proj_tint", "water", "structures", "proj_water", "proj_lines", "proj_vegetation", "study", "proj_marks",
             "proj_labels")
ML_BASE_LAYERS = ("base_ground", "base_contours", "base_fills", "base_water", "base_outlines", "base_names", "water",
                  "structures")
ML_PROJ_LAYERS = ("proj_tint", "proj_water", "proj_lines", "proj_vegetation", "study", "proj_marks", "proj_labels")
ML_FIELD_LAYERS = ("proj_lines", "proj_vegetation", "proj_marks")   # fills here are drawn above the stream
# D9 (Aras 1 Nov, U52 "çok hafif izdüşüm ... transparan çok hafif bir renkle"): the proposal footprint tint, very
# light and transparent, on every plan that shows proposals (p08, p10 plans, p12, p16, p17, p21, p22)
ML_TINT = "5C7A86"                  # palette reference slate (library/examples/palettes)
ML_TINT_ALPHA = 0.16
ML_NAME_MM = 2.12                   # base names 6 pt (the booklet minimum, G-R4-1), BM_MUTED["name"] tone
ML_NO_CLIP = ("proj_labels",)       # labels are placed by the text placer and may sit just outside the line
ML_LOG = []                         # this run's map_draw lines (a page script appends them to its log)


def ml_base(box, scale_den, D=None, contours=False, names=False, override=None, crop=True):
    """the muted base of a map (G-R4-4): basemap mode "muted" = the stream (M5 water), light streets with closed
    edges, light houses with ONE closed outline per block, every outline after every fill; contours=True adds the
    contours coloured to the relief (green ramp, lighter = lower, U48); names=True the place names (6 pt, pale).
    The study line is NOT in it (map_draw draws it in its own layer). box = (x0, y0, x1, y1) survey m; scale_den =
    the map's 1:scale_den. Returns basemap items (bottom first), [] without basemap data. Round 5 (G-R5-10):
    crop=True cuts every item to box, so nothing of the base runs past the drawing's window."""
    ov = dict(contours="height" if contours else False, names=bool(names))
    ov.update(override or {})
    its = basemap_items("muted", ov, box=box, D=D, scale_den=scale_den)
    its = [_bm_tag(("text", it[1], it[2], ML_NAME_MM, BM_MUTED["name"], False, it[6]), "base_names")
           if it[0] == "text" else it for it in its]
    if crop and box:
        its = ml_crop(its, [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])])
    return its


def _ml_clip_poly(R, ring):
    """ring R cut to the convex ring (Sutherland-Hodgman, any turn); [] when nothing is left"""
    n = len(ring)
    ccw = sum((ring[(i + 1) % n][0] - ring[i][0]) * (ring[(i + 1) % n][1] + ring[i][1]) for i in range(n)) < 0
    out = list(R)
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        ex, ey = b[0] - a[0], b[1] - a[1]

        def side(p):
            c = ex * (p[1] - a[1]) - ey * (p[0] - a[0])
            return c if ccw else -c
        if not out:
            return []
        nxt = []
        for j in range(len(out)):
            p, q = out[j - 1], out[j]
            sp, sq = side(p), side(q)
            if sq >= 0:
                if sp < 0:
                    t = sp / (sp - sq)
                    nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                nxt.append(q)
            elif sp >= 0:
                t = sp / (sp - sq)
                nxt.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
        out = nxt
    return out if len(out) >= 3 else []


def _ml_inside_convex(P, ring):
    n = len(ring)
    ccw = sum((ring[(i + 1) % n][0] - ring[i][0]) * (ring[(i + 1) % n][1] + ring[i][1]) for i in range(n)) < 0
    for i in range(n):
        a, b = ring[i], ring[(i + 1) % n]
        for p in P:
            c = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
            if (c if ccw else -c) < 0:
                return False
    return True


def _ml_retag(src, t):
    lay = getattr(src, "layer", None)
    return _bm_tag(t, lay) if lay else t


def ml_crop(items, ring):
    """round 5 (S2, G-R5-10): basemap items cut to the convex ring (survey m, e.g. a key map's turned frame):
    fills ring by ring (a ring wholly inside is kept as it is), lines run by run, the "water" item ring by ring,
    texts kept when their point is inside. Each item keeps its map layer."""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    bb = (min(xs), min(ys), max(xs), max(ys))

    def rings_cut(Rs):
        out = []
        for R in Rs:
            if len(R) < 3:
                continue
            if _ml_inside_convex(R, ring):
                out.append(R)
                continue
            rx, ry = [p[0] for p in R], [p[1] for p in R]
            if max(rx) < bb[0] or min(rx) > bb[2] or max(ry) < bb[1] or min(ry) > bb[3]:
                continue
            c = _ml_clip_poly(R, ring)
            if c:
                out.append(c)
        return out
    out = []
    for it in items:
        if it[0] == "fill":
            rs = rings_cut(it[1])
            if rs:
                out.append(_ml_retag(it, ("fill", rs) + tuple(it[2:])))
        elif it[0] == "line":
            P = it[1]
            if _ml_inside_convex(P, ring):
                out.append(it)
                continue
            for a, b in zip(P, P[1:]):
                ab = _bm_clip_convex(a, b, ring)
                if ab:
                    out.append(_ml_retag(it, ("line", [ab[0], ab[1]]) + tuple(it[2:])))
        elif it[0] == "water":
            gs = []
            for g in it[1]:
                c = rings_cut([g[0]])
                if c:
                    gs.append(c + rings_cut(g[1:]))
            if gs:
                es = []
                for P in it[2]:
                    for a, b in zip(P, P[1:]):
                        ab = _bm_clip_convex(a, b, ring)
                        if ab:
                            es.append([ab[0], ab[1]])
                out.append(_ml_retag(it, ("water", gs, es) + tuple(it[3:])))
        elif it[0] == "text":
            if _ml_inside_convex([it[2]], ring):
                out.append(it)
        else:
            out.append(it)
    return out


def ml_layer_of(it):
    """round 5 (S2, G-R5-8): the map layer of a base item: its own (basemap _BmIt.layer), else by kind (the stream
    item and the base water tones -> "water", texts -> "base_names", the rest "base_fills")"""
    lay = getattr(it, "layer", None)
    if lay in ML_BASE_LAYERS:
        return "water" if lay == "base_water" else lay
    if it[0] == "water":
        return "water"
    if it[0] == "text":
        return "base_names"
    wc = (BM_COL["water"], BM_COL["water_edge"], BM_KEY["water"], BM_KEY["water_edge"])
    if it[0] in ("fill", "line") and it[2] in wc:
        return "water"
    return "base_fills"


def _ml_pip(x, y, R):
    ins = False
    j = len(R) - 1
    for i in range(len(R)):
        xi, yi = R[i]
        xj, yj = R[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            ins = not ins
        j = i
    return ins


def _ml_over_water(fills, water, T=None, n=12):
    """round 5 (S2, G-R5-8): the area (m², or page mm² when the items are already projected) of fills that lie
    over the water rings, estimated on an n x n grid per fill ring (even-odd inside both)"""
    if not fills or not water:
        return 0.0
    wb = [(R, (min(p[0] for p in R), min(p[1] for p in R), max(p[0] for p in R), max(p[1] for p in R)))
          for R in water if len(R) >= 3]
    area = 0.0
    for it in fills:
        for R in it[1]:
            if len(R) < 3:
                continue
            x0, y0 = min(p[0] for p in R), min(p[1] for p in R)
            x1, y1 = max(p[0] for p in R), max(p[1] for p in R)
            if not any(not (b[2] < x0 or b[0] > x1 or b[3] < y0 or b[1] > y1) for _, b in wb):
                continue
            dx, dy = (x1 - x0) / n, (y1 - y0) / n
            hit = 0
            for i in range(n):
                for j in range(n):
                    x, y = x0 + (i + 0.5) * dx, y0 + (j + 0.5) * dy
                    if _ml_pip(x, y, R) and any(b[0] <= x <= b[2] and b[1] <= y <= b[3] and _ml_pip(x, y, W)
                                                for W, b in wb):
                        hit += 1
            area += hit * dx * dy
    return area


def ml_tint(rings, colour=None, alpha=None, study=None, page=None):
    """D9: the light transparent footprint of what we change (channel setbacks, ponds, basins, terraces, store, new
    paths) as fill items, one per ring, clipped to the study rings (study_clip sc_rings_clip) when study is given.
    rings: [ring, ...] survey m (or page mm with study=None). Put them in map_draw's "proj_tint" layer."""
    col, a = colour or ML_TINT, ML_TINT_ALPHA if alpha is None else alpha
    out = []
    for R in rings or ():
        if len(R) < 3:
            continue
        for r in (sc_rings_clip(R, study, page) if study else [R]):
            out.append(("fill", [r], col, a, True))
    return out


def ml_study_items(rings=None, D=None):
    """the study-area outline as line items, ONE style everywhere (BM_STUDY_LINE: violet long-dash-dot, U18/U19);
    rings default = the basemap's study area"""
    st = BM_STUDY_LINE
    rings = rings if rings is not None else basemap_study(D)
    return [("line", list(R) + [R[0]], st["colour"], st["width_mm"], list(st["dash_mm"]), 1.0)
            for R in rings or () if len(R) >= 3]


def map_draw(page, T, fill_fn, line_fn, text_fn, base, project, study=None, clip=True, order_fn=None, log=None,
             water_opts=None, study_line=True, legend_cols=None, water_ok=None):
    """THE draw order of every map (G-R4-4 done-when). page: the booklet page id ("p21"); T(p) survey m -> page
    point (identity for items already projected); fill_fn / line_fn / text_fn as basemap_draw. base: the base items
    (ml_base, in their own order) or {base layer: items}; project: {layer: items} or [(layer, items)] with layers
    from ML_PROJ_LAYERS ("proj_tint", "proj_water", "proj_lines", "proj_vegetation", "proj_marks", "proj_labels");
    study: the study rings (sc_rings): with clip=True every project item except labels is clipped to them
    (sc_items) and counted; the study line goes in the "study" layer (study_line=False leaves it out, e.g. a key map
    that draws its own). order_fn(layer): called before each layer is drawn (the site board's page order numbers:
    base 2-28, tint 30-39, project 40-59, marks 60-69). Draws strictly in ML_LAYERS order, whatever order the
    caller listed. Returns dict(n_base, n_project, n_outside_clipped, layers) and logs (ML_LOG and log) "layers
    base→project ok, n_outside_clipped <n> (<page>)".
    Round 5 (S2, G-R5-8): the base stream is drawn in "water", above "proj_tint" (a flat base list is filed by
    ml_layer_of; a base dict's "base_water" goes to "water"), decks / covered course / bridges in "structures". Logs
    `zones <page> over_water_area <m2>, unlabeled_fields <n>`: over_water_area = fills in proj_lines /
    proj_vegetation / proj_marks (drawn above the stream) over the base water, minus fills whose colour is in
    water_ok (fields in the water by design: widened stream, wetland, sub-hub, spillway, reed arms); unlabeled_fields
    = tint and field fills whose colour is not in legend_cols (the legend's swatch colours; "n/a" + a FLAG when the
    page passes none). A count above 0 is a WARNING line (the run goes on)."""
    if isinstance(base, dict):
        bad = [k for k in base if k not in ML_BASE_LAYERS]
        if bad:
            raise ValueError(u"map_draw %s: base layer(s) %s unknown: use %s" % (page, bad, ", ".join(ML_BASE_LAYERS)))
        bd = {}
        for k in ML_BASE_LAYERS:
            if base.get(k):
                bd.setdefault("water" if k == "base_water" else k, []).extend(base[k])
        base_l = [(k, bd[k]) for k in ML_BASE_LAYERS if bd.get(k)]
    else:
        bd = {}
        for it in base or []:
            bd.setdefault(ml_layer_of(it), []).append(it)
        base_l = [(k, bd[k]) for k in ML_BASE_LAYERS if bd.get(k)]
    proj = {}
    for k, its in (project.items() if isinstance(project, dict) else (project or [])):
        if k not in ML_PROJ_LAYERS or k == "study":
            raise ValueError(u"map_draw %s: project layer %r unknown: use %s" % (page, k, ", ".join(
                l_ for l_ in ML_PROJ_LAYERS if l_ != "study")))
        proj.setdefault(k, []).extend(its or [])
    if study and clip:
        for k in list(proj):
            if k not in ML_NO_CLIP:
                proj[k] = sc_items(proj[k], study, page)
    if study and study_line:
        proj["study"] = ml_study_items(study)
    n_out = sc_count(page)                               # this page's clips this run: at the source + here
    nb = npj = 0
    drawn = []
    for layer in ML_LAYERS:
        its = dict(base_l).get(layer) if layer in ML_BASE_LAYERS else proj.get(layer)
        if not its:
            continue
        if order_fn is not None:
            order_fn(layer)
        n = basemap_draw(its, T, fill_fn, line_fn, text_fn, water_opts)
        drawn.append(layer)
        if layer in ML_BASE_LAYERS:
            nb += n
        else:
            npj += n
    ok = all(ML_LAYERS.index(a) < ML_LAYERS.index(b) for a, b in zip(drawn, drawn[1:]))
    line = (u"layers base→project %s, n_outside_clipped %d (%s: %s)"
            % (u"ok" if ok else u"FLAG out of order", n_out, page, u", ".join(drawn)))
    ML_LOG.append(line)
    if log is not None:
        log.append(line)
    # round 5 (S2, G-R5-8): the zones done-when line
    wrings = basemap_water_rings(dict(base_l).get("water") or [])
    wrings += [R for it in dict(base_l).get("water") or [] if it[0] == "fill" and it[2] not in
               (BM_COL["water"],) for R in it[1] if len(R) >= 3]
    ok_c = set(str(c).upper() for c in (water_ok or ()))
    above = [it for k in ML_FIELD_LAYERS for it in proj.get(k) or []
             if it[0] == "fill" and str(it[2]).upper() not in ok_c]
    ow = _ml_over_water(above, wrings)
    tints = [it for k in ("proj_tint",) + ML_FIELD_LAYERS for it in proj.get(k) or [] if it[0] == "fill"]
    if legend_cols is None:
        nu = u"n/a"
    else:
        lc = set(str(c).upper() for c in legend_cols)
        nu = sum(1 for it in tints if str(it[2]).upper() not in lc)
    zl = u"zones %s over_water_area %d, unlabeled_fields %s" % (page, int(round(ow)), nu)
    extra = []
    if ow > 0.5 or (nu != u"n/a" and nu > 0):
        extra.append(u"WARNING %s zones over_water_area %d, unlabeled_fields %s" % (page, int(round(ow)), nu))
    if nu == u"n/a" and tints:
        extra.append(u"FLAG zones %s: no legend colours passed, unlabeled fields not counted" % page)
    for l_ in [zl] + extra:
        ML_LOG.append(l_)
        if log is not None:
            log.append(l_)
    return dict(n_base=nb, n_project=npj, n_outside_clipped=n_out, layers=drawn, over_water_area=ow,
                unlabeled_fields=nu)


def ml_lines_log():
    """this run's map_draw lines, then emptied"""
    out = list(ML_LOG)
    del ML_LOG[:]
    return out
# ---- Key maps, cut symbol, north arrow (round 4 S2, 1 Nov 2026; G-R4-9, R01, U02 U31 U50 U51 U55 U60; PLAN §4.5) -----
# ONE key-map module: every cut line drawn with the R01 symbol in red (an end bar with an open triangle standing on it
# pointing the way the section looks, a dash-dot line between), in front of a muted base, with ONLY the page's cuts,
# the main street and place names (so the reader knows where it is), never over its legend; ONE north arrow (the
# arrow and "N", no plate, U31 U51). Included by common/basemap.py (its last lines, after map_layers.py); do not
# include it again. The old basemap_cut_items / keymap_items are thin wrappers at the end of this file.
# ROUND 5 (S2, 1 Nov 2026; G-R5-3, D3, D6, A11, U33 U36 U45 U67-U69; PLAN §3 "Key map"): v2. Drawn like the p02 map
# (basemap mode "keymap": green ground, houses by urban fabric, the stream blue, bridges), never the grey blob; the
# frame cut to the map (fitted, fill logged, >= 0.85); turned so the corridor runs along the frame's long side, the
# north arrow showing true north in a free corner; names only through the names table (street_label, keymap_places);
# exported as items for the booklet (km_items: drawing + text labels with anchors + keymap item; G-R5-12, Aras's
# addendum 1 Nov 22:37 point 3). Every page's key map calls km_map (p04, p05, p09, p10 locator, p13-14, p15, p16,
# p18, p19-20, p24; their page sessions S6-S10 switch the callers to km_items); scale_den keeps the round 4 contract.
#   KM_CUT, KM_NAMES, KM_FRAME, KM_CUT_PLAN      the cut symbol, the names switches, the frame line, plan cuts (D6)
#   km_cut_items(cuts, scale_den, frame=None, style=None, text_mm=2.47)      R01 cut symbols as items (survey m)
#   km_map(ids, w_mm=None, h_mm=None, zooms=None, page=None, names=None, legend_box=None, log=None, looks=None,
#          box=None, scale_den=None, extra_names=None, D=None, margin=None, rotate=None, fit=None, pad_mm=None,
#          base_mode="keymap", north=True)                                  a whole key map (survey m + its T)
#   km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None, log=None, frame=True)   draws it
#   km_items(km, page=None, item_id=None, priority=5)                       round 5: the key map as booklet items
#   km_texts(km)                                 its texts in key-map mm, for the page's TextPage (.put)
#   north_items(x, y, ang_rad=0.0, size_mm=6.0, colour="2C2219")           the north arrow (page mm, y up)
# Items: the basemap format (common/basemap.py head). Key-map mm: origin at the key map's lower-left, y up.
import math as _km_m

# R01 in red (G-R4-9): line 0.5 mm dash-dot; end bar 2.4 mm along the line at each end, the open triangle standing on
# it (base = the bar, height tri_h, apex the way the section looks), the end name beyond the bar. Sizes: drawing rules
# of PLAN §4.5 (the triangle's base is the bar so it never overhangs it).
KM_CUT = dict(colour="C0392B", lw=0.5, dash=(3.0, 0.8, 0.6, 0.8), end_bar=2.4, bar_lw=0.6, tri_h=2.1, tri_lw=0.35,
              text_mm=2.47, gap_mm=0.8)
KM_NAMES = dict(streets=("main",), n_streets=4, places=True, n_places=6, size_mm=2.12, colour="6B645B", bold=False,
                pad_mm=0.6)
KM_ZOOM = dict(colour="C0392B", lw=0.35)       # zoom / window frames on a key map: the cut red, solid
KM_FRAME = dict(colour="4A3F35", lw=0.25)      # round 5 (S2, D3): the key map's frame line (site board INK), hairline
# round 5 (S2, D6 a, U30): cut lines ON PLANS (not key maps): thin and muted, 0.25 pt 8E8F8A dashed (PLAN §3); pass
# as km_cut_items(..., style=KM_CUT_PLAN); key maps keep the red R01 KM_CUT. Dash, bar and triangle sizes: design values
KM_CUT_PLAN = dict(colour="8E8F8A", lw=0.0882, dash=(1.6, 0.8), end_bar=1.6, bar_lw=0.0882, tri_h=1.2, tri_lw=0.0882,
                   text_mm=1.59, gap_mm=0.6)
KM_LOG = []


def km_cut_items(cuts, scale_den, frame=None, style=None, text_mm=None):
    """R01 cut symbols (G-R4-9) as items in survey m. cuts = [(end1, end2, (name1, name2)[, look])] (as
    basemap_cut_ids gives them: end1 = the section's left end, look +1 = the viewer stands so end1 is on the left,
    -1 the other way); scale_den: the key map's 1:scale_den (mm sizes -> m); frame: a convex polygon the symbols stay
    inside (the line is cut to it and pulled in so bars and names fit). Per cut: the dash-dot line end to end, at each
    end the bar and the open triangle pointing the look direction, the end's name beyond the bar (bold)."""
    st = dict(KM_CUT)
    st.update(style or {})
    tm = text_mm or st["text_mm"]
    m = scale_den / 1000.0                               # survey m per key-map mm
    col = st["colour"]
    out = []
    for c in cuts:
        a, b, names = c[0], c[1], c[2]
        look = c[3] if len(c) > 3 else 1
        L0 = _km_m.hypot(b[0] - a[0], b[1] - a[1])
        if L0 < 1e-6:
            continue
        ux, uy = (b[0] - a[0]) / L0, (b[1] - a[1]) / L0
        if frame:
            ab = _bm_clip_convex(a, b, frame)
            if ab is None:
                continue
            a, b = ab
            pull = (st["gap_mm"] + tm * 0.6 * max(len(names[0]), len(names[1]), 1)) * m
            L = _km_m.hypot(b[0] - a[0], b[1] - a[1])
            if L <= 2.0 * pull + 2.0 * st["end_bar"] * m:   # 2 Nov fix: too short for its end names: no longer
                n0 = names[0]                                 # dropped; drawn without them, its first name beside
                names = (u"", u"")                            # the middle (km_map's id label goes on the other side)
                pull = st["gap_mm"] * m
                mx_, my_ = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
                if L <= 2.0 * pull + 2.0 * st["end_bar"] * m:   # shorter than the symbol: its least length, centred
                    hl = pull + st["end_bar"] * m + 0.5 * m
                    a, b = (mx_ - ux * hl, my_ - uy * hl), (mx_ + ux * hl, my_ + uy * hl)
                if n0:
                    off_ = tm * 1.2 * m
                    out.append(("text", n0, (mx_ + uy * off_, my_ - ux * off_), tm, col, True, "MC"))
            a = (a[0] + ux * pull, a[1] + uy * pull)
            b = (b[0] - ux * pull, b[1] - uy * pull)
        fx, fy = -uy * look, ux * look                   # the way the section looks
        out.append(("line", [a, b], col, st["lw"], list(st["dash"]), 1.0))
        bar, th = st["end_bar"] * m, st["tri_h"] * m
        for p, nm, sgn in ((a, names[0], -1.0), (b, names[1], 1.0)):
            q = (p[0] - ux * sgn * bar, p[1] - uy * sgn * bar)          # the bar runs from the end inward
            out.append(("line", [p, q], col, st["bar_lw"], None, 1.0))
            mid = ((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0)
            tri = [p, q, (mid[0] + fx * th, mid[1] + fy * th), p]
            out.append(("line", tri, col, st["tri_lw"], None, 1.0))      # open triangle standing on the bar
            off = (st["gap_mm"] + tm * 0.3 * max(1, len(nm))) * m     # beyond the end, clear of the bar
            t = (p[0] + ux * sgn * off, p[1] + uy * sgn * off)
            if nm:
                out.append(("text", nm, t, tm, col, True, "MC"))
    return out


def _km_box_hit(b, boxes, pad=0.0):
    for o in boxes:
        if not (b[2] + pad <= o[0] or b[0] - pad >= o[2] or b[3] + pad <= o[1] or b[1] - pad >= o[3]):
            return True
    return False


def _km_seg_hit(b, segs, pad):
    x0, y0, x1, y1 = b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad
    for p, q in segs:
        L = _km_m.hypot(q[0] - p[0], q[1] - p[1])
        n = max(1, int(L / 0.4))
        for i in range(n + 1):
            x, y = p[0] + (q[0] - p[0]) * i / n, p[1] + (q[1] - p[1]) * i / n
            if x0 <= x <= x1 and y0 <= y <= y1:
                return True
    return False


def _km_axis_deg(P):
    """round 5 (S2): the direction (degrees, counter-clockwise from east) of the long axis of points P (principal
    axis of their spread); 0.0 when P has fewer than 3 points"""
    if len(P) < 3:
        return 0.0
    mx, my = sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
    sxx = sum((p[0] - mx) ** 2 for p in P)
    syy = sum((p[1] - my) ** 2 for p in P)
    sxy = sum((p[0] - mx) * (p[1] - my) for p in P)
    return _km_m.degrees(0.5 * _km_m.atan2(2.0 * sxy, sxx - syy))


def km_map(ids, w_mm=None, h_mm=None, zooms=None, page=None, names=None, legend_box=None, log=None, looks=None,
           box=None, scale_den=None, extra_names=None, D=None, margin=None, rotate=None, fit=None, pad_mm=None,
           base_mode="keymap", north=True):
    """THE key map (round 5 S2 v2: G-R5-3, D3, D6, A11; round 4 G-R4-9). Key-map mm: origin at the frame's lower-left,
    y up. ids: this page's cut ids (cut registry, levels.py) and zoom / window ids (zooms {id: polygon survey m}, else
    level_window(id)); none + page = every cut the registry draws on that page.
    Size and frame (D3 "a frame sized to the map"): with scale_den None (the usual call) the map is FITTED: w_mm /
    h_mm are the most the page offers (either may be None; both None = 80 mm wide), the scale fills that space and the
    frame is cut to the map plus pad_mm (default 1.0) and a margin (default 2 % of the content), so the map fills its
    frame; fit=False keeps the caller's w x h (map centred, round 4). scale_den given: the round 4 contract (fixed
    scale, the caller's frame or box; no turn).
    Turn (U68): rotate=None turns a fitted map so the corridor (the study area's long axis) runs along the frame's
    long side (portrait space: upright), north never pointing down; a number = that turn in degrees
    (counter-clockwise); False = north up. The north arrow shows true north (north=True: arrow only, in the freest
    corner).
    Base (U69 "just draw it like page 2"): basemap mode base_mode ("keymap" = the p02 look: green ground, houses by
    urban fabric, the stream blue, bridges), cut to the frame. Content: the study line, ONLY these cuts (R01 red,
    look direction), zoom frames, names: main streets (OpenStreetMap names by the names table's spelling,
    street_label) and the names table's key-map places (keymap_places: "at" + "km"; never a raw survey name), then
    extra_names; each placed clear of the cuts, their labels, the north arrow, legend_box and each other, else left
    out and logged. Labels are hints: km_items exports them with their anchors for the booklet to place (G-R5-12).
    Logs `keymap <page> fill=<x> rotation=<deg> cuts=<ids>` (fill = the content's box / the frame; WARNING below
    0.85 on a fitted map). Returns dict(base, study, cuts, names, items (survey m, in order), box, scale_den, T, Tinv,
    drawn, missing, label_boxes, w_mm, h_mm, study_rings, rotation_deg, north_deg, fill, frame (survey ring),
    frame_items, north (key-map mm items), labels [dict(string, kind, anchor, box, size_mm, colour, bold)], fitted,
    looks, zoom_ids, page)."""
    D = D if D is not None else basemap_load()
    log = log if log is not None else KM_LOG
    nm_st = dict(KM_NAMES)
    nm_st.update(names or {})
    pg = u"%s" % (page or u"")
    if not ids and page is not None and callable(globals().get("level_registry_all")):
        ids = [e["id"] for e in level_registry_all(str(page))]
    cuts, wins, drawn, missing, seen = [], [], [], [], set()
    win_fn = globals().get("level_window")
    for cid in ids or ():
        if zooms and cid in zooms:
            wins.append((cid, [tuple(p) for p in zooms[cid]]))
            drawn.append(cid)
            continue
        try:
            c = basemap_cut_ids([cid], looks)[0]
            ek = (round(c[0][0], 1), round(c[0][1], 1), round(c[1][0], 1), round(c[1][1], 1))
            if ek not in seen:                           # the crossings of one cut share one line
                seen.add(ek)
                cuts.append((cid, c))
            drawn.append(cid)
            continue
        except Exception:
            pass
        try:
            w = win_fn(cid) if callable(win_fn) else None
            if w:
                wins.append((cid, [tuple(p) for p in w]))
                drawn.append(cid)
                continue
        except Exception:
            pass
        missing.append(cid)
        log.append(u"WARNING %s keymap '%s' is neither a cut of the registry nor a zoom passed in: not drawn."
                   % (pg, cid))
    study = basemap_study(D)
    auto = not scale_den
    fit = auto if fit is None else (bool(fit) and auto)
    if margin is None:
        margin = 0.02 if fit else 0.06
    pad = 1.0 if pad_mm is None else float(pad_mm)
    if box is None:
        cont = [p for R in study for p in R] + [p for _, c in cuts for p in c[:2]] + [p for _, w in wins for p in w]
        if not cont:
            cont = list(basemap_extent(D) or [])
        if not cont:
            raise ValueError(u"key map %s: nothing to frame (no basemap data, no cuts)" % pg)
    else:
        cont = [(box[0], box[1]), (box[2], box[1]), (box[2], box[3]), (box[0], box[3])]
    # the turn: the corridor along the frame's long side (U68)
    if rotate is None:
        if auto:
            bx_ = _bm_bb(cont)
            ax_pts = [p for R in study for p in R if bx_[0] <= p[0] <= bx_[2] and bx_[1] <= p[1] <= bx_[3]]
            th = _km_axis_deg(ax_pts if len(ax_pts) >= 3 else cont)
            portrait = bool(w_mm and h_mm and h_mm > w_mm)
            phi = (90.0 - th) if portrait else -th
        else:
            phi = 0.0
    else:
        phi = float(rotate or 0.0)
    if _km_m.cos(_km_m.radians(phi)) < -1e-9:            # north never points down the page
        phi += 180.0
    phi = (phi + 180.0) % 360.0 - 180.0
    cph, sph = _km_m.cos(_km_m.radians(phi)), _km_m.sin(_km_m.radians(phi))
    bx0 = _bm_bb(cont)
    c0 = ((bx0[0] + bx0[2]) / 2.0, (bx0[1] + bx0[3]) / 2.0)

    def rot(p):
        dx, dy = p[0] - c0[0], p[1] - c0[1]
        return (dx * cph - dy * sph, dx * sph + dy * cph)

    def unrot(q):
        return (q[0] * cph + q[1] * sph + c0[0], -q[0] * sph + q[1] * cph + c0[1])
    rc = [rot(p) for p in cont]
    rx0, ry0, rx1, ry1 = _bm_bb(rc)
    cw, ch = max(rx1 - rx0, 1.0), max(ry1 - ry0, 1.0)  # the content, m
    d = margin * max(cw, ch)
    if fit:     # 2 Nov fix (fill warnings): margin per axis, so a long strip is not padded by its length across
        bw, bh = cw * (1.0 + 2.0 * margin), ch * (1.0 + 2.0 * margin)
    else:
        bw, bh = cw + 2.0 * d, ch + 2.0 * d
    if fit:
        if not w_mm and not h_mm:
            w_mm = 80.0
        dens = []
        if w_mm:
            dens.append(bw * 1000.0 / max(1.0, w_mm - 2.0 * pad))
        if h_mm:
            dens.append(bh * 1000.0 / max(1.0, h_mm - 2.0 * pad))
        den = max(dens)
        w_mm, h_mm = bw * 1000.0 / den + 2.0 * pad, bh * 1000.0 / den + 2.0 * pad
    elif scale_den and (w_mm is None or h_mm is None):   # a fixed scale: the key map is the box at that scale
        den = float(scale_den)
        w_mm, h_mm = bw * 1000.0 / den, bh * 1000.0 / den
    else:
        den = float(scale_den) if scale_den else max(bw * 1000.0 / w_mm, bh * 1000.0 / h_mm)
    s = 1000.0 / den
    rcx, rcy = (rx0 + rx1) / 2.0, (ry0 + ry1) / 2.0

    def T(p):
        r = rot(p)
        return ((r[0] - rcx) * s + w_mm / 2.0, (r[1] - rcy) * s + h_mm / 2.0)

    def Tinv(q):
        return unrot(((q[0] - w_mm / 2.0) / s + rcx, (q[1] - h_mm / 2.0) / s + rcy))
    frame = [Tinv((0.0, 0.0)), Tinv((w_mm, 0.0)), Tinv((w_mm, h_mm)), Tinv((0.0, h_mm))]
    vb = _bm_bb(frame)
    if base_mode == "muted":
        base = ml_base(vb, den, D=D, crop=False) if D else []
    else:
        base = basemap_items(base_mode, box=vb, D=D, scale_den=den) if D else []
    base = ml_crop(base, frame) if base else []
    if D and D.get("format") != BASEMAP_FORMAT:
        log.append(u"FLAG keymap %s: basemap format %s has no urban fabric per house: one house tone until the site "
                   u"board writes format %d" % (pg, D.get("format"), BASEMAP_FORMAT))
    st_items = ml_study_items(study)
    cut_items = []
    for cid, c in cuts:
        its = km_cut_items([c], den, frame=frame)
        nm_fn = globals().get("level_name")
        try:
            name = nm_fn(cid) if callable(nm_fn) else cid
        except Exception:
            name = cid
        name = u"%s" % name
        name = name.split("-")[0]                        # a crossing row (S5-2) is labelled by its cut (S5)
        if not its:
            log.append(u"WARNING %s keymap cut %s too short inside the frame: not drawn" % (pg, cid))
        elif name not in c[2][0] and name not in c[2][1]:   # end names that do not say the id: the id too
            a, b = c[0], c[1]
            L0 = _km_m.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
            nx, ny = -(b[1] - a[1]) / L0, (b[0] - a[0]) / L0
            q = ((a[0] + b[0]) / 2.0 + nx * KM_CUT["text_mm"] * 1.2 / s, (a[1] + b[1]) / 2.0 + ny * KM_CUT["text_mm"]
                 * 1.2 / s)
            its.append(("text", name, q, KM_CUT["text_mm"], KM_CUT["colour"], True, "MC"))
        cut_items += its
    for cid, w in wins:
        cut_items.append(("line", list(w) + [w[0]], KM_ZOOM["colour"], KM_ZOOM["lw"], None, 1.0))
        x0, y0, x1, y1 = _bm_bb([T(p) for p in w])
        cut_items.append(("text", cid, Tinv((x0 + KM_CUT["text_mm"] * 0.9, y1 + KM_CUT["text_mm"] * 0.8)),
                          KM_CUT["text_mm"], KM_CUT["colour"], True, "MC"))
    fmw = globals().get("fm_width")
    pt_of = lambda mm: mm / 0.352778
    segs, boxes, label_boxes, labels = [], [], [], []
    for it in cut_items + st_items:
        if it[0] == "line":
            P = [T(p) for p in it[1]]
            segs += list(zip(P, P[1:]))
    for it in cut_items:
        if it[0] == "text":
            x, y = T(it[2])
            w = fmw(it[1], pt_of(it[3]), bold=it[5]) if callable(fmw) else 0.6 * it[3] * len(it[1])
            b = (x - w / 2.0, y - it[3] / 2.0, x + w / 2.0, y + it[3] / 2.0)
            boxes.append(b)
            label_boxes.append((it[1], b))
            labels.append(dict(string=it[1], kind="cut", anchor=(x, y), box=b, size_mm=it[3], colour=it[4],
                               bold=it[5]))
    # the north arrow: arrow only (G-R4-9), in the first free corner (top right, top left, bottom right, bottom left)
    north_its, nsz = [], 5.0
    if north:
        best = None
        # 2 Nov fix (no free corner): the corners, then along the edges (2 mm steps), at 5 / 4 / 3.2 mm; first clear
        # of every line, then clear of the cuts and labels only (the study line may pass under the arrow)
        cut_segs = []
        for it in cut_items:
            if it[0] == "line":
                P = [T(p) for p in it[1]]
                cut_segs += list(zip(P, P[1:]))
        for sg_ in (segs, cut_segs):
            for nsz_ in (5.0, 4.0, 3.2):
                h_ = 0.9 * nsz_
                xr, xl, yt, yb = w_mm - pad - h_, pad + h_, h_mm - pad - h_, pad + h_
                if xr < xl or yt < yb:
                    continue
                nx_, ny_ = int((xr - xl) / 2.0), int((yt - yb) / 2.0)
                cands = [(xr, yt), (xl, yt), (xr, yb), (xl, yb)]
                cands += [(xr - 2.0 * k, yt) for k in range(1, nx_ + 1)] + [(xr - 2.0 * k, yb) for k in range(1, nx_ + 1)]
                cands += [(xr, yt - 2.0 * k) for k in range(1, ny_ + 1)] + [(xl, yt - 2.0 * k) for k in range(1, ny_ + 1)]
                for cxn, cyn in cands:
                    nb = (cxn - h_, cyn - h_, cxn + h_, cyn + h_)
                    if not _km_seg_hit(nb, sg_, 0.3) and not _km_box_hit(nb, boxes, 0.3):
                        best = (cxn, cyn, nb)
                        break
                if best is not None:
                    if nsz_ != nsz:
                        log.append(u"keymap %s north arrow at %.1f mm (no room at %.1f mm)" % (pg, nsz_, nsz))
                    nsz = nsz_
                    break
            if best is not None:
                break
        if best is None:
            cxn, cyn = w_mm - pad - 0.9 * nsz, h_mm - pad - 0.9 * nsz
            best = (cxn, cyn, (cxn - 0.9 * nsz, cyn - 0.9 * nsz, cxn + 0.9 * nsz, cyn + 0.9 * nsz))
            log.append(u"WARNING %s keymap north arrow: no free corner, set top right over the map" % pg)
        cxn, cyn, nb = best
        a = _km_m.radians(phi)
        foot = (cxn + _km_m.sin(a) * 0.5 * nsz, cyn - _km_m.cos(a) * 0.5 * nsz)    # the arrow centred on (cxn, cyn)
        north_its = north_items(foot[0], foot[1], ang_rad=a, size_mm=nsz * 0.75)
        boxes.append(nb)
    if legend_box:
        boxes.append(tuple(legend_box))
    cand = []
    stl = globals().get("street_label")
    if nm_st.get("streets"):
        for n, p, _a, _cl, _ln in basemap_street_names(vb, D, classes=tuple(nm_st["streets"]))[:4 * nm_st["n_streets"]]:
            cand.append((stl(n) if callable(stl) else n, p, "street"))
    if nm_st.get("places"):
        kp = globals().get("keymap_places")
        if callable(kp):
            for n, p, _k in kp(vb):
                cand.append((n, p, "place"))
        else:
            log.append(u"FLAG keymap %s: common/names.py not included: no place names (never a raw survey name)" % pg)
    for n, p in extra_names or ():
        cand.append((n, tuple(p), "extra"))
    if cand and not callable(fmw):
        raise RuntimeError(u"km_map needs common/font_metrics.py (round 4 S1: fm_width) included before it is "
                           u"called: text widths come from the real font only")
    sz = nm_st["size_mm"]
    pad_n = nm_st["pad_mm"]
    name_items, placed, seen_n = [], {"street": 0, "place": 0, "extra": 0}, set()
    lim = {"street": nm_st["n_streets"], "place": nm_st["n_places"], "extra": 10 ** 6}
    for n, p, kind in cand:
        if placed[kind] >= lim[kind] or n in seen_n:
            continue
        x, y = T(p)
        if not (0.0 <= x <= w_mm and 0.0 <= y <= h_mm):
            continue
        w = fmw(n, pt_of(sz), bold=nm_st["bold"])
        ok = None
        for dx, dy in ((0.0, 0.0), (0.0, sz * 1.1), (0.0, -sz * 1.1), (w / 2.0 + 1.0, 0.0), (-w / 2.0 - 1.0, 0.0),
                       (0.0, sz * 2.2), (0.0, -sz * 2.2)):
            b = (x + dx - w / 2.0, y + dy - sz / 2.0, x + dx + w / 2.0, y + dy + sz / 2.0)
            if b[0] < pad_n or b[1] < pad_n or b[2] > w_mm - pad_n or b[3] > h_mm - pad_n:
                continue
            if _km_box_hit(b, boxes, pad_n) or _km_seg_hit(b, segs, pad_n):
                continue
            ok = b
            break
        if ok is None:
            log.append(u"keymap %s: name '%s' left out (no free place)" % (pg, n))
            continue
        seen_n.add(n)
        boxes.append(ok)
        label_boxes.append((n, ok))
        placed[kind] += 1
        name_items.append(("text", n, Tinv(((ok[0] + ok[2]) / 2.0, (ok[1] + ok[3]) / 2.0)), sz, nm_st["colour"],
                           nm_st["bold"], "MC"))
        labels.append(dict(string=n, kind=kind, anchor=(x, y), box=ok, size_mm=sz, colour=nm_st["colour"],
                           bold=nm_st["bold"]))
    fill = (cw * s) * (ch * s) / max(1e-9, (w_mm - 2.0 * pad) * (h_mm - 2.0 * pad) if fit else w_mm * h_mm)
    fill = min(1.0, fill)
    rot_out = round(phi, 1)
    log.append(u"keymap %s fill=%.2f rotation=%.1f cuts=%s" % (pg, fill, rot_out,
                                                               u",".join(cid for cid, _ in cuts) or u"-"))
    if fit and fill < 0.85:
        log.append(u"WARNING %s keymap fill %.2f below 0.85 (frame %.0f x %.0f mm)" % (pg, fill, w_mm, h_mm))
    if log is not KM_LOG:
        KM_LOG.append(log[-1])
    frame_mm = [(0.0, 0.0), (w_mm, 0.0), (w_mm, h_mm), (0.0, h_mm)]
    frame_items = [("fill", [frame_mm], bm_key_col("paper"), 1.0, True),
                   ("line", frame_mm + [frame_mm[0]], KM_FRAME["colour"], KM_FRAME["lw"], None, 1.0)]
    return dict(base=base, study=st_items, cuts=cut_items, names=name_items,
                items=list(base) + st_items + cut_items + name_items, box=(vb[0], vb[1], vb[2], vb[3]), scale_den=den,
                T=T, Tinv=Tinv, drawn=drawn, missing=missing, label_boxes=label_boxes, w_mm=w_mm, h_mm=h_mm,
                study_rings=study, rotation_deg=rot_out, north_deg=rot_out, fill=fill, frame=frame,
                frame_items=frame_items, north=north_its, labels=labels, fitted=fit, looks=dict(looks or {}),
                zoom_ids=[cid for cid, _ in wins], cut_ids=[cid for cid, _ in cuts], page=page)


def km_draw(km, X, fill_fn, line_fn, text_fn, water_opts=None, page=None, log=None, frame=True):
    """draws a km_map (PLAN §3 order: paper, base, WATER, structures, the study line, the red cuts, names, then the
    frame line and the north arrow): X(q) key-map mm -> page point (e.g. lambda q: (x0 + q[0], y0 + q[1]), or a
    y-down flip). frame=False leaves out the paper, the frame line and the arrow (a caller that draws its own).
    text_fn=None draws no text (the booklet places the labels from km_items). Returns map_draw's dict."""
    T = km["T"]
    if frame:
        basemap_draw(km["frame_items"][:1], X, fill_fn, line_fn, None)
    r = map_draw(page or u"key", lambda p: X(T(p)), fill_fn, line_fn, text_fn, km["base"],
                 {"proj_marks": [it for it in km["cuts"] if it[0] != "text"],
                  "proj_labels": [it for it in km["cuts"] if it[0] == "text"] + km["names"]},
                 study=km.get("study_rings"), clip=False, log=log, water_opts=water_opts)
    if frame:
        basemap_draw(km["frame_items"][1:] + km["north"], X, fill_fn, line_fn, text_fn)
    return r


def km_items(km, page=None, item_id=None, priority=5):
    """round 5 (S2, G-R5-12; PLAN §4 item schema v1, Aras's addendum 1 Nov 22:37 point 3): the key map as items for
    the booklet: one "drawing" (layers of shapes in key-map mm, y up, origin lower-left; texts left out), one "text"
    item per label (names and cut labels, role "label", with its anchor in the drawing and the module's placement as
    hint_box), one "keymap" item (cut ids, looks, zooms, names, fill, rotation). Shapes: {"type": "poly", "rings",
    "fill", "opacity", "nonzero"} and {"type": "line", "pts", "stroke", "width_pt", "dash_pt", "opacity"}."""
    pg = page if page is not None else km.get("page")
    did = item_id or (u"keymap_%s" % (pg or u"key"))
    layers, cur = [], {"name": None}

    def layer(name):
        cur["name"] = name
        layers.append(dict(z=len(layers), name=name, shapes=[]))

    def fill_fn(rings, col, alpha, nonzero):
        if cur["name"] is None:
            layer("base")
        layers[-1]["shapes"].append(dict(type="poly", rings=[[[round(p[0], 3), round(p[1], 3)] for p in R]
                                                             for R in rings], fill=col, opacity=alpha,
                                         nonzero=bool(nonzero)))

    def line_fn(pts, col, w_mm, dash_mm, alpha):
        if cur["name"] is None:
            layer("base")
        layers[-1]["shapes"].append(dict(type="line", pts=[[round(p[0], 3), round(p[1], 3)] for p in pts],
                                         stroke=col, width_pt=round(w_mm / 0.352778, 3),
                                         dash_pt=[round(d_ / 0.352778, 3) for d_ in dash_mm] if dash_mm else None,
                                         opacity=alpha))
    T = km["T"]
    layer("paper")
    basemap_draw(km["frame_items"][:1], lambda q: q, fill_fn, line_fn, None)
    map_draw(u"%s key map" % (pg or u""), T, fill_fn, line_fn, None, km["base"],
             {"proj_marks": [it for it in km["cuts"] if it[0] != "text"]}, study=km.get("study_rings"),
             clip=False, order_fn=layer)
    layer("frame")
    basemap_draw(km["frame_items"][1:] + [it for it in km["north"] if it[0] != "text"], lambda q: q, fill_fn,
                 line_fn, None)
    layers = [L_ for L_ in layers if L_["shapes"]]
    for i, L_ in enumerate(layers):
        L_["z"] = i
    w, h = km["w_mm"], km["h_mm"]
    out = [dict(id=did, page=pg, kind="drawing", role="keymap", priority=priority, group=did, units="mm",
                axes=u"key-map mm, origin lower-left, y up", size_mm=[round(w, 2), round(h, 2)], extent=[0.0, 0.0,
                                                                                                    round(w, 2),
                                                                                                    round(h, 2)],
                scale_pref=None, scale_den=round(km["scale_den"]), scale_bar=False, north_deg=km["north_deg"],
                layers=layers, keep_areas=[[0.0, 0.0, round(w, 2), round(h, 2)]], anchors={})]
    texts = [dict(string=t[1], kind="north", anchor=t[2], box=None, size_mm=t[3], colour=t[4], bold=t[5])
             for t in km["north"] if t[0] == "text"]
    for i, lb in enumerate(km["labels"] + texts):
        out.append(dict(id=u"%s.t%d" % (did, i), page=pg, kind="text", role="label", priority=priority, group=did,
                        string=lb["string"], label_kind=lb["kind"],
                        anchor=dict(drawing=did, point=[round(lb["anchor"][0], 2), round(lb["anchor"][1], 2)]),
                        hint_box=[round(v, 2) for v in lb["box"]] if lb["box"] else None,
                        size_pt=round(lb["size_mm"] / 0.352778, 2), min_pt=4.0, bold=bool(lb["bold"]),
                        colour=lb["colour"], short_forms=[], side_list_ok=False, justify=False))
    out.append(dict(id=u"%s.km" % did, page=pg, kind="keymap", role="keymap", priority=priority, group=did,
                    drawing=did, cuts=[dict(id=c, look=km["looks"].get(c, 1)) for c in km["cut_ids"]],
                    zooms=list(km["zoom_ids"]), names=[lb["string"] for lb in km["labels"] if lb["kind"] != "cut"],
                    fill=round(km["fill"], 3), rotation_deg=km["rotation_deg"], missing=list(km["missing"])))
    return out


def km_texts(km):
    """the key map's texts in key-map mm for the page's TextPage: [(text, (x, y) centre, size_mm, bold, box)]"""
    out = []
    for it in km["cuts"] + km["names"]:
        if it[0] == "text":
            x, y = km["T"](it[2])
            box = next((b for t, b in km["label_boxes"] if t == it[1]), None)
            out.append((it[1], (x, y), it[3], it[5], box))
    return out


def north_items(x, y, ang_rad=0.0, size_mm=6.0, colour="2C2219"):
    """THE north arrow (G-R4-9, U31 U51): only the arrow and "N", no plate or box behind it, as items in page mm
    (y up): a slim filled arrowhead on a short shaft, size_mm tall, "N" above its tip; (x, y) = the shaft's foot;
    ang_rad = north's turn from page-up, counter-clockwise. Draw with basemap_draw(items, lambda p: p, ...)."""
    c, s_ = _km_m.cos(ang_rad), _km_m.sin(ang_rad)

    def R(px, py):
        return (x + px * c - py * s_, y + px * s_ + py * c)
    h = size_mm
    hw = 0.22 * h
    head = [R(0.0, h), R(-hw, 0.55 * h), R(0.0, 0.66 * h), R(hw, 0.55 * h)]
    tm = max(2.12, 0.42 * h)                             # "N" at least 6 pt
    return [("line", [R(0.0, 0.0), R(0.0, 0.62 * h)], colour, max(0.18, 0.04 * h), None, 1.0),
            ("fill", [head], colour, 1.0, True),
            ("text", u"N", R(0.0, h + 0.75 * tm), tm, colour, True, "MC")]


# ---- old names (round 3 callers; page sessions move to km_map / km_cut_items) -------------------------------------
def basemap_cut_items(cuts, scale_den, frame=None, inset_mm=3.0, tri_mm=2.6, text_mm=2.4, col=None, D=None):
    """round 3 name, now the R01 red symbol (G-R4-9): km_cut_items(cuts, scale_den, frame or the analysis frame).
    inset_mm, tri_mm and col are ignored (one symbol, one colour everywhere)."""
    return km_cut_items(cuts, scale_den, frame=frame or basemap_frame(D), text_mm=max(text_mm, 2.12))


def keymap_items(ids=(), scale_den=10000.0, box=None, zooms=None, mode="key", override=None, looks=None, D=None,
                 margin=0.06, text_mm=2.4, col=None, log=None, page=None):
    """round 3 name, now km_map at the caller's scale and box (mode, override, text_mm and col are ignored: the base is
    the muted one, the cuts R01 red): dict(items (survey m, in order), box, drawn, missing) as before"""
    km = km_map(ids, None, None, zooms=zooms, page=page, log=log, looks=looks, box=box, scale_den=scale_den, D=D,
                margin=margin, names=dict(streets=(), places=False))     # round 3 key maps had no names
    return dict(items=km["items"], box=km["box"], drawn=km["drawn"], missing=km["missing"])
# ---- M1 (revision 30 Oct 2026, H-A): ONE booklet grid and ONE set of type styles for every page ----------------------
# Page mm, A3 landscape 420 x 297, origin top-left, y DOWN (the booklet's own system). A script that draws y-up calls
# grid_flip(y) / grid_rect_up(r) for its coordinates. Every block of a page (map, section, legend, intro, key map, box)
# is placed by grid cells: a column span (c0, n) and baseline rows, never by hand-tuned mm.
#   columns   12 x 29 mm, gutters 4 mm, margins 14 mm left/right: 14 + 12 x 29 + 11 x 4 + 14 = 420
#   rows      baseline 4 mm from y = 12 (the top margin); title band 12..25, drawing area 30..273, footer from 276
#   crops     a crop the booklet shows at 1:1 is drawn GRID_W(n) wide (n whole columns), so its own sub-blocks fall on
#             the page grid when the booklet places it on a column line (grid_sub gives that sub-grid inside a crop)
# Type: GRID_TYPE (pt, bold, lead mm, colour role). Intro helper: "*word*" (or "**word**") marks the bold key words.
GRID_PAGE = (420.0, 297.0)
GRID_ML, GRID_MR, GRID_MT, GRID_MB = 14.0, 14.0, 12.0, 12.0
GRID_COLS, GRID_COL, GRID_GUT = 12, 29.0, 4.0
GRID_BASE = 4.0                                   # baseline step, from y = GRID_MT
GRID_TITLE_Y, GRID_RULE_Y = 22.0, 25.0            # title baseline, the rule under the title band
GRID_AREA = (GRID_ML, 30.0, GRID_PAGE[0] - GRID_MR, 273.0)   # where drawings go (x0, y0, x1, y1)
GRID_FOOT_RULE = 276.0
GRID_MIN_PT = 4.0                                 # no text below this size on any page, measured AFTER scaling
                                                  # (round 5 D1, Aras 1 Nov 21:26: 4 pt floor; was 6.0)
# round 5 (S1; PLAN §3 "Fonts and sizes", D1): the STARTING size of every text role the booklet composer sets (pt,
# bold, lead as a multiple of the size, colour role). The composer may step a text down to GRID_MIN_PT, never below.
# Content scripts put these sizes on their exported text items (common/item_export.py takes them from here).
GRID_ROLE_PT = dict(
    title=(16.0, True, 1.15, "ink"),              # the page title
    heading=(7.0, True, 1.25, "ink"),             # a drawing's heading
    intro=(6.0, False, 1.3, "ink"),               # the page intro / a short text block
    caption=(5.0, False, 1.3, "ink2"),            # under a drawing: what, scale
    legend=(5.0, False, 1.3, "ink"),              # legend entries
    list_item=(5.0, False, 1.3, "ink"),           # numbered / bulleted list rows
    note=(5.0, False, 1.3, "ink2"),
    source=(5.0, False, 1.3, "ink2"),
    label=(4.5, False, 1.2, "ink"),               # in-drawing labels (place names, element names)
    badge=(4.5, True, 1.2, "ink"),                # number badges on a drawing
    level_value=(4.5, False, 1.2, "ink"),         # "+43.71" beside a level marker
    pageno=(7.0, True, 1.2, "accent"),            # the page number
)

# colour roles (palette v1.4 core): ink, second ink, accent, rule
GRID_INK = dict(ink="4A3F35", ink2="6B645B", accent="8B3A3F", rule="B0AC9C", paper="FFFFFF")
# style -> (size pt, bold, lead mm, colour role)
GRID_TYPE = dict(
    page_title=(24.0, True, 10.0, "ink"),         # the page's title (booklet header)
    kicker=(8.0, True, 3.6, "accent"),            # the theme line above the title
    intro=(9.5, False, 4.0, "ink"),               # 2-3 lines, key words bold (G4)
    heading=(10.0, True, 4.0, "ink"),             # a drawing's own heading ("Pedestrian flow")
    subheading=(8.0, True, 3.6, "ink2"),
    label=(7.0, False, 3.0, "ink"),               # labels on drawings
    label_small=(6.0, False, 2.6, "ink"),         # the smallest a label may get (crowded maps)
    legend=(7.0, False, 4.0, "ink"),              # legend entries (row pitch = lead)
    legend_title=(7.0, True, 4.0, "ink"),
    caption=(7.5, False, 3.2, "ink2"),            # under a drawing: what, scale
    value=(18.0, True, 7.0, "accent"),            # a box's one headline value (G4)
    note=(7.5, False, 3.2, "ink2"),               # the one line under a value
    pageno=(14.0, True, 6.0, "accent"),
)
GRID_PT = 25.4 / 72.0                             # mm per pt


def grid_role(role):
    """(size_pt, bold, lead_mm_per_pt, hex) of a round 5 text role (GRID_ROLE_PT); unknown roles = 'note'"""
    s, b, ld, c = GRID_ROLE_PT.get(role, GRID_ROLE_PT["note"])
    return s, b, ld, GRID_INK[c]


def _grid_warn(msg):
    """round 5: a grid misfit is a WARNING line + orange message, never a stop (common/warn.py when included)"""
    g_ = globals()
    if "wn_warn" in g_:
        g_["wn_warn"](None, "grid", msg)
    elif "tp_warn" in g_:
        g_["tp_warn"](u"grid: " + msg)
    else:
        print(u"WARNING grid: " + msg)


def grid_style(name):
    """(size_pt, bold, lead_mm, hex) of a type style (GRID_TYPE)"""
    s, b, ld, role = GRID_TYPE[name]
    return s, b, ld, GRID_INK[role]


def grid_w(n):
    """width (mm) of n whole columns with their inner gutters"""
    n = max(1, int(n))
    return n * GRID_COL + (n - 1) * GRID_GUT


def grid_x(c):
    """left edge (mm) of column c (1-based; c = GRID_COLS + 1 gives the right margin line)"""
    return GRID_ML + (c - 1) * (GRID_COL + GRID_GUT)


def grid_x1(c):
    """right edge (mm) of column c"""
    return grid_x(c) + GRID_COL


def grid_span(c0, n):
    """(x, w) of the span of n columns from column c0"""
    if c0 < 1 or c0 + n - 1 > GRID_COLS:              # round 5: a WARNING, the span is kept on the grid
        _grid_warn("span %d+%d is off the %d-column grid: clamped" % (c0, n, GRID_COLS))
        c0 = min(max(1, int(c0)), GRID_COLS)
        n = max(1, min(int(n), GRID_COLS - c0 + 1))
    return grid_x(c0), grid_w(n)


def grid_cols_for(w, lo=1):
    """the fewest whole columns (>= lo) at least w mm wide (GRID_COLS when w is wider than the page)"""
    for n in range(max(1, lo), GRID_COLS + 1):
        if grid_w(n) >= w - 1e-6:
            return n
    return GRID_COLS


def grid_snap_y(y, up=True):
    """y (mm from the top) on the baseline grid: the next line at or below the point (up=True gives the line at or
    above it)"""
    import math as _m
    k = (y - GRID_MT) / GRID_BASE
    k = _m.floor(k + 1e-6) if up else _m.ceil(k - 1e-6)
    return GRID_MT + k * GRID_BASE


def grid_snap_h(h):
    """a height rounded UP to whole baseline steps"""
    import math as _m
    return GRID_BASE * _m.ceil(h / GRID_BASE - 1e-6)


def grid_rows(n):
    """the height of n baseline rows"""
    return n * GRID_BASE


def grid_cell(c0, n, y, h, snap=True):
    """the block rect (x0, y0, x1, y1) of n columns from c0, top y, height h; snap: top on the baseline (next line
    down) and the height to whole steps"""
    x, w = grid_span(c0, n)
    if snap:
        y, h = grid_snap_y(y, up=False), grid_snap_h(h)
    return (x, y, x + w, y + h)


def grid_stack(heights, c0, n, y0=None, gap=GRID_BASE):
    """blocks of the given heights stacked down one column span from y0 (default the drawing area's top), each on the
    baseline: [rect]; a stack that runs past the drawing area is a WARNING (round 5; the composer's layout check
    reports the edge hit too)"""
    y = GRID_AREA[1] if y0 is None else grid_snap_y(y0, up=False)
    out = []
    for h in heights:
        r = grid_cell(c0, n, y, h)
        out.append(r)
        y = r[3] + gap
    if out and out[-1][3] > GRID_AREA[3] + 1e-6:
        _grid_warn("stack runs %.1f mm past the drawing area" % (out[-1][3] - GRID_AREA[3]))
    return out


def grid_row(widths_cols, y, h, c0=1):
    """blocks side by side on one baseline row: widths_cols = [n columns each] from column c0: [rect]"""
    out, c = [], c0
    for n in widths_cols:
        out.append(grid_cell(c, n, y, h))
        c += n
    if c - 1 > GRID_COLS:
        _grid_warn("row needs %d columns, the grid has %d" % (c - 1, GRID_COLS))
    return out


def grid_sub(width_mm, n=None):
    """the sub-grid INSIDE a crop of width_mm (drawn to be shown at 1:1 on the page): [(x0, x1)] of its columns from
    the crop's left edge; n defaults to the whole page columns the width holds"""
    n = n or max(1, int(round((width_mm + GRID_GUT) / (GRID_COL + GRID_GUT))))
    col = (width_mm - (n - 1) * GRID_GUT) / float(n)
    return [(i * (col + GRID_GUT), i * (col + GRID_GUT) + col) for i in range(n)]


def grid_flip(y, page_h=None):
    """a top-down y (mm) as y-up (or back): page_h - y"""
    return (page_h or GRID_PAGE[1]) - y


def grid_rect_up(r, page_h=None):
    """a top-down rect (x0, y0, x1, y1) as a y-up rect (x0, y0, x1, y1) with y0 < y1"""
    H = page_h or GRID_PAGE[1]
    return (r[0], H - r[3], r[2], H - r[1])


def grid_page_counter(n, total=None):
    """the page number, bottom right: the current page only, "17" (round 3, G2 / U20: no "NN/total"; total is
    accepted and ignored so older callers keep working)"""
    return "%d" % int(n)


# ------------------------------------------------------------------------------------------- intro with bold runs
def grid_marked_runs(text):
    """marked text -> runs [(s, bold)]: "*word*" or "**words**" are bold key words, the rest regular. An unpaired
    star is printed as it is."""
    import re as _re
    out = []
    pos = 0
    for m in _re.finditer(r"\*\*(.+?)\*\*|\*(?!\s)([^*]+?)\*", text):
        if m.start() > pos:
            out.append((text[pos:m.start()], False))
        out.append((m.group(1) if m.group(1) is not None else m.group(2), True))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], False))
    return [(s, b) for s, b in out if s]


def grid_plain(text):
    """marked text without its marks (for measuring or logging)"""
    return "".join(s for s, _ in grid_marked_runs(text))


def grid_wrap_runs(runs, width_mm, size_pt, measure):
    """runs wrapped to width_mm: lines of [(s, bold, x_offset_mm)]. measure(s, size_pt, bold) -> mm. Words keep their
    own weight; a bold run is never split from its following punctuation."""
    words = []                                    # [word, bold, space_before]
    sp_next = False
    for s, b in runs:
        for ch in s:
            if ch.isspace():
                sp_next = True
            elif words and not sp_next and words[-1][1] == b:
                words[-1][0] += ch
            else:
                words.append([ch, b, bool(words) and sp_next])
                sp_next = False
    lines, cur, x = [], [], 0.0
    for w, b, sp in words:
        gap = measure(" ", size_pt, False) if (sp and cur) else 0.0
        ww = measure(w, size_pt, b)
        if cur and x + gap + ww > width_mm + 1e-6 and sp:
            lines.append(cur)
            cur, x, gap = [], 0.0, 0.0
        if cur and not sp:                       # glued (e.g. "word," after a bold run): no space
            gap = 0.0
        cur.append((w, b, x + gap))
        x += gap + ww
    if cur:
        lines.append(cur)
    out = []                                      # merge neighbouring words of one weight into one run
    for ln in lines:
        m = []
        for w, b, xo in ln:
            if m and m[-1][1] == b:
                m[-1] = (m[-1][0] + (" " if xo > m[-1][3] + 1e-6 else "") + w, b, m[-1][2], xo + measure(w, size_pt, b))
            else:
                m.append((w, b, xo, xo + measure(w, size_pt, b)))
        out.append([(s, b, xo) for s, b, xo, _ in m])
    return out


def grid_intro(text, width_mm, measure, max_lines=3, style="intro", min_pt=8.0, log=None):
    """the page intro (G4: 2-3 lines, key words bold): marked text -> (lines, size_pt, lead_mm, hex). lines =
    [[(s, bold, x_offset_mm)]]. The size steps down by 0.5 pt (not below min_pt) until it fits max_lines; text that
    still does not fit keeps its lines and a WARNING goes to log (shorten it: the rule is 3 lines)."""
    size, _, lead, col = grid_style(style)
    runs = grid_marked_runs(text)
    s = size
    while True:
        lines = grid_wrap_runs(runs, width_mm, s, measure)
        if len(lines) <= max_lines or s - 0.5 < min_pt - 1e-6:
            break
        s -= 0.5
    if len(lines) > max_lines and log is not None:
        log.append(u"WARNING: intro longer than %d lines at %.1f pt (%d lines): %s" % (
            max_lines, s, len(lines), grid_plain(text)[:60]))
    return lines, s, lead * s / size, col


def grid_text_runs(lines, x, y, lead, y_down=True):
    """intro lines placed: [(s, x_mm, baseline_y_mm, bold)] from the first baseline (x, y); y_down=False for y-up
    pages (lines go to smaller y)"""
    out = []
    for i, ln in enumerate(lines):
        yy = y + i * lead if y_down else y - i * lead
        for s, b, xo in ln:
            out.append((s, x + xo, yy, b))
    return out
# ---- M11 (revision 30 Oct 2026, H-A): the building renderer, plan / axonometric / section ---------------------------
# G7 "buildings look like buildings": plan = the footprint outline + a roof reading (ridge and hips, or fall-line
# hatch), never loose stripes; axonometric = light volumes with roofs (idea R09); section = profiles with their real
# heights in m, roofs and openings. Also the merge that fixes the fake parcel division lines AT THE SOURCE (bld_merge,
# called by the site board's build_site and by basemap_export): pieces of one footprint that share an edge become ONE
# outline, so no survey tick, party-wall split or Voronoi cut is ever drawn as a line.
# Geometry: survey m in, items out in the basemap item format (common/basemap.py head):
#   ("fill", rings, hex, alpha, nonzero)   ("line", pts, hex, width_mm, dash_mm, alpha)
#   ("text", s, (x, y), size_mm, hex, bold, align)
# plan items are in survey m (draw them with basemap_draw and the map's T); axo items are already projected (the
# caller's proj); section items are in (s, z) m along the cut (the caller's section transform).
# A unit (building) is either a site board unit (parts, holes, h, floors) or a basemap building (rings, np, h, floors).
# Roof form: the survey records no roof shapes, so the plan and axo read every pitched building as a hipped tile roof
# at BLD_PITCH (the common Bergama roof; a drawing convention, never printed as data); a unit flagged roof="flat" (or
# with h >= BLD_FLAT_H) is drawn flat with a parapet.
BLD_PITCH = 30.0                    # degrees, hipped tile roofs (drawing convention)
BLD_FLAT_H = 1e9                    # m: units at or above this height drawn flat (off: no survey of roof forms)
BLD_STOREY = 3.0                    # m per storey where a unit gives no floor count
BLD_COL = dict(fill="ECE9E3", edge="7D756C", roof="A39A90", her_fill="EEDCDB", her_edge="AF7474",
               wall_lit="F7F5F1", wall_shade="DCD8D1", roof_lit="EAE5DE", roof_shade="CFC8BE", axo_line="7D756C",
               sec_fill="EEEBE6", sec_cut="2C2219", sec_line="7D756C", opening="FFFFFF", glass="9FB3BA",
               text="4A3F35")
BLD_LW = dict(block=0.18, roof=0.07, hatch=0.05, axo=0.08, sec_cut=0.30, sec_line=0.10, glass=0.08)
BLD_MIN_ROOF_MM = 1.6               # a roof mark only where the building is at least this wide on the page
BLD_HIP_MAX_W = 12.0                # m: axo hipped roofs take at most this width's rise; wider parts get a flat top
                                    # in the middle (drawing rule, round 4 S2: merged blocks never one giant roof)
BLD_EAVE_MIN_M = 2.0                # m: axo eaves at least this far above a footprint's highest corner (drawing rule)


# ------------------------------------------------------------------------------------------- small geometry
def _bld_area(P):
    n = len(P)
    return 0.5 * sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n))


def _bld_pip(x, y, P):
    c, n = False, len(P)
    j = n - 1
    for i in range(n):
        xi, yi, xj, yj = P[i][0], P[i][1], P[j][0], P[j][1]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
            c = not c
        j = i
    return c


def _bld_bb(P):
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return min(xs), min(ys), max(xs), max(ys)


def _bld_inner(P):
    """a point strictly inside polygon P (its centroid when inside, else the middle of the first span of a scan
    line through it)"""
    A = _bld_area(P)
    n = len(P)
    if abs(A) > 1e-9:
        cx = sum((P[i][0] + P[(i + 1) % n][0]) * (P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1])
                 for i in range(n)) / (6.0 * A)
        cy = sum((P[i][1] + P[(i + 1) % n][1]) * (P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1])
                 for i in range(n)) / (6.0 * A)
        if _bld_pip(cx, cy, P):
            return cx, cy
    else:
        cy = sum(p[1] for p in P) / float(n)
    b = _bld_bb(P)
    for f in (0.5, 0.37, 0.63, 0.25, 0.75, 0.1, 0.9):
        y = b[1] + (b[3] - b[1]) * f
        xs = []
        for i in range(n):
            a, c = P[i], P[(i + 1) % n]
            if (a[1] > y) != (c[1] > y):
                xs.append(a[0] + (y - a[1]) * (c[0] - a[0]) / (c[1] - a[1]))
        xs.sort()
        if len(xs) >= 2 and xs[1] - xs[0] > 1e-6:
            return (xs[0] + xs[1]) / 2.0, y
    return P[0][0], P[0][1]


def _bld_unit(u):
    """(outlines, holes) of a site board unit or a basemap building"""
    if "parts" in u:
        return list(u["parts"]), list(u.get("holes") or [])
    R = u.get("rings") or []
    k = u.get("np", len(R))
    return list(R[:k]), list(R[k:])


def _bld_her(u):
    """a heritage building (basemap flag her, or a site board unit of fabric monument / sacred)"""
    return bool(u.get("her")) or u.get("fabric") in ("monument", "sacred")


def _bld_h(u):
    h = u.get("h")
    if h:
        return float(h)
    f = u.get("floors") or 1
    return BLD_STOREY * f


# ------------------------------------------------------------------------------------------- merge (G7 at the source)
def bld_merge(rings, holes=(), tol=0.03):
    """the outlines of pieces merged where they share an edge (also along part of an edge: T-junctions are split
    first), by cancelling every edge two pieces share: [(outline ccw, [holes cw])]. tol (m): points this close are
    one point. Pieces that only overlap (no shared edge) stay as they are."""
    import math as _m
    pts, grid = [], {}

    def vid(p):
        kx, ky = int(_m.floor(p[0] / tol)), int(_m.floor(p[1] / tol))
        for i in (kx - 1, kx, kx + 1):
            for j in (ky - 1, ky, ky + 1):
                for k in grid.get((i, j), ()):
                    q = pts[k]
                    if abs(q[0] - p[0]) <= tol and abs(q[1] - p[1]) <= tol:
                        return k
        pts.append((float(p[0]), float(p[1])))
        grid.setdefault((kx, ky), []).append(len(pts) - 1)
        return len(pts) - 1
    loops = []
    for R in rings:
        if len(R) >= 3:
            loops.append(list(R) if _bld_area(R) > 0 else list(R)[::-1])
    for H in holes:
        if len(H) >= 3:
            loops.append(list(H) if _bld_area(H) < 0 else list(H)[::-1])
    edges = []
    for R in loops:
        ids = [vid(p) for p in R]
        ids = [k for i, k in enumerate(ids) if k != ids[i - 1]] if len(ids) > 1 else ids
        for i in range(len(ids)):
            a, b = ids[i], ids[(i + 1) % len(ids)]
            if a != b:
                edges.append((a, b))
    C = 5.0                                              # T-junctions: points lying on another piece's edge
    vg = {}
    for k, p in enumerate(pts):
        vg.setdefault((int(_m.floor(p[0] / C)), int(_m.floor(p[1] / C))), []).append(k)
    cnt = {}
    for a, b in edges:
        pa, pb = pts[a], pts[b]
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]
        L2 = dx * dx + dy * dy
        cand = []
        if L2 > (2.0 * tol) ** 2:
            Ln = _m.sqrt(L2)
            for i in range(int(_m.floor((min(pa[0], pb[0]) - tol) / C)), int(_m.floor((max(pa[0], pb[0]) + tol) / C)) + 1):
                for j in range(int(_m.floor((min(pa[1], pb[1]) - tol) / C)),
                               int(_m.floor((max(pa[1], pb[1]) + tol) / C)) + 1):
                    for k in vg.get((i, j), ()):
                        if k == a or k == b:
                            continue
                        p = pts[k]
                        t = ((p[0] - pa[0]) * dx + (p[1] - pa[1]) * dy) / L2
                        if t <= 1e-6 or t >= 1.0 - 1e-6:
                            continue
                        if abs((p[0] - pa[0]) * dy - (p[1] - pa[1]) * dx) / Ln <= tol:
                            cand.append((t, k))
        seq = [a] + [k for _, k in sorted(cand)] + [b]
        for s0, s1 in zip(seq, seq[1:]):
            if s0 != s1:
                cnt[(s0, s1)] = cnt.get((s0, s1), 0) + 1
    out = {}
    keep = [e for e, c in cnt.items() if c > cnt.get((e[1], e[0]), 0)]
    for a, b in keep:
        out.setdefault(a, []).append(b)
    used, res_loops = set(), []
    for a0, b0 in keep:
        if (a0, b0) in used:
            continue
        used.add((a0, b0))
        ring, prev, cur, ok = [a0], a0, b0, False
        for _ in range(len(keep) + 1):
            if cur == a0:
                ok = True
                break
            ring.append(cur)
            nxt = [n for n in out.get(cur, ()) if (cur, n) not in used]
            if not nxt:
                break
            if len(nxt) > 1:                             # a pinch point: the sharpest right turn keeps rings simple
                ix, iy = pts[cur][0] - pts[prev][0], pts[cur][1] - pts[prev][1]
                nxt.sort(key=lambda n: _m.atan2(ix * (pts[n][1] - pts[cur][1]) - iy * (pts[n][0] - pts[cur][0]),
                                                ix * (pts[n][0] - pts[cur][0]) + iy * (pts[n][1] - pts[cur][1])))
            used.add((cur, nxt[0]))
            prev, cur = cur, nxt[0]
        if ok and len(ring) >= 3:
            res_loops.append([pts[k] for k in ring])
    clean = []
    for R in res_loops:                                  # straight-through points go
        changed = True
        while changed and len(R) > 3:
            changed = False
            for i in range(len(R)):
                p, q, r = R[i - 1], R[i], R[(i + 1) % len(R)]
                dx, dy = r[0] - p[0], r[1] - p[1]
                L = _m.hypot(dx, dy)
                if L < 1e-9:
                    continue
                if abs((q[0] - p[0]) * dy - (q[1] - p[1]) * dx) / L <= tol * 0.5 and \
                        (q[0] - p[0]) * dx + (q[1] - p[1]) * dy > 0 and (r[0] - q[0]) * dx + (r[1] - q[1]) * dy > 0:
                    del R[i]
                    changed = True
                    break
        A = _bld_area(R)
        if abs(A) >= 0.05:
            clean.append((A, R))
    outs = [[A, R, []] for A, R in clean if A > 0]
    outs.sort(key=lambda o: o[0])
    for A, R in clean:
        if A < 0:
            x, y = _bld_inner(R[::-1])
            for o in outs:                               # the smallest outline holding it
                if _bld_pip(x, y, o[1]):
                    o[2].append(R)
                    break
    return [(R, H) for _, R, H in outs]


def bld_merge_unit(parts, holes=(), tol=0.03):
    """(parts, holes) of ONE building with its pieces merged into one outline per connected piece (the survey's
    party-wall ticks, extended across the face, are not building edges). The input comes back unchanged when the
    merge would change the area by more than 1 % (a piece overlapping another)."""
    A0 = sum(abs(_bld_area(P)) for P in parts) - sum(abs(_bld_area(H)) for H in holes)
    if len(parts) < 2 and not holes:
        return list(parts), list(holes)
    try:
        res = bld_merge(parts, holes, tol)
    except Exception:
        return list(parts), list(holes)
    A1 = sum(_bld_area(o) + sum(_bld_area(h) for h in hs) for o, hs in res)
    if not res or abs(A1 - A0) > 0.01 * max(A0, 1.0):
        return list(parts), list(holes)
    return [o for o, _ in res], [h for _, hs in res for h in hs]


def bld_blocks(units, tol=0.03):
    """the blocks: buildings that share a wall merged into ONE outline (the plan's outline layer; no party walls
    drawn as lines): [dict(outer, holes, units=[index], h=max height m)]. A block whose merged area exceeds its
    buildings' (a failed merge) falls back to its buildings' own outlines."""
    rings, holes = [], []
    for u in units:
        P_, H_ = _bld_unit(u)
        rings += P_
        holes += H_
    res = bld_merge(rings, holes, tol) if rings else []
    cells = {}
    C = 40.0
    for bi, (o, hs) in enumerate(res):
        b = _bld_bb(o)
        for i in range(int(b[0] // C), int(b[2] // C) + 1):
            for j in range(int(b[1] // C), int(b[3] // C) + 1):
                cells.setdefault((i, j), []).append(bi)
    members = {}
    lone = []
    for i, u in enumerate(units):
        P_, _ = _bld_unit(u)
        if not P_:
            continue
        P0 = max(P_, key=lambda P: abs(_bld_area(P)))
        x, y = _bld_inner(P0 if _bld_area(P0) > 0 else P0[::-1])
        hit = None
        for bi in sorted(cells.get((int(x // C), int(y // C)), ()), key=lambda k: _bld_area(res[k][0])):
            if _bld_pip(x, y, res[bi][0]):
                hit = bi
                break
        if hit is None:
            lone.append(i)
        else:
            members.setdefault(hit, []).append(i)
    out = []
    for bi, idx in members.items():
        o, hs = res[bi]
        A = _bld_area(o) + sum(_bld_area(h) for h in hs)
        A_u = sum(sum(abs(_bld_area(P)) for P in _bld_unit(units[i])[0]) -
                  sum(abs(_bld_area(H)) for H in _bld_unit(units[i])[1]) for i in idx)
        if A > 1.02 * A_u + 1.0:
            lone += idx
            continue
        out.append(dict(outer=o, holes=hs, units=sorted(idx), h=max(_bld_h(units[i]) for i in idx)))
    for i in lone:
        P_, H_ = _bld_unit(units[i])
        for P in P_:
            out.append(dict(outer=P if _bld_area(P) > 0 else P[::-1], holes=[], units=[i], h=_bld_h(units[i])))
        for k, H in enumerate(H_):
            out[-1]["holes"].append(H)
    return out


# ------------------------------------------------------------------------------------------- roof geometry
def bld_rect(P):
    """the minimum-area rectangle round P: (cx, cy, ux, uy, L, W), u along the long side (L >= W)"""
    import math as _m
    pts = sorted(set((round(p[0], 4), round(p[1], 4)) for p in P))
    if len(pts) < 3:
        return None

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, hi = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(hi) >= 2 and cross(hi[-2], hi[-1], p) <= 0:
            hi.pop()
        hi.append(p)
    hull = lo[:-1] + hi[:-1]
    best = None
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        L = _m.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        su = [p[0] * ux + p[1] * uy for p in hull]
        sv = [-p[0] * uy + p[1] * ux for p in hull]
        area = (max(su) - min(su)) * (max(sv) - min(sv))
        if best is None or area < best[0]:
            best = (area, ux, uy, min(su), max(su), min(sv), max(sv))
    if best is None:
        return None
    _, ux, uy, u0, u1, v0, v1 = best
    cu, cv = (u0 + u1) / 2.0, (v0 + v1) / 2.0
    cx, cy = cu * ux - cv * uy, cu * uy + cv * ux
    Lu, Lv = u1 - u0, v1 - v0
    if Lv > Lu:
        ux, uy, Lu, Lv = -uy, ux, Lv, Lu
    return cx, cy, ux, uy, Lu, Lv


def _bld_clip_seg(a, b, P):
    """the pieces of segment a-b inside polygon P"""
    ts = [0.0, 1.0]
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = len(P)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]
        ex, ey = q[0] - p[0], q[1] - p[1]
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((p[0] - a[0]) * ey - (p[1] - a[1]) * ex) / den
        s = ((p[0] - a[0]) * dy - (p[1] - a[1]) * dx) / den
        if 0.0 < t < 1.0 and -1e-9 <= s <= 1.0 + 1e-9:
            ts.append(t)
    ts.sort()
    out = []
    for t0, t1 in zip(ts, ts[1:]):
        if t1 - t0 < 1e-6:
            continue
        tm = (t0 + t1) / 2.0
        if _bld_pip(a[0] + dx * tm, a[1] + dy * tm, P):
            out.append([(a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)])
    return out


def bld_roof_lines(P, mode="ridge", spacing=None):
    """the roof reading of one footprint P (survey m): segments [(a, b)] clipped to P. mode "ridge" = ridge + four
    hips of a hipped roof on the footprint's minimum rectangle; "hatch" = the same plus fall lines across the long
    planes every `spacing` m; "flat" = a parapet line inset 0.4 m; "none" = []"""
    if mode == "none":
        return []
    r = bld_rect(P)
    if r is None:
        return []
    cx, cy, ux, uy, L, W = r
    vx, vy = -uy, ux
    out = []
    if mode == "flat":
        k = 0.4
        if W > 2.5 * k:
            Q = [(cx + ux * su * (L / 2 - k) + vx * sv * (W / 2 - k), cy + uy * su * (L / 2 - k) + vy * sv * (W / 2 - k))
                 for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            for a, b in zip(Q, Q[1:] + Q[:1]):
                out += _bld_clip_seg(a, b, P)
        return out
    h = (L - W) / 2.0
    e1, e2 = (cx - ux * h, cy - uy * h), (cx + ux * h, cy + uy * h)
    segs = [(e1, e2)] if h > 0.05 else []
    for e, su in ((e1, -1), (e2, 1)):
        for sv in (-1, 1):
            segs.append((e, (cx + ux * su * L / 2 + vx * sv * W / 2, cy + uy * su * L / 2 + vy * sv * W / 2)))
    if mode == "hatch" and spacing and h > spacing:
        k = -h + spacing / 2.0
        while k < h:
            for sv in (-1, 1):
                a = (cx + ux * k, cy + uy * k)
                segs.append((a, (a[0] + vx * sv * W / 2, a[1] + vy * sv * W / 2)))
            k += spacing
    for a, b in segs:
        out += _bld_clip_seg(a, b, P)
    return out


def _bld_roof_mode(u, mode):
    if u.get("roof") == "flat" or _bld_h(u) >= BLD_FLAT_H:
        return "flat"
    return mode


# ------------------------------------------------------------------------------------------- plan
def bld_plan_items(units, blocks=None, scale_den=1000.0, roof="ridge", box=None, fill=None, edge=None,
                   roof_col=None, her_fill=None, her_edge=None, alpha=1.0, outline=True, hatch_mm=1.2, lw=None):
    """G7 plan: buildings as items (survey m): a light fill per building, the roof reading (ridge + hips; roof="hatch"
    adds fall lines every hatch_mm on the page; "none" leaves it out) where the building is at least BLD_MIN_ROOF_MM
    wide at 1:scale_den, and ONE outline per block (blocks: bld_blocks(units), made when not given): no line between
    buildings that share a wall. Heritage units (her=True) in their own tone. box (x0, y0, x1, y1): only what touches
    it. lw: the block outline width in mm (default BLD_LW["block"]; the round 4 muted base uses 0.12)."""
    fill, edge = fill or BLD_COL["fill"], edge or BLD_COL["edge"]
    lw_b = BLD_LW["block"] if lw is None else lw
    roof_col = roof_col or BLD_COL["roof"]
    her_fill, her_edge = her_fill or BLD_COL["her_fill"], her_edge or BLD_COL["her_edge"]
    mpm = scale_den / 1000.0                             # survey m per page mm

    def hit(P):
        if box is None:
            return True
        b = _bld_bb(P)
        return not (b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3])
    out, chunk, chunk_h, roofs = [], [], [], []
    for u in units:
        P_, H_ = _bld_unit(u)
        P_ = [P for P in P_ if len(P) >= 3 and hit(P)]
        if not P_:
            continue
        (chunk_h if _bld_her(u) else chunk).extend(P_ + H_)
        if roof != "none":
            mode = _bld_roof_mode(u, roof)
            for P in P_:
                r = bld_rect(P)
                if r is None or r[5] / mpm < BLD_MIN_ROOF_MM:
                    continue
                roofs += bld_roof_lines(P, mode, hatch_mm * mpm)
        if len(chunk) >= 300:
            out.append(("fill", chunk, fill, alpha, True))
            chunk = []
    if chunk:
        out.append(("fill", chunk, fill, alpha, True))
    if chunk_h:
        out.append(("fill", chunk_h, her_fill, alpha, True))
    for a, b in roofs:
        out.append(("line", [a, b], roof_col, BLD_LW["roof"], None, alpha))
    if outline:
        if blocks is None:
            blocks = bld_blocks(units)
        her_idx = set(i for i, u in enumerate(units) if _bld_her(u))
        for bk in blocks:
            o = bk["outer"] if "outer" in bk else bk["rings"][0]
            hs = bk.get("holes") if "outer" in bk else bk["rings"][1:]
            if len(o) < 3 or not hit(o):
                continue
            col = her_edge if bk.get("her") or (bk.get("units") and all(i in her_idx for i in bk["units"])) else edge
            for R in [o] + list(hs or []):
                out.append(("line", list(R) + [R[0]], col, lw_b, None, alpha))
    return out


# ------------------------------------------------------------------------------------------- axonometric
def _bld_mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


def bld_axo_items(units, proj, view=(-0.70711, -0.70711), ground=None, pitch=BLD_PITCH, box=None, sun=(-0.6, 0.8),
                  cols=None, lw=None, roofs=True):
    """G7 axonometric (idea R09): light volumes with roofs, as page items. proj(x, y, z) -> (X, Y) page mm (the
    caller's axonometric); view = the horizontal direction from the scene TOWARDS the viewer (survey axes), used for
    which walls show and the drawing order (far first); ground(x, y) -> terrain m (else u["z0"] or 0); sun = the
    horizontal light direction (lit walls and roof planes lighter). Round 4 (S2): ground(x, y) is read at every
    corner (walls follow the slope), eaves = lowest corner + h (>= highest + BLD_EAVE_MIN_M); every pitched part gets
    a hipped roof = the planes of its minimum rectangle clipped to the footprint (pitch of at most BLD_HIP_MAX_W,
    flat top beyond), the walls rise to the roof at gable ends; flat units and parts with a courtyard a flat top."""
    import math as _m
    C = dict(BLD_COL)
    C.update(cols or {})
    lw = lw if lw is not None else BLD_LW["axo"]
    vx, vy = view
    sn = _m.hypot(*sun) or 1.0
    sx, sy = sun[0] / sn, sun[1] / sn
    jobs = []
    for u in units:
        P_, H_ = _bld_unit(u)
        for P in P_:
            if len(P) < 3:
                continue
            if box is not None:
                b = _bld_bb(P)
                if b[2] < box[0] or b[0] > box[2] or b[3] < box[1] or b[1] > box[3]:
                    continue
            P = P if _bld_area(P) > 0 else P[::-1]
            cx, cy = _bld_inner(P)
            jobs.append((cx * vx + cy * vy, u, P, cx, cy))
    jobs.sort(key=lambda j: j[0])                         # far first
    out = []
    t_p = _m.tan(_m.radians(pitch))
    for _, u, P, cx, cy in jobs:
        # round 4 (S2, CHK-4 P12.2): every wall stands on the ground at its own corners (no floating or sunk walls on
        # a slope); the eaves are h above the lowest corner, at least BLD_EAVE_MIN_M above the highest one
        zb = [ground(p[0], p[1]) for p in P] if ground else [float(u.get("z0") or 0.0)] * len(P)
        h = _bld_h(u)
        zt = max(min(zb) + h, max(zb) + BLD_EAVE_MIN_M)
        r = bld_rect(P)
        H_u = _bld_unit(u)[1]
        holes = [H for H in H_u if len(H) >= 3 and _bld_pip(H[0][0], H[0][1], P)]
        # round 4 (S2, CHK-4 P12.2): a hipped roof on EVERY pitched part (was: only where the footprint filled 80 %
        # of its rectangle): the roof planes of its minimum rectangle clipped to the footprint; a part wider than
        # BLD_HIP_MAX_W gets the pitch of that width and a flat top in the middle (a block of several houses never
        # reads as one giant roof); parts with a courtyard keep the flat top
        pitched = roofs and _bld_roof_mode(u, "ridge") != "flat" and r is not None and not holes
        planes = []
        if pitched:
            rcx, rcy, ux, uy, L, W = r
            wx, wy = -uy, ux
            e = min(W / 2.0, BLD_HIP_MAX_W / 2.0)

            def at(su, sv):
                return (rcx + ux * su + wx * sv, rcy + uy * su + wy * sv)
            hl, hw = L / 2.0, W / 2.0
            planes = [([at(-hl, hw), at(hl, hw), at(hl - e, hw - e), at(-hl + e, hw - e)], (wx, wy)),
                      ([at(hl, -hw), at(-hl, -hw), at(-hl + e, -hw + e), at(hl - e, -hw + e)], (-wx, -wy)),
                      ([at(hl, hw), at(hl, -hw), at(hl - e, -hw + e), at(hl - e, hw - e)], (ux, uy)),
                      ([at(-hl, -hw), at(-hl, hw), at(-hl + e, hw - e), at(-hl + e, -hw + e)], (-ux, -uy))]
            if hw - e > 1e-3:
                planes.append(([at(-hl + e, -hw + e), at(hl - e, -hw + e), at(hl - e, hw - e), at(-hl + e, hw - e)],
                               None))

            def zr(x, y, _r=r):
                dx, dy = x - _r[0], y - _r[1]
                su, sv = dx * _r[2] + dy * _r[3], -dx * _r[3] + dy * _r[2]
                d = min(_r[5] / 2.0 - abs(sv), _r[4] / 2.0 - abs(su), e)
                return zt + t_p * max(0.0, d)
        else:
            def zr(x, y):
                return zt
        walls = []
        n = len(P)
        for i in range(n):
            p, q = P[i], P[(i + 1) % n]
            ex, ey = q[0] - p[0], q[1] - p[1]
            L_e = _m.hypot(ex, ey)
            if L_e < 1e-6:
                continue
            nx, ny = ey / L_e, -ex / L_e                 # outward (ccw outline)
            if nx * vx + ny * vy <= 1e-6:
                continue
            lit = nx * sx + ny * sy
            col = _bld_mix(C["wall_shade"], C["wall_lit"], max(0.0, min(1.0, 0.5 + 0.5 * lit)))
            ts = set([0.0, 1.0])                         # the wall top follows the roof (gable ends at notches)
            for pl, _nrm in planes:
                for sa, sb_ in _bld_clip_seg(p, q, pl):
                    for pt in (sa, sb_):
                        ts.add(round(((pt[0] - p[0]) * ex + (pt[1] - p[1]) * ey) / (L_e * L_e), 6))
            top = []
            for t_ in sorted(x_ for x_ in ts if -1e-9 <= x_ <= 1.0 + 1e-9):
                x_, y_ = p[0] + ex * t_, p[1] + ey * t_
                top.append(proj(x_, y_, zr(x_, y_)))
            mx, my = (p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0
            ring = [proj(p[0], p[1], zb[i]), proj(q[0], q[1], zb[(i + 1) % n])] + top[::-1]
            walls.append((mx * vx + my * vy, ring, col))
        walls.sort(key=lambda w: w[0])
        for _, ring, col in walls:
            out.append(("fill", [ring], col, 1.0, True))
            out.append(("line", ring + ring[:1], C["axo_line"], lw, None, 1.0))
        if pitched:
            rp = []
            for pl, nrm in planes:
                piece = _bld_clip_convex(P, pl)
                if len(piece) < 3 or abs(_bld_area(piece)) < 1e-4:
                    continue
                mx = sum(p_[0] for p_ in piece) / len(piece)
                my = sum(p_[1] for p_ in piece) / len(piece)
                if nrm is None:
                    col = C["roof_lit"]
                else:
                    lit = nrm[0] * sx + nrm[1] * sy
                    col = _bld_mix(C["roof_shade"], C["roof_lit"], max(0.0, min(1.0, 0.5 + 0.5 * lit)))
                rp.append((mx * vx + my * vy, [proj(x_, y_, zr(x_, y_)) for x_, y_ in piece], col))
            rp.sort(key=lambda w: w[0])
            for _, ring, col in rp:
                out.append(("fill", [ring], col, 1.0, True))
                out.append(("line", ring + ring[:1], C["axo_line"], lw, None, 1.0))
        else:
            top = [proj(p[0], p[1], zt) for p in P]
            hs = [[proj(p[0], p[1], zt) for p in H] for H in holes]
            out.append(("fill", [top] + hs, C["roof_lit"], 1.0, False))
            out.append(("line", top + top[:1], C["axo_line"], lw, None, 1.0))
    return out


def _bld_clip_convex(P, C_):
    """round 4 (S2): polygon P (any shape) clipped to the convex polygon C_ (Sutherland-Hodgman, either turn of C_)"""
    s_ = _bld_area(C_)
    sgn = 1.0 if s_ > 0 else -1.0
    out = list(P)
    m = len(C_)
    for i in range(m):
        a, b = C_[i], C_[(i + 1) % m]
        if not out:
            break

        def side(p):
            return sgn * ((b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]))
        inp, out = out, []
        for j in range(len(inp)):
            p, q = inp[j - 1], inp[j]
            sp, sq = side(p), side(q)
            if sq >= 0:
                if sp < 0:
                    t = sp / (sp - sq)
                    out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                out.append(q)
            elif sp >= 0:
                t = sp / (sp - sq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return out


# ------------------------------------------------------------------------------------------- section
def bld_section_profile(s0, s1, z0, h, floors=None, roof="gable", pitch=BLD_PITCH, depth_w=None, wall=0.3,
                        openings=True, label=False, label_mm=2.2, cols=None, lw=None, label_gap_m=1.5):
    """G7 section: ONE building cut between s0 and s1 (m along the section), ground z0 and eaves height h (m), as
    items in (s, z) m: the profile (light fill), the cut walls and floor slabs in ink with a window opening per floor
    in each cut wall (sill 0.90 m, head 2.10 m above the floor where the storey allows), the roof cut: "gable" (cut
    across the ridge: apex in the middle), "hip" (cut along the ridge: slopes of depth_w / 2 at both ends), "flat"
    (a 0.60 m parapet). label=True writes the real height "9.60 m" centred label_gap_m over the roof top (2
    decimals; run it through M2 lp_place when buildings stand close)."""
    import math as _m
    C = dict(BLD_COL)
    C.update(cols or {})
    lw = lw or BLD_LW
    if s1 < s0:
        s0, s1 = s1, s0
    w = s1 - s0
    if w <= 2.0 * wall or h <= 0.5:
        return []
    zt = z0 + h
    t = _m.tan(_m.radians(pitch))
    if roof == "flat":
        top = [(s1, zt), (s1, zt + 0.6), (s1 - wall, zt + 0.6), (s1 - wall, zt), (s0 + wall, zt), (s0 + wall, zt + 0.6),
               (s0, zt + 0.6), (s0, zt)]
        apex = zt + 0.6
    elif roof == "hip":
        run = min(w / 2.0, (depth_w or w) / 2.0)
        rise = t * run
        top = [(s1, zt), (s1 - run, zt + rise), (s0 + run, zt + rise), (s0, zt)]
        apex = zt + rise
    else:
        rise = t * w / 2.0
        top = [(s1, zt), ((s0 + s1) / 2.0, zt + rise), (s0, zt)]
        apex = zt + rise
    prof = [(s0, z0), (s1, z0)] + top
    out = [("fill", [prof], C["sec_fill"], 1.0, True)]
    nf = int(floors) if floors else max(1, int(round(h / BLD_STOREY)))
    st = h / float(nf)
    for k in range(1, nf + 1):                           # floor slabs (the top one under the roof)
        z = z0 + k * st
        out.append(("fill", [[(s0, z - 0.25), (s1, z - 0.25), (s1, z), (s0, z)]], C["sec_cut"], 1.0, True))
    for sa in (s0, s1 - wall):                           # cut walls, each storey with its window opening
        for k in range(nf):
            zf = z0 + k * st
            if openings and st >= 2.4:
                for za, zb in ((zf, zf + 0.9), (zf + 2.1, zf + st)):
                    if zb - za > 1e-3:
                        out.append(("fill", [[(sa, za), (sa + wall, za), (sa + wall, zb), (sa, zb)]], C["sec_cut"], 1.0,
                                    True))
                out.append(("line", [(sa + wall / 2.0, zf + 0.9), (sa + wall / 2.0, zf + 2.1)], C["glass"],
                            lw["glass"], None, 1.0))
            else:
                out.append(("fill", [[(sa, zf), (sa + wall, zf), (sa + wall, zf + st), (sa, zf + st)]], C["sec_cut"],
                            1.0, True))
    out.append(("line", list(top), C["sec_cut"], lw["sec_cut"], None, 1.0))
    out.append(("line", [(s0, z0), (s0, zt)], C["sec_line"], lw["sec_line"], None, 1.0))
    out.append(("line", [(s1, z0), (s1, zt)], C["sec_line"], lw["sec_line"], None, 1.0))
    if label:
        out.append(("text", u"{:.2f} m".format(h), ((s0 + s1) / 2.0, apex + label_gap_m), label_mm, C["text"], False,
                    "MC"))
    return out


def bld_section_items(a, b, units, ground=None, pitch=BLD_PITCH, label=False, openings=True, cols=None):
    """G7 section along the cut a -> b (survey m): every building the cut passes through, as bld_section_profile
    items in (s, z) m (s from a). ground(x, y) -> terrain m (else u["z0"] or 0). The roof is cut "gable" where the
    cut crosses the ridge (within 45 degrees of square to it), else "hip"; flat units flat. Heights are the units'
    own (u["h"], m)."""
    import math as _m
    L = _m.hypot(b[0] - a[0], b[1] - a[1])
    if L < 1e-6:
        return []
    dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    out = []
    for u in units:
        P_, _ = _bld_unit(u)
        for P in P_:
            bb = _bld_bb(P)
            if max(min(a[0], b[0]), bb[0]) > min(max(a[0], b[0]), bb[2]) + 1e-6 or \
                    max(min(a[1], b[1]), bb[1]) > min(max(a[1], b[1]), bb[3]) + 1e-6:
                continue
            ts = []
            n = len(P)
            for i in range(n):
                p, q = P[i], P[(i + 1) % n]
                ex, ey = q[0] - p[0], q[1] - p[1]
                den = dx * ey - dy * ex
                if abs(den) < 1e-12:
                    continue
                t = ((p[0] - a[0]) * ey - (p[1] - a[1]) * ex) / den
                s = ((p[0] - a[0]) * dy - (p[1] - a[1]) * dx) / den
                if -1e-9 <= s < 1.0 - 1e-9:
                    ts.append(t)
            ts.sort()
            r = bld_rect(P)
            across = r is None or abs(dx * r[2] + dy * r[3]) < 0.7071
            mode = _bld_roof_mode(u, "ridge")
            for t0, t1 in zip(ts[0::2], ts[1::2]):
                t0, t1 = max(0.0, t0), min(L, t1)
                if t1 - t0 < 1.0:
                    continue
                mx, my = a[0] + dx * (t0 + t1) / 2.0, a[1] + dy * (t0 + t1) / 2.0
                z0 = ground(mx, my) if ground else float(u.get("z0") or 0.0)
                out += bld_section_profile(t0, t1, z0, _bld_h(u), u.get("floors"),
                                           "flat" if mode == "flat" else ("gable" if across else "hip"), pitch,
                                           r[5] if r else None, openings=openings, label=label, cols=cols)
    return out


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

# v17 (round 4 S1 modules): the real font widths, ONE text placer (a collision RAISES), ONE marker, ONE block template
# ---- font_metrics.py (round 4, S1, 1 Nov 2026; G-R4-1, PLAN §4.1): REAL Arial widths and glyph boxes, one source -----
# Every width and text box in the scripts comes from here (the text placer text_place.py, the markers marker.py).
# It reads the same font files the sheets embed (pdf_fonts.py: arial.ttf / arialbd.ttf from the Windows font folder),
# so what is measured is what prints. A missing font RAISES FontMissing: there is no estimate fallback (CHK1_2 F2.1:
# the old Helvetica tables measured bold Ö as 600/1000 against Arial's 778, "walking hubthe busy hub").
# Needs pdf_fonts.py included before it (_pf_path, _pf_tables, _PF_FILES).
#   fm_load(bold=False, italic=False)          the font's tables (read once per run, cached)
#   fm_width(s, pt, bold=False)                -> mm   advance width of s at pt (no kerning: the sheets' PDF
#                                                      writers place glyphs by advance, so this is what prints)
#   fm_box(s, x, y, pt, bold=False, align="L", angle=0, y_down=True) -> (x0, y0, x1, y1) page mm
#                                              the box of s set with its baseline at (x, y): width = the advance
#                                              (or the ink if wider), height = the real ink of its glyphs (accents of
#                                              İ Ö Ü, the tails of ğ g y inside); angle in degrees, counter-clockwise
#                                              as seen on the page; align L / C / R at (x, y); "MC" = (x, y) is
#                                              the middle of the ink (the shape lists' middle-centre text)
#   fm_ink_box(s, pt, bold=True)               -> (x0, y0, x1, y1) mm, the visible glyph box with the pen at (0, 0)
#                                              on the baseline, y UP (for centring a glyph in a marker)
#   fm_asc_desc(pt, bold=False)                -> (ascender, descender) mm of the font (descender negative)
# Units: pt = font size in points (the em); 1 pt = 25.4 / 72 mm (FM_PT).
# Round 5 (S1, P04.7 "bazaar side ? Kale side"): a character the font has no glyph for no longer stops a run where the
# caller checks first:
#   fm_missing(s, bold=False) -> [ch]          the characters of s the font has no glyph for (blanks never count)
#   fm_safe(s, bold=False, sub=u"\u2013") -> (s2, missing)
#                                              s with each missing character replaced by sub ("–", else "-"); the
#                                              booklet composer runs every text through it at load (one WARNING each)
FM_PT = 25.4 / 72.0
_FM_CACHE = {}


class FontMissing(RuntimeError):
    pass


def fm_load(bold=False, italic=False):
    """the font tables for one style, read once per run; raises FontMissing when the font file is not there"""
    st = ("B" if bold else "") + ("I" if italic else "") or "R"
    if st not in _FM_CACHE:
        if "_pf_tables" not in globals():
            raise FontMissing("font_metrics needs common/pdf_fonts.py included before it")
        fn = _PF_FILES[st][0]
        p = _pf_path(fn)
        if not p:
            raise FontMissing("font %s not found (Windows font folder or the user's font folder): text cannot be "
                              "measured, so nothing is placed. Install Arial or copy %s there" % (fn, fn))
        with open(p, "rb") as fh:
            T = _pf_tables(fh.read())
        T["adv_c"], T["ink_c"] = {}, {}
        T["file"] = p
        _FM_CACHE[st] = T
    return _FM_CACHE[st]


def _fm_glyph(T, ch):
    """(advance, ink box or None) of one character in font units; raises when the font has no glyph for it"""
    a = T["adv_c"].get(ch)
    if a is None:
        g = T["gid"](ord(ch)) if ord(ch) <= 0xFFFF else 0
        if not g and ch not in u" ":
            raise ValueError(u"the font %s has no glyph for %r (U+%04X): use another character" % (
                T["file"], ch, ord(ch)))
        a = T["adv"][min(g, T["nhm"] - 1)]
        T["adv_c"][ch] = a
        T["ink_c"][ch] = T["glyph_box"](g) if g else None
    return a, T["ink_c"][ch]


def fm_width(s, pt, bold=False, italic=False):
    """advance width of s in mm at pt points"""
    T = fm_load(bold, italic)
    u = 0
    for ch in u"%s" % s:
        if ch in u"\r\n":
            continue
        u += _fm_glyph(T, ch)[0]
    return u * pt * FM_PT / float(T["upm"])


def fm_ink_box(s, pt, bold=True, italic=False):
    """the visible glyph box of s in mm, pen at (0, 0) on the baseline, y up: (x0, y0, x1, y1); an all-blank string
    gives its advance with zero height"""
    T = fm_load(bold, italic)
    k = pt * FM_PT / float(T["upm"])
    x, box = 0, None
    for ch in u"%s" % s:
        if ch in u"\r\n":
            continue
        a, b = _fm_glyph(T, ch)
        if b:
            r = (x + b[0], b[1], x + b[2], b[3])
            box = r if box is None else (min(box[0], r[0]), min(box[1], r[1]), max(box[2], r[2]), max(box[3], r[3]))
        x += a
    if box is None:
        return (0.0, 0.0, x * k, 0.0)
    return (box[0] * k, box[1] * k, box[2] * k, box[3] * k)


def fm_asc_desc(pt, bold=False, italic=False):
    """the font's ascender and descender (hhea) in mm at pt; descender is negative"""
    T = fm_load(bold, italic)
    k = pt * FM_PT / float(T["upm"])
    return T["asc"] * k, T["desc"] * k


def fm_box(s, x, y, pt, bold=False, align="L", angle=0.0, y_down=True, italic=False):
    """the page box (x0, y0, x1, y1) of s with its baseline at (x, y); see the module notes"""
    import math as _m
    w = fm_width(s, pt, bold, italic)
    ix0, iy0, ix1, iy1 = fm_ink_box(s, pt, bold, italic)
    a0, a1 = min(0.0, ix0), max(w, ix1)
    dx = {"L": 0.0, "C": -w / 2.0, "R": -w}.get(str(align or "L")[:1].upper(), 0.0)
    dv = 0.0
    if str(align or "").upper() in ("MC", "CM"):          # middle centre: (x, y) is the middle of the ink
        dx, dv = -w / 2.0, -(iy0 + iy1) / 2.0
    # corners in text space (along the baseline u, up from it v), then onto the page
    corners = [(a0 + dx, iy0 + dv), (a1 + dx, iy0 + dv), (a1 + dx, iy1 + dv), (a0 + dx, iy1 + dv)]
    t = _m.radians(angle or 0.0)
    c, s_ = _m.cos(t), _m.sin(t)
    sg = -1.0 if y_down else 1.0          # page y of "up"
    P = [(x + u * c - v * s_, y + sg * (u * s_ + v * c)) for u, v in corners]
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    return (min(xs), min(ys), max(xs), max(ys))


def fm_missing(s, bold=False, italic=False):
    """the characters of s the font has no glyph for"""
    T = fm_load(bold, italic)
    out = []
    for ch in u"%s" % s:
        if ch in u"\r\n\t " or ch in out:
            continue
        try:
            _fm_glyph(T, ch)
        except ValueError:
            out.append(ch)
    return out


def fm_safe(s, bold=False, sub=u"\u2013", italic=False):
    """(s with missing glyphs replaced by sub, the missing characters); sub falls back to "-" when the font lacks it"""
    miss = fm_missing(s, bold, italic)
    if not miss:
        return u"%s" % s, []
    if fm_missing(sub, bold, italic):
        sub = u"-"
    s2 = u"%s" % s
    for ch in miss:
        s2 = s2.replace(ch, sub)
    return s2, miss
# ---- warn.py (round 5, S1, 1 Nov 2026; G-R5-1, C11; PLAN §3 "Warnings"): ONE warning sink for every script -----------
# Aras 1 Nov 17:11 / 18:51: a check hit never stops the run; it is an orange Grasshopper warning plus one
# "WARNING <page> <kind> ..." log line, so one run collects every hit. Hard stops only for missing data, fonts or
# levels (raise those as before). C11 (round 4: "0 warnings" printed with a hit in the log): the count at the log's
# head is COUNTED from the finished log's WARNING lines (wn_compose), never kept as a separate number.
# Needs nothing. Include it BEFORE text_place.py: text_place then uses WN_LOG as its TP_LOG (one list, so a script that
# prints tp_log_lines() prints every warning) and routes tp_warn here.
#
#   wn_warn(page, kind, msg, log=None) -> line   one hit: "WARNING <page> <kind>: <msg>" (page / kind may be None) into
#                                                 log (default WN_LOG) + one orange message; returns the line
#   wn_orange(msg)                                the orange Grasshopper message only (no log line); capped at
#                                                 WN_ORANGE_MAX per solve, the rest summed in one message by wn_compose
#   wn_is(line) -> bool                           a WARNING line (its text, leading blanks ignored, starts "WARNING")
#   wn_compose(lines, head=()) -> [str]           the finished log: head lines, then "<n> warnings" with n = the number
#                                                 of WARNING lines found, then every WARNING line (moved, in order, so
#                                                 each is in the log ONCE), then the other lines in their order
#   wn_count(lines) -> n                          WARNING lines in lines
#   wn_reset()                                    empties WN_LOG and the orange counter (call at the start of a run)
WN_LOG = []
WN_ORANGE_MAX = 60
_WN_N = [0, 0]           # [orange messages shown this run, orange messages held back]


def _wn_gh(msg):
    try:
        ghenv.Component.AddRuntimeMessage(__import__("Grasshopper").Kernel.GH_RuntimeMessageLevel.Warning,  # noqa: F821
                                          u"%s" % msg)
    except Exception:
        pass


def wn_orange(msg):
    """one orange (Warning level) runtime message on this component; outside Grasshopper nothing"""
    if _WN_N[0] >= WN_ORANGE_MAX:
        _WN_N[1] += 1
        return
    _WN_N[0] += 1
    _wn_gh(msg)


def wn_warn(page, kind, msg, log=None):
    """one hit as a WARNING line + an orange message; the run goes on"""
    head = u" ".join(u"%s" % p for p in (page, kind) if p not in (None, u"", ""))
    line = u"WARNING " + (head + u": " if head else u"") + u"%s" % msg
    (WN_LOG if log is None else log).append(line)
    wn_orange(line[8:])
    return line


def wn_is(line):
    return (u"%s" % line).lstrip().startswith(u"WARNING")


def wn_count(lines):
    return sum(1 for ln in lines if wn_is(ln))


def wn_compose(lines, head=()):
    """the log with its warning head (see the module notes); the count equals the WARNING lines by construction"""
    flat = []
    for ln in lines:                                   # a list item may hold several lines
        flat.extend((u"%s" % ln).split(u"\n"))
    warn = [ln.strip() for ln in flat if wn_is(ln)]
    rest = [ln for ln in flat if not wn_is(ln)]
    out = list(head) + [u"%d warnings" % len(warn)] + warn
    if _WN_N[1]:
        out.append(u"(orange messages: the first %d shown on the component, %d more only here)" % (_WN_N[0], _WN_N[1]))
        _wn_gh(u"%d more warnings: see the log's head" % _WN_N[1])
    return out + [u""] + rest


def wn_reset():
    del WN_LOG[:]
    _WN_N[0] = _WN_N[1] = 0
# ---- text_place.py (round 4, S1, 1 Nov 2026; G-R4-1, G-R4-2, PLAN §4.1): ONE text placer (round 5: hits WARN) ----
# Replaces label_place.py (its lp_* names stay as shims there until the closing step, see label_place.py).
# Every printed letter of a page goes through ONE TextPage: it measures with the real font (font_metrics.py), keeps
# every box, draws everything in .emit(drawer) (no other text path), and .check() reports (round 5: WARNING lines) any
# two texts, a text and an obstacle, a text and the page edge / margins / footer zone, or two drawing blocks overlap.
# Needs, included before it: pdf_fonts.py, font_metrics.py, grid.py (GRID_MIN_PT, grid_marked_runs); warn.py optional
# (round 5: the one warning sink; without it tp_warn writes its WARNING line itself).
#
#   tp = TextPage(name, bounds, y_down=True, min_pt=None, pad=0.6, margins=None, footer_zone=None, scale=1.0,
#                 unit_mm=1.0, log=None)
#       name        the round 4 BOOKLET page id ("p13a", "p15"), used in every log line and error
#       bounds      (x0, y0, x1, y1) of the sheet / crop in page units; no text outside it (minus margins)
#       y_down      True when page y grows downward (the booklet grid), False for y-up sheets
#       min_pt      smallest PRINTED size (default GRID_MIN_PT = 6.0): pt x scale must reach it, else TextError
#       pad         clear gap (mm) every text keeps from other texts and obstacles
#       margins     (left, top, right, bottom) mm kept free inside bounds ("top" = the visual top)
#       footer_zone (x0, y0, x1, y1) page units where only role="footer" text may sit
#       scale       print factor of this sheet in the booklet (printed mm / sheet mm), for the min_pt test
#       unit_mm     mm per page unit (1.0 for mm sheets; the site board's board units differ)
#       log         a list for the log lines (default TP_LOG; tp_log_lines() empties it)
#   tp.keep(geom, kind="keep", name=None, line=None)   an obstacle no text may touch: a box (x0, y0, x1, y1), a closed
#                                                     area [(x, y) ...] or, with line=True (or kind in TP_LINE_KINDS),
#                                                     an open polyline (streets, banks, cut lines)
#   tp.block(box, name)                               a drawing block (map, section, key map, legend): blocks may touch,
#                                                     never overlap
#   tp.put(text, x, y, pt, bold=False, align="L", angle=0, name=None, role="label", colour=None, allow=(),
#          group=None, emit=True, **extra) -> box     one fixed text (title, caption, footer, scale figure, legend row);
#                                                     (x, y) = the baseline point at `align` (L / C / R; "MC" = the
#                                                     middle of the ink); angle degrees, counter-clockwise on the page;
#                                                     allow = names / kinds of keeps this text may sit on (a number
#                                                     on its own marker disc); emit=False registers text another
#                                                     writer draws (the booklet's crop text)
#   tp.para(text, x, y, w, pt, lead, bold_marks=True, name=None, bold=False, colour=None, role="para",
#           max_lines=None, min_last_words=2, allow=()) -> next baseline
#                                                     wraps with tp_wrap (real widths; "*word*" / "**word**" bold;
#                                                     "\n" breaks; last line >= 2 words, else 0.25 pt smaller once if
#                                                     that stays >= min_pt, else TextError); each run is placed at its
#                                                     measured x, so "Ulucami Önü" + " walking hub" keep their space
#   tp.place(text, anchor, positions=TP_POSITIONS, alts=(), pt=7.0, rank=0, side_list=None, bold=False,
#            colour=None, name=None, r=0.0, gap=0.8, allow=(), role="label") -> item dict
#                                                     a label beside its point: positions in reading order (E, NE, N,
#                                                     NW, W, SW, S, SE, C, or (dx, dy, align) in page units), then the
#                                                     shorter alts, then a NUMBER on the point + a row in side_list;
#                                                     never below min_pt, never dropped (round 5 order: see below;
#                                                     rings=TP_RINGS, step=0.5 pt). rank orders nothing here (callers
#                                                     place rank 0 first); kept for the interface
#   tp.check(raise_=True, log=None, blocks_in=False) -> n_items
#                                                     the collision test; one "WARNING <page> overlap|edge: ..." line
#                                                     per hit, then "overlap <page> checked n, collisions k"; raises
#                                                     only with TP_WARN_ONLY = [False]; tp.hits = [(kind, a, b)]
#   tp.emit(drawer) -> n                              drawer(item) for every text in order; item = dict(text, x, y,
#                                                     pt, size_mm, bold, align, angle, colour, role, name, extra)
#   tp.export() -> dict                               boxes in mm, y DOWN from the bounds' top-left (crop-local) for
#                                                     the booklet (BkBlocks.crop(..., text_boxes, keep))
#   TpSideList(name, row_mm=8.0)                      the numbered key rows of place(); .close(tp) numbers them in
#                                                     reading order (top row first, left to right); .rows() ->
#                                                     [(n, text)]; check() raises while a side list is open
#   tp_wrap(text, w_mm, pt, bold=False, min_last_words=2, bold_marks=True) -> [[(s, bold, x_mm)]]
#   tp_shapes(shapes, tp, name=None, allow=(), y_down=None) -> the other shapes
#                                                     registers the ("text", ...) shapes of the common modules
#                                                     (section_frame, water, basemap, figures, buildings, node, para,
#                                                     xform) in tp, which then draws them; returns the non-text shapes
#                                                     for the caller to draw as before
# Geometry helpers (moved here from label_place.py): tp_hit, tp_seg_box, tp_seg_cross, TpSegIndex, tp_reading_order.
#
# ROUND 5 (S1, 1 Nov 2026; G-R5-1, G-R5-12, C11; PLAN §3 "Warnings"): nothing here stops a run on a layout hit.
#   * tp_warn goes to common/warn.py (wn_warn) when it is included, so every hit is ONE "WARNING <page> <kind>: ..."
#     line in TP_LOG plus an orange message; kinds: overlap, edge, min_text, widow, wrap, side_list, number.
#   * check() writes one WARNING line per hit whatever raise_ says (C11: raise_=False used to log only the count, so
#     "collisions 1" and "0 warnings" could both appear); it raises only when TP_WARN_ONLY = [False] and raise_.
#     check(blocks_in=True) also tests every block against the inner bounds (the booklet composer's edge test).
#   * place() order (G-R5-12 "prevent, not just detect"): its positions, then nearby free spots on rings round the
#     anchor (TP_RINGS mm), then the shorter alts the same way, then the side list number, then smaller sizes in
#     0.5 pt steps down to min_pt; only when all fail: a WARNING and the label at its first position (never dropped).
#   * para(): a widow that 0.25 pt smaller cannot fix is a WARNING and the paragraph is set without the widow rule.
#   * emit(): a "0" number whose side list was never closed is a WARNING and is not drawn; export() checks first.
TP_LOG = WN_LOG if "WN_LOG" in globals() else []   # round 5: with warn.py included, ONE list (the warning sink)
TP_PT = 25.4 / 72.0
TP_ROW_MM = 8.0                 # reading order: anchors within this many mm of height count as one row
TP_POSITIONS = ("E", "NE", "N", "NW", "W", "SW", "S", "SE")
TP_LINE_KINDS = ("line", "edge", "street", "road", "cut", "stream", "bank", "contour", "leader")
TP_RINGS = (1.5, 3.0, 4.5, 6.0)  # round 5: mm from the anchor's own positions where place() looks for a free spot
TP_RING_STEPS = 12               # spots per ring (every 30 degrees, starting east, counter-clockwise on the page)


class TextError(RuntimeError):
    pass


TP_WARN_ONLY = [True]   # 1 Nov (Aras): check() writes hits as warnings instead of raising; [False] = raise


def tp_warn(msg, log=None):
    """1 Nov (Aras 19:33 "get this already"): a layout check that used to stop the run writes "WARNING <msg>" to
    TP_LOG (or log) and an orange Grasshopper warning, and the run goes on (TP_WARN_ONLY = [False] raises TextError
    again). Round 5: through common/warn.py when it is included (one sink, capped orange messages)."""
    if not TP_WARN_ONLY[0]:
        raise TextError(msg)
    lg = TP_LOG if log is None else log
    if "wn_warn" in globals():
        wn_warn(None, None, msg, lg)
        return
    lg.append(u"WARNING " + msg)
    try:
        ghenv.Component.AddRuntimeMessage(__import__("Grasshopper").Kernel.GH_RuntimeMessageLevel.Warning, msg)
    except Exception:
        pass


class TextCollision(TextError):
    def __init__(self, page, item, other, n=1, more=()):
        self.page, self.item, self.other, self.n, self.more = page, item, other, n, list(more)
        msg = u"text collision on %s: %s against %s" % (page, _tp_desc(item), _tp_desc(other))
        if n > 1:
            msg += u" (and %d more: %s)" % (n - 1, u"; ".join(u"%s / %s" % (_tp_desc(a), _tp_desc(b))
                                                               for a, b in self.more[:4]))
        RuntimeError.__init__(self, msg)


def _tp_desc(it):
    if it is None:
        return u"-"
    if isinstance(it, str):
        return it
    if isinstance(it, dict):
        if "text" in it:
            return u"text %r%s" % (it["text"][:40], (u" (%s)" % it["name"]) if it.get("name") else u"")
        return u"%s %s" % (it.get("kind", "obstacle"), it.get("name") or u"")
    return u"%r" % (it,)


def tp_log_lines():
    """this run's text log lines, oldest first; the list is emptied"""
    out = list(TP_LOG)
    del TP_LOG[:]
    return out


# ------------------------------------------------------------------------------------------------ geometry
def tp_hit(a, b, pad=0.0):
    """True when boxes a and b (x0, y0, x1, y1) come closer than pad"""
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def tp_seg_box(p, q, b):
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


def tp_seg_cross(p, q, r, s):
    """True when segments p-q and r-s cross (touching at a shared end point does not count)"""
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    for a in (p, q):
        for b in (r, s):
            if abs(a[0] - b[0]) < 1e-9 and abs(a[1] - b[1]) < 1e-9:
                return False
    d1, d2, d3, d4 = orient(r, s, p), orient(r, s, q), orient(p, q, r), orient(p, q, s)
    return d1 * d2 < 0 and d3 * d4 < 0


class TpSegIndex(object):
    """linework in buckets, so a box tests only the segments near it"""
    def __init__(self, polylines=(), segs=(), cell=10.0):
        self.cell, self.b = float(cell), {}
        for P in polylines:
            for a, c in zip(P, P[1:]):
                self.add(a, c)
        for a, c in segs:
            self.add(a, c)

    def add(self, a, c):
        k = self.cell
        for i in range(int(min(a[0], c[0]) // k), int(max(a[0], c[0]) // k) + 1):
            for j in range(int(min(a[1], c[1]) // k), int(max(a[1], c[1]) // k) + 1):
                self.b.setdefault((i, j), []).append((a, c))

    def near(self, box):
        k, seen, out = self.cell, set(), []
        for i in range(int(box[0] // k), int(box[2] // k) + 1):
            for j in range(int(box[1] // k), int(box[3] // k) + 1):
                for sg in self.b.get((i, j), ()):
                    if id(sg) not in seen:
                        seen.add(id(sg))
                        out.append(sg)
        return out

    def __iter__(self):
        seen = set()
        for lst in self.b.values():
            for sg in lst:
                if id(sg) not in seen:
                    seen.add(id(sg))
                    yield sg


def tp_reading_order(pts, y_down=False, row_mm=TP_ROW_MM):
    """the indexes of pts [(x, y)] in reading order: rows from the visual top down (rows row_mm high), left to right"""
    import math as _m
    if not pts:
        return []
    top = min(p[1] for p in pts) if y_down else max(p[1] for p in pts)
    row = (lambda p: int(_m.floor((p[1] - top) / row_mm))) if y_down else \
        (lambda p: int(_m.floor((top - p[1]) / row_mm)))
    return sorted(range(len(pts)), key=lambda i: (row(pts[i]), pts[i][0], i))


def _tp_in_poly(pt, P):
    x, y = pt
    inside = False
    n = len(P)
    for i in range(n):
        (x1, y1), (x2, y2) = P[i], P[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-12) + x1:
            inside = not inside
    return inside


def _tp_keep_hits(b, K, pad):
    """True when box b comes within pad of the obstacle K"""
    if not tp_hit(b, K["box"], pad):
        return False
    if K["pts"] is None:
        return True
    bb = (b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad)
    for p, q in K["segs"].near(bb):
        if tp_seg_box(p, q, bb):
            return True
    if K["line"]:
        return False
    return _tp_in_poly(((bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0), K["pts"]) or \
        _tp_in_poly(K["pts"][0], [(bb[0], bb[1]), (bb[2], bb[1]), (bb[2], bb[3]), (bb[0], bb[3])])


# ------------------------------------------------------------------------------------------------ wrapping
def _tp_units(text, bold, bold_marks):
    """the text as word units (each a list of (s, bold) pieces glued without a space); None marks a forced break"""
    runs = grid_marked_runs(text) if (bold_marks and "grid_marked_runs" in globals()) else [(text, False)]
    units, cur = [], None
    for s, b in runs:
        b = bool(b or bold)
        for ch in s:
            if ch == "\n":
                if cur:
                    units.append(cur)
                units.append(None)
                cur = None
            elif ch.isspace():
                if cur:
                    units.append(cur)
                cur = None
            elif cur is not None and cur[-1][1] == b:
                cur[-1] = (cur[-1][0] + ch, b)
            elif cur is not None:
                cur.append((ch, b))
            else:
                cur = [(ch, b)]
    if cur:
        units.append(cur)
    return units


class TpWidow(TextError):
    pass


def tp_wrap(text, w_mm, pt, bold=False, min_last_words=2, bold_marks=True):
    """text wrapped to w_mm with real widths: lines of [(s, bold, x_offset_mm)] (neighbouring words of one weight
    merged into one run). "\\n" forces a break. A word wider than w_mm raises TextError. The last line of every
    wrapped paragraph holds at least min_last_words words (words are pulled down from the line before); when that
    cannot be done, TpWidow is raised (TextPage.para then tries 0.25 pt smaller)."""
    sp_w = fm_width(u" ", pt, False)

    def uw(u):
        return sum(fm_width(s, pt, b) for s, b in u)
    paras, cur = [], []
    for u in _tp_units(text, bold, bold_marks):
        if u is None:
            paras.append(cur)
            cur = []
        else:
            cur.append(u)
    paras.append(cur)
    out = []
    for words in paras:
        if not words:
            out.append([])
            continue
        lines, ln, x = [], [], 0.0
        for u in words:
            w = uw(u)
            if w > w_mm + 1e-6:
                tp_warn(u"wrap: the word %r (%.1f mm at %.1f pt) is wider than its column (%.1f mm): it runs over" % (
                    u"".join(s for s, _ in u), w, pt, w_mm))
            if ln and x + sp_w + w > w_mm + 1e-6:
                lines.append(ln)
                ln, x = [], 0.0
            x += (sp_w if ln else 0.0) + w
            ln.append(u)
        lines.append(ln)
        if len(lines) >= 2 and min_last_words > 1:
            while len(lines[-1]) < min_last_words:
                prev = lines[-2]
                if len(prev) <= 2:
                    raise TpWidow(u"last line %r would hold fewer than %d words" % (
                        u"".join(s for s, _ in lines[-1][0]), min_last_words))
                mv = prev.pop()
                lines[-1].insert(0, mv)
                if sum(uw(u) for u in lines[-1]) + sp_w * (len(lines[-1]) - 1) > w_mm + 1e-6:
                    raise TpWidow(u"last line cannot take one more word without passing the column width")
        for ln in lines:
            row, x = [], 0.0                       # row: [text, bold, x_offset]; one run per stretch of one weight
            for i, u in enumerate(ln):
                for j, (s, b) in enumerate(u):
                    gap = (i > 0 and j == 0)
                    if row and row[-1][1] == b:
                        row[-1][0] += (u" " if gap else u"") + s
                    else:
                        row.append([s, b, x + (sp_w if gap else 0.0)])
                    x += (sp_w if gap else 0.0) + fm_width(s, pt, b)
            out.append([(s, b, xo) for s, b, xo in row])
    return out


# ------------------------------------------------------------------------------------------------ the page
class TpSideList(object):
    """the numbered key of place(): rows numbered in reading order when closed"""
    def __init__(self, name, row_mm=TP_ROW_MM):
        self.name, self.row_mm, self.entries, self.closed = name, row_mm, [], False

    def add(self, anchor, text, item):
        if self.closed:
            tp_warn(u"side_list: %s is closed: %r gets no number (place its labels before close())" % (
                self.name, u"%s" % text))
        e = dict(anchor=tuple(anchor), text=text, item=item, n=None)
        self.entries.append(e)
        return e

    def close(self, tp):
        """numbers the entries in reading order and re-measures their number boxes"""
        order = tp_reading_order([e["anchor"] for e in self.entries], tp.y_down, self.row_mm / tp.unit_mm)
        for n, j in enumerate(order, 1):
            e = self.entries[j]
            e["n"] = n
            it = e["item"]
            it["text"] = u"%d" % n
            it["box"] = tp._box(it["text"], it["x"], it["y"], it["pt"], it["bold"], it["align"], it["angle"])
        self.closed = True
        return self.rows()

    def rows(self):
        return [(e["n"], e["text"]) for e in sorted(self.entries, key=lambda e: e["n"] or 0)]


class TextPage(object):
    def __init__(self, name, bounds, y_down=True, min_pt=None, pad=0.6, margins=None, footer_zone=None, scale=1.0,
                 unit_mm=1.0, log=None):
        if not bounds or len(bounds) != 4 or bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
            raise TextError(u"TextPage %s: bounds must be (x0, y0, x1, y1)" % name)
        self.name, self.bounds, self.y_down = name, tuple(float(v) for v in bounds), bool(y_down)
        self.min_pt = float(GRID_MIN_PT if min_pt is None else min_pt)
        self.unit_mm, self.scale = float(unit_mm), float(scale)
        self.pad = pad / self.unit_mm
        m = [v / self.unit_mm for v in (margins or (0.0, 0.0, 0.0, 0.0))]
        b = self.bounds
        if self.y_down:
            self.inner = (b[0] + m[0], b[1] + m[1], b[2] - m[2], b[3] - m[3])
        else:
            self.inner = (b[0] + m[0], b[1] + m[3], b[2] - m[2], b[3] - m[1])
        self.footer_zone = tuple(footer_zone) if footer_zone else None
        self.log = log
        self.items, self.keeps, self.blocks, self.sides = [], [], [], []
        self._gid, self.checked = 0, False
        self.hits = []

    # -- measuring
    def _box(self, text, x, y, pt, bold=False, align="L", angle=0.0):
        b = fm_box(text, 0.0, 0.0, pt, bold, align, angle, self.y_down)
        u = self.unit_mm
        return (x + b[0] / u, y + b[1] / u, x + b[2] / u, y + b[3] / u)

    def _group(self):
        self._gid += 1
        return "g%d" % self._gid

    def _size_ok(self, text, pt):
        if pt * self.scale < self.min_pt - 0.005:       # 1 Nov: 6.00 pt is not under 6.0 (rounding)
            tp_warn(u"%s min_text: %r prints at %.2f pt, below the %.1f pt minimum" % (
                self.name, text[:40], pt * self.scale, self.min_pt), self.log)

    # -- registering
    def keep(self, geom, kind="keep", name=None, line=None):
        """an obstacle no text may touch (see the module notes)"""
        g = list(geom)
        if len(g) == 4 and not hasattr(g[0], "__len__"):
            K = dict(kind=kind, name=name, box=tuple(float(v) for v in g), pts=None, line=False, segs=None)
        else:
            P = [tuple(p[:2]) for p in g]
            if len(P) < 2:
                return None
            is_line = (kind in TP_LINE_KINDS) if line is None else bool(line)
            xs, ys = [p[0] for p in P], [p[1] for p in P]
            segs = list(zip(P, P[1:])) + ([] if is_line else [(P[-1], P[0])])
            K = dict(kind=kind, name=name, box=(min(xs), min(ys), max(xs), max(ys)), pts=P, line=is_line,
                     segs=TpSegIndex(segs=segs, cell=max(5.0 / self.unit_mm, 1e-6)))
        self.keeps.append(K)
        return K

    def block(self, box, name):
        """a drawing block (blocks may touch, never overlap)"""
        B = dict(kind="block", name=name, box=tuple(float(v) for v in box))
        self.blocks.append(B)
        return B["box"]

    def put(self, text, x, y, pt, bold=False, align="L", angle=0.0, name=None, role="label", colour=None, allow=(),
            group=None, emit=True, **extra):
        """one fixed text; returns its box"""
        text = u"%s" % text
        if not text.strip():
            return None
        self._size_ok(text, pt)
        it = dict(text=text, x=float(x), y=float(y), pt=float(pt), size_mm=pt * TP_PT, bold=bool(bold),
                  align=align or "L", angle=float(angle or 0.0), colour=colour, role=role, name=name,
                  allow=tuple(allow or ()), group=group or self._group(), emit=bool(emit), extra=extra)
        it["box"] = self._box(text, it["x"], it["y"], it["pt"], it["bold"], it["align"], it["angle"])
        self.items.append(it)
        self.checked = False
        return it["box"]

    def para(self, text, x, y, w, pt, lead, bold_marks=True, name=None, bold=False, colour=None, role="para",
             max_lines=None, min_last_words=2, allow=()):
        """a wrapped paragraph from the first baseline (x, y), w and lead in page units; returns the next baseline"""
        u = self.unit_mm
        size = float(pt)
        try:
            lines = tp_wrap(text, w * u, size, bold, min_last_words, bold_marks)
        except TpWidow:
            size = size - 0.25
            self._size_ok(text, size)
            try:
                lines = tp_wrap(text, w * u, size, bold, min_last_words, bold_marks)
            except TpWidow as ex:                       # round 5: a WARNING, set without the widow rule
                tp_warn(u"%s widow: %r: %s" % (self.name, text[:50], ex), self.log)
                lines = tp_wrap(text, w * u, size, bold, 1, bold_marks)
            lead = lead * size / float(pt)
        if max_lines is not None and len(lines) > max_lines:
            tp_warn(u"%s overrun: %r needs %d lines, %d allowed: shorten it" % (self.name, text[:50], len(lines),
                                                                               max_lines), self.log)
        g = self._group()
        sg = 1.0 if self.y_down else -1.0
        yy = float(y)
        for ln in lines:
            for s, b, xo in ln:
                self.put(s, x + xo / u, yy, size, b, "L", 0.0, name, role, colour, allow, g)
            yy += sg * lead
        return yy

    def _at(self, code, text, anchor, pt, bold, d):
        """(x, y, align) of a compass position code round the anchor"""
        if not isinstance(code, str):
            dx, dy, al = code
            return anchor[0] + dx, anchor[1] + dy, al
        ix0, iy0, ix1, iy1 = fm_ink_box(text, pt, bold)
        u, sg = self.unit_mm, (-1.0 if self.y_down else 1.0)
        k = 0.7071 * d
        mid = -(iy0 + iy1) / 2.0
        tab = dict(E=(d, mid, "L"), W=(-d, mid, "R"), N=(0.0, d - iy0, "C"), S=(0.0, -d - iy1, "C"),
                   NE=(k, k - iy0, "L"), NW=(-k, k - iy0, "R"), SE=(k, -k - iy1, "L"), SW=(-k, -k - iy1, "R"),
                   C=(0.0, mid, "C"))
        dx, v, al = tab[code.upper()]
        return anchor[0] + dx / u, anchor[1] + sg * v / u, al

    def _free(self, b, allow=(), group=None):
        if not (self.inner[0] <= b[0] and b[2] <= self.inner[2] and self.inner[1] <= b[1] and b[3] <= self.inner[3]):
            return False
        if self.footer_zone and tp_hit(b, self.footer_zone, 0.0):
            return False
        for it in self.items:
            if it["group"] != group and tp_hit(b, it["box"], self.pad):
                return False
        for K in self.keeps:
            if K["name"] in allow or K["kind"] in allow:
                continue
            if _tp_keep_hits(b, K, self.pad):
                return False
        return True

    def _ring_spots(self, text, anchor, pt, bold, d, rings):
        """(x, y, align) spots on rings round the anchor (round 5: the nearby free spots of G-R5-12)"""
        import math as _m
        ix0, iy0, ix1, iy1 = fm_ink_box(text, pt, bold)
        u, sg = self.unit_mm, (-1.0 if self.y_down else 1.0)
        mid = -(iy0 + iy1) / 2.0
        n = max(4, int(TP_RING_STEPS))
        for rr in rings or ():
            R_ = d + float(rr)
            for k in range(n):
                a = 2.0 * _m.pi * k / n
                dx, dv = R_ * _m.cos(a), R_ * _m.sin(a)
                al = "L" if dx > 0.3 * R_ else ("R" if dx < -0.3 * R_ else "C")
                if al == "C":                          # above / below: the ink edge, not its middle, at the ring
                    v = (dv - iy0) if dv > 0 else (dv - iy1)
                else:
                    v = dv + mid
                yield anchor[0] + dx / u, anchor[1] + sg * v / u, al

    def _try(self, t, anchor, positions, pt, bold, d, allow, rings):
        for code in positions:
            x, y, al = self._at(code, t, anchor, pt, bold, d)
            if self._free(self._box(t, x, y, pt, bold, al, 0.0), allow):
                return x, y, al
        for x, y, al in self._ring_spots(t, anchor, pt, bold, d, rings):
            if self._free(self._box(t, x, y, pt, bold, al, 0.0), allow):
                return x, y, al
        return None

    def place(self, text, anchor, positions=TP_POSITIONS, alts=(), pt=7.0, rank=0, side_list=None, bold=False,
              colour=None, name=None, r=0.0, gap=0.8, allow=(), role="label", rings=TP_RINGS, step=0.5):
        """a label beside its point (see the module notes); returns the registered item. Order (round 5): positions,
        rings, alts the same way, the side list number, then pt - step ... down to min_pt (printed), then a WARNING
        and the first position (the label is never dropped; check() names what it hits)"""
        d = float(r) * self.unit_mm + gap
        texts = [u"%s" % t for t in (text,) + tuple(alts or ())]
        self._size_ok(texts[0], pt)
        for t in texts:
            got = self._try(t, anchor, positions, pt, bold, d, allow, rings)
            if got:
                self.put(t, got[0], got[1], pt, bold, got[2], 0.0, name, role, colour, allow)
                return self.items[-1]
        if side_list is None:
            p_ = float(pt) - step
            while p_ * self.scale >= self.min_pt - 0.005:
                for t in texts:
                    got = self._try(t, anchor, positions, p_, bold, d, allow, rings)
                    if got:
                        self.put(t, got[0], got[1], p_, bold, got[2], 0.0, name, role, colour, allow)
                        return self.items[-1]
                p_ -= step
            tp_warn(u"%s overlap: label %r has no free spot round its point down to %.1f pt and no side list: set at "
                    u"its first position" % (self.name, texts[0], self.min_pt), self.log)
            x, y, al = self._at(positions[0] if positions else "E", texts[-1], anchor, pt, bold, d)
            self.put(texts[-1], x, y, pt, bold, al, 0.0, name, role, colour, allow, forced=True)
            return self.items[-1]
        x, y, al = self._at("C", u"0", anchor, pt, True, 0.0)
        self.put(u"0", x, y, pt, True, "C", 0.0, name, "number", colour, tuple(allow) + ("marker",))
        it = self.items[-1]
        if side_list not in self.sides:
            self.sides.append(side_list)
        side_list.add(anchor, u"%s" % text, it)
        return it

    # -- the test
    def check(self, raise_=True, log=None, blocks_in=False):
        """the collision test (see the module notes); returns the number of texts checked. Every hit is one
        "WARNING <page> overlap|edge: ..." line (round 5, C11: also with raise_=False); self.hits keeps them as
        (kind, a, b) for the caller's own counts"""
        lg = log if log is not None else (self.log if self.log is not None else TP_LOG)
        for sl in self.sides:
            if not sl.closed:
                tp_warn(u"%s side_list: %s was never closed (its numbers are not set)" % (self.name, sl.name), lg)
        hits = []
        I = self.items
        inn = self.inner

        def inside(b):
            return (inn[0] - 1e-6 <= b[0] and b[2] <= inn[2] + 1e-6 and inn[1] - 1e-6 <= b[1] and
                    b[3] <= inn[3] + 1e-6)
        for i, a in enumerate(I):
            b = a["box"]
            if not inside(b):
                hits.append(("edge", a, u"the page edge or its margins"))
            if self.footer_zone and a["role"] not in ("footer", "crop_word") and tp_hit(b, self.footer_zone, 0.0):
                hits.append(("edge", a, u"the footer zone"))
            for c in I[i + 1:]:
                if c["group"] != a["group"] and tp_hit(b, c["box"], self.pad):
                    hits.append(("overlap", a, c))
            for K in self.keeps:
                if K["name"] in a["allow"] or K["kind"] in a["allow"]:
                    continue
                if _tp_keep_hits(b, K, self.pad):
                    hits.append(("overlap", a, K))
        B = self.blocks
        for i, a in enumerate(B):
            if blocks_in and not inside(a["box"]):
                hits.append(("edge", a, u"the page edge or its margins"))
            for c in B[i + 1:]:
                if tp_hit(a["box"], c["box"], -0.01 / self.unit_mm):
                    hits.append(("overlap", a, c))
        self.hits = hits
        self.checked = True
        if hits and raise_ and not TP_WARN_ONLY[0]:
            raise TextCollision(self.name, hits[0][1], hits[0][2], len(hits), [h[1:] for h in hits[1:]])
        for k_, a_, b_ in hits:                          # one WARNING line each; the run goes on
            ln_ = u"WARNING %s %s: %s against %s" % (self.name, k_, _tp_desc(a_), _tp_desc(b_))
            lg.append(ln_)
        if hits:
            if "wn_orange" in globals():
                wn_orange(u"%s: %d text hits (each one in the log, 'WARNING %s ...')" % (self.name, len(hits),
                                                                                       self.name))
            else:
                try:
                    ghenv.Component.AddRuntimeMessage(                                           # noqa: F821
                        __import__("Grasshopper").Kernel.GH_RuntimeMessageLevel.Warning,
                        u"%s: %d text hits (each one in the log)" % (self.name, len(hits)))
                except Exception:
                    pass
        lg.append(u"overlap %s checked %d, collisions %d" % (self.name, len(I), len(hits)))
        return len(I)

    def emit(self, drawer):
        """draws every registered text through drawer(item); returns how many"""
        n = 0
        for it in self.items:
            if not it["emit"]:
                continue
            if it["role"] == "number" and it["text"] == u"0":
                tp_warn(u"%s number: a numbered label was never given its number (close its side list): not drawn" %
                        self.name, self.log)
                continue
            drawer(it)
            n += 1
        return n

    def export(self):
        """boxes in mm, y DOWN from the top-left of bounds (crop-local), for the booklet's assembled-page test"""
        if not self.checked:
            self.check(False)
        u, b = self.unit_mm, self.bounds

        def mm(r):
            if self.y_down:
                return ((r[0] - b[0]) * u, (r[1] - b[1]) * u, (r[2] - b[0]) * u, (r[3] - b[1]) * u)
            return ((r[0] - b[0]) * u, (b[3] - r[3]) * u, (r[2] - b[0]) * u, (b[3] - r[1]) * u)
        return dict(page=self.name, size_mm=((b[2] - b[0]) * u, (b[3] - b[1]) * u),
                    texts=[dict(box=mm(it["box"]), role=it["role"], name=it["name"], text=it["text"])
                           for it in self.items],
                    keep=[dict(box=mm(K["box"]), kind=K["kind"], name=K["name"]) for K in self.keeps],
                    blocks=[dict(box=mm(B["box"]), name=B["name"]) for B in self.blocks])


def tp_shapes(shapes, tp, name=None, allow=(), y_down=None):
    """registers the text shapes of a common module's shape list in tp (tp draws them in emit) and returns the other
    shapes. Text shape forms: ("text", s, x, y, size_mm, colour, bold, align[, mat, halo]) and
    ("text", s, (x, y), size_mm, colour, bold, align); align "MC" = (x, y) is the middle of the ink."""
    rest = []
    for s_ in shapes or ():
        if not s_ or s_[0] != "text":
            rest.append(s_)
            continue
        if isinstance(s_[2], (tuple, list)):
            x, y = s_[2][0], s_[2][1]
            tail = list(s_[3:])
        else:
            x, y = s_[2], s_[3]
            tail = list(s_[4:])
        size_mm = tail[0]
        col = tail[1] if len(tail) > 1 else None
        bold = tail[2] if len(tail) > 2 else False
        al = tail[3] if len(tail) > 3 else "L"
        extra = {}
        if len(tail) > 4 and tail[4] is not None:
            extra["mat"] = tail[4]
        if len(tail) > 5 and tail[5] is not None:
            extra["halo"] = tail[5]
        tp.put(s_[1], x, y, size_mm * tp.unit_mm / TP_PT, bold, al, 0.0, name, "shape", col, allow, **extra)
    return rest
# ---- item_export.py (round 5, S1, 1 Nov 2026; G-R5-12, PLAN §4 schema v1): content scripts EXPORT, the booklet composes
# Aras 1 Nov 22:00: "produce every text every drawing and everything and in the last run make it place it and align it
# and booklet it". A content script lays out no page and burns no page text into a drawing: it hands every drawing
# (true-scale vector geometry in draw order) and every text (role, string, anchor) to one Ix, and Ix.save() writes
# Downloads/Bergama/cached/booklet/<folder>/items.json. The booklet (bergama_booklet parts 10-70) reads every such
# file, picks scales, sets and places every text, aligns blocks and checks the page. Successor of booklet_assets.py
# (blocks.json crops); addendum 1 Nov 22:37: no per-script sheet PDFs or previews (a script may still save its single
# drawings under output/<folder>/, but the booklet reads only items.json).
# Needs, included before it: bergama_paths.py (bg_booklet), grid.py (GRID_ROLE_PT, GRID_MIN_PT); warn.py optional (the
# content checks' WARNING lines go through wn_warn when it is included).
#
# items.json = {"schema": "bergama-items/1", "script", "version", "run": "YYYY-MM-DD HH:MM", "units": "m",
#               "pages": {page_id: [item, ...]}, "sources": {key: {text, url}}, "warnings": [str]}
# page_id = the round 5 23-page id ("p13", "p19"); an item with page None goes to "any" (the booklet's PLAN.py says
# where it is shown). Common keys of every item: id (unique in the file), page, kind, role, priority (1 first ... 9),
# group (items that belong together, e.g. one section's level column, legend and texts).
#
#   ix = Ix(folder, script, version)                      folder = the script's cached/booklet/ folder name
#   D = ix.drawing(id, page, extent, scale_pref=None, units="m", dkind="plan", north_deg=None, scale_bar=True,
#                  priority=1, group=None, fit=None, title=None)
#         extent (x0, y0, x1, y1) in drawing units, y UP, the area that must show; scale_pref = allowed 1:den (default
#         SF_SCALES); units "m" = true scale; "mm" = a scale-free diagram/chart in design mm, fit = (min_f, max_f)
#   ix.layer(D, name, shapes, z=None, k=1.0, origin=(0, 0))
#         adds shapes (the common modules' tuples: poly/line/circle/image; text shapes become anchored label items)
#         to layer `name` (water.py WAT_LAYERS for sections, map_layers ML_LAYERS for maps); coordinates are mapped
#         x_d = origin_x + k * x (k = drawing units per shape unit: den / 1000 for page-mm shapes drawn at 1:den);
#         line widths, dashes stay PRINT sizes (mm in the tuples, stored as pt); z defaults to the call order.
#         Stripes (hatches) are dropped: G-R5-4.1 no hatches (one WARNING per layer)
#   ix.keep(D, geom, kind="keep", name=None)               an area (drawing units) no label may cover
#   ix.anchor(D, name, xy)                                 a named point (cut ends, hubs) other items refer to
#   ix.text(page, string, role="label", drawing=None, at=None, size_pt=None, bold=None, colour=None, short_forms=(),
#           side_list_ok=True, justify=None, positions=None, priority=5, group=None, id=None, min_pt=None) -> id
#         role: title, intro, heading, caption, legend, list_item, note, label, level_value, badge, source;
#         a label of a drawing: drawing=id, at=(x, y) in drawing units (the booklet sets it beside that point)
#   ix.legend(page, drawing, entries, title=None, id=None, group=None)
#         entries: [(swatch, text)], swatch = dict(kind="fill"|"line"|"dash"|"dot"|"image", colour, stroke,
#         width_pt, dash_pt, file); text = a string (made a legend text item) or a text id
#   ix.list(page, drawing, texts, numbered=True, anchors=None, id=None, group=None)   ordered text rows
#   ix.levels(page, drawing, levels, side="R", id=None, group=None)
#         levels = [(name, z_m)] (z on the drawing's y axis, m a.s.l. for sections); the booklet draws the level
#         markers (PLAN §3, Aras's sketch U04) and their "+43.71" values beside the drawing
#   ix.inset(page, parent, window, child, factor, id=None)   child = a drawing id of the zoom; window in parent units
#   ix.keymap(page, cuts, looks=None, names=(), zooms=(), id=None)   the key-map module (S2) draws it in the booklet
#   ix.photo(page, file, crop=None, caption=None, source=None, id=None)
#   ix.chart(page, w_mm, h_mm, shapes, id=None)            a vector chart in its own mm box (y up)
#   ix.source(key, text, url, page=None)                   a Sources page row (texts cite it as {src:key})
#   ix.warn(page, kind, msg)                               a content check hit: WARNING line + orange + "warnings"
#   ix.save() -> path                                      writes items.json (UTF-8, 3 decimals), logs nothing itself
#   ix.summary() -> str                                    "items <script>: drawings n, texts n, ... -> <path>"
IX_SCHEMA = "bergama-items/1"
IX_PT = 25.4 / 72.0
IX_KINDS = ("drawing", "text", "legend", "list", "level_column", "inset", "keymap", "photo", "chart", "source")
IX_TEXT_ROLES = ("title", "intro", "heading", "caption", "legend", "list_item", "note", "label", "level_value",
                 "badge", "source")


def _ix_r(v, nd=3):
    try:
        return round(float(v), nd)
    except Exception:
        return v


def _ix_is_pt(p):
    return isinstance(p, (list, tuple)) and len(p) >= 2 and isinstance(p[0], (int, float)) and \
        isinstance(p[1], (int, float))


class Ix(object):
    def __init__(self, folder, script, version):
        import time as _t
        self.folder, self.path = folder, None
        self.d = {"schema": IX_SCHEMA, "script": script, "version": version,
                  "run": _t.strftime("%Y-%m-%d %H:%M"), "units": "m", "pages": {}, "sources": {}, "warnings": []}
        self.ids, self._z, self._n = set(), {}, 0

    # -- bookkeeping
    def _id(self, want, kind):
        if want is None:
            self._n += 1
            want = "%s_%s_%d" % (self.folder[:12], kind[:3], self._n)
        want = u"%s" % want
        if want in self.ids:
            k = 2
            while "%s_%d" % (want, k) in self.ids:
                k += 1
            self.warn(None, "export", u"item id %r used twice: the second is %s_%d" % (want, want, k))
            want = "%s_%d" % (want, k)
        self.ids.add(want)
        return want

    def _put(self, page, item):
        self.d["pages"].setdefault(page or "any", []).append(item)
        return item

    def _item(self, page, kind, id_, role=None, priority=5, group=None, **kw):
        it = dict(id=self._id(id_, kind), page=page, kind=kind, role=role or kind, priority=int(priority),
                  group=group)
        it.update(kw)
        return self._put(page, it)

    def warn(self, page, kind, msg):
        line = u"WARNING " + u" ".join(u"%s" % p for p in (page, kind) if p) + u": %s" % msg
        if "wn_warn" in globals():
            line = wn_warn(page, kind, msg)
        self.d["warnings"].append(line)
        return line

    # -- drawings
    def drawing(self, id, page, extent, scale_pref=None, units="m", dkind="plan", north_deg=None, scale_bar=True,
                priority=1, group=None, fit=None, title=None):
        x0, y0, x1, y1 = [float(v) for v in extent]
        if x1 <= x0 or y1 <= y0:
            self.warn(page, "export", u"drawing %s has an empty extent %r" % (id, extent))
        sp = list(scale_pref) if scale_pref else (list(SF_SCALES) if "SF_SCALES" in globals() else
                                                   [200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000])
        D = self._item(page, "drawing", id, "drawing", priority, group, dkind=dkind, units=units,
                       extent=[_ix_r(x0), _ix_r(y0), _ix_r(x1), _ix_r(y1)],
                       scale_pref=None if units == "mm" else [int(v) for v in sp],
                       fit=list(fit) if fit else ([0.5, 2.0] if units == "mm" else None),
                       north_deg=north_deg, scale_bar=bool(scale_bar and units == "m"), layers=[], keep_areas=[],
                       anchors={}, title=title)
        self._z[D["id"]] = 0
        return D

    def _shape(self, s, k, o):
        """one common-module shape tuple -> a schema shape dict (None for text and unknown kinds)"""
        def P(p):
            return [_ix_r(o[0] + k * p[0]), _ix_r(o[1] + k * p[1])]
        t = s[0]
        if t == "poly":
            if s[1] and not _ix_is_pt(s[1][0]):                       # page item: rings, fill, stroke, lw, dash,
                rings = [list(r) for r in s[1]]                       # stripes, alpha
                fill, stroke = s[2], (s[3] if len(s) > 3 else None)
                lw = s[4] if len(s) > 4 else 0.0
                dash = s[5] if len(s) > 5 else None
                stripes = s[6] if len(s) > 6 else None
                alpha = s[7] if len(s) > 7 else None
            else:                                                     # shape: ring, fill, stroke, lw, alpha, holes
                rings = [list(s[1])] + [list(R) for R in (s[6] if len(s) > 6 and s[6] else ()) if len(R) >= 3]
                fill, stroke = s[2], (s[3] if len(s) > 3 else None)
                lw = s[4] if len(s) > 4 else 0.0
                alpha = s[5] if len(s) > 5 else None
                dash, stripes = None, None
            rings = [[P(p) for p in r] for r in rings if len(r) >= 3]
            if not rings:
                return None
            return dict(t="poly", rings=rings, fill=fill or None, stroke=stroke or None,
                        width_pt=_ix_r((lw or 0.0) / IX_PT), dash_pt=[_ix_r(v / IX_PT) for v in dash] if dash else None,
                        opacity=alpha, _stripes=bool(stripes))
        if t == "line":
            if len(s[1]) < 2:
                return None
            dash = s[4] if len(s) > 4 else None
            return dict(t="line", pts=[P(p) for p in s[1]], stroke=s[2], width_pt=_ix_r((s[3] or 0.0) / IX_PT),
                        dash_pt=[_ix_r(v / IX_PT) for v in dash] if dash else None, cap=s[5] if len(s) > 5 else 1)
        if t == "circle":
            return dict(t="circle", c=P((s[1], s[2])), r=_ix_r(k * s[3]), fill=s[4] or None,
                        stroke=(s[5] if len(s) > 5 else None) or None,
                        width_pt=_ix_r(((s[6] if len(s) > 6 else 0.0) or 0.0) / IX_PT))
        if t == "image":
            x, y, w, h, f = s[1:6]
            clip = s[8] if len(s) > 8 else None
            return dict(t="image", box=P((x, y)) + P((x + w, y + h)), file=f, opacity=s[6] if len(s) > 6 else None,
                        flip=bool(s[7]) if len(s) > 7 else False,
                        clip=(P(clip[:2]) + P(clip[2:4])) if clip else None)
        return None

    def layer(self, D, name, shapes, z=None, k=1.0, origin=(0.0, 0.0)):
        out, texts, hatch = [], 0, 0
        for s in shapes or ():
            if not s:
                continue
            if s[0] == "text":
                self._text_shape(D, s, k, origin)
                texts += 1
                continue
            sh = self._shape(s, float(k), origin)
            if sh is None:
                continue
            if sh.pop("_stripes", False):
                hatch += 1
            out.append(sh)
        if hatch:
            self.warn(D["page"], "hatch", u"%s layer %s: %d hatch fill(s) dropped (G-R5-4.1 solid colours only)" % (
                D["id"], name, hatch))
        if z is None:
            self._z[D["id"]] = self._z.get(D["id"], 0) + 1
            z = self._z[D["id"]]
        D["layers"].append(dict(z=z, name=name, shapes=out))
        return len(out), texts

    def _text_shape(self, D, s, k, o):
        if isinstance(s[2], (tuple, list)):
            x, y = s[2][0], s[2][1]
            tail = list(s[3:])
        else:
            x, y = s[2], s[3]
            tail = list(s[4:])
        size_mm = float(tail[0]) if tail else 2.0
        al = tail[3] if len(tail) > 3 and tail[3] else "L"
        self.text(D["page"], s[1], "label", drawing=D["id"], at=(o[0] + k * x, o[1] + k * y),
                  size_pt=size_mm / IX_PT, bold=bool(tail[2]) if len(tail) > 2 else False,
                  colour=tail[1] if len(tail) > 1 and isinstance(tail[1], str) else None,
                  positions=["=" + str(al)] + ["E", "NE", "N", "NW", "W", "SW", "S", "SE"], group=D.get("group"))

    def keep(self, D, geom, kind="keep", name=None):
        g = list(geom)
        if len(g) == 4 and not hasattr(g[0], "__len__"):
            g = [[g[0], g[1]], [g[2], g[1]], [g[2], g[3]], [g[0], g[3]]]
        D["keep_areas"].append(dict(kind=kind, name=name, pts=[[_ix_r(p[0]), _ix_r(p[1])] for p in g]))

    def anchor(self, D, name, xy):
        D["anchors"][name] = [_ix_r(xy[0]), _ix_r(xy[1])]

    # -- texts and the rest
    def text(self, page, string, role="label", drawing=None, at=None, size_pt=None, bold=None, colour=None,
             short_forms=(), side_list_ok=True, justify=None, positions=None, priority=5, group=None, id=None,
             min_pt=None):
        if role not in IX_TEXT_ROLES:
            self.warn(page, "export", u"text role %r unknown (taken as note): %r" % (role, (u"%s" % string)[:80]))
            role = "note"
        if "names_fix" in globals():                       # G-R4-11 / G-R5-11: proper names through the names table
            try:
                string = names_fix(string)                                                     # noqa: F821
            except Exception:
                pass
        if "sf_strip_widths" in globals():                 # G-R5-4.6 (S3): no width in any exported text
            string = sf_strip_widths(string, page)                                             # noqa: F821
            if not (u"%s" % string).strip():
                return None
        pt0, b0, _ld, c0 = grid_role(role) if "grid_role" in globals() else (5.0, False, 1.3, "4A3F35")
        it = self._item(page, "text", id, role, priority, group, string=u"%s" % string,
                        anchor=None if drawing is None else dict(drawing=drawing,
                                                                 pt=None if at is None else [_ix_r(at[0]),
                                                                                             _ix_r(at[1])]),
                        size_pt=_ix_r(size_pt if size_pt is not None else pt0, 2),
                        min_pt=float(min_pt if min_pt is not None else (GRID_MIN_PT if "GRID_MIN_PT" in globals()
                                                                       else 4.0)),
                        bold=b0 if bold is None else bool(bold), colour=colour or c0,
                        short_forms=[u"%s" % t for t in short_forms or ()], side_list_ok=bool(side_list_ok),
                        justify=(role in ("intro", "caption", "note", "list_item", "source")) if justify is None
                        else bool(justify), positions=list(positions) if positions else None)
        return it["id"]

    def _tid(self, page, t, role, group):
        if isinstance(t, dict) and "id" in t:
            return t["id"]
        if isinstance(t, str) and t in self.ids:
            return t
        return self.text(page, t, role, group=group)

    def legend(self, page, drawing, entries, title=None, id=None, group=None):
        ents = []
        for sw, t in entries:
            tid = self._tid(page, t, "legend", group)
            if tid is not None:                            # a text that was only a width is gone (G-R5-4.6)
                ents.append(dict(swatch=dict(sw), text=tid))
        return self._item(page, "legend", id, "legend", 3, group, drawing=drawing, entries=ents,
                          title=None if title is None else self._tid(page, title, "heading", group))["id"]

    def list(self, page, drawing, texts, numbered=True, anchors=None, id=None, group=None):
        rows = [r for r in (self._tid(page, t, "list_item", group) for t in texts) if r is not None]
        return self._item(page, "list", id, "list", 4, group, drawing=drawing, items=rows, numbered=bool(numbered),
                          anchors=[[_ix_r(a[0]), _ix_r(a[1])] if a else None for a in anchors] if anchors else None)["id"]

    def levels(self, page, drawing, levels, side="R", id=None, group=None):
        lv = [dict(name=u"%s" % n, z=_ix_r(z, 3)) for n, z in levels]
        return self._item(page, "level_column", id, "level_column", 2, group, drawing=drawing, levels=lv,
                          side=side)["id"]

    def inset(self, page, parent, window, child, factor, id=None):
        return self._item(page, "inset", id, "inset", 2, None, parent=parent, window=[_ix_r(v) for v in window],
                          child=child, factor=float(factor))["id"]

    def keymap(self, page, cuts, looks=None, names=(), zooms=(), id=None):
        return self._item(page, "keymap", id, "keymap", 3, None, cuts=list(cuts), looks=dict(looks or {}),
                          names=list(names), zooms=list(zooms))["id"]

    def photo(self, page, file, crop=None, caption=None, source=None, id=None):
        cap = None if caption is None else self._tid(page, caption, "caption", None)
        return self._item(page, "photo", id, "photo", 2, None, file=file, crop=list(crop) if crop else None,
                          caption=cap, source=source)["id"]

    def chart(self, page, w_mm, h_mm, shapes, id=None):
        D = self.drawing(id, page, (0.0, 0.0, w_mm, h_mm), units="mm", dkind="chart", scale_bar=False,
                         fit=(0.75, 1.5))
        self.layer(D, "chart", shapes)
        D["kind_note"] = "chart"
        return D["id"]

    def source(self, key, text, url, page=None):
        self.d["sources"][key] = dict(text=text, url=url)
        if page:
            self._item(page, "source", "src_" + key, "source", 9, None, key=key)

    # -- out
    def save(self):
        import json as _j
        d_ = bg_booklet(self.folder)
        os.makedirs(d_, exist_ok=True)
        self.path = os.path.join(d_, "items.json")
        with open(self.path, "w", encoding="utf-8") as f:
            _j.dump(self.d, f, ensure_ascii=False, separators=(",", ":"))
        return self.path

    def summary(self):
        n = {}
        for its in self.d["pages"].values():
            for it in its:
                n[it["kind"]] = n.get(it["kind"], 0) + 1
        return u"items %s: %s -> %s" % (self.d["script"], u", ".join(u"%s %d" % kv for kv in sorted(n.items())),
                                         self.path or u"(not saved)")
# ---- marker.py (round 4, S1, 1 Nov 2026; G-R4-7, PLAN §4.4): ONE marker (circle + number / letter) everywhere --------
# The glyph sits on the centre of its VISIBLE ink box (font_metrics.fm_ink_box), so "g", "h", "1" and "12" are all
# centred (CHK3_7 §4.1: the old cap-height offsets pulled lowercase letters down and let tails hang out). The circle
# grows with the glyph: radius = half the ink box diagonal + MK_MARGIN_MM, so two digits get a larger circle (§4.2).
# The colour is the colour the named element is drawn in, from ONE table (mk_colour), never a page-wide accent (§4.3).
# Needs font_metrics.py (and pdf_fonts.py) included before it; text_place.py for mk_put.
#   mk_marker(cx, cy, s, colour, size_pt=7.0, r_min=None, style="solid", rim="FFFFFF", rim_mm=0.25, text_col=None,
#             y_down=False) -> (shapes, box, r)
#       y_down  False (default) for the scripts' y-up sheets and the common modules' shape lists (section_frame,
#               figures); True on y-down pages (the booklet grid)
#       shapes  house format: ("poly", ring, fill, stroke, lw) then ("text", s, x, baseline_y, size_mm, colour, True,
#               "L"); box = the marker's outer box (rim included); r = the circle's radius (mm)
#       style   "solid": a disc in colour, a white rim, the glyph white or ink by contrast;
#               "ring": a paper disc, a coloured rim, the glyph in colour
#   mk_register(kind, table)          the element table a page draws with ({key: hex}), so marker = element colour
#   mk_colour(kind, key) -> hex       the registered colour; an unknown kind / key RAISES (no fallback colour)
#   mk_put(tp, shapes, name=None) -> the non-text shapes
#                                     registers the disc as a keep (kind "marker") and the glyph in the TextPage (it
#                                     may sit on its own disc only; give each marker its own name); the caller draws the returned disc shapes, the
#                                     TextPage draws the glyph
MK_MARGIN_MM = 0.45                    # clear ring round the glyph's ink box (G-R4-7 "keep a margin")
MK_PAPER = "FFFFFF"
MK_INK = "2C2219"                      # dark glyph on light discs (the north-arrow ink of PLAN §4.5)
MK_COLOURS = {}
MK_N = [0]                             # markers registered this run (unique keep names)


def _mk_lum(hx):
    """relative luminance (WCAG 2) of a hex colour"""
    h = str(hx).lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def _mk_contrast(a, b):
    la, lb = _mk_lum(a), _mk_lum(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def mk_text_colour(fill):
    """white or ink, whichever contrasts more with fill"""
    return MK_PAPER if _mk_contrast(fill, MK_PAPER) >= _mk_contrast(fill, MK_INK) else MK_INK


def mk_register(kind, table):
    """the colours a page draws its elements of one kind with ({key: hex}); markers of that kind read them"""
    MK_COLOURS.setdefault(kind, {}).update(dict((str(k), str(v).lstrip("#")) for k, v in table.items()))


def mk_colour(kind, key):
    """the colour the named element is drawn in"""
    try:
        return MK_COLOURS[kind][str(key)]
    except KeyError:
        raise KeyError(u"marker colour: no element colour registered for %s / %s (mk_register it from the table the "
                       u"element is drawn with)" % (kind, key))


def mk_marker(cx, cy, s, colour, size_pt=7.0, r_min=None, style="solid", rim="FFFFFF", rim_mm=0.25, text_col=None,
              y_down=False):
    """one marker centred on (cx, cy) page mm (see the module notes)"""
    import math as _m
    s = u"%s" % s
    col = str(colour).lstrip("#")
    ix0, iy0, ix1, iy1 = fm_ink_box(s, size_pt, True)
    r = 0.5 * _m.hypot(ix1 - ix0, iy1 - iy0) + MK_MARGIN_MM
    if r_min is not None:
        r = max(r, float(r_min))
    ring = [(cx + r * _m.cos(2 * _m.pi * i / 48.0), cy + r * _m.sin(2 * _m.pi * i / 48.0)) for i in range(48)]
    if style == "ring":
        lw = max(rim_mm, 0.25)
        disc = ("poly", ring, MK_PAPER, col, lw)
        tc = text_col or col
        out_r = r + lw / 2.0
    else:
        disc = ("poly", ring, col, rim if rim_mm else None, rim_mm)
        tc = text_col or mk_text_colour(col)
        out_r = r + (rim_mm / 2.0 if rim_mm else 0.0)
    x = cx - (ix0 + ix1) / 2.0
    base = cy + (iy0 + iy1) / 2.0 if y_down else cy - (iy0 + iy1) / 2.0
    size_mm = size_pt * 25.4 / 72.0
    shapes = [disc, ("text", s, x, base, size_mm, tc, True, "L")]
    return shapes, (cx - out_r, cy - out_r, cx + out_r, cy + out_r), r


def mk_put(tp, shapes, name=None):
    """registers a marker in the TextPage tp: its disc as a keep, its glyph as a text that may sit on that disc;
    returns the disc shapes for the caller to draw (before tp.emit draws the glyph)"""
    disc = [s_ for s_ in shapes if s_ and s_[0] != "text"]
    MK_N[0] += 1
    nm = name or u"marker %d" % MK_N[0]
    for s_ in disc:
        if s_[0] == "poly":
            tp.keep(s_[1], "marker", nm)
    for s_ in shapes:
        if s_ and s_[0] == "text":
            tp.put(s_[1], s_[2], s_[3], s_[4] * tp.unit_mm / TP_PT, True, "L", 0.0, nm, "marker", s_[5], allow=(nm,))
    return disc
# ---- block.py (round 4, S1, 1 Nov 2026; G-R4-3, PLAN §4.2): ONE section block template (U25 / U27) ---------------------
# A section block = title strip on top + the drawing + its text, laid out on the booklet grid (grid.py: baseline
# GRID_BASE = 4 mm, gutter GRID_GUT = 4 mm, column GRID_COL = 29 mm). No fixed ratios (U27): the caller gives the
# block's box, the template only splits it. Page mm; y_down=False mirrors it for y-up sheets.
#   blk_section(x0, y0, w, h, title, side_w=None, mode="LEFT", why=None, strip_h=None, y_down=True)
#       -> dict(title=box, title_base=(x, y), drawing=box, side=box or None, strip=box or None, mode=mode, title_text)
#   (x0, y0) = the block's visual top-left corner; boxes are (x0, y0, x1, y1)
#   LEFT  (default, U25 left): the title strip on top (one line, heading style, flush with the block's left edge), the
#         drawing below it, a narrow text column on its right sharing the drawing's top and bottom edges (side_w,
#         default one grid column), nothing below. The text column holds the keywords and the numbered list in
#         reading order (G-R4-5.5).
#   RIGHT (wide, short cuts only): the title, the drawing over the full width, a thin strip under it of the same
#         width (strip_h, default 3 baselines = 12 mm). `why` must say why this cut takes RIGHT (the build says why).
#   Title: GRID_TYPE["heading"] (10 pt bold); its baseline sits one baseline (4 mm) below the block's top, and the
#   drawing starts two baselines (8 mm) below it, so drawings and titles stay on the baseline grid.
BLK_TITLE_BASE = 4.0               # mm from the block's top to the title's baseline (one GRID_BASE)
BLK_TITLE_H = 8.0                  # mm from the block's top to the drawing's top (two GRID_BASE)
BLK_STRIP_H = 12.0                 # mm, RIGHT mode's strip under the drawing (three GRID_BASE)


def blk_section(x0, y0, w, h, title, side_w=None, mode="LEFT", why=None, strip_h=None, y_down=True):
    """the boxes of one section block (see the module notes)"""
    mode = str(mode or "LEFT").upper()
    if mode not in ("LEFT", "RIGHT"):
        raise ValueError("blk_section mode %r: LEFT or RIGHT" % mode)
    if mode == "RIGHT" and not (why and str(why).strip()):
        raise ValueError("blk_section %r: RIGHT mode needs `why` (the build says why this cut is not LEFT)" % title)
    gut = GRID_GUT
    sw = float(GRID_COL if side_w is None else side_w)
    st = float(BLK_STRIP_H if strip_h is None else strip_h)
    # visual offsets from the top (t) inside the block, turned into page y at the end
    Y = (lambda t: y0 + t) if y_down else (lambda t: y0 - t)

    def box(xa, ta, xb, tb):
        a, b = Y(ta), Y(tb)
        return (xa, min(a, b), xb, max(a, b))
    x1 = x0 + w
    if mode == "LEFT":
        dx1 = x1 - sw - gut
        if dx1 - x0 < 2 * GRID_COL:
            raise ValueError("blk_section %r: %.1f mm is too narrow for a drawing beside a %.1f mm column" % (
                title, w, sw))
        out = dict(drawing=box(x0, BLK_TITLE_H, dx1, h), side=box(dx1 + gut, BLK_TITLE_H, x1, h), strip=None)
    else:
        if h - BLK_TITLE_H - st - gut < GRID_BASE:
            raise ValueError("blk_section %r: %.1f mm is too low for a drawing over a %.1f mm strip" % (title, h, st))
        out = dict(drawing=box(x0, BLK_TITLE_H, x1, h - st - gut), side=None, strip=box(x0, h - st, x1, h))
    d = out["drawing"]
    out.update(title=box(x0, 0.0, d[2], BLK_TITLE_H - GRID_BASE / 2.0), title_base=(x0, Y(BLK_TITLE_BASE)),
               mode=mode, title_text=title, why=why)
    return out
# ---- M5 water renderer (H-B 30 Oct 2026; brief G8): ONE call per view type, the layer order fixed here ------------
#   water_plan(ring, k, ...)                           plan: textured water, defined bank edge, depth tone along the flow
#   water_axo(P, left, right, z_bed, z_wl, z_top, ...) axonometric: bed, bank walls, water body with depth and surface
#   water_section(profile, k, y_of, cid=...)           section: bed profile filled, water at the AVERAGE YEARLY FLOW
#                                                      (never dry), Q100 and Q500 lines, bank materials
# Every call returns (or adds into) a WaterLayers draw list; draw it with .put(pg) (or shp_put(pg, wl.shapes())):
# the layers always come out in WAT_LAYERS order, whatever order the page added them in, so the p21 / p22
# foreground-background confusion cannot recur. Pages add their own parts into the same list:
#   wl = water_layers(); water_section(..., into=wl); wl.add("structures", deck); wl.add("vegetation", trees);
#   wl.add("figures", people); wl.add("labels", texts); wl.put(pg)
# Needs section_parts.py (SEC, SCT, sec_hatch, sct_hatch_fill, sct_bed, _sec_mix, _sct_inside) and, for cid=,
# levels.py + data/LEVELS.py. Never: a blue fill with waves, a squiggle in mid-stream, a dry bed in a section.
# Round 3 (A2, 31 Oct 2026, G8 / D2): no low-flow line in any plan (the summer strip shows in sections only); the depth
# tone of the flow streaks is capped (WAT_STREAK_CAP) so no dark centre line forms; islands (holes=) stay untextured;
#   water_clip_points(points, water_rings, ...)  drops tree / plant symbols in the water, logs "planting clipped to
#                                                 land: n symbols removed from water"
#   wat_draw_order_lines(page, wl=None, steps=None)  "draw order: ..." (+ a FLAG line when steps break WAT_LAYERS)
#   wat_flag_lines()                             this run's water log lines (emptied): every page script appends them
# Shapes: ("poly", ring, fill, stroke, lw[, alpha]) ("line", pts, colour, lw[, dash]) ("text", s, x, y, size,
# colour, bold, align) ("image", x, y, w, h, path, alpha, flip, clip); page mm, y up.

WAT_LAYERS = ("atmosphere", "background", "ground", "bed", "water", "structures", "vegetation", "figures", "labels")
# the layer names as the log prints them (PLAN §2 Layer order: terrain, bed, water, structures over water, bank
# planting clipped to land, people, labels)
WAT_LAYER_WORDS = dict(atmosphere="sky", background="background", ground="terrain", bed="bed", water="water",
                       structures="structures over water", vegetation="bank planting (clipped to land)",
                       figures="people", labels="labels")
WAT_STREAK_CAP = 0.6             # plan streaks: the depth tone stops darkening here (0..1), so no dark centre line
WAT_LOG = []                     # this run's water log lines (planting clips, draw orders); wat_flag_lines() empties


class WaterLayers(object):
    """a layered draw list: add(layer, shapes) in any order, shapes() / put(pg) in WAT_LAYERS order (G8)"""

    def __init__(self):
        self.L = dict((n, []) for n in WAT_LAYERS)
        self.anchors = {}

    def add(self, layer, shapes):
        if layer not in self.L:
            raise KeyError("water layers: %r; use one of %s" % (layer, ", ".join(WAT_LAYERS)))
        self.L[layer] += list(shapes or [])
        return self

    def merge(self, other):
        for n in WAT_LAYERS:
            self.L[n] += other.L[n]
        self.anchors.update(other.anchors)
        return self

    def shapes(self, layers=None):
        return [s_ for n in WAT_LAYERS if layers is None or n in layers for s_ in self.L[n]]

    def put(self, pg):
        shp_put(pg, self.shapes())


def water_layers():
    """a new, empty WaterLayers draw list"""
    return WaterLayers()


def shp_put(pg, shapes):
    """draws house shapes on a Page with the common API (poly(rings, fill, stroke, lw[, dash, stripes, alpha]),
    line(pts, stroke, lw, dash), text(s, x, y, size, color, bold, align)); "image" shapes go into pg.items for the
    common write_pdf (D1 a). A poly's 7th element = its holes (rings, filled even-odd: islands stay open)"""
    for s_ in shapes or []:
        t = s_[0]
        if t == "poly":
            if len(s_[1]) < 3:
                continue
            a = s_[5] if len(s_) > 5 else None
            rings = [list(s_[1])] + [list(R) for R in (s_[6] if len(s_) > 6 and s_[6] else ()) if len(R) >= 3]
            if a is not None:
                try:
                    pg.poly(rings, fill=s_[2] or None, stroke=s_[3] or None, lw=s_[4] or 0.1, alpha=a)
                    continue
                except TypeError:
                    pass
            pg.poly(rings, fill=s_[2] or None, stroke=s_[3] or None, lw=s_[4] or 0.1)
        elif t == "line":
            if len(s_[1]) >= 2:
                pg.line(list(s_[1]), s_[2], s_[3], s_[4] if len(s_) > 4 else None)
        elif t == "text":
            pg.text(s_[1], s_[2], s_[3], s_[4], s_[5], bold=s_[6] if len(s_) > 6 else False,
                    align=s_[7] if len(s_) > 7 else "L")
        elif t == "image":
            pg.items.append(tuple(s_) + (None,) * (9 - len(s_)))


def _wat_pal():
    """the water palette (calm, G5), from the section language's water blue"""
    m = _sec_mix
    return dict(surface=m(SEC["water"], SEC["paper"], 0.62), shallow=m(SEC["water"], SEC["paper"], 0.45),
                deep=m(SEC["hatch"], SEC["water"], 0.45), streak=m(SEC["water"], SEC["paper"], 0.15),
                edge=m(SEC["hatch"], SEC["ink"], 0.55), sec=SEC["channel"], sec_line=m(SEC["hatch"], SEC["paper"], 0.35),
                q100=m(SEC["hatch"], SEC["ink"], 0.35), q500=m(SEC["hatch"], SEC["ink"], 0.65),
                low=m(SEC["hatch"], SEC["water"], 0.2))    # "low": the summer strip's tone, SECTIONS only (D2)


def _wat_pal_sec():
    """round 5 (S3, G-R5-4.1, PLAN §3): the section water colours: body, surface, Q100 / Q500 lines (one colour,
    dashes tell them apart)"""
    P = dict(_wat_pal())
    if "SCT_WATER" in globals():
        P.update(sec=SCT_WATER["body"], sec_line=SCT_WATER["surface"], q100=SCT_WATER["flood"],
                 q500=SCT_WATER["flood"])
    return P


def _wat_rng(seed):
    s = [int(seed * 69069 + 1013) & 0x7fffffff]

    def r():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7fffffff
        return s[0] / float(0x7fffffff)
    return r


def _wat_edge_index(ring, cell):
    """edges of the ring bucketed by grid cell (size cell, page mm): {(i, j): [(a, b), ...]}"""
    import math as _m
    idx = {}
    for a, b in zip(ring, ring[1:] + ring[:1]):
        i0, i1 = int(_m.floor(min(a[0], b[0]) / cell)), int(_m.floor(max(a[0], b[0]) / cell))
        j0, j1 = int(_m.floor(min(a[1], b[1]) / cell)), int(_m.floor(max(a[1], b[1]) / cell))
        for i in range(i0, i1 + 1):
            for j in range(j0, j1 + 1):
                idx.setdefault((i, j), []).append((a, b))
    return idx


def _wat_near_edge(idx, cell, p, rmax):
    """(distance to the nearest edge, unit direction of that edge) for page point p, searching outward up to rmax"""
    import math as _m
    ci, cj = int(_m.floor(p[0] / cell)), int(_m.floor(p[1] / cell))
    best, bd, n = (1.0, 0.0), 1e18, 0
    while n * cell <= rmax + cell:
        for i in range(ci - n, ci + n + 1):
            for j in range(cj - n, cj + n + 1):
                if max(abs(i - ci), abs(j - cj)) != n:
                    continue
                for a, b in idx.get((i, j), ()):
                    dx, dy = b[0] - a[0], b[1] - a[1]
                    L2 = dx * dx + dy * dy
                    if L2 < 1e-12:
                        continue
                    t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
                    d = _m.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
                    if d < bd:
                        L = _m.sqrt(L2)
                        bd, best = d, (dx / L, dy / L)
        if bd <= n * cell:                              # nothing nearer can lie in a farther ring of cells
            break
        n += 1
    return min(bd, rmax), best


def _wat_scan_inside(ring, spacing, rnd, holes=()):
    """jittered sample points inside the ring and outside its holes, row by row (crossings of each row with the
    rings, paired even-odd: fast on long rings)"""
    ys = [p[1] for p in ring]
    out = []
    y = min(ys) + 0.5 * spacing
    E = [e for R in [ring] + [list(H) for H in holes if len(H) >= 3] for e in zip(R, R[1:] + R[:1])]
    while y < max(ys):
        xs = sorted(a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) for a, b in E
                    if (a[1] <= y < b[1]) or (b[1] <= y < a[1]))
        for i in range(0, len(xs) - 1, 2):
            x = xs[i] + (0.2 + 0.6 * rnd()) * spacing
            while x < xs[i + 1]:
                out.append((x, y + (rnd() - 0.5) * 0.6 * spacing))
                x += spacing * (0.8 + 0.4 * rnd())
        y += spacing
    return out


def water_plan(ring, k, depth=None, flow_deg=None, bank=True, seed=0, spacing=1.3, style="b", into=None, holes=None):
    """the stream in plan inside ring (page mm, the bank line = the wet edge at average flow): a calm surface tone, the
    bank edge as a firm line, and short flow streaks running along the banks (local direction = the nearest bank,
    or flow_deg) whose tone deepens toward the middle (depth tone: distance to the bank, or depth(x, y) 0..1), capped
    at WAT_STREAK_CAP so the middle never reads as a dark centre line (D2). holes = islands inside the ring (page mm
    rings): left open, no streaks, their edge drawn as bank. No low-flow line (round 3, D2: the summer strip is shown
    in sections only). Plans are vector in both styles. Returns the WaterLayers."""
    import math as _m
    wl = into if into is not None else water_layers()
    P = _wat_pal()
    ring = list(ring)
    holes = [list(H) for H in (holes or ()) if len(H) >= 3]
    sh = [("poly", ring, P["surface"], None, 0.1, None, holes) if holes else ("poly", ring, P["surface"], None, 0.1)]
    rnd = _wat_rng(seed)
    cell = 4.0 * spacing
    idx = _wat_edge_index(ring, cell)
    for H in holes:                                    # an island's edge is a bank too (shallow next to it)
        for key, es in _wat_edge_index(H, cell).items():
            idx.setdefault(key, []).extend(es)
    reach = 40.0 * spacing                             # depth tone saturates this far (page mm) from the bank
    samples = []
    for p in _wat_scan_inside(ring, spacing, rnd, holes):
        d, u = _wat_near_edge(idx, cell, p, reach)
        samples.append((p, d, u))
    dmax = max([s_[1] for s_ in samples] or [1.0]) or 1.0
    for p, d, u in samples:
        t = depth(p[0], p[1]) if depth else d / dmax
        if t < 0.15:                                   # a clear, light margin along the bank (shallow water)
            continue
        tc = min(float(t), WAT_STREAK_CAP)             # the tone stops deepening: no dark line down the middle
        if flow_deg is not None:
            u = (_m.cos(_m.radians(flow_deg)), _m.sin(_m.radians(flow_deg)))
        L = (0.5 + 0.9 * tc) * spacing * (0.7 + 0.5 * rnd())
        col = _sec_mix(P["shallow"], P["deep"], tc)
        a = (p[0] - 0.5 * L * u[0], p[1] - 0.5 * L * u[1])
        b = (p[0] + 0.5 * L * u[0], p[1] + 0.5 * L * u[1])
        sh.append(("line", [a, b], col, 0.12 + 0.12 * tc))
    wl.add("water", sh)
    if bank:
        wl.add("water", [("line", R + [R[0]], P["edge"], 0.35) for R in [ring] + holes])
    return wl


def water_legend(x, y, size=1.8, floods=False, gap=None):
    """legend rows for the water drawings (G1: every symbol explained): the stream, the Q100 / Q500 lines and the
    average-flow water (sections); x, y = top left, page mm. Returns shapes (incl. text). Round 5 (S3): the
    section rows in the section colours (_wat_pal_sec)."""
    P = _wat_pal_sec()
    gap = gap or 1.6 * size
    rows = [("Selinos stream (darker = deeper)", "water")]
    if floods:
        rows += [("Q100 flood level", "q100"), ("Q500 flood level", "q500"), ("Water at average yearly flow", "avg")]
    sh, yy = [], y
    for label, kind in rows:
        cy = yy - 0.5 * size
        if kind == "water":
            sh += [("poly", [(x, cy - 0.5 * size), (x + 2.5 * size, cy - 0.5 * size), (x + 2.5 * size, cy + 0.5 * size),
                             (x, cy + 0.5 * size)], P["surface"], P["edge"], 0.25),
                   ("line", [(x + 0.6 * size, cy), (x + 1.9 * size, cy)], P["deep"], 0.2)]
        elif kind == "avg":
            sh += [("poly", [(x, cy - 0.5 * size), (x + 2.5 * size, cy - 0.5 * size), (x + 2.5 * size, cy),
                             (x, cy)], P["sec"], None, 0.1),
                   ("line", [(x, cy), (x + 2.5 * size, cy)], P["sec_line"], 0.3)]
        else:
            sh.append(("line", [(x, cy), (x + 2.5 * size, cy)], P[kind], 0.3,
                       [1.2, 0.6] if kind == "q100" else [0.4, 0.5]))
        sh.append(("text", label, x + 3.2 * size, cy - 0.35 * size, size, SEC["ink"], False, "L"))
        yy -= gap
    return sh


# ---- G8 (round 3, A2): planting kept on land, the draw-order log ---------------------------------------------------
def _wat_bands(rings, h):
    """the rings' edges bucketed by horizontal band of height h: {j: [(a, b), ...]} (for the even-odd point test)"""
    import math as _m
    out = {}
    for R in rings:
        for a, b in zip(R, R[1:] + R[:1]):
            if a[1] == b[1]:
                continue
            for j in range(int(_m.floor(min(a[1], b[1]) / h)), int(_m.floor(max(a[1], b[1]) / h)) + 1):
                out.setdefault(j, []).append((a, b))
    return out


def _wat_inside(bands, h, p):
    """True when p lies inside the rings (even-odd: a hole of a group counts as land)"""
    import math as _m
    x, y = p[0], p[1]
    c = False
    for a, b in bands.get(int(_m.floor(y / h)), ()):
        if (a[1] > y) != (b[1] > y) and x < a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]):
            c = not c
    return c


def water_clip_points(points, water_rings, extra_rings=(), margin=0.0, crown_frac=0.5, get=None, page=None,
                      log=None):
    """G8: the tree / plant symbols that stay on land. points: the symbols, each (x, y) or (x, y, r) with r the crown
    radius (or any item: get(item) -> (x, y, r)); water_rings: the stream's rings (outlines and island holes, even-odd)
    in the SAME units as the points (page mm or survey m: basemap_water_rings gives survey m); extra_rings: more
    water the page draws beyond the stream (widened wetlands, side arms, reed basins, ponds). A symbol is removed
    when its centre lies in water, or within margin + crown_frac x r of the water's edge (its crown reaching more
    than crown_frac of its radius over the water; crown_frac 0 = any overhang). A designed planted island is land
    only when it is a hole in the rings. Logs "planting clipped to land: n symbols removed from water (page)" into
    log (a list) or WAT_LOG. Returns the kept symbols, in their order."""
    import math as _m
    rings = [list(R) for R in list(water_rings or ()) + list(extra_rings or ()) if R and len(R) >= 3]
    pts = list(points or ())
    if get is None:
        def get(q):
            r_ = q[2] if len(q) > 2 and isinstance(q[2], (int, float)) else 0.0
            return q[0], q[1], r_
    if not rings or not pts:
        n, kept = 0, pts
    else:
        xs = [p[0] for R in rings for p in R]
        ys = [p[1] for R in rings for p in R]
        span = max(max(xs) - min(xs), max(ys) - min(ys), 1e-6)
        h = span / 400.0                                # band / cell size: about 400 across the water's extent
        bands = _wat_bands(rings, h)
        idx = {}
        for R in rings:
            for key, es in _wat_edge_index(R, h).items():
                idx.setdefault(key, []).extend(es)
        bb = (min(xs), min(ys), max(xs), max(ys))
        kept, n = [], 0
        for q in pts:
            x, y, r = get(q)
            reach = max(0.0, margin) + max(0.0, crown_frac) * max(0.0, float(r or 0.0))
            if x < bb[0] - reach or x > bb[2] + reach or y < bb[1] - reach or y > bb[3] + reach:
                kept.append(q)
                continue
            wet = _wat_inside(bands, h, (x, y))
            if not wet and reach > 0.0:
                d, _u = _wat_near_edge(idx, h, (x, y), reach)
                wet = d < reach                          # the crown reaches over the water
            if wet:
                n += 1
            else:
                kept.append(q)
    line = u"planting clipped to land: %d symbols removed from water%s" % (n, u" (%s)" % page if page else u"")
    (log if log is not None else WAT_LOG).append(line)
    return kept


def wat_draw_order_lines(page=None, wl=None, steps=None):
    """G8 done-when: the log line(s) naming the order a drawing was drawn in. wl: a WaterLayers (its filled layers, in
    WAT_LAYERS order); steps: the layer names (WAT_LAYERS) in the order a page that draws by hand drew them: out of
    order -> a "FLAG draw order" line naming the pair. Appended to WAT_LOG and returned (list of lines)."""
    if steps is not None:
        seq = [n for n in steps if n in WAT_LAYERS]
    elif wl is not None:
        seq = [n for n in WAT_LAYERS if wl.L.get(n)]
    else:
        seq = list(WAT_LAYERS)
    tag = u" %s" % page if page else u""
    out = [u"draw order%s: %s" % (tag, u", ".join(WAT_LAYER_WORDS[n] for n in seq))]
    for a, b in zip(seq, seq[1:]):
        if WAT_LAYERS.index(b) < WAT_LAYERS.index(a):
            out.append(u"FLAG draw order%s: %s drawn after %s" % (tag, WAT_LAYER_WORDS[b], WAT_LAYER_WORDS[a]))
    WAT_LOG.extend(out)
    return out


def wat_flag_lines():
    """this run's water log lines (planting clips, draw orders, FLAGs), oldest first; the list is emptied"""
    out = list(WAT_LOG)
    del WAT_LOG[:]
    return out


# ---- axonometric (R10 idea: the water body cut open at the box edge, its depth visible) ---------------------------
def _wat_view(P):
    """the direction toward the viewer of a parallel projection P(x, y, z) -> (X, Y), pointing up (z > 0)"""
    o = P(0.0, 0.0, 0.0)
    c = [P(1.0, 0.0, 0.0), P(0.0, 1.0, 0.0), P(0.0, 0.0, 1.0)]
    r1 = [c[i][0] - o[0] for i in range(3)]
    r2 = [c[i][1] - o[1] for i in range(3)]
    v = (r1[1] * r2[2] - r1[2] * r2[1], r1[2] * r2[0] - r1[0] * r2[2], r1[0] * r2[1] - r1[1] * r2[0])
    return v if v[2] >= 0 else (-v[0], -v[1], -v[2])


def _wat_wall_faces(P, line, other, z0, z1, v, fill, ink, course):
    """the visible inner faces of a vertical bank wall along `line` (model x, y), facing toward `other`"""
    sh = []
    ox = sum(p[0] for p in other) / len(other)
    oy = sum(p[1] for p in other) / len(other)
    for a, b in zip(line[:-1], line[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        n = (-dy, dx)
        if n[0] * (ox - a[0]) + n[1] * (oy - a[1]) < 0:
            n = (dy, -dx)
        if n[0] * v[0] + n[1] * v[1] <= 0:              # faces away from the viewer
            continue
        q = [P(a[0], a[1], z0), P(b[0], b[1], z0), P(b[0], b[1], z1), P(a[0], a[1], z1)]
        sh.append(("poly", q, fill, ink, 0.12))
        z = z0 + course
        while z < z1 - 1e-6:                            # stone courses
            sh.append(("line", [P(a[0], a[1], z), P(b[0], b[1], z)], ink, 0.05))
            z += course
    return sh


def water_axo(P, left, right, z_bed, z_wl, z_top, seed=0, wall="stone", bed_t_m=1.0, course_m=0.5, style="b",
              into=None):
    """the stream in an axonometric (P(x, y, z) -> page (X, Y), parallel): left / right = the two bank lines (model
    x, y, both running downstream), z_bed bed, z_wl water at average flow, z_top wall tops (m). Draws the bed floor,
    the visible inner faces of the bank walls (coursed, course_m apart), the water surface (see-through, flow streaks)
    and the cut face at the box edge(s) facing the viewer: water depth and the bed band (bed_t_m, drawing rule).
    Returns the WaterLayers (bed: floor + walls + cut bed; water: body + surface)."""
    wl = into if into is not None else water_layers()
    Pa = _wat_pal()
    v = _wat_view(P)
    left, right = [tuple(p) for p in left], [tuple(p) for p in right]
    floor = [P(p[0], p[1], z_bed) for p in left] + [P(p[0], p[1], z_bed) for p in reversed(right)]
    wall_fill = SCT.get(wall, SCT["stone"])
    bed = [("poly", floor, SCT["gravel"], None, 0.1)]
    bed += _wat_wall_faces(P, left, right, z_bed, z_top, v, wall_fill, SCT["line"], course_m)
    bed += _wat_wall_faces(P, right, left, z_bed, z_top, v, wall_fill, SCT["line"], course_m)
    surf = [P(p[0], p[1], z_wl) for p in left] + [P(p[0], p[1], z_wl) for p in reversed(right)]
    wat = [("poly", surf, Pa["surface"], None, 0.1, 0.85)]
    rnd = _wat_rng(seed)
    for i in range(len(left) - 1):                      # streaks along the flow between the banks
        for j in range(3):
            t = 0.25 + 0.25 * j + 0.08 * (rnd() - 0.5)
            a = (left[i][0] + (right[min(i, len(right) - 1)][0] - left[i][0]) * t,
                 left[i][1] + (right[min(i, len(right) - 1)][1] - left[i][1]) * t)
            b = (left[i + 1][0] + (right[min(i + 1, len(right) - 1)][0] - left[i + 1][0]) * t,
                 left[i + 1][1] + (right[min(i + 1, len(right) - 1)][1] - left[i + 1][1]) * t)
            s0, s1 = 0.15 + 0.3 * rnd(), 0.55 + 0.3 * rnd()
            wat.append(("line", [P(a[0] + (b[0] - a[0]) * s0, a[1] + (b[1] - a[1]) * s0, z_wl),
                                 P(a[0] + (b[0] - a[0]) * s1, a[1] + (b[1] - a[1]) * s1, z_wl)],
                        Pa["deep"] if j == 1 else Pa["shallow"], 0.18))
    for line in (left, right):                          # wall tops
        bed.append(("line", [P(p[0], p[1], z_top) for p in line], SCT["cut"], 0.25))
    for idx, nxt in ((0, 1), (-1, -2)):                 # the cut end(s) facing the viewer
        a, b = left[idx], right[idx]
        dx, dy = left[nxt][0] - a[0], left[nxt][1] - a[1]
        if -(dx * v[0] + dy * v[1]) <= 0:               # outward normal of this end = away from the next point
            continue
        cut_w = [P(a[0], a[1], z_bed), P(b[0], b[1], z_bed), P(b[0], b[1], z_wl), P(a[0], a[1], z_wl)]
        cut_b = [P(a[0], a[1], z_bed - bed_t_m), P(b[0], b[1], z_bed - bed_t_m), P(b[0], b[1], z_bed),
                 P(a[0], a[1], z_bed)]
        bed += sct_hatch_fill(cut_b, "gravel", 5.0, SCT["cut"], 0.25)
        wat += [("poly", cut_w, Pa["sec"], None, 0.1)]
        for f in (0.33, 0.66):
            z = z_bed + (z_wl - z_bed) * f
            wat.append(("line", [P(a[0], a[1], z), P(b[0], b[1], z)], Pa["sec_line"], 0.08))
        wat.append(("line", [P(a[0], a[1], z_wl), P(b[0], b[1], z_wl)], SEC["hatch"], 0.3))
        for p in (a, b):                                # the walls in cut
            bed.append(("line", [P(p[0], p[1], z_bed - bed_t_m), P(p[0], p[1], z_top)], SCT["cut"], 0.35))
    wl.add("bed", bed)
    wl.add("water", wat)
    return wl


# ---- section -----------------------------------------------------------------------------------------------------
def _wat_runs(profile, wl_y):
    """the wet stretches of a profile (left to right) under page y wl_y: [ring, ...] (water to the surface)"""
    out, run = [], []
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
            out.append(run)
            run = []
    if run:
        run.append((P[-1][0], wl_y))
        out.append(run)
    return out


def _wat_sec_body(ring, spacing):
    """water in section. Round 5 (S3, G-R5-4.1): one flat colour and the surface line (section_parts sec_water);
    no level lines, no hatch"""
    return sec_water(ring, spacing)


def _wat_cross(profile, y):
    """(x left, x right): where the level y meets the profile from either side (its ends if the water overtops)"""
    P = list(profile)
    xl, xr = P[0][0], P[-1][0]
    for a, b in zip(P[:-1], P[1:]):                    # first descent through y from the left
        if a[1] >= y > b[1]:
            xl = a[0] + (b[0] - a[0]) * (a[1] - y) / (a[1] - b[1])
            break
    for a, b in zip(reversed(P[1:]), reversed(P[:-1])):
        if a[1] >= y > b[1]:
            xr = a[0] + (b[0] - a[0]) * (a[1] - y) / (a[1] - b[1])
            break
    return xl, xr


def _wat_toes(profile, bed_y, tol):
    """(i_left, i_right): the profile indexes of the bed's two ends (first / last point at the bed)"""
    idx = [i for i, p in enumerate(profile) if p[1] <= bed_y + tol]
    if not idx:
        i = min(range(len(profile)), key=lambda j: profile[j][1])
        return i, i
    return idx[0], idx[-1]


def water_section(profile, k, y_of, cid=None, bed=None, avg=None, q100=None, q500=None, banks=("earth", "earth"),
                  fill_ground=True, bottom_m=1.0, bed_band_m=0.6, labels=True, label_size=1.8, label_x=None,
                  spacing=0.6, style="b", into=None):
    """one stream crossing in section. profile = the cut ground line left to right (page mm, banks and bed, e.g.
    sct_profile of two sct_bank surfaces); y_of(level m) -> page y; k mm per m. Levels come from the cut registry
    (cid: bed, avg_flow, q100, q500 via levels.py) unless given. Draws: the ground cut under the profile in the bank
    materials (banks = left, right: stone / concrete / earth / gravel), the bed in gravel (always filled), the water
    at the AVERAGE YEARLY FLOW (never dry), the Q100 and Q500 lines (dashed, wall to wall). Round 4: no level
    labels inside; wl.anchors["levels"] = [(key, level m, page y)] for sf_level_marks outside the frame. fill_ground False = the page drew the banks
    (sct_bank): only the bed band is added. Returns the WaterLayers."""
    wl = into if into is not None else water_layers()
    Pa = _wat_pal_sec()
    if cid is not None:
        bed = level(cid, "bed") if bed is None else bed
        avg = level_avg_flow(cid) if avg is None else avg
        q100 = level(cid, "q100") if q100 is None else q100
        q500 = level(cid, "q500") if q500 is None else q500
    if bed is None or avg is None:
        raise ValueError("water_section: bed and average-flow levels are required (cid or bed=, avg=)")
    if avg <= bed:
        raise ValueError("water_section: average flow %.2f at or below the bed %.2f: a section is never dry (G8)"
                         % (avg, bed))
    prof = [tuple(p) for p in profile]
    bed_y, wl_y = y_of(bed), y_of(avg)
    tol = max(0.05 * k, 0.05)
    il, ir = _wat_toes(prof, bed_y, tol)
    bot = min(p[1] for p in prof) - bottom_m * k
    if fill_ground:
        left, mid, right = prof[:il + 1], prof[il:ir + 1], prof[ir:]
        for part, mat in ((left, banks[0]), (right, banks[1])):
            if len(part) >= 2:
                wl.add("ground", sct_hatch_fill(part + [(part[-1][0], bot), (part[0][0], bot)], mat, k))
        if len(mid) >= 2:
            wl.add("bed", sct_hatch_fill(mid + [(mid[-1][0], bot), (mid[0][0], bot)], "gravel", k))
        wl.add("ground", [("line", prof, SCT["cut"], 0.35)])
    else:
        x0, x1 = prof[il][0], prof[ir][0]
        if x1 - x0 > 1e-6:
            wl.add("bed", sct_bed(x0, x1, bed_y, k, depth_m=bed_band_m))
    for run in _wat_runs(prof, wl_y):
        wl.add("water", _wat_sec_body(run, spacing))
    xs_w = _wat_cross(prof, wl_y)
    wl.anchors["avg"] = (xs_w[1], wl_y)
    wl.anchors["bed"] = ((prof[il][0] + prof[ir][0]) / 2.0, bed_y)
    lines = []
    for key, lev, dash in (("q100", q100, [1.2, 0.6]), ("q500", q500, [0.4, 0.5])):
        if lev is None:
            continue
        y = y_of(lev)
        xl, xr = _wat_cross(prof, y)
        lines.append(("line", [(xl, y), (xr, y)], Pa[key], 0.25, dash))
        wl.anchors[key] = (xr, y)
    wl.add("water", lines)
    # round 4 (S2, G-R4-5.4, U43/U44): no level label inside the picture any more (_wat_level_labels retired); the
    # page puts the marks OUTSIDE its frame: sf_level_marks(frame_box, wl.anchors["levels"]) (section_frame.py).
    # labels / label_size / label_x are kept so old calls still run; they draw nothing.
    wl.anchors["levels"] = [(key, lev, y_of(lev)) for key, lev in (("q500", q500), ("q100", q100), ("avg", avg),
                                                                   ("bed", bed)) if lev is not None]
    return wl
# ---- M8 section framework (H-B 30 Oct 2026; R2-A 31 Oct: G14 grounding, triangle switch, D8 sky, back houses): scale, frame layers, standard elements, callouts, G6 assert ----------
# Needs section_parts.py, water.py (WaterLayers, shp_put), figures.py, plants.py, levels.py + data/LEVELS.py.
# Units: k = page mm per m of the drawing (1:500 printed at 100 % -> k = 2.0); levels in m a.s.l. through
# sf_y_of(); widths in m in, printed in cm (G6/G13). Shapes as in water.py. The cut registry is levels.py:
# level_registry(cid) / level_registry_all(page) (id, location, bed, avg_flow, q100, q500, walls, pages); no page
# types a level. Every element is drawn at true size; sizes the project has no source for are parameters, and the
# few defaults below are marked as drawing rules (never printed as data).

SF_SCALES = (200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000)    # D6 a: the only scales on any sheet
# round 4 (S2, D11, Aras 1 Nov 10:31): 1:100 is allowed for ZOOM INSETS ONLY (nothing on the list is >= 2 x 1:250)
SF_INSET_SCALES = (100,) + SF_SCALES
SF_INSET_MIN_ZOOM = 2.0             # G-R4-5.6: an inset is at least 2 x its parent's scale


def _sf_warn(page, kind, msg):
    """round 5 (S3, G-R5-1): a section-kit hit is a WARNING (common warn.py sink when included: orange + log line),
    never a stop; without warn.py the line goes to SF_LOG (sec_look_lines prints it)"""
    if globals().get("wn_warn"):
        return wn_warn(page, kind, msg)
    line = u"WARNING " + u" ".join(u"%s" % p_ for p_ in (page, kind) if p_) + u": %s" % msg
    SF_LOG.append(line)
    return line


def sf_scale_ok(den, inset=False):
    """den if it is a standard scale (D6 a; inset=True also allows 1:100, D11 zoom insets only). Round 5 (S3): an
    off-list scale is a WARNING and the next listed scale at or beyond it (smaller drawing, so it still fits) is
    returned; never a stop"""
    sc = SF_INSET_SCALES if inset else SF_SCALES
    d = int(round(float(den)))
    if d in sc:
        return d
    up = [v for v in sc if v >= d] or [sc[-1]]
    _sf_warn(None, "scale", u"1:%s is not on the scale list (D6%s): 1:%d used" % (den, ", D11 insets" if inset else "",
                                                                                 up[0]))
    return up[0]


def sf_k(den, print_k=1.0):
    """page mm per m at 1:den (print_k = the booklet's print reduction, 1.0 = drawn at print size)"""
    return 1000.0 / sf_scale_ok(den) * print_k


def sf_scale_pick(extent_m, box_mm, min_den=None):
    """the largest standard scale (smallest 1:den) at which extent_m (m) fits box_mm (page mm); min_den keeps it at
    or beyond a scale (e.g. 500 so sections of one page share 1:500). ValueError when even 1:20,000 is too big."""
    for den in SF_SCALES:
        if min_den and den < min_den:
            continue
        if extent_m * 1000.0 / den <= box_mm + 1e-6:
            return den
    raise ValueError("%.0f m does not fit %.0f mm at any standard scale" % (extent_m, box_mm))


def sf_scale_text(den):
    """"1:1,000" """
    return u"1:{:,}".format(sf_scale_ok(den))


def sf_y_of(datum, y0, k):
    """level (m a.s.l.) -> page y: datum level drawn at page y0"""
    return lambda lev: y0 + (float(lev) - datum) * k


def sf_cut(cid):
    """the cut registry entry (levels.py level_registry): the one place a section reads its levels"""
    return level_registry(cid)


# ---- frame layers: ground, background topography, atmosphere ------------------------------------------------------
def sf_ground(surface, k, bottom_y=None, material="earth", depth_m=1.5, into=None):
    """cut ground under a surface polyline (page mm, left to right) in its material hatch and the cut line, into the
    "ground" layer; bottom_y default = depth_m below the surface's lowest point (drawing rule)"""
    wl = into if into is not None else water_layers()
    b = bottom_y if bottom_y is not None else min(p[1] for p in surface) - depth_m * k
    wl.add("ground", sct_ground(list(surface), b, k, material))
    return wl


def sf_topo_back(profiles, bottom_y, into=None):
    """background topography: ground lines further from the cut (page mm, the farthest first), each a faded
    silhouette down to bottom_y with a fine edge, into "background" (pages take them from the survey)"""
    wl = into if into is not None else water_layers()
    n = len(profiles)
    for i, pr in enumerate(profiles):
        t = 0.75 - 0.35 * (i / float(max(1, n - 1)))   # far = paler
        ring = list(pr) + [(pr[-1][0], bottom_y), (pr[0][0], bottom_y)]
        wl.add("background", [("poly", ring, _sec_mix(SCT_SOIL["layers"][-1], "FFFFFF", t), None, 0.0),
                              ("line", list(pr), _sec_mix(SEC["ink2"], SEC["paper"], t), 0.12)])
    return wl


# ---- G14 grounding (R2-A 31 Oct 2026): every section item stands on its own ground; nothing floats ---------------
# gy anywhere below = a number (flat), a function x -> y, or a polyline [(x, y), ...] (page mm, y up).
SF_G14 = dict(seen=set(), moved=set(), max_mm=0.0, refused={})


def sf_gy(profile):
    """a ground function x -> y from a polyline [(x, y), ...] (page mm, any order; flat beyond its ends)"""
    import bisect as _b
    P = sorted((float(x), float(y)) for x, y in profile)
    xs = [p[0] for p in P]

    def f(x):
        if x <= xs[0]:
            return P[0][1]
        if x >= xs[-1]:
            return P[-1][1]
        i = _b.bisect_right(xs, x)
        (xa, ya), (xb, yb) = P[i - 1], P[i]
        return ya if xb - xa < 1e-12 else ya + (yb - ya) * (x - xa) / (xb - xa)
    f.sf_pts = P
    return f


def _sf_fn(gy):
    if callable(gy):
        return gy
    if isinstance(gy, (list, tuple)):
        return sf_gy(gy)
    return lambda _x, _v=float(gy): _v


def sf_ground_min(gy, xa, xb, n=8):
    """the lowest ground under [xa, xb] (page mm): G14 seats an item there, so no part of its base floats on a
    slope. Polylines: exact (their vertices inside); functions: n + 1 samples."""
    if xb < xa:
        xa, xb = xb, xa
    f = _sf_fn(gy)
    ys = [f(xa + (xb - xa) * i / float(n)) for i in range(n + 1)]
    ys += [y for x, y in (getattr(f, "sf_pts", None) or ()) if xa < x < xb]
    return min(ys)


def sf_seat_x(gy, x, half_w, tol=0.05):
    """G14: the y an item centred on x with a base half_w wide each side stands at = the lowest ground under its
    base; counted in the G14 log line (moved when it differs from the ground under its centre by more than tol mm)"""
    y = sf_ground_min(gy, x - abs(half_w), x + abs(half_w))
    key = (round(x, 2), round(y, 2))
    SF_G14["seen"].add(key)
    d = _sf_fn(gy)(x) - y
    if d > tol:
        SF_G14["moved"].add(key)
        SF_G14["max_mm"] = max(SF_G14["max_mm"], d)
    return y


def sf_ground_fn(gy, half_w):
    """gy as a function that already seats (sf_seat_x): pass it as the ground of fig_side, fig_activity,
    pla_section ... so every item they place stands on the lowest ground under its base"""
    return lambda x: sf_seat_x(gy, x, half_w)


# ---- people on the surface (round 5, S3, CHK-3 seat fix, G-R5-4.4 / PLAN §3 People) -------------------------------
# sf_seat_x seats on the LOWEST ground under a base: right for plants and houses (a trunk or wall foot may go into a
# slope), wrong for people (U11 "his feet is in the fucking floor", S09 feet sunk in a step). People stand on the
# HIGHER ground at their two feet: no foot is ever inside the ground or a step; on a step edge the person stands on
# the tread. Plants keep sf_seat_x.
SF_PEOPLE = dict(seen=0, grounded=0, tol_mm=0.15)


def sf_seat_feet(gy, x, half_w, n=6):
    """the y a person centred on x stands at: the HIGHER ground at the feet x - half_w and x + half_w (and between
    them, n samples, so a riser between the feet is stood on, never stepped into). half_w = the foot half span
    (figures.py FIG_FOOT_HALF_M x k). Counted in sf_people_line."""
    f = _sf_fn(gy)
    hw = abs(half_w)
    ys = [f(x - hw + 2.0 * hw * i / float(n)) for i in range(n + 1)]
    ys += [y for xx, y in (getattr(f, "sf_pts", None) or ()) if x - hw < xx < x + hw]
    y = max(ys)
    SF_PEOPLE["seen"] += 1
    SF_PEOPLE["grounded"] += 1
    return y


def sf_feet_fn(gy, half_w):
    """gy as a function that seats people by sf_seat_feet: pass it as the ground of fig_side / fig_activity /
    fig_place_zones (S4 figures.py) instead of sf_ground_fn"""
    return lambda x: sf_seat_feet(gy, x, half_w)


def sf_people_check(items, gy, half_w=None, page=None, tol=None):
    """G-R5-4.4 check by reasoning: items = [shapes of one person, ...] standing on ground gy; a person whose feet
    are more than tol mm above (floating) or below (sunk) the sf_seat_feet ground is a WARNING. Adds to the
    `people grounded n of n` count (sf_people_line). Returns the number grounded."""
    tol = SF_PEOPLE["tol_mm"] if tol is None else tol
    ok = 0
    for i, sh in enumerate(items or ()):
        b = _sf_base(sh)
        if b is None:
            continue
        hw = 0.5 * (b[2] - b[1]) if half_w is None else half_w
        g = max(_sf_fn(gy)(b[1]), _sf_fn(gy)(b[2]), _sf_fn(gy)(0.5 * (b[1] + b[2])))
        if half_w is not None:
            g = max(_sf_fn(gy)(0.5 * (b[1] + b[2]) - hw), _sf_fn(gy)(0.5 * (b[1] + b[2]) + hw), g)
        d = b[0] - g
        SF_PEOPLE["seen"] += 1
        if abs(d) <= tol:
            ok += 1
            SF_PEOPLE["grounded"] += 1
        else:
            _sf_warn(page, "people", u"person %d %s %.2f mm at x %.1f" % (i, u"floats" if d > 0 else u"sunk", abs(d),
                                                                         0.5 * (b[1] + b[2])))
    return ok


def sf_people_line():
    """the done-when log line `people grounded n of n` (G-R5-4.8); None when no person was seated or checked"""
    if not SF_PEOPLE["seen"]:
        return None
    return u"people grounded %d of %d" % (SF_PEOPLE["grounded"], SF_PEOPLE["seen"])


# ---- activity guards (round 5, S3; G-R5-4.4, PLAN §8 rule for all): fishing and wading only where water is drawn --
SF_DRY_MONTHS = (7, 8, 9)            # p10: the summer bed "dry or 3 cm Jul-Sep" -> no fishing, no wading Jul-Sep
SF_WADE_MAX_M = 0.50                 # PLAN §3 People: wading only in water <= 0.50 m (figures.py FIG_WADE_MAX_M)


def sf_activity_ok(kind, ground_y=None, water_y=None, k=None, month=None, strip=False, page=None, what=u""):
    """(ok, reason): may a person do `kind` ("fish", "wade", anything else = True) at a spot whose ground is at page
    y ground_y with the drawn water surface at water_y (page y, None = no water drawn there), k mm per m, in month
    (1-12, None = no season shown)? Fishing: water drawn at the spot (the line ends in it) and not a dry month unless
    `strip` (the summer strip whose water is drawn). Wading: water drawn and its depth <= SF_WADE_MAX_M. A refusal is
    a WARNING (`<page> activity`) so the page draws a walker or watcher instead (P05.1)."""
    if kind not in ("fish", "fishing", "wade", "wading"):
        return True, u""
    why = None
    if water_y is None:
        why = u"no water drawn"
    elif month is not None and int(month) in SF_DRY_MONTHS and not strip:
        why = u"month %d: the bed is dry or 3 cm (p10)" % int(month)
    elif kind in ("wade", "wading") and ground_y is not None and k:
        dep = (water_y - ground_y) / float(k)
        if dep > SF_WADE_MAX_M + 1e-6:
            why = u"water %.2f m deep > %.2f m" % (dep, SF_WADE_MAX_M)
        elif dep <= 0.0:
            why = u"ground above the water"
    if why:
        _sf_warn(page, "activity", u"%s %s refused: %s" % (kind, what, why))
        return False, why
    return True, u""


# ---- trees at a middle level (round 5, S3, G-R5-4.5, U37 / U40 / U65) -------------------------------------------
# Where the drawing is not about plants or seasons, trees stand behind the people and lighter (depth layer 1, r3
# G15); where it is (p15, p18, p19-20) trees lead (layer 0). Never squeezed or thinned; shrubs in every section.
SF_TREE_LEAD_PAGES = ("p15", "p18", "p19", "p20")


def sf_tree_level(page):
    """dict(layer, lead) for the trees of a drawing on page (23-page id): layer 0 + lead True on the plant / season
    pages, else layer 1 (behind the people, paler: figures.py fig_fade / plants.py layer tones)"""
    lead = (u"%s" % page) in SF_TREE_LEAD_PAGES
    return dict(layer=0 if lead else 1, lead=lead)


def _sf_pts(s):
    t = s[0]
    if t in ("poly", "line"):
        return list(s[1])
    if t == "image":
        x0, y0, w, h = s[1:5]
        return [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]
    return []


def _sf_move(s, dy):
    t = s[0]
    if t in ("poly", "line"):
        return (t, [(x, y + dy) for x, y in s[1]]) + tuple(s[2:])
    if t == "image":
        return tuple(s[:2]) + (s[2] + dy,) + tuple(s[3:])
    if t == "text":
        return tuple(s[:3]) + (s[3] + dy,) + tuple(s[4:])
    return s


def _sf_base(shapes, base_w=None):
    """(bottom y, x0, x1) of an item's base: images = their centre 40 % (trimmed cutouts: feet / trunk in the
    middle), drawings = the points within 4 % of the item's height above its bottom; base_w (mm) overrides"""
    pts = [p for s in shapes for p in _sf_pts(s)]
    if not pts:
        return None
    y0 = min(p[1] for p in pts)
    h = max(p[1] for p in pts) - y0
    if base_w is None:
        ims = [s for s in shapes if s[0] == "image"]
        if ims and len(ims) == len([s for s in shapes if _sf_pts(s)]):
            xa, xb = min(s[1] for s in ims), max(s[1] + s[3] for s in ims)
            c, hw = 0.5 * (xa + xb), 0.2 * (xb - xa)
            return y0, c - hw, c + hw
        low = [p[0] for p in pts if p[1] <= y0 + 0.04 * h + 1e-6]
        return y0, min(low), max(low)
    xs = [p[0] for p in pts]
    c = 0.5 * (min(xs) + max(xs))
    return y0, c - 0.5 * base_w, c + 0.5 * base_w


def sf_seat(shapes, gy, base_w=None, tol=0.05, sink=False):
    """G14 for any drawn item (cutout image, drawn figure, plant, stall, background house: one item's shapes): moves
    it down onto the lowest ground under its base (only down: a wading figure or a plinth set lower on purpose
    stays; sink=True also lifts an item buried below that ground). Counted in sf_g14_line. Returns the shapes."""
    b = _sf_base(shapes, base_w)
    if b is None:
        return shapes
    y0, xa, xb = b
    g = sf_ground_min(gy, xa, xb)
    key = (round(0.5 * (xa + xb), 2), round(g, 2))
    SF_G14["seen"].add(key)
    dy = g - y0
    if dy < -tol or (sink and dy > tol):
        SF_G14["moved"].add(key)
        SF_G14["max_mm"] = max(SF_G14["max_mm"], abs(dy))
        return [_sf_move(s, dy) for s in shapes]
    return shapes


def sf_seat_box(xa, xb, gy):
    """G14 for a house drawn by its base: the y its walls start at = the lowest ground of its own layer's profile
    under [xa, xb] (pass the profile of the house's depth layer, sf_back_profile, not the cut line)"""
    return sf_seat_x(gy, 0.5 * (xa + xb), 0.5 * abs(xb - xa))


def sf_back_profile(bases, x0, x1):
    """the ground line of one background depth layer through its items' own bases [(xa, xb, base_y)] (page mm:
    each house's ground from the survey): flat under each item, straight between neighbours, flat out to x0 / x1.
    Draw it with sf_topo_back so the houses visibly stand on it, and seat them with sf_seat_box on it."""
    pts = []
    for xa, xb, y in sorted(bases, key=lambda b: 0.5 * (b[0] + b[1])):
        pts += [(min(xa, xb), y), (max(xa, xb), y)]
    if not pts:
        return []
    pts.sort()
    return [(x0, pts[0][1])] + pts + [(x1, pts[-1][1])]


SF_BACK = dict(fill="E6E3DD", line="CFCBC2", roof="DAD6CE", lw=0.08)   # round 4 (S2, G-R4-5.3): background houses
SF_BACK_WIN_M = 30.0                # m behind the cut: farther houses get no windows (drawing rule, PLAN §4.7)


def sf_back_house(xa, xb, gy, h_m, k, layer=1, floors=None, roof="hip", fill=None, ink=None, d_m=None):
    """G14 + G7 + M8: a background house in elevation (not a rectangle): walls h_m (data height, m) high standing
    on the lowest ground of its layer's profile gy under it, a window per bay and storey (sill 0.90 m, head 2.10 m:
    the repo's bld_section_profile values; bay 3.0 m and window 1.20 m wide: drawing rules), a hipped roof at the
    repo's BLD_PITCH (M11 convention, not surveyed; "flat" = 0.60 m parapet), eaves 0.30 m; true size (an
    elevation: k is not reduced). Round 4 v2 (S2, G-R4-5.3): ONE pale tone at every depth (SF_BACK: no darker layer),
    windows only within SF_BACK_WIN_M behind the cut: d_m = the house's distance behind the cut (sf_back_buildings
    gives it); without d_m only depth layer 1 gets windows. fill / ink override the tones. Returns house shapes."""
    import math as _m
    wall = fill or SF_BACK["fill"]
    line = ink or SF_BACK["line"]
    rf = SF_BACK["roof"]
    win = (d_m <= SF_BACK_WIN_M) if d_m is not None else layer <= 1
    xa, xb = min(xa, xb), max(xa, xb)
    y0 = sf_seat_box(xa, xb, gy)
    yt = y0 + h_m * k
    sh = [("poly", [(xa, y0), (xb, y0), (xb, yt), (xa, yt)], wall, line, SF_BACK["lw"])]
    w_m = (xb - xa) / k
    nf = int(floors) if floors else max(1, int(round(h_m / globals().get("BLD_STOREY", 3.0))))
    st = h_m / float(nf)
    nb = max(1, int(w_m // 3.0))
    if win and st >= 2.4 and w_m >= 2.4:
        bw = (xb - xa) / nb
        for i in range(nf):
            for j in range(nb):
                cx = xa + (j + 0.5) * bw
                wy0, wy1 = y0 + (i * st + 0.9) * k, y0 + (i * st + 2.1) * k
                ww = min(1.2 * k, 0.6 * bw)
                sh.append(("poly", [(cx - ww / 2, wy0), (cx + ww / 2, wy0), (cx + ww / 2, wy1), (cx - ww / 2, wy1)],
                           line, None, 0.05))
    if roof == "flat":
        sh.append(("poly", [(xa, yt), (xb, yt), (xb, yt + 0.6 * k), (xa, yt + 0.6 * k)], wall, line, SF_BACK["lw"]))
    else:
        t = _m.tan(_m.radians(globals().get("BLD_PITCH", 30.0)))
        run = min(0.5 * (xb - xa) + 0.3 * k, 4.0 * k)
        rise = t * run
        e = 0.3 * k
        sh.append(("poly", [(xa - e, yt), (xb + e, yt), (xb + e - run, yt + rise), (xa - e + run, yt + rise)], rf, line,
                   SF_BACK["lw"]))
    return sh


SF_BACK_BAND = (8.0, 120.0)   # m behind a cut where background houses are taken from (drawing rule, R2-C)


def sf_back_buildings(cid, t0, t1, d0=None, d1=None, log=None, look=1):
    """R2-C (checklist 7, Aras 31 Oct 12:01 "no background houses"): the basemap buildings standing d0..d1 m behind
    the registry cut cid (the way the section looks: the normal (-u_y, u_x) of its ends, as the page key maps), each
    projected onto the cut: [(t_a, t_b m along the cut, h m, floors or None, d m behind)], farthest first, clipped to
    t0..t1. Height: the building's data height, else the repo's M11 convention floors x BLD_STOREY (buildings.py
    _bld_h, as every cut-through building). Draw with sf_back_house on the depth layer's ground (d < half the band:
    layer 1, else 2). look=-1: the drawing looks the other way (its first end on the right, as the p.12 W cuts and
    their key map, basemap_cut_ids looks=-1)."""
    import math as _m
    d0 = SF_BACK_BAND[0] if d0 is None else d0
    d1 = SF_BACK_BAND[1] if d1 is None else d1
    D = basemap_load(log=log) if globals().get("basemap_load") else None
    L = (D or {}).get("layers") or {}
    a, b = level_ends(cid)
    Lc = _m.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    u = ((b[0] - a[0]) / Lc, (b[1] - a[1]) / Lc)
    f = (-u[1] * look, u[0] * look)
    out = []
    for bl in L.get("buildings", []):
        h = _bld_h(bl) if globals().get("_bld_h") else float(bl.get("h") or 0.0)
        if h <= 0.0:
            continue
        P = [p_ for R_ in bl["rings"][:bl.get("np", len(bl["rings"]))] for p_ in R_]
        if len(P) < 3:
            continue
        ts = [(p_[0] - a[0]) * u[0] + (p_[1] - a[1]) * u[1] for p_ in P]
        ds = [(p_[0] - a[0]) * f[0] + (p_[1] - a[1]) * f[1] for p_ in P]
        dn = min(ds)
        if dn < d0 or dn > d1:
            continue
        ta, tb = max(t0, min(ts)), min(t1, max(ts))
        if tb - ta < 2.0:
            continue
        out.append((ta, tb, round(h, 2), int(bl.get("floors") or 0) or None, dn))
    out.sort(key=lambda r: -r[4])
    if log is not None:
        log.append(u"background houses {}: {} buildings {:.0f}-{:.0f} m behind the cut".format(cid, len(out), d0, d1))
    return out


def sf_assert_g14(items, gy, tol=0.2, strict=True):
    """G14 check by reasoning: items = [shapes of one item, ...] all on ground gy; an item whose base is more than
    tol mm above the lowest ground under it floats. strict: AssertionError listing them; else the messages."""
    bad = []
    for i, sh in enumerate(items):
        b = _sf_base(sh)
        if b is None:
            continue
        g = sf_ground_min(gy, b[1], b[2])
        if b[0] - g > tol:
            bad.append(u"G14: item %d floats %.2f mm over x %.1f-%.1f" % (i, b[0] - g, b[1], b[2]))
    if bad and strict:
        raise AssertionError(u"; ".join(bad))
    return bad


def sf_g14_line():
    """one log line: items seated by G14 and how many were moved onto the ground (None when nothing was seated)"""
    if not SF_G14["seen"]:
        return None
    s = u"G14 grounding: %d items seated, %d moved onto the ground (max %.1f mm)" % (
        len(SF_G14["seen"]), len(SF_G14["moved"]), SF_G14["max_mm"])
    if SF_G14["refused"]:
        s += u"; no people placed in: " + u", ".join(u"%s (%d)" % kv for kv in sorted(SF_G14["refused"].items()))
    return s


# ---- G14 / U22 meaningless triangles: switches (the cut-direction triangles of key maps are not touched) ---------
# walls: the small triangle that marks a surveyed wall (no height) on a section's ground (p4-5);
# aggregate: the open triangles of the concrete hatch (section_parts sct_hatch_fill; dots stay).
SF_TRI = dict(walls=True, aggregate=True)


def sf_triangles(walls=None, aggregate=None):
    """switch the section triangles on / off for what follows; returns the previous state (sf_triangles(**old)
    restores it). Pages switch them off (G14 round 2)."""
    old = dict(SF_TRI)
    if walls is not None:
        SF_TRI["walls"] = bool(walls)
    if aggregate is not None:
        SF_TRI["aggregate"] = bool(aggregate)
    return old


def sf_wall_mark(x, y, h, fill=None):
    """the surveyed-wall mark at (x, y): a triangle h high (its legend must say so); [] when SF_TRI walls is off"""
    if not SF_TRI["walls"]:
        return []
    return [("poly", [(x, y + h), (x - 0.6 * h, y), (x + 0.6 * h, y)], fill or SEC["ink2"], None, 0.1)]


# ---- sky v2 (round 4 S2, G-R4-5.3, U06 "background and sky looks weird"; PLAN §4.7) --------------------------------
# D8 answer (PLAN.md round 2): default a = every section and perspective. sky="d8" / True / "designed" in
# sf_atmosphere all draw this sky.
SF_SKY_DEFAULT = "designed"
# The sky sits back: the paper stays white; only the top SF_SKY["wash_h"] of the drawing's height above its lowest
# ground carries one very light vertical wash (wash_top at the top edge -> paper at the wash's foot); 2-3 OPEN cloud
# contours (a long low top line, no fill, no base line) in a pale cool grey; 2-4 birds in a pale grey. Nothing in the
# sky is darker than the muted base-map houses (map_layers / basemap BM_MUTED: bld EDEBE6, edge C9C5BC). Drawing rules,
# not data. Six fixed arrangements; a cut id keeps its arrangement and neighbouring cuts of a page never share one.
SF_SKY = dict(wash_h=0.30, bands=8, paper="FFFFFF", wash_top="F3F5F6", cloud="C9CFD3", cloud_lw=0.10, bird="C4CACE",
              cloud_w_max=45.0, cloud_h_max=3.0)
SF_SKY_VARIANTS = (                 # cloud centres (x as a fraction of the width, y as a fraction of the height above
    dict(x=(0.18, 0.66), y=(0.86, 0.74), w=(0.24, 0.20), birds=3),          # the lowest ground), widths (fraction of
    dict(x=(0.10, 0.45, 0.80), y=(0.78, 0.89, 0.72), w=(0.18, 0.22, 0.16), birds=2),   # the width), birds
    dict(x=(0.30, 0.80), y=(0.72, 0.86), w=(0.26, 0.18), birds=4),
    dict(x=(0.12, 0.40, 0.72), y=(0.84, 0.70, 0.80), w=(0.16, 0.20, 0.22), birds=3),
    dict(x=(0.55, 0.88), y=(0.82, 0.71), w=(0.28, 0.16), birds=2),
    dict(x=(0.14, 0.50), y=(0.70, 0.83), w=(0.22, 0.26), birds=3),
)
SF_SKY_USED = {}                    # cut id -> variant (a cut keeps its sky wherever it is drawn)
SF_SKY_RECENT = []                  # the last variants handed out: neighbours on a page never share one
SF_LOG = []                         # "sky variant <cid> v<n>", inset and level-mark lines (sec_look_lines)


def sf_sky_variant(cid=None):
    """the sky variant (0-5) of a section: a cut id keeps one variant for the run (hash of the id), moved on while it
    equals one of the last five handed out, so the sections of one page never share a sky; no cid -> the next in
    rotation. Logged once per cut as "sky variant <cid> v<n>"."""
    n = len(SF_SKY_VARIANTS)
    if cid is not None and cid in SF_SKY_USED:
        return SF_SKY_USED[cid]
    if cid is not None:
        v = sum((i + 1) * ord(ch) for i, ch in enumerate(u"%s" % cid)) % n
    else:
        v = (SF_SKY_RECENT[-1] + 1) % n if SF_SKY_RECENT else 0
    for _i in range(n):
        if v not in SF_SKY_RECENT[-(n - 1):]:
            break
        v = (v + 1) % n
    SF_SKY_RECENT.append(v)
    key = cid if cid is not None else u"section %d" % len(SF_SKY_RECENT)
    SF_SKY_USED[key] = v
    SF_LOG.append(u"sky variant %s v%d" % (key, v + 1))
    return v


def _sf_cloud(cx, cy, w, hb, rnd, col, lw):
    """sky v2: one OPEN cloud contour: a long low top line of 2-3 shallow swells, its ends easing down to the cloud's
    foot (no base line, no fill), and a short loose stroke under it"""
    import math as _m
    m = 2 + int(rnd() * 1.999)
    pts = []
    n = 40
    ph = [0.6 + 0.8 * rnd() for _i in range(m)]
    for j in range(n + 1):
        t = j / float(n)
        env = _m.sin(_m.pi * t) ** 0.6                       # ends ease down to the foot
        sw = sum(ph[i] * max(0.0, _m.sin(_m.pi * (t * m - i))) for i in range(m)) / max(ph)
        pts.append((cx - 0.5 * w + w * t, cy + hb * env * (0.45 + 0.55 * sw)))
    x0 = cx - 0.5 * w + w * (0.15 + 0.2 * rnd())
    return [("line", pts, col, lw), ("line", [(x0, cy - 0.35 * hb), (x0 + w * (0.35 + 0.2 * rnd()), cy - 0.35 * hb)],
                                     col, lw)]


def sf_sky(x0, x1, y0, y_top, seed=0, clouds=True, tone=None, cid=None, birds=True, variant=None):
    """sky v2 (round 4 S2, G-R4-5.3) behind a section or perspective: paper white, one very light vertical wash
    (SF_SKY wash_top -> paper) over the top SF_SKY["wash_h"] of y0 (page y, the lowest ground) .. y_top, 2-3 open
    cloud contours and 2-4 pale birds after one of SF_SKY_VARIANTS (variant, else sf_sky_variant(cid): no two
    sections of a page share one). tone: kept for old calls, no effect (the sky never takes a page colour). Draw it
    first (behind the ground). Returns shapes."""
    v = SF_SKY_VARIANTS[(variant if variant is not None else sf_sky_variant(cid)) % len(SF_SKY_VARIANTS)]
    H, W = y_top - y0, x1 - x0
    if W <= 1.0 or H <= 1.0:
        return []
    ys = y_top - SF_SKY["wash_h"] * H
    n = int(SF_SKY["bands"])
    sh = []
    for i in range(n):                                   # the wash: paper at its foot, wash_top at the top edge
        ya = ys + (y_top - ys) * i / float(n)
        yb = ys + (y_top - ys) * (i + 1) / float(n) + (0.05 if i < n - 1 else 0.0)
        sh.append(("poly", [(x0, ya), (x1, ya), (x1, yb), (x0, yb)],
                   _sec_mix(SF_SKY["paper"], SF_SKY["wash_top"], (i + 0.5) / n), None, 0.0))
    if clouds:
        rnd = _wat_rng(seed + 211)
        for fx, fy, fw in zip(v["x"], v["y"], v["w"]):
            w = min(fw * W, SF_SKY["cloud_w_max"])
            hb = min(0.08 * w, SF_SKY["cloud_h_max"], 0.10 * H)
            cx = min(max(x0 + fx * W, x0 + 0.55 * w), x1 - 0.55 * w)
            cy = min(y0 + fy * H, y_top - 1.2 * hb)
            sh += _sf_cloud(cx, cy, w, hb, rnd, SF_SKY["cloud"], SF_SKY["cloud_lw"])
    if birds and v["birds"]:
        sh += sf_birds(x0 + 0.08 * W, x1 - 0.08 * W, y0 + 0.55 * H, y0 + 0.92 * H, seed=seed, n=v["birds"])
    return sh


# ---- D3 birds (round 3 G15): a few architectural silhouettes, generic until research/fauna.md exists ------------
# Shapes in units of the bird's wingspan (drawing rules; page size SF_BIRD_MM, a symbol, not to scale): gliding,
# wings up, wings down; filled in a faded ink, opaque, like R05 / R07. Counted for the fauna FLAG (figures.py).
SF_BIRD_MM = (1.6, 3.0)             # page mm: wingspan range of the symbols
SF_BIRD_SHAPES = {
    "glide": [(-0.50, 0.04), (-0.22, 0.06), (-0.06, 0.02), (0.00, 0.05), (0.06, 0.02), (0.22, 0.06), (0.50, 0.04),
              (0.20, 0.00), (0.07, -0.03), (0.00, -0.07), (-0.07, -0.03), (-0.20, 0.00)],
    "up": [(-0.42, 0.30), (-0.20, 0.12), (-0.05, 0.02), (0.00, 0.05), (0.05, 0.02), (0.20, 0.12), (0.42, 0.30),
           (0.18, 0.02), (0.06, -0.04), (0.00, -0.09), (-0.06, -0.04), (-0.18, 0.02)],
    "down": [(-0.45, -0.18), (-0.22, -0.02), (-0.06, 0.04), (0.00, 0.07), (0.06, 0.04), (0.22, -0.02), (0.45, -0.18),
             (0.20, -0.08), (0.07, -0.03), (0.00, -0.06), (-0.07, -0.03), (-0.20, -0.08)],
}


def sf_birds(x0, x1, y0, y1, seed=0, n=None, ink=None, size=None):
    """2-5 generic bird silhouettes (D3) flying in the box x0..x1, y0..y1 (page mm): varied poses and sizes,
    loosely grouped (never a row); n fixes the count, size (mm) the wingspan. Fauna stays generic until
    research/fauna.md exists (figures.py fig_flag_lines logs "FLAG fauna pending research"). Returns shapes."""
    if x1 - x0 <= 1.0 or y1 - y0 <= 0.5:
        return []
    rnd = _wat_rng(seed + 77)
    ink = ink or SF_SKY["bird"]                          # round 4 sky v2: pale, never darker than the base houses
    cnt = n if n is not None else 2 + int(rnd() * 3.999)
    gx = x0 + (0.15 + 0.7 * rnd()) * (x1 - x0)                 # the flock's centre
    gy = y0 + (0.3 + 0.5 * rnd()) * (y1 - y0)
    keys = ("glide", "up", "down")
    sh = []
    for i in range(cnt):
        s = size or (SF_BIRD_MM[0] + (SF_BIRD_MM[1] - SF_BIRD_MM[0]) * rnd())
        bx = min(max(gx + (rnd() - 0.5) * 0.30 * (x1 - x0) + i * 0.9 * s * (1 if rnd() > 0.5 else -1), x0 + s), x1 - s)
        by = min(max(gy + (rnd() - 0.5) * 0.6 * (y1 - y0), y0), y1)
        tilt = (rnd() - 0.5) * 0.5
        shp = SF_BIRD_SHAPES[keys[(i + int(rnd() * 3)) % 3]]
        sh.append(("poly", [(bx + s * (px - tilt * py), by + s * (py + tilt * px)) for px, py in shp], ink, None, 0.0))
    if globals().get("FIG_FAUNA_DRAWN") is not None:
        FIG_FAUNA_DRAWN[0] += cnt
    return sh


def sec_look_lines():
    """the round 3 section-look log lines for a page's log: sky variants handed out, the plants line (no alpha, bare
    species), the fauna FLAG while research/fauna.md is missing"""
    out = []
    if SF_LOG:
        out.append(u"; ".join(SF_LOG))
    for ln in (globals().get("PLA_LOG") or ()):
        if ln.startswith(u"plants: no alpha"):
            out.append(ln)
    f = globals().get("pla_log_lines")      # round 4 (S3): willow v2 drawn, plants by species / season, colour FLAG
    if f:
        out += f()
    f = globals().get("fig_flag_lines")
    if f:
        out += f()
    out += sf_kit_lines()
    return out


def sf_kit_lines():
    """round 5 (S3) section kit v2 done-when lines (G-R5-4.8): materials solid, `widths 0`, `people grounded n of
    n`, the bridge lines (bridges.py), once per run (the counters are not reset: the last page's call has them all)"""
    out = []
    sl = globals().get("SCT_LOG")
    if sl:
        out.append(u"section materials solid: %d cut rings flat colour, %d with inset joints, hatches 0"
                   % (sl["solid"], sl["detail"]))
    out.append(sf_widths_line())
    pl = sf_people_line()
    if pl:
        out.append(pl)
    f = globals().get("br_log_lines")
    if f:
        out += f()
    return out


def sf_atmosphere(x0, x1, gy, y_top, k, seed=0, sky=True, trees=True, birds=True, mix=None, t0=0.45, t1=0.95,
                  density=0.7, style="b", into=None, back_ground=None, groups=True, water=None, cid=None, month=None):
    """the atmosphere behind a section (p17; R16, R19 idea): a sky from the ground line gy (number, function of x
    or polyline) up to y_top, faded depth trees in D9 layers 2 and 1 (band t0..t1), a few birds. Into "atmosphere"
    (sky, birds) and "background" (trees). sky: "designed" (D8: sf_sky, gradient + soft clouds), "d8" (the D8 answer,
    SF_SKY_DEFAULT), True (the older calm three bands), False (none). R2-A 31 Oct (G14, G9): back_ground = {layer:
    profile} gives each depth layer its own ground (drawn with sf_topo_back, farthest first) and the trees stand on
    it, else on gy; every tree is seated on the lowest ground under it (sf_seat_x); groups=True plants mixed groups
    (plants.py pla_group_section) instead of the single scatter; water (page y or function of x): no tree where the
    ground of its layer lies under it. Round 3 (G15): cid = the cut id that picks the sky variant (sf_sky_variant);
    birds = sf_birds (D3); month (1-12) draws the depth trees in that month's colours / bare (plants.py pla_colour).
    Returns the WaterLayers."""
    wl = into if into is not None else water_layers()
    gf = _sf_fn(gy)
    g0 = min(gf(x0), gf(x1), sf_ground_min(gf, x0, x1, 24))
    if sky is True or sky == "d8":                       # round 4 (S2): every sky is sky v2 (the old bands retired)
        sky = SF_SKY_DEFAULT
    if sky == "designed":
        wl.add("atmosphere", sf_sky(x0, x1, g0, y_top, seed=seed, cid=cid, birds=False))
    if back_ground:
        bot = min(min(p[1] for p in pr) for pr in back_ground.values()) - 1.0
        lays = sorted(back_ground, reverse=True)
        sf_topo_back([back_ground[l_] for l_ in lays], bot, into=wl)
    if trees:
        for layer in (2, 1):
            g_ = sf_gy(back_ground[layer]) if back_ground and layer in back_ground else gf
            if groups:
                sh, _pl, _gr = pla_group_section(x0, x1, g_, k, t0=t0, t1=t1, mix=mix, seed=seed + 31 * layer,
                                            layers=(layer,), style=style, density=density, hires=False, detail=False,
                                            water=water, month=month)
            else:
                sh, _pl = pla_scatter_section(x0, x1, sf_ground_fn(g_, 0.4 * k), k, t0=t0, t1=t1, mix=mix,
                                              seed=seed + 31 * layer, layer=layer, style=style, density=density,
                                              hires=False, detail=False, month=month)
            wl.add("background", sh)
    if birds:
        wl.add("atmosphere", sf_birds(x0, x1, g0 + 0.55 * (y_top - g0), g0 + 0.95 * (y_top - g0), seed=seed))
    return wl


# ---- numbered callouts (R07, R19 idea) ------------------------------------------------------------------------------
class SfCallouts(object):
    """numbered callouts of one drawing: add(x, y, text) -> its number; marks(size) = the numbered circles; key(x, y,
    size) = the numbered list beside the drawing (G1: every number explained)"""

    def __init__(self, start=1):
        self.items, self.n0 = [], start

    def add(self, x, y, text):
        for n, _x, _y, t in self.items:                # the same element twice keeps one number
            if t == text:
                self.items.append((n, x, y, t))
                return n
        n = self.n0 + len(set(t for _n, _x, _y, t in self.items))
        self.items.append((n, x, y, text))
        return n

    def marks(self, size=1.8, ink=None, fill="FFFFFF"):
        ink = ink or SEC["ink"]
        sh = []
        mk = globals().get("mk_marker")                  # round 4 (S2, G-R4-7): the one marker function (S1 marker.py)
        for n, x, y, _t in self.items:
            if callable(mk):
                sh += list(mk(x, y, u"%d" % n, ink, size_pt=max(7.0, size / 0.3528), style="ring")[0])
                continue
            r = 0.75 * size
            sh += [("poly", sec_ellipse(x, y, r, r, 20), fill, ink, 0.15),
                   ("text", u"%d" % n, x, y - 0.36 * size, 0.85 * size, ink, True, "C")]
        return sh

    def key(self, x, y, size=1.8, ink=None, gap=None):
        """the numbered list: one row per number from (x, y) down (y up), gap apart; ink = the caller's colour (else
        SEC ink). Round 4 closing (G-R4-7): each number is the shared marker (marker.py mk_marker, style "ring" as
        .marks: the glyph centred on its ink box, at least 7 pt), its disc centred 0.4 x size above the row's
        baseline and at least its radius in from x; the row's words start 2 x size in (further only when the disc
        is wider). Returns house shapes, as before."""
        ink = ink or SEC["ink"]
        gap = gap or 1.5 * size
        pt = max(7.0, size / 0.3528)
        seen, sh, yy = set(), [], y
        for n, _x, _y, t in sorted(self.items):
            if n in seen:
                continue
            seen.add(n)
            cy = yy - 0.4 * size
            shp, _box, r = mk_marker(x + 0.75 * size, cy, u"%d" % n, ink, size_pt=pt, style="ring")
            if r > 0.75 * size:                          # a wider disc (two digits) moves in to keep x its left edge
                shp, _box, r = mk_marker(x + r, cy, u"%d" % n, ink, size_pt=pt, style="ring")
            sh += list(shp)
            sh.append(("text", t, max(x + 2.0 * size, x + 2.0 * r + 0.4 * size), yy - 0.76 * size, size, ink, False,
                       "L"))
            yy -= gap
        return sh


def sf_width_label(x0, x1, y, width_m, size=2.47, ink=None, unit=True):
    """RETIRED in round 5 (S3, G-R5-4.6, U49 "remove the horizontal dimensions all together ... in all of the
    drawings"): draws nothing, returns []; every call is counted (sf_widths_line). Kept so old calls still run."""
    SF_WIDTHS["calls"] += 1
    return []


# ---- no widths anywhere (round 5, S3, G-R5-4.6): every text a section or its list prints goes through
# sf_strip_widths (item_export Ix.text calls it for every exported text, so page code needs no change): a width in
# cm ("Footway 456 cm", "bed 3,260 cm", "Bike · 300 cm"), a "W x H cm/m" size ("8 x 40 cm seats", "olives 500 x 700
# cm", "rows 7 x 5 m") and a lone "N cm" go with the separator before them; names, heights in m with 2 decimals
# ("+43.71", "2.50 m") and scale texts stay. A value in cm is never a height in this project (units rule: heights in m,
# 2 decimals), so every cm value is a width. Log `widths 0` (none left) or the strips counted.
SF_WIDTHS = dict(calls=0, stripped=0, examples=[])
_SF_W_RE = None


def _sf_w_re():
    global _SF_W_RE
    if _SF_W_RE is None:
        import re as _re
        num = r"\d[\d,.]*"
        _SF_W_RE = (
            # "8 x 40 cm seats", "500 × 700 cm", "rows 7 × 5 m", "400 x 30 cm" (a size pair: always a width)
            _re.compile(r"\s*(?:[·,:;\-–—]\s*)?(?:\(\s*)?" + num + r"\s*(?:cm|m)?\s*[x×]\s*" + num +
                        r"\s*(?:cm|m)\b\)?", _re.U),
            # "1,580 cm", "· 300 cm", "(456 cm)"
            _re.compile(r"\s*(?:[·,:;\-–—]\s*)?(?:\(\s*)?" + num + r"\s*cm\b\)?", _re.U),
        )
    return _SF_W_RE


def sf_strip_widths(s, page=None):
    """s without any horizontal dimension (see the notes above); counted in SF_WIDTHS. Non-strings pass through."""
    if not isinstance(s, str) or (u"cm" not in s and u"×" not in s and u" x " not in s):
        return s
    t = s
    for rx in _sf_w_re():
        t = rx.sub(u"", t)
    if t != s:
        import re as _re
        t = _re.sub(r"\s{2,}", u" ", t)
        t = _re.sub(r"\s*[·,:;\-–—]\s*$", u"", t).strip()
        t = _re.sub(r"^\s*[·,:;\-–—]\s*", u"", t)
        SF_WIDTHS["stripped"] += 1
        if len(SF_WIDTHS["examples"]) < 6:
            SF_WIDTHS["examples"].append(u"%s -> %s" % (s, t or u"(nothing)"))
    return t


def sf_widths_line():
    """the done-when log line: `widths 0` when no width was drawn or printed; else what was stripped (they are gone
    from the page; the line lets the page session find and delete the source strings)"""
    n = SF_WIDTHS["stripped"] + SF_WIDTHS["calls"]
    if not n:
        return u"widths 0"
    return u"widths 0 (removed this run: %d width texts, %d width chains; e.g. %s)" % (
        SF_WIDTHS["stripped"], SF_WIDTHS["calls"], u"; ".join(SF_WIDTHS["examples"]))


# ---- level markers beside the section (round 5, S3, G-R5-4.3, Aras's sketch refs/U04; replaces G-R4-5.4) ---------
# PLAN §3 "Level marker": a short horizontal mark beside the section, SF_LEVEL["gap"] >= 3 mm clear of the drawing's
# outer edge: long dash 3.5 mm, gap 0.8, short dash 0.8, gap 0.8, dash 3.1 mm ending under an open downward triangle
# (2.2 mm wide, 1.4 mm high, apex on the line at its outer end); the value "+43.71 Q100" (m, 2 decimals, 4.5 pt) beyond
# the triangle; stacked markers keep their lines at their levels and spread their labels >= 0.8 mm apart (a hairline
# joins a moved label). In the round 5 booklet the markers are drawn by the composer (pl_levels): a content script
# exports them with sf_level_items (Ix.levels) and draws nothing; sf_level_marks stays for pages still drawing
# themselves and draws the same marker.
SF_LEVEL = dict(gap=3.0, dashes=(3.5, 0.8, 0.8, 0.8, 3.1), tri_w=2.2, tri_h=1.4, size=4.5 * 25.4 / 72.0, lw=0.15,
                clear=0.8, label_gap=0.6)
SF_LEVEL_NAMES = dict(q500=u"Q500", q100=u"Q100", avg=u"mean flow", mean=u"mean flow", bed=u"bed")


def _sf_level_rows(levels, y_of, y0, y1, page):
    Pa = _wat_pal_sec() if globals().get("_wat_pal_sec") else {}
    rows = []
    for lv in levels or ():
        key, val = lv[0], float(lv[1])
        y = lv[2] if len(lv) > 2 and lv[2] is not None else (y_of(val) if y_of else None)
        if y is None:
            _sf_warn(page, "levels", u"level %r has no page y and no y_of: not marked" % (key,))
            continue
        if y0 is not None and (y < y0 - 1e-6 or y > y1 + 1e-6):
            _sf_warn(page, "levels", u"%s %+.2f lies outside the drawing's height: not marked" % (key, val))
            continue
        rows.append((y, key, val, Pa.get(key) or (SCT_WATER["surface"] if "SCT_WATER" in globals() else SEC["ink"])))
    rows.sort(key=lambda r: -r[0])
    return rows


def sf_level_marks(frame_box, levels, side="R", y_of=None, size=None, cols=None, page=None):
    """the level markers of one section beside its drawing (G-R5-4.3, U04). frame_box = (x0, y0, x1, y1) page mm
    (y up) of the drawing's outer edge; levels = [(key or name, level m[, page y])] (water_section's
    wl.anchors["levels"]); keys q500 / q100 / avg / mean / bed are named by SF_LEVEL_NAMES, any other key prints as
    given. side "R" (default) or "L" (mirrored). cols = {key: hex} overrides the water colours. Logs
    "levels <page> gap ok ..." in SF_LOG. Returns shapes (lines, open triangles, value texts)."""
    x0, y0, x1, y1 = frame_box
    size = size or SF_LEVEL["size"]
    rows = _sf_level_rows(levels, y_of, y0, y1, page)
    sgn = 1.0 if side == "R" else -1.0
    xs = (x1 if side == "R" else x0) + sgn * SF_LEVEL["gap"]           # the line starts gap mm off the drawing
    L = sum(SF_LEVEL["dashes"])
    tw, th, lw = SF_LEVEL["tri_w"], SF_LEVEL["tri_h"], SF_LEVEL["lw"]
    sh = []
    xt = xs + sgn * (L + 0.5 * tw + SF_LEVEL["label_gap"])           # labels start beyond the triangle
    last = None
    moved = 0
    for y, key, val, col in rows:
        col = (cols or {}).get(key) or col
        pos = 0.0
        for i, d in enumerate(SF_LEVEL["dashes"]):                    # dash, gap, dash, gap, dash
            if i % 2 == 0:
                sh.append(("line", [(xs + sgn * pos, y), (xs + sgn * (pos + d), y)], col, lw))
            pos += d
        ax = xs + sgn * L                                              # apex on the line at its outer end
        sh.append(("poly", [(ax, y), (ax - 0.5 * tw, y + th), (ax + 0.5 * tw, y + th)], None, col, lw))
        ty = y - 0.35 * size                                           # baseline: text centred on the line
        if last is not None and ty > last - (size + SF_LEVEL["clear"]):
            ty = last - (size + SF_LEVEL["clear"])
            moved += 1
            sh.append(("line", [(ax + sgn * 0.5 * tw, y), (xt - sgn * 0.2, ty + 0.35 * size)], col, 0.08))
        nm = SF_LEVEL_NAMES.get(key, u"%s" % key)
        sh.append(("text", u"%+.2f %s" % (val, nm), xt, ty, size, col, False, "L" if side == "R" else "R"))
        last = ty
    SF_LOG.append(u"levels %s gap ok: %d markers %.1f mm off the drawing (%s), %d labels spread" % (
        page or u"", len(rows), SF_LEVEL["gap"], side, moved))
    return sh


def sf_level_items(ix, page, drawing, levels, side="R"):
    """round 5 (G-R5-12): the level markers as an export item: ix.levels(page, drawing id, [(name, z m)], side); the
    booklet draws them (pl_levels, same U04 marker). levels as for sf_level_marks (keys named by SF_LEVEL_NAMES).
    Logs "levels <page> gap ok (exported n)". Returns the item id."""
    rows = []
    for lv in levels or ():
        rows.append((SF_LEVEL_NAMES.get(lv[0], u"%s" % lv[0]), float(lv[1])))
    SF_LOG.append(u"levels %s gap ok: %d markers exported to the booklet" % (page or u"", len(rows)))
    did = drawing["id"] if isinstance(drawing, dict) else drawing
    return ix.levels(page, did, rows, side=side)


# ---- standard elements (true size; page mm, y up; side +1 = builds to the right of x) ------------------------------
SF_LANE = dict(bike="C4AE9E", walk=SCT["concrete"], road="9C9890", gravel=SCT["gravel"], timber=SCT["timber"])
# round 5 (S3, PLAN §3): walk / gravel / timber = the section kit's solid material colours (section_parts SCT)
SF_RAIL_H = 1.10        # m, the repo's railing height (figures.py railing rail_h)
SF_SEAT_H = 0.45        # m, the repo's seat height (figures.py sit_step seat_h)


def sf_lane(x, y, width_m, k, kind="walk", side=1, t_m=0.15, callouts=None, label=None):
    """a lane on the ground at (x, y): bike (with its centre and edge lines), walk (paving joints), road, gravel or
    timber; t_m = its build-up drawn under the surface (drawing rule). label + callouts: a numbered callout.
    Returns shapes (surface at y)."""
    w, t = width_m * k * side, t_m * k
    xa, xb = min(x, x + w), max(x, x + w)
    sh = [("poly", [(xa, y - t), (xb, y - t), (xb, y), (xa, y)], SF_LANE.get(kind, SCT["concrete"]), SCT["cut"], 0.2)]
    if kind == "walk" and k >= SCT_DETAIL_K:          # round 5 (S3, G-R5-4.1): joints only at inset detail scales
        j = max(0.6 * k, 1.0)
        xx = xa + j
        while xx < xb - 0.2:
            sh.append(("line", [(xx, y - t), (xx, y)], SCT["line"], 0.06))
            xx += j
    elif kind == "bike":
        sh.append(("line", [(xa + 0.1 * k, y + 0.02), (xb - 0.1 * k, y + 0.02)], "FFFFFF", 0.12, [0.8, 0.6]))
    elif kind == "gravel":
        sh = sct_hatch_fill([(xa, y - t), (xb, y - t), (xb, y), (xa, y)], "gravel", k, SCT["cut"], 0.2)
    elif kind == "timber" and k >= SCT_DETAIL_K:
        xx = xa + 0.14 * k
        while xx < xb - 0.05:
            sh.append(("line", [(xx, y - t), (xx, y)], SCT["line"], 0.05))
            xx += 0.14 * k
    if callouts is not None and label:
        callouts.add((xa + xb) / 2.0, y + 1.2, label)
    return sh


def sf_stairs(x, y, n, rise_m, tread_m, k, side=1, material="concrete", t_m=0.15, rail=False):
    """a flight of n steps (rise_m, tread_m each; give them from the design) climbing from (x, y) toward side.
    Returns (shapes, (x_end, y_end))."""
    sh, cx, cy = [], x, y
    for _i in range(n):
        x2, y2 = cx + side * tread_m * k, cy + rise_m * k
        ring = [(cx, cy - t_m * k), (cx, y2), (x2, y2), (x2, cy - t_m * k)]
        sh += sct_hatch_fill(ring, material, k, SCT["cut"], 0.2)
        cx, cy = x2, y2
    if rail:
        sh.append(("line", [(x, y + SF_RAIL_H * k), (cx, cy + SF_RAIL_H * k)], SCT["cut"], 0.2))
        for px, py in ((x, y), (cx, cy)):
            sh.append(("line", [(px, py), (px, py + SF_RAIL_H * k)], SCT["cut"], 0.2))
    return sh, (cx, cy)


def sf_ramp(x, y, run_m, rise_m, k, side=1, t_m=0.20, material="concrete", rail=True):
    """a ramp slab from (x, y) rising rise_m over run_m toward side (slope = the design's; t_m drawing rule).
    Returns (shapes, (x_end, y_end), slope %)."""
    x2, y2 = x + side * run_m * k, y + rise_m * k
    ring = [(x, y - t_m * k), (x, y), (x2, y2), (x2, y2 - t_m * k)]
    sh = sct_hatch_fill(ring, material, k, SCT["cut"], 0.2)
    if rail:
        sh.append(("line", [(x, y + SF_RAIL_H * k), (x2, y2 + SF_RAIL_H * k)], SCT["cut"], 0.15))
    return sh, (x2, y2), (100.0 * rise_m / run_m if run_m else 0.0)


def sf_terrace(x, y, width_m, k, side=1, t_m=0.25, material="timber", rail=True):
    """a level viewing terrace / deck at (x, y) width_m wide toward side, slab t_m (drawing rule), railing SF_RAIL_H
    at its outer edge. Returns shapes."""
    x2 = x + side * width_m * k
    xa, xb = min(x, x2), max(x, x2)
    ring = [(xa, y - t_m * k), (xb, y - t_m * k), (xb, y), (xa, y)]
    sh = (sct_hatch_fill(ring, "concrete", k, SCT["cut"], 0.2) if material == "concrete" else
          [("poly", ring, SF_LANE["timber"], SCT["cut"], 0.2)])
    if rail:
        sh += sct_bank("railing", x2, y, y, side, k, h_m=SF_RAIL_H)[0]
    return sh


def sf_bridge(x0, x1, deck_y, k, deck_t_m=0.50, rail=True, material="concrete"):
    """a bridge deck over the stream from x0 to x1 (top at deck_y), deck_t_m thick (drawing rule unless the design
    gives one), railings at both edges; draw it in the "structures" layer (over the water). Returns shapes."""
    xa, xb = min(x0, x1), max(x0, x1)
    ring = [(xa, deck_y - deck_t_m * k), (xb, deck_y - deck_t_m * k), (xb, deck_y), (xa, deck_y)]
    sh = sct_hatch_fill(ring, material, k, SCT["cut"], 0.3)
    if rail:
        for xr in (xa + 0.1 * k, xb - 0.1 * k):
            sh.append(("line", [(xr, deck_y), (xr, deck_y + SF_RAIL_H * k)], SCT["cut"], 0.2))
        sh.append(("line", [(xa + 0.1 * k, deck_y + SF_RAIL_H * k), (xb - 0.1 * k, deck_y + SF_RAIL_H * k)], SCT["cut"],
                   0.2))
    return sh


def sf_stepping_stones(x0, x1, bed_y, wl_y, k, stone_w_m=0.60, gap_m=0.40, above_m=0.15, seed=0):
    """stepping stones across the water from x0 to x1, standing on the bed and above_m above the average-flow water
    wl_y; widths and gaps vary (no even rhythm). Sizes are drawing rules (a typical stride), not data. Returns
    shapes ("structures": over the water)."""
    rnd = _wat_rng(seed + 9)
    sh, x = [], x0 + 0.5 * gap_m * k
    top = wl_y + above_m * k
    while x + stone_w_m * 0.85 * k <= x1:
        w = stone_w_m * (0.85 + 0.3 * rnd()) * k
        r = 0.12 * w
        ring = [(x, bed_y), (x + w, bed_y), (x + w, top - r), (x + w - r, top), (x + r, top), (x, top - r)]
        sh += sct_hatch_fill(ring, "stone", k, SCT["cut"], 0.25)
        x += w + gap_m * (0.75 + 0.5 * rnd()) * k
    return sh


def sf_bench(x, y, k, side=1, seat_h=SF_SEAT_H, depth_m=0.45, t_m=0.08, back=False):
    """a bench in section at (x, y): seat seat_h (repo 0.45 m) high, depth_m deep (drawing rule), a leg, optional
    back. Returns shapes."""
    x2 = x + side * depth_m * k
    xa, xb = min(x, x2), max(x, x2)
    sy = y + seat_h * k
    sh = [("poly", [(xa, sy - t_m * k), (xb, sy - t_m * k), (xb, sy), (xa, sy)], SF_LANE["timber"], SCT["cut"], 0.2),
          ("line", [((xa + xb) / 2.0, y), ((xa + xb) / 2.0, sy - t_m * k)], SCT["cut"], 0.25)]
    if back:
        bx = xa if side > 0 else xb
        sh.append(("line", [(bx, sy), (bx - side * 0.05 * k, sy + 0.40 * k)], SCT["cut"], 0.25))
    return sh


# ---- street elements (round 3 G15; beside sf_bench). Sizes are DRAWING RULES for a typical element of its kind,
# not project data: never print them as measured. ----------------------------------------------------------------
SF_STREET = dict(lamp_h=4.00, lamp_arm=0.45, bollard_h=0.90, bollard_w=0.15, rack_h=0.75, rack_l=0.70)


def sf_lamp(x, y, k, side=1, h_m=None, layer=0, ink=None):
    """a pedestrian street lamp in section at (x, y): a slim mast h_m high (SF_STREET lamp_h 4.00 m, drawing rule),
    a short arm toward side and a lantern head; ink faded for depth layer (fig_fade). Returns shapes."""
    sc = fig_depth(layer)[0] if layer else 1.0
    K = k * sc
    ink = fig_fade(ink or SEC["ink"], layer) if layer else (ink or SEC["ink"])
    H, a = (h_m or SF_STREET["lamp_h"]) * K, SF_STREET["lamp_arm"] * K * side
    w = max(0.12, 0.06 * K)
    hx, hy = x + a, y + H - 0.05 * K
    return [("poly", [(x - w, y), (x + w, y), (x + 0.6 * w, y + H), (x - 0.6 * w, y + H)], ink, None, 0.0),
            ("line", [(x, y + H), (x + 0.6 * a, y + H + 0.06 * K), (hx, hy)], ink, max(0.1, 0.03 * K)),
            ("poly", [(hx - 0.14 * K, hy), (hx + 0.14 * K, hy), (hx + 0.07 * K, hy - 0.22 * K),
                      (hx - 0.07 * K, hy - 0.22 * K)], ink, None, 0.0)]


def sf_bollard(x, y, k, h_m=None, layer=0, ink=None):
    """a bollard in section at (x, y): SF_STREET bollard_h 0.90 m x bollard_w 0.15 m (drawing rule), rounded top,
    one light band. Returns shapes."""
    sc = fig_depth(layer)[0] if layer else 1.0
    K = k * sc
    ink = fig_fade(ink or SEC["ink"], layer) if layer else (ink or SEC["ink"])
    H, r = (h_m or SF_STREET["bollard_h"]) * K, 0.5 * SF_STREET["bollard_w"] * K
    ring = [(x - r, y), (x + r, y), (x + r, y + H - r)] + \
        [(x + r * __import__("math").cos(t), y + H - r + r * __import__("math").sin(t)) for t in
         [i * 3.14159265 / 8.0 for i in range(1, 8)]] + [(x - r, y + H - r)]
    return [("poly", ring, ink, None, 0.0),
            ("poly", [(x - r, y + 0.70 * H), (x + r, y + 0.70 * H), (x + r, y + 0.78 * H), (x - r, y + 0.78 * H)],
             "FFFFFF", None, 0.0)]


def sf_bike_rack(x, y, k, side=1, layer=0, ink=None):
    """a bike rack (an inverted-U stand) in section at (x, y), seen along its length: SF_STREET rack_l 0.70 m long,
    rack_h 0.75 m high (drawing rule), running toward side. Returns shapes."""
    import math as _m
    sc = fig_depth(layer)[0] if layer else 1.0
    K = k * sc
    ink = fig_fade(ink or SEC["ink"], layer) if layer else (ink or SEC["ink"])
    L, H = SF_STREET["rack_l"] * K * side, SF_STREET["rack_h"] * K
    r = 0.5 * abs(L)
    cx = x + 0.5 * L
    pts = [(x, y), (x, y + H - r)] + [(cx - r * _m.cos(t), y + H - r + r * _m.sin(t)) for t in
                                       [i * _m.pi / 10.0 for i in range(11)]] + [(x + L, y)]
    if side < 0:
        pts = [(x, y), (x, y + H - r)] + [(cx + r * _m.cos(t), y + H - r + r * _m.sin(t)) for t in
                                           [i * _m.pi / 10.0 for i in range(11)]] + [(x + L, y)]
    return [("line", pts, ink, max(0.12, 0.05 * K))]


# ---- zoom-in inset (round 3 G15, Aras's U29 sketch) --------------------------------------------------------------
# A use zone narrower than ~15 mm on the page gets an enlarged copy beside the section: a thin rectangle on the
# spot, the same drawing at the bigger scale in a box (white ground, 0.25 pt neatline like a map: the one frame
# G17 keeps), the label "ZOOMED IN · <what>" over it and ONE short connector from the spot's corner to the box's
# nearest corner (a frame link, not a label leader).
SF_ZOOM = dict(lw_spot=0.064, lw_box=0.088, label_mm=2.47, gap=1.0, bar_h=0.8, bar_lw=0.1)   # round 4: label 7 pt


def sf_scale_bar(x, y, k, den=None, max_mm=30.0, size=2.12, ink=None, segs=4):
    """round 4 (S2, G-R4-5.6): a small scale bar for an inset or section: segs alternating ink / white cells along a
    round length in m (1, 2, 5, 10, 20, 50, 100 ... the longest that fits max_mm at k page mm per m), left end at
    (x, y) (page mm, y up: the bar's top edge), "0" and "<L> m" under its ends and "1:<den>" after it when den is
    given; text 6 pt (minimum). Returns shapes."""
    ink = ink or SEC["ink"]
    Lm = 1.0
    for c in (1, 2, 5, 10, 20, 50, 100, 200, 500, 1000):
        if c * k <= max_mm:
            Lm = float(c)
    L = Lm * k
    h = SF_ZOOM["bar_h"]
    sh = []
    for i in range(segs):
        a, b = x + L * i / segs, x + L * (i + 1) / segs
        sh.append(("poly", [(a, y - h), (b, y - h), (b, y), (a, y)], ink if i % 2 == 0 else "FFFFFF", ink,
                   SF_ZOOM["bar_lw"]))
    ty = y - h - 0.9 * size
    sh.append(("text", u"0", x, ty, size, ink, False, "C"))
    sh.append(("text", u"%g m" % Lm, x + L, ty, size, ink, False, "C"))
    if den:
        sh.append(("text", u"1:{:,}".format(int(den)), x + L + 1.2 * size, y - h, size, ink, False, "L"))
    return sh


def _sf_clip_poly(ring, x0, y0, x1, y1):
    """Sutherland-Hodgman: ring clipped to the rectangle"""
    def cut(P, inside, inter):
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            if inside(b):
                if not inside(a):
                    out.append(inter(a, b))
                out.append(b)
            elif inside(a):
                out.append(inter(a, b))
        return out

    def ix(xv):
        return lambda a, b: (xv, a[1] + (b[1] - a[1]) * (xv - a[0]) / ((b[0] - a[0]) or 1e-12))

    def iy(yv):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (yv - a[1]) / ((b[1] - a[1]) or 1e-12), yv)
    P = list(ring)
    for inside, inter in ((lambda p: p[0] >= x0, ix(x0)), (lambda p: p[0] <= x1, ix(x1)),
                          (lambda p: p[1] >= y0, iy(y0)), (lambda p: p[1] <= y1, iy(y1))):
        if not P:
            break
        P = cut(P, inside, inter)
    return P


def _sf_clip_line(pts, x0, y0, x1, y1):
    """the pieces of a polyline inside the rectangle (Liang-Barsky per segment, joined where they touch)"""
    out, cur = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t0, t1, ok = 0.0, 1.0, True
        for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if abs(p) < 1e-12:
                if q < 0:
                    ok = False
                    break
                continue
            r = q / p
            if p < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if len(cur) >= 2:
                out.append(cur)
            cur = []
            continue
        pa = (a[0] + t0 * dx, a[1] + t0 * dy)
        pb = (a[0] + t1 * dx, a[1] + t1 * dy)
        if cur and abs(cur[-1][0] - pa[0]) < 1e-9 and abs(cur[-1][1] - pa[1]) < 1e-9:
            cur.append(pb)
        else:
            if len(cur) >= 2:
                out.append(cur)
            cur = [pa, pb]
        if t1 < 1.0:
            out.append(cur)
            cur = []
    if len(cur) >= 2:
        out.append(cur)
    return out


def sf_zoom_inset(src_box, dst_box, k_src, k_dst, draw_fn, label, size=None, ink=None, connector=True,
                  scale_den=None, parent_den=None, page=None):
    """G15 zoom-in inset. src_box = (x0, y0, x1, y1) page mm of the spot on the section; dst_box = the inset's box
    beside the section; k_src, k_dst = page mm per m of the section and of the inset (k_dst > k_src). draw_fn: the
    shapes of the section (a list, or a WaterLayers, or a callable returning one): every shape is re-drawn at the
    bigger scale (geometry x k_dst / k_src about the spot's centre -> the box's centre; pen widths and text sizes
    kept) and clipped to the box; images keep their pixels and get the box as clip. label: what is shown ("ZOOMED
    IN · <label>" over the box, left aligned). Returns shapes: the spot rectangle, the connector, the box ground,
    the enlarged copy, the neatline and the label. Size the box so the spot fits: (x1 - x0) x k_dst / k_src.
    Round 4 (S2, G-R4-5.6, D11): RAISES when the inset is less than SF_INSET_MIN_ZOOM (2) x its parent (k_dst / k_src,
    and parent_den / scale_den when both are given); scale_den = the inset's scale (checked against SF_INSET_SCALES:
    1:100 allowed for insets only) -> its own scale bar under the box and "1:<den>" in the caption; without it a
    FLAG line (no bar). page: the booklet page id for the log line "inset <page> parent 1:<a> inset 1:<b>". The
    caption sits above the box, outside the detail; the bar below it."""
    f_chk = float(k_dst) / float(k_src)
    if f_chk < SF_INSET_MIN_ZOOM - 1e-6:                   # round 5 (S3): a WARNING, never a stop
        _sf_warn(page, "inset", u"(%s): zoom %.2f x its parent; G-R4-5.6 needs >= %.0f x (D11: a 1:250 parent takes a "
                                u"1:100 inset)" % (label, f_chk, SF_INSET_MIN_ZOOM))
    if scale_den is not None:
        scale_den = sf_scale_ok(scale_den, inset=True)
        if parent_den is not None and float(parent_den) / float(scale_den) < SF_INSET_MIN_ZOOM - 1e-6:
            _sf_warn(page, "inset", u"(%s): 1:%s is less than 2 x its parent 1:%s (G-R4-5.6)"
                     % (label, scale_den, parent_den))
        SF_LOG.append(u"inset %s parent 1:%s inset 1:%s" % (page or u"", parent_den if parent_den else u"?",
                                                            int(scale_den)))
    else:
        SF_LOG.append(u"FLAG inset %s (%s): no scale_den passed: no scale bar (G-R4-5.6)" % (page or u"", label))
    sh_in = draw_fn() if callable(draw_fn) else draw_fn
    if hasattr(sh_in, "shapes"):
        sh_in = sh_in.shapes()
    ink = ink or SEC["ink"]
    size = size or SF_ZOOM["label_mm"]
    sx0, sy0, sx1, sy1 = src_box
    dx0, dy0, dx1, dy1 = dst_box
    f = float(k_dst) / float(k_src)
    scx, scy = 0.5 * (sx0 + sx1), 0.5 * (sy0 + sy1)
    dcx, dcy = 0.5 * (dx0 + dx1), 0.5 * (dy0 + dy1)

    def T(p):
        return (dcx + (p[0] - scx) * f, dcy + (p[1] - scy) * f)
    out = []
    for s_ in sh_in or ():
        t = s_[0]
        if t == "poly":
            r = _sf_clip_poly([T(p) for p in s_[1]], dx0, dy0, dx1, dy1)
            if len(r) >= 3:
                out.append(("poly", r) + tuple(s_[2:]))
        elif t == "line":
            for piece in _sf_clip_line([T(p) for p in s_[1]], dx0, dy0, dx1, dy1):
                out.append(("line", piece) + tuple(s_[2:]))
        elif t == "text":
            x, y = T((s_[2], s_[3]))
            if dx0 <= x <= dx1 and dy0 <= y <= dy1:
                out.append(("text", s_[1], x, y) + tuple(s_[4:]))
        elif t == "image":
            ax, ay = T((s_[1], s_[2]))
            w, h = s_[3] * f, s_[4] * f
            if ax < dx1 and ax + w > dx0 and ay < dy1 and ay + h > dy0:
                rest = tuple(s_[5:8]) + (None,) * (3 - len(s_[5:8]))
                out.append(("image", ax, ay, w, h) + rest[:3] + ((dx0, dy0, dx1, dy1),))
    box = [(dx0, dy0), (dx1, dy0), (dx1, dy1), (dx0, dy1)]
    sh = [("poly", [(sx0, sy0), (sx1, sy0), (sx1, sy1), (sx0, sy1)], None, ink, SF_ZOOM["lw_spot"])]
    if connector:                                    # spot corner -> the box's nearest corner
        cs = [(sx0, sy0), (sx1, sy0), (sx1, sy1), (sx0, sy1)]
        best = min(((a, b) for a in cs for b in box), key=lambda ab: (ab[0][0] - ab[1][0]) ** 2 + (ab[0][1] - ab[1][1]) ** 2)
        sh.append(("line", [best[0], best[1]], ink, SF_ZOOM["lw_spot"]))
    sh.append(("poly", box, "FFFFFF", None, 0.0))
    sh += out
    sh.append(("poly", box, None, ink, SF_ZOOM["lw_box"]))
    cap = u"ZOOMED IN · %s" % label + (u" · 1:{:,}".format(int(scale_den)) if scale_den else u"")
    sh.append(("text", cap, dx0, dy1 + 0.6 * size, size, ink, True, "L"))
    if scale_den:
        sh += sf_scale_bar(dx0, dy0 - SF_ZOOM["gap"], k_dst, None, max_mm=min(30.0, 0.45 * (dx1 - dx0)),
                           ink=ink)
    return sh


# ---- inset frame v2 (round 5, S3, G-R5-5: U12, U13, U14, U16; keep K2) --------------------------------------------
# Change of approach (round 4's insets were the parent's shapes scaled up: "page 14 zoom ins looks awful"): an inset
# is its OWN drawing, drawn again at its own scale k = sf_inset_k(den) so the kit's detail switches on (k >= 4, 1:250
# and larger: stone courses and deck boards at real size, section_parts SCT_DETAIL_K; treads and risers are drawn at
# true size anyway), and it is FRAMED ON THE ACTION: the window is computed from what the inset is about (the person,
# rod and line end, the water it shows, the seat or tread), never typed. Export: D_child = ix.drawing(...,
# scale_pref=[den]); ix.inset(page, parent id, window, child id, factor) (S1 schema); the booklet draws the frame, the
# link and the scale bar. sf_zoom_inset (scaled copy) stays only for pages not yet moved.
SF_INSET = dict(margin_m=0.6, min_w_m=3.0)          # clear margin round the action; smallest window (drawing rules)


def sf_inset_k(den):
    """page mm per m of an inset at 1:den (1:100 allowed, D11)"""
    return 1000.0 / sf_scale_ok(den, inset=True)


def sf_inset_frame(focus, parent_den, box_mm=None, margin_m=None, page=None, label=u""):
    """G-R5-5 framing: focus = the boxes (x0, y0, x1, y1, drawing m: chainage x, level y) of everything the inset is
    about (person, rod + line end, the water surface it shows, the seat); returns dict(window (m), den, factor, k)
    or None: the window = their union + margin_m on every side (centred on the action, so nothing it is about is
    cut), widened to box_mm's aspect (w, h mm) when given; den = the LARGEST scale on SF_INSET_SCALES that is >= 2 x
    the parent (den <= parent_den / 2) and fits box_mm (when given). WARNING when no listed scale fits."""
    m = SF_INSET["margin_m"] if margin_m is None else margin_m
    bx = [b for b in focus or () if b]
    if not bx:
        _sf_warn(page, "inset", u"(%s): nothing to frame (no focus boxes)" % label)
        return None
    x0 = min(b[0] for b in bx) - m
    y0 = min(b[1] for b in bx) - m
    x1 = max(b[2] for b in bx) + m
    y1 = max(b[3] for b in bx) + m
    if x1 - x0 < SF_INSET["min_w_m"]:
        c = 0.5 * (x0 + x1)
        x0, x1 = c - 0.5 * SF_INSET["min_w_m"], c + 0.5 * SF_INSET["min_w_m"]
    if box_mm:
        bw, bh = float(box_mm[0]), float(box_mm[1])
        w, h = x1 - x0, y1 - y0
        if w / h < bw / bh:                       # widen to the box's aspect, centred (the action stays centred)
            d = 0.5 * (h * bw / bh - w)
            x0, x1 = x0 - d, x1 + d
        else:
            d = 0.5 * (w * bh / bw - h)
            y0, y1 = y0 - d, y1 + d
    ok = [d_ for d_ in SF_INSET_SCALES if d_ <= float(parent_den) / SF_INSET_MIN_ZOOM + 1e-6]
    den = None
    for d_ in ok:                                 # largest scale first (smallest denominator)
        if not box_mm or ((x1 - x0) * 1000.0 / d_ <= box_mm[0] + 1e-6 and (y1 - y0) * 1000.0 / d_ <= box_mm[1] + 1e-6):
            den = d_
            break
    if den is None:
        den = ok[-1] if ok else SF_INSET_SCALES[0]
        _sf_warn(page, "inset", u"(%s): the action (%.1f x %.1f m) does not fit %s mm at any listed inset scale >= 2 x "
                                u"1:%s; 1:%d used" % (label, x1 - x0, y1 - y0, box_mm, parent_den, den))
    SF_LOG.append(u"inset %s %s: parent 1:%s inset 1:%d, window %.1f x %.1f m" % (
        page or u"", label, parent_den, den, x1 - x0, y1 - y0))
    return dict(window=(x0, y0, x1, y1), den=den, factor=float(parent_den) / den, k=1000.0 / den)


def sf_inset_cut_check(window, items, page=None, label=u""):
    """U16 "nothing cut by the inset frame": items = [(name, (x0, y0, x1, y1) m)] of the people, objects and plants
    drawn in the inset; one that the window's edge cuts (partly inside) is a WARNING. Returns the names cut."""
    wx0, wy0, wx1, wy1 = window
    cut = []
    for nm, b in items or ():
        inside = b[0] >= wx0 and b[2] <= wx1 and b[1] >= wy0 and b[3] <= wy1
        out = b[2] <= wx0 or b[0] >= wx1 or b[3] <= wy0 or b[1] >= wy1
        if not inside and not out:
            cut.append(nm)
    if cut:
        _sf_warn(page, "inset", u"(%s): cut by the frame: %s" % (label, u", ".join(u"%s" % c for c in cut)))
    return cut


# ---- G6: people 1.75 m vs tree heights vs buildings, at depth layer 0 ----------------------------------------------
def sf_assert_g6(k, trees=(), buildings=(), strict=False, layer=0, page=None):
    """the G6 scale check of one drawing at depth layer 0: figures print at their true height for k (figures.py
    fig_check_scale), every tree drawn (key, h_m) or placed (key, x, h_m, crown_m) inside its sourced height range
    (so the tree / person ratio is the real one), every building (name, drawn_h_m, data_h_m) at its data height
    (+-0.05 m). Round 5 (S3, A13): a true-scale miss is a WARNING line (never a stop); strict=True still raises for
    an old caller that asks. Returns the messages ([] when all is right)."""
    bad = []
    try:
        fig_check_scale(k, layer=layer)
    except AssertionError as ex:
        bad.append(u"%s" % ex)
    for t in trees or ():
        key, h = t[0], (t[1] if len(t) == 2 else t[2])
        sp = PLA_SPECIES.get(key)
        if sp is None:
            bad.append(u"G6: unknown species %r" % (key,))
            continue
        lo, hi = sp["h_range"]
        if (lo is not None and h < lo - 1e-6) or (hi is not None and h > hi + 1e-6):
            bad.append(u"G6: %s drawn %.2f m, sourced %s-%s m (tree / person %.1f)" % (key, h, lo or "", hi or "",
                                                                                    h / FIG_ADULT_H))
    for name, drawn, data in buildings or ():
        if data is not None and abs(float(drawn) - float(data)) > 0.05:
            bad.append(u"G6: building %s drawn %.2f m, data %.2f m" % (name, drawn, data))
    if bad and strict:
        raise AssertionError(u"; ".join(bad))
    for m_ in bad:
        _sf_warn(page, "scale", m_)
    return bad
bergama_data("BRIDGES")
# ---- bridges.py (round 5, S3, 1 Nov 2026; D8 "bridges in every section possible", G-R5-4.7, N4 a, A15) -------------
# ONE module puts the Selinos bridges into any section: which bridge a cut passes, where it stands along the cut, and
# its shapes, drawn only as far as the sources go. Data: data/BRIDGES.py (positions = the bridge-list points, N4 a;
# facts with their sources). Include after levels.py (+ data/LEVELS.py), section_parts.py and, when present,
# basemap.py (deck outlines) and names.py (printed names):
#   #@include ../common/data/BRIDGES.py
#   #@include ../common/bridges.py
#
#   br_near(cid, look=1, max_m=None, t0=None, t1=None) -> [dict(key, name, t, d, rel, seg_m)]
#         every bridge the cut cid passes: rel "cut" (the cut line runs through it: S6), "beyond" (in view, d m
#         beyond the cut plane, within the drawn span t0..t1), "behind" (behind the viewer: NOT drawn, logged).
#         t = m along the cut from its first end (level_ends), d = m beyond the plane (look: +1 as the site board S
#         cuts / p18-20 / p24 / p12, -1 as the W cuts on p13-14, sf_back_buildings' rule).
#   br_section(cid, X=None, Y=None, look=1, t0=None, t1=None, ground=None, top=None, max_m=None, page=None,
#              into=None) -> {"background": shapes, "structures": shapes, "found": [...]}
#         X(t m) -> drawing x, Y(z m a.s.l.) -> drawing y (default identity = the item-export section convention:
#         x = chainage m, y = elevation m, S1 item_export); ground(t) -> the cut's ground z at t (the bed under a
#         bridge; default the cut's LEVELS bed); top = the road / bank-top level z for bridges with no height source
#         (default the cut's higher LEVELS bank top). A bridge beyond the plane is drawn in elevation in "background"
#         (true size, paler with distance; the cut ground in front hides what lies below the banks); a bridge the
#         cut runs through is drawn cut in "structures" (over the water). into = a WaterLayers: the shapes are added.
#         Logs one `bridge <cid> <name|none>` line per call (br_log_lines).
#   br_log_lines() -> the bridge lines and FLAG lines of this run (sec_look_lines prints them)
#
# Sourced vs drawing rules (A15): the FLAG lines name every part drawn by a rule. Üç Kemer: middle arch span 9.60 m
# and bed-to-keystone 10 m, deck 4.50 x 56.40 m, three round arches on two piers (Visit İzmir) are data; side arch
# size, pier width and masonry over the keystone are the round 4 p12 drawing rules (P12_K5_*, same values). Ulucami
# Önü: two eyes (one round, one smaller pointed; Visit İzmir) and the parapet 7.4-8.6 m over the bed (photo-scaled,
# IMG_5814) are data; the eye sizes are drawing rules. Tabak: two openings (data), no height: the deck at the bank
# top, openings not drawn. K1, K2, K6: no data: the deck at the cut's bank top (the road level), BR_RULE deck_t_m.
# Bridge bed level: not surveyed at any bridge -> the cut's own bed (or ground(t)), FLAG.

BR_NEAR_M = 250.0          # in-code rule already used for "the nearest bridge" (selinus_board 15l_r28_site.py:317)
BR_CUT_M = 6.0             # a cut line passing within this of the bridge point runs THROUGH it (cut ends +-3 m, CHK-8)
BR_DECK_MATCH_M = 40.0     # a survey deck ring (basemap "decks") belongs to a bridge whose point lies this close
BR_RULE = dict(deck_t_m=0.50,      # deck slab thickness: section_frame sf_bridge drawing rule (not sourced)
               crown_m=1.0,        # masonry over the keystone to the deck top: p12 P12_K5_CROWN_M (not sourced)
               pier_m=2.0,         # pier width between two arches: p12 P12_K5_PIER_M (not sourced)
               side_frac=0.6,      # side arch = this x the middle arch's span and height: p12 P12_K5_SIDE (not sourced)
               k4_big_frac=0.55,   # Ulucami Önü: the big eye's share of the clear width between its ends (not sourced)
               k4_small_rise=1.25, # the smaller pointed eye: rise / half span (not sourced)
               fade_far=0.70)      # tone toward the paper at BR_NEAR_M beyond the plane (drawing rule, as sf_topo_back)
BR_COL = dict(stone="A4A1A3", deck="D5D3CE", line="7A6E60", paper="FFFFFF")
BR_LOG = []
BR_FLAGS = []


def _br_flag(msg):
    if msg not in BR_FLAGS:
        BR_FLAGS.append(msg)


def br_name(key):
    """the printed name (names.py bridge_name, G16); the key only when names.py is not included"""
    f = globals().get("bridge_name")
    return f(key) if f else key


def br_fact(key, name):
    """a sourced value of a bridge (data/BRIDGES.py), None when there is none"""
    v = BRIDGES[key].get("facts", {}).get(name)
    return None if v is None else v["value"]


def _br_axis(cid, look, ends=None):
    import math as _m
    a, b = ends if ends else level_ends(cid)
    L = _m.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
    f = (-u[1] * look, u[0] * look)                       # beyond the plane = in view (sf_back_buildings rule)
    return a, u, f, L


def br_near(cid, look=1, max_m=None, t0=None, t1=None, ends=None):
    """the bridges cut cid passes (see the module notes), nearest first; ends = ((x1, y1), (x2, y2)) survey m for a
    cut that is not a LEVELS row (p09 street cuts, p24 D1 / D2 spans, A-A')"""
    import math as _m
    a, u, f, L = _br_axis(cid, look, ends)
    mx = BR_NEAR_M if max_m is None else max_m
    t0 = 0.0 if t0 is None else t0
    t1 = L if t1 is None else t1
    out = []
    for key in sorted(BRIDGES):
        x, y = BRIDGES[key]["xy"]
        dx, dy = x - a[0], y - a[1]
        t = dx * u[0] + dy * u[1]
        d = dx * f[0] + dy * f[1]
        tc = min(max(t, 0.0), L)
        seg = _m.hypot(x - (a[0] + u[0] * tc), y - (a[1] + u[1] * tc))
        if seg <= BR_CUT_M:
            rel = "cut"
        elif abs(d) > mx or t < t0 or t > t1:
            continue
        else:
            rel = "beyond" if d > 0 else "behind"
        out.append(dict(key=key, name=br_name(key), t=t, d=d, rel=rel, seg_m=seg))
    out.sort(key=lambda r: abs(r["d"]))
    return out


def _br_deck_span(key, a, u):
    """(ta, tb) m along the cut covered by the bridge's survey deck ring (basemap decks), or None"""
    import math as _m
    if not globals().get("basemap_load"):
        return None
    try:
        D = basemap_load()
    except Exception:
        return None
    x, y = BRIDGES[key]["xy"]
    best = None
    for R in ((D or {}).get("layers") or {}).get("decks", []) or []:
        if len(R) < 3:
            continue
        cx = sum(p[0] for p in R) / float(len(R))
        cy = sum(p[1] for p in R) / float(len(R))
        dd = _m.hypot(cx - x, cy - y)
        if dd <= BR_DECK_MATCH_M and (best is None or dd < best[0]):
            best = (dd, R)
    if best is None:
        return None
    ts = [(p[0] - a[0]) * u[0] + (p[1] - a[1]) * u[1] for p in best[1]]
    return min(ts), max(ts)


def _br_cut_levels(cid):
    """(bed, higher bank top) of the cut from LEVELS; a cut with several crossings (S5, S6) takes the lowest bed and
    the highest top of its rows"""
    rows = [cid]
    try:
        level_cut(cid)
    except KeyError:
        rows = [r["id"] for r in _lv_cut_rows(cid)]
    if not rows:
        return None, None
    beds = [level(r, "bed") for r in rows]
    tops = [level(r, "top", s) for r in rows for s in ("NE", "SW")]
    beds = [v for v in beds if v is not None]
    tops = [v for v in tops if v is not None]
    return (min(beds) if beds else None), (max(tops) if tops else None)


def _br_arch(tc, half, key_z, bed_z, n=16, half_v=None):
    """an opening: a round arch of half span `half` (m along the cut) with its keystone at key_z, open down to the
    bed: [(t, z)] (springing = key_z - half_v; half_v = the true half span when the face is seen at an angle and its
    spans look shorter along the cut)"""
    import math as _m
    hv = half if half_v is None else half_v
    sp = key_z - hv
    pts = [(tc - half, bed_z), (tc - half, sp)]
    pts += [(tc - half * _m.cos(_m.pi * i / n), sp + hv * _m.sin(_m.pi * i / n)) for i in range(1, n)]
    pts += [(tc + half, sp), (tc + half, bed_z)]
    return pts


def _br_pointed(tc, half, rise, bed_z, sp_z, n=10):
    """a pointed (two-centred) eye: half span `half`, crown `rise` over the springing sp_z"""
    import math as _m
    pts = [(tc - half, bed_z), (tc - half, sp_z)]
    for i in range(1, n):                                  # a simple ogival curve: sine-eased to the crown
        s = i / float(n)
        pts.append((tc - half + half * s, sp_z + rise * _m.sin(0.5 * _m.pi * s) ** 0.8))
    pts.append((tc, sp_z + rise))
    for i in range(n - 1, 0, -1):
        s = i / float(n)
        pts.append((tc + half - half * s, sp_z + rise * _m.sin(0.5 * _m.pi * s) ** 0.8))
    pts += [(tc + half, sp_z), (tc + half, bed_z)]
    return pts


def _br_mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


def br_section(cid, X=None, Y=None, look=1, t0=None, t1=None, ground=None, top=None, max_m=None, page=None,
               into=None, ends=None, bed=None):
    """the bridges of a section (see the module notes); ends as br_near (a cut that is not a LEVELS row then needs
    ground= or bed= and top=)"""
    X = X or (lambda t: t)
    Y = Y or (lambda z: z)
    a, u, f, L = _br_axis(cid, look, ends)
    try:
        bed0, top0 = _br_cut_levels(cid)
    except KeyError:
        bed0, top0 = None, None
    if bed is not None:
        bed0 = bed
    out = {"background": [], "structures": [], "found": []}
    seen = []
    for r in br_near(cid, look, max_m, t0, t1, ends):
        key, nm = r["key"], r["name"]
        if r["rel"] == "behind":
            seen.append(u"%s behind the viewer %.0f m (not seen)" % (nm, -r["d"]))
            continue
        bed = ground(r["t"]) if ground else bed0             # (the `bed` argument was taken into bed0 above)
        if bed is None:
            seen.append(u"%s not drawn: no bed level" % nm)
            continue
        if not ground:
            _br_flag(u"FLAG bridge bed: not surveyed at the bridges; the cut's own bed is used (%s)" % cid)
        B = BRIDGES[key]
        span = _br_deck_span(key, a, u)
        dl = br_fact(key, "deck_l_m")
        dw = br_fact(key, "deck_w_m")
        tc = 0.5 * (span[0] + span[1]) if span else r["t"]     # the survey deck's middle (over the water), else the point
        if r["rel"] == "cut":
            ext = span or ((tc - 0.5 * dw, tc + 0.5 * dw) if dw else None)
        else:                                             # a sourced length wins over the deck ring (which may be only
            ext = (tc - 0.5 * dl, tc + 0.5 * dl) if dl else span    # the part over the water)
        if ext is None:
            seen.append(u"%s not drawn: no deck outline in the survey layers and no sourced length" % nm)
            continue
        ta, tb = ext
        if t0 is not None:
            ta = max(ta, t0)
        if t1 is not None:
            tb = min(tb, t1)
        if tb - ta < 0.5:
            seen.append(u"%s outside the drawn span" % nm)
            continue
        if span is None:
            _br_flag(u"FLAG bridge %s: no survey deck ring found within %.0f m; its sourced length is centred on the "
                     u"bridge-list point" % (nm, BR_DECK_MATCH_M))
        # heights: sourced first, else the drawing rules (FLAG)
        kz = br_fact(key, "keystone_above_bed_m")
        pp = br_fact(key, "parapet_above_bed_m")
        if kz is not None:
            deck_z = bed + kz + BR_RULE["crown_m"]
            _br_flag(u"FLAG %s: masonry over the keystone %.2f m, side arches %.1f x the middle one, piers %.2f m: "
                     u"drawing rules (not sourced, A15)" % (nm, BR_RULE["crown_m"], BR_RULE["side_frac"],
                                                            BR_RULE["pier_m"]))
        elif pp is not None:
            lo, hi = pp
            deck_z = bed + 0.5 * (lo + hi)
            _br_flag(u"FLAG %s: parapet top %.2f m over the bed = the middle of the photo-scaled %.1f-%.1f m (IMG_5814); "
                     u"eye sizes drawing rules (not sourced)" % (nm, 0.5 * (lo + hi), lo, hi))
        else:
            tz = top if top is not None else top0
            if tz is None:
                seen.append(u"%s not drawn: no height source and no bank top" % nm)
                continue
            deck_z = tz
            _br_flag(u"FLAG %s: no height source; deck top drawn at the cut's bank top %+.2f (the road level), slab "
                     u"%.2f m (drawing rule)%s" % (nm, tz, BR_RULE["deck_t_m"],
                                                    u"; its openings are not drawn (no sizes)" if B.get("openings")
                                                    else u""))
        if r["rel"] == "cut":
            sh = _br_cut_shapes(key, ta, tb, bed, deck_z, X, Y)
            out["structures"] += sh
            seen.append(u"%s cut through (%.0f-%.0f m along the cut)" % (nm, ta, tb))
        else:
            fade = BR_RULE["fade_far"] * min(1.0, max(0.0, r["d"] / float(max_m or BR_NEAR_M)))
            sh = _br_elev_shapes(key, ta, tb, tc, bed, deck_z, X, Y, fade, span, dl)
            out["background"] += sh
            seen.append(u"%s %.0f m beyond the cut" % (nm, r["d"]))
        out["found"].append(dict(r, ta=ta, tb=tb, deck_z=round(deck_z, 2), bed=round(bed, 2)))
    line = u"bridge %s %s" % (cid, u"; ".join(seen) if seen else u"none")
    if page:
        line += u" (%s)" % page
    BR_LOG.append(line)
    if into is not None:
        into.add("background", out["background"])
        into.add("structures", out["structures"])
    return out


def _br_cut_shapes(key, ta, tb, bed, deck_z, X, Y):
    """the bridge cut along its width (the cut line runs along the stream through it): solid masonry from the
    opening's crown up to the deck top for an arched bridge with a sourced keystone, else the deck slab"""
    kz = br_fact(key, "keystone_above_bed_m")
    if kz is not None:
        z0 = bed + kz                                     # the cut passes the middle arch: void up to the keystone
        col = BR_COL["stone"]
    else:
        z0 = deck_z - BR_RULE["deck_t_m"]
        col = BR_COL["stone"] if BRIDGES[key].get("form") == "arches" else BR_COL["deck"]
    ring = [(X(ta), Y(z0)), (X(tb), Y(z0)), (X(tb), Y(deck_z)), (X(ta), Y(deck_z))]
    return [("poly", ring, col, BR_COL["line"], 0.25)]


def _br_elev_shapes(key, ta, tb, tc, bed, deck_z, X, Y, fade, span, dl):
    """the bridge in elevation beyond the cut plane: its face from the bed to the deck top over ta..tb with the
    openings the sources name (sizes per the module notes), one flat stone tone faded with distance"""
    B = BRIDGES[key]
    fill = _br_mix(BR_COL["stone"] if B.get("form") == "arches" else BR_COL["deck"], BR_COL["paper"], fade)
    ink = _br_mix(BR_COL["line"], BR_COL["paper"], fade)
    holes = []
    c = 1.0                                               # the cuts that see a bridge in elevation run nearly parallel
    if key == "K5" or (B.get("eyes") and br_fact(key, "mid_span_m")):
        ms, kz = br_fact(key, "mid_span_m"), br_fact(key, "keystone_above_bed_m")
        sf, pm = BR_RULE["side_frac"], BR_RULE["pier_m"]
        half = 0.5 * ms
        off = half + pm + 0.5 * ms * sf
        for dt, hh, kk in ((-off, half * sf, kz * sf), (0.0, half, kz), (off, half * sf, kz * sf)):
            pts = _br_arch(tc + dt * c, hh * c, bed + kk, bed - 0.5, half_v=hh)
            if pts[0][0] > ta and pts[-1][0] < tb:
                holes.append([(X(t), Y(z)) for t, z in pts])
    elif key == "K4":
        w = tb - ta
        clear = w - 2.0 * BR_RULE["pier_m"]
        if clear > 4.0:
            hb = 0.5 * clear * BR_RULE["k4_big_frac"]
            hs = 0.5 * clear * (1.0 - BR_RULE["k4_big_frac"]) - 0.5 * BR_RULE["pier_m"]
            cb = ta + BR_RULE["pier_m"] + hb
            cs = tb - BR_RULE["pier_m"] - hs
            kb = min(deck_z - BR_RULE["crown_m"], bed + 2.0 * hb)
            holes.append([(X(t), Y(z)) for t, z in _br_arch(cb, hb, kb, bed - 0.5)])
            if hs > 0.8:
                sp = bed + max(0.0, kb - bed - hb)
                rise = min(hs * BR_RULE["k4_small_rise"], deck_z - BR_RULE["crown_m"] - sp)
                holes.append([(X(t), Y(z)) for t, z in _br_pointed(cs, hs, rise, bed - 0.5, sp)])
    body = [(X(ta), Y(bed - 0.5)), (X(tb), Y(bed - 0.5)), (X(tb), Y(deck_z)), (X(ta), Y(deck_z))]
    if not holes:                                         # no opening is sourced (K1-K3, K6): the deck slab only,
        body = [(X(ta), Y(deck_z - BR_RULE["deck_t_m"])), (X(tb), Y(deck_z - BR_RULE["deck_t_m"])),   # never a
                (X(tb), Y(deck_z)), (X(ta), Y(deck_z))]                                              # solid wall
        return [("poly", body, fill, ink, 0.12)]
    return [("poly", body, fill, ink, 0.12, None, holes)]


def br_log_lines():
    """the bridge lines (`bridge <cid> <name|none>`) and FLAG lines of this run, each once"""
    out = []
    for ln in BR_LOG + BR_FLAGS:
        if ln not in out:
            out.append(ln)
    return out

# ================================================================ v10 the four proposal sections, true to the cut
# v10 (revision 29 Oct, WO-T3b-3; package C "Page 13", brief 02 §3-§6): the sketches are gone. Each section is drawn
# at 1:500 on the booklet page from the level table (common/levels.py: bed, bed width, bank and wall tops, bank type
# and angle, terraces, Q100, Q500) with the shared section parts (DSİ walls, embankments, loose earth, railings,
# stone / concrete / earth / gravel hatches, steps seated into the bank) and the plants module (every species at its
# true size and form; D6: no fig, citrus, iris, oleander, white poplar; D2: common reed only in lined basins the flood
# passes by). Figures through ps_fig / ps_zones (M7, revision 30 Oct; R2-C). All four sections
# look downstream: the NE bank (left bank) on the left, the SW bank on the right, as the key map's triangles show.
# Drawn in print mm (k = PS_K mm per m, 1:500 since v19); parts/90_booklet.py exports it in metres (no sheet).
# Revision 30 Oct (T6, booklet p12): people are the M7 figures at 1.75 m (D9 layer 0 at the cut), plants the M6
# species at their sourced heights in mixed, wet-to-dry scatters (G9), checked by sf_assert_g6 (G6); the water is the
# M5 section (average yearly flow, never dry; Q100 / Q500 from the cut registry); every bank is a designed place with
# its reason (G10): walks, bike lanes, a stair down the W1 wall into the bed, life in the wet bed, the W4 ramp to a
# viewing terrace and the boardwalk; faded trees behind the cut (R16). Each section is drawn in style "b" (vector)
# and "a" (cutouts, D1) from the same geometry (PsSec.style).
# Round 2 (R2-C, 31 Oct, PG3 p12 #6-#7): people only by zone (fig_place_zones, R2-A): in the water only on stepping
# stones (no wading figures: they are the one drawn pose left), passing the average-flow water so nobody stands in a
# water-filled channel; far people and plants on depth layers 1 / 2; planting in mixed groups (pla_group_section),
# emergent species only where the ground is under water; the trees behind the cut stand on their own layer's ground
# (the cut line incl. the bed, none on the water) under the D8 sky; every item seated (G14, log line); the Q500 wash
# around people is gone (Q100 / Q500 stay lines); every label is a numbered callout "Element: reason" (SfCallouts)
# with its key under the drawing; the section triangles are switched off (U22).
# R2-C pass 2 (Aras 31 Oct 12:01): W1 redrawn to p.17's F1 layout (path and bike lane under the SW trees, view
# terrace on the NE wall top, reed basins beyond) with sitting steps, landings and planted pockets as the way down (no
# straight stair, no blocks in the bed); background houses from the basemap on every depth layer (ps_back); people
# as scenes looking at the water (ps_zones focus).
# v16 (round 3, booklet p12: P12.3-P12.5, G15, G16, DATA-1): each cut tells its scenario (title) and names its use
# zones under the drawing with a reason (R07, ps_zone_strip); people in front (new poses through FIG_ACTIVITY and
# water_edge zones), big trees on depth layer 1 (behind, paler: R05 / R06), street elements with a reason, a quiet sky
# per cut id with a few birds (D3), none of the back trees in the channel, one 1:200 zoom inset in the cut's own free
# sky (U29); cut ends W1 / W1' and the banks by place under the drawing (D6); the walled beds from the surveyed
# sections (water board data/CUTS.py), the summer strip on the survey low point (B2 finding, Aras ask 1 a).
# v17 (round 4, S7, P13.1 / D2): 1:250 on the booklet page, two cuts per page, one cut per full row (CHK-8); numbers
# (mk_marker) instead of callout circles, the words in a side column / strip, level marks outside, insets 1:100.
PS_SCALE = 500                      # v19 (round 5, N3 a, Aras 1 Nov 22:44): W1-W4 merged on one page at 1:500 (was 1:250)
PS_K = 1000.0 / PS_SCALE              # print mm per m (k of section_parts and plants)
PS_DEPTH = 1.0                        # m of cut ground drawn under the bed (section_parts drawing rule)
PS_WALL_T = 0.60                      # m: DSİ wall thickness: no sourced value; the same 0.60 m as p.04-05 (site board P45_WALL_T_M, G2)
PS_RAIL_H = 1.10                      # m: railing height on the wall and bank tops: drawing value
PS_BASIN = dict(kerb_h=0.30, depth=1.10, media=0.80, kerb_t=0.15)   # W1 reed basin cell beyond the NE wall: the
#                                     same drawing values as p.17's F1 (water board P17_BASIN; no source)
PS_STRIP = (3.00, 0.40)               # m: the summer strip channel in the bed (proposal): width, depth
PS_FREEBOARD = 0.30                   # m: a dry proposed floor sits at least this far above Q500 (design rule)
PS_LBL = 7.0 * PT                     # print mm: labels, list, level marks (GRID_TYPE label 7 pt; v17)
PS_TTL = 10.0 * PT                    # section titles (GRID_TYPE heading 10 pt bold; v17)
PS_NOTE = 8.0 * PT                    # the scenario after a title
PS_TIMBER = SF_LANE["timber"]         # boardwalk timber: the same tone as the M8 terraces and lanes
PS_STAIR = (0.30, 0.18)               # m: tread, largest rise of the stairs drawn here (design rule)
PS_RAMP = 1.0 / 12.0                  # rise per run of the W4 ramp (design rule)
PS_TERRACE_W = 4.0                    # m: the W4 viewing terrace's width across the cut (design rule)
# W1 = p.17's F1 (Aras 31 Oct 12:01): the SW path and bike lane widths of p.17 (water board P14_PROM_W, same cut)
# and the way down into the walled bed as sitting steps with landings (design rules, not data)
PS_W1_LANES = (7.0, 3.0)              # m: SW path, SW bike lane (p.17 F1)
PS_W1_SIT = (0.80, 0.45)              # m: sitting step tread (sit, feet on the step below), largest riser (seat high)
PS_W1_FLIGHTS = 3                     # flights of sitting steps, a landing between two flights
PS_W1_LAND = 2.40                     # m: a landing: the way on at its front, a planted pocket at its back
PS_W1_POCKET = (1.20, 0.60)           # m: the planted pocket on a landing: width, soil depth
PS_W1_FLOOR_W = 1.60                  # m: the floor at the water's edge (on the DSİ wall foot, cut down to it)
PS_W1_FLOOR_UP = 0.25                 # m: that floor at least this far over the average-flow water (stays dry)
PS_RAIL_DROP = 0.50                   # m: a drop deeper than this gets a railing (design rule)
PS_STONE_UP = 0.15                    # m: stepping stone tops over the average-flow water (sf_stepping_stones default)
PS_WHY = {"shade": u"shade", "cleaning": u"clean the water", "perception": u"seasonal colour",
          "wind": u"cut the wind", "noise": u"cut street noise", "corridor": u"ecological corridor"}
PS_SHORT = {"plane": u"Plane", "ash": u"Ash", "willow": u"Willow", "olive": u"Olive", "tamarisk": u"Tamarisk",
            "chaste": u"Chaste tree", "rosemary": u"Rosemary", "lavender": u"Lavender", "loosestrife": u"Loosestrife",
            "soft_rush": u"Soft rush", "rush": u"Sharp rush", "stone_pine": u"Stone pine"}
# where each cut crosses the stream axis (survey m; the cut centres of the level table's W rows): the drawn span runs
# from it to the cut's two ends (level_ends), NE end on the left
PS_AXIS = {"W1": (29693.022, 32569.176), "W2": (29959.774, 32264.566), "W3": (30354.663, 31689.671),
           "W4": (30991.856, 31039.404)}
# (sheet key = the surveyed section's key in data/CUTS.py, cut id, number on the page, name, scenario in the title)
# v16 (G15): the scenario says what we offer at that spot and how it differs from the next cut; (G16) bridges by name
PS_CUTS = [("up", "W1", 1, u"Upstream entry",
            u"the quiet entry: sitting steps down into the walled bed, reed basins beyond the Kale side wall clean "
            u"stream water"),
           ("k4", "W2", 2, u"%s walking hub" % bridge_name("K4", short=True),
            u"the busy hub: a dry square in the planes' shade above Q500, seating steps down to the summer strip"),
           ("k5", "W3", 3, u"%s · Demeter's Garden" % bridge_name("K5", short=True),
            u"room for the stream: an open commons the floods may cover, the garden raised above Q500 behind it"),
           ("down", "W4", 4, u"Downstream reach",
            u"the wild edge: planting bands and a boardwalk by flood level, a step-free ramp to a viewing terrace")]
PS_SKY_OVER = 2.0                     # m of sky over the tallest back crown (drawing rule: room for the birds)
PS_INSET_SCALE = 100                  # v17 (G-R4-5.6, D11): the zoom inset's scale, 2.5 x the 1:250 parent
PS_INSET_K = 1000.0 / PS_INSET_SCALE  # its print mm per m
PS_FLAT_TOL = 0.20                    # m: a surveyed floor this level or better is drawn flat (drawing rule)
# v17 (CHK-8, design spec S7): at 1:250 W3 and W4 are cut on their SW side with a break mark like W2 (W3 keeps 10 m of
# Demeter's Garden with its tomato rows and café; W4 keeps 6 m of the cotton field behind the crest)
PS_BREAK = {}                         # v19 (N3 a "spans widened"): no break at 1:500, each cut drawn to its cut end
#                                       (level table ends; never beyond them: no ground is invented); was W2/W3 SW 50 m, W4 38 m
# m of level ground drawn behind an embankment crest (default 3.0): W4 NE 8.0 for the crest walk, bike lane and tree
# corridor (the level table's survey source reads that crest "50.0 m out", about 8 m behind the angled crest)
PS_CREST_FLAT = {("W4", "NE"): 8.0}       # W2's SW land (flat street level to the cut end 80 m out) drawn to 50 m, broken


def ps_lv(z):
    return u"+%.2f" % z


def ps_put(pg, shapes):
    """house shapes of the shared modules -> page items: multi-ring polys here, everything else (poly, line, text,
    image) through M5 shp_put"""
    for s in shapes or []:
        if not s:
            continue
        if s[0] == "poly" and s[1] and isinstance(s[1][0][0], (list, tuple)):
            pg.poly(s[1], fill=s[2], stroke=s[3] if len(s) > 3 else None, lw=(s[4] if len(s) > 4 and s[4] else 0.1),
                    alpha=s[5] if len(s) > 5 else None)
        else:
            shp_put(pg, [s])


def ps_xform(items, s, dx, dy):
    """xform with the D1 a "image" items kept in their place in the drawing order"""
    out = []
    for it in items:
        if it[0] == "image":
            _, x, y, w, h, path, a, flip, clip = (tuple(it) + (None,) * 9)[:9]
            out.append(("image", dx + s * x, dy + s * y, w * s, h * s, path, a, flip,
                        (dx + s * clip[0], dy + s * clip[1], dx + s * clip[2], dy + s * clip[3]) if clip else None))
        else:
            out += xform([it], s, dx, dy)
    return out


def ps_bbox(items):
    """items_bbox with the image items' extents"""
    b = items_bbox([it for it in items if it[0] != "image"])
    ims = [it for it in items if it[0] == "image"]
    if not ims:
        return b
    xs = [it[1] for it in ims] + [it[1] + it[3] for it in ims]
    ys = [it[2] for it in ims] + [it[2] + it[4] for it in ims]
    if b == (0.0, 0.0, 0.0, 0.0) and len(ims) == len(items):
        return (min(xs), min(ys), max(xs), max(ys))
    return (min([b[0]] + xs), min([b[1]] + ys), max([b[2]] + xs), max([b[3]] + ys))


def ps_z_at(prof, u):
    """the level (m) of the cut line prof [(u, z)] at u (its highest where it is vertical)"""
    if u <= prof[0][0]:
        return prof[0][1]
    best = None
    for (ua, za), (ub, zb) in zip(prof[:-1], prof[1:]):
        if ua <= u <= ub:
            z = za if ub - ua < 1e-9 else za + (zb - za) * (u - ua) / (ub - ua)
            best = z if best is None else max(best, z)
    return best if best is not None else prof[-1][1]


class PsSec(object):
    """One section: its own page in print mm, (0, 0) = (left end u0, PS_DEPTH under the bed); u = m across the stream
    from the axis (NE negative), z = m a.s.l."""

    def __init__(self, cid, u0, u1, d, style="b", k=None):
        self.cid, self.u0, self.u1, self.d = cid, float(u0), float(u1), d
        self.style = style                                    # D1: "b" vector, "a" cutouts, one geometry
        self.trees = []                                       # (key, x, h_m, crown_m) at the cut, for the G6 check
        self.bed = level(cid, "bed")
        self.z0 = self.bed - PS_DEPTH
        self.k = k or PS_K                                    # v19: an inset child is drawn again at its own k (G-R5-5)
        self.back_at = 0                                      # v19: item index after the sky and back layers (bridges)
        self.inset_fr = None                                  # v19: sf_inset_frame result (window m, den, k)
        self.hw = level(cid, "bed_width_cm") / 200.0          # half the bed width (m), the bed centred on the axis
        self.pg = Page(0, 0)
        self.calls = []                                       # (text "Element: reason", u, z where its circle sits)
        self.notes = []                                       # log notes of this section (planting that did not fit)
        self.info = []                                        # other log lines of this section (background houses)
        self.prof = []                                        # the cut line (u, z), left to right, for the flood
        self.w = (self.u1 - self.u0) * self.k
        # v16: the bed from the survey (gb = level function of u between the walls, None = flat at the registry
        # bed), the summer strip's centre (u), the use zones named under the drawing (name, reason, ua, ub), the
        # boxes (page mm) of tall things the zoom inset keeps clear of, the inset's spot (ua, ub, za, zb, what)
        self.gb, self.st_c = None, 0.0
        self.zones, self.obst, self.inset = [], [], None
        self.y_top = None                                     # page y of the sky's top (ps_back)
        self.boxes = []                                       # drawn inset boxes (page mm), for the overlap test
        self.inset_busy = None                                # the inset with its label (page mm): callouts keep off
        self.page = None                                      # v17: the booklet page id ("p13a" / "p13b")
        self.marks, self.list = [], []                        # v17: numbers (x, y, n, colour), list (n, text, colour)

    def gbed(self, u):
        """the bed's level (m) at u: the survey profile, else the registry bed"""
        return self.gb(u) if self.gb else self.bed

    def zone(self, name, reason, ua, ub, kind="zone"):
        """a use zone over its span ua..ub (m); v17: numbered on its ground (ps_marks) and named in the side list,
        "Name · reason"; kind "zone" (designed) or "water" (bed, stones, wet edge) sets the number's colour"""
        self.zones.append((name, reason, min(ua, ub), max(ua, ub), kind))

    def X(self, u):
        return (u - self.u0) * self.k

    def Y(self, z):
        return (z - self.z0) * self.k

    def P(self, pts):
        return [(self.X(u), self.Y(z)) for u, z in pts]

    def U(self, x):
        return self.u0 + x / self.k

    def zf(self, f):
        """a level function of u (m) -> a page-y function of page x"""
        return lambda x: self.Y(f(self.U(x)))

    def put(self, shapes):
        ps_put(self.pg, shapes)

    def call(self, text, u, z, kind="built", key=None):
        """a numbered element "Element: reason": its number at (u, z) m (v17: mk_marker, ps_marks); kind "built"
        (street elements, today's wall: ink), "zone" (accent) or "plant" (key = its tallest species: that colour)"""
        self.calls.append((text, u, z, kind, key))


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
            e = max(e, hw + h / math.tan(math.radians(level(cid, "angle_deg", side))) + PS_CREST_FLAT.get((cid, side), 3.0))
        elif kind == "loose_earth":
            e = e + 4.0
        ext[side] = e
    br = PS_BREAK.get(cid)
    if br:
        ext[br[0]] = min(ext[br[0]], br[1])
    return -ext["NE"], ext["SW"], d


def ps_water_y(S):
    """the page y of the water at the average yearly flow (G8): wet ground under it takes only emergent plants and
    no people (fig_place_zones water=)"""
    return S.Y(level_avg_flow(S.cid))


def ps_gprof(S):
    """the cut line S.prof as a page polyline whose x only grows (a wall's two points 0.05 mm apart), so the G14
    seat helpers read it as a ground function: the bed included, the walls nearly vertical"""
    out = []
    for x, y in S.P(S.prof):
        if out and x <= out[-1][0]:
            x = out[-1][0] + 0.05
        out.append((x, y))
    return out


def ps_obst(S, x, gy, h_m, crown_m, layer=0):
    """v16: the box (page mm) of one drawn plant (x, seated on page y gy, its depth layer's size) for the zoom inset's
    free-sky search"""
    sc = fig_depth(layer)[0] if layer else 1.0
    hw_ = 0.55 * crown_m * S.k * sc
    S.obst.append((x - hw_, gy, x + hw_, gy + h_m * S.k * sc * 1.02, int(layer or 0)))   # v17: + its depth layer


def ps_survey(S, key, log):
    """v16 DATA-1 (B2 finding: the W1 surveyed bed slopes; Aras ask 1 a: survey bed, the summer strip on the survey
    low point): the cut's surveyed section from the water board's data/CUTS.py row `key` (ground every 1 m over the
    bed low point, u0 = its SW end, + toward the NE bank), used only when its bed and length match the level module
    (else FLAG, flat). Walled cuts: the bed between the DSİ walls follows the survey, the profile placed so both wall
    feet stand level (drawing rule: the survey predates the walls and the cut's axis is not the survey's stream
    lines; for W1 this lands within ~2 m of p.17's stream-line walls). Unwalled cuts: the banks stay the level table's,
    the bed flat at the registry bed (the survey floor's relief logged). In both, the strip moves onto the survey's
    lowest point inside the drawn bed. Sets S.gb, S.st_c."""
    c, hw = S.cid, S.hw
    row = next((r for r in CUTS if r.get("key") == key), None) if "CUTS" in globals() else None
    ln = level(c, "length_m")
    if not row or not row.get("ground") or row.get("bed") is None:
        log.append(u"FLAG p12 %s: no surveyed section (data/CUTS.py \"%s\"): bed flat at %s, strip on the axis" % (
            c, key, ps_lv(S.bed)))
        return
    g = [float(v) for v in row["ground"]]
    if abs(float(row["bed"]) - S.bed) > 0.005 or (ln and abs(len(g) - 1 - ln) > 1.0):
        log.append(u"FLAG p12 %s: data/CUTS.py \"%s\" (bed %s, %d m) does not match the level module (bed %s, %s m): "
                   u"bed flat, strip on the axis" % (c, key, row["bed"], len(g) - 1, ps_lv(S.bed), ln))
        return
    u0 = float(row["u0"])

    def gz(uc):                                                # m over the bed at survey u (+ toward NE)
        t = max(0.0, min(len(g) - 1.0, uc - u0))
        i = min(len(g) - 2, int(t))
        return g[i] + (g[i + 1] - g[i]) * (t - i)
    walled = ps_kind(c, "NE") == "dsi_wall" and ps_kind(c, "SW") == "dsi_wall"
    cc = 0.0                                                   # survey u that sits on the drawn axis
    if walled:
        cand = [u0 + hw + 0.1 * i for i in range(int(max(0.0, (len(g) - 1) - 2.0 * hw) / 0.1) + 1)]
        if cand:
            cc = min(cand, key=lambda q: (round(abs(gz(q + hw) - gz(q - hw)), 2), abs(q)))
        S.gb = lambda u, _c=cc: S.bed + gz(_c - u)             # drawn u (NE negative) -> survey u (NE positive)
    us = [-hw + 0.25 * i for i in range(int(2.0 * hw / 0.25) + 1)]
    zs = [gz(cc - u) for u in us]
    low = us[zs.index(min(zs))]
    half = PS_STRIP[0] / 2.0
    S.st_c = max(-hw + 0.3 + half, min(hw - 0.3 - half, low))
    if walled:
        log.append(u"p12 %s: bed between the DSİ walls from the surveyed section (data/CUTS.py \"%s\", bed %s, every "
                   u"1 m), placed with both wall feet at +%.2f m over the low point (%.1f m off the cut axis); "
                   u"summer strip moved onto the survey low point at u %.1f m" % (
                       c, key, ps_lv(S.bed), gz(cc + hw), cc, S.st_c))
    else:
        fl = [z for z in zs if z <= 0.5]                       # the survey floor (the TIN floor rule: within 0.5 m)
        rel = (max(fl) - min(fl)) if fl else max(zs) - min(zs)
        log.append(u"%sp12 %s: survey floor level within %.2f m (data/CUTS.py \"%s\"): bed drawn flat at %s; summer "
                   u"strip moved onto the survey low point at u %.1f m" % (
                       u"FLAG " if rel > PS_FLAT_TOL else u"", c, rel, key, ps_lv(S.bed), S.st_c))


def ps_fig(S, pose, u, z, facing=1, **p):
    """one person at the cut on dry land only (M7: adult 1.75 m, D9 layer 0), feet at (u, z) seated on the ground
    (G14 sf_seat_x); people near the channel go through ps_zones, never here"""
    x = S.X(u)
    y = sf_seat_x(S.Y(z), x, FIG_FOOT_HALF_M * S.k)
    S.put(fig_side(pose, x, y, S.k, facing=facing, style=S.style, **p))


def ps_zones(S, zones, seed, layer=0, density=1.0, max_n=None, focus=0.0, **p):
    """G10 people zone by zone (figures.py fig_place_zones): zones [(kind, ua, ub, ground)] with ground = a level
    (m) or a function of u (m) -> level; kinds walkway, bike_lane, viewing_terrace, sun_steps, stepping_stones, lawn
    take people, "water" none (counted in the G14 line). The average-flow water is passed, so nobody stands where
    the drawn water covers the ground; layer 1 / 2 = people further from the cut (smaller, paler). Scenes (R2-C pass
    2, Aras 31 Oct 12:01 "they look like they are just put there"): focus = u (m) that everyone who stays looks at
    (default 0.0 = the water's middle on the axis; a stall or a view where the section has one), children playing
    turn to each other, walkers and riders keep their way; p goes to every figure (seat_h ...)."""
    zz = []
    for kind, ua, ub, g in zones:
        zz.append((kind, S.X(min(ua, ub)), S.X(max(ua, ub)), S.zf(g) if callable(g) else S.Y(g)))
    sh, placed = fig_place_zones(zz, S.Y(S.bed), S.k, seed=seed, layer=layer, style=S.style, density=density,
                                 water=ps_water_y(S), max_per_zone=max_n,
                                 focus=None if focus is None else S.X(focus), **p)
    S.put(sh)
    return placed


def ps_lane(S, ua, ub, z, kind, zone=None):
    """an M8 lane (walk, bike, gravel, timber) from ua to ub on level z; zone = (name, reason): v16 (G15, R07) named
    under the drawing over its span (G10)"""
    a, b = sorted((ua, ub))
    S.put(sf_lane(S.X(a), S.Y(z), b - a, S.k, kind=kind))
    if zone:
        S.zone(zone[0], zone[1], a, b)


def ps_street(S, kind, u, z, call, side=1):
    """v16 (G15, U11): a street element where the design has one, at u on level z, seated (G14), with its reason as
    a numbered callout: "lamp" (sf_lamp), "bollard" (sf_bollard), "rack" (sf_bike_rack); sizes are SF_STREET drawing
    rules, never printed"""
    x = S.X(u)
    y = sf_seat_x(S.Y(z), x, 0.1 * S.k)
    if kind == "lamp":
        sh, h = sf_lamp(x, y, S.k, side=side), SF_STREET["lamp_h"]
    elif kind == "bollard":
        sh, h = sf_bollard(x, y, S.k), SF_STREET["bollard_h"]
    else:
        sh, h = sf_bike_rack(x, y, S.k, side=side), SF_STREET["rack_h"]
    S.put(sh)
    S.obst.append((x - 0.6 * S.k, y, x + 0.6 * S.k, y + (h + 0.3) * S.k, 0))
    if call:
        S.call(call, u, z + h + 0.6)                          # v17: the number at the element's top


def ps_group_text(keys, tags, why=None):
    """the callout of one planting group: "Plane + chaste tree: shade the walk" from the species (tallest first) and
    the group's sourced purpose tags (pla_group_section); why = {tag: words} says it for this place; None when the
    group has no sourced purpose"""
    why = why or {}
    order = [t for t in why if t in tags] + [t for t in ("shade", "cleaning", "wind", "noise", "corridor",
                                                         "perception") if t in tags and t not in why]
    if not order:
        return None
    reason = u", ".join(why.get(t, PS_WHY[t]) for t in order[:2])
    ks = sorted(keys, key=lambda k_: -(PLA_SPECIES[k_].get("h_m") or 0.0))
    for n in (3, 2, 1):
        names = [PS_SHORT.get(k_, PLA_SPECIES[k_]["name"]) for k_ in ks[:n]]
        t = u" + ".join([names[0]] + [m_[0].lower() + m_[1:] for m_ in names[1:]]) + u": " + reason
        if len(t) <= 55 or n == 1:
            return t
    return None


def ps_group(S, ua, ub, zf, t0, t1, mix, seed, layers=(0,), why=None, avoid=(), density=1.0, call=True):
    """G9 planting from ua to ub (m) on the ground zf(u): mixed groups (plants.py pla_group_section: two or more
    species, overlapping crowns, the low layer under and around, depth layers back to front), band t0 (wet) to t1
    (dry); where the ground lies under the average-flow water only emergent species; every plant seated (G14).
    One callout per group saying what it does there (call=False: none). Returns the groups."""
    a, b = sorted((ua, ub))
    av = [tuple(sorted((S.X(p), S.X(q)))) for p, q in avoid] or None
    sh, placed, groups = pla_group_section(S.X(a), S.X(b), S.zf(zf), S.k, t0=t0, t1=t1, mix=mix, seed=seed,
                                           layers=layers, style=S.style, density=density, avoid=av,
                                           water=ps_water_y(S))
    S.put(sh)
    for key, x, h, cr, layer in placed:
        S.trees.append((key, x, h, cr))                       # G6: every plant inside its sourced height range
        ps_obst(S, x, S.Y(zf(S.U(x))), h, cr, layer)
    if not groups:
        S.notes.append(u"no mixed group fits %.1f-%.1f m (%s)" % (a, b, u", ".join(sorted(mix))))
    for layer, xa, xb, ks, tags in groups:
        t = ps_group_text(ks, tags, why) if call else None
        if not t:
            continue
        top = max([h for k_, x, h, cr, l_ in placed if l_ == layer and xa - 0.5 * cr * S.k <= x <= xb] or [2.0])
        u = S.U(0.5 * (xa + xb))
        tall = max(ks, key=lambda k_: PLA_SPECIES[k_].get("h_m") or 0.0)
        S.call(t, u, zf(u) + top * (fig_depth(layer)[0] if layer else 1.0) * 0.8, "plant", tall)   # v17: in the crown
    return groups


def ps_back(S, seed, mix=("plane", "chaste", "olive", "tamarisk")):
    """the D8 sky and the depth behind the cut (R16): D9 layers 2 and 1, each on its own ground = the cut line with
    the bed (G14), the farthest first: R2-C pass 2 (Aras 31 Oct 12:01 "no background houses"; checklist 7) the
    basemap houses SF_BACK_BAND m behind the registry cut (sf_back_buildings: data height, else floors x
    BLD_STOREY; nearer than the band's middle on layer 1, the rest on layer 2) standing on the layer's ground
    (sf_back_house: real profiles, faded by layer, seated), then that layer's faded mixed tree groups round them;
    no house over the channel (it runs on behind the cut) or whose roof leaves the sky, no tree where the ground
    lies under the average-flow water"""
    pr = ps_gprof(S)
    gf = sf_gy(pr)
    wy = ps_water_y(S)
    # v16 (G15, P12.3): the sky reaches PS_SKY_OVER over the tallest back crown (layer 1, the nearest back layer), so
    # it never dominates and the section stays low enough for its cell; a sky of its own per cut id, birds on (D3)
    # v17 (1:250, design spec S7): ash left the BACK mix (front groups keep it), so the sky ends 15 m over the
    # highest ground and two cuts fit one page
    ht = max(PLA_SPECIES[k_]["h_m"] for k_ in mix) * PLA_GROUP["size"][1] * fig_depth(1)[0] + PS_SKY_OVER
    y_top = S.Y(max(z for _u, z in S.prof) + ht)
    S.y_top = y_top
    wl = sf_atmosphere(0.0, S.w, pr, y_top, S.k, seed=seed, sky="d8", trees=False, birds=True, style=S.style,
                       back_ground={2: pr, 1: pr}, cid=S.cid)
    lab = level_end_labels(S.cid)                               # registry m along the cut (t) -> u: the first end's
    d0, sg = S.d[lab[0]], (-1.0 if lab[0] == "SW" else 1.0)    # distance to the axis; SW positive, NE negative
    lo = min(S.prof[0][1], S.prof[-1][1]) - 0.5                 # the channel: the cut line under both land levels
    cu = [u for u, z in S.prof if z < lo]
    ch = (min(cu), max(cu)) if cu else None
    chx = [(S.X(ch[0]), S.X(ch[1]))] if ch else []              # v16 (G8): no back tree in the channel, wet or dry
    blds = sf_back_buildings(S.cid, *sorted((d0 + sg * S.u0, d0 + sg * S.u1)), log=S.info, look=-1)   # the key map's view (SW right)
    dmid = 0.5 * (SF_BACK_BAND[0] + SF_BACK_BAND[1])
    nh, nx = 0, 0
    for layer in (2, 1):
        hs = []
        for ta, tb, h_m, fl, db in blds:                       # this layer's houses, before its trees
            if (1 if db < dmid else 2) != layer or tb - ta < 3.0:   # a sliver under one bay (sf_back_house's 3.0 m)
                continue
            ua, ub = sorted((sg * (ta - d0), sg * (tb - d0)))
            if ch and ub > ch[0] and ua < ch[1]:
                nx += 1
                continue
            hh = sf_back_house(S.X(ua), S.X(ub), pr, h_m, S.k, layer=layer, floors=fl, d_m=db)   # v17: windows <= 30 m
            if not hh or max(p_[1] for s_ in hh for p_ in s_[1]) > y_top:
                nx += 1
                continue
            wl.add("background", hh)
            hs.append((S.X(ua), S.X(ub)))
            S.obst.append((S.X(ua), min(p_[1] for s_ in hh for p_ in s_[1]), S.X(ub),
                           max(p_[1] for s_ in hh for p_ in s_[1]), layer))
            nh += 1
        sh, pl_, _gr = pla_group_section(0.0, S.w, gf, S.k, t0=0.45, t1=0.95, mix=list(mix), seed=seed + 31 * layer,
                                         layers=(layer,), style=S.style, density=0.7, avoid=(hs + chx) or None,
                                         hires=False, detail=False, water=wy)
        wl.add("background", sh)
        for key, x, h, cr, l_ in pl_:
            ps_obst(S, x, gf(x), h, cr, l_)
    wl.put(S.pg)
    S.back_at = len(S.pg.items)                                 # v19: a bridge beyond the cut goes in here (behind)
    S.info.append(u"%d background houses drawn (%d left out: over the channel or above the sky)" % (nh, nx))


def ps_land(S, pts, material="earth"):
    """cut ground under a surface [(u, z)] left to right, down to the drawing's bottom"""
    S.put(sct_ground(S.P(pts), 0.0, S.k, material))


def ps_strip(S):
    """the summer strip channel (PS_STRIP) at S.st_c (v16: the survey low point, ps_survey), cut PS_STRIP depth
    under the lowest bed point it spans: its four points"""
    w, dp = PS_STRIP
    a, e = S.st_c - w / 2.0, S.st_c + w / 2.0
    fl = min(S.gbed(a + (e - a) * i / 8.0) for i in range(9)) - dp
    return [(a, S.gbed(a)), (a + 0.6, fl), (e - 0.6, fl), (e, S.gbed(e))]


def ps_bed_pts(S, uL, uR):
    """v16: the bed surface from uL to uR (m) with the summer strip cut in: the survey every 1 m where S.gb, else
    flat at the registry bed. Put it into S.prof between the banks."""
    st = ps_strip(S)
    pts = [(uL, S.gbed(uL))]
    if S.gb:
        u = math.floor(uL) + 1.0
        while u < st[0][0] - 0.3:
            pts.append((u, S.gbed(u)))
            u += 1.0
    pts += st
    if S.gb:
        u = math.ceil(st[-1][0] + 0.3)
        while u < uR - 0.3:
            pts.append((u, S.gbed(u)))
            u += 1.0
    return pts + [(uR, S.gbed(uR))]


def ps_bed(S, uL, uR, call=(u"Stepping stones", u"cross the summer strip dry-shod"), stones=True):
    """the gravel bed from uL to uR with the summer strip (v16: the surveyed bed and the strip on its low point are
    in S.prof already, ps_bed_pts), then the M5 water (G8): the average yearly flow filling the bed below it (never
    dry), Q100 and Q500 wall to wall (lines only; v17: their levels are marked outside the drawing, ps_page);
    stepping stones across the strip (stones=False: none, W1), named as a zone (call = (name, reason)).
    Returns (u from, u to, level) of the stones' tops: the only place in the water people stand."""
    st = ps_strip(S)
    S.put(sct_ground(S.P(ps_bed_pts(S, uL, uR)), 0.0, S.k, "gravel"))
    # v17 (G-R4-5.4): no level labels in the picture; the levels are marked outside the frame (ps_page)
    wl = water_section(S.P(S.prof), S.k, S.Y, cid=S.cid, fill_ground=False, labels=False)
    wl.put(S.pg)
    ua, ub, ztop = st[0][0] - 0.2, st[-1][0] + 0.2, level_avg_flow(S.cid) + PS_STONE_UP
    if not stones:
        return ua, ub, ztop
    S.put(sf_stepping_stones(S.X(ua), S.X(ub), S.Y(st[1][1]), ps_water_y(S), S.k, above_m=PS_STONE_UP,
                             seed=len(S.cid)))
    if call:
        S.zone(call[0], call[1], ua, ub, "water")
    return ua, ub, ztop


def ps_stair_z(u_bot, z_bot, n, rise, tread, side):
    """the tread level (m) at u of a flight climbing from (u_bot, z_bot) toward side"""
    def f(u):
        i = int(math.ceil((u - u_bot) * side / tread - 1e-9))
        return z_bot + rise * max(0, min(n, i))
    return f


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


def ps_arrow(S, pts, col, lw=0.3, dash=None):
    P = S.P(pts)
    S.pg.line(P, col, lw, dash=dash)
    (ax, ay), (bx, by) = P[-2], P[-1]
    L = math.hypot(bx - ax, by - ay) or 1e-9
    ux, uy, h = (bx - ax) / L, (by - ay) / L, 1.1
    S.pg.poly([[(bx, by), (bx - ux * h - uy * h * 0.45, by - uy * h + ux * h * 0.45),
                (bx - ux * h + uy * h * 0.45, by - uy * h - ux * h * 0.45)]], fill=col)


def ps_low(S, ua, ub, zf, seed, t0=0.55, t1=0.95, avoid=(), density=1.2):
    """v17 (G-R4-5.2, D7): the low layer of sourced shrubs and flowers (plants.py pla_low_section: chaste tree,
    rosemary, French lavender, purple loosestrife, soft rush, mixed by wetness, never in rows) on a soft bank from ua
    to ub (m) on the ground zf(u), seated (G14); avoid = [(u, u)] spans kept free (lanes, benches)"""
    a, b = sorted((ua, ub))
    if b - a < 1.0:
        return
    av = [tuple(sorted((S.X(p), S.X(q)))) for p, q in avoid] or None
    sh, placed = pla_low_section(S.X(a), S.X(b), S.zf(zf), S.k, t0=t0, t1=t1, seed=seed, density=density, avoid=av,
                                 water=ps_water_y(S))
    S.put(sh)
    for key, x, h, cr in placed:
        S.trees.append((key, x, h, cr))
        ps_obst(S, x, S.Y(zf(S.U(x))), h, cr, 0)


def ps_break(S, z_top):
    """the break line at the drawing's right end (the land goes on to the cut end; PS_BREAK), from the drawing's
    bottom to just over the ground at z_top"""
    xb = S.X(S.u1)
    yb, yt = S.Y(S.z0), S.Y(z_top)
    S.pg.line([(xb, yb - 0.6), (xb, yb + 0.35 * (yt - yb)), (xb - 0.7, yb + 0.45 * (yt - yb)),
               (xb + 0.7, yb + 0.6 * (yt - yb)), (xb, yb + 0.7 * (yt - yb)), (xb, yt + 0.8)], COL["ink"], 0.2)


# ---------------------------------------------------------------- W1 upstream entry
def ps_pocket(S, ua, ub, z, seed):
    """a planted pocket on a W1 landing (ua..ub m, soil at z, PS_W1_POCKET deep): a chaste tree with rosemary and
    lavender round it (G9: mixed, overlapping, sourced sizes PLA_SPECIES), each seated (G14); one callout (the same
    words on every landing: one number)"""
    ps_block_ring(S, ua, ub, z - PS_W1_POCKET[1], z, "earth")
    for i, (key, f) in enumerate((("chaste", 0.62), ("rosemary", 0.28), ("lavender", 0.82))):   # tall one first
        sp = PLA_SPECIES[key]
        x = S.X(ua + f * (ub - ua))
        S.put(pla_section(key, x, sf_seat_x(S.Y(z), x, 0.35 * sp["crown_m"] * S.k), S.k, h_m=sp["h_m"],
                          crown_m=sp["crown_m"], seed=seed + i, style=S.style))
        S.trees.append((key, x, sp["h_m"], sp["crown_m"]))
    t = ps_group_text(["chaste", "rosemary", "lavender"], ("perception",),
                      {"perception": u"colour and scent by the seats"})
    S.call(t, (ua + ub) / 2.0, z + 0.8 * PLA_SPECIES["chaste"]["h_m"], "plant", "chaste")


def ps_sec_w1(S):
    """W1 = p.17's F1 (same registry cut; Aras 31 Oct 12:01 "f1 has better surrounding"): the SW bank's path and
    bike lane under the trees with a bench, the viewing terrace on the NE wall top, the lined reed basins beyond it
    on the NE side, the walled bed at the registry levels. The way into the bed is no straight stair: sitting steps
    cut back into the SW bank in PS_W1_FLIGHTS flights (seat-high risers, treads to sit on), landings with a planted
    pocket between them, a floor at the water's edge on the DSİ wall foot (railed: deeper than PS_RAIL_DROP to the
    bed). No blocks in the bed and nobody in its water. v16: the bed from the survey (ps_survey), the edge floor on
    it at the SW wall foot; zones named under the drawing; a lamp at the path; the inset on the floor and steps."""
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, tS = level(c, "top", "NE"), level(c, "top", "SW")
    # the edge floor: dry at the average flow and (v16, DATA-1) never under the surveyed bed at the SW wall foot
    fl = math.ceil(max(level_avg_flow(c) + PS_W1_FLOOR_UP, S.gbed(hw)) * 20.0) / 20.0
    n = int(math.ceil((tS - fl) / PS_W1_SIT[1] - 1e-9))
    rise = (tS - fl) / n
    nf = max(1, min(PS_W1_FLIGHTS, n))
    fls = [n // nf + (1 if i < n % nf else 0) for i in range(nf)]
    u, z = hw + PS_W1_FLOOR_W, fl
    steps, blocks, flights, lands = [(hw, fl), (u, fl)], [], [], []
    for i, m in enumerate(fls):                                 # flight by flight, climbing to the SW (right)
        uf = u
        for j in range(m):
            z += rise
            steps.append((u, z))
            if i == nf - 1 and j == m - 1:
                break
            w = PS_W1_LAND if j == m - 1 else PS_W1_SIT[0]
            blocks.append((u, u + (w - PS_W1_POCKET[0] if j == m - 1 else w), z - rise - 0.15, z))
            if j == m - 1:
                flights.append((uf, u))
                lands.append((u, u + w, z))
            u += w
            steps.append((u, z))
    flights.append((uf, u))
    u_top = u
    S.prof = [(S.u0, tN), (-hw, tN)] + ps_bed_pts(S, -hw, hw) + steps + [(S.u1, tS)]
    gstep = lambda u_: ps_z_at(steps + [(S.u1, tS)], u_)
    # SW bank top (p.17 F1): the path next to the steps' head, a tree strip with the bench, the bike lane outside
    pa = (u_top + 0.3, u_top + 0.3 + PS_W1_LANES[0])
    bk = (S.u1 - 0.4 - PS_W1_LANES[1], S.u1 - 0.4)
    if bk[0] < pa[1] + 1.0:
        S.notes.append(u"the SW path and bike lane overlap the drawn bank (%.1f m left)" % (bk[0] - pa[1]))
    bn = pa[1] + 0.6                                            # the bench, its back to the bike lane
    # NE (p.17 F1): the viewing terrace on the wall top, the reed basins beyond it (behind the cut, faded)
    vt = (-hw - PS_WALL_T - PS_TERRACE_W, -hw - PS_WALL_T)
    bx = (S.u0 + 0.3, vt[0] - 0.6)
    ps_back(S, 11)
    bp = pla_reed_basin(S.X(bx[0]), S.X(bx[1]), S.Y(tN - PS_BASIN["depth"]), S.Y(tN), k, PS_BASIN["kerb_h"],
                        PS_BASIN["kerb_t"], PS_BASIN["media"])
    S.put(bp)
    ps_land(S, [(S.u0, tN), (-hw, tN)])                         # v16 (D7): no white veil over the basins; the
    ps_land(S, steps + [(S.u1, tS)])                            # cut land drawn after them hides what is behind
    ps_lane(S, pa[0], pa[1], tS, "walk", (u"Path", u"in the shade of the bazaar side trees"))
    ps_lane(S, bk[0], bk[1], tS, "bike", (u"Bike lane", u"through route under the trees"))
    S.put(sf_bench(S.X(bn), sf_seat_x(S.Y(tS), S.X(bn), 0.25 * k), k, side=-1, back=True))
    S.call(u"Bench: in the trees' shade, facing the water", bn - 0.2, tS + 1.4)
    ps_street(S, "lamp", u_top + 0.15, tS, u"Lamp: lights the path and the steps' head after dark", side=1)
    ps_bed(S, -hw, hw, call=None, stones=False)                 # no stones, no blocks in the bed (Aras 12:01)
    S.zone(u"Walled bed", u"left to the stream, summer strip on its low point", -hw, hw, "water")
    ps_wall(S, -hw, -1, tN)
    S.put(sf_terrace(S.X(vt[1]), S.Y(tN), PS_TERRACE_W, k, side=-1, material="timber", rail=False))
    S.zone(u"View terrace", u"on the Kale side wall top, over the water", vt[0], vt[1])
    # SW: today's wall (dashed) cut down to the edge floor, the sitting steps seated into the bank behind it
    S.pg.poly([S.P([(hw, S.gbed(hw)), (hw + PS_WALL_T, S.gbed(hw)), (hw + PS_WALL_T, tS), (hw, tS)])],
              stroke=COL["ink2"], lw=0.18, dash=[0.8, 0.5])
    ps_block_ring(S, hw, hw + PS_WALL_T, S.z0, fl, "stone")    # the wall foot, kept under the floor
    ps_block_ring(S, hw + PS_WALL_T, hw + PS_W1_FLOOR_W, fl - 0.25, fl, "concrete")
    for ua_, ub_, z0, z1 in blocks:
        ps_block_ring(S, ua_, ub_, z0, z1, "stone")
    if fl - S.gbed(hw - 0.5) > PS_RAIL_DROP:
        ps_rail(S, hw + 0.15, fl)
    for i, (ua_, ub_, z_) in enumerate(lands):
        ps_pocket(S, ub_ - PS_W1_POCKET[0], ub_, z_, 50 + 3 * i)
    S.call(u"Dashed line: today's DSİ wall, cut back into steps", hw + PS_WALL_T / 2.0, tS + 0.6)
    S.zone(u"Edge floor", u"on the dry bed edge at the foot of the steps", hw, hw + PS_W1_FLOOR_W)
    S.zone(u"Sitting steps", u"%d flights, planted landings" % nf,
           hw + PS_W1_FLOOR_W, u_top)
    ps_arrow(S, [(S.st_c, level_avg_flow(c) + 0.3), (-hw + 1.2, tN + 2.4), (bx[1] - 0.8, tN + 1.8)],
             COL["river_mid"], 0.3, dash=[0.9, 0.6])            # over the terrace's rail and heads to the basins
    S.zone(u"Reed basins", u"stream water cleaned beyond the wall", bx[0], bx[1])
    # planting (G9 groups, p.17 F1): the trees of the SW bank round the path and bike lane (their crowns over both;
    # v16 G15: on depth layer 1, behind the people and paler), an emergent edge at each wall foot on the surveyed bed
    ps_group(S, u_top + 0.2, S.u1 - 0.2, lambda u_: tS, 0.50, 0.56, {"plane": 1.0, "ash": 0.6, "chaste": 0.8}, 11,
             layers=(1,), avoid=[pa, bk, (bn - 0.6, bn + 0.2)], why={"shade": u"shade the path and bike lane"})
    ps_group(S, -hw + 0.2, -hw + 5.0, S.gbed, 0.02, 0.05, ["soft_rush", "loosestrife"], 18, density=1.2,
             why={"cleaning": u"clean the water by the wall"})
    ps_group(S, hw - 5.0, hw - 0.2, S.gbed, 0.05, 0.02, ["soft_rush", "loosestrife"], 22, density=1.2,
             why={"cleaning": u"clean the water by the steps"})
    ps_low(S, pa[1] + 0.3, bk[0] - 0.3, lambda u_: tS, 12, avoid=[(bn - 0.8, bn + 0.4)])   # v17: shrubs + flowers
    # people as scenes, all looking at the water (focus: the strip): at the floor's railing and sitting on the steps
    # together, one on each landing's way down, on the view terrace; walking, running, walking a dog on the path
    # (FIG_ACTIVITY walkway) and riding the bike lane; more further along the path and the terrace (layer 1); nobody
    # in the bed ("water": counted)
    ps_zones(S, [("water", -hw, hw, b), ("viewing_terrace", hw + 0.3, hw + PS_W1_FLOOR_W - 0.1, fl)] +
             [("sun_steps", fa + 0.05, fb - 0.05, gstep) for fa, fb in flights], 15, density=1.5, seat_h=rise,
             focus=S.st_c)
    ps_zones(S, [("walkway", ua_ + 0.1, ub_ - PS_W1_POCKET[0] - 0.1, z_) for ua_, ub_, z_ in lands], 16, max_n=1,
             focus=S.st_c)
    ps_zones(S, [("viewing_terrace", vt[0] + 0.2, vt[1] - 0.2, tN)], 17, density=1.4, max_n=3, focus=S.st_c)
    ps_zones(S, [("walkway", pa[0], pa[1], tS), ("bike_lane", bk[0], bk[1], tS)], 18)
    ps_zones(S, [("viewing_terrace", vt[0] + 0.2, vt[1] - 0.2, tN), ("walkway", pa[0], pa[1], tS)], 19, layer=1,
             density=0.6, max_n=2)
    S.inset = (hw - 0.5, hw + PS_W1_FLOOR_W + 2.5, fl - 0.6, fl + 2.4, u"edge floor and sitting steps")   # v17: 1:100


# ---------------------------------------------------------------- W2 walking hub (Ulucami Önü)
def ps_sec_w2(S):
    """W2 at the Ulucami Önü bridge: the SW wall opened into a sub-hub floor at the water and seating steps up to a
    dry hub square above Q500 with planes; the NE edge walk and bike lane. v16: the bed between the walls from the
    survey with the strip and the stones on its low point, zones named under the drawing, fishing at the floor's
    water edge, a lamp on the edge walk, bike racks and bollards on the square, the inset on the floor."""
    c, b, hw = S.cid, S.bed, S.hw
    tN, tS = level(c, "top", "NE"), level(c, "top", "SW")
    plat = max(b + 0.30, math.ceil(S.gbed(hw) * 20.0) / 20.0)  # sub-hub floor: just above the summer strip, never
    n, tread = 10, 0.80                                         # under the surveyed bed at the wall line
    rise = (tS - plat) / n
    u_st = hw + 4.0                                             # the steps start 4.00 m behind today's wall line
    steps, blocks = ps_steps(u_st, plat, n, rise, tread, 1)
    u_sq = u_st + n * tread                                     # the hub square from here, at the wall top level
    S.prof = [(S.u0, tN), (-hw, tN)] + ps_bed_pts(S, -hw, hw) + [(hw, plat), (u_st, plat)] + steps + [(S.u1, tS)]
    ps_back(S, 21)
    ps_land(S, [(S.u0, tN), (-hw, tN)])
    ps_land(S, [(hw, plat), (u_st, plat)] + steps + [(S.u1, tS)])
    ps_lane(S, -hw - 0.6, -hw - 4.1, tN, "walk", (u"Edge walk", u"looks across to the seating steps"))
    ps_lane(S, -hw - 4.5, -hw - 6.5, tN, "bike", (u"Bike lane", u"street side, clear of the walk"))
    ps_street(S, "lamp", -hw - 4.3, tN, u"Lamp: lights the edge walk and the bike lane", side=1)
    ua, ub, ztop = ps_bed(S, -hw, hw)
    ps_wall(S, -hw, -1, tN)
    ps_block_ring(S, hw, u_st, plat - 0.25, plat, "concrete")   # sub-hub floor slab
    for ua_, ub_, z0, z1 in blocks:                             # steps seated into the cut-back bank
        ps_block_ring(S, ua_, ub_, z0, z1, "stone")
    ps_block_ring(S, u_sq, S.u1, tS - 0.25, tS, "stone")        # hub square paving
    S.pg.poly([S.P([(hw, S.gbed(hw)), (hw + PS_WALL_T, S.gbed(hw)), (hw + PS_WALL_T, tS), (hw, tS)])],
              stroke=COL["ink2"], lw=0.18, dash=[0.8, 0.5])     # today's DSİ wall, replaced by the steps
    S.call(u"Dashed line: today's DSİ wall, opened into steps", hw + PS_WALL_T / 2.0, tS + 0.6)
    S.zone(u"Sub-hub floor", u"at the water, just above the flow", hw, u_st)
    S.zone(u"Seating steps", u"sun and a view of the water", u_st, u_sq)
    S.zone(u"Hub square", u"dry above Q500, in the planes' shade", u_sq, S.u1)
    ps_street(S, "rack", u_sq + 1.0, tS, u"Bike racks: leave the bike, walk down to the water", side=1)
    ps_street(S, "bollard", S.u1 - 1.0, tS, u"Bollards: the square's street edge, no cars")
    ps_break(S, tS)                                             # break line: the land goes on to the cut end
    # planting (G9 groups; v16 G15: the trees on depth layer 1, behind the people): the square's planes with an
    # understorey (Ottoman squares with plane trees, ICOMOS 2014), the street trees behind the NE lanes, an emergent
    # edge in the bed by the sub-hub floor
    ps_group(S, u_sq + 4.0, S.u1 - 0.5, lambda u: tS, 0.48, 0.8, {"plane": 1.0, "chaste": 0.6, "rosemary": 0.5,
                                                                  "lavender": 0.4}, 20, layers=(1,),
             why={"shade": u"shade the hub square"})
    ps_group(S, S.u0 + 0.3, -hw - 0.8, lambda u: tN, 0.45, 0.9, {"plane": 1.0, "ash": 0.5, "chaste": 0.9,
                                                                   "rosemary": 0.7}, 21, layers=(1,),
             why={"shade": u"shade the street walk"})
    ps_group(S, max(ub + 1.0, hw - 5.0), hw - 0.3, S.gbed, 0.0, 0.14, ["soft_rush", "loosestrife", "rush"], 23,
             why={"cleaning": u"clean the water at the steps"})
    ps_low(S, S.u0 + 0.3, -hw - 6.9, lambda u: tN, 28)          # v17: shrubs + flowers behind the NE lanes
    # people by zone: the NE walk and bike lane (walking, running, a dog), across on the stones, fishing at the
    # floor's water edge, children playing on the dry sub-hub floor, sitting on the steps, walking and standing
    # together in the square; more behind (layer 1)
    ps_zones(S, [("walkway", -hw - 4.1, -hw - 0.6, tN), ("bike_lane", -hw - 6.5, -hw - 4.5, tN),
                 ("water", -hw, ua, b), ("stepping_stones", ua, ub, ztop), ("water", ub, hw, b),
                 ("walkway", u_sq + 2.0, S.u1 - 1.6, tS)], 24, focus=S.st_c)
    ps_zones(S, [("water_edge", hw + 0.3, hw + 1.6, plat), ("lawn", hw + 1.8, u_st - 0.3, plat)], 26, density=1.4,
             focus=S.st_c)                                      # fishing at the edge, children playing together
    ps_zones(S, [("sun_steps", u_st + 0.2, u_sq - 0.2, ps_stair_z(u_st, plat, n, rise, tread, 1))], 27, density=1.6,
             seat_h=rise, focus=S.st_c)                         # sitting together on the steps, facing the water
    ps_zones(S, [("walkway", S.u0 + 0.5, -hw - 0.6, tN), ("walkway", u_sq + 2.0, S.u1 - 1.6, tS)], 25, layer=1,
             density=0.6)
    S.inset = (hw + 0.5, u_st + 1.5, plat - 0.6, plat + 2.4, u"sub-hub floor at the water")      # v17: 1:100


# ---------------------------------------------------------------- W3 K5 Demeter's Garden
def ps_sec_w3(S):
    """W3 at Üç Kemer: bank steps seated into the NE loose earth bank, the stream commons on the SW shelf, Demeter's
    Garden raised above Q500 behind its wall. v16: zones named under the drawing, a lamp on the crest walk, families
    lying and playing on the commons, the strip on the survey low point, the inset on the stones."""
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
    S.prof = [(S.u0, tN)] + list(reversed(steps)) + ps_bed_pts(S, -hw, hw) + [(s0, shelf), (s1, shelf), (s1, gf),
                                                                             (S.u1, gf)]
    ps_back(S, 31)
    # NE: today's loose earth bank (dashed) and the steps seated into it (section_parts earth bank with steps)
    sh, _ = sct_bank("earth", S.X(-hw), S.Y(tN), S.Y(b), -1, k, run_m=run, reach_m=crest - S.u0, depth_m=PS_DEPTH,
                     steps=[(rise, tread)] * n, steps_from_m=0.0, step_material="stone")
    ps_land(S, [(hw, b), (s0, shelf), (s1, shelf), (s1, gf), (S.u1, gf)])   # the garden: fill above the shelf
    S.put(sh)
    old = [(-hw - run * i / 12.0, b + (tN - b) * (3 * (i / 12.0) ** 2 - 2 * (i / 12.0) ** 3)) for i in range(13)]
    S.pg.line(S.P(old), COL["ink2"], 0.18, dash=[0.8, 0.5])
    ua, ub, ztop = ps_bed(S, -hw, hw)
    ps_rail(S, crest - 0.2, tN)
    ps_lane(S, crest - 3.6, crest - 0.3, tN, "walk", (u"Crest walk", u"looks down the steps to the water"))
    ps_street(S, "lamp", crest - 3.8, tN, u"Lamp: lights the crest walk and the steps' head", side=1)
    # SW: the stream commons on the shelf, the garden raised above Q500 behind a stone wall
    ps_block_ring(S, s1, s1 + 0.40, shelf - 0.30, gf + 0.15, "stone")
    S.zone(u"Bank steps", u"sit or walk down to the bed", crest, -hw)
    S.zone(u"Stream commons", u"open ground the floods may cover", s0, s1)
    S.zone(u"Demeter's Garden", u"raised above Q500, stays dry", s1, S.u1)
    gy = lambda u: shelf + (b - shelf) * max(0.0, min(1.0, (s0 - u) / (s0 - hw)))
    S.zone(u"Wet edge", u"floods at Q100, holds the bank", hw, s0, "water")
    # planting (G9 groups): a mixed wet edge on the slope up to the commons (wet to drier, emergent only under the
    # water), the garden's trees, shrubs and herbs around the tomato rows, the café's plane a step behind (layer 1)
    ps_group(S, hw + 0.4, s0 - 0.3, gy, 0.0, 0.42, ["soft_rush", "loosestrife", "rush", "willow", "tamarisk"], 33,
             layers=(1, 0), why={"cleaning": u"clean the water", "shade": u"shade the edge"})
    rows = (s1 + 2.6, s1 + 7.0)
    S.put(sf_seat(pla_crop_rows("tomato", S.X(rows[0]), S.X(rows[1]), S.Y(gf), k, spacing=1.0, h_m=1.0,
                                crown_m=0.8), S.Y(gf)))
    S.call(u"Tomato rows: the garden's crop, above the flood", sum(rows) / 2.0, gf + 1.4, "zone")
    ps_group(S, s1 + 0.6, S.u1 - 0.3, lambda u: gf, 0.5, 0.95, {"plane": 0.6, "olive": 1.0, "chaste": 0.8,
                                                                "rosemary": 0.7, "lavender": 0.7}, 34,
             layers=(1, 0), avoid=[(rows[0] - 0.2, rows[1] + 0.2)],
             why={"shade": u"shade the café", "perception": u"seasonal colour"})
    ps_low(S, s1 + 0.6, rows[0] - 0.3, lambda u: gf, 38)       # v17: shrubs + flowers round the tomato rows
    ps_break(S, gf)                                             # v17 (1:250): the garden goes on to the cut end
    # people by zone: on the crest walk, sitting and walking on the bank steps, across on the stones, children and
    # families on the commons; a gardener at the tomato rows and a café guest (dry garden floor, hand-placed)
    ps_zones(S, [("walkway", crest - 3.6, crest - 0.3, tN),
                 ("sun_steps", crest + 1.6, -hw - 0.4, ps_stair_z(-hw, b, n, rise, tread, -1)),
                 ("water", -hw, ua, b), ("stepping_stones", ua, ub, ztop), ("water", ub, s0, gy)], 35, seat_h=rise,
             focus=S.st_c)
    ps_zones(S, [("lawn", s0 + 1.0, s1 - 1.0, shelf)], 37, density=1.4,
             focus=S.st_c)                                      # families playing, lying in the sun on the commons
    ps_zones(S, [("lawn", s0 + 1.0, s1 - 1.0, shelf)], 36, layer=1, density=0.6)
    ps_fig(S, "stand", s1 + 5.2, gf, facing=-1)                # at the tomato rows
    ps_fig(S, "sit_step", s1 + 8.6, gf, facing=-1)             # café in the garden (v17: inside the 50 m break)
    S.call(u"Café: guests in the garden's shade", s1 + 8.6, gf + 2.2, "zone")
    S.inset = (ua - 0.5, ub + 0.5, b - 0.5, b + 2.5, u"stepping stones over the summer strip")    # v17: 1:100


# ---------------------------------------------------------------- W4 downstream reach
def ps_sec_w4(S):
    """W4 downstream: the crest walk, bike lane and tree corridor on the NE embankment, a ramp on a berm to a viewing
    terrace above Q500, steps to a boardwalk that floods at Q100, the SW slope planted wet to dry, the field behind.
    v16: zones named under the drawing, the corridor on depth layers 2-1, a lamp and a bollard on the crest, fishing
    at the boardwalk's end, the strip on the survey low point, the inset on the boardwalk end."""
    c, b, hw, k = S.cid, S.bed, S.hw, S.k
    tN, aN = level(c, "top", "NE"), level(c, "angle_deg", "NE")
    tS, aS = level(c, "top", "SW"), level(c, "angle_deg", "SW")
    q1, q5 = level(c, "q100"), level(c, "q500")
    gN, gS = math.tan(math.radians(aN)), math.tan(math.radians(aS))
    cN, cS = -hw - (tN - b) / gN, hw + (tS - b) / gS            # crests (u)
    S.prof = [(S.u0, tN), (cN, tN)] + ps_bed_pts(S, -hw, hw) + [(cS, tS), (S.u1, tS)]
    ps_back(S, 41)
    zN = lambda u: b + (-hw - u) * gN                           # the NE slope's level at u
    zS = lambda u: b + (u - hw) * gS
    sh, _ = sct_bank("embankment", S.X(-hw), S.Y(tN), S.Y(b), -1, k, angle_deg=aN, reach_m=cN - S.u0,
                     depth_m=PS_DEPTH)
    S.put(sh)
    sh, _ = sct_bank("embankment", S.X(hw), S.Y(tS), S.Y(b), 1, k, angle_deg=aS, reach_m=S.u1 - cS,
                     depth_m=PS_DEPTH)
    S.put(sh)
    # NE crest: the tree corridor, the bike lane, the crest walk (G10)
    ps_lane(S, cN - 0.3, cN - 2.8, tN, "walk", (u"Crest walk", u"above Q500, beside the corridor"))
    ps_lane(S, cN - 3.2, cN - 5.2, tN, "bike", (u"Bike lane", u"along the crest, clear of the walk"))
    ps_street(S, "lamp", cN - 3.0, tN, u"Lamp: lights the crest walk and the bike lane", side=1)
    ps_street(S, "bollard", cN - 0.1, tN, u"Bollard: no vehicles on the ramp")
    # the ramp down the embankment on an earth berm to a viewing terrace above Q500, steps to the boardwalk
    tT = math.ceil((q5 + PS_FREEBOARD) * 20.0) / 20.0           # terrace floor: dry above Q500
    run = (tN - tT) / PS_RAMP
    uT = cN + run                                               # the ramp's foot = the terrace's landward edge
    uW = uT + PS_TERRACE_W                                      # the terrace's water edge
    dk = round((q1 - 0.40) * 20.0) / 20.0                       # boardwalk deck: floods at Q100 (design rule)
    ns = int(math.ceil((tT - dk) / PS_STAIR[1]))
    rs = (tT - dk) / ns
    ub = uW + ns * PS_STAIR[0]                                  # the boardwalk's landward edge
    ua = -hw + 1.6                                              # ... its end, over the bed's edge
    sa, sb, ztop = ps_bed(S, -hw, hw)
    ring = [(cN, tN), (uT, tT - 0.20), (uT, zN(uT))]            # the berm under the ramp
    S.put(sct_hatch_fill(S.P(ring), "earth", k, SCT["cut"], 0.25))
    sh, _, _ = sf_ramp(S.X(uT), S.Y(tT), run, tN - tT, k, side=-1, material="concrete", rail=True)
    S.put(sh)
    S.zone(u"Ramp", u"step-free from the crest to the terrace", cN, uT)
    S.put(sf_terrace(S.X(uT), S.Y(tT), PS_TERRACE_W, k, side=1, material="timber", rail=False))
    u = uT + 0.4
    while u < uW:                                               # the terrace's piles down into the bank
        S.pg.line(S.P([(u, tT - 0.25), (u, zN(u) - 0.6)]), PS_TIMBER, 0.35)
        u += 1.8
    S.zone(u"Viewing terrace", u"above Q500, looks over the water", uT, uW)
    sh, _ = sf_stairs(S.X(ub), S.Y(dk), ns, rs, PS_STAIR[0], k, side=-1, material="concrete", rail=True)
    S.put(sh)
    S.pg.poly([S.P([(ua, dk - 0.20), (ua, dk), (ub, dk), (ub, dk - 0.20)])], fill=PS_TIMBER, stroke=SCT["cut"],
              lw=0.25)
    u = ub + 0.3
    while u < ua - 0.3:                                         # piles down into the bank and the bed
        S.pg.line(S.P([(u, dk - 0.20), (u, min(zN(u), b) - 0.6)]), PS_TIMBER, 0.35)
        u += 2.0
    ps_rail(S, ua + 0.1, dk)
    S.zone(u"Boardwalk", u"steps down, floods at Q100, out over the wet edge", uW, ua)
    # planting (G9 groups): the crest corridor (trees and shrubs; v16 G15: layers 2-1, behind the people), a wet edge
    # under the terrace and boardwalk, the SW slope wet to dry; the field behind the SW crest takes the surplus water
    ps_group(S, S.u0 + 0.3, cN - 5.6, lambda u: tN, 0.45, 0.9,
             {"plane": 1.0, "ash": 0.5, "chaste": 1.0, "rosemary": 0.8, "olive": 0.6}, 42, layers=(2, 1),
             why={"shade": u"shade the crest"})
    S.call(u"Ecological corridor: trees and shrubs along the crest", (S.u0 + cN - 5.6) / 2.0, tN + 4.0, "plant",
           "plane")
    ps_group(S, uT + 0.3, -hw - 0.2, zN, 0.0, 0.16, ["soft_rush", "loosestrife", "rush"], 43,
             why={"cleaning": u"clean the water under the deck"})
    ps_group(S, hw + 0.3, cS - 0.6, zS, 0.0, 0.5, ["soft_rush", "loosestrife", "willow", "tamarisk", "chaste"], 44,
             layers=(1, 0), why={"shade": u"shade the slope", "cleaning": u"clean the water"})
    ps_low(S, S.u0 + 0.3, cN - 5.6, lambda u: tN, 48)            # v17: shrubs + flowers in front of the corridor
    ps_low(S, hw + 1.0, cS - 0.6, zS, 49, t0=0.3)               # v17: and on the bazaar side slope, wet to dry
    S.put(sf_seat(pla_crop_rows("cotton", S.X(cS + 1.0), S.X(S.u1 - 0.4), S.Y(tS), k, spacing=0.9, h_m=1.0,
                                crown_m=0.6), S.Y(tS)))
    S.zone(u"Cotton field", u"takes the surplus water", cS, S.u1)
    ps_break(S, tS)                                             # v17 (1:250): the field goes on to the cut end
    # people by zone: cycling, walking, running, a dog on the crest, down the ramp, sitting and standing on the
    # terrace, on the boardwalk and fishing at its end (water_edge: the line drops to the average-flow water), across
    # on the stones; more along the crest behind the cut (layer 1); a farmer in the field
    ps_zones(S, [("walkway", cN - 2.8, cN - 0.3, tN), ("bike_lane", cN - 5.2, cN - 3.2, tN),
                 ("walkway", cN + 1.0, uT - 1.0, lambda u: tN - (u - cN) * PS_RAMP),
                 ("walkway", ub - 0.3, ua - 2.2, dk), ("water_edge", ua - 2.0, ua - 0.1, dk),
                 ("water", -hw, sa, b), ("stepping_stones", sa, sb, ztop), ("water", sb, hw, b)], 45, focus=S.st_c)
    ps_zones(S, [("viewing_terrace", uT + 0.3, uW - 0.3, tT)], 47, density=1.5,
             focus=S.st_c)                                      # together at the view over the water
    ps_zones(S, [("walkway", cN - 2.8, cN - 0.3, tN)], 46, layer=1, density=0.6)
    ps_fig(S, "stand", S.u1 - 1.2, tS, facing=-1)
    S.inset = (ua - 3.5, ua + 0.6, dk - 1.0, dk + 2.2, u"fishing from the boardwalk's end")       # v17: 1:100


PS_DRAW = {"W1": ps_sec_w1, "W2": ps_sec_w2, "W3": ps_sec_w3, "W4": ps_sec_w4}


# ---------------------------------------------------------------- v17: numbers on the section, the zoom inset
# v17 (round 4, G-R4-5.5, G-R4-7, G-R4-2): every zone and element is ONE marker (marker.py mk_marker) on what it
# names, numbered in reading order; the side list (or W4's strip) repeats the numbers "*Name* · reason". The old
# callout key, zone strip, bank rows and bed dimension line under the drawing are gone (the "today" line says it).
PS_MK_R = 2.2                          # print mm: the room one marker takes (two digits at 7 pt + its rim, marker.py)
PS_MK_COL = {"zone": "8B3A3F", "water": "5D7F8D", "built": "4A3F35"}   # designed zone, water / bed, street element


def ps_mk_col(kind, key=None):
    """the marker colour = the colour of what it names (G-R4-7): a planting group takes its tallest species' fill"""
    if kind == "plant" and key:
        return pla_colours(key)["fill"]
    return PS_MK_COL.get(kind, PS_MK_COL["zone"])


def ps_marks(S):
    """the numbers of one section (section mm): a zone on its ground at its middle, an element (call) at its point;
    a number that touches another or the zoom inset moves up (then sideways) until it is clear and stays inside the
    section's width and height; numbered in reading order (tp_reading_order), one number per distinct text. Fills
    S.marks [(x, y, n, colour)] and S.list [(n, text, colour)]."""
    r = PS_MK_R
    bb = ps_bbox(S.pg.items)
    top = bb[3] - r
    busy = [S.inset_busy] if S.inset_busy else []
    ents = []
    for name, why, ua, ub, kind in S.zones:
        a, b = max(ua, S.u0), min(ub, S.u1)
        u = 0.5 * (a + b)
        ents.append((u"*%s* · %s" % (name, why), S.X(u), S.Y(ps_z_at(S.prof, u)) + r + 0.3, ps_mk_col(kind)))
    for t, u, z, kind, key in S.calls:
        nm, _s, why = t.partition(u": ")
        ents.append((u"*%s* · %s" % (nm, why) if why else u"*%s*" % nm, S.X(u), S.Y(z) + r, ps_mk_col(kind, key)))
    done, at = [], []
    step = 2.0 * r + 0.6

    def free(x, y):
        if any(math.hypot(p[0] - x, p[1] - y) < step for p in done):
            return False
        return not any(q[0] - r - 0.6 < x < q[2] + r + 0.6 and q[1] - r - 0.6 < y < q[3] + r + 0.6 for q in busy)
    for txt, x0, y0, col in ents:
        x0 = max(r, min(S.w - r, x0))
        spot = None
        for sx in (0, 1, -1, 2, -2, 3, -3, 4, -4):
            x = max(r, min(S.w - r, x0 + sx * step))
            y = y0
            while y <= top and not free(x, y):
                y += 0.5
            if y <= top:
                spot = (x, y)
                break
        if spot is None:
            tp_warn(u"p13 %s: no free spot for the number of %r inside the section: not drawn" % (S.cid, txt))
            continue                                             # v18.1: a warning, the run goes on
        done.append(spot)
        at.append((spot[0], spot[1], txt, col))
    num = {}
    S.marks, S.list = [], []
    for j in tp_reading_order([(x, y) for x, y, _t, _c in at], y_down=False, row_mm=3.0 * r):
        x, y, txt, col = at[j]
        if txt not in num:
            num[txt] = len(num) + 1
            S.list.append((num[txt], txt, col))
        S.marks.append((x, y, num[txt], col))


def ps_inset(S, log):
    """v19 (round 5, G-R5-5, change of approach): the inset is no longer the parent's shapes scaled up into its sky.
    The cut's main use spot S.inset (ua, ub, za, zb m, what) is framed with the section kit (sf_inset_frame: the
    action + 0.6 m margin, the largest listed inset scale >= 2 x the 1:500 parent) and kept in S.inset_fr; ps_items
    draws the section AGAIN at that scale's k (ps_section child=True), so stone courses, treads, boards and people
    show at their own detail, and exports it as its own drawing + an inset item (the booklet frames and places it)."""
    if not S.inset:
        return
    ua, ub, za, zb, what = S.inset
    S.inset_fr = sf_inset_frame([(min(ua, ub), min(za, zb), max(ua, ub), max(za, zb))], PS_SCALE, page=S.page,
                                label=u"%s %s" % (S.cid, what))
    if S.inset_fr:
        log.append(u"%s %s: inset (%s) 1:%d, window %.1f x %.1f m (drawn again at its own scale)" % (
            S.page, S.cid, what, S.inset_fr["den"], S.inset_fr["window"][2] - S.inset_fr["window"][0],
            S.inset_fr["window"][3] - S.inset_fr["window"][1]))


def ps_bridges(S, page):
    """v19 (D8, N4 a): the bridges this cut sees (common/bridges.py br_section, look -1: every W cut looks
    downstream); t = m along the cut from its first end (SW) -> u = d_SW - t. A bridge beyond the cut goes behind the
    cut land (after the sky and back layers, S.back_at), one cut through it over the water; behind the viewer: not
    drawn, logged (br_log_lines)."""
    if "br_section" not in globals():
        return
    dsw = S.d.get("SW")
    if dsw is None:
        return
    try:
        br = br_section(S.cid, X=lambda t: S.X(dsw - t), Y=S.Y, look=-1, t0=dsw - S.u1, t1=dsw - S.u0,
                        ground=lambda t: ps_z_at(S.prof, dsw - t), page=page)
    except Exception as ex:
        tp_warn(u"%s %s: bridges not drawn (%s: %s)" % (page, S.cid, type(ex).__name__, ex))
        return
    if br.get("background"):
        tmp = Page(0, 0)
        ps_put(tmp, br["background"])
        S.pg.items[S.back_at:S.back_at] = tmp.items
    if br.get("structures"):
        S.put(br["structures"])


def ps_finish(S, log, child=False):
    """the G6 check, the notes, (v19) the bridges, the inset frame, then the numbers (ps_marks); a child (inset
    redraw (a window of a few metres at the water, far from any bridge) gets none of them"""
    if child:
        return
    ps_bridges(S, S.page)
    for m_ in sf_assert_g6(S.k, trees=S.trees, strict=False):  # G6: people 1.75 m, trees in their sourced range
        log.append(u"G6 CHECK section %s (style %s): %s" % (S.cid, S.style, m_))
    for m_ in S.notes:
        log.append(u"NOTE section %s planting: %s" % (S.cid, m_))
    for m_ in S.info:
        log.append(u"section %s: %s" % (S.cid, m_))
    ps_inset(S, log)
    ps_marks(S)


def ps_section(cid, log, page, style="a", k=None, child=False):
    """one cut as a PsSec (its drawing in S.pg, print mm at S.k: 1:500 = PS_K, or an inset's k), in style a (the
    only style); v16: the surveyed bed first (ps_survey, DATA-1); page = the booklet page id; child=True: the inset
    redraw (its own log, no numbers, no inset of its own)"""
    u0, u1, d = ps_extent(cid)
    S = PsSec(cid, u0, u1, d, style, k=k)
    S.page = page
    ps_survey(S, next(k_ for k_, c_, _n, _m, _t in PS_CUTS if c_ == cid), log)
    PS_DRAW[cid](S)
    ps_finish(S, log, child)
    return S


# ---------------------------------------------------------------- v17: the words beside a section
PS_LIST_PT, PS_TODAY_PT, PS_TITLE_PT, PS_SCEN_PT = 7.0, 6.5, 10.0, 8.0   # pt: list, "today" line, title, scenario
PS_LEAD = 1.3                          # line spacing / size
PS_LIST_ROW = 3.7                      # print mm: least step between two list entries (a two-digit marker + 0.6 mm)


def ps_lead(pt):
    return pt * PT * PS_LEAD


def ps_bank_short(c, side):
    """a bank as the level table has it, short"""
    kind = ps_kind(c, side)
    h = level(c, "height", side) or level_depth(c, side)
    if kind == "dsi_wall":
        return u"DSİ stone wall %.2f m" % h
    if kind == "embankment":
        return u"embankment %.1f° · %.2f m" % (level(c, "angle_deg", side), h)
    if kind == "loose_earth":
        return u"loose earth bank %.2f m" % h
    return u"no crest, the ground keeps rising"


def ps_today(S):
    """v17 (G-R4-2): the one "today" line: both banks and the bed width from the level table, by place name"""
    c = S.cid
    return u"*Today* · %s: %s · %s: %s" % (                    # v19 (G-R5-4.6): no bed width
        place_name("side_NE"), ps_bank_short(c, "NE"), place_name("side_SW"), ps_bank_short(c, "SW"))


def ps_note(cid):
    """the key line of a section, from the level table"""
    q5 = level(cid, "q500")
    if cid == "W1":
        return u"Q500 %s stays *%.2f m* under the DSİ walls · reeds only in lined basins the flood passes by" % (
            ps_lv(q5), level(cid, "top", "SW") - q5)
    if cid == "W2":
        return u"Q500 %s stays *%.2f m* under the hub square · the steps flood, the square stays dry" % (
            ps_lv(q5), level(cid, "top", "SW") - q5)
    if cid == "W3":
        return u"Q500 %s · garden floor *%s* stays dry: olive and lavender need soil that never waterlogs" % (
            ps_lv(q5), ps_lv(math.ceil((q5 + PS_FREEBOARD) * 20.0) / 20.0))
    return u"Q500 %s stays *%.2f m* under the %s bank top · wet edge, boardwalk and trees by flood level" % (
        ps_lv(q5), level(cid, "top", "NE") - q5, place_name("side_NE"))

# ================================================================ v19 key map: this page's four cuts (G-R5-3, D3, S2 module v2)
# v19 (round 5): the one merged page p13 (D9) gets ONE key map from common/keymap.py km_map v2: no scale_den, so the
# module fits its frame to the map, turns it so the corridor runs along the long side and puts its own true-north
# arrow; only W1-W4 (red R01, triangles pointing downstream: every W section looks downstream); names through the
# names table. The script draws nothing of it: km_items() hands the drawing, its labels and the keymap item to
# items.json and the booklet places it in the right column (never over a drawing, no scale bar). The v17 page-drawn
# map (own clip, own north arrow, neatline, TextPage) is gone.
PS_KM_PAD = 120.0                     # m round the page's cut ends in the map window (drawing rule: streets around)
PS_KM_SPACE = (113.6, 90.0)           # print mm: the MOST room offered (right column 113.6 mm, PLAN §3); the module
#                                       returns the fitted, smaller frame


def ps_keymap_items(ix, page, cids, log):
    """the page's key map as items (S2 km_items) added to ix; returns the drawing id or None (WARNING)"""
    ends = [p for c in cids for p in level_ends(c)]
    bx = (min(p[0] for p in ends) - PS_KM_PAD, min(p[1] for p in ends) - PS_KM_PAD,
          max(p[0] for p in ends) + PS_KM_PAD, max(p[1] for p in ends) + PS_KM_PAD)
    try:
        km = km_map(list(cids), PS_KM_SPACE[0], PS_KM_SPACE[1], page=page, looks=dict((c, -1) for c in cids),
                    box=bx, log=log)
        its = km_items(km, page, item_id=u"ps_keymap_%s" % page, priority=3)
    except Exception as ex:
        ix.warn(page, "keymap", u"key map not made (%s: %s)" % (type(ex).__name__, ex))
        return None
    for it in its:                                   # the module's schema dicts go in as they are (ids registered)
        it["id"] = ix._id(it["id"], it.get("kind", "item"))
        if it.get("anchor") and it["anchor"].get("drawing"):
            it["anchor"]["drawing"] = its[0]["id"]
        if it.get("kind") == "keymap":
            it["drawing"] = its[0]["id"]
        ix._put(page, it)
    for m_ in km.get("missing") or []:
        log.append(u"FLAG %s key map: %s not drawn" % (page, m_))
    log.append(u"%s key map: %s, frame %.0f x %.0f mm (fitted), turned %s deg" % (
        page, u" + ".join(cids), km.get("w_mm", 0.0), km.get("h_mm", 0.0), km.get("rotation_deg")))
    return its[0]["id"]

# ================================================================ v19 booklet items (round 5, G-R5-12: produce, the booklet composes)
# Aras 1 Nov 22:00 / addendum 22:37: the script lays out no page and writes no sheet PDF. W1-W4 go to ONE booklet page
# (D9, page id "p13" = p13-14 merged; N3 a: 1:500), each cut = one true-scale drawing in metres (x = u across the
# stream from the cut axis, NE negative / left, y = level m a.s.l.; PLAN §4), its numbers as badges on what they name,
# its numbered list, its level column (the booklet draws the U04 markers), its zoom inset as its own drawing drawn
# again at the inset scale (G-R5-5), plus one key map (S2 module), one material legend, the page title and intro, the
# sources. Everything lands in Downloads/Bergama/cached/booklet/bergama_proposal_sections/items.json.
PS_PAGE = "p13"                                       # D9: p13 + p14 one page (same id in the 23-page numbering)
BK_SOURCES = [("rhs_lavender", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter)",
               u"https://www.rhs.org.uk/Advice/profile?pid=127"),
              ("ecocrop_olive", u"FAO Ecocrop, Olea europaea (will not tolerate waterlogged soils)",
               u"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1553"),
              ("icomos_2014", u"ICOMOS 2014, Evaluation No 1457, Pergamon and its Multi-Layered Cultural Landscape",
               u"https://whc.unesco.org/document/152724")]


def ps_legend_entries():
    """the material key (solid colours, G-R5-4.1) of what the sections draw, as Ix legend entries"""
    P = _wat_pal()
    return [(dict(kind="fill", colour=P["sec"]), u"water at the average yearly flow"),
            (dict(kind="dash", colour=P["q100"], width_pt=0.85, dash_pt=[3.4, 1.7]), u"Q100 flood level"),
            (dict(kind="dash", colour=P["q500"], width_pt=0.85, dash_pt=[1.1, 1.4]), u"Q500 flood level"),
            (dict(kind="fill", colour=SCT["stone"]), u"stone: DSİ walls, steps, garden wall"),
            (dict(kind="fill", colour=SCT["concrete"]), u"concrete: stairs, ramp, basins"),
            (dict(kind="fill", colour=SCT["earth"]), u"earth"),
            (dict(kind="fill", colour=SCT["gravel"]), u"gravel bed"),
            (dict(kind="fill", colour=PS_TIMBER), u"timber: terrace, boardwalk"),
            (dict(kind="fill", colour=SF_LANE["walk"]), u"walk paving"),
            (dict(kind="fill", colour=SF_LANE["bike"]), u"bike lane")]


def _ps_ibox(it):
    """an item's box (print mm) or None"""
    if it[0] == "image":
        return (it[1], it[2], it[1] + it[3], it[2] + it[4])
    if it[0] == "circle":
        return (it[1] - it[3], it[2] - it[3], it[1] + it[3], it[2] + it[3])
    if it[0] == "text":
        return (it[2], it[3], it[2], it[3])
    pts = [p for R in it[1] for p in R] if it[0] == "poly" else list(it[1])
    if not pts:
        return None
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def ps_drawing(ix, S, did, page, scale_pref, group, priority, window=None, title=None):
    """S's items (print mm at S.k) as one true-scale drawing in metres: x = S.u0 + x_mm / S.k, y = S.z0 + y_mm / S.k;
    window (m) = an inset's extent: only items that reach into it go in (the booklet clips at the extent)"""
    k = 1.0 / S.k
    if window:
        ext = window
        wx = [(v - o) * S.k for v, o in zip(window, (S.u0, S.z0, S.u0, S.z0))]
        items = []
        for it in S.pg.items:
            b = _ps_ibox(it)
            if b is None or (b[0] <= wx[2] and b[2] >= wx[0] and b[1] <= wx[3] and b[3] >= wx[1]):
                items.append(it)
    else:
        bb = ps_bbox(S.pg.items)
        ext = (S.u0 + min(0.0, bb[0]) * k, S.z0 + min(0.0, bb[1]) * k, S.u0 + max(S.w, bb[2]) * k, S.z0 + bb[3] * k)
        items = S.pg.items
    D = ix.drawing(did, page, ext, scale_pref=scale_pref, dkind="section", group=group, priority=priority,
                   title=title)
    ix.layer(D, "section", items, k=k, origin=(S.u0, S.z0))
    return D


def ps_items(ix, log):
    """v19: the whole p13 export (see the notes above)"""
    page = PS_PAGE
    ix.text(page, u"The proposals in section", "title", priority=1, id="ps_title")
    ix.text(page, u"Four cuts W1-W4, upstream to downstream, each looking downstream · %s left, %s right" % (
        place_name("side_NE"), place_name("side_SW")), "intro", priority=2, id="ps_intro")
    cids = []
    for i, (key, cid, num, name, take) in enumerate(PS_CUTS):
        S = ps_section(cid, log, page, "a")
        cids.append(cid)
        g = u"ps_%s" % cid
        D = ps_drawing(ix, S, g, page, [PS_SCALE], g, i + 1, title=u"%s · %s" % (cid, name))
        ix.text(page, u"%s · %s" % (cid, name), "heading", priority=i + 1, group=g, id=g + "_head")
        ix.text(page, take, "note", priority=i + 1, group=g, id=g + "_scenario")
        ix.text(page, ps_note(cid), "note", priority=i + 1, group=g, id=g + "_levels_note")   # P13.2 water levels
        # the numbers on what they name (badges at the marker, G-R4-5.5) and the list beside "Name · reason"
        disc = []
        for x, y, n, col in S.marks:
            sh, _b, _r = mk_marker(x, y, n, col, PS_LIST_PT)
            disc += [s_ for s_ in sh if s_[0] != "text"]
            for s_ in sh:
                if s_[0] == "text":
                    ix.text(page, s_[1], "badge", drawing=D["id"], at=(S.u0 + s_[2] / S.k, S.z0 + s_[3] / S.k),
                            size_pt=PS_LIST_PT, bold=True, colour=s_[5], positions=["=L"], side_list_ok=False,
                            priority=i + 1, group=g)
        ix.layer(D, "numbers", disc, k=1.0 / S.k, origin=(S.u0, S.z0))
        if S.list:
            ix.list(page, D["id"], [t for _n, t, _c in S.list], numbered=True, id=g + "_list", group=g)
        sf_level_items(ix, page, D, [("q500", level(cid, "q500")), ("q100", level(cid, "q100")),
                                     ("avg", level_avg_flow(cid)), ("bed", S.bed)])
        # the zoom inset: the section drawn again at the inset scale (G-R5-5), framed on the action
        fr = S.inset_fr
        if fr:
            C = ps_section(cid, [], page, "a", k=fr["k"], child=True)
            cd = ps_drawing(ix, C, g + "_inset", page, [fr["den"]], g, i + 1, window=fr["window"],
                            title=u"%s · %s" % (cid, S.inset[4]))
            ix.inset(page, D["id"], fr["window"], cd["id"], fr["factor"], id=g + "_inset_item")
            ix.text(page, S.inset[4], "caption", priority=i + 1, group=g, id=g + "_inset_caption")
            kk = 1.0 / S.k
            sf_inset_cut_check(fr["window"], [(u"plant/element %d" % j_, (S.u0 + o[0] * kk, S.z0 + o[1] * kk,
                                                                          S.u0 + o[2] * kk, S.z0 + o[3] * kk))
                                              for j_, o in enumerate(S.obst) if (o[4] if len(o) > 4 else 0) == 0],
                               page=page, label=u"%s %s" % (cid, S.inset[4]))
        else:
            ix.warn(page, "inset", u"%s: no inset spot set: no zoom inset (never skipped silently, C5)" % cid)
        log.append(u"%s %s: drawing %.0f x %.0f m at 1:%d, %d numbers, inset %s" % (
            page, cid, D["extent"][2] - D["extent"][0], D["extent"][3] - D["extent"][1], PS_SCALE, len(S.list),
            (u"1:%d" % fr["den"]) if fr else u"none"))
    ix.legend(page, None, ps_legend_entries(), title=u"Materials", id="ps_legend", group="ps_legend")
    ps_keymap_items(ix, page, cids, log)
    for k_, t_, u_ in BK_SOURCES:
        ix.source(k_, t_, u_, page=page)
    for k_, t_ in ps_sources():
        ix.source(k_, t_, None, page=page)
    return ix


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
    log.append(cut_log_line())
    log.append(u"trigger: " + (TRIG_WHY[0] or u"-"))     # what started this run
    log += [fig_set_line(), sf_g14_line()]                # v19 (A17): the plant lines once (sec_look_lines has them)
    log += sec_look_lines() + wat_flag_lines()
    log.append(u"insets: each drawn again at its own scale, so the figure / plant / people counts above include them")
    if pal is None:
        log.append(u"palette: built-in colours (no bergama_palette.py in Downloads/Bergama/Data)")
    head = [u"%s %s · %s · %.1f s" % (GH_LABEL, VERSION, time.strftime("%H:%M"), time.time() - t0),
            u"Items: %s (no sheet PDF: the booklet composes p13)" % path]
    return u"\n".join(wn_compose(tp_log_lines() + [x for x in log if x], head=head))


# ---- trigger.py (round 4, S1, 1 Nov 2026; BRIEF §6, round 3 open row 13): ONE start-up / trigger file ----------------
# Replaces common/chain_fire.py, gh_in_items.py, _gh_inputs.py, to_bool.py and the scripts' own copies of chain_fire,
# upstream_done, button_state, find_button, _button_value and BUTTON_WORDS (each page session removes its copy and
# calls trig_should_run; the closing step deletes the four old files once nothing includes them).
#
# WHAT STARTS A COMPONENT (the same for all nine scripts; RUN_GUIDE quotes this):
#   1. A press of its Button: the input named run (or bake / build / go / press / button / start, any case), else the
#      input a Button is wired into. Only the press starts it (the rising edge: False -> True); holding the Button
#      or re-solving while it is True does not start it again.
#   2. A NEW "done ..." text arriving on any of its own inputs from the script before it in the chain (one-click
#      chain). The first solve after the component is pasted, opened or rewired only NOTES the text already on the
#      wire, so pasting code or rewiring never starts a run (Aras 1 Nov 08:04); when the wire brings nothing, the done
#      text the upstream component left in Rhino's memory is read (Null on the wire).
#   Nothing else starts it: settings written in the script (PHOTO_ANY_LICENCE = True ...) and old globals that
#   Rhino 8 keeps between solves are never read as a press (Aras 1 Nov 08:24); only the component's own inputs are.
#
#   trig_inputs() -> {name: value}         the component's own inputs only (VariableName / NickName / Name), never
#                                          the script's globals; {} outside Grasshopper
#   trig_get(name, default=None)           one own input by name in any case; a list gives its first non-None item
#   to_bool(v, default=False)              True / "true" / "yes" / "1" / "on" / non-zero; a list = any item true
#   upstream_done(name) -> str | None      the "done ..." text the component wired into input `name` left in memory
#   chain_fire(v, key, name=None) -> bool  a NEW done text on v (a list gives its first "done ..." item) fires once;
#                                          the first solve per component + wiring only notes it
#   trig_button(settings=()) -> name|None  the Button input (see 1. above); never a name in settings (inputs that
#                                          carry options, e.g. the masterplan's SETTINGS), never one starting with "_"
#   trig_should_run(key="chain_seen", settings=()) -> (run, why, button)
#                                          run: bool; why: "button <name>" | "chain <input>" | None; button: its name
#                                          or None. Each script logs "trigger: <why>" in its run log.
#
# ROUND 5 (S1, 1 Nov 2026; C2, CHK-13: an output folder appeared when Aras only OPENED the GH file, 16:29): every
# memory above (the first-solve note, the last done text seen, the Button's last state) is now kept per OPEN
# DOCUMENT (trig_doc_key: the GH document's runtime id, else its object hash), not per Rhino session. Before, the
# notes of an earlier opening survived in Rhino's sticky, so the first solve after a reopen was not "first" and a
# done text still on a wire (or a Toggle left True: prev False -> True) started a run. Now the first solve after any
# open, paste or rewire only NOTES the wire and the Button state; only a later change starts a run.
# CHANGED APPROACH (Aras 1 Nov 22:46: "if you struggle with an aspect over and over, change your approach"): the chain
# no longer trusts memory notes alone. A chain start exists ONLY after a Button press in THIS open document
# (trig_mark_chain stores (time, document id)); chain_fire fires a component only when such a press exists and its
# done text is newer than the last one it saw. Opening a file, pasting, rewiring or a Toggle left True can never start
# a chain: without a press in this load, every done text on a wire is only noted.
#   trig_doc_key() -> str                  the open GH document's per-load id ("" outside Grasshopper)
#   trig_mark_chain(why)                   a Button run notes the chain start time (sticky "bergama_chain_t0", read by
#                                          bergama_paths.bg_this_run); trig_should_run calls it
TRIGGER_BUTTON_WORDS = ("run", "bake", "build", "go", "press", "button", "start")


def trig_doc_key():
    """the open Grasshopper document's id for THIS load: GH_Document.RuntimeID (new each time a file is opened in a
    Rhino session), else the document object's hash; "" outside Grasshopper"""
    try:
        d_ = ghenv.Component.OnPingDocument()                              # noqa: F821
    except Exception:
        return ""
    if d_ is None:
        return ""
    for a_ in ("RuntimeID", "RuntimeId"):
        try:
            v_ = getattr(d_, a_)
            if v_ is not None:
                return "doc%s" % v_
        except Exception:
            pass
    try:
        return "doch%s" % d_.GetHashCode()
    except Exception:
        return "docp%s" % id(d_)


def trig_mark_chain(why):
    """a run started by a Button press is the start of a chain run: its time goes to sticky "bergama_chain_t0" so
    readers can tell this run's files from older ones (bergama_paths.bg_this_run)"""
    if not why or not str(why).startswith("button"):
        return
    try:
        import scriptcontext as _scx
        import time as _t
        _scx.sticky["bergama_chain_t0"] = _t.time()
        _scx.sticky["bergama_chain_doc"] = trig_doc_key()
    except Exception:
        pass


def trig_chain_live():
    """True when a Button press started a chain in THIS open document (see CHANGED APPROACH above)"""
    try:
        import scriptcontext as _scx
        return (_scx.sticky.get("bergama_chain_t0") is not None and
                _scx.sticky.get("bergama_chain_doc") == trig_doc_key())
    except Exception:
        return False


def trig_inputs():
    """{name: value} of this component's own inputs (globals holding them), nothing else"""
    g_ = globals()
    out = {}
    try:
        for p_ in ghenv.Component.Params.Input:                            # noqa: F821 (Grasshopper)
            for a_ in ("VariableName", "NickName", "Name"):
                n_ = getattr(p_, a_, None)
                if n_ and str(n_) in g_:
                    out[str(n_)] = g_[str(n_)]
                    break
    except Exception:
        return {}
    return out


def trig_get(name, default=None):
    """an own input by name, any case; a list gives its first non-None item; empty text = default"""
    for k_, v_ in trig_inputs().items():
        if k_.lower() == str(name).lower():
            if isinstance(v_, (list, tuple)):
                v_ = next((x for x in v_ if x is not None), None)
            return default if v_ is None or (isinstance(v_, str) and not v_.strip()) else v_
    return default


def to_bool(v, default=False):
    if v is None:
        return default
    if isinstance(v, (list, tuple)):
        return any(to_bool(x) for x in v)
    if isinstance(v, bool):
        return v
    if isinstance(v, (int, float)):
        return v != 0
    s = str(v).strip().lower()
    if not s:
        return default
    return s in ("true", "yes", "1", "on")


def upstream_done(name):
    """the done text of the component wired into input `name`, read from Rhino's memory (sticky) when the wire brings
    Null. Keys: "done:<guid>", "lu_done:<guid>" or "...<guid>_done" (template scripts)."""
    try:
        import scriptcontext as _scx
        for p_ in ghenv.Component.Params.Input:                            # noqa: F821
            if str(p_.NickName or p_.Name).lower() != str(name).lower():
                continue
            for src_ in p_.Sources:
                g = str(src_.Attributes.GetTopLevel.DocObject.InstanceGuid)
                for k_ in ("done:" + g, "lu_done:" + g):
                    v_ = _scx.sticky.get(k_)
                    if str(v_).startswith("done "):
                        return str(v_)
                for k_, v_ in list(_scx.sticky.items()):
                    if str(k_).endswith(g + "_done") and str(v_).startswith("done "):
                        return str(v_)
    except Exception:
        pass
    return None


def _chain_wiring():
    """the sources wired into this component (their ids, sorted): rewiring starts a new chain memory"""
    try:
        return ",".join(sorted(str(s_.Attributes.GetTopLevel.DocObject.InstanceGuid)          # noqa: F821
                               for p_ in ghenv.Component.Params.Input for s_ in p_.Sources))   # noqa: F821
    except Exception:
        return ""


def chain_fire(v, key, name=None):
    """True once for each NEW "done ..." text on v (see the module notes)"""
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if str(x).startswith("done ")), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done ") and name:
        s = upstream_done(name) or ""
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid) + ":" + _chain_wiring() + ":" + trig_doc_key()  # noqa
        except Exception:
            pass
        # the first solve with this wiring (pasted, rewired or newly opened component) only notes what is on the
        # wire; "first" is tied to this solve's token (_CHAIN_SOLVE, made anew each time the script body runs), not
        # to a global, because Rhino 8 keeps a script's globals between solves
        tok = globals().get("_CHAIN_SOLVE")
        if _scx.sticky.get(key + ":init") is None:
            _scx.sticky[key + ":init"] = tok
        first = _scx.sticky.get(key + ":init") is tok
        if not s.startswith("done "):
            return False
        if first or _scx.sticky.get(key) == s or not trig_chain_live():
            _scx.sticky[key] = s
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def trig_button(settings=()):
    """the Button input's name, or None"""
    ins = trig_inputs()
    skip = set(str(n).lower() for n in settings or ())

    def ok(n):
        return n and not n.startswith("_") and n.lower() not in skip
    for k_ in ins:
        if ok(k_) and "".join(c for c in k_.lower() if c.isalpha()) in TRIGGER_BUTTON_WORDS:
            return k_
    try:
        for p_ in ghenv.Component.Params.Input:                            # noqa: F821
            nm = str(p_.NickName or p_.Name)
            if not ok(nm):
                continue
            for src_ in p_.Sources:
                if "button" in type(src_.Attributes.GetTopLevel.DocObject).__name__.lower():
                    return nm
    except Exception:
        pass
    return None


def trig_should_run(key="chain_seen", settings=()):
    """(run, why, button): does this solve start the script? (see the module notes)"""
    btn = trig_button(settings)
    ins = trig_inputs()
    try:
        import scriptcontext as _scx
        try:
            gk = str(ghenv.Component.InstanceGuid)                          # noqa: F821
        except Exception:
            gk = ""
        pk = "trig_prev:" + key + ":" + gk + ":" + trig_doc_key()
        on = to_bool(trig_get(btn)) if btn else False
        prev = _scx.sticky.get(pk)
        if prev is None:              # round 5 (C2): the first solve of this document only notes the Button's state
            prev = on
        prev = bool(prev)
        _scx.sticky[pk] = on
    except Exception:
        on, prev = (to_bool(trig_get(btn)) if btn else False), False
    if on and not prev:
        trig_mark_chain(u"button")
        return True, u"button " + btn, btn
    # the chain: the button input first (the board family wires the done text there), then every other own input
    skip = set(str(x).lower() for x in settings or ())
    names = ([btn] if btn else []) + [n for n in ins if n != btn and not n.startswith("_") and n.lower() not in skip]
    fired = None
    for n in names:
        v = ins.get(n)
        if v is None or isinstance(v, (bool, int, float)) or (isinstance(v, (list, tuple)) and not any(
                isinstance(x, str) for x in v)):
            if n != btn:
                continue
        if chain_fire(v, key + ":" + n, n) and fired is None:
            fired = n
    if fired:
        return True, u"chain " + fired, btn
    return False, None, btn


_CHAIN_SOLVE = object()     # a new token every time the script body runs (one per solve)
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
