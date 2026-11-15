# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE COMMON v1 (14 Nov 2026), the shared code of the new page scripts (one script per page).
Loaded by exec from Downloads/Bergama/Data/bergama_pages_common.py by bergama_page_transit_v*.py and
bergama_page_heritage_v*.py, so both maps have the SAME frame, scale, context and key (Aras 14 Nov 10:45 UTC: "this
diagram and that one ... should not collide with each other"; 10:51: "transit hubs and heritage loop is two different
slides").

What it gives:
  pc_root(), pc_data(log)            the root folder and Data/bergama_access_heritage.json (frame, stops, lines, key)
  pc_lib(log)                        the PDF / SVG writer of the newest Basemap script (bergama_basemap_v*.py)
  Map(D, den)                        the shared frame: survey m -> sheet mm (north up), sheet size, map box
  pc_mapbase(M, K, log)              the context: the one MapBase cache (press MapBase first), in a quiet look
  pc_study(M, D, log)                the study area (calisma_alan) from the Basemap cache, dash-dot
  pc_lines / pc_stops / pc_hubs ...  the transit layer (used fully on the transit page, greyed on the heritage page)
  pc_heritage(...)                   the heritage places (numbered on the heritage page, dots on the transit page)
  Labels                             name placement that avoids every symbol and name already placed (never drops)
  pc_sheet(...)                      title, legend, north + scale, credit round the map
  pc_write(...)                      PDF + SVG + review PNGs (Aras 14 Nov 10:44: "all scripts should produce PNG's
                                     aswell which should be optimized for your viewing": trimmed, 200 ppi, tiles of
                                     at most 1400 px so nothing is scaled down when read)
Items are the Basemap writer's tuples (page mm, y up):
  ("poly", rings, fill, stroke, lw, None, layer, 1, None, None)
  ("line", pts, stroke, lw, None, layer, 1 | (on mm, off mm))
  ("text", s, x, y, size mm, colour, bold, align "L"|"C"|"R", layer, angle | None, None)
"""
import os, re, json, math, time, glob

PC_VERSION = "v3.36"  # v3.36 (Aras 15 Nov 20:45-20:50 UTC "many of the things from masterplan is missing", "river fill is failed ... we lost ground fills", "take chromium svg reader"): pc_masterplan pastes master.svg as the laptop's Chromium (Edge / Chrome headless) prints it to PDF (pc_mp_print, once per master.svg), placed in the page PDF as a form cut to the working area at the masterplan's place in the drawing order (pc_mp_place, PyMuPDF) and as a linked image in the SVG; without a browser or PyMuPDF the vector pieces stay (FLAG); v3.35 (Aras 15 Nov 19:48 UTC "much much faster"): pc_fast_load, the MapBase and MasterplanBase caches parsed once a Rhino session (marshal copy in sticky, same values and log lines); v3.34 v3.34 (Aras 15 Nov 17:06-17:07 UTC "pull inside of the working area exactly from .svg like cut and paste" / "Make that for every drawing except slide 1", standing): pc_masterplan pastes master.svg inside the working area only: every layer (his existing ev-yol too), his own colours, cut to the working-area outline (clip PC_CLIP_WA = the map frame AND the working area, even-odd), over a paper-white fill of the working area that hides the base map; outside it each page keeps its own context; M.wa keeps the page rings and pc_write adds the clip; paste=False = the v3.29 behaviour; v3.33 (Aras 15 Nov 15:57 UTC "make these blue and red lines thinner like scale the lines according to the drawing size please across all drawings"): pc_stroke_k(w, h) = the stroke factor of a drawing w x h mm (sqrt of its area over PC_STROKE_REF, 0.35-1.0), pc_stroke(lw, k) applies it; v3.32 v3.32 (Aras 15 Nov 14:46 + his Archicad S-01 screenshot 15:02 UTC): pc_cut_mark in Archicad's section marker look (filled triangle on the cut at each end pointing the view, thin stub + dot + dash inward, name turned along the cut beyond the end, regular weight); v3.31 v3.31 (Aras 15 Nov 14:56 UTC "center the numbers in the boundries", standing): pc_text_c centres a mark's letters by their true Helvetica widths (no 5 % bold estimate); pc_cut_mark names use it; v3.30: pc_photos takes PNGs (SVG mime by extension) and an optional 6th item True = placed UNDER the drawing (PDF overlay off; SVG first in the file), for Page01Axo v4's Rhino 3D capture; v3.29 (Aras 15 Nov 14:45 UTC): pc_write puts the working-area dashes (layer study_area) on top of every other item ("make our working area dashed line as the most foreground line"); pc_masterplan draws master.svg (MasterplanBase cache, vector) on a map, for maps that use his masterplan as their base; v3.28: pc_text_c, a mark letter centred on its glyph box (Helvetica cap height 0.718 em: baseline = centre - 0.359 x size; Aras 15 Nov 13:50 UTC "letters are not centered in the boxes"); the loop badge numbers use it; v3.27: no white box behind any name (Aras 15 Nov 13:44 UTC "dont have a opaque background for texts in any single of the drawings"): Labels.put halo = pc_halo, a thin white text-shaped outline (8 white copies 0.1-0.25 mm round the name), no box; v3.26: pc_mapbase logs the fill rings read / in view per layer (MapBase v1.8 mb_fill_log; Aras 07:46 "you might be skipping somewhere in the fills"); v3.25: pc_mapbase a05 bridges a warm dark grey 7A7468 at 0.18 mm (run 1: black 0.3 mm bridge lines were the heaviest ink on the pale base); v3.24: pc_mapbase a05 streets a pale warm grey F5F3EE (MapBaseCheck run 1: white streets on white houses read as one white mass in the old town; houses stay white), the street-edge lines cut to the network (MapBase v1.7); v3.23: pc_mapbase context make-up (Aras 15 Nov 06:03-06:05 "too many stray lines ... houses fills are overlapping ... Roads are not clear"; "thousand times better as house designs" = the 13 Nov A05 house look): houses white with a pale outline (MapBase v1.6 adds the crisp grey shadow to the lower left and drops wall / edge pieces under 3 m); streets white on a darker ground with darker edges; walls lighter; style key "a05": False keeps the old look; v3.22: pc_dg_kit to DIAGRAM_STYLE v2 (ground 3 x other weights, pale-accent terraces, arches silhouette);  v3.21: v3.21: pc_dg_kit dashes at item[6] (Basemap writer), dash_at=4 for the Sections writer;  v3.20: v3.20: pc_dg_kit, the diagram kit of library/diagram_style/DIAGRAM_STYLE.md (Aras 21:30 UTC "all the diagrams are awful"); v3.19: v3.18 undone (the writer keeps a line's clip at item[4]: those lines were really unclipped); v3.17: SiteMap ring + b (survey box), pc_site_den, pc_north_deg, pc_sheet cols + span (legend columns beside a site_alan strip); v3.16: pc_loop names=True (stop names on the map), every stop outside the frame gets an edge arrow, the stream walk in either loop order (loop numbered from Asklepion, Aras 16:26); v3.15: SiteMap / pc_site_map (the map frame = site_alan turned flat, Aras 16:17 UTC "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN"), pc_loop edge arrows to stops outside it, pc_north_items; v3.14: pc_cut_mark = two end arrows, no line between (Aras 16:05 UTC); v3.13: v3.13: pc_mp_data (MasterplanBase: the masterplan SVG cached in survey m); v3.12: pc_cut_mark, the R01 cut symbol (two arrows, Aras 15:37 UTC); v3.11: pc_loop (the heritage loop, one code for the heritage and the transit map; Aras 15:31) and pc_station_name; v3.10: pc_a3_den / pc_a3 (a map page fitted and centred on A3 or a slide panel, Aras 15:25-15:27 UTC); v3.9: no sources in the drawings (Aras 15:23 UTC): pc_nosrc on MapBase legend rows, empty credit skipped; v3.8: a name with no free place goes where it overlaps least (run 7); v3.7: Labels.block_line / block_items (names keep off lines: run 6 review); v3.6: the outside Python runs hidden (no console window, Aras 14 Nov 12:57 UTC); v3.5: frame check skips items with any clip id; pc_mb_lib (MapBase as a library, any projection), pc_sheet north angle, pc_photos (JPEGs into PDF / SVG), pc_write photos / clips; v3.3: pc_frame_check (FLAG map ink outside the map frame); v3.2: context houses cut to the map frame
PC_NOWIN = 0x08000000 if os.name == "nt" else 0   # v3.6: CREATE_NO_WINDOW for the review-PNG / photo subprocesses
PC_DATA = os.path.join("Data", "bergama_access_heritage.json")
PC_CENTRE = os.path.join("Data", "selinos_centreline.json")
PC_LIB_GLOB = os.path.join("scripts", "bergama_basemap_v*.py")
PC_LIB_END = "# ================================================================ main"
PC_STUDY_CACHE = os.path.join("cached", "bergama_basemap", "basemap_layers.json")
PC_CACHE_DIR = os.path.join("cached", "bergama_pages")
PC_MB_GLOB = os.path.join("scripts", "bergama_mapbase_v*.py")
PC_MB_END = "\n# ================================================================ main\n"
PC_CLIP = "map"               # v3.3: the clip id of the map frame (MapBase items are cut to it in the PDF / SVG)
PC_MARGIN_MM = 12.0          # sheet margin round the map
PC_SIDE_MM = 95.0            # the column right of the map: title, legend, notes
PC_PNG_PPI = 200
PC_PNG_TILE = 1400           # px: largest side of one review tile


def pc_root():
    return os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def pc_data(log):
    p = os.path.join(pc_root(), PC_DATA)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    with open(p, encoding="utf-8") as f:
        D = json.load(f)
    log.append(u"data: %s (%d stops, %d lines, %d heritage places)" % (p, len(D["stops"]), len(D["routes"]),
                                                                      len(D["heritage"])))
    return D


def pc_lib(log):
    """the PDF/SVG writer and text widths of the newest Basemap script (everything above its main)"""
    found = glob.glob(os.path.join(pc_root(), PC_LIB_GLOB))
    if not found:
        raise RuntimeError(u"no %s: run Bergama.bat once, then press again" % os.path.join(pc_root(), PC_LIB_GLOB))
    src_ = max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])
    with open(src_, encoding="utf-8") as f:
        code = f.read()
    if PC_LIB_END not in code:
        raise RuntimeError(u"%s has no line %r" % (src_, PC_LIB_END))
    ns = {"__name__": "bergama_basemap_lib"}
    exec(compile(code[:code.index(PC_LIB_END)], src_, "exec"), ns)
    for need in ("write_pdf", "write_svg", "text_w"):
        if need not in ns:
            raise RuntimeError(u"%s has no %s: update the kit (Bergama.bat)" % (src_, need))
    PC_STATE["to_survey"] = ns.get("to_survey")
    PC_STATE["lib"] = ns                              # v3.15: for pc_site_map (Frame, FRAME_COPY)
    log.append(u"drawing code: %s (%s %s)" % (src_, ns.get("GH_LABEL"), ns.get("VERSION")))
    return ns


# ================================================================ the shared frame
class Map(object):
    """north up (survey y = north; the survey grid lies within 0.2 deg of true north here: Helmert turn 0.09 deg,
    grid convergence about 0.11 deg, calculated from GEO in the Basemap script and (lon - 27) x sin(lat))"""

    def __init__(self, D, den):
        self.den = float(den)
        self.k = 1000.0 / self.den
        b = D["box"]
        self.b = b
        self.mw, self.mh = (b[2] - b[0]) * self.k, (b[3] - b[1]) * self.k
        self.x0, self.y0 = PC_MARGIN_MM, PC_MARGIN_MM
        self.w = self.x0 + self.mw + 8.0 + PC_SIDE_MM + PC_MARGIN_MM
        self.h = self.y0 + self.mh + PC_MARGIN_MM
        self.box = (self.x0, self.y0, self.x0 + self.mw, self.y0 + self.mh)

    def T(self, p):
        return (self.x0 + (p[0] - self.b[0]) * self.k, self.y0 + (p[1] - self.b[1]) * self.k)

    def inside(self, q, m=0.0):
        return self.box[0] + m <= q[0] <= self.box[2] - m and self.box[1] + m <= q[1] <= self.box[3] - m

    def clip(self, Q):
        """a sheet polyline cut to the map box: list of runs (Liang-Barsky per segment)"""
        x0, y0, x1, y1 = self.box
        runs, cur = [], []
        for a, b in zip(Q, Q[1:]):
            dx, dy = b[0] - a[0], b[1] - a[1]
            t0, t1, ok = 0.0, 1.0, True
            for p_, q_ in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
                if p_ == 0:
                    if q_ < 0:
                        ok = False
                        break
                    continue
                t = q_ / p_
                if p_ < 0:
                    t0 = max(t0, t)
                else:
                    t1 = min(t1, t)
                if t0 > t1:
                    ok = False
                    break
            if not ok:
                if len(cur) > 1:
                    runs.append(cur)
                cur = []
                continue
            pa = (a[0] + t0 * dx, a[1] + t0 * dy)
            pb = (a[0] + t1 * dx, a[1] + t1 * dy)
            if not cur or abs(cur[-1][0] - pa[0]) > 1e-6 or abs(cur[-1][1] - pa[1]) > 1e-6:
                if len(cur) > 1:
                    runs.append(cur)
                cur = [pa]
            cur.append(pb)
            if t1 < 1.0:
                runs.append(cur)
                cur = []
        if len(cur) > 1:
            runs.append(cur)
        return runs


def pc_dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def circle(cx, cy, r, n=32):
    return [(cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def L_(pts, col, lw, layer, dash=None):
    return ("line", [tuple(p) for p in pts], col, lw, None, layer, dash if dash else 1)


def P_(rings, fill, stroke, lw, layer):
    return ("poly", [[tuple(p) for p in R] for R in rings], fill, stroke, lw, None, layer, 1, None, None)


def T_(s, x, y, size, col, layer, bold=False, align="L"):
    return ("text", s, x, y, size, col, bold, align, layer, None, None)


PC_CAP = 0.359                                       # v3.28: half the Helvetica / Helvetica-Bold cap height (718 / 1000 em)


# v3.31 (Aras 15 Nov 14:56 UTC "center the numbers in the boundries ... check the whole presentation"): the true
# Helvetica-Bold / Helvetica advance widths (Adobe AFM, 1/1000 em) of the characters marks carry; the writers' text_w
# adds 5 % for bold, which pushed a centred bold mark left, so marks no longer rely on it
PC_AFM_B = dict(zip(u"ABCDEFGHIJKLMNOPQRSTUVWXYZ", (722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722,
                                                    778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611)))
PC_AFM_R = dict(zip(u"ABCDEFGHIJKLMNOPQRSTUVWXYZ", (667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
                                                    778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611)))
for _d in (PC_AFM_B, PC_AFM_R):
    _d.update({u"-": 333, u".": 278, u"·": 278, u" ": 278, u"İ": 278, u"Ş": 667, u"Ç": 722,
               u"Ö": 778, u"Ü": 722})


def pc_mark_w(s, size, bold=True):
    """v3.31: page mm width of a mark's text in Helvetica(-Bold) by its AFM widths (digits 556 in both)"""
    afm = PC_AFM_B if bold else PC_AFM_R
    return sum(556 if ch.isdigit() else afm.get(ch, 611 if bold else 556) for ch in s) / 1000.0 * size


def pc_text_c(s, cx, cy, size, col, layer, bold=True):
    """v3.28: a letter / number centred on (cx, cy) by its glyph box (capitals and digits), not by its baseline: for marks
    (badges, tiles, rings, boxes). v3.31: still centre-aligned at about cx (code that finds marks by x keeps working), but
    x is corrected by half the gap between the writer's width estimate and the true AFM width, so the PDF glyphs sit
    exactly on cx"""
    s = u"%s" % s
    tw = (PC_STATE.get("lib") or {}).get("text_w")
    dx = (tw(s, size, bold) - pc_mark_w(s, size, bold)) / 2.0 if tw else 0.0
    return T_(s, cx + dx, cy - PC_CAP * size, size, col, layer, bold, "C")


def pc_halo(s, x, y, size, bold, align, layer, col="FFFFFF"):
    """v3.27 (Aras 15 Nov 13:44 UTC: no opaque background behind text): a knockout halo shaped like the letters, 8 copies
    of the name in col a hair round (x, y), drawn before the name itself; no box"""
    r = min(0.25, max(0.1, size * 0.08))
    return [T_(s, x + r * dx, y + r * dy, size, col, layer, bold, align)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7))]


