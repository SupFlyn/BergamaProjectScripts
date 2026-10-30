# -*- coding: utf-8 -*-
# r: pymupdf==1.26.5
"""Bergama Group 6: A3 BOOKLET ASSEMBLER (26 Oct 2026). Rules: scripts/_template/SCRIPT_STANDARD.md §8.
Builds ONE multi-page landscape A3 PDF (420 x 297 mm) from the scripts' OWN sheet PDFs.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file. The first run installs PyMuPDF 1.26.5 (the
"# r:" line above; needs internet once).
  input  run   Button
  output log   the last run's report: pages, missing drawings, the word size each page prints at
  output done  "done HH:MM:SS.ss · N s" (for the one-click chain: wire the last script's done into run)
Reads  ~/Downloads/Bergama/output/<script folder>/booklet/blocks.json (the panels of each sheet) + the sheet PDFs
Writes ~/Downloads/Bergama/output/bergama_booklet/Bergama_booklet_A3_alt_a.pdf and ..._alt_b.pdf (revision 30 Oct:
  D1/D5 a and b; each crop's _a / _b version where its script wrote one)
NEW IN v21 (Aras 30 Oct 06:20, a feature change): the Sources page lists every asset source once under its own
  ASSETS heading (high-res silhouettes from Data/assets_hires.json, the A1 scale figure sets); no source note beside
  a drawing.
NEW IN v20.1 (bugfix, T5 fix pass 29 Oct): "inferred" joins the status words the sources page never prints.
NEW IN v20 (revision 29 Oct, WO-T5-1; a feature change, so the next whole number):
  * Page list of the revision (data/PLAN.py): p.02 side column = plan 01's key, the edge from above, the readings;
    p.04-05, p.14-15 and p.21 carry their key maps inside their crops (D11: each shows only its page's cuts), no key
    band; p.06 holds the old p.22 filter (D1 a); movement on three pages (D8 b): how people use it, the framework +
    who the project brings + street sections before/after (D3 b), the spine hub by hub; p.17 on two pages, the plant
    ladder page gone (D9 a); masterplan at 1:5,000, the water edge plans with their sections at 1:1,000.
  * Sources page public only (D13, Aras 29 Oct 18:56): a source text prints only the parts that name a public source;
    our survey, readings and calculations get no line; "assumed / interpolated / calculated / estimated" never print;
    a mark with no entry is taken off its page (logged); the site board's p.21 sources and every Commons photo credit
    are listed (blocks.json "sources", PLAN ALWAYS_KEYS); own site photos carry no credit.
  * One figure, one value (G10) also checks the olive area (ha). The pp.07-08 ALT page and the filter page switch
    (MERGE_21_22) are gone with the pages they joined.
NEW IN v19 (MIRAQUA 28 Oct, booklet revision v4; a feature change, so the next whole number):
  * G1 footer without the project and course lines (legend from column 1); G2 every word the booklet adds to a crop
    in the embedded Arial; G9 each crop shows its own stripped copy of its sheet page (words, images and line art
    outside it removed, 0.5 mm margin; G9_LINE_ART = False turns the line-art pass off).
  * G10 one figure, one value: a figure printed two ways is logged. N1 pages renumbered, cross-references checked by
    theme and title, references by number logged.
  * P04.1 / P14.1 section and heritage key maps at 1:1 in a band under the title; the rows make room.
  * N2 sources page: photo credits, the OSM footprints note, Corn (Mısır), the masterplan's place sources (its
    plan_sources), the senses sheet. F5 sources that are not public online removed with their marks (F5_DROP); the
    log lists the figures left without one.
  * D1 "Open ground and where we can build" is one page (MERGE_21_22); S1 new senses page after the S4 cut; p.02 edge
    types, p.07 notes beside the maps, p.09 index change, p.20 key map; no spreads.
  * P78.ALT pp.07 and 08 on one page as a separate PDF (Bergama_booklet_A3_ALT_p07-08.pdf) when legible, otherwise
    the log says why.
NEW IN v18 (Aras 27 Oct 17:35, Prompt 8 "final check of every page"): one source numbering for the whole booklet: the
[n] marks are renumbered in page order (first use first, one number per source text), the sources page lists only what
the pages cite, grouped by theme, and the log names marks without a source entry; the words of a sheet that no page
shows are taken out of it (the hidden stray "1:1,511" of the old p.10, junk in Illustrator); a whole-sheet page gets
the booklet's page number (and its theme where the corner is free); sheet pages are titled in the contents as the
sheets print them; a page whose drawings are all still frames ("later prompt") is left out (PLAN FRAME_PAGES); a
legend too long for the footer goes in columns under the rows when they leave room; two or more rows that leave more
than 40 mm of the page empty share that height out (above, between and below them).
NEW IN v17 (Aras 27 Oct 17:35, Prompt 7 "masterplan"; masterplan v26, site board v49): theme E is the open ground
(crop mp_max_area, now 1:5,000), then one spread: "Before the masterplan: the edge and where we can build" (site board
crop drw_edge_build_e) on the left page, "Masterplan: an ecological corridor" (crop mp_plan: both halves, the notes as
callouts beside them) on the right; all three the whole site frame at 1:5,000, drawn for the page at 1:1. "Why each
place" is gone. A page marked flex goes after the spread that follows it when that spread would open on a right page
(the log says so).
NEW IN v16 (Aras 27 Oct 20:51 "Move the line"; site board v48): the S4 pages ("Four seasons on one cut", "The S4 cut,
north-east bank") get the key map of the sections pages in their title band, S4 alone in ink (site board crop
sec_sections_key_s4): the board's S4 is now the water board's S4. Without that crop the page is built as before and
the log says "key map left out". Prompt 6 (water balance v4, water board v3.1, agriculture v3) needs nothing else here.
NEW IN v15 (Aras 27 Oct 17:34, Prompt 5 "water, part 2"; water board v3, site board v47, agriculture v2): a crop drawn
for its width on the booklet page (block "bk_w") keeps that size in a row too (it was shrunk with the page's one
scale, and a crop with a scale then fell to the next round scale, half size: p.22's plants printed at 1:500 in a
corner); the other crops of the page share what it leaves. p.20, p.21 and p.22's plants panel are such crops (water
board v3, 1:1 on A3). p.22 "Which plant goes where": the plants over the site board's July shade strip (crop
drw_shade_strip, hours of shade along the reach; the tree-cover chart where the board has not made it yet, a plan
key "a||b" = the first of these the scripts have written).
NEW IN v14 (Aras 27 Oct 17:34, Prompt 4 "water, part 1"; water balance v3, water board v2): "How the stream behaves"
is no longer its own page: the water balance sheet (v3) opens with it in a band beside its title, so the page reads
analysis first, then what we got (stage "Analysis, what we got"); "Collect, clean, hold" keeps its crop (the water board
v2 drops the tiles without data). One page fewer from p.12 on.
NEW IN v13 (Aras 27 Oct 17:34, Prompt 3 "movement and the city"; site board v46, city link v2): p.8 "How people use
it" stacks its three maps (the plan, walking today, driving today), each the whole site frame at 1:10,000 with its
scale bar and north arrow under it; p.10 and p.23 take the board's redrawn maps at the same scale (same crops).
NEW IN v12 (Aras 27 Oct 17:34, Prompt 2 "site and stream edge"; site board v45): p.2 "What is there" = plan 01 with the
site readings (bank bars and land-use ring, crop drw_site_readings) as a side panel at the right margin, top-aligned,
the plan's legend in two columns under it on the panel's own grid; p.6 "The stream edge and where we can build" (crop
drw_edge_build at 1:5,000, replaces the edge plan and the photo strip); each sections page has its key map (crop
sec_sections_key_n, 1:50,000) in the title band at the right; a drawing designed at a round booklet scale keeps it
when its sheet scale is rounded (a 0.05 % tolerance; it could print at the next scale, half size).
NEW IN v11 (Aras 27 Oct 17:27, Prompt 1: structure only): pages run in theme cycles A site and stream edge,
B movement and the city, C water, D history and heritage, E masterplan as the synthesis; each theme runs analysis ->
what we got -> what we do with it, named in every page's kicker, the footer and the contents. Merges set up as frames:
old p2 + p4, p5 + p6 one page each; the heritage loop on its own page in D; the masterplan halves + open ground + new
edge diagram + the notes as a two-page spread (left page even). A drawing a later prompt makes is a labelled frame.
NEW IN v10.1 (bugfix, 27 Oct 16:04): page "Why each place" after the masterplan halves, when masterplan v24.1 writes
the notes its key columns had no room for (crop mp_notes); the text under the component shows a newly pasted version
at once, idle.
NEW IN v9 (Aras 27 Oct 06:20 "pair them anyway"): the four proposal sections always share pages two at a time.
NEW IN v8 (Aras 26 Oct 08:27-08:28, on the v7 build): the two masterplan halves share one page, side by side, each at
its own round scale; "Long section along the spine" is left out (it repeated the "What is there" map); water board
v1.13 (larger storage figures).
NEW IN v7 (deck review 26 Oct 07:06, last pass R7; site board v43, water board v1.12, masterplan v23, city link
v1.10, proposal sections v6, agriculture v1.5): no half-empty pages: two drawings planned together share one page
when both fit at no less than 3/4 of the size each gets alone, else each keeps its own page (the four proposal
sections); a sheet's own title words it marks as not for the booklet (" · form A") are taken out of its crop, its
source marks [n] stay (the sources page lists them); more air between a caption and the next row; where several sheet
PDFs match a name, the newest file is used (an old version left in the folder is never picked).
NEW IN v6 (deck review 26 Oct 07:06, water board v1.12): the water board's panels are each laid out as one A3 page;
"Four seasons on one cut" is one crop (wb_s4_seasons, the four rows at 1:250); planting bands and species share one
page (the species list was a half-empty page of its own).
NEW IN v5 (Aras's deck review 26 Oct 07:06, site board v42): "The stream edge" page adds the plan of what meets the
water (drw_edge_plan) between the tree cover and the photos; "Sections across the stream" shows ALL the board's cuts
(S1-S8) at one round scale on at most two pages (sec_sections_1, sec_sections_2), not S1-S5 one by one.
NEW IN v4 (Aras 26 Oct 06:35, lasting rules): one drawing is never divided over two pages (each panel goes on its
page whole, and "what is there" appears once); every printed scale is a round number (1:1,000, 1:2,500, 1:5,000,
1:10,000 ...): the page takes the largest round scale at which everything fits, and a scale a sheet states inside a
panel is changed to the scale the booklet prints it at.
NEW IN v3 (Aras 26 Oct 05:54 "the booklet transformation is not really successful ... drawings themselves in a
separate pdf much more better"; 06:02 picked "sheet pages, split to 5 pt"): every page IS the sheet. An A3 sheet goes
in as it is; a panel of a big sheet is cut out WITH its own words and shown at one scale per page (never stretched,
nothing rewritten or moved). The
booklet adds only the cover, page titles, captions, page numbers and one sources page (each sheet's own source key).
A missing drawing leaves a labelled placeholder, so the booklet always builds.
"""
import os, re, time, json, fnmatch

# ---- SETTINGS ----
VERSION = "v22"
GH_LABEL = "Booklet"
OUT_FOLDER = "bergama_booklet"
LOG_NAME = "bergama_booklet_log.txt"
PDF_NAME = "Bergama_booklet_A3.pdf"
FONT = "Arial"                               # "Arial" (every Windows PC) or "Inter" (if installed)
G9_MARGIN = 0.5                              # v19 (MIRAQUA 28 Oct, G9): mm round a crop that its own copy keeps
G9_LINE_ART = True                           # v19 (G9): False keeps the line art outside a crop (only words and images go)

#@include ../common/bergama_paths.py
#@include ../common/hires.py
#@include ../common/grid.py
BERGAMA = BERGAMA_ROOT
OUT_DIR = bg_output(OUT_FOLDER)                  # v10 (27 Oct): the booklet PDF only
LOG_DIR = bg_logs()
ASSET_ROOT = os.path.join(BERGAMA, "output")     # the scripts' sheet PDFs
BK_ROOT = bg_booklet("")                         # v10: the scripts' booklet assets (cached/booklet/<folder>/blocks.json)

# ---- GRID (design-language.md: all values in mm, origin top-left) ----
# revision 30 Oct (M1): the ONE booklet grid lives in common/grid.py; the names below are its values
PW, PH = GRID_PAGE
ML, MT, MB = GRID_ML, GRID_MT, GRID_MB       # left/right margin, top, bottom
COLS, COL, GUT = GRID_COLS, GRID_COL, GRID_GUT   # 14 + 12 x 29 + 11 x 4 + 14 = 420
BASE = GRID_BASE                             # baseline grid, from y = 12
BOOK_VARIANTS = ("a", "b")                   # revision 30 Oct (D1, D5): two PDFs, ..._alt_a.pdf and ..._alt_b.pdf, each
                                             # crop id taken with the suffix _a / _b where its script wrote one
