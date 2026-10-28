# ---- MIRAQUA round 28 Oct 2026 (site board v50): p.20 the heritage loop (worker SB-heritage). Shared pieces: parts/15h_r28_shared.py,
# common/r28_style.py, common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v50 (MIRAQUA 28 Oct, P20.1-P20.3, D2, F13; replaces v46/v49.1's draw_heritage_loop in 15f and HER_LOOP / HER_OFF in
# 15d): THE HERITAGE LOOP on the survey, not on the site frame. D2 (asked 28 Oct, default B until Aras answers) is the
# switch HER_EXTENT:
#   "loop"   ONE map at 1:10,000, north up, holding every stop the survey covers, the whole-file survey (S.whole, plan
#            01's model) as quiet context with the study area inside it, the stops numbered in loop order and one short
#            text each under the map (crop drw_heritage_loop); beside it a key map of the survey's whole drawn bulk with
#            the loop map's extent and the study area (NEW crop drw_heritage_key, no scale: a key map). North up, not on
#            the frame axis: both fit the page, but on the frame axis the leg to the Acropolis would run ~80 mm along the
#            map's top edge; north up it leaves the map ~23 mm from the gondola station.
#   "survey" the survey's whole drawn bulk at 1:20,000 with the loop core (K3-K4, Red Hall, Ulu Cami) at 1:5,000 beside
#            it, keyed to it by its frame, each with its own scale bar, the list under the inset (one crop
#            drw_heritage_loop; no key crop).
# The Acropolis is the one destination the survey does not cover (3dm_checks §3: nearest survey line 259 m): an arrow at
# the map's edge with its straight distance, no long line. The legs are soft lines stop to stop (no dashes), the stream
# walk K3-K4 a broad soft band along the stream's centre line (the spine). Names English · Turkish with their real
# letters (G3, F13), texts from public online sources only (F5, HER_SRC), keywords bold (G5), names on the maps placed
# by the shared label_place (G4), base tones as b_base but lighter where they are only context (G6).
HER_EXTENT = "loop"     # D2: "loop" (B, default) or "survey" (A: whole survey 1:20,000 + loop-core inset 1:5,000)
HER_DEN, HER_SV_DEN, HER_IN_DEN = 10000, 20000, 5000      # the loop map, the whole survey, the inset (booklet page)
HER_SB_M = {10000: 400.0, 20000: 1000.0, 5000: 200.0}     # m: the scale bar under each map (four parts)
HER_MAP_BK_W, HER_MAP_BK_H = 226.0, 140.0  # mm: the loop map on the booklet page (crop 227 mm: grid columns 1-7)
HER_KEY_BK_W = 160.0    # mm: the key map (crop 161 mm: grid columns 8-12; at most 190): 227 + 4 + 161 = 392 mm
HER_GUT_MM = 5.0        # mm between the two drawings on the sheet (booklet gutter 4 + the crops' 0.5 mm edges)
HER_GAP_MM = 6.0        # mm: between the list's columns, and between the survey map and its inset column (BK_GAP_MM)
HER_SV_MAX_MM = (270.0, 205.0)   # mm: the most the whole-survey map may take ("survey"), the inset column beside it
HER_IN_BK_H = 100.0     # mm: the inset's height ("survey")
HER_MARGIN_M = 150.0    # m: at least this much survey round the outermost places of the loop map
HER_SNAP_M = 30.0       # m: K3 and K4 lie this close to the stream's centre line, else the walk is drawn straight
HER_CORE = ("redhall", "K3", "K4")             # + Ulu Cami: the loop core of the inset ("survey")
HER_PT = dict(list=9.0, lab=7.5, dot=7.0)     # booklet pt: stop texts (body minimum), stop names, heritage places
HER_PITCH, HER_LEAD = 1.75, 1.4               # line pitch of the stop texts / of a map name, x the capital height
HER_ACC = C(dict((k_, h_) for k_, n_, h_ in R28_MARKERS)["heritage"])     # R28 "heritage and views" (= MARK_C)
HER_ROAD = mix(MPL["road"], WHITE, 0.4)       # G6: street surfaces and edges lighter than b_base's (context only)
HER_ROAD_EDGE = mix(MPL["road_edge"], WHITE, 0.45)
HER_GREEN_T = 0.45                            # mapped parks, woods and fields this far to white; no satellite cover

# The loop in its order (P20.2): key, name (English · Turkish, G3), survey m, one short text (P20.3; ** = bold, G5).
# Places: bridges BRIDGES_K; survey labels Kızıl Avlu, Ulu Camii, Hamam, Çizmeciler Arastası (REF_LABELS); lat/lon of
# OpenStreetMap / Visit İzmir -> survey m by the linear fit anchored at K3 (±10-30 m), as v44. Facts: HER_SRC.
HER_STOPS = [
    dict(key="gondola", name=u"Gondola · Teleferik", xy=(30720.4, 32370.1),          # OSM node 2295928011
         txt=u"valley station of the **cable car** (2010) up to the **Acropolis** (Akropol), the Hellenistic city on "
             u"the hill"),
    dict(key="redhall", name=u"Red Hall · Kızıl Avlu", xy=(30203.92, 31974.82),      # survey label 'Kızıl Avlu'
         txt=u"Hadrian's **temple**, 2nd c. AD, built **over the stream**: the Selinos runs under it in twin Roman "
             u"tunnels"),
    dict(key="K3", name=u"K3 · Tabakhane Köprüsü", xy=(30037.01, 32121.57),         # BRIDGES_K
         txt=u"**Roman bridge** of the 2nd-3rd c., named after the old tanneries; the **stream walk** starts here"),
    dict(key="K4", name=u"K4 · Ulucami Önü Köprüsü", xy=(29846.40, 32277.71),       # BRIDGES_K
         txt=u"the bridge before **Ulu Cami** (1398-99, Bayezid I) and **Tabaklar Hamamı**, the tanners' bath; the "
             u"loop crosses here"),
    dict(key="bazaar", name=u"Bazaar · Arasta", xy=(29926.0, 31855.0),               # Hacı Hekim hamam (Visit İzmir)
         txt=u"Hacı Hekim mosque, **arasta** and hamam of 1513, in the old **bazaar** with Çizmeciler Arastası"),
    dict(key="museum", name=u"Bergama Museum · Bergama Müzesi", xy=(29560.0, 31358.0),   # as v44
         txt=u"museum of **1936**: finds from the **excavations** of Pergamon, and the town's carpets"),
    dict(key="asklepieion", name=u"Asklepieion · Asklepion", xy=(29077.3, 31867.3),  # OSM ticket building
         txt=u"the **healing sanctuary** of Asclepius, 4th c. BC, rebuilt under Hadrian, reached by a sacred way, "
             u"the Via Tecta"),
]
HER_WALK = dict(frm="K3", to="K4", name=u"Stream walk K3-K4",                       # the loop's spine
                txt=u"**{:,.0f} m** along the **Selinos** (Bergama Çayı) from the **Roman bridge** K3 to the "
                    u"Ulucami Önü bridge K4: the spine of the loop")   # v50: K4's date unsure (h01 §5 P06)
