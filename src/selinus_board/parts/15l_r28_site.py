# ---- MIRAQUA round 28 Oct 2026 (site board v50): p.02 legend grid + stream-edge diagram, pp.04-05 sections, key maps (worker SB-site). Shared pieces: parts/15h_r28_shared.py,
# common/r28_style.py, common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# P02.2 the stream edge alone, both banks straightened along the stream (crop drw_edge_types, under the site
# readings); P04.1 / P14.1 the sections pages' key maps at their booklet size (crops sec_sections_key_1 / _2 / _s4);
# P04.2 + F12 the cuts' words (key sentence, what steers the project, callouts by priority, larger by steps); bank
# depth (research/bank_depth_2026-10-28/REPORT.md §4 item 1, Aras 28 Oct 14:12): the bank top = the bank crest, the
# DSİ walls of the town reach at wall_height (photos), the bed width only where a cut crosses the stream.

# ============================================================ text: real Arial widths, **bold** runs, arrows (G5)
# v50 (MIRAQUA 28 Oct, G5, P04.2): the PDF writer centres and right-aligns by tw (0.92 x the capital height a
# letter), wider than Arial's letters, so words set side by side (bold keywords in a sentence) or centred on a point
# are placed here by their real widths. Arial = Helvetica's widths (common/pdf_fonts.py), per 1000 em, codes 32-126.
SITE28_AW = [int(v_) for v_ in (
    "278 278 355 556 556 889 667 191 333 333 389 584 278 333 278 278 556 556 556 556 556 556 556 556 556 556 "
    "278 278 584 584 584 556 1015 667 667 722 722 667 611 778 722 278 500 667 556 833 722 778 667 778 722 667 611 "
    "722 667 944 667 667 611 278 278 278 469 556 333 556 556 500 556 556 278 556 556 222 222 500 222 833 556 556 "
    "556 556 333 500 278 556 500 722 500 500 500 334 260 334 584").split()]
SITE28_AWB = [int(v_) for v_ in (
    "278 333 474 556 556 889 722 238 333 333 389 584 278 333 278 278 556 556 556 556 556 556 556 556 556 556 "
    "333 333 584 584 584 611 975 722 722 722 722 667 611 778 722 278 556 722 611 833 722 778 667 778 722 667 611 "
    "722 667 944 667 667 611 333 278 333 584 556 333 556 611 556 611 556 333 611 611 278 278 556 278 889 611 611 "
    "611 611 389 556 333 611 556 778 556 556 500 389 280 389 584").split()]
SITE28_AX = {u"·": (278, 278), u"—": (1000, 1000), u"–": (556, 556), u"ı": (278, 278), u"İ": (278, 278),
             u"ç": (500, 556), u"ş": (500, 556), u"ğ": (556, 611), u"ö": (556, 611), u"ü": (556, 611),
             u"Ç": (722, 722), u"Ş": (667, 667), u"Ğ": (778, 778), u"Ö": (778, 778), u"Ü": (722, 722),
             u"²": (333, 333), u"³": (333, 333), u"×": (584, 584), u"é": (556, 556), u"’": (222, 278),
             u"°": (400, 400)}
SITE28_CAP = 0.718      # capital height / font size of the writer (_PDF_CAP)
SITE28_ARW = 1.5        # an arrow's width in a line of text, x its capital height (the font has no arrow)


def site28_tw(txt, h, bold=False):
    """v50 (MIRAQUA 28 Oct, G5): the width (board units) of txt in Arial at capital height h"""
    tab = SITE28_AWB if bold else SITE28_AW
    w_ = 0
    for ch in txt:
        o = ord(ch)
        w_ += tab[o - 32] if 32 <= o < 127 else SITE28_AX.get(ch, (556, 611))[1 if bold else 0]
    return w_ / 1000.0 * h / SITE28_CAP


def site28_words(txt):
    """'**bold** plain -> more' as words [(space before, [(piece, bold)])]; a word may change weight inside
    (**K4**,); the word '->' is an arrow"""
    toks, cur, sp = [], [], False
    for j, t_ in enumerate(txt.split(u"**")):
        for i, piece in enumerate(t_.split(u" ")):
            if i > 0:
                if cur:
                    toks.append((sp, cur))
                cur, sp = [], True
            if piece:
                cur.append((piece, j % 2 == 1))
    if cur:
        toks.append((sp, cur))
    return toks


def site28_ww(word, h):
    if len(word) == 1 and word[0][0] == u"->":
        return SITE28_ARW * h
    return sum(site28_tw(t_, h, b_) for t_, b_ in word)


def site28_lines(txt, width, h):
    """txt (with **bold** runs) broken at its spaces into lines no wider than width at capital height h"""
    sw_ = site28_tw(u" ", h)
    lines, line, lw_ = [], [], 0.0
    for sp, word in site28_words(txt):
        ww = site28_ww(word, h)
        if line and lw_ + sw_ + ww > width:
            lines.append(line)
            line, lw_ = [], 0.0
        lw_ += (sw_ if line else 0.0) + ww
        line.append((bool(line), word))
    if line:
        lines.append(line)
    return lines


def site28_line_w(line, h):
    sw_ = site28_tw(u" ", h)
    return sum((sw_ if sp else 0.0) + site28_ww(word, h) for sp, word in line)


def site28_one(txt, h):
    """txt as one line (site28_lines without a width)"""
    return [w_ for ln in site28_lines(txt, 1e12, h) for w_ in ln]


def site28_arrow(B, x, y, h, col, L, order=40):
    """a right arrow in a line of text at baseline y, capital height h (SITE28_ARW x h wide)"""
    ym = y + 0.45 * h
    B.line([(x + 0.2 * h, ym), (x + 1.0 * h, ym)], col, L, order, 0.009 * h)
    B.fill([[(x + 0.85 * h, ym + 0.3 * h), (x + 1.3 * h, ym), (x + 0.85 * h, ym - 0.3 * h)]], col, L, order)


def site28_draw_line(B, line, x, y, h, col, L, order=40, bcol=None):
    """one line of site28_lines from x at baseline y, each run of one weight one whole text (live words); bold runs
    in bcol when given. Returns the x at its end."""
    segs = []
    for sp, word in line:
        if len(word) == 1 and word[0][0] == u"->":
            if sp:
                segs.append([u" ", False])
            segs.append(None)
            continue
        for j, (t_, b_) in enumerate(word):
            t2 = (u" " if sp and j == 0 else u"") + t_
            if segs and segs[-1] is not None and segs[-1][1] == b_:
                segs[-1][0] += t2
            else:
                segs.append([t2, b_])
    cx = x
    for sg in segs:
        if sg is None:
            site28_arrow(B, cx, y, h, col, L, order)
            cx += SITE28_ARW * h
            continue
        t_, b_ = sg
        if t_.strip():
            B.text(t_, cx, y, h, bcol if (b_ and bcol is not None) else col, L, order=order, font=FONT_TITLE, bold=b_)
        cx += site28_tw(t_, h, b_)
    return cx


