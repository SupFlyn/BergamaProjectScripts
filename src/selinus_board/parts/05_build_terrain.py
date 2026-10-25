def build_terrain(S, R):
    F = S.F
    bb = (F.bb[0] - 150, F.bb[1] - 150, F.bb[2] + 150, F.bb[3] + 150)

    def inb(x, y):
        return bb[0] <= x <= bb[2] and bb[1] <= y <= bb[3]
    smp = [p for p in R["points"].get(DWG["survey"], []) if inb(p[0], p[1]) and p[2] > 0.5]
    for lay in DWG["contours"]:
        for P in R["plines"].get(lay, []):
            last = None
            for p in P:
                if p[2] > 0.5 and inb(p[0], p[1]) and (last is None or math.hypot(p[0] - last[0], p[1] - last[1]) >= 4.0):
                    smp.append(p)
                    last = p
    for lay in DWG["spot_texts"]:
        for t in R["texts"].get(lay, []):
            v = num(t[0])
            if v is not None and 1.0 < v < 2000.0 and "." in t[0] and inb(t[1], t[2]):
                smp.append((t[1], t[2], v))
    n0 = len(smp)
    for lay in DWG["zlines"]:                            # v33: bank tops and toes, stream lines (heights > 1 m only)
        for P in R["plines"].get("Z::" + lay, []):
            last = None
            for p in P:
                if p[2] > 1.0 and inb(p[0], p[1]) and (last is None or math.hypot(p[0] - last[0], p[1] - last[1]) >= 4.0):
                    smp.append(p)
                    last = p
    S.terrain_banks = len(smp) - n0
    S.terrain_n = len(smp)
    S.terrain_ok = len(smp) > 50
    S.terrain_fp = fp(("idw8-nearest", smp))
    S.terrain_smp = smp
    S.z_at = terrain_z_at(S, smp)


def terrain_z_at(S, smp):
    """S.z_at for the terrain samples smp. v18: taken out of build_terrain unchanged, so the worker processes make
    the very same function from the same samples."""
    g = {}
    Cc = 25.0
    for p in smp:
        g.setdefault((int(math.floor(p[0] / Cc)), int(math.floor(p[1] / Cc))), []).append(p)

    gget = g.get

    def z_at(x, y, k=8):
        """Inverse-distance height from the 8 nearest samples. Square rings of 25 m cells are added (each ring
        column by column) until 8 samples are found and no cell outside the rings can hold a nearer one; the
        samples are ranked by distance (ties: the order they were found)."""
        if not S.terrain_ok:
            return 0.0
        i0, j0 = int(math.floor(x / Cc)), int(math.floor(y / Cc))
        found = list(gget((i0, j0), ()))
        r = 0
        while r < 60:
            r += 1
            jl, jh = j0 - r, j0 + r
            for j in range(jl, jh + 1):                      # first column of the ring: every cell
                found += gget((i0 - r, j), ())
            for i in range(i0 - r + 1, i0 + r):              # middle columns: bottom and top cells only
                found += gget((i, jl), ())
                found += gget((i, jh), ())
            for j in range(jl, jh + 1):                      # last column: every cell
                found += gget((i0 + r, j), ())
            if len(found) >= k:
                dk = sorted((p[0] - x) ** 2 + (p[1] - y) ** 2 for p in found)[k - 1]
                if dk <= (r * Cc) ** 2:
                    break
        if not found:
            return 0.0
        d = [(p[0] - x) ** 2 + (p[1] - y) ** 2 for p in found]
        ws = zs = 0.0
        for q in sorted(range(len(found)), key=d.__getitem__)[:k]:
            d2 = d[q]
            if d2 < 0.01:
                return found[q][2]
            w = 1.0 / d2
            ws += w
            zs += w * found[q][2]
        return zs / ws
    return z_at


def pl_chainage(P, x, y):
    """Distance along polyline P to the point of P nearest (x, y)."""
    best, bs, acc = None, 0.0, 0.0
    for i in range(len(P) - 1):
        ax, ay = P[i]
        bx, by = P[i + 1]
        ex, ey = bx - ax, by - ay
        l2 = ex * ex + ey * ey
        L_ = math.sqrt(l2)
        q = 0.0 if l2 < 1e-12 else max(0.0, min(1.0, ((x - ax) * ex + (y - ay) * ey) / l2))
        d = math.hypot(ax + q * ex - x, ay + q * ey - y)
        if best is None or d < best:
            best, bs = d, acc + q * L_
        acc += L_
    return bs


def water_runs(flags):
    """Index runs [k0, k1) where flags is True."""
    out, k = [], 0
    while k < len(flags):
        if not flags[k]:
            k += 1
            continue
        k0 = k
        while k < len(flags) and flags[k]:
            k += 1
        out.append((k0, k))
    return out


def channel_profile(S):
    """How deep the stream bed lies under its banks, from the survey alone. Every 10 m along the main stream a cut
    across the water (0.5 m steps, as the sections are cut): where the surveyed terrain dips at least 1 m below the
    lower bank, that depth is a measurement. Between measured cuts the depth is interpolated along the stream;
    beyond the first and last it is held. S.chan = dict(line, ch, d, n_cuts)."""
    S.chan = dict(line=None, ch=[], d=[], n_cuts=0)
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    if not streams or not getattr(S, "terrain_ok", False):
        return
    main = max(streams, key=pl_length)
    L = pl_length(main)
    ch, dd = [], []
    n_cuts = 0
    s = 5.0
    gB = S.g_bld
    while s < L - 5.0:
        p, t = pl_point_at(main, s)
        nx, ny = -t[1], t[0]
        pts, flags = [], []
        for k in range(-80, 81):
            qx, qy = p[0] + nx * k * 0.5, p[1] + ny * k * 0.5
            if not S.F.inside(qx, qy):
                pts.append(None)
                flags.append(False)
                continue
            pts.append((qx, qy))                         # water as classify_point has it: in the river, not in a building
            flags.append(water_at(S, qx, qy) and not any(in_unit(qx, qy, u) for u in gB.query((qx, qy, qx, qy))))
        runs = water_runs(flags)
        if runs:
            k0, k1 = min(runs, key=lambda rk: 0 if rk[0] <= 80 < rk[1] else min(abs(rk[0] - 80), abs(rk[1] - 1 - 80)))
            a, b = pts[max(0, k0 - 2)], pts[min(len(pts) - 1, k1)]       # the banks, as the sections take them
            if a is not None and b is not None:
                n_cuts += 1
                depth = min(S.z_at(*a), S.z_at(*b)) - min(S.z_at(*pts[i]) for i in range(k0, k1))
                if depth >= 1.0:
                    ch.append(s)
                    dd.append(depth)
        s += 10.0
    S.chan = dict(line=main, ch=ch, d=dd, n_cuts=n_cuts)


def bed_depth(S, x, y):
    """Depth of the bed under the banks at a point of the stream where the survey has no bed level there:
    the channel_depth input if given, else interpolated along the stream from the surveyed depths; None when the
    survey has no bed level anywhere (the bed is then left as surveyed)."""
    if CH_DEPTH is not None:
        return CH_DEPTH
    C = getattr(S, "chan", None)
    if not C or not C["ch"]:
        return None
    s = pl_chainage(C["line"], x, y)
    ch, dd = C["ch"], C["d"]
    if s <= ch[0]:
        return dd[0]
    if s >= ch[-1]:
        return dd[-1]
    for i in range(len(ch) - 1):
        if ch[i] <= s <= ch[i + 1]:
            t = (s - ch[i]) / (ch[i + 1] - ch[i]) if ch[i + 1] > ch[i] else 0.0
            return dd[i] + (dd[i + 1] - dd[i]) * t
    return dd[-1]


