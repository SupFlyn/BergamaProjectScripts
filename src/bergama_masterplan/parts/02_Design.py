class Design(object):
    def __init__(self, items, areas, warn, opt):
        self.zones, self.strips, self.links, self.removes, self.paths = [], [], [], [], []
        for it in items:
            lay = it["layer"].split("::")[-1]
            kind = item_kind(lay)
            m = it.get("meta") or {}
            P = [(float(p[0]), float(p[1])) for p in it["P"]]
            if kind is None or len(P) < 2:
                continue
            lab = (m.get("label") or "").upper()
            if kind in ("ZONE", "WATER", "REMOVE"):
                P = ring(P)
                if len(P) < 3:
                    continue
                if area2(P) < 0:
                    P = P[::-1]
                q = inner_pt(P)
                sa = next((k for k, A in areas.items() if pip(q[0], q[1], A)), None)    # v12: the calisma part
                own = (m.get("study_area") or "").split("[")[0]                      # v12: whose words it keeps
                z = {"P": P, "q": q, "area": sa, "own": own, "label": lab, "id": str(m.get("id", "")),
                     "tier": (m.get("zone") or "").upper()[:1], "m2": abs(area2(P)),
                     "code": lay.replace("INT_ZONE_", "")[:2].upper() if kind == "ZONE" else ""}
                if kind == "ZONE" and any(w in lab for w in DROPPED):
                    continue                     # no farmland or farm channel inside the site (CONTEXT §2)
                {"ZONE": self.zones, "WATER": self.strips, "REMOVE": self.removes}[kind].append(z)
            elif kind == "PATH":
                sa = next((k for k, A in areas.items() if any(pip(p[0], p[1], A) for p in P)), None)
                self.paths.append({"P": P, "area": sa, "own": (m.get("study_area") or "").split("[")[0],
                                   "label": lab or u"PATH"})
            else:
                lk = link_type(m.get("link") or lay[len("INT_LINK_"):]) or "other"
                self.links.append({"P": P, "kind": lk, "label": lab,
                                   "heads": LINK_TYPES[lk]["heads"] if lk in LINK_TYPES else 1})


def zone_tones(z):
    lt, md, dk = MP.get(CODE_FAMILY.get(z["code"], "park"))
    if z["code"] == "WA" and z["tier"] == "F":
        lt = mix(lt, COL["white"], 0.5)
    return lt, md, dk


# ================================================================ the base of a drawing (v2.3)
class Near(object):
    """Fast 'inside the working area' and 'within r m of it' tests (edges bucketed in r-sized cells)."""

    def __init__(self, P, r):
        self.P, self.r = P, r
        self.c = c = max(r, 10.0)
        self.cells, self.memo = {}, {}
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            for gi in range(int(math.floor(min(a[0], b[0]) / c)), int(math.floor(max(a[0], b[0]) / c)) + 1):
                for gj in range(int(math.floor(min(a[1], b[1]) / c)), int(math.floor(max(a[1], b[1]) / c)) + 1):
                    self.cells.setdefault((gi, gj), []).append((a, b))
        self.bb = bbox(P)

    def inside(self, x, y):
        b = self.bb
        if x < b[0] or x > b[2] or y < b[1] or y > b[3]:
            return False
        k = (int(math.floor(x / self.c)), int(math.floor(y / self.c)))
        if k not in self.cells:                          # no edge crosses this cell: one answer for all of it
            if k not in self.memo:
                self.memo[k] = pip(x, y, self.P)
            return self.memo[k]
        return pip(x, y, self.P)

    def within(self, x, y):
        b, r = self.bb, self.r
        if x < b[0] - r or x > b[2] + r or y < b[1] - r or y > b[3] + r:
            return False
        gi, gj = int(math.floor(x / self.c)), int(math.floor(y / self.c))
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                for a, e in self.cells.get((gi + di, gj + dj), ()):
                    if seg_dist(x, y, a, e) <= r:
                        return True
        return self.inside(x, y)


class View(object):
    """Alternative 3: the corridor of all working areas turned so its long axis runs left to right, the upstream
    entry on the left (the water runs left to right), plus the ring. Graphic: north is shown by an arrow."""

    def __init__(self, areas, ring_m, k, frame=None):
        pts = list(frame) if frame else [p for A in areas.values() for p in A]   # v15: frame = site_alan
        self.cx, self.cy = sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts)
        a = math.radians(principal_angle(pts))
        self.c, self.s = math.cos(a), math.sin(a)
        if "calisma_alan[0]" in areas and "calisma_alan[1]" in areas:     # v12: north part = upstream
            up = sum(self.uv(p)[0] for p in areas["calisma_alan[0]"]) / len(areas["calisma_alan[0]"])
            dn = sum(self.uv(p)[0] for p in areas["calisma_alan[1]"]) / len(areas["calisma_alan[1]"])
            if up > dn:
                self.c, self.s = -self.c, -self.s
        U = [self.uv(p) for p in pts]
        self.u0, self.u1 = min(u for u, v in U) - ring_m, max(u for u, v in U) + ring_m
        self.v0, self.v1 = min(v for u, v in U) - ring_m, max(v for u, v in U) + ring_m
        self.k = k
        self.W, self.H = (self.u1 - self.u0) * k, (self.v1 - self.v0) * k
        corners = [self.xy(u, v) for u, v in ((self.u0, self.v0), (self.u1, self.v0), (self.u1, self.v1),
                                              (self.u0, self.v1))]
        self.P = corners
        self.bb = bbox(corners)

    def uv(self, p):
        dx, dy = p[0] - self.cx, p[1] - self.cy
        return dx * self.c + dy * self.s, -dx * self.s + dy * self.c

    def xy(self, u, v):
        return self.cx + u * self.c - v * self.s, self.cy + u * self.s + v * self.c

    def T(self, p):
        u, v = self.uv(p)
        return (u - self.u0) * self.k, (v - self.v0) * self.k

    def inside(self, x, y):
        u, v = self.uv((x, y))
        return self.u0 <= u <= self.u1 and self.v0 <= v <= self.v1

    within = inside


