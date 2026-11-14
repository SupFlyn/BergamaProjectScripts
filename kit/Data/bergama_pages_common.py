# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE COMMON v1 (14 Nov 2026), the shared code of the new page scripts (one script per page).
Loaded by exec from Downloads/Bergama/Data/bergama_pages_common.py by bergama_page_transit_v*.py and
bergama_page_heritage_v*.py, so both maps have the SAME frame, scale, context and key (Aras 14 Nov 10:45 UTC: "this
diagram and that one ... should not collide with each other"; 10:51: "transit hubs and heritage loop is two different
slides").

What it gives:
  pc_root(), pc_data(log)            the root folder and Data/bergama_access_heritage.json (frame, stops, lines, key)
  pc_lib(log)                        the PDF / SVG writer of the newest Basemap script (bergama_basemap_v*.py)
  Map(D, den)                        the shared frame: survey m -> sheet mm (north up), sheet size, map box
  pc_mapbase(M, K, log)              the context: the one MapBase cache (press MapBase first), in a quiet look
  pc_study(M, D, log)                the study area (calisma_alan) from the Basemap cache, dash-dot
  pc_lines / pc_stops / pc_hubs ...  the transit layer (used fully on the transit page, greyed on the heritage page)
  pc_heritage(...)                   the heritage places (numbered on the heritage page, dots on the transit page)
  Labels                             name placement that avoids every symbol and name already placed (never drops)
  pc_sheet(...)                      title, legend, north + scale, credit round the map
  pc_write(...)                      PDF + SVG + review PNGs (Aras 14 Nov 10:44: "all scripts should produce PNG's
                                     aswell which should be optimized for your viewing": trimmed, 200 ppi, tiles of
                                     at most 1400 px so nothing is scaled down when read)
Items are the Basemap writer's tuples (page mm, y up):
  ("poly", rings, fill, stroke, lw, None, layer, 1, None, None)
  ("line", pts, stroke, lw, None, layer, 1 | (on mm, off mm))
  ("text", s, x, y, size mm, colour, bold, align "L"|"C"|"R", layer, angle | None, None)
"""
import os, re, json, math, time, glob

PC_VERSION = "v3.11"  # v3.11: pc_loop (the heritage loop, one code for the heritage and the transit map; Aras 15:31) and pc_station_name; v3.10: pc_a3_den / pc_a3 (a map page fitted and centred on A3 or a slide panel, Aras 15:25-15:27 UTC); v3.9: no sources in the drawings (Aras 15:23 UTC): pc_nosrc on MapBase legend rows, empty credit skipped; v3.8: a name with no free place goes where it overlaps least (run 7); v3.7: Labels.block_line / block_items (names keep off lines: run 6 review); v3.6: the outside Python runs hidden (no console window, Aras 14 Nov 12:57 UTC); v3.5: frame check skips items with any clip id; pc_mb_lib (MapBase as a library, any projection), pc_sheet north angle, pc_photos (JPEGs into PDF / SVG), pc_write photos / clips; v3.3: pc_frame_check (FLAG map ink outside the map frame); v3.2: context houses cut to the map frame
PC_NOWIN = 0x08000000 if os.name == "nt" else 0   # v3.6: CREATE_NO_WINDOW for the review-PNG / photo subprocesses
PC_DATA = os.path.join("Data", "bergama_access_heritage.json")
PC_CENTRE = os.path.join("Data", "selinos_centreline.json")
PC_LIB_GLOB = os.path.join("scripts", "bergama_basemap_v*.py")
PC_LIB_END = "# ================================================================ main"
PC_STUDY_CACHE = os.path.join("cached", "bergama_basemap", "basemap_layers.json")
PC_CACHE_DIR = os.path.join("cached", "bergama_pages")
PC_MB_GLOB = os.path.join("scripts", "bergama_mapbase_v*.py")
PC_MB_END = "\n# ================================================================ main\n"
PC_CLIP = "map"               # v3.3: the clip id of the map frame (MapBase items are cut to it in the PDF / SVG)
PC_MARGIN_MM = 12.0          # sheet margin round the map
PC_SIDE_MM = 95.0            # the column right of the map: title, legend, notes
PC_PNG_PPI = 200
PC_PNG_TILE = 1400           # px: largest side of one review tile


def pc_root():
    return os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def pc_data(log):
    p = os.path.join(pc_root(), PC_DATA)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    with open(p, encoding="utf-8") as f:
        D = json.load(f)
    log.append(u"data: %s (%d stops, %d lines, %d heritage places)" % (p, len(D["stops"]), len(D["routes"]),
                                                                      len(D["heritage"])))
    return D


def pc_lib(log):
    """the PDF/SVG writer and text widths of the newest Basemap script (everything above its main)"""
    found = glob.glob(os.path.join(pc_root(), PC_LIB_GLOB))
    if not found:
        raise RuntimeError(u"no %s: run Bergama.bat once, then press again" % os.path.join(pc_root(), PC_LIB_GLOB))
    src_ = max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])
    with open(src_, encoding="utf-8") as f:
        code = f.read()
    if PC_LIB_END not in code:
        raise RuntimeError(u"%s has no line %r" % (src_, PC_LIB_END))
    ns = {"__name__": "bergama_basemap_lib"}
    exec(compile(code[:code.index(PC_LIB_END)], src_, "exec"), ns)
    for need in ("write_pdf", "write_svg", "text_w"):
        if need not in ns:
            raise RuntimeError(u"%s has no %s: update the kit (Bergama.bat)" % (src_, need))
    PC_STATE["to_survey"] = ns.get("to_survey")
    log.append(u"drawing code: %s (%s %s)" % (src_, ns.get("GH_LABEL"), ns.get("VERSION")))
    return ns


# ================================================================ the shared frame
class Map(object):
    """north up (survey y = north; the survey grid lies within 0.2 deg of true north here: Helmert turn 0.09 deg,
    grid convergence about 0.11 deg, calculated from GEO in the Basemap script and (lon - 27) x sin(lat))"""

    def __init__(self, D, den):
        self.den = float(den)
        self.k = 1000.0 / self.den
        b = D["box"]
        self.b = b
        self.mw, self.mh = (b[2] - b[0]) * self.k, (b[3] - b[1]) * self.k
        self.x0, self.y0 = PC_MARGIN_MM, PC_MARGIN_MM
        self.w = self.x0 + self.mw + 8.0 + PC_SIDE_MM + PC_MARGIN_MM
        self.h = self.y0 + self.mh + PC_MARGIN_MM
        self.box = (self.x0, self.y0, self.x0 + self.mw, self.y0 + self.mh)

    def T(self, p):
        return (self.x0 + (p[0] - self.b[0]) * self.k, self.y0 + (p[1] - self.b[1]) * self.k)

    def inside(self, q, m=0.0):
        return self.box[0] + m <= q[0] <= self.box[2] - m and self.box[1] + m <= q[1] <= self.box[3] - m

    def clip(self, Q):
        """a sheet polyline cut to the map box: list of runs (Liang-Barsky per segment)"""
        x0, y0, x1, y1 = self.box
        runs, cur = [], []
        for a, b in zip(Q, Q[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            t0, t1, ok = 0.0, 1.0, True
            for p_, q_ in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
                if p_ == 0:
                    if q_ < 0:
                        ok = False
                        break
                    continue
                t = q_ / p_
                if p_ < 0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
                if t0 > t1:
                    ok = False
                    break
            if not ok:
                if len(cur) > 1:
                    runs.append(cur)
                cur = []
                continue
            pa = (a[0] + t0 * dx, a[1] + t0 * dy)
            pb = (a[0] + t1 * dx, a[1] + t1 * dy)
            if not cur or abs(cur[-1][0] - pa[0]) > 1e-6 or abs(cur[-1][1] - pa[1]) > 1e-6:
                if len(cur) > 1:
                    runs.append(cur)
                cur = [pa]
            cur.append(pb)
            if t1 < 1.0:
                runs.append(cur)
                cur = []
        if len(cur) > 1:
            runs.append(cur)
        return runs


def pc_dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def circle(cx, cy, r, n=32):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def L_(pts, col, lw, layer, dash=None):
    return ("line", [tuple(p) for p in pts], col, lw, None, layer, dash if dash else 1)


def P_(rings, fill, stroke, lw, layer):
    return ("poly", [[tuple(p) for p in R] for R in rings], fill, stroke, lw, None, layer, 1, None, None)


def T_(s, x, y, size, col, layer, bold=False, align="L"):
    return ("text", s, x, y, size, col, bold, align, layer, None, None)


def offset_line(Q, d):
    """a sheet polyline moved d mm to its left (mitred, the miter capped at 2 x d)"""
    if abs(d) < 1e-9 or len(Q) < 2:
        return list(Q)
    out = []
    n = len(Q)
    for i in range(n):
        a = Q[max(i - 1, 0)]
        b = Q[min(i + 1, n - 1)]
        if i == 0:
            a, b = Q[0], Q[1]
        elif i == n - 1:
            a, b = Q[-2], Q[-1]
        if i in (0, n - 1):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1.0
            out.append((Q[i][0] - dy / L * d, Q[i][1] + dx / L * d))
            continue
        p0, p1, p2 = Q[i - 1], Q[i], Q[i + 1]
        d1 = (p1[0] - p0[0], p1[1] - p0[1])
        d2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1, l2 = math.hypot(*d1) or 1.0, math.hypot(*d2) or 1.0
        n1 = (-d1[1] / l1, d1[0] / l1)
        n2 = (-d2[1] / l2, d2[0] / l2)
        m = (n1[0] + n2[0], n1[1] + n2[1])
        lm = math.hypot(*m)
        if lm < 1e-6:
            out.append((p1[0] + n1[0] * d, p1[1] + n1[1] * d))
            continue
        m = (m[0] / lm, m[1] / lm)
        c = m[0] * n1[0] + m[1] * n1[1]
        s = d / max(c, 0.5)
        out.append((p1[0] + m[0] * s, p1[1] + m[1] * s))
    return out


def ticked(Q, col, lw, every, tick, layer):
    """a line with short ticks across it every `every` mm (the cable car, as the old heritage page)"""
    it = [L_(Q, col, lw, layer)]
    acc = every / 2.0
    for a, b in zip(Q, Q[1:]):
        L = pc_dist(a, b)
        if L <= 0:
            continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        t = acc
        while t < L:
            px, py = a[0] + ux * t, a[1] + uy * t
            it.append(L_([(px - uy * tick, py + ux * tick), (px + uy * tick, py - ux * tick)], col, lw * 0.8, layer))
            t += every
        acc = t - L
    return it


def arrow_head(a, b, col, size, layer):
    """a filled triangle at b pointing from a to b"""
    L = pc_dist(a, b) or 1.0
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    bx, by = b[0] - ux * size, b[1] - uy * size
    return P_([[b, (bx - uy * size * 0.45, by + ux * size * 0.45), (bx + uy * size * 0.45, by - ux * size * 0.45)]],
              col, None, 0.0, layer)


# ================================================================ v3.3: the one base map (MapBase), quiet look
# Aras 14 Nov 12:16 UTC: "also please update all maps to include every detail, and top of the map, data is missing
# please fill in that"; coordinator 12:18: every map draws from the one MapBase script, each page keeps its own styling.
def pc_mb_lib(log):
    """v3.5: the newest MapBase script as a library (mb_load, mb_draw, MB_STYLE, FAB ...)"""
    found = glob.glob(os.path.join(pc_root(), PC_MB_GLOB))
    if not found:
        raise RuntimeError(u"no %s: run Bergama.bat once" % os.path.join(pc_root(), PC_MB_GLOB))
    src_ = max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])
    with open(src_, encoding="utf-8") as f:
        code = f.read()
    if PC_MB_END not in code:
        raise RuntimeError(u"%s has no main line" % src_)
    ns = {"__name__": "bergama_mapbase_lib"}
    exec(compile(code[:code.index(PC_MB_END)], src_, "exec"), ns)
    ns["BERGAMA_ROOT"] = pc_root()
    log.append(u"base map: %s (%s %s)" % (src_, ns.get("GH_LABEL"), ns.get("VERSION")))
    return ns


def pc_mb_data(log):
    """v3.5: (MapBase library, its cache), loaded once a run"""
    if "mb" not in PC_STATE:
        ns = pc_mb_lib(log)
        C = ns["mb_load"](log)
        if C is None:
            raise RuntimeError(u"press MapBase once (it caches the base map every page draws), then this page")
        PC_STATE["mb"] = (ns, C)
    return PC_STATE["mb"]


def pc_mapbase(M, K, log, layers=None, style=None):
    """(items, legend rows [(kind, hex, text)], counts) of the newest MapBase cache in this page's quiet look, cut to
    the map frame (clip PC_CLIP); stops when MapBase has not been pressed (v3.4: no second context of our own).
    v3.5: layers = mb_draw's layer set (None = all), style = keys over the quiet look"""
    ns, C = pc_mb_data(log)
    mix, paper = ns["mixh"], ns["PAPER"]
    soft = lambda c, t: mix(c, paper, t) if c else c
    S = ns["MB_STYLE"]
    bl = K["building"][1]
    st = {"grain": False, "ground": "F4F2EC", "lc_light": 0.7,
          "veg": dict((k_, v) for k_, v in S["veg"].items()),
          "areas": dict((k_, soft(v, 0.55)) for k_, v in S["areas"].items()),
          "landuse": dict((k_, soft(v, 0.5)) for k_, v in S["landuse"].items()),
          "fab": dict((k_, "E2DED6") for k_ in S["fab"]), "fab_com": dict((k_, "E2DED6") for k_ in S["fab_com"]),
          "edge_dark": 0.6, "ink": bl, "street": "FFFFFF", "street_edge": "CFCBC0", "path": "C4BFB2",
          "water": soft(S["water"], 0.45), "water_line": K["water"][0], "wall": "ABA69A", "osm_wall": "ABA69A",
          "her_wall": "A07A62", "tree": "9EA97F", "contour": "D2CABA", "contour_index": "B5AA95",
          "lw": {"hair": 0.06, "osm_wall": 0.08, "contour": 0.07, "contour_index": 0.14}}
    st["veg"] = dict((k_, soft(v, 0.3)) for k_, v in st["veg"].items())
    st["fab"]["monument"] = st["fab_com"]["monument"] = "D8C8BC"
    st["fab"]["sacred"] = st["fab_com"]["sacred"] = "D8C8BC"
    st.update(style or {})
    items = []
    cnt = ns["mb_draw"](C, items, M.T, M.k, M.box, PC_CLIP, st, layers)
    rows = ns["mb_legend"](C, cnt, st)
    if cnt.get("buildings"):
        rows.append(("box", "E2DED6", u"Buildings (survey, else OSM); monuments and mosques a shade warmer"))
    if cnt.get("walls") or cnt.get("walls_osm"):
        rows.append(("line", st["wall"], u"Walls and retaining walls (survey; OSM where the survey has none)"))
    if cnt.get("heritage_walls"):
        rows.append(("line", st["her_wall"], u"Ancient and city walls (survey and OSM)"))
    if cnt.get("trees_osm"):
        rows.append(("dot", st["tree"], u"Single trees (OSM)"))
    log.append(u"base map drawn: " + u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())))
    return items, rows, cnt


