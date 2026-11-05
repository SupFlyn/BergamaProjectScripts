# ============================================================ v60 (round 5, S7; G-R5-12): THE BOOKLET'S ITEMS, NOT CROPS
# Aras 1 Nov 22:00 (G-R5-12): content scripts only export drawings and texts as items; the booklet (run last) places,
# sizes, aligns, checks and composes every page. Addendum 22:37: no per-script sheet PDFs; labels are exported with
# their anchors. Change of approach (Aras 22:46): the site board's text-collision check (16c sb_text_check) stopped
# runs in round 4 again and again; it is gone. The board still draws every page into Board.items exactly as before,
# and this step hands each booklet crop (CROP_PANELS, the rectangles the pages register with crop_panel) to the
# booklet as ONE item drawing:
#   - shapes (fills, lines, images; hatches as a light solid fill, G-R5-4.1) clipped to the crop, in draw order;
#   - every text whose anchor lies in the crop = an anchored label item (first position exactly where the page set it,
#     then the 8 compass spots), never burnt into the drawing; a crop holding only texts (the p07 notes) = note items;
#   - the crop's legend rows = one legend item, its caption = a caption item;
#   - plans and sections (crop scale known) in METRES at true scale (scale_pref = the Bergama list); diagrams in the mm
#     they were drawn for on the booklet page (fit 0.5-2.0).
# The p03 axonometric (DIAG_SRC page, CROP_DIRECT) goes the same way (mm, its own page items). Nothing here raises on
# text: the booklet's check (bergama_booklet 70_check) reports every hit as an orange warning.
#   sb_items_export(S, B) -> [log lines]   writes Downloads/Bergama/cached/booklet/selinus_board/items.json
# Page ids: v61 (round 6, G6-2, PLAN §2.1): the final 22-page ids, used natively (p08 street cuts R1-R4 + key map,
# p19 heritage loop); the booklet no longer maps ids.
SB_IX_PAGES = {"plan01": "p02", "site_readings": "p02", "edge_types": "p02", "axo_what_is_there": "p03",
               "edge_build": "p06", "movement": "p07",
               "walking_today": "p07", "driving_today": "p07", "mv_note_1": "p07", "mv_note_2": "p07",
               "mv_note_3": "p07", "street_R1": "p08", "street_R2": "p08", "street_R3": "p08", "street_R4": "p08",
               "heritage_loop": "p19"}
SB_KM = {}           # v61: item id -> (page, key map dict) of every other key map (p08 sb_street_keymap ...)
SB_LEG = {}          # v61: item id -> (page, legend entries) of a stand-alone legend item (p08 sb_street_legend ...)
# v61 (G6-9, Aras 4 Nov 17:50-17:51 "apply this to everything"): each primitive carries grp = "<kind>/<element id>"
# (Board.kind tags; untagged shapes = "other", untagged texts = "labels"); axonometric layers -> kinds below
SB_AXO_KIND = {"trees": "trees", "tree_shadows": "trees", "base": "buildings", "outline": "buildings",
               "services": "buildings", "historic_wall": "heritage", "stream": "water", "ground_stream": "water",
               "pools": "water", "banks": "water", "parks": "plants", "ground_streets": "roads", "legend": "legend",
               "callouts": "labels", "words": "labels", "text": "labels", "scale": "annotations",
               "north": "annotations", "arrows": "annotations", "sheet": "frame", "drawing": "other",
               # v62 (L2, 4 Nov run: p03 21049 untagged): the layers draw_building / the ground / overlays / figures use
               "topic": "buildings", "context": "buildings", "ground": "ground", "overlay": "annotations",
               "figures": "people"}
# v62 (L2): an untagged board shape takes its kind from its layer's last part (LU_BOARD::Map::water ...); else "other"
SB_LAYER_KIND = {"water": "water", "ground": "ground", "paper": "ground", "landcover": "ground", "texture": "ground",
                 "trees": "trees", "streets": "roads", "walls": "buildings", "buildings": "buildings",
                 "annotation": "annotations", "legend": "legend"}
