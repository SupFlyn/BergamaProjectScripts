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
Writes ~/Downloads/Bergama/output/bergama_booklet/Bergama_booklet_A3.pdf
NEW IN v3 (Aras 26 Oct 05:54 "the booklet transformation is not really successful ... drawings themselves in a
separate pdf much more better"; 06:02 picked "sheet pages, split to 5 pt"): every page IS the sheet. An A3 sheet goes
in as it is; a panel of a big sheet is cut out WITH its own words and shown at one scale per page (never stretched,
nothing rewritten or moved); a panel whose words would print under about 5 pt is divided over several pages. The
booklet adds only the cover, page titles, captions, page numbers and one sources page (each sheet's own source key).
A missing drawing leaves a labelled placeholder, so the booklet always builds.
"""
import os, re, time, json, fnmatch

# ---- SETTINGS ----
VERSION = "v3"
GH_LABEL = "Booklet"
OUT_FOLDER = "bergama_booklet"
LOG_NAME = "bergama_booklet_log.txt"
PDF_NAME = "Bergama_booklet_A3.pdf"
FONT = "Arial"                               # "Arial" (every Windows PC) or "Inter" (if installed)

BERGAMA = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA, "logs")
ASSET_ROOT = os.path.join(BERGAMA, "output")

# ---- GRID (design-language.md: all values in mm, origin top-left) ----
PW, PH = 420.0, 297.0
ML, MT, MB = 14.0, 12.0, 12.0                # left/right margin, top, bottom
COLS, COL, GUT = 12, 29.0, 4.0               # 14 + 12 x 29 + 11 x 4 + 14 = 420
BASE = 4.0                                   # baseline grid, from y = 12
FOOT_RULE, FOOT_B1, FOOT_B2 = 276.0, 280.0, 284.0
PT = 25.4 / 72.0                             # mm per point
K = 72.0 / 25.4                              # points per mm

# ---- TYPE (pt; size follows design importance) ----
T = dict(title=40, part=24, figure=24, sub=14, statement=13, body=9.5, caption=7.5, label=7.5, kicker=8, pageno=14)
LEAD = dict(title=16.0, part=10.0, statement=6.0, sub=6.0, body=4.0, caption=3.2, label=3.2)   # mm
MIN_BODY, MIN_CAPTION = 9.0, 7.0

# ---- COLOUR (palette v1.4 core roles; contrast on white checked in design-language.md) ----
INK, INK2, ACCENT = "4A3F35", "6B645B", "8B3A3F"
RULE, FRAME, PAPER = "B0AC9C", "D8D5CC", "FFFFFF"

def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_booklet_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_booklet_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_booklet_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'PLAN': 'c8a8c7dd0eef85ae69db9512bc527a09'}.get(name):
        raise RuntimeError("Data file bergama_booklet_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_booklet_data.py:" + name, "exec"), globals())


bergama_data("PLAN")


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


# ------------------------------------------------------------------ sheets
_DOCS = {}


def sheet_doc(fitz, path):
    if path not in _DOCS:
        _DOCS[path] = fitz.open(path)
    return _DOCS[path]


def find_pdf(folder, name):
    """A sheet PDF of a script's output folder (subfolders too, e.g. the board's selinus_board_pdf); name may hold *."""
    root = os.path.join(ASSET_ROOT, folder)
    for d, _, names in sorted(os.walk(root)):
        hit = sorted(n for n in names if fnmatch.fnmatch(n, name))
        if hit:
            return os.path.join(d, hit[-1])
    return None


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


def word_sizes(page, clip):
    return sorted(sp["size"] for b in page.get_text("dict", clip=clip)["blocks"] for ln in b.get("lines", [])
                  for sp in ln["spans"] if sp["text"].strip())


def ink_cuts(fitz, page, clip, n, axis):
    """n - 1 cut positions (points) dividing clip into n equal parts along axis 0 (x) or 1 (y), each moved within
    1/(4n) of its place to the line with the least ink (words included), so a cut runs between things."""
    if n < 2:
        return []
    pix = page.get_pixmap(clip=clip, dpi=30, colorspace=fitz.csGRAY)
    cols, rows = pix.width, pix.height
    m = cols if axis == 0 else rows
    ink = [0] * m
    sm = pix.samples
    for yy in range(rows):
        row = sm[yy * pix.stride: yy * pix.stride + cols]
        for xx in range(cols):
            v = 255 - row[xx]
            if v > 20:
                ink[xx if axis == 0 else yy] += 1
    lo, span = (clip.x0, clip.width) if axis == 0 else (clip.y0, clip.height)
    out = []
    for i in range(1, n):
        c0 = int(m * i / n)
        win = range(max(1, c0 - m // (4 * n)), min(m - 1, c0 + m // (4 * n)) + 1)
        c = min(win, key=lambda q: (ink[q], abs(q - c0)))
        out.append(lo + span * c / float(m))
    return out


def pieces(fitz, page, clip, ncol, nrow=1):
    """The clip divided into ncol x nrow rectangles (cuts between things), read left to right, top to bottom."""
    xs = [clip.x0] + ink_cuts(fitz, page, clip, ncol, 0) + [clip.x1]
    ys = [clip.y0] + ink_cuts(fitz, page, clip, nrow, 1) + [clip.y1]
    return [fitz.Rect(xs[c], ys[r], xs[c + 1], ys[r + 1]) for r in range(nrow) for c in range(ncol)]


def std_scale(den):
    """the first standard scale at or above den, if it is at most 10 % smaller on the page; else den itself"""
    for d in STD_SCALES:
        if d >= den - 0.5:
            return d if d <= den * 1.1 else den
    return den


STD_SCALES = (100, 200, 250, 500, 1000, 1250, 2000, 2500, 5000, 7500, 10000, 20000, 25000, 50000)
CAP_H, ROW_GAP = 5.0, 3.0                        # caption band under each panel, gap between rows (mm)
AREA = (ML, 30.0, PW - ML, FOOT_RULE - 3.0)        # where the panels go (mm)


# ------------------------------------------------------------------ pages
def frame_page(fitz, doc, typo):
    pg = doc.new_page(width=PW * K, height=PH * K)
    pg.insert_font(fontname="FR", fontfile=typo.freg)
    pg.insert_font(fontname="FB", fontfile=typo.fbold)
    return pg


def header(pg, typo, spec):
    part = PARTS.get(spec.get("part"), "")
    typo.line(pg, (spec.get("part", "") + "   " + part).upper(), colx(1), 12, T["kicker"], ACCENT, True)
    typo.line(pg, spec.get("title", ""), colx(1), 22, T["part"], INK, True)
    pg.draw_line((colx(1) * K, 25 * K), ((PW - ML) * K, 25 * K), color=hexrgb(RULE), width=0.25)


def footer(pg, typo, pno, spec, legend):
    pg.draw_line((colx(1) * K, FOOT_RULE * K), ((PW - ML) * K, FOOT_RULE * K), color=hexrgb(RULE), width=0.25)
    typo.line(pg, BOOK["project"], colx(1), FOOT_B1, T["caption"], INK, True)
    typo.line(pg, BOOK["group_line"], colx(1), FOOT_B2, T["caption"], INK2)
    typo.line(pg, "%02d" % pno, PW - ML, FOOT_B2 + 0.6, T["pageno"], ACCENT, True, "R")
    part = PARTS.get(spec.get("part"), "")
    if part:
        typo.line(pg, part.upper(), PW - ML - 12, FOOT_B2, T["caption"], INK2, True, "R")
    # legend: same place on every page (columns 4-10 of the footer band), drawn samples + plain names
    x0, x1 = colx(4), PW - ML - 34.0
    x, y = x0, FOOT_B1
    for it in legend or []:
        w = 4.0 + 1.5 + typo.width(it.get("label", ""), T["caption"]) + 5.0
        if x + w > x1:
            x, y = x0, y + 4.0
            if y > FOOT_B2 + 4.5:
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
    src = sheet_doc(fitz, path)[int(spec.get("page", 0))]
    f = min(PW * K / src.rect.width, PH * K / src.rect.height)
    pg.show_pdf_page(fitz.Rect(0, 0, src.rect.width * f, src.rect.height * f), sheet_doc(fitz, path),
                     int(spec.get("page", 0)))
    return "p.%d %s: sheet %s page %d as it is%s" % (pno, spec["title"], os.path.basename(path),
                                                   int(spec.get("page", 0)) + 1, "" if f > 0.999 else " (x%.2f)" % f)


def panel_page(fitz, doc, typo, pno, spec, rows, assets, missing):
    """rows of [(key, crop block, sheet path, clip)]: one scale for the whole page, the largest at which every row
    fits the width and all rows the height (a true scale when a panel has one); each panel with its own words."""
    gaps_w = [GUT * (len(r) - 1) for r in rows]
    aw, ah = AREA[2] - AREA[0], AREA[3] - AREA[1]
    def wh(it):
        return (it[3].width / K, it[3].height / K) if it[3] is not None else (200.0, 60.0)

    def fit(it):                                     # a piece of a split panel is sized as the largest piece
        return (spec["size"][0] / K, spec["size"][1] / K) if spec.get("size") and it[3] is not None else wh(it)
    s = min([(aw - g) / sum(fit(it)[0] for it in r) for r, g in zip(rows, gaps_w)] +
            [(ah - len(rows) * CAP_H - (len(rows) - 1) * ROW_GAP) / sum(max(fit(it)[1] for it in r) for r in rows)])
    den0 = next((it[1].get("scale_den") for r in rows for it in r if it[1] and it[1].get("scale_den")), None)
    if den0:
        s = min(s, den0 / std_scale(den0 / s))
    pg = frame_page(fitz, doc, typo)
    header(pg, typo, spec)
    legend, rep, y = [], [], AREA[1]
    for r in rows:                                   # rows centred across the page
        rw = sum(wh(it)[0] for it in r) * s + GUT * (len(r) - 1)
        x, rh = AREA[0] + max(0.0, (aw - rw) / 2.0), max(wh(it)[1] for it in r) * s
        for key, blk, path, clip in r:
            w, h = wh((key, blk, path, clip))
            if clip is None:
                missing.add(key.partition("/")[0])
                placeholder(pg, typo, (x, y, w * s, h * s), "%s · %s" % (SCRIPT_OF.get(key.partition("/")[0], ""),
                                                                        key.split("/")[1]))
                rep.append("%s MISSING" % key)
            else:
                src = sheet_doc(fitz, path)
                pg.show_pdf_page(fitz.Rect(x * K, y * K, (x + w * s) * K, (y + h * s) * K), src,
                                 int(blk.get("page", 0)), clip=clip)
                cap = blk.get("caption", "")
                if blk.get("scale_den"):
                    cap = (cap + " · " if cap else "") + "1:{:,.0f}".format(blk["scale_den"] / s)
                if key.count("/") > 1:
                    cap = cap + " (%s)" % key.rsplit("/", 1)[1]
                typo.line(pg, cap, x, y + h * s + 3.6, T["caption"], INK2)
                for it in blk.get("legend") or []:
                    if all(it.get("label") != o.get("label") for o in legend):
                        legend.append(it)
                ws = word_sizes(src[int(blk.get("page", 0))], clip)
                if ws:
                    med, low = ws[len(ws) // 2] * s, ws[len(ws) // 10] * s
                    rep.append("%s words %.1f pt (smallest tenth %.1f)" % (key.split("/", 1)[1], med, low))
                    if med < 4.95:
                        typo.issues.append("SMALL WORDS p.%d %s: %.1f pt" % (pno, key, med))
            x += w * s + GUT
        y += rh + CAP_H + ROW_GAP
    footer(pg, typo, pno, spec, legend)
    return "p.%d %s: x%.2f · %s" % (pno, spec["title"], s, "; ".join(rep))


def expand(fitz, spec, assets):
    """One plan entry -> [(spec, rows)] pages: keys resolved to (key, block, path, clip); "/i" = piece i of the
    panel cut into spec["pieces"][key] columns; spec["split"] (cols, rows) = one page per piece of a one-panel page."""
    def item(key):
        base, _, i = key.rpartition("/") if key.count("/") > 1 else (key, "", "")
        blk, path = resolve(assets, base)
        if not path:
            return (key, blk, None, None)
        page = sheet_doc(fitz, path)[int(blk.get("page", 0))]
        r = blk["rect_mm"]
        clip = fitz.Rect(r[0] * K, r[1] * K, r[2] * K, r[3] * K) & page.rect
        if i:
            clip = pieces(fitz, page, clip, int(spec.get("pieces", {}).get(base, 1)))[int(i) - 1]
        return (key, blk, path, clip)
    rows = [[item(k) for k in r] for r in spec["rows"]]
    if spec.get("optional") and all(it[3] is None for r in rows for it in r):
        return []
    if not spec.get("split"):
        return [(spec, rows)]
    key, blk, path, clip = rows[0][0]
    if clip is None:
        return [(spec, rows)]
    nc, nr = spec["split"]
    parts = pieces(fitz, sheet_doc(fitz, path)[int(blk.get("page", 0))], clip, nc, nr)
    big = (max(p_.width for p_ in parts), max(p_.height for p_ in parts))
    keep = spec.get("keep") or range(1, len(parts) + 1)
    out = []
    for n_, i in enumerate(keep):                    # one scale for all the pieces: sized as the largest
        pc = parts[i - 1]
        sp = dict(spec, title="%s (%d/%d)" % (spec["title"], n_ + 1, len(keep)), size=big)
        out.append((sp, [[(key, blk, path, pc)]]))
    return out


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
    last, seen = None, set()
    for no, sp in pages:
        t = re.sub(r" \(\d+/\d+\)$", "", sp.get("title", ""))
        if t in seen:
            continue
        seen.add(t)
        if sp.get("part") != last:
            last = sp.get("part")
            cy += 2
            typo.line(pg, (last + "  " + PARTS.get(last, "")).upper(), cx, cy, T["caption"], ACCENT, True); cy += 4.5
        typo.line(pg, "%02d" % no, cx, cy, T["caption"], INK2, True)
        typo.line(pg, t, cx + 8, cy, T["caption"], INK); cy += 4.0
    pg.draw_line((colx(1) * K, FOOT_RULE * K), ((PW - ML) * K, FOOT_RULE * K), color=hexrgb(RULE), width=0.25)


def sheet_sources(fitz):
    """[(heading, [entries])]: each sheet page's own source key ("Sources by number: [1] ... [2] ..." or lines
    starting [n]), as the sheet prints it: the [n] marks on that sheet's pages refer to it."""
    out = []
    for pat in SOURCE_SHEETS:
        folder, _, name = pat.partition("/")
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
            ents = [e.strip() for e in re.split(r"\s(?=\[\d+\] )", " " + " ".join(txt)) if e.strip()]
            if ents:
                head = SCRIPT_OF.get(folder, folder) + (" · page %d" % (i + 1) if len(d) > 1 else "")
                if "axonometric" in name:
                    head += " · axonometric"
                out.append((head, ents))
    return out


