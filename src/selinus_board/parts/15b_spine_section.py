# ============================================================ v40 LONG SECTION ALONG THE STREAMSIDE SPINE
# Aras 25 Oct: "please revise the section such as we draw in the site sections with the mainboard script". The spine
# of the masterplan (option A, on the real bank edge; masterplan_results.json, written before this script runs) as one
# developed section: each straight piece of the spine cut by the board's own section engine (section_of_line), the
# pieces laid end to end at ONE scale for length and height (never stretched), the picture beyond each piece, the
# stops above it by number and short name. Without the masterplan file: the city link spine the board already uses
# (city_link_spine); without either, no panel (logged).
MP_RESULTS_FILE = bg_first([os.path.join(bg_cache("bergama_masterplan"), "masterplan_results.json"),      # v44
                            os.path.join(BERGAMA_DIR, "output", "bergama_masterplan", "masterplan_results.json")])
SPINE_TOL = 2.0          # m: the spine's line simplified to straight pieces within this distance (Douglas-Peucker)
SPINE_ROW_M = 360.0      # m: the developed section is laid out in rows of at most about this length
SPINE_STOP_NEAR = 60.0   # m: a stop farther than this from the spine is marked at the spine's end, with its distance


def _dp(P, tol):
    """Douglas-Peucker simplification of a polyline."""
    if len(P) < 3:
        return list(P)
    (ax, ay), (bx, by) = P[0], P[-1]
    L = math.hypot(bx - ax, by - ay)
    best, bi = -1.0, 0
    for i in range(1, len(P) - 1):
        px, py = P[i]
        d = abs((bx - ax) * (ay - py) - (ax - px) * (by - ay)) / L if L > 1e-9 else math.hypot(px - ax, py - ay)
        if d > best:
            best, bi = d, i
    if best <= tol:
        return [P[0], P[-1]]
    return _dp(P[:bi + 1], tol)[:-1] + _dp(P[bi:], tol)


def spine_short(name):
    """A stop's short name (<= 24 characters): the name, or its last two words when longer."""
    name = (name or "").strip()
    if len(name) <= 24:
        return name
    w_ = name.split()[-2:]
    return (" ".join(w_))[:1].upper() + (" ".join(w_))[1:]


def spine_source(S):
    """(polyline, stops [(n, name, (x, y))], source words) of the streamside spine, or None."""
    try:
        with open(MP_RESULTS_FILE, "r", encoding="utf-8") as fh:
            A = json.load(fh)["options"]["A"]
        P = []
        for pc in A.get("spine", []):
            for p in pc.get("P", []):
                q = (float(p[0]), float(p[1]))
                if not P or math.hypot(q[0] - P[-1][0], q[1] - P[-1][1]) > 0.05:
                    P.append(q)
        stops = [(int(s_["n"]), s_.get("name", ""), (float(s_["xy"][0]), float(s_["xy"][1])))
                 for s_ in A.get("stops", []) if s_.get("xy")]
        if len(P) >= 2:
            return P, stops, "masterplan results of " + time.strftime(
                "%d %b %H:%M", time.localtime(os.path.getmtime(MP_RESULTS_FILE)))
    except Exception:
        pass
    try:
        props, attr, src = city_link_spine(S)
        P = []
        for kind, Q, _o in props:
            for q in Q:
                if not P or math.hypot(q[0] - P[-1][0], q[1] - P[-1][1]) > 0.05:
                    P.append((float(q[0]), float(q[1])))
        spec = CITY_LINK_DEFAULT
        try:
            with open(CITY_LINK_FILE, "r", encoding="utf-8") as fh:
                spec = json.load(fh)
        except Exception:
            pass
        stops = [(int(f["n"]), f.get("name", ""), (float(f["xy"][0]), float(f["xy"][1])))
                 for f in spec.get("functions", []) if f.get("xy")]
        if len(P) >= 2:
            return P, stops, src
    except Exception:
        pass
    return None


