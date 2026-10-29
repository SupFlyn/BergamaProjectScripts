# ---- MIRAQUA round 28 Oct 2026 (site board v50): p.07 street index maps + notes, p.09 proposal map and index change (worker SB-move). Shared pieces: parts/15h_r28_shared.py,
# common/r28_style.py, common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# P07.2 a note beside each of the three p.07 maps (crops drw_mv_note_1..3: why these streets matter, only what the
# board computes); P07.3 walking / driving today with the index on EVERY street piece in five classes (colour and
# line weight), the classes in the crops' legend; P07.4 street names 7 pt. P09.1 the proposal map redrawn: pale base,
# reach on foot as crisp classes on the streets (R28_REACH), road categories as line types, crossings and hubs as
# symbols, numbered callouts without overlaps (label_place); P09.2 the list in three groups under it; P09.3 the walk
# and car index today and with the proposal (drw_index_change) instead of the commercial spines map.
import unicodedata

R28MV_CLS = (2.0, 10.0, 25.0, 50.0, 100.0)    # P07.3: index classes 0-2, 2-10, 10-25, 25-50, 50-100 (the top map's steps)
R28MV_CLS_W = (0.2, 0.32, 0.48, 0.68, 0.95)   # mm on the booklet page: the line weight of each class
R28MV_CLS_COL = [mv_ramp(SEQ, seq_t(v_, 100.0)) for v_ in R28MV_CLS]   # a class = the top map's ramp at its upper step
R28MV_LABEL_PT = 7.0     # P07.4: street names on the walking / driving maps (were 8 pt)
R28MV_NOTE_OF = {"walk_b": 2, "car_b": 3}      # P07.2: the maps' notes, crops drw_mv_note_2 / _3 (_1: the top map)
R28MV_NOTE_W = 100.0     # mm: a note's text width at most; map + gutter + note stay within the booklet width BK_AW
R28MV_GUT = 4.0          # mm between two panels of a booklet row (bergama_booklet GUT)
R28MV_LEAD = 1.75        # baseline to baseline / capital height, notes and lists
R28MV_NEAR_M = 100.0     # m: "comes within ... of the stream" (notes)
R28MV_EDGE_M = 40.0      # m: the streets along the stream (as city_link_movement.json "edge")
R28MV_CAP = 0.718        # capital height / font size of the writer (_PDF_CAP)
# P09.1 road categories: (name, colour, line mm, dash (on, off) mm or None, calming ticks); the colours are the
# masterplan's (ROAD_CHANGE_COL, its p.23 plan), the line types tell them apart (secondary encoding)
R28MV_ROAD = {"kept": (u"kept", C("847E75"), 0.7, None, False),
              "calmed": (u"calmed", C("B5832F"), 0.9, None, True),
              "pedestrian": (u"pedestrian", C("8B3A3F"), 1.25, None, False),
              "shared": (u"shared", C("7F5B7B"), 0.9, (1.6, 0.7), False),
              "relocated": (u"relocated", C("C2603A"), 0.9, (0.6, 0.6), False)}
R28MV_BUS = (u"bus line, later step", C("633131"), 0.45, (1.2, 0.8))    # dashed, 1.05 mm beside its streets
R28MV_REACH_W = (0.5, 0.4, 0.3)     # mm: the three reach classes (R28_REACH) on the streets, the nearest heaviest
R28MV_MK = dict((k_, C(hx_)) for k_, lab_, hx_ in R28_MARKERS)   # callout numbers by group, as p.23's markers
R28MV_BRIDGE = C(R28_OPEN["bridge"])                              # bridge kept
R28MV_DISC = 1.6         # mm: radius of a numbered callout on the map (7 pt number)
R28MV_SYM = 2.0          # mm: half-length of a crossing symbol across the stream
R28MV_HUB_R = 2.1        # mm: hub ring radius
R28MV_GROUPS = (("roads", u"Roads"), ("crossings", u"Bridges and crossings"), ("hubs", u"Hubs"))
R28MV_CHANGE_ORDER = ("pedestrian", "calmed", "shared", "relocated", "kept", "truck", "bus")   # index chart rows

# ------------------------------------------------------------ text: Arial widths, **bold** runs (G5)
# Arial has Helvetica's widths (common/pdf_fonts.py): per 1000 em, codes 32-126, plain and bold
_R28MV_HW = [int(v_) for v_ in (
    "278 278 355 556 556 889 667 191 333 333 389 584 278 333 278 278 556 556 556 556 556 556 556 556 556 556 "
    "278 278 584 584 584 556 1015 667 667 722 722 667 611 778 722 278 500 667 556 833 722 778 667 778 722 667 611 "
    "722 667 944 667 667 611 278 278 278 469 556 333 556 556 500 556 556 278 556 556 222 222 500 222 833 556 556 "
    "556 556 333 500 278 556 500 722 500 500 500 334 260 334 584").split()]
_R28MV_HB = [int(v_) for v_ in (
    "278 333 474 556 556 889 722 238 333 333 389 584 278 333 278 278 556 556 556 556 556 556 556 556 556 556 "
    "333 333 584 584 584 611 975 722 722 722 722 667 611 778 722 278 556 722 611 833 722 778 667 778 722 667 611 "
    "722 667 944 667 667 611 333 278 333 584 556 333 556 611 556 611 556 333 611 611 278 278 556 278 889 611 611 "
    "611 611 389 556 333 611 556 778 556 556 500 389 280 389 584").split()]
