# -*- coding: utf-8 -*-
# r: numpy, pillow, scipy, potracer
"""Bergama Group 6: TRACE ASSETS v1 (30 Oct 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.
Turns raster example images (Pinterest and the like) into TRUE VECTOR drawings at 1:1 and pulls every asset out of
each image as its own piece, clipped along its own outer outline (no background box, no neighbours). Aras 30 Oct
06:17-06:22: "transform them into vectoral drawings ... exactly 1:1 vectoral", "every asset from each image",
"clipping each asset from their outer lines", "and vectoral".

Component: Rhino 8 > Grasshopper > Python 3 Script, paste the whole file. The first run installs numpy, Pillow, SciPy
and potracer (the "# r:" line above; needs internet once).
  input  run         Button
  input  rhino_bake  Boolean Toggle, off by default: also bake every traced asset as curves (layer TRACE::<image>)
  output log         the last run's report
  output done        "done HH:MM:SS.ss · N s" (one-click chain)
Reads  ~/Downloads/Bergama/Data/trace_in/   every .png / .jpg / .jpeg / .webp / .bmp (sub-folders too); an optional
       SOURCES.csv there (columns file + url or source) keeps each image's source for the booklet's ASSETS list.
Writes ~/Downloads/Bergama/cached/bergama_trace_assets/<image>/
         <image>_all.svg            every traced asset in place, the image's own size in pixels (no raster inside)
         <image>_NN.svg             asset NN in its traced colours (flat fills, Bezier curves), source pixel units
         <image>_NN_silhouette.svg  asset NN as one filled outline (for recolouring in the sections)
       ~/Downloads/Bergama/cached/bergama_trace_assets/traced_assets.json   one entry per asset (image, box, colours,
         files, source) for later scripts; nothing goes in the public repo (copyrighted sources, Aras 30 Oct 06:19).
How it works: background = the colour of the image border (or transparency); asset = every connected group of
non-background pixels (gaps up to JOIN_PX joined), traced from its OWN pixels only with potrace (curves fitted to the
pixel edges); colours = up to COLOURS flat colours per asset, stacked so no gaps open between them.
How exact: a trace follows the pixel edges to within about one source pixel; detail smaller than a pixel, soft
shadows, gradients and photo textures cannot be recovered and become flat colour areas; assets that touch or
overlap in the image come out as ONE asset.
"""
import os, time, json

# ---- SETTINGS ----
VERSION = "v1"
GH_LABEL = "TraceAssets"
OUT_FOLDER = "bergama_trace_assets"
LOG_NAME = "bergama_trace_assets_log.txt"
COLOURS = 6          # flat colours per asset (1 = silhouette only)
BG_TOL = 40          # colour distance (0-441) from the background colour that still counts as background
JOIN_PX = 3          # pixel gap that still joins two pieces into one asset (leaves of one tree)
MIN_PX = 150         # assets with fewer pixels are specks and are skipped
TURD_PX = 2          # potrace: speckles up to this many pixels inside an asset are ignored
ALPHAMAX = 1.0       # potrace corner threshold (0 = all corners, 1.33 = all curves)
OPT_TOL = 0.2        # potrace curve optimisation tolerance (pixels)
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".bmp")

