# ============================================================ v39: A3 BOOKLET ASSETS (SCRIPT_STANDARD §8, booklet/ASSET_SPEC.md)
# Every booklet frame of this script (asset keys "selinus_board/<block>") as one text-free vector PDF drawn at the
# frame's size, its words as labels in blocks.json (the assembler sets them as live text), and the figures the board
# computes in booklet/results.json. Reuses the board's own drawings (BOARD items) and analyses (S, S.env); the board's
# PDFs, maps and log stay exactly as they were.
BK_SCRIPT = "MainBoard"
BK_VERSION = "v39"
BK_SLOTS = {                                          # booklet_slots.json of the project's booklet/ (w, h mm incl. caption)
    "a1_hero": (293.0, 236.0), "a1_side2": (95.0, 116.0), "a2_hero": (392.0, 236.0), "a3_hero": (260.0, 176.0),
    "a3_side1": (128.0, 56.0), "a3_side2": (128.0, 56.0), "a3_side3": (128.0, 56.0), "a4_s2": (392.0, 56.0),
    "a4_s3": (392.0, 56.0), "a5_s1": (293.0, 56.0), "a5_s2": (293.0, 56.0), "a5_s3": (293.0, 56.0),
    "a5_s4": (293.0, 56.0), "a6_s1": (293.0, 56.0), "a6_s2": (293.0, 56.0), "a6_s3": (293.0, 56.0),
    "a6_s4": (293.0, 56.0), "a7_hero": (260.0, 176.0), "a7_side1": (128.0, 86.0)}
BK_PT = 25.4 / 72.0                                   # mm per point
BK_LAB = 7.5                                          # label size (pt); key labels up to 9.5
BK_INK, BK_INK2 = "4A3F35", "6B645B"                  # booklet ink and caption grey (design-language.md)
BK_LOG = []                                           # notes of the booklet step (booklet/booklet_log.txt)
_BK_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
    [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
     667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
     278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
     260, 334, 584]                                   # Helvetica / Arial advance widths (1/1000 em), ASCII 32-126


def bk_text_w(s, pt, bold=False):
    """Width in mm of a label set in Arial at pt points (Helvetica widths; bold about 6 % wider)."""
    w = sum(_BK_HW[ord(ch) - 32] if 32 <= ord(ch) < 127 else 556 for ch in s)
    return w / 1000.0 * pt * BK_PT * (1.07 if bold else 1.0)


def bk_hex(c):
    return c if isinstance(c, str) else "%02X%02X%02X" % tuple(int(v) for v in c[:3])


class BkPage(object):
    """One booklet drawing: W x H mm, y up from the bottom (as the board's PDF writer), graphics in the board's item
    format, words as labels whose boxes are kept apart and inside the frame."""

    def __init__(self, W, H):
        self.W, self.H = float(W), float(H)
        self.items, self.labels, self.boxes = [], [], []

    # ---- graphics
    def fill(self, polys, col, order=50):
        polys = [P for P in polys if P and len(P) >= 3]
        if polys:
            self.items.append(("fill", polys, tuple(col), "BK", order, None))

    def line(self, P, col, w=0.15, order=50):
        if P and len(P) >= 2:
            self.items.append(("line", list(P), tuple(col), "BK", order, max(0.1, float(w)), None))

    def image(self, path, x0, y0, x1, y1, order=5):
        self.items.append(("image", path, (x0, y0, x1, y1), "BK", order, None))

    def put(self, items, f, k):
        """Board items -> this page through f (board xy -> page mm) with scale k (page mm per board unit); text left
        out (words are labels), line widths at least 0.1 mm."""
        for it in items:
            kd = it[0]
            if kd == "fill":
                self.items.append(("fill", [[f(x, y) for x, y in P] for P in it[1]]) + tuple(it[2:]))
            elif kd == "line":
                self.items.append(("line", [f(x, y) for x, y in it[1]], it[2], it[3], it[4],
                                   max(0.1, float(it[5] if it[5] is not None else 0.13)), it[6]))
            elif kd == "hatch":
                self.items.append(("hatch", [[f(x, y) for x, y in P] for P in it[1]], it[2], it[3], it[4], it[5] * k,
                                   it[6], max(0.1, float(it[7])), it[8]))
            elif kd == "image":
                a, b = f(it[2][0], it[2][1]), f(it[2][2], it[2][3])
                self.items.append(("image", it[1], (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]),
                                                    max(a[1], b[1]))) + tuple(it[3:]))

    # ---- labels
    def lbox(self, text, x, y, size, bold, anchor):
        w = bk_text_w(bk_label_text(text), size, bold) * 1.03
        x0 = x - (w / 2.0 if anchor == "C" else w if anchor == "R" else 0.0)
        return (x0, y - 0.21 * size * BK_PT, x0 + w, y + 0.72 * size * BK_PT)

    def free(self, b, pad=0.4):
        if b[0] < 0.3 or b[1] < 0.3 or b[2] > self.W - 0.3 or b[3] > self.H - 0.3:
            return False
        return not any(b[0] - pad < o[2] and o[0] < b[2] + pad and b[1] - pad < o[3] and o[1] < b[3] + pad
                       for o in self.boxes)

    def keep_out(self, x0, y0, x1, y1):
        """An area labels must not cover (north arrow, scale bar, a key)."""
        self.boxes.append((x0, y0, x1, y1))

    def label(self, text, x, y, size=BK_LAB, bold=False, anchor="L", colour=BK_INK, tries=None, leader=None,
              halo=False):
        """A label at (x, y) (baseline, page mm, y up), or the first free place of tries [(dx, dy, anchor)]; with
        leader=(ax, ay) a thin line from the label to that point when the label had to move. Returns the box or None."""
        size = max(BK_LAB, float(size))
        for dx, dy, an in ([(0.0, 0.0, anchor)] + list(tries or [])):
            b = self.lbox(text, x + dx, y + dy, size, bold, an)
            if self.free(b):
                self.boxes.append(b)
                self.labels.append({"x": round(x + dx, 2), "y": round(self.H - (y + dy), 2), "text": text,
                                    "size": size, "bold": bool(bold), "anchor": an, "colour": bk_hex(colour)})
                if halo:
                    self.fill([rect(b[0] - 0.5, b[1] - 0.4, b[2] + 0.5, b[3] + 0.4)], (255, 255, 255), order=88)
                if leader is not None and (dx or dy):
                    cx = min(max(leader[0], b[0]), b[2])
                    cy = b[1] - 0.3 if leader[1] < b[1] else (b[3] + 0.3 if leader[1] > b[3] else 0.5 * (b[1] + b[3]))
                    if math.hypot(cx - leader[0], cy - leader[1]) > 1.0:
                        self.line([(leader[0], leader[1]), (cx, cy)], C(BK_INK), 0.12, order=89)
                return b
        BK_LOG.append("label left out (no free place): " + text)
        return None

    def around(self, text, x, y, r=1.5, size=BK_LAB, bold=False, colour=BK_INK, leader=True, halo=False):
        """A label beside the point (x, y): right, left, above, below, then further out with a leader."""
        h = 0.72 * max(BK_LAB, size) * BK_PT
        tries = []
        for m in (1.0, 2.2, 3.6, 5.2, 7.0):
            d = r * m
            tries += [(d, -0.5 * h, "L"), (-d, -0.5 * h, "R"), (0.0, d, "C"), (0.0, -d - h, "C"),
                      (d, d, "L"), (-d, d, "R"), (d, -d - h, "L"), (-d, -d - h, "R")]
        return self.label(text, x + tries[0][0], y + tries[0][1], size, bold, "L", colour,
                          tries=[(dx - tries[0][0], dy - tries[0][1], an) for dx, dy, an in tries[1:]],
                          leader=(x, y) if leader else None, halo=halo)

    # ---- map furniture (graphics only; numbers are labels)
    def north(self, x, y, ang, k=4.0):
        """North arrow with its tip direction ang (radians on the page, 0 = up) centred at (x, y)."""
        c, s = math.cos(ang), math.sin(ang)
        R = lambda px, py: (x + c * px + s * py, y - s * px + c * py)
        tip, l, m, r = R(0, 0.75 * k), R(-0.38 * k, -0.5 * k), R(0, -0.22 * k), R(0.38 * k, -0.5 * k)
        self.fill([[tip, l, m]], INK, 95)
        self.fill([[tip, m, r]], (255, 255, 255), 95)
        self.line([tip, l, m, r, tip], INK, 0.12, 96)
        self.keep_out(x - 0.55 * k, y - 0.6 * k, x + 0.55 * k, y + 0.85 * k)

    def scalebar(self, x, y, mm_per_m, max_mm=40.0):
        """Scale bar from (x, y) (lower left): four segments, its length a round number of metres; '0' and the length
        as labels."""
        Lm = nice_floor(max_mm / mm_per_m)
        if Lm <= 0:
            return
        seg = Lm * mm_per_m / 4.0
        bh = 1.0
        for i in range(4):
            self.fill([rect(x + i * seg, y, x + (i + 1) * seg, y + bh)], INK if i % 2 == 0 else (255, 255, 255), 95)
        self.line(rect(x, y, x + 4 * seg, y + bh) + [(x, y)], INK, 0.12, 96)
        self.keep_out(x - 0.5, y - 0.5, x + 4 * seg + 0.5, y + bh + 0.5)
        self.label("0", x, y + bh + 1.7, anchor="C")
        self.label("{:,.0f} m".format(Lm), x + 4 * seg, y + bh + 1.7, anchor="C")

    # ---- output
    def trim(self, r):
        """Cut the graphics to r = (x0, y0, x1, y1) mm: no geometry is kept outside it (a PDF clip would keep it in
        the file, and Illustrator shows it)."""
        out = []
        for it in self.items:
            kd = it[0]
            if kd in ("fill", "hatch"):
                polys = [Q for Q in (bk_clip_poly(P, r) for P in it[1]) if len(Q) >= 3]
                if polys:
                    out.append((kd, polys) + tuple(it[2:]))
            elif kd == "line":
                for Q in bk_clip_line(it[1], r):
                    out.append(("line", Q) + tuple(it[2:]))
            else:
                out.append(it)
        self.items = out

    def write(self, path):
        if getattr(self, "engine", None):                  # a page of the axonometric engine (bk_a2_hero)
            bk_engine_pdf(path, self.engine[0], self.engine[1], self.W, self.H)
            return
        self.trim((0.0, 0.0, self.W, self.H))
        items = sorted(enumerate(self.items), key=lambda t: (float(t[1][4]) if t[1][0] != "text" else 0.0, t[0]))
        bk_write_pdf(path, [it for _i, it in items], self.W, self.H)


