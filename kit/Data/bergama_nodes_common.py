# -*- coding: utf-8 -*-
"""Bergama Group 6: NODES COMMON v1 (14 Nov 2026): the shared parts of the six node page scripts
scripts/bergama_node_n1_v*.py ... bergama_node_n6_v*.py (Panel Review II slides 7-12, one script per node, Aras 14 Nov
11:14 UTC "dont build all those nodes into single script"). Loaded (not pasted) by each node script.

One A3 landscape page per node (420 x 297 mm, PDF with layers + review PNGs via pages_common pc_review). CHAINED, no
job done twice (Aras 14 Nov 12:38 UTC): Basemap -> MapBase -> Sections -> the node scripts.
  PLAN      the node frame (Data/section_lines.json "nodes") + NODE_MARGIN_M round it on its own axes; context = MapBase
            (mb_draw, its cache); over it the section lines, bus lines (quiet), stops, hubs, heritage loop, the
            streamside spine and stream walk (proposed paths), the city square idea (a loop stop and a bus stop in the
            same node) and V1; everything cut to the plan frame (FLAG on ink outside)
  SECTIONS  N#-A, N#-B from cached/bergama_sections/cuts.json (Sections v1.6.4+), the first cached scale that fits
  DIAGRAMS  land use of the node frame (Page02's land_use on MapBase data), water over the bed by season (cached levels)
  PLACEHOLDERS V1 perspective, program brief, building proposal (NO DRAWING rule: Aras makes them)
Reads the newest scripts/bergama_basemap_v*, bergama_p02_what_is_there_v*, bergama_sections_v*, bergama_mapbase_v*
(code only), Data/bergama_pages_common.py, section_lines.json, bergama_access_heritage.json and the caches above.
"""
import os, re, glob, json, math, time

NC_VERSION = "v6.2"   # v6.2: own section header (cached title block dropped), scales to 1:3000, land-use columns fit; v6.1: v6.1: cut items from cuts/<name>.json (Sections v1.6.5); v6: sections read from the Sections cache (cuts.json); v5   # v5: the plan context is the shared MapBase (mb_draw), Aras 12:17-12:18 UTC   # v4: brief plan rules (existing vs proposal, V1 viewpoint, program + building placeholders)   # v2: also output/presentation/<slide>.pdf (Aras 14 Nov 11:22 UTC)
ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
PAGE_W, PAGE_H = 420.0, 297.0
NODE_MARGIN_M = 25.0                       # m of town round the node frame on the plan
PLAN_BOX = (14.0, 100.0, 200.0, 264.0)     # mm: x0, y0, x1, y1 of the plan's room
DEN_STEPS = (1000, 1250, 1500, 2000, 2500, 3000, 4000, 5000)
SEC_DENS = (1000, 1500, 2000, 2500, 3000)  # v6.2: Sections v1.6.6 cache scales; the first that fits its room
SEC_ROOMS = ((214.0, 186.0, 406.0, 266.0), (214.0, 100.0, 406.0, 180.0))   # mm: N#-A, N#-B
INK, GREY, RED = "2C2219", "6E675E", "8B2D2D"
SQUARE_C = "C07A2E"                        # the city-square ring (a contrast to the red loop and blue lines; ours)
CUT_C = "2C2219"


def _newest(pat):
    found = glob.glob(os.path.join(ROOT, "scripts", pat))
    if not found:
        raise RuntimeError(u"no scripts/%s in %s: run Bergama.bat once (the kit copies it)" % (pat, ROOT))
    return max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])


def _exec(path, name):
    with open(path, encoding="utf-8") as f:
        code = f.read()
    ns = {"__name__": name}                   # no ghenv here: the script's Grasshopper block does not run
    exec(compile(code, path, "exec"), ns)
    return ns, code


def load_all(node, out_folder, log):
    """P = Page02's code (with B = the Basemap's), X = the Sections code, G = the pages common"""
    pp = _newest("bergama_p02_what_is_there_v*.py")
    P, _ = _exec(pp, "bergama_p02_lib")
    B = P["load_lib"](log)
    cdir = os.path.join(ROOT, "cached", out_folder)
    os.makedirs(cdir, exist_ok=True)
    B["HOUSE_FILE"] = os.path.join(cdir, "osm_houses_node.json")     # its own: the caches are made per frame
    B["STREET_FILE"] = os.path.join(cdir, "streets_node.json")
    log.append(u"page code: %s (%s %s)" % (pp, P.get("GH_LABEL"), P.get("VERSION")))
    xp = _newest("bergama_sections_v*.py")
    X, xcode = _exec(xp, "bergama_sections_lib")
    X["OUT_DIR"] = os.path.join(ROOT, "output", out_folder)
    X["CACHE_DIR"] = cdir
    log.append(u"section code: %s (%s %s)" % (xp, X.get("GH_LABEL"), X.get("VERSION")))
    X["write_pdf_node"] = _writer(X, xcode, log)
    gp = os.path.join(ROOT, "Data", "bergama_pages_common.py")
    G, _ = _exec(gp, "bergama_pages_common")
    G["PC_STATE"]["to_survey"] = B["to_survey"]
    with open(os.path.join(ROOT, "Data", "section_lines.json"), encoding="utf-8") as f:
        SL = json.load(f)
    if node not in SL["nodes"]:
        raise RuntimeError(u"%s is not in Data/section_lines.json" % node)
    D = G["pc_data"](log)
    return P, B, X, G, SL, D


