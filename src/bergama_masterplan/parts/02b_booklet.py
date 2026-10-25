
# ================================================================ v20: the A3 booklet assets (SCRIPT_STANDARD §8)
# Four drawings for the booklet (booklet/ASSET_SPEC.md), drawn natively at their frame's size, option A only, with
# no text in the PDFs: every word is a label in booklet/blocks.json (set as live text by the assembler).
#   c1_s1 / c1_s2  the whole site (site_alan) in two halves split at the Red Hall (BK_OVERLAP_M overlap), turned so
#                  the stream runs left to right, at 1:5,000 if it fits the frame, else the largest standard scale
#   c3_a / c3_b    north-up 1:1,000 windows (frame size in m): the upstream entry's cleaning and holding chain, and
#                  K5 with Demeter's Garden (1:1,250 when the window cannot hold the garden and the bridge)
# The same layers as the sheet (option A's freely grown zones at the opacity setting, the commons, the promenade,
# the streamside spine in E0B67D, walks, stops) over the survey's buildings (grey) and heritage (pale red). The
# area with no programme yet is plain ground (Aras 25 Oct 20:02). Booklet words: "stream", never "river", for the
# Selinos (Aras 20:02). Label sizes 7.5 pt, key labels 8.5 pt; label boxes never overlap or leave the frame.
BK_FRAMES = {"c1_s1": (392.0, 116.0), "c1_s2": (392.0, 116.0), "c3_a": (194.0, 176.0), "c3_b": (194.0, 176.0)}
BK_STD_SCALES = (1000.0, 1250.0, 2000.0, 2500.0, 5000.0, 10000.0, 20000.0)
BK_C1_SCALE = 5000.0                 # wanted scale of the whole-site halves
BK_WIN_SCALE = 1000.0                # the 1:1,000 windows
BK_OVERLAP_M = 50.0                  # the two halves share this much at the Red Hall
BK_LBL, BK_KEY = 7.5, 8.5            # pt: labels, key labels (zone names)
BK_GAP = 0.4                         # mm kept between label boxes
BK_INK, BK_INK2 = "4A3F35", "6B645B"  # booklet ink and caption ink (design-language.md)
BK_SPINE = "E0B67D"                  # the streamside spine on every frame (Aras 20:02: sand)
BK_PROGRAMME = {u"REED BASINS": [u"cleaning · de-odour · runoff"],      # the plan's keyword lines (SUBS, cut to 30
                u"RETENTION TERRACES": [u"winter rain · stepped · seats"],  # characters a line)
                u"SPILLWAY": [u"overflow · return"],
                u"SHADED WALK": [u"shade · walk · cafe"],
                u"BED": [u"water strip · stepping stones", u"weirs · plaza · reed"],
                u"FLOOD TERRACE": [u"water steps · seats · tamarix"],
                u"DRY TOP": [u"bridge view · kiosk · lavender"],
                u"DEMETER'S GARDEN": [u"olives · pine · aromatics", u"seasonal beds · cafe · basin"],
                RIVER_BAND_NAME: [u"viewpoints · terraces · ramps"]}
BK_C3 = {"c3_a": dict(area="calisma_alan[0]", names=(u"REED BASINS", u"RETENTION TERRACES", u"SPILLWAY",
                                                      u"SHADED WALK"), stops=(7,),
                      caption=u"Upstream entry: collect, clean, hold", bridge=u"K4"),
         "c3_b": dict(area="calisma_alan[1]", names=(u"BED", u"FLOOD TERRACE", u"DRY TOP", u"DEMETER'S GARDEN"),
                      stops=(5, 8), caption=u"K5 bridge and Demeter's Garden", bridge=u"K5")}
BK_WALK_VAL = u"{{val:bergama_masterplan/masterplan_results.json:options.A.walk_m_by_bank_and_class.{} bank|0}}"


def bk_word(s):
    """Booklet wording: the Selinos is a stream (Aras 25 Oct 20:02)."""
    return s.replace(u"RIVERSIDE", u"STREAMSIDE").replace(u"RIVER", u"STREAM").replace(u"riverside", u"streamside")


def bk_lum(c):
    v = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in hex_rgb(c)]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def bk_contrast(a, b):
    la, lb = sorted((bk_lum(a), bk_lum(b)))
    return (lb + 0.05) / (la + 0.05)


def bk_on(fill):
    """Label colour on a fill: white where it reads (WCAG 4.5:1), else the booklet ink."""
    return "FFFFFF" if bk_contrast("FFFFFF", fill) >= 4.5 else BK_INK


class BkBox(object):
    """A rectangle as the 'near' test of prep_base and Grid."""

    def __init__(self, R):
        self.R = R

    def inside(self, x, y):
        R = self.R
        return R[0] <= x <= R[2] and R[1] <= y <= R[3]

    within = inside


