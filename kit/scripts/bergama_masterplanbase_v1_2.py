# -*- coding: utf-8 -*-
"""Bergama Group 6: MASTERPLANBASE v1 (14 Nov 2026): Aras's masterplan SVG read ONCE into a cache in survey metres,
for every slide that shows the proposal.

Aras 14 Nov 15:38 UTC: "please take these from the masterplan that i have given you anything that concerns
masterplans that should use it" (the masterplan = B19_setB_layers259.svg); 12:38 UTC: "don't ever do the same job twice
in two scripts if one scripts does that job cache it and make it usable by the next script" + "we can chain all the
scripts". Chained after MapBase (it reads MapBase's cache for its check).

What it does: reads Data/assets/plan/B19_setB_layers259.svg (MP_SVG; v1.1: no fallback, a plain stop when it is missing),
walks every group with its transforms (SVG code copied from PlanToRhino v2.1: transforms, paths, arcs, shapes) and
writes cached/bergama_masterplanbase/masterplan.json in SURVEY metres:
  layers   {key: [[kind, fill, stroke, width m, [[x, y], ...]], ...]}; key = the chain of named group ids from the top,
           "/"-joined, Illustrator wrappers (Layer_N, no id) left out, e.g. "yuruyus/iskele_kenari", "kopruler/path",
           "teras_-_canopy/kanopi"; kind "r" closed ring, "l" open line, "a" the outline of a clipped picture area
           (his stamped textures: teras, iskele_kenari, ana_su ...: their footprint IS the clip outline), "s" a
           picture stamp outside any clip (its placed rectangle); fill / stroke = his own hex colours (None = none)
  texts    [[key, text, x, y, size m]]
  matrix   SVG units -> survey m (affine a..f), units_per_m, the SVG frame used, the check
PLACING (PlanToRhino v2.1 world_matrix): the box of his existing roads and buildings (group "ev-yol") is site_alan
turned flat (its long side horizontal, upstream left): site_alan's corners come from the Basemap cache (frame).
CHECK: the share of his existing building outlines whose middle lies inside a MapBase building (FLAG under 60 %), and
review PNGs of the cache drawn over MapBase (output/bergama_masterplanbase/review/), whole page.
Draw it (any page): exec this file's code above "# ==== main" (pages_common pc_mp_data does it) ->
  C = mp_load(log); counts = mp_draw(C, items, T, k, lim, cid, layers=None, style=None)
The cache is rebuilt only when the SVG changes (its size + time), or when the input `rebuild` is True.
"""
import os, re, json, math, time, glob

VERSION = "v1.2"
GH_LABEL = "MasterplanBase"
OUT_FOLDER = "bergama_masterplanbase"
LOG_NAME = "bergama_masterplanbase_log.txt"
GH_INPUTS = {"rebuild": "bool"}
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
MP_FILE = "masterplan.json"
MP_SVG = os.path.join("Data", "assets", "plan", "B19_setB_layers259.svg")
MP_SVG_GLOB = os.path.join("Data", "assets", "plan", "B19_setB_layers*.svg")
BASEMAP_CACHE = os.path.join("cached", "bergama_basemap", "basemap_layers.json")
PLACE_GROUP = "ev-yol"                       # his existing roads + buildings: their box = site_alan turned flat
CHECK_GROUP = "existing_buildings"
MAX_PIECES = 400000                          # v1.2: run 1 read 42,255; more means the SVG loops (memory guard)
CURVE_STEP_M = 0.5                           # m between points on a flattened curve (at most 24 per piece)
SKIP_TAGS = ("defs", "clipPath", "symbol", "style", "metadata", "title", "desc", "mask", "pattern", "linearGradient",
             "radialGradient", "filter")
# fills for the clipped picture areas (his textures are pictures: no fill colour in the file); OUR picks from the
# project palette, a page may pass its own (style["area"])
AREA_FILL = {"teras": "CDBFA3", "iskele_kenari": "BFAE92", "kesin_yesil": "A9B98A", "belki_yesil": "C4CFA8",
             "ana_su": "A2B6B5", "su": "A2B6B5", "bitki2": "9EAF85", "kanopi": "D8D6D2"}
AREA_DEFAULT = "D6D0C4"

_NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
SVGNS = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"
ID = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


# ================================================================ SVG geometry (copied from PlanToRhino v2.1)
def mat_mul(a, b):
    return (a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1],
            a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3],
            a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5])


def mat_pt(m, p):
    return (m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5])


