# ---- 40_set (composer core, round 5 S1; G-R5-2, D1, C8, C12): the text setter -----------------------------------------
# Every paragraph, list text and caption is JUSTIFIED with its LAST line LEFT (refs/U29 sketch); single lines stay left.
# Widths are real Arial (font_metrics, the same files the page embeds: 10_load bk_font_files). Sizes start at the
# role's size (grid.py GRID_ROLE_PT) and step down 0.25 pt until the text fits its box, never below GRID_MIN_PT
# (4.0 pt, D1); what still does not fit is a WARNING "overrun" and is set at 4 pt running past its box (the layout
# check reports the edge). No widows: the last line keeps >= 2 words (tp_wrap pulls words down; when that fails at
# this size the next smaller size is tried; at 4 pt a WARNING "widow"). Words are placed one by one at their
# justified x, so no PDF word spacing is needed (PyMuPDF writes Identity-H text, where Tw does not apply).
# C8 (round 4: a renumbered source mark squeezed to 6 pt "may touch the next word"): marks are now ordinary text in
# their paragraph, set and measured with it; nothing is squeezed into a frozen sheet layout.
#   st_lines(text, w, pt, bold=False, justify=True) -> [line]   line = dict(words=[(s, bold, x_mm)], width, last)
#         paragraphs split at "\n"; "*word*" bold; x_mm already justified (last line of each paragraph left)
#   st_fit(text, w, h, role="intro", pt=None, bold=None, lead=None, justify=True, min_pt=None) ->
#         (lines, pt, lead_mm, height_mm)      the largest size <= pt at which the text fits w x h mm (h None = any)
#   st_para(P, text, x, y, w, h=None, role="intro", pt=None, bold=None, colour=None, justify=True, name=None,
#           allow=(), group=None, page=None) -> (height_mm, pt)
#         sets a paragraph block with its TOP at y (page mm, y down) into P's TextPage (drawn by bk_emit at the end)
#   st_line(P, s, x, y, pt, bold=False, colour=None, align="L", role="label", name=None, allow=(), group=None)
#         one line, baseline at y (no wrapping), through the TextPage
#   bk_emit(P) -> n                            draws every text of the page (TextPage.emit) with the page's fonts
#   ST_COUNT                                   dict(justified=n paragraphs justified, lines=n): log "text justified n"
ST_COUNT = dict(justified=0, lines=0, paras=0)


def st_lines(text, w, pt, bold=False, justify=True, min_last_words=2):
    """see the part notes; raises TpWidow when the last-line rule cannot hold at this size"""
    sp = fm_width(u" ", pt, False)
    out = []
    for para in (u"%s" % text).split(u"\n"):
        if not para.strip():
            out.append(dict(words=[], width=0.0, last=True))
            continue
        lines = tp_wrap(para, w, pt, bold, min_last_words, True)
        lines = [ln for ln in lines if ln]
        for i, ln in enumerate(lines):
            words, x = [], 0.0
            for s, b, xo in ln:                       # a run: words of one weight; xo = where the run starts
                x = xo
                for j, wd in enumerate(s.split(u" ")):
                    if j > 0:
                        x += sp
                    words.append([wd, b, x])
                    x += fm_width(wd, pt, b)
            # the extra space goes only into real word spaces: a word glued to the one before (a bold word and its
            # comma, two runs without a space) keeps its place relative to it
            nat = x
            last = (i == len(lines) - 1)
            gaps = []
            for k in range(1, len(words)):
                prev_end = words[k - 1][2] + fm_width(words[k - 1][0], pt, words[k - 1][1])
                gaps.append(words[k][2] - prev_end > 1e-6)
            n_sp = sum(1 for g in gaps if g)
            if justify and not last and n_sp > 0 and nat < w:
                extra = (w - nat) / float(n_sp)
                add = 0.0
                for k in range(1, len(words)):
                    if gaps[k - 1]:
                        add += extra
                    words[k][2] += add
                ST_COUNT["lines"] += 1
            out.append(dict(words=[(s_, b_, xo_) for s_, b_, xo_ in words],
                            width=(w if justify and not last and n_sp and nat < w else nat), last=last))
    return out


