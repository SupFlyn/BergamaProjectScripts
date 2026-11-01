# p.16 the senses and the water: senses_sheet and its sn_* helpers (split from parts/02e_r28_detail.py, parts/02f_r28_senses.py on 29 Oct 2026; moved unchanged)
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
P16_MK_STEP = 3.4                            # design value: centre distance of two stacked History markers, mm
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
    return ml_tint(R, study=st, page=u"p16") if st else ml_tint(R)


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
    """house shapes of common/icons.py ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) on the page"""
    for sh in shapes or ():
        if sh[0] == "poly":
            pg.poly([sh[1]], fill=sh[2], stroke=sh[3], lw=sh[4] if len(sh) > 4 else 0.1)
        elif sh[0] == "line":
            pg.line(sh[1], sh[2], sh[3] if len(sh) > 3 else 0.1)


def sn_cell(pg, G, cx, top, title):
    """one cell: the strip frame (the widened analysis frame at 1:20,000, P16_STRIP_H tall), the panel title at the
    top of its key column (v38, P16.1: the strip's top band holds only the bridge ruler) and the bridge ruler on the
    frame's top edge. v38 (P16.3): the base, the tint and the study line are no longer drawn here: senses_sheet draws
    them with the panel through mp_map_draw (one draw order). Returns the cell (T, box, label bounds, the lines
    labels stay off (segs), boxes they stay off (taken), late = mark drawers for layer proj_marks)."""
    V, fr = G["V"], G["fr"]
    sw, sh = (fr[2] - fr[0]) * SN_K, (fr[3] - fr[1]) * SN_K
    x0, y1 = cx, sn_y(top + P16_STRIP_TOP)
    box = (x0, y1 - sh, x0 + sw, y1)
    T = sn_T(V, box[0], box[1], fr[0], fr[1])
    sx = cx + SN_SIDE
    pg.text(title, sx, sn_y(top + 5.0), sn_mm(SN_TS["panel"]), SN_INK, bold=True, name=u"p16 title " + title,
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
                pg.text(s, xl, yb, fs, SN_INK2, name=u"p16 ruler " + title, role="ruler")
                ruler.append(b)
                break
        else:
            cell.setdefault("ruler_missing", []).append(s)
    return cell


def sn_outline(pg, G, cell):
    """the frame's own hairline (T4: the study area is drawn with the base, sn_cell)"""
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
                bb = (b[0] - 0.3, b[1] - 0.3, b[2] + 0.3, b[3] + 0.3)
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
                             u"p16 {} {}".format(cell.get("title", u""), L_["s"]))
            if got:
                break
        if got is None:
            if rank == 0:
                warn.append(u"FLAG p16 {}: no free spot on the strip for the word '{}' (not printed)".format(
                    cell.get("title", u""), L_["s"]))
            else:
                n_more += 1
    if n_more:
        warn.append(u"senses sheet {}: {} repeat(s) of a word already on the strip left out (no free spot)".format(
            cell.get("title", u""), n_more))


def _p16_fig(pg, pose, x, y, h, facing=1):
    """p.16's ONE figure point: the figure library's side view (common/figures.py fig_side; adult 1.70 m), h mm
    tall on this diagram (pictogram size, not to scale), feet at (x, y). "sit" = sit_chair. v38 (round 4,
    G-R4-5.1): people are black (figures.py pen_black set); the colour argument (ink=) is gone."""
    k = h / 1.70
    _p16_shapes(pg, fig_side({"sit": "sit_chair"}.get(pose, pose), x, y, k, facing))


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
    pg.text(s, cell["side"], yb, fs, SN_INK, bold=True, name=u"p16 key title", role="legend")
    return yb - 3.6