SB_ROLE = {}         # v62 (L2, L1_engine "ONE BOX PER DRAWING"): full text -> its box role ("heading"; no `at`)
SB_SHORT = {}        # v62 (L2): full text -> its short forms (the booklet tries them before numbering / shrinking)
SB_GRP_N = {}        # page -> [kinds set, elements set, untagged n]
SB_IX_SCALES = {"plan01": [2500, 5000, 10000, 20000]}     # P02.2: p02 at 1:20,000 or larger (listed scales only)
SB_IX_MUL_ALPHA = 0.55       # design value: a multiplying Tint (15f) has no blend mode in the booklet's writer; drawn
                             # see-through instead so the base keeps showing (FLAG in the log)
SB_IX_HATCH_MIX = 0.72       # design value: a hatch becomes its colour mixed this far to white, as one solid fill
SB_IX_SCALE_TXT = r"^\s*1\s*:\s*[\d,.]+\s*$"           # a lone "1:5,000": false once the booklet picks the scale
SB_IX_SCALE_TAIL = r"\s*·?\s*1\s*:\s*[\d,]{3,}(\s*(on the a3 page|ON THE A3 PAGE))?\s*$"
SB_IX_LOG = []


def _six_hex(c):
    try:
        return crop_hex(c)
    except Exception:
        return None


def _six_clip_ring(R, bb):
    """Sutherland-Hodgman: ring R cut to the box bb (x0, y0, x1, y1)"""
    def cut(P, inside, inter):
        out = []
        n = len(P)
        for i in range(n):
            a, b = P[i - 1], P[i]
            ia, ib = inside(a), inside(b)
            if ib:
                if not ia:
                    out.append(inter(a, b))
                out.append(b)
            elif ia:
                out.append(inter(a, b))
        return out

    def ix_(a, b, axis, v):
        d = b[axis] - a[axis]
        t = 0.0 if abs(d) < 1e-12 else (v - a[axis]) / d
        return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
    P = list(R)
    for axis, v, keep_lo in ((0, bb[0], False), (0, bb[2], True), (1, bb[1], False), (1, bb[3], True)):
        if len(P) < 3:
            return []
        P = cut(P, (lambda p, axis=axis, v=v, lo=keep_lo: p[axis] <= v if lo else p[axis] >= v),
                (lambda a, b, axis=axis, v=v: ix_(a, b, axis, v)))
    return P if len(P) >= 3 else []


def _six_clip_line(P, bb):
    """a polyline cut to bb: the runs inside (Liang-Barsky per segment)"""
    runs, cur = [], []
    for a, b in zip(P, P[1:]):
        t0, t1 = 0.0, 1.0
        dx, dy = b[0] - a[0], b[1] - a[1]
        ok = True
        for p_, q_ in ((-dx, a[0] - bb[0]), (dx, bb[2] - a[0]), (-dy, a[1] - bb[1]), (dy, bb[3] - a[1])):
            if abs(p_) < 1e-12:
                if q_ < 0:
                    ok = False
                    break
                continue
            r_ = q_ / p_
            if p_ < 0:
                t0 = max(t0, r_)
            else:
                t1 = min(t1, r_)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        A_ = (a[0] + t0 * dx, a[1] + t0 * dy)
        B_ = (a[0] + t1 * dx, a[1] + t1 * dy)
        if cur and abs(cur[-1][0] - A_[0]) < 1e-9 and abs(cur[-1][1] - A_[1]) < 1e-9:
            cur.append(B_)
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [A_, B_]
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def _six_bb_hit(bb, r):
    return bb is not None and bb[2] >= r[0] and bb[0] <= r[2] and bb[3] >= r[1] and bb[1] <= r[3]


def _six_crop_sc(p, w_mm, h_mm):
    """the factor the crop was drawn for on the booklet page (as the round 4 check: bk_w, else the panel fit)"""
    if p.get("bk_w"):
        return p["bk_w"] / w_mm
    return min(BK_AW / w_mm, BK_AH / h_mm)


def _six_grp_count(page, did, grps, note):
    """v61 (G6-9): counts for the `groups <page>` log line; one WARNING per drawing with untagged shapes"""
    c_ = SB_GRP_N.setdefault(page, [set(), set(), 0])
    un = 0
    for g_ in grps:
        k_ = g_.split("/", 1)[0]
        c_[0].add(k_)
        c_[1].add(did + "/" + g_)
        if k_ == "other":
            un += 1
    c_[2] += un
    if un:
        note.append(u"WARNING %s groups %s: %d untagged shape(s) in kind \"other\"" % (page, did, un))