def offset_line(Q, d):
    """a sheet polyline moved d mm to its left (mitred, the miter capped at 2 x d)"""
    if abs(d) < 1e-9 or len(Q) < 2:
        return list(Q)
    out = []
    n = len(Q)
    for i in range(n):
        a = Q[max(i - 1, 0)]
        b = Q[min(i + 1, n - 1)]
        if i == 0:
            a, b = Q[0], Q[1]
        elif i == n - 1:
            a, b = Q[-2], Q[-1]
        if i in (0, n - 1):
            dx, dy = b[0] - a[0], b[1] - a[1]
            L = math.hypot(dx, dy) or 1.0
            out.append((Q[i][0] - dy / L * d, Q[i][1] + dx / L * d))
            continue
        p0, p1, p2 = Q[i - 1], Q[i], Q[i + 1]
        d1 = (p1[0] - p0[0], p1[1] - p0[1])
        d2 = (p2[0] - p1[0], p2[1] - p1[1])
        l1, l2 = math.hypot(*d1) or 1.0, math.hypot(*d2) or 1.0
        n1 = (-d1[1] / l1, d1[0] / l1)
        n2 = (-d2[1] / l2, d2[0] / l2)
        m = (n1[0] + n2[0], n1[1] + n2[1])
        lm = math.hypot(*m)
        if lm < 1e-6:
            out.append((p1[0] + n1[0] * d, p1[1] + n1[1] * d))
            continue
        m = (m[0] / lm, m[1] / lm)
        c = m[0] * n1[0] + m[1] * n1[1]
        s = d / max(c, 0.5)
        out.append((p1[0] + m[0] * s, p1[1] + m[1] * s))
    return out


def ticked(Q, col, lw, every, tick, layer):
    """a line with short ticks across it every `every` mm (the cable car, as the old heritage page)"""
    it = [L_(Q, col, lw, layer)]
    acc = every / 2.0
    for a, b in zip(Q, Q[1:]):
        L = pc_dist(a, b)
        if L <= 0:
            continue
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        t = acc
        while t < L:
            px, py = a[0] + ux * t, a[1] + uy * t
            it.append(L_([(px - uy * tick, py + ux * tick), (px + uy * tick, py - ux * tick)], col, lw * 0.8, layer))
            t += every
        acc = t - L
    return it


def arrow_head(a, b, col, size, layer):
    """a filled triangle at b pointing from a to b"""
    L = pc_dist(a, b) or 1.0
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    bx, by = b[0] - ux * size, b[1] - uy * size
    return P_([[b, (bx - uy * size * 0.45, by + ux * size * 0.45), (bx + uy * size * 0.45, by - ux * size * 0.45)]],
              col, None, 0.0, layer)


# ================================================================ v3.3: the one base map (MapBase), quiet look
# Aras 14 Nov 12:16 UTC: "also please update all maps to include every detail, and top of the map, data is missing
# please fill in that"; coordinator 12:18: every map draws from the one MapBase script, each page keeps its own styling.
def pc_mb_lib(log):
    """v3.5: the newest MapBase script as a library (mb_load, mb_draw, MB_STYLE, FAB ...)"""
    found = glob.glob(os.path.join(pc_root(), PC_MB_GLOB))
    if not found:
        raise RuntimeError(u"no %s: run Bergama.bat once" % os.path.join(pc_root(), PC_MB_GLOB))
    src_ = max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])
    with open(src_, encoding="utf-8") as f:
        code = f.read()
    if PC_MB_END not in code:
        raise RuntimeError(u"%s has no main line" % src_)
    ns = {"__name__": "bergama_mapbase_lib"}
    exec(compile(code[:code.index(PC_MB_END)], src_, "exec"), ns)
    ns["BERGAMA_ROOT"] = pc_root()
    ns["_pc_src"] = src_                              # v3.35: the library file, part of pc_fast_load's key
    log.append(u"base map: %s (%s %s)" % (src_, ns.get("GH_LABEL"), ns.get("VERSION")))
    return ns


def pc_fast_load(tag, src_, files, load, log):
    """v3.35 (Aras 15 Nov 19:48 UTC "optimize the scripts to be much much faster"): a cache read once per Rhino
    session. The first page parses it as before (load(log)); the parsed result is kept as marshal bytes in Rhino's
    sticky, keyed by the library script and each file's size + time, and the next page gets a fresh identical copy
    (same values, same log lines) without parsing the JSON again. Any change to a file or the library -> parsed
    again; a load with a FLAG line is never kept; outside Rhino nothing is kept"""
    import marshal
    try:
        import scriptcontext as _scf
        st = _scf.sticky
    except Exception:
        return load(log)
    try:
        k = [src_, os.stat(src_).st_mtime_ns]
        for p in files:
            s_ = os.stat(p) if os.path.isfile(p) else None
            k.append([p, s_.st_size if s_ else None, s_.st_mtime_ns if s_ else None])
    except Exception:
        return load(log)
    hit = st.get("bergama_fast_" + tag)
    if hit and hit[0] == k:
        log.extend(hit[2])
        return marshal.loads(hit[1])
    n0 = len(log)
    C = load(log)
    lines = log[n0:]
    if C is not None and not any(u"FLAG" in l for l in lines):
        try:
            st["bergama_fast_" + tag] = (k, marshal.dumps(C), list(lines))
        except Exception:
            st.pop("bergama_fast_" + tag, None)
    return C


def pc_mb_data(log):
    """v3.5: (MapBase library, its cache), loaded once a run (v3.35: parsed once a Rhino session, pc_fast_load)"""
    if "mb" not in PC_STATE:
        ns = pc_mb_lib(log)
        R_ = ns["BERGAMA_ROOT"]
        C = pc_fast_load("mb", ns["_pc_src"], [
            os.path.join(R_, "cached", "bergama_mapbase", ns["MB_FILE"]), os.path.join(R_, ns["LC_FILE"]),
            os.path.join(R_, ns["VEG_FILE"])], ns["mb_load"], log)
        if C is None:
            raise RuntimeError(u"press MapBase once (it caches the base map every page draws), then this page")
        PC_STATE["mb"] = (ns, C)
    return PC_STATE["mb"]


PC_MP_GLOB = os.path.join("scripts", "bergama_masterplanbase_v*.py")


def pc_mp_data(log):
    """v3.10: (MasterplanBase library, its cache): Aras's masterplan SVG in survey m (press MasterplanBase once);
    draw with ns["mp_draw"](C, items, T, k, lim, cid, layers, style)"""
    if "mp" not in PC_STATE:
        found = glob.glob(os.path.join(pc_root(), PC_MP_GLOB))
        if not found:
            raise RuntimeError(u"no %s: run Bergama.bat once" % os.path.join(pc_root(), PC_MP_GLOB))
        src_ = max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])
        with open(src_, encoding="utf-8") as f:
            code = f.read()
        ns = {"__name__": "bergama_masterplanbase_lib"}
        exec(compile(code[:code.index(PC_MB_END)], src_, "exec"), ns)
        ns["BERGAMA_ROOT"] = pc_root()
        C = pc_fast_load("mp", src_, [os.path.join(pc_root(), "cached", ns["OUT_FOLDER"], ns["MP_FILE"])],
                         ns["mp_load"], log)              # v3.35: parsed once a Rhino session
        if C is None:
            raise RuntimeError(u"press MasterplanBase once (it caches the masterplan every page draws), then this page")
        PC_STATE["mp"] = (ns, C)
    return PC_STATE["mp"]


