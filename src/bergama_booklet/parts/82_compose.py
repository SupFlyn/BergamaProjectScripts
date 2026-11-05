# ---- 82_compose (round 5 S10; round 6 S9 v31: G6-1 page frames, G6-7/G6-8, G6-9 log): one content page from its items -
# Round 7 (v33, BRIEF §3 L1-L3): a page is its FIXED FRAMES (80_plan: SON frames in mm + SON printed scales) + every
# item its scripts exported for it. NOTHING is fitted: step 3 below is now "scale = the table's den (m drawings) or
# factor f (mm drawings, default 1 = exported size); a drawing that does not fit its frame = WARNING "<pid> <did>
# frame", scale kept". The round 6 fitters (_bk_fit, _bk_same, _bk_justify, the frame clamp, extent-weighted cells)
# are deleted. Round 6 (PLAN §3, G6-1): a page is its FRAMES + every item its scripts exported for it. The v30 rows / right column / share are gone. Steps per page:
#   1. sort the page's items (bk_items) and attach every unanchored text, legend and list to one drawing (bk_attach:
#      its "drawing" key, else the longest drawing id its own id starts with, else the one drawing of its group)
#   2. match: each frame takes the items whose id matches one of its fnmatch patterns (first frame wins; drawings,
#      key maps, texts, legends, lists, photos alike)
#   3. scale (v33): every drawing at the page table's scale (den for maps / sections, f for diagrams, key maps at
#      their SON frame size), placed at its frame's top-left; heading, level column and the scale band ("1:den" +
#      north arrow, outside the drawing, G6-4) sit inside the frame; past the frame = WARNING, scale kept
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
    S = dict(items=its, draw={}, keymaps=[], anchored=[], texts=[], legends=[], lists=[], levels=[], insets=[], photos=[],
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
            a_ = it.get("anchor")
            if it.get("role") == "keymap":
                S["keymaps"].append(it)
            elif it.get("outside") and isinstance(a_, dict) and a_.get("drawing"):
                S["anchored"].append(it)                  # v33: a key map's north (S1 km_export_items): with its map
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
    att = dict((d, dict(head=[], side=[], levels=[], badge=None, sub=None)) for d in S["draw"])
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
        elif t.get("role") == "badge" and att[d]["badge"] is None:     # v32 box: the drawing's number disc
            att[d]["badge"] = t
        elif t.get("role") == "caption" and t.get("priority", 5) <= 1 and att[d]["sub"] is None:
            att[d]["sub"] = t                                           # v32 box: the subtitle under the title
        elif t.get("role") == "heading" and not att[d]["head"]:
            att[d]["head"].append(t)
        else:
            att[d]["side"].append(t)
    strs = set(u"%s" % t.get("string", u"") for t in S["items"] if t.get("kind") == "text")
    for d, a in att.items():                         # v32 box: a title given only as ix.drawing(title=) heads its box
        tt = S["draw"][d].get("title")
        if not a["head"] and isinstance(tt, str) and tt.strip() and tt not in strs:
            a["head"].append(dict(kind="text", role="heading", string=tt, id=u"%s_title" % d, priority=1))
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


def _bk_k(D, s):
    """page mm per drawing unit at s (den for "m" drawings, factor for "mm")"""
    return (1000.0 / float(s)) if D.get("units", "m") == "m" else float(s)


def _bk_res(S, did, s=None):
    """(extra width, extra height) round a drawing: level column (v32: measured at s, both columns), heading, scale
    band"""
    D = S["draw"][did]
    att = S["att"].get(did, {})
    rw = 0.0
    if att.get("levels"):
        if s is None:
            rw = BK_LEVEL_W
        else:
            k = _bk_k(D, s)
            rw = max(pl_levels_w(lc, k, float(D["extent"][3])) for lc in att["levels"])
    band = D.get("units") == "m" or (D.get("north_deg") is not None and D.get("role") != "keymap")
    rh = (BK_SCALE_H if band else 0.0)
    if s is not None:
        dw = sc_size(D, s)[0]
        rh += _bk_head_h(att, dw + rw) + (pl_band_need(D, _bk_k(D, s)) if _bk_is_band(D) else 0.0)
    else:
        rh += (BK_HEAD_H if att.get("head") or att.get("badge") else 0.0)
    return rw, rh


def _bk_is_band(D):
    """v32: a true-scale section sets its labels in a band above it (Aras's W1 box)"""
    return D.get("dkind") == "section" and D.get("units", "m") == "m" and not bk_design_den(D)


def _bk_head_h(att, w):
    """v32 box head: number disc + title row, then the subtitle (wrapped to the box width)"""
    h = BK_HEAD_H if (att.get("head") or att.get("badge")) else 0.0
    if att.get("sub"):
        h += st_fit(att["sub"].get("string", u""), max(20.0, w), None, "caption")[3] + 1.0
    return h


def bk_disc(P, cx, cy, r, fill):
    import fitz as _fz
    sh = P.page.new_shape()
    sh.draw_circle(_fz.Point(cx * BK_K, cy * BK_K), r * BK_K)
    sh.finish(color=None, fill=hex_rgb(fill), width=0)
    sh.commit()


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
    rw, rh = _bk_res(S, did, s)
    dw, dh = sc_size(D, s)
    yy = y
    W = max(dw + rw, 30.0)
    if att["head"] or att.get("badge"):                # v32 box head (Aras's W1 box): disc, title
        hx = x
        if att.get("badge"):
            r_ = 1.8
            bk_disc(P, x + r_, y + r_ + 0.2, r_, GRID_INK["accent"])
            P.tp.keep((x, y, x + 2 * r_, y + 2 * r_ + 0.4), "marker", u"disc %s" % did)
            bpt = 5.0
            P.tp.put(att["badge"].get("string", u""), x + r_, y + r_ + 0.2, bpt, True, "MC", 0.0,
                     att["badge"].get("id"), "badge", "FFFFFF", ("marker",))
            hx += 2 * r_ + 1.2
        if att["head"]:
            st_para(P, att["head"][0].get("string", u""), hx, y, W - (hx - x), BK_HEAD_H - 0.6, "heading",
                    justify=False, page=P.pid)
        yy += BK_HEAD_H
    if att.get("sub"):
        hh, _s2 = st_para(P, att["sub"].get("string", u""), x, yy, W, None, "caption", page=P.pid)
        yy += hh + 1.0
    if _bk_is_band(D):                                 # the label band sits between the head and the drawing
        yy += pl_band_need(D, _bk_k(D, s))
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
        if _bk_is_band(D):
            pl_band(P, placed)
        else:
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
    """v33: the page plan's frames as given in mm (SON, never clamped or grown) -> [dict(key, pats, mm, opts)]; a frame
    past the 14 / 12 mm margins = WARNING "<key> edge" (SON puts it there, F9 / F16: kept); overlapping frames =
    WARNING "frames" (a plan error; over=True may sit on another); log "frame <pid> <key> x,y,w,h" per frame"""
    out = []
    ml, mt, mr, mb = GRID_ML, GRID_MT, GRID_PAGE[0] - GRID_MR, GRID_PAGE[1] - GRID_MB
    for f in spec.get("frames") or []:
        pats = [f["ids"]] if isinstance(f["ids"], str) else list(f["ids"])
        m_ = tuple(f["mm"])
        F_ = dict(f, pats=pats, key=f.get("key") or pats[0], mm=m_, mm0=m_)
        out.append(F_)
        BK_PAGENO_LOG.append(u"frame %s %s %.1f,%.1f,%.1f,%.1f" % (pid, F_["key"], m_[0], m_[1], m_[2] - m_[0],
                                                                    m_[3] - m_[1]))
    # v34: SON frames give order and arrangement only (bk_pack); the v33 edge / overlap warnings on them are gone
    return out


def _bk_pool(S):
    """every placeable item of the page, in export order: (id, kind, item); kind drawing | keymap | text | legend |
    list | photo"""
    out = [(d, "drawing", S["draw"][d]) for d in sorted(S["draw"], key=lambda d: (S["draw"][d].get("priority", 5), d))]
    out += [(k.get("id"), "keymap", k) for k in S["keymaps"]]
    heads = set(id(h) for a in S["att"].values() for h in a["head"] + [a.get("badge"), a.get("sub")] if h)
    out += [(t.get("id"), "text", t) for t in S["texts"] if t is not S.get("intro") and id(t) not in heads]
    out += [(it.get("id"), k, it) for k in ("legend", "list", "photo") for it in S[k + "s"]]
    return out


def _bk_match(S, frames, skip=()):
    """each frame's items in pattern order (first frame wins); returns the set of matched item object ids. v33: ids
    matching a page's skip pattern (SON has no block for them, D4 / F12) are left out with a log line "skip <page> <kind> <id>" """
    pool = _bk_pool(S)
    got = set()
    for iid, k, it in pool:
        if iid is not None and any(fnmatch.fnmatchcase(iid, p) for p in skip):
            got.add(id(it))
            BK_PAGENO_LOG.append(u"skip %s %s %s (SON has no block for it)" % (S.get("pid", u"?"), k, iid))
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


BK_FIT_TOL = 1.5          # mm: SON frames are ink boxes measured ±0.5-2 mm (H4 §0); a drawing past its frame by more
#                           than this = WARNING "<did> frame" (scale kept, never refitted)


def _bk_den(S, F, did, D, pid, quiet=False):
    """v33 (L1): the ONE scale of a drawing, read, never picked: "m" drawings -> the frame's den (int, or dict id ->
    den), else the producer's single fixed scale (scale_pref of one value, then its "sheet scale 1:N", then board_den /
    scale_den), each logged with its source; "mm" drawings -> the frame's factor f (1.0 = the exported size)"""
    if D.get("units", "m") != "m":
        return float(F.get("f") or 1.0), u"size"
    d_ = F.get("den")
    if isinstance(d_, dict):
        d_ = d_.get(did)
    if d_:
        return int(d_), u"table"
    sp = [int(v) for v in (D.get("scale_pref") or [])]
    if len(sp) == 1:
        return sp[0], u"script"
    for k_, v_ in ((u"sheet", bk_design_den(D)), (u"board", D.get("board_den")), (u"script", D.get("scale_den"))):
        if v_:
            return int(v_), k_
    if quiet:
        return 1000, u"none"
    wn_warn(pid, u"%s scale" % did, u"no SON scale in the page table and no fixed scale from its script%s: set at "
            u"1:1,000 (put its SON scale in 80_plan)" % ((u" (it offers 1:%s)" % u", 1:".join(str(v) for v in sp))
                                                       if sp else u""))
    return 1000, u"none"


class _BkTgt(object):
    """a place where notes stack: a box and its running y"""
    def __init__(self, key, box, y=None):
        self.key, self.box, self.y, self.over = key, box, box[1] if y is None else y, False


BK_FLOW_COL = 64.0                 # v32.4: a notes frame at least 2 x this wide flows its notes in columns


def _bk_est_h(P, it, w):
    """a quick height estimate of one note at width w (only to choose where a column breaks)"""
    k = it.get("kind")
    if k == "legend":
        n_ = len(it.get("entries") or [])
        cols = max(1, min(2, int((w + 4.0) // 40.0) or 1))
        return 1.3 * (PL_SW["h"] + PL_SW["row_gap"] + 0.6) * (-(-n_ // cols)) + (5.0 if it.get("title") else 0.0)
    if k == "list":
        return 3.4 * len(it.get("items") or [])
    if k == "text":
        role = it.get("role") or "note"
        try:
            return st_fit(it.get("string", u""), w, None, role if role in GRID_ROLE_PT else "note", page=P.pid)[3]
        except Exception:
            return 6.0
    return 0.0


def _bk_put(P, tg, it):
    """one text / legend / list at the target's running y; past the box foot = one WARNING "overrun" per target.
    v32.4: in a frame at least 2 x BK_FLOW_COL wide the notes flow in columns (top to bottom, then the next column),
    so a stack of legends no longer runs past the page foot while the frame's width stays empty (p21)"""
    x0, _y0, x1, y1 = tg.box
    nc = int((x1 - x0 + 4.0) // BK_FLOW_COL) if it.get("kind") != "photo" else 1
    if it.get("kind") == "legend" and not getattr(tg, "col", 0) and (x1 - x0) > 4.0 * max(1.0, y1 - _y0):
        nc = 1                                     # v32.6: a legend in a band frame (4 x wider than tall) takes the
    if nc >= 2:                                    # frame's width in its own columns (in one 64 mm column it ran
        #                                            28 mm past the p19 foot)
        cw = (x1 - x0 - 4.0 * (nc - 1)) / float(nc)
        c = getattr(tg, "col", 0)
        top = getattr(tg, "ctop", tg.y)
        tg.ctop = top
        if c < nc - 1 and tg.y > top + 1e-6 and tg.y + _bk_est_h(P, it, cw) > y1 + 0.5:
            c += 1
            tg.y = top
        tg.col = c
        x0 = x0 + c * (cw + 4.0)
        x1 = x0 + cw
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


def _bk_misfit(pid, did, F, rect):
    """WARNING "<pid> <did> frame" with the overflow per side (L3: the scale is kept, the drawing is not moved)"""
    f = F["mm"]
    ov = (f[0] - rect[0], rect[2] - f[2], f[1] - rect[1], rect[3] - f[3])
    if max(ov) > BK_FIT_TOL:
        wn_warn(pid, u"%s frame" % did, u"at its scale it runs past its SON frame %s by L%.1f R%.1f T%.1f B%.1f mm "
                u"(scale kept)" % (F["key"], max(0.0, ov[0]), max(0.0, ov[1]), max(0.0, ov[2]), max(0.0, ov[3])))
        return False
    return True


def _bk_anchored(P, S, did, T):
    """v33 (S1 §4): a key map's north arrow ("<id>.north", outside=True) at its anchor = its lower-left in the key
    map's mm (y up), at size 1; its "<id>.head" text is placed with the key map (pl_rigid, anchor point)"""
    for N in S["anchored"]:
        a_ = N.get("anchor") or {}
        if a_.get("drawing") != did or not a_.get("point"):
            continue
        px, py = T.pt(a_["point"][0], a_["point"][1])
        nh = float(N["extent"][3]) - float(N["extent"][1])
        TN = BkT(N, 1.0, px, py - nh)
        pn = rd_drawing(P, N, TN)
        pl_rigid(P, pn, 1.0)
        S["placed"][N["id"]] = pn
        S["done_anch"].add(id(N))


def _bk_frame_draw(P, S, F, same, tg_of, pid):
    """v33: the drawings of one frame at the table's scale (see the part notes): one drawing at the frame's top-left
    (al), several (split "row" | "col") one after the other at their own size, F gap apart; nothing is fitted; a
    drawing past its frame = WARNING "<did> frame" (scale kept); logs "scale <pid> <did> 1:<n>" / "size <pid> <did>
    x<f>" and "keymap <pid> module"; returns ([did], bottom)"""
    ds = [(iid, kk, it) for iid, kk, it in F["items"] if kk in ("drawing", "keymap")]
    out, bottom = [], F["mm"][1]
    al = (F.get("al") or "TL").upper()
    x0, y0, x1, y1 = F["mm"]
    sp = F.get("split") or "row"
    gap = float(F.get("gap", BK_GAP))
    cx, cy = x0, y0                                  # running corner of a split frame
    for did, kk, it in ds:
        if kk == "keymap":                           # G7-3: exactly its SON frame (w x h mm from km_keymap), size 1
            dw, dh = sc_size(it, 1.0)
            T = BkT(it, 1.0, cx, cy)
            pl = pl_mm_drawing(P, it, T)
            S["placed"][did] = pl
            _bk_anchored(P, S, did, T)
            BK_STAT["drawings"] += 1
            BK_PAGENO_LOG.append(u"keymap %s module %s %.1fx%.1f mm at %.1f,%.1f" % (pid, did, dw, dh, cx, cy))
            bottom = max(bottom, pl["rect"][3])
            out.append(did)
            if sp == "col":
                cy += dh + gap
            else:
                cx += dw + gap
            continue
        D = S["draw"][did]
        s, src = _bk_den(S, F, did, D, pid)
        if F.get("k", 1.0) < 0.999:                  # v34: the page's one factor (bk_pack)
            s, src = _bk_ks(D, s, F["k"]), u"%s x%.2f page" % (src, F["k"])
        rw, rh = _bk_res(S, did, s)
        dw, dh = sc_size(D, s)
        tw, th = dw + rw, dh + rh
        if len(ds) == 1:
            ox = x0 + {"C": (x1 - x0 - tw) / 2.0, "R": x1 - x0 - tw}.get(al[1:2], 0.0)
            oy = y0 + {"M": (y1 - y0 - th) / 2.0, "B": y1 - y0 - th}.get(al[:1], 0.0)
        else:
            ox, oy = cx, cy
        side = TpSideList(u"%s %s" % (pid, did))
        if F.get("noscale"):                       # SON prints no ratio here / the drawing's own bar is its scale
            S.setdefault("noscale", set()).add(did)
        pl = bk_place(P, S, did, s, ox, oy, side)
        if pl["T"].den:
            BK_PAGENO_LOG.append(u"scale %s %s 1:%d (%s)" % (pid, did, pl["T"].den, src))
        else:
            BK_PAGENO_LOG.append(u"size %s %s x%.2f %.1fx%.1f mm" % (pid, did, pl["T"].k, dw, dh))
        S.setdefault("rec", {})[did] = dict(F=F, mm=F["mm"], s=s, rect=tuple(pl["rect"]))
        _bk_misfit(pid, did, F, (ox, oy, ox + tw, oy + th + (BK_SCALE_H if pl["T"].den else 0.0)))
        yb = pl["rect"][3] + (BK_SCALE_H if (pl["T"].den or D.get("north_deg") is not None) else 0.0)
        bottom = max(bottom, yb)
        out.append(did)
        if sp == "col":
            cy = oy + th + (BK_SCALE_H if pl["T"].den else 0.0) + gap
        else:
            cx = ox + tw + gap
        if side.entries:                           # labels that fell back to numbers: their rows with the notes
            tg = tg_of(F, did)
            tg.y += pl_side_rows(P, side, tg.box[0], tg.y, tg.box[2] - tg.box[0], max(4.0, tg.box[3] - tg.y)) + \
                BK_NOTE_GAP
    return out, bottom


def bk_check_page(P, S, frames, pid, before):
    """v33 invariants (H5 §4), log only: every placed drawing's scale = the table's, its frame unchanged, its rect not
    moved by the label pass (L6); one line "check <pid> drawings=<n> scale_ok=<n> frames_ok=<n> moved=<n>" """
    n = ok_s = ok_f = mv = 0
    for did, r in (S.get("rec") or {}).items():
        n += 1
        F = r["F"]
        want = F.get("den")
        want = (want.get(did) if isinstance(want, dict) else want)
        if want and F.get("k", 1.0) < 0.999:          # v34: packed page, the table's scale times the page factor
            want = _bk_ks(S["draw"].get(did, {}), want, F["k"])
        want = want or r["s"]
        if S["draw"].get(did, {}).get("units", "m") != "m":
            want = float(F.get("f") or 1.0) * F.get("k", 1.0)
        if abs(want - r["s"]) < 1e-6 or want == r["s"]:
            ok_s += 1
        else:
            wn_warn(pid, u"%s scale" % did, u"printed %s, table %s" % (r["s"], want))
        if tuple(F["mm"]) == tuple(r["mm"]):
            ok_f += 1
        else:
            wn_warn(pid, u"%s frame" % did, u"frame changed %s -> %s" % (r["mm"], F["mm"]))
        if before.get(did) != r["rect"]:
            mv += 1
            wn_warn(pid, u"%s moved" % did, u"the drawing moved during the label pass (L6)")
    BK_PAGENO_LOG.append(u"check %s drawings=%d scale_ok=%d frames_ok=%d moved=%d" % (pid, n, ok_s, ok_f, mv))


# ---- v32 labels (L1, LAYOUT_PLAN_booklet_places_all.md §3.2; Aras 4 Nov 19:17-19:25): after placing, the collision
# test runs and every text that hits something is placed again by the chain (bk_fix -> pl_chain: free spot round its
# point, short form, OUTSIDE the drawing with a leader line, number + key row). NO drawing is scaled down and NO text
# is shrunk to clear a hit; only hits left after that are WARNINGs, the texts printed. (v33: the round 6 page
# justification and scale picking that stood here are deleted, BRIEF L3.)


def bk_fix(P, rounds=3):
    """v32: the texts that hit something run the chain again (pl_chain; the later / movable one of each pair moves);
    returns the hits left"""
    for _r in range(rounds):
        if bk_late():                                     # v32.4: past the page budget, no more fix rounds
            break
        hits = P.tp.hits_now(True)
        movers, seen = [], set()
        for _k, a, b in hits:
            for t in ((b, a) if isinstance(b, dict) and "text" in b else (a,)):
                if isinstance(t, dict) and "text" in t and (t.get("extra") or {}).get("fx") and id(t) not in seen:
                    seen.add(id(t))
                    movers.append(t)
                    break
        if not movers:
            return hits
        for t in movers:
            fx = t["extra"]["fx"]
            if fx.get("tries", 0) >= 3:
                continue
            fx["tries"] = fx.get("tries", 0) + 1
            if P.tp.unput(t):
                pl_unleader(P, fx)
                pl_chain(P, fx, P.fx_side, first=False)
    return P.tp.hits_now(True)


def bk_own_hits(P):
    """v32.4: overlaps left INSIDE one drawing after the booklet moved what it could within that drawing (texts its
    script exported on top of each other): one WARNING per drawing naming the script, with the first pairs, so the
    rest is fixed where it is made (the page test also lists each pair)"""
    tp = P.tp
    by = {}
    for n, it in enumerate(tp.items):
        ex = it.get("extra") or {}
        g = u"%s" % (ex.get("dgrp") or (ex.get("fx") or {}).get("dgrp") or u"")
        if g.startswith(u"drw:"):
            by.setdefault(g[4:], []).append(it)
    for did, its in by.items():
        pairs = []
        for i, a in enumerate(its):
            for c in its[i + 1:]:
                if tp_hit(a["box"], c["box"], 0.0) and a.get("text") != c.get("text"):
                    pairs.append((a["text"], c["text"]))
        if pairs:
            sc_ = (BK_IX_OWNER.get(did) if "BK_IX_OWNER" in globals() else None) or did.split(u"_")[0]
            wn_warn(P.pid, "own", u"%s: %d text pairs still on top of each other inside it (its script %s set them so), e.g. %s"
                    % (did, len(pairs), sc_, u"; ".join(u"%r / %r" % (a[:30], b[:30]) for a, b in pairs[:3])))


def bk_content_page(doc, spec, n, lines):
    """one content page from its frames (see the part notes): compose, fix every hit by moving texts, check"""
    pid = spec["pid"]
    R = _bk_compose(doc, spec, n)
    P, S = R["P"], R["S"]
    st = pl_stat(P)
    bk_own_hits(P)                                        # v32.4: texts a script set on top of each other
    ck_page(P)                                            # the final test: every hit left = one WARNING line
    bk_finish(P)
    g = BK_GRP.get(pid, dict(kinds=set(), elements=set(), untagged=0))
    lines.append(u"page %s frames=%d placed=%d unlisted=%d (attached notes %d)" % (pid, len(R["frames"]),
                                                                                R["placed"], R["unl"], R["att"]))
    lines.append(u"layout %s drawings %d, labels %d (moved %d, short %d, leader %d, numbered %d), drawings made "
                 u"smaller 0, hits left %d (frames grown %d)" % (
                     pid, len(S["placed"]), st["labels"], st["moved"], st["short"], st["leader"], st["numbered"],
                     len(R["left"]), R["grown"]))
    if BK_PG["late"]:
        wn_warn(pid, "time", u"page past its %.0f s budget: %d texts set at their own spot without the search "
                u"(%.0f s)" % (BK_PAGE_BUDGET, BK_PG["late"], time.time() - BK_PG["t0"]))
    if "wp_groups_log" in globals():                # S2's writer counts what it actually wrote
        lines.append(wp_groups_log(pid))
    else:
        lines.append(u"groups %s kinds=%d elements=%d untagged=%d" % (pid, len(g["kinds"]), len(g["elements"]),
                                                                    g["untagged"]))
    lines.append(u"page %d %s: drawings %s" % (
        n, pid, u", ".join(u"%s %s" % (d, (u"1:%d" % p_["T"].den) if p_["T"].den else (u"x%.2f" % p_["T"].k))
                           for d, p_ in S["placed"].items())))
    return P


# ---- v34 MEASURE, THEN PACK (Aras 5 Nov 11:42 "change your approach"; decision card: measure first, then pack).
# v33 put every drawing at SON's printed scale into SON's measured frame and never shrank it: a drawing bigger than its
# frame ran onto its neighbours (p08 street cuts 394 mm in a 292 mm row). Now SON's frames give only the ORDER and the
# ARRANGEMENT (which blocks sit side by side, which stack): the frames are split into rows / columns where SON has a
# clear gap (guillotine cuts), each block is MEASURED at its scale (drawings + level columns + headings + scale band,
# then its texts at that width), and the page is laid out from those real sizes, so two blocks cannot overlap. If the
# page does not fit the area, every drawing on it gets the same factor k (< 1, the printed 1:n is the true one, e.g.
# 1:500 / 0.8 = 1:625); texts keep their size. Key maps keep size 1. Log "pack <pid> k=<k> blocks=<n> w x h mm".
BK_PACK_TOL = 3.0          # mm: SON frames are ink boxes ±2 mm; a cut between two groups may overlap this much


def _bk_ks(D, s, k):
    """the scale of a drawing on a page packed with factor k (den grows, mm factor shrinks)"""
    if D.get("units", "m") == "m":
        return int(round(float(s) / k))
    return float(s) * k


def _bk_leaf(P, S, F, pid, k):
    """(w, h) mm of one frame's content at page factor k: its drawings (split row / col, gap) then its texts"""
    sp = F.get("split") or "row"
    gap = float(F.get("gap", BK_GAP))
    ws, hs = [], []
    for did, kk, it in F["items"]:
        if kk == "keymap":
            w_, h_ = sc_size(it, 1.0)
        elif kk == "drawing":
            D = S["draw"][did]
            s = _bk_ks(D, _bk_den(S, F, did, D, pid, quiet=True)[0], k)
            rw, rh = _bk_res(S, did, s)
            dw, dh = sc_size(D, s)
            w_, h_ = dw + rw, dh + rh + (BK_SCALE_H if D.get("units", "m") == "m" else 0.0)
        else:
            continue
        ws.append(w_)
        hs.append(h_)
    if ws:
        dw_ = max(ws) if sp == "col" else sum(ws) + gap * (len(ws) - 1)
        dh_ = sum(hs) + gap * (len(hs) - 1) if sp == "col" else max(hs)
    else:
        dw_ = dh_ = 0.0
    son = F.get("mm0", F["mm"])
    texts = [it for _i, kk, it in F["items"] if kk in ("text", "legend", "list")]
    for did, kk, it in F["items"]:                   # a drawing's own notes go with it unless a note frame takes them
        if kk == "drawing" and not F.get("note"):
            texts += [x for x in S["att"].get(did, {}).get("side", [])]
    texts += F.get("_notes_in", [])                  # notes of drawings whose frame sends them here
    photos = [it for _i, kk, it in F["items"] if kk == "photo"]
    if ws:
        w = max(dw_, 50.0 if texts else 0.0)
    else:
        w = min(son[2] - son[0], GRID_AREA[2] - GRID_AREA[0])
    h = dh_
    if photos:
        h += (son[3] - son[1]) * (k if ws else 1.0)
    for it in texts:
        h += _bk_est_h(P, it, w) + BK_NOTE_GAP
    return w, max(h, 0.0 if (ws or texts or photos) else 12.0)     # an empty side frame keeps 12 mm for unlisted items


def _bk_cut(groups, ax):
    """split groups (lists of frames) where SON leaves a gap along axis ax (0 = x: side by side, 1 = y: stacked)"""
    bx = lambda g: (min(f["mm0"][ax] for f in g), max(f["mm0"][ax + 2] for f in g))
    gs = sorted(groups, key=lambda g: bx(g)[0])
    out, cur, end = [], [gs[0]], bx(gs[0])[1]
    for g in gs[1:]:
        a, b = bx(g)
        if a >= end - BK_PACK_TOL:
            out.append(cur)
            cur, end = [g], b
        else:
            cur.append(g)
            end = max(end, b)
    out.append(cur)
    return out


def _bk_tree(groups):
    """guillotine tree of SON's arrangement: ("v", [..]) stacked, ("h", [..]) side by side, or a leaf = [frames]"""
    if len(groups) == 1:
        return groups[0]
    for ax, kind in ((1, "v"), (0, "h")):
        parts = _bk_cut(groups, ax)
        if len(parts) > 1:
            return (kind, [_bk_tree(p) for p in parts])
    return ("v", sorted(groups, key=lambda g: min(f["mm0"][1] for f in g)))     # no clean cut: stack in SON order


def _bk_size(P, S, node, pid, k, sizes):
    if isinstance(node, list):                       # a leaf: its frames stacked (a frame SON sets "over" another)
        ws, h = [], 0.0
        for F in node:
            w_, h_ = _bk_leaf(P, S, F, pid, k)
            sizes[id(F)] = (w_, h_)
            ws.append(w_)
            h += h_ + (BK_GAP if h else 0.0)
        return max(ws), h
    kind, ch = node
    wh = [_bk_size(P, S, c, pid, k, sizes) for c in ch]
    g = BK_GAP * (len(wh) - 1)
    if kind == "h":
        return sum(w for w, _h in wh) + g, max(h for _w, h in wh)
    return max(w for w, _h in wh), sum(h for _w, h in wh) + g


def _bk_lay(node, x, y, sizes, wh_of):
    if isinstance(node, list):
        for F in node:
            w_, h_ = sizes[id(F)]
            F["mm"] = (x, y, x + w_, y + h_)
            y += h_ + BK_GAP
        return
    kind, ch = node
    for c in ch:
        _bk_lay(c, x, y, sizes, wh_of)
        w_, h_ = wh_of[id(c)]
        if kind == "h":
            x += w_ + BK_GAP
        else:
            y += h_ + BK_GAP


def spec_side(frames):
    """the page's side frame key, set by _bk_compose before packing (unlisted items land there)"""
    return BK_PACK_SIDE[0]


BK_PACK_SIDE = [None]


def bk_pack(P, S, frames, pid, top):
    """v34: lay the page out from measured sizes (see the notes above); sets every frame's mm and F["k"]"""
    byk = dict((F["key"], F) for F in frames)
    for F in frames:
        F["_notes_in"] = []
    for F in frames:
        if F.get("note") in byk:
            for did, kk, it in F["items"]:
                if kk == "drawing":
                    byk[F["note"]]["_notes_in"] += list(S["att"].get(did, {}).get("side", []))
    live = [F for F in frames if F["items"] or F["_notes_in"] or F.get("key") == spec_side(frames)]
    if not live:
        return 1.0
    over = [F for F in live if F.get("over")]
    groups = [[F] for F in live if not F.get("over")]
    for F in over:                                   # an "over" frame stacks under the frame it covers most
        def ov(g):
            a, b = F["mm0"], g[0]["mm0"]
            return max(0.0, min(a[2], b[2]) - max(a[0], b[0])) * max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
        (max(groups, key=ov) if groups else groups.append([]) or groups[-1]).append(F)
    tree = _bk_tree(groups)
    x0, x1, y1 = GRID_AREA[0], GRID_AREA[2], GRID_AREA[3]
    aw, ah = x1 - x0, y1 - top
    k = 1.0
    for _i in range(8):
        sizes = {}
        W, H = _bk_size(P, S, tree, pid, k, sizes)
        r = min(aw / W if W else 1.0, ah / H if H else 1.0)
        if r >= 0.999:
            break
        k = max(0.25, k * r * 0.99)
    wh_of = {}

    def rec(n):
        if isinstance(n, list):
            wh_of[id(n)] = (max(sizes[id(F)][0] for F in n),
                            sum(sizes[id(F)][1] for F in n) + BK_GAP * (len(n) - 1))
        else:
            for c in n[1]:
                rec(c)
            ws_ = [wh_of[id(c)] for c in n[1]]
            g = BK_GAP * (len(ws_) - 1)
            wh_of[id(n)] = ((sum(w for w, _h in ws_) + g, max(h for _w, h in ws_)) if n[0] == "h" else
                            (max(w for w, _h in ws_), sum(h for _w, h in ws_) + g))
    rec(tree)
    W, H = wh_of[id(tree)]
    if W > aw + 0.5 or H > ah + 0.5:
        wn_warn(pid, "pack", u"the page needs %.0f x %.0f mm at the smallest factor %.2f (area %.0f x %.0f mm)"
                % (W, H, k, aw, ah))
    _bk_lay(tree, x0, top, sizes, wh_of)
    for F in live:
        F["k"] = k
        m_ = F["mm"]
        BK_PAGENO_LOG.append(u"frame %s %s %.1f,%.1f,%.1f,%.1f (packed)" % (pid, F["key"], m_[0], m_[1],
                                                                          m_[2] - m_[0], m_[3] - m_[1]))
    BK_PAGENO_LOG.append(u"pack %s k=%.3f blocks=%d %.0fx%.0f mm" % (pid, k, len(live), W, H))
    if k < 0.999:
        wn_warn(pid, "pack", u"every drawing on the page at x%.2f of its SON scale so the page fits (true 1:n printed)"
                % k)
    return k


def _bk_compose(doc, spec, n):
    """one content page (see the part notes); returns dict(P, S, frames, left hits, counts)"""
    pid = spec["pid"]
    S = bk_items(pid)
    S["placed"], S["pid"] = {}, pid
    bk_attach(S)
    P = bk_page(doc, pid, n)
    P.fx_side = TpSideList(u"%s page key" % pid)
    pl_stat(P)
    intro = S["intro"].get("string") if S["intro"] else spec.get("intro")
    part = spec.get("part")
    rule_y = bk_band(P, bk_kicker(spec), spec["title"], intro)
    frames = _bk_frames(spec, pid)
    S["done_anch"] = set()                                # a key map's north is placed with its key map
    framed = _bk_match(S, frames, spec.get("skip") or ())
    BK_PACK_SIDE[0] = spec.get("side")
    bk_pack(P, S, frames, pid, max(GRID_AREA[1], float(rule_y or 0.0) + 4.0))   # v34: measure, then pack
    grown = 0                                             # v33: frames never grow (L3)
    same = {}
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
    bk_pageno(P, n, bk_footer(spec))
    before = dict((d, r["rect"]) for d, r in (S.get("rec") or {}).items())
    left = bk_fix(P)
    if P.fx_side.entries:                                 # texts the fix pass numbered: their key rows in the side frame
        t = tg[side_key]
        t.y += pl_side_rows(P, P.fx_side, t.box[0], t.y, t.box[2] - t.box[0], max(4.0, t.box[3] - t.y)) + BK_NOTE_GAP
        left = P.tp.hits_now(True)
    pl_draw_leaders(P)
    for d, pl_ in S["placed"].items():                    # the label pass never moves a drawing (L6)
        r_ = (S.get("rec") or {}).get(d)
        if r_ is not None:
            r_["rect"] = tuple(pl_["rect"])
    for it in S["anchored"]:
        if id(it) not in S["done_anch"]:
            wn_warn(pid, u"%s anchor" % it.get("id"), u"its key map %r is not on this page: not placed"
                    % (it.get("anchor") or {}).get("drawing"))
    bk_check_page(P, S, frames, pid, before)
    return dict(P=P, S=S, frames=frames, left=left, placed=n_placed, unl=len(unl), att=n_att, grown=grown)
