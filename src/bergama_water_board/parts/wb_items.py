# ============================================================ v15 (round 5, S8; G-R5-12): THE BOOKLET'S ITEMS, NOT A SHEET
# Aras 1 Nov 22:00 (G-R5-12): content scripts only export drawings and texts as items; the booklet (run last) places,
# sizes, aligns, checks and composes every page. Addendum 22:37: no per-script sheet PDFs or previews; labels are
# exported with their anchors. Change of approach (Aras 22:46): the board's text checks stopped runs in round 4 again
# and again (p12 legend, p18 numbers); they no longer decide anything here. The pages still draw onto the board's Page
# (board mm, y up) as a RECORDER; this part hands what they drew to the booklet:
#   wbx_reset()                                  at the start of build_board
#   n0 = wbx_mark(pg)                            the item index now (before drawing one drawing)
#   wbx_drawing(did, page, pg, bb, n0=None, n1=None, den=None, origin=(0, 0), dkind=None, scale_pref=None,
#               title=None, group=None, priority=1, north_deg=None, fit=None, scale_bar=True, crop=None, keep=())
#         ONE booklet drawing = the items pg.items[n0:n1] (all items when n0 is None) that touch bb, cut to bb.
#         bb = (x0, y0, x1, y1) board mm, y up. den = the scale they are drawn at on the board (1:den; None = a
#         scale-free diagram in mm, fit 0.5-2.0). With den: drawing units = metres at true scale,
#         x_d = origin[0] + (x - bb[0]) * den / 1000 (same for y): sections pass origin = (chainage at bb[0],
#         elevation m a.s.l. at bb[1]) so x = chainage, y = elevation (S1 rule; levels on the same y).
#         Texts in the span whose anchor lies in bb: role "label" (Page.text default) -> anchored label items (first
#         position exactly where the page set it, then the 8 compass spots); any other Page.text role (heading,
#         intro, note, caption, list_item, legend, badge, level_value, source, title) -> a text item of that role in
#         the drawing's group (lines of one Page.tgroup joined into one paragraph). crop = the old BK_CROPS id this
#         drawing replaces (that crop is then not exported whole).
#   wbx_text(page, s, role, did=None, at=None, size_pt=None, bold=None, colour=None, priority=5, id=None,
#            short_forms=(), side_list_ok=True, group=None)   a text item; at = board mm (mapped with did's drawing)
#   wbx_legend(page, did, entries, title=None, id=None)       entries [(swatch, text)]; swatch = wbx_sw(...) or a
#         draw function f(pg, x, y, w, h) (drawn into a swatch box, its shapes ride along for a true sample)
#   wbx_sw(kind="fill", colour=None, stroke=None, width_pt=None, dash_pt=None, file=None) -> swatch dict
#   wbx_list(page, did, texts, numbered=True, anchors_board=None, id=None)   ordered rows (anchors board mm)
#   wbx_levels(page, did, levels, side="R")                   levels [(name, z)] on the drawing's y (m a.s.l.)
#   wbx_keymap(page, km, item_id=None)                        v16: km = km_keymap(...) result (common/keymap.py v3,
#                                                             G6-5); km_export_items makes the booklet items, km_log
#                                                             the log line (the booklet places it in the side column)
# v16 (G6-9): every shape keeps the Page.g() tag it was drawn under: one layer per element "<kind>/<element id>",
#   untagged shapes -> no grp ("other" in the booklet); log `groups <page> <drawing> kinds= elements= untagged=`
#   wbx_inset(page, parent, window_bb, child, factor=None)    window = board mm in the PARENT's drawing; factor from
#                                                             the two dens, else `factor` (scale-free zooms, e.g. x3.1)
#   wbx_photo(page, file, caption=None, source=None, id=None)
#   wbx_keep(did, bb)                                         an area (board mm) no label of the page may cover
#   wbx_warn(page, kind, msg)                                 a content check hit (WARNING line + orange)
#   wbx_export(pg, log) -> path                               at the end of the run: writes
#         Downloads/Bergama/cached/booklet/bergama_water_board/items.json (+ results.json beside it)
# Every booklet crop (BK_CROPS) of an exported page that no wbx_drawing replaced is still exported WHOLE (S7's way:
# one drawing, scale_bar False because it carries its own drawn bar), so a page always reaches the booklet.
# Nothing here raises on text; the booklet's check (bergama_booklet 70_check) reports every hit as an orange warning.
# Page ids = PLAN §4 23-page ids (one line: WBX_PAGE). S7 (site board) wrote 25-page ids: S10 settles one numbering.
WBX_PG_SYSTEM, WBX_PG_SEASONS, WBX_PG_NE, WBX_PG_PLANTS = "p12", "p15", "p16", "p18"     # the booklet pages, as the
WBX_PG_SECT_A, WBX_PG_SECT_B, WBX_PG_FARMS = "p19", "p20", "p21"   # pages pass them (25-page numbering, SCRIPT_MAP)
WBX_PAGE = {"p12": "p11", "p15": "p13", "p16": "p14", "p18": "p16", "p19": None, "p20": None, "p21": "p18"}
# v16 (round 6, PLAN §2.1, G6-2): the board pages as the round 6 booklet pages p01-p22: Collect clean hold -> p11, Four
# seasons -> p13, S4 north-east -> p14, Which plant goes where -> p16, Where the clean water goes -> p18. The two
# "Which plant goes where, in section" pages (board p19/p20, r5 p18a/b) are no booklet pages any more (None): their
# items are not exported, one log line per dropped item (PLAN §2.1 last row)
WBX_CROP_PAGE = {"wb_system": "p12", "wb_s4_seasons": "p15", "wb_s4_ne": "p16", "wb_plants": "p18",
                 "wb_plants_b1": "p19", "wb_plants_b2": "p20", "wb_farms": "p21", "wb_farms_out": "p21",
                 "wb_decision": "p21"}           # 25-page numbering of the round 4 crops (SCRIPT_MAP); wb_water and the
                                                 # two concept sections are not booklet pages (not exported)