def pc_mapbase(M, K, log, layers=None, style=None):
    """(items, legend rows [(kind, hex, text)], counts) of the newest MapBase cache in this page's quiet look, cut to
    the map frame (clip PC_CLIP); stops when MapBase has not been pressed (v3.4: no second context of our own).
    v3.5: layers = mb_draw's layer set (None = all), style = keys over the quiet look"""
    ns, C = pc_mb_data(log)
    mix, paper = ns["mixh"], ns["PAPER"]
    soft = lambda c, t: mix(c, paper, t) if c else c
    S = ns["MB_STYLE"]
    bl = K["building"][1]
    st = {"grain": False, "ground": "F4F2EC", "lc_light": 0.7,
          "veg": dict((k_, v) for k_, v in S["veg"].items()),
          "areas": dict((k_, soft(v, 0.55)) for k_, v in S["areas"].items()),
          "landuse": dict((k_, soft(v, 0.5)) for k_, v in S["landuse"].items()),
          "fab": dict((k_, "E2DED6") for k_ in S["fab"]), "fab_com": dict((k_, "E2DED6") for k_ in S["fab_com"]),
          "edge_dark": 0.6, "ink": bl, "street": "FFFFFF", "street_edge": "CFCBC0", "path": "C4BFB2",
          "water": soft(S["water"], 0.45), "water_line": K["water"][0], "wall": "ABA69A", "osm_wall": "ABA69A",
          "her_wall": "A07A62", "tree": "9EA97F", "contour": "D2CABA", "contour_index": "B5AA95",
          "lw": {"hair": 0.06, "osm_wall": 0.08, "contour": 0.07, "contour_index": 0.14}}
    st["veg"] = dict((k_, soft(v, 0.3)) for k_, v in st["veg"].items())
    st["fab"]["monument"] = st["fab_com"]["monument"] = "D8C8BC"
    st["fab"]["sacred"] = st["fab_com"]["sacred"] = "D8C8BC"
    a05 = (style or {}).get("a05", True)
    if a05:                                              # v3.23: the A05 house look + readable streets
        st["fab"] = dict((k_, "FFFFFF") for k_ in S["fab"])
        st["fab_com"] = dict((k_, "FFFFFF") for k_ in S["fab_com"])
        for k_ in ("monument", "sacred"):
            st["fab"][k_] = st["fab_com"][k_] = "F2E6DC"
        st.update({"ground": "ECE9E1", "street": "F5F3EE", "street_edge": "9E9889", "edge_dark": 1.0, "ink": "D0D0D0",
                   "wall": "CDC8BC", "osm_wall": "CDC8BC"})
        st["lw"] = dict(st["lw"], edge=0.12, wall=0.05, osm_wall=0.05, hair=0.04)
        st["bridge"] = "7A7468"
        st["lw"]["bridge"] = 0.18   # outline 0.08 mm = PlanBase building_plan
    st["a05"] = a05                                      # MapBase v1.6+ draws the shadows, drops the stray pieces
    st.update(dict((k_, v) for k_, v in (style or {}).items() if k_ != "a05"))
    items = []
    cnt = ns["mb_draw"](C, items, M.T, M.k, M.box, PC_CLIP, st, layers)
    rows = ns["mb_legend"](C, cnt, st)
    if cnt.get("buildings"):
        rows.append(("box", "FFFFFF" if a05 else "E2DED6",
                     u"Buildings (survey, else OSM); monuments and mosques a shade warmer"))
    if cnt.get("walls") or cnt.get("walls_osm"):
        rows.append(("line", st["wall"], u"Walls and retaining walls (survey; OSM where the survey has none)"))
    if cnt.get("heritage_walls"):
        rows.append(("line", st["her_wall"], u"Ancient and city walls (survey and OSM)"))
    if cnt.get("trees_osm"):
        rows.append(("dot", st["tree"], u"Single trees (OSM)"))
    log.append(u"base map drawn: " + u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())))
    if "mb_fill_log" in ns:
        ns["mb_fill_log"](log)
    return items, rows, cnt


PC_SRC_WORDS = r"OSM|ESHOT|survey|surveyed|WorldCover|GLO-30|image|MapBase|Copernicus|Wikipedia|calculated"


def pc_nosrc(t):
    """v3.9, Aras 14 Nov 15:23 UTC: "dont give sources in the brackets dont give sources in the drawings at all";
    15:24: "no sources for nothing": a text without its source brackets (sources stay in the log)"""
    t = re.sub(r"\s*\([^()]*\b(%s)\b[^()]*\)" % PC_SRC_WORDS, u"", t)
    return re.sub(r"\s{2,}", u" ", t).strip()


def pc_mb_legend(rows, K):
    """MapBase legend rows -> pc_sheet rows [(draw(x, y), label)]"""
    out = []
    for kind, col, txt in rows:
        txt = pc_nosrc(txt)
        if kind == "line":
            out.append((lambda x, y, c=col: [L_([(x - 4.5, y), (x + 4.5, y)], c, 0.3, "legend")], txt))
        elif kind == "dot":
            out.append((lambda x, y, c=col: [P_([circle(x, y, 0.7, 12)], c, None, 0.0, "legend")], txt))
        else:
            out.append((lambda x, y, c=col: [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0), (x + 4.5, y + 2.0),
                                                  (x - 4.5, y + 2.0)]], c, K["grey_line"], 0.1, "legend")], txt))
    return out


PC_STATE = {}


PC_A3 = (420.0, 297.0)        # v3.10: A3 landscape, mm


def pc_a3_den(D, extra_w=0.0, step=500.0, page=None):
    """v3.10: the smallest round scale (1:step multiples) at which map + column + extra_w mm fit the page (A3 landscape;
    page = (w, h) mm when a slide sheet asks for another size)"""
    b = D["box"]
    page = page or PC_A3
    fw = page[0] - 2 * PC_MARGIN_MM - 8.0 - PC_SIDE_MM - extra_w
    fh = page[1] - 2 * PC_MARGIN_MM
    den = max((b[2] - b[0]) * 1000.0 / max(fw, 1.0), (b[3] - b[1]) * 1000.0 / fh)
    return int(math.ceil(den / step) * step)


def pc_a3(M, extra_w=0.0, log=None, page=None):
    """v3.10: centre map + column (+ extra_w mm the caller adds to M.w later) on the page (A3 landscape); FLAG if larger"""
    W, H = page or PC_A3
    nw, nh = M.w + extra_w, M.h
    if (nw > W + 0.1 or nh > H + 0.1) and log is not None:
        log.append(u"FLAG: the page is %.0f x %.0f mm, larger than A3" % (nw, nh))
    dx, dy = max(0.0, (W - nw) / 2.0), max(0.0, (H - nh) / 2.0)
    M.x0 += dx
    M.y0 += dy
    M.box = (M.x0, M.y0, M.x0 + M.mw, M.y0 + M.mh)
    M.w, M.h = max(W, nw) - extra_w, max(H, nh)
    return M


def pc_study(M, K, log):
    p = os.path.join(pc_root(), PC_STUDY_CACHE)
    if not os.path.isfile(p):
        log.append(u"FLAG: %s missing: the study area is not drawn (press Basemap once)" % p)
        return []
    with open(p, encoding="utf-8") as f:
        cal = json.load(f).get("calisma") or []
    it = []
    for R in cal:
        Q = [M.T(q) for q in R] + [M.T(R[0])]
        for run in M.clip(Q):
            it.append(L_(run, K["study"][0], K["study"][1], "study_area", (2.4, 0.8)))
    log.append(u"study area: %d ring(s) from %s" % (len(cal), p))
    return it


# ================================================================ v3.15: the map frame = site_alan, turned flat
# Aras 14 Nov 16:17 UTC: "KEEP EVERY DRAWING STRICTLY IN SITE_ALAN except" Plan 01 (Page02's 1:25,000 context map).
class SiteMap(Map):
    """site_alan turned flat as the Basemap draws it (its Frame: long side horizontal, eastern end right); the corners
    from the Basemap cache (frame), else the Basemap script's built-in copy (FRAME_COPY). Same use as Map"""

    def __init__(self, den, log):
        lib = PC_STATE.get("lib") or pc_lib(log)
        corners = None
        p = os.path.join(pc_root(), PC_STUDY_CACHE)
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                corners = json.load(f).get("frame")
        if not corners:
            corners = lib["FRAME_COPY"]
            log.append(u"site_alan: the Basemap's built-in copy (no frame in %s)" % p)
        self.F = lib["Frame"]([tuple(c) for c in corners])
        self.ring = [tuple(c[:2]) for c in corners]       # v3.17: the corners (survey m) and their bounding box
        self.den = float(den)
        self.k = 1000.0 / self.den
        self.b = (min(c[0] for c in self.ring), min(c[1] for c in self.ring), max(c[0] for c in self.ring),
                  max(c[1] for c in self.ring))
        self.mw, self.mh = self.F.w * self.k, self.F.h * self.k
        self.x0, self.y0 = PC_MARGIN_MM, PC_MARGIN_MM
        self.w = self.x0 + self.mw + 8.0 + PC_SIDE_MM + PC_MARGIN_MM
        self.h = self.y0 + self.mh + PC_MARGIN_MM
        self.box = (self.x0, self.y0, self.x0 + self.mw, self.y0 + self.mh)
        self.north = self.F.north()
        log.append(u"frame: site_alan %.0f x %.0f m turned flat; 1:%s = %.0f x %.0f mm" % (
            self.F.w, self.F.h, format(int(den), ",d"), self.mw, self.mh))

    def T(self, p):
        u, v = self.F.local(p)
        return (self.x0 + u * self.k, self.y0 + v * self.k)


def pc_site_map(den, log):
    return SiteMap(den, log)


def pc_site_den(M, page, side_w, below_h=0.0, step=500.0):
    """v3.17: the smallest round scale at which the site_alan map (M: a SiteMap at any scale) + side_w mm right of it
    (legend columns) fit the page across, with below_h mm kept under the map"""
    fw = page[0] - 2 * PC_MARGIN_MM - 8.0 - side_w
    fh = page[1] - 2 * PC_MARGIN_MM - below_h
    den = max(M.F.w * 1000.0 / max(fw, 1.0), M.F.h * 1000.0 / max(fh, 1.0))
    return int(math.ceil(den / step) * step)


def pc_north_deg(north):
    """v3.17: a SiteMap's north (page vector) as pc_sheet's north angle (deg clockwise)"""
    return math.degrees(math.atan2(north[0], north[1]))


def pc_north_items(cx, cy, r, north, col, layer="north_scale"):
    """a north arrow in a circle at (cx, cy), pointing along north = page direction (nx, ny) of survey north"""
    nx, ny = north
    ex, ey = ny, -nx
    P = lambda a, b: (cx + a * ex + b * nx, cy + a * ey + b * ny)
    return [P_([circle(cx, cy, r, 48)], None, col, 0.2, layer),
            P_([[P(0, r), P(-0.45 * r, -0.5 * r), P(0, -0.22 * r), P(0.45 * r, -0.5 * r)]], col, None, 0.0, layer),
            T_(u"N", P(0, r + 1.4)[0], P(0, r + 1.4)[1] - 0.9, 2.4, col, layer, True, "C")]


# ================================================================ transit
def pc_stop_lines(D):
    """{stop name: set of line refs}: OSM membership, corrected by ESHOT where the data notes a conflict"""
    out = {}
    for s in D["stops"]:
        out.setdefault(s["name"], set()).update(s["lines"])
    for fx in D.get("official_fixes", []):
        if fx.get("add") and fx["name"] in out:
            out[fx["name"]].update(fx["add"])
    return out


def pc_stop_groups(D):
    """the stops merged by name within 80 m (the two sides of a street): [(name, survey xy, lines)]"""
    lines = pc_stop_lines(D)
    out = []
    for s in D["stops"]:
        for g in out:
            if g[0] == s["name"] and pc_dist(g[1], s["xy"]) < 80.0:
                g[3].append(s["xy"])
                break
        else:
            out.append([s["name"], s["xy"], lines.get(s["name"], set()), [s["xy"]]])
    res = []
    for n, _xy, ln, pts in out:
        res.append((n, (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)), ln))
    return res


def pc_group_of(D, ref):
    for g, v in D["lines"].items():
        if ref in v["refs"]:
            return g
    return None


