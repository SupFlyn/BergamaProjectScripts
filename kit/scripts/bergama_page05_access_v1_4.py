# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE 05 ACCESS v1.4 (14 Nov 2026; v1.4 = Aras 16:27 UTC "the map on the right side is just repeating the information that is on the left side so please remove the map on the right hand side": one map (the transit part, which now carries the loop and its names); v1.3 = Aras 16:17 UTC "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN": both maps framed by site_alan turned flat (pages_common SiteMap, as the Basemap draws it), stacked full width at 1:7,500, loop stops outside the site shown as edge arrows, north arrow turned, legends flowed in columns under the maps; v1.2 = the transit part (v2.10+) draws the loop itself, before its names (run review: names sat on the copied loop), so no copy here; v1.1 = Aras 15:31 UTC "the bold connection between the heritage should stay there just like the old diagram": the heritage loop (bold red legs, numbered stops) also drawn on the transit map, under its transit symbols, taken from the heritage part: not drawn twice in code): slide 5 on ONE A3 landscape sheet: the public-transport map and
the heritage-loop map side by side, one shared legend for the ground they share.

Aras 14 Nov 15:25-15:27 UTC: "draw it in landscape and fit every drawing into A3's like the scale is not important";
"everything that we have in slide 2 gonna be single landscape A3 this applies to everything". Slide 5 holds the transit
map and the heritage loop (coordinator; REUSE_MAP no-repeat check), so both go on this one sheet.

Nothing is drawn twice (Aras 12:38 UTC "don't ever do the same job twice in two scripts"): this script runs the main of
the newest scripts/bergama_page_transit_v*.py and scripts/bergama_page_heritage_v*.py at the A3 scale, takes their map
items and legend rows, and lays them out:
  left   the transit map, its own legend rows under it (two columns)
  middle the heritage map, its own legend rows under it (two columns)
  right  the shared ground (MapBase) legend once, the notes, north arrow, scale bar
No sources on the sheet (Aras 15:23 UTC); they go to the log.

Outputs: Downloads/Bergama/output/bergama_page05_access/Access.pdf + .svg + review/ PNGs; output/presentation/5.pdf.
Reads: the two page scripts above, Data/bergama_pages_common.py and what they read (MapBase cache: press MapBase first).
Grasshopper: a Button on any input runs it; input `scale` (default 12,500: the two maps fit A3 side by side).
"""
import os, re, glob, time

VERSION = "v1.4"
SLIDE = 5
GH_LABEL = "Page05"
OUT_FOLDER = "bergama_page05_access"
LOG_NAME = "bergama_page05_access_log.txt"
GH_INPUTS = {"scale": "int 5000..25000 = 7500"}
COMMON = os.path.join("Data", "bergama_pages_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "Access"
PARTS = (("transit", os.path.join("scripts", "bergama_page_transit_v*.py")),)   # v1.4: one map
SHEET_W, SHEET_H = 420.0, 297.0     # A3 landscape, mm
MARGIN, GAP = 8.0, 5.0             # mm: sheet margin, gap under a map
TITLE_H = 9.0                       # mm above each map: its title
COL_N = 5                           # legend columns under the maps
LEG_TXT, LEG_ROW = 1.9, 1.3         # mm: legend text size, line spacing factor
WIRE_END = "# ---- Grasshopper wiring"


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


def newest(pattern):
    found = glob.glob(os.path.join(BERGAMA_ROOT, pattern))
    if not found:
        raise RuntimeError(u"no %s: run Bergama.bat once" % os.path.join(BERGAMA_ROOT, pattern))
    return max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])


def run_part(path, den, log):
    """the part script's main at scale den, its sheet and file writing caught: (map items, Map, sheet args)"""
    with open(path, encoding="utf-8") as f:
        code = f.read()
    code = code[:code.index(WIRE_END)] if WIRE_END in code else code
    ns = {"__name__": "bergama_page05_part", "scale": den}
    exec(compile(code, path, "exec"), ns)
    G = load_common()
    got = {}

    def sheet(M, K, lib, title, sub, legend, notes, credit):
        got.update(K=K, lib=lib, title=title, sub=sub, legend=legend, notes=notes)
        return []

    def write(lib, M, items, *a, **kw):
        got.update(M=M, items=list(items))
        return []
    G["pc_sheet"], G["pc_write"] = sheet, write
    G["Map"] = lambda D_, den_: G["pc_site_map"](den_, log)     # v1.3: the frame is site_alan
    ns["load_common"] = lambda: G
    res = ns["main"]()
    log.append(u"---- %s %s" % (os.path.basename(path), u"(its log)"))
    log.extend(l for l in res.split(u"\n") if l)
    got["G"] = G
    return got


