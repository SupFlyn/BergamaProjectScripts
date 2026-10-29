# ---- MIRAQUA round 28 Oct 2026 (masterplan v27): p.21 open ground and p.23 the masterplan, each ONE strip; the frame
# area (G10); the open ground for the site board's filter sheet (D1) (worker MP-plan). Shared pieces: common/r28_style.py,
# common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v27 (MIRAQUA 28 Oct, MP-plan). Both pages are crops drawn for the booklet panel (BK_W x BK_H = 392 x 238 mm) at 1:1:
#   * G7: the whole analysis frame (site_alan, 2,845 x 529 m) as ONE strip at 1:10,000 (284.5 x 52.9 mm; 1:5,000 would
#     need 569 mm), the water left to right, at the top-left; no halves, no "continues below".
#   * G8: the study area (calisma_alan, both parts) in R28_STUDY_LINE on both, R28_STUDY_NAME in the legend; the strip's
#     edge is the analysis frame, named (R28_FRAME_NAME) only on p.21, where figures are counted over it.
#   * G10: ONE frame figure, the frame polygon's area; the grid counts only cells whose centre lies inside the frame
#     (pl28_frame_stats); every figure on p.21 and in r28_open_ground.json comes from that one count.
#   * P21.1: every open-ground category in its own R28_OPEN colour, the no-plant-cover hatch too; bars in the map's
#     colours.
#   * P23.1 / P23.2: the numbered markers in their R28_MARKERS group colour, placed by common/label_place.py (G4); the
#     list under the strip by group: coloured number, name, one short line. The reasons and source codes go to the
#     booklet's sources page (blocks.json and booklet/results.json "plan_sources"). The areas left as they are (no
#     intervention) get a grey letter on the plan and one line in the list (their two-line notes do not fit at
#     1:10,000).
#   * D1: the masterplan runs before the site board (RUN_GUIDE §2): the site board draws the filter sheet (drw_filter)
#     from r28_open_ground.json, written here next to masterplan_results.json.
PL28_BAND = 8.0                  # mm above and below the strip where a marker may sit, on a leader (p.23)
PL28_TS, PL28_HEAD_TS = 2.65, 2.82   # booklet label 7.5 pt and kicker 8 pt (PLAN §2), mm
PL28_COLS = (0.0, 99.0, 198.0, 297.0)   # the four columns of the list and the figures, mm from the crop's left
PL28_COL_W = 92.0                # one column, mm (7 mm gutters; the last runs to the crop's right edge)
PL28_TOP = 150.0                 # top of the list / the figures, mm from the crop's foot (under the scale bar row)
PL28_MARKS = (0.0, 100.0, 200.0, 500.0)   # the scale bar at 1:10,000, m (50 mm)
PL28_NI_R = 1.6                  # the letters of the areas left as they are, radius mm
PL28_OPEN_JSON = "r28_open_ground.json"   # D1: in cached/bergama_masterplan/, beside masterplan_results.json
PL28_HUB = {u"K4": u"K4 · Ulucami Önü", u"K3": u"K3 · Tabak", u"İstiklal": u"İstiklal Meydanı",
            u"Kızıl Avlu": u"Kızıl Avlu", u"K5": u"K5 · Üç Kemer", u"K6": u"K6"}   # list names (HUB_NAME, sentence case)
PL28_SRC_TAG = re.compile(u"\\s*\\((survey|satellite 2021|satellite check)\\)")   # source tags of the no-go reasons
PL28_SRC_NAME = {u"survey": u"survey (Bergama_Altlik.3dm)", u"satellite 2021": u"ESA WorldCover 2021",
                 u"satellite check": u"satellite check (OPEN_CHECK)"}