def pc_line_items(M, D, K, grey=None):
    """every bus way once, one lane per line group on it (town, 656, village, regional), side by side; grey = one
    thin grey line per way instead (the heritage page)"""
    groups_on = {}
    for ref, R in D["routes"].items():
        g = pc_group_of(D, ref)
        for wid in R["ways"]:
            groups_on.setdefault(wid, set()).add(g)
    it = []
    order = K["line_order"]
    for wid, gs in sorted(groups_on.items()):
        P = D["ways"].get(wid)
        if not P:
            continue
        Q = [M.T(p) for p in P]
        if grey:
            for run in M.clip(Q):
                it.append(L_(run, grey[0], grey[1], "bus_lines"))
            continue
        gl = [g for g in order if g in gs]
        ws = [K["lines"][g][1] for g in gl]
        tot = sum(ws) + K["lane_gap"] * (len(gl) - 1)
        off = -tot / 2.0
        for g, w in zip(gl, ws):
            col, _w, dash = K["lines"][g]
            QQ = offset_line(Q, off + w / 2.0)
            for run in M.clip(QQ):
                it.append(L_(run, col, w, "bus_lines/" + g, tuple(dash) if dash else None))
            off += w + K["lane_gap"]
    return it


# ================================================================ labels that never sit on a symbol or a name
class Labels(object):
    def __init__(self, M, lib):
        self.M, self.lib, self.boxes, self.items, self.forced = M, lib, [], [], []

    def block(self, b):
        self.boxes.append(b)

    def block_pt(self, q, r):
        self.boxes.append((q[0] - r, q[1] - r, q[0] + r, q[1] + r))

    def block_line(self, P, r):
        """v3.7 (run 6 review: names sat on the spine, the river and the study line): keep names r mm off a polyline
        (page mm), as small boxes every r mm along it"""
        st = max(r, 0.5)
        for a, c in zip(P, P[1:]):
            n = max(1, int(math.hypot(c[0] - a[0], c[1] - a[1]) / st))
            for i in range(n + 1):
                self.block_pt((a[0] + (c[0] - a[0]) * i / n, a[1] + (c[1] - a[1]) * i / n), r)

    def block_items(self, items, layers, pad=0.4):
        """v3.7: block_line for every line item of these layers, half its width + pad"""
        for it in items:
            if it[0] == "line" and it[5] in layers:
                self.block_line(it[1], (it[3] or 0.1) / 2.0 + pad)

    def free(self, b):
        if not (self.M.box[0] <= b[0] and b[2] <= self.M.box[2] and self.M.box[1] <= b[1] and b[3] <= self.M.box[3]):
            return False
        return not any(b[0] < o[2] and o[0] < b[2] and b[1] < o[3] and o[1] < b[3] for o in self.boxes)

    def put(self, s, q, size, col, layer, bold=False, gap=1.6, halo=True):
        """try 8 places round q (right, left, above, below, the corners, then twice as far); the first free one, else
        the right-hand place anyway and a log line (a name is never left out)"""
        if not self.M.inside(q):                         # v3.15: a point outside the frame gets no name here
            return
        w = self.lib["text_w"](s, size, bold)
        h = size * 0.75
        cands = []
        for g in (gap, gap * 2.2, gap * 3.6):
            cands += [(q[0] + g, q[1] - h / 2.0, "L"), (q[0] - g, q[1] - h / 2.0, "R"), (q[0], q[1] + g, "C"),
                      (q[0], q[1] - g - h, "C"), (q[0] + g * 0.8, q[1] + g * 0.8, "L"),
                      (q[0] - g * 0.8, q[1] + g * 0.8, "R"), (q[0] + g * 0.8, q[1] - g * 0.8 - h, "L"),
                      (q[0] - g * 0.8, q[1] - g * 0.8 - h, "R")]
        pick = None
        for x, y, al in cands:
            x0 = x if al == "L" else x - w if al == "R" else x - w / 2.0
            b = (x0 - 0.3, y - 0.25 * size - 0.3, x0 + w + 0.3, y + h + 0.3)
            if self.free(b):
                pick = (x, y, al, b)
                break
        if pick is None:                                 # v3.8: the place with the least overlap (was: right-hand)
            def lap(b_):
                return sum(max(0.0, min(b_[2], o[2]) - max(b_[0], o[0])) * max(0.0, min(b_[3], o[3]) - max(b_[1], o[1]))
                           for o in self.boxes)
            best = None
            for x, y, al in cands:
                x0 = x if al == "L" else x - w if al == "R" else x - w / 2.0
                b = (x0 - 0.3, y - 0.25 * size - 0.3, x0 + w + 0.3, y + h + 0.3)
                inside = self.M.box[0] <= b[0] and b[2] <= self.M.box[2] and self.M.box[1] <= b[1] and b[3] <= self.M.box[3]
                if inside and (best is None or lap(b) < best[0]):
                    best = (lap(b), (x, y, al, b))
            x, y, al = cands[0]
            pick = best[1] if best else (x, y, al, (x - 0.3, y - 0.3, x + w + 0.3, y + h + 0.3))
            self.forced.append(s)
        x, y, al, b = pick
        self.boxes.append(b)
        if halo:                                         # v3.27: a letter-shaped halo, no white box
            self.items += pc_halo(s, x, y, size, bold, al, layer + "_halo")
        self.items.append(T_(s, x, y, size, col, layer, bold, al))


def pc_selinos_line():
    """v3.4: the Selinos centreline in survey m, upstream first (Data/selinos_centreline.json, the line the surveyed
    sections were cut on; the same file Basemap and the section scripts read), read once"""
    if "selinos" not in PC_STATE:
        with open(os.path.join(pc_root(), PC_CENTRE), encoding="utf-8") as f:
            PC_STATE["selinos"] = [tuple(q) for q in json.load(f)["points"]]
    return PC_STATE["selinos"]


def pc_selinos(a, b):
    """the stretch of the Selinos centreline between the points nearest to a and b (survey m), a and b added
    at the ends: the streamside spine and the stream walk follow the stream, not straight legs; None if either point
    lies over 80 m from the line"""
    P = pc_selinos_line()
    if not P:
        return None
    ia = min(range(len(P)), key=lambda i: pc_dist(P[i], a))
    ib = min(range(len(P)), key=lambda i: pc_dist(P[i], b))
    if pc_dist(P[ia], a) > 80.0 or pc_dist(P[ib], b) > 80.0:
        return None
    lo, hi = min(ia, ib), max(ia, ib)
    S = list(P[lo:hi + 1])
    if ia > ib:
        S = S[::-1]
    return [tuple(a)] + S + [tuple(b)]


# ================================================================ v3.10: the heritage loop, drawn by one code on both maps
# Aras 14 Nov 15:31 UTC: "the bold connection between the heritage should stay there just like the old diagram" (on the
# transit map too); 12:38: "don't ever do the same job twice in two scripts".
def pc_station_name(s):
    """an OSM station name as both maps print it (Turkish letters: 'Teleferik, Yukarı İstasyon')"""
    return (s.get("name") or u"").replace(u"Akropolis Teleferik - ", u"Teleferik, ").replace(u" ( ", u" (").replace(
        u" )", u")")


def pc_loop(M, D, K, lab, log, names=False):
    """the loop 1..7: bold red legs stop to stop (3 -> 4 along the Selinos: the stream walk), dotted on foot from the
    upper Teleferik station to Akropol, red numbered badges, Akropol a red ring; lines and badges kept free of names
    (lab). Returns items"""
    T, it = M.T, []
    RED, W, R, tm = K["heritage"], K["heritage_w"], K["heritage_r"], K["text_mm"]
    H = sorted(D["heritage"], key=lambda h: int(h["n"]))
    legs = []
    for a, b in zip(H, H[1:]):
        if {a["key"], b["key"]} == {"tabak_koprusu", "ulucami_onu"}:
            sw = pc_selinos(a["xy"], b["xy"])
            if sw:
                legs.append(("walk", sw))
                log.append(u"stream walk: Tabak Köprüsü -> Ulucami Önü along the Selinos, %.0f m" % sum(
                    pc_dist(p, q) for p, q in zip(sw, sw[1:])))
                continue
            log.append(u"FLAG: the Selinos line is over 80 m from stop 3 or 4: the stream walk is drawn straight")
        legs.append(("leg", [a["xy"], b["xy"]]))
    for kind, P in legs:
        for run in M.clip([T(p) for p in P]):
            it.append(L_(run, "FFFFFF", W + 0.6, "loop"))
            it.append(L_(run, RED, W + (0.6 if kind == "walk" else 0.0), "loop"))
            if kind == "walk":
                it.append(L_(run, "FFFFFF", 0.3, "loop", (1.2, 1.2)))
            lab.block_line(run, W / 2.0 + 0.6)
    upper = next((s for s in D["stations"] if s["kind"] == "gondola" and u"Yukarı" in (s["name"] or u"")), None)
    if upper:
        for run in M.clip([T(upper["xy"]), T(D["akropol"])]):
            it.append(L_(run, RED, 0.5, "loop", (0.01, 1.0)))
    log.append(u"loop: %d stops, %d legs, %.0f m stop to stop (straight legs; the walk along the stream)" % (
        len(H), len(legs), sum(pc_dist(p, q) for _k, P in legs for p, q in zip(P, P[1:]))))
    for h in H:
        q = T(h["xy"])
        if not M.inside(q):
            continue                                     # v3.15: shown by an edge arrow (below)
        it.append(P_([circle(q[0], q[1], R, 32)], RED, "FFFFFF", 0.35, "loop_stops"))
        it.append(pc_text_c(h["n"], q[0], q[1], tm["label"] + 0.2, "FFFFFF", "loop_stops"))   # v3.28
        lab.block_pt(q, R + 0.6)
    qa = T(D["akropol"])
    if M.inside(qa):
        it.append(P_([circle(qa[0], qa[1], R * 0.8, 32)], "FFFFFF", RED, 0.6, "loop_stops"))
        lab.block_pt(qa, R)
    # v3.15: a stop outside the frame: an arrow where its leg leaves the frame, with its number and name
    done, arrows = set(), []
    for (kind, P), (a, b) in zip(legs, zip(H, H[1:])):
        Q = [T(p) for p in P]
        runs = M.clip(Q)
        if not runs:
            continue
        for h, end in ((b, runs[-1][-2:]), (a, runs[0][:2][::-1])):
            if M.inside(T(h["xy"]), -0.01) or h["n"] in done:
                continue
            done.add(h["n"])
            it.append(arrow_head(end[0], end[1], RED, 2.6, "loop_stops"))
            arrows.append((h, end[1]))
            lab.block_pt(end[1], 1.6)
    c = ((M.box[0] + M.box[2]) / 2.0, (M.box[1] + M.box[3]) / 2.0)
    for h in H:                                          # a stop no drawn leg reaches: an arrow toward it from the centre
        if h["n"] in done or M.inside(T(h["xy"]), -0.01):
            continue
        runs = M.clip([c, T(h["xy"])])
        if runs and len(runs[-1]) >= 2:
            done.add(h["n"])
            end = runs[-1][-2:]
            it.append(arrow_head(end[0], end[1], RED, 2.6, "loop_stops"))
            arrows.append((h, end[1]))
            lab.block_pt(end[1], 1.6)
    if names:                                            # the stops inside the frame named on the map
        for h in H:
            if M.inside(T(h["xy"])):
                lab.put(h["name"], T(h["xy"]), tm["label"], RED, "loop_names", True, gap=R + 1.0)
    for h, q in arrows:
        lab.put(u"%s %s" % (h["n"], h["name"]), q, tm["small"], RED, "loop_names", True, gap=2.4)
        log.append(u"stop %s %s lies outside site_alan: an edge arrow" % (h["n"], h["name"]))
    return it


