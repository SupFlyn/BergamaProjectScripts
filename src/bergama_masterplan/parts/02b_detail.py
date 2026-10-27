# ================================================================ v21: the 1:1,000 detail sheet and the booklet crops
# Aras 25 Oct 21:49 on the booklet's 1:1,000 page: "this should add more detail from what we have shown in
# masterplan". The detail sheet shows the two windows of the booklet's C3 page (upstream entry; K5 with Demeter's
# Garden) at 1:1,000 with what the whole plan cannot show, all from the project's data:
#   cuts      at the water board's surveyed channel cuts (the proposal sections stand on them) the bed level and
#             the DSI Q100 / Q500 levels with the width each covers there (CUT_AT); v25: no cut or section lines
#   route     the zone base's water links numbered in the order of the water route (ROUTE), with the areas the
#             script computes from the zone curves (no script computes a storage volume: left out, logged)
#   planting  band letters and species codes of the booklet's verified list (plan page C7 = water board v1.9
#             PLANT_BANDS / SPECIES) on the zones whose wetness tier they belong to (ZONE_PLANTING)
#   levels    survey spot heights (NOKTA_TAKEOMETRI) in the bed and on the bank tops, by the edges river_walks found
#   sketches  (Aras 21:57) terrace steps as a few strokes in the retention terraces and flood terraces, ramps as
#             wedges on the zone base's people-to-the-water links: zones and sketch marks, abstract, no dimensions
# Booklet (CROP_SPEC.md, Aras 21:47): the booklet's drawings are crops of the sheets; blocks.json holds one crop per
# panel (both halves of the masterplan sheet, both detail windows), results.json the frames and places.
DT_SCALE = 1000.0
DT_WINDOWS = [  # crop id, old booklet id, working area, sheet title, booklet caption, zone names the window must show
    ("dt_upstream", "c3_a", "calisma_alan[0]", u"UPSTREAM ENTRY · COLLECT, CLEAN, HOLD",
     u"Upstream entry: collect, clean, hold", (u"REED BASINS", u"RETENTION TERRACES", u"SPILLWAY", u"SHADED WALK")),
    ("dt_k5", "c3_b", "calisma_alan[1]", u"K5 BRIDGE · DEMETER'S GARDEN", u"K5 bridge and Demeter's Garden",
     (u"DEMETER'S GARDEN",))]
# CUT_AT: the water board's surveyed channel cuts (water board v1.9 CUTS, proposal sections v4 panels 1-4):
# number, name, centre (survey m) and span (u m, + = left bank looking downstream) from
# research/rain_river_levels/scripts/surveyed_sections/levels2_out.json (24 Oct); bed and DSI Q100 / Q500 levels (m,
# Manning n 0.050) and the width each covers (u from, to) as there (= water board CUTS bed + depth).
CUT_AT = [("1", u"UPSTREAM ENTRY", (29693.022, 32569.176), (-74.5, 85.5), 70.36, (73.35, -29.5, 14.0), (73.66, -30.5, 15.0)),
          ("2", u"K4 BRIDGE", (29959.774, 32264.566), (-21.0, 91.5), 64.77, (67.33, -58.5, 16.5), (67.61, -70.5, 16.5)),
          ("3", u"K5 BRIDGE", (30354.663, 31689.671), (-86.0, 64.5), 55.96, (58.41, -37.5, 12.0), (58.75, -45.5, 12.5)),
          ("4", u"DOWNSTREAM REACH", (30991.856, 31039.404), (-39.5, 26.5), 45.67, (47.72, -29.5, 19.5), (48.0, -30.5, 20.0))]
# The water route at the upstream entry (zone base links, by the zones they join): order and short words
ROUTE = [((None, "WT"), u"INTO {}", 1), (("WS", "WT"), u"FROM {}", 0), (("WT", "WD"), u"TO {}", 1),
         (("WD", None), u"BACK TO THE STREAM", None)]   # (from, to), words, which end's zone they name
