# -*- coding: utf-8 -*-
"""Bergama Group 6: SECTIONS AC v1 (14 Nov 2026): the 12 node sections with the Archicad background and our layer on top.

What Aras asked (14 Nov 2026, 15:43 UTC): "i want the background to be taken from archicad cuz your sections etc. look
really really undetailed and add our sauce on it like ground hatches etc. lets try both"; scripts stay connected.
The Sections page stays as it is (route 1); this is route 2, on the same cuts:
  OUR LAYER   every cut exactly as the Sections script cached it (cached/bergama_sections/cuts/<cut>.json: sky, ground
              behind, the cut ground, walls, water and levels, planting, people, trees, land-use band, labels), read,
              never redrawn; only its own houses ("houses behind", "context buildings") are taken out
  BACKGROUND  the Archicad section of the same line (AcBuild: cached/bergama_archicad/dwg/<cut>.dwg), placed by its two
              registration blocks (s = 0 and s = L, REG_Z), recoloured to the Sections house palette (one graphic
              code), slotted in where the houses were (same drawing order); the Archicad terrain is left out (our
              ground is drawn instead)
A cut without its DWG keeps the Sections houses (FLAG line).
Layout: all cuts on ONE A3 landscape (Aras 14 Nov 15:25-15:27 UTC), the largest common cached scale that fits.

Reads  ~/Downloads/Bergama/cached/bergama_sections/cuts.json + cuts/, cached/bergama_archicad/acbuild.json + dwg/,
       scripts/bergama_sections_v*.py (newest, as a library: page writer, palette), Data/bergama_pages_common.py
Writes ~/Downloads/Bergama/output/bergama_sections_ac/SectionsAC.pdf + review/ PNGs, logs/bergama_sections_ac_log.txt
Run in Rhino 8 after Sections and AcBuild (any open model: the DWGs are read into a hidden document).
"""
import os, re, json, time, glob, colorsys

VERSION = "v1"
GH_LABEL = "SectionsAC"
OUT_FOLDER = "bergama_sections_ac"
LOG_NAME = "bergama_sections_ac_log.txt"
GH_INPUTS = {}
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
LIB_GLOB = os.path.join(BERGAMA_ROOT, "scripts", "bergama_sections_v*.py")
SEC_DIR = os.path.join(BERGAMA_ROOT, "cached", "bergama_sections")
AC_JSON = os.path.join(BERGAMA_ROOT, "cached", "bergama_archicad", "acbuild.json")
DROP = ("houses behind", "context buildings")       # the Sections houses the Archicad background replaces
SKIP_AC = ("bg terrain", "bg reg")                   # Archicad layers not drawn
AC_LAYER = "archicad background"
LW_MIN, LW_MAX = 0.05, 0.25                          # mm


def load_lib(log):
    fs = sorted(glob.glob(LIB_GLOB), key=lambda p: [int(x) for x in re.findall(r"\d+", os.path.basename(p))])
    if not fs:
        raise RuntimeError(u"%s missing: refresh the kit" % LIB_GLOB)
    ns = {"__name__": "bergama_sections_lib"}
    with open(fs[-1], encoding="utf-8") as f:
        exec(compile(f.read(), fs[-1], "exec"), ns)
    E = ns["load_engine"](log)
    ns["_ENGINE_W"][:] = [E["text_w"]]
    log.append(u"library: %s (%s)" % (fs[-1], ns.get("VERSION")))
    return ns, E


def hexc(c):
    return u"%02X%02X%02X" % (c.R, c.G, c.B)


def _mix(a, b, t):
    A = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    B = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return u"".join(u"%02X" % int(round(x + (y - x) * t)) for x, y in zip(A, B))


