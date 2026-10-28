# ---- MIRAQUA round 28 Oct 2026 (site board v50): p.06/p.22 the stream edge and where we can build, p.16 shade strip, P06.3, the open-to-change export (worker SB-edge). Shared pieces: parts/15h_r28_shared.py,
# common/r28_style.py, common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v50 (MIRAQUA 28 Oct, P06.1-P06.4, P22.1, D1, G3-G8, G13; worker SB-edge). Every drawing here is ONE strip of the
# whole analysis frame at 1:10,000 on the booklet page, on the frame's own axis (G7: 284.5 x 52.9 mm; 1:5,000 would
# need 569 mm), with the study area's outline (G8) and its scale bar and north arrow under it, never on it:
#   * p.06 drw_edge_build: the strip; THE EDGE and WHERE WE CAN BUILD beside it; the map's key under it (it holds the
#     hatches and outlined fills the booklet's legend cannot draw); the eight photos in the height the second strip
#     left (P06.4). p.22 drw_edge_build_e: the same strip without photos (P22.1).
#   * P06.1 context: street names (OpenStreetMap: the main streets first, then the longest named), mahalle names
#     (OpenStreetMap boundary=administrative, admin_level 8), heritage names (the buildings' own names, then named
#     heritage points), bridge names (BRIDGES_K), the survey's 5 m contours (10 m bolder), the study area; placed by
#     common/label_place.py (G4): bridge and stream names always, the others dropped where nothing is free (logged).
#   * P06.2 where we can build: vector hatches in R28_BUILD_HATCH over a light tint of their colour; the loose ground
#     is drawn from the very cells frame_rest counts (S.rest_rows), traced into outlines, simplified (Douglas-Peucker),
#     smoothed (Chaikin) and scaled back to the traced area; the satellite trees and fields are smoothed the same way.
#     Every printed area still comes from the count (ground_open): the drawing moves no figure.
#   * P06.3: buildings in R28E_BLD, darker than the streets, filled by the nonzero rule (r28_nz: overlapping outlines
#     no longer print white); OpenStreetMap footprints with a thin outline; both in the key.
#   * D1: r28_open_to_change.json (r28e_export_open) and the filter sheet drw_filter (r28e_draw_filter): analysis frame
#     -> open ground (the masterplan's r28_open_ground.json) -> of which open to change, and why.
#   * p.16 drw_shade_strip (draw_shade_strip): its rows laid along the frame's axis at 1:10,000, the study area marked.
# Labels and notes are measured with r28mv_tw and set with r28mv_lines / r28mv_para (parts/15i_r28_movement.py).
R28E_DEN = B_DEN                 # 1:10,000 on the booklet page (the theme-B maps' scale)
R28E_SB_M = B_SB_M               # m: the scale bar under each strip, four parts of 100 m
R28E_GAP = BK_GAP_MM             # mm between a strip and the column beside it
R28E_BLD = mix(MPL["bld"], C(R28_OPEN["building"]), 0.45)   # P06.3: A7A299, dE00 about 11 to the streets (was 2.3)
R28E_OSM_EDGE = mix(R28E_BLD, INK, 0.6)                    # P06.3: the thin outline of an OpenStreetMap footprint
R28E_HER_TXT = C(dict((k_, h_) for k_, n_, h_ in R28_MARKERS)["heritage"])   # heritage names (R28 "heritage and views")
R28E_CONTOUR = mix(INK2, WHITE, 0.5)                       # P06.1: contours, light (G6)
R28E_CONTOUR_W = (0.07, 0.13)    # mm: a 5 m and a 10 m contour on the booklet page
R28E_DP_M = (4.0, 2.0)           # m: Douglas-Peucker tolerances tried in turn on a raster outline (steps of 2-10 m) ...
R28E_DP_FINE = 0.3               # m: ... and once more after the corner cutting (fewer points, the same curve)
R28E_CHAIKIN = 2                 # corner-cutting rounds
R28E_SHAPE = 0.25                # the most a ring's area may change before it is scaled back (else the next tolerance)
R28E_MIN_A = 30.0                # m2: smaller rings stay as traced (0.5 mm across at 1:10,000)
R28E_TINT = 0.86                 # a hatch's ground: its line colour this far to white (G6: light)
R28E_HATCH_MM = (1.0, 0.12)      # mm: hatch spacing and line weight on the booklet page
R28E_HATCH = dict((k_, (lab_, C(hx_), ang_)) for k_, lab_, hx_, ang_ in R28_BUILD_HATCH)
R28E_KEYS = (("vacant", "open"), ("parking", "parking"), ("loose", "loose"))   # ground_open's parts -> hatch keys
R28E_N_HER, R28E_N_STREET = 8, 6     # heritage and street names at most (G4 may drop some of them)
R28E_STREET_MIN = 150.0          # m: a named street runs at least this far inside the frame
R28E_MAH_MIN = 20000.0           # m2: a mahalle named on the strip has at least this much ground inside the frame
R28E_OPEN_JSON = os.path.join(SELINUS_RES_DIR, "r28_open_to_change.json")    # D1: the polygons and figures p.06 prints
R28E_MP_JSON = "r28_open_ground.json"    # D1: the masterplan's open ground, next to its masterplan_results.json


class R28NZ(tuple):
    """v50 (MIRAQUA 28 Oct, P06.3): a fill colour the PDF fills by the nonzero winding rule (_pdf_page: "f", not
    "f*"): overlapping building outlines stay filled (even-odd printed their overlap white); courtyards turn the other
    way round (add_unit in 03_street_w.py) and stay open. Rhino bakes it as the plain colour."""
    nz = True


class R28NZTint(Tint):
    """v50 (P06.3): a multiplying Tint (15f) filled by the nonzero rule"""
    nz = True


def r28_nz(c):
    """v50 (P06.3): colour c filled by the nonzero rule (a Tint stays a multiplying Tint)"""
    if getattr(c, "nz", False):
        return c
    return R28NZTint(c) if getattr(c, "mul", False) else R28NZ(c)


def r28e_memo(S):
    """the run's memo of this part (traced and smoothed outlines, names, the export), kept on the site model"""
    m = getattr(S, "_r28e", None)
    if m is None:
        m = S._r28e = {}
    return m


def r28e_rich(B, s, x, y, h, col, L, order=40):
    """G5: one line with **bold** runs from baseline y; returns its width"""
    ln = r28mv_lines(s, 1e12, h)
    return r28mv_draw_line(B, ln[0], x, y, h, col, L, order) if ln else 0.0


# ------------------------------------------------------------ P06.2: raster outlines as smooth vector rings
def r28e_dp_ring(P, tol):
    """Douglas-Peucker on a closed ring: cut at its first point and the point farthest from it, both kept"""
    n = len(P)
    if n < 4:
        return list(P)
    x0, y0 = P[0]
    j = max(range(n), key=lambda i: (P[i][0] - x0) ** 2 + (P[i][1] - y0) ** 2)
    if j == 0:
        return list(P)
    return dp_simplify(P[:j + 1], tol)[:-1] + dp_simplify(P[j:] + [P[0]], tol)[:-1]


def r28e_smooth(P):
    """P06.2: a raster outline as a smooth vector ring: Douglas-Peucker (the first tolerance of R28E_DP_M that keeps
    the area within R28E_SHAPE), Chaikin corner cutting (R28E_CHAIKIN rounds), Douglas-Peucker once more
    (R28E_DP_FINE), then scaled about its centroid back to the area it had (holes too, so drawing and count agree);
    rings under R28E_MIN_A stay as they are"""
    P = [(float(p[0]), float(p[1])) for p in P]
    if len(P) > 3 and P[0] == P[-1]:
        P = P[:-1]
    A0 = signed_area(P)
    if len(P) < 4 or abs(A0) < R28E_MIN_A:
        return P
    for tol in R28E_DP_M:
        Q = r28e_dp_ring(P, tol)
        if len(Q) < 3:
            continue
        Q = r28e_dp_ring(chaikin_closed(Q, R28E_CHAIKIN), R28E_DP_FINE)
        A1 = signed_area(Q) if len(Q) >= 3 else 0.0
        if A1 * A0 <= 0.0 or abs(A1 / A0 - 1.0) > R28E_SHAPE:
            continue
        a_, cx, cy = shoelace(Q)
        f = math.sqrt(A0 / A1)
        return [(cx + (x - cx) * f, cy + (y - cy) * f) for x, y in Q]
    return P


def _r28e_turn(d, e):
    """the turn from direction d to direction e on the cell grid: 0 left, 1 straight on, 2 right, 3 back"""
    if e == (-d[1], d[0]):
        return 0
    if e == d:
        return 1
    if e == (d[1], -d[0]):
        return 2
    return 3


def r28e_trace(rows):
    """P06.2: the outlines of a raster mask (rows of bits as frame_rest's: bit a of row j = cell a, j) in cell
    corners (a, j): outer rings anticlockwise, holes clockwise; cells that touch only at a corner make separate
    rings (the left turn first where two outlines meet in a point); straight-through corners left out"""
    out = {}
    ny = len(rows)
    for j in range(ny):
        m = rows[j]
        if not m:
            continue
        below = rows[j - 1] if j > 0 else 0
        above = rows[j + 1] if j + 1 < ny else 0
        for bits, kind in ((m & ~below, 0), (m & ~above, 1), (m & ~(m >> 1), 2), (m & ~(m << 1), 3)):
            while bits:
                b = bits & -bits
                a = b.bit_length() - 1
                bits ^= b
                if kind == 0:                             # bottom side, eastwards (the cell on the left)
                    s, e = (a, j), (a + 1, j)
                elif kind == 1:                           # top side, westwards
                    s, e = (a + 1, j + 1), (a, j + 1)
                elif kind == 2:                           # right side, northwards
                    s, e = (a + 1, j), (a + 1, j + 1)
                else:                                     # left side, southwards
                    s, e = (a, j + 1), (a, j)
                out.setdefault(s, []).append(e)
    rings = []
    while out:
        s0 = next(iter(out))
        lst = out[s0]
        e = lst.pop()
        if not lst:
            del out[s0]
        ring, prev, cur = [s0], s0, e
        while cur != s0:
            ring.append(cur)
            lst = out.get(cur)
            if not lst:                                   # never expected: every corner has as many ways in as out
                break
            d = (cur[0] - prev[0], cur[1] - prev[1])
            nxt = lst[0] if len(lst) == 1 else min(lst, key=lambda q: _r28e_turn(d, (q[0] - cur[0], q[1] - cur[1])))
            lst.remove(nxt)
            if not lst:
                del out[cur]
            prev, cur = cur, nxt
        n = len(ring)
        keep = [ring[i] for i in range(n)
                if (ring[i][0] - ring[i - 1][0]) * (ring[(i + 1) % n][1] - ring[i][1]) !=
                (ring[i][1] - ring[i - 1][1]) * (ring[(i + 1) % n][0] - ring[i][0])]
        if len(keep) >= 4:
            rings.append(keep)
    return rings


