# p.04-05 sections across the stream (split from parts/14_tsec_wind_arrows.py, parts/15_ndvi_col.py, parts/15c_review_pages.py, parts/15l_r28_site.py on 29 Oct 2026; moved unchanged)
# v51 (revision 29 Oct 2026, WO-T3a-3: package A "Pages 04-05", 02 §3 §4 §6, D4 b, D11, D13): each booklet page is ONE
# drawing that fills the panel (p45_plan, draw_sections_page): the page's key map on top (basemap "topographic", only
# this page's cut lines with their view triangles, inside the frame; draw_sections_key), under it the page's cuts at
# the largest round scale that fits, each beside a column with its name, its reading and its scale bar. Each cut is
# drawn as it really is (p45_strip): its banks and bed from the level module (section_parts: DSİ walls, embankments,
# loose earth; the bed at its level, 100- and 500-year flood levels, terraces), the measured trees at true size and the
# olive rows the survey shows (plants), the buildings at their floors, figures (_p45_fig); under it a segmented strip of
# what the cut crosses, each segment exactly under its part of the cut (R02). Callouts never overlap (one row each).
# The satellite rows, the building types diagram, the per-cut locator and the S4 key map (p14-15 draw their own) are gone.

P45_PAGES = (("S1", "S2", "S3", "S4"), ("S5", "S6", "S7", "S8"))   # p04, p05 (package A)
P45_ALONG = ("S5", "S6")          # cuts that run along the stream: cropped to the part around their crossings
P45_DENS = (2000, 2500, 5000)     # the round scales tried, largest first (SCRIPT_STANDARD §8)
P45_H = BK_AH - 2.0               # mm: the drawing's height on the booklet page (the panel, a 2 mm margin kept)
P45_TXT = dict(head=9.0, call=7.0, minor=6.0, strip=6.0, ctx=7.5)  # booklet pt: names, sentences + callouts, levels
P45_COL_MIN = 66.0                # mm: the column beside each cut (its name, reading, scale bar) at least this wide
P45_GAP = 4.0                     # mm: between a cut and its column, and between rows
P45_KEY_COL = 14.0                # mm: the key map's left column (KEY, the north arrow)
P45_KEY_MIN = 34.0                # mm: the key map at least this tall
P45_KEY_TXT = 78.0                # mm: kept right of the key map for the page's reading and the strip's colours
P45_MATCH_M = 3.0                 # m: a level row is drawn at the crossing whose bed is nearest, within this
P45_WALL_T_M = 0.60               # m: DSİ wall thickness: the value the site board drew (sec_cut chwalls, s +-0.30 m);
#                                   no source found (section_parts asks the caller): see WO-T3a-3 OPEN
P45_STRIP_WORD = {"residential": u"homes", "mixed": u"shops + homes", "commercial": u"shops", "institutional": u"civic",
                  "religious": u"heritage", "industrial": u"workshops", "transport": u"street", "green": u"green",
                  "agri": u"farmland", "vacant": u"vacant", "water": u"stream", "void": u"open ground"}
P45_TREE_KEY = {"olive": "olive", "pine": "stone_pine"}   # the survey's tree symbols -> plants.py species
P45_TREE_ANY = "plane"            # a measured tree with no species in the survey: the broadleaf primitive, unnamed
P45_BANK_WORD = {"dsi_wall": u"a DSİ stone wall", "embankment": u"an embankment", "loose_earth": u"a loose earth bank",
                 "no_crest": u"rising ground"}


def _p45_fig(B, L, pose, x, y, k, facing=1, view="side", col=None, order=34, height=1.75):
    """every human figure of pp.04-05: pose (stand, walk, watch, sit, touch, wade, bike) at true height, feet at
    (x, y) board units, k = board units per metre; facing -1 looks left; view "top": a plan figure (shoulders and
    head, one ink weight, a light flat fill)"""
    # swap point: figures.py fig_side/fig_top when the silhouette set arrives
    c_ = col or mix(INK, PAPER, 0.2)
    if view == "top":
        sh = [(x + 0.25 * k * math.cos(t * math.pi / 12.0), y + 0.14 * k * math.sin(t * math.pi / 12.0))
              for t in range(24)]
        hd = circle_pts(x, y, 0.11 * k, 12)
        for P_ in (sh, hd):
            B.fill([P_], mix(c_, WHITE, 0.7), L, order)
            B.line(P_ + [P_[0]], c_, L, order + 1, 0.04)
        return
    for P_ in fig_polys(pose, height, facing):
        B.fill([[(x + px * k, y + py * k) for px, py in P_]], c_, L, order)


def _p45_c(c):
    return C(c) if isinstance(c, str) else c


def _p45_put(B, L, shapes, T, kb, order):
    """the modules' house shapes ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw) (booklet mm, y up)
    through T (mm -> board units), line weights in booklet mm"""
    for sh in shapes or []:
        if not sh:
            continue
        if sh[0] == "poly":
            pts = [T(p) for p in sh[1]]
            if len(pts) < 3:
                continue
            if sh[2]:
                B.fill([pts], _p45_c(sh[2]), L, order)
            if len(sh) > 3 and sh[3]:
                B.line(pts + [pts[0]], _p45_c(sh[3]), L, order, bk_lw((sh[4] if len(sh) > 4 else None) or 0.1, kb))
        elif sh[0] == "line":
            B.line([T(p) for p in sh[1]], _p45_c(sh[2]), L, order, bk_lw((sh[3] if len(sh) > 3 else None) or 0.1, kb))


def p45_rows_of(nm):
    """the level module's row ids of cut nm (one, or one per crossing on S5/S6); [] without the module"""
    try:
        ids = level_ids()
    except Exception:
        return []
    out = []
    for i in ids:
        try:
            r = level_cut(i)
        except Exception:
            continue
        if i == nm or r.get("cut") == nm:
            out.append(i)
    return out


def p45_sides(sd_):
    """(the bank at the cut's start, the bank at its end) as the level module names them ("NE"/"SW"): the end
    lying further north-east (survey x east, y north) is on the north-east bank"""
    x0, y0, x1, y1 = sd_["line"][:4]
    return ("NE", "SW") if x0 + y0 > x1 + y1 else ("SW", "NE")


def p45_reach(sd_, x_e, dirn, zt, far=60.0):
    """where the surveyed ground, going out from x_e (dirn -1 left, +1 right), first reaches the level zt (relative
    to the cut's base); None within far m"""
    gr = sd_["ground"]
    n = len(gr)
    i = max(0, min(n - 1, int(round(x_e / 0.5))))
    while 0 <= i < n and abs(gr[i][0] - x_e) <= far:
        if gr[i][1] >= zt - 0.02:
            return gr[i][0]
        i += int(dirn)
    return None