WBX_HATCH_MIX = 0.72         # design value: a stripe fill becomes its colour mixed this far to white, solid (G-R5-4.1)
WBX_SCALE_TXT = r"^\s*1\s*:\s*[\d,.]+\s*$"       # a lone "1:250": false once the booklet picks the scale
WBX_SCALE_TAIL = r"\s*·?\s*(at\s+)?1\s*:\s*[\d,]{3,}\s*$"
WBX_SW_BOX = (6.0, 4.0)      # a legend swatch's drawing box, mm (design value)
WBX = dict(draw=[], text=[], legend=[], list=[], levels=[], keymap=[], inset=[], photo=[], keep=[], warn=[])
WBX_LOG = []


def wbx_p(page):
    """a page id as the pages know it (board "p18") -> the round 6 export id ("p16"); None = not a booklet page"""
    return WBX_PAGE.get(page, page)


def wbx_title(t):
    """a board cell title as the page's title text: the scale tail ("· F2 and F4 at 1:250" keeps "F2 and F4") goes,
    the booklet prints 1:den itself"""
    import re as _re
    return _re.sub(WBX_SCALE_TAIL, u"", u"%s" % t).strip(u" ·")


def wbx_reset():
    for v in WBX.values():
        del v[:]
    del WBX_LOG[:]
    _GRP.clear()                     # v16 (G6-9): group tags of the last run's items


def wbx_mark(pg):
    return len(pg.items)


