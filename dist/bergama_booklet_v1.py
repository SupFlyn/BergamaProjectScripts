# -*- coding: utf-8 -*-
# r: pymupdf==1.26.5
"""Bergama Group 6: A3 BOOKLET ASSEMBLER (25 Oct 2026). Rules: scripts/_template/SCRIPT_STANDARD.md §8; grid and type:
booklet/design-language.md (project folder).
Builds ONE multi-page landscape A3 PDF (420 x 297 mm) from the assets the other scripts write, with live text.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file. The first run installs PyMuPDF 1.26.5 (the
"# r:" line above; needs internet once).
  input  run   Button
  output log   the last run's report: pages, missing assets, text that did not fit, repeated text
  output done  "done HH:MM:SS.ss · N s" (for the one-click chain: wire the last script's done into run)
Reads  ~/Downloads/Bergama/output/<script folder>/booklet/blocks.json (+ the vector PDFs it names): each script's assets
       ~/Downloads/Bergama/booklet_images/<name>.jpg|png: photos/visuals for the image frames (optional)
Writes ~/Downloads/Bergama/output/bergama_booklet/Bergama_booklet_A3.pdf
       ~/Downloads/Bergama/output/bergama_booklet/booklet_slots.json: every block's frame size in mm (scripts draw to it)
A missing asset leaves a labelled placeholder frame naming the script, so the booklet always builds.
All text is written by this script with one embedded TrueType font (Arial on Windows), whole lines, never outlined.
"""
import os, re, time, json

# ---- SETTINGS ----
VERSION = "v1"
GH_LABEL = "Booklet"
OUT_FOLDER = "bergama_booklet"
LOG_NAME = "bergama_booklet_log.txt"
PDF_NAME = "Bergama_booklet_A3.pdf"
FONT = "Arial"                               # "Arial" (every Windows PC) or "Inter" (if installed)

BERGAMA = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA, "logs")
IMG_DIR = os.path.join(BERGAMA, "booklet_images")
ASSET_ROOT = os.path.join(BERGAMA, "output")

# ---- GRID (design-language.md: all values in mm, origin top-left) ----
PW, PH = 420.0, 297.0
ML, MT, MB = 14.0, 12.0, 12.0                # left/right margin, top, bottom
COLS, COL, GUT = 12, 29.0, 4.0               # 14 + 12 x 29 + 11 x 4 + 14 = 420
BASE = 4.0                                   # baseline grid, from y = 12
ROW_Y0, ROWS, ROW_H = 36.0, 4, 56.0          # content rows 36-92, 96-152, 156-212, 216-272 (4 mm gutters)
FOOT_RULE, FOOT_B1, FOOT_B2 = 276.0, 280.0, 284.0
PT = 25.4 / 72.0                             # mm per point
K = 72.0 / 25.4                              # points per mm

# ---- TYPE (pt; size follows design importance) ----
T = dict(title=40, part=24, figure=24, sub=14, statement=13, body=9.5, caption=7.5, label=7.5, kicker=8, pageno=14)
LEAD = dict(title=16.0, part=10.0, statement=6.0, sub=6.0, body=4.0, caption=3.2, label=3.2)   # mm
MIN_BODY, MIN_CAPTION = 9.0, 7.0
MEASURE = 110.0                              # longest body line, mm (~65 characters of 9.5 pt Arial; brief: 50-75)

# ---- COLOUR (palette v1.4 core roles; contrast on white checked in design-language.md) ----
INK, INK2, ACCENT = "4A3F35", "6B645B", "8B3A3F"
RULE, FRAME, PAPER = "B0AC9C", "D8D5CC", "FFFFFF"

# ---- BOOKLET PLAN (page order, page titles, key statements, which asset goes in which frame) ----
# One place for page-level text = no repetition. Asset keys are "<script output folder>/<block id>": the block comes from
# that script's output/<folder>/booklet/blocks.json. {src:key} marks become [n] (one numbering for the booklet).
BOOK = dict(
    title=u"From stream corridor to hydrological commons",
    subtitle=u"Selinos stream edge, Bergama",
    project=u"SELİNOS STREAM EDGE · BERGAMA",
    group_line=u"ARCH 4410 Architectural Design Studio V · Group 6",
    course=u"Yaşar University · ARCH 4410 Architectural Design Studio V · 2026-2027 Fall",
    names=[u"Aras Özkaymakcı", u"Begüm Arslan", u"Nil Çetin"],
    date=u"October 2026",
)