def p45_banks(sd_):
    """the cut's stream crossings with a row in the level module (02 §6): [dict(k, rid, a, b, bed, zb, f, sides)],
    sides = [left, right] dicts (side, typ, x, dirn, top, zt, h, ang, crest). The bed, the bank and wall tops,
    their types and angles are the level module's (D4 b: S4 +42.48); the place of the water on the cut is the site
    board's (its run a..b). A row goes to the crossing whose bed is nearest (P45_MATCH_M), across the stream first.
    Memoised on the cut."""
    if "_p45b" in sd_:
        return sd_["_p45b"]
    out = []
    runs = sd_["water"]
    base = sd_["base"]
    rows = p45_rows_of(sd_["name"])
    bks = sd_.get("banks") or []
    m = {}
    if len(rows) == 1 and runs:
        m[site28_main_k(sd_)] = rows[0]
    elif rows and runs:
        free = list(range(len(runs)))
        for rid in rows:
            bed = level(rid, "bed")
            if bed is None or not free:
                continue
            j = min(free, key=lambda j_: ((bks[j_] if j_ < len(bks) else {}).get("ang", 90.0) < SITE28_CROSS,
                                          abs(runs[j_][2] + base - bed)))
            if abs(runs[j][2] + base - bed) > P45_MATCH_M:
                continue
            m[j] = rid
            free.remove(j)
    left, right = p45_sides(sd_)
    for k_ in sorted(m):
        rid = m[k_]
        bed = level(rid, "bed")
        if bed is None:
            continue
        a, b = runs[k_][0], runs[k_][1]
        zb = bed - base
        row = level_cut(rid)
        ang_c = level(rid, "angle_deg")
        f = 1.0 / max(0.25, math.sin(math.radians(ang_c))) if ang_c else 1.0   # along the cut, not across the stream
        sides = []
        for nm_s, x_e, dirn in ((left, a, -1.0), (right, b, 1.0)):
            typ = (row.get(nm_s) or {}).get("type") or "no_crest"
            top = level(rid, "top", nm_s)
            ang = level(rid, "angle_deg", nm_s)
            zt = None if top is None else top - base
            if typ == "dsi_wall" and zt is None:
                zt = zb + SCT_DSI_WALL_H_M
            crest = None
            if typ == "dsi_wall":
                crest = x_e + dirn * P45_WALL_T_M * f
            elif typ == "embankment" and ang and zt is not None and zt > zb:
                crest = x_e + dirn * (zt - zb) / math.tan(math.radians(ang)) * f
            elif zt is not None:
                crest = p45_reach(sd_, x_e, dirn, zt)
            if crest is not None:
                crest = max(0.0, min(sd_["L"], crest))
            sides.append(dict(side=nm_s, typ=typ, x=x_e, dirn=dirn, top=top, zt=zt, h=level(rid, "height", nm_s),
                              ang=ang, crest=crest))
        out.append(dict(k=k_, rid=rid, a=a, b=b, bed=bed, zb=zb, f=f, sides=sides))
    sd_["_p45b"] = out
    return out


def p45_ground(sd_):
    """the cut's ground [(s, z)] as drawn: the surveyed ground, and at each crossing of p45_banks the banks as they
    are (a DSİ wall: its water face up to its top and its thickness; an embankment: toe to top at its angle; loose
    earth: the surveyed slope down to the bed) and the bed flat at its level. Memoised on the cut."""
    if "_p45g" in sd_:
        return sd_["_p45g"]
    g = list(sd_["ground"])
    for cr in p45_banks(sd_):
        l_, r_ = cr["sides"]
        zb = cr["zb"]
        sl = min(cr["a"], l_["crest"] if l_["crest"] is not None else cr["a"])
        sr = max(cr["b"], r_["crest"] if r_["crest"] is not None else cr["b"])
        mid = []
        if l_["typ"] == "dsi_wall":
            mid += [(sl, l_["zt"]), (cr["a"], l_["zt"]), (cr["a"], zb)]
        elif l_["typ"] == "embankment" and l_["crest"] is not None and l_["crest"] < cr["a"]:
            mid += [(sl, l_["zt"]), (cr["a"], zb)]
        else:
            mid += [(s, max(z, zb)) for s, z in sd_["ground"] if sl <= s < cr["a"]] + [(cr["a"], zb)]
        mid.append((cr["b"], zb))
        if r_["typ"] == "dsi_wall":
            mid += [(cr["b"], r_["zt"]), (sr, r_["zt"])]
        elif r_["typ"] == "embankment" and r_["crest"] is not None and r_["crest"] > cr["b"]:
            mid += [(sr, r_["zt"])]
        else:
            mid += [(s, max(z, zb)) for s, z in sd_["ground"] if cr["b"] < s <= sr]
        g = [p for p in g if p[0] < sl - 1e-6] + mid + [p for p in g if p[0] > sr + 1e-6]
        cr["win"] = (sl, sr)
    sd_["_p45g"] = g
    return g


def p45_span(g, c, zq):
    """(s left, s right) to which water at the level zq spreads over the ground g from s = c; None if c is dry"""
    if not g:
        return None
    i = min(range(len(g)), key=lambda j: abs(g[j][0] - c))
    if g[i][1] >= zq:
        return None

    def walk(rng):
        prev = g[i]
        for j in rng:
            q = g[j]
            if q[1] >= zq:
                t = (zq - prev[1]) / (q[1] - prev[1]) if abs(q[1] - prev[1]) > 1e-9 else 0.0
                return prev[0] + t * (q[0] - prev[0])
            prev = q
        return prev[0]
    return walk(range(i - 1, -1, -1)), walk(range(i + 1, len(g)))


def p45_bank_word(sd):
    """a bank's callout from the level module: its kind and its top (heights m, 2 decimals)"""
    if sd["top"] is None and sd["typ"] != "dsi_wall":
        return None
    if sd["typ"] == "dsi_wall":
        hw_ = u_height(sd["h"] if sd["h"] is not None else SCT_DSI_WALL_H_M)
        if sd["top"] is None:
            return u"DSİ stone wall · {} high".format(hw_)
        return u"DSİ stone wall · top {} · {} high".format(u_level(sd["top"]), hw_)
    if sd["typ"] == "embankment":
        return u"embankment{} · top {}".format(u" {:.0f}°".format(sd["ang"]) if sd["ang"] else u"", u_level(sd["top"]))
    if sd["typ"] == "loose_earth":
        return u"loose earth bank · top {}".format(u_level(sd["top"]))
    return None


def p45_symbols(S, sd_):
    """the survey's tree symbols near the cut: [(s along, d to the left of the cut, kind)], memoised"""
    if "_p45t" in sd_:
        return sd_["_p45t"]
    x0, y0, x1, y1 = sd_["line"][:4]
    Lc = math.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / Lc, (y1 - y0) / Lc
    out = []
    for t in getattr(S, "trees", None) or []:
        tx, ty, kind = t[0], t[1], t[3]
        s = (tx - x0) * ux + (ty - y0) * uy
        d = (tx - x0) * -uy + (ty - y0) * ux
        if -5.0 <= s <= Lc + 5.0 and -8.0 <= d <= 75.0:
            out.append((s, d, kind))
    sd_["_p45t"] = out
    return out


def p45_kind(S, sd_, s, d, r):
    """the plants.py species of a measured crown at (s, d) from the nearest survey symbol within its radius"""
    best = None
    for s_, d_, kind in p45_symbols(S, sd_):
        e = math.hypot(s_ - s, d_ - d)
        if e <= max(2.5, r) and (best is None or e < best[0]):
            best = (e, kind)
    return P45_TREE_KEY.get(best[1], P45_TREE_ANY) if best else P45_TREE_ANY


def p45_segments(sd_, minw):
    """what the cut crosses as segments [[s0, s1, cat]]: runs of one kind merged, slivers under minw m given to a
    neighbour (the stream never)"""
    segs = []
    for a, b, cat in sd_["strip"]:
        if segs and segs[-1][2] == cat:
            segs[-1][1] = b
        else:
            segs.append([a, b, cat])
    out = []
    for sg in segs:
        if out and sg[1] - sg[0] < minw and sg[2] != "water":
            out[-1][1] = sg[1]
        elif out and out[-1][1] - out[-1][0] < minw and out[-1][2] != "water":
            sg[0] = out[-1][0]
            out[-1] = sg
        else:
            out.append(sg)
    res = []
    for sg in out:
        if res and res[-1][2] == sg[2]:
            res[-1][1] = sg[1]
        else:
            res.append(list(sg))
    return res


def p45_end(kb):
    """the room (board units) at both ends of a cut for its end name and end level"""
    hd, hm = bk_hk(P45_TXT["head"], kb), bk_hk(P45_TXT["minor"], kb)
    return max(site28_tw(u"+888.88", hm), site28_tw(u"S8'", hd, True)) + 2.0 * kb


def p45_dep(cr):
    """a crossing's bed in words, from the level module: between DSİ walls, or how deep below the lower open bank"""
    walls = [sd for sd in cr["sides"] if sd["typ"] == "dsi_wall"]
    if len(walls) == 2:
        return u"the bed at {} lies between **DSİ stone walls {} high**".format(
            u_level(cr["bed"]), u_height(max(sd["h"] if sd["h"] is not None else SCT_DSI_WALL_H_M for sd in walls)))
    open_ = [sd for sd in cr["sides"] if sd["top"] is not None and sd["typ"] != "dsi_wall"]
    if open_:
        lo = min(open_, key=lambda sd: sd["top"])
        return u"the bed at {} lies **{} below** the lower bank, {}".format(
            u_level(cr["bed"]), u_height(lo["top"] - cr["bed"]), P45_BANK_WORD.get(lo["typ"], u"a bank"))
    return u"the bed lies at {}".format(u_level(cr["bed"]))