ROUTE_SHORT = {u"RETENTION TERRACES": u"TERRACES"}
# Planting (booklet page C7 / water board v1.9 bands A-F and species): band letters and species codes per zone, by
# the zone's wetness (bed and reed basins wet most of the year: B; flood terrace: C; terraces: C and E; dry tops: E
# and F). A design reading of the bands; only species of the verified list.
SPECIES_CODE = [("Ty", u"Typha angustifolia"), ("Ph", u"Phragmites australis"), ("Me", u"Mentha aquatica"),
                ("Sa", u"Salix alba"), ("Ta", u"Tamarix smyrnensis"), ("Vi", u"Vitex agnus-castus"),
                ("Po", u"Populus alba"), ("Fr", u"Fraxinus angustifolia"), ("Pl", u"Platanus orientalis"),
                ("La", u"Lavandula stoechas"), ("Qu", u"Quercus robur"), ("Ul", u"Ulmus laevis")]   # v24: + Qu, Ul
BAND_NAME = {"A": u"A STRIP AND BED · PERMANENT", "B": u"B MARSH · 150-365 D A YEAR", "C": u"C WILLOW · 50-150 D",
             "D": u"D WET MEADOW · 10-150 D", "E": u"E DRY MEADOW · 0.5-50 D", "F": u"F TERRACES · EXTREME ONLY"}
ZONE_PLANTING = {("WT", None): ("B", ("Ty", "Ph", "Me")), ("WA", "W"): ("B", ("Ty", "Ph", "Me")),
                 ("WA", "F"): ("C", ("Sa", "Ta")), ("WS", None): ("CE", ("Vi", "Po", "Fr")),
                 ("GR", None): ("EF", ("Pl", "La"))}
STEP_M = 4.0                         # spacing of the terrace step strokes, m (sketch)
RAMP_W = (3.0, 1.2)                  # ramp wedge width at the top and at the water, m (sketch)
SPOT_GAP_M, SPOT_BANK_M = 30.0, 10.0   # spot levels at least this far apart; bank top = within this of the edge
SPOT_MAX = (6, 8)                    # at most this many bed / bank spot levels per window
# v22 (Aras 26 Oct 06:27 "make them have calculated roughly"): rough volume on the water route = zone area x depth.
# Reed basins: 0.46 m, the water depth of EPA's worked example ("water depth = 0.46 meters (1.5 ft)"; vegetated
# depth "a few inches to two feet or more"), EPA 832-F-00-024 Free Water Surface Wetlands, Sep 2000. Terraces (Aras
# 06:32 picked): the water over them in the DSI Q100 flood = Q100 level at the nearest cut - (bed + TERRACE_UP).
STORE_DEPTH = {"WT": 0.46}
TERRACE_UP = 1.0                     # terrace level above the bed, m (the project's flood rule: "Terrace +1 m")


def store_m3(z):
    """(rough volume m3, words) of a water-route zone, or None: reed basins area x 0.46 m; retention terraces area x
    the Q100 depth over them at the nearest channel cut."""
    if z["code"] in STORE_DEPTH:
        return z["m2"] * STORE_DEPTH[z["code"]], u""
    if z["code"] == "WS" and z.get("P"):
        cx = sum(p[0] for p in z["P"]) / len(z["P"])
        cy = sum(p[1] for p in z["P"]) / len(z["P"])
        num, nm, c, span, bed, q100, q500 = min(CUT_AT, key=lambda r: (r[2][0] - cx) ** 2 + (r[2][1] - cy) ** 2)
        return z["m2"] * max(0.0, q100[0] - (bed + TERRACE_UP)), u" in Q100"
    return None
DT_TS = 2.6                          # detail label size, mm (7.4 pt at 1:1; the booklet sets them at 7.5 pt)


