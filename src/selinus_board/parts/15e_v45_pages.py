# ============================================================ v45 (Aras 27 Oct 17:34, booklet Prompt 2: site and stream edge)
# Booklet p.2 "What is there": the site readings beside plan 01 (the six bank readings as bars and the land-use ring
# with its key, one panel: crop drw_site_readings). p.6 "The stream edge and where we can build" (crop drw_edge_build,
# replaces the v44 edge plan): the whole site frame at 1:5,000 in two stacked strips, drawn crisp in the masterplan's
# drawing language as the masterplan's "before": the edge type every 4 m on both banks, walls and embankments, the
# ground open to change hatched, bridges K1-K6, the eight photo viewpoints as numbered discs with their view cones,
# the photos beside it and the edge shares in a slim panel. The cuts S1-S8 are drawn on no map any more: each sections
# page has one small key map (crop sec_sections_key_n, set in the booklet's title band). Sizes are in booklet mm
# (k = board units per booklet mm, as in v44); text never under 7 pt on the booklet page.
# v50 (MIRAQUA 28 Oct, P06.1-P06.4, P22.1): p.6 and p.22 are drawn in parts/15k_r28_edge.py (ONE strip at 1:10,000,
# G7; vector hatches, P06.2); EB_DEN, EB_N, OPEN_TINT, OPEN_HATCH, eb_hatched and draw_eb_base are gone.
P01_BK_W = 232.0        # mm: plan 01's width on the booklet page beside the site readings (sets its label sizes)
RD_BK_W = 156.0         # mm: the site readings' width on the booklet page
EB_CONE_M = 45.0       # m: the drawn length of a photo's view cone (its angle is the camera's, from the photo)
EB_COL_X = 297.0        # v49: mm from the panel's left edge to the spread copy's column (booklet grid column 10, as the
#                         masterplan page beside it)
WHITE = (255, 255, 255)
# the masterplan's tones (bergama_masterplan COL, ROAD_TONE, RIVER_BAND_TONE, MP["agriculture"]; palette v1.4)
MPL = {"bld": C("D8D5CC"), "her": C("E4CAC9"), "her_edge": C("AF7474"), "water": C("91ADB4"),
       "water_edge": C("5D7F8D"), "tree": C("C4CCB5"), "park": C("DFEBC0"), "field": C("C6C08D"),
       "road": C("CFCCC5"), "road_edge": C("847E75"), "ink_dark": C("2C2219")}
# each photo's camera bearing (degrees from true north) and 35 mm-equivalent focal length, from the original's EXIF
# (GPSImgDirection, ref T; FocalLengthIn35mmFilm): library/_index/site_photos/site_photos.tsv (site visit 2026-10-01)
PHOTO_VIEW = {"IMG_5752": (253.18, 24), "IMG_5774": (234.64, 14), "IMG_5779": (72.63, 24), "IMG_5785": (25.00, 24),
              "IMG_5794": (54.34, 24), "IMG_5802": (303.45, 24), "IMG_5815": (66.92, 24), "IMG_5833": (122.79, 24)}
EDGE_SRC = ("Stream edges: what meets the water along each bank, sampled every 4 m along the surveyed banks (nearest "
            "building within 8 m, walkable path or stairs, street, parking, planted ground; else loose); walled = a "
            "surveyed wall within 3 m, embanked = only a surveyed slope line within 3 m.")
OPEN_SRC = ("Ground open to change: open (vacant) ground and parking & yards as mapped (survey, OpenStreetMap); loose "
            "ground = the frame's unmapped ground that ESA WorldCover 2021 classes as grassland or shrubland (2 m "
            "raster). A reading of what could change, not a check of ownership or zoning. Drawn as the raster's "
            "outlines, simplified and smoothed; every area is counted on the raster.")   # v50 (MIRAQUA 28 Oct, P06.2)
EB_EDGE_LAB = {"building": u"Built edge · enclosed", "street": u"Street edge · visible",
               "pedestrian": u"Walkable edge · accessible", "green": u"Planted edge · permeable",
               "parking": u"Parking edge · transformable", "open": u"Loose edge · transformable"}


def bk_lw(mm, k):
    """v45: the sheet line weight (mm) that prints mm wide on the booklet page (k = board units per booklet mm)."""
    return mm * k / 10.0


def photo_fov(f35):
    """v45: a photo's horizontal angle of view (radians) at 35 mm-equivalent focal length f35: the 4:3 frame's width
    is 34.6 mm of the 43.27 mm reference diagonal (the data pack's photos keep the full 4:3 frame)."""
    return 2.0 * math.atan(34.6 / (2.0 * f35))