HER_BEYOND = [dict(key="acropolis", frm="gondola", name=u"Acropolis · Akropol",    # Trajaneum, OSM way 1410335587;
                   xy=(30209.0, 33177.0))]                                         # off the survey drawing (259 m)
HER_DOTS = [(u"Ulu Cami", (29844.17, 32313.30)),          # survey label 'Ulu Camii'
            (u"Tabaklar Hamamı", (29890.4, 32243.6)),      # survey 'Hamam'
            (u"Çizmeciler Arastası", (29794.31, 31929.85))]   # survey label
HER_SRC = (u"Heritage loop, the places and their dates (public sources): Wikipedia 'Pergamon' (Acropolis, Trajaneum, "
           u"Asklepieion, Via Tecta) and 'Bergama Acropolis Gondola'; UNESCO World Heritage List 1457 and its ICOMOS "
           u"evaluation (2014, whc.unesco.org/document/152724: the Roman tunnels under Kızıl Avlu); Wikipedia 'Red "
           u"Basilica'; Kültür Envanteri (kulturenvanteri.com) 'Kızıl Avlu', 'Tabak Köprüsü', 'Bergama Müzesi'; Visit "
           u"İzmir (visitizmir.org) 'Bergama Ulu (Yıldırım) Mosque' and 'Mevlâna Hacı Hekim Hammam'; KTB İzmir 'Baths "
           u"(Hamams) in İzmir' (Tabaklar Hamamı, named after the tanneries); KTB Türkiye Müzeleri (turkishmuseums.com) "
           u"'The Archaeological Site of Asklepion'; Wikipedia 'Bergama Museum'. Positions: bridges and survey labels on "
           u"the survey drawing; the gondola's valley station, the Trajaneum and the Asklepieion's ticket building from "
           u"OpenStreetMap, lat/lon to survey metres by a linear fit at K3 (±10-30 m). Distances straight between "
           u"places, the stream walk along the stream's centre line; calculated.")

# Arial (= Helvetica) advance widths, 1000 units per em (as DIAG_SRC's text_w): words set run by run (G5) are placed
# at their printed widths
HER_MCH = u' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ\xa0¡¢£¤¥¦§¨©ª«¬\xad®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĞğİıŞş'
HER_MW0 = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584, 556, 222, 556, 333, 1000, 556, 556, 333, 1000, 667, 333, 1000, 611, 222, 222, 333, 333, 350, 556, 1000, 333, 1000, 500, 333, 944, 500, 667, 278, 333, 556, 556, 556, 556, 260, 556, 333, 737, 370, 556, 584, 333, 737, 552, 400, 549, 333, 333, 333, 576, 537, 333, 333, 333, 365, 556, 834, 834, 834, 611, 667, 667, 667, 667, 667, 667, 1000, 722, 667, 667, 667, 667, 278, 278, 278, 278, 722, 722, 778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722, 667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 500, 556, 556, 556, 556, 278, 278, 278, 278, 556, 556, 556, 556, 556, 556, 556, 549, 611, 556, 556, 556, 556, 500, 556, 500, 778, 556, 278, 278, 667, 500]
HER_MW1 = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556, 333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584, 556, 278, 556, 500, 1000, 556, 556, 333, 1000, 667, 333, 1000, 611, 278, 278, 500, 500, 350, 556, 1000, 333, 1000, 556, 333, 944, 500, 667, 278, 333, 556, 556, 556, 556, 280, 556, 333, 737, 370, 556, 584, 333, 737, 552, 400, 549, 333, 333, 333, 576, 556, 333, 333, 333, 365, 556, 834, 834, 834, 611, 722, 722, 722, 722, 722, 722, 1000, 722, 667, 667, 667, 667, 278, 278, 278, 278, 722, 722, 778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722, 667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 556, 556, 556, 556, 556, 278, 278, 278, 278, 611, 611, 611, 611, 611, 611, 611, 549, 611, 611, 611, 611, 611, 556, 611, 556, 778, 611, 278, 278, 667, 556]
HER_W = [dict(zip(HER_MCH, HER_MW0)), dict(zip(HER_MCH, HER_MW1))]


def her_tw(txt, h, bold=False):
    """v50 (G5): the printed width (board units) of txt in Arial at capital height h: the font size is h / 0.718, as
    the PDF writer sets it (_PDF_CAP)"""
    w = HER_W[1 if bold else 0]
    return sum(w.get(c, 556) for c in txt) / 1000.0 * h / 0.718