class BkFrame(object):
    """One booklet drawing: the page (y up), its labels (top-left, y down to the baseline) and its legend."""

    def __init__(self, W, H, F, k):
        self.W, self.H, self.F, self.k = W, H, F, k
        self.pg = Page(W, H)
        self.labels, self.boxes, self.avoid, self.legend, self.missing = [], [], [], [], []

    def T(self, P):
        return [self.F(p) for p in P]

    def tl(self, p):
        x, y = self.F(p)
        return x, self.H - y

    def leg(self, kind, colour, label):
        if all(e["label"] != label for e in self.legend):
            self.legend.append({"kind": kind, "colour": colour, "label": label})

    def lbox(self, s, x, yb, size, bold, anchor):
        w = text_w(s, size * PT, bold)
        x0 = x - (w / 2 if anchor == "C" else w if anchor == "R" else 0.0)
        m = size * PT
        return (x0, yb - 0.72 * m, x0 + w, yb + 0.21 * m)

    def free(self, b, gap=BK_GAP):
        if b[0] < 0.3 or b[1] < 0.3 or b[2] > self.W - 0.3 or b[3] > self.H - 0.3:
            return False
        return not any(hit(b, o, gap) for o in self.boxes + self.avoid)

    def put(self, text, x, yb, size=BK_LBL, bold=False, anchor="L", colour=BK_INK, shown=None):
        """One label (shown = the text as it will print, for its width: a {val:} mark resolved)."""
        self.boxes.append(self.lbox(shown or text, x, yb, size, bold, anchor))
        self.labels.append({"x": round(x, 2), "y": round(yb, 2), "text": text, "size": size, "bold": bool(bold),
                            "anchor": anchor, "colour": colour})

    def block_dims(self, lines):
        """lines [(text, size, bold, shown)] -> (w, h, [baseline offsets from the block top])."""
        w, y, base = 0.0, 0.0, []
        for i, (s, sz, bd, sh) in enumerate(lines):
            m = sz * PT
            y += 0.72 * m if i == 0 else 1.18 * m
            base.append(y)
            w = max(w, text_w(sh or s, m, bd))
        return w, y + 0.21 * lines[-1][1] * PT, base

    def put_block(self, lines, x0, y0, colour):
        w, h, base = self.block_dims(lines)
        for (s, sz, bd, sh), yb in zip(lines, base):
            self.put(s, x0, y0 + yb, sz, bd, "L", colour, sh)

    def place(self, lines, anchor, colour=BK_INK, inside=None, min_d=2.0, max_d=60.0, leader=True,
              fill_colour=None):
        """A label block next to anchor (top-left mm): inside ring `inside` (top-left mm) when it fits there, else
        on a free spot round the anchor with a leader. Returns the box or None."""
        w, h, base = self.block_dims(lines)
        if inside:
            ring_ = thin(inside, 300)
            for x, y in inside_spots(ring_, 22)[:220]:
                b = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
                if self.free(b) and box_in(ring_, (b[0] - 0.6, b[1] - 0.6, b[2] + 0.6, b[3] + 0.6)):
                    self.put_block(lines, b[0], b[1], bk_on(fill_colour) if fill_colour else colour)
                    return b
        ax, ay = anchor
        for d in [0.0] * (min_d <= 0) + [min_d, min_d + 2, min_d + 4, min_d + 7, min_d + 11, min_d + 16, 24, 32, 42,
                                         max_d]:
            if d > max_d:
                break
            for i in range(24):
                a = math.radians(i * 15.0 + 7.5) if d > 0 else 0.0
                cx = ax + math.cos(a) * (d + w / 2)
                cy = ay - math.sin(a) * (d + h / 2)
                b = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
                if not self.free(b):
                    continue
                self.put_block(lines, b[0], b[1], colour)
                if leader and d > 0:
                    qx, qy = min(max(ax, b[0]), b[2]), min(max(ay, b[1]), b[3])
                    if math.hypot(qx - ax, qy - ay) > 1.2:
                        self.pg.line([(ax, self.H - ay), (qx, self.H - qy)], BK_INK2, 0.15)
                        self.pg.circle(ax, self.H - ay, 0.45, fill=BK_INK2)
                return b
        self.missing.append(lines[0][0] + u" (no free spot)")
        return None


def bk_scale(span_w, span_h, W, H, want):
    """The wanted scale if the span (m) fits W x H mm, else the largest standard scale that does."""
    for s in [want] + [s_ for s_ in BK_STD_SCALES if s_ > want]:
        if span_w * 1000.0 / s <= W and span_h * 1000.0 / s <= H:
            return s
    return BK_STD_SCALES[-1]


