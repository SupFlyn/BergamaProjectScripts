# -*- coding: utf-8 -*-
"""Bergama Group 6: MASTERPLAN BASE v2 (12 Nov 2026). Rules: scripts/_template/SCRIPT_STANDARD.md.
Aras 12 Nov 2026: "Masterplan is our first goal"; "we want the base map first", routes and connections "leave that to
last"; "outside of that line will be white and inside is colourful"; "please prepare a new masterplan script from
scratch according to the examples"; "keep it consistent everywhere"; "combine vectoral and raster drawing however
maximize the quality first"; "textured fills like ... the colour palatte that i gave to you".
The look follows his most liked example (A05_board02_x12_13-1-scaled, brief
library/examples/liked_2026-11-12/MERGED_SPEC_v0.1.md): white context with thin grey outlines, colour only inside the
thin red line, the stream the darkest fill without outline, trees as circles in three tones on a pale green underlay.

What is drawn (nothing is invented: every shape is either the survey or a shape of his plan drawing):
  OUTSIDE the red line (calisma_alan): the existing situation exactly as the Basemap draws it (same code, same style
          entries: white buildings with one thin outline, continuous white streets), without the satellite land cover.
  INSIDE  his plan drawing Data/assets/masterlastversion.svg, redrawn shape by shape in the colours of the style
          table. A shape's meaning comes from the group it sits in (and its fill), table PLAN_RULES below. A tree is
          drawn only where his plan has a tree symbol, as a circle of the symbol's own size; its tone by species
          (TREE_TONE). Under every tree three pale rings (UNDERLAY_M m beyond the crown) = the planted-ground underlay.
          Houses of his plan = the same white building as outside; his heritage shapes = the heritage entry.
  NOT YET his routes, arrows, numbered labels, legend, texts, images and the groups not in PLAN_RULES (the log lists
          how many shapes of which group were left out). They come with the routes, later.
The drawing code (style, grain, PDF writer, sheet layout, survey context) is loaded from the newest
scripts/bergama_basemap_v*.py: one code for every drawing. Run Basemap once before this script (it writes the cache).
v5.1 (Rhino run of v5: trees right; number badges of his labels missing, arrows in another colour than the route):
circles and ellipses of his label group are read (the coloured number badges and dots); his route arrows take the
route colour of the style table.
v9, Aras 13 Nov 06:02-06:05 UTC: "roads still dont align dont intersect and they look incomplete ... roads should
always lead to a detination or to the whole end also the route path like the dotted one is not aligning with the roads";
"merging it into the nearest line is not a solution design those roads"; "those roads being like that should have a
meaning". Cause: the town's existing streets inside the red line were not drawn in file 1, so his roads, paths and
bridges stopped short of the town streets and the town streets stopped at the red line. Now Data/roads_design.json
(made offline from the street bands and his plan; its "method" says how) adds, in file 1 only:
  LINKS        the existing street, on its real line and width, wherever it carries a town street from the red line to
               the plan's first road or path, or a plan road, path or bridge end on to the next one or to the town.
               Drawn as "Road" and joined with his roads into one surface. No link where no existing street runs.
  FOOTBRIDGES  a 3.0 m deck (ASSUMPTION: the width) where his dotted route crosses the water with no bridge drawn.
  ROUTES       his dotted route on the centre line of the path it runs on.
The log lists the path ends that have no existing street to follow: they stay as he drew them.
v5, Aras 13 Nov 04:00-04:01 UTC: "masterplan sucks in terms of architectural language"; "recreate that masterplan
drawing 1:1 according to our site"; "use it's assets our from our asset library"; "tree's etc. look weird". So:
  TREES   my discs are gone from file 1. Every tree is HIS drawing of that species: the symbols sym_<species> of his
          plan SVG are read once (their own shapes and colours) and placed exactly as his <use> places them (place,
          size, turn). One PDF form / SVG asset per species; every tree its own subgroup. (File 2 keeps discs for the
          survey's trees: the survey names no species.)
  ROUTES  his route lines (PLAN_ROUTES) as A05's dotted lines, style entry "route".
  LABELS  his route arrows and his labels (PLAN_RAW) are drawn as he drew them, each shape in its own colour.
v4.1 (Rhino run of v4): both v4 additions are taken out again. The grey and white parts of his heritage groups are
the "popped" relief of his own drawing, not plan detail: drawn as parts they gave stepped double outlines. The
building shadow read as a doubled line (and his rule of 11:13 UTC: no shadows for now). Heritage and houses are
drawn as in v3.2.
v4, Aras 12 Nov 19:57-20:00 UTC: "the heritage buildings should have more context in terms of the plans"; "we want
exact language copy of it" (A05). So: (1) his heritage groups (heritage1, Kizil_Avlu_outline...) are drawn with all
their parts, not only the red block: white parts = heritage_court, grey parts = heritage_detail, each with the dark
heritage outline (order: grey parts, red, white on top; his SVG's own stacking is not read, so check the look);
(2) A05's building relief: a grey shadow under every house of his plan (and under the survey's, Basemap v7).
v3.2 (Rhino run of v3.1): the joined road and path outlines had a fine saw-tooth on diagonals (the 0.5 m cells);
they are straightened to within JOIN_TOL_M m and their corners cut twice.
v3.1 (first Rhino run of v3, 0 FLAG; seen in its picture): the thin curved bands of his group "seconder" are his
secondary paths. v1-v3 took them for planted ground (a guess, flagged), so they stayed pale strokes without outline:
his "roads looks like they are flying". They are paths now: joined, outlined and hatched with the other paths.
v3, Aras 12 Nov 19:51-20:05 UTC: "take the tree information from the site data"; "all trees are group together and a
subgroup would include a tree"; "all roads should have outlines and hatches (inside the working area)", "roads looks
like they are flying"; "remove those leftovers from the houses that have been demolished inside the working are"; "we
gonna focus on making as is file look like our current masterplan file". So:
  ROADS    his road shapes and stroked new roads are joined into ONE surface with one outline and the road hatch
           (JOINED; the paths, the promenade and the dark paving the same, each its own surface).
  HOUSES   file 1: a survey building with GONE_SHARE of its corners inside the red line is not drawn (the plan takes
           it); one that only reaches over the line is drawn whole, on top of the plan, not cut at the line.
  AS IS    file 2 has the masterplan's look from site data only: inside the red line the ground tone, the existing
           streets with the road hatch and outline, the survey's own tree symbols (cache "trees", Basemap v6) as the
           same tree discs on the same soft green (crown SURVEY_TREE_R m: the survey gives none), nothing of the plan.
  TREES    A05's tree: a plain disc with a darker rim and a lighter crown; every tree is its own subgroup.
  SVG      Masterplan.svg and Masterplan_as_is.svg: the same drawing with a named group per layer and a subgroup per
           tree, for editing (flat fills; the PDFs keep the grain and stay the print files).
v2, Aras 12 Nov 19:42-19:45 UTC: "dont divide drawings into two like ever"; "for masterplan remove the wave texture
from water however other than that water hatch texture is good"; "trees looks nowhere near the example"; "Try to make
example a05 example as accurate as possible and adapt onto site 1:1". So: one drawing per sheet (A0: the frame once);
no wave strokes; the context is the Basemap v5 context (streets as one joined surface, the river as one surface, clean
lines); the three hard underlay rings are now A05's soft green: one tone under all trees that fades out UNDERLAY_M m
beyond the crowns; a tree is A05's tree redrawn as vector: a disc in its tone with a slightly darker rim, a ring of
lighter leaf spots and a darker centre, turned differently for every tree, light crowns under dark ones.
Aras 12 Nov 19:48 UTC: "make the masterplan produce two way like the one with our changes and one with site as is
with same visuality as always and prepare them in a way that we can edit each layer that we want"; "file 1: our way /
file 2: as is". So two files from the same code and style: Masterplan = the survey with his plan inside the red line;
Masterplan_as_is = the survey alone (with the 2023 tree cover as the soft tone, as the Basemap). In both, every
category is its own PDF layer (plan_water, plan_trees, buildings, ...) that can be switched and edited separately.
UNDERLAY_M, the circle for a tree symbol and the drawing order are drawing values (ours).

Component: Rhino 8 > Grasshopper > Python 3 Script (the board builder places it from the cloud kit).
  input  run     Button (or the previous script's done text)
  input  scale   sheet scale 1:n of Masterplan.pdf (default 2000)
  output log / done   as every Bergama script
Reads  ~/Downloads/Bergama/scripts/bergama_basemap_v*.py              (the newest: the drawing code)
       ~/Downloads/Bergama/Data/bergama_style.json                     (the style table)
       ~/Downloads/Bergama/Data/assets/masterlastversion.svg           (his plan)
       ~/Downloads/Bergama/cached/bergama_basemap/basemap_layers.json  (the survey, written by Basemap)
       ~/Downloads/Bergama/cached/bergama_basemap/streets.json         (the street bands, written by Basemap)
Writes ~/Downloads/Bergama/output/bergama_plan_base/Masterplan.pdf, Masterplan_A0.pdf          (file 1: our way)
       ~/Downloads/Bergama/output/bergama_plan_base/Masterplan_as_is.pdf, Masterplan_as_is_A0.pdf  (file 2: as is)
       ~/Downloads/Bergama/output/bergama_plan_base/Masterplan.svg, Masterplan_as_is.svg           (grouped, to edit)
       ~/Downloads/Bergama/cached/bergama_plan_base/plan_shapes.json   (his plan's shapes by meaning, frame m)
       ~/Downloads/Bergama/logs/bergama_plan_base_log.txt
"""
import os, time, json, math, re, glob

