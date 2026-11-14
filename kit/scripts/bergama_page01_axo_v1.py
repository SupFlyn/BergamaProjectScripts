# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE01 AXO v1 (14 Nov 2026), slide 1 (analysis): heights and urban fabric as one axonometric.

What Aras asked (14 Nov 2026 12:33 UTC): "we need to improve axo drawing for slide 1 from booklet_son the colour coding
implementing the urban fabric colour coding ... industrial drawings and houses should respect their real life heights
... axonometric should have the correct info from urban fabric. also the houses locations should be had from the
basemap"; 12:38 UTC: "use same basemap ... don't ever redraw anything ... if one scripts does that job cache it".

What it draws: every building of MapBase (v1.2 cache, survey + OSM + 2023 satellite outlines, as the plans) inside the
study area plus MAP_MARGIN_M, extruded to its height, in the urban fabric colours of MapBase / Page02 (FAB, shops
FAB_COM); the ground is MapBase's own plan (streets, water, green) laid flat under them. Nothing is redrawn here: the
outlines, the fabric types and the floors all come from cached/bergama_mapbase/mapbase.json.
Heights = floors x storey height. Floors: the survey's floor count (YAZI_KAT_ADEDI), else OSM building:levels (MapBase
"bld_x"); where neither is recorded the building is drawn ONE storey high in a paler shade and counted apart. Storey
heights (site board selinus_board v67 FLOOR_H / STOREY, settled 12 Nov): 3.0 m; civic 3.5 m; industrial 4.5 m (OSM
industrial building tags or inside an OSM industrial zone); mosques and sacred 5.0 m. Ground flat (no terrain).
Projection: orthographic axonometric, viewed from compass bearing view_from at tilt degrees above the horizon; lengths
along the sheet's horizontal are true to the scale, depths x sin(tilt), heights x cos(tilt).

