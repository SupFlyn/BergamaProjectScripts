# ============================================================ v44 (Aras 27 Oct 11:07; revision_2026-10-27/PHASE2_SPEC.md)
# Booklet pages 5-8 of the site board (v45: the stream edge plan is draw_edge_build, 15e; v46: the proposal map,
# the commercial spines and the heritage loop are redrawn at the theme's one scale in 15f): the movement page's key
# streets, the masterplan's proposal map, the commercial spines (restored from v19-v32.1), the city heritage loop,
# the walking-effort proof (Tobler) and the building types under the cuts. Sizes are set from the booklet page: a
# drawing w board units wide fills the booklet's panel width BK_AW mm, so 1 booklet mm = w / BK_AW board units and a
# text height for a given point size follows from it (bk_hk). Labels are placed with measured widths and a collision
# test (place_labels); a label with no free spot becomes a number with a key line under the map.
BK_STD = (100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000, 25000, 50000, 100000)   # = bergama_booklet STD_SCALES
BK_GAP_MM = 6.0         # mm on the booklet page between two map pieces / a map and its analysis column
MV_KEY_N = 5            # key streets named on "walking / driving today": the top 5 named streets (50 m+) by potential
CROSS_HALF = 20.0       # m: a masterplan crossing joins the walking network as a line this far to each side of its
#                         point, across the stream (a network join for the engine, never drawn)
TOBLER_CLS = (1.1, 1.25, 1.5, 2.0)    # walking time / flat-ground time: class limits of the walking-effort map


def bk_std(den):
    """The first round booklet scale at or above den (bergama_booklet std_scale)."""
    return next((d for d in BK_STD if d >= den - 0.5), den)


def bk_s(cw, ch, den=None, share=1.0, hshare=1.0):
    """v44: the factor the booklet prints a crop cw x ch board units with (bergama_booklet panel_page): the largest that
    fits its share of the panel area's width and height; a drawing at a scale (den = its sheet scale) takes the round
    scale at or below it."""
    mm = 1000.0 / PDF_SCALE
    s = min(BK_AW * share / max(1e-9, cw * mm), BK_AH * hshare / max(1e-9, ch * mm))
    return den / bk_std(den / s) if den else s


def bk_hk(pt, k, mono=False):
    """v44: the text height (capital, board units) that prints at pt points on the booklet page, k = board units per
    booklet mm (the writer's font size = height / capital ratio, _PDF_CAP 0.718)."""
    return pt * 25.4 / 72.0 * 0.718 * k                  # v50 (G2): body text is Arial too (mono was Courier, 0.571)


def bk_h(pt, s, mono=False):
    """v44: bk_hk for a crop printed at factor s (1 sheet mm -> s booklet mm; 10 board units per sheet mm)."""
    return bk_hk(pt, PDF_SCALE / 1000.0 / max(1e-9, s), mono)


# ------------------------------------------------------------ clipping a drawing to a rectangle of the page
def clip_rect_poly(P, r):
    """A closed polygon cut to the rectangle r = (x0, y0, x1, y1) (Sutherland-Hodgman, clip_half per side)."""
    for px, py, nx, ny in ((r[0], 0.0, -1.0, 0.0), (r[2], 0.0, 1.0, 0.0), (0.0, r[1], 0.0, -1.0), (0.0, r[3], 0.0, 1.0)):
        if len(P) < 3:
            return []
        P = clip_half(P, px, py, nx, ny)
    return P if len(P) >= 3 else []


