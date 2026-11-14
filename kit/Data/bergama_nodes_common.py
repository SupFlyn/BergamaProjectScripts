# -*- coding: utf-8 -*-
"""Bergama Group 6: NODES COMMON v1 (14 Nov 2026): the shared parts of the six node page scripts
scripts/bergama_node_n1_v*.py ... bergama_node_n6_v*.py (Panel Review II slides 7-12, one script per node, Aras 14 Nov
11:14 UTC "dont build all those nodes into single script"). Loaded (not pasted) by each node script.

One A3 landscape page per node (420 x 297 mm, PDF with layers + review PNGs):
  PLAN      the node frame (Data/section_lines.json "nodes", his node frames of 11 Nov) + NODE_MARGIN_M round it, on the
            frame's own axes (long side flat), drawn with Page02's code: buildings by urban fabric (survey + OSM/satellite
            houses + 2023 image check), streets, the Selinos, walls; the node's two section lines N#-A, N#-B (the part
            drawn on the section thicker); over it the bus lines, stops, hubs and the heritage loop of
            Data/bergama_access_heritage.json (as PageTransit / PageHeritage), and the CITY SQUARE idea (Aras 14 Nov
            11:14-11:15 UTC: "a city square where heritage and transit hub's cross ... people, tourists can gather and
            move on and will be close to transit"): drawn only where a heritage loop stop and a bus stop both lie in
            the node frame, as a dashed ring round the two (place = an idea, not designed), with their straight-line
            distance (calculated)
  SECTIONS  N#-A and N#-B by the newest scripts/bergama_sections_v*.py (its own cut, ground, water and context code,
            autumn look), 1:SEC_DEN, shrunk only if the cut is taller than its room (the real scale is printed)
  DIAGRAMS  land use of the node frame (Page02's 1 m cell count), water depth over the bed by season at both cuts
            (the Sections script's Manning levels: its SEASON_WATER flows and DSI Q100 / Q500), what each cut meets
  PERSPECTIVE  a labelled placeholder (NO DRAWING rule: Aras renders it)
Reads: newest scripts/bergama_basemap_v*.py, scripts/bergama_p02_what_is_there_v*.py, scripts/bergama_sections_v*.py,
Data/bergama_pages_common.py, Data/section_lines.json, Data/bergama_access_heritage.json, the caches of Basemap
(press Basemap first) and the open Rhino model's survey layers (the Sections code reads them).
"""
import os, re, glob, json, math, time

NC_VERSION = "v3"   # v2: also output/presentation/<slide>.pdf (Aras 14 Nov 11:22 UTC)
ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
PAGE_W, PAGE_H = 420.0, 297.0
NODE_MARGIN_M = 25.0                       # m of town round the node frame on the plan
PLAN_BOX = (14.0, 100.0, 200.0, 264.0)     # mm: x0, y0, x1, y1 of the plan's room
DEN_STEPS = (1000, 1250, 1500, 2000, 2500, 3000, 4000, 5000)
SEC_DEN = 1000                             # sections drawn at 1:1000 (shrunk only if taller than the room)
SEC_HALF_M = 95.0                          # m either side of the stream crossing (190 m fits 192 mm at 1:1000)
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
    X["MAX_LEN_M"] = 2.0 * SEC_HALF_M
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
    w, h = Lm + 26.0, 14.0
    X, Y = xr - w - 3.0, y0 + 3.0
    it = [R_([box(X, Y, X + w, Y + h)], "FFFFFF", None, 0.0, "scale_north")]
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


