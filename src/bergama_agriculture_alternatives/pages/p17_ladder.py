# ------------------------------------------------------------------ booklet p17: one plant ladder, streambed to field
# v11 (round 6 S7, 4 Nov 2026; BRIEF §6 row 17, Q9, PLAN §2.2 / §2.3; target refs/targets/r06_S01): the 28 Oct page
# "One plant ladder, streambed to field" restored from f93d84b (agriculture v3.1 page_ladder, ladder_row, chain_strip,
# seasons, data/STEPS.py; the proposal sections' SKETCH_SRC as the sketch engine, included read-only) as booklet items:
#   ag3_chain           the one-way chain along the stream (drawing, mm)
#   ag3_steps           what we do with the water, steps 1-5 (numbered list)
#   ag3_legend          the chain's symbol key (legend, hues from common/hues.py)
#   ag3_ladder_high / ag3_ladder_low / ag3_ladder_harvest   one stepped cut streambed -> field, one season each (drawing)
#   ag3_bands           the plant bands BED .. FARMS with the photos inside (image shapes, so each photo stays under
#                       its band), the REMOVE / ODOUR / reading notes column on the left (drawing)
# SECTION LANGUAGE: SKETCH (BRIEF §3, r06_S01): not to scale, thick black ground line, flat beige soil, flat blue water
# bands, simple tree blobs, few small figures, short captions. No hatches (the winter bed hatch of 28 Oct is gone), no
# horizontal dimensions, no leader lines (labels are placed by the booklet), no red: flood lines WAT r1 (P-5).
# Data (BRIEF §0 DATA): bed and flood depths = research/rain_river_levels/README.md "The answers in short" + its v1.1
# correction table (Q100 205.2 / Q500 263.3 m³/s, surveyed sections 2.0-3.0 / 2.3-3.3 m, flat end 1.4 / 1.5 m, highest
# day 0.96-1.69 m, overtopping only at K4 right bank and S4 left bank); species and reasons = research/water_data/04
# (via data/STEPS.py); today's cover = data/GEO.py "corridor" (ESA WorldCover 2021). The 28 Oct [n] numbers are gone:
# every mark is {src:agsrcN}; the project's own records (programme, garden card, Kermes card, water board season words,
# the chain) carry no mark (F5_OFF), as on every other page.
AG3_PAGE = "p17"
AG3_ID = dict(chain="ag3_chain", steps="ag3_note_steps", legend="ag3_note_legend", bands="ag3_bands", notes="ag3_notes",
              high="ag3_ladder_high", low="ag3_ladder_low", harvest="ag3_ladder_harvest")
SPECIES = "POWO, FEIS, JRC Atlas, Korkusuz et al. 2004, Aydın Temel et al. 2017, Xie et al. 2021, RHS (species, flood and cleaning evidence)"
BANDS = "planting bands after MITECO, Salinas & Cueto 2009 (habitat 92D0), USDA NRCS TN-38"
DEPTH = "DSİ design floods Q100 205.2 m³/s and Q500 263.3 m³/s; DSİ gauge yearbooks 2016-2021"
TODAY = "ESA WorldCover 2021, by distance from the OSM Selinos centreline"
REUSE = "published, 2010 wastewater reuse communiqué"          # the water board's p11 coliform source, same words
CHAIN_REF = ("option A water chain: one way, cleaned once upstream in the reed basins, held in the terrace cascade, "
             "summer strip from storage, surplus to existing farmland outside the site")
PROG = ("MIRAQUA programme and its historic roots: hubs at the Roman bridges K3, K4, K5 with floodable in-bed sub-hubs, "
        "hidden-stream square at İstiklal Meydanı, tanning reach at K3, Tabaklar Hamamı at K4, Late Antique workshops "
        "downstream, plane-tree squares")
GARDEN = ("Demeter's Garden (Begüm, 25 Oct): olives; summer farm-to-table use; winter herbs and greens; seasonal "
          "production, education; south-west bank at K5")
KERMES = "Kermes first held 1937; in the low-water season (project history card h01)"
WB_YEAR = "water board season rows: storage fills in winter, low until the rains in autumn; reeds gold, seed heads"
HARVEST = KAYA                                     # Memecik trees hand-harvested in November (Kaya et al. 2017)
F5_OFF = F5_OFF + (CHAIN_REF, PROG, GARDEN, KERMES, WB_YEAR)   # the project's own records: no mark, not in Sources
JOB_ICON = [("CLEAN", "clean"), ("HOLD", "hold"), ("SHADE", "shade"), ("SCENT", "scent"), ("HARVEST", "olive")]
AG_ICONS.update(clean=("reeds", False), hold=("flood_zone", False), shade=("shade", False), scent=("plants", False),
                outside=("field", False))          # v11: the 28 Oct pictograms by their icons.py names
# v1.6 (28 Oct): the bank top as the project has it: hub squares with plane trees at the bridges and Demeter's
# Garden's olives at K5 (olive "will not tolerate waterlogged soils", DATA_REGISTER PL-11)
STEPS[3].update(sub="hub squares at the bridges · Demeter's Garden at K5", job="SHADE + SCENT",
                plant=[("plane", "hub squares: Ottoman squares with plane trees")] + STEPS[3]["plant"] +
                      [("olive", "Demeter's Garden (K5): dry top only, no waterlogged soil")])

