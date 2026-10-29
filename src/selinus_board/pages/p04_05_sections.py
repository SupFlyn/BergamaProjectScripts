# p.04-05 sections across the stream (split from parts/14_tsec_wind_arrows.py, parts/15_ndvi_col.py, parts/15c_review_pages.py, parts/15l_r28_site.py on 29 Oct 2026; moved unchanged)


# v50 (MIRAQUA 28 Oct, P04.2): section_caption is gone (the cut's header is site28_sec_reading's key sentence)
def draw_locator(S, B, x, ytop, w, U, L, lines_):
    F = S.F
    V, mw, mh = view_fit(F, x, ytop, w, w * F.h / F.w)
    B.fill([V.P(F.P)], PAPER, L, 2)
    for wt in S.water:
        B.fill(V.Ps([wt["P"]] + wt.get("H", [])), BLUE_L, L, 8)
    mini_buildings(S, B, V, L, lambda u: FAINT)
    for (x0, y0, x1, y1, nm) in lines_:
        B.line([V.p(x0, y0), V.p(x1, y1)], INK, L, 15, 0.28)
        bx, by = V.p(x0, y0)
        B.text(nm, bx + 0.2 * U, by + 0.15 * U, 0.3 * U, INK, L, font=FONT_TITLE, bold=True)
    B.line(V.P(F.P + [F.P[0]]), INK2, L, 16, 0.06)
    draw_north_small(B, V, mw, mh, U, L, size=0.38)
    return ytop - mh