def places(spec, CL, survey):
    """Named places (world m): K4, K3, the Red Hall and K5 are city link's surveyed spine anchors (K4 = piece A's
    start, K3 its end, Red Hall = piece C's start, K5 its end), each bridge snapped to the nearest surveyed bridge
    (YOL_KOPRU) within 60 m."""
    sp = dict((pc.get("id"), pc) for pc in spec.get("spine", []))
    out = {}
    for nm, (pid, end) in ((u"K4", ("A", "frm")), (u"K3", ("A", "to")), (u"RED HALL", ("C", "frm")),
                           (u"K5", ("C", "to"))):
        if pid in sp and sp[pid].get(end):
            out[nm] = tuple(sp[pid][end])
    mids = [((B[0][0] + B[-1][0]) / 2.0, (B[0][1] + B[-1][1]) / 2.0) for B in survey.get("bridge", [])]
    for nm in (u"K4", u"K3", u"K5"):
        if nm in out and mids:
            m = min(mids, key=lambda q: math.hypot(q[0] - out[nm][0], q[1] - out[nm][1]))
            if math.hypot(m[0] - out[nm][0], m[1] - out[nm][1]) <= 60.0:
                out[nm] = m
    return out


def detail_windows(D, plc, frame):
    """[{id, old, key, title, caption, R}] north-up windows of frame (mm) x DT_SCALE: centred on the zones it must
    show (and the cut in it), for K5 on the bridge moved just enough to hold Demeter's Garden and the cut."""
    Wm, Hm = frame[0] * DT_SCALE / 1000.0, frame[1] * DT_SCALE / 1000.0
    out = []
    for bid, old, key, title, cap, names in DT_WINDOWS:
        zs = [z for z in D.zones if z["area"] == key and name_of(z, z.get("own", "")) in names]
        pts = [p for z in zs for p in z["P"]] or [p for z in D.zones if z["area"] == key for p in z["P"]]
        if not pts:
            continue
        b = bbox(pts)
        c = ((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0)
        if bid == "dt_k5" and plc.get(u"K5"):
            k5 = plc[u"K5"]
            cut = [x[2] for x in CUT_AT if x[1] == u"K5 BRIDGE"]
            need = bbox(pts + [k5] + cut)
            c = (min(max(k5[0], need[2] - Wm / 2 + 10.0), need[0] + Wm / 2 - 10.0),
                 min(max(k5[1], need[3] - Hm / 2 + 10.0), need[1] + Hm / 2 - 10.0))
        out.append({"id": bid, "old": old, "key": key, "title": title, "caption": cap,
                    "R": (c[0] - Wm / 2, c[1] - Hm / 2, c[0] + Wm / 2, c[1] + Hm / 2)})
    return out


def place_label(pg, lines, anchor, taken, W, H, colour, d0=1.2, leader=True, avoid=(), more=(), anywhere=False):
    """A label block [(text, size, bold)] on a free spot round anchor (page mm, y up), off the rings in avoid, with
    a thin leader when it sits off the anchor. v22: then round each point of more (e.g. along the route), and with
    anywhere the free spot nearest anchor on the whole panel (2 mm grid). Returns its box or None."""
    w, h = block_size(lines)
    ax, ay = anchor
    on = 0.0 <= ax <= W and 0.0 <= ay <= H              # v22: the leader goes to anchor only when it is on the panel

    def free(b):
        return not (b[0] < 0.8 or b[1] < 0.8 or b[2] > W - 0.8 or b[3] > H - 0.8 or
                    any(hit(b, t, 0.4) for t in taken) or (avoid and not box_clear(b, avoid)))

    def put(b, px, py, far):
        draw_block(pg, lines, b[0], b[3], colour, None)
        taken.append(b)
        if leader and far:
            qx, qy = min(max(px, b[0]), b[2]), min(max(py, b[1]), b[3])
            pg.line([(px, py), (qx, qy)], COL["ink2"], 0.15)
        return b

    for k_, (px, py) in enumerate([anchor] + list(more)):
        for d in (d0, d0 + 2.0, d0 + 4.0, d0 + 7.0, d0 + 11.0, d0 + 16.0, 24.0, 32.0):
            for i in range(16):
                a = math.radians(i * 22.5 + 11.25)
                cx, cy = px + math.cos(a) * (d + w / 2), py + math.sin(a) * (d + h / 2)
                b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
                if free(b):
                    return put(b, ax, ay, d > 3.0 or k_ > 0) if on or k_ == 0 else put(b, px, py, d > 3.0)
    if anywhere:                                         # v22: last, any free spot on the panel, nearest first
        cs = [(x_ * 2.0, y_ * 2.0) for x_ in range(int(W / 2.0) + 1) for y_ in range(int(H / 2.0) + 1)]
        for cx, cy in sorted(cs, key=lambda c_: (c_[0] - ax) ** 2 + (c_[1] - ay) ** 2):
            b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            if free(b):
                return put(b, ax, ay, True) if on else put(b, cx, cy, False)
    return None


def _normal_at(ref, q):
    """Unit normal (left of the flow) of STREAM_REF at the point nearest q."""
    s = arclen(ref)
    c, _ = chain_at(ref, q)
    _, t = at_len(ref, s, c)
    return (-t[1], t[0]), t


def _boxes_line(P, half, taken):
    taken += boxes_along(P, half)


def detail_overlay(win, D, CL, spots, plc, missing, warn):
    """The detail of one window, drawn by window_panel after the corridor (see the head of this part)."""
    R = win["R"]
    inR = lambda p, m=0.0: R[0] - m <= p[0] <= R[2] + m and R[1] - m <= p[1] <= R[3] + m
    ref = CL["W"]["ref"]
    shapes = D.zones + D.strips

    def f(pg, T, k, taken, dw, dh, hubs=()):
        ink, ink2 = COL["ink_dark"], COL["ink2"]
        av = [(r_, bbox(r_)) for r_ in hubs]
        # ---- sketches: terrace steps in the terrace zones, ramps on the people-to-the-water links (under the rest)
        for z in D.zones:
            if not (z["code"] == "WS" or (z["code"] == "WA" and z["tier"] == "F")) or not any(inR(p) for p in z["P"]):
                continue
            n, t = _normal_at(ref, z["q"])
            ext = [(p[0] - z["q"][0]) * n[0] + (p[1] - z["q"][1]) * n[1] for p in z["P"]]
            alo = [(p[0] - z["q"][0]) * t[0] + (p[1] - z["q"][1]) * t[1] for p in z["P"]]
            o = min(ext) + STEP_M / 2.0
            i = 0
            while o < max(ext):
                L_ = [(z["q"][0] + n[0] * o + t[0] * a, z["q"][1] + n[1] * o + t[1] * a)
                      for a in (min(alo) - 2.0, max(alo) + 2.0)]
                for r_ in cut_runs(L_, lambda x, y: pip(x, y, z["P"]), 0.5):
                    if len(r_) >= 2 and math.hypot(r_[-1][0] - r_[0][0], r_[-1][1] - r_[0][1]) > 3.0:
                        P = hand_line([T(p) for p in (r_[0], r_[-1])], 0.25, 8.0, 31 + i, over=0.6)
                        pg.line(P, zone_tones(z)[2], 0.3, alpha=0.75)
                        leg(("dt", "steps"))
                o += STEP_M
                i += 1
        for i, L in enumerate(D.links):
            if L["kind"] != "people" or not any(inR(p) for p in L["P"]):
                continue
            P = [T(p) for p in L["P"]]
            (ax, ay), (bx, by) = P[0], P[-1]
            d = math.hypot(bx - ax, by - ay) or 1.0
            ux, uy = (bx - ax) / d, (by - ay) / d
            nx, ny = -uy, ux
            w0, w1 = RAMP_W[0] * k / 2.0, RAMP_W[1] * k / 2.0
            ring_ = [(ax + nx * w0, ay + ny * w0), (bx + nx * w1, by + ny * w1), (bx - nx * w1, by - ny * w1),
                     (ax - nx * w0, ay - ny * w0)]
            pg.poly([ring_], fill=ink2, alpha=0.2)
            pg.poly([ring_], stroke=ink2, lw=0.25)
            for j in (1, 2, 3):                          # chevrons down the slope
                cx, cy = ax + ux * d * j / 4.0, ay + uy * d * j / 4.0
                ww = (w0 + (w1 - w0) * j / 4.0) * 0.8
                pg.line([(cx - ux * 1.0 + nx * ww, cy - uy * 1.0 + ny * ww), (cx, cy),
                         (cx - ux * 1.0 - nx * ww, cy - uy * 1.0 - ny * ww)], ink2, 0.25)
            taken.append(bbox(ring_))
            leg(("dt", "ramp"))
        # ---- the flood levels at the water board's surveyed channel cuts: the width Q100 / Q500 cover there, the bed
        # and both levels. v25 (booklet Prompt 2: "no section lines on any map"): the cut lines, their view markers
        # and the site board's section lines are no longer drawn (each sections page has its own key map)
        cut_lab = []
        for num, nm, c, span, bed, q100, q500 in CUT_AT:
            if not inR(c):
                continue
            n, t = _normal_at(ref, c)
            at = lambda u: (c[0] + n[0] * u, c[1] + n[1] * u)
            for lv, lw, colr in ((q500, 2.2, COL["river_mid"]), (q100, 2.2, COL["river_dark"])):
                pg.line([T(at(lv[1])), T(at(lv[2]))], colr, lw, cap=0, alpha=0.45)
            leg(("dt", "q"))
            P = [T(at(q500[1])), T(at(q500[2]))]
            x0, y0 = T(c)
            _boxes_line(P, 1.2, taken)
            inside = [p for p in P if 0 <= p[0] <= dw and 0 <= p[1] <= dh]
            cut_lab.append(([(nm, DT_TS, True), (u"bed +{:.2f}".format(bed), DT_TS, False),
                             (u"Q100 +{:.2f} · Q500 +{:.2f}".format(q100[0], q500[0]), DT_TS, False)],
                            inside[0] if inside else (min(max(x0, 2.0), dw - 2.0), min(max(y0, 2.0), dh - 2.0))))
        # ---- the water route: the zone base's water links, numbered in the route's order
        steps = []
        for L in D.links:
            if L["kind"] != "water" or not any(inR(p) for p in L["P"]):
                continue
            a, b = link_shapes(L, shapes)
            ab = (a["code"] if a and a in D.zones else None, b["code"] if b and b in D.zones else None)
            order = next((i for i, st in enumerate(ROUTE) if st[0] == ab), len(ROUTE))
            steps.append((order, L, a, b, ab))
        steps.sort(key=lambda s_: s_[0])
        route_lab = []
        for n_, (order, L, a, b, ab) in enumerate(steps, 1):
            P = [T(p) for p in L["P"]]
            link_arrow(pg, P, "water", L["heads"], 3 + n_)
            leg(("link", "water"))
            _boxes_line(P, 1.2, taken)
            if order < len(ROUTE):
                end = ROUTE[order][2]
                z = (a, b)[end] if end is not None else None
                nm = ROUTE_SHORT.get(name_of(z, z.get("own", "")), name_of(z, z.get("own", ""))) if z else u""
                txt = ROUTE[order][1].format(nm)
                if z is not None:
                    txt += u" {:,.0f} m²".format(z["m2"])
                    sv = store_m3(z)                         # v22: rough volume, area x depth
                    if sv:
                        txt += u" · ~{:,.0f} m³{}".format(round(sv[0], -1), sv[1])
                        leg(("dt", "vol"))
            else:
                txt = (L["label"] or u"WATER").replace(u"RIVER", u"STREAM")
            s = arclen(P)
            (mx, my), _ = at_len(P, s, s[-1] / 2.0)
            pg.circle(mx, my, 2.2, fill=COL["white"])
            pg.circle(mx, my, 1.9, fill=COL["river_dark"])
            pg.text(str(n_), mx, my - 0.85, 2.4, COL["white"], bold=True, align="C")
            taken.append((mx - 2.2, my - 2.2, mx + 2.2, my + 2.2))
            leg(("dt", "route"))
            route_lab.append(([(u"{} {}".format(n_, txt), DT_TS, True)], (mx, my),   # v22: + spots along the route
                              [at_len(P, s, s[-1] * f_)[0] for f_ in (0.3, 0.7, 0.1, 0.9, 0.0, 1.0)]))
        # ---- survey spot levels: lowest in the bed, highest on the bank tops (edges of river_walks)
        rows = [r for r in (CL["W"].get("rows") or []) if r.get("NE") and r.get("SW") and inR(r["p"], 60.0)]
        bed, bank = [], []
        for q in spots:
            if not inR(q, -2.0) or not rows:
                continue
            r = min(rows, key=lambda r_: (r_["p"][0] - q[0]) ** 2 + (r_["p"][1] - q[1]) ** 2)
            if math.hypot(r["p"][0] - q[0], r["p"][1] - q[1]) > 40.0:
                continue
            t_ = (q[0] - r["p"][0]) * r["n"][0] + (q[1] - r["p"][1]) * r["n"][1]
            e1, e0 = r["NE"]["e"], r["SW"]["e"]
            if e0 <= t_ <= e1:
                bed.append(q)
            elif e1 < t_ <= e1 + SPOT_BANK_M or e0 - SPOT_BANK_M <= t_ < e0:
                bank.append(q)
        spot_lab = []
        for pts, low, mx_, colr, kind in ((bed, True, SPOT_MAX[0], COL["river_dark"], "spot_bed"),
                                          (bank, False, SPOT_MAX[1], COL["ink_dark"], "spot_bank")):
            kept = []
            for q in sorted(pts, key=lambda q: q[2] if low else -q[2]):
                if len(kept) >= mx_:
                    break
                if all(math.hypot(q[0] - p[0], q[1] - p[1]) >= SPOT_GAP_M for p in kept):
                    kept.append(q)
            for q in kept:
                x, y = T(q)
                pg.line([(x - 0.7, y), (x + 0.7, y)], colr, 0.25)
                pg.line([(x, y - 0.7), (x, y + 0.7)], colr, 0.25)
                taken.append((x - 0.8, y - 0.8, x + 0.8, y + 0.8))
                leg(("dt", kind))
                spot_lab.append(([(u"+{:.2f}".format(q[2]), DT_TS * 0.85, False)], (x, y), colr))
        # ---- labels: cuts, route, bridge, planting codes, spot levels
        for lines, anc in cut_lab:
            if not place_label(pg, lines, anc, taken, dw, dh, ink, avoid=av):
                missing.append(lines[0][0])
        for lines, anc, along in route_lab:              # v22: never left out (Aras 26 Oct: 4 BACK TO THE STREAM)
            if not place_label(pg, lines, anc, taken, dw, dh, COL["river_dark"], d0=2.6, avoid=av, more=along,
                               anywhere=True):
                missing.append(lines[0][0])
        for nm in (u"K4", u"K5"):                         # (not when the commons' keywords already name it)
            if plc.get(nm) and inR(plc[nm]) and nm + u" BRIDGE" not in HUB.get(win["key"], (u"", []))[1]:
                if not place_label(pg, [(nm + u" BRIDGE", DT_TS, True)], T(plc[nm]), taken, dw, dh, ink, d0=2.0,
                                   avoid=av):
                    missing.append(nm + u" BRIDGE")
        for z in D.zones:
            pl = ZONE_PLANTING.get((z["code"], z["tier"])) or ZONE_PLANTING.get((z["code"], None))
            if not pl or not any(inR(p) for p in z["P"]):
                continue
            TP = z["TP"] if z.get("area") == win["key"] and z.get("TP") else [T(p) for p in z["P"]]
            TP = clip_ring(TP, (0.0, 0.0, dw, dh))
            txt = u"{} · {}".format(u" ".join(pl[0]), u" ".join(pl[1]))
            b_ = None
            if len(TP) >= 3:
                TPs = thin(TP, 300)
                for sz in (DT_TS, DT_TS * 0.85):
                    b_ = fit_inside(TPs, inside_spots(TPs), [(txt, sz, False)], taken, pad=0.4, avoid=av)
                    if b_:
                        pg.text(txt, b_[0] + 0.4, b_[1] + 0.4 + 0.06 * sz, sz, zone_tones(z)[2])
                        taken.append(b_)
                        break
            if b_:
                for b_ in pl[0]:
                    leg(("band", b_))
                for c_ in pl[1]:
                    leg(("sp", c_))
            else:
                missing.append(txt + u" (" + name_of(z, z.get("own", "")) + u")")
        for lines, anc, colr in spot_lab:
            place_label(pg, lines, anc, taken, dw, dh, colr, d0=0.6, leader=False, avoid=av)
    return f


def detail_legend():
    """v21: the detail sheet's legend groups (only what it draws): its layers, the planting bands, species codes."""
    W_ = COL["white"]

    def line_sw(*specs):
        def f(pg, x, y, w, h):
            for c_, lw, dash, a_ in specs:
                pg.line([(x, y + h / 2), (x + w, y + h / 2)], c_, lw, dash, cap=0 if dash else 1, alpha=a_)
        return f

    def cross_sw(colr):
        def f(pg, x, y, w, h):
            cx, cy = x + w / 2, y + h / 2
            pg.line([(cx - 1.4, cy), (cx + 1.4, cy)], colr, 0.3)
            pg.line([(cx, cy - 1.4), (cx, cy + 1.4)], colr, 0.3)
        return f

    def steps_sw(pg, x, y, w, h):
        for i in range(4):
            yy = y + h * (i + 0.5) / 4
            pg.line([(x + 1.0, yy), (x + w - 1.0, yy)], MP["storage"][2], 0.3, alpha=0.75)

    def ramp_sw(pg, x, y, w, h):
        R_ = [(x, y + h * 0.1), (x + w, y + h * 0.35), (x + w, y + h * 0.65), (x, y + h * 0.9)]
        pg.poly([R_], fill=COL["ink2"], alpha=0.2)
        pg.poly([R_], stroke=COL["ink2"], lw=0.25)

    def route_sw(pg, x, y, w, h):
        pg.circle(x + w / 2, y + h / 2, 3.0, fill=COL["river_dark"])
        pg.text(u"1", x + w / 2, y + h / 2 - 1.2, 3.4, W_, bold=True, align="C")

    det = []
    for key, name, f in ((("dt", "q"), u"Q500 / Q100 FLOOD WIDTH AT A SURVEYED CUT",
                          line_sw((COL["river_mid"], 2.2, None, 0.45), (COL["river_dark"], 1.0, None, 0.45))),
                         (("dt", "route"), u"WATER ROUTE · STEP", route_sw),
                         (("dt", "spot_bed"), u"SPOT LEVEL · BED (m)", cross_sw(COL["river_dark"])),
                         (("dt", "spot_bank"), u"SPOT LEVEL · BANK TOP (m)", cross_sw(COL["ink_dark"])),
                         (("dt", "steps"), u"TERRACE STEPS", steps_sw),
                         (("dt", "ramp"), u"RAMP", ramp_sw)):
        if key in LEG:
            det.append((name, f))

    def none_sw(pg, x, y, w, h):
        return None
    if ("dt", "vol") in LEG:                             # v22: how the rough volumes are made
        det.append((u"~ m³ = ROUGH VOLUME, AREA × DEPTH · REED BASINS 0.46 m · TERRACES: Q100 OVER BED +1 m "
                    u"AT THE NEAREST CUT", none_sw))
    bands = [(BAND_NAME[b_], none_sw) for b_ in "ABCDEF" if ("band", b_) in LEG]
    sp = [(u"{}  {}".format(c_, nm), none_sw) for c_, nm in SPECIES_CODE if ("sp", c_) in LEG]
    return [(u"DETAIL", det), (u"PLANTING BANDS · DAYS WET", bands), (u"SPECIES", sp)]


def crop_legend(keys, alpha):
    """v24: a 1:1,000 window's legend for its booklet crop (drawn samples as colours + plain names): the corridor's
    symbols it draws (LEG_BOOK), the detail layers and the species codes placed (which plants go where)."""
    out = []

    def add(kind, colour, label):
        if all(e["label"] != label for e in out):
            out.append({"kind": kind, "colour": colour, "label": label})
    for key, nm, f in LEGEND_V24:
        if ("v24", key) in keys and key in LEG_BOOK:
            add(LEG_BOOK[key][0], LEG_BOOK[key][1], nm.lower() if nm.isupper() else nm)
    for key, kind, colour, label in ((("dt", "q"), "line", COL["river_mid"], u"Q500 flood width"),
                                     (("dt", "route"), "dot", COL["river_dark"], u"water route step"),
                                     (("dt", "spot_bed"), "dot", COL["river_dark"], u"spot level, bed"),
                                     (("dt", "spot_bank"), "dot", COL["ink_dark"], u"spot level, bank top"),
                                     (("dt", "steps"), "line", MP["storage"][2], u"terrace steps"),
                                     (("dt", "ramp"), "fill", mix(COL["white"], COL["ink2"], 0.2), u"ramp")):
        if key in keys:
            add(kind, colour, label)
    for c_, nm in SPECIES_CODE:
        if ("sp", c_) in keys:
            add("dot", COL["tree_mid"], u"{} {}".format(c_, nm))
    return out


def booklet_crops(folder, sheets, wins, plc, missing):
    """v21: booklet/blocks.json (one crop per panel of every sheet) and booklet/results.json (as v20's keys:
    script, version, option, frames under the old booklet ids, labels_not_drawn, places_xy)."""
    bk = BkBlocks(folder, u"MasterPlan", SHORT)
    for old in ("c1_s1.pdf", "c1_s2.pdf", "c3_a.pdf", "c3_b.pdf"):   # v20's separate drawings: now crops
        try:
            os.remove(bk.path(old))
        except OSError:
            pass
    res = {"script": "bergama_masterplan_v25.py", "version": VERSION, "option": "A", "frames": {},
           "labels_not_drawn": {}, "places_xy": dict((k_, [round(v[0], 1), round(v[1], 1)])
                                                     for k_, v in sorted(plc.items()))}
    wd = dict((w["id"], w) for w in wins)
    drop = [r"^1:[\d,.]+$"]                               # the sheet's scale text: the booklet prints its own
    for pdf, sh, scale in sheets:
        for key, rc, p in sh.panels:
            bid, old, cap = p.bid
            sc_ = getattr(p, "scale", scale)              # v24: each panel its own round scale
            leg_ = crop_legend(p.pleg, _ALPHA[0]) if getattr(p, "pleg", None) else []   # v24: p15 halves: in the crop
            bk.crop(bid, os.path.basename(pdf), rc, caption=cap, scale_den=sc_, legend=leg_, drop=drop)
            fr = {"crop": bid, "scale_den": sc_, "w_mm": round(rc[2] - rc[0], 1), "h_mm": round(rc[3] - rc[1], 1)}
            if bid in wd:
                R = wd[bid]["R"]
                fr.update(centre_xy=[round((R[0] + R[2]) / 2, 1), round((R[1] + R[3]) / 2, 1)],
                          window_m=[round(R[2] - R[0], 1), round(R[3] - R[1], 1)])
            else:                                         # the masterplan panel's world extent (survey x, m)
                R = p.world
                fr.update(from_m=round(R[0], 1), to_m=round(R[2], 1), overlap_m=0.0)
            res["frames"][old] = fr
            res["labels_not_drawn"][old] = missing.get(bid, [])
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return bk.save()