def site28_text(B, txt, x, y, h, col, L, order=40, bcol=None, align="L"):
    """one line with **bold** runs and -> arrows, placed by its real width (align L, C or R at x); returns (x0, x1)"""
    line = site28_one(txt, h)
    lw_ = site28_line_w(line, h)
    x0 = x - {"C": 0.5, "R": 1.0}.get(align, 0.0) * lw_
    site28_draw_line(B, line, x0, y, h, col, L, order, bcol)
    return x0, x0 + lw_


def site28_fit(B, txt, x, y, h, width, col, L, order=40, bcol=None, align="L"):
    """site28_text made smaller when it is wider than width (as B.fit); returns the height used"""
    need = site28_line_w(site28_one(txt, h), h)
    if need > width > 0:
        h *= width / need
    site28_text(B, txt, x, y, h, col, L, order, bcol, align)
    return h


def site28_para(B, txt, x, y, width, h, col, L, lead=1.7, order=40, bcol=None):
    """txt wrapped to width from baseline y; returns the next baseline"""
    for ln in site28_lines(txt, width, h):
        site28_draw_line(B, ln, x, y, h, col, L, order, bcol)
        y -= lead * h
    return y


def site28_title(s):
    """an upper-case name in title case with its Turkish letters (K4 · ULUCAMİ ÖNÜ -> K4 · Ulucami Önü); words
    with digits and words not in capitals stay as written"""
    out = []
    for w_ in (s or u"").split(u" "):
        if not w_ or any(c_.isdigit() for c_ in w_) or not w_.isupper():
            out.append(w_)
            continue
        lo = w_.replace(u"I", u"ı").replace(u"İ", u"i").lower()
        out.append({u"i": u"İ", u"ı": u"I"}.get(lo[0], lo[0].upper()) + lo[1:])
    return u" ".join(out)


# ============================================================ bank depth (REPORT §4 item 1; Aras 28 Oct 14:12)
# The bank top of a stream crossing is the bank CREST, found by the water board's rule (res_bank_top) on a 1 m
# profile out from the bed, up to SITE28_CREST_M on each side; the lower crest is printed. The survey shows the town
# reach before the DSİ walls: from the frame's upstream end to Üç Kemer (research chainage 5,290-6,560) the walls,
# WALL_H above the bed (site photos 1 Oct 2026, 4-6 m; input wall_height), stand wherever the survey crest is lower.
SITE28_CREST_M = 60     # m: the crest is searched this far out from the bed on each side (as the research cuts)
SITE28_RCH = (5965.0, 6560.0)       # research chainage of K4 and Üç Kemer (K5) on the survey centreline (REPORT)
SITE28_WALLED = (5290.0, 6560.0)    # the DSİ walled town reach in that chainage: the frame's upstream end to Üç Kemer
SITE28_NOBED = ((5790.0, 5940.0), (6065.0, 6390.0))   # no survey heights in the channel: "bed not surveyed"
SITE28_CROSS = 60.0     # degrees: a cut crossing the stream at this angle or more prints its bed width (REPORT 1c)
SITE28_NEAR_M = 80.0    # m: a point farther than this from the stream's main line has no reach chainage


def site28_crest(zf, reach=SITE28_CREST_M):
    """REPORT §4 1a, the water board's res_bank_top on a 1 m profile: going out from the bed, a steep rise (0.15 m
    or more per metre, 0.5 m or more in all) with level or falling ground behind it (the next 5 m within 0.15 m of
    its top); the crest = the highest point of that top. zf(m) = the ground m metres out from the bed (None beyond
    the cut), read only as far as needed. (m, z) or None."""
    memo = {}

    def g(m):
        if m > reach:
            return None
        if m not in memo:
            memo[m] = zf(m)
        return memo[m]
    i, toe = 0, None
    while g(i) is not None and g(i + 1) is not None:
        if g(i + 1) - g(i) >= 0.15:
            toe = i if toe is None else toe
        elif toe is not None:
            behind = [g(j) for j in range(i, i + 6)]
            if None not in behind and g(i) - g(toe) >= 0.5 and max(behind) - g(i) <= 0.15:
                j = max(range(6), key=lambda q: behind[q])
                return i + j, behind[j]
            toe = None
        i += 1
    return None


def site28_cut_top(S, p, nx, ny):
    """the lower bank crest (m a.s.l.) of a cut across the stream from its bed point p along +-(nx, ny) (a unit
    vector), 1 m steps on the terrain (S.z_at) inside the frame; None unless both sides show one"""
    zs = []
    for d in (-1.0, 1.0):
        def zf(m, d=d):
            qx, qy = p[0] + d * nx * m, p[1] + d * ny * m
            return S.z_at(qx, qy) if S.F.inside(qx, qy) else None
        c_ = site28_crest(zf)
        if c_ is None:
            return None
        zs.append(c_[1])
    return min(zs)


def site28_reach(S, x, y, ux=None, uy=None):
    """(research chainage, angle, tangent) of the stream point nearest (x, y): the board's main stream line (S.chan)
    scaled through K4 and K5 (BRIDGES_K) to SITE28_RCH; the angle (degrees, 0-90) of the direction (ux, uy) to the
    stream there (90 without one); (None, 90, None) without the line or farther than SITE28_NEAR_M from it"""
    m = getattr(S, "_s28_line", None)
    if m is None:
        main = (getattr(S, "chan", None) or {}).get("line")
        m = False
        if main and len(main) >= 2:
            kq = dict((b_[0], (b_[2], b_[3])) for b_ in BRIDGES_K)
            b4, b5 = pl_chainage(main, *kq["K4"]), pl_chainage(main, *kq["K5"])
            if abs(b5 - b4) > 50.0:
                m = (main, b4, b5)
        S._s28_line = m
    if not m:
        return None, 90.0, None
    main, b4, b5 = m
    s = pl_chainage(main, x, y)
    q, t = pl_point_at(main, s)
    if math.hypot(q[0] - x, q[1] - y) > SITE28_NEAR_M:
        return None, 90.0, None
    ang = 90.0 if ux is None else math.degrees(math.asin(min(1.0, abs(ux * t[1] - uy * t[0]))))
    return SITE28_RCH[0] + (s - b4) * (SITE28_RCH[1] - SITE28_RCH[0]) / (b5 - b4), ang, t