def sn_key_foot(pg, G, cell):
    """T4 (G1: every plan its own scale bar and north arrow): the north arrow and the scale bar at the foot of the
    key column, level with its strip's bottom edge (rows above end 19 mm over it)"""
    sx, yb = cell["side"], cell["box"][1] + 2.4
    sn_north(pg, G["V"], sx + 4.0, yb)
    sn_scale_bar(pg, sx + 11.0, yb, (0.0, 100.0, 250.0, 500.0))


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
        name, hx = R28_ZONE[key]
        Ps = [Q for Q in ([T(p) for p in R] for R in rings) if len(Q) >= 3 and sn_in(bbox(Q), box)]
        if not Ps:
            continue
        sn_field(pg, Ps, hx)
        for Q in Ps:                                     # the words stay off the fields' edges
            Qs = Q[::max(1, len(Q) // 24)] + Q[:1]
            cell["segs"].extend(zip(Qs, Qs[1:]))
        at = inner_pt(max(Ps, key=lambda Q: abs(area2(Q))))
        labs.append(dict(s=SN_ZONE_SHORT.get(key, name), at=at, col=mix(hx, SN_DARK, 0.5)))
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


def sn_north(pg, V, ax, ay):
    """v38 (round 4, G-R4-9): THE north arrow of common/keymap.py (north_items: arrow and "N", no plate), its foot at
    (ax, ay), turned with the strips (survey +Y in the View), P16_NORTH_MM tall; drawn through basemap_draw with the
    page's own calls ("N" registered in the TextPage like every text)"""
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    L = math.hypot(nu, nv) or 1.0
    nx_, ny_ = nu / L, nv / L
    its = north_items(ax, ay, math.atan2(-nx_, ny_), P16_NORTH_MM, SN_DARK)

    def fill(rings, hx, a, nz):
        pg.poly(rings, fill=hx)

    def line(pts, hx, w, dash, a):
        pg.line(pts, hx, w)

    def text(s_, xy, size, hx, bold, align):
        y_ = xy[1]
        if align in ("MC", "CM"):                        # (x, y) = the middle of the ink: to the baseline
            ix0, iy0, ix1, iy1 = fm_ink_box(s_, size / PT, bool(bold))
            y_ = xy[1] - (iy0 + iy1) / 2.0
            align = "C"
        pg.text(s_, xy[0], y_, size, hx, bold=bool(bold), align=align if align in ("L", "C", "R") else "L",
                name=u"p16 north", role="north")
    basemap_draw(its, lambda p: p, fill, line, text)


def sn_scale_bar(pg, x, y, marks):
    """a strip's scale bar (m), its bar from y to y + 1.2: the numbers at 7 pt under it, the scale over its start
    (T4: fits the 46 mm key column beside the north arrow)"""
    for i, (a, b) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * SN_K, y, x + b * SN_K, y + 1.2)], fill=SN_DARK if i % 2 == 0 else "FFFFFF",
                stroke=SN_DARK, lw=0.15)
    fs = sn_mm(SN_TS["small"])
    for m_ in marks:
        pg.text(u"{:,.0f}{}".format(m_, u" m" if m_ == marks[-1] else u""), x + m_ * SN_K, y - fs * 0.95, fs,
                SN_INK, align="C")
    pg.text(u"1:{:,.0f}".format(SN_SCALE), x, y + 2.0, fs, SN_DARK, bold=True)


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
        if sn_in((x, y, x, y), box, 6.0):
            sn_blot(pg, x, y, R, sn_mood_col(SN_MOOD[mood]), veins, 11 + i)
    for p, mood, R, veins, pose in B:                    # pictograms (senses_ref1's black figures), not crowded
        x, y = T(p)
        if pose and sn_in((x, y, x, y), box) and all(math.hypot(x - a, y - b) >= 2.2 for a, b in figs):
            _p16_fig(pg, pose, x, y - 1.4, 2.8)
            figs.append((x, y))
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
    for z in G["zones_raw"]:                             # reeds: the lined reed basins only (v28.1, D2: the side
        if z["code"] == "WT":                            # arms are open channels with rush and loosestrife, no reed)
            sn_cluster(pg, "reeds", T(z["q"]), 2.2, 7, col["reeds"], rnd, 0.25)
    for p in sn_spaced(G["forest"], T, 7.0):             # birds: the forest corridor and the wetland (v32: 7 mm)
        x, y = T(p)
        sn_cluster(pg, "birds", (x, y + 0.8), 1.2, 2, col["birds"], rnd)
    for p in sn_spaced([w["at"] for w in G["widen"]], T, 6.0):
        x, y = T(p)
        sn_cluster(pg, "birds", (x, y + 1.2), 1.8, 4, col["birds"], rnd)
    kids = [h["sub_xy"]["c"] for h in G["hubs"] if h.get("sub_xy")] + \
        [h["xy"] for h in G["hubs"] if h["role"] == "walking" and h["id"] != u"K6"]
    for p in kids:                                       # children at the edge: the sub-hubs and the hub squares
        sn_cluster(pg, "children", T(p), 1.4, 4, col["children"], rnd)
    for p in G["market"] + ([G["kermes"]] if G["kermes"] else []):   # market and Kermes voices
        sn_cluster(pg, "voices", T(p), 1.5, 3, col["voices"], rnd, math.pi)
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
    for p in sn_spaced(wind, T, 14.0):                   # wind: the open places (viewing terrace, widened stream)
        x, y = T(p)
        ang = sn_page_ang(V, at_len(ref, s, chain_at(ref, p)[0])[1]) if len(ref) >= 2 else 0.0
        for j in range(3):
            sn_mark(pg, "wind", x + (j - 1) * 1.2, y + (j - 1) * 1.3, col["wind"], ang)
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
        for k in range(n):
            Q = sn_ring(x, y, r0 + k * dr, 101 + i, 0.06 + 0.03 * k, 56)
            pg.line(Q + Q[:1], col[key], 0.16, alpha=(0.9 - 0.55 * k / (n - 1.0)) * P16_FADE)
        dots.append((x, y, col[key]))
    for x, y, c in dots:
        pg.circle(x, y, 0.6, fill=c)
    pg.unclip()
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
        pg.poly([[(x, y), tip1, tip2]], fill=mix(colour, "FFFFFF", 0.55), stroke=colour, lw=0.25)
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
# v38 (P16.2): FIVE distinct hues, one per encounter type (K2: the types, words, poses and marks unchanged), all
# Bergama palette v1.4 colours (palette.json): WALK and TOUCH as PLAN §4.10 sets them, the other three chosen so
# WALK and TOUCH are not hue neighbours. Checked offline (OKLCH hue, CIEDE2000, WCAG contrast; 1 Nov 2026):
#   key       hex     source (palette.json)          OKLCH h  L     on paper / muted house EDEBE6 / D9 tint E4E9EB
#   touch     8B2D2D  image A brick red (accent)      24.1   0.44   8.36 / 7.02 / 6.83
#   cross     8C5D05  figure_colours ochre            74.2   0.52   5.70 / 4.79 / 4.66
#   watch     3C4733  image A dark green (green_deep) 131.4  0.38   9.81 / 8.23 / 8.01
#   walk      5C7A86  image B slate blue (water_deep) 224.4  0.56   4.58 / 3.85 / 3.74
#   remember  8C7088  land_use institutional plum     331.0  0.58   4.39 / 3.68 / 3.58
# hue order round the wheel: touch - cross - watch - walk - remember - touch: WALK's neighbours are watch and
# remember, TOUCH's are cross and remember; WALK to TOUCH 160 deg, dE00 40.9. Smallest pair: walk / watch dE00 24.6
# (93 deg); every pair >= 24.6 (v37: watch / walk 16.8). Against the study line 6A4C93: dE00 >= 17.5 (remember).
# All marks are drawn on a white casing / rim, so the water (91ADB4, contrast 1.85-4.13) never carries them alone.
# REMEMBER leaves the heritage red (v37 8B3A3F): next to TOUCH's brick red it was the colour pair Aras saw as one.
P16_EXP = (("watch", u"Watch", "3C4733", "watch"), ("walk", u"Walk", "5C7A86", "walk"),
           ("touch", u"Touch", "8B2D2D", "touch"), ("cross", u"Cross", "8C5D05", "wade"),
           ("remember", u"Remember", "8C7088", "stand"))


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

    def late():                                          # layer order kept: cross, watch, touch, remember
        for k_, x_, y_, ux_, uy_, d_ in marks:
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


