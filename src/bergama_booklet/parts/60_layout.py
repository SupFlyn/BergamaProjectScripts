# ---- 60_layout (composer core, round 5 S1; round 6 S9 v31: G6-1 page frames): one page = one grid ------------------
# A3 landscape 420 x 297 mm, margins 14 / 12 (grid.py; = SON page2 margins x 3.3-96.7 %, PLAN P-6: one set for every
# page). Round 6 (v31): every block of a page sits in a FRAME of the page plan (80_plan, PLAN §3 "Target frames"),
# given in % of the page ([x, y, w, h], 0,0 top left; 1 % x = 4.2 mm, 1 % y = 2.97 mm). Title band (PLAN §3, frames
# files "common SON frame"): section label y 3-4 %, title y 5-8 %, the intro right of the title, a thin rule at 8.8 %;
# content from y 10 %; the page number alone, bottom right (PLAN §2.1: no "NN/23", no theme footer).
#   P = bk_page(doc, pid, n=None)            a new page: P.page (PyMuPDF), P.tp (TextPage over the whole sheet with the
#                                            14/12 mm margins, the edge test of 70_check), P.placed, P.ink, P.boxes
#   bk_kicker(spec) / bk_footer(spec)       v33 (L4): "<letter> <CHAPTER> · <PART>" / "<letter> <CHAPTER>" labels
#   lay_split(box, n, gap=4.0, vertical=True, weights=None) -> [box]   a box cut into n parts (rows or columns)
#   bk_band(P, label, title, intro=None) -> y_mm   v31 title band: section label, title (16 pt bold), intro (6 pt,
#                                            justified) right of the title, rule; returns the rule's y
#   bk_caption(P, text, box)                 a caption (5 pt, justified, last line left) in its box
#   bk_pageno(P, n, label=None)              the footer: label + page number, bottom right (7 pt bold accent); log
#                                            line "pagenum <n>"
#   bk_finish(P) -> n texts                  draws every text (40_set bk_emit) after the drawings
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


BK_PCT = (GRID_PAGE[0] / 100.0, GRID_PAGE[1] / 100.0)      # mm per % (x 4.2, y 2.97)
BK_BAND = dict(label_y=8.5, title_y=15.5, rule_y=25.0, intro_gap=8.0)   # v33: MM, SON page2 measured (PLAN §4.1:
#                                     kicker [13.5,8.5], title + lead [13.5,15.5], rule y 25 across 14 -> 406)
BK_PAGENO_LOG = []                  # "pagenum <n>" lines (code.py adds them to the log)


def bk_kicker(spec):
    """v33 (L4): "<letter> <CHAPTER> · <PART>" in caps (SON page2), from the one page list"""
    part = spec.get("part")
    if not part:
        return None
    st = STAGES.get(spec.get("stage"), u"")
    return (u"%s  %s%s" % (part, PARTS.get(part, u""), (u"  ·  " + st) if st else u"")).upper()


def bk_footer(spec):
    """v33 (L4): the footer label "<letter>  <CHAPTER>" (the number follows it)"""
    part = spec.get("part")
    return (u"%s  %s" % (part, PARTS.get(part, u""))).upper() if part else None


def bk_band(P, label, title, intro=None):
    """v31 title band (see the part notes): label line, title, intro beside it, rule; returns the rule's y (mm)"""
    x0, x1 = GRID_ML, GRID_PAGE[0] - GRID_MR
    acc, ink = GRID_INK["accent"], GRID_INK["ink"]
    if label:
        pt = 6.0
        a_, _d = fm_asc_desc(pt, True)
        P.tp.put(label, x0, BK_BAND["label_y"] + a_, pt, True, "L", 0.0, "label", "title", acc)
    pt = grid_role("title")[0]
    tw_max = 0.55 * (x1 - x0)                       # v33: the title keeps its size (L2); over 55 % = WARNING
    w = fm_width(title, pt, True)
    if w > tw_max:
        wn_warn(P.pid, "title", u"title %.0f mm wide at %.1f pt (over 55 %% of the band): the lead gets %.0f mm"
                % (w, pt, x1 - x0 - w - BK_BAND["intro_gap"]))
    a_, _d = fm_asc_desc(pt, True)
    ty = BK_BAND["title_y"]
    P.tp.put(title, x0, ty + a_, pt, True, "L", 0.0, "title", "title", ink)
    ry = BK_BAND["rule_y"]
    if intro:
        ix = x0 + w + BK_BAND["intro_gap"]
        st_para(P, intro, ix, ty, max(30.0, x1 - ix), ry - ty - 0.8, "intro", page=P.pid)
    bk_line(P, [(x0, ry), (x1, ry)], GRID_INK["rule"], 0.4)
    return ry


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


def bk_caption(P, text, box):
    return st_para(P, text, box[0], box[1], box[2] - box[0], box[3] - box[1], "caption", page=P.pid)


def bk_pageno(P, n, label=None):
    """v33 (L4): footer bottom right "<letter>  <CHAPTER>  <n>" (SON page2: label ends ~3 mm left of the number)"""
    pt, b, _l, col = grid_role("pageno")
    xr = GRID_PAGE[0] - GRID_MR
    P.tp.put(u"%d" % int(n), xr, BK_PAGENO_Y, pt, b, "R", 0.0, "pageno", "footer", col, ("footer",))
    if label:
        lpt = 6.0
        P.tp.put(label, xr - fm_width(u"%d" % int(n), pt, b) - 3.0, BK_PAGENO_Y, lpt, True, "R", 0.0, "footer_label",
                 "footer", GRID_INK["ink2"], ("footer",))
    BK_PAGENO_LOG.append(u"pagenum %d" % int(n))


def bk_finish(P):
    return bk_emit(P)
