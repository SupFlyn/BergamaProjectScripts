# ================================================================ v19 booklet items (round 5, G-R5-12: produce, the booklet composes)
# Aras 1 Nov 22:00 / addendum 22:37: the script lays out no page and writes no sheet PDF. W1-W4 go to ONE booklet page
# (D9, page id "p13" = p13-14 merged; N3 a: 1:500), each cut = one true-scale drawing in metres (x = u across the
# stream from the cut axis, NE negative / left, y = level m a.s.l.; PLAN §4), its numbers as badges on what they name,
# its numbered list, its level column (the booklet draws the U04 markers), its zoom inset as its own drawing drawn
# again at the inset scale (G-R5-5), plus one key map (S2 module), one material legend, the page title and intro, the
# sources. Everything lands in Downloads/Bergama/cached/booklet/bergama_proposal_sections/items.json.
PS_PAGE = "p13"                                       # D9: p13 + p14 one page (same id in the 23-page numbering)
BK_SOURCES = [("rhs_lavender", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter)",
               u"https://www.rhs.org.uk/Advice/profile?pid=127"),
              ("ecocrop_olive", u"FAO Ecocrop, Olea europaea (will not tolerate waterlogged soils)",
               u"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1553"),
              ("icomos_2014", u"ICOMOS 2014, Evaluation No 1457, Pergamon and its Multi-Layered Cultural Landscape",
               u"https://whc.unesco.org/document/152724")]


def ps_legend_entries():
    """the material key (solid colours, G-R5-4.1) of what the sections draw, as Ix legend entries"""
    P = _wat_pal()
    return [(dict(kind="fill", colour=P["sec"]), u"water at the average yearly flow"),
            (dict(kind="dash", colour=P["q100"], width_pt=0.85, dash_pt=[3.4, 1.7]), u"Q100 flood level"),
            (dict(kind="dash", colour=P["q500"], width_pt=0.85, dash_pt=[1.1, 1.4]), u"Q500 flood level"),
            (dict(kind="fill", colour=SCT["stone"]), u"stone: DSİ walls, steps, garden wall"),
            (dict(kind="fill", colour=SCT["concrete"]), u"concrete: stairs, ramp, basins"),
            (dict(kind="fill", colour=SCT["earth"]), u"earth"),
            (dict(kind="fill", colour=SCT["gravel"]), u"gravel bed"),
            (dict(kind="fill", colour=PS_TIMBER), u"timber: terrace, boardwalk"),
            (dict(kind="fill", colour=SF_LANE["walk"]), u"walk paving"),
            (dict(kind="fill", colour=SF_LANE["bike"]), u"bike lane")]


def _ps_ibox(it):
    """an item's box (print mm) or None"""
    if it[0] == "image":
        return (it[1], it[2], it[1] + it[3], it[2] + it[4])
    if it[0] == "circle":
        return (it[1] - it[3], it[2] - it[3], it[1] + it[3], it[2] + it[3])
    if it[0] == "text":
        return (it[2], it[3], it[2], it[3])
    pts = [p for R in it[1] for p in R] if it[0] == "poly" else list(it[1])
    if not pts:
        return None
    return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))


def ps_drawing(ix, S, did, page, scale_pref, group, priority, window=None, title=None):
    """S's items (print mm at S.k) as one true-scale drawing in metres: x = S.u0 + x_mm / S.k, y = S.z0 + y_mm / S.k;
    window (m) = an inset's extent: only items that reach into it go in (the booklet clips at the extent)"""
    k = 1.0 / S.k
    if window:
        ext = window
        wx = [(v - o) * S.k for v, o in zip(window, (S.u0, S.z0, S.u0, S.z0))]
        items = []
        for it in S.pg.items:
            b = _ps_ibox(it)
            if b is None or (b[0] <= wx[2] and b[2] >= wx[0] and b[1] <= wx[3] and b[3] >= wx[1]):
                items.append(it)
    else:
        bb = ps_bbox(S.pg.items)
        ext = (S.u0 + min(0.0, bb[0]) * k, S.z0 + min(0.0, bb[1]) * k, S.u0 + max(S.w, bb[2]) * k, S.z0 + bb[3] * k)
        items = S.pg.items
    D = ix.drawing(did, page, ext, scale_pref=scale_pref, dkind="section", group=group, priority=priority,
                   title=title)
    ix.layer(D, "section", items, k=k, origin=(S.u0, S.z0))
    return D