def _six_layer_grp(ix, D, name, shapes, grps):
    """v61 (G6-9): ix.layer with each written shape dict carrying its grp (shapes the writer drops are skipped
    here the same way, so the two lists stay aligned)"""
    keep = [(s_, g_) for s_, g_ in zip(shapes, grps)
            if s_ and s_[0] != "text" and ix._shape(s_, 1.0, (0.0, 0.0)) is not None]
    r_ = ix.layer(D, name, [s_ for s_, _g in keep])
    out = D["layers"][-1]["shapes"] if D.get("layers") else []
    for sh, (_s, g_) in zip(out, keep):
        sh["grp"] = g_
    return r_


def _six_text_grp(ix, page, tid, grp):
    """v61 (G6-9): the grp of an exported text item"""
    if not tid:
        return
    for it_ in reversed(ix.d["pages"].get(page) or []):
        if it_.get("id") == tid:
            it_["grp"] = grp
            break


def _six_board_crop(ix, B, p, page, note):
    """one CROP_PANELS crop of board B -> one drawing (or notes) + texts + legend + caption in ix"""
    import re as _re
    k = 1000.0 / PDF_SCALE                               # sheet mm per board unit
    bb = p["bb"]
    w_mm, h_mm = (bb[2] - bb[0]) * k, (bb[3] - bb[1]) * k
    if w_mm <= 0 or h_mm <= 0:
        ix.warn(page, "export", u"crop %s is empty (%.1f x %.1f mm)" % (p["slug"], w_mm, h_mm))
        return
    sc = _six_crop_sc(p, w_mm, h_mm)
    den = p.get("scale_den")
    if den:                                              # true scale: board unit -> m
        units, ku = "m", float(den) / PDF_SCALE
    else:                                                # a diagram: board unit -> booklet mm as drawn for the page
        units, ku = "mm", k * sc
    pats = [_re.compile(d_) for d_ in (p.get("drop") or ())] + [_re.compile(SB_IX_SCALE_TXT)]
    tail = _re.compile(SB_IX_SCALE_TAIL)
    did = u"sb_" + p["slug"]
    yoff = 0.0                                           # v62 (L2): a section's y = m a.s.l. (its level column's datum)
    if units == "m" and p.get("datum"):
        yoff = p["datum"][1] - (p["datum"][0] - bb[1]) * ku

    def M(q):
        return ((q[0] - bb[0]) * ku, (q[1] - bb[1]) * ku + yoff)
    pad = 0.01 * max(bb[2] - bb[0], bb[3] - bb[1])
    cb = (bb[0] - pad, bb[1] - pad, bb[2] + pad, bb[3] + pad)
    order = []
    tags = getattr(B, "tags", None) or {}
    m_col = _re.match(r"mv_note_(\d+)$", u"%s" % p["slug"])   # v62.2: a p07 column's crop runs past its map once
    col_re = _re.compile(r"column (\d+) ")                    # nothing is left out (L2) and reaches the next
    #                                                          # column: it keeps only its own column's shapes/texts

    def other_col(n_):
        if not m_col:
            return False
        c_ = col_re.search(u"%s " % (tags.get(n_) or u""))
        return bool(c_) and c_.group(1) != m_col.group(1)
    for n_, it in enumerate(B.items):
        if it[0] == "text" or other_col(n_):
            continue
        o_ = it[4]
        try:
            o_ = float(o_)
        except Exception:
            o_ = 0.0
        if _six_bb_hit(_item_bb(it), bb):
            order.append((o_, n_, it))
    order.sort(key=lambda t_: (t_[0], t_[1]))
    shapes, n_mul, n_hatch, n_nz = [], 0, 0, 0
    grps = []                                            # v61 (G6-9): one grp per shape
    for _o, _n, it in order:
        kd = it[0]
        g_ = tags.get(_n)
        if not g_:                                       # v62 (L2): untagged: the layer's kind, else "other"
            lk_ = SB_LAYER_KIND.get((u"%s" % it[3]).split("::")[-1].lower())
            g_ = u"%s/%s %d" % (lk_, (u"%s" % it[3]).split("::")[-1], _n) if lk_ else u"other/%d" % _n
        n0_ = len(shapes)
        if kd in ("fill", "hatch"):
            col_ = it[2]
            if kd == "hatch":
                col_ = mix(col_, WHITE, SB_IX_HATCH_MIX)
                n_hatch += 1
            rings = [_six_clip_ring(P_, cb) for P_ in it[1] if len(P_) >= 3]
            rings = [[M(q) for q in R_] for R_ in rings if R_]
            if not rings:
                continue
            a_ = None
            if getattr(it[2], "mul", False):
                a_ = SB_IX_MUL_ALPHA
                n_mul += 1
            if getattr(it[2], "nz", False):
                n_nz += 1
            shapes.append(("poly", rings, _six_hex(col_), None, 0.0, None, None, a_))
        elif kd == "line":
            w_ = (it[5] if it[5] is not None else 0.13) * PDF_LINE_SCALE * sc     # print mm on the booklet page
            for run in _six_clip_line(list(it[1]), cb):
                shapes.append(("line", [M(q) for q in run], _six_hex(it[2]), w_, None))
        elif kd == "image":
            x0_, y0_, x1_, y1_ = it[2]
            a0, a1 = M((x0_, y0_)), M((x1_, y1_))
            shapes.append(("image", a0[0], a0[1], a1[0] - a0[0], a1[1] - a0[1], it[1],
                           it[6] if len(it) > 6 else None, bool(it[7]) if len(it) > 7 else False))
        grps.extend([g_] * (len(shapes) - n0_))
    texts = []
    for n_, it in enumerate(B.items):                    # texts: anchor inside the crop
        if it[0] != "text" or other_col(n_):
            continue
        txt = (u"%s" % it[1]).strip()
        if not txt or any(q_.search(txt) for q_ in pats):
            continue
        x_, y_ = it[2]
        if not (bb[0] <= x_ <= bb[2] and bb[1] <= y_ <= bb[3]):
            continue
        txt = tail.sub(u"", txt).strip()
        if not txt:
            continue
        h_ = it[3]
        al = it[9] or "L"
        if al == "MC":                                   # middle-centre -> centre on the baseline
            y_ -= 0.5 * h_
            al = "C"
        pt = h_ * k / _PDF_CAP[kind_of(it[7])] / IX_PT * sc
        texts.append((txt, M((x_, y_)), pt, bool(it[8]), _six_hex(it[4]), al, math.degrees(it[10] or 0.0),
                      it[13] if len(it) > 13 else None, tags.get(n_) or u"labels/t%d" % n_))
    if not shapes:                                       # a text-only crop (p07 notes): notes in reading order
        groups, seen = {}, []
        for t_ in sorted(texts, key=lambda t_: (-t_[1][1], t_[1][0])):
            g_ = t_[7] or id(t_)
            if g_ not in groups:
                groups[g_] = []
                seen.append(g_)
            groups[g_].append(t_)
        for i_, g_ in enumerate(seen):
            ts = groups[g_]
            ix.text(page, u" ".join(t_[0] for t_ in ts), "note", size_pt=ts[0][2], bold=ts[0][3] or None,
                    priority=5, group=p.get("note_of") or did, id=u"%s_n%d" % (did, i_ + 1),
                    drawing=p.get("note_of"))            # v62 (L2): a cut's note is attached to its drawing
        note.append(u"items %s %s: notes %d (text only)" % (page, p["slug"], len(seen)))
        return
    ext = (0.0, yoff, (bb[2] - bb[0]) * ku, (bb[3] - bb[1]) * ku + yoff)
    D = ix.drawing(did, page, ext, scale_pref=SB_IX_SCALES.get(p["slug"]), units=units,
                   dkind=p.get("dkind") or ("plan" if units == "m" else "diagram"), scale_bar=False, priority=1, group=did,
                   title=p.get("caption") or None)
    if units == "m":
        D["scale_note"] = (u"own scale bar drawn as geometry (true at any print scale); sheet scale 1:%d, round 4 "
                           u"booklet print about 1:%d" % (int(den), int(round(den / sc))))
    _six_layer_grp(ix, D, "drawing", shapes, grps)
    _six_grp_count(page, did, grps + [t_[8] for t_ in texts], note)
    for t_ in texts:
        if SB_ROLE.get(t_[0]):                           # v62 (L2): a box part (heading): the booklet sets it, no `at`
            tid = ix.text(page, t_[0], SB_ROLE[t_[0]], drawing=did, size_pt=t_[2], bold=t_[3], colour=t_[4],
                          group=did, priority=1, short_forms=SB_SHORT.get(t_[0]) or ())
            _six_text_grp(ix, page, tid, t_[8])
            continue
        tid = ix.text(page, t_[0], "label", drawing=did, at=t_[1], size_pt=t_[2], bold=t_[3], colour=t_[4],
                      positions=["=" + t_[5], "E", "NE", "N", "NW", "W", "SW", "S", "SE"], group=did, priority=5,
                      short_forms=SB_SHORT.get(t_[0]) or ())
        _six_text_grp(ix, page, tid, t_[8])
        if tid and abs(t_[6]) >= 0.5:                    # a turned label (street names): its angle for the booklet
            for it_ in reversed(ix.d["pages"].get(page) or []):
                if it_.get("id") == tid:
                    it_["deg"] = round(t_[6], 1)
                    break
    # sb_keep areas are NOT exported: they hold the drawing's own texts (a key map's names, a map's tags), which the
    # booklet would then push off; the whole drawing is already a keep that only its own labels may enter (30_render)
    if p.get("levels"):                                  # v62 (L2): the cut's level values; the booklet sets them
        sf_level_items(ix, page, D, p["levels"], side="R")
        note.append(u"items %s %s: %d level values exported (%s)" % (page, p["slug"], len(p["levels"]), u", ".join(
            u"%s %+.2f" % (k_, v_) for k_, v_ in p["levels"])))
    if p.get("legend"):
        ents = [(dict(kind={"dashdot": "dash"}.get(e_["kind"], e_["kind"]), colour=e_["colour"]), e_["label"])
                for e_ in p["legend"] if e_.get("label")]
        if ents:
            ix.legend(page, did, ents, group=did, id=did + "_legend")
    if p.get("caption"):
        cap_ = tail.sub(u"", p["caption"]).strip()
        ix.text(page, cap_, "caption", group=did, priority=6, id=did + "_caption",
                short_forms=SB_SHORT.get(p["caption"]) or SB_SHORT.get(cap_) or ())
    if p.get("geo"):                                     # plan 01's georeference (agriculture's farms layer)
        D["georef"] = [[round(gx, 3), round(gy, 3), round((bx - bb[0]) * ku, 3), round((by - bb[1]) * ku, 3)]
                       for gx, gy, bx, by in p["geo"]]
    if n_mul:
        note.append(u"FLAG items %s %s: %d multiplying tint fill(s) drawn see-through (%.2f), no blend mode" % (
            page, p["slug"], n_mul, SB_IX_MUL_ALPHA))
    if n_nz:
        note.append(u"FLAG items %s %s: %d nonzero fill(s) written even-odd (overlapping rings may show holes)" % (
            page, p["slug"], n_nz))
    if n_hatch:
        note.append(u"items %s %s: %d hatch(es) as solid light fills (G-R5-4.1)" % (page, p["slug"], n_hatch))
    note.append(u"items %s %s: %s, %d shapes, %d labels%s" % (
        page, p["slug"], u"1:%d sheet, metres" % den if units == "m" else u"mm x %.2f" % sc, len(shapes),
        len(texts), u", legend %d" % len(p.get("legend") or ()) if p.get("legend") else u""))


