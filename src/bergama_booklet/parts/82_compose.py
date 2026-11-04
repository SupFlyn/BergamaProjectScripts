# ---- 82_compose (round 5 S10; round 6 S9 v31: G6-1 page frames, G6-7/G6-8, G6-9 log): one content page from its items -
# Round 6 (PLAN §3, G6-1): a page is its FRAMES (80_plan, the SUBMISSION_SON arrangement with the drawings enlarged)
# + every item its scripts exported for it. The v30 rows / right column / share are gone. Steps per page:
#   1. sort the page's items (bk_items) and attach every unanchored text, legend and list to one drawing (bk_attach:
#      its "drawing" key, else the longest drawing id its own id starts with, else the one drawing of its group)
#   2. match: each frame takes the items whose id matches one of its fnmatch patterns (first frame wins; drawings,
#      key maps, texts, legends, lists, photos alike)
#   3. scale: every drawing is scaled UNIFORMLY into its frame (never stretched): maps and sections at the largest
#      Bergama-list scale that fits (frames with the same "same" key share one scale = the smallest of their fits, so
#      p04/p05 cuts and p13 seasons print one scale), diagrams / charts / key maps at the largest factor that fits
#      (<= BK_MM_MAX); an inset at >= 2 x its parent's scale. Heading, level column and the scale band (bar or
#      "1:den" + north arrow, outside the drawing, G6-4) are reserved inside the frame
#   4. draw: heading, drawing (30_render), north, level markers, labels (50_place), scale; then the drawing's attached
#      texts / legends / lists / side-list rows go to the frame's "note" frame, else under the drawing in its own frame,
#      else the page's "side" frame
#   5. every item no frame names and no drawing owns = WARNING "unlisted" and goes to the page's side frame (PLAN §2.2:
#      never lost); frames of one page that overlap = WARNING "frames"; an empty frame = WARNING "missing"
#   6. page number; layout check (70_check: overlaps, edges, empty bands, < 4 pt = one WARNING each, G6-7/G6-8); log
#      "page <pid> frames=<n> placed=<n> unlisted=<n>" and "groups <pid> kinds=<n> elements=<n> untagged=<n>" (G6-9)
# Nothing here raises on layout: every misfit is a WARNING (one run collects all; Aras 1 Nov 17:11).
BK_GAP = 4.0               # mm between cells / rows / right-column blocks (grid gutter)
BK_HEAD_H = 4.5            # heading band over a drawing
BK_SCALE_H = 5.5           # scale bar / "1:den" band under a true-scale drawing
BK_LEVEL_W = 24.0          # level markers + "+43.71 Q500" beside a section (3 gap + 9 marker + 12 label)
BK_NORTH_MM = 4.6          # v31: the north arrow sits in the scale band under the plan, right end (outside, G6-4)
BK_NOTE_GAP = 1.5          # mm between stacked notes / legends / lists


def _bk_pat(p):
    return any(c in p for c in "*?[")


def bk_items(pid):
    its = [it for it in ix_page(pid) if isinstance(it, dict)]
    S = dict(items=its, draw={}, keymaps=[], texts=[], legends=[], lists=[], levels=[], insets=[], photos=[],
             titles=[], used=set())
    ref = set()
    for it in its:
        k = it.get("kind")
        if k == "legend":
            ref.update(e.get("text") for e in it.get("entries") or [] if isinstance(e.get("text"), str))
            if isinstance(it.get("title"), str):
                ref.add(it["title"])
        elif k == "list":
            ref.update(t for t in it.get("items") or [] if isinstance(t, str))
        elif k == "photo" and isinstance(it.get("caption"), str):
            ref.add(it["caption"])
    for it in its:
        k = it.get("kind")
        if k == "drawing":
            if it.get("role") == "keymap":
                S["keymaps"].append(it)
            else:
                S["draw"][it["id"]] = it
        elif k == "text":
            a_ = it.get("anchor")
            if it.get("id") in ref:
                continue
            if isinstance(a_, dict) and a_.get("drawing") and _pl_apt(it) is not None:
                continue                                  # an in-drawing label: placed with its drawing
            if it.get("role") == "title":
                S["titles"].append(it)
            else:
                S["texts"].append(it)
        elif k in ("legend", "list", "photo"):
            S[k + "s"].append(it)
        elif k == "level_column":
            S["levels"].append(it)
        elif k == "inset":
            S["insets"].append(it)
    return S


