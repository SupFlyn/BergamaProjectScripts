# ---------------------------------------------------------------- A3 booklet (v1.9; SCRIPT_STANDARD §8, booklet/ASSET_SPEC.md)
# One text-free vector PDF per booklet frame, drawn for the frame's own size (bk_frame), and every word as a label in
# booklet/blocks.json (the assembler sets them as live text). Figures come from this script's own tables and cuts.
# Booklet drawings are option A only. Words: the plan's labels; the site's watercourse is the Selinos "stream".
BK_SLOTS = {"b1_hero": (260.0, 176.0), "b1_side": (128.0, 176.0), "b2_hero": (260.0, 176.0), "b4_side": (128.0, 176.0),
            "b5_strip": (392.0, 56.0), "b5_hero": (260.0, 176.0), "c6_s1": (293.0, 56.0), "c6_s2": (293.0, 56.0),
            "c6_s3": (293.0, 56.0), "c6_s4": (293.0, 56.0), "c8_a": (194.0, 176.0)}
BK_PT, BK_KEY = 7.5, 9.5             # label sizes, pt (key labels up to 9.5)
BK_INK, BK_INK2, BK_ACC = "4A3F35", "6B645B", "8B3A3F"
_DET_PROF = []                       # the S4 ground profile draw_detail used (survey re-cut or embedded)


def bk_disp(s):
    """A label as the assembler prints it, for measuring: {src:..} -> [00], {val:..} -> a 7-figure number."""
    import re
    return re.sub(r"\{val:[^}]+\}", u"000,000", re.sub(r"\{src:[^}]+\}", u"[00]", s))


def bk_box(s, x, y, size, bold=False, align="L"):
    """The assembler's label box (mm, y down): baseline y, width measured at size pt."""
    w = text_w(bk_disp(s), size * PT, bold)
    bx = x - (w / 2.0 if align == "C" else w if align == "R" else 0.0)
    return (bx, y - size * PT * 0.72, bx + w, y + size * PT * 0.21)


def bk_hit(a, b, pad=0.0):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


class BkPage(Page):
    """A booklet drawing at its frame's size. Geometry calls here take y DOWN from the top (as the labels do);
    text items carry their size in pt and become labels (never PDF text)."""

    def __init__(self, key):
        w, h = bk_frame(OUT_FOLDER + "/" + key, *BK_SLOTS[key])
        Page.__init__(self, w, h)
        self.key = key

    def ln(self, pts, col, lw=0.25, dash=None, cap=1):
        self.line([(x, self.H - y) for x, y in pts], col, lw, dash, cap)

    def pl(self, rings, fill=None, stroke=None, lw=0.2, dash=None, alpha=None):
        self.poly([[(x, self.H - y) for x, y in r] for r in rings], fill, stroke, lw, dash, None, None, alpha)

    def rc(self, x0, y0, x1, y1, fill=None, stroke=None, lw=0.2, alpha=None):
        self.pl([rect(x0, y0, x1, y1)], fill, stroke, lw, None, alpha)

    def ic(self, kind, x, y, sz):
        icon(self, kind, x, self.H - y, sz)

    def boxes(self):
        return [bk_box(it[1], it[2], self.H - it[3], it[4], it[6], it[7]) for it in self.items if it[0] == "text"]

    def fits(self, s, x, y, size=BK_PT, bold=False, align="L", pad=0.8):
        b = bk_box(s, x, y, size, bold, align)
        if b[0] < 0.4 or b[2] > self.W - 0.4 or b[1] < 0.4 or b[3] > self.H - 0.4:
            return False
        return not any(bk_hit(b, o, pad) for o in self.boxes())

    def lab(self, s, x, y, size=BK_PT, colour=BK_INK, bold=False, align="L"):
        self.text(s, x, self.H - y, size, colour, bold, align)
        return bk_box(s, x, y, size, bold, align)

    def lab_near(self, s, cands, size=BK_PT, colour=BK_INK, bold=False, anchor=None, lead=None):
        """The first candidate (x, y, align) where the label fits; a thin leader from the label to anchor."""
        pick = next((c for c in cands if self.fits(s, c[0], c[1], size, bold, c[2])), cands[0])
        b = self.lab(s, pick[0], pick[1], size, colour, bold, pick[2])
        if anchor:
            ex = min(max(anchor[0], b[0]), b[2])
            ey = b[3] + 0.4 if anchor[1] > b[3] else (b[1] - 0.4 if anchor[1] < b[1] else (b[1] + b[3]) / 2.0)
            if abs(ex - anchor[0]) + abs(ey - anchor[1]) > 1.0:
                self.ln([(ex, ey), anchor], lead or colour, 0.15)
        return b

    def finish(self):
        """Lines never under 0.1 mm."""
        out = []
        for it in self.items:
            if it[0] == "poly":
                it = it[:4] + (max(0.1, it[4]),) + it[5:]
            elif it[0] == "line":
                it = it[:3] + (max(0.1, it[3]),) + it[4:]
            elif it[0] == "circle":
                it = it[:6] + (max(0.1, it[6]),)
            out.append(it)
        self.items = out


def bk_check(labels, W, H):
    """What the assembler would log for this frame: overlapping labels, labels outside the frame, type too small."""
    probs, boxes = [], []
    for lb in labels:
        b = bk_box(lb["text"], lb["x"], lb["y"], lb["size"], lb["bold"], lb["anchor"])
        if any(bk_hit(b, o) for o in boxes):
            probs.append(u"labels overlap: " + lb["text"][:30])
        if b[0] < 0 or b[2] > W or b[1] < 0 or b[3] > H:
            probs.append(u"label outside the frame: " + lb["text"][:30])
        if lb["size"] < BK_PT:
            probs.append(u"label below 7.5 pt: " + lb["text"][:30])
        boxes.append(b)
    return probs


