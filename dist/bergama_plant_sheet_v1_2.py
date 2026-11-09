# -*- coding: utf-8 -*-
# CURRENT VERSION: bergama_plant_sheet_v1_2.py = v1.2 (4 Nov 2026, Aras 19:15: no empty "no image" boxes; each row
# lists its missing images once, under the species name)
"""BERGAMA PLANT SHEET v1 (round 5, session S4, 1 Nov 2026; BRIEF D4, G-R5-6, G-R5-4.4, D10; PLAN §9 "D4 STOP").
ONE A0 portrait sheet for Aras to approve before any booklet page uses the new plants and people:
  * every species x state (general, spring, summer, autumn, winter) of the plant module v3 (common/plants.py): the
    section at 1:250, the plan at 1:1,000, and for shrubs, flowers and reeds a detail at 1:50 (1:100 above 2.5 m);
    under each cell the image source (asset_png = Data/plants/, cutout = Data/cutouts/, hires = assets_hires.json,
    placeholder = no image yet: a labelled dashed box, never a stand-in drawing);
  * the crops (cotton, maize, tomato) per state; their size is not sourced, so they are shown in a 1.00 m box;
  * the people (common/figures.py, set "library_dark") in every pose the pages use, at 1:50, each on what it touches
    (step, water, rail, bank, branch, stall), with its source (asset_library / drawn_A1_style); the three depth
    layers; the plan-view people.
Colours: every plant colour is still "pending research/plant_colours.md" (FLAG in the log); the sheet says so.
Writes Downloads/Bergama/output/Bergama_plant_sheet/Bergama_plant_sheet.pdf; log in Downloads/Bergama/logs/.
Runs as delivered in a Grasshopper Python 3 component (press a Button wired to any input named run) or plain
Python 3. Needs Data/ from the run kit: figures_A1.json, cutouts/, assets_hires.json; Data/plants/ when the asset
project has delivered it (until then the placeholders show what is missing).
"""
import os
import json
import math
import time
import zlib

VERSION = "v1.2"
GH_LABEL = "PlantSheet"
OUT_FOLDER = "Bergama_plant_sheet"
OUT_PDF_NAME = "Bergama_plant_sheet.pdf"
LOG_NAME = "bergama_plant_sheet_log.txt"

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
OUT_DIR = bg_output(OUT_FOLDER)
LOG_DIR = bg_logs()

def hex_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16) / 255.0, int(h[2:4], 16) / 255.0, int(h[4:6], 16) / 255.0)
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
_ENC_EXTRA = _PF_EXTRA
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
PT = FM_PT


def text_w(s, size, bold=False):
    """the real Arial width (font_metrics.fm_width) of s at size mm"""
    return fm_width(s, size / PT, bold)


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
    """A water body (ring, page mm): channel blue, 45-degree blue hatch, the water line on top (as draw_stream)."""
    sh = [("poly", ring, SEC["channel"], None, 0.1)]
    sh += [("line", [p, q], SEC["hatch"], lw) for p, q in sec_hatch(ring, spacing)]
    top = max(p[1] for p in ring)
    xs = [p[0] for p in ring if abs(p[1] - top) < 1e-6]
    if len(xs) >= 2:
        sh.append(("line", [(min(xs), top), (max(xs), top)], SEC["hatch"], 0.3))
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


def sct_hatch_fill(ring, material, k, outline=None, lw=0.25, fill=True, hatch_lw=None):
    """A cut ring (page mm) in its material's fill and standard hatch: stone, concrete, earth, gravel or water.
    fill=False: the hatch only (sct_ground lays the soil gradient under it); hatch_lw: the earth hatch's line width
    (page mm; default 0.07)."""
    import math as _m
    if material == "water":
        return sec_water(ring)
    if material not in ("stone", "concrete", "earth", "gravel"):
        raise ValueError("sct_hatch_fill: unknown material %r" % material)
    g = max(0.7, min(1.4, k / 5.0))           # patterns are page-mm conventions (1:200 size), eased with k; no real sizes
    ln = SCT["line"]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    sh = [("poly", ring, SCT[material], None, 0.1)] if fill else []
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
                if (i + j) % 3 == 0 and globals().get("SF_TRI", {}).get("aggregate", True):   # R2-A: sf_triangles
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
                sh.append(("line", [(p[0] + ux * s, p[1] + uy * s), (p[0] + ux * e, p[1] + uy * e)], ln,
                           hatch_lw or 0.07))
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


