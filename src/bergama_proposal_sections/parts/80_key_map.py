# ================================================================ v22 key map: p12's four cuts W1-W4 (G7-3, round 7 S5)
# Round 7: THE key map module (common/keymap.py v4 km_keymap = SON page8 "Where each street is cut", S1) at the page's
# SON key-map frame PS_KM_MM = SON page13's key-map size (PLAN §3 row 12: 109.2 x 22.0 mm at [296.8, 27.0], top right).
# Map window = the module's own (study rings + cuts fill the frame); no box, no fitting. North on the LEFT (outside the
# frame, in the free room above the panel grid: at the right it would pass the 406 mm margin). No heading (SON13 none).
# Only W1-W4, each looking downstream (looks -1). The booklet places it at 1:1; the script draws nothing of it.
PS_KM_MM = (109.2, 22.0)              # SON page13 key-map frame, mm (PLAN §3 row 12, H4 §5 page 12)


def ps_keymap_items(ix, page, cids, log):
    """the page's key map as items added to ix; returns the drawing id or None (WARNING, never a stop)"""
    try:
        km = km_keymap(page, cuts=list(cids), w_mm=PS_KM_MM[0], h_mm=PS_KM_MM[1], heading=None, log=log,
                       looks=dict((c, -1) for c in cids), north_side="left")
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
