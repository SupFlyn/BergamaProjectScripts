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

VERSION = "v1.8"   # v1.8 (run 7 review): Archicad pieces clipped at the bottom of the drawing (walls and piers no longer hang below the ground into the band)   # v1.7 v1.7 (run 7: 0 of 12, 3-7 boxes found): the pair = level bottoms and equal heights, farthest apart; the scale from their distance (= L) instead of the 0.5 m height; the block tops (REG_Z + 0.5) give z; widths only checked (FLAG over 0.15 m off); the boxes logged when no pair   # v1.6 v1.6 (run 6: 0 of 12 registered): the block rectangles also when the DWG draws them as separate edge lines (touching pieces in the lowest band joined first; pieces wider than half the drawing left out); the newest DWG of each cut when the publisher set has written it to more than one folder   # v1.5 v1.5 (run 5: houses floated ~50 m, N4 squeezed): registration by the two block rectangles alone (equal bottoms and 0.5 m heights, widths 1:2; the vertical scale from the 0.5 m height, so long level lines no longer spoil it), checked against L (FLAG over 2 m: Sections houses kept); pieces below the drawing left out; Sections v1.24 kept: its ground behind and the asset trees of "houses behind" stay (only the house drawings go), the AcBuild 200 m profile goes under them as the farthest ground; the registered background written in s/z metres to cached/bergama_archicad/background/<cut>.json for the Sections page   # v1.4 (run 4): v1.4 (run 4): the ground behind from AcBuild v1.3 under the Archicad houses; sky raised and the heading moved up when the houses reach above the drawing   # v1.3: the registration blocks (z below the ground, AcBuild v1.2 puts them at -50 m) are not drawn   # v1.2 (run 2: no layer "BG reg" found in any DWG): registration blocks also found by geometry (the lowest pieces, z 0-0.5 m, far below the ground); DWG layer names logged   # v1.1 (14 Nov run 1): only the 12 node cuts N1-A ... N6-B (the cache also holds S4: 13 cuts fit no grid)
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
DROP = ("houses behind", "context buildings")       # the Sections houses the Archicad background replaces (v1.5: images kept)
BG_DIR = os.path.join(BERGAMA_ROOT, "cached", "bergama_archicad", "background")
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
    """v1.5: DWG (x, y) -> (s, z) from the two registration block rectangles: bottoms level, heights equal (0.5 m),
    the end block twice as wide as the start block (0.8 / 0.4 m, or half of each where the section edge cuts it).
    The scale comes from the 0.5 m height; the position along the cut from the start block, checked against the end
    block (register.res, m). None when no such pair is found."""
    B = []
    for lay, kind, rings, c, w in G:
        P = [p for r in rings for p in r]
        if len(P) < 2:
            continue
        xs, ys = [p[0] for p in P], [p[1] for p in P]
        B.append([min(xs), max(xs), min(ys), max(ys)])
    if not B:
        return None
    y0 = min(b[2] for b in B)
    H = max(b[3] for b in B) - y0
    Wd = max(b[1] for b in B) - min(b[0] for b in B)
    tol = 1e-4 * H
    # v1.6: edges drawn as separate lines: touching pieces of the lowest band joined into one box
    M = [b[:] for b in B if b[3] < y0 + 0.3 * H and b[1] - b[0] < 0.5 * Wd]
    merged = True
    while merged:
        merged = False
        out = []
        for b in M:
            for o in out:
                if b[0] <= o[1] + tol and o[0] <= b[1] + tol and b[2] <= o[3] + tol and o[2] <= b[3] + tol:
                    o[0], o[1], o[2], o[3] = min(o[0], b[0]), max(o[1], b[1]), min(o[2], b[2]), max(o[3], b[3])
                    merged = True
                    break
            else:
                out.append(b)
        M = out
    low = [(b[0], b[1], b[2], b[3] - b[2], b[1] - b[0]) for b in M]
    register.boxes = u"%d: %s" % (len(low), u"; ".join(u"x %.4g-%.4g y %.4g h %.4g" % (b[0], b[1], b[2], b[3])
                                                       for b in sorted(low)[:8]))
    # v1.7: the pair = two boxes with level bottoms and equal heights, farthest apart; the scale from their distance
    # (= L, the section edges may cut either block in half), the height only reported (slab thickness unverified)
    best = None
    for i, a_ in enumerate(low):
        for b_ in low[i + 1:]:
            hh = max(a_[3], b_[3])
            if hh <= 0 or abs(a_[3] - b_[3]) > 0.03 * hh or abs(a_[2] - b_[2]) > 0.03 * hh:
                continue
            sep = abs((a_[0] + a_[1]) - (b_[0] + b_[1])) / 2.0
            if best is None or sep > best[0]:
                best = (sep, a_, b_)
    if best is None:
        return None
    sep, a_, b_ = best
    if a_[4] > b_[4]:
        a_, b_ = b_, a_                                  # the narrower block is the start (0.4 m / 0.8 m)
    k = L / sep
    wa, wb = a_[4] * k, b_[4] * k
    full_a = abs(wa - 0.4) <= abs(wa - 0.2)
    full_b = abs(wb - 0.8) <= abs(wb - 0.4)
    sa = 0.0 if full_a else 0.1
    sb = L if full_b else L - 0.2
    k = (sb - sa) / sep                                  # the half-cut blocks' centres are 0.1 / 0.2 m inside
    xa, xb = (a_[0] + a_[1]) / 2.0, (b_[0] + b_[1]) / 2.0
    d = 1.0 if xb > xa else -1.0
    register.res = max(abs(wa - (0.4 if full_a else 0.2)), abs(wb - (0.8 if full_b else 0.4)))
    register.how = u"block rectangles (scale %.6f m per DWG unit, widths %.2f / %.2f m, height %.2f m, %s)" % (
        k, a_[4] * k, b_[4] * k, a_[3] * k, "left to right" if d > 0 else "mirrored")
    top = a_[2] + a_[3]
    return lambda x, y: (sa + (x - xa) * k * d, reg["z"] + 0.5 + (y - top) * k)


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
    dwgs = sorted(glob.glob(os.path.join(AC.get("dwg_dir") or "", "**", "*.dwg"), recursive=True) if AC else [],
                  key=os.path.getmtime, reverse=True)        # v1.6: the newest of each cut first
    names = sorted(n_ for n_ in CJ["cuts"] if re.match(r"^N[1-6]-[AB]$", n_))
    log.append(u"cuts drawn: %s (left out: %s)" % (u", ".join(names), u", ".join(
        n_ for n_ in CJ["cuts"] if n_ not in names) or u"none"))
    if not names:
        raise RuntimeError(u"no N1-A ... N6-B cut in %s: press Sections first" % SEC_DIR)
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
    if best is None:
        raise RuntimeError(u"%d cuts fit no A3 grid %s" % (len(names), lib["A3_GRIDS"]))
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
                lays = {}
                for g_ in G:
                    lays[g_[0]] = lays.get(g_[0], 0) + 1
                log.append(u"%s DWG layers: %s" % (nm, u", ".join(u"%s %d" % kv for kv in sorted(
                    lays.items(), key=lambda kv: -kv[1])[:15])))
                f_ = register(G, AC["reg"], Lof[nm])
                if f_ is not None:
                    log.append(u"%s: registered by %s; block widths %.2f m off" % (nm, register.how, register.res))
                    if register.res > 0.15:
                        log.append(u"FLAG %s: the block widths are %.2f m off 0.4 / 0.8 m: registration not trusted, "
                                   u"Sections houses kept (boxes %s)" % (nm, register.res, register.boxes))
                        f_ = None
                else:
                    log.append(u"FLAG %s: the two registration blocks not found in %s (boxes in the lowest band %s): "
                               u"Sections houses kept" % (nm, dwg, getattr(register, "boxes", "?")))
                if f_ is not None:
                    bg = []
                    bx = cut["bbox"]
                    K = mp["K"]
                    pg = lambda x, y: (mp["X0"] + (f_(x, y)[0] - mp["lo"]) * K, mp["Y0"] + (f_(x, y)[1] - mp["zb"]) * K)
                    for lay, kind, rings, col, lw in G:
                        if any(lay.endswith(s_) for s_ in SKIP_AC):
                            continue
                        if max(f_(*p)[1] for r in rings for p in r) < max(AC["reg"]["z"] + 1.0, mp["zb"]):
                            continue                     # a registration block, a level line: below the drawing
                        SZ = [[f_(*p) for p in r] for r in rings]
                        if max(q[0] for r in SZ for q in r) < 0 or min(q[0] for r in SZ for q in r) > Lof[nm]:
                            continue
                        bg.append((kind, [[(round(q[0], 3), round(q[1], 3)) for q in r] for r in SZ], col, lw))
                        R = [[pg(*p) for p in r] for r in rings]
                        xs = [p[0] for r in R for p in r]
                        if max(xs) < bx[0] or min(xs) > bx[2]:
                            continue
                        yb_ = mp["Y0"]                   # v1.8: the bottom of the drawing (z = zb)
                        R = [[(min(bx[2], max(bx[0], p[0])), max(yb_, p[1])) for p in r] for r in R]   # trimmed to the cut
                        if kind == "fill":
                            acit.append(("poly", R, recolour(col, P, True), None, 0.0, None, AC_LAYER, 1, None, None))
                        else:
                            acit.append(("line", R[0], recolour(col, P, False), lw, None, AC_LAYER, 1))
                    zs = [p[1] for _k, r_, _c, _w in bg for r in r_ for p in r]
                    log.append(u"%s: Archicad background %s, %d pieces, z %.1f ... %.1f m (cut ground %.1f ... %.1f m)" % (
                        nm, os.path.basename(dwg), len(acit), min(zs or [0]), max(zs or [0]),
                        min([z for _s, z in CJ["cuts"][nm].get("surface") or [(0, 0)]]),
                        max([z for _s, z in CJ["cuts"][nm].get("surface") or [(0, 0)]])))
                    os.makedirs(BG_DIR, exist_ok=True)
                    with open(os.path.join(BG_DIR, nm + ".json"), "w", encoding="utf-8") as fo:
                        json.dump({"version": VERSION, "cut": nm, "L": Lof[nm], "dwg": dwg, "units": "s, z in m (z absolute)",
                                   "pieces": [{"kind": k_, "rings": r_, "colour": recolour(c_, P, k_ == "fill"),
                                               "lw": w_} for k_, r_, c_, w_ in bg]}, fo)
            except Exception as ex:
                log.append(u"FLAG %s: %s not read (%s: %s): Sections houses kept" % (nm, dwg, type(ex).__name__, ex))
        elif AC:
            log.append(u"FLAG %s: no DWG in %s: Sections houses kept" % (nm, AC.get("dwg_dir")))
        if acit:
            n_ac += 1
            back = next((c_.get("back") for c_ in AC.get("cuts", []) if c_["name"] == nm), None) or []
            surf = CJ["cuts"][nm].get("surface") or []
            mp = cut["map"]
            PX = lambda s_, z_: (mp["X0"] + (s_ - mp["lo"]) * mp["K"], mp["Y0"] + (z_ - mp["zb"]) * mp["K"])

            def sz(s_):
                if not surf:
                    return -1e9
                j = min(range(len(surf)), key=lambda i_: abs(surf[i_][0] - s_))
                return surf[j][1]
            bx = cut["bbox"]
            pts_ = [(s_, max(z_, sz(s_))) for s_, z_ in back if z_ is not None]
            pts_ = [p_ for p_ in pts_ if bx[0] <= PX(*p_)[0] <= bx[2]]
            gb = [x for x in its if _layer(x) == "ground behind" and x[0] == "poly"]
            far = None
            if len(pts_) >= 2:
                ring = [PX(*p_) for p_ in pts_] + [PX(pts_[-1][0], mp["zb"]), PX(pts_[0][0], mp["zb"])]
                far = ("poly", [ring], gb[0][2] if gb else lib["BACK_FILL"], None, 0.0, None, "ground behind", 1,
                       None, None)
            else:
                log.append(u"%s: no ground-behind profile in acbuild.json (AcBuild v1.3 writes it)" % nm)
            drop = lambda x: _layer(x) in DROP and x[0] != "image"
            keep = [x for x in its if not drop(x)]
            g_i = [j for j, x in enumerate(keep) if _layer(x) == "ground behind"]
            s_i = [j for j, x in enumerate(keep) if _layer(x) == "sky"]
            first = g_i[0] if g_i else (s_i[-1] + 1 if s_i else 0)
            at = g_i[-1] + 1 if g_i else first
            its = keep[:first] + ([far] if far else []) + keep[first:at] + acit + keep[at:]
            its = _lift(lib, its, acit, _layer)
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