def site28_bank_top(S, smp, k0, k1, step, x0, y0, ux, uy):
    """REPORT §4 1a for the water run smp[k0:k1] of a cut from (x0, y0) along (ux, uy) (smp rows [s, kind, ref, z],
    step m apart): its lowest point ib, the reach chainage r and the cut's angle to the stream (site28_reach), and
    the lower bank crest (m a.s.l.): out from the bed along the cut where it crosses the stream at SITE28_CROSS° or
    more (sl, sr: the crests' s on the cut; pts their (s, z)), else across the stream at the bed (site28_cut_top);
    crest None unless both sides show one"""
    ib = min(range(k0, k1), key=lambda j: smp[j][3])
    bx, by = x0 + ux * smp[ib][0], y0 + uy * smp[ib][0]
    r, ang, t = site28_reach(S, bx, by, ux, uy)
    out = dict(ib=ib, r=r, ang=ang, crest=None, sl=None, sr=None, pts=[])
    if ang >= SITE28_CROSS or t is None:
        st = max(1, int(round(1.0 / step)))
        for key, d in (("sl", -1), ("sr", 1)):
            def zf(m, d=d):
                j = ib + d * m * st
                return smp[j][3] if 0 <= j < len(smp) else None
            c_ = site28_crest(zf)
            if c_:
                out[key] = smp[ib + d * c_[0] * st][0]
                out["pts"].append((out[key], c_[1]))
        if len(out["pts"]) == 2:
            out["crest"] = min(z_ for s_, z_ in out["pts"])
    else:
        out["crest"] = site28_cut_top(S, (bx, by), -t[1], t[0])
    return out


def site28_bank_rule(cr, bed, old, span):
    """REPORT §4 1b-1e for one stream crossing (cr from site28_bank_top; bed and the old bank top, the ground just
    outside the water, in m a.s.l.; span = the water run on the cut, m): kind "crest" (the lower crest), "ground"
    (no crest on a side: the old bank top, as before) or "wall" (in the DSİ walled reach where the survey's top is
    lower than the walls: bed + WALL_H); top (drawn and printed), survey (the survey's top), town (in the walled
    reach), nobed (no survey heights in the channel there), w (the bed width across the stream, m, to 0.5 m)"""
    r = cr.get("r")
    survey = cr["crest"] if cr.get("crest") is not None else old
    out = dict(kind="crest" if cr.get("crest") is not None else "ground", top=survey, survey=survey,
               town=r is not None and r <= SITE28_WALLED[1],
               nobed=r is not None and any(a_ <= r <= b_ for a_, b_ in SITE28_NOBED),
               w=round(2.0 * span * math.sin(math.radians(cr.get("ang", 90.0)))) / 2.0)
    if out["town"] and survey < bed + WALL_H:
        out.update(kind="wall", top=bed + WALL_H)
    return out


def site28_channel_top(sd_, cr, a, b):
    """(bank top above the cut's base, (s0, s1) the channel is drawn within) for channel_polys: the crest within
    the crests, the walls between the walls; (None, None) for the old rule"""
    if not cr or cr.get("kind") not in ("crest", "wall"):
        return None, None
    top = cr["top"] - sd_["base"]
    if cr["kind"] == "wall":
        return top, (a, b)
    lo = cr["sl"] if cr.get("sl") is not None else a - 4.0
    hi = cr["sr"] if cr.get("sr") is not None else b + 4.0
    return top, (min(lo, a), max(hi, b))


def site28_main_k(sd_):
    """the index of a cut's main stream crossing (its lowest bed), or None"""
    if not sd_["water"]:
        return None
    return min(range(len(sd_["water"])), key=lambda k_: sd_["water"][k_][2])


def site28_bank_of(sd_, k_):
    """(the crossing's bank dict or {}, its bank level m a.s.l. or None) for water run k_"""
    bks = sd_.get("banks") or []
    lv = [l_ for l_ in sd_["levels"] if l_[3] == "bank"]
    return (bks[k_] if k_ < len(bks) else {}) or {}, (lv[k_][2] if k_ < len(lv) else None)


# ============================================================ pp.04-05 the cuts' words (P04.2, F12, G4, G13)
# The words of the cuts grow by steps (booklet pt, largest first): sections_plan takes the largest step at which
# the cuts still fit as at the smallest one (the last step: about the v49 callouts' size). head = names and title,
# call = the key sentence and the callouts, minor = levels, tags and the scale bar, sat = the satellite rows' names.
SITE28_SEC_TXT = (dict(head=8.0, call=7.5, minor=7.0, sat=6.0), dict(head=8.0, call=7.5, minor=6.0, sat=5.5),
                  dict(head=7.5, call=7.0, minor=5.5, sat=5.0), dict(head=7.0, call=6.5, minor=5.0, sat=5.0))
SITE28_SEC_TIERS = 3    # rows of callouts under a cut (the water's own words may take two more)
SITE28_TYPES_F = (5.0, 2.5, 1.0)    # the building types enlarged (a diagram) by the first of these that fits (P05.1)
SITE28_EDGE_WORD = {"building": u"backs of buildings", "street": u"a street", "pedestrian": u"a walkable path",
                    "green": u"planted ground", "parking": u"parking", "open": u"loose ground"}
SITE28_WL_WORD = {1: u" behind a wall", 2: u" on an embankment"}
# what steers the project at the water, the strongest first (the edge types' own words, EDGE)
SITE28_STEER = (("building", u"**backs of buildings** to the water"),
                ("parking", u"**parking** at the water, waiting to change"),
                ("open", u"**loose ground** at the water, open to change"),
                ("street", u"a **street edge**: seen, not touched"),
                ("green", u"a **planted edge**, porous"),
                ("pedestrian", u"a **walkable edge** within reach"))
SITE28_HUB_M = 300.0    # m: the masterplan hub named as a cut's link at most this far from its crossing
SITE28_XING_M = 200.0   # m: else a masterplan crossing this near
SITE28_K_M = 250.0      # m: without the masterplan's movement, the nearest bridge K1-K6 this near


def site28_sec_end(st, k, U):
    """the room kept at both ends of a cut (board units) at step st (an entry of SITE28_SEC_TXT; k = board units
    per booklet mm): its end name, end level and the satellite rows' names"""
    hd, hm, hs = bk_hk(st["head"], k), bk_hk(st["minor"], k), bk_hk(st["sat"], k)
    return max(SEC_END * U, site28_tw(u"+888.88", hm) + 0.7 * U, site28_tw(u"S8'", hd, True) + 0.7 * U,
               max(site28_tw(lab, hs) for k_, lab in SAT_ROWS) + 0.55 * U)


