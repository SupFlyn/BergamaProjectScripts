# -*- coding: utf-8 -*-
"""Bergama Group 6: PAGE01 AXO v5.2 (15 Nov 2026; v5.2 = Aras 19:06-19:08 UTC "if draw the axo once properly in rhino we can get everything from there diagrams and etc." (chose one 3D model, vector by 3D order): _pin and _depth_order moved above AXO_LIB_END so the node axos and diagrams order their buildings and trees the same way; the page drawing is unchanged; v5.1 = run 25, Aras 18:59 UTC "foreground background is still fucked": the PDF writes one block per layer, so all trees and all buildings were drawn as two piles and the 3D order was lost: buildings and tree crowns now share one layer (axo_body) in their 3D order, tree shadows on the ground under them; v5.0 = Aras 17:02 UTC "this is low res. too dark is it a render ?", "some of the building is not capped", "these kinda errors are everywhere and it is a raster image we want it vectoral": the axo is VECTOR again, drawn in the old 2D axo's flat colours (every roof a closed polygon, no raster, no specks), and what the raster route was for (Aras 14:50 "you mix the foreground and background") is now solved in the vector drawing itself: the order of buildings and trees comes from their 3D form (for each overlapping pair the view ray through a shared point decides which is in front: roof or wall plane of a building, the front of a crown), a topological sort, not one depth number per object; the Rhino capture is no longer used for the page (axo3d_* stay above AXO_LIB_END for other scripts); v4.5 = run 24 look check: Rhino still lit the model (the slab top EFEDE6 came out 184/183/181, every colour about 0.77 x and cooler, so the axo read grey, not the warm 2D look): every mesh normal now faces the camera (one uniform light factor everywhere, the lit / shaded walls stay in the vertex colours) and a calibration tile of a known grey (C8C8C8) beside the slab gives the per-channel gain that brings the whole capture back to its true colours; the tile is cleared from the image after; v4.4 = run 23: the capture came out shaded and right, but on the display mode's own black background (the app background setting is not used there) and Slide01 stopped (thin_lines sat below the wiring marker): the background colour is read from the image corners and made transparent, the check counts only the model; thin_lines moved above main; v4.3 = run 22 (every capture 53 % opaque in all three modes): the lighting value found by name ('None' is a Python word), the tree model's imported layers removed, the check logs the half-transparent share, mean colour and image size; the three tries were byte-identical wireframes (ViewCapture ignored the viewport's display mode): each try is now rendered by the view in its named mode (RhinoView.CaptureToBitmap(size, mode)) on a white background made transparent after; ViewCapture only as a fallback; Aras 15:57 UTC "scale the lines according to the drawing size" (standing): lines over 0.25 mm times pages_common pc_stroke_k; v4.2 = Aras 15:15 UTC "wtf is this ?" on run 21: Rhino drew the 3D model as mesh wires (black tree blobs, a cross-hatched river, a speckled ground, see-through buildings) instead of shaded faces: every capture is now checked before it is used (inside the slab edge at least 95 % of the pixels opaque and at most 12 % near-black), tried in the display modes "Bergama Axo", "Shaded" and "Rendered" in turn, each try saved and logged with its display mode as Rhino reports it; if none passes, the 2D painter draws the axo (FLAG); the lighting setting's error is logged; v4.1 = Aras 14:56 UTC "center the numbers in the boundries" (standing): every marker number is drawn with pages_common pc_text_c on its disc centre (the drawing markers find their disc among the label shapes; the legend discs); v4.0 = Aras 14:50-14:55 UTC "draw these in 3D with scripts in rhino and take the drawings from rhino because the way you approach you mix the foreground and background" (he chose a shaded view capture), "visual style of what we have as a axo drawing was good your first target should be that", "correct outlines please", "you can use that 3D map everywhere you want": the drawing is built as a 3D model in the open Rhino (layer axo3d_page01, removed after; the 3dm never saved) from the same data and in the same flat colours as v3.4 (slab, parks, streets with their edges, flat river, dashed historic walls, buildings with lit / shaded walls, roofs and thin outlines, trees as smooth crowns in his painted symbols' colours with trunks and grey shadows), captured from the axo's parallel view in the display mode "Bergama Axo" (lighting off, flat), registered on the drawing by the slab edge and placed UNDER the vector slab band and numbered markers; Rhino's depth buffer hides what is behind (buildings, trees and outlines); without Rhino the 2D painter (v3.4) draws it and a FLAG says so; axo3d_build / axo3d_capture / axo3d_clear sit above AXO_LIB_END for other scripts; v3.4 = Aras 14:48-14:49 UTC "these trees are awful please fix them to the trees that we have at assets and make them 3dize", "tree's shouldnt be on top of roads and tree's shadows should be more grayish": every crown is one of his painted tree symbols (masterp_agac.svg traces, Data/bergama_b19_plan_data.py TREE_EMBED; plane, ash and the default set), 4 tone bands, on a trunk; no tree inside MapBase's street region; shadows grey D3D3D0; v3.3 = Aras 14:38 UTC "dont do hatches to river" (a rule for every drawing): the water is a flat fill, no hatch; v3.2 = Aras 14:31 UTC "make trees 3D's like real smooth 3D. not like two crossed into each other and increase the trees texture size": each tree is a smooth crown ellipsoid on a trunk, shaded as a lit sphere (shade, lit body, highlight) with large leaf clusters, in the asset cutout's own colours, and a ground shadow (no crossed cutouts); "cut the buildings in axonometric": each building's first model shape carries its plan footprint (foot, survey m), height (h), class and colours, so slide 2 can cut it at its node frame and raise it again; v3.1 = run 19 in the slide (scale 0.76): "ink outside the map frame: axo_slab 4": the slab cut-face band (1.4 page mm) reached below the drawing box: the box now reaches 3 + 1 drawing mm under the slab edge, not cut at the booklet extent; v3.0 = Aras 13:39-13:41 UTC "change the trees on axonometric drawing use it from assets and make those 2d representations 3d", "the trees in the middle of the river is so stupid", "river drawing in axonometric is fucked fix it according to the basemap", "make axonometric get produced by basemap": the whole drawing is now drawn from the MapBase cache, draped on the terrain: the slab (site_alan), parks and green ground, the river (MapBase river, its fill, bank line and water hatch, drawn over the streets as mb_draw does), the street region, the historic walls, the buildings, and the trees (one every 8 m in the 2023 canopy patches MapBase reads, plus its OSM trees; none in the river or on a roof), each tree the asset library cutout (Data/cutouts, traced live) stood up as two crossed copies with a ground shadow; of the booklet drawing only its view, the use class each building stands in and the numbered markers stay; the drawing and its view cached in cached/bergama_page01_axo/axo_model.json for slide 2's node axos; v2.9 = Aras 10:31 UTC "the thickness of the ground is subject to review": the slab as slide 2's node axonometrics draw it (one system): its cut faces a constant SLAB_MM band under the ground edge (was about 5 mm, deeper at the low end), soil hairline hatching on them, a 0.3 base line; v2.8 = run 18 review: buildings across the site_alan edge (the long sheds at the front) hung over the slab: every footprint is now cut to site_alan before it is raised; v2.7 (15 Nov 2026; v2.7 = v2.6 undone: Aras 10:31-10:32 UTC wants every building coloured by this axo's classes (slide 2's node axos copy them), so the residential mass keeps its palette colour (FAB regular) again; v2.6 = Aras 12:10 UTC "review the drawings yourself and compare with the examples": as the liked axo diagrams (F03, D12: context = white volumes, colour only where it means something; Aras 12 Nov "lighter more soft colours"), the residential fabric (the mass of the town) is drawn as the A05 white houses (roof FFFFFF, walls the A05 wall tone CDC8BC and a lighter lit face, outline the A05 street edge 9E9889) instead of mid grey; the coloured uses stand out on it; v2.5 = Aras 10:34 UTC "axo drawing has mistakes how road is drawn and also the buildings doesnt seem right in many places": the booklet's 212 loose road strips are replaced by MapBase's one closed street region (cut to site_alan, draped on the terrain), and its buildings (the 9 Nov board site model: merged blocks, boxes with no survey footprint) by the MapBase footprints, drawn the booklet engine's way (its view, fitted to the slab it drew; halo, lit / shaded walls, roof) with the class of the booklet building each stands in and its surveyed floors as height; trees keep their place among the buildings; legend counts recounted; v2.4 = Aras 05:55 UTC "same goes for this axo" (too cramped, extend it from most left to most right): the numbered list leaves the drawing's right side and joins the legend (a numbered disc per row), the drawing's box is cut to the drawing itself, so the axo runs the whole page width; v2.3 = Aras 04:58 UTC approved cleaning the numbered list (booklet content): "Les Pergamon Boutique Hotel" was listed twice (5 and 6, two buildings): one row, both markers 5, rows 7-12 renumbered 6-11 and moved up; the "· 5.00 m" notes (a default height, not a measure) dropped; "most enclosed stretch" kept only on the lowest sky view, the others "enclosed stretch"; "Kızıl Avlu" (the name was in broken order); list words up to 1.25 x larger (as far as the widest row stays in the extent), notes placed after their names; v2.2 = slide 1 run 7: a tall empty band between the legend and the drawing: the drawing now sits 6 mm under the legend, the empty space left at the page foot; v2.1 = slide 1 review (run 5): the title "What is there" repeated Plan 01's title: now "Heights, heritage, water, green" (the booklet caption's own words), and the title + legend sit ABOVE the drawing), slide 1 (analysis): the booklet's page-3 axonometric ("What is
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
Reads: Data/bergama_pages_common.py, the newest MapBase script (palette) and its cache (streets, buildings, floors),
Data/bergama_dem_glo30.json (terrain), selinus_board's items.json (above).
"""
import os, re, time, json

VERSION = "v5.2"  # v4.3: line weights scale with the drawing size (Aras 15:57 UTC, pages_common v3.33 pc_stroke_k);
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
GROUND = "FAF8F1"
SLAB_MM = 1.4                      # v2.9: page mm, the ground slab's cut face (slide 2 spine AXO_SLAB)
WHITE_RES = ("FFFFFF", "E9E6DF", "CDC8BC", "9E9889")   # v2.6: roof, lit wall, shaded wall, outline (MapBase A05 look)                  # the booklet axo's ground colour: a see-through fill is mixed onto it
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


def clean_list(c, tw, log):
    """v2.3: the numbered list (booklet coords): merge the duplicate hotel rows, renumber, drop default heights"""
    T = c["texts"]
    X0, Y0 = 314.0, 120.0                                # the list block (booklet mm); marker 12 sits at y 26
    inl = lambda t: t["anchor"]["pt"][0] >= X0 and t["anchor"]["pt"][1] >= Y0
    num = lambda t: t["string"].strip().isdigit()
    badges = dict((int(t["string"]), t) for t in T if inl(t) and num(t))
    names = sorted([t for t in T if inl(t) and not num(t) and not t["string"].startswith(u"\u00b7")
                    and t["string"] != u"NUMBERED ON THE DRAWING"], key=lambda t: -t["anchor"]["pt"][1])
    rowy = lambda t: t["anchor"]["pt"][1]
    name_of = lambda n: next((t for t in names if abs(rowy(t) - rowy(badges[n])) < 1.0), None)
    dup = [n for n in sorted(badges) if n > 1 and name_of(n) and name_of(n - 1) and
           name_of(n)["string"] == name_of(n - 1)["string"]]
    if not dup:
        log.append(u"list: no duplicate rows found")
        return c
    d = dup[0]
    yd, dy = rowy(badges[d]), rowy(badges[d - 1]) - rowy(badges[d])
    shapes, texts = [], []
    for sh in c["shapes"]:
        g = sh.get("grp") or u""
        pts = [q for R in sh.get("rings", []) for q in R] or sh.get("pts", [])
        if g.startswith(u"labels") and pts and min(q[0] for q in pts) >= X0 - 2.0 and min(q[1] for q in pts) >= Y0:
            cy = sum(q[1] for q in pts) / len(pts)
            if abs(cy - yd) < dy * 0.45:
                continue                                 # the duplicate row's badge
            if cy < yd - dy * 0.45:
                sh = dict(sh, rings=[[(q[0], q[1] + dy) for q in R] for R in sh["rings"]]) if "rings" in sh else \
                    dict(sh, pts=[(q[0], q[1] + dy) for q in sh["pts"]])
        shapes.append(sh)
    for t in T:
        x, y = t["anchor"]["pt"]
        if inl(t):
            if abs(y - yd) < 1.0:
                continue                                 # the duplicate row's words
            if y < yd - 1.0:
                t = dict(t, anchor=dict(t["anchor"], pt=[x, y + dy]))
        if num(t):
            n = int(t["string"])
            if n >= d:
                t = dict(t, string=str(n - 1))           # the drawing's marker d becomes d-1, the rest renumbered
        texts.append(t)
    c = dict(c, shapes=shapes, texts=texts)
    log.append(u"list: rows %d and %d were the same place (%s): merged, %d markers renumbered" % (
        d - 1, d, name_of(d - 1)["string"], len([b for b in badges if b >= d])))
    # notes: no default heights, one "most enclosed", names in full, words larger, notes after their names
    T = c["texts"]
    rows = [t for t in T if inl(t) and not num(t)]
    sky = [(int(re.search(r"(\d+)", t["string"]).group(1)), t) for t in rows if t["string"].startswith(u"Sky view")]
    lo = min(v for v, t in sky) if sky else None
    out = []
    for t in T:
        st = t["string"]
        if inl(t):
            if st == u"\u00b7 most open stretch of the bed":
                st = u"\u00b7 most open stretch"                 # shorter notes, so the list words can grow
            if st.strip() == u"\u00b7 5.00 m":
                continue
            if st == u"Kızıl Avlu Tapınağı Mısır Tanrıları":
                st = u"Kızıl Avlu"
            elif st == u"\u00b7 most enclosed stretch of the bed":
                nm = next((r for r in rows if r["string"].startswith(u"Sky view") and
                           abs(r["anchor"]["pt"][1] - t["anchor"]["pt"][1]) < 1.0), None)
                v = int(re.search(r"(\d+)", nm["string"]).group(1)) if nm else lo
                st = u"\u00b7 most enclosed stretch" if v == lo else u"\u00b7 enclosed stretch"
            t = dict(t, string=st)
        out.append(t)
    # the larger list words: up to 1.25 x, as far as the widest row stays inside the booklet's extent
    nm_ = lambda t: inl(t) and not num(t) and not t["string"].startswith(u"\u00b7")
    wrow = 0.0
    for r in out:
        if nm_(r):
            nt = next((t for t in out if inl(t) and t["string"].startswith(u"\u00b7") and
                       abs(t["anchor"]["pt"][1] - r["anchor"]["pt"][1]) < 1.0), None)
            w = tw(r["string"], r["size_pt"] * PT, True) + (1.2 + tw(nt["string"], nt["size_pt"] * PT, False)
                                                             if nt else 0.0)
            wrow = max(wrow, r["anchor"]["pt"][0] + w)
    x0 = min(r["anchor"]["pt"][0] for r in out if nm_(r))
    f = max(1.0, min(1.25, (c["extent"][2] - x0) / max(wrow - x0, 1.0)))
    out = [dict(t, size_pt=t["size_pt"] * f) if inl(t) and not num(t) else t for t in out]
    log.append(u"list: words x %.2f (widest row %.0f mm)" % (f, (wrow - x0) * f))
    for t in out:                                        # each note right after its row's name
        if inl(t) and t["string"].startswith(u"\u00b7"):
            nm = next((r for r in out if inl(r) and not num(r) and not r["string"].startswith(u"\u00b7") and
                       abs(r["anchor"]["pt"][1] - t["anchor"]["pt"][1]) < 1.0), None)
            if nm:
                t["anchor"] = dict(t["anchor"], pt=[nm["anchor"]["pt"][0] + tw(nm["string"], nm["size_pt"] * PT,
                                                                                True) + 1.2, t["anchor"]["pt"][1]])
    return dict(c, texts=out)