def spine_section(S):
    """The developed section along the spine (memoised on S): a section dict as draw_section_strip's, s along the
    spine, plus segs [(x0, y0, x1, y1, s0, L, own section)], stops [(n, short name, s, off_m)], covered [(a, b, bed)]
    and ends (start, end words); None without a spine."""
    if hasattr(S, "_spine_sec"):
        return S._spine_sec
    S._spine_sec = None
    src = spine_source(S)
    if src is None:
        LOG.append("Long section along the spine: no masterplan results and no city link spine, so not drawn.")
        return None
    P, stops, words = src
    P = _dp(P, SPINE_TOL)
    # the side looked at: the stream beyond the cut over most of the length (every section looks to its left)
    streams = [Q for Q in (getattr(S, "selinus", None) or []) if len(Q) >= 2]
    main = max(streams, key=pl_length) if streams else None
    lt = rt = 0.0
    if main:
        for (ax, ay), (bx, by) in zip(P[:-1], P[1:]):
            mx, my = 0.5 * (ax + bx), 0.5 * (ay + by)
            q, t = pl_point_at(main, pl_chainage(main, mx, my))
            side = (bx - ax) * (q[1] - ay) - (by - ay) * (q[0] - ax)
            if math.hypot(q[0] - mx, q[1] - my) > 3.0:
                if side > 0:
                    lt += math.hypot(bx - ax, by - ay)
                else:
                    rt += math.hypot(bx - ax, by - ay)
    rev = rt > lt
    if rev:
        P = P[::-1]
    ends = ("downstream", "upstream") if rev else ("upstream", "downstream")
    segs, c = [], 0.0
    for (ax, ay), (bx, by) in zip(P[:-1], P[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 0.5:
            continue
        segs.append([ax, ay, bx, by, c, L, section_of_line(S, ax, ay, bx, by, "SP")])
        c += L
    if not segs:
        return None
    Ltot = c
    base = min(sg[6]["base"] for sg in segs)
    D = dict(name="SP", line=(segs[0][0], segs[0][1], segs[-1][2], segs[-1][3], "SP"), L=Ltot, base=base,
             bld=[], trees=[], walls=[], chwalls=[], water=[], bed_src=[], water_src=[], labels=[], levels=[],
             strip=[], comp={}, zmax=0.0, places=[], bridges=[], beyond=[], btrees=[])
    gr = []
    for k, (ax, ay, bx, by, s0, L, d) in enumerate(segs):
        dz = d["base"] - base
        last = k == len(segs) - 1
        gr += [(s + s0, z + dz) for s, z in d["ground"] if s < L - 1e-6 or last]
        D["bld"] += [(a + s0, b + s0, z0 + dz, z1 + dz) + tuple(r[4:]) for r in d["bld"] for a, b, z0, z1 in [r[:4]]]
        D["trees"] += [(s + s0, zg + dz, hw, lo, hi) for s, zg, hw, lo, hi in d["trees"] if 0.0 <= s < L]
        D["walls"] += [(s + s0, zg + dz) for s, zg in d["walls"]]
        D["chwalls"] += [(s + s0, zb + dz, zt + dz) for s, zb, zt in d["chwalls"]]
        D["water"] += [(a + s0, b + s0, bed + dz, lvl + dz) for a, b, bed, lvl in d["water"]]
        D["bed_src"] += d["bed_src"]
        D["water_src"] += d["water_src"]
        D["labels"] += [(s + s0, typ, wl, gz + dz) for s, typ, wl, gz in d["labels"]]
        D["levels"] += [(s + s0, zl + dz, za, kd) for s, zl, za, kd in d["levels"] if kd != "end"]
        D["strip"] += [(a + s0, b + s0, cat) for a, b, cat in d["strip"]]
        for k_, v_ in d["comp"].items():
            D["comp"][k_] = D["comp"].get(k_, 0.0) + v_
        D["zmax"] = max(D["zmax"], d["zmax"] + dz)
        for a, b, nm_ in d["places"]:
            if D["places"] and D["places"][-1][2] == nm_ and a + s0 - D["places"][-1][1] < 2.0:
                D["places"][-1] = (D["places"][-1][0], b + s0, nm_)
            else:
                D["places"].append((a + s0, b + s0, nm_))
    # the ground on an even 0.5 m step (draw_section_strip reads it by index)
    n = int(Ltot / 0.5) + 1
    gs_ = [g[0] for g in gr]
    ground = []
    for i in range(n):
        s = min(Ltot, i * 0.5)
        j = max(0, min(len(gr) - 2, _bisect_right(gs_, s) - 1))
        (sa_, za), (sb_, zb) = gr[j], gr[j + 1]
        ground.append((s, za if sb_ <= sa_ else za + (zb - za) * max(0.0, min(1.0, (s - sa_) / (sb_ - sa_)))))
    D["ground"] = ground
    D["levels"] += [(0.0, ground[0][1], ground[0][1] + base, "end"), (Ltot, ground[-1][1], ground[-1][1] + base, "end")]
    D["water"] = [w_ for w_ in D["water"] if w_[1] - w_[0] >= 1.0]
    # the stream under the street where the spine runs over a covered reach: its bed (interpolated along the stream)
    cov, run = [], None
    for i in range(0, n, 2):
        s = i * 0.5
        sg = next(g for g in segs if g[4] <= s <= g[4] + g[5] + 1e-6)
        t = (s - sg[4]) / sg[5]
        x_, y_ = sg[0] + (sg[2] - sg[0]) * t, sg[1] + (sg[3] - sg[1]) * t
        on = any(pl_dist(x_, y_, Q, False) < 8.0 for Q in (getattr(S, "covered", None) or []) if len(Q) >= 2)
        if on and run is None:
            run = [s, s, x_, y_]
        elif on:
            run[1] = s
        if (not on or i + 2 >= n) and run is not None:
            if run[1] - run[0] >= 10.0:
                sm = 0.5 * (run[0] + run[1])
                dd_ = bed_depth(S, run[2], run[3])
                cov.append((run[0], run[1], None if dd_ is None else ground[int(round(sm / 0.5))][1] - dd_))
            run = None
    D["covered"] = cov
    # the stops: where each one stands along the spine, or how far beyond its ends
    st = []
    pts = [(sg[0], sg[1], sg[2], sg[3], sg[4], sg[5]) for sg in segs]
    for nn, nm_, (x_, y_) in stops:
        best = None
        for ax, ay, bx, by, s0, L in pts:
            t = max(0.0, min(1.0, ((x_ - ax) * (bx - ax) + (y_ - ay) * (by - ay)) / (L * L)))
            d = math.hypot(ax + (bx - ax) * t - x_, ay + (by - ay) * t - y_)
            if best is None or d < best[0]:
                best = (d, s0 + t * L)
        st.append((nn, spine_short(nm_), best[1], best[0]))
    D["stops"] = sorted(st, key=lambda r: r[0])
    D["segs"] = segs
    D["ends"] = ends
    D["src"] = words
    S._spine_sec = D
    LOG.append("Long section along the spine: {:.0f} m from the {} in {} straight pieces (within {:.0f} m), looking "
               "{} the stream; stops {}.".format(Ltot, words, len(segs), SPINE_TOL,
                                                "across" if max(lt, rt) >= 0.5 * (lt + rt) else "along",
                                                ", ".join("{} at {:.0f} m{}".format(r[0], r[2], "" if r[3] <= SPINE_STOP_NEAR
                                                          else " ({:.0f} m off)".format(r[3])) for r in D["stops"])))
    return D


def sec_slice(D, r0, r1):
    """The part r0..r1 (m) of a developed section, s from 0."""
    def cl(a, b):
        return max(a, r0) - r0, min(b, r1) - r0
    R = dict(D)
    R["L"] = r1 - r0
    R["ground"] = [(s - r0, z) for s, z in D["ground"] if r0 - 1e-6 <= s <= r1 + 1e-6]
    R["bld"] = [cl(r[0], r[1]) + tuple(r[2:]) for r in D["bld"] if r[1] > r0 and r[0] < r1]
    R["strip"] = [cl(a, b) + (c_,) for a, b, c_ in D["strip"] if b > r0 and a < r1]
    keep = [k for k, w_ in enumerate(D["water"]) if w_[1] > r0 and w_[0] < r1]
    R["water"] = [cl(D["water"][k][0], D["water"][k][1]) + tuple(D["water"][k][2:]) for k in keep]
    R["bed_src"] = [D["bed_src"][k] for k in keep if k < len(D["bed_src"])]
    R["water_src"] = [D["water_src"][k] for k in keep if k < len(D["water_src"])]
    R["places"] = [cl(a, b) + (nm_,) for a, b, nm_ in D["places"] if b > r0 and a < r1]
    R["covered"] = [cl(a, b) + (z,) for a, b, z in D.get("covered", []) if b > r0 and a < r1]
    for k_ in ("trees", "walls", "chwalls", "labels", "levels"):
        R[k_] = [(r[0] - r0,) + tuple(r[1:]) for r in D[k_] if r0 <= r[0] <= r1]
    return R


def spine_rows(D):
    """The rows of the developed section: [(r0, r1)], split where two straight pieces meet."""
    n = max(1, int(math.ceil(D["L"] / SPINE_ROW_M - 0.08)))
    cuts = [0.0]
    joints = [sg[4] for sg in D["segs"][1:]]
    for k in range(1, n):
        want = D["L"] * k / float(n)
        cuts.append(min(joints, key=lambda j: abs(j - want)) if joints else want)
    cuts.append(D["L"])
    cuts = sorted(set(cuts))
    return [(a, b) for a, b in zip(cuts[:-1], cuts[1:]) if b - a > 1.0]


def _merge(spans, gap):
    """Spans [(a, b, ...)] sorted, those under gap apart joined (the first one's extra fields kept)."""
    out = []
    for sp in sorted(spans):
        if out and sp[0] - out[-1][1] < gap:
            out[-1] = (out[-1][0], max(out[-1][1], sp[1])) + tuple(out[-1][2:])
        else:
            out.append(tuple(sp))
    return out


def spine_calls(R, g_at):
    """The words under a part of the developed section: the stream where the cut runs in it (stretches under 10 m
    apart as one, at least 8 m long) with its bed level, the covered stream under the street, named places.
    [(s, z, text)]. The bank edges are left out: along the stream the cut meets them at every step."""
    out = []
    for a, b, bed, lvl in _merge(R["water"], 10.0):
        if b - a >= 8.0:
            out.append((0.5 * (a + b), bed, "stream · bed +{:.2f}".format(bed + R["base"])))
    for a, b, z in _merge(R.get("covered", []), 15.0):
        out.append((0.5 * (a + b), z if z is not None else g_at(0.5 * (a + b)), "stream covered below"))
    out += [((a + b) / 2.0, g_at((a + b) / 2.0), nm_) for a, b, nm_ in R.get("places", [])]
    return out


def draw_spine_section(S, B, x, y, w, U, tag="drawing"):
    """The long section along the streamside spine: rows of the developed section at one scale (length = height),
    the stops above by number and short name, the words at the water under each row, a locator and a scale bar."""
    L = "LU_BOARD::Sections"
    D = spine_section(S)
    if D is None:
        return y
    rows = spine_rows(D)
    ss = round_ss((w - 2.0 * SEC_END * U) / max(b - a for a, b in rows))   # page units per metre, along AND up
    th = SEC_CALL_H * U
    locw = min(12.0 * U, 0.2 * w)
    B.fit("LONG SECTION ALONG THE STREAMSIDE SPINE  ·  THE STOPS 1-{}".format(max([r[0] for r in D["stops"]] or [0])),
          x, y, 0.6 * U, w - locw - 2.0 * U, INK, L, font=FONT_TITLE, bold=True)
    g = D["ground"]
    B.text("{:.0f} m along the spine · ground +{:.2f} to +{:.2f} · developed, true heights".format(
        D["L"], min(z for s, z in g) + D["base"], max(z for s, z in g) + D["base"]), x, y - 0.95 * U, 0.3 * U, INK2, L)
    F = S.F                                               # the locator: the spine on the site, north up
    V, mw, mh = view_fit(F, x + w - locw, y + 0.55 * U, locw, locw * F.h / F.w)
    B.fill([V.P(F.P)], PAPER, L, 2)
    for wt in S.water:
        B.fill(V.Ps([wt["P"]] + wt.get("H", [])), BLUE_L, L, 8)
    mini_buildings(S, B, V, L, lambda u: FAINT)
    B.line([V.p(sg[0], sg[1]) for sg in D["segs"]] + [V.p(D["segs"][-1][2], D["segs"][-1][3])], INK, L, 15, 0.28)
    B.line(V.P(F.P + [F.P[0]]), INK2, L, 16, 0.06)
    draw_north_small(B, V, mw, mh, U, L, size=0.38)
    top = min(y - 1.6 * U, y + 0.55 * U - mh - 0.5 * U)
    low = top
    for ri, (r0, r1) in enumerate(rows):
        R = sec_slice(D, r0, r1)
        Lm = r1 - r0
        X0 = x + SEC_END * U
        # the stops of this row above it, each on the first line where it clears the others
        here = [r for r in D["stops"] if (r0 <= r[2] < r1 or (ri == len(rows) - 1 and r[2] >= r1 - 1e-6))]
        lab = []
        for nn, nm_, s, off in here:
            fx = X0 + (s - r0) * ss
            txt = nm_ if off <= SPINE_STOP_NEAR else "{} ({:.0f} m)".format(nm_, off)
            x_l, x_r = fx - 0.45 * U, fx + 0.75 * U + tw(txt, th)
            tier = 0
            while any(t2 == tier and x_l < r2 + 0.6 * U and l2 - 0.6 * U < x_r for l2, r2, t2 in lab):
                tier += 1
            lab.append((x_l, x_r, tier))
        nt = max([t2 for _l, _r, t2 in lab] or [-1]) + 1
        row_top = low - (nt * (th + 0.55 * U) + 0.6 * U if nt else 0.3 * U)
        Y0 = row_top - D["zmax"] * ss

        def P(s, z, X0=X0, Y0=Y0):
            return (X0 + s * ss, Y0 + z * ss)

        def g_at(s, R=R):
            return R["ground"][max(0, min(len(R["ground"]) - 1, int(round(s / 0.5))))][1]
        # the pictures beyond the cut, piece by piece, all at the same height range
        if HAVE_NP:
            for k, (ax, ay, bx, by, s0, Ls, d) in enumerate(D["segs"]):
                if s0 + Ls <= r0 + 1e-6 or s0 >= r1 - 1e-6:
                    continue
                sd_k = dict(name="SP%02d" % (k + 1), line=(ax, ay, bx, by, "SP%02d" % (k + 1)), L=Ls, s_off=0.0, part=(1, 1),
                            base=D["base"], zmax=D["zmax"],
                            ground=[(s, z + d["base"] - D["base"]) for s, z in d["ground"]])
                png = sec_art_png(S, sd_k, ss, tag)
                if png:
                    path, zlo_a, zhi_a = png
                    B.image(path, X0 + (s0 - r0) * ss, Y0 + (zlo_a - D["base"]) * ss, X0 + (s0 + Ls - r0) * ss,
                            Y0 + (zhi_a - D["base"]) * ss, L, 5)
        sec_cut(B, L, R, P, Lm, ss, U, dry=not HAVE_NP)
        for a, b, z in R.get("covered", []):              # the covered stream: its bed under the street, dashed
            if z is not None:
                for dd in dashes([P(a, z), P(b, z)], 0.5 * U, 0.3 * U):
                    B.line(dd, SEC_CHANNEL_HATCH, L, 30, 0.3)
        calls = []
        for ax, ay, bx, by, s0, Ls, d in D["segs"]:       # the streets crossed, piece by piece
            if s0 + Ls <= r0 + 1e-6 or s0 >= r1 - 1e-6:
                continue
            o_ = s0 - r0

            def Pk(s, z, o_=o_):
                return P(s + o_, z)

            def gk(s, o_=o_):
                return g_at(s + o_)
            calls += [(s + o_, z, t.split(" · ")[0]) for s, z, t in draw_sec_roads(S, B, L, Pk, gk, (ax, ay, bx, by),
                                                                                   Ls, U)
                      if 0.0 <= s + o_ <= Lm and not t.startswith("STREET")]
        # the stops: a numbered mark over the ground, its name beside it
        for (nn, nm_, s, off), (x_l, x_r, tier) in zip(here, lab):
            fx = X0 + (s - r0) * ss
            sl = min(Lm, max(0.0, s - r0))
            gy = P(sl, g_at(sl))[1]
            ly = row_top + 0.6 * U + (nt - 1 - tier) * (th + 0.55 * U)
            cy = ly + 0.5 * th
            for dd in dashes([(fx, gy + 0.15 * U), (fx, cy - 0.5 * U)], 0.3 * U, 0.2 * U):
                B.line(dd, INK2, L, 37, 0.06)
            mk = circle_pts(fx, cy, 0.5 * U, 24)
            B.fill([mk], INK, L, 40)
            B.text(str(nn), fx, cy, 0.42 * U, PAPER, L, order=41, font=FONT_TITLE, bold=True, align="MC")
            txt = nm_ if off <= SPINE_STOP_NEAR else "{} ({:.0f} m)".format(nm_, off)
            B.text(txt, fx + 0.75 * U, ly, th, INK, L, font=FONT_TITLE, bold=True)
        # the row's ends: level and, at the spine's ends, which way the stream runs
        for s, zl, za, kind in R["levels"]:
            if kind != "end":
                continue
            bx, by = P(s, zl)
            B.fill([[(bx, by), (bx - 0.22 * U, by + 0.38 * U), (bx + 0.22 * U, by + 0.38 * U)]], INK, L, 36)
            out = -1.0 if s < Lm * 0.5 else 1.0
            B.text("+{:.2f}".format(za), bx + out * 0.4 * U, by + 0.08 * U, 0.26 * U, INK, L,
                   align="L" if out > 0 else "R")
        for s, word, real in ((0.0, D["ends"][0], ri == 0), (Lm, D["ends"][1], ri == len(rows) - 1)):
            if real:                                      # the spine's ends: which way the stream runs
                calls.append((s, g_at(s), word.upper() + " END"))
            else:                                         # where the rows meet
                bx, by = P(s, g_at(s))
                B.line([(bx, by - 0.9 * U), (bx, by + 1.2 * U)], INK2, L, 36, 0.05)
        calls += spine_calls(R, g_at)
        low = sec_callouts(B, L, P, calls, P(0, -3.0)[1] - 0.45 * U, U, xlo=x, xhi=x + w)
        rib = low - 0.5 * U
        for a, b, cat in R["strip"]:
            B.fill([rect(P(a, 0)[0], rib - 0.16 * U, P(b, 0)[0], rib)], CAT[cat][1], L, 20)
        low = rib - 0.16 * U - 0.8 * U
    sb = nice_floor(max(b - a for a, b in rows) / 4.0)
    xb = x + w - SEC_END * U - sb * ss - 0.9 * U
    yb = low - 0.6 * U
    PANEL_RECTS["spine_section"] = (x, yb - 0.25 * U, x + w, top + 0.2 * U)
    draw_scalebar(B, xb, yb, ss, sb, U, L, h=0.26)
    B.text("1:{:,.0f} at {:.0f} mm · lengths and heights at one scale".format(
        nice_ratio(1000.0 / max(1e-9, ss * MMU)), SHEET_MM), x + SEC_END * U, yb + 0.1 * U, 0.24 * U, INK2, L)
    return yb - 0.35 * U
