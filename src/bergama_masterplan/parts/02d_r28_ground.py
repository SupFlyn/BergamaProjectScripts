# ---- MIRAQUA round 28 Oct 2026 (masterplan v27): p.23 the masterplan (v28: the open ground page is gone); the frame
# area (G10) (worker MP-plan). Shared pieces: common/r28_style.py,
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
PL28_TS, PL28_HEAD_TS = 2.65, 2.82   # booklet label 7.5 pt and kicker 8 pt (PLAN §2), mm
PL28_MARKS = (0.0, 100.0, 200.0, 500.0)   # the scale bar at 1:10,000, m (50 mm)
PL28_NI_R = 1.6                  # the letters of the areas left as they are, radius mm
PL28_HUB = {u"K4": bridge_name("K4"), u"K3": bridge_name("K3"), u"İstiklal": landmark_name("istiklal_meydani"),
            u"Kızıl Avlu": landmark_name("kizil_avlu"), u"K5": bridge_name("K5"),
            u"K6": bridge_name("K6")}   # list names; v37 (round 3, G16): the full names of common/data/NAMES.py
PL28_SRC_TAG = re.compile(u"\\s*\\((survey|satellite 2021|satellite check)\\)")   # source tags of the no-go reasons
PL28_SRC_NAME = {u"survey": u"survey (Bergama_Altlik.3dm)", u"satellite 2021": u"ESA WorldCover 2021",
                 u"satellite check": u"satellite check (OPEN_CHECK)"}


# v28 (revision 29 Oct, WO-T4b-1): ground_page (crop mp_max_area, the open ground page) is gone with p.22 (D1 a:
# merged into the site board's p.06), and with it r28_open_ground.json (no reader since site board v51).



# ---- v38 (round 4, S8, G-R4-4): ONE draw order for the masterplan's maps (p16, p21, p22) ------------------------
def mp_map_draw(pg, page, T, base, steps=None, tint=(), study=None, log=None, water_opts=None, study_line=True):
    """The masterplan's adapter to common/map_layers.map_draw: the base (ml_base items, survey m) and the D9 tint
    (ml_tint items) go through map_draw as items; the page's own drawing (water, lines, planting, marks), which the
    Page draws directly, is called as steps = {layer: fn()} AT its layer, so map_draw alone decides the order
    (ML_LAYERS: base_* -> proj_tint -> proj_water -> proj_lines -> proj_vegetation -> study -> proj_marks ->
    proj_labels) and its log line "layers base→project ok, n_outside_clipped n (page: layers)" is the real order.
    Everything a step draws must already be clipped to the study area at its source (Corridor, v38) or by the step
    (sc_*). study: the study rings (survey m) for the tint clip and the study line. Returns map_draw's dict."""
    steps = dict(steps or {})

    def fill(rings, hx, a, nz):
        al = None if a is None or a >= 0.995 else a
        if nz and len(rings) > 1:                         # the Page fills even-odd: a nonzero item (overlapping
            for r_ in rings:                              # building rings) one ring at a time, so overlaps never
                pg.poly([r_], fill=hx, alpha=al)          # open white notches (CHK-3)
        else:
            pg.poly(rings, fill=hx, alpha=al)

    def line(pts, hx, w, dash, a):
        pg.line(pts, hx, w, list(dash) if dash else None, cap=0 if dash else 1,
                alpha=None if a is None or a >= 0.995 else a)

    def text(s_, xy, size, hx, bold, align):
        pg.text(s_, xy[0], xy[1], size, hx, bold=bool(bold), align=align if align in ("L", "C", "R") else "L",
                role="base_name")
    project = {}
    if tint:
        project["proj_tint"] = list(tint)
    for k_ in steps:
        project.setdefault(k_, []).append(("step",))     # basemap_draw skips unknown kinds; order_fn draws it

    def order(layer):
        f_ = steps.get(layer)
        if f_ is not None:
            f_()
    return map_draw(page, T, fill, line, text, base, project, study=study, clip=True, order_fn=order, log=log,
                    water_opts=water_opts, study_line=study_line)


def mp_marker(pg, cx, cy, s, colour, size_pt=7.0, style="solid", name=None, r_min=None, rim="FFFFFF", rim_mm=0.25):
    """v38 (round 4, G-R4-7): ONE marker on a masterplan Page (y up): common/marker.mk_marker's disc drawn by the
    page, kept as an obstacle in the page's TextPage (kind "marker"), its glyph centred on its ink box and drawn by
    pg.text (registered, allowed only on its own disc). colour = the colour of the element it names (mk_colour).
    Returns (box, r)."""
    shapes, box, r = mk_marker(cx, cy, s, colour, size_pt, r_min, style, rim, rim_mm, None, False)
    MK_N[0] += 1
    nm = name or u"marker %d" % MK_N[0]
    for s_ in shapes:
        if s_[0] == "poly":
            pg.poly([s_[1]], fill=s_[2], stroke=s_[3], lw=s_[4] or 0.1)
            pg.keep(s_[1], "marker", nm)
    for s_ in shapes:
        if s_[0] == "text":
            pg.text(s_[1], s_[2], s_[3], s_[4], s_[5], bold=True, align="L", name=nm, allow=(nm,), role="marker")
    return box, r