def draw_section_strip(S, B, sd_, x, y, w, ss, U, dry=False, tag="page", scale_txt=None, loc=True):
    """One long section: the surveyed ground, the bed, the buildings at their heights; behind the cut a picture of what
    the section sees (buildings and ground beyond, trees at their measured size, scale figures). v45: loc=False draws
    no locator (the sections page has one key map); scale_txt="" writes no scale word (the page states one).
    v50 (MIRAQUA 28 Oct, P04.2, F12, G4, G13): the header is the cut's name, one key sentence with bold keywords and
    what on the cut steers the project (site28_sec_reading; was a caption of figures, section_caption); every word at
    the sizes of the cut's step (sd_["_txt"], set by sections_plan; SITE28_SEC_TXT), placed by its real width; the
    callouts by priority on at most SITE28_SEC_TIERS rows (site28_callouts: the water always, then edges and history,
    then streets and places); levels and heights in m with 2 decimals, horizontal dimensions in cm; the cut's length
    is no longer printed (its scale bar gives it) and the width dimension over the water is gone (its callout says
    the bed width where the cut crosses the stream)."""
    L = "LU_BOARD::Sections"
    nm = sd_["name"]
    Lm = sd_["L"]
    pk, pn = sd_.get("part", (1, 1))
    off = sd_.get("s_off", 0.0)
    hd, hc, hm, hs, end = site28_sec_sizes(sd_, U)
    locw = min(9.0 * U, 0.22 * w) if loc else 0.0
    gq = sd_["ground"]                                   # v50: room over the drawing for the end names (over their
    need = max([0.38 * U + hm + hd - (sd_["zmax"] - g_[1]) * ss for g_ in (gq[0], gq[-1])] +     # levels) and tags
               ([0.12 * U + hm - 1.0 * ss] if sd_["bld"] else []))
    if pk == 1:
        # ---- header: the name, the key sentence, what steers the project; a locator with north arrow (loc)
        tw_ = w - locw - (0.6 * U if loc else 0.0)
        co = sd_.get("crop_of")                          # v42: a cut cropped to the part around the stream
        tx_ = site28_text(B, u"**SECTION {0} — {0}'**".format(nm), x, y, hd, INK, L)[1]
        if pn > 1 or co:
            site28_text(B, u" · in {} parts".format(pn) if pn > 1 else u" · the part around the stream", tx_, y, hd,
                        INK2, L)
        key_, steer_ = site28_sec_reading(S, sd_.get("whole", sd_) if pn > 1 else sd_)
        cy = y - 0.45 * hd - 1.3 * hc
        for t_, c_ in ((key_, INK), (steer_, INK2)):
            if t_:
                cy = site28_para(B, t_, x, cy, tw_, hc, c_, L, lead=1.5, bcol=INK)
        last = cy + 1.2 * hc                             # the last line's foot
        if loc:
            lb = draw_locator(S, B, x + w - locw, y + 0.55 * U, locw, U, L, [sd_["line"]])
            top = min(last, lb - 1.2 * U) - 0.35 * U - max(0.0, need)
        else:
            top = last - 0.35 * U - max(0.0, need)
    else:
        site28_text(B, u"**SECTION {0} — {0}'** · continued".format(nm), x, y, hd, INK2, L)
        top = y - 0.3 * hd - 0.35 * U - max(0.0, need)
    X0 = x + max(end, (w - Lm * ss) / 2.0)
    Y0 = top - sd_["zmax"] * ss

    def P(px, pz):
        return (X0 + px * ss, Y0 + pz * ss)

    def g_at(s):
        return sd_["ground"][max(0, min(len(sd_["ground"]) - 1, int(round(s / 0.5))))][1]
    # ---- the picture behind the cut
    if not dry:
        png = sec_art_png(S, sd_, ss, tag)
        if png:
            path, zlo_a, zhi_a = png
            base = sd_["base"]
            B.image(path, X0, Y0 + (zlo_a - base) * ss, X0 + Lm * ss, Y0 + (zhi_a - base) * ss, L, 5)
    tags_ = sec_cut(B, L, sd_, P, Lm, ss, U, dry)
    road_calls = draw_sec_roads(S, B, L, P, g_at, sd_["line"], Lm, U, off=off)   # v25: the streets crossed
    # ---- annotation: end levels and names, the tallest roof's level, callouts below (v50: no width dimension)
    for s, zl, za, kind in sd_["levels"]:
        if kind != "end":
            continue
        bx, by = P(s, zl)
        B.fill([[(bx, by), (bx - 0.22 * U, by + 0.38 * U), (bx + 0.22 * U, by + 0.38 * U)]], INK, L, 36)
        t_ = u_level(za)                                 # outside the strip, clear of the buildings at the ends
        site28_text(B, t_, bx + 0.4 * U if s >= Lm * 0.5 else bx - 0.4 * U - site28_tw(t_, hm), by + 0.08 * U, hm,
                    INK, L)
    g0, g1 = sd_["ground"][0], sd_["ground"][-1]
    for px_, pz_, lab, out, real in ((g0[0], g0[1], nm, -1.0, pk == 1), (g1[0], g1[1], nm + "'", 1.0, pk == pn)):
        bx, by = P(px_, pz_)
        if real:                                         # over its end level
            site28_text(B, u"**{}**".format(lab), bx + out * 0.4 * U, by + 0.38 * U + hm, hd, INK, L,
                        align="L" if out > 0 else "R")
        else:                                            # where the parts meet
            B.line([(bx, by - 0.9 * U), (bx, by + 1.2 * U)], INK2, L, 36, 0.05)
            site28_text(B, u"continues below" if out > 0 else u"continued from above", bx - out * 0.3 * U,
                        by + 0.95 * U, hm, INK2, L, align="R" if out > 0 else "L")
    # the tallest cut roof: its level, as on an architectural section
    if sd_["bld"]:
        a, b, z0, z1, cat, annex, ftype, fl, floors, fsrc = max(sd_["bld"], key=lambda t: t[3])
        lev_ = u_level(z1 + sd_["base"])
        lw_ = site28_tw(lev_, hm)
        for side in ((1.0, -1.0) if (b - a) * ss > 0.6 * U else ()):
            bx, by = P(b if side > 0 else a, z1)         # v16.3: at the eaves beside the wall, clear of the type's tag
            bx += side * 0.4 * U
            t0, t1 = (bx - 0.16 * U, bx + 0.25 * U + lw_) if side > 0 else (bx - 0.25 * U - lw_, bx + 0.16 * U)
            if any(t0 < x1_ and x0_ < t1 and -(hm + 0.2 * U) < y_ - by < hm + 0.2 * U for x0_, x1_, y_ in tags_):
                continue                                 # v40: never over a building's tag; else the other wall
            B.line([(bx - side * 0.4 * U, by), (bx + side * 0.16 * U, by)], INK, L, 36, 0.04)
            B.fill([[(bx, by), (bx - 0.16 * U, by + 0.28 * U), (bx + 0.16 * U, by + 0.28 * U)]], INK, L, 36)
            site28_text(B, lev_, bx + 0.25 * U if side > 0 else bx - 0.25 * U - lw_, by + 0.06 * U, hm, INK, L)
            break
    # v40 (Aras 25 Oct): the words at the water in one clean band right under the cut ground, each on a short leader
    # to its bank or bed point; no word on the drawing's ink, none over another; caveats go to the log, not the page.
    # v50 (P04.2, G4): by priority, at most SITE28_SEC_TIERS rows: the water (0), edges and history (1), named
    # streets with the length the cut runs on them in cm (2), other streets and places (3); the rest left out
    calls = list(sec_water_calls(sd_, g_at, nm, dry)) + [(s, g_at(s), t, 1) for s, t in sec_edge_calls(sd_)]
    calls += [((a + b) / 2.0, g_at((a + b) / 2.0), nm_, 3) for a, b, nm_ in sd_.get("places", [])]   # v16.7
    for s_, z_, t_ in road_calls:                        # v25: every street crossed
        c_ = site28_road_call(t_)
        calls.append((s_, z_, c_[0], c_[1]))
    calls += [(s_, g_at(s_), t_, 1) for s_, t_ in sec_history_calls(S, sd_) if 0.0 <= s_ <= Lm]   # v44
    low, left_ = site28_callouts(B, L, P, calls, P(0, -3.0)[1] - 0.45 * U, U, hc, x, x + w)
    if left_ and not dry:
        LOG.append(u"Section {}: {} callout(s) left out, no free row under the cut: {}.".format(nm, len(left_),
                                                                                             u"; ".join(left_)))
    # the use ribbon and the satellite rows under the callouts
    rib = low - 0.3 * hc - 0.35 * U
    for a, b, cat in sd_["strip"]:
        B.fill([rect(P(a, 0)[0], rib - 0.16 * U, P(b, 0)[0], rib)], CAT[cat][1], L, 20)
    rib_low = rib - 0.16 * U
    if "_sat" not in sd_:
        sd_["_sat"] = section_sat(sd_)
    if sd_["_sat"]:                                      # v33: land cover and greenness from satellite, metre by metre
        rib_low = draw_sat_strips(B, sd_["_sat"], P, Lm, rib_low, x, U, L, th=hs)
    sb = nice_floor(Lm / 4.0)
    xb = X0 + Lm * ss - sb * ss - 0.9 * U
    yb = rib_low - 0.73 * U - hm - 0.25 * U              # the bar's numbers sit over it, hm high
    draw_scalebar(B, xb, yb, ss, sb, U, L, h=hm / U)
    ratio = 1000.0 / max(1e-9, ss * MMU)
    if scale_txt != "":                                  # v45: "" = the page states the one scale
        B.text(scale_txt or "1:{:,.0f} at {:.0f} mm".format(nice_ratio(ratio), SHEET_MM), X0, yb + 0.1 * U,
               hm, INK2, L)                              # v42: the cuts' common scale on the booklet page
    return yb - 0.35 * U