def her_words(txt):
    """v50 (G5): 'a **b**, c' -> words, each a list of (text, bold) runs; a run with no space before it is glued to the
    word before ('**b**,' is one word of two runs)"""
    words, end_sp = [], True
    for i, part in enumerate(txt.split(u"**")):
        if not part:
            continue
        toks = part.split()
        if not toks:
            end_sp = True
            continue
        glue = bool(words) and not end_sp and not part[0].isspace()
        for j, t_ in enumerate(toks):
            if j == 0 and glue:
                words[-1].append((t_, i % 2 == 1))
            else:
                words.append([(t_, i % 2 == 1)])
        end_sp = part[-1].isspace()
    return words


def her_wrap(txt, h, width):
    """v50 (G5): txt (** = bold) broken into lines of words no wider than width at capital height h"""
    sp = her_tw(u" ", h)
    lines, cur, cw = [], [], 0.0
    for wd in her_words(txt):
        ww = sum(her_tw(t_, h, b_) for t_, b_ in wd)
        if cur and cw + sp + ww > width:
            lines.append(cur)
            cur, cw = [], 0.0
        cw += (sp if cur else 0.0) + ww
        cur.append(wd)
    if cur:
        lines.append(cur)
    return lines


def her_line(B, words, x, y, h, col, L, order=40):
    """v50 (G5): one line of her_wrap, its plain and bold runs each one live text at its measured width; returns the
    x after it"""
    runs = []
    for i, wd in enumerate(words):
        for j, (t_, b_) in enumerate(wd):
            t_ = (u" " if i > 0 and j == 0 else u"") + t_
            if runs and runs[-1][1] == b_:
                runs[-1][0] += t_
            else:
                runs.append([t_, b_])
    cx = x
    for t_, b_ in runs:
        s_ = t_.lstrip()
        cx += her_tw(t_[:len(t_) - len(s_)], h, b_)      # a space that starts a run: its width, no text
        B.text(s_, cx, y, h, col, L, order=order, font=FONT_TITLE, bold=b_)
        cx += her_tw(s_, h, b_)
    return cx


class HerBox(object):
    """v50 (P20.1): a north-up map rectangle in survey m, used as a Frame by View and draw_north_at (u = east, v =
    north whatever its proportions: a Frame turns its longest side to u, so a tall box would come out on its side)"""

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0, self.x1, self.y1 = min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)
        self.cx, self.cy = 0.5 * (self.x0 + self.x1), 0.5 * (self.y0 + self.y1)
        self.w, self.h = self.x1 - self.x0, self.y1 - self.y0
        self.u0, self.u1, self.v0, self.v1 = -0.5 * self.w, 0.5 * self.w, -0.5 * self.h, 0.5 * self.h
        self.ang, self.area = 0.0, self.w * self.h
        self.P = [(self.x0, self.y0), (self.x1, self.y0), (self.x1, self.y1), (self.x0, self.y1)]
        self.bb = (self.x0, self.y0, self.x1, self.y1)

    def local(self, x, y):
        return (x - self.cx, y - self.cy)

    def world(self, u, v):
        return (self.cx + u, self.cy + v)

    def inside(self, x, y):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1


def her_box_around(pts, w_m, h_m, margin):
    """v50: a HerBox w_m x h_m centred on the points' box, larger where the points and margin need it"""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cx, cy = 0.5 * (min(xs) + max(xs)), 0.5 * (min(ys) + max(ys))
    w_m = max(w_m, max(xs) - min(xs) + 2.0 * margin)
    h_m = max(h_m, max(ys) - min(ys) + 2.0 * margin)
    return HerBox(cx - 0.5 * w_m, cy - 0.5 * h_m, cx + 0.5 * w_m, cy + 0.5 * h_m)


def her_bulk(SA, keep=0.995, pad=80.0):
    """v50 (P20.1): the survey's drawn bulk, north up (survey m): the central keep of the surveyed buildings' centres
    in x and in y, pad m round it (3dm_checks §2: the file's own extent is set by control points and loose survey
    points kilometres beyond the drawing); the model's frame box when it has too few buildings"""
    bl = getattr(SA, "bld", None) or []
    xs = sorted(u["cx"] for u in bl if u.get("cx") is not None)
    ys = sorted(u["cy"] for u in bl if u.get("cy") is not None)
    n = min(len(xs), len(ys))
    if n < 50:
        return tuple(SA.F.bb)
    i0 = int(n * (1.0 - keep) / 2.0)
    return (xs[i0] - pad, ys[i0] - pad, xs[n - 1 - i0] + pad, ys[n - 1 - i0] + pad)


def her_bld_col(u):
    """v50: a building's tone, as b_base: heritage (monument, sacred) or plain"""
    return MPL["her"] if u.get("fabric") in ("monument", "sacred") else MPL["bld"]


