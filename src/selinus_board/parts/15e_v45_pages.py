# ============================================================ v45 (Aras 27 Oct 17:34, booklet Prompt 2: site and stream edge)
# Booklet p.2 "What is there": the site readings beside plan 01 (the six bank readings as bars and the land-use ring
# with its key, one panel: crop drw_site_readings). p.6 "The stream edge and where we can build" (crop drw_edge_build,
# replaces the v44 edge plan): the whole site frame at 1:5,000 in two stacked strips, drawn crisp in the masterplan's
# drawing language as the masterplan's "before": the edge type every 4 m on both banks, walls and embankments, the
# ground open to change hatched, bridges K1-K6, the eight photo viewpoints as numbered discs with their view cones,
# the photos beside it and the edge shares in a slim panel. The cuts S1-S8 are drawn on no map any more: each sections
# page has one small key map (crop sec_sections_key_n, set in the booklet's title band). Sizes are in booklet mm
# (k = board units per booklet mm, as in v44); text never under 7 pt on the booklet page.
P01_BK_W = 232.0        # mm: plan 01's width on the booklet page beside the site readings (sets its label sizes)
RD_BK_W = 156.0         # mm: the site readings' width on the booklet page
EB_DEN = 5000           # the stream edge plan at 1:5,000 on the booklet page: two strips of 284.5 x 105.8 mm
EB_N = 2                # strips, cut along the frame's length, stacked (upstream on top)
EB_CONE_M = 45.0        # m: the drawn length of a photo's view cone (its angle is the camera's, from the photo)
EB_COL_X = 297.0        # v49: mm from the panel's left edge to the spread copy's column (booklet grid column 10, as the
#                         masterplan page beside it)
SK_DEN = 50000          # the sections pages' key map at 1:50,000 (57 x 11 mm: fits the booklet page's title band)
WHITE = (255, 255, 255)
# the masterplan's tones (bergama_masterplan COL, ROAD_TONE, RIVER_BAND_TONE, MP["agriculture"]; palette v1.4)
MPL = {"bld": C("D8D5CC"), "her": C("E4CAC9"), "her_edge": C("AF7474"), "water": C("91ADB4"),
       "water_edge": C("5D7F8D"), "tree": C("C4CCB5"), "park": C("DFEBC0"), "field": C("C6C08D"),
       "road": C("CFCCC5"), "road_edge": C("847E75"), "ink_dark": C("2C2219")}
OPEN_TINT = mix(C("E0B67D"), WHITE, 0.72)    # the ground open to change: the masterplan's "centre" tone, light ...
OPEN_HATCH = C("AA8148")                     # ... and its mid tone for the hatches
# each photo's camera bearing (degrees from true north) and 35 mm-equivalent focal length, from the original's EXIF
# (GPSImgDirection, ref T; FocalLengthIn35mmFilm): library/_index/site_photos/site_photos.tsv (site visit 2026-10-01)
PHOTO_VIEW = {"IMG_5752": (253.18, 24), "IMG_5774": (234.64, 14), "IMG_5779": (72.63, 24), "IMG_5785": (25.00, 24),
              "IMG_5794": (54.34, 24), "IMG_5802": (303.45, 24), "IMG_5815": (66.92, 24), "IMG_5833": (122.79, 24)}
EDGE_SRC = ("Stream edges: what meets the water along each bank, sampled every 4 m along the surveyed banks (nearest "
            "building within 8 m, walkable path or stairs, street, parking, planted ground; else loose); walled = a "
            "surveyed wall within 3 m, embanked = only a surveyed slope line within 3 m.")
