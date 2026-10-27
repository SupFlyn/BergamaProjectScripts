# ================================================================ v24: the ecological corridor (p15 + p16 redo)
# Aras 27 Oct 11:07 (revision_2026-10-27/PHASE2_SPEC.md §6 "p15", "p16"; history decisions D1-D12, H1-H7):
#   * the uses blend like a GRADIENT and read as an ECOLOGICAL CORRIDOR: stepped translucent rings of planting from the
#     water outward (denser at the water), and stepped translucent programme rings round the bridge hubs (densest at
#     the hubs, thinning between them: H1). No zone-by-zone fills.
#   * the empty surroundings are developed inside the MAXIMUM POTENTIAL AREA (spec §5 q1 default): the open ground of
#     the site frame (site_alan) with no survey building (BINA_*) and no survey road (YOL_SOSE / YOL_BORDUR, ROAD_BUF_M
#     either side of an edge line, as the v2.3 puzzle grows a street), on a CELL_M grid; shown as its own proof panel
#     (crop mp_max_area).
#   * every design move is computed from the survey / data, never placed by hand, and carries its stacked reasons
#     (D11) naming only analyses that are in the booklet (D12): max area panel, survey contours, water board cuts
#     (Q100 / Q500, p12) and chain (p13), the site board's edge plan (p5, bridges K1-K6, marks C1-C6), OSM road classes
#     (site board p6), history cards h01-h03 (H1-H7).
#   * notes on the map are numbered badges (measured, collision-checked, leader when moved) with the short notes and
#     their reasons in the key column beside the plan: no text overlaps another.
# The proposal's movement (roads, truck route, crossings, hubs) is written to masterplan_results.json key "movement"
# (spec §4) for the site board's p6 proposal map.
MP_SCALE = 5000.0            # p15: each half at 1:5,000 (booklet area 392 x 243 mm: two rows of <= 113 mm)
MA_SCALE = 10000.0           # mp_max_area proof panel (p16 bottom row)
CELL_M = 3.0                 # grid of the max potential area, m
ROAD_BUF_M = 4.5             # a surveyed carriageway edge marks road this far either side (= STREET_M), m
DMAX_M = 200.0               # distance from the water computed this far, m
ECO_BANDS = (8.0, 18.0, 32.0, 50.0, 75.0)    # m from the water: stepped planting rings (graphic, design reading)
ECO_ORGANIC = 18.0           # rings up to this far from the water are organic, further out faceted (form rule)
HUB_RINGS = (40.0, 80.0, 125.0, 175.0)       # m round a hub: the programme rings (H1; graphic, design reading)
HUB_CORRIDOR = 120.0         # programme rings stay within this far of the water, m
HUB_SQ_M = 28.0              # a hub square = open ground within this far of the bridge anchor, m (design value)
FOREST = (6.0, 32.0, 110.0, 9.0)     # forest corridor: from, to m from the water, at least m from a hub, spacing m
TREES = (32.0, 60.0, 70.0, 18.0)     # tree-planted area: the same (design values)
SEAT_STEP = ((100.0, 25.0), (220.0, 50.0))   # streamside seats: within m of a walking hub, one every m of walkway
FOOT_GAP_M = 300.0           # a reach this long without a crossing gets a footbridge (design value)
WIDEN_MIN, BRANCH_MIN, KEPT_MAX, FREE_MAX = 20.0, 55.0, 5.0, 90.0   # open ground beside the bank, m (design rules)
WIDEN_K, WIDEN_CAP, ARM_K, ARM_CAP = 0.4, 20.0, 0.7, 45.0          # widened edge / side arm: share of it, cap m
MOVE_RUN_M = 30.0            # shorter runs of one move are dropped, m
KEPT_SPACE_M = 150.0         # "kept" badges at least this far apart, m (graphic)
TERRACE_D = (4.0, 70.0)      # upstream terraces: contours this far from the water, m
COL_W = 103.0                # key column beside each half, mm
KEY_TS, KEY_MIN = 2.6, 2.47  # key text, mm (7.4 pt; 7 pt the floor)
PLACE_TS = 4.3               # place names on the plans, mm (12.2 pt)
LAB_TS = 2.6                 # labels on the 1:1,000 windows, mm
BADGE_R, BADGE_TS = 1.95, 2.5
DT_PLAN = (194.0, 160.0)     # p16 windows, mm at 1:1,000 (194 x 171.5 crop + 53 mm max area row fit 243 mm)
ECO_COL, HUB_COL = "6F8A4E", "D9A35E"        # palette "tree" family darkened / "centre" family (graphic)
WATER_COL, WET_COL = COL["river"], "B7CFC8"
SQ_FILL, SQ_EDGE = "F4E6CC", "9C7440"
ROAD_CHANGE_COL = {"calmed": "B5832F", "pedestrian": "8B3A3F", "shared": "7F5B7B", "kept": "847E75",
                   "relocated": "C2603A", "later": "633131"}

# Bridges over the Selinos (site board BRIDGES_K = CONCEPT_RECORD 2.1, survey m)
BRIDGES_K = [("K1", (29628.35, 32630.87)), ("K2", (29604.93, 32622.02)), ("K3", (30037.01, 32121.57)),
             ("K4", (29846.40, 32277.71)), ("K5", (30293.63, 31792.25)), ("K6", (30646.94, 31251.65))]
# Hubs (D2, D3, D10; h03 Q1 + Aras 27 Oct 12:05 "Both"): id, bridge key (spec §4), anchor (survey m: H1 bridge
# anchors h01 §5 P06 P08 P09 P30; İstiklal = P16 label; Kızıl Avlu = P02), its OSM bus stop (name, survey m by the
# h01 §0 formula from bergama_osm.osm of 28 Jul 2026, +-10-30 m), river sub-hub in the bed (D10).
MAIN_TRANSIT_HUB = (u"İstiklal", u"Kızıl Avlu")   # Aras 12:05: the town lines stop here; switch: hub ids
HUBS = [(u"K4", "K4", (29846.0, 32278.0), u"Camikebir Caddesi", (29841.0, 32243.7), True),
        (u"K3", "K3", (30037.0, 32122.0), u"Tabak Köprüsü", (30017.4, 32106.8), True),
        (u"İstiklal", u"İstiklal", (29990.0, 32030.5), u"İstiklal Meydanı", (29995.4, 32019.8), False),
        (u"Kızıl Avlu", u"İstiklal", (30245.0, 31962.0), u"Kızıl Avlu", (30245.0, 32020.1), False),
        (u"K5", "K5", (30294.0, 31792.0), u"Üç Kemer Köprüsü", (30296.4, 31696.7), True),
        (u"K6", "K6", (30647.0, 31252.0), u"Bergama Sanayi", (30575.0, 31232.4), False)]
HUB_NAME = {u"K4": u"K4 · ULUCAMİ ÖNÜ", u"K3": u"K3 · TABAK", u"İstiklal": u"İSTİKLAL MEYDANI",
            u"Kızıl Avlu": u"KIZIL AVLU", u"K5": u"K5 · ÜÇ KEMER", u"K6": u"K6"}
# Places named on the plans (h01 §5 register; survey labels, m): Ulu Cami P05, Tabaklar Hamamı P07, Tabakhane E07
PLACES = [(u"ULU CAMİ", (29844.2, 32313.3)), (u"TABAKLAR HAMAMI", (29890.4, 32243.6)),
          (u"TABAKHANE", (30062.0, 32106.0)), (u"HARAP CAMİİ", (30435.7, 31584.6))]
# H5 (h03 Q3): Trajaneum centroid 39.1327803, 27.1832652 (OSM) -> survey by the h01 §0 formula (+-10-30 m)
TRAJANEUM = (30209.0, 33177.0)
ROMAN_WALL = (29800.2, 32362.3)      # H6: "Eski Kozak Yolu" label, Roman complex with ~120 m bank wall (P12, E10)
CRAFT_XY = (30062.0, 32106.0)        # H3: "Eski Tabakhane Sk." label (E07) = city link stop 2 (workshops)
# Roads (OSM bergama_osm.osm, 28 Jul 2026, highway class and name; survey m by the h01 §0 formula, +-10-30 m). Each
# change is read from data: the OSM class (site board p6 driving map), the site board mark C3 "K4: monument and
# traffic" (p5), and the OSM chainages of the car crossings along the stream (calculated). No traffic count exists
# on these streets (card t01: KGM counts only on 35-04, 35-05, D240): no "relocated" road.
ROADS = [
    dict(name=u"Bergama - Kozak Yolu", change="kept", note=u"kept: through road to Kozak",
         proof=u"OSM secondary (one 11.9 km way)",
         xy=[[29668.6, 32896.0], [29643.3, 32796.0], [29633.4, 32739.9], [29627.0, 32698.6], [29625.9, 32675.0],
             [29627.8, 32656.7], [29636.9, 32624.0], [29648.9, 32599.2], [29667.9, 32549.9], [29687.1, 32517.5],
             [29726.2, 32490.9], [29760.3, 32463.9], [29772.4, 32442.5], [29775.9, 32394.5], [29772.1, 32343.5],
             [29773.3, 32313.3], [29777.8, 32297.2], [29792.2, 32271.3]]),
    dict(name=u"Cami Kebir Caddesi + Ulucami Köprüsü", change="calmed", note=u"calmed: monument meets traffic at K4",
         proof=u"site board p5 mark C3; OSM secondary",
         xy=[[29854.5, 32289.9], [29843.7, 32252.8], [29873.2, 32232.0], [29934.1, 32225.0], [29960.0, 32218.3],
             [29976.9, 32203.2], [30015.5, 32111.3]]),
    dict(name=u"Tabak Köprüsü", change="calmed", note=u"calmed: hub square and workshops at K3",
         proof=u"H1, H3 (h01/h02); OSM secondary", xy=[[30023.7, 32110.3], [30052.5, 32130.6]]),
    dict(name=u"Kınık Caddesi", change="kept", note=u"kept: main spine, shops",
         proof=u"city link p9 main spine; OSM secondary",
         xy=[[29992.8, 32017.4], [30005.0, 32029.4], [30032.5, 32038.3], [30089.7, 32057.7], [30138.7, 32039.0]]),
    dict(name=u"Kızıl Avlu Çıkmazı", change="pedestrian", note=u"pedestrian: dead end over hidden stream",
         proof=u"OSM living_street, dead end; H2",
         xy=[[30144.3, 31986.1], [30123.6, 31988.0], [30099.4, 31997.7]]),
    dict(name=u"Üç Kemer Köprüsü", change="pedestrian", note=u"pedestrian: car crossings 190-230 m away",
         proof=u"OSM residential; OSM chainage of Kızıl Avlu Cd / next bridge (calc); H1",
         xy=[[30277.2, 31777.9], [30314.7, 31804.7]]),
    dict(name=u"Adnan Menderes Bulvarı", change="kept", note=u"kept: regional road İzmir-Soma at K6",
         proof=u"OSM primary; h02 E12", xy=[[30609.3, 31239.0], [30695.5, 31266.2]]),
    dict(name=u"bank street, lower reach", change="shared", note=u"shared: local bank street, stream widens",
         proof=u"OSM residential; max area panel",
         xy=[[30713.4, 31260.3], [30730.6, 31243.9], [30800.4, 31198.6], [30862.6, 31166.0], [30923.9, 31135.4],
             [30975.8, 31095.9], [31012.3, 31057.8], [31062.1, 30994.1], [31143.6, 30884.2], [31192.5, 30817.8],
             [31216.8, 30791.6]])]
