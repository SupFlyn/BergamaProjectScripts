# p.16 the senses and the water: senses_sheet and its sn_* helpers (split from parts/02e_r28_detail.py, parts/02f_r28_senses.py on 29 Oct 2026; moved unchanged)


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


def sn_T(V, x0, y0):
    """survey m -> page mm of a strip whose frame's lower-left corner is (x0, y0): the corridor's View (site_alan
    turned so the water runs left to right, the north-east bank on top) at 1:20,000"""
    c_, s_, cx, cy, u0, v0 = V.c, V.s, V.cx, V.cy, V.u0, V.v0

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
    cut = dict((r_[1], r_[2]) for r_ in globals().get("CUT_AT", ()) if len(r_) > 2)   # the water board's cuts
    V = C.V
    up = cut.get(u"UPSTREAM ENTRY") or V.xy(V.u0 + 0.07 * (V.u1 - V.u0), (V.v0 + V.v1) / 2.0)
    dn = cut.get(u"DOWNSTREAM REACH") or V.xy(V.u0 + 0.77 * (V.u1 - V.u0), (V.v0 + V.v1) / 2.0)
    bk = dict(BRIDGES_K)
    hub = G["hub"]
    G["stops"] = [(u"Upstream entry", up, True), (u"K4", bk.get("K4"), False), (u"K3", bk.get("K3"), False),
                  (u"İstiklal Meydanı", hub[u"İstiklal"]["xy"] if u"İstiklal" in hub else None, True),
                  (u"K5", bk.get("K5"), False), (u"Downstream", dn, True)]
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
def sn_cell(pg, G, cx, top, title, under=None):
    """one cell: its title, the strip frame (the whole analysis frame at 1:20,000), the spine (bed, stream lines,
    hidden stream) and the bridge ruler on the frame's top edge. Returns the cell (T, box, label room)."""
    V = G["V"]
    sw, sh = (V.u1 - V.u0) * SN_K, (V.v1 - V.v0) * SN_K
    x0, y1 = cx, sn_y(top + SN_TOP)
    box = (x0, y1 - sh, x0 + sw, y1)
    T = sn_T(V, box[0], box[1])
    size = sn_mm(SN_TS["panel"])
    yt = sn_y(top + 5.0)
    pg.text(title, cx, yt, size, SN_INK, bold=True)
    cell = {"x": cx, "top": top, "box": box, "T": T, "side": cx + SN_SIDE,
            "bounds": (cx, sn_y(top + SN_CH), cx + SN_SIDE - 3.0, sn_y(top + 0.5)),
            "taken": [(cx, yt - size * 0.25, cx + text_w(title, size, True) + 1.0, yt + size * 0.8), box,
                      (cx + SN_SIDE - 2.0, sn_y(top + SN_CH), cx + SN_CW, sn_y(top))]}
    pg.clip([rect(*box)])
    if under:
        under(pg, G, cell)
    Ps = [[T(p) for p in L_] for L_ in G["bed"]]
    if Ps:
        pg.poly(Ps, fill=SN_WATER, alpha=0.55)
    for P in G["streams"]:
        pg.line([T(p) for p in P], SN_WATER_MID, 0.1, alpha=0.6)
    for P in G["covered"]:
        pg.line([T(p) for p in P], SN_WATER_MID, 0.4, [1.0, 0.6], cap=0, alpha=0.75)
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
    for s, x in labs:
        w = text_w(s, fs)
        xl = min(max(x - w / 2.0, box[0]), box[2] - w)
        b = (xl - 0.3, box[3] + 0.6, xl + w + 0.3, box[3] + 1.0 + fs * 0.8)
        if any(lp_hit(b, t) for t in cell["taken"][3:]):
            continue
        pg.text(s, xl, box[3] + 1.0, fs, SN_INK2)
        cell["taken"].append(b)
    return cell