def pc_cut_mark(a, b, look, name, col="C0392B", layer="section_lines", ts=2.5):
    """v3.32 (Aras 15 Nov 14:46 UTC "use the one that archicad uses for section line annotation" + his screenshot of
    Archicad's S-01 marker, 15:02 UTC): a cut shown by its two ends only, page mm, in Archicad's marker look: at each
    end a filled triangle whose base lies on the cut line, starting at the end and running inward, its tip pointing the
    way the section looks (look: a page vector); a short thin stub of the cut line inward from the triangle, with one
    dot and one short dash after it (Archicad's dash-dot cut line, broken off); the name in regular weight, turned to
    read along the cut, just beyond the end. No line between the ends (Aras 14 Nov 16:05). Items in the Basemap
    format (text angle in degrees)."""
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    if L < 1e-6:
        return []
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    sg = 1.0 if (-uy * look[0] + ux * look[1]) >= 0.0 else -1.0
    fx, fy = -uy * sg, ux * sg                          # the side the section looks to
    base = min(2.4, L / 4.0)                            # triangle base along the cut (screenshot: base = depth)
    depth = base
    out = []
    ang = math.degrees(math.atan2(uy, ux))              # text along the cut, kept readable (-90 < ang <= 90)
    if ang > 90.0:
        ang -= 180.0
    elif ang <= -90.0:
        ang += 180.0
    ra = math.radians(ang)
    rx, ry = math.cos(ra), math.sin(ra)                 # reading direction
    tw = PC_STATE.get("lib", {}).get("text_w") if isinstance(PC_STATE.get("lib"), dict) else None
    for p, s in ((a, 1.0), (b, -1.0)):                  # s: inward along the cut
        ix, iy = ux * s, uy * s
        p0 = tuple(p)
        p1 = (p[0] + ix * base, p[1] + iy * base)
        mid = (p[0] + ix * base / 2.0, p[1] + iy * base / 2.0)
        tip = (mid[0] + fx * depth, mid[1] + fy * depth)
        out.append(("poly", [[p0, p1, tip]], col, None, 0.0, None, layer, 1, None, None))
        d0 = base
        for d_a, d_b in ((0.0, 1.6), (2.2, 2.45), (3.05, 4.3)):   # stub, dot, short dash
            q0 = (p[0] + ix * (d0 + d_a), p[1] + iy * (d0 + d_a))
            q1 = (p[0] + ix * (d0 + d_b), p[1] + iy * (d0 + d_b))
            out.append(("line", [q0, q1], col, 0.18, None, layer, 1))
        if name:
            w_ = tw(name, ts, False) if tw else 0.6 * ts * len(name)
            gap = 1.0
            c_ = (p[0] - ix * (gap + w_ / 2.0), p[1] - iy * (gap + w_ / 2.0))   # name centre, beyond the end
            c_ = (c_[0] + fx * depth * 0.5, c_[1] + fy * depth * 0.5)          # over the triangle, as in Archicad
            x0 = c_[0] - rx * w_ / 2.0 - (-ry) * ts * PC_CAP
            y0 = c_[1] - ry * w_ / 2.0 - rx * ts * PC_CAP
            out.append(("text", name, x0, y0, ts, col, False, "L", layer, ang, None))
    return out


# ================================================================ sheet furniture (right-hand column)
def pc_sheet(M, K, lib, title, sub, legend, notes, credit, north=0.0, bar_note=None, cols=1, span=None):
    """legend = [(draw(x, y) -> items, label)], swatch 10 x 5 mm; (None, text) = a bold header row; notes = [text];
    v3.17: cols = legend columns side by side (title across them, notes in the last); span = (bottom, top) page y of
    the column when it is taller than the map (a strip map: north and scale at the span's foot); returns items"""
    it = []
    tm = K["text_mm"]
    INK = K["ink"]
    tw = lib["text_w"]
    x = M.box[2] + 8.0
    W = PC_SIDE_MM
    ybot, ytop = span if span else (M.box[1], M.box[3])
    y = ytop - tm["title"]
    for ln in wrap(title.upper(), tm["title"], W * cols + 6.0 * (cols - 1), tw, True):
        it.append(T_(ln, x, y, tm["title"], INK, "title", True))
        y -= tm["title"] * 1.25
    y -= 1.0
    for ln in wrap(sub, tm["sub"], W * cols + 6.0 * (cols - 1), tw):
        it.append(T_(ln, x, y, tm["sub"], INK, "title"))
        y -= tm["sub"] * 1.4
    y -= 5.0
    n_ = len(legend)
    cut = [int(round(n_ * i / float(cols))) for i in range(cols + 1)]
    for i in range(1, cols):                             # v3.17: a column never ends with a header row
        while 0 < cut[i] < n_ and legend[cut[i] - 1][0] is None:
            cut[i] -= 1
    y_leg, x0c = y, x
    for c_ in range(cols):
        x = x0c + c_ * (W + 6.0)
        y = y_leg
        for draw, label in legend[cut[c_]:cut[c_ + 1]]:
            if draw is None:                             # a header row (EXISTING ... / PROPOSAL MARKS), as the node pages
                y -= 1.5
                it.append(T_(label, x, y, tm["legend"], INK, "legend", True))
                y -= 6.0
                continue
            it += draw(x + 5.0, y + 1.0)
            lines = wrap(label, tm["legend"], W - 14.0, tw)
            yy = y
            for ln in lines:
                it.append(T_(ln, x + 13.0, yy, tm["legend"], INK, "legend"))
                yy -= tm["legend"] * 1.3
            y = min(y - 6.0, yy - 2.0)
    y -= 3.0
    for nt in notes:
        for ln in wrap(nt, tm["small"] + 0.2, W, tw):
            it.append(T_(ln, x, y, tm["small"] + 0.2, INK, "notes"))
            y -= (tm["small"] + 0.2) * 1.4
        y -= 1.5
    x = x0c
    # north arrow + scale bar under the column, above the credit
    yb = ybot + 30.0
    cx, cy, r = x + 7.0, yb + 7.0, 5.5
    it.append(P_([circle(cx, cy, r, 48)], None, INK, 0.2, "north_scale"))
    ca_, sa_ = math.cos(math.radians(north)), math.sin(math.radians(north))   # v3.5: north turned clockwise (deg)
    rot = lambda dx, dy: (cx + dx * ca_ + dy * sa_, cy - dx * sa_ + dy * ca_)
    it.append(P_([[rot(0, r), rot(-2.4, -2.6), rot(0, -1.2), rot(2.4, -2.6)]], INK, None, 0.0, "north_scale"))
    q_ = rot(0, r + 2.4)
    it.append(T_(u"N", q_[0], q_[1] - 1.0, 2.6, INK, "north_scale", True, "C"))
    bar = 100.0 if M.den <= 2500 else 250.0 if M.den <= 6000 else 500.0
    Lb = bar * M.k
    xb, yb2 = x + 18.0, yb + 4.0
    for i in range(4):
        it.append(P_([[(xb + Lb * i / 4, yb2), (xb + Lb * (i + 1) / 4, yb2), (xb + Lb * (i + 1) / 4, yb2 + 1.4),
                       (xb + Lb * i / 4, yb2 + 1.4)]], INK if i % 2 == 0 else "FFFFFF", INK, 0.15, "north_scale"))
    it.append(T_(u"0", xb, yb2 - 3.0, 2.0, INK, "north_scale", False, "C"))
    it.append(T_(u"%d m" % bar, xb + Lb, yb2 - 3.0, 2.0, INK, "north_scale", False, "C"))
    it.append(T_(u"1:%s" % format(int(M.den), ",d"), xb, yb2 + 4.0, 3.2, INK, "north_scale", True))
    if bar_note:
        it.append(T_(bar_note, xb, yb2 - 6.2, 2.0, INK, "north_scale"))
    yc = ybot + 20.0
    for ln in (wrap(credit, tm["small"], W, tw) if credit else []):   # v3.9: no credit line (no sources)
        it.append(T_(ln, x, yc, tm["small"], "6E6C66", "credit"))
        yc -= tm["small"] * 1.4
    it.append(P_([[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]], None,
                 INK, 0.25, "frame"))
    return it


def wrap(s, size, width, tw, bold=False):
    out, line = [], u""
    for wd in s.split(u" "):
        t = (line + u" " + wd).strip()
        if line and tw(t, size, bold) > width:
            out.append(line)
            line = wd
        else:
            line = t
    if line:
        out.append(line)
    return out


# ================================================================ outputs: PDF, SVG, review PNGs
PC_STROKE_REF = (380.0, 260.0)   # mm: v3.33, a full A3 drawing = factor 1.0 (the route / bus / loop weights were set on it)
PC_STROKE_MIN = 0.35             # the thinnest factor (a small inset or node axo)


def pc_stroke_k(w_mm, h_mm, log=None, name=u"drawing"):
    """v3.33 (Aras 15 Nov 15:57 UTC, standing for every drawing): line weights scale with the drawing's size: factor =
    sqrt(w x h / PC_STROKE_REF area), kept within PC_STROKE_MIN-1.0. Multiply route, bus, loop, river-edge and other
    heavy line weights (and casings) by it: pc_stroke(lw, k)"""
    k = math.sqrt(max(w_mm, 0.0) * max(h_mm, 0.0) / (PC_STROKE_REF[0] * PC_STROKE_REF[1]))
    k = max(PC_STROKE_MIN, min(1.0, k))
    if log is not None:
        log.append(u"line weights: %s %.0f x %.0f mm, stroke factor %.2f" % (name, w_mm, h_mm, k))
    return k


def pc_stroke(lw, k, floor=0.1):
    """v3.33: a line weight lw (mm) scaled by the drawing's stroke factor k, never under floor mm"""
    return max(floor, lw * k) if lw else lw


def pc_layer_of(it):
    """v3.29: the layer of a Basemap-writer item (line: index 5, poly: 6, text: 8), else None"""
    i = {"line": 5, "poly": 6, "text": 8}.get(it[0] if it else None)
    return it[i] if i is not None and len(it) > i else None


def pc_study_top(items, log=None, layer="study_area"):
    """v3.29 (Aras 15 Nov 14:45 UTC): the working-area dashed line is the topmost line of every drawing: its items
    move to the end of the list (drawn last), in their own order"""
    top = [it for it in items if pc_layer_of(it) == layer]
    if not top:
        return items
    if log is not None:
        log.append(u"working-area line on top: %d piece(s)" % len(top))
    return [it for it in items if pc_layer_of(it) != layer] + top


PC_MP_MAX_M2 = 100000.0     # m2: v3.29, a bigger masterplan piece is a sheet / texture frame (nodes common v8.1)


PC_CLIP_WA = "map_wa"        # v3.34: the clip id of the masterplan pasted inside the working area


def pc_wa_rings(M, log=None):
    """v3.34: the working-area rings (Basemap cache calisma) through the map transform, page mm; [] if missing"""
    p = os.path.join(pc_root(), PC_STUDY_CACHE)
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8") as f:
        cal = [R for R in (json.load(f).get("calisma") or []) if len(R) >= 3]
    return [[tuple(M.T(q)) for q in R] for R in cal]


PC_MP_MARK = "010305"          # v3.36: the stand-in fill where the browser-printed masterplan goes in the PDF


def pc_mp_print(MPn, log):
    """v3.36 (Aras 15 Nov 20:45-20:50 UTC "many of the things from masterplan is missing", "use one from open source
    browsers ... really good svg reading engine", "yeah take chromium svg reader"): master.svg as the laptop's Chromium
    (Edge / Chrome) prints it to a vector PDF, made ONCE per master.svg by scripts/bergama_master_print_v*.py (outside
    Rhino: it can take many minutes); a page only reads it. Returns (pdf, viewBox (x, y, w, h)) or None (FLAG)"""
    svg = os.path.join(pc_root(), MPn["MP_SVG"])
    cdir = os.path.join(pc_root(), "cached", MPn["OUT_FOLDER"])
    pdf, stp = os.path.join(cdir, "master_print.pdf"), os.path.join(cdir, "master_print.stamp")
    if not (os.path.isfile(svg) and os.path.isfile(pdf) and os.path.isfile(stp)):
        log.append(u"FLAG masterplan print missing: run scripts/bergama_master_print_v1.py once (py -3): masterplan "
                   u"drawn as vector pieces (no pictures, no river texture)")
        return None
    try:
        with open(stp, encoding="utf-8") as f:
            st = json.load(f)
    except Exception:
        st = {}
    if st.get("stamp") != u"%d/%d" % (os.path.getsize(svg), int(os.path.getmtime(svg))):
        log.append(u"FLAG masterplan print is older than master.svg: run scripts/bergama_master_print_v1.py again: "
                   u"masterplan drawn as vector pieces")
        return None
    return pdf, st["viewbox"]