def bk_scalebar(pg, x1, y, metres, k):
    """Scale bar ending at x1 (mm), baseline y; two halves; its numbers are labels."""
    L = metres * k
    x0 = x1 - L
    pg.rc(x0, y - 1.6, x0 + L / 2.0, y - 0.4, fill=BK_INK)
    pg.rc(x0 + L / 2.0, y - 1.6, x1, y - 0.4, fill="FFFFFF", stroke=BK_INK, lw=0.15)
    pg.lab(u"0", x0 - 1.2, y, align="R", colour=BK_INK2)
    pg.lab(u"{:.0f} m".format(metres), x1 + 1.2, y, colour=BK_INK2)


def bk_months(pg, X, y):
    for i, m in enumerate(WY):
        pg.lab(MONTHS[m][0], X(i), y, colour=BK_INK2, align="C")


# ---------------------------------------------------------------- B1 hero: the year of the water
def bk_year(pg, res):
    H = pg.H
    gx0, gx1, rx = 16.0, 192.0, 198.0
    mw = (gx1 - gx0) / 12.0

    def X(i):
        return gx0 + (i + 0.5) * mw

    def grid(yb, h, vmax, ticks, fmt):
        for t in ticks:
            yy = yb - h * t / vmax
            pg.ln([(gx0, yy), (gx1, yy)], COL["faint"], 0.12)
            pg.lab(fmt(t), gx0 - 1.6, yy + 0.95, colour=BK_INK2, align="R")
        pg.ln([(gx0, yb), (gx1, yb)], COL["ink2"], 0.25)
    # ---- row 1: rain and open-water evaporation
    yb, h, vmax = 46.0, 35.0, 220.0
    pg.rc(gx0, 3.9, gx0 + 3.2, 6.0, fill=C["w3"])
    b = pg.lab(YEAR_SRC[0][0], gx0 + 4.4, 6.0, bold=True)
    pg.rc(b[2] + 6.0, 3.9, b[2] + 9.2, 6.0, fill=C["structure"])
    b = pg.lab(u"open-water evaporation", b[2] + 10.4, 6.0)
    pg.lab(u"+ = rain > evaporation", b[2] + 8.0, 6.0, colour=C["d3"], bold=True)
    grid(yb, h, vmax, (0, 100, 200), lambda t: u"{:.0f}".format(t))
    for i, m in enumerate(WY):
        x = gx0 + i * mw
        hr, he = h * RAIN[m] / vmax, h * EVAP[m] / vmax
        pg.rc(x + 0.12 * mw, yb - hr, x + 0.48 * mw, yb, fill=C["w3"])
        pg.rc(x + 0.52 * mw, yb - he, x + 0.88 * mw, yb, fill=C["structure"])
        if RAIN[m] > EVAP[m]:
            cx, cy = x + 0.30 * mw, yb - hr - 2.4
            pg.ln([(cx - 1.1, cy), (cx + 1.1, cy)], C["d3"], 0.4)
            pg.ln([(cx, cy - 1.1), (cx, cy + 1.1)], C["d3"], 0.4)
    jul = WY.index(6)
    x = gx0 + jul * mw
    d_jul = RAIN[6] - EVAP[6]
    yr, ye = yb - h * RAIN[6] / vmax, yb - h * EVAP[6] / vmax
    pg.ln([(x + 0.5 * mw, yr), (x + 0.5 * mw, ye)], BK_ACC, 0.35)
    for yy in (yr, ye):
        pg.ln([(x + 0.5 * mw - 1.0, yy), (x + 0.5 * mw + 1.0, yy)], BK_ACC, 0.35)
    pg.ln([(x + 0.5 * mw, ye - 0.6), (x + 0.5 * mw, 10.6), (rx - 1.0, 10.6)], BK_ACC, 0.15)
    pg.lab(u"July: {:.1f} mm".format(d_jul), rx, 11.6, colour=BK_ACC, bold=True)
    res["year"] = {"rain_mm_year": round(sum(RAIN), 1), "evaporation_mm_year": round(sum(EVAP), 1),
                   "july_rain_minus_evaporation_mm": round(d_jul, 1),
                   "surplus_months": [MONTHS[m] for m in WY if RAIN[m] > EVAP[m]]}
    # ---- row 2: the stream past the site
    yb, h, vmax = 98.0, 34.0, 7.5e6
    pg.lab(u"stream, million m³ a month", gx0, 58.0, bold=True)
    grid(yb, h, vmax, (0, 2e6, 4e6, 6e6), lambda t: u"{:.0f}".format(t / 1e6))
    win = set(WY.index(m) for m in (11, 0, 1, 2, 3))
    for i, m in enumerate(WY):
        x = gx0 + i * mw
        hh = max(0.25, h * RIVER[m] / vmax)
        pg.rc(x + 0.15 * mw, yb - hh, x + 0.85 * mw, yb, fill=MP["discharge"][2] if i in win else MP["discharge"][0])
    a, b_ = min(win), max(win)
    yk = yb - h * max(RIVER) / vmax - 2.2
    pg.ln([(gx0 + a * mw + 1.0, yk + 1.2), (gx0 + a * mw + 1.0, yk), (gx0 + (b_ + 1) * mw - 1.0, yk),
           (gx0 + (b_ + 1) * mw - 1.0, yk + 1.2)], MP["discharge"][2], 0.3)
    pg.lab(u"Dec-Apr: storage fills", gx0 + (b_ + 1) * mw + 1.5, yk + 1.0, colour=MP["discharge"][2], bold=True)
    dry = [WY.index(m) for m in (6, 7, 8)]
    yd = yb - h * max(RIVER[m] for m in (6, 7, 8)) / vmax - 3.0
    pg.ln([(gx0 + dry[0] * mw + 1.0, yd + 1.2), (gx0 + dry[0] * mw + 1.0, yd), (gx1 - 1.0, yd), (gx1 - 1.0, yd + 1.2)],
          BK_INK2, 0.3)
    pg.lab(u"Jul-Sep: trickle or dry bed", gx1 - 1.0, yd - 1.6, colour=BK_INK2, align="R")
    tot = float(sum(RIVER))
    res["year"].update({"stream_m3_year": int(sum(RIVER)),
                        "stream_dec_apr_pct": round(100.0 * sum(RIVER[m] for m in (11, 0, 1, 2, 3)) / tot, 1),
                        "stream_jul_sep_m3_month": [RIVER[m] for m in (6, 7, 8)]})
    # ---- row 3: mean depth in the bed
    yb, h, vmax = 157.0, 44.0, 0.7

    def Yd(v):
        return yb - h * min(v, vmax) / vmax
    pg.lab(u"mean depth in the bed, m", gx0, 109.0, bold=True)
    grid(yb, h, vmax, (0.0, 0.2, 0.4, 0.6), lambda t: u"{:.1f}".format(t))
    pg.ln([(gx0, Yd(STRIP_DEPTH)), (gx1, Yd(STRIP_DEPTH))], MP["storage"][2], 0.4, dash=[1.2, 0.8])
    pg.lab(u"strip {:.2f} m (design)".format(STRIP_DEPTH), gx1 - 1.0, Yd(STRIP_DEPTH) - 1.2, colour=MP["storage"][2],
           bold=True, align="R")
    series = [(u"upstream entry", ("up",), MP["discharge"][1], 0.5, [1.4, 0.7]),
              (u"K4 · K5 · downstream reach", ("k4", "k5", "down"), "3C5159", 0.5, None),
              (u"flat downstream end", ("flat",), MP["discharge"][2], 0.9, None)]
    ly = 116.0
    for lab, keys, colr, lw, dash in series:
        lo = [min(DEPTH[k][g][WY[i]] for k in keys for g in (0, 1)) for i in range(12)]
        hi = [max(DEPTH[k][g][WY[i]] for k in keys for g in (0, 1)) for i in range(12)]
        pg.pl([[(X(i), Yd(hi[i])) for i in range(12)] + [(X(i), Yd(lo[i])) for i in range(11, -1, -1)]],
              fill=colr, alpha=0.15)
        pg.ln([(X(i), Yd(hi[i])) for i in range(12)], colr, lw, dash=dash)
        pg.ln([(rx, ly - 0.9), (rx + 6.0, ly - 0.9)], colr, max(lw, 0.5), dash=dash)
        pg.lab(lab, rx + 7.5, ly)
        ly += 4.6
    pg.lab(u"low-flow depths indicative", rx, ly + 1.0, colour=BK_INK2)
    bk_months(pg, X, 163.5)