INTRO_MIN_COLS = 5                           # the intro sits beside the title when this many columns are free
LEG_ROW, LEG_GAP = 4.0, 4.0                  # a drawing's legend: row pitch, gap between its columns (mm)
FOOT_RULE, FOOT_B1, FOOT_B2 = 276.0, 280.0, 284.0
FOOT_LEG_COL = 1                             # v19 (MIRAQUA 28 Oct, G1): the footer legend from column 1 (was 4: the
                                             # project and course lines sat in columns 1-3)
PT = 25.4 / 72.0                             # mm per point
K = 72.0 / 25.4                              # points per mm

# ---- TYPE (pt; size follows design importance) ----
T = dict(title=40, part=24, figure=24, sub=14, statement=13, body=9.5, caption=7.5, label=7.5, kicker=8, pageno=14)
LEAD = dict(title=16.0, part=10.0, statement=6.0, sub=6.0, body=4.0, caption=3.2, label=3.2)   # mm
MIN_BODY, MIN_CAPTION = 9.0, 7.0

# ---- COLOUR (palette v1.4 core roles; contrast on white checked in design-language.md) ----
INK, INK2, ACCENT = "4A3F35", "6B645B", "8B3A3F"
RULE, FRAME, PAPER = "B0AC9C", "D8D5CC", "FFFFFF"

#@include data/PLAN.py


def colx(c):
    return ML + (c - 1) * (COL + GUT)


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


# ------------------------------------------------------------------ fonts
def font_files():
    """(regular, bold) TrueType files for FONT, else Arial, else Liberation Sans/DejaVu (offline test only)."""
    win = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
    user = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts")
    cands = {"Inter": [("Inter-Regular.ttf", "Inter-Bold.ttf"), ("Inter-Regular.otf", "Inter-Bold.otf")],
             "Arial": [("arial.ttf", "arialbd.ttf")]}
    order = [FONT] + [f for f in ("Arial",) if f != FONT]
    for fam in order:
        for reg, bold in cands.get(fam, []):
            for d in (win, user, "/usr/share/fonts/opentype/inter"):
                r, b = os.path.join(d, reg), os.path.join(d, bold)
                if os.path.isfile(r) and os.path.isfile(b):
                    return fam, r, b
    for d, r, b in (("/usr/share/fonts/truetype/liberation", "LiberationSans-Regular.ttf", "LiberationSans-Bold.ttf"),
                    ("/usr/share/fonts/truetype/dejavu", "DejaVuSans.ttf", "DejaVuSans-Bold.ttf")):
        if os.path.isfile(os.path.join(d, r)):
            return "fallback " + r[:-4], os.path.join(d, r), os.path.join(d, b)
    raise RuntimeError("no TrueType font found (looked for %s and Arial in %s)" % (FONT, win))


class Typo(object):
    """Text writer: whole lines as live text, one embedded font, wrapping by measured width."""
    def __init__(self, fitz):
        self.fam, self.freg, self.fbold = font_files()
        self.F = {False: fitz.Font(fontfile=self.freg), True: fitz.Font(fontfile=self.fbold)}
        self.issues, self.notes = [], []

    def width(self, s, size, bold=False):
        return self.F[bold].text_length(s, fontsize=size) * PT

    def split_long(self, word, w, size, bold=False):
        """A word wider than w (a URL) cut into pieces that fit, after / . - _ ? & = where possible."""
        out, cur = [], ""
        for ch in word:
            if cur and self.width(cur + ch, size, bold) > w:
                m = max(cur.rfind(c) for c in "/.-_?&=")
                if m > len(cur) // 2:
                    out.append(cur[:m + 1]); cur = cur[m + 1:]
                else:
                    out.append(cur); cur = ""
            cur += ch
        return out + [cur]

    def wrap(self, s, w, size, bold=False):
        out = []
        for para in str(s).split("\n"):
            line = ""
            words = []
            for word in para.split(" "):
                words += self.split_long(word, w, size, bold) if self.width(word, size, bold) > w else [word]
            for word in words:
                t = (line + " " + word).strip()
                if line and self.width(t, size, bold) > w:
                    out.append(line); line = word
                else:
                    line = t
            out.append(line)
        return out

    def line(self, page, s, x, y, size, col=INK, bold=False, align="L", angle=0.0, small_ok=False):
        """One line of live text; (x, y) = left (or centre/right) end of the baseline, mm; angle in degrees
        (counter-clockwise, about the baseline start). small_ok: only the sources page may go below 7 pt."""
        if not s:
            return
        if size < MIN_CAPTION and not small_ok:
            self.issues.append("TYPE BELOW 7 pt (%.1f): %s" % (size, s[:40]))
        if align != "L":
            wd = self.width(s, size, bold)
            x -= wd / 2 if align == "C" else wd
        if abs(angle) > 0.5:
            import fitz as _fz
            pt = _fz.Point(x * K, y * K)
            page.insert_text(pt, s, fontname="FB" if bold else "FR", fontsize=size, color=hexrgb(col),
                             morph=(pt, _fz.Matrix(-angle)))
        else:
            page.insert_text((x * K, y * K), s, fontname="FB" if bold else "FR", fontsize=size, color=hexrgb(col))


# ------------------------------------------------------------------ assets
def load_assets():
    """{script folder: blocks.json dict (with its folder)} for every script that wrote booklet assets."""
    found = {}
    names = set()
    for root in (BK_ROOT, ASSET_ROOT):
        if os.path.isdir(root):
            names.update(n for n in os.listdir(root) if os.path.isdir(os.path.join(root, n)))
    for name in sorted(names):
        p = bg_first([os.path.join(BK_ROOT, name, "blocks.json"),                 # v10: cached/booklet/<folder>/
                      os.path.join(ASSET_ROOT, name, "booklet", "blocks.json")])   # scripts before 27 Oct
        if os.path.isfile(p):
            try:
                with open(p, encoding="utf-8") as f:
                    d = json.load(f)
                d["_dir"] = os.path.dirname(p)
                d["_time"] = time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
                found[name] = d
            except Exception as ex:
                found[name] = {"_error": "%s: %s" % (type(ex).__name__, ex)}
    return found


# ------------------------------------------------------------------ sheets
_DOCS = {}


def sheet_doc(fitz, path):
    if path not in _DOCS:
        _DOCS[path] = fitz.open(path)
    return _DOCS[path]


def find_pdf(folder, name):
    """A sheet PDF of a script's output folder (subfolders too, e.g. the board's selinus_board_pdf); name may hold *."""
    root = os.path.join(ASSET_ROOT, folder)
    hit = [os.path.join(d, n) for d, _, names in os.walk(root) for n in names if fnmatch.fnmatch(n, name)]
    return max(hit, key=os.path.getmtime) if hit else None    # v7: the newest (v1_8 sorts after v1_12 by name)


_COPY = {}       # v19 (G9): (sheet path, page index, clip key) -> (doc, page index): one copy per place a page shows
_PAGE_TXT = {}   # v19: (sheet path, page index) -> (its lines of words, invisible words, images): read once a run
_FONTBUF = {}    # v19 (G2): bold -> (font file bytes, fitz.Font): the booklet's Arial, read once a run
G9_STATS = dict(copies=0, lines=0, chars=0, images=0, failed=[])
_RED = dict(img_none=0, img_remove=1, art_none=0, art_covered=1, txt_remove=0, txt_none=1)   # PyMuPDF redaction codes


def clip_key(clip):
    return None if clip is None else tuple(round(v, 1) for v in clip)


def src_page(fitz, path, pno_, clip=None):
    """v18: (doc, page index) the booklet shows of a sheet page. v19 (MIRAQUA 28 Oct, G9): one copy per (sheet, page,
    clip), made once (strip_copy): its marks in the booklet's source numbers and, for a crop, nothing outside it"""
    ck = (path, pno_, clip_key(clip))
    if ck not in _COPY:
        _COPY[ck] = strip_copy(fitz, path, pno_, clip, _SRC[0] if _SRC else None)
    return _COPY[ck]


def own_font(fitz, pg, bold=False):
    """v19 (MIRAQUA 28 Oct, G2): the booklet's Arial, embedded on a copied sheet page for the words the booklet
    rewrites there (scales, source numbers; they were the standard Helvetica helv/hebo, not embedded):
    (font name on pg, fitz.Font to measure with)"""
    if bold not in _FONTBUF:
        with open(font_files()[2 if bold else 1], "rb") as f:
            data = f.read()
        _FONTBUF[bold] = (data, fitz.Font(fontbuffer=data))
    name = "BkB" if bold else "BkR"                  # never the sheets' own /F1 ... names
    pg.insert_font(fontname=name, fontbuffer=_FONTBUF[bold][0])
    return name, _FONTBUF[bold][1]


def page_text(fitz, path, i):
    """v19: a sheet page's lines of words (rawdict), its invisible words (render mode 3, e.g. the water balance's
    source key) and its images (bboxes), read once a run for every copy made of it (laptop speed: they were read
    again for each copy)"""
    k = (path, i)
    if k not in _PAGE_TXT:
        page = sheet_doc(fitz, path)[i]
        lines = [ln for b in page.get_text("rawdict")["blocks"] for ln in b.get("lines", [])]
        try:
            inv = [fitz.Rect(s_["bbox"]) for s_ in page.get_texttrace() if s_.get("type") == 3]
        except Exception:
            inv = []
        try:
            ims = [fitz.Rect(im["bbox"]) for im in page.get_image_info()]
        except Exception:
            ims = []
        _PAGE_TXT[k] = (lines, inv, ims)
    return _PAGE_TXT[k]


def strip_copy(fitz, path, i, clip, srcs=None):
    """v19 (MIRAQUA 28 Oct, G9 "remove everything that isn't visible on its own page"): (doc, page index) of sheet page
    i copied for ONE place the booklet shows it; the sheet page itself when nothing changes or the copy fails (logged)"""
    try:
        return _strip_copy(fitz, path, i, clip, srcs)
    except Exception as ex:
        G9_STATS["failed"].append("%s page %d (%s: %s)" % (os.path.basename(path), i + 1, type(ex).__name__, ex))
        return sheet_doc(fitz, path), i


