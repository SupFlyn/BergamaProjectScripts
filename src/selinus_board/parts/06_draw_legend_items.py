def draw_legend_items(B, items, x, y, width, U, L, h=0.5):
    """Legend rows; two columns only when every label fits. Returns the y below."""
    sw = 1.1
    lw2 = width / 2.0
    if any(k_ == "hdr" for k_, _c, _l in items):            # v33: titled groups, each in as many columns as fit
        groups, cur = [], None
        for it in items:
            if it[0] == "hdr":
                cur = [it[2], []]
                groups.append(cur)
            elif cur is None:
                cur = ["", [it]]
                groups.append(cur)
            else:
                cur[1].append(it)
        ncol = max(1, int(width // (16.0 * U)))
        colw = width / ncol
        for title, its in groups:
            if title:
                B.text(title, x, y, h * U, INK2, L, font=FONT_TITLE, bold=True)
                y -= 1.6 * h * U + 0.15 * U
            for j, (kind, col, label) in enumerate(its):
                cx = x + (j % ncol) * colw
                draw_symbol(B, kind, col, cx, y, U, L, sw=sw)
                B.fit(label, cx + (sw + 0.5) * U, y, h * U, colw - (sw + 0.8) * U, INK, L)
                if j % ncol == ncol - 1 or j == len(its) - 1:
                    y -= 1.6 * h * U + 0.15 * U
            y -= 0.35 * U
        return y
    two = all(tw(lbl, h * U) + (sw + 0.6) * U <= lw2 - 0.6 * U for _, _, lbl in items)
    cols = 2 if two and len(items) > 2 else 1
    colw = width / cols
    for j, (kind, col, label) in enumerate(items):
        cx = x + (j % cols) * colw
        draw_symbol(B, kind, col, cx, y, U, L, sw=sw)
        B.fit(label, cx + (sw + 0.5) * U, y, h * U, colw - (sw + 0.8) * U, INK, L)
        if j % cols == cols - 1 or j == len(items) - 1:
            y -= 1.6 * h * U + 0.15 * U
    return y


# ============================================================ THE LAND-USE MAP
def edge_key(a, b):
    return frozenset(((round(a[0], 3), round(a[1], 3)), (round(b[0], 3), round(b[1], 3))))


def edge_counts(polys):
    n = {}
    for P in polys:
        for i in range(len(P)):
            e = edge_key(P[i], P[(i + 1) % len(P)])
            n[e] = n.get(e, 0) + 1
    return n


def unit_outline(parts, n=None):
    """v41 (Aras 26 Oct 06:35 "these lines in what is there looks weird"): the pale outline of a building = its edges
    without the walls it shares with another piece (n: edge counts over all buildings), so a footprint the survey
    draws as one block and the script cuts along its party walls reads as one mass, with no cut lines through it.
    Open runs of edges, or the closed piece where nothing is shared."""
    n = n or edge_counts(parts)
    k = edge_key
    out = []
    for P in parts:
        m = len(P)
        inner = [n.get(k(P[i], P[(i + 1) % m]), 0) > 1 for i in range(m)]
        if not any(inner):
            out.append(P + [P[0]])
            continue
        i0 = inner.index(True)
        run = []
        for j in range(1, m + 1):
            i = (i0 + j) % m
            if inner[i]:
                if len(run) > 1:
                    out.append(run)
                run = []
            else:
                run = run or [P[i]]
                run.append(P[(i + 1) % m])
        if len(run) > 1:
            out.append(run)
    return out


def draw_landuse_map(S, B, V, bcol=None):
    """bcol (v33): the colour of each building (default: its land-use colour)."""
    L = "LU_BOARD::Map"
    s = V.s
    U = S.U
    B.fill([V.P(S.F.P)], PAPER, L + "::paper", 2)
    draw_landcover(S, B, V, L + "::landcover", 3)       # v31: under the surveyed / OSM ground (4)
    for z in S.zones:
        if z["kind"] == "green":
            col = GREEN_SUB.get(z["sub"], CAT["green"][1])
        elif z["kind"] == "transport":
            col = mix(CAT["transport"][1], PAPER, 0.3)
        else:
            col = CAT[z["kind"]][1]
        B.fill(V.Ps(z["Ps"] + z["Hs"]), col, L + "::" + z["kind"], 4)
        if z["kind"] == "vacant" and TEXTURE:
            for ln in hatch_lines(z["Ps"], z["Hs"], z["bb"], 5.0, math.radians(45)):
                B.line(V.P(ln), mix(INK, PAPER, 0.55), L + "::texture", 5, 0.06)
        if z["kind"] == "agri" and z["sub"] == "field" and TEXTURE:
            ang = (_zlib_crc(repr([round(v_, 2) for v_ in z["bb"]]).encode("utf-8")) % 180) * math.pi / 180.0
            for ln in hatch_lines(z["Ps"], z["Hs"], z["bb"], 7.0, ang):
                B.line(V.P(ln), mix(CAT["agri"][1], INK, 0.22), L + "::texture", 5, 0.04)
    for w in S.water:
        B.fill(V.Ps([w["P"]] + w.get("H", [])), CAT["water"][1], L + "::water", 6)
    for q in getattr(S, "decks", []):
        B.fill([V.P(q)], ROADC, L + "::streets", 7)
    for P in getattr(S, "covered", []):              # the covered course: a hidden line over the streets and roofs
        for d in dashes(V.P(P), 0.35 * U, 0.25 * U):
            B.line(d, BLUE_D, L + "::water", 19, 0.12)
    for P in S.water_outline:                         # the river edge: one continuous line per stretch (under decks)
        B.line(V.P(P), BLUE_D, L + "::water", 6, 0.13)
    for P in river_free_banks(S):                     # other surveyed streams and ditches, thinner
        B.line(V.P(P), BLUE_D, L + "::water", 7, 0.07)
    for P in S.pools:
        B.line(V.P(P), BLUE_D, L + "::water", 7, 0.08)
    road_lines(S, B, V, L + "::streets", 8, casing=ROAD_EDGE, surface=ROADC, min_w=0.04, fill=ROAD_FILL)
    for p in S.paths:                                 # paths whose width the survey does not show: a thin line
        if not p.get("w"):
            B.line(V.P(p["P"]), ROADC, L + "::streets", 9, 0.04)
    if TEXTURE:
        for x, y, r, kind in S.trees:
            bx, by = V.p(x, y)
            B.fill([circle_pts(bx + 0.35 * r * s, by - 0.35 * r * s, r * s, 14)], TREE_SHADOW, L + "::trees", 10)
            B.fill([circle_pts(bx, by, r * s, 14)], TREE_COLS.get(kind, TREE_COLS["tree"]), L + "::trees", 11)
            if kind == "pine":
                B.fill([circle_pts(bx - 0.25 * r * s, by + 0.25 * r * s, 0.45 * r * s, 10)],
                       mix(TREE_COLS["pine"], PAPER, 0.35), L + "::trees", 12)
        sh = mix(INK, PAPER, 0.6)
        for u in S.bld:
            off = min(3.0, 0.11 * u["h"]) * s
            B.fill([[(x + off, y - off) for x, y in V.P(P)] for P in u["parts"] + (u.get("holes") or [])], sh,
                   L + "::texture", 13)
    shared = edge_counts([P for u in S.bld for P in u["parts"]]) if TEXTURE else None
    for u in S.bld:
        col = CAT[u["cat"]][1]
        if u["annex"]:
            col = mix(col, PAPER, 0.35)
        if bcol is not None:
            col = bcol(u)
        B.fill(V.Ps(u["parts"] + (u.get("holes") or [])), col, L + "::" + u["cat"], 14)
        if TEXTURE:
            for P in unit_outline(u["parts"], shared) + [H + [H[0]] for H in u.get("holes") or []]:
                B.line(V.P(P), PAPER, L + "::texture", 15, 0.04)
    for P in S.slope_hatch:
        B.line(V.P(P), mix(INK2, PAPER, 0.4), L + "::ground", 16, 0.04)
    for P in S.slopes:
        B.line(V.P(P), INK2, L + "::ground", 16, 0.08)
    for P in S.stairs:
        B.line(V.P(P), INK2, L + "::ground", 16, 0.05)
    for P in S.fences:
        B.line(V.P(P), mix(INK2, PAPER, 0.3), L + "::ground", 16, 0.04)
    for P in S.park_lines:
        for d in dashes(V.P(P), 0.4 * U, 0.28 * U):
            B.line(d, mix(CAT["green"][1], INK, 0.3), L + "::ground", 16, 0.08)
    for P in S.walls:
        B.line(V.P(P), INK, L + "::walls", 17, 0.16)
    for P in S.bridges:
        B.line(V.P(P), INK, L + "::walls", 18, 0.24)


def study_areas_from(R, I):
    """v19: the closed curves on STUDY_LAYERS in survey coordinates: [dict(name, layer, P, area)]. Read only."""
    out = []
    for lay in STUDY_LAYERS:
        nm = (lay[:-5] if lay.lower().endswith("_alan") else lay).upper()
        for P in (R.get("plines") or {}).get(lay, []):
            pts = [T_apply(I, p[0], p[1]) for p in P]
            closed = len(pts) > 3 and math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1]) < 1e-6
            if not closed:
                LOG.append("WARNING: a curve on the layer '{}' is not closed, so it is not drawn as a study area."
                           .format(lay))
                continue
            pts = pts[:-1]
            out.append(dict(name=nm, layer=lay, P=pts, area=shoelace(pts)[0]))
    if out:
        LOG.append("Group study areas (read only, never drawn): " + "; ".join(
            "{} {:,.0f} m2".format(a["name"], a["area"]) for a in out) + ".")
    return out