def sn_layers_round(pg, x, y, R, colour, seed, n=6, a=0.1 * P16_FADE):
    for k in range(n):
        pg.poly([sn_ring(x, y, R * (1.0 - k / float(n)), seed, 0.12, 40, (2, 3))], fill=colour, alpha=a)
    return (x, y)


def sn_layers_band(pg, P, W, colour, n=6, a=0.1 * P16_FADE):
    """layers along a page polyline, each narrower and shorter: darkest at the core"""
    s = arclen(P)
    L = s[-1]
    for k in range(n):
        cut = L * 0.22 * k / float(n)
        Q = sn_band(sub_line(P, s, cut, L - cut) if L > 2.0 * cut + 0.2 else P, W * (1.0 - k / float(n)), 0.35)
        if len(Q) >= 3:
            pg.poly([Q], fill=colour, alpha=a)
    return at_len(P, s, L / 2.0)[0]


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


def _p16_photo_row(keys_at, box, avoid, capm):
    """T4 (PG1 p15 "the photos are scattered"): ONE ordered row of photos along the strip's top or bottom edge, left
    to right in the order of their places, each as near above or below its place as the row allows; the edge whose
    band covers the fewest places (weight per point in avoid = [((x, y), weight)]) is taken. capm = the caption's
    room under each photo. Returns ({key: (x, y) lower-left photo corner}, W, H)."""
    n = len(keys_at)
    if not n:
        return {}, 0.0, 0.0
    gap = 2.4
    W = min(P16_PHOTO_W, (box[2] - box[0] - 2.0 - (n - 1) * gap) / float(n))
    H = W * P16_PHOTO_H / P16_PHOTO_W
    srt = sorted(keys_at, key=lambda e: e[1][0])
    xs, prev = [], box[0] + 1.0 - gap
    for k, a in srt:
        x = max(a[0] - W / 2.0, prev + gap)
        xs.append(x)
        prev = x + W
    over = xs[-1] + W - (box[2] - 1.0)
    if over > 0.0:                                       # pulled back from the right edge, the order kept
        xs[-1] -= over
        for j in range(n - 2, -1, -1):
            xs[j] = min(xs[j], xs[j + 1] - gap - W)
    best = None
    for top in (True, False):
        yb = box[3] - 1.0 - H - capm if top else box[1] + 1.0     # the band's bottom (captions under the photos)
        sc = sum(w for (px, py), w in avoid
                 if yb - 1.0 <= py <= yb + H + capm + 1.0 and any(x - 1.0 <= px <= x + W + 1.0 for x in xs))
        if best is None or sc < best[0]:
            best = (sc, yb)
    y = best[1] + capm
    return dict((k, (x, y)) for (k, a), x in zip(srt, xs)), W, H