# ---- Bergama folders (Aras 24 Oct 08:28 + 27 Oct 11:07; SCRIPT_STANDARD §9). Every script uses ONLY these. ----
#   Downloads/Bergama/output/<name>/          final PDFs only
#   Downloads/Bergama/logs/                    every log file and log folder
#   Downloads/Bergama/cached/<name>/           caches, results other scripts read, any other working file
#   Downloads/Bergama/cached/booklet/<name>/   the script's booklet assets (blocks.json, results, images);
#                                              the booklet's own leftovers in cached/booklet/
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_booklet(name):
    return os.path.join(BERGAMA_ROOT, "cached", "booklet", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


def bg_first(paths):
    """The first path that exists (new place first, then where older versions wrote it), else the first."""
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[0]


def bg_tidy_output(name, cache_dir=None):
    """output/<name>/ keeps PDFs only: log files and anything in a log folder move to logs/<name>/, every other
    non-PDF file to cached/<name>/from_output/ (or cache_dir: the booklet uses cached/booklet/; moved, never deleted;
    same sub-folders). Empty folders go.
    Returns short log lines (counts, not one line per file)."""
    import shutil as _sh
    root, moved, fail = bg_output(name), {}, []
    if not os.path.isdir(root):
        return []
    for d, subs, files in os.walk(root, topdown=False):
        rel = os.path.relpath(d, root)
        rel = "" if rel == "." else rel
        for fn in files:
            if fn.lower().endswith(".pdf"):
                continue
            is_log = "log" in fn.lower() or any("log" in p.lower() for p in rel.split(os.sep) if p)
            dst = os.path.join(bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output")), rel, fn)
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(dst):
                    os.remove(dst)
                _sh.move(os.path.join(d, fn), dst)
                top = bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output"))
                moved[top] = moved.get(top, 0) + 1
            except Exception as ex:
                fail.append(u"%s (%s)" % (os.path.join(rel, fn), type(ex).__name__))
        if d != root:
            try:
                os.rmdir(d)                       # only when empty
            except Exception:
                pass
    return ([u"output/%s: %d non-PDF file(s) moved to %s" % (name, n, d) for d, n in sorted(moved.items())] +
            ([u"output/%s: could not move %s" % (name, ", ".join(fail[:5]))] if fail else []))

BERGAMA = BERGAMA_ROOT
DATA_DIR = os.path.join(BERGAMA, "Data")
IN_DIR = os.path.join(DATA_DIR, "trace_in")
CACHE_DIR = bg_cache(OUT_FOLDER)
LOG_DIR = bg_logs()

def chain_fire(v, key):
    """25 Oct 10:20 (one-click chain): the previous script's done output is a text "done HH:MM:SS.ss ..." that stays
    after the Button is released; each NEW text fires this script once (the Button still works as before)."""
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
    """The done output: kept until the next run (this Rhino session)."""
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


def tr_sources():
    """{image file name (lower case): source text} from trace_in/SOURCES.csv, or {}"""
    import csv
    p = os.path.join(IN_DIR, "SOURCES.csv")
    out = {}
    if os.path.isfile(p):
        with open(p, encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                fn = os.path.basename((row.get("file") or "").strip()).lower()
                src = " · ".join(v for v in ((row.get("title") or "").strip(), (row.get("author") or "").strip(),
                                             (row.get("url") or row.get("page URL") or row.get("source") or "").strip()) if v)
                if fn:
                    out[fn] = src
    return out


def tr_load(path):
    """(rgb uint8 HxWx3, foreground bool HxW): transparency where the image has it, else distance from the border
    colour (median of the outermost pixel ring)"""
    import numpy as np
    from PIL import Image
    im = Image.open(path)
    im.load()
    rgba = np.asarray(im.convert("RGBA"), dtype=np.uint8)
    rgb = rgba[:, :, :3]
    a = rgba[:, :, 3]
    if (a < 250).mean() > 0.02:                  # a cut-out PNG: the alpha channel is the outline
        return rgb, a >= 128
    ring = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]]).astype(float)
    bg = np.median(ring, axis=0)
    d = np.sqrt(((rgb.astype(float) - bg) ** 2).sum(axis=2))
    return rgb, d > BG_TOL


def tr_assets(fg):
    """[(slice_y, slice_x, own mask)]: one per connected asset, its mask only its own pixels (neighbours cleared)"""
    import numpy as np
    from scipy import ndimage as ndi
    join = ndi.binary_dilation(fg, iterations=JOIN_PX) if JOIN_PX > 0 else fg
    lab, n = ndi.label(join)
    out = []
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        if sl is None:
            continue
        own = fg[sl] & (lab[sl] == i)
        if own.sum() >= MIN_PX:
            out.append((sl[0], sl[1], own))
    return out


