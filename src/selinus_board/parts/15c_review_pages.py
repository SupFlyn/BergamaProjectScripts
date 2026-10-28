# ============================================================ v42 (Aras's deck review, 26 Oct 07:06)
# p.07 "The stream edge": a plan of what meets the water along each bank (the edge types the board already measures,
# every 4 m: build_edges), with walls, embankments, bridges, the cuts and the photo viewpoints, and the share of each
# edge type as one bar. p.09-11: every cut across the stream on ONE drawing at ONE round scale, on at most two booklet
# pages (Aras: "merge S1-S8 onto fewer pages, at a consistent scale"); a cut too long for a row is cropped to the part
# around the stream (global rule 2: crop, never stretch). Every drawing of these pages opens with a short context line
# (global rule 4: what it shows, why it is here, what to take from it).
CTX_H = 0.75            # page units: the context line's text height on a drawing about 120-140 units wide
BK_AW, BK_AH = 392.0, 238.0   # mm: the booklet's panel area on one page (bergama_booklet v4: A3 less margins, caption)
SEC_BOOK_DENS = (2500, 5000, 10000)   # the round booklet scales tried for the cuts, largest first (v45, Prompt 2: "keep
#                                      all eight sections at 1:2,500": the strips lost their locators, so 1:2,000 could fit)
SEC_KEEP = 0.7          # a cut is cropped to the part around the stream only if at least this share of it stays
SEC_COL_GAP = 2.0       # page units between two cuts side by side
SEC_ROW_GAP = 1.6       # page units between rows of cuts


def ctx_line(B, txt, x, y, w, h, L, font=None):
    """v42: a drawing's context line (1-2 sentences) under its title, from baseline y; returns the y below it. v47:
    in font (FONT_TITLE for the drawings whose words are all sans; default the body font, as before)."""
    return B.para(txt, x, y, w, h, INK2, L, lead=1.45, font=font)


def edge_shares(S):
    """v42: {edge type: % of the bank length}, and the % walled and embanked (the key question's measure)."""
    tot = sum(S.edge_len.values())
    if tot <= 0:
        return {}, 0.0, 0.0, 0.0
    return (dict((k, 100.0 * v / tot) for k, v in S.edge_len.items()), 100.0 * S.walled_len / tot,
            100.0 * getattr(S, "embanked_len", 0.0) / tot, tot)


def sec_cropped(S, sd_, Lmax):
    """v42: the part of a cut Lmax long around the stream (centred on its water, kept inside the cut), cut again by the
    same section engine; its title says which part of the whole it is."""
    x0, y0, x1, y1, nm = sd_["line"]
    L = sd_["L"]
    if sd_["water"]:
        c = 0.5 * (min(w_[0] for w_ in sd_["water"]) + max(w_[1] for w_ in sd_["water"]))
    else:
        c = 0.5 * L
    s0 = max(0.0, min(L - Lmax, c - 0.5 * Lmax))
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    out = section_of_line(S, x0 + ux * s0, y0 + uy * s0, x0 + ux * (s0 + Lmax), y0 + uy * (s0 + Lmax), nm)
    out["crop_of"] = (L, s0)
    return out


def typology_size(S, ss_t, th, U, enl=1.0):
    """v44: (width, height) in page units of the building types drawn at ss_t page units per metre, tags th high.
    v50 (P05.1): enl as draw_typology_key's."""
    yb = draw_typology_key(S, Board(), 0.0, 0.0, 1e9, U, ss=ss_t, th=th, crop=False, enl=enl)
    return getattr(draw_typology_key, "last_w", 0.0), -yb


