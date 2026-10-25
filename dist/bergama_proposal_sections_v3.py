# -*- coding: utf-8 -*-
"""BERGAMA PROPOSAL SECTIONS v3 (2026-10-25): Group 6's four proposals in section, upstream to downstream, in the
water board's hand-drawn section style (Aras 25 Oct 11:38-11:45: "we want section from each proposal just like our
water board sections"; "the style of waterboard sections were really really good you can do it somewhere else").
For the studio session of 26.10.2026: "Sections: Illustrating the spatial relationships and key design decisions."

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
VERSION = "v3"
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
    ("levels", RR + u" v1.1 table: levels calculated on the surveyed river-height cuts (Manning, main survey TIN)"),
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

def wrap(s, size, width, bold=False):
    out, cur = [], ""
    for wd in s.split():
        t = (cur + " " + wd).strip()
        if cur and text_w(t, size, bold) > width:
            out.append(cur)
            cur = wd
        else:
            cur = t
    if cur:
        out.append(cur)
    return out

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

def write_pdf(pg, path, title):
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    font = []
    for nm in ("Helvetica", "Helvetica-Bold"):
        font.append(add("<< /Type /Font /Subtype /Type1 /BaseFont /{} /Encoding << /Type /Encoding /BaseEncoding "
                        "/WinAnsiEncoding {} >> >>".format(nm, _DIFF).encode("latin-1")))
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 20.0)).encode("latin-1")) for i in range(1, 20)]
    gs_res = " ".join("/A{:02d} {} 0 R".format(i + 1, o_) for i, o_ in enumerate(gs))
    pages_id = add(b"")
    data = zlib.compress(page_stream(pg), 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data +
              b"\nendstream")
    kid = add("<< /Type /Page /Parent {} 0 R /MediaBox [0 0 {} {}] /Contents {} 0 R /Resources << /Font "
              "<< /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >> >> >>".format(pages_id, _f(pg.W / PT), _f(pg.H / PT), cid,
                                                                                    font[0], font[1], gs_res).encode("latin-1"))
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

def _tree_rand(x, y):
    """A small repeatable random stream from the tree's position (the same in every Python)."""
    s = [(int(round(x * 100.0)) * 73856093 ^ int(round(y * 100.0)) * 19349663) & 0x7FFFFFFF or 1]

    def nxt():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7FFFFFFF
        return s[0] / 2147483648.0
    return nxt

# ---------------------------------------------------------------- composing the board from drawn parts
# Every drawing is drawn on its own Page at its natural size (page mm), then placed on the board at one uniform
# scale that fits its box (place). Text, lines and dashes scale with it, as a reduced print does.
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

def place(pg, part, box, max_s=1.0, align="C", log=None, name=""):
    """Puts part (a Page) into box (x0, y0, x1, y1) at the largest scale up to max_s that fits, centred (align C) or
    at the top left (align TL). Returns (scale, placed bbox)."""
    b = items_bbox(part.items)
    bw, bh = max(b[2] - b[0], 1e-6), max(b[3] - b[1], 1e-6)
    s = min(max_s, (box[2] - box[0]) / bw, (box[3] - box[1]) / bh)
    if align == "TL":
        dx, dy = box[0] - s * b[0], box[3] - s * b[3]
    else:
        dx = (box[0] + box[2]) / 2.0 - s * (b[0] + b[2]) / 2.0
        dy = (box[1] + box[3]) / 2.0 - s * (b[1] + b[3]) / 2.0
    pg.items += xform(part.items, s, dx, dy)
    small = min([it[4] for it in part.items if it[0] == "text"] or [9.0]) * s
    if log is not None and small < 1.25:
        log.append(u"NOTE {}: placed at {:.0%} of its drawn size; smallest text {:.1f} mm".format(name, s, small))
    return s, (dx + s * b[0], dy + s * b[1], dx + s * b[2], dy + s * b[3])

# ---------------------------------------------------------------- drawing helpers (page mm, y up)
def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

def node(pg, x, y, n, opt, r=3.2):
    """Element number (the old card numbers, 1-11, on every drawing): a roundel in A, a square in B."""
    d = COL["river_dark"] if n != 10 else COL["ink"]
    if opt == "A":
        pg.circle(x, y, r, fill=COL["white"], stroke=d, lw=0.3)
        pg.circle(x, y, r * 0.74, fill=d)
    else:
        s = r * 0.92
        pg.poly([[(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)]], fill=COL["white"], stroke=d,
                lw=0.3)
        s *= 0.74
        pg.poly([[(x - s, y - s), (x + s, y - s), (x + s, y + s), (x - s, y + s)]], fill=d)
    fs = r * (0.82 if n < 10 else 0.66)
    pg.text(str(n), x, y - fs * CAP / 2, fs, COL["white"], bold=True, align="C")
    return (x - r, y - r, x + r, y + r)

def para(pg, x, y, w, text, size, colour, bold=False, lh=1.28):
    for ln in wrap(text, size, w, bold):
        y -= size * lh
        pg.text(ln, x, y, size, colour, bold=bold)
    return y

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

def sketch_engine():
    if not _SK:
        ns = {"__name__": "pr1_sketches", "_tree_rand": _tree_rand}   # reeds use the trees' random stream
        exec(compile(SKETCH_SRC, "pr1_sketches", "exec"), ns)
        _SK.append(ns)
    return _SK[0]

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

