# ---- planting.py (round 5 S4, 1 Nov 2026; G-R5-7, P18.2, P23.2, P24.4; PLAN §3 "Planting placer") ------------------
# ONE placer for planting in plan, used by every plan that plants (masterplan p23/p24, water board p18 ...). Include it
# after plants.py (it calls PLA_NICHE, _pla_pick, _pla_rowlike, PLA_SPECIES, pla_plan).
# What it does (Aras U53-U55, U60, U61; target refs/T02 = the round 3 copse method of pl23_tree_set, CHK-5):
#   * the whole project is designed; intensity I fades from the cores (S23 red, I = 1) outward with no hard edge
#     (smoothstep over PLN_FADE_M), the outer designed areas (S23 blue) keep a lighter designed level PLN_OUTER that
#     ramps in from their edge, the rest of the project a floor PLN_FLOOR (meadow, scattered groves);
#   * outside the project nothing at all (outside_project 0, checked and logged);
#   * trees come in copses: copse centres by dart throwing (never a grid), spaced PLN_COPSE_M (near at I = 1, far at
#     the floor), 2-6 trees per copse jittered round the centre, at least 0.85 x their mean crown apart, any tree that
#     would continue a straight evenly spaced line rejected (_pla_rowlike: no rows); shrub drifts round the copses;
#   * species by the wet -> dry niche band (PLA_NICHE: t = distance to the water edge / PLN_WET_BAND_M), each copse led
#     by one species with others mixed in (never two species alternating, never uniform clumps);
#   * nothing on water or in `avoid` rings (paths, squares, buildings).
# Units: any plan unit; k = units per metre (survey m: k = 1; page mm: k = mm per m). Rings = lists of (x, y).
#   pln_place(project, cores=(), outer=(), water=(), k=1.0, seed=0, mix=None, density=1.0, avoid=(), max_n=4000,
#             page="", shrubs=True) -> dict(trees=[(key, x, y, crown_m, I)], shrubs=[...], counts={...})
#   pln_intensity_fn(project, cores, outer, k) -> I(x, y)   (0 outside the project)
#   pln_draw(placed, k, season=None, month=None) -> house shapes (pla_plan per plant, shrubs first, big crowns last)
#   pln_log_lines(page=None) -> ["planting <page> core n / edge n / outside n", "outside_project 0", ...]
import math as _pln_m

PLN_FADE_M = 60.0          # m: core -> outer fade length (drawing rule)
PLN_OUTER = 0.35           # intensity inside the outer designed areas (drawing rule)
PLN_OUTER_RAMP_M = 25.0    # m: the outer level ramps in over this distance from the outer area's edge (no hard edge)
PLN_FLOOR = 0.12           # intensity in the rest of the project (lightly designed; drawing rule)
PLN_COPSE_M = (14.0, 46.0) # m: copse centre spacing at I = 1 and at I = 0 (drawing rule, T02 copses >= 42 m apart)
PLN_COPSE_N = (2, 6)       # trees per copse at I = 0 / I = 1 (T02: 2-4; cores denser)
PLN_COPSE_R_M = 9.0        # m: trees within this radius of their copse centre (T02 "within 9 m")
PLN_WET_BAND_M = 60.0      # m: niche t = 0 at the water edge to 1 at this distance (drawing rule)
PLN_CORE_I = 0.80          # I at or above = "core" in the log
PLN_LOG = []
_PLN_COUNTS = {}


def _pln_rng(seed):
    s = [int(seed * 2654435761 + 1013) & 0x7fffffff]

    def r():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7fffffff
        return s[0] / float(0x7fffffff)
    return r