# ---------------------------------------------------------------- B1 side: greenness by month
def bk_ndvi(pg, res):
    gx0, gx1, yt, yb = 14.0, 124.0, 16.0, 156.0
    mw = (gx1 - gx0) / 12.0
    v0, v1 = 0.10, 0.35

    def X(i):
        return gx0 + (i + 0.5) * mw

    def Yn(v):
        return yb - (yb - yt) * (v - v0) / (v1 - v0)
    pg.lab(YEAR_SRC[5][0], gx0, 6.0, bold=True)
    for t in (0.1, 0.2, 0.3):
        pg.ln([(gx0, Yn(t)), (gx1, Yn(t))], COL["faint"], 0.12)
        pg.lab(u"{:.1f}".format(t), gx0 - 1.6, Yn(t) + 0.95, colour=BK_INK2, align="R")
    pg.ln([(gx0, yb), (gx1, yb)], COL["ink2"], 0.25)
    dates = {}
    for doy, word, nm in ((LEAF_OFF, u"leaf-fall", "leaf_fall"), (LEAF_ON, u"leaf-out", "leaf_out")):
        d = datetime.date(2021, 1, 1) + datetime.timedelta(days=doy - 1)
        dates[nm] = u"{} {}".format(d.day, MONTHS[d.month - 1])
        xx = gx0 + wy_pos(doy) * mw
        pg.ln([(xx, yt - 1.0), (xx, yb)], "495338", 0.25, dash=[0.8, 0.8])
        pg.lab(u"{} {}".format(word, dates[nm]), xx + 1.0, yt + 2.0, colour="495338")
    rip, rest = NDVI[0][4], NDVI[1][4]
    pg.ln([(X(i), Yn(rest[WY[i]])) for i in range(12)], COL["structure"], 0.6, dash=[1.2, 0.8])
    pg.ln([(X(i), Yn(rip[WY[i]])) for i in range(12)], "495338", 0.7)
    top3 = min(Yn(rip[WY[i]]) for i in range(3))
    pg.lab(u"riparian strip, 0-30 m", gx0 + 1.0, top3 - 3.0, colour="495338", bold=True)
    pg.lab(u"rest of the site frame", gx0 + 1.0, max(Yn(rest[WY[i]]) for i in range(3)) + 5.0, colour=BK_INK2)
    j = WY.index(6)
    ya, yb_ = Yn(rip[6]), Yn(rest[6])
    pg.ln([(X(j), ya + 1.4), (X(j), yb_ - 1.4)], BK_ACC, 0.35)
    for yy in (ya + 1.4, yb_ - 1.4):
        pg.ln([(X(j) - 1.0, yy), (X(j) + 1.0, yy)], BK_ACC, 0.35)
    pg.lab(u"July: {:.2f} vs {:.2f}".format(rip[6], rest[6]), X(j) - 1.8, (ya + yb_) / 2.0 + 1.0, colour=BK_ACC,
           bold=True, align="R")
    bk_months(pg, X, yb + 6.0)
    res["greenness"] = {"july_riparian": rip[6], "july_rest_of_frame": rest[6], "leaf_out": dates["leaf_out"],
                        "leaf_fall": dates["leaf_fall"]}