# Aras 12:05: a town-line extension to K4 as a PROPOSED LATER STEP, on the existing streets İstiklal stop -> Kınık Cd
# -> Cami Kebir Cd -> K4 stop (OSM ways 370936581, 1222988932, 371130159, as above)
TOWN_LINE = dict(name=u"town bus line to K4", change=u"proposed later: bus line 651 to K4",
                 note=u"later step: town line on to K4", proof=u"h03 Q1 (town lines stop at İstiklal); K4 stop 35 m",
                 xy=[[29995.4, 32019.8], [30005.0, 32029.4], [30032.5, 32038.3], [30084.6, 32056.0], [30089.7, 32057.7],
                     [30075.0, 32066.0], [30041.0, 32089.8], [30017.4, 32106.8], [30015.5, 32111.3], [29976.9, 32203.2],
                     [29960.0, 32218.3], [29934.1, 32225.0], [29873.2, 32232.0], [29841.0, 32243.7]])
# Species codes (water board SPECIES, bands B-F; only species of that list): which plants go where (p16)
PLANT_AT = {"bed": ("B", ("Ty", "Ph", "Me")), "wet": ("C", ("Sa", "Ta")), "forest": ("E", ("Fr", "Po", "Qu", "Ul")),
            "trees": ("E", ("Po", "Fr")), "hub": ("E", ("Pl",)), "terrace": ("F", ("La",)), "arm": ("B", ("Ty", "Ph"))}


class _All(object):
    """v24: every cell of the corridor grid is valid (Grid's 'near' test)."""

    def within(self, x, y):
        return True

    inside = within


