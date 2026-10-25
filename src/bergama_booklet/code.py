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
import os, re, time, json, math

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

#@include data/PLAN.py


def colx(c):
    return ML + (c - 1) * (COL + GUT)


def roww(r):
    return ROW_Y0 + (r - 1) * (ROW_H + GUT)


def slot_rect(c1, c2, r1, r2, unit="row"):
    """x, y, w, h in mm of a block spanning columns c1-c2 and rows r1-r2; unit "half" = half rows 1-8
    (26 mm + 4 mm gutter: two half rows make one row)."""
    x, w = colx(c1), (c2 - c1 + 1) * COL + (c2 - c1) * GUT
    if unit == "half":
        hh = (ROW_H - GUT) / 2.0
        return x, ROW_Y0 + (r1 - 1) * (hh + GUT), w, (r2 - r1 + 1) * hh + (r2 - r1) * GUT
    return x, roww(r1), w, (r2 - r1 + 1) * ROW_H + (r2 - r1) * GUT


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
        self.issues, self.seen, self.notes = [], {}, []

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
        """{src:key} -> [n]; {val:folder/file.json:a.b|fmt} -> the live value another script computed."""
        if not s:
            return s
        s = re.sub(r"\{val:([^}]+)\}", lambda m: live_value(m.group(1)), str(s))
        return re.sub(r"\{src:([\w.-]+)\}", lambda m: self.num(m.group(1)), s)


_JSON = {}
LIVE_MISSING = []


def live_value(spec):
    """"folder/file.json:key.sub|0" -> number from ~/Downloads/Bergama/output/folder/file.json, formatted with
    thousands commas and the given decimals (default 0). Missing -> "?" and a log line (never a made-up number)."""
    path, _, rest = spec.partition(":")
    keys, _, fmt = rest.partition("|")
    if path not in _JSON:
        try:
            with open(os.path.join(ASSET_ROOT, path), encoding="utf-8") as f:
                _JSON[path] = json.load(f)
        except Exception:
            _JSON[path] = None
    v = _JSON[path]
    for k in keys.split("."):
        if isinstance(v, list) and k.isdigit():
            v = v[int(k)] if int(k) < len(v) else None
        else:
            v = v.get(k) if isinstance(v, dict) else None
    if v is None:
        LIVE_MISSING.append(spec)
        return "?"
    if isinstance(v, (int, float)):
        d = int(fmt) if fmt.isdigit() else 0
        return "{:,.{}f}".format(v, d)
    return str(v)


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
    boxes = []
    for lb in blk.get("labels") or []:               # labels as live text, positions in mm from the drawing's top-left
        size = max(T["label"], float(lb.get("size", T["label"])))
        lx, ly = x + lb["x"] * f, y + lb["y"] * f
        txt, bold, an = src.sub(lb.get("text", "")), bool(lb.get("bold")), lb.get("anchor", "L")
        wd = typo.width(txt, size, bold)
        bx = lx - (wd / 2 if an == "C" else wd if an == "R" else 0)
        box = (bx, ly - size * PT * 0.72, bx + wd, ly + size * PT * 0.21)
        if any(box[0] < o[2] and o[0] < box[2] and box[1] < o[3] and o[1] < box[3] for o in boxes):
            typo.issues.append("LABELS OVERLAP p.%s %s: %s" % (pno, sid, txt[:30]))
        if box[0] < x - 0.5 or box[2] > x + w + 0.5 or box[1] < y - 0.5 or box[3] > y + dh + 0.5:
            typo.issues.append("LABEL OUTSIDE FRAME p.%s %s: %s" % (pno, sid, txt[:30]))
        boxes.append(box)
        typo.line(pg, txt, lx, ly, size, lb.get("colour", INK), bold, an)
    if len(sp.get_text("text").strip()):
        typo.issues.append("TEXT INSIDE DRAWING PDF p.%s %s: words must be labels in blocks.json" % (pno, sid))
    cap = src.sub(blk.get("caption", ""))
    if blk.get("scale_den"):
        cap = (cap + "   " if cap else "") + "1:{:,}".format(int(round(blk["scale_den"] / f, -1)))
    typo.line(pg, cap, x, y + h - 1.0, T["caption"], INK2)


