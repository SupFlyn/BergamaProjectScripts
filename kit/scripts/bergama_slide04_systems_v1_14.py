# -*- coding: utf-8 -*-
"""Bergama Group 6: SLIDE 04 SYSTEMS v1 (15 Nov 2026): Panel Review II slide 4, water / green / edges / public space,
ONE A3 landscape page (brief: "water/landscape/public space plan", perspectives marked V1, V2 on the plan).

Aras 15 Nov 08:42 UTC: "yes start that way, water enrichment building stays in that is the building near industrial
area ... it would serve as both industrial and education building, leave the placeholders".
  TOP     his masterplan (master.svg) over the whole site_alan strip, rendered by Edge / Chrome (nodes common
          svg_crop) with every layer of his drawing coloured by sub-system (SUB below): existing grey, water,
          cleaning planting, green + trees, edges, public space. Over it: the water enrichment + education building
          (his "desings" pieces inside the N6 frame, accent outline, "E"), the terrace close-up frame "D", V1 and V2,
          an edge arrow toward the fields fed (water balance farm extent). Scale = the largest 1:250 step that fits
          the sheet (1:2,000 would be 1.4 m long; Aras 14 Nov 15:25 "fit every drawing into A3's like the scale is
          not important"); the scale bar is true.
  BELOW   STORAGE (river months in / need months out with values, catch, stores by volume) | WATER CYCLE (one cut,
          8 numbered steps) | OUR STRIP (cut S4 in four seasons, v1.9; planting panel dropped) | D TERRACE CLOSE-UP (master.svg at 1:1,000,
          the terrace stretch outside every node frame with the most terrace pieces) | V1 and V2 perspective
          placeholders (Aras supplies the renders).
Every figure is read live: water_balance_results.json (Water balance script; the cloud default copy in Data/ only if
missing, FLAG), Data/water_balance_key_figures.json (farm extent), master.svg (tree counts), MasterplanBase cache.
The two strip storage figures are the rain/river analysis table (CONCEPT_RECORD.md: tables/A6_strip_storage.csv).
No sources on the sheet (Aras 14 Nov 15:23 UTC); they go to the log.

Outputs: Downloads/Bergama/output/bergama_slide04_systems/Slide04_systems.pdf + review/ PNGs; output/presentation/4.pdf.
Reads: Data/bergama_nodes_common.py (and what it loads), Data/assets/plan/master.svg, the MasterplanBase cache.
Grasshopper: a Button on any input runs it.
"""
import os, re, json, math, time

VERSION = "v1.14"   # v1.14 = Aras 15 Nov 17:06-17:07 UTC (standing, every drawing except slide 1): master.svg exactly as drawn, pasted inside the working area only: no sub-system recolouring, his ev-yol / builts2 shown, the crops clipped to the working area (Basemap cache calisma, an SVG clipPath in his own units), the base map hidden under it (white working-area paper), base map outside it; the sub-system colour swatches left the legend (his own colours now); v1.13 = the new masterplan (MasterplanBase v1.6, Aras 15 Nov 16:15): his "agaclar-2" is now "agaclar", "ordek" is gone; "kesin_yesil" is now a group holding one picture, which the sub-system filter still recolours (an SVG filter on a group works on the pixels of a picture inside it); v1.12 = own review of run v1.11 + Aras 15 Nov 15:57 UTC (line weights scale with the drawing size, pages_common v3.33 pc_stroke_k): every line of the three panels scaled by its drawing's stroke factor; month chart taller, ticks every 1,000 (thousand m3), small values with one decimal (no "0" for 45 m3); season intake arrows go into the ground toward the store, not into the air; v1.11 = Aras 15 Nov 15:53 UTC "dont make this logarithmic keep it linear": river in and need out on ONE linear scale (thousand m3), value on every bar; 15:54 "these numbers are so big make them smaller": storage words shorter and smaller, volumes as 8.64 MILLION / 26.7K (exact in the log); v1.10 = Aras 15 Nov 15:52 UTC "get rid of city feeding ... we give back to fields and orchads and thats it": no city blocks, no surplus pipe, step 7 = back to the river; v1.9 = Aras 15 Nov 15:41-15:47 UTC "we need more diagramatic drawings", "left side needs numbers", "how much water we can catch", planting panel "get rid of that ... explain our water cycle more in detail", "show out strip flows 4 seasons", "we give back to the strip": STORAGE = the month comparison with every value printed (thousand m3) and a value axis, the catch line (river take + site catch) and the stores hung under one ground line, length = volume; WATER CYCLE = one cut river > intake > ground store > strip > cleaning planting > E > fields > back to the river, numbered steps with their volumes; OUR STRIP = cut S4 four times (winter-autumn), stream depth, intake and the store giving back to the strip each season; planting panel dropped; v1.8 = Aras 15 Nov 15:16-15:19 UTC "take these perspectives either from archicad or rhino": V1 / V2 eye and look points (survey m), the E building rings and the V box sizes written to cached/bergama_perspectives/views_slide04.json for the Perspectives script (Rhino); its slide04_V1.png / slide04_V2.png placed in the V boxes when they exist, else the placeholder; no UNVERIFIED tags on the page (Aras 15:22 UTC "i dont want to see any placeholder"): DESIGN RANGE / DESIGN ESTIMATE / OUR PROPOSAL, the borehole note in the log; v1.7 = marker letters centred by pages_common pc_text_c (Aras 15 Nov 14:56 UTC "center the numbers in the boundries", standing); v1.6 = v1.6 = run 4 review: N1-N6 brackets and names just above the plan frame (unreadable over the base map); v1.5 = v1.5 = Aras 15 Nov 13:50 UTC "letters are not centered in the boxes": marker letters centred on their glyph box (measured width, cap height 0.72 x size); v1.4 = v1.4 = Aras 15 Nov 13:44 UTC "dont have a opaque background for texts in any single of the drawings": no box behind any text (placeholder label band gone, E ring and farm-feed boxes outline only); v1.3 = v1.3 = Aras 15 Nov 13:41-13:42 UTC "Every 3D, 2D or whatever the drawing is should use the basemap": the existing town is MapBase (A05 look) under his drawing, his own existing roads/buildings (ev-yol, builts2) hidden, the crops transparent; v1.2 = v1.2 = own review vs the liked set (WHY_WE_LIKED.md: the stream is the darkest shape on a white sheet, A05; everything named on the drawing, bracket naming): water a deep blue-grey ribbon, N1-N6 named by hairline brackets along the plan top; v1.1 = v1.1 = run 1 review: his tree drawings ("assets", 80k paths) coloured as green + trees; D picked by terrace + water-step + pier-edge pieces (run 1 found 1 terrace piece); the farm extent holds the site, so no edge arrow (log line, no FLAG)
SLIDE = 4
GH_LABEL = "Slide04"
OUT_FOLDER = "bergama_slide04_systems"
LOG_NAME = "bergama_slide04_systems_log.txt"
GH_INPUTS = {}
COMMON = os.path.join("Data", "bergama_nodes_common.py")
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
NAME = u"Slide04_systems"
PERSP_DIR = os.path.join(BERGAMA_ROOT, "cached", "bergama_perspectives")   # v1.8: views_slide04.json out, slide04_V1.png / slide04_V2.png in