def clip_rect_line(P, r):
    """A polyline cut to the rectangle r: the runs inside (Liang-Barsky per segment)."""
    runs, cur = [], []
    for a, b in zip(P[:-1], P[1:]):
        t0, t1 = 0.0, 1.0
        dx, dy = b[0] - a[0], b[1] - a[1]
        ok = True
        for p_, q_ in ((-dx, a[0] - r[0]), (dx, r[2] - a[0]), (-dy, a[1] - r[1]), (dy, r[3] - a[1])):
            if abs(p_) < 1e-12:
                if q_ < 0:
                    ok = False
                    break
                continue
            t = q_ / p_
            if p_ < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                ok = False
                break
        if not ok:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        pa, pb = (a[0] + dx * t0, a[1] + dy * t0), (a[0] + dx * t1, a[1] + dy * t1)
        if cur and t0 <= 0.0:
            cur.append(pb)
        else:
            if len(cur) >= 2:
                runs.append(cur)
            cur = [pa, pb]
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


class ClipB(object):
    """v44: a Board seen through a rectangle of the page: fills, hatches and lines are cut to it, words outside it
    left out; everything else goes to the Board as it is."""

    def __init__(self, B, r):
        self.B, self.r = B, r

    def __getattr__(self, k):
        return getattr(self.B, k)

    def fill(self, polys, color, layer, order):
        self.B.fill([clip_rect_poly(list(P), self.r) for P in polys if P], color, layer, order)

    def hatch(self, polys, color, layer, order, spacing, ang=math.radians(45.0), w=0.03):
        self.B.hatch([clip_rect_poly(list(P), self.r) for P in polys if P], color, layer, order, spacing, ang, w)

    def line(self, P, color, layer, order, w=0.13):
        for run in clip_rect_line(list(P), self.r):
            self.B.line(run, color, layer, order, w)

    def text(self, txt, x, y, h, *a, **kw):
        if self.r[0] <= x <= self.r[2] and self.r[1] <= y <= self.r[3]:
            self.B.text(txt, x, y, h, *a, **kw)


# ------------------------------------------------------------ labels without overlaps
def _hit(b, taken):
    return any(b[0] < q[2] and q[0] < b[2] and b[1] < q[3] and q[1] < b[3] for q in taken)


def place_labels(B, labels, taken, L, bounds=None, order=66):
    """v44: labels [(lines, px, py, h, colour)] (lines: one or more short lines, the first bold) beside their points,
    each box measured (tw, sans) and tested against every box in taken and the labels placed before; first the eight
    spots round the point, then the same three times farther out on a thin leader. A label with no free spot is a
    number at its point; returns the key [(number, lines)] for the lines under the map. taken grows."""
    key = []
    for lines, px, py, h, col in labels:
        lines = [l_ for l_ in lines if l_]
        if not lines:
            continue
        lead = 1.45 * h
        w_ = max(tw(l_, h, "sans") for l_ in lines)
        hb = h + (len(lines) - 1) * lead
        spot = None
        for far in (1.0, 3.0):
            d = 0.7 * h * far
            for ox, oy in ((d, -0.5 * hb), (-d - w_, -0.5 * hb), (-0.5 * w_, d), (-0.5 * w_, -hb - d),
                           (d, d * 0.6), (-d - w_, d * 0.6), (d, -hb - d * 0.6), (-d - w_, -hb - d * 0.6)):
                b = (px + ox - 0.15 * h, py + oy - 0.15 * h, px + ox + w_ + 0.15 * h, py + oy + hb + 0.15 * h)
                if bounds and not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
                    continue
                if not _hit(b, taken):
                    spot = (ox, oy, b, far)
                    break
            if spot:
                break
        if spot is None:                                  # a number at the point, the words in the key
            n = len(key) + 1
            t_ = str(n)
            b = (px - 0.1 * h, py - 0.5 * h, px + tw(t_, h, "sans") + 0.1 * h, py + 0.5 * h)
            B.text(t_, px, py - 0.5 * h, h, col, L, order=order, font=FONT_TITLE, bold=True)
            taken.append(b)
            key.append((n, lines))
            continue
        ox, oy, b, far = spot
        taken.append(b)
        if far > 1.0:                                     # the leader from the point to the nearer side of the box
            tx = px + ox if ox > 0 else px + ox + w_
            B.line([(px, py), (tx, py + oy + 0.5 * hb)], col, L, order - 1, 0.06)
        yl = py + oy + hb - h
        for j, l_ in enumerate(lines):
            B.text(l_, px + ox, yl - j * lead, h, col, L, order=order, font=FONT_TITLE, bold=(j == 0))
    return key