# ---- SETTINGS ----
VERSION = "v9"
GH_LABEL = "PlanBase"
OUT_FOLDER = "bergama_plan_base"
LOG_NAME = "bergama_plan_base_log.txt"
GH_INPUTS = {"scale": "int 500..10000 = 2000"}

PLAN_SVG = os.path.join("Data", "assets", "masterlastversion.svg")
LIB_GLOB = os.path.join("scripts", "bergama_basemap_v*.py")
LIB_END = "# ================================================================ main"
# his group id -> {fill of the shape (lower case hex) or "*" = any fill: style category}; drawn in ORDER below
PLAN_RULES = {
    "green_corridor_open_ground_within_25_m_of_the_water": {"*": "soft_ground"},
    "seconder": {"*": "paving"},      # v3.1: his secondary paths (thin curved bands), not planted ground
    "Selinos": {"*": "water"},
    "water_drainage_wall": {"*": "wet_edge"},
    "wetland_shallow_water_reeds": {"#a9c4c2": "wet_edge", "#5d8980": "wet_edge", "*": "reed"},
    "roads_streets": {"#fff": "plan_road", "#f8f8f6": "plan_road", "#e9ded8": "plan_road"},
    "yeni_yol": {"*": "plan_road"},
    "walks_paths_bike_lane": {"#e8cfcf": "promenade", "#a8705c": "paving_dark", "#efddda": "paving", "#f8f5f3": "paving",
                              "#eee5e1": "paving", "#f3edea": "paving", "#e9ded8": "paving"},
    "evler": {"#f7f8f6": "building", "#e4877a": "heritage"},
    "heritage1": {"#e4877a": "heritage"},
    "Kizil_Avlu_outline_popped_the_reason_for_the_red_area": {"#b8483a": "heritage"},
}
STROKED = ("yeni_yol",)            # groups whose stroked lines are drawn too, at their own width (his new roads)
ORDER = ["soft_ground", "planted", "water", "wet_edge", "reed", "plan_road", "paving", "promenade", "paving_dark",
         "building", "heritage"]
PLAN_RAW = ("route_arrows", "labels")   # his groups drawn as they are: every filled shape in its own colour
PLAN_ROUTES = ("route_line", "route_footbridges")   # his route lines: drawn dotted (A05), style entry "route"
RAW_STEP = 0.3                     # SVG units: curve pieces for his label letters and arrows (finer than PATH_STEP)
SYMBOL_STEP = 0.02                 # symbol units (a tree symbol is about 2 wide): curve pieces of his tree drawings
TREE_SYMBOL = "sym_"               # his tree symbols: <use xlink:href="#sym_<species>">
TREE_TONE = {"plane": "tree_dark", "stone_pine": "tree_dark", "ash": "tree_mid", "olive": "tree_mid",
             "willow": "tree_light", "tamarisk": "tree_light", "rosemary": "tree_light"}