def _writer(X, code, log):
    """the Sections PDF writer (it places the people cutouts), taught two things of the plan: "~" fills (drawn plain:
    this writer has no paper grain) and even-odd rings ("eo", holes stay open)"""
    a = code.index("def write_pdf(")
    b = code.index("\n\n\n", a)
    src = code[a:b].replace("def write_pdf(", "def write_pdf_node(", 1)
    old1 = "rings, fill, stroke, lw, dash, _ly, join, stripes, alpha = it[1:10]"
    old2 = 'A.append("B" if (fill and stroke) else "f" if fill else "S")'
    if old1 not in src or old2 not in src:
        log.append(u"FLAG the Sections writer changed: plan fills with holes may print filled")
        return X["write_pdf"]
    pad = src[:src.index(old1)].rsplit("\n", 1)[1]
    src = src.replace(old1, old1 + "\n" + pad + "eo = stripes == 'eo'\n" + pad +
                      "fill = fill.lstrip('~')[:6] if fill else fill\n" + pad +
                      "alpha = alpha if isinstance(alpha, (int, float)) else None\n" + pad +
                      "dash = dash if isinstance(dash, (list, tuple)) else None", 1)
    src = src.replace(old2, 'A.append(("B*" if eo else "B") if (fill and stroke) else ("f*" if eo else "f") if fill '
                            'else "S")', 1)
    exec(compile(src, "write_pdf_node", "exec"), X)
    return X["write_pdf_node"]


class Cut(object):
    """v6: one cached cut (cached/bergama_sections/cuts.json) with its line ends: what the page needs of it"""

    def __init__(self, name, ab, J, CL):
        self.name, self.J = name, J
        self.A, self.B = tuple(ab[0]), tuple(ab[1])
        self.L = math.hypot(self.B[0] - self.A[0], self.B[1] - self.A[1])
        J = J or {}
        self.z_th, self.window = J.get("z_th", 0.0), tuple(J.get("window") or (0.0, self.L))
        self.levels = {}
        for k_, v in (J.get("levels") or {}).items():
            if u"|" in k_:
                sea, q = k_.split(u"|")
                k_ = (sea, float(q))
            self.levels[k_] = tuple(v)
        self.bld, self.roads, self.trees = J.get("bld", []), J.get("roads", []), J.get("trees", [])
        sc = None
        for a, b in zip(CL[:-1], CL[1:]):                 # where the line crosses the Selinos centreline
            d = (self.B[0] - self.A[0]) * (b[1] - a[1]) - (self.B[1] - self.A[1]) * (b[0] - a[0])
            if abs(d) < 1e-12:
                continue
            t = ((a[0] - self.A[0]) * (b[1] - a[1]) - (a[1] - self.A[1]) * (b[0] - a[0])) / d
            u = ((a[0] - self.A[0]) * (self.B[1] - self.A[1]) - (a[1] - self.A[1]) * (self.B[0] - self.A[0])) / d
            if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0 and (sc is None or t < sc):
                sc = t
        self.s_th = (sc if sc is not None else 0.5) * self.L

    def xy(self, s):
        return (self.A[0] + (self.B[0] - self.A[0]) * s / self.L, self.A[1] + (self.B[1] - self.A[1]) * s / self.L)


# ================================================================ small helpers (page mm)
def T_(s, x, y, size, col=INK, bold=False, align="L", layer="text"):
    return ("text", s, x, y, size, col, bold, align, layer, None, None)


def L_(pts, col, lw, layer, dash=None):
    return ("line", [tuple(p) for p in pts], col, lw, list(dash) if dash else None, layer, 1)


def R_(rings, fill, stroke, lw, layer, eo=False):
    return ("poly", [[tuple(p) for p in r] for r in rings], fill, stroke, lw, None, layer, 1, "eo" if eo else None,
            None)


