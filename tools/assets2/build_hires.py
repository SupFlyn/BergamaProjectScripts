"""Builds assets_hires.json: the high-res PhyloPic silhouettes of the assets_2 pack (30 Oct 2026) as rings.

Run once, in the cloud, from the unpacked pack (revision_2026-10-29/assets_2_2026-10/Bergama_assets_2_2026-10/):
    python build_hires.py <pack dir> <out.json>
Needs shapely + svgelements (pip). Not a Rhino script: the Grasshopper scripts read the JSON (common/hires.py).

Per asset: painter's order (white paths cut, others add), even-odd inside a path, roots cut at the ground (trees,
tomato), feet / ground at y = 0, height 1.0 (units of its own height), y up, x centred on the stem at the ground
(plants) or on the bounding box (fauna), simplified to 0.15 % of the height. Each part = {fill: one keyhole ring (even-odd), lines: [outer, holes...] for outlines}.
"""
import json, sys, os, csv
import svgelements as se
from shapely.geometry import Polygon, MultiPolygon, LineString, box
from shapely.ops import unary_union
from shapely import affinity, make_valid

# id: (file under the pack, what, kind, ground cut)  kind: tree / crop / fauna
PICKS = {
    # trees (one author: Guillaume Dera, CC0). Stand-ins of the same genus per GAPS.md A.
    "plane": ("A_plants/sets/phylopic_dera_trees/Platanus_occidentalis__Guillaume_Dera__CC0_1_0__2ae6e310.svg",
              "Platanus occidentalis (stand-in for P. orientalis), leafy", "tree", True),
    "plane_bare": ("A_plants/sets/phylopic_dera_trees/Platanus_occidentalis__Guillaume_Dera__CC0_1_0__3262ed7c.svg",
                   "Platanus occidentalis (stand-in for P. orientalis), bare", "tree", True),
    "ash": ("A_plants/sets/phylopic_dera_trees/Fraxinus_excelsior__Guillaume_Dera__CC0_1_0__ee1e627e.svg",
            "Fraxinus excelsior (stand-in for F. angustifolia)", "tree", True),
    "olive": ("A_plants/sets/phylopic_dera_trees/Olea_europaea__Guillaume_Dera__CC0_1_0__f72ef53b.svg",
              "Olea europaea", "tree", True),
    "stone_pine": ("A_plants/sets/phylopic_dera_trees/Pinus_pinea__Guillaume_Dera__CC0_1_0__9872213f.svg",
                   "Pinus pinea", "tree", True),
    # crops
    "maize": ("B_agriculture/sets/phylopic_crops/Zea_mays__Mason_McNair__CC0_1_0__cd2aa8d4.svg",
              "Zea mays", "crop", False),
    "tomato": ("B_agriculture/sets/phylopic_crops/Solanum_lycopersicum__Aviad_Perry__CC0_1_0__64046749.svg",
               "Solanum lycopersicum", "crop", True),
    # fauna (PICKS_harmony.csv)
    "heron": ("D_fauna/sets/phylopic/heron/Ardea_cinerea__Guillaume_Dera__CC0_1_0__5d38ae89.svg",
              "Ardea cinerea", "fauna", False),
    "egret": ("D_fauna/sets/phylopic/little_egret/Egretta_garzetta_nigripes__Hugo_Gruson__CC0_1_0__ca77f63b.svg",
              "Egretta garzetta nigripes", "fauna", False),
    "stork": ("D_fauna/sets/phylopic/white_stork/Ciconia_ciconia__Andy_Wilson__CC0_1_0__2babc63a.svg",
              "Ciconia ciconia", "fauna", False),
    "kingfisher": ("D_fauna/sets/phylopic/kingfisher/Alcedo_atthis__Steven_Traver__CC0_1_0__632580ed.svg",
                   "Alcedo atthis", "fauna", False),
    "swallow": ("D_fauna/sets/phylopic/other_stream_birds/Hirundo_rustica__Andy_Wilson__CC0_1_0__092135f1.svg",
                "Hirundo rustica", "fauna", False),
    "frog": ("D_fauna/sets/phylopic/marsh_frog/Pelophylax_esculentus__Luca_Leicht__CC_BY_4_0__b41b4b2e.svg",
             "Pelophylax esculentus (stand-in for P. ridibundus)", "fauna", False),
    # green toad: the PICKS file holds a raster <image> inside the SVG, no vector: not used (drawn pictogram stays)
    "turtle": ("D_fauna/sets/phylopic/terrapin/Mauremys_reevesii__Kawahara_Keiga__Public_Domain_Mark_1_0__1944f7c1.svg",
               "Mauremys reevesii (stand-in for M. rivulata)", "fauna", False),
    "snake": ("D_fauna/sets/phylopic/snake/Natrix_natrix__Danny_S__Public_Domain_Mark_1_0__1da15fb6.svg",
              "Natrix natrix (stand-in for N. tessellata)", "fauna", False),
    "dragonfly": ("D_fauna/sets/phylopic/dragonfly/Aeshna_mixta__Wouter_Koch__CC0_1_0__36543d34.svg",
                  "Aeshna mixta (stand-in for Sympetrum fonscolombii)", "fauna", False),
    "damselfly": ("D_fauna/sets/phylopic/damselfly/Calopteryx_splendens__Maxime_Dahirel__CC_BY_3_0__8af9c80d.svg",
                  "Calopteryx splendens", "fauna", False),
}
TOL = 0.0015      # simplify tolerance, fraction of the height
N_SEG = 10        # points per curve segment


