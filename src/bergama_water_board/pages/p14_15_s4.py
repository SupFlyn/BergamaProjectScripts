# p.14-15 S4 through the seasons and its occupancy (split from code.py, parts/r28_occupancy.py on 29 Oct 2026; moved unchanged)


def from_engine(items):
    """Items of the detail-section engine's Page (with layer and join fields) in this board's form."""
    out = []
    for it in items:
        k = it[0]
        if k == "poly":
            _, rings, fill, stroke, lw, dash, layer, join, stripes, alpha = it
            out.append(("poly", rings, fill, stroke, lw, dash, stripes, alpha))
        elif k == "line":
            _, pts, stroke, lw, dash, layer, cap = it
            out.append(("line", pts, stroke, lw, dash, cap))
        elif k == "circle":
            _, cx, cy, r, fill, stroke, lw, layer = it
            out.append(("circle", cx, cy, r, fill, stroke, lw))
        elif k == "text":
            _, s, x, y, size, color, bold, align, layer, mat, halo = it
            out.append(("text", s, x, y, size, color, bold, align, mat, halo))
    return out


def engine_section(E, d, prof, sea_key, scale, skip_z=(), drop=(), poche=None):
    """One S4 bank drawn by the detail engine at 1:scale in the look of one season. Level lines at the heights in
    skip_z are left out; items on the layers in drop are left out; poche = depth of the cut soil under the strip, m
    (v1.12; None = the engine's 1.9 m). Returns (board items, the engine's Sec)."""
    keep = (E["SCALE"], E["K"], dict(E["SEA"]), E["level_line"])
    lay = {"poly": 6, "line": 5, "circle": 7, "text": 8}
    orig = E["level_line"]

    def ll(pg, S, z, label, dash, colour=E["FLOOD"]):
        if any(abs(z - q) < 1e-6 for q in skip_z):
            return
        orig(pg, S, z, label, dash, colour)
    try:
        E["SCALE"], E["K"] = scale, 1000.0 / scale
        E["level_line"] = ll
        E["SEA"].clear()
        E["SEA"].update(E["SEASON_LOOK"][sea_key])
        sea = [s for s in E["SEASONS"] if s["key"] == sea_key][0]
        pg = E["Page"]("s4", sea_key)
        S = E["Sec"](d, prof)
        if poche is not None:
            S.zb = E["THALWEG"][1] - E["STRIP"][2] - poche
        E["draw_section"](pg, S, 0.0, 0.0, [], sea)
    finally:
        E["SCALE"], E["K"] = keep[0], keep[1]
        E["SEA"].clear()
        E["SEA"].update(keep[2])
        E["level_line"] = keep[3]
    k = 1000.0 / scale                      # S keeps this drawing's scale after the engine's K is set back
    S.X = lambda s_: S.X0 + (s_ - d["s_from"]) * S.dir * k
    S.Y = lambda z_: S.Y0 + (z_ - S.zb) * k
    S.P = lambda s_, z_: (S.X(s_), S.Y(z_))
    return from_engine([it for it in pg.items if it[lay[it[0]]] not in drop]), S