def draw_north_at(B, F, x, y, a_mm, k, L, order=60):
    """v45: a north arrow a_mm long centred on (x, y), for a map drawn on F's axes (page x = u), set beside its scale
    bar, never on the map. Returns its half-width (board units)."""
    a = math.atan2(math.cos(F.ang), math.sin(F.ang))
    c, s = math.cos(a - math.pi / 2), math.sin(a - math.pi / 2)
    q = a_mm * k / 1.3

    def R(px, py):
        return (x + c * px - s * py, y + s * px + c * py)
    tip, l, m, r = R(0, 0.75 * q), R(-0.38 * q, -0.5 * q), R(0, -0.22 * q), R(0.38 * q, -0.5 * q)
    B.fill([[tip, l, m]], INK, L, order)
    B.fill([[tip, m, r]], WHITE, L, order)
    B.line([tip, l, m, r, tip], INK, L, order + 1, bk_lw(0.15, k))
    nx, ny = R(0, 1.15 * q)
    B.text("N", nx, ny, bk_hk(7.0, k), INK, L, order=order + 1, font=FONT_TITLE, bold=True, align="MC")
    return 1.4 * q


def draw_scalebar_bk(B, x, y, ss, Lm, k, L, order=60):
    """v45: a scale bar for the booklet page: four parts, Lm metres at ss board units per metre, its top at y and its
    numbers 7 pt UNDER it (clear of the drawing above). Returns the y below the numbers."""
    bh, seg = 1.2 * k, Lm / 4.0 * ss
    for i in range(4):
        B.fill([rect(x + i * seg, y - bh, x + (i + 1) * seg, y)], INK if i % 2 == 0 else WHITE, L, order)
    B.line(rect(x, y - bh, x + 4 * seg, y) + [(x, y - bh)], INK, L, order + 1, bk_lw(0.15, k))
    h = bk_hk(7.0, k)
    yt = y - bh - 1.0 * k - h
    for v in (0.0, Lm / 2.0):
        B.text(u"{:,.0f}".format(v), x + v * ss, yt, h, INK, L, order=order + 1, font=FONT_TITLE, align="C")
    t = u"{:,.0f}".format(Lm)
    B.text(t + u" m", x + Lm * ss - 0.5 * tw(t, h, "sans"), yt, h, INK, L, order=order + 1, font=FONT_TITLE)
    return yt - 0.8 * k


# ------------------------------------------------------------ p.2 the site readings beside plan 01
def reading_rows(S):
    """v45: the key question's six readings: (name, phrase, [(m of bank, colour)]), stacked parts dark first."""
    e = S.edge_len
    wl, em = S.walled_len, getattr(S, "embanked_len", 0.0)
    tot = sum(e.values()) or 1.0
    return [("ACCESSIBLE", u"walkable edges within reach", [(e.get("pedestrian", 0.0), EDGE["pedestrian"][1])]),
            ("VISIBLE", u"street edges, seen across the water", [(e.get("street", 0.0), EDGE["street"][1])]),
            ("PERMEABLE", u"planted edges that let the ground through", [(e.get("green", 0.0), EDGE["green"][1])]),
            ("ENCLOSED", u"built edges: backs of buildings face the bed", [(e.get("building", 0.0), INK)]),
            ("DISCONNECTED", u"walled {:.0f}% · embanked {:.0f}%: cut off from the street".format(
                100.0 * wl / tot, 100.0 * em / tot), [(wl, INK2), (em, mix(INK2, PAPER, 0.5))]),
            ("TRANSFORMABLE", u"parking {:.0f}% · loose {:.0f}%: open to change".format(
                100.0 * e.get("parking", 0.0) / tot, 100.0 * e.get("open", 0.0) / tot),
             [(e.get("parking", 0.0), EDGE["parking"][1]), (e.get("open", 0.0), EDGE["open"][1])])]