# ================================================================ embedded engines
# SKETCH_SRC: pr1_drawings v3.1's concept sketches (SKETCH style) with a page-item layer instead of Rhino baking;
# owner names, working-area bars and figures printed elsewhere taken out (24 Oct). Run by sketch_engine().
SKETCH_SRC = r'''# The idea sketches of pr1_drawings v3.1 (concept sections, SKETCH style), run in their own namespace: pr1 baked them
# into Rhino; here the same calls make page items. The draw order is pr1's (bake order plus its lifts Z_*).
import math
ZP = []
ORDER = [0]
FORM = "A"
PEOPLE = True
NODE = None                                          # set by the board: the element numbers
CITE = None                                          # v3: set by the board: a source's number "[n]" (footer key)
ORIGIN = (0.0, 0.0)                                  # pr1 placed the sketches beside the site map; here at 0


def _hexc(c):
    return "%02X%02X%02X" % tuple(c)


def _put(item, z):
    ORDER[0] += 1
    ZP.append((ORDER[0] + z, ORDER[0], item))


def P(o, x, y):
    return (o[0] + x, o[1] + y)


def add_polyline(q):
    out = []
    for p in q:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-6:
            out.append((p[0], p[1]))
    return out if len(out) >= 2 else None


def keep(obj, sub, colour, width=None, dashed=False, alpha=None, z=0):
    if obj is None:
        return None
    _put(("line", obj, _hexc(colour), width if width else 0.13, [1.0, 0.7] if dashed else None, 1), z)
    return obj


def pline(o, pts, sub, colour, width=0.18, closed=False, dashed=False, z=0):
    q = [P(o, x, y) for x, y in pts]
    if closed and q[0] != q[-1]:
        q.append(q[0])
    return keep(add_polyline(q), sub, colour, width, dashed, z=z)


def fill(o, pts, sub, colour, alpha=None, boundary=True, z=0, hand_=None):
    if HAND[0] if hand_ is None else hand_:
        pts = hand_ring(pts, sub)
        boundary = False
    ring = [P(o, x, y) for x, y in pts]
    if len(ring) < 3:
        return None
    _put(("poly", [ring], _hexc(colour), None, 0.1, None, None, alpha), z)
    if boundary:
        pline(o, pts, sub, colour, 0.13, closed=True, z=z)
    return ring


def hatch_lines(o, pts, sub, colour, spacing=1.6, angle=45.0, width=None):
    width = LW_HATCH if width is None else width
    for p0, p1 in clip_segments(pts, spacing, angle):
        keep([P(o, *p0), P(o, *p1)], sub, colour, width)


def text(o, s, x, y, size_pt, colour=None, sub="text", just="left", bold=False, mask=None):
    colour = INK if colour is None else colour
    h = size_pt * 0.353
    for i, ln in enumerate(s.split("\n")):
        if ln.strip():
            q = P(o, x, y - i * h * 1.35)
            _put(("text", ln, q[0], q[1], h, _hexc(colour), bold, {"left": "L", "right": "R"}.get(just, "C"), None,
                  _hexc(mask) if mask else None), Z_TEXT)      # pr1's text mask: a halo in its colour


def _smooth(o, pts):
    """A Catmull-Rom curve through the points (pr1: Rhino's interpolated curve), as a fine polyline."""
    q = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(8):
            t = k / 8.0
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    out.append(pts[-1])
    return add_polyline([P(o, x, y) for x, y in out])


def title(o, h, s):
    text(o, s, 0, h + 4, 7.0, INK, "title", bold=True)

def hx(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

INK, INK2 = hx("4A3F35"), hx("847E75")
SOIL, STONE, ROAD = hx("CDBF9F"), hx("A4A1A3"), hx("3A3A3A")
W_SUM, W_WIN, W_EXT = hx("A9C3CC"), hx("7FA7B8"), hx("5C7A86")
REED, ACCENT, HERITAGE, WHITE = hx("89986A"), hx("BC6F45"), hx("8B2D2D"), (255, 255, 255)
CELL, FARM = hx("DFE6CF"), hx("E7E0C8")
def mix(a, b, t):
    """Plain RGB mix of two palette colours (t = share of b), for hatch and outline tones only."""
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

SOIL_HATCH = mix(SOIL, INK, 0.30)      # earth hatch over the soil poché
STONE_HATCH = mix(STONE, INK, 0.35)    # masonry hatch, K4 bridge behind
REED_HEAD = mix(REED, INK, 0.35)       # reed plumes
FIGURE = INK2                          # scale figures
# line weights (print width, mm): what the section cuts is heaviest, what is seen beyond it is thin
LW_CUT, LW_PROFILE, LW_EDGE, LW_BEYOND, LW_FINE, LW_HATCH = 0.50, 0.35, 0.25, 0.13, 0.09, 0.05
Z_TREE, Z_LINE, Z_PEOPLE, Z_TEXT = 300000, 400000, 600000, 900000   # draw-order lifts: trees, lines, people, texts
def clip_segments(pts, spacing, angle):
    """The pieces of parallel lines (spacing, angle in degrees) that lie inside a closed outline."""
    segs = []
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    r = [(x * ca + y * sa, -x * sa + y * ca) for x, y in pts]       # outline turned so the hatch runs along x
    if r[0] != r[-1]:
        r.append(r[0])
    ys = [p[1] for p in r]
    k = int(math.floor(min(ys) / spacing)) + 1
    while k * spacing < max(ys):
        yy = k * spacing
        xs = sorted(x1 + (yy - y1) * (x2 - x1) / (y2 - y1) for (x1, y1), (x2, y2) in zip(r[:-1], r[1:])
                    if (y1 <= yy < y2) or (y2 <= yy < y1))
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 0.05:
                p0 = (xs[i] * ca - yy * sa, xs[i] * sa + yy * ca)
                p1 = (xs[i + 1] * ca - yy * sa, xs[i + 1] * sa + yy * ca)
                segs.append((p0, p1))
        k += 1
    return segs

def notch(g, cuts):
    """Ground outline g with rectangular basins cut into its level stretches: cuts = [(x0, x1, y_top, depth)]."""
    out = list(g)
    for x0, x1, y, d in cuts:
        for i in range(len(out) - 1):
            (ax, ay), (bx, by) = out[i], out[i + 1]
            if abs(ay - y) < 1e-9 and abs(by - y) < 1e-9 and min(ax, bx) <= x0 and x1 <= max(ax, bx):
                ins = [(x0, y), (x0, y - d), (x1, y - d), (x1, y)]
                ins = ins if ax < bx else ins[::-1]
                ins = [p for p in ins if p != out[i] and p != out[i + 1]]
                out[i + 1:i + 1] = ins
                break
    return out

def surface_y(surface, x):
    """Height of the ground surface at x (on a vertical step: the lower of the two)."""
    ys = [ay + (by - ay) * (x - ax) / (bx - ax) for (ax, ay), (bx, by) in zip(surface[:-1], surface[1:])
          if bx != ax and min(ax, bx) <= x <= max(ax, bx)]
    return min(ys) if ys else None

def surface_between(surface, x0, x1, dy=0.0):
    """The surface from x0 to x1 (steps inside kept, risers at the two ends dropped), lifted by dy."""
    out = []
    for (ax, ay), (bx, by) in zip(surface[:-1], surface[1:]):
        if max(ax, bx) < x0 or min(ax, bx) > x1:
            continue
        if ax == bx:
            seg = [(ax, ay), (bx, by)]
        else:
            seg = []
            for x in (max(min(ax, bx), x0), min(max(ax, bx), x1)) if ax < bx else (min(max(ax, bx), x1), max(min(ax, bx), x0)):
                seg.append((x, ay + (by - ay) * (x - ax) / (bx - ax)))
        for q in seg:
            if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > 1e-9:
                out.append(q)
    while len(out) > 2 and out[0][0] == out[1][0]:
        out.pop(0)
    while len(out) > 2 and out[-1][0] == out[-2][0]:
        out.pop()
    return [(x, y + dy) for x, y in out]

def reeds(o, x0, x1, y, h=3.5, plan=False):
    """Reed clumps at v2.8's spacing and height: a fan of thin arched blades of mixed height, a plume on every third
    clump. plan=True (form plans): a small tuft of radiating leaves seen from above."""
    rnd = _tree_rand(x0 + 0.37 * x1, y)
    n = max(3, int((x1 - x0) / 1.6))
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        if plan:
            m = 6 + int(rnd() * 3)
            for j in range(m):
                t = 6.283 * (j + 0.4 * rnd()) / m
                L = h * 0.38 * (0.6 + 0.4 * rnd())
                keep([P(o, x, y), P(o, x + L * math.cos(t), y + L * math.sin(t))], "planting", REED, LW_FINE)
            continue
        nb = 5 + int(rnd() * 3)
        tall = None
        for j in range(nb):
            s = (j / (nb - 1.0) - 0.5) * 2.0 + (rnd() - 0.5) * 0.35       # -1 .. 1: leaning left .. right
            hh = h * (0.62 + 0.38 * rnd()) * (1.0 - 0.18 * abs(s))
            pts = [(x + 0.12 * s + s * hh * 0.42 * t * t, y + hh * (t - 0.10 * abs(s) * t * t)) for t in (0.0, 0.35, 0.7, 1.0)]
            keep(_smooth(o, pts), "planting", REED, LW_FINE)
            if tall is None or hh > tall[0]:
                tall = (hh, pts)
        if i % 3 == 1 and tall:                    # plume along the tallest blade's tip
            (ax, ay), (bx, by) = tall[1][-2], tall[1][-1]
            L = math.hypot(bx - ax, by - ay) or 1.0
            ux, uy = (bx - ax) / L, (by - ay) / L
            ln, wd = 0.30 * h, 0.05 * h
            cx, cy = bx + ux * ln * 0.5, by + uy * ln * 0.5
            fill(o, [(bx, by), (cx - uy * wd, cy + ux * wd), (bx + ux * ln, by + uy * ln), (cx + uy * wd, cy - ux * wd)],
                 "planting", REED_HEAD, boundary=False)

def bank(p, q, n=24):
    """Edge where the project meets the water: S-curve in form A, one straight facet in form B."""
    if FORM == "B":
        return [p, q]
    out = []
    for i in range(n):
        t = i / (n - 1.0)
        s = (1 - math.cos(t * math.pi)) / 2
        out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * s))
    return out

def road(o, x0, x1, y, label, ly=None, mask=None):
    fill(o, [(x0, y), (x1, y), (x1, y + 1.3), (x0, y + 1.3)], "road", ROAD)
    text(o, label, x0 + 1, ly if ly is not None else y - 2.5, 5.0, ROAD, "road", mask=mask)

def level_mark(o, x, y, colour, sub):
    """Level sign: a small open triangle standing point-down on the level line."""
    pline(o, [(x - 1.0, y + 1.7), (x + 1.0, y + 1.7), (x, y)], sub, colour, LW_BEYOND, closed=True, z=Z_LINE)

HAND_AMP = 0.18          # mm: sideways wobble of a hand line
HAND_WAV = 7.0           # mm: length of one wobble
HAND_OVER = 1.1          # mm: how far a stroke runs past its corner
HAND_FONT = ["Ink Free", "Segoe Print", "Comic Sans MS"]   # first one installed (Windows 10/11 ship Ink Free)
PEN_HAIR, PEN_FINE, PEN_MED, PEN_BOLD = 0.13, 0.20, 0.40, 0.70   # masterplan v9 pens (mm)
SKINK = hx("1E1E1E")                                 # fine-liner black: the line that carries the idea
SUN, SUN_RAY = hx("E8C64A"), hx("C9A227")           # the dry summer (Aras): marker yellow
HAND = [False]                                       # True while a part is drawn by hand (form plans: pline / fill wobble)
HAND_TEXT = [False]                                  # True while texts take the hand font and drop their masks
KHAKI, PAPER, BG_ = hx("BCB794"), hx("F1EDDF"), hx("E6E0C8")
SEC_POCHE = mix(KHAKI, PAPER, 0.62)                  # board: the cut ground
SEC_POCHE_BAND = mix(SEC_POCHE, KHAKI, 0.45)          # the band just under the surface, a little deeper
SEC_PAVE = mix(hx("BC6F45"), BG_, 0.12)              # board: walkable edge, terracotta
SEC_CHANNEL_HATCH = hx("3E7DAE")                     # board: the stream bed's blue hatch
SITE_WATER, SITE_WATER_D, SITE_FLOOD = hx("7FA4B3"), hx("5E8494"), hx("B4CBD2")   # board CAT water, BLUE_D, BLUE_L
FLOOD_WASH, FLOOD_ALPHA = hx("4F9BD9"), 0.09         # the design flood's reach up to Q500: one clear blue, see-through
                                                      # and so faint it takes a moment to see (Nil 17:59: "really really faint blue,
                                                      # almost indistinguishable ... should need a focus to see"); raise FLOOD_ALPHA = stronger
SITE_PEOPLE = mix(hx("7A6E60"), BG_, 0.1)            # board: SA_STYLE_BOARD people
SITE_TREE = (hx("B2C484"), hx("8CA466"), hx("688052"))   # board SA_TREE_PAL["tree"]: light, mid, shadow
SITE_TRUNK = hx("6E625A")                            # board SA_TRUNK
HOUSE_WALL, HOUSE_ROOF = hx("D9B98C"), hx("A86A55")  # board TYPO["traditional"] tone, TYPO_ROOF_C
SA_FIGS = [                                          # board SA_FIGS (m, 1.75 m tall), SA_HEAD
    [(-0.10, 0.0), (-0.06, 0.0), (-0.03, 0.82), (0.03, 0.82), (0.06, 0.0), (0.10, 0.0), (0.12, 0.85), (0.16, 1.38),
     (0.10, 1.47), (0.05, 1.50), (0.05, 1.53), (-0.05, 1.53), (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.12, 0.85)],
    [(-0.30, 0.0), (-0.24, 0.0), (-0.02, 0.78), (0.18, 0.0), (0.25, 0.0), (0.11, 0.86), (0.18, 1.12), (0.12, 1.40),
     (0.06, 1.48), (0.05, 1.53), (-0.05, 1.53), (-0.07, 1.47), (-0.14, 1.38), (-0.20, 1.10), (-0.12, 0.86)],
    [(-0.20, 0.0), (0.20, 0.0), (0.13, 0.62), (0.11, 1.08), (0.15, 1.36), (0.09, 1.45), (0.05, 1.49), (0.05, 1.52),
     (-0.05, 1.52), (-0.05, 1.49), (-0.09, 1.45), (-0.15, 1.36), (-0.11, 1.08), (-0.13, 0.62)],
    [(-0.11, 0.0), (-0.06, 0.0), (-0.02, 0.80), (0.04, 0.80), (0.08, 0.0), (0.13, 0.0), (0.12, 0.86), (0.30, 0.86),
     (0.30, 0.55), (0.40, 0.55), (0.40, 0.95), (0.17, 1.38), (0.10, 1.47), (0.05, 1.51), (0.05, 1.53), (-0.05, 1.53),
     (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.13, 0.86)],
]
SA_HEAD = (0.0, 1.64, 0.105)

import zlib as _zlib, random as _random
def _seed(*parts):
    return _zlib.crc32(repr([round(float(v), 2) if isinstance(v, float) else v for v in parts]).encode("utf-8")) & 0x7fffffff

def _densify(P, step):
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / step)))
        out += [(a[0] + (b[0] - a[0]) * k / float(n), a[1] + (b[1] - a[1]) * k / float(n)) for k in range(1, n + 1)]
    return out

def _normals(a):
    out = []
    for i in range(len(a)):
        p, q = a[max(0, i - 1)], a[min(len(a) - 1, i + 1)]
        d = math.hypot(q[0] - p[0], q[1] - p[1]) or 1e-12
        out.append((-(q[1] - p[1]) / d, (q[0] - p[0]) / d))
    return out

def _noise(n, step, wav, rnd):
    """n values of smooth noise (std about 1), features about wav long (masterplan smooth_noise)."""
    k = max(2, int(math.ceil(n * step / wav)) + 3)
    ctrl = [rnd.gauss(0.0, 1.0) for _ in range(k)]
    out = []
    for j in range(n):
        x = j * step / wav
        i = min(int(x), k - 2)
        f = x - i
        f = f * f * (3 - 2 * f)
        out.append(ctrl[i] * (1 - f) + ctrl[i + 1] * f)
    return out

def hand(P, amp, wav, seed, closed=False, over=0.0):
    """A polyline as a hand draws it (masterplan hand_line): smooth sideways wobble of about amp (at most 2.2 amp),
    an overshoot of `over` at both ends of an open line; a closed ring starts at a random point."""
    a = [(float(p[0]), float(p[1])) for p in P]
    if len(a) < 2:
        return a
    rnd = _random.Random(seed)
    step = max(wav / 6.0, 1e-6)
    if closed:
        if math.hypot(a[0][0] - a[-1][0], a[0][1] - a[-1][1]) < 1e-9:
            a = a[:-1]
        k = rnd.randrange(len(a))
        a = a[k:] + a[:k] + [a[k]]
    a = _densify(a, step)
    if over > 0 and not closed:
        (x0, y0), (x1, y1) = a[0], a[1]
        d = math.hypot(x1 - x0, y1 - y0) or 1e-12
        s = (x0 - (x1 - x0) / d * over, y0 - (y1 - y0) / d * over)
        (x0, y0), (x1, y1) = a[-1], a[-2]
        d = math.hypot(x1 - x0, y1 - y0) or 1e-12
        a = [s] + a + [(x0 - (x1 - x0) / d * over, y0 - (y1 - y0) / d * over)]
    if amp > 0:
        w = [max(-2.2, min(2.2, v)) * amp for v in _noise(len(a), step, wav, rnd)]
        a = [(p[0] + n[0] * v, p[1] + n[1] * v) for p, n, v in zip(a, _normals(a), w)]
    return a

def _strokes(P, closed, turn=28.0):
    """A polyline split at its corners, as a hand draws it: one stroke per straight run."""
    P = list(P) + ([P[0]] if closed and P[0] != P[-1] else [])
    out = [[P[0]]]
    for i in range(1, len(P) - 1):
        a, b, c = P[i - 1], P[i], P[i + 1]
        t1, t2 = math.atan2(b[1] - a[1], b[0] - a[0]), math.atan2(c[1] - b[1], c[0] - b[0])
        out[-1].append(b)
        if abs((math.degrees(t2 - t1) + 180) % 360 - 180) > turn:
            out.append([b])
    out[-1].append(P[-1])
    return [s for s in out if len(s) > 1]

def _crosses(ring):
    """True when a closed ring crosses itself (a hatch from it would fail or fill wrongly)."""
    q = list(ring) + ([ring[0]] if ring[0] != ring[-1] else [])
    E = list(zip(q[:-1], q[1:]))
    box = [(min(a[0], b[0]), max(a[0], b[0]), min(a[1], b[1]), max(a[1], b[1])) for a, b in E]

    def o_(p, r, t):
        return (r[0] - p[0]) * (t[1] - p[1]) - (r[1] - p[1]) * (t[0] - p[0])
    m = len(E)
    for i in range(m):
        a, b = E[i]
        bi = box[i]
        for j in range(i + 2, m):
            if i == 0 and j == m - 1:
                continue
            bj = box[j]
            if bi[1] < bj[0] or bj[1] < bi[0] or bi[3] < bj[2] or bj[3] < bi[2]:
                continue
            c, d = E[j]
            if o_(a, b, c) * o_(a, b, d) < -1e-12 and o_(c, d, a) * o_(c, d, b) < -1e-12:
                return True
    return False

def hand_ring(pts, sub, amp=HAND_AMP, wav=HAND_WAV):
    """A closed outline drawn by hand; where the wobble would make it cross itself (narrow or sharp shapes), a smaller
    wobble, else the true outline."""
    sd = _seed(pts[0][0], pts[0][1], len(pts), sub)
    for k in (1.0, 0.5, 0.25):
        r = hand(pts, amp * k, wav, sd, closed=True)
        if not _crosses(r):
            return r
    return list(pts)

def sketch(o, pts, sub, colour, width=0.25, closed=False, over=HAND_OVER, amp=HAND_AMP, retrace=True, z=0,
           dashed=False):
    """Fine-liner line: each straight run its own stroke, wobbling and running past the corners; long runs are
    traced a second time, lighter and not quite end to end, as a sketch is."""
    for k, s in enumerate(_strokes(pts, closed)):
        sd = _seed(s[0][0], s[0][1], s[-1][0], s[-1][1], k, sub)
        q = hand(s, amp, HAND_WAV, sd, over=over)
        keep(add_polyline([P(o, *p) for p in q]), sub, colour, width, dashed, z=z)
        L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(s[:-1], s[1:]))
        if retrace and not dashed and L > 6.0:
            rnd = _random.Random(sd + 7)
            q = hand(s, amp * 1.6, HAND_WAV * 0.8, sd + 11, over=over * 0.5)
            i0, i1 = int(len(q) * 0.15 * rnd.random()), len(q) - int(len(q) * 0.25 * rnd.random())
            if i1 - i0 > 1:
                keep(add_polyline([P(o, *p) for p in q[i0:i1]]), sub, colour, width * 0.45, z=z)

def wash(o, poly, sub, colour, alpha=0.5, z=0):
    """Watercolour wash: a see-through fill whose edge wobbles a little past the true outline."""
    ring = hand_ring(poly, sub, HAND_AMP * 1.8, HAND_WAV * 1.6)
    return fill(o, ring, sub, colour, alpha=alpha, boundary=False, z=z, hand_=False)

def marker(o, poly, sub, colour, angle=55.0, spacing=0.75, thick=0.62, alpha=0.55, base=0.22, z=0):
    """Marker fill: parallel strokes laid side by side at a slant, each a little longer or shorter than the shape
    (and slightly turned), over a faint wash of the same colour: the key element of a sketch (example 4)."""
    if base:
        wash(o, poly, sub, colour, base, z)
    rnd = _random.Random(_seed(poly[0][0], poly[0][1], angle, sub))
    for p0, p1 in clip_segments(poly, spacing, angle):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        if L < 0.2:
            continue
        ux, uy = dx / L, dy / L
        a0, a1 = (rnd.random() - 0.35) * 0.9, (rnd.random() - 0.35) * 0.9
        tw = (rnd.random() - 0.5) * 0.35
        s = (p0[0] - ux * a0, p0[1] - uy * a0)
        e = (p1[0] + ux * a1 - uy * tw, p1[1] + uy * a1 + ux * tw)
        nx, ny = -uy * thick / 2, ux * thick / 2
        fill(o, [(s[0] + nx, s[1] + ny), (e[0] + nx, e[1] + ny), (e[0] - nx, e[1] - ny), (s[0] - nx, s[1] - ny)],
             sub, colour, alpha=alpha, boundary=False, z=z, hand_=False)

def band(surface, x0, x1, depth):
    """Polygons of a band `depth` under the ground surface from x0 to x1 (split at vertical steps)."""
    seg = surface_between(surface, x0, x1)
    pieces, cur = [], [seg[0]] if seg else []
    for q in seg[1:]:
        if abs(q[0] - cur[-1][0]) < 1e-9:
            pieces.append(cur)
            cur = [q]
        else:
            cur.append(q)
    if cur:
        pieces.append(cur)
    return [pc + [(x, y - depth) for x, y in pc[::-1]] for pc in pieces if len(pc) > 1]

def under_level(surface, x0, x1, level):
    """The space between the ground and a level, x0..x1 (what that level puts under water)."""
    bed = [(x, min(level, y)) for x, y in surface_between(surface, x0, x1)]
    return [(x0, level), (x1, level)] + bed[::-1] if len(bed) > 1 else None

def hand_arrow(o, a, b, colour, sub="arrows", width=0.55, head=2.2, z=Z_LINE, bend=0.0):
    """Link arrow in the masterplan v9 manner (head barbs at 38 deg), drawn as filled marker shapes so it reads at
    every zoom and in the viewport, where print widths do not show (Nil 18 Oct 17:55: "the outflow drainage is gone"):
    a hand-wobbled shaft `width` wide that tapers a little towards the tip (bend > 0 bows it), and a solid head."""
    pts = [a, b]
    if bend:
        m = ((a[0] + b[0]) / 2.0 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2.0 + (b[0] - a[0]) * bend)
        pts = [(a[0] * (1 - t) ** 2 + 2 * m[0] * t * (1 - t) + b[0] * t * t, a[1] * (1 - t) ** 2 + 2 * m[1] * t * (1 - t) + b[1] * t * t)
               for t in [i / 24.0 for i in range(25)]]
    t = math.atan2(b[1] - pts[-2][1], b[0] - pts[-2][0])
    hl = head * math.cos(math.radians(38))                 # the head's length along the shaft
    L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts[:-1], pts[1:]))
    shaft, acc = [pts[0]], 0.0
    for p, q in zip(pts[:-1], pts[1:]):
        d = math.hypot(q[0] - p[0], q[1] - p[1])
        if acc + d >= L - hl * 0.7:
            f = (L - hl * 0.7 - acc) / (d or 1e-12)
            shaft.append((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f))
            break
        shaft.append(q)
        acc += d
    sh = hand(shaft, HAND_AMP * 0.5, HAND_WAV, _seed(a[0], a[1], b[0], b[1], sub))
    nm = _normals(sh)
    n = len(sh)
    w_ = [width * (1.0 - 0.3 * i / max(1, n - 1)) / 2.0 for i in range(n)]
    left = [(p[0] + v[0] * w, p[1] + v[1] * w) for p, v, w in zip(sh, nm, w_)]
    right = [(p[0] - v[0] * w, p[1] - v[1] * w) for p, v, w in zip(sh, nm, w_)]
    fill(o, left + right[::-1], sub, colour, boundary=False, z=z, hand_=False)
    tip = (b[0] + math.cos(t) * 0.2, b[1] + math.sin(t) * 0.2)
    wings = [(b[0] - head * math.cos(t + sg * math.radians(38)), b[1] - head * math.sin(t + sg * math.radians(38))) for sg in (1, -1)]
    notch_ = (b[0] - hl * 0.7 * math.cos(t), b[1] - hl * 0.7 * math.sin(t))
    fill(o, [tip, wings[0], notch_, wings[1]], sub, colour, boundary=False, z=z, hand_=False)

def sun(o, x, y, r=2.2):
    """The dry summer: a marker-yellow sun with short hand rays (as in Nil's SNFCC sketch)."""
    disc_ = [(x + r * math.cos(6.283 * i / 20), y + r * math.sin(6.283 * i / 20)) for i in range(20)]
    wash(o, disc_, "sun", SUN, 0.85, z=Z_LINE)
    sketch(o, disc_, "sun", SKINK, PEN_FINE, closed=True, over=0.0, amp=0.08, retrace=False, z=Z_LINE)
    for k in range(9):
        t = 6.283 * (k + 0.3) / 9
        sketch(o, [(x + 1.45 * r * math.cos(t), y + 1.45 * r * math.sin(t)), (x + 2.1 * r * math.cos(t), y + 2.1 * r * math.sin(t))],
               "sun", SKINK, PEN_FINE, over=0.0, amp=0.03, retrace=False, z=Z_LINE)

def cloud_rain(o, x, y, r=1.0):
    """v3: the wet winter, a hand cloud with three rain strokes, centred at (x, y)."""
    pts = []
    for i in range(28):
        a = 6.283 * i / 28
        k = 1.0 + 0.24 * max(0.0, math.sin(a)) * abs(math.sin(3 * a))
        pts.append((x + 1.6 * r * math.cos(a) * k, max(y - 0.5 * r, y + 0.85 * r * math.sin(a) * k)))
    wash(o, pts, "season", SITE_FLOOD, 0.85, z=Z_LINE)
    sketch(o, pts, "season", SKINK, PEN_FINE, closed=True, over=0.0, amp=0.05, retrace=False, z=Z_LINE)
    for dx in (-0.8, 0.0, 0.8):
        sketch(o, [(x + dx * r, y - 0.8 * r), (x + dx * r - 0.35 * r, y - 1.8 * r)], "season", SITE_WATER_D, PEN_FINE,
               over=0.0, amp=0.02, retrace=False, z=Z_LINE)

def failsafe_mark(o, x, y, r=1.4):
    """v3: the fail-safe mark, an accent ring with a step and the water spilling over it."""
    ring = [(x + r * math.cos(6.283 * i / 20), y + r * math.sin(6.283 * i / 20)) for i in range(20)]
    sketch(o, ring, "fail-safe", ACCENT, PEN_FINE, closed=True, over=0.0, amp=0.05, retrace=False, z=Z_LINE)
    sketch(o, [(x - 0.75 * r, y + 0.3 * r), (x - 0.1 * r, y + 0.3 * r), (x - 0.1 * r, y - 0.45 * r), (x + 0.75 * r, y - 0.45 * r)],
           "fail-safe", SKINK, PEN_FINE, over=0.0, amp=0.03, retrace=False, z=Z_LINE)
    hand_arrow(o, (x - 0.55 * r, y + 0.55 * r), (x + 0.25 * r, y - 0.15 * r), ACCENT, width=0.16, head=0.55, bend=-0.3)

def keyed(o, kind, s, x, y, size_pt, colour=None, sub="text", mask=None):
    """v3: a keyword callout led by a hand pictogram at its first line: "winter" (cloud and rain), "summer" (the
    sun) or "failsafe". The text starts a little to the right of x."""
    h = size_pt * 0.353
    cx, cy = x + 1.1 * h, y + 0.36 * h
    if kind == "winter":
        cloud_rain(o, cx, cy + 0.15 * h, 0.5 * h)
    elif kind == "summer":
        sun(o, cx, cy, 0.36 * h)
    elif kind == "failsafe":
        failsafe_mark(o, cx, cy, 0.62 * h)
    text(o, s, x + 2.4 * h, y, size_pt, colour, sub, mask=mask)

def tick_dim(o, x, y0, y1, colour=INK2):
    """Sketch dimension: a vertical line with slashed ticks at both ends (example 4); no figure."""
    sketch(o, [(x, y0), (x, y1)], "dimensions", colour, LW_BEYOND, over=0.9, retrace=False, z=Z_LINE)
    for y in (y0, y1):
        sketch(o, [(x - 0.9, y - 0.9), (x + 0.9, y + 0.9)], "dimensions", colour, LW_EDGE, over=0.0, retrace=False, z=Z_LINE)

def sketch_ground(o, g, sub="ground"):
    """Ground: the board's poché, solid (a see-through ground shows the viewport through it and the band under the
    surface then reads as a gap, Nil 18 Oct 17:46), a slightly deeper band under the surface, and short earth strokes
    just under the line (the surface line itself: drawn by the caller)."""
    surf = g[1:-1]
    wash(o, g, sub, SEC_POCHE, None)
    floor = min(p[1] for p in g)
    for pc in band(surf, surf[0][0], surf[-1][0], 3.0):
        pc = [(x, max(floor, y)) for x, y in pc]           # never below the drawn ground (low-flow channel)
        if not _crosses(pc):
            wash(o, pc, sub, SEC_POCHE_BAND, None)
    rnd = _random.Random(_seed(surf[0][0], surf[-1][0], len(surf)))
    for (ax, ay), (bx, by) in zip(surf[:-1], surf[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 3.0 or abs(bx - ax) < 0.5 * L:
            continue
        n = int(L / 3.2)
        for k in range(n):
            t = (k + 0.3 + 0.4 * rnd.random()) / n
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t - 0.7
            sketch(o, [(x, y), (x - 1.1, y - 1.1)], sub + " hatch", INK2, LW_HATCH * 2, over=0.0, amp=0.05, retrace=False)
    return surf

def sketch_tree(o, x, y, h):
    """Loose tree: a crown of washes in the board's tree greens, a scribbled outline and a trunk with two limbs."""
    rnd = _random.Random(_seed(x, y, h))
    cx, cy, rx, ry = x, y + 0.64 * h, 0.36 * h, 0.30 * h
    ph = [rnd.uniform(0, 6.3) for _ in range(3)]
    crown = []
    for q in range(36):                                  # board _sa_lumpy
        a = 6.283 * q / 36
        k = 1.0 + 0.12 * (math.sin(5 * a + ph[0]) + 0.6 * math.sin(8 * a + ph[1]) + 0.4 * math.sin(13 * a + ph[2])) / 2.0
        crown.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
    for (sx, sy, col, al) in ((0.0, 0.0, SITE_TREE[1], 0.55), (-0.18, 0.2, SITE_TREE[0], 0.5), (0.2, -0.22, SITE_TREE[2], 0.35)):
        part = [(cx + (px - cx) * 0.62 + sx * rx, cy + (py - cy) * 0.62 + sy * ry) for px, py in crown]
        wash(o, part if al < 0.55 else crown, "planting", col, al, z=Z_TREE)
    sketch(o, crown, "planting", SITE_TREE[2], LW_FINE, closed=True, over=0.0, amp=0.25, retrace=False, z=Z_TREE)
    sketch(o, [(x, y), (x + 0.15, cy - 0.1 * h)], "planting", SITE_TRUNK, LW_EDGE, over=0.0, retrace=False, z=Z_TREE)
    for s in (-1, 1):
        sketch(o, [(x + 0.1, cy - 0.25 * h), (x + s * 0.22 * h, cy + 0.05 * h)], "planting", SITE_TRUNK, LW_FINE,
               over=0.0, retrace=False, z=Z_TREE)

def sketch_person(o, x, y, h=4.5, kind=0, flip=False):
    """Board scale figure (SA_FIGS) at the drawing's figure height h."""
    s = h / 1.745
    sg = -1.0 if flip else 1.0
    if not PEOPLE:
        return
    fill(o, [(x + sg * bx * s, y + by * s) for bx, by in SA_FIGS[kind % len(SA_FIGS)]], "people", SITE_PEOPLE,
         alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)
    hx_, hy_, hr = SA_HEAD
    fill(o, [(x + sg * hx_ * s + hr * s * math.cos(6.283 * i / 12), y + hy_ * s + hr * s * math.sin(6.283 * i / 12))
             for i in range(12)], "people", SITE_PEOPLE, alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)

def sketch_house(o, x0, x1, y, wall=6.0, pipe=False):
    """Context: an old town house beyond the street (board TYPO "traditional": stone base, hipped tile roof, deep
    eaves), generic, not surveyed. pipe=True adds the downpipe that takes its roof water to the street."""
    ev, rise = 0.9, 2.6
    body = [(x0, y), (x1, y), (x1, y + wall), (x0, y + wall)]
    roof = [(x0 - ev, y + wall), (x1 + ev, y + wall), (x1 - 2.2, y + wall + rise), (x0 + 2.2, y + wall + rise)]
    wash(o, body, "context", HOUSE_WALL, 0.45)
    marker(o, roof, "context", HOUSE_ROOF, angle=-35.0, spacing=0.6, thick=0.5, alpha=0.45, base=0.25)
    sketch(o, body, "context", INK2, LW_FINE, closed=True)
    sketch(o, roof, "context", INK2, LW_FINE, closed=True)
    sketch(o, [(x0, y + 1.0), (x1, y + 1.0)], "context", INK2, LW_HATCH * 2, over=0.4, retrace=False)
    for wx in (x0 + 0.28 * (x1 - x0), x0 + 0.62 * (x1 - x0)):
        sketch(o, [(wx, y + 2.2), (wx + 1.3, y + 2.2), (wx + 1.3, y + 4.6), (wx, y + 4.6)], "context", INK2, LW_HATCH * 2,
               closed=True, over=0.3, retrace=False)
    if pipe:
        sketch(o, [(x1 + 0.6, y + wall), (x1 + 0.6, y + 0.3)], "context", SITE_WATER_D, LW_EDGE, over=0.0, retrace=False)

def rain(o, x0, x1, y0, y1, n=14):
    rnd = _random.Random(_seed(x0, x1, y0, y1))
    for _ in range(n):
        x, y = x0 + rnd.random() * (x1 - x0), y0 + rnd.random() * (y1 - y0)
        sketch(o, [(x, y), (x - 0.5, y - 1.6)], "rain", SITE_WATER_D, LW_FINE, over=0.0, amp=0.04, retrace=False)

def water_body(surface, xs, level):
    """The water standing at `level` around x = xs: from where the ground on the left rises through the level to
    where it does on the right (banks, walls, the low-flow channel), following the bed in between. So the water always
    meets its banks (Nil 18 Oct 17:55: the water did not meet the left bank)."""
    k = None
    for i, ((ax, ay), (bx, by)) in enumerate(zip(surface[:-1], surface[1:])):
        if ax != bx and min(ax, bx) <= xs <= max(ax, bx):
            y = ay + (by - ay) * (xs - ax) / (bx - ax)
            if y < level and (k is None or y < k[1]):
                k = (i, y)
    if k is None:
        return None

    def cross(p, q):                                  # p under the level, q at or over it
        if abs(q[1] - p[1]) < 1e-12:
            return (q[0], level)
        t = (level - p[1]) / (q[1] - p[1])
        return (p[0] + (q[0] - p[0]) * t, level)
    i = k[0]
    left, right = [], []
    j = i
    while j >= 0 and surface[j][1] < level:
        left.append(surface[j])
        j -= 1
    left.append(cross(left[-1] if left else (xs, k[1]), surface[j]) if j >= 0 else (surface[0][0], level))
    j = i + 1
    while j < len(surface) and surface[j][1] < level:
        right.append(surface[j])
        j += 1
    right.append(cross(right[-1] if right else (xs, k[1]), surface[j]) if j < len(surface) else (surface[-1][0], level))
    bed = left[::-1] + right
    out = []
    for p in bed:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-9:
            out.append(p)
    return out                                        # first and last point on the level, the bed between

def water_level(o, surface, xs, level, colour, bed_hatch=False, line=True):
    """Water at `level` around xs, cut exactly to the ground (solid), a hand surface line; bed_hatch: the board's blue
    hatch over the stream bed."""
    pts = water_body(surface, xs, level)
    if not pts or len(pts) < 3:
        return None
    fill(o, pts, "water", colour, boundary=False, hand_=False)
    if bed_hatch:
        hatch_lines(o, pts, "water", SEC_CHANNEL_HATCH, 1.1, 45.0, PEN_HAIR)
    if line:
        sketch(o, [pts[0], pts[-1]], "water lines", SITE_WATER_D, PEN_FINE, over=0.0, retrace=False, z=Z_LINE)
    return pts

def concept_aras_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_aras_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_aras_sketch():
    """PROBLEM: the bed is dry in summer, the winter runoff leaves the streets. MOVE: the bank becomes a cascade that
    holds the winter water, cleans it in reed basins and gives it back to the summer river."""
    o, w = ORIGIN, 200
    title(o, 82, "UPSTREAM ENTRY · collect, clean and hold · form " + FORM)
    g = [(0, 8), (0, 64), (34, 64), (34, 52), (68, 52), (68, 40), (102, 40), (102, 28), (130, 28)] + bank((130, 28), (140, 12))[1:] + \
        [(170, 12), (170, 28), (w, 28), (w, 8)]
    basins = ((40, 52), (74, 40), (108, 28))
    # the summer strip runs in a low-flow channel cut into the bed (v2.8: 150-160, 2.2 deep)
    gs = sketch_ground(o, notch(g, [(x0, x0 + 22, y, 5) for x0, y in basins] + [(150, 160, 12, 2.2)]))
    # winter: rain on the old town's roofs and street (context house generic, not surveyed)
    rain(o, 6, 33, 67.5, 73.5, 16)
    sketch_house(o, 15, 27, 65.3, wall=5.0, pipe=True)
    road(o, 0, 30, 64, "ROAD " + CITE("survey") + "\nschematic", ly=61.5, mask=SOIL)
    # Q500's reach first (solid wash), so the basins' water and reeds stay on top of it
    for pc in [under_level(gs, 102, w, 31.5)]:
        if pc:
            wash(o, pc, "flood", FLOOD_WASH, FLOOD_ALPHA)
    # the move: the cascade of reed basins (marker band = what holds and cleans the water)
    for x0, y in basins:
        water_level(o, gs, x0 + 11, y - 0.4, W_WIN)
        reeds(o, x0 + 1, x0 + 21, y - 5, 3.2)
    for pc in band(gs, 34, 130, 1.6):
        marker(o, pc, "terraces", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    sketch_tree(o, 65, 52, 9); sketch_tree(o, 99, 40, 7)    # on the strips between the basins, above Q500's reach
    # summer: the river (dry bed today) gets the clean water back
    water_level(o, gs, 155, 19, W_WIN, bed_hatch=True)
    water_level(o, gs, 155, 12, W_EXT, line=False)
    sun(o, 188, 58)
    sketch_person(o, 13, 65.3, kind=1); sketch_person(o, 70.8, 40)               # never inside water or the Q500 reach
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    keyed(o, "winter", "winter flow", 172, 24, 5.6, W_EXT, "water")
    keyed(o, "summer", "low-flow strip\nregulated release\ntoday: dry bed", 172, 19, 5.6, W_EXT, "water")
    sketch(o, [(102, 31.5), (w, 31.5)], "flood lines", HERITAGE, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 123.8, 31.5, HERITAGE, "flood lines")
    # v3 fix (audit problem 3): the surveyed ARAS cut keeps Q500 inside the banks (rain_river_levels README v1.1
    # line 21); the lowest terrace floods only if it is set below that level
    text(o, "Q500 +73.66 m · 3.30 m · inside the banks " + CITE("levels") + "\nlowest terrace floods only if set below it",
         126, 35.6, 5.0, HERITAGE, "flood")
    hand_arrow(o, (8, 72), (44, 56), SITE_WATER_D, bend=0.12)
    keyed(o, "winter", "street + roof runoff · Nov-Feb 59.1 % of rain " + CITE("rain") + "\nreed basins clean it with river water",
          6, 77.4, 5.8)
    hand_arrow(o, (126, 31), (150, 20), SITE_WATER_D, bend=-0.15)
    keyed(o, "summer", "regulated release · continuous strip\nJun-Sep 7.4 % of rain " + CITE("rain") + "\nriver below runs clean",
          109, 47, 5.8)
    for a, b in (((64, 49), (66, 44)), ((98, 37), (100, 32)), ((130, 26), (141, 18))):
        hand_arrow(o, a, b, ACCENT, width=0.4, head=1.5, bend=-0.2)
    keyed(o, "failsafe", "FAIL-SAFE\nfull basin: spills to the next\nlast basin: into the channel\nflood flow bypasses the reeds\ngravity · no pumps",
          2, 31, 5.8, ACCENT, mask=SOIL)
    text(o, "hold in winter,\ngive back in summer", 46, 21, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((2, 51, 56), (3, 65, 56), (4, 85, 44), (5, 143, 22), (6, 155, 24)):
        NODE(o, x_, y_, n_)

def concept_begum_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_begum_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_begum_sketch():
    """PROBLEM: the design flood runs over today's bank top. MOVE: the street level D is raised above it and the steps
    under it let the river climb: W wet every winter, F only in big floods, D never. K4 stays as it is."""
    o, w = (ORIGIN[0], ORIGIN[1] - 110), 200
    title(o, 82, "K4 BRIDGE · amphibious heritage threshold · form " + FORM)
    cx, cy = 120.0, 11.9                                           # the v2.8 arc through (98,14) (120,34) (142,14)
    r = math.hypot(98 - cx, 14 - cy)
    t0, t1 = math.atan2(14 - cy, 142 - cx), math.atan2(14 - cy, 98 - cx)
    arc = [(cx + r * math.cos(t0 + (t1 - t0) * i / 30.0), cy + r * math.sin(t0 + (t1 - t0) * i / 30.0)) for i in range(31)]
    sketch(o, arc, "K4 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)  # behind
    text(o, "K4 Roman bridge behind\nexisting · kept untouched", 104, 45, 5.4, INK2)
    g = [(0, 8), (0, 62), (40, 62), (40, 50), (62, 50), (62, 40), (84, 40), (84, 30), (90, 30)] + bank((90, 30), (100, 14))[1:] + \
        [(150, 14), (150, 62), (w, 62), (w, 8)]
    gs = sketch_ground(o, notch(g, [(118, 132, 14, 2.5)]))     # summer strip: low-flow channel (v2.8: 118-132, 2.5)
    wall = [(150, 14), (154, 14), (154, 62), (150, 62)]
    marker(o, wall, "wall", STONE, angle=45.0, spacing=0.55, thick=0.5, alpha=0.55, base=0.35)
    text(o, "east: existing channel wall kept\ndefault · Q1 " + CITE("concept"), 156, 65, 5.4)
    # the river climbing the steps: every winter (W), the design flood (F), never D
    fl = under_level(gs, 40, 150, 52)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 125, 33, W_WIN, bed_hatch=True)
    water_level(o, gs, 125, 14, W_EXT, line=False)
    keyed(o, "winter", "every winter: bed under water", 156, 31.8, 5.6, W_EXT, "water")
    keyed(o, "summer", "continuous strip · regulated\ntoday: dry, pools", 156, 15.3, 5.6, W_EXT, "water")
    for x0, x1, y, lab in ((0, 40, 62, "dry top · in use all year"), (40, 84, 50, "flood terraces · out of\nservice only in big floods"),
                           (84, 100, 30, "bed + lowest\nstep · wet\nin winter")):
        for pc in band(gs, x0, x1, 1.5):
            marker(o, pc, "tiers", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
        text(o, lab, x0 + 1, y - 3.0, 5.8, mask=SOIL)
    reeds(o, 102, 148, 14, 4.5)
    road(o, 0, 16, 62, "ROAD " + CITE("survey") + "\nK4 deck: traffic\nschematic", ly=54.5, mask=SOIL)
    sketch_tree(o, 24, 62, 9)                               # only on D: F floods in big floods, W every winter
    sketch_person(o, 31, 62, kind=1); sketch_person(o, 35, 62, kind=2, flip=True); sketch_person(o, 195, 62)  # on dry D / east
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    sketch(o, wall, "wall lines", SKINK, PEN_BOLD, closed=True, z=Z_LINE)
    sketch(o, [(40, 52), (150, 52)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    tick_dim(o, 43, 52, 62, SKINK)                                                # D: raised clear of the flood
    hand_arrow(o, (138, 34.5), (138, 50.5), SITE_WATER_D, width=0.45, head=1.8)  # the river climbs in big floods
    level_mark(o, 146, 52, W_EXT, "flood lines")
    text(o, "Q500 over today's bank top\nK4 cut " + CITE("levels") + "\ndry top raised above it", 156, 51, 5.6, W_EXT, "water")
    text(o, "the river may climb the steps,\nthe street stays above Q500", 6, 31, 8.0, SKINK, "idea")
    text(o, "tiers " + CITE("tiers") + ": level 1 floods yearly · 2 only in 10-year storms\n"
         "level 3 street: dry, only if set above Q500", 2, 5.5, 5.2, INK2)
    for n_, x_, y_ in ((6, 125, 18), (7, 110, 22), (8, 73, 44), (9, 6, 67)):
        NODE(o, x_, y_, n_)

def concept_k5_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_k5_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_k5_sketch():
    """v1.4. Demeter's Garden (Begüm's idea alone, card i01) on the dry top of the south-west bank by K5 (zones DG 1-2,
    tier D). PROBLEM: olives and lavender cannot stand waterlogged soil. MOVE: the garden sits on the dry top, above the
    K5 cut's Q500, and the clean river waters it. Intake, lift and basin volume: not in her page, so not drawn."""
    o, w = ORIGIN, 200
    title(o, 82, "K5 BRIDGE · Demeter's Garden (idea: Begüm) · form " + FORM)
    for c in (108.3, 125.0, 141.7):                                # K5 behind: three arches by its name, schematic
        arc = [(c + 8.0 * math.cos(math.pi * i / 20.0), 20.0 + 8.0 * math.sin(math.pi * i / 20.0)) for i in range(21)]
        sketch(o, arc, "K5 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)
    sketch(o, [(98, 36), (156, 36)], "K5 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)
    text(o, "K5 Üçkemer bridge behind\nexisting · kept · schematic", 100, 50, 5.4, INK2)
    g = [(0, 8), (0, 40), (92, 40)] + bank((92, 40), (104, 14))[1:] + [(150, 14), (160, 40), (w, 40), (w, 8)]
    gs = sketch_ground(o, notch(g, [(56, 68, 40, 3.5), (122, 136, 14, 2.5)]))   # basin by the bridge; summer strip
    fl = under_level(gs, 92, 158, 35)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 129, 22, W_WIN, bed_hatch=True)
    water_level(o, gs, 129, 14, W_EXT, line=False)
    water_level(o, gs, 62, 39.6, W_WIN)                            # the water collection basin (volume: not given)
    for pc in band(gs, 18, 92, 1.5):
        marker(o, pc, "tiers", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    reeds(o, 104, 118, 14, 4.0)
    road(o, 0, 16, 40, "STREET (survey)\nschematic", ly=37.5, mask=SOIL)
    cafe = [(72, 40), (86, 40), (86, 45.5), (72, 45.5)]
    wash(o, cafe, "garden", HOUSE_WALL, 0.45)
    sketch(o, cafe, "garden", INK2, LW_FINE, closed=True)
    sketch(o, [(71, 45.5), (87, 45.5), (85, 47.5), (73, 47.5)], "garden", INK2, LW_FINE, closed=True)
    sketch_tree(o, 26, 40, 9); sketch_tree(o, 38, 40, 8)                 # olives
    sketch_tree(o, 49, 40, 12)                                           # stone pine
    sketch_person(o, 89, 40, kind=1); sketch_person(o, 31, 40, kind=2, flip=True); sketch_person(o, 195, 40)
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)
    sketch(o, [(95, 35), (158, 35)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 154, 35, W_EXT, "flood lines")
    text(o, "Q500 +58.75 m · 2.79 m over the bed " + CITE("levels") + "\ninside the banks · K5 cut\nbridge not modelled:\nhigher just upstream", 160, 54, 5.4, W_EXT, "water")
    keyed(o, "winter", "bed under water", 162, 31, 5.6, W_EXT, "water", mask=SOIL)
    keyed(o, "summer", "continuous strip · regulated\ntoday: dry, pools", 162, 17, 5.6, W_EXT, "water", mask=SOIL)
    text(o, "olives", 22, 53, 5.2, INK2); text(o, "stone pine", 44, 58, 5.2, INK2)
    text(o, "basin", 57, 45, 5.2, INK2); text(o, "cafe", 75, 50, 5.2, INK2)
    text(o, "DEMETER'S GARDEN (idea: Begüm) " + CITE("garden") + "\nSW bank · dry top · all year · DG 1-2", 20, 37, 5.6, mask=SOIL)
    text(o, "olive, lavender: no waterlogged soil " + CITE("plants") + "\ngarden on the dry top", 4, 27, 5.2, ACCENT, mask=SOIL)
    hand_arrow(o, (128, 17), (66, 38.6), SITE_WATER_D, bend=0.15)
    text(o, "clean strip water for the garden\nintake · lift: not designed\nvolume: not in the idea", 56, 31, 5.2, SITE_WATER_D, mask=SOIL)
    # v3: Begüm's crop list as two season rows (sun = summer, cloud = winter); every crop kept
    keyed(o, "summer", "farm-to-table cafe beds: beans · tomatoes · peppers\nfigs · grapes", 4, 79, 5.6)
    keyed(o, "winter", "Aegean herbs · greens · cabbages · citrus · quince " + CITE("garden"), 4, 73.6, 5.6)
    text(o, "clean river waters a\nproductive heritage garden", 100, 68, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((6, 129, 18), (7, 110, 22), (9, 8, 45)):
        NODE(o, x_, y_, n_)

def concept_nil_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_nil_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_nil_sketch():
    """v1.4. Give back (zones WP 1-2 and the floodable boardwalk, ZONES.md). PROBLEM: the downstream edge is unused
    ground and the summer bed is a trickle. MOVE: the clean river from the upstream basins feeds floodable planting
    people can walk along; nothing is treated here; surplus goes to the farmland outside the site."""
    o, w = ORIGIN, 200
    title(o, 82, "DOWNSTREAM REACH · give back · form " + FORM)
    g = [(0, 8), (0, 62), (30, 62), (46, 30), (110, 30)] + bank((110, 30), (120, 14))[1:] + \
        [(165, 14), (175, 32), (w, 32), (w, 8)]
    gs = sketch_ground(o, notch(g, [(136, 150, 14, 2.2)]))     # summer strip: low-flow channel
    fl = under_level(gs, 110, 178, 27)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 143, 21, W_WIN, bed_hatch=True)
    water_level(o, gs, 143, 14, W_EXT, line=False)
    for pc in band(gs, 46, 110, 1.6):
        marker(o, pc, "planting", REED, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    reeds(o, 121, 134, 14, 3.5)
    sketch_tree(o, 78, 30, 6); sketch_tree(o, 92, 30, 5.5); sketch_tree(o, 103, 30, 5)
    deck = [(44.5, 33.2), (72, 33.2), (72, 34.2), (44.5, 34.2)]
    fill(o, deck, "boardwalk", SEC_PAVE)
    for x_ in (50, 58, 66):
        sketch(o, [(x_, 33.2), (x_, 30)], "boardwalk", INK2, LW_EDGE, over=0.0, retrace=False)
    sketch_person(o, 60, 34.2, kind=1); sketch_person(o, 14, 62)
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)
    sketch(o, [(112, 27), (178, 27)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 172, 27, W_EXT, "flood lines")
    text(o, "Q500 +48.00 m · 2.33 m over the bed " + CITE("levels") + "\ninside the banks · NİL cut\nflat end: 1.54 m\nbanks about 114 m apart\nfloods spread wide, shallow", 150, 60, 5.4, W_EXT, "water")
    keyed(o, "winter", "bed under water", 176, 28.5, 5.6, W_EXT, "water", mask=SOIL)
    keyed(o, "summer", "regulated strip\ntoday: trickle\nor dry bed " + CITE("gauges"), 176, 23.5, 5.6, W_EXT, "water", mask=SOIL)
    text(o, "floodable riverside planting · WP 1-2 " + CITE("zones") + "\nflood- + drought-tolerant · clean-river fed\nno farmland inside the site", 48, 27, 5.4, mask=SOIL)
    text(o, "floodable boardwalk: an open deck " + CITE("zones"), 48, 45, 5.4)
    text(o, "slope (schematic)", 2, 59, 5.2, INK2, mask=SOIL)
    keyed(o, "failsafe", "FAIL-SAFE\nfloodable planting · open deck\nhigh water passes over", 1, 50, 5.6, ACCENT, mask=SOIL)
    hand_arrow(o, (141, 16), (100, 31.5), SITE_WATER_D, bend=0.15)
    text(o, "clean river + strip\nfeed the planting", 112, 45, 5.6, SITE_WATER_D)
    hand_arrow(o, (184, 35), (196, 44), ACCENT, width=0.4, head=1.5, bend=-0.2)
    text(o, "surplus clean water · existing farmland outside\nroute not designed", 150, 72, 5.6, ACCENT)
    text(o, "arrives clean from the upstream reeds · no treatment here", 62, 76, 5.6)
    text(o, "clean river back to a\nwalkable planted edge", 4, 76, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((6, 143, 17.5), (7, 84, 34), (10, 158, 18), (11, 190, 38)):
        NODE(o, x_, y_, n_)

'''


