# ---- 82_compose (round 5, S10, 2 Nov 2026; G-R5-1, G-R5-2, G-R5-12, D2, D7, D9, N3): one content page from its items --
# Change of approach (round 4 failed on text collisions and sheet crops): no sheet crop anywhere. A page = its plan row
# (80_plan) + every item its scripts exported for it. Steps per page:
#   1. sort the page's items: drawings (the left area's rows, the right column, key maps), texts, legends, lists, level
#      columns, insets, photos; every unanchored text, legend, list and photo is ATTACHED to one drawing (its "drawing"
#      key, else the longest drawing id its own id starts with, else the one drawing of its group) or stays page-level
#   2. scales (bk_fit): rows of the left area get the LARGEST Bergama-list scale at which the rows still fit (each row
#      its own scale, or one scale for the page with "common": merged pages N3 1:500); then the leftover height goes to
#      the scale-free diagrams (charts, key maps), and what is still left is spread evenly between the rows (no empty
#      band at the foot, D2); insets take >= 2 x their parent's scale
#   3. draw: each cell = heading over the drawing, the drawing (30_render), its north arrow (plans: from north_deg,
#      counter-clockwise from page-up, the key-map module's convention), its level markers (beside it, U04), its
#      in-drawing labels (50_place: anchor, rings, side list, smaller), its scale bar or "1:den" under it (the scale the
#      booklet picked: S7 stripped the old printed scales); the window of an inset drawn on its parent
#   4. right column (G-R5-2: legend, lists, key map, short text beside the drawings): key maps on top, then each row's
#      attached texts / legends / lists / side-list rows starting level with the row's top (U35: belongs to its
#      drawing), then the right-column drawings, then page-level texts, then photos in a strip
#   5. page number; layout check (70_check); every text drawn last (40_set)
# Nothing here raises on layout: every misfit is a WARNING (one run collects all; Aras 1 Nov 17:11).
BK_GAP = 4.0               # mm between cells / rows / right-column blocks (grid gutter)
BK_HEAD_H = 4.5            # heading band over a drawing
BK_SCALE_H = 5.5           # scale bar / "1:den" band under a true-scale drawing
BK_LEVEL_W = 24.0          # level markers + "+43.71 Q500" beside a section (3 gap + 9 marker + 12 label)
BK_KM_H = 72.0             # the most height a key map takes at the top of the right column
BK_PHOTO_H = 30.0          # photo strip height in the right column
BK_NORTH_MM = 7.0


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


def bk_cells(S, row, pid):
    out = []
    names = sorted(S["draw"], key=lambda d: (S["draw"][d].get("priority", 5), d))
    for p in row:
        hit = [d for d in names if fnmatch.fnmatchcase(d, p) and d not in S["used"]] if _bk_pat(p) else \
            ([p] if p in S["draw"] and p not in S["used"] else [])
        if not hit and not _bk_pat(p):
            wn_warn(pid, "missing", u"drawing %s not exported (its script not run, or failed): left out" % p)
        for d in hit:
            S["used"].add(d)
            out.append(d)
    return out


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
    rh = (BK_HEAD_H if att.get("head") else 0.0) + (BK_SCALE_H if D.get("units") == "m" else 0.0)
    return rw, rh


def _bk_inset_den(D, parent_den, w, h):
    al = [d for d in _sc_allowed(D, inset=True) if d * BK_INSET_ZOOM <= parent_den + 1e-6]
    if not al:
        return None
    for den in al:
        dw, dh = sc_size(D, den)
        if dw <= w + 1e-6 and dh <= h + 1e-6:
            return den
    return al[-1]