def ground_page(C, warn):
    """v27 (MIRAQUA 28 Oct, P21.1, P21.2, G7, G8, G10): the open ground (crop mp_max_area; p.21, used when D1 = keep).
    Top-left ONE strip of the analysis frame at 1:10,000, crisp (it is analysis), each category in its own R28_OPEN
    colour (the no-plant-cover hatch too), the study area outline; the scale bar row under it, the legend beside it;
    under them, from PL28_TOP, the figures in the map's colours, all from ONE count (pl28_frame_stats: the frame
    polygon's area, cells inside the frame): the frame's split as one bar across the page, the open ground by distance
    from the water and by land cover on the satellite, the satellite check."""
    k = 1000.0 / MP_SCALE
    g = pl28_strip(C, k)
    T, dw, dh = g["T"], g["dw"], g["dh"]
    O = R28_OPEN
    hatch, since = (O["noplant_hatch"], 0.9, 0.18, 45.0), (COL["ink_dark"], 0.8, 0.2, 45.0)
    W, H = BK_W, BK_H
    pg = Page(dw, dh)
    TL = lambda Ls: [Q for Q in ([T(p) for p in L_] for L_ in Ls) if hit(bbox(Q), (-2.0, -2.0, dw + 2.0, dh + 2.0))]
    pg.poly(TL(C.max_loops), fill=O["open_fill"])
    pg.poly(TL(C.bare_loops), stripes=hatch)
    pg.poly(TL(C.bed_loops), fill=O["stream"])
    for P in C.streams:
        pg.line([T(p) for p in P], COL["river_mid"], 0.15)
    for role in ("building", "housing", "shed", "heritage"):
        pg.poly(TL(C.bld.get(role, [])), fill=O["building"])
    pg.poly(TL(C.built_since), fill=O["building"], stripes=since)
    pg.poly(TL(C.road_loops), fill=O["road"])
    for P in C.bridges:                                  # v27: over the roads (the road fill hid them)
        pg.line([T(p) for p in P], O["bridge"], 0.3)
    study = pl28_draw_study(pg, C, T)
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    x0, y0 = 0.0, H - PL28_BAND - dh                     # the strip where p.23 has it
    sh.clip([rect(x0, y0, x0 + dw, y0 + dh)])
    blit(sh, pg, x0, y0)
    sh.unclip()
    sh.poly([rect(x0, y0, x0 + dw, y0 + dh)], stroke=COL["ink2"], lw=0.25)   # the analysis frame (its figures below)
    y_row = y0 - PL28_BAND - 10.0
    pl28_marks(sh, C, x0, y_row)
    ink, ink2 = COL["ink"], COL["ink2"]
    pl28_legend(sh, [(u"SURVEY · SATELLITE",
                      [(u"Open ground", _sw_fill(O["open_fill"], ink2)),
                       (u"No plant cover (satellite)", _sw_fill(O["open_fill"], ink2, stripes=hatch)),
                       (u"Stream bed", _sw_fill(O["stream"])), (u"Building", _sw_fill(O["building"])),
                       (u"Road", _sw_fill(O["road"], ink2)), (u"Bridge", _sw_line(O["bridge"], 0.3))] +
                      ([(u"Built since survey", _sw_fill(O["building"], stripes=since))] if C.built_since else []) +
                      ([(R28_STUDY_NAME, pl28_sw_study())] if study else []) +
                      [(R28_FRAME_NAME, _sw_line(ink2, 0.25))])], COL_X, W, H, y_row, 1, warn)
    # ---- the figures: ONE count (G10)
    st, tot, F, inF = C.stats, C.frame_m2 or 1.0, C.F, C.inF
    y = PL28_TOP - PL28_HEAD_TS * 1.18
    sh.text(u"{} · {}".format(R28_FRAME_NAME, u_area(tot, "ha")), 0.0, y + 0.5, PL28_HEAD_TS, COL["ink_dark"], bold=True)
    y -= PL28_TS * 1.3
    pl28_runs(sh, 0.0, y + 0.5, [(u"Open ground", True), (u" = no survey building, no survey road ({:.1f} m either side "
                                                          u"of a street edge), not the stream bed · {:.0f} m grid, cells "
                                                          u"inside the frame".format(ROAD_BUF_M, C.G.c), False)],
              PL28_TS, ink)
    y -= PL28_TS * 1.3
    pl28_runs(sh, 0.0, y + 0.5, [(u"Open to change", True), (u" (where we can build) counts only vacant ground, parking "
                                                             u"and yards, and loose ground", False)], PL28_TS, ink2)
    y -= 3.0
    parts = [(u"open ground", O["open_fill"], st[0]), (u"stream bed", O["stream"], st[3]),
             (u"buildings", O["building"], st[1]), (u"roads", O["road"], st[2])]
    xa = 0.0
    for nm, fill, a in parts:                            # the frame's split as one bar across the page
        w_ = W * a / tot
        sh.poly([rect(xa, y - 7.0, xa + w_, y)], fill=fill, stroke=ink2, lw=0.1)
        xa += w_
    y -= 8.8
    for i, (nm, fill, a) in enumerate(parts):
        x = PL28_COLS[i]
        sh.poly([rect(x, y - 2.9, x + 6.0, y - 0.5)], fill=fill, stroke=ink2, lw=0.15)
        pl28_runs(sh, x + 7.5, y - 2.6, [(nm + u" ", False), (u_area(a, "ha"), True),
                                         (u" · {:.0f} %".format(100.0 * a / tot), False)], PL28_TS, ink)
    y -= 3.6 + 8.0
    c2 = C.cell_m2
    by_d, by_lc = [0.0] * 4, {}
    for n in range(C.N):
        if F[n] != 0 or not inF[n]:
            continue
        d = C.Dst[n]
        by_d[0 if d <= 25.0 else (1 if d <= ECO_BANDS[-1] else (2 if d <= DMAX_M else 3))] += c2
        by_lc[C.lc[n]] = by_lc.get(C.lc[n], 0.0) + c2
    of = O["open_fill"]
    y1 = pl28_chart(sh, 0.0, y, 190.0, u"Open ground by distance from the water",
                    [(u"walking", True), (u" through open ground, survey", False)],
                    [(u"0-25 m", by_d[0], of, None), (u"25-{:.0f} m".format(ECO_BANDS[-1]), by_d[1], of, None),
                     (u"{:.0f}-{:.0f} m".format(ECO_BANDS[-1], DMAX_M), by_d[2], of, None),
                     (u"no open way within {:.0f} m".format(DMAX_M), by_d[3], of, None)])
    y2 = pl28_chart(sh, PL28_COLS[2], y, W - PL28_COLS[2], u"Open ground by land cover",
                    [(u"ESA WorldCover 2021", True), (u", satellite, 10 m pixels", False)],
                    [(nm, by_lc.get(code, 0.0), of, hatch if code == 0 else None)
                     for code, nm in ((1, u"cropland"), (5, u"orchards"), (2, u"tree cover"), (3, u"scrub"),
                                      (4, u"grassland"), (0, u"no plant cover"))])
    y = min(y1, y2) - 8.0
    ck = OPEN_CHECK
    y -= PL28_HEAD_TS * 1.18
    if ck.get("imagery"):
        sh.text(u"Satellite check · done", 0.0, y + 0.5, PL28_HEAD_TS, COL["ink_dark"], bold=True)
        s_ = u"{} of {}: {} area{} built on since the survey (dark hatch), out of the open ground".format(
            ck["imagery"], ck.get("date") or u"date not given", len(C.built_since), u"" if len(C.built_since) == 1 else u"s")
    else:
        og = getattr(C, "og_check", {})
        sh.text(u"Satellite check · pending", 0.0, y + 0.5, PL28_HEAD_TS, COL["ink_dark"], bold=True)
        s_ = u"no satellite image could be opened from the cloud (27 Oct 2026) · {} open areas of {:.2f} ha or more to " \
             u"check in Google Earth, {} with no plant cover first (hatched): logs/{}".format(
                 og.get("n", 0), OG_MIN_HA, og.get("flag", 0), OG_KML)
    for ln in wrap(s_, PL28_TS, 190.0):
        y -= PL28_TS * 1.3
        sh.text(ln, 0.0, y + 0.5, PL28_TS, ink2)
    if y < 1.0:
        warn.append(u"open ground page: the figures run {:.1f} mm below the crop".format(1.0 - y))
    sh.crop = (0.0, 0.0, W, H)
    sh.key, sh.world, sh.scale, sh.pleg = "max_area", bbox(C.V.P), MP_SCALE, None
    sh.bid = ("mp_max_area", "mp_max_area", u"Open ground in the {} (survey){}".format(
        R28_FRAME_NAME.lower(), u" · satellite check: {}, {}".format(ck["imagery"], ck.get("date") or u"date not given")
        if ck.get("imagery") else u" · satellite check pending"))
    return sh


