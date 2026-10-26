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