# ---------------------------------------------------------------- B2 hero: six surveyed cuts at one scale
BK_CUT_NAMES = {"up": u"upstream entry", "k4": u"K4 bridge", "k5": u"K5 bridge", "down": u"downstream reach",
                "s4": u"S4 cut", "flat": u"flat downstream end"}


def bk_s4_cut(res_log=None):
    """The S4 cut in the form of CUTS: ground every 1 m above the bed low point, bed, the three drawn levels and
    their wet widths, the road edges; levels as the S4 detail prints them."""
    E = detail_engine()
    prof = _DET_PROF[0] if _DET_PROF else (E["PROFILE_S0"], E["PROFILE_DS"], E["PROFILE_Z"])
    bed = E["THALWEG"][1]
    s0, s1 = 548, 660
    g = [E["prof_z"](prof, float(s)) - bed for s in range(s0, s1 + 1)]
    hd = next(w[0] for s in E["SEASONS"] if s["key"] == "winter" for w in s["water"] if "highest" in w[2]) - bed
    dep = (None, hd, None, E["Q100"] - bed, E["Q500"] - bed)
    i0 = min(range(len(g)), key=lambda i: g[i])
    ext = [None] * 5
    for k in (1, 3, 4):
        a = b = i0
        while a > 0 and g[a - 1] < dep[k]:
            a -= 1
        while b < len(g) - 1 and g[b + 1] < dep[k]:
            b += 1
        ext[k] = (s0 + a - 0.5, s0 + b + 0.5)
    road = [s for s, what, z in E["SURVEY_MARKS"] if what.startswith("road edge")]
    return dict(key="s4", bed=bed, u0=s0, ground=g, dep=dep, ext=ext, road=(min(road), max(road)) if road else None)


def bk_bank_top(g, i0, step):
    """(toe, crest) index of the bank going out from the bed at i0 in direction step: a steep rise (0.15 m or more
    per metre, 0.5 m or more in all) with level or falling ground behind it (the next 5 m within 0.15 m of its top);
    the crest is the highest point of that top. None if the cut shows none."""
    i, toe = i0, None
    while 0 <= i + step < len(g):
        if g[i + step] - g[i] >= 0.15:
            toe = i if toe is None else toe
        elif toe is not None:
            behind = [j for j in range(i, i + 6 * step, step) if 0 <= j < len(g)]
            if g[i] - g[toe] >= 0.5 and len(behind) == 6 and max(g[j] for j in behind) - g[i] <= 0.15:
                return toe, max(behind, key=lambda j: g[j])
            toe = None
        i += step
    return None


def bk_cuts(pg, res):
    W, H = pg.W, pg.H
    k = 1000.0 / 1500.0                                 # 1:1,500 across, vertical x8
    ky = 8.0 * k
    cuts = {c["key"]: c for c in CUTS}
    cuts["s4"] = bk_s4_cut()
    order = [["up", "k4", "k5"], ["down", "s4", "flat"]]
    cw, rh = W / 3.0, (H - 10.0) / 2.0
    res["cuts"] = {}
    over_labels = []
    for r, row in enumerate(order):
        top = max(max(d for d in cuts[c]["dep"] if d is not None) for c in row) + 0.8
        y0 = r * rh + 4.0 + max(0.0, (rh - (9.0 + (top + 0.6) * ky + 19.0)) / 2.0)   # the row's content centred
        ybed = y0 + 9.0 + top * ky
        for c_, key in enumerate(row):
            cut = cuts[key]
            g, u0, dep, ext = cut["ground"], cut["u0"], cut["dep"], cut["ext"]
            wd = (len(g) - 1) * k
            xl = c_ * cw + (cw - wd) / 2.0

            def T(u, z):
                return (xl + (u - u0) * k, ybed - z * ky)
            pg.lab(BK_CUT_NAMES[key], xl, y0 + 4.0, size=8.5, bold=True)
            # ground
            top_pts = [T(u0 + i, min(z, top)) for i, z in enumerate(g)]
            pg.pl([top_pts + [T(u0 + len(g) - 1, -0.6), T(u0, -0.6)]], fill=COL["structure"])
            pg.ln(top_pts, COL["ink"], 0.3)
            i0 = min(range(len(g)), key=lambda i: g[i])
            # overtopping: Q100 / Q500 above the first bank top on either side
            info = {"bed": round(cut["bed"], 2), "highest_day_m": round(dep[1], 2), "q100_m": round(dep[3], 2),
                    "q500_m": round(dep[4], 2), "q100_level": round(cut["bed"] + dep[3], 2),
                    "q500_level": round(cut["bed"] + dep[4], 2)}
            for step, side in ((-1, "right"), (1, "left")):
                bt = bk_bank_top(g, i0, step)
                if not bt:
                    continue
                toe, tp = bt
                flooded = []
                for lev in (3, 4):
                    a, b = ext[lev]
                    reach = (a - u0) if step < 0 else (b - u0)
                    if dep[lev] > g[tp] + 0.005 and (reach - tp) * step > 0.5:
                        end = int(round(reach))
                        idx = list(range(tp, end + step, step))
                        idx = [i for i in idx if 0 <= i < len(g)]
                        ring = [T(u0 + i, dep[lev]) for i in idx] + [T(u0 + i, min(g[i], dep[lev])) for i in idx[::-1]]
                        pg.pl([ring], fill=BK_ACC, alpha=0.35)
                        flooded.append(lev)
                if flooded:
                    pg.ln([T(u0 + i, g[i]) for i in range(toe, tp + step, step)], BK_ACC, 0.9)
                    info["over_%s_bank_q500_m" % side] = round(dep[4] - g[tp], 2)
                    info["%s_bank_top_m" % side] = round(g[tp], 2)
                    xe = T(ext[4][0] if step < 0 else ext[4][1], 0)[0]
                    xt = T(u0 + tp, 0)[0]
                    over_labels.append((key, side, round(dep[4] - g[tp], 2), T(u0 + tp, dep[4]),
                                        (min(xe, xt), max(xe, xt)), y0))
            # levels
            for lev, colr, lw in ((1, LEVEL_COL[1], 0.4), (3, LEVEL_COL[3], 0.55), (4, LEVEL_COL[4], 0.7)):
                a, b = ext[lev]
                pg.ln([T(a, dep[lev]), T(b, dep[lev])], colr, lw)
            if cut.get("road"):
                ra, rb = cut["road"]
                za = max(g[int(round(ra - u0))], g[int(round(rb - u0))])
                pg.rc(T(ra, 0)[0], T(0, za)[1] - 0.9, T(rb, 0)[0], T(0, za)[1] - 0.1, fill=BK_INK)
                rx_ = (T(ra, 0)[0] + T(rb, 0)[0]) / 2.0
                pg.lab_near(u"road", [(rx_, ybed + 0.6 * ky + 3.8, "C"), (rx_, T(0, za)[1] + 4.6, "C")],
                            colour=BK_INK2, anchor=(rx_, T(0, za)[1] - 0.2), lead=BK_INK)
            base = ybed + 0.6 * ky
            if r == 0 and c_ == 0:
                pg.lab(u"right bank", xl, base + 3.8, colour=BK_INK2)
                pg.lab(u"left bank", xl + wd, base + 3.8, colour=BK_INK2, align="R")
            yy = base + 8.0
            for t, colr in ((u"bed {:+.2f}".format(cut["bed"]), BK_INK),
                            (u"highest day {:.2f} m".format(dep[1]), LEVEL_COL[1]),
                            (u"Q100 {:.2f} m ({:+.2f})".format(dep[3], cut["bed"] + dep[3]), LEVEL_COL[3]),
                            (u"Q500 {:.2f} m ({:+.2f})".format(dep[4], cut["bed"] + dep[4]), LEVEL_COL[4])):
                pg.lab(t, xl, yy, colour=colr, bold=t.startswith(u"Q"))
                yy += 3.5
            res["cuts"][key] = info
    for key, side, d, anc, (xa, xb), y0 in over_labels:
        t = u"over the {} bank".format(side) + (u" by {:.2f} m".format(d) if key == "s4" else u"")
        xm = (xa + xb) / 2.0
        pg.lab_near(t, [(xm, anc[1] - 3.0, "C"), (xa, anc[1] - 3.0, "L"), (xb, anc[1] - 3.0, "R"),
                        (xm, anc[1] - 6.5, "C"), (xa, y0 + 7.5, "L")], colour=BK_ACC, bold=True,
                    anchor=(xm, anc[1] + 0.8))
    bk_scalebar(pg, W - 12.0, H - 3.0, 50.0, k)
    res["cuts_scale"] = "1:1,500 across, vertical x8"