PC_SRC_WORDS = r"OSM|ESHOT|survey|surveyed|WorldCover|GLO-30|image|MapBase|Copernicus|Wikipedia|calculated"


def pc_nosrc(t):
    """v3.9, Aras 14 Nov 15:23 UTC: "dont give sources in the brackets dont give sources in the drawings at all";
    15:24: "no sources for nothing": a text without its source brackets (sources stay in the log)"""
    t = re.sub(r"\s*\([^()]*\b(%s)\b[^()]*\)" % PC_SRC_WORDS, u"", t)
    return re.sub(r"\s{2,}", u" ", t).strip()


def pc_mb_legend(rows, K):
    """MapBase legend rows -> pc_sheet rows [(draw(x, y), label)]"""
    out = []
    for kind, col, txt in rows:
        txt = pc_nosrc(txt)
        if kind == "line":
            out.append((lambda x, y, c=col: [L_([(x - 4.5, y), (x + 4.5, y)], c, 0.3, "legend")], txt))
        elif kind == "dot":
            out.append((lambda x, y, c=col: [P_([circle(x, y, 0.7, 12)], c, None, 0.0, "legend")], txt))
        else:
            out.append((lambda x, y, c=col: [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0), (x + 4.5, y + 2.0),
                                                  (x - 4.5, y + 2.0)]], c, K["grey_line"], 0.1, "legend")], txt))
    return out


