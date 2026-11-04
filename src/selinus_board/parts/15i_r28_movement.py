# ---- MIRAQUA round 28 Oct 2026 (site board v50): p.07 street index maps + notes, p.09 proposal map and index change (worker SB-move). Shared pieces: parts/15h_r28_shared.py,
# common/r28_style.py, common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# P07.2 a note beside each of the three p.07 maps (crops drw_mv_note_1..3: why these streets matter, only what the
# board computes); P07.3 walking / driving today with the index on EVERY street piece in five classes (colour and
# line weight), the classes in the crops' legend; P07.4 street names 7 pt. P09.1 the proposal map redrawn: pale base,
# reach on foot as crisp classes on the streets (R28_REACH), road categories as line types, crossings and hubs as
# symbols, numbered callouts without overlaps (label_place); P09.2 the list in three groups under it; P09.3 the walk
# and car index today and with the proposal (drw_index_change) instead of the commercial spines map.
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
def r28mv_tw(txt, h, bold=False):
    """v50 (MIRAQUA 28 Oct, G5): the width (board units) of txt in Arial at capital height h, so that bold and plain
    runs set side by side on one line meet. v59 (round 4, G-R4-1): the REAL Arial widths (tw -> common/
    font_metrics.py, Turkish letters included); the Helvetica tables _R28MV_HW / _R28MV_HB / _R28MV_SP are gone."""
    return tw(txt, h, "sans", bold)


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
    # v59 (round 4 closing, G-R4-2): no single-word last line (text_place.tp_wrap's rule, min_last_words=2, as the
    # core wrap): the last word of the line above moves down when that line keeps 2 words and the two then fit
    if len(lines) >= 2 and len(lines[-1]) == 1 and len(lines[-2]) >= 3:
        cand = [(False, lines[-2][-1][1]), (True, lines[-1][0][1])]
        if sum(r28mv_tw(t_, h, b_) for sp_, wd in cand for t_, b_ in wd) + sw_ <= width:
            lines[-2], lines[-1] = lines[-2][:-1], cand
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
    own = callable(getattr(B, "tgroup", None)) and getattr(B, "tg", None) is None                 # v59 (round 4, G-R4-1): the runs of a line are one text group
    if own:
        B.tgroup()
    try:
        for t_, b_ in runs:
            B.text(t_, cx, y, h, col, L, order=order, font=FONT_TITLE, bold=b_)
            cx += r28mv_tw(t_, h, b_)
    finally:
        if own:
            B.tgroup(False)
    return cx - x


def r28mv_para(B, s, x, y, width, h, col, L, order=66):
    """s wrapped to width from the baseline y; returns the baseline after its last line. v59 (round 4, G-R4-1): its
    lines are one text group (the page check sb_text_check)"""
    own = callable(getattr(B, "tgroup", None)) and getattr(B, "tg", None) is None
    if own:
        B.tgroup()
    try:
        for ln in r28mv_lines(s, width, h):
            r28mv_draw_line(B, ln, x, y, h, col, L, order)
            y -= R28MV_LEAD * h
    finally:
        if own:
            B.tgroup(False)
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




# ============================================================ v58 (round 3, P07.1-P07.4): the p.07 side columns
# P07.1: each map's legend right beside it, in the column the booklet row leaves (crop drw_mv_note_<n>), then its
# numbered streets (P07.3) and small graphics where the board has the numbers (P07.4: index bars, shop counts,
# services per function, the network length per class), then a compact "Why these streets matter". Every helper
# draws from the top y down at x (board units), w mm wide, k board units per booklet mm, and returns (height mm,
# text boxes in board units); draw=False only measures.
R28MV_PT = 7.0           # pt: the columns' rows and notes
R28MV_HEAD_PT = 8.0      # pt: a column's block headings
R28MV_ROW = 3.3          # mm: one legend / list row at 7 pt
R28MV_MKR = 1.4          # mm: radius of a numbered street marker (on the map and in the list)
R28MV_SW = 4.0           # mm: a legend swatch's length