def r28e_groups(rings):
    """outer rings (anticlockwise) each with the holes (clockwise) inside it: [[outer, hole, ...], ...], so that a
    fill or hatch drawn group by group never loses a hole"""
    outs, hols = [], []
    for P in rings:
        a_ = signed_area(P)
        if a_ > 0.0:
            outs.append((a_, P))
        elif a_ < 0.0:
            hols.append(P)
    grp = [[P] for a_, P in outs]
    if hols and outs:
        g = Grid(60.0)
        for i, (a_, P) in enumerate(outs):
            g.add(i, bb_pts(P))
        for H in hols:
            x, y = interior_point(H)
            best = None
            for i in g.query((x, y, x, y)):
                if (best is None or outs[i][0] < outs[best][0]) and pip(x, y, outs[i][1]):
                    best = i
            if best is not None:
                grp[best].append(H)
    return grp


def r28e_lc(S, key):
    """P06.2: a satellite class (S.lc[key]: WorldCover 10 m pixel outlines) smoothed (r28e_smooth) and grouped"""
    m = r28e_memo(S)
    if ("lc", key) not in m:
        m[("lc", key)] = r28e_groups([r28e_smooth(P) for P in (getattr(S, "lc", None) or {}).get(key) or []])
    return m[("lc", key)]


def r28e_loose(S):
    """P06.2: the loose ground as frame_rest counts it (grass or shrub cells of the frame's unmapped ground on the
    REST_CELL raster, S.rest_rows) as smooth outlines, grouped: [[outer, holes ...], ...] in survey m"""
    m = r28e_memo(S)
    if "loose" in m:
        return m["loose"]
    rr = getattr(S, "rest_rows", None) or {}
    g_, s_ = rr.get("grass") or [], rr.get("shrub") or []
    mask = [(g_[j] if j < len(g_) else 0) | (s_[j] if j < len(s_) else 0) for j in range(max(len(g_), len(s_)))]
    F, c = S.F, REST_CELL
    raw = [[F.world(F.u0 + a * c, F.v0 + j * c) for a, j in R_] for R_ in r28e_trace(mask)]
    sm = [r28e_smooth(P) for P in raw]
    m["loose"] = r28e_groups(sm)
    LOG.append(u"Where we can build (P06.2): the loose ground's {:,} raster cells traced into {:,} outlines ({:.2f} ha "
               u"traced, {:.2f} ha drawn after smoothing); the figure printed is the count, {:.2f} ha.".format(
                   sum(bin(r_).count("1") for r_ in mask), len(raw), sum(signed_area(P) for P in raw) / 1e4,
                   sum(signed_area(P) for P in sm) / 1e4, rest_of(S, "grass", "shrub") / 1e4))
    return m["loose"]


def r28e_open_groups(S):
    """P06.2: the ground open to change as drawn, by ground_open's parts: {"vacant", "parking": the mapped zones
    (outlines with their holes), "loose": r28e_loose}"""
    m = r28e_memo(S)
    if "open" not in m:
        m["open"] = {"vacant": [z["Ps"] + z["Hs"] for z in S.zones if z["kind"] == "vacant"],
                     "parking": [z["Ps"] + z["Hs"] for z in S.zones if z["kind"] == "transport"],
                     "loose": r28e_loose(S)}
    return m["open"]


def r28e_hatched(CB, V, groups, key, k, L, order, fill=True):
    """P06.2: one part of where we can build (key of R28_BUILD_HATCH): the light tint of its colour (fill=False:
    none) and its hatch, R28E_HATCH_MM apart and wide on the booklet page at its angle (vector lines), group by group"""
    lab, col, ang = R28E_HATCH[key]
    chunk = []
    for i, g in enumerate(groups):
        chunk.extend(g)
        if len(chunk) >= 400 or i == len(groups) - 1:
            Ps = V.Ps(chunk)
            if fill:
                CB.fill(Ps, mix(col, WHITE, R28E_TINT), L, order)
            CB.hatch(Ps, col, L, order + 1, R28E_HATCH_MM[0] * k, math.radians(ang), bk_lw(R28E_HATCH_MM[1], k))
            chunk = []