def sec_road_spans(S, x0, y0, ux, uy, L, step=0.25):
    """v25: the streets a section line crosses: [(s0, s1, name, src)], s along the line. The stretch is where the line
    runs on a surveyed street surface (S.road_net); the name is the OSM street (S.roads, footpaths excluded) whose
    centreline crosses inside that stretch (the nearest one), else "". A named OSM centreline crossed off every surface
    gives (s, s, name, "osm") (position only, no surveyed width). Read only."""
    net = getattr(S, "road_net", None) or []
    n = int(L / step) + 1
    ss_ = [min(L, k * step) for k in range(n)]
    xs = [x0 + ux * s_ for s_ in ss_]
    ys = [y0 + uy * s_ for s_ in ss_]
    lb = (min(xs), min(ys), max(xs), max(ys))
    on = [False] * n
    for rg_ in net:
        P = rg_["P"]
        bx0, by0 = min(p[0] for p in P), min(p[1] for p in P)
        bx1, by1 = max(p[0] for p in P), max(p[1] for p in P)
        if bx1 < lb[0] or bx0 > lb[2] or by1 < lb[1] or by0 > lb[3]:
            continue
        for k in range(n):
            if not on[k] and bx0 <= xs[k] <= bx1 and by0 <= ys[k] <= by1 and pip(xs[k], ys[k], P) and \
                    not any(pip(xs[k], ys[k], H) for H in rg_.get("H") or []):
                on[k] = True
    spans = []
    k = 0
    while k < n:
        if on[k]:
            j = k
            while j + 1 < n and on[j + 1]:
                j += 1
            spans.append([max(0.0, ss_[k] - 0.5 * step), min(L, ss_[j] + 0.5 * step), "", "survey"])
            k = j + 1
        else:
            k += 1
    hits = []                                            # (s, name) where an OSM street centreline crosses the line
    for r in getattr(S, "roads", None) or []:
        hw = (r.get("tags") or {}).get("highway")
        if hw in PED:
            continue
        nm = proper_name((r.get("tags") or {}).get("name") or "")
        P = r["P"]
        for i in range(len(P) - 1):
            (ax, ay), (bx, by) = P[i][:2], P[i + 1][:2]
            ex, ey = bx - ax, by - ay
            den = ux * ey - uy * ex
            if abs(den) < 1e-12:
                continue
            wx, wy = ax - x0, ay - y0
            s = (wx * ey - wy * ex) / den
            t = (wx * uy - wy * ux) / den
            if 0.0 <= t <= 1.0 and 0.0 <= s <= L:
                hits.append((s, nm))
    for s, nm in sorted(hits):
        sp = next((q for q in spans if q[0] - 1.0 <= s <= q[1] + 1.0), None)
        if sp is not None:
            if nm and not sp[2]:
                sp[2] = nm
        elif nm and not any(abs(q[0] - s) < 3.0 and q[2] == nm for q in spans):
            spans.append([s, s, nm, "osm"])
    return sorted(tuple(q) for q in spans)


def road_label(s0, s1, nm, src):
    """v25: the text of a street in a section."""
    nm_ = tr_upper(nm) if nm else "STREET"
    if src == "osm":
        return nm_ + " · OSM line, no surveyed surface"
    return "{} · {:.1f} m on the cut".format(nm_, s1 - s0)


def draw_sec_roads(S, B, L, P, g_at, line, Lm, U, off=0.0, order=36, w=0.5):
    """v25: the streets in a section: a bold ink line on the ground over each street's surface, its ends ticked.
    Returns [(s_mid, z, label)] for the section's callouts (s within this part)."""
    x0, y0, x1, y1 = line[:4]
    Ll = math.hypot(x1 - x0, y1 - y0)
    if Ll < 1e-6:
        return []
    ux, uy = (x1 - x0) / Ll, (y1 - y0) / Ll
    out = []
    # v50 (MIRAQUA 28 Oct, laptop speed): the spans of a line once (sections_plan draws each cut dry at every step
    # of its words; the streets' point-in-polygon search was repeated each time)
    memo = getattr(S, "_s28_spans", None)
    if memo is None:
        memo = S._s28_spans = {}
    kk_ = (x0, y0, x1, y1)
    if kk_ not in memo:
        memo[kk_] = sec_road_spans(S, x0, y0, ux, uy, Ll)
    for s0, s1, nm, src in memo[kk_]:
        a0, a1 = s0 - off, s1 - off
        if a1 < -1e-6 or a0 > Lm + 1e-6:
            continue
        a0, a1 = max(0.0, a0), min(Lm, a1)
        if src == "osm":
            q = P(a0, g_at(a0))
            B.line([(q[0], q[1] - 0.25 * U), (q[0], q[1] + 0.45 * U)], INK, L, order, w)
        else:
            nn = max(2, int((a1 - a0) / 0.5) + 1)
            pts = [P(a0 + (a1 - a0) * k / (nn - 1.0), g_at(a0 + (a1 - a0) * k / (nn - 1.0))) for k in range(nn)]
            B.line(pts, INK, L, order, w)
            for q in (pts[0], pts[-1]):
                B.line([(q[0], q[1] - 0.2 * U), (q[0], q[1] + 0.2 * U)], INK, L, order, 0.5 * w)
        sm = 0.5 * (a0 + a1)
        out.append((sm, g_at(sm), road_label(s0, s1, nm, src)))
    return out


def draw_map_annotations(S, B, V, U, rh=None):
    """The stream's name and the frame line. v45 (Prompt 2: "no section lines on any map"): the cuts S1-S8 are no
    longer marked here (each sections page has its own key map); rh = the name's height (default 0.5 U)."""
    L = "LU_BOARD::Map::annotation"
    s = V.s
    if S.river_label and S.selinus:                     # river name on the stretch farthest from the section marks
        main = max(S.selinus, key=pl_length)
        Lm = pl_length(main)
        best = None
        for k in range(3, 18):
            p, t = pl_point_at(main, Lm * k / 20.0)
            d = min([seg_dist(p[0], p[1], x0, y0, x1, y1) for x0, y0, x1, y1, nm in S.sec_lines] + [1e9])
            d = min(d, pl_dist(p[0], p[1], S.F.P, True) * 1.5)
            if best is None or d > best[0]:
                best = (d, p, t)
        _, p, t = best
        ang = V.angle(t[0], t[1])
        bx, by = V.p(p[0], p[1])
        rh = rh or 0.5 * U
        off = 2.8 * rh
        B.text(S.river_label[3], bx - math.sin(ang) * off, by + math.cos(ang) * off, rh, BLUE_D, L,
               align="MC", angle=ang, italic=True)
    B.line(V.P(S.F.P + [S.F.P[0]]), INK, L, 21, 0.25)