PC_STATE = {}


PC_A3 = (420.0, 297.0)        # v3.10: A3 landscape, mm


def pc_a3_den(D, extra_w=0.0, step=500.0, page=None):
    """v3.10: the smallest round scale (1:step multiples) at which map + column + extra_w mm fit the page (A3 landscape;
    page = (w, h) mm when a slide sheet asks for another size)"""
    b = D["box"]
    page = page or PC_A3
    fw = page[0] - 2 * PC_MARGIN_MM - 8.0 - PC_SIDE_MM - extra_w
    fh = page[1] - 2 * PC_MARGIN_MM
    den = max((b[2] - b[0]) * 1000.0 / max(fw, 1.0), (b[3] - b[1]) * 1000.0 / fh)
    return int(math.ceil(den / step) * step)


def pc_a3(M, extra_w=0.0, log=None, page=None):
    """v3.10: centre map + column (+ extra_w mm the caller adds to M.w later) on the page (A3 landscape); FLAG if larger"""
    W, H = page or PC_A3
    nw, nh = M.w + extra_w, M.h
    if (nw > W + 0.1 or nh > H + 0.1) and log is not None:
        log.append(u"FLAG: the page is %.0f x %.0f mm, larger than A3" % (nw, nh))
    dx, dy = max(0.0, (W - nw) / 2.0), max(0.0, (H - nh) / 2.0)
    M.x0 += dx
    M.y0 += dy
    M.box = (M.x0, M.y0, M.x0 + M.mw, M.y0 + M.mh)
    M.w, M.h = max(W, nw) - extra_w, max(H, nh)
    return M


def pc_study(M, K, log):
    p = os.path.join(pc_root(), PC_STUDY_CACHE)
    if not os.path.isfile(p):
        log.append(u"FLAG: %s missing: the study area is not drawn (press Basemap once)" % p)
        return []
    with open(p, encoding="utf-8") as f:
        cal = json.load(f).get("calisma") or []
    it = []
    for R in cal:
        Q = [M.T(q) for q in R] + [M.T(R[0])]
        for run in M.clip(Q):
            it.append(L_(run, K["study"][0], K["study"][1], "study_area", (2.4, 0.8)))
    log.append(u"study area: %d ring(s) from %s" % (len(cal), p))
    return it


