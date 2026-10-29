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


# ============================================================ bank depth (REPORT §4 item 1; Aras 28 Oct 14:12)
# The bank top of a stream crossing is the bank CREST, found by the water board's rule (res_bank_top) on a 1 m
# profile out from the bed, up to SITE28_CREST_M on each side; the lower crest is printed. The survey shows the town
# reach before the DSİ walls: from the frame's upstream end to Üç Kemer (research chainage 5,290-6,560) the walls,
# WALL_H above the bed (site photos 1 Oct 2026, 4-6 m; input wall_height), stand wherever the survey crest is lower.
SITE28_CREST_M = 60     # m: the crest is searched this far out from the bed on each side (as the research cuts)
SITE28_RCH = (5849.4, 6559.6)       # chainage of K4 and Üç Kemer (K5) on the survey centreline (v51: K4 from the level table, T1 levels gap 3)
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


# ============================================================ P02.2 the stream edge alone, both banks straightened
SITE28_ET_BIN = 8.0     # m: a bin of the diagram (two of the bars' 4 m samples)
SITE28_ET_NEAR = 60.0   # m: an edge sample farther than this from the centreline is not on the Selinos's banks
SITE28_K_NEAR = 150.0   # m: a bridge K1-K6 this near the centreline is ticked on it (K1 crosses a side inlet)
SITE28_ET_COL = dict((t_, INK if t_ == "building" else EDGE[t_][1]) for t_ in EDGE)   # the bars' colours
SITE28_ET_WL = {1: INK2, 2: mix(INK2, PAPER, 0.5)}    # walled / embanked, as the DISCONNECTED bar
SITE28_ET_KEY = (("pedestrian", u"walkable"), ("street", u"street"), ("green", u"planted"), ("building", u"built"),
                 ("parking", u"parking"), ("open", u"loose"))


