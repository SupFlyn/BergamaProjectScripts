# ================================================================ v21 booklet items (v21: labels as items, no declutter): p12 "The proposals in section" (round 6, S6)
# BRIEF row 12, Q9, P-12, P-1: ONE page = refs/targets/r06_S02 (the 28 Oct 4-in-1 page). Language: SKETCH (BRIEF §3:
# not to scale, thick black ground line, flat beige soil, flat blue water bands, numbered circles on the element they
# name, short captions, few small figures, simple tree blobs). Restored from commit f93d84b (proposal sections v8.1:
# draw_concept, declutter, sections, the 2 x 2 sheet) and data/SKETCH_SRC.py, now exported as booklet items:
#   ps_panel_1 ... ps_panel_4   one scale-free drawing each (units "mm", all four the SAME extent PS_PANEL_MM and the
#                               same factor, so the booklet prints them at one size), its title (heading) + purpose (note)
#   ps_legend_strip             one shared legend, hue table categories (G6-6)
#   ps_keymap_p12               W1-W4 key map, km_keymap at SON13's frame 109.2 x 22.0 (v22, G7-3), top right
#   ps_title, ps_caption        page title; caption "... 1-11 as in Collect, clean, hold" (P7)
# Numbers 1-11 = the 28 Oct element numbers (f93d84b water board CHAIN), which CCH_STEPS must equal (S1).
PS_PAGE = "p12"                                       # round 6 page id (PLAN §2.1)
PS_PANEL_MM = (194.8, 92.0)                           # v22 (round 7, layout r06_S02, PLAN §3 row 12): each panel's
#   drawing at its print size, mm. Width = r06_S02 panel width 194.8 (2 columns 13.7-208.5 / 211.2-406.0, gap 2.7).
#   Height: grid y 51 (under the key map, PLAN §3) to 262 (caption + legend strip under it, r06_S02 y 264.5-274.2)
#   = 211 mm, less one row gap 2.3 = 2 rows of 104.3; less the title row (~6.5) and purpose row (~5.5) = 92.0
PS_LBL_PT = 7.0                                       # smallest word at that size (the 28 Oct page's 7 pt; G6-7 floor 4)
PS_FIT = (1.0, 1.0)                                   # v22 (BRIEF §3 L1): printed at exactly PS_PANEL_MM, never fitted
BK_SOURCES = [("rhs_lavender", u"RHS, Lavender growing guide (no soil that becomes waterlogged over winter)",
               u"https://www.rhs.org.uk/Advice/profile?pid=127"),
              ("ecocrop_olive", u"FAO Ecocrop, Olea europaea (will not tolerate waterlogged soils)",
               u"https://ecocrop.apps.fao.org/ecocrop/srv/en/cropView?id=1553"),
              ("icomos_2014", u"ICOMOS 2014, Evaluation No 1457, Pergamon and its Multi-Layered Cultural Landscape",
               u"https://whc.unesco.org/document/152724")]
# the sketches' CITE keys -> Sources keys; None = an internal source (course survey, concept record, cards, zone base):
# no mark (booklet rule: public sources only). The [n] the 28 Oct page printed become {src:key} (BRIEF §0 DATA).
PS_CITE = {"levels": "levels", "plane": "icomos_2014", "plants": "rhs_lavender", "rain": "ps_rain",
           "gauges": "ps_gauges", "survey": None, "concept": None, "hubs": None, "hamam": None, "garden": None,
           "zones": None}
PS_SRC_EXTRA = [("ps_rain", u"MGM 17742 Bergama, monthly rain, climate normals 1991-2020 (WMO)"),
                ("ps_gauges", u"DSİ stream gauges D04A053 and D04A063, yearbooks 2016-2021")]


def _tr_up(s):
    """Turkish-aware capitals for titles (i -> İ, ı -> I)"""
    return s.replace(u"i", u"İ").replace(u"ı", u"I").upper()


def ps_panels():
    """the four panels: (key, sketch level cut, title, purpose). Titles as BRIEF row 12, bridges by their names"""
    k4, k5 = bridge_name("K4", short=True), bridge_name("K5", short=True)
    return [("up", "W1", u"1 · UPSTREAM ENTRY",
             u"Winter runoff: cleaned in reed basins, held in the terrace basins, given back in summer as the strip"),
            ("k4", "W2", u"2 · K4 BRIDGE (%s) · WALKING HUB" % _tr_up(k4),
             u"Q500 tops today's bank: dry hub square above it, floodable sub-hub in the bed, steps between"),
            ("k5", "W3", u"3 · K5 BRIDGE (%s) · DEMETER'S GARDEN + WALKING HUB" % _tr_up(k5),
             u"Bank tops stay dry: garden and hub square · bed: stream commons = sub-hub, floods in winter"),
            ("down", "W4", u"4 · DOWNSTREAM REACH",
             u"Clean water arrives from upstream: floodable planting + boardwalk, surplus to farmland")]