PAGE_W, PAGE_H = 420.0, 297.0
MARGIN = 14.0
PLAN_TOP = 268.0                 # mm: top of the plan
PLAN_HMAX = 82.0                 # mm: the plan is at most this tall
DETAIL_DEN = 1000.0              # the terrace close-up scale
INK, GREY, ACC, WATER_LN = "2C2219", "6E675E", "C07A2E", "3F86B8"
WB_FILE = "water_balance_results.json"
WB_DEFAULT = os.path.join("Data", "water_balance_results_default.json")
WB_KEY = os.path.join("Data", "water_balance_key_figures.json")
SVG = os.path.join("Data", "assets", "plan", "master.svg")
# strip storage, 4 m reference strip, worst case (CONCEPT_RECORD.md "Strip losses" table, tables/A6_strip_storage.csv):
# "| **4 m (reference)** | 11,796 m² | 3,539 m³ | 18,208 / **26,675 m³** | 58,550 / **83,060 m³** |"
STRIP_SEALED_M3, STRIP_UNSEALED_M3 = 26675, 83060
STRIP_W, STRIP_D = 4.0, 0.30     # the summer strip, m (design; Sections STRIP_W, STRIP_D, case.md s.4)

# sub-systems: his layer ids (master.svg) -> colour pair (dark, light) of a duotone (his detail kept, one hue each);
# palette: project board + library/examples/palettes (5C7A86 CFDBE4, 3C4733, 89986A 70754C, 4C2528, C07A2E)
SUB = [
    ("existing", u"EXISTING", ("5E5A54", "FFFFFF"),
     ("heritage", "kizil_avlu")),
    ("water", u"WATER", ("24404D", "8FAAB8"),
     ("su_outline", "su_texture", "kaya", "Doldurma_renk")),
    ("clean", u"CLEANING PLANTING", ("2F3A28", "AFC2A6"),
     ("yosun", "bitki2")),
    ("green", u"GREEN + TREES", ("5E6440", "E3E6CF"),
     ("belki_yesil", "kesin_yesil", "agaclar", "agaclar-2", "assets")),
    ("edges", u"EDGES", ("4C2528", "E9DCD8"),
     ("tas", "istinaat", "iskele_kenari", "teras", "yol_kenar", "begum_su_merdiven")),
    ("public", u"PUBLIC SPACE", ("8A4E14", "F3E0C8"),
     ("circulation", "bina_cerceve", "kopruler", "bisiklet", "kanopi", "desings")),
]
JOBS = {"stone_pine": u"ROAD + WIND", "willow": u"WATER EDGE", "plane": u"WALKS", "olive": u"HERITAGE",
        "ash": u"MIXED GROVES", "tamarisk": u"MIXED GROVES", "rosemary": u"STRIPS UNDER 150 m2"}
HIDE = ("ev-yol", "builts2")   # his own copy of the existing town: MapBase draws it (Aras 13:41)
MONTHS = u"JFMAMJJASOND"
MON3 = (u"JAN", u"FEB", u"MAR", u"APR", u"MAY", u"JUN", u"JUL", u"AUG", u"SEP", u"OCT", u"NOV", u"DEC")