def bk_anchors(BK):
    """Named places (world m): the bridges K4, K3, K5 and the Red Hall are city link's surveyed spine anchors (K4 =
    piece A's start, K3 its end, Red Hall = piece C's start, K5 its end); K6 lies city link's K5-K6 chainage downstream
    of K5 on the stream line. Each bridge snaps to the nearest surveyed bridge (YOL_KOPRU) within 60 m."""
    spec, CL = BK["spec"], BK["CL"]
    sp = dict((pc.get("id"), pc) for pc in spec.get("spine", []))
    out = {}
    for nm, (pid, end) in ((u"K4", ("A", "frm")), (u"K3", ("A", "to")), (u"RED HALL", ("C", "frm")),
                           (u"K5", ("C", "to"))):
        if pid in sp and sp[pid].get(end):
            out[nm] = tuple(sp[pid][end])
    ref = CL["W"]["ref"]
    s = arclen(ref)
    ch = spec.get("chainage") or {}
    if u"K5" in out and "K5" in ch and "K6" in ch:
        c5, _ = chain_at(ref, out[u"K5"])
        out[u"K6"], _ = at_len(ref, s, c5 + float(ch["K6"]) - float(ch["K5"]))
    mids = [((B[0][0] + B[-1][0]) / 2.0, (B[0][1] + B[-1][1]) / 2.0) for B in BK["survey"].get("bridge", [])]
    for nm in (u"K4", u"K3", u"K5", u"K6"):
        if nm in out and mids:
            m = min(mids, key=lambda q: math.hypot(q[0] - out[nm][0], q[1] - out[nm][1]))
            if math.hypot(m[0] - out[nm][0], m[1] - out[nm][1]) <= 60.0:
                out[nm] = m
    return out


def bk_seen(P, cb, ring_=True):
    """Page polyline / ring P shows inside the page rectangle cb (x0, y0, x1, y1)."""
    if any(cb[0] <= x <= cb[2] and cb[1] <= y <= cb[3] for x, y in P):
        return True
    if not ring_ or len(P) < 3:
        return False
    pb = bbox(P)
    if not hit(pb, cb):
        return False
    return any(pip(cb[0] + (cb[2] - cb[0]) * i / 4.0, cb[1] + (cb[3] - cb[1]) * j / 4.0, P)
               for i in range(5) for j in range(5))


def bk_layers(fr, BK, base, keys, RB, SP, clip, fine):
    """The drawing of one frame (no words): survey context, zones, commons, promenade, spine, stream, bridges,
    walks; only what shows in the frame (and only that in its legend). fine = the 1:1,000 windows (line weights of
    the sheet), else the 1:5,000 halves (lighter)."""
    pg, W_ = fr.pg, COL["white"]
    alpha = BK["alpha"]
    cb = bbox(clip)
    T = lambda P: fr.T(P)
    seen_rings = lambda loops: [R_ for R_ in (T(L_) for L_ in loops) if bk_seen(R_, cb)]
    seen_lines = lambda P: bk_seen(P, cb, False)
    pg.poly([clip], fill=W_)
    pg.clip([clip])
    fc = base["faces"]
    rings = seen_rings([F_ for role in ("building", "housing") for F_ in fc.get(role, [])])
    if rings:
        pg.poly(rings, fill=COL["bld"])
        fr.leg("fill", COL["bld"], u"building")
    rings = seen_rings(fc.get("heritage", []))
    if rings:
        pg.poly(rings, fill=COL["her"], stroke=COL["her_edge"], lw=0.1)
        fr.leg("fill", COL["her"], u"heritage building")
    pz = [pc for key in keys for pc in BK["pzs"].get(key, [])]
    free = [(pc, seen_rings(pc["loops"])) for pc in pz if pc["kind"] == "free"]
    free = [(pc, R_) for pc, R_ in free if R_]
    hubs = [(pc, seen_rings(pc["loops"])) for pc in pz if pc["kind"] == "hub"]
    hubs = [(pc, R_) for pc, R_ in hubs if R_]
    RBs = seen_rings(RB or [])
    SPs = seen_rings(SP or [])
    for pc, R_ in free:
        pg.poly(R_, fill=W_, stroke=W_, lw=0.3 if fine else 0.15)
    if RBs:
        lt, md, dk = RIVER_BAND_TONE
        s_ = 0.8 if fine else 0.3
        pg.poly([[(x + s_, y - s_) for x, y in L_] for L_ in RBs], fill=dk, alpha=0.22)
        pg.poly(RBs, fill=lt, alpha=0.85)
        pg.poly(RBs, stroke=dk, lw=0.35 if fine else 0.15)
        fr.leg("fill", mix(W_, lt, 0.85), RIVER_BAND_NAME.lower())
    for pc, R_ in free:
        pg.poly(R_, fill=zone_tones(pc["zone"])[0], alpha=alpha)
    for pc, R_ in free:
        fr.leg("fill", mix(W_, zone_tones(pc["zone"])[0], alpha), bk_zone_legend(pc["zone"]))
    for pc, R_ in hubs:
        pg.poly(R_, fill=piece_tone(pc)[0], stroke=W_, lw=0.3 if fine else 0.15)
        fr.leg("fill", piece_tone(pc)[0], u"commons")
    if SPs:
        pg.poly(SPs, fill=BK_SPINE)
        fr.leg("fill", BK_SPINE, u"streamside spine")
    for P in base["streams"]:
        P = T(P)
        if seen_lines(P):
            pg.line(P, COL["river_mid"], 0.22 if fine else 0.12)
    for s_ in BK["D"].strips:
        P = T(s_["P"])
        if bk_seen(P, cb):
            pg.poly([P], fill=COL["river"], stroke=COL["river_dark"], lw=0.2 if fine else 0.1)
            fr.leg("fill", COL["river"], u"water strip")
    for ck, lw, dash, P in base["lines"]:
        P = T(P)
        if ck == "ink" and seen_lines(P):                  # bridges
            pg.line(P, COL["ink"], 0.35 if fine else 0.25)
    ref = BK["CL"]["W"]["ref"]
    for s0, s1 in BK["covered"]:
        P = T(ref_between(ref, s0, s1))
        if seen_lines(P):
            pg.line(P, COL["river_dark"], 0.5 if fine else 0.3, [1.2, 0.8], cap=0)
            fr.leg("line", COL["river_dark"], u"stream, covered reach")
    for x in BK["CL"]["W"]["runs"]:
        P = T(x["F"])
        if not seen_lines(P):
            continue
        pg.line(P, W_, 1.5 if fine else 0.7)
        if x["cls"] == "bank":
            pg.line(P, COL["walk"], 0.7 if fine else 0.35)
            fr.leg("line", COL["walk"], u"bank walk, car-free")
        elif x["cls"] == "street":
            pg.line(P, COL["walk"], 0.7 if fine else 0.35, [2.2, 0.8] if fine else [1.2, 0.5], cap=0)
            fr.leg("line", COL["walk"], u"street walk")
        else:
            pg.line(P, COL["river_dark"], 0.7 if fine else 0.35, [0.5, 0.6] if fine else [0.35, 0.4], cap=0)
            fr.leg("line", COL["river_dark"], u"bed walk, closed in floods")
    pg.unclip()


