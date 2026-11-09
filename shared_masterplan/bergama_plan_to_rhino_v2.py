# -*- coding: utf-8 -*-
"""Bergama Group 6: PLAN TO RHINO v2 (8 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.

v2 (Aras 8 Nov 10:24-10:47 UTC, shared masterplan): works after SharedSync v1 (bergama_shared_sync_v1.py), which puts
the combined master plan in Data/assets/plan/ (masterplan_latest.svg) and has already copied every Rhino edit into it.
  - after a SharedSync run every layer is baked fresh from the master (nothing is kept: your Rhino edits are already
    in the master, or in master/conflicts/ if a newer edit of the same layer won)
  - every baked object carries the SVG group it came from (user text bergama_unit); the file keeps the placing
    (SVG -> survey) and the pieces per group, so SharedSync can write Rhino edits back into the SVG
  - planting_area_<species> groups -> layer proposal_planting_<species> (the planting analysis reads them)
  - run input also takes the 'done' output of SharedSync (wire it in: one press runs the chain)

Aras 8 Nov 2026 09:50-09:59 UTC: his own edited masterplan SVG is the plan. This script copies it, as it is, into the
open Bergama_Altlik.3dm at the survey's own coordinates (nothing is redrawn or regenerated):
  masterplan::proposal_<thing>   what the project adds   (proposal_green, proposal_paths, ...)
  masterplan::existing_<thing>   what is on the site now (existing_housing, existing_roads, ...)
  masterplan::texts_proposal_<thing> / texts_existing_<thing> / texts_sheet   every text, with the thing it names
  masterplan::sheet              frame, title, legend
A layer you changed in Rhino after a bake (anything added, moved or deleted) is never cleared or baked over again
(Aras 8 Nov 10:05 UTC); the log names it. Delete such a layer yourself to have it baked fresh.
Each top group of the SVG -> one layer (table LAYER_MAP, Data/bergama_plan_to_rhino_data.py if present); each group
inside it -> one Rhino group; each SVG symbol (trees, his urban asset pieces) -> one Rhino block, placed as instances.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file.
  input  run          Button: the script does nothing until it is pressed
  input  LineDrawing  Boolean Toggle: True = bake the plan (the last bake is cleared first); False = nothing baked
  input  ShowSurvey   Boolean Toggle: False = every layer outside masterplan hidden; True = those layers shown again
  output log          the last run's report
  output done         "done HH:MM:SS.ss · N s" after a good run
The SVG: the newest .svg in Downloads/Bergama/Data/assets/plan/ (drop each new edit there; the newest file wins).
The file is NOT saved by the script: save it yourself (Ctrl+S) when the bake looks right.
"""
import os, time, math, re, base64

# ---- SETTINGS ----
VERSION = "v2"
GH_LABEL = "PlanToRhino"
OUT_FOLDER = "bergama_plan_to_rhino"
LOG_NAME = "bergama_plan_to_rhino_log.txt"
ROOT_LAYER = "masterplan"
SITE_LAYER = "site_alan"
PLAN_SUBDIR = os.path.join("assets", "plan")      # under Downloads/Bergama/Data/
CAP = 0.716                                       # Arial capital height / font size (Rhino sizes text by capitals)
VIS_KEY = "bergama_plan_to_rhino"                 # document string: the layers this script hid

# SVG top group (its id, without Illustrator's _2 / 1 copies) -> layer under masterplan. First match wins (prefix).
# "texts" = the texts layer: each text then goes to texts_<layer of what it names>.
LAYER_MAP = [
    ("green_around_the_zone", "existing_green"),
    ("heritage", "existing_heritage"),
    ("ground", "existing_topography"),
    ("topo", "existing_topography"),
    ("water", "proposal_water"),
    ("duvar", "existing_walls"),
    ("survey_walls", "existing_walls"),
    ("roads", "existing_roads"),
    ("houses", "existing_housing"),
    ("places", "proposal_places"),
    ("walks", "proposal_paths"),
    ("paths", "proposal_paths"),
    ("people", "proposal_people"),
    ("trees", "proposal_green"),
    ("planting", "proposal_green"),
    ("terraces", "proposal_terraces"),
    ("annotations", "proposal_annotations"),
    ("sheet", "sheet"),
    ("texts", "texts"),
]
CALLOUT_LAYER = "proposal_annotations"            # a text inside one of its filled boxes names a place
CALLOUT_TEXT_LAYER = "texts_proposal_places"

# ---- Bergama folders (template block, SCRIPT_STANDARD §9) ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


DATA_DIR = os.path.join(BERGAMA_ROOT, "Data")
OUT_DIR = bg_output(OUT_FOLDER)
CACHE_DIR = bg_cache(OUT_FOLDER)
LOG_DIR = bg_logs()


def data_file(name):
    p = os.path.join(DATA_DIR, name)
    return p if os.path.isfile(p) else None


# =====================================================================================================  SVG reading
_NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
SVGNS = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"
INHERIT = ("fill", "stroke", "stroke-width", "fill-rule", "font-size", "font-family", "font-weight", "visibility",
           "stroke-dasharray", "stroke-linecap", "fill-opacity", "stroke-opacity")


def mat_mul(a, b):
    """affine a*b (a after b); (a, b, c, d, e, f) = x' = a x + c y + e, y' = b x + d y + f"""
    return (a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1],
            a[0] * b[2] + a[2] * b[3], a[1] * b[2] + a[3] * b[3],
            a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5])


ID = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)


def mat_pt(m, p):
    return (m[0] * p[0] + m[2] * p[1] + m[4], m[1] * p[0] + m[3] * p[1] + m[5])


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
    """Illustrator's <style>: '.st0, .st1 { fill: #6a6760; }' -> {class: {prop: value}} (rules merged in order)"""
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