def water_level(S, x, y, bed, bank):
    """v16.5: (level of the water surface, source) where the stream crosses a section at (x, y), its bed at bed and its
    lower bank top at bank: the measured levels of the water_levels input interpolated along the stream (within their
    stretch only); else the bed + water_depth (the input, else the APPROXIMATE depth). Never above the lower bank."""
    pts = getattr(S, "water_pts", None)
    C = getattr(S, "chan", None)
    if pts and C and C.get("line"):
        s = pl_chainage(C["line"], x, y)
        q = sorted((pl_chainage(C["line"], px, py), pz) for px, py, pz in pts)
        if len(q) == 1 and abs(s - q[0][0]) <= 50.0:
            return min(bank, max(bed, q[0][1])), "measured"
        for (s0, z0), (s1, z1) in zip(q, q[1:]):
            if s0 <= s <= s1:
                z = z0 if s1 <= s0 else z0 + (z1 - z0) * (s - s0) / (s1 - s0)
                return min(bank, max(bed, z)), "measured"
    return min(bank, bed + WATER_DEPTH), WATER_SRC


def water_key(S):
    """What the water drawn in the sections depends on (cache keys)."""
    return (WATER_DEPTH, WATER_SRC, tuple(getattr(S, "water_pts", None) or ()))


# ============================================================ URBAN FABRIC (building types read from the survey)
# Every building gets one fabric type from what the survey and open data record about it and its surroundings:
# survey layer (historic, ruin, religious, civic...), names, OSM / Overture heritage tags, surveyed floors,
# footprint size and regularity, whether it shares walls, and the grain of the 40 m around it (coverage, how
# aligned the buildings are, sheds). The rules are listed in the legend; the same type is drawn in every section.
FABRIC_ORDER = ["monument", "sacred", "traditional", "block", "regular", "selfbuilt", "large", "construction"]
FABRIC = {
    "monument": ("Monuments & historic buildings", "survey historic / ruin layers, named monuments, heritage tags",
                 C("A8382A")),
    "sacred": ("Mosques & sacred buildings", "survey religious layer, mosque names, places of worship", C("D98A3D")),
    "traditional": ("Old town fabric", "low, attached, organic: dense grain, shared walls, irregular plots",
                    C("2E2C2A")),
    "block": ("Planned apartment blocks", "3+ surveyed floors on regular footprints", C("62605C")),
    "regular": ("Planned low-rise houses", "1-2 floors on regular, aligned plots", C("97948E")),
    "selfbuilt": ("Small irregular houses", "under 130 m2, irregular, loose grain or added sheds; "
                  "the survey's 'Baraka' (shack) labels", C("C9C5BC")),
    "large": ("Civic, school & industrial halls", "public layers, institutions, industry or 1000 m2+", C("FBFAF6")),
    "construction": ("Under construction", "survey 'in construction' layer", C("E9E5DA")),
}
FABRIC_SHORT = {"monument": "Monuments, historic", "sacred": "Mosques & sacred", "traditional": "Old town fabric",
                "block": "Apartment blocks", "regular": "Planned low-rise", "selfbuilt": "Small irregular",
                "large": "Civic & industrial", "construction": "Under construction"}     # legend labels (two columns)
HERITAGE_WORDS = ("tarihi", "harabe", "harap", "kalıntı", "kalinti", "hamam", " han ", "bedesten", "arasta", "türbe",
                  "turbe", "medrese", "kızıl avlu", "kizil avlu", "tapınağı", "tapinagi", "kilise", "sinagog", "çeşme",
                  "cesme", "sebil", "kervansaray", "müze", "muze")
SACRED_WORDS = ("cami", "mescit", "mescid", "cemevi", "tekke", "zaviye")


def fabric_types(S):
    """Fabric type of every survey unit (u["fabric"]) and the measures behind it (u["fm"])."""
    units = S.bld
    if not units:
        return
    # shared walls: an edge (to the centimetre) that belongs to two units
    owner = {}
    for k, u in enumerate(units):
        for P in u["parts"]:
            n = len(P)
            for i in range(n):
                a = (round(P[i][0], 2), round(P[i][1], 2))
                b = (round(P[(i + 1) % n][0], 2), round(P[(i + 1) % n][1], 2))
                key = (a, b) if a <= b else (b, a)
                s_ = owner.get(key)
                if s_ is None:
                    owner[key] = {k}
                else:
                    s_.add(k)
    att = [False] * len(units)
    for s_ in owner.values():
        if len(s_) > 1:
            for k in s_:
                att[k] = True
    for k, u in enumerate(units):
        pts = [p for P in u["parts"] for p in P]
        r = min_area_rect(pts)
        if r:
            area, ang, u0, u1, v0, v1 = r
            rect = u["A"] / max(area, 1e-6)
            ang = ang if (u1 - u0) >= (v1 - v0) else ang + math.pi / 2.0
        else:
            rect, ang = 1.0, 0.0
        u["fm"] = dict(rect=rect, ang=ang, att=att[k])
    grid = {}
    for k, u in enumerate(units):
        grid.setdefault((int(math.floor(u["cx"] / 20.0)), int(math.floor(u["cy"] / 20.0))), []).append(k)
    R = 40.0
    for k, u in enumerate(units):
        i0, j0 = int(math.floor(u["cx"] / 20.0)), int(math.floor(u["cy"] / 20.0))
        nb = [m for i in range(i0 - 2, i0 + 3) for j in range(j0 - 2, j0 + 3) for m in grid.get((i, j), ())
              if math.hypot(units[m]["cx"] - u["cx"], units[m]["cy"] - u["cy"]) <= R]
        mains = [units[m] for m in nb if not units[m]["annex"]]
        w = sum(v["A"] for v in mains) or 1.0
        zx = sum(math.cos(4.0 * v["fm"]["ang"]) * v["A"] for v in mains)
        zy = sum(math.sin(4.0 * v["fm"]["ang"]) * v["A"] for v in mains)
        fm = u["fm"]
        fm["cov"] = sum(units[m]["A"] for m in nb) / (math.pi * R * R)
        fm["coh"] = math.hypot(zx, zy) / w
        fm["attsh"] = sum(1 for v in mains if v["fm"]["att"]) / float(max(1, len(mains)))
        fm["shed"] = sum(1 for m in nb if units[m]["annex"]) / float(max(1, len(mains)))
    her_pois = [p for p in getattr(S, "pois", []) if p.get("her")]
    gH = Grid(30.0)
    for p in her_pois:
        gH.add(p, (p["x"], p["y"], p["x"], p["y"]))
    for u in units:
        if u["annex"]:
            continue
        kind = DWG["bld"].get(u["layer"], "mesken")
        nm = " " + (u.get("name") or "").lower() + " "
        tg = u.get("tags") or {}
        fm = u["fm"]
        her_poi = any(any(pip(p["x"], p["y"], P) for P in u["parts"])
                      for p in gH.query((u["bb"][0] - 1, u["bb"][1] - 1, u["bb"][2] + 1, u["bb"][3] + 1)))
        if (kind in ("tarihi", "harabe") or any(w_ in nm for w_ in HERITAGE_WORDS) or tg.get("historic") or
                tg.get("heritage") or tg.get("building") in ("ruins", "temple", "historic", "synagogue", "church") or her_poi):
            t = "monument"
        elif kind == "dini" or any(w_ in nm for w_ in SACRED_WORDS) or u["cat"] == "religious" or tg.get("building") == "mosque":
            t = "sacred"
        elif kind == "insaat" or u["cat"] == "vacant":
            t = "construction"
        elif (u["cat"] in ("institutional", "industrial", "transport") or
              kind in ("resmi", "okul", "spor", "fabrika", "sera", "akaryakit") or u["A"] >= 1000.0):
            t = "large"
        elif u["floors"] >= 4 or (u["floors"] >= 3 and fm["rect"] >= 0.75):
            t = "block"
        elif fm["cov"] >= 0.35 and fm["attsh"] >= 0.55 and (fm["coh"] < 0.8 or fm["rect"] < 0.85):
            t = "traditional"
        elif u["A"] < 130.0 and (fm["rect"] < 0.8 or fm["coh"] < 0.6) and (fm["shed"] >= 0.15 or fm["attsh"] < 0.5):
            t = "selfbuilt"
        elif fm["rect"] >= 0.8 and fm["coh"] >= 0.6:
            t = "regular"
        elif fm["cov"] >= 0.35:
            t = "traditional"
        else:
            t = "selfbuilt" if (fm["rect"] < 0.8 and u["A"] < 130.0) else "regular"     # small irregular: < 130 m2
        if u.get("baraka"):
            t = "selfbuilt"                              # the survey itself labels it a shack
        u["fabric"] = t
    mains = [u for u in units if not u["annex"]]
    gM = Grid(40.0)
    for u in mains:
        gM.add(u, u["bb"])
    for u in units:                                     # sheds and annexes belong to the house they stand by
        if not u["annex"]:
            continue
        best, bd = None, 1e18
        for v in gM.query((u["cx"] - 40, u["cy"] - 40, u["cx"] + 40, u["cy"] + 40)):
            d = min(pl_dist(u["cx"], u["cy"], P, True) for P in v["parts"])     # the house it stands by
            if d < bd:
                best, bd = v, d
        u["fabric"] = "selfbuilt" if u.get("baraka") else (best["fabric"] if best else "selfbuilt")
    S.fabric_area = dict((k, 0.0) for k in FABRIC_ORDER)
    for u in mains:
        S.fabric_area[u["fabric"]] += u["A"]