def _strip_copy(fitz, path, i, clip, srcs):
    """The copy: its [n] marks in the booklet's numbers (srcs; v18) and, for a crop (clip), what no viewer sees taken out
    (v18 took out only the words outside every crop of the page, 3 mm round them; graphics and images all stayed):
    the words outside the clip + G9_MARGIN (whole lines, else the letters of a line across its edge); the images
    wholly outside it; the line art lying wholly in the four bands round it (PDF_REDACT_LINE_ART_REMOVE_IF_COVERED: a
    path partly inside stays whole with its hidden part, e.g. the long street lines and the big building fills; never
    IF_TOUCHED, which would cut visible lines). Three redaction passes: words, images, line art, each blind to the others."""
    lines, inv, ims = page_text(fitz, path, i)
    folder = (srcs.used.get((path, i)) or [None])[0] if srcs else None
    kid = srcs.key_for(folder, path, i) if srcs and folder else None
    pr = sheet_doc(fitz, path)[i].rect
    mg = G9_MARGIN * K
    near = None if clip is None else fitz.Rect(clip.x0 - mg, clip.y0 - mg, clip.x1 + mg, clip.y1 + mg)
    cut, put, seen, n_l, n_c = [], [], [], 0, 0

    def mid(r, a=None, b=None):                       # the middle of letters: the lines above and below stay whole
        a, b = r if a is None else a, r if b is None else b
        return fitz.Rect(r.x0 + 0.2 * a.width, r.y0 + 0.3 * r.height, r.x1 - 0.2 * b.width, r.y1 - 0.3 * r.height)
    for ln in lines:
        lr = fitz.Rect(ln["bbox"])
        if lr.width < 0.1 or lr.height < 0.1:
            continue
        if near is not None and not lr.intersects(near):          # shown nowhere here: the whole line goes
            cut.append(fitz.Rect(lr.x0, lr.y0 + 0.3 * lr.height, lr.x1, lr.y1 - 0.3 * lr.height))
            n_l += 1
            continue
        seen.append(lr)
        seq = [(ch, s_) for s_ in ln["spans"] for ch in s_["chars"]]
        if near is not None and not near.contains(lr):            # across the clip's edge: its letters outside
            run = []
            for ch, _ in seq + [(None, None)]:
                cr = fitz.Rect(ch["bbox"]) if ch is not None else None
                if cr is not None and cr.width > 0.05 and not cr.intersects(near):
                    run.append(cr)
                    continue
                if run:
                    u = fitz.Rect(run[0])
                    for c_ in run[1:]:
                        u |= c_
                    cut.append(mid(fitz.Rect(u.x0, lr.y0, u.x1, lr.y1), run[0], run[-1]))
                    n_c += len(run)
                    run = []
        if kid is None or abs(ln["dir"][1]) > 0.01 or any(lr.intersects(v) for v in inv):
            continue                                              # turned words, the invisible key
        txt = "".join(ch["c"] for ch, _ in seq)
        for m in MARKS.finditer(txt):
            new = srcs.renum(m.group(0), kid)
            if new == m.group(0):
                continue
            (c0, s0), c1 = seq[m.start()], seq[m.end() - 1][0]
            r = fitz.Rect(c0["bbox"]) | fitz.Rect(c1["bbox"])
            if near is not None and not r.intersects(near):
                continue                                          # it goes with the letters outside the clip
            cut.append(mid(r, fitz.Rect(c0["bbox"]), fitz.Rect(c1["bbox"])))
            if new:                                               # v19 (F5): "" = its sources are not public online
                nxt = next((ch["bbox"][0] for ch, _ in seq[m.end():] if ch["c"].strip()), None)
                ends = [clip.x1] if clip is not None and clip.intersects(r) else []
                room = min([pr.x1 if nxt is None else nxt] + ends) - c0["origin"][0] - 0.3
                put.append((c0["origin"], new, s0["size"], s0["color"], "bold" in s0["font"].lower(), room))
    gone, bands = [], []
    if near is not None:
        keep = [r for r in ims if r.intersects(near)]
        for r in ims:                                 # an image wholly outside: a dot at its centre that hits nothing seen
            if r.is_empty or r.intersects(near):
                continue
            c = fitz.Point((r.x0 + r.x1) / 2.0, (r.y0 + r.y1) / 2.0)
            if not any(k_.contains(c) for k_ in keep + seen):
                gone.append(fitz.Rect(c.x - 0.05, c.y - 0.05, c.x + 0.05, c.y + 0.05))
        if G9_LINE_ART:                               # left and right bands full height: a corner path lies in one
            bands = [b for b in (fitz.Rect(pr.x0, pr.y0, pr.x1, near.y0), fitz.Rect(pr.x0, near.y1, pr.x1, pr.y1),
                                 fitz.Rect(pr.x0, pr.y0, near.x0, pr.y1), fitz.Rect(near.x1, pr.y0, pr.x1, pr.y1))
                     if b.width > 1.0 and b.height > 1.0]
    if clip is None and not cut and not put:
        return sheet_doc(fitz, path), i               # a whole sheet page with nothing to renumber: the sheet itself
    tmp = fitz.open()
    tmp.insert_pdf(sheet_doc(fitz, path), from_page=i, to_page=i)
    pg = tmp[0]
    for annots, opt in ((cut, dict(images=_RED["img_none"], graphics=_RED["art_none"], text=_RED["txt_remove"])),
                        (gone, dict(images=_RED["img_remove"], graphics=_RED["art_none"], text=_RED["txt_none"])),
                        (bands, dict(images=_RED["img_none"], graphics=_RED["art_covered"], text=_RED["txt_none"]))):
        if annots:
            for r in annots:
                pg.add_redact_annot(r, fill=False)
            pg.apply_redactions(**opt)
    fonts = {}
    for org, new, size, col, bold, room in put:       # the new numbers in the booklet's own Arial (G2)
        if bold not in fonts:
            fonts[bold] = own_font(fitz, pg, bold)
        fn, font = fonts[bold]
        w = font.text_length(new, fontsize=size)
        if w > room > 0:                              # the words after it stay clear
            size2 = max(0.75 * size, size * room / w)
            if srcs:
                srcs.n_tight += int(w * size2 / size > room + 0.2)
            size = size2
        pg.insert_text(org, new, fontname=fn, fontsize=size,
                       color=((col >> 16 & 255) / 255.0, (col >> 8 & 255) / 255.0, (col & 255) / 255.0))
    if clip is not None:
        G9_STATS["copies"] += 1
        G9_STATS["lines"] += n_l
        G9_STATS["chars"] += n_c
        G9_STATS["images"] += len(gone)
    return tmp, 0


def resolve(assets, key):
    """(crop block, sheet path) of "<folder>/<crop id>"; an id missing under its own sheet key or letter case is looked
    up by its panel name (the board's sections are section_s1 ... on whichever sheet holds them)."""
    folder, _, bid = key.partition("/")
    bl = (assets.get(folder) or {}).get("blocks") or {}
    b = bl.get(bid)
    if b is None:
        tail = bid.lower().split("_", 1)[-1]
        b = next((v for k, v in sorted(bl.items()) if k.lower() == bid.lower() or
                  k.lower().split("_", 1)[-1] == tail), None)
    if not b or b.get("type") != "crop":
        return None, None
    return b, find_pdf(folder, os.path.basename(b.get("pdf", "")))


SCALE_WORD = re.compile(r"1\s?:\s?(\d{1,3}(?:,\d{3})+|\d{2,})")


def rescaled(fitz, path, pno_, clip, s, drop=()):
    """v4: the sheet page with each scale it states inside clip ("1:400") changed to the scale the booklet prints it
    at (1:400 / s), in the same place, size and colour; the drawing itself untouched. v7: a line of the sheet's words
    matching one of its crop's "drop" patterns is taken out (source marks "[n]" stay). (doc, page index)"""
    src, pno_ = src_page(fitz, path, pno_, clip)         # v18: the booklet's source numbers; v19 (G9): this crop's copy
    page = src[pno_]
    pats = [re.compile(d) for d in drop or () if not d.startswith("^\\[")]
    hits, gone = {}, []
    for b in page.get_text("dict", clip=clip)["blocks"]:
        for ln in b.get("lines", []):
            if pats and any(p.search("".join(sp["text"] for sp in ln["spans"]).strip()) for p in pats):
                gone.append(fitz.Rect(ln["bbox"]))
                continue
            for sp in ln["spans"]:
                for m in SCALE_WORD.finditer(sp["text"]):
                    hits[m.group(0)] = (int(m.group(1).replace(",", "")), sp["size"], sp["color"],
                                        "bold" in sp["font"].lower())
    if abs(s - 1.0) < 1e-3:
        hits = {}
    if not hits and not gone:
        return src, pno_
    tmp = fitz.open()
    tmp.insert_pdf(src, from_page=pno_, to_page=pno_)
    pg = tmp[0]
    for r in gone:                                   # the middle of the line only: the lines above/below stay whole
        pg.add_redact_annot(fitz.Rect(r.x0, r.y0 + 0.3 * r.height, r.x1, r.y1 - 0.3 * r.height), fill=False)
    put = []
    for word, (den, size, col, bold) in hits.items():
        for r in pg.search_for(word, clip=clip):
            pg.add_redact_annot(r, fill=False)
            put.append((r, "1:{:,.0f}".format(den / s), size, col, bold))
    pg.apply_redactions(images=0, graphics=0, text=0)
    fonts = {}
    for r, txt, size, col, bold in put:              # v19 (MIRAQUA 28 Oct, G2): in the booklet's embedded Arial
        if bold not in fonts:
            fonts[bold] = own_font(fitz, pg, bold)[0]
        pg.insert_text((r.x0, r.y1 - 0.22 * size), txt, fontsize=size, fontname=fonts[bold],
                       color=((col >> 16 & 255) / 255.0, (col >> 8 & 255) / 255.0, (col & 255) / 255.0))
    return tmp, 0


def word_sizes(page, clip):
    return sorted(sp["size"] for b in page.get_text("dict", clip=clip)["blocks"] for ln in b.get("lines", [])
                  for sp in ln["spans"] if sp["text"].strip())


def std_scale(den):
    """v4 (Aras 26 Oct 06:35 "they need to be round numbers"): the first round scale at or above den. v12: within
    0.05 % counts as that scale (a drawing made at a round booklet scale, its sheet scale rounded to whole numbers)"""
    return next((d for d in STD_SCALES if d >= den - max(0.5, 5e-4 * den)), den)


def nearest_std(v):
    """v12: the round scale nearest v"""
    return min(STD_SCALES, key=lambda d: abs(d - v) / d)


STD_SCALES = (100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000, 25000, 50000, 100000)
CAP_H, ROW_GAP = 5.0, 6.0                        # caption band under each panel, gap between rows (mm)
AREA = (ML, 30.0, PW - ML, FOOT_RULE - 3.0)        # where the panels go (mm)


# ------------------------------------------------------------------ pages
def frame_page(fitz, doc, typo):
    pg = doc.new_page(width=PW * K, height=PH * K)
    pg.insert_font(fontname="FR", fontfile=typo.freg)
    pg.insert_font(fontname="FB", fontfile=typo.fbold)
    return pg


_TOTAL = [0]       # revision 30 Oct (G2): the final page count of the booklet being built (cover + pages + sources)
_VARIANT = [None]  # revision 30 Oct (D1, D5): "a" / "b" while that PDF is built


def page_no(pno):
    """revision 30 Oct (G2 [C]): the page counter, computed from the final page list: "07/23" (a text is kept)"""
    if isinstance(pno, str):
        return pno
    return grid_page_counter(pno, _TOTAL[0]) if _TOTAL[0] else "%02d" % pno


def intro_layout(typo, spec):
    """revision 30 Oct (M1, G4): the page intro of PLAN (spec "intro", key words marked "*word*") as (lines, size,
    lead, x, first baseline, extra): beside the title in the title band when INTRO_MIN_COLS columns are free there,
    else under the rule, where `extra` mm is the room the panels give up. None without an intro."""
    txt = spec.get("intro")
    if not txt:
        return None
    measure = lambda s_, size_, bold_: typo.width(s_, size_, bold_)
    tw = typo.width(spec.get("title", ""), T["part"], True)
    c0 = next((c for c in range(2, COLS + 1) if colx(c) >= colx(1) + tw + GUT), COLS + 1)
    if COLS - c0 + 1 >= INTRO_MIN_COLS:
        x = colx(c0)
        lines, size, lead, _ = grid_intro(txt, PW - ML - x, measure, 3, log=typo.issues)
        y0 = 25.0 - 1.6 - lead * (len(lines) - 1)     # the last line sits on the band's lowest baseline
        return lines, size, lead, x, max(MT + 2.4, y0), 0.0
    lines, size, lead, _ = grid_intro(txt, PW - 2 * ML, measure, 3, log=typo.issues)
    return lines, size, lead, colx(1), 25.0 + BASE + 0.4, grid_snap_h(lead * len(lines) + 1.0)


def header(pg, typo, spec):
    part = PARTS.get(spec.get("part"), "")
    stage = STAGES.get(spec.get("stage"), "")         # v11: where the page sits in its theme's cycle
    typo.line(pg, (spec.get("part", "") + "   " + part + ("   ·   " + stage if stage else "")).upper(), colx(1), 12,
              T["kicker"], ACCENT, True)
    typo.line(pg, spec.get("title", ""), colx(1), 22, T["part"], INK, True)
    pg.draw_line((colx(1) * K, 25 * K), ((PW - ML) * K, 25 * K), color=hexrgb(RULE), width=0.25)
    il = intro_layout(typo, spec)                     # revision 30 Oct (M1, G4): 2-3 lines, key words bold
    if il:
        lines, size, lead, x, y0, extra = il
        for s_, x_, y_, b_ in grid_text_runs(lines, x, y0, lead):
            typo.line(pg, s_, x_, y_, size, INK, b_)
        return extra
    return 0.0


def intro_extra(typo, spec):
    """the mm the intro takes from the panel area (0 when it sits beside the title)"""
    il = intro_layout(typo, spec)
    return il[5] if il else 0.0


def foot_label(spec):
    part = PARTS.get(spec.get("part"), "")
    return (spec.get("part", "") + "  " + part).upper() if part else ""


def foot_x1(typo, spec):
    """v11: the legend band ends 5 mm before the footer's theme label (longer since v11), never under it"""
    lab = foot_label(spec)
    return PW - ML - 12 - (typo.width(lab, T["caption"], True) + 5.0 if lab else 22.0)


def footer(pg, typo, pno, spec, legend):
    """v19 (MIRAQUA 28 Oct, G1): the rule, the theme label and the page number (pno: a number, or the words to print
    there); the project and course lines are gone"""
    pg.draw_line((colx(1) * K, FOOT_RULE * K), ((PW - ML) * K, FOOT_RULE * K), color=hexrgb(RULE), width=0.25)
    no = page_no(pno)                                # revision 30 Oct (G2): "NN/total", computed
    typo.line(pg, no, PW - ML, FOOT_B2 + 0.6, T["pageno"], ACCENT, True, "R")
    lab_x = PW - ML - 12 - max(0.0, typo.width(no, T["pageno"], True) - typo.width("00", T["pageno"], True))
    if foot_label(spec):
        typo.line(pg, foot_label(spec), lab_x, FOOT_B2, T["caption"], INK2, True, "R")
    # legend: same place on every page (v19: from column 1 of the footer band), drawn samples + plain names
    x0, x1 = colx(FOOT_LEG_COL), foot_x1(typo, spec) - (PW - ML - 12 - lab_x)
    x, y = x0, FOOT_B1
    for it in legend or []:
        w = 4.0 + 1.5 + typo.width(it.get("label", ""), T["caption"]) + 5.0
        if x + w > x1:
            x, y = x0, y + 4.0
            if y > FOOT_B2 + 4.5:
                typo.issues.append("LEGEND TOO LONG p.%s" % pno)
                break
        legend_item(pg, typo, it, x, y)
        x += w