def sec_water_calls(sd_, g_at, nm, dry=False):
    """v40: the stream's callouts in a section: its width and depth at the water, its bed level and depth below the
    lower bank at the bed; [(s, z, text)] (text <= 30 characters). Where a figure is interpolated or approximate the
    log says so (not the page). v50 (MIRAQUA 28 Oct, bank depth REPORT §4 1a-1e, G13): [(s, z, text, priority 0)]:
    the bed width in cm only where the cut crosses the stream at SITE28_CROSS° or more (1c); the water "approx."
    unless measured (1d); the bed level and its depth below the lower bank crest (1a), or between the DSİ walls
    (WALL_H, photos) in the walled town reach (1b), or "bed not surveyed" (1e); there the survey's crest, labelled
    "survey, before the DSİ walls" (Aras 28 Oct 14:12). Levels and heights in m, 2 decimals."""
    out, notes = [], []
    srcs = sd_.get("bed_src") or ["surveyed"] * len(sd_["water"])
    wsrc_ = sd_.get("water_src") or [WATER_SRC] * len(sd_["water"])
    base = sd_["base"]
    for k, ((a, b, bed, lvl), src, ws_) in enumerate(zip(sd_["water"], srcs, wsrc_)):
        cr, zb = site28_bank_of(sd_, k)
        dep = lvl - bed
        wt = []
        if cr.get("ang", 90.0) >= SITE28_CROSS:
            wt.append(u"bed {} wide".format(u_dim(cr.get("w", b - a))))
        if dep > 0.005:
            wt.append((u"water " if ws_ == "measured" else u"water approx. ") + u_height(dep))
        elif ws_ != "approx":
            wt.append(u"no water")
        if wt:
            out.append((a + (b - a) / 3.0, lvl if dep > 0.005 else bed, u" · ".join(wt), 0))
        btxt = u"bed not surveyed" if cr.get("nobed") else u"bed " + u_level(bed + base)
        if cr.get("kind") == "wall":
            btxt += u" · walls {} (photos)".format(u_height(WALL_H))
        elif zb is not None and not cr.get("nobed"):
            btxt += u" · {} below {}".format(u_height(zb - (bed + base)), u"crest" if cr.get("kind") == "crest" else
                                             u"bank")
        out.append((a + 2.0 * (b - a) / 3.0, bed, btxt, 0))
        if cr.get("town"):                                # the survey's bank top, from before the walls
            pt_ = min(cr.get("pts") or [(a, cr["survey"])], key=lambda q: q[1])
            out.append((pt_[0], pt_[1] - base, u"survey {} {}, before the DSİ walls".format(
                u"crest" if cr.get("crest") is not None else u"bank", u_level(cr["survey"])),
                0 if cr.get("kind") == "crest" else 1))
        if not dry and cr.get("kind") == "wall":
            notes.append(u"Section {}: the bank top is the DSİ walls, {} above the bed (wall_height; site photos 1 Oct "
                         u"2026, 4-6 m): the survey's {} {} is from before the walls.".format(
                             nm, u_height(WALL_H), u"crest" if cr.get("crest") is not None else u"bank top",
                             u_level(cr["survey"])))
        if not dry and (src != "surveyed" or ws_ in ("approx", "input")):
            notes.append("Section {}: {}{}.".format(nm, {"interpolated": "bed level interpolated along the stream from the "
                                                                      "surveyed depths", "input": "bed from the "
                                                                      "channel_depth input", "terrain": "no bed level "
                                                                      "surveyed here (terrain)"}.get(src, "bed surveyed"),
                                                   {"approx": "; water depth approximate, not measured",
                                                    "input": "; water depth from the water_depth input"}.get(ws_, "")))
    for t_ in notes:
        if t_ not in LOG:
            LOG.append(t_)
    return out


