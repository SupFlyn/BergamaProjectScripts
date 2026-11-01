# ---- 70_check (composer core, round 5 S1; G-R5-1, D1, D2, C7, C11, C12): the layout check on FINAL page coordinates ---
# Runs after a page is composed (every drawing, label, legend, list, marker, scale bar and text placed). Measures:
#   fill        area of the union of everything placed (drawing windows, photos, markers, scale bars, legend / list
#               blocks, every text box) inside the margins (14 / 12 mm) / that area; 1 mm cells
#   empty_band  the tallest run of 1 mm rows inside the margins with nothing placed on them, in mm
#   overlaps    TextPage.check: text/text, text/drawing (a drawing's window is a keep only its own labels may enter),
#               text/legend swatch, text/marker, block/block (drawings, legends, lists, key maps, photos)
#   edge        text or block past the margins (blocks too: check(blocks_in=True)); labels never cross their window
#               (50_place does not take such spots)
#   min_text    the smallest printed size on the page (D1: >= 4.0 pt after scaling; C12)
# Every overlap / edge hit is one WARNING line (TextPage.check); fill below the reference and a band over the limit are
# WARNING lines in ck_finish; a text under 4 pt is its own WARNING when it is set. Nothing stops the run.
# The measure counts boxes (a drawing's window is filled), the same measure for p15 and every page (D2).
#   ck_page(P) -> dict(pid, fill, band_mm, overlaps, edge, min_text, n_text)   (kept in CK_RES)
#   ck_finish(ref="p15", log=None) -> [line]
#         after all pages: the reference fill = p15's measured fill (D2: the round 5 p15 composed by this booklet);
#         per page "layout <page> fill=<x> ref_p15=<y> empty_band=<mm> overlaps <n> edge <n> min_text=<pt>", a WARNING
#         "fill" when fill < ref, a WARNING "empty_band" when the band > CK_BAND_MAX of the inner height (D2: 3 %),
#         then "text justified n" (40_set). Lines go to log (default the warning list, so they reach the log).
CK_RES = []
CK_CELL = 1.0
CK_BAND_MAX = 0.03


def _ck_inner():
    return (GRID_ML, GRID_MT, GRID_PAGE[0] - GRID_MR, GRID_PAGE[1] - GRID_MB)


def _ck_mark(G, cols, rows, inn, b):
    import math as _m
    x0, y0 = max(b[0], inn[0]), max(b[1], inn[1])
    x1, y1 = min(b[2], inn[2]), min(b[3], inn[3])
    if x1 <= x0 or y1 <= y0:
        return
    c0, c1 = int(_m.floor((x0 - inn[0]) / CK_CELL)), min(cols, int(_m.ceil((x1 - inn[0]) / CK_CELL)))
    r0, r1 = int(_m.floor((y0 - inn[1]) / CK_CELL)), min(rows, int(_m.ceil((y1 - inn[1]) / CK_CELL)))
    if c1 <= c0:
        return
    run = b"\x01" * (c1 - c0)
    for r in range(r0, r1):
        G[r * cols + c0:r * cols + c1] = run


def ck_page(P):
    tp = P.tp
    tp.check(raise_=False, blocks_in=True)
    ov = sum(1 for h in tp.hits if h[0] == "overlap")
    ed = sum(1 for h in tp.hits if h[0] == "edge")
    inn = _ck_inner()
    cols = int((inn[2] - inn[0]) / CK_CELL)
    rows = int((inn[3] - inn[1]) / CK_CELL)
    G = bytearray(cols * rows)
    for it in tp.items:
        _ck_mark(G, cols, rows, inn, it["box"])
    for B in tp.blocks:
        _ck_mark(G, cols, rows, inn, B["box"])
    for _k, b, _n in P.ink:
        _ck_mark(G, cols, rows, inn, b)
    fill = sum(G) / float(cols * rows) if cols and rows else 0.0
    band = best = 0
    for r in range(rows):
        if any(G[r * cols:(r + 1) * cols]):
            band = 0
        else:
            band += 1
            best = max(best, band)
    pts = [it["pt"] * tp.scale for it in tp.items if it.get("emit", True)]
    res = dict(pid=P.pid, fill=fill, band_mm=best * CK_CELL, overlaps=ov, edge=ed,
               min_text=min(pts) if pts else None, n_text=len(pts))
    CK_RES.append(res)
    return res


def ck_finish(ref="p15", log=None):
    lg = WN_LOG if log is None else log
    R = [r for r in CK_RES if r["pid"] == ref]
    rf = R[-1]["fill"] if R else None
    if rf is None:
        wn_warn(None, "fill", u"the reference page %s was not composed: no fill threshold this run (D2)" % ref, lg)
    lim = CK_BAND_MAX * (GRID_PAGE[1] - GRID_MT - GRID_MB)
    out = []
    for r in CK_RES:
        if rf is not None and r["pid"] != ref and r["fill"] < rf - 1e-4:
            wn_warn(r["pid"], "fill", u"fill %.2f below %s's %.2f: enlarge the drawings (D2)" % (r["fill"], ref, rf), lg)
        if r["band_mm"] > lim + 1e-6:
            wn_warn(r["pid"], "empty_band", u"an empty band %.0f mm tall (limit %.1f mm = 3 %% of the height, D2)" % (
                r["band_mm"], lim), lg)
        # min_text: every text under the floor was already one WARNING "min_text" when it was set (TextPage._size_ok)
        ln = u"layout %s fill=%.2f ref_p15=%s empty_band=%.0f overlaps %d edge %d min_text=%s" % (
            r["pid"], r["fill"], (u"%.2f" % rf) if rf is not None else u"none", r["band_mm"], r["overlaps"],
            r["edge"], (u"%.2f" % r["min_text"]) if r["min_text"] is not None else u"-")
        lg.append(ln)
        out.append(ln)
    ln = u"text justified %d (of %d paragraphs set; %d lines stretched)" % (ST_COUNT["justified"], ST_COUNT["paras"],
                                                                          ST_COUNT["lines"])
    lg.append(ln)
    out.append(ln)
    return out


def ck_reset():
    del CK_RES[:]
    for k in ST_COUNT:
        ST_COUNT[k] = 0
