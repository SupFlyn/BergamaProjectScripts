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
# v27 (MIRAQUA 28 Oct, P24.1-P24.5, F11): the windows are drawn by r28_window_panel (parts/02e_r28_detail.py) in the
# fade-out programme language; of the list above they keep the cuts' bed and flood levels (no bands across the
# stream) and the water route with its areas and rough volumes. The planting codes, band letters, survey spot
# heights and sketches are gone (their tables with them).
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


def crop_legend(keys, alpha):
    """v24: a panel's legend for its booklet crop (drawn samples as colours + plain names): the corridor's symbols
    it draws (LEG_BOOK). v27 (MIRAQUA 28 Oct, P24.4): the 1:1,000 windows carry their own (sh.r28_leg, 02e)."""
    out = []

    def add(kind, colour, label):
        if all(e["label"] != label for e in out):
            out.append({"kind": kind, "colour": colour, "label": label})
    for key, nm, f in LEGEND_V24:
        if ("v24", key) in keys and key in LEG_BOOK:
            add(LEG_BOOK[key][0], LEG_BOOK[key][1], nm.lower() if nm.isupper() else nm)
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
    res = {"script": "bergama_masterplan_v27.py", "version": VERSION, "option": "A", "frames": {},
           "labels_not_drawn": {}, "places_xy": dict((k_, [round(v[0], 1), round(v[1], 1)])
                                                     for k_, v in sorted(plc.items()))}
    wd = dict((w["id"], w) for w in wins)
    drop = [r"^1:[\d,.]+$"]                               # the sheet's scale text: the booklet prints its own
    for pdf, sh, scale in sheets:
        for key, rc, p in sh.panels:
            bid, old, cap = p.bid
            sc_ = getattr(p, "scale", scale)              # v24: each panel its own round scale
            leg_ = crop_legend(p.pleg, _ALPHA[0]) if getattr(p, "pleg", None) else []   # v24: p15 halves: in the crop
            if getattr(p, "r28_leg", None):               # v27 (MIRAQUA 28 Oct, P24.4): the windows' dot legend
                leg_ = p.r28_leg
            if ("dt", "vol") in (getattr(p, "pleg", None) or {}):   # v26.1 (Prompt 8): the rough volumes' method,
                cap += u" · ~ m³ = area × depth: reed basins 0.46 m (EPA 2000), terraces Q100 depth over bed +1 m " \
                       u"at the nearest cut"                 # as the sheet's legend says it (the booklet sets no note)
            bk.crop(bid, os.path.basename(pdf), rc, caption=cap, scale_den=sc_, legend=leg_, drop=drop)
            if getattr(p, "plan_sources", None):          # v27 (MIRAQUA 28 Oct, P23.2, N2): what the p.23 list no
                bk.d["plan_sources"] = res["plan_sources"] = p.plan_sources   # longer prints, for the sources page
            if bid in ("mp_plan", "mp_max_area", "dt_upstream", "dt_k5"):   # v26: drawn for the booklet page at 1:1
                bk.d["blocks"][bid]["bk_w"] = round(rc[2] - rc[0], 3)   # (its width there); v26.1: the 1:1,000
                # windows too (194 + 4 + 194 mm = the page's 392 mm), so p.26 prints them at 1:1,000 in one row
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