# ---- crops of the scripts' own sheets (Aras 25 Oct 21:47: the booklet shows the sheets' drawings, re-laid) ----
STD_SCALES = (200, 250, 500, 1000, 1250, 2000, 2500, 5000, 10000, 20000, 25000, 50000)
CAVEAT = re.compile(r"\s*(?::|·|-|,)?\s*\(?(?:not designed|route not designed|not verified|unverified|schematic"
                    r"(?:, not to scale)?|not to scale|provisional)\)?\s*$", re.I)
WORDING = [(r"\bRIVERSIDE\b", "STREAMSIDE"), (r"\bRiverside\b", "Streamside"), (r"\briverside\b", "streamside"),
           (r"\bRIVERBED\b", "STREAM BED"), (r"\briverbed\b", "stream bed"), (r"\bRIVER\b", "STREAM"),
           (r"\bRiver\b", "Stream"), (r"\briver\b", "stream")]
_SHEETS = {}


def sheet_page(fitz, path, pno):
    """(page without its text, page with it) of a sheet PDF, cached: the drawing is shown from the copy whose words
    were removed (vector and images kept), the words are read from the original."""
    key = (path, pno)
    if key not in _SHEETS:
        org = fitz.open(path)
        bare = fitz.open()
        bare.insert_pdf(org, from_page=pno, to_page=pno)
        bp = bare[0]
        for b in bp.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    if sp["text"].strip():
                        bp.add_redact_annot(fitz.Rect(sp["bbox"]))
        bp.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                            text=fitz.PDF_REDACT_TEXT_REMOVE)
        _SHEETS[key] = (bare, org[pno])
    return _SHEETS[key]