LAD_W = 200.0                        # sketch units across: 5 steps of 40
LAD_S = LAD_W / 5.0
LAD_X0, LAD_X1 = 106.0, 406.0        # the cut, mm (left of it: the season column)
LAD_F = (LAD_X1 - LAD_X0) / LAD_W    # mm a sketch unit, the same across and up
LAD_GB = 13.0                        # v11: the bottom of the cut ground, sketch units (28 Oct 12; 1 unit under the
#                                      channel's foot at 14, so the row is 3 mm lower and the band frames fit)
LAD_GY = (16.0, 21.0, 26.0, 30.0, 33.0)   # ground of each step (bed, lower bank, terrace, bank top, farms)
LAD_Q100, LAD_Q500 = 30.8, 31.6      # over the bank top only at K4 / S4 (README v1.1), under the farms
ROW_H = 47.0                         # mm a season row (28 Oct 50); the bank top's plane tree ends 3 mm under the top
SUBHUB = (27.0, 36.0)                # the floodable sub-hub in the bed, sketch x
HUB = (3 * LAD_S + 2.0, 3 * LAD_S + 17.0)   # the dry hub square on the bank top at the bridges, sketch x
SIT_FIG = [(-0.14, 0.0), (0.30, 0.0), (0.30, -0.42), (0.42, -0.42), (0.42, 0.13), (0.10, 0.14), (0.12, 0.62),
           (0.05, 0.70), (-0.10, 0.70), (-0.17, 0.58)]   # a seated figure (m, as the board's SA_FIGS), seat at (0, 0)
AG3_TREES = [0, 0]                   # this press: [trees with a species, generic trees] on p17 (G6-10 log)
AG3_NOPHOTO = []                     # species whose photo did not load this press (listed under the band, logged)


PH_GAP = 2.0                         # mm between two photos side by side (28 Oct)
# v13 (round 7 S2, L6 + BRIEF row 17): the bands' photos are 28 x 13 mm (cover-cropped by the clip, never stretched;
# was PHOTO_W x PHOTO_H 28 x 21). The r06_S01 bands frame [106.5,205.6 298.9x80.2] held names only; v12 prints every
# species' reason too (nothing dropped), which at 21 mm photos ran ~7 mm a row past the frame and, scaled down in R6,
# made the 19 caption overlaps. 8 mm less photo a row = room for the reasons inside the frame at SON size.
AG3_PH_H = 13.0


def name_lines(key, mark, size, w, bold=True):
    """28 Oct (v2): a plant's name under its photo: "English (Turkish) {src}" on one line when it fits in w, else the
    English name and "(Turkish) {src}" on two (each wrapped to w if it is longer still)"""
    t = plant_name(key) + ((" " + mark) if mark else "")
    if text_w(t, size, bold) <= w:
        return [t]
    en, _, tr = plant_name(key).partition(" (")
    if not tr:
        return wrap(t, size, w, bold)
    return wrap(en, size, w, bold) + wrap("(" + tr + ((" " + mark) if mark else ""), size, w, bold)


def _bed(i):
    """the bed's water from STEPS: 0 = Jul-Sep, 1 = Jan-Apr"""
    return STEPS[0]["water"][i].split(": ", 1)[1]


# the season rows: what the water does (left column) and what people do where (on the cut). acts: (figure kind or
# "sit" / None, sketch x, sketch y, flip, label, source, align). v11: labels on the farms step start right of the
# site edge (align L), so the dashed edge never runs through them (target overlap).
def seasons():
    g0, g1, g2, g3, g4 = LAD_GY
    return [
        dict(key="high", name="HIGH WATER", months="Jan-Apr", mark="winter",
             side=[("bed " + _bed(1) + " deep", DEPTH), ("lower bank under water", None), ("sub-hubs closed", PROG),
                   ("storage fills", WB_YEAR)],
             acts=[("sit", 2 * LAD_S + 1.0, g2, True, "sit at the edge · watch the water", PROG, "C"),
                   (0, HUB[0] + 4.0, g3, False, "hub square: dry, step-free", PROG, "C"),
                   (2, HUB[0] + 8.5, g3, True, None, None, "C"),
                   (None, sum(SUBHUB) / 2.0, g1 + 1.8, False, "sub-hub under water: closed", PROG, "C")]),
        dict(key="low", name="LOW WATER", months="Jul-Sep", mark="summer",
             side=[("bed " + _bed(0), DEPTH), ("strip 0.30 m all summer (design)", None), ("sub-hubs open", PROG),
                   (STEPS[4]["water"][0], None)],
             acts=[(1, 10.5, g0, False, "walk in the bed", PROG, "C"),
                   (0, 19.0, g0 - 2.0, False, "wade the strip", None, "C"),
                   (2, SUBHUB[0] + 3.0, g0 + 0.7, False, "sub-hub open", PROG, "C"),
                   (None, 6.0, g0 + 8.5, False, "Kermes (since 1937) in the dry bed", KERMES, "L"),   # v13 (L6): was g0 + 6.0, 1.65 mm over "walk in the bed" (R6 overlap); r06_S01 puts it a line above
                   (1, 2 * LAD_S + 20.0, g2, False, "shade under the trees", None, "C"),
                   (0, HUB[0] + 4.0, g3, False, "hub square: %s shade" % name_lc("plane"), PROG, "C"),
                   (None, 3 * LAD_S + 25.0, g3 + 2.0, False, "at K5: Demeter's Garden · café, summer beds", GARDEN, "R"),
                   (3, 4 * LAD_S + 19.0, g4, False, "fields + %s trees watered from storage" % name_lc("olive"), None,
                    "L")]),
        dict(key="harvest", name=name_caps("olive") + " HARVEST", months="Nov", mark="olive",
             side=[("%s: hand-picked in Nov" % name_lc("olive"), HARVEST), ("storage low until the rains", WB_YEAR),
                   ("first-flush cleaning", WB_YEAR)],
             acts=[(None, 5.0, g0 + 3.0, False, "%s gold · seed heads" % name_lc("reed"), WB_YEAR, "L"),
                   (0, 3 * LAD_S + 30.0, g3, False, "Demeter's Garden: winter herbs + greens · education", GARDEN, "R"),
                   (3, 4 * LAD_S + 12.0, g4, False, "%s harvest" % name_lc("olive"), HARVEST, "L"),
                   (1, 4 * LAD_S + 23.0, g4, True, None, None, "C")])]