def her_base(SA, CB, V, k, L, bb):
    """v50 (P20.1, G6): the survey as quiet context under the loop, through ClipB CB, in b_base's layer order and
    tones: mapped green (lighter; no satellite cover), street surfaces and edges (lighter), the stream with its edge and
    the covered course dashed, buildings (heritage in its tone), bridges. Only what meets bb (survey m) is drawn, so the
    whole survey is never clipped piece by piece; buildings from the model's grid (g_bld)."""
    hit = lambda P: bool(P) and bb_hit(bb_pts(P), bb)
    for z in getattr(SA, "zones", None) or []:
        if z.get("kind") not in ("green", "agri") or not z.get("Ps"):
            continue
        if not bb_hit(z.get("bb") or bb_union([bb_pts(P) for P in z["Ps"]]), bb):
            continue
        col = MPL["field"] if z["kind"] == "agri" else (MPL["tree"] if z.get("sub") == "wood" else MPL["park"])
        CB.fill(V.Ps(z["Ps"] + (z.get("Hs") or [])), mix(col, WHITE, HER_GREEN_T), L, 4)
    for rg_ in getattr(SA, "road_net", None) or []:
        if hit(rg_["P"]):
            CB.fill(V.Ps([rg_["P"]] + (rg_.get("H") or [])), HER_ROAD, L, 5)
    for wt in getattr(SA, "water", None) or []:
        if wt.get("P") and bb_hit(wt.get("bb") or bb_pts(wt["P"]), bb):
            CB.fill(V.Ps([wt["P"]] + (wt.get("H") or [])), MPL["water"], L, 6)
    for P in getattr(SA, "water_outline", None) or []:
        if hit(P):
            CB.line(V.P(P), MPL["water_edge"], L, 7, bk_lw(0.15, k))
    for q in getattr(SA, "decks", None) or []:            # streets on decks over the water stay above it
        if hit(q):
            CB.fill([V.P(q)], HER_ROAD, L, 8)
    for P in getattr(SA, "covered", None) or []:
        if hit(P):
            for d in dashes(V.P(P), 1.6 * k, 0.9 * k):
                CB.line(d, MPL["water_edge"], L, 8, bk_lw(0.3, k))
    g = getattr(SA, "g_bld", None)
    units = g.query(bb) if g is not None else [u for u in (getattr(SA, "bld", None) or []) if bb_hit(u["bb"], bb)]
    by = {}
    for u in units:
        by.setdefault(her_bld_col(u), []).append(u["parts"] + (u.get("holes") or []))
    for col, groups in by.items():
        fill_units(CB, V, groups, col, L, 10)
    for P in getattr(SA, "bridges", None) or []:
        if hit(P):
            CB.line(V.P(P), MPL["ink_dark"], L, 11, bk_lw(0.3, k))
    for P in getattr(SA, "road_lines_net", None) or []:
        if hit(P):
            CB.line(V.P(P), HER_ROAD_EDGE, L, 12, bk_lw(0.08, k))
    for r_ in getattr(SA, "roads", None) or []:
        if not r_.get("w") and hit(r_.get("P")):
            CB.line(V.P(r_["P"]), HER_ROAD_EDGE, L, 12, bk_lw(0.08, k))


