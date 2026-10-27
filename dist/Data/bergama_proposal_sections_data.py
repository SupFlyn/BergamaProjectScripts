# Built-in data of bergama_proposal_sections (made by tools/build.py from src/bergama_proposal_sections/data/; do not edit by hand)

#@@ SKETCH_SRC
SKETCH_SRC = r'''# The idea sketches of pr1_drawings v3.1 (concept sections, SKETCH style), run in their own namespace: pr1 baked them
# into Rhino; here the same calls make page items. The draw order is pr1's (bake order plus its lifts Z_*).
import math
ZP = []
ORDER = [0]
FORM = "A"
PEOPLE = True
NODE = None                                          # set by the board: the element numbers
CITE = None                                          # v3: set by the board: a source's number "[n]" (footer key)
ORIGIN = (0.0, 0.0)                                  # pr1 placed the sketches beside the site map; here at 0
TXT_K = [1.0]                                        # v7: every text (and its pictogram) at this multiple of its size; set by
                                                      # the board so the smallest word prints >= 7 pt on the one booklet page
GROUP = [0]                                          # v7: label group of the items being put (0: none, < 0: fixed, e.g. numbers)
NEXT_G = [0]                                         # v7: last label group number given out


def _hexc(c):
    return "%02X%02X%02X" % tuple(c)


def _put(item, z):
    ORDER[0] += 1
    ZP.append((ORDER[0] + z, ORDER[0], item, GROUP[0]))   # v7: + the label group (the board keeps labels apart)


def _group():
    """v7: open a new label group unless one is open. Returns True if this call opened it (then it closes it)."""
    if GROUP[0]:
        return False
    NEXT_G[0] += 1
    GROUP[0] = NEXT_G[0]
    return True


def P(o, x, y):
    return (o[0] + x, o[1] + y)


def add_polyline(q):
    out = []
    for p in q:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-6:
            out.append((p[0], p[1]))
    return out if len(out) >= 2 else None


def keep(obj, sub, colour, width=None, dashed=False, alpha=None, z=0):
    if obj is None:
        return None
    _put(("line", obj, _hexc(colour), width if width else 0.13, [1.0, 0.7] if dashed else None, 1), z)
    return obj


def pline(o, pts, sub, colour, width=0.18, closed=False, dashed=False, z=0):
    q = [P(o, x, y) for x, y in pts]
    if closed and q[0] != q[-1]:
        q.append(q[0])
    return keep(add_polyline(q), sub, colour, width, dashed, z=z)


def fill(o, pts, sub, colour, alpha=None, boundary=True, z=0, hand_=None):
    if HAND[0] if hand_ is None else hand_:
        pts = hand_ring(pts, sub)
        boundary = False
    ring = [P(o, x, y) for x, y in pts]
    if len(ring) < 3:
        return None
    _put(("poly", [ring], _hexc(colour), None, 0.1, None, None, alpha), z)
    if boundary:
        pline(o, pts, sub, colour, 0.13, closed=True, z=z)
    return ring


def hatch_lines(o, pts, sub, colour, spacing=1.6, angle=45.0, width=None):
    width = LW_HATCH if width is None else width
    for p0, p1 in clip_segments(pts, spacing, angle):
        keep([P(o, *p0), P(o, *p1)], sub, colour, width)


def text(o, s, x, y, size_pt, colour=None, sub="text", just="left", bold=False, mask=None):
    colour = INK if colour is None else colour
    h = size_pt * 0.353 * TXT_K[0]
    own = _group()                                    # v7: one text (all its lines) = one label group
    for i, ln in enumerate(s.split("\n")):
        if ln.strip():
            q = P(o, x, y - i * h * 1.35)
            _put(("text", ln, q[0], q[1], h, _hexc(colour), bold, {"left": "L", "right": "R"}.get(just, "C"), None,
                  _hexc(mask) if mask else None), Z_TEXT)      # pr1's text mask: a halo in its colour
    if own:
        GROUP[0] = 0


def _smooth(o, pts):
    """A Catmull-Rom curve through the points (pr1: Rhino's interpolated curve), as a fine polyline."""
    q = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(8):
            t = k / 8.0
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    out.append(pts[-1])
    return add_polyline([P(o, x, y) for x, y in out])


def hx(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

INK, INK2 = hx("4A3F35"), hx("847E75")
SOIL, STONE, ROAD = hx("CDBF9F"), hx("A4A1A3"), hx("3A3A3A")
W_SUM, W_WIN, W_EXT = hx("A9C3CC"), hx("7FA7B8"), hx("5C7A86")
REED, ACCENT, HERITAGE, WHITE = hx("89986A"), hx("BC6F45"), hx("8B2D2D"), (255, 255, 255)
CELL, FARM = hx("DFE6CF"), hx("E7E0C8")
def mix(a, b, t):
    """Plain RGB mix of two palette colours (t = share of b), for hatch and outline tones only."""
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

SOIL_HATCH = mix(SOIL, INK, 0.30)      # earth hatch over the soil poché
STONE_HATCH = mix(STONE, INK, 0.35)    # masonry hatch, K4 bridge behind
REED_HEAD = mix(REED, INK, 0.35)       # reed plumes
FIGURE = INK2                          # scale figures
# line weights (print width, mm): what the section cuts is heaviest, what is seen beyond it is thin
LW_CUT, LW_PROFILE, LW_EDGE, LW_BEYOND, LW_FINE, LW_HATCH = 0.50, 0.35, 0.25, 0.13, 0.09, 0.05
Z_TREE, Z_LINE, Z_PEOPLE, Z_TEXT = 300000, 400000, 600000, 900000   # draw-order lifts: trees, lines, people, texts
def clip_segments(pts, spacing, angle):
    """The pieces of parallel lines (spacing, angle in degrees) that lie inside a closed outline."""
    segs = []
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    r = [(x * ca + y * sa, -x * sa + y * ca) for x, y in pts]       # outline turned so the hatch runs along x
    if r[0] != r[-1]:
        r.append(r[0])
    ys = [p[1] for p in r]
    k = int(math.floor(min(ys) / spacing)) + 1
    while k * spacing < max(ys):
        yy = k * spacing
        xs = sorted(x1 + (yy - y1) * (x2 - x1) / (y2 - y1) for (x1, y1), (x2, y2) in zip(r[:-1], r[1:])
                    if (y1 <= yy < y2) or (y2 <= yy < y1))
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 0.05:
                p0 = (xs[i] * ca - yy * sa, xs[i] * sa + yy * ca)
                p1 = (xs[i + 1] * ca - yy * sa, xs[i + 1] * sa + yy * ca)
                segs.append((p0, p1))
        k += 1
    return segs

def notch(g, cuts):
    """Ground outline g with rectangular basins cut into its level stretches: cuts = [(x0, x1, y_top, depth)]."""
    out = list(g)
    for x0, x1, y, d in cuts:
        for i in range(len(out) - 1):
            (ax, ay), (bx, by) = out[i], out[i + 1]
            if abs(ay - y) < 1e-9 and abs(by - y) < 1e-9 and min(ax, bx) <= x0 and x1 <= max(ax, bx):
                ins = [(x0, y), (x0, y - d), (x1, y - d), (x1, y)]
                ins = ins if ax < bx else ins[::-1]
                ins = [p for p in ins if p != out[i] and p != out[i + 1]]
                out[i + 1:i + 1] = ins
                break
    return out

def surface_y(surface, x):
    """Height of the ground surface at x (on a vertical step: the lower of the two)."""
    ys = [ay + (by - ay) * (x - ax) / (bx - ax) for (ax, ay), (bx, by) in zip(surface[:-1], surface[1:])
          if bx != ax and min(ax, bx) <= x <= max(ax, bx)]
    return min(ys) if ys else None

def surface_between(surface, x0, x1, dy=0.0):
    """The surface from x0 to x1 (steps inside kept, risers at the two ends dropped), lifted by dy."""
    out = []
    for (ax, ay), (bx, by) in zip(surface[:-1], surface[1:]):
        if max(ax, bx) < x0 or min(ax, bx) > x1:
            continue
        if ax == bx:
            seg = [(ax, ay), (bx, by)]
        else:
            seg = []
            for x in (max(min(ax, bx), x0), min(max(ax, bx), x1)) if ax < bx else (min(max(ax, bx), x1), max(min(ax, bx), x0)):
                seg.append((x, ay + (by - ay) * (x - ax) / (bx - ax)))
        for q in seg:
            if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > 1e-9:
                out.append(q)
    while len(out) > 2 and out[0][0] == out[1][0]:
        out.pop(0)
    while len(out) > 2 and out[-1][0] == out[-2][0]:
        out.pop()
    return [(x, y + dy) for x, y in out]

def reeds(o, x0, x1, y, h=3.5, plan=False):
    """Reed clumps at v2.8's spacing and height: a fan of thin arched blades of mixed height, a plume on every third
    clump. plan=True (form plans): a small tuft of radiating leaves seen from above."""
    rnd = _tree_rand(x0 + 0.37 * x1, y)
    n = max(3, int((x1 - x0) / 1.6))
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        if plan:
            m = 6 + int(rnd() * 3)
            for j in range(m):
                t = 6.283 * (j + 0.4 * rnd()) / m
                L = h * 0.38 * (0.6 + 0.4 * rnd())
                keep([P(o, x, y), P(o, x + L * math.cos(t), y + L * math.sin(t))], "planting", REED, LW_FINE)
            continue
        nb = 5 + int(rnd() * 3)
        tall = None
        for j in range(nb):
            s = (j / (nb - 1.0) - 0.5) * 2.0 + (rnd() - 0.5) * 0.35       # -1 .. 1: leaning left .. right
            hh = h * (0.62 + 0.38 * rnd()) * (1.0 - 0.18 * abs(s))
            pts = [(x + 0.12 * s + s * hh * 0.42 * t * t, y + hh * (t - 0.10 * abs(s) * t * t)) for t in (0.0, 0.35, 0.7, 1.0)]
            keep(_smooth(o, pts), "planting", REED, LW_FINE)
            if tall is None or hh > tall[0]:
                tall = (hh, pts)
        if i % 3 == 1 and tall:                    # plume along the tallest blade's tip
            (ax, ay), (bx, by) = tall[1][-2], tall[1][-1]
            L = math.hypot(bx - ax, by - ay) or 1.0
            ux, uy = (bx - ax) / L, (by - ay) / L
            ln, wd = 0.30 * h, 0.05 * h
            cx, cy = bx + ux * ln * 0.5, by + uy * ln * 0.5
            fill(o, [(bx, by), (cx - uy * wd, cy + ux * wd), (bx + ux * ln, by + uy * ln), (cx + uy * wd, cy - ux * wd)],
                 "planting", REED_HEAD, boundary=False)

def bank(p, q, n=24):
    """Edge where the project meets the water: S-curve in form A, one straight facet in form B."""
    if FORM == "B":
        return [p, q]
    out = []
    for i in range(n):
        t = i / (n - 1.0)
        s = (1 - math.cos(t * math.pi)) / 2
        out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * s))
    return out

def road(o, x0, x1, y, label, ly=None, mask=None):
    fill(o, [(x0, y), (x1, y), (x1, y + 1.3), (x0, y + 1.3)], "road", ROAD)
    text(o, label, x0 + 1, ly if ly is not None else y - 2.5, 5.0, ROAD, "road", mask=mask)

def level_mark(o, x, y, colour, sub):
    """Level sign: a small open triangle standing point-down on the level line."""
    pline(o, [(x - 1.0, y + 1.7), (x + 1.0, y + 1.7), (x, y)], sub, colour, LW_BEYOND, closed=True, z=Z_LINE)

HAND_AMP = 0.18          # mm: sideways wobble of a hand line
HAND_WAV = 7.0           # mm: length of one wobble
HAND_OVER = 1.1          # mm: how far a stroke runs past its corner
HAND_FONT = ["Ink Free", "Segoe Print", "Comic Sans MS"]   # first one installed (Windows 10/11 ship Ink Free)
PEN_HAIR, PEN_FINE, PEN_MED, PEN_BOLD = 0.13, 0.20, 0.40, 0.70   # masterplan v9 pens (mm)
SKINK = hx("1E1E1E")                                 # fine-liner black: the line that carries the idea
SUN, SUN_RAY = hx("E8C64A"), hx("C9A227")           # the dry summer (Aras): marker yellow
HAND = [False]                                       # True while a part is drawn by hand (form plans: pline / fill wobble)
HAND_TEXT = [False]                                  # True while texts take the hand font and drop their masks
KHAKI, PAPER, BG_ = hx("BCB794"), hx("F1EDDF"), hx("E6E0C8")
SEC_POCHE = mix(KHAKI, PAPER, 0.62)                  # board: the cut ground
SEC_POCHE_BAND = mix(SEC_POCHE, KHAKI, 0.45)          # the band just under the surface, a little deeper
SEC_PAVE = mix(hx("BC6F45"), BG_, 0.12)              # board: walkable edge, terracotta
SEC_CHANNEL_HATCH = hx("3E7DAE")                     # board: the stream bed's blue hatch
SITE_WATER, SITE_WATER_D, SITE_FLOOD = hx("7FA4B3"), hx("5E8494"), hx("B4CBD2")   # board CAT water, BLUE_D, BLUE_L
FLOOD_WASH, FLOOD_ALPHA = hx("4F9BD9"), 0.09         # the design flood's reach up to Q500: one clear blue, see-through
                                                      # and so faint it takes a moment to see (Nil 17:59: "really really faint blue,
                                                      # almost indistinguishable ... should need a focus to see"); raise FLOOD_ALPHA = stronger
SITE_PEOPLE = mix(hx("7A6E60"), BG_, 0.1)            # board: SA_STYLE_BOARD people
SITE_TREE = (hx("B2C484"), hx("8CA466"), hx("688052"))   # board SA_TREE_PAL["tree"]: light, mid, shadow
SITE_TRUNK = hx("6E625A")                            # board SA_TRUNK
HOUSE_WALL, HOUSE_ROOF = hx("D9B98C"), hx("A86A55")  # board TYPO["traditional"] tone, TYPO_ROOF_C
SA_FIGS = [                                          # board SA_FIGS (m, 1.75 m tall), SA_HEAD
    [(-0.10, 0.0), (-0.06, 0.0), (-0.03, 0.82), (0.03, 0.82), (0.06, 0.0), (0.10, 0.0), (0.12, 0.85), (0.16, 1.38),
     (0.10, 1.47), (0.05, 1.50), (0.05, 1.53), (-0.05, 1.53), (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.12, 0.85)],
    [(-0.30, 0.0), (-0.24, 0.0), (-0.02, 0.78), (0.18, 0.0), (0.25, 0.0), (0.11, 0.86), (0.18, 1.12), (0.12, 1.40),
     (0.06, 1.48), (0.05, 1.53), (-0.05, 1.53), (-0.07, 1.47), (-0.14, 1.38), (-0.20, 1.10), (-0.12, 0.86)],
    [(-0.20, 0.0), (0.20, 0.0), (0.13, 0.62), (0.11, 1.08), (0.15, 1.36), (0.09, 1.45), (0.05, 1.49), (0.05, 1.52),
     (-0.05, 1.52), (-0.05, 1.49), (-0.09, 1.45), (-0.15, 1.36), (-0.11, 1.08), (-0.13, 0.62)],
    [(-0.11, 0.0), (-0.06, 0.0), (-0.02, 0.80), (0.04, 0.80), (0.08, 0.0), (0.13, 0.0), (0.12, 0.86), (0.30, 0.86),
     (0.30, 0.55), (0.40, 0.55), (0.40, 0.95), (0.17, 1.38), (0.10, 1.47), (0.05, 1.51), (0.05, 1.53), (-0.05, 1.53),
     (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.13, 0.86)],
]
SA_HEAD = (0.0, 1.64, 0.105)

import zlib as _zlib, random as _random
def _seed(*parts):
    return _zlib.crc32(repr([round(float(v), 2) if isinstance(v, float) else v for v in parts]).encode("utf-8")) & 0x7fffffff

def _densify(P, step):
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / step)))
        out += [(a[0] + (b[0] - a[0]) * k / float(n), a[1] + (b[1] - a[1]) * k / float(n)) for k in range(1, n + 1)]
    return out

def _normals(a):
    out = []
    for i in range(len(a)):
        p, q = a[max(0, i - 1)], a[min(len(a) - 1, i + 1)]
        d = math.hypot(q[0] - p[0], q[1] - p[1]) or 1e-12
        out.append((-(q[1] - p[1]) / d, (q[0] - p[0]) / d))
    return out

def _noise(n, step, wav, rnd):
    """n values of smooth noise (std about 1), features about wav long (masterplan smooth_noise)."""
    k = max(2, int(math.ceil(n * step / wav)) + 3)
    ctrl = [rnd.gauss(0.0, 1.0) for _ in range(k)]
    out = []
    for j in range(n):
        x = j * step / wav
        i = min(int(x), k - 2)
        f = x - i
        f = f * f * (3 - 2 * f)
        out.append(ctrl[i] * (1 - f) + ctrl[i + 1] * f)
    return out

def hand(P, amp, wav, seed, closed=False, over=0.0):
    """A polyline as a hand draws it (masterplan hand_line): smooth sideways wobble of about amp (at most 2.2 amp),
    an overshoot of `over` at both ends of an open line; a closed ring starts at a random point."""
    a = [(float(p[0]), float(p[1])) for p in P]
    if len(a) < 2:
        return a
    rnd = _random.Random(seed)
    step = max(wav / 6.0, 1e-6)
    if closed:
        if math.hypot(a[0][0] - a[-1][0], a[0][1] - a[-1][1]) < 1e-9:
            a = a[:-1]
        k = rnd.randrange(len(a))
        a = a[k:] + a[:k] + [a[k]]
    a = _densify(a, step)
    if over > 0 and not closed:
        (x0, y0), (x1, y1) = a[0], a[1]
        d = math.hypot(x1 - x0, y1 - y0) or 1e-12
        s = (x0 - (x1 - x0) / d * over, y0 - (y1 - y0) / d * over)
        (x0, y0), (x1, y1) = a[-1], a[-2]
        d = math.hypot(x1 - x0, y1 - y0) or 1e-12
        a = [s] + a + [(x0 - (x1 - x0) / d * over, y0 - (y1 - y0) / d * over)]
    if amp > 0:
        w = [max(-2.2, min(2.2, v)) * amp for v in _noise(len(a), step, wav, rnd)]
        a = [(p[0] + n[0] * v, p[1] + n[1] * v) for p, n, v in zip(a, _normals(a), w)]
    return a

def _strokes(P, closed, turn=28.0):
    """A polyline split at its corners, as a hand draws it: one stroke per straight run."""
    P = list(P) + ([P[0]] if closed and P[0] != P[-1] else [])
    out = [[P[0]]]
    for i in range(1, len(P) - 1):
        a, b, c = P[i - 1], P[i], P[i + 1]
        t1, t2 = math.atan2(b[1] - a[1], b[0] - a[0]), math.atan2(c[1] - b[1], c[0] - b[0])
        out[-1].append(b)
        if abs((math.degrees(t2 - t1) + 180) % 360 - 180) > turn:
            out.append([b])
    out[-1].append(P[-1])
    return [s for s in out if len(s) > 1]

def _crosses(ring):
    """True when a closed ring crosses itself (a hatch from it would fail or fill wrongly)."""
    q = list(ring) + ([ring[0]] if ring[0] != ring[-1] else [])
    E = list(zip(q[:-1], q[1:]))
    box = [(min(a[0], b[0]), max(a[0], b[0]), min(a[1], b[1]), max(a[1], b[1])) for a, b in E]

    def o_(p, r, t):
        return (r[0] - p[0]) * (t[1] - p[1]) - (r[1] - p[1]) * (t[0] - p[0])
    m = len(E)
    for i in range(m):
        a, b = E[i]
        bi = box[i]
        for j in range(i + 2, m):
            if i == 0 and j == m - 1:
                continue
            bj = box[j]
            if bi[1] < bj[0] or bj[1] < bi[0] or bi[3] < bj[2] or bj[3] < bi[2]:
                continue
            c, d = E[j]
            if o_(a, b, c) * o_(a, b, d) < -1e-12 and o_(c, d, a) * o_(c, d, b) < -1e-12:
                return True
    return False

def hand_ring(pts, sub, amp=HAND_AMP, wav=HAND_WAV):
    """A closed outline drawn by hand; where the wobble would make it cross itself (narrow or sharp shapes), a smaller
    wobble, else the true outline."""
    sd = _seed(pts[0][0], pts[0][1], len(pts), sub)
    for k in (1.0, 0.5, 0.25):
        r = hand(pts, amp * k, wav, sd, closed=True)
        if not _crosses(r):
            return r
    return list(pts)

def sketch(o, pts, sub, colour, width=0.25, closed=False, over=HAND_OVER, amp=HAND_AMP, retrace=True, z=0,
           dashed=False):
    """Fine-liner line: each straight run its own stroke, wobbling and running past the corners; long runs are
    traced a second time, lighter and not quite end to end, as a sketch is."""
    for k, s in enumerate(_strokes(pts, closed)):
        sd = _seed(s[0][0], s[0][1], s[-1][0], s[-1][1], k, sub)
        q = hand(s, amp, HAND_WAV, sd, over=over)
        keep(add_polyline([P(o, *p) for p in q]), sub, colour, width, dashed, z=z)
        L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(s[:-1], s[1:]))
        if retrace and not dashed and L > 6.0:
            rnd = _random.Random(sd + 7)
            q = hand(s, amp * 1.6, HAND_WAV * 0.8, sd + 11, over=over * 0.5)
            i0, i1 = int(len(q) * 0.15 * rnd.random()), len(q) - int(len(q) * 0.25 * rnd.random())
            if i1 - i0 > 1:
                keep(add_polyline([P(o, *p) for p in q[i0:i1]]), sub, colour, width * 0.45, z=z)

def wash(o, poly, sub, colour, alpha=0.5, z=0):
    """Watercolour wash: a see-through fill whose edge wobbles a little past the true outline."""
    ring = hand_ring(poly, sub, HAND_AMP * 1.8, HAND_WAV * 1.6)
    return fill(o, ring, sub, colour, alpha=alpha, boundary=False, z=z, hand_=False)

def marker(o, poly, sub, colour, angle=55.0, spacing=0.75, thick=0.62, alpha=0.55, base=0.22, z=0):
    """Marker fill: parallel strokes laid side by side at a slant, each a little longer or shorter than the shape
    (and slightly turned), over a faint wash of the same colour: the key element of a sketch (example 4)."""
    if base:
        wash(o, poly, sub, colour, base, z)
    rnd = _random.Random(_seed(poly[0][0], poly[0][1], angle, sub))
    for p0, p1 in clip_segments(poly, spacing, angle):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        if L < 0.2:
            continue
        ux, uy = dx / L, dy / L
        a0, a1 = (rnd.random() - 0.35) * 0.9, (rnd.random() - 0.35) * 0.9
        tw = (rnd.random() - 0.5) * 0.35
        s = (p0[0] - ux * a0, p0[1] - uy * a0)
        e = (p1[0] + ux * a1 - uy * tw, p1[1] + uy * a1 + ux * tw)
        nx, ny = -uy * thick / 2, ux * thick / 2
        fill(o, [(s[0] + nx, s[1] + ny), (e[0] + nx, e[1] + ny), (e[0] - nx, e[1] - ny), (s[0] - nx, s[1] - ny)],
             sub, colour, alpha=alpha, boundary=False, z=z, hand_=False)

def band(surface, x0, x1, depth):
    """Polygons of a band `depth` under the ground surface from x0 to x1 (split at vertical steps)."""
    seg = surface_between(surface, x0, x1)
    pieces, cur = [], [seg[0]] if seg else []
    for q in seg[1:]:
        if abs(q[0] - cur[-1][0]) < 1e-9:
            pieces.append(cur)
            cur = [q]
        else:
            cur.append(q)
    if cur:
        pieces.append(cur)
    return [pc + [(x, y - depth) for x, y in pc[::-1]] for pc in pieces if len(pc) > 1]

def under_level(surface, x0, x1, level):
    """The space between the ground and a level, x0..x1 (what that level puts under water)."""
    bed = [(x, min(level, y)) for x, y in surface_between(surface, x0, x1)]
    return [(x0, level), (x1, level)] + bed[::-1] if len(bed) > 1 else None

def hand_arrow(o, a, b, colour, sub="arrows", width=0.55, head=2.2, z=Z_LINE, bend=0.0):
    """Link arrow in the masterplan v9 manner (head barbs at 38 deg), drawn as filled marker shapes so it reads at
    every zoom and in the viewport, where print widths do not show (Nil 18 Oct 17:55: "the outflow drainage is gone"):
    a hand-wobbled shaft `width` wide that tapers a little towards the tip (bend > 0 bows it), and a solid head."""
    pts = [a, b]
    if bend:
        m = ((a[0] + b[0]) / 2.0 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2.0 + (b[0] - a[0]) * bend)
        pts = [(a[0] * (1 - t) ** 2 + 2 * m[0] * t * (1 - t) + b[0] * t * t, a[1] * (1 - t) ** 2 + 2 * m[1] * t * (1 - t) + b[1] * t * t)
               for t in [i / 24.0 for i in range(25)]]
    t = math.atan2(b[1] - pts[-2][1], b[0] - pts[-2][0])
    hl = head * math.cos(math.radians(38))                 # the head's length along the shaft
    L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts[:-1], pts[1:]))
    shaft, acc = [pts[0]], 0.0
    for p, q in zip(pts[:-1], pts[1:]):
        d = math.hypot(q[0] - p[0], q[1] - p[1])
        if acc + d >= L - hl * 0.7:
            f = (L - hl * 0.7 - acc) / (d or 1e-12)
            shaft.append((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f))
            break
        shaft.append(q)
        acc += d
    sh = hand(shaft, HAND_AMP * 0.5, HAND_WAV, _seed(a[0], a[1], b[0], b[1], sub))
    nm = _normals(sh)
    n = len(sh)
    w_ = [width * (1.0 - 0.3 * i / max(1, n - 1)) / 2.0 for i in range(n)]
    left = [(p[0] + v[0] * w, p[1] + v[1] * w) for p, v, w in zip(sh, nm, w_)]
    right = [(p[0] - v[0] * w, p[1] - v[1] * w) for p, v, w in zip(sh, nm, w_)]
    fill(o, left + right[::-1], sub, colour, boundary=False, z=z, hand_=False)
    tip = (b[0] + math.cos(t) * 0.2, b[1] + math.sin(t) * 0.2)
    wings = [(b[0] - head * math.cos(t + sg * math.radians(38)), b[1] - head * math.sin(t + sg * math.radians(38))) for sg in (1, -1)]
    notch_ = (b[0] - hl * 0.7 * math.cos(t), b[1] - hl * 0.7 * math.sin(t))
    fill(o, [tip, wings[0], notch_, wings[1]], sub, colour, boundary=False, z=z, hand_=False)

def sun(o, x, y, r=2.2):
    """The dry summer: a marker-yellow sun with short hand rays (as in Nil's SNFCC sketch)."""
    disc_ = [(x + r * math.cos(6.283 * i / 20), y + r * math.sin(6.283 * i / 20)) for i in range(20)]
    wash(o, disc_, "sun", SUN, 0.85, z=Z_LINE)
    sketch(o, disc_, "sun", SKINK, PEN_FINE, closed=True, over=0.0, amp=0.08, retrace=False, z=Z_LINE)
    for k in range(9):
        t = 6.283 * (k + 0.3) / 9
        sketch(o, [(x + 1.45 * r * math.cos(t), y + 1.45 * r * math.sin(t)), (x + 2.1 * r * math.cos(t), y + 2.1 * r * math.sin(t))],
               "sun", SKINK, PEN_FINE, over=0.0, amp=0.03, retrace=False, z=Z_LINE)

def cloud_rain(o, x, y, r=1.0):
    """v3: the wet winter, a hand cloud with three rain strokes, centred at (x, y)."""
    pts = []
    for i in range(28):
        a = 6.283 * i / 28
        k = 1.0 + 0.24 * max(0.0, math.sin(a)) * abs(math.sin(3 * a))
        pts.append((x + 1.6 * r * math.cos(a) * k, max(y - 0.5 * r, y + 0.85 * r * math.sin(a) * k)))
    wash(o, pts, "season", SITE_FLOOD, 0.85, z=Z_LINE)
    sketch(o, pts, "season", SKINK, PEN_FINE, closed=True, over=0.0, amp=0.05, retrace=False, z=Z_LINE)
    for dx in (-0.8, 0.0, 0.8):
        sketch(o, [(x + dx * r, y - 0.8 * r), (x + dx * r - 0.35 * r, y - 1.8 * r)], "season", SITE_WATER_D, PEN_FINE,
               over=0.0, amp=0.02, retrace=False, z=Z_LINE)

def failsafe_mark(o, x, y, r=1.4):
    """v3: the fail-safe mark, an accent ring with a step and the water spilling over it."""
    ring = [(x + r * math.cos(6.283 * i / 20), y + r * math.sin(6.283 * i / 20)) for i in range(20)]
    sketch(o, ring, "fail-safe", ACCENT, PEN_FINE, closed=True, over=0.0, amp=0.05, retrace=False, z=Z_LINE)
    sketch(o, [(x - 0.75 * r, y + 0.3 * r), (x - 0.1 * r, y + 0.3 * r), (x - 0.1 * r, y - 0.45 * r), (x + 0.75 * r, y - 0.45 * r)],
           "fail-safe", SKINK, PEN_FINE, over=0.0, amp=0.03, retrace=False, z=Z_LINE)
    hand_arrow(o, (x - 0.55 * r, y + 0.55 * r), (x + 0.25 * r, y - 0.15 * r), ACCENT, width=0.16, head=0.55, bend=-0.3)

def keyed(o, kind, s, x, y, size_pt, colour=None, sub="text", mask=None):
    """v3: a keyword callout led by a hand pictogram at its first line: "winter" (cloud and rain), "summer" (the
    sun) or "failsafe". The text starts a little to the right of x."""
    h = size_pt * 0.353 * TXT_K[0]
    own = _group()                                    # v7: the pictogram and its words move together
    cx, cy = x + 1.1 * h, y + 0.36 * h
    if kind == "winter":
        cloud_rain(o, cx, cy + 0.15 * h, 0.5 * h)
    elif kind == "summer":
        sun(o, cx, cy, 0.36 * h)
    elif kind == "failsafe":
        failsafe_mark(o, cx, cy, 0.62 * h)
    text(o, s, x + 2.4 * h, y, size_pt, colour, sub, mask=mask)
    if own:
        GROUP[0] = 0

def tick_dim(o, x, y0, y1, colour=INK2):
    """Sketch dimension: a vertical line with slashed ticks at both ends (example 4); no figure."""
    sketch(o, [(x, y0), (x, y1)], "dimensions", colour, LW_BEYOND, over=0.9, retrace=False, z=Z_LINE)
    for y in (y0, y1):
        sketch(o, [(x - 0.9, y - 0.9), (x + 0.9, y + 0.9)], "dimensions", colour, LW_EDGE, over=0.0, retrace=False, z=Z_LINE)

def sketch_ground(o, g, sub="ground"):
    """Ground: the board's poché, solid (a see-through ground shows the viewport through it and the band under the
    surface then reads as a gap, Nil 18 Oct 17:46), a slightly deeper band under the surface, and short earth strokes
    just under the line (the surface line itself: drawn by the caller)."""
    surf = g[1:-1]
    wash(o, g, sub, SEC_POCHE, None)
    floor = min(p[1] for p in g)
    for pc in band(surf, surf[0][0], surf[-1][0], 3.0):
        pc = [(x, max(floor, y)) for x, y in pc]           # never below the drawn ground (low-flow channel)
        if not _crosses(pc):
            wash(o, pc, sub, SEC_POCHE_BAND, None)
    rnd = _random.Random(_seed(surf[0][0], surf[-1][0], len(surf)))
    for (ax, ay), (bx, by) in zip(surf[:-1], surf[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 3.0 or abs(bx - ax) < 0.5 * L:
            continue
        n = int(L / 3.2)
        for k in range(n):
            t = (k + 0.3 + 0.4 * rnd.random()) / n
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t - 0.7
            sketch(o, [(x, y), (x - 1.1, y - 1.1)], sub + " hatch", INK2, LW_HATCH * 2, over=0.0, amp=0.05, retrace=False)
    return surf

def sketch_tree(o, x, y, h):
    """Loose tree: a crown of washes in the board's tree greens, a scribbled outline and a trunk with two limbs."""
    rnd = _random.Random(_seed(x, y, h))
    cx, cy, rx, ry = x, y + 0.64 * h, 0.36 * h, 0.30 * h
    ph = [rnd.uniform(0, 6.3) for _ in range(3)]
    crown = []
    for q in range(36):                                  # board _sa_lumpy
        a = 6.283 * q / 36
        k = 1.0 + 0.12 * (math.sin(5 * a + ph[0]) + 0.6 * math.sin(8 * a + ph[1]) + 0.4 * math.sin(13 * a + ph[2])) / 2.0
        crown.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
    for (sx, sy, col, al) in ((0.0, 0.0, SITE_TREE[1], 0.55), (-0.18, 0.2, SITE_TREE[0], 0.5), (0.2, -0.22, SITE_TREE[2], 0.35)):
        part = [(cx + (px - cx) * 0.62 + sx * rx, cy + (py - cy) * 0.62 + sy * ry) for px, py in crown]
        wash(o, part if al < 0.55 else crown, "planting", col, al, z=Z_TREE)
    sketch(o, crown, "planting", SITE_TREE[2], LW_FINE, closed=True, over=0.0, amp=0.25, retrace=False, z=Z_TREE)
    sketch(o, [(x, y), (x + 0.15, cy - 0.1 * h)], "planting", SITE_TRUNK, LW_EDGE, over=0.0, retrace=False, z=Z_TREE)
    for s in (-1, 1):
        sketch(o, [(x + 0.1, cy - 0.25 * h), (x + s * 0.22 * h, cy + 0.05 * h)], "planting", SITE_TRUNK, LW_FINE,
               over=0.0, retrace=False, z=Z_TREE)

def sketch_person(o, x, y, h=4.5, kind=0, flip=False):
    """Board scale figure (SA_FIGS) at the drawing's figure height h."""
    s = h / 1.745
    sg = -1.0 if flip else 1.0
    if not PEOPLE:
        return
    fill(o, [(x + sg * bx * s, y + by * s) for bx, by in SA_FIGS[kind % len(SA_FIGS)]], "people", SITE_PEOPLE,
         alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)
    hx_, hy_, hr = SA_HEAD
    fill(o, [(x + sg * hx_ * s + hr * s * math.cos(6.283 * i / 12), y + hy_ * s + hr * s * math.sin(6.283 * i / 12))
             for i in range(12)], "people", SITE_PEOPLE, alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)

def sketch_house(o, x0, x1, y, wall=6.0, pipe=False):
    """Context: an old town house beyond the street (board TYPO "traditional": stone base, hipped tile roof, deep
    eaves), generic, not surveyed. pipe=True adds the downpipe that takes its roof water to the street."""
    ev, rise = 0.9, 2.6
    body = [(x0, y), (x1, y), (x1, y + wall), (x0, y + wall)]
    roof = [(x0 - ev, y + wall), (x1 + ev, y + wall), (x1 - 2.2, y + wall + rise), (x0 + 2.2, y + wall + rise)]
    wash(o, body, "context", HOUSE_WALL, 0.45)
    marker(o, roof, "context", HOUSE_ROOF, angle=-35.0, spacing=0.6, thick=0.5, alpha=0.45, base=0.25)
    sketch(o, body, "context", INK2, LW_FINE, closed=True)
    sketch(o, roof, "context", INK2, LW_FINE, closed=True)
    sketch(o, [(x0, y + 1.0), (x1, y + 1.0)], "context", INK2, LW_HATCH * 2, over=0.4, retrace=False)
    for wx in (x0 + 0.28 * (x1 - x0), x0 + 0.62 * (x1 - x0)):
        sketch(o, [(wx, y + 2.2), (wx + 1.3, y + 2.2), (wx + 1.3, y + 4.6), (wx, y + 4.6)], "context", INK2, LW_HATCH * 2,
               closed=True, over=0.3, retrace=False)
    if pipe:
        sketch(o, [(x1 + 0.6, y + wall), (x1 + 0.6, y + 0.3)], "context", SITE_WATER_D, LW_EDGE, over=0.0, retrace=False)

def rain(o, x0, x1, y0, y1, n=14):
    rnd = _random.Random(_seed(x0, x1, y0, y1))
    for _ in range(n):
        x, y = x0 + rnd.random() * (x1 - x0), y0 + rnd.random() * (y1 - y0)
        sketch(o, [(x, y), (x - 0.5, y - 1.6)], "rain", SITE_WATER_D, LW_FINE, over=0.0, amp=0.04, retrace=False)

def water_body(surface, xs, level):
    """The water standing at `level` around x = xs: from where the ground on the left rises through the level to
    where it does on the right (banks, walls, the low-flow channel), following the bed in between. So the water always
    meets its banks (Nil 18 Oct 17:55: the water did not meet the left bank)."""
    k = None
    for i, ((ax, ay), (bx, by)) in enumerate(zip(surface[:-1], surface[1:])):
        if ax != bx and min(ax, bx) <= xs <= max(ax, bx):
            y = ay + (by - ay) * (xs - ax) / (bx - ax)
            if y < level and (k is None or y < k[1]):
                k = (i, y)
    if k is None:
        return None

    def cross(p, q):                                  # p under the level, q at or over it
        if abs(q[1] - p[1]) < 1e-12:
            return (q[0], level)
        t = (level - p[1]) / (q[1] - p[1])
        return (p[0] + (q[0] - p[0]) * t, level)
    i = k[0]
    left, right = [], []
    j = i
    while j >= 0 and surface[j][1] < level:
        left.append(surface[j])
        j -= 1
    left.append(cross(left[-1] if left else (xs, k[1]), surface[j]) if j >= 0 else (surface[0][0], level))
    j = i + 1
    while j < len(surface) and surface[j][1] < level:
        right.append(surface[j])
        j += 1
    right.append(cross(right[-1] if right else (xs, k[1]), surface[j]) if j < len(surface) else (surface[-1][0], level))
    bed = left[::-1] + right
    out = []
    for p in bed:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-9:
            out.append(p)
    return out                                        # first and last point on the level, the bed between

def water_level(o, surface, xs, level, colour, bed_hatch=False, line=True):
    """Water at `level` around xs, cut exactly to the ground (solid), a hand surface line; bed_hatch: the board's blue
    hatch over the stream bed."""
    pts = water_body(surface, xs, level)
    if not pts or len(pts) < 3:
        return None
    fill(o, pts, "water", colour, boundary=False, hand_=False)
    if bed_hatch:
        hatch_lines(o, pts, "water", SEC_CHANNEL_HATCH, 1.1, 45.0, PEN_HAIR)
    if line:
        sketch(o, [pts[0], pts[-1]], "water lines", SITE_WATER_D, PEN_FINE, over=0.0, retrace=False, z=Z_LINE)
    return pts

def label2(o, head, body, x, y, size_pt, colour=None, mask=None):
    """v7: a bold name line with plain lines under it, one label group (they move together)."""
    own = _group()
    text(o, head, x, y, size_pt, colour, "labels", bold=True, mask=mask)
    text(o, body, x, y - size_pt * 0.353 * TXT_K[0] * 1.35, size_pt, colour, "labels", mask=mask)
    if own:
        GROUP[0] = 0

def hub_route(o, gs, x0, x1, rise=1.4):
    """v7 (history D10): the walk between the dry walking hub square and the sub-hub in the bed: an accent dashed line
    just over the steps from x0 (hub side) to x1 (sub-hub side), its head at the sub-hub."""
    r = surface_between(gs, min(x0, x1), max(x0, x1), rise)
    if len(r) < 2:
        return
    r = r if x0 < x1 else r[::-1]
    sketch(o, r, "hub route", ACCENT, PEN_MED, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    (ax, ay), (bx, by) = r[-2], r[-1]
    L = math.hypot(bx - ax, by - ay) or 1.0
    hand_arrow(o, (bx - (bx - ax) / L * 4.0, by - (by - ay) / L * 4.0), (bx, by), ACCENT, width=0.4, head=1.6)

def concept_aras_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_aras_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_aras_sketch():
    """PROBLEM: the bed is dry in summer, the winter runoff leaves the streets. MOVE: the bank becomes a cascade that
    holds the winter water, cleans it in reed basins and gives it back to the summer stream. v7: shorter words."""
    o, w = ORIGIN, 200
    g = [(0, 8), (0, 64), (34, 64), (34, 52), (68, 52), (68, 40), (102, 40), (102, 28), (130, 28)] + bank((130, 28), (140, 12))[1:] + \
        [(170, 12), (170, 28), (w, 28), (w, 8)]
    basins = ((40, 52), (74, 40), (108, 28))
    # the summer strip runs in a low-flow channel cut into the bed (v2.8: 150-160, 2.2 deep)
    gs = sketch_ground(o, notch(g, [(x0, x0 + 22, y, 5) for x0, y in basins] + [(150, 160, 12, 2.2)]))
    # winter: rain on the old town's roofs and street (context house generic, not surveyed)
    rain(o, 6, 33, 67.5, 73.5, 16)
    sketch_house(o, 15, 27, 65.3, wall=5.0, pipe=True)
    road(o, 0, 30, 64, "ROAD " + CITE("survey"), ly=61.5, mask=SOIL)          # v5: no caveat word
    # Q500's reach first (solid wash), so the basins' water and reeds stay on top of it
    for pc in [under_level(gs, 102, w, 31.5)]:
        if pc:
            wash(o, pc, "flood", FLOOD_WASH, FLOOD_ALPHA)
    # the move: the cascade of reed basins (marker band = what holds and cleans the water)
    for x0, y in basins:
        water_level(o, gs, x0 + 11, y - 0.4, W_WIN)
        reeds(o, x0 + 1, x0 + 21, y - 5, 3.2)
    for pc in band(gs, 34, 130, 1.6):
        marker(o, pc, "terraces", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    sketch_tree(o, 65, 52, 9); sketch_tree(o, 99, 40, 7)    # on the strips between the basins, above Q500's reach
    # summer: the stream (dry bed today) gets the clean water back
    water_level(o, gs, 155, 19, W_WIN, bed_hatch=True)
    water_level(o, gs, 155, 12, W_EXT, line=False)
    sun(o, 188, 58)
    sketch_person(o, 13, 65.3, kind=1); sketch_person(o, 70.8, 40)               # never inside water or the Q500 reach
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    keyed(o, "winter", "winter flow", 172, 24, 5.6, W_EXT, "water")
    keyed(o, "summer", "low-flow strip\ntoday: dry bed", 172, 19, 5.6, W_EXT, "water")
    sketch(o, [(102, 31.5), (w, 31.5)], "flood lines", HERITAGE, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 123.8, 31.5, HERITAGE, "flood lines")
    # v3 fix (audit problem 3): the surveyed ARAS cut keeps Q500 inside the banks (rain_river_levels README v1.1
    # line 21: 3.30 m, +73.66 m)
    text(o, "Q500 +73.66 m · 3.30 m " + CITE("levels") + "\ninside the banks", 126, 35.6, 5.2, HERITAGE, "flood")
    hand_arrow(o, (8, 72), (44, 56), SITE_WATER_D, bend=0.12)
    keyed(o, "winter", "street + roof runoff " + CITE("rain") + "\nNov-Feb 59.1 % of rain", 6, 77.4, 5.8)
    hand_arrow(o, (126, 31), (150, 20), SITE_WATER_D, bend=-0.15)
    keyed(o, "summer", "summer release " + CITE("rain") + "\nJun-Sep 7.4 % of rain", 109, 47, 5.8)
    for a, b in (((64, 49), (66, 44)), ((98, 37), (100, 32)), ((130, 26), (141, 18))):
        hand_arrow(o, a, b, ACCENT, width=0.4, head=1.5, bend=-0.2)
    keyed(o, "failsafe", "FAIL-SAFE · gravity\nfull basin spills to the next", 2, 31, 5.8, ACCENT, mask=SOIL)
    text(o, "hold in winter,\ngive back in summer", 46, 21, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((2, 51, 56), (3, 65, 56), (4, 85, 44), (5, 143, 22), (6, 155, 24)):
        NODE(o, x_, y_, n_)

def concept_begum_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_begum_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_begum_sketch():
    """PROBLEM: the design flood runs over today's bank top. MOVE: the street level D is raised above it and the steps
    under it let the stream climb: W wet every winter, F only in big floods, D never. K4 stays as it is.
    v7 (history D8, D10, H4): D = the dry, step-free WALKING HUB SQUARE with plane trees (irrigated from storage, h03 Q4); the bed beside the summer strip =
    the floodable SUB-HUB (its floor meets the strip: the water-touching step); a route runs down the steps between
    them. The overtopped bank is the right bank (water board CUTS k4: "right bank 2.1 m: street floods"), the bank card
    h02 gives Tabaklar Hamamı (E08, ~56 m downstream of K4, calculated): named on the lower flood terrace that faces
    it, not drawn (no surveyed outline or height in this script)."""
    o, w = (ORIGIN[0], ORIGIN[1] - 110), 200
    cx, cy = 120.0, 11.9                                           # the v2.8 arc through (98,14) (120,34) (142,14)
    r = math.hypot(98 - cx, 14 - cy)
    t0, t1 = math.atan2(14 - cy, 142 - cx), math.atan2(14 - cy, 98 - cx)
    arc = [(cx + r * math.cos(t0 + (t1 - t0) * i / 30.0), cy + r * math.sin(t0 + (t1 - t0) * i / 30.0)) for i in range(31)]
    sketch(o, arc, "K4 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)  # behind
    text(o, "Roman bridge K4\nbehind · kept", 104, 45, 5.4, INK2)
    g = [(0, 8), (0, 62), (40, 62), (40, 50), (62, 50), (62, 40), (84, 40), (84, 30), (90, 30)] + bank((90, 30), (100, 14))[1:] + \
        [(150, 14), (150, 62), (w, 62), (w, 8)]
    gs = sketch_ground(o, notch(g, [(118, 132, 14, 2.5)]))     # summer strip: low-flow channel (v2.8: 118-132, 2.5)
    wall = [(150, 14), (154, 14), (154, 62), (150, 62)]
    marker(o, wall, "wall", STONE, angle=45.0, spacing=0.55, thick=0.5, alpha=0.55, base=0.35)
    text(o, "channel wall kept " + CITE("concept"), 156, 65, 5.4)
    # the stream climbing the steps: every winter (W), the design flood (F), never D
    fl = under_level(gs, 40, 150, 52)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 125, 33, W_WIN, bed_hatch=True)
    water_level(o, gs, 125, 14, W_EXT, line=False)
    keyed(o, "winter", "bed under water", 156, 31.8, 5.6, W_EXT, "water")
    keyed(o, "summer", "summer strip\ntoday: dry, pools", 156, 15.3, 5.6, W_EXT, "water")
    for x0, x1 in ((0, 40), (40, 84), (84, 100)):
        for pc in band(gs, x0, x1, 1.5):
            marker(o, pc, "tiers", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    # v7: the sub-hub floor in the bed at the strip level, up to the channel edge (the water-touching step)
    fill(o, [(101, 14), (117.6, 14), (117.6, 15.0), (101, 15.0)], "sub-hub", SEC_PAVE)
    reeds(o, 133, 148, 14, 4.5)
    road(o, 0, 16, 62, "ROAD " + CITE("survey") + "\nK4 deck: traffic", ly=54.5, mask=SOIL)
    sketch_tree(o, 22, 62, 10); sketch_tree(o, 35, 62, 10)                      # plane trees on the dry hub square (D8)
    sketch_person(o, 28, 62, kind=1); sketch_person(o, 30.5, 62, kind=2, flip=True); sketch_person(o, 195, 62)
    sketch_person(o, 108, 15.0, kind=0)                                         # sub-hub at low water
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    sketch(o, wall, "wall lines", SKINK, PEN_BOLD, closed=True, z=Z_LINE)
    sketch(o, [(40, 52), (150, 52)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    tick_dim(o, 43, 52, 62, SKINK)                                                # D: raised clear of the flood
    hand_arrow(o, (138, 34.5), (138, 50.5), SITE_WATER_D, width=0.45, head=1.8)  # the stream climbs in big floods
    level_mark(o, 146, 52, W_EXT, "flood lines")
    hub_route(o, gs, 36, 104)                                                     # hub square -> steps -> sub-hub
    hand_arrow(o, (80, 63.3), (80, 41.6), HERITAGE, width=0.35, head=1.4)         # label -> the terrace facing the ruin
    text(o, "Q500 over today's bank " + CITE("levels") + "\nhub square above it", 156, 51, 5.6, W_EXT, "water")
    label2(o, "WALKING HUB SQUARE " + CITE("hubs"), "street level · step-free\nplane trees · irrigated from storage " + CITE("plane"),
           1, 82, 5.6, SKINK)
    label2(o, "TABAKLAR HAMAMI ruin " + CITE("hamam"), "~56 m downstream · terrace faces it", 58, 69, 5.6, HERITAGE)
    label2(o, "steps + flood terraces", "wet only in big floods", 41, 47, 5.6, SKINK, mask=SOIL)
    label2(o, "SUB-HUB in the bed " + CITE("hubs"), "strip level · shut in winter floods\nwater-touching step at the strip",
           100, 10.8, 5.6, SKINK, mask=SOIL)
    text(o, "the stream climbs the steps,\nthe hub square stays dry", 6, 31, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((6, 125, 18), (7, 110, 27), (8, 75, 35.5), (9, 6, 67)):
        NODE(o, x_, y_, n_)

def concept_k5_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_k5_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_k5_sketch():
    """v1.4. Demeter's Garden (card i01) on the dry top of the south-west bank by K5 (zones DG 1-2, tier D). PROBLEM:
    olives and lavender cannot stand waterlogged soil. MOVE: the garden sits on the dry top, above the K5 cut's Q500,
    and the clean stream waters it. Intake, lift and basin volume: not in the card, so not drawn.
    v7 (history D8, D10): the other bank top = the dry, step-free WALKING HUB SQUARE with plane trees (irrigated from storage, h03 Q4); steps down that
    bank to the bed; the stream commons in the bed = the floodable SUB-HUB at the strip level."""
    o, w = ORIGIN, 200
    for c in (108.3, 125.0, 141.7):                                # K5 behind: three arches by its name, schematic
        arc = [(c + 8.0 * math.cos(math.pi * i / 20.0), 20.0 + 8.0 * math.sin(math.pi * i / 20.0)) for i in range(21)]
        sketch(o, arc, "K5 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)
    sketch(o, [(98, 36), (156, 36)], "K5 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)
    text(o, "Üç Kemer bridge K5\nbehind · kept", 100, 50, 5.4, INK2)
    stairs = []                                                    # v7: the bank from the bed to the hub as steps
    for k_ in range(1, 7):
        stairs += [(150 + 10.0 * (k_ - 1) / 6.0, 14 + 26.0 * k_ / 6.0), (150 + 10.0 * k_ / 6.0, 14 + 26.0 * k_ / 6.0)]
    g = [(0, 8), (0, 40), (92, 40)] + bank((92, 40), (104, 14))[1:] + [(150, 14)] + stairs + [(w, 40), (w, 8)]
    gs = sketch_ground(o, notch(g, [(56, 68, 40, 3.5), (122, 136, 14, 2.5)]))   # basin by the bridge; summer strip
    fl = under_level(gs, 92, 158, 35)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 129, 22, W_WIN, bed_hatch=True)
    water_level(o, gs, 129, 14, W_EXT, line=False)
    water_level(o, gs, 62, 39.6, W_WIN)                            # the water collection basin (volume: not given)
    for pc in band(gs, 18, 92, 1.5):
        marker(o, pc, "tiers", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    for pc in band(gs, 160, w, 1.5):                               # v7: the hub square, dry like the garden
        marker(o, pc, "tiers", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    reeds(o, 104, 118, 14, 4.0)
    road(o, 0, 16, 40, "STREET " + CITE("survey"), ly=37.5, mask=SOIL)
    cafe = [(72, 40), (86, 40), (86, 45.5), (72, 45.5)]
    wash(o, cafe, "garden", HOUSE_WALL, 0.45)
    sketch(o, cafe, "garden", INK2, LW_FINE, closed=True)
    sketch(o, [(71, 45.5), (87, 45.5), (85, 47.5), (73, 47.5)], "garden", INK2, LW_FINE, closed=True)
    sketch_tree(o, 26, 40, 9); sketch_tree(o, 38, 40, 8)                 # olives
    sketch_tree(o, 49, 40, 12)                                           # stone pine
    sketch_tree(o, 170, 40, 10); sketch_tree(o, 184, 40, 10)             # v7: plane trees on the hub square (D8)
    sketch_person(o, 89, 40, kind=1); sketch_person(o, 31, 40, kind=2, flip=True)
    sketch_person(o, 177, 40); sketch_person(o, 195, 40, kind=2, flip=True); sketch_person(o, 142, 14, kind=0)
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)
    sketch(o, [(95, 35), (158, 35)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 154, 35, W_EXT, "flood lines")
    hub_route(o, gs, 166, 138)                                                    # hub square -> steps -> sub-hub
    h = 5.6 * 0.353 * TXT_K[0]                                                    # one line of 5.6 pt words
    text(o, "Q500 +58.75 m · 2.79 m " + CITE("levels") + "\ninside the banks", 160, 64 + 2.9 * h, 5.4, W_EXT, "water")
    label2(o, "WALKING HUB " + CITE("hubs"), "street level · step-free\nplane trees " + CITE("plane") + "\nirrigated from storage",
           160, 64, 5.6, SKINK)
    text(o, "steps", 141, 27.5, 5.6, SKINK)
    keyed(o, "winter", "bed under water", 162, 31, 5.6, W_EXT, "water", mask=SOIL)
    keyed(o, "summer", "summer strip\ntoday: dry, pools", 162, 17, 5.6, W_EXT, "water", mask=SOIL)
    text(o, "olives", 22, 53, 5.2, INK2); text(o, "stone pine", 44, 58, 5.2, INK2)
    text(o, "basin", 57, 45, 5.2, INK2); text(o, "cafe", 75, 50, 5.2, INK2)
    label2(o, "DEMETER'S GARDEN " + CITE("garden"), "dry bank top · all year · DG 1-2", 20, 36.5, 5.6, mask=SOIL)
    text(o, "olive, lavender: no waterlogged soil " + CITE("plants"), 4, 26, 5.2, ACCENT, mask=SOIL)
    hand_arrow(o, (128, 17), (66, 38.6), SITE_WATER_D, bend=0.15)
    text(o, "strip water to the garden\nintake + lift", 62, 22, 5.2, SITE_WATER_D, mask=SOIL)
    # v3: the card's crop list as two season rows (sun = summer, cloud = winter); every crop kept
    keyed(o, "summer", "cafe beds: beans · tomatoes · peppers · figs · grapes", 4, 80, 5.6)
    keyed(o, "winter", "herbs · greens · cabbages · citrus · quince " + CITE("garden"), 4, 80 - 1.5 * h, 5.6)
    for n_, x_, y_ in ((6, 129, 18), (7, 110, 22), (9, 8, 45)):
        NODE(o, x_, y_, n_)
    # v6: the two zones under the cut, and what each water state means for people; v7: the bed is the sub-hub
    yz = 3.0 - 0.75 * h
    for x0, x1, col, lab in ((18, 92, SUN, "DRY · DEMETER'S GARDEN · bank top"),
                             (95, 158, W_EXT, "WET · COMMONS = SUB-HUB · bed")):
        sketch(o, [(x0, 4.5), (x1, 4.5)], "zones", col, PEN_BOLD, over=0.0, retrace=False, z=Z_LINE)
        for xe in (x0, x1):
            sketch(o, [(xe, 3.2), (xe, 5.8)], "zones", col, PEN_BOLD, over=0.0, retrace=False, z=Z_LINE)
        text(o, lab, x0, yz, 5.6, SKINK, "zones", bold=True)
    keyed(o, "winter", "high water: up in the garden + hub", 18, yz - 1.5 * h, 5.6, INK2)
    keyed(o, "summer", "low water: down to the sub-hub", 95, yz - 1.5 * h, 5.6, W_EXT)

def concept_nil_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_nil_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_nil_sketch():
    """v1.4. Give back (zones WP 1-2 and the floodable boardwalk, ZONES.md). PROBLEM: the downstream edge is unused
    ground and the summer bed is a trickle. MOVE: the clean stream from the upstream basins feeds floodable planting
    people can walk along; nothing is treated here; surplus goes to the farmland outside the site. v7: shorter words."""
    o, w = ORIGIN, 200
    g = [(0, 8), (0, 62), (30, 62), (46, 30), (110, 30)] + bank((110, 30), (120, 14))[1:] + \
        [(165, 14), (175, 32), (w, 32), (w, 8)]
    gs = sketch_ground(o, notch(g, [(136, 150, 14, 2.2)]))     # summer strip: low-flow channel
    fl = under_level(gs, 110, 178, 27)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 143, 21, W_WIN, bed_hatch=True)
    water_level(o, gs, 143, 14, W_EXT, line=False)
    for pc in band(gs, 46, 110, 1.6):
        marker(o, pc, "planting", REED, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    reeds(o, 121, 134, 14, 3.5)
    sketch_tree(o, 78, 30, 6); sketch_tree(o, 92, 30, 5.5); sketch_tree(o, 103, 30, 5)
    deck = [(44.5, 33.2), (72, 33.2), (72, 34.2), (44.5, 34.2)]
    fill(o, deck, "boardwalk", SEC_PAVE)
    for x_ in (50, 58, 66):
        sketch(o, [(x_, 33.2), (x_, 30)], "boardwalk", INK2, LW_EDGE, over=0.0, retrace=False)
    sketch_person(o, 60, 34.2, kind=1); sketch_person(o, 14, 62)
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)
    sketch(o, [(112, 27), (178, 27)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 172, 27, W_EXT, "flood lines")
    text(o, "Q500 +48.00 m · 2.33 m " + CITE("levels") + "\ninside the banks\nflat end: floods wide + shallow", 150, 60, 5.4, W_EXT, "water")
    keyed(o, "winter", "bed under water", 170, 28.5, 5.6, W_EXT, "water", mask=SOIL)
    keyed(o, "summer", "summer strip\ntoday: trickle " + CITE("gauges"), 170, 23.5, 5.6, W_EXT, "water", mask=SOIL)
    text(o, "floodable planting · WP 1-2 " + CITE("zones") + "\nclean-stream fed", 48, 27, 5.4, mask=SOIL)
    text(o, "floodable boardwalk " + CITE("zones"), 48, 45, 5.4)
    text(o, "slope", 2, 59, 5.2, INK2, mask=SOIL)
    keyed(o, "failsafe", "FAIL-SAFE\nhigh water passes over", 1, 50, 5.6, ACCENT, mask=SOIL)
    hand_arrow(o, (141, 16), (100, 31.5), SITE_WATER_D, bend=0.15)
    text(o, "clean stream + strip\nfeed the planting", 112, 45, 5.6, SITE_WATER_D)
    hand_arrow(o, (184, 35), (196, 44), ACCENT, width=0.4, head=1.5, bend=-0.2)
    text(o, "surplus · farmland outside", 150, 72, 5.6, ACCENT)
    text(o, "arrives clean · no treatment here", 62, 76, 5.6)
    text(o, "clean stream back to a\nwalkable planted edge", 4, 76, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((6, 143, 17.5), (7, 84, 34), (10, 158, 18), (11, 190, 38)):
        NODE(o, x_, y_, n_)

'''