# ============================================================ ANALYSES
def run_analyses(S):
    S.int_cells, S.int_breaks, S.int_cell, S.int_peak, S.int_peak_name = [], (0, 0, 0), 50.0, 0.0, ""
    S.corr_primary, S.corr_secondary, S.clusters, S.n_inst = [], [], [], 0
    S.edge_runs, S.wall_runs, S.edge_samples = [], [], []
    S.edge_len = dict((k, 0.0) for k in EDGE_ORDER)
    S.walled_len = 0.0
    S.embanked_len = 0.0
    S.bank_runs = []
    S.sections, S.sec_lines, S.observations = [], [], []
    for fn in (build_intensity, build_corridors, build_clusters, build_edges, build_sections, build_observations):
        try:
            fn(S)
        except Exception:
            LOG.append("{} failed:\n{}".format(fn.__name__, traceback.format_exc()))


def build_intensity(S, cell=10.0):
    """Floor-area ratio on a 10 m grid: every footprint is split exactly across the cells it covers."""
    F = S.F
    if not S.bld:
        return
    acc = {}
    for u in S.bld:
        fl = u["floors"]
        for P in u["parts"]:
            Q = [F.local(x, y) for x, y in P]
            us, vs = [q[0] for q in Q], [q[1] for q in Q]
            for i in range(int(math.floor((min(us) - F.u0) / cell)), int(math.floor((max(us) - F.u0) / cell)) + 1):
                cu = F.u0 + i * cell
                Ci = clip_half(clip_half(Q, cu, 0.0, -1.0, 0.0), cu + cell, 0.0, 1.0, 0.0)
                if len(Ci) < 3:
                    continue
                for j in range(int(math.floor((min(vs) - F.v0) / cell)), int(math.floor((max(vs) - F.v0) / cell)) + 1):
                    cv = F.v0 + j * cell
                    Cj = clip_half(clip_half(Ci, 0.0, cv, 0.0, -1.0), 0.0, cv + cell, 0.0, 1.0)
                    if len(Cj) >= 3:
                        a_ = shoelace(Cj)[0]
                        if a_ > 0.01:
                            acc[(i, j)] = acc.get((i, j), 0.0) + a_ * fl
    far = dict((k, v / (cell * cell)) for k, v in acc.items() if v > 0.0)
    if not far:
        return
    vals = sorted(far.values())

    def q(p):
        return vals[min(len(vals) - 1, int(p * len(vals)))]
    br = (q(0.25), q(0.5), q(0.75))
    cls = lambda f: 0 if f < br[0] else (1 if f < br[1] else (2 if f < br[2] else 3))
    rows = {}
    for (i, j), f in far.items():
        rows.setdefault(j, []).append((i, cls(f)))
    for j, lst in rows.items():                         # merge equal neighbours in a row into one strip
        lst.sort()
        k = 0
        while k < len(lst):
            i0, c0 = lst[k]
            i1 = i0
            while k + 1 < len(lst) and lst[k + 1][0] == i1 + 1 and lst[k + 1][1] == c0:
                k += 1
                i1 = lst[k][0]
            u0, u1 = F.u0 + i0 * cell, F.u0 + (i1 + 1) * cell
            v0, v1 = F.v0 + j * cell, F.v0 + (j + 1) * cell
            S.int_cells.append(([F.world(u0, v0), F.world(u1, v0), F.world(u1, v1), F.world(u0, v1)], c0, j))
            k += 1
    S.int_breaks, S.int_cell = br, cell
    (pi, pj), pf = max(far.items(), key=lambda kv: kv[1])
    S.int_peak = pf
    px, py = F.world(F.u0 + (pi + 0.5) * cell, F.v0 + (pj + 0.5) * cell)
    named = [r for r in S.roads + S.paths if r["tags"].get("name")]
    if named:
        r = min(named, key=lambda r: pl_dist(px, py, r["P"], False))
        if pl_dist(px, py, r["P"], False) < 40.0:
            S.int_peak_name = r["tags"]["name"]


def build_corridors(S):
    skip = {"service", "track", "motorway", "motorway_link", "footway", "path", "steps", "cycleway",
            "bridleway", "corridor"}
    groups = {}
    grid = Grid(60.0)
    for r in S.roads + S.paths:
        if r["tags"].get("highway") in skip:
            continue
        name = r["tags"].get("name", "")
        key = name if name else "#{}".format(id(r))
        g = groups.setdefault(key, dict(label=name or "an unnamed street", Ps=[], n=0))
        g["Ps"].append(r["P"])
        r["grp"] = g
        grid.add(r, r["bb"])
    pts = [(u["cx"], u["cy"]) for u in S.bld if u["cat"] in ("commercial", "mixed") and not u["annex"]]
    pts += [(p["x"], p["y"]) for p in S.pois if p["cat"] == "commercial" and not p["in_bld"]]
    for x, y in pts:
        best, bd = None, 30.0
        for r in grid.query((x - 30, y - 30, x + 30, y + 30)):
            d = pl_dist(x, y, r["P"], False)
            if d < bd:
                bd, best = d, r.get("grp")
        if best is not None:
            best["n"] += 1
    ranked = sorted([g for g in groups.values() if g["n"] >= 3], key=lambda g: -g["n"])
    S.corr_primary = [g for g in ranked if g["n"] >= 6][:2]
    S.corr_secondary = [g for g in ranked if all(g is not p for p in S.corr_primary)][:4]