SHADOW_M = (-1.2, -1.2)            # A05: every building throws a short, crisp, dark shadow to the lower left: m on the
                                   # page (right, up). Estimated from the A05 image (about a tenth of a small house);
                                   # None draws none. Vector, one shape per building (v7; v6 was a blurred tone)
SOFT_CELL_M = 1.0                  # m cell of the soft green outside (v6.1: 2 m cells showed as steps)
CONTEXT_GREEN = False              # the soft green of the 2023 tree cover outside the red line: off (Aras 13 Nov 05:39 UTC:
                                   # "that hue greeneery looks like a drawing error"); True draws it again
UNDERLAY_M = 5.0                   # m beyond the crown that the soft green reaches before it fades (ours)
JOINED = ("plan_road", "paving", "promenade", "paving_dark")   # each joined into one outlined surface
JOIN_TOL_M = 0.6                   # m: the joined outline is straightened to within this (v3.2: no saw-tooth on diagonals)
JOIN_CLOSE_M, JOIN_MIN_M2 = 0.5, 4.0   # m seams closed between the pieces of one surface; smallest island kept (ours)
GONE_SHARE = 0.5                   # a survey building with this share of its corners inside the red line is taken
#                                    by the plan (not drawn in file 1); one with fewer is drawn whole, on top (ours)
# the survey's tree symbol layers -> style entry (our reading of the layer names: YPDKN = yaprak doken, deciduous;
# YAP_DOKMEYEN = evergreen; TEK_AGAC = single tree)
SURVEY_TONE = {"SEMBOL_YPDKN_AGAC": "site_tree_light", "SEMBOL_TEK_AGAC": "site_tree_mid",
               "SEMBOL_YAP_DOKMEYEN": "site_tree_dark"}
SURVEY_TREE_R = 3.0                # m: crown drawn for a survey tree symbol (the survey gives no crown size; ours)
PATH_STEP = 1.5                    # SVG units: curves of his plan are cut into pieces of about this length
CREDIT = (u"Inside the red line: the plan drawing masterlastversion.svg, redrawn by layer. Outside: the survey "
          u"(buildings, road edges, water) with street bands along OpenStreetMap centrelines; houses the survey draws only as open "
          u"street fronts: footprints (c) OpenStreetMap contributors, else backs read from Esri World Imagery "
          u"(Maxar, 1 Mar 2023), about +-5 m.")

CREDIT_ASIS = (u"The site as it is: the survey (buildings, road edges, water, tree symbols) with street bands along "
               u"OpenStreetMap centrelines; houses the survey draws only as open street fronts: footprints (c) "
               u"OpenStreetMap contributors, else backs read from Esri World Imagery (Maxar, 1 Mar 2023), about +-5 m. Inside the red line the same look as the masterplan, nothing of the plan.")

# ---- folders (same in every script) ----
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")
OUT_DIR = os.path.join(BERGAMA_ROOT, "output", OUT_FOLDER)
CACHE_DIR = os.path.join(BERGAMA_ROOT, "cached", OUT_FOLDER)
LOG_DIR = os.path.join(BERGAMA_ROOT, "logs")
SHAPE_FILE = os.path.join(CACHE_DIR, "plan_shapes.json")
DESIGN_FILE = os.path.join("Data", "roads_design.json")   # v9: the road links, footbridge decks and centred routes
SHAPE_FORMAT = 2


def load_lib(log):
    """the drawing code of the newest Basemap script (everything above its main) as a dict of names"""
    found = glob.glob(os.path.join(BERGAMA_ROOT, LIB_GLOB))
    if not found:
        raise RuntimeError(u"no %s: run Bergama.bat once (the kit copies the Basemap script), then press again"
                           % os.path.join(BERGAMA_ROOT, LIB_GLOB))
    src_ = max(found, key=lambda p: [int(n) for n in re.findall(r"\d+", os.path.basename(p))])
    with open(src_, encoding="utf-8") as f:
        code = f.read()
    if LIB_END not in code:
        raise RuntimeError(u"%s has no line %r: it is older than Basemap v4" % (src_, LIB_END))
    ns = {"__name__": "bergama_basemap_lib"}
    exec(compile(code[:code.index(LIB_END)], src_, "exec"), ns)
    if "sheet" not in ns or "load_style" not in ns:
        raise RuntimeError(u"%s is older than Basemap v4: update the kit (Bergama.bat), then press again" % src_)
    ns["BERGAMA_ROOT"] = BERGAMA_ROOT
    log.append(u"drawing code: %s (%s %s)" % (src_, ns.get("GH_LABEL"), ns.get("VERSION")))
    return ns


