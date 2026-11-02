# ---- 02g Demeter's Garden designed (round 5 S6, 2 Nov 2026; BRIEF P23.7 / P24.7, U64; G-R5-9 organic) --------------
# Aras (U64): "Demeter garden olarak tasarlanacak alanın tasarısı eksik … ne Master planda ne genel olarak kesitte".
# ONE design, read by p23 (the masterplan), p24 (the Üç Kemer window and the D2-D2′ section) and any later page:
#   dg_design(C) -> dict(rings, rows, cafe, paths, seats, gather, edge, shade_trees, src, terrace, olive)   (survey m)
#     rings        the garden's organic outlines: every zone-base DG zone (Option A, "DG 1", "DG 2"), Chaikin-smoothed,
#                  + its stream terrace (below) as a ring of its own
#     rows         tomato-row polylines (the garden's crop, above the flood) in the stream terrace and in the
#                  stream-side half of each garden
#     olive        the landward half of each garden (rings): the olive grove the round 4 plan drew there (project data:
#                  P24_SPECIES "demeter" = olive, lavender; olive rows are the plant module's sourced crop)
#     cafe         [ring]: the café disc at the zone's own label point z["q"] (round 4 put the café there)
#     shade_trees  [(key, x, y)]: planes round the café ("café · guests in the garden's shade"; plane = round 4's café
#                  shade tree and the hub squares' sourced shade tree)
#     paths        [polyline]: café -> the riverside walk (round 4 rule, <= 80 m); garden -> garden -> Üç Kemer Köprüsü
#     gather       [ring]: a gathering place on the stream terrace by the water
#     seats        [(x, y, ang)]: seats round the gathering place and the café (ang = the seat's long axis, rad)
#     edge         [polyline]: the terrace's water-side edge (the garden's edge down to the stream) and the path
#                  length that reaches Üç Kemer Köprüsü
# Facts used (booklet text, round 4 PDF): raised above Q500, stays dry (the sections set its floor at Q500 + 0.30 m,
# p24_section's existing rule); tomato rows; café under shade; places to sit and gather; edge down to the stream and
# to Üç Kemer Köprüsü; organic form. Positions: zone base DG rings (embedded copy / zone base file), the W3 (K5) cut
# from LEVELS, the stream half width from its bed width, Üç Kemer = the bridge-list point (BRIDGES "K5", N4 a).
# Every SIZE below is a drawing rule (no source gives one) and is marked so; anything else is [ask].
DG_SMOOTH_N = 3            # Chaikin passes on every outline (G-R5-9; drawing rule)
DG_REACH_M = 30.0          # a garden this near the W3 (K5) cut gets the stream terrace that reaches the cut (P23.7
#                            "in the cut, not beyond"; design reading, drawing rule)
DG_PAST_CUT_M = 6.0        # the terrace runs this far past the cut, so the D2-D2′ section cuts through it (drawing rule)
DG_INTO_M = 3.0            # the terrace overlaps its garden by this much (one shape; drawing rule)
DG_BANK_M = 1.0            # the terrace stops this far short of the bank top (drawing rule)
DG_ROW_M = 1.5             # tomato row spacing: NOT sourced (plants.py PLA_CROPS tomato row_m None) -> drawing rule [ask]
DG_TOMATO_H_M = 0.8        # tomato plant height in section: NOT sourced (PLA_CROPS tomato h_m None) -> drawing rule [ask]
DG_TOMATO_W_M = 0.6        # tomato plant spread in section: NOT sourced (crown_m None) -> drawing rule [ask]
DG_CAFE_R_M = 6.0          # café disc radius (drawing rule)
DG_GATHER_R_M = 5.0        # gathering place radius (drawing rule)
DG_SEAT_STEP_M = 4.0       # a seat every this many m round the gathering place and the café (drawing rule)
DG_SHADE_N = 3             # planes round the café (drawing rule; round 4 drew 2)
DG_K5_MAX_M = 200.0        # the garden path runs on to Üç Kemer Köprüsü when it is this near (drawing rule)
DG_WALK_MAX_M = 80.0       # café -> walk path only when the walk is this near (round 4 P24_DG rule)