def ladder_row(sea, mark_xy):
    """One season of the plant ladder in the SKETCH language: [(item, (kind, element id))] in sketch units (0..LAD_W
    across), draw order kept (z, order). mark_xy: where the season's sun / rain mark goes, sketch units.
    v11 (G6-9): every element's engine items carry its group (kind, element id), tagged as they are made."""
    E = sketch_engine()
    E["FORM"] = "A"                                   # organic only where the project meets the water
    del E["ZP"][:]
    E["ORDER"][0] = 0
    tags, mk = {}, [0]

    def T(kind, eid):                                 # every engine item since the last call belongs to this element
        for e in E["ZP"][mk[0]:]:
            tags[e[1]] = (kind, eid)
        mk[0] = len(E["ZP"])
    o, w, gy = (0.0, 0.0), LAD_S, LAD_GY
    g = [(0.0, LAD_GB), (0.0, gy[0])]
    for i in range(1, 5):
        xa = i * w
        if i == 1:                                    # the water's edge: the bank in form A (organic)
            g += E["bank"]((xa - 3.0, gy[0]), (xa + 3.0, gy[1]))
        elif i == 2:                                  # the terrace edge: a sitting step (straight riser)
            g += [(xa - 0.5, gy[1]), (xa + 0.5, gy[2])]
        else:                                         # elsewhere faceted, straight slopes
            g += [(xa - 2.0, gy[i - 1]), (xa + 2.0, gy[i])]
    g += [(LAD_W, gy[4]), (LAD_W, LAD_GB)]
    gs = E["sketch_ground"](o, E["notch"](g, [(13.0, 25.0, gy[0], 2.0)]))   # the summer strip's low-flow channel
    T("ground", "cut_ground")
    hub_c, sub_c = E["hx"](_hu("PUB", 3)), E["hx"](_hu("PUB", 2))      # G6-6: hub square PUB r3, sub-hub PUB r2
    E["fill"](o, [(HUB[0], gy[3] - 0.6), (HUB[1], gy[3] - 0.6), (HUB[1], gy[3]), (HUB[0], gy[3])], "paving", hub_c,
              boundary=False, hand_=False)        # the dry hub square at street level
    T("hubs", "hub_square")
    slab = [(SUBHUB[0], gy[0]), (SUBHUB[1], gy[0]), (SUBHUB[1], gy[0] + 0.7), (SUBHUB[0], gy[0] + 0.7)]
    E["fill"](o, slab, "paving", sub_c, boundary=False, hand_=False)   # the floodable sub-hub in the bed
    T("hubs", "sub_hub")
    if sea["key"] == "high":
        pc = E["under_level"](gs, 0.0, LAD_W, LAD_Q500)   # the design flood's reach (faint)
        if pc:
            E["wash"](o, pc, "flood", E["FLOOD_WASH"], E["FLOOD_ALPHA"])
        T("water", "q500_reach")
        E["water_level"](o, gs, 19.0, gy[1] + 1.8, E["W_WIN"], bed_hatch=False)   # winter highs: bed + lower bank
        T("water", "winter_high")
        E["sketch"](o, slab, "paving", E["SKINK"], E["PEN_HAIR"], closed=True, over=0.0, retrace=False,
                    dashed=True, z=E["Z_LINE"])       # the sub-hub under the water
        T("hubs", "sub_hub_under_water")
    elif sea["key"] == "low":
        E["water_level"](o, gs, 19.0, gy[0] - 0.8, E["W_EXT"], line=False)       # the summer strip in its channel
        T("water", "summer_strip")
    else:
        E["water_level"](o, gs, 19.0, gy[0] - 1.2, E["W_SUM"], line=False)       # autumn: water back in the channel
        T("water", "autumn_channel")
    # plants by step (graphic sizes): reeds in the bed, rushes and shrubs on the lower bank, trees on the terrace,
    # plane tree + lavender on the bank top, olives and a field crop on the farms
    E["reeds"](o, 1.5, 8.0, gy[0] - 0.2, 4.2)
    T("plants", "reed_bed")
    x_ = w + 4.0
    while x_ < w + 18.0:                              # rushes: short hand tufts
        for d in (-0.5, 0.0, 0.5):
            E["sketch"](o, [(x_, gy[1]), (x_ + d * 0.9, gy[1] + 2.0 - abs(d))], "planting", E["REED"], E["LW_FINE"],
                        over=0.0, amp=0.03, retrace=False, z=E["Z_TREE"])
        T("plants", "rush_%.0f" % x_)
        x_ += 1.6
    for nm, xs, hs, ws in (("tamarisk", w + 24.0, 5.0, 6.0), ("willow", w + 33.0, 4.2, 5.0)):   # STEPS lower bank shrubs
        dome = [(xs + ws / 2.0 * math.cos(math.pi * i / 14.0), gy[1] + hs * math.sin(math.pi * i / 14.0) ** 0.7) for i in range(15)]
        E["wash"](o, dome, "planting", E["SITE_TREE"][1], 0.6, z=E["Z_TREE"])
        E["sketch"](o, dome, "planting", E["SITE_TREE"][2], E["LW_FINE"], closed=True, over=0.0, amp=0.12, retrace=False,
                    z=E["Z_TREE"])
        T("plants", nm)
    trees = (("terrace_tree_1", None, 2 * w + 14.0, gy[2], 11.0), ("terrace_tree_2", None, 2 * w + 30.0, gy[2], 9.0),
             ("plane_hub_square", "plane", HUB[0] + 7.0, gy[3], 11.0))
    for eid, sp, xs, ys, hh in trees:                 # G6-10: a design species only where the project names one
        E["sketch_tree"](o, xs, ys, hh)
        T("trees", eid + ("" if sp else "_species_unspecified"))
        AG3_TREES[0 if sp else 1] += 1
    x_ = 3 * w + 20.0
    while x_ < 3 * w + 31.0:                          # lavender mounds with flower spikes
        mound = [(x_ + 1.2 * math.cos(math.pi * i / 10.0), gy[3] + 1.0 * math.sin(math.pi * i / 10.0)) for i in range(11)]
        E["wash"](o, mound, "planting", E["hx"](C["olive"]), 0.6, z=E["Z_TREE"])
        for d in (-0.5, 0.0, 0.5):
            E["sketch"](o, [(x_ + d, gy[3] + 0.8), (x_ + d * 1.3, gy[3] + 1.9)], "planting", E["hx"]("8E7CC3"), 0.3,
                        over=0.0, amp=0.02, retrace=False, z=E["Z_TREE"])
        T("plants", "lavender_%.0f" % x_)
        x_ += 2.8
    for eid, xs, ys, hh in (("olive_demeters_garden", 3 * w + 34.5, gy[3], 6.0), ("olive_farm_1", 4 * w + 6.0, gy[4], 7.0),
                            ("olive_farm_2", 4 * w + 15.0, gy[4], 7.0)):
        E["sketch_tree"](o, xs, ys, hh)
        T("trees", eid)
        AG3_TREES[0] += 1
    x_ = 4 * w + 26.0
    while x_ < LAD_W - 1.0:                           # field crop rows (AGR r3)
        E["sketch"](o, [(x_, gy[4]), (x_, gy[4] + 1.6)], "planting", E["hx"](_hu("AGR", 3)), 0.35, over=0.0, amp=0.02,
                    retrace=False, z=E["Z_TREE"])
        x_ += 1.4
    T("fields", "crop_rows")
    # the site edge: farmland only outside the site (v11: 6 units over the farms, was 11: it ran through the labels)
    E["sketch"](o, [(4 * w, gy[3] + 1.5), (4 * w, gy[4] + 6.0)], "site edge", E["INK2"], E["PEN_FINE"], over=0.0,
                retrace=False, dashed=True, z=E["Z_LINE"])
    T("annotations", "site_edge")
    s_ = 4.5 / 1.745                                  # people: the season's activities
    for n_, (kind, x, y, flip, _lab, _src, _al) in enumerate(sea["acts"]):
        if kind == "sit":
            sg = -1.0 if flip else 1.0
            E["fill"](o, [(x + sg * a * s_, y + b * s_) for a, b in SIT_FIG], "people", E["SITE_PEOPLE"], alpha=0.9,
                      boundary=False, z=E["Z_PEOPLE"], hand_=False)
            hx_, hy_, hr = E["SA_HEAD"][0] - 0.02, 0.84, E["SA_HEAD"][2]
            E["fill"](o, [(x + sg * hx_ * s_ + hr * s_ * math.cos(6.283 * i / 12), y + hy_ * s_ + hr * s_ * math.sin(6.283 * i / 12))
                          for i in range(12)], "people", E["SITE_PEOPLE"], alpha=0.9, boundary=False, z=E["Z_PEOPLE"],
                      hand_=False)
        elif kind is not None:
            E["sketch_person"](o, x, y, kind=kind, flip=flip)
        T("people", "person_%d" % n_)
    if sea["key"] == "high":                          # the design flood levels: hand dashed lines and level marks
        xe = 4 * w - 2.0 + 4.0 * (LAD_Q500 - gy[3]) / (gy[4] - gy[3])
        fl = E["hx"](_hu("WAT", 1))                   # P-5: no red on the page (was the engine's heritage red)
        for lv, nm in ((LAD_Q500, "q500"), (LAD_Q100, "q100")):
            E["sketch"](o, [(0.0, lv), (xe, lv)], "flood lines", fl, E["PEN_FINE"], over=0.0, retrace=False,
                        dashed=True, z=E["Z_LINE"])
            E["level_mark"](o, 3 * w + 26.0 if lv == LAD_Q500 else 3 * w + 20.0, lv, fl, "flood lines")
            T("levels", nm)
    if sea["key"] == "low":                           # the farms are watered from storage in summer: the one arrow
        E["hand_arrow"](o, (3 * w + 22.0, gy[4] + 6.5), (4 * w + 9.0, gy[4] + 5.5), E["SITE_WATER_D"], bend=-0.15)
        T("water", "stored_water_arrow")
    if sea["mark"] == "winter":
        E["cloud_rain"](o, mark_xy[0], mark_xy[1], 2.0)
        T("annotations", "season_mark")
    elif sea["mark"] == "summer":
        E["sun"](o, mark_xy[0], mark_xy[1], 1.7)
        T("annotations", "season_mark")
    E["sketch"](o, gs, "ground lines", E["SKINK"], E["PEN_BOLD"], z=E["Z_LINE"])   # the cut: the gesture
    T("ground", "ground_line")
    return [(e[2], tags.get(e[1], ("other", "sketch"))) for e in sorted(E["ZP"], key=lambda e: (e[0], e[1]))]