PARTS = {"A": u"Site as it is", "B": u"Water", "C": u"Proposal"}

# frames on the 12-column x 4-row grid: (first column, last column, first row, last row)
TEMPLATES = {
    "map":      {"side": (1, 3, 1, 4), "hero": (4, 12, 1, 4)},
    "map_r":    {"hero": (1, 9, 1, 4), "side": (10, 12, 1, 4)},
    "two":      {"a": (1, 6, 1, 3), "b": (7, 12, 1, 3), "strip": (1, 12, 4, 4)},
    "three":    {"a": (1, 4, 1, 3), "b": (5, 8, 1, 3), "c": (9, 12, 1, 3), "strip": (1, 12, 4, 4)},
    "sections": {"s1": (1, 12, 1, 1), "s2": (1, 12, 2, 2), "s3": (1, 12, 3, 3), "s4": (1, 12, 4, 4)},
    "sections2": {"s1": (1, 12, 1, 2), "s2": (1, 12, 3, 4)},
    "grid8":    dict(("g%d" % (i + 1), (1 + 3 * (i % 4), 3 + 3 * (i % 4), 1 + 2 * (i // 4), 2 + 2 * (i // 4))) for i in range(8)),
    "tiles":    {"strip": (1, 12, 1, 1), "hero": (1, 8, 2, 4), "side": (9, 12, 2, 4)},
    "full":     {"hero": (1, 12, 1, 4)},
}

SCRIPT_OF = {   # output folder -> script, named on placeholders and in the log
    "selinus_board": u"selinus_board (MainBoard)",
    "bergama_water_board": u"bergama_water_board (WaterBoard)",
    "Bergama_water_balance_analysis": u"bergama_water_balance (WaterBalance)",
    "bergama_masterplan": u"bergama_masterplan (MasterPlan)",
    "Bergama_city_link_analysis": u"bergama_city_link (CityLink)",
    "Bergama_agriculture_alternatives": u"bergama_agriculture_alternatives (AgriCulture)",
    "bergama_proposal_sections": u"bergama_proposal_sections (ProposalSections)",
}

PLAN_SOURCES = {}   # sources used by page-level text below (scripts bring their own in blocks.json)

PLAN = [
    # ---------------- A  SITE AS IT IS
    dict(id="A1", part="A", template="map", title=u"What is there",
         statement=u"",
         slots={"side": "selinus_board/a1_side", "hero": "selinus_board/plan01"}),
    dict(id="A2", part="A", template="grid8", title=u"Layers of the site",
         statement=u"",
         slots=dict(("g%d" % i, "selinus_board/d%d" % i) for i in range(1, 9))),
    dict(id="A3", part="A", template="map_r", title=u"How people use it",
         statement=u"",
         slots={"hero": "selinus_board/plan07", "side": "selinus_board/a3_side"}),
    dict(id="A4", part="A", template="sections", title=u"The stream edge in section",
         statement=u"",
         slots={"s1": "selinus_board/t1", "s2": "selinus_board/t2", "s3": "selinus_board/t3", "s4": "selinus_board/t4"}),
    dict(id="A5", part="A", template="sections", title=u"The stream edge in section",
         statement=u"",
         slots={"s1": "selinus_board/t5", "s2": "selinus_board/t6", "s3": "selinus_board/t7", "s4": "selinus_board/s1_axo"}),
    dict(id="A6", part="A", template="tiles", title=u"Comfort through the year",
         statement=u"",
         slots={"strip": "selinus_board/climate_tiles", "hero": "selinus_board/t8_utci", "side": "selinus_board/a6_side"}),
    # ---------------- B  WATER
    dict(id="B1", part="B", template="tiles", title=u"The year of the water",
         statement=u"",
         slots={"strip": "bergama_water_board/w1_tiles", "hero": "bergama_water_board/w1_year", "side": "bergama_water_board/w1_side"}),
    dict(id="B2", part="B", template="sections2", title=u"River height at the surveyed cuts",
         statement=u"",
         slots={"s1": "bergama_water_board/w2a_cuts", "s2": "bergama_water_board/w2b_s4"}),
    dict(id="B3", part="B", template="tiles", title=u"How much water to hold",
         statement=u"",
         slots={"strip": "Bergama_water_balance_analysis/tiles", "hero": "Bergama_water_balance_analysis/balance_chart",
                "side": "bergama_water_board/w4_cubes"}),
    dict(id="B4", part="B", template="three", title=u"Collect, clean, hold",
         statement=u"",
         slots={"a": "bergama_water_board/chain", "b": "bergama_water_board/w6_cleaning", "c": "bergama_water_board/w3b_planting",
                "strip": "bergama_water_board/w7_destination"}),
    # ---------------- C  PROPOSAL
    dict(id="C1", part="C", template="full", title=u"Masterplan",
         statement=u"",
         slots={"hero": "bergama_masterplan/whole_site"}),
    dict(id="C2", part="C", template="map", title=u"Masterplan: the water edge",
         statement=u"",
         slots={"side": "bergama_masterplan/zoom_side", "hero": "bergama_masterplan/zoom_1000"}),
    dict(id="C3", part="C", template="map_r", title=u"Connection to the city",
         statement=u"",
         slots={"hero": "Bergama_city_link_analysis/spine_plan", "side": "Bergama_city_link_analysis/stops"}),
    dict(id="C4", part="C", template="two", title=u"Water for the farmland",
         statement=u"",
         slots={"a": "Bergama_agriculture_alternatives/alt1", "b": "Bergama_agriculture_alternatives/alt3",
                "strip": "Bergama_agriculture_alternatives/tiles"}),
    dict(id="C5", part="C", template="sections2", title=u"Proposal sections",
         statement=u"",
         slots={"s1": "bergama_proposal_sections/p1_upstream", "s2": "bergama_proposal_sections/p2_k4"}),
    dict(id="C6", part="C", template="sections2", title=u"Proposal sections",
         statement=u"",
         slots={"s1": "bergama_proposal_sections/p3_k5", "s2": "bergama_proposal_sections/p4_downstream"}),
    dict(id="C7", part="C", template="tiles", title=u"Four seasons",
         statement=u"",
         slots={"strip": "bergama_water_board/season_tiles", "hero": "bergama_water_board/season_matrix",
                "side": "bergama_water_board/season_side"}),
]


def colx(c):
    return ML + (c - 1) * (COL + GUT)


def roww(r):
    return ROW_Y0 + (r - 1) * (ROW_H + GUT)


def slot_rect(c1, c2, r1, r2):
    """x, y, w, h in mm of a block spanning columns c1-c2 and rows r1-r2."""
    x, y = colx(c1), roww(r1)
    return x, y, (c2 - c1 + 1) * COL + (c2 - c1) * GUT, (r2 - r1 + 1) * ROW_H + (r2 - r1) * GUT


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
        self.issues, self.seen = [], {}

    def width(self, s, size, bold=False):
        return self.F[bold].text_length(s, fontsize=size) * PT

    def wrap(self, s, w, size, bold=False):
        out = []
        for para in str(s).split("\n"):
            line = ""
            for word in para.split(" "):
                t = (line + " " + word).strip()
                if line and self.width(t, size, bold) > w:
                    out.append(line); line = word
                else:
                    line = t
            out.append(line)
        return out

    def line(self, page, s, x, y, size, col=INK, bold=False, align="L"):
        """One line of live text; (x, y) = left (or centre/right) end of the baseline, mm."""
        if not s:
            return
        if size < MIN_CAPTION:
            self.issues.append("TYPE BELOW 7 pt (%.1f): %s" % (size, s[:40]))
        if align != "L":
            wd = self.width(s, size, bold)
            x -= wd / 2 if align == "C" else wd
        page.insert_text((x * K, y * K), s, fontname="FB" if bold else "FR", fontsize=size, color=hexrgb(col))

    def block(self, page, pno, s, x, y, w, size, lead, col=INK, bold=False, max_y=None, where=""):
        """Wrapped text from baseline y; stops at max_y and reports what did not fit. Returns the next baseline."""
        if not s:
            return y
        key = re.sub(r"\s+", " ", str(s).strip().lower())
        if len(key) > 24:
            if key in self.seen and self.seen[key] != pno:
                self.issues.append("REPEATED TEXT p.%s and p.%s: %s" % (self.seen[key], pno, str(s)[:50]))
            self.seen.setdefault(key, pno)
        lines = self.wrap(s, w, size, bold)
        for i, ln in enumerate(lines):
            if max_y is not None and y > max_y + 0.01:
                self.issues.append("TEXT DOES NOT FIT p.%s %s: %d of %d lines cut (\"%s...\")" %
                                   (pno, where, len(lines) - i, len(lines), ln[:30]))
                break
            self.line(page, ln, x, y, size, col, bold)
            y += lead
        return y


# ------------------------------------------------------------------ assets
def load_assets():
    """{script folder: blocks.json dict (with its folder)} for every script that wrote booklet assets."""
    found = {}
    if not os.path.isdir(ASSET_ROOT):
        return found
    for name in sorted(os.listdir(ASSET_ROOT)):
        p = os.path.join(ASSET_ROOT, name, "booklet", "blocks.json")
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


class Sources(object):
    """One numbering for the whole booklet: {src:key} in any text -> [n]; the list is printed once, on the last page."""
    def __init__(self, assets):
        self.defs, self.order = {}, []
        for d in [PLAN_SOURCES] + [a.get("sources") or {} for a in assets.values()]:
            for k, v in d.items():
                self.defs.setdefault(k, v)

    def num(self, key):
        if key not in self.defs:
            return "[?%s]" % key
        if key not in self.order:
            self.order.append(key)
        return "[%d]" % (self.order.index(key) + 1)

    def sub(self, s):
        return re.sub(r"\{src:([\w.-]+)\}", lambda m: self.num(m.group(1)), str(s)) if s else s


# ------------------------------------------------------------------ page parts
def frame_page(fitz, doc, typo):
    pg = doc.new_page(width=PW * K, height=PH * K)
    pg.insert_font(fontname="FR", fontfile=typo.freg)
    pg.insert_font(fontname="FB", fontfile=typo.fbold)
    return pg


def header(pg, typo, src, pno, spec):
    part = PARTS.get(spec.get("part"), "")
    typo.line(pg, (spec.get("part", "") + "   " + part).upper(), colx(1), 16, T["kicker"], ACCENT, True)
    typo.line(pg, src.sub(spec.get("title", "")), colx(1), 32, T["title"], INK, True)
    st = src.sub(spec.get("statement", ""))
    if st:
        x, _, w, _ = slot_rect(8, 12, 1, 1)
        lines = typo.wrap(st, w, T["statement"])
        if len(lines) > 3:
            typo.issues.append("STATEMENT OVER 3 LINES p.%s: %s" % (pno, st[:40]))
            lines = lines[:3]
        y = 32 - LEAD["statement"] * (len(lines) - 1)
        for ln in lines:
            typo.line(pg, ln, x, y, T["statement"], INK)
            y += LEAD["statement"]
    pg.draw_line((colx(1) * K, 34 * K), ((PW - ML) * K, 34 * K), color=hexrgb(RULE), width=0.25)


def footer(pg, typo, pno, spec, legend):
    pg.draw_line((colx(1) * K, FOOT_RULE * K), ((PW - ML) * K, FOOT_RULE * K), color=hexrgb(RULE), width=0.25)
    typo.line(pg, BOOK["project"], colx(1), FOOT_B1, T["caption"], INK, True)
    typo.line(pg, BOOK["group_line"], colx(1), FOOT_B2, T["caption"], INK2)
    typo.line(pg, "%02d" % pno, PW - ML, FOOT_B2 + 0.6, T["pageno"], ACCENT, True, "R")
    part = PARTS.get(spec.get("part"), "")
    if part:
        typo.line(pg, part.upper(), PW - ML - 12, FOOT_B2, T["caption"], INK2, True, "R")
    # legend: same place on every page (columns 4-10 of the footer band), drawn samples + plain names
    x0, x1 = colx(4), colx(10) + COL
    x, y = x0, FOOT_B1
    for it in legend or []:
        w = 4.0 + 1.5 + typo.width(it.get("label", ""), T["caption"]) + 5.0
        if x + w > x1:
            x, y = x0, y + 4.0
            if y > FOOT_B2:
                typo.issues.append("LEGEND TOO LONG p.%s" % pno)
                break
        c = hexrgb(it.get("colour", INK))
        r = (x * K, (y - 2.6) * K, (x + 4.0) * K, (y + 0.2) * K)
        kind = it.get("kind", "fill")
        if kind == "line":
            pg.draw_line((x * K, (y - 1.2) * K), ((x + 4.0) * K, (y - 1.2) * K), color=c, width=it.get("width", 1.2))
        elif kind == "dot":
            pg.draw_circle(((x + 2.0) * K, (y - 1.2) * K), 1.3 * K, color=None, fill=c)
        else:
            pg.draw_rect(r, color=None, fill=c)
        typo.line(pg, it.get("label", ""), x + 5.5, y, T["caption"], INK)
        x += w


def placeholder(pg, typo, rect, text):
    x, y, w, h = rect
    pg.draw_rect((x * K, y * K, (x + w) * K, (y + h) * K), color=hexrgb(FRAME), width=0.5, dashes="[2 2] 0")
    typo.line(pg, text, x + w / 2, y + h / 2, T["body"], INK2, False, "C")


def put_drawing(fitz, pg, typo, pno, rect, blk, adir, src, sid):
    x, y, w, h = rect
    cap_h = 5.0 if (blk.get("caption") or blk.get("scale_den")) else 0.0
    dh = h - cap_h
    path = os.path.join(adir, blk.get("pdf", ""))
    if not os.path.isfile(path):
        placeholder(pg, typo, (x, y, w, dh), "missing " + blk.get("pdf", "?"))
        return
    s = fitz.open(path)
    sp = s[blk.get("page", 0)]
    sw, sh = sp.rect.width / K, sp.rect.height / K
    f = min(w / sw, dh / sh)
    if abs(f - 1) > 0.01:
        typo.issues.append("SCALED p.%s %s: drawing %.0f x %.0f mm made for another frame, x%.2f (frame %.0f x %.0f)" %
                           (pno, sid, sw, sh, f, w, dh))
    tgt = fitz.Rect(x * K, y * K, (x + sw * f) * K, (y + sh * f) * K)
    pg.show_pdf_page(tgt, s, blk.get("page", 0))
    for lb in blk.get("labels") or []:               # labels as live text, positions in mm from the drawing's top-left
        size = max(T["label"], float(lb.get("size", T["label"])))
        lx, ly = x + lb["x"] * f, y + lb["y"] * f
        typo.line(pg, src.sub(lb.get("text", "")), lx, ly, size, lb.get("colour", INK), bool(lb.get("bold")),
                  lb.get("anchor", "L"))
    cap = src.sub(blk.get("caption", ""))
    if blk.get("scale_den"):
        cap = (cap + "   " if cap else "") + "1:{:,}".format(int(round(blk["scale_den"] / f, -1)))
    typo.line(pg, cap, x, y + h - 1.0, T["caption"], INK2)


def put_text(pg, typo, pno, rect, blk, src, sid):
    x, y, w, h = rect
    w = min(w, MEASURE)
    yb = y + 5.0
    if blk.get("heading"):
        yb = typo.block(pg, pno, src.sub(blk["heading"]), x, yb, w, T["sub"], LEAD["sub"], INK, True, y + h, sid) + 1.0
    if blk.get("body"):
        yb = typo.block(pg, pno, src.sub(blk["body"]), x, yb, w, T["body"], LEAD["body"], INK, False, y + h, sid)
    for b in blk.get("bullets") or []:
        typo.line(pg, "·", x, yb, T["body"], ACCENT, True)
        yb = typo.block(pg, pno, src.sub(b), x + 3, yb, w - 3, T["body"], LEAD["body"], INK, False, y + h, sid)


def put_tiles(fitz, pg, typo, pno, rect, blk, adir, src, sid):
    """Pictogram tiles (SCRIPT_STANDARD §5b): icon + keyword + one big figure + unit + [n]; a row in a wide frame,
    a column in a narrow one."""
    x, y, w, h = rect
    tiles = blk.get("tiles") or []
    if not tiles:
        return
    across = w > h
    n = len(tiles)
    tw = (w - (n - 1) * GUT) / n if across else w
    th = h if across else (h - (n - 1) * GUT) / n
    for i, t in enumerate(tiles):
        tx = x + i * (tw + GUT) if across else x
        ty = y if across else y + i * (th + GUT)
        if th < 20:
            typo.issues.append("TILE TOO SMALL p.%s %s (%.0f mm high)" % (pno, sid, th))
        pg.draw_line((tx * K, ty * K), ((tx + tw) * K, ty * K), color=hexrgb(ACCENT), width=1.0)
        ix = tx
        if t.get("icon_pdf") and os.path.isfile(os.path.join(adir, t["icon_pdf"])):
            s = fitz.open(os.path.join(adir, t["icon_pdf"]))
            pg.show_pdf_page(fitz.Rect(tx * K, (ty + 3) * K, (tx + 12) * K, (ty + 15) * K), s, 0)
            ix = tx + 14
        typo.line(pg, src.sub(t.get("keyword", "")).upper(), ix, ty + 6, T["label"], INK2, True)
        fig = src.sub(t.get("figure", ""))
        typo.line(pg, fig, ix, ty + 15, T["figure"], ACCENT, True)
        typo.line(pg, src.sub(t.get("unit", "")), ix + typo.width(fig, T["figure"], True) + 1.5, ty + 15, T["body"], INK)
        typo.block(pg, pno, src.sub(t.get("note", "")), tx, ty + 20, tw, T["caption"], LEAD["caption"], INK2,
                   False, ty + th, sid)


def put_image(fitz, pg, typo, rect, blk, src):
    x, y, w, h = rect
    name = blk.get("image", "")
    cand = [os.path.join(IMG_DIR, name + e) for e in ("", ".jpg", ".jpeg", ".png")]
    p = next((c for c in cand if os.path.isfile(c)), None)
    cap_h = 5.0 if blk.get("caption") else 0.0
    if not p:
        placeholder(pg, typo, (x, y, w, h - cap_h), "image frame: drop %s.jpg into Downloads/Bergama/booklet_images" % name)
    else:
        pg.insert_image(fitz.Rect(x * K, y * K, (x + w) * K, (y + h - cap_h) * K), filename=p, keep_proportion=True)
    typo.line(pg, src.sub(blk.get("caption", "")), x, y + h - 1.0, T["caption"], INK2)


# ------------------------------------------------------------------ special pages
def cover(pg, typo, pages):
    x = colx(1)
    typo.line(pg, BOOK["course"].upper(), x, 16, T["kicker"], ACCENT, True)
    y = 64
    for ln in typo.wrap(BOOK["title"], slot_rect(1, 7, 1, 1)[2], 48, True):
        typo.line(pg, ln, x, y, 48, INK, True); y += 18
    typo.line(pg, BOOK["subtitle"], x, y + 2, T["sub"], INK)
    yb = 232
    for ln in BOOK["names"]:
        typo.line(pg, ln, x, yb, T["body"], INK); yb += LEAD["body"]
    typo.line(pg, BOOK["date"], x, yb + 4, T["caption"], INK2)
    # contents: parts and page titles, columns 9-12
    cx, cy = colx(9), 64
    typo.line(pg, "CONTENTS", cx, cy - 8, T["kicker"], ACCENT, True)
    last = None
    for no, sp in pages:
        if sp.get("part") != last:
            last = sp.get("part")
            cy += 3
            typo.line(pg, (last + "  " + PARTS.get(last, "")).upper(), cx, cy, T["caption"], ACCENT, True); cy += 4.5
        typo.line(pg, "%02d" % no, cx, cy, T["body"], INK2, True)
        typo.line(pg, sp.get("title", ""), cx + 9, cy, T["body"], INK); cy += LEAD["body"] + 0.5
    pg.draw_line((colx(1) * K, FOOT_RULE * K), ((PW - ML) * K, FOOT_RULE * K), color=hexrgb(RULE), width=0.25)


def sources_page(pg, typo, src, pno):
    typo.line(pg, "SOURCES", colx(1), 16, T["kicker"], ACCENT, True)
    typo.line(pg, "Sources", colx(1), 32, T["title"], INK, True)
    pg.draw_line((colx(1) * K, 34 * K), ((PW - ML) * K, 34 * K), color=hexrgb(RULE), width=0.25)
    cols = [(1, 4), (5, 8), (9, 12)]
    ci, y = 0, 42.0
    for i, key in enumerate(src.order, 1):
        d = src.defs[key]
        x, _, w, _ = slot_rect(cols[ci][0], cols[ci][1], 1, 1)
        txt = "[%d] %s" % (i, d.get("text", key)) + ("  " + d["url"] if d.get("url") else "")
        need = len(typo.wrap(txt, w, T["caption"])) * LEAD["caption"] + 1.5
        if y + need > 272:
            ci += 1; y = 42.0
            if ci >= len(cols):
                typo.issues.append("SOURCES PAGE FULL: %d sources not listed" % (len(src.order) - i + 1)); break
            x, _, w, _ = slot_rect(cols[ci][0], cols[ci][1], 1, 1)
        y = typo.block(pg, pno, txt, x, y, w, T["caption"], LEAD["caption"], INK) + 1.5
    footer(pg, typo, pno, {"part": None}, [])


# ------------------------------------------------------------------ main
def page_slots():
    """{asset key: (page id, slot, w, h)} for every frame of the plan: scripts read booklet_slots.json to draw to size."""
    out = {}
    for sp in PLAN:
        for sl, key in (sp.get("slots") or {}).items():
            x, y, w, h = slot_rect(*TEMPLATES[sp["template"]][sl])
            out[key] = {"page": sp["id"], "slot": sl, "w_mm": round(w, 2), "h_mm": round(h, 2)}
    return out


def main():
    t0 = time.time()
    import fitz                                   # PyMuPDF
    os.makedirs(OUT_DIR, exist_ok=True)
    slots = page_slots()
    with open(os.path.join(OUT_DIR, "booklet_slots.json"), "w", encoding="utf-8") as f:
        json.dump(slots, f, indent=1)
    assets = load_assets()
    typo = Typo(fitz)
    src = Sources(assets)
    doc = fitz.open()
    numbered = [(i + 2, sp) for i, sp in enumerate(PLAN)]          # page 1 = cover + contents
    cover(frame_page(fitz, doc, typo), typo, numbered)
    missing = set()
    for pno, sp in numbered:
        pg = frame_page(fitz, doc, typo)
        header(pg, typo, src, pno, sp)
        legend = []
        for sl, key in (sp.get("slots") or {}).items():
            rect = slot_rect(*TEMPLATES[sp["template"]][sl])
            folder, _, bid = key.partition("/")
            a = assets.get(folder) or {}
            blk = (a.get("blocks") or {}).get(bid)
            if blk is None:
                missing.add(folder)
                placeholder(pg, typo, rect, "%s · %s" % (SCRIPT_OF.get(folder, folder), bid))
                continue
            kind = blk.get("type")
            if kind == "drawing":
                put_drawing(fitz, pg, typo, pno, rect, blk, a["_dir"], src, key)
            elif kind == "text":
                put_text(pg, typo, pno, rect, blk, src, key)
            elif kind == "tiles":
                put_tiles(fitz, pg, typo, pno, rect, blk, a["_dir"], src, key)
            elif kind == "image":
                put_image(fitz, pg, typo, rect, blk, src)
            legend += [it for it in blk.get("legend") or [] if it not in legend]
        for sl, blk in (sp.get("own") or {}).items():           # page-level blocks written in the plan itself
            rect = slot_rect(*TEMPLATES[sp["template"]][sl])
            if blk.get("type") == "image":
                put_image(fitz, pg, typo, rect, blk, src)
            else:
                put_text(pg, typo, pno, rect, blk, src, sp["id"] + "/" + sl)
        footer(pg, typo, pno, sp, legend)
    sources_page(frame_page(fitz, doc, typo), typo, src, len(numbered) + 2)
    doc.subset_fonts()
    out = os.path.join(OUT_DIR, PDF_NAME)
    doc.save(out, garbage=3, deflate=True)
    n = doc.page_count
    doc.close()
    rows = ["%s  %s  (%d pages, font %s)" % (out, time.strftime("%H:%M:%S"), n, typo.fam)]
    for name in sorted(assets):
        rows.append("assets %s: %s" % (name, assets[name].get("_error") or assets[name]["_time"]))
    for m in sorted(missing):
        rows.append("MISSING assets of %s: placeholders left" % SCRIPT_OF.get(m, m))
    rows += typo.issues[:40] + (["... %d more" % (len(typo.issues) - 40)] if len(typo.issues) > 40 else [])
    rows.append("%s %s, %.1f s" % (GH_LABEL, VERSION, time.time() - t0))
    return "\n".join(rows)


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
    log = _sc.sticky.get(_k + "_log", "Press the Button to build " + os.path.join(OUT_DIR, PDF_NAME))
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
else:
    print(write_log(main()))
