# -*- coding: utf-8 -*-
"""Bergama Group 6: PLANTING ANALYSIS v1 (8 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.

Aras 8 Nov 2026 10:24 UTC: the planting distribution board (planting_area_diagram_v9, made outside Rhino until now)
rebuilt on every run from the layers as they are now (the master plan, after SharedSync + PlanToRhino v2):
  areas     masterplan::proposal_planting_<species> (+ proposal_planting_meadow_lawn): m², ranking, leaf habit, maps
  trees     the tree blocks (SVG symbols sym_<species>) under masterplan: design counts per species
  reasons   each tree's rule worked out again from where it stands (water, walks, NE edge, wide roads, heritage)
Output: the board drawn in Rhino on masterplan::analysis_planting::<part> (below the plan, 1 board mm = 1 m) and saved
as a layered SVG Downloads/Bergama/Data/analysis/planting_analysis.svg (open it in Illustrator; the run before is kept
as planting_analysis_prev.svg). The board is rebuilt each run: edits made to the board itself are not carried over.
Look = board v9 (8 Nov 10:20); only the numbers, maps and counts follow the layers.
Plan and section drawings of each species: read live from Data/assets/agaclar.svg (Aras's trees), never redrawn.

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file.
  input  run      Button, or PlanToRhino v2's 'done' wired in (one press runs SharedSync -> PlanToRhino -> this)
  output log      the last run's report
  output done     "done HH:MM:SS.ss · N s" after a good run
"""
import os, time, json, re, math

# ---- SETTINGS ----
VERSION = "v1"
GH_LABEL = "PlantingAnalysis"
OUT_FOLDER = "bergama_planting_analysis"
LOG_NAME = "bergama_planting_analysis_log.txt"
ROOT_LAYER = "masterplan"
BOARD_LAYER = "analysis_planting"                 # masterplan::analysis_planting::<part>
BOARD_GAP_M = 150.0                               # the board sits this far below the plan (model m)
PTR_KEY = "bergama_plan_to_rhino"                 # PlanToRhino v2 document strings (placing)
CAP = 0.716                                       # Arial capital height / font size
# rules (design rules of the proposal, same numbers as board v9 / plant.py, 8 Nov)
WATER_BAND = (2.0, 24.0)                          # m from the water
PATH_SHADE = (2.5, 14.0)                          # m from the walks
ROAD_SCREEN_M = 25.0                              # m from a wide road
WIDE_ROAD_M = 8.5                                 # a road counts as wide from this width (v9: 17 px opening = 8.5 m)
NE_STEP = (15.0, 20.0)                            # 25 m toward NE (0.6, 0.8): outside the park there = NE edge
OPEN_LAWN = (22.0, 28.0)                          # single tree: > 22 m from walks and > 28 m from water ...
SOLO_GAP_M = 15.0                                 # ... and no other tree within 15 m (v9: a noise pattern; see log)
SAMPLE_M = 1.5                                    # edge sampling step for distances (m)

# ---- Bergama folders (template block, SCRIPT_STANDARD §9) ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


DATA_DIR = os.path.join(BERGAMA_ROOT, "Data")
LOG_DIR = bg_logs()
OUT_SVG = os.path.join(DATA_DIR, "analysis", "planting_analysis.svg")
AGACLAR = os.path.join(DATA_DIR, "assets", "agaclar.svg")

# species (bergama_plant_sheet_v1_2.py PLA_SPECIES, as on board v9): name, latin, turkish, layer, crown m, h m, leaf habit
SPECIES = {
    'plane': ('Oriental plane', 'Platanus orientalis', 'Doğu çınarı', 'tree', 15.0, 15.0, 'deciduous'),
    'ash': ('Narrow-leaved ash', 'Fraxinus angustifolia', 'Dişbudak', 'tree', 14.0, 20.0, 'deciduous'),
    'willow': ('White willow', 'Salix alba', 'Ak söğüt', 'tree', 10.5, 15.0, 'deciduous*'),
    'olive': ('Olive', 'Olea europaea', 'Zeytin', 'tree', 10.35, 11.5, 'evergreen'),
    'stone_pine': ('Stone pine', 'Pinus pinea', 'Fıstık çamı', 'tree', 15.1, 27.5, 'evergreen'),
    'tamarisk': ('Tamarisk', 'Tamarix smyrnensis', 'Ilgın', 'tree', 7.6, 9.5, 'deciduous'),
    'chaste': ('Chaste tree', 'Vitex agnus-castus', 'Hayıt', 'shrub', 2.0, 2.0, 'deciduous'),
    'rosemary': ('Rosemary', 'Salvia rosmarinus', 'Biberiye', 'shrub', 0.75, 0.75, 'evergreen'),
    'lavender': ('French lavender', 'Lavandula stoechas', 'Karabaş otu', 'ground', 0.66, 0.55, 'evergreen*'),
    'loosestrife': ('Purple loosestrife', 'Lythrum salicaria', 'Aklar otu', 'emergent', 0.75, 1.35, 'herbaceous'),
    'soft_rush': ('Soft rush', 'Juncus effusus', '(unverified)', 'emergent', 0.6, 1.0, 'not found'),
    'rush': ('Sharp rush', 'Juncus acutus', 'Kofa', 'emergent', 0.8, 0.8, 'not found'),
}
TREES = ['plane', 'ash', 'willow', 'olive', 'stone_pine', 'tamarisk']
KEYS = TREES + ['chaste', 'rosemary', 'lavender', 'loosestrife', 'soft_rush', 'rush']
COLOUR = {'plane': '#F2A65A', 'ash': '#6FA3C8', 'willow': '#C5D86D', 'olive': '#A68CC4', 'stone_pine': '#2F7F74',
          'tamarisk': '#E79BB9', 'chaste': '#8E7BC9', 'rosemary': '#8FBFA4', 'lavender': '#CDB8EA',
          'loosestrife': '#D46FA8', 'soft_rush': '#9BC46B', 'rush': '#6B8F47'}
PURPOSE = {  # masterplan v43 PLA_PURPOSE; * = tag from general ecology (PLA_PURPOSE_UNSURE)
    'plane': 'shade · corridor*', 'ash': 'shade · corridor*', 'willow': 'shade · cleaning · corridor*',
    'olive': 'shade · perception*', 'stone_pine': 'shade* · wind* · perception*', 'tamarisk': 'shade · wind* · corridor*',
    'chaste': 'perception · corridor*', 'rosemary': 'perception', 'lavender': 'perception',
    'loosestrife': 'cleaning · perception · corridor*', 'soft_rush': 'cleaning · corridor*', 'rush': 'cleaning* · corridor*'}
USE = {'shade': ('SHADE', '#C97B3C'), 'wind': ('WIND', '#70754C'), 'cleaning': ('CLEANS WATER', '#4F7D8C'),
       'perception': ('COLOUR · SCENT', '#A0628F'), 'corridor': ('WILDLIFE', '#5E8A3A')}
NICHE = {'soft_rush': 0.04, 'loosestrife': 0.10, 'rush': 0.14, 'willow': 0.24, 'tamarisk': 0.36, 'ash': 0.46,
         'plane': 0.52, 'chaste': 0.55, 'olive': 0.80, 'rosemary': 0.86, 'lavender': 0.90, 'stone_pine': 0.92}