def sk_draw(pg, items):
    """sketch-engine items (already placed with xform) on this script's recorder"""
    for it in items:
        if it[0] == "poly":
            _, rings, fill, stroke, lw, dash, _st, alpha = it
            pg.path(rings, fill, stroke, lw, True, dash, alpha)      # stripes (hatches) are never drawn
        elif it[0] == "line":
            _, pts, stroke, lw, dash, _cap = it
            pg.line(pts, stroke, lw, dash)
        elif it[0] == "circle":
            _, cx, cy, r, fill, stroke, lw = it
            pg.circle(cx, cy, r, fill, stroke, lw)
        elif it[0] == "text":
            _, s, x, y, h, col, bold, align, _m, _halo = it
            pg.text(s, x, y, h / 0.3528, col, bool(bold), align or "L")


# the one-way chain along the stream, upstream to the farms: (name, marker, programme, historic root, sources)
CHAIN = [("UPSTREAM ENTRY", "reeds", "reed basins clean once · terraces hold", None, (CHAIN_REF,)),
         ("K4", "hub", "hub + sub-hub · water-touching step", "Roman bridge · Tabaklar Hamamı", (PROG,)),
         ("K3", "hub", "hub + sub-hub · craft workshops", "tanning quarter (Tabakhane)", (PROG,)),
         (u"İSTİKLAL MEYDANI", "small", "hidden-stream square", u"over the %s tunnels" % landmark_name("kizil_avlu"), (PROG,)),
         ("K5", "hub", "hub + sub-hub · Demeter's Garden", "Roman bridge · Demeter, abundance", (PROG, GARDEN)),
         ("K6", "gate", "gateway out", None, (PROG,)),
         ("DOWNSTREAM REACH", "reeds", "floodable planting · boardwalk", "Late Antique workshops", (CHAIN_REF, PROG)),
         ("FARMLAND", "outside", "outside the site · water from storage", "Tersane cotton (16th c.)", (COTTON_H,))]