def mat_scale(m):
    return math.sqrt(abs(m[0] * m[3] - m[1] * m[2])) or 1.0


def parse_transform(s):
    m = ID
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", s or ""):
        v = [float(x) for x in _NUM.findall(args)]
        if name == "matrix" and len(v) == 6:
            t = tuple(v)
        elif name == "translate":
            t = (1.0, 0.0, 0.0, 1.0, v[0], v[1] if len(v) > 1 else 0.0)
        elif name == "scale":
            t = (v[0], 0.0, 0.0, v[1] if len(v) > 1 else v[0], 0.0, 0.0)
        elif name == "rotate":
            a = math.radians(v[0])
            r = (math.cos(a), math.sin(a), -math.sin(a), math.cos(a), 0.0, 0.0)
            if len(v) == 3:
                t = mat_mul((1.0, 0.0, 0.0, 1.0, v[1], v[2]), mat_mul(r, (1.0, 0.0, 0.0, 1.0, -v[1], -v[2])))
            else:
                t = r
        elif name == "skewX":
            t = (1.0, 0.0, math.tan(math.radians(v[0])), 1.0, 0.0, 0.0)
        elif name == "skewY":
            t = (1.0, math.tan(math.radians(v[0])), 0.0, 1.0, 0.0, 0.0)
        else:
            continue
        m = mat_mul(m, t)
    return m


def parse_css(text):
    out = {}
    text = re.sub(r"/\*.*?\*/", "", text or "", flags=re.S)
    for sel, body in re.findall(r"([^{}]+)\{([^}]*)\}", text):
        decl = {}
        for part in body.split(";"):
            if ":" in part:
                k, v = part.split(":", 1)
                decl[k.strip().lower()] = v.strip()
        for s_ in sel.split(","):
            s_ = s_.strip()
            if s_.startswith("."):
                out.setdefault(s_[1:], {}).update(decl)
    return out


def hex_of(v):
    """an SVG paint -> 'RRGGBB' or None (none, url(...), unknown)"""
    if not v:
        return None
    v = v.strip().lower()
    if v in ("none", "transparent") or v.startswith("url("):
        return None
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return h[:6].upper() if len(h) >= 6 else None
    if v.startswith("rgb"):
        n = [float(x) for x in _NUM.findall(v)[:3]]
        if "%" in v:
            n = [x * 2.55 for x in n]
        return "%02X%02X%02X" % tuple(int(round(max(0, min(255, x)))) for x in n) if len(n) == 3 else None
    return {"black": "000000", "white": "FFFFFF", "red": "FF0000", "green": "008000", "blue": "0000FF",
            "gray": "808080", "grey": "808080"}.get(v)


def path_segments(d):
    """SVG path data -> [(closed, [start, ('L', p) | ('C', c1, c2, p), ...])] (PlanToRhino v2.1)"""
    toks = re.findall(r"[MmZzLlHhVvCcSsQqTtAa]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", d or "")
    subs, cur, pos, start = [], None, (0.0, 0.0), (0.0, 0.0)
    i, cmd, last_c, last_q = 0, None, None, None

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            if cmd in "Zz":
                if cur is not None:
                    subs.append((True, cur))
                    cur = None
                pos = start
                last_c = last_q = None
                continue
        elif cmd is None:
            i += 1
            continue
        rel = cmd.islower()
        c = cmd.upper()
        ox, oy = pos if rel else (0.0, 0.0)
        if c == "M":
            p = (num() + ox, num() + oy)
            if cur is not None:
                subs.append((False, cur))
            cur, pos, start = [p], p, p
            cmd = "l" if rel else "L"
            last_c = last_q = None
            continue
        if cur is None:
            cur = [pos]
        if c == "L":
            p = (num() + ox, num() + oy)
            cur.append(("L", p))
            last_c = last_q = None
        elif c == "H":
            p = (num() + ox, pos[1])
            cur.append(("L", p))
            last_c = last_q = None
        elif c == "V":
            p = (pos[0], num() + oy)
            cur.append(("L", p))
            last_c = last_q = None
        elif c == "C":
            c1 = (num() + ox, num() + oy)
            c2 = (num() + ox, num() + oy)
            p = (num() + ox, num() + oy)
            cur.append(("C", c1, c2, p))
            last_c, last_q = c2, None
        elif c == "S":
            c1 = (2 * pos[0] - last_c[0], 2 * pos[1] - last_c[1]) if last_c else pos
            c2 = (num() + ox, num() + oy)
            p = (num() + ox, num() + oy)
            cur.append(("C", c1, c2, p))
            last_c, last_q = c2, None
        elif c in "QT":
            if c == "Q":
                q = (num() + ox, num() + oy)
            else:
                q = (2 * pos[0] - last_q[0], 2 * pos[1] - last_q[1]) if last_q else pos
            p = (num() + ox, num() + oy)
            c1 = (pos[0] + 2.0 / 3.0 * (q[0] - pos[0]), pos[1] + 2.0 / 3.0 * (q[1] - pos[1]))
            c2 = (p[0] + 2.0 / 3.0 * (q[0] - p[0]), p[1] + 2.0 / 3.0 * (q[1] - p[1]))
            cur.append(("C", c1, c2, p))
            last_q, last_c = q, None
        elif c == "A":
            rx, ry, phi = abs(num()), abs(num()), num()
            fa, fs = num(), num()
            p = (num() + ox, num() + oy)
            cur.extend(arc_to_cubics(pos, rx, ry, phi, fa != 0, fs != 0, p))
            last_c = last_q = None
        else:
            i += 1
            continue
        pos = p
    if cur is not None and len(cur) > 1:
        subs.append((False, cur))
    return [(cl, s) for cl, s in subs if len(s) > 1]


