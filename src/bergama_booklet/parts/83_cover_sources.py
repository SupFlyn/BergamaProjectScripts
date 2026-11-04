# ---- 83_cover_sources (round 5 S10; round 6 S9 v31: G6-2 contents, G6-3 Sources last): the two pages the booklet draws
# v31: contents list the 22 pages of PLAN §2.1 from BK_PAGES (Sources = page 22, the last row of part E); the Sources
# page has the v31 title band, four text columns (five when four would need < 4.5 pt), entries "[n] text" numbered in
# page order with a hanging indent, left-aligned (lists, not justified), 4.5-5 pt (frames_p14-22 "new page 22").
# Cover (P01.1): the cover photo (Data/COVER_IMG) fills the WHOLE page behind everything (full bleed, proportions kept,
# the overflow cut by the page edge) under a white veil of COVER_VEIL opacity, so the photo shows very light and the
# text stays readable. Left: course, MIRAQUA, title, subtitle, the approved text, names, date. Right (P01.2): contents
# of the 22 pages (theme, stage, page title with its number).
# Sources: every source cited on a page ({src:key} marks and the scripts' page source rows), numbered in page order as
# the pages print them (81_ids bk_src_number), then the masterplan's numbered places, the relief's height data and the
# assets (scale figures, silhouettes, cutouts) once each, under their headings (round 4 rules kept).
BK_ASSET_SOURCES = [
    u"Scale figures: Wijayarathna S., Architectural human figures sketches (set 1), https://sashx.gumroad.com/l/gSAgZ",
    u"Scale figures: studio_articulation, Sketchy Human Figures 2, "
    u"https://learnarchitecture.online/products/sketchy-human-figures-2",
    u"Scale figures: studio_articulation, Sketchy Human Figures 3, "
    u"https://learnarchitecture.online/products/sketchy-human-figures-3"]          # v21-v29 list, unchanged
ELEV_SOURCES = [
    u"Site survey, Bergama (course file), contours 1-10 m: the ground inside the site frame",
    u"Copernicus DEM GLO-30, ESA / DLR / Airbus, TanDEM-X 2011-2015; https://dataspace.copernicus.eu/explore-data/"
    u"data-collections/copernicus-contributing-missions/collections-description/COP-DEM; © DLR e.V. 2010-2014 and © "
    u"Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA"]   # v25-v29


def bk_cover(doc, n, lines):
    import fitz as _fz
    P = bk_page(doc, "p01", n)
    W_, H_ = GRID_PAGE
    path = os.path.join(BERGAMA_ROOT, "Data", COVER_IMG)
    if os.path.isfile(path):
        try:
            pm = _fz.Pixmap(path)
            pw, ph = float(pm.width), float(pm.height)
            pm = None
            s = max(W_ / pw, H_ / ph)
            iw, ih = pw * s, ph * s
            x0, y0 = (W_ - iw) / 2.0, (H_ - ih) / 2.0
            P.page.insert_image(_fz.Rect(x0 * BK_K, y0 * BK_K, (x0 + iw) * BK_K, (y0 + ih) * BK_K), filename=path,
                                keep_proportion=False)
            sh = P.page.new_shape()
            sh.draw_rect(P.page.rect)
            sh.finish(color=None, fill=(1, 1, 1), fill_opacity=COVER_VEIL)
            sh.commit()
            P.ink.append(("photo", (0.0, 0.0, W_, H_), "cover"))
            lines.append(u"cover photo %s full bleed, veil %.2f (photo at %.0f %%)" % (COVER_IMG, COVER_VEIL,
                                                                                       100 * (1 - COVER_VEIL)))
        except Exception as ex:
            wn_warn("p01", "photo", u"cover photo %s unreadable (%s)" % (COVER_IMG, type(ex).__name__))
    else:
        wn_warn("p01", "photo", u"cover photo missing: copy %s into Downloads/Bergama/Data/" % COVER_IMG)
    ink, acc = GRID_INK["ink"], GRID_INK["accent"]
    x = GRID_ML
    lw = 225.0
    st_line(P, BOOK["course"].upper(), x, 18.0, 8.0, True, acc, role="title")
    st_line(P, BOOK["hook"], x, 64.0, 48.0, True, acc, role="title")
    y = 82.0
    hh, _s = st_para(P, BOOK["title"], x, y - 8.0, lw, 24.0, "title", pt=24.0, bold=True, justify=False)
    y += hh
    st_line(P, BOOK["subtitle"], x, y + 6.0, 14.0, False, ink, role="title")
    y += 16.0
    hh, _s = st_para(P, COVER_TEXT, x, y, 205.0, 40.0, "intro", pt=9.5)
    yb = 250.0
    for nm in BOOK["names"]:
        st_line(P, nm, x, yb, 9.5, False, ink, role="intro")
        yb += 4.4
    st_line(P, BOOK["date"], x, 272.0, 7.5, False, GRID_INK["ink2"], role="caption")
    # contents (P01.2, G6-2): from column 9 (x = 14 + 8 x 33 = 66.2 % as SON), 22 pages
    cx = GRID_ML + 8 * 33.0
    st_line(P, u"CONTENTS", cx, 18.0, 8.0, True, acc, role="title")
    rows, last, lst = [], None, None
    for i, sp in enumerate(BK_PAGES, 1):
        if i == 1:
            continue
        if sp.get("kind") == "sources":          # v31: the last row of part E (frames_p01-08 page 1 target)
            rows.append(("title", sp["title"], i))
            continue
        if sp.get("part") != last:
            last, lst = sp.get("part"), None
            if rows:
                rows.append(("gap", None, None))
            rows.append(("part", (last + u"  " + PARTS.get(last, u"")).upper(), None))
        if sp.get("stage") != lst:
            lst = sp.get("stage")
            rows.append(("stage", STAGES.get(lst, u""), None))
        rows.append(("title", sp["title"], i))
    step = dict(part=5.2, stage=4.4, title=4.4, gap=3.0)
    need = sum(step[k] for k, _t, _n in rows)
    f = max(1.0, min(1.35, (272.0 - 30.0) / need)) if need else 1.0
    cy = 30.0
    for k, t, no in rows:
        if k == "part":
            st_line(P, t, cx, cy, 8.0, True, acc, role="title")
        elif k == "stage":
            st_line(P, t, cx + 9.0, cy, 6.5, True, "5C7A86", role="heading")
        elif k == "title":
            st_line(P, u"%d" % no, cx + 6.0, cy, 7.0, True, GRID_INK["ink2"], "R", role="list_item")
            st_line(P, t, cx + 9.0, cy, 7.0, False, ink, role="list_item")
        cy += step[k] * f
    if cy > 276.0:
        wn_warn("p01", "overrun", u"contents run to %.0f mm, past the margin" % cy)
    lines.append(u"contents: %d pages listed" % sum(1 for k, _t, _n in rows if k == "title"))
    ck_page(P)
    bk_finish(P)
    return P