def landuse_slices(S):
    """v45: the site frame's ground in plan 01's own colours, for the land-use ring: [(label, colour, m2)]: buildings
    by use, the streets' measured surface, parking & yards, woods and tree cover, parks, grass, shrubs, fields,
    orchards (inferred), vacant ground, the stream and the unmapped rest; under 0.5 % joined as "others"."""
    lcc = dict((k_, c_) for k_, l_, c_ in LC_CLASSES)
    tz = sum(z["A"] for z in S.zones if z["kind"] == "transport")
    gz = {}
    for z in S.zones:
        if z["kind"] == "green":
            sub = z.get("sub") if z.get("sub") in GREEN_SUB else "park"   # as on the plan: other greens in the park tone
            gz[sub] = gz.get(sub, 0.0) + z["A"]
    rows = [(short(CAT[k_][0]), CAT[k_][1], S.area.get(k_, 0.0)) for k_ in
            ("residential", "mixed", "commercial", "institutional", "religious", "industrial")]
    rows += [(u"Streets", ROAD_FILL, max(0.0, S.area.get("transport", 0.0) - tz)),
             (u"Parking & yards", mix(CAT["transport"][1], PAPER, 0.3), tz),
             (u"Woods & tree cover", GREEN_SUB["wood"], gz.get("wood", 0.0) + rest_of(S, "trees")),
             (u"Parks", GREEN_SUB["park"], gz.get("park", 0.0)),
             (u"Grass", GREEN_SUB["grass"], gz.get("grass", 0.0) + rest_of(S, "grass")),
             (u"Shrubs", lcc.get("shrub", mix(CAT["green"][1], PAPER, 0.3)), rest_of(S, "shrub")),
             (u"Fields & orchards, mapped", CAT["agri"][1], S.area.get("agri", 0.0) + rest_of(S, "farmland")),
             (u"Orchards, inferred", lcc.get("orchard", ORCH_C), rest_of(S, "orchard")),
             (u"Vacant ground", CAT["vacant"][1], S.area.get("vacant", 0.0)),
             (u"The stream", CAT["water"][1], S.area.get("water", 0.0)),
             (u"Other unmapped", REST_C, rest_of(S, "rest"))]
    tot = frame_total(S) or 1.0
    rows.append((u"Others", mix(PAPER, INK2, 0.45), max(0.0, tot - sum(a for _l, _c, a in rows))))
    keep = [r_ for r_ in rows[:-1] if r_[2] >= 0.005 * tot]
    small = sum(r_[2] for r_ in rows if r_[2] < 0.005 * tot) + (rows[-1][2] if rows[-1][2] >= 0.005 * tot else 0.0)
    if small > 0.0005 * tot:
        keep.append((u"Others, each under 0.5%", rows[-1][1], small))
    return keep, tot


