# p.16 the senses and the water: p17_items (round 5; was senses_sheet) and its sn_* helpers (split from parts/02e_r28_detail.py, parts/02f_r28_senses.py on 29 Oct 2026; moved unchanged)
# T4a (29 Oct 2026, WO-T4a-1, package E): the shared basemap (02 §1) under every strip, chosen per panel (D5) by
# P16_BASEMAP; the stream comes only from the basemap (never the corridor's own pieces); every strip is widened so its
# surroundings show and fills its cell (labels sit on the drawing); Encounters rebuilt as five lanes that meet at the
# hubs, Kermes and the flood zone; History with small photos beside its places. basemap.py and icons.py come from
# the masterplan core includes (T4b, v28).
# T4 (30 Oct 2026, booklet p15, PG1): all six maps on ONE M3 base (basemap mode "base": the stream by M5, faint
# streets, M11 buildings, the study area) with one legend logic: every key column starts level with its strip's top
# edge under a title, and every strip has its own north arrow and scale bar at the key column's foot. Encounters =
# the previous trial's flow ribbons (v27, git 8f04e72) in separate lanes, no hub / flood icons or hatched clouds;
# History photos in one ordered, numbered row; Smell shows the sourced flowering months; no photo credits on the
# sheet (they go to the Sources page).
# v32 (Aras 31 Oct, booklet p15 "the maps look so crowded, make it more transparent and less dense, somewhere between
# the previous drawing and now"; "I don't like the encounters", redraw like the references he sent): one base for
# all six, between the 29 Oct "minimal" and the 30 Oct M3 base (buildings very faint); every panel layer at P16_FADE
# of its opacity; fewer feeling veins and dots (they read as trees), fewer smell rings, birds half as dense;
# Encounters redrawn after senses_ref3: braided ribbons that meet on the stream at their places and run on to
# organic, outlined vignette bubbles (sn_encounters, sn_bubble).
# v38 (round 4, S8: P16.1-P16.4, G-R4-1/2/4/7/9/11, G-R4-5.1): bigger strips (P16_ROWS / P16_CH, title in the key
# column, no statement line); ONE muted base (map_layers ml_base) under all six strips through mp_map_draw (base ->
# D9 tint -> the panel -> study line -> marks), the P16_BASEMAP per-panel modes are gone; the D9 tint of what the
# project changes on the five project panels; five distinct Encounters hues (P16_EXP) and bigger marks; every text
# registered in the sheet's TextPage "p16" (labels placed by pg.tp.place, pg.check_text() before the PDF is written);
# History numbers by mp_marker in the heritage colour; north arrows by keymap north_items; names from the table;
# people black (figures.py), the Encounters colour carried by the bubble and the mark.
# v41 (round 6 S8, new page 15, BRIEF row 15 "G6-1 only" + G6-2..G6-10): page id p15; every colour from the round 6
# category -> hue table (common/hues.py, PLAN §2.6): zone fields by P16_ZONE_HUE, moods PUB, sounds / smells /
# encounters by their category, heritage browns (History numbers by HER_RANK, base heritage houses HER r4 / r3);
# legends sorted by category then rank; no leader ties in History (markers spread instead); labels kept P16_LAB_GAP
# clear of each other and of the feeling pictograms; watch wedges under the cross bars; element groups (G6-9,
# mpx_grp); the unused north arrow / scale bar drawers gone (the booklet draws them, north_deg on each drawing).

P16_WATER_OPTS = {"spacing": 0.6, "seed": 5}  # M5 water_plan at 1:20,000 (the stream is only a few mm wide here)
# Smell: the species whose flowering months common/plants.py holds (pla_months, sourced there); the other sources
# have no season data in the repo and get no month bar
P16_SMELL_SPECIES = {"reeds": "reed", "lavender": "lavender"}
# v38 (round 4, P16.1, U30 "we need the drawings bigger"): the statement line is gone (G-R4-2: the scale is on every
# strip's bar, "one base map" in the base key), the panel title moved to the top of its key column (the strip's top
# band holds only the bridge ruler), so the cells start right under the title band and every strip is 71 mm tall
# instead of 62 (+15 % map area). The strips stay at 1:20,000: the only standard scale (D6 a, SF_SCALES) at which
# six strips fit one A3 (the analysis frame is 142 mm wide at 1:20,000, 284 mm at 1:10,000).
P16_ROWS = (29.0, 111.5, 194.0)              # design value: cell tops, mm from the page top (title band ends at 25;
#                                              the last cell ends at 272.5, the booklet's footer starts at 276)
P16_CH = 78.5                                # design value: a cell's height, mm (3 x 78.5 + 2 x 4 gap = 243.5)
P16_STRIP_TOP = 7.5                          # design value: the strip's top below its cell's top: two ruler rows of
#                                              7 pt bridge names (row pitch P16_RULER_ROW) above the frame
P16_STRIP_H = P16_CH - P16_STRIP_TOP         # mm: every strip's height (71 mm; v37: 62)
P16_RULER_ROW = 3.6                          # design value: ruler row pitch, mm (7 pt ink 2.3 mm + the 0.6 mm text gap)
P16_TP_MARGINS = (14.0, 8.0, 14.0, 22.0)     # design value: TextPage margins (left, top, right, bottom) mm: the
#                                              kicker's top at 10 mm; the bottom 22 mm (y > 275) stay free for the
#                                              booklet's footer and page number (bottom right)
P16_LAB_R = (0.8, 2.0, 3.5)                  # design value: label distances from their point tried in turn, mm
P16_MK_STEP = 4.2                            # design value: centre distance of two History markers, mm (v41: 3.4 ->
#                                              4.2, SON page17 markers 2/3/4 touching: 3.6 mm disc + 0.6 clear)
#                                              (7 pt marker radius 1.42 + rim; glyph to the other disc >= 0.6)
P16_TINT_TERR_M = 4.0                        # design value: half-width (m) of the D9 tint band along a terrace edge
#                                              (the same band sn_zone_fields gives the terraces)
P16_TINT_PANELS = (u"Zones", u"Feeling", u"Sound", u"Smell", u"Encounters")   # panels that show the project (D9)
P16_NORTH_MM = 5.0                           # design value: north arrow height (common/keymap north_items), mm
P16_PHOTO_DIR = os.path.join(DATA_DIR, "heritage_photos")   # the run kit's photo folder (p.21's contract)
P16_PHOTO_CSV = "photos.csv"
P16_PHOTO_W, P16_PHOTO_H = 22.0, 16.5        # mm: one History photo at most (4:3, cropped to fill)
# History photos: own site photos by file name (no credit, D13) first, else a photos.csv row whose place or file
# name holds an alias. v29 (Aras 30 Oct "ok to use kermes photos"): Kermes takes the DHA photo. T4 (G12): no credit
# lines on the sheet; the csv's credit lines go to the Sources page (p23).
P16_PLACES = (
    dict(key="hamam", cap=(landmark_name("tabaklar_hamami"),),     # v38 (G-R4-11): names from the names table
         own=(u"tabaklar_hamami_1.jpg", u"tabaklar_hamami_2.jpg"), alias=(u"tabaklarhamami",)),
    dict(key="tabakhane", cap=(u"Tabakhane",), own=(u"tabakhane_1.jpg",), alias=(u"tabakhane",),
         notalias=(u"koprusu",)),
    dict(key="k3", cap=(bridge_name("K3"), u"Roman bridge"), own=(u"tabak_koprusu_1.jpg", u"tabak_koprusu_2.jpg"),
         alias=(u"tabakkoprusu",)),
    dict(key="k5", cap=(bridge_name("K5"), u"Roman bridge"), own=(), alias=(u"uckemer",)),
    dict(key="tunnels", cap=(landmark_name("kizil_avlu"), u"tunnels"), own=(), alias=(u"tunnel",)),
    dict(key="kermes", cap=(u"Kermes",), own=(), alias=(u"kermes",)))      # v29: DHA photo
P16_KEY_ROW = 4.6                            # mm: one row of every key column
P16_FADE = 0.65                              # v32: every panel layer's opacity times this (Aras 31 Oct: lighter)
P16_THIN = 0.5                               # v32: feeling veins and dots times this (they read as trees)
P16_CONE_A = 0.30                            # round 5 (P17.1, U18 "make the vision cones see through"): opacity of
#                                              the sight wedges (design value; was an opaque pale fill)
P16_BASE_FADE = 0.35                         # round 5 (P17.2, U52 "çok koyu ... hiçbir şey okunmuyor"): the muted base's
#                                              colours mixed this far toward paper on this page (design value)
P16_LAB_GAP = 0.8                            # v41 (G6-8, SON page17 crowding): a word keeps this clear of taken boxes, mm
# v41 (round 6, G6-6, PLAN §2.6): zone field -> (category, rank): darker = more important inside each category
P16_ZONE_HUE = {"reed": ("WW", 1), "wetland": ("WW", 2), "terraces": ("WW", 3), "hub": ("PUB", 1),
                "subhub": ("PUB", 2), "cafe": ("PUB", 3), "demeter": ("AGR", 2), "forest": ("GRN", 2)}
P16_CAT_ORDER = ("CTX", "HER", "WAT", "WW", "GRN", "AGR", "MOV", "PUB")   # PLAN §2.6 table order (legend sort)
P16_ZONE_KIND = {"reed": "water", "wetland": "water", "terraces": "water", "hub": "hubs", "subhub": "hubs",
                 "cafe": "hubs", "demeter": "fields", "forest": "plants"}   # G6-9 kind of each zone field
P16_WET_FIELDS = ("subhub", "wetland")       # round 5 (G-R5-8): zone fields IN the water by design (drawn above it);
#                                              every other field and the feeling blots go under the water
_P16_MEMO = {}


def r28_zone_fields(C):
    """[(zone key, rings)]: each R28_ZONES programme field over the whole frame (its own cells: core and lighter
    part, no fade), survey m, closed rings (fill even-odd), in R28_ZONES order; worked out once a press (kept on C).
    Shared helper: the senses page (MP-senses) builds its fade-out zones from the same fields."""
    got = getattr(C, "_r28_fields", None)
    if got is None:
        S = r28_zone_strength(C)
        got = [(k_, _r28_loops(C, list(S[k_][0]))) for k_, _, _ in R28_ZONES if k_ in S]
        got = [(k_, r_) for k_, r_ in got if r_]
        C._r28_fields = got
    return got


def sn_y(td):
    """mm from the page top -> page y (the sheet is drawn y up)"""
    return SN_PH - td


def sn_mm(pt):
    return pt * SN_PT


def sn_ring(cx, cy, r, seed=0, amp=0.0, n=40, lobes=(2, 3, 5)):
    """an organic closed ring round (cx, cy): radius r with a smooth wobble of about amp x r (the same seed gives
    the same wobble, so rings of one source read as contours)"""
    rnd = random.Random(seed)
    ph = [rnd.uniform(0.0, 2.0 * math.pi) for _ in lobes]
    out = []
    for i in range(n):
        a = 2.0 * math.pi * i / n
        k = 1.0 + sum(amp / (j + 1.0) * math.sin(L * a + p) for j, (L, p) in enumerate(zip(lobes, ph)))
        out.append((cx + r * k * math.cos(a), cy + r * k * math.sin(a)))
    return out


def sn_disc(c, r, n=20):
    return sn_ring(c[0], c[1], r, 0, 0.0, n)