RULES = [('#5C7A86', 'WATER EDGE', 'within 24 m of the water: willow + tamarisk hold the bank', 'water_band'),
         ('#C46A3C', 'SHADE ON THE WALKS', '2.5-14 m beside the walks: plane + ash, olive on dry ground', 'path_shade'),
         ('#70754C', 'NE WIND BREAK', 'park edge facing NE (summer, autumn, winter wind): stone pine + tamarisk', 'wind'),
         ('#4C2528', 'ROAD SCREEN', 'within 25 m of the wide roads: evergreen stone pine + tamarisk *', 'noise'),
         ('#E4877A', 'HERITAGE VIEWS', 'near Kizil Avlu: low olive only, views stay open', 'heritage'),
         ('#89986A', 'GROVE', 'trees standing in a group, outside the rules above', 'grove'),
         ('#A2B6B5', 'SINGLE TREE IN A LAWN', 'lawns stay open for play, events, flood water', 'solitary')]
# Aras's drawings in agaclar.svg (8 Nov 09:18 layout, plan row under section row): the box round each drawing
# (x, y, w, h in the file's units, measured on his file 8 Nov; species matched by colour as on board v9).
# Everything of his inside a box is copied as it is, every run.
ARAS_BOX = {
    'plane': ((3708, 1419, 257, 251), (3658, 1026, 418, 325)), 'ash': ((1470, 1443, 207, 205), (1368, 727, 476, 697)),
    'willow': ((4211, 1396, 285, 299), (4111, 520, 485, 836)), 'olive': ((4771, 1404, 265, 279), (4670, 713, 419, 653)),
    'stone_pine': ((3013, 1411, 246, 240), (2880, 908, 400, 458)), 'tamarisk': ((2239, 1437, 213, 217), (2134, 729, 413, 674)),
    'chaste': ((1111, 1446, 198, 189), (1023, 1000, 314, 398)), 'rosemary': ((3354, 1447, 208, 203), (3355, 1024, 206, 353)),
    'lavender': ((1872, 1451, 192, 196), (1843, 1002, 249, 399)), 'soft_rush': ((318, 1488, 145, 148), (265, 935, 167, 386)),
    'rush': ((0, 1415, 212, 215), (0, 1010, 270, 374)), 'loosestrife': ((796, 1437, 222, 222), (784, 1013, 236, 371))}
FONT = "Arial"


# =====================================================================================================  SVG geometry (copied from PlanToRhino v2)
_NUM = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
SVGNS = "{http://www.w3.org/2000/svg}"
XLINK = "{http://www.w3.org/1999/xlink}href"

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



def local(tag):
    return tag.split("}", 1)[1] if isinstance(tag, str) and "}" in tag else (tag if isinstance(tag, str) else "")