def shift(items, dx, dy, cid_old, cid_new):
    """items moved by (dx, dy) mm; the clip id cid_old renamed cid_new (each map is cut to its own frame)"""
    out = []
    for it in items:
        t = it[0]
        if t == "poly":
            it = list(it)
            it[1] = [[(p[0] + dx, p[1] + dy) for p in R] for R in it[1]]
            if len(it) > 9 and it[9] == cid_old:
                it[9] = cid_new
        elif t == "line":
            it = list(it)
            it[1] = [(p[0] + dx, p[1] + dy) for p in it[1]]
            if it[4] == cid_old:
                it[4] = cid_new
        elif t == "text":
            it = list(it)
            it[2], it[3] = it[2] + dx, it[3] + dy
        else:
            continue
        out.append(tuple(it))
    return out


def legend_block(G, rows, x, y, w, tw, ink):
    """legend rows [(draw(x, y) | None, text)] from (x, y) down, width w; returns (items, y at the end)"""
    it = []
    for draw, label in rows:
        if draw is None:
            y -= 1.0
            it.append(G["T_"](label, x, y, LEG_TXT, ink, "legend", True))
            y -= LEG_TXT * 2.0
            continue
        it += draw(x + 5.0, y + 0.7)
        yy = y
        for ln in G["wrap"](label, LEG_TXT, w - 12.0, tw):
            it.append(G["T_"](ln, x + 11.5, yy, LEG_TXT, ink, "legend"))
            yy -= LEG_TXT * LEG_ROW
        y = min(y - 4.6, yy - 1.4)
    return it, y


def inside_only(items, M, cid, key, log):
    """Aras 16:17 UTC "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN": a line not cut by the clip is cut to the frame; a shape or
    text that leaves the frame is left out (counted in the log)"""
    out, gone = [], {}
    x0, y0, x1, y1 = M.box
    for it in items:
        if it[0] == "line" and it[4] != cid:
            for run in M.clip(it[1]):
                out.append(it[:1] + (run,) + it[2:])
            continue
        if it[0] == "poly" and not (len(it) > 9 and it[9] == cid):
            pts = [q for R in it[1] for q in R]
            if pts and not all(x0 - 0.05 <= q[0] <= x1 + 0.05 and y0 - 0.05 <= q[1] <= y1 + 0.05 for q in pts):
                gone[it[6]] = gone.get(it[6], 0) + 1
                continue
        out.append(it)
    if gone:
        log.append(u"%s: left out, outside site_alan: %s" % (key, u", ".join(u"%s %d" % kv for kv in sorted(gone.items()))))
    return out


def flow(G, blocks, x0, ytop, ybot, colw, ncol, tw, ink, log):
    """legend blocks [(header, rows)] flowed into ncol columns of width colw from ytop down to ybot"""
    it, col, y = [], 0, ytop
    for head, rows in blocks:
        rows = ([(None, head)] if head else []) + list(rows)
        for draw, label in rows:
            if draw is None:
                need = LEG_TXT * 3.0 + 4.6
            else:
                need = max(4.6, len(G["wrap"](label, LEG_TXT, colw - 14.0, tw)) * LEG_TXT * LEG_ROW + 1.4)
            if y - need < ybot and y < ytop - 0.1:
                col, y = col + 1, ytop
            if col >= ncol:
                log.append(u"FLAG: the legends need more than %d columns: %s and after left out" % (ncol, label))
                return it
            a, y = legend_block(G, [(draw, label)], x0 + col * colw, y, colw - 2.0, tw, ink)
            it += a
    return it