def skyline(items, x0, x1, step=1.0):
    """Highest drawn point (page y) in every step-wide column from x0 to x1 (lines sampled along their length)."""
    n = int((x1 - x0) / step) + 2
    top = [-1e9] * n

    def put(x, y):
        i = int((x - x0) / step)
        if 0 <= i < n and y > top[i]:
            top[i] = y

    def seg(p, q):
        m = max(1, int(abs(q[0] - p[0]) / step) + 1)
        for j in range(m + 1):
            t = j / float(m)
            put(p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
    for it in items:
        if it[0] == "poly":
            for r in it[1]:
                for i in range(len(r)):
                    seg(r[i], r[(i + 1) % len(r)])
        elif it[0] == "line":
            for i in range(len(it[1]) - 1):
                seg(it[1][i], it[1][i + 1])
        elif it[0] == "circle":
            put(it[1], it[2] + it[3])
    return lambda a, b: max(top[max(0, int((a - x0) / step)):max(1, int((b - x0) / step) + 1)] or [-1e9])


def sky_labels(pg, labs, items, x_lo, x_hi, y_cap, fs, boxes=None):
    """Short labels set in the open sky over a section, each as low as it fits above everything drawn under it and
    clear of the other labels, with a thin leader to its anchor. labs = [(ax, ay, [lines], colour, bold)]."""
    sky = skyline(items, x_lo - 60.0, x_hi + 60.0)
    boxes = boxes if boxes is not None else []
    lead = fs * 1.25
    for ax, ay, lines, colour, bold in sorted(labs, key=lambda t: t[0]):
        w = max(text_w(t, fs, bold) for t in lines) * BK_GROW + 0.8
        h = lead * len(lines) * BK_GROW
        best = None
        for x0 in (ax - 1.0, ax - w + 1.0, ax - w / 2.0):
            x0 = max(x_lo, min(x0, x_hi - w))
            y = max(sky(x0, x0 + w) + 1.2, ay + 1.5)
            while y + h < y_cap + 30.0:
                if not any(x0 < b[2] and b[0] < x0 + w and y < b[3] and b[1] < y + h for b in boxes):
                    break
                y += 0.5
            if best is None or y < best[1]:
                best = (x0, y)
        x0, y = best
        boxes.append((x0, y, x0 + w, y + h))
        for i, t in enumerate(lines):
            pg.text(t, x0 + 0.4, y + h - BK_GROW * lead * (i + 0.8), fs, colour, bold=bold)
        lx = min(max(ax, x0 + 0.6), x0 + w - 0.6)
        pg.line([(ax, ay), (lx, y - 0.3)], COL["ink2"], 0.1)
        pg.circle(ax, ay, 0.35, fill=COL["ink"])
    return boxes


def r28_tw(s, size, bold=False):
    """the width of one line of text with **bold** keywords, mm"""
    return sum(text_w(t, size, b) for t, b in r28_runs(r28_words(s, bold)))


def r28_text(pg, s, x, y, size, colour, bold=False, align="L", kcol=None, halo=None):
    """one line of text with **bold** keywords (kcol: their colour); returns its width"""
    runs = r28_runs(r28_words(s, bold))
    w = sum(text_w(t, size, b) for t, b in runs)
    r28_draw_runs(pg, runs, x - {"L": 0.0, "C": w / 2.0, "R": w}[align], y, size, colour, kcol, halo)
    return w


def r28_bold(s, words):
    """s with the first place of each of words marked **bold**"""
    for wd in words:
        i = s.find(wd)
        if i >= 0:
            s = s[:i] + u"**" + wd + u"**" + s[i + len(wd):]
    return s


def r28_mix(a, b, t):
    """hex colour a taken t of the way to b"""
    return u"".join(u"%02X" % int(round(int(a[i:i + 2], 16) * (1.0 - t) + int(b[i:i + 2], 16) * t)) for i in (0, 2, 4))


def r28_bar_free(items, cands, den, fs=None, below=True):
    """the first spot (x, y) of cands where the scale bar lies clear of everything in items, else None"""
    boxes = [items_bbox([it]) for it in items]
    for x, y in cands:
        b = r28_bar_box(x, y, den, fs, below)
        if not any(lp_hit(b, o, 0.6) for o in boxes):
            return x, y
    return None


def r28_stall(pg, x, y, k, colour, lw=0.18):
    """a market stall in thin lines, its base centred at (x, y), k mm per m. Returns its box."""
    a, b, h = x - 1.2 * k, x + 1.2 * k, 2.0 * k
    for xx in (a, b):
        pg.line([(xx, y), (xx, y + h)], colour, lw)
    pg.line([(a - 0.25 * k, y + h), (x, y + h + 0.35 * k), (b + 0.25 * k, y + h)], colour, lw)
    pg.line([(a, y + 0.8 * k), (b, y + 0.8 * k)], colour, lw)
    return (a - 0.25 * k, y, b + 0.25 * k, y + h + 0.35 * k)


def season_climate(sea):
    """the season's measured climate and its water balance as the detail engine's SEASONS texts give them (strings,
    unchanged): (rain mm, share %, rain days, mean C, rain minus evaporation mm, its words), or None if a text reads
    otherwise"""
    import re as _re
    m = _re.search(r"Rain ([\d.]+) mm \(([\d.]+) %[^)]*\), ([\d.]+) rain days, mean ([\d.]+) C", sea["climate"][0])
    b = _re.search(r"evaporation ([+-]?[\d.]+) mm[:;]?\s*(.*?)\s*\(calculated",
                   sea["climate"][1]) if len(sea["climate"]) > 1 else None
    if not m or not b:
        return None
    return m.groups() + b.groups()


def season_info(pg, x, y, key, w):
    """THE SEASON beside a p.14 row, w wide from the top y: the climate (measured) and the rain the open water loses
    (calculated), what the plants do (design) and the season's story, keywords bold (G5). Returns the bottom y."""
    fs = FS_MIN
    sea = [s for s in detail_engine()["SEASONS"] if s["key"] == key][0]
    use = SEASON_USE[key]
    cl = season_climate(sea)
    if cl:
        rain, pct, days, temp, bal, words = cl
        yy = r28_para(pg, x, y, w, u"**rain {} mm** · {} % of the year · {} rain days · mean **{} °C** {}".format(
            rain, pct, days, temp, cite(YEAR_SRC[0][1])), fs, COL["ink"])
        yy = r28_para(pg, x, yy - 0.4, w, u"rain minus open-water evaporation **{} mm**{} {}".format(
            bal, (u": " + words) if words else u"", cite(YEAR_SRC[1][1])), fs, COL["ink"])
    else:
        yy = r28_para(pg, x, y, w, u" ".join(sea["climate"]), fs, COL["ink"])
    yy = r28_para(pg, x, yy - 1.2, w, r28_bold(sea["plants"], R28_PLANT_KEY.get(key, ())), fs, C["wet"])
    if use.get("extra"):
        kind, words = use["extra"][0], use["extra"][1]
        yy -= 0.8
        if kind == "stall":
            r28_stall(pg, x + 2.3, yy - 4.4, 1.7, COL["ink"])
        else:
            icon(pg, kind, x, yy, 4.6)
        yy = min(yy - 5.2, r28_para(pg, x + 6.0, yy + fs * 0.2, w - 6.0, words, fs, MP["discharge"][2]) - 0.4)
    return yy


def occ_frac(S, a, b, z):
    """the share of this cut's ground from s a to s b that lies under the level z"""
    n = max(4, int(abs(b - a) / 0.25))
    return sum(1 for i in range(n + 1) if S.surf(a + (b - a) * i / float(n)) < z) / float(n + 1)


def occ_ease(vals, t):
    """a value a month (Jan-Dec, at the month middles) at t months from 1 Jan, cosine-eased, round the year"""
    u = t - 0.5
    i = int(math.floor(u))
    w = (1.0 - math.cos(math.pi * (u - i))) / 2.0
    return vals[i % 12] * (1.0 - w) + vals[(i + 1) % 12] * w


def occ_step(vals, t, r=0.12):
    """a value a month at t, held through each month and eased over r months at its ends"""
    m = int(math.floor(t))
    f = t - m
    if f < r:
        w = 0.5 + 0.5 * f / r
        return vals[(m - 1) % 12] * (1.0 - w) + vals[m % 12] * w
    if f > 1.0 - r:
        w = 0.5 + 0.5 * (1.0 - f) / r
        return vals[m % 12] * w + vals[(m + 1) % 12] * (1.0 - w)
    return vals[m % 12]


def occ_kermes(t, r=0.15):
    """the Kermes visitors at t: 3 in the Kermes week (OCC_KERMES), eased to nothing over r months"""
    a, b = OCC_KERMES
    d = a - t if t < a else (t - b if t > b else 0.0)
    return 3.0 * (1.0 + math.cos(math.pi * d / r)) / 2.0 if d < r else 0.0


def occ_runs(n, ok):
    """the indices 0 .. n-1 for which ok(i), in runs"""
    out, cur = [], []
    for i in range(n):
        if ok(i):
            cur.append(i)
        elif cur:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def occ_spans(ms):
    """the months ms (0 = Jan) as spans [(first, end)] along the year: Dec-Feb gives (0, 2) and (11, 12)"""
    out, m = [], 0
    while m < 12:
        if m in ms:
            n = m
            while n + 1 < 12 and (n + 1) in ms:
                n += 1
            out.append((m, n + 1))
            m = n + 1
        else:
            m += 1
    return out


def draw_occupancy(pg, E, S, y0, h_avail, x_left, x_right):
    """THROUGH THE YEAR under the S4 north-east cut (P15.2; references p15_ref1 "Dock Square 24h": lanes, bands that
    swell with intensity, small figures in them; p15_ref2 "flexible programmes": user groups as see-through flowing
    shapes that overlap, two hatches for free time), on the cut's own width: one lane a band of the cut (OCC_LANES), the
    users in it (OCC_USE, design assumption) with silhouettes and a few words, the season's water toned and the winter
    flood reach (Q500 hatched, Q100 dashed) where this cut's ground lies under them, free time hatched (shareable;
    open to new programmes), the in-bed sub-hub and the Kermes in the head row, feel · hear · touch in a few words,
    the key at the right (x_right = the cut's right edge). Fills h_avail from y0 down. Returns the bottom y."""
    fs = FS_MIN
    XL, XR = min(S.X(OCC_S[0]), S.X(OCC_S[1])), max(S.X(OCC_S[0]), S.X(OCC_S[1]))
    mw = (XR - XL) / 12.0

    def X(t):
        return XL + t * mw
    bed, q100, q500 = E["THALWEG"][1], E["Q100"], E["Q500"]
    lev = [(None, False)] * 12                           # the season's water a month, as the season cuts draw it
    for sea in E["SEASONS"]:
        filled = [w_[0] for w_ in sea["water"] if w_[1]]
        for m in S4_MONTH_IDX[sea["key"]]:
            lev[m] = (max(filled) if filled else None, sea["strip_held"])
    segs = [("winter", 0, 2), ("spring", 2, 5), ("summer", 5, 8), ("autumn", 8, 11)]

    def sense_text(key):
        u_ = SEASON_USE[key]
        return u"**{}** · {} · {}".format(*[u_[k_][1].replace(u"**", u"") for k_ in ("feel", "hear", "touch")])
    hs = max(max(len(r28_lines(sense_text(k_), fs, (b_ - a_) * mw - 1.6)) for k_, a_, b_ in segs) * fs * 1.28 + 1.2,
             fs * 2.6 + 0.8)
    L = max(7.0, min(11.5, (h_avail - 11.0 - hs - 0.5) / len(OCC_LANES)))
    yl = y0 - 11.0                                       # the top of the lanes
    ybot = yl - L * len(OCC_LANES)
    ts = [i * 0.05 for i in range(241)]                  # 0 ... 12 months
    nt = len(ts)
    lanes = []
    for i, (key, name, a, b) in enumerate(OCC_LANES):
        cache = {}

        def fr(z, a=a, b=b, cache=cache):
            if z not in cache:
                cache[z] = occ_frac(S, a, b, z)
            return cache[z]
        top = yl - i * L
        ln = dict(key=key, name=name, a=a, b=b, top=top, bot=top - L, mid=top - L / 2.0)
        ln["back"] = [fr(lev[m][0]) if lev[m][0] is not None else 0.0 for m in range(12)]
        ln["tone"] = [max(ln["back"][m], fr(bed + 0.005) if lev[m][1] else 0.0) for m in range(12)]
        ln["f500"] = [fr(q500) if m in OCC_FLOOD else 0.0 for m in range(12)]
        ln["f100"] = [fr(q100) if m in OCC_FLOOD else 0.0 for m in range(12)]
        use = OCC_USE.get(key, [])
        ln["bands"] = []
        for j, (g, vals, marks) in enumerate(use):
            th = [(occ_kermes(t) if vals is None else occ_ease(vals, t)) / 3.0 * OCC_T * L for t in ts]
            ln["bands"].append((g, ln["mid"] + OCC_OFF[j % len(OCC_OFF)] * L, th, marks))
        ln["total"] = [sum(v[m] for _, v, _ in use if v is not None) for m in range(12)]
        lanes.append(ln)

    def env(ln, i):
        on = [(c - th[i] / 2.0, c + th[i] / 2.0) for _, c, th, _ in ln["bands"] if th[i] > 0.05]
        return (min(e[0] for e in on), max(e[1] for e in on)) if on else None

    def free(ln, m):
        """the free time of a lane in month m: "share", "open" or None (busy, the water's, or the bed closed)"""
        if ln["back"][m] >= 0.5 or ln["f500"][m] >= 0.5:
            return None
        if ln["key"] == "bed" and m not in SUBHUB_OPEN:
            return None
        return "open" if ln["total"][m] <= 1 else ("share" if ln["total"][m] <= 2 else None)
    # free time under everything: wavy lines (shareable) or dots (open to new programmes) round the bands
    pad = 0.4
    for ln in lanes:
        tone = [occ_step(ln["tone"], t) for t in ts]
        for m in range(12):
            cls = free(ln, m)
            if cls is None:
                continue
            idx = [i for i in range(nt) if m - 1e-6 <= ts[i] <= m + 1 + 1e-6]
            es = [env(ln, i) or (ln["mid"], ln["mid"]) for i in idx]
            if cls == "share":
                if all(env(ln, i) is None for i in idx):
                    regs = [rect(X(m), ln["bot"] + pad, X(m + 1), ln["top"] - pad)]
                else:
                    regs = [[(X(m), ln["top"] - pad), (X(m + 1), ln["top"] - pad)] +
                            [(X(ts[i]), min(ln["top"] - pad, e[1] + pad)) for i, e in zip(idx, es)][::-1],
                            [(X(m), ln["bot"] + pad)] +
                            [(X(ts[i]), max(ln["bot"] + pad, e[0] - pad)) for i, e in zip(idx, es)] +
                            [(X(m + 1), ln["bot"] + pad)]]
                for r_ in regs:
                    pg.poly([r_], fill=COL["white"], stripes=(COL["ink2"], 1.1, 0.12, 0.0, True))
                continue
            gx = XL + 0.75 + 1.5 * math.ceil((X(m) + 0.3 - XL - 0.75) / 1.5)
            while gx < X(m + 1) - 0.3:
                i = min(nt - 1, max(0, int(round((gx - XL) / mw / 0.05))))
                e = env(ln, i)
                gy = ln["bot"] + 0.75
                while gy < ln["top"] - 0.5:
                    if gy > ln["bot"] + tone[i] * (L - 0.2) + 0.3 and (e is None or gy > e[1] + pad or gy < e[0] - pad):
                        pg.circle(gx, gy, 0.15, fill=COL["ink2"])
                    gy += 1.5
                gx += 1.5
    # the grid: months (seasons a little darker), lanes
    for m in range(13):
        pg.line([(X(m), y0 - 7.0), (X(m), ybot)], C["structure"] if m % 3 == 2 or m in (0, 12) else COL["faint"],
                0.12 if m % 3 == 2 else 0.1)
    for i in range(len(OCC_LANES) + 1):
        pg.line([(x_left, yl - i * L), (XR, yl - i * L)], C["structure"] if i in (0, len(OCC_LANES)) else COL["faint"],
                0.15)
    # the water: the season's (tone, as the season cuts draw it), the winter flood reach (Q500 hatched, Q100 dashed)
    for ln in lanes:
        for vals, kind in ((ln["tone"], "tone"), (ln["f500"], "q500"), (ln["f100"], "q100")):
            fv = [occ_step(vals, t) for t in ts]
            for run in occ_runs(nt, lambda i: fv[i] > 0.003):
                top_ = [(X(ts[i]), ln["bot"] + fv[i] * (L - 0.2)) for i in run]
                ring = [(X(ts[run[0]]), ln["bot"])] + top_ + [(X(ts[run[-1]]), ln["bot"])]
                if kind == "tone":
                    pg.poly([ring], fill=C["w1"], alpha=0.6)
                    pg.line(top_, C["w2"], 0.2)
                elif kind == "q500":
                    pg.poly([ring], fill=None, stroke=C["w4"], lw=0.1, stripes=(C["w4"], 0.9, 0.12, 45.0))
                else:
                    pg.line(top_, C["w4"], 0.2, dash=[0.8, 0.5])
    # the in-bed sub-hub along the bed lane: solid while open, dashed while closed
    for ln in lanes:
        if ln["key"] == "bed":
            for ms, op in ((SUBHUB_OPEN, True), ([m for m in range(12) if m not in SUBHUB_OPEN], False)):
                for a_, b_ in occ_spans(ms):
                    pg.line([(X(a_), ln["top"] - 0.3), (X(b_), ln["top"] - 0.3)], OCC_HUB_COL, 0.4 if op else 0.2,
                            dash=None if op else [0.8, 0.6])
    # the users: flowing see-through bands, the silhouettes in them, their words (G4: place_labels_all)
    for ln in lanes:
        for g, c, th, marks in ln["bands"]:
            for run in occ_runs(nt, lambda i: th[i] > 0.05):
                up = [(X(ts[i]), c + th[i] / 2.0) for i in run]
                lo = [(X(ts[i]), c - th[i] / 2.0) for i in run]
                pg.poly([up + lo[::-1]], fill=OCC_COL[g], stroke=OCC_COL[g], lw=0.1, alpha=OCC_ALPHA)
    taken, says = [], []
    k = OCC_FIG * L / 1.75
    for ln in lanes:
        for g, c, th, marks in ln["bands"]:
            fc = r28_mix(OCC_COL[g], COL["ink_dark"], 0.3)
            for t, pose, h, words in marks:
                if pose == "stall":
                    bx = r28_stall(pg, X(t), c - 0.5 * OCC_FIG * L, k * 0.8, fc)
                else:
                    bx = r28_fig(pg, pose, X(t), c - 0.5 * OCC_FIG * L, k, fc, 1, h)
                taken.append(bx)
                if words:
                    says.append((ln["key"], bx[2] + 0.3, (bx[1] + bx[3]) / 2.0, words, 0))
    for key, t, words in OCC_NOTES:
        for ln in lanes:
            if ln["key"] == key:
                says.append((key, X(t), ln["bot"] + max(0.6, occ_step(ln["tone"], t) * (L - 0.2) * 0.5), words, 1))
    for ln in lanes:
        mine = [s_ for s_ in says if s_[0] == ln["key"]]
        its = [dict(x=ax, y=ay, rank=rk, wh=lambda f, s=wd: (r28_tw(s, fs * f) + 0.8, fs * f * 0.95 + 0.5))
               for _, ax, ay, wd, rk in mine]
        got = place_labels_all(its, taken, (XL + 0.3, ln["bot"] + 0.2, XR - 0.3, ln["top"] - 0.2), (), (1.0,), 0.4)
        for i, (bx, far, f) in got.items():
            if far:
                pg.line([(its[i]["x"], its[i]["y"]), lp_leader_end(bx, (its[i]["x"], its[i]["y"]))], COL["ink2"], 0.1)
            r28_text(pg, mine[i][3], bx[0] + 0.4, bx[1] + 0.25 + fs * f * 0.21, fs * f, COL["ink_dark"],
                     halo=COL["white"])
    # the head row: the floods and the Kermes (line 1), the in-bed sub-hub (line 2); the months
    y1, y2, yh = y0 - 2.4, y0 - 5.6, y0 - 6.3
    for a_, b_ in occ_spans(OCC_FLOOD):
        pg.line([(X(a_) + 0.3, y0 - 3.9), (X(a_) + 0.3, y0 - 3.2), (X(b_) - 0.3, y0 - 3.2), (X(b_) - 0.3, y0 - 3.9)],
                C["w4"], 0.35)
    wf = r28_text(pg, u"**floods** · Q100 / Q500 reach", X(0) + 0.3, y1, fs, C["w4"])
    k0, k1 = X(OCC_KERMES[0]), X(OCC_KERMES[1])
    pg.poly([rect(k0, y0 - 7.0, k1, y0 - 3.0)], fill=OCC_COL["kermes"], alpha=0.6)
    kt = u"**Kermes** · late Jun-early Jul"
    kx = k0 - 0.8 - r28_tw(kt, fs)
    if kx < X(0) + 0.3 + wf + 2.0:
        kx = k1 + 0.8
    r28_text(pg, kt, kx, y1, fs, OCC_COL["kermes"])
    for a_, b_ in occ_spans(SUBHUB_OPEN):
        pg.line([(X(a_) + 0.3, yh - 0.7), (X(a_) + 0.3, yh), (X(b_) - 0.3, yh), (X(b_) - 0.3, yh - 0.7)], OCC_HUB_COL,
                0.4)
        r28_text(pg, u"**in-bed sub-hub** open {}-{}".format(MONTHS[a_], MONTHS[b_ - 1]), X(b_) - 0.3, y2, fs,
                 COL["ink"], align="R")
    for a_, b_ in occ_spans([m for m in range(12) if m not in SUBHUB_OPEN]):
        pg.line([(X(a_) + 0.3, yh), (X(b_) - 0.3, yh)], OCC_HUB_COL, 0.2, dash=[0.8, 0.6])
        if text_w(u"closed", fs) < (b_ - a_) * mw - 2.0:
            pg.text(u"closed", (X(a_) + X(b_)) / 2.0, y2, fs, COL["ink2"], align="C")
    for m in range(12):
        pg.text(MONTHS[m], X(m + 0.5), y0 - 10.0, fs, COL["ink2"], align="C")
    # the left column: the title, the lanes' names and levels, the cut's small profile with the lane's band in ink
    pg.text(u"THROUGH THE YEAR", x_left, y0 - 3.2, 3.2, COL["ink_dark"], bold=True)
    pg.text(u"the cut's bands · Jan-Dec", x_left, y0 - 10.0, fs, COL["ink2"])
    lvs = []
    for ln in lanes:
        n = max(4, int(abs(ln["b"] - ln["a"]) / 0.25))
        zz = [S.surf(ln["a"] + (ln["b"] - ln["a"]) * i / float(n)) for i in range(n + 1)]
        if ln["key"] == "strip":
            lvs.append(u"{} · {} deep".format(u_level(min(zz)), u_height(E["STRIP"][2])))
        elif max(zz) - min(zz) < 0.02:
            lvs.append(u_level(max(zz)))
        else:
            lvs.append(u"{} to {}".format(u_level(max(zz)), u_level(min(zz))))
    tw = max(max(text_w(ln["name"], fs, True), text_w(lv, fs)) for ln, lv in zip(lanes, lvs))
    pw = 12.0
    px0 = XL - 2.5 - pw
    show = x_left + tw + 1.5 <= px0
    ps = [OCC_S[0] + (OCC_S[1] - OCC_S[0]) * i / 128.0 for i in range(129)]
    pz = [S.surf(s_) for s_ in ps]
    z0, z1 = min(pz), max(pz)
    for ln, lv in zip(lanes, lvs):
        pg.text(ln["name"], x_left, ln["top"] - 3.0, fs, COL["ink_dark"], bold=True)
        pg.text(lv, x_left, ln["top"] - 3.0 - fs * 1.2, fs, COL["ink2"])
        if show and z1 > z0:
            ph = max(1.5, min(3.0, L - 4.5))

            def pp(s_, z_, ln=ln, ph=ph):
                return (px0 + (OCC_S[0] - s_) / (OCC_S[0] - OCC_S[1]) * pw, ln["bot"] + 0.9 + (z_ - z0) / (z1 - z0) * ph)
            pg.line([pp(s_, z_) for s_, z_ in zip(ps, pz)], C["structure"], 0.12)
            pg.line([pp(s_, z_) for s_, z_ in zip(ps, pz) if ln["b"] <= s_ <= ln["a"]], COL["ink_dark"], 0.4)
    # feel · hear · touch: a few words a season (design intention), under the lanes
    ys = ybot - 0.8
    pg.text(u"FEEL · HEAR · TOUCH", x_left, ys - fs, fs, COL["ink_dark"], bold=True)
    pg.text(u"design intention, ours", x_left, ys - fs * 2.25, fs, COL["ink2"])
    for key, a_, b_ in segs:
        r28_para(pg, X(a_) + 0.8, ys + fs * 0.28, (b_ - a_) * mw - 1.6, sense_text(key), fs, COL["ink"])
    r28_para(pg, X(11) + 0.8, ys + fs * 0.28, mw - 1.6, u"**winter**: as Jan-Feb", fs, COL["ink"])   # Dec
    for m in (2, 5, 8, 11):
        pg.line([(X(m), ybot), (X(m), ybot - hs + 0.6)], C["structure"], 0.12)
    # the key at the right of the lanes
    lx = XR + 6.0
    kw_ = max(24.0, x_right - lx)                       # within the cut's own width (the panel is as wide as the cell)
    y = y0

    def head(t, y):
        pg.text(t, lx, y - fs, fs, COL["ink_dark"], bold=True)
        return y - fs * 1.55

    def entry(y, words):
        return min(y - 3.1, r28_para(pg, lx + 7.5, y + fs * 0.25, kw_ - 7.5, words, fs, COL["ink"]) - 0.5)
    y = head(u"WHO", y)
    for g, name, col in OCC_GROUPS:
        pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=col, stroke=col, lw=0.1, alpha=OCC_ALPHA)
        y = entry(y, name)
    y = head(u"WATER", y - 0.8)
    pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=C["w1"], alpha=0.6)
    pg.line([(lx, y - 0.2), (lx + 6.0, y - 0.2)], C["w2"], 0.2)
    y = entry(y, u"season water on this cut, **calculated**")
    pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=None, stroke=C["w4"], lw=0.1,
            stripes=(C["w4"], 0.9, 0.12, 45.0))
    y = entry(y, u"**flood reach** in winter: Q500, Q100 dashed")
    y = head(u"FREE TIME", y - 0.8)
    pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=COL["white"], stroke=COL["faint"], lw=0.1,
            stripes=(COL["ink2"], 1.1, 0.12, 0.0, True))
    y = entry(y, u"**shareable** time")
    pg.poly([rect(lx, y - 2.6, lx + 6.0, y - 0.2)], fill=None, stroke=COL["faint"], lw=0.1)
    for dx in (1.0, 2.5, 4.0, 5.5):
        for dy in (0.9, 2.0):
            pg.circle(lx + dx - 0.25, y - dy, 0.15, fill=COL["ink2"])
    y = entry(y, u"**open** to new programmes")
    pg.line([(lx, y - 1.0), (lx + 2.8, y - 1.0)], OCC_HUB_COL, 0.4)
    pg.line([(lx + 3.4, y - 1.0), (lx + 6.0, y - 1.0)], OCC_HUB_COL, 0.2, dash=[0.8, 0.6])
    y = entry(y - 0.8, u"in-bed **sub-hub** open · closed")
    y = r28_para(pg, lx, y - 0.6, kw_, u"band thickness = how busy: **design assumption**, ours", fs, COL["ink2"])
    return min(ybot - hs, y) - 0.5