# ============================================================ LEGEND / DISTRIBUTION / READINGS (page 1)
def draw_legend(S, B, x, y, w, U):
    L = "LU_BOARD::Legend"
    B.text("LAND USE", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    hy = y - 1.7 * U
    h = 0.5
    B.text("ha", x + w - 6.0 * U, hy, 0.42 * U, INK2, L, align="R")
    B.text("%", x + w, hy, 0.42 * U, INK2, L, align="R")
    B.line([(x, hy - 0.45 * U), (x + w, hy - 0.45 * U)], INK, L, 20, 0.15)
    ry = hy - 1.4 * U
    tot = frame_total(S)                                 # v35: every % is a % of the site frame
    namew = w - 1.6 * U - 13.0 * U
    for k in CAT_ORDER:
        a = S.area.get(k, 0.0)
        if a <= 0.0:
            continue
        B.fill([rect(x, ry - 0.05 * U, x + 1.1 * U, ry + 0.62 * U)], CAT[k][1], L, 20)
        B.line(rect(x, ry - 0.05 * U, x + 1.1 * U, ry + 0.62 * U) + [(x, ry - 0.05 * U)], INK2, L, 21, 0.05)
        parts = CAT[k][0].split(" · ")
        B.fit(parts[0], x + 1.6 * U, ry, h * U, namew, INK, L)
        B.text("{:.2f}".format(a / 1e4), x + w - 6.0 * U, ry, h * U, INK, L, align="R")
        B.text("{:.1f}".format(100.0 * a / tot), x + w, ry, h * U, INK, L, align="R")
        if len(parts) > 1:
            ry -= 0.72 * U
            B.fit(parts[1], x + 1.6 * U, ry, 0.38 * U, namew, INK2, L)
        ry -= 1.12 * U
    B.line([(x, ry + 0.55 * U), (x + w, ry + 0.55 * U)], INK, L, 20, 0.15)
    ry -= 0.25 * U
    rest = getattr(S, "rest", None) or []
    if rest:                                             # v35: the mapped part, then the rest of the frame by satellite
        B.text("MAPPED ON THE SURVEY AND OSM", x + 1.6 * U, ry, h * U, INK, L, bold=True)
        B.text("{:.2f}".format(S.total_area / 1e4), x + w - 6.0 * U, ry, h * U, INK, L, bold=True, align="R")
        B.text("{:.1f}".format(100.0 * S.total_area / tot), x + w, ry, h * U, INK, L, bold=True, align="R")
        ry -= 1.12 * U
        for k_, lab, col, a in rest:
            B.fill([rect(x, ry - 0.05 * U, x + 1.1 * U, ry + 0.62 * U)], col, L, 20)
            B.line(rect(x, ry - 0.05 * U, x + 1.1 * U, ry + 0.62 * U) + [(x, ry - 0.05 * U)], INK2, L, 21, 0.05)
            parts = lab.split(" · ") if k_ == "rest" else [lab]
            B.fit(parts[0], x + 1.6 * U, ry, h * U, namew, INK, L)
            B.text("{:.2f}".format(a / 1e4), x + w - 6.0 * U, ry, h * U, INK, L, align="R")
            B.text("{:.1f}".format(100.0 * a / tot), x + w, ry, h * U, INK, L, align="R")
            if len(parts) > 1:
                ry -= 0.72 * U
                B.fit(parts[1], x + 1.6 * U, ry, 0.38 * U, namew, INK2, L)
            ry -= 1.12 * U
        B.line([(x, ry + 0.55 * U), (x + w, ry + 0.55 * U)], INK, L, 20, 0.15)
        ry -= 0.25 * U
    B.text("TOTAL · SITE FRAME" if rest else "TOTAL", x + 1.6 * U, ry, h * U, INK, L, bold=True)
    B.text("{:.2f}".format(tot / 1e4), x + w - 6.0 * U, ry, h * U, INK, L, bold=True, align="R")
    B.text("100.0", x + w, ry, h * U, INK, L, bold=True, align="R")
    ry -= 1.2 * U
    km, km_w = getattr(S, "street_km", (0.0, 0.0))
    # v38: keywords and [n] (was a paragraph); the sentences are entries of the Sources key
    r1 = bcite("Land use: ground cover inside the frame: surveyed footprints by use, open ground, street surfaces and "
               "the stream bed. Pale tones are sheds and annexes. Street surface only where its width is measured on "
               "the survey.")
    B.fit("ground cover in the frame · pale = sheds, annexes " + r1, x, ry, 0.38 * U, w, INK2, L)
    ry -= 0.7 * U
    B.fit("street width measured · {:.1f} of {:.1f} km {}".format(km_w, km, r1), x, ry, 0.38 * U, w, INK2, L)
    ry -= 0.7 * U
    if rest:
        r2 = bcite("Unmapped ground: the ground the survey and OSM leave unmapped is split by ESA WorldCover 2021 (10 m "
                   "satellite classes, CC BY 4.0) on a {:g} m raster; orchards inferred from the survey's olive and "
                   "fruit-tree symbols.".format(REST_CELL))
        B.fit("satellite rows · ESA WorldCover 2021 " + r2, x, ry, 0.38 * U, w, INK2, L)     # v40: no caveat
        ry -= 0.7 * U
    return ry


def page1_readings(S):
    """v38: the page-one readings as figures for drawing (were five generated sentences): the largest use, solid and
    void, the surveyed floors, green and fields. Every value is computed here, as before."""
    R = {}
    tot = S.total_area
    land = [(k, S.area[k]) for k in CAT_ORDER if S.area.get(k, 0) > 0 and k != "water"]
    if land:
        k, a = max(land, key=lambda t: t[1])
        R["use"] = (CAT[k][1], short(CAT[k][0]), 100.0 * a / tot)
    bc = 100.0 * S.built_area / S.frame_area
    R["solid"] = (bc, "tight" if bc > 40 else ("loose" if bc < 22 else "measured"))
    surv = [u for u in S.bld if u["floors_src"] == "survey" and not u["annex"]]
    if surv:
        cnt = {}
        for u in surv:
            cnt[u["floors"]] = cnt.get(u["floors"], 0) + 1
        R["floors"] = (dict((f, 100.0 * n / len(surv)) for f, n in cnt.items()),
                       sum(u["floors"] for u in surv) / float(len(surv)), S.int_peak_name or "")
    g = rest_of(S, "trees", "grass", "shrub")            # as green_sat_note: the satellite's green on the unmapped ground
    R["green"] = (S.green_pct, S.n_major_green,
                  100.0 * (sum(z["A"] for z in S.zones if z["kind"] == "green") + g) / S.frame_area if g > 0.0 else None)
    agri = 100.0 * (S.area.get("agri", 0.0) + rest_of(S, "farmland", "orchard")) / S.frame_area   # v35: + satellite
    if agri >= 5.0:
        R["agri"] = agri
    return R


def draw_distribution(S, B, x, y, U):
    """Donut of ground cover; about 13 page units wide. Returns the y below."""
    L = "LU_BOARD::Distribution"
    B.text("DISTRIBUTION", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    r1, r0 = 4.4 * U, 2.6 * U
    cx, cy = x + r1 + 1.4 * U, y - 2.4 * U - r1 - 1.0 * U
    tot = frame_total(S)                                 # v35: the site frame, the unmapped ground by satellite class
    a0 = math.pi / 2.0
    slices = [(S.area.get(k, 0.0), CAT[k][1]) for k in CAT_ORDER] + [
        (a, col) for _k, _l, col, a in (getattr(S, "rest", None) or [])]
    for a, col in slices:
        if a <= 0.0:
            continue
        fr = a / tot
        a1 = a0 - 2.0 * math.pi * fr
        B.fill([annulus(cx, cy, r0, r1, a0, a1)], col, L, 20)
        B.line([(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)), (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0))],
               BG, L, 21, 0.2)
        if fr >= 0.04:
            am = 0.5 * (a0 + a1)
            B.text("{:.0f}%".format(100.0 * fr), cx + (r1 + 0.9 * U) * math.cos(am), cy + (r1 + 0.9 * U) * math.sin(am),
                   0.4 * U, INK, L, align="MC")
        a0 = a1
    B.text("{:.1f}".format(tot / 1e4), cx, cy + 0.1 * U, 0.95 * U, INK, L, font=FONT_TITLE, align="C")
    B.text("ha site frame" if getattr(S, "rest", None) else "ha mapped", cx, cy - 0.8 * U, 0.36 * U, INK2, L, align="C")
    crop_panel("ground_cover", x - 0.2 * U, cy - r1 - 1.5 * U, cx + r1 + 1.6 * U, cy + r1 + 1.5 * U,
               u"Ground cover in the frame")              # v40: the booklet crop of the ring
    return cy - r1 - 1.6 * U