# ---------------------------------------------------------------- B4 side: storage cubes to scale
def bk_cubes(pg, res):
    W, H = pg.W, pg.H
    k = 1000.0 / 1250.0
    mix = u"orchard olive + cropland cotton"
    try:
        v_seal = float(WB["today_strip_storage"][mix]["storage_m3"])
    except Exception:
        v_seal = VOL_SEALED
    try:
        v_cut = float(WB["design"]["storage_m3"])
    except Exception:
        v_cut = float(WB_STORE[1])
    e1, e2, e3, e4 = [v ** (1.0 / 3.0) for v in (VOL_FIRST, v_seal, VOL_UNSEALED, v_cut)]

    def cube(e, tones, solid, dash=None):
        tmp = Page(0, 0)
        draw_cube(tmp, BoxView(PSI, 0.0, k, 0.0, 0.0), 0, 0, e, tones, solid, dash)
        return tmp

    def put(part, x, y_bottom):
        """Place a part (y up) with its bbox left at x and its bottom at y_bottom (y down); returns the bbox, y down."""
        bb = items_bbox(part.items)
        dx, dy = x - bb[0], (H - y_bottom) - bb[1]
        pg.items += xform(part.items, 1.0, dx, dy)
        return (x, y_bottom - (bb[3] - bb[1]), x + bb[2] - bb[0], y_bottom)
    nest = cube(e2, MP["storage"], True)
    nest.items += cube(e3, MP["storage"], False).items
    big = cube(e4, MP["discharge"], False, [1.6, 0.8])
    small = cube(e1, MP["discharge"], True)
    bb_big = put(big, 3.0, H - 10.0)
    bb_nest = put(nest, 3.0, bb_big[1] - 6.0)
    x_lab = bb_nest[2] + 4.0
    bb_small = put(small, x_lab, bb_nest[1] + (items_bbox(small.items)[3] - items_bbox(small.items)[1]))
    y = bb_small[1] + 3.0
    pg.lab(u"first fill {:,.0f} m³".format(VOL_FIRST), bb_small[2] + 2.5, bb_small[1] + 4.0, bold=True)
    pg.lab(u"strip: 2,949 m x 4 m x {:.2f} m".format(STRIP_DEPTH), bb_small[2] + 2.5, bb_small[1] + 7.6,
           colour=BK_INK2)
    y = max(bb_small[3], bb_small[1] + 8.0) + 8.0
    for t, bold, colr in ((u"strip, sealed bed {val:Bergama_water_balance_analysis/water_balance_results.json:"
                           u"today_strip_storage.orchard olive + cropland cotton.storage_m3|0} m³", True, BK_INK),
                          (u"unsealed bed: ≥ {:,.0f} m³".format(VOL_UNSEALED), True, BK_INK),
                          (u"worst case -30.7 % {src:mgm_2025_deficit}", False, BK_INK2),
                          (u"seepage 5 / 25 mm a day {src:fao_seepage}", False, BK_INK2)):
        pg.lab(t, x_lab, y, bold=bold, colour=colr)
        y += 3.8
    xb = bb_big[2] + 3.0
    pg.lab(u"cut-off {val:Bergama_water_balance_analysis/water_balance_results.json:design.storage_m3|0} m³",
           xb, bb_big[1] + 12.0, bold=True)
    bk_scalebar(pg, W - 10.0, H - 3.0, 20.0, k)
    res["storage"] = {"first_fill_m3": VOL_FIRST, "strip_sealed_m3": v_seal, "strip_unsealed_m3": VOL_UNSEALED,
                      "cut_off_m3": v_cut, "edges_m": [round(e, 1) for e in (e1, e2, e3, e4)], "scale": "1:1,250"}