def sec_history_calls(S, sd_):
    """v44 (PHASE2_SPEC §3, p.7-8): where a cut crosses the survey's historic city wall line (layer SINIR_TARIHI_SUR,
    S.walls_hist) or the covered course of the stream (OSM tunnel / culvert, S.covered): [(s, text)] along the cut.
    Only what the data holds: the survey layer does not date the wall, so no period is named."""
    x0, y0, x1, y1, nm = sd_["line"]
    Lc = math.hypot(x1 - x0, y1 - y0)
    if Lc <= 0:
        return []
    out = []
    for key, txt in (("walls_hist", u"historic city wall"), ("covered", u"covered stream")):
        for P in getattr(S, key, None) or []:
            for a, b in zip(P[:-1], P[1:]):
                hit = seg_x((x0, y0), (x1 - x0, y1 - y0), a, (b[0] - a[0], b[1] - a[1]))
                if hit:
                    s_ = hit[0] * Lc
                    if all(abs(s_ - q) > 3.0 or t_ != txt for q, t_ in out):
                        out.append((s_, txt))
    return out


# v50 (MIRAQUA 28 Oct, G13): sec_road_text is gone (site28_road_call: the length in cm, a priority)
def sec_edge_calls(sd_):
    """v40: the bank edges where the section meets the water: [(s, text)], e.g. "loose edge · embanked"."""
    return [(s, short(EDGE[typ][0]).lower() + {1: " · walled", 2: " · embanked"}.get(wl, ""))
            for s, typ, wl, gzz in sd_["labels"]]