def bk_attach(S):
    """who belongs to which drawing (see step 1); att[did] = dict(head=[texts], side=[items]); page-level in S["page"]"""
    ids = sorted(S["draw"], key=len, reverse=True)
    groups = {}
    for d in sorted(S["draw"].values(), key=lambda d: (d.get("priority", 5), d["id"])):
        groups.setdefault(d.get("group"), []).append(d["id"])
    att = dict((d, dict(head=[], side=[], levels=[])) for d in S["draw"])
    S["page"], S["intro"] = [], None

    def owner(it):
        a_ = it.get("anchor")
        d = it.get("drawing") or (a_.get("drawing") if isinstance(a_, dict) else None)
        if d in att:
            return d
        iid = u"%s" % it.get("id", u"")
        for d in ids:
            if iid.startswith(d + u"_"):
                return d
        g = groups.get(it.get("group"))
        if g:
            return g[0]
        return None
    for t in S["texts"]:
        d = owner(t)
        if t.get("role") == "intro" and (d is None or not (u"%s" % t.get("id", u"")).startswith(d + u"_")):
            if S["intro"] is None:
                S["intro"] = t
                continue
        if d is None:
            S["page"].append(t)
        elif t.get("role") == "heading" and not att[d]["head"]:
            att[d]["head"].append(t)
        else:
            att[d]["side"].append(t)
    for it in S["legends"] + S["lists"]:
        d = owner(it)
        (att[d]["side"] if d else S["page"]).append(it)
    for it in S["levels"]:
        d = it.get("drawing")
        if d in att:
            att[d]["levels"].append(it)
        else:
            wn_warn(it.get("page"), "levels", u"level column %s names drawing %r, not on this page" % (it.get("id"), d))
    S["att"] = att
    for k in ("side",):
        for d in att:
            att[d][k].sort(key=lambda it: (it.get("priority", 5), {"heading": 0, "note": 1, "caption": 2}.get(
                it.get("role"), 3)))
    S["page"].sort(key=lambda it: it.get("priority", 5))
    return att


# ---- sizes --------------------------------------------------------------------------------------------------------
def _bk_parent(S, did):
    for ins in S["insets"]:
        if ins.get("child") == did:
            return ins.get("parent")
    return None


def _bk_res(S, did):
    """(extra width, extra height) round a drawing: level column, heading, scale band"""
    D = S["draw"][did]
    att = S["att"].get(did, {})
    rw = BK_LEVEL_W if att.get("levels") else 0.0
    band = D.get("units") == "m" or (D.get("north_deg") is not None and D.get("role") != "keymap")
    rh = (BK_HEAD_H if att.get("head") else 0.0) + (BK_SCALE_H if band else 0.0)
    return rw, rh


# ---- drawing ------------------------------------------------------------------------------------------------------
def bk_north(P, rect, deg, did):
    """true-north arrow (plain solid arrow + N, no box) OUTSIDE the drawing (G6-4): in the scale band under it, at its
    right end; deg = north's turn from page-up, counter-clockwise (keymap.py north_items convention; UNVERIFIED
    against each script's own sign)"""
    import math as _m
    h = BK_NORTH_MM
    t = _m.radians(float(deg))
    ux, uy = -_m.sin(t), -_m.cos(t)               # page y down
    px, py = -uy, ux
    cx, cy = rect[2] - h / 2.0 - 0.5, rect[3] + BK_SCALE_H / 2.0 + 0.3
    fx, fy = cx - ux * h / 2.0, cy - uy * h / 2.0

    def R(a, b):
        return (fx + ux * b + px * a, fy + uy * b + py * a)
    ink = "2C2219"
    bk_line(P, [R(0.0, 0.0), R(0.0, 0.62 * h)], ink, 0.6)
    hw = 0.24 * h
    bk_poly(P, [R(0.0, h), R(-hw, 0.52 * h), R(hw, 0.52 * h)], ink, None, 0.1)
    pt = 5.0
    P.tp.put(u"N", cx - h / 2.0 - 0.8, cy + fm_asc_desc(pt, True)[0] / 2.0, pt, True, "R", 0.0, "north", "label", ink,
             (did,))
    P.tp.keep((cx - h / 2.0 - 0.3, cy - h / 2.0 - 0.3, cx + h / 2.0 + 0.3, cy + h / 2.0 + 0.3), "north", did)