def draw_readings(S, B, x, y, w, bottom, U):
    """Page-one readings as pictures (v38, visual first; were five sentences): the largest use as a tile, solid and
    void as a bar, the surveyed floors as a histogram, green and fields as rings. `bottom` is kept for the callers."""
    O = "LU_BOARD::Readings"
    B.text("READINGS", x, y, 1.05 * U, INK, O, font=FONT_TITLE, bold=True)
    R = page1_readings(S)
    oy = y - 1.6 * U
    tfill = mix(PAPER, (255, 255, 255), 0.5)
    if R.get("use"):
        col, nm, pct = R["use"]
        oy = vis_tiles(B, x, oy, w, [("build", nm.upper() + " · LARGEST", "{:.0f}% of mapped".format(pct),
                                      bcite("Readings: shares of the mapped cover (largest use) and of the site frame "
                                            "(solid / void, green, fields)."))],
                       U, O, h=1.3, ink=INK, grey=INK2, fill=tfill, rule=FAINT) - 1.0 * U
    bc, grain = R["solid"]                                # solid / void bar
    B.text("SOLID / VOID · {} GRAIN {}".format(grain.upper(), bcite("Solid / void: the voids are streets, courtyards "
                                                                     "and the stream bed.")), x, oy, 0.4 * U, INK, O,
           font=FONT_TITLE, bold=True)
    by = oy - 0.55 * U
    B.fill([rect(x, by - 0.8 * U, x + w, by)], PAPER, O, 20)
    B.fill([rect(x, by - 0.8 * U, x + w * min(1.0, bc / 100.0), by)], INK, O, 21)
    B.line(rect(x, by - 0.8 * U, x + w, by) + [(x, by - 0.8 * U)], INK2, O, 22, 0.05)
    B.text("solid {:.0f}%".format(bc), x + 0.2 * U, by - 0.6 * U, 0.4 * U, PAPER if bc > 25 else INK, O, order=23)
    B.text("void {:.0f}%".format(100.0 - bc), x + w - 0.2 * U, by - 0.6 * U, 0.4 * U, INK, O, order=23, align="R")
    oy = by - 0.8 * U - 1.2 * U
    if R.get("floors"):                                   # floors histogram of the surveyed buildings
        share, avg, peak = R["floors"]
        B.text("FLOORS · SURVEYED · MEAN {:.1f} {}".format(avg, bcite("Skyline: surveyed buildings by floors; density "
                                                                       "gathers where it rises.")), x, oy, 0.4 * U,
               INK, O, font=FONT_TITLE, bold=True)
        fl = sorted(share)
        hb = 2.6 * U
        cw = w / float(max(1, len(fl)))
        top_ = max(share.values()) or 1.0
        base = oy - 0.7 * U - hb
        for i, f in enumerate(fl):
            hh = hb * share[f] / top_
            B.fill([rect(x + i * cw + 0.08 * cw, base, x + (i + 0.92) * cw, base + hh)],
                   INTENSITY[2] if f == 1 else mix(INTENSITY[2], PAPER, 0.35), O, 20)
            B.fit("{:.0f}%".format(share[f]), x + (i + 0.5) * cw, base + hh + 0.12 * U, 0.3 * U, cw * 0.98, INK, O,
                  align="C")
            B.fit("{}".format(f), x + (i + 0.5) * cw, base - 0.45 * U, 0.3 * U, cw * 0.98, INK2, O, align="C")
        B.line([(x, base), (x + w, base)], INK2, O, 21, 0.05)
        oy = base - 0.9 * U
        B.text("floors" + (" · densest near " + peak if peak else ""), x, oy, 0.3 * U, INK2, O)
        oy -= 1.2 * U
    r = min(2.4 * U, w / 5.0)                             # green and fields as rings of the frame
    rings = [("GREEN", R["green"][0], CAT["green"][1], "{} larger ground{}".format(
        R["green"][1], "" if R["green"][1] == 1 else "s"), "{:.1f}%",
        bcite("Green: the mapped green of the frame, a thin weave anchored by its larger grounds."))]
    if R["green"][2] is not None:
        rings.append(("+ SATELLITE GREEN", R["green"][2], mix(CAT["green"][1], PAPER, 0.3), "unmapped ground too",
                      "{:.0f}%", bcite("With the satellite's tree cover, grass and shrubs on the unmapped ground.")))
    if R.get("agri") is not None:
        rings.append(("FIELDS & ORCHARDS", R["agri"], CAT["agri"][1], "town loosens into its plain", "{:.0f}%",
                      bcite("Fields and orchards (survey, OSM and satellite) of the frame: here the town loosens into "
                            "its plain.")))
    cw = w / float(len(rings))
    for i, (head, pct, col, sub, fmt_, ref) in enumerate(rings):
        cx, cy = x + (i + 0.5) * cw, oy - 0.4 * U - r
        vis_ring(B, cx, cy, r, pct, col, FAINT, O)
        B.text(fmt_.format(pct), cx, cy - 0.2 * U, 0.5 * U, INK, O, font=FONT_TITLE, bold=True, align="C")
        B.fit(head + " " + ref, cx, cy - r - 0.65 * U, 0.3 * U, cw * 0.96, INK, O, font=FONT_TITLE, bold=True, align="C")
        B.fit(sub, cx, cy - r - 1.15 * U, 0.26 * U, cw * 0.96, INK2, O, align="C")
    return oy - 0.4 * U - 2.0 * r - 1.6 * U


# ============================================================ DIAGRAM PANELS
def mini_base(S, B, V, L, water_col=BLUE_L):
    B.fill([V.P(S.F.P)], PAPER, L, 2)
    for w in S.water:
        B.fill(V.Ps([w["P"]] + w.get("H", [])), water_col, L, 8)


def fill_units(B, V, groups, col, L, order):
    """Fill the outlines of many buildings in one colour, a building's courtyards (holes) always in the same hatch."""
    chunk = []
    for loops in groups:
        chunk.extend(loops)
        if len(chunk) >= 400:
            B.fill(V.Ps(chunk), col, L, order)
            chunk = []
    if chunk:
        B.fill(V.Ps(chunk), col, L, order)


def mini_buildings(S, B, V, L, colfn, order=12):
    by_col = {}
    for u in S.bld:
        col = colfn(u)
        if col is not None:
            by_col.setdefault(col, []).append(u["parts"] + (u.get("holes") or []))
    for col, groups in by_col.items():
        fill_units(B, V, groups, r28_nz(col), L, order)   # v50 (MIRAQUA 28 Oct, P06.3): nonzero, overlaps stay filled


MAIN_ROADS = ("motorway", "trunk", "primary", "secondary", "tertiary")


# ============================================================ PAGE-ONE BLOCKS THAT FILL A GIVEN BAND


# ============================================================ ENVIRONMENT · sun and shade, solar radiation, sound, surface heat
# Methods (all standard and published; checked against pvlib, the reference solar library, during development):
#   sun position   NOAA / Meeus solar position algorithm, refraction included (agrees with pvlib to ~0.01 deg)
#   weather        PVGIS-SARAH2 typical meteorological year 2005-2020 for these coordinates (EU JRC), every hour
#   terrain        PVGIS DEM horizon profiles every 100 m over the frame (bilinear between nodes), as seen from the
#                  ground; in a section plane lowered with height by the fall of the terrain's own horizon (v16.3:
#                  survey terrain inside the frame, PVGIS DEM node heights to the grid's edge, terrain beyond as far)
#   trees          Meta / WRI 1 m canopy height crowns (modelled heights); leaf type per crown (CLC+ Backbone 2021 /
#                  Sentinel-2) and the deciduous leaf-out and leaf-fall days (Sentinel-2 2019-2025); 3 % / 46 %
#                  transmission, olive (evergreen broadleaf) 15 % (v24)
#   shade          exact obstruction by every building and crown and the terrain for every degree of sun azimuth,
#                  every minute of the four key days and of all 365 days (the mean day)
#   radiation      every hour of the typical year: direct + Perez 1990 diffuse (isotropic, horizon band) + ground
#                  reflection on the ground and every roof; mean kWh/m2 per day of each season
#   sound          RLS-90 road emission and segment method (distance, air, ground); building screening RLS-90-type
#                  D_z with ISO 9613-2 limits and sign (v21, R01-26: not VBUS's screening; no D_met, no reflections);
#                  Lden from day / evening / night traffic; optional calibration with your own measurements
#   surface heat   Landsat 8/9 Collection 2 Level-2 surface temperature (USGS), the mean of the clear scenes of
#                  each season
ENV_PATH = clean_path(inp("env_path", None), "env_path") or data_file("bergama_environment.json") or ""
# v33 24 Oct: all files under Downloads/Bergama/ (Aras rule): cache in cached/selinus_cache, the rest in output/selinus_board
#@include ../../common/bergama_paths.py
BERGAMA_DIR = BERGAMA_ROOT
SELINUS_CACHE_DIR = os.path.join(BERGAMA_DIR, "cached", "selinus_cache")
SELINUS_OUT_DIR = bg_output("selinus_board")          # v44 (27 Oct): final PDFs only (in selinus_board_pdf)
SELINUS_RES_DIR = bg_cache("selinus_board")           # v44: results other scripts read, maps, photos (working files)
ENVIRONMENT = bool(inp("environment", False))
NOISE_PALETTE = str(inp("noise_palette", "") or "").strip().lower()     # "" = the graded bands (v16.4)
NOISE_PTS_IN = inp("noise_points", [])
NOISE_DB_IN = inp("noise_db", [])
FOCUS_IN = inp("focus", None)

SEASONS = [dict(key="spring", name="SPRING", day=(3, 20), months=(3, 4, 5), event="spring equinox, 20 March"),
           dict(key="summer", name="SUMMER", day=(6, 21), months=(6, 7, 8), event="summer solstice, 21 June"),
           dict(key="autumn", name="AUTUMN", day=(9, 22), months=(9, 10, 11), event="autumn equinox, 22 September"),
           dict(key="winter", name="WINTER", day=(12, 21), months=(12, 1, 2), event="winter solstice, 21 December")]
# Deciduous crowns are in leaf from leaf-out (inclusive) to leaf-fall (exclusive), days of the year measured over this
# site: Sentinel-2 L2A NDVI 2019-2025 of the Copernicus CLC+ Backbone 2021 broadleaved deciduous pixels, unmixed from
# their canopy-free surroundings, double-logistic fit over the day of the year, 50 % of the seasonal amplitude:
# leaf-out day 106 (16 April; 95 % interval 102-110), leaf-fall day 318 (14 November; 311-324). Environment data v2
# carries the same values ("phenology") and they are taken from there.
LEAF_DOY = [106, 318]
EVERGREEN = ("pine", "olive")             # needle-leaved and broadleaved evergreen crowns
LEAF_KIND = {0: "tree", 1: "olive", 2: "pine"}     # environment data v2 leaf code: deciduous, evergreen broadleaf, needle