def bk_zone_legend(z):
    if z["code"] == "WA":
        return u"flood terrace" if z["tier"] == "F" else u"bed"
    nm = bk_word(name_of(z, z.get("own", "")))
    return {u"SHADED WALK": u"dry top, shaded walk", u"DRY TOP": u"dry top, shaded walk",
            u"DEMETER'S GARDEN": u"Demeter's Garden"}.get(nm, nm.lower())


def bk_stops(fr, BK, want, r, inside):
    """Stops as numbered accent dots (the number is a label)."""
    for n, nm, xy, how in BK["CL"]["stops"]:
        if want is not None and n not in want:
            continue
        x, y = fr.F(xy)
        if not inside(x, y):
            continue
        fr.pg.circle(x, y, r + 0.35, fill=COL["white"])
        fr.pg.circle(x, y, r, fill=COL["accent"])
        fr.leg("dot", COL["accent"], u"stop")
        yt = fr.H - y
        fr.put(str(n), x, yt + 0.255 * BK_LBL * PT, BK_LBL, True, "C", "FFFFFF")
        fr.avoid.append((x - r - 0.2, yt - r - 0.2, x + r + 0.2, yt + r + 0.2))


def bk_north(fr, x, y, ang):
    """North arrow at (x, y) page mm (y up), pointing at angle ang (rad, from page +x); 'N' is a label."""
    L = 7.0
    dx, dy = math.cos(ang), math.sin(ang)
    tip = (x + dx * L / 2, y + dy * L / 2)
    tail = (x - dx * L / 2, y - dy * L / 2)
    nx, ny = -dy, dx
    fr.pg.poly([[tip, (tail[0] + nx * 1.6, tail[1] + ny * 1.6), (x - dx * 1.2, y - dy * 1.2)]], fill=COL["ink_dark"])
    fr.pg.poly([[tip, (x - dx * 1.2, y - dy * 1.2), (tail[0] - nx * 1.6, tail[1] - ny * 1.6)]], fill=COL["white"],
               stroke=COL["ink_dark"], lw=0.15)
    lx, ly = tip[0] + dx * 2.6, fr.H - (tip[1] + dy * 2.6)
    fr.put(u"N", lx, ly + 0.255 * BK_LBL * PT, BK_LBL, True, "C", BK_INK)
    fr.avoid.append((min(tip[0], tail[0]) - 1.8, fr.H - max(tip[1], tail[1]) - 1.8,
                     max(tip[0], tail[0]) + 1.8, fr.H - min(tip[1], tail[1]) + 1.8))


def bk_scale_bar(fr, x, y, scale, marks):
    """Scale bar at (x, y) page mm (left end, y up): ink and white blocks; its numbers are labels below it."""
    k = 1000.0 / scale
    for i, (a, b) in enumerate(zip(marks[:-1], marks[1:])):
        fr.pg.poly([rect(x + a * k, y, x + b * k, y + 1.0)], fill=COL["ink_dark"] if i % 2 == 0 else COL["white"],
                   stroke=COL["ink_dark"], lw=0.12)
    yb = fr.H - y + 3.4
    for i, m_ in enumerate(marks):
        num = u"{:,.0f}".format(m_)
        if i == len(marks) - 1:                          # the unit after the last number, the number on its tick
            fr.put(num + u" m", x + m_ * k - text_w(num, BK_LBL * PT) / 2.0, yb, BK_LBL, False, "L", BK_INK)
        else:
            fr.put(num, x + m_ * k, yb, BK_LBL, False, "C", BK_INK)
    fr.avoid.append((x - 1.0, fr.H - y - 2.0, x + marks[-1] * k + 1.0, fr.H - y + 0.5))