class Corridor(object):
    """v24: the survey and the design of the whole site frame, computed once a press, in world (survey) m.
    F per grid cell: 0 open, 1 building, 2 road, 3 stream bed / water line. Dst: distance from the water through open
    ground (m). Everything the panels draw: bands, hub rings and squares, moves, terraces, trees, seats, crossings,
    roads, notes (numbered) and the movement record."""

    def __init__(self, V, survey, CL, D, spots, warn):
        self.V, self.D, self.CL, self.warn, self.spots = V, D, CL or {}, warn, spots or []
        G = self.G = Grid((V.u0, V.v0, V.u1, V.v1), _All(),
                          int((V.u1 - V.u0) * (V.v1 - V.v0) / (CELL_M * CELL_M)) + 1)
        N = self.N = G.nx * G.ny
        F = self.F = bytearray(N)
        uvP = lambda P: [V.uv(p) for p in P]
        inF = lambda P: any(V.inside(p[0], p[1]) for p in P)
        self.bld = {}
        for role in ("building", "housing", "heritage", "shed"):          # buildings: whole footprints (faces)
            polys = [P for P in survey.get(role, []) if inF(P)]
            self.bld[role] = faces(polys, max_area=30000.0) if polys else []
            for Fc in self.bld[role]:
                for n in G.poly_cells(uvP(Fc)):
                    F[n] = 1
        self.roads = [P for role in ("road", "kerb") for P in survey.get(role, []) if inF(P)]
        r = max(1, int(round(ROAD_BUF_M / G.c)))
        nx, ny = G.nx, G.ny
        for P in self.roads:
            for n in G.line_cells(uvP(P)):
                i, j = n % nx, n // nx
                for dj in range(-r, r + 1):
                    for di in range(-r, r + 1):
                        ii, jj = i + di, j + dj
                        if di * di + dj * dj <= r * r + 1 and 0 <= ii < nx and 0 <= jj < ny and F[jj * nx + ii] == 0:
                            F[jj * nx + ii] = 2
        self.ref = self.CL.get("W", {}).get("ref") or stream_ref()[0]
        self.rows = [x for x in (self.CL.get("W", {}).get("rows") or [])
                     if not x["cov"] and x.get("NE") and x.get("SW") and V.inside(x["p"][0], x["p"][1])]
        for x in self.rows:                                              # the bed between the edges river_walks found
            t = x["SW"]["e"]
            while t <= x["NE"]["e"]:
                n = self.cell((x["p"][0] + x["n"][0] * t, x["p"][1] + x["n"][1] * t))
                if n is not None and F[n] != 1:
                    F[n] = 3
                t += G.c * 0.5
        self.streams = [P for P in survey.get("stream", []) if inF(P)]
        self.contours = [P for role in ("contour", "contour10") for P in survey.get(role, []) if inF(P)]
        for P in self.streams:
            for n in G.line_cells(uvP(P)):
                if F[n] == 0:
                    F[n] = 3
        if not self.rows:
            warn.append(u"corridor: no stream edges from the survey (river_walks rows): no bed, widening or moves")
        self.stats = dict((k_, sum(1 for v in F if v == k_) * G.c * G.c) for k_ in (0, 1, 2, 3))
        self.dist_water()
        self.hubs = []
        for hid, br, xy, stop, sxy, sub in HUBS:
            self.hubs.append({"id": hid, "bridge": br, "xy": xy, "stop": stop, "stop_xy": sxy, "sub": sub,
                              "role": "transit" if hid in MAIN_TRANSIT_HUB else "walking",
                              "stop_m": math.hypot(sxy[0] - xy[0], sxy[1] - xy[1])})
        self.prog = [h for h in self.hubs if h["id"] != u"K6"]           # K6 = gateway out (D2): no programme ring
        self.notes = []
        self.build()

    # ---- grid helpers
    def cell(self, p):
        """Grid cell of world point p, or None outside the frame."""
        u, v = self.V.uv(p)
        G = self.G
        i, j = int((u - G.x0) / G.c), int((v - G.y0) / G.c)
        if 0 <= i < G.nx and 0 <= j < G.ny:
            return j * G.nx + i
        return None

    def near_cells(self, xy, r):
        """Cells whose centre lies within r m of world point xy."""
        G = self.G
        u, v = self.V.uv(xy)
        out = []
        for j in range(max(0, int((v - r - G.y0) / G.c)), min(G.ny, int((v + r - G.y0) / G.c) + 1)):
            for i in range(max(0, int((u - r - G.x0) / G.c)), min(G.nx, int((u + r - G.x0) / G.c) + 1)):
                if math.hypot(G.x0 + (i + 0.5) * G.c - u, G.y0 + (j + 0.5) * G.c - v) <= r:
                    out.append(j * G.nx + i)
        return out

    def wxy(self, n):
        return self.V.xy(*self.G.xy(n))

    def dist_water(self):
        G, F = self.G, self.F
        nx, ny, c = G.nx, G.ny, G.c
        Dst = self.Dst = [1e9] * self.N
        hp = [(0.0, n) for n in range(self.N) if F[n] == 3]
        for _, n in hp:
            Dst[n] = 0.0
        heapq.heapify(hp)
        nb = [(1, 0, c), (-1, 0, c), (0, 1, c), (0, -1, c), (1, 1, c * 1.4142), (-1, 1, c * 1.4142),
              (1, -1, c * 1.4142), (-1, -1, c * 1.4142)]
        while hp:
            d, n = heapq.heappop(hp)
            if d > Dst[n] or d > DMAX_M:
                continue
            i, j = n % nx, n // nx
            for di, dj, w in nb:
                ii, jj = i + di, j + dj
                if 0 <= ii < nx and 0 <= jj < ny:
                    m = jj * nx + ii
                    if (F[m] == 0 or F[m] == 3) and d + w < Dst[m]:
                        Dst[m] = d + w
                        heapq.heappush(hp, (d + w, m))

    def dhub(self, p, hubs=None):
        return min([math.hypot(p[0] - h["xy"][0], p[1] - h["xy"][1]) for h in (hubs or self.prog)] or [1e9])

    def loops(self, cells, organic):
        """World loops of a cell set: organic (smoothed) at the water, faceted elsewhere (form rule)."""
        out = []
        for Lp in trace(self.G, set(cells)):
            Q = smooth(Lp, self.G.c * 0.9, 2 if organic else 0)
            if len(Q) >= 3 and abs(area2(Q)) > 6.0 * self.G.c * self.G.c:
                out.append([self.V.xy(u, v) for u, v in Q])
        return out

    def note(self, key, text, why, at):
        """A numbered note (numbers given after all are made, upstream first); same key = one note, more places."""
        for nt in self.notes:
            if nt["key"] == key:
                nt["at"] += list(at)
                return nt
        self.notes.append({"key": key, "text": text, "why": list(why), "at": list(at)})
        return self.notes[-1]

    # ---- the design
    def build(self):
        F, Dst, N = self.F, self.Dst, self.N
        open_ = lambda n: F[n] == 0 or F[n] == 3
        self.max_loops = self.loops([n for n in range(N) if open_(n)], False)
        self.road_loops = self.loops([n for n in range(N) if F[n] == 2], False)
        self.bed_loops = self.loops([n for n in range(N) if F[n] == 3], True)
        self.eco = [(t, self.loops([n for n in range(N) if open_(n) and Dst[n] <= t], t <= ECO_ORGANIC))
                    for t in ECO_BANDS]
        dh = [1e9] * N
        for n in range(N):
            if F[n] == 0 and Dst[n] <= HUB_CORRIDOR:
                dh[n] = self.dhub(self.wxy(n))
        self.dh = dh
        self.rings = [(r, self.loops([n for n in range(N) if dh[n] <= r], False)) for r in HUB_RINGS]
        for h in self.hubs:                                              # the dry hub squares (faceted)
            h["square"] = []
            if h["id"] in (u"K6", u"Kızıl Avlu"):
                continue
            cs = [n for n in self.near_cells(h["xy"], HUB_SQ_M) if F[n] == 0 and Dst[n] >= 4.0]
            h["square"] = self.loops(cs, False)
            h["trees"] = []
            for L_ in h["square"]:
                s = arclen(L_ + L_[:1])
                t = 0.0
                while t < s[-1]:
                    h["trees"].append(at_len(L_ + L_[:1], s, t)[0])
                    t += 9.0
            h["sub_xy"] = self.sub_hub(h["xy"]) if h["sub"] else None
        self.moves()
        self.terraces()
        self.planting()
        self.crossings()
        self.view_terrace()
        self.make_notes()

    def sub_hub(self, xy):
        """The bed station nearest a bridge anchor (within 60 m): its centre and both edges (D10 sub-hub)."""
        best = min(self.rows, key=lambda x: (x["p"][0] - xy[0]) ** 2 + (x["p"][1] - xy[1]) ** 2) if self.rows else None
        if best is None or math.hypot(best["p"][0] - xy[0], best["p"][1] - xy[1]) > 60.0:
            return None
        at = lambda t: (best["p"][0] + best["n"][0] * t, best["p"][1] + best["n"][1] * t)
        e0, e1 = best["SW"]["e"], best["NE"]["e"]
        return {"c": at((e0 + e1) / 2.0), "a": at(e0), "b": at(e1), "w": e1 - e0}

    def free_out(self, x, side, sg):
        """Open ground beyond a bank edge along the station's normal (m) and what stops it."""
        e, t = x[side]["e"], 1.0
        while t < FREE_MAX:
            n = self.cell((x["p"][0] + x["n"][0] * (e + sg * t), x["p"][1] + x["n"][1] * (e + sg * t)))
            if n is None:
                return t, "frame"
            if self.F[n] == 1:
                return t, "building"
            if self.F[n] == 2:
                return t, "road"
            t += self.G.c * 0.5
        return FREE_MAX, "open"

    def moves(self):
        """Widen, side arm (branch), kept: per bank station, from the open ground beside the edge (max area). Widening
        and arms only from K5 downstream (spec: 'downstream'); kept everywhere (where we could not expand)."""
        self.widen, self.arms, self.kept = [], [], []
        ch5 = chain_at(self.ref, BRIDGES_K[4][1])[0] if self.ref else 0.0
        st = self.rows
        for side, sg in (("NE", 1.0), ("SW", -1.0)):
            raw = [self.free_out(x, side, sg) for x in st]
            fw = [_median([v[0] for v in raw[max(0, i - 4):i + 5]]) for i in range(len(raw))]
            cls = []
            for i, x in enumerate(st):
                down = x["ch"] >= ch5 + 20.0
                cls.append("kept_" + raw[i][1] if fw[i] < KEPT_MAX else
                           ("branch" if down and fw[i] >= BRANCH_MIN else ("widen" if down and fw[i] >= WIDEN_MIN else None)))

            def runs(pred):
                out, cur = [], []
                for i, x in enumerate(st):
                    if pred(cls[i]) and (not cur or x["ch"] - st[cur[-1]]["ch"] <= 3 * WALK_STEP):
                        cur.append(i)
                        continue
                    if len(cur) * WALK_STEP >= MOVE_RUN_M:
                        out.append(cur)
                    cur = [i] if pred(cls[i]) else []
                if len(cur) * WALK_STEP >= MOVE_RUN_M:
                    out.append(cur)
                return out
            at = lambda x, t: (x["p"][0] + x["n"][0] * t, x["p"][1] + x["n"][1] * t)
            for ix in runs(lambda c_: c_ in ("widen", "branch")):
                L = len(ix)
                inner, outer = [], []
                for a, i in enumerate(ix):
                    x, e = st[i], st[i][side]["e"]
                    tap = min(1.0, (a + 1) / 6.0, (L - a) / 6.0)
                    inner.append(at(x, e))
                    outer.append(at(x, e + sg * min(WIDEN_K * fw[i], WIDEN_CAP) * tap))
                ring_ = chaikin(inner + outer[::-1], 2, closed=True)
                mid = st[ix[L // 2]]
                self.widen.append({"ring": ring_, "at": at(mid, mid[side]["e"] + sg * 4.0),
                                   "fw": (min(fw[i] for i in ix), max(fw[i] for i in ix))})
            for ix in runs(lambda c_: c_ == "branch"):
                if len(ix) * WALK_STEP < 2 * MOVE_RUN_M:
                    continue
                L = len(ix)
                arm = []
                for a, i in enumerate(ix):
                    x, e = st[i], st[i][side]["e"]
                    tap = math.sin(math.pi * min(1.0, (a + 0.5) / 10.0, (L - a - 0.5) / 10.0) / 2.0)
                    arm.append(at(x, e + sg * min(ARM_K * fw[i], ARM_CAP) * tap))
                self.arms.append({"P": chaikin(arm, 2), "at": arm[L // 2]})
            for why in ("building", "road", "frame"):
                for ix in runs(lambda c_, w_=why: c_ == "kept_" + w_):
                    mid = st[ix[len(ix) // 2]]
                    self.kept.append({"why": why, "at": at(mid, mid[side]["e"] + sg * 2.0)})

    def terraces(self):
        """Upstream (from the frame's upstream end to K4, where the contours crowd): survey contours on open ground
        TERRACE_D from the water become terrace edges; each holds the rain that runs down to it (ticks toward the
        stream = down the valley side). Steepness = contour length per open hectare, upstream vs from K5 down."""
        V = self.V
        u4 = V.uv(BRIDGES_K[3][1])[0]
        u5 = V.uv(BRIDGES_K[4][1])[0]
        self.terr, per = [], {"up": [0.0, 0.0], "down": [0.0, 0.0]}

        def ok(x, y):
            n = self.cell((x, y))
            return n is not None and self.F[n] == 0 and TERRACE_D[0] <= self.Dst[n] <= TERRACE_D[1] and \
                V.uv((x, y))[0] < u4
        for P in self.contours:
            for r_ in cut_runs(P, ok, 2.0):
                if len(r_) >= 2 and arclen(r_)[-1] >= 15.0:
                    self.terr.append(r_)
            for a, b in zip(P, P[1:]):
                q = ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)
                n = self.cell(q)
                if n is None or self.F[n] != 0:
                    continue
                u = V.uv(q)[0]
                k_ = "up" if u < u4 else ("down" if u > u5 else None)
                if k_:
                    per[k_][0] += math.hypot(b[0] - a[0], b[1] - a[1])
        G = self.G
        for n in range(self.N):
            if self.F[n] == 0:
                u = G.x0 + (n % G.nx + 0.5) * G.c
                k_ = "up" if u < u4 else ("down" if u > u5 else None)
                if k_:
                    per[k_][1] += G.c * G.c / 10000.0
        self.steep = dict((k_, v[0] / v[1] if v[1] > 0 else 0.0) for k_, v in per.items())

    def planting(self):
        """Forest corridor (dense) and tree-planted area (sparse) on open ground by distance from the water, away
        from the hubs (H1: programme at the hubs, planting between); jittered grid (deterministic)."""
        G, F, Dst = self.G, self.F, self.Dst
        self.forest, self.trees = [], []
        for (d0, d1, hmin, sp), out in ((FOREST, self.forest), (TREES, self.trees)):
            s = max(1, int(round(sp / G.c)))
            for j in range(0, G.ny, s):
                for i in range(0, G.nx, s):
                    jit = math.sin(i * 12.9898 + j * 78.233) * 43758.5453
                    jit = jit - math.floor(jit)
                    ii = min(G.nx - 1, i + int(jit * s))
                    n = j * G.nx + ii
                    if F[n] != 0 or not (d0 <= Dst[n] <= d1):
                        continue
                    p = self.wxy(n)
                    if self.dhub(p) >= hmin:
                        out.append(p)
        runs = [x for x in self.CL.get("W", {}).get("runs", []) if x.get("cls") == "bank" and len(x.get("F") or []) > 1]
        keep = []
        for x in runs:                                   # one canopied walkway per reach: the longer of two banks
            other = [y for y in runs if y["bank"] != x["bank"] and min(x["ch1"], y["ch1"]) - max(x["ch0"], y["ch0"]) >
                     0.5 * (x["ch1"] - x["ch0"]) and y["m"] > x["m"]]
            if not other:
                keep.append(x["F"])
        self.canopy = keep
        walk = [h for h in self.hubs if h["role"] == "walking" and h["id"] != u"K6"]
        self.seats = []
        for P in keep:
            s = arclen(P)
            t = 0.0
            while t < s[-1]:
                q = at_len(P, s, t)[0]
                d = self.dhub(q, walk)
                step = next((st_ for lim, st_ in SEAT_STEP if d <= lim), None)
                if step is None:
                    t += SEAT_STEP[-1][1]
                    continue
                self.seats.append(q)
                t += step

    def crossings(self):
        """Bridges kept (K1-K6 within 40 m of the stream line), footbridges where a reach without a
        crossing is longer than FOOT_GAP_M (at the open-ground station nearest the gap's middle, both landings open),
        stepping stones at each sub-hub."""
        ref = self.ref
        if not ref:
            self.cross, self.covered = [], []
            return
        s_ref = arclen(ref)
        ch = []
        for nm, xy in BRIDGES_K:
            c_, d_ = chain_at(ref, xy)
            if d_ <= 40.0:
                ch.append((c_, nm, xy))
        self.cross = [{"name": nm + u" bridge", "kind": "bridge kept", "xy": xy} for c_, nm, xy in ch]
        lo = min((chain_at(ref, p)[0] for p in self.V.P), default=0.0)
        hi = max((chain_at(ref, p)[0] for p in self.V.P), default=s_ref[-1])
        cov = stream_ref()[1]
        cs = sorted([lo] + [c_ for c_, _, _ in ch] + [min(hi, s_ref[-1])])
        rows = self.rows
        n_ft = 0
        for a, b in zip(cs, cs[1:]):
            gap = b - a
            if gap <= FOOT_GAP_M:
                continue
            k_ = int(math.ceil(gap / FOOT_GAP_M)) - 1
            for q in range(1, k_ + 1):
                target = a + gap * q / (k_ + 1.0)
                cand = [x for x in rows if abs(x["ch"] - target) <= gap / (2.0 * (k_ + 1))]
                cand.sort(key=lambda x: abs(x["ch"] - target))
                for x in cand:
                    if self.free_out(x, "NE", 1.0)[0] >= 4.0 and self.free_out(x, "SW", -1.0)[0] >= 4.0:
                        at = lambda t: (x["p"][0] + x["n"][0] * t, x["p"][1] + x["n"][1] * t)
                        A_, B_ = at(x["SW"]["e"] - 3.0), at(x["NE"]["e"] + 3.0)
                        n_ft += 1
                        self.cross.append({"name": u"footbridge {}".format(n_ft), "kind": "footbridge",
                                           "xy": ((A_[0] + B_[0]) / 2.0, (A_[1] + B_[1]) / 2.0), "P": [A_, B_],
                                           "gap": gap})
                        break
        for h in self.hubs:
            if h.get("sub_xy"):
                self.cross.append({"name": u"stepping stones " + h["id"], "kind": "stepping stones",
                                   "xy": h["sub_xy"]["c"], "P": [h["sub_xy"]["a"], h["sub_xy"]["b"]]})
        self.covered = [P for P in self.CL.get("W", {}).get("covered", [])] or \
            [[ref[i], ref[i + 1]] for i in range(len(ref) - 1) if i < len(cov) and cov[i]]

    def view_terrace(self):
        """H5 (D5; h03 Q3): the viewing terrace, sited by a computed sightline to the Trajaneum (TRAJANEUM). Method:
        candidates = open ground (no building, no road, not the bed) 4-40 m from the water between the frame's
        upstream end and K3; a candidate is clear when the straight line from it toward the Trajaneum crosses no
        survey building inside the site frame (plan check, 2D: no surveyed summit point, the acropolis height is
        uncertain 300/335/336 m, so no height-based visibility is computed); of the clear ones the terrace takes the
        highest ground (survey spot heights NOKTA_TAKEOMETRI within 12 m), else the one nearest K4. Beyond the frame
        the line is not checked."""
        self.terrace = None
        F, Dst, G = self.F, self.Dst, self.G
        u3 = self.V.uv(BRIDGES_K[2][1])[0]
        bk = {}
        for q in self.spots:                                  # spot heights bucketed in 12 m cells
            bk.setdefault((int(q[0] // 12.0), int(q[1] // 12.0)), []).append(q)
        best = None
        for n in range(0, self.N, 3):
            if F[n] != 0 or not (4.0 <= Dst[n] <= 40.0):
                continue
            if G.x0 + (n % G.nx + 0.5) * G.c > u3:
                continue
            p = self.wxy(n)
            dx, dy = TRAJANEUM[0] - p[0], TRAJANEUM[1] - p[1]
            L = math.hypot(dx, dy) or 1.0
            t, clear = G.c, True
            while t < 600.0:
                m = self.cell((p[0] + dx / L * t, p[1] + dy / L * t))
                if m is None:
                    break
                if F[m] == 1:
                    clear = False
                    break
                t += G.c
            if not clear:
                continue
            gx, gy = int(p[0] // 12.0), int(p[1] // 12.0)
            zs = [q[2] for di in (-1, 0, 1) for dj in (-1, 0, 1) for q in bk.get((gx + di, gy + dj), ())
                  if abs(q[0] - p[0]) <= 12.0 and abs(q[1] - p[1]) <= 12.0]
            k4 = math.hypot(p[0] - BRIDGES_K[3][1][0], p[1] - BRIDGES_K[3][1][1])
            score = (max(zs) if zs else -1e9, -k4)
            if best is None or score > best[0]:
                best = (score, p, max(zs) if zs else None, L)
        if best is not None:
            self.terrace = {"xy": best[1], "z": best[2], "d": best[3],
                            "dir": ((TRAJANEUM[0] - best[1][0]) / best[3], (TRAJANEUM[1] - best[1][1]) / best[3])}
        else:
            self.warn.append(u"viewing terrace: no open ground with a clear line to the Trajaneum (upstream of K3)")

    def make_notes(self):
        """The numbered notes: short note + stacked reasons (D11), each reason an analysis in the booklet (D12)."""
        V = self.V
        for h in self.hubs:
            hid = h["id"]
            sq = [inner_pt(max(h["square"], key=lambda L_: abs(area2(L_))))] if h.get("square") else [h["xy"]]
            stop = u"bus stop {} {:.0f} m".format(h["stop"], h["stop_m"])
            if h["role"] == "transit":
                txt = u"TRANSIT HUB · {}".format(HUB_NAME[hid])
                why = [u"town bus lines stop here (h03 Q1)", stop]
                why += [u"H2 culvert under the square: hidden-stream square", u"D8 plane trees, irrigated from storage"] \
                    if hid == u"İstiklal" else [u"H2 Red Hall tunnels"]
            elif hid == u"K6":
                txt, why = u"GATEWAY OUT · K6", [u"OSM primary road kept (h02 E12)", stop]
            else:
                txt = u"WALKING HUB · {} · DRY SQUARE{}".format(hid, u" + BED SUB-HUB" if h.get("sub_xy") else u"")
                why = [u"H1 Roman bridge", u"open ground (max area)", stop, u"D8 plane trees, irrigated from storage"]
                if h.get("sub_xy"):
                    why.append(u"sub-hub closes in floods (Q100/Q500, p12)")
                if hid == u"K3":
                    why.insert(1, u"H3 tanning reach: workshops, education")
                if hid == u"K5":
                    why.insert(1, u"Demeter's Garden: Q500 stays in the banks at the K5 cut (p12)")
            self.note(("hub", hid), txt, why, sq)
        self.note(("h4",), u"STEP TO THE WATER FACING TABAKLAR HAMAMI", [u"H4 bath ruin 1.5 m from the stream"],
                  [PLACES[1][1]])
        self.note(("h6",), u"DECK OVER THE ROMAN BANK WALL", [u"H6 Roman complex, ~120 m bank wall (P12)"], [ROMAN_WALL])
        if self.terrace:
            z = u", highest clear ground +{:.1f} m".format(self.terrace["z"]) if self.terrace["z"] is not None else u""
            self.note(("view",), u"VIEWING TERRACE · TRAJANEUM {:,.0f} m".format(self.terrace["d"]),
                      [u"H5 computed sightline: no building on the line (site frame){}".format(z)], [self.terrace["xy"]])
        for z in self.D.zones:
            if z["code"] == "WT":
                self.note(("wt",), u"WATER CLEANED ONCE · REED BASINS",
                          [u"collect, clean, hold chain (water board p13)", u"clean-water classroom (city link stop 7)"],
                          [z["q"]])
        if self.terr:
            st = self.steep
            self.note(("terr",), u"TERRACES ON THE CONTOURS HOLD THE RAIN",
                      [u"survey contours: {:.0f} m/ha upstream, {:.0f} m/ha below K5".format(st.get("up", 0.0),
                                                                                        st.get("down", 0.0)),
                       u"overflow to the reed basins (p13 chain)"],
                      [self.terr[len(self.terr) // 2][len(self.terr[len(self.terr) // 2]) // 2]])
        if self.covered:
            P = max(self.covered, key=lambda P: arclen(P)[-1])
            self.note(("cov",), u"NOTHING OPENED · WATER LINE IN THE PAVING",
                      [u"H2 covered reach, ~240 m without stream lines (h02 E01)"],
                      [at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0]])
        if self.widen:
            lo, hi = min(w["fw"][0] for w in self.widen), max(w["fw"][1] for w in self.widen)
            self.note(("widen",), u"STREAM WIDENED: ROOM FOR WATER, WETLAND",
                      [u"open ground {:.0f}-{:.0f} m beside the bank (max area)".format(lo, hi)],
                      [w["at"] for w in self.widen])
        if self.arms:
            self.note(("arm",), u"SIDE ARM: REED CHANNEL CLEANS THE RETURN",
                      [u"open ground >= {:.0f} m (max area)".format(BRANCH_MIN), u"H7 downstream working edge (h02 E11)"],
                      [a["at"] for a in self.arms])
        for why, txt in (("building", u"KEPT: BUILDINGS STAND AT THE BANK"), ("road", u"KEPT: A ROAD RUNS AT THE BANK"),
                         ("frame", u"NOTHING PLACED: EDGE OF THE SITE FRAME")):
            at = []
            for k in self.kept:                          # one badge per KEPT_SPACE_M at most (legible plan)
                if k["why"] == why and all(math.hypot(k["at"][0] - q[0], k["at"][1] - q[1]) >= KEPT_SPACE_M for q in at):
                    at.append(k["at"])
            if at:
                self.note(("kept", why), txt, [u"less than {:.0f} m open (max area)".format(KEPT_MAX)], at)
        ft = [c_ for c_ in self.cross if c_["kind"] == "footbridge"]
        if ft:
            self.note(("foot",), u"FOOTBRIDGE: {:.0f}+ m WITHOUT A CROSSING".format(FOOT_GAP_M),
                      [u"crossings K1-K6 (site board p5)", u"both landings open (max area)"], [c_["xy"] for c_ in ft])
        for rd in ROADS + [TOWN_LINE]:
            P = rd["xy"]
            mid = at_len(P, arclen(P), arclen(P)[-1] / 2.0)[0]
            self.note(("road", rd["name"]), rd["note"].upper(), [rd["proof"]], [mid])
        self.notes.sort(key=lambda nt: min(V.uv(p)[0] for p in nt["at"]))
        for i, nt in enumerate(self.notes, 1):
            nt["n"] = i

    def movement(self):
        """masterplan_results.json "movement" (spec §4; survey coordinates)."""
        r2 = lambda p: [round(p[0], 1), round(p[1], 1)]
        roads = [{"name": rd["name"], "change": rd["change"], "note": rd["note"], "reason_proof": rd["proof"],
                  "xy": [r2(p) for p in rd["xy"]]} for rd in ROADS]
        routes = [{"name": TOWN_LINE["name"], "note": TOWN_LINE["note"], "later": True, "change": TOWN_LINE["change"],
                   "reason_proof": TOWN_LINE["proof"], "xy": [r2(p) for p in TOWN_LINE["xy"]]}]   # site board v44
        cross = []
        for c_ in self.cross:
            note = {"bridge kept": u"existing bridge kept", "stepping stones": u"sub-hub crossing, closes in floods",
                    "footbridge": u"{:.0f} m reach without a crossing".format(c_.get("gap", 0.0))}[c_["kind"]]
            cross.append({"name": c_["name"], "kind": c_["kind"], "note": note, "xy": r2(c_["xy"])})
        hubs = [{"name": HUB_NAME[h["id"]], "bridge": h["bridge"], "xy": r2(h["xy"]), "bus_stop": h["stop"],
                 "bus_stop_m": round(h["stop_m"], 0), "sub_hub": bool(h.get("sub_xy")), "role": h["role"]}
                for h in self.hubs]
        return {"roads": roads, "routes": routes, "truck_route": None, "crossings": cross, "hubs": hubs,
                "pending": [u"truck_route: no data names the truck route (no HGV tags in OSM, no KGM count on the "
                            u"streets by the stream, card t01)", u"bus line numbers per hub (only the later town line "
                            u"to K4 is named)"]}


# ================================================================ v24: drawing the corridor on a plan
def ticks_line(pg, P, colour, lw, every, size, side=1.0):
    """A line with short ticks every `every` mm to one side (terrace edges, pergola)."""
    if len(P) < 2:
        return
    pg.line(P, colour, lw)
    s = arclen(P)
    t = every / 2.0
    while t < s[-1]:
        (x, y), (ux, uy) = at_len(P, s, t)
        pg.line([(x, y), (x - uy * size * side, y + ux * size * side)], colour, lw * 0.8)
        t += every


def icon(pg, kind, x, y, s):
    """Pictograms (page mm, centre x, y, size s)."""
    W_, ink = COL["white"], COL["ink_dark"]
    if kind == "cafe":
        pg.poly([rect(x - s * 0.35, y - s * 0.35, x + s * 0.25, y + s * 0.25)], fill=MP["centre"][2])
        pg.circle(x + s * 0.33, y - s * 0.05, s * 0.14, stroke=MP["centre"][2], lw=0.25)
    elif kind == "edu":
        pg.poly([[(x, y - s * 0.3), (x - s * 0.45, y - s * 0.15), (x - s * 0.45, y + s * 0.35), (x, y + s * 0.2)],
                 [(x, y - s * 0.3), (x + s * 0.45, y - s * 0.15), (x + s * 0.45, y + s * 0.35), (x, y + s * 0.2)]],
                fill=COL["accent_dark"])
    elif kind == "seat":
        pg.poly([rect(x - s * 0.4, y - s * 0.1, x + s * 0.4, y + s * 0.1)], fill=ink)
    elif kind == "transit":
        pg.poly([rect(x - s * 0.5, y - s * 0.5, x + s * 0.5, y + s * 0.5)], fill=COL["accent_dark"], stroke=W_, lw=0.3)
        pg.poly([rect(x - s * 0.28, y - s * 0.05, x + s * 0.28, y + s * 0.28)], fill=W_)
        pg.circle(x - s * 0.18, y - s * 0.25, s * 0.09, fill=W_)
        pg.circle(x + s * 0.18, y - s * 0.25, s * 0.09, fill=W_)
    elif kind == "walkhub":
        pg.poly([rect(x - s * 0.5, y - s * 0.5, x + s * 0.5, y + s * 0.5)], fill=SQ_EDGE, stroke=W_, lw=0.3)
        pg.circle(x, y + s * 0.22, s * 0.12, fill=W_)
        pg.line([(x, y + s * 0.08), (x, y - s * 0.3)], W_, 0.35)
    elif kind == "sub":
        pg.poly([[(x, y + s * 0.5), (x + s * 0.5, y), (x, y - s * 0.5), (x - s * 0.5, y)]], fill=COL["river_dark"],
                stroke=W_, lw=0.25)
    elif kind == "gate":
        pg.poly([[(x - s * 0.5, y + s * 0.45), (x + s * 0.5, y), (x - s * 0.5, y - s * 0.45), (x - s * 0.2, y)]],
                fill=COL["ink_dark"])
    elif kind == "view":
        pg.poly([[(x - s * 0.5, y - s * 0.3), (x + s * 0.5, y - s * 0.3), (x, y + s * 0.5)]], fill=COL["accent"])
    elif kind == "deck":
        pg.poly([rect(x - s * 0.5, y - s * 0.3, x + s * 0.5, y + s * 0.3)], fill=COL["histwall"], stroke=W_, lw=0.25)


def badge(pg, n, anchor, taken, W, H, colour=None):
    """A numbered badge on a free spot at or round anchor (page mm), with a leader when moved; True when placed."""
    r = BADGE_R
    ax, ay = anchor
    if not (0.0 <= ax <= W and 0.0 <= ay <= H):
        return False
    for d in (0.0, 3.0, 5.0, 7.5, 10.5, 14.0, 18.0, 23.0, 29.0):
        for i in range(12 if d else 1):
            a = math.radians(i * 30.0 + 15.0)
            cx, cy = ax + math.cos(a) * d, ay + math.sin(a) * d
            b = (cx - r, cy - r, cx + r, cy + r)
            if b[0] < 0.4 or b[1] < 0.4 or b[2] > W - 0.4 or b[3] > H - 0.4 or any(hit(b, t, 0.3) for t in taken):
                continue
            if d > 0.0:
                L = math.hypot(cx - ax, cy - ay) or 1.0
                pg.line([(ax, ay), (cx - (cx - ax) / L * r, cy - (cy - ay) / L * r)], COL["ink_dark"], 0.18)
                pg.circle(ax, ay, 0.35, fill=COL["ink_dark"])
            pg.circle(cx, cy, r + 0.25, fill=COL["white"])
            pg.circle(cx, cy, r, fill=colour or COL["ink_dark"])
            pg.text(str(n), cx, cy - BADGE_TS * 0.36, BADGE_TS, COL["white"], bold=True, align="C")
            taken.append(b)
            return True
    return False


def draw_corridor(pg, T, k, C, inP, taken, dw, dh, detail=False):
    """Every layer of the corridor on plan page pg (T: world -> page mm, k: mm per m; inP: world point on this
    plan). Returns (legend keys used, note numbers placed). detail = the 1:1,000 windows: direct labels, species."""
    used, placed = set(), []
    W_, ink, ink2 = COL["white"], COL["ink_dark"], COL["ink2"]
    vis = lambda TPs: [Q for Q in TPs if hit(bbox(Q), (-2.0, -2.0, dw + 2.0, dh + 2.0))]
    TL = lambda Ls: vis([[T(p) for p in L_] for L_ in Ls])
    # ---- base: buildings, roads (survey), contours
    for role, fill in (("building", COL["bld"]), ("housing", COL["bld"]), ("shed", COL["bld"]),
                       ("heritage", COL["her"])):
        Ps = TL(C.bld.get(role, []))
        if Ps:
            pg.poly(Ps, fill=fill, stroke=COL["her_edge"] if role == "heritage" else None, lw=0.1)
            used.add("bld" if role != "heritage" else "her")
    # ---- the gradient: planting rings from the water (outermost first), programme rings round the hubs
    for t, Ls in reversed(C.eco):
        Ps = TL(Ls)
        if Ps:
            pg.poly(Ps, fill=ECO_COL, alpha=0.14)
            used.add("eco")
    for r_, Ls in reversed(C.rings):
        Ps = TL(Ls)
        if Ps:
            pg.poly(Ps, fill=HUB_COL, alpha=0.16)
            used.add("ring")
    for P in C.roads:
        Q = [T(p) for p in P]
        if hit(bbox(Q), (0.0, 0.0, dw, dh)):
            pg.line(Q, ROAD_TONE[1], 0.18 if k < 0.5 else 0.3)
            used.add("street")
    # ---- water: bed, widened stream, side arms, reed basins, hidden-stream line
    Ps = TL(C.bed_loops)
    if Ps:
        pg.poly(Ps, fill=WATER_COL, alpha=0.85)
        used.add("bed")
    Ps = TL([w["ring"] for w in C.widen])
    if Ps:
        pg.poly(Ps, fill=WET_COL, stroke=COL["river_mid"], lw=0.25)
        used.add("widen")
    for a in C.arms:
        Q = [T(p) for p in a["P"]]
        pg.line(Q, WET_COL, max(1.0, 6.0 * k))
        pg.line(Q, COL["river_mid"], 0.25, [1.0, 0.6])
        used.add("arm")
    for z in C.D.zones:
        if z["code"] == "WT":
            Q = [T(p) for p in z["P"]]
            if hit(bbox(Q), (0.0, 0.0, dw, dh)):
                pg.poly([Q], fill=WET_COL, stroke=COL["river_dark"], lw=0.25,
                        stripes=(COL["river_dark"], 0.9 if k < 0.5 else 1.6, 0.15, 90.0))
                used.add("reed")
        elif z["code"] == "DG":
            Q = [T(p) for p in z["P"]]
            if hit(bbox(Q), (0.0, 0.0, dw, dh)):
                pg.poly([Q], stroke=MP["agriculture"][2], lw=0.3, dash=[1.0, 0.6])
                used.add("dg")
    for P in C.covered:
        pg.line([T(p) for p in P], COL["river_mid"], 0.8 if k < 0.5 else 1.6, [1.6, 0.9], cap=0)
        used.add("hidden")
    for P in C.streams:
        pg.line([T(p) for p in P], COL["river_mid"], 0.15)
    # ---- terraces on the contours (upstream): edge + ticks toward the stream
    for P in C.terr:
        Q = [T(p) for p in P]
        if not hit(bbox(Q), (0.0, 0.0, dw, dh)):
            continue
        mid = P[len(P) // 2]
        c_, _ = chain_at(C.ref, mid)
        q, _ = at_len(C.ref, arclen(C.ref), c_)
        s = arclen(Q)
        (x, y), (ux, uy) = at_len(Q, s, s[-1] / 2.0)
        qx, qy = T(q)
        side = 1.0 if (-uy) * (qx - x) + ux * (qy - y) > 0 else -1.0
        ticks_line(pg, Q, MP["storage"][2], 0.3 if k < 0.5 else 0.45, 1.6 if k < 0.5 else 3.0,
                   0.6 if k < 0.5 else 1.2, side)
        used.add("terrace")
    # ---- trees: forest corridor, tree-planted area, survey trees
    for pts, r_, a_, key in ((C.forest, max(0.45, 2.8 * k), 0.85, "forest"), (C.trees, max(0.45, 2.8 * k), 0.55, "trees")):
        for p in pts:
            x, y = T(p)
            if -1.0 <= x <= dw + 1.0 and -1.0 <= y <= dh + 1.0:
                pg.circle(x, y, r_, fill=COL["tree_mid"] if key == "forest" else COL["tree"], alpha=a_)
                used.add(key)
    # ---- hub squares, plane trees, canopied walkway, seats
    for h in C.hubs:
        Ps = TL(h.get("square") or [])
        if Ps:
            pg.poly(Ps, fill=SQ_FILL, stroke=SQ_EDGE, lw=0.35)
            used.add("square")
            for p in h.get("trees", []):
                x, y = T(p)
                pg.circle(x, y, max(0.7, 4.0 * k), fill="5E7A3A", stroke=W_, lw=0.15)
                used.add("plane")
    for P in C.canopy:
        Q = [T(p) for p in P]
        if hit(bbox(Q), (0.0, 0.0, dw, dh)):
            pg.line(Q, W_, 1.3 if k < 0.5 else 2.4)
            ticks_line(pg, Q, MP["centre"][2], 0.45 if k < 0.5 else 0.6, 1.2 if k < 0.5 else 2.4,
                       0.5 if k < 0.5 else 1.0, 1.0)
            used.add("canopy")
    s_ic = 2.2 if k < 0.5 else 3.0
    for p in C.seats:
        x, y = T(p)
        if 0.0 <= x <= dw and 0.0 <= y <= dh:
            icon(pg, "seat", x, y, s_ic * 0.8)
            used.add("seat")
    # ---- roads changed (OSM) and the later town line
    for rd in ROADS + [TOWN_LINE]:
        Q = [T(p) for p in rd["xy"]]
        if not hit(bbox(Q), (0.0, 0.0, dw, dh)):
            continue
        ch = rd["change"] if rd["change"] in ROAD_CHANGE_COL else "later"
        if ch == "later":
            pg.line(Q, ROAD_CHANGE_COL["later"], 0.6 if k < 0.5 else 0.9, [2.0, 1.0], cap=0)
        else:
            pg.line(Q, ROAD_CHANGE_COL[ch], 1.6 if k < 0.5 else 3.0, alpha=0.75)
        used.add("road_" + ch)
    # ---- crossings
    for c_ in C.cross:
        if c_["kind"] == "footbridge":
            A_, B_ = T(c_["P"][0]), T(c_["P"][1])
            pg.line([A_, B_], W_, 1.4 if k < 0.5 else 2.4, cap=0)
            pg.line([A_, B_], ink, 0.8 if k < 0.5 else 1.4, cap=0)
            used.add("foot")
        elif c_["kind"] == "stepping stones":
            A_, B_ = T(c_["P"][0]), T(c_["P"][1])
            for i in range(5):
                f = (i + 0.5) / 5.0
                pg.circle(A_[0] + (B_[0] - A_[0]) * f, A_[1] + (B_[1] - A_[1]) * f, 0.35 if k < 0.5 else 0.9,
                          fill=ink2)
            used.add("stones")
        else:
            x, y = T(c_["xy"])
            if 0.0 <= x <= dw and 0.0 <= y <= dh:
                pg.poly([rect(x - 0.9, y - 0.9, x + 0.9, y + 0.9)], fill=ink)
                used.add("bridge")
    # ---- pictograms: hubs, sub-hubs, cafes, education, viewing terrace, H4 step, H6 deck, gateway
    ic = []
    for h in C.hubs:
        ic.append(("transit" if h["role"] == "transit" else ("gate" if h["id"] == u"K6" else "walkhub"), h["xy"]))
        if h.get("sub_xy"):
            ic.append(("sub", h["sub_xy"]["c"]))
    for z in C.D.zones:
        if z["code"] in ("GR", "DG"):
            ic.append(("cafe", z["q"]))
        if z["code"] == "WT":
            ic.append(("edu", z["q"]))
        if z["code"] == "WS" or (z["code"] == "WA" and z["tier"] == "F"):
            ic.append(("seat", z["q"]))
    ic += [("edu", CRAFT_XY), ("deck", ROMAN_WALL), ("view", C.terrace["xy"]) if C.terrace else None]
    for it in [i_ for i_ in ic if i_]:
        x, y = T(it[1])
        if 0.0 <= x <= dw and 0.0 <= y <= dh:
            icon(pg, it[0], x, y, s_ic * (1.25 if it[0] in ("transit", "walkhub", "gate") else 1.0))
            taken.append((x - s_ic * 0.6, y - s_ic * 0.6, x + s_ic * 0.6, y + s_ic * 0.6))
            used.add(it[0])
    if C.terrace:                                         # the sightline toward the Trajaneum (off the plan)
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 400.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 400.0)
        x2, y2 = T(p2)
        pg.line([(x, y), (x2, y2)], COL["accent"], 0.35, [1.4, 0.8], cap=0)
        used.add("sight")
    # ---- words: place names (large), then notes (badges) or direct labels (detail)
    big = [(HUB_NAME[h["id"]], h["xy"]) for h in C.hubs] + \
        [(nm, xy) for nm, xy in BRIDGES_K if nm in (u"K1", u"K2")] + PLACES
    for nm, xy in big:
        if inP(xy):
            place_label(pg, [(nm, PLACE_TS if k < 0.5 else PLACE_TS * 1.15, True)], T(xy), taken, dw, dh, ink,
                        d0=1.5, anywhere=False)
    if C.terrace and inP(C.terrace["xy"]):
        x, y = T(C.terrace["xy"])
        p2 = (C.terrace["xy"][0] + C.terrace["dir"][0] * 120.0, C.terrace["xy"][1] + C.terrace["dir"][1] * 120.0)
        x2, y2 = T(p2)
        place_label(pg, [(u"→ TRAJANEUM {:,.0f} m".format(C.terrace["d"]), LAB_TS, True)],
                    (min(max(x2, 1.0), dw - 1.0), min(max(y2, 1.0), dh - 1.0)), taken, dw, dh, COL["accent"], d0=1.0)
    if not detail:
        for nt in C.notes:
            for p in nt["at"]:
                if inP(p) and badge(pg, nt["n"], T(p), taken, dw, dh):
                    if nt["n"] not in placed:
                        placed.append(nt["n"])
        return used, placed
    # ---- detail windows: direct labels, species (which plants go where)
    sp = lambda key: u"{} {}".format(PLANT_AT[key][0], u" ".join(PLANT_AT[key][1]))
    lab = []
    for h in C.hubs:
        if h.get("square"):
            L_ = max(h["square"], key=lambda q: abs(area2(q)))
            lab.append(([(u"HUB SQUARE · DRY, STEP-FREE", LAB_TS, True),
                         (u"plane trees {} · irrigated from storage".format(sp("hub")), LAB_TS, False)], inner_pt(L_), "hub"))
        if h.get("sub_xy"):
            lab.append(([(u"SUB-HUB IN THE BED · STEPPING STONES", LAB_TS, True),
                         (u"closes in floods · {}".format(sp("bed")), LAB_TS, False)], h["sub_xy"]["c"], "bed"))
    if C.forest:
        lab.append(([(u"FOREST CORRIDOR", LAB_TS, True), (u"{} · {} at the water".format(sp("forest"), sp("wet")),
                                                          LAB_TS, False)], None, "forest"))
    if C.trees:
        lab.append(([(u"TREE-PLANTED AREA · {}".format(sp("trees")), LAB_TS, True)], None, "trees"))
    if C.terr:
        lab.append(([(u"TERRACES ON CONTOURS · HOLD RAIN", LAB_TS, True), (sp("terrace"), LAB_TS, False)], None,
                    "terrace"))
    for w in C.widen:
        lab.append(([(u"STREAM WIDENED · WETLAND {}".format(sp("wet")), LAB_TS, True)], w["at"], "widen"))
    for a in C.arms:
        lab.append(([(u"REED SIDE ARM · {}".format(sp("arm")), LAB_TS, True)], a["at"], "arm"))
    for P in C.canopy:
        lab.append(([(u"CANOPIED WALKWAY · SEATS", LAB_TS, True)], None, "canopy"))
        break
    for c_ in C.cross:
        if c_["kind"] == "footbridge":
            lab.append(([(u"FOOTBRIDGE", LAB_TS, True)], c_["xy"], "foot"))
    if C.terrace:
        lab.append(([(u"VIEWING TERRACE → TRAJANEUM", LAB_TS, True)], C.terrace["xy"], "view"))
    lab.append(([(u"STEP TO THE WATER · TABAKLAR HAMAMI", LAB_TS, True)], PLACES[1][1], "h4"))
    lab.append(([(u"DECK · ROMAN BANK WALL", LAB_TS, True)], ROMAN_WALL, "h6"))
    lab.append(([(u"WORKSHOPS · EDUCATION", LAB_TS, True)], CRAFT_XY, "edu"))
    for z in C.D.zones:
        if z["code"] in ("GR", "DG"):
            lab.append(([(u"CAFE", LAB_TS, True)], z["q"], "cafe"))
    pts_of = {"forest": C.forest, "trees": C.trees, "terrace": [p for P in C.terr for p in P],
              "canopy": [p for P in C.canopy for p in P]}
    for lines, at, key in lab:
        if at is None:                                    # the visible point nearest the plan's middle
            cand = [p for p in pts_of.get(key, []) if inP(p)]
            if not cand:
                continue
            at = min(cand, key=lambda p: (T(p)[0] - dw / 2) ** 2 + (T(p)[1] - dh / 2) ** 2)
        if not inP(at):
            continue
        place_label(pg, lines, T(at), taken, dw, dh, ink, d0=1.5, anywhere=True)
        for code in [c_ for k_, v in PLANT_AT.items() if k_ in (key, "wet" if key in ("forest", "widen") else "")
                     for c_ in v[1]]:
            leg(("sp", code))
    return used, placed


# ================================================================ v24: the legend (rebuilt for the corridor)
def _sw_fill(fill, stroke=None, alpha=None, stripes=None):
    def f(pg, x, y, w, h):
        pg.poly([rect(x, y, x + w, y + h)], fill=fill, alpha=alpha, stripes=stripes)
        if stroke:
            pg.poly([rect(x, y, x + w, y + h)], stroke=stroke, lw=0.25)
    return f


def _sw_line(colour, lw, dash=None, alpha=None):
    def f(pg, x, y, w, h):
        pg.line([(x, y + h / 2), (x + w, y + h / 2)], colour, lw, dash, cap=0 if dash else 1, alpha=alpha)
    return f


def _sw_grad(colour):
    def f(pg, x, y, w, h):
        for i in range(4):
            pg.poly([rect(x + w * i / 8.0, y, x + w - w * i / 8.0, y + h)], fill=colour, alpha=0.18)
    return f


def _sw_icon(kind, s=2.4):
    def f(pg, x, y, w, h):
        icon(pg, kind, x + w / 2, y + h / 2, s)
    return f


def _sw_dots(colour, r, alpha):
    def f(pg, x, y, w, h):
        for i in range(4):
            pg.circle(x + w * (i + 0.5) / 4, y + h / 2, r, fill=colour, alpha=alpha)
    return f


def _sw_ticks(colour, lw):
    def f(pg, x, y, w, h):
        ticks_line(pg, [(x, y + h * 0.6), (x + w, y + h * 0.6)], colour, lw, 1.4, 0.7, -1.0)
    return f


LEGEND_V24 = [
    ("eco", u"Planting gradient from the water", _sw_grad(ECO_COL)),
    ("ring", u"Programme: densest at the hubs", _sw_grad(HUB_COL)),
    ("bed", u"Stream bed, amphibious", _sw_fill(WATER_COL, alpha=0.85)),
    ("widen", u"Stream widened, wetland", _sw_fill(WET_COL, COL["river_mid"])),
    ("arm", u"Side arm, reed channel", _sw_line(COL["river_mid"], 0.25, [1.0, 0.6])),
    ("reed", u"Water cleaned: reed basins", _sw_fill(WET_COL, COL["river_dark"], stripes=(COL["river_dark"], 0.9, 0.15, 90.0))),
    ("hidden", u"Hidden stream line in paving", _sw_line(COL["river_mid"], 0.8, [1.6, 0.9])),
    ("terrace", u"Terrace on a contour, holds rain", _sw_ticks(MP["storage"][2], 0.3)),
    ("forest", u"Forest corridor", _sw_dots(COL["tree_mid"], 0.6, 0.85)),
    ("trees", u"Tree-planted area", _sw_dots(COL["tree"], 0.6, 0.55)),
    ("square", u"Hub square, plane trees", _sw_fill(SQ_FILL, SQ_EDGE)),
    ("walkhub", u"Walking hub", _sw_icon("walkhub")),
    ("transit", u"Transit hub, town buses", _sw_icon("transit")),
    ("sub", u"Sub-hub in the bed", _sw_icon("sub")),
    ("stones", u"Stepping-stone crossing", _sw_dots(COL["ink2"], 0.45, None)),
    ("foot", u"New footbridge", _sw_line(COL["ink_dark"], 0.8)),
    ("bridge", u"Bridge kept", _sw_fill(COL["ink_dark"])),
    ("canopy", u"Canopied walkway", _sw_ticks(MP["centre"][2], 0.45)),
    ("seat", u"Seating, streamside seats", _sw_icon("seat")),
    ("cafe", u"Cafe", _sw_icon("cafe")),
    ("edu", u"Education, workshop", _sw_icon("edu")),
    ("view", u"Viewing terrace, sightline", _sw_icon("view")),
    ("deck", u"Deck over archaeology", _sw_icon("deck")),
    ("gate", u"Gateway out", _sw_icon("gate")),
    ("dg", u"Demeter's Garden", _sw_line(MP["agriculture"][2], 0.3, [1.0, 0.6])),
    ("road_calmed", u"Road calmed", _sw_line(ROAD_CHANGE_COL["calmed"], 1.6, alpha=0.75)),
    ("road_pedestrian", u"Road made pedestrian", _sw_line(ROAD_CHANGE_COL["pedestrian"], 1.6, alpha=0.75)),
    ("road_shared", u"Road shared", _sw_line(ROAD_CHANGE_COL["shared"], 1.6, alpha=0.75)),
    ("road_kept", u"Road kept (why: see key)", _sw_line(ROAD_CHANGE_COL["kept"], 1.6, alpha=0.75)),
    ("road_later", u"Town bus line, later step", _sw_line(ROAD_CHANGE_COL["later"], 0.6, [2.0, 1.0])),
    ("bld", u"Building (survey)", _sw_fill(COL["bld"])),
    ("her", u"Heritage building", _sw_fill(COL["her"], COL["her_edge"])),
    ("street", u"Street edge (survey)", _sw_line(ROAD_TONE[1], 0.3))]
# the same as booklet footer entries (fill / line / dot + plain name) for the 1:1,000 crops
LEG_BOOK = {"eco": ("fill", mix(COL["white"], ECO_COL, 0.4)), "ring": ("fill", mix(COL["white"], HUB_COL, 0.45)),
            "bed": ("fill", WATER_COL), "widen": ("fill", WET_COL), "reed": ("fill", WET_COL),
            "hidden": ("line", COL["river_mid"]), "terrace": ("line", MP["storage"][2]), "forest": ("dot", COL["tree_mid"]),
            "trees": ("dot", COL["tree"]), "square": ("fill", SQ_FILL), "sub": ("dot", COL["river_dark"]),
            "stones": ("dot", COL["ink2"]), "foot": ("line", COL["ink_dark"]), "canopy": ("line", MP["centre"][2]),
            "seat": ("line", COL["ink_dark"]), "cafe": ("fill", MP["centre"][2]), "edu": ("fill", COL["accent_dark"]),
            "view": ("dot", COL["accent"]), "deck": ("fill", COL["histwall"]), "transit": ("fill", COL["accent_dark"]),
            "walkhub": ("fill", SQ_EDGE), "road_calmed": ("line", ROAD_CHANGE_COL["calmed"]),
            "road_pedestrian": ("line", ROAD_CHANGE_COL["pedestrian"]), "road_shared": ("line", ROAD_CHANGE_COL["shared"]),
            "road_kept": ("line", ROAD_CHANGE_COL["kept"]), "road_later": ("line", ROAD_CHANGE_COL["later"]),
            "bld": ("fill", COL["bld"]), "her": ("fill", COL["her"])}


def legend_v24_groups():
    """v24: the sheet band's legend group of the 1:1,000 detail sheet (what it draws)."""
    return [(u"CORRIDOR", [(nm, f) for key, nm, f in LEGEND_V24 if ("v24", key) in LEG])]


# ================================================================ v24: the panels (p15 halves, max area, p16 windows)
def _col_blocks(lines, width, size):
    """[(text, bold)] -> [(line, size, bold)] wrapped to width."""
    return [(t, size, bd) for s_, bd in lines for t in wrap(s_, size, width, bd)]


def half_panel(C, h, used_all, warn):
    """One half of the corridor (h = 0 upstream, 1 downstream; the frame turned so the water runs left to right) at
    1:5,000, with its key column: title, north arrow and scale bar, the legend (downstream half: of both halves),
    the numbered notes placed on this half with their reasons. Returns the panel (sh.crop, sh.key...)."""
    V = C.V
    k = 1000.0 / MP_SCALE
    um = (V.u0 + V.u1) / 2.0
    ua, ub = (V.u0, um) if h == 0 else (um, V.u1)
    dw, dh = (ub - ua) * k, (V.v1 - V.v0) * k

    def T(p):
        u, v = V.uv(p)
        return ((u - ua) * k, (v - V.v0) * k)
    inP = lambda p: ua <= V.uv(p)[0] <= ub and V.v0 <= V.uv(p)[1] <= V.v1
    pg = Page(dw, dh)
    used, placed = draw_corridor(pg, T, k, C, inP, [], dw, dh)
    used_all |= used
    return {"pg": pg, "h": h, "dw": dw, "dh": dh, "placed": placed, "ua": ua, "ub": ub}


def compose_half(C, hp, used_all, warn):
    pg, dw, dh, h = hp["pg"], hp["dw"], hp["dh"], hp["h"]
    G_, M = 3.0, 1.0
    W = M + dw + G_ + COL_W + M
    title = [(u"UPSTREAM · ENTRY, K4, K3, K5" if h == 0 else u"DOWNSTREAM · K5 TO THE CONFLUENCE", True)]
    notes = [nt for nt in C.notes if nt["n"] in hp["placed"]]
    leg_items = [(nm, f) for key, nm, f in LEGEND_V24 if key in used_all] if h == 1 else []
    for ts in (KEY_TS, KEY_MIN):                              # the column: title, marks, legend, notes
        cw = COL_W
        ent = []
        for nt in notes:
            ent.append((nt["n"], _col_blocks([(nt["text"], True), (u"← " + u" · ".join(nt["why"]), False)],
                                             cw - 5.0, ts)))
        lh = ts * 1.18
        need = PLACE_TS * 1.2 + 11.0 + (int(math.ceil(len(leg_items) / 2.0)) * 3.6 + 2.0 if leg_items else 0.0) + \
            sum(max(len(b) * lh, 2 * BADGE_R) + 0.8 for _, b in ent)
        if need <= dh:
            break
    if need > dh:
        warn.append(u"masterplan half {}: key column {:.0f} mm for a {:.0f} mm plan: the panel is taller".format(
            h + 1, need, dh))
    H = max(dh, need) + 2 * M
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sh.clip([rect(M, H - M - dh, M + dw, H - M)])
    blit(sh, pg, M, H - M - dh)
    sh.unclip()
    sh.poly([rect(M, H - M - dh, M + dw, H - M)], stroke=COL["ink2"], lw=0.2)
    x0, y = M + dw + G_, H - M
    sh.text(title[0][0], x0, y - PLACE_TS, PLACE_TS, COL["ink_dark"], bold=True)
    y -= PLACE_TS * 1.2 + 2.0
    V = C.V                                                  # north arrow: survey +Y turned with the plan
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    nx_, ny_ = nu, nv
    L = math.hypot(nx_, ny_) or 1.0
    nx_, ny_ = nx_ / L, ny_ / L
    ax, ay = x0 + 3.5, y - 4.5
    tip = (ax + nx_ * 3.5, ay + ny_ * 3.5)
    sh.poly([[tip, (ax - ny_ * 1.6 - nx_ * 3.0, ay + nx_ * 1.6 - ny_ * 3.0), (ax - nx_ * 1.8, ay - ny_ * 1.8)]],
            fill=COL["ink_dark"])
    sh.poly([[tip, (ax - nx_ * 1.8, ay - ny_ * 1.8), (ax + ny_ * 1.6 - nx_ * 3.0, ay - nx_ * 1.6 - ny_ * 3.0)]],
            fill=COL["white"], stroke=COL["ink_dark"], lw=0.15)
    sh.text(u"N", tip[0] + 1.2, tip[1] - 0.6, 2.6, COL["ink_dark"], bold=True)
    scale_bar(sh, x0 + 12.0, y - 6.0, MP_SCALE, (0.0, 50.0, 100.0, 250.0))
    y -= 11.0
    if leg_items:
        cw2 = (COL_W - 3.0) / 2.0
        for i, (nm, f) in enumerate(leg_items):
            cx = x0 + (i % 2) * (cw2 + 3.0)
            cy = y - (i // 2) * 3.6
            f(sh, cx, cy - 2.6, 6.0, 2.4)
            sh.text(nm, cx + 7.0, cy - 2.3, KEY_MIN, COL["ink"], bold=False)
        y -= int(math.ceil(len(leg_items) / 2.0)) * 3.6 + 2.0
    for n, b in ent:
        sh.circle(x0 + BADGE_R, y - BADGE_R, BADGE_R, fill=COL["ink_dark"])
        sh.text(str(n), x0 + BADGE_R, y - BADGE_R - BADGE_TS * 0.36, BADGE_TS, COL["white"], bold=True, align="C")
        draw_block(sh, b, x0 + 5.0, y - 0.4, COL["ink_dark"], None)
        y -= max(len(b) * b[0][1] * 1.18, 2 * BADGE_R) + 0.8
    sh.crop = (0.0, 0.0, W, H)
    cs = [V.xy(hp["ua"], V.v0), V.xy(hp["ub"], V.v1)]
    sh.key, sh.world, sh.scale, sh.pleg = "half{}".format(h), bbox(cs), MP_SCALE, None
    sh.bid = (("mp_upstream", "c1_s1", u"Masterplan upstream: entry, K4, K3, K5") if h == 0 else
              ("mp_downstream", "c1_s2", u"Masterplan downstream: K5 to the confluence"))
    return sh


def max_area_panel(C):
    """The proof panel: the maximum potential area (open ground of the site frame, no building, no road) at
    1:10,000, the frame turned as the halves, with its figures (cell counts x cell area, calculated)."""
    V = C.V
    k = 1000.0 / MA_SCALE
    dw, dh = (V.u1 - V.u0) * k, (V.v1 - V.v0) * k

    def T(p):
        u, v = V.uv(p)
        return ((u - V.u0) * k, (v - V.v0) * k)
    pg = Page(dw, dh)
    TL = lambda Ls: [[T(p) for p in L_] for L_ in Ls]
    pg.poly(TL(C.max_loops), fill="CFE0A8")
    pg.poly(TL(C.road_loops), fill=ROAD_TONE[0])
    for role in ("building", "housing", "shed", "heritage"):
        pg.poly(TL(C.bld.get(role, [])), fill="9C978C")
    pg.poly(TL(C.bed_loops), fill=WATER_COL)
    M, G_ = 1.0, 3.0
    W, H = M + dw + G_ + COL_W + M, M + max(dh, 40.0) + M
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sh.clip([rect(M, H - M - dh, M + dw, H - M)])
    blit(sh, pg, M, H - M - dh)
    sh.unclip()
    sh.poly([rect(M, H - M - dh, M + dw, H - M)], stroke=COL["ink2"], lw=0.2)
    st = C.stats
    tot = sum(st.values()) or 1.0
    x0, y = M + dw + G_, H - M
    rows_ = [(u"MAXIMUM POTENTIAL AREA", PLACE_TS * 0.85, True),
             (u"open ground in the site frame: no building, no road", KEY_TS, False)]
    for ln in rows_:
        y -= ln[1] * 1.18
        sh.text(ln[0], x0, y, ln[1], COL["ink_dark"], bold=ln[2])
    y -= 2.0
    for fill, txt in (("CFE0A8", u"open ground {:.1f} ha · {:.0f} %".format((st[0]) / 1e4, 100.0 * st[0] / tot)),
                      (WATER_COL, u"stream bed {:.1f} ha".format(st[3] / 1e4)),
                      ("9C978C", u"buildings {:.1f} ha · {:.0f} %".format(st[1] / 1e4, 100.0 * st[1] / tot)),
                      (ROAD_TONE[0], u"roads {:.1f} ha · {:.0f} %".format(st[2] / 1e4, 100.0 * st[2] / tot))):
        sh.poly([rect(x0, y - 2.6, x0 + 6.0, y - 0.2)], fill=fill, stroke=COL["ink2"], lw=0.15)
        sh.text(txt, x0 + 7.5, y - 2.3, KEY_TS, COL["ink_dark"])
        y -= 3.6
    sh.text(u"site frame {:.0f} ha · {:.0f} m grid".format(tot / 1e4, C.G.c), x0, y - 2.3, KEY_TS, COL["ink"])
    scale_bar(sh, x0 + 0.0, M + 1.5, MA_SCALE, (0.0, 100.0, 250.0, 500.0))
    sh.crop = (0.0, 0.0, W, H)
    sh.key, sh.world, sh.scale, sh.pleg = "max_area", bbox(V.P), MA_SCALE, None
    sh.bid = ("mp_max_area", "mp_max_area", u"Maximum potential area: open ground in the site frame")
    return sh


def window_panel(C, w, D, CL, spots, plc, missing, warn):
    """A 1:1,000 window (p16), north up: the corridor with every element named, which plants go where (species
    codes of the water board list), seating; the water board cuts, water route and spot levels of the detail
    overlay. No text block under the plan (Aras 27 Oct)."""
    R = w["R"]
    k = 1000.0 / DT_SCALE
    dw, dh = (R[2] - R[0]) * k, (R[3] - R[1]) * k
    T = lambda p: ((p[0] - R[0]) * k, (p[1] - R[1]) * k)
    inP = lambda p: R[0] <= p[0] <= R[2] and R[1] <= p[1] <= R[3]
    _PLEG[0] = {}
    pg = Page(dw, dh)
    taken = []
    used, _ = draw_corridor(pg, T, k, C, inP, taken, dw, dh, detail=True)
    detail_overlay(w, D, CL, spots, plc, missing, warn)(pg, T, k, taken, dw, dh, ())
    for key in used:
        leg(("v24", key))
    M = 12.0
    W, H = M + dw + M, M + dh + 14.0
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    sh.clip([rect(M, M, M + dw, M + dh)])
    blit(sh, pg, M, M)
    sh.unclip()
    sh.text(w["title"] + u" · 1:1,000", M, M + dh + 5.0, 5.0, COL["ink_dark"], bold=True)
    panel_marks(sh, M, 1.5, DT_SCALE, (0.0, 10.0, 20.0, 50.0))
    sh.crop = (M, 0.5, M + dw, M + dh)
    sh.key, sh.world, sh.scale = w["key"], R, DT_SCALE
    pl = dict(_PLEG[0])
    pl.update((("v24", u_), True) for u_ in used)
    sh.pleg, _PLEG[0] = pl, None
    sh.bid = (w["id"], w["old"], w["caption"])
    return sh