def chain_strip(pg, y_top):
    """the chain across the page: node names, the one-way water ribbon with hubs and sub-hubs, programme keywords and
    the historic roots (HER r2). v11: the symbol key is the legend item ag3_legend (G6-4: no key on the drawing).
    Returns the lowest y used."""
    n = len(CHAIN)
    x0, dx = 16.0, (404.0 - 16.0) / n
    yr = y_top - 6.0                                 # the ribbon
    xs = [x0 + 2.0 + i * dx for i in range(n)]
    wc, wd = _hu("WAT", 3), _hu("WAT", 2)
    pg.tag("water", "ribbon")
    pg.line([(xs[0], yr), (xs[2], yr)], wc, 1.6)
    pg.line([(xs[3] + dx * 0.5, yr), (xs[-1] - 4.0, yr)], wc, 1.6)
    pg.poly([(xs[-1] - 4.0, yr + 1.8), (xs[-1] - 0.6, yr), (xs[-1] - 4.0, yr - 1.8)], fill=wc, closed=True)
    pg.tag("water", "covered_reach")
    pg.line([(xs[2], yr), (xs[3] + dx * 0.5, yr)], wc, 1.6, (1.6, 1.1))   # the covered reach
    pg.tag("water", "flow_arrows")
    for i in range(n - 2):                           # one way, with the stream
        ax = (xs[i] + xs[i + 1]) / 2.0 + 4.0
        pg.poly([(ax - 1.2, yr + 1.1), (ax + 0.6, yr), (ax - 1.2, yr - 1.1)], fill=wd, closed=True)
    low = yr
    for i, (name, mk, prog, root, refs) in enumerate(CHAIN):
        x = xs[i]
        pg.tag("hubs" if mk in ("hub", "small", "gate") else ("plants" if mk == "reeds" else "fields"),
               "chain_" + name.lower().replace(" ", "_"))
        if mk == "hub":
            pg.rect(x - 1.6, yr - 1.6, 3.2, 3.2, fill=_hu("PUB", 3), stroke=_hu("PUB", 2), lw=0.2)
            pg.circle(x, yr - 3.4, 0.8, fill=_hu("PUB", 2))
        elif mk == "small":
            pg.rect(x - 1.1, yr - 1.1, 2.2, 2.2, fill=C["white"], stroke=_hu("PUB", 3), lw=0.4)
        elif mk == "gate":
            pg.line([(x - 1.2, yr + 1.8), (x + 0.8, yr), (x - 1.2, yr - 1.8)], C["ink"], 0.4)
        else:
            _ag_icon(pg, "clean" if mk == "reeds" else "outside", x - 2.5, yr + 7.5, 5.0)
        pg.tag("labels", "chain_" + name.lower().replace(" ", "_"))
        tx = x - 1.5
        pg.text(name, tx, yr + 3.6 if mk not in ("reeds", "outside") else yr + 8.4, 8.5, C["ink"], True)
        y = yr - 7.0                               # clear of the sub-hub dot
        mark = "".join(cite(r) for r in refs)
        lines = [(q, C["ink"]) for q in wrap(prog + ("" if root else (" " + mark if mark else "")), 7, dx - 3.0)]
        if root:
            lines += [(q, _hu("HER", 2)) for q in wrap(root + (" " + mark if mark else ""), 7, dx - 3.0)]
        for q, col in lines:
            pg.text(q, tx, y, 7, col)
            y -= 2.9
        low = min(low, y + 2.9 - 1.2)
    return low