OPEN_SRC = ("Ground open to change: open (vacant) ground and parking & yards as mapped (survey, OpenStreetMap); loose "
            "ground = the frame's unmapped ground that ESA WorldCover 2021 classes as grassland or shrubland (2 m "
            "raster). A reading of what could change, not a check of ownership or zoning.")
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
    designed for RD_BK_W mm beside plan 01 on the booklet page. Returns the y below."""
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
            B.text(u"{:.0f}%".format(pct), x + hw, yy - h9, h9, INK, L, font=FONT_TITLE, bold=True, align="R")
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
    B.text(u"{:,.1f}".format(ftot / 1e4), cx, cy + 0.6 * k, h12, INK, L, font=FONT_TITLE, bold=True, align="C")
    B.text(u"ha", cx, cy - 1.4 * k - h7, h7, INK2, L, font=FONT_TITLE, align="C")
    low = min(low, cy - r1)
    # under both: the ring's key, three columns (the plan's ground and green colours, so the plan needs no other key)
    ky = low - 5.0 * k
    cw = (w - 2.0 * 4.0 * k) / 3.0
    nr = (len(sl) + 2) // 3
    for j, (lab, col, a) in enumerate(sl):
        kx = x + (j // nr) * (cw + 4.0 * k)
        yk = ky - (j % nr) * 3.6 * k
        B.fill([rect(kx, yk - 0.3 * k, kx + 3.4 * k, yk + 2.1 * k)], col, L, 20)
        B.line(rect(kx, yk - 0.3 * k, kx + 3.4 * k, yk + 2.1 * k) + [(kx, yk - 0.3 * k)], INK2, L, 21, bk_lw(0.1, k))
        pct = 100.0 * a / ftot
        B.text(u"{} {}".format(lab, u"{:.0f}%".format(pct) if pct >= 1.0 else u"< 1%"), kx + 4.6 * k, yk, h7, INK, L,
               font=FONT_TITLE)
    low = ky - (nr - 1) * 3.6 * k - 1.5 * k
    crop_panel("site_readings", x, low, x + w, top + 0.5 * k, u"Site readings · bank and ground")
    CROP_PANELS[-1]["bk_w"] = RD_BK_W                     # v45: its width on the booklet page (side panel of p.2) ...
    CROP_PANELS[-1]["grid"] = [0.0, RD_BK_W - 74.0]       # ... and its two halves' left edges (the legend under it)
    return low - 1.0 * U


# ------------------------------------------------------------ p.6 the stream edge and where we can build
def ground_open(S):
    """v45: the site frame's ground open to change, m2: (open (vacant) ground, parking & yards, loose ground, sum):
    the mapped vacant and parking zones, and the unmapped ground the satellite classes as grass or scrub."""
    vac = sum(z["A"] for z in S.zones if z["kind"] == "vacant")
    park = sum(z["A"] for z in S.zones if z["kind"] == "transport")
    loose = rest_of(S, "grass", "shrub")
    return vac, park, loose, vac + park + loose


def eb_hatched(CB, Ps, k, L, order, angs):
    """v45: the ground open to change: the light tint and its hatch (1 mm apart on the booklet page) at angles angs."""
    if not Ps:
        return
    for i in range(0, len(Ps), 400):
        CB.fill(Ps[i:i + 400], OPEN_TINT, L, order)
        for a in angs:
            CB.hatch(Ps[i:i + 400], OPEN_HATCH, L, order + 1, 1.0 * k, math.radians(a), bk_lw(0.1, k))


def draw_eb_base(S, CB, V, k, L):
    """v45: the base of the stream edge plan through ClipB CB, crisp, in the masterplan's tones and its layer order
    (ground, green, water, buildings, bridges, roads): loose ground (unmapped grass or scrub) under the satellite
    trees and fields, then the mapped zones (parking & yards, vacant ground hatched as open to change), street
    surfaces, the stream and its edge, the covered course, buildings (heritage with its edge), bridges, street
    edges."""
    lc = getattr(S, "lc", {}) or {}
    eb_hatched(CB, V.Ps((lc.get("grass") or []) + (lc.get("shrub") or [])), k, L, 2, (135.0,))
    for key, col in (("trees", MPL["tree"]), ("farmland", MPL["field"]), ("orchard", MPL["field"])):
        rings = lc.get(key) or []
        for i in range(0, len(rings), 400):
            CB.fill(V.Ps(rings[i:i + 400]), col, L, 4)
    for z in S.zones:
        Ps = V.Ps(z["Ps"] + z["Hs"])
        if z["kind"] == "vacant":
            eb_hatched(CB, Ps, k, L, 6, (45.0,))
        elif z["kind"] == "transport":
            eb_hatched(CB, Ps, k, L, 6, (45.0, 135.0))
        elif z["kind"] == "green":
            CB.fill(Ps, MPL["tree"] if z.get("sub") == "wood" else MPL["park"], L, 6)
        elif z["kind"] == "agri":
            CB.fill(Ps, MPL["field"], L, 6)
    for rg_ in getattr(S, "road_net", None) or []:
        CB.fill(V.Ps([rg_["P"]] + rg_["H"]), MPL["road"], L, 8)
    for wt in S.water:
        CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), MPL["water"], L, 15)
    for P in getattr(S, "water_outline", []) or []:
        CB.line(V.P(P), MPL["water_edge"], L, 16, bk_lw(0.25, k))
    for q in getattr(S, "decks", []) or []:               # streets on decks over the water stay above it
        CB.fill([V.P(q)], MPL["road"], L, 17)
    for P in getattr(S, "covered", []) or []:             # the covered course under streets and roofs
        for d in dashes(V.P(P), 1.6 * k, 0.9 * k):
            CB.line(d, MPL["water_edge"], L, 18, bk_lw(0.35, k))
    her = lambda u: u.get("fabric") in ("monument", "sacred")
    mini_buildings(S, CB, V, L, lambda u: MPL["her"] if her(u) else MPL["bld"], order=20)
    for u in S.bld:
        if her(u):
            for P in u["parts"]:
                CB.line(V.P(P + [P[0]]), MPL["her_edge"], L, 21, bk_lw(0.12, k))
    for P in getattr(S, "bridges", []) or []:
        CB.line(V.P(P), MPL["ink_dark"], L, 25, bk_lw(0.3, k))
    for P in getattr(S, "road_lines_net", []) or []:
        CB.line(V.P(P), MPL["road_edge"], L, 30, bk_lw(0.18, k))
    for r_ in S.roads:
        if not r_.get("w"):
            CB.line(V.P(r_["P"]), MPL["road_edge"], L, 30, bk_lw(0.18, k))
    draw_r28_study(S, CB, V, k, L)                        # v50 (G8): the study area's outline on every base


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


def draw_edge_build(S, B, x, y, w, U, with_photos=True):
    """v49 (Prompt 7 task 4): with_photos=False draws the copy for the masterplan spread (draw_edge_build_e).
    v45 (Prompt 2, replaces v44's "what meets the water"): THE STREAM EDGE AND WHERE WE CAN BUILD. The whole site
    frame at 1:5,000 on the booklet page, cut along its length into two strips (upstream on top), in the masterplan's
    drawing language: what meets the water on both banks every 4 m (built, street, walkable, planted, parking, loose;
    walled and embanked marked), the ground open to change hatched (open ground, parking and yards, loose ground),
    bridges K1-K6, the photo viewpoints 1-8 as numbered discs with view cones (camera bearing and angle from the
    photos); beside it the eight photos with one-line captions and a slim panel of the edge shares, the walled and
    embanked rings and the open ground's areas. Designed for the full booklet panel width (BK_AW). Returns the y below."""
    L = "LU_BOARD::EdgeBuild"
    F = S.F
    k = w / BK_AW
    h7, h75, h8, h9 = bk_hk(7.0, k), bk_hk(7.5, k), bk_hk(8.0, k), bk_hk(9.0, k)
    ss = 1000.0 * k / EB_DEN                              # board units per metre: 1:5,000 on the booklet page
    mw, mh = F.w / EB_N * ss, F.h * ss
    gap = BK_GAP_MM * k
    top = y
    photos = []
    try:
        photos = photo_files(os.path.join(SELINUS_RES_DIR, "_site_photos")) if with_photos else []
    except Exception:
        LOG.append("WARNING: the site photos could not be read for the stream edge plan:\n" + traceback.format_exc())
    rd = 2.0 * k                                          # photo disc radius; its number 9 pt
    strips = []
    for i in range(EB_N):
        Fi = sub_frame(F, F.u0 + i * F.w / EB_N, F.u0 + (i + 1) * F.w / EB_N)
        yt = top - i * (mh + gap)
        V = View(Fi, ss, x, yt)
        r = (x, yt - mh, x + mw, yt)
        strips.append((Fi, V, r))
        CB = ClipB(B, r)
        B.fill([rect(*r)], WHITE, L, 1)
        draw_eb_base(S, CB, V, k, L)
        for typ, pts in getattr(S, "edge_runs", []):       # the edge every 4 m, both banks
            CB.line(V.P(pts), EDGE[typ][1], L, 40, bk_lw(1.0, k))
        for pts in getattr(S, "wall_runs", []):
            for d in dashes(V.P(pts), 1.2 * k, 0.9 * k):
                CB.line(d, WHITE, L, 41, bk_lw(0.4, k))
        for pts in getattr(S, "bank_runs", []):
            for d in dashes(V.P(pts), 0.2 * k, 1.1 * k):
                CB.line(d, WHITE, L, 41, bk_lw(0.4, k))
        taken, labels = [], []
        for kk, nm, bx, by in BRIDGES_K:                  # the six crossings: a bar across the stream
            if not Fi.inside(bx, by):
                continue
            px, py = V.p(bx, by)
            nrm = stream_normal(S, bx, by) or (0.0, 1.0)
            a_ = V.p(bx + nrm[0], by + nrm[1])
            ln = math.hypot(a_[0] - px, a_[1] - py) or 1.0
            e = ((a_[0] - px) / ln * 1.8 * k, (a_[1] - py) / ln * 1.8 * k)
            CB.line([(px - e[0], py - e[1]), (px + e[0], py + e[1])], MPL["ink_dark"], L, 45, bk_lw(0.8, k))
            taken.append((px - 1.8 * k, py - 1.8 * k, px + 1.8 * k, py + 1.8 * k))
            labels.append(([kk], px, py, h9, INK))
        for j, (p, it) in enumerate(photos):              # viewpoints: cone from the camera, disc behind it
            if not Fi.inside(it["x"], it["y"]):
                continue
            px, py = V.p(it["x"], it["y"])
            brg, f35 = PHOTO_VIEW.get(it.get("file", "").split(".")[0], (None, None))
            dx, dy, fov = 0.0, 0.0, 0.0
            if brg is not None:                           # bearing from true north, clockwise; survey y = north
                fov = photo_fov(f35)
                tip = V.p(it["x"] + math.sin(math.radians(brg)) * EB_CONE_M,
                          it["y"] + math.cos(math.radians(brg)) * EB_CONE_M)
                ln = math.hypot(tip[0] - px, tip[1] - py) or 1.0
                dx, dy = (tip[0] - px) / ln, (tip[1] - py) / ln
                ac, R_ = math.atan2(dy, dx), EB_CONE_M * ss
                arc = [(px + R_ * math.cos(ac + fov * (t_ / 12.0 - 0.5)), py + R_ * math.sin(ac + fov * (t_ / 12.0 - 0.5)))
                       for t_ in range(13)]
                CB.line([arc[-1], (px, py), arc[0]] + arc[1:], INK, L, 50, bk_lw(0.25, k))
            B.fill([circle_pts(px, py, 0.5 * k, 10)], INK, L, 51)
            spot = None
            back = math.atan2(-dy, -dx) if brg is not None else 0.0
            for far in (1.0, 1.8, 2.6):
                for a in range(12):
                    ang = back + (a + 1) // 2 * (1 if a % 2 else -1) * math.pi / 6.0
                    dd = far * (rd + 0.8 * k)
                    if brg is not None and dd <= EB_CONE_M * ss + rd:
                        off = abs((ang - math.atan2(dy, dx) + math.pi) % (2.0 * math.pi) - math.pi)
                        if off < 0.5 * fov + math.radians(12.0):
                            continue                      # never on its own cone
                    cx_, cy_ = px + dd * math.cos(ang), py + dd * math.sin(ang)
                    b = (cx_ - rd, cy_ - rd, cx_ + rd, cy_ + rd)
                    if r[0] <= b[0] and b[2] <= r[2] and r[1] <= b[1] and b[3] <= r[3] and not _hit(b, taken):
                        spot = (cx_, cy_, b)
                        break
                if spot:
                    break
            if spot is None:
                spot = (px - (rd + 0.8 * k), py, (px - 2 * rd - 0.8 * k, py - rd, px - 0.8 * k, py + rd))
                LOG.append("Stream edge plan: photo {} has no free place for its number; drawn beside it.".format(j + 1))
            cx_, cy_, b = spot
            B.line([(px, py), (cx_, cy_)], INK, L, 59, bk_lw(0.2, k))
            B.fill([circle_pts(cx_, cy_, rd, 24)], INK, L, 60)
            B.text(str(j + 1), cx_, cy_, h9, WHITE, L, order=61, font=FONT_TITLE, bold=True, align="MC")
            taken.append(b)
        key = place_labels(B, labels, taken, L, bounds=r)
        if key:                                           # never expected (six short names); the log says so
            LOG.append("Stream edge plan: {} bridge names had no free place: {}.".format(
                len(key), ", ".join(" ".join(l_) for n_, l_ in key)))
        B.line(rect(*r) + [(r[0], r[1])], INK, L, 70, bk_lw(0.25, k))
        if i < EB_N - 1:
            B.text(u"continues below", r[2], r[1] - 1.0 * k - h7, h7, INK2, L, font=FONT_TITLE, align="R")
        if i > 0:
            B.text(u"continued from above", r[0], r[3] + 1.0 * k, h7, INK2, L, font=FONT_TITLE)
    if not with_photos:
        return draw_edge_build_e(S, B, x, top, w, U, k, ss, strips, L)
    # under the strips: scale bar and north arrow, outside the map
    rb = strips[-1][2]
    Lm = 200.0
    # v49.1 (Aras 27 Oct, Prompt 8): 1 mm in from the crop's left edge (x): the "0" is centred on the bar's end, so
    # its left half was cut off
    low = draw_scalebar_bk(B, x + 1.0 * k, rb[1] - 3.0 * k, ss, Lm, k, L)
    draw_north_at(B, F, x + 1.0 * k + Lm * ss + 12.0 * k, rb[1] - 5.0 * k, 4.0, k, L)
    low = min(low, rb[1] - 9.5 * k)
    # beside the strips: the photos, then the slim panel
    cx0 = x + mw + BK_GAP_MM * k
    cw = x + w - cx0
    sh_, wl_, em_, tot = edge_shares(S)
    vac, park, loose, opn = ground_open(S)
    panel_h = 4.2 * k + 6 * 3.5 * k + 2.5 * k + 21.0 * k  # header, six bars, gap, rings and the open-ground key
    yy = top - h75
    n_ph = len(photos)
    if n_ph:
        B.text(u"SITE PHOTOS · 1 OCT 2026 · NUMBERS AND CONES ON THE PLAN " + bcite(
            u"Photos: site visit 2026-10-01 (group photos, GPS within {:.0f} m). On the plan: the dot is where each was "
            u"taken, the cone its direction (compass, true north) and angle of view (35 mm-equivalent focal length), "
            u"both from the photo's own record (EXIF), {:.0f} m long. Captions: keywords of the photo index (a visual "
            u"reading); Roman bridges after h01 §5.".format(max(it.get("gps_err_m", 0.0) for p, it in photos),
                                                             EB_CONE_M)), cx0, yy, h75, INK, L, font=FONT_TITLE, bold=True)
        yy -= 3.0 * k
        cols, g = 2, 3.0 * k
        cell = (cw - (cols - 1) * g) / cols
        rows_ = (n_ph + cols - 1) // cols
        cap_h = 1.2 * k + h7 + 2.2 * k                    # caption under each photo and the row gap
        avail = (yy - low) - panel_h - 4.0 * k            # the column ends with the plan's scale bar row
        ph = min(cell * 0.75, (avail - rows_ * cap_h) / rows_)
        pw = ph / 0.75                                    # never stretched: 4:3 as taken
        bn = 4.2 * k
        for j, (p, it) in enumerate(photos):
            px = cx0 + (j % cols) * (cell + g)
            py = yy - (j // cols) * (ph + cap_h)
            B.image(p, px, py - ph, px + pw, py, L, order=5)
            B.fill([rect(px, py - bn, px + bn, py)], INK, L, 64)
            B.text(str(j + 1), px + 0.5 * bn, py - 0.5 * bn, h9, WHITE, L, order=65, font=FONT_TITLE, bold=True,
                   align="MC")
            B.text(eb_caption(it, pw, h7), px, py - ph - 1.2 * k - h7, h7, INK, L, font=FONT_TITLE)
        yy -= rows_ * (ph + cap_h) - 2.2 * k + 4.0 * k
    # the slim panel: edge shares as bars, walled / embanked as rings, the ground open to change
    if tot > 0:
        B.text(u"THE EDGE · % OF {:,.1f} KM OF BANK, BOTH SIDES, EVERY 4 M {}".format(tot / 1000.0, bcite(EDGE_SRC)),
               cx0, yy - h75, h75, INK, L, font=FONT_TITLE, bold=True)
        yy -= h75 + 2.3 * k
        lw_ = 40.0 * k
        bw0 = cw - lw_ - 9.0 * k
        vmax = max(sh_.values() or [1.0]) or 1.0
        for k_ in EDGE_ORDER:
            v_ = sh_.get(k_, 0.0)
            B.text(EB_EDGE_LAB[k_], cx0, yy - h7, h7, INK, L, font=FONT_TITLE)
            bx_ = cx0 + lw_
            if v_ > 0:
                B.fill([rect(bx_, yy - h7 - 0.3 * k, bx_ + bw0 * v_ / vmax, yy + 0.2 * k)], EDGE[k_][1], L, 20)
            B.text(u"{:.0f}%".format(v_), bx_ + bw0 * v_ / vmax + 1.2 * k, yy - h7, h7, INK, L, font=FONT_TITLE,
                   bold=True)
            yy -= 3.5 * k
        yy -= 2.5 * k
        rr = 5.0 * k                                      # walled and embanked: rings, the mark drawn on the map beside
        for j, (pct, lab, dash) in enumerate(((wl_, u"walled", (1.2, 0.9)), (em_, u"embanked", (0.2, 1.1)))):
            rx = cx0 + rr + j * 21.0 * k
            ry = yy - rr
            vis_ring(B, rx, ry, rr, pct, INK2, FAINT, L)
            B.text(u"{:.0f}%".format(pct), rx, ry, h8, INK, L, order=40, font=FONT_TITLE, bold=True, align="MC")
            sx, sy = rx - rr, ry - rr - 2.8 * k
            B.line([(sx, sy), (sx + 4.5 * k, sy)], INK2, L, 40, bk_lw(1.0, k))
            for d in dashes([(sx, sy), (sx + 4.5 * k, sy)], dash[0] * k, dash[1] * k):
                B.line(d, WHITE, L, 41, bk_lw(0.4, k))
            B.text(lab, sx + 5.5 * k, sy - 0.5 * h7, h7, INK, L, font=FONT_TITLE)
        B.text(u"disconnected", cx0, yy - 2.0 * rr - 6.2 * k, h7, INK2, L, font=FONT_TITLE)
        ox = cx0 + 44.0 * k                               # the ground open to change, beside the rings
        B.text(u"WHERE WE CAN BUILD " + bcite(OPEN_SRC), ox, yy - h75, h75, INK, L, font=FONT_TITLE, bold=True)
        B.text(u"{:,.1f} ha · {:.0f}% of the frame, open to change".format(opn / 1e4, 100.0 * opn / max(
            1.0, S.frame_area)), ox, yy - h75 - 1.6 * k - h7, h7, INK2, L, font=FONT_TITLE)
        oy = yy - h75 - 1.6 * k - h7 - 2.0 * k
        for lab, a, angs in ((u"Open ground", vac, (45.0,)), (u"Parking & yards", park, (45.0, 135.0)),
                             (u"Loose ground", loose, (135.0,))):
            sw_ = rect(ox, oy - 3.0 * k, ox + 6.0 * k, oy)
            B.fill([sw_], OPEN_TINT, L, 20)
            for a_ in angs:
                B.hatch([sw_], OPEN_HATCH, L, 21, 1.0 * k, math.radians(a_), bk_lw(0.1, k))
            B.line(sw_ + [sw_[0]], OPEN_HATCH, L, 22, bk_lw(0.1, k))
            B.text(u"{} · {:,.1f} ha".format(lab, a / 1e4), ox + 7.5 * k, oy - 3.0 * k + 0.5 * k, h7, INK, L,
                   font=FONT_TITLE)
            oy -= 4.4 * k
        yy = min(yy - 2.0 * rr - 7.0 * k, oy)
    low = min(low, yy)
    leg = [("box", MPL["bld"], u"Building"), ("box", MPL["her"], u"Heritage building"),
           ("box", MPL["water"], u"Stream"), ("line", MPL["water_edge"], u"Covered course, dashed"),
           ("box", MPL["tree"], u"Woods, tree cover"), ("box", MPL["park"], u"Parks, grass"),
           ("box", MPL["field"], u"Fields, orchards"), ("box", MPL["road"], u"Street"),
           ("line", MPL["ink_dark"], u"Bridge, K1-K6"), ("dot", INK, u"Photo viewpoint and view cone")]
    crop_panel("edge_build", x, low - 0.5 * k, x + w, top + 0.5 * k,
               u"Both banks, the edge every 4 m · ground open to change · photo viewpoints 1-{}".format(n_ph or 8),
               crop_scale(ss), crop_legend(leg))
    LOG.append(u"Stream edge plan 1:{:,}: ground open to change {:,.2f} ha ({:.1f}% of the frame): open ground {:,.2f}, "
               u"parking & yards {:,.2f}, loose ground {:,.2f} ha.".format(EB_DEN, opn / 1e4, 100.0 * opn / max(
                   1.0, S.frame_area), vac / 1e4, park / 1e4, loose / 1e4))
    return low - 1.0 * U


def draw_edge_build_e(S, B, x, top, w, U, k, ss, strips, L):
    """v49 (Prompt 7 task 4, the masterplan spread p.24-25): the strips draw_edge_build drew (no photos, no
    viewpoints) on a page laid out as the masterplan page beside it: exactly BK_AW x BK_AH booklet mm, the column on
    the booklet's 12-column grid from EB_COL_X (the edge shares beside the upstream strip, the walled / embanked rings
    and where we can build beside the downstream strip), the legend under the strips, scale bar and north arrow at
    the column's foot. Crop drw_edge_build_e, drawn for its width on the booklet page. Returns the y below."""
    F = S.F
    h7, h75, h8 = bk_hk(7.0, k), bk_hk(7.5, k), bk_hk(8.0, k)
    bot = top - BK_AH * k
    cx0, cw = x + EB_COL_X * k, w - EB_COL_X * k
    sh_, wl_, em_, tot = edge_shares(S)
    vac, park, loose, opn = ground_open(S)
    yy = top
    if tot > 0:                                           # beside the upstream strip: what meets the water
        B.text(u"THE EDGE " + bcite(EDGE_SRC), cx0, yy - h75, h75, INK, L, font=FONT_TITLE, bold=True)
        yy -= h75 + 1.6 * k
        B.text(u"% of {:,.1f} km of bank, both sides, every 4 m".format(tot / 1000.0), cx0, yy - h7, h7, INK2, L,
               font=FONT_TITLE)
        yy -= h7 + 3.0 * k
        lw_ = 40.0 * k
        bw0 = cw - lw_ - 9.0 * k
        vmax = max(sh_.values() or [1.0]) or 1.0
        for k_ in EDGE_ORDER:
            v_ = sh_.get(k_, 0.0)
            B.text(EB_EDGE_LAB[k_], cx0, yy - h7, h7, INK, L, font=FONT_TITLE)
            bx_ = cx0 + lw_
            if v_ > 0:
                B.fill([rect(bx_, yy - h7 - 0.3 * k, bx_ + bw0 * v_ / vmax, yy + 0.2 * k)], EDGE[k_][1], L, 20)
            B.text(u"{:.0f}%".format(v_), bx_ + bw0 * v_ / vmax + 1.2 * k, yy - h7, h7, INK, L, font=FONT_TITLE,
                   bold=True)
            yy -= 4.6 * k
        yy = min(yy - 3.0 * k, strips[-1][2][3])          # beside the downstream strip: walled, embanked, open ground
        rr = 5.0 * k
        for j, (pct, lab, dash) in enumerate(((wl_, u"walled", (1.2, 0.9)), (em_, u"embanked", (0.2, 1.1)))):
            rx = cx0 + rr + j * 21.0 * k
            ry = yy - rr
            vis_ring(B, rx, ry, rr, pct, INK2, FAINT, L)
            B.text(u"{:.0f}%".format(pct), rx, ry, h8, INK, L, order=40, font=FONT_TITLE, bold=True, align="MC")
            sx, sy = rx - rr, ry - rr - 2.8 * k
            B.line([(sx, sy), (sx + 4.5 * k, sy)], INK2, L, 40, bk_lw(1.0, k))
            for d in dashes([(sx, sy), (sx + 4.5 * k, sy)], dash[0] * k, dash[1] * k):
                B.line(d, WHITE, L, 41, bk_lw(0.4, k))
            B.text(lab, sx + 5.5 * k, sy - 0.5 * h7, h7, INK, L, font=FONT_TITLE)
        B.text(u"disconnected", cx0, yy - 2.0 * rr - 6.2 * k, h7, INK2, L, font=FONT_TITLE)
        oy = yy - 2.0 * rr - 6.2 * k - h7 - 5.0 * k
        B.text(u"WHERE WE CAN BUILD " + bcite(OPEN_SRC), cx0, oy - h75, h75, INK, L, font=FONT_TITLE, bold=True)
        B.text(u"{:,.1f} ha · {:.0f}% of the frame, open to change".format(opn / 1e4, 100.0 * opn / max(
            1.0, S.frame_area)), cx0, oy - h75 - 1.6 * k - h7, h7, INK2, L, font=FONT_TITLE)
        oy -= h75 + 1.6 * k + h7 + 2.6 * k
        for lab, a, angs in ((u"Open ground", vac, (45.0,)), (u"Parking & yards", park, (45.0, 135.0)),
                             (u"Loose ground", loose, (135.0,))):
            sw_ = rect(cx0, oy - 3.0 * k, cx0 + 6.0 * k, oy)
            B.fill([sw_], OPEN_TINT, L, 20)
            for a_ in angs:
                B.hatch([sw_], OPEN_HATCH, L, 21, 1.0 * k, math.radians(a_), bk_lw(0.1, k))
            B.line(sw_ + [sw_[0]], OPEN_HATCH, L, 22, bk_lw(0.1, k))
            B.text(u"{} · {:,.1f} ha".format(lab, a / 1e4), cx0 + 7.5 * k, oy - 3.0 * k + 0.5 * k, h7, INK, L,
                   font=FONT_TITLE)
            oy -= 4.4 * k
    rb = strips[-1][2]                                    # under the strips: the legend, columns top down
    leg = [("box", MPL["bld"], u"Building"), ("box", MPL["her"], u"Heritage building"),
           ("box", MPL["water"], u"Stream"), ("line", MPL["water_edge"], u"Covered course, dashed"),
           ("box", MPL["tree"], u"Woods, tree cover"), ("box", MPL["park"], u"Parks, grass"),
           ("box", MPL["field"], u"Fields, orchards"), ("box", MPL["road"], u"Street"),
           ("line", MPL["ink_dark"], u"Bridge, K1-K6")]
    leg += [("line", EDGE[k_][1], EB_EDGE_LAB[k_].split(u" · ")[0]) for k_ in EDGE_ORDER]
    leg += [("hatch", None, u"Ground open to change")]
    pitch = 3.3 * k
    nrow = max(1, int((rb[1] - bot - 2.0 * k) / pitch))
    ncol = (len(leg) + nrow - 1) // nrow
    colw = min(48.0 * k, (rb[2] - x) / ncol)
    for i, (kind, col, lab) in enumerate(leg):
        lx, ly = x + (i // nrow) * colw, rb[1] - 1.6 * k - (i % nrow) * pitch
        sw_ = rect(lx, ly - 2.4 * k, lx + 6.0 * k, ly)
        if kind == "box":
            B.fill([sw_], col, L, 20)
        elif kind == "line":
            B.line([(lx, ly - 1.2 * k), (lx + 6.0 * k, ly - 1.2 * k)], col, L, 20, bk_lw(1.0, k))
        else:
            B.fill([sw_], OPEN_TINT, L, 20)
            B.hatch([sw_], OPEN_HATCH, L, 21, 1.0 * k, math.radians(45.0), bk_lw(0.1, k))
        B.text(lab, lx + 7.0 * k, ly - 2.4 * k + 0.4 * k, h7, INK, L, font=FONT_TITLE)
    draw_scalebar_bk(B, cx0, bot + 9.0 * k, ss, 200.0, k, L)
    draw_north_at(B, F, cx0 + 200.0 * ss + 12.0 * k, bot + 6.0 * k, 4.0, k, L)
    crop_panel("edge_build_e", x, bot, x + w, top,
               u"Before the masterplan: both banks, the edge every 4 m · ground open to change", crop_scale(ss), [])
    CROP_PANELS[-1]["bk_w"] = BK_AW                       # drawn for the full booklet panel width
    return bot - 1.0 * U


# ------------------------------------------------------------ sections pages: one key map each
def draw_sections_key(S, B, x, y, sw, names, k_):
    """v45 (Prompt 2: "no section lines on any map; one small key map at the top right of each sections page"): the
    whole site frame at 1:50,000 on the booklet page (SK_DEN), water and buildings faint, every cut thin and this
    page's cuts in ink with their names; north arrow beside it (v49.1: no scale word; the crop's block keeps its scale
    for the booklet). Drawn under the page's cuts on the sheet,
    right-aligned; its own crop (sections_key_n) goes in the booklet page's title band. Returns the y below."""
    L = "LU_BOARD::Sections"
    F = S.F
    k = sw / BK_AW                                        # the cuts' page: board units per booklet mm
    ss = 1000.0 * k / SK_DEN
    mw, mh = F.w * ss, F.h * ss
    h7 = bk_hk(7.0, k)
    x0 = x + sw - mw
    yt = y - 0.6 * k
    V = View(F, ss, x0, yt)
    r = (x0, yt - mh, x0 + mw, yt)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 30)
    for wt in S.water:
        CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), BLUE_L, L, 31)
    mini_buildings(S, CB, V, L, lambda u: FAINT, order=32)
    on = set(names)
    taken = []
    for x0_, y0_, x1_, y1_, nm in sorted(S.sec_lines, key=lambda c_: c_[4] not in on):   # this page's names first
        a, b = V.p(x0_, y0_), V.p(x1_, y1_)
        hi = nm in on
        CB.line([a, b], INK if hi else mix(INK2, PAPER, 0.35), L, 37 if hi else 36, bk_lw(0.45 if hi else 0.2, k))
        h = h7
        tw_ = tw(nm, h, "sans")
        for (px, py) in sorted((a, b), key=lambda p_: -p_[1]):    # the upper end first, the lower if it is taken
            px = min(max(px, r[0] + 0.6 * k), r[2] - tw_ - 0.6 * k)
            py = min(max(py, r[1] + 0.6 * k + 0.5 * h), r[3] - 0.6 * k - 0.5 * h)
            bx = (px + 0.6 * k, py - 0.5 * h - 0.3 * k, px + 0.6 * k + tw_, py + 0.5 * h + 0.3 * k)
            if not _hit(bx, taken):
                taken.append(bx)
                B.text(nm, px + 0.6 * k, py - 0.5 * h, h, INK if hi else INK2, L, order=39, font=FONT_TITLE, bold=hi)
                break
    B.line(rect(*r) + [(r[0], r[1])], INK2, L, 38, bk_lw(0.15, k))
    lx = x0 - 2.5 * k                                     # beside it on the left: KEY, the north arrow
    B.text(u"KEY", lx, yt - h7, h7, INK, L, font=FONT_TITLE, bold=True, align="R")
    # v49.1 (Aras 27 Oct, Prompt 8): no scale word. On the sheet it was the sheet's own scale (about 1:30,200), which
    # the booklet rewrites only inside this crop: next to the cuts' crops it stayed, hidden, as a stray scale (the old
    # "1:1,511" kind); and 1:50,000 is not one of Aras's scales (the key's scale is his call)
    nx = lx - tw(u"KEY", h7, "sans") - 5.0 * k
    draw_north_at(B, F, nx, yt - 0.5 * mh - 0.6 * k, 4.0, k, L)
    low = r[1] - 0.6 * k
    crop_panel("sections_key_%s" % (k_ + 1 if isinstance(k_, int) else k_), nx - 4.0 * k, low, x0 + mw + 0.3 * k, y,   # v48: "s4"
               u"Key · " + u", ".join(names), crop_scale(ss))
    CROP_PANELS[-1]["bk_w"] = (x0 + mw + 0.3 * k - (nx - 4.0 * k)) / k     # its width on the booklet page, mm
    return low