def wbx_drawing(did, page, pg, bb, n0=None, n1=None, den=None, origin=(0.0, 0.0), dkind=None, scale_pref=None,
                title=None, group=None, priority=1, north_deg=None, fit=None, scale_bar=True, crop=None, keep=()):
    if bb is None or bb[2] - bb[0] <= 0 or bb[3] - bb[1] <= 0:
        wbx_warn(page, "export", u"drawing %s has an empty box %r" % (did, bb))
        return did
    WBX["draw"].append(dict(id=did, page=page, pg=pg, bb=tuple(bb), n0=n0, n1=len(pg.items) if n1 is None else n1,
                            den=den, origin=tuple(origin), dkind=dkind or ("section" if den else "diagram"),
                            scale_pref=scale_pref, title=title, group=group or did, priority=priority,
                            north_deg=north_deg, fit=fit, scale_bar=scale_bar, crop=crop))
    for b_ in keep or ():
        wbx_keep(did, b_)
    return did


def wbx_text(page, s, role, did=None, at=None, size_pt=None, bold=None, colour=None, priority=5, id=None,
             short_forms=(), side_list_ok=True, group=None):
    if s and (u"%s" % s).strip():
        WBX["text"].append(dict(page=page, s=s, role=role, did=did, at=at, size_pt=size_pt, bold=bold,
                                colour=colour, priority=priority, id=id, short_forms=short_forms,
                                side_list_ok=side_list_ok, group=group))


def wbx_sw(kind="fill", colour=None, stroke=None, width_pt=None, dash_pt=None, file=None):
    d = dict(kind=kind, colour=colour)
    for k_, v_ in (("stroke", stroke), ("width_pt", width_pt), ("dash_pt", dash_pt), ("file", file)):
        if v_ is not None:
            d[k_] = v_
    return d


def wbx_legend(page, did, entries, title=None, id=None):
    WBX["legend"].append(dict(page=page, did=did, entries=list(entries), title=title, id=id))


def wbx_list(page, did, texts, numbered=True, anchors_board=None, id=None):
    WBX["list"].append(dict(page=page, did=did, texts=list(texts), numbered=numbered, anchors=anchors_board, id=id))


def wbx_levels(page, did, levels, side="R"):
    WBX["levels"].append(dict(page=page, did=did, levels=[(n_, z_) for n_, z_ in levels], side=side))


def wbx_keymap(page, km, item_id=None):
    WBX["keymap"].append(dict(page=page, km=km, id=item_id))


def wbx_inset(page, parent, window_bb, child, factor=None):
    WBX["inset"].append(dict(page=page, parent=parent, window=tuple(window_bb), child=child, factor=factor))


def wbx_photo(page, file, caption=None, source=None, id=None):
    WBX["photo"].append(dict(page=page, file=file, caption=caption, source=source, id=id))


def wbx_keep(did, bb):
    WBX["keep"].append((did, tuple(bb)))


def wbx_warn(page, kind, msg):
    WBX["warn"].append((page, kind, msg))


# ---- geometry (copies of the site board's 16d clip helpers: Sutherland-Hodgman / Liang-Barsky)
def _wbx_clip_ring(R, bb):
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
    P = [tuple(p[:2]) for p in R]
    for axis, v, keep_lo in ((0, bb[0], False), (0, bb[2], True), (1, bb[1], False), (1, bb[3], True)):
        if len(P) < 3:
            return []
        P = cut(P, (lambda p, axis=axis, v=v, lo=keep_lo: p[axis] <= v if lo else p[axis] >= v),
                (lambda a, b, axis=axis, v=v: ix_(a, b, axis, v)))
    return P if len(P) >= 3 else []


def _wbx_clip_line(P, bb):
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


def _wbx_hit(b, bb):
    return b[2] >= bb[0] and b[0] <= bb[2] and b[3] >= bb[1] and b[1] <= bb[3]


def _wbx_mix(c, t):
    try:
        r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
        return u"%02X%02X%02X" % tuple(int(round(v + (255 - v) * t)) for v in (r, g, b))
    except Exception:
        return c