# G15 soil (round 3, PLAN.md §2 "Soil"): drawing rules, not measured soil data. A topsoil band SCT_SOIL["top_m"]
# thick (drawn at the section's scale) in the dark brown at the surface, then SCT_SOIL["steps"] bands following the
# surface down to the cut bottom, lightening step by step to the pale subsoil; the broken earth hatch on top at
# 0.15 pt (0.053 mm).
SCT_SOIL = dict(top="5A4632", bottom="C9BBA2", top_m=0.30, steps=5, hatch_lw=0.053)


def sct_soil_gradient(surface, bottom_y, k):
    """G15 soil under a surface polyline (page mm, left to right) down to bottom_y: the topsoil band (SCT_SOIL top_m
    x k deep under every point of the surface) then SCT_SOIL steps bands, each parallel to the surface, from the
    topsoil colour to the subsoil colour at bottom_y. Opaque fills only, no strokes. Returns shapes."""
    S = [(float(x), float(y)) for x, y in surface]
    if len(S) < 2:
        return []
    t = SCT_SOIL["top_m"] * k
    n = int(SCT_SOIL["steps"])
    b = float(bottom_y)

    def depth_at(y, f):                       # f = 0 at the topsoil's underside .. 1 at the cut bottom
        top = max(b, y - t)
        return top - (top - b) * f

    sh = [("poly", [(x, y) for x, y in S] + [(x, max(b, y - t)) for x, y in reversed(S)], SCT_SOIL["top"], None,
           0.0)]
    for i in range(n):
        fa, fb = i / float(n), (i + 1) / float(n)
        col = _sec_mix(SCT_SOIL["top"], SCT_SOIL["bottom"], (i + 1) / float(n))
        ring = [(x, depth_at(y, fa)) for x, y in S] + [(x, depth_at(y, fb)) for x, y in reversed(S)]
        sh.append(("poly", ring, col, None, 0.0))
    return sh