def draw_site_readings(S, B, x, y, w, U):
    """v45 (p.2: old p.4 "grain of the town" folded in): the six readings of the bank (accessible ... transformable)
    as bars, and the land use of the site frame as a ring with its key, in plan 01's colours; one panel w wide,
    designed for RD_BK_W mm beside plan 01 on the booklet page. Returns the y below. v50 (MIRAQUA 28 Oct, P02.1,
    P02.2): the ring's key on the panel's two-column grid; the stream edge diagram (draw_edge_types, its own crop
    drw_edge_types) drawn under the panel."""
    L = "LU_BOARD::SiteReadings"
    k = w / RD_BK_W
    h7, h75, h8, h9, h12 = (bk_hk(p_, k) for p_ in (7.0, 7.5, 8.0, 9.0, 12.0))
    hw = 74.0 * k                                         # each half; 8 mm between them
    top = y
    # left: the bars
    tot = sum(S.edge_len.values())
    B.text(u"WHERE IS THE STREAM ...?", x, y - h8, h8, INK, L, font=FONT_TITLE, bold=True)
    B.text(u"% of the bank length · both banks · every 4 m " + bcite(EDGE_SRC), x, y - h8 - 1.6 * k - h7, h7, INK2,
           L, font=FONT_TITLE)
    yy = y - h8 - 1.6 * k - h7 - 4.0 * k
    if tot > 0:
        for name, phrase, parts in reading_rows(S):
            pct = 100.0 * sum(v_ for v_, c_ in parts) / tot
            B.text(name, x, yy - h75, h75, INK, L, font=FONT_TITLE, bold=True)
            site28_text(B, u"**{:.0f}%**".format(pct), x + hw, yy - h9, h9, INK, L, align="R")   # v50: real width
            yb = yy - h9 - 1.0 * k
            B.fill([rect(x, yb - 2.2 * k, x + hw, yb)], FAINT, L, 20)
            bx = x
            for v_, c_ in parts:
                if v_ > 0:
                    B.fill([rect(bx, yb - 2.2 * k, bx + hw * v_ / tot, yb)], c_, L, 21)
                    bx += hw * v_ / tot
            yp = yb - 2.2 * k - 1.0 * k - h7
            B.text(phrase, x, yp, h7, INK2, L, font=FONT_TITLE)
            yy = yp - 3.0 * k
    low = yy
    # right: the land-use ring
    rx = x + w - hw
    sl, ftot = landuse_slices(S)
    B.text(u"LAND USE AND GROUND COVER", rx, y - h8, h8, INK, L, font=FONT_TITLE, bold=True)
    B.text(u"site frame · % of its {:,.1f} ha {}".format(ftot / 1e4, bcite(
        u"Land use and ground cover of the site frame (site_alan, {:,.1f} ha), as plan 01 draws it: buildings by use "
        u"and the measured street surfaces from the survey; parks, fields, vacant ground, parking and yards from the "
        u"survey and OpenStreetMap; the unmapped rest by satellite class.".format(ftot / 1e4)) + bcite(LC_CREDIT)),
        rx, y - h8 - 1.6 * k - h7, h7, INK2, L, font=FONT_TITLE)
    r1, r0 = 25.0 * k, 15.0 * k
    cx, cy = rx + 0.5 * hw, y - h8 - 1.6 * k - h7 - 4.0 * k - r1
    a0 = math.pi / 2.0
    for lab, col, a in sl:
        a1 = a0 - 2.0 * math.pi * a / ftot
        B.fill([annulus(cx, cy, r0, r1, a0, a1)], col, L, 20)
        B.line([(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)), (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0))],
               WHITE, L, 21, bk_lw(0.25, k))
        a0 = a1
    site28_text(B, u"**{:,.1f}**".format(ftot / 1e4), cx, cy + 0.6 * k, h12, INK, L, align="C")   # v50: real widths
    site28_text(B, u"ha", cx, cy - 1.4 * k - h7, h7, INK2, L, align="C")
    low = min(low, cy - r1)
    # under both: the ring's key (the plan's ground and green colours, so the plan needs no other key). v50 (MIRAQUA
    # 28 Oct, P02.1): on the panel's grid, two columns at the halves' left edges (0 and RD_BK_W - 74 mm: the grid of
    # the booklet's legend under the panel), each entry as the booklet's legend_item draws one: a 4.0 x 2.8 mm
    # swatch from 0.2 mm under the baseline, the name 5.5 mm in at 7.5 pt, 4.0 mm a row (were three columns, 7 pt)
    ky = low - 5.0 * k
    nr = (len(sl) + 1) // 2
    for j, (lab, col, a) in enumerate(sl):
        kx = x + (j // nr) * (w - hw)
        yk = ky - (j % nr) * 4.0 * k
        B.fill([rect(kx, yk - 0.2 * k, kx + 4.0 * k, yk + 2.6 * k)], col, L, 20)
        pct = 100.0 * a / ftot
        site28_fit(B, u"{} {}".format(lab, u"{:.0f}%".format(pct) if pct >= 1.0 else u"< 1%"), kx + 5.5 * k, yk, h75,
                   hw - 5.5 * k, INK, L)
    low = ky - (nr - 1) * 4.0 * k - 1.5 * k
    crop_panel("site_readings", x, low, x + w, top + 0.5 * k, u"Site readings · bank and ground")
    CROP_PANELS[-1]["bk_w"] = RD_BK_W                     # v45: its width on the booklet page (side panel of p.2) ...
    CROP_PANELS[-1]["grid"] = [0.0, RD_BK_W - 74.0]       # ... and its two halves' left edges (the legend under it)
    return draw_edge_types(S, B, x, low - 1.0 * U, w, U)  # v50 (P02.2): the stream edge alone, its own crop under it


# ------------------------------------------------------------ p.6 the stream edge and where we can build
def ground_open(S):
    """v45: the site frame's ground open to change, m2: (open (vacant) ground, parking & yards, loose ground, sum):
    the mapped vacant and parking zones, and the unmapped ground the satellite classes as grass or scrub."""
    vac = sum(z["A"] for z in S.zones if z["kind"] == "vacant")
    park = sum(z["A"] for z in S.zones if z["kind"] == "transport")
    loose = rest_of(S, "grass", "shrub")
    return vac, park, loose, vac + park + loose


def eb_caption(it, width, h):
    """v45: a photo's keyword caption on ONE line at height h: middle keywords left out until it fits width (real
    Helvetica runs about 0.72 x the capital height per character)."""
    parts = photo_caption(it).split(u" · ")
    est = (lambda t: len(t) * 0.72 * h)
    while len(parts) > 2 and est(u" · ".join(parts)) > width:
        del parts[-2]
    t = u" · ".join(parts)
    while len(t) > 6 and est(t) > width:
        t = t[:-2].rstrip(u" ·") + u"…"
    return t


# v50 (MIRAQUA 28 Oct, P06.1-P06.4, P22.1): draw_edge_build and draw_edge_build_e (p.6 and p.22, ONE strip at
# 1:10,000) are in parts/15k_r28_edge.py


# v50 (MIRAQUA 28 Oct, P04.1, P14.1): draw_sections_key (the sections pages' key map, was at 1:50,000, SK_DEN) is
# in parts/15l_r28_site.py, drawn at its booklet size