# ================================================================ transit
def pc_stop_lines(D):
    """{stop name: set of line refs}: OSM membership, corrected by ESHOT where the data notes a conflict"""
    out = {}
    for s in D["stops"]:
        out.setdefault(s["name"], set()).update(s["lines"])
    for fx in D.get("official_fixes", []):
        if fx.get("add") and fx["name"] in out:
            out[fx["name"]].update(fx["add"])
    return out


def pc_stop_groups(D):
    """the stops merged by name within 80 m (the two sides of a street): [(name, survey xy, lines)]"""
    lines = pc_stop_lines(D)
    out = []
    for s in D["stops"]:
        for g in out:
            if g[0] == s["name"] and pc_dist(g[1], s["xy"]) < 80.0:
                g[3].append(s["xy"])
                break
        else:
            out.append([s["name"], s["xy"], lines.get(s["name"], set()), [s["xy"]]])
    res = []
    for n, _xy, ln, pts in out:
        res.append((n, (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)), ln))
    return res


def pc_group_of(D, ref):
    for g, v in D["lines"].items():
        if ref in v["refs"]:
            return g
    return None


def pc_line_items(M, D, K, grey=None):
    """every bus way once, one lane per line group on it (town, 656, village, regional), side by side; grey = one
    thin grey line per way instead (the heritage page)"""
    groups_on = {}
    for ref, R in D["routes"].items():
        g = pc_group_of(D, ref)
        for wid in R["ways"]:
            groups_on.setdefault(wid, set()).add(g)
    it = []
    order = K["line_order"]
    for wid, gs in sorted(groups_on.items()):
        P = D["ways"].get(wid)
        if not P:
            continue
        Q = [M.T(p) for p in P]
        if grey:
            for run in M.clip(Q):
                it.append(L_(run, grey[0], grey[1], "bus_lines"))
            continue
        gl = [g for g in order if g in gs]
        ws = [K["lines"][g][1] for g in gl]
        tot = sum(ws) + K["lane_gap"] * (len(gl) - 1)
        off = -tot / 2.0
        for g, w in zip(gl, ws):
            col, _w, dash = K["lines"][g]
            QQ = offset_line(Q, off + w / 2.0)
            for run in M.clip(QQ):
                it.append(L_(run, col, w, "bus_lines/" + g, tuple(dash) if dash else None))
            off += w + K["lane_gap"]
    return it


# ================================================================ labels that never sit on a symbol or a name
class Labels(object):
    def __init__(self, M, lib):
        self.M, self.lib, self.boxes, self.items, self.forced = M, lib, [], [], []

    def block(self, b):
        self.boxes.append(b)

    def block_pt(self, q, r):
        self.boxes.append((q[0] - r, q[1] - r, q[0] + r, q[1] + r))

    def block_line(self, P, r):
        """v3.7 (run 6 review: names sat on the spine, the river and the study line): keep names r mm off a polyline
        (page mm), as small boxes every r mm along it"""
        st = max(r, 0.5)
        for a, c in zip(P, P[1:]):
            n = max(1, int(math.hypot(c[0] - a[0], c[1] - a[1]) / st))
            for i in range(n + 1):
                self.block_pt((a[0] + (c[0] - a[0]) * i / n, a[1] + (c[1] - a[1]) * i / n), r)

    def block_items(self, items, layers, pad=0.4):
        """v3.7: block_line for every line item of these layers, half its width + pad"""
        for it in items:
            if it[0] == "line" and it[5] in layers:
                self.block_line(it[1], (it[3] or 0.1) / 2.0 + pad)

    def free(self, b):
        if not (self.M.box[0] <= b[0] and b[2] <= self.M.box[2] and self.M.box[1] <= b[1] and b[3] <= self.M.box[3]):
            return False
        return not any(b[0] < o[2] and o[0] < b[2] and b[1] < o[3] and o[1] < b[3] for o in self.boxes)

    def put(self, s, q, size, col, layer, bold=False, gap=1.6, halo=True):
        """try 8 places round q (right, left, above, below, the corners, then twice as far); the first free one, else
        the right-hand place anyway and a log line (a name is never left out)"""
        w = self.lib["text_w"](s, size, bold)
        h = size * 0.75
        cands = []
        for g in (gap, gap * 2.2, gap * 3.6):
            cands += [(q[0] + g, q[1] - h / 2.0, "L"), (q[0] - g, q[1] - h / 2.0, "R"), (q[0], q[1] + g, "C"),
                      (q[0], q[1] - g - h, "C"), (q[0] + g * 0.8, q[1] + g * 0.8, "L"),
                      (q[0] - g * 0.8, q[1] + g * 0.8, "R"), (q[0] + g * 0.8, q[1] - g * 0.8 - h, "L"),
                      (q[0] - g * 0.8, q[1] - g * 0.8 - h, "R")]
        pick = None
        for x, y, al in cands:
            x0 = x if al == "L" else x - w if al == "R" else x - w / 2.0
            b = (x0 - 0.3, y - 0.25 * size - 0.3, x0 + w + 0.3, y + h + 0.3)
            if self.free(b):
                pick = (x, y, al, b)
                break
        if pick is None:                                 # v3.8: the place with the least overlap (was: right-hand)
            def lap(b_):
                return sum(max(0.0, min(b_[2], o[2]) - max(b_[0], o[0])) * max(0.0, min(b_[3], o[3]) - max(b_[1], o[1]))
                           for o in self.boxes)
            best = None
            for x, y, al in cands:
                x0 = x if al == "L" else x - w if al == "R" else x - w / 2.0
                b = (x0 - 0.3, y - 0.25 * size - 0.3, x0 + w + 0.3, y + h + 0.3)
                inside = self.M.box[0] <= b[0] and b[2] <= self.M.box[2] and self.M.box[1] <= b[1] and b[3] <= self.M.box[3]
                if inside and (best is None or lap(b) < best[0]):
                    best = (lap(b), (x, y, al, b))
            x, y, al = cands[0]
            pick = best[1] if best else (x, y, al, (x - 0.3, y - 0.3, x + w + 0.3, y + h + 0.3))
            self.forced.append(s)
        x, y, al, b = pick
        self.boxes.append(b)
        if halo:
            self.items.append(P_([[(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])]], "FFFFFF", None, 0.0,
                                 layer + "_halo"))
        self.items.append(T_(s, x, y, size, col, layer, bold, al))