def draw_section_strip(S, B, sd_, x, y, w, ss, U, dry=False, tag="page", scale_txt=None, loc=True):
    """v51: one cut, drawn by p45_strip from y down in a column w wide (the old signature, kept for the core's
    sections_plan, which measures cuts with it); returns the y below. tag, scale_txt and loc are no longer used (the
    page draws the cut's name, reading and scale bar beside it, and one key map)."""
    kb = (sd_.get("_p45") or sd_.get("_txt") or {}).get("k") or 140.0 * U / BK_AW
    return p45_strip(S, B, sd_, x, y, w, ss, kb, U, dry=dry)


def p45_strip(S, B, sd_, x, ytop, wd, ss, kb, U, dry=False, L="LU_BOARD::Sections"):
    """v51 (WO-T3a-3; package A p04-05, 02 §3 §4 §6, R02): one cut as it really is, from ytop down in a column wd
    wide, its start at x + p45_end (ss board units per metre, kb per booklet mm): behind it the buildings and trees
    beyond (paler); the cut ground (p45_ground) with the banks and bed of the level module through section_parts
    (DSİ walls, embankments, earth, the gravel bed), the 100- and 500-year flood water, the terraces; the cut
    buildings at their floors with their tags; the measured trees at true size (plants, species from the survey's
    symbols), the survey's olive rows where the cut crosses them, figures where people stand; its end names and
    levels outside it; under it the segmented strip of what it crosses, each segment under its part of the cut; then
    the callouts, each on its own row (site28_callouts). dry: only what sets the height. Returns the y below."""
    nm = sd_["name"]
    Lm = sd_["L"]
    off = sd_.get("s_off", 0.0)
    base = sd_["base"]
    hd, hc, hm, hst = [bk_hk(P45_TXT[q], kb) for q in ("head", "call", "minor", "strip")]
    end = p45_end(kb)
    km = ss / kb                                          # booklet mm per metre: the modules' k
    crs = p45_banks(sd_)
    g = p45_ground(sd_)
    zmax = max([sd_["zmax"]] + [sd["zt"] + 0.5 for cr in crs for sd in cr["sides"] if sd["zt"] is not None])
    zbot = min(-3.0, min(z for s, z in g) - 1.2) if g else -3.0
    X0 = x + end
    room = max([1.5 * kb] + [0.9 * hm + hd + 0.5 * kb - (zmax - g_[1]) * ss for g_ in ((g[0], g[-1]) if g else ())])
    Y0 = ytop - room - zmax * ss                          # the end names over their levels stay under ytop

    def P(px, pz):
        return (X0 + px * ss, Y0 + pz * ss)

    def T(q):                                             # module shapes: booklet mm from the cut's origin
        return (X0 + q[0] * kb, Y0 + q[1] * kb)

    gr = sd_["ground"]

    def g_at(s):
        return gr[max(0, min(len(gr) - 1, int(round(s / 0.5))))][1]

    def gy_mm(xm):
        return g_at(xm / km) * km
    tags_ = []
    if not dry:
        # ---- beyond the cut: buildings and trees, paler with distance (far first)
        for a, b, zb_, zt_, cat, d, floors, annex, fabric, flags, fsrc in sd_.get("beyond") or []:
            col = mix(sa_board_bld(dict(cat=cat, fabric=fabric, annex=annex)), WHITE, min(0.8, 0.3 + 0.5 * d / 75.0))
            r0, r1 = P(a, zb_), P(b, zt_)
            B.fill([rect(r0[0], r0[1], r1[0], r1[1])], col, L, 12)
        for i, (s, zg, tr, lo, hi, d) in enumerate(sd_.get("btrees") or []):
            key = p45_kind(S, sd_, s, d, tr)
            _p45_put(B, L, pla_section(key, s * km, zg * km, km, h_m=hi, crown_m=max(1.5, 2.0 * tr), beyond=True,
                                       seed=i), T, kb, 13)
        # ---- the cut ground: poche, then the banks' earth and the bed in their materials
        B.fill([[P(s, z) for s, z in g] + [P(Lm, zbot), P(0.0, zbot)]], SEC_SOIL, L, 20)
        for cr in crs:
            sl, sr = cr.get("win", (cr["a"], cr["b"]))
            w0, w1 = max(0.0, sl - 6.0), min(Lm, sr + 6.0)
            ring = [(s * km, z * km) for s, z in g if w0 <= s <= w1]
            if len(ring) >= 2 and w1 - w0 < 160.0:
                ring += [(ring[-1][0], (cr["zb"] - 1.0) * km), (ring[0][0], (cr["zb"] - 1.0) * km)]
                _p45_put(B, L, sct_hatch_fill(ring, "earth", km), T, kb, 21)
            _p45_put(B, L, sct_bed(cr["a"] * km, cr["b"] * km, cr["zb"] * km, km, depth_m=1.0), T, kb, 23)
            for sd in cr["sides"]:
                side = 1.0 if sd["dirn"] > 0 else -1.0
                if sd["typ"] == "dsi_wall":
                    sh, _ = sct_bank("dsi_wall", sd["x"] * km, sd["zt"] * km, cr["zb"] * km, side, km,
                                     t_m=P45_WALL_T_M * cr["f"], reach_m=0.3, depth_m=1.0)
                    _p45_put(B, L, sh, T, kb, 24)
                elif sd["typ"] == "embankment" and sd["crest"] is not None and sd["zt"] is not None \
                        and abs(sd["crest"] - sd["x"]) > 0.2:
                    sh, _ = sct_bank("embankment", sd["x"] * km, sd["zt"] * km, cr["zb"] * km, side, km,
                                     run_m=abs(sd["crest"] - sd["x"]), reach_m=0.3, depth_m=1.0)
                    _p45_put(B, L, sh, T, kb, 24)
            # the 100- and 500-year flood water (level module), tinted to the 100-year line
            c_ = 0.5 * (cr["a"] + cr["b"])
            for key, col, wl_, tint in (("q500", mix(BLUE_D, WHITE, 0.35), 0.18, False),
                                        ("q100", BLUE_D, 0.25, True)):
                q = level(cr["rid"], key)
                sp = p45_span(g, c_, q - base) if q is not None else None
                if not sp:
                    continue
                zq = q - base
                if tint:
                    poly = [P(sp[0], zq), P(sp[1], zq)] + [P(s, z) for s, z in reversed(g) if sp[0] < s < sp[1]]
                    B.fill([poly], mix(BLUE_L, WHITE, 0.35), L, 22)
                for d_ in r28_pattern([P(sp[0], zq), P(sp[1], zq)], [m_ * kb for m_ in (1.6, 0.8)]):
                    B.line(d_, col, L, 25, bk_lw(wl_, kb))
            # the level shelves (terraces) the level module finds on the banks
            for t_ in (level_cut(cr["rid"]).get("terraces") or []):
                lv = (t_.get("level") or {}).get("value")
                sd = next((q_ for q_ in cr["sides"] if q_["side"] == t_.get("side")), None)
                if lv is None or sd is None:
                    continue
                sa_, sb_ = [c_ + sd["dirn"] * m_ * cr["f"] for m_ in (t_.get("from_m", 0.0), t_.get("to_m", 0.0))]
                if 0.0 <= min(sa_, sb_) and max(sa_, sb_) <= Lm:
                    B.line([P(sa_, lv - base), P(sb_, lv - base)], INK, L, 26, bk_lw(0.35, kb))
        # ---- cut buildings: the volume to its height, a line at every storey, its tag (as sec_cut, v50)
        for a, b, z0, z1, cat, annex, ftype, fl, floors, fsrc in sd_["bld"]:
            r0, r1 = P(a, z0), P(b, z1)
            if b - a < 1.2:
                B.fill([rect(r0[0], r0[1], r1[0], r1[1])], SEC_WALL, L, 28)
                continue
            heritage = ftype in ("monument", "sacred")
            room = mix(typo_tone(ftype, cat), PAPER, 0.12 + (0.15 if annex else 0.0))
            wall_c = mix(FABRIC[ftype][2], INK, 0.45) if heritage else INK
            prof = bld_profile(ftype, cat, a, b, z0, z0, z1, floors, fsrc == "published", seed=int(a * 7.0),
                               ruin=fl[2], minaret=fl[3] if len(fl) > 3 else None)
            bld_draw_cut(B, L, P, prof, room, wall_c, ss, U, order=27)
            tag_ = typo_label(ftype, cat, floors, fl[0], fl[4] if len(fl) > 4 else "")
            lab_ = None if annex else site28_tag_fit(tag_, (b - a) * ss, hm)
            if lab_:
                site28_bld_tag(B, L, P, prof, lab_, hm, wall_c, U, tags_)
        # ---- the cut line, broken inside the cut buildings
        spans = sorted((a, b) for a, b, z0, z1, cat, annex, ftype, fl, floors, fsrc in sd_["bld"])
        run = []
        for s, z in g:
            if any(a_ + 0.01 < s < b_ - 0.01 for a_, b_ in spans):
                if len(run) >= 2:
                    B.line(run, INK, L, 26, bk_lw(0.35, kb))
                run = []
                continue
            run.append(P(s, z))
        if len(run) >= 2:
            B.line(run, INK, L, 26, bk_lw(0.35, kb))
        for s, zg in sd_["walls"]:                       # a surveyed wall: its place on the ground (no height surveyed)
            bx, by = P(s, zg)
            B.fill([[(bx, by + 1.0 * kb), (bx - 0.6 * kb, by), (bx + 0.6 * kb, by)]], SEC_WALL, L, 28)
        # ---- planting at true size (02 §4): the measured trees on the cut; olive rows where the survey shows them
        for i, (s, zg, hw, lo, hi) in enumerate(sd_["trees"]):
            key = p45_kind(S, sd_, s, 0.0, hw)
            _p45_put(B, L, pla_section(key, s * km, zg * km, km, h_m=hi, crown_m=max(1.5, 2.0 * hw), seed=i),
                     T, kb, 32)
        for a, b, cat in p45_segments(sd_, 4.0):
            if cat != "agri" or b - a < 10.0:
                continue
            if p45_olives(S, sd_, a, b):
                _p45_put(B, L, pla_crop_rows("olive", a * km, b * km, gy_mm, km), T, kb, 32)
            elif not sd_.get("_p45_nocrop"):
                sd_["_p45_nocrop"] = True
                LOG.append(u"Section {}: farmland on the cut with no crop in the survey or OpenStreetMap: drawn as "
                           u"field ground only (no rows).".format(nm))
        # ---- figures where people are (02 §3): at each bank top, looking at the water; one on the widest street
        for cr in crs:
            for sd in cr["sides"]:
                if sd["crest"] is None:
                    continue
                zf = sd["zt"] if sd["typ"] in ("dsi_wall", "embankment") and sd["zt"] is not None else g_at(sd["crest"])
                fx, fy = P(sd["crest"] + sd["dirn"] * 0.8, zf)
                _p45_fig(B, L, "watch", fx, fy, ss, facing=-sd["dirn"])
        st_ = [sg for sg in p45_segments(sd_, 2.0) if sg[2] == "transport"]
        if st_:
            a, b, cat = max(st_, key=lambda q_: q_[1] - q_[0])
            fx, fy = P(0.5 * (a + b), g_at(0.5 * (a + b)))
            _p45_fig(B, L, "walk", fx, fy, ss, facing=1)
    road_calls = draw_sec_roads(S, B, L, P, g_at, sd_["line"], Lm, U, off=off)   # v25: the streets crossed
    # ---- the ends: name over its level, outside the cut (a cropped end: a break, its level only)
    co = sd_.get("crop_of")
    for s_, lab, out in ((0.0, nm, -1.0), (Lm, nm + u"'", 1.0)):
        real = not co or (s_ == 0.0 and co[1] <= 0.01) or (s_ == Lm and co[1] + Lm >= co[0] - 0.01)
        bx, by = P(s_, g[0][1] if s_ == 0.0 else g[-1][1])
        t_ = u_level(g_at(s_) + base)
        xa = bx + out * 1.0 * kb
        site28_text(B, t_, xa, by - 0.5 * hm, hm, INK, L, align="L" if out > 0 else "R")
        if real:
            site28_text(B, u"**{}**".format(lab), xa, by + 0.9 * hm, hd, INK, L, align="L" if out > 0 else "R")
        else:
            B.line([(bx - 0.6 * kb, by - 2.0 * kb), (bx + 0.6 * kb, by - 0.7 * kb), (bx - 0.6 * kb, by + 0.7 * kb),
                    (bx + 0.6 * kb, by + 2.0 * kb)], INK2, L, 36, bk_lw(0.18, kb))
    # the tallest cut roof: its level, as on an architectural section
    if sd_["bld"] and not dry:
        a, b, z0, z1, cat, annex, ftype, fl, floors, fsrc = max(sd_["bld"], key=lambda t: t[3])
        lev_ = u_level(z1 + base)
        lw_ = site28_tw(lev_, hm)
        for side in ((1.0, -1.0) if (b - a) * ss > 0.6 * U else ()):
            bx, by = P(b if side > 0 else a, z1)         # v16.3: at the eaves beside the wall, clear of the type's tag
            bx += side * 0.4 * U
            t0, t1 = (bx - 0.16 * U, bx + 0.25 * U + lw_) if side > 0 else (bx - 0.25 * U - lw_, bx + 0.16 * U)
            if any(t0 < x1_ and x0_ < t1 and -(hm + 0.2 * U) < y_ - by < hm + 0.2 * U for x0_, x1_, y_ in tags_):
                continue                                 # v40: never over a building's tag; else the other wall
            B.line([(bx - side * 0.4 * U, by), (bx + side * 0.16 * U, by)], INK, L, 36, 0.04)
            B.fill([[(bx, by), (bx - 0.16 * U, by + 0.28 * U), (bx + 0.16 * U, by + 0.28 * U)]], INK, L, 36)
            site28_text(B, lev_, bx + 0.25 * U if side > 0 else bx - 0.25 * U - lw_, by + 0.06 * U, hm, INK, L)
            break
    # ---- the segmented strip (R02): what the cut crosses, each segment exactly under its part of the cut
    ys = P(0.0, zbot)[1] - 0.6 * kb
    hb = max(1.9 * hst, 2.6 * kb)
    for a, b, cat in p45_segments(sd_, 1.2 / km):
        xa_, xb_ = P(a, 0)[0], P(b, 0)[0]
        col = CAT[cat][1] if cat != "void" else mix(KHAKI, PAPER, 0.55)
        B.fill([rect(xa_, ys - hb, xb_, ys)], col, L, 20)
        B.line([(xb_, ys - hb), (xb_, ys)], WHITE, L, 21, bk_lw(0.25, kb))
        w_ = P45_STRIP_WORD.get(cat, cat)
        if xb_ - xa_ > site28_tw(w_, hst) + 1.2 * kb:
            dark = sum(col[:3]) < 420
            B.text(w_, 0.5 * (xa_ + xb_), ys - 0.5 * (hb + hst), hst, WHITE if dark else INK, L, order=22,
                   font=FONT_TITLE, align="C")
    # ---- the callouts, each on its own row (site28_callouts): the water and banks (level module) first, then
    # terraces and history, then streets and places; levels and heights in m with 2 decimals, widths in cm
    calls = []
    for cr in crs:
        bw = level(cr["rid"], "bed_width_cm")
        calls.append((cr["a"] + 0.7 * (cr["b"] - cr["a"]), cr["zb"], u"bed {}{}".format(
            u_level(cr["bed"]), u" · {} wide".format(u_dim(bw / 100.0)) if bw else u""), 0))
        for sd in cr["sides"]:
            t_ = p45_bank_word(sd)
            if t_:
                sx = sd["crest"] if sd["crest"] is not None else sd["x"]
                calls.append((sx, sd["zt"] if sd["zt"] is not None else g_at(sx), t_, 0))
        q1, q5 = level(cr["rid"], "q100"), level(cr["rid"], "q500")
        if q1 is not None:
            calls.append((cr["a"] + 0.3 * (cr["b"] - cr["a"]), q1 - base, u"100-year flood {}{}".format(
                u_level(q1), u" · 500-year {}".format(u_level(q5)) if q5 is not None else u""), 0))
        c_ = 0.5 * (cr["a"] + cr["b"])
        for t_ in (level_cut(cr["rid"]).get("terraces") or []):
            lv = (t_.get("level") or {}).get("value")
            sd = next((q_ for q_ in cr["sides"] if q_["side"] == t_.get("side")), None)
            if lv is None or sd is None:
                continue
            sm_ = c_ + sd["dirn"] * 0.5 * (t_.get("from_m", 0.0) + t_.get("to_m", 0.0)) * cr["f"]
            if 0.0 <= sm_ <= Lm:
                calls.append((sm_, lv - base, u"terrace {}".format(u_level(lv)), 1))
    calls += [((a + b) / 2.0, g_at((a + b) / 2.0), nm_, 3) for a, b, nm_ in sd_.get("places", [])]
    for s_, z_, t_ in road_calls:
        c2 = site28_road_call(t_)
        calls.append((s_, z_, c2[0], c2[1]))
    calls += [(s_, g_at(s_), t_, 1) for s_, t_ in sec_history_calls(S, sd_) if 0.0 <= s_ <= Lm]
    low, left_ = site28_callouts(B, L, P, calls, ys - hb - 1.0 * kb, U, hc, x, x + wd)
    if left_ and not dry:
        LOG.append(u"Section {}: {} callout(s) left out, no free row under the cut: {}.".format(nm, len(left_),
                                                                                             u"; ".join(left_)))
    return min(low, ys - hb) - 0.8 * kb