def ring(cx, cy, r, n=48):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def box(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def wrap(B, s, size, width, bold=False):
    out, ln = [], u""
    for wd in s.split(u" "):
        if ln and B["text_w"](ln + u" " + wd, size, bold) > width:
            out.append(ln)
            ln = wd
        else:
            ln = (ln + u" " + wd).strip()
    if ln:
        out.append(ln)
    return out


def para(B, items, s, x, y, size, width, col=INK, bold=False, step=None, layer="text"):
    for ln in wrap(B, s, size, width, bold):
        items.append(T_(ln, x, y, size, col, bold, "L", layer))
        y -= step or size * 1.4
    return y


def scale_items(items, f, ox, oy, dx, dy):
    """items scaled by f about (ox, oy), then moved by (dx, dy): points, radii, text and image sizes"""
    S = lambda p: (ox + (p[0] - ox) * f + dx, oy + (p[1] - oy) * f + dy)
    out = []
    for it in items:
        t = it[0]
        if t == "poly":
            out.append((t, [[S(p) for p in r] for r in it[1]]) + tuple(it[2:]))
        elif t == "line":
            out.append((t, [S(p) for p in it[1]]) + tuple(it[2:]))
        elif t == "circle":
            q = S((it[1], it[2]))
            out.append((t, q[0], q[1], it[3] * f) + tuple(it[4:]))
        elif t == "text":
            q = S((it[2], it[3]))
            out.append((t, it[1], q[0], q[1], it[4] * f) + tuple(it[5:]))
        elif t == "image":
            q = S((it[1], it[2]))
            out.append((t, q[0], q[1], it[3] * f, it[4] * f) + tuple(it[5:]))
        else:
            out.append(it)
    return out


def scale_north(F, den, xr, y0):
    """north arrow and a scale bar of 50 / 100 / 200 m (the longest under 40 mm), lower right inside the plan"""
    k = 1000.0 / den
    bar = max(b for b in (25.0, 50.0, 100.0, 200.0) if b * k <= 40.0 or b == 25.0)
    Lm = bar * k
    w = Lm + 26.0
    X, Y = xr - w - 3.0, y0 + 3.0
    it = []                                               # transparent: no box behind (Aras 14 Nov 12:10 UTC)
    cx, cy, r = X + 7.0, Y + 7.0, 5.0
    it.append(R_([ring(cx, cy, r, 48)], None, INK, 0.2, "scale_north"))
    nx, ny = F.north()
    tip = (cx + nx * r, cy + ny * r)
    it.append(R_([[tip, (cx - nx * r * 0.55 - ny * r * 0.45, cy - ny * r * 0.55 + nx * r * 0.45), (cx, cy),
                   (cx - nx * r * 0.55 + ny * r * 0.45, cy - ny * r * 0.55 - nx * r * 0.45)]], INK, None, 0.0,
                 "scale_north"))
    it.append(T_(u"N", tip[0] + nx * 1.8 - 0.8, tip[1] + ny * 1.8 - 0.8, 2.2, INK, True, "L", "scale_north"))
    xb, yb = X + 17.0, Y + 4.0
    for i in range(4):
        it.append(R_([box(xb + Lm * i / 4.0, yb, xb + Lm * (i + 1) / 4.0, yb + 1.2)], INK if i % 2 == 0 else "FFFFFF",
                     INK, 0.15, "scale_north"))
    it.append(T_(u"0", xb, yb - 2.8, 2.0, INK, False, "C", "scale_north"))
    it.append(T_(u"%d m" % bar, xb + Lm, yb - 2.8, 2.0, INK, False, "C", "scale_north"))
    it.append(T_(u"1:%d" % den, xb, yb + 3.6, 2.8, INK, True, "L", "scale_north"))
    return it


def clip_plan(B, items, bx, log):
    """plan items cut to the frame bx (page mm): lines and rings cut, texts moved inside or (no room) left out"""
    out, moved, lost = [], 0, []
    for it in items:
        t = it[0]
        if t == "line":
            for run in B["clip_line"](it[1], bx):
                if len(run) >= 2:
                    out.append((t, [tuple(q) for q in run]) + tuple(it[2:]))
        elif t == "poly":
            rr = [R for R in (B["clip_ring"](R_, bx) for R_ in it[1]) if len(R) >= 3]
            if rr:
                out.append((t, [[tuple(q) for q in R] for R in rr]) + tuple(it[2:]))
        elif t == "text":
            w = B["text_w"](it[1], it[4], it[6])
            x = it[2] - {"L": 0.0, "C": w / 2.0, "R": w}.get(it[7], 0.0)
            y = it[3]
            if not (bx[0] - 2.0 <= it[2] <= bx[2] + 2.0 and bx[1] <= y <= bx[3]):
                lost.append(it[1])
                continue
            dx = max(0.0, bx[0] + 0.5 - x) - max(0.0, x + w - (bx[2] - 0.5))
            dy = max(0.0, bx[1] + 0.5 - y) - max(0.0, y + it[4] - (bx[3] - 0.5))
            if dx or dy:
                if w > bx[2] - bx[0] - 1.0:
                    lost.append(it[1])
                    continue
                moved += 1
                it = (t, it[1], it[2] + dx, it[3] + dy) + tuple(it[4:])
            out.append(it)
        else:
            out.append(it)
    log.append(u"plan cut to its frame: %d name(s) moved inside" % moved)
    if lost:
        log.append(u"FLAG plan names outside the frame, left out: %s" % u", ".join(lost[:12]))
    return out


# ================================================================ the plan
def node_frame(B, corners):
    """the node frame on its own axes (long side flat) with NODE_MARGIN_M m round it"""
    F0 = B["Frame"]([tuple(p) for p in corners])
    T = [F0.raw(p) for p in corners]
    u0, u1 = min(q[0] for q in T) - NODE_MARGIN_M, max(q[0] for q in T) + NODE_MARGIN_M
    v0, v1 = min(q[1] for q in T) - NODE_MARGIN_M, max(q[1] for q in T) + NODE_MARGIN_M

    def back(qx, qy):
        return (F0.ca * qx + F0.sa * qy, -F0.sa * qx + F0.ca * qy)
    return B["Frame"]([back(u0, v0), back(u1, v0), back(u1, v1), back(u0, v1)])


def load_mb(log):
    """v5: the library part of the newest MapBase script (mb_load, mb_draw, mb_legend): one base map for every map
    (Aras 14 Nov 12:17-12:18 UTC: "create one map from that (outlines and etc.) and every map should use that")"""
    pth = _newest("bergama_mapbase_v*.py")
    with open(pth, encoding="utf-8") as f:
        code = f.read()
    end = "\n# ================================================================ main\n"
    ns = {"__name__": "bergama_mapbase_lib"}
    exec(compile(code[:code.index(end)], pth, "exec"), ns)
    ns["BERGAMA_ROOT"] = ROOT
    log.append(u"base map: %s (%s %s)" % (pth, ns.get("GH_LABEL"), ns.get("VERSION")))
    return ns


def mb_plan(MB, C, F, T, k, lim, B, P, log):
    """the plan's context from MapBase (its default look, no grain: this writer has none; water hatched) and, for the
    land-use count, the buildings, river and streets in frame m"""
    items = []
    cnt = MB["mb_draw"](C, items, T, k, lim, None, style={"grain": False})
    riv = [R for R in (B["clip_ring"]([T(p) for p in R_], lim) for R_ in C["polys"].get("river", [])) if len(R) >= 3]
    items += hatch(riv, 1.0, P["WATER_LINE"], 0.08, "water_hatch")
    inF = lambda q: -5.0 <= q[0] <= F.w + 5.0 and -5.0 <= q[1] <= F.h + 5.0
    units = []
    for R, fab_, com, src, nm in C["bld"]:
        Q = [F.local(p) for p in R]
        if len(Q) >= 3 and any(inF(q) for q in Q):
            units.append({"P": Q, "fab": fab_, "com": com, "src": src, "A": abs(P["area"](Q)),
                          "cx": sum(q[0] for q in Q) / len(Q), "cy": sum(q[1] for q in Q) / len(Q)})
    loc = lambda Rs: [(True, Q, 0.0, 0.0) for Q in ([F.local(p) for p in R] for R in Rs) if len(Q) >= 3]
    L = {"river": loc(C["polys"].get("river", [])), "road_net": loc(C["polys"].get("streets", []))}
    lc = dict((k_, [Q for cl, Q, a, b in loc(v)]) for k_, v in (C.get("lc") or {}).items())
    log.append(u"plan context (MapBase): %d buildings in the frame (%s); drawn: %s" % (
        len(units), u", ".join(u"%s %d" % (s_, n_) for s_, n_ in sorted(
            dict((u["src"], sum(1 for v in units if v["src"] == u["src"])) for u in units).items())),
        u", ".join(u"%s %d" % kv for kv in sorted(cnt.items()))))
    return items, cnt, units, L, lc


def hatch(rings, gap, col, lw, layer):
    """45 degree lines every gap mm inside the rings (even-odd), page mm: the textured water"""
    out = []
    if not rings:
        return out
    c, s = math.cos(math.pi / 4), math.sin(math.pi / 4)
    rot = lambda p: (p[0] * c + p[1] * s, -p[0] * s + p[1] * c)
    back = lambda q: (q[0] * c - q[1] * s, q[0] * s + q[1] * c)
    RR = [[rot(p) for p in R] for R in rings]
    vs = [q[1] for R in RR for q in R]
    v = math.floor(min(vs) / gap) * gap + gap / 2.0
    while v < max(vs):
        X = []
        for R in RR:
            for i in range(len(R)):
                a, b = R[i - 1], R[i]
                if (a[1] <= v) != (b[1] <= v):
                    X.append(a[0] + (v - a[1]) * (b[0] - a[0]) / (b[1] - a[1]))
        X.sort()
        for x0, x1 in zip(X[0::2], X[1::2]):
            if x1 - x0 > 0.05:
                out.append(L_([back((x0, v)), back((x1, v))], col, lw, layer))
        v += gap
    return out


# ================================================================ the page
def node_page(cfg, log):
    """cfg: NODE, SLIDE, OUT_FOLDER, NAME, INTRO (each node script's own words)"""
    t0 = time.time()
    node, out_folder = cfg["NODE"], cfg["OUT_FOLDER"]
    out_dir = os.path.join(ROOT, "output", out_folder)
    P, B, X, G, SL, D = load_all(node, out_folder, log)
    nd = SL["nodes"][node]
    F = node_frame(B, nd["corners"])
    pw, ph = PLAN_BOX[2] - PLAN_BOX[0], PLAN_BOX[3] - PLAN_BOX[1]
    den = next((d for d in DEN_STEPS if F.w * 1000.0 / d <= pw and F.h * 1000.0 / d <= ph), DEN_STEPS[-1])
    k = 1000.0 / den
    X0 = PLAN_BOX[0] + (pw - F.w * k) / 2.0
    Y0 = PLAN_BOX[3] - F.h * k
    log.append(u"plan: %s frame %.0f x %.0f m (+%.0f m round it), 1:%d, %.0f x %.0f mm" % (
        node, F.w - 2 * NODE_MARGIN_M, F.h - 2 * NODE_MARGIN_M, NODE_MARGIN_M, den, F.w * k, F.h * k))
    MB = load_mb(log)
    MC = MB["mb_load"](log)
    if MC is None:
        raise RuntimeError(u"MapBase cache missing: press MapBase once (after Basemap), then this node")
    items = [R_([box(X0, Y0, X0 + F.w * k, Y0 + F.h * k)], P["PAPER"], None, 0.0, "map_paper")]
    its_, mb_cnt, units, L, lc = mb_plan(MB, MC, F, lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k), k,
                                         (X0, Y0, X0 + F.w * k, Y0 + F.h * k), B, P, log)
    items += its_
    sec_ids = set()
    pgS = lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k)
    inside = lambda q, m=0.0: X0 + m <= q[0] <= X0 + F.w * k - m and Y0 + m <= q[1] <= Y0 + F.h * k - m
    bxF = (0.0, 0.0, F.w, F.h)

    def sline(pts, col, lw, layer, dash=None):
        for run in B["clip_line"]([F.local(p) for p in pts], bxF):
            if len(run) >= 2:
                items.append(L_([(X0 + q[0] * k, Y0 + q[1] * k) for q in run], col, lw, layer, dash))
    # node frame
    sline(nd["corners"] + [nd["corners"][0]], INK, 0.35, "node_frame", (3.0, 1.0, 0.6, 1.0))

    # ---- sections first (their windows go on the plan). v6 (Aras 12:38 UTC "don't ever do the same job twice ...
    # cache it and make it usable by the next script"): read from the Sections cache, never rebuilt here
    E = X["load_engine"](log)                             # only its text widths (the writer centres text with them)
    X["_ENGINE_W"][:] = [E["text_w"]]
    CL, cum = X["load_centreline"](log)
    pc = os.path.join(ROOT, "cached", "bergama_sections", "cuts.json")
    if not os.path.isfile(pc):
        raise RuntimeError(u"%s not found: press Sections (v1.6.4 or newer) first, then this node" % pc)
    with open(pc, encoding="utf-8") as f:
        CJ = json.load(f)
    log.append(u"sections: %s (Sections %s, run %s)" % (pc, CJ.get("version"), CJ.get("run")))
    for nm in (node + u"-A", node + u"-B"):              # v6.1: Sections v1.6.5 keeps items in cuts/<name>.json
        j_ = CJ["cuts"].get(nm)
        if j_ and "items" not in j_ and j_.get("items_file"):
            with open(os.path.join(os.path.dirname(pc), j_["items_file"]), encoding="utf-8") as f:
                j_["items"] = json.load(f)
    cuts = [Cut(nm, SL["lines"][nm], CJ["cuts"].get(nm), CL) for nm in (node + u"-A", node + u"-B")]
    done = []
    for C, room in zip(cuts, SEC_ROOMS):
        x0, y0, x1, y1 = room
        if C.J is None:
            items.append(T_(u"FLAG: section %s is not in the Sections cache" % C.name, x0, y1 - 12.0, 2.6, RED))
            sec_ids.add(id(items[-1]))
            log.append(u"FLAG section %s not in %s: press Sections again" % (C.name, pc))
            continue
        # v6.2 (run 3: 8 of 12 cuts shrunk, mostly by the cached 13 mm title block): the cached title, scale and
        # subtitle are left out and the page prints one header line plus the "meets" line; the drawing gets the rest
        top_y = y1 - 10.0
        for den_s in SEC_DENS:                        # the first cached scale that fits the room
            e_ = C.J["items"].get(str(den_s))
            if not e_:
                continue
            body = [it for it in e_["items"] if not (it[0] == "text" and it[8] == "title" and it[3] > -15.0)]
            bb = list(e_["bbox"])
            bb[3] = max([p_[1] for it in body if it[0] == "poly" for r in it[1] for p_ in r] +
                        [p_[1] for it in body if it[0] == "line" for p_ in it[1]] +
                        [it[3] + it[4] for it in body if it[0] == "text"] +
                        [it[2] + it[3] for it in body if it[0] == "circle"])
            w, h = bb[2] - bb[0], bb[3] - bb[1]
            f = min(1.0, (x1 - x0) / w, (top_y - y0) / h)
            if f >= 0.999:
                break
        items.append(T_(u"SECTION %s" % C.name, x0, y1 - 4.5, 4.5, INK, True, "L", "sections"))
        sub = next((it[1] for it in e_["items"] if it[0] == "text" and it[1].startswith(u"both banks")), u"")
        items.append(T_(u"1:%d%s · %s" % (den_s if f >= 0.999 else den_s / f,
                                          u"" if f >= 0.999 else u" (shrunk, approx.)", sub),
                        x0 + 42.0, y1 - 4.5, 2.4, GREY, False, "L", "sections"))
        sec_ids.update(id(it) for it in items[-2:])
        its = scale_items(body, f, bb[0], bb[3], x0 - bb[0], top_y - bb[3])
        items += its
        sec_ids.update(id(it) for it in its)
        log.append(u"section %s: %.0f x %.0f mm at 1:%d (cached)" % (C.name, w * f, h * f, den_s))
        if f < 0.999:
            log.append(u"FLAG section %s too large even at 1:%d: shrunk x%.2f, its printed scale is wrong" % (
                C.name, den_s, f))
        done.append(C)
        nb = sum(1 for t in C.bld if t.get("cut"))
        items.append(T_(u"meets: %d building(s) cut, %d behind; %d road(s); %d survey tree(s); bed +%.2f m" % (
            nb, len(C.bld) - nb, len(C.roads), len(C.trees), C.z_th), x0, y1 - 8.0, 2.0, GREY, False, "L",
            "sections"))
        sec_ids.add(id(items[-1]))
        log += [u"%s: %s" % (C.name, n_) for n_ in C.J.get("notes", []) if n_.startswith(u"FLAG")]

    # ---- section lines on the plan: the whole line thin, the drawn window bold, names at both ends
    ends = []
    for C in cuts:
        sline([C.A, C.B], CUT_C, 0.25, "section_lines", (2.0, 0.8))
        if C in done:
            s0, s1 = C.window
            sline([C.xy(s0), C.xy(s1)], CUT_C, 0.7, "section_lines")
        for e_ in (C.A, C.B):
            q = pgS(e_)
            near = next((m for m in ends if G["pc_dist"](m[0], q) < 6.0), None)
            if near is not None:                          # v4.1 (run 1, N1: A and B drawn on top of each other)
                near[1].append(C.name)
                continue
            ends.append((q, [C.name]))
            if inside(q, 2.0):
                items.append(R_([ring(q[0], q[1], 2.6, 24)], "FFFFFF", CUT_C, 0.3, "section_names"))
                items.append(T_(C.name[-1], q[0], q[1] - 1.0, 2.8, CUT_C, True, "C", "section_names"))

    for q, nms in ends:
        if inside(q, 2.0):
            if len(nms) > 1:
                items.append(R_([ring(q[0], q[1], 2.6, 24)], "FFFFFF", CUT_C, 0.3, "section_names"))
                items.append(T_(u"/".join(n[-1] for n in nms), q[0], q[1] - 1.0, 2.4, CUT_C, True, "C",
                                "section_names"))
            items.append(T_(u" / ".join(nms), q[0] + 3.2, q[1] + 1.6, 2.2, CUT_C, True, "L", "section_names"))

    # ---- transit and heritage over the plan (PageTransit / PageHeritage data and colours)
    K = D["key"]
    for g in K["line_order"]:
        col, lw, dash = K["lines"][g]
        for ref, r in D["routes"].items():
            if G["pc_group_of"](D, ref) != g:
                continue
            for wid in r["ways"]:
                P_ = D["ways"].get(wid)
                if P_:
                    sline(P_, P["mixh"](col, P["PAPER"], 0.55), lw * 0.45, "bus_lines", dash)   # v4.4: quiet
    stops = [(nm, xy, ln) for nm, xy, ln in G["pc_stop_groups"](D)]
    stops_in = []
    for nm, xy, ln in stops:
        q = pgS(xy)
        if inside(q):
            stops_in.append((nm, xy, ln))
            items.append(R_([ring(q[0], q[1], 1.2, 20)], "FFFFFF", INK, 0.35, "bus_stops"))
            items.append(T_(u"%s · %s" % (nm, u" ".join(sorted(ln, key=lambda r: (len(r), r)))), q[0] + 1.8, q[1] - 2.8,
                            2.2, INK, False, "L", "bus_stops"))
    H = sorted(D["heritage"], key=lambda h: int(h["n"]))
    # v4.4 (Aras 12:15 UTC "public transport lines should be less appearant compared to our proposed path"): the
    # proposed paths lead: the streamside spine K4 -> K5 and the stream walk (loop 3 -> 4) along the Selinos, strong
    sp = G["pc_selinos"](D["hubs"]["K4"], D["hubs"]["K5"])
    if sp:
        sline(sp, "FFFFFF", 2.2, "proposed_path")
        sline(sp, SQUARE_C, 1.4, "proposed_path")
    for a, b in zip(H, H[1:]):
        sw = G["pc_selinos"](a["xy"], b["xy"]) if (a["key"], b["key"]) == ("tabak_koprusu", "ulucami_onu") else None
        if sw:
            sline(sw, RED, 0.9, "heritage_loop")
        else:
            sline([a["xy"], b["xy"]], RED, 0.35, "heritage_loop", (0.01, 0.9))   # v4.1: dotted, legs are straight
    her_in = []
    for h in H:
        q = pgS(h["xy"])
        if inside(q):
            her_in.append(h)
            items.append(R_([ring(q[0], q[1], K["heritage_r"], 32)], RED, "FFFFFF", 0.35, "heritage_loop"))
            items.append(T_(h["n"], q[0], q[1] - 1.0, 2.8, "FFFFFF", True, "C", "heritage_loop"))
            items.append(T_(h["name"], q[0] + K["heritage_r"] + 1.0, q[1] + 1.2, 2.4, RED, True, "L", "heritage_loop"))
    for d_ in D.get("heritage_dots", []):
        q = pgS(d_["xy"])
        if inside(q):
            items.append(R_([ring(q[0], q[1], 0.9, 16)], RED, None, 0.0, "heritage_loop"))
            items.append(T_(d_["name"], q[0] + 1.4, q[1] + 0.8, 2.0, RED, False, "L", "heritage_loop"))
    for code, xy in D["hubs"].items():
        q = pgS(xy)
        if inside(q):
            hc = "T" if code in ("IST", "RED") else code
            col = K["hub"][D["hub_kind"][hc]]
            items.append(R_([box(q[0] - 2.3, q[1] - 2.3, q[0] + 2.3, q[1] + 2.3)], col, "FFFFFF", 0.3, "hubs"))
            items.append(T_(hc, q[0], q[1] - 0.9, 2.4, "FFFFFF", True, "C", "hubs"))

    # ---- the city square (Aras's idea): a heritage loop stop and a bus stop both in the node frame
    sq = None
    framed = lambda xy: P["pip"](xy[0], xy[1], nd["corners"])
    hs = [h for h in H if framed(h["xy"])]
    ss = [s for s in stops if framed(s[1])]
    if hs and ss:
        d_, h, s = min((G["pc_dist"](h["xy"], s[1]), h, s) for h in hs for s in ss)
        mid = ((h["xy"][0] + s[1][0]) / 2.0, (h["xy"][1] + s[1][1]) / 2.0)
        r_m = d_ / 2.0 + 20.0
        q = pgS(mid)
        items.append(("poly", [ring(q[0], q[1], r_m * k, 64)], None, SQUARE_C, 0.6, [2.0, 1.0], "city_square", 1,
                      None, None))
        qa, qb = pgS(h["xy"]), pgS(s[1])
        items.append(L_([qa, qb], SQUARE_C, 0.4, "city_square", (0.01, 0.9)))
        items.append(T_(u"CITY SQUARE (idea)", q[0], q[1] + r_m * k + 1.5, 2.6, SQUARE_C, True, "C", "city_square"))
        sq = (h, s, d_)
        log.append(u"city square: loop stop %s %s and bus stop %s are %.0f m apart (straight line)" % (
            h["n"], h["name"], s[0], d_))
    else:
        log.append(u"city square: not in %s (%s)" % (node, u"no heritage loop stop in the frame" if not hs else
                                                     u"no bus stop in the frame"))
    # ---- V1, the viewpoint of the perspective (brief: viewpoints marked on each node plan; place assumed): from the
    # city square, else from the bank end of the drawn part of section A, looking to the stream bed of the nearest cut
    vp = None
    if done:
        if sq:
            c0 = ((sq[0]["xy"][0] + sq[1][1][0]) / 2.0, (sq[0]["xy"][1] + sq[1][1][1]) / 2.0)
            Cn = min(done, key=lambda C: G["pc_dist"](C.xy(C.s_th), c0))
        else:
            Cn = done[0]
            c0 = Cn.xy(Cn.window[0])
        vp = (c0, Cn.xy(Cn.s_th))
        qa, qb = pgS(vp[0]), pgS(vp[1])
        ang = math.atan2(qb[1] - qa[1], qb[0] - qa[0])
        for da in (-0.35, 0.35):
            items.append(L_([qa, (qa[0] + 9.0 * math.cos(ang + da), qa[1] + 9.0 * math.sin(ang + da))], SQUARE_C, 0.35,
                            "viewpoints"))
        items.append(R_([ring(qa[0], qa[1], 2.0, 24)], SQUARE_C, "FFFFFF", 0.3, "viewpoints"))
        items.append(T_(u"V1", qa[0], qa[1] - 0.8, 2.2, "FFFFFF", True, "C", "viewpoints"))
        log.append(u"V1 viewpoint (assumed): %s, looking to the bed of %s" % (
            u"the city square" if sq else u"the bank end of %s" % Cn.name, Cn.name))
    # v4.3 (Aras 12:14 UTC "drawings do flows outside of it"): every plan item cut to the plan frame
    items = clip_plan(B, [it for it in items if id(it) not in sec_ids], (X0, Y0, X0 + F.w * k, Y0 + F.h * k), log) + \
        [it for it in items if id(it) in sec_ids]
    G["pc_frame_check"]([it for it in items if id(it) not in sec_ids], (X0, Y0, X0 + F.w * k, Y0 + F.h * k), log,
                        lambda t, z, b_: B["text_w"](t, z, b_))
    items.append(L_([(X0, Y0), (X0 + F.w * k, Y0), (X0 + F.w * k, Y0 + F.h * k), (X0, Y0 + F.h * k), (X0, Y0)], INK,
                    0.25, "map_frame"))
    items += scale_north(F, den, X0 + F.w * k, Y0)

    # ---- key under the plan
    ky = Y0 - 5.0
    items.append(T_(u"Plan · %s %s · EXISTING today, orange = PROPOSAL marks · 1:%d" % (node, nd["name"], den), PLAN_BOX[0], ky, 2.8, INK, True))
    ky -= 5.0
    shown = set(u["fab"] for u in units)
    if P.get("FAB_COM"):                                  # v4.5: Page02 v2.3+ two swatches: plain, ground-floor shops
        rows1 = [("hdr", None, u"EXISTING: BUILDINGS · URBAN FABRIC (right swatch: ground floor shops, OSM)")] + \
            [("box2", (P["FAB"][f_], P["FAB_COM"][f_]), P["FAB_WORDS"][f_]) for f_ in P["FAB_ORDER"] if f_ in shown]
    else:
        rows1 = [("hdr", None, u"EXISTING: BUILDINGS · URBAN FABRIC")] + [("box", P["FAB"][f_], P["FAB_WORDS"][f_])
                                                                for f_ in P["FAB_ORDER"] if f_ in shown]
    rows2 = [("hdr", None, u"EXISTING: MOVEMENT AND HERITAGE"),
             ("line", P["mixh"](K["lines"]["town"][0], P["PAPER"], 0.55), u"bus lines, quiet (OSM, ESHOT)"),
             ("disc", INK, u"bus stop with its lines (OSM)"),
             ("disc", RED, u"heritage loop stop, loop order (PageHeritage)"),
             ("box", K["hub"]["walk"], u"hub tile (K4, K3, T, K5, K6 as PageTransit)"),
             ("line", CUT_C, u"section line N#-A / N#-B; bold = the part drawn"),
             ("box", P["WATER_C"], u"the Selinos"),
             ("hdr", None, u"PROPOSAL MARKS"),
             ("line", SQUARE_C, u"city square idea: loop meets transit (place not designed)"),
             ("line", SQUARE_C, u"streamside spine K4 - K5 along the Selinos (proposed path)"),
             ("line", RED, u"stream walk of the heritage loop, Tabak Köprüsü - Ulucami Önü"),
             ("disc", SQUARE_C, u"V1 viewpoint of the perspective (place assumed)")]
    rows1 += [("hdr", None, u"EXISTING: GROUND AND GREEN (MapBase)")] + MB["mb_legend"](MC, mb_cnt, {"grain": False})
    cw = (PLAN_BOX[2] - PLAN_BOX[0]) / 2.0
    yk1 = P["draw_rows"](B, items, rows1, PLAN_BOX[0], ky, cw - 3.0, step=3.0, ts=2.1)
    yk2 = P["draw_rows"](B, items, rows2, PLAN_BOX[0] + cw, ky, cw - 3.0, step=3.4, ts=2.3)

    # ---- land use of the node frame (Page02's count, 1 m cells, on the node frame's own box)
    fq = [F.local(p) for p in nd["corners"]]
    fbox = (min(q[0] for q in fq), min(q[1] for q in fq), max(q[0] for q in fq), max(q[1] for q in fq))
    su = [u for u in units if fbox[0] <= u["cx"] <= fbox[2] and fbox[1] <= u["cy"] <= fbox[3]]
    lu, tot = P["land_use"](su, L, lc, fbox, log)
    ly = min(yk1, yk2) - 3.0
    items.append(T_(u"LAND USE OF THE NODE FRAME · %.1f ha, 1 m cells (calculated)" % (tot / 1e4), PLAN_BOX[0], ly,
                    2.8, INK, True, "L", "diagrams"))
    bar_y, bar_h, bw = ly - 7.0, 4.0, PLAN_BOX[2] - PLAN_BOX[0]
    xx = PLAN_BOX[0]
    keep = [r_ for r_ in lu if r_[2] > 0]
    for lab, col, a_ in keep:
        w_ = bw * a_ / tot
        items.append(R_([box(xx, bar_y, xx + w_, bar_y + bar_h)], col, "FFFFFF", 0.15, "diagrams"))
        xx += w_
    rows = [("box", col, u"%s %s" % (lab, (u"%.0f%%" % (100.0 * a_ / tot)) if 100.0 * a_ / tot >= 0.5 else u"< 1%"))
            for lab, col, a_ in keep]
    # v6.2 (run 3, N2: rows ran into the credit line): as many columns as it takes to stay above y 10 mm
    per = max(1, int((bar_y - 5.0 - 10.0) / 3.0) + 1)
    nc = max(3, -(-len(rows) // per))
    if nc > 5:
        log.append(u"FLAG land use: %d rows need %d columns; rows below y 10 mm cut" % (len(rows), nc))
        nc = 5
    third = -(-len(rows) // nc)
    for ci in range(nc):
        P["draw_rows"](B, items, rows[ci * third:(ci + 1) * third][:per], PLAN_BOX[0] + ci * bw / nc, bar_y - 5.0,
                       bw / nc - 3.0, step=3.0, ts=2.1)

    # ---- water depth over the bed by season, both cuts (the Sections code's levels)
    dx0, dy1 = 214.0, 94.0
    items.append(T_(u"WATER OVER THE BED, BY SEASON", dx0, dy1 - 3.0, 2.8, INK, True, "L", "diagrams"))
    items.append(T_(u"m above the lowest bed point of each cut; Manning n 0.050 (calculated)", dx0, dy1 - 6.8, 2.0,
                    GREY, False, "L", "diagrams"))
    SW = X["SEASON_WATER"]
    rows_w = []
    for sea in X["SEASONS_ORDER"]:
        for Q, fill, lab in SW[sea]:
            rows_w.append((u"%s · %s m3/s" % (sea, (u"%.3g" % Q)), (sea, Q)))
    rows_w += [(u"Q100 · %.1f m3/s (DSI)" % X["Q100"], "q100"), (u"Q500 · %.1f m3/s (DSI)" % X["Q500"], "q500")]
    dep = {}
    for C in done:
        for lab, key in rows_w:
            lv = C.levels.get(key)
            if lv:
                dep[(C.name, key)] = lv[0] - C.z_th
    dmax = max(list(dep.values()) + [1.0])
    yy = dy1 - 12.0
    cA, cB = "5C7A86", "A2B6B5"
    for lab, key in rows_w:
        items.append(T_(lab, dx0, yy - 0.6, 2.0, INK, False, "L", "diagrams"))
        for j, (C, col) in enumerate(zip(done, (cA, cB))):
            v = dep.get((C.name, key))
            yb = yy - 2.6 - j * 2.6
            if v is None:
                items.append(T_(u"no level", dx0 + 34.0, yb, 1.8, GREY, False, "L", "diagrams"))
                continue
            w_ = 44.0 * max(v, 0.0) / dmax
            items.append(R_([box(dx0 + 34.0, yb, dx0 + 34.0 + w_, yb + 2.0)], col, None, 0.0, "diagrams"))
            items.append(T_(u"%.2f" % v, dx0 + 35.0 + w_, yb + 0.3, 1.8, INK, False, "L", "diagrams"))
        yy -= 3.0 + 2.6 * max(1, len(done))
    for j, (C, col) in enumerate(zip(done, (cA, cB))):
        items.append(R_([box(dx0 + j * 30.0, 15.0, dx0 + j * 30.0 + 4.0, 17.0)], col, None, 0.0, "diagrams"))
        items.append(T_(C.name, dx0 + j * 30.0 + 5.5, 15.3, 2.2, INK, False, "L", "diagrams"))
    items.append(T_(u"summer: no flow figure; the held strip 4.0 x 0.30 m is the design's", dx0, 11.5, 1.8, GREY,
                    False, "L", "diagrams"))

    # ---- placeholders (NO DRAWING rule; brief: perspective, program brief, building proposal per node)
    def holder(x0, y0, x1, y1, title, sub, layer):
        items.append(R_([box(x0, y0, x1, y1)], "F1EFEA", GREY, 0.3, layer))
        items.append(L_([(x0, y0), (x1, y1)], "C9C5BC", 0.2, layer))
        items.append(L_([(x0, y1), (x1, y0)], "C9C5BC", 0.2, layer))
        hw = min(30.0, (x1 - x0) / 2.0 - 2.0)                 # v4.1: the label band stays inside its box
        items.append(R_([box((x0 + x1) / 2.0 - hw, (y0 + y1) / 2.0 - 5.0, (x0 + x1) / 2.0 + hw,
                             (y0 + y1) / 2.0 + 6.5)], "F1EFEA", None, 0.0, layer))
        items.append(T_(title, (x0 + x1) / 2.0, (y0 + y1) / 2.0 + 2.0, 2.8, INK, True, "C", layer))
        yy_ = (y0 + y1) / 2.0 - 2.0
        for ln in wrap(B, sub, 2.0, min(58.0, x1 - x0 - 4.0)):
            items.append(T_(ln, (x0 + x1) / 2.0, yy_, 2.0, GREY, False, "C", layer))
            yy_ -= 2.6
    holder(310.0, 60.0, 406.0, 94.0, u"V1 · PERSPECTIVE · %s" % node,
           u"placeholder: Aras's render (Archicad, Unreal 5) from V1 on the plan", "placeholder_perspective")
    holder(310.0, 22.0, 356.0, 56.0, u"PROGRAM BRIEF", u"placeholder: what happens here, for whom, in which season",
           "placeholder_program")
    holder(360.0, 22.0, 406.0, 56.0, u"BUILDING PROPOSAL", u"placeholder: plan, section, elevation (if the node has one)",
           "placeholder_building")
    if sq:
        h, s, d_ = sq
        para(B, items, u"City square idea: loop stop %s %s and bus stop %s (%s) %.0f m apart, straight line." % (
            h["n"], h["name"], s[0], u" ".join(sorted(s[2], key=lambda r: (len(r), r))), d_), 310.0, 18.5, 2.0, 96.0,
            SQUARE_C, True, 2.7, "diagrams")
    else:
        para(B, items, u"No heritage loop stop and bus stop share this node: no city square here.", 310.0, 18.5, 2.0,
             96.0, GREY, False, 2.7, "diagrams")

    # ---- title band and credit
    items.append(T_(u"C  NODES IN DETAIL · SLIDE %d" % cfg["SLIDE"], 14.0, 288.0, 2.6, INK, True))
    items.append(T_(u"%s · %s" % (node, nd["name"]), 14.0, 278.5, 7.5, INK, True))
    para(B, items, cfg["INTRO"], 214.0, 288.0, 2.6, 192.0, INK, False, 3.6, "title")
    items.append(T_(u"Sources: survey Bergama_Altlik.3dm; node frames and section lines Data/section_lines.json (11 Nov); "
                    u"OpenStreetMap 28 Jul 2026 (ODbL); ESHOT; ESA WorldCover 2021; flows DSI and gauges as the Sections "
                    u"script. Distances straight line, calculated.", 14.0, 6.0, 1.8, GREY, False, "L", "credit"))

    bb = X["items_bbox"](items)                           # anything past the sheet edge: FLAG (Aras 11:26 UTC)
    if bb[0] < -0.5 or bb[1] < -0.5 or bb[2] > PAGE_W + 0.5 or bb[3] > PAGE_H + 0.5:
        log.append(u"FLAG drawing runs past the page: ink from x %.0f to %.0f, y %.0f to %.0f mm (page %.0f x %.0f)" % (
            bb[0], bb[2], bb[1], bb[3], PAGE_W, PAGE_H))
    os.makedirs(out_dir, exist_ok=True)
    pdf = X["write_pdf_node"](os.path.join(out_dir, cfg["NAME"] + u".pdf"), [(PAGE_W, PAGE_H, items)],
                              u"Slide %d, %s %s" % (cfg["SLIDE"], node, nd["name"]))
    log.append(u"%s  %s" % (pdf, time.strftime("%H:%M:%S")))
    G["pc_present"](pdf, cfg["SLIDE"], log)
    G["pc_review"](pdf, os.path.join(out_dir, "review"), log)     # v3: the shared standard (pages_common v3)
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s, %d of 2 section(s), %d FLAG line(s), %.1f s" % (u"\n".join(log), node, len(done), len(flags),
                                                                    time.time() - t0)