def sources_page(pg, typo, pno, groups):
    """All sources on ONE page (Aras 25 Oct 21:54): each sheet's own key under its name, three columns, the type
    size lowered step by step until everything fits; only this page may go below 7 pt."""
    typo.line(pg, "SOURCES", colx(1), 12, T["kicker"], ACCENT, True)
    typo.line(pg, "Sources, by sheet", colx(1), 22, T["part"], INK, True)
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


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    import fitz                                   # PyMuPDF
    os.makedirs(OUT_DIR, exist_ok=True)
    assets = load_assets()
    typo = Typo(fitz)
    doc = fitz.open()
    plan = []
    for spec in PAGES:
        if spec.get("sheet"):
            plan.append((spec, None))
        else:
            plan += expand(fitz, spec, assets)
    numbered = [(i + 2, sp, rows) for i, (sp, rows) in enumerate(plan)]   # page 1 = cover + contents
    cover(frame_page(fitz, doc, typo), typo, [(n, sp) for n, sp, _ in numbered])
    missing, rep = set(), []
    for pno, sp, rows in numbered:
        rep.append(sheet_page(fitz, doc, typo, pno, sp) if rows is None else
                   panel_page(fitz, doc, typo, pno, sp, rows, assets, missing))
    sources_page(frame_page(fitz, doc, typo), typo, len(numbered) + 2, sheet_sources(fitz))
    text_check(fitz, doc, typo, set(n - 1 for n, sp, rows in numbered if rows is None))
    doc.subset_fonts()
    out = os.path.join(OUT_DIR, PDF_NAME)
    doc.save(out, garbage=3, deflate=True)
    n = doc.page_count
    doc.close()
    rows = ["%s  %s  (%d pages, font %s)" % (out, time.strftime("%H:%M:%S"), n, typo.fam)]
    for name in sorted(assets):
        rows.append("assets %s: %s" % (name, assets[name].get("_error") or assets[name]["_time"]))
    for m in sorted(missing):
        rows.append("MISSING drawings of %s: placeholders left" % SCRIPT_OF.get(m, m))
    rows += rep + typo.notes
    rows += typo.issues[:40] + (["... %d more" % (len(typo.issues) - 40)] if len(typo.issues) > 40 else [])
    rows.append("%s %s, %.1f s" % (GH_LABEL, VERSION, time.time() - t0))
    return "\n".join(rows)


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