# ================================================================ his plan, shape by shape
def read_plan(B, F, log):
    """his plan's shapes by style category, in frame m:
    {"shapes": {category: [[ring, ...]]}, "lines": [[points, width m]], "trees": [[u, v, r m, species]], "left": {...}}"""
    src = os.path.join(BERGAMA_ROOT, PLAN_SVG)
    if not os.path.isfile(src):
        raise RuntimeError(u"%s not found: his plan drawing is needed for the masterplan" % src)
    st = os.stat(src)
    key = u"%d|%s|%s|%d|%d" % (SHAPE_FORMAT, VERSION, B.get("VERSION"), st.st_size, st.st_mtime_ns)
    if os.path.isfile(SHAPE_FILE):
        try:
            with open(SHAPE_FILE, encoding="utf-8") as f:
                P = json.load(f)
            if P.get("key") == key:
                log.append(u"same plan drawing as the cache: %s used, the SVG not read again" % SHAPE_FILE)
                return P
        except Exception:
            pass
    t0 = time.time()
    with open(src, encoding="utf-8") as f:
        txt = f.read()
    fr, how = B["plan_frame"](txt, F)
    if fr is None:
        raise RuntimeError(u"%s: %s: the plan cannot be placed" % (src, how))
    rx, ry, rw, rh = fr
    s = rw / F.w

    def U(p):
        return [round((p[0] - rx) / s, 2), round((ry + rh - p[1]) / s, 2)]
    shapes, lines, trees, left, odd = {}, [], [], {}, 0
    uses, raw, routes, symbols = [], [], [], {}
    for sm in re.finditer(r"<symbol\b([^>]*)>(.*?)</symbol>", txt, re.S):   # his tree drawings, each once
        sa = dict(re.findall(r'([\w:-]+)="([^"]*)"', sm.group(1)))
        sid = sa.get("id", "")
        if not sid.startswith(TREE_SYMBOL):
            continue
        try:
            vb = [float(x) for x in (sa.get("viewBox") or "0 0 2 2").replace(",", " ").split()]
        except Exception:
            vb = [0.0, 0.0, 2.0, 2.0]
        shp = []
        for pm in re.finditer(r"<path\b([^>]*?)/?>", sm.group(2)):
            pa = dict(re.findall(r'([\w:-]+)="([^"]*)"', pm.group(1)))
            col = B["_hex6"](pa.get("fill"))
            if not col or "transform" in pa:
                continue
            rings_ = [[[round(q[0], 4), round(q[1], 4)] for q in Pp] for cl_, Pp in B["path_rings"](pa.get("d", ""), SYMBOL_STEP)
                      if len(Pp) >= 3]
            if rings_:
                shp.append([col, rings_])
        if shp and len(vb) == 4:
            symbols[sid[len(TREE_SYMBOL):]] = {"w": vb[2], "h": vb[3], "shapes": shp}
    stack, hidden, skip = [], 0, 0                       # stack of (group id, hidden?); skip = inside defs / symbol
    for m in re.finditer(r"<(/?)(g|defs|symbol|clipPath|mask|pattern|path|polygon|polyline|line|rect|use|circle|ellipse)\b([^>]*?)(/?)>", txt):
        end, tag, attrs, selfc = m.group(1), m.group(2), m.group(3), m.group(4)
        if tag in ("defs", "symbol", "clipPath", "mask", "pattern"):
            if not selfc:
                skip += -1 if end else 1
            continue
        if skip:
            continue
        if tag == "g":
            if end:
                if stack and stack.pop()[1]:
                    hidden -= 1
            elif not selfc:
                h = 'display="none"' in attrs
                gid = re.search(r'\bid="([^"]*)"', attrs)
                stack.append((gid.group(1) if gid else None, h))
                hidden += 1 if h else 0
            continue
        if end or hidden or 'display="none"' in attrs:
            continue
        a = dict(re.findall(r'([\w:-]+)="([^"]*)"', attrs))
        if tag == "use":
            href = a.get("xlink:href") or a.get("href") or ""
            if not href.startswith("#" + TREE_SYMBOL):
                continue
            tr = a.get("transform", "")
            mt = re.search(r"translate\(\s*([-\d.eE]+)[\s,]*([-\d.eE]+)?\s*\)", tr)
            ms = re.search(r"scale\(\s*([-\d.eE]+)", tr)
            mr = re.search(r"rotate\(\s*([-\d.eE]+)", tr)
            try:
                w, h = float(a["width"]), float(a["height"])
                sc = float(ms.group(1)) if ms else 1.0
                tx, ty = (float(mt.group(1)), float(mt.group(2) or 0.0)) if mt else (0.0, 0.0)
            except Exception:
                odd += 1
                continue
            ang = math.radians(float(mr.group(1))) if mr else 0.0
            hx, hy = w * sc / 2.0, h * sc / 2.0
            c = U((tx + hx * math.cos(ang) - hy * math.sin(ang), ty + hx * math.sin(ang) + hy * math.cos(ang)))
            trees.append(c + [round(max(w, h) * abs(sc) / 2.0 / s, 2), href[1 + len(TREE_SYMBOL):]])
            uses.append(U((tx, ty)) + [round(sc / s, 5), round(ang, 5), href[1 + len(TREE_SYMBOL):]])
            continue
        gid = next((g for g, _ in reversed(stack) if g in PLAN_RULES or g in PLAN_RAW or g in PLAN_ROUTES), None)
        if gid is None:
            g0 = next((g for g, _ in reversed(stack) if g and not g.startswith("Layer_")), None) or u"(no named group)"
            left[g0] = left.get(g0, 0) + 1
            continue
        if tag in ("circle", "ellipse") and gid not in PLAN_RAW:   # dots are read only where his drawing is copied
            continue
        if "transform" in a:
            odd += 1
            continue
        fill = (a.get("fill") or "").lower()
        rule = PLAN_RULES.get(gid, {})
        if tag == "path":
            subs = B["path_rings"](a.get("d", ""), RAW_STEP if gid in PLAN_RAW else PATH_STEP)
        elif tag in ("polygon", "polyline"):
            v = [float(x) for x in re.findall(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", a.get("points", ""))]
            subs = [(tag == "polygon", list(zip(v[0::2], v[1::2])))]
        elif tag in ("circle", "ellipse"):                # v5.1: the number badges and dots of his labels
            try:
                cx_, cy_ = float(a.get("cx", 0)), float(a.get("cy", 0))
                rx_ = float(a["r"]) if tag == "circle" else float(a["rx"])
                ry_ = float(a["r"]) if tag == "circle" else float(a["ry"])
                subs = [(True, [(cx_ + rx_ * math.cos(i_ * math.pi / 16.0), cy_ + ry_ * math.sin(i_ * math.pi / 16.0))
                                for i_ in range(32)])]
            except Exception:
                subs = []
        elif tag == "line":
            try:
                subs = [(False, [(float(a["x1"]), float(a["y1"])), (float(a["x2"]), float(a["y2"]))])]
            except Exception:
                subs = []
        else:
            try:
                x, y, w, h = float(a.get("x", 0)), float(a.get("y", 0)), float(a["width"]), float(a["height"])
                subs = [(True, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)])]
            except Exception:
                subs = []
        if gid in PLAN_RAW:                               # his own drawing, colour and all
            col = B["_hex6"](a.get("fill"))
            rings = [[U(p) for p in P] for cl, P in subs if len(P) >= 3]
            if col and rings and tag not in ("line", "polyline"):
                raw.append([gid, col, rings])
            else:
                left[gid] = left.get(gid, 0) + 1
            continue
        if gid in PLAN_ROUTES:
            if a.get("stroke", "none") != "none":
                for cl, P in subs:
                    if len(P) >= 2:
                        routes.append([U(p) for p in P] + ([U(P[0])] if cl else []))
            else:
                left[gid] = left.get(gid, 0) + 1
            continue
        filled = fill not in ("", "none") or (tag in ("path", "polygon", "rect") and "fill" not in a and "stroke" not in a
                                                and gid == "water_drainage_wall")
        cat = (rule.get(fill) or rule.get("*")) if filled else None
        if cat and tag != "line" and tag != "polyline":
            rings = [[U(p) for p in P] for cl, P in subs if len(P) >= 3]
            if rings:
                shapes.setdefault(cat, []).append(rings)
            continue
        sw = re.match(r"[\d.]+", a.get("stroke-width", "") or "")
        if gid in STROKED and a.get("stroke", "none") != "none" and sw:
            for cl, P in subs:
                if len(P) >= 2:
                    lines.append([[U(p) for p in P] + ([U(P[0])] if cl else []), round(float(sw.group(0)) / s, 2)])
            continue
        left[gid] = left.get(gid, 0) + 1
    P = {"key": key, "made_by": u"%s %s" % (GH_LABEL, VERSION), "made_at": time.strftime("%Y-%m-%d %H:%M:%S"),
         "what": u"his plan %s by style category, in frame m (u along the frame's long side from its west end, v up); "
                 u"frame = %s at (%.2f, %.2f) %.2f x %.2f units, %.4f units per m" % (os.path.basename(src), how, rx, ry,
                                                                                     rw, rh, s),
         "shapes": shapes, "lines": lines, "trees": trees, "left": left, "odd": odd,
         "symbols": symbols, "uses": uses, "raw": raw, "routes": routes}
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(SHAPE_FILE, "w", encoding="utf-8") as f:
        json.dump(P, f, ensure_ascii=False)
    log.append(u"%s  %s (his plan %s, %.1f MB, read in %.1f s; %s)" % (
        SHAPE_FILE, time.strftime("%H:%M:%S"), os.path.basename(src), st.st_size / 1048576.0, time.time() - t0, P["what"]))
    return P