# ------------------------------------------------------------ P06.1: contours and names
def r28e_contours(R, F):
    """P06.1 (called by build_site, so kept with the site model): the survey's contours inside the frame,
    [(10 m line, polyline)], every 5 m, simplified to 0.5 m. A line's height = the median of its points' heights; a
    line without heights counts by its layer (EGRI_10M, EGRI_5M); other heights are left out."""
    out = []
    for lay in DWG["contours"]:
        for P in (R.get("plines") or {}).get(lay, []):
            if len(P) < 2:
                continue
            zs = sorted(p[2] for p in P)
            z = zs[len(zs) // 2]
            if z > 0.5:
                if abs(z / 5.0 - round(z / 5.0)) > 0.01:
                    continue
                major = abs(z / 10.0 - round(z / 10.0)) < 0.006
            elif lay in ("EGRI_10M", "EGRI_5M"):
                major = lay == "EGRI_10M"
            else:
                continue
            for run in F.clip_line([(p[0], p[1]) for p in P]):
                out.append((major, dp_simplify(run, 0.5)))
    return out


def r28e_streets(S):
    """P06.1: the named streets of the strip (OpenStreetMap names of S.roads): those with a main-road class
    (MAIN_ROADS) first, then the longest, each R28E_STREET_MIN or more inside the frame, at most R28E_N_STREET:
    [(name, x, y)] at the middle of its longest piece"""
    by = {}
    for r_ in S.roads:
        t = r_.get("tags") or {}
        nm = u" ".join((t.get("name") or u"").split())
        if not nm or r_.get("L", 0.0) <= 0.0 or len(r_["P"]) < 2:
            continue
        e = by.setdefault(nm, dict(L=0.0, main=False, best=None))
        e["L"] += r_["L"]
        e["main"] = e["main"] or t.get("highway") in MAIN_ROADS
        if e["best"] is None or r_["L"] > e["best"]["L"]:
            e["best"] = r_
    names = sorted((nm for nm, e in by.items() if e["L"] >= R28E_STREET_MIN),
                   key=lambda nm: (not by[nm]["main"], -by[nm]["L"]))
    out = []
    for nm in names[:R28E_N_STREET]:
        P = by[nm]["best"]["P"]
        q = pl_point_at(P, 0.5 * pl_length(P))[0]
        out.append((nm, q[0], q[1]))
    return out


def r28e_heritage(S):
    """P06.1: the heritage names of the strip: the monuments' and sacred buildings' own names (u["proper"]: survey or
    OpenStreetMap), the largest first, then named heritage points (OpenStreetMap, places) standing free; one label a
    place (a name, or the same first word within 60 m, once), at most R28E_N_HER: [(name, x, y)]"""
    F = S.F
    cand = sorted([(u["A"], u["proper"], interior_point(u["parts"][0])) for u in S.bld
                   if u.get("fabric") in ("monument", "sacred") and u.get("proper")], key=lambda c_: -c_[0])
    cand += [(0.0, p_["name"], (p_["x"], p_["y"])) for p_ in getattr(S, "pois", None) or []
             if p_.get("her") and not p_.get("in_bld") and proper_name(p_.get("name") or u"")]
    out = []
    for a_, nm, (x_, y_) in cand:
        nm = u" ".join(nm.split())
        w0 = nm.split()[0].lower()
        if not F.inside(x_, y_) or any(nm == o[0] or (o[0].split()[0].lower() == w0 and
                                                      math.hypot(o[1] - x_, o[2] - y_) < 60.0) for o in out):
            continue
        out.append((nm, x_, y_))
        if len(out) >= R28E_N_HER:
            break
    return out


def r28e_mahalle(S):
    """P06.1: the mahalle names of the strip: OpenStreetMap boundary=administrative, admin_level 8 relations (their
    outer ways joined into closed rings, cut to the frame), each named at an inside point of its largest piece in the
    frame when that holds R28E_MAH_MIN or more: [(name without "Mahallesi", x, y)]"""
    m = r28e_memo(S)
    if "mahalle" in m:
        return m["mahalle"]
    out, F = [], S.F
    osm = getattr(S, "osm", None) or {}
    ways, Pj = osm.get("ways") or {}, osm.get("P")
    for mem, tags in osm.get("rels") or []:
        nm = u" ".join((tags.get("name") or u"").split())
        if tags.get("boundary") != "administrative" or str(tags.get("admin_level")) != "8" or not nm or Pj is None:
            continue
        lines_ = []
        for ref, role in mem:
            if role in ("outer", "", None) and ref in ways:
                pts = [q for q in (Pj(n_) for n_ in ways[ref][0]) if q]
                if len(pts) >= 2:
                    lines_.append(pts)
        best = None
        for R_ in chain_segments(lines_, 0.05):
            if len(R_) < 4 or math.hypot(R_[0][0] - R_[-1][0], R_[0][1] - R_[-1][1]) > 1.0:
                continue
            Q = F.clip_poly(R_[:-1])
            a_ = shoelace(Q)[0] if Q else 0.0
            if a_ >= R28E_MAH_MIN and (best is None or a_ > best[0]):
                best = (a_, Q)
        if best is not None:
            for suf in (u" Mahallesi", u" Mahalle"):
                if nm.endswith(suf):
                    nm = nm[:-len(suf)].strip()
            x_, y_ = interior_point(best[1])
            out.append((nm, x_, y_))
    m["mahalle"] = out
    LOG.append(u"Mahalle names on the stream edge plan (OpenStreetMap, admin_level 8): {}.".format(
        u", ".join(nm for nm, x_, y_ in out) or u"none (no closed boundary with 2 ha or more in the frame)"))
    return out


def r28e_names(S, V, k):
    """P06.1: the strip's context names as r28e_place items, 7 pt: the stream (always shown), heritage, main
    streets, mahalle (each may be dropped where nothing is free)"""
    F = S.F
    h = bk_hk(7.0, k)
    out = []
    rl = getattr(S, "river_label", None)
    if rl and F.inside(rl[0], rl[1]):
        px, py = V.p(rl[0], rl[1])
        out.append(dict(x=px, y=py, lines=[(rl[3], False)], h=h, col=MPL["water_edge"], rank=0, italic=True))
    for nm, x_, y_ in r28e_heritage(S):
        px, py = V.p(x_, y_)
        out.append(dict(x=px, y=py, lines=[(nm, False)], h=h, col=R28E_HER_TXT, rank=1))
    for nm, x_, y_ in r28e_streets(S):
        px, py = V.p(x_, y_)
        out.append(dict(x=px, y=py, lines=[(nm, False)], h=h, col=INK, rank=1))
    for nm, x_, y_ in r28e_mahalle(S):
        px, py = V.p(x_, y_)
        out.append(dict(x=px, y=py, lines=[(tr_upper(nm), False)], h=h, col=INK2, rank=1, centre=True))
    return out


def r28e_place(B, items, taken, bounds, k, L, segs=(), order=66):
    """G4 (common/label_place.py): the labels items [dict(x, y (board units), lines [(text, bold)], h (capital
    height), col, rank (0 always shown, 1 may be dropped), centre (an area's name: on its point when that is free),
    italic)] placed clear of each other, of the boxes in taken (symbols) and of the lines segs [(p, q)], inside
    bounds; a label set off its point gets a thin leader. Worked in booklet mm; never smaller than drawn (7 pt).
    Returns the texts of the labels dropped; taken grows."""
    mm = 1.0 / k
    pad, lead = 0.3, 1.4
    tk = [tuple(v * mm for v in b) for b in taken]
    bd = tuple(v * mm for v in bounds) if bounds else None
    sg = [((p[0] * mm, p[1] * mm), (q[0] * mm, q[1] * mm)) for p, q in segs]

    def size(it):
        h = it["h"] * mm
        return (max(r28mv_tw(t, h, b) for t, b in it["lines"]) + 2.0 * pad,
                h * (1.0 + lead * (len(it["lines"]) - 1)) + 2.0 * pad)

    def free(b):
        return ((bd is None or (bd[0] <= b[0] and b[2] <= bd[2] and bd[1] <= b[1] and b[3] <= bd[3])) and
                not any(lp_hit(b, t) for t in tk) and not any(_lp_seg_box(p, q, b) for p, q in sg))

    placed = {}

    def run(idx):
        sub = []
        for i in idx:
            wh_ = size(items[i])
            sub.append(dict(x=items[i]["x"] * mm, y=items[i]["y"] * mm, wh=(lambda f, s_=wh_: s_),
                            rank=items[i].get("rank", 1)))
        for j, got in place_labels_all(sub, tk, bd, sg, sizes=(1.0,), pad=0.2).items():
            placed[idx[j]] = (got[0], got[1])

    run([i for i, it in enumerate(items) if it.get("rank", 1) == 0])
    rest = []
    for i, it in enumerate(items):
        if it.get("rank", 1) == 0:
            continue
        if it.get("centre"):
            w_, h_ = size(it)
            ax, ay = it["x"] * mm, it["y"] * mm
            b = (ax - 0.5 * w_, ay - 0.5 * h_, ax + 0.5 * w_, ay + 0.5 * h_)
            if free(b):
                tk.append(b)
                placed[i] = (b, False)
                continue
        rest.append(i)
    run(rest)
    dropped = []
    for i, it in enumerate(items):
        if i not in placed:
            dropped.append(u" ".join(t for t, b_ in it["lines"]))
            continue
        b, far = placed[i]
        x0, y1 = b[0] * k, b[3] * k
        if far:
            e = lp_leader_end(b, (it["x"] * mm, it["y"] * mm))
            B.line([(it["x"], it["y"]), (e[0] * k, e[1] * k)], it["col"], L, order - 1, bk_lw(0.1, k))
        h = it["h"]
        yl = y1 - pad * k - h
        for t, bold in it["lines"]:
            B.text(t, x0 + pad * k, yl, h, it["col"], L, order=order, font=FONT_TITLE, bold=bold,
                   italic=it.get("italic", False))
            yl -= lead * h
    taken[:] = [tuple(v * k for v in b) for b in tk]
    return dropped


# ------------------------------------------------------------ the strip and its base
def r28e_base(S, CB, V, k, L):
    """v50 (P06.1-P06.3, replaces draw_eb_base): the stream edge plan's base through ClipB CB, crisp, in the
    masterplan's tones and layer order: satellite trees and fields (smoothed), mapped parks, woods and fields, where
    we can build (vector hatches), contours, street surfaces, the stream and its edge, the covered course,
    buildings (R28E_BLD, nonzero; heritage with its edge, OpenStreetMap footprints with a thin outline), bridges,
    street edges, the study area (G8). The ground (white) is the caller's."""
    for key, col in (("trees", MPL["tree"]), ("farmland", MPL["field"]), ("orchard", MPL["field"])):
        fill_units(CB, V, r28e_lc(S, key), col, L, 3)
    for z in S.zones:
        if z["kind"] in ("green", "agri"):
            CB.fill(V.Ps(z["Ps"] + z["Hs"]), MPL["field"] if z["kind"] == "agri" else (
                MPL["tree"] if z.get("sub") == "wood" else MPL["park"]), L, 4)
    og = r28e_open_groups(S)
    for part, hk in R28E_KEYS:
        r28e_hatched(CB, V, og[part], hk, k, L, 6)
    for major, P in getattr(S, "contours", None) or []:
        CB.line(V.P(P), R28E_CONTOUR, L, 8, bk_lw(R28E_CONTOUR_W[1 if major else 0], k))
    for rg_ in getattr(S, "road_net", None) or []:
        CB.fill(V.Ps([rg_["P"]] + rg_["H"]), MPL["road"], L, 10)
    for wt in S.water:
        CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), MPL["water"], L, 15)
    for P in getattr(S, "water_outline", []) or []:
        CB.line(V.P(P), MPL["water_edge"], L, 16, bk_lw(0.18, k))
    for q in getattr(S, "decks", []) or []:               # streets on decks over the water stay above it
        CB.fill([V.P(q)], MPL["road"], L, 17)
    for P in getattr(S, "covered", []) or []:             # the covered course under streets and roofs
        for d in dashes(V.P(P), 1.6 * k, 0.9 * k):
            CB.line(d, MPL["water_edge"], L, 18, bk_lw(0.3, k))
    her = lambda u: u.get("fabric") in ("monument", "sacred")
    mini_buildings(S, CB, V, L, lambda u: MPL["her"] if her(u) else R28E_BLD, order=20)
    for u in S.bld:
        if her(u):
            for P in u["parts"]:
                CB.line(V.P(list(P) + [P[0]]), MPL["her_edge"], L, 21, bk_lw(0.12, k))
        elif u.get("src") in ("osm", "osm+label"):        # P06.3: a footprint the survey does not have
            for P in u["parts"]:
                CB.line(V.P(list(P) + [P[0]]), R28E_OSM_EDGE, L, 21, bk_lw(0.08, k))
    for P in getattr(S, "bridges", []) or []:
        CB.line(V.P(P), MPL["ink_dark"], L, 25, bk_lw(0.3, k))
    for P in getattr(S, "road_lines_net", []) or []:
        CB.line(V.P(P), MPL["road_edge"], L, 30, bk_lw(0.12, k))
    for r_ in S.roads:
        if not r_.get("w"):
            CB.line(V.P(r_["P"]), MPL["road_edge"], L, 30, bk_lw(0.12, k))
    draw_r28_study(S, CB, V, k, L)


def r28e_strip(S, B, x, yt, k, L, photos=()):
    """v50 (G7, P06.1, P06.4): the whole frame as ONE strip at 1:10,000, its top-left corner at (x, yt): the base,
    the edge every 4 m on both banks (walled and embanked marked), bridges K1-K6 as bars with their names, the photo
    viewpoints (numbered discs, view cones), the context names (G4), the frame's line. Returns (View, board units
    per metre, the strip's rectangle, the labels dropped)."""
    F = S.F
    ss = 1000.0 * k / R28E_DEN
    V = View(F, ss, x, yt)
    r = (x, yt - F.h * ss, x + F.w * ss, yt)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    r28e_base(S, CB, V, k, L)
    for typ, pts in getattr(S, "edge_runs", []):          # the edge every 4 m, both banks
        CB.line(V.P(pts), EDGE[typ][1], L, 40, bk_lw(0.7, k))
    for pts in getattr(S, "wall_runs", []):
        for d in dashes(V.P(pts), 1.0 * k, 0.8 * k):
            CB.line(d, WHITE, L, 41, bk_lw(0.3, k))
    for pts in getattr(S, "bank_runs", []):
        for d in dashes(V.P(pts), 0.2 * k, 1.0 * k):
            CB.line(d, WHITE, L, 41, bk_lw(0.3, k))
    h7 = bk_hk(7.0, k)
    taken, items = [], []
    for kk, nm, bx, by in BRIDGES_K:                      # the six crossings: a bar across the stream, K and name
        if not F.inside(bx, by):
            continue
        px, py = V.p(bx, by)
        nrm = stream_normal(S, bx, by) or (0.0, 1.0)
        a_ = V.p(bx + nrm[0], by + nrm[1])
        ln = math.hypot(a_[0] - px, a_[1] - py) or 1.0
        e = ((a_[0] - px) / ln * 1.6 * k, (a_[1] - py) / ln * 1.6 * k)
        CB.line([(px - e[0], py - e[1]), (px + e[0], py + e[1])], MPL["ink_dark"], L, 45, bk_lw(0.6, k))
        taken.append((px - 1.6 * k, py - 1.6 * k, px + 1.6 * k, py + 1.6 * k))
        items.append(dict(x=px, y=py, lines=[(kk, True), (nm, False)], h=h7, col=INK, rank=0))
    rd = 1.6 * k                                          # a viewpoint's disc; its number 7 pt
    for j, (p, it) in enumerate(photos):                  # viewpoints: cone from the camera, disc behind it
        if not F.inside(it["x"], it["y"]):
            continue
        px, py = V.p(it["x"], it["y"])
        brg, f35 = PHOTO_VIEW.get(it.get("file", "").split(".")[0], (None, None))
        dx, dy, fov = 0.0, 0.0, 0.0
        if brg is not None:                               # bearing from true north, clockwise; survey y = north
            fov = photo_fov(f35)
            tip = V.p(it["x"] + math.sin(math.radians(brg)) * EB_CONE_M,
                      it["y"] + math.cos(math.radians(brg)) * EB_CONE_M)
            ln = math.hypot(tip[0] - px, tip[1] - py) or 1.0
            dx, dy = (tip[0] - px) / ln, (tip[1] - py) / ln
            ac, R_ = math.atan2(dy, dx), EB_CONE_M * ss
            arc = [(px + R_ * math.cos(ac + fov * (t_ / 12.0 - 0.5)), py + R_ * math.sin(ac + fov * (t_ / 12.0 - 0.5)))
                   for t_ in range(13)]
            CB.line([arc[-1], (px, py), arc[0]] + arc[1:], INK, L, 50, bk_lw(0.2, k))
            cq = arc + [(px, py)]
            taken.append((min(q[0] for q in cq), min(q[1] for q in cq), max(q[0] for q in cq), max(q[1] for q in cq)))
        B.fill([circle_pts(px, py, 0.4 * k, 10)], INK, L, 51)
        spot = None
        back = math.atan2(-dy, -dx) if brg is not None else 0.0
        for far in (1.0, 1.8, 2.6):
            for a in range(12):
                ang = back + (a + 1) // 2 * (1 if a % 2 else -1) * math.pi / 6.0
                dd = far * (rd + 0.8 * k)
                if brg is not None and dd <= EB_CONE_M * ss + rd:
                    off = abs((ang - math.atan2(dy, dx) + math.pi) % (2.0 * math.pi) - math.pi)
                    if off < 0.5 * fov + math.radians(12.0):
                        continue                          # never on its own cone
                cx_, cy_ = px + dd * math.cos(ang), py + dd * math.sin(ang)
                b = (cx_ - rd, cy_ - rd, cx_ + rd, cy_ + rd)
                own = [t_ for t_ in taken if not (t_[0] <= px <= t_[2] and t_[1] <= py <= t_[3])]   # not its own cone
                if r[0] <= b[0] and b[2] <= r[2] and r[1] <= b[1] and b[3] <= r[3] and not _hit(b, own):
                    spot = (cx_, cy_, b)
                    break
            if spot:
                break
        if spot is None:
            spot = (px - (rd + 0.8 * k), py, (px - 2 * rd - 0.8 * k, py - rd, px - 0.8 * k, py + rd))
            LOG.append("Stream edge plan: photo {} has no free place for its number; drawn beside it.".format(j + 1))
        cx_, cy_, b = spot
        B.line([(px, py), (cx_, cy_)], INK, L, 59, bk_lw(0.15, k))
        B.fill([circle_pts(cx_, cy_, rd, 24)], INK, L, 60)
        B.text(str(j + 1), cx_, cy_, h7, WHITE, L, order=61, font=FONT_TITLE, bold=True, align="MC")
        taken.append(b)
    items += r28e_names(S, V, k)
    segs = []                                             # labels never sit on the stream's centre line
    for P in getattr(S, "selinus", None) or []:
        Q = V.P(dp_simplify(P, 15.0))
        segs += list(zip(Q[:-1], Q[1:]))
    dropped = r28e_place(B, items, taken, (r[0] + 0.5 * k, r[1] + 0.5 * k, r[2] - 0.5 * k, r[3] - 0.5 * k), k, L,
                         segs)
    B.line(rect(*r) + [(r[0], r[1])], INK, L, 70, bk_lw(0.25, k))
    return V, ss, r, dropped