def _bk_cutout_sources():
    p_ = os.path.join(BERGAMA_ROOT, "Data", "cutouts", "cutouts.json")
    try:
        with open(p_, encoding="utf-8") as f_:
            d_ = json.load(f_).get("cutouts") or {}
    except Exception:
        return []
    out = []
    for key, ents in sorted(d_.items()):
        for e_ in (ents if isinstance(ents, list) else [ents]):
            t = (u"%s" % ((e_ or {}).get("source") or u"")).strip() if isinstance(e_, dict) else u""
            if t and t not in out:
                out.append(t)
    return [u"Cutout: " + t for t in out]


def bk_source_groups(lines):
    groups = [(u"SOURCES, IN PAGE ORDER", [u"[%d] %s" % (i, BK_SRC["text"][k]) for i, k in
                                           enumerate(BK_SRC["order"], 1)])]
    mp = BK_IX.get("bergama_masterplan", {}).get("extra", {}).get("plan_sources")
    if mp:
        rows = []
        if isinstance(mp, dict):                           # v30.1 (closing): masterplan plan_sources dict
            for m_ in mp.get("markers") or ():             # (p23_plan.py: crop, heading, markers, left_as_is)
                if not isinstance(m_, dict):
                    continue
                ts = [(u"%s" % ((s_ or {}).get("text") or u"")).strip() for s_ in m_.get("sources") or ()
                      if isinstance(s_, dict)]
                ts = [t for t in ts if t]
                if ts:
                    rows.append(u"%s %s: %s" % (m_.get("n", u""), m_.get("name") or u"", u"; ".join(ts)))
        else:
            for r in (mp if isinstance(mp, list) else []):
                rows.append(u" · ".join(u"%s" % v for v in r) if isinstance(r, (list, tuple)) else u"%s" % r)
        if rows:
            groups.append((u"SOURCES OF THE NUMBERED PLACES ON THE MASTERPLAN", rows))
    groups.append((u"HEIGHT DATA", list(ELEV_SOURCES)))
    hr = []
    if "hr_sources" in globals():
        try:
            hr = list(hr_sources())
        except Exception:
            hr = []
    assets = []
    for t in hr + BK_ASSET_SOURCES + _bk_cutout_sources():
        if t not in assets:
            assets.append(t)
    groups.append((u"ASSETS", assets))
    unused = [k for d in BK_IX.values() for k in (d.get("sources") or {}) if k not in BK_SRC["num"]]
    lines.append(u"sources: %d cited in page order; %d rows of the scripts not cited on any page, left out%s" % (
        len(BK_SRC["order"]), len(unused), (u" (" + u", ".join(sorted(set(unused))[:30]) + u")") if unused else u""))
    return [(h, r) for h, r in groups if r]