def sn_normals(P):
    out = []
    for i in range(len(P)):
        a, b = P[max(0, i - 1)], P[min(len(P) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        out.append((-dy / L, dx / L))
    return out


def sn_band(P, w, taper=0.0):
    """the outline of a band of half-width w round polyline P (any units); taper = the share of the length over
    which each end narrows (0: square ends)"""
    Q = [tuple(P[0])] if P else []
    for p in P[1:]:
        if math.hypot(p[0] - Q[-1][0], p[1] - Q[-1][1]) > 1e-6:
            Q.append(tuple(p))
    if len(Q) < 2:
        return []
    s = arclen(Q)
    L = s[-1] or 1.0
    lt, rt = [], []
    for p, n_, t in zip(Q, sn_normals(Q), s):
        ww = w
        if taper > 0.0:
            f = min(1.0, t / (taper * L), (L - t) / (taper * L))
            ww = w * math.sqrt(max(0.0, math.sin(f * math.pi / 2.0)))
        lt.append((p[0] + n_[0] * ww, p[1] + n_[1] * ww))
        rt.append((p[0] - n_[0] * ww, p[1] - n_[1] * ww))
    return lt + rt[::-1]


def sn_along(P, step):
    """points every step along polyline P (same units)"""
    if len(P) < 2:
        return list(P)
    s = arclen(P)
    out, t = [], 0.0
    while t <= s[-1]:
        out.append(at_len(P, s, t)[0])
        t += step
    return out


def sn_spaced(pts, T, gap):
    """the points of pts at least gap page mm apart (first come first kept)"""
    out, at = [], []
    for p in pts:
        q = T(p)
        if all(math.hypot(q[0] - a[0], q[1] - a[1]) >= gap for a in at):
            out.append(p)
            at.append(q)
    return out


def sn_in(bb, box, m=0.0):
    return bb[2] >= box[0] - m and bb[0] <= box[2] + m and bb[3] >= box[1] - m and bb[1] <= box[3] + m


def sn_vcent(P):
    return (sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))


def sn_T(V, x0, y0, u0=None, v0=None):
    """survey m -> page mm of a strip whose frame's lower-left corner is (x0, y0): the corridor's View (site_alan
    turned so the water runs left to right, the north-east bank on top) at 1:20,000; (u0, v0) = the widened frame's
    lower-left corner in the View (default the View's own)"""
    c_, s_, cx, cy = V.c, V.s, V.cx, V.cy
    u0 = V.u0 if u0 is None else u0
    v0 = V.v0 if v0 is None else v0

    def T(p):
        dx, dy = p[0] - cx, p[1] - cy
        return (x0 + (dx * c_ + dy * s_ - u0) * SN_K, y0 + (-dx * s_ + dy * c_ - v0) * SN_K)
    return T


def sn_page_ang(V, d):
    """page angle (radians) of the survey direction d in the strip"""
    return math.atan2(-d[0] * V.s + d[1] * V.c, d[0] * V.c + d[1] * V.s)


def sn_on_ref(G, q):
    """the point of the stream line nearest q"""
    ref = G["ref"]
    if q is None or len(ref) < 2:
        return q
    return at_len(ref, G["sref"], chain_at(ref, q)[0])[0]


def sn_ref_piece(G, q, half):
    """the stream line half m either side of the point nearest q"""
    ref, s = G["ref"], G["sref"]
    if q is None or len(ref) < 2:
        return []
    c, _ = chain_at(ref, q)
    return sub_line(ref, s, max(0.0, c - half), min(s[-1], c + half))


def sn_seg_cross(ref, a, b):
    """where segment a-b first crosses polyline ref, else None"""
    for p, q in zip(ref, ref[1:]):
        rx, ry, sx, sy = b[0] - a[0], b[1] - a[1], q[0] - p[0], q[1] - p[1]
        d = rx * sy - ry * sx
        if abs(d) < 1e-12:
            continue
        t = ((p[0] - a[0]) * sy - (p[1] - a[1]) * sx) / d
        u = ((p[0] - a[0]) * ry - (p[1] - a[1]) * rx) / d
        if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
            return (a[0] + t * rx, a[1] + t * ry)
    return None


# ---------------------------------------------------------------- the zones (ONE set with p.24)
def sn_zone_fields(C):
    """[(R28_ZONES key, [rings, survey m])] read from the masterplan's own design, as the plans draw it: reed basins
    = the zone base's WT zones + the corridor's reed side arms; terraces = WS zones + the terrace edges on the
    contours; hub squares = the corridor's dry hub squares; sub-hubs = the bed station at each hub (its width);
    Demeter's Garden = DG zones; forest corridor = the planting rule's band (FOREST: open ground 6-32 m from the
    water, 110 m or more from a hub); widened stream / wetland = the widened reaches; café = the café places of
    the plan (GR and DG zones). Used when MP-detail's r28_zone_fields (p.24) is not there."""
    out = {}

    def add(k, rings):
        out.setdefault(k, []).extend([R for R in rings if len(R) >= 3])
    for z in C.D.zones:
        if z["code"] == "WT":
            add("reed", [z["P"]])
        elif z["code"] == "WS":
            add("terraces", [z["P"]])
        elif z["code"] == "DG":
            add("demeter", [z["P"]])
        if z["code"] in ("GR", "DG"):
            add("cafe", [sn_disc(z["q"], 12.0)])
    for a in C.arms:
        add("reed", [sn_band(a["P"], 6.0, 0.15)])
    for P in C.terr:
        add("terraces", [sn_band(P, 4.0, 0.15)])
    for h in C.hubs:
        add("hub", h.get("square") or [])
        s = h.get("sub_xy")
        if s:
            add("subhub", [sn_disc(s["c"], max(8.0, s["w"] / 2.0))])
    add("wetland", [w["ring"] for w in C.widen])
    dh = getattr(C, "dh", None)
    if dh is not None:
        d0, d1, hmin, _ = FOREST
        F, Dst = C.F, C.Dst
        add("forest", C.loops([n for n in range(C.N) if F[n] == 0 and d0 <= Dst[n] <= d1 and dh[n] >= hmin], True))
    else:
        add("forest", [sn_disc(p, 9.0, 10) for p in C.forest])
    return [(k, out[k]) for k, _, _ in R28_ZONES if out.get(k)]


def sn_fields(C, warn):
    """(fields, source): MP-detail's r28_zone_fields(C) (p.24, 02e) when it gives valid rings, else sn_zone_fields"""
    f = globals().get("r28_zone_fields")
    if callable(f):
        try:
            got = [(k, [ring(list(R)) for R in rs if len(R) >= 3]) for k, rs in f(C) if k in R28_ZONE]
            got = [(k, [R for R in rs if len(R) >= 3]) for k, rs in got]
            got = [(k, rs) for k, rs in got if rs]
            if got:
                return got, u"r28_zone_fields"
        except Exception as ex:
            warn.append(u"senses sheet: r28_zone_fields not used ({}: {}); its own reading of the zones".format(
                type(ex).__name__, ex))
    return sn_zone_fields(C), u"own reading"


def sn_data(C, areas, warn):
    """everything the six strips draw, in survey m, read once from the corridor (C) and the working areas"""
    ref = [tuple(p) for p in (C.ref or [])]
    G = {"V": C.V, "ref": ref, "sref": arclen(ref) if len(ref) >= 2 else [0.0],
         "covered": [P for P in (C.covered or []) if len(P) >= 2], "bed": list(C.bed_loops or []),
         "streams": list(C.streams or []),
         "study": [list(R) for R in (getattr(C, "study", None) or []) if len(R) >= 3] or
         [ring(list(A)) for A in (areas or {}).values()],          # v38: the Corridor's study rings (C.study) first
         "bld": [P for role in ("building", "housing", "heritage", "shed") for P in C.bld.get(role, [])],
         "hubs": list(C.hubs), "hub": dict((h["id"], h) for h in C.hubs), "zones_raw": list(C.D.zones),
         "arms": list(C.arms), "terr": list(C.terr), "widen": list(C.widen), "forest": list(C.forest),
         "canopy": list(C.canopy), "cross": list(C.cross), "terrace": C.terrace}
    if not G["study"]:
        warn.append(u"senses sheet: no calisma_alan outline: the study area is not drawn")
    G["fields"], G["fields_src"] = sn_fields(C, warn)
    G["bath"] = next((xy for nm, xy in PLACES if u"TABAKLAR" in nm), None)
    G["kermes"] = sn_seg_cross(ref, SN_S4[0], SN_S4[1]) or sn_on_ref(G, sn_vcent(list(SN_S4)))
    _p16_frame(G, C.V)
    _p16_basemap(G, warn)
    _p16_base(G, warn)                                   # v38 (P16.3): the ONE muted base of all six strips
    try:                                                 # v38 (P16.4): the D9 footprint of what we change
        G["tint"] = _p16_tint(C, G)
    except Exception as ex:
        G["tint"] = []
        warn.append(u"FLAG p16: D9 tint not drawn ({}: {})".format(type(ex).__name__, ex))
    G["traffic"] = [(rd["xy"], rd["change"]) for rd in ROADS
                    if u"Cami Kebir" in rd["name"] or u"Adnan Menderes" in rd["name"]]   # K4 and K6 (BRIEF §3)
    G["market"] = []
    try:                                                 # city link's stops: the bank bazaar, the producers' market
        for f_ in city_link()[0].get("functions", []):
            nm = (f_.get("name") or u"").lower()
            if f_.get("xy") and (u"bazaar" in nm or u"market" in nm):
                G["market"].append(tuple(f_["xy"]))
    except Exception:
        pass
    return G


# ---------------------------------------------------------------- the strip frame every panel shares
def _p16_frame(G, V):
    """T4a: the widened strip frame in the View (u0, v0, u1, v1), the same for all six strips: the analysis frame
    grown to the strip width the cell allows (SN_SIDE - 4 mm) and to P16_STRIP_H tall at 1:20,000, so the stream
    reads with its surroundings; G["bm_box"] = its survey bounding box (the basemap's cull box)"""
    sw0, sh0 = (V.u1 - V.u0) * SN_K, (V.v1 - V.v0) * SN_K
    pu = max(0.0, (SN_SIDE - 4.0 - sw0) / 2.0) / SN_K
    pv = max(0.0, (P16_STRIP_H - sh0) / 2.0) / SN_K
    fr = (V.u0 - pu, V.v0 - pv, V.u1 + pu, V.v1 + pv)
    G["fr"] = fr
    G["bm_box"] = tuple(bbox([V.xy(u, v) for u, v in ((fr[0], fr[1]), (fr[2], fr[1]), (fr[2], fr[3]),
                                                       (fr[0], fr[3]))]))


def _p16_basemap(G, warn):
    """T4a: the shared basemap's data, read once a run (common/basemap.py); None without it (the site board writes
    it): the strips are then drawn without stream, streets and buildings, and the log says so (one line)"""
    D = None
    try:
        D = basemap_load(log=[])
    except Exception as ex:
        warn.append(u"senses sheet: basemap not read ({}: {})".format(type(ex).__name__, ex))
    if not D:
        warn.append(u"senses sheet: no basemap data (Downloads/Bergama/cached/basemap/basemap.json, written by the "
                    u"site board): the strips are drawn without stream, streets and buildings")
    G["bm"] = D or None


def _p16_base(G, warn):
    """v38 (round 4, P16.3, G-R4-4): the ONE base of the sheet: map_layers ml_base (basemap mode "muted": the stream
    by M5, light streets with closed edges, light houses with one closed outline per block, every outline after every
    fill; no study line, map_draw draws it in its own layer) over the strips' common survey box, at 1:20,000, made
    once a run and drawn under all six strips (one mode, one tone inside and outside the study area). G["base"] =
    the items, G["base_kinds"] = what they hold (for the base key)."""
    its = []
    if G.get("bm"):
        try:
            its = ml_base(G["bm_box"], SN_SCALE, D=G["bm"])
        except Exception as ex:
            warn.append(u"senses sheet: muted base not drawn ({}: {})".format(type(ex).__name__, ex))
            its = []
    G["base"] = its
    G["base_kinds"] = _p16_base_kinds(its)


def _p16_base_kinds(items):
    """v38 (replaces _p16_bm_style): what the muted base items draw, for the base key, only the kinds present: water
    ("m5" or "fill"), covered (hex, width, dash), street (fill hex), bld and her ((fill hex, edge hex))"""
    out = {}
    if basemap_water_rings(items):
        out["water"] = "m5" if any(it[0] == "water" for it in items) else "fill"
    fills = set(it[2] for it in items if it[0] == "fill")
    for it in items:
        if it[0] == "line" and it[4] and list(it[4]) == list(BM_COVERED_DASH):
            out.setdefault("covered", (it[2], it[3], list(it[4])))
    if BM_MUTED["road"] in fills:
        out["street"] = BM_MUTED["road"]
    if BM_MUTED["bld"] in fills:
        out["bld"] = (BM_MUTED["bld"], BM_MUTED["bld_edge"])
    if BM_MUTED["her"] in fills:
        out["her"] = (BM_MUTED["her"], BM_MUTED["her_edge"])
    return out


def _p16_tint(C, G):
    """v38 (round 4, P16.4, D9, U52 "çok hafif izdüşüm ... transparan çok hafif bir renkle"): the light transparent
    footprint of what the project changes, as map_layers ml_tint items (ML_TINT 5C7A86 at alpha 0.16), survey m,
    clipped to the study area once here (page "p16"): the channel setbacks (the widened reaches, C.widen rings), the
    ponds and reed basins (the zone base's WT zones), the terraces (a band P16_TINT_TERR_M either side of each
    terrace edge, C.terr) and the hub squares (h["square"]). Drawn in layer proj_tint of the panels P16_TINT_PANELS."""
    R = [w_.get("ring") or [] for w_ in (C.widen or [])]
    R += [z["P"] for z in C.D.zones if z.get("code") == "WT"]
    R += [sn_band(P, P16_TINT_TERR_M) for P in (C.terr or []) if len(P) >= 2]
    for h in C.hubs:
        R += list(h.get("square") or [])
    R = [[tuple(p[:2]) for p in r_] for r_ in R if r_ and len(r_) >= 3]
    st = G.get("study") or None
    return ml_tint(R, study=st, page=u"p15") if st else ml_tint(R)


def _p16_water_swatch(pg, x, y, kind, w=9.0, h=1.8):
    """the key's stream sample as the strip draws it: M5's surface, bank line and a depth streak, else the plain fill"""
    sf, ed, dp = BM_COL["water"], BM_COL["water_edge"], None
    if kind == "m5":
        try:
            P_ = _wat_pal()
            sf, ed, dp = P_["surface"], P_["edge"], P_["deep"]
        except Exception:
            pass
    pg.poly([rect(x, y - h / 2.0, x + w, y + h / 2.0)], fill=sf, stroke=ed, lw=0.25)
    if dp:
        pg.line([(x + 1.5, y), (x + w - 1.5, y)], dp, 0.2)


def _p16_shapes(pg, shapes):
    """house shapes of common/icons.py ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) on the page.
    Round 5 (S6, S4 interfaces): ("image", x0, y0, w, h, path, alpha, flip, clip) items of the plant / figure
    modules go into the recorder as image items (the item export keeps them; never pla_images(False))."""
    for sh in shapes or ():
        if sh[0] == "image":
            pg.items.append(tuple(sh) + (None,) * (9 - len(sh)))
        elif sh[0] == "poly":
            pg.poly([sh[1]], fill=sh[2], stroke=sh[3], lw=sh[4] if len(sh) > 4 else 0.1)
        elif sh[0] == "line":
            pg.line(sh[1], sh[2], sh[3] if len(sh) > 3 else 0.1)


def sn_cell(pg, G, cx, top, title):
    """one cell: the strip frame (the widened analysis frame at 1:20,000, P16_STRIP_H tall), the panel title at the
    top of its key column (v38, P16.1: the strip's top band holds only the bridge ruler) and the bridge ruler on the
    frame's top edge. v38 (P16.3): the base, the tint and the study line are no longer drawn here: p17_items draws
    them with the panel through mp_map_draw (one draw order). Returns the cell (T, box, label bounds, the lines
    labels stay off (segs), boxes they stay off (taken), late = mark drawers for layer proj_marks)."""
    V, fr = G["V"], G["fr"]
    sw, sh = (fr[2] - fr[0]) * SN_K, (fr[3] - fr[1]) * SN_K
    x0, y1 = cx, sn_y(top + P16_STRIP_TOP)
    box = (x0, y1 - sh, x0 + sw, y1)
    T = sn_T(V, box[0], box[1], fr[0], fr[1])
    sx = cx + SN_SIDE
    pg.text(title, sx, sn_y(top + 5.0), sn_mm(SN_TS["panel"]), SN_INK, bold=True, name=u"p15 title " + title,
            role="heading")
    refp = [T(p) for p in G["ref"]]
    cell = {"x": cx, "top": top, "box": box, "T": T, "side": sx, "title": title,
            "bounds": (box[0] + 0.6, box[1] + 0.6, box[2] - 0.6, box[3] - 0.6),
            "taken": [], "segs": list(zip(refp, refp[1:])), "late": []}
    xs = {}
    for nm, xy in BRIDGES_K:                             # the ruler: a tick per bridge, its name above the frame
        x = T(xy)[0]
        if box[0] <= x <= box[2]:
            pg.line([(x, box[3]), (x, box[3] - 1.0)], SN_INK2, 0.2)
            xs[nm] = x
    # v37 (round 3, G16 / D9): the bridges by their names (common/names.py, short form; the History key and p.21 carry
    # the full names), in stream order; K1 and K2 (about 25 m apart) share one tick label; a name that would touch its
    # neighbour goes up one row (two rows above the frame, P16_STRIP_TOP). v38 (G-R4-1): the boxes are the real ink
    # boxes (fm_box) kept 0.7 mm apart (the TextPage's gap is 0.6), rows P16_RULER_ROW apart
    labs = ([(u"side crossings", (xs["K1"] + xs["K2"]) / 2.0)] if "K1" in xs and "K2" in xs else []) + \
        [(bridge_name(nm, short=True), xs[nm]) for nm in bridges_in_order() if nm in xs and nm not in ("K1", "K2")]
    fs = sn_mm(SN_TS["small"])
    ruler = []
    for s, x in labs:
        w = text_w(s, fs)
        xl = min(max(x - w / 2.0, box[0]), box[2] - w)
        for r_ in (0, 1):
            yb = box[3] + 1.0 + r_ * P16_RULER_ROW
            b = fm_box(s, xl, yb, SN_TS["small"], False, "L", 0.0, False)
            if not any(tp_hit(b, t, 0.7) for t in ruler):
                pg.text(s, xl, yb, fs, SN_INK2, name=u"p15 ruler " + title, role="ruler")
                ruler.append(b)
                break
        else:
            cell.setdefault("ruler_missing", []).append(s)
    return cell


def sn_outline(pg, G, cell):
    """the frame's own hairline (T4: the study area is drawn with the base, sn_cell)"""
    with mpx_grp(pg, "frame", cell.get("title") or u"strip"):   # v41 (G6-9)
        pg.poly([rect(*cell["box"])], stroke=SN_FRAME, lw=0.15)


def _p16_place(pg, cell, segs, s, at, pt, colour, bold=True, alts=(), name=None):
    """v38 (round 4, G-R4-1): one label on or right beside its point ON the strip, through the sheet's TextPage:
    the positions (centre, then E NE N NW W SW S SE at the distances P16_LAB_R) whose real box (fm_box) stays inside
    the strip, off the stream line and the panel's lines (segs) and off the boxes in cell["taken"] (photos, markers)
    are handed to pg.tp.place, which takes the first one free of every registered text and obstacle; then the shorter
    alts. Draws the placed item; returns it, None when no spot is free (the caller reports it)."""
    bd, taken = cell["bounds"], cell["taken"]
    for t in (s,) + tuple(alts or ()):
        ix0, iy0, ix1, iy1 = fm_ink_box(t, pt, bold)
        mid = -(iy0 + iy1) / 2.0
        pos = []
        for j, r in enumerate(P16_LAB_R):
            k = 0.7071 * r
            cand = ([(0.0, mid, "C")] if j == 0 else []) + \
                [(r, mid, "L"), (k, k - iy0, "L"), (0.0, r - iy0, "C"), (-k, k - iy0, "R"), (-r, mid, "R"),
                 (-k, -k - iy1, "R"), (0.0, -r - iy1, "C"), (k, -k - iy1, "L")]
            for dx, dy, al in cand:
                b = fm_box(t, at[0] + dx, at[1] + dy, pt, bold, al, 0.0, False)
                if not (bd[0] <= b[0] and b[2] <= bd[2] and bd[1] <= b[1] and b[3] <= bd[3]):
                    continue
                bb = (b[0] - P16_LAB_GAP, b[1] - P16_LAB_GAP, b[2] + P16_LAB_GAP, b[3] + P16_LAB_GAP)   # v41 (G6-8)
                if any(tp_hit(bb, q) for q in taken) or any(tp_seg_box(p, q, bb) for p, q in segs.near(bb)):
                    continue
                pos.append((dx, dy, al))
        if not pos:
            continue
        try:
            it = pg.tp.place(t, at, positions=tuple(pos), pt=pt, bold=bold, colour=colour, name=name, gap=0.0)
        except TextCollision:
            continue
        pg.items.append(("text", it["text"], it["x"], it["y"], it["size_mm"], colour, bold, it["align"], None))
        taken.append(it["box"])
        return it
    return None


def _p16_inner_pts(P, n=18, k=6, sep=4.0):
    """v40.4 (2 Nov run: 'Forest corridor', 'Wetland' not printed): up to k points inside ring P, the farthest from
    its edges first, at least sep apart (mm on the strip): further spots for a field's word (sn_place)"""
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    step = max(1, len(P) // 120)
    E = [(P[i], P[(i + step) % len(P)]) for i in range(0, len(P), step)]
    c = []
    for i in range(n):
        for j in range(n):
            x = min(xs) + (i + 0.5) / n * (max(xs) - min(xs))
            y = min(ys) + (j + 0.5) / n * (max(ys) - min(ys))
            if pip(x, y, P):
                c.append((min(seg_dist(x, y, a, b) for a, b in E), (x, y)))
    out = []
    for _d, q in sorted(c, key=lambda dq: -dq[0]):
        if all((q[0] - o[0]) ** 2 + (q[1] - o[1]) ** 2 >= sep * sep for o in out):
            out.append(q)
            if len(out) >= k:
                break
    return out


def sn_place(pg, cell, labs, warn):
    """v37 (round 3, G3: no leader lines): each word on or right next to its place ON the strip, never on the stream
    line or a panel's own lines (cell["segs"]) or boxes (cell["taken"]), at its size or the small size; "more" =
    further places of the same word: the word again at each, small (rank 1). v38 (round 4, G-R4-1): placed through
    the sheet's TextPage (_p16_place -> pg.tp.place), so no word touches any registered text, marker or keep; the
    old self-test (lp_overlap_flag on its own boxes) is gone: pg.check_text() tests the whole sheet. A rank-0 word
    with no free spot is FLAGged in the log (named), rank-1 repeats left out are counted in the log."""
    segs = TpSegIndex(segs=cell.get("segs", ()))
    small = SN_TS["small"]
    items = []
    for L_ in labs:
        items.append((L_.get("rank", 0), L_, L_["at"], L_.get("pt", SN_TS["label"])))
        for a in L_.get("more", ()):
            items.append((1, L_, a, small))
    n_more = 0
    for rank, L_, at, pt0 in sorted(items, key=lambda it: it[0]):
        b_ = L_.get("bold", True)
        got = None
        for pt in ([pt0, small] if pt0 > small else [small]):
            got = _p16_place(pg, cell, segs, L_["s"], at, pt, L_.get("col", SN_INK), b_, L_.get("alts", ()),
                             u"p15 {} {}".format(cell.get("title", u""), L_["s"]))
            if got:
                break
        if got is None and rank == 0:                    # v40.4 (2 Nov run): the field's other spots, small; then
            fid = set(id(q) for q in cell.get("field_segs", ()))   # the same spots allowed over a field's own edge
            segs2 = TpSegIndex(segs=[q for q in cell.get("segs", ()) if id(q) not in fid]) if fid else None
            for sg_ in (segs, segs2):
                for a2 in ([at] if sg_ is not segs else []) + list(L_.get("also", ())):
                    if sg_ is None:
                        continue
                    got = _p16_place(pg, cell, sg_, L_["s"], a2, small, L_.get("col", SN_INK), b_, L_.get("alts", ()),
                                     u"p15 {} {}".format(cell.get("title", u""), L_["s"]))
                    if got:
                        break
                if got:
                    break
        if got is None:                                  # v42 (L3): never left out: recorded on its place as an
            pg.items.append(("text", L_["s"], at[0], at[1], sn_mm(pt0 if rank == 0 else small),   # anchored label;
                             L_.get("col", SN_INK), b_, "C", None))                   # the booklet places it
            n_more += 1
    if n_more:
        MPX_LOG.append(u"info p15 {}: {} word(s) with no free spot on the strip handed to the booklet's placer".format(
            cell.get("title", u""), n_more))


def _p16_fig(pg, pose, x, y, h, facing=1):
    """p.16's ONE figure point: the figure library's side view (common/figures.py fig_side; adult 1.70 m), h mm
    tall on this diagram (pictogram size, not to scale), feet at (x, y). "sit" = sit_step (S4 alias). v38 (round 4,
    G-R4-5.1): people are black (figures.py pen_black set); the colour argument (ink=) is gone."""
    k = h / 1.70
    _p16_shapes(pg, fig_side(pose, x, y, k, facing))   # round 5 (S4): "sit" = the library's sit_step (alias)


def sn_key_row(pg, x, y, word, pt=None):
    size = sn_mm(pt or SN_TS["label"])
    pg.text(word, x, y - size * 0.35, size, SN_INK)


def sn_key_title(pg, cell, s=None):
    """T4 (G1, one legend logic for all six): the key column starts level with its own strip's top edge; returns the
    y of its first row's middle. v38 (P16.1, G-R4-2): the panel title sits above it (sn_cell), so a key title is
    drawn only where it says something the panel title does not (s), else the rows start at the top"""
    if not s:
        return cell["box"][3] - 3.0
    fs = sn_mm(SN_TS["small"])
    yb = cell["box"][3] - 2.6
    pg.text(s, cell["side"], yb, fs, SN_INK, bold=True, name=u"p15 key title", role="legend")
    return yb - 3.6


# ---------------------------------------------------------------- Zones: the base map (p24_ref2 fade-out fields)
def sn_field(pg, rings, colour, core=0.42 * P16_FADE, halo=(1.3, 0.9, 0.5), ha=0.12 * P16_FADE):
    """a fade-out field: a translucent core and, outside its edge only, steps fading outward (no outline)"""
    rings = [Q for Q in rings if len(Q) >= 3]
    m = halo[0] + 1.0
    for Q in rings:
        bb = bbox(Q)
        pg.clip([rect(bb[0] - m, bb[1] - m, bb[2] + m, bb[3] + m), Q])
        for w in halo:
            pg.line(Q + Q[:1], colour, 2.0 * w, alpha=ha)
        pg.unclip()
    for Q in rings:
        pg.poly([Q], fill=colour, alpha=core)


def sn_zones(pg, G, cell, warn):
    T, box = cell["T"], cell["box"]
    labs = []
    pg.clip([rect(*box)])
    for key, rings in G["fields"]:
        name, hx = R28_ZONE[key][0], _p16_zone_col(key)  # v41 (G6-6): the table's hue
        Ps = [Q for Q in ([T(p) for p in R] for R in rings) if len(Q) >= 3 and sn_in(bbox(Q), box)]
        if not Ps:
            continue
        tpg = pg if key in P16_WET_FIELDS else (cell.get("upg") or pg)   # round 5 (G-R5-8)
        with mpx_grp(tpg, P16_ZONE_KIND.get(key, "other"), SN_ZONE_SHORT.get(key, name)):   # v41 (G6-9)
            sn_field(tpg, Ps, hx)
        cell.setdefault("zone_keys", []).append(key)
        for Q in Ps:                                     # the words stay off the fields' edges
            Qs = Q[::max(1, len(Q) // 24)] + Q[:1]
            sg_ = list(zip(Qs, Qs[1:]))
            cell["segs"].extend(sg_)
            cell.setdefault("field_segs", []).extend(sg_)   # v40.4: sn_place's last try may cross these (not text)
        Ps_ = sorted(Ps, key=lambda Q: -abs(area2(Q)))
        at = inner_pt(Ps_[0])
        also = [q for Q in Ps_ for q in _p16_inner_pts(Q) if q != at]   # v40.4: more spots in the field(s)
        labs.append(dict(s=SN_ZONE_SHORT.get(key, name), at=at, col=mix(hx, SN_DARK, 0.5), also=also))
    pg.unclip()
    sx = cell["side"]                                    # key column: the ONE base all six strips share (T4)
    st, bs = BM_STUDY_LINE, G.get("base_kinds") or {}    # v38 (P16.3): the muted base's kinds (_p16_base_kinds)
    y = sn_key_title(pg, cell, u"Base map · all six strips")
    rows = [(R28_STUDY_NAME, "study"), (u"What we change", "tint"), (place_name("stream"), "water"),
            (u"Hidden (covered) stream", "covered"), (u"Streets", "street"), (u"Buildings", "bld"),
            (u"Heritage buildings", "her"), (u"Bridge (ticks on top)", "bridge"), (u"Flow direction", "flow")]
    for word, kind in rows:
        if kind in ("water", "covered", "street", "bld", "her") and kind not in bs:
            continue                                     # the key lists only what the base drew
        if kind == "study" and not G["study"]:
            continue
        if kind == "tint" and not G.get("tint"):
            continue
        if kind == "study":
            pg.line([(sx, y), (sx + 9.0, y)], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
        elif kind == "tint":                             # v38 (P16.4, D9): the footprint tint, as the strips draw it
            pg.poly([rect(sx, y - 1.0, sx + 9.0, y + 1.0)], fill=ML_TINT, alpha=ML_TINT_ALPHA)
            pg.poly([rect(sx, y - 1.0, sx + 9.0, y + 1.0)], stroke=SN_FRAME, lw=0.1)
        elif kind == "water":
            _p16_water_swatch(pg, sx, y, bs["water"])
        elif kind == "covered":
            pg.line([(sx, y), (sx + 9.0, y)], bs["covered"][0], bs["covered"][1], bs["covered"][2], cap=0)
        elif kind == "street":
            pg.poly([rect(sx, y - 0.7, sx + 9.0, y + 0.7)], fill=bs["street"], stroke=BM_MUTED["road_edge"],
                    lw=BM_MUTED["lw"])
        elif kind in ("bld", "her"):
            f_, e_ = bs[kind]
            pg.poly([rect(sx + 1.5, y - 1.0, sx + 7.5, y + 1.0)], fill=f_, stroke=e_, lw=BM_MUTED["lw"])
        elif kind == "bridge":
            pg.line([(sx + 4.5, y + 0.9), (sx + 4.5, y - 0.9)], SN_INK2, 0.2)
        else:                                            # the water's direction in every strip (left to right)
            pg.line([(sx, y), (sx + 7.6, y)], SN_WATER_MID, 0.35)
            pg.poly([[(sx + 9.0, y), (sx + 7.2, y + 0.8), (sx + 7.2, y - 0.8)]], fill=SN_WATER_MID)
        sn_key_row(pg, sx + 11.0, y, word)
        y -= P16_KEY_ROW
    return labs


def _p16_zone_col(key):
    """v41 (round 6, G6-6): a zone field's colour from the category -> hue table (P16_ZONE_HUE; the R28_ZONE colour
    only for a key the table does not name)"""
    c = P16_ZONE_HUE.get(key)
    return hue(c[0], c[1]) if c else R28_ZONE[key][1]


def _p16_her_col(name, default=3):
    """v41 (Q5): a heritage place's brown by its sourced status (common/hues.py HER_RANK; PLAN §2.6: Kızıl Avlu r1,
    the rest r3 = no sourced status)"""
    try:
        r_ = HER_RANK.get(name, default) if hasattr(HER_RANK, "get") else HER_RANK[name]
    except Exception:
        r_ = default
    return hue("HER", r_ if r_ in (1, 2, 3) else default)


def _p16_cat_key(cr):
    """legend sort key: (category, rank) -> table order, then darker first"""
    c, r = cr
    return (P16_CAT_ORDER.index(c) if c in P16_CAT_ORDER else len(P16_CAT_ORDER), r)


# ---------------------------------------------------------------- Feeling (senses_ref1: emotion blots)
def sn_mood_col(ang):
    st = sorted(SN_FEEL)
    st = st + [(360.0, st[0][1])]
    a = ang % 360.0
    for (a0, c0), (a1, c1) in zip(st, st[1:]):
        if a0 <= a <= a1:
            return mix(c0, c1, (a - a0) / ((a1 - a0) or 1.0))
    return st[0][1]


def sn_blot(pg, x, y, R, colour, veins, seed, dots=True):
    """a watercolour blot strongest at its centre and spreading out (stacked translucent organic discs), vein
    strokes running out from it (a mood that gathers) and a dot texture thinning outward"""
    rnd = random.Random(seed)
    for i in range(7):
        r = R * (1.0 - i * 0.12)
        pg.poly([sn_ring(x + rnd.uniform(-0.08, 0.08) * R, y + rnd.uniform(-0.08, 0.08) * R, r, seed * 31 + i,
                         0.22, 36)], fill=colour, alpha=0.08 * P16_FADE)
    dark = mix(colour, SN_DARK, 0.35)
    for j in range(int(round(veins * P16_THIN))):
        a = rnd.uniform(0.0, 2.0 * math.pi)
        L = R * rnd.uniform(0.9, 1.55)
        ph = rnd.uniform(0.0, 6.0)
        pts = [(x + math.cos(a + 0.35 * math.sin(t * 3.0 + ph) * t) * L * t,
                y + math.sin(a + 0.35 * math.sin(t * 3.0 + ph) * t) * L * t) for t in [k / 8.0 for k in range(9)]]
        for seg, w in ((pts[:4], 0.28), (pts[3:7], 0.17), (pts[6:], 0.09)):
            pg.line(seg, dark, w, alpha=0.6 * P16_FADE)
    if dots:
        for k in range(int(R * 9 * P16_THIN)):
            a, d = rnd.uniform(0.0, 2.0 * math.pi), R * 1.15 * rnd.random() ** 0.8
            pg.circle(x + math.cos(a) * d, y + math.sin(a) * d, 0.11, fill=SN_DARK, alpha=0.45 * P16_FADE)


def sn_feeling(pg, G, cell, warn):
    T, box = cell["T"], cell["box"]
    B = []                                               # (survey xy, mood, R mm, veins, figure)
    for z in G["zones_raw"]:
        if z["code"] == "WT":
            B.append((z["q"], "calm", 4.5, 0, "sit"))
    for p in sn_spaced([w["at"] for w in G["widen"]], T, 9.0):
        B.append((p, "calm", 5.5, 0, None))
    if G["covered"]:
        P = max(G["covered"], key=lambda P: arclen(P)[-1])
        B.append((at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0], "hidden", 4.0, 0, None))
    for h in G["hubs"]:
        if h["id"] == u"K6":                             # gateway on the regional road (h02 E12)
            B.append((h["xy"], "tense", 3.4, 5, None))
        elif h["role"] == "transit":
            B.append((h["xy"], "busy", 4.2, 6, "stand"))
        else:
            B.append((h["xy"], "lively", 5.0, 7, "walk"))
        if h.get("sub_xy"):
            B.append((h["sub_xy"]["c"], "play", 3.0, 3, "wade"))
    for P, ch in G["traffic"]:                           # K4: monument meets traffic (edge plan mark C3)
        if ch != "kept" and len(P) >= 2:
            B.append((at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0], "tense", 2.6, 4, None))
    labs, seen, figs = [], set(), []
    pg.clip([rect(*box)])
    for i, (p, mood, R, veins, pose) in sorted(enumerate(B), key=lambda e: -e[1][2]):
        x, y = T(p)
        if sn_in((x, y, x, y), box, 6.0):                # round 5 (G-R5-8): under the water (cell["upg"])
            bpg = cell.get("upg") or pg
            with mpx_grp(bpg, "people", u"feeling %s %d" % (mood, i)):   # v41 (G6-9): one mood place
                sn_blot(bpg, x, y, R, sn_mood_col(SN_MOOD[mood]), veins, 11 + i)
    for p, mood, R, veins, pose in B:                    # pictograms (senses_ref1's black figures), not crowded
        x, y = T(p)
        if pose and sn_in((x, y, x, y), box) and all(math.hypot(x - a, y - b) >= 2.2 for a, b in figs):
            with mpx_grp(pg, "people", u"figure %s %d" % (pose, len(figs) + 1)):   # v41 (G6-9)
                _p16_fig(pg, pose, x, y - 1.4, 2.8)
            figs.append((x, y))
            cell["taken"].append((x - 1.1, y - 1.5, x + 1.1, y + 1.5))   # v41 (G6-8): no word on a pictogram
    pg.unclip()
    for p, mood, R, veins, pose in sorted(B, key=lambda e: -e[2]):
        x, y = T(p)
        if mood not in seen and sn_in((x, y, x, y), box):
            seen.add(mood)
            labs.append(dict(s=mood, at=(x, y), col=mix(sn_mood_col(SN_MOOD[mood]), SN_DARK, 0.45)))
    sx = cell["side"]                                    # key column: the feeling wheel, gathers / thins out, people
    y0 = sn_key_title(pg, cell)                          # v38 (G-R4-2): no "Mood" title (the panel title says it)
    cx, cy, r = sx + 23.0, y0 - 12.0, 8.5
    for i in range(72):
        a0, a1 = math.radians(5.0 * i), math.radians(5.0 * (i + 1))
        pg.line([(cx + r * math.cos(a0 + (a1 - a0) * t / 3.0), cy + r * math.sin(a0 + (a1 - a0) * t / 3.0))
                 for t in range(4)], sn_mood_col(5.0 * i + 2.5), 1.5, cap=0, alpha=0.85)
    fs = sn_mm(SN_TS["small"])
    pg.text(u"active", cx, cy + r + 1.6, fs, SN_INK, align="C")
    pg.text(u"passive", cx, cy - r - 1.6 - fs * 0.75, fs, SN_INK, align="C")
    pg.text(u"positive", cx + r + 1.8, cy - fs * 0.35, fs, SN_INK)
    pg.text(u"negative", cx - r - 1.8, cy - fs * 0.35, fs, SN_INK, align="R")
    y1, y2, y3 = y0 - 29.0, y0 - 36.0, y0 - 43.0
    sn_blot(pg, sx + 4.5, y1, 2.4, sn_mood_col(SN_MOOD["lively"]), 6, 5)
    sn_key_row(pg, sx + 11.0, y1, u"Gathers")
    sn_blot(pg, sx + 4.5, y2, 2.6, sn_mood_col(SN_MOOD["calm"]), 0, 6)
    sn_key_row(pg, sx + 11.0, y2, u"Thins out")
    _p16_fig(pg, "walk", sx + 2.5, y3 - 1.4, 2.8)        # the pictograms on the strip (G1)
    _p16_fig(pg, "sit", sx + 6.5, y3 - 1.4, 2.8)
    sn_key_row(pg, sx + 11.0, y3, u"What people do")         # v38 (G-R4-2): shorter
    return labs


# ---------------------------------------------------------------- Sound (senses_ref5: a mark texture per source)
def sn_mark(pg, kind, x, y, colour, ang=0.0):
    ca, sa = math.cos(ang), math.sin(ang)

    def R(px, py):
        return (x + px * ca - py * sa, y + px * sa + py * ca)
    if kind == "water":
        pg.line([R(-0.9 + 0.225 * i, 0.16 * math.sin(i * math.pi / 2.0)) for i in range(9)], colour, 0.22)
    elif kind == "reeds":
        for i in range(4):
            dx = (i - 1.5) * 0.28
            pg.line([R(dx, 0.0), R(dx * 1.8, 1.15 + 0.15 * (i % 2))], colour, 0.18)
    elif kind == "birds":
        pg.line([R(-0.5, 0.32), R(-0.15, 0.0), R(0.0, 0.12), R(0.15, 0.0), R(0.5, 0.32)], colour, 0.2)
    elif kind == "children":
        pg.circle(x, y, 0.36, stroke=colour, lw=0.2)
    elif kind == "voices":
        for r in (0.35, 0.75, 1.15):
            pg.line([R(r * math.cos(math.radians(-50.0 + 10.0 * i)), r * math.sin(math.radians(-50.0 + 10.0 * i)))
                     for i in range(11)], colour, 0.2)
    elif kind == "traffic":
        pg.poly([[R(-0.5, -0.28), R(0.5, -0.28), R(0.5, 0.28), R(-0.5, 0.28)]], fill=colour)
    elif kind == "wind":
        pg.line([R(-2.6 + 0.65 * i, 0.35 * math.sin(i * 0.7)) for i in range(9)], colour, 0.45, alpha=0.7)


def sn_cluster(pg, kind, at, r, n, colour, rnd, spin=0.4):
    """n marks scattered within r mm of at (a source as senses_ref5 draws it)"""
    for i in range(n):
        a, d = rnd.uniform(0.0, 2.0 * math.pi), r * math.sqrt(rnd.random())
        sn_mark(pg, kind, at[0] + math.cos(a) * d, at[1] + math.sin(a) * d, colour, rnd.uniform(-spin, spin))


def sn_sound(pg, G, cell, warn):
    T, box, V = cell["T"], cell["box"], G["V"]
    col = dict((k, c) for k, _, c in SN_SOUND)
    rnd = random.Random(7)
    ref, s = G["ref"], G["sref"]
    cov = [(a, b) for P in G["covered"] for a, b in zip(P, P[1:])]
    pg.clip([rect(*box)])
    pg.group("water", u"sound running water")           # v41 (G6-9): one group per sound source
    if len(ref) >= 2:                                    # running water: the open stream (the hidden reach is silent)
        t, k = 0.0, 0
        while t <= s[-1]:
            p, d = at_len(ref, s, t)
            x, y = T(p)
            if box[0] - 1.0 <= x <= box[2] + 1.0 and not any(seg_dist(p[0], p[1], a, b) < 12.0 for a, b in cov):
                ang = sn_page_ang(V, d)
                off = 0.55 if k % 2 else -0.55
                sn_mark(pg, "water", x - math.sin(ang) * off, y + math.cos(ang) * off, col["water"], ang)
            t += 2.0 / SN_K
            k += 1
    pg.endgroup()
    pg.group("plants", u"sound reeds")
    for z in G["zones_raw"]:                             # reeds: the lined reed basins only (v28.1, D2: the side
        if z["code"] == "WT":                            # arms are open channels with rush and loosestrife, no reed)
            sn_cluster(pg, "reeds", T(z["q"]), 2.2, 7, col["reeds"], rnd, 0.25)
    pg.endgroup()
    pg.group("plants", u"sound birds")
    for p in sn_spaced(G["forest"], T, 7.0):             # birds: the forest corridor and the wetland (v32: 7 mm)
        x, y = T(p)
        sn_cluster(pg, "birds", (x, y + 0.8), 1.2, 2, col["birds"], rnd)
    for p in sn_spaced([w["at"] for w in G["widen"]], T, 6.0):
        x, y = T(p)
        sn_cluster(pg, "birds", (x, y + 1.2), 1.8, 4, col["birds"], rnd)
    kids = [h["sub_xy"]["c"] for h in G["hubs"] if h.get("sub_xy")] + \
        [h["xy"] for h in G["hubs"] if h["role"] == "walking" and h["id"] != u"K6"]
    pg.endgroup()
    pg.group("people", u"sound children")
    for p in kids:                                       # children at the edge: the sub-hubs and the hub squares
        sn_cluster(pg, "children", T(p), 1.4, 4, col["children"], rnd)
    pg.endgroup()
    pg.group("people", u"sound market and Kermes")
    for p in G["market"] + ([G["kermes"]] if G["kermes"] else []):   # market and Kermes voices
        sn_cluster(pg, "voices", T(p), 1.5, 3, col["voices"], rnd, math.pi)
    pg.endgroup()
    pg.group("roads", u"sound traffic")
    for P, ch in G["traffic"]:                           # traffic at K4 (calmed) and K6 (kept): blocks along the road
        Q = [T(p) for p in P]
        if len(Q) < 2:
            continue
        sq = arclen(Q)
        t = 0.4
        while t <= sq[-1]:
            (x, y), (ux, uy) = at_len(Q, sq, t)
            sn_mark(pg, "traffic", x, y, col["traffic"], math.atan2(uy, ux))
            t += 1.1 if ch == "kept" else 2.2
    wind = ([G["terrace"]["xy"]] if G["terrace"] else []) + [w["at"] for w in G["widen"]] + \
        [z["q"] for z in G["zones_raw"] if z["code"] == "WP"]
    pg.endgroup()
    pg.group("other", u"sound wind")
    for p in sn_spaced(wind, T, 14.0):                   # wind: the open places (viewing terrace, widened stream)
        x, y = T(p)
        ang = sn_page_ang(V, at_len(ref, s, chain_at(ref, p)[0])[1]) if len(ref) >= 2 else 0.0
        for j in range(3):
            sn_mark(pg, "wind", x + (j - 1) * 1.2, y + (j - 1) * 1.3, col["wind"], ang)
    pg.endgroup()
    pg.unclip()
    sx = cell["side"]                                    # key column: the playful key
    y = sn_key_title(pg, cell)                           # v38 (G-R4-2): the panel title says "Sound"
    for key, word, c in SN_SOUND:
        if key in ("water", "traffic", "wind"):
            for j in range(3 if key != "wind" else 1):
                sn_mark(pg, key, sx + 1.4 + j * 3.0 if key != "wind" else sx + 4.5, y, c, 0.0)
        else:
            for j in range(3):
                sn_mark(pg, key, sx + 1.4 + j * 3.0, y - (0.5 if key == "reeds" else 0.0), c, 0.0)
        sn_key_row(pg, sx + 11.0, y, word)
        y -= 5.2
    return []


# ---------------------------------------------------------------- Smell (senses_ref4: contour rings)
def _p16_bloom(key):
    """the sourced flowering months (1-12) of a smell source's species (P16_SMELL_SPECIES, common/plants.py
    pla_months), [] where the repo has none"""
    sp = P16_SMELL_SPECIES.get(key)
    f = globals().get("pla_months")
    if not sp or not callable(f):
        return []
    try:
        return sorted(set(int(m_) for m_ in f(sp).get("bloom", []) if 1 <= int(m_) <= 12))
    except Exception:
        return []


def _p16_month_bar(pg, x, y, months, colour, cw=1.5, ch=1.2):
    """12 month cells (Jan to Dec) from x, centred on y: the given months filled in colour, the others an outline"""
    for m_ in range(12):
        r_ = rect(x + m_ * cw, y - ch / 2.0, x + (m_ + 1) * cw - 0.25, y + ch / 2.0)
        if m_ + 1 in months:
            pg.poly([r_], fill=colour, alpha=0.85)
        else:
            pg.poly([r_], stroke=SN_FRAME, lw=0.1)


def sn_smell(pg, G, cell, warn):
    """the smell sources (senses_ref4: contour rings round each source at its place in the masterplan's design) and,
    T4 (PG1 p15 "sources, intensity and seasons"), the sourced flowering months of each source's species in the key.
    The repo holds no smell intensity: every source gets the same rings (no strength is implied), and the sources
    without season data get no month bar (reported, never invented)."""
    T, box = cell["T"], cell["box"]
    col = dict((k, c) for k, _, c in SN_SMELL)
    S, dg = [], []                                       # (key, survey xy)
    for z in G["zones_raw"]:
        c = z["code"]
        if c == "WT":
            S.append(("reeds", z["q"]))
        elif c == "WS":                                  # the terraces' dry band F (French lavender)
            S.append(("lavender", z["q"]))
        elif c == "DG":                                  # herbs and greens (card i01)
            S.append(("demeter", sn_vcent(z["P"])))
            dg += z["P"]
        if c in ("GR", "DG"):                            # the plan's café places
            S.append(("cafe", z["q"]))
    mids = [P[len(P) // 2] for P in G["terr"] if P]
    for p in sn_spaced(mids, T, 8.0)[:4]:
        S.append(("lavender", p))
    if dg:                                               # olives in Demeter's Garden (card i01)
        S.append(("olive", sn_vcent(dg)))
    n, r0, dr = 3, 0.9, 0.8                              # rings, first radius, step (mm): the same for every source
    pg.clip([rect(*box)])
    dots = []
    for i, (key, p) in enumerate(S):
        x, y = T(p)
        if not sn_in((x, y, x, y), box, r0 + n * dr):
            continue
        with mpx_grp(pg, "hubs" if key == "cafe" else "plants", u"smell %s %d" % (key, i + 1)):   # v41 (G6-9)
            for k in range(n):
                Q = sn_ring(x, y, r0 + k * dr, 101 + i, 0.06 + 0.03 * k, 56)
                pg.line(Q + Q[:1], col[key], 0.16, alpha=(0.9 - 0.55 * k / (n - 1.0)) * P16_FADE)
        dots.append((x, y, col[key], key, i + 1))
    for x, y, c, key, i in dots:
        with mpx_grp(pg, "hubs" if key == "cafe" else "plants", u"smell %s %d" % (key, i)):
            pg.circle(x, y, 0.6, fill=c)
    pg.unclip()
    cell["smell_keys"] = sorted(set(k for k, _ in S))   # round 5: the sources drawn (p17_items' legend)
    sx = cell["side"]                                    # key column: source, then its months in flower under it
    y = sn_key_title(pg, cell)                           # v38 (G-R4-2): the panel title says "Smell"
    fs = sn_mm(SN_TS["small"])
    shown = set(k for k, _ in S)
    for key, word, c in SN_SMELL:
        if key not in shown:
            continue                                     # only the sources the strip draws
        for r in (1.1, 1.8):
            Q = sn_ring(sx + 4.5, y, r, 3, 0.08, 36)
            pg.line(Q + Q[:1], c, 0.16, alpha=0.8)
        pg.circle(sx + 4.5, y, 0.6, fill=c)
        sn_key_row(pg, sx + 11.0, y, word)
        months = _p16_bloom(key)
        if months:
            y -= 3.0
            _p16_month_bar(pg, sx + 11.0, y, months, c)
        y -= 5.2
    if any(_p16_bloom(k) for k in shown):                # what the month bar says (G1)
        _p16_month_bar(pg, sx + 11.0, y, [], SN_INK2)    # 12 cells, Jan to Dec
        pg.text(u"Jan to Dec", sx + 11.0 + 12 * 1.5 + 1.5, y - fs * 0.35, fs, SN_INK)
        y -= 3.4
        pg.poly([rect(sx + 11.0, y - 0.6, sx + 12.25, y + 0.6)], fill=SN_INK2, alpha=0.85)
        pg.text(u"filled: month in flower", sx + 13.5, y - fs * 0.35, fs, SN_INK)
    return []


# ---------------------------------------------------------------- Encounters (senses_ref3: flow ribbons)
def sn_spine_y(refp, x0, x1, step=0.5):
    """the stream line's y (page mm) every step mm from x0 to x1, smoothed: the ribbons' path"""
    n = int((x1 - x0) / step) + 1
    xs = [x0 + i * step for i in range(n)]
    bk = {}
    for p in (densify(refp, 0.3) if len(refp) >= 2 else []):
        if x0 - 3.0 <= p[0] <= x1 + 3.0:
            bk.setdefault(int(math.floor((p[0] - x0) / step)), []).append(p[1])
    ys = []
    for i in range(n):
        got = [y for k in range(i - 3, i + 4) for y in bk.get(k, ())]
        ys.append(sum(got) / len(got) if got else None)
    known = [y for y in ys if y is not None]
    if not known:
        return xs, None
    last = known[0]
    for i in range(n):                                   # gaps take the nearest known value
        if ys[i] is None:
            ys[i] = last
        last = ys[i]
    return xs, [sum(ys[max(0, i - 6):i + 7]) / len(ys[max(0, i - 6):i + 7]) for i in range(n)]


def sn_bez(a, b, c, d, t):
    m = 1.0 - t
    return (m ** 3 * a[0] + 3 * m * m * t * b[0] + 3 * m * t * t * c[0] + t ** 3 * d[0],
            m ** 3 * a[1] + 3 * m * m * t * b[1] + 3 * m * t * t * c[1] + t ** 3 * d[1])


def sn_wave(pg, x0, x1, y, colour, lw=0.3):
    pg.line([(x0 + (x1 - x0) * i / 16.0, y + 0.25 * math.sin(i * math.pi / 2.0)) for i in range(17)], colour, lw)


def sn_blob_ring(x, y, w, h, seed, n=48):
    """v32: an organic outline w x h mm, its left end at x, centred on y (senses_ref3's vignette bubbles)"""
    ph = 1.7 * seed
    a, b, cx = w / 2.0, h / 2.0, x + w / 2.0
    return [(cx + a * math.cos(t) * (1.0 + 0.03 * math.sin(3.0 * t + ph)),
             y + b * math.sin(t) * (1.0 + 0.07 * math.sin(2.0 * t + ph))) for t in
            (2.0 * math.pi * i / n for i in range(n))]


def sn_bubble(pg, x, y, key, word, colour, pose, seed=0):
    """a vignette at a ribbon's end (v32, senses_ref3): an organic bubble outlined in the ribbon's colour on a pale
    tint of it, a small scene with a figure of common/figures.py, and the word in capitals"""
    w, h = 34.0, 7.6
    pg.poly([sn_blob_ring(x, y, w, h, seed)], fill=mix(colour, "FFFFFF", 0.86), stroke=colour, lw=0.45)
    fx, fy = x + 6.5, y - h / 2.0 + 1.1
    if key == "remember":                                # under a Roman arch
        pg.line([(fx + 3.0 + 2.3 * math.cos(math.radians(a)), fy + 2.3 * math.sin(math.radians(a)))
                 for a in range(0, 181, 15)], colour, 0.45, alpha=0.55)
    if key in ("touch", "cross"):
        sn_wave(pg, fx - 3.5, fx + 4.5, fy + (0.8 if key == "cross" else 0.0), SN_WATER_MID)
    else:
        pg.line([(fx - 3.5, fy), (fx + 6.0, fy)], SN_INK2, 0.2)
    _p16_fig(pg, pose, fx, fy, 5.2)                      # v38 (G-R4-5.1): black; the colour is the bubble's and mark's
    if key == "watch":                                   # the line of sight
        pg.line([(fx + 0.5, fy + 4.6), (fx + 5.0, fy + 3.9)], colour, 0.2, [0.6, 0.4], cap=0)
    size = sn_mm(SN_TS["label"])
    pg.text(word.upper(), x + 14.0, y - size * 0.35, size, mix(colour, SN_DARK, 0.3), bold=True)


def sn_exp_places(G):
    """v37 (round 3, P15.1 / G19: each encounter only where the project makes it happen), survey m:
    cross    the real crossings: the six bridges (BRIDGES_K) and the masterplan's new footbridges and stepping stones
    watch    the viewing terrace (with its sightline) and the open edges of the widened reaches (wetlands)
    touch    the sub-hubs in the bed (dry months) and the step to the water facing Tabaklar Hamamı
    walk     the riverside walk as the masterplan runs it (its lines, both banks where it has them)
    remember the heritage places only: the Roman bridges Tabak, Ulucami Önü, Üç Kemer, Tabaklar Hamamı, Tabakhane,
             the Roman bank wall and the Kızıl Avlu tunnels"""
    hub = G["hub"]
    bk = dict(BRIDGES_K)
    edges = []
    ref = G["ref"]
    for w_ in G.get("widen") or []:                      # the land edge of each widened reach: its point farthest
        R_ = w_.get("ring") or []                        # from the stream line
        if len(R_) >= 3 and len(ref) >= 2:
            q = max(R_, key=lambda p: min(seg_dist(p[0], p[1], a, b) for a, b in zip(ref, ref[1:])))
            edges.append(q)
    pl = {"cross": [bk[k_] for k_ in bridges_in_order() if k_ in bk] + [c_["xy"] for c_ in G["cross"]
                                                                       if c_.get("P") and c_.get("xy")],
          "watch": ([G["terrace"]["xy"]] if G["terrace"] else []) + edges,
          "touch": [h["sub_xy"]["c"] for h in G["hubs"] if h.get("sub_xy")] + ([G["bath"]] if G["bath"] else []),
          "remember": [bk.get(k_) for k_ in ("K4", "K3", "K5")] + [G["bath"], CRAFT_XY, ROMAN_WALL] +
          ([hub[u"Kızıl Avlu"]["xy"]] if u"Kızıl Avlu" in hub else [])}
    return dict((k_, [p for p in v if p]) for k_, v in pl.items())


def _sn_tangent(refp, q):
    """the unit tangent of the page polyline refp at its point nearest q, and that point"""
    best = None
    for a, b in zip(refp, refp[1:]):
        d = seg_dist(q[0], q[1], a, b)
        if best is None or d < best[0]:
            best = (d, a, b)
    if best is None:
        return (1.0, 0.0), q
    _d, a, b = best
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    t = max(0.0, min(L, (q[0] - a[0]) * ux + (q[1] - a[1]) * uy))
    return (ux, uy), (a[0] + ux * t, a[1] + uy * t)


def sn_enc_mark(pg, key, x, y, colour, ux=1.0, uy=0.0, dirx=None):
    """v37 (P15.1, R02 idea: each mode its own mark where it happens) one encounter mark at page (x, y):
    cross = a bar across the water (perpendicular to the stream tangent ux, uy) with end ticks; watch = a sight wedge
    toward dirx (unit vector); touch = a disc with a wave; walk = (drawn as the walk's own line, here a key sample);
    remember = a small Roman arch on a white disc. v38 (round 4, P16.2): the same marks, larger (SN_ENC_* sizes)"""
    white = COL["white"]
    if key == "cross":
        nx_, ny_ = -uy, ux
        h = SN_ENC_CROSS_MM / 2.0
        a, b = (x - nx_ * h, y - ny_ * h), (x + nx_ * h, y + ny_ * h)
        pg.line([a, b], white, SN_ENC_CROSS_LW + 0.6, cap=0)
        pg.line([a, b], colour, SN_ENC_CROSS_LW, cap=0)
        for e in (a, b):
            pg.line([(e[0] - ux * 0.8, e[1] - uy * 0.8), (e[0] + ux * 0.8, e[1] + uy * 0.8)], colour, 0.4)
    elif key == "watch":
        dx, dy = dirx or (0.0, -1.0)
        L, s = SN_ENC_WATCH_MM, 0.45
        tip1 = (x + (dx * math.cos(s) - dy * math.sin(s)) * L, y + (dx * math.sin(s) + dy * math.cos(s)) * L)
        tip2 = (x + (dx * math.cos(-s) - dy * math.sin(-s)) * L, y + (dx * math.sin(-s) + dy * math.cos(-s)) * L)
        pg.poly([[(x, y), tip1, tip2]], fill=colour, stroke=colour, lw=0.25, alpha=P16_CONE_A)   # P17.1 see-through
        pg.circle(x, y, SN_ENC_WATCH_DOT, fill=colour, stroke=white, lw=0.25)
    elif key == "touch":
        r, f = SN_ENC_TOUCH_R, SN_ENC_TOUCH_R / 1.05
        pg.circle(x, y, r, fill=colour, stroke=white, lw=0.3)
        pg.line([(x - 0.6 * f + 1.2 * f * i / 8.0, y + 0.18 * f * math.sin(i * math.pi / 2.0)) for i in range(9)],
                white, 0.25)
    elif key == "walk":
        pg.line([(x - 2.5, y), (x + 2.5, y)], colour, SN_ENC_WALK_LW)
    else:                                                # remember: an arch
        r, f = SN_ENC_REM_R, SN_ENC_REM_R / 1.25
        pg.circle(x, y, r, fill=white, stroke=colour, lw=0.35)
        pg.line([(x + 0.8 * f * math.cos(math.radians(a)), y - 0.45 * f + 0.9 * f * math.sin(math.radians(a)))
                 for a in range(0, 181, 20)], colour, 0.4)
        pg.line([(x - 0.95 * f, y - 0.45 * f), (x + 0.95 * f, y - 0.45 * f)], colour, 0.35)


# v38 (round 4, P16.2, U52 "dokunmak ve yürümek gibi hisler arka planda kalmış renkler birbirine çok yakın", S21):
# legible marks at 1:20,000 (v37 sizes in brackets), mm
SN_ENC_CROSS_MM = 5.5        # design value: a cross bar's length across the water (5.0; the stream is 1-4 mm wide)
SN_ENC_CROSS_LW = 0.8        # design value: the cross bar's width (0.7), on a white casing 0.6 wider
SN_ENC_WALK_LW = 1.0         # design value: the walk's line (0.7), on a white casing 0.5 wider
SN_ENC_WATCH_MM = 5.0        # design value: the sight wedge's length (4.2)
SN_ENC_WATCH_DOT = 0.9       # design value: the watch point's radius (0.75)
SN_ENC_TOUCH_R = 1.6         # design value: the touch disc's radius (1.05)
SN_ENC_REM_R = 1.6           # design value: the remember disc's radius (1.25)
SN_ENC_REM_OFF = 2.9         # design value: a remember mark at a bridge sits this far beside its cross mark, along
#                              the stream (2.4): disc 1.6 + cross tick 0.8 + 0.5 clear
# v41 (round 6, G6-6, PLAN §2.6; replaces v38's five free hues): each encounter in its category's hue: WALK and
# CROSS are movement (MOV r1 the walk line, r2 the cross bar: told apart by their marks), TOUCH is the water (WAT r1),
# WATCH is public life (PUB r2), REMEMBER is heritage (HER r3: the places have no sourced status, Q5). All marks keep
# their white casing / rim, so the water never carries them alone.
P16_EXP = (("remember", u"Remember", hue("HER", 3), "stand"), ("touch", u"Touch", hue("WAT", 1), "touch"),
           ("walk", u"Walk", hue("MOV", 1), "walk"), ("cross", u"Cross", hue("MOV", 2), "wade"),
           ("watch", u"Watch", hue("PUB", 2), "watch"))      # legend order = the table's category order, then rank
P16_EXP_KIND = {"watch": "people", "walk": "paths", "touch": "water", "cross": "paths", "remember": "heritage"}


def sn_encounters(pg, G, cell, warn):
    """v37 (round 3, P15.1, Aras: "it says cross but it is parallel to river", "it says watch however it has
    buildings in front"; G19): no bands along the stream. Each way of meeting the water is drawn ONLY where the
    masterplan makes it happen (sn_exp_places), in its colour with its own mark (R02 idea): WALK as the riverside
    walk's own line on the banks it runs on (R01: on the real path, from place to place), CROSS as a bar across the
    water at each real crossing, WATCH as a sight wedge from the viewing terrace (along its sightline) and from the
    open edge of each widened reach toward the water, TOUCH as a disc at the sub-hubs in the bed and the step facing
    Tabaklar Hamamı, REMEMBER as an arch at the heritage places only (R03: attached to the exact stretch, both banks).
    Layer order: walk lines, then cross, watch, touch, remember. The key column keeps the five vignette bubbles, each
    with its mark sample. A design reading of the masterplan, no numbers.
    v38 (round 4, P16.2): the five hues of P16_EXP and larger marks (SN_ENC_*); the walk lines are this panel's
    proj_lines, the cross / watch / touch / remember marks are drawn in layer proj_marks (cell["late"], above the
    study line); places and counts are worked out here, unchanged (K2)."""
    T, box = cell["T"], cell["box"]
    x0, y0, x1, y1 = box
    refp = [T(p) for p in G["ref"]]
    pl = sn_exp_places(G)
    col = dict((k_, c_) for k_, _w, c_, _p in P16_EXP)
    inb = lambda q: x0 + 1.0 <= q[0] <= x1 - 1.0 and y0 + 1.0 <= q[1] <= y1 - 1.0
    n = {}
    pg.clip([rect(*box)])
    for P in G["canopy"]:                                # walk: the masterplan's walk lines
        Q = [T(p) for p in P]
        if len(Q) >= 2 and any(inb(q) for q in Q):
            with mpx_grp(pg, "paths", u"walk %d" % (n.get("walk", 0) + 1)):   # v41 (G6-9)
                pg.line(Q, COL["white"], SN_ENC_WALK_LW + 0.5)
                pg.line(Q, col["walk"], SN_ENC_WALK_LW)
            n["walk"] = n.get("walk", 0) + 1
    pg.unclip()
    marks = []                                           # (key, x, y, ux, uy, dirx), drawn in layer proj_marks
    cross_at = []
    for p in pl["cross"]:
        q = T(p)
        if not inb(q):
            continue
        (ux, uy), _m = _sn_tangent(refp, q)
        marks.append(("cross", q[0], q[1], ux, uy, None))
        cross_at.append((q, ux, uy))
        n["cross"] = n.get("cross", 0) + 1
    for i, p in enumerate(pl["watch"]):
        q = T(p)
        if not inb(q):
            continue
        if i == 0 and G["terrace"]:                      # the terrace: along its sightline (data: C.terrace["dir"])
            d0 = G["terrace"]["dir"]
            q2 = T((p[0] + d0[0] * 50.0, p[1] + d0[1] * 50.0))
        else:                                            # an open edge: toward the water
            q2 = _sn_tangent(refp, q)[1]
        L = math.hypot(q2[0] - q[0], q2[1] - q[1]) or 1.0
        marks.append(("watch", q[0], q[1], 1.0, 0.0, ((q2[0] - q[0]) / L, (q2[1] - q[1]) / L)))
        n["watch"] = n.get("watch", 0) + 1
    for p in pl["touch"]:
        q = T(p)
        if inb(q):
            marks.append(("touch", q[0], q[1], 1.0, 0.0, None))
            n["touch"] = n.get("touch", 0) + 1
    for p in pl["remember"]:
        q = T(p)
        if not inb(q):
            continue
        near = [c_ for c_ in cross_at if math.hypot(c_[0][0] - q[0], c_[0][1] - q[1]) < 1.5]
        if near:                                         # a Roman bridge: the arch beside its cross bar
            (cq, ux, uy) = near[0]
            q = (cq[0] + ux * SN_ENC_REM_OFF, cq[1] + uy * SN_ENC_REM_OFF)
        marks.append(("remember", q[0], q[1], 1.0, 0.0, None))
        n["remember"] = n.get("remember", 0) + 1

    def late():                                          # v41 (G6-8, SON page17 "WATCH cones over CROSS bars"): the
        order_ = ("watch", "cross", "touch", "remember")   # see-through watch wedges first, the cross bars over them
        for j_, (k_, x_, y_, ux_, uy_, d_) in enumerate(sorted(marks, key=lambda m_: order_.index(m_[0]))):
            with mpx_grp(pg, P16_EXP_KIND.get(k_, "other"), u"%s %d" % (k_, j_ + 1)):   # v41 (G6-9)
                sn_enc_mark(pg, k_, x_, y_, col[k_], ux_, uy_, dirx=d_)
    cell["late"].append(late)
    for k_, _w, _c, _p in P16_EXP:
        if not n.get(k_):
            warn.append(u"senses sheet: Encounters: no {} place inside the strip".format(k_))
    sx, ytop = cell["side"], box[3]
    pitch = 10.0                                         # mm: the vignettes' pitch (v38: 8.8; the key column is
    for i, (key, word, colour, pose) in enumerate(P16_EXP):   # 71 mm tall now and has no title)
        bx, by = sx + 11.0, ytop - 5.0 - pitch * i
        sn_enc_mark(pg, key, sx + 4.5, by, colour, 1.0, 0.0, dirx=(1.0, 0.0))
        sn_bubble(pg, bx, by, key, word, colour, pose, i)
    return []


def _p16_mid(P):
    """round 5 (S6): the middle of a page polyline (where the round 4 layered band put its label)"""
    s_ = arclen(P)
    return at_len(P, s_, s_[-1] / 2.0)[0]


def _p16_norm(s):
    """lower case, Turkish (and other) accents folded, letters and digits only ('Kızıl Avlu' -> 'kizilavlu')"""
    import unicodedata
    t = unicodedata.normalize("NFKD", (s or u"").replace(u"ı", u"i").replace(u"İ", u"I")).lower()
    return u"".join(c for c in t if c.isalnum() and not unicodedata.combining(c))


def _p16_jpeg(path):
    """(width px, height px, components, bytes) of a JPEG file read from its header, once a run; None if it is not
    a JPEG with 1 or 3 components (a PDF DCTDecode image)"""
    m = _P16_MEMO.setdefault("jpg", {})
    if path in m:
        return m[path]
    got = None
    try:
        with open(path, "rb") as fh:
            b = fh.read()
        i = 2 if b[:2] == b"\xff\xd8" else len(b)
        while i + 9 < len(b):
            if b[i] != 0xFF:
                break
            mk = b[i + 1]
            if mk == 0xFF:
                i += 1
                continue
            if mk == 0x01 or 0xD0 <= mk <= 0xD8:
                i += 2
                continue
            L = (b[i + 2] << 8) | b[i + 3]
            if mk in (0xC0, 0xC1, 0xC2):
                h, w, nc = (b[i + 5] << 8) | b[i + 6], (b[i + 7] << 8) | b[i + 8], b[i + 9]
                if w and h and nc in (1, 3):
                    got = (w, h, nc, b)
                break
            i += 2 + L
    except Exception:
        got = None
    m[path] = got
    return got


def _p16_photos(warn):
    """{P16_PLACES key: (path, credit line or None)} once a run, from P16_PHOTO_DIR (p.21's run-kit contract): own
    photos by file name (no credit, D13), else the first unused photos.csv row whose place or file name holds an
    alias (its credit line). v29: Kermes rows are used for Kermes. A missing folder: {} and one log line."""
    if "photos" in _P16_MEMO:
        return _P16_MEMO["photos"]
    d, out = P16_PHOTO_DIR, {}
    if not os.path.isdir(d):
        warn.append(u"senses sheet: no photo folder {}: History is drawn without photos".format(d))
        _P16_MEMO["photos"] = out
        return out

    def find(f):
        for p in (os.path.join(d, f), os.path.join(d, "own", os.path.basename(f)),
                  os.path.join(d, "photos", os.path.basename(f))):
            if os.path.isfile(p) and _p16_jpeg(p):
                return p
        return None
    own = set(_p16_norm(os.path.basename(f)) for pl in P16_PLACES for f in pl["own"])
    rows, cp = [], os.path.join(d, P16_PHOTO_CSV)
    if os.path.isfile(cp):
        try:
            import csv as _csv
            with open(cp, encoding="utf-8-sig", newline="") as fh:
                for r_ in _csv.DictReader(fh):
                    rows.append(dict((_p16_norm(k_), (v_ or u"").strip()) for k_, v_ in r_.items() if k_))
        except Exception as ex:
            warn.append(u"senses sheet: {} not read ({}): own photos only".format(cp, ex))
    used = set()
    for pl in P16_PLACES:
        got = None
        for f in pl["own"]:
            p = find(f)
            if p:
                got = (p, None)
                break
        for r_ in ([] if got else rows):
            fn = r_.get("file", u"")
            tx = _p16_norm(r_.get("place", u"")) + u"|" + _p16_norm(os.path.splitext(os.path.basename(fn))[0])
            if not fn or fn in used or not any(a in tx for a in pl["alias"]) or \
                    any(a in tx for a in pl.get("notalias", ())):
                continue
            p = find(fn)
            if p is None:
                continue
            used.add(fn)
            cr = r_.get("creditline") or r_.get("credit") or u""
            got = (p, None if _p16_norm(os.path.basename(fn)) in own or not cr else cr)
            break
        if got:
            out[pl["key"]] = got
    miss = [pl["cap"][0] for pl in P16_PLACES if pl["key"] not in out]
    if miss:
        warn.append(u"senses sheet: no photo for {} (named on the strip instead)".format(u", ".join(miss)))
    _P16_MEMO["photos"] = out
    return out


def sn_num(pg, x, y, n_, colour):
    """a numbered marker (G3: its number explained by the photo caption of the same number). v38 (round 4, G-R4-7):
    the ONE marker (mp_marker: glyph centred on its ink box, radius from the glyph, kept in the TextPage), in the
    colour of the element it names (the heritage fields, SN_HER); returns its box"""
    return mp_marker(pg, x, y, u"{}".format(n_), colour, size_pt=SN_TS["small"])[0]


def sn_history(pg, G, cell, warn):
    """the stream's heritage places, numbered on the map; their photos (P16_PLACES) are exported as photo items with
    the same number in the caption (round 5 S6, G-R5-12: the booklet places the photos; the round 4 photo row inside
    the strip is gone). Round 5 (G-R5-8): the layered heritage fields (sn_layers_round / sn_layers_band: graphic
    fields with no zone extent, lying on the stream) are gone; each place is its number marker (with a photo) or its
    word (without). Own photos and csv photos alike carry no credit on the page (G12: Sources page).
    G["photos_out"] = [(n, path, caption lines, credit or None)] for p17_items."""
    T, box = cell["T"], cell["box"]
    txt = hue("HER", 2)                                  # v41 (G6-6, P-5): heritage words in the brown ramp, no red
    labs, anchors = [], {}

    def field(q, half):
        """the place's point: the middle of the stream piece round q (half m either side), else q"""
        P = [T(p) for p in sn_ref_piece(G, q, half)] if half else []
        if len(P) >= 2 and arclen(P)[-1] > 0.5:
            return _p16_mid(P)
        return T(q)
    ka = G["hub"].get(u"Kızıl Avlu")                     # the Kızıl Avlu tunnels: the covered reach under it (H2)
    if ka:
        best = None
        for P in G["covered"]:
            c, d = chain_at(P, ka["xy"])
            if d <= 150.0 and (best is None or d < best[0]):
                best = (d, P, c)
        at = T(ka["xy"])
        if best:
            d, P, c = best
            Q = [T(p) for p in sub_line(P, arclen(P), max(0.0, c - 90.0), min(arclen(P)[-1], c + 90.0))]
            if len(Q) >= 2 and arclen(Q)[-1] > 0.5:
                at = _p16_mid(Q)
        anchors["tunnels"] = at
    bk = dict(BRIDGES_K)
    for k in ("K3", "K5"):                               # the Roman bridges (h01 §5 P08, P09; K4 "Roman?", P06)
        if bk.get(k):
            anchors[k.lower()] = T(bk[k])
    if G["bath"]:                                        # Tabaklar Hamamı (H4)
        anchors["hamam"] = T(G["bath"])
    anchors["tabakhane"] = field(CRAFT_XY, 70.0)         # Tabakhane (H3)
    if G["kermes"]:                                      # Kermes in the dry bed (h01 §2.8), at the S4 cut (v29: photo)
        anchors["kermes"] = field(G["kermes"], 90.0)
    anchors = dict((k, a) for k, a in anchors.items() if sn_in((a[0], a[1], a[0], a[1]), box))
    ph = _p16_photos(warn)
    with_ph = [(k, anchors[k]) for k in (pl["key"] for pl in P16_PLACES) if k in anchors and k in ph]
    try:                                                 # T4 (M12): the shown photos' credit lines for the Sources page
        d_ = bg_booklet(os.path.basename(os.path.normpath(OUT_FOLDER)))
        os.makedirs(d_, exist_ok=True)
        with open(os.path.join(d_, "photo_credits.json"), "w", encoding="utf-8") as f_:
            json.dump({"photo_credits": [ph[k][1] for k, _a in with_ph if ph[k][1]]}, f_, ensure_ascii=False)
    except Exception as ex:
        warn.append(u"senses photo credits not written for the Sources page ({})".format(type(ex).__name__))
    names = dict((pl["key"], pl["cap"]) for pl in P16_PLACES)
    rb = [anchors[k] for k in ("k3", "k5") if k in anchors and k not in ph]
    if rb:                                               # places without a photo keep their word on the strip
        labs.append(dict(s=u"Roman bridges", at=rb[0], more=rb[1:], col=txt))
    for k, s in (("hamam", landmark_name("tabaklar_hamami")), ("tabakhane", u"Tabakhane"),   # v38 (G-R4-11)
                 ("tunnels", u"{} tunnels".format(landmark_name("kizil_avlu"))),
                 ("kermes", u"Kermes")):                 # v29: Kermes keeps its word when it has no photo
        if k in anchors and k not in ph:
            labs.append(dict(s=s, at=anchors[k], col=txt))
    order = sorted(with_ph, key=lambda e: e[1][0])       # numbered left to right along the strip
    G["photos_out"] = [(n_, ph[k][0], list(names[k]), ph[k][1]) for n_, (k, a) in enumerate(order, 1)]
    rm = 1.8                                             # a marker's half size with its rim, mm (7 pt, <= 1.68)
    her_nm = {"k3": (bridge_name("K3"), 3), "k5": (bridge_name("K5"), 3),
              "hamam": (landmark_name("tabaklar_hamami"), 3), "tabakhane": (u"Tabakhane", 3),
              "tunnels": (landmark_name("kizil_avlu"), 1), "kermes": (u"Kermes", 3)}   # v41 (Q5, PLAN §2.6)
    marks = []
    st_ = P16_MK_STEP
    for n_, (k, a) in enumerate(order, 1):
        # v41 (G6-4: no leader lines; G6-8: SON page17 numbers 2/3/4 touching): the marker on its place, else the
        # nearest free spot round it (right, left, up, down, then the diagonals, 1 and 2 steps), no tie line
        cands = [(0.0, 0.0)] + [(dx * m, dy * m) for m in (1.0, 2.0) for dx, dy in
                                ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1))]
        m_ = None
        for dx, dy in cands:
            q = (a[0] + dx * st_, a[1] + dy * st_)
            if not (box[0] + rm + 0.6 <= q[0] <= box[2] - rm - 0.6 and box[1] + rm + 0.6 <= q[1] <= box[3] - rm - 0.6):
                continue
            if not any(math.hypot(q[0] - o[1], q[1] - o[2]) < st_ for o in marks):
                m_ = q
                break
        if m_ is None:
            m_ = (a[0], a[1])
            warn.append(u"WARNING p15 History: marker {} has no free spot round its place (drawn on it)".format(n_))
        nm_, r0_ = her_nm.get(k, (k, 3))
        marks.append((n_, m_[0], m_[1], _p16_her_col(nm_, r0_)))
        cell["taken"].append((m_[0] - rm, m_[1] - rm, m_[0] + rm, m_[1] + rm))

    def late():
        for n_, x_, y_, c_ in marks:
            with mpx_grp(pg, "heritage", u"place %d" % n_):   # v41 (G6-9)
                sn_num(pg, x_, y_, n_, c_)
    cell["late"].append(late)
    return labs


# ---------------------------------------------------------------- round 5: the page as items (S6, G-R5-12)
P16_CELLS = ((u"Zones", "zones"), (u"Feeling", "feeling"), (u"Sound", "sound"), (u"Smell", "smell"),
             (u"Encounters", "encounters"), (u"History", "history"))
_P16_MONTHS = (u"Jan", u"Feb", u"Mar", u"Apr", u"May", u"Jun", u"Jul", u"Aug", u"Sep", u"Oct", u"Nov", u"Dec")


def _p16_map_draw(pg, T, base, steps, tint, study, legend_cols, water_ok):
    """mp_map_draw (02d) with two round 5 additions for this page: the muted base's colours mixed P16_BASE_FADE
    toward paper (P17.2: the base recedes, the project reads in front) and the zone check's legend_cols / water_ok
    (G-R5-8: `zones p16 over_water_area, unlabeled_fields`). One draw order: base -> tint -> WATER -> panel."""
    cur = {"layer": None, "n": 0}
    steps = dict(steps or {})
    her_c = {BM_MUTED["her"]: hue("HER", 4), BM_MUTED["her_edge"]: hue("HER", 3)}   # v41 (Q5): no sourced status

    def fade(hx):
        if hx in her_c and (cur["layer"] or "").startswith("base_"):
            return her_c[hx]                             # v41: base heritage houses in the heritage browns, unfaded
        return mix(hx, "FFFFFF", P16_BASE_FADE) if hx and (cur["layer"] or "").startswith("base_") else hx

    def kind(hx):
        """v41 (G6-9): the element kind of a base / project call by its layer and colour"""
        lay = cur["layer"] or ""
        if lay in ("water", "base_water"):
            return "water"
        if lay == "study":
            return "annotations"
        if lay.startswith("base_"):
            if hx in her_c:
                return "heritage"
            if hx in (BM_MUTED["bld"], BM_MUTED["bld_edge"]):
                return "buildings"
            if hx in (BM_MUTED["road"], BM_MUTED["road_edge"]):
                return "roads"
            return "ground"
        return "other"

    def fill(rings, hx, a, nz):
        al = None if a is None or a >= 0.995 else a
        cur["n"] += 1
        pg.group(kind(hx), u"%s %d" % (cur["layer"] or u"base", cur["n"]))
        if nz and len(rings) > 1:
            for r_ in rings:
                pg.poly([r_], fill=fade(hx), alpha=al)
        else:
            pg.poly(rings, fill=fade(hx), alpha=al)
        pg.endgroup()

    def line(pts, hx, w, dash, a):
        cur["n"] += 1
        pg.group(kind(hx), u"%s %d" % (cur["layer"] or u"base", cur["n"]))
        pg.line(pts, fade(hx), w, list(dash) if dash else None, cap=0 if dash else 1,
                alpha=None if a is None or a >= 0.995 else a)
        pg.endgroup()

    def text(s_, xy, size, hx, bold, align):
        pg.text(s_, xy[0], xy[1], size, hx, bold=bool(bold), align=align if align in ("L", "C", "R") else "L",
                role="base_name")
    project = {}
    if tint:
        project["proj_tint"] = list(tint)
    for k_ in steps:
        project.setdefault(k_, []).append(("step",))

    def order(layer):
        cur["layer"] = layer
        f_ = steps.get(layer)
        if f_ is not None:
            f_()
    return map_draw(u"p15", T, fill, line, text, base, project, study=study, clip=True, order_fn=order,
                    water_opts=P16_WATER_OPTS, legend_cols=legend_cols, water_ok=water_ok)


def _p16_sw(fn):
    """a legend sample function f(pg, x, y, w, h) from a drawer centred on (cx, cy)"""
    return lambda pg_, x, y, w, h: fn(pg_, x + w / 2.0, y + h / 2.0)


def _p16_north_deg(V):
    """the survey north in the strip's View frame, degrees from up, counter-clockwise (as keymap north_items)"""
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    nu, nv = nu - V.uv((V.cx, V.cy))[0], nv - V.uv((V.cx, V.cy))[1]
    return math.degrees(math.atan2(-nu, nv))


def _p16_legend(key, G, cell):
    """the cell's key column as legend entries [(sample, text)] (round 5: the booklet sets it beside its drawing)"""
    out = []
    if key == "zones":
        st, bs = BM_STUDY_LINE, G.get("base_kinds") or {}
        if G["study"]:
            out.append((_sw_line(st["colour"], st["width_mm"], list(st["dash_mm"])), R28_STUDY_NAME))
        if G.get("tint"):
            out.append((_sw_fill(ML_TINT, alpha=ML_TINT_ALPHA), u"What we change"))
        zk = sorted(set(cell.get("zone_keys") or []), key=lambda k_: _p16_cat_key(P16_ZONE_HUE.get(k_, ("~", 9))))
        for k_ in zk:                                    # v41 (G6-6): by category, darker first
            nm, hx = R28_ZONE[k_][0], _p16_zone_col(k_)
            out.append((_sw_fill(hx, alpha=0.42 * P16_FADE), SN_ZONE_SHORT.get(k_, nm)))
        if "water" in bs:
            out.append((lambda pg_, x, y, w, h: _p16_water_swatch(pg_, x, y + h / 2.0, bs["water"], w, h * 0.75),
                        place_name("stream")))
        if "covered" in bs:
            out.append((_sw_line(bs["covered"][0], bs["covered"][1], bs["covered"][2]), u"Hidden (covered) stream"))
        if "street" in bs:
            out.append((_sw_fill(mix(bs["street"], "FFFFFF", P16_BASE_FADE)), u"Streets"))
        if "bld" in bs:
            out.append((_sw_fill(mix(bs["bld"][0], "FFFFFF", P16_BASE_FADE), mix(bs["bld"][1], "FFFFFF",
                                                                                 P16_BASE_FADE)), u"Buildings"))
        if "her" in bs:                                  # v41 (Q5): as the strips draw them (HER r4 / r3)
            out.append((_sw_fill(hue("HER", 4), hue("HER", 3)), u"Heritage buildings"))
    elif key == "feeling":
        out.append((_p16_sw(lambda pg_, x, y: sn_blot(pg_, x, y, 1.1, sn_mood_col(SN_MOOD["lively"]), 6, 5, False)),
                    u"Gathers"))
        out.append((_p16_sw(lambda pg_, x, y: sn_blot(pg_, x, y, 1.1, sn_mood_col(SN_MOOD["calm"]), 0, 6, False)),
                    u"Thins out"))
        out.append((_p16_sw(lambda pg_, x, y: (_p16_fig(pg_, "walk", x - 0.9, y - 1.1, 2.2),
                                                _p16_fig(pg_, "sit", x + 0.9, y - 1.1, 2.2))), u"What people do"))
    elif key == "sound":
        for k_, word, c in SN_SOUND:
            out.append((_p16_sw(lambda pg_, x, y, k_=k_, c=c: [sn_mark(pg_, k_, x + d_, y, c, 0.0)
                                                              for d_ in ((0.0,) if k_ == "wind" else (-1.2, 1.2))]),
                        word))
    elif key == "smell":
        shown = set(cell.get("smell_keys") or [k_ for k_, _w, _c in SN_SMELL])
        for k_, word, c in SN_SMELL:
            if k_ not in shown:
                continue
            ms = _p16_bloom(k_)
            out.append((_p16_sw(lambda pg_, x, y, c=c: (pg_.line(sn_ring(x, y, 1.0, 3, 0.08, 36) +
                                                                  sn_ring(x, y, 1.0, 3, 0.08, 36)[:1], c, 0.16),
                                                        pg_.circle(x, y, 0.45, fill=c))),
                        word + (u" · in flower " + u", ".join(_P16_MONTHS[m_ - 1] for m_ in ms) if ms else u"")))
    elif key == "history":
        if G.get("photos_out"):
            out.append((_p16_sw(lambda pg_, x, y: sn_num(pg_, x, y, 1, SN_HER)), u"Photo and its place"))
    return out


def _p16_wheel(ix, page):
    """the Feeling key's mood wheel as its own small diagram (mm): colour round the wheel = the mood"""
    W = 30.0
    wp = Page(W, W)
    cx, cy, r = W / 2.0, W / 2.0, 8.5
    wp.group("legend", u"mood wheel")                      # v42 (G6-9): the 72 segments are one element
    for i in range(72):
        a0, a1 = math.radians(5.0 * i), math.radians(5.0 * (i + 1))
        wp.line([(cx + r * math.cos(a0 + (a1 - a0) * t / 3.0), cy + r * math.sin(a0 + (a1 - a0) * t / 3.0))
                 for t in range(4)], sn_mood_col(5.0 * i + 2.5), 1.5, cap=0)
    wp.endgroup()
    fs = sn_mm(SN_TS["small"])
    wp.text(u"active", cx, cy + r + 1.6, fs, SN_INK, align="C")
    wp.text(u"passive", cx, cy - r - 1.6 - fs * 0.75, fs, SN_INK, align="C")
    wp.text(u"positive", cx + r + 1.8, cy - fs * 0.35, fs, SN_INK)
    wp.text(u"negative", cx - r - 1.8, cy - fs * 0.35, fs, SN_INK, align="R")
    return mpx_drawing(ix, "mp_sn_feeling_wheel", page, wp, (0.0, 0.0, W, W), None, dkind="diagram",
                       group="mp_senses", priority=4)


def _p16_enc_key(ix, page):
    """the Encounters key: the five vignette bubbles (v32, senses_ref3) with their marks, as one small diagram (mm)"""
    pitch, W = 10.0, 47.0
    H = pitch * len(P16_EXP)
    ep = Page(W, H)
    for i, (key, word, colour, pose) in enumerate(P16_EXP):
        by = H - pitch / 2.0 - pitch * i
        with mpx_grp(ep, "legend", u"encounter %s" % word):   # v42 (G6-9): mark + bubble = one element
            sn_enc_mark(ep, key, 4.5, by, colour, 1.0, 0.0, dirx=(1.0, 0.0))
            sn_bubble(ep, 11.0, by, key, word, colour, pose, i)
    return mpx_drawing(ix, "mp_sn_encounters_key", page, ep, (0.0, 0.0, W, H), None, dkind="diagram",
                       group="mp_senses", priority=4)


def p17_items(ix, C, areas, warn):
    """round 5 S6 (G-R5-12; addendum 1 Nov 22:37 point 2: no sheet PDF): booklet p17 "The senses and the water"
    (item page MPX_PAGE["p17"]) as items. The six strips are drawn as before (sn_* panels, one draw order) into ONE
    recorder Page; each strip = one true-scale drawing (1:SN_SCALE as drawn; units = the corridor View's metres,
    north_deg given), its title a heading, its key column a legend (the mood wheel and the encounter bubbles small
    diagrams), the History photos photo items; the words on the strips are anchored labels; the bridge names along
    the top edge are labels at their ticks. No scale bars, no north arrows, no page text in the drawings. Round 5:
    see-through sight wedges (P17.1); the base muted further (P17.2); land fields and feeling blots UNDER the water,
    only the wetland and the sub-hubs above it (G-R5-8); no layered heritage fields. Returns log lines."""
    t0 = time.time()
    page = MPX_PAGE["p17"]
    _P16_MEMO.clear()                                    # photos are read once a run
    G = sn_data(C, areas, warn)
    G["warn"] = warn
    pg = Page(SN_PW, SN_PH)
    pg.text_page(u"p15", margins=P16_TP_MARGINS)         # the round 4 placer still finds each word a free spot
    ix.text(page, SN_TITLE, "title", group="mp_senses", id="mp_sn_title", priority=1)
    ix.text(page, SN_KICKER.replace(u"   ", u" "), "intro", group="mp_senses", id="mp_sn_kicker", priority=2)
    funcs = {"zones": sn_zones, "feeling": sn_feeling, "sound": sn_sound, "smell": sn_smell,
             "encounters": sn_encounters, "history": sn_history}
    pos = [(SN_COLX[0], P16_ROWS[0]), (SN_COLX[1], P16_ROWS[0]), (SN_COLX[0], P16_ROWS[1]),
           (SN_COLX[1], P16_ROWS[1]), (SN_COLX[0], P16_ROWS[2]), (SN_COLX[1], P16_ROWS[2])]
    zone_cols = [_p16_zone_col(k_) for k_ in R28_ZONE]  # v41 (G6-6): the table's hues
    wet_cols = [_p16_zone_col(k_) for k_ in P16_WET_FIELDS if k_ in R28_ZONE]
    nd = _p16_north_deg(G["V"])
    fr = G["fr"]
    n_ok, out = 0, []
    for (cx, top), (title, key) in zip(pos, P16_CELLS):
        layer = funcs[key]
        cell = sn_cell(pg, G, cx, top, title)
        cell["upg"] = Page(SN_PW, SN_PH)                 # round 5: what goes UNDER the water (spliced in below)
        labs, box = [], cell["box"]
        n0 = len(pg.items)

        def panel(layer=layer, cell=cell, labs=labs, box=box):
            pg.unclip()
            try:
                labs.extend(layer(pg, G, cell, warn) or [])
            finally:
                pg.clip([rect(*box)])

        def marks(cell=cell):
            for f_ in cell["late"]:
                f_()

        def under(cell=cell):
            cell["under_at"] = len(pg.items)
        pg.clip([rect(*box)])
        try:
            _p16_map_draw(pg, cell["T"], G["base"], {"proj_tint": under, "proj_lines": panel, "proj_marks": marks},
                          G["tint"] if title in P16_TINT_PANELS else (), G["study"] or None,
                          [ML_TINT] + zone_cols, wet_cols)
            n_ok += 1
        except Exception as ex:
            import traceback
            warn.append(u"senses p15: panel {} not drawn ({}: {})".format(title, type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
        if cell.get("under_at") is not None and cell["upg"].items:
            i_ = cell["under_at"]
            pg.items[i_:i_] = cell["upg"].items
        open_ = sum(1 if it[0] == "clip" else -1 if it[0] == "unclip" else 0 for it in pg.items[n0:])
        for _ in range(max(0, open_)):
            pg.unclip()
        sn_outline(pg, G, cell)
        sn_place(pg, cell, labs, warn)
        did = u"mp_sn_" + key
        D = mpx_drawing(ix, did, page, pg, box, SN_SCALE, origin_m=(fr[0], fr[1]), dkind="plan", north_deg=nd,
                        group="mp_senses", priority=1, items=pg.items[n0:])
        ix.text(page, title, "heading", drawing=did, group="mp_senses", id=did + u"_head", priority=3)   # v42 box
        for nm, xy in BRIDGES_K:                         # the bridge names at their ticks on the top edge (labels)
            x = cell["T"](xy)[0]
            if box[0] <= x <= box[2] and nm not in ("K1", "K2"):
                u_ = fr[0] + (x - box[0]) / SN_K
                ix.text(page, bridge_name(nm, short=True), "label", drawing=D["id"], at=(u_, fr[3]),
                        size_pt=SN_TS["small"] - 1.0, colour=SN_INK2, positions=["S", "SE", "SW"],
                        group="mp_senses", priority=7)
        ents = [(mpx_sw(f_), t_) for f_, t_ in _p16_legend(key, G, cell)]
        if ents:
            ix.legend(page, D["id"], ents, id=did + u"_key", group="mp_senses")
        if key == "feeling":
            _p16_wheel(ix, page)
        elif key == "encounters":
            _p16_enc_key(ix, page)
        elif key == "history":
            for n_, path, cap, credit in G.get("photos_out") or []:
                ix.photo(page, path, caption=u"{} {}".format(n_, u" · ".join(cap)), source=credit,
                         id=u"mp_sn_photo_%d" % n_)
    if callable(globals().get("basemap_warnings")):
        warn.extend(basemap_warnings())
    MPX_PAGES.append(("A", "p15", pg))
    out.append(u"legend p15 hues=table")                 # v41 (G6-6): every key above reads common/hues.py
    out.append(u"trees p15 species=0 generic=0 (no tree symbols on this page: the forest is a zone field)")
    out.append(u"p15 senses: strips {}/6 exported (1:{:,.0f} as drawn, zones: {}), D9 tint {} rings, photos {}, "
               u"base faded {:.0%}, {:.1f} s".format(n_ok, SN_SCALE, G["fields_src"], len(G.get("tint") or []),
                                                     len(G.get("photos_out") or []), P16_BASE_FADE,
                                                     time.time() - t0))
    return out
