# ---- v33 (Q11): satellite strips under every section: land cover (CLC+ Backbone 2021) and greenness (Sentinel-2
# NDVI, January and July), metre by metre along the line, from the plant analysis's section data in SEAM_PACK
CLC_COL = {1: C("A5A097"), 2: LEAF_COL[2], 3: LEAF_COL[0], 4: LEAF_COL[1], 5: C("A9AE7C"), 6: C("C9D1A0"),
           7: C("E0D8A0"), 8: C("D8D2C0"), 9: C("E6DCC8"), 10: C("91ADB4")}
NDVI_STEPS = [(0.15, C("E9E2CF")), (0.25, C("D9D7A8")), (0.35, C("B9C27F")), (0.45, C("93A65E")), (0.55, C("6E8A47")),
              (9.0, C("4E6B37"))]
SAT_ROWS = [("clc", "land cover"), ("jan", "green, Jan"), ("jul", "green, Jul")]


# v40 (Aras 25 Oct: "texts and graphics are on top each other ... make the diagram clearer"): the tree-cover chart
# reads at a glance: each bank's four distance bands named beside their rows (0-15 m next to the stream), the stream
# between the banks with its covered reaches drawn on it and the bridges as ticks across it only, a distance axis
# every 500 m, a key of drawn samples. Values as in the pack (no smoothing). Words at RIP_TH page units: the booklet
# crops this panel at 392 mm wide, where they print at 7.5 pt or more.
RIP_TH = 0.6
RIP_RAMP = [(0.0, C("F6F5EF")), (1.0, C("E3E6CF")), (5.0, C("C9D1A4")), (10.0, C("A9B57F")), (20.0, C("8C9969")),
            (40.0, C("6B774A"))]
RIP_COVERED = mix(BLUE_D, INK, 0.35)                   # the stream where it runs under the town
PANEL_RECTS = {}        # v40: a panel's drawing with its in-drawing words (no title, key or notes): (x0, y0, x1, y1)


def rip_legend():
    """The tree-cover chart's key as drawn samples: [(kind, colour, name)]."""
    out = []
    for k, (t, c_) in enumerate(RIP_RAMP):
        out.append(("box", c_, "tree cover {:g}-{:g} %".format(t, RIP_RAMP[k + 1][0]) if k + 1 < len(RIP_RAMP)
                    else "tree cover {:g} % +".format(t)))
    return out + [("box", CAT["water"][1], "the Selinos stream"), ("box", RIP_COVERED, "covered reach"),
                  ("line", INK, "bridge")]


# v33: the green table of bergama_fabric_green v10
def green_rows(S):
    """(label, m2) for the green table: land-use areas of selinus_board (S.area) and, for the agricultural ground,
    the farmland / orchard zone outlines (z["A"])."""
    orch = sum(z["A"] for z in S.zones if z["kind"] == "agri" and z.get("sub") == "orchard")
    field = sum(z["A"] for z in S.zones if z["kind"] == "agri" and z.get("sub") != "orchard")
    g, a, w = S.area.get("green", 0.0), S.area.get("agri", 0.0), S.area.get("water", 0.0)
    return [("Green & open ground", g, True), ("Agricultural ground (land-use table)", a, True),
            ("   of which farmland · fields (zone outlines)", field, False),
            ("   of which orchards (zone outlines)", orch, False),
            ("Water · the Selinus", w, True), ("GREEN + AGRICULTURE + WATER", g + a + w, True)] + [
            (lab, getattr(S, "lc_area", {}).get(k, 0.0), True) for k, lab, _c in reversed(LC_CLASSES)
            if getattr(S, "lc", {}).get(k)]


