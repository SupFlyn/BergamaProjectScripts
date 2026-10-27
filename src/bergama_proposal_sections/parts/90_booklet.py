# ================================================================ A3 booklet = crops of this sheet (v5, booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own sections (SHEET_BOXES, set by build_sheet).
# v7 (Aras 27 Oct 11:07: p.18-19 merged into one page): ps_all = the whole 2 x 2 block (titles, notes, the four
# sections) shaped like the booklet's panel area, for ONE booklet page; the four single crops stay (note + sketch,
# tight; the title is the booklet caption).
BK_SOURCES = [("rhs_lavender", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter)",
               u"https://www.rhs.org.uk/Advice/profile?pid=127"),
              ("ecocrop_olive", u"FAO Ecocrop, Olea europaea (will not tolerate waterlogged soils)",
               u"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1553")]
BK_CROPS = [("ps_all", "all", u"Proposal sections, upstream to downstream · relative levels"),
            ("ps_upstream", "up", u"1 · Upstream entry: collect, clean and hold"),
            ("ps_k4", "k4", u"2 · K4 bridge: walking hub"),
            ("ps_k5", "k5", u"3 · K5 bridge: Demeter's Garden and walking hub"),
            ("ps_downstream", "down", u"4 · Downstream reach: give back")]
BK_DROP = [u"^\\[\\d+\\]$"]                           # the sheet's source numbers: the booklet has its own source list


def _bk_hex(c):
    return "%02X%02X%02X" % tuple(int(v) for v in c)


def booklet_export(log):
    """booklet/blocks.json: one crop per section of the sheet + ps_all (rect in mm from the sheet's top-left, y down)."""
    bk = BkBlocks(OUT_DIR, GH_LABEL, VERSION)
    for k, t, u in BK_SOURCES:
        bk.source(k, t, u)
    E = sketch_engine()                               # the sheet's own colours for the legend samples
    wash = E["mix"]((255, 255, 255), E["FLOOD_WASH"], E["FLOOD_ALPHA"])   # the Q500 wash as it shows on white
    legend = [dict(kind="fill", colour=_bk_hex(E["W_WIN"]), label=u"winter water"),
              dict(kind="fill", colour=_bk_hex(E["W_EXT"]), label=u"summer strip"),
              dict(kind="fill", colour=_bk_hex(wash), label=u"reach of the design flood (Q500)"),
              dict(kind="fill", colour=_bk_hex(E["REED"]), label=u"reeds and planting")]
    route = dict(kind="line", colour=_bk_hex(E["ACCENT"]), label=u"walk from the hub square to the sub-hub")
    deck = dict(kind="fill", colour=_bk_hex(E["SEC_PAVE"]), label=u"boardwalk, sub-hub floor")
    extra = {"all": [route, deck], "k4": [route, deck], "k5": [route], "down": [deck]}
    for bid, key, cap in BK_CROPS:
        if key not in SHEET_BOXES:
            log.append(u"booklet %s: section %s not on the sheet" % (bid, key))
            continue
        x0, y0, x1, y1 = SHEET_BOXES[key]
        bk.crop(bid, OUT_NAME.format("A"), (x0, BOARD_H - y1, x1, BOARD_H - y0), caption=cap, scale_den=None,
                legend=legend + extra.get(key, []), drop=BK_DROP)
    return bk.save()