# ---------------------------------------------------------------- v2.5: roads and buildings from MapBase
# Aras 15 Nov 10:34 UTC: "axo drawing has mistakes how road is drawn and also the buildings doesnt seem right in many
# places". The booklet's roads were 212 separate strips (gaps at junctions, loose pieces) and its buildings came from
# the 9 Nov board site model. Both are redrawn from the one base map (MapBase cache, survey m) in the booklet
# engine's own way: its view (fitted to the booklet's slab, below), its terrain, its building faces and colours.
PHI = 32.9                         # deg: the booklet engine's view angle below the horizontal (DIAG_SRC PHI)
DEM = os.path.join("Data", "bergama_dem_glo30.json")
STOREY = {"civic": 3.5, "sacred": 5.0, "industry": 4.5}   # m per floor (Aras 12 Nov), else 3.0
CTX = ("FAF8F1", "D7D3C2", "BFBBAB", "949081")             # the engine's context building: roof, lit, shade, outline
SLAB_TOP = "EFEDE6"                # the slab's top face (fill) in the booklet drawing
ROAD = ("FAF8F1", "949081", 0.142)  # the booklet's street fill, edge colour, edge width (pt)
LEGEND_CLS = (("Workshops", "industry"), ("Commerce", "commerce"), ("Mixed use", "mixed"),
              ("Residential", "residential"), ("Sacred", "sacred"), ("Civic", "civic"), ("Ruins", "ruins"))


def _pip(x, y, R):
    ins, n = False, len(R)
    for i in range(n):
        (ax, ay), (bx, by) = R[i - 1], R[i]
        if (ay > y) != (by > y) and x < ax + (y - ay) * (bx - ax) / (by - ay):
            ins = not ins
    return ins