def subhub_words(key):
    """The in-bed sub-hub in this season: (pictogram, keywords) from SUBHUB_OPEN."""
    ms = [m for m in S4_MONTH_IDX[key] if m in SUBHUB_OPEN]
    if not ms:
        return "hub_closed", u"in-bed hub closed"
    if len(ms) == 3:
        return "hub_open", u"in-bed hub open"
    return "hub_open", u"in-bed hub open " + u", ".join(MONTHS[m] for m in ms)


def draw_s4_season(key, log=None, scale=None):
    """One season of the S4 cut, south-west bank and bed: the season's water hatched and its levels at the right, and
    what people do there (S4_SEASON words) set in the sky with leaders. v1.14: the season's name, water, hub and
    senses are drawn beside the row by draw_seasons_panel (v4: with one scale bar under the four rows)."""
    scale = scale or S4_SCALE
    E = detail_engine()
    prof = s4_profile(E, log)
    d = E["SECTIONS"][0]
    bed, q100, q500 = E["THALWEG"][1], E["Q100"], E["Q500"]
    skip = () if key == "winter" else (q100, q500)
    items, S = engine_section(E, d, prof, key, scale, skip, ("title", "callouts", "dimensions", "band", "survey",
                                                              "text"), S4_POCHE)
    pg = Page(0, 0)
    pg.items = items
    sea = [s for s in E["SEASONS"] if s["key"] == key][0]
    info = S4_SEASON[key]
    fs = S4_FS
    xl, xr = S.X(d["s_from"]), S.X(d["s_to"])
    bb = items_bbox(items)
    y_cap = bb[3]
    boxes = []
    lv = [(S.Y(bed), u"{:+.2f} bed".format(bed), COL["ink"], False)]
    names = info["water"]
    for i, w in enumerate(sea["water"]):
        lv.append((S.Y(w[0]), u"{:.2f} m {}".format(w[0] - bed, names[i] if i < len(names) else u""),
                   E["FLOOD"], i == 0))
    if sea["strip_held"] and not [w for w in sea["water"] if w[1]]:
        lv.append((S.Y(bed) + 0.01, u"strip {} × {}".format(u_dim(abs(E["STRIP"][1] - E["STRIP"][0])),   # v4 (G13)
                                                            u_height(E["STRIP"][2])), E["FLOOD"], True))
    if key == "winter":
        lv += [(S.Y(q100), u"{:.2f} m Q100".format(q100 - bed), E["FLOOD"], True),
               (S.Y(q500), u"{:.2f} m Q500".format(q500 - bed), E["FLOOD"], True)]
    level_ladder(pg, lv, xr + 0.5, xr + 6.0, fs, boxes, lo=bb[1] + 1.0)
    labs = []
    for s, z, t in info["words"]:
        labs.append((S.X(s), S.Y(z if z is not None else S.surf(s) + 0.05), [t], COL["ink_dark"], True))
    if key == "winter":
        labs.append((S.X(552.5), S.Y(E["DRY"]), [u"raised walk {:.2f} m".format(E["DRY"] - q500) + u" over Q500"],
                     E["FLOOD"], True))
    sky_labels(pg, labs, items, xl, xr + 24.0, y_cap, fs, boxes)
    return pg