def bk_context(BK):
    """Shared data of the four frames: whole-site base and bands, the covered reach, named places."""
    P, cov = stream_ref()
    sP = arclen(P)
    runs, a = [], None
    for i, c in enumerate(cov):
        if c and (i == 0 or not cov[i - 1]):
            a = sP[i]
        if c and (i == len(cov) - 1 or not cov[i + 1]):
            runs.append((a, sP[i + 1]))
    BK["covered"] = [max(runs, key=lambda r_: r_[1] - r_[0])] if runs else []
    BK["places"] = bk_anchors(BK)


def booklet_export(folder, BK):
    """v20: the four booklet drawings (option A) + booklet/blocks.json + booklet/results.json."""
    bk = BkBlocks(folder, u"MasterPlan", SHORT)
    bk_context(BK)
    V0 = View(BK["areas"], 0.0, 1.0, frame=BK["site"])      # the sheet's whole-site view, 1 m = 1 unit
    site_W, site_H = V0.W, V0.H
    places = BK["places"]
    u_rh = V0.T(places[u"RED HALL"])[0] if u"RED HALL" in places else site_W / 2.0
    halves = {"c1_s1": (0.0, min(site_W, u_rh + BK_OVERLAP_M / 2.0)),
              "c1_s2": (max(0.0, u_rh - BK_OVERLAP_M / 2.0), site_W)}
    Wc, Hc = bk_frame("bergama_masterplan/c1_s1", *BK_FRAMES["c1_s1"])
    scale1 = bk_scale(max(b - a for a, b in halves.values()), site_H, Wc, Hc, BK_C1_SCALE)
    res = {"script": "bergama_masterplan_v20.py", "version": VERSION, "option": "A", "frames": {}}
    # ---- whole-site base and broad zones (the sheet's growth, on one corridor-wide grid)
    baseS = prep_base(BK["survey"], V0, V0.bb, full=True)
    G = Grid(V0.bb, V0, BAND_CELLS)
    RB_S = grow_band(G, baseS["streams"] + baseS["banks"], [s_["P"] for s_ in BK["D"].strips], RIVER_BAND_M, 101, "A")
    SP_S = grow_band(G, [s_["F"] for s_ in BK["CL"]["spine"]], [], SPINE_ZONE_M, 103, "A")
    # ---- the two 1:1,000 windows (chosen first: the halves outline them)
    wins = {}
    for bid in ("c3_a", "c3_b"):
        Ww, Hw = bk_frame("bergama_masterplan/" + bid, *BK_FRAMES[bid])
        wins[bid] = bk_window(BK, bid, Ww, Hw)
    # ---- C1: the halves
    for bid in ("c1_s1", "c1_s2"):
        W, H = bk_frame("bergama_masterplan/" + bid, *BK_FRAMES[bid])
        k = 1000.0 / scale1
        u0, u1 = halves[bid]
        dw, dh = (u1 - u0) * k, site_H * k
        x0 = W - dw if bid == "c1_s1" else 0.0                # s1 ends at the right edge, s2 starts at the left
        y0 = (H - dh) / 2.0

        def F(p, u0=u0, x0=x0, y0=y0, k=k):
            u, v = V0.T(p)
            return x0 + (u - u0) * k, y0 + v * k
        fr = BkFrame(W, H, F, k)
        clip = rect(x0, y0, x0 + dw, y0 + dh)
        bk_layers(fr, BK, baseS, ("calisma_alan[0]", "calisma_alan[1]"), RB_S, SP_S, clip, False)
        for wid, w_ in wins.items():                          # the 1:1,000 windows, outlined
            pts = [fr.F(p) for p in w_["corners"]]
            if all(x0 - 0.5 <= x <= x0 + dw + 0.5 for x, y in pts):
                fr.pg.poly([pts], stroke=COL["accent"], lw=0.25)
                w_["on"] = (bid, pts)
        ins = lambda x, y: x0 <= x <= x0 + dw and y0 <= y <= y0 + dh
        bk_stops(fr, BK, None, 1.9, ins)
        ang = math.atan2(V0.uv((0.0, 1.0))[1] - V0.uv((0.0, 0.0))[1], V0.uv((0.0, 1.0))[0] - V0.uv((0.0, 0.0))[0])
        if bid == "c1_s1":
            bk_north(fr, x0 - 8.0, y0 + dh - 9.0, ang)
            bk_scale_bar(fr, x0 - 6.0 - 250.0 * k, y0 + 6.0, scale1, (0.0, 50.0, 100.0, 250.0))
        else:
            bk_north(fr, x0 + dw + (W - x0 - dw) / 2.0, y0 + dh - 9.0, ang)
            bk_scale_bar(fr, W - 9.0 - 100.0 * k, y0 + 6.0, scale1, (0.0, 50.0, 100.0))
        bk_c1_words(fr, BK, bid, wins, (x0, H - y0 - dh, x0 + dw, H - y0))
        name = bid + ".pdf"
        write_pdf(fr.pg, bk.path(name), u"Bergama masterplan booklet " + bid)
        bk.drawing(bid, name, fr.labels, caption=u"Whole site, " + (u"upstream" if bid == "c1_s1" else u"downstream")
                   + u" half", scale_den=scale1, legend=fr.legend)
        res.setdefault("labels_not_drawn", {})[bid] = fr.missing
        res["frames"][bid] = {"scale_den": scale1, "w_mm": W, "h_mm": H, "from_m": round(u0, 1), "to_m": round(u1, 1),
                              "overlap_m": BK_OVERLAP_M}
    # ---- C3: the windows
    for bid in ("c3_a", "c3_b"):
        w_ = wins[bid]
        W, H, sc_, R = w_["W"], w_["H"], w_["scale"], w_["R"]
        k = 1000.0 / sc_

        def F(p, R=R, k=k):
            return (p[0] - R[0]) * k, (p[1] - R[1]) * k
        fr = BkFrame(W, H, F, k)
        Rm = (R[0] - 40.0, R[1] - 40.0, R[2] + 40.0, R[3] + 40.0)
        nr = BkBox(Rm)
        base = prep_base(BK["survey"], nr, Rm, full=True)
        Gw = Grid(Rm, nr, BAND_CELLS)
        RB = grow_band(Gw, base["streams"] + base["banks"], [s_["P"] for s_ in BK["D"].strips], RIVER_BAND_M, 101, "A")
        SP = grow_band(Gw, [s_["F"] for s_ in BK["CL"]["spine"]], [], SPINE_ZONE_M, 103, "A")
        bk_layers(fr, BK, base, ("calisma_alan[0]", "calisma_alan[1]"), RB, SP, rect(0.0, 0.0, W, H), True)
        if bid == "c3_a":
            bk_arrows(fr, BK)
        bk_stops(fr, BK, BK_C3[bid]["stops"], 2.3, lambda x, y: 0 <= x <= W and 0 <= y <= H)
        bk_north(fr, W - 6.0, H - 8.0, math.pi / 2.0)
        bk_scale_bar(fr, W - 6.0 - 50.0 * k, 5.0, sc_, (0.0, 10.0, 20.0, 50.0))
        bk_c3_words(fr, BK, bid, RB)
        name = bid + ".pdf"
        write_pdf(fr.pg, bk.path(name), u"Bergama masterplan booklet " + bid)
        bk.drawing(bid, name, fr.labels, caption=BK_C3[bid]["caption"], scale_den=sc_, legend=fr.legend)
        res.setdefault("labels_not_drawn", {})[bid] = fr.missing
        res["frames"][bid] = {"scale_den": sc_, "w_mm": W, "h_mm": H, "centre_xy": [round((R[0] + R[2]) / 2, 1),
                              round((R[1] + R[3]) / 2, 1)], "window_m": [round(R[2] - R[0], 1), round(R[3] - R[1], 1)]}
    res["places_xy"] = dict((k_, [round(v[0], 1), round(v[1], 1)]) for k_, v in sorted(places.items()))
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return bk.save()