def bk_badges(P, placed):
    """marker digits stay ON their discs (S6, S8, S9 §5): set at their first exported position, never moved, never
    shrunk (a free spot elsewhere would leave the disc empty)"""
    T = placed["T"]
    for it in ix_texts(placed["D"]):
        if it.get("role") != "badge":
            continue
        a_ = _pl_apt(it)
        if a_ is None:
            continue
        anchor = T.pt(a_[0], a_[1])
        codes = _pl_codes(it.get("positions") or ["=C"])
        pt = max(float(it.get("size_pt") or grid_role("badge")[0]), GRID_MIN_PT)
        x, y, al = P.tp._at(codes[0], it.get("string", u""), anchor, pt, bool(it.get("bold", True)), 0.0)
        P.tp.put(it.get("string", u""), x, y, pt, bool(it.get("bold", True)), al, 0.0, it.get("id"), "badge",
                 it.get("colour"), (placed["id"], "marker"))


def bk_design_den(D):
    """the scale a true-scale drawing's texts were designed at: "sheet scale 1:N" in its scale_note, else None"""
    import re as _re
    m_ = _re.search(r"sheet scale 1:([0-9][0-9,]*)", u"%s" % (D.get("scale_note") or u""))
    return int(m_.group(1).replace(",", "")) if m_ else None


def bk_place(P, S, did, s, x, y, side):
    """one cell at (x, y) top-left: heading, drawing, north, levels, labels, scale (see step 3) -> placed"""
    D = S["draw"][did]
    att = S["att"].get(did, dict(head=[], side=[], levels=[]))
    rw, rh = _bk_res(S, did)
    dw, dh = sc_size(D, s)
    yy = y
    if att["head"]:
        st_para(P, att["head"][0].get("string", u""), x, y, max(dw + rw, 30.0), BK_HEAD_H - 0.6, "heading",
                justify=False, page=P.pid)
        yy += BK_HEAD_H
    T = BkT(D, s, x, yy)
    placed = rd_drawing(P, D, T)
    S["placed"][did] = placed
    if D.get("north_deg") is not None and D.get("role") != "keymap":
        bk_north(P, T.rect, D["north_deg"], did)
    if D.get("window_m"):                            # p09 windows: one size, framed (no frame in the drawing)
        bk_rect(P, T.rect, None, GRID_INK["ink"], 0.5)
    if not T.den:
        lo = (D.get("fit") or (0.5, 2.0))[0]
        if s < lo - 1e-3:
            wn_warn(P.pid, "scale", u"%s set at x%.2f, below its x%.2f minimum (row too full)" % (did, s, lo))
    for lc in att["levels"]:
        pl_levels(P, lc, placed, "R")
    dden = bk_design_den(D)
    if T.den and dden:                              # v30.3: a board drawing (site board: "sheet scale 1:N") keeps its
        pl_rigid(P, placed, float(dden) / float(T.den))   # own text layout, scaled from its sheet scale to this one
    elif T.den:
        bk_badges(P, placed)
        pl_labels(P, placed, side, roles=("label",))
    else:                                           # v30.3: diagrams keep their own text layout, scaled with them
        pl_rigid(P, placed, s)
    if T.den:
        r = T.rect
        if D.get("scale_bar"):
            pl_scalebar(P, placed, r[0], r[3] + 1.2)
        elif did not in S.get("noscale", ()):        # the drawing carries its own bar (S7 crops): the scale only
            pt = grid_role("caption")[0]
            a_, _d = fm_asc_desc(pt)
            P.tp.put(u"1:{:,}".format(int(T.den)), r[0], r[3] + 1.2 + a_, pt, False, "L", 0.0, None, "scale",
                     GRID_INK["ink"], (), "sb_%s" % did)
    BK_STAT["drawings"] += 1
    BK_STAT["scales"].append(u"%s %s" % (did, (u"1:%d" % T.den) if T.den else (u"x%.2f" % T.k)))
    return placed