def p45_olives(S, sd_, a, b):
    """True where the cut's farmland a..b is an olive grove in the data: the survey's olive symbols on it (within
    15 m of the cut) or an OpenStreetMap orchard tagged with olive trees"""
    if any(kind == "olive" and a <= s <= b and abs(d) <= 15.0 for s, d, kind in p45_symbols(S, sd_)):
        return True
    x0, y0, x1, y1 = sd_["line"][:4]
    Lc = math.hypot(x1 - x0, y1 - y0) or 1.0
    sm = 0.5 * (a + b)
    mx, my = x0 + (x1 - x0) * sm / Lc, y0 + (y1 - y0) * sm / Lc
    for z in S.g_agri.query((mx - 1.0, my - 1.0, mx + 1.0, my + 1.0)):
        if (z.get("tags") or {}).get("trees") == "olive_trees" and region_contains(mx, my, z["Ps"], z.get("Hs") or []):
            return True
    return False


def sec_history_calls(S, sd_):
    """v44 (PHASE2_SPEC §3, p.7-8): where a cut crosses the survey's historic city wall line (layer SINIR_TARIHI_SUR,
    S.walls_hist) or the covered course of the stream (OSM tunnel / culvert, S.covered): [(s, text)] along the cut.
    Only what the data holds: the survey layer does not date the wall, so no period is named."""
    x0, y0, x1, y1, nm = sd_["line"]
    Lc = math.hypot(x1 - x0, y1 - y0)
    if Lc <= 0:
        return []
    out = []
    for key, txt in (("walls_hist", u"historic city wall"), ("covered", u"covered stream")):
        for P in getattr(S, key, None) or []:
            for a, b in zip(P[:-1], P[1:]):
                hit = seg_x((x0, y0), (x1 - x0, y1 - y0), a, (b[0] - a[0], b[1] - a[1]))
                if hit:
                    s_ = hit[0] * Lc
                    if all(abs(s_ - q) > 3.0 or t_ != txt for q, t_ in out):
                        out.append((s_, txt))
    return out