def draw_label_key(B, key, x, y, w, h, L):
    """v44: the numbered labels that found no place on the map, as lines under it; returns the y below."""
    for n, lines in key:
        B.fit(u"{} · {}".format(n, u" · ".join(lines)), x, y - h, h, w, INK, L, font=FONT_TITLE)
        y -= 1.5 * h
    return y


def sub_frame(F, ua, ub, va=None, vb=None):
    """v44: the part of frame F between local u = ua..ub (and v = va..vb), on F's own axes."""
    va = F.v0 if va is None else va
    vb = F.v1 if vb is None else vb
    return Frame([F.world(ua, va), F.world(ub, va), F.world(ub, vb), F.world(ua, vb)])


# ------------------------------------------------------------ p.5 photo captions
# v44 (Aras: "a short keyword caption under each photo"): keywords taken from each photo's description in the data
# pack (library/site_photos/site_photos_index.csv, Nil 2026-10-01), nothing added; the historic bridge is named by
# photo_caption where the description shows a bridge and a K bridge lies within 60 m of the viewpoint.
PHOTO_KEYS = {"IMG_5779": u"low drop · algae · stone wall",          # "shallow water falling over a low ... drop, green algae"
              "IMG_5802": u"channel · stone walls · 3-4 storeys",    # "Channel ... rubble-stone walls; 3-4 storey buildings"
              "IMG_5815": u"overgrown bank · new wall, railing",     # "Overgrown bank ... new rubble-stone wall with railing"
              "IMG_5785": u"dry bank · litter · railing",            # "Dry bank ground with shrubs and litter; railing"
              "IMG_5794": u"arch over water · plane tree",           # "large arch over water ...; plane tree"
              "IMG_5833": u"sumac · pine",                           # "Same bridge closer, with sumac and pine"
              "IMG_5774": u"road · stone wall, steps · pines",       # "asphalt road ... rubble-stone wall with steps, umbrella pines"
              "IMG_5752": u"road · railing on parapet · houses"}     # "Asphalt road ... railing on a low stone parapet; houses"
ROMAN_K = ("K3", "K4", "K5")   # Roman bridges, 2nd-3rd c. (PHASE2_SPEC §3 H1; h01 §5 P06, P08, P09)


def photo_caption(it):
    """v44: a photo's keyword caption: the historic bridge it shows (description says bridge, K bridge within 60 m)
    then its keywords (PHOTO_KEYS, else the description's first clause, cut to 30 characters)."""
    d = it.get("description", "") or ""
    stem = (it.get("file", "") or "").split(".")[0]
    kw = PHOTO_KEYS.get(stem) or d.split(";")[0].split(":")[0].strip().rstrip(".")[:30]
    if "bridge" in d.lower():
        near = min(((math.hypot(bx - it["x"], by - it["y"]), kk) for kk, nm, bx, by in BRIDGES_K), default=None)
        if near and near[0] <= 60.0:
            kw = u"{} {} · {}".format(u"Roman bridge" if near[1] in ROMAN_K else u"bridge", near[1], kw)
    return kw


# ------------------------------------------------------------ p.6 walking / driving today: the key streets only
def mv_key_rows(MV, key, n=MV_KEY_N):
    """v44: the n named streets (50 m+ in the frame) with the highest potential `key` today (the engine's own street
    table), highest first."""
    return [r for r in sorted(MV.get("big") or [], key=lambda r: -r[key]) if r[key] > 0][:n]


