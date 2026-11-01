# ============================================================ v59 (round 4, G-R4-1): EVERY TEXT OF EVERY CROP CHECKED
# Aras 1 Nov: "overlapping texts are recurring situation please fix those everywhere once and for all". Every text the
# board draws ends in Board.items (Board.text / para / fit, site28_*, the page wrappers and the shape lists all land
# there), so the check reads the finished board: for each booklet crop (CROP_PANELS) one TextPage (common/
# text_place.py) of the crop's rectangle gets every text item that reaches into it, measured with the real Arial
# metrics (font_metrics.py) at the size the PDF writer prints it; texts the booklet drops (the crop's "drop"
# patterns) are left out. Collisions text-text (other groups), text-crop edge and text below 6 pt at the largest
# scale the booklet can print the crop (one full row) are collected for all crops, logged per page
# ("overlap <page> checked n, collisions k") and then RAISED at once (SbTextCollisions) before any sheet PDF or
# booklet crop is written: a board with a collision on a booklet page is never delivered.
# Text groups: the lines of one paragraph (Board.para) or of one open B.tgroup() are one group; two texts on the same
# baseline that follow each other within one word space, and lines of one left/centre-aligned stack (same x, same
# size, line spacing 1.2-2.4 x the capital height) are joined into one group (they are one word block).
# v59.1: plan01_key left out: an empty 0.5 mm strip the booklet does not print (the edge strip's heading under it
# reached into it and was reported)
SB_TP_PAGES = {"plan01": "p02", "site_readings": "p02", "edge_types": "p02",
               "sections_1": "p04", "sections_2": "p05", "edge_build": "p06", "movement": "p07",
               "walking_today": "p07", "driving_today": "p07", "mv_note_1": "p07", "mv_note_2": "p07",
               "mv_note_3": "p07", "street_sections": "p09", "heritage_loop": "p20"}
SB_TP_PAD = 0.6                                       # mm clear gap between texts (text_place default)
SB_TP_LOG = []
# v59 (round 4 closing, G-R4-1 keeps): the drawing areas no text may cover, registered while the pages draw (sb_keep):
# key maps, legends, section pictures, the stream at each cut, zoom insets, photos and map frames. Each holds the
# texts its own drawing set (its names, tags, numbers: items i0..i1 of the board) as allowed on it, so a place name on
# its map passes and a column text, caption or other block running over the drawing raises like text-text.
SB_KEEPS = []                                         # dict(lst, geom, kind, name, i0, i1, line); reset per layout


class SbTextCollisions(RuntimeError):
    pass


def sb_mark(B):
    """v59 (closing, G-R4-1): the index the next item of board B gets (the i0 of sb_keep); None on a dry run"""
    it = getattr(B, "items", None)
    return len(it) if isinstance(it, list) else None


def sb_keep(B, geom, name, kind="keep", i0=None, line=None):
    """v59 (closing, G-R4-1): one drawing area of board B no text may cover, for the page check: geom = a box (x0,
    y0, x1, y1) or a closed area [(x, y) ...] in board units (line=True: an open line). The texts B drew from item
    i0 (sb_mark taken before the drawing) up to this call are the drawing's own and may sit on it; i0 None = no text
    may (the stream at a cut). A dry run (no board items) registers nothing. Returns the keep's name."""
    it = getattr(B, "items", None)
    if not isinstance(it, list) or not geom:
        return None
    n = len(it)
    nm = u"%s#%d" % (name, len(SB_KEEPS))
    SB_KEEPS.append(dict(lst=it, geom=list(geom), kind=kind, name=nm, i0=n if i0 is None else int(i0), i1=n,
                         line=line))
    return nm


def _sb_keep_box(K):
    g = K["geom"]
    if len(g) == 4 and not hasattr(g[0], "__len__"):
        return tuple(g)
    return (min(p[0] for p in g), min(p[1] for p in g), max(p[0] for p in g), max(p[1] for p in g))


def _sb_tp_pt(it, k):
    """(pt, kind) the PDF writer prints a board text item at (_pdf_page: size = cap height on the page / _PDF_CAP)"""
    kd = kind_of(it[7])
    return it[3] * k / _PDF_CAP[kd] / FM_PT, kd