def hexmix(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    cb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return u"%02X%02X%02X" % tuple(int(round(x + (y - x) * t)) for x, y in zip(ca, cb))


def css_text(wa_svg):
    """v1.14: his drawing exactly as drawn, clipped to the working area (rings in his svg units)"""
    if not wa_svg:
        return u""
    pts = u"".join(u'<polygon points="%s"/>' % u" ".join(u"%.3f,%.3f" % q for q in R) for R in wa_svg)
    return (u'<defs><clipPath id="wa_clip" clipPathUnits="userSpaceOnUse">%s</clipPath></defs>'
            u'<style>:root > g{clip-path:url(#wa_clip)}</style>' % pts)


def css_text_subsystems():
    """v1.13 and older (kept for the record): each listed layer a duotone of its sub-system (lightness kept)"""
    f = []
    st = []
    for key, _, (dk, lt), ids in SUB:
        tv = lambda i: u"%.4f %.4f" % (int(dk[i:i + 2], 16) / 255.0, int(lt[i:i + 2], 16) / 255.0)
        f.append(u'<filter id="sub_%s" color-interpolation-filters="sRGB" x="0" y="0" width="1" height="1">'
                 u'<feColorMatrix type="matrix" values="0.2126 0.7152 0.0722 0 0 0.2126 0.7152 0.0722 0 0 '
                 u'0.2126 0.7152 0.0722 0 0 0 0 0 1 0"/><feComponentTransfer><feFuncR type="table" tableValues="%s"/>'
                 u'<feFuncG type="table" tableValues="%s"/><feFuncB type="table" tableValues="%s"/>'
                 u'</feComponentTransfer></filter>' % (key, tv(0), tv(2), tv(4)))
        st.append(u",".join(u'[id="%s"]' % i for i in ids) + u"{filter:url(#sub_%s)}" % key)
    st.append(u",".join(u'[id="%s"]' % i for i in HIDE) + u"{display:none}")
    return u"<defs>%s</defs><style>%s</style>" % (u"".join(f), u"".join(st))


def wb_load(root, log):
    """the Water balance results (live), else the cloud default copy (FLAG)"""
    for parts in (("cached", "Bergama_water_balance_analysis", WB_FILE), ("output", "Bergama_water_balance_analysis",
                                                                         WB_FILE)):
        p = os.path.join(root, *parts)
        if os.path.isfile(p):
            log.append(u"water balance: %s" % p)
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    p = os.path.join(root, WB_DEFAULT)
    log.append(u"FLAG water balance: no %s from the Water balance script; using the cloud default copy %s (24 Oct)" %
               (WB_FILE, p))
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def tree_counts(root, log):
    """trees per species in his master.svg planting group (<use> per trees_<species> group), with the group name"""
    p = os.path.join(root, SVG)
    with open(p, encoding="utf-8") as f:
        t = f.read()
    m = re.search(r'id="(PLANTING_[^"]*)"', t)
    out = []
    for g in re.finditer(r'<g[^>]*\bid="trees_([a-z_]+)"[^>]*>', t[m.start() if m else 0:]):
        s = (m.start() if m else 0) + g.end()
        depth, n = 1, 0
        for tag in re.finditer(r'<(/?)(g|use)\b[^>]*?(/?)>', t[s:s + 20000000]):
            if tag.group(2) == "use":
                n += 0 if tag.group(1) else 1
            elif tag.group(1):
                depth -= 1
                if depth == 0:
                    break
            elif not tag.group(3):
                depth += 1
        out.append((g.group(1), n))
    log.append(u"trees in master.svg %s: %s" % (m.group(1) if m else u"(no PLANTING group)",
                                                 u", ".join(u"%s %d" % c for c in out)))
    if not out:
        log.append(u"FLAG no trees_<species> groups found in %s" % p)
    return (m.group(1) if m else u""), out


def span_name(flags):
    """months where flags is True as 'NOV-APR' (one run, wrapping over the year end) or None"""
    on = [i for i in range(12) if flags[i]]
    if not on or len(on) == 12:
        return None
    start = next(i for i in range(12) if flags[i] and not flags[i - 1])
    end = start
    while flags[(end + 1) % 12]:
        end = (end + 1) % 12
    if sum(1 for i in range(12) if flags[i]) != (end - start) % 12 + 1:
        return None
    return u"%s-%s" % (MON3[start], MON3[end])


def inside(p, R):
    c = False
    j = len(R) - 1
    for i in range(len(R)):
        if (R[i][1] > p[1]) != (R[j][1] > p[1]) and \
                p[0] < (R[j][0] - R[i][0]) * (p[1] - R[i][1]) / (R[j][1] - R[i][1]) + R[i][0]:
            c = not c
        j = i
    return c


def short(v):
    """v1.11: a volume for the page, short: 8.64 MILLION, 26.7K, 363K (the exact value goes to the log)"""
    if v >= 1e6:
        return u"%.2f MILLION" % (v / 1e6)
    if v >= 1e5:
        return u"%dK" % int(round(v / 1e3))
    if v >= 1e3:
        return (u"%.1f" % (v / 1e3)).rstrip(u"0").rstrip(u".") + u"K"
    return fmt(v)


def fmt(v):
    return format(int(round(v)), ",d")


def main():
    t0 = time.time()
    log = []
    p = os.path.join(BERGAMA_ROOT, COMMON)
    if not os.path.isfile(p):
        raise RuntimeError(u"%s missing: run Bergama.bat once (the kit copies it), then press again" % p)
    NC = {"__name__": "bergama_nodes_common"}
    with open(p, encoding="utf-8") as f:
        exec(compile(f.read(), p, "exec"), NC)
    log.append(u"common: %s (%s)" % (p, NC.get("NC_VERSION")))
    root = NC["ROOT"]
    T_, L_, R_, ring, box, wrap = NC["T_"], NC["L_"], NC["R_"], NC["ring"], NC["box"], NC["wrap"]
    P, B, X, G, SL, D = NC["load_all"]("N6", OUT_FOLDER, log)       # loads the shared code (node name: caches only)
    tw = B["text_w"]
    items = []

    def arrow(a, b, col, lw=0.35, hl=2.2, hw=0.9, layer="marks"):
        L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
        ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
        items.append(L_([a, (b[0] - ux * hl * 0.8, b[1] - uy * hl * 0.8)], col, lw, layer))
        items.append(R_([[b, (b[0] - ux * hl - uy * hw, b[1] - uy * hl + ux * hw),
                          (b[0] - ux * hl + uy * hw, b[1] - uy * hl - ux * hw)]], col, None, 0.0, layer))

    def ctext(s, cx, cy, size, col, layer):
        """a marker letter centred on (cx, cy): left-aligned at half its measured width, baseline at half the cap height"""
        items.append(G["pc_text_c"](s, cx, cy, size, col, layer))   # v1.7: the shared centred mark

    def para(s, x, y, size, width, col=INK, bold=False, layer="text"):
        for ln in wrap(B, s, size, width, bold):
            items.append(T_(ln, x, y, size, col, bold, "L", layer))
            y -= size * 1.4
        return y

    def vmark(q, look, name):
        """viewpoint: accent dot, a short view cone toward look, its name"""
        L = math.hypot(look[0] - q[0], look[1] - q[1]) or 1.0
        ux, uy = (look[0] - q[0]) / L, (look[1] - q[1]) / L
        a = (q[0] + ux * 5.0 - uy * 2.0, q[1] + uy * 5.0 + ux * 2.0)
        b = (q[0] + ux * 5.0 + uy * 2.0, q[1] + uy * 5.0 - ux * 2.0)
        items.append(R_([[q, a, b]], hexmix(ACC, "FFFFFF", 0.55), ACC, 0.2, "viewpoints"))
        items.append(R_([ring(q[0], q[1], 1.1, 24)], ACC, "FFFFFF", 0.2, "viewpoints"))
        items.append(T_(name, q[0] - ux * 2.2 - 1.5, q[1] - uy * 2.2 - 1.0, 2.4, ACC, True, "C", "viewpoints"))

    # ---------------------------------------------------------------- the plan: site_alan strip, his drawing
    M0 = G["pc_site_map"](7500, log)
    F = M0.F
    fw = PAGE_W - 2 * MARGIN
    den = max(F.w * 1000.0 / fw, F.h * 1000.0 / PLAN_HMAX)
    den = math.ceil(den / 250.0) * 250.0
    k = 1000.0 / den
    X0 = (PAGE_W - F.w * k) / 2.0
    Y1 = PLAN_TOP
    Y0 = Y1 - F.h * k
    PB = (X0, Y0, X0 + F.w * k, Y1)
    pgS = lambda xy: (X0 + F.local(xy)[0] * k, Y0 + F.local(xy)[1] * k)
    log.append(u"plan: site_alan %.0f x %.0f m at 1:%s = %.0f x %.0f mm (1:2,000 would be %.0f mm long)" % (
        F.w, F.h, fmt(den), F.w * k, F.h * k, F.w / 2.0))

    def back(u, v):                                       # local m -> survey m (inverse of F.local)
        rx, ry = u + F.u0, v + F.v0
        return (F.ca * rx + F.sa * ry, -F.sa * rx + F.ca * ry)

    MPn, MPC = G["pc_mp_data"](log)
    # v1.14: the working area (Basemap cache calisma, survey m) -> his svg units for the crop clip; white paper over
    # the base map inside it
    class _Id(object):
        T = staticmethod(lambda q: (q[0], q[1]))
    WA = G["pc_wa_rings"](_Id(), log) if "pc_wa_rings" in G else []
    a_, b_, c_, d_, e_, f_ = MPC["matrix"]
    det = a_ * d_ - b_ * c_
    wa_svg = [[((d_ * (X - e_) - c_ * (Y - f_)) / det, (-b_ * (X - e_) + a_ * (Y - f_)) / det) for X, Y in R]
              for R in WA] if det else []
    if not WA:
        log.append(u"FLAG plan: no working area (press Basemap once, pages_common v3.34): master.svg shown unclipped")
    CSS = css_text(wa_svg)
    wa_paper = lambda T: [R_([[T(q) for q in R] for R in WA], "FFFFFF", None, 0.0, "wa_paper", True)] if WA else []
    MB = NC["load_mb"](log)                               # the base map under every drawing (Aras 13:41-13:42)
    MC = MB["mb_load"](log)
    if MC is None:
        raise RuntimeError(u"MapBase cache missing: press MapBase once, then this page")
    items += NC["clip_plan"](B, NC["mb_plan"](MB, MC, F, pgS, k, PB, B, P, log)[0] + wa_paper(pgS), PB, log)
    png = NC["svg_crop"](u"slide04_plan", MPC["matrix"], pgS, PB, log, css=CSS, bg=False)
    if png:
        items.append(("image", X0, Y0, F.w * k, F.h * k, png, None, False, None, "masterplan_svg"))
    else:                                                 # his drawing as vector pieces, same colours by layer word
        log.append(u"FLAG plan: no crop, the MasterplanBase pieces are drawn instead (no trees in that cache)")
        fills = {}
        for key, _, (dk, lt), ids in SUB:
            for i in ids:
                fills[i] = hexmix(dk, lt, 0.55)
        MPn["mp_draw"](MPC, items, pgS, k, PB, None, style={"fill": fills, "stroke": fills, "area": fills})
    items.append(R_([box(*PB)], None, INK, 0.3, "map_frame"))

    # ---- node frames (u ranges), the building, the terrace close-up
    nodes = {}
    for n, nd in sorted(SL["nodes"].items()):
        us = [F.local(tuple(c))[0] for c in nd["corners"]]
        nodes[n] = (min(us), max(us), [tuple(c) for c in nd["corners"]])
    big = lambda P_: abs(sum(P_[i][0] * P_[i - 1][1] - P_[i - 1][0] * P_[i][1] for i in range(len(P_)))) / 2.0 > \
        NC["MP_MAX_M2"]
    cen = lambda P_: (sum(q[0] for q in P_) / len(P_), sum(q[1] for q in P_) / len(P_))
    # node names by hairline brackets along the top of the plan (the 'agora' naming, DIAGRAM_STYLE; liked set: named)
    for n, (a_, b_, _) in sorted(nodes.items()):
        xa, xb = X0 + max(a_, 0.0) * k + 0.6, X0 + min(b_, F.w) * k - 0.6
        if xb - xa < 4.0:
            continue
        yb_ = Y1 + 1.4                                   # v1.6: above the frame, ticks down toward it
        items.append(L_([(xa, yb_ - 0.8), (xa, yb_), (xb, yb_), (xb, yb_ - 0.8)], INK, 0.15, "node_names"))
        items.append(T_(n, (xa + xb) / 2.0 - tw(n, 2.0, True) / 2.0, yb_ + 0.9, 2.0, INK, True, "L", "node_names"))
    # E: his proposed buildings ("desings") inside the N6 frame = the water enrichment + education building
    bld = []
    for key, recs in MPC["layers"].items():
        if key.split("/")[0] != "desings":
            continue
        for e in recs:
            if len(e[4]) >= 3 and not big(e[4]) and "N6" in nodes and inside(cen(e[4]), nodes["N6"][2]):
                bld.append(e[4])
    if bld:
        for P_ in bld:
            items.append(R_([[pgS(q) for q in P_]], None, ACC, 0.35, "building_E"))
        allq = [pgS(q) for P_ in bld for q in P_]
        bx = (min(q[0] for q in allq), min(q[1] for q in allq), max(q[0] for q in allq), max(q[1] for q in allq))
        ec = ((bx[0] + bx[2]) / 2.0, bx[3] + 3.2 if bx[3] + 4.5 < Y1 else bx[1] - 3.2)
        items.append(R_([ring(ec[0], ec[1], 1.9, 32)], None, ACC, 0.3, "building_E"))
        ctext(u"E", ec[0], ec[1], 2.4, ACC, "building_E")
        bc_s = cen([q for P_ in bld for q in P_])
        log.append(u"E: %d 'desings' piece(s) inside the N6 frame, %.0f x %.0f m on the plan box, centre %.1f, %.1f" % (
            len(bld), (bx[2] - bx[0]) / k, (bx[3] - bx[1]) / k, bc_s[0], bc_s[1]))
    else:
        bc_s = None
        log.append(u"FLAG E: no 'desings' piece of his masterplan inside the N6 frame: the water enrichment building is "
                   u"not marked (ask Aras where it is)")

    # D: the terrace close-up (box size from its panel), the terrace stretch outside every node frame
    col_w = (fw - 8.0) / 3.0
    cols = [MARGIN + i * (col_w + 4.0) for i in range(3)]
    row2 = (MARGIN, Y0 - 24.0 - (Y0 - 24.0 - MARGIN - 6.0) / 2.0)   # bottom row y0, y1 (top row above it)
    row1 = (row2[1] + 6.0, Y0 - 24.0)
    dbox = (cols[0], row2[0], cols[0] + col_w, row2[1] - 8.0)
    k2 = 1000.0 / DETAIL_DEN
    Wm, Hm = (dbox[2] - dbox[0]) / k2, (dbox[3] - dbox[1]) / k2
    ter = [cen([F.local(q) for q in e[4]]) for key, recs in MPC["layers"].items() if set(key.split("/")) & {"teras", "begum_su_merdiven", "iskele_kenari"}
           for e in recs if len(e[4]) >= 2 and not big(e[4])]
    free = lambda ua: all(ua + Wm <= a or ua >= b for a, b, _ in nodes.values())
    best = None
    ua = 0.0
    while ua + Wm <= F.w:
        if free(ua):
            n_ = sum(1 for q in ter if ua <= q[0] <= ua + Wm)
            if n_ and (best is None or n_ > best[0]):
                best = (n_, ua)
        ua += 10.0
    D_ok = best is not None
    VIEWS = {}                                            # v1.8: for the Perspectives script
    log.append(u"UNVERIFIED: the fields + strip range and the storage volume wait on borehole tests (log only; the page says design range / estimate)")
    if D_ok:
        ua = best[1]
        vs = sorted(q[1] for q in ter if ua <= q[0] <= ua + Wm)
        vc = vs[len(vs) // 2]
        va = min(max(vc - Hm / 2.0, 0.0), max(F.h - Hm, 0.0))
        log.append(u"D: %d terrace / water-step / pier-edge pieces in u %.0f-%.0f m, v %.0f-%.0f m (outside N1-N6)" % (best[0], ua, ua + Wm, va,
                                                                                                va + Hm))
        dr = (X0 + ua * k, Y0 + va * k, X0 + (ua + Wm) * k, Y0 + min(va + Hm, F.h) * k)
        items.append(R_([box(*dr)], None, ACC, 0.3, "detail_D"))
        items.append(T_(u"D", dr[0] + 0.6, dr[3] + 1.0, 2.4, ACC, True, "L", "detail_D"))
        q1 = (X0 + (ua + Wm * 0.12) * k, Y0 + vc * k)
        vmark(q1, (X0 + (ua + Wm * 0.6) * k, Y0 + vc * k), u"V1")
        VIEWS["V1"] = dict(eye=back(ua + Wm * 0.12, vc), look=back(ua + Wm * 0.6, vc))
    else:
        log.append(u"FLAG D: no terrace pieces outside the node frames: no close-up")
    if bc_s is not None:
        CL = G["pc_selinos_line"]()
        cp = min(CL, key=lambda q: math.hypot(q[0] - bc_s[0], q[1] - bc_s[1]))
        bq, cq = pgS(bc_s), pgS(cp)
        d_ = math.hypot(cq[0] - bq[0], cq[1] - bq[1]) or 1.0
        q2 = (cq[0] + (cq[0] - bq[0]) / d_ * 3.0, cq[1] + (cq[1] - bq[1]) / d_ * 3.0)   # just over the stream
        q2 = (min(max(q2[0], PB[0] + 4.0), PB[2] - 4.0), min(max(q2[1], PB[1] + 4.0), PB[3] - 4.0))
        vmark(q2, bq, u"V2")
        VIEWS["V2"] = dict(eye=back((q2[0] - X0) / k, (q2[1] - Y0) / k), look=tuple(bc_s), building=[[list(q) for q in P_] for P_ in bld])

    # the fields fed: an edge arrow toward the farm extent (water balance key figures)
    try:
        with open(os.path.join(root, WB_KEY), encoding="utf-8") as f:
            KF = json.load(f)
        fc = cen([tuple(c) for c in KF["farms_fed"]["corners_survey_xy"]])
        a_ = F.local(back(F.w / 2.0, F.h / 2.0))
        b_ = F.local(fc)
        if 0 <= b_[0] <= F.w and 0 <= b_[1] <= F.h:
            log.append(u"fields: the farm extent (around2.pdf) holds the site: no edge arrow")
        else:
            dx, dy = b_[0] - a_[0], b_[1] - a_[1]
            t = min([v for v in ((F.w - a_[0]) / dx if dx > 0 else (-a_[0] / dx if dx < 0 else 9e9),
                                 (F.h - a_[1]) / dy if dy > 0 else (-a_[1] / dy if dy < 0 else 9e9)) if v > 0])
            ex = (a_[0] + dx * t, a_[1] + dy * t)
            L = math.hypot(dx, dy)
            ux, uy = dx / L, dy / L
            tip = (X0 + ex[0] * k - ux * 1.0, Y0 + ex[1] * k - uy * 1.0)
            tail = (tip[0] - ux * 14.0, tip[1] - uy * 14.0)
            arrow(tail, tip, WATER_LN, 0.5, 2.6, 1.2, "fields")
            dist = math.hypot(fc[0] - back(*ex)[0], fc[1] - back(*ex)[1])
            lab = u"TO THE FIELDS"
            lx = tail[0] - (tw(lab, 2.0, True) + 1.5 if ux > 0 else -1.5)
            items.append(T_(lab, min(max(lx, PB[0] + 1.0), PB[2] - tw(lab, 2.0, True) - 1.0),
                            tail[1] - 0.7, 2.0, WATER_LN, True, "L", "fields"))
            log.append(u"fields: farm extent centre %.0f, %.0f (around2.pdf, %s ha); %.0f m beyond the site edge "
                       u"(calculated)" % (fc[0], fc[1], KF["farms_fed"]["area_ha"], dist))
    except Exception as ex_:
        log.append(u"FLAG fields arrow not drawn (%s: %s)" % (type(ex_).__name__, ex_))

    # ---- legend row + scale + north under the plan
    yl = Y0 - 9.0
    x = MARGIN
    for sym, nm in ((u"E", u"WATER ENRICHMENT + EDUCATION BUILDING (PROPOSAL)"), (u"D", u"TERRACE CLOSE-UP"),
                    (u"V", u"VIEWPOINT")):
        if sym == u"V":
            items.append(R_([ring(x + 1.6, yl + 1.6, 1.1, 24)], ACC, None, 0.0, "legend"))
        else:
            items.append(R_([box(x, yl, x + 3.2, yl + 3.2)], None, ACC, 0.3, "legend"))
            ctext(sym, x + 1.6, yl + 1.6, 2.0, ACC, "legend")
        items.append(T_(nm, x + 4.5, yl + 0.6, 2.0, INK, True, "L", "legend"))
        x += 4.5 + tw(nm, 2.0, True) + 5.0
    sn = NC["scale_north"](F, den, PAGE_W - MARGIN, Y0 - 17.0)
    sx0 = min(it[2] for it in sn if it[0] == "text") if sn else PAGE_W
    items += sn
    items.append(T_(u"1:%s" % fmt(den), PAGE_W - MARGIN, Y0 - 3.6, 2.0, INK, True, "R", "scale_north"))
    if x > sx0 - 22.0:
        log.append(u"FLAG legend row (to x %.0f mm) runs into the scale bar (from %.0f mm)" % (x, sx0 - 20.0))

    def panel_title(x0, y1, head, claim):
        items.append(T_(u"%s · %s" % (head, claim), x0, y1 - 3.0, 2.8, INK, True, "L", "titles"))
        items.append(L_([(x0, y1 - 5.0), (x0 + col_w, y1 - 5.0)], INK, 0.15, "titles"))
        return y1 - 9.0

    WB = wb_load(root, log)
    dz = WB["design"]
    mix = dz.get("mix") or list(WB["farm_demand_m3"].keys())[0]
    river = WB["river_month_m3"]
    need = [a + b for a, b in zip(WB["strip_month_m3"], WB["farm_demand_month_m3"][mix]["mean"])]
    flow_on = span_name([v > 0 for v in river])
    dry = span_name([v <= 0 for v in river])

    # ---------------------------------------------------------------- A STORAGE (v1.9: numbered months + the store cut)
    n_panels = len(items)                                 # v1.12: stroke scaling from here
    x0, y1 = cols[0], row1[1]
    y = panel_title(x0, y1, u"STORAGE", u"WINTER WATER CARRIES THE DRY SUMMER")
    Hn = y - row1[0]
    catch_r = sum(river)                                  # river water we can take a year (calculated: sum of river_month_m3)
    catch_s = WB.get("site_catch_m3_per_year", 0)
    fd = WB["farm_demand_m3"][mix]["mean"]
    need_y = WB["strip_m3_per_year"] + fd                 # calculated: strip + fields mean
    lab_w = 15.0
    cw = (col_w - lab_w) / 12.0
    ch = Hn * 0.66                                        # the month chart's share of the panel
    rmax = float(max(max(river), max(need)) or 1.0)       # v1.11: one linear scale for in and out
    rh = ch - 13.0                                        # bar room above the axis
    nh = rh * max(need) / rmax                            # need out to the same scale (small: that is the picture)
    nmax = rmax
    ax = y - 3.0 - rh * max(river) / rmax                 # month axis
    k_ = 1000.0

    def nice(vmax):
        raw = vmax / 3.5
        mag = 10 ** math.floor(math.log10(raw))
        return next(m * mag for m in (1, 2, 5, 10) if m * mag >= raw)
    def kv(v):                                            # v1.12: thousand m3, small ones with a decimal
        t = v / k_
        return u"<0.1" if t < 0.1 else (u"%.1f" % t if t < 10 else fmt(t))
    for top_, h_, vmax, sgn, col_ in ((ax + 0.4, rh, rmax, 1, WATER_LN),):
        st = nice(vmax)
        v = st
        while v <= vmax * 1.001:                          # value axis: ticks + numbers (thousand m3)
            yy = top_ + sgn * h_ * v / vmax
            items.append(L_([(x0 + lab_w - 0.8, yy), (x0 + col_w, yy)], "D8D4CC", 0.1, "storage"))
            items.append(T_(fmt(v / k_), x0 + lab_w - 1.2, yy - 0.5, 1.4, col_, True, "R", "storage"))
            v += st
    for i in range(12):
        xa = x0 + lab_w + i * cw
        if river[i] > 0:
            h = rh * river[i] / rmax
            items.append(R_([box(xa + 0.6, ax + 0.4, xa + cw - 0.6, ax + 0.4 + h)], "A2B6B5", None, 0.0, "storage"))
            items.append(T_(kv(river[i]), xa + cw / 2.0, ax + 1.0 + h, 1.4, WATER_LN, True, "C", "storage"))
        if need[i] > 0:
            h = rh * need[i] / rmax                       # v1.11: the river's scale
            items.append(R_([box(xa + 0.6, ax - 0.4 - h, xa + cw - 0.6, ax - 0.4)], hexmix(ACC, "FFFFFF", 0.35), None,
                            0.0, "storage"))
            items.append(T_(kv(need[i]), xa + cw / 2.0, ax - 2.3 - h, 1.4, ACC, True, "C", "storage"))
        items.append(T_(MONTHS[i], xa + cw / 2.0, ax - nh - 5.0, 1.7, GREY, True, "C", "storage"))
    items.append(L_([(x0 + lab_w, ax), (x0 + col_w, ax)], INK, 0.5, "storage"))
    items.append(T_(u"RIVER IN", x0, y - 1.0, 1.6, WATER_LN, True, "L", "storage"))
    items.append(T_(u"NEED OUT", x0, ax - 2.6, 1.6, ACC, True, "L", "storage"))
    items.append(T_(u"THOUSAND m3 A MONTH · ONE SCALE", x0 + col_w, y + 0.6, 1.4, GREY, True, "R",
                    "storage"))
    # the volumes: one ground line, each store hangs under it, length = volume (one scale)
    yv = ax - nh - 8.4
    yv = para(u"WE CAN CATCH %s m3 A YEAR FROM THE RIVER (%s) + %s m3 SITE CATCH: THE STORE IS THE LIMIT" % (
        short(catch_r), flow_on or u"", short(catch_s)), x0, yv, 1.4, col_w, INK, True, "storage") - 0.6
    items.append(L_([(x0, yv), (x0 + col_w, yv)], INK, 0.7, "storage"))
    lo, hi = dz["central_range_m3"]
    vb = [(STRIP_SEALED_M3, None, "A2B6B5", u"%s m3 · STRIP STORE TODAY" % short(STRIP_SEALED_M3)),
          (STRIP_UNSEALED_M3, None, "A2B6B5", u"%s m3 · STRIP STORE, UNSEALED BED" % short(STRIP_UNSEALED_M3)),
          (hi, lo, hexmix(ACC, "FFFFFF", 0.35), u"%s-%s m3 · GROUND STORE (DESIGN ESTIMATE)" % (
              short(lo).rstrip(u"K"), short(hi))),
          (need_y, None, None, u"%s m3 A YEAR · NEED: STRIP + FIELDS" % short(need_y))]
    lw_max = max(tw(b[3], 1.3, True) for b in vb) + 2.0
    vmax = float(max(b[0] for b in vb))
    sc = (col_w - lw_max) / vmax
    yb = yv - 0.5
    for v, v0, fill, nm in vb:
        L = sc * v
        if fill:
            items.append(R_([box(x0, yb - 2.0, x0 + L, yb)], fill, None, 0.0, "storage"))
        else:
            items.append(R_([box(x0, yb - 2.0, x0 + L, yb)], None, ACC, 0.25, "storage"))
        if v0 is not None:
            items.append(L_([(x0 + sc * v0, yb - 2.0), (x0 + sc * v0, yb)], "FFFFFF", 0.3, "storage"))
        items.append(T_(nm, x0 + L + 2.0, yb - 1.5, 1.3, INK, True, "L", "storage"))
        yb -= 3.0
    yb = para(u"DESIGN ESTIMATE: SIZED BY COST AGAINST RECYCLED WATER; MEETS %s %% OF THE NEED IN A 1-IN-5 DRY YEAR"
              % dz.get("covered_pct_1in5_dry", u""), x0, yb - 1.2, 1.25, col_w, GREY, True, "storage")
    if yb < row1[0] - 0.5:
        log.append(u"FLAG storage panel runs %.1f mm below its row" % (row1[0] - yb))
    log.append(u"storage: river months %s, dry %s; catch %s m3/yr = sum of river_month_m3 (water balance: river water "
               u"an intake can take) + site catch %s m3/yr; need %s m3/yr = strip + fields '%s' mean (calculated); "
               u"design %s m3 (%s)" % (flow_on, dry, fmt(catch_r), fmt(catch_s), fmt(need_y), mix,
                                       fmt(dz["storage_m3"]), dz.get("note", u"")))

    # ---------------------------------------------------------------- B WATER CYCLE (v1.9: one cut, river to fields and back)
    x0 = cols[1]
    y = panel_title(x0, y1, u"WATER CYCLE", u"RIVER, STORE, STRIP, FIELDS AND BACK")
    lands = WB["lands"]
    cut = WB.get("cutoff", {}).get(mix, {}).get(dz.get("case", "central"), {})
    back_m3 = cut.get("released_365d_m3_per_year")
    sh = 26.0                                             # the cut's height
    sb = y - sh
    K = G["pc_dg_kit"](items, x0, sb, col_w, sh, "cycle", lw=col_w, lh=sh, dash_at=4)
    C = K["C"]
    gl = 12.0
    gp = [(0.0, gl - 5.0), (10.0, gl - 5.0), (13.0, gl), (18.0, gl), (18.0, gl - 1.6), (26.0, gl - 1.6), (26.0, gl),
          (col_w, gl)]
    K["water"](0.0, 11.0, gl - 5.0, gl - 1.5)              # the Selinos at the frame edge (the driver)
    K["ground"](gp, gl - 11.0)
    K["poly"]([(18.0, gl - 1.6), (26.0, gl - 1.6), (26.0, gl - 0.4), (18.0, gl - 0.4)], C["water"])   # the strip
    K["line"]([(18.0, gl), (18.0, gl - 1.6), (26.0, gl - 1.6), (26.0, gl)], C["move"], 0.45)
    K["poly"]([(16.0, gl - 3.5), (50.0, gl - 3.5), (50.0, gl - 9.5), (16.0, gl - 9.5)], C["water"], C["move"], 0.45)
    for i in range(14):                                   # cleaning + scenting planting along the strip: a reed row
        xx = 27.5 + i * 0.95
        K["line"]([(xx, gl), (xx + 0.3 * ((i % 3) - 1), gl + 2.0 + 0.6 * (i % 2))], "2F3A28", 0.22)
    K["poly"]([(56.0, gl), (68.0, gl), (68.0, gl + 7.0), (56.0, gl + 7.0)], hexmix(ACC, "FFFFFF", 0.8), C["move"], 0.45)
    ctext(u"E", x0 + 62.0, sb + gl + 3.5, 2.4, ACC, "cycle")
    for i in range(28):                                   # fields: crop rows, then a few orchard trees
        xx = 72.0 + i * 1.5
        K["line"]([(xx, gl), (xx, gl + 1.2)], "5E6440", 0.3)
    for xx in (114.0, 117.5, 121.0, 124.5):
        K["line"]([(xx, gl), (xx, gl + 1.6)], "5E6440", 0.25)
        K["poly"]([(xx + 1.1 * math.cos(2 * math.pi * j / 10), gl + 2.5 + 1.1 * math.sin(2 * math.pi * j / 10))
                   for j in range(10)], "89986A")
    K["arrow"]((7.0, gl - 2.6), (16.5, gl - 5.0), "water")                          # 1 intake
    K["arrow"]((22.0, gl - 3.7), (22.0, gl - 0.6), "water")                         # 3 store -> strip
    K["line"]([(50.0, gl - 6.0), (62.0, gl - 6.0)], C["water_ln"], 0.3)
    K["arrow"]((62.0, gl - 6.0), (62.0, gl - 0.2), "water")                         # store -> E
    K["arrow"]((68.5, gl + 2.0), (78.0, gl + 2.0), "water")                         # 6 E -> fields
    K["arrow"]((17.5, gl - 1.0), (11.5, gl - 2.0), "water")                         # 7 back to the river
    marks = [(1, 4.0, gl + 3.5), (2, 33.0, gl - 6.5), (3, 22.0, gl + 3.5), (4, 34.0, gl + 5.5), (5, 62.0, gl + 10.0),
             (6, 86.0, gl + 6.0), (7, 12.5, gl + 6.5)]
    for n_, mx, my in marks:
        q = (x0 + mx, sb + my)
        items.append(R_([ring(q[0], q[1], 1.5, 28)], None, INK, 0.2, "cycle"))
        ctext(u"%d" % n_, q[0], q[1], 1.7, INK, "cycle")
    fmon = span_name([v > 0 for v in WB["farm_demand_month_m3"][mix]["mean"]])
    smon = span_name([v > 0 for v in WB["strip_month_m3"]])
    steps_ = [u"1 INTAKE %s · WE CAN TAKE %s m3 A YEAR" % (flow_on or u"", short(catch_r)),
              u"2 GROUND STORE · %s m3 (DESIGN ESTIMATE)" % short(dz["storage_m3"]),
              u"3 STRIP %s · %s m3 A YEAR GIVEN BACK FROM THE STORE" % (smon or u"", short(WB["strip_m3_per_year"])),
              u"4 CLEANING + SCENTING PLANTING ALONG THE STRIP",
              u"5 E · WATER ENRICHMENT + EDUCATION (OUR PROPOSAL): ENRICHES THE IRRIGATION LINE ONLY",
              u"6 FIELDS %s · %s ha CROPLAND + %s ha ORCHARD · %s m3 A YEAR" % (
                  fmon or u"", lands["cropland_ha"], lands["orchard_ha"], short(fd)),
              u"7 BACK TO THE RIVER · %s m3 A YEAR OF STORED WATER OLDER THAN 365 DAYS" % short(back_m3)
              if back_m3 else u"7 BACK TO THE RIVER · STORED WATER OLDER THAN 365 DAYS"]
    hw = (col_w - 4.0) / 2.0
    ya = yb_ = sb - 3.0
    for i, s in enumerate(steps_):
        xx = x0 + (0.0 if i < 4 else hw + 4.0)
        if i == 4:
            ya, yb_ = yb_, ya
        yb_ = para(s, xx, yb_, 1.5, hw, INK, True, "cycle") - 0.9
    yt = min(ya, yb_)
    if yt < row1[0] - 0.5:
        log.append(u"FLAG water cycle panel runs %.1f mm below its row" % (row1[0] - yt))
    log.append(u"water cycle: lands %s ha cropland + %s ha orchard (around2.pdf), fields '%s' mean %s m3/yr %s, strip "
               u"%s m3/yr %s, back to the river %s m3/yr (cutoff released_365d); no city feed (Aras 15:52)" % (lands["cropland_ha"], lands["orchard_ha"], mix, fmt(fd), fmon,
                                         fmt(WB["strip_m3_per_year"]), smon, back_m3))

    # ---------------------------------------------------------------- C THE STRIP IN FOUR SEASONS (v1.9, replaces planting)
    x0 = cols[2]
    y = panel_title(x0, y1, u"OUR STRIP", u"HOW IT FLOWS IN FOUR SEASONS")
    Lv = None
    try:
        with open(os.path.join(root, "Data", "bergama_water_board_data.py"), encoding="utf-8") as f:
            src = f.read()
        a_ = src.index(u"LEVELS = [")
        ns_ = {}
        exec(src[a_:src.index(u"\nBRIDGES = {", a_)], ns_)
        r_ = dict((r.get("id"), r) for r in ns_["LEVELS"])["S4"]
        terr = [t for t in r_.get("terraces", []) if t.get("side") == "NE"]
        Lv = dict(bed=r_["bed"]["value"], q100=r_["q100"]["value"], sw=r_["SW"]["top"]["value"],
                  ne=r_["NE"]["top"]["value"], terr=terr[0]["level"]["value"] if terr else r_["bed"]["value"] + 0.5,
                  dm=r_["depth_month"]["value"])
    except Exception as ex_:
        log.append(u"FLAG four seasons: cut S4 levels not read from Data/bergama_water_board_data.py (%s: %s)" % (
            type(ex_).__name__, ex_))
    if Lv:
        dmax = [max(t) for t in zip(*Lv["dm"].values())]   # the higher of the gauges each month (as slide 3)
        bed = Lv["bed"]
        zmin, zmax = bed - STRIP_D - 0.35, max(Lv["sw"], Lv["q100"]) + 0.25
        sw_mm = col_w * 0.52
        rows_h = (y - row1[0] - 6.0) / 4.0
        lwu = 60.0
        prof = [(0.0, Lv["sw"]), (7.0, Lv["sw"]), (15.0, bed), (22.0, bed), (22.0, bed - STRIP_D), (25.0, bed - STRIP_D),
                (25.0, bed), (32.0, bed), (34.0, Lv["terr"]), (44.0, Lv["terr"]), (48.0, Lv["ne"]), (lwu, Lv["ne"])]

        def wpoly(pr, z):
            out, cur = [], []
            for i, (xq, hq) in enumerate(pr):
                if i:
                    xa_, ha_ = pr[i - 1]
                    if (ha_ < z) != (hq < z) and hq != ha_:
                        xi = xa_ + (z - ha_) * (xq - xa_) / (hq - ha_)
                        if ha_ < z:
                            cur.append((xi, z))
                            out.append(cur)
                            cur = []
                        else:
                            cur = [(xi, z)]
                if hq < z:
                    cur.append((xq, hq))
            if cur:
                out.append(cur + [(pr[-1][0], z)])
            return [p_ for p_ in out if len(p_) >= 3]
        SEAS = ((u"WINTER", u"DEC-FEB", (11, 0, 1)), (u"SPRING", u"MAR-MAY", (2, 3, 4)),
                (u"SUMMER", u"JUN-AUG", (5, 6, 7)), (u"AUTUMN", u"SEP-NOV", (8, 9, 10)))
        for j, (nm, mon, idx) in enumerate(SEAS):
            ry = y - 1.0 - (j + 1) * rows_h
            K = G["pc_dg_kit"](items, x0, ry, sw_mm, rows_h - 1.5, "seasons", lw=lwu, lh=zmax - zmin, dash_at=4)
            Z = lambda z: z - zmin
            dep = sum(dmax[i] for i in idx) / 3.0          # calculated: mean of the season's months
            inn = sum(river[i] for i in idx)
            rel = sum(WB["strip_month_m3"][i] for i in idx)
            for p_ in wpoly(prof, bed + dep):
                K["poly"]([(q[0], Z(q[1])) for q in p_], K["C"]["water"])
            if rel > 0:                                    # the strip held by the store
                K["poly"]([(22.0, Z(bed - STRIP_D)), (25.0, Z(bed - STRIP_D)), (25.0, Z(bed)), (22.0, Z(bed))],
                          K["C"]["water"])
            K["ground"]([(q[0], Z(q[1])) for q in prof], 0.0)
            K["line"]([(22.0, Z(bed)), (22.0, Z(bed - STRIP_D)), (25.0, Z(bed - STRIP_D)), (25.0, Z(bed))],
                      K["C"]["move"], 0.45)
            K["line"]([(0.0, Z(Lv["q100"])), (lwu, Z(Lv["q100"]))], K["C"]["water_ln"], 0.1, (1.4, 0.9))
            if j == 0:
                K["text"](u"Q100", lwu, Z(Lv["q100"]) + 0.12, 1.4, K["C"]["water_ln"], True, "R")
            Pp = lambda u, z: (x0 + u * sw_mm / lwu, ry + (z - zmin) * (rows_h - 1.5) / (zmax - zmin))   # page mm
            if inn > 0:                                    # page-mm arrows (the kit's are stretched by the exaggeration)
                arrow(Pp(27.0, bed + dep), Pp(lwu - 3.0, bed + 0.25), WATER_LN, 0.3, 1.6, 0.6, "seasons")
            if rel > 0:
                arrow(Pp(lwu - 3.0, bed - STRIP_D - 0.12), Pp(25.4, bed - STRIP_D + 0.06), WATER_LN, 0.3, 1.6, 0.6,
                      "seasons")
            tx, ty = x0 + sw_mm + 3.0, ry + rows_h - 3.4
            items.append(T_(u"%s · %s" % (nm, mon), tx, ty, 1.9, INK, True, "L", "seasons"))
            ln = [(u"STREAM %.2f m DEEP" % dep, GREY)]
            if inn > 0:
                ln.append((u"%s m3 TAKEN TO THE STORE" % short(inn), WATER_LN))
            ln.append((u"STRIP: %s m3 FROM THE STORE" % short(rel), ACC) if rel > 0 else
                      (u"STRIP UNDER THE STREAM", GREY))
            for s, c_ in ln:
                ty -= 2.4
                items.append(T_(s, tx, ty, 1.5, c_, True, "L", "seasons"))
        para(u"STRIP %.1f m WIDE, %.2f m DEEP AT THE BED LOW POINT (DESIGN) · CUT S4 · DEPTH = MEAN OF THE SEASON'S "
             u"MONTHS (CALCULATED) · HEIGHTS EXAGGERATED" % (STRIP_W, STRIP_D), x0, row1[0] + 3.6, 1.4, col_w, GREY,
             True, "seasons")
        log.append(u"four seasons: cut S4 bed %+.2f, Q100 %+.2f, banks SW %+.2f / NE %+.2f, terrace %+.2f "
                   u"(water board LEVELS); depth = higher gauge per month, season mean; intake = river_month_m3, strip = "
                   u"strip_month_m3 (water balance)" % (bed, Lv["q100"], Lv["sw"], Lv["ne"], Lv["terr"]))

    # v1.12: line weights by drawing size (Aras 15:57 UTC, pages_common v3.33)
    if "pc_stroke_k" in G:
        kmap = {"storage": G["pc_stroke_k"](col_w, Hn, log, u"storage panel"),
                "cycle": G["pc_stroke_k"](col_w, 26.0, log, u"water cycle cut"),
                "seasons": G["pc_stroke_k"](col_w * 0.52, (Hn - 6.0) / 4.0, log, u"season cut")}
        for i in range(n_panels, len(items)):
            it = items[i]
            if it[0] == "line" and it[5] in kmap and it[3]:
                items[i] = it[:3] + (G["pc_stroke"](it[3], kmap[it[5]]),) + it[4:]
            elif it[0] == "poly" and it[6] in kmap and it[4]:
                items[i] = it[:4] + (G["pc_stroke"](it[4], kmap[it[6]]),) + it[5:]
    else:
        log.append(u"FLAG pages_common has no pc_stroke_k (v3.33): panel line weights not scaled; run Bergama.bat")

    # ---------------------------------------------------------------- D TERRACE CLOSE-UP, V1, V2
    x0, y1 = cols[0], row2[1]
    panel_title(x0, y1, u"D", u"TERRACE CLOSE-UP")
    if D_ok:
        pgS2 = lambda xy: (dbox[0] + (F.local(xy)[0] - ua) * k2, dbox[1] + (F.local(xy)[1] - va) * k2)
        items += NC["clip_plan"](B, NC["mb_plan"](MB, MC, F, pgS2, k2, dbox, B, P, log)[0] + wa_paper(pgS2), dbox,
                                 log)
        png2 = NC["svg_crop"](u"slide04_detail", MPC["matrix"], pgS2, dbox, log, css=CSS, bg=False)
        if png2:
            items.append(("image", dbox[0], dbox[1], dbox[2] - dbox[0], dbox[3] - dbox[1], png2, None, False, None,
                          "detail_svg"))
        else:
            log.append(u"FLAG D: the close-up crop failed")
        items.append(R_([box(*dbox)], None, INK, 0.3, "detail_frame"))
        items += NC["scale_north"](F, DETAIL_DEN, dbox[2], dbox[1])
    else:
        items.append(R_([box(*dbox)], None, GREY, 0.3, "detail_frame"))

    def holder(x0_, y0_, x1_, y1_, title, sub):
        items.append(L_(box(x0_, y0_, x1_, y1_) + [(x0_, y0_)], GREY, 0.3, "placeholder_perspective", (2.0, 1.2)))
        hw = min(34.0, (x1_ - x0_) / 2.0 - 2.0)
        cx, cy = (x0_ + x1_) / 2.0, (y0_ + y1_) / 2.0
        items.append(T_(title, cx, cy + 2.0, 2.8, INK, True, "C", "placeholder_perspective"))
        yy = cy - 2.0
        for ln in wrap(B, sub, 2.0, 2 * hw - 2.0):
            items.append(T_(ln, cx, yy, 2.0, GREY, False, "C", "placeholder_perspective"))
            yy -= 2.6
    try:                                                  # v1.8: the viewpoints for the Perspectives script
        os.makedirs(PERSP_DIR, exist_ok=True)
        for v_ in VIEWS.values():
            v_["box_mm"] = [col_w, y1 - 8.0 - row2[0]]
        with open(os.path.join(PERSP_DIR, "views_slide04.json"), "w", encoding="utf-8") as f:
            json.dump(dict(page="slide04", version=VERSION, views=VIEWS), f, ensure_ascii=False)
        log.append(u"views: %s written to %s" % (u", ".join(sorted(VIEWS)) or u"none", PERSP_DIR))
    except Exception as ex:
        log.append(u"FLAG views.json not written (%s)" % ex)
    for i, (vn, what) in enumerate(((u"V1", u"THE TERRACES"), (u"V2", u"WATER ENRICHMENT + EDUCATION BUILDING"))):
        x0 = cols[1 + i]
        panel_title(x0, y1, vn, what)
        pp = os.path.join(PERSP_DIR, u"slide04_" + vn + u".png")
        if os.path.isfile(pp):                            # v1.8: the Perspectives script's capture
            items.append(("image", x0, row2[0], col_w, y1 - 8.0 - row2[0], pp, None, False, None, "perspective_" + vn))
            log.append(u"%s: perspective %s (%s)" % (vn, pp, time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(pp)))))
        else:
            holder(x0, row2[0], x0 + col_w, y1 - 8.0, u"%s · PERSPECTIVE" % vn,
                   u"placeholder: Aras's render from %s on the plan" % vn)
            log.append(u"%s: no %s yet (press Perspectives, then this page): placeholder" % (vn, pp))

    # ---------------------------------------------------------------- title band
    items.append(T_(u"SLIDE %d · SYSTEMS" % SLIDE, MARGIN, 288.0, 2.6, INK, True))
    items.append(T_(u"WATER, GREEN, EDGES AND PUBLIC SPACE", MARGIN, 278.5, 7.5, INK, True))
    log.append(u"Sources: masterplan master.svg (Aras, 15 Nov) via MasterplanBase; water balance results "
               u"(bergama_water_balance, DSI flows, FAO-56, around2.pdf lands); strip storage CONCEPT_RECORD.md table "
               u"(tables/A6_strip_storage.csv); farm extent water_balance_key_figures.json; planting jobs v13.2 "
               u"(Aras 15 Nov 04:58). Distances straight line, calculated.")
    items = [(it[0], NC["no_src"](it[1])) + tuple(it[2:]) if it[0] == "text" else it for it in items]
    bb = X["items_bbox"](items)
    if bb[0] < -0.5 or bb[1] < -0.5 or bb[2] > PAGE_W + 0.5 or bb[3] > PAGE_H + 0.5:
        log.append(u"FLAG drawing runs past the page: x %.0f-%.0f, y %.0f-%.0f mm" % (bb[0], bb[2], bb[1], bb[3]))
    os.makedirs(OUT_DIR, exist_ok=True)
    pdf = X["write_pdf_node"](os.path.join(OUT_DIR, NAME + u".pdf"), [(PAGE_W, PAGE_H, items)],
                              u"Slide %d, water, green, edges and public space" % SLIDE)
    log.append(u"%s  %s" % (pdf, time.strftime("%H:%M:%S")))
    G["pc_present"](pdf, SLIDE, log)
    G["pc_review"](pdf, os.path.join(OUT_DIR, "review"), log)
    flags = [l for l in log if u"FLAG" in l]
    return u"%s\n%s %s, %d FLAG line(s), %.1f s" % (u"\n".join(log), GH_LABEL, VERSION, len(flags), time.time() - t0)


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