def tr_palette(rgb, mask, k):
    """k flat colours of the masked pixels (k-means, fixed start = the same result every run) and each pixel's index;
    colours sorted by area, largest first"""
    import numpy as np
    px = rgb[mask].astype(float)
    k = max(1, min(k, len(px)))
    if k == 1:
        return [px.mean(axis=0)], np.zeros(mask.shape, int)
    q = np.quantile(px.sum(axis=1), np.linspace(0.05, 0.95, k))
    cen = np.array([px[np.argmin(np.abs(px.sum(axis=1) - v))] for v in q])
    step = max(1, len(px) // 200000)             # big assets: fit on a sample, assign all
    sample = px[::step]
    for _ in range(12):
        lab = ((sample[:, None, :] - cen[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
        for j in range(k):
            if (lab == j).any():
                cen[j] = sample[lab == j].mean(axis=0)
    lab_all = np.zeros(mask.shape, int)
    lab_all[mask] = ((px[:, None, :] - cen[None, :, :]) ** 2).sum(axis=2).argmin(axis=1)
    order = np.argsort([-(lab_all[mask] == j).sum() for j in range(k)])
    remap = np.zeros(k, int)
    remap[order] = np.arange(k)
    return [cen[j] for j in order], remap[lab_all]


def tr_trace(mask):
    """potrace curves of a bool mask: [[("M", (x, y)), ("L", (x, y)) | ("C", c1, c2, end), ...], ...] in mask pixels"""
    import numpy as np
    import potrace
    from PIL import Image
    img = Image.fromarray(np.where(mask, 0, 255).astype(np.uint8), "L")   # filled pixels black
    bm = potrace.Bitmap(img, blacklevel=0.5)
    plist = bm.trace(turdsize=TURD_PX, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=ALPHAMAX,
                     opticurve=True, opttolerance=OPT_TOL)
    paths = []
    for curve in plist:
        s = curve.start_point
        seg = [("M", (s.x, s.y))]
        for g in curve.segments:
            if g.is_corner:
                seg += [("L", (g.c.x, g.c.y)), ("L", (g.end_point.x, g.end_point.y))]
            else:
                seg.append(("C", (g.c1.x, g.c1.y), (g.c2.x, g.c2.y), (g.end_point.x, g.end_point.y)))
        paths.append(seg)
    return paths


def tr_d(paths, ox, oy):
    """SVG path data, shifted by (ox, oy) pixels (the asset's place in the image)"""
    f = lambda p: "%.2f,%.2f" % (p[0] + ox, p[1] + oy)
    out = []
    for seg in paths:
        for g in seg:
            out.append(g[0] + (f(g[1]) if g[0] != "C" else " ".join(f(q) for q in g[1:])))
        out.append("Z")
    return "".join(out)


def tr_hex(c):
    return "#%02x%02x%02x" % tuple(int(max(0, min(255, round(v)))) for v in c)


def tr_svg(path, w, h, layers, vx=0, vy=0):
    """write an SVG: layers [(hex, d)], even-odd fills, viewBox in source pixels (1:1)"""
    with open(path, "w", encoding="utf-8") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="%d %d %d %d">\n' %
                (w, h, vx, vy, w, h))
        for col, d in layers:
            f.write('<path fill="%s" fill-rule="evenodd" stroke="none" d="%s"/>\n' % (col, d))
        f.write("</svg>\n")


def tr_bake(layer, items):
    """curves into the open Rhino file on TRACE::<image>::NN (1 source pixel = 1 model unit, y flipped up)"""
    import Rhino
    doc = Rhino.RhinoDoc.ActiveDoc
    n = 0
    for sub, paths in items:
        idx, parent, walk = -1, None, []
        for part in ("TRACE", layer, sub):    # TRACE::<image>::NN, parents made where missing
            walk.append(part)
            idx = doc.Layers.FindByFullPath("::".join(walk), -1)
            if idx < 0:
                L = Rhino.DocObjects.Layer()
                L.Name = part
                if parent is not None:
                    L.ParentLayerId = parent
                idx = doc.Layers.Add(L)
            parent = doc.Layers[idx].Id
        attr = Rhino.DocObjects.ObjectAttributes()
        attr.LayerIndex = idx
        P = lambda q: Rhino.Geometry.Point3d(q[0], -q[1], 0.0)
        for seg in paths:
            pc = Rhino.Geometry.PolyCurve()
            cur = None
            for g in seg:
                if g[0] == "M":
                    cur = P(g[1])
                elif g[0] == "L":
                    nxt = P(g[1])
                    if nxt.DistanceTo(cur) > 1e-9:
                        pc.Append(Rhino.Geometry.LineCurve(cur, nxt))
                    cur = nxt
                else:
                    bz = Rhino.Geometry.BezierCurve([cur, P(g[1]), P(g[2]), P(g[3])])
                    pc.Append(bz.ToNurbsCurve())
                    cur = P(g[3])
            if pc.SegmentCount:
                pc.MakeClosed(1e-6)
                doc.Objects.AddCurve(pc, attr)
                n += 1
    doc.Views.Redraw()
    return n


def tr_key(path):
    st = os.stat(path)
    return "%s|%d|%d|%s" % (VERSION, st.st_size, int(st.st_mtime),
                            ",".join(str(v) for v in (COLOURS, BG_TOL, JOIN_PX, MIN_PX, TURD_PX, ALPHAMAX, OPT_TOL)))


def main():
    t0 = time.time()
    os.makedirs(CACHE_DIR, exist_ok=True)
    if not os.path.isdir(IN_DIR):
        os.makedirs(IN_DIR, exist_ok=True)
        return "No images yet: put them in %s and press again\n%s %s, %.1f s" % (IN_DIR, GH_LABEL, VERSION,
                                                                               time.time() - t0)
    files = sorted(os.path.join(d, f) for d, _, fs in os.walk(IN_DIR) for f in fs if f.lower().endswith(IMG_EXT))
    srcs = tr_sources()
    lib_p = os.path.join(CACHE_DIR, "traced_assets.json")
    try:
        with open(lib_p, encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        old = {}
    lib, lines, n_new, n_kept, bake = {}, [], 0, 0, []
    for path in files:
        stem = os.path.splitext(os.path.relpath(path, IN_DIR))[0].replace(os.sep, "__")
        key = tr_key(path)
        out_dir = os.path.join(CACHE_DIR, stem)
        prev = old.get(stem)
        if prev and prev.get("key") == key and os.path.isfile(os.path.join(out_dir, stem + "_all.svg")):
            lib[stem] = prev                     # unchanged image, same settings: kept (second press is quick)
            n_kept += 1
            continue
        ti = time.time()
        rgb, fg = tr_load(path)
        H, W = fg.shape
        os.makedirs(out_dir, exist_ok=True)
        for fn in os.listdir(out_dir):           # this image's old pieces go: the new trace replaces them all
            if fn.lower().endswith(".svg"):
                os.remove(os.path.join(out_dir, fn))
        assets, all_layers = [], []
        for nn, (sy, sx, own) in enumerate(tr_assets(fg), 1):
            oy, ox = sy.start, sx.start
            h, w = own.shape
            cols, idx = tr_palette(rgb[sy, sx], own, COLOURS)
            layers = []
            for j in range(len(cols)):           # stacked: layer j covers its colour and every smaller one
                m = own & (idx >= j)
                if m.sum() >= TURD_PX + 1:
                    layers.append((tr_hex(cols[j]), tr_d(tr_trace(m), ox, oy)))
            sil = tr_trace(own)
            base = "%s_%02d" % (stem, nn)
            tr_svg(os.path.join(out_dir, base + ".svg"), w, h, layers, ox, oy)
            tr_svg(os.path.join(out_dir, base + "_silhouette.svg"), w, h, [("#000000", tr_d(sil, ox, oy))], ox, oy)
            all_layers += layers
            assets.append(dict(n=nn, box_px=[ox, oy, w, h], pixels=int(own.sum()), colours=[tr_hex(c) for c in cols],
                               svg=base + ".svg", silhouette=base + "_silhouette.svg"))
            if "rhino_bake" in globals() and rhino_bake is True:                 # noqa: F821
                bake.append((stem, "%02d" % nn, [[(g[0],) + tuple((q[0] + ox, q[1] + oy) for q in g[1:]) for g in seg]
                                                  for seg in sil]))
        tr_svg(os.path.join(out_dir, stem + "_all.svg"), W, H, all_layers)
        lib[stem] = dict(key=key, image=os.path.relpath(path, IN_DIR), size_px=[W, H],
                         source=srcs.get(os.path.basename(path).lower(), ""), assets=assets)
        n_new += 1
        lines.append(u"%s: %d assets, %.1f s  %s" % (os.path.relpath(path, IN_DIR), len(assets), time.time() - ti,
                                                     time.strftime("%H:%M:%S")))
    with open(lib_p, "w", encoding="utf-8") as f:
        json.dump(lib, f, indent=1)
    n_b = 0
    if bake:
        by = {}
        for stem, sub, paths in bake:
            by.setdefault(stem, []).append((sub, paths))
        for stem, items in by.items():
            n_b += tr_bake(stem, items)
    no_src = sorted(s for s, v in lib.items() if not v.get("source"))
    head = [u"%s  %s" % (lib_p, time.strftime("%H:%M:%S")),
            u"%d images: %d traced, %d unchanged (kept); %d assets in all" % (
                len(lib), n_new, n_kept, sum(len(v["assets"]) for v in lib.values()))]
    if n_b:
        head.append(u"Rhino: %d curves baked on TRACE::<image>::NN" % n_b)
    if no_src:
        head.append(u"No source in trace_in/SOURCES.csv for %d image(s): %s" % (len(no_src), ", ".join(no_src[:8])))
    return "%s\n%s\n%s %s, %.1f s" % ("\n".join(head), "\n".join(lines), GH_LABEL, VERSION, time.time() - t0)


# ---- Grasshopper wiring (same in every script; never define a function named run: it would hide the input) ----
if "ghenv" in globals():
    import scriptcontext as _sc
    _k = "bergama_" + OUT_FOLDER
    try:
        _k += ":" + str(ghenv.Component.InstanceGuid)   # each component copy keeps its own log and done  # noqa: F821
    except Exception:
        pass
    _pressed = any(v is True for k, v in list(globals().items())
                   if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "rhino_bake", "done")) or \
        any(chain_fire(v, _k + "_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:                 # the error goes into the log panel; the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky[_k + "_log"] = write_log(_res)
        _sc.sticky[_k + "_status"] = ("ERROR" if _res.startswith("ERROR") else
                                      time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky[_k + "_done"] = done_text(True, not _res.startswith("ERROR"), time.time() - _t0)
        _sc.sticky[_k + "_ver"] = VERSION
    if _sc.sticky.get(_k + "_ver") != VERSION:   # Aras 27 Oct 15:35: a newly pasted version shows itself at once, idle
        for _s in ("_log", "_status", "_done"):
            _sc.sticky.pop(_k + _s, None)
    done = _sc.sticky.get(_k + "_done", "idle")
    log = _sc.sticky.get(_k + "_log", "Press the Button to trace the images in " + IN_DIR)
    print(log)
    try:
        ghenv.Component.Message = GH_LABEL + " " + VERSION + " · " + _sc.sticky.get(_k + "_status", "idle")  # noqa: F821
    except Exception:
        pass
else:
    print(write_log(main()))