SKETCH_FN = {"up": "concept_aras_sketch", "k4": "concept_begum_sketch", "k5": "concept_k5_sketch",
             "down": "concept_nil_sketch"}


def _ps_hx(code, rank):
    """a hue table colour (common/hues.py, G6-6) as the engine's (r, g, b)"""
    h = hue(code, rank).lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def ps_engine_colours(E):
    """v20 (G6-6, P-3, P-5): every colour the legend keys comes from the hue table; red leaves the page"""
    E["W_EXT"] = _ps_hx("WAT", 1)                     # summer strip, Q500 line and words
    E["W_WIN"] = _ps_hx("WAT", 2)                     # winter water
    E["W_SUM"] = _ps_hx("WAT", 3)
    E["SITE_WATER_D"] = _ps_hx("WAT", 2)              # flow arrows, rain strokes
    E["SITE_FLOOD"] = _ps_hx("WAT", 4)                # the winter pictogram's cloud
    E["FLOOD_WASH"], E["FLOOD_ALPHA"] = _ps_hx("WAT", 4), None     # reach of the design flood: the WAT tint, solid
    E["REED"] = _ps_hx("GRN", 3)                      # reeds and planting bands
    E["REED_HEAD"] = _ps_hx("GRN", 2)
    E["SITE_TREE"] = (_ps_hx("GRN", 4), _ps_hx("GRN", 3), _ps_hx("GRN", 2))   # tree blobs: light, mid, shadow
    E["SITE_TRUNK"] = _ps_hx("CTX", 2)
    E["DRY_WW"] = _ps_hx("WW", 3)                     # dry-top terraces over the basins (P-15 name)
    E["SPILL"] = _ps_hx("WW", 2)                      # a full basin spills to the next
    E["FAILSAFE_C"] = _ps_hx("WW", 1)
    E["DRY_PUB"] = _ps_hx("PUB", 3)                   # hub square + steps
    E["SUBHUB_C"] = _ps_hx("PUB", 2)                  # the sub-hub floor in the bed
    E["DRY_AGR"] = _ps_hx("AGR", 3)                   # Demeter's Garden
    E["FARM_C"] = _ps_hx("AGR", 1)                    # garden plants, surplus to farmland
    E["CAFE_C"] = _ps_hx("AGR", 4)
    E["ROUTE"] = _ps_hx("MOV", 2)                     # walk hub square -> sub-hub
    E["BOARD_C"] = _ps_hx("MOV", 3)                   # boardwalk
    E["ROAD"] = _ps_hx("CTX", 1)
    E["WALL_C"] = _ps_hx("CTX", 3)                    # channel wall kept
    E["STONE_HATCH"] = _ps_hx("CTX", 2)               # bridges behind (dashed)
    E["HOUSE_WALL"], E["HOUSE_ROOF"] = _ps_hx("CTX", 4), _ps_hx("CTX", 3)
    E["HER_C"] = _ps_hx("HER", her_rank(u"Tabaklar Hamamı"))   # Q5: no sourced status -> rank 3
    E["HERITAGE"] = E["HER_C"]
    E["ACCENT"] = _ps_hx("MOV", 2)


def ps_legend_entries():
    """G6-6: the strip's entries, category hue + rank, sorted by category (legend_group); each keys a drawn colour"""
    ent = [("WAT", 2, dict(kind="fill", colour=hue("WAT", 2)), u"winter water"),
           ("WAT", 1, dict(kind="fill", colour=hue("WAT", 1)), u"summer strip"),
           ("WAT", 4, dict(kind="fill", colour=hue("WAT", 4), stroke=hue("WAT", 2)),      # P-4: tint outlined
            u"reach of the design flood (Q500)"),
           ("WW", 3, dict(kind="fill", colour=hue("WW", 3)), u"dry-top terraces over the basins"),
           ("GRN", 3, dict(kind="fill", colour=hue("GRN", 3)), u"reeds and planting"),
           ("AGR", 3, dict(kind="fill", colour=hue("AGR", 3)), u"Demeter's Garden"),
           ("MOV", 2, dict(kind="dash", colour=hue("MOV", 2), width_pt=1.1, dash_pt=[3.0, 1.5]),
            u"walk from the hub square to the sub-hub"),
           ("MOV", 3, dict(kind="fill", colour=hue("MOV", 3)), u"boardwalk"),
           ("PUB", 2, dict(kind="fill", colour=hue("PUB", 2)), u"sub-hub floor"),
           ("PUB", 3, dict(kind="fill", colour=hue("PUB", 3)), u"hub square and steps")]
    return [(e[2], e[3]) for e in legend_group(ent)]