def _wbx_shapes(items, bb, grps=None):
    """the non-text page items cut to bb (board mm); stripes -> solid light fill (G-R5-4.1). -> (shapes, n_stripes).
    v16 (G6-9): with a list `grps`, the group tag of each output shape is appended to it (same order)"""
    out, n_h = [], 0
    for it in items:
        kd = it[0]
        n_out = len(out)
        if kd == "poly":
            rings = [r_ for r_ in (_wbx_clip_ring(R0, bb) for R0 in it[1] if len(R0) >= 3) if r_]
            if not rings:
                continue
            fill, stroke = it[2], it[3]
            lw_ = it[4] if len(it) > 4 else 0.1
            dash = it[5] if len(it) > 5 else None
            st = it[6] if len(it) > 6 else None
            al = it[7] if len(it) > 7 else None
            if st:
                n_h += 1
                sc_ = st[0] if isinstance(st, (list, tuple)) and st and isinstance(st[0], str) else None
                fill = fill if (fill and fill not in ("FFFFFF", COL.get("white"))) else _wbx_mix(sc_ or fill or
                                                                                                 "A4A1A3", WBX_HATCH_MIX)
            out.append(("poly", rings, fill, stroke, lw_, dash, None, al))
        elif kd == "line":
            for run in _wbx_clip_line([tuple(p[:2]) for p in it[1]], bb):
                out.append(("line", run, it[2], it[3], it[4] if len(it) > 4 else None, it[5] if len(it) > 5 else 1))
        elif kd == "circle":
            if bb[0] <= it[1] <= bb[2] and bb[1] <= it[2] <= bb[3]:
                out.append(tuple(it))
        elif kd == "image":
            x_, y_, w_, h_ = it[1:5]
            if _wbx_hit((x_, y_, x_ + w_, y_ + h_), bb):
                clip = (max(x_, bb[0]), max(y_, bb[1]), min(x_ + w_, bb[2]), min(y_ + h_, bb[3]))
                out.append(("image", x_, y_, w_, h_, it[5], it[6] if len(it) > 6 else None,
                            it[7] if len(it) > 7 else False, clip))
        if grps is not None:
            grps += [wb_grp_of(it)] * (len(out) - n_out)
    return out, n_h


def _wbx_layers(ix, D, shapes, grps, k_, org):
    """v16 (G6-9, Aras 4 Nov 17:50-17:51): one layer per element, named "<kind>/<element id>" (Page.g tags), in drawing
    order (a run of shapes of one element = one layer, z keeps the order), passed as Ix.layer(..., grp=) (S2 handover
    §1 route 3); untagged runs stay layer "drawing" (no grp: the booklet writes them under "other" + WARNING).
    -> (kinds, elements, untagged shapes)"""
    runs = []
    for sh, g_ in zip(shapes, grps):
        if runs and runs[-1][0] == g_:
            runs[-1][1].append(sh)
        else:
            runs.append((g_, [sh]))
    kinds, elems, n_un = set(), set(), 0
    for z_, (g_, shs) in enumerate(runs):
        if not g_:
            n_un += len(shs)
            ix.layer(D, "drawing", shs, z=z_, k=k_, origin=org)   # no tag: the booklet writes it under "other"
            continue
        kinds.add(g_.split(u"/", 1)[0])
        elems.add(g_)
        ix.layer(D, g_, shs, z=z_, k=k_, origin=org, grp=g_)      # S2 item_export: grp stamped on each shape
    return len(kinds), len(elems), n_un


def _wbx_src(s):
    """the board's [n] source marks -> {src:wb_n} (S5's form; the booklet numbers them on its Sources page)"""
    import re as _re
    n = len(globals().get("SRC_KEY") or ())

    def rep(m):
        nums = [int(v) for v in _re.findall(r"\d+", m.group(0))]
        if not nums or max(nums) > n or min(nums) < 1:
            return m.group(0)
        return u" ".join(u"{src:wb_%d}" % v for v in nums)
    return _re.sub(r"\[\d+(?:\s*[,–-]\s*\d+)*\]", rep, s)


class _WbxMap(object):
    def __init__(self, r):
        self.bb, self.k = r["bb"], (float(r["den"]) / 1000.0 if r["den"] else 1.0)
        self.o = r["origin"]

    def __call__(self, q):
        return (self.o[0] + (q[0] - self.bb[0]) * self.k, self.o[1] + (q[1] - self.bb[1]) * self.k)