def plan_units(P, B, F, log):
    """Page02's preparation on the node frame: L (layers in frame m), units (buildings with fabric), lc, O, D"""
    if not os.path.isfile(B["CACHE_FILE"]):
        raise RuntimeError(u"%s not found: press Basemap once first" % B["CACHE_FILE"])
    with open(B["CACHE_FILE"], encoding="utf-8") as f:
        D = json.load(f)
    fl_of = {}
    fls = (D.get("floors") or {}).get("buildings") or []
    j_ = 0
    for cl, Q in D["layers"].get("buildings", []):
        if cl and len(Q) >= 3:
            if j_ < len(fls):
                fl_of[(round(Q[0][0], 2), round(Q[0][1], 2))] = fls[j_]
            j_ += 1
    D["layers"].update(B["osm_houses"](D, F, log))
    D["layers"].update(B["sat_houses"](D, F, log))
    L = B["localise"](D, F)
    B["image_check"](L, F, log)
    B["road_surface"](L, F, log)
    B["town_streets"](L, F, log)
    try:
        B["build_river"](L, F, log)
    except Exception as e:
        L["river"] = []
        log.append(u"FLAG river: not built on the node plan (%s: %s): the stream is its survey lines" % (
            type(e).__name__, e))
    O = P["read_osm"](B, log)
    inF = lambda q: -5.0 <= q[0] <= F.w + 5.0 and -5.0 <= q[1] <= F.h + 5.0
    units = []
    for key in ("buildings", "heritage", "osm_houses", "sat_houses"):
        for cl, Q, a, b in L.get(key, []):
            if not (cl and len(Q) >= 3) or not any(inF(q) for q in Q):
                continue
            A = abs(P["area"](Q))
            if A < 2.0:
                continue
            fl = fl_of.get(P["_survey_key"](F, Q[0]), 0) if key == "buildings" else 0
            units.append({"P": Q, "A": A, "fl": fl, "her": key == "heritage", "src": key})
    names = [(F.local((x, y)), t) for t, x, y, a_, kind in D.get("labels") or [] if kind != "street"]
    for q, t in names:
        for u in units:
            if not u.get("name") and P["pip"](q[0], q[1], u["P"]):
                u["name"] = t
                break
    for x, y, tg in O["nodes"]:
        q = F.local((x, y))
        if inF(q):
            for u in units:
                if not u.get("tags") and P["pip"](q[0], q[1], u["P"]):
                    u["tags"] = tg
                    break
    P["fabric"](units, log)
    lc = {}
    src = os.path.join(ROOT, P["LC_FILE"])
    if os.path.isfile(src):
        with open(src, encoding="utf-8") as f:
            J = json.load(f)
        for k_, rings in (J.get("rings") or {}).items():
            lc[k_] = [R for R in ([F.local(p) for p in R_] for R_ in rings) if len(R) >= 3]
    log.append(u"node plan: %d buildings (%s)" % (len(units), u", ".join(
        u"%s %d" % (s_, sum(1 for u in units if u["src"] == s_)) for s_ in ("buildings", "heritage", "osm_houses",
                                                                            "sat_houses"))))
    return D, L, units, lc, O