def arc_to_cubics(p0, rx, ry, phi, large, sweep, p1):
    """SVG elliptical arc -> cubic pieces (W3C implementation notes F.6; PlanToRhino v2.1)"""
    if rx == 0 or ry == 0 or p0 == p1:
        return [("L", p1)]
    ph = math.radians(phi)
    cp, sp = math.cos(ph), math.sin(ph)
    dx, dy = (p0[0] - p1[0]) / 2.0, (p0[1] - p1[1]) / 2.0
    x1, y1 = cp * dx + sp * dy, -sp * dx + cp * dy
    lam = (x1 * x1) / (rx * rx) + (y1 * y1) / (ry * ry)
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num_ = rx * rx * ry * ry - rx * rx * y1 * y1 - ry * ry * x1 * x1
    den = rx * rx * y1 * y1 + ry * ry * x1 * x1
    co = math.sqrt(max(0.0, num_ / den)) if den else 0.0
    if large == sweep:
        co = -co
    cx1, cy1 = co * rx * y1 / ry, -co * ry * x1 / rx
    cx, cy = cp * cx1 - sp * cy1 + (p0[0] + p1[0]) / 2.0, sp * cx1 + cp * cy1 + (p0[1] + p1[1]) / 2.0
    ang = lambda ux, uy, vx, vy: math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
    t1 = ang(1, 0, (x1 - cx1) / rx, (y1 - cy1) / ry)
    dt = ang((x1 - cx1) / rx, (y1 - cy1) / ry, (-x1 - cx1) / rx, (-y1 - cy1) / ry)
    if not sweep and dt > 0:
        dt -= 2 * math.pi
    elif sweep and dt < 0:
        dt += 2 * math.pi
    n = max(1, int(math.ceil(abs(dt) / (math.pi / 2))))
    out, h = [], dt / n
    k = 4.0 / 3.0 * math.tan(h / 4.0)
    E = lambda t: (cx + rx * math.cos(t) * cp - ry * math.sin(t) * sp, cy + rx * math.cos(t) * sp + ry * math.sin(t) * cp)
    D = lambda t: (-rx * math.sin(t) * cp - ry * math.cos(t) * sp, -rx * math.sin(t) * sp + ry * math.cos(t) * cp)
    for j in range(n):
        a, b = t1 + j * h, t1 + (j + 1) * h
        pa, pb, da, db = E(a), E(b), D(a), D(b)
        out.append(("C", (pa[0] + k * da[0], pa[1] + k * da[1]), (pb[0] - k * db[0], pb[1] - k * db[1]),
                    p1 if j == n - 1 else pb))
    return out