def sections_plan(S, sw, U):
    """v42: (den, ss, pages): the largest round booklet scale 1:den at which every cut (cropped to the part around the
    stream where it is too long, keeping >= SEC_KEEP of it) fits on at most two booklet pages; pages = [[row, ...]],
    row = [(section, width)]. ss = page units per metre. v44 (Aras 27 Oct: "move the building types to p8 with the
    other sections"): the building types are one more item after the last cut (a dict with "_types"); without room,
    left out (logged). v45 (Prompt 2: neighbouring drawings at one scale): the types at the cuts' own scale; the
    strips without locators (each page has one key map, draw_sections_key). v50 (MIRAQUA 28 Oct, F12, P05.1): the
    cuts' words at the largest step of SITE28_SEC_TXT (booklet pt) at which they still fit as at the smallest one:
    the same scale and pages, S4 on the same page, the building types kept (set on each cut as c_["_txt"]); then the
    building types enlarged as a diagram (SITE28_TYPES_F) as far as that fit allows (the types item's "tf")."""
    secs = list(S.sections)
    hmax = sw * BK_AH / BK_AW * 0.97
    kb = sw / BK_AW                                   # board units per booklet mm
    th = bk_hk(7.5, kb, mono=True)                    # tags 7.5 pt on the booklet page
    nst = len(SITE28_SEC_TXT)
    best = None

    def pack(items):
        rows, cur, cw = [], [], 0.0                   # in order, side by side while they fit the width
        for it in items:
            if cur and cw + SEC_COL_GAP * U + it[1] > sw:
                rows.append(cur)
                cur, cw = [], 0.0
            cw += (SEC_COL_GAP * U if cur else 0.0) + it[1]
            cur.append(it)
        if cur:
            rows.append(cur)
        pages, ph = [[]], 4.0 * U                     # the first page also holds the context line
        for r in rows:
            rh = max(h_ for c_, w_, h_ in r) + SEC_ROW_GAP * U
            if pages[-1] and ph + rh > hmax:
                pages.append([])
                ph = 1.0 * U
            pages[-1].append(r)
            ph += rh
        ok = len(pages) <= 2 and all(max(h_ for c_, w_, h_ in r) + 5.0 * U <= hmax for r in rows)
        return [[[(c_, w_) for c_, w_, h_ in r] for r in pg] for pg in pages], ok
    for den in SEC_BOOK_DENS:
        ss = 1000.0 * sw / (den * BK_AW)             # the drawing fills the booklet's width: 1:den on the page
        end = site28_sec_end(SITE28_SEC_TXT[0], kb, U)    # v50: the ends' room for the largest words, at every step
        Lmax = (sw - 2.0 * end) / ss
        if any(sd_["L"] * SEC_KEEP > Lmax for sd_ in secs):
            continue
        cut = [sd_ if sd_["L"] <= Lmax else sec_cropped(S, sd_, Lmax) for sd_ in secs]
        tcache = {}

        def items_at(st):
            out = []
            for c_ in cut:
                c_["_txt"] = dict(step=st, k=kb, end=end)
                wi = min(sw, c_["L"] * ss + 2.0 * end)
                n0 = len(LOG)
                hi = -draw_section_strip(S, Board(), c_, 0.0, 0.0, wi, ss, U, dry=True, loc=False)
                del LOG[n0:]
                out.append((c_, wi, hi))
            return out

        def types_at(tf):
            if tf not in tcache:
                wt, ht = typology_size(S, ss * tf, th, U, tf)
                tcache[tf] = (dict(_types=True, name=u"building types", ss=ss * tf, th=th, den=den, tf=tf), wt,
                              ht + 0.6 * U) if 0.0 < wt <= sw else None
            return tcache[tf]
        ref = items_at(nst - 1)                      # the smallest words: the reference fit (about v49's)
        t1 = types_at(1.0)
        pages0, ok0 = pack(ref + ([t1] if t1 else []))
        has_t = ok0 and t1 is not None
        if not has_t:
            pages0, ok0 = pack(ref)
        best = (den, ss, pages0)
        if not ok0:
            continue
        p4 = site28_page_of(pages0, "S4")
        got = None
        for st in range(nst):                        # the largest words first, then the largest building types
            its = ref if st == nst - 1 else items_at(st)
            for tf in (SITE28_TYPES_F if has_t else (None,)):
                tt = types_at(tf) if tf else None
                if tf and tt is None:
                    continue
                pg_, ok_ = pack(its + ([tt] if tt else []))
                if ok_ and len(pg_) == len(pages0) and site28_page_of(pg_, "S4") == p4:
                    got = (st, tf or 1.0, pg_)
                    break
            if got:
                break
        st, tf, pages = got or (nst - 1, 1.0, pages0)
        for c_ in cut:
            c_["_txt"] = dict(step=st, k=kb, end=end)
        best = (den, ss, pages)
        LOG.append("Sections (F12, P05.1): the cuts' words at step {} of {} (names {head} pt, sentences and callouts "
                   "{call} pt, levels and tags {minor} pt, satellite rows {sat} pt){}; the building types {}.".format(
                       st + 1, nst, " (the smallest: larger words break the fit)" if st == nst - 1 else "",
                       "enlarged {:g} x (a diagram)".format(tf) if tf > 1.0 else "at the cuts' scale",
                       **SITE28_SEC_TXT[st]))
        if not has_t:
            LOG.append("Sections: the building types do not fit beside or under the cuts on two pages at "
                       "1:{:,}; drawn only as their own drawing (booklet crop drw_building_types).".format(den))
        if den != SEC_BOOK_DENS[0]:                  # v49.1 (Aras 27 Oct, Prompt 8): was silent
            LOG.append("WARNING: Sections: the cuts do not fit two booklet pages at 1:{:,}; drawn at 1:{:,} "
                       "(Aras: all cuts at 1:{:,}).".format(SEC_BOOK_DENS[0], den, SEC_BOOK_DENS[0]))
        return best
    LOG.append("WARNING: Sections: the cuts do not fit two booklet pages even at 1:{:,}.".format(SEC_BOOK_DENS[-1]))
    return best