def area_clips(cal, pg, F, u0, u1, tag):
    """the two cuts every area item uses: tag = calisma_alan and the window, tag + "w" = the window alone"""
    win = [pg(q) for q in ((u0, 0), (u1, 0), (u1, F.h), (u0, F.h))]
    return {tag: [[[pg(q) for q in R] for R in cal], [win]], tag + "w": [[win]]}


def tree_marks(B, cat, trees, tones, order, pg, k, u0, u1, layer, tag):
    """trees [(u, v, r m, kind)] as A05's tree: a plain disc in its tone with a darker rim and a lighter crown inside,
    light tones under dark ones. Every tree is its own subgroup layer/tree_0001 (disc + crown).
    Returns (items, {tone: count}, {kind without a tone: 1})"""
    items, cnt, unknown = [], {}, {}
    n_ = 0
    for tone in order:
        c = cat[tone]
        crown = B["_mix"](c["fill"], 0.12)
        for u, v, r, sp in trees:
            t = tones.get(sp)
            if t is None:
                unknown[sp] = 1
                t = order[len(order) // 2]
            if t != tone or not (u0 - r <= u <= u1 + r):
                continue
            n_ += 1
            ly = u"%s/tree_%04d" % (layer, n_)
            X, Y = pg((u, v))
            R_ = r * k
            items.append(("poly", [circle((X, Y), R_, 32)], B["fill_of"](c), c["line"], c["w"], None, ly, 1, None, tag))
            items.append(("poly", [circle((X - R_ * 0.18, Y + R_ * 0.18), R_ * 0.55, 20)], crown, None, 0.0, None, ly, 1,
                          None, tag))
            cnt[tone] = cnt.get(tone, 0) + 1
    return items, cnt, unknown


def plan_items(B, P, S, F, cal, den, x0, y0, u0, u1, tag):
    """his plan for the window u0..u1 as items cut to calisma_alan and the window; returns (items, clips, counts)"""
    k = 1000.0 / den
    items, cnt = [], {}

    def pg(p):
        return (x0 + (p[0] - u0) * k, y0 + p[1] * k)
    cat = S["cat"]
    fill_of = B["fill_of"]
    clips = area_clips(cal, pg, F, u0, u1, tag)
    c = cat["meadow"]                                    # the ground of the whole working area
    items.append(("poly", [[pg(q) for q in R] for R in cal], fill_of(c), None, 0.0, None, "plan_open_ground", 1, "eo",
                  tag + "w"))
    cnt["meadow"] = len(cal)

    def inwin(rings):
        return any(min(q[0] for q in R) <= u1 and max(q[0] for q in R) >= u0 for R in rings)
    for name in ORDER:
        c = cat[name]
        if name == "water":                              # the underlay lies on the ground, under water, paths and trees
            if P.get("soft"):
                items.append(B["soft_item"](P["soft"], cat["underlay_2"]["fill"], "plan_planted_underlay", tag, den, x0, y0))
                cnt["underlay_2"] = 1
        if name in JOINED:                               # roads and paths: ONE surface each, one outline, its hatch
            rings = [R for R in P["net"].get(name, []) if inwin([R])]
            if rings:
                items.append(("poly", [[pg(q) for q in R] for R in rings], fill_of(c), c["line"], c["w"], None,
                              "plan_" + name, 1, "eo", tag))
                cnt[name] = len(rings)
            continue
        for rings in P["shapes"].get(name, []):
            if not inwin(rings):
                continue
            items.append(("poly", [[pg(q) for q in R] for R in rings], fill_of(c), c["line"], c["w"], None, "plan_" + name,
                          1, "eo" if len(rings) > 1 else None, tag))
            cnt[name] = cnt.get(name, 0) + 1
    syms = P.get("symbols") or {}
    unknown = {}
    if syms and P.get("uses"):                           # his own tree drawings, placed as he placed them
        n_ = 0
        for uo, vo, mu, ang, sp in P["uses"]:
            if sp not in syms:
                unknown[sp] = 1
                continue
            if not (u0 - 30.0 <= uo <= u1 + 30.0):
                continue
            n_ += 1
            X, Y = pg((uo, vo))
            mm_, ca, sa = mu * k, math.cos(ang), math.sin(ang)
            items.append(("form", sp, (mm_ * ca, -mm_ * sa, -mm_ * sa, -mm_ * ca, X, Y), u"plan_trees/tree_%04d" % n_, tag))
        cnt["tree_symbol"] = n_
    else:
        it, c2, unknown = tree_marks(B, cat, P["trees"], TREE_TONE, ("tree_light", "tree_mid", "tree_dark"), pg, k, u0,
                                     u1, "plan_trees", tag)
        items += it
        cnt.update(c2)
    if cat.get("route"):                                 # his routes, dotted (A05)
        c = cat["route"]
        for pts in P.get("routes") or []:
            if inwin([pts]):
                items.append(("line", [pg(q) for q in pts], c["line"], c["w"], tag, "plan_routes", (0.0, c["w"] * 2.4)))
                cnt["route"] = cnt.get("route", 0) + 1
    for gid_, col, rings in P.get("raw") or []:          # his arrows and labels, as he drew them
        if inwin(rings):
            if gid_ == "route_arrows" and cat.get("route"):   # one colour for the route and its arrows
                col = cat["route"]["line"]
            items.append(("poly", [[pg(q) for q in R] for R in rings], col, None, 0.0, None, "plan_" + gid_, 1,
                          "eo" if len(rings) > 1 else None, None if gid_ == "labels" else tag))   # v6.1: a label is never cut
            cnt[gid_] = cnt.get(gid_, 0) + 1
    return items, clips, cnt, unknown


def site_items(B, T, soft, cover, L, S, F, cal, den, x0, y0, u0, u1, tag, items):
    """the as-is file in the masterplan's look, put into the context items in place: inside the red line the ground
    tone, the soft green under the survey's trees, the existing streets with the road hatch and outline, the survey's
    trees. Returns (clips, counts, {tree layer without a tone: 1})"""
    k = 1000.0 / den
    cat = S["cat"]
    cnt = {}

    def pg(p):
        return (x0 + (p[0] - u0) * k, y0 + p[1] * k)
    clips = area_clips(cal, pg, F, u0, u1, tag)
    head = [("poly", [[pg(q) for q in R] for R in cal], B["fill_of"](cat["meadow"]), None, 0.0, None, "site_ground", 1,
             "eo", tag + "w")]
    cnt["meadow"] = len(cal)
    if soft:
        head.append(B["soft_item"](soft, cat["underlay_2"]["fill"], "site_tree_underlay", tag, den, x0, y0))
        cnt["underlay_2"] = 1
    elif cover is not None and cover.soft:               # no tree symbols in the survey cache: the 2023 tree cover
        head.append(B["soft_item"](cover.soft, cat["tree_cover"]["fill"], "satellite_trees", tag, den, x0, y0))
        cnt["tree_cover"] = 1
    rings = [Q for cl, Q, a, b in L.get("street_net", []) if len(Q) >= 3]
    if rings:                                            # right above the white street surface, under every line
        at = max([i for i, it in enumerate(items) if B["_item_layer"](it) == "existing_streets"] or [-1]) + 1
        c = cat["plan_road"]
        items.insert(at, ("poly", [[pg(q) for q in R] for R in rings], B["fill_of"](c), c["line"], c["w"], None,
                          "site_streets_in_area", 1, "eo", tag))
    items[0:0] = head
    it, c2, unknown = tree_marks(B, cat, T, SURVEY_TONE, ("site_tree_light", "site_tree_mid", "site_tree_dark"), pg, k,
                                 u0, u1, "site_trees", tag)
    items += it
    cnt.update(c2)
    return clips, cnt, unknown


def look_items(B, S, items, green, den, x0, y0, F):
    """A05's context language put into the finished item list in place (Masterplan files only): the soft green of
    the tree cover under everything; every building white with a pale outline (style building_plan) and a short dark
    vector shadow to the lower left (style building_shadow), all shadows under all buildings. Returns the counts"""
    cnt = {}
    cat = S["cat"]
    k = 1000.0 / den
    lay = B["_item_layer"]
    pale = cat.get("building_plan")
    sh = cat.get("building_shadow") if SHADOW_M else None
    dx, dy = ((SHADOW_M[0] * k, SHADOW_M[1] * k) if SHADOW_M else (0.0, 0.0))
    xa, ya, xb, yb = x0, y0, x0 + F.w * k, y0 + F.h * k

    def cl(p):                                           # a shadow never leaves the frame
        return (min(xb, max(xa, p[0])), min(yb, max(ya, p[1])))
    shadows, first = [], None
    edge = cat.get("street_plan")                         # v7.1: A05's street and road edges are very pale too
    for i, it in enumerate(items):
        if edge and it[0] == "line" and lay(it) in ("existing_streets", "existing_roads"):
            items[i] = it[:2] + (edge["line"],) + it[3:]
            continue
        if not lay(it).startswith("existing_buildings"):
            continue
        if first is None:
            first = i
        if it[0] == "poly":
            if sh:
                quads = []
                for R in it[1]:
                    a2 = sum(R[j - 1][0] * R[j][1] - R[j][0] * R[j - 1][1] for j in range(len(R)))
                    for j in range(len(R)):
                        a, b = (R[j - 1], R[j]) if a2 >= 0 else (R[j], R[j - 1])   # walked counter-clockwise
                        if (b[1] - a[1]) * dx - (b[0] - a[0]) * dy > 1e-9:         # this side faces the shadow
                            quads.append([a, b, cl((b[0] + dx, b[1] + dy)), cl((a[0] + dx, a[1] + dy))])
                if quads:
                    shadows.append(("poly", quads, sh["fill"], None, 0.0) + it[5:6] + ("building_shadow",) + it[7:8] +
                                   (None,) + it[9:])
            if pale:
                items[i] = it[:2] + (pale["fill"] or it[2], pale["line"], pale["w"]) + it[5:]
        elif it[0] == "line" and pale:
            items[i] = it[:2] + (pale["line"], pale["w"]) + it[4:]
    if shadows:
        items[first:first] = shadows
        cnt["building_shadow"] = len(shadows)
    if green and not any(lay(it) == "satellite_trees" for it in items):
        items.insert(0, B["soft_item"](green, cat["tree_cover"]["fill"], "satellite_trees", None, den, x0, y0))
        cnt["tree_cover"] = 1
    return cnt


def circle(c, r, n):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


# ================================================================ main
def main():
    t0 = time.time()
    log = []
    den = int(globals().get("scale") or 2000)
    B = load_lib(log)
    S = B["load_style"]()
    B["set_grain"](S, log)
    log.append(u"style: %s (%s)" % (S["version"], os.path.join(BERGAMA_ROOT, B["STYLE_FILE"])))
    if not os.path.isfile(B["CACHE_FILE"]):
        raise RuntimeError(u"%s not found: press Basemap once first (it reads the survey and writes this cache)"
                           % B["CACHE_FILE"])
    with open(B["CACHE_FILE"], encoding="utf-8") as f:
        D = json.load(f)
    if not D.get("calisma"):
        raise RuntimeError(u"the Basemap cache has no calisma_alan outline: the plan cannot be cut to the working area")
    F = B["Frame"]([tuple(p) for p in D["frame"]])
    D["layers"].update(B["load_veg"](D, log))             # the tree cover of today, for the as-is file only
    D["layers"].update(B["build_streets"](D, F, log))
    D["layers"].update(B["osm_houses"](D, F, log))        # v7: the houses the survey draws only as open fronts
    D["layers"].update(B["sat_houses"](D, F, log))        # v8: the rest of them, backs read from the satellite image
    L = B["localise"](D, F)
    B["prepare"](D, L, F, log)
    fade = B["Fade"](D, F)
    cover = B["Cover"](L, F, log) if L.get("sat_trees") else None
    P = read_plan(B, F, log)
    cal = [[F.local(p) for p in R] for R in D["calisma"]]
    P["soft"] = B["haze_data"]([(u, v, r + UNDERLAY_M) for u, v, r, sp in P["trees"]], F) if P["trees"] else None
    design = {}                                           # v9: the road links (see the head of the file)
    dsrc = os.path.join(BERGAMA_ROOT, DESIGN_FILE)
    if os.path.isfile(dsrc):
        try:
            with open(dsrc, encoding="utf-8") as f:
                dj = json.load(f)
            for k_, cat_ in (("links", "plan_road"), ("footbridges", "paving")):
                design[cat_] = [[[list(F.local(q)) for q in R] for R in shp] for shp in dj.get(k_) or []]
            same = dj.get("plan_svg_bytes") == os.path.getsize(os.path.join(BERGAMA_ROOT, PLAN_SVG))
            if same and dj.get("routes"):
                P["routes"] = [[list(F.local(q)) for q in r] for r in dj["routes"]]
            else:
                log.append(u"FLAG roads: %s was made for another version of his plan SVG: the links are drawn, the "
                           u"dotted route is left as he drew it; ask for a new roads_design.json" % dsrc)
            log.append(u"roads: %d link(s) along existing streets and %d footbridge deck(s) added to his roads and paths; "
                       u"dotted route %s; %d path end(s) of his plan have no existing street to follow and stay as "
                       u"drawn, at (m along the frame, m up): %s" % (
                           len(design["plan_road"]), len(design["paving"]),
                           u"on the path centre lines" if same else u"as he drew it", len(dj.get("open_ends") or []),
                           u", ".join(u"%.0f/%.0f" % (e[0], e[1]) for e in dj.get("open_ends") or []) or u"none"))
        except Exception as e:
            design = {}
            log.append(u"FLAG roads: %s not read (%s: %s): his roads and paths are drawn without the links"
                       % (dsrc, type(e).__name__, e))
    else:
        log.append(u"FLAG roads: %s not found: his roads and paths are drawn without the links" % dsrc)
    P["net"] = {}                                         # roads and paths: one joined surface per category
    for name in JOINED:
        src = [rings for rings in P["shapes"].get(name, [])] + design.get(name, [])
        if name == "plan_road":
            for pts, wm in P["lines"]:
                src += [[R] for R in B["stroke_rings"](pts, wm / 2.0)]
        if src:
            P["net"][name] = B["join_rings"](src, F, JOIN_CLOSE_M, JOIN_MIN_M2, JOIN_TOL_M, 2)[0]
    log.append(u"his roads and paths joined: %s" % (u", ".join(
        u"%s %d shapes -> %d outline(s)" % (n_, len(P["shapes"].get(n_, [])) + (len(P["lines"]) if n_ == "plan_road" else 0),
                                            len(P["net"][n_])) for n_ in JOINED if n_ in P["net"]) or u"none found"))

    def inside(q):
        return any(B["g_pip"](q[0], q[1], R) for R in cal)
    L1, Ltop, gone = dict(L), {}, 0                       # file 1: the survey without the houses the plan takes
    for key in ("sat_houses", "osm_houses", "buildings", "heritage"):
        base, top = [], []
        for it in L.get(key, []):
            sh = sum(1 for q in it[1] if inside(q)) / float(max(1, len(it[1])))
            if sh <= 0:
                base.append(it)
            elif sh < GONE_SHARE:
                top.append(it)
            else:
                gone += 1
        L1[key], Ltop[key] = base, top
    log.append(u"file 1, survey buildings at the red line: %d inside (%.0f %% of their corners or more) not drawn, the "
               u"plan takes them; %d reaching over the line drawn whole on top" % (
                   gone, 100 * GONE_SHARE, sum(len(v) for v in Ltop.values())))
    T = []                                                # the survey's trees inside the red line, frame m
    for x, y, r, lay_ in D.get("trees") or []:
        q = F.local((x, y))
        if 0 <= q[0] <= F.w and 0 <= q[1] <= F.h and inside(q):
            T.append((q[0], q[1], r if 1.0 <= r <= 10.0 else SURVEY_TREE_R, lay_))
    if "trees" not in D:
        log.append(u"FLAG as-is trees: the Basemap cache has no survey trees (written by Basemap v6 or newer): press "
                   u"Basemap once, then PlanBase; until then file 2 shows the 2023 tree cover instead")
    else:
        log.append(u"file 2, survey trees: %d symbols in the model, %d inside the red line (%s); crown %.1f m where the "
                   u"symbol has no size between 1 and 10 m" % (len(D["trees"]), len(T), u", ".join(
                       u"%s %d" % (k_, sum(1 for t in T if t[3] == k_)) for k_ in sorted(set(t[3] for t in T))) or u"none",
                       SURVEY_TREE_R))
    site_soft = B["haze_data"]([(u, v, r + UNDERLAY_M) for u, v, r, sp in T], F) if T else None
    log.append(u"his plan: %s; %d stroked road lines; %d tree symbols (%s)" % (
        u", ".join(u"%s %d" % (k_, len(v)) for k_, v in sorted(P["shapes"].items())), len(P["lines"]), len(P["trees"]),
        u", ".join(u"%s %d" % (sp, sum(1 for t in P["trees"] if t[3] == sp)) for sp in sorted(set(t[3] for t in P["trees"])))))
    log.append(u"his assets: tree drawings %s; %d trees placed; %d route lines (dotted); arrows and labels as drawn: %s" % (
        u", ".join(u"%s %d shapes" % (k_, len(v["shapes"])) for k_, v in sorted((P.get("symbols") or {}).items())) or u"NONE",
        len(P.get("uses") or []), len(P.get("routes") or []),
        u", ".join(u"%s %d" % (g_, sum(1 for r_ in (P.get("raw") or []) if r_[0] == g_)) for g_ in PLAN_RAW)))
    if not P.get("symbols"):
        log.append(u"FLAG trees: no tree symbols (sym_...) read from his plan SVG: file 1 falls back to plain discs")
    if P["left"]:
        log.append(u"not drawn yet (routes, labels, legend, groups without a rule): %s" % u", ".join(
            u"%s %d" % kv for kv in sorted(P["left"].items(), key=lambda kv: -kv[1])[:40]))
    if P.get("odd"):
        log.append(u"FLAG his plan: %d shape(s) with a transform or unreadable numbers were left out" % P["odd"])
    order = (["water", "wet_edge", "reed", "soft_ground", "meadow", "planted", "underlay_2", "tree_light", "tree_mid",
              "tree_dark", "promenade", "paving", "paving_dark", "plan_road", "building", "heritage", "street", "tree_cover", "route",
              "calisma"])
    order_asis = (["meadow", "underlay_2", "tree_cover", "site_tree_light", "site_tree_mid", "site_tree_dark"] +
                  list(dict.fromkeys(c for _, c, _ in B["CONTEXT"][::-1])) + ["calisma"])
    unknown = {}
    t1 = time.time()
    green = B["haze_data"](cover.rows["sat_trees"], F, None, SOFT_CELL_M) if (
        CONTEXT_GREEN and cover is not None and cover.soft) else None
    log.append(u"A05 look: buildings white with a pale outline and a vector shadow %s; soft green of the 2023 tree "
               u"cover outside the red line %s (%.1f s)" % (
                   (u"moved %.1f, %.1f m" % SHADOW_M) if (SHADOW_M and "building_shadow" in S["cat"]) else u"none",
                   (u"drawn on %.1f m cells" % SOFT_CELL_M) if green else u"none", time.time() - t1))
    n_a0 = B["a0_scale"](F)
    # file 1 "our way" = the survey with his plan inside the red line; file 2 "as is" = the survey alone, same code
    for name, ours, a0 in ((u"Masterplan", True, False), (u"Masterplan", True, True),
                           (u"Masterplan_as_is", False, False), (u"Masterplan_as_is", False, True)):
        d = n_a0 if a0 else den

        def band(den_, x, y, u0, u1, tag, ours=ours):
            items, cnt = B["draw_context"](L1 if ours else L, F, S, den_, x, y, u0, u1, cover=None, fade=fade)
            if ours:
                it, clips, c2, unk = plan_items(B, P, S, F, cal, den_, x, y, u0, u1, tag)
                lab = [a for a in it if B["_item_layer"](a) == "plan_labels"]   # v6.1: his labels last, over everything
                items += [a for a in it if B["_item_layer"](a) != "plan_labels"]
                it, c3 = B["draw_context"](Ltop, F, S, den_, x, y, u0, u1, cover=None, fade=fade)
                for i_, a in enumerate(it):               # their own layers, above the plan
                    j_ = 6 if a[0] == "poly" else 5
                    it[i_] = a[:j_] + (a[j_] + "_at_red_line",) + a[j_ + 1:]
                items += it
                for k_, v in c3.items():
                    c2[k_] = c2.get(k_, 0) + v
            else:
                clips, c2, unk = site_items(B, T, site_soft, cover, L, S, F, cal, den_, x, y, u0, u1, tag, items)
            unknown.update(unk)
            for k_, v in look_items(B, S, items, green, den_, x, y, F).items():
                c2[k_] = max(c2.get(k_, 0), v)
            for k_, v in c2.items():
                cnt[k_] = cnt.get(k_, 0) + v
            items += B["draw_top"](D, F, S, den_, x, y, u0, u1, names=False, sections=False)
            if ours:
                items += lab
            cnt["calisma"] = len(cal)
            return items, clips, cnt
        w, h, items, clips, cnt = B["sheet"](
            F, S, d, a0, u"Masterplan" if ours else u"Site as it is",
            (u"Base map of the proposal, 1:%s" if ours else u"Existing situation, 1:%s") % format(d, ",d"),
            (lambda c: [k_ for k_ in order if c.get(k_)]) if ours else
            (lambda c: [k_ for k_ in order_asis if c.get(k_)]), CREDIT if ours else CREDIT_ASIS, band)
        p = B["write_pdf"](os.path.join(OUT_DIR, name + (u"_A0.pdf" if a0 else u".pdf")), w, h, items,
                           u"%s, site_alan, 1:%d" % (name, d), clips, P.get("symbols") if ours else None)
        log.append(B["out_line"](p, w, h, d, items, u"" if a0 else u"; " + u", ".join(
            u"%s %d" % kv for kv in sorted(cnt.items()))))
        if not a0:                                        # the same drawing grouped, for editing
            try:
                q = B["write_svg"](os.path.join(OUT_DIR, name + u".svg"), w, h, items, u"%s, site_alan, 1:%d" % (name, d),
                                   clips, P.get("symbols") if ours else None)
                log.append(u"%s  %s (%.1f MB; a group per layer, every tree its own subgroup; flat fills)" % (
                    q, time.strftime("%H:%M:%S"), os.path.getsize(q) / 1048576.0))
            except Exception as e:
                log.append(u"FLAG %s.svg not written (%s: %s); the PDFs are complete" % (name, type(e).__name__, e))
    if unknown:
        log.append(u"FLAG tree symbols of a species or layer without a tone (TREE_TONE, SURVEY_TONE), drawn in the middle tone: %s"
                   % u", ".join(sorted(unknown)))
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