def senses(pg, x, y, use, w, fs=FS_MIN):
    """FEEL / HEAR / TOUCH of one season in a column w wide: three pictograms with their keywords from the top y.
    v4 (MIRAQUA 28 Oct): keywords bold (G5), no [n] (F5: design intentions, our own record), a little smaller so the
    1:500 rows keep their height. Returns bottom y."""
    for slot in ("feel", "hear", "touch"):
        icon(pg, use[slot][0], x, y, 5.6)
        yy = r28_para(pg, x + 7.0, y + fs * 0.2, w - 7.0, use[slot][1], fs, COL["ink"])
        y = min(y - 6.6, yy - 1.0)
    return y


def season_tag(pg, x, y, key):
    """The season's column: name, months, water state, what people do, the in-bed hub. v4 (MIRAQUA 28 Oct, P14.2):
    compact for the 1:500 rows; what people do as common/figures.py silhouettes 6 mm tall (P19.2), said to be design
    (F5: no [n] for our concept note); the season's story moved to THE SEASON (season_info). Returns bottom y."""
    fs = FS_MIN
    w = TAG_W - 2.0
    use = SEASON_USE[key]
    sea = [s for s in detail_engine()["SEASONS"] if s["key"] == key][0]
    pg.poly([rect(x, y - 1.0, x + w, y)], fill=BAND_BLUE[SEAS.index(key)])
    pg.text(sea["name"], x, y - 5.6, 4.4, COL["ink_dark"], bold=True)
    yy = para(pg, x, y - 6.2, w, S4_MONTHS[key] + u" · " + S4_SEASON[key]["head"], fs, COL["ink2"], bold=True) - 1.0
    icon(pg, use["water"][0], x, yy, 4.6)
    pg.text(use["water"][1], x + 6.0, yy - 3.2, fs, MP["discharge"][2], bold=True)
    yy -= 6.0
    k = 6.0 / 1.75                                       # an adult 6 mm tall
    xa = x + 0.6
    for kind in use["acts"]:
        if kind == "stall":
            xa = r28_stall(pg, xa + 3.8, yy - 6.0, k * 0.75, COL["ink"])[2] + 1.4
        else:
            pose, h = R28_ACT_POSE[kind]
            bx = r28_fig(pg, pose, xa + 0.6, yy - 6.0, k, COL["ink"], 1, h)
            xa = bx[2] + 1.4
    pg.text(u"design", xa + 0.4, yy - 5.6, fs, COL["ink2"])
    yy -= 7.4
    kind, words = subhub_words(key)
    icon(pg, kind, x, yy, 4.6)
    return para(pg, x + 6.0, yy + fs * 0.2, w - 6.0, words, fs, COL["ink"], bold=True) - 1.0