def is_white(c):
    try:
        return c is not None and c.value is not None and c.red > 240 and c.green > 240 and c.blue > 240
    except Exception:
        return False


def path_geom(e):
    """even-odd geometry of one svgelements Path"""
    g = None
    for sp in e.as_subpaths():
        pts = []
        for seg in se.Path(sp):
            if isinstance(seg, se.Move):
                pts.append((seg.end.x, seg.end.y))
            elif isinstance(seg, (se.Line, se.Close)):
                if seg.end is not None:
                    pts.append((seg.end.x, seg.end.y))
            else:
                for i in range(1, N_SEG + 1):
                    p = seg.point(i / float(N_SEG))
                    pts.append((p.x, p.y))
        if len(pts) < 3:
            continue
        poly = make_valid(Polygon(pts))
        g = poly if g is None else g.symmetric_difference(poly)
    return g


def load(fn):
    svg = se.SVG.parse(fn)
    res = None
    for e in svg.elements():
        if not isinstance(e, se.Path) or e.fill is None or e.fill.value is None:
            continue
        g = path_geom(e)
        if g is None or g.is_empty:
            continue
        if is_white(e.fill):
            if res is not None:
                res = res.difference(g)
        else:
            res = g if res is None else res.union(g)
    return affinity.scale(res, 1.0, -1.0, origin=(0, 0))      # y up


def width_at(g, y, x0, x1):
    return g.intersection(LineString([(x0 - 1, y), (x1 + 1, y)])).length


def ground_y(g):
    """top of the root zone: lowest level of the stem (narrowest band) above which the roots spread"""
    x0, y0, x1, y1 = g.bounds
    H = y1 - y0
    ys = [y0 + H * i / 400.0 for i in range(1, 400)]
    ws = [width_at(g, y, x0, x1) for y in ys]
    # the stem: narrowest level in the lower 45 % that still has ink
    wmax = max(ws)
    run, yrun = None, None
    for w, y in sorted(zip(ws, ys), key=lambda t: -t[1]):       # from the top down
        if y > y0 + 0.6 * H or w <= 0:
            continue
        if run is None or w < run:
            run, yrun = w, y
        elif run < 0.15 * wmax and w > 3.0 * run:            # the stem has been passed: the roots spread here
            return y, yrun, run
    return y0, yrun, run