def sections_context(S, names=None):
    """v51 (WO-T3a-3, 02 §6, D13): the reading of a page's cuts (names; all when None), every level from the level
    module: how deep the bed lies below the lower open bank top, the DSİ walls' height where the cuts meet them;
    bold keywords. No status or internal source is printed."""
    nms = [sd_["name"] for sd_ in S.sections if names is None or sd_["name"] in names]
    d, walls = [], []
    for nm in nms:
        for rid in p45_rows_of(nm):
            row = level_cut(rid)
            hs = []
            for s_ in ("NE", "SW"):
                typ = (row.get(s_) or {}).get("type")
                h = level(rid, "height", s_)
                if h is None:
                    continue
                if typ == "dsi_wall":
                    walls.append(h)
                elif typ in ("embankment", "loose_earth"):
                    hs.append(h)
            if hs:
                d.append(min(hs))
    txt = u"**{} cuts across the Selinos stream**, each drawn as it is: the ground, the bed and banks, the buildings, " \
          u"trees and fields it crosses; the strip under each cut names what it crosses".format(len(nms))
    if d:
        txt += u" · the bed **{} below** the lower open bank".format(
            u"{:.2f}-{}".format(min(d), u_height(max(d))) if len(d) > 1 and max(d) - min(d) >= 0.005 else u_height(d[0]))
    if walls:
        txt += u" · **DSİ stone walls {} high** in the walled town reach".format(u_height(max(walls)))
    return txt + u"."


def p45_crop(S, sd_, Lmax):
    """the part of a cut Lmax m long around its stream (sec_cropped), once per run"""
    memo = getattr(S, "_p45_crop", None)
    if memo is None:
        memo = {}
        S._p45_crop = memo
    key = (sd_["name"], round(Lmax, 1))
    if key not in memo:
        memo[key] = sec_cropped(S, sd_, Lmax)
    return memo[key]


def p45_bar_h(kb, U):
    """the height of a cut's scale bar with its numbers (board units)"""
    return 0.38 * U + 0.35 * U + bk_hk(P45_TXT["minor"], kb) + 0.6 * kb


def p45_bar(B, x, y, w, ss, sd_, den, kb, U, L="LU_BOARD::Sections"):
    """a cut's scale bar beside it (02 §8: beside every orthogonal drawing), its foot at y, with the ratio"""
    hm = bk_hk(P45_TXT["minor"], kb)
    sb = nice_floor(max(1.0, min(sd_["L"] / 4.0, 0.5 * w / ss)))
    draw_scalebar(B, x, y, ss, sb, U, L, h=hm / U)
    site28_text(B, u"1:{:,}".format(int(den)), x + sb * ss + 0.9 * U + site28_tw(u"m", hm) + 2.0 * kb, y, hm, INK, L)


def p45_head(S, B, sd_, x, y, w, kb, U, L="LU_BOARD::Sections"):
    """the column beside a cut: its name, its key sentence and what on it steers the project (site28_sec_reading),
    the public source of a bed width where there is one (level_public_source; nothing else is credited, D13).
    Returns the y below."""
    hd, hc, hm = bk_hk(P45_TXT["head"], kb), bk_hk(P45_TXT["call"], kb), bk_hk(P45_TXT["minor"], kb)
    nm = sd_["name"]
    yy = y - hd
    site28_text(B, u"**SECTION {0} — {0}'**".format(nm), x, yy, hd, INK, L)
    if sd_.get("crop_of"):
        yy -= 1.5 * hm
        site28_text(B, u"the part around the stream", x, yy, hm, INK2, L)
    key_, steer_ = site28_sec_reading(S, sd_)
    yy -= 0.5 * hd + 1.3 * hc
    for t_, c_ in ((key_, INK), (steer_, INK2)):
        if t_:
            yy = site28_para(B, t_, x, yy, w, hc, c_, L, lead=1.45, bcol=INK)
    srcs = []
    for cr in p45_banks(sd_):
        src = level_public_source(cr["rid"], "bed_width_cm")
        bw = level(cr["rid"], "bed_width_cm")
        if src and bw:
            t_ = u"Bed width {}: {}".format(u_dim(bw / 100.0), src)
            if t_ not in srcs:
                srcs.append(t_)
    for t_ in srcs:
        yy = site28_para(B, t_, x, yy - 0.2 * hc, w, hm, INK2, L, lead=1.4)
    return yy + 0.4 * hc