# ------------------------------------------------------------ the key and the panels beside the strip
def r28e_swatch(B, kind, ref, x, y, k, L, w=6.0, h=2.4, order=20):
    """a key sample w x h booklet mm, its top-left corner at (x, y): box (fill ref), osm (a building with the
    OpenStreetMap footprint's thin outline), her (heritage building), hatch / hatchline (R28_BUILD_HATCH key ref: tint
    and hatch as the strip / the hatch alone), line (ref = (colour, mm)), dash (ref = colour: the covered course),
    study (G8), contour (a 10 m and a 5 m line), bridge (a bar across the stream), edge (the six edge colours),
    walled / embanked (the bank marks), cone (a viewpoint), frame (the analysis frame's line), note (results needed)"""
    w, h = w * k, h * k
    sw_ = rect(x, y - h, x + w, y)
    ym = y - 0.5 * h
    if kind == "box":
        B.fill([sw_], ref, L, order)
    elif kind == "osm":
        B.fill([sw_], R28E_BLD, L, order)
        B.line(sw_ + [sw_[0]], R28E_OSM_EDGE, L, order + 1, bk_lw(0.08, k))
    elif kind == "her":
        B.fill([sw_], MPL["her"], L, order)
        B.line(sw_ + [sw_[0]], MPL["her_edge"], L, order + 1, bk_lw(0.12, k))
    elif kind in ("hatch", "hatchline"):
        lab, col, ang = R28E_HATCH[ref]
        if kind == "hatch":
            B.fill([sw_], mix(col, WHITE, R28E_TINT), L, order)
        B.hatch([sw_], col, L, order + 1, R28E_HATCH_MM[0] * k, math.radians(ang), bk_lw(R28E_HATCH_MM[1], k))
        B.line(sw_ + [sw_[0]], col, L, order + 2, bk_lw(0.1, k))
    elif kind == "line":
        B.line([(x, ym), (x + w, ym)], ref[0], L, order, bk_lw(ref[1], k))
    elif kind == "dash":
        for d in dashes([(x, ym), (x + w, ym)], 1.6 * k, 0.9 * k):
            B.line(d, ref, L, order, bk_lw(0.3, k))
    elif kind == "study":
        st = R28_STUDY_LINE
        for d in r28_pattern([(x, ym), (x + w, ym)], [m_ * k for m_ in st["dash_mm"]]):
            B.line(d, C(st["colour"]), L, order, bk_lw(st["width_mm"], k))
    elif kind == "contour":
        B.line([(x, ym + 0.6 * k), (x + w, ym + 0.6 * k)], R28E_CONTOUR, L, order, bk_lw(R28E_CONTOUR_W[1], k))
        B.line([(x, ym - 0.6 * k), (x + w, ym - 0.6 * k)], R28E_CONTOUR, L, order, bk_lw(R28E_CONTOUR_W[0], k))
    elif kind == "bridge":
        B.fill([rect(x, ym - 0.7 * k, x + w, ym + 0.7 * k)], MPL["water"], L, order)
        B.line([(x + 0.5 * w, y), (x + 0.5 * w, y - h)], MPL["ink_dark"], L, order + 1, bk_lw(0.6, k))
    elif kind == "edge":
        n_ = len(EDGE_ORDER)
        for i, k_ in enumerate(EDGE_ORDER):
            B.line([(x + i * w / n_, ym), (x + (i + 1) * w / n_, ym)], EDGE[k_][1], L, order, bk_lw(0.7, k))
    elif kind in ("walled", "embanked"):
        B.line([(x, ym), (x + w, ym)], INK2, L, order, bk_lw(0.7, k))
        dd = (1.0, 0.8) if kind == "walled" else (0.2, 1.0)
        for d in dashes([(x, ym), (x + w, ym)], dd[0] * k, dd[1] * k):
            B.line(d, WHITE, L, order + 1, bk_lw(0.3, k))
    elif kind == "cone":
        B.line([(x + w, y), (x + 0.8 * k, ym), (x + w, y - h)], INK, L, order, bk_lw(0.2, k))
        B.fill([circle_pts(x + 0.8 * k, ym, 0.4 * k, 10)], INK, L, order + 1)
    elif kind == "frame":
        B.line(sw_ + [sw_[0]], INK, L, order, bk_lw(0.25, k))
    elif kind == "note":
        B.line(sw_ + [sw_[0]], MARK_C, L, order, bk_lw(0.2, k))