# ---------------------------------------------------------------- B5 strip: one way, with the stream (pictograms)
BK_CHAIN = [("sewer_x", u"0 sewer: 3 km + 500 m {src:gercek_izmir_sewer}", u"completion not verified"),
            ("rain", u"1 stream in · mostly winter", None), ("reed", u"2 reed beds clean once", None),
            ("tank", u"3 terraces hold runoff", None), ("cube", u"4 basins hold winter water", None),
            ("over", u"5 spillway to the stream", None),
            ("strip", u"6 strip 4 m x {:.2f} m".format(STRIP_DEPTH), u"only above legal minimum flow"),
            ("flood", u"7 strip waters planting", None), ("spread", u"8 floods onto terraces", None),
            ("clean", u"10 clean stream leaves", None), ("farm", u"11 farmland outside", None)]


def bk_chain(pg, res):
    W, H = pg.W, pg.H
    n = len(BK_CHAIN)
    sw, sz, yi = W / n, 13.0, 9.5
    for i, (kind, t, sub) in enumerate(BK_CHAIN):
        cx = (i + 0.5) * sw
        pg.ic(kind, cx - sz / 2.0, yi, sz)
        if i % 2 == 0:
            pg.lab(t, cx, yi + sz + 6.0, align="C")
            if sub:
                pg.lab(sub, cx, yi + sz + 9.6, align="C", colour=BK_INK2)
        else:
            pg.lab(t, cx, yi - 3.2, align="C")
        if 0 < i < n - 1:
            arrow(pg, [(cx + sz / 2.0 + 1.5, H - yi - sz / 2.0), (cx + sw - sz / 2.0 - 1.5, H - yi - sz / 2.0)],
                  C["w3"], 0.6, 2.2)
    yr = H - 9.0
    xa, xb = 1.5 * sw, (n - 1.5) * sw
    pg.ln([(xa + 2.0, yr), (xb, yr)], BK_INK2, 0.35, dash=[1.2, 0.8])
    pg.pl([[(xa, yr), (xa + 2.4, yr - 1.0), (xa + 2.4, yr + 1.0)]], fill=BK_INK2)
    xm = (xa + xb) / 2.0
    pg.ln([(xm - 2.2, yr - 2.2), (xm + 2.2, yr + 2.2)], BK_ACC, 0.6)
    pg.ln([(xm - 2.2, yr + 2.2), (xm + 2.2, yr - 2.2)], BK_ACC, 0.6)
    pg.lab(u"no pumping back", xm + 4.0, yr + 1.0, colour=BK_ACC, bold=True)
    pg.lab(u"gravity · no pumps", xa - 3.0, yr + 1.0, colour=MP["discharge"][2], bold=True, align="R")


# ---------------------------------------------------------------- B5 hero: what reed beds remove, coliforms left
def bk_cleaning(pg, res):
    W, H = pg.W, pg.H
    x0, x1, yt, yb = 16.0, 150.0, 14.0, 128.0
    pg.lab(u"% removed", x0, 7.0, bold=True)
    for t in (0, 50, 100):
        yy = yb - (yb - yt) * t / 100.0
        pg.ln([(x0, yy), (x1, yy)], COL["faint"], 0.12)
        pg.lab(str(t), x0 - 1.6, yy + 0.95, colour=BK_INK2, align="R")
    cols = [C["wet1"], C["d2"], C["wet"]]
    gw = (x1 - x0) / len(WETLAND_KEYS)
    bw = gw * 0.78 / len(WETLAND)
    for i, nm in enumerate(WETLAND_KEYS):
        for j, (_, vals) in enumerate(WETLAND):
            bx = x0 + i * gw + gw * 0.11 + j * bw
            pg.rc(bx, yb - (yb - yt) * vals[i] / 100.0, bx + bw * 0.9, yb, fill=cols[j])
        pg.lab(u"solids" if nm == u"Solids" else nm.replace(u"Total", u"total"), x0 + (i + 0.5) * gw, yb + 5.0,
               align="C")
    pg.ln([(x0, yb), (x1, yb)], COL["ink2"], 0.25)
    for j, (nm, _) in enumerate(WETLAND):
        yy = yb + 15.0 + j * 4.6
        pg.rc(x0, yy - 2.4, x0 + 4.0, yy - 0.2, fill=cols[j])
        pg.lab(nm.lower() if j else nm[0].lower() + nm[1:], x0 + 5.5, yy)
    res["cleaning"] = {"removal_pct": {nm: dict(zip(WETLAND_KEYS, vals)) for nm, vals in WETLAND}}
    # coliforms, log scale 1 - 10^6 per 100 ml
    ax, yt2, yb2 = 176.0, 18.0, 150.0
    dec = (yb2 - yt2) / 6.0

    def Yl(v):
        return yb2 - dec * (math.log10(v) if v > 0 else 0.0)
    pg.lab(u"coliforms per 100 ml", ax - 12.0, 7.0, bold=True)
    for e in range(7):
        yy = Yl(10 ** e)
        pg.ln([(ax, yy), (W - 4.0, yy)], COL["faint"], 0.12)
        pg.lab(u"1" if e == 0 else (u"10" if e == 1 else u"10^{}".format(e)), ax - 1.6, yy + 0.95, colour=BK_INK2,
               align="R")
    pg.ln([(ax, yt2), (ax, yb2)], COL["ink2"], 0.25)
    lo, hi = COLIFORM[0][1], COLIFORM[0][2]
    pg.rc(ax + 3.0, Yl(hi), ax + 13.0, Yl(lo), fill=C["d2"])
    pg.lab(u"after a wetland: 10^{:.0f}-10^{:.0f} {{src:paraskevopoulos_2020}}".format(math.log10(lo), math.log10(hi)),
           ax + 16.0, (Yl(lo) + Yl(hi)) / 2.0 + 1.0, colour=C["d3"], bold=True)
    lim_b = COLIFORM[1][1]
    pg.ln([(ax, Yl(lim_b)), (W - 4.0, Yl(lim_b))], BK_ACC, 0.7)
    pg.lab(u"class B, orchards: below {:,.0f}".format(lim_b), ax + 16.0, Yl(lim_b) + 4.4, colour=BK_ACC, bold=True)
    pg.ln([(ax, yb2 - 0.5), (ax + 40.0, yb2 - 0.5)], BK_ACC, 1.0)
    pg.lab(u"class A, parks: 0 {src:reuse_classes_2010}", ax + 16.0, yb2 - 3.0, colour=BK_ACC, bold=True)
    res["cleaning"].update({"wetland_coliforms_per_100ml": [lo, hi], "class_b_limit": lim_b, "class_a_limit": 0})