def r28mv_tbox(s, x, y, h, bold=False, align="L"):
    """the box (board units) of text s set at baseline y, capital height h"""
    w_ = r28mv_tw(s, h, bold)
    x0 = x - (0.5 * w_ if align == "C" else (w_ if align == "R" else 0.0))
    return (x0, y - 0.25 * h, x0 + w_, y + h)


def r28mv_mk(B, x, y, s, colour, k, L, order=68, size_pt=6.5, r_min=None, style="solid"):
    """v59 (round 4, G-R4-7): one marker on the board through THE marker function (common/marker.py mk_marker: the
    glyph centred on its ink box, the circle sized to it, white or ink glyph by contrast) at (x, y) board units, k =
    board units per booklet mm; colour = the colour of what it names. Returns its box (board units)."""
    sh, bx, _r = mk_marker(x / k, y / k, s, crop_hex(colour), size_pt=size_pt, r_min=r_min, style=style)
    _T3Put(B, 0.0, 0.0, k, L).put(sh, order)
    return tuple(v_ * k for v_ in bx)


def r28mv_marker(B, x, y, n, k, L, order=68):
    """a numbered street marker: a dark disc with its white number (6.5 pt) on the street (G3: number on the spot, the
    name in the list beside the map). Returns its box (board units). v59 (round 4, G-R4-7): drawn by mk_marker
    (r28mv_mk), at least R28MV_MKR in radius (was roundel)."""
    return r28mv_mk(B, x, y, u"%d" % n, INK, k, L, order=order, size_pt=6.5, r_min=R28MV_MKR)


def r28mv_head(B, s, x, ytop, k, L, draw=True):
    """a block heading (8 pt bold) under ytop"""
    hh = bk_hk(R28MV_HEAD_PT, k)
    y = ytop - hh
    if draw:
        B.text(s, x, y, hh, INK, L, order=66, font=FONT_TITLE, bold=True)
    return 1.75 * hh / k, [r28mv_tbox(s, x, y, hh, True)]


def _r28mv_fit_h(s, h, avail, k, bold=False):
    """capital height for s: h, made smaller (never under 6 pt) until it fits avail (board units)"""
    w_ = r28mv_tw(s, h, bold)
    return max(bk_hk(6.0, k), h * avail / w_) if w_ > avail > 0 else h


def r28mv_swatch(B, kind, col, x, ym, k, L, wmm=None):
    """a legend swatch R28MV_SW mm long from x, centred on ym: line (wmm), thick, dash, box, dot, study, mark (a
    numbered marker), case (a busiest street: dark casing under its colour)"""
    sw = R28MV_SW * k
    seg = [(x, ym), (x + sw, ym)]
    if kind == "line":
        B.line(seg, col, L, 66, bk_lw(wmm or 0.4, k))
    elif kind == "thick":
        B.line(seg, col, L, 66, bk_lw(1.1, k))
    elif kind == "dash":
        for d in dashes(seg, 1.0 * k, 0.6 * k):
            B.line(d, col, L, 66, bk_lw(0.3, k))
    elif kind == "box":
        B.fill([rect(x, ym - 0.9 * k, x + sw, ym + 0.9 * k)], col, L, 66)
    elif kind == "dot":
        B.fill([circle_pts(x + 0.5 * sw, ym, 0.8 * k, 12)], col, L, 66)
    elif kind == "study":
        for d in r28_pattern(seg, [m_ * 0.5 * k for m_ in R28_STUDY_LINE["dash_mm"]]):
            B.line(d, col, L, 66, bk_lw(R28_STUDY_LINE["width_mm"], k))
    elif kind == "case":
        B.line(seg, INK, L, 66, bk_lw((wmm or 0.7) + 0.45, k))
        B.line(seg, col, L, 67, bk_lw(wmm or 0.7, k))
    elif kind == "mark":
        r28mv_marker(B, x + 0.5 * sw, ym, 1, k, L, order=66)