def parse_color(v):
    """'#rgb' / '#rrggbb' / 'rgb(r,g,b)' / a few names -> (r, g, b) 0-255, or None (none, url(...), unknown)"""
    if not v:
        return None
    v = v.strip().lower()
    if v in ("none", "transparent") or v.startswith("url("):
        return None
    if v.startswith("#"):
        h = v[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        try:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
        except Exception:
            return None
    if v.startswith("rgb"):
        n = [float(x) for x in _NUM.findall(v)[:3]]
        if "%" in v:
            n = [x * 2.55 for x in n]
        return tuple(int(round(max(0, min(255, x)))) for x in n) if len(n) == 3 else None
    return {"black": (0, 0, 0), "white": (255, 255, 255), "red": (255, 0, 0), "green": (0, 128, 0),
            "blue": (0, 0, 255), "gray": (128, 128, 128), "grey": (128, 128, 128)}.get(v)


def path_segments(d):
    """SVG path data -> [(closed, [start, ('L', p) | ('C', c1, c2, p), ...])] in the path's own units.
    Arcs become cubic pieces, quadratics are raised to cubics."""
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
            cmd = "l" if rel else "L"                    # later pairs are line-tos
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
    """SVG elliptical arc -> cubic pieces (W3C implementation notes F.6)"""
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

    def ang(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a
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
    """rect / circle / ellipse / line / polygon / polyline -> the same form as path_segments"""
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


def tx_subpaths(subs, m):
    out = []
    for cl, s in subs:
        q = [mat_pt(m, s[0])]
        for seg in s[1:]:
            if seg[0] == "L":
                q.append(("L", mat_pt(m, seg[1])))
            else:
                q.append(("C", mat_pt(m, seg[1]), mat_pt(m, seg[2]), mat_pt(m, seg[3])))
        out.append((cl, q))
    return out


def mat_scale(m):
    return math.sqrt(abs(m[0] * m[3] - m[1] * m[2])) or 1.0


def first_num(v, dflt):
    n = _NUM.findall(v or "")
    return float(n[0]) if n else dflt


def el_clip(el, st):
    """the clipPath id an element points at (attribute, class or style), or None"""
    v = el.get("clip-path") or (st.get("clip-path") if st.get("clip-path") and el.get("class") else None)
    m = re.search(r"url\(\s*#([^)\s]+)\s*\)", v or "")
    return m.group(1) if m else None


def _flat(s, n=8):
    """one subpath with its curves as points (only for pieces cut by the frame)"""
    pts, last = [s[0]], s[0]
    for seg in s[1:]:
        if seg[0] == "L":
            pts.append(seg[1])
        else:
            a, b, c, e = last, seg[1], seg[2], seg[3]
            for k in range(1, n + 1):
                t = k / float(n)
                pts.append(tuple((1 - t) ** 3 * a[i] + 3 * (1 - t) ** 2 * t * b[i] + 3 * (1 - t) * t * t * c[i] +
                                 t ** 3 * e[i] for i in range(2)))
        last = pts[-1]
    return pts


def _sh_clip(P, F):
    """Sutherland-Hodgman: ring P cut to rectangle F = (x, y, w, h)"""
    x0, y0, x1, y1 = F[0], F[1], F[0] + F[2], F[1] + F[3]
    for inside, cut in ((lambda p: p[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
                        (lambda p: p[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
                        (lambda p: p[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
                        (lambda p: p[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1))):
        if not P:
            break
        out = []
        for i in range(len(P)):
            a, b = P[i - 1], P[i]
            if inside(b):
                if not inside(a):
                    out.append(cut(a, b))
                out.append(b)
            elif inside(a):
                out.append(cut(a, b))
        P = out
    return P


def _line_clip(P, F):
    """an open polyline cut to rectangle F: the pieces inside (Liang-Barsky per segment)"""
    x0, y0, x1, y1 = F[0], F[1], F[0] + F[2], F[1] + F[3]
    pieces, cur = [], []
    for a, b in zip(P[:-1], P[1:]):
        t0, t1, dx, dy = 0.0, 1.0, b[0] - a[0], b[1] - a[1]
        ok = True
        for p_, q_ in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if p_ == 0:
                if q_ < 0:
                    ok = False
                    break
            else:
                r = q_ / p_
                if p_ < 0:
                    t0 = max(t0, r)
                else:
                    t1 = min(t1, r)
        if not ok or t0 > t1:
            if len(cur) > 1:
                pieces.append(cur)
            cur = []
            continue
        pa = (a[0] + t0 * dx, a[1] + t0 * dy)
        pb = (a[0] + t1 * dx, a[1] + t1 * dy)
        if not cur or cur[-1] != pa:
            if len(cur) > 1:
                pieces.append(cur)
            cur = [pa]
        cur.append(pb)
        if t1 < 1.0:
            pieces.append(cur)
            cur = []
    if len(cur) > 1:
        pieces.append(cur)
    return pieces


def clip_to_frame(items, F):
    """pieces the SVG cuts at the plan frame are cut the same way: whole pieces outside dropped, pieces across the
    edge cut (their curves turned to fine points there), pieces inside kept as they are. Returns pieces cut."""
    x0, y0, x1, y1 = F[0], F[1], F[0] + F[2], F[1] + F[3]
    keep, n_cut = [], 0
    for it in items:
        if not it.get("fc"):
            keep.append(it)
            continue
        if it["kind"] == "shape":
            subs = []
            for cl, s in it["subs"]:
                P = _flat(s, 1)
                if all(x0 <= p[0] <= x1 and y0 <= p[1] <= y1 for p in P):
                    subs.append((cl, s))
                    continue
                if max(p[0] for p in P) < x0 or min(p[0] for p in P) > x1 or max(p[1] for p in P) < y0 or \
                        min(p[1] for p in P) > y1:
                    continue
                n_cut += 1
                Q = _flat(s)
                if it["fill"] is not None:
                    R = _sh_clip(Q, F)
                    if len(R) >= 3:
                        if it["stroke"] is not None:   # the cut edge must not get a stroke: fill and stroke apart
                            keep.append(dict(it, subs=[(True, [R[0]] + [("L", p) for p in R[1:]])], stroke=None))
                            for L in _line_clip(Q + ([Q[0]] if cl else []), F):
                                keep.append(dict(it, subs=[(False, [L[0]] + [("L", p) for p in L[1:]])], fill=None))
                        else:
                            subs.append((True, [R[0]] + [("L", p) for p in R[1:]]))
                else:
                    for L in _line_clip(Q + ([Q[0]] if cl else []), F):
                        subs.append((False, [L[0]] + [("L", p) for p in L[1:]]))
            if subs:
                keep.append(dict(it, subs=subs))
        elif it["kind"] in ("block", "text"):
            p = (it["m"][4], it["m"][5]) if it["kind"] == "block" else it["p"]
            if x0 <= p[0] <= x1 and y0 <= p[1] <= y1:
                keep.append(it)
        elif it["kind"] == "image":
            P = (it["tl"], it["tr"], it["bl"])
            if not (max(p[0] for p in P) < x0 or min(p[0] for p in P) > x1 or max(p[1] for p in P) < y0 or
                    min(p[1] for p in P) > y1):
                keep.append(it)                      # images are not cut: Rhino cannot crop a picture frame
        else:
            keep.append(it)
    items[:] = keep
    return n_cut


class Plan(object):
    """The SVG read once: items in drawing order. Item = dict(kind, top, grp, ...); geometry in SVG user units."""

    def __init__(self, path):
        import xml.etree.ElementTree as ET
        self.path = path
        self.tree = ET.parse(path)
        self.root = self.tree.getroot()
        self.css = {}
        for st in self.root.iter(SVGNS + "style"):
            self.css.update(parse_css(st.text or ""))
        self.ids = {}
        for el in self.root.iter():
            if el.get("id"):
                self.ids[el.get("id")] = el
        self.items, self.symbols, self.clip_rects, self.clip_ids = [], {}, [], {}
        self.n_clipped, self.n_alpha, self.n_skipped, self.n_hidden = 0, 0, {}, 0
        self.grp_n = 0
        for cp in self.root.iter(SVGNS + "clipPath"):
            for r in cp:
                if r.tag == SVGNS + "rect":
                    try:
                        m = parse_transform(r.get("transform"))
                        x, y, w, h = (first_num(r.get(k), 0.0) for k in ("x", "y", "width", "height"))
                        c = [mat_pt(m, p) for p in ((x, y), (x + w, y + h))]
                        self.clip_rects.append((min(c[0][0], c[1][0]), min(c[0][1], c[1][1]),
                                                abs(c[1][0] - c[0][0]), abs(c[1][1] - c[0][1])))
                        self.clip_ids[cp.get("id")] = (x, y, w, h)
                    except Exception:
                        pass
        style0 = {"fill": "#000000", "stroke": "none", "stroke-width": "1", "font-size": "16",
                  "font-family": "Arial", "font-weight": "normal", "fill-rule": "nonzero"}
        self.frame = max(self.clip_rects, key=lambda r: r[2] * r[3]) if self.clip_rects else None
        self.walk(self.root, ID, style0, None, None, 0)
        self.n_cut = clip_to_frame(self.items, self.frame) if self.frame else 0

    def style_of(self, el, parent):
        st = dict((k, v) for k, v in parent.items() if k in INHERIT)
        st.pop("opacity", None)
        for k in ("fill", "stroke", "stroke-width", "fill-rule", "font-size", "font-family", "font-weight", "opacity",
                  "display", "visibility", "stroke-dasharray", "stroke-linecap", "fill-opacity", "stroke-opacity",
                  "clip-path", "mix-blend-mode"):
            if el.get(k) is not None:
                st[k] = el.get(k)
        for c in (el.get("class") or "").split():
            st.update(self.css.get(c, {}))
        for part in (el.get("style") or "").split(";"):
            if ":" in part:
                k, v = part.split(":", 1)
                st[k.strip().lower()] = v.strip()
        return st

    def skip(self, why):
        self.n_skipped[why] = self.n_skipped.get(why, 0) + 1

    def walk(self, el, m, pst, top, grp, depth, in_symbol=False, hid=False, fc=False):
        for ch in el:
            tag = ch.tag.replace(SVGNS, "") if isinstance(ch.tag, str) else ""
            if tag in ("defs", "clipPath", "mask", "metadata", "style", "title", "desc", "linearGradient",
                       "radialGradient", "pattern", "filter", "marker"):
                if tag == "defs":                        # symbols inside defs are read when a <use> points at them
                    pass
                continue
            if tag == "symbol":
                continue
            st = self.style_of(ch, pst)
            h_ = hid or st.get("display", "").strip() == "none" or st.get("visibility", "").strip() == "hidden"
            if h_ and not hid:
                self.n_hidden += 1                       # hidden in Illustrator: baked, its layer switched off
            mm = mat_mul(m, parse_transform(ch.get("transform")))
            fc_ = fc
            cpv = el_clip(ch, st)
            if cpv:
                r = self.clip_ids.get(cpv)
                if r is not None and self.frame and not in_symbol:
                    a_, b_ = mat_pt(mm, (r[0], r[1])), mat_pt(mm, (r[0] + r[2], r[1] + r[3]))
                    F = self.frame
                    tol_ = 0.002 * max(F[2], F[3])
                    if abs(min(a_[0], b_[0]) - F[0]) < tol_ and abs(min(a_[1], b_[1]) - F[1]) < tol_ and \
                            abs(abs(b_[0] - a_[0]) - F[2]) < tol_ and abs(abs(b_[1] - a_[1]) - F[3]) < tol_:
                        fc_ = True                       # cut at the plan frame, as in the SVG
                    else:
                        self.n_clipped += 1
                else:
                    self.n_clipped += 1
            op = first_num(st.get("opacity"), 1.0)
            if op < 0.999:
                self.n_alpha += 1
            if tag == "g":
                t_, g_ = top, grp
                if depth == 0 or (top is None and depth <= 1):
                    pass
                nm = ch.get("id") or ch.get("data-name")
                if top is None and nm and not re.match(r"^Layer_\d+$", nm) and not in_symbol:
                    t_ = nm                                  # the first named group under the page = the layer
                elif top is None and nm and re.match(r"^Layer_\d+$", nm) and len(
                        [c for c in ch if c.tag == SVGNS + "g"]) < 2:
                    t_ = nm                                  # a drawing layer of his own (Layer_2 ...)
                if t_ is not None and top is not None and grp is None:
                    self.grp_n += 1
                    g_ = u"%s %d" % (top, self.grp_n)      # each group inside a layer = one Rhino group
                self.walk(ch, mm, st, t_, g_, depth + 1, in_symbol, h_, fc_)
                continue
            if tag == "a" or tag == "switch":
                self.walk(ch, mm, st, top, grp, depth + 1, in_symbol, h_, fc_)
                continue
            base = dict(top=top, grp=grp, hid=h_, fc=fc_)
            if tag == "path" or tag in ("rect", "circle", "ellipse", "line", "polygon", "polyline"):
                subs = path_segments(ch.get("d")) if tag == "path" else shape_subpaths(tag, ch)
                if not subs:
                    continue
                fill = parse_color(st.get("fill"))
                stroke = parse_color(st.get("stroke"))
                if fill is None and stroke is None:
                    self.skip("no fill, no stroke")
                    continue
                if tag in ("line", "polyline"):
                    fill = None
                base.update(kind="shape", subs=tx_subpaths(subs, mm), fill=fill, stroke=stroke,
                            lw=first_num(st.get("stroke-width"), 1.0) * mat_scale(mm),
                            dash=bool(st.get("stroke-dasharray") and st.get("stroke-dasharray") != "none"))
                self.items.append(base)
            elif tag == "text":
                self.text(ch, mm, st, base)
            elif tag == "image":
                self.image(ch, mm, base)
            elif tag == "use":
                ref = (ch.get(XLINK) or ch.get("href") or "").lstrip("#")
                tgt = self.ids.get(ref)
                if tgt is None:
                    self.skip("use without target")
                    continue
                mu = mat_mul(mm, (1.0, 0.0, 0.0, 1.0, first_num(ch.get("x"), 0.0), first_num(ch.get("y"), 0.0)))
                ttag = tgt.tag.replace(SVGNS, "")
                if ttag == "symbol":
                    mu = mat_mul(mu, self.viewbox_m(tgt, ch))
                    self.symbol(ref, tgt)
                    base.update(kind="block", sym=ref, m=mu)
                    self.items.append(base)
                elif ttag == "image":
                    self.image(tgt, mat_mul(mu, parse_transform(tgt.get("transform"))), base)
                else:
                    wrap = [tgt]
                    self.walk(wrap and _Wrap(wrap), mu, st, top, grp, depth + 1, in_symbol, h_, fc_)
            else:
                self.skip("element <%s>" % tag)

    def viewbox_m(self, sym, use):
        vb = [float(x) for x in _NUM.findall(sym.get("viewBox") or "")]
        if len(vb) != 4 or vb[2] <= 0 or vb[3] <= 0:
            return ID
        w, h = first_num(use.get("width"), vb[2]), first_num(use.get("height"), vb[3])
        s = min(w / vb[2], h / vb[3])                # preserveAspectRatio xMidYMid meet
        return (s, 0.0, 0.0, s, -vb[0] * s + (w - vb[2] * s) / 2.0, -vb[1] * s + (h - vb[3] * s) / 2.0)

    def symbol(self, ref, el):
        """a symbol read once into its own items (symbol units)"""
        if ref in self.symbols:
            return
        keep, self.items = self.items, []
        self.symbols[ref] = None
        self.walk(el, ID, {"fill": "#000000", "stroke": "none", "stroke-width": "1"}, "_sym", None, 9, True)
        self.symbols[ref] = self.items
        self.items = keep

    def text(self, el, m, st, base):
        parts = []
        x0, y0 = first_num(el.get("x"), 0.0), first_num(el.get("y"), 0.0)
        if el.text and el.text.strip():
            parts.append((el.text, x0, y0, st))
        for ts in el:
            if ts.tag == SVGNS + "tspan":
                s2 = self.style_of(ts, st)
                parts.append((u"".join(ts.itertext()), first_num(ts.get("x"), x0), first_num(ts.get("y"), y0), s2))
        for s, x, y, s2 in parts:
            s = re.sub(r"\s+", " ", s or "").strip()
            if not s:
                continue
            col = parse_color(s2.get("fill")) or (0, 0, 0)
            fs = first_num(s2.get("font-size"), 16.0)
            fam = (s2.get("font-family") or "Arial").split(",")[0].strip().strip("'\"")
            bold = "bold" in (s2.get("font-weight") or "") or (s2.get("font-weight") or "").strip() in ("600", "700", "800", "900") \
                or "Bold" in fam
            fam = re.sub(r"[-_]?(Bold|BoldMT|MT|Regular)$", "", fam) or "Arial"
            if fam.lower().startswith("arial"):
                fam = "Arial"
            anc = (s2.get("text-anchor") or "start").strip()
            it = dict(base, kind="text", s=s, p=mat_pt(m, (x, y)), dirx=(m[0], m[1]), size=fs * mat_scale(m),
                      col=col, bold=bold, font=fam, align={"middle": "C", "end": "R"}.get(anc, "L"))
            self.items.append(it)

    def image(self, el, m, base):
        href = el.get(XLINK) or el.get("href") or ""
        w, h = first_num(el.get("width"), 0.0), first_num(el.get("height"), 0.0)
        x, y = first_num(el.get("x"), 0.0), first_num(el.get("y"), 0.0)
        if not href.startswith("data:image") or w <= 0 or h <= 0:
            self.skip("image not embedded")
            return
        try:
            head, b64 = href.split(",", 1)
            data = base64.b64decode(b64)
        except Exception:
            self.skip("image unreadable")
            return
        ext = ".png" if "png" in head else ".jpg"
        base = dict(base, kind="image", data=data, ext=ext, tl=mat_pt(m, (x, y)), tr=mat_pt(m, (x + w, y)),
                    bl=mat_pt(m, (x, y + h)))
        self.items.append(base)


class _Wrap(list):
    """lets walk() read a referenced element (use -> g/path) as if it were a child"""
    pass


# =====================================================================================================  placing
def site_turn(site):
    """the angle (rad) that turns site_alan's longest side horizontal, its eastern end to the right (B19 b8_site_turn)"""
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
    """SVG user units -> survey metres. The SVG's biggest clip rectangle is the B19 sheet's drawing frame, which IS
    site_alan turned flat (B19 b19_page: the long side horizontal, upstream left). Returns an affine (a..f)."""
    rot = site_turn(site)
    ca, sa = math.cos(rot), math.sin(rot)
    ox, oy = site[0]
    turned = [(ox + ca * (p[0] - ox) - sa * (p[1] - oy), oy + sa * (p[0] - ox) + ca * (p[1] - oy)) for p in site]
    x0, y0 = min(p[0] for p in turned), min(p[1] for p in turned)
    x1, y1 = max(p[0] for p in turned), max(p[1] for p in turned)
    rx, ry, rw, rh = rect
    sx, sy = rw / (x1 - x0), rh / (y1 - y0)
    s = (sx + sy) / 2.0
    notes.append(u"placing: the SVG frame %.2f x %.2f units = site_alan %.1f x %.1f m turned flat (%.4f units per m; "
                 u"width and height agree to %.2f %%)" % (rw, rh, x1 - x0, y1 - y0, s, abs(sx - sy) / s * 100.0))
    if abs(sx - sy) / s > 0.01:
        notes.append(u"WARNING placing: the frame's width and height scales differ by %.1f %%: is the biggest clip "
                     u"rectangle still the plan frame?" % (abs(sx - sy) / s * 100.0))
    # SVG (u, v) -> turned (x0 + (u - rx) / s, y0 + (ry + rh - v) / s) -> world: turn back by -rot round (ox, oy)
    A = (1.0 / s, 0.0, 0.0, -1.0 / s, x0 - rx / s, y0 + (ry + rh) / s)
    Ri = (ca, -sa, sa, ca, ox - ca * ox - sa * oy, oy + sa * ox - ca * oy)
    return mat_mul(Ri, A), 1.0 / s


def layer_for(top):
    key = re.sub(r"(_?\d+)$", "", (top or "").strip()).lower()
    if key.startswith("planting_area_"):            # v2: one layer per species area (planting analysis)
        return u"proposal_planting_" + re.sub(r"[^a-z0-9_]+", "_", key[len("planting_area_"):])
    table = LAYER_MAP
    try:
        p = data_file("bergama_plan_to_rhino_data.py")
        if p:
            g = {}
            exec(open(p, encoding="utf-8").read(), g)
            table = g.get("LAYER_MAP") or table
    except Exception:
        pass
    for k, lay in table:
        if key.startswith(k.lower()):
            return lay
    return None


def item_bbox(it):
    if it["kind"] == "shape":
        xs = [p[0] for cl, s in it["subs"] for p in ([s[0]] + [seg[-1] for seg in s[1:]])]
        ys = [p[1] for cl, s in it["subs"] for p in ([s[0]] + [seg[-1] for seg in s[1:]])]
        return (min(xs), min(ys), max(xs), max(ys))
    if it["kind"] == "block":
        return (it["m"][4] - 1.0, it["m"][5] - 1.0, it["m"][4] + 1.0, it["m"][5] + 1.0)
    if it["kind"] == "image":
        P = (it["tl"], it["tr"], it["bl"])
        return (min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P))
    return None


def edge_dist(it, p):
    """distance from p to a piece's drawn edges (curve pieces by their end points), blocks/images by their box"""
    if it["kind"] != "shape":
        bb = item_bbox(it)
        return math.hypot(max(bb[0] - p[0], 0.0, p[0] - bb[2]), max(bb[1] - p[1], 0.0, p[1] - bb[3]))
    best = float("inf")
    for cl, s in it["subs"]:
        P = [s[0]] + [seg[-1] for seg in s[1:]] + ([s[0]] if cl else [])
        for a, b in zip(P[:-1], P[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L2 = dx * dx + dy * dy
            t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
            best = min(best, math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy))
    return best


def assign_layers(plan, frame, notes):
    """every item gets its layer; texts get texts_<layer of what they name>"""
    unknown = {}
    for it in plan.items:
        lay = layer_for(it["top"]) if it["top"] else None
        if lay is None:
            unknown[it["top"] or u"(outside any group)"] = unknown.get(it["top"] or u"(outside any group)", 0) + 1
            lay = u"unsorted_%s" % re.sub(r"[^A-Za-z0-9_]+", "_", it["top"] or "loose")
        it["layer"] = lay
    if unknown:
        notes.append(u"FLAG layers: SVG groups not in the layer table, put on unsorted_<group> layers: " +
                     u", ".join(u"%s (%d)" % kv for kv in sorted(unknown.items())))
    # texts -> the thing they name
    owners = [(item_bbox(it), it["layer"], it) for it in plan.items
              if it["kind"] != "text" and it["layer"] not in ("sheet", "texts") and not it["layer"].startswith("unsorted")]
    owners = [o for o in owners if o[0] is not None]
    boxes = [(bb, it) for bb, lay, it in owners if lay == CALLOUT_LAYER and it["kind"] == "shape" and it["fill"]
             and (bb[2] - bb[0]) * (bb[3] - bb[1]) < (frame[2] * frame[3]) * 0.002]
    near, n_by = [], {}
    for it in plan.items:
        if it["kind"] != "text":
            continue
        own = it["layer"]
        if own in ("texts", "sheet"):
            x, y = it["p"]
            fx, fy, fw, fh = frame
            if own == "sheet" or not (fx <= x <= fx + fw and fy <= y <= fy + fh):
                tl = "texts_sheet"
            elif any(bb[0] <= x <= bb[2] and bb[1] <= y <= bb[3] for bb, o in boxes):
                tl = CALLOUT_TEXT_LAYER
            else:
                best = None                              # the drawn edge nearest to the text's anchor
                for bb, lay, o in owners:
                    dx = max(bb[0] - x, 0.0, x - bb[2])
                    dy = max(bb[1] - y, 0.0, y - bb[3])
                    if best is not None and math.hypot(dx, dy) >= best[0]:
                        continue
                    d = edge_dist(o, (x, y))
                    if best is None or d < best[0]:
                        best = (d, lay)
                tl = u"texts_" + (best[1] if best else "sheet")
                near.append(u"'%s' -> %s" % (it["s"][:40], tl))
        else:
            tl = u"texts_" + own
        it["layer"] = tl
        n_by[tl] = n_by.get(tl, 0) + 1
    notes.append(u"texts: " + u", ".join(u"%s %d" % kv for kv in sorted(n_by.items())))
    if near:
        notes.append(u"texts given to the nearest object (please check): " + u"; ".join(near))


# =====================================================================================================  Rhino
def bake(doc, plan, M, s_m, notes):
    """the plan into the open Rhino file under ROOT_LAYER; the last bake cleared first. Returns object count."""
    import Rhino
    import System
    rg = Rhino.Geometry
    tol = doc.ModelAbsoluteTolerance
    try:
        u = Rhino.RhinoMath.UnitScale(Rhino.UnitSystem.Meters, doc.ModelUnitSystem)
    except Exception:
        u = 1.0
    W = lambda p: (lambda q: rg.Point3d(q[0] * u, q[1] * u, 0.0))(mat_pt(M, p))
    n_del, keep = clear_bake(doc)
    try:
        if (doc.Strings.GetValue(SYNC_KEY, "rebake_all") or "") == "1":     # v2: SharedSync put every edit in the master
            notes.append(u"SharedSync ran first: every layer baked fresh from the master (Rhino edits are in it)")
            if keep:
                keep2 = set(keep)
                keep = set()
                n_del += clear_layers(doc, keep2)
            doc.Strings.SetString(SYNC_KEY, "rebake_all", "0")
    except Exception as ex_:
        notes.append(u"FLAG SharedSync flag unreadable: %s" % ex_)
    notes.append(u"cleared the last bake: %d objects" % n_del)
    if keep:
        notes.append(u"KEPT as you changed them (not cleared, not baked over): " + u", ".join(sorted(keep)))
    # layers
    lay_ix = {}

    def layer(name):
        if name in lay_ix:
            return lay_ix[name]
        full = ROOT_LAYER if name is None else u"%s::%s" % (ROOT_LAYER, name)
        i = doc.Layers.FindByFullPath(full, -1)
        if i < 0:
            L = Rhino.DocObjects.Layer()
            L.Name = ROOT_LAYER if name is None else name
            if name is not None:
                L.ParentLayerId = doc.Layers[layer(None)].Id
            i = doc.Layers.Add(L)
        lay_ix[name] = i
        return i
    layer(None)
    solid = -1
    for mk in (lambda: doc.HatchPatterns.FindName("Solid").Index,
               lambda: doc.HatchPatterns.Add(Rhino.DocObjects.HatchPattern.Defaults.Solid),
               lambda: doc.HatchPatterns.Add(Rhino.DocObjects.HatchPattern.Defaults.Solid()),
               lambda: doc.HatchPatterns.FindName("SOLID").Index):
        try:
            solid = int(mk())
            if solid >= 0:
                break
        except Exception:
            pass
    if solid < 0:
        notes.append(u"FLAG: no Solid hatch pattern in this file: fills cannot be drawn")
    dash_lt = -1
    try:
        lt = doc.Linetypes.FindName("Dashed")
        dash_lt = int(lt.Index) if lt is not None else -1
    except Exception:
        pass
    order = [0]
    groups = {}
    tag = time.strftime("%H%M%S")
    count, fail = {}, {}

    def attr(lix, col, lw=None, dash=False, grp=None):
        a = Rhino.DocObjects.ObjectAttributes()
        a.LayerIndex = lix
        order[0] += 1
        try:
            a.DisplayOrder = order[0]                   # Rhino stacks the pieces in the SVG's order
        except Exception:
            pass
        c = System.Drawing.Color.FromArgb(255, col[0], col[1], col[2])
        a.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        a.ObjectColor = c
        a.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject
        a.PlotColor = c
        if lw is not None:
            a.PlotWeightSource = Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject
            a.PlotWeight = max(0.01, float(lw))
        if dash and dash_lt >= 0:
            a.LinetypeSource = Rhino.DocObjects.ObjectLinetypeSource.LinetypeFromObject
            a.LinetypeIndex = dash_lt
        if grp is not None:
            if grp not in groups:
                groups[grp] = doc.Groups.Add(u"mp %s %s" % (grp, tag))   # a name per run: names stay taken
            if groups[grp] >= 0:
                a.AddToGroup(groups[grp])
        return a

    def curves(subs, P, close_all):
        out = []
        for cl, s in subs:
            cl = cl or close_all
            pc = rg.PolyCurve()
            only_lines = all(seg[0] == "L" for seg in s[1:])
            if only_lines:
                Q = [P(s[0])]
                for seg in s[1:]:
                    q = P(seg[1])
                    if Q[-1].DistanceTo(q) > tol:
                        Q.append(q)
                if cl and len(Q) > 2:
                    if Q[-1].DistanceTo(Q[0]) <= tol:
                        Q[-1] = Q[0]
                    else:
                        Q.append(Q[0])
                if len(Q) < 2:
                    continue
                c = rg.PolylineCurve(Q)
            else:
                last = P(s[0])
                for seg in s[1:]:
                    if seg[0] == "L":
                        q = P(seg[1])
                        if last.DistanceTo(q) > tol:
                            pc.Append(rg.LineCurve(last, q))
                            last = q
                    else:
                        cps = [last, P(seg[1]), P(seg[2]), P(seg[3])]
                        if cps[0].DistanceTo(cps[3]) <= tol and cps[0].DistanceTo(cps[1]) <= tol:
                            continue
                        bz = rg.BezierCurve(cps)
                        pc.Append(bz.ToNurbsCurve())
                        last = cps[3]
                if cl and last.DistanceTo(P(s[0])) > tol:
                    pc.Append(rg.LineCurve(last, P(s[0])))
                if pc.SegmentCount == 0:
                    continue
                c = pc
            if c.IsValid:
                out.append(c)
        return out

    def add_shape(it, P, lix, grp, sink):
        if it["fill"] is not None and solid >= 0:
            cs = [c for c in curves(it["subs"], P, True) if c.IsClosed]
            hs = rg.Hatch.Create(cs, solid, 0.0, 1.0, tol) if cs else None
            for h in hs or []:
                sink(h, attr(lix, it["fill"], grp=grp), "fills")
            if cs and not hs:
                fail["fill"] = fail.get("fill", 0) + 1
        if it["stroke"] is not None:
            for c in curves(it["subs"], P, False):
                sink(c, attr(lix, it["stroke"], lw=it["lw"] * s_m, dash=it["dash"], grp=grp), "lines")

    per_layer = {}

    cur = [None]                                      # v2: the SVG group (unit) of the item being baked
    per_unit, layer_units = {}, {}

    def stamp(a, sig_):
        a.SetUserString(STAMP, sig_)
        if cur[0]:
            a.SetUserString(UNIT_KEY, cur[0])

    def counted(a):
        per_layer[a.LayerIndex] = per_layer.get(a.LayerIndex, 0) + 1
        if cur[0]:
            per_unit[cur[0]] = per_unit.get(cur[0], 0) + 1
            lu = layer_units.setdefault(doc.Layers[a.LayerIndex].FullPath, {})
            lu[cur[0]] = lu.get(cur[0], 0) + 1

    def add_doc(g, a, kind):
        stamp(a, geom_sig(g))
        gid = doc.Objects.Add(g, a)
        if gid != System.Guid.Empty:
            count[kind] = count.get(kind, 0) + 1
            counted(a)
        else:
            fail[kind] = fail.get(kind, 0) + 1
    # blocks: one definition per SVG symbol, named per run (a deleted block name stays taken in the file)
    blk = {}

    def block(ref):
        if ref in blk:
            return blk[ref]
        blk[ref] = -1
        geos, atts = [], []
        Pl = lambda p: rg.Point3d(p[0], -p[1], 0.0)     # symbol units, y turned up (the instance turns it back)

        def sink(g, a, kind):
            a2 = Rhino.DocObjects.ObjectAttributes()
            a2.LayerIndex = layer(None)                 # inside the block on masterplan itself: hiding a survey
            a2.ColorSource = a.ColorSource              # layer never hides the trees
            a2.ObjectColor = a.ObjectColor
            a2.PlotColorSource = a.PlotColorSource
            a2.PlotColor = a.PlotColor
            a2.PlotWeightSource = a.PlotWeightSource
            a2.PlotWeight = a.PlotWeight
            geos.append(g)
            atts.append(a2)
        for sit in plan.symbols.get(ref) or []:
            if sit["kind"] == "shape":
                add_shape(sit, Pl, 0, None, sink)
        if geos:
            nm = u"mp_%s_%s" % (re.sub(r"[^A-Za-z0-9_]+", "_", ref), tag)
            i = doc.InstanceDefinitions.Add(nm, u"plan to Rhino: SVG symbol %s" % ref, rg.Point3d.Origin, geos, atts)
            blk[ref] = i
        if blk[ref] < 0:
            fail["block definition"] = fail.get("block definition", 0) + 1
        return blk[ref]
    img_dir = os.path.join(CACHE_DIR, "images")
    os.makedirs(img_dir, exist_ok=True)
    n_img = [0]
    for it in plan.items:
        if u"%s::%s" % (ROOT_LAYER, it["layer"]) in keep:
            continue
        lix = layer(it["layer"])
        cur[0] = it.get("top")
        grp = it.get("grp")
        try:
            if it["kind"] == "shape":
                add_shape(it, W, lix, grp, add_doc)
            elif it["kind"] == "block":
                bi = block(it["sym"])
                if bi < 0:
                    continue
                m = mat_mul(M, mat_mul(it["m"], (1.0, 0.0, 0.0, -1.0, 0.0, 0.0)))   # undo the y turn of the definition
                xf = rg.Transform(1.0)
                xf.M00, xf.M01, xf.M03 = m[0] * u, m[2] * u, m[4] * u
                xf.M10, xf.M11, xf.M13 = m[1] * u, m[3] * u, m[5] * u
                a_i = attr(lix, (0, 0, 0), grp=grp)
                stamp(a_i, u"I%.3f,%.3f" % (xf.M03, xf.M13))
                gid = doc.Objects.AddInstanceObject(bi, xf, a_i)
                if gid != System.Guid.Empty:
                    count["blocks placed"] = count.get("blocks placed", 0) + 1
                    counted(a_i)
                else:
                    fail["block placed"] = fail.get("block placed", 0) + 1
            elif it["kind"] == "text":
                p = W(it["p"])
                dx, dy = it["dirx"]
                d = mat_pt(M, (it["p"][0] + dx, it["p"][1] + dy))
                q = mat_pt(M, it["p"])
                xa = rg.Vector3d(d[0] - q[0], d[1] - q[1], 0.0)
                if not xa.Unitize():
                    xa = rg.Vector3d.XAxis
                ya = rg.Vector3d.CrossProduct(rg.Vector3d.ZAxis, xa)
                te = rg.TextEntity.Create(it["s"], rg.Plane(p, xa, ya), doc.DimStyles.Current, False, 0.0, 0.0)
                te.TextHeight = it["size"] * s_m * u * CAP
                try:
                    te.DimensionScale = 1.0
                except Exception:
                    pass
                try:
                    te.Font = Rhino.DocObjects.Font.FromQuartetProperties(it["font"], bool(it["bold"]), False)
                except Exception:
                    pass
                try:
                    te.TextHorizontalAlignment = {"L": Rhino.DocObjects.TextHorizontalAlignment.Left,
                                                  "C": Rhino.DocObjects.TextHorizontalAlignment.Center,
                                                  "R": Rhino.DocObjects.TextHorizontalAlignment.Right}[it["align"]]
                    te.TextVerticalAlignment = Rhino.DocObjects.TextVerticalAlignment.Bottom
                except Exception:
                    pass
                try:
                    te.MaskEnabled = False
                except Exception:
                    pass
                a_t = attr(lix, it["col"], grp=grp)
                stamp(a_t, geom_sig(te))
                gid = doc.Objects.AddText(te, a_t)
                if gid != System.Guid.Empty:
                    count["texts"] = count.get("texts", 0) + 1
                    counted(a_t)
                else:
                    fail["text"] = fail.get("text", 0) + 1
            elif it["kind"] == "image":
                n_img[0] += 1
                fn = os.path.join(img_dir, u"image_%03d%s" % (n_img[0], it["ext"]))
                with open(fn, "wb") as fh:
                    fh.write(it["data"])
                o = W(it["bl"])
                tr_bl = mat_pt(M, it["tr"])
                bl = mat_pt(M, it["bl"])
                tl = mat_pt(M, it["tl"])
                br = (tr_bl[0] - tl[0] + bl[0], tr_bl[1] - tl[1] + bl[1])
                xa = rg.Vector3d((br[0] - bl[0]) * u, (br[1] - bl[1]) * u, 0.0)
                ya = rg.Vector3d((tl[0] - bl[0]) * u, (tl[1] - bl[1]) * u, 0.0)
                w_, h_ = xa.Length, ya.Length
                if w_ <= 0 or h_ <= 0:
                    continue
                pl = rg.Plane(o, xa, ya)
                gid = doc.Objects.AddPictureFrame(pl, fn, False, w_, h_, True, True)
                if gid != System.Guid.Empty:
                    count["images"] = count.get("images", 0) + 1
                    ob = doc.Objects.FindId(gid)
                    if ob is not None:
                        a = ob.Attributes.Duplicate()
                        a.LayerIndex = lix
                        order[0] += 1
                        try:
                            a.DisplayOrder = order[0]
                        except Exception:
                            pass
                        if grp is not None and groups.get(grp, -1) >= 0:
                            a.AddToGroup(groups[grp])
                        stamp(a, geom_sig(ob.Geometry))
                        counted(a)
                        ob.Attributes = a
                        ob.CommitChanges()
                else:
                    fail["image"] = fail.get("image", 0) + 1
        except Exception as ex:
            k = u"%s (%s: %s)" % (it["kind"], type(ex).__name__, str(ex)[:60])
            fail[k] = fail.get(k, 0) + 1
    try:                                              # v2: what SharedSync needs to write Rhino edits back
        import json as _json
        doc.Strings.SetString(VIS_KEY, "v2_matrix", _json.dumps(dict(M=list(M), s_m=s_m, u=u, svg=PLAN_FILE[0])))
        doc.Strings.SetString(VIS_KEY, "v2_unit_count", _json.dumps(per_unit))
        doc.Strings.SetString(VIS_KEY, "v2_layer_unit", _json.dumps(
            dict((k, max(v, key=v.get)) for k, v in layer_units.items())))
    except Exception as ex_:
        notes.append(u"FLAG placing not saved in the file (SharedSync cannot write Rhino edits back): %s" % ex_)
    for lx, n_ in per_layer.items():                  # how many pieces each layer got: a later run checks it
        try:
            doc.Strings.SetString(VIS_KEY + "_count", doc.Layers[lx].FullPath, str(n_))
        except Exception:
            pass
    shown = {}
    for it in plan.items:                             # a layer whose pieces were all hidden in Illustrator: off
        shown[it["layer"]] = shown.get(it["layer"], False) or not it.get("hid")
    off = []
    for lay, vis in shown.items():
        i = lay_ix.get(lay)
        if i is not None and doc.Layers[i].IsVisible != vis:
            doc.Layers[i].IsVisible = vis
            try:
                doc.Layers.Modify(doc.Layers[i], i, True)
            except Exception:
                pass
        if not vis:
            off.append(lay)
    if off:
        notes.append(u"layers switched off (hidden in your SVG): " + u", ".join(sorted(off)))
    by_layer = {}
    for it in plan.items:
        by_layer[it["layer"]] = by_layer.get(it["layer"], 0) + 1
    notes.append(u"layers under %s: " % ROOT_LAYER + u", ".join(u"%s %d" % kv for kv in sorted(by_layer.items())))
    notes.append(u"Rhino objects: " + u", ".join(u"%s %d" % kv for kv in sorted(count.items())) +
                 u"; %d block definitions; %d Rhino groups" % (len([b for b in blk.values() if b >= 0]), len(groups)))
    if fail:
        notes.append(u"FLAG not drawn: " + u", ".join(u"%s %d" % kv for kv in sorted(fail.items())))
    return sum(count.values())


STAMP = "bergama_plan_to_rhino"                    # user text on every baked object: where it was baked
UNIT_KEY = "bergama_unit"                          # v2: user text: the SVG group the object came from
SYNC_KEY = "bergama_shared_sync"                   # v2: document strings written by SharedSync
PLAN_FILE = [""]


def clear_layers(doc, paths):
    """v2: every object on these layer paths deleted (SharedSync already put their edits in the master)"""
    import Rhino
    es = Rhino.DocObjects.ObjectEnumeratorSettings()
    es.HiddenObjects = True
    es.LockedObjects = True
    ix = set(l.Index for l in doc.Layers if not l.IsDeleted and l.FullPath in paths)
    n = 0
    for o in list(doc.Objects.GetObjectList(es)):
        if o.Attributes.LayerIndex in ix:
            if doc.Objects.Delete(o.Id, True):
                n += 1
    return n


def geom_sig(g):
    """a piece's place when baked: its bounding-box centre (blocks: their insertion point)"""
    try:
        import Rhino
        if isinstance(g, Rhino.Geometry.InstanceReferenceGeometry):
            x = g.Xform
            return u"I%.3f,%.3f" % (x.M03, x.M13)
        if isinstance(g, Rhino.Geometry.TextEntity):     # a text's box depends on its font: its anchor is steadier
            o = g.Plane.Origin
            return u"T%.3f,%.3f" % (o.X, o.Y)
        c = g.GetBoundingBox(True).Center
        return u"%.3f,%.3f" % (c.X, c.Y)
    except Exception:
        return u"?"


def obj_sig(o):
    try:
        import Rhino
        if isinstance(o, Rhino.DocObjects.InstanceObject):
            x = o.InstanceXform
            return u"I%.3f,%.3f" % (x.M03, x.M13)
    except Exception:
        pass
    return geom_sig(o.Geometry)


def clear_bake(doc):
    """every object on ROOT_LAYER's sub-layers deleted, then the plan's old blocks (mp_*) purged; a layer Aras has
    changed since the bake (a piece without the bake stamp, a piece moved, or fewer pieces than baked) is kept whole.
    Returns (deleted, kept layer paths)."""
    import Rhino
    import System
    lays = dict((l.Index, l.FullPath) for l in doc.Layers if not l.IsDeleted and
                (l.FullPath == ROOT_LAYER or l.FullPath.startswith(ROOT_LAYER + "::")))
    if not lays:
        return 0, set()
    es = Rhino.DocObjects.ObjectEnumeratorSettings()
    es.HiddenObjects = True
    es.LockedObjects = True
    on = {}
    for o in doc.Objects.GetObjectList(es):
        if o.Attributes.LayerIndex in lays:
            on.setdefault(o.Attributes.LayerIndex, []).append(o)
    keep = set()
    for lx, objs in on.items():
        try:
            n0 = int(doc.Strings.GetValue(VIS_KEY + "_count", lays[lx]) or -1)
        except Exception:
            n0 = -1
        changed = n0 >= 0 and len(objs) != n0
        if not changed:
            for o in objs:
                st = o.Attributes.GetUserString(STAMP)
                if not st or st != obj_sig(o):
                    changed = True
                    break
        if changed:
            keep.add(lays[lx])
    keep_ix = set(lx for lx, p in lays.items() if p in keep)
    ids = [o.Id for lx, objs in on.items() if lx not in keep_ix for o in objs]
    n = 0
    try:
        from System.Collections.Generic import List as _L
        gl = _L[System.Guid]()
        for i in ids:
            gl.Add(i)
        n = int(doc.Objects.Delete(gl, True))
    except Exception:
        for i in ids:
            if doc.Objects.Delete(i, True):
                n += 1
    in_use = set()
    for lx in keep_ix:                                  # blocks still placed on a kept layer stay
        for o in on.get(lx, []):
            try:
                if isinstance(o, Rhino.DocObjects.InstanceObject):
                    in_use.add(o.InstanceDefinition.Name)
            except Exception:
                pass
    try:                                                # the old run's empty Rhino groups
        for gi in range(doc.Groups.Count - 1, -1, -1):
            g_ = doc.Groups.FindIndex(gi)
            if g_ is not None and (g_.Name or u"").startswith(u"mp ") and not doc.Groups.GroupMembers(gi):
                doc.Groups.Delete(gi)
    except Exception:
        pass
    for d in list(doc.InstanceDefinitions):
        try:
            if d is not None and not d.IsDeleted and d.Name.startswith(u"mp_") and d.Name not in in_use:
                doc.InstanceDefinitions.Delete(d.Index, True, True)
                try:
                    doc.InstanceDefinitions.Purge(d.Index)
                except Exception:
                    pass
        except Exception:
            pass
    return n, keep


def survey_visibility(doc, show, notes):
    """show = False: every top layer outside ROOT_LAYER hidden (their names kept in the file's document strings);
    show = True: the layers this script hid shown again"""
    root = doc.Layers.FindByFullPath(ROOT_LAYER, -1)
    try:
        hidden = [s for s in (doc.Strings.GetValue(VIS_KEY, "hidden") or "").split("\n") if s]
    except Exception:
        hidden = []
    if show:
        n = 0
        for full in hidden:
            i = doc.Layers.FindByFullPath(full, -1)
            if i >= 0 and not doc.Layers[i].IsVisible:
                doc.Layers[i].IsVisible = True
                try:
                    doc.Layers.Modify(doc.Layers[i], i, True)
                except Exception:
                    pass
                n += 1
        try:
            doc.Strings.SetString(VIS_KEY, "hidden", "")
        except Exception:
            pass
        notes.append(u"ShowSurvey True: %d layers shown again" % n)
        return
    if root >= 0:
        try:
            doc.Layers.SetCurrentLayerIndex(root, True)   # Rhino never hides the current layer
        except Exception:
            pass
    new = []
    for l in doc.Layers:
        if l.IsDeleted or l.ParentLayerId != System_Guid_Empty() or l.FullPath == ROOT_LAYER:
            continue
        if l.IsVisible:
            l.IsVisible = False
            try:
                doc.Layers.Modify(l, l.Index, True)
            except Exception:
                pass
            new.append(l.FullPath)
    all_ = sorted(set(hidden) | set(new))
    try:
        doc.Strings.SetString(VIS_KEY, "hidden", "\n".join(all_))
    except Exception:
        pass
    notes.append(u"ShowSurvey False: %d top layers hidden (%s)" % (len(new), u", ".join(new[:12]) +
                                                               (u" ..." if len(new) > 12 else u"")))


def System_Guid_Empty():
    import System
    return System.Guid.Empty


def read_site(doc):
    """site_alan's corner points (survey m) from the open file"""
    import Rhino
    i = doc.Layers.FindByFullPath(SITE_LAYER, -1)
    if i < 0:
        for l in doc.Layers:
            if not l.IsDeleted and l.Name == SITE_LAYER:
                i = l.Index
                break
    if i < 0:
        return None
    best = None
    for o in doc.Objects.FindByLayer(doc.Layers[i]) or []:
        g = o.Geometry
        if isinstance(g, Rhino.Geometry.Curve):
            ok, pl = g.TryGetPolyline()
            if ok and pl.Count >= 4:
                P = [(p.X, p.Y) for p in pl]
                if P[0] == P[-1]:
                    P = P[:-1]
                a = abs(sum(P[k][0] * P[k - 1][1] - P[k - 1][0] * P[k][1] for k in range(len(P)))) / 2.0
                if best is None or a > best[0]:
                    best = (a, P)
    return best[1] if best else None


def newest_svg():
    d = os.path.join(DATA_DIR, PLAN_SUBDIR)
    try:
        fs = [os.path.join(d, f) for f in os.listdir(d) if f.lower().endswith(".svg")]
    except Exception:
        fs = []
    return max(fs, key=os.path.getmtime) if fs else None


# =====================================================================================================  main
def main(line_drawing, show_survey):
    t0 = time.time()
    notes = [u"%s %s · %s" % (GH_LABEL, VERSION, time.strftime("%Y-%m-%d %H:%M"))]
    import Rhino
    doc = Rhino.RhinoDoc.ActiveDoc
    if doc is None:
        raise RuntimeError("no Rhino file is open")
    if line_drawing:
        svg = newest_svg()
        if svg is None:
            raise RuntimeError("no plan SVG: put your edited plan .svg in " + os.path.join(DATA_DIR, PLAN_SUBDIR))
        notes.append(u"plan SVG: %s (%s, %.1f MB)" % (svg, time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(svg))),
                                                     os.path.getsize(svg) / 1048576.0))
        plan = Plan(svg)
        PLAN_FILE[0] = svg
        notes.append(u"read: %d pieces, %d symbols, %.1f s" % (len(plan.items), len(plan.symbols), time.time() - t0))
        if plan.n_skipped:
            notes.append(u"left out of the SVG: " + u", ".join(u"%s %d" % kv for kv in sorted(plan.n_skipped.items())))
        if plan.n_cut:
            notes.append(u"cut at the plan frame as in the SVG: %d pieces" % plan.n_cut)
        if plan.n_hidden:
            notes.append(u"groups hidden in your SVG: %d (baked, their layers switched off)" % plan.n_hidden)
        if plan.n_clipped or plan.n_alpha:
            notes.append(u"v1 limits: %d other clipping masks not applied (in your 09:18 file these are small squares "
                         u"round single trees: no visible change); %d see-through pieces drawn solid (Rhino bakes "
                         u"no transparency)" % (plan.n_clipped, plan.n_alpha))
        if not plan.clip_rects:
            raise RuntimeError("the SVG has no clip rectangle (the plan frame), so it cannot be placed on site_alan")
        frame = plan.frame
        site = read_site(doc)
        if not site:
            raise RuntimeError("no closed curve on layer %s in the open file: the plan cannot be placed" % SITE_LAYER)
        M, s_m = world_matrix(site, frame, notes)
        assign_layers(plan, frame, notes)
        import scriptcontext as sc_
        sc_doc = sc_.doc
        undo0 = doc.UndoRecordingEnabled
        try:
            sc_.doc = doc
            doc.Views.RedrawEnabled = False
            doc.UndoRecordingEnabled = False
            t1 = time.time()
            n = bake(doc, plan, M, s_m, notes)
            notes.append(u"baked %d objects under layer %s in %.0f s (file NOT saved: Ctrl+S when it looks right)" %
                         (n, ROOT_LAYER, time.time() - t1))
        finally:
            doc.UndoRecordingEnabled = undo0
            doc.Views.RedrawEnabled = True
            sc_.doc = sc_doc
    else:
        notes.append(u"LineDrawing False: nothing baked")
    survey_visibility(doc, bool(show_survey), notes)
    doc.Views.Redraw()
    notes.append(u"%.1f s" % (time.time() - t0))
    return u"\n".join(notes)


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, LOG_NAME), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text


def done_text(ran, ok, secs):
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


def _flag(name):
    v = globals().get(name)
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if x is not None), None)
    return v is True or (isinstance(v, str) and v.strip().lower() == "true")


# ---- Grasshopper wiring (template; the two toggles never count as a press) ----
if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _pressed = globals().get("run") is True or (isinstance(globals().get("run"), list) and True in globals().get("run"))
    _rv = globals().get("run")                        # v2: SharedSync's 'done' wired in = a press, once per new value
    if isinstance(_rv, list):
        _rv = next((x for x in _rv if x is not None), None)
    if isinstance(_rv, str) and _rv.startswith("done ") and _sc.sticky.get(_k + "_chain") != _rv:
        _sc.sticky[_k + "_chain"] = _rv
        _pressed = True
    if _pressed:
        _t0 = time.time()
        try:
            _res = main(_flag("LineDrawing"), _flag("ShowSurvey"))
        except Exception as _ex:
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button. LineDrawing True bakes the plan SVG from " +
                         os.path.join(DATA_DIR, PLAN_SUBDIR))
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