def _sb_tp_items(B, bb, k, drop):
    """[(text, x, y, pt, bold, align, deg, tg, drawing, index)] of the board's texts that reach into bb (board
    units); index = the item's place in B.items (closing: the keeps it may sit on, sb_keep)"""
    import re as _re
    pats = [_re.compile(d) for d in drop or ()]
    out = []
    for i_, it in enumerate(B.items):
        if it[0] != "text":
            continue
        txt = u"%s" % it[1]
        if not txt.strip() or any(p_.search(txt.strip()) for p_ in pats):
            continue
        x, y = it[2]
        h = it[3]
        reach = (2.0 + len(txt)) * h                   # a generous reach: the exact box is measured in the TextPage
        if x + reach < bb[0] or x - reach > bb[2] or y + reach < bb[1] or y - reach > bb[3]:
            continue
        pt, kd = _sb_tp_pt(it, k)
        deg = math.degrees(it[10] or 0.0)
        tg = it[13] if len(it) > 13 else None
        out.append([txt, x, y, pt, bool(it[8]), it[9] or "L", deg, tg, it[12], i_])
    return out


def _sb_tp_join(T, k):
    """join same-line runs and line stacks into one group (see the module notes); T items are edited in place"""
    par = {}

    def find(a):
        while par.get(a, a) != a:
            a = par[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            par[rb] = ra
    for i, t in enumerate(T):
        if t[7] is None:
            t[7] = "s%d" % i
    flat = sorted((i for i, t in enumerate(T) if abs(t[6]) < 0.5), key=lambda i: (round(T[i][2], 2), T[i][1]))
    for a, b in zip(flat, flat[1:]):                   # runs on one baseline
        A, Bt = T[a], T[b]
        if A[8] != Bt[8] or abs(A[2] - Bt[2]) > 0.05 * A[3] * FM_PT / k:
            continue
        xa1 = A[1] + (tw(A[0], A[3] * FM_PT * _PDF_CAP["sans"] / k, "sans", A[4]) if A[5] == "L" else 0.0)
        gap = Bt[1] - xa1
        sp = fm_width(u" ", max(A[3], Bt[3]), False) / k * 1.6
        if A[5] == "L" and Bt[5] == "L" and -0.05 * sp <= gap <= sp:
            union(A[7], Bt[7])
    by_x = {}
    for i, t in enumerate(T):                          # stacks of lines
        if abs(t[6]) < 0.5 and t[5] in ("L", "C", "R"):
            by_x.setdefault((t[8], t[5], round(t[1] * k * 10.0), round(t[3] * 4)), []).append(i)
    for key, L in by_x.items():
        L.sort(key=lambda i: -T[i][2])
        for a, b in zip(L, L[1:]):
            cap = T[a][3] * FM_PT * _PDF_CAP["sans"] / k     # capital height, board units
            d = T[a][2] - T[b][2]
            if 1.2 * cap <= d <= 2.4 * cap:
                union(T[a][7], T[b][7])
    for t in T:
        t[7] = find(t[7])


def _sb_tp_put(tp, t, k, allow=()):
    """register one text; a turned text as short chunks along its baseline (its true strip, not its bounding box);
    allow = the keeps it may sit on (closing: those of its own drawing)"""
    txt, x, y, pt, bold, align, deg, tg, _d = t[:9]
    if abs(deg) < 0.5 or len(txt) <= 4:
        tp.put(txt, x, y, pt, bold, align, deg, name=txt[:24], group=tg, emit=False, allow=allow)
        return
    a = math.radians(deg)
    full = fm_width(txt, pt, bold) / k
    x0 = {"L": 0.0, "C": -0.5, "MC": -0.5, "R": -1.0}.get(align, 0.0) * full
    s0 = 0.0
    for j in range(0, len(txt), 4):
        ch = txt[j:j + 4]
        if ch.strip():
            u = x0 + s0
            tp.put(ch, x + u * math.cos(a), y + u * math.sin(a), pt, bold, "L", deg, name=txt[:24], group=tg,
                   emit=False, allow=allow)
        s0 += fm_width(ch, pt, bold) / k


def sb_text_check(B):
    """the page check of every booklet crop (module notes); RAISES SbTextCollisions listing every collision"""
    del SB_TP_LOG[:]
    k = 1000.0 / PDF_SCALE                              # mm on the sheet per board unit
    bad, n_pages = [], 0
    for p in CROP_PANELS:
        page = SB_TP_PAGES.get(p["slug"])
        if page is None:
            continue
        bb = p["bb"]
        w_mm, h_mm = (bb[2] - bb[0]) * k, (bb[3] - bb[1]) * k
        if w_mm <= 0 or h_mm <= 0:
            continue
        sc = (p["bk_w"] / w_mm) if p.get("bk_w") else min(BK_AW / w_mm, BK_AH / h_mm)
        tp = TextPage(u"%s %s" % (page, p["slug"]), bb, y_down=False, min_pt=GRID_MIN_PT, pad=SB_TP_PAD,
                      scale=sc, unit_mm=k, log=SB_TP_LOG)
        # v59 (closing, G-R4-1): the drawing areas of this board that reach into the crop (sb_keep)
        ks_ = [K for K in SB_KEEPS if K["lst"] is B.items and tp_hit(_sb_keep_box(K), bb, 0.0)]
        for K in ks_:
            tp.keep(K["geom"], kind=K["kind"], name=K["name"], line=K["line"])
        T = _sb_tp_items(B, bb, k, p.get("drop"))
        _sb_tp_join(T, k)
        for t in T:
            # a text that only comes near the crop counts only when its box enters it
            if not tp_hit(tp._box(t[0], t[1], t[2], t[3], t[4], t[5], t[6]), bb, 0.0):
                continue
            try:
                _sb_tp_put(tp, t, k, tuple(K["name"] for K in ks_ if K["i0"] <= t[9] < K["i1"]))
            except TextError as ex:
                bad.append(u"%s %s: %s" % (page, p["slug"], ex))
        try:
            tp.check(False, SB_TP_LOG)
        except Exception as ex:
            bad.append(u"%s %s: check failed (%s)" % (page, p["slug"], ex))
            continue
        n_pages += 1
        hits = _sb_tp_hits(tp)
        for a, c in hits:
            bad.append(u"%s %s: %r hits %s" % (page, p["slug"], a["text"][:40], c))
    LOG.extend(SB_TP_LOG)
    if bad:
        LOG.append(u"FLAG overlap: %d collision(s) on the booklet crops (listed in the error)" % len(bad))
        raise SbTextCollisions(u"text collisions on the booklet pages (G-R4-1: the sheets are not written):\n  " +
                               u"\n  ".join(bad[:40]) + (u"\n  ... %d more" % (len(bad) - 40) if len(bad) > 40 else u""))
    return n_pages


def _sb_tp_hits(tp):
    """the collisions of a checked TextPage as (item, description of the other) pairs (same tests as check())"""
    out = []
    I = tp.items
    for i, a in enumerate(I):
        b = a["box"]
        # v59.2: a glyph's ink may reach up to 0.05 mm past the crop edge (invisible in print): Arial Bold's "V" starts
        # a hair left of its pen point, and "VISIBLE" set on the crop's left edge was reported "left by 0.00 mm"
        e_ = 0.05 / tp.unit_mm
        if not (tp.inner[0] - e_ <= b[0] and b[2] <= tp.inner[2] + e_ and
                tp.inner[1] - e_ <= b[1] and b[3] <= tp.inner[3] + e_):
            # v59.1: which edge and by how much (mm on the sheet), so the next fix needs no guessing
            u_ = tp.unit_mm
            ov_ = [(nm_, d_ * u_) for nm_, d_ in (("left", tp.inner[0] - b[0]), ("right", b[2] - tp.inner[2]),
                                                  ("bottom", tp.inner[1] - b[1]), ("top", b[3] - tp.inner[3]))
                   if d_ > e_]
            out.append((a, u"the crop edge (%s)" % u", ".join(u"%s by %.2f mm" % q_ for q_ in ov_)))
        for c in I[i + 1:]:
            if c["group"] != a["group"] and tp_hit(b, c["box"], tp.pad):
                out.append((a, repr(c["text"][:40])))
        for K in tp.keeps:
            if K["name"] in a["allow"] or K["kind"] in a["allow"]:
                continue
            if _tp_keep_hits(b, K, tp.pad):
                out.append((a, u"%s %s" % (K["kind"], K["name"] or u"")))
    return out