def draw_green_table(S, B, x, y, w, U):
    L = "LU_BOARD::Legend"
    B.text("GREEN, FARMLAND AND ORCHARDS", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    tot = S.frame_area                                   # v35: was the mapped part only (62.59 of 149 ha in the test)
    h = 0.5 * U
    yy = y - 1.6 * U
    B.text("ha", x + w - 6.0 * U, yy, 0.38 * U, INK2, L, align="R")
    B.text("%", x + w, yy, 0.38 * U, INK2, L, align="R")
    B.line([(x, yy - 0.32 * U), (x + w, yy - 0.32 * U)], INK, L, 20, 0.15)
    yy -= 1.2 * U
    for lab, a, main in green_rows(S):
        col = INK if main else INK2
        B.fit(lab, x, yy, h, w - 14.0 * U, col, L, bold=lab.isupper())
        B.text("{:.2f}".format(a / 1e4), x + w - 6.0 * U, yy, h, col, L, align="R", bold=lab.isupper())
        B.text("{:.1f}".format(100.0 * a / tot), x + w, yy, h, col, L, align="R", bold=lab.isupper())
        yy -= 1.25 * U
    SA = getattr(S, "whole", None)
    if SA is not None and getattr(SA, "lc", None):        # v36: farmland and orchards outside the frame, whole file
        la, lb = getattr(SA, "lc_area", {}), getattr(S, "lc_area", {})
        out_f = max(0.0, la.get("farmland", 0.0) - lb.get("farmland", 0.0))
        out_o = max(0.0, la.get("orchard", 0.0) - lb.get("orchard", 0.0))
        lab = u"Outside the frame · farmland {:.1f} + orchards {:.1f} {}".format(                        # v38
            out_f / 1e4, out_o / 1e4, bcite(u"Outside the frame: farmland and orchards in the whole survey file "
                                            u"beyond the site frame, satellite / inferred."))
        B.fit(lab, x, yy, h, w - 14.0 * U, INK2, L)
        B.text("{:.2f}".format((out_f + out_o) / 1e4), x + w - 6.0 * U, yy, h, INK2, L, align="R")
        B.text(u"-", x + w, yy, h, INK2, L, align="R")
        yy -= 1.25 * U
    yy = B.para("% of the site frame · {:.2f} ha {}".format(tot / 1e4, bcite(                           # v38: keywords
        "Green table: farmland and orchard figures are the summed zone outlines of the survey and OSM and need not add "
        "up exactly to the agricultural row. Satellite rows: ESA WorldCover 2021 inside the site, counted under "
        "buildings and streets too (10 m pixels).")), x, yy - 0.2 * U, w, 0.36 * U, INK2, L)
    return yy


# ============================================================ v33 S2 · HOW PEOPLE USE IT
# Movement potential: the engine of bergama_movement v1 (2026-10-22), merged unchanged from 'the route search' to
# '_runs' (its own copies of _py_candidates and _popen_kw dropped: the board's are the same; _kernel_file, ramp and
# PAR renamed _mv_kernel_file, mv_ramp and MV_PAR). Method: bergama_movement v1 header, repeated in the drawing.
import heapq
import hashlib
import tempfile
import time
import pickle

# ============================================================ the route search (run in Rhino AND in the worker processes)
# One text, executed in both places, so both run the same code. Whole numbers only: the sums are exact in any order.
MV_KERNEL = r'''
import heapq, os, pickle, sys


def mv_source(adj, s, ws, dw, limit):
    """Origin node s (ws buildings on it): the shortest-route tree within limit, then every destination's pairs
    carried back towards s. adj[i] = ((j, cost, edge), ...); dw = {node: destinations on it}. Returns {edge: pairs}.
    Ties: the first route found with the smallest cost, nodes taken in (cost, node number) order."""
    dist = {s: 0.0}
    pred = {}
    seen = set()
    order = []
    h = [(0.0, s)]
    while h:
        d, i = heapq.heappop(h)
        if i in seen:
            continue
        seen.add(i)
        order.append(i)
        for j, c, e in adj[i]:
            nd = d + c
            if nd <= limit and (j not in dist or nd < dist[j]):
                dist[j] = nd
                pred[j] = (i, e)
                heapq.heappush(h, (nd, j))
    flow = {}
    out = {}
    for i in reversed(order):
        f = flow.get(i, 0) + dw.get(i, 0)
        if f and i != s:
            p, e = pred[i]
            out[e] = out.get(e, 0) + ws * f
            flow[p] = flow.get(p, 0) + f
    return out


def mv_many(adj, tasks, dw, limit):
    """Every origin of tasks [(node, buildings)]: (sum per edge, the first origin's own result)."""
    tot = {}
    first = None
    for k, (s, ws) in enumerate(tasks):
        r = mv_source(adj, s, ws, dw, limit)
        if k == 0:
            first = r
        for e, v in r.items():
            tot[e] = tot.get(e, 0) + v
    return tot, first


def _mv_worker_main(argv):
    if len(argv) > 1 and argv[1] == "--probe":
        sys.stdout.write("mv-ok")
        return
    mf, tf, of = argv[1], argv[2], argv[3]
    with open(mf, "rb") as fh:
        adj, dw, limit = pickle.load(fh)
    with open(tf, "rb") as fh:
        tasks = pickle.load(fh)
    res = mv_many(adj, tasks, dw, limit)
    with open(of + ".tmp", "wb") as fh:
        pickle.dump(res, fh, protocol=4)
    os.replace(of + ".tmp", of)
'''
_MVK = {"__name__": "mv_kernel"}
exec(compile(MV_KERNEL, "mv_kernel", "exec"), _MVK)

_MV_PY = {}




def _mv_kernel_file():
    h = hashlib.sha1(MV_KERNEL.encode("utf-8")).hexdigest()[:12]
    d = os.path.join(tempfile.gettempdir(), "bergama_movement_workers")
    if not os.path.isdir(d):
        os.makedirs(d)
    f = os.path.join(d, "mv_kernel_%s.py" % h)
    if not os.path.isfile(f):
        with open(f + ".tmp", "w", encoding="utf-8") as fh:
            fh.write(MV_KERNEL + "\n\nif __name__ == '__main__':\n    _mv_worker_main(sys.argv)\n")
        os.replace(f + ".tmp", f)
    return f, d


def worker_python():
    if "py" in _MV_PY:
        return _MV_PY["py"]
    import subprocess
    _MV_PY["py"], _MV_PY["why"] = None, "no python executable found beside Rhino"
    try:
        kf, _ = _mv_kernel_file()
    except Exception as ex:
        _MV_PY["why"] = "cannot write to the temp folder ({})".format(ex)
        return None
    for py in _py_candidates():
        try:
            r = subprocess.run([py, "-I", kf, "--probe"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=120,
                               **_popen_kw())
            if r.returncode == 0 and r.stdout.decode("utf-8", "replace").strip() == "mv-ok":
                _MV_PY["py"], _MV_PY["why"] = py, ""
                return py
            _MV_PY["why"] = "{} did not answer the probe".format(py)
        except Exception as ex:
            _MV_PY["why"] = "{} could not be started ({})".format(py, type(ex).__name__)
    return None


def run_routes(adj, tasks, dw, limit, label, log):
    """Sum of mv_source over every origin: on worker processes (one per core) when available, else in Rhino.
    The first origin of every worker is computed in Rhino too and must match exactly."""
    import subprocess
    t0 = time.time()
    n = min(MV_PAR["n"], len(tasks) // 8) if MV_PAR.get("procs", True) else 1
    py = worker_python() if n >= 2 else None
    if py is None:
        if n >= 2:
            log.append("{}: one core ({}).".format(label, _MV_PY.get("why", "")))
        tot = _MVK["mv_many"](adj, tasks, dw, limit)[0]
        log.append("{}: {} origin nodes in {:.1f} s in Rhino.".format(label, len(tasks), time.time() - t0))
        return tot
    files, procs = [], []
    try:
        kf, d = _mv_kernel_file()
        tag = "%d_%d" % (os.getpid(), int(t0 * 1000) % 100000000)
        mf = os.path.join(d, "model_%s.bin" % tag)
        with open(mf, "wb") as fh:
            pickle.dump((adj, dw, limit), fh, protocol=4)
        files.append(mf)
        parts = [tasks[w::n] for w in range(n)]       # interleaved: every worker gets a fair share
        for w, part in enumerate(parts):
            tf, of = os.path.join(d, "tasks_%s_%d.bin" % (tag, w)), os.path.join(d, "out_%s_%d.bin" % (tag, w))
            with open(tf, "wb") as fh:
                pickle.dump(part, fh, protocol=4)
            files += [tf, of]
            procs.append((subprocess.Popen([py, "-I", kf, mf, tf, of], stdout=subprocess.DEVNULL,
                                           stderr=subprocess.PIPE, **_popen_kw()), of, part))
        tot = {}
        bad = 0
        for pr, of, part in procs:
            err = pr.communicate()[1]
            if pr.returncode != 0:
                last = err.decode("utf-8", "replace").strip().splitlines()[-1:] if err else []
                raise RuntimeError("a worker stopped" + (": " + last[0] if last else ""))
            with open(of, "rb") as fh:
                wt, wfirst = pickle.load(fh)
            if part and _MVK["mv_source"](adj, part[0][0], part[0][1], dw, limit) != wfirst:
                bad += 1
            for e, v in wt.items():
                tot[e] = tot.get(e, 0) + v
        if bad:
            raise RuntimeError("{} checked origin(s) differ from Rhino's own result".format(bad))
        log.append("{}: {} origin nodes on {} worker processes in {:.1f} s (checked against Rhino).".format(
            label, len(tasks), n, time.time() - t0))
        return tot
    except Exception as ex:
        for pr, _, _ in procs:
            try:
                if pr.poll() is None:
                    pr.kill()
            except Exception:
                pass
        log.append("{}: worker processes not used ({}: {}); computed in Rhino.".format(label, type(ex).__name__, ex))
        t1 = time.time()
        tot = _MVK["mv_many"](adj, tasks, dw, limit)[0]
        log.append("{}: {} origin nodes in {:.1f} s in Rhino.".format(label, len(tasks), time.time() - t1))
        return tot
    finally:
        for f_ in files:
            try:
                os.remove(f_)
            except Exception:
                pass


# ============================================================ the street network
WALK_NO_HW = {"motorway", "motorway_link"}
CAR_HW = {"trunk", "trunk_link", "primary", "primary_link", "secondary", "secondary_link", "tertiary", "tertiary_link",
          "unclassified", "residential", "living_street", "service", "road"}
NO_VALUES = ("no",)
CLOSE_D = 4.0           # car_closed: a street piece whose middle lies this close to the curve loses its cars


def _walk_ok(t):
    if t.get("highway") in WALK_NO_HW:
        return False
    if t.get("foot") in ("yes", "designated", "permissive"):
        return True
    return t.get("foot") not in NO_VALUES and t.get("access") not in NO_VALUES


def _car_dirs(t):
    """(forward, backward) allowed for cars, as OSM tags them."""
    if t.get("highway") not in CAR_HW:
        return False, False
    for k_ in ("access", "vehicle", "motor_vehicle", "motorcar"):
        if t.get(k_) in NO_VALUES:
            return False, False
    ow = (t.get("oneway") or "").lower()
    if ow in ("yes", "1", "true"):
        return True, False
    if ow == "-1":
        return False, True
    if t.get("junction") in ("roundabout", "circular") and ow != "no":
        return True, False
    return True, True


def _speed(t, urban):
    """km/h: the OSM maxspeed, else the urban limit; (value, source)."""
    v = (t.get("maxspeed") or "").strip().lower()
    if v in ("tr:urban",):
        return urban, "maxspeed TR:urban"
    try:
        num = float(v.replace("km/h", "").replace("kmh", "").strip().split(";")[0])
        if v.endswith("mph"):
            num *= 1.609344
        if 3.0 <= num <= 150.0:
            return num, "OSM maxspeed"
    except Exception:
        pass
    return urban, "urban limit"


class SGrid(object):
    """A plain bucket grid of boxes (x0, y0, x1, y1)."""

    def __init__(self, c):
        self.c, self.d = float(c), {}

    def add(self, k, bb):
        c = self.c
        for i in range(int(math.floor(bb[0] / c)), int(math.floor(bb[2] / c)) + 1):
            for j in range(int(math.floor(bb[1] / c)), int(math.floor(bb[3] / c)) + 1):
                self.d.setdefault((i, j), []).append(k)

    def query(self, bb):
        c, out, seen = self.c, [], set()
        for i in range(int(math.floor(bb[0] / c)), int(math.floor(bb[2] / c)) + 1):
            for j in range(int(math.floor(bb[1] / c)), int(math.floor(bb[3] / c)) + 1):
                for k in self.d.get((i, j), ()):
                    if k not in seen:
                        seen.add(k)
                        out.append(k)
        return out


def _seg_x(p, q, r, s):
    """Proper crossing of segments pq and rs: (t on pq, u on rs, point) or None."""
    d = (q[0] - p[0]) * (s[1] - r[1]) - (q[1] - p[1]) * (s[0] - r[0])
    if abs(d) < 1e-12:
        return None
    t = ((r[0] - p[0]) * (s[1] - r[1]) - (r[1] - p[1]) * (s[0] - r[0])) / d
    u = ((r[0] - p[0]) * (q[1] - p[1]) - (r[1] - p[1]) * (q[0] - p[0])) / d
    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        return t, u, (p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1]))
    return None


def _proj(p, a, b):
    """(t, distance, point) of p's nearest point on segment ab."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 < 1e-18 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    q = (a[0] + t * dx, a[1] + t * dy)
    return t, math.hypot(p[0] - q[0], p[1] - q[1]), q


def build_pieces(ns, osm, props, opt, log):
    """Every street piece of the OSM network (split at shared nodes) with the proposal curves joined in.
    props: [(kind, [(x, y) survey], cross)] with kind spine | spine_car | bridge. Returns (pieces, xy) where
    pieces = [dict(a, b, L, walk, cf, cb, v, way, tags, prop)] and xy = {node: (x, y)}; OSM nodes keep their id
    (positive), new nodes get negative ids."""
    urban = float(ns.get("URBAN_LIMIT", 50.0))
    skip = set(ns.get("SKIP_HW", ()))
    xy, segs = {}, []
    n_sp = {}
    for wid in sorted(osm["ways"], key=lambda k: int(k) if str(k).lstrip("-").isdigit() else 0):
        refs, tags = osm["ways"][wid]
        hw = tags.get("highway")
        if not hw or hw in skip or tags.get("area") == "yes" or "building" in tags or len(refs) < 2:
            continue
        walk = _walk_ok(tags)
        cf, cb = _car_dirs(tags)
        if not walk and not cf and not cb:
            continue
        v, vs = _speed(tags, urban)
        n_sp[vs] = n_sp.get(vs, 0) + 1
        prev = None
        for ref in refs:
            p = osm["P"](ref)
            if not p:
                prev = None
                continue
            nid = int(ref)
            xy[nid] = (p[0], p[1])
            if prev is not None and prev != nid:
                segs.append(dict(a=prev, b=nid, walk=walk, cf=cf, cb=cb, v=v, way=str(wid), tags=tags, prop=None))
            prev = nid
    log.append("Network: {} street pieces from OSM; car speeds: {}.".format(
        len(segs), ", ".join("{} ways {}".format(n_, k_) for k_, n_ in sorted(n_sp.items()))))
    # ---- the proposal curves, joined where they cross (and at their ends)
    grid = SGrid(50.0)

    def bb2(a, b):
        pa, pb = xy[a], xy[b]
        return (min(pa[0], pb[0]), min(pa[1], pb[1]), max(pa[0], pb[0]), max(pa[1], pb[1]))
    for i, s in enumerate(segs):
        grid.add(i, bb2(s["a"], s["b"]))
    splits = {}                                       # seg index -> [(t, node)]
    nxt = [-1]

    def new_node(p):
        k = nxt[0]
        nxt[0] -= 1
        xy[k] = (p[0], p[1])
        return k
    n_x = n_end = n_loose = 0
    for ci, (kind, pts, cross) in enumerate(props):
        car = kind == "spine_car"
        ids = [new_node(p) for p in pts]
        mine = []
        for a, b in zip(ids[:-1], ids[1:]):
            mine.append(len(segs))
            segs.append(dict(a=a, b=b, walk=True, cf=car, cb=car, v=urban, way="proposal", tags={"name": kind},
                             prop=kind))
        if cross:
            for si in mine:
                s = segs[si]
                p, q = xy[s["a"]], xy[s["b"]]
                for oi in grid.query(bb2(s["a"], s["b"])):
                    o = segs[oi]
                    hit = _seg_x(p, q, xy[o["a"]], xy[o["b"]])
                    if hit is None:
                        continue
                    t, u, X = hit
                    k = new_node(X)
                    splits.setdefault(si, []).append((t, k))
                    splits.setdefault(oi, []).append((u, k))
                    n_x += 1
        for end, si in ((ids[0], mine[0]), (ids[-1], mine[-1])):
            pe = xy[end]
            if any(math.hypot(xy[k][0] - pe[0], xy[k][1] - pe[1]) < 0.5 for _, k in splits.get(si, [])):
                continue                              # the end already sits on a crossing
            best = None
            for oi in grid.query((pe[0] - opt["snap_end"], pe[1] - opt["snap_end"], pe[0] + opt["snap_end"],
                                  pe[1] + opt["snap_end"])):
                o = segs[oi]
                t, d, q = _proj(pe, xy[o["a"]], xy[o["b"]])
                if d <= opt["snap_end"] and (best is None or d < best[1]):
                    best = (oi, d, t, q)
            if best is None:
                n_loose += 1
                continue
            oi, d, t, q = best
            o = segs[oi]
            if math.hypot(q[0] - xy[o["a"]][0], q[1] - xy[o["a"]][1]) < 0.5:
                k = o["a"]
            elif math.hypot(q[0] - xy[o["b"]][0], q[1] - xy[o["b"]][1]) < 0.5:
                k = o["b"]
            else:
                k = new_node(q)
                splits.setdefault(oi, []).append((t, k))
            if d > 1e-6:
                segs.append(dict(a=end, b=k, walk=True, cf=car, cb=car, v=urban, way="proposal",
                                 tags={"name": kind + " link"}, prop=kind))
            n_end += 1
        for si in mine:
            grid.add(si, bb2(segs[si]["a"], segs[si]["b"]))
    if props:
        log.append("Proposal: {} curves; {} crossings with streets or each other, {} ends joined to the nearest street "
                   "within {:.0f} m{}.".format(len(props), n_x, n_end, opt["snap_end"],
                                              "; WARNING: {} ends join nothing (no street within reach)".format(n_loose)
                                              if n_loose else ""))
    pieces = []
    for i, s in enumerate(segs):
        cuts = sorted(splits.get(i, []))
        chain = [s["a"]] + [k for _, k in cuts] + [s["b"]]
        for a, b in zip(chain[:-1], chain[1:]):
            if a == b:
                continue
            L = math.hypot(xy[b][0] - xy[a][0], xy[b][1] - xy[a][1])
            pieces.append(dict(s, a=a, b=b, L=L, parent=i))
    return pieces, xy


def compress(pieces, use, key_extra, car):
    """The graph of the pieces `use` (indices) as chains between junctions: (adj, chains, kidx).
    A chain runs between key nodes (junctions, dead ends, and key_extra: where origins and destinations attach)
    through nodes of degree 2. car: a chain is passable one way only if every piece on it is. adj[k] = sorted
    ((k2, cost, chain), ...) over key-node numbers 0..K-1 (in node id order)."""
    inc = {}
    for pi in use:
        p = pieces[pi]
        inc.setdefault(p["a"], []).append(pi)
        inc.setdefault(p["b"], []).append(pi)
    keys = set(n for n, l in inc.items() if len(l) != 2) | (set(key_extra) & set(inc))
    for n, l in inc.items():                          # a piece from a node to itself
        if len(l) == 2 and l[0] == l[1]:
            keys.add(n)
    done = set()
    chains = []

    def walk_from(k, pi):
        nodes, seq = [k], []
        cur = k
        while True:
            p = pieces[pi]
            done.add(pi)
            nxt = p["b"] if p["a"] == cur else p["a"]
            seq.append((pi, p["a"] == cur))           # (piece, travelled a -> b)
            nodes.append(nxt)
            cur = nxt
            if cur in keys:
                break
            l = inc[cur]
            pi = l[0] if l[1] == pi else l[1]
            if pi in done:
                break
        return nodes, seq
    for k in sorted(keys):
        for pi in inc[k]:
            if pi not in done:
                chains.append(walk_from(k, pi))
    for pi in use:                                    # rings with no key node
        if pi not in done:
            k = min(pieces[pi]["a"], pieces[pi]["b"])
            keys.add(k)
            chains.append(walk_from(k, pi))
    kl = sorted(keys)
    kidx = dict((n, i) for i, n in enumerate(kl))
    adj = [[] for _ in kl]
    out = []
    zs = {} if car else (getattr(pieces, "z", None) or {})     # v34: node heights for the walking slope
    for ci, (nodes, seq) in enumerate(chains):
        L = sum(pieces[pi]["L"] for pi, _ in seq)
        if car:
            f = all(pieces[pi]["cf"] if fw else pieces[pi]["cb"] for pi, fw in seq)
            b = all(pieces[pi]["cb"] if fw else pieces[pi]["cf"] for pi, fw in seq)
            c = sum(pieces[pi]["L"] / (pieces[pi]["v"] / 3.6) for pi, _ in seq)
        else:
            f = b = True
            c = cb_ = L
            z0, z1 = zs.get(nodes[0]), zs.get(nodes[-1])        # v34: Tobler slope cost, per chain, each way
            if z0 is not None and z1 is not None and L > 1.0:
                c, cb_ = L * tobler_factor((z1 - z0) / L), L * tobler_factor((z0 - z1) / L)
        u, v = kidx[nodes[0]], kidx[nodes[-1]]
        if f:
            adj[u].append((v, c, ci))
        if b:
            adj[v].append((u, c if car else cb_, ci))
        out.append(dict(nodes=nodes, seq=seq, L=L))
    adj = [tuple(sorted(a)) for a in adj]
    return adj, out, kidx


def tobler_factor(g):
    """v34: walking time on grade g (dh/dx) over walking time on flat ground, Tobler (1993): speed = 6 exp(-3.5
    |g + 0.05|) km/h, flat 5.04 km/h. Grades are capped at +-0.5 (steps and survey noise)."""
    g = max(-0.5, min(0.5, g))
    return math.exp(-3.5 * 0.05) / math.exp(-3.5 * abs(g + 0.05))


class _Pieces(list):
    """v34: the street pieces with the terrain height of their nodes (attribute z = {node: height})."""
    z = None


def snap_points(pts, xy, node_ids, dmax):
    """{node: count} of the nearest node (of node_ids) of every point within dmax; and how many were too far."""
    g = SGrid(max(dmax, 25.0))
    for n in node_ids:
        x, y = xy[n]
        g.add(n, (x, y, x, y))
    out, far = {}, 0
    for x, y in pts:
        best, bd = None, dmax
        for n in g.query((x - dmax, y - dmax, x + dmax, y + dmax)):
            d = math.hypot(xy[n][0] - x, xy[n][1] - y)
            if d < bd or (d == bd and best is not None and n < best):
                best, bd = n, d
        if best is None:
            far += 1
        else:
            out[best] = out.get(best, 0) + 1
    return out, far


def potential(pieces, use, origins, dests, opt, car, label, log):
    """Route pairs per piece (whole numbers) for one mode and scenario."""
    adj, chains, kidx = compress(pieces, use, list(origins) + list(dests), car)
    tasks = [(kidx[n], w) for n, w in sorted(origins.items()) if n in kidx]
    dw = dict((kidx[n], w) for n, w in dests.items() if n in kidx)
    lost = sum(w for n, w in origins.items() if n not in kidx)
    if lost:
        log.append("{}: {} buildings sit on nodes this network no longer reaches.".format(label, lost))
    tot = run_routes(adj, tasks, dw, opt["t_car"] if car else opt["r_walk"], label, log)
    val = {}
    for ci, ch in enumerate(chains):
        v = tot.get(ci, 0)
        for pi, _ in ch["seq"]:
            val[pi] = v
    return val, chains


# ============================================================ origins and destinations
def collect_od(ns, S, osm, places_path, opt, log):
    """Buildings (origins) and everyday destinations within `buffer` of the frame, in survey coordinates."""
    F = S.F
    b = opt["buffer"]

    def in_area(x, y):
        u, v = F.local(x, y)
        return F.u0 - b <= u <= F.u1 + b and F.v0 - b <= v <= F.v1 + b
    org = [(u["cx"], u["cy"]) for u in S.bld if not u.get("annex") and u.get("src") != "shed"]
    n_sv = len(org)
    n_osm = 0
    for refs, tags in osm["ways"].values():
        if "building" not in tags or len(refs) < 4 or refs[0] != refs[-1]:
            continue
        P = [p for p in (osm["P"](r) for r in refs[:-1]) if p]
        if len(P) < 3:
            continue
        a_, cx, cy = ns["shoelace"]([(p[0], p[1]) for p in P])
        if a_ <= 0.0 or F.inside(cx, cy) or not in_area(cx, cy):
            continue
        org.append((cx, cy))
        n_osm += 1
    dst, srcs = [], {}
    pl = []
    if places_path:
        for p in ns["parse_places"](places_path):
            if in_area(p["x"], p["y"]):
                pl.append(p)
    g = SGrid(20.0)
    for i, p in enumerate(pl):
        g.add(i, (p["x"], p["y"], p["x"], p["y"]))
        dst.append((p["x"], p["y"], p["cat"]))
        srcs["Overture places"] = srcs.get("Overture places", 0) + 1
    dup = 0
    for ll, tags in osm["pois"]:
        bus = tags.get("highway") == "bus_stop" or tags.get("public_transport") == "platform"
        pc = "bus stop" if bus else ns["poi_class"](tags)
        if not pc:
            continue
        x, y = ns["to_dwg"](*ll)
        if not in_area(x, y):
            continue
        if not bus and any(pl[i]["cat"] == pc and math.hypot(pl[i]["x"] - x, pl[i]["y"] - y) <= 10.0
                           for i in g.query((x - 10, y - 10, x + 10, y + 10))):
            dup += 1
            continue
        dst.append((x, y, pc))
        k_ = "OSM bus stops" if bus else "OSM points"
        srcs[k_] = srcs.get(k_, 0) + 1
    cats = {}
    for _, _, c in dst:
        cats[c] = cats.get(c, 0) + 1
    log.append("Origins: {} buildings ({} surveyed in the frame, {} OSM outlines within {:.0f} m around it).".format(
        len(org), n_sv, n_osm, b))
    log.append("Destinations: {} ({}; {} OSM points dropped as the same place as an Overture place); by class: {}."
               .format(len(dst), ", ".join("{} {}".format(v, k) for k, v in sorted(srcs.items())), dup,
                       ", ".join("{} {}".format(v, k) for k, v in sorted(cats.items()))))
    return org, dst


# ============================================================ statistics
def _ranks(xs):
    o = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and xs[o[j + 1]] == xs[o[i]]:
            j += 1
        for k in range(i, j + 1):
            r[o[k]] = (i + j) / 2.0 + 1.0
        i = j + 1
    return r


def spearman(a, b):
    """Spearman rank correlation (average ranks for ties), or None."""
    if len(a) < 3:
        return None
    ra, rb = _ranks(a), _ranks(b)
    ma, mb = sum(ra) / len(ra), sum(rb) / len(rb)
    sab = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    saa = math.sqrt(sum((x - ma) ** 2 for x in ra))
    sbb = math.sqrt(sum((y - mb) ** 2 for y in rb))
    return None if saa == 0 or sbb == 0 else sab / (saa * sbb)


# ============================================================ colours
SEQ = ((238, 233, 218), (246, 207, 133), (234, 140, 62), (190, 55, 46), (98, 24, 62))     # low -> high
DIV = ((33, 102, 172), (146, 197, 222), (226, 224, 216), (244, 165, 130), (178, 24, 43))  # less -> more
WATER = (176, 208, 224)
CTX = (200, 196, 188)
PROP_C = (40, 150, 120)
INK_C = (40, 40, 40)


def mv_ramp(stops, t):
    t = max(0.0, min(1.0, t))
    x = t * (len(stops) - 1)
    i = min(len(stops) - 2, int(x))
    f = x - i
    a, b = stops[i], stops[i + 1]
    return tuple(int(round(a[k] + (b[k] - a[k]) * f)) for k in range(3))


def seq_t(v, vmax):
    return 0.0 if vmax <= 0 else math.sqrt(max(0.0, v) / vmax)


# ============================================================ the whole analysis (also used outside Rhino)
def analyse(ns, S, osm, places_path, props, closed, attractors, opt, log):
    """Both scenarios, both modes. Returns R with the pieces, their values and the street table."""
    F = S.F
    pieces, xy = build_pieces(ns, osm, props, opt, log)
    pieces = _Pieces(pieces)
    z_at = getattr(S, "z_at", None) if getattr(S, "terrain_ok", False) else None
    if z_at is not None:                                  # v34: node heights for Tobler's slope cost (walking)
        used = set(n for p in pieces if p["walk"] for n in (p["a"], p["b"]))
        pieces.z = dict((n, z_at(xy[n][0], xy[n][1])) for n in used)
        log.append("Walking cost: Tobler slope on the survey terrain ({} nodes).".format(len(pieces.z)))
    else:
        log.append("Walking cost: flat (no survey terrain), as v33.")
    org, dst = collect_od(ns, S, osm, places_path, opt, log)
    # cars off the streets under car_closed (the proposal only)
    n_cl = 0
    if closed:
        g = SGrid(50.0)
        segs = []
        for P in closed:
            for a, b in zip(P[:-1], P[1:]):
                g.add(len(segs), (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))
                segs.append((a, b))
        for p in pieces:
            if not (p["cf"] or p["cb"]) or p["prop"]:
                continue
            m = ((xy[p["a"]][0] + xy[p["b"]][0]) / 2.0, (xy[p["a"]][1] + xy[p["b"]][1]) / 2.0)
            if any(_proj(m, segs[i][0], segs[i][1])[1] <= CLOSE_D
                   for i in g.query((m[0] - CLOSE_D, m[1] - CLOSE_D, m[0] + CLOSE_D, m[1] + CLOSE_D))):
                p["closed"] = True
                n_cl += 1
        log.append("car_closed: cars taken off {} street pieces (within {:.0f} m of the curves).".format(n_cl, CLOSE_D))
    has_prop = any(p["prop"] for p in pieces)
    car_changes = n_cl > 0 or any(p["prop"] == "spine_car" for p in pieces)
    walk_b = [i for i, p in enumerate(pieces) if p["walk"] and not p["prop"]]
    walk_a = [i for i, p in enumerate(pieces) if p["walk"]]
    car_b = [i for i, p in enumerate(pieces) if (p["cf"] or p["cb"]) and not p["prop"]]
    car_a = []
    for i, p in enumerate(pieces):
        if (p["cf"] or p["cb"]) and not p.get("closed"):
            car_a.append(i)
    # origins and existing destinations attach to EXISTING nodes, the same in both scenarios
    wn = set(n for i in walk_b for n in (pieces[i]["a"], pieces[i]["b"]) if n > 0)
    cn = set(n for i in car_b for n in (pieces[i]["a"], pieces[i]["b"]) if n > 0)
    o_w, far_ow = snap_points(org, xy, wn, opt["snap"])
    d_w, far_dw = snap_points([(x, y) for x, y, _ in dst], xy, wn, opt["snap"])
    o_c, far_oc = snap_points(org, xy, cn, opt["snap"])
    d_c, far_dc = snap_points([(x, y) for x, y, _ in dst], xy, cn, opt["snap"])
    log.append("Attached within {:.0f} m: walking {} buildings / {} destinations ({} / {} too far); driving {} / {} "
               "({} / {} too far).".format(opt["snap"], sum(o_w.values()), sum(d_w.values()), far_ow, far_dw,
                                           sum(o_c.values()), sum(d_c.values()), far_oc, far_dc))
    d_wa, d_ca = dict(d_w), dict(d_c)
    if attractors:
        wn_a = set(n for i in walk_a for n in (pieces[i]["a"], pieces[i]["b"]))
        add_w, far_aw = snap_points(attractors, xy, wn_a, opt["snap"])
        for n, w in add_w.items():
            d_wa[n] = d_wa.get(n, 0) + w * opt["attr_w"]
        cn_a = set(n for i in car_a for n in (pieces[i]["a"], pieces[i]["b"]))
        add_c, _ = snap_points(attractors, xy, cn_a, opt["snap"])
        for n, w in add_c.items():
            d_ca[n] = d_ca.get(n, 0) + w * opt["attr_w"]
        log.append("Attractors: {} new destinations (weight {} each){}.".format(
            sum(add_w.values()), opt["attr_w"], "; WARNING: {} further than {:.0f} m from any street or spine".format(
                far_aw, opt["snap"]) if far_aw else ""))
    V = {}
    V["walk_b"], CH_wb = potential(pieces, walk_b, o_w, d_w, opt, False, "Walking today", log)
    if has_prop or attractors:
        V["walk_a"], CH_wa = potential(pieces, walk_a, o_w, d_wa, opt, False, "Walking with the spine", log)
    else:
        V["walk_a"], CH_wa = V["walk_b"], CH_wb
    V["car_b"], CH_cb = potential(pieces, car_b, o_c, d_c, opt, True, "Driving today", log)
    if car_changes or (attractors and d_ca != d_c):
        V["car_a"], CH_ca = potential(pieces, car_a, o_c, d_ca, opt, True, "Driving with the spine", log)
    else:
        V["car_a"], CH_ca = V["car_b"], CH_cb
        log.append("Driving with the spine: the proposal changes no street for cars, so it equals today.")
    # pieces inside the frame, the indices (100 = busiest piece in the frame today, per mode)
    inside = [i for i, p in enumerate(pieces)
              if F.inside((xy[p["a"]][0] + xy[p["b"]][0]) / 2.0, (xy[p["a"]][1] + xy[p["b"]][1]) / 2.0)]
    mx_w = max([V["walk_b"].get(i, 0) for i in inside] or [0])
    mx_c = max([V["car_b"].get(i, 0) for i in inside] or [0])
    mix = opt["mix"]
    IDX = dict((k, {}) for k in ("walk_b", "walk_a", "car_b", "car_a", "comb_b", "comb_a"))
    for i in inside:
        for k, mx in (("walk_b", mx_w), ("walk_a", mx_w), ("car_b", mx_c), ("car_a", mx_c)):
            IDX[k][i] = 100.0 * V[k].get(i, 0) / mx if mx else 0.0
        IDX["comb_b"][i] = mix * IDX["walk_b"][i] + (1.0 - mix) * IDX["car_b"][i]
        IDX["comb_a"][i] = mix * IDX["walk_a"][i] + (1.0 - mix) * IDX["car_a"][i]
    log.append("Index 100 = walking {} route pairs, driving {} route pairs (the busiest piece inside the frame today)."
               .format(mx_w, mx_c))
    return dict(pieces=pieces, xy=xy, V=V, IDX=IDX, inside=inside, mx_w=mx_w, mx_c=mx_c, has_prop=has_prop,
                car_changes=car_changes, chains=dict(walk_b=CH_wb, walk_a=CH_wa, car_b=CH_cb, car_a=CH_ca))


def street_table(ns, S, R, log):
    """Named streets in the frame: shops (selinus_board build_corridors) and the length-weighted mean index of every
    map. Plus the checks: Spearman of shops against potential, the board's primary spine, the KGM-counted roads."""
    pieces, xy, IDX = R["pieces"], R["xy"], R["IDX"]
    shops = {}
    try:
        ns["build_corridors"](S)
        for r in S.roads + S.paths:
            g = r.get("grp")
            if g and g["label"] != "an unnamed street":
                shops[g["label"]] = g["n"]
        prim = [g["label"] for g in S.corr_primary]
    except Exception as ex:
        prim = []
        log.append("WARNING: selinus_board build_corridors failed ({}): no shop counts.".format(ex))
    acc = {}
    for i in R["inside"]:
        p = pieces[i]
        nm = (p["tags"].get("name") or "").strip()
        if not nm or p["prop"]:
            continue
        a = acc.setdefault(nm, dict(L=0.0, hw={}, s=dict((k, 0.0) for k in IDX)))
        a["L"] += p["L"]
        hw = p["tags"].get("highway", "")
        a["hw"][hw] = a["hw"].get(hw, 0.0) + p["L"]
        for k in IDX:
            a["s"][k] += IDX[k].get(i, 0.0) * p["L"]
    rows = []
    for nm, a in acc.items():
        if a["L"] < 1.0:
            continue
        m = dict((k, a["s"][k] / a["L"]) for k in IDX)
        rows.append(dict(name=nm, L=a["L"], hw=max(a["hw"], key=a["hw"].get), shops=shops.get(nm, 0), **m))
    rows.sort(key=lambda r: -r["comb_b"])
    big = [r for r in rows if r["L"] >= 50.0]
    log.append("")
    log.append("Named streets in the frame: {} ({} at least 50 m long, used for the checks).".format(len(rows), len(big)))
    for k, lab in (("walk_b", "walking"), ("car_b", "driving"), ("comb_b", "combined")):
        rho = spearman([r["shops"] for r in big], [r[k] for r in big])
        log.append("Shops per street vs {} potential today: Spearman {} (n = {}).".format(
            lab, "n/a" if rho is None else "{:.2f}".format(rho), len(big)))
    for nm in prim:
        for k, lab in (("walk_b", "walking"), ("car_b", "driving"), ("comb_b", "combined")):
            order = sorted(big, key=lambda r: -r[k])
            pos = next((j + 1 for j, r in enumerate(order) if r["name"] == nm), None)
            log.append("Board's primary spine {}: rank {} of {} by {} potential today.".format(
                nm, pos if pos else "n/a (under 50 m in the frame)", len(order), lab))
    # KGM-counted roads (selinus_board v18 COUNTED) against driving potential
    rc = ns.get("road_count")
    if rc:
        seen = {}
        for i in R["inside"]:
            p = pieces[i]
            if p["prop"]:
                continue
            c_ = rc(p["tags"])
            if c_:
                s_ = seen.setdefault(c_["src"], [c_["aadt"], 0.0, 0.0])
                s_[1] += IDX["car_b"].get(i, 0.0) * p["L"]
                s_[2] += p["L"]
        if seen:
            for src, (aadt, s_, L_) in sorted(seen.items()):
                log.append("KGM count in the frame: {} | driving index here today {:.2f} (mean over {:.0f} m).".format(
                    src, s_ / L_ if L_ else 0.0, L_))
            if len(seen) < 3:
                log.append("Too few counted roads in the frame to test the driving potential against counts.")
        else:
            log.append("No KGM-counted road runs inside the frame.")
    return rows


PANELS = (
    ("walk_b", "seq", "WALKING TODAY", "walk"), ("walk_a", "seq", "WALKING WITH THE STREAM-EDGE SPINE", "walk"),
    ("walk_d", "div", "WALKING: CHANGE WITH THE SPINE", "walk"),
    ("car_b", "seq", "DRIVING TODAY", "car"), ("car_a", "seq", "DRIVING WITH THE STREAM-EDGE SPINE", "car"),
    ("car_d", "div", "DRIVING: CHANGE WITH THE SPINE", "car"),
    ("comb_b", "seq", "COMBINED (WALKING + DRIVING) TODAY", "comb"),
    ("comb_a", "seq", "COMBINED WITH THE STREAM-EDGE SPINE", "comb"),
    ("comb_d", "div", "COMBINED: CHANGE WITH THE SPINE", "comb"))


MV_PAR = {"n": max(1, os.cpu_count() or 1)}           # worker processes for the route searches (one per core)
# Movement options of bergama_movement v1 (its defaults; parameters, not data; printed in the drawing's method line)
MV_OPT = dict(r_walk=800.0, t_car=600.0, buffer=1000.0, snap=150.0, snap_end=25.0, mix=0.5, attr_w=1)
PROPOSAL_INPUTS = ("spine", "spine_car", "bridges", "car_closed", "attractors")
# v34: the riverside spine of bergama_city_link (Thread 4), used when no proposal curves are wired. The file wins; the
# built-in copy (city link v1.1, 24 Oct; pieces A and C side "auto" = the bank the data picks) is the fallback. Survey coordinates; offsets are schematic for the network.
CITY_LINK_FILE = bg_first([os.path.join(bg_cache("Bergama_city_link_analysis"), "city_link_results.json"),   # v44
                           os.path.join(BERGAMA_DIR, "output", "Bergama_city_link_analysis", "city_link_results.json")])
CITY_LINK_DEFAULT = json.loads('{"spine":[{"id":"A","name":"Ulu Cami to K3 bank walk","frm":[29846.0,32278.0],"to":[30037.0,32122.0],"side_ref":[29844.2,32313.3],"offset_m":15.0,"side":"auto","catch_m":250.0},{"id":"B","name":"Junction over the covered reach","frm":[30037.0,32122.0],"to":[30238.7,31931.2],"side_ref":null,"offset_m":0.0},{"id":"C","name":"Red Hall to Üç Kemer bank walk","frm":[30238.7,31931.2],"to":[30294.0,31792.0],"side_ref":[30245.0,31962.0],"offset_m":15.0,"side":"auto","catch_m":250.0}],"functions":[{"n":1,"name":"Bank bazaar","xy":[29890.4,32243.6],"stage":null},{"n":2,"name":"Parchment and leather workshops","xy":[30062.0,32106.0],"stage":null},{"n":3,"name":"Junction square","xy":[30058.0,32047.0],"stage":null},{"n":4,"name":"Red Hall water terrace","xy":[30238.7,31931.2],"stage":null},{"n":5,"name":"Producers\' market","xy":[30294.0,31792.0],"stage":null},{"n":6,"name":"Study terraces","xy":[29941.0,32200.0],"stage":null},{"n":7,"name":"Clean-water classroom","xy":null,"stage":"entry"},{"n":8,"name":"Summer bed events","xy":null,"stage":null}]}')
CITY_LINK_MV = os.path.join(SELINUS_RES_DIR, "city_link_movement.json")      # v44: cached/
# OSM highway -> line class on the S2 plan (the road classes of bergama_diagrams D3); print mm
MV_CLASS = {"primary": "main", "trunk": "main", "secondary": "main", "tertiary": "secondary",
            "unclassified": "secondary"}
MV_W = {"main": 0.85, "secondary": 0.55, "lane": 0.3}
# the walks of D7: function, letter, colour (D5 / D4 / D2 palette colours of bergama_diagrams)
WALK_FUN = [("health", "H", "4C3349", "Health"), ("education", "E", "F4C178", "Education"),
            ("civic", "C", "8C7088", "Civic"), ("worship", "W", "8B3A3F", "Worship"),
            ("market", "M", "BC6F45", "Food & market"), ("park", "P", "8C9969", "Park"),
            ("heritage", "A", "4C2528", "Heritage")]
# working areas named by place, upstream to downstream (Q16: no owner names on the drawings)
STAGES = [("upstream entry", "entry"), ("K4 bridge", "K4"), ("K5 bridge", "K5"), ("downstream end", "end")]


def _xy_of(x):
    """A point input as (x, y) in file coordinates, or None."""
    g = x
    for _ in range(3):
        if hasattr(g, "X") and hasattr(g, "Y"):
            return (float(g.X), float(g.Y))
        if hasattr(g, "Location"):
            return (float(g.Location.X), float(g.Location.Y))
        if not hasattr(g, "Value"):
            break
        g = g.Value
    try:
        o = doc.Objects.FindId(g if isinstance(g, System.Guid) else System.Guid(str(g)))
        p = o.Geometry.Location
        return (float(p.X), float(p.Y))
    except Exception:
        return None


def city_link_spine(S):
    """v34: the riverside spine and its stops from bergama_city_link: (props, attractors, source). Each spine piece
    follows the main Selinus line between the chainages of its two anchors, offset_m to the side of side_ref
    (0 = on the line, over the covered reach); a piece whose anchors lie over 80 m from the line is a straight line."""
    spec, src = None, "built-in copy of 24 Oct (city link file not found)"
    try:
        with open(CITY_LINK_FILE, "r", encoding="utf-8") as fh:
            spec = json.load(fh)
        src = "city link file of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(CITY_LINK_FILE)))
    except Exception:
        spec = CITY_LINK_DEFAULT
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    main = max(streams, key=pl_length) if streams else None
    props, attr, votes = [], [], []
    for pc in spec.get("spine", []):
        a, b = tuple(pc["frm"]), tuple(pc["to"])
        P = None
        if main and min(_proj(a, p, q)[1] for p, q in zip(main[:-1], main[1:])) < 80.0 \
                and min(_proj(b, p, q)[1] for p, q in zip(main[:-1], main[1:])) < 80.0:
            s0, s1 = pl_chainage(main, a[0], a[1]), pl_chainage(main, b[0], b[1])
            sgn = 0.0
            if pc.get("side_ref") and float(pc.get("offset_m", 0)) > 0:
                r = pc["side_ref"]
                q, t = pl_point_at(main, pl_chainage(main, r[0], r[1]))
                sgn = 1.0 if t[0] * (r[1] - q[1]) - t[1] * (r[0] - q[0]) > 0 else -1.0
                if pc.get("side") == "auto":                # v34: the bank the data picks (spine_bank_vote)
                    sgn, vote = spine_bank_vote(S, main, s0, s1, sgn, float(pc.get("catch_m", 250.0)))
                    votes.append(dict(vote, id=pc.get("id")))
                elif pc.get("side") == "SW":
                    sgn = -sgn
            off = sgn * float(pc.get("offset_m", 0))
            n = max(2, int(abs(s1 - s0) // 10.0) + 1)
            P = []
            for k in range(n + 1):
                q, t = pl_point_at(main, s0 + (s1 - s0) * k / float(n))
                P.append((q[0] - t[1] * off, q[1] + t[0] * off))
        if not P:
            P = [a, b]
        props.append(("spine", P, True))
    stages = dict((sh, a_) for nm, sh, a_ in stage_areas(S))
    for f in spec.get("functions", []):
        if f.get("xy"):
            attr.append((float(f["xy"][0]), float(f["xy"][1])))
        elif f.get("stage") in stages:
            attr.append(tuple(shoelace(stages[f["stage"]]["P"])[1:]))
    S.city_link_votes = votes
    return props, attr, src


def spine_bank_vote(S, main, s0, s1, sgn_ne, catch):
    """v34: which bank a spine piece runs on, from the board's buildings (survey floors; unlabelled ones inferred
    from their 5 nearest, as the density drawings). Per bank, within `catch` m of the stream between chainages s0
    and s1: people = floors of homes and mixed use (a proxy: footprints not weighted), modern = buildings of 3 or more
    floors. The bank with more of both wins; if they split, modern decides when the people differ by under 10 %,
    else people. Returns (sign, vote); sign +1 = left of the flow; sgn_ne = the sign of the north-east bank."""
    lo, hi = min(s0, s1), max(s0, s1)
    segs = list(zip(main[:-1], main[1:]))
    acc = {1.0: [0, 0, 0], -1.0: [0, 0, 0]}               # buildings, people (floors), modern
    for u in getattr(S, "bld", []) or []:
        if u.get("annex") or u.get("src") == "shed" or not u.get("floors"):
            continue
        x, y = u["cx"], u["cy"]
        if min(_proj((x, y), a, b)[1] for a, b in segs) > catch:
            continue
        ch = pl_chainage(main, x, y)
        if not lo <= ch <= hi:
            continue
        q, t = pl_point_at(main, ch)
        sg = 1.0 if t[0] * (y - q[1]) - t[1] * (x - q[0]) > 0 else -1.0
        a_ = acc[sg]
        a_[0] += 1
        if u.get("cat") in ("residential", "mixed"):
            a_[1] += int(u["floors"])
        if int(u["floors"]) >= 3:
            a_[2] += 1
    ne, sw = acc[sgn_ne], acc[-sgn_ne]
    if ne[1] >= sw[1] and ne[2] >= sw[2]:
        win, why = sgn_ne, "more people and more modern buildings"
    elif sw[1] >= ne[1] and sw[2] >= ne[2]:
        win, why = -sgn_ne, "more people and more modern buildings"
    elif abs(ne[1] - sw[1]) < 0.10 * max(ne[1], sw[1], 1):
        win, why = (sgn_ne if ne[2] > sw[2] else -sgn_ne), "people within 10 %, more modern buildings"
    else:
        win, why = (sgn_ne if ne[1] > sw[1] else -sgn_ne), "more people (the banks split on modern buildings)"
    return win, dict(bank="NE" if win == sgn_ne else "SW", why=why, catch_m=catch,
                     NE=dict(buildings=ne[0], people_floors=ne[1], modern_3plus=ne[2]),
                     SW=dict(buildings=sw[0], people_floors=sw[1], modern_3plus=sw[2]))


def mv_proposal(S):
    """The proposal curves and points wired into the board (all optional), in survey coordinates. v34: with none
    wired, the riverside spine of bergama_city_link (city_link_spine)."""
    props, closed, attr = [], [], []
    for nm, kind in (("spine", "spine"), ("spine_car", "spine_car"), ("bridges", "bridge"), ("car_closed", None)):
        for x in as_list(inp(nm, [])):
            c = as_curve(x)
            if c is None:
                LOG.append("WARNING: {}: a value that is not a curve; left out.".format(nm))
                continue
            P = [T_apply(S.I, a, b) for a, b in curve_points(c)]
            P = [p for k, p in enumerate(P) if k == 0 or math.hypot(p[0] - P[k - 1][0], p[1] - P[k - 1][1]) > 1e-6]
            if len(P) < 2:
                continue
            if kind is None:
                closed.append(P)
            else:
                props.append((kind, P, kind != "bridge"))
    for x in as_list(inp("attractors", [])):
        p = _xy_of(x)
        if p is None:
            LOG.append("WARNING: attractors: a value that is not a point; left out.")
        else:
            attr.append(T_apply(S.I, p[0], p[1]))
    S.city_link = None
    if not props and not closed and not attr:             # v34: nothing wired -> the city link spine and stops
        try:
            props, attr, src = city_link_spine(S)
            S.city_link = dict(props=props, attr=attr, src=src)
            LOG.append("Riverside spine: {} pieces and {} stops from the {}.".format(len(props), len(attr), src))
            for v_ in getattr(S, "city_link_votes", []) or []:
                LOG.append("Spine piece {}: {} bank ({}; NE {} / SW {} home floors, {} / {} buildings of 3+ floors, "
                           "within {:.0f} m).".format(v_["id"], v_["bank"], v_["why"], v_["NE"]["people_floors"],
                                                      v_["SW"]["people_floors"], v_["NE"]["modern_3plus"],
                                                      v_["SW"]["modern_3plus"], v_["catch_m"]))
        except Exception:
            LOG.append("WARNING: the city link spine failed, so no proposal:\n" + traceback.format_exc())
            props, attr = [], []
    return props, closed, attr


def movement(S):
    """Movement potential of bergama_movement v1 (merged here, v33): every street piece's count of shortest routes
    between buildings and everyday destinations, walking and driving, today and (when proposal curves are wired)
    with the proposal. Once per run; S.mv = dict(R, rows, rho) or {} when there is no OSM file."""
    if getattr(S, "mv", None) is not None:
        return S.mv
    S.mv = {}
    osm = getattr(S, "osm", None)
    if not osm:
        LOG.append("Movement potential: no osm_path, so not computed.")
        return S.mv
    t0 = time.time()
    log = []
    props, closed, attr = mv_proposal(S)
    ns = dict(globals())
    if getattr(S, "corr_primary", None) is not None:
        ns["build_corridors"] = lambda S_: None              # the board has built its spines already
    R = analyse(ns, S, osm, PLACES_PATH or None, props, closed, attr, MV_OPT, log)
    rows = street_table(ns, S, R, log)
    big = [r for r in rows if r["L"] >= 50.0]
    rho = dict((k, spearman([r["shops"] for r in big], [r[k] for r in big])) for k in ("walk_b", "car_b", "comb_b"))
    S.mv = dict(R=R, rows=rows, big=big, rho=rho, props=props, closed=closed, attr=attr)
    try:
        write_city_link_movement(S, R)                     # v34: for bergama_city_link's page 1
    except Exception:
        LOG.append("WARNING: city_link_movement.json not written:\n" + traceback.format_exc())
    LOG.append("Movement potential ({:.0f} s): ".format(time.time() - t0) + " ".join(l_ for l_ in log if l_))
    return S.mv