def ps_q_text(log):
    """the Q500 words of each panel, read live from the level table (BRIEF §0 DATA: never the 28 Oct numbers).
    up / k5 / down: "Q500 +<level> m · <depth over the bed> m" + whether it stays inside the banks (both bank tops);
    k4: the sketch's words (the K4 panel is drawn at the bridge; W2 lies downstream of it), checked against W2."""
    out = {}
    for key, cid in (("up", "W1"), ("k5", "W3"), ("down", "W4"), ("k4", "W2")):
        q, d = level(cid, "q500"), level_flood_depth(cid, "q500")
        tops = [t for t in (level(cid, "top", "NE"), level(cid, "top", "SW")) if t is not None]
        inside = bool(tops) and q is not None and q <= min(tops)
        mk = u" {src:levels}"
        if key == "k4":
            out[key] = u"Q500 over today's bank" + mk + u"\nhub square above it"
            if inside:
                log.append(u"FLAG %s k4 panel: the level table puts W2's Q500 (+%.2f) under both bank tops %s; the "
                           u"sketch says it tops today's bank (drawn at the K4 bridge, upstream of W2)" % (
                               PS_PAGE, q, tops))
            continue
        if q is None or d is None:
            out[key] = u"Q500" + mk
            log.append(u"FLAG %s %s: no Q500 / bed in the level table: level words left out" % (PS_PAGE, cid))
            continue
        out[key] = u"Q500 +%.2f m · %.2f m over the bed%s\n%s" % (
            q, d, mk, u"inside the banks" if inside else u"over the lower bank top")
        log.append(u"%s %s Q500 words from LEVELS %s: q500 %.2f, bed depth %.2f, bank tops %s -> %s" % (
            PS_PAGE, key, cid, q, d, tops, u"inside" if inside else u"over"))
    return out


def ps_cite(key):
    k = PS_CITE.get(key)
    return u"{src:%s}" % k if k else u""


def draw_concept(which, log):
    """v8.1 draw_concept (f93d84b), form A. Returns (Page, kinds, groups): kinds[i] = (sub, element) of item i,
    groups[i] = its label group (v21: no declutter, every item kept)"""
    E = sketch_engine()
    E["FORM"] = "A"
    del E["ZP"][:]
    E["KINDS"].clear()
    E["ORDER"][0] = 0
    E["GROUP"][0] = 0
    E["NEXT_G"][0] = 0
    E["NEXT_E"][0] = 0
    E["ELEM"][0] = None
    k = E["TXT_K"][0]

    def NODE(o, x, y, n):
        tmp = Page(0, 0)
        node(tmp, o[0] + x, o[1] + y, n, "A", 2.6 * k)
        E["NEXT_G"][0] += 1
        E["GROUP"][0] = -E["NEXT_G"][0]                # an element number never moves; labels keep off it
        pe = E["elem_open"]("annotations", u"number %d" % n)
        for it in tmp.items:
            E["SUB"][0] = "numbers"
            E["_put"](it, E["Z_TEXT"])
        E["elem_close"](pe)
        E["GROUP"][0] = 0
    E["NODE"] = NODE
    E["CITE"] = ps_cite
    E[SKETCH_FN[which]]()
    srt = sorted(E["ZP"], key=lambda e: (e[0], e[1]))
    kinds = [E["KINDS"].get(o_, ("other", None)) for _, o_, _, _ in srt]
    pg = Page(0, 0)
    pg.items = [it for _, _, it, _ in srt]
    # v21 (LAYOUT PLAN §3.1, Aras 4 Nov 19:18): nothing is moved or left out here; every word goes to the booklet
    # at its drawn point (label group kept: g > 0 = one label's lines, < 0 = an element number, never moved)
    return pg, kinds, [g for _, _, _, g in srt]