Outputs (Downloads/Bergama/output/bergama_page01_axo/): HeightsAxo.pdf, HeightsAxo.svg, review/ PNGs.
Reads: Data/bergama_pages_common.py (v3.4+), the newest scripts/bergama_mapbase_v*.py and its cache (press MapBase v1.2
first). Grasshopper: a Button on any input runs it; inputs scale (1:2,500), view_from (225 = from the south-west),
tilt (35).
"""
import os, time, math

VERSION = "v1"
GH_LABEL = "Page01Axo"
OUT_FOLDER = "bergama_page01_axo"
LOG_NAME = "bergama_page01_axo_log.txt"
GH_INPUTS = {"scale": "int 1000..10000 = 2500", "view_from": "int 0..359 = 225", "tilt": "int 20..60 = 35"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "HeightsAxo"
MAP_MARGIN_M = 100.0               # m round the study area's rectangle (ours: a block of context each side)
FLOOR_H = 3.0                      # m per storey (selinus_board v67 FLOOR_H)
STOREY = {"sacred": 5.0, "civic": 3.5, "industrial": 4.5}   # m (selinus_board v67 STOREY)
INDUSTRIAL = ("industrial", "warehouse", "factory", "hangar", "manufacture")
UNKNOWN_PALE = 0.55                # a building with no floor count: its colour mixed this far toward the paper
WALL_DARK = (0.18, 0.42)           # wall shade toward the ink: lit side, shadow side
MIN_BOX_H = 215.0                  # mm: the drawing area at least this tall (the legend column fits beside it)


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


class Sheet(object):
    """what pc_sheet / pc_write need: box (the drawing area, page mm), w, h, den, k"""
    def __init__(self, box, den, side):
        self.box, self.den, self.k = box, float(den), 1000.0 / den
        self.w, self.h = box[2] + 8.0 + side + 12.0, box[3] + 12.0


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    K = G["pc_data"](log)["key"]
    MB = G["pc_mb_lib"](log)
    if MB is None:
        raise RuntimeError(u"no MapBase script: run Bergama.bat once")
    C = MB["mb_load"](log)
    if C is None:
        raise RuntimeError(u"no MapBase cache: press MapBase once, then this")
    X = C.get("bld_x")
    if not X or len(X) != len(C["bld"]):
        log.append(u"FLAG: the MapBase cache has no floors (made by %s): press MapBase v1.2+ again; every building is "
                   u"drawn one storey" % C.get("version"))
        X = [[0, u"", u""] for _ in C["bld"]]
    den = int(globals().get("scale") or 2500)
    vf = float(globals().get("view_from") or 225)
    tilt = math.radians(float(globals().get("tilt") or 35))
    k = 1000.0 / den
    mix, PAPER, INK = MB["mixh"], MB["PAPER"], MB["INK"]

    # ---- the frame: the study area's smallest rectangle + MAP_MARGIN_M
    cal = [q for R in (C.get("calisma") or []) for q in R] or [q for R in C["extent"] for q in R]
    ang = MB["min_rect"](cal)[1]
    ca, sa = math.cos(ang), math.sin(ang)
    us = [q[0] * ca + q[1] * sa for q in cal]
    vs = [-q[0] * sa + q[1] * ca for q in cal]
    u0, u1, v0, v1 = min(us) - MAP_MARGIN_M, max(us) + MAP_MARGIN_M, min(vs) - MAP_MARGIN_M, max(vs) + MAP_MARGIN_M
    rect = [(u * ca - v * sa, u * sa + v * ca) for u, v in ((u0, v0), (u1, v0), (u1, v1), (u0, v1))]
    inrect = lambda q: u0 <= q[0] * ca + q[1] * sa <= u1 and v0 <= -q[0] * sa + q[1] * ca <= v1
    log.append(u"frame: the study area's rectangle + %.0f m: %.0f x %.0f m" % (MAP_MARGIN_M, u1 - u0, v1 - v0))

    # ---- the projection: plan turned so the view runs up the sheet, then tilted
    th = math.radians(vf + 180.0)                    # compass bearing of the view direction
    ct, st_ = math.cos(th), math.sin(th)
    cx0, cy0 = sum(q[0] for q in rect) / 4.0, sum(q[1] for q in rect) / 4.0
    rot = lambda q: ((q[0] - cx0) * ct - (q[1] - cy0) * st_, (q[0] - cx0) * st_ + (q[1] - cy0) * ct)
    sE, cE = math.sin(tilt), math.cos(tilt)

    def P(q, z=0.0):
        a, b = rot(q)
        return (a * k, (b * sE + z * cE) * k)

    # ---- the buildings: height, colour, depth
    ind_zones = [R for R, cl, sub, nm in C["areas"] if cl == "landuse" and sub == "industrial"]
    blds = []
    n_known = 0
    for (R, fab, com, src, nm), (fl, btag, amen) in zip(C["bld"], X):
        if len(R) < 3:
            continue
        cx, cy = sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R)
        if not inrect((cx, cy)):
            continue
        if fab == "sacred":
            sh = STOREY["sacred"]
        elif fab == "large":
            ind = btag in INDUSTRIAL or any(MB["pip"](cx, cy, Z) for Z in ind_zones)
            sh = STOREY["industrial" if ind else "civic"]
        else:
            sh = FLOOR_H
        known = int(fl or 0) > 0
        n_known += known
        col = (MB["FAB_COM"] if com else MB["FAB"]).get(fab, MB["FAB"]["regular"])
        if not known:
            col = mix(col, PAPER, UNKNOWN_PALE)
        blds.append((rot((cx, cy))[1], R, (int(fl) if known else 1) * sh, col, fab, com, known))
    blds.sort(key=lambda b: -b[0])                   # far first (painter's order)
    if not blds:
        raise RuntimeError(u"no MapBase building inside the frame")

    # ---- sheet placement: everything drawn, then shifted onto the page
    pts = [P(q) for q in rect] + [P(q, b[2]) for b in blds for q in b[1]]
    x0, x1 = min(p[0] for p in pts), max(p[0] for p in pts)
    y0, y1 = min(p[1] for p in pts), max(p[1] for p in pts)
    hgt = max(y1 - y0, MIN_BOX_H)
    box = (12.0, 12.0, 12.0 + x1 - x0, 12.0 + hgt)
    dx, dy = box[0] - x0, box[1] + (hgt - (y1 - y0)) / 2.0 - y0
    T = lambda q, z=0.0: (P(q, z)[0] + dx, P(q, z)[1] + dy)
    M = Sheet(box, den, G["PC_SIDE_MM"])
    ground = [T(q) for q in rect]
    gb = (min(p[0] for p in ground), min(p[1] for p in ground), max(p[0] for p in ground), max(p[1] for p in ground))
    items = []
    cnt = MB["mb_draw"](C, items, T, k, gb, G["PC_CLIP"], {"grain": False, "lc_light": 0.55},
                        {"ground", "lc", "veg", "areas", "parks", "streets", "water", "walls", "bridges"})
    log.append(u"ground (MapBase plan, flat): " + u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())))
    items.append(("poly", [ground], None, INK, 0.2, None, "ground_edge", 1, None, None))

    # ---- the blocks: walls facing the viewer (far ones first), then the roof
    n_faces = 0
    for depth, R, h, col, fab, com, known in blds:
        Q = list(R)
        if MB["area"](Q) < 0:
            Q.reverse()                                  # anticlockwise: outward normal = (dy, -dx)
        walls = []
        for i in range(len(Q)):
            a, b = Q[i - 1], Q[i]
            ra, rb = rot(a), rot(b)
            nx, ny = rb[1] - ra[1], -(rb[0] - ra[0])
            ln = math.hypot(nx, ny)
            if ln < 1e-6 or ny >= 0:                     # faces away (the viewer looks up the sheet, +y)
                continue
            t = WALL_DARK[0] + (WALL_DARK[1] - WALL_DARK[0]) * (nx / ln + 1.0) / 2.0
            walls.append(((ra[1] + rb[1]) / 2.0, [T(a), T(b), T(b, h), T(a, h)], mix(col, INK, t)))
        lay = "blocks_" + fab + ("_shops" if com else "") + ("" if known else "_floors_unknown")
        for _d, ring, c_ in sorted(walls, key=lambda w: -w[0]):
            items.append(("poly", [ring], c_, mix(c_, INK, 0.35), 0.03, None, lay, 1, None, None))
            n_faces += 1
        roof = [T(q, h) for q in Q]
        items.append(("poly", [roof], col, mix(col, INK, 0.45), 0.04, None, lay, 1, None, None))
    hs = sorted(b[2] for b in blds)
    log.append(u"buildings: %d drawn (%d walls), %d with a floor count (survey or OSM), %d without (one storey, pale); "
               u"heights %.1f-%.1f m, median %.1f m; by fabric: %s" % (
                   len(blds), n_faces, n_known, len(blds) - n_known, hs[0], hs[-1], hs[len(hs) // 2], u", ".join(
                       u"%s %d" % (MB["FAB_WORDS"][f_], sum(1 for b in blds if b[4] == f_)) for f_ in MB["FAB_ORDER"])))

    # ---- legend
    P_ = G["P_"]

    def sw(col):
        return lambda x, y: [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0), (x + 4.5, y + 2.0), (x - 4.5, y + 2.0)]],
                                col, mix(col, INK, 0.45), 0.1, "legend")]
    legend = [(None, u"EXISTING: URBAN FABRIC (MAPBASE)")]
    for f_ in MB["FAB_ORDER"]:
        n_ = sum(1 for b in blds if b[4] == f_)
        if n_:
            legend.append((sw(MB["FAB"][f_]), u"%s (%d): %s" % (MB["FAB_WORDS"][f_], n_, MB["FAB_RULE"][f_])))
    n_com = sum(1 for b in blds if b[5])
    if n_com:
        legend.append((sw(MB["FAB_COM"]["regular"]), u"Same type with shops, offices or workshops (OSM), brighter (%d)"
                       % n_com))
    legend += [(sw(mix(MB["FAB"]["regular"], PAPER, UNKNOWN_PALE)),
                u"Floors not recorded: drawn one storey, paler (%d)" % (len(blds) - n_known)),
               (None, u"EXISTING: GROUND (MAPBASE PLAN, FLAT)")]
    legend += G["pc_mb_legend"](MB["mb_legend"](C, cnt, {"lc_light": 0.55}), K)
    notes = [u"Height = floors x storey: survey floor counts, else OSM building:levels; storey 3.0 m, civic 3.5 m, "
             u"industrial 4.5 m, mosques 5.0 m (site board values). Ground drawn flat.",
             u"Viewed from %.0f deg (compass), %.0f deg above the horizon. Tallest %.1f m." % (
                 vf, math.degrees(tilt), hs[-1])]
    credit = (u"Sources: survey (Bergama municipality DWG); © OpenStreetMap contributors (ODbL); 2023 satellite image "
              u"check; ESA WorldCover 2021 (CC BY 4.0). Fabric types: MapBase rules (Page02).")
    nv = rot((cx0, cy0 + 100.0))
    north = math.degrees(math.atan2(nv[0], nv[1] * sE))
    items += G["pc_sheet"](M, K, lib, u"Heights and urban fabric", u"Every building at its recorded height, coloured "
                           u"by its fabric type", legend, notes, credit, north=north,
                           bar_note=u"true along the sheet's horizontals only")
    items = [it for it in items if it[6 if it[0] == "poly" else 5 if it[0] == "line" else 8] != "frame"]
    G["pc_write"](lib, M, items, OUT_DIR, NAME, u"Heights and urban fabric, axonometric 1:%d" % den, log,
                  clips={G["PC_CLIP"]: [[ground]]})
    flags = [l for l in log if l.startswith(u"FLAG")]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


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
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to export to " + OUT_DIR)
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
