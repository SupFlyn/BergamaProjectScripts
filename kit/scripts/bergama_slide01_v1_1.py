# -*- coding: utf-8 -*-
"""Bergama Group 6: SLIDE01 v1.1 (14 Nov 2026; v1.1 = run 1 review: Page02 drawn at 0.47 had 1.1 mm texts: Page02 v2.11+ takes page_mm too, so every panel gets page_mm and is drawn at TEXT_SCALE), slide 1 (analysis) on ONE A3 landscape sheet (Aras 14 Nov 15:27 UTC:
"currently everything in slide 1 would be single A3 ... this applies to everything"; 15:25 UTC "the scale is not
important"). Four drawings, each made live by its own page script (nothing read back from a PDF, Aras 12:55 UTC):
  site map (newest bergama_p02_what_is_there_v*), heights axo (newest bergama_page01_axo_v*), free ground with the site
  photos (newest bergama_page01_free_v*), street use (newest bergama_page01_move_v*).
Each page script runs with scale 0 and page_mm = its panel / TEXT_SCALE (so its map is fitted, its texts drawn at their
own size), its items are caught before writing, then scaled into its panel of the A3 sheet (2 x 2, no overlaps):
every item, clip, line width, text size and photo is transformed, layers and clips renamed per panel.
Writes output/bergama_slide01/Slide01_Analysis.pdf / .svg, review PNGs, and output/presentation/1.pdf.
Reads: Data/bergama_pages_common.py (v3.10+) and whatever the four page scripts read (their caches are reused).
"""
import os, re, glob, time

VERSION = "v1.1"
GH_LABEL = "Slide01"
OUT_FOLDER = "bergama_slide01"
LOG_NAME = "bergama_slide01_log.txt"
GH_INPUTS = {"text_scale": "float 0.3..1.0 = 0.6"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "Slide01_Analysis"
SLIDE = 1
SHEET = (420.0, 297.0)             # mm, A3 landscape
MARGIN, GAP = 6.0, 4.0             # mm
GRID = [["site", "axo"], ["free", "move"]]    # rows, top first
PAGES = {"site": "bergama_p02_what_is_there_v*.py", "axo": "bergama_page01_axo_v*.py",
         "free": "bergama_page01_free_v*.py", "move": "bergama_page01_move_v*.py"}
WIRING = "# ---- Grasshopper wiring"


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


def newest(pat):
    found = glob.glob(os.path.join(BERGAMA_ROOT, "scripts", pat))
    if not found:
        raise RuntimeError(u"no %s: run Bergama.bat once" % os.path.join(BERGAMA_ROOT, "scripts", pat))
    return max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])


def page_ns(path):
    with open(path, encoding="utf-8") as f:
        code = f.read()
    ns = {"__name__": "bergama_slide01_page"}
    exec(compile(code[:code.index(WIRING)] if WIRING in code else code, path, "exec"), ns)
    return ns


def run_page(key, path, G, page, log):
    """the page script's main() with its writer caught: {w, h, items, clips, photos}"""
    ns = page_ns(path)
    got = {}
    if key == "site":                                    # Page02: its own A3 page; catch write_pdf (it still writes
        real = ns["load_lib"]                            # its own files, as a press of Page02 would)

        def load_lib(lg):
            B = dict(real(lg))
            wp = B["write_pdf"]

            def write_pdf(p, w, h, items, title, clips=None, forms=None):
                got.update(w=w, h=h, items=list(items), clips=dict(clips or {}), photos=[], forms=forms)
                return wp(p, w, h, items, title, clips, forms) if forms else wp(p, w, h, items, title, clips)
            B["write_pdf"] = write_pdf
            return B
        ns["load_lib"] = load_lib
        ns["page_mm"] = page                             # v1.1: Page02 v2.11+ lays out a compact page at this size
    else:
        def pc_write(lib, M, items, out_dir, name, title, lg, photos=None, clips=None):
            G["pc_frame_check"](items, M.box, lg, lib.get("text_w"))
            bx = M.box
            got.update(w=M.w, h=M.h, items=list(items), photos=list(photos or []), forms=None,
                       clips=clips or {G["PC_CLIP"]: [[[(bx[0], bx[1]), (bx[2], bx[1]), (bx[2], bx[3]),
                                                       (bx[0], bx[3])]]]})
            lg.append(u"%s caught for the slide (%.0f x %.0f mm, 1:%s)" % (name, M.w, M.h, format(int(M.den), ",d")))
            return []
        ns["load_common"] = lambda: dict(G, pc_write=pc_write)
        ns["scale"] = 0
        ns["page_mm"] = page
    res = ns["main"]()
    lines = (res or u"").splitlines()
    log.append(u"---- %s: %s" % (key, os.path.basename(path)))
    log += [u"  " + l for l in lines if l.startswith(u"FLAG")]
    log.append(u"  " + (lines[-1] if lines else u"(no log)"))
    if not got:
        log.append(u"FLAG: %s wrote nothing" % key)
    return got