def plan_items(P, B, F, L, units, lc, den, X0, Y0, log):
    """Page02's drawing on the node frame (water hatched: this writer has no grain)"""
    items = []
    k = 1000.0 / den
    bx = (0.0, 0.0, F.w, F.h)
    pg = lambda q: (X0 + q[0] * k, Y0 + q[1] * k)

    def poly(rings, fill, layer, eo=True):
        rr = [R for R in (B["clip_ring"](R_, bx) for R_ in rings) if len(R) >= 3]
        if rr:
            items.append(R_([[pg(q) for q in R] for R in rr], fill, None, 0.0, layer, eo))
        return rr

    def line(Q, col, lw, layer, dash=None):
        for run in B["clip_line"](Q, bx):
            if len(run) >= 2:
                items.append(L_([pg(q) for q in run], col, lw, layer, dash))
    items.append(R_([box(X0, Y0, X0 + F.w * k, Y0 + F.h * k)], P["PAPER"], None, 0.0, "map_paper"))
    for k_ in P["LC_ORDER"]:
        for R in lc.get(k_, []):
            poly([R], P["mixh"](P["LC"][k_][0], P["PAPER"], P["LC_LIGHT"]), "landcover_" + k_)
    poly([Q for key in ("road_net", "town_net") for cl, Q, a, b in L.get(key, [])], P["STREET_C"], "streets")
    hair = 0.1
    for key in ("road_edges", "kerbs", "town_edges"):
        for cl, Q, a, b in L.get(key, []):
            line(Q, P["STREET_EDGE"], hair, "street_edges")
    riv = poly([Q for cl, Q, a, b in L.get("river", [])], P["WATER_C"], "water")
    items += hatch([[pg(q) for q in R] for R in riv], 1.0, P["WATER_LINE"], 0.08, "water_hatch")
    for key, w_ in (("stream_banks", 0.2), ("ponds", 0.12)):
        for cl, Q, a, b in L.get(key, []):
            line(Q + ([Q[0]] if cl else []), P["WATER_LINE"], w_, "water")
    for cl, Q, a, b in L.get("walls", []):
        line(Q, P["WALL_C"], hair, "walls")
    for cl, Q, a, b in L.get("heritage_walls", []):
        line(Q, P["HER_WALL"], 0.25, "heritage_walls")
    for u in units:                                       # outlines twice the pen first, fills over them
        rr = B["clip_ring"](u["P"], bx)
        if len(rr) >= 3:
            items.append(L_([pg(q) for q in rr + [rr[0]]], P["mixh"](P["FAB"][u["fab"]], INK, P["P02_EDGE_DARK"]),
                            2 * hair, "buildings_outline"))
    for f_ in P["FAB_ORDER"]:
        rr = [R for R in (B["clip_ring"](u["P"], bx) for u in units if u["fab"] == f_) if len(R) >= 3]
        if rr:
            items.append(R_([[pg(q) for q in R] for R in rr], P["FAB"][f_], None, 0.0, "buildings_" + f_))
    for cl, Q, a, b in L.get("bridges", []):
        line(Q, INK, 0.2, "bridges")
    return items


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
    BD, L, units, lc, O = plan_units(P, B, F, log)
    items = plan_items(P, B, F, L, units, lc, den, X0, Y0, log)
    pgS = lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k)
    inside = lambda q, m=0.0: X0 + m <= q[0] <= X0 + F.w * k - m and Y0 + m <= q[1] <= Y0 + F.h * k - m
    bxF = (0.0, 0.0, F.w, F.h)

    def sline(pts, col, lw, layer, dash=None):
        for run in B["clip_line"]([F.local(p) for p in pts], bxF):
            if len(run) >= 2:
                items.append(L_([(X0 + q[0] * k, Y0 + q[1] * k) for q in run], col, lw, layer, dash))
    # node frame
    sline(nd["corners"] + [nd["corners"][0]], INK, 0.35, "node_frame", (3.0, 1.0, 0.6, 1.0))

    # ---- sections first (their windows go on the plan)
    E = X["load_engine"](log)
    E["_DRY0"] = E["DRY"]
    X["_ENGINE_W"][:] = [E["text_w"]]
    CL, cum = X["load_centreline"](log)
    BM = X["load_basemap"](log)
    names = [node + u"-A", node + u"-B"]
    cuts = []
    for i, nm in enumerate(names):
        a, b = SL["lines"][nm]
        cuts.append(X["Cut"](i + 1, tuple(a), tuple(b), nm, nm))
    pad = max(X["CORRIDOR_STEPS"][-1], X["SLOPE_HALF"] + 20.0) + X["HYD_HALF"]
    xs = [p[0] for C in cuts for p in (C.A, C.B)]
    ys = [p[1] for C in cuts for p in (C.A, C.B)]
    survey = X["read_survey"]((min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad), log)
    done = []
    for C, room in zip(cuts, SEC_ROOMS):
        x0, y0, x1, y1 = room
        items.append(T_(u"Section %s · looking downstream" % C.name, x0, y1 - 3.5, 3.4, INK, True, "L", "sections"))
        try:
            C.survey = survey
            X["build_cut"](C, CL, cum, E, log, BM)
            pg, S_, yb = X["draw_cut"](E, C, X["SEASON"], SEC_DEN, 0.0, 0.0)
            bb = X["items_bbox"](pg.items)
            w, h = bb[2] - bb[0], bb[3] - bb[1]
            f = min(1.0, (x1 - x0) / w, (y1 - y0 - 7.0) / h)
            its = scale_items(pg.items, f, bb[0], bb[3], x0 - bb[0], (y1 - 7.0) - bb[3])
            items += its
            items[-len(its) - 1] = T_(u"Section %s · looking downstream · 1:%d" % (C.name, round(SEC_DEN / f)), x0,
                                      y1 - 3.5, 3.4, INK, True, "L", "sections")
            done.append(C)
            log.append(u"section %s: %.0f x %.0f mm at 1:%d%s" % (C.name, w * f, h * f, round(SEC_DEN / f),
                                                                 u"" if f >= 0.999 else u" (shrunk to fit its room)"))
        except Exception as ex:
            import traceback as _tb
            items.append(T_(u"FLAG: section %s not drawn: %s" % (C.name, ex), x0, y1 - 12.0, 2.6, RED))
            log.append(u"FLAG section %s not drawn: %s: %s | %s" % (C.name, type(ex).__name__, ex, u" / ".join(
                _tb.format_exc()[-400:].splitlines())))
        log += C.notes

    # ---- section lines on the plan: the whole line thin, the drawn window bold, names at both ends
    for C in cuts:
        sline([C.A, C.B], CUT_C, 0.25, "section_lines", (2.0, 0.8))
        if C in done:
            s0, s1 = C.window
            sline([C.xy(s0), C.xy(s1)], CUT_C, 0.7, "section_lines")
        for e_ in (C.A, C.B):
            q = pgS(e_)
            if inside(q, 2.0):
                items.append(R_([ring(q[0], q[1], 2.6, 24)], "FFFFFF", CUT_C, 0.3, "section_names"))
                items.append(T_(C.name[-1], q[0], q[1] - 1.0, 2.8, CUT_C, True, "C", "section_names"))

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
                    sline(P_, col, lw, "bus_lines", dash)
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
    for a, b in zip(H, H[1:]):
        sline([a["xy"], b["xy"]], RED, K["heritage_w"], "heritage_loop")
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
    items.append(L_([(X0, Y0), (X0 + F.w * k, Y0), (X0 + F.w * k, Y0 + F.h * k), (X0, Y0 + F.h * k), (X0, Y0)], INK,
                    0.25, "map_frame"))
    items += scale_north(F, den, X0 + F.w * k, Y0)

    # ---- key under the plan
    ky = Y0 - 5.0
    items.append(T_(u"Plan · %s %s today · 1:%d" % (node, nd["name"], den), PLAN_BOX[0], ky, 2.8, INK, True))
    ky -= 5.0
    shown = set(u["fab"] for u in units)
    rows1 = [("hdr", None, u"BUILDINGS · URBAN FABRIC")] + [("box", P["FAB"][f_], P["FAB_WORDS"][f_])
                                                            for f_ in P["FAB_ORDER"] if f_ in shown]
    rows2 = [("hdr", None, u"MOVEMENT AND HERITAGE"),
             ("line", K["lines"]["town"][0], u"bus lines (OSM; weight = buses a weekday, ESHOT)"),
             ("disc", INK, u"bus stop with its lines (OSM)"),
             ("disc", RED, u"heritage loop stop, loop order (PageHeritage)"),
             ("box", K["hub"]["walk"], u"hub tile (K4, K3, T, K5, K6 as PageTransit)"),
             ("line", SQUARE_C, u"city square idea: loop meets transit (place not designed)"),
             ("line", CUT_C, u"section line; bold = the part drawn"),
             ("box", P["WATER_C"], u"the Selinos")]
    cw = (PLAN_BOX[2] - PLAN_BOX[0]) / 2.0
    yk1 = P["draw_rows"](B, items, rows1, PLAN_BOX[0], ky, cw - 3.0, step=3.4, ts=2.3)
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
    half = (len(rows) + 1) // 2
    P["draw_rows"](B, items, rows[:half], PLAN_BOX[0], bar_y - 5.0, bw / 2.0 - 3.0, step=3.2, ts=2.2)
    P["draw_rows"](B, items, rows[half:], PLAN_BOX[0] + bw / 2.0, bar_y - 5.0, bw / 2.0 - 3.0, step=3.2, ts=2.2)

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

    # ---- perspective placeholder, then what each cut meets and the city square under it
    px0, py0, px1, py1 = 310.0, 40.0, 406.0, 94.0
    items.append(R_([box(px0, py0, px1, py1)], "F1EFEA", GREY, 0.3, "perspective_placeholder"))
    items.append(L_([(px0, py0), (px1, py1)], "C9C5BC", 0.2, "perspective_placeholder"))
    items.append(L_([(px0, py1), (px1, py0)], "C9C5BC", 0.2, "perspective_placeholder"))
    items.append(T_(u"PERSPECTIVE · %s" % node, (px0 + px1) / 2.0, (py0 + py1) / 2.0 + 2.0, 3.2, INK, True, "C",
                    "perspective_placeholder"))
    items.append(T_(u"placeholder: Aras's render (Archicad model, Unreal 5)", (px0 + px1) / 2.0, (py0 + py1) / 2.0 - 3.0,
                    2.2, GREY, False, "C", "perspective_placeholder"))
    ty = 36.0
    items.append(T_(u"WHAT THE CUTS MEET", px0, ty, 2.6, INK, True, "L", "diagrams"))
    ty -= 4.0
    for C in done:
        nb = sum(1 for t in C.bld if t[4])
        nbk = sum(1 for t in C.bld if not t[4])
        ty = para(B, items, u"%s: %d building(s) cut, %d behind; %d road(s); %d survey tree(s); bed +%.2f m" % (
            C.name, nb, nbk, len(C.roads), len(C.trees), C.z_th), px0, ty, 2.0, px1 - px0, INK, False, 2.8, "diagrams")
    ty -= 1.5
    if sq:
        h, s, d_ = sq
        para(B, items, u"City square idea: loop stop %s %s and bus stop %s (%s) %.0f m apart, straight line." % (
            h["n"], h["name"], s[0], u" ".join(sorted(s[2], key=lambda r: (len(r), r))), d_), px0, ty, 2.0, px1 - px0,
            SQUARE_C, True, 2.8, "diagrams")
    else:
        para(B, items, u"No heritage loop stop and bus stop share this node: no city square here.", px0, ty, 2.0,
             px1 - px0, GREY, False, 2.8, "diagrams")

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