def shape_subpaths(tag, el):
    """rect / circle / ellipse / line / polygon / polyline -> the form of path_segments (PlanToRhino v2.1)"""
    f = lambda k, dflt=0.0: float(_NUM.findall(el.get(k, "") or "")[0]) if _NUM.findall(el.get(k, "") or "") else dflt
    if tag == "rect":
        x, y, w, h = f("x"), f("y"), f("width"), f("height")
        if w <= 0 or h <= 0:
            return []
        return [(True, [(x, y), ("L", (x + w, y)), ("L", (x + w, y + h)), ("L", (x, y + h))])]
    if tag in ("circle", "ellipse"):
        cx, cy = f("cx"), f("cy")
        rx = f("r") if tag == "circle" else f("rx")
        ry = f("r") if tag == "circle" else f("ry")
        if rx <= 0 or ry <= 0:
            return []
        k = 0.5522847498
        P = [(cx + rx, cy), ("C", (cx + rx, cy + k * ry), (cx + k * rx, cy + ry), (cx, cy + ry)),
             ("C", (cx - k * rx, cy + ry), (cx - rx, cy + k * ry), (cx - rx, cy)),
             ("C", (cx - rx, cy - k * ry), (cx - k * rx, cy - ry), (cx, cy - ry)),
             ("C", (cx + k * rx, cy - ry), (cx + rx, cy - k * ry), (cx + rx, cy))]
        return [(True, P)]
    if tag == "line":
        return [(False, [(f("x1"), f("y1")), ("L", (f("x2"), f("y2")))])]
    if tag in ("polygon", "polyline"):
        v = [float(x) for x in _NUM.findall(el.get("points", ""))]
        pts = list(zip(v[0::2], v[1::2]))
        if len(pts) < 2:
            return []
        return [(tag == "polygon", [pts[0]] + [("L", p) for p in pts[1:]])]
    return []


