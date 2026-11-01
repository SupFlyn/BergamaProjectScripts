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