def sn_num(pg, x, y, n_, colour):
    """a numbered marker (G3: its number explained by the photo caption of the same number). v38 (round 4, G-R4-7):
    the ONE marker (mp_marker: glyph centred on its ink box, radius from the glyph, kept in the TextPage), in the
    colour of the element it names (the heritage fields, SN_HER); returns its box"""
    return mp_marker(pg, x, y, u"{}".format(n_), colour, size_pt=SN_TS["small"])[0]


def sn_history(pg, G, cell, warn):
    """layered heritage fields on the stream's places (senses_ref2) and, T4, the photos (P16_PLACES) in ONE ordered
    row along the strip's top or bottom edge, numbered left to right; the same number marks each photo's place on
    the map (no leaders, nothing crosses). Own photos and csv photos alike carry no credit on the sheet (G12: the
    credits go to the Sources page). The photos are embedded by _p16_save (the core's PDF writer draws no images)."""
    T, box = cell["T"], cell["box"]
    txt = COL["accent_dark"]
    labs, anchors = [], {}

    def field(q, half, R, seed):
        """a field along the stream line round q (half m either side), else a round one"""
        P = [T(p) for p in sn_ref_piece(G, q, half)] if half else []
        if len(P) >= 2 and arclen(P)[-1] > 0.5:
            return sn_layers_band(pg, P, R, SN_HER)
        x, y = T(q)
        return sn_layers_round(pg, x, y, R, SN_HER, seed)
    pg.clip([rect(*box)])
    ka = G["hub"].get(u"Kızıl Avlu")                     # the Kızıl Avlu tunnels: the covered reach under it (H2)
    if ka:
        best = None
        for P in G["covered"]:
            c, d = chain_at(P, ka["xy"])
            if d <= 150.0 and (best is None or d < best[0]):
                best = (d, P, c)
        if best:
            d, P, c = best
            Q = [T(p) for p in sub_line(P, arclen(P), max(0.0, c - 90.0), min(arclen(P)[-1], c + 90.0))]
            at = sn_layers_band(pg, Q, 1.6, SN_HER) if len(Q) >= 2 and arclen(Q)[-1] > 0.5 else \
                sn_layers_round(pg, T(ka["xy"])[0], T(ka["xy"])[1], 2.4, SN_HER, 31)
        else:
            at = sn_layers_round(pg, T(ka["xy"])[0], T(ka["xy"])[1], 2.4, SN_HER, 31)
        anchors["tunnels"] = at
    bk = dict(BRIDGES_K)
    for i, k in enumerate(("K3", "K5")):                 # the Roman bridges (h01 §5 P08, P09; K4 "Roman?", P06)
        if bk.get(k):
            x, y = T(bk[k])
            anchors[k.lower()] = sn_layers_round(pg, x, y, 2.3, SN_HER, 40 + i)
    if G["bath"]:                                        # Tabaklar Hamamı (H4)
        x, y = T(G["bath"])
        anchors["hamam"] = sn_layers_round(pg, x, y, 2.0, SN_HER, 50)
    anchors["tabakhane"] = field(CRAFT_XY, 70.0, 1.8, 60)   # Tabakhane (H3)
    if G["kermes"]:                                      # Kermes in the dry bed (h01 §2.8), at the S4 cut (v29: photo)
        anchors["kermes"] = field(G["kermes"], 90.0, 1.8, 70)
    pg.unclip()
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
    fs = sn_mm(SN_TS["small"])
    lh = fs * 1.2
    capm = 0.8 + 2.0 * lh                                # two caption lines under each photo
    avoid = [(a, 50.0) for a in anchors.values()] + [(p, 1.0) for p in (T(q) for q in G["ref"])] + \
        [(p, 1.0) for A in G["study"] for p in (T(q) for q in A)]
    slots, W, H = _p16_photo_row(with_ph, box, avoid, capm)
    # v38 (round 4, G-R4-1, G-R4-7): each caption's number is an mp_marker (centre 1.6 mm in, the caption 4.0 mm in:
    # disc edge to text >= 0.6 mm); each photo is kept in the TextPage (no text on a picture); the map markers move
    # off the photo band (away from it, P16_MK_STEP at a time) and apart from each other, and are drawn in layer
    # proj_marks (above the study line)
    order = sorted(with_ph, key=lambda e: slots[e[0]][0])
    capboxes = []
    for n_, (k, a) in enumerate(order, 1):
        x, y = slots[k]
        path = ph[k][0]                                  # ph[k][1] = the csv credit line: Sources page only (G12)
        cap = names[k]
        lines = wrap(cap[0], fs, W - 4.0, True)
        if len(lines) > 2:
            warn.append(u"FLAG p16 History: caption '{}' needs {} lines under its photo (2 shown)".format(
                cap[0], len(lines)))
            lines = lines[:2]
        nb = len(lines)                                  # the name's lines are bold, a second caption line is not
        if nb == 1 and len(cap) > 1:
            if text_w(cap[1], fs) <= W - 4.0:
                lines.append(cap[1])
            else:
                warn.append(u"FLAG p16 History: '{}' does not fit under its photo (left out)".format(cap[1]))
        yb = y - 0.8 - fs * 0.8
        sn_num(pg, x + 1.6, yb + fs * 0.36, n_, SN_HER)
        for j, s in enumerate(lines):
            pg.text(s, x + 4.0, yb - j * lh, fs, txt if j < nb else SN_INK2, bold=(j < nb), name=u"p16 caption",
                    role="caption")
        pg.keep((x, y, x + W, y + H), "photo", u"p16 photo {}".format(n_))
        capboxes.append((x, y - capm, x + W, y + H))
        G.setdefault("imgs", []).append((path, (x, y, W, H)))
    cell["taken"] += capboxes
    top_band = bool(order) and slots[order[0][0]][1] > (box[1] + box[3]) / 2.0
    away = -1.0 if top_band else 1.0                     # markers step away from the photo band
    rm = 1.8                                             # a marker's half size with its rim, mm (7 pt, <= 1.68)
    marks, ties = [], []
    for n_, (k, a) in enumerate(order, 1):
        m_ = (a[0], a[1])                                # its place on the map, the same number
        for _i in range(12):
            mb = (m_[0] - rm, m_[1] - rm, m_[0] + rm, m_[1] + rm)
            if not (any(math.hypot(m_[0] - q[1], m_[1] - q[2]) < P16_MK_STEP for q in marks) or
                    any(tp_hit(mb, cb, 0.7) for cb in capboxes)):
                break
            m_ = (m_[0], min(max(m_[1] + away * P16_MK_STEP, box[1] + rm + 0.6), box[3] - rm - 0.6))
        if m_ != (a[0], a[1]):                           # moved: a short tie to its place
            ties.append([a, (m_[0], m_[1] - away * 1.4)])
        marks.append((n_, m_[0], m_[1]))
        cell["taken"].append((m_[0] - rm, m_[1] - rm, m_[0] + rm, m_[1] + rm))

    def late():
        for P in ties:
            pg.line(P, SN_INK2, 0.15)
        for n_, x_, y_ in marks:
            sn_num(pg, x_, y_, n_, SN_HER)
    cell["late"].append(late)
    sx = cell["side"]                                    # key column: the heritage field, the numbered places
    y = sn_key_title(pg, cell)                           # v38 (G-R4-2): the panel title says "History"
    sn_layers_round(pg, sx + 4.5, y, 2.3, SN_HER, 40)
    sn_key_row(pg, sx + 11.0, y, u"Heritage place")
    if with_ph:
        y -= P16_KEY_ROW + 1.0
        sn_num(pg, sx + 4.5, y, 1, SN_HER)
        sn_key_row(pg, sx + 11.0, y, u"Photo and its place")   # v38 (G-R4-2): one row (v37: two)
    return labs