def ps_sections(log):
    """v8.1 sections(): the four sketches at ONE common factor s (the largest at which each fits PS_PANEL_MM); their
    words raised (TXT_K, up to 4 tries) until the smallest prints >= PS_LBL_PT at the design size.
    Returns ({key: (Page, kinds)}, s)."""
    E = sketch_engine()
    E["TXT_K"][0] = 1.0
    W, H = PS_PANEL_MM
    for _ in range(4):
        parts = dict((k, draw_concept(k, log)) for k in SKETCH_FN)
        s = min(min(W / max(b[2] - b[0], 1e-6), H / max(b[3] - b[1], 1e-6))
                for b in (items_bbox(p[0].items) for p in parts.values()))
        small = min(it[4] for p in parts.values() for it in p[0].items
                    if it[0] == "text" and it[5] != COL["white"])        # white = digits inside the numbers
        pt = small * s / PT
        if pt >= PS_LBL_PT - 0.05:
            break
        E["TXT_K"][0] *= PS_LBL_PT / pt * 1.02
    log.append(u"%s sections: one factor %.3f mm per sketch unit; words x%.2f; smallest word %.1f pt at the design "
               u"size %.0f x %.0f mm" % (PS_PAGE, s, E["TXT_K"][0], pt, W, H))
    return parts, s


PS_SUB_KIND = {"ground": "ground", "ground lines": "ground", "tiers": "ground", "terraces": "ground", "wall": "other",
               "wall lines": "other", "water": "water", "water lines": "water", "rain": "water", "flood": "water",
               "flood lines": "levels", "planting": "plants", "people": "people", "context": "buildings",
               "garden": "buildings", "road": "roads", "hub route": "paths", "boardwalk": "paths", "sub-hub": "hubs",
               "arrows": "annotations", "sun": "annotations", "season": "annotations", "fail-safe": "annotations",
               "dimensions": "annotations", "zones": "annotations", "numbers": "annotations", "labels": "labels",
               "text": "labels", "idea": "labels", "K4 bridge (existing)": "other", "K5 bridge (existing)": "other"}


def _ps_layers(ix, D, items, kinds):
    """G6-9: consecutive items of one element = one layer tagged grp "<kind>/<element>" (S2 Ix.layer grp=); draw order
    kept. Returns {kind: elements} for the log."""
    runs, cnt = [], {}
    for it, (sub, el) in zip(items, kinds):
        if el:                                        # a named element (tree, person, text, number, house)
            key = (el[0], el[1])
            if runs and runs[-1][0] == key and runs[-1][2]:
                runs[-1][1].append(it)
                continue
        else:                                         # unnamed: consecutive items of one kind = one element
            kind = PS_SUB_KIND.get(sub, "other")
            if runs and not runs[-1][2] and runs[-1][0][0] == kind:
                runs[-1][1].append(it)
                continue
            key = (kind, u"%s %d" % (sub, len(runs) + 1))
        runs.append([key, [it], bool(el)])
    for (kind, eid), its, _ in runs:
        cnt.setdefault(kind, set()).add(eid)
        nm = u"%s/%s" % (kind, eid)
        try:
            ix.layer(D, nm, its, grp=nm)
        except TypeError:                             # item_export without S2's grp (before the round 6 merge)
            ix.layer(D, nm, its)
    return dict((k, len(v)) for k, v in cnt.items())


def ps_label_items(ix, D, did, lbl):
    """v21 (LAYOUT PLAN §3.1-2): every line of a sketch label = one label item of panel D at its drawn point (units
    mm), drawn alignment first, then the ring. Lines of one label share the id stem "<did>_lbl_<g>_" (n = line,
    from 1, top down) so the booklet can keep them together. An element number's digit (group < 0) = role "badge"
    (booklet bk_badges: stays on its disc, never moved), id "<did>_num_<digit>". Returns (labels, lines)."""
    n_line, seen = {}, []
    for t, g in lbl:
        _, txt, x, y, size, colour, bold, al = t[:8]
        if not (u"%s" % txt).strip():
            continue
        if g < 0:
            nid = u"%s_num_%s" % (did, txt)
            k_ = 2
            while nid in ix.ids:                      # the same number twice in one panel: _2, _3 (no export warning)
                nid = u"%s_num_%s_%d" % (did, txt, k_)
                k_ += 1
            ix.text(D["page"], txt, "badge", drawing=D["id"], at=(x, y), size_pt=size / PT, bold=bool(bold),
                    colour=colour if isinstance(colour, str) else None, positions=["=" + str(al or "C")],
                    side_list_ok=False, group=did, id=nid)
            continue
        n_line[g] = n_line.get(g, 0) + 1
        if g not in seen:
            seen.append(g)
        ix.text(D["page"], txt, "label", drawing=D["id"], at=(x, y), size_pt=size / PT, bold=bool(bold),
                colour=colour if isinstance(colour, str) else None,
                positions=["=" + str(al or "L")] + ["E", "NE", "N", "NW", "W", "SW", "S", "SE"],
                group=did, id=u"%s_lbl_%d_%d" % (did, g, n_line[g]))
    return len(seen), sum(n_line.values())