def bk_clip_poly(P, r):
    """One ring cut to the rectangle r (Sutherland-Hodgman); a hole ring stays a hole of the cut ring."""
    x0, y0, x1, y1 = r
    if all(x0 <= p[0] <= x1 and y0 <= p[1] <= y1 for p in P):
        return list(P)
    for inside, cut in ((lambda p: p[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
                        (lambda p: p[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
                        (lambda p: p[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
                        (lambda p: p[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1))):
        if not P:
            break
        Q, a = [], P[-1]
        for b in P:
            if inside(b):
                if not inside(a):
                    Q.append(cut(a, b))
                Q.append(b)
            elif inside(a):
                Q.append(cut(a, b))
            a = b
        P = Q
    return P


def bk_clip_line(P, r):
    """A polyline cut to the rectangle r (Liang-Barsky per segment): the pieces inside, joined where they meet."""
    x0, y0, x1, y1 = r
    out, cur = [], []
    for a, b in zip(P[:-1], P[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t0, t1, ok = 0.0, 1.0, True
        for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if p == 0.0:
                if q < 0.0:
                    ok = False
                    break
            else:
                t = q / p
                if p < 0.0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
        if not ok or t0 > t1:
            if len(cur) >= 2:
                out.append(cur)
            cur = []
            continue
        pa = (a[0] + t0 * dx, a[1] + t0 * dy)
        pb = (a[0] + t1 * dx, a[1] + t1 * dy)
        if cur and t0 == 0.0:
            cur.append(pb)
        else:
            if len(cur) >= 2:
                out.append(cur)
            cur = [pa, pb]
        if t1 < 1.0:
            out.append(cur)
            cur = []
    if len(cur) >= 2:
        out.append(cur)
    return out


def bk_write_pdf(path, items, W, H):
    """One single-page vector PDF of W x H mm: the board's own PDF writer (_pdf_page), no fonts, no text."""
    stream, imgs = _pdf_page(items, (0.0, 0.0, W, H), 1.0)
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    xo = []
    for im_ in imgs:
        w_, h_, data = im_[:3]
        if len(im_) > 3:
            xo.append(add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace /DeviceRGB "
                           "/BitsPerComponent 8 /Filter /DCTDecode /Length %d >>\nstream\n" % (w_, h_, len(data))
                           ).encode("latin-1") + data + b"\nendstream"))
            continue
        xo.append(add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace /DeviceRGB "
                       "/BitsPerComponent 8 /Filter /FlateDecode /DecodeParms << /Predictor 15 /Colors 3 "
                       "/BitsPerComponent 8 /Columns %d >> /Length %d >>\nstream\n" % (w_, h_, w_, len(data))
                       ).encode("latin-1") + data + b"\nendstream"))
    data = _zlib.compress(stream, 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data + b"\nendstream")
    pages_id = len(objs) + 2
    res = ("/XObject << %s >>" % " ".join("/Im%d %d 0 R" % (i + 1, x_) for i, x_ in enumerate(xo))) if xo else ""
    page = add(("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %s %s] /Contents %d 0 R /Resources << %s >> >>"
                % (pages_id, _pf(W * _PT), _pf(H * _PT), cid, res)).encode("latin-1"))
    add(("<< /Type /Pages /Kids [%d 0 R] /Count 1 >>" % page).encode("latin-1"))
    cat = add(("<< /Type /Catalog /Pages %d 0 R >>" % pages_id).encode("latin-1"))
    info = add(b"<< /Producer " + pdf_str(SCRIPT_VERSION + " booklet") + b" >>")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += ("%d 0 obj\n" % (i + 1)).encode() + b + b"\nendobj\n"
    x_ = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)).encode()
    for o_ in offs:
        out += ("%010d 00000 n \n" % o_).encode()
    out += ("trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objs) + 1, cat, info, x_)).encode()
    with open(path, "wb") as fh:
        fh.write(bytes(out))


def bk_group(B, name):
    """The board items of one drawing (its group "DRAWING · <name>" or "TECHNICAL <name>"), in display order."""
    its = [(i, it) for i, it in enumerate(B.items) if str(it[-1]) == name]
    return [it for i, it in sorted(its, key=lambda t: (float(t[1][6] if t[1][0] == "text" else t[1][4]), t[0]))]


def bk_in(items, r):
    """Items whose extent touches r = (x0, y0, x1, y1)."""
    out = []
    for it in items:
        bb = _item_bb(it)
        if bb is not None and bb[2] >= r[0] and bb[0] <= r[2] and bb[3] >= r[1] and bb[1] <= r[3]:
            out.append(it)
    return out


def bk_sim(model, board):
    """The similarity (scale, rotation, shift) taking model points to board points, from two pairs: f(x, y)."""
    (a0, a1), (b0, b1) = model[:2], board[:2]
    za, zb = complex(a1[0] - a0[0], a1[1] - a0[1]), complex(b1[0] - b0[0], b1[1] - b0[1])
    m = zb / za
    o = complex(*b0) - m * complex(*a0)

    def f(x, y):
        z = m * complex(x, y) + o
        return (z.real, z.imag)
    f.scale, f.rot = abs(m), math.atan2(m.imag, m.real)
    return f


def bk_frame_lines(items, F, widths=(0.25, 0.12), col=INK):
    """The board's lines of the frame F (closed 5-point polylines drawn as V.P(F.P + [F.P[0]])) among items, in
    drawing order: [model -> board similarity]."""
    out = []
    for w_ in widths:
        for it in items:
            if it[0] == "line" and len(it[1]) == len(F.P) + 1 and abs(float(it[5]) - w_) < 1e-6 and it[2] == col:
                f = bk_sim(F.P[:2], it[1][:2])
                p = f(*F.P[2])
                if math.hypot(p[0] - it[1][2][0], p[1] - it[1][2][1]) < 1e-3 * max(1.0, f.scale * F.w):
                    out.append(f)
    return out


def bk_frame_line(items, F, widths=(0.25, 0.12), col=INK):
    """The first of bk_frame_lines, or None."""
    fs = bk_frame_lines(items, F, widths, col)
    return fs[0] if fs else None


def bk_fit(r, W, H, pad=0.0, mode="fit"):
    """Board rect r -> page: uniform scale fitting r into W x H (fit) or filling it (fill), centred. (f, k)."""
    rw, rh = r[2] - r[0], r[3] - r[1]
    k = (min if mode == "fit" else max)((W - 2 * pad) / rw, (H - 2 * pad) / rh)
    ox, oy = 0.5 * (W - k * rw), 0.5 * (H - k * rh)
    f = lambda x, y: (ox + k * (x - r[0]), oy + k * (y - r[1]))
    return f, k


def bk_den(mm_per_m_max):
    """A printed scale 1:N for a drawing that may be at most mm_per_m_max mm per metre: N rounded up to 500 (to
    1,000 above 20,000). Returns (N, mm per metre)."""
    den = 1000.0 / mm_per_m_max
    step = 500.0 if den < 20000.0 else 1000.0
    den = step * math.ceil(den / step - 1e-9)
    return den, 1000.0 / den


def bk_bg_rect(items, order=1):
    """The extent of a map's quiet ground (its first fill at this order): the map's rectangle on the board."""
    for it in items:
        if it[0] == "fill" and float(it[4]) == order:
            return _item_bb(it)
    return None


def bk_no_north(items):
    """Items without the board's small north arrow (fills and lines at display order 60/61) and its crop frames."""
    return [it for it in items if not (it[0] in ("fill", "line") and float(it[4]) in (60.0, 61.0))
            and "Crop frames" not in str(it[3])]


def bk_texts(items, r=None):
    """[(text, x, y, height)] of the text items (in r when given)."""
    out = []
    for it in items:
        if it[0] == "text":
            x, y = it[2]
            if r is None or (r[0] <= x <= r[2] and r[1] <= y <= r[3]):
                out.append((str(it[1]), x, y, it[3]))
    return out


def bk_map_page(W, H, items, m2b, focus, fill_w=0.9, fill_h=0.8, clip=None, ox=None, oy=None):
    """A plan of board items at a round scale: the model points `focus` fill at most fill_w x fill_h of the frame,
    centred (or with their centre at ox, oy mm; ox "L": against the left edge). Returns (page, model -> page f, mm per metre, N)."""
    bb = bb_pts([m2b(x, y) for x, y in focus])
    s = m2b.scale                                          # board units per metre
    den, mpm = bk_den(min(fill_w * W / ((bb[2] - bb[0]) / s), fill_h * H / ((bb[3] - bb[1]) / s)))
    k = mpm / s                                            # page mm per board unit
    cx, cy = 0.5 * (bb[0] + bb[2]), 0.5 * (bb[1] + bb[3])
    px = 0.5 * W if ox is None else (0.5 + 0.5 * k * (bb[2] - bb[0]) if ox == "L" else ox)
    py = 0.5 * H if oy is None else oy
    b2p = lambda x, y: (px + k * (x - cx), py + k * (y - cy))
    reg = (cx - px / k, cy - py / k, cx + (W - px) / k, cy + (H - py) / k)
    if clip is not None:
        reg = (max(reg[0], clip[0]), max(reg[1], clip[1]), min(reg[2], clip[2]), min(reg[3], clip[3]))
    pg = BkPage(W, H)
    pg.put(bk_in(items, reg), b2p, k)
    a_, b_ = b2p(reg[0], reg[1]), b2p(reg[2], reg[3])
    pg.trim((max(0.0, a_[0]), max(0.0, a_[1]), min(W, b_[0]), min(H, b_[1])))   # the map's rectangle, cut
    pg.b2p = b2p
    f = lambda x, y: b2p(*m2b(x, y))
    return pg, f, mpm, den


def bk_furniture(pg, f, mpm, corner="BR", bar_mm=30.0):
    """North arrow and scale bar in a corner of a plan (graphics; the bar's numbers are labels)."""
    a = f(0.0, 0.0)
    b = f(0.0, 100.0)
    ang = math.atan2(b[0] - a[0], b[1] - a[1])
    W, H = pg.W, pg.H
    if corner == "BR":
        pg.north(W - 4.0, 5.0, ang)
        pg.scalebar(W - 16.0 - bar_mm, 1.5, mpm, bar_mm)
    elif corner == "BL":
        pg.north(4.0, 5.0, ang)
        pg.scalebar(12.0, 1.5, mpm, bar_mm)
    else:                                                  # "R": a column right of a strip map
        pg.north(W - 4.0, H - 5.0, ang)
        pg.scalebar(W - 3.5 - bar_mm, 2.2, mpm, bar_mm)


def bk_label_text(t):
    """A label's width-relevant text: {src:...} becomes [nn], {val:...} its fallback."""
    import re as _re
    t = _re.sub(r"\{src:[^}]*\}", "[00]", t)
    return _re.sub(r"\{val:[^}|]*\|?([^}]*)\}", lambda m: m.group(1) or "000", t)


def bk_leg(kind, col, label):
    return {"kind": kind, "colour": bk_hex(col), "label": label}


def bk_street_mid(S, name):
    """The middle of the longest piece of the named street inside the frame (movement network), model xy, or None."""
    R = (movement(S) or {}).get("R")
    if not R or not name:
        return None
    best = None
    for i in R["inside"]:
        p = R["pieces"][i]
        if (p["tags"].get("name") or "").strip() == name and (best is None or p["L"] > best["L"]):
            best = p
    if best and best["a"] in R["xy"] and best["b"] in R["xy"]:
        a, b = R["xy"][best["a"]], R["xy"][best["b"]]
        return (0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]))
    return None


# ------------------------------------------------------------ A1 · what is there
def bk_a1_hero(S, B, W, H):
    its = bk_group(B, "DRAWING · 01 What is there")
    M = bk_bg_rect(its)
    m2b = bk_frame_line(its, S.F, (0.12, 0.25))
    if M is None or m2b is None:
        raise Exception("plan 01 not found on the board")
    pg, f, mpm, den = bk_map_page(W, H, bk_no_north(its), m2b, S.F.P, 0.9, 0.62, clip=M)
    bk_furniture(pg, f, mpm, "BR")
    pos = dict((t, pg.b2p(x, y)) for t, x, y, h in bk_texts(its, M))
    rv = pos.get(S.river_label[3]) if getattr(S, "river_label", None) else None
    if rv:
        pg.around(u"Selinos · Bergama Çayı {src:dai_selinos}", rv[0], rv[1], 1.0, colour=bk_hex(BLUE_D), halo=True)
    fb = bb_pts([f(x, y) for x, y in S.F.P])
    pg.label(u"Site frame {:,.0f} x {:,.0f} m".format(S.F.w, S.F.h), fb[0], fb[3] + 1.2,
             tries=[(0.0, fb[1] - fb[3] - 4.2, "L")], halo=True)
    cs = ((u"C1", u"walls cut the town off"), (u"C2", u"heritage over hidden stream"),
          (u"C3", u"K4: monument and traffic"), (u"C4", u"dry bed, bad smell"),
          (u"C5", u"flood against everyday life"), (u"C6", u"industry at the confluence"))
    for k, t in cs:
        if k in pos:
            pg.around(k + u" " + t, pos[k][0], pos[k][1], 1.6, halo=True)
    ks = [pos[k] for k in ("K1", "K2", "K3", "K4", "K5", "K6") if k in pos]
    if ks:
        pg.around(u"K1-K6 bridges", ks[len(ks) // 2][0], ks[len(ks) // 2][1], 2.5, halo=True)
    ph = [pos[str(i)] for i in range(1, 9) if str(i) in pos]
    if ph:
        c_ = (sum(p[0] for p in ph) / len(ph), sum(p[1] for p in ph) / len(ph))
        near = min(ph, key=lambda p: math.hypot(p[0] - c_[0], p[1] - c_[1]))
        pg.around(u"1-8 photo viewpoints", near[0], near[1], 2.0, halo=True)
    st = bk_street_mid(S, getattr(S, "int_peak_name", "") or "")
    if st:                                                 # the density peak's street (page1_readings)
        x, y = f(*st)
        pg.around(u"Densest near " + S.int_peak_name, x, y, 2.0, halo=True)
    leg = [bk_leg("fill", CAT[k][1], n) for k, n in (
        ("residential", "Homes"), ("mixed", "Shop below, home above"), ("commercial", "Commerce"),
        ("institutional", "Civic"), ("religious", "Sacred and heritage"), ("industrial", "Workshops and industry"),
        ("green", "Parks and green ground"), ("water", "The stream"))]
    leg += [bk_leg("line", EDGE[k][1], short(EDGE[k][0])) for k in EDGE_ORDER]
    return dict(page=pg, caption=u"Plan 01 · what is there today", scale_den=den, legend=leg)


BK_CAT_SHORT = {"residential": u"Homes", "mixed": u"Shop below, home above", "commercial": u"Commerce",
                "institutional": u"Civic", "religious": u"Sacred and heritage", "industrial": u"Workshops and industry",
                "transport": u"Movement", "green": u"Parks and green ground", "agri": u"Farmland",
                "vacant": u"Vacant", "water": u"The stream"}       # the plan's legend words for the use colours


def bk_a1_side2(S, B, W, H):
    """Ground cover of the frame as one bar per row, % of the site frame, in the use colours; the unmapped ground in
    its satellite tones below."""
    tot = frame_total(S)
    rows = [(CAT[k][1], 100.0 * S.area.get(k, 0.0) / tot, BK_CAT_SHORT.get(k, CAT[k][0]))
            for k in CAT_ORDER if S.area.get(k, 0.0) > 0.0]
    rest = [(col, 100.0 * a / tot, lab.split(u" · ")[0]) for k_, lab, col, a in (getattr(S, "rest", None) or [])
            if a > 0.0]
    if not rows:
        return None
    pg = BkPage(W, H)
    top = H - 1.0
    pg.label(u"% of the site frame", 0.5, top - 2.0)
    n = len(rows) + len(rest)
    head = 4.6 + (5.2 if rest else 0.0)
    pitch = min(6.5, (H - head - 1.0) / float(n))
    bh = min(3.4, 0.62 * pitch)
    vmax = max(v for c, v, t in rows + rest)
    # the bars name themselves (no legend: the A1 footer holds the plan's map legend)
    tw = max(bk_text_w(u"{} {:.1f}".format(t, v), BK_LAB) for c, v, t in rows + rest)
    wmax = W - 3.0 - tw
    y = top - 4.6
    for i, (col, v, nm) in enumerate(rows + rest):
        if i == len(rows) and rest:
            y -= 1.4
            pg.label(u"unmapped ground: satellite", 0.5, y - 2.4)
            y -= 3.8
        yb = y - pitch + 0.5 * (pitch - bh)
        L_ = max(0.4, wmax * v / vmax)
        pg.fill([rect(0.5, yb, 0.5 + L_, yb + bh)], col, 20)
        if i >= len(rows):
            pg.line(rect(0.5, yb, 0.5 + L_, yb + bh) + [(0.5, yb)], INK2, 0.1, 21)
        pg.label(u"{} {:.1f}".format(nm, v), L_ + 1.5, yb + 0.5 * bh - 0.9)
        y -= pitch
    return dict(page=pg, caption=u"Ground cover in the frame", scale_den=None, legend=[])


# ------------------------------------------------------------ A2 · heights and enclosure (the axonometric engine)
BK_AXO_LAYERS = ("base", "contours", "ground_streets", "parks", "stream", "pools", "tree_shadows", "historic_wall",
                 "banks", "trees", "outline", "topic", "context")


def bk_a2_hero(S, B, W, H):
    """Plan 01 as a parallel axonometric (the engine of export_axonometrics), drawn again for this frame without its
    sheet, words and callouts; the callouts' places carry the labels."""
    import re as _re
    DG, ctx = diagram_ctx(S)
    ext = ctx.extents[0]
    n0 = len(DG["LOG"])
    pg0, _st = DG["compose"](ctx, DG["SPECS"]["S1"](ctx, ext), ext, "")
    del DG["LOG"][n0:]
    lay = lambda it: it[{"poly": 6, "line": 5, "circle": 7, "text": 8}[it[0]]]
    draw = [it for it in pg0.items if it[0] != "text" and lay(it) in BK_AXO_LAYERS]
    pts = []
    for it in draw:
        if it[0] == "poly":
            pts += [p for r in it[1] for p in r]
        elif it[0] == "line":
            pts += it[1]
        else:
            pts.append((it[1], it[2]))
    bb = bb_pts(pts)
    band = 9.0                                             # mm kept at the top and bottom for the labels
    k = min((W - 1.0) / (bb[2] - bb[0]), (H - 2 * band) / (bb[3] - bb[1]))
    ox, oy = 0.5 * (W - k * (bb[2] - bb[0])), 0.5 * (H - k * (bb[3] - bb[1]))
    f = lambda x, y: (ox + k * (x - bb[0]), oy + k * (y - bb[1]))
    out = []
    for it in draw:
        if it[0] == "poly":
            out.append(("poly", [[f(*p) for p in r] for r in it[1]], it[2], it[3], max(0.1, it[4]) if it[3] else it[4])
                       + tuple(it[5:]))
        elif it[0] == "line":
            out.append(("line", [f(*p) for p in it[1]], it[2], max(0.1, it[3])) + tuple(it[4:]))
        else:
            c_ = f(it[1], it[2])
            out.append(("circle", c_[0], c_[1], it[3] * k) + tuple(it[4:6]) + (max(0.1, it[6]),) + tuple(it[7:]))
    pg = BkPage(W, H)
    # the callouts: title (bold) -> its leader (first point = the place it points at)
    leads = [it[1] for it in pg0.items if it[0] == "line" and it[5] == "callouts"]
    sky = stream_sky(S) or {}
    lows = sorted(m[2] for m in sky.get("marks", []) if m[3] == "low")
    wants = []
    for it in pg0.items:
        if it[0] != "text" or it[8] != "callouts" or not it[6] or len(it[1]) < 3:
            continue
        t, tx, ty = it[1], it[2], it[3]
        if not leads:
            break
        ld = min(leads, key=lambda P: math.hypot(P[-1][0] - tx, P[-1][1] - ty))
        tgt = f(*ld[0])
        m = _re.match(r"Sky view (\d+) %", t)
        if m:
            v = int(m.group(1))
            hi = [q[2] for q in sky.get("marks", []) if q[3] == "high"]
            if hi and abs(100.0 * hi[0] - v) < 0.6:
                lab = u"V sky {} % · most open".format(v)
            elif lows and abs(100.0 * lows[0] - v) < 0.6:
                lab = u"V sky {} % · most enclosed".format(v)
            else:
                lab = u"V sky {} % · enclosed".format(v)
            wants.append((lab, tgt))
        elif t.startswith(u"Kızıl Avlu"):
            wants.append((u"Kızıl Avlu · Red Hall {src:dai2020}", tgt))
            wants.append((u"stream in 2 tunnels below {src:icomos2014}", tgt))
        elif t in (u"Bergama Ulu Cami", u"Ansarlı Camii", u"Emir Sultan Cami", u"Tarihi Kalıntılar") or \
                t.startswith((u"K4 ", u"K5 ")):
            wants.append((t, tgt))
    for lab, (x, y) in wants:
        pg.fill([circle_pts(x, y, 0.7, 12)], (255, 255, 255), 90)
        pg.fill([circle_pts(x, y, 0.45, 12)], INK, 91)
        pg.keep_out(x - 0.8, y - 0.8, x + 0.8, y + 0.8)
    for lab, (x, y) in wants:
        pg.around(lab, x, y, 3.0, halo=True)
    if sky.get("mean") is not None:
        wd = [(it[2], it[3]) for it in pg0.items if it[0] == "text" and it[8] == "words"]
        x, y = f(*wd[0]) if wd else (0.5 * W, 0.5 * H)
        pg.around(u"bed mean {:.0f} %".format(100.0 * sky["mean"]), x, y, 2.0, halo=True)
    for it in pg.items:                                    # leaders, dots and halos onto the engine's page
        if it[0] == "fill":
            out.append(("poly", it[1], bk_hex(it[2]), None, 0.1, None, "booklet", 1, None))
        elif it[0] == "line":
            out.append(("line", it[1], bk_hex(it[2]), it[5], None, "booklet", 1))
    pg.engine = (DG, out)
    leg = [bk_leg("fill", CAT[k_][1], n) for k_, n in (
        ("residential", "Homes"), ("mixed", "Shop below, home above"), ("commercial", "Commerce"),
        ("institutional", "Civic"), ("religious", "Sacred and heritage"), ("industrial", "Workshops and industry"),
        ("green", "Parks and green ground"), ("water", "The stream"))]
    return dict(page=pg, caption=u"Heights: floors x storey height (our model) · V: sky view", scale_den=None,
                legend=leg)


def bk_engine_pdf(path, DG, items, W, H):
    """A page of the axonometric engine's items written by its own PDF writer at W x H mm."""
    pg = DG["Page"]("booklet", "")
    pg.items = items
    old = DG["PAGE_W"], DG["PAGE_H"]
    try:
        DG["PAGE_W"], DG["PAGE_H"] = W, H
        DG["write_pdf"]([pg], path)
    finally:
        DG["PAGE_W"], DG["PAGE_H"] = old


# ------------------------------------------------------------ A3 · how people use it
def bk_a3_hero(S, B, W, H):
    its = bk_group(B, "DRAWING · 07 How people use it")
    M = bk_bg_rect(its)
    m2b = bk_frame_line(its, S.F, (0.25,))
    if M is None or m2b is None:
        raise Exception("plan 07 not found on the board")
    sp_c = mix(CAT["commercial"][1], INK, 0.35)
    white = (255, 255, 255)
    keep = []
    for it in bk_no_north(its):
        if it[0] in ("fill", "line"):
            o_ = float(it[4])
            if it[2] == sp_c or (it[0] == "line" and it[2] == white and o_ == 20.0):
                continue                                   # the proposed spine and its stops: part C
            if o_ in (62.0, 63.0, 64.0):
                continue                                   # roundels and name boxes: redrawn at this size below
        keep.append(it)
    pg, f, mpm, den = bk_map_page(W, H, keep, m2b, context_frame(S.F).P, 0.99, 0.9, clip=M)
    bk_furniture(pg, f, mpm, "BR")
    MV = movement(S) or {}
    # destinations of the walks: roundels big enough for their letter
    fcol = dict((let, hexrgb(c)) for fn_, let, c, lab in WALK_FUN)
    rr = 1.9
    lets = [(t, pg.b2p(x, y)) for t, x, y, h in bk_texts(its, M) if t in ("H", "E", "C", "W", "M")]
    for t, (x, y) in lets:
        pg.fill([circle_pts(x, y, rr, 20)], fcol[t], 70)
        pg.line(circle_pts(x, y, rr, 20) + [circle_pts(x, y, rr, 20)[0]], white, 0.2, 71)
    for t, (x, y) in lets:
        pg.label(t, x, y - 0.95, bold=True, anchor="C", colour="FFFFFF")
    if MV.get("rows"):
        nm = MV["rows"][0]["name"]
        st = bk_street_mid(S, nm)
        if st:
            x, y = f(*st)
            pg.around(nm, x, y, 1.5, bold=True, halo=True)

    def mid(Ps):
        P = max(Ps, key=pl_length)
        p, t = pl_point_at(P, 0.5 * pl_length(P))
        return f(*p)
    if S.corr_primary:
        x, y = mid([P for g in S.corr_primary for P in g["Ps"]])
        pg.around(u"primary commercial spine", x, y, 2.0, halo=True)
    if S.corr_secondary:
        x, y = mid([P for g in S.corr_secondary for P in g["Ps"]])
        pg.around(u"secondary spine", x, y, 2.0, halo=True)
    cl = [c for c in S.clusters if any(S.F.inside(x, y) for x, y in c["P"])]
    if cl:
        P = max(cl, key=lambda c: c.get("n", 0))["P"]
        x, y = f(sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P))
        pg.around(u"civic constellation", x, y, 2.0, halo=True)
    if lets:                                               # the letters' key, under the map
        y = 15.0
        for t in (u"H health · E education", u"C civic · W worship", u"M food and market"):
            pg.label(t, 1.0, y)
            y -= 4.2
    else:
        BK_LOG.append("a3_hero: no walks to the nearest service on this run (no working areas): the letter key "
                      "H/E/C/W/M is left out")
    leg = [bk_leg("line", SEQ[0], "Few routes"), bk_leg("line", SEQ[2], "More routes"),
           bk_leg("line", SEQ[4], "Busiest street"), bk_leg("fill", CAT["commercial"][1], "Commerce"),
           bk_leg("fill", CAT["mixed"][1], "Shop below, home above"), bk_leg("fill", CAT["institutional"][1], "Civic"),
           bk_leg("fill", CAT["religious"][1], "Sacred")]
    leg += [bk_leg("dot", hexrgb(c), lab) for fn_, let, c, lab in WALK_FUN if let in ("H", "E", "W", "M")]
    return dict(page=pg, caption=u"Movement potential = routes, not counts of people", scale_den=den, legend=leg)


def bk_a3_inset(S, B, W, H, j, caption):
    its = bk_group(B, "DRAWING · 07 How people use it")
    fs = bk_frame_lines(its, S.F, (0.1,), INK2)
    if len(fs) <= j:
        BK_LOG.append("%s: inset %d not on the board (no movement potential on this run)" % (caption, j + 1))
        return None
    m2b = fs[j]
    fr = bb_pts([m2b(x, y) for x, y in S.F.P])
    pad = 0.02 * (fr[2] - fr[0])
    clip = (fr[0] - pad, fr[1] - pad, fr[2] + pad, fr[3] + pad)
    pg, f, mpm, den = bk_map_page(W, H, bk_no_north(its), m2b, S.F.P, 0.99, 0.72, clip=clip, ox="L", oy=H - 15.5)
    bk_furniture(pg, f, mpm, "BL")
    return dict(page=pg, caption=caption, scale_den=den, legend=[])


def bk_a3_side1(S, B, W, H):
    return bk_a3_inset(S, B, W, H, 0, u"Walking today")


def bk_a3_side2(S, B, W, H):
    return bk_a3_inset(S, B, W, H, 1, u"Driving today")


def bk_a3_side3(S, B, W, H):
    """Shops per street against walking potential today, one dot per named street of 50 m+ (movement())."""
    MV = movement(S) or {}
    big = [r for r in (MV.get("big") or []) if r.get("walk_b") is not None]
    if not big:
        BK_LOG.append("a3_side3: no movement potential on this run")
        return None
    pg = BkPage(W, H)
    x0, y0, x1, y1 = 9.0, 9.5, W - 1.0, H - 4.0
    xm = max(100.0, max(r["walk_b"] for r in big))
    ym = max(1.0, max(r["shops"] for r in big))
    ym = float(nice_step(ym, 4) * math.ceil(ym / nice_step(ym, 4)))
    pg.fill([rect(x0, y0, x1, y1)], mix(PAPER, (255, 255, 255), 0.5), 10)
    for v in (0.0, 50.0, 100.0):
        if v <= xm:
            xx = x0 + (x1 - x0) * v / xm
            pg.line([(xx, y0), (xx, y1)], FAINT, 0.1, 11)
            pg.label("{:.0f}".format(v), xx, y0 - 3.4, anchor="C" if v > 0 else "L", tries=[(0.0, 0.0, "R")])
    for v in (0.0, ym):
        yy = y0 + (y1 - y0) * v / ym
        pg.line([(x0, yy), (x1, yy)], FAINT, 0.1, 11)
        pg.label("{:.0f}".format(v), x0 - 1.2, yy - 0.9, anchor="R")
    for r in big:
        pg.fill([circle_pts(x0 + (x1 - x0) * r["walk_b"] / xm, y0 + (y1 - y0) * r["shops"] / ym, 0.55, 10)],
                mix(CAT["commercial"][1], INK, 0.2), 20)
    pg.line([(x0, y0), (x1, y0)], INK2, 0.12, 21)
    pg.line([(x0, y0), (x0, y1)], INK2, 0.12, 21)
    pg.label(u"walking index", 0.5 * (x0 + x1), 1.0, anchor="C")
    pg.label(u"shops", x0 + 1.0, y1 + 1.0)
    pg.label(u"{} streets of 50 m+".format(len(big)), x1, y1 + 1.0, anchor="R")
    return dict(page=pg, caption=u"More walkers, more shops", scale_den=None, legend=[])


# ------------------------------------------------------------ A4 · the stream edge
BK_RIP_RAMP = [(1.0, "E3E6CF"), (5.0, "C9D1A4"), (10.0, "A9B57F"), (20.0, "8C9969"), (40.0, "6B774A"), (60.0, "495338")]


def bk_a4_s2(S, B, W, H):
    """The stream's tree cover bank by bank every 25 m (draw_riparian's data), laid out for a full-width strip."""
    cor = seam_pack().get("corridor", {})
    if not cor:
        BK_LOG.append("a4_s2: no corridor data in the data pack")
        return None
    n, bm = cor["n_bins"], cor["bin_m"]
    names = ["left 60-100", "left 30-60", "left 15-30", "left 0-15", "right 0-15", "right 15-30", "right 30-60",
             "right 60-100"]
    pg = BkPage(W, H)
    lw_ = 27.0
    cx0, cx1 = lw_, W - 1.0
    cw = (cx1 - cx0) / float(n)
    X = lambda ch: cx0 + ch / bm * cw
    top = H - 4.6
    wat = 3.4
    rh = (top - wat - 1.8 - 4.2 - 1.0) / 8.0
    yy = top
    rows_y = []
    for j, nm in enumerate(names):
        if j == 4:
            yw = yy
            pg.fill([rect(cx0, yw - wat, cx1, yw)], CAT["water"][1], 3)
            yy -= wat
        rows_y.append(yy)
        vals = cor["cover"].get(nm, {}).get("pct") or cor["cover"].get(nm, {}).get("cover") or []
        cells = cor["cover"].get(nm, {}).get("cells", [])
        pg.fill([rect(cx0, yy - rh, cx1, yy)], C("F6F5EF"), 2)
        for i in range(n):
            v = vals[i] if i < len(vals) else None
            if v is None or (i < len(cells) and cells[i] < 20):
                continue
            col = None
            for t_, h_ in BK_RIP_RAMP:
                if v >= t_:
                    col = C(h_)
            if col:
                pg.fill([rect(cx0 + i * cw, yy - rh, cx0 + (i + 1) * cw, yy)], col, 3)
        yy -= rh
    yb = yy
    pg.label(u"the Selinos (flowing right)", cx0 + 1.0, yw - wat + 0.5 * (wat - 2.46) + 0.55)
    pg.label(u"left bank", lw_ - 1.5, rows_y[2] - 0.9, anchor="R")
    pg.label(u"right bank", lw_ - 1.5, rows_y[5] - 0.9, anchor="R")
    for a, b in cor.get("covered_reaches", []):
        pg.fill([rect(X(a), yb - 1.6, X(b), yb - 0.4)], BLUE_D, 4)
    ch = cor.get("bridges_ch", [])
    for i in range(0, len(ch) - 1, 2):
        xm = X(0.5 * (ch[i] + ch[i + 1]))
        pg.line([(xm, top + 0.3), (xm, yb - 0.2)], INK, 0.15, 6)
    for nm, c_ in sorted(cor.get("sections_ch", []), key=lambda t: t[1]):
        pg.label(nm, X(c_), yb - 4.6, bold=True, anchor="C")
        pg.line([(X(c_), yb - 1.9), (X(c_), yb - 2.4)], INK, 0.12, 6)
    for m, t in ((0.0, u"0 m"), (2500.0, u"2,500 m")):
        if m <= n * bm:
            pg.line([(X(m), top), (X(m), top + 0.6)], INK2, 0.1, 6)
            pg.label(t, X(m), top + 1.0, anchor="C" if m > 0 else "L")
    ky = 1.0
    pg.fill([rect(1.0, ky + 4.4, 4.0, ky + 5.6)], BLUE_D, 4)
    pg.label(u"covered (culvert)", 5.0, ky + 4.1)
    pg.line([(2.5, ky - 0.2), (2.5, ky + 2.4)], INK, 0.15, 6)
    pg.label(u"bridge", 5.0, ky)
    leg = [bk_leg("fill", C(h_), lab) for (t_, h_), lab in zip(
        [BK_RIP_RAMP[0], BK_RIP_RAMP[2], BK_RIP_RAMP[4], BK_RIP_RAMP[5]], (u"1 %+ under crowns", u"10 %+", u"40 %+",
                                                                         u"60 %+"))]
    return dict(page=pg, caption=u"Tree cover along the banks, every 25 m", scale_den=None, legend=leg)


def bk_a4_s3(S, B, W, H):
    """Section S1 as the board draws it (draw_section_strip): the cut and what lies beyond it, without the land-cover
    ribbon, header and words, fitted to the strip; the strip's own figures and names as labels at their places. The
    section lines exist only in Rhino: with none, the block is left out (no placeholder)."""
    import re as _re
    secs = getattr(S, "sections", None) or []
    if not secs:
        BK_LOG.append("a4_s3: no section lines on this run (they come from Rhino): the section block is left out")
        return None
    sd = next((s_ for s_ in secs if s_["name"] == "S1"), secs[0])
    nm = sd["name"]
    its = [it for it in B.items if str(it[-1]).startswith("DRAWING · ") and str(it[-1]).endswith(" Section " + nm)]
    if not its:
        BK_LOG.append("a4_s3: the drawing of section %s is not on the board" % nm)
        return None
    tx = bk_texts(its)
    ends = sorted([t for t in tx if t[0] in (nm, nm + "'")], key=lambda t: -t[3])[:2]
    lev = [t for t in tx if _re.match(r"^\+\d", t[0])]
    wid = [t for t in tx if _re.match(r"^\d+ m$", t[0])]
    if len(ends) < 2 or not (lev or wid):
        BK_LOG.append("a4_s3: the section drawing's ends or levels not found: left out")
        return None
    he = max(t[3] for t in ends)
    y_top = max(t[2] for t in ends) + 1.6 * he
    y_bot = min(t[2] - 1.2 * t[3] for t in lev + wid)
    band = [it for it in its if it[0] != "text" and "Crop frames" not in str(it[3])]
    band = bk_in(band, (-1e12, y_bot, 1e12, y_top))
    xs = []
    for it in band:
        b = _item_bb(it)
        if b is not None and b[1] >= y_bot - 1e-6 and b[3] <= y_top + 1e-6:
            xs += [b[0], b[2]]
    x0, x1 = min(xs + [t[1] for t in ends]), max(xs + [t[1] for t in ends])
    top_band = 4.5
    f, k = bk_fit((x0, y_bot, x1, y_top), W, H - top_band, 0.3)
    pg = BkPage(W, H)
    pg.put(band, f, k)
    e0, e1 = sorted(ends, key=lambda t: t[1])
    for t, an in ((e0, "L"), (e1, "R")):
        x, y = f(t[1], t[2])
        pg.label(t[0], x, y, size=9.5, bold=True, anchor="C", tries=[(0.0, 2.0, "C"), (0.0, -3.0, "C")])
    beds = [l for l in sd["levels"] if l[3] == "bed"]
    banks = [l for l in sd["levels"] if l[3] == "bank"]
    if wid:
        x, y = f(wid[0][1], wid[0][2])
        pg.around(u"stream width " + wid[0][0], x, y, 1.0, halo=True)
        if beds and banks:
            pg.around(u"bed {:.1f} m below banks".format(banks[0][2] - beds[0][2]), x, y - 3.0, 1.5, halo=True)
    for t in lev:
        x, y = f(t[1], t[2])
        pg.around(t[0], x, y, 0.8, halo=True)
    row = [t for t in tx if t[2] < y_bot]
    for t in row:
        m = _re.match(r"^([A-ZÇĞİÖŞÜ ]+EDGE) · (WALLED|EMBANKED)", t[0])
        if m:
            x = f(t[1], t[2])[0]
            yw = f(0.0, wid[0][2])[1] if wid else 0.5 * H
            pg.around(m.group(2) + u" · " + m.group(1).lower(), x, yw + 2.0, 1.2, halo=True)
    cut_y = [t[2] for t in row if t[0].endswith("on the cut")]
    for t in row:
        if t[0].endswith("on the cut") or (t[2] in cut_y and "EDGE" not in t[0] and "STREAM" not in t[0]):
            name = t[0].split(" · ")[0][:30]
            x = f(t[1], t[2])[0]
            pg.label(name, x, H - 3.2, anchor="C", tries=[(0.0, 0.0, "L"), (0.0, 0.0, "R")])
    return dict(page=pg, caption=u"Section {} · the ground as it falls to the water".format(nm), scale_den=None,
                legend=[])


# ------------------------------------------------------------ A5, A6 · the technical maps (T1-T8)
def bk_tmap(S, B, W, H, group, png, caption, legend):
    its = bk_group(B, group)
    img = [it for it in its if it[0] == "image" and os.path.basename(it[1]) == png]
    if not img:
        BK_LOG.append("%s: %s not on the board on this run" % (caption, png))
        return None
    try:                                                   # the map itself is the board's raster (render_tech)
        with open(img[0][1], "rb") as fh:
            hd = fh.read(24)
        pw_, ph_ = _struct.unpack(">II", hd[16:24]) if hd[12:16] == b"IHDR" else (0, 0)
    except Exception:
        pw_ = ph_ = 0
    if pw_ * ph_ < 10000:
        BK_LOG.append("%s: %s is missing or empty on this run: the frame is left out" % (caption, png))
        return None
    r = img[0][2]
    tol = 0.002 * (r[2] - r[0])
    over = [it for it in bk_no_north(its) if it[0] in ("fill", "line", "hatch") and float(it[4]) > 5.0]
    over = [it for it in over if (lambda b: b is not None and b[0] >= r[0] - tol and b[1] >= r[1] - tol and
                                  b[2] <= r[2] + tol and b[3] <= r[3] + tol)(_item_bb(it))]
    F = S.F
    s = (r[2] - r[0]) / F.w

    def m2b(x, y):
        u, v = F.local(x, y)
        return (r[0] + s * (u - F.u0), r[3] + s * (v - F.v1))
    m2b.scale = s
    pg, f, mpm, den = bk_map_page(W, H, [img[0]] + over, m2b, F.P, (W - 36.0) / W, 0.995, clip=r, ox="L")
    bk_furniture(pg, f, mpm, "R")
    return dict(page=pg, caption=caption, scale_den=den, legend=legend)


def bk_a5_s1(S, B, W, H):
    return bk_tmap(S, B, W, H, "TECHNICAL T1 · Sound", "T1_sound_lden.png",
                   u"T1 · road noise, Lden · model, not measured on site", [])


def bk_a5_s2(S, B, W, H):
    return bk_tmap(S, B, W, H, "TECHNICAL T2 · Surface heat", "T2_surface_heat_summer.png",
                   u"T2 · ground surface temperature, summer", [])


def bk_a5_s3(S, B, W, H):
    return bk_tmap(S, B, W, H, "TECHNICAL T3 · Shade", "T3_shade_year.png",
                   u"T3 · hours in shade, the mean day of the year", [])


def bk_a5_s4(S, B, W, H):
    return bk_tmap(S, B, W, H, "TECHNICAL T4 · Solar radiation", "T4_solar_radiation_summer.png",
                   u"T4 · solar radiation, summer day", [])


def bk_a6_s1(S, B, W, H):
    return bk_tmap(S, B, W, H, "TECHNICAL T5 · Wind", "T5_wind_summer.png",
                   u"T5 · wind at 1.5 m, summer daylight hours", [])


def bk_a6_s2(S, B, W, H):
    return bk_tmap(S, B, W, H, "TECHNICAL T7 · Felt temperature", "T7_felt_temperature_summer.png",
                   u"T7 · felt temperature (UTCI {src:brode2012}), summer", [])


def bk_a6_s3(S, B, W, H):
    return bk_tmap(S, B, W, H, "TECHNICAL T7 · Felt temperature", "T7_felt_temperature_winter.png",
                   u"T7 · felt temperature, winter", [])


def bk_a6_s4(S, B, W, H):
    return bk_tmap(S, B, W, H, "TECHNICAL T8 · Comfortable hours", "T8_comfortable_hours_year.png",
                   u"T8 · hours neither hot nor cold, UTCI 9-26 °C {src:blazejczyk2013}", [])


# ------------------------------------------------------------ A7 · climate and comfort
BK_SUN, BK_SHADE, BK_MEAN = C("E85319"), C("4A94A9"), C("4A3F35")     # the plan's legend colours of the three curves
BK_BANDS = [(26.0, 32.0, (253, 236, 206), u"moderate heat"), (32.0, 38.0, (250, 214, 180), u"strong heat"),
            (38.0, 46.0, (244, 186, 160), None), (46.0, 99.0, (232, 160, 150), None),
            (9.0, 26.0, (236, 242, 228), u"no thermal stress"), (0.0, 9.0, (214, 228, 240), u"slight cold"),
            (-13.0, 0.0, (196, 214, 236), None)]


def bk_a7_hero(S, B, W, H):
    """Felt temperature (UTCI) through the typical day of each season, 2 x 2: open sun and street shade
    (utci_reference_day) and the site's mean (T7), over the UTCI stress bands."""
    CF = (getattr(S, "env", None) or {}).get("comfort")
    if not CF:
        BK_LOG.append("a7_hero: no comfort results on this run")
        return None
    data = []
    for sd in SEASONS:
        ref = utci_reference_day(S, sd["key"])
        data.append((sd, ref["sun"], ref["shade"], CF["seasons"][sd["key"]]["by_hour"]))
    vv = [v for d in data for ser in d[1:] for v in ser if v is not None]
    lo, hi = 5.0 * math.floor(min(vv) / 5.0), 5.0 * math.ceil(max(vv) / 5.0)
    pg = BkPage(W, H)
    gx, gy = 6.0, 5.0
    cw, chh = (W - gx) / 2.0, (H - gy) / 2.0
    named = set()
    for q, (sd, sun, sha, site) in enumerate(data):
        X0 = (q % 2) * (cw + gx)
        Yt = H - (q // 2) * (chh + gy)
        px0, px1 = X0 + 8.0, X0 + cw - 1.0
        py0, py1 = Yt - chh + 7.0, Yt - 5.0
        Xh = lambda t: px0 + (px1 - px0) * t / 24.0
        Yv = lambda v: py0 + (py1 - py0) * (max(lo, min(hi, v)) - lo) / (hi - lo)
        pg.fill([rect(px0, py0, px1, py1)], (250, 250, 251), 10)
        for b0, b1, col, nm in BK_BANDS:
            if b1 <= lo or b0 >= hi:
                continue
            pg.fill([rect(px0, Yv(b0), px1, Yv(b1))], col, 11)
        st = nice_step(hi - lo, 5)
        v = math.ceil(lo / st) * st
        while v <= hi + 1e-9:
            pg.line([(px0, Yv(v)), (px1, Yv(v))], (214, 214, 220), 0.1, 12)
            pg.label("{:.0f}".format(v), px0 - 1.0, Yv(v) - 0.9, anchor="R")
            v += st
        for t in (0, 6, 12, 18, 24):
            pg.label("%02d:00" % t if t < 24 else "24:00", Xh(t), py0 - 3.6, anchor="C" if 0 < t < 24 else
                     ("L" if t == 0 else "R"))
        summer = sd["key"] == "summer"
        for ser, col, w_ in ((sun, BK_SUN, 0.6 if summer else 0.35), (sha, BK_SHADE, 0.6 if summer else 0.35),
                             (site, BK_MEAN, 0.4 if summer else 0.25)):
            run = []
            for t in range(25):
                if t < 24 and ser[t] is not None:
                    run.append((Xh(t), Yv(ser[t])))
                    continue
                if len(run) >= 2:
                    pg.line(run, col, w_, 30)
                run = []
        pg.line(rect(px0, py0, px1, py1) + [(px0, py0)], INK2, 0.1, 31)
        pg.label(sd["key"], px0, py1 + 1.2, size=9.5, bold=True, colour=bk_hex(MARK_C) if summer else BK_INK)
        for b0, b1, col, nm in BK_BANDS:                   # each band named once, where it shows
            if nm and nm not in named and b0 < hi and b1 > lo and Yv(min(b1, hi)) - Yv(max(b0, lo)) >= 3.2:
                if pg.label(nm, px1 - 0.8, Yv(min(b1, hi)) - 2.6, anchor="R",
                            tries=[(0.0, -2.8, "R"), (-30.0, 0.0, "R")]):
                    named.add(nm)
        if summer:                                          # the three curves named once, on the summer chart
            for ser, nm in ((sun, u"open sun"), (sha, u"street shade"), (site, u"site mean")):
                pts = [(t, v_) for t, v_ in enumerate(ser) if v_ is not None]
                if pts:
                    t, v_ = max(pts, key=lambda p: p[1]) if nm == u"open sun" else pts[len(pts) // 2]
                    pg.around(nm, Xh(t), Yv(v_), 1.2, halo=True)
    leg = [bk_leg("line", BK_SUN, u"Open sun"), bk_leg("line", BK_SHADE, u"Street shade"),
           bk_leg("line", BK_MEAN, u"Site mean")]
    return dict(page=pg, caption=u"Felt temperature through the typical day", scale_den=None, legend=leg)


def bk_a7_side1(S, B, W, H):
    """Comfortable hours by season: the share of the daylight hours with no thermal stress (T8 seasons)."""
    CF = (getattr(S, "env", None) or {}).get("comfort")
    if not CF or not CF.get("year"):
        BK_LOG.append("a7_side1: no comfort results on this run")
        return None
    sh = CF["year"]["share"]
    pg = BkPage(W, H)
    n = len(SEASONS)
    pitch = (H - 2.0) / n
    bh = 0.45 * pitch
    lut = stops_table(COMFORT_SHARE, 0.0, 100.0)
    for i, sd in enumerate(SEASONS):
        v = float(sh[sd["key"]])
        yt = H - 1.0 - i * pitch
        yb = yt - pitch + 1.0
        pg.fill([rect(0.5, yb, W - 0.5, yb + bh)], FAINT, 10)
        pg.fill([rect(0.5, yb, 0.5 + (W - 1.0) * v / 100.0, yb + bh)], lut(v), 11)
        pg.label(u"{} {:.0f} %".format(sd["key"], v), 0.5, yb + bh + 1.4, bold=sd["key"] == "summer")
    return dict(page=pg, caption=u"Comfortable hours by season", scale_den=None, legend=[])


# ------------------------------------------------------------ the booklet step
BK_FRAMES = [("a1_hero", bk_a1_hero), ("a1_side2", bk_a1_side2), ("a2_hero", bk_a2_hero), ("a3_hero", bk_a3_hero),
             ("a3_side1", bk_a3_side1), ("a3_side2", bk_a3_side2), ("a3_side3", bk_a3_side3), ("a4_s2", bk_a4_s2),
             ("a4_s3", bk_a4_s3), ("a5_s1", bk_a5_s1), ("a5_s2", bk_a5_s2), ("a5_s3", bk_a5_s3), ("a5_s4", bk_a5_s4),
             ("a6_s1", bk_a6_s1), ("a6_s2", bk_a6_s2), ("a6_s3", bk_a6_s3), ("a6_s4", bk_a6_s4), ("a7_hero", bk_a7_hero),
             ("a7_side1", bk_a7_side1)]                # every asset key "selinus_board/<block>" of the plan, page order


def booklet_export(S, B, rects):
    """v39: the booklet assets of every frame in BK_FRAMES into output/selinus_board/booklet/ (blocks.json, one PDF per
    frame, results.json, booklet_log.txt) and the site photos into Downloads/Bergama/booklet_images/. A frame that
    cannot be drawn is left out (booklet_log.txt; an error also in the board's log). Returns (done, left out)."""
    del BK_LOG[:]
    BK = BkBlocks(out_folder(), BK_SCRIPT, BK_VERSION)
    done, left = [], []
    for bid, fn in BK_FRAMES:
        W, H = bk_frame("selinus_board/" + bid, *BK_SLOTS[bid])
        try:
            r = fn(S, B, W, H)
            if r is None:
                left.append(bid)
                continue
            r["page"].write(BK.path(bid + ".pdf"))
            BK.drawing(bid, bid + ".pdf", r["page"].labels, r.get("caption", ""), r.get("scale_den"), r.get("legend"))
            done.append(bid)
        except Exception:
            left.append(bid)
            BK_LOG.append("%s: failed\n%s" % (bid, traceback.format_exc()))
            LOG.append("WARNING: booklet frame %s not written (%s); see booklet/booklet_log.txt." % (
                bid, traceback.format_exc().strip().splitlines()[-1]))
    try:
        res = bk_results(S)
        import json as _j
        with open(BK.path("results.json"), "w", encoding="utf-8") as f_:
            _j.dump(res, f_, ensure_ascii=False, indent=1, sort_keys=True)
    except Exception:
        BK_LOG.append("results.json failed\n" + traceback.format_exc())
        LOG.append("WARNING: booklet results.json not written (%s)." % (traceback.format_exc().strip().splitlines()[-1],))
    try:
        bk_photos()
    except Exception:
        BK_LOG.append("photos not copied\n" + traceback.format_exc())
    BK.save()
    with open(BK.path("booklet_log.txt"), "w", encoding="utf-8") as f_:
        f_.write(u"%s booklet assets\nwritten: %s\nleft out: %s\n\n%s\n" % (
            SCRIPT_VERSION, ", ".join(done) or "none", ", ".join(left) or "none", "\n".join(BK_LOG)))
    return done, left


def bk_results(S):
    """The figures this board computes for the booklet's A pages (plan_merged.json: values_from "none"), by key. Every
    value is computed here from the same data and with the same rule as the sheet that prints it."""
    R = {"script": SCRIPT_VERSION, "note": "figures computed by the site board for the booklet (A pages)"}
    rd = lambda v, n=1: None if v is None else round(float(v), n)
    # ---- A1 · readings and land use (draw_legend, page1_readings)
    tot = frame_total(S)
    R["frame_ha"] = rd(tot / 1e4, 2)
    R["frame_w_m"], R["frame_h_m"] = rd(S.F.w, 0), rd(S.F.h, 0)
    R["built_pct_of_frame"] = rd(100.0 * S.built_area / S.frame_area)
    R["void_pct_of_frame"] = rd(100.0 - 100.0 * S.built_area / S.frame_area)
    R["mapped_pct_of_frame"] = rd(100.0 * S.total_area / tot)
    R["homes_pct_of_mapped"] = rd(100.0 * S.area.get("residential", 0.0) / S.total_area)
    P1 = page1_readings(S)
    if P1.get("floors"):
        share, avg, peak = P1["floors"]
        R["floors_mean"] = rd(avg, 2)
        R["floors_one_pct"] = rd(share.get(1, 0.0))
        R["densest_near"] = peak
    fa = sum(S.fabric_area.values()) or 1.0
    R["old_town_pct_of_built_frame"] = rd(100.0 * S.fabric_area.get("traditional", 0.0) / fa)
    SA = getattr(S, "whole", None)
    if SA is not None and getattr(SA, "fabric_area", None):   # plan 01's tile: the whole-file map's footprint
        fa = sum(SA.fabric_area.values()) or 1.0
        R["old_town_pct_of_built_wholefile"] = rd(100.0 * SA.fabric_area.get("traditional", 0.0) / fa)
    R["green_pct_of_frame_mapped"] = rd(P1["green"][0], 2)
    R["green_pct_with_satellite"] = rd(P1["green"][2]) if P1["green"][2] is not None else None
    for k in CAT_ORDER:
        R["landuse_pct_" + k] = rd(100.0 * S.area.get(k, 0.0) / tot)
    for k_, lab, col, a in (getattr(S, "rest", None) or []):
        R["unmapped_pct_" + k_] = rd(100.0 * a / tot)
    # ---- A2 · sky view of the stream bed (stream_sky)
    sky = stream_sky(S)
    if sky:
        lows = sorted(m[2] for m in sky["marks"] if m[3] == "low")
        R["sky_bed_mean_pct"] = rd(100.0 * sky["mean"], 0)
        R["sky_most_enclosed_pct"] = rd(100.0 * lows[0], 0) if lows else None
        R["sky_enclosed_pcts"] = [rd(100.0 * v, 0) for v in lows[1:]]
        R["sky_most_open_pct"] = rd(100.0 * max(m[2] for m in sky["marks"]), 0)
    # ---- A3 · movement, services (movement(), draw_how_people_use_it)
    MV = movement(S) or {}
    if MV.get("rows"):
        R["busiest_street"] = MV["rows"][0]["name"]
        R["busiest_street_index"] = rd(MV["rows"][0]["comb_b"], 0)
    for k_, nm in (("walk_b", "walk"), ("car_b", "drive"), ("comb_b", "combined")):
        if (MV.get("rho") or {}).get(k_) is not None:
            R["spearman_shops_" + nm] = rd(MV["rho"][k_], 2)
    if MV.get("big"):
        R["streets_50m_n"] = len(MV["big"])
    try:
        DG, ctx = diagram_ctx(S)
        n_pl = {}
        for p in ctx.places:
            if S.F.inside(p[0], p[1]):
                n_pl[p[2]] = n_pl.get(p[2], 0) + 1
        for fn_, let, c, lab in WALK_FUN:
            R["places_" + fn_] = n_pl.get(fn_, 0)
    except Exception:
        BK_LOG.append("results: services not counted\n" + traceback.format_exc())
    # ---- A4 · the key question: % of bank length (key_cells)
    etot = sum(S.edge_len.values())
    if etot > 0:
        for name, val, col, phrase in key_cells(S):
            R["bank_%s_pct" % name.lower()] = rd(100.0 * val / etot, 0)
        R["bank_length_m"] = rd(etot, 0)
    env = getattr(S, "env", None) or {}
    # ---- A5 · T1 noise (sheet_sound)
    nm = env.get("noise")
    if nm:
        cells = [c for row in nm["grid"] for c in row if c and c.get("lden") is not None]
        n_out = sum(1 for row in nm["grid"] for c in row if c and c.get("out"))
        ntot = max(1, len(cells) + n_out)
        R["t1_over53_lden_pct"] = rd(100.0 * sum(1 for c in cells if c["lden"] > 53.0) / ntot, 0)
        R["t1_over45_night_pct"] = rd(100.0 * sum(1 for c in cells if c["night"] is not None and c["night"] > 45.0)
                                      / ntot, 0)
    # ---- T2 surface heat, summer (heat_scale, lst_tiles, heat_canopy_inset)
    if env.get("lst"):
        hsc = heat_scale(S, "summer")
        if hsc:
            R["t2_summer_median_c"] = rd(hsc[1], 2)
        tl = dict((t[1], t[2]) for t in lst_tiles(S, "summer"))
        if "AT THE STREAM" in tl:
            R["t2_summer_stream_vs_150m_c"] = rd(float(tl["AT THE STREAM"].split()[0]), 1)
            R["t2_summer_within50m_c"] = rd(float(tl["WITHIN 50 m OF STREAM"].split()[0]), 1)
            R["t2_summer_beyond150m_c"] = rd(float(tl["BEYOND 150 m"].split()[0]), 1)
        hs = (seam_pack().get("heat") or {}).get("seasons", {}).get("summer")
        pts = (hs or {}).get("points") or []
        if pts:
            v0 = [t for c, t in pts if c <= 0.0]
            v25 = [t for c, t in pts if 0.25 <= c < 1.01]
            R["t2_summer_no_crowns_c"] = rd(sum(v0) / len(v0), 2) if v0 else None
            R["t2_summer_dense_crowns_c"] = rd(sum(v25) / len(v25), 2) if v25 else None
    # ---- T3 shade, the mean day of the year (shade_tiles)
    if env.get("shade"):
        it = [i_ for i_ in shade_items(S) if i_["key"] == "year"][0]
        tl = dict((t[1], t[2]) for t in shade_tiles(S, it))
        R["t3_year_mean_shade_h"] = tl.get("OPEN GROUND · MEAN SHADE", "").replace(" h", "") or None
        R["t3_year_share_of_daylight_pct"] = rd(float(tl["SHARE OF THE DAYLIGHT"].split()[0]), 0) \
            if "SHARE OF THE DAYLIGHT" in tl else None
        R["t3_year_shaded_over_half_pct"] = rd(float(tl["SHADED > HALF THE DAY"].split()[0]), 0) \
            if "SHADED > HALF THE DAY" in tl else None
        R["t3_year_within30m_stream_shade_h"] = tl.get("WITHIN 30 m OF STREAM", "").replace(" h", "") or None
    # ---- T4 radiation, summer (rad_tiles)
    if env.get("rad"):
        tl = dict((t[1], t[2]) for t in rad_tiles(S, "summer"))
        for key, lab in (("roof_mean", "ROOFS · MEAN kWh/m²·day"), ("ground_mean", "GROUND · MEAN kWh/m²·day"),
                         ("ground_lowest10", "LOWEST 10 % GROUND · BELOW"), ("open_flat", "OPEN FLAT GROUND")):
            if lab in tl:
                R["t4_summer_%s_kwh" % key] = rd(float(tl[lab]), 2)
    CF = env.get("comfort")
    if CF:
        names = ("N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW")
        for sd in SEASONS:
            c = CF["seasons"][sd["key"]]
            k = sd["key"]
            # ---- T5 wind (sheet_wind)
            dir_from, share = prevailing(c)
            R["t5_%s_from" % k] = names[int(round(dir_from / 22.5)) % 16]
            R["t5_%s_from_pct" % k] = rd(100.0 * share, 0)
            vals = c["uped"][np.isfinite(c["uped"])]
            open_v = c["u10_mean"] * PED_WIND
            R["t5_%s_open_ms" % k] = rd(open_v, 2)
            R["t5_%s_site_mean_ms" % k] = rd(float(vals.mean()), 2) if vals.size else None
            R["t5_%s_sheltered_pct" % k] = rd(100.0 * float((vals < 0.5 * open_v).mean()), 0) if vals.size else None
            # ---- T6 air (sheet_air)
            ta = c["ta"][np.isfinite(c["ta"])]
            if ta.size:
                R["t6_%s_air_min_c" % k], R["t6_%s_air_max_c" % k] = rd(float(ta.min()), 2), rd(float(ta.max()), 2)
            # ---- T7 felt (sheet_felt)
            u = c["utci"][np.isfinite(c["utci"])]
            R["t7_%s_felt_mean_c" % k] = rd(float(u.mean()), 2) if u.size else None
            R["t7_%s_felt_sun_c" % k] = rd(c["utci_sun"], 2)
            R["t7_%s_felt_shade_c" % k] = rd(c["utci_shade"], 2)
        # ---- T8 comfortable hours (sheet_comfort_year)
        Yr = CF.get("year")
        if Yr:
            v = Yr["comfort"][np.isfinite(Yr["comfort"])]
            v18 = Yr["comfort18"][np.isfinite(Yr["comfort18"])]
            R["t8_year_comfortable_pct"] = rd(float(v.mean()), 0) if v.size else None
            R["t8_best_spot_pct"] = rd(float(v.max()), 0) if v.size else None
            R["t8_worst_spot_pct"] = rd(float(v.min()), 0) if v.size else None
            R["t8_near_comfort_18_26_pct"] = rd(float(v18.mean()), 0) if v18.size else None
            for sd in SEASONS:
                R["t8_%s_comfortable_pct" % sd["key"]] = rd(Yr["share"][sd["key"]], 0)
    return R


def bk_photos():
    """The site photos of the data pack (photo_files, numbered as on plan 01) as booklet_images/photo_<n>.jpg."""
    import shutil
    d = os.path.join(BERGAMA_DIR, "booklet_images")
    if not os.path.isdir(d):
        os.makedirs(d)
    n = 0
    for i, (p, it) in enumerate(photo_files(os.path.join(pdf_folder(), "_site_photos"))):
        shutil.copyfile(p, os.path.join(d, "photo_%d.jpg" % (i + 1)))
        n += 1
    BK_LOG.append("photos: %d copied to %s as photo_1..%d.jpg" % (n, d, n))