def sct_ground(surface, bottom_y, k, material="earth", lw=0.35):
    """Cut ground under a surface polyline (page mm, left to right) down to bottom_y: hatch and the cut line.
    material "earth": the G15 soil gradient (sct_soil_gradient) under the broken hatch (round 3, every section)."""
    ring = list(surface) + [(surface[-1][0], bottom_y), (surface[0][0], bottom_y)]
    if material == "earth":
        return (sct_soil_gradient(surface, bottom_y, k) +
                sct_hatch_fill(ring, material, k, fill=False, hatch_lw=SCT_SOIL["hatch_lw"]) +
                [("line", list(surface), SCT["cut"], lw)])
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
    return []                                    # v1.2 (Aras 4 Nov 19:15): no empty box; the row lists what is missing


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
    seated on the lowest ground under its feet (sf_seat_x). Pass water whenever a zone reaches the channel: nobody
    stands where the drawn water is deeper than FIG_WADE_MAX_M (knee) on a wading strip, or above the ground at all
    on any other zone (refused parts counted in the G14 log line as "<kind> (too deep)"). p goes to every figure
    (seat_h, rail_h ...). focus = page x everyone who stays looks at (R2-C scenes: the water; see fig_activity), or
    a function of (kind, x0, x1) -> page x or None per zone. Returns (shapes, placed [(kind, pose, x)])."""
    seat = globals().get("sf_seat_x")
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


class Page(object):
    def __init__(self, W, H):
        self.W, self.H, self.items = W, H, []

    def poly(self, rings, fill=None, stroke=None, lw=0.1, dash=None, stripes=None, alpha=None):
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            self.items.append(("poly", rings, fill, stroke, lw, dash, stripes, alpha))

    def line(self, pts, stroke, lw=0.1, dash=None, cap=1):
        if len(pts) >= 2:
            self.items.append(("line", pts, stroke, lw, dash, cap))

    def text(self, s, x, y, size, color, bold=False, align="L"):
        if s:
            self.items.append(("text", s, x, y, size, color, bold, align, None, None))


def put(pg, shapes):
    """house shapes onto the page (as water.py shp_put): poly, line, text, image"""
    for s_ in shapes or []:
        t = s_[0]
        if t == "poly":
            if len(s_[1]) >= 3:
                pg.poly([list(s_[1])], fill=s_[2] or None, stroke=s_[3] or None, lw=s_[4] or 0.1)
        elif t == "line":
            pg.line(list(s_[1]), s_[2], s_[3], s_[4] if len(s_) > 4 else None)
        elif t == "text":
            pg.text(s_[1], s_[2], s_[3], s_[4], s_[5], bold=s_[6] if len(s_) > 6 else False,
                    align=s_[7] if len(s_) > 7 else "L")
        elif t == "image":
            pg.items.append(tuple(s_) + (None,) * (9 - len(s_)))


# ---- sheet layout (A0 portrait; sizes in mm; design values) -------------------------------------------------------------
SH_W, SH_H, SH_M = 841.0, 1189.0, 14.0
INK, INK2, RED = "3C4733", "8E8F8A", "8B2D2D"          # palette (Bergama COLOUR rule)
WATER, WATER_LINE, STEP = "A2B6B5", "5C7A86", "D5D3CE"  # PLAN §3 section materials
GROUND = "C2A383"                                        # PLAN §3 soil top layer
T_TITLE, T_HEAD, T_TEXT, T_SMALL = 16 * PT, 7 * PT, 5 * PT, 4.5 * PT
STATES = (None, "spring", "summer", "autumn", "winter")
K_SEC, K_PLAN = 4.0, 1.0                                 # 1:250 and 1:1,000: page mm per m
LABEL_W = 92.0
COL_W = (SH_W - 2 * SH_M - LABEL_W) / 5.0
SPECIES_ROWS = ("stone_pine", "ash", "plane", "willow", "olive", "tamarisk", "chaste", "rosemary", "lavender",
                "loosestrife", "soft_rush", "rush", "reed", "mint")
CROP_ROWS = ("cotton", "maize", "tomato")
CROP_BOX_M = 1.00                                        # crop size not sourced: shown in a 1.00 m box (labelled)
K_PEOPLE = 20.0                                          # 1:50


def _xspan(shapes):
    """(min x, max x) of house shapes, or None"""
    xs = []
    for s_ in shapes or []:
        if s_[0] in ("poly", "line"):
            xs += [q[0] for q in s_[1]]
        elif s_[0] == "image":
            xs += [s_[1], s_[1] + s_[3]]
        elif s_[0] == "text":
            xs.append(s_[2])
    return (min(xs), max(xs)) if xs else None


def _shift(shapes, dx):
    """house shapes moved by dx (page mm) along x"""
    out = []
    for s_ in shapes or []:
        if s_[0] in ("poly", "line"):
            out.append((s_[0], [(q[0] + dx, q[1]) for q in s_[1]]) + tuple(s_[2:]))
        elif s_[0] == "image":
            out.append((s_[0], s_[1] + dx) + tuple(s_[2:]))
        elif s_[0] == "text":
            out.append(s_[:2] + (s_[2] + dx,) + tuple(s_[3:]))
        else:
            out.append(s_)
    return out


def _at_left(shapes, left):
    """shapes moved so their left edge is at `left`; returns (shapes, right edge)"""
    sp = _xspan(shapes)
    if not sp:
        return shapes, left
    return _shift(shapes, left - sp[0]), left + sp[1] - sp[0]


def _src(key, state, view):
    v = PLA_SRC.get((key, state or "general", view)) or "-"
    return u"no image" if v == "placeholder" else v


def _missing_row(key):
    """v1.2: 'no image yet · side: spring, winter · plan: all' for one species / crop row ('' when nothing is missing)"""
    out = []
    for view, nm in (("side", u"side"), ("top", u"plan")):
        st = [s_ or "general" for s_ in STATES if PLA_SRC.get((key, s_ or "general", view)) == "placeholder"]
        if st:
            out.append(u"%s: %s" % (nm, u"all" if len(st) == len(STATES) else u", ".join(st)))
    return (u"no image yet · " + u" · ".join(out)) if out else u""


def _sec_draw(key, x, g, k, state):
    """one species in section (reed and mint, which grow only in lined cells, through the image call itself)"""
    if key in ("reed", "mint"):
        sp = PLA_SPECIES[key]
        h, w = sp["h_m"], sp["crown_m"] or 1.0
        c0 = pla_colours(key, state)
        return _pla_img_draw(key, state, "side", x, g, h, w, k, c0, 0, False, 0, c0["bare"]) or \
            _pla_missing_draw(key, state, "side", x, g, h, w, k) or []
    return pla_section(key, x, g, k, season=state)


def sheet_plants(pg, top, log):
    """the species x state table; returns the y below it"""
    y = top
    x0 = SH_M + LABEL_W
    for i, s_ in enumerate(STATES):
        cx = x0 + i * COL_W
        pg.text((s_ or "general").capitalize(), cx + 4.0, y - 6.0, T_HEAD, INK, True)
        pg.text(u"section 1:250 · plan 1:1,000 · detail 1:50 (1:100 above 2.5 m)", cx + 4.0, y - 9.5, T_SMALL, INK2)
    pg.text(u"Species (sourced drawing height)", SH_M, y - 6.0, T_HEAD, INK, True)
    y -= 14.0
    for key in SPECIES_ROWS:
        sp = PLA_SPECIES[key]
        h = float(sp["h_m"])
        small = sp["layer"] != "tree"
        k2 = 20.0 if h <= 2.5 else 10.0
        row_h = max(h * K_SEC, h * k2 if small else 0.0) + 16.0
        g = y - row_h + 10.0                             # ground line of the row
        pg.text(sp["name"], SH_M, g + row_h - 14.0, T_TEXT, INK, True)
        pg.text(sp["latin"], SH_M, g + row_h - 16.5, T_SMALL, INK2)
        pg.text(u"h %.2f m%s" % (h, (u" · detail 1:%d" % (1000 / k2)) if small else u""), SH_M, g + row_h - 19.0,
                T_SMALL, INK2)
        if key in ("reed", "mint"):
            pg.text(u"lined cells only (no plan symbol)", SH_M, g + row_h - 21.5, T_SMALL, INK2)
        for i, s_ in enumerate(STATES):
            cx = x0 + i * COL_W
            pg.line([(cx + 2.0, g), (cx + COL_W - 4.0, g)], INK2, 0.15)
            shp, xr = _at_left(_sec_draw(key, 0.0, g, K_SEC, s_), cx + 4.0)   # true size, never squeezed
            put(pg, shp)
            lab = u"%s" % _src(key, s_, "side")
            if key not in ("reed", "mint"):
                shp, xr = _at_left(pla_plan(key, 0.0, g + 10.0, K_PLAN, season=s_), max(xr, cx + 10.0) + 6.0)
                put(pg, shp)
                lab += u" | plan %s" % _src(key, s_, "top")
            if small:
                shp, xr = _at_left(_sec_draw(key, 0.0, g, k2, s_), xr + 6.0)
                put(pg, shp)
            if xr > cx + COL_W:
                log.append(u"WARNING sheet %s %s runs %.0f mm into the next column" % (key, s_ or "general",
                                                                                   xr - cx - COL_W))
            if lab.replace(u"no image", u"").strip(u" |plan-"):
                pg.text(lab.replace(u" | plan no image", u""), cx + 2.0, g - 3.5, T_SMALL, INK2)
        miss_ = _missing_row(key)
        if miss_:
            pg.text(miss_, SH_M, g + row_h - 24.0, T_SMALL, RED)
        y -= row_h
    for crop in CROP_ROWS:
        row_h = CROP_BOX_M * 20.0 + 16.0
        g = y - row_h + 10.0
        pg.text(PLA_CROPS[crop]["name"], SH_M, g + row_h - 14.0, T_TEXT, INK, True)
        pg.text(u"size not sourced: shown in a 1.00 m box at 1:50", SH_M, g + row_h - 16.5, T_SMALL, RED)
        for i, s_ in enumerate(STATES):
            cx = x0 + i * COL_W
            st = pla_crop_state(crop, s_)
            pg.line([(cx + 2.0, g), (cx + COL_W - 4.0, g)], INK2, 0.15)
            put(pg, _pla_crop_sec(crop, cx + 20.0, g, CROP_BOX_M, 0.6 * CROP_BOX_M, 20.0, i, False, st, s_))
            src_ = _src(crop, s_, "side") if st not in ("bare", "harvested") else u"drawn"
            pg.text(u"%s" % st if src_ == u"no image" else u"%s · %s" % (st, src_), cx + 2.0, g - 3.5, T_SMALL, INK2)
        miss_ = _missing_row(crop)
        if miss_:
            pg.text(miss_.replace(u" · plan: all", u""), SH_M, g + row_h - 19.0, T_SMALL, RED)
        y -= row_h
    return y


# people scenes: (pose, params, width m); each scene shows what the figure touches
PEOPLE = (("stand", {}, 0.9), ("walk", {}, 1.0), ("watch", {}, 1.0), ("railing", {"rail_h": 1.10}, 1.4),
          ("sit_step", {"seat_h": 0.45}, 1.4), ("wade", {"depth_m": 0.40}, 1.4), ("fishing", {"water_dy": -0.80}, 3.6),
          ("touch", {"reach_y": -0.30}, 1.4), ("bike", {}, 2.0), ("adult_child", {}, 1.2), ("child_play", {}, 1.6),
          ("olive", {"branch_h": 1.90}, 1.2), ("running", {}, 1.2), ("lying", {}, 2.0), ("dog_walk", {}, 2.6),
          ("stall", {}, 3.0))


def _scene(pose, p, x, g, k):
    """the ground / step / water / rail / branch a figure touches, then the figure (feet at (x, g))"""
    sh = []
    if pose == "wade":                                   # wading strip: bed, water to depth_m, legs cut at the water
        d = p["depth_m"] * k
        sh.append(("poly", [(x - 0.6 * k, g), (x + 0.6 * k, g), (x + 0.6 * k, g + d), (x - 0.6 * k, g + d)], WATER, None, 0))
        sh.append(("line", [(x - 0.6 * k, g + d), (x + 0.6 * k, g + d)], WATER_LINE, 0.2))
        return sh + fig_side(pose, x, g, k, pick=1, **p)
    if pose in ("fishing", "touch"):                     # bank edge, water below it
        wd = p.get("water_dy", p.get("reach_y", -0.3)) * k
        ex = x + (0.35 if pose == "fishing" else 0.45) * k
        bed = g + wd - 0.4 * k
        sh.append(("poly", [(ex, bed), (x + 3.4 * k, bed), (x + 3.4 * k, g + wd), (ex, g + wd)], WATER, None, 0))
        sh.append(("line", [(ex, g + wd), (x + 3.4 * k, g + wd)], WATER_LINE, 0.2))
        sh.append(("poly", [(x - 0.6 * k, bed), (ex, bed), (ex, g), (x - 0.6 * k, g)], STEP, INK2, 0.1))
        return sh + fig_side(pose, x, g, k, pick=1, **p)
    if pose == "sit_step":                               # the step it sits on (nosing from fig_meta)
        an = fig_meta(pose, **p)
        nx, sy = x + an.get("seat_x", 0.15) * k, g + an.get("seat_y", p["seat_h"]) * k
        sh.append(("poly", [(nx - 0.55 * k, g), (nx, g), (nx, sy), (nx - 0.55 * k, sy)], STEP, INK2, 0.1))
        return sh + fig_side(pose, x, g, k, pick=1, **p)
    if pose == "railing":
        an = fig_meta(pose, **p)
        rx, ry = x + an.get("rail_x", 0.4) * k, g + an.get("rail_y", p["rail_h"]) * k
        sh += fig_side(pose, x, g, k, pick=1, **p)
        sh += [("line", [(rx, g), (rx, ry)], INK2, 0.35), ("line", [(rx - 0.3 * k, ry), (rx + 0.3 * k, ry)], INK2, 0.5)]
        return sh
    if pose == "olive":
        an = fig_meta(pose, **p)
        hx = x + an.get("hand_x", 0.3) * k
        by = g + p["branch_h"] * k
        sh.append(("line", [(hx - 0.5 * k, by + 0.1 * k), (hx + 0.6 * k, by - 0.05 * k)], PLA_TRUNK, 0.6))
        return sh + fig_side(pose, x, g, k, pick=1, **p)
    if pose == "stall":
        return fig_stall(x + 1.2 * k, g, k, facing=1)
    return fig_side(pose, x, g, k, pick=1, **p)


def sheet_people(pg, top, log):
    """the people panel: every pose at 1:50 on what it touches, the depth layers, the plan views; returns y"""
    k = K_PEOPLE
    pg.text(u"People · one set, one dark tone (A1 library first, then cutouts, then poses drawn in the A1 language) "
            u"· 1:50", SH_M, top - 6.0, T_HEAD, INK, True)
    g = top - 14.0 - 2.6 * k
    x = SH_M + 4.0
    for pose, p, wm in PEOPLE:
        if x + wm * k > SH_W - SH_M:
            g -= 3.2 * k
            x = SH_M + 4.0
        cx = x + 0.5 * k
        pg.line([(x - 2.0, g), (x + wm * k, g)], INK2, 0.15)
        put(pg, _scene(pose, p, cx, g, k))
        q = dict(p)
        src = _fig_side_dark(FIG_POSE_ALIAS.get(pose, pose) if pose != "stall" else "stall", 1, q)[0]
        pg.text(pose.replace("_", " "), x, g - 3.0, T_TEXT, INK, True)
        pg.text(src, x, g - 5.2, T_SMALL, INK2)
        x += wm * k + 8.0
    g -= 3.0 * k                                         # depth layers 0 / 1 / 2 (nearer stronger, farther paler)
    x = SH_M + 4.0
    pg.text(u"Depth layers 0 / 1 / 2 (opaque, paler and smaller behind)", x, g + 2.4 * k, T_TEXT, INK, True)
    for lay in (0, 1, 2):
        for j, pose in enumerate(("stand", "walk", "sit_step")):
            xx = x + (lay * 3 + j) * 0.9 * k
            put(pg, fig_side(pose, xx, g, k, layer=lay, pick=2 + j, seat_h=0.45) if pose == "sit_step" else
                fig_side(pose, xx, g, k, layer=lay, pick=2 + j))
    pg.line([(x - 2.0, g), (x + 8.2 * k, g)], INK2, 0.15)
    x2 = x + 9.5 * k                                     # plan views
    pg.text(u"Plan views (drawn A1 style)", x2, g + 2.4 * k, T_TEXT, INK, True)
    for j, pose in enumerate(("stand", "walk", "sit_step", "bike", "adult_child", "fishing", "dog_walk", "lying")):
        put(pg, fig_top(pose, x2 + 0.6 * k + j * 1.9 * k, g + 0.9 * k, k, pick=j))
        pg.text(pose.replace("_", " "), x2 + j * 1.9 * k, g - 3.0, T_SMALL, INK2)
    return g - 8.0


def main(G):
    t0 = time.time()
    pla_missing("placeholder")                            # the sheet shows what is missing, never a stand-in
    pg = Page(SH_W, SH_H)
    pg.poly([[(0, 0), (SH_W, 0), (SH_W, SH_H), (0, SH_H)]], fill="FFFFFF")
    pg.text(u"Plants and people · sample sheet for approval (D4)", SH_M, SH_H - SH_M - 6.0, T_TITLE, INK, True)
    pg.text(u"Plant colours: pending research/plant_colours.md (every species). Image source under each cell: asset_png "
            u"= Data/plants, cutout = Data/cutouts (species by look), hires = PhyloPic silhouette; missing images are listed "
            u"in red under each species name (no empty boxes).", SH_M, SH_H - SH_M - 12.0, T_TEXT, RED)
    warn = []
    y = sheet_plants(pg, SH_H - SH_M - 26.0, warn)
    y = sheet_people(pg, y - 6.0, warn)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, OUT_PDF_NAME)
    try:
        write_pdf(pg, out, "Bergama plant sheet " + VERSION)
    except PermissionError:
        return "ERROR: The PDF is open in a viewer: close it and press the Button again (%s)" % out
    lines = [u"%s  %s" % (out, time.strftime("%H:%M:%S")), u"plant sheet %s, %.1f s" % (VERSION, time.time() - t0)]
    if y < 0:
        warn.append(u"WARNING sheet content runs %.0f mm below the page" % -y)
    lines = warn + lines
    lines += pla_log_lines()
    lines.append(fig_set_line())
    lines += fig_flag_lines()
    lines.append(u"FLAG fauna pending research (deferred; not on this sheet)")
    lines += FIG_LOG + SIL_LOG + HR_LOG + WP_IMG_LOG + PLA_LOG
    nw = sum(1 for ln in lines if ln.startswith(u"WARNING"))
    return u"%d warnings\n" % nw + u"\n".join(lines)


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


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
TRIGGER_BUTTON_WORDS = ("run", "bake", "build", "go", "press", "button", "start")


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
            key = key + ":" + str(ghenv.Component.InstanceGuid) + ":" + _chain_wiring()      # noqa: F821
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
        if first or _scx.sticky.get(key) == s:
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
        pk = "trig_prev:" + key + ":" + gk
        on = to_bool(trig_get(btn)) if btn else False
        prev = bool(_scx.sticky.get(pk, False))
        _scx.sticky[pk] = on
    except Exception:
        on, prev = (to_bool(trig_get(btn)) if btn else False), False
    if on and not prev:
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
def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try:
        _ik = ":" + str(ghenv.Component.InstanceGuid)
    except Exception:
        _ik = ""
    _pressed, _why, _btn = trig_should_run("bergama_plant_sheet_log_chain")
    if _pressed and str(_why or "").startswith("button"):
        # v1.1 (Aras 2 Nov 05:38): a Button press here starts a chain run, so ZoneBase wired after it fires
        try:
            _d = ghenv.Component.OnPingDocument()                          # noqa: F821
            _dk = ""
            if _d is not None:
                for _a in ("RuntimeID", "RuntimeId"):
                    try:
                        if getattr(_d, _a) is not None:
                            _dk = "doc%s" % getattr(_d, _a)
                            break
                    except Exception:
                        pass
                if not _dk:
                    try:
                        _dk = "doch%s" % _d.GetHashCode()
                    except Exception:
                        _dk = "docp%s" % id(_d)
            _sc.sticky["bergama_chain_t0"] = time.time()
            _sc.sticky["bergama_chain_doc"] = _dk
        except Exception:
            pass
    if _pressed:
        _t0 = time.time()
        try:
            _res = main(globals()) + u"\ntrigger: " + (_why or u"-")
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_plant_sheet_log" + _ik] = write_log(_res)
        _ok = not _res.startswith("ERROR")
        _sc.sticky["bergama_plant_sheet_log_status" + _ik] = (time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0)
                                                              if _ok else "ERROR")
        _sc.sticky["bergama_plant_sheet_log_done" + _ik] = done_text(True, _ok, time.time() - _t0)
        _sc.sticky["bergama_plant_sheet_log_ver" + _ik] = VERSION
        try:
            if _ok and _res.split("\n", 1)[0] != "0 warnings":
                ghenv.Component.AddRuntimeMessage(ghenv.Component.RuntimeMessageLevel.Warning, _res.split("\n", 1)[0])
        except Exception:
            pass
    if _sc.sticky.get("bergama_plant_sheet_log_ver" + _ik) != VERSION:
        for _s in ("", "_status", "_done"):
            _sc.sticky.pop("bergama_plant_sheet_log" + _s + _ik, None)
    done = _sc.sticky.get("bergama_plant_sheet_log_done" + _ik, "idle")
    log = _sc.sticky.get("bergama_plant_sheet_log" + _ik, "Press the Button to draw the sheet into " + OUT_DIR)
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(
            "bergama_plant_sheet_log_status" + _ik, "idle")
    except Exception:
        pass
else:
    print(write_log(main(globals())))