def bk_row_eval(S, cells, W, den, hcap):
    """the row's cells at den (true-scale cells) and fitted factors (scale-free cells, not taller than the true-scale
    part, or hcap when the row has none): dict(fit, w, h, cells=[(did, s, w, h)])"""
    res, used_w, mh = {}, 0.0, 0.0
    m = [d for d in cells if S["draw"][d].get("units") == "m" and not _bk_parent(S, d)]
    for d in m:
        rw, rh = _bk_res(S, d)
        dw, dh = sc_size(S["draw"][d], den)
        res[d] = (den, dw + rw, dh + rh)
        used_w += dw + rw
        mh = max(mh, dh + rh)
    for d in cells:
        par = _bk_parent(S, d)
        if par and S["draw"][d].get("units") == "m":
            pden = res.get(par, (den,))[0] or den
            rw, rh = _bk_res(S, d)
            cd = _bk_inset_den(S["draw"][d], pden or 1000, W * 0.45, (mh or hcap) - rh)
            if cd:
                dw, dh = sc_size(S["draw"][d], cd)
                res[d] = (cd, dw + rw, dh + rh)
                used_w += dw + rw
                mh = max(mh, dh + rh)
    mm = [d for d in cells if d not in res]
    gaps = BK_GAP * (len(cells) - 1)
    hc = mh if (m and mh > 0) else hcap
    if mm:
        avail = max(1.0, W - used_w - gaps)
        fs = []
        for d in mm:
            D = S["draw"][d]
            ew, eh = _sc_ext(D)
            rw, rh = _bk_res(S, d)
            lo, hi = (D.get("fit") or (0.5, 2.0))[:2]
            hi = max(float(hi), BK_MM_MAX)                # v30.3: diagrams grow into the room they have
            fs.append([d, min(float(hi), max(0.0, hc - rh) / eh), ew, eh, rw, rh, float(lo)])
        tw = sum(f[1] * f[2] + f[4] for f in fs)
        if tw > avail:
            k = avail / tw
            for f in fs:
                f[1] *= k
        for d, f, ew, eh, rw, rh, lo in fs:
            res[d] = (f, f * ew + rw, f * eh + rh)
    w = sum(res[d][1] for d in cells) + gaps
    h = max([res[d][2] for d in cells] or [0.0])
    fit = w <= W + 1e-6
    return dict(fit=fit, w=w, h=h, den=den, cells=[(d,) + res[d] for d in cells], mm_only=not m)


def bk_fit(S, rows, W, H, common, pid):
    """rows -> [eval] (see step 2)"""
    n = len(rows)
    if not n:
        return []
    gaps = BK_GAP * (n - 1)

    def allowed(cells):
        if S.get("scales"):                          # v30.3: the page plan's own scales (p22: 1:1,000 or 1:1,500)
            return sorted(int(v) for v in S["scales"])
        al = None
        for d in cells:
            D = S["draw"][d]
            if D.get("units") == "m" and not _bk_parent(S, d):
                a_ = set(_sc_allowed(D))
                al = a_ if al is None else (al & a_)
        return sorted(al) if al is not None else [None]
    mm_min = {}
    for i, r in enumerate(rows):
        if allowed(r) == [None]:
            e = bk_row_eval(S, r, W, None, H)
            lo = min([(S["draw"][d].get("fit") or (0.5, 2.0))[0] for d in r] or [0.5])
            mm_min[i] = min(e["h"], max(12.0, e["h"] * lo))
    if common:
        al = None
        for r in rows:
            a_ = allowed(r)
            if a_ != [None]:
                al = set(a_) if al is None else (al & set(a_))
        al = [None] if al is None else sorted(al)
        if not al:
            wn_warn(pid, "scale", u"the page's drawings share no scale: each row takes its own")
            common = False
        else:
            pick = None
            for den in al:
                ev = [bk_row_eval(S, r, W, den, H) if i not in mm_min else None for i, r in enumerate(rows)]
                tot = sum(e["h"] for e in ev if e) + sum(mm_min.values()) + gaps
                if all(e["fit"] for e in ev if e) and tot <= H + 1e-6:
                    pick = den
                    break
            if pick is None:
                pick = al[-1]
                wn_warn(pid, "scale", u"rows do not fit %.0f x %.0f mm at any common scale; set at 1:%s" % (
                    W, H, pick))
            cur = [bk_row_eval(S, r, W, pick, H) if i not in mm_min else None for i, r in enumerate(rows)]
    if not common:
        cand = [allowed(r) for r in rows]
        idx = [len(c) - 1 for c in cand]
        cur = [bk_row_eval(S, r, W, cand[i][idx[i]], H) if i not in mm_min else None for i, r in enumerate(rows)]
        for i, e in enumerate(cur):
            if e and not e["fit"]:
                wn_warn(pid, "scale", u"row %d (%s) is %.0f mm wide at its smallest scale 1:%s, %.0f mm free" % (
                    i + 1, u", ".join(rows[i]), e["w"], e["den"], W))
        while True:
            tot = sum(e["h"] for e in cur if e) + sum(mm_min.values()) + gaps
            best = None
            for i, r in enumerate(rows):
                if cur[i] is None or idx[i] == 0:
                    continue
                e2 = bk_row_eval(S, r, W, cand[i][idx[i] - 1], H)
                if e2["fit"] and tot - cur[i]["h"] + e2["h"] <= H + 1e-6:
                    gain = e2["w"] * e2["h"] - cur[i]["w"] * cur[i]["h"]
                    if best is None or gain > best[0]:
                        best = (gain, i, e2)
            if best is None:
                break
            idx[best[1]] -= 1
            cur[best[1]] = best[2]
    tot_m = sum(e["h"] for e in cur if e)
    if tot_m + sum(mm_min.values()) + gaps > H + 1e-6:
        wn_warn(pid, "overrun", u"the drawing rows need %.0f mm, %.0f mm free: smallest scales used" % (
            tot_m + sum(mm_min.values()) + gaps, H))
    left = max(0.0, H - tot_m - gaps)
    mm_rows = [i for i in range(n) if cur[i] is None]
    while mm_rows:
        share = left / len(mm_rows)
        done = []
        for i in mm_rows:
            e = bk_row_eval(S, rows[i], W, None, share)
            if e["h"] < share - 0.5:
                cur[i] = e
                done.append(i)
        if not done:
            for i in mm_rows:
                cur[i] = bk_row_eval(S, rows[i], W, None, share)
            break
        for i in done:
            left -= cur[i]["h"]
            mm_rows.remove(i)
    return cur


