# -*- coding: utf-8 -*-
"""Bergama Group 6: SLIDE 06 MASTERPLAN v1 (15 Nov 2026): slide 6, the masterplan of the whole working area with
the six node frames N1-N6 and the 12 section lines, on one A3 landscape.

Aras 15 Nov 16:15 UTC: "here is the newest and latest masterplan svg use it and replace it where needed"; 14:45 UTC
"we gonna use masterplan svg as the base of the maps" + the working-area dash as the topmost line; 17:06 UTC "pull
inside of the working area exactly from .svg like cut and paste" (pages_common v3.34 pc_masterplan pastes master.svg
inside the working area); 14:46 UTC section marks in Archicad's marker look (pc_cut_mark); 14 Nov 15:27 UTC one A3
per slide. Brief (ARCH 4410 PR II): slide 6 = 1:1,000 with the N1-N6 frames and the 12 section lines; the 2.8 km
strip is 2.8 m long at 1:1,000, so on one A3 it is drawn at the smallest round scale that fits (logged and printed
on the sheet as it is; FLAG).

Draws  the base map (MapBase, the quiet page look) under his masterplan (master.svg via the MasterplanBase cache,
       pasted inside the working area), the node frames (Data/section_lines.json "nodes", accent C07A2E, name at
       the frame), the 12 cuts (section_lines.json "lines", pc_cut_mark: A across the stream looks downstream, B
       along the bank looks at the stream), the working-area dash on top (pc_write), title, legend, north, scale bar.
Writes output/bergama_slide06_masterplan/Slide06_Masterplan.pdf + .svg + review/ PNGs; output/presentation/6.pdf.
Reads  Data/bergama_pages_common.py and what it reads (MapBase + MasterplanBase caches), Data/section_lines.json,
       Data/selinos_centreline.json (through pc_selinos_line).
"""
import os, re, json, math, time

VERSION = "v2"   # v2 (Aras 15 Nov 20:29 UTC "just putting masterplan would leave most of the page empty"; his rule NEVER SPLIT A DRAWING): the whole strip stays ONE drawing across the top; under it N1-N6 close-ups from the same master.svg at one larger scale (CLOSE_DEN, 3 x 2), each centred where its A and B cuts cross, with its frame and its two cuts; legend column at the right with his texture legend (colours as drawn on the page), north arrow and both scale bars
SLIDE = 6
GH_LABEL = "Slide06"
OUT_FOLDER = "bergama_slide06_masterplan"
LOG_NAME = "bergama_slide06_masterplan_log.txt"
GH_INPUTS = {}
COMMON = os.path.join("Data", "bergama_pages_common.py")
LINES_JSON = os.path.join("Data", "section_lines.json")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = "Slide06_Masterplan"
PAGE = (420.0, 297.0)                # A3 landscape, mm
MARGIN, TITLE_H = 12.0, 20.0         # mm: sheet margin; title band above the map
ACC = "C07A2E"                       # our moves (DIAGRAM_STYLE rule 5), as the node frames on the node pages
MB_LAYERS = {"ground", "areas", "parks", "contours", "streets", "water", "walls", "buildings", "bridges", "trees"}
BRIEF_DEN = 1000                     # the brief's scale for slide 6
CLOSE_DEN = 2500                     # v2: the node close-ups (3 x the strip's 1:7,500)
LEG_W, GAP = 88.0, 6.0               # v2: legend column width; gap between panels (mm)
# v2: his texture legend (Aras 15 Nov 18:12-18:17 UTC) -> the masterplan layer it is drawn from on this page
TEX_LEGEND = ((u"river", ("su", "ana_su")), (u"bridges", ("kopruler",)), (u"historic buildings", ("heritage", "kizil_avlu")),
              (u"our buildings (blue = glass)", ("desings",)), (u"timber decks", ("teras",)),
              (u"shading canopies", ("kanopi",)), (u"reed beds", ("su_bitkii",)),
              (u"stepped terraces into the river", ("begum_su_merdiven",)), (u"stone paving at the water", ("iskele_kenari",)))