def pc_selinos_line():
    """v3.4: the Selinos centreline in survey m, upstream first (Data/selinos_centreline.json, the line the surveyed
    sections were cut on; the same file Basemap and the section scripts read), read once"""
    if "selinos" not in PC_STATE:
        with open(os.path.join(pc_root(), PC_CENTRE), encoding="utf-8") as f:
            PC_STATE["selinos"] = [tuple(q) for q in json.load(f)["points"]]
    return PC_STATE["selinos"]


def pc_selinos(a, b):
    """the stretch of the Selinos centreline between the points nearest to a and b (survey m), a and b added
    at the ends: the streamside spine and the stream walk follow the stream, not straight legs; None if either point
    lies over 80 m from the line"""
    P = pc_selinos_line()
    if not P:
        return None
    ia = min(range(len(P)), key=lambda i: pc_dist(P[i], a))
    ib = min(range(len(P)), key=lambda i: pc_dist(P[i], b))
    if pc_dist(P[ia], a) > 80.0 or pc_dist(P[ib], b) > 80.0:
        return None
    lo, hi = min(ia, ib), max(ia, ib)
    S = list(P[lo:hi + 1])
    if ia > ib:
        S = S[::-1]
    return [tuple(a)] + S + [tuple(b)]


# ================================================================ v3.10: the heritage loop, drawn by one code on both maps
# Aras 14 Nov 15:31 UTC: "the bold connection between the heritage should stay there just like the old diagram" (on the
# transit map too); 12:38: "don't ever do the same job twice in two scripts".
def pc_station_name(s):
    """an OSM station name as both maps print it (Turkish letters: 'Teleferik, Yukarı İstasyon')"""
    return (s.get("name") or u"").replace(u"Akropolis Teleferik - ", u"Teleferik, ").replace(u" ( ", u" (").replace(
        u" )", u")")


def pc_loop(M, D, K, lab, log):
    """the loop 1..7: bold red legs stop to stop (3 -> 4 along the Selinos: the stream walk), dotted on foot from the
    upper Teleferik station to Akropol, red numbered badges, Akropol a red ring; lines and badges kept free of names
    (lab). Returns items"""
    T, it = M.T, []
    RED, W, R, tm = K["heritage"], K["heritage_w"], K["heritage_r"], K["text_mm"]
    H = sorted(D["heritage"], key=lambda h: int(h["n"]))
    legs = []
    for a, b in zip(H, H[1:]):
        if (a["key"], b["key"]) == ("tabak_koprusu", "ulucami_onu"):
            sw = pc_selinos(a["xy"], b["xy"])
            if sw:
                legs.append(("walk", sw))
                log.append(u"stream walk: Tabak Köprüsü -> Ulucami Önü along the Selinos, %.0f m" % sum(
                    pc_dist(p, q) for p, q in zip(sw, sw[1:])))
                continue
            log.append(u"FLAG: the Selinos line is over 80 m from stop 3 or 4: the stream walk is drawn straight")
        legs.append(("leg", [a["xy"], b["xy"]]))
    for kind, P in legs:
        for run in M.clip([T(p) for p in P]):
            it.append(L_(run, "FFFFFF", W + 0.6, "loop"))
            it.append(L_(run, RED, W + (0.6 if kind == "walk" else 0.0), "loop"))
            if kind == "walk":
                it.append(L_(run, "FFFFFF", 0.3, "loop", (1.2, 1.2)))
            lab.block_line(run, W / 2.0 + 0.6)
    upper = next((s for s in D["stations"] if s["kind"] == "gondola" and u"Yukarı" in (s["name"] or u"")), None)
    if upper:
        for run in M.clip([T(upper["xy"]), T(D["akropol"])]):
            it.append(L_(run, RED, 0.5, "loop", (0.01, 1.0)))
    log.append(u"loop: %d stops, %d legs, %.0f m stop to stop (straight legs; the walk along the stream)" % (
        len(H), len(legs), sum(pc_dist(p, q) for _k, P in legs for p, q in zip(P, P[1:]))))
    for h in H:
        q = T(h["xy"])
        if not M.inside(q):
            log.append(u"FLAG: stop %s %s lies outside the frame" % (h["n"], h["name"]))
            continue
        it.append(P_([circle(q[0], q[1], R, 32)], RED, "FFFFFF", 0.35, "loop_stops"))
        it.append(T_(h["n"], q[0], q[1] - tm["label"] * 0.36, tm["label"] + 0.2, "FFFFFF", "loop_stops", True, "C"))
        lab.block_pt(q, R + 0.6)
    qa = T(D["akropol"])
    it.append(P_([circle(qa[0], qa[1], R * 0.8, 32)], "FFFFFF", RED, 0.6, "loop_stops"))
    lab.block_pt(qa, R)
    return it