def _wbx_texts(ix, r, items, M, pats, tail):
    """texts of a drawing's span with their anchor in bb -> label items / role items; returns (labels, others)"""
    bb, did, page = r["bb"], r["id"], wbx_p(r["page"])
    groups, order = {}, []
    for it in items:
        if it[0] != "text":
            continue
        s_ = (u"%s" % (it[1] or u"")).strip()
        if not s_ or not (bb[0] <= it[2] <= bb[2] and bb[1] <= it[3] <= bb[3]):
            continue
        tag = _TXT_TAG.get(id(it))
        g_, role = (tag[1], tag[4]) if tag is not None and tag[0] is it else (u"i%d" % id(it), "label")
        if g_ not in groups:
            groups[g_] = []
            order.append(g_)
        groups[g_].append((it, role))
    n_lab = n_oth = 0
    for g_ in order:
        rows = groups[g_]
        rows.sort(key=lambda t_: (-round(t_[0][3], 1), t_[0][2]))
        lines, cur, cy = [], [], None
        for it, _r in rows:                              # one line = items on one baseline (runs), lines top-down
            if cy is not None and abs(it[3] - cy) > 0.05:
                lines.append(u"".join(cur))
                cur = []
            cur.append(u"%s" % it[1])
            cy = it[3]
        if cur:
            lines.append(u"".join(cur))
        s_ = _wbx_src(u" ".join(l_.strip() for l_ in lines if l_.strip()))
        if any(q_.search(s_) for q_ in pats):
            continue
        s_ = tail.sub(u"", s_).strip()
        if not s_:
            continue
        it0, role = rows[0]
        if len([l_ for l_ in lines if l_.strip()]) > 1 and role in (None, "label"):
            # v17.3 (booklet JPG check, p18 "8,000 m³ per ha ... [87]" as one 12 pt line across the page): a block
            # of several lines is handed over line run by line run, each at its own spot, size and weight (the
            # booklet sets runs of one line one after the other); was one paragraph at the first line's size
            for it, _r in rows:
                p_ = tail.sub(u"", _wbx_src(u"%s" % it[1])).strip()
                if not p_:
                    continue
                al_ = it[7] or "L"
                ix.text(page, p_, "label", drawing=did, at=M((it[2], it[3])), size_pt=it[4] / IX_PT,
                        bold=bool(it[6]), colour=it[5] if isinstance(it[5], str) else None,
                        positions=["=" + al_, "E", "NE", "N", "NW", "W", "SW", "S", "SE"], group=r["group"],
                        priority=5)
                n_lab += 1
            continue
        pt = it0[4] / IX_PT
        bold = bool(it0[6])
        col = it0[5] if isinstance(it0[5], str) else None
        al = it0[7] or "L"
        if role in (None, "label") or role not in IX_TEXT_ROLES:
            tid = ix.text(page, s_, "label", drawing=did, at=M((it0[2], it0[3])), size_pt=pt, bold=bold, colour=col,
                          positions=["=" + al, "E", "NE", "N", "NW", "W", "SW", "S", "SE"], group=r["group"],
                          priority=5)
            mat = it0[8] if len(it0) > 8 else None
            if tid and mat:
                deg = math.degrees(math.atan2(mat[0][1], mat[0][0]))
                if abs(deg) >= 0.5:
                    for d_ in reversed(ix.d["pages"].get(page) or []):
                        if d_.get("id") == tid:
                            d_["deg"] = round(deg, 1)
                            break
            n_lab += 1
        else:
            anch = role in ("badge", "level_value")      # v17 (L4, L1 "one box per drawing"): every text of the
            ix.text(page, s_, role, drawing=did, at=M((it0[2], it0[3])) if anch else None,   # span is attached to D
                    size_pt=pt, bold=bold, colour=col, group=r["group"], priority=4)
            n_oth += 1
    return n_lab, n_oth


