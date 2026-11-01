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
# v17 (round 4, D2): booklet p13 becomes two pages at 1:250, ps_p1 = p13a (W1, W2) and ps_p2 = p13b (W3, W4), each
# a whole page drawn at the booklet scale (BK_S 1: the booklet prints the crop 1:1, so its scale words stay 1:250 and
# the insets 1:100); ps_all is gone. The single crops are the four rows (unused by the booklet today).
BK_CROPS = [("ps_p1", "p1", u"Proposal sections W1, W2, upstream, each looking downstream"),
            ("ps_p2", "p2", u"Proposal sections W3, W4, downstream, each looking downstream"),
            ("ps_upstream", "up", u"W1 · Upstream entry, looking downstream"),
            ("ps_k4", "k4", u"W2 · %s, looking downstream" % PS_CUTS[1][3]),          # v16 (G16): real names
            ("ps_k5", "k5", u"W3 · %s, looking downstream" % PS_CUTS[2][3]),
            ("ps_downstream", "down", u"W4 · Downstream reach, looking downstream")]
BK_DROP = [u"^\\[\\d+\\]$"]                           # the sheet's source numbers: the booklet has its own source list


def booklet_export(log):
    """booklet/blocks.json: the two pages ps_p1 / ps_p2 + one crop per row (rect in mm from the sheet's top-left, y
    down)."""
    bk = BkBlocks(OUT_DIR, GH_LABEL, VERSION)
    for k, t, u in BK_SOURCES:
        bk.source(k, t, u)
    bk.d["sheet_sources"] = {"0": [u"[{}] {}".format(i + 1, v) for i, (_, v) in enumerate(ps_sources())]}   # v7: the booklet's sources page
    # v10: drawn samples of what the sections draw (fills as they show on white; hatches by their ground colour), for
    # the single crops; v17: the pages ps_p1 / ps_p2 carry their own legend, so the booklet adds none under them
    P = _wat_pal()
    legend = [dict(kind="fill", colour=P["sec"], label=u"water at the average yearly flow"),
              dict(kind="dash", colour=P["q100"], label=u"Q100 flood level"),
              dict(kind="dash", colour=P["q500"], label=u"Q500 flood level"),
              dict(kind="fill", colour=SCT["stone"], label=u"stone: DSİ walls, steps, garden wall"),
              dict(kind="fill", colour=SCT["concrete"], label=u"concrete: stairs, ramp, basins"),
              dict(kind="fill", colour=SCT["earth"], label=u"earth"),
              dict(kind="fill", colour=SCT["gravel"], label=u"gravel bed"),
              dict(kind="fill", colour=PS_TIMBER, label=u"timber: terrace, boardwalk"),
              dict(kind="fill", colour=SF_LANE["walk"], label=u"walk paving"),
              dict(kind="fill", colour=SF_LANE["bike"], label=u"bike lane"),
              dict(kind="fill", colour=COL["accent"], label=u"proposal (labels), cut lines on the key map")]
    for style, part in STYLES:                        # v13 (Aras 31 Oct): style a only, plain ids
        boxes = SHEET_BOXES.get(style, {})
        for bid, key, cap in BK_CROPS:
            if key not in boxes:
                log.append(u"booklet %s: section %s not on the sheet" % (bid, key))
                continue
            x0, y0, x1, y1 = boxes[key]
            bk.crop(bid, OUT_NAME.format(part), (x0, BOARD_H - y1, x1, BOARD_H - y0), caption=cap,
                    scale_den=PS_SCALE * BK_S, legend=([] if key in ("p1", "p2") else legend), drop=BK_DROP)
    return bk.save()
