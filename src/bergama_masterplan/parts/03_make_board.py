def make_board(opt, alt, pages, title=None):
    """The working areas side by side (two rows when wider than BOARD_MAX_W) under the sheet's title. v21: the
    result's .panels = [(key, crop rect in page mm from the top-left, y down)] for the booklet's crops."""
    M, HEAD, G = 14.0, 24.0, 10.0
    rows = [pages]
    if sum(p.W for p in pages) + G * (len(pages) - 1) + 2 * M > BOARD_MAX_W:
        rows = [pages[:2], pages[2:]]
    W = max(sum(p.W for p in r_) + G * (len(r_) - 1) for r_ in rows) + 2 * M
    H = sum(max(p.H for p in r_) for r_ in rows) + G * (len(rows) - 1) + 2 * M + HEAD
    bd = Page(W, H)
    bd.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sheet_head(bd, M, H - M, alt, opt, title)
    y = H - M - HEAD
    at = []
    for r_ in rows:
        x = M
        hr = max(p.H for p in r_)
        for p in r_:
            blit(bd, p, x, y - p.H)
            at.append((p, x, y - p.H))
            x += p.W + G
        y -= hr + G
    sh = add_legend(bd, alt, _ALPHA[0], M)               # v17
    dy = sh.H - bd.H                                     # the legend band added under the board
    sh.panels = []
    for p, x, y0 in at:
        c = getattr(p, "crop", None)
        if c:
            x0, x1, yb, yt = x + c[0], x + c[2], y0 + dy + c[1], y0 + dy + c[3]
            sh.panels.append((getattr(p, "key", None), (x0, sh.H - yt, x1, sh.H - yb), p))
    return sh


# ================================================================ v17: the legend band (only what the sheet draws)
LEG = {}                       # what the sheet being drawn uses: key -> sample data (reset for every sheet)
LEG_ZONE = [("WS", u"WATER STORAGE · RETENTION TERRACES"), ("WT", u"CLEANING · REED BASINS"),
            ("WD", u"CLEAN WATER BACK · SPILLWAY"), ("WA", u"AMPHIBIOUS · BED"),
            ("WAF", u"AMPHIBIOUS · FLOOD TERRACE"), ("WP", u"STREAMSIDE PLANTING"),
            ("GR", u"GREEN · SHADED WALK, DRY TOP"), ("DG", u"DEMETER'S GARDEN"), ("WI", u"AGRICULTURE"),
            ("CH", u"HERITAGE"), ("MC", u"CENTRE"), ("HO", u"HOUSING"), ("CV", u"CIVIC"), ("SR", u"SPORT"),
            ("PA", u"SERVICE")]
LEG_CTX = [("river", u"STREAM"), ("street", u"STREET"), ("park", u"PARK"), ("heritage", u"HERITAGE BUILDING"),
           ("housing", u"HOUSING"), ("building", u"OTHER BUILDING"), ("cleared", u"CLEARED GROUND")]
LEG_SW, LEG_SH, LEG_ROW, LEG_TS, LEG_HS, LEG_GAP = 22.0, 8.0, 11.0, 3.4, 4.0, 14.0   # sizes, mm


_PLEG = [None]                 # v21: the legend keys of the panel being drawn (its booklet crop's legend)


def leg(key, val=True):
    LEG.setdefault(key, val)
    if _PLEG[0] is not None:
        _PLEG[0].setdefault(key, val)


def legend_groups(alt, alpha):
    """[(heading, [(name, draw(pg, x, y, w, h))])] of what LEG holds, in a fixed order."""
    W_ = COL["white"]

    def zone_sw(code, tier):
        def f(pg, x, y, w, h):
            z = {"code": code, "tier": tier, "id": "legend", "q": (0.0, 0.0)}
            lt, md, dk = zone_tones(z)
            TP = rect(x, y, x + w, y + h)
            pg.poly([TP], fill=W_)
            pg.poly([TP], fill=lt, alpha=alpha)
            pg.poly([TP], stroke=COL["ink2"], lw=0.15)
        return f

    def fill_sw(fill, stroke=None, lw=0.15, dash=None, alpha_=None):
        def f(pg, x, y, w, h):
            pg.poly([rect(x, y, x + w, y + h)], fill=fill, alpha=alpha_)
            pg.poly([rect(x, y, x + w, y + h)], stroke=stroke or COL["ink2"], lw=lw, dash=dash)
        return f

    def line_sw(*specs):                                   # (colour, lw, dash, alpha) drawn in order
        def f(pg, x, y, w, h):
            for c_, lw, dash, a_ in specs:
                pg.line([(x, y + h / 2), (x + w, y + h / 2)], c_, lw, dash, cap=0 if dash else 1, alpha=a_)
        return f

    zones = []
    for code, name in LEG_ZONE:
        if ("zone", code) in LEG:
            zones.append((name, zone_sw("WA" if code == "WAF" else code, LEG[("zone", code)])))
    for (k_, code), tier in sorted([(k_, v) for k_, v in LEG.items() if k_[0] == "zone"
                                    and k_[1] not in dict(LEG_ZONE)]):
        zones.append((code, zone_sw(code, tier)))
    if "hub" in LEG:
        tones = LEG["hub"]

        def hub_sw(pg, x, y, w, h):
            n = len(tones)
            for i, t_ in enumerate(tones):
                pg.poly([rect(x + w * i / n, y, x + w * (i + 1) / n, y + h)], fill=t_)
        zones.append((u"COMMONS · WHERE THE PROGRAMMES MEET", hub_sw))
    zl = [code for code, _ in LEG_ZONE if ("zone", code) in LEG]
    if len(zl) >= 2:
        a_, b_ = [zone_tones({"code": "WA" if c_ == "WAF" else c_, "tier": "F" if c_ == "WAF" else "D"})[0]
                  for c_ in zl[:2]]

        def ov_sw(pg, x, y, w, h):
            r1, r2 = rect(x, y, x + w * 0.62, y + h), rect(x + w * 0.38, y, x + w, y + h)
            pg.poly([r1], fill=W_)
            pg.poly([r2], fill=W_)
            pg.poly([r1], fill=a_, alpha=alpha)
            pg.poly([r2], fill=b_, alpha=alpha)
        zones.append((u"OVERLAP · SHARED USE (DARKER)", ov_sw))
    if "river_band" in LEG:
        def rb_sw(pg, x, y, w, h):
            lt, md, dk = RIVER_BAND_TONE
            pg.poly([rect(x + 0.8, y - 0.8, x + w + 0.8, y + h - 0.8)], fill=dk, alpha=0.22)
            pg.poly([rect(x, y, x + w, y + h)], fill=lt, alpha=0.85)
            pg.poly([rect(x, y, x + w, y + h)], stroke=dk, lw=0.35)
        zones.append((RIVER_BAND_NAME, rb_sw))
    for nm_ in (u"MAIN SPINE", u"STREAMSIDE SPINE"):
        if ("spinezone", nm_) in LEG:
            zones.append((nm_, fill_sw(mix(W_, MP["centre"][0], alpha))))
    if "strip" in LEG:
        zones.append((u"NEW WATER STRIP", fill_sw(COL["river"], COL["river_dark"], 0.3, [1.2, 0.7])))
    if "cleared" in LEG:
        zones.append((u"BUILDING CLEARED", fill_sw(W_, COL["ink2"], 0.3, [0.9, 0.6])))

    ctx = []
    for kind, name in LEG_CTX:
        if ("ctx", kind) in LEG:
            ctx.append((name, fill_sw(PIECE_TONE[kind][0])))
    surv = [(("s", "contour"), u"CONTOURS", line_sw((COL["contour10"], 0.3, None, None))),
            (("s", "park"), u"EXISTING PARK", fill_sw(COL["park"])),
            (("s", "pond"), u"POND", fill_sw(COL["river"])),
            (("road", "main"), u"MAIN ROAD", line_sw((ROAD_TONE[2], ROAD_LW[1], None, None))),     # v21
            (("road", "street"), u"STREET EDGE", line_sw((ROAD_TONE[1], ROAD_LW[0], None, None))),
            (("s", "building"), u"BUILDING", fill_sw(COL["bld"], COL["bld_edge"])),
            (("s", "heritage"), u"HERITAGE BUILDING", fill_sw(COL["her"], COL["her_edge"])),
            (("s", "tree"), u"TREE", None),
            (("line", "river_mid"), u"STREAM AND BANK LINES", line_sw((COL["river_mid"], 0.3, None, None))),
            (("line", "histwall"), u"HISTORIC WALL", line_sw((COL["histwall"], 0.3, [1.2, 0.5], None))),
            (("line", "ink"), u"BRIDGE", line_sw((COL["ink"], 0.5, None, None)))]
    for key, name, f in surv:
        if key in LEG:
            if f is None:
                def f(pg, x, y, w, h):
                    for i in range(3):
                        pg.circle(x + w * (i + 0.5) / 3, y + h / 2, h * 0.3, fill=COL["tree"], alpha=0.85)
            ctx.append((name, f))

    lines = []
    if ("walk", "bank") in LEG:
        lines.append((u"BANK WALK · CAR-FREE", line_sw((W_, 1.5, None, None), (COL["walk"], 0.7, None, None))))
    if ("walk", "street") in LEG:
        lines.append((u"STREET WALK", line_sw((W_, 1.5, None, None), (COL["walk"], 0.7, [2.2, 0.8], None))))
    if ("walk", "bed") in LEG:
        lines.append((u"BED WALK · CLOSED IN FLOODS",
                      line_sw((W_, 1.5, None, None), (COL["river_dark"], 0.7, [0.5, 0.6], None))))
    band = max(1.6, SPINE_W_M * 1000.0 / _SCALE[0])
    if "main" in LEG:
        lines.append((u"MAIN SPINE", line_sw((COL["spine"], band * 1.25, None, 0.55),
                                             (COL["spine_dark"], 0.35, None, None))))
    if ("spine", "edge") in LEG or ("spine", "over") in LEG:
        lines.append((u"STREAMSIDE SPINE", line_sw((COL["spine"], band, None, 0.75))))
    if ("spine", "deck") in LEG:
        lines.append((u"STREAMSIDE SPINE · DECK", line_sw((COL["spine"], band, [1.4, 0.9], 0.75))))
    if "path" in LEG:
        lines.append((u"PATH", line_sw((W_, 1.9, None, None), (COL["path"], 1.0, [1.0, 0.35], None))))

    links = []
    for kd in ("water", "flood", "people", "other"):
        if ("link", kd) in LEG:
            name = {"water": u"WATER MOVES", "flood": u"HIGH WATER SPREADS", "people": u"PEOPLE TO THE WATER",
                    "other": u"LINK"}[kd]

            def f(pg, x, y, w, h, kd=kd):
                link_arrow(pg, [(x, y + h / 2), (x + w, y + h / 2)], kd,
                           LINK_TYPES[kd]["heads"] if kd in LINK_TYPES else 1, 3)
            links.append((name, f))
    if "stop" in LEG:
        def f(pg, x, y, w, h):
            pg.circle(x + w / 2, y + h / 2, 2.65, fill=W_)
            pg.circle(x + w / 2, y + h / 2, 2.3, fill=COL["accent"])
            pg.text(u"1", x + w / 2, y + h / 2 - 1.0, 2.8, W_, bold=True, align="C")
        links.append((u"STOP", f))
    return [(u"ZONES", zones), (u"AROUND THE ZONES", ctx),
            (u"WALKS AND SPINES", lines), (u"LINKS", links)] + legend_v24_groups() + detail_legend()