# ================================================================ the sheet (v1)
PROPOSALS = [("up", u"1 · UPSTREAM ENTRY · COLLECT, CLEAN AND HOLD",        # v3: subtitles as keyword chips
              [("reed", u"CLEAN · river + held runoff"), ("cascade", u"STORE · winter water"),
               ("strip", u"SUMMER STRIP")]),
             ("k4", u"2 · K4 BRIDGE · AMPHIBIOUS HERITAGE THRESHOLD",
              [("steps", u"TIERS W / F / D"), ("climb", u"river may climb the steps"),
               ("level", u"street level above Q500"), ("bridge", u"Roman bridge stays as it is")]),
             ("k5", u"3 · K5 BRIDGE · DEMETER'S GARDEN (idea: Begüm)",
              [("olive", u"PRODUCTIVE HERITAGE GARDEN"), ("sun", u"dry top · south-west bank"),
               ("drop", u"watered by the clean river")]),
             ("down", u"4 · DOWNSTREAM REACH · GIVE BACK",
              [("reed", u"FLOODABLE PLANTING · clean-river fed"), ("deck", u"floodable boardwalk"),
               ("notreat", u"no treatment here")])]
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
    flow_arrow(pg, x - 1.0, x + 11 * 4.6 + 4.0, yc, dk, 0.35, 1.4)   # under the roundels: one way, with the river
    for n_ in range(1, 12):
        node(pg, x + 1.6, yc, n_, opt, 1.6)
        x += 4.6
    x += 5.5
    for wd in (u"downstream · one way, with the river", u"1-11 as on the water board"):
        pg.text(wd, x, yb, fs, dk, bold=True)
        x += text_w(wd, fs, True) + 8.0
    tag = u"schematic · relative levels · not to scale"
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