_R28MV_SP = {u"ı": 278, u"·": 278, u"–": 556, u"—": 1000, u"²": 333, u"³": 333, u"°": 400, u"’": 278}


def r28mv_tw(txt, h, bold=False):
    """v50 (MIRAQUA 28 Oct, G5): the width (board units) of txt in Arial at capital height h, so that bold and plain
    runs set side by side on one line meet (tw's 0.92 h per letter is a safe upper bound, too wide for that)"""
    tab = _R28MV_HB if bold else _R28MV_HW
    w_ = 0
    for ch in txt:
        o = ord(ch)
        if 32 <= o < 127:
            w_ += tab[o - 32]
        elif ch in _R28MV_SP:
            w_ += _R28MV_SP[ch]
        else:
            b_ = unicodedata.normalize("NFD", ch)[:1]
            w_ += tab[ord(b_) - 32] if b_ and 32 <= ord(b_) < 127 else 556
    return w_ / 1000.0 * h / R28MV_CAP


def r28mv_parse(s):
    """'**bold** plain' -> [(text, bold)]"""
    return [(t_, j % 2 == 1) for j, t_ in enumerate(s.split(u"**")) if t_]


def r28mv_lines(s, width, h):
    """s (with **bold** runs) broken at its spaces into lines no wider than width (board units) at capital height h.
    A line = [(space before, word)], a word = [(text, bold)] (it may change weight inside, e.g. **K4**,)."""
    toks, cur, sp = [], [], False
    for t_, b_ in r28mv_parse(s):
        for j, piece in enumerate(t_.split(u" ")):
            if j > 0:
                if cur:
                    toks.append((sp, cur))
                cur, sp = [], True
            if piece:
                cur.append((piece, b_))
    if cur:
        toks.append((sp, cur))
    sw_ = r28mv_tw(u" ", h)
    lines, line, lw_ = [], [], 0.0
    for sp, word in toks:
        ww = sum(r28mv_tw(t_, h, b_) for t_, b_ in word)
        if line and lw_ + sw_ + ww > width:
            lines.append(line)
            line, lw_ = [], 0.0
        lw_ += (sw_ if line else 0.0) + ww
        line.append((bool(line), word))
    if line:
        lines.append(line)
    return lines


def r28mv_draw_line(B, line, x, y, h, col, L, order=66):
    """one line of r28mv_lines at baseline y, each run of one weight as one whole text (live in Illustrator).
    Returns its width."""
    runs = []
    for sp, word in line:
        for j, (t_, b_) in enumerate(word):
            t2 = (u" " if sp and j == 0 else u"") + t_
            if runs and runs[-1][1] == b_:
                runs[-1][0] += t2
            else:
                runs.append([t2, b_])
    cx = x
    for t_, b_ in runs:
        B.text(t_, cx, y, h, col, L, order=order, font=FONT_TITLE, bold=b_)
        cx += r28mv_tw(t_, h, b_)
    return cx - x


def r28mv_para(B, s, x, y, width, h, col, L, order=66):
    """s wrapped to width from the baseline y; returns the baseline after its last line"""
    for ln in r28mv_lines(s, width, h):
        r28mv_draw_line(B, ln, x, y, h, col, L, order)
        y -= R28MV_LEAD * h
    return y


R28MV_SRC_COM = ("Commerce: shopfronts within 30 m of a street (survey, OSM, Overture). Services: Overture/Meta "
                 "places. Walks: the shortest along OSM streets and footways from the edge of each working area, "
                 "rounded to 10 m.")      # = draw_how_people_use_it's r_com (the same [n])


# ------------------------------------------------------------ a pale base (G6)
def r28mv_pale(c, t):
    return mix(c, WHITE, t)


class R28Pale(object):
    """v50 (MIRAQUA 28 Oct, P09.1, G6): a drawing target that lays b_base's colours t of the way to white (the water
    t_w) and thins its lines (wf): the pale, recessive base under the proposal. The study area's outline passes as it
    is (G8: one line style everywhere)."""

    def __init__(self, B, t=0.5, t_w=0.3, wf=0.7):
        self.B, self.t, self.t_w, self.wf = B, t, t_w, wf
        self.keep = tuple(C(R28_STUDY_LINE["colour"]))
        self.water = (tuple(MPL["water"]), tuple(MPL["water_edge"]))

    def __getattr__(self, k_):
        return getattr(self.B, k_)

    def _c(self, c):
        c3 = tuple(c[:3])
        if c3 == self.keep:
            return c
        return r28mv_pale(c3, self.t_w if c3 in self.water else self.t)

    def fill(self, polys, color, layer, order):
        self.B.fill(polys, self._c(color), layer, order)

    def hatch(self, polys, color, layer, order, spacing, ang=math.radians(45.0), w=0.03):
        self.B.hatch(polys, self._c(color), layer, order, spacing, ang, w)

    def line(self, P, color, layer, order, w=0.13):
        keep = tuple(color[:3]) == self.keep
        self.B.line(P, self._c(color), layer, order, w if keep else w * self.wf)