def month_strip(pg, x, y, gx, gw):
    """v1.14: the year in 12 cells from gx, gw wide: the in-bed sub-hub open (sand) or closed (water), the Kermes,
    and the high-water months (Dec-Apr, the year calendar's 89 % flow) when the Roman tunnels carry the stream; its
    name in the season column at x. Returns bottom y."""
    fs = FS_MIN
    icon(pg, "hub_open", x, y, 5.6)
    para(pg, x + 7.0, y + 3.2 * 0.2, TAG_W - 9.0, u"IN-BED SUB-HUB", 3.2, COL["ink_dark"], bold=True)
    pg.text(u"open {}-{}".format(MONTHS[SUBHUB_OPEN[0]], MONTHS[SUBHUB_OPEN[-1]]), x, y - 9.2, fs, COL["ink2"],
            bold=True)
    cw = gw / 12.0
    yc = y - 0.5
    for m in range(12):
        op = m in SUBHUB_OPEN
        pg.poly([rect(gx + m * cw + 0.3, yc - 5.0, gx + (m + 1) * cw - 0.3, yc)], fill="E4D6B0" if op else C["w2"])
        pg.text(MONTHS[m], gx + (m + 0.5) * cw, yc - 3.6, fs, COL["ink_dark"] if op else COL["white"], bold=True,
                align="C")
    xk = gx + OCC_KERMES[0] * cw                         # Kermes 29 Jun-5 Jul (h01 §2.8)
    xk1 = gx + OCC_KERMES[1] * cw
    # v4 (MIRAQUA 28 Oct): the Kermes in its p.15 colour, its stall in thin lines as on p.15; no [n] (F5: the dates
    # and the tunnels come from our own research notes)
    pg.poly([rect(xk, yc - 6.2, xk1, yc - 5.4)], fill=OCC_COL["kermes"])
    r28_stall(pg, xk + 0.3, yc - 11.0, 1.7, OCC_COL["kermes"])
    pg.text(u"Kermes · late Jun-early Jul", xk + 3.4, yc - 10.3, fs, OCC_COL["kermes"], bold=True)
    yb = yc - 6.2
    for a_, b_ in ((0, 3), (11, 11)):                    # Dec-Apr
        pg.line([(gx + a_ * cw + 0.5, yb), (gx + a_ * cw + 0.5, yb - 1.2), (gx + (b_ + 1) * cw - 0.5, yb - 1.2),
                 (gx + (b_ + 1) * cw - 0.5, yb)], MP["discharge"][2], 0.35)
    icon(pg, "tunnel", gx, yb - 2.0, 4.6)
    r28_text(pg, u"high water: the **Roman tunnels** at work", gx + 5.6, yb - 5.6, fs, MP["discharge"][2])
    return min(yb - 8.0, y - 10.5)