def bk_insets(P, S):
    for ins in S["insets"]:
        a, b = S["placed"].get(ins.get("parent")), S["placed"].get(ins.get("child"))
        wi = ins.get("window")
        if a and b and wi and len(wi) == 4:
            p0 = a["T"].pt(wi[0], wi[3])
            p1 = a["T"].pt(wi[2], wi[1])
            bk_rect(P, (min(p0[0], p1[0]), min(p0[1], p1[1]), max(p0[0], p1[0]), max(p0[1], p1[1])), None,
                    GRID_INK["ink"], 0.5)
            bk_rect(P, b["rect"], None, GRID_INK["ink"], 0.5)


# ---- right column -------------------------------------------------------------------------------------------------
def bk_side_item(P, it, x, y, w, ybot):
    """one attached thing in the right column at (x, y): returns the height used"""
    h = max(4.0, ybot - y)
    k = it.get("kind")
    if k == "text":
        role = it.get("role") or "note"
        if role not in GRID_ROLE_PT:
            role = "note"
        hh, _s = st_para(P, it.get("string", u""), x, y, w, h, role, justify=role != "heading", page=P.pid)
        return hh
    if k == "legend":
        b = pl_legend(P, it, x, y, w, h, 2)
        return b[3] - b[1]
    if k == "list":
        b = pl_list(P, it, x, y, w, h)
        return b[3] - b[1]
    return 0.0


# ---- the page -----------------------------------------------------------------------------------------------------
BK_STAT = dict(drawings=0, scales=[], pages=[])




# ---- frames (v31, G6-1) -------------------------------------------------------------------------------------------
def _bk_frames(spec, pid):
    """the page plan's frames -> [dict(key, pats, mm box, opts)]; overlapping frames = WARNING "frames" (a plan error;
    a frame marked over=True may sit on another, e.g. p03's list over the axo's empty corner)"""
    out = []
    for f in spec.get("frames") or []:
        pats = [f["ids"]] if isinstance(f["ids"], str) else list(f["ids"])
        out.append(dict(f, pats=pats, key=f.get("key") or pats[0], mm=bk_pct(f["box"])))
    for i, a in enumerate(out):
        for b in out[i + 1:]:
            if a.get("over") or b.get("over"):
                continue
            ox = min(a["mm"][2], b["mm"][2]) - max(a["mm"][0], b["mm"][0])
            oy = min(a["mm"][3], b["mm"][3]) - max(a["mm"][1], b["mm"][1])
            if ox > 0.5 and oy > 0.5:
                wn_warn(pid, "frames", u"frames %s and %s overlap %.0f x %.0f mm (page plan)" % (a["key"], b["key"],
                                                                                              ox, oy))
    return out


def _bk_pool(S):
    """every placeable item of the page, in export order: (id, kind, item); kind drawing | keymap | text | legend |
    list | photo"""
    out = [(d, "drawing", S["draw"][d]) for d in sorted(S["draw"], key=lambda d: (S["draw"][d].get("priority", 5), d))]
    out += [(k.get("id"), "keymap", k) for k in S["keymaps"]]
    heads = set(id(h) for a in S["att"].values() for h in a["head"])      # set over their drawing by bk_place
    out += [(t.get("id"), "text", t) for t in S["texts"] if t is not S.get("intro") and id(t) not in heads]
    out += [(it.get("id"), k, it) for k in ("legend", "list", "photo") for it in S[k + "s"]]
    return out


def _bk_match(S, frames):
    """each frame's items in pattern order (first frame wins); returns the set of matched item object ids"""
    pool = _bk_pool(S)
    got = set()
    for F in frames:
        F["items"] = []
        for p in F["pats"]:
            for iid, k, it in pool:
                if id(it) in got or iid is None:
                    continue
                if (fnmatch.fnmatchcase(iid, p) if _bk_pat(p) else iid == p):
                    got.add(id(it))
                    F["items"].append((iid, k, it))
    return got