def _wbx_one(ix, r, photos):
    import re as _re
    pg, bb, page = r["pg"], r["bb"], wbx_p(r["page"])
    span = pg.items[(r["n0"] or 0):r["n1"]]
    M = _WbxMap(r)
    grps = []
    shapes, n_h = _wbx_shapes([it for it in span if it[0] != "text"], bb, grps)
    for (x0, y0, x1, y1, path) in photos:                # plant photos the board embedded after its PDF
        if x0 >= bb[0] - 0.5 and y0 >= bb[1] - 0.5 and x1 <= bb[2] + 0.5 and y1 <= bb[3] + 0.5:
            shapes.append(("image", x0, y0, x1 - x0, y1 - y0, path, None, False, None))
            grps.append(u"plants/photo %s" % os.path.basename(u"%s" % path))
    ext = M((bb[0], bb[1])) + M((bb[2], bb[3]))
    units = "m" if r["den"] else "mm"
    sp = r["scale_pref"]
    if units == "m" and sp is None:
        sp = [int(r["den"])]                             # v18 (L1): the drawing's own scale only (no coarser allowance)
    D = ix.drawing(r["id"], page, ext, scale_pref=sp, units=units, dkind=r["dkind"], north_deg=r["north_deg"],
                   scale_bar=bool(r["scale_bar"]), priority=r["priority"], group=r["group"], fit=r["fit"],
                   title=r["title"])
    if units == "m":
        D["board_den"] = int(r["den"])
    k_ = M.k
    nk, ne, nu = _wbx_layers(ix, D, shapes, grps, k_, (M.o[0] - bb[0] * k_, M.o[1] - bb[1] * k_))
    WBX_LOG.append(u"groups %s %s kinds=%d elements=%d untagged=%d" % (page, r["id"], nk, ne, nu))
    pats = [_re.compile(WBX_SCALE_TXT)]
    nl, no = _wbx_texts(ix, r, span, M, pats, _re.compile(WBX_SCALE_TAIL))
    WBX_LOG.append(u"items %s %s: %s, %d shapes, %d labels, %d texts%s" % (
        page, r["id"], u"1:%d metres" % r["den"] if r["den"] else u"mm", len(shapes), nl, no,
        u", %d stripe fills solid" % n_h if n_h else u""))
    return D, M


def _wbx_sw(ix, sw):
    if isinstance(sw, dict):
        return dict(sw)
    if not callable(sw):
        return dict(kind="fill", colour=sw if isinstance(sw, str) else None)
    W, H = WBX_SW_BOX
    p_ = Page(W, H)
    try:
        sw(p_, 0.0, 0.0, W, H)
    except Exception as ex:
        WBX_LOG.append(u"WARNING legend swatch not drawn (%s)" % type(ex).__name__)
        wn_orange(WBX_LOG[-1][8:])  # v15.1 (closing): this WARNING line also orange (one sink)
        return dict(kind="fill", colour=None)
    sh, _n = _wbx_shapes(p_.items, (0.0, 0.0, W, H))
    fills = [s_ for s_ in sh if s_[0] == "poly" and s_[2]]
    lines = [s_ for s_ in sh if s_[0] == "line"]
    if fills:
        d_ = dict(kind="fill", colour=fills[0][2], stroke=fills[0][3])
    elif lines:
        d_ = dict(kind="dash" if lines[0][4] else "line", colour=lines[0][2], width_pt=round((lines[0][3] or 0.1) /
                                                                                             IX_PT, 2))
    else:
        d_ = dict(kind="fill", colour=None)
    d_["shapes"] = [s_ for s_ in (ix._shape(s_, 1.0, (0.0, 0.0)) for s_ in sh) if s_ is not None]
    for s_ in d_["shapes"]:
        s_.pop("_stripes", None)
    d_["box_mm"] = [W, H]
    return d_