WE_DO = [(1, "clean once, at the upstream end"), (2, "hold winter water"), (3, "strip first, all summer"),
         (4, "plant each step for the water it gets"), (5, "surplus to the farms outside, never drinking")]


def _ag3_photo(pg, key, x, top, h=None):
    """v11: a plant's photo as an image shape (x, top - PHOTO_H)..(x + PHOTO_W, top), cover-cropped to the box by a
    clip (never stretched), with a keep area. False (nothing drawn) when the photo did not load."""
    p, _cr, why = photo_get(key)
    PHOTO_N[1] += 1
    if not p:
        AG3_NOPHOTO.append((key, why or "not loaded"))
        return False
    px = None
    try:
        with open(p, "rb") as fh:
            px = jpeg_info(fh.read())
    except Exception:
        px = None
    W, H = PHOTO_W, (h or PHOTO_H)                     # v13: h = the bands' AG3_PH_H; the notes photo keeps PHOTO_H
    y0 = top - H
    if px and px[0] > 0 and px[1] > 0:
        s = max(W / float(px[0]), H / float(px[1]))
        iw, ih = px[0] * s, px[1] * s
    else:
        iw, ih = W, H
        LOG_NOTES.append("FLAG p17 photo %s: size not read, set to the box" % key)
    pg.image(x + (W - iw) / 2.0, y0 + (H - ih) / 2.0, iw, ih, p, clip=(x, y0, x + W, y0 + H))
    pg.keep((x, y0, x + W, top), "photo " + key, "photo")
    PHOTO_N[0] += 1
    return True