def recolour(c, P, fill):
    """the Archicad colour in the Sections house palette: blue-ish = glass, red / orange = roof, the rest on a
    light-to-dark ramp wall -> edge; lines are edge-dark"""
    r, g, b = [int(c[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    if not fill:
        return _mix(P["H_EDGE"], P["INK_CUT"], 0.5 if l > 0.3 else 0.9)
    if s > 0.2 and 0.45 <= h <= 0.72:
        return P["H_GLASS"]
    if s > 0.25 and (h <= 0.1 or h >= 0.93):
        return P["H_ROOF"]
    if l < 0.25:
        return P["INK_CUT"]
    return _mix(P["H_EDGE"], P["H_WALL"], min(1.0, max(0.0, (l - 0.25) / 0.65)))


def read_dwg(path, log):
    """[(layer lower-case, kind 'fill'|'line', [[(x, y)]], colour hex, lw mm)] of a DWG read into a hidden document;
    blocks are opened (their parts take the block's layer when on layer 0)"""
    import Rhino
    rg = Rhino.Geometry
    doc, temp = None, []
    try:
        doc = Rhino.RhinoDoc.CreateHeadless(None)
        if not doc.Import(path):
            doc.Dispose()
            doc = None
    except Exception:
        doc = None
    if doc is None:                                   # fallback: import into the open model, then delete again
        doc = Rhino.RhinoDoc.ActiveDoc
        before = set(o.Id for o in doc.Objects)
        Rhino.RhinoApp.RunScript(u'_-Import "%s" _Enter' % path, False)
        temp = [o for o in doc.Objects if o.Id not in before]
        if not temp:
            raise RuntimeError(u"Rhino could not import %s" % path)
        log.append(u"%s read into the open model (no hidden document) and removed again" % os.path.basename(path))
    try:
        out = []

        def lay_of(a, parent):
            nm = doc.Layers[a.LayerIndex].Name if a.LayerIndex >= 0 else u""
            return parent if (parent and nm.lower() in (u"0", u"default", u"")) else nm

        def col_of(a, parent_col):
            src = a.ColorSource
            if src == Rhino.DocObjects.ObjectColorSource.ColorFromObject:
                return hexc(a.ObjectColor)
            if src == Rhino.DocObjects.ObjectColorSource.ColorFromParent and parent_col:
                return parent_col
            return hexc(doc.Layers[a.LayerIndex].Color)

        def lw_of(a):
            w = a.PlotWeight if a.PlotWeightSource == Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject \
                else doc.Layers[a.LayerIndex].PlotWeight
            return min(LW_MAX, max(LW_MIN, w if w and w > 0 else 0.1))

        def emit(g, a, xf, parent, pcol, depth=0):
            layer, col = lay_of(a, parent), col_of(a, pcol)
            if isinstance(g, rg.InstanceReferenceGeometry):
                idef = doc.InstanceDefinitions.FindId(g.ParentIdefId)
                if idef is None or depth > 8:
                    return
                for so in idef.GetObjects():
                    emit(so.Geometry, so.Attributes, xf * g.Xform, layer, col, depth + 1)
                return
            g = g.Duplicate()
            g.Transform(xf)
            if isinstance(g, rg.Hatch):
                rings = []
                for outer in (True, False):
                    for cv in g.Get3dCurves(outer) or []:
                        P = [(p[0], p[1]) for p in _pts(rg, cv)]
                        if len(P) >= 3:
                            rings.append(P)
                if rings:
                    out.append((layer.lower(), "fill", rings, col, 0.0))
            elif isinstance(g, rg.Curve):
                P = [(p[0], p[1]) for p in _pts(rg, g)]
                if len(P) >= 2:
                    out.append((layer.lower(), "line", [P], col, lw_of(a)))
        for o in (temp or doc.Objects):
            emit(o.Geometry, o.Attributes, rg.Transform.Identity, u"", None)
        return out
    finally:
        if temp:
            for o in temp:
                doc.Objects.Delete(o, True)
        else:
            doc.Dispose()


def _pts(rg, g):
    try:
        ok, pl = g.TryGetPolyline()
        if ok:
            return [(p.X, p.Y) for p in pl]
    except Exception:
        pass
    pl = g.ToPolyline(0.01, 0.0, 0.0, 0.0)      # tolerance 0.01 drawing units
    if pl is not None:
        ok, P = pl.TryGetPolyline()
        if ok:
            return [(p.X, p.Y) for p in P]
    ts = g.DivideByCount(24, True) or []
    return [(g.PointAt(t).X, g.PointAt(t).Y) for t in ts]


def register(G, reg, L):
    """DWG (x, y) -> (s, z): the two registration blocks (start 0.4 m wide at s = 0, end 0.8 m at s = L, bottom at
    reg z); None when they are not found"""
    R = [p for lay, k, rings, c, w in G if lay.endswith(u"bg reg") for r in rings for p in r]
    if len(R) < 4:
        return None
    xs = sorted(p[0] for p in R)
    gap = max(range(1, len(xs)), key=lambda i: xs[i] - xs[i - 1])
    left = [p for p in R if p[0] < xs[gap]]
    right = [p for p in R if p[0] >= xs[gap]]
    wl = max(p[0] for p in left) - min(p[0] for p in left)
    wr = max(p[0] for p in right) - min(p[0] for p in right)
    cl = (max(p[0] for p in left) + min(p[0] for p in left)) / 2.0
    cr = (max(p[0] for p in right) + min(p[0] for p in right)) / 2.0
    xs0, xs1 = (cl, cr) if wl <= wr else (cr, cl)       # the narrow block is the start
    k = L / (xs1 - xs0)
    yb = min(p[1] for p in R)
    return lambda x, y: ((x - xs0) * k, reg["z"] + (y - yb) * abs(k))


def main():
    t0 = time.time()
    log = []
    lib, E = load_lib(log)
    _layer = lib["_item_layer"]
    P = dict((k, lib[k]) for k in ("H_WALL", "H_ROOF", "H_EDGE", "H_GLASS", "INK_CUT"))
    with open(os.path.join(SEC_DIR, "cuts.json"), encoding="utf-8") as f:
        CJ = json.load(f)
    log.append(u"Sections cache: %s (%s %s)" % (SEC_DIR, CJ.get("version"), CJ.get("run")))
    AC = {}
    if os.path.isfile(AC_JSON):
        with open(AC_JSON, encoding="utf-8") as f:
            AC = json.load(f)
        log.append(u"AcBuild: %s (%s %s, Tapir %s)" % (AC_JSON, AC.get("version"), AC.get("run"), AC.get("tapir")))
    else:
        log.append(u"FLAG %s not found: press AcBuild first; every cut keeps the Sections houses" % AC_JSON)
    Lof = dict((c["name"], c["L"]) for c in AC.get("cuts", []))
    dwgs = glob.glob(os.path.join(AC.get("dwg_dir") or "", "**", "*.dwg"), recursive=True) if AC else []
    names = list(CJ["cuts"].keys())
    items_of = {}
    for nm in names:
        with open(os.path.join(SEC_DIR, CJ["cuts"][nm]["items_file"]), encoding="utf-8") as f:
            items_of[nm] = json.load(f)
    # ---- the grid and the one cached scale (as the Sections a3_sheet)
    W, H = lib["A3"]
    M_, G_, T_ = lib["A3_MARGIN"], lib["A3_GAP"], lib["A3_TITLE"]
    scales = sorted(int(d) for d in items_of[names[0]])
    best = None
    for nc, nr in lib["A3_GRIDS"]:
        if nc * nr < len(names):
            continue
        cw = (W - 2 * M_ - (nc - 1) * G_) / nc
        ch = (H - 2 * M_ - T_ - (nr - 1) * G_) / nr

        def fits(d):
            for nm in names:
                b = items_of[nm][str(d)]["bbox"]
                if b[2] - b[0] > cw or (b[3] - b[1]) * 1.15 > ch:    # 15 %: room for taller Archicad roofs
                    return False
            return True
        d = next((d for d in scales if fits(d)), scales[-1])
        if best is None or d < best[0]:
            best = (d, nc, nr, cw, ch)
    den, nc, nr, cw, ch = best
    sheet = [("text", u"SECTIONS N1-A ... N6-B · both banks", M_, H - M_ - 5.0, 5.0, E["INK"], True, "L", "title",
              None, None)]
    n_ac = 0
    for i, nm in enumerate(names):
        cut = items_of[nm][str(den)]
        mp = cut["map"]
        its = [_tup(x) for x in cut["items"]]
        dwg = next((p for p in dwgs if re.search(r"(^|[^A-Za-z0-9])%s([^A-Za-z0-9]|$)" % re.escape(nm),
                                                 os.path.splitext(os.path.basename(p))[0])), None)
        acit = []
        if dwg and nm in Lof:
            try:
                G = read_dwg(dwg, log)
                f_ = register(G, AC["reg"], Lof[nm])
                if f_ is None:
                    log.append(u"FLAG %s: registration blocks (layer BG reg) not in %s: Sections houses kept" % (nm, dwg))
                else:
                    bx = cut["bbox"]
                    K = mp["K"]
                    pg = lambda x, y: (mp["X0"] + (f_(x, y)[0] - mp["lo"]) * K, mp["Y0"] + (f_(x, y)[1] - mp["zb"]) * K)
                    for lay, kind, rings, col, lw in G:
                        if any(lay.endswith(s_) for s_ in SKIP_AC):
                            continue
                        R = [[pg(*p) for p in r] for r in rings]
                        xs = [p[0] for r in R for p in r]
                        if max(xs) < bx[0] or min(xs) > bx[2]:
                            continue
                        R = [[(min(bx[2], max(bx[0], p[0])), p[1]) for p in r] for r in R]   # trimmed to the cut
                        if kind == "fill":
                            acit.append(("poly", R, recolour(col, P, True), None, 0.0, None, AC_LAYER, 1, None, None))
                        else:
                            acit.append(("line", R[0], recolour(col, P, False), lw, None, AC_LAYER, 1))
                    log.append(u"%s: Archicad background %s, %d pieces" % (nm, os.path.basename(dwg), len(acit)))
            except Exception as ex:
                log.append(u"FLAG %s: %s not read (%s: %s): Sections houses kept" % (nm, dwg, type(ex).__name__, ex))
        elif AC:
            log.append(u"FLAG %s: no DWG in %s: Sections houses kept" % (nm, AC.get("dwg_dir")))
        if acit:
            n_ac += 1
            at = next((j for j, x in enumerate(its) if _layer(x) in DROP), None)
            if at is None:
                at = max([j + 1 for j, x in enumerate(its) if _layer(x) in ("sky", "ground behind")] or [0])
            keep = [x for x in its if _layer(x) not in DROP]
            at = sum(1 for x in its[:at] if _layer(x) not in DROP)
            its = keep[:at] + acit + keep[at:]
        b = lib["items_bbox"](its)
        w, h = b[2] - b[0], b[3] - b[1]
        f = min(1.0, cw / w, ch / h)
        its = [lib["_shift"](x, -b[0], -b[1]) for x in its if not (x[0] == "text" and re.match(u"^(SCALE )?1:[0-9]", x[1]))]
        if f < 1.0:
            its = [lib["_scale_it"](x, f) for x in its]
        col, row = i % nc, i // nc
        x0 = M_ + col * (cw + G_)
        y0 = H - M_ - T_ - (row + 1) * ch - row * G_
        sheet += [lib["_shift"](x, x0, y0 + (ch - h * f)) for x in its]
    log.append(u"one A3 landscape sheet, %d x %d grid, cached scale 1:%d, %d of %d cut(s) with the Archicad background"
               % (nc, nr, den, n_ac, len(names)))
    os.makedirs(OUT_DIR, exist_ok=True)
    pdf = lib["write_pdf"](os.path.join(OUT_DIR, u"SectionsAC.pdf"), [(W, H, sheet)],
                           u"Sections %s, Archicad background" % u", ".join(names))
    log.append(u"%s  %s" % (pdf, time.strftime("%H:%M:%S")))
    cp = os.path.join(BERGAMA_ROOT, "Data", "bergama_pages_common.py")
    try:
        ns = {"__name__": "bergama_pages_common", "__file__": cp}
        with open(cp, encoding="utf-8") as f:
            exec(compile(f.read(), cp, "exec"), ns)
        ns["pc_review"](pdf, os.path.join(OUT_DIR, "review"), log)
    except Exception as ex:
        log.append(u"FLAG review PNGs not written (%s: %s)" % (type(ex).__name__, ex))
    flags = [l for l in log if u"FLAG" in l]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


def _tup(x):
    """a cached JSON item back to the Sections item tuple (points as tuples)"""
    t = x[0]
    if t == "poly":
        return (t, [[tuple(p) for p in r] for r in x[1]]) + tuple(x[2:])
    if t == "line":
        return (t, [tuple(p) for p in x[1]]) + tuple(x[2:])
    return tuple(x)


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


def _run():
    try:
        return main()
    except Exception as _ex:
        import traceback as _tb
        return "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-900:])


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
        _res = _run()
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
elif __name__ == "__main__":
    print(write_log(_run()))