def flat(m, s, upm):
    """one subpath through m, its curves as points about CURVE_STEP_M apart (upm = SVG units per m)"""
    P = [mat_pt(m, s[0])]
    for seg in s[1:]:
        if seg[0] == "L":
            P.append(mat_pt(m, seg[1]))
            continue
        a, c1, c2, b = P[-1], mat_pt(m, seg[1]), mat_pt(m, seg[2]), mat_pt(m, seg[3])
        L = math.hypot(c1[0] - a[0], c1[1] - a[1]) + math.hypot(c2[0] - c1[0], c2[1] - c1[1]) + \
            math.hypot(b[0] - c2[0], b[1] - c2[1])
        n = max(1, min(24, int(L / (CURVE_STEP_M * upm))))
        for j in range(1, n + 1):
            t = j / float(n)
            u = 1 - t
            P.append((u * u * u * a[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t * t * t * b[0],
                      u * u * u * a[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t * t * t * b[1]))
    return P


def local(tag):
    return tag.split("}", 1)[-1] if isinstance(tag, str) else ""


# ================================================================ placing (PlanToRhino v2.1 site_turn, world_matrix)
def site_turn(site):
    best = None
    for a, b in zip(site, site[1:] + site[:1]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if best is None or L > best[0]:
            best = (L, b[0] - a[0], b[1] - a[1])
    _, vx, vy = best
    if vx < 0:
        vx, vy = -vx, -vy
    return -math.atan2(vy, vx)


def world_matrix(site, rect, notes):
    """SVG units -> survey m: the SVG box rect (x, y, w, h) IS site_alan turned flat (long side horizontal)"""
    rot = site_turn(site)
    ca, sa = math.cos(rot), math.sin(rot)
    ox, oy = site[0]
    turned = [(ox + ca * (p[0] - ox) - sa * (p[1] - oy), oy + sa * (p[0] - ox) + ca * (p[1] - oy)) for p in site]
    x0, y0 = min(p[0] for p in turned), min(p[1] for p in turned)
    x1, y1 = max(p[0] for p in turned), max(p[1] for p in turned)
    rx, ry, rw, rh = rect
    sx, sy = rw / (x1 - x0), rh / (y1 - y0)
    s = (sx + sy) / 2.0
    notes.append(u"placing: the SVG box %.2f x %.2f units = site_alan %.1f x %.1f m turned flat (%.4f units per m; "
                 u"width and height agree to %.2f %%)" % (rw, rh, x1 - x0, y1 - y0, s, abs(sx - sy) / s * 100.0))
    if abs(sx - sy) / s > 0.01:
        notes.append(u"FLAG placing: the box's width and height scales differ by %.1f %%: is %s still cut at "
                     u"site_alan?" % (abs(sx - sy) / s * 100.0, PLACE_GROUP))
    A = (1.0 / s, 0.0, 0.0, -1.0 / s, x0 - rx / s, y0 + (ry + rh) / s)
    Ri = (ca, -sa, sa, ca, ox - ca * ox - sa * oy, oy + sa * ox - ca * oy)
    return mat_mul(Ri, A), s


# ================================================================ read the SVG
def read_svg(path, log):
    """every piece in SVG units: (layers {key: [[kind, fill, stroke, width units, pts]]}, texts, box of PLACE_GROUP)"""
    import xml.etree.ElementTree as ET
    tree_ = []
    for ev, el in ET.iterparse(path, events=("end",)):  # the pictures' data dropped as read (the file is mostly them)
        if local(el.tag) == "image":
            for k_ in list(el.attrib):
                if k_.endswith("href"):
                    el.attrib[k_] = ""
        tree_.append(el) if local(el.tag) == "svg" else None
    root = tree_[-1]
    ids, css = {}, {}
    for el in root.iter():
        i_ = el.get("id")
        if i_:
            ids[i_] = el
        if local(el.tag) == "style":
            css.update(parse_css(el.text or ""))
    layers, texts, box = {}, [], [1e18, 1e18, -1e18, -1e18]
    n = {"pieces": 0, "areas": 0, "stamps": 0, "texts": 0}

    def style_of(el, st):
        s = dict(st)
        for c in (el.get("class") or "").split():
            s.update(css.get(c, {}))
        for part in (el.get("style") or "").split(";"):
            if ":" in part:
                k, v = part.split(":", 1)
                s[k.strip().lower()] = v.strip()
        for k in ("fill", "stroke", "stroke-width", "display", "visibility"):
            if el.get(k) is not None:
                s[k] = el.get(k)
        return s

    def named(i_):
        return bool(i_) and not re.match(r"^(Layer_\d+|g\d*|_?x?\d.*)$", i_)

    def add(key, rec, m):
        tot[0] += 1
        if tot[0] > MAX_PIECES:                         # v1.2: a hard stop instead of filling the PC's memory
            raise RuntimeError(u"more than %d pieces read: the SVG repeats itself (a <use> loop?); stopped" % MAX_PIECES)
        layers.setdefault(key, []).append(rec)
        if key.split("/")[0] == PLACE_GROUP:
            for p in rec[4]:
                box[0], box[1] = min(box[0], p[0]), min(box[1], p[1])
                box[2], box[3] = max(box[2], p[0]), max(box[3], p[1])

    def quad(m, w, h):
        return [mat_pt(m, q) for q in ((0, 0), (w, 0), (w, h), (0, h))]

    tot = [0]

    def walk(el, m, chain, st, clipped, depth=0, via=()):
        for ch in el:
            tag = local(ch.tag)
            if tag in SKIP_TAGS or depth > 60:
                continue
            s = style_of(ch, st)
            if s.get("display") == "none" or s.get("visibility") == "hidden":
                continue
            mm = mat_mul(m, parse_transform(ch.get("transform")))
            key = u"/".join(chain) or u"_root"
            if tag in ("g", "a", "switch"):
                i_ = ch.get("id")
                c2 = chain + [i_] if named(i_) else chain
                cp = re.search(r"url\(\s*#([^)\s]+)\s*\)", ch.get("clip-path") or s.get("clip-path") or "")
                cl2 = clipped
                if cp and cp.group(1) in ids:          # the clip outline = the area of the pictures inside it
                    k2 = u"/".join(c2) or u"_root"
                    for sh in ids[cp.group(1)]:
                        t_ = local(sh.tag)
                        subs = path_segments(sh.get("d")) if t_ == "path" else shape_subpaths(t_, sh)
                        m2 = mat_mul(mm, parse_transform(sh.get("transform")))
                        for cl_, sp in subs:
                            add(k2, ["a", None, None, 0.0, flat(m2, sp, UPM[0])], m2)
                            n["areas"] += 1
                    cl2 = True
                walk(ch, mm, c2, s, cl2, depth + 1, via)
            elif tag in ("use", "image"):
                x, y = float(ch.get("x") or 0), float(ch.get("y") or 0)
                m2 = mat_mul(mm, (1.0, 0.0, 0.0, 1.0, x, y))
                tgt = ch
                if tag == "use":
                    href = ch.get(XLINK) or ch.get("href") or ""
                    tgt = ids.get(href.lstrip("#"))
                    if tgt is None or href in via:      # v1.2: a <use> that leads back to itself is skipped
                        continue
                    if local(tgt.tag) != "image":       # a group / shape: drawn in place
                        wrap_ = ET.Element("g")
                        wrap_.append(tgt)
                        walk(wrap_, m2, chain, s, clipped, depth + 1, via + (href,))
                        continue
                if not clipped:
                    w_, h_ = float(tgt.get("width") or 0), float(tgt.get("height") or 0)
                    if w_ > 0 and h_ > 0:
                        mt = mat_mul(m2, parse_transform(tgt.get("transform")) if tgt is not ch else ID)
                        add(key, ["s", None, None, 0.0, quad(mt, w_, h_)], m2)
                        n["stamps"] += 1
            elif tag == "text":
                t_ = u"".join(ch.itertext()).strip()
                if t_:
                    sz = float((_NUM.findall(s.get("font-size", "") or "") or [10])[0]) * mat_scale(mm)
                    q = mat_pt(mm, (float(ch.get("x") or 0), float(ch.get("y") or 0)))
                    texts.append([key, t_, q[0], q[1], sz])
                    n["texts"] += 1
            elif tag in ("path", "rect", "circle", "ellipse", "line", "polygon", "polyline"):
                subs = path_segments(ch.get("d")) if tag == "path" else shape_subpaths(tag, ch)
                fill = hex_of(s.get("fill", "#000000"))
                stroke = hex_of(s.get("stroke"))
                if fill is None and stroke is None:
                    continue
                sw = float((_NUM.findall(s.get("stroke-width", "1") or "1") or [1])[0]) * mat_scale(mm)
                for cl_, sp in subs:
                    P = flat(mm, sp, UPM[0])
                    closed_ = cl_ or (fill is not None and len(P) >= 3)
                    add(key, ["r" if closed_ else "l", fill if closed_ else None, stroke, sw if stroke else 0.0, P],
                        mm)
                    n["pieces"] += 1
    UPM = [2.2]                                          # rough units per m for curve steps (refined after placing)
    walk(root, parse_transform(root.get("transform")), [], {}, False)
    log.append(u"SVG read: %d pieces, %d clipped picture areas, %d picture stamps, %d texts in %d layers" % (
        n["pieces"], n["areas"], n["stamps"], n["texts"], len(layers)))
    return layers, texts, box


def site_alan(log):
    p = os.path.join(BERGAMA_ROOT, BASEMAP_CACHE)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: press Basemap once (it caches site_alan), then this" % p)
    with open(p, encoding="utf-8") as f:
        fr = json.load(f).get("frame")
    if not fr or len(fr) < 4:
        raise RuntimeError(u"no site_alan frame in %s" % p)
    log.append(u"site_alan from the Basemap cache: %s" % u", ".join(u"(%.1f, %.1f)" % tuple(q[:2]) for q in fr[:4]))
    return [tuple(q[:2]) for q in fr[:4]]


def svg_file(log):
    """only Aras's masterplan (B19_setB_layers259.svg); no fallback to another SVG"""
    p = os.path.join(BERGAMA_ROOT, MP_SVG)
    if not os.path.isfile(p):
        others = sorted(os.path.basename(f) for f in glob.glob(os.path.join(BERGAMA_ROOT, MP_SVG_GLOB)))
        raise RuntimeError(u"Aras's masterplan SVG is missing: copy B19_setB_layers259.svg (about 134 MB) into %s, "
                           u"then press MasterplanBase again (other SVGs there, not used: %s)"
                           % (os.path.dirname(p), u", ".join(others) or u"none"))
    log.append(u"SVG opened: %s (%.1f MB)" % (p, os.path.getsize(p) / 1048576.0))
    return p


# ================================================================ the library for pages (load + draw)
def mp_load(log):
    """the MasterplanBase cache (survey m) or None (FLAG)"""
    p = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER, MP_FILE)
    if not os.path.isfile(p):
        log.append(u"FLAG MasterplanBase: %s not found: press MasterplanBase once first" % p)
        return None
    with open(p, encoding="utf-8") as f:
        C = json.load(f)
    log.append(u"MasterplanBase %s of %s: %s, %d layers" % (C.get("version"), C.get("made"), C.get("svg"),
                                                          len(C["layers"])))
    return C


def mp_keys(C, prefix):
    """the cache's layer keys that start with prefix ("yuruyus" -> "yuruyus", "yuruyus/iskele_kenari", ...)"""
    return [k for k in C["layers"] if k == prefix or k.startswith(prefix + "/")]


def mp_draw(C, items, T, k, lim, cid, layers=None, style=None):
    """the cache through the page transform T (survey m -> page mm, k = mm per m), into Basemap-writer items cut to
    clip id cid; layers = a set of key prefixes (None = all but the existing ones: PLACE_GROUP); style keys:
    "area" {key word: hex} for the clipped picture areas, "stamps" True to draw stamp outlines, "lw_min" mm,
    "fill" / "stroke" {key word: hex} to restyle. Returns {key: pieces drawn}"""
    st = style or {}
    pick = (lambda key: any(key == p or key.startswith(p + "/") for p in layers)) if layers else \
        (lambda key: key.split("/")[0] != PLACE_GROUP)
    word = lambda key, d_: next((v for w, v in d_.items() if w in key.split("/")), None)
    x0, y0, x1, y1 = lim
    cnt = {}
    for key, recs in C["layers"].items():
        if not pick(key):
            continue
        for kind, fill, stroke, w, P in recs:
            if kind == "s" and not st.get("stamps"):
                continue
            Q = [T(p) for p in P]
            if len(Q) < 2 or max(q[0] for q in Q) < x0 or min(q[0] for q in Q) > x1 or \
                    max(q[1] for q in Q) < y0 or min(q[1] for q in Q) > y1:
                continue
            if kind == "a":
                fill = word(key, st.get("area") or {}) or word(key, AREA_FILL) or AREA_DEFAULT
            fill = word(key, st.get("fill") or {}) or fill
            stroke = word(key, st.get("stroke") or {}) or stroke
            lw = max(st.get("lw_min", 0.05), (w or 0.0) * k)
            if kind in ("r", "a", "s") and len(Q) >= 3:
                items.append(("poly", [Q], fill, stroke, lw if stroke else 0.0, None, "mp/" + key, 1, None, cid))
            elif stroke:
                items.append(("line", Q, stroke, lw, None, "mp/" + key, 1, cid))
            else:
                continue
            cnt[key] = cnt.get(key, 0) + 1
    return cnt


# ================================================================ main
def build():
    t0 = time.time()
    log = []
    src = svg_file(log)
    stamp = u"%d/%d" % (os.path.getsize(src), int(os.path.getmtime(src)))
    out = os.path.join(CACHE_DIR, MP_FILE)
    if os.path.isfile(out) and not globals().get("rebuild"):
        try:
            with open(out, encoding="utf-8") as f:
                old = json.load(f)
            if old.get("svg_stamp") == stamp:                # v1.2: the same SVG = no rebuild (any version)
                return u"cache up to date (%s, %s): nothing rebuilt (set rebuild to True to force)\n%s %s, 0 FLAG " \
                       u"line(s), %.1f s" % (out, os.path.basename(src), GH_LABEL, VERSION, time.time() - t0)
        except Exception:
            pass
    log.append(u"SVG: %s (%.1f MB)" % (src, os.path.getsize(src) / 1e6))
    site = site_alan(log)
    layers, texts, box = read_svg(src, log)
    if box[0] > box[2]:
        raise RuntimeError(u"no group %s in the SVG: it places the plan" % PLACE_GROUP)
    W, upm = world_matrix(site, (box[0], box[1], box[2] - box[0], box[3] - box[1]), log)
    sw = 1.0 / upm
    rd = lambda p: [round(c, 2) for c in mat_pt(W, p)]
    L = {}
    for key, recs in layers.items():
        L[key] = [[kind, fill, stroke, round(w * sw, 3), [rd(p) for p in P]] for kind, fill, stroke, w, P in recs]
    T_ = [[key, s_, round(mat_pt(W, (x, y))[0], 2), round(mat_pt(W, (x, y))[1], 2), round(sz * sw, 2)]
          for key, s_, x, y, sz in texts]
    # check: his existing building outlines against MapBase's buildings
    chk = u"not checked (no MapBase cache)"
    try:
        ns = {"__name__": "bergama_mapbase_lib"}
        mbp = max(glob.glob(os.path.join(BERGAMA_ROOT, "scripts", "bergama_mapbase_v*.py")),
                  key=lambda p: [int(x) for x in re.findall(r"\d+", os.path.basename(p))])
        with open(mbp, encoding="utf-8") as f:
            code = f.read()
        exec(compile(code[:code.index("\n# ================================================================ main\n")], mbp,
                     "exec"), ns)
        ns["BERGAMA_ROOT"] = BERGAMA_ROOT
        MB = ns["mb_load"](log)
        if MB:
            grid = {}
            for R, *_ in MB["bld"]:
                xs, ys = [p[0] for p in R], [p[1] for p in R]
                for i in range(int(min(xs) // 20), int(max(xs) // 20) + 1):
                    for j in range(int(min(ys) // 20), int(max(ys) // 20) + 1):
                        grid.setdefault((i, j), []).append(R)

            def inside(x, y, R):
                c = False
                for (x1_, y1_), (x2_, y2_) in zip(R, R[1:] + R[:1]):
                    if (y1_ > y) != (y2_ > y) and x < x1_ + (y - y1_) * (x2_ - x1_) / (y2_ - y1_):
                        c = not c
                return c
            mine = [r for key, recs in L.items() if CHECK_GROUP in key.split("/") for r in recs if r[0] == "r"]
            hit = 0
            for r in mine:
                cx = sum(p[0] for p in r[4]) / len(r[4])
                cy = sum(p[1] for p in r[4]) / len(r[4])
                if any(inside(cx, cy, R) for R in grid.get((int(cx // 20), int(cy // 20)), [])):
                    hit += 1
            pct = 100.0 * hit / len(mine) if mine else 0.0
            chk = u"%d of %d of his existing building outlines (%.0f %%) have their middle inside a MapBase building" % (
                hit, len(mine), pct)
            log.append(u"check: " + chk)
            if pct < 60.0:
                log.append(u"FLAG check: under 60 %%: the placing is off; look at the review PNGs")
    except Exception as ex:
        log.append(u"FLAG check not done (%s: %s)" % (type(ex).__name__, ex))
    os.makedirs(CACHE_DIR, exist_ok=True)
    C = {"what": u"Aras's masterplan SVG in survey metres, read once by MasterplanBase (see the script's notes); "
                 u"kinds: r ring, l line, a clipped picture area, s picture stamp; fill / stroke hex, width m",
         "version": VERSION, "made": time.strftime("%Y-%m-%d %H:%M"), "svg": os.path.basename(src),
         "svg_stamp": stamp, "matrix": list(W), "units_per_m": upm, "svg_box": box, "check": chk,
         "layers": L, "texts": T_}
    with open(out, "w", encoding="utf-8") as f:
        json.dump(C, f, ensure_ascii=False)
    log.append(u"cache: %s (%.1f MB)" % (out, os.path.getsize(out) / 1e6))
    log.append(u"layers: " + u", ".join(u"%s %d" % (k_, len(v)) for k_, v in sorted(L.items())))
    try:
        review(C, box, W, upm, log)
    except Exception as ex:
        log.append(u"FLAG review PNGs not made (%s: %s)" % (type(ex).__name__, ex))
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


def review(C, box, W, upm, log):
    """the cache over MapBase on one A3-wide sheet, site_alan turned flat as in his file (pages_common pc_write ->
    PDF + review PNGs, whole page)"""
    p = os.path.join(BERGAMA_ROOT, "Data", "bergama_pages_common.py")
    G = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), G)
    lib = G["pc_lib"](log)
    D = G["pc_data"](log)
    K = D["key"]
    a, b, c, d, e, f_ = W                                # survey -> SVG units: the inverse of W
    det = a * d - b * c
    inv = lambda q: ((d * (q[0] - e) - c * (q[1] - f_)) / det, (-b * (q[0] - e) + a * (q[1] - f_)) / det)
    sc = 396.0 / (box[2] - box[0])
    k = sc * upm

    class RM(G["Map"]):
        def __init__(self):
            self.den, self.k = 1000.0 / k, k
            self.mw, self.mh = 396.0, (box[3] - box[1]) * sc
            self.x0, self.y0 = 12.0, 12.0
            self.w, self.h = 420.0, self.mh + 24.0
            self.box = (12.0, 12.0, 408.0, 12.0 + self.mh)
            self.b = None

        def T(self, p):
            u, v = inv(p)
            return (12.0 + (u - box[0]) * sc, 12.0 + (box[3] - v) * sc)
    M = RM()
    items = G["pc_mapbase"](M, K, log, {"buildings", "water", "streets"}, {"lc_light": 0.9})[0]
    cnt = mp_draw(C, items, M.T, M.k, M.box, "map")
    items.append(("poly", [[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]],
                  None, "2B2B2B", 0.25, None, "frame", 1, None, None))
    log.append(u"review drawn: " + u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())))
    G["pc_write"](lib, M, items, OUT_DIR, "MasterplanBase_check", u"MasterplanBase over MapBase", log)


main = build


# ---- Grasshopper wiring (same in every script) ----
def chain_fire(v, key):
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if x is not None), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done "):
        return False
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid)              # noqa: F821
        except Exception:
            pass
        if _scx.sticky.get(key) == s:
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def done_text(ran, ok, secs):
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed = any(v is True for k, v in list(globals().items())
                   if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done")) or \
        any(chain_fire(v, _k + "_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-900:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
