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

# D5 / M3: (mode, override) of the basemap per panel, the same base under all six (T4, PG1 p15 "every analysis map
# sits on the M3 base"); senses_sheet(..., basemap={title: (mode, override)}) changes a panel's choice for one run
P16_BASEMAP = dict((t_, ("base", {"buildings": "veryfaint"})) for t_ in (u"Zones", u"Feeling", u"Sound", u"Smell", u"Encounters",
                                                    u"History"))
P16_WATER_OPTS = {"spacing": 0.6, "seed": 5}  # M5 water_plan at 1:20,000 (the stream is only a few mm wide here)
# Smell: the species whose flowering months common/plants.py holds (pla_months, sourced there); the other sources
# have no season data in the repo and get no month bar
P16_SMELL_SPECIES = {"reeds": "reed", "lavender": "lavender"}
P16_STRIP_TOP = 10.5                         # mm: the strip's top below its cell's top (title, then the bridge ruler)
P16_STRIP_H = 62.0                           # mm: every strip's height (1,240 m across at 1:20,000; the cell is 76)
P16_PHOTO_DIR = os.path.join(DATA_DIR, "heritage_photos")   # the run kit's photo folder (p.21's contract)
P16_PHOTO_CSV = "photos.csv"
P16_PHOTO_W, P16_PHOTO_H = 22.0, 16.5        # mm: one History photo at most (4:3, cropped to fill)
# History photos: own site photos by file name (no credit, D13) first, else a photos.csv row whose place or file
# name holds an alias. v29 (Aras 30 Oct "ok to use kermes photos"): Kermes takes the DHA photo. T4 (G12): no credit
# lines on the sheet; the csv's credit lines go to the Sources page (p23).
P16_PLACES = (
    dict(key="hamam", cap=(u"Tabaklar Hamamı",), own=(u"tabaklar_hamami_1.jpg", u"tabaklar_hamami_2.jpg"),
         alias=(u"tabaklarhamami",)),
    dict(key="tabakhane", cap=(u"Tabakhane",), own=(u"tabakhane_1.jpg",), alias=(u"tabakhane",),
         notalias=(u"koprusu",)),
    dict(key="k3", cap=(u"Tabak Köprüsü", u"Roman bridge · K3"), own=(u"tabak_koprusu_1.jpg", u"tabak_koprusu_2.jpg"),
         alias=(u"tabakkoprusu",)),
    dict(key="k5", cap=(u"Üç Kemer Köprüsü", u"Roman bridge · K5"), own=(), alias=(u"uckemer",)),
    dict(key="tunnels", cap=(u"Kızıl Avlu", u"tunnels"), own=(), alias=(u"tunnel",)),
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


def sn_rich(pg, x, y, runs, pt, colour):
    """one line of [(text, bold)] runs (G5: the bold keywords inside a line); its width, mm"""
    size = sn_mm(pt)
    w0 = x
    for t, b in runs:
        pg.text(t, x, y, size, colour, bold=b)
        x += text_w(t, size, b)
    return x - w0


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
         "streams": list(C.streams or []), "study": [ring(list(A)) for A in (areas or {}).values()],
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


def _p16_bm_items(G, choice):
    """the basemap items of one panel: choice = (mode, override) of P16_BASEMAP (memoised by basemap_items)"""
    if not G.get("bm"):
        return []
    mode, ov = choice if choice else ("base", None)
    try:
        return basemap_items(mode, ov, G["bm_box"], G["bm"], True, SN_SCALE)
    except Exception as ex:
        k = ("bm_err", mode, repr(ov))
        if k not in _P16_MEMO:
            _P16_MEMO[k] = 1
            G.setdefault("warn", []).append(u"senses sheet: basemap {} not drawn ({}: {})".format(
                mode, type(ex).__name__, ex))
        return []


def _p16_bm_draw(pg, items, T):
    """the basemap items through this page's calls (even-odd fills: buildings come split, one fill each); the
    stream through M5 (water_plan, P16_WATER_OPTS) when the script includes common/water.py"""
    def fill(rings, hx, a, nz):
        pg.poly(rings, fill=hx, alpha=a)

    def line(pts, hx, w, dash, a):
        pg.line(pts, hx, w, list(dash) if dash else None, cap=0 if dash else 1, alpha=a)
    basemap_draw(items, T, fill, line, None, P16_WATER_OPTS)


def _p16_bm_style(items):
    """T4 (H-A request): what a panel's basemap items draw, for the shared key, only the kinds present: water ("m5"
    or "fill"; read with basemap_water_rings, so the M5 stream counts), covered (hex, width, dash), street (hex),
    bld and her (fill hex, edge hex or None), study (True)"""
    out = {}
    if basemap_water_rings(items):
        out["water"] = "m5" if any(it[0] == "water" for it in items) else "fill"
    fills = set(it[2] for it in items if it[0] == "fill")
    for it in items:
        if it[0] == "line" and it[4]:
            if it[2] == R28_STUDY_LINE["colour"]:
                out["study"] = True
            elif it[2] in (BM_COL["water_edge"], BM_COL["water"]):
                out.setdefault("covered", (it[2], it[3], list(it[4])))
    for hx in (BM_FAINT["road"], BM_COL["road"]):
        if hx in fills:
            out["street"] = hx
            break
    bc = globals().get("BLD_COL") or {}
    for f_, e_ in ((BM_FAINT["bld_veryfaint"], BM_FAINT["road_line"]), (bc.get("fill"), bc.get("edge")),
                   (BM_FAINT["bld"], None), (BM_COL["bld"], None)):
        if f_ and f_ in fills:
            out["bld"] = (f_, e_)
            break
    for f_, e_ in (("F1E6E5", "CDAAAA"), (bc.get("her_fill"), bc.get("her_edge")), (BM_COL["her"], BM_COL["her_edge"])):
        if f_ and f_ in fills:                           # heritage buildings (basemap "plan_faint" tones first)
            out["her"] = (f_, e_)
            break
    return out


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


def sn_cell(pg, G, cx, top, title, choice=None):
    """one cell: its title, the strip frame (the widened analysis frame at 1:20,000, P16_STRIP_H tall), the shared
    M3 base of this panel (choice = (mode, override); the stream only from the base, by M5), the study area with
    the base (under the panel's own layer; drawn here from calisma_alan when the base has none) and the bridge
    ruler on the frame's top edge. Returns the cell (T, box, label room: labels sit on the drawing, off the stream
    line)."""
    V, fr = G["V"], G["fr"]
    sw, sh = (fr[2] - fr[0]) * SN_K, (fr[3] - fr[1]) * SN_K
    x0, y1 = cx, sn_y(top + P16_STRIP_TOP)
    box = (x0, y1 - sh, x0 + sw, y1)
    T = sn_T(V, box[0], box[1], fr[0], fr[1])
    size = sn_mm(SN_TS["panel"])
    yt = sn_y(top + 5.0)
    pg.text(title, cx, yt, size, SN_INK, bold=True)
    refp = [T(p) for p in G["ref"]]
    cell = {"x": cx, "top": top, "box": box, "T": T, "side": cx + SN_SIDE,
            "bounds": (box[0] + 0.6, box[1] + 0.6, box[2] - 0.6, box[3] - 0.6),
            "taken": [(cx, yt - size * 0.25, cx + text_w(title, size, True) + 1.0, yt + size * 0.8),
                      (cx + SN_SIDE - 2.0, sn_y(top + SN_CH), cx + SN_CW, sn_y(top))],
            "segs": list(zip(refp, refp[1:]))}
    items = _p16_bm_items(G, choice)
    cell["bm_style"] = bs = _p16_bm_style(items)
    pg.clip([rect(*box)])
    if items:
        _p16_bm_draw(pg, items, T)
    if not bs.get("study"):                              # the study area once, in R28_STUDY_LINE, with the base
        st = R28_STUDY_LINE
        for A in G["study"]:
            Q = [T(p) for p in A]
            if len(Q) >= 3:
                pg.line(Q + Q[:1], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
    pg.unclip()
    xs = {}
    for nm, xy in BRIDGES_K:                             # the ruler: a tick per bridge, its name above the frame
        x = T(xy)[0]
        if box[0] <= x <= box[2]:
            pg.line([(x, box[3]), (x, box[3] - 1.0)], SN_INK2, 0.2)
            xs[nm] = x
    labs = ([(u"K1·K2", (xs["K1"] + xs["K2"]) / 2.0)] if "K1" in xs and "K2" in xs else []) + \
        [(nm, xs[nm]) for nm in ("K3", "K4", "K5", "K6") if nm in xs]
    fs = sn_mm(SN_TS["small"])
    ruler = []
    for s, x in labs:
        w = text_w(s, fs)
        xl = min(max(x - w / 2.0, box[0]), box[2] - w)
        b = (xl - 0.3, box[3] + 0.6, xl + w + 0.3, box[3] + 1.0 + fs * 0.8)
        if any(lp_hit(b, t) for t in ruler):
            continue
        pg.text(s, xl, box[3] + 1.0, fs, SN_INK2)
        ruler.append(b)
    return cell


def sn_outline(pg, G, cell):
    """the frame's own hairline (T4: the study area is drawn with the base, sn_cell)"""
    pg.poly([rect(*cell["box"])], stroke=SN_FRAME, lw=0.15)


def sn_place(pg, cell, labs, warn):
    """G4 (common/label_place.py): each word round its place ON the strip (T4a: the widened frame has room), never
    on the stream line or a panel's own lines (cell["segs"]) or boxes (cell["taken"]), on a thin leader when off
    it; "more" = further places the same word points to. A word with no room is logged."""
    items = []
    for L_ in labs:
        size, b = sn_mm(L_.get("pt", SN_TS["label"])), L_.get("bold", True)
        items.append(dict(x=L_["at"][0], y=L_["at"][1], rank=L_.get("rank", 0),
                          wh=lambda f, s=L_["s"], size=size, b=b: (text_w(s, max(size * f, sn_mm(SN_TS["small"])), b),
                                                                   max(size * f, sn_mm(SN_TS["small"])) * 0.95)))
    got = place_labels_all(items, cell["taken"], cell["bounds"], cell.get("segs", ()),
                           sizes=(1.0, SN_TS["small"] / SN_TS["label"]))
    for i, L_ in enumerate(labs):
        if i not in got:
            if L_.get("rank", 0) == 0:
                warn.append(u"senses sheet: no room for the word '{}'".format(L_["s"]))
            continue
        bx, leader, f = got[i]
        size = max(sn_mm(L_.get("pt", SN_TS["label"])) * f, sn_mm(SN_TS["small"]))   # never under 7 pt
        pg.text(L_["s"], bx[0], bx[1] + size * 0.2, size, L_.get("col", SN_INK), bold=L_.get("bold", True))
        for k, a in enumerate([L_["at"]] + list(L_.get("more", ()))):
            if leader or k > 0:
                pg.line([a, lp_leader_end(bx, a)], SN_INK2, 0.15)
                pg.circle(a[0], a[1], 0.3, fill=SN_INK2)


def _p16_fig(pg, pose, x, y, h, colour, facing=1):
    """p.16's ONE figure point: the figure library's side view (common/figures.py fig_side; adult 1.70 m), h mm
    tall on this diagram (pictogram size, not to scale), feet at (x, y), one colour. "sit" = sit_chair."""
    k = h / 1.70
    _p16_shapes(pg, fig_side({"sit": "sit_chair"}.get(pose, pose), x, y, k, facing, ink=colour))


def sn_key_row(pg, x, y, word, pt=None):
    size = sn_mm(pt or SN_TS["label"])
    pg.text(word, x, y - size * 0.35, size, SN_INK)


def sn_key_title(pg, cell, s):
    """T4 (G1, one legend logic for all six): the key column starts level with its own strip's top edge, under a
    bold title; returns the y of its first row's middle"""
    fs = sn_mm(SN_TS["small"])
    yb = cell["box"][3] - fs * 0.8
    pg.text(s, cell["side"], yb, fs, SN_INK, bold=True)
    return yb - 3.6


def sn_key_foot(pg, G, cell):
    """T4 (G1: every plan its own scale bar and north arrow): the north arrow and the scale bar at the foot of the
    key column, level with its strip's bottom edge (rows above end 9 mm over it)"""
    sx, yb = cell["side"], cell["box"][1] + 2.4
    sn_north(pg, G["V"], sx + 3.0, yb + 1.4)
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
    st, bs = R28_STUDY_LINE, cell.get("bm_style", {})
    y = sn_key_title(pg, cell, u"Base map · all six strips")
    rows = [(R28_STUDY_NAME, "study"), (u"Selinos stream", "water"), (u"Hidden (covered) stream", "covered"),
            (u"Streets", "street"), (u"Buildings", "bld"), (u"Heritage buildings", "her"),
            (u"Bridge (ticks on top)", "bridge"), (u"Flow direction", "flow")]
    for word, kind in rows:
        if kind in ("water", "covered", "street", "bld", "her") and kind not in bs:
            continue                                     # the key lists only what the base drew
        if kind == "study" and not (bs.get("study") or G["study"]):
            continue
        if kind == "study":
            pg.line([(sx, y), (sx + 9.0, y)], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
        elif kind == "water":
            _p16_water_swatch(pg, sx, y, bs["water"])
        elif kind == "covered":
            pg.line([(sx, y), (sx + 9.0, y)], bs["covered"][0], bs["covered"][1], bs["covered"][2], cap=0)
        elif kind == "street":
            pg.poly([rect(sx, y - 0.7, sx + 9.0, y + 0.7)], fill=bs["street"])
        elif kind in ("bld", "her"):
            f_, e_ = bs[kind]
            pg.poly([rect(sx + 1.5, y - 1.0, sx + 7.5, y + 1.0)], fill=f_, stroke=e_, lw=0.18 if e_ else 0.1)
        elif kind == "bridge":
            pg.line([(sx + 4.5, y + 0.9), (sx + 4.5, y - 0.9)], SN_INK2, 0.2)
        else:                                            # the water's direction in every strip (left to right)
            pg.line([(sx, y), (sx + 7.6, y)], SN_WATER_MID, 0.35)
            pg.poly([[(sx + 9.0, y), (sx + 7.2, y + 0.8), (sx + 7.2, y - 0.8)]], fill=SN_WATER_MID)
        sn_key_row(pg, sx + 11.0, y, word)
        y -= P16_KEY_ROW
    return labs


def sn_north(pg, V, ax, ay):
    """north arrow (survey +Y turned with the strips), tip toward north, 'N' beside it"""
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    L = math.hypot(nu, nv) or 1.0
    nx_, ny_ = nu / L, nv / L
    tip = (ax + nx_ * 3.5, ay + ny_ * 3.5)
    pg.poly([[tip, (ax - ny_ * 1.6 - nx_ * 3.0, ay + nx_ * 1.6 - ny_ * 3.0), (ax - nx_ * 1.8, ay - ny_ * 1.8)]],
            fill=SN_DARK)
    pg.poly([[tip, (ax - nx_ * 1.8, ay - ny_ * 1.8), (ax + ny_ * 1.6 - nx_ * 3.0, ay - nx_ * 1.6 - ny_ * 3.0)]],
            fill="FFFFFF", stroke=SN_DARK, lw=0.15)
    pg.text(u"N", tip[0] + 1.2, tip[1] - 0.6, sn_mm(SN_TS["small"]), SN_DARK, bold=True)


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
            _p16_fig(pg, pose, x, y - 1.4, 2.8, SN_DARK)
            figs.append((x, y))
    pg.unclip()
    for p, mood, R, veins, pose in sorted(B, key=lambda e: -e[2]):
        x, y = T(p)
        if mood not in seen and sn_in((x, y, x, y), box):
            seen.add(mood)
            labs.append(dict(s=mood, at=(x, y), col=mix(sn_mood_col(SN_MOOD[mood]), SN_DARK, 0.45)))
    sx = cell["side"]                                    # key column: the feeling wheel, gathers / thins out, people
    y0 = sn_key_title(pg, cell, u"Mood")
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
    _p16_fig(pg, "walk", sx + 2.5, y3 - 1.4, 2.8, SN_DARK)        # the pictograms on the strip (G1)
    _p16_fig(pg, "sit", sx + 6.5, y3 - 1.4, 2.8, SN_DARK)
    sn_key_row(pg, sx + 11.0, y3, u"What people do there")
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
    y = sn_key_title(pg, cell, u"Sound sources")
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
    y = sn_key_title(pg, cell, u"Smell sources")
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
    _p16_fig(pg, pose, fx, fy, 5.2, colour)
    if key == "watch":                                   # the line of sight
        pg.line([(fx + 0.5, fy + 4.6), (fx + 5.0, fy + 3.9)], colour, 0.2, [0.6, 0.4], cap=0)
    size = sn_mm(SN_TS["label"])
    pg.text(word.upper(), x + 14.0, y - size * 0.35, size, mix(colour, SN_DARK, 0.3), bold=True)


def sn_exp_places(G):
    """where each way of meeting the water is strongest (the masterplan's places; design reading)"""
    hub = G["hub"]
    walk = [h["xy"] for h in G["hubs"] if h["role"] == "walking" and h["id"] != u"K6"]
    bk = dict(BRIDGES_K)
    pl = {"watch": ([G["terrace"]["xy"]] if G["terrace"] else []) + [z["q"] for z in G["zones_raw"] if z["code"] == "WT"],
          "walk": walk + [p for P in G["canopy"] for p in sn_along(P, 40.0)],
          "touch": [h["sub_xy"]["c"] for h in G["hubs"] if h.get("sub_xy")] + [G["bath"], G["kermes"]],
          "cross": [c_["xy"] for c_ in G["cross"]],
          "remember": [bk.get(k) for k in ("K3", "K4", "K5")] + [G["bath"], CRAFT_XY, ROMAN_WALL] +
          [hub[k]["xy"] for k in (u"İstiklal", u"Kızıl Avlu") if k in hub]}
    return dict((k, [p for p in v if p]) for k, v in pl.items())


def sn_encounters(pg, G, cell, warn):
    """v35 (round 2, Aras 31 Oct: "still overlapping", no overlapping lines left): five ribbons, one per way of
    meeting the water, each in its OWN lane along the stream (fixed offset, never pulled onto the stream line), so no
    two ribbons ever touch or cross. At its places (sn_exp_places) a ribbon swells inside its lane. Thickness is
    measured vertically and lanes are gap apart (> the widest swell), so the bands stay apart on slopes too; the
    entry and the fan to the vignette bubbles keep the lane order (no crossings). The v32 crossing clouds are gone.
    A design reading of the masterplan's places, never a measurement (no numbers)."""
    T, box = cell["T"], cell["box"]
    x0, y0, x1, y1 = box
    step = 0.5
    xs, ys = sn_spine_y([T(p) for p in G["ref"]], x0, x1, step)
    if ys is None:
        ys = [(y0 + y1) / 2.0] * len(xs)
        warn.append(u"senses sheet: no stream line in the strip: the encounter ribbons run along its middle")
    n = len(ys)                                          # a calmer path: 15 mm moving mean
    ys = [sum(ys[max(0, i - 15):i + 16]) / len(ys[max(0, i - 15):i + 16]) for i in range(n)]
    m = len(SN_EXP)
    gap, sig, w0, w1, lead = 4.0, 2.6, 0.8, 1.6, 18.0   # mm: lane pitch (> w0 + w1), swell, width, swell, entry
    half = gap * (m - 1) / 2.0 + (w0 + w1) / 2.0 + 1.0   # the bundle stays whole inside the frame
    ys = [min(max(y, y0 + half), y1 - half) for y in ys]
    pl = sn_exp_places(G)
    PX = [[x for x in (T(p)[0] for p in pl.get(key, [])) if x0 - 3.0 <= x <= x1 + 3.0] for key, _w, _c, _p in SN_EXP]
    sx, ytop = cell["side"], box[3]
    pitch = 8.8                                          # mm: the vignettes' pitch
    for i, (key, word, colour, pose) in enumerate(SN_EXP):
        px = PX[i]
        off = ((m - 1) / 2.0 - i) * gap                  # lane i: watch on top, remember at the bottom
        ys0 = y1 - 5.0 - i * (y1 - y0 - 10.0) / max(1, m - 1)    # where it enters at the strip's left edge
        C_, W_ = [], []
        for x, yb in zip(xs, ys):
            b = max([math.exp(-((x - q) / sig) ** 2) for q in px] or [0.0])
            y_ = yb + off                                # v35: its own lane everywhere (no pull)
            t = min(1.0, (x - x0) / lead)
            t = t * t * (3.0 - 2.0 * t)                  # smoothstep: from its entry into its lane
            C_.append((x, ys0 + (y_ - ys0) * t))
            W_.append((0.25 + (w0 - 0.25) * t) + w1 * b)
        bx, by = sx + 11.0, ytop - 8.4 - pitch * i
        ex, ey = C_[-1]
        fan = [sn_bez((ex, ey), (ex + 6.0, ey), (bx - 6.0, by), (bx, by), k_ / 24.0) for k_ in range(1, 25)]
        P = C_ + fan
        Wl = W_ + [W_[-1] + (w0 - W_[-1]) * k_ / 24.0 for k_ in range(1, 25)]
        L_ = [(p[0], p[1] + w / 2.0) for p, w in zip(P, Wl)]    # v35: vertical thickness (lanes never meet)
        R_ = [(p[0], p[1] - w / 2.0) for p, w in zip(P, Wl)]
        pg.poly([L_ + R_[::-1]], fill=colour, alpha=0.85)
        Cs = C_[::6] + C_[-1:]
        cell["segs"].extend(zip(Cs, Cs[1:]))
        sn_bubble(pg, bx, by, key, word, colour, pose, i)
    y = ytop - 8.4 - pitch * (m - 1) - 4.0 - 4.2         # key row: the swell (G1)
    sw = [(sx + 9.0 * t / 30.0, w0 + w1 * math.exp(-((t / 30.0 - 0.5) / 0.16) ** 2)) for t in range(31)]
    pg.poly([[(x, y + w / 2.0) for x, w in sw] + [(x, y - w / 2.0) for x, w in sw][::-1]], fill=SN_INK2, alpha=0.72)
    sn_key_row(pg, sx + 11.0, y, u"Wider: where it happens")
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
    """a numbered marker (G3: its number explained by the photo caption of the same number)"""
    fs = sn_mm(SN_TS["small"])
    pg.circle(x, y, 1.3, fill=colour, stroke="FFFFFF", lw=0.2)
    pg.text(u"{}".format(n_), x, y - fs * 0.36, fs, "FFFFFF", bold=True, align="C")


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
    ka = G["hub"].get(u"Kızıl Avlu")                     # the Red Hall tunnels: the covered reach under it (H2)
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
    for k, s in (("hamam", u"Tabaklar Hamamı"), ("tabakhane", u"Tabakhane"), ("tunnels", u"Kızıl Avlu tunnels"),
                 ("kermes", u"Kermes")):                 # v29: Kermes keeps its word when it has no photo
        if k in anchors and k not in ph:
            labs.append(dict(s=s, at=anchors[k], col=txt))
    fs = sn_mm(SN_TS["small"])
    lh = fs * 1.2
    capm = 0.8 + 2.0 * lh                                # two caption lines under each photo
    avoid = [(a, 50.0) for a in anchors.values()] + [(p, 1.0) for p in (T(q) for q in G["ref"])] + \
        [(p, 1.0) for A in G["study"] for p in (T(q) for q in A)]
    slots, W, H = _p16_photo_row(with_ph, box, avoid, capm)
    marks = []
    for n_, (k, a) in enumerate(sorted(with_ph, key=lambda e: slots[e[0]][0]), 1):
        x, y = slots[k]
        path = ph[k][0]                                  # ph[k][1] = the csv credit line: Sources page only (G12)
        cap = names[k]
        lines = wrap(cap[0], fs, W - 3.2, True)[:2]
        nb = len(lines)                                  # the name's lines are bold, a second caption line is not
        if nb == 1 and len(cap) > 1:
            lines.append(cap[1])
        yb = y - 0.8 - fs * 0.8
        sn_num(pg, x + 1.3, yb + fs * 0.36, n_, txt)
        for j, s in enumerate(lines):
            pg.text(s, x + 3.2, yb - j * lh, fs, txt if j < nb else SN_INK2, bold=(j < nb))
        m_ = (a[0], a[1])                                # its place on the map, the same number
        while any(math.hypot(m_[0] - q[0], m_[1] - q[1]) < 2.7 for q in marks):
            m_ = (m_[0], m_[1] + 2.7)                    # two places close together: stacked, a short tie
        if m_ != (a[0], a[1]):
            pg.line([a, (m_[0], m_[1] - 1.3)], SN_INK2, 0.15)
        sn_num(pg, m_[0], m_[1], n_, txt)
        marks.append(m_)
        cell["taken"] += [(x, y - capm, x + W, y + H), (m_[0] - 1.4, m_[1] - 1.4, m_[0] + 1.4, m_[1] + 1.4)]
        G.setdefault("imgs", []).append((path, (x, y, W, H)))
    sx = cell["side"]                                    # key column: the heritage field, the numbered places
    y = sn_key_title(pg, cell, u"Heritage")
    sn_layers_round(pg, sx + 4.5, y, 2.3, SN_HER, 40)
    sn_key_row(pg, sx + 11.0, y, u"Heritage place")
    if with_ph:
        y -= P16_KEY_ROW + 0.6
        sn_num(pg, sx + 4.5, y, 1, txt)
        sn_key_row(pg, sx + 11.0, y, u"Place of the photo")
        sn_key_row(pg, sx + 11.0, y - 3.4, u"with the same number")
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
    press by build_all (a failure is only a warning there). basemap = {panel title: (mode, override)} changes
    P16_BASEMAP's choice (D5) for this run."""
    t0 = time.time()
    _P16_MEMO.clear()                                    # photos are read once a run
    bm = dict(P16_BASEMAP)
    bm.update(basemap or {})
    G = sn_data(C, areas, warn)
    G["warn"] = warn
    pg = Page(SN_PW, SN_PH)
    pg.poly([rect(0.0, 0.0, SN_PW, SN_PH)], fill="FFFFFF")
    pg.text(SN_KICKER, SN_ML, sn_y(12.0), sn_mm(SN_TS["kicker"]), SN_ACC, bold=True)   # the booklet's header band
    pg.text(SN_TITLE, SN_ML, sn_y(22.0), sn_mm(SN_TS["title"]), SN_INK, bold=True)
    pg.line([(SN_ML, sn_y(25.0)), (SN_PW - SN_ML, sn_y(25.0))], SN_RULE, 0.25 * SN_PT)
    sn_rich(pg, SN_ML, sn_y(30.5), [(u"The fade-out zones and the ", False), (u"senses", True),
                                    (u" along the Selinos stream: six maps on ", False), (u"one base map", True),
                                    (u" · every strip ", False), (u"1:20,000", True)], SN_TS["statement"], SN_INK)
    cells = [(SN_COLX[0], SN_ROWS[0], u"Zones", sn_zones),
             (SN_COLX[1], SN_ROWS[0], u"Feeling", sn_feeling),
             (SN_COLX[0], SN_ROWS[1], u"Sound", sn_sound),
             (SN_COLX[1], SN_ROWS[1], u"Smell", sn_smell),
             (SN_COLX[0], SN_ROWS[2], u"Encounters", sn_encounters),
             (SN_COLX[1], SN_ROWS[2], u"History", sn_history)]
    for cx, top, title, layer in cells:
        cell = sn_cell(pg, G, cx, top, title, bm.get(title))
        labs, n0 = [], len(pg.items)
        try:
            labs = layer(pg, G, cell, warn) or []
        except Exception as ex:
            import traceback
            warn.append(u"senses sheet: panel {} not drawn ({}: {})".format(title, type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
            open_ = sum(1 if it[0] == "clip" else -1 if it[0] == "unclip" else 0 for it in pg.items[n0:])
            for _ in range(max(0, open_)):               # close a clip the failed panel left open
                pg.unclip()
        sn_outline(pg, G, cell)
        sn_key_foot(pg, G, cell)
        sn_place(pg, cell, labs, warn)
    if callable(globals().get("basemap_warnings")):
        warn.extend(basemap_warnings())                  # e.g. the M5 stream fell back to the plain fill
    imgs = G.get("imgs") or []
    path = _p16_save(pg, folder, SN_NAME, SN_TITLE, imgs) if imgs else save(pg, folder, SN_NAME, SN_TITLE)
    files.append(path)
    return u"{}  {}  {:.1f} s (zones: {})".format(os.path.basename(path), datetime.datetime.now().strftime("%H:%M:%S"),
                                                  time.time() - t0, G["fields_src"])