def _bk_fit(S, did, w, h, pid):
    """the uniform size of drawing did in a w x h mm box: den (maps, sections: the largest list scale that fits) or
    factor (diagrams, charts, key maps: the largest that fits, <= BK_MM_MAX); reserves its heading / levels / band"""
    D = S["draw"].get(did) or ix_get(did)
    rw, rh = _bk_res(S, did) if did in S["draw"] else (0.0, 0.0)
    if D.get("units") == "m" and D.get("role") != "keymap":
        return sc_pick(D, max(1.0, w - rw), max(1.0, h - rh), page=pid)
    return sc_factor(D, max(1.0, w - rw), max(1.0, h - rh), pid)


def _bk_boxes(F, n, items=None):
    """a frame's box (less its "foot") cut into n cells: side by side (split "row") or stacked ("col"); default along
    its longer side; cells sized by the drawings' extents along the split (so one-scale cuts of different lengths each
    get their share), gap = the frame's "gap" in mm (default BK_GAP)"""
    b = F["mm"]
    if F.get("foot"):                              # room kept under the drawings for their notes (% of the page)
        b = (b[0], b[1], b[2], max(b[1] + 5.0, b[3] - float(F["foot"]) * BK_PCT[1]))
    if n <= 1:
        return [b]
    sp = F.get("split") or ("row" if (b[2] - b[0]) >= (b[3] - b[1]) else "col")
    wts = None
    if items and len(items) == n:
        try:
            wts = [max(1e-6, _sc_ext(it)[0 if sp == "row" else 1]) for _i, _k, it in items]
        except Exception:
            wts = None
    return lay_split(b, n, float(F.get("gap", BK_GAP)), vertical=(sp == "col"), weights=wts)


def _bk_same(S, frames, pid):
    """frames sharing a "same" key: one scale (the smallest print of their fits) / one factor (the smallest)"""
    val = {}
    for F in frames:
        k = F.get("same")
        if not k:
            continue
        ds = [(iid, kk, it) for iid, kk, it in F["items"] if kk in ("drawing", "keymap")]
        for (did, kk, _it), b in zip(ds, _bk_boxes(F, len(ds), ds)):     # the same cells as _bk_frame_draw
            if kk != "drawing" or _bk_parent(S, did):
                continue
            s = _bk_fit(S, did, b[2] - b[0], b[3] - b[1], pid)
            m = S["draw"][did].get("units") == "m"
            cur = val.get(k)
            if cur is None:
                val[k] = (m, s)
            elif cur[0] != m:
                wn_warn(pid, "scale", u"frames \"%s\" mix maps and diagrams: %s keeps its own size" % (k, did))
            else:
                val[k] = (m, max(cur[1], s) if m else min(cur[1], s))
    return val


class _BkTgt(object):
    """a place where notes stack: a box and its running y"""
    def __init__(self, key, box, y=None):
        self.key, self.box, self.y, self.over = key, box, box[1] if y is None else y, False


def _bk_put(P, tg, it):
    """one text / legend / list at the target's running y; past the box foot = one WARNING "overrun" per target"""
    x0, _y0, x1, y1 = tg.box
    if it.get("kind") == "photo":
        hh = _bk_photo_grid(P, [it], (x0, tg.y, x1, y1))
    else:
        hh = bk_side_item(P, it, x0, tg.y, x1 - x0, y1)
    tg.y += hh + BK_NOTE_GAP
    if tg.y > y1 + 0.5 and not tg.over:
        tg.over = True
        wn_warn(P.pid, "overrun", u"frame %s: its texts run %.0f mm past its foot (y %.0f mm)" % (tg.key, tg.y - y1, y1))
    return hh


