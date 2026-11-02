# ---- 83_cover_sources (round 5, S10, 2 Nov 2026; P01.1, P01.2, Sources): the two pages the booklet draws itself -----
# Cover (P01.1): the cover photo (Data/COVER_IMG) fills the WHOLE page behind everything (full bleed, proportions kept,
# the overflow cut by the page edge) under a white veil of COVER_VEIL opacity, so the photo shows very light and the
# text stays readable. Left: course, MIRAQUA, title, subtitle, the approved text, names, date. Right (P01.2): contents
# of the 23 pages (theme, stage, page title with its number), merged pages listed once (D7, D9).
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
    # contents (P01.2): from column 9 (x = 14 + 8 x 33), 23 pages
    cx = GRID_ML + 8 * 33.0
    st_line(P, u"CONTENTS", cx, 18.0, 8.0, True, acc, role="title")
    rows, last, lst = [], None, None
    for i, sp in enumerate(BK_PAGES, 1):
        if i == 1:
            continue
        if sp.get("kind") == "sources":
            rows.append(("gap", None, None))
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
        for r in (mp if isinstance(mp, list) else (mp.items() if isinstance(mp, dict) else [])):
            rows.append(u" · ".join(u"%s" % v for v in r) if isinstance(r, (list, tuple)) else u"%s" % r)
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


def bk_sources(doc, n, lines):
    """the Sources page(s): 3 columns, one size for all rows (5 pt, down to 4 pt), a second page only if needed"""
    groups = bk_source_groups(lines)
    x0, y0, x1, y1 = GRID_AREA
    ncol = 3
    cw = (x1 - x0 - BK_GAP * (ncol - 1)) / float(ncol)
    flat = []
    for h, rows in groups:
        flat.append(("heading", h))
        flat += [("source", r) for r in rows]
    s = 5.0
    while True:
        hs = [st_fit(t, cw, None, k, s if k == "source" else 6.0, justify=(k == "source"), page="p23")[3] + 1.0
              for k, t in flat]
        if sum(hs) <= ncol * (y1 - y0) * 0.97 or s <= GRID_MIN_PT + 1e-6:
            break
        s -= 0.25
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
                P = bk_page(doc, "p23", n + len(pages))
                L = lay_page(P, 1.0, 1)
                bk_title(P, L, u"Sources" if not pages else u"Sources (continued)")
                pages.append(P)
                col, y = 0, y0
        st_para(P, t, x0 + col * (cw + BK_GAP), y, cw, None, k, s if k == "source" else 6.0,
                justify=(k == "source"), page="p23")
        y += hh
    if P is not None:
        bk_pageno(P, n + len(pages) - 1)
        ck_page(P)
        bk_finish(P)
    if len(pages) > 1:
        wn_warn("p23", "overrun", u"the sources need %d pages at %.2f pt (the booklet has 23 + %d)" % (
            len(pages), s, len(pages) - 1))
    lines.append(u"sources page: %d rows at %.2f pt, %d page(s)" % (len(flat), s, len(pages)))
    return len(pages)