def ps_items(ix, log):
    """v19: the whole p13 export (see the notes above)"""
    page = PS_PAGE
    ix.text(page, u"The proposals in section", "title", priority=1, id="ps_title")
    ix.text(page, u"Four cuts W1-W4, upstream to downstream, each looking downstream · %s left, %s right" % (
        place_name("side_NE"), place_name("side_SW")), "intro", priority=2, id="ps_intro")
    cids = []
    for i, (key, cid, num, name, take) in enumerate(PS_CUTS):
        S = ps_section(cid, log, page, "a")
        cids.append(cid)
        g = u"ps_%s" % cid
        D = ps_drawing(ix, S, g, page, [PS_SCALE], g, i + 1, title=u"%s · %s" % (cid, name))
        ix.text(page, u"%s · %s" % (cid, name), "heading", priority=i + 1, group=g, id=g + "_head")
        ix.text(page, take, "note", priority=i + 1, group=g, id=g + "_scenario")
        ix.text(page, ps_note(cid), "note", priority=i + 1, group=g, id=g + "_levels_note")   # P13.2 water levels
        # the numbers on what they name (badges at the marker, G-R4-5.5) and the list beside "Name · reason"
        disc = []
        for x, y, n, col in S.marks:
            sh, _b, _r = mk_marker(x, y, n, col, PS_LIST_PT)
            disc += [s_ for s_ in sh if s_[0] != "text"]
            for s_ in sh:
                if s_[0] == "text":
                    ix.text(page, s_[1], "badge", drawing=D["id"], at=(S.u0 + s_[2] / S.k, S.z0 + s_[3] / S.k),
                            size_pt=PS_LIST_PT, bold=True, colour=s_[5], positions=["=L"], side_list_ok=False,
                            priority=i + 1, group=g)
        ix.layer(D, "numbers", disc, k=1.0 / S.k, origin=(S.u0, S.z0))
        if S.list:
            ix.list(page, D["id"], [t for _n, t, _c in S.list], numbered=True, id=g + "_list", group=g)
        sf_level_items(ix, page, D, [("q500", level(cid, "q500")), ("q100", level(cid, "q100")),
                                     ("avg", level_avg_flow(cid)), ("bed", S.bed)])
        # the zoom inset: the section drawn again at the inset scale (G-R5-5), framed on the action
        fr = S.inset_fr
        if fr:
            C = ps_section(cid, [], page, "a", k=fr["k"], child=True)
            cd = ps_drawing(ix, C, g + "_inset", page, [fr["den"]], g, i + 1, window=fr["window"],
                            title=u"%s · %s" % (cid, S.inset[4]))
            ix.inset(page, D["id"], fr["window"], cd["id"], fr["factor"], id=g + "_inset_item")
            ix.text(page, S.inset[4], "caption", priority=i + 1, group=g, id=g + "_inset_caption")
            kk = 1.0 / S.k
            sf_inset_cut_check(fr["window"], [(u"plant/element %d" % j_, (S.u0 + o[0] * kk, S.z0 + o[1] * kk,
                                                                          S.u0 + o[2] * kk, S.z0 + o[3] * kk))
                                              for j_, o in enumerate(S.obst) if (o[4] if len(o) > 4 else 0) == 0],
                               page=page, label=u"%s %s" % (cid, S.inset[4]))
        else:
            ix.warn(page, "inset", u"%s: no inset spot set: no zoom inset (never skipped silently, C5)" % cid)
        log.append(u"%s %s: drawing %.0f x %.0f m at 1:%d, %d numbers, inset %s" % (
            page, cid, D["extent"][2] - D["extent"][0], D["extent"][3] - D["extent"][1], PS_SCALE, len(S.list),
            (u"1:%d" % fr["den"]) if fr else u"none"))
    ix.legend(page, None, ps_legend_entries(), title=u"Materials", id="ps_legend", group="ps_legend")
    ps_keymap_items(ix, page, cids, log)
    for k_, t_, u_ in BK_SOURCES:
        ix.source(k_, t_, u_, page=page)
    for k_, t_ in ps_sources():
        ix.source(k_, t_, None, page=page)
    return ix