def _bk_photo_grid(P, photos, box):
    """photos in a grid filling the box (proportions kept, never stretched); captions under each; -> height used"""
    if not photos:
        return 0.0
    import math as _m
    x0, y0, x1, y1 = box
    w, h = x1 - x0, max(8.0, y1 - y0)
    n = len(photos)
    cols = max(1, min(n, int(round(_m.sqrt(n * w / h))) or 1))
    rows = -(-n // cols)
    cw = (w - BK_GAP * (cols - 1)) / float(cols)
    ch = (h - BK_GAP * (rows - 1)) / float(rows)
    ybot = y0
    for i, ph in enumerate(photos):
        c, r = i % cols, i // cols
        cx, cy = x0 + c * (cw + BK_GAP), y0 + r * (ch + BK_GAP)
        cap = ph.get("caption")
        t = ix_text(cap, ph.get("_folder")) if cap else u""
        ch_img = ch - (6.0 if t else 0.0)
        bx = pl_photo(P, ph, cx, cy, cw, max(4.0, ch_img))
        yb = bx[3] if bx else cy
        if t:
            h2, _s = st_para(P, t, cx, yb + 0.8, cw, 5.2, "caption", page=P.pid)
            yb += h2 + 0.8
        ybot = max(ybot, yb)
    return ybot - y0


def _bk_frame_draw(P, S, F, same, tg_of, pid):
    """the drawings of one frame (see steps 3-4); returns [did]"""
    ds = [(iid, kk, it) for iid, kk, it in F["items"] if kk in ("drawing", "keymap")]
    out, bottom = [], F["mm"][1]
    al = (F.get("al") or "TL").upper()
    for (did, kk, it), b in zip(ds, _bk_boxes(F, len(ds), ds)):
        w, h = b[2] - b[0], b[3] - b[1]
        if kk == "keymap":
            f = sc_factor(it, w, h, pid)
            dw, dh = sc_size(it, f)
            ox = b[0] + {"C": (w - dw) / 2.0, "R": w - dw}.get(al[1:2], 0.0)
            oy = b[1] + {"M": (h - dh) / 2.0, "B": h - dh}.get(al[:1], 0.0)
            pl = pl_mm_drawing(P, it, ix_texts(it), ox, oy, dw, dh, "L")
            BK_STAT["drawings"] += 1
            bottom = max(bottom, pl["rect"][3])
            out.append(did)
            continue
        D = S["draw"][did]
        rw, rh = _bk_res(S, did)
        par = _bk_parent(S, did)
        if par and D.get("units") == "m":
            pp = S["placed"].get(par)
            if pp and pp["T"].den:
                s = sc_inset_den(pp["T"].den, D, max(1.0, w - rw), max(1.0, h - rh), pid)
            else:
                wn_warn(pid, "scale", u"inset %s placed before its parent %s (page plan order): own fit" % (did, par))
                s = _bk_fit(S, did, w, h, pid)
        elif F.get("same") in same and same[F["same"]][0] == (D.get("units") == "m"):
            s = same[F["same"]][1]
        else:
            s = _bk_fit(S, did, w, h, pid)
        dw, dh = sc_size(D, s)
        tw, th = dw + rw, dh + rh
        ox = b[0] + {"C": (w - tw) / 2.0, "R": w - tw}.get(al[1:2], 0.0)
        oy = b[1] + {"M": (h - th) / 2.0, "B": h - th}.get(al[:1], 0.0)
        side = TpSideList(u"%s %s" % (pid, did))
        if F.get("noscale"):                       # the drawing's own bar is its scale (p19: no orphan "1:n")
            S.setdefault("noscale", set()).add(did)
        pl = bk_place(P, S, did, s, ox, oy, side)
        yb = pl["rect"][3] + (BK_SCALE_H if (pl["T"].den or D.get("north_deg") is not None) else 0.0)
        bottom = max(bottom, yb)
        out.append(did)
        if side.entries:                           # labels that fell back to numbers: their rows with the notes
            tg = tg_of(F, did)
            tg.y += pl_side_rows(P, side, tg.box[0], tg.y, tg.box[2] - tg.box[0], max(4.0, tg.box[3] - tg.y)) + \
                BK_NOTE_GAP
    return out, bottom


def bk_content_page(doc, spec, n, lines):
    """one content page from its frames (see the part notes)"""
    pid = spec["pid"]
    S = bk_items(pid)
    S["placed"] = {}
    bk_attach(S)
    P = bk_page(doc, pid, n)
    intro = S["intro"].get("string") if S["intro"] else spec.get("intro")
    part = spec.get("part")
    bk_band(P, (u"%s  %s" % (part, PARTS.get(part, u""))).upper() if part else None, spec["title"], intro)
    frames = _bk_frames(spec, pid)
    framed = _bk_match(S, frames)
    same = _bk_same(S, frames, pid)
    tg = {}
    for F in frames:
        tg[F["key"]] = _BkTgt(F["key"], F["mm"])
    side_key = spec.get("side")
    if side_key not in tg:
        wn_warn(pid, "frames", u"the page plan names no side frame (%r): unlisted items go under the last frame"
                % side_key)
        side_key = frames[-1]["key"] if frames else None
    if side_key is None:
        tg[None] = _BkTgt(None, GRID_AREA)

    def tg_of(F, did=None):
        """where a drawing's notes go: its frame's "note" frame, else under it in its own frame, else the side"""
        k = F.get("note")
        if k in tg:
            return tg[k]
        t = tg[F["key"]]
        if t.box[3] - t.y >= 8.0:
            return t
        return tg[side_key]
    owner_f = {}
    n_placed = 0
    for F in frames:
        if not F["items"]:
            if not F.get("opt"):
                wn_warn(pid, "missing", u"frame %s: nothing exported for %s (its script not run, or the id changed)"
                        % (F["key"], u", ".join(F["pats"])))
            continue
        ds, bottom = _bk_frame_draw(P, S, F, same, tg_of, pid)
        for d in ds:
            owner_f[d] = F
        if ds:
            tg[F["key"]].y = bottom + BK_NOTE_GAP
        photos = [it for _i, kk, it in F["items"] if kk == "photo"]
        if photos:
            t = tg[F["key"]]
            t.y += _bk_photo_grid(P, photos, (t.box[0], t.y, t.box[2], t.box[3])) + BK_NOTE_GAP
        for _i, kk, it in F["items"]:
            if kk in ("text", "legend", "list"):
                _bk_put(P, tg[F["key"]], it)
        n_placed += len(F["items"])
    bk_insets(P, S)
    # a placed drawing's attached items that no frame names: with their drawing
    n_att = 0
    for did, F in owner_f.items():
        for it in S["att"].get(did, {}).get("side", []):
            if id(it) not in framed:
                framed.add(id(it))
                _bk_put(P, tg_of(F, did), it)
                n_att += 1
    # everything else: unlisted -> the side frame, WARNING (never lost)
    unl = [(iid, kk, it) for iid, kk, it in _bk_pool(S) if id(it) not in framed]
    for iid, kk, it in sorted(unl, key=lambda r: u"%s" % r[0]):
        wn_warn(pid, "unlisted", u"%s %s is in no frame of the page plan: set in the side frame %s" % (kk, iid, side_key))
        t = tg[side_key]
        if kk in ("drawing", "keymap"):
            Fx = dict(key=u"side %s" % iid, mm=(t.box[0], t.y, t.box[2], max(t.y + 10.0, t.box[3])),
                      items=[(iid, kk, it)])
            _ds, bottom = _bk_frame_draw(P, S, Fx, {}, lambda F_, d_=None: t, pid)
            t.y = bottom + BK_NOTE_GAP
            if t.y > t.box[3] + 0.5:
                wn_warn(pid, "overrun", u"side frame %s: %s runs past its foot" % (side_key, iid))
        else:
            _bk_put(P, t, it)
    bk_pageno(P, n)
    ck_page(P)
    bk_finish(P)
    g = BK_GRP.get(pid, dict(kinds=set(), elements=set(), untagged=0))
    lines.append(u"page %s frames=%d placed=%d unlisted=%d (attached notes %d)" % (pid, len(frames), n_placed,
                                                                                len(unl), n_att))
    if "wp_groups_log" in globals():                # S2's writer counts what it actually wrote
        lines.append(wp_groups_log(pid))
    else:
        lines.append(u"groups %s kinds=%d elements=%d untagged=%d" % (pid, len(g["kinds"]), len(g["elements"]),
                                                                    g["untagged"]))
    lines.append(u"page %d %s: drawings %s" % (
        n, pid, u", ".join(u"%s %s" % (d, (u"1:%d" % p_["T"].den) if p_["T"].den else (u"x%.2f" % p_["T"].k))
                           for d, p_ in S["placed"].items())))
    return P