def main():
    t0 = time.time()
    log = []
    den = int(globals().get("scale") or 7500)
    parts = [(key, run_part(newest(pat), den, log)) for key, pat in PARTS]
    G = parts[0][1]["G"]
    lib, K = parts[0][1]["lib"], parts[0][1]["K"]
    ink, tw = K["ink"], lib["text_w"]
    M0 = parts[0][1]["M"]
    mw, mh = M0.mw, M0.mh
    x0 = (SHEET_W - mw) / 2.0
    if x0 < MARGIN - 0.1:
        log.append(u"FLAG: at 1:%s the site (%.0f mm) is wider than A3: set scale higher" % (format(den, ",d"), mw))
    items, clips = [], {}
    shared, own = [], {}
    for key, P in parts:                     # the ground rows both maps share: printed once
        rows, grp = [], None
        for draw, label in P["legend"]:
            if draw is None:
                grp = label
                if label == u"EXISTING: CONTEXT":
                    continue
            elif grp == u"EXISTING: CONTEXT":
                if label not in [l_ for _d, l_ in shared]:
                    shared.append((draw, label))
                continue
            rows.append((draw, label))
        own[key] = rows
    top = SHEET_H - MARGIN
    for i, (key, P) in enumerate(parts):
        M = P["M"]
        mt = top - TITLE_H
        dx, dy = x0 - M.box[0], mt - M.box[3]
        P["items"] = inside_only(P["items"], M, G["PC_CLIP"], key, log)
        G["pc_frame_check"](P["items"], M.box, log, tw)
        cid = u"map_" + key
        items += shift(P["items"], dx, dy, G["PC_CLIP"], cid)
        b = (x0, mt - mh, x0 + mw, mt)
        clips[cid] = [[[(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])]]]
        items.append(G["P_"]([[(b[0], b[1]), (b[2], b[1]), (b[2], b[3]), (b[0], b[3])]], None, ink, 0.25, "frame"))
        items.append(G["T_"](P["title"].upper(), x0, mt + 3.4, 4.0, ink, "title", True))
        items.append(G["T_"](P["sub"], x0 + tw(P["title"].upper(), 4.0, True) + 4.0, mt + 3.4, 2.2, ink, "title"))
        if i == 0:                           # north arrow + scale bar at the right end of the first title row
            k = 1000.0 / den
            bar = 250.0 if den <= 10000 else 500.0
            Lb = bar * k
            xb, yb = x0 + mw - Lb - 34.0, mt + 2.0
            items += G["pc_north_items"](x0 + mw - 4.0, mt + 4.6, 3.4, M.north, ink)
            for j in range(4):
                items.append(G["P_"]([[(xb + Lb * j / 4, yb), (xb + Lb * (j + 1) / 4, yb), (xb + Lb * (j + 1) / 4,
                                       yb + 1.2), (xb + Lb * j / 4, yb + 1.2)]], ink if j % 2 == 0 else "FFFFFF", ink,
                                     0.15, "north_scale"))
            items.append(G["T_"](u"0", xb, yb + 2.2, 1.9, ink, "north_scale", False, "C"))
            items.append(G["T_"](u"%d m" % bar, xb + Lb, yb + 2.2, 1.9, ink, "north_scale", False, "C"))
            items.append(G["T_"](u"1:%s" % format(den, ",d"), xb + Lb + 9.0, yb, 2.4, ink, "north_scale", True))
        top = mt - mh - GAP
    notes = [(lambda x, y: [], nt) for _k, P in parts for nt in P["notes"]]
    blocks = [(None, own["transit"]), (u"EXISTING: CONTEXT", shared), (u"NOTES", notes)]
    items += flow(G, blocks, x0, top - 2.0, MARGIN, mw / COL_N, COL_N, tw, ink, log)
    # write
    os.makedirs(OUT_DIR, exist_ok=True)
    pdf = None
    for ext, fn in ((".pdf", lib["write_pdf"]), (".svg", lib["write_svg"])):
        p = os.path.join(OUT_DIR, NAME + ext)
        try:
            p = fn(p, SHEET_W, SHEET_H, items, u"Slide 5: public transport and the heritage loop", clips) or p
            log.append(u"%s  %s (A3 landscape, 1:%s, %d objects)" % (p, time.strftime("%H:%M:%S"), format(den, ",d"),
                                                                   len(items)))
            if ext == ".pdf":
                pdf = p
        except Exception as ex:
            log.append(u"FLAG: %s not written (%s: %s)" % (p, type(ex).__name__, ex))
    if pdf:
        G["pc_review"](pdf, os.path.join(OUT_DIR, "review"), log)
        G["pc_present"](pdf, SLIDE, log)
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
