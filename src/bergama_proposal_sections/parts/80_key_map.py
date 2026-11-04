# ================================================================ v19 key map: this page's four cuts (G-R5-3, D3, S2 module v2)
# v19 (round 5): the one merged page p13 (D9) gets ONE key map from common/keymap.py km_map v2: no scale_den, so the
# module fits its frame to the map, turns it so the corridor runs along the long side and puts its own true-north
# arrow; only W1-W4 (red R01, triangles pointing downstream: every W section looks downstream); names through the
# names table. The script draws nothing of it: km_items() hands the drawing, its labels and the keymap item to
# items.json and the booklet places it in the right column (never over a drawing, no scale bar). The v17 page-drawn
# map (own clip, own north arrow, neatline, TextPage) is gone.
PS_KM_PAD = 120.0                     # m round the page's cut ends in the map window (drawing rule: streets around)
PS_KM_SPACE = (113.6, 90.0)           # print mm: the MOST room offered (right column 113.6 mm, PLAN §3); the module
#                                       returns the fitted, smaller frame


def ps_keymap_items(ix, page, cids, log):
    """the page's key map as items (S2 km_items) added to ix; returns the drawing id or None (WARNING)"""
    ends = [p for c in cids for p in level_ends(c)]
    bx = (min(p[0] for p in ends) - PS_KM_PAD, min(p[1] for p in ends) - PS_KM_PAD,
          max(p[0] for p in ends) + PS_KM_PAD, max(p[1] for p in ends) + PS_KM_PAD)
    try:
        km = km_map(list(cids), PS_KM_SPACE[0], PS_KM_SPACE[1], page=page, looks=dict((c, -1) for c in cids),
                    box=bx, log=log)
        its = km_items(km, page, item_id=u"ps_keymap_%s" % page, priority=3)
    except Exception as ex:
        ix.warn(page, "keymap", u"key map not made (%s: %s)" % (type(ex).__name__, ex))
        return None
    for it in its:                                   # the module's schema dicts go in as they are (ids registered)
        it["id"] = ix._id(it["id"], it.get("kind", "item"))
        if it.get("anchor") and it["anchor"].get("drawing"):
            it["anchor"]["drawing"] = its[0]["id"]
        if it.get("kind") == "keymap":
            it["drawing"] = its[0]["id"]
        ix._put(page, it)
    for m_ in km.get("missing") or []:
        log.append(u"FLAG %s key map: %s not drawn" % (page, m_))
    log.append(u"%s key map: %s, frame %.0f x %.0f mm (fitted), turned %s deg" % (
        page, u" + ".join(cids), km.get("w_mm", 0.0), km.get("h_mm", 0.0), km.get("rotation_deg")))
    return its[0]["id"]