def site28_sec_sizes(sd_, U):
    """[head, call, minor, sat] capital heights (board units) of a cut's words and its end room, at its step
    (sd_["_txt"] = dict(step, k, end), set by sections_plan); without one the smallest step on the 140 U page"""
    t = sd_.get("_txt") or {}
    st = SITE28_SEC_TXT[min(len(SITE28_SEC_TXT) - 1, max(0, int(t.get("step", len(SITE28_SEC_TXT) - 1))))]
    k = t.get("k") or 140.0 * U / BK_AW
    return [bk_hk(st[q], k) for q in ("head", "call", "minor", "sat")] + [t.get("end") or site28_sec_end(st, k, U)]


def site28_road_call(t):
    """(text, priority) of a street a cut crosses, from road_label's text: its name and the length the cut runs on
    it in cm (G13), priority 2; an OSM line with no surveyed surface: its name alone, an unnamed street: "street",
    priority 3"""
    nm_, _, rest = t.partition(u" · ")
    nm_ = site28_title(nm_)
    if u"OSM line" in rest:
        return nm_, 3
    try:
        m_ = float(rest.split(u" m")[0])
    except ValueError:
        return nm_, 3
    if nm_.lower() == u"street":
        return u"street · " + u_dim(m_), 3
    return nm_ + u" · " + u_dim(m_), 2


def site28_callouts(B, L, P, calls, ytop, U, lh, xlo, xhi, tiers=SITE28_SEC_TIERS):
    """v50 (MIRAQUA 28 Oct, P04.2, G4): a cut's callouts [(s, z, text, priority)] in rows under it from ytop down,
    by priority (0 the water: always; 1 edges and history; 2 named streets; 3 other streets and places): each on the
    first row where it clears the words placed before it by two letters, kept between xlo and xhi and over its
    leader; at most `tiers` rows (priority 0 two more); a word with no free row is left out. A leader from its point
    to its word, broken where it passes a word of a row above. Returns (lowest baseline, [texts left out])."""
    step = lh + 0.4 * U
    base_y = ytop - lh
    gap = max(0.6 * U, 2.2 * lh)
    placed, out_ = [], []
    for c_ in sorted(calls, key=lambda q: (q[3], q[0])):
        s, zf, txt, pr = c_
        fx = P(s, zf)[0]
        half = 0.5 * site28_tw(txt, lh)
        cx = fx
        if xlo is not None:
            cx = max(cx, min(fx + half - 0.3 * U, xlo + half))
        if xhi is not None:
            cx = min(cx, max(fx - half + 0.3 * U, xhi - half))
        cap = tiers + (2 if pr == 0 else 0)
        tier = 0
        while tier < cap and any(t2 == tier and cx - half < r2 + gap and l2 - gap < cx + half
                                 for l2, r2, t2, c2 in placed):
            tier += 1
        if tier >= cap:
            out_.append(txt)
            continue
        placed.append((cx - half, cx + half, tier, c_))
    low = base_y
    for l1, r1, tier, (s, zf, txt, pr) in placed:
        fx, fy = P(s, zf)
        ly = base_y - tier * step
        cuts = sorted((base_y - t2 * step - 0.12 * U, base_y - t2 * step + lh + 0.12 * U)
                      for l2, r2, t2, c2 in placed if t2 < tier and l2 - 0.15 * U < fx < r2 + 0.15 * U)
        ytop_ = fy
        for c0, c1 in reversed(cuts):
            if c1 < ytop_:
                B.line([(fx, ytop_), (fx, c1)], INK2, L, 35, 0.035)
            ytop_ = min(ytop_, c0)
        if ly + lh + 0.12 * U < ytop_:
            B.line([(fx, ytop_), (fx, ly + lh + 0.12 * U)], INK2, L, 35, 0.035)
        B.fill([circle_pts(fx, fy, 0.09 * U, 8)], INK2, L, 35)
        site28_text(B, txt, 0.5 * (l1 + r1), ly, lh, INK, L, align="C")
        low = min(low, ly)
    return low, out_


def site28_tag_fit(tag, wpx, h):
    """a cut building's tag at height h if the building (wpx board units wide) holds it (as v16.4: 0.6 x its
    width), else its floors alone ("2 fl"), else None"""
    if wpx > 0.6 * site28_tw(tag, h):
        return tag
    short_ = tag.split(u" · ")[-1]
    if short_ != tag and short_.endswith(u" fl") and wpx > 0.6 * site28_tw(short_, h):
        return short_
    return None


def site28_bld_tag(B, L, P, prof, txt, h, col, U, placed, order=31):
    """a cut building's tag over its roof (as bld_draw_cut's, at height h, centred by its real width); left out when
    it would overlap a tag already placed [(x0, x1, y)]"""
    top_ = max(z for s, z in (prof["roof"] or prof["body"]))
    sm = (prof["body"][0][0] + prof["body"][1][0]) / 2.0
    q = P(sm, top_)
    hw_ = 0.5 * site28_tw(txt, h) + 0.15 * U
    if any(x0_ < q[0] + hw_ and q[0] - hw_ < x1_ and abs(y_ - q[1]) < h + 0.15 * U for x0_, x1_, y_ in placed):
        return
    site28_text(B, txt, q[0], q[1] + 0.12 * U, h, col, L, order=order, align="C")
    placed.append((q[0] - hw_, q[0] + hw_, q[1]))


def site28_link(S, px, py, line):
    """what a cut's crossing (px, py) links to in the masterplan (masterplan_results.json "movement", once per run):
    its nearest hub within SITE28_HUB_M, else its nearest crossing within SITE28_XING_M, else a street it changes
    that the cut crosses; without the masterplan's movement the nearest bridge K1-K6 within SITE28_K_M; u"" when none"""
    if not hasattr(S, "_s28_mp"):
        S._s28_mp = mp_movement()
    M = S._s28_mp
    if M:
        best = None
        for h in M.get("hubs") or []:
            q = _xy1(h.get("xy"))
            d = math.hypot(q[0] - px, q[1] - py) if q else 1e12
            if d <= SITE28_HUB_M and (best is None or d < best[0]):
                best = (d, h)
        if best:
            h = best[1]
            return u"**{}**, {} hub{}".format(site28_title(h.get("name") or u""), u"transit" if h.get("role") ==
                                              "transit" else u"walking", u" · sub-hub in the bed" if h.get("sub_hub")
                                              else u"")
        for c_ in M.get("crossings") or []:
            q = _xy1(c_.get("xy"))
            d = math.hypot(q[0] - px, q[1] - py) if q else 1e12
            if d <= SITE28_XING_M and (best is None or d < best[0]):
                best = (d, c_)
        if best:
            return u"**{}**, {}".format(site28_title(best[1].get("name") or u""), best[1].get("kind") or u"crossing")
        x0, y0, x1, y1 = line[:4]
        for r_ in M.get("roads") or []:
            if r_.get("change") in (None, "", "kept"):
                continue
            P_ = _xy_list(r_.get("xy"))
            if any(seg_x((x0, y0), (x1 - x0, y1 - y0), a_, (b_[0] - a_[0], b_[1] - a_[1])) for a_, b_ in zip(P_, P_[1:])):
                return u"**{}**, {}".format(r_.get("name") or u"street", r_.get("change"))
        return u""
    best = None
    for kk, nm_, bx, by in BRIDGES_K:
        d = math.hypot(bx - px, by - py)
        if d <= SITE28_K_M and (best is None or d < best[0]):
            best = (d, kk, nm_)
    return u"the nearest bridge is **{} {}**".format(best[1], best[2]) if best else u""