def leaf_on_doy(doy):
    """Deciduous crowns in leaf on these days of the year (1-365)."""
    d = np.asarray(doy)
    return (d >= LEAF_DOY[0]) & (d < LEAF_DOY[1])


def doy_of(mo, d):
    return sum((31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[:mo - 1]) + d


def leaf_key(season):
    """Deciduous crowns in leaf on a season's key day (None or any other key: in leaf)."""
    for s_ in SEASONS:
        if s_["key"] == season:
            return LEAF_DOY[0] <= doy_of(*s_["day"]) < LEAF_DOY[1]
    return True


def leaf_dates():
    """The leaf-out day and the last day in leaf, as text ("16 April", "13 November")."""
    import datetime as _dt

    def f(k):
        d = _dt.date(2025, 1, 1) + _dt.timedelta(days=k - 1)
        return "{} {}".format(d.day, MONTHS_EN[d.month - 1])
    return f(LEAF_DOY[0]), f(LEAF_DOY[1] - 1)


MONTHS_EN = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December")
ALBEDO = 0.20


def load_env(path):
    """The environment data and a fingerprint of the file's bytes (the cache key of everything computed from it)."""
    if not path:
        return None, None
    try:
        with open(path, "rb") as f:
            raw = f.read()
        return json.loads(raw.decode("utf-8")), _hashlib.sha1(raw).hexdigest()
    except Exception as ex:
        LOG.append("WARNING: environment data could not be read ({}).".format(ex))
        return None, None


# ------------------------------------------------------------ results kept between runs
import hashlib as _hashlib
import pickle as _pickle
import zlib as _zlib_store
# Version of each computation. A change to a method gets a new number, so results computed the old way are never reused.
MV = dict(solids=4, sky=2, shade=5, faces=1, ground=4, noise=6, comfort=5, shelter=3, season=3, core=2, relief=2,
          render=2, blocks=1, sec_geom=6, sec_field=8)     # v24: shade, ground, comfort, sec_field +1 (olive 15 %);
#                                                            v33: comfort +1 (the year's comfortable hours, T8);
#                                                            v47: shade +1 (the July mean day, so a stored shade
#                                                            without it is computed again once)
_MEMSTORE = {}


def fp(*parts):
    """Fingerprint of everything a result depends on (exact: the full repr of the values)."""
    h = _hashlib.sha1()
    for p in parts:
        h.update(repr(p).encode("utf-8"))
        h.update(b"\x1f")
    return h.hexdigest()


class Store(object):
    """Results this script computed before, kept between bakes: in Rhino's memory for this session, and as files in
    Downloads/Bergama/cached/selinus_cache for later sessions (v33 24 Oct; an old "selinus_cache" next to env_path is still read). An entry is found only by the fingerprint of everything it
    was computed from (drawing, frame, data files, settings, method version), so a change anywhere can never pick up
    an old result. Only plain data is stored (lists, numbers, arrays), never live objects."""

    KEEP_IN_MEMORY = 6                                       # recent entries per kind; older ones stay on disk

    def __init__(self):
        mem = _MEMSTORE
        if HAVE_RHINO:
            mem = sc.sticky.get("selinus_store")
            if mem is None:
                mem = sc.sticky["selinus_store"] = {}
        self.mem = mem
        self.order = mem.setdefault("__order__", {})
        base = os.path.dirname(ENV_PATH) if ENV_PATH else ""
        self.dir = SELINUS_CACHE_DIR                         # v33 24 Oct (Aras rule); was beside env_path
        self.old_dir = os.path.join(base, "selinus_cache") if base else None   # old place: read only, as a fallback
        self.hits_mem, self.hits_disk, self.made = [], [], []
        self._made_keys = set()
        self._pruned = False

    def _path(self, kind, key):
        return os.path.join(self.dir, "%s_%s.bin" % (kind, key[:40]))

    def _remember(self, kind, k, val):
        self.mem[k] = val
        lst = self.order.setdefault(kind, [])
        if k in lst:
            lst.remove(k)
        lst.append(k)
        while len(lst) > self.KEEP_IN_MEMORY:
            self.mem.pop(lst.pop(0), None)

    def get(self, kind, key):
        k = kind + ":" + key
        v = self.mem.get(k)
        if v is not None:
            self.hits_mem.append(kind)
            return v
        if self.dir:
            p = self._path(kind, key)
            if not os.path.exists(p) and self.old_dir:
                p = os.path.join(self.old_dir, os.path.basename(p))
            try:
                if os.path.exists(p):
                    with open(p, "rb") as f:
                        stored_key, v = _pickle.loads(_zlib_store.decompress(f.read()))
                    if stored_key == key:
                        try:
                            os.utime(p, None)
                        except Exception:
                            pass
                        self._remember(kind, k, v)
                        (self.hits_mem if k in self._made_keys else self.hits_disk).append(kind)
                        return v
            except Exception:
                pass
        return None

    def has(self, kind, key):
        """v18: whether get would find it (without loading it or counting it as reused)."""
        k = kind + ":" + key
        if self.mem.get(k) is not None:
            return True
        return bool(self.dir) and (os.path.exists(self._path(kind, key)) or bool(self.old_dir) and
                                   os.path.exists(os.path.join(self.old_dir, os.path.basename(self._path(kind, key)))))

    def put(self, kind, key, val, disk=True):
        self._remember(kind, kind + ":" + key, val)
        self._made_keys.add(kind + ":" + key)
        self.made.append(kind)
        if disk and self.dir:
            try:
                if not os.path.isdir(self.dir):
                    os.makedirs(self.dir)
                self.prune()
                p = self._path(kind, key)
                tmp = p + ".part"
                with open(tmp, "wb") as f:
                    f.write(_zlib_store.compress(_pickle.dumps((key, val), protocol=4), 1))
                os.replace(tmp, p)
            except Exception:
                pass
        return val

    def prune(self, max_age_days=45.0, max_bytes=3e9):
        """Keep the cache folder bounded: files unused for 45 days go, then the oldest beyond 3 GB."""
        if self._pruned or not self.dir or not os.path.isdir(self.dir):
            return
        self._pruned = True
        try:
            import time as _t
            now = _t.time()
            files = []
            for nm in os.listdir(self.dir):
                if not (nm.endswith(".bin") or nm.endswith(".part")):
                    continue
                p = os.path.join(self.dir, nm)
                st = os.stat(p)
                files.append((st.st_mtime, st.st_size, p))
            files.sort()
            total = sum(f[1] for f in files)
            for mt, size, p in files:
                if now - mt > max_age_days * 86400.0 or total > max_bytes:
                    os.remove(p)
                    total -= size
        except Exception:
            pass

    def summary(self):
        def cnt(lst):
            d = {}
            for k in lst:
                d[k] = d.get(k, 0) + 1
            return ", ".join("%s %d" % kv if kv[1] > 1 else kv[0] for kv in sorted(d.items()))
        parts = []
        if self.hits_mem:
            parts.append("reused from this session: " + cnt(self.hits_mem))
        if self.hits_disk:
            parts.append("reused from earlier sessions: " + cnt(self.hits_disk))
        if self.made:
            parts.append("computed now: " + cnt(self.made))
        return "; ".join(parts)


def site_prints(S):
    """Fingerprints of what the analyses read from the site; computed once per bake."""
    p = getattr(S, "prints", None)
    if p:
        return p
    p = dict(
        bld=fp([(u["parts"], u["floors"], u["cat"], u["annex"], u["h"]) for u in S.bld]),
        terrain=getattr(S, "terrain_fp", None),
        zones=fp([(z["kind"], z["sub"], z["Ps"], z["Hs"]) for z in S.zones]),
        trees=fp(S.trees[:getattr(S, "n_trees_surveyed", len(S.trees))]),
        frame=fp(S.F.P),
        roads=fp([(r["P"], sorted(r["tags"].items()), r.get("w")) for r in S.roads]),
        water=fp([(w["P"], w.get("H", [])) for w in S.water]),
        stream=fp(getattr(S, "selinus", [])))
    S.prints = p
    return p


def solids_portable(solids, S):
    """Buildings and crowns as plain data (the link to the survey unit kept as its index)."""
    bl, gB, trees = solids
    uidx = dict((id(u), i) for i, u in enumerate(S.bld))
    pb = []
    for b in bl:
        d = dict((k, v) for k, v in b.items() if k != "u")
        d["ui"] = uidx.get(id(b.get("u")), -1)
        pb.append(d)
    return (pb, [dict(t) for t in trees])


def solids_live(port, S):
    pb, trees = port
    bl = []
    for d in pb:
        b = dict(d)
        ui = b.get("ui", -1)
        b["u"] = S.bld[ui] if 0 <= ui < len(S.bld) else None
        bl.append(b)
    g = Grid(25.0)
    for b in bl:
        g.add(b, b["bb"])
    return bl, g, [dict(t) for t in trees]


def lst_seasons(E):
    """Surface temperature per season: the multi-scene means of environment data v2, else v1's single scenes."""
    return E.get("lst_seasons") or E.get("lst", {})


def grid_geom(r):
    """The geometry of an analysis grid, kept with its results (cells, frame, open cells, cell centres)."""
    nx, ny, cell = r["nx"], r["ny"], r["cell"]
    F = Frame(r["frame"])
    u = F.u0 + (np.arange(nx) + 0.5) * cell
    v = F.v0 + (np.arange(ny) + 0.5) * cell
    UU, VV = np.meshgrid(u, v)
    xx, yy = f_world(F, UU.ravel(), VV.ravel())
    return dict(nx=nx, ny=ny, cell=cell, frame=r["frame"], open=r["open"], z=r["z"], xx=xx, yy=yy)


def run_environment(S):
    """The environment analyses, each taken from the store when its inputs are unchanged, otherwise computed and
    stored: buildings and crowns; shade, wind and temperature on the frame (one pass over the sun's positions);
    solar radiation on the focus area; sound."""
    import time as _t
    E, E_fp = load_env(ENV_PATH)
    if E is None:
        LOG.append("WARNING: environment analyses need the data file bergama_environment.json in env_path.")
        S.env = None
        return
    ph = E.get("phenology") or {}
    if ph.get("leaf_on_doy") and ph.get("leaf_off_doy"):
        LEAF_DOY[:] = [int(ph["leaf_on_doy"]), int(ph["leaf_off_doy"])]
    ST = Store()
    S.store = ST
    pr = site_prints(S)
    t0 = _t.time()
    keys = {}
    keys["solids"] = fp("solids", MV["solids"], pr["bld"], pr["terrain"], pr["zones"], pr["trees"], pr["frame"], E_fp)
    port = ST.get("solids", keys["solids"])
    if port is None:
        port = ST.put("solids", keys["solids"], solids_portable(env_solids(S, E), S))
    solids = solids_live(port, S)
    env = dict(E=E, E_fp=E_fp, solids=solids, lst=lst_seasons(E), keys=keys, memo={},
               bindex=dict((id(b), i) for i, b in enumerate(solids[0])), shade=None, comfort=None, rad=None)
    S.env = env
    log = []
    if not HAVE_NP:
        LOG.append("WARNING: the technical analyses need numpy. The line '# r: numpy' at the top of the script makes "
                   "Rhino 8 install it on the first run (internet needed once); then press the button again.")
        S.env = None
        return
    TT = tmy_table(E)
    env["TT"] = TT
    keys["shade"] = fp("shade16", MV["shade"], keys["solids"], SHADE_CELL, SUN_BINS)
    keys["comfort"] = fp("comfort16", MV["comfort"], MV["shelter"], keys["solids"], COMFORT_CELL, SUN_BINS, SKY_BINS,
                         WIND_BINS, hours_window())
    # v17: the sound map starts first, on the worker processes, and runs while Rhino computes shade, comfort and
    # solar radiation on its own threads (the analyses do not depend on each other); it is collected below.
    t_s0 = _t.time()
    keys["noise_raw"] = fp("noise", MV["noise"], keys["solids"], pr["roads"], pr["terrain"], pr["frame"], 10.0,
                           traffic_key(S))
    raw_nm = ST.get("noise", keys["noise_raw"])
    nm_job = noise_map_start(S, solids, cell=10.0, model=noise_model(S)) if raw_nm is None else None
    t_s = _t.time() - t_s0
    sh = ST.get("shade", keys["shade"])
    cf = ST.get("comfort", keys["comfort"]) if TT["full"] else None
    # v16.6: the shade (1 m) and the comfort analyses (2 m) on grids of their own (v16.5: both on one 3 m grid)
    for cell_, want_sh, want_cf in ((SHADE_CELL, sh is None, False), (COMFORT_CELL, False, TT["full"] and cf is None)):
        if want_sh or want_cf:
            r = env16_frame(S, E, solids, S.F, cell_, want_sh, want_cf, log)
            geo = dict(nx=r["nx"], ny=r["ny"], cell=r["cell"], frame=r["frame"], open=r["open"], z=r["z"])
            if want_sh:
                sh = ST.put("shade", keys["shade"], dict(r["shade"], geo=geo))
            if want_cf:
                cf = ST.put("comfort", keys["comfort"], dict(r["comfort"], geo=geo))
            r = None
    env["shade"] = dict(sh, grid=grid_geom(sh["geo"]))
    if cf is not None:
        env["comfort"] = dict(cf, grid=grid_geom(cf["geo"]))
    else:
        LOG.append("WARNING: wind, air and felt temperature need the hourly weather of the typical year (humidity, wind, "
                   "long-wave radiation): environment data version 2. This file has only sun and air temperature, so "
                   "T5-T7 and their sections are skipped.")
    focus = getattr(S, "focus_frame", None) or S.F       # v16.5: the whole frame (v16.4: the densest 420 x 210 m stretch)
    env["focus"] = focus
    keys["focus"] = fp(focus.P)
    keys["rad"] = fp("rad16", MV["ground"], keys["solids"], keys["focus"], 1.5, SUN_BINS, SKY_BINS)
    rd = ST.get("rad", keys["rad"])
    if rd is None:
        rd = ST.put("rad", keys["rad"], env16_focus(S, E, solids, focus, 1.5, log))
    env["rad"] = rd
    t1 = _t.time() - t_s
    if raw_nm is None:
        raw_nm = ST.put("noise", keys["noise_raw"], noise_map_collect(nm_job))
    nm = dict(raw_nm, grid=[[(dict(c) if c else c) for c in row] for row in raw_nm["grid"]])
    dbs = NOISE_DB_PAIRED[:len(NOISE_PTS_SURVEY)]
    off, n = calibrate_noise(S, nm, NOISE_PTS_SURVEY, dbs)
    nm["offset"], nm["n_meas"] = off, n
    keys["noise"] = fp(keys["noise_raw"], NOISE_PTS_SURVEY, dbs)
    env["noise"] = nm
    t2 = _t.time()
    parts = ["{} {:.0f} s".format(nm_, sec) for nm_, n_, sec in log if nm_ in ("sky", "shelter", "sun pass", "dark hours",
                                                                                "focus sky", "focus total", "frame total")]
    try:
        n_all_ = max(1, int(os.cpu_count() or 1))
    except Exception:
        n_all_ = 1
    LOG.append("Cores used: {} of {} (Rhino's threads for shade, comfort and solar; the sound model on worker "
               "processes{}).".format(n_cores(), n_all_, "" if _NOISE_PY.get("py", 1) else ": not available, " +
                                      _NOISE_PY.get("why", "")))
    LOG.append("Environment analyses: {}; {} tree crowns.".format(                 # v27: no step timings
        "computed" if parts else "all reused from the cache", len(solids[2])))


def noise_model(S):
    """The sound model of this bake (road pieces, building grid), shared by the map and every sound section."""
    m = S.env.get("noise_model")
    if m is None:
        m = S.env["noise_model"] = NoiseModel(S, S.env["solids"])
    return m


# ------------------------------------------------------------ sun
def sun_position(y, mo, d, hour_utc, lat, lon):
    """NOAA solar position (Meeus). Returns azimuth (deg from true north, clockwise), apparent elevation (deg)."""
    yy, mm = (y - 1, mo + 12) if mo <= 2 else (y, mo)
    A_ = yy // 100
    jd = int(365.25 * (yy + 4716)) + int(30.6001 * (mm + 1)) + d + (2 - A_ + A_ // 4) - 1524.5 + hour_utc / 24.0
    T = (jd - 2451545.0) / 36525.0
    L0 = (280.46646 + T * (36000.76983 + 0.0003032 * T)) % 360.0
    M = math.radians(357.52911 + T * (35999.05029 - 0.0001537 * T))
    e = 0.016708634 - T * (0.000042037 + 0.0000001267 * T)
    Cc = (math.sin(M) * (1.914602 - T * (0.004817 + 0.000014 * T)) + math.sin(2 * M) * (0.019993 - 0.000101 * T)
          + math.sin(3 * M) * 0.000289)
    om = math.radians(125.04 - 1934.136 * T)
    lam = math.radians(L0 + Cc - 0.00569 - 0.00478 * math.sin(om))
    eps = math.radians(23.0 + (26.0 + (21.448 - T * (46.815 + T * (0.00059 - T * 0.001813))) / 60.0) / 60.0
                       + 0.00256 * math.cos(om))
    dec = math.asin(math.sin(eps) * math.sin(lam))
    yv = math.tan(eps / 2.0) ** 2
    L0r = math.radians(L0)
    eqt = 4.0 * math.degrees(yv * math.sin(2 * L0r) - 2 * e * math.sin(M) + 4 * e * yv * math.sin(M) * math.cos(2 * L0r)
                             - 0.5 * yv * yv * math.sin(4 * L0r) - 1.25 * e * e * math.sin(2 * M))
    ha = math.radians(((hour_utc * 60.0 + eqt + 4.0 * lon) % 1440.0) / 4.0 - 180.0)
    lr = math.radians(lat)
    cz = math.sin(lr) * math.sin(dec) + math.cos(lr) * math.cos(dec) * math.cos(ha)
    zen = math.acos(max(-1.0, min(1.0, cz)))
    el = 90.0 - math.degrees(zen)
    if el > 85.0:
        r = 0.0
    elif el > 5.0:
        te = math.tan(math.radians(el))
        r = 58.1 / te - 0.07 / te ** 3 + 0.000086 / te ** 5
    elif el > -0.575:
        r = 1735.0 + el * (-518.2 + el * (103.4 + el * (-12.79 + el * 0.711)))
    else:
        r = -20.774 / math.tan(math.radians(el))     # v21: NOAA (R04-02)
    sz = math.sin(zen)
    if sz < 1e-9:
        az = 180.0
    else:
        a = math.degrees(math.acos(max(-1.0, min(1.0, (math.sin(lr) * cz - math.sin(dec)) / (math.cos(lr) * sz)))))
        az = (a + 180.0) % 360.0 if ha > 0 else (540.0 - a) % 360.0
    return az, el + r / 3600.0


def dni_extra(doy):
    b = 2.0 * math.pi * (doy - 1) / 365.0                   # v21: Spencer, day 0 = 1 January (R04-16)
    return 1366.1 * (1.00011 + 0.034221 * math.cos(b) + 0.00128 * math.sin(b) + 0.000719 * math.cos(2 * b)
                     + 0.000077 * math.sin(2 * b))


def airmass_ky(zen_deg):
    if zen_deg >= 90.0:
        return None
    return 1.0 / (math.cos(math.radians(zen_deg)) + 0.50572 * (96.07995 - zen_deg) ** -1.6364)


PEREZ_F1 = [(-0.008, 0.588, -0.062), (0.13, 0.683, -0.151), (0.33, 0.487, -0.221), (0.568, 0.187, -0.295),
            (0.873, -0.392, -0.362), (1.132, -1.237, -0.412), (1.06, -1.6, -0.359), (0.678, -0.327, -0.25)]
PEREZ_F2 = [(-0.06, 0.072, -0.022), (-0.019, 0.066, -0.029), (0.055, -0.064, -0.026), (0.109, -0.152, -0.014),
            (0.226, -0.462, 0.001), (0.288, -0.823, 0.056), (0.264, -1.127, 0.131), (0.156, -1.377, 0.251)]
PEREZ_EPS = (1.065, 1.23, 1.5, 1.95, 2.8, 4.5, 6.2)


def perez_f(dhi, dni, zen_deg, doy):
    """Perez et al. 1990 circumsolar (F1) and horizon (F2) brightness coefficients."""
    am = airmass_ky(zen_deg)
    if dhi <= 0.0 or am is None:
        return 0.0, 0.0
    z = math.radians(zen_deg)
    k = 1.041 * z ** 3
    eps = ((dhi + dni) / dhi + k) / (1.0 + k)
    delta = dhi * am / dni_extra(doy)
    b = sum(1 for t in PEREZ_EPS if eps >= t)
    c1, c2 = PEREZ_F1[b], PEREZ_F2[b]
    return max(0.0, c1[0] + c1[1] * delta + c1[2] * z), c2[0] + c2[1] * delta + c2[2] * z


class Compass(object):
    """True north and east as unit vectors in survey coordinates (meridian convergence and survey rotation)."""

    def __init__(self, lon, lat):
        a, b = to_dwg(lon, lat), to_dwg(lon, lat + 0.002)
        L_ = math.hypot(b[0] - a[0], b[1] - a[1])
        self.N = ((b[0] - a[0]) / L_, (b[1] - a[1]) / L_)
        self.E = (self.N[1], -self.N[0])

    def vec(self, az):
        r = math.radians(az)
        return (math.sin(r) * self.E[0] + math.cos(r) * self.N[0], math.sin(r) * self.E[1] + math.cos(r) * self.N[1])

    def az(self, dx, dy):
        return math.degrees(math.atan2(dx * self.E[0] + dy * self.E[1], dx * self.N[0] + dy * self.N[1])) % 360.0


class Horizons(object):
    """Terrain horizon (DEM) profiles; each point of the site uses the nearest profile."""

    def __init__(self, hz):
        self.P = [(h["x"], h["y"]) for h in hz]
        self.H = [h["h"] for h in hz]
        self.step = hz[0]["step"] if hz else 7.5

    def nearest(self, x, y):
        if not self.P:
            return None
        d = [(p[0] - x) ** 2 + (p[1] - y) ** 2 for p in self.P]    # same distances, first minimum as before
        return min(range(len(d)), key=d.__getitem__)

    def h(self, i, az):
        if i is None:
            return 0.0
        prof = self.H[i]
        f = (az % 360.0) / self.step
        k = int(f) % len(prof)
        t = f - int(f)
        return prof[k] * (1 - t) + prof[(k + 1) % len(prof)] * t


def env_solids(S, E=None):
    """Surveyed buildings as prisms (their height u["h"] on terrain: floors x storey height, or a published height)
    and trees as 3D crowns measured on the 1 m canopy height map (a surveyed tree symbol carries no size, so it
    is not modelled). Leaf type: measured per crown in environment data v2 (CLC+ Backbone 2021 / Sentinel-2),
    else from the survey's land-use zones (wood: needle-leaved, orchard: evergreen broadleaf, else deciduous)."""
    bl = []
    for u in S.bld:
        H = u["h"]
        if H <= 0.0:
            continue
        holes = u.get("holes") or []
        for P in u["parts"]:
            a, cx, cy = shoelace(P)
            if abs(a) < 2.0:
                continue
            Q = ccw(P)                                                # counter-clockwise
            hs = [list(reversed(ccw(h))) for h in holes if pip(interior_point(h)[0], interior_point(h)[1], Q)]
            base = S.z_at(cx, cy)
            bl.append(dict(P=Q, H=H, base=base, top=base + H, bb=bb_pts(Q), cx=cx, cy=cy, u=u, holes=hs))
    g = Grid(25.0)
    for b in bl:
        g.add(b, b["bb"])
    woods = [z for z in S.zones if (z["kind"] == "green" and z["sub"] in ("wood", "forest")) or z["sub"] == "forest"]
    orch = [z for z in S.zones if z["kind"] == "agri" and z["sub"] == "orchard"]

    def leaf_kind(x, y):
        for zs, kind in ((woods, "pine"), (orch, "olive")):
            for z in zs:
                if bb_hit(z["bb"], (x, y, x, y)) and any(pip(x, y, P) for P in z["Ps"]):
                    return kind
        return "tree"
    fb = S.F.bb
    fbx = (fb[0] - 80, fb[1] - 80, fb[2] + 80, fb[3] + 80)
    trees = []
    gT = Grid(10.0)
    for row in (E or {}).get("trees", []):
        x, y, r, h = row[:4]
        if not (fbx[0] <= x <= fbx[2] and fbx[1] <= y <= fbx[3]) or h < 3.0:
            continue
        uu, vv = S.F.local(x, y)
        if not (S.F.u0 - 60 <= uu <= S.F.u1 + 60 and S.F.v0 - 60 <= vv <= S.F.v1 + 60):
            continue
        if any(pip(x, y, b["P"]) for b in g.query((x, y, x, y))):
            continue                                                  # a crown on a roof is a misreading
        if len(row) > 5:
            kind, lsrc = LEAF_KIND.get(int(row[4]), "tree"), int(row[5])
        else:
            kind, lsrc = leaf_kind(x, y), 0
        t = dict(x=x, y=y, r=r, lo=max(1.5, 0.35 * h), hi=h, kind=kind, leaf_src=lsrc, base=S.z_at(x, y), src="canopy map")
        trees.append(t)
        gT.add(t, (x, y, x, y))
    return bl, g, trees


def convex_parts(P):
    """Split a footprint into convex pieces (ear clipping, merged greedily) so shadows stay exact."""
    a, _, _ = shoelace(P)
    if abs(convex_hull(P) and shoelace(convex_hull(P))[0]) <= abs(a) * 1.03:
        return [P]
    V = list(P)
    tris = []
    guard = 0
    while len(V) > 3 and guard < 500:
        guard += 1
        n = len(V)
        for i in range(n):
            p0, p1, p2 = V[i - 1], V[i], V[(i + 1) % n]
            if (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p1[1] - p0[1]) * (p2[0] - p0[0]) <= 0:
                continue
            if any(pip(q[0], q[1], [p0, p1, p2]) for q in V if q not in (p0, p1, p2)):
                continue
            tris.append([p0, p1, p2])
            del V[i]
            break
        else:
            break
    if len(V) == 3:
        tris.append(V)
    return tris or [P]


# ------------------------------------------------------------ shade: hours in shade on the season's key day
def raster_rows(L_, F, cell, nx, ny):
    """Scanline a convex polygon given in frame-local coordinates: [(row, first cell, end cell)]."""
    n = len(L_)
    if n < 3:
        return []
    u0, v0 = F.u0, F.v0
    ys = [p[1] for p in L_]
    ymin, ymax = min(ys), max(ys)
    j0 = max(0, int(math.ceil((ymin - v0) / cell - 0.5)))
    j1 = min(ny - 1, int(math.floor((ymax - v0) / cell - 0.5)))
    if j1 < j0:
        return []
    edges = []
    for k in range(n):
        (x0, y0), (x1, y1) = L_[k], L_[(k + 1) % n]
        if y0 != y1:
            if y0 > y1:
                x0, y0, x1, y1 = x1, y1, x0, y0
            edges.append((y0, y1, x0, (x1 - x0) / (y1 - y0)))
    out = []
    ceil, floor = math.ceil, math.floor
    for j in range(j0, j1 + 1):
        yc = v0 + (j + 0.5) * cell
        lo = hi = None
        for y0, y1, x0, sl in edges:
            if y0 <= yc < y1:
                x = x0 + (yc - y0) * sl
                if lo is None or x < lo:
                    lo = x
                if hi is None or x > hi:
                    hi = x
        if lo is not None:
            a0 = max(0, int(ceil((lo - u0) / cell - 0.5)))
            a1 = min(nx, int(floor((hi - u0) / cell - 0.5)) + 1)
            if a1 > a0:
                out.append((j, a0, a1))
    return out


# ------------------------------------------------------------ sound: RLS-90 emission and segment method, VBUS period shares, Lden
# v16.3: EVERY street carries traffic. Where KGM (General Directorate of Highways) counted a road, its count is used as
# before; every other street takes a correlated estimate, labelled as such on every sheet:
#   1. the default flow of its street type from the European Commission's noise-mapping guidance: WG-AEN "Good Practice
#      Guide for Strategic Noise Mapping and the Production of Associated Data on Noise Exposure", version 2 (13 January
#      2006), Toolkit 2, Tool 2.5 (default flows by road type), with the OSM street types mapped to its road categories as
#      the open-source NoiseModelling software (Universite Gustave Eiffel / Cerema; Import_OSM.groovy, class Road,
#      release 4.0.5) does it: GPG_FLOWS below;
#   2. the correlation the KGM counts give for that street type here: factor k = counted AADT / GPG default daily flow
#      of the counted road's own type, taken from the nearest counted road of the SAME street type (a street type
#      with no count in reach keeps k = 1, the plain GPG default, and says so);
#   3. flow = k x the GPG default in each period (day 12 h, evening 4 h, night 8 h); the heavy share is the counted
#      road's KGM printed truck share (p_kgm, daily) where a count of the same type exists, else the GPG default share
#      of each period. (v22: the counted roads themselves use p over 3.5 t; the correlated streets keep p_kgm, so the
#      group's estimate for the streets without a count is unchanged.)
# A one-way OSM way (a dual carriageway is mapped as two of them) carries half the two-way flow, as NoiseModelling does.
# k in dB: 10 lg k (k = 1.54 is +1.9 dB on the GPG default). Nothing here is measured on the street itself: the sheets
# list every street type with its k, its source count and its km in the frame.
# The counts (two-way AADT, vehicles/day). p = the RLS-90 / VBUS heavy share (VBUS Table 1: Lkw over 3.5 t
# permissible gross weight) from KGM's class columns of the same row: OYTT + bus + truck + articulated over the total
# (v22, Aras's choice; R01-02; OYTT, about 3.5-10 t trucks and 14-25-seat buses, counted as heavy is an assumption).
# p_kgm = KGM's own printed heavy share, trucks and articulated trucks only (KGM 2022, pp. 3 and 9), kept for the
# correlated streets. Class counts car / OYTT / bus / truck / articulated:
#   35-04 section 1  KGM 2023 provincial roads, "KINIK (240-01) D.Y.AYR. (BERGAMA) - KOZAK", 21 km, OTSS1: 3,087,
#                    2,548 / 273 / 8 / 149 / 109 -> p 17.46 %, p_kgm 8 %  (project copy il23.txt line 2666)
#   35-05 section 3  KGM 2023 provincial roads, "GOCBEYLI (35-07) IL Y.AYR. - (BERGAMA-KINIK)(240-01) D.Y.AYR.", 5 km,
#                    OTSS1: 4,069, 3,445 / 363 / 1 / 217 / 43 -> p 15.34 %, p_kgm 6 %  (il23.txt line 2674)
#   240-01 section 1 KGM 2024 state roads (2. Bolge, Izmir), 8 km, OTSS1: 22,053,
#                    17,462 / 1,914 / 283 / 1,053 / 1,341 -> p 20.82 %, p_kgm 11 %  (KGM 2024 Bolge2.pdf map box)
#   240-01 section 2 KGM 2024 state roads (2. Bolge, Izmir), 2 km, OTSS1: 14,490,
#                    11,363 / 1,168 / 50 / 638 / 1,271 -> p 21.58 %, p_kgm 13 %  (same map)
#   240-01 section 3 KGM 2024 state roads (2. Bolge, Izmir), 16 km, OTSS3: 13,683,
#                    10,756 / 816 / 59 / 628 / 1,424 -> p 21.39 %, p_kgm 15 %  (same map)
# Which OSM way is which 240-01 section (KGM's report text gives no section ends; worked out from its own figures):
#   * KGM's section map shows section 1 as 3 + 5 km from the D550 (550-08) junction west of Bergama, section 2 (2 km)
#     ending where 35-05 joins ("(BERGAMA-KINIK)(240-01) D.Y.AYR.", KGM 2023), section 3 (16 km) on to Kinik.
#   * OSM: 35-05 starts at the roundabout where "Bergama Cevre Yolu" (the ring road, 6.85 km from the west end of the
#     extract) ends and "Akhisar - Bergama Yolu" begins, so Akhisar - Bergama Yolu is SECTION 3. On the ring road an
#     interchange (links to the town) lies 2.1-2.6 km before that roundabout and 4.2-4.8 km from the extract's west end,
#     about 3 km short of the D550 junction: the 3 + 5 / 2 km split; the ring road is cut there (KGM_SPLIT) into
#     section 1 (west) and section 2 (east).
#   * KGM's own speeds rule out the parallel route through the town (Ataturk and Adnan Menderes Bulvari, OSM primary,
#     50-70 km/h): cars on sections 1 and 2 average 67 km/h, 85th percentile 82 and 80 km/h, with 1 % and 4 % over the
#     limit; the OSM ring road is signed 110 km/h.
COUNTED = {
    "35-04": [dict(aadt=3087.0, p=100.0 * 539 / 3087, p_kgm=8.0,
                   src="KGM 2023, 35-04 section 1: 3,087 veh/day, 17.5 % over 3.5 t (KGM trucks + articulated 8 %) (OTSS1)")],
    "35-05": [dict(aadt=4069.0, p=100.0 * 624 / 4069, p_kgm=6.0,
                   src="KGM 2023, 35-05 section 3: 4,069 veh/day, 15.3 % over 3.5 t (KGM trucks + articulated 6 %) (OTSS1)")],
    "D240": [dict(aadt=22053.0, p=100.0 * 4591 / 22053, p_kgm=11.0, name="Bergama Çevre Yolu", section="1",
                  src="KGM 2024, 240-01 section 1: 22,053 veh/day, 20.8 % over 3.5 t (KGM trucks + articulated 11 %) (OTSS1)"),
             dict(aadt=14490.0, p=100.0 * 3127 / 14490, p_kgm=13.0, name="Bergama Çevre Yolu", section="2",
                  src="KGM 2024, 240-01 section 2: 14,490 veh/day, 21.6 % over 3.5 t (KGM trucks + articulated 13 %) (OTSS1)"),
             dict(aadt=13683.0, p=100.0 * 2927 / 13683, p_kgm=15.0, name="Akhisar - Bergama Yolu",
                  src="KGM 2024, 240-01 section 3: 13,683 veh/day, 21.4 % over 3.5 t (KGM trucks + articulated 15 %) (OTSS3)")],
}
# The ring road's cut between 240-01 sections 1 and 2: the interchange's two ramp nodes on the eastbound carriageway
# (OSM nodes at 27.1956573 E 39.0986022 N and 27.2004928 E 39.1020103 N; the cut is the line through their midpoint,
# square to the road between them). Section 1 lies on the west side of it, section 2 on the east.
KGM_SPLIT = {"Bergama Çevre Yolu": ((27.1956573, 39.0986022), (27.2004928, 39.1020103), "1", "2")}