# ---------------------------------------------------------------- the sheet's writer with photos (T4a)
def _p16_write_pdf(pg, path, title, imgs):
    """the core's write_pdf (parts/01) plus JPEG photos: imgs = [(path, (x, y, w, h) page mm)], each embedded once
    as a DCTDecode image XObject, drawn after the page's vector items (cropped to fill its slot, a hairline frame).
    Kept here because the core's writer draws no images (T4b may move image support into the core)."""
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    font = pdf_fonts(add, ("R", "B"))
    gs = [add("<< /Type /ExtGState /ca {0} /CA {0} >>".format(_f(i / 100.0)).encode("latin-1")) for i in range(1, 100)]
    gs_res = " ".join("/A{:02d} {} 0 R".format(i + 1, o_) for i, o_ in enumerate(gs))
    xo, ops, names = [], [], {}
    for p_, (x, y, w, h) in imgs:
        j = _p16_jpeg(p_)
        if not j:
            continue
        iw, ih, nc, data = j
        if p_ not in names:
            oid = add("<< /Type /XObject /Subtype /Image /Width {} /Height {} /ColorSpace /{} /BitsPerComponent 8 "
                      "/Filter /DCTDecode /Length {} >>\nstream\n".format(
                          iw, ih, "DeviceRGB" if nc == 3 else "DeviceGray", len(data)).encode("latin-1") +
                      data + b"\nendstream")
            names[p_] = "/Im{}".format(len(names) + 1)
            xo.append("{} {} 0 R".format(names[p_], oid))
        a = iw / float(ih)
        dw, dh = (h * a, h) if a > w / h else (w, w / a)
        r_, g_, b_ = hex_rgb(SN_INK2)
        ops.append("q {} {} {} {} re W n {} 0 0 {} {} {} cm {} Do Q".format(
            _f(x), _f(y), _f(w), _f(h), _f(dw), _f(dh), _f(x - (dw - w) / 2.0), _f(y - (dh - h) / 2.0), names[p_]))
        ops.append("q {} {} {} RG 0.15 w {} {} {} {} re S Q".format(_f(r_), _f(g_), _f(b_), _f(x), _f(y), _f(w), _f(h)))
    pages_id = add(b"")
    body = page_stream(pg) + (("\n" + "\n".join(ops)).encode("latin-1") if ops else b"")
    data = zlib.compress(body, 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data +
              b"\nendstream")
    kid = add("<< /Type /Page /Parent {} 0 R /MediaBox [0 0 {} {}] /Contents {} 0 R /Resources << /Font "
              "<< /F1 {} 0 R /F2 {} 0 R >> /ExtGState << {} >>{} >> >>".format(
                  pages_id, _f(pg.W / PT), _f(pg.H / PT), cid, font[0], font[1], gs_res,
                  " /XObject << {} >>".format(" ".join(xo)) if xo else "").encode("latin-1"))
    objs[pages_id - 1] = "<< /Type /Pages /Kids [{} 0 R] /Count 1 >>".format(kid).encode("latin-1")
    cat = add("<< /Type /Catalog /Pages {} 0 R >>".format(pages_id).encode("latin-1"))
    info = add(b"<< /Title " + pdf_str(title) + b" /Producer " + pdf_str(VERSION) + b" >>")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += "{} 0 obj\n".format(i + 1).encode() + b + b"\nendobj\n"
    x = len(out)
    out += "xref\n0 {}\n0000000000 65535 f \n".format(len(objs) + 1).encode()
    for o_ in offs:
        out += "{:010d} 00000 n \n".format(o_).encode()
    out += "trailer\n<< /Size {} /Root {} 0 R /Info {} 0 R >>\nstartxref\n{}\n%%EOF\n".format(
        len(objs) + 1, cat, info, x).encode()
    with open(path, "wb") as fh:
        fh.write(bytes(out))