def _six_axo(ix, pg, rm, ph, cap, leg, note):
    """the p03 axonometric (DIAG_SRC page items, mm y up; rm = crop mm from the top, y down) -> one mm drawing"""
    page, did = "p03", u"sb_axo_what_is_there"
    bb = (rm[0], ph - rm[3], rm[2], ph - rm[1])

    def M(q):
        return (q[0] - bb[0], q[1] - bb[1])
    shapes, texts, n_h = [], [], 0
    grps, n_el = [], {}                                  # v61 (G6-9): axonometric layers -> kinds

    def G(lay):
        k_ = SB_AXO_KIND.get(lay or "", "other")
        n_el[k_] = n_el.get(k_, 0) + 1
        return u"%s/%04d" % (k_, n_el[k_])
    for it in pg.items:
        kd = it[0]
        n0_ = len(shapes)
        lay_ = {"poly": 6, "line": 5, "circle": 7, "text": 8}.get(kd)
        lay_ = it[lay_] if lay_ is not None and len(it) > lay_ else None
        if kd == "poly":
            rings = [[M(q) for q in R_] for R_ in (_six_clip_ring(R0, bb) for R0 in it[1]) if R_]
            if not rings:
                continue
            fill, stroke, lw_, dash = it[2], it[3], it[4], it[5]
            if len(it) > 8 and it[8]:                    # stripes: solid (G-R5-4.1)
                n_h += 1
            shapes.append(("poly", rings, fill, stroke, lw_ or 0.0, dash, None, it[9] if len(it) > 9 else None))
        elif kd == "line":
            for run in _six_clip_line(list(it[1]), bb):
                shapes.append(("line", [M(q) for q in run], it[2], it[3], it[4], it[6] if len(it) > 6 else 1))
        elif kd == "circle":
            if bb[0] <= it[1] <= bb[2] and bb[1] <= it[2] <= bb[3]:
                c_ = M((it[1], it[2]))
                shapes.append(("circle", c_[0], c_[1], it[3], it[4], it[5], it[6]))
        elif kd == "image":
            x_, y_, w_, h_ = it[1:5]
            if _six_bb_hit((x_, y_, x_ + w_, y_ + h_), bb):
                c_ = M((x_, y_))
                shapes.append(("image", c_[0], c_[1], w_, h_) + tuple(it[5:9]))
        elif kd == "text":
            s_, x_, y_, sz = it[1], it[2], it[3], it[4]
            if s_ and s_.strip() and bb[0] <= x_ <= bb[2] and bb[1] <= y_ <= bb[3]:
                texts.append((s_.strip(), M((x_, y_)), sz / IX_PT, bool(it[6]), it[5], it[7] or "L",
                              it[9] is not None, G(lay_ if lay_ not in (None, "drawing") else "text")))
        if len(shapes) > n0_:
            g_ = G(lay_)
            grps.extend([g_] * (len(shapes) - n0_))
    D = ix.drawing(did, page, (0.0, 0.0, bb[2] - bb[0], bb[3] - bb[1]), units="mm", dkind="axo", scale_bar=False,
                   priority=1, group=did, title=cap)
    _six_layer_grp(ix, D, "drawing", shapes, grps)
    _six_grp_count(page, did, grps + [t_[7] for t_ in texts], note)
    n_plane = 0
    for t_ in texts:
        tid = ix.text(page, t_[0], "label", drawing=did, at=t_[1], size_pt=t_[2], bold=t_[3], colour=t_[4],
                      positions=["=" + t_[5], "E", "NE", "N", "NW", "W", "SW", "S", "SE"], group=did, priority=5)
        _six_text_grp(ix, page, tid, t_[7])
        if tid and t_[6]:
            n_plane += 1
    if leg:
        ents = [(dict(kind={"dashdot": "dash"}.get(e_["kind"], e_["kind"]), colour=e_["colour"]), e_["label"])
                for e_ in leg if e_.get("label")]
        if ents:
            ix.legend(page, did, ents, group=did, id=did + "_legend")
    if cap:
        ix.text(page, cap, "caption", group=did, priority=6, id=did + "_caption")
    note.append(u"items p03 axo_what_is_there: mm, %d shapes, %d labels (%d set in the drawing plane, exported "
                u"upright)%s" % (len(shapes), len(texts), n_plane, u", %d stripes solid" % n_h if n_h else u""))