def faces(polys, snap=0.02, max_area=30000.0):
    """Closed footprints from loose survey segments: the bounded faces of the planar graph (shared walls of row
    houses work; courtyards come out as faces too and are cut out by the even-odd fill)."""
    key = lambda p: (int(round(p[0] / snap)), int(round(p[1] / snap)))
    segs = [(a, b) for P in polys for a, b in zip(P[:-1], P[1:])]
    ends, G = {}, 5.0                                    # T-junctions: split a segment where another one ends on it
    for a, b in segs:
        for p in (a, b):
            ends.setdefault((int(p[0] // G), int(p[1] // G)), {})[key(p)] = p
    split = []
    for a, b in segs:
        ka, kb = key(a), key(b)
        L2 = (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2
        if L2 < snap * snap:
            continue
        on = []
        for gi in range(int(min(a[0], b[0]) // G), int(max(a[0], b[0]) // G) + 1):
            for gj in range(int(min(a[1], b[1]) // G), int(max(a[1], b[1]) // G) + 1):
                for kp, p in ends.get((gi, gj), {}).items():
                    if kp in (ka, kb):
                        continue
                    t = ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / L2
                    if 0.0 < t < 1.0 and seg_dist(p[0], p[1], a, b) <= snap:
                        on.append((t, p))
        pts = [a] + [p for t, p in sorted(on)] + [b]
        split += list(zip(pts[:-1], pts[1:]))
    pos, adj = {}, {}
    for a, b in split:
        ka, kb = key(a), key(b)
        if ka == kb:
            continue
        pos.setdefault(ka, a)
        pos.setdefault(kb, b)
        adj.setdefault(ka, set()).add(kb)
        adj.setdefault(kb, set()).add(ka)
    stack = [k for k, s in adj.items() if len(s) < 2]
    while stack:                                         # loose ends cannot bound a face
        k = stack.pop()
        s = adj.pop(k, None)
        for n in s or ():
            t = adj.get(n)
            if t is not None:
                t.discard(k)
                if len(t) < 2:
                    stack.append(n)
    order, idx = {}, {}
    for k, s in adj.items():
        x, y = pos[k]
        order[k] = sorted(s, key=lambda n: math.atan2(pos[n][1] - y, pos[n][0] - x))
        idx[k] = dict((n, i) for i, n in enumerate(order[k]))
    used, out = set(), []
    for u in order:
        for v in order[u]:
            if (u, v) in used:
                continue
            R, a, b = [], u, v
            while (a, b) not in used and len(R) < 20000:
                used.add((a, b))
                R.append(pos[a])
                nb = order[b]
                a, b = b, nb[(idx[b][a] - 1) % len(nb)]
            if 0.5 < area2(R) < max_area:
                out.append(R)
    return out


def cut_runs(P, test, step=LINE_STEP_M):
    """The parts of polyline P where test(x, y) holds, sampled every `step` m."""
    runs, run = [], []
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / step))
        for j in range(n + (1 if i == len(P) - 2 else 0)):
            t = j / float(n)
            p = (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))
            if test(p[0], p[1]):
                run.append(p)
            else:
                if len(run) >= 2:
                    runs.append(run)
                run = []
    if len(run) >= 2:
        runs.append(run)
    return runs


def prep_base(survey, nr, R, full=False):
    """The survey within test nr (a working area's ring, or the corridor of alternative 3) inside rectangle R:
    footprints as faces (whole when any corner is within), street and stream lines and the line work drawn on top,
    cut at the edge; full = also contours and bank lines (alternative 3)."""
    inR = lambda P: any(R[0] <= p[0] <= R[2] and R[1] <= p[1] <= R[3] for p in P)
    base = {"faces": {}, "lines": [], "streets": [], "streams": [], "contours": [], "contours10": [], "banks": []}
    for role, max_a in (("park", 400000.0), ("pond", 50000.0), ("housing", 30000.0), ("building", 30000.0),
                        ("heritage", 30000.0)):
        polys = [P for P in survey.get(role, []) if inR(P)]
        base["faces"][role] = [F for F in faces(polys, max_area=max_a) if any(nr.within(p[0], p[1]) for p in F)]
    for role in ("road", "kerb"):
        for P in survey.get(role, []):
            if inR(P):
                base["streets"] += cut_runs(P, nr.within)
    styles = {"histwall": ("histwall", 0.30, [1.2, 0.5]), "stream": ("river_mid", 0.22, None),
              "bridge": ("ink", 0.35, None)}
    for role in ("stream", "histwall", "bridge"):
        ck, lw, dash = styles[role]
        for P in survey.get(role, []):
            if inR(P):
                for r_ in cut_runs(P, nr.within):
                    base["lines"].append((ck, lw, dash, r_))
                    if role == "stream":
                        base["streams"].append(r_)
    if full:
        for role, key in (("contour", "contours"), ("contour10", "contours10"), ("bank", "banks"),
                          ("bank_top", "banks"), ("chan_top", "banks")):
            for P in survey.get(role, []):
                if inR(P):
                    base[key] += cut_runs(P, nr.within, 2.0)
    base["near"], base["R"] = nr, R
    return base


# ================================================================ links between shapes (v2.3)
def link_shapes(L, shapes, near=30.0):
    """The shape (zone or strip) a link starts in and the one it ends in (holding the end, else nearest)."""
    def at(e, skip=None):
        for z in shapes:
            if z is not skip and pip(e[0], e[1], z["P"]):
                return z
        best, bd = None, near
        for z in shapes:
            if z is skip:
                continue
            d = min(seg_dist(e[0], e[1], a, b) for a, b in zip(thin(z["P"]), thin(z["P"])[1:] + thin(z["P"])[:1]))
            if d < bd:
                best, bd = z, d
        return best
    a = at(L["P"][0])
    return a, at(L["P"][-1], skip=a)


# ================================================================ the flowing puzzle (v2.3; Nil 2026-10-18 19:00)
# Every space of the working area and its ring is one puzzle piece, grown on one grid from its surveyed or zone
# base shape. A piece spreads beyond its shape by GROW_M x its extroversion, with a front that wanders more the more
# extrovert it is (liquid); introvert pieces keep their shape (solid). Housing is closed: nothing enters it except the
# streets, which reach into it slowly. Where the zone base links two zones, the giving zone sends a tongue into the
# receiving one, so the pieces interlock. Graphic reading only: extroversion values are set in EXTRO, not measured.
# v10 (alternative 2): every programme piece is also grown on its own ("free"), so pieces overlap where they reach
# into each other; the cells most of them cover ("meet") carry the commons' words.

EXTRO = {  # kind: (extroversion 0 introvert ... 1 extrovert, legend)
    "river": (1.00, u"RIVER"),
    "W": (0.95, u"WET BED ZONES"), "F": (0.80, u"FLOOD TERRACE ZONES"), "D": (0.65, u"DRY TOP ZONES"),
    "cleared": (0.55, u"CLEARED GROUND"),
    "street": (0.60, u"STREETS"),
    "park": (0.50, u"PARKS"),
    "heritage": (0.30, u"HERITAGE"),
    "building": (0.12, u"OTHER BUILDINGS"),
    "housing": (0.00, u"HOUSING"),
}
FEED_BONUS = 0.08            # per zone base link a zone gives: the feeding zone flows outward more
GROW_M = 12.0                # how far the most extrovert piece spreads beyond its shape, m (graphic)
STREET_M = 4.5               # a street grows this far from its surveyed kerb / road lines, m (fills the carriageway)
HOUSING_CLOSE_M = 1.0        # housing grows this far: closes the gaps between joined houses into one solid block
TONGUE_M = 28.0              # longest tongue a giving zone sends into the zone it feeds, m
MAX_CELLS = 170000           # grid cells per working area (cell size follows from it, at least 0.5 m)
BAND_CELLS = 600000          # v18: grid cells of the corridor-wide grid of the broad zones of alternative 3
RIVER_BAND_M = 15.0          # v18: the river corridor reaches this far beyond the stream / bank lines, m (graphic default)
SPINE_ZONE_M = 10.0          # v18: a spine zone reaches this far either side of its route, m (graphic default)
BAND_E = 0.6                 # v18: how much the broad zones' edges wander (alternative 2's growth, 0-1)
RIVER_BAND_TONE = ("C4CCB5", "89986A", "3C4733")   # v18: sage, palette reference 89986A (light = mixed 1:1 with white)
RIVER_BAND_NAME = u"PROMENADE"   # v19: one catchy word for Aras's "function/circulation area" (16:39, 16:41)
RIVER_BAND_WORDS = [u"VIEWPOINTS", u"TERRACES", u"WALK PATHS", u"RAMPS", u"CAFES"]   # his words, 16:39
PIECE_TONE = {"river": ("91ADB4", "5D7F8D", "32525F"), "street": ("E6E3DC", "CFCCC5", "847E75"),
              "park": ("DFEBC0", "A7B67F", "49522B"), "heritage": ("E4CAC9", "AF7474", "4C2528"),
              "building": ("D8D5CC", "B0AC9C", "847E75"), "housing": ("D9CDAE", "BFB08F", "594B2E"),
              "cleared": ("F6F4EE", "B0AC9C", "4A3F35")}
FADE_RING = 0.55             # pieces in the ring (outside the working area) are mixed this much with white


def _noise(i):
    """A smooth wandering field for piece i (three crossing waves, deterministic)."""
    r = [math.sin((i + 1) * 12.9898 + j * 78.233) * 43758.5453 for j in range(9)]
    r = [x - math.floor(x) for x in r]
    W = [(2 * math.pi / (17.0 + 9.0 * r[0]), r[1] * 6.283, r[2] * 6.283),
         (2 * math.pi / (29.0 + 11.0 * r[3]), r[4] * 6.283, r[5] * 6.283),
         (2 * math.pi / (43.0 + 13.0 * r[6]), r[7] * 6.283, r[8] * 6.283)]
    D = [(math.cos(t), math.sin(t), w, ph) for w, t, ph in W]
    return lambda x, y: sum(math.sin(w * (cx * x + cy * y) + ph) for cx, cy, w, ph in D) / 3.0


class Grid(object):
    def __init__(self, R, nr, cells=MAX_CELLS):
        self.c = c = max(0.5, math.sqrt((R[2] - R[0]) * (R[3] - R[1]) / float(cells)))
        self.x0, self.y0 = R[0], R[1]
        self.nx, self.ny = int((R[2] - R[0]) / c) + 1, int((R[3] - R[1]) / c) + 1
        self.valid = bytearray(self.nx * self.ny)
        self.inside = bytearray(self.nx * self.ny)
        for j in range(self.ny):
            y = self.y0 + (j + 0.5) * c
            for i in range(self.nx):
                x = self.x0 + (i + 0.5) * c
                if nr.within(x, y):
                    self.valid[j * self.nx + i] = 1
                    if nr.inside(x, y):
                        self.inside[j * self.nx + i] = 1

    def xy(self, n):
        return self.x0 + (n % self.nx + 0.5) * self.c, self.y0 + (n // self.nx + 0.5) * self.c

    def poly_cells(self, P):
        """Cells whose centre lies in ring P (scanline)."""
        out = []
        b = bbox(P)
        j0, j1 = max(0, int((b[1] - self.y0) / self.c)), min(self.ny - 1, int((b[3] - self.y0) / self.c) + 1)
        E = list(zip(P, P[1:] + P[:1]))
        for j in range(j0, j1 + 1):
            y = self.y0 + (j + 0.5) * self.c
            xs = sorted(a[0] + (y - a[1]) * (e[0] - a[0]) / (e[1] - a[1]) for a, e in E
                        if (a[1] > y) != (e[1] > y))
            for k in range(0, len(xs) - 1, 2):
                i0 = max(0, int(math.ceil((xs[k] - self.x0) / self.c - 0.5)))
                i1 = min(self.nx - 1, int(math.floor((xs[k + 1] - self.x0) / self.c - 0.5)))
                out += range(j * self.nx + i0, j * self.nx + i1 + 1)
        return out

    def line_cells(self, P):
        out = set()
        for a, b in zip(P[:-1], P[1:]):
            n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / (self.c * 0.5)))
            for t in range(n + 1):
                x, y = a[0] + (b[0] - a[0]) * t / n, a[1] + (b[1] - a[1]) * t / n
                i, j = int((x - self.x0) / self.c), int((y - self.y0) / self.c)
                if 0 <= i < self.nx and 0 <= j < self.ny:
                    out.add(j * self.nx + i)
        return out


def zone_extro(z, n_out):
    return min(1.0, EXTRO.get(z["tier"] or "D", EXTRO["D"])[0] + FEED_BONUS * n_out)


def puzzle(base, D, key):
    """Grow all pieces of one working area on one grid -> list of pieces with their outline loops (world m): the
    partition (context, zone and hub pieces) and, for alternative 2, the free zone pieces and their meeting cells."""
    G = Grid(base["R"], base["near"])
    zones = [z for z in D.zones if z["area"] == key]
    strips = [s for s in D.strips if any(base["near"].within(p[0], p[1]) for p in thin(s["P"], 60))]
    removes = [r for r in D.removes if r["area"] == key]
    pieces = []

    def piece(kind, e, g, zone=None):
        pieces.append({"kind": kind, "e": e, "g": g, "zone": zone, "seeds": {}, "noise": _noise(len(pieces))})
        return pieces[-1]

    def seed(pc, cells, cost):
        s = pc["seeds"]
        for n in cells:
            if G.valid[n] and cost < s.get(n, 1e9):
                s[n] = cost
    gives = {}
    for L in D.links:
        a, b = link_shapes(L, zones + strips)
        if a is not None and b is not None and a is not b:
            gives.setdefault(id(a), []).append((b, L))
    fc = base["faces"]
    hs = piece("housing", EXTRO["housing"][0], HOUSING_CLOSE_M)
    for F in fc.get("housing", []):
        seed(hs, G.poly_cells(F), -hs["g"])
    bl = piece("building", EXTRO["building"][0], HOUSING_CLOSE_M)
    for F in fc.get("building", []):
        seed(bl, G.poly_cells(F), -bl["g"])
    for kind in ("heritage", "park"):
        e = EXTRO[kind][0]
        pc = piece(kind, e, e * GROW_M * 0.5)
        for F in fc.get(kind, []):
            seed(pc, G.poly_cells(F), -pc["g"])
    st = piece("street", EXTRO["street"][0], STREET_M)
    for P in base["streets"]:
        seed(st, G.line_cells(P), -st["g"])
    rv = piece("river", EXTRO["river"][0], EXTRO["river"][0] * GROW_M)
    for s in strips:
        seed(rv, G.poly_cells(s["P"]), -rv["g"])
    for P in base["streams"]:
        seed(rv, G.line_cells(P), -rv["g"] * 0.6)
    for F in fc.get("pond", []):
        seed(rv, G.poly_cells(F), -rv["g"] * 0.5)
    for r in removes:
        pc = piece("cleared", EXTRO["cleared"][0], EXTRO["cleared"][0] * GROW_M * 0.4)
        seed(pc, G.poly_cells(r["P"]), -pc["g"])
    zp = {}
    for z in zones:
        e = zone_extro(z, len(gives.get(id(z), [])))
        pc = piece("zone", e, e * GROW_M, z)
        seed(pc, G.poly_cells(z["P"]), -pc["g"])
        zp[id(z)] = pc
    for s in strips:
        zp[id(s)] = rv
    for z in zones + strips:                             # the giving zone reaches into the zone it feeds
        src = zp.get(id(z))
        for b, L in gives.get(id(z), []):
            TA, TB = thin(z["P"]), thin(b["P"])
            p, q, d = closest_pair(TA, TB)
            pa, pb = inner_pt(TA, 10), inner_pt(TB, 10)
            u = (pb[0] - pa[0], pb[1] - pa[1]) if d < 0.5 else (q[0] - p[0], q[1] - p[1])
            Lu = math.hypot(u[0], u[1]) or 1.0
            u = (u[0] / Lu, u[1] / Lu)
            ext = [x * u[0] + y * u[1] for x, y in TB]
            ln = min(TONGUE_M, 0.45 * (max(ext) - min(ext)))
            line = [(p[0] - u[0] * 3.0, p[1] - u[1] * 3.0), (q[0] + u[0] * ln, q[1] + u[1] * ln)]
            seed(src, G.line_cells(line), -src["g"] - 2.0)
    # ---- multi-source growth (Dijkstra on the grid): the lowest cost claims the cell
    N = G.nx * G.ny
    best = [1e18] * N
    lab = [-1] * N
    prot = bytearray(N)
    for n in hs["seeds"]:
        prot[n] = 1
    hp = []
    for li, pc in enumerate(pieces):
        for n, c0 in pc["seeds"].items():
            if c0 < best[n]:
                best[n], lab[n] = c0, li
    for n in range(N):
        if lab[n] >= 0:
            hp.append((best[n], n, lab[n]))
    heapq.heapify(hp)
    c, nx = G.c, G.nx
    nbr = [(1, 0, c), (-1, 0, c), (0, 1, c), (0, -1, c), (1, 1, c * 1.4142), (-1, 1, c * 1.4142),
           (1, -1, c * 1.4142), (-1, -1, c * 1.4142)]
    amp = [0.8 * pc["e"] for pc in pieces]
    street_i, housing_i = pieces.index(st), pieces.index(hs)
    while hp:
        cost, n, li = heapq.heappop(hp)
        if cost > best[n] or lab[n] != li:
            continue
        i, j = n % nx, n // nx
        x, y = G.xy(n)
        f = 1.0 + amp[li] * pieces[li]["noise"](x, y)
        for di, dj, w in nbr:
            ii, jj = i + di, j + dj
            if ii < 0 or jj < 0 or ii >= nx or jj >= G.ny:
                continue
            m = jj * nx + ii
            if not G.valid[m]:
                continue
            step = w * f
            if prot[m] and li != housing_i:
                if li != street_i:
                    continue                             # housing is closed to everything but the streets
                step *= 3.0
            nc = cost + step
            if nc < best[m] and nc <= 0.0:
                best[m], lab[m] = nc, li
                heapq.heappush(hp, (nc, m, li))
    # ---- the commons: programme cells within reach of 3 (else 2) programme pieces become one darker piece
    fn = [li for li, pc in enumerate(pieces) if pc["kind"] == "zone"]
    if len(fn) >= 2 and key in HUB:
        rv_i = pieces.index(rv)
        layers = int(HUB_R_M[0] / c) + 1
        dist = {}
        for li in fn + [rv_i]:
            d = bytearray([255]) * N
            fr = [n for n in range(N) if lab[n] == li]
            for n in fr:
                d[n] = 0
            for L_ in range(1, layers + 1):
                nf = []
                for n in fr:
                    i, j = n % nx, n // nx
                    for di, dj, _w in nbr:
                        ii, jj = i + di, j + dj
                        if 0 <= ii < nx and 0 <= jj < G.ny:
                            m = jj * nx + ii
                            if d[m] == 255:
                                d[m] = L_
                                nf.append(m)
                fr = nf
            dist[li] = d
        prog = [n for n in range(N) if lab[n] in fn and G.inside[n]]
        hub = []
        for need in (3, 2):
            for r_m in HUB_R_M:
                r = int(r_m / c)
                hub = [n for n in prog if sum(1 for li in dist if dist[li][n] <= r) >= need]
                if hub and len(hub) <= HUB_MAX * len(prog):
                    break
                hub = []
            if hub:
                break
        if hub:
            fam = {}
            for n in hub:
                f_ = MP[CODE_FAMILY.get(pieces[lab[n]]["zone"]["code"], "park")][1]
                fam[f_] = fam.get(f_, 0) + 1
            tot = float(sum(fam.values()))
            rgb = [sum(hex_rgb(f_)[q] * v for f_, v in fam.items()) / tot for q in range(3)]
            md = "".join("{:02X}".format(int(round(255 * x))) for x in rgb)
            dk = mix(md, COL["ink_dark"], 0.45)
            pieces.append({"kind": "hub", "e": 0.9, "zone": None, "tone": (dk, md, COL["white"]),
                           "name": HUB[key][0], "words": HUB[key][1]})
            hi = len(pieces) - 1
            for n in hub:
                lab[n] = hi
    # ---- v10, alternative 2: every programme piece grown on its own (same costs, housing still closed)
    free = {}
    for li in fn:
        bst = dict(pieces[li]["seeds"])
        hq = [(c0, n) for n, c0 in bst.items()]
        heapq.heapify(hq)
        while hq:
            cost, n = heapq.heappop(hq)
            if cost > bst.get(n, 1e18):
                continue
            i, j = n % nx, n // nx
            x, y = G.xy(n)
            f = 1.0 + amp[li] * pieces[li]["noise"](x, y)
            for di, dj, w in nbr:
                ii, jj = i + di, j + dj
                if ii < 0 or jj < 0 or ii >= nx or jj >= G.ny:
                    continue
                m = jj * nx + ii
                if not G.valid[m] or prot[m]:
                    continue
                nc = cost + w * f
                if nc <= 0.0 and nc < bst.get(m, 1e18):
                    bst[m] = nc
                    heapq.heappush(hq, (nc, m))
        free[li] = set(bst)
    cnt = {}
    for li, S_ in free.items():
        for n in S_:
            if G.inside[n]:
                cnt[n] = cnt.get(n, 0) + 1
    meet = []
    for need in (3, 2):
        meet = [n for n, v in cnt.items() if v >= need]
        if len(meet) * c * c >= HUB_MIN_M2:
            break
        meet = []
    # ---- outlines: one set of loops per piece and side (in the working area / in the ring)
    groups = {}
    for n in range(N):
        if lab[n] >= 0:
            groups.setdefault((lab[n], 1 if pieces[lab[n]]["kind"] in ("zone", "hub") else G.inside[n]),
                              []).append(n)
    out = []
    for li, pc in enumerate(pieces):
        for ins in (1, 0):
            cells = groups.get((li, ins))
            if not cells:
                continue
            loops = trace(G, set(cells))
            tol, it = (c * 0.6, 0) if pc["e"] < 0.2 else (c * 0.9, 2 if pc["e"] < 0.5 else 4)   # solid .. liquid
            loops = [smooth(Lp, tol, it) for Lp in loops if len(Lp) >= 4]
            loops = [Lp for Lp in loops if len(Lp) >= 3 and abs(area2(Lp)) >
                     (HUB_MIN_M2 if pc["kind"] == "hub" else 2.0 * c * c)]
            if loops:
                out.append({"kind": pc["kind"], "e": pc["e"], "zone": pc["zone"], "inside": bool(ins),
                            "loops": loops, "m2": len(cells) * c * c, "tone": pc.get("tone"),
                            "name": pc.get("name"), "words": pc.get("words")})
    for li, S_ in free.items():
        pc = pieces[li]
        loops = [smooth(Lp, c * 0.9, 2 if pc["e"] < 0.5 else 4) for Lp in trace(G, S_) if len(Lp) >= 4]
        loops = [Lp for Lp in loops if len(Lp) >= 3 and abs(area2(Lp)) > 2.0 * c * c]
        if loops:
            out.append({"kind": "free", "e": pc["e"], "zone": pc["zone"], "inside": True, "loops": loops,
                        "m2": len(S_) * c * c})
    if meet and key in HUB:
        fam = {}
        for n in meet:
            for li, S_ in free.items():
                if n in S_:
                    f_ = MP[CODE_FAMILY.get(pieces[li]["zone"]["code"], "park")][1]
                    fam[f_] = fam.get(f_, 0) + 1
        tot = float(sum(fam.values()))
        md = "".join("{:02X}".format(int(round(255 * sum(hex_rgb(f_)[q] * v for f_, v in fam.items()) / tot)))
                     for q in range(3))
        loops = [smooth(Lp, c * 0.9, 2) for Lp in trace(G, set(meet)) if len(Lp) >= 4]
        loops = [Lp for Lp in loops if len(Lp) >= 3 and abs(area2(Lp)) > HUB_MIN_M2]
        if loops:
            out.append({"kind": "meet", "e": 0.9, "zone": None, "inside": True, "loops": loops,
                        "m2": len(meet) * c * c, "tone": (mix(md, COL["ink_dark"], 0.45), md, COL["white"]),
                        "name": HUB[key][0], "words": HUB[key][1]})
    return out


def grow_band(G, lines, polys, g, ni, opt):
    """v18: one broad zone grown on grid G from lines and shapes (world m), up to g m out, its edge wandering like
    alternative 2's pieces (noise ni) -> outer loops, holes filled; option A liquid, option B faceted."""
    N = G.nx * G.ny
    best = [1e18] * N
    cells = set()
    for P in lines:
        cells |= G.line_cells(P)
    for P in polys:
        cells.update(G.poly_cells(P))
    hp = [(-g, n) for n in cells if G.valid[n]]
    for _, n in hp:
        best[n] = -g
    heapq.heapify(hp)
    nz, amp, c, nx = _noise(ni), 0.8 * BAND_E, G.c, G.nx
    nbr = [(1, 0, c), (-1, 0, c), (0, 1, c), (0, -1, c), (1, 1, c * 1.4142), (-1, 1, c * 1.4142),
           (1, -1, c * 1.4142), (-1, -1, c * 1.4142)]
    while hp:
        cost, n = heapq.heappop(hp)
        if cost > best[n]:
            continue
        i, j = n % nx, n // nx
        x, y = G.xy(n)
        f = 1.0 + amp * nz(x, y)
        for di, dj, w in nbr:
            ii, jj = i + di, j + dj
            if ii < 0 or jj < 0 or ii >= nx or jj >= G.ny:
                continue
            m = jj * nx + ii
            nc = cost + w * f
            if G.valid[m] and nc < best[m] and nc <= 0.0:
                best[m] = nc
                heapq.heappush(hp, (nc, m))
    S = set(n for n in range(N) if best[n] <= 0.0)
    loops = [Lp for Lp in trace(G, S) if len(Lp) >= 4 and area2(Lp) > 0.0]
    loops = [dp(Lp, c * 3.0) if opt == "B" else smooth(Lp, c * 0.9, 4) for Lp in loops]
    return [Lp for Lp in loops if len(Lp) >= 3 and abs(area2(Lp)) > 50.0 * c * c]


def trace(G, S):
    """Outline loops of a cell set (cell edges, the set on the left; holes come out clockwise)."""
    c, nx, x0, y0 = G.c, G.nx, G.x0, G.y0
    nxt = {}
    for n in S:
        i, j = n % nx, n // nx
        if (j - 1) * nx + i not in S or j == 0:
            nxt.setdefault((i, j), []).append((i + 1, j))
        if i + 1 >= nx or j * nx + i + 1 not in S:
            nxt.setdefault((i + 1, j), []).append((i + 1, j + 1))
        if (j + 1) * nx + i not in S:
            nxt.setdefault((i + 1, j + 1), []).append((i, j + 1))
        if i == 0 or j * nx + i - 1 not in S:
            nxt.setdefault((i, j + 1), []).append((i, j))
    loops = []
    while nxt:
        start = next(iter(nxt))
        Lp, p, prev = [], start, None
        while True:
            outs = nxt.get(p)
            if not outs:
                break
            if len(outs) > 1 and prev is not None:       # pinch corner: turn left first (keeps loops simple)
                dx, dy = p[0] - prev[0], p[1] - prev[1]
                left = (p[0] - dy, p[1] + dx)
                q = left if left in outs else outs[0]
            else:
                q = outs[0]
            outs.remove(q)
            if not outs:
                del nxt[p]
            Lp.append((x0 + p[0] * c, y0 + p[1] * c))
            prev, p = p, q
            if p == start:
                break
        if len(Lp) >= 4:
            loops.append(Lp)
    return loops


def dp(P, tol):
    """Douglas-Peucker on a closed loop (drops the cell staircase)."""
    if len(P) < 5:
        return P
    k = max(range(len(P)), key=lambda i: (P[i][0] - P[0][0]) ** 2 + (P[i][1] - P[0][1]) ** 2)

    def run(Q):
        keep = [0, len(Q) - 1]
        st = [(0, len(Q) - 1)]
        while st:
            a, b = st.pop()
            dmax, im = 0.0, None
            for i in range(a + 1, b):
                d = seg_dist(Q[i][0], Q[i][1], Q[a], Q[b])
                if d > dmax:
                    dmax, im = d, i
            if im is not None and dmax > tol:
                keep.append(im)
                st += [(a, im), (im, b)]
        return [Q[i] for i in sorted(keep)]
    A_ = run(P[:k + 1])
    B_ = run(P[k:] + P[:1])
    return A_[:-1] + B_[:-1]


def smooth(P, tol, it):
    Q = [((P[i][0] + P[(i + 1) % len(P)][0]) / 2, (P[i][1] + P[(i + 1) % len(P)][1]) / 2) for i in range(len(P))]
    Q = dp(Q, tol)
    return chaikin(Q, it, closed=True) if len(Q) >= 3 else Q


def piece_tone(pc):
    if pc["kind"] in ("hub", "meet"):
        return pc["tone"]
    if pc["kind"] in ("zone", "free"):
        return zone_tones(pc["zone"])
    lt, md, dk = PIECE_TONE[pc["kind"]]
    if not pc["inside"]:
        lt = mix(lt, COL["white"], FADE_RING)
    return lt, md, dk



# ================================================================ words inside pieces (v2.3)
def box_in(TP, b, vb=None):
    """Box b lies inside ring TP (9 sample points inside, no ring vertex inside the box)."""
    for x in (b[0], (b[0] + b[2]) / 2, b[2]):
        for y in (b[1], (b[1] + b[3]) / 2, b[3]):
            if not pip(x, y, TP):
                return False
    for p in (vb if vb is not None else TP):
        if b[0] < p[0] < b[2] and b[1] < p[1] < b[3]:
            return False
    return True


def box_clear(b, avoid):
    """v10: box b keeps off the rings in avoid (the commons drawn over the zones of alternative 3)."""
    for A_ in avoid:
        ab = A_[1]
        if not hit(b, ab):
            continue
        for x in (b[0], (b[0] + b[2]) / 2, b[2]):
            for y in (b[1], (b[1] + b[3]) / 2, b[3]):
                if pip(x, y, A_[0]):
                    return False
        for p in A_[0]:
            if b[0] < p[0] < b[2] and b[1] < p[1] < b[3]:
                return False
    return True


def inside_spots(TP, n=16):
    bx = bbox(TP)
    pole = inner_pt(TP)
    S = []
    for i in range(n):
        for j in range(n):
            x = bx[0] + (i + 0.5) / n * (bx[2] - bx[0])
            y = bx[1] + (j + 0.5) / n * (bx[3] - bx[1])
            if pip(x, y, TP):
                S.append((x, y))
    S.sort(key=lambda p: (p[0] - pole[0]) ** 2 + (p[1] - pole[1]) ** 2)
    return [pole] + S


def spread(spots, placed):
    """Spots ordered so a word lands as far as possible from the words already in its piece."""
    if not placed:
        return spots
    return sorted(spots, key=lambda p: -min((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 for q in placed))


def block_size(lines):
    """lines: [(text, size, bold)] -> (w, h)."""
    w = max(text_w(s, sz, bd) for s, sz, bd in lines)
    h = sum(sz * 1.18 for s, sz, bd in lines)
    return w, h


def draw_block(pg, lines, x0, y_top, colour, halo):
    y = y_top
    for s, sz, bd in lines:
        y -= sz * 1.0
        pg.text(s, x0, y, sz, colour, bold=bd, halo=halo)
        y -= sz * 0.18


def fit_inside(TP, spots, lines, taken, pad=0.6, avoid=()):
    w, h = block_size(lines)
    bx = bbox(TP)
    if w + 2 * pad > bx[2] - bx[0] or h + 2 * pad > bx[3] - bx[1]:
        return None
    for (x, y) in spots:
        b = (x - w / 2 - pad, y - h / 2 - pad, x + w / 2 + pad, y + h / 2 + pad)
        if any(hit(b, t) for t in taken):
            continue
        if box_in(TP, b) and (not avoid or box_clear(b, avoid)):
            return b
    return None


def subs_for(z, owner, key, opt):
    rows = [r for r in SUBS if r[0] == owner and r[1] == z["code"]]
    if z["tier"]:
        rows = [r for r in rows if r[2] == z["tier"]] or ([] if len(set(r[2] for r in rows)) > 1 else rows)
    elif len(set(r[2] for r in rows)) > 1:
        rows = []
    out = []
    for r in rows:
        if r[3] in (None, opt, key):
            out += r[4]
    return out


def name_of(z, owner):
    for (o_, c_, t_), nm in NAMES.items():
        if o_ == owner and c_ == z["code"] and t_ in (None, z["tier"]):
            return nm
    return z["label"] or z["code"]


def sig_of(z, owner):
    return next((v for (o_, c_, t_), v in SIG.items() if o_ == owner and c_ == z["code"] and t_ in (None, z["tier"])),
                0.6)


def zone_words(pg, z, TP, owner, key, opt, taken, seen, avoid=(), halo=None):
    """The zone's keyword name (size by SIG) and its sourced keywords scattered inside TP; what does not fit at the
    smallest size is left out (v2.3: no callouts)."""
    dk = zone_tones(z)[2]
    TPs = thin(TP, 300)
    spots = inside_spots(TPs)
    placed = []
    f = sig_of(z, owner)
    bw = max(18.0, (bbox(TPs)[2] - bbox(TPs)[0]) * 0.8)
    for sz in [7.5 * f * t for t in STEPS]:
        lines = [(s_, sz, True) for s_ in wrap(name_of(z, owner), sz, bw, True)]
        if z["code"] == "DG":                        # v13: the very small credit under the name
            lines.append((CREDIT_DG, max(1.2, sz * 0.25), False))
        b = fit_inside(TPs, spots, lines, taken, avoid=avoid)
        if b:
            draw_block(pg, lines, b[0] + 0.6, b[3] - 0.6, dk, halo)
            taken.append(b)
            placed.append(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
            break
    kind_key = (key, z["code"], z["tier"])
    words = subs_for(z, owner, key, opt) if kind_key not in seen else []
    seen.add(kind_key)
    for w_ in words:
        for sz in [3.4 * f * t for t in STEPS]:
            b = fit_inside(TPs, spread(spots, placed), [(w_, sz, False)], taken, pad=1.0 * sz, avoid=avoid)
            if b:
                pg.text(w_, b[0] + 1.0 * sz, b[1] + 1.0 * sz + 0.06 * sz, sz, dk, halo=halo)
                taken.append(b)
                placed.append(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
                break


def hub_words(pg, TP, name, words, colour, taken, halo):
    """The commons' name (large) and what it gathers, inside its piece. v10: a name that fits nowhere inside is
    written centred on the piece with a halo (v2.3 left it out, so the commons often had no name)."""
    TP = thin(TP, 300)
    spots = inside_spots(TP, 20)
    placed = []
    for sz in [8.0 * HUB_SIG * t for t in STEPS]:
        lines = [(s_, sz, True) for s_ in wrap(name, sz, max(18.0, (bbox(TP)[2] - bbox(TP)[0]) * 0.8), True)]
        b = fit_inside(TP, spots, lines, taken)
        if b:
            draw_block(pg, lines, b[0] + 0.6, b[3] - 0.6, colour, None)
            taken.append(b)
            placed.append(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
            break
    else:
        best = None
        for sz in [8.0 * HUB_SIG * t for t in STEPS[3:]]:
            lines = [(s_, sz, True) for s_ in wrap(name, sz, 30.0, True)]
            w, h = block_size(lines)
            for x, y in spots[:60]:
                b = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
                if not any(hit(b, t) for t in taken):
                    best = (lines, b, (x, y))
                    break
            if best:
                break
        if best is None:
            x, y = spots[0]
            best = (lines, (x - w / 2, y - h / 2, x + w / 2, y + h / 2), (x, y))
        draw_block(pg, best[0], best[1][0], best[1][3], colour, halo)
        taken.append(best[1])
        placed.append(best[2])
    for w_ in words:
        for sz in [3.4 * HUB_SIG * t for t in STEPS]:
            b = fit_inside(TP, spread(spots, placed), [(w_, sz, True)], taken, pad=1.0 * sz)
            if b:
                pg.text(w_, b[0] + 1.0 * sz, b[1] + 1.0 * sz + 0.06 * sz, sz, colour, bold=True)
                taken.append(b)
                placed.append(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2))
                break


def word_in(pg, TP, word, sizes, colour, taken, pad=0.5, bold=True):
    """One word inside ring TP at the largest size that fits."""
    TP = thin(TP, 300)
    for sz in sizes:
        b = fit_inside(TP, inside_spots(TP), [(word, sz, bold)], taken, pad=pad)
        if b:
            pg.text(word, b[0] + pad, b[1] + pad + 0.06 * sz, sz, colour, bold=bold)
            taken.append(b)
            return True
    return False


def word_along(pg, TP, word, size, colour, taken, W, H):
    """v10: a word beside a path (PATH_WORDS: v2.3 had them but never wrote them), at the first free spot along it."""
    s = arclen(TP)
    w = text_w(word, size, True)
    for f in (0.5, 0.35, 0.65, 0.2, 0.8):
        (x, y), _ = at_len(TP, s, s[-1] * f)
        for dy in (1.6, -1.6 - size):
            b = (x - w / 2 - 0.5, y + dy - 0.5, x + w / 2 + 0.5, y + dy + size + 0.5)
            if b[0] < 0 or b[1] < 0 or b[2] > W or b[3] > H or any(hit(b, t) for t in taken):
                continue
            pg.text(word, x, y + dy + 0.06 * size, size, colour, bold=True, align="C", halo=COL["white"])
            taken.append(b)
            return True
    return False


def open_rest(A, zones, nr):
    """The point of a working area farthest from its edges and its zones (where it has no programme yet)."""
    best, bd = None, -1.0
    bxa = bbox(A)
    for i in range(28):
        for j in range(28):
            x = bxa[0] + (i + 0.5) / 28 * (bxa[2] - bxa[0])
            y = bxa[1] + (j + 0.5) / 28 * (bxa[3] - bxa[1])
            if not nr.inside(x, y) or any(pip(x, y, z["P"]) for z in zones):
                continue
            d = min([seg_dist(x, y, A[q], A[(q + 1) % len(A)]) for q in range(0, len(A), max(1, len(A) // 200))] +
                    [math.hypot(x - z["q"][0], y - z["q"][1]) for z in zones])
            if d > bd:
                best, bd = (x, y), d
    return best


def no_programme(pg, xy, taken):
    if not xy:
        return
    x, y = xy
    lines = [(u"NO PROGRAMME YET", 4.0, True)]
    w, h = block_size(lines)
    b = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    if not any(hit(b, t) for t in taken):
        draw_block(pg, lines, b[0], b[3], COL["ink2"], COL["white"])
        taken.append(b)


def soft(P, r=ROUND_M, step=1.5):
    """Rounded outline (cleared buildings, v2.3): every corner rounded (up to r m, at most 45 % of each side), then
    one smoothing pass. Graphic only."""
    if len(P) < 3:
        return P
    Q = [P[0]]
    for p in P[1:]:                                      # drop vertices closer than 2 m: corners made of tiny steps
        if math.hypot(p[0] - Q[-1][0], p[1] - Q[-1][1]) >= 2.0:
            Q.append(p)
    if len(Q) < 3:
        return P
    out = []
    for i in range(len(Q)):
        a, b, c = Q[i - 1], Q[i], Q[(i + 1) % len(Q)]
        la, lc = math.hypot(a[0] - b[0], a[1] - b[1]), math.hypot(c[0] - b[0], c[1] - b[1])
        d = min(r, 0.45 * la, 0.45 * lc)
        if d < 0.05:
            out.append(b)
            continue
        p0 = (b[0] + (a[0] - b[0]) * d / la, b[1] + (a[1] - b[1]) * d / la)
        p2 = (b[0] + (c[0] - b[0]) * d / lc, b[1] + (c[1] - b[1]) * d / lc)
        n = max(2, int(d / step))
        for j in range(n + 1):                           # quadratic Bezier through the corner
            t = j / float(n)
            out.append(((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * b[0] + t * t * p2[0],
                        (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * b[1] + t * t * p2[1]))
    return chaikin(out, 1, closed=True)


# ================================================================ the hand-marker line (masterplan v9, pure Python)
def normals(P):
    """Unit left normals at each vertex (averaged over the two segments)."""
    n = len(P)
    T = []
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1.0
        T.append((-dy / L, dx / L))
    return T


def smooth_noise(n, step, wav, rnd):
    """n values of smooth random noise (std about 1) sampled every `step`, with features about `wav` long."""
    k = max(2, int(math.ceil(n * step / max(wav, 1e-9))) + 3)
    ctrl = [rnd.gauss(0.0, 1.0) for _ in range(k)]
    out = []
    for i in range(n):
        x = i * step / max(wav, 1e-9)
        j = min(int(x), k - 2)
        f = x - j
        f = f * f * (3 - 2 * f)
        out.append(ctrl[j] * (1 - f) + ctrl[j + 1] * f)
    return out


def hand_line(P, amp, wav, seed, closed=False, over=0.0):
    """A polyline as a hand would draw it: a smooth sideways wobble of about amp (never more than 2.2 amp), an
    overshoot of over at both ends (a closed ring starts at a random point and runs over past its start). Graphic
    only: areas are never computed from this."""
    P = [tuple(p) for p in P]
    if len(P) < 2:
        return P
    rnd = random.Random(seed)
    step = max(wav / 6.0, 1e-6)
    if closed:
        if math.hypot(P[0][0] - P[-1][0], P[0][1] - P[-1][1]) < 1e-9:
            P = P[:-1]
        k = rnd.randrange(len(P))
        P = P[k:] + P[:k] + [P[k]]
    P = densify(P, step)
    if over > 0 and len(P) >= 2:
        if closed:
            s = arclen(P)
            P = P + [p for p, t in zip(P[1:], s[1:]) if t <= over]
        else:
            (x0, y0), (x1, y1) = P[0], P[1]
            L0 = math.hypot(x0 - x1, y0 - y1) or 1.0
            (x2, y2), (x3, y3) = P[-1], P[-2]
            L1 = math.hypot(x2 - x3, y2 - y3) or 1.0
            P = [(x0 + (x0 - x1) / L0 * over, y0 + (y0 - y1) / L0 * over)] + P + \
                [(x2 + (x2 - x3) / L1 * over, y2 + (y2 - y3) / L1 * over)]
    if amp > 0:
        w = [max(-2.2, min(2.2, v)) * amp for v in smooth_noise(len(P), step, wav, rnd)]
        N = normals(P)
        P = [(p[0] + n[0] * d, p[1] + n[1] * d) for p, n, d in zip(P, N, w)]
    return P


def link_cols(kind):
    """(shaft, head) colours of a link arrow (masterplan v9 link_cols): water dark water-blue; high water
    water-blue with dark heads; people to the water and untyped links in the accent red."""
    if kind == "water":
        return COL["river_dark"], COL["river_dark"]
    if kind == "flood":
        return COL["river_mid"], COL["river_dark"]
    return COL["accent"], COL["accent_dark"]


def link_arrow(pg, P, kind, heads, seed):
    """The bold hand-drawn link arrow along P (page mm), its head at the end (both ends when heads = 2); the head
    shrinks on a short arrow, the pen never does (masterplan v9)."""
    shaft_c, head_c = link_cols(kind)
    s = arclen(P)
    Lt = s[-1]
    if Lt < 1e-6:
        return
    k = min(1.0, Lt / (HA["barb"] * (3.2 if heads == 2 else 2.0)))
    barb = HA["barb"] * k
    inset = barb * 0.25
    sh = sub_line(P, s, inset if heads == 2 else 0.0, Lt - inset)
    sh = hand_line(sh, HA["amp"], HA["wav"], seed)
    if kind == "flood":
        pg.line(sh, shaft_c, HA["shaft"], [1.6, 0.9], cap=0)
    else:
        pg.line(sh, shaft_c, HA["shaft"], cap=1)
    ends = [(Lt, max(0.0, Lt - barb * 0.8))] + ([(0.0, min(Lt, barb * 0.8))] if heads == 2 else [])
    for t_tip, t_back in ends:
        (tx, ty), _ = at_len(P, s, t_tip)
        (bx, by), _ = at_len(P, s, t_back)
        d = math.hypot(tx - bx, ty - by) or 1.0
        dx, dy = (tx - bx) / d, (ty - by) / d
        for sg in (1, -1):
            a = math.radians(HA["ang"]) * sg
            vx, vy = dx * math.cos(a) - dy * math.sin(a), dx * math.sin(a) + dy * math.cos(a)
            ex, ey = tx - vx * barb, ty - vy * barb
            pg.line([(tx + vx * HA["over"] * k, ty + vy * HA["over"] * k), (ex, ey)], head_c, HA["barb_w"], cap=1)
            h = HA["serif"] * k / 2
            pg.line([(ex - vy * h, ey + vx * h), (ex + vy * h, ey - vx * h)], head_c, HA["serif_w"], cap=1)


def boxes_along(P, half):
    """Boxes along a line (page mm): what words keep off."""
    s = arclen(P)
    out = []
    t = 0.0
    while t <= s[-1]:
        (x, y), _ = at_len(P, s, t)
        out.append((x - half, y - half, x + half, y + half))
        t += half
    return out


# ================================================================ zone patterns (masterplan v9 5b; graphic only)
def draw_area(spec, opt, alt, D, base, pz, scale, alpha, A, CL=None):
    """One working area of alternative 1 (partition, darker commons) or 2 (free pieces that overlap) -> Page."""
    key, place, idea = spec
    k = 1000.0 / scale
    R = base["R"]
    M, HEAD = 12.0, 20.0
    dw, dh = (R[2] - R[0]) * k, (R[3] - R[1]) * k
    zones = sorted([z for z in D.zones if z["area"] == key], key=lambda z: -z["m2"])
    removes = [r for r in D.removes if r["area"] == key]
    paths = [p for p in D.paths if p["area"] == key]
    pg = Page(dw, dh)
    T = lambda p: ((p[0] - R[0]) * k, (p[1] - R[1]) * k)
    for pc in pz:
        pc["tones"] = piece_tone(pc)
        pc["TPs"] = [[T(p) for p in Lp] for Lp in pc["loops"]]
    ctx = [pc for pc in pz if pc["kind"] not in ("zone", "hub", "free", "meet")]
    W_ = COL["white"]
    # ---- the pieces: context and the commons opaque (white seams); programme pieces at the opacity on white
    for pc in pz:                                        # v17: the legend's entries
        if pc["kind"] == "free":
            leg_zone(pc["zone"])
        elif pc["kind"] == "hub":
            LEG.setdefault("hub", [])
            if pc["tones"][0] not in LEG["hub"]:
                LEG["hub"].append(pc["tones"][0])
        elif pc["kind"] in PIECE_TONE:
            leg(("ctx", pc["kind"]))
    for ck, lw, dash, P in base["lines"]:
        leg(("line", ck))
    if removes:
        leg("cleared")
    if paths:
        leg("path")
    # v19: context opaque; alternative 2's free zone pieces on one white base; the promenade and the spine zones;
    # the free pieces' light fill at the opacity (overlaps darken); alternative 1's commons opaque on top
    for pc in sorted(ctx, key=lambda q: q["e"]):
        pg.poly(pc["TPs"], fill=pc["tones"][0], stroke=W_, lw=0.5)
    fr = [q for q in pz if q["kind"] == "free"]
    for pc in fr:
        pg.poly(pc["TPs"], fill=W_, stroke=W_, lw=0.5)
    G = Grid(R, base["near"], BAND_CELLS)
    CLc = clip_city(CL, base["near"].within) if CL is not None else None
    RB = [[T(p) for p in L_] for L_ in grow_band(G, base["streams"] + base["banks"],
                                                  [s_["P"] for s_ in D.strips], RIVER_BAND_M, 101, opt)]
    if RB:
        leg("river_band")
        lt, md, dk = RIVER_BAND_TONE
        pg.poly([[(x + 0.8, y - 0.8) for x, y in L_] for L_ in RB], fill=dk, alpha=0.22)   # shadow: volume
        pg.poly(RB, fill=lt, alpha=0.85)
        pg.poly(RB, stroke=dk, lw=0.35)
    SZ = []
    if CLc is not None:
        for nm_, lines_, ni in ((u"MAIN SPINE", CLc["mains"] if "mains" in CLc else [CLc["main"]], 102),
                                (u"RIVERSIDE SPINE", [s_["P"] for s_ in CLc["spine"]], 103)):
            TPs = [[T(p) for p in L_] for L_ in grow_band(G, lines_, [], SPINE_ZONE_M, ni, opt)]
            if TPs:
                leg(("spinezone", nm_))
                pg.poly(TPs, fill=MP["centre"][0], alpha=alpha)
                SZ.append((nm_, TPs))
    for pc in fr:
        pg.poly(pc["TPs"], fill=pc["tones"][0], alpha=alpha)
    for pc in [q for q in pz if q["kind"] == "hub"]:
        pg.poly(pc["TPs"], fill=pc["tones"][0], stroke=W_, lw=0.5)
    for ck, lw, dash, P in base["lines"]:
        pg.line([T(p) for p in P], COL[ck], lw, dash)
    for z in list(zones):                                # the words go into the zone's own (free) piece
        pc = next((q for q in pz if q["kind"] == "free" and q["zone"] is z), None) or \
            next((q for q in pz if q["kind"] == "zone" and q["zone"] is z), None)
        if pc is None or not pc["TPs"]:
            zones.remove(z)
            continue
        z["TP"] = max(pc["TPs"], key=lambda r_: abs(area2(r_)))
    taken = []
    for r in removes:
        r["TP"] = [T(p) for p in soft(r["P"])]
        pg.poly([r["TP"]], stroke=COL["ink2"], lw=0.3, dash=[0.9, 0.6])
    for p in paths:
        p["TP"] = [T(q) for q in p["P"]]
        pg.line(p["TP"], W_, 1.9)
        pg.line(p["TP"], COL["path"], 1.0, [1.0, 0.35], cap=0)
    if CLc is not None:                                  # v11: walks (v19: the spines are zones above)
        draw_city(pg, T, CLc, k, spines=False)
    # ---- words: the commons first, the promenade and spine zones, then each zone (largest first), cleared, context
    for pc in [q for q in pz if q["kind"] == "hub"]:
        hub_words(pg, max(pc["TPs"], key=lambda r_: abs(area2(r_))), pc["name"], pc["words"], W_, taken,
                  pc["tones"][0])
    for nm_, TPs in ([(RIVER_BAND_NAME, RB)] if RB else []) + SZ:   # v18-v19: names and keywords on the fills
        TP_ = max(TPs, key=lambda r_: abs(area2(r_)))
        dk_ = RIVER_BAND_TONE[2] if nm_ == RIVER_BAND_NAME else MP["centre"][2]
        word_in(pg, TP_, nm_, (4.0, 3.4, 2.8), dk_, taken)
        for w_ in (RIVER_BAND_WORDS if nm_ == RIVER_BAND_NAME else []):
            for TP2 in sorted(TPs, key=lambda r_: -abs(area2(r_)))[:3]:
                if word_in(pg, TP2, w_, (2.6, 2.2, 1.8), dk_, taken):
                    break
    seen = set()
    for z in zones:
        zone_words(pg, z, z["TP"], z.get("own", ""), key, opt, taken, seen)
    for r in removes:
        word_in(pg, r["TP"], REMOVE_WORDS[0], (2.3, 1.8, 1.5), COL["ink"], taken)
    for pc in ctx:                                       # context pieces carry their own word (no legend)
        wd = KIND_WORD.get(pc["kind"])
        if not wd or not pc["inside"]:
            continue
        for TP in sorted(pc["TPs"], key=lambda r_: -abs(area2(r_)))[:3]:
            word_in(pg, TP, wd, (2.6, 2.2, 1.8), pc["tones"][2], taken, pad=0.8)
    for p in paths:
        for w_ in PATH_WORDS.get(p.get("own"), []):
            word_along(pg, p["TP"], w_, 2.2, COL["path"], taken, dw, dh)
    if key == "calisma_alan[1]":                         # the open rest of the area: marked, not filled in
        xy = open_rest(A, zones, base["near"])
        no_programme(pg, T(xy) if xy else None, taken)
    # ---- the panel: place and idea over the plan (no owner names, no working-area outline)
    W = M + dw + M
    H = M + HEAD + dh + M
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sh.clip([rect(M, M, M + dw, M + dh)])
    blit(sh, pg, M, M)
    sh.unclip()
    for txt, size, y in ((place, 8.0, H - M - 8.0), (idea, 4.0, H - M - 14.0)):
        sh.text(txt, M, y, min(size, size * dw / max(text_w(txt, size, True), 1e-6)), COL["ink_dark"], bold=True)
    return sh


