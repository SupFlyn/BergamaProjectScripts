# -*- coding: utf-8 -*-
"""Bergama Group 6: SLIDE01 v1.8 (15 Nov 2026; v1.8 = slide 1 run 10: in pass 2 the streets page, given a short slot, shrank its map to 1:71,000 and FLAGged: a pass-2 page is now kept only if it has no more FLAGs, its map is not drawn at under 2/3 of its pass-1 scale and its sheet scale not lower; else the pass-1 page stays (it always fits its slot); v1.7 = slide 1 run 9: the bottom fifth of the sheet stayed empty because each page was laid out for a first-guess panel: a second pass now gives every page its real slot (the column height shared in proportion to the first pass) at its planned scale, so a page with more height can use it (fewer legend columns, a larger map), then the ink is fitted again; v1.6 = slide 1 run 8: the sheet's bottom quarter stayed empty (the packing only raised the smallest scale): among the packings whose smallest scale is at least 95 % of the best, the one that covers the most of the sheet is taken; v1.5 = slide 1 review (run 5): (1) the printed scales were wrong on the sheet (a 1:15,000 page drawn at 0.65 is 1:23,000): each map panel is now drawn at the round scale just below its fit, and its "1:N" / "1/N" words are rewritten to that scale; (2) empty bands: the column width and the two panel heights per column are searched so the smallest text scale on the sheet is as large as possible, panels stacked top-down left-aligned with 8 mm gutters; v1.4 = Aras 21:26 UTC "drawings flows out fix that": each panel is fitted by its INK (every shape, line, word and photo the page script drew, clipped shapes counted only inside their clip), not by its page box, so nothing can reach past its panel into another; every unclipped shape and line is also cut to its panel; a FLAG if any ink still lies outside; v1.3 = run 3 review: Page02's compact page fills 60 % of its panel height, the free ground panel needed two legend columns: site 0.33 / axo 0.67 of the left column, free 0.60 / move 0.40 of the right; panels top-aligned; v1.2 = Aras 16:17 UTC "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN": free ground and street use are site_alan strips, so they take the right column (free ground with its photos the taller panel), the site map and the axo the left column (PANELS); v1.1 = run 1 review: Page02 drawn at 0.47 had 1.1 mm texts: Page02 v2.11+ takes page_mm too, so every panel gets page_mm and is drawn at TEXT_SCALE), slide 1 (analysis) on ONE A3 landscape sheet (Aras 14 Nov 15:27 UTC:
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

VERSION = "v1.8"
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
MARGIN, GAP = 6.0, 8.0             # mm (v1.5: 8 mm gutters)
L_W = 150.0                        # mm: the left column (site map over the axo); the right column takes the rest
PANELS = {"site": ("L", 0.33), "axo": ("L", 0.67), "free": ("R", 0.60), "move": ("R", 0.40)}   # column, height share
ORDER = ["site", "axo", "free", "move"]   # top first within each column
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


def ink_box(got, tw):
    """v1.4: the box (page mm) of everything a page script drew; a clipped item counts only inside its clip's box"""
    cb = {}
    for k, v in got["clips"].items():
        pts = [q for R in (v[0] if v else []) for q in R]
        if pts:
            cb[k] = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))
    B = [1e18, 1e18, -1e18, -1e18]

    def add(b, c=None):
        if c in cb:
            b = (max(b[0], cb[c][0]), max(b[1], cb[c][1]), min(b[2], cb[c][2]), min(b[3], cb[c][3]))
            if b[0] > b[2] or b[1] > b[3]:
                return
        B[0], B[1], B[2], B[3] = min(B[0], b[0]), min(B[1], b[1]), max(B[2], b[2]), max(B[3], b[3])

    def pbox(P, h=0.0):
        return (min(q[0] for q in P) - h, min(q[1] for q in P) - h, max(q[0] for q in P) + h, max(q[1] for q in P) + h)
    for it in got["items"]:
        t = it[0]
        if t == "poly":
            P = [q for R in it[1] for q in R]
            if P:
                add(pbox(P, (it[4] or 0.0) / 2.0 if it[3] else 0.0), it[9])
        elif t == "line":
            if it[1]:
                add(pbox(it[1], (it[3] or 0.0) / 2.0), it[4])
        elif t == "text":
            if not it[1]:
                continue
            w = tw(it[1], it[4], bool(it[6]))
            x = it[2] - (w / 2.0 if it[7] == "C" else w if it[7] == "R" else 0.0)
            add((x, it[3] - 0.25 * it[4], x + w, it[3] + it[4]))
        elif t in ("mask", "soft"):
            add((it[4], it[5], it[4] + it[6], it[5] + it[7]), it[11])
    for jp, x, y, w, h in got["photos"]:
        add((x, y, x + w, y + h))
    if B[0] > B[2]:
        return (0.0, 0.0, got["w"], got["h"])
    return tuple(B)