def crop_words(fitz, page, clip, drop):
    """The sheet's words inside clip as units {lines, x0, y0, x1, y1 (pt), size, bold, colour, align, angle}: one unit
    per text block (a label and its keyword lines stay together), wording and caveat rules applied."""
    units = []
    for b in page.get_text("dict", clip=clip)["blocks"]:
        rows = []
        for ln in b.get("lines", []):
            t = "".join(sp["text"] for sp in ln["spans"]).strip()
            if not t:
                continue
            bb = fitz.Rect(ln["bbox"])
            if not clip.contains(fitz.Point((bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2)):
                continue
            for a, b_ in WORDING:
                t = re.sub(a, b_, t)
            t = CAVEAT.sub("", t).strip()
            if not t or any(re.search(d, t) for d in drop) or re.search(r"\(?\bidea:", t, re.I):
                continue
            if any(r["t"] == t and abs(r["bb"].x0 - ln["bbox"][0]) < 2 and abs(r["bb"].y0 - ln["bbox"][1]) < 2
                   for r in rows):                   # the same word drawn twice (outline under fill)
                continue
            sp = max(ln["spans"], key=lambda q: q["size"])
            dx, dy = ln.get("dir", (1.0, 0.0))
            rows.append(dict(t=t, bb=bb, size=sp["size"], bold=bool(sp["flags"] & 16) or "bold" in sp["font"].lower(),
                             col="%06X" % sp["color"], angle=-math.degrees(math.atan2(dy, dx)), org=ln["spans"][0]["origin"]))
        flat = [r for r in rows if abs(r["angle"]) < 2]
        for r in rows:
            if abs(r["angle"]) >= 2:
                units.append(dict(lines=[r["t"]], bb=r["bb"], size=r["size"], bold=r["bold"], col=r["col"],
                                  align="L", angle=r["angle"], org=r["org"]))
        if flat:
            bb = fitz.Rect(flat[0]["bb"])
            for r in flat[1:]:
                bb |= r["bb"]
            cx = [(r["bb"].x0 + r["bb"].x1) / 2 for r in flat]
            al = "L"
            if len(flat) > 1 and max(cx) - min(cx) < 1.0 and max(r["bb"].x0 for r in flat) - min(r["bb"].x0 for r in flat) > 1.0:
                al = "C"
            elif len(flat) > 1 and max(r["bb"].x1 for r in flat) - min(r["bb"].x1 for r in flat) < 1.0 and \
                    max(r["bb"].x0 for r in flat) - min(r["bb"].x0 for r in flat) > 1.0:
                al = "R"
            units.append(dict(lines=[r["t"] for r in flat], bb=bb, size=max(r["size"] for r in flat),
                              bold=flat[0]["bold"], col=flat[0]["col"], align=al, angle=0.0, org=flat[0]["org"]))
    return units


def put_crop(fitz, pg, typo, pno, rect, blk, sdir, src, sid):
    """A panel of a script's sheet, scaled into the frame (top-left), its words set again as live labels >= 7.5 pt:
    a label that would collide is moved (above, below, beside), else left out and logged."""
    x, y, w, h = rect
    cap_h = 5.0
    dh = h - cap_h
    path = os.path.join(sdir, blk.get("pdf", ""))
    if not os.path.isfile(path):
        placeholder(pg, typo, (x, y, w, dh), "missing sheet " + blk.get("pdf", "?"))
        return
    bare, org = sheet_page(fitz, path, int(blk.get("page", 0)))
    r = blk["rect_mm"]
    clip = fitz.Rect(r[0] * K, r[1] * K, r[2] * K, r[3] * K) & org.rect
    cw, ch = clip.width / K, clip.height / K
    f = min(w / cw, dh / ch)
    den, sden = None, blk.get("scale_den")
    if sden:
        raw = sden / f
        std = min([v for v in STD_SCALES if v >= raw * 0.999] or [raw])
        if std / raw <= 1.25:
            f, den = sden / std, std
        else:
            den = int(round(raw, -1))
    tgt = fitz.Rect(x * K, y * K, (x + cw * f) * K, (y + ch * f) * K)
    pg.show_pdf_page(tgt, bare, 0, clip=clip)
    T_ = lambda px, py: (x + (px - clip.x0) / K * f, y + (py - clip.y0) / K * f)
    units, seen = [], []
    for u in crop_words(fitz, org, clip, blk.get("drop") or []):
        sig = ("\n".join(u["lines"]), round(u["bb"].x0 / 3), round(u["bb"].y0 / 3))
        if sig not in seen:                          # twin blocks (a halo copy of the same words)
            seen.append(sig); units.append(u)
    units.sort(key=lambda u: (-u["size"], not u["bold"]))
    placed, dropped = [], []
    fx0, fy0, fx1, fy1 = x, y, x + cw * f, y + ch * f
    for u in units:
        size = min(max(T["label"], u["size"] * f), 14.0)
        lead = size * PT * 1.15
        if abs(u["angle"]) >= 2:                                 # rotated word (a street name): its own line
            ox, oy = T_(*u["org"])
            wd = typo.width(u["lines"][0], size, u["bold"])
            a = math.radians(u["angle"])
            pts = [(ox, oy), (ox + wd * math.cos(a), oy - wd * math.sin(a))]
            box = (min(p[0] for p in pts) - 0.5, min(p[1] for p in pts) - size * PT, max(p[0] for p in pts) + 0.5,
                   max(p[1] for p in pts) + 0.5)
            if box[0] < fx0 or box[2] > fx1 or box[1] < fy0 or box[3] > fy1 or \
                    any(box[0] < o[2] and o[0] < box[2] and box[1] < o[3] and o[1] < box[3] for o in placed):
                dropped.append(u["lines"][0]); continue
            placed.append(box)
            typo.line(pg, src.sub(u["lines"][0]), ox, oy, size, u["col"], u["bold"], "L", angle=u["angle"])
            continue
        lines = [src.sub(t) for t in u["lines"]]
        wd = max(typo.width(t, size, u["bold"]) for t in lines)
        hgt = size * PT * 0.95 + lead * (len(lines) - 1)
        bx0, by0 = T_(u["bb"].x0, u["bb"].y0)
        bx1, by1 = T_(u["bb"].x1, u["bb"].y1)
        ax = {"L": bx0, "C": (bx0 + bx1) / 2, "R": bx1}[u["align"]]
        cy = (by0 + by1) / 2
        ok = None
        for dx, dy in ((0, 0), (0, -hgt - 0.6), (0, hgt + 0.6), (wd * 0.6, 0), (-wd * 0.6, 0), (0, -2 * hgt - 1.2),
                       (0, 2 * hgt + 1.2)):
            left = ax + dx - {"L": 0.0, "C": wd / 2, "R": wd}[u["align"]]
            top = cy + dy - hgt / 2
            box = (left - 0.3, top - 0.3, left + wd + 0.3, top + hgt + 0.3)
            if box[0] < fx0 or box[2] > fx1 or box[1] < fy0 or box[3] > fy1:
                continue
            if any(box[0] < o[2] and o[0] < box[2] and box[1] < o[3] and o[1] < box[3] for o in placed):
                continue
            ok = (left, top, box)
            break
        if not ok:
            dropped.append(" / ".join(lines)); continue
        left, top, box = ok
        placed.append(box)
        xa = left + {"L": 0.0, "C": wd / 2, "R": wd}[u["align"]]
        for k_, t in enumerate(lines):
            typo.line(pg, t, xa, top + size * PT * 0.75 + k_ * lead, size, u["col"], u["bold"], u["align"])
    if dropped:
        typo.issues.append("CROP WORDS LEFT OUT p.%s %s (no room at %.1f pt): %s" %
                           (pno, sid, T["label"], "; ".join(d[:24] for d in dropped[:8]) +
                            (" ... +%d" % (len(dropped) - 8) if len(dropped) > 8 else "")))
    cap = src.sub(blk.get("caption", ""))
    if den:
        cap = (cap + "   " if cap else "") + "1:{:,}".format(int(den))
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
    """Pictogram tiles (SCRIPT_STANDARD §5b): icon + keyword + one big figure + unit + [n], in the grid of columns
    that fits the frame best."""
    x, y, w, h = rect
    tiles = blk.get("tiles") or []
    if not tiles:
        return
    if blk.get("heading"):
        typo.line(pg, src.sub(blk["heading"]), x, y + 5, T["sub"], INK, True)
        y, h = y + 9, h - 9
    n = len(tiles)
    best = None
    for c in range(1, n + 1):                     # columns: the layout whose tiles come closest to 45 x 26 mm
        r = -(-n // c)
        tw, th = (w - (c - 1) * GUT) / c, (h - (r - 1) * GUT) / r
        sc = min(tw / 45.0, th / 26.0)
        if best is None or sc > best[0]:
            best = (sc, c, tw, th)
    _, c, tw, th = best
    if th < 22 or tw < 36:
        typo.issues.append("TILES TOO SMALL p.%s %s (%d tiles in %.0f x %.0f mm)" % (pno, sid, n, w, h))
    for i, t in enumerate(tiles):
        tx, ty = x + (i % c) * (tw + GUT), y + (i // c) * (th + GUT)
        pg.draw_line((tx * K, ty * K), ((tx + tw) * K, ty * K), color=hexrgb(ACCENT), width=1.0)
        ix = tx
        if t.get("icon_pdf") and os.path.isfile(os.path.join(adir, t["icon_pdf"])):
            s = fitz.open(os.path.join(adir, t["icon_pdf"]))
            pg.show_pdf_page(fitz.Rect(tx * K, (ty + 3) * K, (tx + 12) * K, (ty + 15) * K), s, 0)
            ix = tx + 14
        typo.line(pg, src.sub(t.get("keyword", "")).upper(), ix, ty + 6, T["label"], INK2, True)
        fig, unit = src.sub(t.get("figure", "")), src.sub(t.get("unit", ""))
        fw = typo.width(fig, T["figure"], True)
        if fw > tx + tw - ix:
            typo.issues.append("TILE FIGURE TOO WIDE p.%s %s: %s" % (pno, sid, fig))
        typo.line(pg, fig, ix, ty + 15, T["figure"], ACCENT, True)
        yn = ty + 20
        if ix + fw + 1.5 + typo.width(unit, T["body"]) <= tx + tw:
            typo.line(pg, unit, ix + fw + 1.5, ty + 15, T["body"], INK)
        else:                                      # unit under the figure in a narrow tile
            typo.line(pg, unit, ix, ty + 19.5, T["body"], INK)
            yn = ty + 23.5
        typo.block(pg, pno, src.sub(t.get("note", "")), tx, yn, tw, T["caption"], LEAD["caption"], INK2,
                   False, ty + th, sid)


def put_image(fitz, pg, typo, rect, blk, src):
    x, y, w, h = rect
    name = blk.get("image", "")
    cand = [os.path.join(IMG_DIR, name + e) for e in ("", ".jpg", ".jpeg", ".png")]
    p = next((c for c in cand if os.path.isfile(c)), None)
    cap_h = 5.0 if blk.get("caption") else 0.0
    if not p:
        placeholder(pg, typo, (x, y, w, h - cap_h), "%s.jpg missing" % name)
    else:
        pg.insert_image(fitz.Rect(x * K, y * K, (x + w) * K, (y + h - cap_h) * K), filename=p, keep_proportion=True)
    typo.line(pg, src.sub(blk.get("caption", "")), x, y + h - 1.0, T["caption"], INK2)


# ------------------------------------------------------------------ special pages
def cover(pg, typo, pages):
    x = colx(1)
    typo.line(pg, BOOK["course"].upper(), x, 16, T["kicker"], ACCENT, True)
    typo.line(pg, BOOK["hook"], x, 64, 48, ACCENT, True)
    y = 82
    for ln in typo.wrap(BOOK["title"], slot_rect(1, 7, 1, 1)[2], T["part"], True):
        typo.line(pg, ln, x, y, T["part"], INK, True); y += 10
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
    """All sources on ONE page (Aras 25 Oct 21:54): three columns, every entry wrapped to its column (long URLs cut),
    the type size lowered step by step until everything fits; only this page may go below 7 pt."""
    typo.line(pg, "SOURCES", colx(1), 16, T["kicker"], ACCENT, True)
    typo.line(pg, "Sources", colx(1), 32, T["title"], INK, True)
    pg.draw_line((colx(1) * K, 34 * K), ((PW - ML) * K, 34 * K), color=hexrgb(RULE), width=0.25)
    cols = [(1, 4), (5, 8), (9, 12)]
    y0, y1 = 42.0, FOOT_RULE - 3.0
    txts = []
    for i, key in enumerate(src.order, 1):
        d = src.defs[key]
        txts.append("[%d] %s" % (i, d.get("text", key)) + (" " + d["url"] if d.get("url") else ""))
    w = slot_rect(1, 4, 1, 1)[2]

    def layout(size):
        lead, gap = size * PT * 1.18, size * PT * 0.6
        out, ci, y = [], 0, y0 + size * PT
        for t in txts:
            lines = typo.wrap(t, w - 1.5, size)
            need = len(lines) * lead
            if y + need - lead > y1:
                ci, y = ci + 1, y0 + size * PT
                if ci >= len(cols):
                    return None
            out.append((ci, y, lines))
            y += need + gap
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
    for ci, y, lines in rows:
        x = colx(cols[ci][0])
        for k_, ln in enumerate(lines):
            typo.line(pg, ln, x + (1.5 if k_ else 0.0), y + k_ * lead, size, INK, small_ok=True)
    if size < MIN_CAPTION:
        typo.notes.append("sources page set at %.2f pt to fit one page (%d sources)" % (size, len(txts)))
    footer(pg, typo, pno, {"part": None}, [])


# ------------------------------------------------------------------ main
def put_images(fitz, pg, typo, rect, blk, src):
    """A row of photos (Downloads/Bergama/booklet_images/<image>.jpg|png), equal widths, caption under each."""
    x, y, w, h = rect
    ims = blk.get("images") or []
    n = max(1, len(ims))
    iw = (w - (n - 1) * GUT) / n
    for i, im in enumerate(ims):
        put_image(fitz, pg, typo, (x + i * (iw + GUT), y, iw, h),
                  {"image": im.get("image", "photo_%s" % im.get("n", i + 1)), "caption": im.get("caption", "")}, src)


def place(fitz, pg, typo, src, pno, rect, blk, sid, assets, legend, missing):
    """One frame of the plan. A drawing comes from its script's blocks.json (asset key); the plan's caption, legend
    and scale win over the script's (page text lives in one place)."""
    kind = blk.get("type")
    if kind == "stack":
        x, y, w, h = rect
        parts = blk.get("blocks") or []
        wts = [float(b.get("h", 1)) for b in parts]
        yy = y
        for b, wt in zip(parts, wts):
            hh = (h - GUT * (len(parts) - 1)) * wt / sum(wts)
            place(fitz, pg, typo, src, pno, (x, yy, w, hh), b, sid, assets, legend, missing)
            yy += hh + GUT
        return
    if kind == "drawing":
        folder, _, bid = blk["asset"].partition("/")
        a = assets.get(folder) or {}
        ab = (a.get("blocks") or {}).get(bid)
        if ab is None:
            missing.add(folder)
            placeholder(pg, typo, rect, "%s · %s" % (SCRIPT_OF.get(folder, folder), bid))
            typo.line(pg, src.sub(blk.get("caption", "")), rect[0], rect[1] + rect[3] - 1.0, T["caption"], INK2)
        else:
            ab = dict(ab)
            for k in ("caption", "scale_den"):
                if blk.get(k):
                    ab[k] = blk[k]
            if ab.get("type") == "crop":                 # the sheet's own drawing (pdf path from the script's folder)
                put_crop(fitz, pg, typo, pno, rect, ab, os.path.dirname(a["_dir"]), src, sid)
            else:
                put_drawing(fitz, pg, typo, pno, rect, ab, a["_dir"], src, sid)
            if not blk.get("legend"):
                legend += [it for it in ab.get("legend") or [] if it not in legend]
    elif kind == "tiles":
        put_tiles(fitz, pg, typo, pno, rect, blk, OUT_DIR, src, sid)
    elif kind == "image":
        put_image(fitz, pg, typo, rect, blk, src)
    elif kind == "images":
        put_images(fitz, pg, typo, rect, blk, src)
    else:
        put_text(pg, typo, pno, rect, blk, src, sid)
    legend += [it for it in blk.get("legend") or [] if it not in legend]


def drawing_frames(blk, rect, out, pid, slot):
    if blk.get("type") == "stack":
        x, y, w, h = rect
        parts = blk.get("blocks") or []
        wts = [float(b.get("h", 1)) for b in parts]
        yy = y
        for b, wt in zip(parts, wts):
            hh = (h - GUT * (len(parts) - 1)) * wt / sum(wts)
            drawing_frames(b, (x, yy, w, hh), out, pid, slot)
            yy += hh + GUT
    elif blk.get("type") == "drawing":
        out[blk["asset"]] = {"page": pid, "slot": slot, "w_mm": round(rect[2], 2), "h_mm": round(rect[3], 2)}


def page_slots():
    """{asset key: page, slot, w, h} for every drawing frame: scripts read booklet_slots.json to draw to size."""
    out = {}
    for sp in PLAN:
        for sl, blk in sp["frames"].items():
            drawing_frames(blk, slot_rect(*TEMPLATES[sp["template"]][sl]), out, sp["id"], sl)
    return out


def main():
    t0 = time.time()
    import fitz                                   # PyMuPDF
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "booklet_slots.json"), "w", encoding="utf-8") as f:
        json.dump(page_slots(), f, indent=1)
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
        for sl, blk in sp["frames"].items():
            place(fitz, pg, typo, src, pno, slot_rect(*TEMPLATES[sp["template"]][sl]), blk, sp["id"] + "/" + sl,
                  assets, legend, missing)
        footer(pg, typo, pno, sp, legend)
    sources_page(frame_page(fitz, doc, typo), typo, src, len(numbered) + 2)
    text_check(fitz, doc, typo)
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
    if LIVE_MISSING:
        rows.append("LIVE VALUES NOT FOUND (shown as ?): " + ", ".join(sorted(set(LIVE_MISSING))[:10]))
    rows += typo.notes
    rows += typo.issues[:40] + (["... %d more" % (len(typo.issues) - 40)] if len(typo.issues) > 40 else [])
    rows.append("%s %s, %.1f s" % (GH_LABEL, VERSION, time.time() - t0))
    return "\n".join(rows)


def text_check(fitz, doc, typo):
    """Every text line of the finished booklet, read back from the PDF: none may leave the page's margins or
    overlap another line (the check that missed the sources page before, 25 Oct 21:53)."""
    for i, pg in enumerate(doc):
        boxes = []
        for b in pg.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                t = "".join(sp["text"] for sp in ln["spans"]).strip()
                if t:
                    r = fitz.Rect(ln["bbox"])
                    sz = max(sp["size"] for sp in ln["spans"])
                    r = fitz.Rect(r.x0, r.y1 - sz * 0.95, r.x1, r.y1 - sz * 0.2) if r.height > sz * 0.5 else r
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
