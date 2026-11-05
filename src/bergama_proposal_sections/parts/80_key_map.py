# ================================================================ v20 key map: p12's four cuts W1-W4 (G6-5, P-1)
# Round 6: the one key-map module (common/keymap.py v3, S1) draws it, the p08 "Where each street is cut" look: strong
# base, bold red cuts across with end marks, subtle street names, the study area as one closed dash-dot line. P-1:
# kept small in the side column (the r06_S02 target has none; G6-5 says every page with cuts). Only W1-W4, each looking
# downstream (looks -1). The booklet places it; the script draws nothing of it.
PS_KM_PAD = 120.0                     # m round the page's cut ends in the map window (streets around)
PS_KM_SPACE = (60.0, 45.0)            # print mm: the most room offered (small, side column, P-1); fitted smaller


def ps_keymap_items(ix, page, cids, log):
    """the page's key map as items added to ix; returns the drawing id or None (WARNING, never a stop)"""
    ends = [p for c in cids for p in level_ends(c)]
    bx = (min(p[0] for p in ends) - PS_KM_PAD, min(p[1] for p in ends) - PS_KM_PAD,
          max(p[0] for p in ends) + PS_KM_PAD, max(p[1] for p in ends) + PS_KM_PAD)
    try:
        km = km_keymap(page, cut_ids=list(cids), w_mm=PS_KM_SPACE[0], h_mm=PS_KM_SPACE[1], box=bx, log=log,
                       looks=dict((c, -1) for c in cids))
        its = km_export_items(km, page, item_id=u"ps_keymap_%s" % page, priority=6)
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
    return its[0]["id"]