def sn_outline(pg, G, cell):
    """G8: the study area (calisma_alan, both parts) in R28_STUDY_LINE, then the frame's own hairline"""
    st, T, box = R28_STUDY_LINE, cell["T"], cell["box"]
    pg.clip([rect(*box)])
    for A in G["study"]:
        Q = [T(p) for p in A]
        if len(Q) >= 3:
            pg.line(Q + Q[:1], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
    pg.unclip()
    pg.poly([rect(*box)], stroke=SN_FRAME, lw=0.15)


def sn_place(pg, cell, labs, warn):
    """G4 (common/label_place.py): each word round its place, outside the strip (its box is taken), on a thin
    leader when off it; "more" = further places the same word points to. A word with no room is logged."""
    items = []
    for L_ in labs:
        size, b = sn_mm(L_.get("pt", SN_TS["label"])), L_.get("bold", True)
        items.append(dict(x=L_["at"][0], y=L_["at"][1], rank=L_.get("rank", 0),
                          wh=lambda f, s=L_["s"], size=size, b=b: (text_w(s, size * f, b), size * f * 0.95)))
    got = place_labels_all(items, cell["taken"], cell["bounds"], (), sizes=(1.0, SN_TS["small"] / SN_TS["label"]))
    for i, L_ in enumerate(labs):
        if i not in got:
            warn.append(u"senses sheet: no room for the word '{}'".format(L_["s"]))
            continue
        bx, leader, f = got[i]
        size = sn_mm(L_.get("pt", SN_TS["label"])) * f
        pg.text(L_["s"], bx[0], bx[1] + size * 0.2, size, L_.get("col", SN_INK), bold=L_.get("bold", True))
        for k, a in enumerate([L_["at"]] + list(L_.get("more", ()))):
            if leader or k > 0:
                pg.line([a, lp_leader_end(bx, a)], SN_INK2, 0.15)
                pg.circle(a[0], a[1], 0.3, fill=SN_INK2)


def sn_figure(pg, pose, x, y, h, colour, facing=1):
    """a figure of common/figures.py, h mm tall, feet at (x, y): filled outlines, one colour, no stroke"""
    f = h / 1.75
    for Q in fig_polys(pose, 1.75, facing):
        pg.poly([[(x + px * f, y + py * f) for px, py in Q]], fill=colour)


def sn_key_row(pg, x, y, word, pt=None):
    size = sn_mm(pt or SN_TS["label"])
    pg.text(word, x, y - size * 0.35, size, SN_INK)


# ---------------------------------------------------------------- Zones: the base map (p24_ref2 fade-out fields)
def sn_field(pg, rings, colour, core=0.42, halo=(1.3, 0.9, 0.5), ha=0.12):
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


def sn_zones_under(pg, G, cell):
    """the faint survey base under the zones: the survey buildings as the plans read them, light"""
    T, box = cell["T"], cell["box"]
    Ps = [Q for Q in ([T(p) for p in P] for P in G["bld"]) if len(Q) >= 3 and sn_in(bbox(Q), box)]
    if Ps:
        pg.poly(Ps, fill=COL["bld"], alpha=0.6)


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
        at = inner_pt(max(Ps, key=lambda Q: abs(area2(Q))))
        labs.append(dict(s=SN_ZONE_SHORT.get(key, name), at=at, col=mix(hx, SN_DARK, 0.5)))
    pg.unclip()
    sx, top = cell["side"], cell["top"]                  # key column: the spine's legend, north, scale bar
    st = R28_STUDY_LINE
    y = sn_y(top + 4.0)
    rows = [(R28_STUDY_NAME, "study"), (u"Stream · bed", "bed"), (u"Hidden stream", "hidden"), (u"Bridge", "bridge"),
            (u"Buildings · survey", "bld"), (u"Water flow", "flow")]
    for word, kind in rows:
        if kind == "study":
            pg.line([(sx, y), (sx + 9.0, y)], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
        elif kind == "bed":
            pg.poly([rect(sx, y - 0.9, sx + 9.0, y + 0.9)], fill=SN_WATER, alpha=0.55)
            pg.line([(sx, y), (sx + 9.0, y)], SN_WATER_MID, 0.1, alpha=0.6)
        elif kind == "hidden":
            pg.line([(sx, y), (sx + 9.0, y)], SN_WATER_MID, 0.4, [1.0, 0.6], cap=0, alpha=0.75)
        elif kind == "bridge":
            pg.line([(sx + 4.5, y + 0.9), (sx + 4.5, y - 0.9)], SN_INK2, 0.2)
        elif kind == "bld":
            pg.poly([rect(sx, y - 0.9, sx + 9.0, y + 0.9)], fill=COL["bld"], alpha=0.6)
        else:                                            # the water's direction in every strip (left to right)
            pg.line([(sx, y), (sx + 7.6, y)], SN_WATER_MID, 0.35)
            pg.poly([[(sx + 9.0, y), (sx + 7.2, y + 0.8), (sx + 7.2, y - 0.8)]], fill=SN_WATER_MID)
        sn_key_row(pg, sx + 11.0, y, word)
        y -= 4.6
    sn_north(pg, G["V"], sx + 4.0, sn_y(top + 46.0))
    sn_scale_bar(pg, sx, sn_y(top + 62.0), (0.0, 100.0, 250.0, 500.0))
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
    """the strips' scale bar (m, G13), numbers at 7 pt, the scale beside it"""
    for i, (a, b) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * SN_K, y, x + b * SN_K, y + 1.2)], fill=SN_DARK if i % 2 == 0 else "FFFFFF",
                stroke=SN_DARK, lw=0.15)
    fs = sn_mm(SN_TS["small"])
    for m_ in marks:
        pg.text(u"{:,.0f}{}".format(m_, u" m" if m_ == marks[-1] else u""), x + m_ * SN_K, y + 2.2, fs, SN_INK,
                align="C")
    pg.text(u"1:{:,.0f}".format(SN_SCALE), x + marks[-1] * SN_K + 5.0, y - 0.1, sn_mm(SN_TS["label"]), SN_DARK,
            bold=True)


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
                         0.22, 36)], fill=colour, alpha=0.08)
    dark = mix(colour, SN_DARK, 0.35)
    for j in range(veins):
        a = rnd.uniform(0.0, 2.0 * math.pi)
        L = R * rnd.uniform(0.9, 1.55)
        ph = rnd.uniform(0.0, 6.0)
        pts = [(x + math.cos(a + 0.35 * math.sin(t * 3.0 + ph) * t) * L * t,
                y + math.sin(a + 0.35 * math.sin(t * 3.0 + ph) * t) * L * t) for t in [k / 8.0 for k in range(9)]]
        for seg, w in ((pts[:4], 0.28), (pts[3:7], 0.17), (pts[6:], 0.09)):
            pg.line(seg, dark, w, alpha=0.6)
    if dots:
        for k in range(int(R * 9)):
            a, d = rnd.uniform(0.0, 2.0 * math.pi), R * 1.15 * rnd.random() ** 0.8
            pg.circle(x + math.cos(a) * d, y + math.sin(a) * d, 0.11, fill=SN_DARK, alpha=0.45)


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
            sn_figure(pg, pose, x, y - 1.4, 2.8, SN_DARK)
            figs.append((x, y))
    pg.unclip()
    for p, mood, R, veins, pose in sorted(B, key=lambda e: -e[2]):
        x, y = T(p)
        if mood not in seen and sn_in((x, y, x, y), box):
            seen.add(mood)
            labs.append(dict(s=mood, at=(x, y), col=mix(sn_mood_col(SN_MOOD[mood]), SN_DARK, 0.45)))
    sx, top = cell["side"], cell["top"]                  # key column: the feeling wheel, gathers / thins out
    cx, cy, r = sx + 23.0, sn_y(top + 22.0), 8.5
    for i in range(72):
        a0, a1 = math.radians(5.0 * i), math.radians(5.0 * (i + 1))
        pg.line([(cx + r * math.cos(a0 + (a1 - a0) * t / 3.0), cy + r * math.sin(a0 + (a1 - a0) * t / 3.0))
                 for t in range(4)], sn_mood_col(5.0 * i + 2.5), 1.5, cap=0, alpha=0.85)
    fs = sn_mm(SN_TS["small"])
    pg.text(u"active", cx, cy + r + 1.6, fs, SN_INK, align="C")
    pg.text(u"passive", cx, cy - r - 1.6 - fs * 0.75, fs, SN_INK, align="C")
    pg.text(u"positive", cx + r + 1.8, cy - fs * 0.35, fs, SN_INK)
    pg.text(u"negative", cx - r - 1.8, cy - fs * 0.35, fs, SN_INK, align="R")
    y1, y2 = sn_y(top + 44.0), sn_y(top + 58.0)
    sn_blot(pg, sx + 5.0, y1, 3.0, sn_mood_col(SN_MOOD["lively"]), 6, 5)
    sn_key_row(pg, sx + 12.0, y1, u"Gathers")
    sn_blot(pg, sx + 5.0, y2, 3.6, sn_mood_col(SN_MOOD["calm"]), 0, 6)
    sn_key_row(pg, sx + 12.0, y2, u"Thins out")
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
    for z in G["zones_raw"]:                             # reeds: the reed basins and the reed side arms
        if z["code"] == "WT":
            sn_cluster(pg, "reeds", T(z["q"]), 2.2, 7, col["reeds"], rnd, 0.25)
    for a in G["arms"]:
        for p in sn_along(a["P"], 1.6 / SN_K):
            sn_cluster(pg, "reeds", T(p), 0.8, 2, col["reeds"], rnd, 0.25)
    for p in sn_spaced(G["forest"], T, 3.5):             # birds: the forest corridor and the wetland
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
    sx, y = cell["side"], sn_y(cell["top"] + 5.0)        # key column: the playful key
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
def sn_smell(pg, G, cell, warn):
    T, box = cell["T"], cell["box"]
    col = dict((k, c) for k, _, c in SN_SMELL)
    S, dg = [], []                                       # (key, survey xy, rings, first radius mm, step mm)
    for z in G["zones_raw"]:
        c = z["code"]
        if c == "WT":
            S.append(("reeds", z["q"], 5, 0.9, 0.7))
        elif c == "WA" and z["tier"] == "W":             # the bed band B: reeds, cattail, water mint (p.16)
            S.append(("mint", z["q"], 4, 0.7, 0.55))
        elif c == "WS":                                  # the terraces' dry band F (French lavender, rosemary)
            S.append(("lavender", z["q"], 5, 0.9, 0.7))
        elif c == "DG":                                  # herbs and greens (card i01)
            S.append(("demeter", sn_vcent(z["P"]), 5, 0.9, 0.75))
            dg += z["P"]
        if c in ("GR", "DG"):                            # the plan's café places
            S.append(("cafe", z["q"], 3, 0.6, 0.55))
    for p in sn_spaced([a["at"] for a in G["arms"]], T, 6.0):
        S.append(("reeds", p, 4, 0.7, 0.6))
    mids = [P[len(P) // 2] for P in G["terr"] if P]
    for p in sn_spaced(mids, T, 8.0)[:4]:
        S.append(("lavender", p, 4, 0.7, 0.6))
    if dg:                                               # olives in Demeter's Garden (card i01), harvested in Nov
        S.append(("olive", sn_vcent(dg), 6, 2.0, 1.1))
    pg.clip([rect(*box)])
    dots = []
    for i, (key, p, n, r0, dr) in enumerate(S):
        x, y = T(p)
        if not sn_in((x, y, x, y), box, r0 + n * dr):
            continue
        for k in range(n):
            Q = sn_ring(x, y, r0 + k * dr, 101 + i, 0.06 + 0.03 * k, 56)
            pg.line(Q + Q[:1], col[key], 0.16, alpha=0.9 - 0.55 * k / max(1.0, n - 1.0))
        dots.append((x, y, col[key]))
    for x, y, c in dots:
        pg.circle(x, y, 0.6, fill=c)
    pg.unclip()
    sx, y = cell["side"], sn_y(cell["top"] + 5.0)        # key column
    for key, word, c in SN_SMELL:
        for r in (1.1, 1.8):
            Q = sn_ring(sx + 2.4, y, r, 3, 0.08, 36)
            pg.line(Q + Q[:1], c, 0.16, alpha=0.8)
        pg.circle(sx + 2.4, y, 0.6, fill=c)
        sn_key_row(pg, sx + 7.0, y, word)
        y -= 6.0
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


def sn_rrect(x0, y0, x1, y1, r, n=6):
    out = []
    for cx, cy, a0 in ((x1 - r, y1 - r, 0.0), (x0 + r, y1 - r, 90.0), (x0 + r, y0 + r, 180.0), (x1 - r, y0 + r, 270.0)):
        for i in range(n + 1):
            a = math.radians(a0 + 90.0 * i / n)
            out.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return out


def sn_wave(pg, x0, x1, y, colour, lw=0.3):
    pg.line([(x0 + (x1 - x0) * i / 16.0, y + 0.25 * math.sin(i * math.pi / 2.0)) for i in range(17)], colour, lw)


def sn_bubble(pg, x, y, key, word, colour, pose):
    """a vignette at a ribbon's end: an organic bubble, a figure of common/figures.py and one word"""
    w, h = 34.0, 11.0
    pg.poly([sn_rrect(x, y - h / 2.0, x + w, y + h / 2.0, 4.0)], fill="FFFFFF", stroke=colour, lw=0.35)
    fx, fy = x + 6.5, y - h / 2.0 + 1.8
    if key == "remember":                                # under a Roman arch
        pg.line([(fx + 3.4 + 2.6 * math.cos(math.radians(a)), fy + 2.6 * math.sin(math.radians(a)))
                 for a in range(0, 181, 15)], colour, 0.45, alpha=0.55)
    if key in ("touch", "cross"):
        sn_wave(pg, fx - 3.5, fx + 4.5, fy + (0.9 if key == "cross" else 0.0), SN_WATER_MID)
    else:
        pg.line([(fx - 3.5, fy), (fx + 6.5, fy)], SN_INK2, 0.2)
    sn_figure(pg, pose, fx, fy, 7.0, colour)
    if key == "watch":                                   # the line of sight
        pg.line([(fx + 0.6, fy + 6.2), (fx + 5.6, fy + 5.4)], colour, 0.2, [0.6, 0.4], cap=0)
    size = sn_mm(SN_TS["label"])
    pg.text(word, x + 14.0, y - size * 0.35, size, mix(colour, SN_DARK, 0.3), bold=True)


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
    T, box = cell["T"], cell["box"]
    x0, y0, x1, y1 = box
    xs, ys = sn_spine_y([T(p) for p in G["ref"]], x0, x1, 0.5)
    if ys is None:
        ys = [(y0 + y1) / 2.0] * len(xs)
        warn.append(u"senses sheet: no stream line in the strip: the ribbons run along its middle")
    pl = sn_exp_places(G)
    sig, A, lam = 2.6, 3.0, 30.0                         # graphic: swell width, braid amplitude and length, mm
    top = cell["top"]
    for i, (key, word, colour, pose) in enumerate(SN_EXP):
        px = [x for x in (T(p)[0] for p in pl.get(key, [])) if x0 - 3.0 <= x <= x1 + 3.0]
        C_, W_ = [], []
        for x, yb in zip(xs, ys):
            b = max([math.exp(-((x - q) / sig) ** 2) for q in px] or [0.0])
            w = 0.45 + 1.9 * b
            o = A * math.sin(2.0 * math.pi * (x - x0) / lam + 2.0 * math.pi * i / 5.0) * (1.0 - 0.8 * b)
            f = min(1.0, max(0.0, (x - (x1 - 18.0)) / 18.0))
            f = f * f * (3.0 - 2.0 * f)                  # into its exit lane (watch on top) before the end
            yc = yb + o * (1.0 - f) + (2 - i) * 2.2 * f
            C_.append((x, min(max(yc, y0 + 1.0 + w / 2.0), y1 - 1.0 - w / 2.0)))
            W_.append(w)
        bx, by = cell["side"] + 11.0, sn_y(top + 8.0 + 14.5 * i)
        ex, ey = C_[-1]
        fan = [sn_bez((ex, ey), (ex + 7.0, ey), (bx - 7.0, by), (bx, by), t / 24.0) for t in range(1, 25)]
        P = C_ + fan
        Wl = W_ + [W_[-1] + (1.3 - W_[-1]) * t / 24.0 for t in range(1, 25)]
        N = sn_normals(P)
        pg.poly([[(p[0] + n_[0] * w / 2.0, p[1] + n_[1] * w / 2.0) for p, n_, w in zip(P, N, Wl)] +
                 [(p[0] - n_[0] * w / 2.0, p[1] - n_[1] * w / 2.0) for p, n_, w in zip(P, N, Wl)][::-1]],
                fill=colour, alpha=0.78)
        sn_bubble(pg, bx, by, key, word, colour, pose)
    labs, first = [], None
    for h in G["hubs"]:                                  # hatched clouds: high water closes the bed sub-hubs
        s_ = h.get("sub_xy")
        if s_:
            x, y = T(s_["c"])
            if sn_in((x, y, x, y), box):
                pg.poly([sn_ring(x, y, 1.9, 77, 0.22, 40, (3, 5))], stripes=(SN_INK2, 0.45, 0.12, 0.0), alpha=0.8)
                first = first or (x, y)
    for name, xy, named in G["stops"]:                   # the stops of the water's journey
        q = sn_on_ref(G, xy)
        if q is None:
            continue
        x, y = T(q)
        if x0 <= x <= x1:
            pg.circle(x, y, 0.75, fill="FFFFFF", stroke=SN_INK, lw=0.25)
            if named:                                    # the bridges are named by the ruler
                labs.append(dict(s=name, at=(x, y)))
    if first:
        labs.append(dict(s=u"Floods", at=first, bold=False, col=SN_INK2))
    return labs


# ---------------------------------------------------------------- History (senses_ref2: layered fade fields)
def sn_layers_round(pg, x, y, R, colour, seed, n=6, a=0.1):
    for k in range(n):
        pg.poly([sn_ring(x, y, R * (1.0 - k / float(n)), seed, 0.12, 40, (2, 3))], fill=colour, alpha=a)
    return (x, y)


def sn_layers_band(pg, P, W, colour, n=6, a=0.1):
    """layers along a page polyline, each narrower and shorter: darkest at the core"""
    s = arclen(P)
    L = s[-1]
    for k in range(n):
        cut = L * 0.22 * k / float(n)
        Q = sn_band(sub_line(P, s, cut, L - cut) if L > 2.0 * cut + 0.2 else P, W * (1.0 - k / float(n)), 0.35)
        if len(Q) >= 3:
            pg.poly([Q], fill=colour, alpha=a)
    return at_len(P, s, L / 2.0)[0]


def sn_history(pg, G, cell, warn):
    T, box = cell["T"], cell["box"]
    txt = COL["accent_dark"]
    labs = []

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
        labs.append(dict(s=u"Red Hall tunnels", at=at, col=txt))
    bk = dict(BRIDGES_K)
    rb = []
    for i, k in enumerate(("K3", "K5")):                 # the Roman bridges (h01 §5 P08, P09; K4 "Roman?", P06)
        if bk.get(k):
            x, y = T(bk[k])
            rb.append(sn_layers_round(pg, x, y, 2.3, SN_HER, 40 + i))
    if rb:
        labs.append(dict(s=u"Roman bridges", at=rb[0], more=rb[1:], col=txt))
    if G["bath"]:                                        # Tabaklar Hamamı (H4)
        x, y = T(G["bath"])
        labs.append(dict(s=u"Tabaklar Hamamı", at=sn_layers_round(pg, x, y, 2.0, SN_HER, 50), col=txt))
    labs.append(dict(s=u"Tannery quarter", at=field(CRAFT_XY, 70.0, 1.8, 60), col=txt))   # Tabakhane (H3)
    if G["kermes"]:                                      # Kermes in the dry bed (h01 §2.8), at the S4 cut
        labs.append(dict(s=u"Kermes", at=field(G["kermes"], 90.0, 1.8, 70), col=txt))
    pg.unclip()
    sx, top = cell["side"], cell["top"]                  # key column: how the page is read (G5)
    sn_rich(pg, sx, sn_y(top + 62.0), [(u"Places", True), (u": the masterplan's data", False)], SN_TS["label"],
            SN_INK2)
    sn_rich(pg, sx, sn_y(top + 66.5), [(u"Intensities", True), (u": design readings", False)], SN_TS["label"],
            SN_INK2)
    return labs


# ---------------------------------------------------------------- the sheet
def senses_sheet(C, areas, folder, files, warn):
    """S1: writes Bergama_senses_A3.pdf into the masterplan's output folder (the masterplan's own PDF writer, Arial
    embedded); returns the log line. Called once a press by build_all (a failure is only a warning there)."""
    t0 = time.time()
    G = sn_data(C, areas, warn)
    pg = Page(SN_PW, SN_PH)
    pg.poly([rect(0.0, 0.0, SN_PW, SN_PH)], fill="FFFFFF")
    pg.text(SN_KICKER, SN_ML, sn_y(12.0), sn_mm(SN_TS["kicker"]), SN_ACC, bold=True)   # the booklet's header band
    pg.text(SN_TITLE, SN_ML, sn_y(22.0), sn_mm(SN_TS["title"]), SN_INK, bold=True)
    pg.line([(SN_ML, sn_y(25.0)), (SN_PW - SN_ML, sn_y(25.0))], SN_RULE, 0.25 * SN_PT)
    sn_rich(pg, SN_ML, sn_y(30.5), [(u"The fade-out zones and the ", False), (u"senses", True),
                                    (u" · every strip ", False), (u"1:20,000", True)], SN_TS["statement"], SN_INK)
    cells = [(SN_COLX[0], SN_ROWS[0], u"Zones", sn_zones, sn_zones_under),
             (SN_COLX[1], SN_ROWS[0], u"Feeling", sn_feeling, None),
             (SN_COLX[0], SN_ROWS[1], u"Sound", sn_sound, None),
             (SN_COLX[1], SN_ROWS[1], u"Smell", sn_smell, None),
             (SN_COLX[0], SN_ROWS[2], u"Encounters", sn_encounters, None),
             (SN_COLX[1], SN_ROWS[2], u"History", sn_history, None)]
    for cx, top, title, layer, under in cells:
        cell = sn_cell(pg, G, cx, top, title, under)
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
        sn_place(pg, cell, labs, warn)
    path = save(pg, folder, SN_NAME, SN_TITLE)
    files.append(path)
    return u"{}  {}  {:.1f} s (zones: {})".format(os.path.basename(path), datetime.datetime.now().strftime("%H:%M:%S"),
                                                  time.time() - t0, G["fields_src"])