def build_clusters(S, D=100.0):
    pts = [(u["cx"], u["cy"]) for u in S.bld if u["cat"] in ("institutional", "religious") and not u["annex"]]
    pts += [(p["x"], p["y"]) for p in S.pois if p["cat"] in ("institutional", "religious") and not p["in_bld"]]
    n = len(pts)
    S.n_inst = n
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    g = Grid(D)
    for i, p in enumerate(pts):
        g.add(i, (p[0], p[1], p[0], p[1]))
    for i, p in enumerate(pts):
        for j in g.query((p[0] - D, p[1] - D, p[0] + D, p[1] + D)):
            if j > i and (pts[j][0] - p[0]) ** 2 + (pts[j][1] - p[1]) ** 2 <= D * D:
                parent[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(pts[i])
    for grp in groups.values():
        if len(grp) < 3:
            continue
        cx = sum(p[0] for p in grp) / len(grp)
        cy = sum(p[1] for p in grp) / len(grp)
        h = hull(grp)
        if len(h) < 3:
            r = max(math.hypot(p[0] - cx, p[1] - cy) for p in grp) + 25.0
            h = circle_pts(cx, cy, r, 28)
        else:
            infl = []
            for hx, hy in h:
                d = math.hypot(hx - cx, hy - cy) or 1.0
                infl.append((hx + (hx - cx) / d * 25.0, hy + (hy - cy) / d * 25.0))
            h = infl
        S.clusters.append(dict(P=h, n=len(grp)))


def zone_dist(x, y, z):
    if region_contains(x, y, z["Ps"], z["Hs"]):
        return 0.0
    return min(pl_dist(x, y, P, True) for P in z["Ps"] + z["Hs"])         # from inside a hole: to the hole's edge


def edge_type(S, x, y):
    best, bd = None, 1e9
    for u in S.g_bld.query((x - 8, y - 8, x + 8, y + 8)):
        d = min(pl_dist(x, y, P, True) for P in u["parts"])
        if d < 8.0 and d < bd:
            bd, best = d, "building"
    for r in S.g_path.query((x - 21, y - 21, x + 21, y + 21)):            # measured path widths reach 30 m
        d = pl_dist(x, y, r["P"], False) - street_w(r) / 2.0
        if d < 6.0 and d < bd:
            bd, best = d, "pedestrian"
    for P in S.g_stairs.query((x - 5, y - 5, x + 5, y + 5)):
        d = pl_dist(x, y, P, False)
        if d < 5.0 and d < bd:
            bd, best = d, "pedestrian"
    for r in S.g_road.query((x - 23, y - 23, x + 23, y + 23)):
        d = pl_dist(x, y, r["P"], False) - street_w(r) / 2.0
        if d < 8.0 and d < bd:
            bd, best = d, "street"
    for P in S.g_redge.query((x - 7, y - 7, x + 7, y + 7)):
        d = pl_dist(x, y, P, False) + 1.0
        if d < 7.0 and d < bd:
            bd, best = d, "street"
    for z in S.g_park.query((x - 8, y - 8, x + 8, y + 8)):
        d = zone_dist(x, y, z)
        if d < 8.0 and d < bd:
            bd, best = d, "parking"
    for z in S.g_green.query((x - 8, y - 8, x + 8, y + 8)) + S.g_agri.query((x - 8, y - 8, x + 8, y + 8)):
        d = zone_dist(x, y, z)
        if d < 8.0 and d < bd:
            bd, best = d, "green"
    if best is None:
        for t in S.g_tree.query((x - 6, y - 6, x + 6, y + 6)):
            if math.hypot(t[0] - x, t[1] - y) < 6.0:
                best = "green"
                break
    return best or "open"


def build_edges(S):
    SP = 4.0
    F = S.F
    for P in getattr(S, "water_outline", []):
        if len(P) < 2:
            continue
        seq = []
        for x, y in resample(P, SP):
            if pl_dist(x, y, F.P, True) < 3.0:
                seq.append(None)
                continue
            t = edge_type(S, x, y)
            # 1: a surveyed wall within 3 m, 2: only a surveyed slope line (an embankment), 0: neither
            wl = 1 if any(pl_dist(x, y, W, False) < 3.0 for W in S.g_wall.query((x - 3, y - 3, x + 3, y + 3))) else (
                2 if any(pl_dist(x, y, W, False) < 3.0 for W in S.g_slope.query((x - 3, y - 3, x + 3, y + 3))) else 0)
            seq.append((x, y, t, wl))
            S.edge_samples.append((x, y, t, wl))
            S.edge_len[t] += SP
            if wl == 1:
                S.walled_len += SP
            elif wl == 2:
                S.embanked_len += SP
        S.edge_runs.extend(make_runs(seq, 2))
        S.wall_runs.extend([pts for flag, pts in make_runs(seq, 3) if flag == 1])
        S.bank_runs.extend([pts for flag, pts in make_runs(seq, 3) if flag == 2])
    S.g_edge = Grid(20.0)
    for e in S.edge_samples:
        S.g_edge.add(e, (e[0], e[1], e[0], e[1]))


def in_unit(x, y, u):
    """Inside a building's outline and not in one of its courtyards."""
    return any(pip(x, y, P) for P in u["parts"]) and not any(pip(x, y, H) for H in u.get("holes") or ())


def classify_point(S, x, y):
    q = (x, y, x, y)
    for u in S.g_bld.query(q):
        if in_unit(x, y, u):
            return "bld", u
    if water_at(S, x, y):
        return "water", None
    M = getattr(S, "road_mask", None)
    if M is not None:                                  # the street surfaces as drawn on the plan
        if mask_at(S.F, M, x, y):
            return "road", None
    else:
        for r in S.g_road.query((x - 16, y - 16, x + 16, y + 16)):      # measured widths reach 30 m
            w = r.get("w")
            if w and pl_dist(x, y, r["P"], False) < w / 2.0:
                return "road", None
        for r in S.g_path.query((x - 16, y - 16, x + 16, y + 16)):
            w = r.get("w")
            if w and pl_dist(x, y, r["P"], False) < w / 2.0:
                return "road", None
    for z in S.g_green.query(q):
        if region_contains(x, y, z["Ps"], z["Hs"]):
            return "green", None
    for z in S.g_park.query(q):
        if region_contains(x, y, z["Ps"], z["Hs"]):
            return "parking", None
    for z in S.g_vac.query(q):
        if region_contains(x, y, z["Ps"], z["Hs"]):
            return "vacant", None
    for z in S.g_agri.query(q):
        if region_contains(x, y, z["Ps"], z["Hs"]):
            return "agri", None
    return "void", None


def sec_endpoints(ln):
    """Start and end of a section line (a curve, a Line, or two points); None if it has no length."""
    e = None
    for get in (lambda: (ln.PointAtStart, ln.PointAtEnd), lambda: (ln.From, ln.To)):
        try:
            a, b = get()
            e = ((a.X, a.Y), (b.X, b.Y))
            break
        except Exception:
            pass
    if e is None:
        try:
            e = ((float(ln[0][0]), float(ln[0][1])), (float(ln[1][0]), float(ln[1][1])))
        except Exception:
            return None
    if math.hypot(e[1][0] - e[0][0], e[1][1] - e[0][1]) < 1e-6:
        return None
    return e


def build_sections(S):
    lines_ = []
    for k, ln in enumerate(SEC_IN):
        e = sec_endpoints(ln)
        if e is None:
            continue
        runs = S.F.clip_line([e[0], e[1]])
        if not runs:
            LOG.append("Section line {} lies outside the frame and was skipped.".format(k + 1))
            continue
        a, b = runs[0][0], runs[0][-1]
        if math.hypot(a[0] - e[0][0], a[1] - e[0][1]) + math.hypot(b[0] - e[1][0], b[1] - e[1][1]) > 1.0:
            LOG.append("Section line {} was trimmed to the frame.".format(k + 1))
        lines_.append((a, b))
    if SEC_IN and not lines_:
        LOG.append("WARNING: none of the {} section lines cross the study area. If they were drawn before you rotated or "
                   "moved the drawing, redraw them across the stream (or rotate them with it).".format(len(SEC_IN)))
    S.sections_auto = False
    step = 0.5
    n_kept = 0
    for i, ((x0, y0), (x1, y1)) in enumerate(lines_):
        L = math.hypot(x1 - x0, y1 - y0)
        if L < 5.0:
            LOG.append("A section line shorter than 5 m inside the frame was skipped.")
            continue
        n_kept += 1
        name = "S{}".format(n_kept)
        S.sec_lines.append((x0, y0, x1, y1, name))
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        xs = [k * step for k in range(int(L / step) + 1)]
        smp = []
        for s in xs:
            px, py = x0 + ux * s, y0 + uy * s
            kind, ref = classify_point(S, px, py)
            smp.append([s, kind, ref, S.z_at(px, py)])
        # water intervals: the bed where the survey levels it; elsewhere the depth interpolated along the stream
        # from the surveyed depths (bed_depth). v16.5: the water surface from water_level (approximate unless measured).
        k = 0
        wat = []
        wsrcs = []
        while k < len(smp):
            if smp[k][1] != "water":
                k += 1
                continue
            k0 = k
            while k < len(smp) and smp[k][1] == "water":
                k += 1
            za = smp[max(0, k0 - 2)][3]
            zb = smp[min(len(smp) - 1, k)][3]
            bank = min(za, zb)
            bed = min(r[3] for r in smp[k0:k])
            src = "surveyed"
            if bank - bed < 1.0:
                sm = (smp[k0][0] + smp[k - 1][0]) / 2.0
                dd_ = bed_depth(S, x0 + ux * sm, y0 + uy * sm)
                if dd_ is None:
                    src = "terrain"
                else:
                    bed, src = bank - dd_, ("input" if CH_DEPTH is not None else "interpolated")
            for r in smp[k0:k]:
                r.append(bed)
            sm_ = (smp[k0][0] + smp[k - 1][0]) / 2.0
            lvl, wsrc = water_level(S, x0 + ux * sm_, y0 + uy * sm_, bed, bank)
            wat.append((smp[k0][0], smp[k - 1][0] + step, bed, lvl, bank, src))
            wsrcs.append(wsrc)
        for r in smp:
            if len(r) == 4:
                r.append(r[3])
        base = min(r[4] for r in smp) - 2.0
        ground = [(r[0], r[4] - base) for r in smp]
        runs, cur = [], None
        for r in smp:
            key = (r[1], id(r[2]) if r[2] is not None else 0)
            if cur is None or cur["key"] != key:
                if cur:
                    runs.append(cur)
                cur = dict(key=key, kind=r[1], ref=r[2], s=[r])
            else:
                cur["s"].append(r)
        if cur:
            runs.append(cur)
        bl, strip, comp, trees = [], [], {}, []
        zmax = max(g[1] for g in ground)
        for r in runs:
            s0 = r["s"][0][0]
            s1 = min(L, r["s"][-1][0] + step)
            if r["kind"] == "bld":
                u = r["ref"]
                zb = min(q[3] for q in r["s"]) - base
                ms_ = minaret_s(u, x0, y0, ux, uy, s0, s1) if u.get("fabric") == "sacred" else None
                bl.append((s0, s1, zb, zb + u["h"], u["cat"], u["annex"], u.get("fabric", "regular"),
                           unit_flags(u) + (ms_, label_name(u)), u["floors"], u["floors_src"]))  # + minaret, name
                zmax = max(zmax, zb + u["h"] + typo_rise(u.get("fabric", "regular"), u["cat"], s1 - s0, u["h"],
                                                         ms_ is not None) + 1.0)
                cat = u["cat"]
            elif r["kind"] == "water":
                cat = "water"
            elif r["kind"] == "green":
                cat = "green"
            elif r["kind"] in ("road", "parking"):
                cat = "transport"
            elif r["kind"] == "vacant":
                cat = "vacant"
            elif r["kind"] == "agri":
                cat = "agri"
            else:
                cat = "void"
            strip.append((s0, s1, cat))
            comp[cat] = comp.get(cat, 0.0) + (s1 - s0)

        def g_at(s):
            return ground[max(0, min(len(ground) - 1, int(round(s / step))))][1]
        # ---- tree crowns as measured on the canopy height map: cut by the line, and those seen beyond it
        nx, ny = -uy, ux
        btrees = []
        for (tx, ty, tr, th) in crowns_near(S, (min(x0, x1) - 80, min(y0, y1) - 80, max(x0, x1) + 80, max(y0, y1) + 80)):
            d = (tx - x0) * nx + (ty - y0) * ny
            s = (tx - x0) * ux + (ty - y0) * uy
            if not (-tr < s < L + tr):
                continue
            lo, hi = crown_lo(th), th
            if abs(d) < tr:
                hw = math.sqrt(tr * tr - d * d)
                trees.append((s, S.z_at(tx, ty) - base, hw, lo, hi))
                zmax = max(zmax, S.z_at(tx, ty) - base + hi)
            elif tr <= d < 60.0:
                btrees.append((s, S.z_at(tx, ty) - base, tr, lo, hi, d))
        btrees.sort(key=lambda t: -t[5])
        # ---- surveyed walls crossing the line: their place only (the survey gives no wall heights)
        walls, chwalls = [], []
        sbb = (min(x0, x1) - 5, min(y0, y1) - 5, max(x0, x1) + 5, max(y0, y1) + 5)
        for P in S.g_wall.query(sbb):
            for k in range(len(P) - 1):
                res = seg_x((x0, y0), (x1 - x0, y1 - y0), P[k], (P[k + 1][0] - P[k][0], P[k + 1][1] - P[k][1]))
                if res:
                    s = res[0] * L
                    walls.append((s, g_at(s)))
        labels, levels = [], []
        for (s0, s1, bed, lvl, bank, src) in wat:
            for s in (s0, s1):
                px, py = x0 + ux * s, y0 + uy * s
                best, bd = None, 12.0
                for e in S.g_edge.query((px - 12, py - 12, px + 12, py + 12)):
                    d = math.hypot(e[0] - px, e[1] - py)
                    if d < bd:
                        bd, best = d, e
                if best:
                    labels.append((s, best[2], best[3], bank - base))
                    if best[3] == 1:
                        chwalls.append((s, bed - base, bank - base))     # the channel wall, bed to bank
            levels.append(((s0 + s1) / 2.0, bed - base, bed, "bed"))
            levels.append((s0, bank - base, bank, "bank"))
        levels.append((0.0, ground[0][1], ground[0][1] + base, "end"))
        levels.append((L, ground[-1][1], ground[-1][1] + base, "end"))
        # ---- what lies beyond the cut, looking to the left of S -> S'
        zcut = zmax
        band = (min(x0, x1) - 80, min(y0, y1) - 80, max(x0, x1) + 80, max(y0, y1) + 80)
        beyond = []
        for u in S.g_bld.query(band):
            d = (u["cx"] - x0) * nx + (u["cy"] - y0) * ny
            if not 1.5 < d < 75.0:
                continue
            sv = [(px - x0) * ux + (py - y0) * uy for P in u["parts"] for (px, py) in P]
            a, b = max(0.0, min(sv)), min(L, max(sv))
            if b - a < 1.5:
                continue
            zb = S.z_at(u["cx"], u["cy"]) - base
            beyond.append((a, b, zb, min(zb + u["h"], zcut + 5.0), u["cat"], d, u["floors"], u["annex"],
                           u.get("fabric", "regular"), unit_flags(u), u["floors_src"]))
        beyond.sort(key=lambda t: -t[5])
        for b_ in beyond:
            zmax = max(zmax, min(b_[3] + 1.6, zcut + 6.0))
        for t in btrees:
            zmax = max(zmax, min(t[1] + t[4], zcut + 6.0))
        bridges = []
        for P in S.bridges:
            if len(P) < 2:
                continue
            mx, my = sum(p[0] for p in P) / len(P), sum(p[1] for p in P) / len(P)
            d = (mx - x0) * nx + (my - y0) * ny
            if not 2.0 < d < 120.0:
                continue
            sv = [(px - x0) * ux + (py - y0) * uy for (px, py) in P]
            a, b = max(0.0, min(sv)), min(L, max(sv))
            if b - a > 2.0:
                bridges.append((a, b, S.z_at(mx, my) - base, d))
        # v16.7: named parks and places the line crosses (OpenStreetMap areas with their own name), called out by name
        places = []
        lbb = (min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))
        for z in S.zones:
            nm_ = proper_name((z.get("tags") or {}).get("name") or "")
            if not nm_ or not bb_hit(z["bb"], lbb):
                continue
            ins = [s for s in xs if region_contains(x0 + ux * s, y0 + uy * s, z["Ps"], z.get("Hs") or [])]
            if len(ins) >= 4:
                places.append((ins[0], ins[-1] + step, nm_))
        S.sections.append(dict(name=name, line=(x0, y0, x1, y1, name), L=L, ground=ground, bld=bl, trees=trees, walls=walls,
                               chwalls=chwalls, water=[(a, b, bed - base, lvl - base) for (a, b, bed, lvl, bank, src) in wat],
                               bed_src=[src for (a, b, bed, lvl, bank, src) in wat], water_src=wsrcs,
                               labels=labels, levels=levels, strip=strip, comp=comp, zmax=zmax, base=base,
                               beyond=beyond, btrees=btrees, bridges=bridges, places=places))