def _pln_ss(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


class _PlnRings(object):
    """rings with bounding boxes: point-in (even-odd over all rings) and distance to the nearest edge (bucketed)"""

    def __init__(self, rings, cell):
        self.rings = [list(r) for r in (rings or ()) if len(r) >= 3]
        self.bb = [(min(p[0] for p in r), min(p[1] for p in r), max(p[0] for p in r), max(p[1] for p in r))
                   for r in self.rings]
        self.cell = max(cell, 1e-6)
        self.grid = {}
        for r in self.rings:
            n = len(r)
            for i in range(n):
                a, b = r[i], r[(i + 1) % n]
                c = self.cell
                for gx in range(int(_pln_m.floor(min(a[0], b[0]) / c)), int(_pln_m.floor(max(a[0], b[0]) / c)) + 1):
                    for gy in range(int(_pln_m.floor(min(a[1], b[1]) / c)), int(_pln_m.floor(max(a[1], b[1]) / c)) + 1):
                        self.grid.setdefault((gx, gy), []).append((a, b))

    def inside(self, p):
        """True when p is inside the rings (even-odd: holes given as rings stay open)"""
        x, y = p
        hit = False
        for r, (x0, y0, x1, y1) in zip(self.rings, self.bb):
            if x < x0 or x > x1 or y < y0 or y > y1:
                continue
            j = len(r) - 1
            for i in range(len(r)):
                xi, yi = r[i]
                xj, yj = r[j]
                if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi:
                    hit = not hit
                j = i
        return hit

    def dist(self, p, dmax):
        """distance from p to the nearest edge, at most dmax"""
        if not self.rings:
            return dmax
        c = self.cell
        gx, gy = int(_pln_m.floor(p[0] / c)), int(_pln_m.floor(p[1] / c))
        rr = int(dmax / c) + 1
        best = dmax
        for ix in range(gx - rr, gx + rr + 1):
            for iy in range(gy - rr, gy + rr + 1):
                for a, b in self.grid.get((ix, iy), ()):
                    dx, dy = b[0] - a[0], b[1] - a[1]
                    L2 = dx * dx + dy * dy
                    t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
                    d = _pln_m.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
                    if d < best:
                        best = d
        return best


def pln_intensity_fn(project, cores=(), outer=(), k=1.0):
    """I(x, y): 0 outside the project; 1 in a core, fading by smoothstep over PLN_FADE_M from the core edge; the
    outer areas at least PLN_OUTER (ramped in over PLN_OUTER_RAMP_M from their edge); elsewhere PLN_FLOOR"""
    P = _PlnRings(project, PLN_FADE_M * k)
    C = _PlnRings(cores, PLN_FADE_M * k)
    O = _PlnRings(outer, PLN_OUTER_RAMP_M * k)

    def I(x, y):
        p = (x, y)
        if not P.inside(p):
            return 0.0
        if C.rings and C.inside(p):
            return 1.0
        v = PLN_FLOOR
        if C.rings:
            v = max(v, _pln_ss(1.0 - C.dist(p, PLN_FADE_M * k) / (PLN_FADE_M * k)))
        if O.rings and O.inside(p):
            v = max(v, PLN_FLOOR + (PLN_OUTER - PLN_FLOOR) *
                    _pln_ss(O.dist(p, PLN_OUTER_RAMP_M * k) / (PLN_OUTER_RAMP_M * k)))
        return v
    return I


class _PlnHash(object):
    def __init__(self, cell):
        self.c, self.g = max(cell, 1e-6), {}

    def add(self, p, v):
        self.g.setdefault((int(_pln_m.floor(p[0] / self.c)), int(_pln_m.floor(p[1] / self.c))), []).append((p, v))

    def near(self, p, r):
        n = int(r / self.c) + 1
        gx, gy = int(_pln_m.floor(p[0] / self.c)), int(_pln_m.floor(p[1] / self.c))
        out = []
        for ix in range(gx - n, gx + n + 1):
            for iy in range(gy - n, gy + n + 1):
                for q, v in self.g.get((ix, iy), ()):
                    if _pln_m.hypot(q[0] - p[0], q[1] - p[1]) <= r:
                        out.append((q, v))
        return out


def _pln_keys(mix):
    keys = list(mix) if mix else [k_ for k_ in PLA_NICHE]
    return [k_ for k_ in keys if k_ in PLA_NICHE]


def pln_place(project, cores=(), outer=(), water=(), k=1.0, seed=0, mix=None, density=1.0, avoid=(), max_n=4000,
              page="", shrubs=True):
    """the planting of a plan (see the module notes). project / cores / outer / water / avoid = rings in plan units;
    k = plan units per m; mix = {species: weight} limits and weights the species (default every PLA_NICHE species);
    density scales the number of copses. Returns dict(trees, shrubs, counts) with plants (key, x, y, crown_m, I)."""
    rnd = _pln_rng(seed)
    I = pln_intensity_fn(project, cores, outer, k)
    Pj = _PlnRings(project, PLN_FADE_M * k)
    W = _PlnRings(water, PLN_WET_BAND_M * k)
    A = _PlnRings(avoid, 20.0 * k)
    keys = _pln_keys(mix)

    def ok_ground(p):
        return Pj.inside(p) and not (W.rings and W.inside(p)) and not (A.rings and A.inside(p))

    def niche_t(p):
        return W.dist(p, PLN_WET_BAND_M * k) / (PLN_WET_BAND_M * k) if W.rings else 0.5

    def crown(key_):
        return float(PLA_SPECIES[key_]["crown_m"] or 3.0) * (0.88 + 0.20 * rnd())
    if not Pj.rings:
        return dict(trees=[], shrubs=[], counts=dict(core=0, edge=0, outside=0))
    x0 = min(b[0] for b in Pj.bb)
    y0 = min(b[1] for b in Pj.bb)
    x1 = max(b[2] for b in Pj.bb)
    y1 = max(b[3] for b in Pj.bb)
    area = (x1 - x0) * (y1 - y0)
    tries = int(min(60000, 3.0 * area / ((PLN_COPSE_M[0] * k) ** 2) * max(0.2, density)))
    centres = _PlnHash(PLN_COPSE_M[1] * k)
    trees = _PlnHash(PLN_COPSE_R_M * k)
    shrub_h = _PlnHash(4.0 * k)
    T, S = [], []
    for _ in range(tries):
        if len(T) >= max_n:
            break
        c = (x0 + rnd() * (x1 - x0), y0 + rnd() * (y1 - y0))
        if not ok_ground(c):
            continue
        Ic = I(c[0], c[1])
        if rnd() > min(1.0, Ic * density * 1.6):       # fewer copses where the design is lighter
            continue
        sp = (PLN_COPSE_M[0] + (PLN_COPSE_M[1] - PLN_COPSE_M[0]) * (1.0 - Ic)) * k
        if centres.near(c, sp):
            continue
        centres.add(c, sp)
        t = niche_t(c)
        lead = _pla_pick(t, rnd, keys, mix if isinstance(mix, dict) else None, True)
        if lead is None:                               # no tree at home here (wet edge): shrubs / emergents only
            n = 0
        else:
            n = int(round(PLN_COPSE_N[0] + (PLN_COPSE_N[1] - PLN_COPSE_N[0]) * Ic + (rnd() - 0.5)))
        placed = 0
        for _j in range(n * 4):
            if placed >= n:
                break
            a, r = 2.0 * _pln_m.pi * rnd(), PLN_COPSE_R_M * k * (0.15 + 0.85 * rnd() ** 0.5)
            p = (c[0] + r * _pln_m.cos(a), c[1] + r * _pln_m.sin(a))
            if not ok_ground(p):
                continue
            key_ = lead if rnd() < 0.7 else (_pla_pick(niche_t(p), rnd, keys, mix if isinstance(mix, dict) else None,
                                                       True) or lead)
            cw = crown(key_)
            if any(_pln_m.hypot(q[0] - p[0], q[1] - p[1]) < 0.85 * 0.5 * (cw + v) * k for q, v in trees.near(p, 30.0 * k)):
                continue
            nb = [q for q, _v in trees.near(p, 3.0 * cw * k)]
            if len(nb) >= 2 and _pla_rowlike(p, nb, 3.0 * cw * k):
                continue
            trees.add(p, cw)
            T.append((key_, p[0], p[1], cw, I(p[0], p[1])))
            placed += 1
        if shrubs:                                      # shrub drift round the copse, its size by intensity
            m = int(round(1 + 4 * Ic * rnd()))
            for _j in range(m * 3):
                a, r = 2.0 * _pln_m.pi * rnd(), (PLN_COPSE_R_M + 2.0 + 8.0 * rnd()) * k
                p = (c[0] + r * _pln_m.cos(a), c[1] + r * _pln_m.sin(a))
                if not ok_ground(p):
                    continue
                key_ = _pla_pick(niche_t(p), rnd, keys, mix if isinstance(mix, dict) else None, False)
                if key_ is None or key_ in ("reed", "mint"):   # reed and mint: lined cells only (plants.py)
                    continue
                cw = crown(key_)
                if shrub_h.near(p, 0.9 * cw * k) or any(_pln_m.hypot(q[0] - p[0], q[1] - p[1]) < 0.5 * v * k
                                                         for q, v in trees.near(p, 15.0 * k)):
                    continue
                shrub_h.add(p, cw)
                S.append((key_, p[0], p[1], cw, I(p[0], p[1])))
    outside = sum(1 for pl in T + S if not Pj.inside((pl[1], pl[2])))
    core = sum(1 for pl in T + S if pl[4] >= PLN_CORE_I)
    counts = dict(core=core, edge=len(T) + len(S) - core - outside, outside=outside, trees=len(T), shrubs=len(S))
    _PLN_COUNTS[page or "-"] = counts
    return dict(trees=T, shrubs=S, counts=counts)


def pln_draw(placed, k, season=None, month=None):
    """house shapes of a placement (pla_plan per plant: shrubs first, then trees, bigger crowns last)"""
    sh = []
    for i, (key_, x, y, cw, _I) in enumerate(placed.get("shrubs", ())):
        sh += pla_plan(key_, x, y, k, crown_m=cw, seed=i * 7 + 3, season=season, month=month)
    for i, (key_, x, y, cw, _I) in enumerate(sorted(placed.get("trees", ()), key=lambda t: t[3])):
        sh += pla_plan(key_, x, y, k, crown_m=cw, seed=i * 11 + 1, season=season, month=month)
    return sh


def pln_log_lines(page=None):
    """"planting <page> core n / edge n / outside n" per page placed, then "outside_project <total outside>" """
    out = []
    tot = 0
    for pg, c in sorted(_PLN_COUNTS.items()):
        if page is not None and pg != page:
            continue
        out.append(u"planting %s core %d / edge %d / outside %d (trees %d, shrubs %d)" % (
            pg, c["core"], c["edge"], c["outside"], c["trees"], c["shrubs"]))
        tot += c["outside"]
    out.append(u"outside_project %d" % tot)
    return out