def her_walk(S, pts):
    """v50 (P20.2): the stream walk K3 -> K4 along the stream's centre line (the longest piece of S.selinus) every
    10 m, and its length along the stream (m); a straight line when the centre line is missing or misses a bridge"""
    a, b = pts[HER_WALK["frm"]], pts[HER_WALK["to"]]
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    main = max(streams, key=pl_length) if streams else None
    if main is None or max(pl_dist(a[0], a[1], main, False), pl_dist(b[0], b[1], main, False)) > HER_SNAP_M:
        LOG.append("Heritage loop: the stream's centre line misses K3 or K4 (over {:.0f} m), so the stream walk is "
                   "drawn straight.".format(HER_SNAP_M))
        return [a, b], math.hypot(b[0] - a[0], b[1] - a[1])
    s0, s1 = pl_chainage(main, a[0], a[1]), pl_chainage(main, b[0], b[1])
    nn = max(2, int(abs(s1 - s0) // 10.0))
    return [pl_point_at(main, s0 + (s1 - s0) * i / float(nn))[0] for i in range(nn + 1)], abs(s1 - s0)


def her_arrow(B, A_, D_, r, k, col, L):
    """v50 (P20.2): a neat arrowhead where the line A_ -> D_ (page; A_ inside the map rectangle r) leaves the map: its
    tip 0.6 mm inside the edge, 2.6 mm long. Returns (tip, base, box) or None"""
    cut = clip_rect_line([A_, D_], r)
    if not cut:
        return None
    E = cut[0][-1]
    dx, dy = D_[0] - A_[0], D_[1] - A_[1]
    dl = math.hypot(dx, dy) or 1.0
    ux, uy = dx / dl, dy / dl
    ah = 2.6 * k
    tip = (E[0] - ux * 0.6 * k, E[1] - uy * 0.6 * k)
    base = (tip[0] - ux * ah, tip[1] - uy * ah)
    tri = [tip, (base[0] - uy * 0.45 * ah, base[1] + ux * 0.45 * ah), (base[0] + uy * 0.45 * ah, base[1] - ux * 0.45 * ah)]
    B.fill([tri], col, L, 62)
    return tip, base, (min(p[0] for p in tri), min(p[1] for p in tri), max(p[0] for p in tri), max(p[1] for p in tri))


def her_labels(B, items, taken, bounds, k, L, segs=(), order=66):
    """v50 (G4): names on a map placed by the shared label_place (place_labels_all, in booklet mm): beside the point,
    else farther out on a thin leader (never across a placed name or symbol), else 0.9 x the size; rank 1 (a heritage
    place, the stream) is left out when it finds no spot (logged), rank 0 (a stop, an arrow) always shows. items:
    dicts lines, x, y (board units), h, col, bold (first line), italic, rank, r0 (the symbol's radius: the leader
    starts at its rim). taken: the symbols' boxes (board units), grown by the names; segs: the loop's lines (no name
    sits on them). Returns the items left out."""
    if not items:
        return []
    pad = 0.35                                            # mm round the words
    tk = [(b[0] / k, b[1] / k, b[2] / k, b[3] / k) for b in taken]
    bd = (bounds[0] / k + 0.6, bounds[1] / k + 0.6, bounds[2] / k - 0.6, bounds[3] / k - 0.6)
    sg = [((p[0] / k, p[1] / k), (q[0] / k, q[1] / k)) for p, q in segs]
    pl = []
    for it in items:
        h, n = it["h"], len(it["lines"])
        w0 = max(her_tw(l_, h, bool(it.get("bold")) and j == 0) for j, l_ in enumerate(it["lines"])) / k
        h0 = (h + (n - 1) * HER_LEAD * h) / k
        pl.append(dict(x=it["x"] / k, y=it["y"] / k, rank=it.get("rank", 0),
                       wh=(lambda a_, b_: (lambda f: (a_ * f + 2.0 * pad, b_ * f + 2.0 * pad)))(w0, h0)))
    got = place_labels_all(pl, tk, bd, sg)
    left = []
    for i, it in enumerate(items):
        if i not in got:
            left.append(it)
            LOG.append(u"Heritage loop: no free spot for the name \"{}\"{}.".format(
                u" / ".join(it["lines"]), u", left out" if it.get("rank", 0) else u" (WARNING: a stop's name)"))
            continue
        b, ldr, f = got[i]
        h = it["h"] * f
        bx = (b[0] * k, b[1] * k, b[2] * k, b[3] * k)
        for j, l_ in enumerate(it["lines"]):
            B.text(l_, bx[0] + pad * k, bx[3] - pad * k - h - j * HER_LEAD * h, h, it["col"], L, order=order,
                   font=FONT_TITLE, bold=bool(it.get("bold")) and j == 0, italic=bool(it.get("italic")))
        if ldr:                                           # the leader from the symbol's rim to the nearer side
            e = lp_leader_end(bx, (it["x"], it["y"]))
            dx, dy = e[0] - it["x"], e[1] - it["y"]
            dl = math.hypot(dx, dy) or 1.0
            r0 = min(it.get("r0", 0.0), 0.8 * dl)
            B.line([(it["x"] + dx * r0 / dl, it["y"] + dy * r0 / dl), e], it["col"], L, order - 1, bk_lw(0.13, k))
        taken.append(bx)
    return left


def her_map(S, SA, B, V, Fm, r, k, L, inner=None):
    """v50 (P20.1, P20.2): one map of the loop in the page rectangle r (View V of the north-up HerBox Fm): the survey
    as quiet context (her_base), the study area (G8), soft legs stop to stop, the stream walk K3-K4 as a broad band
    along the stream (the spine), the stops numbered in loop order, the heritage places, an arrow at the edge where a
    leg or a destination beyond the map leaves it (with the stop's number, or the destination's name and straight
    distance), the stream's name; every name placed clear of the others, the symbols and the loop's lines (G4).
    inner (survey box): the inset's extent on the whole-survey map: drawn and named; inside it numbers only.
    Returns the stream walk's length (m)."""
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    her_base(SA, CB, V, k, L, Fm.bb)
    draw_r28_study(S, CB, V, k, L)                        # G8: the study area's outline
    acc = HER_ACC
    h_lab, h_dot = bk_hk(HER_PT["lab"], k), bk_hk(HER_PT["dot"], k)
    rd = 1.7 * k
    pts = dict((s_["key"], s_["xy"]) for s_ in HER_STOPS)
    num = dict((s_["key"], j + 1) for j, s_ in enumerate(HER_STOPS))
    name = dict((s_["key"], s_["name"]) for s_ in HER_STOPS)
    order = [s_["key"] for s_ in HER_STOPS]
    ins = lambda p: r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3]
    ir = None
    if inner is not None:
        a_, b_ = V.p(inner[0], inner[1]), V.p(inner[2], inner[3])
        ir = (min(a_[0], b_[0]), min(a_[1], b_[1]), max(a_[0], b_[0]), max(a_[1], b_[1]))
    in_ir = lambda p: ir is not None and ir[0] <= p[0] <= ir[2] and ir[1] <= p[1] <= ir[3]
    walk, walk_m = her_walk(S, pts)
    segs, taken, labs = [], [], []

    def leg(P, spine=False):                              # soft (proposal): multiplying tints, no dashes
        if spine:
            soft_line(CB, P, acc, k, L, 30, w_mm=3.0, t=0.12)
        else:
            soft_line(CB, P, acc, k, L, 31, w_mm=1.2, t=0.3)
        for run in clip_rect_line(P, r):
            segs.extend(zip(run[:-1], run[1:]))
    for a, b in zip(order[:-1], order[1:]):
        A_, B_ = V.p(*pts[a]), V.p(*pts[b])
        if (a, b) == (HER_WALK["frm"], HER_WALK["to"]):   # the spine along the stream
            P = V.P(walk)
            leg(P, True)
            taken.extend((q[0] - 0.9 * k, q[1] - 0.9 * k, q[0] + 0.9 * k, q[1] + 0.9 * k) for q in P if ins(q))
            continue
        if ins(A_) == ins(B_):
            leg([A_, B_])
            continue
        far = b
        if not ins(A_):                                   # the end inside first
            A_, B_, far = B_, A_, a
        got = her_arrow(B, A_, B_, r, k, acc, L)
        if got:
            leg([A_, got[1]])
            taken.append(got[2])
            labs.append(dict(lines=[u"to {}".format(num[far])], x=got[0][0], y=got[0][1], h=h_lab, col=acc,
                             bold=True, rank=0))
    for d_ in HER_BEYOND:                                 # P20.2: a destination beyond the map: an arrow at its edge
        a = d_["frm"]
        A_, D_ = V.p(*pts[a]), V.p(*d_["xy"])
        if not ins(A_):
            continue
        lines = [d_["name"], u"{:,.0f} m from {}".format(math.hypot(d_["xy"][0] - pts[a][0], d_["xy"][1] - pts[a][1]),
                                                       num[a])]
        if ins(D_):                                       # on the map (the whole survey's): a ring at its place
            leg([A_, D_])
            ring = circle_pts(D_[0], D_[1], 1.3 * k, 24)
            B.line(ring + [ring[0]], acc, L, 60, bk_lw(0.45, k))
            taken.append((D_[0] - 1.3 * k, D_[1] - 1.3 * k, D_[0] + 1.3 * k, D_[1] + 1.3 * k))
            labs.append(dict(lines=lines, x=D_[0], y=D_[1], h=h_lab, col=acc, bold=True, rank=0, r0=1.3 * k))
            continue
        got = her_arrow(B, A_, D_, r, k, acc, L)
        if got:
            leg([A_, got[1]])
            taken.append(got[2])
            labs.append(dict(lines=lines, x=got[0][0], y=got[0][1], h=h_lab, col=acc, bold=True, rank=0))
    for k_ in order:                                      # the stops, numbered in loop order
        p = V.p(*pts[k_])
        if not ins(p):
            continue
        B.fill([circle_pts(p[0], p[1], rd, 24)], acc, L, 60)
        B.text(str(num[k_]), p[0], p[1], h_lab, WHITE, L, order=61, font=FONT_TITLE, bold=True, align="MC")
        taken.append((p[0] - rd, p[1] - rd, p[0] + rd, p[1] + rd))
        if not in_ir(p):
            labs.append(dict(lines=[name[k_]], x=p[0], y=p[1], h=h_lab, col=INK, bold=True, rank=0, r0=rd))
    for nm, q in HER_DOTS:                                # heritage places
        p = V.p(*q)
        if not ins(p) or in_ir(p):
            continue
        B.fill([circle_pts(p[0], p[1], 0.6 * k, 12)], INK, L, 58)
        taken.append((p[0] - 0.6 * k, p[1] - 0.6 * k, p[0] + 0.6 * k, p[1] + 0.6 * k))
        labs.append(dict(lines=[nm], x=p[0], y=p[1], h=h_dot, col=INK2, rank=1, r0=0.6 * k))
    if ir is not None:                                    # the inset's extent, keyed to it
        q = rect(*ir)
        B.line(q + [q[0]], INK, L, 64, bk_lw(0.35, k))
        segs.extend(zip(q, q[1:] + q[:1]))
        labs.append(dict(lines=[u"inset"], x=ir[0], y=ir[3], h=h_lab, col=INK, bold=True, rank=0))
    sel = [P for P in (getattr(SA, "selinus", None) or []) if len(P) >= 2] or \
        [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    if sel:                                               # the stream's name, clear of the stops (up to 30 mm)
        marks = [V.p(*q) for q in [s_["xy"] for s_ in HER_STOPS] + [q_ for nm, q_ in HER_DOTS]]
        best = None
        for q in resample(max(sel, key=pl_length), 40.0):
            p = V.p(*q)
            if not ins(p) or in_ir(p):
                continue
            d = min([math.hypot(p[0] - m[0], p[1] - m[1]) for m in marks] + [30.0 * k])
            if best is None or d > best[0] + 1e-9:
                best = (d, p)
        if best:
            labs.append(dict(lines=[u"Selinos · Bergama Çayı"], x=best[1][0], y=best[1][1], h=h_lab,
                             col=MPL["water_edge"], italic=True, rank=1))
    her_labels(B, labs, taken, r, k, L, segs)
    return walk_m


def her_foot(B, F, x, yb, ss, k, L, den, tag=u""):
    """v50 ("survey"): b_foot (scale bar, north arrow) and the scale beside them: the page holds two scales, so each
    map states its own"""
    Lm = HER_SB_M.get(den, 400.0)
    low = b_foot(B, F, x, yb, ss, k, L, Lm)
    B.text(u"1:{:,}".format(den) + tag, x + Lm * ss + 16.5 * k, yb - 4.4 * k, bk_hk(7.0, k), INK, L, font=FONT_TITLE,
           bold=True)
    return low


def her_list(B, x, ytop, w, ncol, k, L, walk_m, inline=False):
    """v50 (P20.3, G5, F13): the stops in loop order: the number disc as on the map, the name (English · Turkish, bold)
    and one short explanation with its keywords bold (9 pt, the body minimum); the stream walk K3-K4 after stop 3 with
    the spine's sample. ncol columns of equal width, filled down; inline: the name starts the text. The [n] of the
    sources (HER_SRC) on the list's heading. Returns the y below."""
    h, hn = bk_hk(HER_PT["list"], k), bk_hk(HER_PT["lab"], k)
    pitch, rd, ind, gap = HER_PITCH * h, 1.7 * k, 5.6 * k, HER_GAP_MM * k
    B.text(u"THE LOOP, STOP BY STOP " + bcite(HER_SRC), x, ytop - hn, hn, INK2, L, font=FONT_TITLE, bold=True)
    y0 = ytop - hn - 3.0 * k
    ents = []
    for j, s_ in enumerate(HER_STOPS):
        ents.append((str(j + 1), s_["name"], s_["txt"]))
        if s_["key"] == HER_WALK["frm"]:
            ents.append((None, HER_WALK["name"], HER_WALK["txt"].format(walk_m)))
    cw = (w - gap * (ncol - 1)) / float(ncol)
    per = (len(ents) + ncol - 1) // ncol
    low = y0
    for c in range(ncol):
        cx, yy = x + c * (cw + gap), y0
        for num_, head, txt in ents[c * per:(c + 1) * per]:
            my = yy - 0.5 * h
            if num_ is None:                              # the stream walk: the spine's sample
                soft_line(B, [(cx, my), (cx + 2.0 * rd, my)], HER_ACC, k, L, 30, w_mm=3.0, t=0.12)
            else:
                B.fill([circle_pts(cx + rd, my, rd, 24)], HER_ACC, L, 60)
                B.text(num_, cx + rd, my, hn, WHITE, L, order=61, font=FONT_TITLE, bold=True, align="MC")
            if inline:
                lines = her_wrap(u"**" + head + u"** · " + txt, h, cw - ind)
            else:
                B.text(head, cx + ind, yy - h, h, INK, L, font=FONT_TITLE, bold=True)
                yy -= pitch
                lines = her_wrap(txt, h, cw - ind)
            for ln in lines:
                her_line(B, ln, cx + ind, yy - h, h, INK, L)
                yy -= pitch
            yy -= 0.7 * pitch
        low = min(low, yy)
    return low + 1.7 * pitch - 1.3 * h


def her_leg(inset=False):
    """v50: the page's legend rows (drawn samples, plain names): the loop, the stops, the places, the base, the study
    area (R28_STUDY_LEG, in B_BASE_LEG)"""
    return ([("line", mix(HER_ACC, WHITE, 0.3), u"Heritage loop, stop to stop"),
             ("thick", mix(HER_ACC, WHITE, 0.12), u"Stream walk K3-K4 · the loop's spine"),
             ("dot", HER_ACC, u"Stop, numbered in loop order"), ("dot", INK, u"Heritage place")] +
            ([("line", INK, u"Extent of the inset")] if inset else []) + B_BASE_LEG)


def her_key(S, SA, B, x, top, k, L, Fm):
    """v50 (P20.1, D2 "loop"): the key map beside the loop map (crop drw_heritage_key): the survey's whole drawn bulk
    (her_bulk, grown to hold the loop map), north up, HER_KEY_BK_W mm wide on the booklet page, no scale bar (a key
    map): buildings and the stream, the study area (G8), the loop map's extent, the Acropolis where the key holds it.
    Returns the y below."""
    b0 = her_bulk(SA)
    Fk = HerBox(min(b0[0], Fm.x0 - 60.0), min(b0[1], Fm.y0 - 60.0), max(b0[2], Fm.x1 + 60.0), max(b0[3], Fm.y1 + 60.0))
    ks = HER_KEY_BK_W * k / Fk.w
    kw, kh = Fk.w * ks, Fk.h * ks
    V = View(Fk, ks, x, top)
    r = (x, top - kh, x + kw, top)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    for wt in getattr(SA, "water", None) or []:
        if wt.get("P"):
            CB.fill(V.Ps([wt["P"]] + (wt.get("H") or [])), MPL["water"], L, 6)
    g = getattr(SA, "g_bld", None)
    by = {}
    for u in (g.query(Fk.bb) if g is not None else (getattr(SA, "bld", None) or [])):
        by.setdefault(her_bld_col(u), []).append(u["parts"] + (u.get("holes") or []))
    for col, groups in by.items():
        fill_units(CB, V, groups, col, L, 10)
    draw_r28_study(S, CB, V, k, L)                        # G8
    q = V.P(Fm.P)
    B.line(q + [q[0]], INK, L, 40, bk_lw(0.35, k))       # the loop map's extent
    segs, taken = list(zip(q, q[1:] + q[:1])), []
    labs = [dict(lines=[u"Heritage loop map"], x=q[3][0], y=q[3][1], h=bk_hk(HER_PT["lab"], k), col=INK, bold=True,
                 rank=0)]
    for d_ in HER_BEYOND:
        p = V.p(*d_["xy"])
        if r[0] <= p[0] <= r[2] and r[1] <= p[1] <= r[3]:
            B.fill([circle_pts(p[0], p[1], 0.8 * k, 16)], HER_ACC, L, 60)
            taken.append((p[0] - 0.8 * k, p[1] - 0.8 * k, p[0] + 0.8 * k, p[1] + 0.8 * k))
            labs.append(dict(lines=[d_["name"]], x=p[0], y=p[1], h=bk_hk(HER_PT["dot"], k), col=HER_ACC, rank=1,
                             r0=0.8 * k))
    her_labels(B, labs, taken, r, k, L, segs)
    b_frame(B, r, k, L)
    leg = [("line", INK, u"Extent of the heritage loop map")] + B_BASE_LEG
    crop_panel("heritage_key", x - 0.5 * k, r[1] - 0.5 * k, x + kw + 0.5 * k, top + 0.5 * k,
               u"The whole survey · key to the heritage loop map", None, crop_legend(leg))
    CROP_PANELS[-1]["bk_w"] = kw / k + 1.0                # its width on the booklet page, mm (no scale)
    LOG.append(u"Heritage loop key map (crop drw_heritage_key): the survey's drawn bulk {:,.0f} x {:,.0f} m (central "
               u"99.5 % of {} surveyed buildings' centres, grown to the loop map), {:.0f} x {:.0f} mm, no scale.".format(
                   Fk.w, Fk.h, len(getattr(SA, "bld", None) or []), kw / k, kh / k))
    return r[1]


def her_loop_page(S, SA, B, x, top, k, L):
    """v50 (D2 "loop", default B): the loop map at 1:10,000 north up, its scale bar and north arrow under it, the list
    under them in two columns (crop drw_heritage_loop, drawn for its width on the booklet page), the key map beside
    it (crop drw_heritage_key). Returns the y below."""
    ss = 1000.0 * k / HER_DEN
    Fm = her_box_around([s_["xy"] for s_ in HER_STOPS] + [q for nm, q in HER_DOTS], HER_MAP_BK_W * HER_DEN / 1000.0,
                        HER_MAP_BK_H * HER_DEN / 1000.0, HER_MARGIN_M)
    mw, mh = Fm.w * ss, Fm.h * ss
    V = View(Fm, ss, x, top)
    r = (x, top - mh, x + mw, top)
    walk_m = her_map(S, SA, B, V, Fm, r, k, L)
    b_frame(B, r, k, L)
    low = b_foot(B, Fm, x, r[1], ss, k, L, HER_SB_M[HER_DEN])
    low = her_list(B, x, low - 2.0 * k, mw, 2, k, L, walk_m)
    crop_panel("heritage_loop", x - 0.5 * k, low - 0.5 * k, x + mw + 0.5 * k, top + 0.5 * k, u"City heritage loop",
               crop_scale(ss), crop_legend(her_leg()))
    CROP_PANELS[-1]["bk_w"] = mw / k + 1.0                # its width on the booklet page, mm (prints 1:10,000)
    ac = HER_BEYOND[0]
    LOG.append(u"Heritage loop (D2 \"loop\"): one map at 1:10,000, north up, {:,.0f} x {:,.0f} m ({:.0f} x {:.0f} mm), "
               u"every stop the survey covers on it, the survey from the {} model; {} off the survey, {:,.0f} m from "
               u"the gondola station: an arrow at the map's edge. Stream walk K3-K4 {:,.0f} m along the stream.".format(
                   Fm.w, Fm.h, mw / k, mh / k, "whole-file" if SA is not S else "site frame's", ac["name"],
                   math.hypot(ac["xy"][0] - HER_STOPS[0]["xy"][0], ac["xy"][1] - HER_STOPS[0]["xy"][1]), walk_m))
    return min(low, her_key(S, SA, B, x + mw + HER_GUT_MM * k, top, k, L, Fm))


def her_survey_page(S, SA, B, x, top, k, L):
    """v50 (D2 "survey", A): the survey's whole drawn bulk at 1:20,000 north up (grown to hold every stop, cut to
    HER_SV_MAX_MM), the loop core at 1:5,000 in the column beside it, keyed by its frame on the survey map, each with
    its own scale bar and scale; the list under the inset, one column, the name starting each text. One crop
    drw_heritage_loop (two scales: no scale_den; the caption names both), no key crop. Returns the y below."""
    ss, si = 1000.0 * k / HER_SV_DEN, 1000.0 * k / HER_IN_DEN
    b0 = her_bulk(SA)
    sp = [s_["xy"] for s_ in HER_STOPS]
    bx = (min([b0[0]] + [p[0] - HER_MARGIN_M for p in sp]), min([b0[1]] + [p[1] - HER_MARGIN_M for p in sp]),
          max([b0[2]] + [p[0] + HER_MARGIN_M for p in sp]), max([b0[3]] + [p[1] + HER_MARGIN_M for p in sp]))
    wmax, hmax = HER_SV_MAX_MM[0] * HER_SV_DEN / 1000.0, HER_SV_MAX_MM[1] * HER_SV_DEN / 1000.0
    cx, cy = 0.5 * (bx[0] + bx[2]), 0.5 * (bx[1] + bx[3])
    w_, h_ = min(bx[2] - bx[0], wmax), min(bx[3] - bx[1], hmax)
    if w_ < bx[2] - bx[0] or h_ < bx[3] - bx[1]:
        LOG.append(u"Heritage loop (D2 \"survey\"): the survey's bulk {:,.0f} x {:,.0f} m is cut to {:,.0f} x {:,.0f} m "
                   u"round its centre to fit the page at 1:20,000.".format(bx[2] - bx[0], bx[3] - bx[1], w_, h_))
    Fs = HerBox(cx - 0.5 * w_, cy - 0.5 * h_, cx + 0.5 * w_, cy + 0.5 * h_)
    mw, mh = Fs.w * ss, Fs.h * ss
    gap = HER_GAP_MM * k
    x2 = x + mw + gap
    cw = (BK_AW - 1.0) * k - mw - gap                     # the inset's column (the crop is the panel's full width)
    core = [s_["xy"] for s_ in HER_STOPS if s_["key"] in HER_CORE] + [q for nm, q in HER_DOTS if nm == u"Ulu Cami"]
    Fi = her_box_around(core, cw / si, HER_IN_BK_H * k / si, 70.0)
    iw, ih = Fi.w * si, Fi.h * si
    walk_m = her_map(S, SA, B, View(Fs, ss, x, top), Fs, (x, top - mh, x + mw, top), k, L, inner=Fi.bb)
    b_frame(B, (x, top - mh, x + mw, top), k, L)
    low = her_foot(B, Fs, x, top - mh, ss, k, L, HER_SV_DEN)
    ri = (x2, top - ih, x2 + iw, top)
    her_map(S, SA, B, View(Fi, si, x2, top), Fi, ri, k, L)
    b_frame(B, ri, k, L)
    ilow = her_foot(B, Fi, x2, ri[1], si, k, L, HER_IN_DEN, u" · inset")
    low = min(low, her_list(B, x2, ilow - 2.0 * k, cw, 1, k, L, walk_m, inline=True))
    crop_panel("heritage_loop", x - 0.5 * k, low - 0.5 * k, x2 + cw + 0.5 * k, top + 0.5 * k,
               u"City heritage loop · the whole survey 1:20,000 · inset 1:5,000", None, crop_legend(her_leg(True)))
    CROP_PANELS[-1]["bk_w"] = (x2 + cw - x) / k + 1.0     # its width on the booklet page, mm (the two scales hold)
    LOG.append(u"Heritage loop (D2 \"survey\"): the survey's drawn bulk at 1:20,000 ({:,.0f} x {:,.0f} m, {:.0f} x "
               u"{:.0f} mm), the loop core at 1:5,000 ({:,.0f} x {:,.0f} m, {:.0f} x {:.0f} mm), the list under it; no "
               u"key crop.".format(Fs.w, Fs.h, mw / k, mh / k, Fi.w, Fi.h, iw / k, ih / k))
    return low


def draw_heritage_loop(S, B, x, y, w, U):
    """v50 (MIRAQUA 28 Oct, P20.1-P20.3, D2, F13; replaces v46/v49.1's, 15f): THE HERITAGE LOOP on the survey: the
    loop in its order, gondola valley station (to the Acropolis) -> Red Hall -> K3 -> the stream walk along the
    Selinos (the spine) -> K4 by Ulu Cami and Tabaklar Hamamı -> the bazaar -> Bergama Museum -> the Asklepieion, every
    stop the survey covers on the map, the Acropolis at an arrow with its distance, one short text per stop. Extent by
    HER_EXTENT (D2): "loop" = her_loop_page (crops drw_heritage_loop at 1:10,000 + drw_heritage_key), "survey" =
    her_survey_page (crop drw_heritage_loop: 1:20,000 + inset 1:5,000). Sized for the booklet page: k = board units
    per booklet mm of a drawing 120 U wide, as every theme-B map. Returns the y below."""
    L = "LU_BOARD::HeritageLoop"
    B.text("CITY HERITAGE LOOP", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    k = 120.0 * U / BK_AW
    SA = getattr(S, "whole", None) or S                   # P20.1: the whole-file survey (plan 01's model)
    if SA is S:
        LOG.append("Heritage loop: no whole-file model (run \"technical\", or it failed): the survey under the loop is "
                   "the site frame's only.")
    if HER_EXTENT == "survey":
        return her_survey_page(S, SA, B, x, y - 1.2 * U, k, L) - 1.0 * U
    if HER_EXTENT != "loop":
        LOG.append(u"WARNING: HER_EXTENT \"{}\" is neither \"loop\" nor \"survey\": \"loop\" used.".format(HER_EXTENT))
    return her_loop_page(S, SA, B, x, y - 1.2 * U, k, L) - 1.0 * U