def r28mv_legend(B, rows, x, ytop, w, k, L, ncol=2, draw=True):
    """legend rows [(kind, colour, label[, line mm])] in ncol columns (the order runs along each row), 7 pt; a label
    too long for its column set smaller (never under 6 pt)"""
    h, rh, cw = bk_hk(R28MV_PT, k), R28MV_ROW * k, w * k / max(1, ncol)
    boxes = []
    for i, row in enumerate(rows):
        kind, col, lab = row[0], row[1], row[2]
        cx = x + (i % ncol) * cw
        yb = ytop - (i // ncol + 1) * rh + 0.3 * rh
        tx = cx + (R28MV_SW + 1.2) * k
        h_ = _r28mv_fit_h(lab, h, cx + cw - 1.0 * k - tx, k)
        if draw:
            r28mv_swatch(B, kind, col, cx, yb + 0.4 * h, k, L, row[3] if len(row) > 3 else None)
            B.text(lab, tx, yb, h_, INK, L, order=66, font=FONT_TITLE)
        boxes.append(r28mv_tbox(lab, tx, yb, h_))
    return ((len(rows) + ncol - 1) // ncol) * R28MV_ROW, boxes


def r28mv_ramp(B, x, ytop, w, k, L, draw=True, txt=None, by_value=True):
    """P07.4: the street index as ONE graphic (was five legend rows): the maps' colour (mv_ramp SEQ at seq_t) and line
    weight (_t3_grad_w; by_value=False: one weight, the top map's width tells the street class) of every value 0-100
    along a bar, the class tops ticked and numbered under it, what it means beside it (txt, **bold** runs)"""
    h = bk_hk(R28MV_PT - 0.5, k)
    bw = 0.45 * w * k
    ym = ytop - 1.6 * k
    boxes = []
    n = 40
    if draw:
        for i in range(n):
            t0, t1 = i / float(n), (i + 1) / float(n)
            v = 100.0 * (0.5 * (t0 + t1)) ** 2            # seq_t is a square root: t = sqrt(v / 100)
            hw = 0.5 * (_t3_grad_w(v) if by_value else 0.6) * k
            B.fill([rect(x + t0 * bw, ym - hw, x + t1 * bw + 0.02 * k, ym + hw)], mv_ramp(SEQ, seq_t(v, 100.0)), L, 66)
    yt = ym - 1.2 * k - h
    for v in R28MV_CLS:
        tx = x + seq_t(v, 100.0) * bw
        s = u"{:.0f}".format(v)
        if draw:
            B.line([(tx, ym - 0.75 * k), (tx, ym - 1.05 * k)], INK2, L, 66, bk_lw(0.15, k))
            B.text(s, tx, yt, h, INK2, L, order=66, font=FONT_TITLE, align="C")
        boxes.append(r28mv_tbox(s, tx, yt, h, align="C"))
    tx0 = x + bw + 2.5 * k
    y = ytop - 0.2 * k - h
    txt = txt or (u"**Street colour and width**: the share of everyday routes using the street (100 = the busiest "
                  u"street piece)")
    for ln in r28mv_lines(txt, (x + w * k) - tx0, h):
        if draw:
            r28mv_draw_line(B, ln, tx0, y, h, INK, L)
        boxes.append((tx0, y - 0.25 * h, tx0 + sum(r28mv_tw(t_, h, b_) for _sp, wd in ln for t_, b_ in wd) +
                      r28mv_tw(u" ", h) * (len(ln) - 1), y + h))
        y -= R28MV_LEAD * h
    return max((ytop - yt) / k + 0.6, (ytop - y) / k - R28MV_LEAD * h / k + 0.8), boxes


def r28mv_bars(B, rows, x, ytop, w, k, L, vmax, draw=True):
    """P07.3 / P07.4: a list with bars: rows dicts n (a street marker number or None), dot (a colour swatch dot or
    None), label, value (None = no bar), vtext, colour; the labels in one column, the bars from one baseline,
    value / vmax of the room left, the value text after its bar; 7 pt"""
    h, rh = bk_hk(R28MV_PT, k), R28MV_ROW * k
    boxes = []
    lead = 0.0
    if any(r_.get("n") is not None or r_.get("dot") is not None for r_ in rows):
        lead = (2.0 * R28MV_MKR + 1.0) * k
    lw_ = min(0.5 * w * k, max([r28mv_tw(r_["label"], h) for r_ in rows] or [0.0]))
    vw = max([r28mv_tw(r_.get("vtext") or u"", h) for r_ in rows if r_.get("value") is not None] or [0.0])
    bx0 = x + lead + lw_ + 1.5 * k
    blen = max(2.0 * k, x + w * k - bx0 - vw - 1.5 * k)
    for i, r_ in enumerate(rows):
        yb = ytop - (i + 1) * rh + 0.3 * rh
        ym = yb + 0.4 * h
        if draw and r_.get("n") is not None:
            r28mv_marker(B, x + R28MV_MKR * k, ym, r_["n"], k, L, order=66)
        elif draw and r_.get("dot") is not None:
            B.fill([circle_pts(x + R28MV_MKR * k, ym, 0.8 * k, 12)], r_["dot"], L, 66)
        h_ = _r28mv_fit_h(r_["label"], h, lw_, k)
        v = r_.get("value")
        hv = h
        if v is None:                                     # no bar: the text runs from the bars' baseline
            xe = bx0
            if r_.get("vtext"):
                hv = _r28mv_fit_h(r_["vtext"], h, x + w * k - bx0 - 0.8 * k, k)
        else:
            xe = bx0 + blen * max(0.0, min(1.0, v / float(vmax or 1.0)))
        if draw:
            B.text(r_["label"], x + lead, yb, h_, INK, L, order=66, font=FONT_TITLE)
            if v is not None:
                B.fill([rect(bx0, ym - 0.8 * k, max(xe, bx0 + 0.3 * k), ym + 0.8 * k)], r_.get("colour") or INK2, L, 66)
            if r_.get("vtext"):
                B.text(r_["vtext"], xe + 0.8 * k, yb, hv, INK, L, order=66, font=FONT_TITLE)
        boxes.append(r28mv_tbox(r_["label"], x + lead, yb, h_))
        if r_.get("vtext"):
            boxes.append(r28mv_tbox(r_["vtext"], xe + 0.8 * k, yb, hv))
    return len(rows) * R28MV_ROW, boxes


def r28mv_stack(B, parts, x, ytop, w, k, L, draw=True):
    """P07.4: one 100 % bar of parts [(share 0-1, colour, label or None)], each label under the middle of its part
    (a label that would touch the one before it is left out); 7 pt"""
    h = bk_hk(R28MV_PT - 0.5, k)
    bw, y1 = w * k, ytop - 0.3 * k
    y0 = y1 - 2.2 * k
    yt = y0 - 1.0 * k - h
    x_, boxes, last = x, [], -1e9
    for sh_, col, lab in parts:
        dx = bw * max(0.0, sh_)
        if draw and dx > 0:
            B.fill([rect(x_, y0, x_ + dx + 0.02 * k, y1)], col, L, 66)
        if lab:
            b_ = r28mv_tbox(lab, x_ + 0.5 * dx, yt, h, align="C")
            if b_[0] < x:
                b_ = (x, b_[1], x + b_[2] - b_[0], b_[3])
            if b_[2] > x + bw:
                b_ = (x + bw - (b_[2] - b_[0]), b_[1], x + bw, b_[3])
            if b_[0] >= last + 0.8 * k:
                if draw:
                    B.text(lab, b_[0], yt, h, INK, L, order=66, font=FONT_TITLE)
                boxes.append(b_)
                last = b_[2]
        x_ += dx
    return (ytop - yt) / k + 0.8, boxes


def r28mv_column(B, crop, k, L, num, rows, items, head=u"Why these streets matter"):
    """v58 (round 3, P07.1, P07.2, P07.4): the column beside a p.07 map (crop: the map's crop, board units): rows of
    blocks [(need, [(fn, share of the width)])] (fn(B, x, ytop, w_mm, draw) -> (h mm, boxes); two blocks side by side
    share the width with 3 mm between them), then head and the note items (**bold** keywords) at 7.5 pt (7 where the
    map's height asks for it). Nothing taller than the map's crop: the last items, then the last optional rows, are
    left out (logged). Crop drw_mv_note_<num>, drawn for its width on the booklet page (bk_w): the map + 4 mm +
    column stay within BK_AW, so the map keeps 1:10,000. Returns the text boxes (board units)."""
    wmax = BK_AW - R28MV_GUT - (crop[2] - crop[0]) / k - 0.5
    nw = min(R28MV_NOTE_W, wmax - 1.0)
    if nw < 30.0:
        LOG.append("Column {} beside the p.07 map not drawn (no width).".format(num))
        return []
    hmax = (crop[3] - crop[1]) / k - 1.0                 # mm: no taller than its map's crop
    x0 = crop[2] + R28MV_GUT * k
    tx = x0 + 0.5 * k
    gap = 1.2

    def row_h(r_):
        ws = _r28mv_widths(r_[1], nw)
        return max(fn(B, tx, 0.0, w_, False)[0] for (fn, _s), w_ in zip(r_[1], ws)) + gap
    rows, items = list(rows), list(items)
    fit = None
    while fit is None:
        hr = sum(row_h(r_) for r_ in rows)
        for pt in (7.5, 7.0):
            h = bk_hk(pt, k)
            lines = [r28mv_lines(it, nw * k, h) for it in items]
            ht = 0.0
            if lines:
                ht = 1.75 * bk_hk(R28MV_HEAD_PT, k) / k + (sum(len(l_) for l_ in lines) * R28MV_LEAD * h +
                                                            (len(lines) - 1) * 0.4 * h) / k
            if hr + ht <= hmax:
                fit = (h, lines)
                break
        if fit is None:
            if items:
                LOG.append(u"Column {} beside the p.07 map: \"{}\" left out (no room).".format(num, items[-1]))
                items = items[:-1]
            elif any(not r_[0] for r_ in rows):
                j = max(i for i, r_ in enumerate(rows) if not r_[0])
                LOG.append(u"Column {} beside the p.07 map: a graphic left out (no room).".format(num))
                rows = rows[:j] + rows[j + 1:]
            else:
                LOG.append(u"WARNING: column {} beside the p.07 map is taller than its map.".format(num))
                fit = (bk_hk(7.0, k), [])
    h, lines = fit
    boxes = []
    y = crop[3] - 0.5 * k
    for r_ in rows:
        ws = _r28mv_widths(r_[1], nw)
        xx, hh_ = tx, 0.0
        for (fn, _s), w_ in zip(r_[1], ws):
            hb, bx = fn(B, xx, y, w_, True)
            boxes += bx
            hh_ = max(hh_, hb)
            xx += (w_ + 3.0) * k
        y -= (hh_ + gap) * k
    if lines:
        hb, bx = r28mv_head(B, head, tx, y, k, L)
        boxes += bx
        y -= hb * k
        y -= h
        for item in lines:
            for ln in item:
                w_ = r28mv_draw_line(B, ln, tx, y, h, INK, L)
                boxes.append((tx, y - 0.25 * h, tx + w_, y + h))
                y -= R28MV_LEAD * h
            y -= 0.4 * h
        y += R28MV_LEAD * h + 0.4 * h - 0.25 * h
    bot = min(y, crop[3] - 1.0 * k)
    crop_panel("mv_note_{}".format(num), x0, bot - 0.5 * k, x0 + (nw + 1.0) * k, crop[3], u"")
    CROP_PANELS[-1]["bk_w"] = nw + 1.0
    return boxes


def _r28mv_widths(blocks, nw):
    """the widths (mm) of one row's blocks: their shares of nw less 3 mm between two"""
    tot = sum(s_ for _f, s_ in blocks) or 1.0
    free = nw - 3.0 * (len(blocks) - 1)
    return [free * s_ / tot for _f, s_ in blocks]