def ag3_bands(pg, top, pn=None):
    """the plant bands under the three rows (one column under each step) and, left, what goes, the odour and how to
    read the steps (28 Oct page_ladder part 3). Every plant of a step with its photo PHOTO_W x AG3_PH_H (v13), two side by
    side, its name "English (Turkish)" + the photo's credit mark under it, then the species' reason (v12, L6: always
    exported; the booklet places it; the 28 Oct "only when there is room" rule is the booklet's). v11: a species whose photo did not load is never an empty box: it is named in one line "also:" under
    its band's photos and logged (BRIEF §6 row 17). v11: the left column goes into pn (its own drawing ag3_notes,
    booklet frame "ag3_note*"), the bands + photos stay in pg. Returns (lowest y of pg, lowest y of pn)."""
    pn = pn or pg
    yt = top - 3.0
    w = LAD_S * LAD_F
    per = 2 if 2 * PHOTO_W + PH_GAP <= w - 2.0 else 1
    lowest = yt
    for i, st in enumerate(STEPS):
        xa = LAD_X0 + i * w + 1.0
        el = "band_" + st["name"].lower().replace(" ", "_")
        pg.tag("labels", el)
        y = yt
        pg.text(st["name"], xa, y, 8.5, C["ink"], True); y -= 3.4
        pg.text(st["sub"], xa, y, 7, C["ink2"]); y -= 6.4
        tag_y = y
        y -= 4.0
        if st["band"]:
            l_, r_ = GEO["corridor"]["left " + st["band"]], GEO["corridor"]["right " + st["band"]]
            v = [(l_[k] + r_[k]) / 2.0 for k in ("trees", "grass", "farmland")]
            for q in wrap("today: trees %.0f %% · grass %.0f %% · fields %.0f %% %s" % (v[0], v[1], v[2], cite(TODAY)), 7, w - 4.0):
                pg.text(q, xa, y, 7, C["ink2"]); y -= 2.9
        if st["name"] == "FARMS":
            rm = cite(REUSE)
            for q in wrap(STEPS[4]["water"][1].replace(" {reuse}", (" " + rm) if rm else ""), 7, w - 4.0):
                pg.text(q, xa, y, 7, C["ink2"]); y -= 2.9
        y -= 1.2
        sm = cite(SPECIES)
        pg.text(("WE PLANT" + ((" " + sm) if sm else "")) if st["name"] != "FARMS" else "THEY GROW", xa, y, 7,
                _hu("GRN", 1), True)
        y -= 1.6                                     # the top of the first row of photos
        got = [(key, why) for key, why in st["plant"] if photo_get(key)[0]]
        miss = [key for key, _ in st["plant"] if not photo_get(key)[0]]
        low = y
        rs = [why for _k, why in got if why]       # v13 (L6): a reason shared by 2+ plants of a step prints once,
        shared = [r for i_, r in enumerate(rs) if rs.count(r) > 1 and rs.index(r) == i_]   # under the photos
        for r0 in range(0, len(got), per):
            yl = y - AG3_PH_H - 2.5                   # v12 (L6): the lowest baseline of this row's name + reason lines
            for c_, (key, why) in enumerate(got[r0:r0 + per]):
                px = xa + c_ * (PHOTO_W + PH_GAP)
                pg.tag("plants", "%s_%s" % (el, key))
                _ag3_photo(pg, key, px, y, AG3_PH_H)
                pg.tag("labels", "%s_%s" % (el, key))
                yy = y - AG3_PH_H - 2.5
                nl = name_lines(key, photo_mark(key), 7, PHOTO_W)
                for q in nl:
                    pg.text(q, px, yy, 7, C["ink"], True); yy -= 2.6
                why = None if why in shared else why    # v13: shared reasons print once below
                for q in (wrap(why, 6.5, PHOTO_W) if why else []):   # v12 (L6): the species' reason always exported
                    pg.text(q, px, yy, 6.5, C["ink2"]); yy -= 2.4  # (28 Oct rule "only when there is room" = booklet's job)
                yl = min(yl, yy + (2.4 if why else 2.6))
            low = yl - 0.6
            y = low - 1.1
        for r in shared:                             # v13: "cotton, corn, tomato: <reason>" once, full column width
            pg.tag("labels", el + "_shared")
            nm = ", ".join(name_lc(k) for k, why in got if why == r)
            for q in wrap(nm + ": " + r, 6.5, w - 4.0):
                pg.text(q, xa, y - 1.4, 6.5, C["ink2"]); y -= 2.4
            low = y - 0.6
        for key in miss:                             # no empty box: the name in one line, logged
            AG3_NOPHOTO.append((key, photo_get(key)[2] or "not loaded"))
            PHOTO_N[1] += 1
        if miss:
            pg.tag("labels", el + "_no_photo")
            for q in wrap("also: " + ", ".join(plant_name(k) for k in miss), 7, w - 4.0):
                y -= 0.6
                pg.text(q, xa, y - 2.0, 7, C["ink"], True)
                y -= 2.9
            low = y
        lowest = min(lowest, low)
        pg.tag("annotations", el + "_job")
        pg.rect(xa, tag_y, text_w(st["job"], 8, True) + 4, 5.2, fill=_hu("GRN", 1))
        pg.text(st["job"], xa + 2, tag_y + 1.5, 8, C["white"], True)
        jx = xa + text_w(st["job"], 8, True) + 6
        for word, kind in JOB_ICON:                  # the job as pictograms beside the tag
            if word in st["job"]:
                _ag_icon(pg, kind, jx + 0.5, tag_y + 5.6, 5.0)
                pg.keep((jx + 0.5, tag_y + 0.6, jx + 5.5, tag_y + 5.6), "job icon " + kind, "icon")
                jx += 7.0
    # left column: what goes, the odour, how to read the steps (v11: its own recorder pn)
    pg = pn
    pg.tag("labels", "remove_giant_reed")
    y = yt
    gm = photo_mark("giant_reed")
    for t, sz, b in ((u"REMOVE: " + plant_name("giant_reed") + ((" " + gm) if gm else ""), 8, True),
                     ("raises flood risk, blocks bridges", 7, False)):
        for q in wrap(t, sz, LAD_X0 - 18.0, b):
            pg.text(q, 14.0, y, sz, C["ink"], b)
            y -= sz * 0.3528 * 1.35
    pg.tag("plants", "remove_giant_reed")
    if _ag3_photo(pg, "giant_reed", 14.0, y + 1.4):
        y -= PHOTO_H + 0.6
    y -= 3.0
    pg.tag("labels", "odour")
    sm = cite(SPECIES)
    for t, b in (("ODOUR: no measured plant effect" + ((" " + sm) if sm else ""), True), ("keep sewage out", False),
                 ("clean once, at the upstream end", False), ("plants: clean nutrients, give scent", False)):
        for q in wrap(t, 7.5, LAD_X0 - 18.0, b):
            pg.text(q, 14.0, y, 7.5, C["ink"], b); y -= 3.2
    y -= 3.0
    pg.tag("labels", "reading_notes")
    for t in ("steps = planting bands " + cite(BANDS), "depths above the bed " + cite(DEPTH), "a diagram, not to scale",
              "downstream flat end: Q100 1.4 m, Q500 1.5 m"):
        for q in wrap(t.strip(), 7, LAD_X0 - 18.0):
            pg.text(q, 14.0, y, 7, C["ink2"]); y -= 2.9
    return lowest, y