def draw_seasons_panel(W, H, log):
    """v3 (Aras 27 Oct 17:34, Prompt 5 task 1: "Each season's section fills the band between the left label column
    (WINTER / SPRING ...) and the right FEEL · HEAR · TOUCH column, and its baseline sits on that row's divider line.
    All four at the same scale and the same horizontal extent, stacked so the bank lines up"): the month strip, then
    one row a season, each closed by its divider line: the season's column at the left, the S4 cut standing on the
    divider (all four on one x, so the bank lines up), FEEL / HEAR / TOUCH at the right in the width the cuts leave.
    The rows share the height that is left, so the panel fills W x H with no empty band. v4 (MIRAQUA 28 Oct, P14.2
    "empty right side"): one stated scale, 1:500 (S4_DENS; H is at most R28_PART_H under the S4 key map), and the
    width the cuts leave filled with content: THE SEASON (season_info: climate measured, plants designed) between the
    cuts and FEEL · HEAR · TOUCH; the scale bar under the cuts. Returns (Page, scale denominator)."""
    W, H = W - 0.5, H - 0.5                              # a hair inside, so the panel is placed at 1:1
    den = S4_DENS[0]
    cuts = dict((k_, draw_s4_season(k_, log, den)) for k_ in SEAS)
    bbs = [items_bbox(cuts[k_].items) for k_ in SEAS]
    cx0, foot = min(b[0] for b in bbs), min(b[1] for b in bbs)
    wcut, hcut = max(b[2] for b in bbs) - cx0, max(b[3] for b in bbs) - foot
    xc = TAG_W + SEASON_GAP                              # the cuts' band, the same x for all four
    xi = xc + wcut + SEASON_GAP                          # THE SEASON
    sw = max(SENSE_MIN, min(R28_SENSE_W, (W - xi) * 0.4))   # FEEL / HEAR / TOUCH
    iw = W - xi - SEASON_GAP - sw
    xs = xi + iw + SEASON_GAP
    scratch = Page(0, 0)
    hrow = max([hcut] + [-season_tag(scratch, 0.0, 0.0, k_) for k_ in SEAS] +
               [-season_info(scratch, 0.0, 0.0, k_, iw) for k_ in SEAS] +
               [-senses(scratch, 0.0, 0.0, SEASON_USE[k_], sw) for k_ in SEAS]) + 1.5
    pg = Page(0, 0)
    y = month_strip(pg, 0.0, 0.0, xc, wcut) - SEASON_GAP
    for x_, w_, head, sub in ((xi, iw, u"THE SEASON", u"climate **measured** · plants **designed**"),
                              (xs, sw, u"FEEL · HEAR · TOUCH", u"design intention, ours")):
        para(pg, x_, 3.2 * 0.2, w_, head, 3.2, COL["ink_dark"], bold=True)
        r28_para(pg, x_, -5.0, w_, sub, FS_MIN, COL["ink2"])
    top = items_bbox(pg.items)[3]
    bar = r28_bar_box(0.0, 0.0, den)
    gap = SEASON_GAP
    free = H - (top - y) - 4 * hrow - 4 * gap - (bar[3] - bar[1])
    if free < 0.0:                                       # tighter gaps before anything is shrunk
        gap = 1.0
        free = H - (top - y) - 4 * hrow - 4 * gap - (bar[3] - bar[1])
    if free < 0.0 and log is not None:
        log.append(u"WARNING: p.14 S4 seasons {:.1f} mm taller than the {:.0f} mm under the key map".format(-free, H))
    hrow += max(free, 0.0) / 4.0
    for key in SEAS:
        div = y - hrow                                   # the row's divider line: the cut stands on it
        pg.items += xform(cuts[key].items, 1.0, xc - cx0, div - foot)
        season_tag(pg, 0.0, y, key)
        season_info(pg, xi, y, key, iw)
        senses(pg, xs, y, SEASON_USE[key], sw)
        pg.line([(0.0, div), (xs + sw, div)], COL["faint"], 0.25)
        y = div - gap
    r28_scale_bar(pg, xc, y - bar[3], den)               # one bar for the four cuts (one scale)
    if log is not None:
        log.append(u"p.14 S4 seasons: 1:{:,.0f}, rows {:.1f} mm, cuts {:.0f} mm wide, THE SEASON {:.0f} mm, FEEL column "
                   u"{:.0f} mm, panel {:.0f} x {:.0f} mm".format(den, hrow, wcut, iw, sw, W, top - y + bar[3] - bar[1]))
    return pg, den


