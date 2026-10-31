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


# ------------------------------------------------------------ p.6 the stream edge and where we can build
def ground_open(S):
    """v45: the site frame's ground open to change, m2: (open (vacant) ground, parking & yards, loose ground, sum):
    the mapped vacant and parking zones, and the unmapped ground the satellite classes as grass or scrub."""
    vac = sum(z["A"] for z in S.zones if z["kind"] == "vacant")
    park = sum(z["A"] for z in S.zones if z["kind"] == "transport")
    loose = rest_of(S, "grass", "shrub")
    return vac, park, loose, vac + park + loose


# v50 (MIRAQUA 28 Oct, P06.1-P06.4, P22.1): draw_edge_build and draw_edge_build_e (p.6 and p.22, ONE strip at
# 1:10,000) are in parts/15k_r28_edge.py


# v50 (MIRAQUA 28 Oct, P04.1, P14.1): draw_sections_key (the sections pages' key map, was at 1:50,000, SK_DEN) is
# in parts/15l_r28_site.py, drawn at its booklet size