def wbx_export(pg, log):
    """writes items.json from this run's registrations (+ the whole crops nobody replaced) and results.json; returns
    the items path. Every failure is a WARNING, never a stop."""
    import json as _j
    import traceback as _tb
    ix = Ix("bergama_water_board", "bergama_water_board", VERSION)
    maps, done_crops = {}, set()
    # v16 (PLAN §2.1): registrations of board pages that are no booklet page any more are dropped, one line each
    for key_, L_ in WBX.items():
        if key_ == "warn":
            continue
        keep_ = []
        for r_ in L_:
            pg_id = r_[0] if isinstance(r_, tuple) else r_.get("page")
            if isinstance(r_, dict) and pg_id is not None and wbx_p(pg_id) is None:
                WBX_LOG.append(u"items dropped (board page %s is no round 6 booklet page): %s %s" % (
                    pg_id, key_, r_.get("id") or r_.get("did") or u"%s" % (r_.get("s") or u"")[:40]))
            else:
                keep_.append(r_)
        L_[:] = keep_
    WBX["warn"][:] = [w_ for w_ in WBX["warn"] if not (w_[0] and wbx_p(w_[0]) is None)]
    photos = list(globals().get("PHOTOS") or ())
    for r in WBX["draw"]:
        try:
            D, M = _wbx_one(ix, r, photos)
            maps[r["id"]] = (D, M)
            if r["crop"]:
                done_crops.add(r["crop"])
        except Exception:
            ix.warn(wbx_p(r["page"]), "export", u"drawing %s not exported: %s" % (
                r["id"], _tb.format_exc().strip().splitlines()[-1]))
    for cid, rr, den, legend, drop in BK_CROPS:          # a booklet crop no registration replaced: exported whole
        page = WBX_CROP_PAGE.get(cid)
        if page is None or cid in done_crops:
            continue
        if wbx_p(page) is None:                          # v16: a crop of a dropped page
            WBX_LOG.append(u"items dropped (board page %s is no round 6 booklet page): crop %s" % (page, cid))
            continue
        r = dict(id=cid, page=page, pg=pg, bb=tuple(rr), n0=None, n1=len(pg.items), den=den, origin=(0.0, 0.0),
                 dkind="section" if den else "diagram", scale_pref=None, title=BK_CAPTIONS.get(cid) or None,
                 group=cid, priority=1, north_deg=None, fit=None, scale_bar=False, crop=cid)
        try:
            D, M = _wbx_one(ix, r, photos)
            D["scale_note"] = u"whole round 4 crop: carries its own drawn scale bar"
            maps[cid] = (D, M)
            WBX_LOG.append(u"FLAG items %s %s: exported as one whole crop (not split by its page)" % (
                wbx_p(page), cid))
        except Exception:
            ix.warn(wbx_p(page), "export", u"crop %s not exported: %s" % (cid, _tb.format_exc().strip().splitlines()[-1]))

    def mp(did, q):
        return maps[did][1](q) if did in maps and q is not None else None
    for t in WBX["text"]:
        try:
            ix.text(wbx_p(t["page"]), _wbx_src(u"%s" % t["s"]), t["role"],   # v17 (L4): attached to its drawing
                    drawing=t["did"] if t["did"] in maps else None,
                    at=mp(t["did"], t["at"]), size_pt=t["size_pt"], bold=t["bold"], colour=t["colour"],
                    priority=t["priority"], id=t["id"], short_forms=t["short_forms"],
                    side_list_ok=t["side_list_ok"], group=t["group"] or t["did"])
        except Exception:
            ix.warn(wbx_p(t["page"]), "export", u"text not exported: %s" % _tb.format_exc().strip().splitlines()[-1])
    for d_, bb in WBX["keep"]:
        if d_ in maps:
            a, b = mp(d_, bb[:2]), mp(d_, bb[2:])
            ix.keep(maps[d_][0], (a[0], a[1], b[0], b[1]))
    for L in WBX["legend"]:
        try:
            ix.legend(wbx_p(L["page"]), L["did"], [(_wbx_sw(ix, sw), _wbx_src(u"%s" % tx) if isinstance(tx, str) else
                                                    tx) for sw, tx in L["entries"]],
                      title=L["title"], id=L["id"], group=L["did"])
        except Exception:
            ix.warn(wbx_p(L["page"]), "export", u"legend not exported: %s" % _tb.format_exc().strip().splitlines()[-1])
    for L in WBX["list"]:
        an = [mp(L["did"], a_) for a_ in L["anchors"]] if L["anchors"] else None
        ix.list(wbx_p(L["page"]), L["did"], [_wbx_src(u"%s" % t_) for t_ in L["texts"]], numbered=L["numbered"],
                anchors=an, id=L["id"], group=L["did"])
    for L in WBX["levels"]:
        ix.levels(wbx_p(L["page"]), L["did"], L["levels"], side=L["side"], group=L["did"])
    for K in WBX["keymap"]:
        try:
            page = wbx_p(K["page"])
            # v16 (G6-5): the one key-map module (common/keymap.py v3, S1): km_keymap(...) result -> booklet items
            its = km_export_items(K["km"], page, K["id"] or u"%s_keymap" % page)
            kd = None
            for it in its:
                it = dict(it)
                it["id"] = ix._id(it.get("id"), it.get("kind", "item"))
                it["page"] = page
                if it.get("kind") == "drawing" and kd is None:
                    kd = it["id"]
                elif it.get("anchor") and kd is not None:
                    it["anchor"] = dict(it["anchor"], drawing=kd)
                elif it.get("kind") == "keymap" and kd is not None:
                    it["drawing"] = kd
                ix._put(page, it)
            WBX_LOG.append(u"items %s key map %s: %d items" % (page, kd, len(its)))
        except Exception:
            ix.warn(wbx_p(K["page"]), "export", u"key map not exported: %s" % _tb.format_exc().strip().splitlines()[-1])
    for I in WBX["inset"]:
        if I["parent"] in maps and I["child"] in maps:
            a, b = mp(I["parent"], I["window"][:2]), mp(I["parent"], I["window"][2:])
            dp, dc = maps[I["parent"]][0].get("board_den"), maps[I["child"]][0].get("board_den")
            ix.inset(wbx_p(I["page"]), I["parent"], (a[0], a[1], b[0], b[1]), I["child"],
                     float(dp) / float(dc) if dp and dc else float(I.get("factor") or 1.0))
        else:
            ix.warn(wbx_p(I["page"]), "export", u"inset %s -> %s: a drawing is missing" % (I["parent"], I["child"]))
    for P in WBX["photo"]:
        ix.photo(wbx_p(P["page"]), P["file"], caption=P["caption"], source=P["source"], id=P["id"])
    for page, kind, msg in WBX["warn"]:
        ix.warn(wbx_p(page) if page else None, kind, msg)
    try:
        for i_, k_ in enumerate(globals().get("SRC_KEY") or ()):
            ix.source(u"wb_%d" % (i_ + 1), u"%s" % k_, None)
    except Exception:
        pass
    seen = set(r_["page"] for r_ in WBX["draw"]) | set(WBX_CROP_PAGE.get(c_[0]) for c_ in BK_CROPS)
    for p25 in sorted(set(WBX_CROP_PAGE.values())):
        if p25 not in seen and wbx_p(p25) is not None:
            ix.warn(wbx_p(p25), "export", u"page %s drew nothing this run (see its 'stopped drawing' line)" % p25)
    path = ix.save()
    try:
        with open(os.path.join(bg_booklet("bergama_water_board"), "results.json"), "w", encoding="utf-8") as f:
            _j.dump(bk_results(), f, ensure_ascii=False, indent=1)
        WBX_LOG.append(u"results.json written (cached/booklet/bergama_water_board/)")
    except Exception:
        ix.warn(None, "export", u"results.json not written: %s" % _tb.format_exc().strip().splitlines()[-1])
    log.extend(WBX_LOG)
    log.append(ix.summary())
    return path