# ================================================================ sheet furniture (right-hand column)
def pc_sheet(M, K, lib, title, sub, legend, notes, credit, north=0.0, bar_note=None):
    """legend = [(draw(x, y) -> items, label)], swatch 10 x 5 mm; (None, text) = a bold header row; notes = [text];
    returns items"""
    it = []
    tm = K["text_mm"]
    INK = K["ink"]
    tw = lib["text_w"]
    x = M.box[2] + 8.0
    W = PC_SIDE_MM
    y = M.box[3] - tm["title"]
    for ln in wrap(title.upper(), tm["title"], W, tw, True):
        it.append(T_(ln, x, y, tm["title"], INK, "title", True))
        y -= tm["title"] * 1.25
    y -= 1.0
    for ln in wrap(sub, tm["sub"], W, tw):
        it.append(T_(ln, x, y, tm["sub"], INK, "title"))
        y -= tm["sub"] * 1.4
    y -= 5.0
    for draw, label in legend:
        if draw is None:                                 # a header row (EXISTING ... / PROPOSAL MARKS), as the node pages
            y -= 1.5
            it.append(T_(label, x, y, tm["legend"], INK, "legend", True))
            y -= 6.0
            continue
        it += draw(x + 5.0, y + 1.0)
        lines = wrap(label, tm["legend"], W - 14.0, tw)
        yy = y
        for ln in lines:
            it.append(T_(ln, x + 13.0, yy, tm["legend"], INK, "legend"))
            yy -= tm["legend"] * 1.3
        y = min(y - 6.0, yy - 2.0)
    y -= 3.0
    for nt in notes:
        for ln in wrap(nt, tm["small"] + 0.2, W, tw):
            it.append(T_(ln, x, y, tm["small"] + 0.2, INK, "notes"))
            y -= (tm["small"] + 0.2) * 1.4
        y -= 1.5
    # north arrow + scale bar under the column, above the credit
    yb = M.box[1] + 30.0
    cx, cy, r = x + 7.0, yb + 7.0, 5.5
    it.append(P_([circle(cx, cy, r, 48)], None, INK, 0.2, "north_scale"))
    ca_, sa_ = math.cos(math.radians(north)), math.sin(math.radians(north))   # v3.5: north turned clockwise (deg)
    rot = lambda dx, dy: (cx + dx * ca_ + dy * sa_, cy - dx * sa_ + dy * ca_)
    it.append(P_([[rot(0, r), rot(-2.4, -2.6), rot(0, -1.2), rot(2.4, -2.6)]], INK, None, 0.0, "north_scale"))
    q_ = rot(0, r + 2.4)
    it.append(T_(u"N", q_[0], q_[1] - 1.0, 2.6, INK, "north_scale", True, "C"))
    bar = 100.0 if M.den <= 2500 else 250.0 if M.den <= 6000 else 500.0
    Lb = bar * M.k
    xb, yb2 = x + 18.0, yb + 4.0
    for i in range(4):
        it.append(P_([[(xb + Lb * i / 4, yb2), (xb + Lb * (i + 1) / 4, yb2), (xb + Lb * (i + 1) / 4, yb2 + 1.4),
                       (xb + Lb * i / 4, yb2 + 1.4)]], INK if i % 2 == 0 else "FFFFFF", INK, 0.15, "north_scale"))
    it.append(T_(u"0", xb, yb2 - 3.0, 2.0, INK, "north_scale", False, "C"))
    it.append(T_(u"%d m" % bar, xb + Lb, yb2 - 3.0, 2.0, INK, "north_scale", False, "C"))
    it.append(T_(u"1:%s" % format(int(M.den), ",d"), xb, yb2 + 4.0, 3.2, INK, "north_scale", True))
    if bar_note:
        it.append(T_(bar_note, xb, yb2 - 6.2, 2.0, INK, "north_scale"))
    yc = M.box[1] + 20.0
    for ln in (wrap(credit, tm["small"], W, tw) if credit else []):   # v3.9: no credit line (no sources)
        it.append(T_(ln, x, yc, tm["small"], "6E6C66", "credit"))
        yc -= tm["small"] * 1.4
    it.append(P_([[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]], None,
                 INK, 0.25, "frame"))
    return it


def wrap(s, size, width, tw, bold=False):
    out, line = [], u""
    for wd in s.split(u" "):
        t = (line + u" " + wd).strip()
        if line and tw(t, size, bold) > width:
            out.append(line)
            line = wd
        else:
            line = t
    if line:
        out.append(line)
    return out


# ================================================================ outputs: PDF, SVG, review PNGs
def pc_write(lib, M, items, out_dir, name, title, log, photos=None, clips=None):
    """v3.5: photos = pc_photos list (placed before the review PNGs); clips = own clip rings (default: the map box)"""
    os.makedirs(out_dir, exist_ok=True)
    pc_frame_check(items, M.box, log, lib.get("text_w"))
    paths = []
    for ext, fn in ((".pdf", lib["write_pdf"]), (".svg", lib["write_svg"])):
        p = os.path.join(out_dir, name + ext)
        try:
            clips = clips or {PC_CLIP: [[[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]),
                                         (M.box[0], M.box[3])]]]}          # v3.3: the MapBase items are cut to the frame
            p2 = fn(p, M.w, M.h, items, title, clips)
            paths.append(p2 or p)
        except Exception as ex:
            log.append(u"FLAG: %s not written (%s: %s)" % (p, type(ex).__name__, ex))
    for p in paths:
        log.append(u"%s  %s (%.0f x %.0f mm, 1:%s, %d objects)" % (p, time.strftime("%H:%M:%S"), M.w, M.h,
                                                                   format(int(M.den), ",d"), len(items)))
    if photos:
        pc_photos(paths, photos, M.h, log)
    pdfs = [p_ for p_ in paths if p_.lower().endswith(".pdf")]
    if not (pdfs and pc_review(pdfs[0], os.path.join(out_dir, "review"), log)):
        try:
            pc_png(items, M, os.path.join(out_dir, "review"), name, log)
        except Exception as ex:
            log.append(u"FLAG: review PNGs stopped (%s: %s)" % (type(ex).__name__, ex))
    return paths


# ================================================================ review PNGs, the standard of every page script
# v3, Aras 14 Nov 11:25 UTC: "every script should have it as a standard procedure to produce review png's in the most
# efficient way that claude reads ... optimize for yourself reading"; 11:26 UTC: "dont crop to the drawing have the all
# page ... if something goes out of the drawing you would want to see it". From the PDF (what is printed): the WHOLE
# page, 200 ppi, cut into an even grid of tiles of at most 1100 x 500 px (read without any downscale), plus
# 00_overview.png (the whole page, at most 1000 px wide) and index.txt (tile -> page mm, from the top left).
PC_REVIEW = r'''
import sys, os, glob, math
try:
    import pymupdf as fitz
except ImportError:
    import fitz
pdf, out = sys.argv[1], sys.argv[2]
PPI, TW, TH = 200, 1100, 500
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, "*.png")) + glob.glob(os.path.join(out, "index.txt")):
    os.remove(f)
idx = []
doc = fitz.open(pdf)
for pn, pg in enumerate(doc):
    r = pg.rect                                       # the whole page, never cropped (Aras 11:26 UTC)
    pre = "" if len(doc) == 1 else "p%d_" % (pn + 1)
    pg.get_pixmap(dpi=int(min(PPI, 1000.0 * 72 / r.width)), clip=r).save(os.path.join(out, pre + "00_overview.png"))
    W, H = r.width / 72 * PPI, r.height / 72 * PPI
    nc, nr = int(math.ceil(W / TW)), int(math.ceil(H / TH))
    for j in range(nr):
        for i in range(nc):
            t = fitz.Rect(r.x0 + r.width * i / nc, r.y0 + r.height * j / nr, r.x0 + r.width * (i + 1) / nc,
                          r.y0 + r.height * (j + 1) / nr)
            nm = pre + "r%02dc%02d.png" % (j + 1, i + 1)
            pg.get_pixmap(dpi=PPI, clip=t).save(os.path.join(out, nm))
            mm = 25.4 / 72
            idx.append("%s  x %.0f-%.0f mm, y %.0f-%.0f mm from the top left" % (nm, t.x0 * mm, t.x1 * mm, t.y0 * mm,
                                                                               t.y1 * mm))
    n = nc * nr
with open(os.path.join(out, "index.txt"), "w") as f:
    f.write("\n".join(idx) + "\n")
print("review: overview + %d tiles (%d x %d grid, about %d x %d px, 200 ppi) in %s" % (n, nr, nc, W / nc, H / nr, out))
'''