# ---- drawing ------------------------------------------------------------------------------------------------------
def bk_north(P, rect, deg, did):
    """true-north arrow (arrow + N, no box, G-R4-9) inside the drawing's top-right corner; deg = north's turn from
    page-up, counter-clockwise (keymap.py north_items convention; UNVERIFIED against each script's own sign)"""
    import math as _m
    h = BK_NORTH_MM
    t = _m.radians(float(deg))
    ux, uy = -_m.sin(t), -_m.cos(t)               # page y down
    px, py = -uy, ux
    cx, cy = rect[2] - 6.0, rect[1] + 6.0 + h / 2.0
    fx, fy = cx - ux * h / 2.0, cy - uy * h / 2.0

    def R(a, b):
        return (fx + ux * b + px * a, fy + uy * b + py * a)
    ink = "2C2219"
    bk_line(P, [R(0.0, 0.0), R(0.0, 0.62 * h)], ink, 0.6)
    hw = 0.22 * h
    bk_poly(P, [R(0.0, h), R(-hw, 0.55 * h), R(0.0, 0.66 * h), R(hw, 0.55 * h)], ink, None, 0.1)
    tx, ty = R(0.0, h + 2.4)
    pt = 6.0
    P.tp.put(u"N", tx, ty, pt, True, "MC", 0.0, "north", "label", ink, (did,))
    P.tp.keep((cx - h / 2.0 - 1.0, cy - h / 2.0 - 4.0, cx + h / 2.0 + 1.0, cy + h / 2.0 + 1.0), "north", did)


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
    if D.get("north_deg") is not None and (T.den or D.get("dkind") in ("plan", "diagram")):
        bk_north(P, T.rect, D["north_deg"], did)
    if D.get("window_m"):                            # p10 windows: one size, framed (S9 §5: no frame in the drawing)
        bk_rect(P, T.rect, None, GRID_INK["ink"], 0.5)
    if not T.den:
        lo = (D.get("fit") or (0.5, 2.0))[0]
        if s < lo - 1e-3:
            wn_warn(P.pid, "scale", u"%s set at x%.2f, below its x%.2f minimum (row too full)" % (did, s, lo))
    for lc in att["levels"]:
        pl_levels(P, lc, placed, "R")
    bk_badges(P, placed)
    pl_labels(P, placed, side, roles=("label",))
    if T.den:
        r = T.rect
        if D.get("scale_bar"):
            pl_scalebar(P, placed, r[0], r[3] + 1.2)
        else:                                       # the drawing carries its own bar (S7 crops): the scale only
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


def bk_right_drawing(P, S, did, x, y, w, ybot):
    D = S["draw"][did]
    rw, rh = _bk_res(S, did)
    hmax = max(10.0, min(ybot - y, 110.0)) - rh
    if D.get("units") == "m":
        s = sc_pick(D, w - rw, hmax, page=P.pid)
    else:
        s = sc_factor(D, w - rw, hmax, P.pid, 2.0)    # v30.3: right-column diagrams keep the old x2 ceiling
    side = TpSideList(u"%s %s" % (P.pid, did))
    placed = bk_place(P, S, did, s, x, y, side)
    yy = placed["rect"][3] + (BK_SCALE_H if placed["T"].den else 0.0) + 1.5
    if side.entries:
        yy += pl_side_rows(P, side, x, yy, w, max(4.0, ybot - yy)) + 1.5
    for it in S["att"][did]["side"]:
        yy += bk_side_item(P, it, x, yy, w, ybot) + 1.5
    return yy - y