def _six_keymap(ix, km, page, item_id, note):
    """v60.2 (G-R5-12, as the city link's cl_keymap): a key map (km_map result) exported with km_items: its drawing
    (key-map mm), label texts anchored on it and the keymap item, ids registered in ix"""
    if "study_ring" in km and "km_export_items" in globals():      # v61: the round 6 key-map module (G6-5)
        its = km_export_items(km, page, item_id)                                              # noqa: F821
    else:
        its = km_items(km, page, item_id=item_id, priority=2)
    did = None
    for it in its:
        it = dict(it)
        it["id"] = ix._id(it.get("id"), it.get("kind", "item"))
        it["page"] = page
        if it.get("kind") == "drawing" and did is None:
            did = it["id"]
        elif it.get("anchor") and did is not None:
            it["anchor"] = dict(it["anchor"], drawing=did)
        elif it.get("kind") == "keymap" and did is not None:
            it["drawing"] = did
        if it.get("kind") == "drawing":                  # v61 (G6-9): a key map is one kind in its drawing
            for L_ in it.get("layers") or ():
                for sh in L_.get("shapes") or ():
                    sh.setdefault("grp", u"keymap/%s" % (L_.get("name") or "map"))
        elif "grp" not in it:
            it["grp"] = u"keymap/labels"
        ix.d["pages"].setdefault(page, []).append(it)
    note.append(u"items %s key map %s: %d items, frame %.0f x %.0f mm" % (page, did, len(its), km["w_mm"], km["h_mm"]))
    return did