def crown_lo(h):
    """Height where a crown starts above the ground: the analyses' convention (35 % of the measured top, at least
    1.5 m), the canopy map gives the top height and the crown radius, not the crown base."""
    return max(1.5, 0.35 * h)


def crowns_near(S, bb):
    """Tree crowns measured on the 1 m canopy height map (Meta / WRI) as (x, y, radius, top height), from env_path;
    crowns standing on a roof are misreadings and left out, as in the analyses. Empty without the environment file."""
    g = getattr(S, "g_crown", None)
    if g is None:
        E = (getattr(S, "env", None) or {}).get("E")
        if E is None and ENV_PATH:
            E, _ = load_env(ENV_PATH)
        fb = S.F.bb
        g = Grid(20.0)
        for row in (E or {}).get("trees", []):
            x, y, r, h = row[:4]
            if h < 3.0 or not (fb[0] - 80 <= x <= fb[2] + 80 and fb[1] - 80 <= y <= fb[3] + 80):
                continue
            if any(in_unit(x, y, u) for u in S.g_bld.query((x, y, x, y))):
                continue
            g.add((x, y, r, h), (x, y, x, y))
        S.g_crown = g
    return g.query(bb)


NAME_GENERIC = {"cami", "camii", "mescit", "mescid", "trafo", "w.c", "wc", "w.c.", "depo", "baraka", "okul", "park",
                "bahçe", "bahce", "havuz", "türbe", "turbe", "çeşme", "cesme", "mezar", "mezarlık", "mezarlik", "kilise",
                "hamam", "harabe", "kalıntı", "kalinti", "sundurma", "ahır", "ahir", "garaj", "dükkan", "dukkan", "yapı",
                "yapi", "bina", "inş", "ins", "inşaat", "insaat", "halinde", "fabrika", "fab", "atölye", "atolye",
                "kulübe", "kulube", "ambar", "samanlık", "tuvalet", "büfe", "bufe", "kahve", "kahvehane", "lojman",
                "monument", "mosque", "ruin", "place", "of", "worship", "sanayi", "sanayii", "sitesi", "harap", "kule",
                "tarihi", "salonu", "düğün", "dugun", "sahne"}