def ag_p17_items(ix):
    """v11 (round 6 S7): booklet p17 as items, drawn at the 28 Oct sheet places (A3 mm, y up) into one recorder per
    item and exported by ag_export_block (chain, three season rows, bands) + the steps list and the symbol key.
    Logs: section p17 ladder_<season> SKETCH (x3), legend p17 hues=table, trees p17 species=n generic=n."""
    CUR_PAGE[0] = AG3_PAGE
    AG3_TREES[0] = AG3_TREES[1] = 0
    del AG3_NOPHOTO[:]
    ix.list(AG3_PAGE, None, [lab for _, lab in WE_DO], numbered=True, id=AG3_ID["steps"], group=AG3_ID["chain"])
    ix.legend(AG3_PAGE, None, [
        (dict(kind="fill", colour=_hu("PUB", 3), stroke=_hu("PUB", 2), width_pt=0.6), "hub square, dry"),
        (dict(kind="dot", colour=_hu("PUB", 2)), "sub-hub in the bed, floodable"),
        (dict(kind="dash", colour=_hu("WAT", 3), width_pt=4.5, dash_pt=[4.5, 3.1]), "covered reach"),
        (dict(kind="line", colour=_hu("WAT", 3), width_pt=4.5), "one way, with the stream")],
        id=AG3_ID["legend"], group=AG3_ID["chain"])
    hue_log(AG3_PAGE, LOG_NOTES)                     # v13 (G7-4): the table's own log call (was the line by hand)
    pg = AgRec()
    y_chain = chain_strip(pg, 264.0)
    ag_export_block(ix, pg, AG3_ID["chain"], 1, 13.0, 270.0, 394.0, 270.0 - (y_chain - 1.0), 0.0, page=AG3_PAGE)
    top = y_chain - 2.0
    for r, sea in enumerate(seasons()):
        T_, B = top - r * ROW_H, top - (r + 1) * ROW_H
        y0 = B + 2.0 - LAD_GB * LAD_F                # page y of the sketch's 0
        mark = ((19.0 - LAD_X0) / LAD_F, (T_ - 6.0 - y0) / LAD_F)
        pg = AgRec()
        for it, (kind, eid) in ladder_row(sea, mark):
            pg.tag(kind, eid)
            sk_draw(pg, xform([it], LAD_F, LAD_X0, y0))
        pg.tag("labels", "season_column")
        if sea["mark"] == "olive":
            _ag_icon(pg, "olive", 14.0, T_ - 1.5, 9.0)
        pg.text(sea["name"], 26.0, T_ - 8.0, 12, C["ink"], True)
        pg.text(sea["months"], 26.0, T_ - 13.0, 9, _hu("WAT", 1), True)
        y = T_ - 18.5
        for t, ref in sea["side"]:
            mk = cite(ref) if ref else ""
            for q in wrap(t + ((" " + mk) if mk else ""), 7.5, LAD_X0 - 30.0):
                pg.text(q, 26.0, y, 7.5, C["ink"])
                y -= 3.2
        Y = lambda v: y0 + v * LAD_F
        X = lambda v: LAD_X0 + v * LAD_F
        fl = _hu("WAT", 1)
        if sea["key"] == "high":                     # flood levels first: they sit at their lines
            pg.tag("levels", "q500")
            dm = cite(DEPTH)
            pg.text("Q500 · 263 m³/s · 2.3-3.3 m above the bed" + ((" " + dm) if dm else ""), X(1.5), Y(LAD_Q500) + 0.8,
                    7, fl, positions=("NE", "N", "E"))
            pg.tag("levels", "q100")
            pg.text("Q100 · 205 m³/s · 2.0-3.0 m", X(1.5), Y(LAD_Q100) - 0.8 - 7 * 0.3528, 7, fl,
                    positions=("SE", "S", "E"))
            pg.tag("labels", "overtopping")
            pg.text("over the bank top only at K4 (right bank) and S4 (left)", X(3 * LAD_S + 3.0), Y(LAD_Q500) + 3.0,
                    7, fl, positions=("NE", "N", "NW", "E"))
            pg.tag("labels", "site_edge")
            pg.text("site edge: farmland outside", X(4 * LAD_S) + 1.0, Y(LAD_GY[4] + 6.0) + 0.6, 7, C["ink2"],
                    positions=("NE", "E", "N"))
        if sea["key"] == "low":
            pg.tag("labels", "stored_water_arrow")
            pg.text("stored winter water", X(3 * LAD_S + 22.0), Y(LAD_GY[4] + 6.5) + 1.0, 7, _hu("WAT", 2), True,
                    positions=("N", "NE", "NW"))
        for n_, (kind, x, yv, flip, lab, ref, al) in enumerate(sea["acts"]):
            if lab:
                pg.tag("labels", "act_%d" % n_)
                hgt = 0.0 if kind is None else (3.2 if kind == "sit" else 4.9)
                mk = cite(ref) if ref else ""
                ax = X(4 * LAD_S) + 1.5 if (al == "L" and x > 4 * LAD_S) else X(x)
                pg.text(lab + ((" " + mk) if mk else ""), ax, Y(yv + hgt) + 1.0, 7, C["ink"], True, al,
                        positions=("N", "NE", "NW", "E", "W") if al == "C" else
                        (("NE", "E", "N") if al == "L" else ("NW", "W", "N")))
        did = AG3_ID[sea["key"]]
        ag_export_block(ix, pg, did, 2 + r, 13.0, T_, 394.0, ROW_H, 0.0, page=AG3_PAGE)
        LOG_NOTES.append("section p17 %s SKETCH" % did.replace("ag3_", ""))
    bot = top - 3 * ROW_H
    pg, pn = AgRec(), AgRec()
    low, low_n = ag3_bands(pg, bot, pn)
    bx = LAD_X0 - 2.0                            # v11: bands + photos from the cut's left edge; the notes left of it
    ag_export_block(ix, pg, AG3_ID["bands"], 5, bx, bot, 13.0 + 394.0 - bx, bot - (low - 1.0), 0.0, page=AG3_PAGE)
    ag_export_block(ix, pn, AG3_ID["notes"], 6, 13.0, bot, bx - 4.0 - 13.0, bot - (low_n - 1.0), 0.0, page=AG3_PAGE)
    LOG_NOTES.append("trees p17 species=%d generic=%d" % tuple(AG3_TREES))
    for key, why in AG3_NOPHOTO:
        ix.warn(AG3_PAGE, "photo", u"no photo for %s (%s): its box is left out, the name is under the band" % (
            plant_name(key), why))
    CUR_PAGE[0] = AG_PAGE