def ps_items(ix, log):
    """v20: the whole p12 export (see the notes above)"""
    page = PS_PAGE
    E = sketch_engine()
    ps_engine_colours(E)
    E["BRIDGE"] = lambda c: bridge_name(c)
    E["Q_TEXT"].clear()
    E["Q_TEXT"].update(ps_q_text(log))
    ix.text(page, u"The proposals in section", "title", priority=1, id="ps_title")
    parts, s = ps_sections(log)
    W, H = PS_PANEL_MM
    trees = {}
    for i, (key, cid, ttl, purpose) in enumerate(ps_panels()):
        pg, kinds, grps = parts[key]
        b = items_bbox(pg.items)
        dx = W / 2.0 - s * (b[0] + b[2]) / 2.0        # centred across, at the top of the box (as the 28 Oct sheet)
        dy = H - s * b[3]
        did = u"ps_panel_%d" % (i + 1)
        its, kd, lbl = [], [], []
        for it, kn, g in zip(pg.items, kinds, grps):  # item by item: kinds and groups stay aligned
            t_ = xform([it], s, dx, dy)
            if not t_:
                continue
            if t_[0][0] == "text" and g:              # a label's line / a number's digit -> an item (below)
                lbl.append((t_[0], g))
            else:
                its.append(t_[0])
                kd.append(kn)
        kinds = kd
        # SKETCH language (BRIEF §3): a scale-free diagram, no scale bar; same extent for all four = one print size
        num, _, head = ttl.partition(u" · ")          # v21 (L1 box per drawing): number -> disc, rest -> title
        D = ix.drawing(did, page, (0.0, 0.0, W, H), units="mm", dkind="diagram", scale_bar=False, priority=i + 1,
                       group=did, fit=PS_FIT, title=head)
        kc = _ps_layers(ix, D, its, kinds)
        nl = ps_label_items(ix, D, did, lbl)
        # v21 (L1_engine "ONE BOX PER DRAWING"): every part attached with drawing=D; disc number without `at`
        ix.text(page, num, "badge", drawing=did, priority=1, group=did, id=did + "_num")
        ix.text(page, head, "heading", drawing=did, priority=1, group=did, id=did + "_title")
        ix.text(page, purpose, "caption", drawing=did, priority=1, group=did, id=did + "_purpose")
        for el in set(k_[1] for k_ in kinds if k_[1] and k_[1][0] == "trees"):
            sp = el[1] if not el[1].startswith(u"trees ") else None
            trees[sp] = trees.get(sp, 0) + 1
        log.append(u"section %s P%d %s SKETCH (panel %s at %s; not to scale)" % (page, i + 1, cid, key, ttl))
        log.append(u"%s %s: %d items, groups %s" % (page, did, len(its), u", ".join(
            u"%s %d" % (k_, n_) for k_, n_ in sorted(kc.items()))))
        log.append(u"%s %s: labels %d (%d lines) exported at their drawn points; the booklet places them, none left "
                   u"out" % (page, did, nl[0], nl[1]))
    ix.text(page, u"Proposal sections, upstream to downstream · relative levels · 1-11 as in Collect, clean, hold",
            "caption", priority=5, id="ps_caption")
    ix.legend(page, None, ps_legend_entries(), title=None, id="ps_legend_strip", group="ps_legend_strip")
    hue_log(page, log)
    gen = trees.pop(None, 0)
    log.append(u"trees %s species=%d generic=%d (%s; sketch trees: species as the sketch names them)" % (
        page, sum(trees.values()), gen, u", ".join(u"%s %d" % kv for kv in sorted(trees.items()))))
    ps_keymap_items(ix, page, [c for _, c, _, _ in ps_panels()], log)
    for k_, t_, u_ in BK_SOURCES:
        ix.source(k_, t_, u_, page=page)
    for k_, t_ in ps_sources() + PS_SRC_EXTRA:
        ix.source(k_, t_, None, page=page)
    # P7: the circles carry the 28 Oct numbers, which CCH_STEPS takes over (S1); logged so the run shows the names
    log.append(u"%s numbers 1-11 as CCH_STEPS: %s" % (page, u"; ".join(
        u"%d %s" % (n_, cch_name(n_)) for n_ in range(1, 12))))
    return ix