def p45_plan(S, sw, U):
    """v51 (WO-T3a-3, package A "fill the page"): the two sections pages (P45_PAGES: p04 S1-S4, p05 S5-S8), each at
    the largest round scale P45_DENS at which its cuts, the columns beside them and a key map at least P45_KEY_MIN
    tall fit the booklet panel (sw board units = BK_AW mm); a cut longer than the drawing column is cropped to the
    part around the stream (S5, S6 always may be; the others keep >= SEC_KEEP). Returns (dens, sss, pages, P):
    pages as sections_plan's ([[row of (cut, width)]]: the core's page count and names), P the pages' plans
    dict(den, ss, wd, wc, rows=[(cut, height)], need, names). Memoised per run."""
    memo = getattr(S, "_p45_plan", None)
    if memo and memo[0] == sw:
        return memo[1]
    kb = sw / BK_AW
    end = p45_end(kb)
    out = []
    for names in P45_PAGES:
        secs = [sd_ for nm in names for sd_ in S.sections if sd_["name"] == nm]
        if not secs:
            continue
        pick = None
        for den in P45_DENS:
            ss = kb * 1000.0 / den
            Lmax = (sw - (P45_COL_MIN + P45_GAP) * kb - 2.0 * end) / ss
            cuts, ok = [], True
            for sd_ in secs:
                if sd_["L"] <= Lmax:
                    cuts.append(sd_)
                elif sd_["name"] in P45_ALONG or sd_["L"] * SEC_KEEP <= Lmax:
                    cuts.append(p45_crop(S, sd_, Lmax))
                else:
                    ok = False
                    break
            if not ok:
                continue
            wd = max(c_["L"] for c_ in cuts) * ss + 2.0 * end
            wc = sw - wd - P45_GAP * kb
            rows = []
            n0 = len(LOG)
            for c_ in cuts:
                c_["_p45"] = dict(k=kb, den=den)
                hs_ = -p45_strip(S, Board(), c_, 0.0, 0.0, wd, ss, kb, U, dry=True)
                hh_ = -p45_head(S, Board(), c_, 0.0, 0.0, wc, kb, U) + p45_bar_h(kb, U) + 1.0 * kb
                rows.append((c_, max(hs_, hh_)))
            del LOG[n0:]
            need = sum(h_ for c_, h_ in rows) + len(rows) * P45_GAP * kb + P45_KEY_MIN * kb
            pick = dict(den=den, ss=ss, wd=wd, wc=wc, rows=rows, need=need, names=[c_["name"] for c_ in cuts])
            if need <= P45_H * kb:
                break
        if pick is None:
            LOG.append(u"WARNING: sections {}: no cut fits the page at 1:{:,}; page left out.".format(
                u", ".join(names), P45_DENS[-1]))
            continue
        if pick["need"] > P45_H * kb:
            LOG.append(u"WARNING: sections {}: {:.0f} mm tall at 1:{:,} (the panel holds {:.0f} mm).".format(
                u", ".join(pick["names"]), pick["need"] / kb, pick["den"], P45_H))
        LOG.append(u"Sections {} at 1:{:,} (WO-T3a-3: the largest round scale that fills the page).".format(
            u", ".join(pick["names"]), pick["den"]))
        out.append(pick)
    res = ([p["den"] for p in out], [p["ss"] for p in out], [[[(c_, sw)] for c_, h_ in p["rows"]] for p in out], out)
    S._p45_plan = (sw, res)
    return res


def draw_sections_page(S, B, x, y, sw, U, plan, k):
    """v51 (WO-T3a-3; package A p04-05): page k of the cuts as ONE drawing that fills the booklet panel (sw board
    units = BK_AW mm, P45_H tall): the key map on top (draw_sections_key: as tall as the cuts leave room for), then
    each cut (p45_strip) with its column beside it (p45_head) and its scale bar at the column's foot; room left
    over goes between the rows (no dead band). Its own crop sections_<k+1> at its booklet size (bk_w). plan is the
    core's (only its page count is used): the layout is p45_plan's. Returns the y below."""
    L = "LU_BOARD::Sections"
    pl = p45_plan(S, sw, U)
    if k >= len(pl[3]):
        LOG.append(u"Sections page {}: no cuts for it (p45_plan).".format(k + 1))
        return y
    pg = pl[3][k]
    kb = sw / BK_AW
    den, ss, wd, wc, rows = pg["den"], pg["ss"], pg["wd"], pg["wc"], pg["rows"]
    names = pg["names"]
    B.text(u"SECTIONS ACROSS THE STREAM · {} · 1:{:,} ON THE A3 PAGE".format(u", ".join(names), den), x, y, 0.9 * U,
           INK, L, font=FONT_TITLE, bold=True)          # on the sheet only (above the crop)
    top = y - 1.3 * U
    H = P45_H * kb
    gap = P45_GAP * kb
    rows_h = sum(h_ for c_, h_ in rows) + len(rows) * gap
    F = S.F
    hk_max = (sw - (P45_KEY_COL + P45_KEY_TXT + P45_GAP) * kb) * F.h / F.w
    hk = max(P45_KEY_MIN * kb, min(H - rows_h, hk_max))
    extra = max(0.0, H - rows_h - hk) / (len(rows) + 1.0)
    cats = []
    for c_, h_ in rows:
        for a, b, cat in p45_segments(c_, 1.2 * den / 1000.0):
            if cat not in cats:
                cats.append(cat)
    yy = draw_sections_key(S, B, x, top, sw, hk, names, kb, cats) - gap - extra
    for c_, h_ in rows:
        c_["_p45"] = dict(k=kb, den=den)
        p45_strip(S, B, c_, x, yy, wd, ss, kb, U)
        p45_head(S, B, c_, x + wd + gap, yy, wc, kb, U)
        p45_bar(B, x + wd + gap, yy - h_ + 0.6 * kb, wc, ss, c_, den, kb, U)
        yy -= h_ + gap + extra
    low = min(top - H, yy + gap + extra)
    crop_panel("sections_%d" % (k + 1), x, low, x + sw, top,
               u"Sections across the stream · {} · key map and cuts · 1:{:,}".format(u", ".join(names), den),
               crop_scale(ss))
    CROP_PANELS[-1]["bk_w"] = BK_AW                      # drawn at its booklet size: the booklet keeps it
    return low


def site28_title(s):
    """an upper-case name in title case with its Turkish letters (K4 · ULUCAMİ ÖNÜ -> K4 · Ulucami Önü); words
    with digits and words not in capitals stay as written"""
    out = []
    for w_ in (s or u"").split(u" "):
        if not w_ or any(c_.isdigit() for c_ in w_) or not w_.isupper():
            out.append(w_)
            continue
        lo = w_.replace(u"I", u"ı").replace(u"İ", u"i").lower()
        out.append({u"i": u"İ", u"ı": u"I"}.get(lo[0], lo[0].upper()) + lo[1:])
    return u" ".join(out)


def site28_main_k(sd_):
    """the index of a cut's main stream crossing (its lowest bed), or None"""
    if not sd_["water"]:
        return None
    return min(range(len(sd_["water"])), key=lambda k_: sd_["water"][k_][2])


def site28_bank_of(sd_, k_):
    """(the crossing's bank dict or {}, its bank level m a.s.l. or None) for water run k_"""
    bks = sd_.get("banks") or []
    lv = [l_ for l_ in sd_["levels"] if l_[3] == "bank"]
    return (bks[k_] if k_ < len(bks) else {}) or {}, (lv[k_][2] if k_ < len(lv) else None)