def pc_mp_affine(M, MPC, vb, log):
    """v3.36: the matrix (a, b, c, d, e, f) from the printed page's points (y up) to this page's mm (y up): print
    point -> SVG user unit (viewBox, 0.75 pt a px) -> survey m (MasterplanBase matrix) -> page mm (M.T, checked affine)"""
    a, b, c, d, e, f = MPC["matrix"]
    Hpt = vb[3] * 0.75

    def chain(xs, ys):
        u, v = vb[0] + xs / 0.75, vb[1] + (Hpt - ys) / 0.75
        return M.T((a * u + c * v + e, b * u + d * v + f))
    p0, px, py = chain(0.0, 0.0), chain(1000.0, 0.0), chain(0.0, 1000.0)
    A = ((px[0] - p0[0]) / 1000.0, (px[1] - p0[1]) / 1000.0, (py[0] - p0[0]) / 1000.0, (py[1] - p0[1]) / 1000.0,
         p0[0], p0[1])
    q = chain(3000.0, 600.0)
    err = math.hypot(A[0] * 3000 + A[2] * 600 + A[4] - q[0], A[1] * 3000 + A[3] * 600 + A[5] - q[1])
    if err > 0.2:
        log.append(u"FLAG masterplan print: the map transform is not affine (%.2f mm off): vector pieces used" % err)
        return None
    return A


PC_MP_PLACE = r"""
import sys, re, json
try:
    import pymupdf as fitz
except ImportError:
    import fitz
pdf, spec = sys.argv[1], json.load(open(sys.argv[2]))
MARK = re.compile(rb"q\n(?:[-0-9. ]+ [ml]\n|h\n)+%s rg\nf\*?\nQ\n" % spec["mark"].encode())
d = fitz.open(pdf)
pg = d[0]
s = fitz.open(spec["src"])
old = [(x, d.xref_stream(x)) for x in pg.get_contents()]
pg.show_pdf_page(pg.rect, s, 0, keep_proportion=False, overlay=True)
fx, name = [(x[0], x[1]) for x in pg.get_xobjects() if x[2] == 0][-1]
sr = s[0].rect
A = spec["A"]
ux, uy = sr.width / pg.rect.width, sr.height / pg.rect.height
A = (A[0] * ux, A[1] * ux, A[2] * uy, A[3] * uy, A[4], A[5])
keep = set(x for x, _ in old)
for x in pg.get_contents():
    if x not in keep:
        d.update_stream(x, b"")
n = 0
for x, st in old:
    st2, k = MARK.subn(lambda m: b"q %s cm /%s Do Q\n" % (" ".join("%.6f" % v for v in A).encode(), name.encode()), st)
    d.update_stream(x, st2)
    n += k
d.save(pdf + ".tmp", garbage=3, deflate=True)
d.close()
import os
os.replace(pdf + ".tmp", pdf)
print("masterplan print placed %d time(s) (%s)" % (n, name))
"""


def pc_mp_place(paths, M, log):
    """v3.36: the browser-printed masterplan put where pc_masterplan left its stand-in (PDF: as a form, under every
    later item, cut to the working area; SVG: a linked image of master.svg at the same place)"""
    import subprocess, sys as _sys
    pdf_, A, vb, svg = M.mp_place
    for p in paths:
        try:
            if p.lower().endswith(".svg"):
                with open(p, encoding="utf-8") as f:
                    s_ = f.read()
                H = M.h
                # image units: SVG user units minus the viewBox origin -> print pt -> page mm (y up) -> SVG page (y down)
                a, b, c, d, e, f = A
                Hpt = vb[3] * 0.75                       # image unit (x, y) = print point (0.75 x, Hpt - 0.75 y)
                ma, mb = a * 0.75, -(b * 0.75)
                mc, md = -(c * 0.75), (d * 0.75)
                me, mf = c * Hpt + e, H - (d * Hpt + f)
                img = (u'<image x="0" y="0" width="%.4f" height="%.4f" preserveAspectRatio="none" '
                       u'transform="matrix(%.6f %.6f %.6f %.6f %.4f %.4f)" xlink:href="%s"/>'
                       % (vb[2], vb[3], ma, mb, mc, md, me, mf, u"file:///" + svg.replace(u"\\", u"/")))
                s2, n_ = re.subn(r'<path d="[^"]*" fill="#%s"/>' % PC_MP_MARK, lambda m: img, s_)
                with open(p, "w", encoding="utf-8") as f:
                    f.write(s2)
                log.append(u"masterplan: linked master.svg placed %d time(s) in %s" % (n_, p))
                continue
            cdir = os.path.join(pc_root(), PC_CACHE_DIR)
            os.makedirs(cdir, exist_ok=True)
            tp, sp = os.path.join(cdir, "mp_place_v1.py"), os.path.join(cdir, "mp_place_spec.json")
            with open(tp, "w", encoding="utf-8") as f:
                f.write(PC_MP_PLACE)
            with open(sp, "w") as f:
                json.dump({"src": pdf_, "A": list(A), "mark": "%.3f %.3f %.3f" % tuple(
                    int(PC_MP_MARK[i:i + 2], 16) / 255.0 for i in (0, 2, 4))}, f)
            cmds = [["py", "-3"], ["python"]]
            if os.path.basename(_sys.executable or "").lower().startswith("python"):
                cmds.insert(0, [_sys.executable])
            env = dict((k, v) for k, v in os.environ.items() if not k.upper().startswith("PYTHON"))
            ok = False
            for cmd in cmds:
                try:
                    r_ = subprocess.run(cmd + ["-I", tp, p, sp], capture_output=True, text=True, timeout=900, env=env,
                                        creationflags=PC_NOWIN)
                except Exception:
                    continue
                if r_.returncode == 0:
                    log.append(r_.stdout.strip() + u" in " + p)
                    ok = "placed 0 time" not in r_.stdout
                    break
            if not ok:
                log.append(u"FLAG masterplan print not placed in %s: the map shows paper there" % p)
        except Exception as ex:
            log.append(u"FLAG masterplan print not placed in %s (%s: %s)" % (p, type(ex).__name__, ex))


def pc_masterplan(M, log, lim=None, paste=True):
    """v3.29 (Aras 15 Nov 14:45 UTC "we gonna use masterplan svg as the base of the maps"): his masterplan
    (master.svg via the MasterplanBase cache) as vector pieces through the map transform, cut to clip PC_CLIP; his own
    copy of the existing roads and buildings (ev-yol) is left out by mp_draw, as are sheet frames over PC_MP_MAX_M2 and
    4-corner picture rectangles (nodes common v8.1-8.2). Returns items"""
    MPn, MPC = pc_mp_data(log)
    ar_ = lambda P_: abs(sum(P_[i][0] * P_[i - 1][1] - P_[i - 1][0] * P_[i][1] for i in range(len(P_)))) / 2.0
    cut_ = lambda e_: len(e_[4]) > 2 and (ar_(e_[4]) > PC_MP_MAX_M2 or (e_[0] == "a" and len(e_[4]) == 4))
    n_big = sum(1 for v_ in MPC["layers"].values() for e_ in v_ if cut_(e_))
    MPC = dict(MPC, layers=dict((kk, [e_ for e_ in v_ if not cut_(e_)]) for kk, v_ in MPC["layers"].items()))
    items = []
    wa = pc_wa_rings(M, log) if paste else []
    if paste and not wa:
        log.append(u"FLAG masterplan: no working area (press Basemap once): master.svg drawn over the whole map")
    if wa:                                                    # v3.34: cut-and-paste inside the working area
        M.wa = wa
        items.append(("poly", [list(R) for R in wa], "FFFFFF", None, 0.0, None, "wa_paper", 1, "eo", PC_CLIP))
        pr_ = pc_mp_print(MPn, log)                           # v3.36: his file as Chromium draws it
        A_ = pc_mp_affine(M, MPC, pr_[1], log) if pr_ else None
        if A_:
            b_ = M.box
            items.append(("poly", [[(b_[0], b_[1]), (b_[2], b_[1]), (b_[2], b_[3]), (b_[0], b_[3])]], PC_MP_MARK, None,
                          0.0, None, "mp/master_print", 1, None, PC_CLIP_WA))
            M.mp_place = (pr_[0], A_, pr_[1], os.path.join(pc_root(), MPn["MP_SVG"]))
            log.append(u"masterplan (master.svg) pasted inside the working area (%d ring(s)) as Chromium prints it: "
                       u"every picture, texture, gradient and clip of his file, base map hidden under it" % len(wa))
            return items
        keys = set(kk.split("/")[0] for kk in MPC["layers"])   # every layer, his existing ev-yol included
        cnt = MPn["mp_draw"](MPC, items, M.T, M.k, lim or M.box, PC_CLIP_WA, keys)
        log.append(u"masterplan (master.svg) pasted inside the working area (%d ring(s)): %d pieces in %d layer(s), "
                   u"his existing ev-yol included, base map hidden under it; %d sheet frames / picture rectangles "
                   u"left out" % (len(wa), sum(cnt.values()), len(cnt), n_big))
        return items
    cnt = MPn["mp_draw"](MPC, items, M.T, M.k, lim or M.box, PC_CLIP)
    log.append(u"masterplan (master.svg): %d pieces drawn in %d layer(s); %d sheet frames / picture rectangles "
               u"left out" % (sum(cnt.values()), len(cnt), n_big))
    return items


def pc_clips(M, clips=None):
    """v3.34: the page clips: the map frame (PC_CLIP) and, after pc_masterplan, the frame AND the working area"""
    fr = [[[(M.box[0], M.box[1]), (M.box[2], M.box[1]), (M.box[2], M.box[3]), (M.box[0], M.box[3])]]]
    out = dict(clips or {PC_CLIP: fr})
    if getattr(M, "wa", None) and PC_CLIP_WA not in out:
        out[PC_CLIP_WA] = fr + [[list(R) for R in M.wa]]
    return out


def pc_write(lib, M, items, out_dir, name, title, log, photos=None, clips=None):
    """v3.5: photos = pc_photos list (placed before the review PNGs); clips = own clip rings (default: the map box)"""
    os.makedirs(out_dir, exist_ok=True)
    items = pc_study_top(items, log)                          # v3.29: the working-area dashes last = on top
    pc_frame_check(items, M.box, log, lib.get("text_w"))
    paths = []
    for ext, fn in ((".pdf", lib["write_pdf"]), (".svg", lib["write_svg"])):
        p = os.path.join(out_dir, name + ext)
        try:
            clips = pc_clips(M, clips)                    # v3.3 frame; v3.34 + the working area
            p2 = fn(p, M.w, M.h, items, title, clips)
            paths.append(p2 or p)
        except Exception as ex:
            log.append(u"FLAG: %s not written (%s: %s)" % (p, type(ex).__name__, ex))
    for p in paths:
        log.append(u"%s  %s (%.0f x %.0f mm, 1:%s, %d objects)" % (p, time.strftime("%H:%M:%S"), M.w, M.h,
                                                                   format(int(M.den), ",d"), len(items)))
    if getattr(M, "mp_place", None):                      # v3.36: the browser-printed masterplan in place
        pc_mp_place(paths, M, log)
    if photos:
        pc_photos(paths, photos, M.h, log)
    pdfs = [p_ for p_ in paths if p_.lower().endswith(".pdf")]
    if not (pdfs and pc_review(pdfs[0], os.path.join(out_dir, "review"), log)):
        try:
            pc_png(items, M, os.path.join(out_dir, "review"), name, log)
        except Exception as ex:
            log.append(u"FLAG: review PNGs stopped (%s: %s)" % (type(ex).__name__, ex))
    return paths