def legend_item(pg, typo, it, x, y):
    """one legend entry: a drawn sample (fill, line or dot) and its plain name, baseline y"""
    c = hexrgb(it.get("colour", INK))
    kind = it.get("kind", "fill")
    if kind == "line":
        pg.draw_line((x * K, (y - 1.2) * K), ((x + 4.0) * K, (y - 1.2) * K), color=c, width=it.get("width", 1.2))
    elif kind == "dot":
        pg.draw_circle(((x + 2.0) * K, (y - 1.2) * K), 1.3 * K, color=None, fill=c)
    elif kind in ("dash", "dashdot"):                    # MIRAQUA round: dashed samples (dashdot = the study area, G8)
        pat = "[3 0.8 0.4 0.8]" if kind == "dashdot" else "[1.6 0.9]"
        pg.draw_line((x * K, (y - 1.2) * K), ((x + 5.0) * K, (y - 1.2) * K), color=c, width=it.get("width", 1.2),
                     dashes="[%s] 0" % " ".join("%.2f" % (float(v) * K) for v in pat.strip("[]").split()))
    else:
        pg.draw_rect((x * K, (y - 2.6) * K, (x + 4.0) * K, (y + 0.2) * K), color=None, fill=c)
    typo.line(pg, it.get("label", ""), x + 5.5, y, T["caption"], INK)


def placeholder(pg, typo, rect, text):
    x, y, w, h = rect
    pg.draw_rect((x * K, y * K, (x + w) * K, (y + h) * K), color=hexrgb(FRAME), width=0.5, dashes="[2 2] 0")
    typo.line(pg, text, x + w / 2, y + h / 2, T["body"], INK2, False, "C")


def sheet_page(fitz, doc, typo, pno, spec):
    """A whole A3 sheet page, as it is (a sheet of another size: scaled to fit, one scale)."""
    folder, _, name = spec["sheet"].partition("/")
    path = find_pdf(folder, name)
    pg = frame_page(fitz, doc, typo)
    if not path or int(spec.get("page", 0)) >= len(sheet_doc(fitz, path)):
        header(pg, typo, spec)
        placeholder(pg, typo, (ML, AREA[1], PW - 2 * ML, AREA[3] - AREA[1]),
                    "%s · %s missing: run the script" % (SCRIPT_OF.get(folder, folder), name))
        footer(pg, typo, pno, spec, [])
        return "p.%d %s: MISSING %s" % (pno, spec["title"], name)
    sd, si = src_page(fitz, path, int(spec.get("page", 0)))     # v18: marks in the booklet's source numbers
    src = sd[si]
    f = min(PW * K / src.rect.width, PH * K / src.rect.height)
    pg.show_pdf_page(fitz.Rect(0, 0, src.rect.width * f, src.rect.height * f), sd, si)
    sheet_foot(fitz, pg, typo, pno, spec, src, f)
    return "p.%d %s: sheet %s page %d as it is%s" % (pno, spec["title"], os.path.basename(path),
                                                   int(spec.get("page", 0)) + 1, "" if f > 0.999 else " (x%.2f)" % f)


def sheet_foot(fitz, pg, typo, pno, spec, src, f):
    """v18 (Prompt 8: "footers and page numbers"): a whole-sheet page gets the booklet's page number in the footer's
    place, and its theme left of it where the sheet leaves that corner free; the log says when the number sits on
    the sheet's own words or drawing."""
    no = page_no(pno)                                # revision 30 Oct (G2): "NN/total", computed
    wn, lab = typo.width(no, T["pageno"], True), foot_label(spec)
    rn = (PW - ML - wn - 1.0, FOOT_B2 - 4.6, PW - ML + 0.5, FOOT_B2 + 1.4)
    wl = typo.width(lab, T["caption"], True) if lab else 0.0
    sh_ = max(0.0, wn - typo.width("00", T["pageno"], True))      # revision 30 Oct: the longer "NN/total"
    rl = (PW - ML - 12 - sh_ - wl - 1.0, FOOT_B2 - 2.8, PW - ML - 12 - sh_ + 0.5, FOOT_B2 + 1.0)
    try:
        big = 0.5 * abs(src.rect)                      # a sheet's white ground is not "content"
        boxes = [fitz.Rect(d["rect"]) for d in src.get_drawings() if abs(fitz.Rect(d["rect"])) < big]
        boxes += [fitz.Rect(w[:4]) for w in src.get_text("words")]
    except Exception:
        boxes = []

    def free(r):
        R = fitz.Rect(r[0] * K / f, r[1] * K / f, r[2] * K / f, r[3] * K / f)
        return not any(b.intersects(R) for b in boxes)
    if not free(rn):
        typo.issues.append("PAGE NUMBER ON THE SHEET'S OWN CONTENT p.%d %s" % (pno, spec.get("title", "")))
    typo.line(pg, no, PW - ML, FOOT_B2 + 0.6, T["pageno"], ACCENT, True, "R")
    if lab and free(rl):
        typo.line(pg, lab, PW - ML - 12 - sh_, FOOT_B2, T["caption"], INK2, True, "R")


def wh(it):
    if it[3] is None and it[1] and it[1].get("slot"):  # v11: a frame for a later drawing keeps its planned size
        return it[1]["size_mm"]
    return (it[3].width / K, it[3].height / K) if it[3] is not None else (200.0, 60.0)


def fixed(it):
    """v15: a crop drawn for its width on the booklet page (block "bk_w") keeps that size (own_s) in a row"""
    return bool(it[1] and it[1].get("bk_w") and it[3] is not None)


def absent(it):
    """v19: a panel its script has not written (a frame for a later drawing is not absent)"""
    return it[3] is None and not (it[1] and it[1].get("slot"))


def row_items(r):
    """v19: the panels of a row that set its size: a missing panel beside drawn ones only takes the room they leave
    (its labelled frame there), so a note not yet written never shrinks the maps of p.07"""
    return [it for it in r if not absent(it)] or r


def scale_of(it, s_fit):
    """v19 (was panel_page's sc): the factor a panel prints at on a page of scale s_fit: drawn for its booklet width
    (v15): its own size; with a true scale: the round scale at or below s_fit (v4); else s_fit"""
    if fixed(it):
        return own_s(it)
    den = it[1].get("scale_den") if it[1] and it[3] is not None else None
    return den / std_scale(den / s_fit) if den else s_fit


def fit(rows, aw=None, ah=None):
    """the one scale at which every row fits the panel area's width (v12: or aw mm) and all rows its height (v19: or ah
    mm: a key map's band takes its share); v15: the fixed crops (fixed) keep their own size, the others share the
    width and height they leave"""
    aw = aw if aw is not None else AREA[2] - AREA[0]
    ah = ah if ah is not None else AREA[3] - AREA[1]
    ws, hs, hfix = [], [], 0.0
    for r in rows:
        r = row_items(r)                               # v19
        free = [it for it in r if not fixed(it)]
        if free:
            ws.append((aw - GUT * (len(r) - 1) - sum(wh(it)[0] * own_s(it) for it in r if fixed(it))) /
                      sum(wh(it)[0] for it in free))
            hs.append(max(wh(it)[1] for it in free))
        else:
            hfix += max(wh(it)[1] * own_s(it) for it in r)
    if not hs:
        return 1.0
    return max(0.02, min(ws + [(ah - len(rows) * CAP_H - (len(rows) - 1) * ROW_GAP - hfix) / sum(hs)]))


def own_s(it):
    """v12: the factor a crop prints at when it is drawn for a width on the booklet page (block "bk_w", mm): exactly
    its round scale when it has one"""
    w, h = wh(it)
    blk = it[1] or {}
    s = blk["bk_w"] / w if blk.get("bk_w") and it[3] is not None else 1.0
    den = blk.get("scale_den") if it[3] is not None else None
    return den / nearest_std(den / s) if den else s