def _ys(x):
    t = x[0]
    if t in ("poly",):
        return [p[1] for r in x[1] for p in r]
    if t == "line":
        return [p[1] for p in x[1]]
    if t == "text":
        return [x[3]]
    if t == "circle":
        return [x[2]]
    return []


def _lift(lib, its, acit, _layer):
    """v1.4: houses reaching above the drawing: the sky is raised to cover them and the heading above it (titles,
    scale bar) moved up by the same amount"""
    sky = [x for x in its if _layer(x) == "sky" and x[0] == "poly"]
    if not sky:
        return its
    top = max(max(_ys(x)) for x in sky)
    ac_top = max([max(_ys(x)) for x in acit if _ys(x)] or [top])
    dy = ac_top + 2.0 - top
    if dy <= 0:
        return its
    out, ids = [], set(id(x) for x in acit)
    for x in its:
        if id(x) in ids:
            out.append(x)
        elif _layer(x) == "sky" and x[0] == "poly":
            out.append((x[0], [[(p[0], p[1] + dy if p[1] >= top - 0.01 else p[1]) for p in r] for r in x[1]]) + x[2:])
        elif _ys(x) and min(_ys(x)) >= top - 0.01:
            out.append(lib["_shift"](x, 0.0, dy))
        else:
            out.append(x)
    return out


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