BK_SRC_COLS = {4: [(3.0, 22.0), (26.0, 22.0), (50.0, 22.0), (73.0, 24.0)],          # % of the page (x, w)
               5: [(3.0, 17.6), (22.0, 17.6), (41.0, 17.6), (60.0, 17.6), (79.0, 18.0)]}
BK_SRC_Y = (10.0, 92.0)            # % of the page: columns top / foot
BK_SRC_PT = (5.0, 4.5)             # largest / smallest size before a fifth column (then down to GRID_MIN_PT)
BK_SRC_IND = 4.6                   # mm: the hanging indent of an entry ("[142] " at 5 pt is about 4.2 mm)
_BK_SRC_NUM = re.compile(r"^(\[\d+\])\s+")


def _bk_src_h(k, t, cw, s):
    if k == "heading":
        return st_fit(t, cw, None, "heading", 6.0, justify=False, page="sources")[3] + 1.4
    m_ = _BK_SRC_NUM.match(t)
    body = t[m_.end():] if m_ else t
    return st_fit(body, cw - (BK_SRC_IND if m_ else 0.0), None, "source", s, justify=False, page="sources")[3] + 0.9


def bk_sources(doc, n, lines, pid="p22", title=u"Sources", part=None):
    """the Sources page(s), see the part notes; a second page only if even five columns at 4 pt do not hold them"""
    groups = bk_source_groups(lines)
    flat = []
    for h, rows in groups:
        flat.append(("heading", h))
        flat += [("source", r) for r in rows]
    y0, y1 = BK_SRC_Y[0] * BK_PCT[1], BK_SRC_Y[1] * BK_PCT[1]
    colh = y1 - y0
    pick = None
    for ncol, lo in ((4, BK_SRC_PT[1]), (5, GRID_MIN_PT)):
        cw = BK_SRC_COLS[ncol][-2][1] * BK_PCT[0]
        s = BK_SRC_PT[0]
        while True:
            hs = [_bk_src_h(k, t, cw, s) for k, t in flat]
            if sum(hs) <= ncol * colh * 0.96 or s - 0.25 < lo - 1e-6:
                break
            s -= 0.25
        pick = (ncol, s, hs)
        if sum(hs) <= ncol * colh * 0.96:
            break
    ncol, s, hs = pick
    cols = [(x * BK_PCT[0], w * BK_PCT[0]) for x, w in BK_SRC_COLS[ncol]]
    label = (u"%s  %s" % (part, PARTS.get(part, u""))).upper() if part else None
    pages, P, col, y = [], None, 0, y0
    for (k, t), hh in zip(flat, hs):
        if P is None or y + hh > y1 + 1e-6:
            if P is not None:
                col += 1
                y = y0
            if P is None or col >= ncol:
                if P is not None:
                    bk_pageno(P, n + len(pages) - 1)
                    ck_page(P)
                    bk_finish(P)
                P = bk_page(doc, pid, n + len(pages))
                bk_band(P, label, title if not pages else title + u" (continued)")
                pages.append(P)
                col, y = 0, y0
        cx, cw = cols[col]
        if k == "heading":
            st_para(P, t, cx, y, cw, None, "heading", 6.0, justify=False, page=pid)
        else:
            m_ = _BK_SRC_NUM.match(t)
            if m_:                                  # hanging indent: the number, then the text block beside it
                a_, _d = fm_asc_desc(s)
                P.tp.put(m_.group(1), cx, y + a_, s, False, "L", 0.0, None, "source", GRID_INK["ink2"], ())
                st_para(P, t[m_.end():], cx + BK_SRC_IND, y, cw - BK_SRC_IND, None, "source", s, justify=False,
                        page=pid)
            else:
                st_para(P, t, cx, y, cw, None, "source", s, justify=False, page=pid)
        y += hh
    if P is not None:
        bk_pageno(P, n + len(pages) - 1)
        ck_page(P)
        bk_finish(P)
    if len(pages) > 1:
        wn_warn(pid, "overrun", u"the sources need %d pages at %.2f pt in %d columns (the booklet has %d + %d)" % (
            len(pages), s, ncol, n, len(pages) - 1))
    lines.append(u"sources page: %d rows at %.2f pt, %d columns, %d page(s)" % (len(flat), s, ncol, len(pages)))
    return len(pages)