PC_SHEET_LAYERS = ("legend", "title", "notes", "credit", "north_scale", "frame", "map_frame")


def pc_frame_check(items, box, log, text_w=None, skip=PC_SHEET_LAYERS):
    """v3.2 (Aras 12:14 UTC "drawings do flows outside of it"): FLAG every map item (any layer not in skip) whose ink
    leaves the map box (page mm); texts measured with text_w(s, size, bold) when given"""
    bad = {}
    for it in items:
        t = it[0]
        ly = it[6] if t == "poly" else it[5] if t == "line" else it[8] if t == "text" else None
        if ly is None or ly in skip:
            continue
        if (t == "line" and it[4]) or (t == "poly" and len(it) > 9 and it[9]):    # v3.5: any clip id
            continue                                     # v3.3: cut to the frame by its clip in the PDF / SVG
        if t == "text":
            w = text_w(it[1], it[4], bool(it[6])) if text_w else 0.5 * it[4] * len(it[1])
            x = it[2] - {"L": 0.0, "C": w / 2.0, "R": w}.get(it[7], 0.0)
            bx = (x, it[3], x + w, it[3] + it[4])
        else:
            pts = [q for R in it[1] for q in R] if t == "poly" else it[1]
            if not pts:
                continue
            bx = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))
        if bx[0] < box[0] - 0.1 or bx[1] < box[1] - 0.1 or bx[2] > box[2] + 0.1 or bx[3] > box[3] + 0.1:
            bad[ly] = bad.get(ly, 0) + 1
    if bad:
        log.append(u"FLAG frame check: ink outside the map frame: %s" % u", ".join(
            u"%s %d" % (k, v) for k, v in sorted(bad.items())))
    else:
        log.append(u"frame check: all map ink inside its frame")
    return bad


def pc_review(pdf, out, log):
    """the review PNGs of a PDF into folder out (Rhino's Python if it has PyMuPDF, else the Windows py -3 / python);
    True when written"""
    try:
        cdir = os.path.join(pc_root(), PC_CACHE_DIR)
        os.makedirs(cdir, exist_ok=True)
        tp = os.path.join(cdir, "review_tiles_v3.py")
        with open(tp, "w", encoding="utf-8") as f:
            f.write(PC_REVIEW)
        import subprocess, sys as _sys
        cmds = [["py", "-3"], ["python"]]
        if os.path.basename(_sys.executable or "").lower().startswith("python"):
            cmds.insert(0, [_sys.executable])
        # a clean outside Python: Rhino's PYTHONHOME/PYTHONPATH made it fail with "SRE module mismatch" (14 Nov run)
        env = dict((k, v) for k, v in os.environ.items() if not k.upper().startswith("PYTHON"))
        err = u""
        for cmd in cmds:
            try:
                r_ = subprocess.run(cmd + ["-I", tp, pdf, out], capture_output=True, text=True, timeout=600, env=env, creationflags=PC_NOWIN)
            except Exception as ex:
                err = u"%s" % ex
                continue
            if r_.returncode == 0:
                log.append(r_.stdout.strip().splitlines()[-1] if r_.stdout.strip() else u"review: %s" % out)
                return True
            err = (r_.stderr or u"").strip().splitlines()[-1:] or [u""]
            err = err[0]
        log.append(u"FLAG review PNGs not written: no Python with PyMuPDF ran (%s); pip install pymupdf" % err)
    except Exception as ex:
        log.append(u"FLAG review PNGs not written (%s: %s)" % (type(ex).__name__, ex))
    return False


PC_PHOTO = r'''
import sys, json
try:
    import pymupdf as fitz
except ImportError:
    import fitz
pdf, spec = sys.argv[1], sys.argv[2]
with open(spec) as f:
    S = json.load(f)
doc = fitz.open(pdf)
pg = doc[0]
H = pg.rect.height
k = 72.0 / 25.4
for jp, x, y, w, h in S:
    pg.insert_image(fitz.Rect(x * k, H - (y + h) * k, (x + w) * k, H - y * k), filename=jp, keep_proportion=False)
doc.saveIncr()
print("photos: %d placed" % len(S))
'''


def pc_photos(paths, photos, H, log):
    """v3.5: JPEG photos into the written PDF (an outside Python with PyMuPDF, as the review PNGs) and SVG (an <image>
    each). photos = [(jpeg file, x, y, w, h)] in page mm (y up, (x, y) = lower left); H = page height mm"""
    import base64, subprocess, sys as _sys
    for p in paths:
        try:
            if p.lower().endswith(".svg"):
                with open(p, encoding="utf-8") as f:
                    s_ = f.read()
                add = u"".join(u'<image x="%.2f" y="%.2f" width="%.2f" height="%.2f" preserveAspectRatio="none" '
                               u'xlink:href="data:image/jpeg;base64,%s"/>' % (x, H - y - h, w, h, base64.b64encode(
                                   open(jp, "rb").read()).decode("ascii")) for jp, x, y, w, h in photos)
                with open(p, "w", encoding="utf-8") as f:
                    f.write(s_.replace(u"</svg>", u'<g id="photos">' + add + u"</g></svg>"))
                continue
            cdir = os.path.join(pc_root(), PC_CACHE_DIR)
            os.makedirs(cdir, exist_ok=True)
            tp, sp = os.path.join(cdir, "photos_v1.py"), os.path.join(cdir, "photos_spec.json")
            with open(tp, "w", encoding="utf-8") as f:
                f.write(PC_PHOTO)
            with open(sp, "w") as f:
                json.dump(photos, f)
            cmds = [["py", "-3"], ["python"]]
            if os.path.basename(_sys.executable or "").lower().startswith("python"):
                cmds.insert(0, [_sys.executable])
            env = dict((k, v) for k, v in os.environ.items() if not k.upper().startswith("PYTHON"))
            ok = False
            for cmd in cmds:
                try:
                    r_ = subprocess.run(cmd + ["-I", tp, p, sp], capture_output=True, text=True, timeout=300, env=env, creationflags=PC_NOWIN)
                except Exception:
                    continue
                if r_.returncode == 0:
                    log.append(r_.stdout.strip() + u" in " + p)
                    ok = True
                    break
            if not ok:
                log.append(u"FLAG photos not placed in %s: no Python with PyMuPDF ran (pip install pymupdf)" % p)
        except Exception as ex:
            log.append(u"FLAG photos not placed in %s (%s: %s)" % (p, type(ex).__name__, ex))