def draw_mv_key(S, B, V, R, MV, key, F, L, h, bounds):
    """v44: one network map with only its key streets in colour (index of the street, SEQ ramp) and named; every other
    street piece thin grey. Returns the names drawn."""
    rows = mv_key_rows(MV, key)
    val_of = dict((r["name"], r[key]) for r in rows)
    pieces = R["pieces"]
    net = "car_b" if key.startswith("car") else "walk_b"

    def val(pi):
        p = pieces[pi]
        nm = (p["tags"].get("name") or "").strip()
        return (MV_CLASS.get(p["tags"].get("highway"), "lane"), nm if nm in val_of else "")
    runs = _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F)
    grey = mix(INK2, PAPER, 0.55)
    best = {}
    for P, (cls, nm) in runs:
        if not nm:
            B.line(V.P(P), grey, L, 14, MV_W[cls] * 0.3)
            continue
        B.line(V.P(P), mv_ramp(SEQ, seq_t(val_of[nm], 100.0)), L, 16, MV_W[cls] * 0.6 + 0.35)
        if nm not in best or pl_length(P) > pl_length(best[nm]):
            best[nm] = P
    labels = []
    for r in rows:
        P = best.get(r["name"])
        if P:
            q, t = pl_point_at(P, pl_length(P) / 2.0)
            px, py = V.p(q[0], q[1])
            labels.append(([u"{} · {:.0f}".format(r["name"], r[key])], px, py, h, INK))
    key_ = place_labels(B, labels, [], L, bounds=bounds)
    return [r["name"] for r in rows], key_


# ------------------------------------------------------------ p.6 the proposal (masterplan_results.json "movement")
MP_CHANGE = {"relocated": (u"relocated", MARK_C), "calmed": (u"calmed", (214, 130, 40)),
             "pedestrian": (u"pedestrian", PROP_C), "shared": (u"shared", (120, 90, 160)),
             "kept": (u"kept", mix(INK2, PAPER, 0.3))}
HUB_C = {"transit": MARK_C, "walking": PROP_C}
TRANSIT_C = (52, 92, 160)


def mp_movement():
    """v44 (PHASE2_SPEC §4): the masterplan's proposal for movement (roads, truck route, crossings, hubs, routes), from
    masterplan_results.json key "movement"; None (logged) without the file or the key."""
    try:
        with open(MP_RESULTS_FILE, "r", encoding="utf-8") as fh:
            M = json.load(fh).get("movement")
    except Exception:
        LOG.append("Proposal map: no masterplan_results.json ({}), so not drawn.".format(MP_RESULTS_FILE))
        return None
    if not isinstance(M, dict):
        LOG.append("Proposal map: masterplan_results.json has no \"movement\" key yet, so not drawn.")
        return None
    return M


def _xy_list(v):
    try:
        return [(float(p[0]), float(p[1])) for p in (v or [])]
    except Exception:
        return []


def _xy1(v):
    try:
        return (float(v[0]), float(v[1]))
    except Exception:
        return None


def mv_with_masterplan(S, M):
    """v44: the movement engine run with the masterplan's proposal (once per run, S.mv_mp): cars off the roads it makes
    pedestrian or relocates, each crossing joined to the walking network across the stream, the hub squares as new
    everyday destinations (as the city link stops are in the board's own proposal run). None without OSM."""
    if getattr(S, "mv_mp", None) is not None:
        return S.mv_mp or None
    S.mv_mp = {}
    osm = getattr(S, "osm", None)
    if not osm:
        return None
    closed = [_xy_list(r.get("xy")) for r in M.get("roads") or [] if r.get("change") in ("pedestrian", "relocated")]
    closed = [P for P in closed if len(P) >= 2]
    props = []
    for c in M.get("crossings") or []:
        p = _xy1(c.get("xy"))
        nrm = stream_normal(S, p[0], p[1]) if p else None
        if p and nrm:
            props.append(("bridge", [(p[0] - nrm[0] * CROSS_HALF, p[1] - nrm[1] * CROSS_HALF),
                                     (p[0] + nrm[0] * CROSS_HALF, p[1] + nrm[1] * CROSS_HALF)], False))
    attr = [p for p in (_xy1(h.get("xy")) for h in M.get("hubs") or []) if p]
    t0, log = time.time(), []
    try:
        ns = dict(globals())
        ns["build_corridors"] = lambda S_: None              # the board has built its spines already
        S.mv_mp = dict(R=analyse(ns, S, osm, PLACES_PATH or None, props, closed, attr, MV_OPT, log))
    except Exception:
        LOG.append("WARNING: movement with the masterplan's proposal failed:\n" + traceback.format_exc())
        return None
    LOG.append("Movement with the masterplan's proposal ({:.0f} s; {} roads closed to cars, {} crossings, {} hubs): "
               .format(time.time() - t0, len(closed), len(props), len(attr)) + " ".join(l_ for l_ in log if l_))
    return S.mv_mp