def st_fit(text, w, h, role="intro", pt=None, bold=None, lead=None, justify=True, min_pt=None, page=None):
    p0, b0, ld0, _c = grid_role(role)
    pt = float(pt or p0)
    bold = b0 if bold is None else bool(bold)
    lo = float(min_pt or GRID_MIN_PT)
    lines, used = None, pt
    s = pt
    while True:
        lead_mm = (lead / pt * s) if lead else s * ld0 * GRID_PT
        try:
            lines = st_lines(text, w, s, bold, justify)
            hh = _st_height(lines, s, lead_mm, bold)
            if h is None or hh <= h + 1e-6:
                return lines, s, lead_mm, hh
        except TpWidow:
            pass
        if s - 0.25 < lo - 1e-6:
            break
        s -= 0.25
    s = lo
    lead_mm = (lead / pt * s) if lead else s * ld0 * GRID_PT
    try:
        lines = st_lines(text, w, s, bold, justify)
    except TpWidow as ex:
        wn_warn(page, "widow", u"%r: %s (set without the last-line rule)" % (grid_plain(text)[:50], ex))
        lines = st_lines(text, w, s, bold, justify, 1)
    hh = _st_height(lines, s, lead_mm, bold)
    if h is not None and hh > h + 1e-6:
        wn_warn(page, "overrun", u"%r needs %.1f mm at %.1f pt, %.1f mm free: cut the text or give it room" % (
            grid_plain(text)[:50], hh, s, h))
    return lines, s, lead_mm, hh


def _st_height(lines, pt, lead_mm, bold):
    if not lines:
        return 0.0
    a, d = fm_asc_desc(pt, bold)
    return a + (len(lines) - 1) * lead_mm - d


def st_para(P, text, x, y, w, h=None, role="intro", pt=None, bold=None, colour=None, justify=True, name=None,
            allow=(), group=None, page=None, lead=None):
    p0, b0, _ld, c0 = grid_role(role)
    bold = b0 if bold is None else bool(bold)
    lines, s, lead_mm, hh = st_fit(text, w, h, role, pt, bold, lead, justify, page=page or P.pid)
    a, _d = fm_asc_desc(s, bold)
    g = group or P.tp._group()
    yy = y + a
    for ln in lines:
        for wd, b, xo in ln["words"]:
            if wd:
                P.tp.put(wd, x + xo, yy, s, b, "L", 0.0, name, role, colour or c0, allow, g)
        yy += lead_mm
    ST_COUNT["paras"] += 1
    if justify and len([l for l in lines if l["words"]]) > 1:
        ST_COUNT["justified"] += 1
    return hh, s


def st_line(P, s, x, y, pt, bold=False, colour=None, align="L", role="label", name=None, allow=(), group=None,
            angle=0.0):
    return P.tp.put(s, x, y, pt, bold, align, angle, name, role, colour or GRID_INK["ink"], allow, group)


def bk_emit(P):
    """every text of the page drawn with the page's embedded Arial (the files it was measured with)"""
    import fitz as _fz
    if not getattr(P, "_fonts", False):
        r, b = bk_font_files()
        xr = {"BKR": P.page.insert_font(fontname="BKR", fontfile=r),
              "BKB": P.page.insert_font(fontname="BKB", fontfile=b)}
        _ins0 = P.page.insert_font

        def _ins(fontname="helv", fontfile=None, **kw):       # v32.4: PyMuPDF looked the font up again for EVERY
            k = fontname[1:] if fontname.startswith("/") else fontname   # text by scanning all the page's
            if k not in xr:                                   # resources, inside each embedded drawing too (p02:
                xr[k] = _ins0(fontname=fontname, fontfile=fontfile, **kw)   # 10+ min); the xref is the same each
            return xr[k]                                      # time, so it is kept after the first look-up
        P.page.insert_font = _ins
        P._fonts = True

    def draw(it):
        s, pt, bold = it["text"], it["pt"], it["bold"]
        w = fm_width(s, pt, bold)
        al = str(it.get("align") or "L").upper()
        x, y = it["x"], it["y"]
        if al in ("MC", "CM"):
            ix0, iy0, ix1, iy1 = fm_ink_box(s, pt, bold)
            dx, y = -w / 2.0, y + (iy0 + iy1) / 2.0
        else:
            dx = {"L": 0.0, "C": -w / 2.0, "R": -w}.get(al[:1], 0.0)
        col = hex_rgb(it.get("colour") or GRID_INK["ink"])
        ang = float(it.get("angle") or 0.0)
        if abs(ang) > 0.01:
            import math as _m
            t = _m.radians(ang)
            pp = _fz.Point((x + dx * _m.cos(t)) * BK_K, (y - dx * _m.sin(t)) * BK_K)
            P.page.insert_text(pp, s, fontname="BKB" if bold else "BKR", fontsize=pt, color=col,
                               morph=(pp, _fz.Matrix(-ang)))
        else:
            P.page.insert_text(_fz.Point((x + dx) * BK_K, y * BK_K), s, fontname="BKB" if bold else "BKR",
                               fontsize=pt, color=col)
    return P.tp.emit(draw)