def pc_present(pdf, slide, log):
    """v2, Aras 14 Nov 11:22 UTC: "in the output folder there should be a folder called presentation and in that folder
    each script output should be called by page name like page 1 is 1.pdf": a copy of the page's PDF as
    Downloads/Bergama/output/presentation/<slide>.pdf"""
    import shutil
    d = os.path.join(pc_root(), "output", "presentation")
    q = os.path.join(d, u"%d.pdf" % int(slide))
    try:
        os.makedirs(d, exist_ok=True)
        shutil.copyfile(pdf, q)
        log.append(u"presentation: %s" % q)
    except Exception as ex:
        log.append(u"FLAG presentation copy %s not written (%s: %s): close it in the PDF viewer and press again" % (
            q, type(ex).__name__, ex))
    return q


def pc_png(items, M, folder, name, log):
    """review PNGs by .NET System.Drawing (Rhino 8 on Windows): the whole sheet at most PC_PNG_TILE px long, then the
    sheet cut into tiles of at most PC_PNG_TILE x PC_PNG_TILE px at PC_PNG_PPI, trimmed to the sheet, nothing scaled down"""
    try:
        import clr
        clr.AddReference("System.Drawing")
        import System.Drawing as SD
        import System.Drawing.Drawing2D as SD2
        import System.Drawing.Text as SDT
        import System.Drawing.Imaging as SDI
    except Exception as ex:
        log.append(u"FLAG: review PNGs not written: System.Drawing not available (%s: %s)" % (type(ex).__name__, ex))
        return
    os.makedirs(folder, exist_ok=True)
    for old in glob.glob(os.path.join(folder, name + u"_*.png")):
        try:
            os.remove(old)
        except Exception:
            pass
    fonts = {}

    def col(h, a=255):
        h = (h or "000000").lstrip("#~")
        return SD.Color.FromArgb(a, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def render(path, ppmm, x0, y0, wpx, hpx):
        bmp = SD.Bitmap(int(wpx), int(hpx))
        g = SD.Graphics.FromImage(bmp)
        g.SmoothingMode = SD2.SmoothingMode.AntiAlias
        g.TextRenderingHint = SDT.TextRenderingHint.AntiAliasGridFit
        g.Clear(SD.Color.White)
        X = lambda x: float((x - x0) * ppmm)
        Y = lambda y: float(hpx - (y - y0) * ppmm)
        for it in items:
            t = it[0]
            if t == "poly":
                rings, fill, stroke, lw = it[1:5]
                gp = SD2.GraphicsPath(SD2.FillMode.Alternate)
                for R in rings:
                    if len(R) >= 3:
                        gp.AddPolygon(System_points(SD, [(X(p[0]), Y(p[1])) for p in R]))
                if fill:
                    g.FillPath(SD.SolidBrush(col(fill)), gp)
                if stroke and lw:
                    g.DrawPath(SD.Pen(col(stroke), float(max(lw * ppmm, 0.6))), gp)
            elif t == "line":
                pts, stroke, lw = it[1:4]
                if len(pts) < 2:
                    continue
                pen = SD.Pen(col(stroke), float(max((lw or 0.1) * ppmm, 0.6)))
                if isinstance(it[6], (tuple, list)):
                    w_ = max((lw or 0.1), 0.05)
                    pen.DashPattern = System_floats([max(it[6][0] / w_, 0.1), max(it[6][1] / w_, 0.1)])
                g.DrawLines(pen, System_points(SD, [(X(p[0]), Y(p[1])) for p in pts]))
            elif t == "text":
                s, x, y, size, color, bold, align = it[1:8]
                kf = (round(size * ppmm, 1), bool(bold))
                if kf not in fonts:
                    fonts[kf] = SD.Font("Arial", float(max(size * ppmm, 1.0)),
                                        SD.FontStyle.Bold if bold else SD.FontStyle.Regular, SD.GraphicsUnit.Pixel)
                f = fonts[kf]
                sz = g.MeasureString(s, f, SD.PointF(0, 0), SD.StringFormat.GenericTypographic)
                xx = X(x) - (sz.Width if align == "R" else sz.Width / 2.0 if align == "C" else 0.0)
                yy = Y(y) - size * ppmm * 0.905           # Arial ascent: the item's y is the baseline
                g.DrawString(s, f, SD.SolidBrush(col(color)), float(xx), float(yy), SD.StringFormat.GenericTypographic)
        g.Dispose()
        bmp.Save(path, SDI.ImageFormat.Png)
        bmp.Dispose()

    n = 0
    k_all = PC_PNG_TILE / max(M.w, M.h)
    render(os.path.join(folder, name + u"_00_whole.png"), k_all, 0.0, 0.0, M.w * k_all, M.h * k_all)
    ppmm = PC_PNG_PPI / 25.4
    tmm = PC_PNG_TILE / ppmm
    nx, ny = int(math.ceil(M.w / tmm)), int(math.ceil(M.h / tmm))
    for j in range(ny):
        for i in range(nx):
            x0, y1 = i * tmm, M.h - j * tmm                # row 1 = the top of the sheet
            w_, h_ = min(tmm, M.w - x0), min(tmm, y1)
            render(os.path.join(folder, u"%s_r%dc%d.png" % (name, j + 1, i + 1)), ppmm, x0, y1 - h_, w_ * ppmm,
                   h_ * ppmm)
            n += 1
    log.append(u"review PNGs: %s (%s_00_whole.png + %d tiles of at most %d px at %d ppi, rows from the top)" % (
        folder, name, n, PC_PNG_TILE, PC_PNG_PPI))


def System_points(SD, pts):
    import System
    arr = System.Array.CreateInstance(SD.PointF, len(pts))
    for i, (x, y) in enumerate(pts):
        arr[i] = SD.PointF(float(x), float(y))
    return arr


def System_floats(v):
    import System
    arr = System.Array.CreateInstance(System.Single, len(v))
    for i, x in enumerate(v):
        arr[i] = float(x)
    return arr