def ndvi_col(v):
    return next(c for t, c in NDVI_STEPS if v < t)


def section_sat(sd_):
    """The pack's satellite rows for this section (or this part of it): {row: [colour per metre]} or None."""
    x0, y0, x1, y1 = sd_["line"][:4]
    L = sd_["L"]
    best = None
    for ps in seam_pack().get("sections", []):
        (ax, ay), (bx, by) = ps["a"], ps["b"]
        dx, dy = bx - ax, by - ay
        n = math.hypot(dx, dy) or 1.0
        off = max(abs(((px - ax) * dy - (py - ay) * dx) / n) for px, py in ((x0, y0), (x1, y1)))
        if off < 2.0 and (best is None or off < best[0]):
            best = (off, ps, dx / n, dy / n)
    if best is None:
        return None
    _, ps, ux, uy = best
    ax, ay = ps["a"]
    clc, nd = ps.get("clc") or [], ps.get("ndvi") or {}
    ex, ey = (x1 - x0) / (L or 1.0), (y1 - y0) / (L or 1.0)
    rows = dict((k, []) for k, _ in SAT_ROWS)
    for s in range(int(L) + 1):
        px, py = x0 + ex * s, y0 + ey * s
        i = int(round((px - ax) * ux + (py - ay) * uy))
        ok = 0 <= i < len(clc)
        rows["clc"].append(CLC_COL.get(int(clc[i])) if ok and clc[i] else None)
        for k in ("jan", "jul"):
            v = nd.get(k) or []
            rows[k].append(ndvi_col(v[i] / 1000.0) if 0 <= i < len(v) and v[i] is not None else None)
    return rows


def draw_sat_strips(B, rows, P, Lm, ytop, x, U, L, th=None):
    """The satellite rows under the use ribbon, named at the left; returns the y below them. v50 (MIRAQUA 28 Oct,
    F12): th = the names' capital height (the rows as tall as their names, the names right-aligned by their real
    width); without it as before."""
    h, g = (0.24 * U if th is None else max(0.24 * U, 1.15 * th)), 0.06 * U
    y = ytop - g
    for k, lab in SAT_ROWS:
        vals = rows[k]
        a = 0
        while a < len(vals):
            b = a
            while b + 1 < len(vals) and vals[b + 1] == vals[a]:
                b += 1
            if vals[a] is not None:
                B.fill([rect(P(a, 0)[0], y - h, P(min(Lm, b + 1), 0)[0], y)], vals[a], L, 20)
            a = b + 1
        if th is None:
            B.text(lab, P(0, 0)[0] - 0.25 * U, y - h * 0.85, 0.18 * U, INK2, L, align="R")
        else:
            B.text(lab, P(0, 0)[0] - 0.25 * U - site28_tw(lab, th), y - 0.5 * (h + th), th, INK2, L, font=FONT_TITLE)
        y -= h + g
    return y


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