def sections_context(S):
    """v42: the context line of the cuts, with the bed's depth below the banks over all cuts (computed). v50 (MIRAQUA
    28 Oct, P04.2, G5, G13, bank depth REPORT §4 1a-1e): bold keywords; the depth at each cut's main crossing below
    its lower bank crest (2 decimals), the crossings at the DSİ walls and those with no surveyed bed left out of the
    range, the walls named (WALL_H, site photos)."""
    d, kinds, wall = [], set(), False
    for sd_ in S.sections:
        wall = wall or any((b_ or {}).get("kind") == "wall" for b_ in sd_.get("banks") or [])
        k_ = site28_main_k(sd_)
        if k_ is None:
            continue
        cr, top = site28_bank_of(sd_, k_)
        if top is None or cr.get("kind") == "wall" or cr.get("nobed"):
            continue
        d.append(top - (sd_["water"][k_][2] + sd_["base"]))     # the water runs' beds are above the cut's base
        kinds.add(cr.get("kind", "ground"))
    if d:
        rng = (u"{:.2f}-{}".format(min(d), u_height(max(d))) if len(d) > 1 else u_height(d[0]))
        dep = u"the bed **{} below** the lower bank {}".format(rng, u"crest" if kinds == {"crest"} else u"top")
    else:
        dep = u"the bed below the banks"
    return (u"**{} cuts** · **one scale** · surveyed ground, bed, buildings at their floors, streets crossed · {}{}"
            u"".format(len(S.sections), dep, u" · **walls {} high** in the town reach (site photos, 1 Oct 2026)".format(
                u_height(WALL_H)) if wall else u""))            # v44: keywords (visual first)


def draw_sections_page(S, B, x, y, sw, U, plan, k):
    """v42: page k of the cuts (sections_plan): rows of whole cuts at one scale, the context line on the first page.
    v45: no locator and no scale word per cut (the caption states the one scale); the page's key map under it, its
    own crop for the booklet page's title band. Returns the y below. v50 (MIRAQUA 28 Oct, P04.1, P04.2, P05.1): the
    key maps at their booklet size (draw_sections_key, parts/15l), the context line's keywords bold, the building
    types enlarged as a diagram where sections_plan found room."""
    L = "LU_BOARD::Sections"
    den, ss, pages = plan
    names = [c_["name"] for r in pages[k] for c_, w_ in r if not c_.get("_types")]
    B.text(u"SECTIONS ACROSS THE STREAM · {}{} · 1:{:,} ON THE A3 PAGE".format(
        names[0], "" if len(names) == 1 else "-" + names[-1], den), x, y, 0.9 * U, INK, L, font=FONT_TITLE, bold=True)
    top = y - 1.3 * U if k == 0 else y - 1.8 * U
    # v50 (MIRAQUA 28 Oct, P04.2, G5): the context line with its keywords bold
    yy = site28_para(B, sections_context(S), x, top, sw, CTX_H * U, INK2, L, lead=1.45, bcol=INK) - 0.4 * U \
        if k == 0 else top
    low = yy
    for r in pages[k]:
        cx = x
        rl = yy
        for c_, w_ in r:
            if c_.get("_types"):                         # v44: the building types, at their own round scale
                # v50 (P05.1): enlarged as a diagram by sections_plan's tf
                bot = draw_typology_key(S, B, cx, yy, w_, U, ss=c_["ss"], th=c_["th"], crop=False,
                                        enl=c_.get("tf", 1.0))
            else:                                        # v44: the sheet's own scale; the booklet prints 1:den
                bot = draw_section_strip(S, B, c_, cx, yy, w_, ss, U, tag="drawing", scale_txt="", loc=False)
            rl = min(rl, bot)
            cx += w_ + SEC_COL_GAP * U
        yy = rl - SEC_ROW_GAP * U
        low = rl
    crop_panel("sections_%d" % (k + 1), x, low - 0.2 * U, x + sw, (top + CTX_H * U + 0.3 * U) if k == 0 else top + 0.9 * U,
               u"Sections across the stream · {}{}".format(", ".join(names), next((
                   u" · building types" + (u" (diagram, enlarged)" if c_.get("tf", 1.0) > 1.0 else u"")
                   for r in pages[k] for c_, w_ in r if c_.get("_types")), u"")), crop_scale(ss))   # v50 (P05.1)
    low = draw_sections_key(S, B, x, low - 1.6 * U, sw, names, k)
    if k == len(pages) - 1 and any(c_[4] == "S4" for c_ in S.sec_lines):   # v48: the water board's S4 pages' key map
        low = draw_sections_key(S, B, x, low - 1.6 * U, sw, ["S4"], "s4")
    return low