# ================================================================ review PNGs, the standard of every page script
# v3, Aras 14 Nov 11:25 UTC: "every script should have it as a standard procedure to produce review png's in the most
# efficient way that claude reads ... optimize for yourself reading"; 11:26 UTC: "dont crop to the drawing have the all
# page ... if something goes out of the drawing you would want to see it". From the PDF (what is printed): the WHOLE
# page, 200 ppi, cut into an even grid of tiles of at most 1100 x 500 px (read without any downscale), plus
# 00_overview.png (the whole page, at most 1000 px wide) and index.txt (tile -> page mm, from the top left).
PC_REVIEW = r'''
import sys, os, glob, math
try:
    import pymupdf as fitz
except ImportError:
    import fitz
pdf, out = sys.argv[1], sys.argv[2]
PPI, TW, TH = 200, 1100, 500
os.makedirs(out, exist_ok=True)
for f in glob.glob(os.path.join(out, "*.png")) + glob.glob(os.path.join(out, "index.txt")):
    os.remove(f)
idx = []
doc = fitz.open(pdf)
for pn, pg in enumerate(doc):
    r = pg.rect                                       # the whole page, never cropped (Aras 11:26 UTC)
    pre = "" if len(doc) == 1 else "p%d_" % (pn + 1)
    pg.get_pixmap(dpi=int(min(PPI, 1000.0 * 72 / r.width)), clip=r).save(os.path.join(out, pre + "00_overview.png"))
    W, H = r.width / 72 * PPI, r.height / 72 * PPI
    nc, nr = int(math.ceil(W / TW)), int(math.ceil(H / TH))
    for j in range(nr):
        for i in range(nc):
            t = fitz.Rect(r.x0 + r.width * i / nc, r.y0 + r.height * j / nr, r.x0 + r.width * (i + 1) / nc,
                          r.y0 + r.height * (j + 1) / nr)
            nm = pre + "r%02dc%02d.png" % (j + 1, i + 1)
            pg.get_pixmap(dpi=PPI, clip=t).save(os.path.join(out, nm))
            mm = 25.4 / 72
            idx.append("%s  x %.0f-%.0f mm, y %.0f-%.0f mm from the top left" % (nm, t.x0 * mm, t.x1 * mm, t.y0 * mm,
                                                                               t.y1 * mm))
    n = nc * nr
with open(os.path.join(out, "index.txt"), "w") as f:
    f.write("\n".join(idx) + "\n")
print("review: overview + %d tiles (%d x %d grid, about %d x %d px, 200 ppi) in %s" % (n, nr, nc, W / nc, H / nr, out))
'''


PC_SHEET_LAYERS = ("legend", "title", "notes", "credit", "north_scale", "frame", "map_frame")


def pc_frame_check(items, box, log, text_w=None, skip=PC_SHEET_LAYERS):
    """v3.2 (Aras 12:14 UTC "drawings do flows outside of it"): FLAG every map item (any layer not in skip) whose ink
    leaves the map box (page mm); texts measured with text_w(s, size, bold) when given"""
    bad = {}
    for it in items:
        t = it[0]
        ly = it[6] if t == "poly" else it[5] if t == "line" else it[8] if t == "text" else None
        if ly is None or ly in skip:
            continue
        if (t == "line" and it[4]) or (t == "poly" and len(it) > 9 and it[9]):    # v3.5: any clip id (a line's at item[4], v3.19)
            continue                                     # v3.3: cut to the frame by its clip in the PDF / SVG
        if t == "text":
            w = text_w(it[1], it[4], bool(it[6])) if text_w else 0.5 * it[4] * len(it[1])
            x = it[2] - {"L": 0.0, "C": w / 2.0, "R": w}.get(it[7], 0.0)
            bx = (x, it[3], x + w, it[3] + it[4])
        else:
            pts = [q for R in it[1] for q in R] if t == "poly" else it[1]
            if not pts:
                continue
            bx = (min(q[0] for q in pts), min(q[1] for q in pts), max(q[0] for q in pts), max(q[1] for q in pts))
        if bx[0] < box[0] - 0.1 or bx[1] < box[1] - 0.1 or bx[2] > box[2] + 0.1 or bx[3] > box[3] + 0.1:
            bad[ly] = bad.get(ly, 0) + 1
    if bad:
        log.append(u"FLAG frame check: ink outside the map frame: %s" % u", ".join(
            u"%s %d" % (k, v) for k, v in sorted(bad.items())))
    else:
        log.append(u"frame check: all map ink inside its frame")
    return bad


def pc_review(pdf, out, log):
    """the review PNGs of a PDF into folder out (Rhino's Python if it has PyMuPDF, else the Windows py -3 / python);
    True when written"""
    try:
        cdir = os.path.join(pc_root(), PC_CACHE_DIR)
        os.makedirs(cdir, exist_ok=True)
        tp = os.path.join(cdir, "review_tiles_v3.py")
        with open(tp, "w", encoding="utf-8") as f:
            f.write(PC_REVIEW)
        import subprocess, sys as _sys
        cmds = [["py", "-3"], ["python"]]
        if os.path.basename(_sys.executable or "").lower().startswith("python"):
            cmds.insert(0, [_sys.executable])
        # a clean outside Python: Rhino's PYTHONHOME/PYTHONPATH made it fail with "SRE module mismatch" (14 Nov run)
        env = dict((k, v) for k, v in os.environ.items() if not k.upper().startswith("PYTHON"))
        err = u""
        for cmd in cmds:
            try:
                r_ = subprocess.run(cmd + ["-I", tp, pdf, out], capture_output=True, text=True, timeout=600, env=env, creationflags=PC_NOWIN)
            except Exception as ex:
                err = u"%s" % ex
                continue
            if r_.returncode == 0:
                log.append(r_.stdout.strip().splitlines()[-1] if r_.stdout.strip() else u"review: %s" % out)
                return True
            err = (r_.stderr or u"").strip().splitlines()[-1:] or [u""]
            err = err[0]
        log.append(u"FLAG review PNGs not written: no Python with PyMuPDF ran (%s); pip install pymupdf" % err)
    except Exception as ex:
        log.append(u"FLAG review PNGs not written (%s: %s)" % (type(ex).__name__, ex))
    return False


PC_PHOTO = r'''
import sys, json
try:
    import pymupdf as fitz
except ImportError:
    import fitz
pdf, spec = sys.argv[1], sys.argv[2]
with open(spec) as f:
    S = json.load(f)
doc = fitz.open(pdf)
pg = doc[0]
H = pg.rect.height
k = 72.0 / 25.4
for e in S:
    jp, x, y, w, h = e[:5]
    pg.insert_image(fitz.Rect(x * k, H - (y + h) * k, (x + w) * k, H - y * k), filename=jp, keep_proportion=False,
                    overlay=not (len(e) > 5 and e[5]))
doc.saveIncr()
print("photos: %d placed" % len(S))
'''


def pc_photos(paths, photos, H, log):
    """v3.5: JPEG photos into the written PDF (an outside Python with PyMuPDF, as the review PNGs) and SVG (an <image>
    each). photos = [(jpeg file, x, y, w, h)] in page mm (y up, (x, y) = lower left); H = page height mm"""
    import base64, subprocess, sys as _sys
    for p in paths:
        try:
            if p.lower().endswith(".svg"):
                with open(p, encoding="utf-8") as f:
                    s_ = f.read()
                img = lambda e: u'<image x="%.2f" y="%.2f" width="%.2f" height="%.2f" preserveAspectRatio="none" ' \
                    u'xlink:href="data:image/%s;base64,%s"/>' % (e[1], H - e[2] - e[4], e[3], e[4],
                                                                 u"png" if e[0].lower().endswith(".png") else u"jpeg",
                                                                 base64.b64encode(open(e[0], "rb").read()).decode("ascii"))
                top = u"".join(img(e) for e in photos if not (len(e) > 5 and e[5]))
                under = u"".join(img(e) for e in photos if len(e) > 5 and e[5])
                if under:                                # v3.30: an image UNDER the drawing (Page01Axo's 3D capture)
                    i_ = s_.index(u">", s_.index(u"<svg")) + 1
                    s_ = s_[:i_] + u'<g id="photos_under">' + under + u"</g>" + s_[i_:]
                with open(p, "w", encoding="utf-8") as f:
                    f.write(s_.replace(u"</svg>", u'<g id="photos">' + top + u"</g></svg>") if top else s_)
                continue
            cdir = os.path.join(pc_root(), PC_CACHE_DIR)
            os.makedirs(cdir, exist_ok=True)
            tp, sp = os.path.join(cdir, "photos_v1.py"), os.path.join(cdir, "photos_spec.json")
            with open(tp, "w", encoding="utf-8") as f:
                f.write(PC_PHOTO)
            with open(sp, "w") as f:
                json.dump(photos, f)
            cmds = [["py", "-3"], ["python"]]
            if os.path.basename(_sys.executable or "").lower().startswith("python"):
                cmds.insert(0, [_sys.executable])
            env = dict((k, v) for k, v in os.environ.items() if not k.upper().startswith("PYTHON"))
            ok = False
            for cmd in cmds:
                try:
                    r_ = subprocess.run(cmd + ["-I", tp, p, sp], capture_output=True, text=True, timeout=300, env=env, creationflags=PC_NOWIN)
                except Exception:
                    continue
                if r_.returncode == 0:
                    log.append(r_.stdout.strip() + u" in " + p)
                    ok = True
                    break
            if not ok:
                log.append(u"FLAG photos not placed in %s: no Python with PyMuPDF ran (pip install pymupdf)" % p)
        except Exception as ex:
            log.append(u"FLAG photos not placed in %s (%s: %s)" % (p, type(ex).__name__, ex))


def pc_present(pdf, slide, log):
    """v2, Aras 14 Nov 11:22 UTC: "in the output folder there should be a folder called presentation and in that folder
    each script output should be called by page name like page 1 is 1.pdf": a copy of the page's PDF as
    Downloads/Bergama/output/presentation/<slide>.pdf"""
    import shutil
    d = os.path.join(pc_root(), "output", "presentation")
    q = os.path.join(d, u"%d.pdf" % int(slide))
    try:
        os.makedirs(d, exist_ok=True)
        shutil.copyfile(pdf, q)
        log.append(u"presentation: %s" % q)
    except Exception as ex:
        log.append(u"FLAG presentation copy %s not written (%s: %s): close it in the PDF viewer and press again" % (
            q, type(ex).__name__, ex))
    return q