def site28_sec_reading(S, sd_):
    """v50 (MIRAQUA 28 Oct, P04.2): (key sentence, what steers the project) of a cut, from its own data only, with
    **bold** keywords: whether it crosses or runs along the stream, the bed's depth below the lower bank crest or
    between the DSİ walls (photos; REPORT §4 1a-1e), the edges on its banks; then the strongest constraint or chance
    at the water and its link in the masterplan (site28_link). Memoised on the cut (sd_["_read"])."""
    if "_read" in sd_:
        return sd_["_read"]
    x0, y0, x1, y1 = sd_["line"][:4]
    Lc = math.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / Lc, (y1 - y0) / Lc
    k_ = site28_main_k(sd_)
    tot = sum(sd_["comp"].values()) or 1.0
    top = sorted(sd_["comp"].items(), key=lambda kv: -kv[1])[:2]
    if k_ is None:
        key = u"The cut **does not cross the stream**" + (u": it runs through " + u" and ".join(
            u"{} ({:.0f}%)".format(short(CAT[c_][0]).lower(), 100.0 * v_ / tot) for c_, v_ in top) if top else u"") + u"."
        cons = u"**{}** over {:.0f}% of the cut".format(short(CAT[top[0][0]][0]).lower(), 100.0 * top[0][1] / tot) \
            if top else u""
        px, py = x0 + ux * 0.5 * Lc, y0 + uy * 0.5 * Lc
    else:
        a, b, bed, lvl = sd_["water"][k_]
        bz = bed + sd_["base"]
        cr, zb = site28_bank_of(sd_, k_)
        wall = cr.get("kind") == "wall"
        if cr.get("nobed"):
            dep = u"the bed is **not surveyed** here" + (u", between **walls {} high** (site photos, 1 Oct 2026)".format(
                u_height(WALL_H)) if wall else u"")
        elif wall:
            dep = u"the bed at {} lies between **walls {} high** (site photos, 1 Oct 2026)".format(u_level(bz),
                                                                                              u_height(WALL_H))
        elif zb is not None:
            dep = u"the bed at {} lies **{} below** the lower bank{}".format(
                u_level(bz), u_height(zb - bz), u" crest" if cr.get("kind") == "crest" else u"")
            if cr.get("town"):
                dep += u" (survey, before the DSİ walls)"
        else:
            dep = u"the bed lies at {}".format(u_level(bz))
        if (sd_.get("bed_src") or [])[k_:k_ + 1] == ["interpolated"] and not cr.get("nobed"):   # as section_caption
            dep += u" " + bcite("Section bed levels: interpolated along the stream from the surveyed depths.")
        if cr.get("ang", 90.0) < SITE28_CROSS:
            key = u"The cut runs **along the stream**, not across it; " + dep
        else:
            key = dep[:1].upper() + dep[1:]
        sides = [(t_, wl_) for s_, t_, wl_, gz_ in sd_["labels"] if abs(s_ - a) < 0.3 or abs(s_ - b) < 0.3]
        ws = [SITE28_EDGE_WORD.get(t_, t_) + SITE28_WL_WORD.get(wl_, u"") for t_, wl_ in sides]
        if len(ws) >= 2 and ws[0] == ws[1]:
            key += u"; {} on both banks".format(ws[0])
        elif len(ws) >= 2:
            key += u"; {} on one bank, {} on the other".format(ws[0], ws[1])
        elif ws:
            key += u"; {} at the water".format(ws[0])
        key += u"."
        tys = [t_ for t_, wl_ in sides]
        wls = [wl_ for t_, wl_ in sides]
        if wall and "pedestrian" not in tys:
            cons = u"**walls {} high**, no walkable edge at the water".format(u_height(WALL_H))
        elif 2 in wls:
            cons = u"an **embanked** bank, cut off from the street"
        elif 1 in wls:
            cons = u"a **walled** bank, cut off from the street"
        else:
            cons = next((t2 for t1, t2 in SITE28_STEER if t1 in tys), u"")
        sm = 0.5 * (a + b)
        px, py = x0 + ux * sm, y0 + uy * sm
    link = site28_link(S, px, py, sd_["line"])
    steer = u""
    if cons or link:
        steer = u"Steers the project: " + cons + ((u" -> " if cons else u"") + link if link else u"") + u"."
    sd_["_read"] = (key, steer)
    return sd_["_read"]


def site28_page_of(pages, nm):
    """v50 (MIRAQUA 28 Oct, F12): the index of the page of sections_plan's pages ([[row of (item, width)]]) that holds
    the cut named nm, or None."""
    for i, pg in enumerate(pages):
        if any(c_.get("name") == nm for r in pg for c_, w_ in r):
            return i
    return None


# ============================================================ P04.1 / P14.1 the sections pages' key maps
SITE28_KEY_W = 190.0    # mm: a sections page's key map on the booklet page (drawn at that size, placed at scale 1.0)
SITE28_KEY_H = 42.0     # mm: at most this tall
SITE28_KEY_COL = 14.0   # mm: its left column (KEY, the north arrow)


