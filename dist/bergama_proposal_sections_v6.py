# -*- coding: utf-8 -*-
"""BERGAMA PROPOSAL SECTIONS v4 (2026-10-25): Group 6's four proposals in section, upstream to downstream, in the
water board's hand-drawn section style (Aras 25 Oct 11:38-11:45: "we want section from each proposal just like our
water board sections"; "the style of waterboard sections were really really good you can do it somewhere else").
For the studio session of 26.10.2026: "Sections: Illustrating the spatial relationships and key design decisions."

NEW IN v6 (Aras's deck review 26 Oct 07:06, p.25 + global rules 3-4): every section opens with a context line (what it
  shows, why it is here, how to read it: NOTES) at the top of its drawing box, inside the booklet crop; the sketch sits
  right under it at the same scale and the crop ends under the sketch (no empty foot). K5: why the amphibious stream
  commons and Demeter's Garden sit together (dry garden / wet commons under the cut, who goes where at low and high
  water, Q500 inside the banks keeps the garden dry). No personal credit in titles (booklet rule).
NEW IN v5 (Aras 25 Oct 21:47-21:51, booklet/CROP_SPEC.md): the booklet shows this sheet's own four sections:
  booklet/blocks.json lists one crop per section (the drawing box each panel frame leaves under its title and chips,
  kept in SHEET_BOXES); the separate booklet redraw (parts/90_booklet.py drawers, c4_s1..c5_s2.pdf) is gone. Sheet
  words: the Selinos is a stream (never river), no caveat notes ("schematic", "not to scale", ": not designed",
  "route not designed", "volume: not in the idea", "bridge not modelled"), no personal name inside the K5 drawing.
  Layout and look unchanged.
OLDER VERSIONS: their notes are in HISTORY.md (repo SupFlyn/BergamaProjectScripts, src/bergama_proposal_sections/).

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
VERSION = "v6"
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
    ("levels", RR + u" v1.1 table: levels calculated on the surveyed stream-height cuts (Manning, main survey TIN)"),
    ("rain", u"water_data/README: MGM 17742 normals 1991-2020, seasonal shares of the year's rain (arithmetic)"),
    ("concept", CR + u" (Q1: east channel wall kept, default)"),
    ("tiers", u"Aras's concept text: tiers, level 1 / 2 / 3"),
    ("garden", u"card i01: Demeter's Garden, page and crop list (zones DG 1-2)"),
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
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'SKETCH_SRC': '96af56d7a396468b0a25e9b919384d03'}.get(name):
        raise RuntimeError("Data file bergama_proposal_sections_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_proposal_sections_data.py:" + name, "exec"), globals())


bergama_data("SKETCH_SRC")

# ---- A3 booklet assets (SCRIPT_STANDARD §8; booklet/ASSET_SPEC.md) ----
# Each booklet frame = one text-free vector PDF drawn at the frame's size + its words as labels in blocks.json.
# The assembler (bergama_booklet) sets every label as live text in the booklet font, never below 7 pt.
BK_MIN_PT = 7.5                              # labels and captions on the booklet (brief: 7-8 pt, minimum 7)
BK_CAPTION_MM = 5.0                          # caption line under every drawing frame


def bk_frame(key, w_default, h_default):
    """(w, h) mm a drawing for asset key "<folder>/<block>" is drawn at: the assembler's booklet_slots.json if it has
    run once, else the defaults given (the plan's frame size). h excludes the caption line."""
    try:
        import json as _j
        with open(os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "bergama_booklet",
                               "booklet_slots.json"), encoding="utf-8") as f:
            s = _j.load(f)[key]
        return float(s["w_mm"]), float(s["h_mm"]) - BK_CAPTION_MM
    except Exception:
        return float(w_default), float(h_default) - BK_CAPTION_MM


def bk_take_text(items, H):
    """Page items (poly/line/circle/text tuples, y up from the bottom, mm) -> (items without text, labels).
    Labels: x, y in mm from the top-left (y to the baseline), size raised to BK_MIN_PT, colour hex."""
    keep, labels = [], []
    for it in items:
        if it[0] != "text":
            keep.append(it)
            continue
        _, s, x, y, size, color, bold, align = it[:8]
        labels.append({"x": round(x, 2), "y": round(H - y, 2), "text": s, "size": max(float(size), BK_MIN_PT),
                       "bold": bool(bold), "anchor": align or "L", "colour": color if isinstance(color, str) else "4A3F35"})
    return keep, labels