def site28_road_call(t):
    """(text, priority) of a street a cut crosses, from road_label's text: its name and the length the cut runs on
    it in cm (G13), priority 2; an OSM line with no surveyed surface: its name alone, an unnamed street: "street",
    priority 3"""
    nm_, _, rest = t.partition(u" · ")
    nm_ = site28_title(nm_)
    if u"OSM line" in rest:
        return nm_, 3
    try:
        m_ = float(rest.split(u" m")[0])
    except ValueError:
        return nm_, 3
    if nm_.lower() == u"street":
        return u"street · " + u_dim(m_), 3
    return nm_ + u" · " + u_dim(m_), 2


def site28_callouts(B, L, P, calls, ytop, U, lh, xlo, xhi, tiers=SITE28_SEC_TIERS):
    """v50 (MIRAQUA 28 Oct, P04.2, G4): a cut's callouts [(s, z, text, priority)] in rows under it from ytop down,
    by priority (0 the water: always; 1 edges and history; 2 named streets; 3 other streets and places): each on the
    first row where it clears the words placed before it by two letters, kept between xlo and xhi and over its
    leader; at most `tiers` rows (priority 0 two more); a word with no free row is left out. A leader from its point
    to its word, broken where it passes a word of a row above. Returns (lowest baseline, [texts left out])."""
    step = lh + 0.4 * U
    base_y = ytop - lh
    gap = max(0.6 * U, 2.2 * lh)
    placed, out_ = [], []
    for c_ in sorted(calls, key=lambda q: (q[3], q[0])):
        s, zf, txt, pr = c_
        fx = P(s, zf)[0]
        half = 0.5 * site28_tw(txt, lh)
        cx = fx
        if xlo is not None:
            cx = max(cx, min(fx + half - 0.3 * U, xlo + half))
        if xhi is not None:
            cx = min(cx, max(fx - half + 0.3 * U, xhi - half))
        cap = tiers + (2 if pr == 0 else 0)
        tier = 0
        while tier < cap and any(t2 == tier and cx - half < r2 + gap and l2 - gap < cx + half
                                 for l2, r2, t2, c2 in placed):
            tier += 1
        if tier >= cap:
            out_.append(txt)
            continue
        placed.append((cx - half, cx + half, tier, c_))
    low = base_y
    for l1, r1, tier, (s, zf, txt, pr) in placed:
        fx, fy = P(s, zf)
        ly = base_y - tier * step
        cuts = sorted((base_y - t2 * step - 0.12 * U, base_y - t2 * step + lh + 0.12 * U)
                      for l2, r2, t2, c2 in placed if t2 < tier and l2 - 0.15 * U < fx < r2 + 0.15 * U)
        ytop_ = fy
        for c0, c1 in reversed(cuts):
            if c1 < ytop_:
                B.line([(fx, ytop_), (fx, c1)], INK2, L, 35, 0.035)
            ytop_ = min(ytop_, c0)
        if ly + lh + 0.12 * U < ytop_:
            B.line([(fx, ytop_), (fx, ly + lh + 0.12 * U)], INK2, L, 35, 0.035)
        B.fill([circle_pts(fx, fy, 0.09 * U, 8)], INK2, L, 35)
        site28_text(B, txt, 0.5 * (l1 + r1), ly, lh, INK, L, align="C")
        low = min(low, ly)
    return low, out_


def site28_link(S, px, py, line):
    """what a cut's crossing (px, py) links to in the masterplan (masterplan_results.json "movement", once per run):
    its nearest hub within SITE28_HUB_M, else its nearest crossing within SITE28_XING_M, else a street it changes
    that the cut crosses; without the masterplan's movement the nearest bridge K1-K6 within SITE28_K_M; u"" when none"""
    if not hasattr(S, "_s28_mp"):
        S._s28_mp = mp_movement()
    M = S._s28_mp
    if M:
        best = None
        for h in M.get("hubs") or []:
            q = _xy1(h.get("xy"))
            d = math.hypot(q[0] - px, q[1] - py) if q else 1e12
            if d <= SITE28_HUB_M and (best is None or d < best[0]):
                best = (d, h)
        if best:
            h = best[1]
            return u"**{}**, {} hub{}".format(site28_title(h.get("name") or u""), u"transit" if h.get("role") ==
                                              "transit" else u"walking", u" · sub-hub in the bed" if h.get("sub_hub")
                                              else u"")
        for c_ in M.get("crossings") or []:
            q = _xy1(c_.get("xy"))
            d = math.hypot(q[0] - px, q[1] - py) if q else 1e12
            if d <= SITE28_XING_M and (best is None or d < best[0]):
                best = (d, c_)
        if best:
            return u"**{}**, {}".format(site28_title(best[1].get("name") or u""), best[1].get("kind") or u"crossing")
        x0, y0, x1, y1 = line[:4]
        for r_ in M.get("roads") or []:
            if r_.get("change") in (None, "", "kept"):
                continue
            P_ = _xy_list(r_.get("xy"))
            if any(seg_x((x0, y0), (x1 - x0, y1 - y0), a_, (b_[0] - a_[0], b_[1] - a_[1])) for a_, b_ in zip(P_, P_[1:])):
                return u"**{}**, {}".format(r_.get("name") or u"street", r_.get("change"))
        return u""
    best = None
    for kk, nm_, bx, by in BRIDGES_K:
        d = math.hypot(bx - px, by - py)
        if d <= SITE28_K_M and (best is None or d < best[0]):
            best = (d, kk, nm_)
    return u"the nearest bridge is **{} {}**".format(best[1], best[2]) if best else u""


def site28_sec_reading(S, sd_):
    """v50 (MIRAQUA 28 Oct, P04.2): (key sentence, what steers the project) of a cut, from its own data only, with
    **bold** keywords: whether it crosses or runs along the stream, the bed's depth below the lower bank crest or
    between the DSİ walls, the edges on its banks; then the strongest constraint or chance at the water and its link
    in the masterplan (site28_link). Memoised on the cut (sd_["_read"]). v51 (WO-T3a-3): the bed, banks and walls
    from the level module (p45_banks, p45_dep); no source or status words on the page (D13)."""
    if "_read" in sd_:
        return sd_["_read"]
    x0, y0, x1, y1 = sd_["line"][:4]
    Lc = math.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / Lc, (y1 - y0) / Lc
    k_ = site28_main_k(sd_)
    tot = sum(sd_["comp"].values()) or 1.0
    top = sorted(sd_["comp"].items(), key=lambda kv: -kv[1])[:2]
    if k_ is None:
        key = u"The cut **does not cross the stream**" + (u": it runs through " + u" and ".join(
            u"{} ({:.0f}%)".format(short(CAT[c_][0]).lower(), 100.0 * v_ / tot) for c_, v_ in top) if top else u"") + u"."
        cons = u"**{}** over {:.0f}% of the cut".format(short(CAT[top[0][0]][0]).lower(), 100.0 * top[0][1] / tot) \
            if top else u""
        px, py = x0 + ux * 0.5 * Lc, y0 + uy * 0.5 * Lc
    else:
        a, b, bed, lvl = sd_["water"][k_]
        cr, zb = site28_bank_of(sd_, k_)
        # v51 (WO-T3a-3, 02 §6, D4 b, D13): the bed and banks from the level module; no status, no internal source
        crs_ = p45_banks(sd_)
        main = next((c2 for c2 in crs_ if c2["k"] == k_), crs_[0] if crs_ else None)
        wall = bool(main) and any(sd["typ"] == "dsi_wall" for sd in main["sides"])
        if main is not None:
            a, b = main["a"], main["b"]
        if len(crs_) > 1:
            dep = u"it crosses the stream **{} times**, the bed at {}".format(
                len(crs_), u", ".join(u_level(c2["bed"]) for c2 in crs_))
        elif main is None:
            dep = u"it crosses the stream"
        else:
            dep = p45_dep(main)
        if cr.get("ang", 90.0) < SITE28_CROSS:
            key = u"The cut runs **along the stream**, not across it; " + dep
        else:
            key = dep[:1].upper() + dep[1:]
        sides = [(t_, wl_) for s_, t_, wl_, gz_ in sd_["labels"] if abs(s_ - a) < 0.3 or abs(s_ - b) < 0.3]
        ws = [SITE28_EDGE_WORD.get(t_, t_) + SITE28_WL_WORD.get(wl_, u"") for t_, wl_ in sides]
        if len(ws) >= 2 and ws[0] == ws[1]:
            key += u"; {} on both banks".format(ws[0])
        elif len(ws) >= 2:
            key += u"; {} on one bank, {} on the other".format(ws[0], ws[1])
        elif ws:
            key += u"; {} at the water".format(ws[0])
        key += u"."
        tys = [t_ for t_, wl_ in sides]
        wls = [wl_ for t_, wl_ in sides]
        if wall and "pedestrian" not in tys:
            hw_ = max([sd["h"] for sd in main["sides"] if sd["typ"] == "dsi_wall" and sd["h"] is not None] or
                      [SCT_DSI_WALL_H_M])
            cons = u"**DSİ walls {} high**, no walkable edge at the water".format(u_height(hw_))
        elif 2 in wls:
            cons = u"an **embanked** bank, cut off from the street"
        elif 1 in wls:
            cons = u"a **walled** bank, cut off from the street"
        else:
            cons = next((t2 for t1, t2 in SITE28_STEER if t1 in tys), u"")
        sm = 0.5 * (a + b)
        px, py = x0 + ux * sm, y0 + uy * sm
    link = site28_link(S, px, py, sd_["line"])
    steer = u""
    if cons or link:
        steer = u"Steers the project: " + cons + ((u" -> " if cons else u"") + link if link else u"") + u"."
    sd_["_read"] = (key, steer)
    return sd_["_read"]