def pc_png(items, M, folder, name, log):
    """review PNGs by .NET System.Drawing (Rhino 8 on Windows): the whole sheet at most PC_PNG_TILE px long, then the
    sheet cut into tiles of at most PC_PNG_TILE x PC_PNG_TILE px at PC_PNG_PPI, trimmed to the sheet, nothing scaled down"""
    try:
        import clr
        clr.AddReference("System.Drawing")
        import System.Drawing as SD
        import System.Drawing.Drawing2D as SD2
        import System.Drawing.Text as SDT
        import System.Drawing.Imaging as SDI
    except Exception as ex:
        log.append(u"FLAG: review PNGs not written: System.Drawing not available (%s: %s)" % (type(ex).__name__, ex))
        return
    os.makedirs(folder, exist_ok=True)
    for old in glob.glob(os.path.join(folder, name + u"_*.png")):
        try:
            os.remove(old)
        except Exception:
            pass
    fonts = {}

    def col(h, a=255):
        h = (h or "000000").lstrip("#~")
        return SD.Color.FromArgb(a, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def render(path, ppmm, x0, y0, wpx, hpx):
        bmp = SD.Bitmap(int(wpx), int(hpx))
        g = SD.Graphics.FromImage(bmp)
        g.SmoothingMode = SD2.SmoothingMode.AntiAlias
        g.TextRenderingHint = SDT.TextRenderingHint.AntiAliasGridFit
        g.Clear(SD.Color.White)
        X = lambda x: float((x - x0) * ppmm)
        Y = lambda y: float(hpx - (y - y0) * ppmm)
        for it in items:
            t = it[0]
            if t == "poly":
                rings, fill, stroke, lw = it[1:5]
                gp = SD2.GraphicsPath(SD2.FillMode.Alternate)
                for R in rings:
                    if len(R) >= 3:
                        gp.AddPolygon(System_points(SD, [(X(p[0]), Y(p[1])) for p in R]))
                if fill:
                    g.FillPath(SD.SolidBrush(col(fill)), gp)
                if stroke and lw:
                    g.DrawPath(SD.Pen(col(stroke), float(max(lw * ppmm, 0.6))), gp)
            elif t == "line":
                pts, stroke, lw = it[1:4]
                if len(pts) < 2:
                    continue
                pen = SD.Pen(col(stroke), float(max((lw or 0.1) * ppmm, 0.6)))
                if isinstance(it[6], (tuple, list)):
                    w_ = max((lw or 0.1), 0.05)
                    pen.DashPattern = System_floats([max(it[6][0] / w_, 0.1), max(it[6][1] / w_, 0.1)])
                g.DrawLines(pen, System_points(SD, [(X(p[0]), Y(p[1])) for p in pts]))
            elif t == "text":
                s, x, y, size, color, bold, align = it[1:8]
                kf = (round(size * ppmm, 1), bool(bold))
                if kf not in fonts:
                    fonts[kf] = SD.Font("Arial", float(max(size * ppmm, 1.0)),
                                        SD.FontStyle.Bold if bold else SD.FontStyle.Regular, SD.GraphicsUnit.Pixel)
                f = fonts[kf]
                sz = g.MeasureString(s, f, SD.PointF(0, 0), SD.StringFormat.GenericTypographic)
                xx = X(x) - (sz.Width if align == "R" else sz.Width / 2.0 if align == "C" else 0.0)
                yy = Y(y) - size * ppmm * 0.905           # Arial ascent: the item's y is the baseline
                g.DrawString(s, f, SD.SolidBrush(col(color)), float(xx), float(yy), SD.StringFormat.GenericTypographic)
        g.Dispose()
        bmp.Save(path, SDI.ImageFormat.Png)
        bmp.Dispose()

    n = 0
    k_all = PC_PNG_TILE / max(M.w, M.h)
    render(os.path.join(folder, name + u"_00_whole.png"), k_all, 0.0, 0.0, M.w * k_all, M.h * k_all)
    ppmm = PC_PNG_PPI / 25.4
    tmm = PC_PNG_TILE / ppmm
    nx, ny = int(math.ceil(M.w / tmm)), int(math.ceil(M.h / tmm))
    for j in range(ny):
        for i in range(nx):
            x0, y1 = i * tmm, M.h - j * tmm                # row 1 = the top of the sheet
            w_, h_ = min(tmm, M.w - x0), min(tmm, y1)
            render(os.path.join(folder, u"%s_r%dc%d.png" % (name, j + 1, i + 1)), ppmm, x0, y1 - h_, w_ * ppmm,
                   h_ * ppmm)
            n += 1
    log.append(u"review PNGs: %s (%s_00_whole.png + %d tiles of at most %d px at %d ppi, rows from the top)" % (
        folder, name, n, PC_PNG_TILE, PC_PNG_PPI))


def System_points(SD, pts):
    import System
    arr = System.Array.CreateInstance(SD.PointF, len(pts))
    for i, (x, y) in enumerate(pts):
        arr[i] = SD.PointF(float(x), float(y))
    return arr


def System_floats(v):
    import System
    arr = System.Array.CreateInstance(System.Single, len(v))
    for i, x in enumerate(v):
        arr[i] = float(x)
    return arr


# ================================================================ v3.20: diagram kit (library/diagram_style/DIAGRAM_STYLE.md)
DG_W = {"cut": 0.70, "move": 0.22, "thin": 0.22, "arrow": 0.30, "hair": 0.10}   # v3.22: ground = 3 x the rest (Niarchos, measured)
DG_C = {"ink": "1E1E1E", "ground": "D9D4CA", "ctx": "B9B4AA", "her": "8E877C", "water": "A2B6B5",
        "water_ln": "3F86B8", "move": "C07A2E", "move_t": "EBCFAE", "bus": "8A8A8A", "paper": "FFFFFF"}


def pc_dg_kit(items, x0, y0, W, H, layer="concept", lw=192.0, lh=30.0, dash_at=6):
    """v3.20 (Aras 14 Nov 21:30 UTC "all the diagrams are awful"): one drawing kit for every explanatory diagram, the
    rules of library/diagram_style/DIAGRAM_STYLE.md: three weights (cut 0.70 / move 0.45 / thin 0.18), ground as poché,
    context as a regular row, ONE accent (DG_C move) for our move, water flat, at most 3 arrows and 4 labels.
    Local units: a lw x lh box at page (x0, y0), y up; returns a dict of drawing functions that append to items."""
    sx, sy = W / lw, H / lh
    P = lambda p: (x0 + p[0] * sx, y0 + p[1] * sy)
    C, Wt = DG_C, DG_W

    def line(pts, col=C["ink"], w=Wt["thin"], dash=None):
        d_ = list(dash) if dash else None                 # v3.21: dash at item[6] (Basemap writer: [4] = clip id);
        items.append(("line", [P(p) for p in pts], col, w, d_, layer, 1) if dash_at == 4 else   # the Sections writer
                     ("line", [P(p) for p in pts], col, w, None, layer, d_ or 1))                  # (nodes) reads [4]

    def poly(pts, fill, stroke=None, w=0.0):
        items.append(("poly", [[P(p) for p in pts]], fill, stroke, w if stroke else 0.0, None, layer, 1, None, None))

    def text(s, x, y, size=1.7, col=C["ink"], bold=True, al="L"):
        q = P((x, y))
        items.append(("text", s, q[0], q[1], size, col, bold, al, layer, None, None))

    def ground(pts, base=0.0):
        """the cut ground: poché down to base, then the one heavy line"""
        poly([(pts[0][0], base)] + list(pts) + [(pts[-1][0], base)], C["ground"])
        line(pts, C["ink"], Wt["cut"])

    def gy(pts, x):
        for a, b in zip(pts, pts[1:]):
            if a[0] <= x <= b[0] and b[0] > a[0]:
                return a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])
        return pts[0][1] if x < pts[0][0] else pts[-1][1]

    def city(gpts, xa, xb, step=4.0, h=2.6, focus=None, roof=True, col=None):
        """the town as a rhythm: one row of small blocks ON the ground, smaller away from focus (our move)"""
        col = col or C["ctx"]
        n = max(1, int((xb - xa) / step))
        span = max(abs(xa - (focus if focus is not None else xa)), abs(xb - (focus if focus is not None else xb)), 1.0)
        for i in range(n):
            x = xa + (i + 0.5) * (xb - xa) / n
            f = 1.0 if focus is None else 1.0 - 0.55 * abs(x - focus) / span
            w_, hh = step * 0.62 * f, h * f
            yb = gy(gpts, x)
            pts = [(x - w_ / 2, yb), (x + w_ / 2, yb), (x + w_ / 2, yb + hh)]
            pts += [(x, yb + hh + w_ * 0.45)] if roof else []
            poly(pts + [(x - w_ / 2, yb + hh)], col)

    def water(xa, xb, yb, yt, levels=()):
        """flat water, one hairline per named level (name at the right end)"""
        poly([(xa, yb), (xb, yb), (xb, yt), (xa, yt)], C["water"])
        for y, nm in levels:
            line([(xa, y), (xb, y)], C["water_ln"], Wt["hair"] * 2, (1.4, 0.9))
            text(nm, xb - 0.5, y + 0.6, 1.5, C["water_ln"], True, "R")

    def move(pts):
        """OUR move: the only accent shape"""
        poly(pts, C["move"], C["move"], Wt["move"])

    def steps(xa, xb, ya, yb, n, base=None, tint=True):
        """accent terraces from (xa, ya) down to (xb, yb), down to base: v3.22 a pale accent body with the accent
        tread line (the accent stays small, DIAGRAM_STYLE v2); tint=False = solid"""
        base = min(ya, yb) if base is None else base
        pts, y = [(xa, ya)], ya
        for i in range(n):
            x1 = xa + (xb - xa) * (i + 1) / float(n)
            y1 = ya + (yb - ya) * (i + 1) / float(n)
            pts += [(x1, y), (x1, y1)]
            y = y1
        if tint:
            poly(pts + [(xb, base), (xa, base)], C["move_t"])
            line(pts, C["move"], Wt["move"] * 2.0)
        else:
            move(pts + [(xb, base), (xa, base)])

    def arrow(a, b, kind="people"):
        col = {"people": C["move"], "water": C["water_ln"], "bus": C["bus"]}.get(kind, C["ink"])
        L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        hl, hw = 2.2, 0.9
        line([a, (b[0] - ux * hl * 0.8, b[1] - uy * hl * 0.8)], col, Wt["arrow"])
        poly([b, (b[0] - ux * hl - uy * hw, b[1] - uy * hl + ux * hw),
              (b[0] - ux * hl + uy * hw, b[1] - uy * hl - ux * hw)], col)

    def person(x, y, col=None):
        col = col or C["ink"]
        line([(x, y), (x, y + 1.7)], col, 0.3)
        line([(x - 0.5, y), (x, y + 0.8), (x + 0.5, y)], col, 0.22)
        poly([(x + 0.38 * math.cos(2 * math.pi * i / 10), y + 2.15 + 0.38 * math.sin(2 * math.pi * i / 10))
              for i in range(10)], col)

    def people(xs, y):
        for x in xs:
            person(x, y)

    def bracket(xa, xb, y, name, col=C["ink"]):
        """the 'agora' naming: a hairline span with end ticks, its name centred under it"""
        line([(xa, y + 0.8), (xa, y), (xb, y), (xb, y + 0.8)], col, Wt["hair"] * 1.5)
        text(name, (xa + xb) / 2.0, y - 2.0, 1.5, col, True, "C")

    def road(x, yb, h=6.0, w=3.0):
        """the driver at the frame edge: dense vertical hatching (the Niarchos highway)"""
        for i in range(9):
            xx = x + w * i / 8.0
            line([(xx, yb), (xx, yb + h * (0.75 + 0.25 * ((i * 7) % 5) / 4.0))], C["ink"], Wt["thin"])

    def label(s, x, y, accent=False, al="L"):
        text(s.upper(), x, y, 1.7, C["move"] if accent else C["ink"], True, al)

    def silhouette(kind, x, yb, s=1.0):
        """heritage as one recognisable outline, grey: dome, minaret, arch (bridge), basilica (Red Hall)"""
        if kind == "dome":
            poly([(x - 4 * s, yb), (x + 4 * s, yb), (x + 4 * s, yb + 3 * s)] +
                 [(x + 4 * s * math.cos(math.radians(a)), yb + 3 * s + 3 * s * math.sin(math.radians(a)))
                  for a in range(0, 181, 15)] + [(x - 4 * s, yb + 3 * s)], C["paper"], C["her"], Wt["thin"] * 1.4)
        elif kind == "minaret":
            poly([(x - 0.7 * s, yb), (x + 0.7 * s, yb), (x + 0.7 * s, yb + 11 * s), (x, yb + 13 * s),
                  (x - 0.7 * s, yb + 11 * s)], C["paper"], C["her"], Wt["thin"] * 1.4)
        elif kind == "mosque":
            poly([(x - 8 * s, yb), (x + 8 * s, yb), (x + 8 * s, yb + 4 * s), (x - 8 * s, yb + 4 * s)],
                 C["paper"], C["her"], Wt["thin"] * 1.4)
            poly([(x + 5 * s * math.cos(math.radians(a)), yb + 4 * s + 3.6 * s * math.sin(math.radians(a)))
                  for a in range(0, 181, 12)], C["paper"], C["her"], Wt["thin"] * 1.4)
        elif kind == "arches":                          # a stone bridge of n arches (deck at yb + 6 s)
            n_ = 3
            w_ = 16.0 * s
            top = yb + (w_ * 0.76 / n_ / 2.0) * 1.3 + 1.0 * s   # deck just over the arch crowns
            pts = [(x - w_ / 2, top), (x + w_ / 2, top), (x + w_ / 2, yb)]
            for i in range(n_ - 1, -1, -1):
                xa_ = x - w_ / 2 + w_ * (i + 0.12) / n_
                xb_ = x - w_ / 2 + w_ * (i + 0.88) / n_
                r_ = (xb_ - xa_) / 2
                pts += [(xb_, yb)] + [((xa_ + xb_) / 2 + r_ * math.cos(math.radians(a_)), yb + r_ * 1.3 *
                                       math.sin(math.radians(a_))) for a_ in range(0, 181, 15)] + [(xa_, yb)]
            poly(pts + [(x - w_ / 2, yb)], "E4E1DA", C["her"], Wt["thin"] * 1.4)
        elif kind == "basilica":
            poly([(x - 16 * s, yb), (x + 16 * s, yb), (x + 16 * s, yb + 11 * s), (x, yb + 14 * s),
                  (x - 16 * s, yb + 11 * s)], C["paper"], C["her"], Wt["move"])

    return {"line": line, "poly": poly, "text": text, "ground": ground, "gy": gy, "city": city, "water": water,
            "move": move, "steps": steps, "arrow": arrow, "person": person, "people": people, "bracket": bracket,
            "road": road, "label": label, "silhouette": silhouette, "C": C, "W": Wt}