def draw_sections_key(S, B, x, y, sw, names, k_):
    """v45 (Prompt 2: one small key map on each sections page) ... v50 (MIRAQUA 28 Oct, P04.1, P14.1, G8; was in
    parts/15e at 1:50,000): drawn at its booklet size, SITE28_KEY_W x at most SITE28_KEY_H mm (the booklet places
    it at scale 1.0: k = PDF_SCALE / 1000 board units per mm), no scale (a key map): a left column with KEY and the
    north arrow, the whole site frame with water and buildings faint, the study area (draw_r28_study), every cut thin
    and grey, this page's cuts in ink with both end names (k_ "s4": S4-S4' thick in the accent, MARK_C), the names
    7.5 pt placed clear of each other and of the cut lines (place_labels_all); a legend row under it. Right-aligned
    under the page's cuts on the sheet; its own crop sections_key_n. Returns the y below."""
    L = "LU_BOARD::Sections"
    F = S.F
    k = PDF_SCALE / 1000.0
    h75, h7 = bk_hk(7.5, k), bk_hk(7.0, k)
    s4 = k_ == "s4"
    x1 = x + sw - 0.3 * k                                 # the map's right edge (the crop ends at the cuts' edge)
    ss = min((SITE28_KEY_W - SITE28_KEY_COL - 0.6) * k / F.w, (SITE28_KEY_H - 4.8) * k / F.h)
    mw, mh = F.w * ss, F.h * ss
    x0 = x1 - mw
    yt = y - 0.6 * k
    V = View(F, ss, x0, yt)
    r = (x0, yt - mh, x1, yt)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 30)
    for wt in S.water:
        CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), BLUE_L, L, 31)
    mini_buildings(S, CB, V, L, lambda u: FAINT, order=32)
    draw_r28_study(S, CB, V, k, L, order=33)              # G8
    on = set(names)
    grey = mix(INK2, PAPER, 0.45)
    hi_c = MARK_C if s4 else INK
    segs, items = [], []
    for x0_, y0_, x1_, y1_, nm in sorted(S.sec_lines, key=lambda c_: c_[4] in on):   # this page's cuts on top
        a, b = V.p(x0_, y0_), V.p(x1_, y1_)
        hi = nm in on
        CB.line([a, b], hi_c if hi else grey, L, 37 if hi else 36, bk_lw((1.0 if s4 else 0.6) if hi else 0.25, k))
        segs.append(((a[0] / k, a[1] / k), (b[0] / k, b[1] / k)))
        ends = [(a, nm), (b, nm + u"'")] if hi else [(max((a, b), key=lambda p_: p_[1]), nm)]
        for p_, t_ in ends:
            wd = site28_tw(t_, h75, hi) / k
            items.append(dict(x=p_[0] / k, y=p_[1] / k, rank=0 if hi else 1, t=t_, hi=hi,
                              wh=(lambda f, wd=wd: (wd * f + 0.8, 1.5 * h75 / k * f))))
    got = place_labels_all(items, [], bounds=(r[0] / k, r[1] / k, r[2] / k, r[3] / k), segs=segs, sizes=(1.0,))
    for i, (bx, lead, f) in got.items():
        it = items[i]
        if lead:
            e = lp_leader_end(bx, (it["x"], it["y"]))
            B.line([(it["x"] * k, it["y"] * k), (e[0] * k, e[1] * k)], INK2, L, 39, bk_lw(0.15, k))
        site28_text(B, (u"**{}**" if it["hi"] else u"{}").format(it["t"]), (bx[0] + 0.4) * k,
                    bx[1] * k + 0.3 * h75, h75, hi_c if it["hi"] else INK2, L, order=40)
    B.line(rect(*r) + [(r[0], r[1])], INK2, L, 38, bk_lw(0.15, k))
    kx = x0 - SITE28_KEY_COL * k                          # the left column: KEY, the north arrow under it
    B.text(u"KEY", kx, yt - h75, h75, INK, L, font=FONT_TITLE, bold=True)
    draw_north_at(B, F, kx + 4.0 * k, yt - h75 - 8.0 * k, 4.0, k, L)
    # the legend row: the study area, this page's cuts, the others (drawn samples, 7 pt)
    yl = r[1] - 1.4 * k - h7
    lx = x0
    st = R28_STUDY_LINE
    for d_ in r28_pattern([(lx, yl + 0.4 * h7), (lx + 6.0 * k, yl + 0.4 * h7)], [m * k for m in st["dash_mm"]]):
        B.line(d_, C(st["colour"]), L, 40, bk_lw(st["width_mm"], k))
    lx = site28_text(B, R28_STUDY_NAME, lx + 7.5 * k, yl, h7, INK, L)[1] + 4.0 * k
    for col_, lw_, t_ in ((hi_c, (1.0 if s4 else 0.6), (u"S4, the water board's cut" if s4 else
                                                         u"cuts on this page")), (grey, 0.25, u"other cuts")):
        B.line([(lx, yl + 0.4 * h7), (lx + 6.0 * k, yl + 0.4 * h7)], col_, L, 40, bk_lw(lw_, k))
        lx = site28_text(B, t_, lx + 7.5 * k, yl, h7, INK, L)[1] + 4.0 * k
    low = yl - 0.8 * k
    crop_panel("sections_key_%s" % (k_ + 1 if isinstance(k_, int) else k_), kx - 0.3 * k, low, x1 + 0.3 * k, y,
               u"Key · " + u", ".join(names))
    CROP_PANELS[-1]["bk_w"] = (x1 + 0.3 * k - (kx - 0.3 * k)) / k      # its width on the booklet page, mm
    if (y - low) / k > SITE28_KEY_H + 0.05:
        LOG.append("WARNING: sections key map {} is {:.1f} mm tall (at most {:.0f} mm).".format(k_, (y - low) / k,
                                                                                              SITE28_KEY_H))
    return low


# ============================================================ P02.2 the stream edge alone, both banks straightened
SITE28_ET_BIN = 8.0     # m: a bin of the diagram (two of the bars' 4 m samples)
SITE28_ET_NEAR = 60.0   # m: an edge sample farther than this from the centreline is not on the Selinos's banks
SITE28_K_NEAR = 150.0   # m: a bridge K1-K6 this near the centreline is ticked on it (K1 crosses a side inlet)
SITE28_ET_COL = dict((t_, INK if t_ == "building" else EDGE[t_][1]) for t_ in EDGE)   # the bars' colours
SITE28_ET_WL = {1: INK2, 2: mix(INK2, PAPER, 0.5)}    # walled / embanked, as the DISCONNECTED bar
SITE28_ET_KEY = (("pedestrian", u"walkable"), ("street", u"street"), ("green", u"planted"), ("building", u"built"),
                 ("parking", u"parking"), ("open", u"loose"))