def _clip(R, H):
    """ring R cut to the convex window H (half-planes (a, b, c): a x + b y + c >= 0), Sutherland-Hodgman"""
    for a, b, c0 in H:
        out, n = [], len(R)
        for i in range(n):
            p, q = R[i - 1], R[i]
            fp, fq = a * p[0] + b * p[1] + c0, a * q[0] + b * q[1] + c0
            if fq >= 0:
                if fp < 0:
                    t = fp / (fp - fq)
                    out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
                out.append(q)
            elif fp >= 0:
                t = fp / (fp - fq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
        R = out
        if len(R) < 3:
            return []
    return R


class AxoView(object):
    """the booklet engine's view, fitted to the slab it drew (X = c0 + c1 x + c2 y; Y = oy + s (-c2 x + c1 y) +
    k cos(phi) z(x, y)), z = the DEM above the booklet's lowest node (offset fitted on the slab edge)"""

    def __init__(self, ring, corners, log):
        import math as m_
        self.m = m_
        E = []
        for i in range(4):
            p, q = corners[i], corners[(i + 1) % 4]
            L = m_.hypot(q[0] - p[0], q[1] - p[1])
            n = max(1, int(L / 15.0))                    # the engine's TERRAIN_CELL edge points
            E += [(p[0] + (q[0] - p[0]) * j / n, p[1] + (q[1] - p[1]) * j / n) for j in range(n)]
        if len(E) != len(ring):
            raise RuntimeError(u"the booklet slab has %d edge points, site_alan gives %d: not the same frame" % (
                len(ring), len(E)))
        # least squares X = c0 + c1 x + c2 y (3 x 3 normal equations)
        mx, my = sum(e[0] for e in E) / len(E), sum(e[1] for e in E) / len(E)
        mX = sum(r[0] for r in ring) / len(ring)
        sxx = sum((e[0] - mx) ** 2 for e in E)
        syy = sum((e[1] - my) ** 2 for e in E)
        sxy = sum((e[0] - mx) * (e[1] - my) for e in E)
        sxX = sum((e[0] - mx) * (r[0] - mX) for e, r in zip(E, ring))
        syX = sum((e[1] - my) * (r[0] - mX) for e, r in zip(E, ring))
        det = sxx * syy - sxy * sxy
        self.c1 = (sxX * syy - syX * sxy) / det
        self.c2 = (syX * sxx - sxX * sxy) / det
        self.c0 = mX - self.c1 * mx - self.c2 * my
        res = max(abs(self.c0 + self.c1 * e[0] + self.c2 * e[1] - r[0]) for e, r in zip(E, ring))
        self.k = m_.hypot(self.c1, self.c2)
        ph = m_.radians(PHI)
        self.s, self.kz = m_.sin(ph), self.k * m_.cos(ph)
        self.dem(log)
        fl = [self.s * (-self.c2 * e[0] + self.c1 * e[1]) for e in E]
        rr = [r[1] - f for r, f in zip(ring, fl)]
        self.oy = min(rr)
        zE = [(v - self.oy) / self.kz for v in rr]
        zD = [self.zdem(e[0], e[1]) for e in E]
        self.z0 = sum(a - b for a, b in zip(zD, zE)) / len(E)
        rms = (sum((a - b - self.z0) ** 2 for a, b in zip(zD, zE)) / len(E)) ** 0.5
        log.append(u"view: fitted to the booklet slab (%d edge points): across %.4f mm off at most, %.4f mm per m; "
                   u"terrain = elevation model - %.1f m, %.1f m rms on the slab edge" % (len(E), res, self.k, self.z0,
                                                                                      rms))
        if res > 0.02:
            log.append(u"FLAG view: the slab does not fit site_alan (%.3f mm): roads and buildings may be misplaced"
                       % res)
        if rms > 8.0:
            log.append(u"FLAG view: terrain %.1f m rms off the booklet's on its edge" % rms)
        a, b, c = self.c1, self.c2, self.s
        self.inv = (a * a * c + b * b * c)               # determinant of [[c1, c2], [-s c2, s c1]]

    def dem(self, log):
        p = os.path.join(BERGAMA_ROOT, DEM)
        with open(p, encoding="utf-8") as f:
            J = json.load(f)
        nr, nc, P = int(J["rows"]), int(J["cols"]), J["pts"]
        self.Z = [P[r * nc:(r + 1) * nc] for r in range(nr)]
        self.Z = [[q[2] for q in row] for row in self.Z]
        self.gx0, self.gy0 = P[0][0], P[0][1]
        self.gdx = (P[nc - 1][0] - P[0][0]) / float(nc - 1)
        self.gdy = (P[(nr - 1) * nc][1] - P[0][1]) / float(nr - 1)
        self.nr, self.nc = nr, nc

    def zdem(self, x, y):
        fi = min(self.nc - 1.000001, max(0.0, (x - self.gx0) / self.gdx))
        fj = min(self.nr - 1.000001, max(0.0, (y - self.gy0) / self.gdy))
        i, j = int(fi), int(fj)
        a, b = fi - i, fj - j
        Z = self.Z
        return (Z[j][i] * (1 - a) + Z[j][i + 1] * a) * (1 - b) + (Z[j + 1][i] * (1 - a) + Z[j + 1][i + 1] * a) * b

    def z(self, x, y):
        return max(0.0, self.zdem(x, y) - self.z0)

    def depth(self, x, y):
        return -self.c2 * x + self.c1 * y               # larger = farther (drawn first)

    def P(self, x, y, h=0.0):
        return (self.c0 + self.c1 * x + self.c2 * y,
                self.oy + self.s * self.depth(x, y) + self.kz * (self.z(x, y) + h))

    def back(self, X, Y):
        """plan point of a screen point on the ground (the terrain iterated)"""
        z = 0.0
        x = y = 0.0
        for _ in range(4):
            A, B = X - self.c0, Y - self.oy - self.kz * z
            # c1 x + c2 y = A ; s (-c2 x + c1 y) = B
            x = (A * self.c1 * self.s - self.c2 * B) / self.inv
            y = (self.c2 * self.s * A + self.c1 * B) / self.inv
            z = self.z(x, y)
        return x, y

    def facing(self, nx, ny):
        """outward normal (nx, ny): visible, lit (the engine's View.facing, in its own sin / cos)"""
        st, ct = self.c1 / self.k, -self.c2 / self.k
        return nx * ct + ny * st < -1e-9, (nx * st - ny * ct) < 0


def _bld_shapes(V, P, h, cols, topic):
    """the engine's draw_building for one footprint P (survey m, ccw) of height h: halo, walls far to near, roof"""
    roof, lit, shade, outline = cols
    walls = []
    n = len(P)
    for i in range(n):
        p, q = P[i], P[(i + 1) % n]
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = (dx * dx + dy * dy) ** 0.5
        if L < 1e-6:
            continue
        vis, lt = V.facing(dy / L, -dx / L)
        if vis:
            walls.append((V.depth((p[0] + q[0]) / 2.0, (p[1] + q[1]) / 2.0),
                          [V.P(p[0], p[1]), V.P(q[0], q[1]), V.P(q[0], q[1], h), V.P(p[0], p[1], h)],
                          lit if lt else shade))
    rf = [V.P(x, y, h) for x, y in P]
    walls.sort(key=lambda t: -t[0])
    sh = lambda rings, fi, st, w: {"t": "poly", "rings": rings, "fill": fi, "stroke": st, "width_pt": w,
                                   "dash_pt": None, "opacity": None, "grp": u"buildings/mb"}
    out = []
    if topic:
        out.append(sh([w_[1] for w_ in walls] + [rf], None, outline, 0.34))
    out += [sh([R_], c_, c_, 0.113) for _, R_, c_ in walls]
    out.append(sh([rf], roof, roof if topic else outline, 0.113 if topic else 0.142))
    return out


# ================================================================ v4.0: the axo as a real 3D model in Rhino (shared base)
# Aras 14:50-14:53 UTC: "draw these in 3D with scripts in rhino and take the drawings from rhino because the way you
# approach you mix the foreground and background"; he chose "Shaded view capture"; "shaded view capture should get a
# facelift with what we have talked till now"; "you can use that 3D map everywhere you want". So every layer the 2D axo
# drew is built as 3D in the open Rhino (one layer AXO3D_LAYER, objects deleted after the capture, the 3dm never saved),
# from the same data (MapBase cache, DEM, the booklet's use class per building): terrain slab, parks, streets, river
# (flat), historic walls (dashed), buildings (cut to site_alan, roofs and lit / shaded walls in this axo's colours, thin
# outlines), trees (smooth crowns coloured from Aras's painted symbols, light to dark across the crown, with leaf
# patches; trunks; grey ground shadows), all in FLAT colours computed here (vertex colours) and shown in the display
# mode AXO3D_MODE (a copy of Shaded with lighting, isocurves and mesh wires off), so nothing gets Rhino's default grey
# look. The view is a parallel view along the axo's camera; Rhino's depth buffer settles what is in front.
# Other scripts may call: axo3d_build(doc, d3, dem, log) -> (guids, bbox); axo3d_capture(doc, cam, pts, width, png,
# log) -> {"png", "w", "h", "px": [(world point, image px)]}; axo3d_clear(doc, guids, log). cam = (right, up, dir) unit
# vectors; d3 = the dict rebuild() returns in c["d3"] (plan rings in survey m, colours as hex).
AXO3D_LAYER = "axo3d_page01"
AXO3D_MODE = "Bergama Axo"
AXO3D_PX = 6000                    # capture width in pixels (about 380 ppi on the 396 mm page drawing)
AXO_RASTER = False                 # v5.0: the page drawing is vector (the Rhino capture route off)
AXO3D_CAL = "C8C8C8"               # v4.5: the calibration tile's colour (outside the slab, cleared after)
AXO3D_DZ = {"terrain": 0.0, "parks": 0.35, "streets": 0.55, "water": 0.7, "shadow": 0.8, "edge": 0.95}
AXO3D_TREE_GLB = os.path.join(BERGAMA_ROOT, "Data", "trees3d", "broadleaf.glb")   # v4.2: a 3D tree model (optional)
AXO3D_TREE_FACES = 2500            # v4.2: the model reduced to about this many faces (3,000+ trees in the axo)
AXO3D_TREE_CREDIT = (u"3D tree model: 'Small Ash Tree' by rhcreations, Sketchfab "
                     u"https://sketchfab.com/models/5382ed9455b44e77ba3d2e128ce4b076, CC BY")   # logs only, never drawn
LIGHT = (-0.45, 0.55, 0.70)        # the crowns' light (from the upper left of the view, as the buildings' lit walls)


def _rgb(h):
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _mixc(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def axo3d_mode(log):
    """the flat display mode (a copy of Shaded: lighting, isocurves, surface edges, mesh wires off); its Id"""
    import Rhino, System
    D = Rhino.Display.DisplayModeDescription
    m = D.FindByName(AXO3D_MODE)
    if m is None:
        base = D.FindByName("Shaded")
        nid = D.CopyDisplayMode(base.Id, AXO3D_MODE)
        m = D.GetDisplayMode(nid)
    a = m.DisplayAttributes
    done, miss = [], []

    def put(obj, nm, val):
        try:
            setattr(obj, nm, val)
            done.append(nm)
        except Exception:
            miss.append(nm)
    for nm, val in (("ShowIsoCurves", False), ("ShowSurfaceEdges", False), ("ShowTangentEdges", False),
                    ("ShowTangentSeams", False), ("ShowGrid", False), ("ShowGridAxes", False), ("ShowWorldAxes", False),
                    ("CurveThickness", 1), ("ShadingEnabled", True), ("CastShadows", False)):
        put(a, nm, val)
    try:
        LS = Rhino.Display.DisplayPipelineAttributes.LightingSchema
        import System as S_
        none_ = [v for v in S_.Enum.GetValues(LS) if str(v) in ("None", "None_")]   # v4.3: "None" is a Python word
        if not none_:
            raise RuntimeError(u"values: %s" % u", ".join(str(v) for v in S_.Enum.GetValues(LS)))
        put(a, "LightingScheme", none_[0])
    except Exception as ex:
        miss.append("LightingScheme (%s: %s)" % (type(ex).__name__, ex))
    try:                                                 # v4.4: a white background (no dark fringe at the edges)
        a.FillMode = Rhino.Display.DisplayPipelineAttributes.FrameBufferFillMode.SolidColor
        a.SetFill(System.Drawing.Color.White)
        done.append("white background")
    except Exception as ex:
        miss.append("white background (%s: %s)" % (type(ex).__name__, ex))
    try:
        ma = a.MeshSpecificAttributes
        for nm in ("ShowMeshWires", "ShowMeshEdges", "ShowMeshNakedEdges", "ShowMeshNonmanifoldEdges"):
            put(ma, nm, False)
    except Exception:
        miss.append("MeshSpecificAttributes")
    try:
        D.UpdateDisplayMode(m)
    except Exception as ex:
        log.append(u"FLAG 3D: display mode %s not updated (%s)" % (AXO3D_MODE, ex))
    log.append(u"3D: display mode '%s': set %s%s" % (AXO3D_MODE, u", ".join(done),
                                                    (u"; FLAG not set: " + u", ".join(miss)) if miss else u""))
    return m


def axo3d_tree_model(doc, log, path=AXO3D_TREE_GLB):
    """v4.2: the 3D tree model as one mesh (base centre at the origin, z up, crown width 1, about AXO3D_TREE_FACES
    faces), imported from path into the open Rhino and its imported objects removed again; None if missing / failed"""
    if not os.path.isfile(path):
        log.append(u"3D trees: no model at %s: smooth crowns drawn instead" % path)
        return None
    import Rhino
    import Rhino.Geometry as rg
    keep = set(o.Id for o in doc.Objects)
    ndef0 = doc.InstanceDefinitions.Count
    lay0 = set(l.Id for l in doc.Layers)                  # v4.3: the import's own layers are removed again
    try:
        ok = doc.Import(path)
    except Exception as ex:
        log.append(u"FLAG 3D trees: import of %s failed (%s): smooth crowns drawn instead" % (path, ex))
        return None
    new = [o for o in doc.Objects if o.Id not in keep]
    M = rg.Mesh()

    def grab(o, xf=None):
        g = o.Geometry
        if isinstance(g, rg.Mesh):
            m = g.DuplicateMesh()
        elif isinstance(g, rg.Brep):
            ms = rg.Mesh.CreateFromBrep(g, rg.MeshingParameters.FastRenderMesh) or []
            m = rg.Mesh()
            for x_ in ms:
                m.Append(x_)
        elif isinstance(g, rg.Extrusion):
            m = rg.Mesh.CreateFromBrep(g.ToBrep(), rg.MeshingParameters.FastRenderMesh)
            m = m[0] if m else None
        elif isinstance(o, Rhino.DocObjects.InstanceObject):
            x2 = o.InstanceXform if xf is None else xf * o.InstanceXform
            for so in o.InstanceDefinition.GetObjects():
                grab(so, x2)
            return
        else:
            return
        if m is not None:
            if xf is not None:
                m.Transform(xf)
            M.Append(m)
    for o in new:
        grab(o)
    for o in new:
        doc.Objects.Delete(o.Id, True)
    for i in range(doc.InstanceDefinitions.Count - 1, ndef0 - 1, -1):   # the model's own block definitions
        try:
            doc.InstanceDefinitions.Delete(i, True, True)
        except Exception:
            pass
    nl_ = 0
    for l in sorted([l for l in doc.Layers if l.Id not in lay0 and not l.IsDeleted], key=lambda l: -len(l.FullPath)):
        try:
            nl_ += 1 if doc.Layers.Delete(l.Index, True) else 0
        except Exception:
            pass
    log.append(u"3D trees: %d imported layer(s) removed" % nl_)
    if M.Faces.Count == 0:
        log.append(u"FLAG 3D trees: %s imported %d object(s) but no mesh: smooth crowns drawn instead" % (path, len(new)))
        return None
    f0 = M.Faces.Count
    bb = M.GetBoundingBox(True)
    dx, dy, dz = bb.Max.X - bb.Min.X, bb.Max.Y - bb.Min.Y, bb.Max.Z - bb.Min.Z
    if dy > 1.5 * dz and dy > dx:                         # still Y up (glTF): stand it up
        M.Rotate(1.5707963267948966, rg.Vector3d.XAxis, rg.Point3d.Origin)
        bb = M.GetBoundingBox(True)
    if M.Faces.Count > AXO3D_TREE_FACES:
        try:
            M.Reduce(AXO3D_TREE_FACES, True, 5, True)
        except Exception as ex:
            log.append(u"3D trees: model not reduced (%s)" % ex)
    bb = M.GetBoundingBox(True)
    w = max(bb.Max.X - bb.Min.X, bb.Max.Y - bb.Min.Y) or 1.0
    M.Translate(-(bb.Min.X + bb.Max.X) / 2.0, -(bb.Min.Y + bb.Max.Y) / 2.0, -bb.Min.Z)
    M.Scale(1.0 / w)
    M.VertexColors.Clear()
    M.Normals.ComputeNormals()
    M.Compact()
    hb = M.GetBoundingBox(True)
    log.append(u"3D trees: model %s, %d object(s), %d -> %d faces, height / width %.2f" % (
        os.path.basename(path), len(new), f0, M.Faces.Count, hb.Max.Z - hb.Min.Z))
    log.append(AXO3D_TREE_CREDIT)
    return M


def axo3d_build(doc, d3, dem, log):
    """every d3 layer as meshes (vertex colours) and curves on AXO3D_LAYER; dem(x, y) = ground z (m, absolute)"""
    import Rhino, System
    import Rhino.Geometry as rg
    import math as m_
    t0 = time.time()
    li = doc.Layers.FindByFullPath(AXO3D_LAYER, -1)
    if li < 0:
        L = Rhino.DocObjects.Layer()
        L.Name = AXO3D_LAYER
        li = doc.Layers.Add(L)
    old = doc.Objects.FindByLayer(doc.Layers[li]) or []
    for o in old:
        doc.Objects.Delete(o.Id, True)
    guids = []
    tol = doc.ModelAbsoluteTolerance or 0.001
    Dv0 = d3["cam_dir"]
    ln0 = m_.sqrt(sum(v * v for v in Dv0)) or 1.0
    NV = (-Dv0[0] / ln0, -Dv0[1] / ln0, -Dv0[2] / ln0)    # v4.5: the normal every face gets
    col = lambda h: System.Drawing.Color.FromArgb(*_rgb(h))

    def attr(h=None):
        a = Rhino.DocObjects.ObjectAttributes()
        a.LayerIndex = li
        if h:
            a.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
            a.ObjectColor = col(h)
        return a

    def face_cam(M):                                     # v4.5: every normal toward the camera (uniform light)
        M.Normals.Clear()
        for i in range(M.Vertices.Count):
            M.Normals.Add(NV[0], NV[1], NV[2])

    def add_mesh(M, h=None):
        if M is None or M.Vertices.Count == 0:
            return
        M.Compact()
        face_cam(M)
        g = doc.Objects.AddMesh(M, attr(h))
        if g != System.Guid.Empty:
            guids.append(g)

    def paint(M, h):
        c = col(h)
        M.VertexColors.Clear()
        for _ in range(M.Vertices.Count):
            M.VertexColors.Add(c)
        return M

    mp = rg.MeshingParameters.Minimal
    try:
        mp.SimplePlanes = False
        mp.MaximumEdgeLength = 5.0
        mp.GridMinCount = 0
    except Exception:
        pass

    def region(rings, h, dz, key):
        """closed plan rings (holes by nesting) -> one draped mesh in flat colour h"""
        cs = []
        for R in rings:
            if len(R) >= 3:
                pl = rg.Polyline([rg.Point3d(q[0], q[1], 0.0) for q in R] + [rg.Point3d(R[0][0], R[0][1], 0.0)])
                cs.append(pl.ToPolylineCurve())
        if not cs:
            return 0
        breps = rg.Brep.CreatePlanarBreps(cs, tol) or []
        M = rg.Mesh()
        for b in breps:
            for mm in rg.Mesh.CreateFromBrep(b, mp) or []:
                M.Append(mm)
        for i in range(M.Vertices.Count):
            v = M.Vertices[i]
            M.Vertices.SetVertex(i, v.X, v.Y, dem(v.X, v.Y) + dz)
        add_mesh(paint(M, h), h)
        log.append(u"3D %s: %d ring(s) -> %d face(s)" % (key, len(cs), M.Faces.Count))
        return M.Faces.Count

    def drape_line(P, h, dz, dash=None):
        if len(P) < 2:
            return
        pts = []
        for i in range(1, len(P)):
            a, b = P[i - 1], P[i]
            n = max(1, int(m_.hypot(b[0] - a[0], b[1] - a[1]) / 3.0))
            pts += [(a[0] + (b[0] - a[0]) * t / float(n), a[1] + (b[1] - a[1]) * t / float(n)) for t in range(n)]
        pts.append(P[-1])
        runs = [pts]
        if dash:                                         # dashes in metres along the line
            runs, cur, s, on = [], [pts[0]], 0.0, True
            for i in range(1, len(pts)):
                s += m_.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
                if on:
                    cur.append(pts[i])
                if s >= (dash[0] if on else dash[1]):
                    if on and len(cur) > 1:
                        runs.append(cur)
                    on, s, cur = not on, 0.0, [pts[i]]
            if on and len(cur) > 1:
                runs.append(cur)
        for r in runs:
            pl = rg.Polyline([rg.Point3d(q[0], q[1], dem(q[0], q[1]) + dz) for q in r])
            g = doc.Objects.AddPolyline(pl, attr(h))
            if g != System.Guid.Empty:
                guids.append(g)

    if d3.get("cal"):                                    # v4.5: the calibration tile
        q_ = d3["cal"]
        cm = rg.Mesh()
        for p_ in q_:
            cm.Vertices.Add(p_[0], p_[1], p_[2])
        cm.Faces.AddFace(0, 1, 2, 3)
        add_mesh(paint(cm, AXO3D_CAL), AXO3D_CAL)
    # ground: slab top (terrain), parks, streets, water, their edges, historic walls
    region([d3["slab"]], d3["c_slab"], AXO3D_DZ["terrain"], "terrain")
    region(d3["parks"], d3["c_park"], AXO3D_DZ["parks"], "parks")
    region(d3["streets"], d3["c_street"], AXO3D_DZ["streets"], "streets")
    region(d3["water"], d3["c_water"], AXO3D_DZ["water"], "water")
    for P in d3["street_edges"]:
        drape_line(P, d3["c_street_edge"], AXO3D_DZ["edge"])
    for P in d3["water_edges"]:
        drape_line(P, d3["c_water_edge"], AXO3D_DZ["edge"])
    for P in d3["walls"]:
        drape_line(P, d3["c_wall"], AXO3D_DZ["edge"] + 0.3, (4.0, 2.5))

    # buildings: walls in their lit / shaded colour, roof, outline (roof ring + corner edges)
    E, F = d3["cam_e"], d3["cam_f"]
    Dv = d3["cam_dir"]
    pull = lambda x, y, z: rg.Point3d(x - 0.25 * Dv[0], y - 0.25 * Dv[1], z - 0.25 * Dv[2])   # outlines a hair toward the camera
    bm = {}
    nb = 0
    for P, h, cols in d3["blds"]:
        zs = [dem(x, y) for x, y in P]
        gz = dem(sum(q[0] for q in P) / len(P), sum(q[1] for q in P) / len(P))
        z0, z1 = min(zs) - 1.0, gz + h
        n = len(P)
        for i in range(n):
            p, q = P[i], P[(i + 1) % n]
            dx, dy = q[0] - p[0], q[1] - p[1]
            L = m_.hypot(dx, dy)
            if L < 1e-6:
                continue
            nx, ny = dy / L, -dx / L                     # outward (P ccw)
            lit = (nx * E[0] + ny * E[1]) < 0           # as V.facing: walls facing left are lit
            hc = cols[1] if lit else cols[2]
            M = bm.setdefault(hc, rg.Mesh())
            k0 = M.Vertices.Count
            for x_, y_, z_ in ((p[0], p[1], z0), (q[0], q[1], z0), (q[0], q[1], z1), (p[0], p[1], z1)):
                M.Vertices.Add(x_, y_, z_)
            M.Faces.AddFace(k0, k0 + 1, k0 + 2, k0 + 3)
        roof = rg.Mesh.CreateFromClosedPolyline(rg.Polyline([rg.Point3d(x, y, z1) for x, y in P] +
                                                            [rg.Point3d(P[0][0], P[0][1], z1)]))
        if roof:
            bm.setdefault(cols[0], rg.Mesh()).Append(roof)
        ring = [pull(x, y, z1) for x, y in P] + [pull(P[0][0], P[0][1], z1)]
        g = doc.Objects.AddPolyline(rg.Polyline(ring), attr(cols[3]))
        if g != System.Guid.Empty:
            guids.append(g)
        for x, y in P:                                   # the depth buffer hides the corners behind the walls
            g = doc.Objects.AddLine(rg.Line(pull(x, y, dem(x, y)), pull(x, y, z1)), attr(cols[3]))
            if g != System.Guid.Empty:
                guids.append(g)
        nb += 1
    for hc, M in bm.items():
        add_mesh(paint(M, hc), hc)

    # trees: grey ground shadow, trunk, a smooth crown shaded light to dark with leaf patches (vertex colours)
    Lx, Ly, Lz = LIGHT
    ln = m_.sqrt(Lx * Lx + Ly * Ly + Lz * Lz)
    Lw = (Lx / ln * E[0] + Ly / ln * F[0], Lx / ln * E[1] + Ly / ln * F[1], Lz / ln)   # light in world axes
    crown, trunk, shadow = rg.Mesh(), rg.Mesh(), rg.Mesh()
    nt = 0
    TM = axo3d_tree_model(doc, log)                      # v4.2: the 3D tree model as blocks, one per colour set
    tdefs = {}
    if TM is not None:
        for x, y, D, cl in d3["trees"]:
            key = tuple(cl)
            if key not in tdefs:
                lt, body, dk = _rgb(cl[0]), _rgb(cl[1]), _rgb(cl[2])
                m = TM.DuplicateMesh()
                for i in range(m.Vertices.Count):
                    n_ = m.Normals[i]
                    lam = max(0.0, n_.X * Lw[0] + n_.Y * Lw[1] + n_.Z * Lw[2])
                    c = _mixc(dk, body, min(1.0, lam * 1.4)) if lam < 0.7 else _mixc(body, lt, (lam - 0.7) / 0.3)
                    m.VertexColors.Add(System.Drawing.Color.FromArgb(*c))
                face_cam(m)                                  # v4.5
                a_ = attr()
                nm_ = u"axo3d_tree_%d" % len(tdefs)
                old_ = doc.InstanceDefinitions.Find(nm_)
                if old_ is not None:
                    doc.InstanceDefinitions.Delete(old_.Index, True, True)
                tdefs[key] = doc.InstanceDefinitions.Add(nm_, u"Page01Axo 3D tree", rg.Point3d.Origin, [m], [a_])
        hz = TM.GetBoundingBox(True).Max.Z
    for x, y, D, cl in d3["trees"]:
        if TM is not None and tdefs.get(tuple(cl), -1) >= 0:
            gz = dem(x, y)
            xf = rg.Transform.Translation(x, y, gz) * rg.Transform.Scale(rg.Point3d.Origin, D)
            g = doc.Objects.AddInstanceObject(tdefs[tuple(cl)], xf, attr())
            if g != System.Guid.Empty:
                guids.append(g)
            rs = D / 2.0 * 0.95
            sh = rg.Mesh.CreateFromClosedPolyline(rg.Polyline(
                [rg.Point3d(x + rs * m_.cos(t) + 0.3 * rs * E[0], y + rs * m_.sin(t) + 0.3 * rs * E[1],
                            dem(x + rs * m_.cos(t), y + rs * m_.sin(t)) + AXO3D_DZ["shadow"])
                 for t in [j * m_.pi / 10.0 for j in range(20)]] +
                [rg.Point3d(x + rs + 0.3 * rs * E[0], y + 0.3 * rs * E[1], dem(x + rs, y) + AXO3D_DZ["shadow"])]))
            if sh:
                shadow.Append(sh)
            nt += 1
            continue
        lt, body, dk = _rgb(cl[0]), _rgb(cl[1]), _rgb(cl[2])
        r = D / 2.0
        gz = dem(x, y)
        ht = max(1.5, 0.45 * D)
        cz = gz + ht + 0.55 * D
        sp = rg.Mesh.CreateFromSphere(rg.Sphere(rg.Point3d(x, y, cz), r), 14, 10)
        sp.Transform(rg.Transform.Scale(rg.Plane(rg.Point3d(x, y, cz), rg.Vector3d.ZAxis), 1.0, 1.0, 1.15))
        seed = (int(x * 10) * 7 + int(y * 10) * 13) % 997
        cols_ = []
        for i in range(sp.Vertices.Count):
            v = sp.Vertices[i]
            nx, ny, nz = (v.X - x) / r, (v.Y - y) / r, (v.Z - cz) / (1.15 * r)
            lam = max(0.0, nx * Lw[0] + ny * Lw[1] + nz * Lw[2])
            leaf = ((i * 37 + seed) % 7) / 6.0              # leaf patches: coarse, a few vertices each
            c = _mixc(dk, body, min(1.0, lam * 1.4)) if lam < 0.7 else _mixc(body, lt, (lam - 0.7) / 0.3)
            if leaf > 0.8:
                c = _mixc(c, dk, 0.45)
            cols_.append(System.Drawing.Color.FromArgb(*c))
        for c in cols_:
            sp.VertexColors.Add(c)
        crown.Append(sp)
        cyl = rg.Mesh.CreateFromCylinder(rg.Cylinder(rg.Circle(rg.Plane(rg.Point3d(x, y, gz), rg.Vector3d.ZAxis),
                                                               max(0.2, 0.04 * D)), ht + 0.3 * D), 1, 6)
        trunk.Append(cyl)
        rs = r * 0.95
        sh = rg.Mesh.CreateFromClosedPolyline(rg.Polyline(
            [rg.Point3d(x + rs * m_.cos(t) + 0.3 * rs * E[0], y + rs * m_.sin(t) + 0.3 * rs * E[1],
                        dem(x + rs * m_.cos(t), y + rs * m_.sin(t)) + AXO3D_DZ["shadow"])
             for t in [j * m_.pi / 10.0 for j in range(20)]] +
            [rg.Point3d(x + rs + 0.3 * rs * E[0], y + 0.3 * rs * E[1], dem(x + rs, y) + AXO3D_DZ["shadow"])]))
        if sh:
            shadow.Append(sh)
        nt += 1
    add_mesh(paint(shadow, d3["c_shadow"]), d3["c_shadow"])
    add_mesh(paint(trunk, d3["c_trunk"]), d3["c_trunk"])
    add_mesh(crown, None)
    bb = rg.BoundingBox.Empty
    for g in guids:
        o = doc.Objects.FindId(g)
        if o:
            bb.Union(o.Geometry.GetBoundingBox(True))
    log.append(u"3D: %d buildings, %d trees, %d objects on layer %s in %.1f s" % (nb, nt, len(guids), AXO3D_LAYER,
                                                                                 time.time() - t0))
    return guids, bb


def axo3d_capture(doc, cam, pts, width, png, log, fit=None, mode_name=None):
    """the axo's parallel view (cam = (right, up, dir)) of the AXO3D layer alone, every other layer hidden, in
    AXO3D_MODE, zoomed to fit (a BoundingBox) or the model, captured width px wide (transparent) to png; returns
    {"png", "w", "h", "px": [(pt, (px, py))]} for the world points pts (to register the image)"""
    import Rhino, System
    import Rhino.Geometry as rg
    view = doc.Views.ActiveView
    vp = view.ActiveViewport
    info0 = Rhino.DocObjects.ViewportInfo(vp)
    dm0 = vp.DisplayMode
    vis = [(l.Index, l.IsVisible) for l in doc.Layers if not l.IsDeleted]
    cur0 = doc.Layers.CurrentLayerIndex
    li = doc.Layers.FindByFullPath(AXO3D_LAYER, -1)
    try:
        doc.Layers.SetCurrentLayerIndex(li, True)
        for l in doc.Layers:
            if l.IsDeleted:
                continue
            on = l.Index == li
            if l.IsVisible != on:
                l.IsVisible = on
                try:
                    doc.Layers.Modify(l, l.Index, True)
                except Exception:
                    pass
        R, U, Dv = cam
        vp.ChangeToParallelProjection(True)
        bb = fit
        if bb is None or not bb.IsValid:
            bb = rg.BoundingBox.Empty
            for o in doc.Objects.FindByLayer(doc.Layers[li]) or []:
                bb.Union(o.Geometry.GetBoundingBox(True))
        tg = bb.Center
        dv = rg.Vector3d(*Dv)
        vp.SetCameraLocations(tg, tg - dv * (bb.Diagonal.Length * 2.0 + 100.0))
        vp.CameraUp = rg.Vector3d(*U)
        vp.ZoomBoundingBox(bb)
        if mode_name in (None, AXO3D_MODE):
            mode = axo3d_mode(log)
        else:                                            # v4.2: a built-in mode by name ("Shaded", "Rendered")
            mode = Rhino.Display.DisplayModeDescription.FindByName(mode_name)
            if mode is None:
                raise RuntimeError(u"no display mode %s" % mode_name)
        vp.DisplayMode = mode
        view.Redraw()
        try:
            log.append(u"3D capture: the viewport shows display mode '%s'" % vp.DisplayMode.EnglishName)
        except Exception:
            pass
        sz = vp.Size
        h = int(round(width * sz.Height / float(sz.Width)))
        # v4.3: run 22's three tries were byte-identical wireframes (ViewCapture ignored the mode set on the viewport):
        # the view is now rendered in the named mode itself (RhinoView.CaptureToBitmap(size, mode)) on a white
        # background, white made transparent after (the page is white too)
        AS = Rhino.ApplicationSettings.AppearanceSettings
        bg0 = AS.ViewportBackgroundColor
        bmp = None
        try:
            AS.ViewportBackgroundColor = System.Drawing.Color.White
            view.Redraw()
            bmp = view.CaptureToBitmap(System.Drawing.Size(int(width), h), mode)
            log.append(u"3D capture: rendered by the view in mode '%s'" % mode.EnglishName)
        except Exception as ex:
            log.append(u"3D capture: view.CaptureToBitmap(size, mode) failed (%s: %s): ViewCapture used" % (
                type(ex).__name__, ex))
        finally:
            AS.ViewportBackgroundColor = bg0
        if bmp is None:
            cap = Rhino.Display.ViewCapture()
            cap.Width, cap.Height = int(width), h
            for nm, val in (("ScaleScreenItems", False), ("DrawAxes", False), ("DrawGrid", False),
                            ("DrawGridAxes", False), ("TransparentBackground", True)):
                try:
                    setattr(cap, nm, val)
                except Exception:
                    log.append(u"3D capture: %s not set" % nm)
            bmp = cap.CaptureToBitmap(view)
        if bmp is None:
            raise RuntimeError(u"Rhino returned no image")
        cs_ = [bmp.GetPixel(x_, y_) for x_, y_ in ((2, 2), (bmp.Width - 3, 2), (bmp.Width - 3, bmp.Height // 2),
                                                    (2, bmp.Height // 2))]   # v4.4: the background = the corners'
        key_ = max(cs_, key=lambda c_: sum(1 for d_ in cs_ if d_.ToArgb() == c_.ToArgb()))
        log.append(u"3D capture: background %d/%d/%d (from the corners) made transparent" % (key_.R, key_.G, key_.B))
        bmp.MakeTransparent(key_)
        os.makedirs(os.path.dirname(png), exist_ok=True)
        bmp.Save(png, System.Drawing.Imaging.ImageFormat.Png)
        f = width / float(sz.Width)
        px = []
        for p in pts:
            q = vp.WorldToClient(rg.Point3d(*p))
            px.append((p, (q.X * f, q.Y * f)))
        log.append(u"3D capture: %d x %d px from a %d x %d viewport -> %s" % (width, h, sz.Width, sz.Height, png))
        return {"png": png, "w": int(width), "h": h, "px": px}
    finally:
        for i_, was in vis:
            l = doc.Layers[i_]
            if l.IsVisible != was:
                l.IsVisible = was
                try:
                    doc.Layers.Modify(l, i_, True)
                except Exception:
                    pass
        try:
            doc.Layers.SetCurrentLayerIndex(cur0, True)
        except Exception:
            pass
        try:
            vp.SetViewProjection(info0, True)
            vp.DisplayMode = dm0
        except Exception:
            pass
        view.Redraw()


def axo3d_calibrate(cap, quad_px, log, target=AXO3D_CAL):
    """v4.5: Rhino's light scales every colour (one factor, all normals face the camera): the calibration tile's mean
    colour against its true colour gives a gain per channel, applied to the whole capture (saved in place); the tile is
    then cleared. Returns the gains"""
    import System
    D_ = System.Drawing
    xs, ys = [q[0] for q in quad_px], [q[1] for q in quad_px]
    cx, cy = sum(xs) / 4.0, sum(ys) / 4.0
    bm = D_.Bitmap(cap["png"])
    sr = sg = sb = n = 0
    for j in range(-6, 7):
        for i in range(-6, 7):
            x, y = int(cx + i * (max(xs) - min(xs)) / 40.0), int(cy + j * (max(ys) - min(ys)) / 40.0)
            if 0 <= x < bm.Width and 0 <= y < bm.Height:
                p = bm.GetPixel(x, y)
                if p.A > 200:
                    sr, sg, sb, n = sr + p.R, sg + p.G, sb + p.B, n + 1
    if n < 20:
        bm.Dispose()
        log.append(u"FLAG 3D colour: the calibration tile was not found in the capture (%d px): colours as Rhino drew them"
                   % n)
        return None
    t = _rgb(target)
    g = [t[0] / max(1.0, sr / float(n)), t[1] / max(1.0, sg / float(n)), t[2] / max(1.0, sb / float(n))]
    out = D_.Bitmap(bm.Width, bm.Height, D_.Imaging.PixelFormat.Format32bppArgb)
    gr = D_.Graphics.FromImage(out)
    try:
        cmx = D_.Imaging.ColorMatrix()
        cmx.Matrix00, cmx.Matrix11, cmx.Matrix22, cmx.Matrix33, cmx.Matrix44 = g[0], g[1], g[2], 1.0, 1.0
        ia = D_.Imaging.ImageAttributes()
        ia.SetColorMatrix(cmx)
        gr.DrawImage(bm, D_.Rectangle(0, 0, bm.Width, bm.Height), 0, 0, bm.Width, bm.Height, D_.GraphicsUnit.Pixel, ia)
    finally:
        gr.Dispose()
        bm.Dispose()
    pad = 4
    for y in range(max(0, int(min(ys)) - pad), min(out.Height, int(max(ys)) + pad + 1)):   # clear the tile
        for x in range(max(0, int(min(xs)) - pad), min(out.Width, int(max(xs)) + pad + 1)):
            out.SetPixel(x, y, D_.Color.Transparent)
    out.Save(cap["png"], D_.Imaging.ImageFormat.Png)
    out.Dispose()
    log.append(u"3D colour: calibration tile read %d/%d/%d (true %d/%d/%d), gains %.2f / %.2f / %.2f applied" % (
        sr // n, sg // n, sb // n, t[0], t[1], t[2], g[0], g[1], g[2]))
    return g


def axo3d_check(cap, log, min_cover=0.95, max_dark=0.12):
    """v4.2: (ok, text): the capture inside the slab edge (cap["px"], the edge points in order) must be opaque (shaded
    faces, not wires on a transparent ground) and not mostly near-black"""
    import System
    P = [q for _, q in cap["px"]]
    xs, ys = [q[0] for q in P], [q[1] for q in P]

    def inside(x, y):
        c_ = False
        for i in range(len(P)):
            (x1, y1), (x2, y2) = P[i - 1], P[i]
            if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                c_ = not c_
        return c_
    bm = System.Drawing.Bitmap(cap["png"])
    n = op = dk = semi = 0
    sr = sg = sb = 0
    try:
        for j in range(60):
            for i in range(120):
                x = min(xs) + (max(xs) - min(xs)) * (i + 0.5) / 120.0
                y = min(ys) + (max(ys) - min(ys)) * (j + 0.5) / 60.0
                if not inside(x, y) or not (0 <= x < bm.Width and 0 <= y < bm.Height):
                    continue
                px = bm.GetPixel(int(x), int(y))
                n += 1
                if 0 < px.A <= 200:
                    semi += 1
                if px.A > 200:
                    op += 1
                    sr, sg, sb = sr + px.R, sg + px.G, sb + px.B
                    if px.R + px.G + px.B < 120:
                        dk += 1
    finally:
        bm.Dispose()
    if n == 0:
        return False, u"no samples inside the slab edge"
    cov, dark = op / float(n), dk / float(max(1, op))
    return cov >= min_cover and dark <= max_dark, (u"%d samples, %.0f %% opaque, %.0f %% half-transparent, %.0f %% "
                                                   u"near-black, mean opaque colour %d/%d/%d, image %d x %d" % (
        n, 100 * cov, 100.0 * semi / n, 100 * dark, sr // max(1, op), sg // max(1, op), sb // max(1, op),
        cap["w"], cap["h"]))


def axo3d_clear(doc, guids, log):
    n = 0
    for g in guids:
        n += 1 if doc.Objects.Delete(g, True) else 0
    for d_ in list(doc.InstanceDefinitions):             # v4.2: the tree blocks
        try:
            if d_ is not None and not d_.IsDeleted and d_.Name.startswith(u"axo3d_tree_"):
                doc.InstanceDefinitions.Delete(d_.Index, True, True)
        except Exception:
            pass
    li = doc.Layers.FindByFullPath(AXO3D_LAYER, -1)
    if li >= 0:
        try:
            doc.Layers.Delete(li, True)
        except Exception:
            pass
    doc.Views.Redraw()
    log.append(u"3D: %d objects and layer %s removed (the 3dm is not saved)" % (n, AXO3D_LAYER))


# v5.2: the 3D drawing order sits here so slide 2 node axos and diagrams use the same one (Aras 19:06 UTC "draw the axo
# once properly ... we can get everything from there")
def _pin(X, Y, R):
    c_ = False
    for i in range(len(R)):
        (x1, y1), (x2, y2) = R[i - 1], R[i]
        if (y1 > Y) != (y2 > Y) and X < x1 + (Y - y1) * (x2 - x1) / (y2 - y1):
            c_ = not c_
    return c_


def _depth_order(V, objs, log):
    """v5.0 (Aras 17:02 UTC "it is a raster image we want it vectoral"; 14:50 "you mix the foreground and background"):
    the drawing order of the buildings and trees worked out from their 3D form, not from one depth number each: for every
    two objects whose pictures overlap, a point inside both is found and the ray through it is followed into each (roof
    or wall plane of a building, the front of a tree crown): the one it meets first (smaller plan depth along the view)
    is drawn after the other; the order is then a topological sort of these pairs, far objects first where nothing ties
    them. objs: dicts with d (depth of the middle), sh (shapes), and either P, h (building) or x, y, D (tree)"""
    import heapq
    m_ = V.m
    k = V.k
    for o in objs:                                       # pictures: polygons on the drawing (booklet mm)
        if "P" in o:
            P, h = o["P"], o["h"]
            polys, walls = [], []
            for i in range(len(P)):
                p, q = P[i], P[(i + 1) % len(P)]
                dx, dy = q[0] - p[0], q[1] - p[1]
                L = (dx * dx + dy * dy) ** 0.5
                if L < 1e-6:
                    continue
                vis, _ = V.facing(dy / L, -dx / L)
                if vis:
                    quad = [V.P(p[0], p[1]), V.P(q[0], q[1]), V.P(q[0], q[1], h), V.P(p[0], p[1], h)]
                    polys.append(quad)
                    walls.append((quad, p, (dx, dy)))
            rf = [V.P(x, y, h) for x, y in P]
            o["roof"], o["walls"], o["polys"] = rf, walls, polys + [rf]
        else:
            B = V.P(o["x"], o["y"])
            r = o["D"] / 2.0
            ht = max(1.5, 0.45 * o["D"])
            o["cen"], o["rad"] = (B[0], B[1] + V.kz * ht), k * r
            a = o["rad"]
            o["polys"] = [[(o["cen"][0] + a * m_.cos(t), o["cen"][1] + a * m_.sin(t))
                           for t in [j * m_.pi / 8.0 for j in range(16)]]]
        xs = [q[0] for R in o["polys"] for q in R]
        ys = [q[1] for R in o["polys"] for q in R]
        o["bb"] = (min(xs), min(ys), max(xs), max(ys))

    def inside(o, X, Y):
        if "P" not in o:
            return (X - o["cen"][0]) ** 2 + (Y - o["cen"][1]) ** 2 <= o["rad"] ** 2
        return any(_pin(X, Y, R) for R in o["polys"])

    def hit(o, X, Y):                                    # plan depth where the ray through (X, Y) meets o
        if "P" not in o:
            if (X - o["cen"][0]) ** 2 + (Y - o["cen"][1]) ** 2 > o["rad"] ** 2:
                return None
            return V.depth(o["x"], o["y"]) - o["D"] / 2.0
        best = None
        if _pin(X, Y, o["roof"]):
            zz = 0.0
            for _ in range(5):
                A_, B_ = X - V.c0, Y - V.oy - V.kz * (zz + o["h"])
                x = (A_ * V.c1 * V.s - V.c2 * B_) / V.inv
                y = (V.c2 * V.s * A_ + V.c1 * B_) / V.inv
                zz = V.z(x, y)
            best = V.depth(x, y)
        for quad, p, (dx, dy) in o["walls"]:
            if _pin(X, Y, quad):
                den = V.c1 * dx + V.c2 * dy
                if abs(den) < 1e-12:
                    continue
                t = max(0.0, min(1.0, (X - V.c0 - V.c1 * p[0] - V.c2 * p[1]) / den))
                d_ = V.depth(p[0] + t * dx, p[1] + t * dy)
                best = d_ if best is None else min(best, d_)
        return best

    def probes(o):
        if "P" not in o:
            c_, a = o["cen"], o["rad"]
            return [c_] + [(c_[0] + 0.7 * a * m_.cos(t), c_[1] + 0.7 * a * m_.sin(t)) for t in (0.4, 2.0, 3.6, 5.2)]
        out = []
        for R in o["polys"]:
            cx, cy = sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R)
            out.append((cx, cy))
            out += [(q[0] + 0.08 * (cx - q[0]), q[1] + 0.08 * (cy - q[1])) for q in R]
        return out

    def lat_dep(x, y):                                   # v5.1: plan sideways / depth (m) along the view
        return (V.c1 * x + V.c2 * y) / k, (-V.c2 * x + V.c1 * y) / k

    for o in objs:
        if "P" in o:
            o["LD"] = [lat_dep(x, y) for x, y in o["P"]]
            us = [q[0] for q in o["LD"]]
            o["lat"] = (min(us), max(us))
        else:
            u0, d0 = lat_dep(o["x"], o["y"])
            r = o["D"] / 2.0
            o["LD"], o["lat"] = (u0, d0, r), (u0 - r, u0 + r)

    def front(o, u):                                     # the first depth on the line of sight at sideways u
        if "P" not in o:
            u0, d0, r = o["LD"]
            w = r * r - (u - u0) ** 2
            return None if w < 0 else d0 - w ** 0.5
        best, R = None, o["LD"]
        for ii in range(len(R)):
            (u1, d1), (u2, d2) = R[ii - 1], R[ii]
            if (u1 <= u) != (u2 <= u):
                d_ = d1 + (u - u1) * (d2 - d1) / (u2 - u1)
                best = d_ if best is None or d_ < best else best
        return best

    cell = 6.0
    grid = {}
    for i, o in enumerate(objs):
        b = o["bb"]
        for gi in range(int(b[0] // cell), int(b[2] // cell) + 1):
            for gj in range(int(b[1] // cell), int(b[3] // cell) + 1):
                grid.setdefault((gi, gj), []).append(i)
    seen, after = set(), [[] for _ in objs]
    indeg = [0] * len(objs)
    n_pairs = n_edges = 0
    for ids in grid.values():
        for ai in range(len(ids)):
            for bi in range(ai + 1, len(ids)):
                i, j = ids[ai], ids[bi]
                if i > j:
                    i, j = j, i
                if (i, j) in seen:
                    continue
                seen.add((i, j))
                A, B = objs[i], objs[j]
                a, b = A["bb"], B["bb"]
                if a[2] < b[0] or b[2] < a[0] or a[3] < b[1] or b[3] < a[1]:
                    continue
                n_pairs += 1
                # v5.1: decided in PLAN, exactly: the drawing's X is the plan's sideways coordinate, so two upright
                # bodies can only overlap where their sideways spans share a strip, and on each line of sight in that
                # strip the one whose front edge comes first (smaller depth) hides the other, whatever the heights
                lo, hi = max(A["lat"][0], B["lat"][0]), min(A["lat"][1], B["lat"][1])
                if hi - lo <= 1e-6:
                    continue
                vote = 0
                for f_ in (0.1, 0.3, 0.5, 0.7, 0.9):
                    u = lo + f_ * (hi - lo)
                    da, db = front(A, u), front(B, u)
                    if da is None or db is None or abs(da - db) < 1e-6:
                        continue
                    vote += 1 if da < db else -1
                if vote == 0:
                    continue
                near, far = (i, j) if vote > 0 else (j, i)
                after[far].append(near)
                indeg[near] += 1
                n_edges += 1
    heap = [(-o["d"], i) for i, o in enumerate(objs) if indeg[i] == 0]
    heapq.heapify(heap)
    done, order, n_cyc = [False] * len(objs), [], 0
    while len(order) < len(objs):
        if not heap:                                     # a cycle: the farthest one left goes first
            i = max((i for i in range(len(objs)) if not done[i]), key=lambda i: objs[i]["d"])
            n_cyc += 1
        else:
            _, i = heapq.heappop(heap)
            if done[i]:
                continue
        done[i] = True
        order.append(i)
        for n_ in after[i]:
            indeg[n_] -= 1
            if indeg[n_] == 0 and not done[n_]:
                heapq.heappush(heap, (-objs[n_]["d"], n_))
    log.append(u"drawing order (v5.1, plan lines of sight): %d objects, %d overlapping pairs, %d settled by their 3D form, "
               u"%d cycle(s) broken by depth" % (len(objs), n_pairs, n_edges, n_cyc))
    return [objs[i] for i in order]


# ================================================================ AXO_LIB_END (v3.0: slide 2's spine execs everything above)
# ---------------------------------------------------------------- v3.0: trees from the asset cutouts, stood up in 3D
# Aras 15 Nov 13:39 UTC: "change the trees on axonometric drawing use it from assets and make those 2d representations 3d
# with rotating or raying or something". Each tree is the asset library's own cutout (Data/cutouts, the sections'
# trees), read live: its PNG decoded here (pure Python, no add-ons), its silhouette and its darkest third traced on a
# coarse grid (TREE_ROWS rows; a tree is about 1 mm tall on the page) in the cutout's own colours, cached in
# cached/bergama_page01_axo/tree_traces.json (re-traced when a PNG changes). In the drawing each tree stands as TWO
# copies crossed at 90 degrees (a billboard cross, each turned 45 degrees off the view), the back halves in the
# cutout's lighter depth tone (_d1), the front halves in its own colours, with a ground shadow: the 2D cutout reads as
# a volume, as the section trees and the axo share one asset.
TREE_ROWS = 16                     # grid rows a cutout is traced on
TREE_SET = ("plane_1", "plane_2", "plane_3", "plane_4", "plane_5", "plane_6", "ash_1", "ash_2", "ash_3", "ash_4")
TREE_SP = 8.0                      # m: one tree every TREE_SP m (hex grid) in a 2023 canopy patch (a drawing rule)
TREE_MIN_A = 10.0                  # m2: canopy patches smaller than this are left out (shrubs, image noise)
TREE_D = (3.5, 8.5)                # m: crown width drawn, from the patch area per tree, clamped
SHADOW = "D3D3D0"                  # v3.4: grey (was beige DDD9CC, Aras 14:49 UTC)
TRUNK = "6B5A48"                    # v3.2: the tree trunk (drawing value)                  # the tree's ground shadow (drawing value)
PARK_C = "C2CCB3"                  # parks and green ground (the booklet legend's colour)
WALL_C = "84573E"                  # historic wall lines (the booklet legend's colour)
PARK_KINDS = ("park", "green", "wood", "cemetery")
TREE_KEY = "6E7A4C"                 # the legend dot for trees (drawing value)


def _png_rgba(path):
    """an 8-bit RGBA / RGB PNG (not interlaced) as (w, h, rows of bytes, bytes per pixel), pure Python"""
    import struct, zlib
    with open(path, "rb") as f:
        b = f.read()
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(u"not a PNG")
    i, idat, w = 8, [], None
    while i < len(b):
        n, typ = struct.unpack(">I4s", b[i:i + 8])
        d = b[i + 8:i + 8 + n]
        if typ == b"IHDR":
            w, h, bd, ct, _, _, il = struct.unpack(">IIBBBBB", d)
            if bd != 8 or ct not in (2, 6) or il:
                raise ValueError(u"PNG type %d/%d/%d not read" % (bd, ct, il))
            bpp = 4 if ct == 6 else 3
        elif typ == b"IDAT":
            idat.append(d)
        i += 12 + n
    raw = zlib.decompress(b"".join(idat))
    st = w * bpp
    rows, prev = [], bytearray(st)
    p = 0
    for _ in range(h):
        ft = raw[p]
        line = bytearray(raw[p + 1:p + 1 + st])
        p += 1 + st
        if ft == 1:
            for x in range(bpp, st):
                line[x] = (line[x] + line[x - bpp]) & 255
        elif ft == 2:
            for x in range(st):
                line[x] = (line[x] + prev[x]) & 255
        elif ft == 3:
            for x in range(st):
                a = line[x - bpp] if x >= bpp else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif ft == 4:
            for x in range(st):
                a = line[x - bpp] if x >= bpp else 0
                c_ = prev[x - bpp] if x >= bpp else 0
                b_ = prev[x]
                pa, pb, pc = abs(b_ - c_), abs(a - c_), abs(a + b_ - 2 * c_)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b_ if pb <= pc else c_)) & 255
        rows.append(line)
        prev = line
    return w, h, rows, bpp


def _cells_rings(S):
    """the outline rings (grid corners, region on the left) of a set S of (col, row) cells"""
    E = {}
    for (i, j) in S:
        for a, b, nb in (((i, j + 1), (i + 1, j + 1), (i, j + 1)), ((i + 1, j + 1), (i + 1, j), (i + 1, j)),
                         ((i + 1, j), (i, j), (i, j - 1)), ((i, j), (i, j + 1), (i - 1, j))):
            if nb not in S:
                E.setdefault(a, []).append(b)
    rings = []
    while E:
        a = next(iter(E))
        R = [a]
        cur = a
        while True:
            nx_ = E[cur].pop()
            if not E[cur]:
                del E[cur]
            if nx_ == a:
                break
            R.append(nx_)
            cur = nx_
            if cur not in E:
                break
        out = [R[k] for k in range(len(R)) if not (
            (R[k - 1][0] == R[k][0] == R[(k + 1) % len(R)][0]) or (R[k - 1][1] == R[k][1] == R[(k + 1) % len(R)][1]))]
        if len(out) >= 3:
            rings.append(out)
    return rings


def _trace_png(path):
    """a cutout traced: {"wr": width / height, "sil": (colour, rings), "dark": (colour, rings)}; rings in (u, v),
    u across from the trunk and v up from the foot, both in tree heights"""
    w, h, rows, bpp = _png_rgba(path)
    cell = h / float(TREE_ROWS)
    nc = int(w / cell + 0.999)
    stp = max(1, int(cell / 4))
    cells = {}
    for j in range(TREE_ROWS):
        for i in range(nc):
            n = cov = r = g = b = 0
            for y in range(int(j * cell), min(h, int((j + 1) * cell)), stp):
                L = rows[y]
                for x in range(int(i * cell), min(w, int((i + 1) * cell)), stp):
                    n += 1
                    if bpp == 3 or L[x * 4 + 3] > 128:
                        k = x * bpp
                        cov += 1
                        r += L[k]
                        g += L[k + 1]
                        b += L[k + 2]
            if n and cov >= 0.45 * n:
                cells[(i, TREE_ROWS - 1 - j)] = (r / cov, g / cov, b / cov)
    if not cells:
        raise ValueError(u"no opaque cells")
    foot = [i for (i, j) in cells if j <= 1] or [i for (i, j) in cells]
    tx = (sum(foot) / float(len(foot)) + 0.5) * cell
    lum = lambda c: 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    ls = sorted(lum(c) for c in cells.values())
    t1 = ls[len(ls) // 3]
    hexc = lambda cs: u"%02X%02X%02X" % tuple(int(sum(c[k] for c in cs) / len(cs)) for k in range(3))
    dk = dict((q, c) for q, c in cells.items() if lum(c) <= t1)
    uv = lambda R: [((q[0] * cell - tx) / h, q[1] * cell / h) for q in R]
    return {"wr": w / float(h), "sil": (hexc(list(cells.values())), [uv(R) for R in _cells_rings(set(cells))]),
            "dark": (hexc(list(dk.values())) if dk else None, [uv(R) for R in _cells_rings(set(dk))])}


def tree_traces(log):
    """{name: {"main": trace, "d1": trace}} for TREE_SET, from Data/cutouts (cached until a PNG changes)"""
    src = os.path.join(BERGAMA_ROOT, "Data", "cutouts")
    cp = os.path.join(os.path.dirname(CACHE), "tree_traces.json")
    try:
        with open(cp, encoding="utf-8") as f:
            T = json.load(f)
    except Exception:
        T = {}
    out, made = {}, 0
    for nm in TREE_SET:
        for key, fn in (("main", nm + ".png"), ("d1", nm + "_d1.png")):
            p = os.path.join(src, fn)
            if not os.path.isfile(p):
                continue
            mt = os.path.getmtime(p)
            e = T.get(fn)
            if not e or e.get("mtime") != mt or e.get("rows") != TREE_ROWS:
                try:
                    e = dict(_trace_png(p), mtime=mt, rows=TREE_ROWS)
                except Exception as ex:
                    log.append(u"FLAG trees: %s not traced (%s: %s)" % (fn, type(ex).__name__, ex))
                    continue
                T[fn] = e
                made += 1
            out.setdefault(nm, {})[key] = e
    out = dict((k, v) for k, v in out.items() if "main" in v)
    for v in out.values():
        v.setdefault("d1", v["main"])
    if made:
        try:
            os.makedirs(os.path.dirname(cp), exist_ok=True)
            with open(cp, "w", encoding="utf-8") as f:
                json.dump(T, f)
        except Exception as ex:
            log.append(u"trees: traces not cached (%s)" % ex)
    log.append(u"trees: %d asset cutouts from %s (%d traced this press, the rest from %s)" % (
        len(out), src, made, cp))
    if not out:
        log.append(u"FLAG trees: no tree cutouts found in %s: no trees drawn" % src)
    return out


# v3.4 (Aras 14:48 UTC "these trees are awful please fix them to the trees that we have at assets and make them 3dize"):
# each tree's crown is one of Aras's own painted tree symbols (masterp_agac.svg, traced 6 Nov into stacked tone bands;
# read live from Data/bergama_b19_plan_data.py TREE_EMBED, the same library the masterplan draws), stood up as the crown
# seen from the axo's camera (a painted round crown reads as a lit volume), on a trunk, with a grey ground shadow.
TREE_SYMS = ("S047", "S027", "S045", "S056", "S081", "S014", "S007", "S022", "S086", "S046")   # plane, ash, default
TREE_BANDS = 4                     # tone bands kept per symbol (silhouette ... darkest), for speed
TREE_PTS = 40                      # points per ring at most (a crown is 1-3 mm on the page)


def tree_syms(log):
    """{id: [(fill, rings in unit -1..1, y up)]} for TREE_SYMS, decoded from the B19 data file's TREE_EMBED"""
    import zlib, base64
    p = os.path.join(BERGAMA_ROOT, "Data", "bergama_b19_plan_data.py")
    try:
        L = open(p, encoding="utf-8").read().split("\n")
        i = next(i for i, l in enumerate(L) if l.startswith("TREE_EMBED = ("))
        j = next(j for j in range(i + 1, len(L)) if L[j].startswith(")"))
        b = "".join(l.strip().strip(",").strip('"') for l in L[i + 1:j])
        J = json.loads(zlib.decompress(base64.b64decode(b)).decode("utf-8"))
    except Exception as ex:
        log.append(u"FLAG trees: the painted tree symbols not read from %s (%s: %s): no trees drawn" % (
            p, type(ex).__name__, ex))
        return {}
    by = dict((s["id"], s) for s in J["symbols"])
    out = {}
    for sid in TREE_SYMS:
        s = by.get(sid)
        if not s:
            continue
        bands = s["bands"]
        pick = [bands[int(round(t * (len(bands) - 1) / max(1, TREE_BANDS - 1)))] for t in range(TREE_BANDS)] \
            if len(bands) > TREE_BANDS else bands
        bl = []
        for bd in pick:
            rr = []
            for R in bd["rings"]:
                if len(R) < 3:
                    continue
                st = max(1, int(len(R) / TREE_PTS + 0.999))
                Q = R[::st]
                if len(Q) >= 3:
                    rr.append([tuple(q) for q in Q])
            if rr:
                bl.append((bd["fill"].lstrip("#").upper(), rr))
        if bl:
            out[sid] = bl
    log.append(u"trees: %d of Aras's painted tree symbols (%s) from %s, %d tone bands each, rings at most %d points" % (
        len(out), u", ".join(sorted(out)), p, TREE_BANDS, TREE_PTS))
    return out


def _tree_shapes(V, x, y, D, sym, anchor):
    """one tree: grey ground shadow, trunk, then the painted crown's tone bands, the crown D wide at its height"""
    m_ = V.m
    k = V.k
    e = (V.c1 / k, V.c2 / k)
    f = (-V.c2 / k, V.c1 / k)
    sv = lambda d: (V.c1 * d[0] + V.c2 * d[1], V.s * (-V.c2 * d[0] + V.c1 * d[1]))
    se, sf = sv(e), sv(f)
    r = D / 2.0
    ht = max(1.5, 0.45 * D)                              # trunk up to the crown's centre
    B = V.P(x, y)
    C = (B[0], B[1] + V.kz * ht)
    sh = lambda rings, fi: {"t": "poly", "rings": rings, "fill": fi, "stroke": None, "width_pt": 0.0,
                            "dash_pt": None, "opacity": None, "grp": u"trees/mb", "anchor": anchor, "bld": None}
    rs = r * 0.9
    out = [sh([[(B[0] + rs * (m_.cos(t) * se[0] + m_.sin(t) * sf[0]) + 0.3 * rs * se[0],
                 B[1] + rs * (m_.cos(t) * se[1] + m_.sin(t) * sf[1])) for t in
                [i * m_.pi / 10.0 for i in range(20)]]], SHADOW)]
    tw = max(0.05, k * 0.15)
    out.append(sh([[(B[0] - tw, B[1]), (B[0] + tw, B[1]), (B[0] + tw, C[1]), (B[0] - tw, C[1])]], TRUNK))
    a = k * r
    for fi, rings in sym:
        out.append(sh([[(C[0] + u * a, C[1] + v * a) for u, v in R] for R in rings], fi))
    return out


def rebuild(c, G, log):
    """c (the booklet p03 drawing, booklet mm) with its roads and buildings redrawn from MapBase"""
    import math as m_
    S = c["shapes"]
    slab = next((i for i, s in enumerate(S[:6]) if s["t"] == "poly" and s.get("fill") == SLAB_TOP), None)
    if slab is None:
        log.append(u"FLAG rebuild: the booklet slab not found: roads and buildings kept as the booklet drew them")
        return c, None
    corners = [tuple(q[:2]) for q in G["pc_site_map"](1000.0, log).ring]
    V = AxoView([tuple(q) for q in S[slab]["rings"][0]], corners, log)
    ns_, C = G["pc_mb_data"](log)
    # ---- the site_alan window as half-planes (inside >= 0)
    cx_, cy_ = sum(q[0] for q in corners) / 4.0, sum(q[1] for q in corners) / 4.0
    H = []
    for i in range(4):
        p, q = corners[i], corners[(i + 1) % 4]
        a, b = -(q[1] - p[1]), q[0] - p[0]
        c0 = -(a * p[0] + b * p[1])
        if a * cx_ + b * cy_ + c0 < 0:
            a, b, c0 = -a, -b, -c0
        nn = m_.hypot(a, b)
        H.append((a / nn, b / nn, c0 / nn))
    inside = lambda x, y: all(a * x + b * y + c0 >= 0 for a, b, c0 in H)

    # ---- the booklet's buildings: halo, walls, roof per building; class, height, ground footprint (screen)
    USE_ROOF = dict((u[1][0], (u[0], u[1])) for u in USE)
    USE_ROOF[CTX[0]] = ("context", CTX)
    isb = lambda s: (s.get("grp") or u"").startswith(u"buildings")
    first = next(i for i in range(slab + 1, len(S)) if isb(S[i]))
    last = max(i for i in range(len(S)) if isb(S[i]))
    old, cur = [], []
    runs, run = [], []                                   # tree / other runs between buildings: (after building n, shapes)
    for i in range(first, last + 1):
        s = S[i]
        if not isb(s):
            run.append(s)
            continue
        if run:
            runs.append((len(old), run))
            run = []
        cur.append(s)
        if s["t"] == "poly" and s.get("fill") in USE_ROOF and s.get("fill") == s.get("stroke") or \
                s.get("fill") == CTX[0] and s.get("stroke") == CTX[3]:
            old.append(cur)
            cur = []
    tail = S[last + 1:]
    for b in old:
        roof = b[-1]
        cls = USE_ROOF.get(roof.get("fill"), ("context", CTX))[0]
        hs = [(w["rings"][0][3][1] - w["rings"][0][0][1]) / V.kz for w in b[:-1]
              if w.get("fill") is not None and len(w["rings"][0]) == 4]
        h = max(hs) if hs else None
        R = roof["rings"][0]
        foot = [(q[0], q[1] - V.kz * (h or 0.0)) for q in R]
        gx, gy = sum(q[0] for q in foot) / len(foot), sum(q[1] for q in foot) / len(foot)
        x, y = V.back(gx, gy)
        b[:] = [dict(cls=cls, h=h, foot=foot, bb=(min(q[0] for q in foot), min(q[1] for q in foot),
                                                   max(q[0] for q in foot), max(q[1] for q in foot)),
                     d=V.depth(x, y), n=0)]
    old = [b[0] for b in old]
    grid = {}
    for k_, b in enumerate(old):
        for gi in range(int(b["bb"][0] // 2), int(b["bb"][2] // 2) + 1):
            for gj in range(int(b["bb"][1] // 2), int(b["bb"][3] // 2) + 1):
                grid.setdefault((gi, gj), []).append(k_)

    def match(X, Y):
        for dy in (0.0, 0.25, -0.25, 0.5, -0.5):
            for k_ in grid.get((int(X // 2), int((Y + dy) // 2)), ()):
                b = old[k_]
                if b["bb"][0] <= X <= b["bb"][2] and b["bb"][1] <= Y + dy <= b["bb"][3] and _pip(X, Y + dy, b["foot"]):
                    return k_
        return None

    # ---- MapBase buildings inside site_alan: class + height from the booklet building they stand in
    stor = dict(STOREY)
    new, n_fl, n_bk, n_def, n_new = [], 0, 0, 0, 0
    cnt = {}
    foots, d3_blds = [], []
    for bi, (row, x_) in enumerate(zip(C["bld"], C["bld_x"])):
        P = [tuple(q) for q in row[0]]
        if len(P) > 1 and P[0] == P[-1]:
            P = P[:-1]
        if len(P) < 3:
            continue
        ar = sum(P[i - 1][0] * P[i][1] - P[i][0] * P[i - 1][1] for i in range(len(P))) / 2.0
        gx = sum(q[0] for q in P) / len(P)
        gy = sum(q[1] for q in P) / len(P)
        if not inside(gx, gy) or abs(ar) < 4.0:
            continue
        if ar < 0:
            P = P[::-1]
        P = _clip(P, H)                                  # v2.8: cut to site_alan, nothing hangs over the slab
        if len(P) < 3:
            continue
        X, Y = V.P(gx, gy)
        k_ = match(X, Y)
        fab = row[1]
        if k_ is not None:
            old[k_]["n"] += 1
            cls = old[k_]["cls"]
        else:
            n_new += 1
            cls = "ruins" if fab == "monument" else "sacred" if fab == "sacred" else "context"
        fl = int(x_[0] or 0)
        if fl > 0:
            h = fl * stor.get(cls, 3.0)
            n_fl += 1
        elif k_ is not None and old[k_]["h"]:
            h = old[k_]["h"]
            n_bk += 1
        else:
            h = 3.0
            n_def += 1
        cnt[cls] = cnt.get(cls, 0) + 1
        cols = dict((u[0], u[1]) for u in USE).get(cls, CTX)
        foots.append(P)
        d3_blds.append((P, h, cols))
        bs_ = [dict(sh_, anchor=(gx, gy), bld=bi) for sh_ in _bld_shapes(V, P, h, cols, cls != "context")]
        bs_[0] = dict(bs_[0], foot=P, h=h, cls=cls, cols=cols)   # v3.2: so slide 2 can re-cut it at a node frame
        new.append({"d": V.depth(gx, gy), "sh": bs_, "P": P, "h": h})   # v5.0: its 3D form for the order
    gone = [b for b in old if b["n"] == 0]
    merged = [b for b in old if b["n"] >= 2]
    log.append(u"buildings: %d from MapBase %s in site_alan (booklet had %d): class from the booklet building they "
               u"stand in for %d, %d not in the booklet (class from MapBase: ruins / sacred, else context)" % (
                   len(new), C.get("version"), len(old), len(new) - n_new, n_new))
    log.append(u"buildings: heights from surveyed floors %d (x 3.0 m; civic 3.5, sacred 5.0, industry 4.5), from the "
               u"booklet %d, not recorded (one floor, 3.0 m) %d" % (n_fl, n_bk, n_def))
    log.append(u"buildings: %d booklet buildings stand on no MapBase footprint (dropped), %d booklet blocks held "
               u"2+ MapBase buildings (now drawn one by one)" % (len(gone), len(merged)))
    log.append(u"buildings per class: %s" % u", ".join(u"%s %d" % kv for kv in sorted(cnt.items())))

    # ---- v3.0 (Aras 13:40-13:41 UTC "river drawing in axonometric is fucked fix it according to the basemap", "make
    # axonometric get produced by basemap"): the slab, ground, water, streets, walls, buildings and trees are ALL drawn
    # from the MapBase cache (and the 2023 canopy patches MapBase reads), draped on the terrain; of the booklet drawing
    # only the view (fitted to its slab), the use class each building stands in and the numbered markers stay.
    S_ = ns_["MB_STYLE"]
    WATER, WATER_LINE = S_["water"], S_["water_line"]
    on_edge = lambda p: any(abs(a * p[0] + b * p[1] + c0) < 0.05 for a, b, c0 in H)

    def dens(Q, step=5.0, closed=True):
        D = [] if closed else [Q[0]]
        rng = range(len(Q)) if closed else range(1, len(Q))
        for i in rng:
            p, q = Q[i - 1], Q[i]
            L = m_.hypot(q[0] - p[0], q[1] - p[1])
            n = max(1, int(L / step))
            D += [(p[0] + (q[0] - p[0]) * t / n, p[1] + (q[1] - p[1]) * t / n) for t in range(1, n + 1)]
        return D

    def region(rings_in, fill, edge, w_pt, grp, one=True):
        """closed plan rings cut to site_alan, draped: one fill (even-odd) or one per ring; edges not along the cut"""
        rr = []
        for R in rings_in:
            Q = _clip([tuple(q[:2]) for q in R], H)
            if len(Q) >= 3:
                D = dens(Q)
                rr.append(([V.P(x, y) for x, y in D], D))
        if not rr:
            return [], 0
        mk = lambda rings, a: {"t": "poly", "rings": rings, "fill": fill, "stroke": None, "width_pt": 0.0,
                               "dash_pt": None, "opacity": None, "grp": grp, "anchor": a, "bld": None}
        out = [mk([r[0] for r in rr], rr[0][1][0])] if one else [mk([r[0]], r[1][0]) for r in rr]
        if edge:
            for scr, D in rr:
                cur_ = []
                for i in range(len(D)):
                    p, q = D[i - 1], D[i]
                    if on_edge(p) and on_edge(q):
                        if len(cur_) > 1:
                            out.append({"t": "line", "pts": cur_, "fill": None, "stroke": edge, "width_pt": w_pt,
                                        "dash_pt": None, "opacity": None, "grp": grp, "anchor": D[0], "bld": None})
                        cur_ = []
                        continue
                    if not cur_:
                        cur_ = [scr[i - 1]]
                    cur_.append(scr[i])
                if len(cur_) > 1:
                    out.append({"t": "line", "pts": cur_, "fill": None, "stroke": edge, "width_pt": w_pt,
                                "dash_pt": None, "opacity": None, "grp": grp, "anchor": D[0], "bld": None})
        return out, len(rr)

    # the slab: its top = site_alan draped, its two cut faces toward the viewer (the band is drawn in main)
    E = dens([tuple(q) for q in corners], 15.0)
    slab_top = {"t": "poly", "rings": [[V.P(x, y) for x, y in E]], "fill": SLAB_TOP, "stroke": None, "width_pt": 0.0,
                "dash_pt": None, "opacity": None, "grp": u"slab/mb", "anchor": corners[0], "bld": None}
    sides = []
    for i in range(4):
        p, q = corners[i], corners[(i + 1) % 4]
        L = m_.hypot(q[0] - p[0], q[1] - p[1])
        nx, ny = (q[1] - p[1]) / L, -(q[0] - p[0]) / L
        if (p[0] + q[0]) / 2.0 * nx + (p[1] + q[1]) / 2.0 * ny < cx_ * nx + cy_ * ny:
            nx, ny = -nx, -ny
        vis, lt = V.facing(nx, ny)
        if vis:
            run = [V.P(x, y) for x, y in dens([p, q], 15.0, False)]
            sides.append({"t": "poly", "rings": [run + [(run[-1][0], run[-1][1] - 3.0), (run[0][0], run[0][1] - 3.0)]],
                          "fill": "B0AC9C" if lt else "847E75", "stroke": None, "width_pt": 0.0, "dash_pt": None,
                          "opacity": None, "grp": u"slab/mb", "anchor": p, "bld": None})
    if len(sides) != 2:
        log.append(u"FLAG slab: %d cut faces face the viewer (2 expected)" % len(sides))

    # parks and green ground: MapBase parks + its OSM areas of park / green / wood / cemetery
    pr = list(C["polys"].get("parks", [])) + [a[0] for a in C.get("areas", []) if len(a) > 1 and a[1] in PARK_KINDS]
    parks, n_pk = region(pr, PARK_C, None, 0.0, u"plants/mb", one=False)
    # the water: MapBase's river (the Selinos and its banks, as every base map draws it)
    riv = [[tuple(q[:2]) for q in R] for R in C["polys"].get("river", [])]
    water, n_wr = region(riv, WATER, WATER_LINE, 0.45, u"water/mb")
    rbb = [(min(q[0] for q in R), min(q[1] for q in R), max(q[0] for q in R), max(q[1] for q in R)) for R in riv]
    in_water = lambda x, y: sum(1 for R, b in zip(riv, rbb) if b[0] <= x <= b[2] and b[1] <= y <= b[3] and
                                _pip(x, y, R)) % 2 == 1
    # historic walls: MapBase's heritage walls and city walls, draped, cut to site_alan
    walls, n_wl, wall_runs = [], 0, []
    for P in [w_[1] for w_ in C["lines"].get("heritage_walls", [])] + list(C.get("osm_citywalls", [])):
        P = [tuple(q[:2]) for q in P]   # lines rows: (closed, points)
        if len(P) < 2:
            continue
        cur_, pl_ = [], []
        for q in dens(P, 2.0, False) + [None]:
            if q is not None and inside(q[0], q[1]):
                cur_.append(V.P(q[0], q[1], 0.3))
                pl_.append(q)
                continue
            if len(pl_) > 1:
                wall_runs.append(pl_)
            pl_ = []
            if len(cur_) > 1:
                walls.append({"t": "line", "pts": cur_, "fill": None, "stroke": WALL_C, "width_pt": 0.6,
                              "dash_pt": (4.5, 2.5), "opacity": None, "grp": u"heritage/mb", "anchor": P[0],
                              "bld": None})
                n_wl += 1
            cur_ = []
    log.append(u"ground: slab from site_alan, %d park / green area(s), river %d ring(s), %d historic wall piece(s), "
               u"all from MapBase %s" % (n_pk, n_wr, n_wl, C.get("version")))

    # ---- trees: the 2023 canopy patches MapBase reads (C["veg"]["trees"]) and its OSM trees; never in the water
    trs = tree_syms(log)
    names = sorted(trs)
    bgrid = {}
    for k_, P in enumerate(foots):
        for gi in range(int(min(q[0] for q in P) // 20), int(max(q[0] for q in P) // 20) + 1):
            for gj in range(int(min(q[1] for q in P) // 20), int(max(q[1] for q in P) // 20) + 1):
                bgrid.setdefault((gi, gj), []).append(k_)
    in_bld = lambda x, y: any(_pip(x, y, foots[k_]) for k_ in bgrid.get((int(x // 20), int(y // 20)), ()))
    pts, n_small, n_wat, n_bl, n_st = [], 0, 0, 0, 0
    sn = [[tuple(q[:2]) for q in R] for R in C["polys"].get("street_net", []) if len(R) >= 3]   # v3.4: no tree on a street
    sgrid = {}
    for k_, R in enumerate(sn):
        for gi in range(int(min(q[0] for q in R) // 50), int(max(q[0] for q in R) // 50) + 1):
            for gj in range(int(min(q[1] for q in R) // 50), int(max(q[1] for q in R) // 50) + 1):
                sgrid.setdefault((gi, gj), []).append(k_)
    on_street = lambda x, y: sum(1 for k_ in sgrid.get((int(x // 50), int(y // 50)), ()) if _pip(x, y, sn[k_])) % 2 == 1
    patches = (C.get("veg") or {}).get("trees", [])
    if not patches:
        log.append(u"FLAG trees: MapBase carries no 2023 canopy patches (Data/veg2023.json): only OSM trees drawn")
    ys_ = TREE_SP * 0.8660254
    for R in patches:
        R = [tuple(q[:2]) for q in R]
        x0, y0 = min(q[0] for q in R), min(q[1] for q in R)
        x1, y1 = max(q[0] for q in R), max(q[1] for q in R)
        if not (inside(x0, y0) or inside(x1, y1) or inside(x0, y1) or inside(x1, y0)):
            continue
        a = abs(sum(R[i - 1][0] * R[i][1] - R[i][0] * R[i - 1][1] for i in range(len(R)))) / 2.0
        if a < TREE_MIN_A:
            n_small += 1
            continue
        got = []
        for j in range(int(y0 // ys_), int(y1 // ys_) + 1):
            off = TREE_SP / 2.0 if j % 2 else 0.0
            for i in range(int((x0 - off) // TREE_SP), int((x1 - off) // TREE_SP) + 1):
                x, y = i * TREE_SP + off, j * ys_
                if x0 <= x <= x1 and y0 <= y <= y1 and _pip(x, y, R):
                    got.append((x, y))
        if not got:
            got = [(sum(q[0] for q in R) / len(R), sum(q[1] for q in R) / len(R))]
        D = 2.0 * (a / len(got) / m_.pi) ** 0.5
        for x, y in got:
            pts.append((x, y, min(TREE_D[1], max(TREE_D[0], D))))
    for q in C.get("trees", []):
        if not any(abs(q[0] - p[0]) < TREE_SP / 2 and abs(q[1] - p[1]) < TREE_SP / 2 for p in pts):
            pts.append((q[0], q[1], 6.0))
    trees, d3_trees = [], []
    for x, y, D in pts:
        if not inside(x, y):
            continue
        if in_water(x, y):
            n_wat += 1
            continue
        if in_bld(x, y):
            n_bl += 1
            continue
        if on_street(x, y):
            n_st += 1
            continue
        if names:
            tr = trs[names[(int(x * 7.0) + int(y * 13.0)) % len(names)]]
            trees.append({"d": V.depth(x, y), "sh": _tree_shapes(V, x, y, D, tr, (x, y)), "x": x, "y": y, "D": D})
            bc = [b_[0] for b_ in tr]
            d3_trees.append((x, y, D, (bc[1 % len(bc)], bc[min(2, len(bc) - 1)], bc[-1])))
    cnt["_trees"] = len(trees)
    log.append(u"trees: %d drawn (one every %.0f m in the 2023 canopy patches over %.0f m2, crowns %.1f-%.1f m; OSM "
               u"trees where no patch); left out: %d in the river, %d on a building roof, %d on a street, %d patches under %.0f m2" % (
                   len(trees), TREE_SP, TREE_MIN_A, TREE_D[0], TREE_D[1], n_wat, n_bl, n_st, n_small, TREE_MIN_A))

    objs = _depth_order(V, new + trees, log)             # v5.0: settled by the 3D form of each pair
    # v5.1 (run 25, Aras 18:59 UTC "foreground background is still fucked"): the PDF writer draws one marked block per
    # layer, so trees (layer trees) and buildings (layer buildings) were drawn as two piles and the 3D order was lost:
    # every tree shadow now lies on the ground first (one layer), then buildings and tree crowns in their 3D order on
    # ONE layer (axo_body)
    body = [dict(s, lay=u"shadows") for o in objs if "x" in o for s in o["sh"][:1]] + \
        [dict(s, lay=u"body") for o in objs for s in (o["sh"][1:] if "x" in o else o["sh"])]

    # ---- the streets: MapBase's one closed street region, cut to site_alan, draped on the terrain
    road, n_rd = region(C["polys"].get("street_net", []), ROAD[0], ROAD[1], ROAD[2], u"roads/mb")
    log.append(u"streets: MapBase's street region (%d ring(s) in site_alan, one fill, edges not drawn along the frame "
               u"cut)" % n_rd)
    labels = [dict(s, anchor=None, bld=None) for s in S if (s.get("grp") or u"").startswith(u"labels")]
    nold = len(S) - len(labels)
    log.append(u"booklet drawing: %d shapes left out (its slab, ground, water, trees, people, roads, buildings); its %d "
               u"numbered marker shape(s) kept" % (nold, len(labels)))
    # ---- v4.0: the same layers for the 3D model (plan rings / runs in survey m, colours of this drawing)
    def clipped(rings):
        return [Q for Q in (_clip([tuple(q[:2]) for q in R], H) for R in rings) if len(Q) >= 3]

    def plan_edges(rings):
        out = []
        for Q in rings:
            D = dens(Q)
            cur_ = []
            for i in range(len(D)):
                p, q = D[i - 1], D[i]
                if on_edge(p) and on_edge(q):
                    if len(cur_) > 1:
                        out.append(cur_)
                    cur_ = []
                    continue
                if not cur_:
                    cur_ = [p]
                cur_.append(q)
            if len(cur_) > 1:
                out.append(cur_)
        return out
    ph = m_.radians(PHI)
    e_, f_ = (V.c1 / V.k, V.c2 / V.k), (-V.c2 / V.k, V.c1 / V.k)
    st_ = clipped(C["polys"].get("street_net", []))
    wt_ = clipped(riv)
    d3 = {"slab": [tuple(q) for q in corners], "parks": clipped(pr), "streets": st_, "water": wt_,
          "street_edges": plan_edges(st_), "water_edges": plan_edges(wt_), "walls": wall_runs, "blds": d3_blds,
          "trees": d3_trees, "cam_e": e_, "cam_f": f_,
          "cam_up": (m_.sin(ph) * f_[0], m_.sin(ph) * f_[1], m_.cos(ph)),
          "cam_dir": (m_.cos(ph) * f_[0], m_.cos(ph) * f_[1], -m_.sin(ph)),
          "c_slab": SLAB_TOP, "c_park": PARK_C, "c_street": ROAD[0], "c_street_edge": ROAD[1], "c_water": WATER,
          "c_water_edge": WATER_LINE, "c_wall": WALL_C, "c_shadow": SHADOW, "c_trunk": TRUNK}
    S2 = sides + [slab_top] + parks + road + water + walls + body + labels   # water over the streets (mb_draw order)
    return dict(c, shapes=S2, view=V, d3=d3), cnt


def _hatch(rings, step, ang):
    """v3.0: even-odd hatch segments (page mm) of rings at ang degrees every step mm"""
    import math as m_
    a = m_.radians(ang)
    dv, nv = (m_.cos(a), m_.sin(a)), (-m_.sin(a), m_.cos(a))
    E = [(R[i - 1], R[i]) for R in rings for i in range(len(R))]
    ts = [q[0] * nv[0] + q[1] * nv[1] for R in rings for q in R]
    if not ts:
        return []
    out = []
    t = (int(min(ts) / step) + 1) * step
    while t < max(ts):
        xs = []
        for p, q in E:
            fp, fq = p[0] * nv[0] + p[1] * nv[1] - t, q[0] * nv[0] + q[1] * nv[1] - t
            if (fp < 0) != (fq < 0):
                r = fp / (fp - fq)
                xs.append((p[0] + (q[0] - p[0]) * r, p[1] + (q[1] - p[1]) * r))
        xs.sort(key=lambda z: z[0] * dv[0] + z[1] * dv[1])
        out += [(xs[i], xs[i + 1]) for i in range(0, len(xs) - 1, 2)]
        t += step
    return out


def thin_lines(items, k):
    """v4.3 (Aras 15 Nov 15:57 UTC "scale the lines according to the drawing size ... across all drawings", standing):
    every line heavier than 0.25 mm times the drawing's stroke factor k (pages_common pc_stroke_k), never under 0.25"""
    return [it[:3] + (max(0.25, it[3] * k),) + it[4:] if it[0] == "line" and it[3] and it[3] > 0.25 else it
            for it in items]


def main():
    t0 = time.time()
    log = []
    G = load_common()
    lib = G["pc_lib"](log)
    K = G["pc_data"](log)["key"]
    MB = G["pc_mb_lib"](log)
    mix = MB["mixh"]
    page = tuple(globals().get("page_mm") or A3)
    c = clean_list(p03(log), lib["text_w"], log)    # v2.3: the numbered list cleaned (Aras 04:58 UTC)
    c, bcnt = rebuild(c, G, log)                      # v2.5: roads and buildings from MapBase (Aras 10:34 UTC)

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
    leg = list(c["legend"])
    if bcnt is not None:                                 # v2.5: the building rows recounted, context row added
        out_ = []
        for sw, txt in leg:
            cl_ = next((v for k_, v in LEGEND_CLS if txt.startswith(k_)), None)
            if cl_ is not None:
                if not bcnt.get(cl_):
                    continue
                txt = re.sub(r"\(\d[\d,]*\)\s*$", u"(%d)" % bcnt[cl_], txt)
            out_.append((sw, txt))
        if bcnt.get("context"):
            k_ = max([i_ for i_, (sw, txt) in enumerate(out_) if any(txt.startswith(k__) for k__, v in LEGEND_CLS)]
                     or [-1]) + 1
            out_.insert(k_, ({"kind": "fill", "colour": CTX[0], "edge": CTX[3]},
                             u"Other buildings, use not recorded (%d)" % bcnt["context"]))
        leg = out_
        out_ = []                                        # v3.0: water, trees from MapBase
        for sw, txt in leg:
            if txt.startswith(u"Trees: Stone pine"):
                continue
            if txt.startswith(u"Trees"):
                sw, txt = dict(sw, colour=TREE_KEY), u"Trees (%d)" % bcnt.get("_trees", 0)
            elif txt.startswith(u"Stream channel"):
                sw = dict(sw, colour=MB["MB_STYLE"]["water"])
            out_.append((sw, txt))
        leg = out_
    for sw, txt in leg:
        col = rc(sw.get("colour"))
        if sw.get("kind") == "dash":
            rows.append((lambda x, y, col=col: [L_([(x - 4.5, y), (x + 4.5, y)], col, 0.25, "legend", (1.6, 0.9))],
                         txt))
        elif sw.get("kind") == "dot":
            rows.append((lambda x, y, col=col: [P_([circle(x, y, 1.2, 16)], col, None, 0.0, "legend")], txt))
        else:
            rows.append((lambda x, y, col=col, ed=sw.get("edge"): [P_([[(x - 4.5, y - 2.0), (x + 4.5, y - 2.0),
                                                                        (x + 4.5, y + 2.0), (x - 4.5, y + 2.0)]],
                                                                      col, ed, 0.15 if ed else 0.0, "legend")], txt))
    # ---- v2.4: the numbered list out of the drawing, into the legend; the drawing's box = the drawing itself
    X0, Y0 = 314.0, 120.0
    inl = lambda t: t["anchor"]["pt"][0] >= X0 and t["anchor"]["pt"][1] >= Y0
    num = lambda t: t["string"].strip().isdigit()
    lt = [t for t in c["texts"] if inl(t)]
    badge_fill = {}
    keep = []
    for sh in c["shapes"]:
        pts = [q for R in sh.get("rings", []) for q in R] or sh.get("pts", [])
        if (sh.get("grp") or u"").startswith(u"labels") and pts and min(q[0] for q in pts) >= X0 - 2.0 and \
                min(q[1] for q in pts) >= Y0:
            badge_fill[round(sum(q[1] for q in pts) / len(pts), 0)] = rc(sh.get("fill"))
            continue
        keep.append(sh)
    if lt:
        lrows = [(None, u"NUMBERED ON THE DRAWING")]
        for b in sorted([t for t in lt if num(t)], key=lambda t: int(t["string"])):
            y = b["anchor"]["pt"][1]
            words = sorted([t for t in lt if not num(t) and abs(t["anchor"]["pt"][1] - y) < 1.0],
                           key=lambda t: t["anchor"]["pt"][0])
            label = u" ".join(t["string"] for t in words)
            fill = badge_fill[min(badge_fill, key=lambda yy: abs(yy - y))] if badge_fill else "4A3F35"
            lrows.append((lambda x, y, n=b["string"], f_=fill: [P_([circle(x, y, 2.0, 32)], f_, "FFFFFF", 0.2,
                                                                     "legend"),
                                                                  G["pc_text_c"](n, x, y, 2.2, "FFFFFF", "legend")], label))
        rows = lrows + rows
        c = dict(c, shapes=keep, texts=[t for t in c["texts"] if not inl(t)])
        P = [q for sh in c["shapes"] for q in ([q for R in sh.get("rings", []) for q in R] or sh.get("pts", []))]
        P += [tuple(t["anchor"]["pt"]) for t in c["texts"]]
        ext = (max(c["extent"][0], min(q[0] for q in P) - 1.0), min(q[1] for q in P) - 1.0,
               min(c["extent"][2], max(q[0] for q in P) + 1.0), min(c["extent"][3], max(q[1] for q in P) + 1.0))
        log.append(u"list: %d rows moved into the legend; drawing box %.0f x %.0f mm (was %.0f x %.0f)" % (
            len(lrows) - 1, ext[2] - ext[0], ext[3] - ext[1], c["extent"][2] - c["extent"][0],
            c["extent"][3] - c["extent"][1]))
        c = dict(c, extent=ext)
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
    # ---- v4.0: the drawing from the 3D model in Rhino (depth by Rhino), the 2D painter only without Rhino
    photos, use3d = [], False
    d3 = c.get("d3")
    V = c.get("view")
    doc = None
    try:
        import Rhino
        doc = Rhino.RhinoDoc.ActiveDoc
    except Exception:
        pass
    if AXO_RASTER and doc is not None and d3 and V is not None:   # v5.0: off (Aras 17:02: vector only)
        guids = []
        try:
            rc3 = lambda h: rc(h) or h
            d3c = dict(d3)
            for k_ in [k_ for k_ in d3c if k_.startswith("c_")]:
                d3c[k_] = rc3(d3c[k_])
            d3c["blds"] = [(P_b, h_b, tuple(rc3(x_) for x_ in cl_)) for P_b, h_b, cl_ in d3["blds"]]
            cam = ((d3["cam_e"][0], d3["cam_e"][1], 0.0), d3["cam_up"], d3["cam_dir"])
            reg = []
            for i in range(4):
                p, q = d3["slab"][i], d3["slab"][(i + 1) % 4]
                for j in range(10):
                    x, y = p[0] + (q[0] - p[0]) * j / 10.0, p[1] + (q[1] - p[1]) * j / 10.0
                    reg.append((x, y, V.zdem(x, y)))
            # v4.5: the calibration tile, 30 m square, 150 m left of the slab's leftmost corner (in the view)
            E3 = d3["cam_e"]
            lv = min(d3["slab"], key=lambda p_: p_[0] * E3[0] + p_[1] * E3[1])
            zc = V.zdem(lv[0], lv[1])
            cc = (lv[0] - 150.0 * E3[0], lv[1] - 150.0 * E3[1])
            cal = [(cc[0] + a_ * 15.0, cc[1] + b_ * 15.0, zc) for a_, b_ in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            d3c["cal"] = cal
            guids, bb3 = axo3d_build(doc, d3c, V.zdem, log)
            cap, why = None, []
            for mi_, mn_ in enumerate((AXO3D_MODE, "Shaded", "Rendered")):   # v4.2: the first capture that passes
                png = os.path.join(OUT_DIR, NAME + "_3d%s.png" % (u"" if mi_ == 0 else u"_" + mn_.lower()))
                try:
                    c_ = axo3d_capture(doc, cam, reg + cal, AXO3D_PX, png, log, bb3, mn_)
                    calpx = [q_ for _, q_ in c_["px"][len(reg):]]
                    c_["px"] = c_["px"][:len(reg)]                # the slab edge only (check, registration)
                    axo3d_calibrate(c_, calpx, log)
                except Exception as ex:
                    why.append(u"%s: %s" % (mn_, ex))
                    continue
                ok_, msg_ = axo3d_check(c_, log)
                log.append(u"3D check, mode %s: %s%s" % (mn_, msg_, u"" if ok_ else u" (rejected)"))
                if ok_:
                    cap = c_
                    break
                why.append(u"%s: %s" % (mn_, msg_))
            if cap is None:
                raise RuntimeError(u"no capture passed the check (" + u"; ".join(why) + u")")
            # register: image px -> drawing mm (the 2D view's own formula, terrain not clamped)
            XY = [(V.c0 + V.c1 * p_[0] + V.c2 * p_[1], V.oy + V.s * V.depth(p_[0], p_[1]) + V.kz * (p_[2] - V.z0))
                  for p_, _ in cap["px"]]
            PX = [q_ for _, q_ in cap["px"]]

            def fit1(u, v):
                n = float(len(u))
                mu, mv = sum(u) / n, sum(v) / n
                a = sum((a_ - mu) * (b_ - mv) for a_, b_ in zip(u, v)) / max(1e-12, sum((a_ - mu) ** 2 for a_ in u))
                return a, mv - a * mu
            ax_, bx_ = fit1([q_[0] for q_ in PX], [r_[0] for r_ in XY])
            ay_, by_ = fit1([q_[1] for q_ in PX], [r_[1] for r_ in XY])
            res = max(max(abs(ax_ * q_[0] + bx_ - r_[0]), abs(ay_ * q_[1] + by_ - r_[1])) for q_, r_ in zip(PX, XY))
            log.append(u"3D registration: %d slab edge points, %.3f / %.3f drawing mm per px, %.2f mm off at most" % (
                len(PX), ax_, -ay_, res))
            if ax_ <= 0 or ay_ >= 0 or res > 0.5:
                raise RuntimeError(u"the capture does not register on the drawing (%.2f mm off, scale %.3f / %.3f)"
                                   % (res, ax_, ay_))
            # crop the capture to the drawing's box (the slide fits each panel by its ink, photos included)
            ex_ = c["extent"]
            i0 = max(0, int((ex_[0] - bx_) / ax_))
            i1 = min(cap["w"], int((ex_[2] - bx_) / ax_) + 1)
            j0 = max(0, int((ex_[3] - by_) / ay_))
            j1 = min(cap["h"], int((ex_[1] - by_) / ay_) + 1)
            import System
            bm_ = System.Drawing.Bitmap(png)
            try:
                cr_ = bm_.Clone(System.Drawing.Rectangle(i0, j0, i1 - i0, j1 - j0), bm_.PixelFormat)
            finally:
                bm_.Dispose()
            png2 = os.path.join(OUT_DIR, NAME + "_3d_crop.png")
            cr_.Save(png2, System.Drawing.Imaging.ImageFormat.Png)
            cr_.Dispose()
            log.append(u"3D capture cut to the drawing box: px %d-%d x %d-%d -> %s" % (i0, i1, j0, j1, png2))
            xl, xr = ax_ * i0 + bx_, ax_ * i1 + bx_
            yt, yb = ay_ * j0 + by_, ay_ * j1 + by_
            p0, p1 = T((xl, yb)), T((xr, yt))
            photos = [(png2, p0[0], p0[1], p1[0] - p0[0], p1[1] - p0[1], True)]
            use3d = True
        except Exception as ex:
            import traceback as tb_
            log.append(u"FLAG 3D: %s: %s; the 2D painter's drawing is used (%s)" % (
                type(ex).__name__, ex, tb_.format_exc().strip().splitlines()[-3:]))
        finally:
            if guids:
                axo3d_clear(doc, guids, log)
    items, n_re = [], 0
    for i_s, s in enumerate(c["shapes"]):
        if i_s < 2 and s["t"] == "poly" and s.get("fill") in ("B0AC9C", "847E75") and len(s["rings"][0]) > 3:
            run = [T(q) for q in s["rings"][0][:-2]]      # v2.9: the cut face = a constant band under the edge
            low = [(q[0], q[1] - SLAB_MM) for q in run]
            items.append(("poly", [run + low[::-1]], rc(s["fill"]), None, 0.0, None, u"axo_slab", 1, None, None))
            P0, P1 = run[0], run[-1]
            Ln = ((P1[0] - P0[0]) ** 2 + (P1[1] - P0[1]) ** 2) ** 0.5
            for j in range(1, int(Ln / 0.9)):            # soil hatching, as slide 2's axo tiles (B08)
                t_ = j * 0.9 / Ln
                k_ = min(len(run) - 1, int(t_ * (len(run) - 1)))
                q = (P0[0] + (P1[0] - P0[0]) * t_, run[k_][1] + (run[min(k_ + 1, len(run) - 1)][1] - run[k_][1]) *
                     (t_ * (len(run) - 1) - k_))
                items.append(("line", [(q[0], q[1] - 0.15), (q[0] - 0.9, q[1] - SLAB_MM + 0.15)], "8E877C", 0.06,
                              None, u"axo_slab", 1))
            items.append(("line", low, "6E675E", 0.3, None, u"axo_slab", 1))
            continue
        if use3d and not (s.get("grp") or u"").startswith(u"labels"):
            continue                                     # v4.0: drawn by Rhino (the image under the vector)
        lay = u"axo_" + (s.get("lay") or (s.get("grp") or u"other/0").split(u"/")[0])   # v5.1: one body layer
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
        if False:  # v3.3: no hatch on the water (Aras 14:38 UTC)   # v3.0: the base map's water hatch
            hs, ha, hc, hw = MB["MB_STYLE"]["water_hatch"]
            for a_, b_ in _hatch([[T(q) for q in R] for R in s["rings"]], hs, ha):
                items.append(("line", [a_, b_], hc, hw, None, u"axo_water_hatch", 1))
    model = [dict((k_, v) for k_, v in s.items() if k_ != "opacity") for s in c["shapes"]]
    for s in model:                                      # v3.0: slide 2's node axos cut from this (spine thread)
        s["fill"], s["stroke"] = rc(s.get("fill")), rc(s.get("stroke"))
    V = c.get("view")
    try:
        mp = os.path.join(os.path.dirname(CACHE), "axo_model.json")
        with open(mp, "w", encoding="utf-8") as f:
            json.dump({"version": VERSION, "units": u"drawing mm (y up); page mm = (ox + x * sd, oy + y * sd)",
                       "view": dict(c0=V.c0, c1=V.c1, c2=V.c2, oy=V.oy, s=V.s, k=V.k, kz=V.kz, phi=PHI, z0=V.z0)
                       if V else None, "page": dict(ox=ox, oy=oy, sd=sd, w=page[0], h=page[1]),
                       "shapes": model, "d3": c.get("d3")}, f, ensure_ascii=False)   # v4.0: the 3D inputs too
        log.append(u"model: %d shapes + view written to %s (slide 2 node axos)" % (len(model), mp))
    except Exception as ex:
        log.append(u"FLAG model: %s not written (%s: %s)" % (mp, type(ex).__name__, ex))
    discs = []                                           # v4.1: the numbered markers' discs (booklet mm)
    for s in c["shapes"]:
        R = (s.get("rings") or [[]])[0]
        if (s.get("grp") or u"").startswith(u"labels") and len(R) >= 24:
            xs, ys = [q[0] for q in R], [q[1] for q in R]
            w_, h_ = max(xs) - min(xs), max(ys) - min(ys)
            if 2.5 < w_ < 6.0 and abs(w_ - h_) < 0.15 * w_:
                discs.append(((min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0))
    n_cen = 0
    for t in c["texts"]:
        x, y = T(t["anchor"]["pt"])
        if t["string"].strip().isdigit() and discs:      # v4.1: a marker number sits on its disc centre
            ax_, ay_ = t["anchor"]["pt"]
            dc = min(discs, key=lambda q: (q[0] - ax_) ** 2 + (q[1] - ay_) ** 2)
            if (dc[0] - ax_) ** 2 + (dc[1] - ay_) ** 2 < 2.5 ** 2:
                cx_, cy_ = T(dc)
                items.append(G["pc_text_c"](t["string"].strip(), cx_, cy_, t["size_pt"] * PT * sd,
                                            rc(t.get("colour") or "FFFFFF"), u"axo_labels", bool(t.get("bold", True))))
                n_cen += 1
                continue
        al = (t.get("positions") or [u"=L"])[0].replace(u"=", u"")
        items.append(("text", t["string"], x, y, t["size_pt"] * PT * sd, rc(t.get("colour") or "4A3F35"),
                      bool(t.get("bold")), al if al in (u"L", u"C", u"R") else u"L", u"axo_labels", None, None))
    log.append(u"markers: %d number(s) centred on %d disc(s)" % (n_cen, len(discs)))
    log.append(u"drawing: %d shapes (%d recoloured), %d words, legend %d rows; booklet run %s (%s)" % (
        len(c["shapes"]), n_re, len(c["texts"]), len(rows), c.get("run"), c.get("version")))
    M = Sheet(box, page[0], page[1])
    Mc = Sheet((0.0, box[3] + 6.0, 4.0, page[1] - 12.0), page[0], page[1])
    items += [it for it in G["pc_sheet"](Mc, K, lib, title, sub, rows, [], u"", cols=ncol)
              if it[8 if it[0] == "text" else 6 if it[0] == "poly" else 5] not in ("north_scale", "frame")]
    items = thin_lines(items, G["pc_stroke_k"](box[2] - box[0], box[3] - box[1], log, NAME))   # v4.3
    G["pc_write"](lib, M, items, OUT_DIR, NAME, u"What is there, axonometric", log, photos=photos)
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
