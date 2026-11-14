# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE01 AXO v2.2 (14 Nov 2026; v2.2 = slide 1 run 7: a tall empty band between the legend and the drawing: the drawing now sits 6 mm under the legend, the empty space left at the page foot; v2.1 = slide 1 review (run 5): the title "What is there" repeated Plan 01's title: now "Heights, heritage, water, green" (the booklet caption's own words), and the title + legend sit ABOVE the drawing), slide 1 (analysis): the booklet's page-3 axonometric ("What is
there · heights, heritage, water, green", selinus_board v65+ / its axonometric engine), only scaled down and recoloured.

Aras 14 Nov 16:15 UTC: "you had the proper axonometric drawing before why did you fucked it up only thing you needed to
do is to scale it down and change the colours". So v1-v1.6 (an axo of our own) are dropped and this script draws the
booklet drawing itself, from selinus_board's own cache of it (nothing redrawn, nothing read from a PDF):
  ~/Downloads/Bergama/cached/booklet/selinus_board/items.json, page p03, drawing sb_axo_what_is_there (mm, y up):
  every face, tree, road, label and the legend exactly as selinus_board exported them (Aras 12:38 UTC "if one script
  does that job cache it and make it usable by the next script"). Its p03 part is cached once in
  cached/bergama_page01_axo/p03_axo.json (re-read when items.json changes).
The two changes:
  SCALE: the drawing and its words scaled as one to the page (A3 landscape, or the slide's page_mm), legend under it.
  COLOURS: each building use class of the booklet (roof, its two wall shades and outline) takes a colour of the current
  palette (MapBase FAB / FAB_COM, the one palette source); the wall shades keep the booklet's light-to-dark steps.
  The purples (sacred, civic) are gone. Everything else (ground, water, trees, people) keeps its booklet colour.
No sources in the drawing (Aras 15:23 UTC). Outputs: output/bergama_page01_axo/WhatIsThereAxo.pdf / .svg, review PNGs.
Reads: Data/bergama_pages_common.py, the newest MapBase script (palette), selinus_board's items.json (above).
"""
import os, time, json

VERSION = "v2.2"
GH_LABEL = "Page01Axo"
OUT_FOLDER = "bergama_page01_axo"
LOG_NAME = "bergama_page01_axo_log.txt"
GH_INPUTS = {}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
SRC = os.path.join(BERGAMA_ROOT, "cached", "booklet", "selinus_board", "items.json")
CACHE = os.path.join(BERGAMA_ROOT, "cached", "bergama_page01_axo", "p03_axo.json")
DID = "sb_axo_what_is_there"
NAME = "WhatIsThereAxo"
A3 = (420.0, 297.0)
PT = 25.4 / 72.0                   # mm per pt
GROUND = "FAF8F1"                  # the booklet axo's ground colour: a see-through fill is mixed onto it
# booklet use class: (roof, lit wall, shaded wall, outline) as exported (read from items.json, 9 Nov run) -> the
# current palette entry (table, key) of MapBase
USE = [("residential", ("CCA363", "B9872F", "705426", "8F6304"), ("FAB", "regular")),
       ("commerce", ("734C17", "653E00", "3C2300", "4A2C01"), ("FAB_COM", "regular")),
       ("mixed", ("A67628", "926202", "593B01", "6C4803"), ("FAB_COM", "construction")),
       ("industry", ("847E75", "726B60", "44403A", "554E43"), ("FAB", "large")),
       ("civic", ("7F5B7B", "73476E", "432B41", "5A2E56"), ("FAB_COM", "large")),
       ("sacred", ("452842", "3F1B3C", "220E20", "310C2E"), ("FAB", "sacred")),
       ("ruins", ("84573E", "7A4423", "472917", "622B04"), ("FAB", "monument"))]


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


class Sheet(object):
    """what pc_sheet / pc_write need: box (page mm), w, h, den, k"""
    def __init__(self, box, w, h):
        self.box, self.w, self.h, self.den, self.k = box, w, h, 1.0, 1.0


def p03(log):
    """selinus_board's p03 axonometric: (drawing, texts, legend, caption), cached apart from the 104 MB items.json"""
    if not os.path.isfile(SRC):
        raise RuntimeError(u"%s missing: press selinus_board once (it writes the booklet items), then this" % SRC)
    mt = os.path.getmtime(SRC)
    try:
        with open(CACHE, encoding="utf-8") as f:
            c = json.load(f)
        if c.get("src_mtime") == mt:
            log.append(u"booklet p03 axo: cache %s (items.json of %s)" % (CACHE, c.get("run")))
            return c
    except Exception:
        pass
    with open(SRC, encoding="utf-8") as f:
        d = json.load(f)
    P = d["pages"]["p03"]
    dr = [it for it in P if it.get("id") == DID][0]
    tx = dict((it["id"], it) for it in P if it.get("kind") == "text")
    lg = [it for it in P if it.get("kind") == "legend" and it.get("drawing") == DID]
    c = {"src_mtime": mt, "run": d.get("run"), "version": d.get("version"), "extent": dr["extent"],
         "shapes": [s for L in dr["layers"] for s in L["shapes"]],
         "texts": [t for t in tx.values() if (t.get("anchor") or {}).get("drawing") == DID],
         "legend": [(e["swatch"], tx.get(e["text"], {}).get("string", u"")) for e in (lg[0]["entries"] if lg else [])],
         "caption": next((t["string"] for t in tx.values() if t.get("role") == "caption"), u"")}
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False)
    log.append(u"booklet p03 axo: read from %s (%s, run %s), cached in %s" % (SRC, d.get("version"), d.get("run"),
                                                                            CACHE))
    return c


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    K = G["pc_data"](log)["key"]
    MB = G["pc_mb_lib"](log)
    mix = MB["mixh"]
    page = tuple(globals().get("page_mm") or A3)
    c = p03(log)

    # ---- the colours: each old shade -> the palette colour darkened by the booklet's own step (luminance ratio)
    lum = lambda h: 0.2126 * int(h[0:2], 16) + 0.7152 * int(h[2:4], 16) + 0.0722 * int(h[4:6], 16) + 1.0
    RE = {}
    for nm, old, (tab, key) in USE:
        new = MB[tab][key]
        for sh in old:
            RE[sh] = new if sh == old[0] else mix(new, "000000", max(0.0, 1.0 - lum(sh) / lum(old[0])))
        log.append(u"colours: %s %s -> %s %s (%s)" % (nm, old[0], tab, key, new))
    rc = lambda h: RE.get(h, h) if h else h

    # ---- the legend rows (the booklet's, recoloured) and the page layout: legend columns under the drawing
    P_, L_, circle = G["P_"], G["L_"], G["circle"]
    rows = []
    for sw, txt in c["legend"]:
        col = rc(sw.get("colour"))
        if sw.get("kind") == "dash":
            rows.append((lambda x, y, col=col: [L_([(x - 4.5, y), (x + 4.5, y)], col, 0.25, "legend", (1.6, 0.9))],
                         txt))
        elif sw.get("kind") == "dot":
            rows.append((lambda x, y, col=col: [P_([circle(x, y, 1.2, 16)], col, None, 0.0, "legend")], txt))
        else:
            rows.append((lambda x, y, col=col: [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0), (x + 4.5, y + 2.0),
                                                     (x - 4.5, y + 2.0)]], col, None, 0.0, "legend")], txt))
    title, sub = u"Heights, heritage, water, green", u""      # v2.1: not Plan 01's "What is there" again
    W0, H0 = c["extent"][2] - c["extent"][0], c["extent"][3] - c["extent"][1]
    dry = Sheet((0.0, -5000.0, 0.0, 0.0), 0.0, 0.0)
    ncol, need = 1, 0.0
    for n_ in (4, 3, 2, 1):
        if n_ * G["PC_SIDE_MM"] + (n_ - 1) * 6.0 <= page[0] - 24.0:
            ys = [it[3] for it in G["pc_sheet"](dry, K, lib, title, sub, rows, [], u"", cols=n_)
                  if it[0] == "text" and it[8] in ("title", "legend")]
            ncol, need = n_, -min(ys) + 3.0
            break
    sd = min((page[0] - 24.0) / W0, (page[1] - 24.0 - need - 6.0) / H0)
    ox = (page[0] - W0 * sd) / 2.0 - c["extent"][0] * sd
    oy = page[1] - 12.0 - need - 6.0 - c["extent"][3] * sd   # v2.2: right under the legend
    T = lambda q: (ox + q[0] * sd, oy + q[1] * sd)
    box = (ox + c["extent"][0] * sd, oy + c["extent"][1] * sd, ox + c["extent"][2] * sd, oy + c["extent"][3] * sd)
    log.append(u"layout: page %.0f x %.0f mm, drawing %.0f x %.0f mm at %.2f of the booklet's, legend %d column(s)"
               % (page[0], page[1], W0 * sd, H0 * sd, sd, ncol))

    # ---- the drawing: every shape as exported, in its order, recoloured; see-through fills mixed onto the ground
    items, n_re = [], 0
    for s in c["shapes"]:
        lay = u"axo_" + (s.get("grp") or u"other/0").split(u"/")[0]
        lw = (s.get("width_pt") or 0.0) * PT * sd
        st = rc(s.get("stroke"))
        if s["t"] == "line":
            ds = s.get("dash_pt")
            items.append(("line", [T(q) for q in s["pts"]], st, lw, None, lay,
                          tuple(v * PT * sd for v in ds) if ds else 1))
            continue
        fi = rc(s.get("fill"))
        n_re += fi != s.get("fill") or st != s.get("stroke")
        op = s.get("opacity")
        if fi and op is not None and op < 1.0:
            fi = mix(fi, GROUND, 1.0 - op)
        items.append(("poly", [[T(q) for q in R] for R in s["rings"]], fi, st, lw, None, lay, 1, None, None))
    for t in c["texts"]:
        x, y = T(t["anchor"]["pt"])
        al = (t.get("positions") or [u"=L"])[0].replace(u"=", u"")
        items.append(("text", t["string"], x, y, t["size_pt"] * PT * sd, rc(t.get("colour") or "4A3F35"),
                      bool(t.get("bold")), al if al in (u"L", u"C", u"R") else u"L", u"axo_labels", None, None))
    log.append(u"drawing: %d shapes (%d recoloured), %d words, legend %d rows; booklet run %s (%s)" % (
        len(c["shapes"]), n_re, len(c["texts"]), len(rows), c.get("run"), c.get("version")))
    M = Sheet(box, page[0], page[1])
    Mc = Sheet((0.0, box[3] + 6.0, 4.0, page[1] - 12.0), page[0], page[1])
    items += [it for it in G["pc_sheet"](Mc, K, lib, title, sub, rows, [], u"", cols=ncol)
              if it[8 if it[0] == "text" else 6 if it[0] == "poly" else 5] not in ("north_scale", "frame")]
    G["pc_write"](lib, M, items, OUT_DIR, NAME, u"What is there, axonometric", log)
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