def site28_project(LX, LY, LC, pts):
    """the chainage and signed offset (m; + left, looking downstream) of each point on a centreline with vertices
    LX, LY and chainages LC: from its nearest vertex and the line's direction there (as shade_strip_calc)"""
    n = len(LX)
    if not pts:
        return []
    if HAVE_NP:
        X, Y = np.asarray(LX, float), np.asarray(LY, float)
        Q = np.asarray(pts, float)
        J = np.zeros(len(pts), np.int64)
        for a in range(0, len(pts), 500):                 # in chunks (memory)
            c_ = Q[a:a + 500]
            d2 = (c_[:, 0][:, None] - X[None, :]) ** 2 + (c_[:, 1][:, None] - Y[None, :]) ** 2
            J[a:a + 500] = d2.argmin(axis=1)
        J = [int(j_) for j_ in J]
    else:                                                 # every 10th vertex, then its neighbours
        cand = list(range(0, n, 10)) + [n - 1]
        J = []
        for px, py in pts:
            i0 = min(cand, key=lambda i: (LX[i] - px) ** 2 + (LY[i] - py) ** 2)
            J.append(min(range(max(0, i0 - 10), min(n, i0 + 11)), key=lambda i: (LX[i] - px) ** 2 + (LY[i] - py) ** 2))
    out = []
    for (px, py), j in zip(pts, J):
        tx, ty = LX[min(n - 1, j + 1)] - LX[max(0, j - 1)], LY[min(n - 1, j + 1)] - LY[max(0, j - 1)]
        tl = math.hypot(tx, ty) or 1.0
        tx, ty = tx / tl, ty / tl
        dx, dy = px - LX[j], py - LY[j]
        out.append((LC[j] + tx * dx + ty * dy, tx * dy - ty * dx))
    return out


def site28_edge_bins(S):
    """v50 (MIRAQUA 28 Oct, P02.2): the bank edge samples (S.edge_samples: every 4 m, the bars' own data) on the data
    pack's centreline (the tree-cover and shade charts' chainage, 0 at the upstream frame edge): dict(n, bm, L,
    bins = [left, right], each [(type, walled 0/1/2) or None per SITE28_ET_BIN bin: the most samples], used = m of
    bank drawn, tot = m the bars count, cor, line); None without samples or line. Once per run (S._s28_et)."""
    if getattr(S, "_s28_et", None) is not None:
        return S._s28_et or None
    S._s28_et = {}
    pk = seam_pack()
    cor, sel = pk.get("corridor") or {}, pk.get("selinos") or {}
    LX, LY, LC = ([float(v_) for v_ in (sel.get(q) or [])] for q in ("x", "y", "ch"))
    if len(LX) < 2 or len(LC) != len(LX) or len(LY) != len(LX) or not getattr(S, "edge_samples", None):
        return None
    Lt = float(cor.get("n_bins") or 0) * float(cor.get("bin_m") or 0.0) or LC[-1]
    nb = max(1, int(math.ceil(Lt / SITE28_ET_BIN)))
    cnt = [[None] * nb, [None] * nb]
    used = 0
    for (ex, ey, t_, wl_), (s_, o_) in zip(S.edge_samples, site28_project(LX, LY, LC, [(e[0], e[1])
                                                                                     for e in S.edge_samples])):
        if abs(o_) > SITE28_ET_NEAR or not 0.0 <= s_ < Lt:
            continue
        sd = 0 if o_ > 0.0 else 1
        i_ = min(nb - 1, int(s_ / SITE28_ET_BIN))
        if cnt[sd][i_] is None:
            cnt[sd][i_] = ({}, {})
        tc, wc = cnt[sd][i_]
        tc[t_] = tc.get(t_, 0) + 1
        wc[wl_] = wc.get(wl_, 0) + 1
        used += 1
    bins = []
    for sd in (0, 1):
        row = []
        for c_ in cnt[sd]:
            if c_ is None:
                row.append(None)
                continue
            tc, wc = c_
            row.append((max(sorted(tc), key=lambda q: (tc[q], q)), max(sorted(wc), key=lambda q: (wc[q], q))))
        for i_ in range(1, nb - 1):                       # a one-bin gap between two equal bins is closed
            if row[i_] is None and row[i_ - 1] is not None and row[i_ - 1] == row[i_ + 1]:
                row[i_] = row[i_ - 1]
        bins.append(row)
    S._s28_et = dict(n=nb, bm=SITE28_ET_BIN, L=Lt, bins=bins, used=4.0 * used, tot=4.0 * len(S.edge_samples), cor=cor,
                     line=(LX, LY, LC))
    return S._s28_et


def site28_runs(vals):
    """[(i0, i1, value)]: the runs of equal values (None left out)"""
    out, i = [], 0
    while i < len(vals):
        j = i
        while j + 1 < len(vals) and vals[j + 1] == vals[i]:
            j += 1
        if vals[i] is not None:
            out.append((i, j + 1, vals[i]))
        i = j + 1
    return out