# ---------------------------------------------------------------- C6: the S4 cut in each season
BK_SEASONS = [("c6_s1", "winter"), ("c6_s2", "spring"), ("c6_s3", "summer"), ("c6_s4", "autumn")]
BK_DROP_LAYERS = ("title", "levels", "callouts", "dimensions", "band", "survey", "text")


def bk_season(pg, res, key):
    E = detail_engine()
    W, H = pg.W, pg.H
    i = [s["key"] for s in E["SEASONS"]].index(key)
    sea = E["SEASONS"][i]
    prof = _DET_PROF[0] if _DET_PROF else (E["PROFILE_S0"], E["PROFILE_DS"], E["PROFILE_Z"])
    d = E["SECTIONS"][0]                                     # the south-west bank, the bed and the strip
    keep = (E["SCALE"], E["K"], dict(E["SEA"]))
    lay = {"poly": 6, "line": 5, "circle": 7}
    x0, y0, x1, y1 = 40.0, 2.0, W - 2.0, H - 2.0             # the cut's box (mm, y down); names at the left
    kk = 1.0                                                 # first pass at 1 mm per m, then as large as it fits
    try:
        E["SEA"].clear()
        E["SEA"].update(E["SEASON_LOOK"][key])
        for _ in range(2):
            E["K"] = kk
            E["SCALE"] = 1000.0 / kk
            tmp = E["Page"]("bk", key)
            E["draw_section"](tmp, E["Sec"](d, prof), 0.0, 0.0, [], sea)
            items = from_engine([it for it in tmp.items if it[0] in lay and it[lay[it[0]]] not in BK_DROP_LAYERS])
            bb = items_bbox(items)
            kk *= min((x1 - x0) / (bb[2] - bb[0]), (y1 - y0) / (bb[3] - bb[1])) * 0.995
    finally:
        E["SCALE"], E["K"] = keep[0], keep[1]
        E["SEA"].clear()
        E["SEA"].update(keep[2])
    s_ = min(1.0, (x1 - x0) / (bb[2] - bb[0]), (y1 - y0) / (bb[3] - bb[1]))
    dx = x0 - s_ * bb[0] + ((x1 - x0) - s_ * (bb[2] - bb[0])) / 2.0
    dy = (H - y1) - s_ * bb[1] + ((y1 - y0) - s_ * (bb[3] - bb[1])) / 2.0
    pg.items += xform(items, s_, dx, dy)
    pg.rc(0.0, 0.0, 34.0, 1.6, fill=BAND_BLUE[i])
    pg.lab(u"{} · {}".format(sea["name"], sea["months"].replace(u" ", u"")), 0.0, 8.5, size=BK_KEY, bold=True)
    pg.lab(u"S4 cut", 0.0, 13.5, colour=BK_INK2)
    res.setdefault("seasons", {})[key] = {"water_m_above_bed": [round(w[0] - E["THALWEG"][1], 2) for w in sea["water"]],
                                          "strip_held": sea["strip_held"]}