def mv_line_index(R, P, key, d=12.0):
    """v44: the length-weighted mean index `key` of the street pieces inside the frame whose middle lies within d m
    of the line P; None when none does."""
    pieces, xy, IDX = R["pieces"], R["xy"], R["IDX"][key]
    s_, l_ = 0.0, 0.0
    for i in R["inside"]:
        p = pieces[i]
        if p["prop"]:
            continue
        m = ((xy[p["a"]][0] + xy[p["b"]][0]) / 2.0, (xy[p["a"]][1] + xy[p["b"]][1]) / 2.0)
        if pl_dist(m[0], m[1], P, False) <= d:
            s_ += IDX.get(i, 0.0) * p["L"]
            l_ += p["L"]
    return s_ / l_ if l_ > 0 else None


# ------------------------------------------------------------ p.6 the city heritage loop (spec §3 D6)
# Places in survey coordinates and where each comes from. Lat/lon -> survey with h01 §0's formula (anchor K3, ±10-30 m).
HER_LOOP = [  # (key, name, (x, y), source)
    ("gondola", u"Gondola · to the Acropolis", (30720.4, 32370.1), "h03 Q3: valley station 39.1255343, 27.1891834"),
    ("redhall", u"Red Hall", (30203.92, 31974.82), "survey label 'Kızıl Avlu' (REF_LABELS)"),
    ("K3", u"K3 · Tabakhane", (30037.01, 32121.57), "BRIDGES_K"),
    ("K4", u"K4 · Ulu Cami 1398-99", (29846.40, 32277.71), "BRIDGES_K; Ulu Cami h01 §5 P05"),
    ("bazaar", u"Bazaar · Hacı Hekim · arasta", (29926.0, 31855.0), "h01 §5 P23 (hamam, calc)"),
    ("museum", u"Bergama Museum", (29560.0, 31358.0), "h01 §5 P24"),
]
HER_DOTS = [(u"Ulu Cami", (29844.17, 32313.30)),          # survey label 'Ulu Camii' (REF_LABELS)
            (u"Tabaklar Hamamı", (29890.4, 32243.6)),      # h01 §5 P07, survey 'Hamam'
            (u"Çizmeciler Arastası", (29794.31, 31929.85))]   # survey label (REF_LABELS)
HER_OFF = [(u"Acropolis · Trajaneum", "gondola", (30209.0, 33177.0)),   # h03 Q3: OSM centroid 39.1327803, 27.1832652
           (u"Asklepieion", "museum", (29077.3, 31867.3))]             # h03 Q3: ticket building 39.1210181, 27.1701577