def draw_edge_types(S, B, x, y, w, U):
    """v50 (MIRAQUA 28 Oct, P02.2): the stream edge alone, straightened: both banks as two bands along the stream's
    chainage (m from the upstream frame edge; no scale: a diagram), each bin coloured by its edge type in the bars'
    own colours (the same 4 m samples, SITE28_ET_BIN bins), walls and embankments as a thin strip on the water side,
    the stream between them with its covered reaches hatched and its bridges as ticks, K1-K6 as ticks across it all
    with their names under it (placed clear of each other, label_place). Its own crop (drw_edge_types), designed for
    RD_BK_W mm in p.02's side column under the site readings; words 7-8 pt. Returns the y below."""
    L = "LU_BOARD::SiteReadings"
    d = site28_edge_bins(S)
    if not d:
        LOG.append("Stream edge diagram (drw_edge_types): no bank samples or no centreline in the data pack, so not "
                   "drawn.")
        return y
    k = w / RD_BK_W
    h7, h8 = bk_hk(7.0, k), bk_hk(8.0, k)
    top = y
    B.text(u"WHERE EACH EDGE IS · BOTH BANKS, STRAIGHTENED", x, y - h8, h8, INK, L, font=FONT_TITLE, bold=True)
    yy = site28_para(B, u"chainage along the stream, m · left and right looking downstream · every 4 m, in the "
                        u"readings' colours " + bcite(EDGE_SRC), x, y - h8 - 1.6 * k - h7, w, h7, INK2, L, lead=1.45)
    lab_w = max(site28_tw(t_, h7, True) for t_ in (u"LEFT BANK", u"RIGHT BANK")) + 2.5 * k
    gx0, gx1 = x + lab_w, x + w
    sx = (gx1 - gx0) / d["L"]

    def X(s_):
        return gx0 + max(0.0, min(d["L"], s_)) * sx
    band, strip, stream = 5.5 * k, 1.2 * k, 3.0 * k
    ya = yy - 0.4 * k                                     # the chainage axis' numbers, then the bands
    yb0 = ya - 1.8 * k
    yls = yb0 - band                                      # left strip, stream, right strip, right band (tops)
    yst = yls - strip
    yrs = yst - stream
    yrb = yrs - strip
    ybot = yrb - band
    v = 0.0
    while v <= d["L"] + 1e-6:                             # the axis every 500 m, its unit on the last number
        t_ = u"{:,.0f}".format(v)
        tx = X(v) - 0.5 * site28_tw(t_, h7)
        if v + 500.0 > d["L"]:
            t_ += u" m"
        tx = min(max(tx, gx0), gx1 - site28_tw(t_, h7))
        B.text(t_, tx, ya, h7, INK2, L, font=FONT_TITLE)
        B.line([(X(v), ya - 0.5 * k), (X(v), yb0)], INK2, L, 21, bk_lw(0.15, k))
        v += 500.0
    for t_, yb_ in ((u"LEFT BANK", yb0 - band), (u"RIGHT BANK", ybot)):
        B.text(t_, x, yb_ + 0.5 * band - 0.5 * h7, h7, INK, L, font=FONT_TITLE, bold=True)
    for sd, (yt_, yb_), (st_, sb_) in ((0, (yb0, yls), (yls, yst)), (1, (yrb, ybot), (yrs, yrb))):
        B.fill([rect(gx0, yb_, gx1, yt_)], FAINT, L, 20)
        for i0, i1, t_ in site28_runs([v_[0] if v_ else None for v_ in d["bins"][sd]]):
            B.fill([rect(X(i0 * d["bm"]), yb_, X(i1 * d["bm"]), yt_)], SITE28_ET_COL.get(t_, FAINT), L, 21)
        for i0, i1, wl_ in site28_runs([v_[1] if v_ and v_[1] in SITE28_ET_WL else None for v_ in d["bins"][sd]]):
            B.fill([rect(X(i0 * d["bm"]), sb_, X(i1 * d["bm"]), st_)], SITE28_ET_WL[wl_], L, 21)
    cov_c = mix(CAT["water"][1], PAPER, 0.55)
    B.fill([rect(gx0, yrs, gx1, yst)], CAT["water"][1], L, 20)
    for a_, b_ in d["cor"].get("covered_reaches", []):
        cr_ = rect(X(a_), yrs, X(b_), yst)
        B.fill([cr_], cov_c, L, 21)
        B.hatch([cr_], SS_COVER_C, L, 22, 0.8 * k, math.radians(45.0), bk_lw(0.12, k))
    bch = d["cor"].get("bridges_ch", [])
    for i_ in range(0, len(bch) - 1, 2):                  # every bridge: a tick across the stream
        bx_ = X(0.5 * (bch[i_] + bch[i_ + 1]))
        B.line([(bx_, yls), (bx_, yrb)], INK, L, 23, bk_lw(0.3, k))
    # K1-K6: a tick across it all, the name under it
    LX, LY, LC = d["line"]
    kp = site28_project(LX, LY, LC, [(b_[2], b_[3]) for b_ in BRIDGES_K])
    items = []
    for (kk, nm_, bx, by), (s_, o_) in zip(BRIDGES_K, kp):
        if not 0.0 <= s_ <= d["L"] or abs(o_) > SITE28_K_NEAR:
            continue
        px = X(s_)
        B.line([(px, yb0 + 0.6 * k), (px, ybot - 0.6 * k)], INK, L, 24, bk_lw(0.35, k))
        t_ = u"**{}** {}".format(kk, nm_)
        wd = site28_line_w(site28_one(t_, h7), h7) / k
        items.append(dict(x=px / k, y=(ybot - 0.6 * k) / k, rank=0, t=t_, wh=(lambda f, wd=wd: (wd * f + 0.8,
                                                                                               1.5 * h7 / k * f))))
    taken = [(x / k, (ybot - 0.4 * k) / k, (x + w) / k, (ya + h7) / k)]
    got = place_labels_all(items, taken, bounds=(x / k, (ybot - 16.0 * k) / k, (x + w) / k, (ybot - 0.4 * k) / k),
                           sizes=(1.0,))
    low = ybot - 1.0 * k
    for i, (bx, lead, f) in got.items():
        it = items[i]
        e = lp_leader_end(bx, (it["x"], it["y"]))
        B.line([(it["x"] * k, it["y"] * k), (e[0] * k, e[1] * k)], INK2, L, 24, bk_lw(0.15, k))
        site28_text(B, it["t"], (bx[0] + 0.4) * k, bx[1] * k + 0.3 * h7, h7, INK, L)
        low = min(low, bx[1] * k)
    # the key: the edge types in the bars' colours, walls, embankments, the covered stream, bridges
    ky = low - 2.5 * k - h7
    kx = x
    keys = [(SITE28_ET_COL[t_], t_w) for t_, t_w in SITE28_ET_KEY] + [(SITE28_ET_WL[1], u"walled"),
                                                                       (SITE28_ET_WL[2], u"embanked"),
                                                                       (CAT["water"][1], u"stream"),
                                                                       (None, u"covered stream"), (INK, u"bridge")]
    for col_, t_ in keys:
        iw = 5.5 * k + site28_tw(t_, h7)
        if kx > x and kx + iw > x + w:
            kx, ky = x, ky - 4.0 * k
        sw_ = rect(kx, ky - 0.2 * k, kx + 4.0 * k, ky + 2.6 * k)
        if t_ == u"bridge":
            B.line([(kx + 2.0 * k, ky - 0.4 * k), (kx + 2.0 * k, ky + 2.8 * k)], INK, L, 24, bk_lw(0.35, k))
        elif col_ is None:
            B.fill([sw_], cov_c, L, 21)
            B.hatch([sw_], SS_COVER_C, L, 22, 0.8 * k, math.radians(45.0), bk_lw(0.12, k))
        else:
            B.fill([sw_], col_, L, 21)
        B.text(t_, kx + 5.5 * k, ky, h7, INK, L, font=FONT_TITLE)
        kx += iw + 3.5 * k
    low = ky - 1.5 * k
    crop_panel("edge_types", x, low, x + w, top + 0.5 * k, u"The stream edge · both banks, straightened")
    CROP_PANELS[-1]["bk_w"] = RD_BK_W                     # its width on the booklet page (p.02's side column) ...
    CROP_PANELS[-1]["grid"] = [0.0, RD_BK_W - 74.0]       # ... on the site readings' grid
    LOG.append("Stream edge diagram (drw_edge_types): {:,.0f} m of the bars' {:,.0f} m of bank lie within {:.0f} m of "
               "the stream's centreline and are drawn ({} bins of {:.0f} m a bank).".format(
                   d["used"], d["tot"], SITE28_ET_NEAR, d["n"], d["bm"]))
    return low - 1.0 * U