def load_common():
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    ns = {"__name__": "bergama_pages_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), ns)
    return ns


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    D = G["pc_data"](log)
    K = dict(D["key"])
    INK, tm, tw = K["ink"], K["text_mm"], lib["text_w"]
    L_, P_, T_ = G["L_"], G["P_"], G["T_"]
    M0 = G["pc_site_map"](1000, log)
    den = int(math.ceil(M0.F.w * 1000.0 / (PAGE[0] - 2 * MARGIN) / 500.0) * 500)
    M = G["pc_site_map"](den, log)
    M.x0 = (PAGE[0] - M.mw) / 2.0
    M.y0 = PAGE[1] - MARGIN - TITLE_H - M.mh
    M.w, M.h = PAGE
    M.box = (M.x0, M.y0, M.x0 + M.mw, M.y0 + M.mh)
    log.append(u"FLAG scale: the brief asks 1:%s; the %.0f m strip fits one A3 at 1:%s (%.0f x %.0f mm), so it is "
               u"drawn and labelled 1:%s" % (format(BRIEF_DEN, ",d"), M.F.w, format(den, ",d"), M.mw, M.mh,
                                             format(den, ",d")))
    sk = G["pc_stroke_k"](M.mw, M.mh, log, u"masterplan")
    T = M.T
    # base map + his masterplan inside the working area
    MB = G["pc_mapbase"](M, K, log, MB_LAYERS, {"lc_light": 0.8, "water_hatch": None})
    items = MB[0]
    items += G["pc_masterplan"](M, log)
    items += G["pc_study"](M, K, log)
    # node frames
    with open(os.path.join(BERGAMA_ROOT, LINES_JSON), encoding="utf-8") as f:
        SL = json.load(f)
    lw_f = G["pc_stroke"](0.5, sk)
    for nd, v in sorted(SL["nodes"].items()):
        R = [T(p) for p in v["corners"]]
        for run in M.clip(R + [R[0]]):                   # cut to the map frame
            items.append(L_(run, ACC, lw_f, "node_frames"))
        top = max(R, key=lambda q: q[1])
        top = (min(max(top[0], M.box[0] + 15.0), M.box[2] - 15.0), min(top[1], M.box[3] - 4.0))
        items.append(T_(u"%s %s" % (nd, v["name"]), top[0], top[1] + 1.2, tm["label"], ACC, "node_frames", True, "C"))
    log.append(u"node frames: %s (section_lines.json %s)" % (u", ".join(sorted(SL["nodes"])), SL["what"][:3]))
    # section lines
    CL = G["pc_selinos_line"]()
    n_cut = 0
    for nm, (a, b) in sorted(SL["lines"].items()):
        mid = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
        i = min(range(len(CL)), key=lambda j: G["pc_dist"](CL[j], mid))
        if nm.endswith(u"-A"):                            # across the stream: looking downstream
            j = min(i + 1, len(CL) - 1)
            i0 = j - 1
            dl = (CL[j][0] - CL[i0][0], CL[j][1] - CL[i0][1])
        else:                                             # along the bank: looking at the stream
            dl = (CL[i][0] - mid[0], CL[i][1] - mid[1])
        q0, q1 = T(mid), T((mid[0] + dl[0], mid[1] + dl[1]))
        items += G["pc_cut_mark"](T(a), T(b), (q1[0] - q0[0], q1[1] - q0[1]), nm, layer="section_names",
                                  ts=tm["label"])
        n_cut += 1
    log.append(u"section lines: %d (A across the stream looks downstream, B along the bank looks at the stream)" % n_cut)
    # v2: N1-N6 close-ups under the strip, one larger scale, each a window of the same master.svg (never a split)
    clips = {"map": [[[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]]]}
    if getattr(M, "wa", None):
        clips["map_wa"] = clips["map"] + [[list(R) for R in M.wa]]
    pw = (PAGE[0] - 2 * MARGIN - LEG_W - 3 * GAP) / 3.0
    top_ = M.box[1] - 2 * GAP
    ph = (top_ - MARGIN - 2 * 5.0 - GAP) / 2.0
    n_p, n_drop = 0, [0]

    def inside_(it_, bx):
        if it_[0] == "text":
            return bx[0] <= it_[2] <= bx[2] and bx[1] <= it_[3] <= bx[3]
        pts = [q for R in it_[1] for q in R] if it_[0] == "poly" else it_[1] if it_[0] == "line" else []
        return bool(pts) and all(bx[0] - 0.1 <= q[0] <= bx[2] + 0.1 and bx[1] - 0.1 <= q[1] <= bx[3] + 0.1 for q in pts)
    for i_, (nd, v) in enumerate(sorted(SL["nodes"].items())[:6]):
        cx_ = MARGIN + (i_ % 3) * (pw + GAP)
        cy_ = top_ - 5.0 - ph - (i_ // 3) * (ph + 5.0 + GAP)
        Mi = G["pc_site_map"](CLOSE_DEN, log)
        ln_ = [SL["lines"].get(nd + u"-A"), SL["lines"].get(nd + u"-B")]
        cen = None
        if ln_[0] and ln_[1]:                            # where his two cuts cross
            (a1, a2), (b1, b2) = ln_
            d1, d2 = (a2[0] - a1[0], a2[1] - a1[1]), (b2[0] - b1[0], b2[1] - b1[1])
            den_ = d1[0] * d2[1] - d1[1] * d2[0]
            if abs(den_) > 1e-9:
                t_ = ((b1[0] - a1[0]) * d2[1] - (b1[1] - a1[1]) * d2[0]) / den_
                cen = (a1[0] + t_ * d1[0], a1[1] + t_ * d1[1])
        if cen is None:
            cen = (sum(q[0] for q in v["corners"]) / len(v["corners"]), sum(q[1] for q in v["corners"]) / len(v["corners"]))
        q_ = Mi.T(cen)
        Mi.x0 += cx_ + pw / 2.0 - q_[0]
        Mi.y0 += cy_ + ph / 2.0 - q_[1]
        Mi.w, Mi.h = PAGE
        Mi.box = (cx_, cy_, cx_ + pw, cy_ + ph)
        pid = u"n%d" % (i_ + 1)
        sub = G["pc_mapbase"](Mi, K, log, MB_LAYERS, {"lc_light": 0.8, "water_hatch": None})[0]
        sub += G["pc_masterplan"](Mi, log)
        sub += G["pc_study"](Mi, K, log)
        ren = {"map": pid, "map_wa": pid + u"_wa"}
        for it_ in sub:                                  # the window's own clips
            it_ = list(it_)
            j_ = 9 if it_[0] == "poly" and len(it_) > 9 else 4 if it_[0] == "line" else None
            if j_ is not None and it_[j_] in ren:
                it_[j_] = ren[it_[j_]]
            elif not inside_(it_, Mi.box):               # an unclipped piece of the whole site: only what is in
                n_drop[0] += 1                           # this window
                continue
            items.append(tuple(it_))
        ring_ = [[(Mi.box[0], Mi.box[1]), (Mi.box[2], Mi.box[1]), (Mi.box[2], Mi.box[3]), (Mi.box[0], Mi.box[3])]]
        clips[pid] = [ring_]
        clips[pid + u"_wa"] = [ring_] + [[list(R) for R in getattr(Mi, "wa", None) or []]] if getattr(Mi, "wa", None) else [ring_]
        R = [Mi.T(q) for q in v["corners"]]
        for run in Mi.clip(R + [R[0]]):
            items.append(L_(run, ACC, G["pc_stroke"](0.5, 1.0), "node_frames"))
        for nm in (nd + u"-A", nd + u"-B"):
            if nm not in SL["lines"]:
                continue
            a, b = SL["lines"][nm]
            runs = Mi.clip([Mi.T(a), Mi.T(b)])
            if not runs:
                continue
            p0, p1 = runs[0][0], runs[-1][-1]
            mid = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
            k_ = min(range(len(CL)), key=lambda j: G["pc_dist"](CL[j], mid))
            if nm.endswith(u"-A"):
                j = min(k_ + 1, len(CL) - 1)
                dl = (CL[j][0] - CL[j - 1][0], CL[j][1] - CL[j - 1][1])
            else:
                dl = (CL[k_][0] - mid[0], CL[k_][1] - mid[1])
            q0, q1 = Mi.T(mid), Mi.T((mid[0] + dl[0], mid[1] + dl[1]))
            items += G["pc_cut_mark"](p0, p1, (q1[0] - q0[0], q1[1] - q0[1]), nm, layer="section_names", ts=tm["label"])
        items.append(T_(u"%s %s" % (nd, v["name"]), cx_, cy_ + ph + 1.4, tm["label"], ACC, "node_frames", True))
        items.append(P_(ring_, None, INK, 0.25, "frame"))
        n_p += 1
    log.append(u"node close-ups: %d windows at 1:%s (%.0f x %.0f mm = %.0f x %.0f m), each centred where its A and B "
               u"cuts cross, the same master.svg as the strip; %d unclipped pieces outside the windows left out" % (n_p, format(CLOSE_DEN, ",d"), pw, ph,
                                                                   pw * CLOSE_DEN / 1000.0, ph * CLOSE_DEN / 1000.0, n_drop[0]))
    # title, legend, north arrow, scale bars
    it = []
    yt = PAGE[1] - MARGIN - tm["title"]
    it.append(T_(u"MASTERPLAN", MARGIN, yt, tm["title"], INK, "title", True))
    it.append(T_(u"The Selinos as a stepped, amphibious bed: the whole working area with the six nodes and the 12 "
                 u"section lines; below, the six nodes closer", MARGIN, yt - tm["sub"] * 1.6, tm["sub"], INK, "title"))
    rows = [(lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], ACC, lw_f, "legend")], u"node frame N1-N6"),
            (lambda x, y: [L_([(x - 4.5, y), (x + 4.5, y)], K["study"][0], K["study"][1], "legend", (2.4, 0.8))],
             u"working area"),
            (lambda x, y: G["pc_cut_mark"]((x - 4.5, y), (x + 4.5, y), (0.0, 1.0), u"", layer="legend",
                                           ts=tm["legend"]), u"section line (arrows: the way it looks)")]
    drawn = {}                                           # v2: colour of each legend layer AS DRAWN on this page
    for it_ in items:
        if it_[0] == "poly" and isinstance(it_[6], str) and it_[6].startswith(u"mp/"):
            for w_ in it_[6][3:].split(u"/"):
                if w_ not in drawn and (it_[2] or it_[3]):
                    drawn[w_] = (it_[2], it_[3])
    miss_ = []
    for label, keys in TEX_LEGEND:
        c_ = next((drawn[k_] for k_ in keys if k_ in drawn), None)
        if c_ is None:
            miss_.append(label)
            continue
        rows.append((lambda x, y, c=c_: [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0), (x + 4.5, y + 2.0), (x - 4.5, y + 2.0)]],
                                            c[0], c[1] or K["grey_line"], 0.15, "legend")], label))
    if miss_:
        log.append(u"FLAG legend: not drawn on this page, so not in the legend: %s" % u", ".join(miss_))
    rows += G["pc_mb_legend"]([r_ for r_ in MB[1] if u"WorldCover" not in r_[2]], K)
    lx = PAGE[0] - MARGIN - LEG_W
    y = top_ - 2.0
    for draw, label in rows:
        if y < MARGIN + 40.0:
            log.append(u"FLAG legend: %d row(s) did not fit the column" % (len(rows) - rows.index((draw, label))))
            break
        it += draw(lx + 5.0, y + 1.0)
        it.append(T_(label, lx + 13.0, y, tm["legend"], INK, "legend"))
        y -= 5.5
    cx, cy, r = lx + 8.0, MARGIN + 28.0, 5.5
    it += G["pc_north_items"](cx, cy, r, M.north, INK)
    for row_, (dd, nm_) in enumerate(((den, u"strip"), (CLOSE_DEN, u"close-ups"))):
        bar = 100.0 if dd <= 2500 else 250.0 if dd <= 6000 else 500.0
        Lb, xb, yb = bar * 1000.0 / dd, lx + 2.0, MARGIN + 12.0 - row_ * 9.0
        for i in range(4):
            it.append(P_([[(xb + Lb * i / 4, yb), (xb + Lb * (i + 1) / 4, yb), (xb + Lb * (i + 1) / 4, yb + 1.4),
                           (xb + Lb * i / 4, yb + 1.4)]], INK if i % 2 == 0 else "FFFFFF", INK, 0.15, "north_scale"))
        it.append(T_(u"0", xb, yb - 3.0, 2.0, INK, "north_scale", False, "C"))
        it.append(T_(u"%d m" % bar, xb + Lb, yb - 3.0, 2.0, INK, "north_scale", False, "C"))
        it.append(T_(u"%s 1:%s" % (nm_, format(dd, ",d")), xb + Lb + 6.0, yb, 2.8, INK, "north_scale", True))
    it.append(P_([[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]], None,
                 INK, 0.25, "frame"))
    if tw(u"MASTERPLAN", tm["title"], True) > PAGE[0]:
        log.append(u"FLAG title wider than the sheet")
    items += it
    M.box = (MARGIN, MARGIN, PAGE[0] - MARGIN, PAGE[1] - MARGIN)   # v2: the frame check over the whole sheet
    paths = G["pc_write"](lib, M, items, OUT_DIR, NAME, u"Masterplan, 1:%d" % den, log, clips=clips)
    pdfs = [p_ for p_ in paths if p_.lower().endswith(".pdf")]
    if pdfs:
        G["pc_present"](pdfs[0], SLIDE, log)
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