# ------------------------------------------------------------ proof (D11/D12): walking effort, Tobler
def draw_walking_effort(S, B, x, y, w, U):
    """v44 (proof of "Tobler walking effort"): every walkable street piece of the movement engine in the frame and
    its ring, coloured by how much longer it takes to walk than on flat ground in its slower direction (Tobler 1993,
    tobler_factor, on the survey terrain: the walking cost the movement maps use); the share of the network length
    in each class. Returns the y below (unchanged without the terrain)."""
    L = "LU_BOARD::WalkingEffort"
    MV = movement(S)
    R = MV.get("R")
    pieces = R["pieces"] if R else None
    z = getattr(pieces, "z", None) if pieces is not None else None
    if not z:
        LOG.append("Walking effort: no survey terrain heights on the street network, so not drawn.")
        return y
    F = S.F
    F2 = context_frame(F)
    xy = R["xy"]
    B.text("WALKING EFFORT · TIME ON FOOT AGAINST FLAT GROUND", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    V, mw, mh = view_fit(F2, x, y - 1.2 * U, w, 10.0 * w)
    s_b = bk_s(mw, mh * 1.5, crop_scale(V.s))
    h7, h9 = bk_h(7.5, s_b), bk_h(9.0, s_b)
    B.fill([V.P(F2.P)], mix(PAPER, (255, 255, 255), 0.55), L, 1)
    mini_base(S, B, V, L, water_col=mix(CAT["water"][1], PAPER, 0.3))
    mini_buildings(S, B, V, L, lambda u: mix(INK2, PAPER, 0.72), order=12)
    cols = [mv_ramp(SEQ, t_) for t_ in (0.05, 0.3, 0.55, 0.8, 1.0)]
    lens = [0.0] * 5
    for p in pieces:
        if not p["walk"] or p["prop"] or p["a"] not in z or p["b"] not in z or p["L"] < 0.5:
            continue
        a, b = xy[p["a"]], xy[p["b"]]
        if not F2.inside(0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1])):
            continue
        za, zb = z[p["a"]], z[p["b"]]
        if za is None or zb is None:
            continue
        g = (zb - za) / p["L"]
        f = max(tobler_factor(g), tobler_factor(-g))      # the slower direction (uphill)
        c = sum(1 for t_ in TOBLER_CLS if f >= t_)
        lens[c] += p["L"]
        for run in F2.clip_line([a, b]):
            B.line(V.P(run), cols[c], L, 14 + c, MV_W[MV_CLASS.get(p["tags"].get("highway"), "lane")] * 0.7)
    B.line(V.P(F.P + [F.P[0]]), INK, L, 26, 0.2)
    draw_map_annotations(S, B, V, U)
    draw_north_small(B, V, mw, mh, U, L, size=0.7)
    mb = y - 1.2 * U - mh
    draw_scalebar(B, V.X0, mb - 1.4 * U, V.s, nice_floor(F2.w / 8.0), U, L, h=h7 / U)
    tot = sum(lens) or 1.0
    names = [u"flat · under x{:.2f}".format(TOBLER_CLS[0])] + [
        u"x{:.2f}-{:.2f}".format(a_, b_) for a_, b_ in zip(TOBLER_CLS[:-1], TOBLER_CLS[1:])] + [
        u"steep · x{:.1f} and more".format(TOBLER_CLS[-1])]
    leg = [("thick", cols[i], u"{} · {:.0f}% of the network".format(names[i], 100.0 * lens[i] / tot)) for i in range(5)]
    yy = mb - 2.4 * U
    B.text(u"walking time on the street piece / on flat ground, slower direction " + bcite(
        "Walking effort: Tobler (1993) hiking function, speed = 6 exp(-3.5 |g + 0.05|) km/h on the grade g of each OSM "
        "street piece between the survey terrain heights of its ends (grades capped at ±0.5); the same cost as the "
        "movement maps' walking routes. Shares of the walkable network length in the frame and its ring."),
        V.X0, yy, h7, INK2, L, font=FONT_TITLE)
    ly = draw_legend_items(B, leg, V.X0, yy - 1.4 * h7 - 0.4 * U, mw, U, L, h=h7 / U)
    crop_panel("walking_effort", V.X0, mb - 1.6 * U, V.X0 + mw, y - 1.2 * U, u"Walking effort · Tobler slope cost",
               crop_scale(V.s), crop_legend(leg))
    return ly - 0.4 * U
