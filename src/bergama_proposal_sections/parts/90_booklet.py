# ================================================================ A3 booklet = crops of this sheet (v5, booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own sections (SHEET_BOXES, set by build_sheet).
# v7 (Aras 27 Oct 11:07: p.18-19 merged into one page): ps_all = the whole 2 x 2 block (titles, notes, the four
# sections) shaped like the booklet's panel area, for ONE booklet page; the four single crops stay (note + sketch,
# tight; the title is the booklet caption).
BK_SOURCES = [("rhs_lavender", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter)",
               u"https://www.rhs.org.uk/Advice/profile?pid=127"),
              ("ecocrop_olive", u"FAO Ecocrop, Olea europaea (will not tolerate waterlogged soils)",
               u"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1553"),
              # v9 (MIRAQUA 28 Oct, F5): the public page behind SRC_KEY plane (v10: the hamam is no longer drawn)
              ("icomos_2014", u"ICOMOS 2014, Evaluation No 1457, Pergamon and its Multi-Layered Cultural Landscape",
               u"https://whc.unesco.org/document/152724")]
# v10: ps_all = page 13 (key map strip + the four sections at 1:500, scale_den set so the booklet prints "1:500");
# the single crops are the four panels (unused by the booklet today, kept for other pages)
BK_CROPS = [("ps_all", "all", u"Proposal sections W1-W4, upstream to downstream, each looking downstream"),
            ("ps_upstream", "up", u"W1 · Upstream entry, looking downstream"),
            ("ps_k4", "k4", u"W2 · K4 walking hub, looking downstream"),
            ("ps_k5", "k5", u"W3 · K5 Demeter's Garden, looking downstream"),
            ("ps_downstream", "down", u"W4 · Downstream reach, looking downstream")]
BK_DROP = [u"^\\[\\d+\\]$"]                           # the sheet's source numbers: the booklet has its own source list


def _ps_mix(a, b, t):
    """hex a seen at opacity t over hex b"""
    A, B = hex_rgb(a), hex_rgb(b)
    return "%02X%02X%02X" % tuple(int(round(255.0 * (B[i] + (A[i] - B[i]) * t))) for i in range(3))


def booklet_export(log):
    """booklet/blocks.json: one crop per section of the sheet + ps_all (rect in mm from the sheet's top-left, y down)."""
    bk = BkBlocks(OUT_DIR, GH_LABEL, VERSION)
    for k, t, u in BK_SOURCES:
        bk.source(k, t, u)
    bk.d["sheet_sources"] = {"0": [u"[{}] {}".format(i + 1, v) for i, (_, v) in enumerate(ps_sources())]}   # v7: the booklet's sources page
    # v10: drawn samples of what the sections draw (fills as they show on white; hatches by their ground colour)
    legend = [dict(kind="fill", colour=_ps_mix(PS_FLOOD, "FFFFFF", PS_FLOOD_A), label=u"reach of the 500-year flood (Q500)"),
              dict(kind="dash", colour=COL["river_mid"], label=u"Q500 (dashed) and Q100 (dotted) water levels"),
              dict(kind="fill", colour=SEC["channel"], label=u"summer strip, basin water"),
              dict(kind="fill", colour=SCT["stone"], label=u"stone: DSİ walls, steps, garden wall"),
              dict(kind="fill", colour=SCT["concrete"], label=u"concrete: basins, floors"),
              dict(kind="fill", colour=SCT["earth"], label=u"earth"),
              dict(kind="fill", colour=SCT["gravel"], label=u"gravel bed"),
              dict(kind="fill", colour=PS_TIMBER, label=u"timber boardwalk"),
              dict(kind="fill", colour=COL["accent"], label=u"proposal (labels), cut lines on the key map")]
    for bid, key, cap in BK_CROPS:
        if key not in SHEET_BOXES:
            log.append(u"booklet %s: section %s not on the sheet" % (bid, key))
            continue
        x0, y0, x1, y1 = SHEET_BOXES[key]
        bk.crop(bid, OUT_NAME.format("A"), (x0, BOARD_H - y1, x1, BOARD_H - y0), caption=cap,
                scale_den=PS_SCALE * BK_S, legend=legend, drop=BK_DROP)
    return bk.save()