def add_legend(sh, alt, alpha, M):
    """sh with a legend band under it: one column per group, wrapped into rows at the sheet width."""
    cols = []
    for head, items in legend_groups(alt, alpha):
        if items:
            w = LEG_SW + 3.0 + max([text_w(n, LEG_TS, True) for n, _ in items] +
                                   [text_w(head, LEG_HS, True) - LEG_SW - 3.0])
            cols.append((head, items, w))
    if not cols:
        return sh
    rows, cur, cw = [], [], 0.0
    for c in cols:
        if cur and cw + c[2] > sh.W - 2 * M:
            rows.append(cur)
            cur, cw = [], 0.0
        cur.append(c)
        cw += c[2] + LEG_GAP
    rows.append(cur)
    hs = [LEG_HS + 4.0 + max(len(c[1]) for c in r_) * LEG_ROW for r_ in rows]
    LH = sum(hs) + 6.0 * (len(rows) - 1) + M
    pg = Page(sh.W, sh.H + LH)
    pg.poly([rect(0, 0, pg.W, pg.H)], fill=COL["paper"])
    blit(pg, sh, 0.0, LH)
    y = LH
    for r_, h in zip(rows, hs):
        x = M
        for head, items, w in r_:
            pg.text(head, x, y - LEG_HS, LEG_HS, COL["ink_dark"], bold=True)
            yy = y - LEG_HS - 4.0
            for name, f in items:
                f(pg, x, yy - LEG_SH, LEG_SW, LEG_SH)
                pg.text(name, x + LEG_SW + 3.0, yy - LEG_SH / 2 - LEG_TS * 0.35, LEG_TS, COL["ink"], bold=True)
                yy -= LEG_ROW
            x += w + LEG_GAP
        y -= h + 6.0
    return pg


def sheet_head(pg, x, y_top, alt, opt, title=None):
    pg.text(u"BERGAMA · GROUP 6 · " + (title or ALT_TEXT[alt]), x, y_top - 7.0, 7.0, COL["ink_dark"], bold=True)
    pg.text(OPTION_TEXT[opt], x, y_top - 13.0, 3.4, COL["ink"], bold=True)   # v24: no names, each panel its scale


def scale_bar(pg, x, y, scale, marks=(0.0, 50.0, 100.0, 200.0)):
    """v16: 0-50-100-200 m bar (ink and white blocks) and the scale as text, at the print scale 1:scale (v21: marks
    may be given: the detail windows use 0-10-20-50 m)."""
    k = 1000.0 / scale                                    # page mm per metre
    for i, (a, b) in enumerate(zip(marks[:-1], marks[1:])):
        pg.poly([rect(x + a * k, y, x + b * k, y + 1.2)], fill=COL["ink_dark"] if i % 2 == 0 else COL["white"],
                stroke=COL["ink_dark"], lw=0.15)
    for m_ in marks:                                      # v26.1 (Prompt 8): 7 pt (KEY_MIN), the booklet's floor and
        pg.text(u"{:.0f}{}".format(m_, u" m" if m_ == marks[-1] else u""), x + m_ * k, y + 2.2, KEY_MIN, COL["ink"],
                align="C")                                # the site board's scale bars on p.24 (was 2 mm = 5.7 pt)
    pg.text(u"1:{:,.0f}".format(scale), x + marks[-1] * k + 6.0, y - 0.1, 3.4, COL["ink_dark"], bold=True)