def proper_name(nm):
    """v16.7: the name itself when it names this one place (Ulu Camii, Kızıl Avlu), '' when it is only a type word
    (Cami, Trafo, Depo) or a number. Never invents or translates: the name is returned as the source spells it."""
    nm = " ".join((nm or "").split())
    if any(c_ in nm for c_ in "§�") or nm.lower().endswith(("mahallesi", "mahalle")):
        return ""                                        # a garbled spelling, or a neighbourhood's name
    h_ = nm.split()
    if len(h_) % 2 == 0 and h_[:len(h_) // 2] == h_[len(h_) // 2:]:
        nm = " ".join(h_[:len(h_) // 2])                 # the same name entered twice
    words = [w.strip(".,;:()-/").lower() for w in nm.split()]
    rest = [w for w in words if w and w not in NAME_GENERIC and not w.replace(".", "").isdigit()]
    return nm if any(len(w) >= 3 for w in rest) else ""


def label_name(u):
    """v16.7: the name drawn on a cut building in place of its type word: only for monuments, sacred buildings, civic
    halls and other civic or religious buildings that a source names (shops, hotels and houses keep their type)."""
    if not u or not u.get("proper"):
        return ""
    if u.get("fabric") in ("monument", "sacred", "large") or u.get("cat") in ("religious", "institutional"):
        return u["proper"]
    return ""


def live_unit(S, u):
    """v16.7: this run's building for a cached copy of it (cached solids keep the unit as it was when they were made,
    without the names added in v16.7). Matched by its centre."""
    if not u or "proper" in u:
        return u
    lk = getattr(S, "_live_units", None)
    if lk is None:
        lk = S._live_units = dict(((round(v["cx"], 2), round(v["cy"], 2)), v) for v in S.bld if "cx" in v)
    return lk.get((round(u.get("cx", 0.0), 2), round(u.get("cy", 0.0), 2)), u)


def unit_flags(u):
    """(mosque, minaret, ruin) as the survey records them: names, the minaret symbol, the ruin layer."""
    nm = " " + (u.get("name") or "").lower() + " "
    kind = DWG["bld"].get(u.get("layer"), "mesken")
    mosque = any(w in nm for w in ("cami", "mescit", "mescid")) or (kind == "dini" and bool(u.get("minaret")))
    ruin = kind == "harabe" or any(w in nm for w in ("harabe", "harap", "kalıntı", "kalinti"))
    return (mosque or bool(u.get("minaret")), bool(u.get("minaret")), ruin)


def build_observations(S):
    obs = []
    tot = S.total_area
    land = [(k, S.area[k]) for k in CAT_ORDER if S.area.get(k, 0) > 0 and k != "water"]
    if land:
        k, a = max(land, key=lambda t: t[1])
        obs.append((CAT[k][1], "{} carries the ground: {:.1f}% of all mapped cover, {:.2f} ha.".format(
            CAT[k][0], 100.0 * a / tot, a / 1e4)))
    bc = 100.0 * S.built_area / S.frame_area
    obs.append((INK, "Solid {:.0f}%, void {:.0f}%: a {} grain whose voids are streets, courtyards and the stream bed.".format(
        bc, 100.0 - bc, "tight" if bc > 40 else ("loose" if bc < 22 else "measured"))))
    surv = [u for u in S.bld if u["floors_src"] == "survey" and not u["annex"]]
    if surv:
        one = 100.0 * len([u for u in surv if u["floors"] == 1]) / len(surv)
        avg = sum(u["floors"] for u in surv) / float(len(surv))
        obs.append((CAT["residential"][1], "A low skyline: {:.0f}% of surveyed buildings stand a single storey; "
                                           "the mean is {:.1f} floors.".format(one, avg)))
    if S.corr_primary:
        names = [g["label"] for g in (S.corr_primary + S.corr_secondary)[:3]]
        obs.append((CAT["commercial"][1], "Commerce gathers along {}, where ground floors open to the street.".format(
            join_names(names))))
    obs.append((CAT["green"][1], "Green holds {:.1f}% of the frame; {} larger ground{} anchor{} a thin, broken weave.".format(
        S.green_pct, S.n_major_green, "" if S.n_major_green == 1 else "s", "s" if S.n_major_green == 1 else "") +
        green_sat_note(S)))
    if S.clusters:
        obs.append((CAT["institutional"][1], "{} civic constellation{} gather the town's public life.".format(
            len(S.clusters), "" if len(S.clusters) == 1 else "s")))
    te = sum(S.edge_len.values())
    if te > 0:
        k = max(S.edge_len, key=S.edge_len.get)
        obs.append((CAT["water"][1], "Along the Selinus, {} dominate ({:.0f}% of {:.0f} m of bank); {:.0f}% of the banks "
                                     "are walled and {:.0f}% embanked, a seam the town mostly turns its back on.".format(
            EDGE[k][2], 100.0 * S.edge_len[k] / te, te, 100.0 * S.walled_len / te, 100.0 * S.embanked_len / te)))
    S.observations = obs


# ============================================================ TEXT METRICS
# Rhino's text height is the CAPITAL height. Courier New advances ~1.05 x height per character,
# Arial/Josefin capitals ~0.92 x height. All wrapping and column fitting uses these widths.
ADV = {"mono": 1.05, "sans": 0.92}


def kind_of(font):
    return "mono" if font == FONT_BODY else "sans"


def tw(txt, h, kind="mono"):
    return len(txt) * h * ADV[kind]


def wrap(txt, width, h, kind="mono"):
    return textwrap.wrap(txt, max(6, int(width / (h * ADV[kind]))))


def short(label):
    return label.split(" · ")[0]


# ============================================================ BOARD MODEL (pure geometry, baked at the end)
class Board(object):
    """Pure-geometry drawing list. Every item remembers its drawing (group) and layer root."""

    def __init__(self):
        self.items = []
        self.group = None
        self.root = "LU_BOARD"

    def begin(self, group, root):
        self.group, self.root = group, root

    def _lay(self, layer):
        return self.root + layer[len("LU_BOARD"):] if layer.startswith("LU_BOARD") else layer

    def fill(self, polys, color, layer, order):
        polys = [P for P in polys if P and len(P) >= 3]
        if polys:
            self.items.append(("fill", polys, color, self._lay(layer), order, self.group))

    def line(self, P, color, layer, order, w=0.13):
        if P and len(P) >= 2:
            self.items.append(("line", P, color, self._lay(layer), order, w, self.group))

    def hatch(self, polys, color, layer, order, spacing, ang=math.radians(45.0), w=0.03):
        """v16.5: parallel hatch lines over the area of polys (outer rings and holes, even-odd), spacing apart in page
        units at angle ang. Baked as a Rhino hatch (pattern "SELINUS lines"); as plain lines where that fails."""
        polys = [P for P in polys if P and len(P) >= 3]
        if polys and spacing > 0:
            self.items.append(("hatch", polys, color, self._lay(layer), order, spacing, ang, w, self.group))

    def image(self, path, x0, y0, x1, y1, layer, order=5):
        self.items.append(("image", path, (x0, y0, x1, y1), self._lay(layer), order, self.group))

    def text(self, txt, x, y, h, color, layer, order=40, font=None, bold=False, align="L", angle=0.0, italic=False):
        self.items.append(("text", txt, (x, y), h, color, self._lay(layer), order, font or FONT_BODY, bold, align,
                           angle, italic, self.group))

    def para(self, txt, x, y, width, h, color, layer, lead=1.8, font=None, order=40):
        """Wrapped paragraph; returns the y below it."""
        k = kind_of(font or FONT_BODY)
        for ln in wrap(txt, width, h, k):
            self.text(ln, x, y, h, color, layer, order, font)
            y -= h * lead
        return y

    def para_fit(self, txt, x, y, width, h, ymin, color, layer, lead=1.8, font=None, order=40):
        """Wrapped paragraph kept above ymin: the text is made smaller, step by step, until its last line fits."""
        k = kind_of(font or FONT_BODY)
        for _ in range(16):
            if y - (len(wrap(txt, width, h, k)) - 1) * h * lead >= ymin:
                break
            h *= 0.94
        return self.para(txt, x, y, width, h, color, layer, lead=lead, font=font, order=order)

    def fit(self, txt, x, y, h, width, color, layer, **kw):
        """Single line, shrunk to fit the width if needed."""
        k = kind_of(kw.get("font") or FONT_BODY)
        need = tw(txt, h, k)
        if need > width > 0:
            h *= width / need
        self.text(txt, x, y, h, color, layer, **kw)
        return h


class View(object):
    def __init__(self, F, s, X0, Ytop):
        self.F, self.s, self.X0, self.Yt = F, s, X0, Ytop

    def p(self, x, y):
        u, v = self.F.local(x, y)
        return (self.X0 + self.s * (u - self.F.u0), self.Yt + self.s * (v - self.F.v1))

    def P(self, pts):
        return [self.p(x, y) for x, y in pts]

    def Ps(self, lst):
        return [self.P(P) for P in lst if P]

    def angle(self, tx, ty):
        a0 = self.F.local(0.0, 0.0)
        a1 = self.F.local(tx, ty)
        a = math.atan2(a1[1] - a0[1], a1[0] - a0[0])
        while a > math.pi / 2:
            a -= math.pi
        while a <= -math.pi / 2:
            a += math.pi
        return a


def view_fit(F, x, ytop, bw, bh):
    s = min(bw / F.w, bh / F.h)
    return View(F, s, x + (bw - F.w * s) / 2.0, ytop), F.w * s, F.h * s


def hatch_lines(Ps, Hs, bb, spacing, ang):
    d = (math.cos(ang), math.sin(ang))
    nrm = (-d[1], d[0])
    cx, cy = 0.5 * (bb[0] + bb[2]), 0.5 * (bb[1] + bb[3])
    R = 0.5 * math.hypot(bb[2] - bb[0], bb[3] - bb[1]) + spacing
    out = []
    k = -R
    while k <= R and len(out) < 600:
        ox, oy = cx + nrm[0] * k, cy + nrm[1] * k
        a = (ox - d[0] * R, oy - d[1] * R)
        r = (2 * d[0] * R, 2 * d[1] * R)
        ts = []
        for P in Ps + Hs:
            for i in range(len(P)):
                q, q2 = P[i], P[(i + 1) % len(P)]
                res = seg_x(a, r, q, (q2[0] - q[0], q2[1] - q[1]))
                if res:
                    ts.append(res[0])
        ts.sort()
        for i in range(0, len(ts) - 1, 2):
            out.append([(a[0] + r[0] * ts[i], a[1] + r[1] * ts[i]), (a[0] + r[0] * ts[i + 1], a[1] + r[1] * ts[i + 1])])
        k += spacing
    return out


def hatch_segments(polys, spacing, ang):
    """v16.5: the hatch lines of an area (rings: outer and holes alike, even-odd) as segments [(p, q)]: lines at angle
    ang, spacing apart, on one grid for every area (neighbouring areas line up). numpy; the old scanner without it."""
    if not HAVE_NP:
        bb = bb_pts([p for P in polys for p in P])
        return hatch_lines(polys, [], bb, spacing, ang)
    ca, sa = math.cos(ang), math.sin(ang)
    ua, va, ub, vb = [], [], [], []
    for P in polys:
        a = np.asarray(P, float)
        if len(a) < 3:
            continue
        b = np.roll(a, -1, axis=0)
        ua.append(ca * a[:, 0] + sa * a[:, 1])
        va.append(-sa * a[:, 0] + ca * a[:, 1])
        ub.append(ca * b[:, 0] + sa * b[:, 1])
        vb.append(-sa * b[:, 0] + ca * b[:, 1])
    if not ua:
        return []
    ua, va, ub, vb = (np.concatenate(q) for q in (ua, va, ub, vb))
    lo, hi = np.minimum(va, vb), np.maximum(va, vb)
    k0 = np.ceil(lo / spacing).astype(np.int64)
    k1 = np.ceil(hi / spacing).astype(np.int64) - 1          # half-open [lo, hi): every closed ring crosses a line evenly
    n = np.maximum(0, k1 - k0 + 1)
    n[va == vb] = 0
    tot = int(n.sum())
    if tot == 0:
        return []
    idx = np.repeat(np.arange(len(n)), n)
    off = np.repeat(np.cumsum(n) - n, n)
    kk = k0[idx] + (np.arange(tot) - off)
    v = kk * spacing
    u = ua[idx] + (v - va[idx]) * (ub[idx] - ua[idx]) / (vb[idx] - va[idx])
    o = np.lexsort((u, kk))
    kk, u, v = kk[o], u[o], v[o]
    out = []
    if len(kk) % 2 == 0 and np.all(kk[0::2] == kk[1::2]):
        pairs = zip(u[0::2], u[1::2], v[0::2])
    else:                                                   # an open ring: pair within each line only
        pairs = []
        for k in np.unique(kk):
            m = kk == k
            uu, vv = u[m], v[m][0]
            pairs += [(uu[i], uu[i + 1], vv) for i in range(0, len(uu) - 1, 2)]
    tiny = 0.15 * spacing
    for u0, u1, vv in pairs:
        if u1 - u0 > tiny:
            out.append([(ca * u0 - sa * vv, sa * u0 + ca * vv), (ca * u1 - sa * vv, sa * u1 + ca * vv)])
    return out


def draw_scalebar(B, x, y, scale, Lm, U, L, h=0.42):
    seg = Lm / 4.0
    bh = 0.38 * U
    for i in range(4):
        x0 = x + i * seg * scale
        B.fill([rect(x0, y, x0 + seg * scale, y + bh)], INK if i % 2 == 0 else KHAKI, L, 20)
    B.line(rect(x, y, x + Lm * scale, y + bh) + [(x, y)], INK, L, 21, 0.08)
    labs = [(v, "{:g}".format(v)) for v in (0.0, 2 * seg, Lm)]
    wd = [tw(t, h * U) for _, t in labs]
    gap = 0.3 * U                                     # a label is left out rather than run into its neighbour
    keep = [Lm * scale >= 0.5 * (wd[0] + wd[2]) + gap,
            2 * seg * scale >= 0.5 * (wd[0] + wd[1]) + gap and 2 * seg * scale >= 0.5 * (wd[1] + wd[2]) + gap, True]
    for (v, t), k in zip(labs, keep):
        if k:
            B.text(t, x + v * scale, y + bh + 0.35 * U, h * U, INK, L, align="C")
    B.text("m", x + Lm * scale + 0.9 * U, y, h * U, INK, L)


def draw_north_small(B, V, mw, mh, U, L, size=0.55):
    """Small north arrow kept fully inside the top-right corner of a map, in the foreground."""
    k = size * U
    x = V.X0 + mw - 1.2 * k - 0.35 * U
    y = V.Yt - 1.75 * k - 0.35 * U
    a = math.atan2(math.cos(V.F.ang), math.sin(V.F.ang))
    c, s = math.cos(a - math.pi / 2), math.sin(a - math.pi / 2)

    def R(px, py):
        return (x + c * px - s * py, y + s * px + c * py)
    tip, l, m, r = R(0, 0.75 * k), R(-0.38 * k, -0.5 * k), R(0, -0.22 * k), R(0.38 * k, -0.5 * k)
    B.fill([[tip, l, m]], INK, L, 60)
    B.fill([[tip, m, r]], KHAKI, L, 60)
    B.line([tip, l, m, r, tip], INK, L, 61, 0.05)
    nx, ny = R(0, 1.12 * k)
    B.text("N", nx, ny, 0.42 * k, INK, L, order=61, font=FONT_TITLE, bold=True, align="MC")


def draw_symbol(B, kind, col, x, y, U, L, sw=1.1, sh=0.62):
    y0, y1 = y - 0.05 * U, y + sh * U
    ym = 0.5 * (y0 + y1)
    seg = [(x, ym), (x + sw * U, ym)]
    if kind == "box":
        B.fill([rect(x, y0, x + sw * U, y1)], col, L, 20)
        B.line(rect(x, y0, x + sw * U, y1) + [(x, y0)], INK2, L, 21, 0.05)
    elif kind == "line":
        B.line(seg, col, L, 21, 0.5)
    elif kind == "thick":
        B.line(seg, col, L, 21, EDGE_W)
    elif kind == "dash":
        for d in dashes(seg, 0.32 * U, 0.2 * U):
            B.line(d, col, L, 21, 0.3)
    elif kind == "walled":
        B.line(seg, col, L, 21, EDGE_W)
        for d in dashes(seg, 0.22 * U, 0.18 * U):
            B.line(d, PAPER, L, 22, EDGE_MARK_W)
    elif kind == "embanked":
        B.line(seg, col, L, 21, EDGE_W)
        for d in dashes(seg, 0.06 * U, 0.22 * U):
            B.line(d, PAPER, L, 22, EDGE_MARK_W)
    elif kind == "dot":
        B.fill([circle_pts(x + 0.5 * sw * U, ym, 0.28 * U, 12)], col, L, 21)
    elif kind == "thin":                              # v33: stream thresholds on the plan
        B.line(seg, col, L, 21, THRESH_W)
    elif kind == "dense":
        B.line(seg, col, L, 21, 0.22)
    elif kind == "ktick":                             # v40: plan 01's bridge tick, conflict and photo dots
        B.line([(x + 0.5 * sw * U, y0 - 0.1 * U), (x + 0.5 * sw * U, y1 + 0.1 * U)], col, L, 21, 0.3)
    elif kind == "cdot":
        B.fill([circle_pts(x + 0.5 * sw * U, ym, 0.17 * U, 12)], col, L, 21)
    elif kind == "pdot":
        B.fill([circle_pts(x + 0.5 * sw * U, ym, 0.13 * U, 12)], col, L, 21)
    elif kind == "street":
        B.line(seg, col, L, 21, 0.42)
        B.line(seg, ROAD_FILL if ROAD_SOLID else (255, 255, 255), L, 22, 0.3)     # v16.7: the solid street colour