def bk_window(BK, bid, W, H):
    """The north-up window of a C3 frame: centred on what it shows (c3_a: the reed basins, retention terraces,
    spillway and the commons of the upstream entry; c3_b: the K5 bridge, moved just enough to hold Demeter's
    Garden), at 1:1,000, else 1:1,250 when the garden and the bridge do not fit together."""
    spec = BK_C3[bid]
    zs = [z for z in BK["D"].zones if z["area"] == spec["area"]]
    if bid == "c3_a":
        pts = [p for z in zs if name_of(z, z.get("own", "")) in spec["names"] for p in z["P"]]
        if not pts:
            pts = [p for z in zs for p in z["P"]]
        b = bbox(pts)
        c = ((b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0)
        sc_ = BK_WIN_SCALE
    else:
        k5 = BK["places"].get(u"K5")
        dg = [p for z in zs if z["code"] == "DG" for p in z["P"]]
        c, sc_ = k5 or inner_pt(BK["areas"][spec["area"]]), BK_WIN_SCALE
        if dg and k5:
            b = bbox(dg + [k5])
            for s_ in (BK_WIN_SCALE, 1250.0):
                ww, hh = W * s_ / 1000.0, H * s_ / 1000.0
                if b[2] - b[0] <= ww - 20.0 and b[3] - b[1] <= hh - 20.0:
                    sc_ = s_
                    cx = min(max(k5[0], b[2] - ww / 2 + 10.0), b[0] + ww / 2 - 10.0)
                    cy = min(max(k5[1], b[3] - hh / 2 + 10.0), b[1] + hh / 2 - 10.0)
                    c = (cx, cy)
                    break
    ww, hh = W * sc_ / 1000.0, H * sc_ / 1000.0
    R = (c[0] - ww / 2, c[1] - hh / 2, c[0] + ww / 2, c[1] + hh / 2)
    return {"W": W, "H": H, "scale": sc_, "R": R, "corners": [(R[0], R[1]), (R[2], R[1]), (R[2], R[3]), (R[0], R[3])]}


def bk_arrows(fr, BK):
    """The water links of the zone base (collect, clean, hold, return) as the sheet's bold hand arrows."""
    for i, L in enumerate(BK["D"].links):
        if L["kind"] != "water":
            continue
        P = fr.T(L["P"])
        if not any(0 <= x <= fr.W and 0 <= y <= fr.H for x, y in P):
            continue
        fr.pg.clip([rect(0.0, 0.0, fr.W, fr.H)])
        link_arrow(fr.pg, P, "water", L["heads"], 3 + i)
        fr.pg.unclip()
        fr.leg("line", link_cols("water")[0], u"water moves (arrow)")
        Pt = [(x, fr.H - y) for x, y in P]
        for a, b in zip(Pt, Pt[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / 2.0))
            for j in range(n + 1):
                x, y = a[0] + (b[0] - a[0]) * j / n, a[1] + (b[1] - a[1]) * j / n
                fr.avoid.append((x - 1.2, y - 1.2, x + 1.2, y + 1.2))


def bk_ring_tl(fr, L_):
    return [(x, fr.H - y) for x, y in fr.T(L_)]


def bk_best(fr, loops, cb):
    """Of world rings, the one showing most inside cb (top-left mm), cut to cb; None when none shows."""
    best, ba = None, 20.0
    for L_ in loops:
        R_ = bk_clip_ring(bk_ring_tl(fr, L_), cb)
        if len(R_) >= 3 and abs(area2(R_)) > ba:
            best, ba = R_, abs(area2(R_))
    return best


def bk_zone_loops(BK, z):
    """The zone's free-piece rings (world m), else its own outline."""
    for key in ("calisma_alan[0]", "calisma_alan[1]"):
        for pc in BK["pzs"].get(key, []):
            if pc["kind"] == "free" and pc["zone"] is z:
                return pc["loops"]
    return [z["P"]]


def bk_clip_ring(R, cb):
    """A ring cut to the rectangle cb = (x0, y0, x1, y1) (Sutherland-Hodgman on the four sides)."""
    def cut(P, inside, inter):
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            if inside(b):
                if not inside(a):
                    out.append(inter(a, b))
                out.append(b)
            elif inside(a):
                out.append(inter(a, b))
        return out
    P = list(R)
    for ax, lim, keep_lo in ((0, cb[0], False), (0, cb[2], True), (1, cb[1], False), (1, cb[3], True)):
        if not P:
            break

        def inside(p, ax=ax, lim=lim, keep_lo=keep_lo):
            return p[ax] <= lim if keep_lo else p[ax] >= lim

        def inter(a, b, ax=ax, lim=lim):
            t = (lim - a[ax]) / ((b[ax] - a[ax]) or 1e-12)
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        P = cut(P, inside, inter)
    return P


def bk_c1_words(fr, BK, bid, wins, cb):
    """The words of a whole-site half (plan C1): places, bridges, the commons, the spine, a walk length, the
    window of page C3, 'continues'. Each sits next to its place, with a leader where it cannot. cb = the drawn
    rectangle (top-left mm)."""
    places, ref = BK["places"], BK["CL"]["W"]["ref"]

    def at(p):
        x, y = fr.tl(p)
        return (x, y) if cb[0] <= x <= cb[2] and cb[1] <= y <= cb[3] else None

    def one(text, p, bold=True, colour=BK_INK, shown=None, inside=None, fill=None):
        a = at(p) if p is not None else None
        if a is None:
            fr.missing.append(text + u" (not in this half)")
            return None
        return fr.place([(text, BK_LBL, bold, shown)], a, colour, inside=inside, min_d=1.5, fill_colour=fill)
    pin = [p for p in ref if at(p)]
    if bid == "c1_s1":
        one(u"UPSTREAM ENTRY", pin[0] if pin else None)
        for nm in (u"K4", u"K3"):
            one(nm, places.get(nm))
    else:
        one(u"DOWNSTREAM END", pin[-1] if pin else None)
        one(u"K5 ÜÇ KEMER", places.get(u"K5"))
        one(u"K6", places.get(u"K6"))
    one(u"RED HALL", places.get(u"RED HALL"))
    if bid == "c1_s1" and BK["covered"]:
        s0, s1 = BK["covered"][0]
        q, _ = at_len(ref, arclen(ref), (s0 + s1) / 2.0)
        one(u"COVERED REACH", q)
    key = "calisma_alan[0]" if bid == "c1_s1" else "calisma_alan[1]"
    for pc in BK["pzs"].get(key, []):
        if pc["kind"] == "hub":
            R_ = bk_best(fr, pc["loops"], cb)
            if R_:
                fr.place([(bk_word(pc["name"]), BK_LBL, True, None)], inner_pt(R_), BK_INK, inside=R_, min_d=1.5,
                         fill_colour=piece_tone(pc)[0])
            break
    if bid == "c1_s2":
        for code, nm in (("DG", u"DEMETER'S GARDEN"), ("WP", u"STREAMSIDE PLANTING")):
            zs = [z for z in BK["D"].zones if z["code"] == code]
            R_ = bk_best(fr, [L_ for z in zs for L_ in bk_zone_loops(BK, z)], cb)
            if R_:
                fr.place([(nm, BK_LBL, True, None)], inner_pt(R_), zone_tones(zs[0])[2], inside=R_, min_d=1.5)
    else:
        edge = [s_ for s_ in BK["CL"]["spine"] if s_["kind"] == "edge" and any(at(p) for p in s_["F"])]
        if edge:
            s_ = max(edge, key=lambda e: arclen(e["F"])[-1])
            q, _ = at_len(s_["F"], arclen(s_["F"]), arclen(s_["F"])[-1] / 2.0)
            one(u"STREAMSIDE SPINE", q, colour=MP["centre"][2])
    bank = "NE" if bid == "c1_s1" else "SW"
    runs = [x for x in BK["CL"]["W"]["runs"] if x["bank"] == bank and x["cls"] == "bank"
            and sum(1 for p in x["F"] if at(p)) > len(x["F"]) / 2]
    if runs:
        x = max(runs, key=lambda r_: r_["m"])
        q, _ = at_len(x["F"], arclen(x["F"]), arclen(x["F"])[-1] / 2.0)
        m_ = BK["CL"]["W"]["stats"].get(bank + " bank", 0.0)
        one(bank + u" bank walk " + BK_WALK_VAL.format(bank) + u" m", q, bold=False,
            shown=u"{} bank walk {:,.0f} m".format(bank, m_), colour=COL["walk"])
    for wid, w_ in sorted(wins.items()):
        if w_.get("on", (None,))[0] != bid:
            continue
        pts = [(x, fr.H - y) for x, y in w_["on"][1]]
        c = (sum(p[0] for p in pts) / 4.0, min(p[1] for p in pts))
        fr.place([(u"1:{:,.0f} window, page C3".format(w_["scale"]), BK_LBL, False, None)], c, COL["accent"],
                 min_d=1.0)
    yc = (cb[1] + cb[3]) / 2.0
    fr.place([(u"continues", BK_LBL, False, None)], (cb[2] if bid == "c1_s1" else cb[0], yc), BK_INK2, min_d=1.0,
             leader=False)


def bk_c3_words(fr, BK, bid, RB):
    """The words of a 1:1,000 window (plan C3): zone names with their keyword lines on the fills (a leader where a
    block does not fit its fill), the commons, the promenade, the bridge."""
    spec = BK_C3[bid]
    W, H = fr.W, fr.H
    cb = (0.0, 0.0, W, H)
    br = BK["places"].get(spec["bridge"])
    x, y = fr.tl(br) if br else (-1.0, -1.0)
    if 0 <= x <= W and 0 <= y <= H:
        fr.place([(spec["bridge"] + u" BRIDGE", BK_LBL, True, None)], (x, y), BK_INK, min_d=2.0)
    else:
        fr.missing.append(spec["bridge"] + u" BRIDGE (outside the window)")
    key = spec["area"]
    for pc in BK["pzs"].get(key, []):
        if pc["kind"] == "hub":
            R_ = bk_best(fr, pc["loops"], cb)
            if R_:
                fr.place([(bk_word(pc["name"]), BK_KEY, True, None)], inner_pt(R_), BK_INK, inside=R_,
                         fill_colour=piece_tone(pc)[0], min_d=2.0)
            else:
                fr.missing.append(bk_word(pc["name"]) + u" (outside the window)")
    for nm in spec["names"]:
        zs = [z for z in BK["D"].zones if z["area"] == key and bk_word(name_of(z, z.get("own", ""))) == nm]
        R_ = bk_best(fr, [L_ for z in zs for L_ in bk_zone_loops(BK, z)], cb)
        if not R_:
            fr.missing.append(nm + u" (outside the window)")
            continue
        lines = [(nm, BK_KEY, True, None)] + [(s_, BK_LBL, False, None) for s_ in BK_PROGRAMME.get(nm, [])]
        fr.place(lines, inner_pt(R_), zone_tones(zs[0])[2], inside=R_, min_d=2.0)
    R_ = bk_best(fr, RB or [], cb)
    if R_:
        lines = [(RIVER_BAND_NAME, BK_KEY, True, None)] + [(s_, BK_LBL, False, None)
                                                            for s_ in BK_PROGRAMME[RIVER_BAND_NAME]]
        fr.place(lines, inner_pt(R_), RIVER_BAND_TONE[2], inside=R_, min_d=2.0)