def show(fitz, pg, typo, it, x, y, s, rep, missing, cap=True):
    """v12: one crop (or its labelled placeholder) at (x, y) mm, factor s, its caption under it; returns its height"""
    key, blk, path, clip = it
    w, h = wh(it)
    if clip is None:
        missing.add(key.partition("/")[0])
        placeholder(pg, typo, (x, y, w * s, h * s), "%s · %s" % (SCRIPT_OF.get(key.partition("/")[0], ""),
                                                                key.split("/")[1]))
        rep.append("%s MISSING" % key)
        return h * s
    src, pi = rescaled(fitz, path, int(blk.get("page", 0)), clip, s, blk.get("drop"))
    pg.show_pdf_page(fitz.Rect(x * K, y * K, (x + w * s) * K, (y + h * s) * K), src, pi, clip=clip)
    if cap:
        c = renum(blk.get("caption", ""), key, blk, path)      # v18: its marks in the booklet's source numbers
        if blk.get("scale_den"):
            c = (c + " · " if c else "") + "1:{:,.0f}".format(blk["scale_den"] / s)
        typo.line(pg, c, x, y + h * s + 3.6, T["caption"], INK2)
    ws = word_sizes(src[pi], clip)
    if ws:
        rep.append("%s words %.1f pt (smallest tenth %.1f)" % (key.split("/", 1)[1], ws[len(ws) // 2] * s,
                                                                ws[len(ws) // 10] * s))
    return h * s


def panel_page(fitz, doc, typo, pno, spec, rows, assets, missing):
    """rows of [(key, crop block, sheet path, clip)]: one scale for the page, the largest at which every row fits the
    width and all rows the height; a drawing with a true scale takes the round scale at or just below it (v4), so
    its printed scale is always round; each panel with its own words. v12: "side" panels at the right margin beside
    the rows (their own width), the page's legend under them; a "key" map in the title band at the right.
    v19 (MIRAQUA 28 Oct, P04.1, P14.1): the key map at scale 1.0 (drawn at its booklet size, 190 x <= 42 mm; never
    stretched) in a band under the title, the rows below it making room; beside the rows at the top right instead
    when that costs them less (a narrow map, or a fixed crop the band would push past the page).
    Revision 30 Oct (G1, M1, M2): each crop's legend is drawn under it, aligned to its left edge, in the columns its
    width holds (never in the footer band, never detached); the rows make room for it. The page intro (PLAN "intro",
    G4) sits beside the title or under it; the footer prints the page counter NN/total."""
    top0 = AREA[1] + intro_extra(typo, spec)          # revision 30 Oct (G4): an intro under the title takes its room
    aw, ah = AREA[2] - AREA[0], AREA[3] - top0
    side_it = spec.get("_side") or []
    # v19: a missing side panel does not set the column's width (its labelled frame takes the column)
    side_w = min(aw / 2.0, max([wh(it)[0] * own_s(it) for it in row_items(side_it)] or [0.0]))
    aw_r = aw - side_w - GUT if side_it else aw      # the rows' width
    key_it, key_at, kw, kh, ks = spec.get("_key"), None, 0.0, 0.0, 1.0
    if key_it is not None and key_it[3] is not None:
        kw, kh = wh(key_it)
        ks = min(1.0, aw / kw)
        kw, kh = kw * ks, kh * ks
        opts = [("band", aw_r, ah - kh - ROW_GAP)] + ([("beside", aw_r - kw - GUT, ah)]
                                                       if not side_it and aw_r - kw - GUT >= 60.0 else [])
        best = None
        for at, w_, h_ in opts:                      # least overrun first, then the largest scale; a tie: the band
            s_ = fit(rows, w_, h_)
            hh = sum(max(wh(it)[1] * scale_of(it, s_) for it in row_items(r)) + CAP_H for r in rows) + \
                ROW_GAP * (len(rows) - 1)
            ww = max(sum(wh(it)[0] * scale_of(it, s_) for it in row_items(r)) + GUT * (len(row_items(r)) - 1)
                     for r in rows)
            cost = (round(max(0.0, hh - h_, ww - w_), 1), -round(s_, 4))
            if best is None or cost < best[0]:
                best = (cost, at)
        key_at = best[1]
        if ks < 0.999:
            typo.issues.append("KEY MAP WIDER THAN THE PAGE p.%d: printed at %.0f %%" % (pno, 100.0 * ks))
        if kh > 42.5:
            typo.issues.append("KEY MAP TALLER THAN 42 mm p.%d (%.0f mm): the rows lose that height" % (pno, kh))
    ah_r = ah - (kh + ROW_GAP if key_at == "band" else 0.0)
    aw_r -= kw + GUT if key_at == "beside" else 0.0

    def row_leg(r, s_):                              # revision 30 Oct (G1): the legend band under a row's crops
        return max([legend_h(typo, crop_legend(it), wh(it)[0] * scale_of(it, s_)) for it in row_items(r)] or [0.0])
    s_fit = fit(rows, aw_r, ah_r)
    for _ in range(3):                               # narrower crops hold fewer legend columns: settle the scale
        s_fit = fit(rows, aw_r, ah_r - sum(row_leg(r, s_fit) for r in rows))
    leg_rows = [row_leg(r, s_fit) for r in rows]

    def sc(it):                                      # v4, v15 (v19: scale_of)
        return scale_of(it, s_fit)
    pg = frame_page(fitz, doc, typo)
    header(pg, typo, spec)
    rep = []
    y = y_top = top0 + (kh + ROW_GAP if key_at == "band" else 0.0)
    if key_it is not None and key_it[3] is None:
        rep.append("%s MISSING (key map left out)" % key_it[0])
    rws = [sum(wh(it)[0] * sc(it) for it in row_items(r)) + GUT * (len(row_items(r)) - 1) for r in rows]
    if key_at:                                       # v19: the key map, scale 1.0, no caption (no scale: a key map)
        kx = AREA[2] - kw if key_at == "beside" or side_it else \
            max(AREA[0], min(AREA[2], AREA[0] + (aw + max(rws)) / 2.0) - kw)   # band: flush with the rows' right edge
        show(fitz, pg, typo, key_it, kx, top0, ks, rep, missing, cap=False)
        rep.append("key map %s" % ("beside the rows" if key_at == "beside" else "in the band under the title"))
    # v18 (Prompt 8, rule 4 "no large empty areas"): rows that leave more than 40 mm of the height empty share it out
    # (old p.10: 91 mm under two maps the width holds at 1:10,000)
    free = ah_r - sum(max(wh(it)[1] * sc(it) for it in row_items(r)) + CAP_H + lh + ROW_GAP
                      for r, lh in zip(rows, leg_rows)) + ROW_GAP
    pad = free / (len(rows) + 1) if len(rows) > 1 and free > 40.0 and not side_it else 0.0
    y += pad
    for r, rw, lh in zip(rows, rws, leg_rows):       # rows centred across the page
        pres = row_items(r)
        fill = [it for it in r if not any(it is p for p in pres)]    # v19: missing beside drawn panels
        x = AREA[0] + (0.0 if side_it or fill or key_at == "beside" else max(0.0, (aw - rw) / 2.0))
        rh = max(wh(it)[1] * sc(it) for it in pres)
        fw = (aw_r - rw - GUT * len(fill)) / len(fill) if fill else 0.0
        for it in r:
            key, blk, path, clip = it
            if any(it is f for f in fill):          # v19: its labelled frame in the room the drawn panels leave
                missing.add(key.partition("/")[0])
                rep.append("%s MISSING" % key)
                if fw >= 20.0:
                    placeholder(pg, typo, (x, y, fw, rh), "%s · %s" % (SCRIPT_OF.get(key.partition("/")[0], ""),
                                                                      key.split("/")[1]))
                    x += fw + GUT
                continue
            s = sc(it)
            w, h = wh(it)
            if clip is None and blk and blk.get("slot"):     # v11: frame for a drawing a later prompt makes
                placeholder(pg, typo, (x, y, w * s, h * s), blk["slot"])
                rep.append("frame: %s" % blk["slot"])
            elif clip is None:
                missing.add(key.partition("/")[0])
                placeholder(pg, typo, (x, y, w * s, h * s), "%s · %s" % (SCRIPT_OF.get(key.partition("/")[0], ""),
                                                                        key.split("/")[1]))
                rep.append("%s MISSING" % key)
            else:
                src, pi = rescaled(fitz, path, int(blk.get("page", 0)), clip, s, blk.get("drop"))
                pg.show_pdf_page(fitz.Rect(x * K, y * K, (x + w * s) * K, (y + h * s) * K), src, pi, clip=clip)
                cap = renum(blk.get("caption", ""), key, blk, path)   # v18: the booklet's source numbers
                if blk.get("scale_den"):
                    cap = (cap + " · " if cap else "") + "1:{:,.0f}".format(blk["scale_den"] / s)
                    if round(blk["scale_den"] / s) not in STD_SCALES:
                        typo.issues.append("SCALE NOT ROUND p.%d %s: 1:%.0f" % (pno, key, blk["scale_den"] / s))
                typo.line(pg, cap, x, y + h * s + 3.6, T["caption"], INK2)
                lg = crop_legend(it)                 # revision 30 Oct (G1): its legend under it, aligned to it
                if lg:
                    draw_legend_under(pg, typo, lg, x, y + h * s + CAP_H - 0.6, w * s, pno)
                ws = word_sizes(src[pi], clip)
                if ws:
                    med, low = ws[len(ws) // 2] * s, ws[len(ws) // 10] * s
                    rep.append("%s words %.1f pt (smallest tenth %.1f)" % (key.split("/", 1)[1], med, low))
            x += w * s + GUT
        y += rh + CAP_H + lh + ROW_GAP + pad
    if y - ROW_GAP > AREA[3] + 0.5:                  # v15: fixed crops are not shrunk: say when they overrun
        typo.issues.append("PAGE OVERRUNS ITS AREA p.%d by %.1f mm" % (pno, y - ROW_GAP - AREA[3]))
    if side_it:                                      # v12: beside the rows, right margin, top-aligned
        x1, ys = AREA[0] + max(rws) + GUT, y_top
        for it in side_it:
            w, h = wh(it)
            lg = crop_legend(it)                     # revision 30 Oct (G1): each side panel's legend under it
            s = max(0.05, min(own_s(it), (AREA[2] - x1) / w,
                              (AREA[3] - ys - CAP_H - legend_h(typo, lg, AREA[2] - x1)) / h))
            xs = AREA[2] - w * s
            ys += show(fitz, pg, typo, it, xs, ys, s, rep, missing) + CAP_H
            if lg:
                draw_legend_under(pg, typo, lg, xs, ys - 0.6, w * s, pno)
                ys += legend_h(typo, lg, w * s)
            if ys > AREA[3] + 0.5:
                typo.issues.append("SIDE COLUMN OVERRUNS ITS AREA p.%d by %.1f mm" % (pno, ys - AREA[3]))
    footer(pg, typo, pno, spec, [])
    return "p.%d %s: x%.2f · %s" % (pno, spec["title"], s_fit, "; ".join(rep))


def crop_legend(it):
    """revision 30 Oct (G1, M2): a crop's own legend entries, its marks in the booklet's source numbers ([] for a
    missing crop)"""
    if it is None or it[3] is None:
        return []
    out = []
    for e in (it[1] or {}).get("legend") or []:
        e = dict(e, label=renum(e.get("label", ""), it[0], it[1], it[2]))     # v18
        if all(e.get("label") != o.get("label") for o in out):
            out.append(e)
    return out


def legend_cols(typo, legend, w):
    """(columns, rows, column width mm) of a drawing's legend laid out under it, w mm wide"""
    if not legend:
        return 0, 0, 0.0
    lw = 6.0 + max(typo.width(e.get("label", ""), T["caption"]) for e in legend)
    ncol = max(1, min(len(legend), int((w + LEG_GAP) // (lw + LEG_GAP))))
    return ncol, -(-len(legend) // ncol), lw


def legend_h(typo, legend, w):
    """the height (mm) a drawing's legend takes under its caption, w mm wide"""
    n = legend_cols(typo, legend, w)[1]
    return n * LEG_ROW + 1.0 if n else 0.0


def draw_legend_under(pg, typo, legend, x, y, w, pno):
    """revision 30 Oct (G1): a drawing's legend under it from its left edge (y = the top of the legend band), in the
    columns its width holds: next to its drawing, aligned to it, never at the page bottom"""
    ncol, nrow, lw = legend_cols(typo, legend, w)
    if lw > w + 0.5:
        typo.issues.append("LEGEND WIDER THAN ITS DRAWING p.%d (%.0f mm, the drawing %.0f mm)" % (pno, lw, w))
    for i, e in enumerate(legend):
        legend_item(pg, typo, e, x + (i // nrow) * (lw + LEG_GAP), y + 3.0 + LEG_ROW * (i % nrow))


def panel_item(fitz, assets, key):
    """a plan key -> (key, block, path, clip) (v19: was expand's own item, now also for the P78.ALT page)"""
    if "||" in key:                                    # v15: "a||b": the first of these the scripts have written
        its = [panel_item(fitz, assets, k) for k in key.split("||")]
        return next((it for it in its if it[3] is not None), its[0])
    if key.startswith("slot|"):                        # v11: SLOT(text, w, h) of the plan
        _, w, h, text = key.split("|", 3)
        return (key, {"slot": text, "size_mm": (float(w), float(h))}, None, None)
    if _VARIANT[0]:                                    # revision 30 Oct (D1, D5): the _a / _b crop of this PDF where
        folder, _, bid = key.partition("/")             # its script wrote one, under the plan's own key
        vk = "%s_%s" % (bid, _VARIANT[0])
        if vk in ((assets.get(folder) or {}).get("blocks") or {}):
            _VARIANT_USED.add(folder + "/" + vk)
            return (key,) + tuple(panel_item_one(fitz, assets, folder + "/" + vk)[1:])
    return panel_item_one(fitz, assets, key)


_VARIANT_USED = set()   # revision 30 Oct: the _a / _b crops this build took (logged)


def panel_item_one(fitz, assets, key):
    """panel_item for one plain crop key (no "||", no slot, no variant)"""
    blk, path = resolve(assets, key)
    if not path:
        return (key, blk, None, None)
    page = sheet_doc(fitz, path)[int(blk.get("page", 0))]
    r = blk["rect_mm"]
    clip = fitz.Rect(r[0] * K, r[1] * K, r[2] * K, r[3] * K) & page.rect
    if not blk.get("scale_den"):                     # v4: a panel that states one scale in its words is to scale
        dens = set(int(m.group(1).replace(",", "")) for m in SCALE_WORD.finditer(page.get_text(clip=clip)))
        if len(dens) == 1:
            blk = dict(blk, scale_den=dens.pop())
    return (key, blk, path, clip)


def expand(fitz, spec, assets):
    """One plan entry -> [(spec, rows)]: keys resolved to (key, block, path, clip); each panel whole (v4)."""
    def item(key):
        return panel_item(fitz, assets, key)
    rows = [[item(k) for k in r] for r in spec["rows"]]
    rows = [r for r in ([it for it in r if not (it[0] in OPTIONAL_KEYS and it[3] is None)] for r in rows) if r]
    spec = dict(spec, _side=[item(k) for k in spec.get("side", [])],          # v12: side panels, title-band key map
                _key=item(spec["key"]) if spec.get("key") else None)
    if not rows:
        return []
    if spec.get("optional") and all(it[3] is None for r in rows for it in r):
        return []
    if spec.get("alone") and fit(rows) < 0.75 * min(fit([r]) for r in rows):   # v7: together only if both stay big
        return [(dict(spec, title=t), [r]) for t, r in zip(spec["alone"], rows)]
    return [(spec, rows)]


def cover(pg, typo, pages):
    x = colx(1)
    typo.line(pg, BOOK["course"].upper(), x, 16, T["kicker"], ACCENT, True)
    typo.line(pg, BOOK["hook"], x, 64, 48, ACCENT, True)
    y = 82
    for ln in typo.wrap(BOOK["title"], 7 * COL + 6 * GUT, T["part"], True):
        typo.line(pg, ln, x, y, T["part"], INK, True); y += 10
    typo.line(pg, BOOK["subtitle"], x, y + 2, T["sub"], INK)
    yb = 232
    for ln in BOOK["names"]:
        typo.line(pg, ln, x, yb, T["body"], INK); yb += LEAD["body"]
    typo.line(pg, BOOK["date"], x, yb + 4, T["caption"], INK2)
    # contents: parts and page titles, columns 9-12 (a title split over pages listed once)
    cx, cy = colx(9), 40
    typo.line(pg, "CONTENTS", cx, cy - 8, T["kicker"], ACCENT, True)
    last, lstage, seen = None, None, set()
    for no, sp in pages:
        t = re.sub(r" \(\d+/\d+\)$", "", sp.get("title", ""))
        if t in seen:
            continue
        seen.add(t)
        if sp.get("part") != last:
            last, lstage = sp.get("part"), None
            cy += 2
            typo.line(pg, (last + "  " + PARTS.get(last, "")).upper(), cx, cy, T["caption"], ACCENT, True); cy += 4.5
        if sp.get("stage") != lstage:                  # v11: the cycle step, once where it starts
            lstage = sp.get("stage")
            typo.line(pg, STAGES.get(lstage, "").lower(), cx + 8, cy, T["caption"], INK2); cy += 3.6
        typo.line(pg, "%02d" % no, cx, cy, T["caption"], INK2, True)
        typo.line(pg, t, cx + 12, cy, T["caption"], INK); cy += 4.0
    pg.draw_line((colx(1) * K, FOOT_RULE * K), ((PW - ML) * K, FOOT_RULE * K), color=hexrgb(RULE), width=0.25)


_F5_RX = []


def f5_rx():
    """v19 (F5): the plan's (F5_INTERNAL, F5_PUBLIC, F5_STRIP) patterns, compiled once"""
    if not _F5_RX:
        _F5_RX.extend([re.compile(p) for p in ps] for ps in (F5_INTERNAL, F5_PUBLIC, F5_STRIP))
        _F5_RX.append(re.compile(F5_STATUS))          # v20 (Aras 29 Oct 18:56): status words
    return _F5_RX


def split_top(t, sep=";"):
    """t split at sep outside brackets (the separators stay out)"""
    out, cur, depth = [], "", 0
    for ch in t:
        depth += (ch in "([") - (ch in ")]")
        if ch == sep and depth <= 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    return out + [cur]


def corn(t):
    """v19 (MIRAQUA 28 Oct, G11): "Corn (Mısır)", never maize, in the booklet's sources text; Wikimedia file names
    (File:... .jpg) and links stay as they are"""
    if not t or "aize" not in t:
        return t
    parts = re.split(r"(File:[^\n]*?\.(?:jpe?g|png|tiff?|gif|svg|webp)|\S*wikimedia\.org\S*)", t, flags=re.I)
    for k in range(0, len(parts), 2):
        p = re.sub(u"\\b[Mm]aize \\(Mısır\\)", u"Corn (Mısır)", parts[k])
        parts[k] = re.sub(r"\bmaize\b", "corn", re.sub(r"\bMaize\b", "Corn", p))
    return "".join(parts)


def public_src(t):
    """v19 (MIRAQUA 28 Oct, F5, Aras 28 Oct 11:38: "every [n] whose source is not public online (research cards,
    notes, decisions, chats, Begüm's page) goes"): a source text as the sources page prints it, or None when it cites
    our own working material (F5_INTERNAL) and names no public source (F5_PUBLIC). A kept text loses its ';' parts
    that only cite that material, and the brackets and register codes of F5_STRIP. Corn, not maize (G11).
    v20 (Aras 29 Oct 18:56, D13): every ';' part must name a public source (F5_PUBLIC), else it goes, our survey and
    our own readings and calculations too; None when no part is left; the status words (F5_STATUS) never print."""
    t = (t or "").strip()
    if not t or not F5_DROP:
        return corn(t)
    rin, rpub, rstrip, rstat = f5_rx()
    t = ";".join(s for s in split_top(t) if s.strip() and any(r.search(s) for r in rpub) and
                 re.sub(r"\W+", "", rstat.sub("", s)))
    if not t:
        return None
    for r in rstrip:
        t = r.sub("", t)
    t = re.sub(r"\s*,\s*(?=[;)]|$)", "", rstat.sub("", t))
    t = re.sub(r"\s{2,}", " ", t).strip(" ;,")
    return corn(t[:1].upper() + t[1:]) if t else None


def src_line(e):
    """"[n] text" -> the line the sources page prints (public_src), or None (F5)"""
    m = KEY_LINE.match(str(e or ""))
    if not m:
        return public_src(str(e or "")) or None
    t = public_src(m.group(2) or "")
    return "[%s] %s" % (m.group(1), t) if t else None


def plan_codes(assets):
    """v19 (MIRAQUA 28 Oct, P23.2 + N2): the technical source codes the masterplan's numbered list no longer prints,
    from its booklet results.json key "plan_codes" (a list of "n name: codes" lines, or of {"n", "name", "codes"}, or
    {n: codes / {"name", "codes"}}): ["n · name: codes", ...] with only the public ones (F5); [] when there are none"""
    a = assets.get(MP.rstrip("/")) or {}
    try:
        with open(os.path.join(a.get("_dir", ""), "results.json"), encoding="utf-8") as f:
            j_ = json.load(f)
    except Exception:
        return []
    d, ps = j_.get("plan_codes"), j_.get("plan_sources")
    if not d and isinstance(ps, dict):                    # masterplan v27 writes "plan_sources" (pl28_plan_sources)
        d = [{"n": m_.get("n"), "name": m_.get("name"),
              "codes": [s_.get("text", "") for s_ in m_.get("sources") or [] if s_.get("kind") == u"public online"]}
             for m_ in ps.get("markers") or []] + \
            [{"n": l_.get("id"), "name": u"left as it is", "codes": l_.get("sources") or []}
             for l_ in ps.get("left_as_is") or []]
    if isinstance(d, dict):
        d = [dict(v, n=k) if isinstance(v, dict) else {"n": k, "codes": v} for k, v in
             sorted(d.items(), key=lambda kv: (int(kv[0]) if str(kv[0]).isdigit() else 999, str(kv[0])))]
    out = []
    for e in d or []:
        if not isinstance(e, dict):
            t = public_src(str(e))
            if t:
                out.append(t)
            continue
        codes = e.get("codes") or e.get("source") or e.get("sources") or ""
        codes = [str(c) for c in codes] if isinstance(codes, (list, tuple)) else \
            [c for c in re.split(r"\s*[,;]\s*", str(codes)) if c]
        codes = [c for c in (public_src(c) for c in codes) if c]
        if codes:
            head = " · ".join(str(v) for v in (e.get("n"), e.get("name")) if v not in (None, ""))
            out.append((head + ": " if head else "") + ", ".join(codes))
    return out


def sheet_sources(fitz, assets):
    """[(heading, [entries])]: each sheet page's own source key. v10 (Aras 27 Oct: source footers go): first the
    key a script writes into its blocks.json "sheet_sources" ({page or "pdf#page": ["[1] ...", ...]}), else the
    key as the sheet prints it ("Sources by number: [1] ... [2] ..." or lines starting [n], visible or not).
    v19 (F5, G11): public online sources only, corn not maize (src_line)."""
    out, done = [], set()
    for pat in SOURCE_SHEETS:
        folder, _, name = pat.partition("/")
        keyed = (assets.get(folder) or {}).get("sheet_sources") or {}
        if keyed:
            if folder not in done:
                done.add(folder)
                for k in sorted(keyed, key=lambda k_: str(k_)):
                    ents = [e for e in (src_line(e_) for e_ in keyed[k] if e_) if e]
                    if ents:
                        out.append((SCRIPT_OF.get(folder, folder) + ("" if len(keyed) == 1 else " · page %d" % (int(k) + 1) if str(k).isdigit()
                                                                    else " · " + re.sub(r"\.pdf(#\d+)?$", "", str(k)).replace("_", " ")), ents))
            continue
        path = find_pdf(folder, name)
        if not path:
            continue
        d = sheet_doc(fitz, path)
        for i, page in enumerate(d):
            txt = []
            for b in page.get_text("blocks"):
                t = re.sub(r"\s+", " ", b[4]).strip()
                if "Sources by number:" in t:
                    txt.append(t.split("Sources by number:", 1)[1])
                elif re.match(r"\[\d+\] ", t):
                    txt.append(t)
            ents = [e for e in (src_line(e_.strip()) for e_ in re.split(r"\s(?=\[\d+\] )", " " + " ".join(txt))
                                if e_.strip()) if e]
            if ents:
                head = SCRIPT_OF.get(folder, folder) + (" · page %d" % (i + 1) if len(d) > 1 else "")
                if "axonometric" in name:
                    head += " · axonometric"
                out.append((head, ents))
    return out


# ------------------------------------------------------------------ v18 sources: one numbering for the whole booklet
MARK = re.compile(u"\\[(\\d{1,3}(?:\\s*[,–-]\\s*\\d{1,3})*)\\]")              # one mark: [3] [7,8] [3-5]
MARKS = re.compile(u"\\[\\d{1,3}(?:\\s*[,–-]\\s*\\d{1,3})*\\](?:\\s*\\[\\d{1,3}(?:\\s*[,–-]\\s*\\d{1,3})*\\])*")
KEY_LINE = re.compile(r"^\s*\[(\d{1,3})\]\s*(.*\S)?")
WMARK = re.compile(u"(\\s*)" + MARK.pattern)         # v19: a mark with the space before it (F5: both go)
_SRC = []        # v18: this run's Sources (main), read by renum


def renum(s, key, blk, path):
    """v18: s with its [n] marks in the booklet's source numbers (unchanged when Sources is not working)"""
    if not s or not _SRC or "[" not in s:
        return s
    return _SRC[0].renum(s, _SRC[0].key_for(key.partition("/")[0], path, int((blk or {}).get("page", 0))))


# v21 (Aras 30 Oct 06:20): the scale figure sets the pages draw from (common/figures.py, library/figures_A1/INDEX.md);
# the high-res silhouettes come from Data/assets_hires.json (hr_sources)
BK_ASSET_SOURCES = [
    u"Scale figures: Wijayarathna S., Architectural human figures sketches (set 1), https://sashx.gumroad.com/l/gSAgZ",
    u"Scale figures: studio_articulation, Sketchy Human Figures 2, "
    u"https://learnarchitecture.online/products/sketchy-human-figures-2",
    u"Scale figures: studio_articulation, Sketchy Human Figures 3, "
    u"https://learnarchitecture.online/products/sketchy-human-figures-3"]


def cutout_sources():
    """T4 30 Oct (M12, D1 a): one line per cutout source in Data/cutouts/cutouts.json (optional "source" of an entry:
    author / title / URL), once each, in key order; [] when the file or the field is missing"""
    p_ = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "Data", "cutouts", "cutouts.json")
    try:
        with open(p_, encoding="utf-8") as f_:
            d_ = json.load(f_).get("cutouts") or {}
    except Exception:
        return []
    out = []
    for key, ents in sorted(d_.items()):
        for e_ in (ents if isinstance(ents, list) else [ents]):
            t = str((e_ or {}).get("source") or "").strip() if isinstance(e_, dict) else ""
            if t and t not in out:
                out.append(t)
    return [u"Cutout: " + t for t in out]


class Sources(object):
    """v18 (Aras 27 Oct, Prompt 8: "every [n] used exists, none are unused, numbering follows the new order"): every
    [n] mark the pages show (sheet words inside each crop, captions, legend names), read in page order, takes one
    booklet number: first use first, one number per source text (the board's drawings and sections sheets share a
    key). v19 (G9): each place a sheet page is shown gets its own copy (strip_copy): its marks rewritten in place (same
    size, colour and baseline, in the booklet's Arial; a longer number set smaller where the words after it would be
    hit) and nothing outside that crop. v19 (F5): a source not public online takes no number; its marks go."""
    def __init__(self, fitz, assets):
        self.fz = fitz
        self.assets = assets    # v19: for the photo credits and the masterplan's plan_codes (N2)
        self.f5 = []            # v19 (F5): the marks taken out, for the log
        self.numbered = []      # v19: the booklet's pages (collect), for the sources page's headings
        self.keys = {}          # key id -> {n: source text}
        self.glob = {}          # (key id, n) -> booklet number
        self.by_text = {}       # source text (normalised) -> booklet number
        self.order = []         # [(booklet number, key id, n, part, page, folder)]
        self.used = {}          # (sheet path, page index) -> [folder, [clips]] (clip None = the whole page)
        self.kid = {}           # (folder, path, page index) -> key id
        self.first = {}         # T4 30 Oct (M12): folder -> first booklet page showing it (credits in page order)
        self.log, self.n_tight = [], 0
        for folder, a in sorted(assets.items()):
            for k, ents in sorted(((a or {}).get("sheet_sources") or {}).items(), key=lambda kv: str(kv[0])):
                k = str(k)
                if "#" in k:                           # the board: "<sheet pdf>#<page>"
                    pdf, _, p_ = k.rpartition("#")
                    kid = (folder, os.path.basename(pdf), int(p_) if p_.isdigit() else None)
                elif k.isdigit():                      # a page of the script's sheet (one key = all its pages)
                    kid = (folder, None, int(k))
                else:
                    kid = (folder, os.path.basename(k), None)
                self.keys[kid] = self.entries(ents or [])

    @staticmethod
    def entries(ents):
        """["[1] text", ...] -> {1: "text", ...} (an entry without its number takes its place in the list)"""
        out = {}
        for i, e in enumerate([str(e_).strip() for e_ in ents if e_ and str(e_).strip()]):
            m = KEY_LINE.match(e)
            out.setdefault(int(m.group(1)) if m else i + 1, ((m.group(2) or "") if m else e).strip())
        return out

    def parsed(self, path, i):
        """the key a sheet page prints itself ("Sources by number: [1] ..." or lines starting [n], visible or not)"""
        kid = ("sheet", path, i)
        if kid not in self.keys:
            txt = []
            for b in sheet_doc(self.fz, path)[i].get_text("blocks"):
                t = re.sub(r"\s+", " ", b[4]).strip()
                if "Sources by number:" in t:
                    txt.append(t.split("Sources by number:", 1)[1])
                elif re.match(r"\[\d+\] ", t):
                    txt.append(t)
            self.keys[kid] = self.entries(re.split(r"\s(?=\[\d+\] )", " " + " ".join(txt)))
        return kid if self.keys[kid] else None

    def key_for(self, folder, path, i):
        """the key the marks of this sheet page refer to: the script's own (blocks.json "sheet_sources": per sheet PDF
        and page, per page, or one for all), else the one the sheet prints (this page, else the one page of this
        sheet or of the folder's SOURCE_SHEETS sheet that has one); ("none", folder) when there is none"""
        ck = (folder, path, i)
        if ck not in self.kid:
            pdf = os.path.basename(path or "")
            kid = next((k for k in ((folder, pdf, i), (folder, pdf, None), (folder, None, i)) if self.keys.get(k)),
                       None)
            own = [k for k in self.keys if k[0] == folder and self.keys[k]]
            if kid is None and len(own) == 1:
                kid = own[0]
            if kid is None and path:
                kid = self.parsed(path, i)
                cands = [path] + [p for p in (find_pdf(folder, pat.partition("/")[2]) for pat in SOURCE_SHEETS
                                              if pat.partition("/")[0] == folder) if p and p != path]
                for p in cands if kid is None else []:
                    hits = [k for k in (self.parsed(p, j) for j in range(len(sheet_doc(self.fz, p)))) if k]
                    if len(hits) == 1:
                        kid = hits[0]
                        break
            self.kid[ck] = kid or ("none", folder)
        return self.kid[ck]

    @staticmethod
    def nums(s):
        """"3" / "7,8" / "3-5" -> [3] / [7, 8] / [3, 4, 5]"""
        out = []
        for part in s.split(","):
            ab = [x for x in re.split(u"[–-]", part) if x.strip()]
            try:
                a, b = int(ab[0]), int(ab[-1])
            except (ValueError, IndexError):
                continue
            out += list(range(a, b + 1)) if 0 <= b - a <= 12 else [a, b]
        return out

    def invisible(self, page):
        """rects of the page's invisible words (render mode 3: e.g. the water balance's source key)"""
        try:
            return [self.fz.Rect(s_["bbox"]) for s_ in page.get_texttrace() if s_.get("type") == 3]
        except Exception:
            return []

    def lines_in(self, page, clip, inv=None):
        """the visible lines of words inside clip (None = the page) holding a "[", outside any printed source key
        (v19: inv = the page's invisible words when read before, page_text)"""
        inv, out = self.invisible(page) if inv is None else inv, []
        for b in page.get_text("dict", clip=clip)["blocks"]:
            lines = [("".join(s_["text"] for s_ in ln["spans"]), self.fz.Rect(ln["bbox"])) for ln in b.get("lines", [])]
            if any("Sources by number:" in t for t, _ in lines):
                continue
            out += [t for t, r in lines if "[" in t and not any(r.intersects(v) for v in inv)]
        return out

    def use(self, kid, n, part, pno, folder):
        if (kid, n) in self.glob:
            return
        t = (self.keys.get(kid) or {}).get(n)
        if t and public_src(t) is None:                # v19 (F5): not public online: no number, its marks go
            self.glob[(kid, n)] = 0
            self.f5.append(u"p.%02d [%d] (%s): %s" % (pno, n, SCRIPT_OF.get(folder, folder), t[:110]))
            return
        if not t:                                      # v20 (D13): no entry = nothing public to print: the mark goes
            self.glob[(kid, n)] = 0
            self.log.append("SOURCE MARK WITHOUT AN ENTRY p.%d [%d] (%s): taken off the page" % (
                pno, n, SCRIPT_OF.get(folder, folder)))
            return
        norm = re.sub(r"\W+", " ", t).strip().lower() if t else None
        if norm and norm in self.by_text:              # the same source under another sheet's number
            self.glob[(kid, n)] = self.by_text[norm]
            return
        g = len(self.order) + 1
        self.glob[(kid, n)] = g
        if norm:
            self.by_text[norm] = g
        self.order.append((g, kid, n, part, pno, folder))

    def collect(self, numbered):
        """pass 1: the marks of every page in page order -> booklet numbers; which parts of which sheet pages show"""
        self.numbered = numbered
        for pno, sp, rows in numbered:
            its = []
            if rows is None:
                folder, _, name = sp["sheet"].partition("/")
                path, i = find_pdf(folder, name), int(sp.get("page", 0))
                if path and i < len(sheet_doc(self.fz, path)):
                    its.append((folder, path, i, None, "", []))
            else:
                for key, blk, path, clip in [it for r in rows for it in r] + list(sp.get("_side") or []) + \
                        ([sp["_key"]] if sp.get("_key") else []):
                    if clip is not None:
                        its.append((key.partition("/")[0], path, int(blk.get("page", 0)), clip,
                                    blk.get("caption") or "", [e.get("label", "") for e in blk.get("legend") or []]))
            for folder, path, i, clip, cap, labels in its:
                self.used.setdefault((path, i), [folder, []])[1].append(clip)
                self.first.setdefault(folder, pno)
                kid = self.key_for(folder, path, i)
                inv = page_text(self.fz, path, i)[1]   # v19: read once per sheet page, not once per crop
                for t in self.lines_in(sheet_doc(self.fz, path)[i], clip, inv) + [cap] + labels:
                    for m in MARK.finditer(t):
                        for n in self.nums(m.group(1)):
                            self.use(kid, n, sp.get("part"), pno, folder)

    def renum(self, s, kid):
        """s with its marks in the booklet's numbers; v19 (F5): a mark whose sources all are not public online goes
        with the space before it, a mark with some keeps the others"""
        def one(m):
            ns = [self.glob.get((kid, n)) for n in self.nums(m.group(2))]
            if not ns or None in ns:
                return m.group(0)
            ns = sorted(set(n for n in ns if n))
            if not ns:
                return ""
            if len(ns) > 2 and ns[-1] - ns[0] == len(ns) - 1:
                return m.group(1) + "[%d-%d]" % (ns[0], ns[-1])
            return m.group(1) + "[%s]" % (", " if ", " in m.group(2) else ",").join(str(n) for n in ns)
        return WMARK.sub(one, s)

    def build(self):
        """pass 2 (v19, G9): the copy of every place a sheet page is shown (strip_copy), made now, its marks renumbered"""
        for (path, i), (folder, clips) in self.used.items():
            for clip in clips:
                ck = (path, i, clip_key(clip))
                if ck not in _COPY:
                    _COPY[ck] = strip_copy(self.fz, path, i, clip, self)

    def groups(self):
        """[(theme heading, ["[n] text", ...])] in booklet order, for sources_page. v19: public online sources only (F5)
        and corn, not maize (G11) (public_src); then (N2) the photo credits and data notes of the sheets shown that no
        page cites by a number (plan ALWAYS_LIST; blocks.json "photo_credits"), once each, and the technical source
        codes the masterplan's list no longer prints (plan_codes), headed by that page's title (N1)"""
        def ck(t):                                    # one photo = one credit (its Commons page id)
            m = re.search(r"curid=(\d+)", t or "")
            return ("id", m.group(1)) if m else ("t", re.sub(r"\W+", " ", t or "").strip().lower())
        out, last, printed = [], object(), set()
        for g, kid, n, part, pno, folder in self.order:
            if part != last:
                last = part
                out.append(((part + "  " + PARTS.get(part, "")).upper() if part else u"COVER", []))
            t = (self.keys.get(kid) or {}).get(n)
            t = public_src(t) if t else t
            printed.add(ck(t))
            out[-1][1].append(u"[%d] %s" % (g, t))
        pats, texts, extra = [re.compile(p) for p in ALWAYS_LIST], [], []
        for kid in sorted(set(self.kid.values()), key=str):
            texts += [t for n, t in sorted((self.keys.get(kid) or {}).items())
                      if (kid, n) not in self.glob and t and any(p.search(t) for p in pats)]
        shown = set(f for f, _ in self.used.values())
        # T4 30 Oct (M12): the scripts' photo credits in booklet page order (first page each sheet shows on), so the
        # p.20 photo credits moved off the heritage map print here with the others
        for f_, a in sorted(self.assets.items(), key=lambda kv: (self.first.get(kv[0], 999), str(kv[0]))):
            texts += [str(t) for t in (a or {}).get("photo_credits") or [] if t]
            try:                                      # T4 (M12): photo_credits.json beside blocks.json (masterplan
                with open(os.path.join((a or {}).get("_dir") or "", "photo_credits.json"), encoding="utf-8") as fh:
                    texts += [str(t) for t in json.load(fh).get("photo_credits") or [] if t]   # senses photos)
            except Exception:
                pass
            if f_ in shown:                           # v20 (WO-T5-1): registered public sources and photo credits
                texts += [str((v or {}).get("text") or "") for k, v in sorted(((a or {}).get("sources") or {}).items())
                          if re.match(ALWAYS_KEYS, str(k)) and isinstance(v, dict)]
        for t in texts:
            t = public_src(t)
            if t and ck(t) not in printed:
                printed.add(ck(t))
                extra.append(t)
        if extra:
            out.append((u"PHOTO CREDITS AND DATA NOTES", extra))
        codes = plan_codes(self.assets)
        if codes:
            title = next((sp.get("title", "") for _, sp, rows in self.numbered if rows and
                          any(it[0] == MP + "mp_plan" for r in rows for it in r)), u"Masterplan: an ecological corridor")
            out.append((u"SOURCES OF THE NUMBERED PLACES IN ‘%s’" % title.upper(), codes))
        assets = [public_src(t) or corn(t) for t in hr_sources() + BK_ASSET_SOURCES + cutout_sources()]
        if assets:                                    # v21 (Aras 30 Oct 06:20): every asset source once, under ASSETS
            out.append((u"ASSETS", assets))
        return out

    def report(self):
        kids = set(self.kid.values())
        left = sum(1 for k in kids for n in (self.keys.get(k) or {}) if (k, n) not in self.glob)
        return ("sources: %d cited, numbered in page order (one number per source); %d entries of the scripts' keys "
                "for these sheets not cited on any page, left out; %d not public online, their marks taken off the "
                "pages (F5, listed at the end of this log); %d marks set smaller to fit" % (
                    len(self.order), left, len(self.f5), self.n_tight))


def sources_page(pg, typo, pno, groups, head=u"Sources, by sheet"):
    """All sources on ONE page (Aras 25 Oct 21:54): each sheet's own key under its name, three columns, the type
    size lowered step by step until everything fits; only this page may go below 7 pt. v18: head = the page title
    (the booklet's one numbering: groups = themes)."""
    typo.line(pg, "SOURCES", colx(1), 12, T["kicker"], ACCENT, True)
    typo.line(pg, head, colx(1), 22, T["part"], INK, True)
    pg.draw_line((colx(1) * K, 25 * K), ((PW - ML) * K, 25 * K), color=hexrgb(RULE), width=0.25)
    cols = [colx(1), colx(5), colx(9)]
    y0, y1 = 31.0, FOOT_RULE - 3.0
    w = 4 * COL + 3 * GUT
    items = []
    for head, ents in groups:
        items.append((True, head))
        items += [(False, e) for e in ents]

    def layout(size):
        lead, gap = size * PT * 1.18, size * PT * 0.45
        out, ci, y = [], 0, y0 + size * PT
        for bold, t in items:
            lines = typo.wrap(t, w - 1.5, size, bold)
            need = len(lines) * lead + (gap * 2 if bold else 0)
            if y + need - lead > y1:
                ci, y = ci + 1, y0 + size * PT
                if ci >= len(cols):
                    return None
            if bold and y > y0 + size * PT + 0.1:
                y += gap * 2
            out.append((ci, y, lines, bold))
            y += len(lines) * lead + gap
        return out, lead
    size, res = T["caption"], None
    while size >= 3.0:
        res = layout(size)
        if res:
            break
        size = round(size - 0.25, 2)
    if not res:
        typo.issues.append("SOURCES DO NOT FIT ON ONE PAGE even at 3 pt")
        return
    rows, lead = res
    for ci, y, lines, bold in rows:
        for k_, ln in enumerate(lines):
            typo.line(pg, ln, cols[ci] + (1.5 if k_ else 0.0), y + k_ * lead, size, ACCENT if bold else INK, bold,
                      small_ok=True)
    if size < MIN_CAPTION:
        typo.notes.append("sources page set at %.2f pt to fit one page (%d entries)" % (size, len(items)))
    footer(pg, typo, pno, {"part": None}, [])


def flex_order(plan, typo):
    """v17: a spread opens on a left (even) page: when it would open on a right page and the page before it is marked
    flex, that page goes after the spread instead (plan index i = page i + 2: page 1 is the cover)."""
    for i in range(1, len(plan) - 1):
        if plan[i][0].get("spread") == "L" and i % 2 and plan[i - 1][0].get("flex"):
            typo.notes.append("page '%s' moved after the spread '%s' so the spread opens on a left page" % (
                plan[i - 1][0].get("title", ""), plan[i][0].get("title", "")))
            n = 2 if plan[i + 1][0].get("spread") == "R" else 1
            return plan[:i - 1] + plan[i:i + n] + [plan[i - 1]] + plan[i + n:]
    return plan


def pno_of(numbered, key=None, sheet=None, page=0):
    """v19: the page number (2 digits) of the page showing crop key, or sheet page; "" when no page does"""
    for pno, sp, rows in numbered:
        if (key and rows and any(it[0] == key for r in rows for it in r)) or \
                (sheet and rows is None and sp.get("sheet") == sheet and int(sp.get("page", 0)) == page):
            return "%02d" % pno
    return ""


def page_checks(doc, numbered, typo):
    """v19 (MIRAQUA 28 Oct): read back from the finished pages. G10 ("one number, one calculation"): a figure of the
    plan's FIGURE_CHECKS printed two ways on the booklet's pages (e.g. the frame 150.5 ha on p.02, 151 ha on p.21)
    is logged with every page of each value. N1: the cross-references the pages print still point right after the
    renumbering: "NEXT <theme letter> <theme>" names the next theme, "see '<title>'" a page title; a reference by
    page number is logged (pages are named by their titles). The sources page and the cover are not read."""
    last = len(doc)
    texts = {}
    for i, pg in enumerate(doc):
        if 0 < i < last - 1:
            try:
                texts[i + 1] = re.sub(r"\s+", " ", pg.get_text("text"))
            except Exception:
                texts[i + 1] = ""
    for name, unit, pats in FIGURE_CHECKS:
        seen = {}
        for pno, t in texts.items():
            for p in pats:
                for m in re.finditer(p, t):
                    seen.setdefault(m.group("v").replace(",", ""), set()).add(pno)
        if len(seen) > 1:
            typo.issues.append(u"ONE FIGURE, TWO VALUES (G10) %s: %s" % (name, u" · ".join(
                u"%s %s (p.%s)" % (v, unit, ", ".join("%02d" % p for p in sorted(ps))) for v, ps in sorted(seen.items()))))
        elif seen and len(list(seen.values())[0]) > 1:
            v, ps = list(seen.items())[0]
            typo.notes.append(u"G10 %s: %s %s on p.%s, the same everywhere" % (name, v, unit,
                                                                            ", ".join("%02d" % p for p in sorted(ps))))
    titles = dict((re.sub(r"\W+", " ", sp.get("title", "")).strip().lower(), pno) for pno, sp, _ in numbered)
    part_of = dict((pno, sp.get("part")) for pno, sp, _ in numbered)
    n_ok = 0
    for pno, t in sorted(texts.items()):
        for m in re.finditer(u"NEXT\\W{0,4}([A-E])\\b", t):
            nxt = next((part_of[p] for p in sorted(part_of) if p > pno and part_of[p] != part_of.get(pno)), None)
            if m.group(1) != nxt:
                typo.issues.append(u"CROSS-REFERENCE p.%02d: \"NEXT %s\", but the next theme is %s" % (
                    pno, m.group(1), nxt or "none"))
            else:
                n_ok += 1
        for m in re.finditer(u"(?i)\\bsee\\s+[‘'\"“]([^’'\"”]{3,80})[’'\"”]", t):
            if re.sub(r"\W+", " ", m.group(1)).strip().lower() not in titles:
                typo.issues.append(u"CROSS-REFERENCE p.%02d: see '%s', but no page has that title" % (pno, m.group(1)))
            else:
                n_ok += 1
        for m in re.finditer(r"(?i)\b(?:pp?\.|page) ?\d{1,2}\b(?! ?of\b)", t):
            typo.issues.append(u"CROSS-REFERENCE BY NUMBER p.%02d: \"%s\" (pages are renumbered: name the page by its "
                               u"title)" % (pno, m.group(0)))
    if n_ok:
        typo.notes.append("cross-references checked (N1): %d point to the right theme or title" % n_ok)


# ------------------------------------------------------------------ main
def main():
    """revision 30 Oct (D1, D5): the booklet built twice, ..._alt_a.pdf and ..._alt_b.pdf (BOOK_VARIANTS), each taking
    a crop's _a / _b version where its script wrote one (else the crop itself); one log for both"""
    t0 = time.time()
    rows = []
    for v in BOOK_VARIANTS:
        rows += build_variant(v)
    rows += bg_tidy_output(OUT_FOLDER, BK_ROOT)  # v10 (27 Oct): output/ = the PDF only, leftovers to cached/booklet/
    rows.append("%s %s, %.1f s" % (GH_LABEL, VERSION, time.time() - t0))
    return "\n".join(rows)


def variant_pdf(v):
    """the PDF name of variant v: Bergama_booklet_A3_alt_a.pdf"""
    root, ext = os.path.splitext(PDF_NAME)
    return "%s_alt_%s%s" % (root, v, ext) if v else PDF_NAME


def build_variant(variant):
    """one booklet PDF (variant "a" / "b", None = the plain one): its log rows"""
    import fitz                                   # PyMuPDF
    os.makedirs(OUT_DIR, exist_ok=True)
    _VARIANT[0] = variant
    _VARIANT_USED.clear()
    assets = load_assets()
    typo = Typo(fitz)
    doc = fitz.open()
    plan = []
    for spec in PAGES:
        if spec.get("sheet"):
            plan.append((spec, None))
        elif not FRAME_PAGES and all(k.startswith("slot|") for r in spec.get("rows", []) for k in r):
            typo.notes.append("page '%s' left out: its drawings are not made yet (frames only; PLAN FRAME_PAGES)" %
                              spec.get("title", ""))           # v18 (Prompt 8): no empty frame page in the booklet
        else:
            plan += expand(fitz, spec, assets)
    plan = flex_order(plan, typo)
    numbered = [(i + 2, sp, rows) for i, (sp, rows) in enumerate(plan)]   # page 1 = cover + contents
    _TOTAL[0] = len(numbered) + 2                   # revision 30 Oct (G2): cover + pages + sources, the counter's total
    _COPY.clear()
    _PAGE_TXT.clear()
    G9_STATS.update(copies=0, lines=0, chars=0, images=0, failed=[])
    del _SRC[:]
    srcs = Sources(fitz, assets)                    # v18: one source numbering for the booklet, in page order
    try:
        srcs.collect(numbered)
        srcs.build()
        _SRC.append(srcs)
        typo.notes.append(srcs.report())
        typo.issues += srcs.log
    except Exception as ex:
        _COPY.clear()
        typo.issues.append("SOURCES NOT RENUMBERED (%s: %s): marks and sources page by sheet, as before v18" %
                           (type(ex).__name__, ex))
    cover(frame_page(fitz, doc, typo), typo, [(n, sp) for n, sp, _ in numbered])
    missing, rep = set(), []
    for pno, sp, rows in numbered:                   # v11: a spread opens on a left (even) page
        if sp.get("spread") == "L" and pno % 2:
            typo.issues.append("SPREAD STARTS ON A RIGHT PAGE p.%d %s" % (pno, sp.get("title", "")))
    for pno, sp, rows in numbered:
        rep.append(sheet_page(fitz, doc, typo, pno, sp) if rows is None else
                   panel_page(fitz, doc, typo, pno, sp, rows, assets, missing))
    sources_page(frame_page(fitz, doc, typo), typo, len(numbered) + 2,
                 *((srcs.groups(), u"Sources, in page order") if _SRC else (sheet_sources(fitz, assets),)))
    text_check(fitz, doc, typo, set(n - 1 for n, sp, rows in numbered if rows is None))
    page_checks(doc, numbered, typo)                 # v19: G10 figures, N1 cross-references
    typo.notes.append("G9: %d crops each shown from its own copy of its sheet page; taken out of the copies: %d lines "
                      "and %d letters of words outside them, %d images wholly outside, the line art lying wholly "
                      "outside%s" % (G9_STATS["copies"], G9_STATS["lines"], G9_STATS["chars"], G9_STATS["images"],
                                     "" if G9_LINE_ART else " (off: G9_LINE_ART)"))
    typo.issues += ["G9 COPY FAILED, the whole sheet page shown: %s" % f for f in G9_STATS["failed"]]
    doc.subset_fonts()
    out = os.path.join(OUT_DIR, variant_pdf(variant))
    doc.save(out, garbage=3, deflate=True)
    n = doc.page_count
    doc.close()
    if n != _TOTAL[0]:
        typo.issues.append("PAGE COUNTER: %d pages built, the counter says %d" % (n, _TOTAL[0]))
    rows = ["%s  %s  (%d pages, font %s)" % (out, time.strftime("%H:%M:%S"), n, typo.fam)]
    if variant:
        rows.append("variant %s: %d crops taken as their _%s version%s" % (
            variant, len(_VARIANT_USED), variant, (": " + ", ".join(sorted(_VARIANT_USED))) if _VARIANT_USED else ""))
    for name in sorted(assets):
        rows.append("assets %s: %s" % (name, assets[name].get("_error") or assets[name]["_time"]))
    for m in sorted(missing):
        rows.append("MISSING drawings of %s: placeholders left" % SCRIPT_OF.get(m, m))
    rows += rep + typo.notes
    rows += typo.issues[:40] + (["... %d more" % (len(typo.issues) - 40)] if len(typo.issues) > 40 else [])
    if _SRC and _SRC[0].f5:                       # v19 (F5): Aras's list of figures left without a public source
        rows += ["F5 · sources not public online: left off the sources page, their marks taken off the pages; the "
                 "figures they backed have no public source now (page, the sheet's own mark, its source):"]
        rows += ["  " + t for t in _SRC[0].f5]
    return rows


def text_check(fitz, doc, typo, skip=()):
    """The booklet's own text, read back from the PDF (cover, sources page, title and footer bands, captions): none may
    leave the page's margins or overlap another line. The sheets' words are theirs, as the sheets print them."""
    last = len(doc) - 1
    for i, pg in enumerate(doc):
        if i in skip:
            continue
        own = i in (0, last)
        boxes = []
        for b in pg.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                t = "".join(sp["text"] for sp in ln["spans"]).strip()
                if t:
                    r = fitz.Rect(ln["bbox"])
                    sz = max(sp["size"] for sp in ln["spans"])
                    r = fitz.Rect(r.x0, r.y1 - sz * 0.95, r.x1, r.y1 - sz * 0.2) if r.height > sz * 0.5 else r
                    if own or r.y1 < 27 * K or r.y0 > (FOOT_RULE - 1) * K or \
                            any(sp["size"] == T["caption"] for sp in ln["spans"]):
                        boxes.append((r, t))
        lim = fitz.Rect(ML * K * 0.5, MT * K * 0.5, (PW - ML * 0.5) * K, (PH - MB * 0.5) * K)
        for r, t in boxes:
            if not lim.contains(r):
                typo.issues.append("TEXT OFF THE PAGE p.%d: %s" % (i + 1, t[:40]))
        n = 0
        for a in range(len(boxes)):
            ra = boxes[a][0]
            for b_ in range(a + 1, len(boxes)):
                rb = boxes[b_][0]
                ov = ra & rb
                if ov.is_empty or ov.width < 0.5 or ov.height < 0.5:
                    continue
                if ov.width * ov.height > 0.15 * min(ra.width * ra.height, rb.width * rb.height):
                    n += 1
                    if n <= 3:
                        typo.issues.append("TEXT OVERLAPS TEXT p.%d: \"%s\" / \"%s\"" % (i + 1, boxes[a][1][:25],
                                                                                    boxes[b_][1][:25]))
        if n > 3:
            typo.issues.append("TEXT OVERLAPS TEXT p.%d: %d more" % (i + 1, n - 3))


def chain_fire(v, key):
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


# ---- Grasshopper wiring (same in every script; never define a function named run: it would hide the input) ----
if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    # v19: a setting in capitals (MERGE_21_22, F5_DROP, G9_LINE_ART = True) is never the Button
    _pressed = any(v is True for k, v in list(globals().items())
                   if not k.startswith("_") and not k.isupper() and isinstance(v, bool) and
                   k not in ("True", "False", "rhino_bake", "done")) or \
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
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:   # v10.1 (Aras 27 Oct 15:35): a newly pasted version shows itself at once,
        for _s in ("_log", "_status", "_done"):   # idle, without the old run's time or log
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to build " + " and ".join(
        os.path.join(OUT_DIR, variant_pdf(v_)) for v_ in BOOK_VARIANTS))
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
else:
    print(write_log(main()))
