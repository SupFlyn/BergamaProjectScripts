# ---- 60_layout (composer core, round 5 S1; G-R5-2, D2, PLAN §3 "Page"): one page = one grid ---------------------------
# A3 landscape 420 x 297 mm, margins 14 / 12 (grid.py); content area GRID_AREA (14, 30, 406, 273); title strip on top
# (12 .. 25: title left, intro right of it); drawings take the left share (default 70 % of the 392 mm inner width,
# ~274 mm, PLAN §3 / refs/U29 Aras's p23 redesign), a 4 mm gutter, the right column (~114 mm) in sub-columns for legend,
# lists, key map and short text; caption bottom-left under the drawings; page number only, bottom right (G-R4-10).
# Every block shares edges with the grid lines named here, so blocks align across a page (U21).
#   P = bk_page(doc, pid, n=None)            a new page: P.page (PyMuPDF), P.tp (TextPage over the whole sheet with the
#                                            14/12 mm margins, the edge test of 70_check), P.placed, P.ink, P.boxes
#   lay_page(P, share=0.70, sub=2, title_h=13.0, caption_h=0.0) -> dict
#         grid boxes (x0, y0, x1, y1) mm: title, intro, draw, right, subs [right sub-columns], caption, all
#   lay_split(box, n, gap=4.0, vertical=True, weights=None) -> [box]   a box cut into n parts (rows or columns)
#   lay_stack(box, heights, gap=4.0, page=None) -> [box]              blocks stacked from the box top; past its foot
#                                                                     = WARNING "overrun" (never a stop)
#   bk_title(P, L, title, intro=None)        the page title (16 pt bold) and its intro (6 pt, justified) in the strip
#   bk_caption(P, text, box)                 a caption (5 pt, justified, last line left) in its box
#   bk_pageno(P, n)                          the page number, bottom right (7 pt bold accent), role "footer"
#   bk_finish(P) -> n texts                  draws every text (40_set bk_emit) after the drawings
BK_SHARE = 0.70
BK_GUT = 4.0
BK_PAGENO_Y = 283.5                 # baseline of the page number: inside the 12 mm bottom margin line (285)


class BkPage(object):
    def __init__(self, doc, pid, n=None):
        self.pid, self.n = pid, n
        self.page = doc.new_page(width=GRID_PAGE[0] * BK_K, height=GRID_PAGE[1] * BK_K)
        self.tp = TextPage(pid, (0.0, 0.0, GRID_PAGE[0], GRID_PAGE[1]), y_down=True,
                           margins=(GRID_ML, GRID_MT, GRID_MR, GRID_MB), footer_zone=None)
        self.placed, self.ink, self.boxes, self.layout = [], [], {}, None
        self._fonts = False


def bk_page(doc, pid, n=None):
    return BkPage(doc, pid, n)


def lay_page(P, share=BK_SHARE, sub=2, title_h=13.0, caption_h=0.0):
    x0, x1 = GRID_ML, GRID_PAGE[0] - GRID_MR
    W = x1 - x0
    a = GRID_AREA
    dw = round(share * W - BK_GUT / 2.0, 1)
    draw = (x0, a[1], x0 + dw, a[3] - caption_h)
    right = (x0 + dw + BK_GUT, a[1], x1, a[3])
    subs = lay_split(right, max(1, int(sub)), BK_GUT, vertical=False)
    title = (x0, GRID_MT, x0 + dw, GRID_MT + title_h)
    intro = (right[0], GRID_MT, x1, GRID_MT + title_h + 4.0)
    cap = (x0, a[3] - caption_h + 1.0, x0 + dw, a[3]) if caption_h > 0 else None
    L = dict(title=title, intro=intro, draw=draw, right=right, subs=subs, caption=cap, all=(x0, a[1], x1, a[3]),
             share=share)
    P.layout = L
    return L


def lay_split(box, n, gap=BK_GUT, vertical=True, weights=None):
    x0, y0, x1, y1 = box
    n = max(1, int(n))
    wts = list(weights) if weights else [1.0] * n
    tot = float(sum(wts))
    span = ((y1 - y0) if vertical else (x1 - x0)) - gap * (n - 1)
    out, p = [], (y0 if vertical else x0)
    for wv in wts:
        d = span * wv / tot
        out.append((x0, p, x1, p + d) if vertical else (p, y0, p + d, y1))
        p += d + gap
    return out


def lay_stack(box, heights, gap=BK_GUT, page=None):
    out, y = [], box[1]
    for h in heights:
        out.append((box[0], y, box[2], y + h))
        y += h + gap
    if out and out[-1][3] > box[3] + 1e-6:
        wn_warn(page, "overrun", u"blocks stacked %.1f mm past their area's foot (y %.1f)" % (out[-1][3] - box[3],
                                                                                            box[3]))
    return out


def bk_title(P, L, title, intro=None):
    t = L["title"]
    pt = grid_role("title")[0]
    a_, _d = fm_asc_desc(pt, True)
    w = fm_width(title, pt, True)
    if w > t[2] - t[0]:                       # a long title steps down (never below the floor)
        pt = max(GRID_MIN_PT, pt * (t[2] - t[0]) / w)
        a_, _d = fm_asc_desc(pt, True)
    P.tp.put(title, t[0], t[1] + a_, pt, True, "L", 0.0, "title", "title", GRID_INK["ink"])
    if intro:
        i = L["intro"]
        st_para(P, intro, i[0], i[1], i[2] - i[0], i[3] - i[1], "intro", page=P.pid)


def bk_caption(P, text, box):
    return st_para(P, text, box[0], box[1], box[2] - box[0], box[3] - box[1], "caption", page=P.pid)


def bk_pageno(P, n):
    pt, b, _l, col = grid_role("pageno")
    P.tp.put(u"%d" % int(n), GRID_PAGE[0] - GRID_MR, BK_PAGENO_Y, pt, b, "R", 0.0, "pageno", "footer", col,
             ("footer",))


def bk_finish(P):
    return bk_emit(P)