class BkBlocks(object):
    """Collects one script's booklet blocks and writes output/<folder>/booklet/blocks.json."""
    def __init__(self, out_dir, script, version):
        self.dir = os.path.join(out_dir, "booklet")
        os.makedirs(self.dir, exist_ok=True)
        self.d = {"script": script, "version": version, "sources": {}, "blocks": {}}

    def path(self, name):
        return os.path.join(self.dir, name)

    def source(self, key, text, url):
        """A public source: used in any text as {src:key}; numbered once for the whole booklet."""
        self.d["sources"][key] = {"text": text, "url": url}

    def drawing(self, bid, pdf_name, labels, caption="", scale_den=None, legend=None):
        self.d["blocks"][bid] = {"type": "drawing", "pdf": pdf_name, "page": 0, "labels": labels, "caption": caption,
                                 "scale_den": scale_den, "legend": legend or []}

    def crop(self, bid, pdf_name, rect_mm, caption="", scale_den=None, legend=None, page=0, drop=None):
        """A booklet drawing taken from this script's own sheet (Aras 25 Oct 21:47: the booklet shows the sheet's
        drawing, re-laid): pdf_name = the sheet PDF in this script's output folder, rect_mm = (x0, y0, x1, y1) of the
        panel in mm from the sheet page's top-left (y down), scale_den = the sheet's scale at 1:1 print (None if not to
        scale). The assembler scales the crop to its frame and resets the sheet's words inside it as live labels;
        drop = regexes of sheet texts not to carry."""
        self.d["blocks"][bid] = {"type": "crop", "pdf": pdf_name, "page": page,
                                 "rect_mm": [round(float(v), 2) for v in rect_mm], "caption": caption,
                                 "scale_den": scale_den, "legend": legend or [], "drop": drop or []}

    def tiles(self, bid, tiles):
        self.d["blocks"][bid] = {"type": "tiles", "tiles": tiles}

    def text(self, bid, heading="", body="", bullets=None):
        self.d["blocks"][bid] = {"type": "text", "heading": heading, "body": body, "bullets": bullets or []}

    def save(self):
        import json as _j
        p = os.path.join(self.dir, "blocks.json")
        with open(p, "w", encoding="utf-8") as f:
            _j.dump(self.d, f, ensure_ascii=False, indent=1)
        return p

# ================================================================ A3 booklet = crops of this sheet (v5, booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own four sections. Each crop is the drawing box its panel frame
# leaves under the title and keyword chips (SHEET_BOXES, set by build_sheet): the sketch and its in-drawing words.
BK_SOURCES = [("rhs_lavender", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter)",
               u"https://www.rhs.org.uk/Advice/profile?pid=127"),
              ("ecocrop_olive", u"FAO Ecocrop, Olea europaea (will not tolerate waterlogged soils)",
               u"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1553")]
BK_CROPS = [("ps_upstream", "up", u"1 · Upstream entry: collect, clean and hold"),
            ("ps_k4", "k4", u"2 · K4 bridge: amphibious heritage threshold"),
            ("ps_k5", "k5", u"3 · K5 bridge: Demeter's Garden"),
            ("ps_downstream", "down", u"4 · Downstream reach: give back")]
BK_DROP = [u"^\\[\\d+\\]$",                           # the sheet's source numbers: the booklet has its own source list
           u" · form [AB]$"]                        # the sketch's own title line (the booklet sets the caption)


def _bk_hex(c):
    return "%02X%02X%02X" % tuple(int(v) for v in c)


def booklet_export(log):
    """booklet/blocks.json: one crop per section of the sheet (rect in mm from the sheet's top-left, y down)."""
    bk = BkBlocks(OUT_DIR, GH_LABEL, VERSION)
    for k, t, u in BK_SOURCES:
        bk.source(k, t, u)
    E = sketch_engine()                               # the sheet's own colours for the legend samples
    wash = E["mix"]((255, 255, 255), E["FLOOD_WASH"], E["FLOOD_ALPHA"])   # the Q500 wash as it shows on white
    legend = [dict(kind="fill", colour=_bk_hex(E["W_WIN"]), label=u"winter water"),
              dict(kind="fill", colour=_bk_hex(E["W_EXT"]), label=u"summer strip"),
              dict(kind="fill", colour=_bk_hex(wash), label=u"reach of the design flood (Q500)"),
              dict(kind="fill", colour=_bk_hex(E["REED"]), label=u"reeds and planting")]
    for bid, key, cap in BK_CROPS:
        if key not in SHEET_BOXES:
            log.append(u"booklet %s: section %s not on the sheet" % (bid, key))
            continue
        x0, y0, x1, y1 = SHEET_BOXES[key]
        extra = [dict(kind="fill", colour=_bk_hex(E["SEC_PAVE"]), label=u"floodable boardwalk")] if key == "down" else []
        bk.crop(bid, OUT_NAME.format("A"), (x0, BOARD_H - y1, x1, BOARD_H - y0), caption=cap, scale_den=None,
                legend=legend + extra, drop=BK_DROP)
    return bk.save()