def draw_sections_key(S, B, x, y, sw, hk, names, kb, cats=None):
    """v51 (WO-T3a-3; package A p04-05, 02 §1, D11): the page's key map in its band hk tall at the top of the page
    (kb board units per booklet mm), no scale bar (a key map): a left column with KEY and the north arrow; the site
    frame in the basemap's "topographic" mode (stream, faint buildings, very faint contours coloured by height:
    basemap_items, memoised), the study area (draw_r28_study), ONLY this page's cut lines from the level module
    (basemap_cut_ids + basemap_cut_items), kept inside the frame, a triangle at each end showing the way the section
    looks, the end names beyond; right of the map the page's reading (sections_context) and the colours of the strip
    under the cuts (cats). Part of the page's one crop. Returns the y below the band."""
    L = "LU_BOARD::Sections"
    F = S.F
    h75, h7, hcx = bk_hk(7.5, kb), bk_hk(7.0, kb), bk_hk(P45_TXT["ctx"], kb)
    x0 = x + P45_KEY_COL * kb
    mw_max = sw - (P45_KEY_COL + P45_KEY_TXT + P45_GAP) * kb
    ssk = min(mw_max / F.w, hk / F.h)
    mw, mh = F.w * ssk, F.h * ssk
    yt = y
    V = View(F, ssk, x0, yt)
    r = (x0, yt - mh, x0 + mw, yt)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 30)

    def fill_fn(rings, hx, al, nz):
        CB.fill(rings, mix(WHITE, _p45_c(hx), 1.0 if al is None else al), L, 31)

    def line_fn(pts, hx, wmm, dash, al, order=32):
        col = mix(WHITE, _p45_c(hx), 1.0 if al is None else al)
        for d_ in (r28_pattern(pts, [m_ * kb for m_ in dash]) if dash else [pts]):
            CB.line(d_, col, L, order, bk_lw(wmm or 0.1, kb))

    def text_fn(s, p, size_mm, hx, bold, align, order=41):
        CB.text(s, p[0], p[1], size_mm * 0.718 * kb, _p45_c(hx), L, order=order, font=FONT_TITLE, bold=bold,
                align=align or "L")
    items = None
    try:
        items = basemap_items("topographic", box=F.bb)
    except Exception as e:
        LOG.append(u"Sections key map: no basemap ({}).".format(e))
    if items:
        basemap_draw(items, V.p, fill_fn, line_fn, text_fn)
    else:                                                 # before the first basemap export: water and buildings
        for wt in S.water:
            CB.fill(V.Ps([wt["P"]] + wt.get("H", [])), BLUE_L, L, 31)
        mini_buildings(S, CB, V, L, lambda u: FAINT, order=32)
    draw_r28_study(S, CB, V, kb, L, order=38)             # G8
    # ONLY this page's cut lines (D11), from the level module; the site board's own lines where it has none
    try:
        cuts = basemap_cut_ids(names)
    except Exception as e:
        cuts = [((x0_, y0_), (x1_, y1_), (nm, nm + u"'")) for x0_, y0_, x1_, y1_, nm in S.sec_lines if nm in names]
        LOG.append(u"Sections key map: cut lines from the site board's sec_lines ({}).".format(e))
    den_k = 1000.0 * kb / ssk                             # the key map's scale (no bar: the triangles' size)
    ci = basemap_cut_items(cuts, den_k, frame=list(F.P), tri_mm=3.0, text_mm=3.4, col="4A3F35")
    basemap_draw(ci, V.p, lambda rings, hx, al, nz: CB.fill(rings, _p45_c(hx), L, 39),
                 lambda pts, hx, wmm, dash, al: line_fn(pts, hx, wmm, dash, al, 39),
                 lambda s, p, size_mm, hx, bold, align: text_fn(s, p, size_mm, hx, bold, align, 42))
    B.line(rect(*r) + [(r[0], r[1])], INK2, L, 40, bk_lw(0.15, kb))
    kx = x                                                # the left column: KEY, the north arrow under it
    B.text(u"KEY", kx, yt - h75, h75, INK, L, font=FONT_TITLE, bold=True)
    draw_north_at(B, F, kx + 4.0 * kb, yt - h75 - 8.0 * kb, 4.0, kb, L)
    # right of the map: the page's reading, then the strip's colours and the key's samples (7 pt)
    tx = r[2] + P45_GAP * kb
    tw_ = x + sw - tx
    yy = site28_para(B, sections_context(S, names), tx, yt - hcx, tw_, hcx, INK2, L, lead=1.45, bcol=INK)
    yy -= 0.6 * h7
    lx = tx
    for cat in cats or []:
        w_ = P45_STRIP_WORD.get(cat, cat)
        need = 4.0 * kb + site28_tw(w_, h7) + 3.0 * kb
        if lx > tx and lx + need > x + sw:
            lx, yy = tx, yy - 1.7 * h7
        col = CAT[cat][1] if cat != "void" else mix(KHAKI, PAPER, 0.55)
        B.fill([rect(lx, yy - 0.15 * h7, lx + 3.0 * kb, yy + 1.0 * h7)], col, L, 40)
        lx = site28_text(B, w_, lx + 4.0 * kb, yy, h7, INK, L)[1] + 3.0 * kb
    yy -= 1.9 * h7
    st = R28_STUDY_LINE
    for d_ in r28_pattern([(tx, yy + 0.4 * h7), (tx + 6.0 * kb, yy + 0.4 * h7)], [m_ * kb for m_ in st["dash_mm"]]):
        B.line(d_, C(st["colour"]), L, 40, bk_lw(st["width_mm"], kb))
    site28_text(B, R28_STUDY_NAME, tx + 7.5 * kb, yy, h7, INK, L)
    yy -= 1.9 * h7
    B.line([(tx, yy + 0.4 * h7), (tx + 6.0 * kb, yy + 0.4 * h7)], INK, L, 40, bk_lw(0.35, kb))
    B.fill([[(tx + 5.3 * kb, yy + 0.4 * h7), (tx + 6.7 * kb, yy + 0.4 * h7), (tx + 6.0 * kb, yy + 1.6 * h7)]], INK, L,
           40)
    site28_text(B, u"cut line · the triangle: the way the cut looks", tx + 8.0 * kb, yy, h7, INK, L)
    if yy - 0.5 * h7 < yt - hk:
        LOG.append(u"Sections key band {}: its words run {:.1f} mm below the map.".format(
            u", ".join(names), (yt - hk - (yy - 0.5 * h7)) / kb))
    return yt - max(hk, mh)