def _p16_save(pg, folder, name, title, imgs):
    """the core's save() with _p16_write_pdf: a new name when the old file is open in another program"""
    path = os.path.join(folder, name)
    try:
        _p16_write_pdf(pg, path, title, imgs)
    except (IOError, OSError):
        path = os.path.join(folder, name.replace(".pdf", datetime.datetime.now().strftime("_%H%M%S.pdf")))
        _p16_write_pdf(pg, path, title, imgs)
    return path


# ---------------------------------------------------------------- the sheet
def senses_sheet(C, areas, folder, files, warn, basemap=None):
    """S1: writes Bergama_senses_A3.pdf into the masterplan's output folder (the masterplan's PDF writer, Arial
    embedded; with History photos _p16_save, the same writer plus JPEG images); returns the log line. Called once a
    press by build_all (a failure is only a warning there). v38 (round 4): basemap is ignored (one muted base for all
    six strips, P16.3); every text goes through the sheet's TextPage "p16" and pg.check_text() runs before the PDF
    is written (a collision raises TextCollision: the sheet is not written, the log names page, text and obstacle).
    Per strip, ONE draw order through mp_map_draw: the muted base -> the D9 tint (P16_TINT_PANELS) -> the panel
    (proj_lines) -> the study line -> its marks (proj_marks) -> then the words (sn_place)."""
    t0 = time.time()
    _P16_MEMO.clear()                                    # photos are read once a run
    G = sn_data(C, areas, warn)
    G["warn"] = warn
    pg = Page(SN_PW, SN_PH)
    pg.text_page(u"p16", margins=P16_TP_MARGINS)         # v38 (G-R4-1): every text registered from here on
    pg.poly([rect(0.0, 0.0, SN_PW, SN_PH)], fill="FFFFFF")
    pg.text(SN_KICKER, SN_ML, sn_y(12.0), sn_mm(SN_TS["kicker"]), SN_ACC, bold=True, name=u"p16 kicker",
            role="heading")                              # the booklet's header band
    pg.text(SN_TITLE, SN_ML, sn_y(22.0), sn_mm(SN_TS["title"]), SN_INK, bold=True, name=u"p16 title",
            role="heading")
    pg.line([(SN_ML, sn_y(25.0)), (SN_PW - SN_ML, sn_y(25.0))], SN_RULE, 0.25 * SN_PT)
    # v38 (P16.1, G-R4-2): no statement line (its facts are on the sheet once: the scale on every bar, the one base
    # in the base key); the cells start at P16_ROWS[0]
    cells = [(SN_COLX[0], P16_ROWS[0], u"Zones", sn_zones),
             (SN_COLX[1], P16_ROWS[0], u"Feeling", sn_feeling),
             (SN_COLX[0], P16_ROWS[1], u"Sound", sn_sound),
             (SN_COLX[1], P16_ROWS[1], u"Smell", sn_smell),
             (SN_COLX[0], P16_ROWS[2], u"Encounters", sn_encounters),
             (SN_COLX[1], P16_ROWS[2], u"History", sn_history)]
    n_ok = 0
    for cx, top, title, layer in cells:
        cell = sn_cell(pg, G, cx, top, title)
        for s_ in cell.get("ruler_missing") or []:      # v37: a bridge name with no room on the ruler
            warn.append(u"senses sheet {}: bridge name not on the ruler (no room): {}".format(title, s_))
        labs, n0, box = [], len(pg.items), cell["box"]

        def panel(layer=layer, cell=cell, labs=labs, box=box):
            pg.unclip()                                  # the panel clips its own strip work; its key column is
            try:                                         # outside the strip
                labs.extend(layer(pg, G, cell, warn) or [])
            finally:
                pg.clip([rect(*box)])

        def marks(cell=cell):
            for f_ in cell["late"]:
                f_()
        pg.clip([rect(*box)])
        try:
            mp_map_draw(pg, u"p16", cell["T"], G["base"], steps={"proj_lines": panel, "proj_marks": marks},
                        tint=G["tint"] if title in P16_TINT_PANELS else (), study=G["study"] or None,
                        water_opts=P16_WATER_OPTS)
            n_ok += 1
        except TextCollision:
            raise
        except Exception as ex:
            import traceback
            warn.append(u"senses sheet: panel {} not drawn ({}: {})".format(title, type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
        open_ = sum(1 if it[0] == "clip" else -1 if it[0] == "unclip" else 0 for it in pg.items[n0:])
        for _ in range(max(0, open_)):                   # close the strip's clip (and any a failed panel left open)
            pg.unclip()
        sn_outline(pg, G, cell)
        sn_key_foot(pg, G, cell)
        sn_place(pg, cell, labs, warn)
    if callable(globals().get("basemap_warnings")):
        warn.extend(basemap_warnings())                  # e.g. the M5 stream fell back to the plain fill
    pg.check_text(log=TP_LOG)                            # v38 (G-R4-1): raises TextCollision; logs "overlap p16 ..."
    imgs = G.get("imgs") or []
    path = _p16_save(pg, folder, SN_NAME, SN_TITLE, imgs) if imgs else save(pg, folder, SN_NAME, SN_TITLE)
    files.append(path)
    return u"{}  {}  {:.1f} s (zones: {}; strips {}/6 on one muted base, D9 tint {} rings)".format(
        os.path.basename(path), datetime.datetime.now().strftime("%H:%M:%S"), time.time() - t0, G["fields_src"],
        n_ok, len(G.get("tint") or []))