SCALE_RE = re.compile(u"(?<![0-9.,])1 ?[:/] ?([0-9]{1,3}(?:,[0-9]{3})+|[0-9]{3,7})(?![0-9])")


def page_den(got):
    """v1.5: the page's map scale, from its first "1:N" / "1/N" word (None: no map scale on it)"""
    for it in got["items"]:
        if it[0] == "text" and it[1]:
            m = SCALE_RE.search(it[1])
            if m:
                return int(m.group(1).replace(u",", u""))
    return None


def round_den(d):
    step = 500 if d < 20000 else 1000 if d < 100000 else 5000
    return int(-(-d // step) * step)


def rescale_words(items, den, den2):
    """v1.5: every "1:den" / "1/den" word of a page rewritten as 1:den2"""
    def f(m):
        return u"1:%s" % format(den2, ",d") if int(m.group(1).replace(u",", u"")) == den else m.group(0)
    return [(it[:1] + (SCALE_RE.sub(f, it[1]),) + tuple(it[2:])) if it[0] == "text" and it[1] else it for it in items]


def best_layout(boxes):
    """v1.5: column width and the share of each column's height that make the smallest panel scale largest;
    boxes = {key: (bw, bh)} ink sizes; returns (L_W, {key: s}) """
    H = SHEET[1] - 2 * MARGIN
    cands = []
    for lw in range(90, 312, 2):
        widths = {"L": float(lw), "R": SHEET[0] - 2 * MARGIN - GAP - lw}
        sc = {}
        for side in ("L", "R"):
            ks = [k_ for k_ in ORDER if PANELS[k_][0] == side and k_ in boxes]
            hh = H - (len(ks) - 1) * GAP
            if len(ks) == 1:
                sc[ks[0]] = min(widths[side] / boxes[ks[0]][0], hh / boxes[ks[0]][1])
                continue
            if not ks:
                continue
            a_, b_ = ks[0], ks[1]
            opts = []
            for i in range(10, 91):
                f_ = i / 100.0
                sa = min(widths[side] / boxes[a_][0], f_ * hh / boxes[a_][1])
                sb = min(widths[side] / boxes[b_][0], (1 - f_) * hh / boxes[b_][1])
                opts.append((sa, sb))
            sc[side] = (a_, b_, opts)
        cands.append((lw, sc))
    # v1.6: every combination of the two columns' splits: the best smallest scale, then the most sheet covered
    area = lambda k_, s_: boxes[k_][0] * boxes[k_][1] * s_ * s_
    pool = []
    for lw, sc in cands:
        per = []
        for side, v in sc.items():
            if isinstance(v, tuple):
                a_, b_, opts = v
                per.append([((a_, sa), (b_, sb)) for sa, sb in opts])
            else:
                per.append([((side, v),)])
        for c1 in per[0]:
            for c2 in (per[1] if len(per) > 1 else [()]):
                d = dict(c1 + c2)
                pool.append((min(d.values()), sum(area(k_, s_) for k_, s_ in d.items()), lw, d))
    vbest = max(p_[0] for p_ in pool)
    v_, a_, lw, d = max((p_ for p_ in pool if p_[0] >= 0.95 * vbest), key=lambda p_: p_[1])
    return lw, d


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    ts = float(globals().get("text_scale") or 0.6)
    items, clips, photos = [], {}, []
    forms = {}
    H = SHEET[1] - 2 * MARGIN
    tops = {"L": SHEET[1] - MARGIN, "R": SHEET[1] - MARGIN}
    gots = {}
    for key in ORDER:                                    # each page made once, at its first-guess panel size
        side, share = PANELS[key]
        n_ = sum(1 for k_ in ORDER if PANELS[k_][0] == side)
        pw = L_W if side == "L" else SHEET[0] - 2 * MARGIN - GAP - L_W
        ph = share * (H - (n_ - 1) * GAP)
        got = run_page(key, newest(PAGES[key]), G, (pw / ts, ph / ts), log)
        if got:
            gots[key] = (got, ink_box(got, lib["text_w"]))
    boxes = dict((k_, (max(ib[2] - ib[0], 1.0), max(ib[3] - ib[1], 1.0))) for k_, (g_, ib) in gots.items())
    lw, sc = best_layout(boxes)                          # v1.5: the packing with the largest smallest scale
    log.append(u"layout: left column %.0f mm; panel scales %s" % (lw, u", ".join(
        u"%s %.2f" % (k_, sc[k_]) for k_ in ORDER if k_ in sc)))
    slot = {}
    for side in ("L", "R"):                              # v1.7: second pass, each page laid out for its real slot
        ks = [k_ for k_ in ORDER if PANELS[k_][0] == side and k_ in gots]
        if not ks:
            continue
        pw = float(lw) if side == "L" else SHEET[0] - 2 * MARGIN - GAP - lw
        hc = H - (len(ks) - 1) * GAP
        tot = sum(boxes[k_][1] * sc[k_] for k_ in ks)
        for k_ in ks:
            sh = hc * boxes[k_][1] * sc[k_] / tot
            n0 = len(log)
            nf0 = sum(1 for l in log if l.lstrip().startswith(u"FLAG"))
            got2 = run_page(k_, newest(PAGES[k_]), G, (pw / sc[k_], sh / sc[k_]), log)
            if not got2:
                del log[n0:]
                continue
            ib2 = ink_box(got2, lib["text_w"])
            bw2, bh2 = max(ib2[2] - ib2[0], 1.0), max(ib2[3] - ib2[1], 1.0)
            s2 = min(pw / bw2, sh / bh2)
            d1, d2 = page_den(gots[k_][0]), page_den(got2)
            nf = sum(1 for l in log[n0:] if l.lstrip().startswith(u"FLAG"))
            if nf > 0 or s2 < sc[k_] or (d1 and d2 and d2 > 1.5 * d1):   # v1.8: only a better page replaces pass 1
                del log[n0:]
                log.append(u"  pass 2 %s: slot %.0f x %.0f mm gave scale %.2f, map 1:%s, %d FLAG(s): pass 1 kept"
                           % (k_, pw, sh, s2, format(d2 or 0, ",d"), nf))
                continue
            log.append(u"  pass 2 %s: slot %.0f x %.0f mm, scale %.2f -> %.2f" % (k_, pw, sh, sc[k_], s2))
            gots[k_], boxes[k_], sc[k_] = (got2, ib2), (bw2, bh2), s2
    for key in ORDER:
        if key not in gots:
            continue
        got, ib = gots[key]
        side = PANELS[key][0]
        pw = float(lw) if side == "L" else SHEET[0] - 2 * MARGIN - GAP - lw
        x0 = MARGIN if side == "L" else MARGIN + lw + GAP
        s = sc[key]
        den = page_den(got)
        if den:                                          # v1.5: a round scale on the sheet, its words rewritten
            den2 = round_den(den / s)
            s = den / float(den2)
            got = dict(got, items=rescale_words(got["items"], den, den2))
            log.append(u"  panel %s: page 1:%s drawn at 1:%s" % (key, format(den, ",d"), format(den2, ",d")))
        bw, bh = boxes[key]
        ph = bh * s
        y0 = tops[side] - ph
        tops[side] = y0 - GAP
        ox, oy = x0 - ib[0] * s, y0 - ib[1] * s           # left- and top-aligned in its slot
        if True:
            it_, cl_, ph_ = place(got, key, ox, oy, s)
            pc = u"%s_panel" % key                           # v1.4: every unclipped shape / line cut to its panel
            cl_[pc] = [[[(x0, y0), (x0 + pw, y0), (x0 + pw, y0 + ph), (x0, y0 + ph)]]]
            it_ = [(it[:9] + (pc,) + tuple(it[10:])) if it[0] == "poly" and it[9] is None else
                   (it[:4] + (pc,) + tuple(it[5:])) if it[0] == "line" and it[4] is None else it for it in it_]
            nb = (ox + ib[0] * s, oy + ib[1] * s, ox + ib[2] * s, oy + ib[3] * s)
            if nb[0] < x0 - 0.3 or nb[1] < MARGIN - 0.3 or nb[2] > x0 + pw + 0.3 or nb[3] > y0 + ph + 0.3:
                log.append(u"FLAG: panel %s ink %.0f-%.0f x %.0f-%.0f mm reaches past its panel %.0f-%.0f x %.0f-%.0f"
                           % (key, nb[0], nb[2], nb[1], nb[3], x0, x0 + pw, y0, y0 + ph))
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