def sb_items_export(S, B):
    """v60: every booklet crop of this run as items (module notes), plus the board's results.json, sources and site
    photos; returns the log lines"""
    del SB_IX_LOG[:]
    SB_GRP_N.clear()
    ix = Ix("selinus_board", "selinus_board", SCRIPT_VERSION)
    note, seen = [], set()
    for p in CROP_PANELS:
        page = SB_IX_PAGES.get(p["slug"]) or p.get("ix_page")   # v60.2: p04/p05 per-cut crops carry their page
        if page is None:
            continue
        if p["slug"] in seen:
            ix.warn(page, "export", u"crop %s registered twice: the first is exported" % p["slug"])
            continue
        seen.add(p["slug"])
        try:
            _six_board_crop(ix, B, p, page, note)
        except Exception:
            ix.warn(page, "export", u"crop %s not exported: %s" % (
                p["slug"], traceback.format_exc().strip().splitlines()[-1]))
    for pid_, km_ in sorted(P45_KM.items()):              # v60.2 (G-R5-12 split): the p04/p05 key maps as items
        try:
            _six_keymap(ix, km_, pid_, u"sb_sec_keymap_%s" % pid_, note)
        except Exception:
            ix.warn(pid_, "keymap", u"key map not exported: %s" % traceback.format_exc().strip().splitlines()[-1])
    for pid_, ents_ in sorted(P45_LEG.items()):           # v60.2: the p04/p05 legends (strip colours, lines)
        if ents_:
            ix.legend(pid_, None, ents_, id=u"sb_sec_legend_%s" % pid_)
    for iid_, (pid_, km_) in sorted(SB_KM.items()):      # v61: the other key maps (p08 sb_street_keymap ...)
        try:
            _six_keymap(ix, km_, pid_, iid_, note)
        except Exception:
            ix.warn(pid_, "keymap", u"key map %s not exported: %s" % (
                iid_, traceback.format_exc().strip().splitlines()[-1]))
    for iid_, (pid_, ents_) in sorted(SB_LEG.items()):   # v61: stand-alone legends (p08 sb_street_legend ...)
        if ents_:
            ix.legend(pid_, None, ents_, id=iid_)
    for row in CROP_DIRECT:
        if len(row) < 9 or row[0] != "axo_what_is_there":
            continue
        try:
            _six_axo(ix, row[7], row[2], row[8], row[3], row[5], note)
            seen.add(row[0])
        except Exception:
            ix.warn("p03", "export", u"axonometric not exported: %s" % traceback.format_exc().strip().splitlines()[-1])
    for slug, page in sorted(SB_IX_PAGES.items(), key=lambda kv: kv[1]):
        if slug not in seen:
            ix.warn(page, "export", u"booklet drawing %s was not drawn on this run (no crop registered)" % slug)
    try:                                                  # v51 (D13): p.22's public sources and Commons photo credits
        ix.source("heritage_loop", HER_SRC, None, page="p19")
        for pl_, cr_ in her21_credits():
            ix.source("photo_" + her21_norm(pl_), cr_, None)
    except Exception:
        note.append(u"heritage sources not registered: " + traceback.format_exc().strip().splitlines()[-1])
    for pg_, c_ in sorted(SB_GRP_N.items()):             # v61 (G6-9) log line per page
        note.append(u"groups %s kinds=%d elements=%d untagged=%d" % (pg_, len(c_[0]), len(c_[1]), c_[2]))
    ix.save()
    note.append(ix.summary())
    try:                                                  # the figures the booklet's A pages read (unchanged keys)
        import json as _j
        res = bk_results(S)
        d_ = bg_booklet("selinus_board")
        os.makedirs(d_, exist_ok=True)
        with open(os.path.join(d_, "results.json"), "w", encoding="utf-8") as f_:
            _j.dump(res, f_, ensure_ascii=False, indent=1, sort_keys=True)
    except Exception:
        ix.warn(None, "export", u"booklet results.json not written (%s)" % (
            traceback.format_exc().strip().splitlines()[-1],))
    try:
        bk_photos()
        note.extend(BK_LOG)
    except Exception:
        note.append(u"photos not copied: " + traceback.format_exc().strip().splitlines()[-1])
    return note