def stem_x(g, y):
    x0, _, x1, _ = g.bounds
    s = g.intersection(LineString([(x0 - 1, y), (x1 + 1, y)]))
    parts = list(getattr(s, "geoms", [s]))
    p = max(parts, key=lambda q: q.length)
    return (p.bounds[0] + p.bounds[2]) / 2.0


def keyhole(outer, holes):
    """ONE ring for an even-odd fill: each hole spliced into the outer ring at its nearest vertex pair (the slit is
    walked there and back, so it never shows in the fill; outlines are drawn from the separate rings)"""
    import numpy as np
    ring = list(outer)
    for h in holes:
        A, Hh = np.array(ring), np.array(h)
        d = ((A[:, None, :] - Hh[None, :, :]) ** 2).sum(axis=2)
        i, j = np.unravel_index(int(d.argmin()), d.shape)
        ring = ring[:i + 1] + h[j:] + h[:j + 1] + ring[i:]
    return ring


def rings(g):
    out = []
    for p in getattr(g, "geoms", [g]):
        if not isinstance(p, Polygon) or p.area <= 0:
            continue
        r = lambda c: [[round(x, 4), round(y, 4)] for x, y in list(c.coords)[:-1]]
        ext, hol = r(p.exterior), [r(i) for i in p.interiors if len(i.coords) > 3]
        out.append(dict(fill=keyhole(ext, hol), lines=[ext] + hol))
    return out


def facing(g):
    """+1 when the head (topmost point) lies left of the centre (PhyloPic convention: face left)"""
    x0, y0, x1, y1 = g.bounds
    top = g.intersection(box(x0, y1 - 0.08 * (y1 - y0), x1, y1)).centroid.x
    return 1 if top < (x0 + x1) / 2.0 else -1


def main(pack, out):
    src = {}
    for fn in (os.path.join(pack, "SOURCES.csv"), os.path.join(pack, "D_fauna/sets/phylopic/PICKS_harmony.csv")):
        if os.path.exists(fn):
            for row in csv.DictReader(open(fn, encoding="utf-8")):
                src[row.get("file")] = row
    lib = {}
    for key, (rel, what, kind, cut) in PICKS.items():
        g = load(os.path.join(pack, rel))
        g = make_valid(g)
        x0, y0, x1, y1 = g.bounds
        note = ""
        if cut:
            gy, ys, wst = ground_y(g)
            g = g.intersection(box(x0 - 1, gy, x1 + 1, y1 + 1))
            cx = stem_x(g, gy + 0.01 * (y1 - gy))
            note = "roots cut at %.1f %% of the drawn height" % (100.0 * (gy - y0) / (y1 - y0))
        else:
            cx = (x0 + x1) / 2.0
            gy = y0
        bx0, by0, bx1, by1 = g.bounds
        H = by1 - gy
        g = affinity.translate(g, -cx, -gy)
        g = affinity.scale(g, 1.0 / H, 1.0 / H, origin=(0, 0))
        g = g.simplify(TOL, preserve_topology=True)
        g = unary_union([p for p in getattr(g, "geoms", [g]) if p.area > 2e-5])
        b = g.bounds
        row = src.get(rel, {})
        lib[key] = dict(what=what, kind=kind, file=os.path.basename(rel), author=row.get("author", ""),
                        url=row.get("url", ""), licence=row.get("licence", ""), credit=row.get("credit", ""),
                        x0=round(b[0], 4), x1=round(b[2], 4), h=1.0, face=facing(g) if kind == "fauna" else 0,
                        note=note, parts=rings(g))
        n = sum(len(p["fill"]) for p in lib[key]["parts"])
        print("%-11s w/h %.2f  parts %3d  points %5d  face %+d  %s  %s" % (
            key, b[2] - b[0], len(lib[key]["parts"]), n, lib[key]["face"], row.get("licence", "?"), note))
    json.dump(dict(version="assets_2 30 Oct 2026", units="height = 1, ground/feet y = 0, y up", lib=lib),
              open(out, "w"), separators=(",", ":"))
    print(out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