def esc(s):
    return (u"%s" % s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def mix(c, d, t):
    a = [int(c[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(d[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def inv(m):
    a, b, c, d, e, f = m
    det = a * d - b * c
    return (d / det, -b / det, -c / det, a / det, (c * f - d * e) / det, (b * e - a * f) / det)


# =====================================================================================================  plain geometry
def ring_area(r):
    return sum(r[i - 1][0] * r[i][1] - r[i][0] * r[i - 1][1] for i in range(len(r))) / 2.0


def ring_centroid(r):
    a = ring_area(r)
    if abs(a) < 1e-9:
        return (sum(p[0] for p in r) / len(r), sum(p[1] for p in r) / len(r))
    cx = cy = 0.0
    for i in range(len(r)):
        x0, y0 = r[i - 1]
        x1, y1 = r[i]
        k = x0 * y1 - x1 * y0
        cx += (x0 + x1) * k
        cy += (y0 + y1) * k
    return (cx / (6 * a), cy / (6 * a))


def bbox_of(rings):
    xs = [p[0] for r in rings for p in r]
    ys = [p[1] for r in rings for p in r]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None


class Region(object):
    """one filled area: rings (first = outer, others = holes; even-odd), its m² and centre"""

    def __init__(self, rings, area=None):
        self.rings = [r for r in rings if len(r) >= 3]
        self.bb = bbox_of(self.rings)
        if area is None:                              # even-odd: a ring inside an odd number of others is a hole
            area = 0.0
            bbs = [bbox_of([r]) for r in self.rings]
            for i, r in enumerate(self.rings):
                p = r[0]
                depth = 0
                for j, q in enumerate(self.rings):
                    if j == i or not (bbs[j][0] <= p[0] <= bbs[j][2] and bbs[j][1] <= p[1] <= bbs[j][3]):
                        continue
                    if Region([q], 0.0).contains(p):
                        depth += 1
                area += abs(ring_area(r)) * (1 if depth % 2 == 0 else -1)
            area = abs(area)
        self.area = area
        big = max(self.rings, key=lambda r: abs(ring_area(r))) if self.rings else None
        self.centre = ring_centroid(big) if big else (0.0, 0.0)

    def contains(self, p):
        if not self.bb or not (self.bb[0] <= p[0] <= self.bb[2] and self.bb[1] <= p[1] <= self.bb[3]):
            return False
        x, y = p
        c = False
        for r in self.rings:
            n = len(r)
            for i in range(n):
                x1, y1 = r[i]
                x2, y2 = r[i - 1]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    c = not c
        return c


def inside_any(regions, p):
    return any(rg_.contains(p) for rg_ in regions)


class Near(object):
    """distance from a point to the nearest of many edges (edges sampled every SAMPLE_M m, 10 m buckets)"""

    def __init__(self, lines, step=SAMPLE_M, cell=10.0):
        self.cell = cell
        self.b = {}
        self.n = 0
        for ln in lines:
            for i in range(1, len(ln)):
                (x0, y0), (x1, y1) = ln[i - 1], ln[i]
                L = math.hypot(x1 - x0, y1 - y0)
                k = max(1, int(L / step))
                for j in range(k + 1):
                    x, y = x0 + (x1 - x0) * j / k, y0 + (y1 - y0) * j / k
                    self.b.setdefault((int(x // cell), int(y // cell)), []).append((x, y))
                    self.n += 1

    def dist(self, p, rmax):
        if not self.b:
            return 1e9
        cx, cy = int(p[0] // self.cell), int(p[1] // self.cell)
        R = int(rmax // self.cell) + 1
        best = 1e9
        for i in range(cx - R, cx + R + 1):
            for j in range(cy - R, cy + R + 1):
                for q in self.b.get((i, j), ()):
                    d = (q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2
                    if d < best:
                        best = d
        best = math.sqrt(best)
        return best if best <= rmax else 1e9


def clip_ring(r, box):
    """Sutherland-Hodgman: a ring cut to the rectangle box (x0, y0, x1, y1)"""
    x0, y0, x1, y1 = box
    for inside, cut in ((lambda p: p[0] >= x0, lambda a, b: (x0, a[1] + (b[1] - a[1]) * (x0 - a[0]) / (b[0] - a[0]))),
                        (lambda p: p[0] <= x1, lambda a, b: (x1, a[1] + (b[1] - a[1]) * (x1 - a[0]) / (b[0] - a[0]))),
                        (lambda p: p[1] >= y0, lambda a, b: (a[0] + (b[0] - a[0]) * (y0 - a[1]) / (b[1] - a[1]), y0)),
                        (lambda p: p[1] <= y1, lambda a, b: (a[0] + (b[0] - a[0]) * (y1 - a[1]) / (b[1] - a[1]), y1))):
        out = []
        n = len(r)
        for i in range(n):
            a, b = r[i - 1], r[i]
            if inside(b):
                if not inside(a):
                    out.append(cut(a, b))
                out.append(b)
            elif inside(a):
                out.append(cut(a, b))
        r = out
        if not r:
            break
    return r


def closed(r):
    return list(r) + [r[0]]


# =====================================================================================================  analysis
def analyse(data, notes):
    """data from the layers -> results (areas, counts, the rule of every tree)"""
    A = data["areas"]
    area = dict((k, sum(r.area for r in A.get(k, []))) for k in KEYS)
    meadow = sum(r.area for r in A.get("meadow_lawn", []))
    planted = sum(area.values())
    park = [r for k in KEYS + ["meadow_lawn"] for r in A.get(k, [])]
    trees = data["trees"]
    cnt = dict((k, 0) for k in TREES)
    for sp, x, y in trees:
        cnt[sp] = cnt.get(sp, 0) + 1
    water = data["water"]
    nW = Near([closed(r) for rg_ in water for r in rg_.rings])
    nP = Near([closed(r) for rg_ in data["paths_fill"] for r in rg_.rings] + data["paths_line"])
    wide = [rg_ for rg_ in data["roads"] if rg_.width >= WIDE_ROAD_M and not inside_any(park, rg_.centre)]
    nR = Near([closed(r) for rg_ in wide for r in rg_.rings])
    her = data["heritage"]
    nPark = Near([closed(r) for rg_ in park for r in rg_.rings])
    tb = {}
    for sp, x, y in trees:
        tb.setdefault((int(x // SOLO_GAP_M), int(y // SOLO_GAP_M)), []).append((x, y))

    def alone(x, y):
        cx, cy = int(x // SOLO_GAP_M), int(y // SOLO_GAP_M)
        return all(math.hypot(q[0] - x, q[1] - y) > SOLO_GAP_M or (q[0] == x and q[1] == y)
                   for i in (-1, 0, 1) for j in (-1, 0, 1) for q in tb.get((cx + i, cy + j), []))

    def outside_park(q):                              # the traced areas leave thin gaps: 8 m from an area = inside
        return not inside_any(park, q) and nPark.dist(q, 8.0) > 8.0
    rule = []
    for sp, x, y in trees:
        p = (x, y)
        dW = 0.0 if inside_any(water, p) else nW.dist(p, 60.0)
        dP = 0.0 if inside_any(data["paths_fill"], p) else nP.dist(p, 30.0)
        if inside_any(her, p):
            r_ = "heritage"
        elif nR.dist(p, ROAD_SCREEN_M + 1) <= ROAD_SCREEN_M:
            r_ = "noise"
        elif park and outside_park((x + NE_STEP[0], y + NE_STEP[1])):
            r_ = "wind"
        elif PATH_SHADE[0] <= dP <= PATH_SHADE[1]:
            r_ = "path_shade"
        elif WATER_BAND[0] <= dW <= WATER_BAND[1]:
            r_ = "water_band"
        elif dP > OPEN_LAWN[0] and dW > OPEN_LAWN[1] and alone(x, y):
            r_ = "solitary"
        else:
            r_ = "grove"
        rule.append(r_)
    rc = {}
    for r_ in rule:
        rc[r_] = rc.get(r_, 0) + 1
    notes.append(u"areas (m², measured on the layers): " + u", ".join(u"%s %s" % (k, f"{area[k]:,.0f}") for k in KEYS) +
                 u"; meadow / lawn %s; planted total %s" % (f"{meadow:,.0f}", f"{planted:,.0f}"))
    notes.append(u"trees (design counts): " + u", ".join(u"%s %d" % (k, cnt.get(k, 0)) for k in TREES) +
                 u"; total %d" % len(trees))
    notes.append(u"reasons (worked out from where each tree stands): " +
                 u", ".join(u"%s %d" % (r[3], rc.get(r[3], 0)) for r in RULES))
    if not water:
        notes.append(u"FLAG no water fills found on proposal_water: water distances not used")
    if not wide:
        notes.append(u"FLAG no wide road (>= %.1f m) on existing_roads: road screen rule not used" % WIDE_ROAD_M)
    return dict(area=area, meadow=meadow, planted=planted, cnt=cnt, rule=rule, rc=rc)


# =====================================================================================================  agaclar.svg
def aras_icons(path, notes):
    """Aras's plan + section of each species, cut live from agaclar.svg by the boxes in ARAS_BOX.
    Returns {key: {'plan': (shapes, svg fragment, box), 'sect': ...}}; shapes in the file's units."""
    import xml.etree.ElementTree as ET
    if not os.path.isfile(path):
        notes.append(u"FLAG no %s: species drawings left out of the board" % path)
        return {}
    root = ET.parse(path).getroot()
    css = {}
    for st in root.iter(SVGNS + "style"):
        css.update(parse_css(st.text or ""))
    kids = [c for c in root if local(c.tag) not in ("defs", "metadata", "style", "title")]
    style0 = {"fill": "#000000", "stroke": "none", "stroke-width": "1"}

    def walk(el, m, st, out):
        for ch in el:
            tg = local(ch.tag)
            s2 = dict((k, v) for k, v in st.items())
            for k in ("fill", "stroke", "stroke-width", "fill-rule", "opacity", "display"):
                if ch.get(k) is not None:
                    s2[k] = ch.get(k)
            for c in (ch.get("class") or "").split():
                s2.update(css.get(c, {}))
            for part in (ch.get("style") or "").split(";"):
                if ":" in part:
                    k, v = part.split(":", 1)
                    s2[k.strip().lower()] = v.strip()
            if s2.get("display", "").strip() == "none":
                continue
            mm = mat_mul(m, parse_transform(ch.get("transform")))
            if tg == "g":
                walk(ch, mm, s2, out)
            elif tg in ("path", "rect", "circle", "ellipse", "polygon", "polyline", "line"):
                subs = path_segments(ch.get("d")) if tg == "path" else shape_subpaths(tg, ch)
                if subs:
                    fill = parse_color(s2.get("fill"))
                    stroke = parse_color(s2.get("stroke"))
                    if tg in ("line", "polyline"):
                        fill = None
                    if fill is not None or stroke is not None:
                        out.append(dict(subs=tx_subpaths(subs, mm), fill=fill, stroke=stroke,
                                        lw=first_num(s2.get("stroke-width"), 1.0) * mat_scale(mm),
                                        evenodd=(s2.get("fill-rule") or "") == "evenodd"))
    def bbox(out):
        pts = [p for sh in out for cl, s in sh["subs"] for p in [s[0]] + [seg[-1] for seg in s[1:]]]
        return (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)) if pts else None

    def pick(el, m, st, box, shapes, frag):
        """el wholly in the box: taken; a group across the box edge: its children looked at; a loose piece: by its centre"""
        x, y, w, h = box
        out = []
        walk([el], m, st, out)
        bb = bbox(out)
        if bb is None:
            return
        if bb[0] >= x - 3 and bb[1] >= y - 3 and bb[2] <= x + w + 3 and bb[3] <= y + h + 3:
            take = True
        elif local(el.tag) == "g" and bb[0] < x + w and bb[2] > x and bb[1] < y + h and bb[3] > y:
            m2 = mat_mul(m, parse_transform(el.get("transform")))
            for ch in el:
                pick(ch, m2, st, box, shapes, frag)
            return
        else:
            cx, cy = (bb[0] + bb[2]) / 2.0, (bb[1] + bb[3]) / 2.0
            take = local(el.tag) != "g" and x - 2 <= cx <= x + w + 2 and y - 2 <= cy <= y + h + 2
        if take:
            shapes.extend(out)
            s = ET.tostring(el, encoding="unicode")
            s = re.sub(r' xmlns(:\w+)?="[^"]*"', "", s)
            s = re.sub(r'<(/?)ns\d+:', r'<\1', s)
            s = re.sub(r' id="[^"]*"', "", s)
            if m != ID:
                s = '<g transform="matrix(%s)">%s</g>' % (" ".join("%.8g" % v for v in m), s)
            frag.append(s)
    res = {}
    for k, boxes in ARAS_BOX.items():
        res[k] = {}
        for part, box in zip(("plan", "sect"), boxes):
            shapes, frag = [], []
            for c in kids:
                pick(c, ID, style0, box, shapes, frag)
            if shapes:
                res[k][part] = (shapes, "".join(frag), box)
        if len(res[k]) < 2:
            notes.append(u"FLAG agaclar.svg: no %s drawing found in its box for %s" %
                         (" / ".join(p for p in ("plan", "sect") if p not in res[k]), k))
    return res


def icon_matrix(part, box):
    """file units -> unit icon: plan = radius 1 round its centre; section = height 1, base at 0 (as board v9)"""
    x, y, w, h = box
    if part == "plan":
        R = max(w, h) / 2.0
        return (1.0 / R, 0.0, 0.0, 1.0 / R, -(x + w / 2.0) / R, -(y + h / 2.0) / R)
    return (1.0 / h, 0.0, 0.0, 1.0 / h, -(x + w / 2.0) / h, -(y + h) / h)


# =====================================================================================================  the board
class Board(object):
    """primitives in board mm (A1 landscape 841 x 594, y down), each on a part (= Rhino sub-layer / SVG group)"""

    def __init__(self):
        self.p = []
        self.part = "title"

    def poly(self, rings, fill=None, stroke=None, sw=0.25):
        rings = [r for r in rings if len(r) >= 2]
        if rings:
            self.p.append(dict(k="poly", rings=rings, fill=fill, stroke=stroke, sw=sw, L=self.part))

    def rect(self, x, y, w, h, fill=None, stroke=None, sw=0.25):
        self.poly([[(x, y), (x + w, y), (x + w, y + h), (x, y + h)]], fill, stroke, sw)

    def circle(self, cx, cy, r, fill=None, stroke=None, sw=0.25):
        n = 24
        self.poly([[(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]],
                  fill, stroke, sw)

    def text(self, x, y, s, size, fill="#333333", bold=False, anchor="start", italic=False):
        self.p.append(dict(k="text", x=x, y=y, s=u"%s" % s, size=size, fill=fill, bold=bold, anchor=anchor,
                           italic=italic, L=self.part))

    def icon(self, key, part, x, y, scale):
        self.p.append(dict(k="icon", key=key, part=part, x=x, y=y, scale=scale, L=self.part))

    def grad(self, x, y, w, h, stops):
        self.p.append(dict(k="grad", x=x, y=y, w=w, h=h, stops=stops, L=self.part))


def build_board(data, res, icons, notes):
    B = Board()
    A, area, cnt = data["areas"], res["area"], res["cnt"]
    planted = res["planted"] or 1.0
    to_svg = data["to_svg"]                          # model m -> plan SVG units
    park = [r for k in KEYS + ["meadow_lawn"] for r in A.get(k, [])]
    pb = bbox_of([[to_svg(p) for p in r] for rg_ in park for r in rg_.rings]) or (0, 0, 1, 1)
    # main map: board v9 scale (0.10357 mm per plan unit) if the park fits in 800 x 176 mm, else smaller
    S = min(0.10357238, 800.0 / max(1e-6, pb[2] - pb[0]), 176.0 / max(1e-6, pb[3] - pb[1]))
    ox = 20 + (800 - (pb[2] - pb[0]) * S) / 2.0 - pb[0] * S
    oy = 62 + (176 - (pb[3] - pb[1]) * S) / 2.0 - pb[1] * S

    def F(p):
        u_, v_ = to_svg(p)
        return (ox + u_ * S, oy + v_ * S)

    def rings_of(regs, f):
        return [[f(p) for p in r] for rg_ in regs for r in rg_.rings]
    B.part = "title"
    B.text(20, 26, "PLANTING DISTRIBUTION", 11, "#2B2B2B", True)
    B.text(20, 36, "MIRAQUA · Selinos stream · where each species grows, and how much ground it takes", 4.2, "#555555")
    B.text(20, 43, "Proposal areas measured on the plan layers (not survey). Species, heights and crowns: plant module "
                   "(bergama_plant_sheet_v1_2.py PLA_SPECIES). Rebuilt %s from the master plan." %
           time.strftime("%d %b %Y %H:%M"), 3, "#777777")
    B.part = "map"
    mapclip = (20, 62, 820, 238)

    def clipped(rings, box=mapclip):
        out = [clip_ring(r, box) for r in rings]
        return [r for r in out if len(r) >= 3]
    B.poly(clipped(rings_of(data["roads"], F)), "#EFEFEC")
    B.poly(clipped(rings_of(data["water"], F)), "#5C7A86")
    B.poly(clipped(rings_of(A.get("meadow_lawn", []), F)), "#EEF0E6", "#FFFFFF", 0.25)
    B.poly(clipped(rings_of(data["paths_fill"], F)), "#FFFFFF")
    for ln in data["paths_line"]:
        q = [F(p) for p in ln]
        if any(mapclip[0] <= x <= mapclip[2] and mapclip[1] <= y <= mapclip[3] for x, y in q):
            B.poly([q], None, "#FFFFFF", 0.35)
    for k in KEYS:
        B.part = "map_area_" + k
        B.poly(rings_of(A.get(k, []), F), COLOUR[k], "#FFFFFF", 1.1)
    B.part = "map_labels"
    for k in TREES:
        big = sorted(A.get(k, []), key=lambda r: -r.area)[:2]
        for rg_ in big:
            if rg_.area < 1500:
                continue
            x, y = F(rg_.centre)
            B.text(x, y, SPECIES[k][0], 2.4, "#1F1F1F", True, "middle")
            B.text(x, y + 2.4, f"{rg_.area:,.0f} m²", 1.9, "#1F1F1F", anchor="middle")
    B.part = "scale"
    mpu = data["m_per_unit"]                          # m per plan SVG unit
    sb = 100.0 / mpu * S                              # 100 m on the board
    B.rect(700, 235.1, sb, 1.2, "#333333")
    B.rect(700 + sb, 235.1, sb, 1.2, "#FFFFFF", "#333333", 0.2)
    B.text(700, 240.3, "0      100      200 m   (scale ≈ 1:%d on A1)" % round(1000.0 * mpu / S), 2.4)
    na = data["north"]                                # north on the board (unit vector, y down)
    tip = (815 + na[0] * 6, 56 + na[1] * 6)
    side = (-na[1] * 3, na[0] * 3)
    B.poly([[tip, (815 - na[0] * 3 + side[0], 56 - na[1] * 3 + side[1]), (815 - na[0] * 1.5, 56 - na[1] * 1.5),
             (815 - na[0] * 3 - side[0], 56 - na[1] * 3 - side[1])]], "#333333")
    B.text(815 + na[0] * 9, 56 + na[1] * 9 + 1, "N", 3, anchor="middle")
    # ---- leaf habit
    ev = [k for k in KEYS if SPECIES[k][6].startswith("evergreen")]
    de = [k for k in KEYS if SPECIES[k][6].startswith("deciduous")]
    a_ev, a_de = sum(area[k] for k in ev), sum(area[k] for k in de)
    a_ot = res["planted"] - a_ev - a_de
    S2 = S * 360.0 / 800.0
    for col, (title, group, a, colr) in enumerate((("EVERGREEN", ev, a_ev, COLOUR["olive"]),
                                                   ("DECIDUOUS", de, a_de, COLOUR["plane"]))):
        B.part = "leaf_habit"
        oy2 = 268 + col * 78
        x0 = 20

        def G(p, oy2=oy2):
            u_, v_ = to_svg(p)
            return (x0 + (u_ - pb[0]) * S2, oy2 + (v_ - pb[1]) * S2)
        B.poly(rings_of(park, G), "#E6E6E2")
        B.poly(clipped(rings_of(data["water"], G), (x0, oy2 - 2, x0 + 362, oy2 + 70)), "#C9D3D6")
        B.poly(rings_of([r for k in group for r in A.get(k, [])], G), colr)
        B.text(x0 + 372, oy2 + 30, "%d%%" % round(100 * a / planted), 13, colr, True)
        B.text(x0 + 372, oy2 + 37, "%s · %s m²" % (title, f"{a:,.0f}"), 3.2)
        names = [SPECIES[k][0] for k in group]
        for li in range(0, len(names), 3):
            B.text(x0 + 372, oy2 + 41.5 + li, ", ".join(names[li:li + 3]), 2.2, "#666666")
    B.text(20, 262, "LEAF HABIT · share of the planted area", 4, "#2B2B2B", True)
    B.text(20, 424, "Rushes and loosestrife (%s m²) not counted: leaf habit not found / herbaceous. * willow, lavender: "
                    "habit not quoted in the source (plant module flags it)." % f"{a_ot:,.0f}", 2.2, "#777777")
    # ---- ranking
    B.part = "ranking"
    B.text(470, 262, "AREA RANKING · m² and share of planted area (%s m²)" % f"{res['planted']:,.0f}", 4, "#2B2B2B", True)
    B.text(526, 268.5, "where it grows (whole park, river in blue)", 2.2, "#555555")
    B.text(644, 268.5, "share of the planted area", 2, "#777777")
    S3 = min(112.0 / max(1e-6, pb[2] - pb[0]), 11.6 / max(1e-6, pb[3] - pb[1]))
    rk = sorted(KEYS, key=lambda k: -area[k])
    pcmax = max(1e-6, 100 * area[rk[0]] / planted)
    for i, k in enumerate(rk):
        y = 270 + i * 12.6
        a = area[k]
        pc = 100 * a / planted
        B.text(470, y + 3, SPECIES[k][0], 3, "#2B2B2B", True)
        B.text(470, y + 6.5, "%s m² · %.1f%%" % (f"{a:,.0f}", pc), 2.2, "#555555")
        B.text(470, y + 9.5, SPECIES[k][1], 2, "#888888", italic=True)

        def Kf(p, y=y):
            u_, v_ = to_svg(p)
            return (526 + (u_ - pb[0]) * S3, y + 0.4 + (v_ - pb[1]) * S3)
        B.part = "ranking_where_" + k
        B.poly(rings_of(park, Kf), "#EDEDE9")
        B.poly(clipped(rings_of(data["water"], Kf), (525, y, 639, y + 12.4)), "#D5DDE0")
        B.poly(rings_of(A.get(k, []), Kf), COLOUR[k], COLOUR[k], 0.25)
        B.part = "ranking"
        B.rect(644, y + 4.5, 160 * pc / pcmax, 2.4, COLOUR[k])
        B.text(647 + 160 * pc / pcmax, y + 6.6, "%.1f%%" % pc, 2.2)
    # ---- species row
    B.part = "species"
    B.text(20, 438, "SPECIES · wet edge → dry ground (niche centre t, masterplan v43 PLA_NICHE)", 4, "#2B2B2B", True)
    B.grad(20, 443, 800, 3, [(0, "#5C7A86"), (0.35, "#A2B6B5"), (1, "#E3D9C2")])
    B.text(20, 450, "water edge", 2)
    B.text(820, 450, "60 m and more from the water", 2, anchor="end")
    order = sorted(KEYS, key=lambda k: NICHE[k])
    cw = 800.0 / len(order)
    for i, k in enumerate(order):
        cx, cy = 20 + cw * (i + 0.5), 470
        nm, lat, tr, layer, cr, h, fol = SPECIES[k]
        B.part = "species_" + k
        if k in icons and "plan" in icons[k]:
            B.icon(k, "plan", cx - 12, cy, 6 + cr * 0.3)
        else:
            B.circle(cx - 12, cy, 9, COLOUR[k], mix(COLOUR[k], "#1E2A1E", 0.45), 0.35)
        if k in icons and "sect" in icons[k]:
            B.icon(k, "sect", cx + 12, cy + 12, 22)
        B.text(cx, 492, "%d" % (i + 1), 3.4, "#333333", True, "middle")
        lines = [(nm, 2.6, True, "#222222"), (lat, 2.1, False, "#555555"), (tr, 2.1, False, "#555555"),
                 ("h %g m · crown %g m" % (h, cr), 2.1, False, "#333333"), (fol, 2.0, False, "#333333"),
                 ("design count: %d trees" % cnt.get(k, 0) if k in TREES else "bed area: %s m²" % f"{area[k]:,.0f}",
                  1.9, False, "#333333")]
        for j, (tx, fs, bo, c) in enumerate(lines):
            B.text(cx, 499 + j * 4.2, tx, fs, c, bo, "middle")
        tags = [t.strip() for t in PURPOSE[k].split("·")]
        tw = [len(USE[t.rstrip("*")][0]) * 1.15 + 3 + (1.2 if t.endswith("*") else 0) for t in tags]
        xx = cx - (sum(tw) + (len(tw) - 1)) / 2.0
        for t, w_ in zip(tags, tw):
            lab, colr = USE[t.rstrip("*")]
            B.rect(xx, 524.5, w_, 3.6, colr)
            B.text(xx + w_ / 2, 527.2, lab + ("*" if t.endswith("*") else ""), 2, "#FFFFFF", True, "middle")
            xx += w_ + 1
    B.part = "species"
    B.text(20, 536, "Heights h = plant module h_m (mid of the sourced range: plane S68/S69, ash S7, willow S4, olive S72, "
                    "stone pine S74, tamarisk S9b genus, chaste S58, rosemary S58, lavender S58, loosestrife S19, soft "
                    "rush S20, sharp rush S21).", 2, "#777777")
    B.text(20, 540, "Not planted: common reed and water mint (lined basin cells only, D2/D6), giant reed (REMOVE, raises "
                    "flood risk, S36), oleander (toxic, replaced).", 2, "#777777")
    # ---- why here
    B.part = "why"
    B.text(20, 237.6, "WHY EACH TREE STANDS WHERE IT DOES", 2.8, "#2B2B2B", True)
    B.text(86, 237.6, "numbers on the map = trees placed by that rule (each rule worked out from where the tree stands)",
           2.2, "#666666")
    trees, rule = data["trees"], res["rule"]
    present = [r for r in RULES if res["rc"].get(r[3])]
    bw = 800.0 / max(1, len(present))
    marks = []
    for n_, (c, ti, ex, key) in enumerate(present):
        bx, by = 20 + n_ * bw, 240
        B.part = "why_" + key
        B.rect(bx, by, bw - 2.5, 16, "#FFFFFF", c, 0.6)
        B.circle(bx + 4, by + 4.6, 2.2, c)
        B.text(bx + 4, by + 5.5, "%d" % (n_ + 1), 2.6, "#FFFFFF", True, "middle")
        B.text(bx + 7.5, by + 5.6, "%s · %d trees" % (ti, res["rc"].get(key, 0)), 2.9, c, True)
        words, l1, l2 = ex.split(), "", ""
        lim = int((bw - 6) / 1.12)
        for w_ in words:
            if len(l1) + len(w_) < lim and not l2:
                l1 += (" " if l1 else "") + w_
            else:
                l2 += (" " if l2 else "") + w_
        B.text(bx + 2.5, by + 10.4, l1, 2.3)
        B.text(bx + 2.5, by + 14, l2, 2.3)
        tt = sorted([F((t[1], t[2])) for t, r_ in zip(trees, rule) if r_ == key])
        picks = [tt[int(len(tt) * q)] for q in (0.15, 0.5, 0.85)] if len(tt) >= 3 else tt
        B.part = "why_marks"
        for px, py in picks:
            if all(math.hypot(px - qx, py - qy) > 7 for qx, qy in marks):
                marks.append((px, py))
                B.circle(px, py, 1.9, c, "#FFFFFF", 0.4)
                B.text(px, py + 0.8, "%d" % (n_ + 1), 2.3, "#FFFFFF", True, "middle")
    # ---- use key
    B.part = "use_key"
    B.text(20, 556, "WHAT EACH PLANT IS FOR", 4, "#2B2B2B", True)
    ukey = [("shade", "cools the walks, lawns and seats in summer"), ("wind", "slows the NE wind (summer, autumn, winter)"),
            ("cleaning", "roots and reeds filter the stream water"), ("perception", "colour, flowers and scent people notice"),
            ("corridor", "food and cover that link habitats for birds and insects")]
    for i, (t, ex) in enumerate(ukey):
        lab, colr = USE[t]
        x, y = 20 + (i % 3) * 270, 562 + (i // 3) * 9
        w_ = len(lab) * 1.15 + 3
        B.rect(x, y, w_, 3.6, colr)
        B.text(x + w_ / 2, y + 2.7, lab, 2, "#FFFFFF", True, "middle")
        B.text(x + w_ + 2, y + 2.9, ex, 2.4)
    B.text(20, 584, "* = use tag from general ecology, not a project source (masterplan v43 PLA_PURPOSE_UNSURE). Uses: "
                    "masterplan v43 PLA_PURPOSE. Design counts, not survey. Rules = design rules of this proposal. Wind: "
                    "Selinus_T5 (PVGIS TMY 2005-2020).", 1.9, "#888888")
    return B


# =====================================================================================================  SVG out
def board_svg(B, icons):
    o = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="841mm" '
         'height="594mm" viewBox="0 0 841 594">', "<defs>"]
    used = set((p["key"], p["part"]) for p in B.p if p["k"] == "icon")
    for k, part in sorted(used):
        shapes, frag, box = icons[k][part]
        m = icon_matrix(part, box)
        vb = "-1.1 -1.1 2.2 2.2" if part == "plan" else "-0.7 -1.05 1.4 1.1"
        o.append('<symbol id="%s_%s" viewBox="%s" overflow="visible"><g transform="matrix(%s)">%s</g></symbol>' %
                 ("sym" if part == "plan" else "sec", k, vb, " ".join("%.8g" % v for v in m), frag))
    gi = 0
    for p in B.p:
        if p["k"] == "grad":
            gi += 1
            p["gid"] = "grad%d" % gi
            o.append('<linearGradient id="%s">%s</linearGradient>' % (p["gid"], "".join(
                '<stop offset="%g" stop-color="%s"/>' % s for s in p["stops"])))
    o.append("</defs>")
    o.append('<rect id="paper" width="841" height="594" fill="#FFFFFF"/>')
    parts = []
    for p in B.p:
        if p["L"] not in parts:
            parts.append(p["L"])
    for part in parts:
        o.append('<g id="%s" font-family="Arial, Helvetica, sans-serif">' % part)
        for p in B.p:
            if p["L"] != part:
                continue
            if p["k"] == "poly":
                d = " ".join("M" + " L".join("%.2f,%.2f" % q for q in r) + "Z" for r in p["rings"])
                if p["fill"] is None:
                    d = " ".join("M" + " L".join("%.2f,%.2f" % q for q in r) for r in p["rings"])
                o.append('<path d="%s" fill="%s"%s fill-rule="evenodd"/>' % (
                    d, p["fill"] or "none", ' stroke="%s" stroke-width="%g" stroke-linejoin="round"' % (p["stroke"], p["sw"])
                    if p["stroke"] else ""))
            elif p["k"] == "text":
                o.append("<text x='%.2f' y='%.2f' font-size='%g'%s%s fill='%s'%s>%s</text>" % (
                    p["x"], p["y"], p["size"], " font-weight='bold'" if p["bold"] else "",
                    " font-style='italic'" if p["italic"] else "", p["fill"],
                    " text-anchor='%s'" % p["anchor"] if p["anchor"] != "start" else "", esc(p["s"])))
            elif p["k"] == "icon":
                if p["part"] == "plan":
                    o.append('<use x="-1.1" y="-1.1" width="2.2" height="2.2" xlink:href="#sym_%s" '
                             'transform="translate(%.2f %.2f) scale(%.3f)"/>' % (p["key"], p["x"], p["y"], p["scale"]))
                else:
                    o.append('<use x="-0.7" y="-1.05" width="1.4" height="1.1" xlink:href="#sec_%s" '
                             'transform="translate(%.2f %.2f) scale(%.3f)"/>' % (p["key"], p["x"], p["y"], p["scale"]))
            elif p["k"] == "grad":
                o.append('<rect x="%g" y="%g" width="%g" height="%g" fill="url(#%s)"/>' % (p["x"], p["y"], p["w"], p["h"], p["gid"]))
        o.append("</g>")
    o.append("</svg>")
    return "\n".join(o)


# =====================================================================================================  Rhino in / out
def read_layers(doc, notes):
    """everything the analysis needs, from the layers under masterplan (model m)"""
    import Rhino
    rg = Rhino.Geometry
    try:
        mx = json.loads(doc.Strings.GetValue(PTR_KEY, "v2_matrix") or "null")
    except Exception:
        mx = None
    if not mx:
        raise RuntimeError("the plan has not been baked with PlanToRhino v2 in this file: run SharedSync + PlanToRhino first")
    u = float(mx.get("u") or 1.0)                     # model units per m
    M = tuple(mx["M"])                                # plan SVG units -> m
    Mi = inv(M)
    es = Rhino.DocObjects.ObjectEnumeratorSettings()
    es.HiddenObjects = True
    es.LockedObjects = True
    by_layer = {}
    for o in doc.Objects.GetObjectList(es):
        fp = doc.Layers[o.Attributes.LayerIndex].FullPath
        if fp.startswith(ROOT_LAYER + "::") and not fp.startswith(ROOT_LAYER + "::" + BOARD_LAYER):
            by_layer.setdefault(fp[len(ROOT_LAYER) + 2:], []).append(o)

    def pts(crv):
        try:
            ok, pl = crv.TryGetPolyline()
        except Exception:
            ok = False
        if not ok:
            try:
                pc = crv.ToPolyline(0.05 * u, 0.1, 0.0, 0.0)
                ok, pl = pc.TryGetPolyline()
            except Exception:
                ok = False
        if not ok:
            return []
        P = [(p.X / u, p.Y / u) for p in pl]
        if len(P) > 1 and P[0] == P[-1]:
            P = P[:-1]
        return P

    def colour(o):
        a = o.Attributes
        try:
            if a.ColorSource == Rhino.DocObjects.ObjectColorSource.ColorFromObject:
                return a.ObjectColor
        except Exception:
            pass
        return doc.Layers[a.LayerIndex].Color

    def regions(objs, test=None):
        out = []
        for o in objs:
            g = o.Geometry
            if isinstance(g, rg.Hatch):
                if test is not None and not test(colour(o)):
                    continue
                rings = [pts(c) for c in g.Get3dCurves(True)] + [pts(c) for c in g.Get3dCurves(False)]
                a = None
                try:
                    a = rg.AreaMassProperties.Compute(g).Area / (u * u)
                except Exception:
                    a = None
                r_ = Region(rings, a)
                if r_.rings:
                    out.append(r_)
            elif isinstance(g, rg.Curve) and g.IsClosed and test is None:
                r_ = Region([pts(g)])
                if r_.rings:
                    out.append(r_)
        return out
    data = {"areas": {}}
    found = []
    for sub, objs in by_layer.items():
        nm = sub.split("::")[-1]
        if nm.startswith("proposal_planting_"):
            k = nm[len("proposal_planting_"):]
            if k in KEYS or k == "meadow_lawn":
                data["areas"].setdefault(k, []).extend(regions(objs))
                found.append(k)
    missing = [k for k in KEYS + ["meadow_lawn"] if k not in found]
    if missing:
        notes.append(u"FLAG no layer proposal_planting_<species> for: " + u", ".join(missing))
    blue = lambda c: c.B > c.R + 15 and c.B >= c.G - 25
    data["water"] = regions(by_layer.get("proposal_water", []), blue)
    pf, pl_ = [], []
    for o in by_layer.get("proposal_paths", []):
        g = o.Geometry
        if isinstance(g, rg.Hatch):
            pf += regions([o])
        elif isinstance(g, rg.Curve):
            q = pts(g)
            if len(q) >= 2:
                pl_.append(q + ([q[0]] if g.IsClosed else []))
    data["paths_fill"], data["paths_line"] = pf, pl_
    roads = regions(by_layer.get("existing_roads", []))
    for r_ in roads:
        per = sum(math.hypot(r[i][0] - r[i - 1][0], r[i][1] - r[i - 1][1]) for r in r_.rings for i in range(len(r)))
        r_.width = 2.0 * r_.area / per if per > 0 else 0.0
    data["roads"] = roads
    data["heritage"] = regions(by_layer.get("existing_heritage", []))
    trees, n_other = [], 0
    for sub, objs in by_layer.items():
        for o in objs:
            if not isinstance(o, Rhino.DocObjects.InstanceObject):
                continue
            idf = o.InstanceDefinition
            desc = (idf.Description or "") + " " + (idf.Name or "")
            m = re.search(r"sym_(" + "|".join(sorted(TREES, key=len, reverse=True)) + r")\b", desc)
            if not m:
                n_other += 1
                continue
            x = o.InstanceXform
            trees.append((m.group(1), x.M03 / u, x.M13 / u))
    data["trees"] = trees
    notes.append(u"read: %d area pieces, %d water fills, %d path fills + %d path lines, %d road fills, %d heritage fills, "
                 u"%d trees (%d other blocks)" % (sum(len(v) for v in data["areas"].values()), len(data["water"]),
                                                  len(pf), len(pl_), len(roads), len(data["heritage"]), len(trees), n_other))
    data["to_svg"] = lambda p: mat_pt(Mi, p)
    data["m_per_unit"] = math.sqrt(abs(M[0] * M[3] - M[1] * M[2]))
    a0, a1 = mat_pt(Mi, (0.0, 0.0)), mat_pt(Mi, (0.0, 100.0))   # north (survey +y) on the plan / board (y down)
    L = math.hypot(a1[0] - a0[0], a1[1] - a0[1]) or 1.0
    data["north"] = ((a1[0] - a0[0]) / L, (a1[1] - a0[1]) / L)
    allp = [p for v in data["areas"].values() for r_ in v for r in r_.rings for p in r]
    if not allp:
        allp = [(t[1], t[2]) for t in trees] or [(0.0, 0.0)]
    data["plan_bb"] = (min(p[0] for p in allp), min(p[1] for p in allp), max(p[0] for p in allp), max(p[1] for p in allp))
    data["u"] = u
    return data


def draw_rhino(doc, B, icons, data, notes):
    """the board on masterplan::analysis_planting::<part>; the last board deleted first"""
    import Rhino
    import System
    rg = Rhino.Geometry
    u = data["u"]
    tol = doc.ModelAbsoluteTolerance
    x0 = data["plan_bb"][0]
    y0 = data["plan_bb"][1] - BOARD_GAP_M
    W = lambda p: rg.Point3d((x0 + p[0]) * u, (y0 - p[1]) * u, 0.0)
    root = doc.Layers.FindByFullPath(ROOT_LAYER, -1)
    if root < 0:
        L_ = Rhino.DocObjects.Layer()
        L_.Name = ROOT_LAYER
        root = doc.Layers.Add(L_)
    base = ROOT_LAYER + "::" + BOARD_LAYER
    es = Rhino.DocObjects.ObjectEnumeratorSettings()
    es.HiddenObjects = True
    es.LockedObjects = True
    old = [o.Id for o in doc.Objects.GetObjectList(es) if doc.Layers[o.Attributes.LayerIndex].FullPath.startswith(base)]
    for i in old:
        doc.Objects.Delete(i, True)
    for d in list(doc.InstanceDefinitions):
        try:
            if d is not None and not d.IsDeleted and d.Name.startswith("pa_icon_"):
                doc.InstanceDefinitions.Delete(d.Index, True, True)
        except Exception:
            pass
    lix = {}

    def layer(part):
        if part in lix:
            return lix[part]
        bi = doc.Layers.FindByFullPath(base, -1)
        if bi < 0:
            L_ = Rhino.DocObjects.Layer()
            L_.Name = BOARD_LAYER
            L_.ParentLayerId = doc.Layers[root].Id
            bi = doc.Layers.Add(L_)
        i = doc.Layers.FindByFullPath(base + "::" + part, -1)
        if i < 0:
            L_ = Rhino.DocObjects.Layer()
            L_.Name = part
            L_.ParentLayerId = doc.Layers[bi].Id
            i = doc.Layers.Add(L_)
        lix[part] = i
        return i
    solid = -1
    for mk in (lambda: doc.HatchPatterns.FindName("Solid").Index,
               lambda: doc.HatchPatterns.Add(Rhino.DocObjects.HatchPattern.Defaults.Solid)):
        try:
            solid = int(mk())
            if solid >= 0:
                break
        except Exception:
            pass
    order = [0]

    def attr(part, col, lw=None):
        a = Rhino.DocObjects.ObjectAttributes()
        a.LayerIndex = layer(part)
        order[0] += 1
        try:
            a.DisplayOrder = order[0]
        except Exception:
            pass
        c = System.Drawing.ColorTranslator.FromHtml(col) if isinstance(col, str) else \
            System.Drawing.Color.FromArgb(255, col[0], col[1], col[2])
        a.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
        a.ObjectColor = c
        a.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromObject
        a.PlotColor = c
        if lw is not None:
            a.PlotWeightSource = Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject
            a.PlotWeight = max(0.01, float(lw))
        return a
    n = {"fills": 0, "lines": 0, "texts": 0, "icons": 0}
    blk = {}

    def icon_block(k, part):
        if (k, part) in blk:
            return blk[(k, part)]
        blk[(k, part)] = -1
        shapes, frag, box = icons[k][part]
        m = icon_matrix(part, box)
        geos, atts = [], []
        for sh in shapes:
            for c in shape_curves([(cl, [mat_pt(m, s[0])] + [tuple([seg[0]] + [mat_pt(m, q) for q in seg[1:]]) for seg in s[1:]])
                                   for cl, s in sh["subs"]], lambda p: rg.Point3d(p[0] * u, -p[1] * u, 0.0), tol, sh["fill"] is not None):
                if sh["fill"] is not None and c.IsClosed and solid >= 0:
                    for h in rg.Hatch.Create([c], solid, 0.0, 1.0, tol) or []:
                        geos.append(h)
                        atts.append(attr("species", sh["fill"]))
                if sh["stroke"] is not None:
                    geos.append(c)
                    atts.append(attr("species", sh["stroke"], sh["lw"] * m[0]))
        if geos:
            for a in atts:
                a.LayerIndex = root
            blk[(k, part)] = doc.InstanceDefinitions.Add("pa_icon_%s_%s_%s" % (k, part, time.strftime("%H%M%S")),
                                                         "planting analysis: Aras's %s of %s (agaclar.svg)" % (part, k),
                                                         rg.Point3d.Origin, geos, atts)
        return blk[(k, part)]
    for p in B.p:
        part = p["L"]
        if p["k"] == "poly":
            crvs = []
            for r in p["rings"]:
                Q = [W(q) for q in r]
                if p["fill"] is not None or (len(r) > 2 and r[0] == r[-1]):
                    Q = Q + [Q[0]]
                if len(Q) >= 2:
                    crvs.append(rg.PolylineCurve(Q))
            if p["fill"] is not None and solid >= 0:
                cs = [c for c in crvs if c.IsClosed]
                for h in (rg.Hatch.Create(cs, solid, 0.0, 1.0, tol) if cs else None) or []:
                    doc.Objects.AddHatch(h, attr(part, p["fill"]))
                    n["fills"] += 1
            if p["stroke"] is not None:
                for c in crvs:
                    doc.Objects.AddCurve(c, attr(part, p["stroke"], p["sw"]))
                    n["lines"] += 1
        elif p["k"] == "text":
            te = rg.TextEntity.Create(p["s"], rg.Plane(W((p["x"], p["y"])), rg.Vector3d.XAxis, rg.Vector3d.YAxis),
                                      doc.DimStyles.Current, False, 0.0, 0.0)
            te.TextHeight = p["size"] * CAP * u
            try:
                te.DimensionScale = 1.0
            except Exception:
                pass
            try:
                te.Font = Rhino.DocObjects.Font.FromQuartetProperties(FONT, bool(p["bold"]), bool(p["italic"]))
            except Exception:
                pass
            try:
                te.TextHorizontalAlignment = {"start": Rhino.DocObjects.TextHorizontalAlignment.Left,
                                              "middle": Rhino.DocObjects.TextHorizontalAlignment.Center,
                                              "end": Rhino.DocObjects.TextHorizontalAlignment.Right}[p["anchor"]]
                te.TextVerticalAlignment = Rhino.DocObjects.TextVerticalAlignment.Bottom
            except Exception:
                pass
            doc.Objects.AddText(te, attr(part, p["fill"]))
            n["texts"] += 1
        elif p["k"] == "icon":
            bi = icon_block(p["key"], p["part"])
            if bi >= 0:
                o_ = W((p["x"], p["y"]))
                xf = rg.Transform.Translation(rg.Vector3d(o_.X, o_.Y, 0.0)) * rg.Transform.Scale(rg.Point3d.Origin, p["scale"])
                doc.Objects.AddInstanceObject(bi, xf, attr(part, "#000000"))
                n["icons"] += 1
        elif p["k"] == "grad":
            k_ = 40
            for i in range(k_):
                t = (i + 0.5) / k_
                st = p["stops"]
                for (t0, c0), (t1, c1) in zip(st, st[1:]):
                    if t0 <= t <= t1:
                        col = mix(c0, c1, (t - t0) / (t1 - t0))
                        break
                x = p["x"] + p["w"] * i / k_
                Q = [W(q) for q in ((x, p["y"]), (x + p["w"] / k_, p["y"]), (x + p["w"] / k_, p["y"] + p["h"]), (x, p["y"] + p["h"]))]
                for h in rg.Hatch.Create([rg.PolylineCurve(Q + [Q[0]])], solid, 0.0, 1.0, tol) or []:
                    doc.Objects.AddHatch(h, attr(part, col))
                    n["fills"] += 1
    notes.append(u"board drawn in Rhino on %s::<part> (%d parts), %d below the plan's south edge: " %
                 (base, len(lix), int(BOARD_GAP_M)) + u", ".join(u"%s %d" % kv for kv in sorted(n.items())))


def shape_curves(subs, P, tol, close_all):
    """sub-paths (L / C pieces) -> Rhino curves (as PlanToRhino v2 bakes them)"""
    import Rhino
    rg = Rhino.Geometry
    out = []
    for cl, s in subs:
        cl = cl or close_all
        if all(seg[0] == "L" for seg in s[1:]):
            Q = [P(s[0])] + [P(seg[1]) for seg in s[1:]]
            if cl and len(Q) > 2:
                Q.append(Q[0])
            if len(Q) >= 2:
                out.append(rg.PolylineCurve(Q))
            continue
        pc = rg.PolyCurve()
        last = P(s[0])
        for seg in s[1:]:
            if seg[0] == "L":
                q = P(seg[1])
                if last.DistanceTo(q) > tol:
                    pc.Append(rg.LineCurve(last, q))
                    last = q
            else:
                cps = [last, P(seg[1]), P(seg[2]), P(seg[3])]
                pc.Append(rg.BezierCurve(cps).ToNurbsCurve())
                last = cps[3]
        if cl and last.DistanceTo(P(s[0])) > tol:
            pc.Append(rg.LineCurve(last, P(s[0])))
        if pc.SegmentCount:
            out.append(pc)
    return out


# =====================================================================================================  main
def main(doc=None, data=None):
    t0 = time.time()
    notes = [u"%s %s · %s" % (GH_LABEL, VERSION, time.strftime("%Y-%m-%d %H:%M"))]
    if data is None:
        data = read_layers(doc, notes)
    res = analyse(data, notes)
    icons = aras_icons(AGACLAR, notes)
    B = build_board(data, res, icons, notes)
    svg = board_svg(B, icons)
    os.makedirs(os.path.dirname(OUT_SVG), exist_ok=True)
    if os.path.isfile(OUT_SVG):
        prev = OUT_SVG[:-4] + "_prev.svg"
        if os.path.isfile(prev):
            os.remove(prev)
        os.replace(OUT_SVG, prev)
    with open(OUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg)
    notes.append(u"board SVG (open in Illustrator, one group per part): %s (%.1f MB)" % (OUT_SVG, len(svg) / 1048576.0))
    if doc is not None:
        import scriptcontext as sc_
        old = sc_.doc
        try:
            sc_.doc = doc
            doc.Views.RedrawEnabled = False
            draw_rhino(doc, B, icons, data, notes)
        finally:
            doc.Views.RedrawEnabled = True
            sc_.doc = old
        doc.Views.Redraw()
    notes.append(u"single tree in a lawn: > %g m from walks, > %g m from water and no other tree within %g m (board v9 "
                 u"used a random lawn pattern here, which cannot be read back from the layers)" %
                 (OPEN_LAWN[0], OPEN_LAWN[1], SOLO_GAP_M))
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


# ---- Grasshopper wiring (template; PlanToRhino v2's 'done' wired into run = a press per new value) ----
if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # noqa: F821
    except Exception:
        pass
    _rv = globals().get("run")
    if isinstance(_rv, list):
        _rv = next((x for x in _rv if x is not None), None)
    _pressed = _rv is True
    if isinstance(_rv, str) and _rv.startswith("done ") and _sc.sticky.get(_k + "_chain") != _rv:
        _sc.sticky[_k + "_chain"] = _rv
        _pressed = True
    if _pressed:
        _t0 = time.time()
        try:
            import Rhino as _Rh
            _res = main(doc=_Rh.RhinoDoc.ActiveDoc)
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
    log = _sc.sticky.get(_k + "_log", "Press the Button (or wire PlanToRhino v2's done into run): the planting board is "
                                      "rebuilt from the layers under masterplan")
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