def r28e_key(B, rows, x, y, ncol, colw, k, L):
    """the map's key (P06.2, P06.3: it draws the hatches and outlined fills the booklet's legend cannot), rows
    [(kind, ref, label)] in ncol columns colw wide, filled column by column from (x, y) (top), 7 pt. Returns the y
    under it."""
    pitch = 3.3 * k
    nrow = max(1, (len(rows) + ncol - 1) // ncol)
    h7 = bk_hk(7.0, k)
    for i, (kind, ref, lab) in enumerate(rows):
        lx, ly = x + (i // nrow) * colw, y - (i % nrow) * pitch
        r28e_swatch(B, kind, ref, lx, ly, k, L)
        B.text(lab, lx + 7.0 * k, ly - 2.4 * k + 0.4 * k, h7, INK, L, font=FONT_TITLE)
    return y - nrow * pitch


def r28e_key_rows(photos=True):
    """the stream edge plan's key (the hatches of where we can build are in its own panel, with their areas)"""
    rows = [("box", R28E_BLD, u"Building (survey)"), ("osm", None, u"Building, OpenStreetMap footprint"),
            ("her", None, u"Heritage building"), ("box", MPL["road"], u"Street"),
            ("box", MPL["water"], u"Stream"), ("dash", MPL["water_edge"], u"Covered course"),
            ("box", MPL["tree"], u"Woods, tree cover"), ("box", MPL["park"], u"Parks, grass"),
            ("box", MPL["field"], u"Fields, orchards"), ("contour", None, u"Contours, 5 m (10 m bolder)"),
            ("bridge", None, u"Bridge K1-K6 and its name"), ("edge", None, u"Bank edge, every 4 m (THE EDGE)"),
            ("walled", None, u"Walled bank"), ("embanked", None, u"Embanked bank (slope line)"),
            ("study", None, R28_STUDY_NAME), ("frame", None, R28_FRAME_NAME + u" (the map's edge)")]
    if photos:
        rows.append(("cone", None, u"Photo viewpoint and view cone"))
    return rows


def r28e_edge_panel(S, B, x, y, w, k, L):
    """THE EDGE: what meets the water, % of the bank length on both sides, six bars in the strip's edge colours,
    from (x, y) (top), w wide. Returns (the y under it, % walled, % embanked)."""
    sh_, wl_, em_, tot = edge_shares(S)
    if tot <= 0:
        return y, wl_, em_
    h7, h75 = bk_hk(7.0, k), bk_hk(7.5, k)
    B.text(u"THE EDGE " + bcite(EDGE_SRC), x, y - h75, h75, INK, L, font=FONT_TITLE, bold=True)
    y -= h75 + 1.6 * k
    r28e_rich(B, u"% of **{}** of bank · both sides, **every 4 m**".format(u_dim(tot, "km")), x, y - h7, h7, INK2, L)
    y -= h7 + 2.6 * k
    lw_ = 40.0 * k
    bw0 = w - lw_ - 9.0 * k
    vmax = max(sh_.values() or [1.0]) or 1.0
    for k_ in EDGE_ORDER:
        v_ = sh_.get(k_, 0.0)
        B.text(EB_EDGE_LAB[k_], x, y - h7, h7, INK, L, font=FONT_TITLE)
        bx_ = x + lw_
        if v_ > 0:
            B.fill([rect(bx_, y - h7 - 0.3 * k, bx_ + bw0 * v_ / vmax, y + 0.2 * k)], EDGE[k_][1], L, 20)
        B.text(u"{:.0f}%".format(v_), bx_ + bw0 * v_ / vmax + 1.2 * k, y - h7, h7, INK, L, font=FONT_TITLE, bold=True)
        y -= 3.5 * k
    return y, wl_, em_


def r28e_rings(B, x, y, wl_, em_, k, L):
    """walled and embanked: two rings, each with the mark the strip draws, "disconnected" under them; top at y.
    Returns the y under them."""
    h7, h8 = bk_hk(7.0, k), bk_hk(8.0, k)
    rr = 5.0 * k
    for j, (pct, kind) in enumerate(((wl_, "walled"), (em_, "embanked"))):
        rx, ry = x + rr + j * 21.0 * k, y - rr
        vis_ring(B, rx, ry, rr, pct, INK2, FAINT, L)
        B.text(u"{:.0f}%".format(pct), rx, ry, h8, INK, L, order=40, font=FONT_TITLE, bold=True, align="MC")
        sx, sy = rx - rr, ry - rr - 2.8 * k
        r28e_swatch(B, kind, None, sx, sy + 1.2 * k, k, L, w=4.5)
        B.text(kind, sx + 5.5 * k, sy - 0.5 * h7, h7, INK, L, font=FONT_TITLE)
    B.text(u"disconnected", x, y - 2.0 * rr - 6.2 * k, h7, INK2, L, font=FONT_TITLE)
    return y - 2.0 * rr - 7.2 * k


def r28e_build_key(S, B, x, y, w, k, L, fill=True):
    """WHERE WE CAN BUILD (P06.2: the legend beside the strip): the ground open to change, its three parts as the
    strip draws them (tint and vector hatch) with their areas; every figure is ground_open's count. Top at y.
    Returns the y under it."""
    h7, h75 = bk_hk(7.0, k), bk_hk(7.5, k)
    vac, park, loose, opn = ground_open(S)
    B.text(u"WHERE WE CAN BUILD " + bcite(OPEN_SRC), x, y - h75, h75, INK, L, font=FONT_TITLE, bold=True)
    y -= h75 + 1.6 * k
    r28e_rich(B, u"**{}** · {:.0f}% of the frame, **open to change**".format(
        u_area(opn, "ha"), 100.0 * opn / max(1.0, S.frame_area)), x, y - h7, h7, INK2, L)
    y -= h7 + 2.0 * k
    for (part, hk), a in zip(R28E_KEYS, (vac, park, loose)):
        r28e_swatch(B, "hatch" if fill else "hatchline", hk, x, y, k, L, h=3.0)
        r28e_rich(B, u"**{}** · {}".format(R28E_HATCH[hk][0], u_area(a, "ha")), x + 7.5 * k, y - 2.5 * k, h7, INK, L)
        y -= 4.4 * k
    return y


# ------------------------------------------------------------ p.06 and p.22
def draw_edge_build(S, B, x, y, w, U, with_photos=True):
    """v50 (MIRAQUA 28 Oct, P06.1-P06.4, G7, G8; replaces v45's two strips at 1:5,000): THE STREAM EDGE AND WHERE
    WE CAN BUILD (p.06, crop drw_edge_build). The whole frame as ONE strip at 1:10,000 on the booklet page
    (r28e_strip: the edge every 4 m on both banks, walls and embankments, where we can build hatched, bridges K1-K6
    with their names, street, mahalle and heritage names, contours, the study area, the photo viewpoints), its scale
    bar and north arrow under it; beside it THE EDGE, the walled / embanked rings and WHERE WE CAN BUILD; the map's
    key under them; the photos, four to a row, in the height left (the page's BK_AH). with_photos=False: p.22's copy
    (draw_edge_build_e). Drawn for the full booklet panel width (BK_AW). Returns the y below."""
    L = "LU_BOARD::EdgeBuild"
    F = S.F
    k = w / BK_AW
    top = y
    if not with_photos:
        return draw_edge_build_e(S, B, x, top, w, U, k, L)
    h7, h75, h9 = bk_hk(7.0, k), bk_hk(7.5, k), bk_hk(9.0, k)
    photos = []
    try:
        photos = photo_files(os.path.join(SELINUS_RES_DIR, "_site_photos"))
    except Exception:
        LOG.append("WARNING: the site photos could not be read for the stream edge plan:\n" + traceback.format_exc())
    V, ss, r, dropped = r28e_strip(S, B, x, top, k, L, photos)
    foot = b_foot(B, F, x, r[1], ss, k, L, R28E_SB_M)
    cx0 = r[2] + R28E_GAP * k                             # the column beside the strip
    cw = x + w - cx0
    yy, wl_, em_ = r28e_edge_panel(S, B, cx0, top, cw, k, L)
    yy -= 2.5 * k
    y1 = r28e_rings(B, cx0, yy, wl_, em_, k, L)
    y2 = r28e_build_key(S, B, cx0 + 44.0 * k, yy, cw - 44.0 * k, k, L)
    low = r28e_key(B, r28e_key_rows(bool(photos)), x, min(foot, y1, y2) - 3.0 * k, 6, w / 6.0, k, L)
    bot = top - BK_AH * k
    n_ph = len(photos)
    if n_ph:                                              # P06.4: the photos in the height the second strip left
        hb = low - 3.0 * k - h75
        B.text(u"SITE PHOTOS · 1 OCT 2026 · NUMBERS AND CONES ON THE PLAN " + bcite(
            u"Photos: site visit 2026-10-01 (group photos, GPS within {:.0f} m). On the plan: the dot is where each was "
            u"taken, the cone its direction (compass, true north) and angle of view (35 mm-equivalent focal length), "
            u"both from the photo's own record (EXIF), {:.0f} m long. Captions: keywords of the photo index (a visual "
            u"reading); Roman bridges after h01 §5.".format(max(it.get("gps_err_m", 0.0) for p, it in photos),
                                                             EB_CONE_M)), x, hb, h75, INK, L, font=FONT_TITLE, bold=True)
        py0 = hb - 3.0 * k
        cols, g = 4, 3.0 * k
        cell = (w - (cols - 1) * g) / cols
        rows_ = (n_ph + cols - 1) // cols
        cap_h = 1.2 * k + h7 + 2.2 * k                    # caption under each photo and the row gap
        ph = max(10.0 * k, min(cell * 0.75, (py0 - bot - 1.0 * k + 2.2 * k) / rows_ - cap_h))
        pw = ph / 0.75                                    # never stretched: 4:3 as taken
        bn = 4.2 * k
        for j, (p, it) in enumerate(photos):
            px = x + (j % cols) * (cell + g)
            py = py0 - (j // cols) * (ph + cap_h)
            B.image(p, px, py - ph, px + pw, py, L, order=5)
            B.fill([rect(px, py - bn, px + bn, py)], INK, L, 64)
            B.text(str(j + 1), px + 0.5 * bn, py - 0.5 * bn, h9, WHITE, L, order=65, font=FONT_TITLE, bold=True,
                   align="MC")
            B.text(eb_caption(it, pw, h7), px, py - ph - 1.2 * k - h7, h7, INK, L, font=FONT_TITLE)
        low = py0 - rows_ * (ph + cap_h) + 2.2 * k
        if low < bot + 0.5 * k:
            LOG.append(u"WARNING: the stream edge plan's photos end {:.1f} mm below the booklet page's area.".format(
                (bot + 0.5 * k - low) / k))
    crop_panel("edge_build", x, low - 0.5 * k, x + w, top + 0.5 * k,
               u"Both banks, the edge every 4 m · ground open to change · photo viewpoints 1-{}".format(n_ph or 8),
               crop_scale(ss), [])
    CROP_PANELS[-1]["bk_w"] = BK_AW                       # drawn for the full booklet panel width
    vac, park, loose, opn = ground_open(S)
    LOG.append(u"Stream edge plan (p.06): ONE strip at 1:{:,}, {:.1f} x {:.1f} mm; ground open to change {} ({:.1f}% "
               u"of the frame): open ground {}, parking & yards {}, loose ground {}; {} photos; labels left out (G4): "
               u"{}.".format(R28E_DEN, F.w * ss / k, F.h * ss / k, u_area(opn, "ha"), 100.0 * opn / max(1.0, S.frame_area),
                             u_area(vac, "ha"), u_area(park, "ha"), u_area(loose, "ha"), n_ph,
                             u", ".join(dropped) or u"none"))
    r28e_export_open(S)
    return low - 1.0 * U


def draw_edge_build_e(S, B, x, top, w, U, k, L):
    """v50 (P22.1, G7, G8; p.22 "Before the masterplan", cut when the booklet merges pp.21 + 22, D1): the strip of
    draw_edge_build without photos or viewpoints, ONE strip at 1:10,000; the column from EB_COL_X as before (THE
    EDGE, the walled / embanked rings, WHERE WE CAN BUILD, stacked), the key where the legend was (under the strip),
    scale bar and north arrow under the strip. Crop drw_edge_build_e, drawn for the full booklet panel width. Returns
    the y below."""
    V, ss, r, dropped = r28e_strip(S, B, x, top, k, L)
    foot = b_foot(B, S.F, x, r[1], ss, k, L, R28E_SB_M)
    cx0 = x + EB_COL_X * k
    cw = x + w - cx0
    yy, wl_, em_ = r28e_edge_panel(S, B, cx0, top, cw, k, L)
    yy = r28e_rings(B, cx0, yy - 2.5 * k, wl_, em_, k, L)
    yy = r28e_build_key(S, B, cx0, yy - 3.0 * k, cw, k, L)
    low = min(yy, r28e_key(B, r28e_key_rows(False), x, foot - 3.0 * k, 4, (r[2] - x) / 4.0, k, L))
    crop_panel("edge_build_e", x, low - 0.5 * k, x + w, top + 0.5 * k,
               u"Before the masterplan: both banks, the edge every 4 m · ground open to change", crop_scale(ss), [])
    CROP_PANELS[-1]["bk_w"] = BK_AW                       # drawn for the full booklet panel width
    LOG.append(u"Stream edge plan, p.22 copy: ONE strip at 1:{:,}; {:.0f} mm high; labels left out (G4): {}.".format(
        R28E_DEN, (top - low) / k, u", ".join(dropped) or u"none"))
    r28e_export_open(S)
    return low - 1.0 * U


# ------------------------------------------------------------ D1: the export and the filter sheet
def r28e_export_open(S):
    """D1: r28_open_to_change.json in SELINUS_RES_DIR, once a run: the ground open to change as p.06 counts and
    draws it, {frame_ha, total_ha, classes {vacant, parking, loose: {ha (ground_open's count, the figures p.06
    prints), rings (survey m, as drawn: the mapped outlines with their holes; the loose ground traced from the
    counted cells and smoothed)}}, definition, rings, source}"""
    m = r28e_memo(S)
    if m.get("exported"):
        return
    m["exported"] = True
    try:
        vac, park, loose, opn = ground_open(S)
        og = r28e_open_groups(S)
        cls = {}
        for (part, hk), a in zip(R28E_KEYS, (vac, park, loose)):
            cls[part] = {"ha": round(a / 1e4, 2),
                         "rings": [[[round(p[0], 2), round(p[1], 2)] for p in P] for g in og[part] for P in g
                                   if len(P) >= 3]}
        out = {"frame_ha": round(S.frame_area / 1e4, 2), "total_ha": round(opn / 1e4, 2), "classes": cls,
               "definition": u"Open to change (site board, p.06) = the analysis frame's vacant lots and parking & "
                             u"yards as mapped (survey, OpenStreetMap) and its loose ground: unmapped ground that ESA "
                             u"WorldCover 2021 classes as grassland or shrubland, counted on a {:.0f} m raster. A "
                             u"reading of what could change, not a check of ownership or zoning".format(REST_CELL),
               "rings": u"survey m; each class's outlines as p.06 draws them (the loose ground traced from the counted "
                        u"cells, simplified and smoothed); the areas are the count; fill even-odd",
               "source": u"{} · {}".format(SCRIPT_VERSION, time.strftime("%Y-%m-%d %H:%M"))}
        os.makedirs(SELINUS_RES_DIR, exist_ok=True)
        with open(R28E_OPEN_JSON, "w", encoding="utf-8") as fh:
            json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
        LOG.append(u"r28_open_to_change.json (D1): {} open to change of {} ({}: vacant {}, parking & yards {}, loose "
                   u"{} rings).".format(u_area(opn, "ha"), u_area(S.frame_area, "ha"), R28E_OPEN_JSON,
                                        len(cls["vacant"]["rings"]), len(cls["parking"]["rings"]),
                                        len(cls["loose"]["rings"])))
    except Exception:
        LOG.append("WARNING: r28_open_to_change.json not written:\n" + traceback.format_exc())


def r28e_mp_open():
    """D1: the masterplan's open ground (r28_open_ground.json beside its masterplan_results.json: the masterplan runs
    before the site board), or None (logged) when it is missing or not complete; and the path looked at"""
    p = bg_first([os.path.join(bg_cache("bergama_masterplan"), R28E_MP_JSON),
                  os.path.join(os.path.dirname(MP_RESULTS_FILE), R28E_MP_JSON)])
    try:
        with open(p, "r", encoding="utf-8") as fh:
            d = json.load(fh)
        if isinstance(d, dict) and isinstance(d.get("classes"), dict) and d.get("open_ha") is not None and \
                d.get("frame_ha") is not None:
            return d, p
        LOG.append(u"WARNING: {} has no open_ha, frame_ha or classes: the filter sheet says \"masterplan results "
                   u"needed\".".format(p))
    except Exception as ex:
        LOG.append(u"Filter sheet: the masterplan's open ground ({}) could not be read ({}): it says \"masterplan "
                   u"results needed\" and prints no open-ground figure.".format(p, ex))
    return None, p


def r28e_draw_filter(S, B, x, y, w, U):
    """v50 (MIRAQUA 28 Oct, D1; crop drw_filter, the booklet's one page for pp.21 + 22 when it merges them): THE
    FILTER. One strip of the analysis frame at 1:10,000 (G7, G8): the masterplan's open ground and what it leaves out
    (buildings, streets, the stream bed: its own cells, read from r28_open_ground.json) in R28_OPEN's colours, the
    ground open to change hatched as on p.06; under it the filter as three bars to one scale, analysis frame -> open
    ground (the masterplan's count, printed as it is: G10) -> of which open to change (ground_open, the figure p.06
    prints), one short reason a step (G5), and the two definitions named side by side. Without the masterplan's file
    the strip and the second bar say "masterplan results needed" and no open-ground figure is printed. Drawn for the
    full booklet panel width (BK_AW). Returns the y below."""
    L = "LU_BOARD::Filter"
    F = S.F
    k = w / BK_AW
    top = y
    h7, h75, h8, h9, h10 = (bk_hk(p_, k) for p_ in (7.0, 7.5, 8.0, 9.0, 10.0))
    mp, mp_path = r28e_mp_open()
    oc = dict((k_, C(R28_OPEN[k_])) for k_ in ("open_fill", "building", "road", "stream", "bridge"))
    cls = (mp or {}).get("classes") or {}

    def ha(key):                                          # a class of the masterplan's count, m2
        return float((cls.get(key) or {}).get("ha") or 0.0) * 1e4
    # ---- the strip
    ss = 1000.0 * k / R28E_DEN
    V = View(F, ss, x, top)
    r = (x, top - F.h * ss, x + F.w * ss, top)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    if mp:
        for key, ck, o_ in (("open", "open_fill", 3), ("road", "road", 4), ("bed", "stream", 5),
                            ("building", "building", 6)):
            rings = [[(float(q[0]), float(q[1])) for q in P] for P in (cls.get(key) or {}).get("rings") or []
                     if len(P) >= 3]
            if rings:
                CB.fill(V.Ps(rings), oc[ck], L, o_)
    else:                                                 # the board's own streets, stream and buildings
        for rg_ in getattr(S, "road_net", None) or []:
            CB.fill(V.Ps([rg_["P"]] + rg_["H"]), oc["road"], L, 4)
        for wt in S.water:
            CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), oc["stream"], L, 5)
        mini_buildings(S, CB, V, L, lambda u: oc["building"], order=6)
    og = r28e_open_groups(S)
    for part, hk in R28E_KEYS:
        r28e_hatched(CB, V, og[part], hk, k, L, 8, fill=False)
    for P in getattr(S, "bridges", []) or []:
        CB.line(V.P(P), oc["bridge"], L, 12, bk_lw(0.3, k))
    draw_r28_study(S, CB, V, k, L)
    if not mp:
        t_ = u"Open ground: masterplan results needed (r28_open_ground.json)"
        tl = r28mv_tw(t_, h8, True)
        cx_, cy_ = 0.5 * (r[0] + r[2]), 0.5 * (r[1] + r[3])
        bx = rect(cx_ - 0.5 * tl - 1.5 * k, cy_ - 0.5 * h8 - 1.5 * k, cx_ + 0.5 * tl + 1.5 * k, cy_ + 0.5 * h8 + 1.5 * k)
        B.fill([bx], WHITE, L, 60)
        B.line(bx + [bx[0]], MARK_C, L, 61, bk_lw(0.2, k))
        B.text(t_, cx_ - 0.5 * tl, cy_ - 0.5 * h8, h8, MARK_C, L, order=62, font=FONT_TITLE, bold=True)
    B.line(rect(*r) + [(r[0], r[1])], INK, L, 70, bk_lw(0.25, k))
    foot = b_foot(B, F, x, r[1], ss, k, L, R28E_SB_M)
    # ---- the key beside the strip
    kx = r[2] + R28E_GAP * k
    tw_ = x + w - kx
    vac, park, loose, opn = ground_open(S)
    rows = [("frame", None, R28_FRAME_NAME), ("study", None, R28_STUDY_NAME),
            ("box", oc["open_fill"], u"Open ground (masterplan)") if mp else
            ("note", None, u"Open ground: masterplan results needed"),
            ("box", oc["building"], u"Building"), ("box", oc["road"], u"Street"), ("box", oc["stream"], u"Stream bed"),
            ("line", (oc["bridge"], 0.3), u"Bridge")]
    rows += [("hatchline", hk, u"Open to change: " + nm_) for (part, hk), nm_ in
             zip(R28E_KEYS, (u"vacant lots", u"parking & yards", u"loose ground"))]
    kl = r28e_key(B, rows, kx, top, 1, tw_, k, L)
    # ---- the filter: three bars to one scale (the frame = the strip's length), a reason each
    fr = S.frame_area
    mfr = float(mp["frame_ha"]) * 1e4 if mp else fr
    if mp and abs(mfr - fr) > 500.0:
        LOG.append(u"Filter sheet: the masterplan's frame is {}, the board's {} (G10: the first bar prints the "
                   u"board's).".format(u_area(mfr, "ha"), u_area(fr, "ha")))
    oa = float(mp["open_ha"]) * 1e4 if mp else 0.0
    bars_w = r[2] - x
    pct = lambda a, b: u"{:.0f}%".format(100.0 * a / max(1.0, b))
    steps = [dict(label=u"1 · " + R28_FRAME_NAME, fig=u"{} · 100%".format(u_area(fr, "ha")), w=bars_w,
                  why=u"**{}**: the strip's rectangle, {} × {}; every figure on this page is counted over "
                      u"it.".format(R28_FRAME_NAME, u_num(F.w), u_dim(F.h, "m", 0)),
                  segs=[(u"Open ground", ha("open"), oc["open_fill"], INK),
                        (u"Buildings", ha("building"), oc["building"], WHITE),
                        (u"Streets", ha("road"), oc["road"], INK), (u"Stream bed", ha("bed"), oc["stream"], INK)]
                  if mp else [])]
    if mp:
        steps.append(dict(label=u"2 · Open ground (masterplan)", fig=u"{} · {} of the frame".format(
            u_area(oa, "ha"), pct(oa, mfr)), w=bars_w * oa / max(1.0, mfr),
            why=u"**Open ground**: no building, no street, not the stream bed: all the masterplan may draw on. "
                u"**Left out**: buildings {}, streets {}, the stream bed {}.".format(
                    u_area(ha("building"), "ha"), u_area(ha("road"), "ha"), u_area(ha("bed"), "ha")),
            segs=[(u"", oa, oc["open_fill"], INK)]))
    else:
        steps.append(dict(label=u"2 · Open ground (masterplan)", fig=None, w=None, note=True,
                          why=u"**Masterplan results needed**: the open ground is the masterplan's own count "
                              u"(r28_open_ground.json, written when the masterplan runs); no figure is printed "
                              u"without it."))
    steps.append(dict(label=u"3 · Of which open to change (site board, as p.06)", fig=u"{} · {} of the frame".format(
        u_area(opn, "ha"), pct(opn, fr)), w=bars_w * opn / max(1.0, fr), hatch=True,
        why=u"**No use recorded**: vacant lots {}, parking & yards {}, loose ground {} (grass or scrub where nothing is "
            u"mapped). **Not counted**: planted or farmed ground (parks, woods, fields, orchards) and unmapped ground "
            u"the satellite does not see as grass or scrub.".format(
                u_area(vac, "ha"), u_area(park, "ha"), u_area(loose, "ha"))))
    close_s = (u"**Two readings, not two answers.** Open ground is what is not built, paved or water: all the "
               u"masterplan may draw on. Open to change is only the ground with no use recorded, counted on the site "
               u"board's own map (p.06). Both read what could change, **not a check of ownership or zoning**.")
    src = bcite(OPEN_SRC)
    if mp:
        src += bcite(u"Open ground: the masterplan's count, read from its r28_open_ground.json ({}). {}.".format(
            mp.get("source", u""), mp.get("definition", u"")))
    yy = min(foot, kl) - 4.0 * k
    B.text(u"THE FILTER · ANALYSIS FRAME, OPEN GROUND, OPEN TO CHANGE " + src, x, yy - h9, h9, INK, L,
           font=FONT_TITLE, bold=True)
    yy -= h9 + 4.0 * k
    bh = 10.0 * k
    heights = []
    for st_ in steps:
        n_ = len(r28mv_lines(st_["why"], tw_, h8))
        th = (h10 + 2.2 * k if st_.get("fig") else 0.0) + h8 + (n_ - 1) * R28MV_LEAD * h8 + 0.6 * k
        heights.append(max(h75 + 1.6 * k + bh, th))
    n_c = len(r28mv_lines(close_s, w, h8))
    close_h = 5.0 * k + h8 + (n_c - 1) * R28MV_LEAD * h8 + 0.6 * k
    bot = top - BK_AH * k + 1.0 * k
    spare = (yy - bot) - sum(heights) - close_h
    gap = max(8.0 * k, min(24.0 * k, 0.5 * spare))        # the funnels take the height the page has
    funnel = mix(oc["open_fill"], WHITE, 0.55)
    prev = None
    ty = yy
    for st_, hgt in zip(steps, heights):
        lb = ty - h75
        bt = lb - 1.6 * k
        bb_ = bt - bh
        if mp and prev is not None and st_.get("w"):      # the funnel from the bar above
            B.fill([[(x, prev[1]), (x + prev[0], prev[1]), (x + st_["w"], bt), (x, bt)]], funnel, L, 2)
        B.text(st_["label"], x, lb, h75, INK, L, font=FONT_TITLE, bold=True)
        if st_.get("hatch"):
            cx_ = x
            for (part, hk), a in zip(R28E_KEYS, (vac, park, loose)):
                sw = bars_w * a / max(1.0, fr)
                if sw > 0.0:
                    q = rect(cx_, bb_, cx_ + sw, bt)
                    lab_, col_, ang_ = R28E_HATCH[hk]
                    B.fill([q], mix(col_, WHITE, R28E_TINT), L, 20)
                    B.hatch([q], col_, L, 21, R28E_HATCH_MM[0] * k, math.radians(ang_), bk_lw(R28E_HATCH_MM[1], k))
                    cx_ += sw
            B.line(rect(x, bb_, cx_, bt) + [(x, bb_)], INK, L, 22, bk_lw(0.15, k))
        elif st_.get("note"):
            q = rect(x, bb_, x + 0.5 * bars_w, bt)
            B.line(q + [q[0]], MARK_C, L, 22, bk_lw(0.2, k))
            B.text(u"masterplan results needed", x + 1.5 * k, bb_ + 0.5 * (bh - h75), h75, MARK_C, L, order=24,
                   font=FONT_TITLE, bold=True)
        else:
            cx_ = x
            tot_ = sum(s_[1] for s_ in st_.get("segs") or []) or 0.0
            for nm_, a, col_, tc_ in (st_.get("segs") or []) if tot_ > 0.0 else []:
                sw = st_["w"] * a / tot_
                B.fill([rect(cx_, bb_, cx_ + sw, bt)], col_, L, 20)
                t_ = u"{} {}".format(nm_, u_area(a, "ha")) if nm_ else u""
                if t_ and r28mv_tw(t_, h7) + 2.4 * k <= sw:
                    B.text(t_, cx_ + 1.2 * k, bb_ + 0.5 * (bh - h7), h7, tc_, L, order=24, font=FONT_TITLE)
                cx_ += sw
            if tot_ <= 0.0:                               # the frame alone (without the masterplan's classes)
                B.fill([rect(x, bb_, x + st_["w"], bt)], WHITE, L, 20)
            B.line(rect(x, bb_, x + st_["w"], bt) + [(x, bb_)], INK, L, 22, bk_lw(0.15, k))
        yb = ty
        if st_.get("fig"):
            B.text(st_["fig"], kx, ty - h10, h10, INK, L, font=FONT_TITLE, bold=True)
            yb = ty - h10 - 2.2 * k
        r28mv_para(B, st_["why"], kx, yb - h8, tw_, h8, INK, L, order=40)
        prev = (st_.get("w") or 0.0, bb_)
        y_end = ty - hgt
        ty = y_end - gap
    yc = r28mv_para(B, close_s, x, y_end - 5.0 * k - h8, w, h8, INK, L, order=40)
    low = yc + R28MV_LEAD * h8 - 0.6 * k - h8 * 0.3
    if low < bot - 0.5 * k:
        LOG.append(u"WARNING: the filter sheet ends {:.1f} mm below the booklet page's area.".format((bot - low) / k))
    crop_panel("filter", x, low - 0.5 * k, x + w, top + 0.5 * k,
               u"The filter · analysis frame, open ground, open to change", crop_scale(ss), [])
    CROP_PANELS[-1]["bk_w"] = BK_AW                       # drawn for the full booklet panel width
    LOG.append(u"Filter sheet (D1, crop drw_filter): {} frame -> open ground {} -> open to change {} (vacant {}, "
               u"parking & yards {}, loose {}); one strip at 1:{:,}; {:.0f} mm high.".format(
                   u_area(fr, "ha"), u_area(oa, "ha") if mp else u"(masterplan results needed: " + mp_path + u")",
                   u_area(opn, "ha"), u_area(vac, "ha"), u_area(park, "ha"), u_area(loose, "ha"), R28E_DEN,
                   (top - low) / k))
    r28e_export_open(S)
    return low - 1.0 * U


# ------------------------------------------------------------ p.16 the shade strip on the frame's axis
def draw_shade_strip(S, B, x, y, w, U):
    """v50 (MIRAQUA 28 Oct, G7, G8; replaces v47's chart on the chainage axis): SHADE ALONG THE STREAM, the mean July
    day (p.16, crop drw_shade_strip): hours out of direct sun at ground level on the left bank, the bed and the right
    bank in shade_strip_data's 25 m bins, each bin drawn where it lies along the analysis frame's axis at 1:10,000
    (the maps' scale and length: one strip), the study area's stretches framed in its line (G8), the stream's
    chainage as ticks every 500 m, a scale bar under the rows; covered reaches hatched on the bed (no value), bridges
    as ticks across it, each row's mean at the right; no section markers. Every word 7.5 pt in the sans, drawn for
    SS_BK_W mm. Returns the y below; draws nothing without shade results (build_sheet leaves it out then)."""
    L = "LU_BOARD::ShadeStrip"
    d = shade_strip_data(S)
    if not d:
        return y
    F = S.F
    cor, n, bm, rows = d["cor"], d["n"], d["bm"], d["rows"]
    k = w / SS_BK_W                                       # board units per booklet mm
    h75 = bk_hk(7.5, k)
    ss = 1000.0 * k / R28E_DEN                            # 1:10,000 along the frame's axis
    B.text(u"SHADE ALONG THE STREAM · JULY, MEAN DAY · BED AND BANKS, EVERY 25 M", x, y, 1.05 * U, INK, L,
           font=FONT_TITLE, bold=True)                    # the sheet's title, above the crop
    top = y - 0.5 * U
    f1 = lambda v: u"{:.1f}".format(v) if v is not None else u"-"
    ctx = (u"**Hours out of direct sun** at ground level on the stream bed and on {:.0f} m of each bank, every {:.0f} m "
           u"downstream, cast by buildings, the terrain and tree crowns. **July, mean day** ({} h of sun up): the bed "
           u"is in shade {} h on average, the banks {} h (left) and {} h (right)").format(
        SS_BANK_M, bm, f1(d["daylight"]), f1(rows["bed"]["mean"]), f1(rows["left"]["mean"]), f1(rows["right"]["mean"]))
    if d["under2"] is not None:
        ctx += u"; {:.0f}% of the bed's {:.0f} m bins get under {:.0f} h of shade".format(d["under2"], bm, SS_STEP)
    ctx += (u". Each bin is drawn where it lies along the analysis frame's axis at 1:10,000, as the maps (the rows' "
            u"height is not to scale); the ticks count metres along the stream.")
    yt = r28mv_para(B, ctx, x, top - 0.8 * k - h75, w, h75, INK2, L, order=40)
    lab_w = tw(u"RIGHT BANK", h75, "sans") + 2.5 * k      # the rows' names at the left
    x0 = x + lab_w
    x1 = x0 + F.w * ss                                    # the frame's length at 1:10,000; each row's mean beyond
    sel = seam_pack().get("selinos") or {}
    LX, LY, LC = (np.asarray(sel[k_], float) for k_ in ("x", "y", "ch"))

    def at(ch):                                           # the centreline's point at chainage ch (survey m)
        return float(np.interp(ch, LC, LX)), float(np.interp(ch, LC, LY))

    def X(ch):                                            # chainage -> page x along the frame's axis
        return x0 + min(F.w, max(0.0, F.local(*at(ch))[0] - F.u0)) * ss
    xe = [X(i * bm) for i in range(n + 1)]                # the bins' ends

    def span(i, e):                                       # bins i..e as a page x range (the stream may turn back)
        return min(xe[i:e + 2]), max(max(xe[i:e + 2]), min(xe[i:e + 2]) + 0.1 * k)
    # ---- the stream's chainage, every 500 m downstream (as on the tree crown cover chart)
    ya = yt - 1.0 * k
    gtop = ya - 1.8 * k
    B.text(u"downstream", x0 - 1.5 * k, ya, h75, INK2, L, font=FONT_TITLE, align="R")
    last = -1e30
    for m in range(0, int(n * bm) + 1, 500):
        xm = X(m)
        t_ = u"{:,}".format(m) + (u" m" if m == 0 else u"")
        tl = tw(t_, h75, "sans")
        B.line([(xm, gtop + 0.3 * k), (xm, gtop + 1.1 * k)], INK2, L, 6, bk_lw(0.15, k))
        lx_ = xm if m == 0 else xm - 0.5 * tl
        if lx_ > last + 1.0 * k:
            B.text(t_, xm, ya, h75, INK2, L, font=FONT_TITLE, align="L" if m == 0 else "C")
            last = lx_ + tl
    B.text(u"mean", x1 + 1.5 * k, ya, h75, INK2, L, font=FONT_TITLE)
    # ---- the three rows: runs of bins in one colour step as one fill, blank under SS_MIN_CELLS cells
    rh, rg = 7.0 * k, 0.9 * k                             # a row, the gap between two
    for r_, (nm, key) in enumerate(((u"LEFT BANK", "left"), (u"BED", "bed"), (u"RIGHT BANK", "right"))):
        rt = gtop - r_ * (rh + rg)
        vals = rows[key]["vals"]
        i = 0
        while i < n:
            if vals[i] is None:
                i += 1
                continue
            c_ = ss_colour(vals[i])
            e = i
            while e + 1 < n and vals[e + 1] is not None and ss_colour(vals[e + 1]) == c_:
                e += 1
            xa, xb = span(i, e)
            B.fill([rect(xa, rt - rh, xb, rt)], c_, L, 3)
            i = e + 1
        B.line(rect(x0, rt - rh, x1, rt) + [(x0, rt - rh)], FAINT, L, 4, bk_lw(0.1, k))
        ym = rt - 0.5 * rh - 0.5 * h75
        B.text(nm, x0 - 1.5 * k, ym, h75, INK, L, font=FONT_TITLE, bold=True, align="R")
        if rows[key]["mean"] is not None:
            B.text(u"{:.1f} h".format(rows[key]["mean"]), x1 + 1.5 * k, ym, h75, INK, L, font=FONT_TITLE, bold=True)
    # ---- on the bed row: the covered reaches hatched (no value), the bridges as ticks across it
    bt = gtop - (rh + rg)
    for a_, b_ in cor.get("covered_reaches", []):
        xs_ = [X(a_), X(0.5 * (a_ + b_)), X(b_)]
        cov = rect(min(xs_), bt - rh, max(xs_), bt)
        B.fill([cov], WHITE, L, 5)
        B.hatch([cov], SS_COVER_C, L, 6, 1.0 * k, w=bk_lw(0.15, k))
        B.line(cov + [cov[0]], SS_COVER_C, L, 6, bk_lw(0.1, k))
    bch = cor.get("bridges_ch", [])
    for i_ in range(0, len(bch) - 1, 2):
        xa, xb = sorted((X(bch[i_]), X(bch[i_ + 1])))
        if xb - xa < 0.5 * k:
            xa, xb = 0.5 * (xa + xb) - 0.25 * k, 0.5 * (xa + xb) + 0.25 * k
        B.fill([rect(xa, bt - rh - 0.6 * k, xb, bt + 0.6 * k)], INK, L, 7)
    # ---- G8: the stretches inside the study area, framed in its line across the three rows
    ybot = gtop - 3.0 * rh - 2.0 * rg
    st_ = R28_STUDY_LINE
    ins = [any(pip(at((i + 0.5) * bm)[0], at((i + 0.5) * bm)[1], P) for P in getattr(S, "r28_study", None) or [])
           for i in range(n)]
    i = 0
    while i < n:
        if not ins[i]:
            i += 1
            continue
        e = i
        while e + 1 < n and ins[e + 1]:
            e += 1
        xa, xb = span(i, e)
        q = rect(xa, ybot - 0.5 * k, xb, gtop + 0.2 * k)
        for dd in r28_pattern(q + [q[0]], [m_ * k for m_ in st_["dash_mm"]]):
            B.line(dd, C(st_["colour"]), L, 9, bk_lw(st_["width_mm"], k))
        i = e + 1
    # ---- the scale bar under the rows (1:10,000 along the frame's axis)
    yl0 = draw_scalebar_bk(B, x0 + 1.0 * k, ybot - 2.5 * k, ss, R28E_SB_M, k, L)
    B.text(u"1:{:,} along the frame's axis".format(R28E_DEN), x0 + 1.0 * k + R28E_SB_M * ss +
           tw(u"{:,.0f} m".format(R28E_SB_M), h75, "sans") + 3.0 * k, ybot - 2.5 * k - 1.2 * k, h75, INK2, L,
           font=FONT_TITLE)
    # ---- key in one row: the colour steps, a covered reach, a bridge, the study area
    ky = yl0 - 2.0 * k                                    # the swatches' top
    sh_ = 2.6 * k
    yl = ky - sh_ - 1.0 * k - h75                         # the steps' names under their swatches
    t_ = u"h of shade, July mean day"
    B.text(t_, x, ky - sh_, h75, INK, L, font=FONT_TITLE, bold=True)
    kx = x + tw(t_, h75, "sans") + 3.0 * k
    sw = 9.0 * k
    nr = len(SS_RAMP)
    for i, c_ in enumerate(SS_RAMP):
        B.fill([rect(kx + i * sw, ky - sh_, kx + (i + 1) * sw, ky)], c_, L, 20)
        B.text(u"{:g}-{:g}".format(i * SS_STEP, (i + 1) * SS_STEP) if i + 1 < nr else u"{:g}+".format(i * SS_STEP),
               kx + (i + 0.5) * sw, yl, h75, INK2, L, font=FONT_TITLE, align="C")
    B.line(rect(kx, ky - sh_, kx + nr * sw, ky) + [(kx, ky - sh_)], INK2, L, 21, bk_lw(0.1, k))
    B.text(u"h", kx + nr * sw + 1.0 * k, yl, h75, INK2, L, font=FONT_TITLE)
    kx += nr * sw + 6.0 * k
    sw = 6.0 * k
    cov = rect(kx, ky - sh_, kx + sw, ky)
    B.fill([cov], WHITE, L, 20)
    B.hatch([cov], SS_COVER_C, L, 21, 1.0 * k, w=bk_lw(0.15, k))
    B.line(cov + [cov[0]], SS_COVER_C, L, 22, bk_lw(0.1, k))
    t_ = u"covered: under the town, no sun"
    B.text(t_, kx + sw + 1.5 * k, ky - sh_, h75, INK, L, font=FONT_TITLE)
    kx += sw + 1.5 * k + tw(t_, h75, "sans") + 6.0 * k
    B.fill([rect(kx + 0.5 * sw - 0.3 * k, ky - sh_ - 0.6 * k, kx + 0.5 * sw + 0.3 * k, ky + 0.6 * k)], INK, L, 22)
    B.text(u"bridge", kx + sw + 1.5 * k, ky - sh_, h75, INK, L, font=FONT_TITLE)
    kx += sw + 1.5 * k + tw(u"bridge", h75, "sans") + 6.0 * k
    for dd in r28_pattern([(kx, ky - 0.5 * sh_), (kx + 8.0 * k, ky - 0.5 * sh_)], [m_ * k for m_ in st_["dash_mm"]]):
        B.line(dd, C(st_["colour"]), L, 22, bk_lw(st_["width_mm"], k))
    B.text(R28_STUDY_NAME, kx + 9.5 * k, ky - sh_, h75, INK, L, font=FONT_TITLE)
    kx += 9.5 * k + tw(R28_STUDY_NAME, h75, "sans") + 6.0 * k
    t_ = u"left and right looking downstream · blank: under {} cells".format(SS_MIN_CELLS)
    if kx + tw(t_, h75, "sans") > x + w:                  # no room left in the row: under the steps' names
        kx, yl = x, yl - 1.8 * h75
        B.text(t_, kx, yl, h75, INK2, L, font=FONT_TITLE)
    else:
        B.text(t_, kx, ky - sh_, h75, INK2, L, font=FONT_TITLE)
    # ---- the method, labelled computed; the full sentence in the drawings' source key
    src = (u"Shade along the stream (computed by this board): hours out of direct sun on the mean July day at ground "
           u"level on a 1 m grid, every minute the sun is up on all 31 days of July 2025 (NOAA / Meeus solar position, "
           u"UTC+3) summed and divided by 31. In the sun's way: every surveyed building footprint as a prism of its "
           u"height (surveyed floors x storey height, or a published height) on the surveyed ground; the tree crowns "
           u"of the canopy map (Meta / WRI 1 m canopy height, modelled), deciduous ones in leaf, counted by the light "
           u"they block; the terrain horizon (PVGIS DEM profiles every 100 m) and the ground's own slope. Not "
           u"modelled: walls, the channel's own banks, bridge decks and the roofs over the covered reaches, so where "
           u"walls or deep banks line the bed its hours are a lower bound. Bed = the 1 m cells inside the stream's "
           u"mapped outline, those under a bridge or a covered reach left out; banks = the open cells within {:.0f} m "
           u"beyond the channel's edge on each side, left and right looking downstream. Chainage along the OSM Selinos "
           u"centreline from the upstream frame edge, as on the tree crown cover chart; {:.0f} m bins, a bin under {} "
           u"cells left blank.").format(SS_BANK_M, bm, SS_MIN_CELLS)
    yb = ctx_line(B, u"computed · sun every minute of July 2025 at the site (NOAA / Meeus) · surveyed building "
                     u"footprints at their roof heights · tree crowns from the canopy map (modelled) · terrain horizon "
                     u"from the DEM (PVGIS) · 1 m grid, ground level · walls and the channel's banks not modelled " +
                  bcite(src), x, yl - 3.0 * k - h75, w, h75, L, font=FONT_TITLE)
    low = yb + 1.15 * h75 - 0.8 * k                       # under the last line's descenders
    crop_panel("shade_strip", x, low, x + w, top, u"Shade along the stream · July, mean day · bed and banks, every 25 m",
               crop_scale(ss))
    CROP_PANELS[-1]["bk_w"] = SS_BK_W                     # its width on the booklet page, mm
    LOG.append(u"Shade along the stream (July, mean day, {} h of sun up): in shade {} h on the bed, {} h on the left "
               u"bank and {} h on the right bank on average; {} of {} bed bins under {:.0f} h; {} bins in the study "
               u"area; one strip at 1:{:,} along the frame's axis; booklet crop drw_shade_strip, {:.0f} mm wide, "
               u"{:.1f} mm high.".format(
                   f1(d["daylight"]), f1(rows["bed"]["mean"]), f1(rows["left"]["mean"]), f1(rows["right"]["mean"]),
                   sum(1 for v in rows["bed"]["vals"] if v is not None and v < SS_STEP), d["n_bed"], SS_STEP,
                   sum(ins), R28E_DEN, SS_BK_W, (top - low) / k))
    return low - 1.0 * U