def draw_s4_ne(log, den=None, h_max=None):
    """The north-east bank of the S4 cut at 1:den (v3: S4_NE_SCALE, 1:250), summer, with the engine's callouts, widths
    (cm, v1.14), materials and levels, the flood levels at its left. v4 (MIRAQUA 28 Oct, P15.2): under it the
    occupancy diagram THROUGH THE YEAR (draw_occupancy, was the four season strips of ne_strips), the whole at most
    h_max tall (R28_PART_H: the booklet's key map); the scale bar beside the cut; soil S4_NE_POCHE under the strip."""
    den = den or S4_NE_SCALE
    E = detail_engine()
    prof = s4_profile(E, log)
    keep = (E["SCALE"], E["K"])
    E["SCALE"], E["K"] = den, 1000.0 / den
    try:
        E["SEA"].clear()
        E["SEA"].update(E["SEASON_LOOK"]["summer"])
        sea = dict(E["SEASONS"][2])
        pg = E["Page"]("detail", "S4")
        S = E["Sec"](E["SECTIONS"][1], prof)
        S.zb = E["THALWEG"][1] - E["STRIP"][2] - S4_NE_POCHE   # v4 (MIRAQUA 28 Oct, P15.2): room for the diagram
        del E["_LV"][:]
        notes = []
        E["draw_section"](pg, S, 0.0, 0.0, notes, sea)
        lv = sorted(E["_LV"], key=lambda e: e[0])
        xl = S.X0 - 4.0
        ys = [S.Y(z) for z, _, _, _ in lv]
        ly = spread(ys, FS_MIN * 1.3)
        for (z, lab, colour, dash), Y, Yl in zip(lv, ys, ly):
            pg.line([(xl + 2.5, Y), (xl - 1.0, Y), (xl - 3.0, Yl + 0.6), (xl - 4.0, Yl + 0.6)], colour, 0.15,
                    layer="ladder")
            t = u"{:+.2f}  {}".format(z, lab.replace(u"%+.2f" % z, u"").replace(u"(calculated on this cut)", u"")
                                       .replace(u"(design)", u"").replace(u"  ", u" ").strip(u" ,;"))
            pg.text(t, xl - 4.4, Yl, FS_MIN, colour if colour != E["WATER_LINE"] else E["FLOOD"], align="R",
                    layer="ladder")
    finally:
        E["SCALE"], E["K"] = keep
    k = 1000.0 / den                        # S keeps this drawing's scale after the engine's K is set back
    S.X = lambda s_: S.X0 + (s_ - S.d["s_from"]) * S.dir * k
    S.Y = lambda z_: S.Y0 + (z_ - S.zb) * k
    S.P = lambda s_, z_: (S.X(s_), S.Y(z_))
    for n_ in notes:
        log.append(u"S4 detail: " + n_)
    out = Page(0, 0)
    # the frame names it (title texts out). v3.2 (Aras 27 Oct, Prompt 8: labels overlapping, words under 7 pt): the
    # survey marks are left out, as on the season rows (engine_section's drop): their 4.5 pt labels "road edge
    # (YOL_SOSE) 626.06 / 629.99" lay on each other and on the lower walk
    lay = {"poly": 6, "line": 5, "circle": 7, "text": 8}
    out.items = from_engine([it for it in pg.items if (it[0] != "text" or it[8] != "title") and
                             it[lay[it[0]]] != "survey"])
    # v4 (MIRAQUA 28 Oct): the scale bar in a free corner under the cut (its left or right foot), else in the gap
    # under it; then the occupancy diagram (P15.2) in the height left under h_max
    bb = items_bbox(out.items)
    bx = r28_bar_box(0.0, 0.0, den)
    spot = r28_bar_free(out.items, [(bb[0] + 1.0, bb[1] - bx[1]), (bb[2] - bx[2] - 0.5, bb[1] - bx[1])], den)
    y0 = bb[1] - 5.0
    if spot:
        r28_scale_bar(out, spot[0], spot[1], den)
    else:
        yb_ = bb[1] - 1.0 - (r28_bar_box(0.0, 0.0, den, below=False)[3])
        r28_scale_bar(out, S.X(OCC_S[0]), yb_, den, below=False)
        y0 = yb_ - FS_MIN * 0.3 - 4.0
    h_max = h_max or R28_PART_H
    draw_occupancy(out, E, S, y0, h_max - (bb[3] - y0) - 0.5, bb[0], bb[2])
    ob = items_bbox(out.items)
    log.append(u"p.15 S4 north-east bank 1:{:,.0f} with the occupancy diagram: {:.0f} x {:.0f} mm{}".format(
        den, ob[2] - ob[0], ob[3] - ob[1], u"" if ob[3] - ob[1] <= h_max + 0.05 else
        u" (WARNING: more than the {:.0f} mm under the key map)".format(h_max)))
    return out