def _dg_pip(p, R):
    x, y, ins = p[0], p[1], False
    for (x1, y1), (x2, y2) in zip(R, R[1:] + R[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            ins = not ins
    return ins


def _dg_disc(c, r, n=24):
    return [(c[0] + r * math.cos(2.0 * math.pi * i / n), c[1] + r * math.sin(2.0 * math.pi * i / n)) for i in range(n)]


def _dg_smooth(R):
    P = [tuple(p[:2]) for p in R]
    if len(P) > 3 and abs(P[0][0] - P[-1][0]) < 1e-9 and abs(P[0][1] - P[-1][1]) < 1e-9:
        P = P[:-1]
    return chaikin(P, DG_SMOOTH_N, closed=True) if len(P) >= 3 else P


def _dg_rows(R, u, step):
    """parallel polylines along unit vector u across ring R, step m apart, cut to R (sc_lines)"""
    n = (-u[1], u[0])
    ss = [p[0] * n[0] + p[1] * n[1] for p in R]
    ls = [p[0] * u[0] + p[1] * u[1] for p in R]
    out, s = [], min(ss) + step / 2.0
    while s < max(ss):
        a = (u[0] * (min(ls) - 1.0) + n[0] * s, u[1] * (min(ls) - 1.0) + n[1] * s)
        b = (u[0] * (max(ls) + 1.0) + n[0] * s, u[1] * (max(ls) + 1.0) + n[1] * s)
        out += [r_ for r_ in sc_lines([a, b], [R]) if len(r_) >= 2]
        s += step
    return out


def _dg_wet(C, p):
    n = C.cell(p)
    return C.Dst[n] if n is not None and C.Dst[n] < 1e8 else None


def _dg_half(R, c, nrm):
    side = lambda p: (p[0] - c[0]) * nrm[0] + (p[1] - c[1]) * nrm[1]
    out = []
    for p, q in zip(R, R[1:] + R[:1]):
        sp, sq = side(p), side(q)
        if sp >= 0.0:
            out.append(p)
        if (sp >= 0.0) != (sq >= 0.0):
            f_ = sp / (sp - sq)
            out.append((p[0] + (q[0] - p[0]) * f_, p[1] + (q[1] - p[1]) * f_))
    return out


def dg_design(C):
    got = getattr(C, "_dg", None)
    if got is not None:
        return got
    out = dict(rings=[], rows=[], olive=[], cafe=[], paths=[], seats=[], gather=[], edge=[], shade_trees=[],
               terrace=[], src=u"zone base DG zones (Option A); W3 cut (LEVELS); Üç Kemer = bridge-list point K5; "
                               u"sizes = drawing rules (02g)")
    zs = [z for z in C.D.zones if z.get("code") == "DG" and len(z.get("P") or ()) >= 3]
    if not zs:
        out["src"] = u"no DG zone in the zone base: nothing designed [ask]"
        C._dg = out
        return out
    study = getattr(C, "study", None)
    # the W3 (K5) cut frame: c0 its centre, cd along it (SW -> NE), f upstream (p24's convention), hw the bed half
    try:
        reg = level_registry("W3")
        hw = reg["bed_width_cm"] / 200.0
        cd, f = _p24_cut_dir("W3")
        c0 = CUT_AT[2][2]
    except Exception:
        reg, hw, cd, f, c0 = None, None, None, None, None
    tz = lambda p: ((p[0] - c0[0]) * cd[0] + (p[1] - c0[1]) * cd[1], (p[0] - c0[0]) * f[0] + (p[1] - c0[1]) * f[1])
    pz = lambda t, d: (c0[0] + cd[0] * t + f[0] * d, c0[1] + cd[1] * t + f[1] * d)
    k5 = BRIDGES.get("K5", {}).get("xy") if "BRIDGES" in globals() else None
    walk = [P for P in (C.canopy or []) if len(P) >= 2]
    cents = []
    for z in zs:
        R = _dg_smooth(z["P"])
        if study:
            Rs = [r_ for r_ in sc_rings_clip(R, study) if len(r_) >= 3]
            R = max(Rs, key=lambda r_: abs(area2(r_))) if Rs else R
        out["rings"].append(R)
        c = (sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R))
        cents.append(c)
        # the stream-side half (tomato rows) and the landward half (olive grove), split across the long axis
        a = math.radians(principal_angle(R))
        u = (math.cos(a), math.sin(a))
        halves = [h for h in (_dg_half(R, c, u), _dg_half(R, c, (-u[0], -u[1]))) if len(h) >= 3]
        wet = lambda H_: sum(d for d in (_dg_wet(C, p) for p in H_) if d is not None) / max(1, len(H_))
        halves.sort(key=wet)
        if len(halves) == 2:
            out["rows"] += _dg_rows(halves[0], u, DG_ROW_M)
            out["olive"].append(halves[1])
        else:
            out["rows"] += _dg_rows(R, u, DG_ROW_M)
        # the café at the zone's own label point, its planes round it, seats round it
        q = z.get("q")
        if q and _dg_pip(q, R):
            out["cafe"].append(_dg_disc(q, DG_CAFE_R_M))
            for i in range(DG_SHADE_N):
                ang = 2.0 * math.pi * (i + 0.25) / DG_SHADE_N
                p = (q[0] + (DG_CAFE_R_M + 3.0) * math.cos(ang), q[1] + (DG_CAFE_R_M + 3.0) * math.sin(ang))
                if _dg_pip(p, R):
                    out["shade_trees"].append(("plane", p[0], p[1]))
            n_s = max(3, int(2.0 * math.pi * DG_CAFE_R_M / DG_SEAT_STEP_M))
            for i in range(n_s):
                ang = 2.0 * math.pi * i / n_s
                out["seats"].append((q[0] + (DG_CAFE_R_M - 1.0) * math.cos(ang),
                                     q[1] + (DG_CAFE_R_M - 1.0) * math.sin(ang), ang + math.pi / 2.0))
            if walk:                                       # café -> the riverside walk (round 4 rule)
                best = None
                for P in walk:
                    for a_, b_ in zip(P, P[1:]):
                        dx, dy = b_[0] - a_[0], b_[1] - a_[1]
                        l2 = dx * dx + dy * dy
                        t_ = 0.0 if l2 < 1e-12 else max(0.0, min(1.0, ((q[0] - a_[0]) * dx + (q[1] - a_[1]) * dy) / l2))
                        w_ = (a_[0] + dx * t_, a_[1] + dy * t_)
                        d_ = math.hypot(q[0] - w_[0], q[1] - w_[1])
                        if best is None or d_ < best[0]:
                            best = (d_, w_)
                if best and best[0] <= DG_WALK_MAX_M:
                    out["paths"].append([tuple(q), best[1]])
        # the stream terrace: the garden's edge down to the stream, carried past the D2-D2′ cut (P23.7)
        if c0 is not None:
            TD = [tz(p) for p in R]
            side = -1.0 if sum(t for t, d in TD) / len(TD) < 0 else 1.0
            near_t = min(t * side for t, d in TD) * side      # the garden's stream-facing t (nearest the stream)
            dmin = min(d for t, d in TD)
            if abs(near_t) > hw and dmin <= DG_REACH_M:
                t_in = near_t + side * DG_INTO_M                # into the garden
                t_bank = side * (hw + DG_BANK_M)
                d_hi = min(dmin + 15.0, max(d for t, d in TD))   # along the garden's stream side (drawing rule)
                box = [(t_in, -DG_PAST_CUT_M), (t_bank, -DG_PAST_CUT_M), (t_bank, d_hi), (t_in, d_hi)]
                T_ = _dg_smooth([pz(t, d) for t, d in box])
                if study:
                    Ts = [r_ for r_ in sc_rings_clip(T_, study) if len(r_) >= 3]
                    T_ = max(Ts, key=lambda r_: abs(area2(r_))) if Ts else None
                if T_:
                    out["terrace"].append(T_)
                    out["rings"].append(T_)
                    out["rows"] += _dg_rows(T_, f, DG_ROW_M)
                    e_ = [pz(t_bank, -DG_PAST_CUT_M + 1.0), pz(t_bank, d_hi - 1.0)]
                    out["edge"].append(e_)
                    gc = pz((t_in + t_bank) / 2.0, (dmin - DG_PAST_CUT_M) / 2.0)
                    gr = min(DG_GATHER_R_M, abs(t_bank - t_in) / 2.0 - 0.5)
                    if gr > 1.5 and _dg_pip(gc, T_):
                        out["gather"].append(_dg_disc(gc, gr))
                        n_s = max(3, int(2.0 * math.pi * gr / DG_SEAT_STEP_M))
                        for i in range(n_s):
                            ang = 2.0 * math.pi * i / n_s
                            out["seats"].append((gc[0] + gr * math.cos(ang), gc[1] + gr * math.sin(ang),
                                                 ang + math.pi / 2.0))
    # the garden path: garden -> garden -> Üç Kemer Köprüsü (upstream along the SW bank)
    if cents:
        pts = sorted(cents, key=lambda c: -tz(c)[1] if c0 is not None else c[1])
        if k5 and min(math.hypot(c[0] - k5[0], c[1] - k5[1]) for c in cents) <= DG_K5_MAX_M:
            pts = sorted(cents, key=lambda c: -math.hypot(c[0] - k5[0], c[1] - k5[1])) + [tuple(k5)]
            out["edge"].append([pts[-2], pts[-1]] if len(pts) >= 2 else [])
        if len(pts) >= 2:
            P = chaikin(pts, 2) if len(pts) > 2 else pts
            if study:
                runs = [r_ for r_ in sc_lines(P, study) if len(r_) >= 2]
                out["paths"] += runs
            else:
                out["paths"].append(P)
    out["edge"] = [e for e in out["edge"] if len(e) >= 2]
    C._dg = out
    return out