# ================================================================ v11: the riverside walks (Thread 5)
# Survey-based, recomputed on every press from the open file (the copy of the course survey's results is the
# fallback). From the stream's reference line (STREAM_REF), every WALK_STEP m, a line square to the stream finds
# the channel edge on each bank and how much ground is free of buildings behind it:
#   edge   the outermost water line / channel top (HIDRO_DERE_SULU, SEV_SEVUST) within EDGE_WATER m; else the bank
#          top (SEV_UST) within EDGE_TOP m; else the nearest wall or building within EDGE_WALL m (masonry banks)
#   free   from the edge to the first building outline (BINA_* except sheds; buildings the zone base clears are
#          ignored)
#   class  bank walk     free >= WALK_W + WALK_CLEAR, no street on it
#          street walk   the same, but a surveyed carriageway edge (YOL_SOSE / YOL_BORDUR) lies on it: the walk
#                        is the footway of an existing street
#          bed walk      no room on the bank, but the channel is at least BED_MIN_W wide: the walk drops to a
#                        terrace in the bed beside the water strip; it closes in floods (flood rule, Thread 4)
#          none          no room on the bank and a narrow channel
# Over the covered reach (STREAM_REF's tunnel pieces, joined across open gaps under COVER_JOIN m) there are no
# bank walks: the riverside spine runs on the street over the stream there. Runs shorter than WALK_MIN_RUN m are
# dropped, gaps up to WALK_GAP m inside one class are closed; edge distances are smoothed over 5 stations.
# Graphic and design values, not data: WALK_W (the water balance's 3 m riverside walk), WALK_CLEAR, BED_MIN_W.
WALK_STEP = 2.0
WALK_W = 3.0
WALK_CLEAR = 0.5
BED_MIN_W = 10.0               # 4 m water strip + 3 m walk + 3 m to spare (design rule)
EDGE_WATER, EDGE_TOP, EDGE_WALL = 45.0, 90.0, 35.0
WALK_SEARCH = 60.0
WALK_MIN_RUN = 25.0
WALK_GAP = 10.0
COVER_JOIN = 60.0
WALK_WIN, WALK_JUMP = 15, 6.0        # stations and m: an edge this far off its neighbours is a stray line
WALK_ROLES = dict(water=("stream", "chan_top"), top=("bank_top",), obst=("building", "housing", "heritage"),
                  wall=("wall",), road=("road", "kerb"))


class SegGrid(object):
    """Segments bucketed in C-m cells; crossings of a ray with them."""

    def __init__(self, lines, skip=None, c=10.0):
        self.c, self.g = c, {}
        for P in lines:
            for a, b in zip(P, P[1:]):
                a, b = (a[0], a[1]), (b[0], b[1])
                if skip is not None and skip(((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)):
                    continue
                for gx in range(int(math.floor(min(a[0], b[0]) / c)), int(math.floor(max(a[0], b[0]) / c)) + 1):
                    for gy in range(int(math.floor(min(a[1], b[1]) / c)), int(math.floor(max(a[1], b[1]) / c)) + 1):
                        self.g.setdefault((gx, gy), []).append((a, b))

    def cross(self, p, u, t0, t1):
        """Sorted parameters t in [t0, t1] where the ray p + t u crosses a segment."""
        c = self.c
        n = int(abs(t1 - t0) / (c / 2.0)) + 2
        cells = set()
        for k in range(n + 1):
            t = t0 + (t1 - t0) * k / float(n)
            x, y = p[0] + u[0] * t, p[1] + u[1] * t
            gx, gy = int(math.floor(x / c)), int(math.floor(y / c))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    cells.add((gx + dx, gy + dy))
        out, seen = [], set()
        for cell in cells:
            for a, b in self.g.get(cell, ()):
                if (a, b) in seen:
                    continue
                seen.add((a, b))
                ex, ey = b[0] - a[0], b[1] - a[1]
                den = u[0] * ey - u[1] * ex
                if abs(den) < 1e-12:
                    continue
                wx, wy = a[0] - p[0], a[1] - p[1]
                t = (wx * ey - wy * ex) / den
                v = (wx * u[1] - wy * u[0]) / den
                if t0 <= t <= t1 and 0.0 <= v <= 1.0:
                    out.append(t)
        return sorted(out)


def stream_ref():
    """(points, covered flag per segment) of the reference line, the covered reach joined across short gaps."""
    R_ = json.loads(zlib.decompress(base64.b64decode("".join(STREAM_REF))).decode("utf-8"))
    P = [tuple(p) for p in R_["P"]]
    cov = list(R_["covered"])
    L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(P, P[1:])]
    idx = [i for i, c in enumerate(cov) if c]
    for i, j in zip(idx, idx[1:]):
        if j - i > 1 and sum(L[i + 1:j]) < COVER_JOIN:
            for k in range(i + 1, j):
                cov[k] = True
    return P, cov