def place(got, key, ox, oy, s):
    """every item of a page moved by (ox, oy) and scaled by s; layers and clip ids get the panel's prefix"""
    T = lambda q: (ox + q[0] * s, oy + q[1] * s)
    L = lambda n: u"%s_%s" % (key, n)
    C = lambda c: None if c is None else u"%s_%s" % (key, c)
    out = []
    for it in got["items"]:
        t = it[0]
        if t == "poly":
            out.append((t, [[T(q) for q in R] for R in it[1]], it[2], it[3], it[4] * s, it[5], L(it[6]), it[7],
                        it[8], C(it[9])) + tuple(it[10:]))
        elif t == "line":
            d = it[6] if len(it) > 6 else 1
            d = tuple(v * s for v in d) if isinstance(d, (tuple, list)) else d
            out.append((t, [T(q) for q in it[1]], it[2], it[3] * s, C(it[4]), L(it[5]), d) + tuple(it[7:]))
        elif t == "text":
            x, y = T((it[2], it[3]))
            out.append((t, it[1], x, y, it[4] * s, it[5], it[6], it[7], L(it[8])) + tuple(it[9:]))
        elif t in ("mask", "soft"):
            x, y = T((it[4], it[5]))
            out.append(it[:4] + (x, y, it[6] * s, it[7] * s) + it[8:10] + (L(it[10]), C(it[11])) + tuple(it[12:]))
        elif t == "form":
            a, b, c, d, e, f = it[2]
            e2, f2 = T((e, f))
            out.append((t, it[1], (a * s, b * s, c * s, d * s, e2, f2), L(it[3]), C(it[4])) + tuple(it[5:]))
        else:
            out.append(it)
    clips = dict((C(k), [[[T(q) for q in R] for R in rs] for rs in v]) for k, v in got["clips"].items())
    photos = [(jp, ox + x * s, oy + y * s, w * s, h * s) for jp, x, y, w, h in got["photos"]]
    return out, clips, photos


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    ts = float(globals().get("text_scale") or 0.6)
    rows = len(GRID)
    ph = (SHEET[1] - 2 * MARGIN - (rows - 1) * GAP) / rows
    items, clips, photos = [], {}, []
    forms = {}
    for r, row in enumerate(GRID):
        pw = (SHEET[0] - 2 * MARGIN - (len(row) - 1) * GAP) / len(row)
        y0 = SHEET[1] - MARGIN - (r + 1) * ph - r * GAP
        for c, key in enumerate(row):
            x0 = MARGIN + c * (pw + GAP)
            path = newest(PAGES[key])
            got = run_page(key, path, G, (pw / ts, ph / ts), log)
            if not got:
                continue
            s = min(pw / got["w"], ph / got["h"])
            ox, oy = x0 + (pw - got["w"] * s) / 2.0, y0 + (ph - got["h"] * s) / 2.0
            it_, cl_, ph_ = place(got, key, ox, oy, s)
            items += it_
            clips.update(cl_)
            photos += ph_
            forms.update(got.get("forms") or {})
            log.append(u"  panel %s: page %.0f x %.0f mm drawn at %.2f (texts %.0f%% of their size), at x %.0f y %.0f"
                       % (key, got["w"], got["h"], s, 100 * s, ox, oy))
            if s < 0.45:
                log.append(u"FLAG: panel %s drawn at %.2f: its texts may be too small to read" % (key, s))
    os.makedirs(OUT_DIR, exist_ok=True)
    title = u"Slide 1: analysis"
    paths = []
    for ext, fn in ((".pdf", lib["write_pdf"]), (".svg", lib["write_svg"])):
        p = os.path.join(OUT_DIR, NAME + ext)
        try:
            p2 = fn(p, SHEET[0], SHEET[1], items, title, clips, forms) if forms else \
                fn(p, SHEET[0], SHEET[1], items, title, clips)
            paths.append(p2 or p)
            log.append(u"%s  %s (%.0f x %.0f mm, %d objects)" % (p2 or p, time.strftime("%H:%M:%S"), SHEET[0],
                                                                 SHEET[1], len(items)))
        except Exception as ex:
            log.append(u"FLAG: %s not written (%s: %s)" % (p, type(ex).__name__, ex))
    if photos:
        G["pc_photos"](paths, photos, SHEET[1], log)
    pdfs = [p_ for p_ in paths if p_.lower().endswith(".pdf")]
    if pdfs:
        G["pc_review"](pdfs[0], os.path.join(OUT_DIR, "review"), log)
        G["pc_present"](pdfs[0], SLIDE, log)
    flags = [l for l in log if l.lstrip().startswith(u"FLAG")]
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