# ---------------------------------------------------------------- C8 a: where the clean water goes (pictograms)
def bk_farms(pg, res):
    W, H = pg.W, pg.H
    # row 1: the clean stream leaves the site for the farmland outside (the focal arrow)
    pg.pl([rect(4.0, 14.0, 66.0, 52.0)], stroke=BK_INK2, lw=0.3, dash=[1.4, 1.0])
    wave = [(6.0 + t * 0.5, 31.0 + 1.2 * math.sin(t * 0.5)) for t in range(0, 121)]
    pg.ln(wave, C["w3"], 1.6)
    pg.lab(u"no farm channel inside", 6.5, 48.5, colour=BK_INK2)
    arrow(pg, [(68.0, H - 31.0), (112.0, H - 31.0)], BK_ACC, 1.4, 5.0)
    pg.lab(u"clean stream leaves the site", 68.0, 26.0, colour=BK_ACC, bold=True)
    farm = draw_farm_picto("A")
    farm.items = [it for it in farm.items if it[0] not in ("text", "circle")]
    bb = items_bbox(farm.items)
    s_ = min((W - 118.0 - 3.0) / (bb[2] - bb[0]), 40.0 / (bb[3] - bb[1]))
    pg.items += xform(farm.items, s_, 118.0 - s_ * bb[0], (H - 52.0) - s_ * bb[1])
    pg.lab(u"farmland outside · route open", 118.0, 57.5, colour=MP["agriculture"][2], bold=True)
    # row 2: winter water into the alluvium, only if the boreholes allow it
    pg.ic("rain", 8.0, 66.0, 20.0)
    pg.rc(48.0, 82.0, 150.0, 104.0, fill=COL["soil"])
    r = _tree_rand(48.0, 82.0)
    for _ in range(140):
        pg.circle(48.5 + 101.0 * r(), H - (82.5 + 21.0 * r()), 0.25, fill=COL["soil_dk"])
    pg.ln([(48.0, 82.0), (150.0, 82.0)], COL["edge3d"], 0.3)
    arrow(pg, [(30.0, H - 76.0), (56.0, H - 76.0)], C["w3"], 0.8, 3.0)
    pg.ln([(56.0, 76.0), (126.0, 76.0)], C["w3"], 0.8, dash=[1.4, 0.9])
    for xx in (70.0, 98.0, 126.0):                          # dashed: only if the borehole tests accept it
        arrow(pg, [(xx, H - 76.0), (xx, H - 97.0)], C["w3"], 0.8, 3.0, dash=[1.4, 0.9])
    pg.lab(u"recharge, if tests accept", 153.0, 94.0, colour=C["d3"], bold=True)
    # row 3: the town's wastewater: treatment plant -> Bakırçay, not into the Selinos
    pg.ic("sewage", 8.0, 120.0, 20.0)
    arrow(pg, [(31.0, H - 130.0), (52.0, H - 130.0)], BK_INK2, 0.7, 2.6)
    pg.ic("plant", 55.0, 120.0, 20.0)
    arrow(pg, [(78.0, H - 130.0), (108.0, H - 130.0)], BK_INK2, 0.7, 2.6)
    pg.rc(110.0, 126.0, 190.0, 134.0, fill=C["w2"])
    pg.lab(u"treatment plant -> Bakırçay", 110.0, 140.5, colour=BK_INK)
    pg.ln([(65.0, 142.0), (65.0, 157.0)], BK_INK2, 0.5, dash=[1.2, 0.8])
    pg.pl([[(65.0, 158.5), (63.9, 156.0), (66.1, 156.0)]], fill=BK_INK2)
    pg.ln([(62.4, 147.2), (67.6, 152.4)], BK_ACC, 0.7)
    pg.ln([(62.4, 152.4), (67.6, 147.2)], BK_ACC, 0.7)
    pg.rc(30.0, 159.0, 100.0, 163.0, fill=C["w3"])
    pg.lab(u"not into the Selinos", 71.0, 151.0, colour=BK_ACC, bold=True)


# ---------------------------------------------------------------- the frames and their plan entries
BK_FRAMES = [
    ("b1_hero", bk_year, u"Oct -> Sep · mean year · natural flow, worst-case roughness", None,
     [("fill", C["w3"], u"Rain"), ("fill", C["structure"], u"Open-water evaporation"),
      ("fill", MP["discharge"][2], u"Stream flow, Dec-Apr"), ("fill", MP["discharge"][0], u"Stream flow, other months"),
      ("line", "3C5159", u"Mean depth in the bed")]),
    ("b1_side", bk_ndvi, u"Greener by the water every month {src:sentinel2} {src:clcplus}", None,
     [("line", "495338", u"Riparian strip"), ("line", COL["structure"], u"Rest of the site frame")]),
    ("b2_hero", bk_cuts, u"Depth above the bed · vertical x8 · looking upstream", 1500,
     [("fill", COL["structure"], u"Ground"), ("line", LEVEL_COL[1], u"Highest day 2016-2021"),
      ("line", LEVEL_COL[3], u"Q100"), ("line", LEVEL_COL[4], u"Q500"), ("fill", BK_ACC, u"Over the bank top")]),
    ("b4_side", bk_cubes, u"Cubes to scale 1:1,250 · edge = cube root of volume", 1250,
     [("fill", MP["storage"][1], u"Stored water, to scale")]),
    ("b5_strip", bk_chain, u"Our design: one way, with the stream", None,
     [("line", C["w3"], u"Water, one way")]),
    ("b5_hero", bk_cleaning, u"Reed beds clean, UV makes it safe to touch {src:vymazal_2010} {src:reuse_uv_2010}", None,
     []),                                                  # the three wetland types are labelled on the drawing
] + [(k_, (lambda s_: (lambda pg, res: bk_season(pg, res, s_)))(s_),
      u"{} on the downstream cut".format(s_.capitalize()), None, [("fill", BAND_BLUE[i_], s_)])
     for i_, (k_, s_) in enumerate(BK_SEASONS)] + [
    ("c8_a", bk_farms, u"Our design: farms outside, class B water", None,
     [("line", C["w3"], u"Clean stream water"), ("fill", MP["agriculture"][1], u"Farmland outside the site")])]


def booklet_export(folder, log):
    """Writes output/<folder>/booklet/: one text-free PDF per frame, blocks.json (labels, captions, legends) and
    results.json (the figures the drawings print). Problems go to the log; the sheets are already written."""
    bk = BkBlocks(folder, GH_LABEL, SHORT)
    res = {"script": GH_LABEL, "version": SHORT}
    for key, fn, cap, den, legend in BK_FRAMES:
        try:
            pg = BkPage(key)
            fn(pg, res)
            pg.finish()
            pg.items, labels = bk_take_text(pg.items, pg.H)
            for lb in labels:
                lb["size"] = round(lb["size"], 2)
            for p in bk_check(labels, pg.W, pg.H):
                log.append(u"booklet {}: {}".format(key, p))
            write_pdf(pg, bk.path(key + ".pdf"), u"Bergama water board {} booklet {}".format(SHORT, key))
            bk.drawing(key, key + ".pdf", labels, cap, den,
                       [{"kind": k_, "colour": c_, "label": l_} for k_, c_, l_ in legend])
        except Exception as ex:
            log.append(u"booklet {} not written: {}: {}".format(key, type(ex).__name__, ex))
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    bk.save()