# ================================================================ the sheet (v1)
PROPOSALS = [("up", u"1 · UPSTREAM ENTRY · COLLECT, CLEAN AND HOLD",        # v3: subtitles as keyword chips
              [("reed", u"CLEAN · stream + held runoff"), ("cascade", u"STORE · winter water"),
               ("strip", u"SUMMER STRIP")]),
             ("k4", u"2 · K4 BRIDGE · AMPHIBIOUS HERITAGE THRESHOLD",
              [("steps", u"TIERS W / F / D"), ("climb", u"stream may climb the steps"),
               ("level", u"street level above Q500"), ("bridge", u"Roman bridge stays as it is")]),
             ("k5", u"3 · K5 BRIDGE · DEMETER'S GARDEN",
              [("olive", u"PRODUCTIVE HERITAGE GARDEN"), ("sun", u"dry top · south-west bank"),
               ("drop", u"watered by the clean stream")]),
             ("down", u"4 · DOWNSTREAM REACH · GIVE BACK",
              [("reed", u"FLOODABLE PLANTING · clean-stream fed"), ("deck", u"floodable boardwalk"),
               ("notreat", u"no treatment here")])]
# v6 (review 26 Oct, rule 4): one context line per section [(text, bold)]: what it shows, why, how to read it.
# K5 keeps to the masterplan v23 detail note (dt_note "dt_k5") without repeating it.
NOTES = {
    "up": [(u"WHY THIS SECTION: the one-way water system starts here.", True),
           (u"Winter runoff from the streets is cleaned once in the reed basins, held in the terrace cascade and "
            u"released in summer as a continuous strip in the bed. Read it left to right, the way the water moves.",
            False)],
    "k4": [(u"WHY THIS SECTION: at K4 the design flood (Q500) runs over today's bank top.", True),
           (u"So the street is raised above it and steps under it let the stream climb: the lowest step is wet every "
            u"winter, the terraces only in big floods, the street never. The Roman bridge stays as it is.", False)],
    "k5": [(u"WHY THE STREAM COMMONS AND DEMETER'S GARDEN SIT TOGETHER AT K5", True),
           (u"Read the cut from the dry bank top down to the wet bed: the garden holds the dry ground and is watered "
            u"from the clean strip; the commons is the bed people use at low water and give to the stream at high "
            u"water. Here even Q500 stays inside the banks, so the garden stays dry while the commons floods.",
            False)],
    "down": [(u"WHY THIS SECTION: downstream the stream gives the clean water back.", True),
             (u"The water arrives clean from the upstream reeds, so nothing is treated here: it feeds floodable "
              u"planting and an open boardwalk, and the surplus goes to existing farmland outside the site.", False)]}
NOTE_TS = 4.6                                         # mm: about 9 pt at the booklet's scale of this panel


def note(pg, box, lines):
    """v6: the section's context line at the top of its drawing box (inside the booklet crop). Returns the box left
    under it for the sketch."""
    x0, y0, x1, y1 = box
    y = y1
    for txt, bold in lines or []:
        y = para(pg, x0, y, (x1 - x0) * 0.66, txt, NOTE_TS, COL["ink_dark"] if bold else COL["ink"], bold) - 0.8
    return (x0, y0, x1, y - 6.0) if lines else box


SHEET_BOXES = {}                                      # v5: key -> drawing box (x0, y0, x1, y1), mm, y up; set by build_sheet
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
        _, pb = place(pg, draw_concept(key, opt), note(pg, b, NOTES.get(key)), 3.0, "TL", log, "section " + key)
        SHEET_BOXES[key] = (b[0], max(b[1], pb[1] - 4.0), b[2], b[3])   # v6: booklet crop = context line + sketch
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