def walk_stations(P, cov, step):
    """(point, unit tangent, covered, chainage m) every step m along P."""
    out, s0 = [], 0.0
    for i, (a, b) in enumerate(zip(P, P[1:])):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        n = max(1, int(L // step))
        t = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        for k in range(n):
            f = k / float(n)
            out.append(((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f), t, cov[i], s0 + L * f))
        s0 += L
    return out


def _median(v):
    v = sorted(v)
    return v[len(v) // 2]


def river_walks(survey, removes=()):
    """{"runs": [{"bank", "cls", "P", "m", "ch0", "ch1"}], "covered": [P], "stats": {...}} from the survey roles.
    removes: polygons of the buildings the zone base clears (their outlines do not block a walk)."""
    rm = [r for r in removes if len(r) >= 3]
    skip = (lambda q: any(pip(q[0], q[1], r) for r in rm)) if rm else None
    G = dict((k, SegGrid([P for role in roles for P in survey.get(role, [])], skip if k == "obst" else None))
             for k, roles in WALK_ROLES.items())
    P, cov = stream_ref()
    st = walk_stations(P, cov, WALK_STEP)
    rows = []
    for p, t, cv, ch in st:
        nl = (-t[1], t[0])                                # left of the flow: the north-east bank
        row = {"p": p, "n": nl, "cov": cv, "ch": ch}
        rows.append(row)
        if cv:
            continue
        w = G["water"].cross(p, nl, -EDGE_WATER, EDGE_WATER)
        if len(w) >= 2:                                   # the channel between its outermost water lines
            row["NE"], row["SW"] = {"e": w[-1], "water": True}, {"e": w[0], "water": True}
            row["width"] = w[-1] - w[0]
            continue
        for key, lim in (("top", EDGE_TOP), ("wall", EDGE_WALL)):
            x = G["top"].cross(p, nl, -lim, lim) if key == "top" else \
                G["obst"].cross(p, nl, -lim, lim) + G["wall"].cross(p, nl, -lim, lim)
            pos, neg = [v for v in x if v > 0.5], [v for v in x if v < -0.5]
            if pos and neg:
                row["NE"], row["SW"] = {"e": min(pos), "water": False}, {"e": max(neg), "water": False}
                row["width"] = min(pos) - max(neg)
                break
    # edges: drop jumps (more than WALK_JUMP m off the median of WALK_WIN stations), then smooth over 5
    for side, sg in (("NE", 1.0), ("SW", -1.0)):
        E = [r[side]["e"] if r.get(side) else None for r in rows]
        for i, r in enumerate(rows):
            if E[i] is None:
                continue
            near = [E[j] for j in range(max(0, i - WALK_WIN // 2), min(len(rows), i + WALK_WIN // 2 + 1)) if E[j] is not None]
            if abs(E[i] - _median(near)) > WALK_JUMP:
                r[side] = None
        E = [r[side]["e"] if r.get(side) else None for r in rows]
        for i, r in enumerate(rows):
            if E[i] is None:
                continue
            r[side]["e"] = _median([E[j] for j in range(max(0, i - 2), min(len(rows), i + 3)) if E[j] is not None])
        for r in rows:
            s = r.get(side)
            if not s:
                continue
            p, nl, e = r["p"], r["n"], s["e"]
            ob = sorted(sg * x - sg * e for x in G["obst"].cross(p, nl, *sorted((e, e + sg * WALK_SEARCH)))
                        if sg * x - sg * e > 0.05)
            s["free"] = ob[0] if ob else WALK_SEARCH
            s["street"] = bool(G["road"].cross(p, nl, *sorted((e, e + sg * (WALK_W + 1.0)))))
            if s["free"] >= WALK_W + WALK_CLEAR:
                s["cls"] = "street" if s["street"] else "bank"
                s["pos"] = e + sg * (WALK_CLEAR + WALK_W / 2.0)
            elif r.get("width", 0.0) >= BED_MIN_W:
                s["cls"] = "bed"
                s["pos"] = e - sg * (WALK_W / 2.0 + WALK_CLEAR)
            else:
                s["cls"] = None
    # runs of one class per bank
    runs = []
    for side, sg in (("NE", 1.0), ("SW", -1.0)):
        cur = None
        for r in rows + [None]:
            s = r.get(side) if r else None
            c = s["cls"] if s else None
            if cur and (r is None or c != cur["cls"] or r["ch"] - cur["ch1"] > WALK_STEP * 1.5):
                runs.append(cur)
                cur = None
            if c:
                q = (r["p"][0] + r["n"][0] * s["pos"], r["p"][1] + r["n"][1] * s["pos"])
                if cur is None:
                    cur = {"bank": side, "cls": c, "P": [], "C": [], "ch0": r["ch"]}
                cur["P"].append(q)
                cur["C"].append(r["ch"])
                cur["ch1"] = r["ch"]
    # close short gaps inside one class, drop short runs
    out = []
    for side in ("NE", "SW"):
        rs = sorted([x for x in runs if x["bank"] == side], key=lambda x: x["ch0"])
        merged = []
        for x in rs:
            y = merged[-1] if merged else None
            if y and y["cls"] == x["cls"] and x["ch0"] - y["ch1"] <= WALK_GAP + WALK_STEP:
                y["P"] += x["P"]
                y["C"] += x["C"]
                y["ch1"] = x["ch1"]
            else:
                merged.append(x)
        out += [x for x in merged if x["ch1"] - x["ch0"] >= WALK_MIN_RUN]
    for x in out:
        x["m"] = arclen(x["P"])[-1] if len(x["P"]) > 1 else 0.0
    covered, cur = [], None
    for (a, b), c in zip(zip(P, P[1:]), cov):
        if c:
            if cur is None:
                cur = [a]
            cur.append(b)
        elif cur:
            covered.append(cur)
            cur = None
    if cur:
        covered.append(cur)
    stats = {}
    for x in out:
        k = x["bank"] + " " + x["cls"]
        stats[k] = stats.get(k, 0.0) + x["m"]
    return {"runs": out, "covered": covered, "stats": stats, "ref": P, "rows": rows}   # v21; v24: rows for the corridor


# v11 constants (Thread 5)
SPINE_W_M = 6.0                # drawn width of the spines, m (graphic)
WALK_FACET_M = 4.0             # option B: walks as straight facets, Douglas-Peucker tolerance, m (graphic)
_BERGAMA = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
CITY_LINK_FILES = [os.path.join(bg_cache("Bergama_city_link_analysis"), "city_link_results.json"),   # 27 Oct: cached/
                   os.path.join(_BERGAMA, "output", "Bergama_city_link_analysis", "city_link_results.json")]


def dp_open(P, tol):
    """Douglas-Peucker on an open line."""
    if len(P) < 3:
        return list(P)
    keep, st = [0, len(P) - 1], [(0, len(P) - 1)]
    while st:
        a, b = st.pop()
        dmax, im = 0.0, None
        for i in range(a + 1, b):
            d = seg_dist(P[i][0], P[i][1], P[a], P[b])
            if d > dmax:
                dmax, im = d, i
        if im is not None and dmax > tol:
            keep.append(im)
            st += [(a, im), (im, b)]
    return [P[i] for i in sorted(keep)]


def walk_form(P, opt):
    """Form rule (Aras 16 Oct): option A follows the river edge (a soft line, organic only where the project meets
    the water); option B is straight facets (Douglas-Peucker at WALK_FACET_M)."""
    if len(P) < 3:
        return list(P)
    if opt == "B":
        return dp_open(P, WALK_FACET_M)
    Q = [P[0]] + [tuple(sum(P[j][c] for j in range(i - 2, i + 3)) / 5.0 for c in (0, 1))
                  for i in range(2, len(P) - 2)] + [P[-1]]
    return dp_open(Q, 0.4)


def chain_at(P, q):
    """Chainage (m) along P of the point of P nearest q, and that distance."""
    best, s0 = (None, 1e18), 0.0
    for a, b in zip(P, P[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L > 1e-9:
            t = max(0.0, min(1.0, ((q[0] - a[0]) * (b[0] - a[0]) + (q[1] - a[1]) * (b[1] - a[1])) / (L * L)))
            d = math.hypot(a[0] + (b[0] - a[0]) * t - q[0], a[1] + (b[1] - a[1]) * t - q[1])
            if d < best[1]:
                best = (s0 + L * t, d)
        s0 += L
    return best


def ref_between(P, s0, s1):
    """The piece of P between chainages s0 < s1."""
    s = arclen(P)
    return sub_line(P, s, max(0.0, s0), min(s[-1], s1))


def city_link():
    """(spec, source) of the riverside spine: city_link_results.json of bergama_city_link (Thread 4), read live;
    else the copy embedded here (CITY_LINK_COPY). main_spine (the
    Bankalar - Kınık Caddesi line) from the file if it has one, else MAIN_SPINE below."""
    spec, src = None, None
    for p in CITY_LINK_FILES:
        try:
            with open(p, "r", encoding="utf-8") as fh:
                spec = json.load(fh)
            src = u"city link file of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
            break
        except Exception:
            continue
    if spec is None:
        spec, src = json.loads(CITY_LINK_COPY), u"copy embedded in this script (city link file not found)"
    if not spec.get("main_spine"):
        spec["main_spine"] = MAIN_SPINE
    return spec, src


def spine_on_edge(spec, W):
    """The riverside spine on the real edge -> [{"id", "name", "kind", "P"}], kind edge (on the bank walk),
    deck (no room on the bank: a deck over the bed is needed, straight between the walk's ends) or over (on the
    street over the covered reach). Each piece runs between the chainages of its two anchors on STREAM_REF, on the
    bank city link decided by data (spine_banks: NE / SW / over; Thread 4, 24 Oct 09:14); without spine_banks, on
    the bank its side_ref stands on."""
    ref = W["ref"]
    banks = spec.get("spine_banks") or {}
    out = []
    for pc in spec.get("spine", []):
        s0, d0 = chain_at(ref, pc["frm"])
        s1, d1 = chain_at(ref, pc["to"])
        if s0 is None or s1 is None:
            continue
        if s1 < s0:
            s0, s1 = s1, s0
        name = pc.get("name", pc.get("id", ""))
        sb = banks.get(pc.get("id"))
        if sb == "over" or (sb not in ("NE", "SW") and (not pc.get("side_ref") or float(pc.get("offset_m", 0) or 0) <= 0)):
            out.append({"id": pc.get("id"), "name": name, "kind": "over", "P": ref_between(ref, s0, s1)})
            continue
        if sb in ("NE", "SW"):
            bank = sb
        else:
            r = pc["side_ref"]
            sr, _ = chain_at(ref, r)
            q, t = at_len(ref, arclen(ref), sr)
            bank = "NE" if t[0] * (r[1] - q[1]) - t[1] * (r[0] - q[0]) > 0 else "SW"
        pts = sorted([(c, p) for x in W["runs"] if x["bank"] == bank for c, p in zip(x["C"], x["P"])
                      if s0 <= c <= s1], key=lambda cp: cp[0])
        run_, last = [], None
        for c, p in pts:
            if last is not None and c - last[0] > WALK_GAP + WALK_STEP:
                if len(run_) > 1:
                    out.append({"id": pc.get("id"), "name": name, "kind": "edge", "P": run_})
                out.append({"id": pc.get("id"), "name": name, "kind": "deck", "P": [last[1], p]})
                run_ = []
            run_.append(p)
            last = (c, p)
        if len(run_) > 1:
            out.append({"id": pc.get("id"), "name": name, "kind": "edge", "P": run_})
        if not pts:                                       # no walk at all on that bank: the anchors, straight
            out.append({"id": pc.get("id"), "name": name, "kind": "deck", "P": [tuple(pc["frm"]), tuple(pc["to"])]})
    return out


def stop_points(spec, D, areas):
    """[(n, name, (x, y), placed_by)] of the spine's stops. A stop without xy is placed by a stated rule: stage
    "entry" -> the reed basins (largest WT zone) of the upstream entry, else that area's inner point; stop 8 (summer
    bed events) -> the largest bed zone (WA, tier W). Placement rules are graphic, not data."""
    out = []
    for f in spec.get("functions", []):
        n, nm = f.get("n"), f.get("name", "")
        if f.get("xy"):
            out.append((n, nm, (float(f["xy"][0]), float(f["xy"][1])), "city link"))
            continue
        cand = []
        if f.get("stage") == "entry":
            cand = [z for z in D.zones if z.get("own") == "aras_alan" and z["code"] == "WT"]
            if not cand and "calisma_alan[0]" in areas:
                out.append((n, nm, inner_pt(areas["calisma_alan[0]"]), "upstream entry, inner point"))
                continue
        else:
            cand = [z for z in D.zones if z["code"] == "WA" and z["tier"] == "W"]
        if cand:
            z = max(cand, key=lambda z: z["m2"])
            out.append((n, nm, z["q"], "largest " + ("reed basin" if f.get("stage") == "entry" else "bed zone")))
    return out


def city_layer(opt, D, areas, survey, warn):
    """Everything Thread 5 adds for one option: walks, the spine on the edge, the main spine, the stops."""
    W, src_w = None, u"survey of the open file"
    if survey.get("stream") or survey.get("chan_top") or survey.get("bank_top"):
        try:
            W = river_walks(survey, [r["P"] for r in D.removes])
        except Exception as ex:
            warn.append(u"option {}: the riverside walks were not computed ({}: {}); the embedded copy is "
                        u"used".format(opt, type(ex).__name__, ex))
    if W is None or not W["runs"]:
        cp = json.loads(zlib.decompress(base64.b64decode("".join(WALK_COPY))).decode("utf-8"))[opt]
        W = {"runs": cp["runs"], "covered": cp["covered"], "ref": stream_ref()[0], "stats": {}}
        for x in W["runs"]:
            x["P"] = [tuple(p) for p in x["P"]]
            x["m"] = arclen(x["P"])[-1] if len(x["P"]) > 1 else 0.0
            k_ = x["bank"] + " " + x["cls"]
            W["stats"][k_] = W["stats"].get(k_, 0.0) + x["m"]
        src_w = u"copy embedded in this script (from the course survey, 24 Oct)"
        warn.append(u"option {}: no stream / bank layers in the open file: the riverside walks are the embedded "
                    u"copy".format(opt))
    spec, src_c = city_link()
    sp = spine_on_edge(spec, W)
    if areas and WALK_CLIP:                              # v12: walks only inside calisma_alan (off, Aras 08:10)
        W["runs"] = clip_runs(W["runs"], areas)
        W["stats"] = {}
        for x in W["runs"]:
            k_ = x["bank"] + " " + x["cls"]
            W["stats"][k_] = W["stats"].get(k_, 0.0) + x["m"]
    for x in W["runs"]:
        x["F"] = walk_form(x["P"], opt)
    for s in sp:
        s["F"] = walk_form(s["P"], opt) if s["kind"] == "edge" else s["P"]
    m2 = sum(x["m"] for x in W["runs"]) * WALK_W
    return {"W": W, "spine": sp, "main": [tuple(p) for p in spec["main_spine"]], "stops": stop_points(spec, D, areas),
            "src_walks": src_w, "src_city": src_c, "walk_m2": m2,
            "spine_m": dict((k_, sum(arclen(s["P"])[-1] for s in sp if s["kind"] == k_)) for k_ in ("edge", "deck", "over"))}


def city_results(CLs):
    """masterplan_results.json: what other scripts read (water balance: riverside_walk_m2)."""
    out = {"script": "bergama_masterplan_v26.py", "version": VERSION,
           "run_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
           "note": "survey coordinates (m); walk width %.1f m (design value); lengths calculated from the survey" % WALK_W,
           "options": {}}
    for opt, CL in CLs.items():
        W = CL["W"]
        out["options"][opt] = {
            "riverside_walk_m2": round(CL["walk_m2"], 0),
            "walk_m_by_bank_and_class": dict((k_, round(v, 0)) for k_, v in sorted(W["stats"].items())),
            "spine_m": dict((k_, round(v, 0)) for k_, v in CL["spine_m"].items()),
            "walks": [{"bank": x["bank"], "cls": x["cls"], "m": round(x["m"], 1),
                       "P": [[round(p[0], 2), round(p[1], 2)] for p in x["F"]]} for x in W["runs"]],
            "spine": [{"id": s["id"], "name": s["name"], "kind": s["kind"],
                       "P": [[round(p[0], 2), round(p[1], 2)] for p in s["F"]]} for s in CL["spine"]],
            "stops": [{"n": n, "name": nm, "xy": [round(xy[0], 2), round(xy[1], 2)], "placed_by": how}
                      for n, nm, xy, how in CL["stops"]],
            "sources": {"walks": CL["src_walks"], "city_link": CL["src_city"]}}
    return out


# ================================================================ link helpers
# ================================================================ Rhino bake (only with rhino_bake = True)
def _flat(c, alpha):
    """A fill's colour as it shows on white paper (the bake has no opacity)."""
    return c if alpha is None or alpha >= 0.995 else mix(COL["white"], c, alpha)


def _rgb(c):
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def bake_page(rs, pg, layer, x0, y0, s):
    """The vectors of one sheet as curves, solid hatches and text on layer, at x0 + page mm x s. White fills (the
    paper and the white base) and the pattern stripes are left out; colours are flattened on white."""
    P3 = lambda p: (x0 + p[0] * s, y0 + p[1] * s, 0.0)
    ids = []

    def keep(i, colour, width=None):
        if i:
            rs.ObjectColor(i, _rgb(colour))
            if width is not None:
                rs.ObjectPrintWidth(i, width)
            ids.append(i)

    def curve(pts, closed):
        Q = [P3(p) for p in pts] + ([P3(pts[0])] if closed else [])
        return rs.AddPolyline(Q) if len(Q) >= 2 else None

    for it in pg.items:
        kd = it[0]
        if kd == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            cs = [c for c in (curve(r_, True) for r_ in rings) if c]
            if fill and fill.upper() != "FFFFFF" and cs:
                for h in rs.AddHatches(cs, "Solid") or []:
                    keep(h, _flat(fill, alpha))
            if stroke and stroke.upper() != "FFFFFF":
                for c in cs:
                    keep(c, _flat(stroke, alpha), lw)
            elif cs:
                rs.DeleteObjects(cs)
        elif kd in ("line", "clipline"):
            pts, stroke, lw = (it[1], it[2], it[3]) if kd == "line" else (it[2], it[3], it[4])
            if stroke.upper() != "FFFFFF":
                keep(curve(pts, False), stroke, lw)
        elif kd == "circle":
            _, cx, cy, r, fill, stroke, lw, alpha = it
            c = rs.AddCircle(P3((cx, cy)), r * s)
            if fill and c:
                for h in rs.AddHatches([c], "Solid") or []:
                    keep(h, _flat(fill, alpha))
            if stroke:
                keep(c, stroke, lw)
            elif c:
                rs.DeleteObject(c)
        elif kd == "text":
            _, t, x, y, size, colour, bold, align, halo = it
            keep(rs.AddText(t, P3((x, y)), size * s, "Arial", 1 if bold else 0, {"L": 1, "C": 2, "R": 4}[align]),
                 colour)
    if ids:
        rs.ObjectLayer(ids, layer)
    return len(ids)


def bake_pages(doc, pages, scale):
    """Bake the sheets into Rhino under BAKE_ROOT::<option>_alt<n>, at their print scale, to the right of
    everything else in the file and side by side (never on top of each other or of the survey). The last bake is
    deleted first."""
    import rhinoscriptsyntax as rs
    rs.EnableRedraw(False)
    try:
        for lay in list(rs.LayerNames() or []):
            if lay == BAKE_ROOT or lay.startswith(BAKE_ROOT + "::"):
                old = rs.ObjectsByLayer(lay)
                if old:
                    rs.DeleteObjects(old)
        try:
            u = Rhino.RhinoMath.UnitScale(Rhino.UnitSystem.Meters, doc.ModelUnitSystem)
        except Exception:
            u = 1.0
        s = scale / 1000.0 * u                                # model units per mm on the sheet
        x, y0 = 0.0, 0.0
        try:
            bb = doc.Objects.BoundingBox
            if bb.IsValid:
                x, y0 = bb.Max.X, bb.Min.Y
        except Exception:
            pass
        x += BAKE_GAP * pages[0][2].W * s
        n = 0
        for opt, alt, pg in pages:
            lay = u"{}::{}_alt{}".format(BAKE_ROOT, opt, alt)
            if not rs.IsLayer(lay):
                rs.AddLayer(lay)
            n += bake_page(rs, pg, lay, x, y0, s)
            x += pg.W * s * (1.0 + BAKE_GAP)
    finally:
        rs.EnableRedraw(True)
    return u"Rhino bake: layer {}, {} sheets side by side right of the file's content, {} objects  {}".format(
        BAKE_ROOT, len(pages), n, datetime.datetime.now().strftime("%H:%M:%S"))


# ================================================================ one press
def save(pg, folder, name, title):
    path = os.path.join(folder, name)
    try:
        write_pdf(pg, path, title)
    except (IOError, OSError):                       # the old file is open in another program: a new name
        path = os.path.join(folder, name.replace(".pdf", datetime.datetime.now().strftime("_%H%M%S.pdf")))
        write_pdf(pg, path, title)
    return path


def opacity_input(warn):
    v = inp("opacity", None)
    if v is None:
        return OPACITY
    try:
        f = float(str(v).strip().replace(",", ".").rstrip("%"))
        if f > 1.0:
            f /= 100.0                              # given in per cent
        if 0.0 < f <= 1.0:
            return max(0.05, f)
    except Exception:
        pass
    warn.append(u"input opacity = '{}' is not 0-1 or 1-100 %: {:g} was used".format(v, OPACITY))
    return OPACITY


def option_input():
    return ("A",)                                        # v19: option A only, project-wide (Aras 25 Oct 16:43)


def build_all(doc, warn):
    """Read, draw and write. Returns (folder, files, log lines, pages)."""
    folder = out_folder(doc)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    scale = inp_num("scale", BOARD_SCALE, warn)
    _SCALE[0] = scale                                    # v16: for the scale bar on every sheet
    ring_m = inp_num("zoom_m", None, warn)                      # v15: margin of the zoomed pages (alternatives 1-2)
    if ring_m is None:
        ring_m = inp_num("ring_m", RING_M, warn)
    alpha = opacity_input(warn)
    _ALPHA[0] = alpha                                    # v17: for the legend swatches
    if doc is not None:
        load_palette([DATA_DIR] + search_dirs(doc), warn)
    # ---- working areas (extents only), survey, base of each drawing
    areas = read_areas(doc) if doc is not None else {}
    if len(areas) < 2:                                   # v12: calisma_alan of Bergama_Altlik.3dm, built in
        areas = calisma_from([ring(list(P)) for P in CALISMA_COPY])
        warn.append(u"no calisma_alan outlines in the open file: the built-in copy (Bergama_Altlik.3dm, 25 Oct) "
                    u"was used")
    site, site_found = read_site(doc)
    if not site_found:
        warn.append(u"no site_alan outline in the open file: the built-in copy (Bergama_Altlik.3dm, 25 Oct) was used")
    V = View(areas, 0.0, 1000.0 / scale, frame=site)            # v15: alternative 3 = exactly site_alan
    bb = [bbox(A) for A in areas.values()] + [V.bb]
    R = (min(b[0] for b in bb) - ring_m - 5, min(b[1] for b in bb) - ring_m - 5,
         max(b[2] for b in bb) + ring_m + 5, max(b[3] for b in bb) + ring_m + 5)
    survey = read_survey(doc, R) if doc is not None else {}
    if not survey.get("building") and not survey.get("housing"):
        warn.append(u"no survey buildings (BINA_*) in the open file: the zones are drawn on plain paper")
    # ---- per option: the zones (file, else zone base file, else the embedded copy), the corridor, the sheets
    files, lines, pages = [], [], []
    sheets, wins, plc, missing = [], [], {}, {}           # v21: sheets for the booklet crops
    CLs, Cs = {}, {}
    zb = None
    for opt in option_input():
        its = read_items(doc, opt) if doc is not None else []
        if not its:
            if zb is None:
                zb = zone_base_file(doc, warn)
            its = [i for i in zb[1] if i["layer"].startswith("Option_" + opt + "::")]
            src = zb[0]
            if not its:
                its = [i for i in embedded_items() if i["layer"].startswith("Option_" + opt + "::")]
                src = u"the copy of zone base v5 embedded in this script"
            warn.append(u"option {}: no Option_{}::INT_ zones in the open file; {} was used".format(opt, opt, src))
        D = Design(its, areas, warn, opt)
        out_z = [z["id"] or z["label"] for z in D.zones if any(off_work(p, areas) > SNAP_M for p in z["P"])]
        if out_z:                                        # v12: proposals on calisma_alan (within SNAP_M counts as on it)
            warn.append(u"option {}: zone(s) more than {:.0f} m outside calisma_alan: {}".format(
                opt, SNAP_M, ", ".join(out_z)))
        try:                                             # v11: walks, the spine on the edge, stops
            CLs[opt] = city_layer(opt, D, areas, survey, warn)
            CL = CLs[opt]
            st_ = CL["W"]["stats"]
            lines.append(u"option {}: walks {} (m); spine on the edge {:.0f} m, no room {:.0f} m, over the covered "
                         u"reach {:.0f} m; riverside walks {:,.0f} m2 ({}; {})".format(
                             opt, ", ".join(u"{} {:.0f}".format(k_, v_) for k_, v_ in sorted(st_.items())),
                             CL["spine_m"]["edge"], CL["spine_m"]["deck"], CL["spine_m"]["over"], CL["walk_m2"],
                             CL["src_walks"], CL["src_city"]))
        except Exception as ex:
            import traceback
            CL = None
            warn.append(u"option {}: walks and spine NOT drawn ({}: {})".format(opt, type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
        C = None
        try:                                             # v24: the ecological corridor of the whole site frame
            t0 = time.time()
            spots_all = read_spots(doc, [V.bb]) if doc is not None else []
            C = Cs[opt] = Corridor(V, survey, CL, D, spots_all, warn)
            st_ = C.stats
            lines.append(u"option {}: max potential area: open {:.1f} ha, bed {:.1f} ha, buildings {:.1f} ha, roads "
                         u"{:.1f} ha; widened {} reaches, side arms {}, kept {}; terraces {} (contours {:.0f} m/ha "
                         u"upstream, {:.0f} below K5); crossings {}; viewing terrace {}; notes {}; {:.1f} s".format(
                             opt, st_[0] / 1e4, st_[3] / 1e4, st_[1] / 1e4, st_[2] / 1e4, len(C.widen), len(C.arms),
                             len(C.kept), len(C.terr), C.steep.get("up", 0.0), C.steep.get("down", 0.0),
                             len(C.cross), u"at {:.0f}, {:.0f}".format(*C.terrace["xy"]) if C.terrace else u"none",
                             len(C.notes), time.time() - t0))
            lines.append(u"option {}: no intervention: {} areas of {:.0f} ha or more ({})".format(
                opt, len(C.nogo), NI_MIN_HA, u"; ".join(u"{:.1f} ha {}".format(r_["ha"], r_["why"]) for r_ in C.nogo)))
        except Exception as ex:
            import traceback
            warn.append(u"option {}: corridor NOT computed ({}: {})".format(opt, type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
        if C is not None and opt == "A":                 # v26: the open ground for the satellite check (Google Earth)
            try:
                os.makedirs(LOG_DIR, exist_ok=True)
                os.makedirs(bg_cache(OUT_FOLDER), exist_ok=True)
                n_, f_ = open_ground_kml(C, os.path.join(LOG_DIR, OG_KML),
                                         os.path.join(bg_cache(OUT_FOLDER), u"open_ground_check.json"))
                lines.append(u"logs/{}  {} open areas of {:.2f} ha or more, {} with no plant cover (satellite 2021) "
                             u"first  {}".format(OG_KML, n_, OG_MIN_HA, f_, datetime.datetime.now().strftime("%H:%M:%S")))
            except Exception as ex:
                lines.append(u"logs/{}  NOT WRITTEN ({}: {})".format(OG_KML, type(ex).__name__, ex))
        for alt in (1,):                                 # v19: the one sheet
            name = OUT_NAME.format(opt, alt)
            t0 = time.time()
            try:
                if C is None:
                    raise ValueError(u"no corridor computed (see the warnings)")
                panels = [ground_page(C, warn), plan_page(C, warn)]   # v26: the booklet pages p.23 and p.25
                lines.append(u"masterplan page: {} callouts beside the plan; no-intervention notes placed {} of {}".format(
                    len(C.notes), C.ni_placed, len(C.nogo)))
                for r_ in C.nogo:
                    if not r_.get("placed"):
                        warn.append(u"no-intervention note not placed (no free spot in its area): {:.1f} ha {}".format(
                            r_["ha"], r_["why"]))
                LEG.clear()                              # v24: the pages carry their own legend
                pg = make_board(opt, alt, panels)
                path = save(pg, folder, name, u"Bergama masterplan {} option {} (1:{:,.0f})".format(SHORT, opt,
                                                                                                    MP_SCALE))
                files.append(path)
                pages.append((opt, alt, pg))
                sheets.append((path, pg, MP_SCALE))
                lines.append(u"{}  {}  {:.1f} s".format(os.path.basename(path),
                                                       datetime.datetime.now().strftime("%H:%M:%S"), time.time() - t0))
            except Exception as ex:
                import traceback
                lines.append(u"{}  NOT WRITTEN ({}: {})".format(name, type(ex).__name__, ex))
                warn.append(traceback.format_exc()[-480:])
        if opt == "A" and CL is not None and C is not None:   # v21: the 1:1,000 detail sheet (option A)
            name = DETAIL_NAME.format(opt)
            t0 = time.time()
            LEG.clear()
            _SCALE[0] = DT_SCALE
            try:
                plc = places(city_link()[0], CL, survey)
                wins = detail_windows(D, plc, DT_PLAN)    # v24: no text block under the plan
                spots = read_spots(doc, [w["R"] for w in wins]) if doc is not None else []
                if not spots:
                    warn.append(u"no survey spot heights ({}) in the detail windows: no spot levels".format(SPOT_LAYER))
                dpanels = []
                for w in wins:
                    missing[w["id"]] = []
                    dpanels.append(window_panel(C, w, D, CL, spots, plc, missing[w["id"]], warn))
                    for m_ in missing[w["id"]]:
                        warn.append(u"detail {}: label not placed: {}".format(w["id"], m_))
                pg = make_board(opt, 1, dpanels, title=u"MASTERPLAN · DETAIL 1:1,000")
                path = save(pg, folder, name, u"Bergama masterplan {} detail option {} (1:1,000)".format(SHORT, opt))
                files.append(path)
                pages.append((opt, "detail", pg))
                sheets.append((path, pg, DT_SCALE))
                lines.append(u"{}  {}  {:.1f} s".format(os.path.basename(path),
                                                       datetime.datetime.now().strftime("%H:%M:%S"), time.time() - t0))
            except Exception as ex:
                import traceback
                lines.append(u"{}  NOT WRITTEN ({}: {})".format(name, type(ex).__name__, ex))
                warn.append(traceback.format_exc()[-480:])
            _SCALE[0] = scale
    if CLs:                                              # v11: what the other scripts read
        try:
            res_ = city_results(CLs)
            if "A" in Cs:                                # v24: the proposal's movement (spec §4), for the site board
                C_ = Cs["A"]
                res_["movement"] = C_.movement()
                r2 = lambda p: [round(p[0], 1), round(p[1], 1)]
                res_["notes"] = [{"n": nt["n"], "text": nt["text"], "why": nt["why"], "at": [r2(p) for p in nt["at"]]}
                                 for nt in sorted(C_.notes, key=lambda nt: nt["n"])]   # v26: every reason, in full
                res_["no_intervention"] = [{"kind": r_["kind"], "why": r_["why"], "ha": round(r_["ha"], 2),
                                            "at": r2(r_["at"][0])} for r_ in C_.nogo]
                res_["open_ground_check"] = {"imagery": OPEN_CHECK.get("imagery"), "date": OPEN_CHECK.get("date"),
                                             "built_since": len(C_.built_since),
                                             "kml": getattr(C_, "og_check", None)}
            os.makedirs(bg_cache(OUT_FOLDER), exist_ok=True)       # 27 Oct: results in cached/, output/ = PDFs only
            with open(os.path.join(bg_cache(OUT_FOLDER), RESULTS_NAME), "w", encoding="utf-8") as f:
                json.dump(res_, f, ensure_ascii=False, indent=1)
            lines.append(u"{}  {}".format(RESULTS_NAME, datetime.datetime.now().strftime("%H:%M:%S")))
        except Exception as ex:
            lines.append(u"{}  NOT WRITTEN ({}: {})".format(RESULTS_NAME, type(ex).__name__, ex))
    if sheets:                                           # v21: the booklet's crops of the sheets; never breaks them
        try:
            booklet_crops(folder, sheets, wins, plc, missing)
            lines.append(u"cached/booklet/{}/blocks.json  {} crops".format(OUT_FOLDER, sum(len(sh_.panels) for _, sh_, _ in sheets)))
        except Exception as ex:
            import traceback
            lines.append(u"booklet  NOT WRITTEN ({}: {})".format(type(ex).__name__, ex))
            warn.append(traceback.format_exc()[-480:])
    return folder, files, lines, pages, scale


def run():
    btn, on = button_state()
    try:
        was = bool(sc.sticky.get(_key("prev"), False))
    except Exception:
        was = False
    pressed = (on and not was) or chain_fire(_GH_IN.get(btn), "chain_seen", btn)
    globals()["_ran_now"] = pressed
    mem_set("prev", on, persist=False)
    if not pressed:
        same = mem_get("ver", "") == VERSION        # v24.1 (Aras 27 Oct 15:35): a newly pasted version shows itself
        last = mem_get("last", "") if same else ""   # at once, idle, without the old run's time, log or warnings
        gh_status((mem_get("status", "") if same else "") or SHORT + " · idle")
        for w in (mem_get("warn", []) if same else []) or []:
            gh_message("warning", w)
        return (last if last else u"Idle. Press the Button to write the masterplan. ({})".format(VERSION)), \
            mem_get("files", [])
    t0 = time.time()
    warn, err, folder, files, lines = [], None, None, [], []
    doc = Rhino.RhinoDoc.ActiveDoc if Rhino is not None else None
    try:
        folder, files, lines, pages, scale = build_all(doc, warn)
        if to_bool(inp("rhino_bake", False)) and pages:
            try:
                lines.append(bake_pages(doc, pages, scale))
            except Exception as ex_:
                lines.append(u"Rhino bake NOT DONE ({}: {})".format(type(ex_).__name__, ex_))
    except Exception as ex_:
        import traceback
        err = u"ERROR: {}: {}".format(type(ex_).__name__, ex_)
        warn.append(traceback.format_exc()[-480:])
    lines += bg_tidy_output(OUT_FOLDER)              # 27 Oct: output/ = PDFs only
    secs = time.time() - t0
    head = [u"{} · total {:.0f} s".format(VERSION, secs), err or u"Output: {}".format(folder)]
    text = u"\n".join(head + lines)
    status = u"{} · {}".format(SHORT, "ERROR" if err else time.strftime("%H:%M") + " · {:.0f} s".format(secs))
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    mem_set("ver", VERSION)
    mem_set("last", text)
    mem_set("status", status)
    mem_set("files", files)
    mem_set("warn", warn)
    gh_status(status)
    for w in warn:
        gh_message("warning", w)
    if err:
        gh_message("error", err)
    return text, files


# ================================================================ embedded copies (fallbacks; see DATA RULES)
# ZONE_COPY: zone base v5 BASE_DATA (md5 c1f667e7eae0a000d4d80078a433427d), only the items drawn here (INT_ZONE,
# INT_WATER, INT_LINK, INT_REMOVE, INT_ROAD_path of Option_A and Option_B) with user text label, id, study_area,
# zone and link, coordinates rounded to 1 cm; v13 adds zone base v7's DG 1 / DG 2; JSON, zlib + base64 (json md5
# 81615ea37596b7b954663a368020b9a5).
#@include ../data/ZONE_COPY.py


# STREAM_REF (v11): the Selinos reference line from the frame's north-west end to the Ilıca Deresi confluence, with a
# covered flag per segment. OpenStreetMap "Selinos Çayı" (extract of 28 Jul 2026, traffic package bergama_osm.osm)
# converted with the h01 §0 formula (x = 30037.01 + (lon - 27.18127) x 86,361; y = 32121.57 + (lat - 39.123302) x
# 111,320; +-10-30 m), then moved onto the middle of the survey channel (HIDRO_DERE_SULU / walls; median of 21
# stations, 2 m apart) and thinned to 10 m. Covered = OSM tunnel / culvert ways. Calculated 24 Oct 2026, Thread 5.
#@include ../data/STREAM_REF.py

# MAIN_SPINE (v11): Bankalar Caddesi + Kınık Caddesi (OSM "secondary" ways, same extract and formula, +-10-30 m),
# from Bankalar's south end to Kınık Caddesi east of the frame's K5-K6 reach; used when city_link_results.json has no
# main_spine.
MAIN_SPINE = [[29756.1, 31655.4], [29777.7, 31668.2], [29793.7, 31679.4], [29806.4, 31691.6], [29813.1, 31702.3], [29819.3, 31712.8], [29828.2, 31728.8], [29852.9, 31760.3], [29869.5, 31780.3], [29880.9, 31808.0], [29885.0, 31824.8], [29896.2, 31862.5], [29901.7, 31880.7], [29908.9, 31905.2], [29916.1, 31928.8], [29919.2, 31939.1], [29929.8, 31960.8], [29944.8, 31984.6], [29951.9, 31990.3], [29956.3, 31993.2], [29992.8, 32017.4], [29995.4, 32019.8], [29998.6, 32022.6], [30005.0, 32029.4], [30032.5, 32038.3], [30084.6, 32056.0], [30089.7, 32057.7], [30092.6, 32056.5], [30096.2, 32055.0], [30138.7, 32039.0], [30153.1, 32036.3], [30235.7, 32021.9], [30245.0, 32020.1], [30269.2, 32015.6], [30274.2, 32014.5], [30278.7, 32012.8], [30281.9, 32010.3], [30285.0, 32007.1], [30308.8, 31981.0], [30310.4, 31979.3], [30317.5, 31972.1], [30331.6, 31957.6], [30373.7, 31924.2], [30399.9, 31903.0], [30432.4, 31879.5], [30499.5, 31831.0], [30545.8, 31800.5], [30562.8, 31796.3], [30574.8, 31795.5], [30598.1, 31797.7], [30626.3, 31799.4], [30663.0, 31801.6], [30682.2, 31803.0], [30709.6, 31804.9], [30718.5, 31805.5], [30741.5, 31803.1], [30767.5, 31791.6], [30786.2, 31779.9], [30813.0, 31760.8], [30824.8, 31752.4], [30889.1, 31700.8], [30978.8, 31622.0], [30993.4, 31611.0], [31007.0, 31604.5], [31023.2, 31601.7]]

# CITY_LINK_COPY (v11): the riverside spine, its banks (spine_banks) and stops of bergama_city_link v1.1 (24 Oct 09:15); used when Downloads/Bergama/output/Bergama_city_link_analysis/city_link_results.json is missing.
CITY_LINK_COPY = '{"spine_banks": {"A": "SW", "B": "over", "C": "SW"}, "spine": [{"id": "A", "name": "Ulu Cami to K3 bank walk", "frm": [29846.0, 32278.0], "to": [30037.0, 32122.0], "side_ref": [29844.2, 32313.3], "offset_m": 15.0, "side": "auto", "catch_m": 250.0}, {"id": "B", "name": "Junction over the covered reach", "frm": [30037.0, 32122.0], "to": [30238.7, 31931.2], "side_ref": null, "offset_m": 0.0}, {"id": "C", "name": "Red Hall to Üç Kemer bank walk", "frm": [30238.7, 31931.2], "to": [30294.0, 31792.0], "side_ref": [30245.0, 31962.0], "offset_m": 15.0, "side": "auto", "catch_m": 250.0}], "functions": [{"n": 1, "name": "Bank bazaar", "xy": [29890.4, 32243.6], "stage": null}, {"n": 2, "name": "Parchment and leather workshops", "xy": [30062.0, 32106.0], "stage": null}, {"n": 3, "name": "Junction square", "xy": [30058.0, 32047.0], "stage": null}, {"n": 4, "name": "Red Hall water terrace", "xy": [30238.7, 31931.2], "stage": null}, {"n": 5, "name": "Producers\' market", "xy": [30294.0, 31792.0], "stage": null}, {"n": 6, "name": "Study terraces", "xy": [29941.0, 32200.0], "stage": null}, {"n": 7, "name": "Clean-water classroom", "xy": null, "stage": "entry"}, {"n": 8, "name": "Summer bed events", "xy": null, "stage": null}]}'

# WALK_COPY (v11): river_walks() run on the course survey "Bergama Müdahele Alanları" (17 Oct) with each option's
# cleared buildings from ZONE_COPY, 24 Oct 2026; used only when the open file has no stream or bank layers.
#@include ../data/WALK_COPY.py

# LC_EMBED (v26): ESA WorldCover 2021 (CC BY 4.0) in survey coordinates, the site board's built-in copy
# (data/landcover/bergama_landcover_worldcover2021.json, zlib + base64): the no-intervention reasons and the
# open-ground figures read it.
#@include ../../selinus_board/data/LC_EMBED.py


if Rhino is not None:
    try:
        _txt, _files = run()
    except Exception as _ex:
        _txt, _files = u"ERROR: {}: {} ({})".format(type(_ex).__name__, _ex, VERSION), []
        gh_status(SHORT + " · ERROR")
        mem_set("ver", VERSION)
        mem_set("last", _txt)   # 25 Oct: the error stays on the log after the Button is released
        mem_set("status", SHORT + " · ERROR")
    log = _txt
    print(_txt)              # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    pdf = _files
    if globals().get("_ran_now"):
        mem_set("done", done_text(True, "ERROR" not in str(mem_get("status", "")), time.time() - _T_START))
    done = mem_get("done", "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