def bk_photos(P, photos, x, y, w, ybot):
    if not photos:
        return 0.0
    n = min(3, len(photos))
    cw = (w - BK_GAP * (n - 1)) / float(n)
    yy, hmax = y, 0.0
    for i, ph in enumerate(photos):
        c = i % n
        if c == 0 and i:
            yy += hmax + 1.5
            hmax = 0.0
        box = pl_photo(P, ph, x + c * (cw + BK_GAP), yy, cw, min(BK_PHOTO_H, max(8.0, ybot - yy - 6.0)))
        hh = (box[3] - yy) if box else 0.0
        cap = ph.get("caption")
        if cap:
            t = ix_text(cap, ph.get("_folder"))
            if t and t != cap:
                h2, _s = st_para(P, t, x + c * (cw + BK_GAP), yy + hh + 0.8, cw, 6.0, "caption", page=P.pid)
                hh += h2 + 0.8
        hmax = max(hmax, hh)
    return yy + hmax - y


# ---- the page -----------------------------------------------------------------------------------------------------
BK_STAT = dict(drawings=0, scales=[], pages=[])


def bk_content_page(doc, spec, n, lines):
    pid = spec["pid"]
    S = bk_items(pid)
    S["placed"] = {}
    S["scales"] = spec.get("scales")
    bk_attach(S)
    P = bk_page(doc, pid, n)
    L = lay_page(P, spec.get("share", BK_SHARE), 1)
    intro = S["intro"].get("string") if S["intro"] else spec.get("intro")
    bk_title(P, L, spec["title"], intro)
    rows = [c for c in (bk_cells(S, r, pid) for r in spec.get("rows") or []) if c]
    right = []
    for p in spec.get("right") or []:
        right += bk_cells(S, [p], pid)
    left_over = [d for d in sorted(S["draw"], key=lambda d: (S["draw"][d].get("priority", 5), d)) if d not in S["used"]]
    if left_over:
        lines.append(u"%s: not in the page plan, set in the right column: %s" % (pid, u", ".join(left_over)))
        right += left_over
    if not rows and not right and not S["keymaps"]:
        wn_warn(pid, "missing", u"no items exported for this page: its scripts were not run (page left with its title)")
    dr = L["draw"]
    W, H = dr[2] - dr[0], dr[3] - dr[1]
    ev = bk_fit(S, rows, W, H, spec.get("common"), pid)
    used = sum(e["h"] for e in ev) + BK_GAP * max(0, len(ev) - 1)
    extra = max(0.0, H - used) / float(len(ev) + 1) if ev else 0.0
    y = dr[1] + extra
    row_tops = []
    for i, (r, e) in enumerate(zip(rows, ev)):
        side = TpSideList(u"%s row %d" % (pid, i + 1))
        x = dr[0]
        row_tops.append((y, r, side))
        for did, s, cw, ch in e["cells"]:
            bk_place(P, S, did, s, x, y, side)
            x += cw + BK_GAP
        y += e["h"] + BK_GAP + extra
    bk_insets(P, S)
    # right column
    rx0, ry0, rx1, ry1 = L["right"]
    rw = rx1 - rx0
    cy = max(ry0, L["intro"][3] + 1.0)
    for km in S["keymaps"]:
        f = sc_factor(km, rw, min(BK_KM_H, max(10.0, ry1 - cy)), pid)
        dh = _sc_ext(km)[1] * f
        pl = pl_mm_drawing(P, km, ix_texts(km), rx0, cy, rw, dh, "L")
        cy = pl["rect"][3] + BK_GAP
    for top, r, side in row_tops:
        cy = max(cy, top)
        if side.entries:
            cy += pl_side_rows(P, side, rx0, cy, rw, max(4.0, ry1 - cy)) + 1.5
        for did in r:
            for it in S["att"][did]["side"]:
                cy += bk_side_item(P, it, rx0, cy, rw, ry1) + 1.5
        cy += 1.0
    for did in right:
        cy += bk_right_drawing(P, S, did, rx0, cy, rw, ry1) + BK_GAP
    for it in S["page"]:
        cy += bk_side_item(P, it, rx0, cy, rw, ry1) + 1.5
    cy += bk_photos(P, S["photos"], rx0, cy, rw, ry1)
    if cy > ry1 + 0.5:
        wn_warn(pid, "overrun", u"the right column runs %.0f mm past the foot: cut text or widen the column (share)"
                % (cy - ry1))
    bk_pageno(P, n)
    ck_page(P)
    bk_finish(P)
    lines.append(u"page %d %s: rows %d, right %d, key maps %d, drawings %s" % (
        n, pid, len(rows), len(right), len(S["keymaps"]),
        u", ".join(u"%s %s" % (d, (u"1:%d" % p_["T"].den) if p_["T"].den else (u"x%.2f" % p_["T"].k))
                   for d, p_ in S["placed"].items())))
    return P
