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
    n_cuts = n_crest = 0
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
                # v50 (MIRAQUA 28 Oct, bank depth REPORT §4 1a): below the lower bank CREST (the water board's rule,
                # site28_cut_top, out from the bed point); the ground just outside the water where a side shows none
                zb_ = [S.z_at(*pts[i]) for i in range(k0, k1)]
                ib_ = min(range(len(zb_)), key=zb_.__getitem__)
                top_ = site28_cut_top(S, pts[k0 + ib_], nx, ny)
                n_crest += top_ is not None
                depth = (min(S.z_at(*a), S.z_at(*b)) if top_ is None else top_) - zb_[ib_]
                if depth >= 1.0:
                    ch.append(s)
                    dd.append(depth)
        s += 10.0
    S.chan = dict(line=main, ch=ch, d=dd, n_cuts=n_cuts)
    LOG.append("Stream depth below the banks: the lower bank crest (the water board's rule) at {} of {} cuts every "
               "10 m; at the others the ground just outside the water.".format(n_crest, n_cuts))


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


# v48 (Aras 27 Oct 20:51 "Move the line"): the 4th cut IS the water board's S4 (its detail section v2 at the flat
# downstream end: the 62 m north-east bank cut, bed +43.59; DETAIL_SRC S4_A -> S4_B), in survey coordinates: the S4
# that selinos.gh picked in Nilnoktali-BERGAMA_layerekli.3dm (SECTION_LINES_LK[3]). Trimmed to the frame as every cut.
S4_WB = ((30616.354683, 30540.470648), (31489.513378, 31161.826317))


# v59 (round 4, P05.1 / N4 b, Aras 1 Nov 11:42): S5 ran ALONG the stream (1,140.7 m, three crossings, no banks, ~3 m
# relief: "looks weird"). It is now a cut ACROSS the stream at one of its three crossings: the crossing inside the
# study area (calisma_alan) with the most bank data in the level table (terraces + banks with a crest; reading taken
# for "the most designed edge": the shelves and crests the project designs on), ties to the first; at right angles to
# the stream there (the stream's direction = the old line turned by the level table's angle_deg of that crossing, to
# the side where the survey's water runs on longer), as long as the mean of the cuts S1-S4, centred on the crossing,
# trimmed to the frame. The level row of that crossing is the cut's only row (sd_["p45_cross"]); every key map
# reads the new line (LV_ENDS_OVERRIDE, common/levels.py). Drawing rules, not data: the 1 m water samples, the
# 5-60 m direction test.
S5_CROSS = {}                                         # v59: dict(rid, line, why) of this run (empty = S5 unchanged)


def s5_cross_line(S, a, b, others):
    """v59 (P05.1 / N4 b): ((x0, y0), (x1, y1), rid, why) of the cut across the stream that replaces S5 (a -> b,
    the old line); None when no crossing of the old line matches a level row"""
    try:
        rows = [r for r in level_ids() if (level_cut(r).get("cut") == "S5")]
    except Exception:
        return None
    if not rows:
        return None
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    if L < 5.0:
        return None
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L

    def wet(px, py):
        try:
            return classify_point(S, px, py)[0] == "water"
        except Exception:
            return False
    runs, cur = [], None
    for i in range(int(L) + 1):
        if wet(a[0] + ux * i, a[1] + uy * i):
            cur = [i, i] if cur is None else [cur[0], i]
        elif cur is not None:
            runs.append(cur)
            cur = None
    if cur is not None:
        runs.append(cur)
    study = getattr(S, "r28_study", None) or [list(P_) for P_ in R28_STUDY_COPY]
    cands = []
    for s0, s1 in runs:
        zs = [S.z_at(a[0] + ux * s_, a[1] + uy * s_) for s_ in range(int(s0), int(s1) + 1)]
        zs = [z for z in zs if z is not None]
        if not zs:
            continue
        zb = min(zs)
        rid = min(rows, key=lambda r: abs((level(r, "bed") or 1e9) - zb))
        if abs((level(rid, "bed") or 1e9) - zb) > 3.0:
            continue
        sm = 0.5 * (s0 + s1)
        c = (a[0] + ux * sm, a[1] + uy * sm)
        row = level_cut(rid)
        score = len(row.get("terraces") or []) + sum(1 for sd in ("NE", "SW")
                                                     if (row.get(sd) or {}).get("type") not in (None, "no_crest"))
        cands.append((sc_inside(c, study), score, rid, c))
    if not cands:
        return None
    inside = [q for q in cands if q[0]]
    pick = max(inside or cands, key=lambda q: q[1])
    _in, score, rid, c = pick
    th = math.radians(level(rid, "angle_deg") or 90.0)
    best = None
    for sg in (1.0, -1.0):                               # the stream's direction: the side with the longer water run
        dx, dy = ux * math.cos(sg * th) - uy * math.sin(sg * th), ux * math.sin(sg * th) + uy * math.cos(sg * th)
        n_w = sum(1 for d in range(5, 65, 5) for e in (1.0, -1.0) if wet(c[0] + e * d * dx, c[1] + e * d * dy))
        if best is None or n_w > best[0]:
            best = (n_w, dx, dy)
    _n, dx, dy = best
    nx, ny = -dy, dx                                     # across the stream
    if nx * ux + ny * uy < 0:                            # the first end on the old line's first side
        nx, ny = -nx, -ny
    lens = [math.hypot(q[1][0] - q[0][0], q[1][1] - q[0][1]) for q in others]
    Lc = sum(lens) / len(lens) if lens else 550.0
    p0, p1 = (c[0] - nx * 0.5 * Lc, c[1] - ny * 0.5 * Lc), (c[0] + nx * 0.5 * Lc, c[1] + ny * 0.5 * Lc)
    runs_ = S.F.clip_line([p0, p1]) or []
    run = next((r_ for r_ in runs_ if min(math.hypot(q[0] - c[0], q[1] - c[1]) for q in r_) < 0.6 * Lc), None)
    if not run:
        return None
    why = (u"S5 is a cut across the stream at crossing {} ({}; {} terrace(s) and crested banks: score {}; {} the "
           u"study area), {:.0f} m long (mean of S1-S4), at right angles to the stream".format(
               level_cut(rid).get("crossing"), rid, len(level_cut(rid).get("terraces") or []), score,
               u"inside" if _in else u"FLAG no crossing inside", Lc))
    return run[0], run[-1], rid, why


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
    s4 = S.F.clip_line([S4_WB[0], S4_WB[1]]) if len(lines_) >= 3 else None    # v48: S4 = the water board's S4
    if s4:
        s4 = (s4[0][0], s4[0][-1])
        if len(lines_) >= 4:
            lines_[3] = s4
            LOG.append("Section S4 is the water board's S4 (its 62 m north-east bank cut; S4_WB), {:.0f} m inside the "
                       "frame, in place of the 4th line picked or on sec_lines.".format(
                           math.hypot(s4[1][0] - s4[0][0], s4[1][1] - s4[0][1])))
        else:
            lines_.append(s4)
            LOG.append("Section S4 added: the water board's S4 (S4_WB), {:.0f} m inside the frame.".format(
                math.hypot(s4[1][0] - s4[0][0], s4[1][1] - s4[0][1])))
    elif len(lines_) >= 3:
        LOG.append("WARNING: the water board's S4 (S4_WB) does not cross the frame; S4 stays the 4th line picked.")
    S5_CROSS.clear()                                      # v59 (P05.1 / N4 b): S5 across the stream at one crossing
    LV_ENDS_OVERRIDE.pop("S5", None)
    if len(lines_) >= 5:
        try:
            q_ = s5_cross_line(S, lines_[4][0], lines_[4][1], lines_[:4])
        except Exception:
            q_ = None
            LOG.append("WARNING: S5 could not be turned across the stream (kept as drawn):\n" + traceback.format_exc())
        if q_:
            lines_[4] = (q_[0], q_[1])
            S5_CROSS.update(rid=q_[2], line=(q_[0], q_[1]), why=q_[3])
            LV_ENDS_OVERRIDE["S5"] = (q_[0], q_[1])
            LOG.append(q_[3] + ".")
        else:
            LOG.append("FLAG S5: no crossing of the S5 line matches a level row: S5 drawn as picked (along the stream).")
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
        S.sections.append(section_of_line(S, x0, y0, x1, y1, name, step))
        if name == "S5" and S5_CROSS:                    # v59: its one level row (p45_banks)
            S.sections[-1]["p45_cross"] = S5_CROSS["rid"]


def section_of_line(S, x0, y0, x1, y1, name, step=0.5):
    """v40: one straight section x0,y0 -> x1,y1 (was the body of build_sections): ground, water, buildings, trees,
    walls, levels, what lies beyond; the dict draw_section_strip draws."""
    L = math.hypot(x1 - x0, y1 - y0)
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
    crs = []                                             # v50: each crossing's bank top (site28_bank_top / _rule)
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
        # v50 (MIRAQUA 28 Oct, bank depth REPORT §4 1a): the bank top = the lower bank CREST (the water board's
        # rule) out from the bed, along the cut or, where the cut runs along the stream, across it at the bed; the
        # ground just outside the water (as before) where a side shows none
        cr_ = site28_bank_top(S, smp, k0, k, step, x0, y0, ux, uy)
        old_ = bank
        if cr_["crest"] is not None:
            bank = cr_["crest"]
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
        cr_.update(site28_bank_rule(cr_, bed, old_, (k - k0) * step))   # v50 (1b-1e): the DSİ walls, no bed, width
        crs.append(cr_)
        wat.append((smp[k0][0], smp[k - 1][0] + step, bed, lvl, cr_["top"], src))
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
    btrees, trees_sp, btrees_sp = [], [], []          # v61 (G6-10): *_sp = (species, source, inferred) per tree
    for (tx, ty, tr, th, lf_, ls_) in crowns_near_full(S, (min(x0, x1) - 80, min(y0, y1) - 80, max(x0, x1) + 80,
                                                           max(y0, y1) + 80)):
        d = (tx - x0) * nx + (ty - y0) * ny
        s = (tx - x0) * ux + (ty - y0) * uy
        if not (-tr < s < L + tr):
            continue
        lo, hi = crown_lo(th), th
        if abs(d) < tr:
            hw = math.sqrt(tr * tr - d * d)
            trees.append((s, S.z_at(tx, ty) - base, hw, lo, hi))
            trees_sp.append(sb_tree_species(S, tx, ty, lf_, ls_, tr, th))
            zmax = max(zmax, S.z_at(tx, ty) - base + hi)
        elif tr <= d < 60.0:
            btrees.append((s, S.z_at(tx, ty) - base, tr, lo, hi, d))
            btrees_sp.append(sb_tree_species(S, tx, ty, lf_, ls_, tr, th))
    o_ = sorted(range(len(btrees)), key=lambda i_: -btrees[i_][5])
    btrees, btrees_sp = [btrees[i_] for i_ in o_], [btrees_sp[i_] for i_ in o_]
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
    for (s0, s1, bed, lvl, bank, src), cr_ in zip(wat, crs):
        for s in (s0, s1):
            px, py = x0 + ux * s, y0 + uy * s
            best, bd = None, 12.0
            for e in S.g_edge.query((px - 12, py - 12, px + 12, py + 12)):
                d = math.hypot(e[0] - px, e[1] - py)
                if d < bd:
                    bd, best = d, e
            if best:
                labels.append((s, best[2], best[3], bank - base))
                if best[3] == 1 and cr_["kind"] != "wall":
                    chwalls.append((s, bed - base, bank - base))     # the channel wall, bed to bank
            if cr_["kind"] == "wall":                     # v50 (REPORT §4 1b): the DSİ walls, bed to wall top
                chwalls.append((s, bed - base, bank - base))
                zmax = max(zmax, bank - base + 0.5)
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
    return dict(name=name, line=(x0, y0, x1, y1, name), L=L, ground=ground, bld=bl, trees=trees, walls=walls,
                chwalls=chwalls, water=[(a, b, bed - base, lvl - base) for (a, b, bed, lvl, bank, src) in wat],
                bed_src=[src for (a, b, bed, lvl, bank, src) in wat], water_src=wsrcs,
                labels=labels, levels=levels, strip=strip, comp=comp, zmax=zmax, base=base,
                beyond=beyond, btrees=btrees, bridges=bridges, places=places, trees_sp=trees_sp, btrees_sp=btrees_sp,
                banks=crs)                                # v50: per crossing, its bank top (site28_bank_rule)


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


def crowns_near_full(S, bb):
    """v61 (G6-10): as crowns_near, each crown as (x, y, radius, top height, leaf, leaf_src) from the same env rows
    (leaf: CLC+ 0 deciduous / 1 evergreen broadleaf / 2 needle-leaved; leaf_src 1-3, 3 = nearest pixel, the weakest);
    None where the row has no such field."""
    g = getattr(S, "g_crown_full", None)
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
            lf = row[4] if len(row) > 4 else None
            ls = row[5] if len(row) > 5 else None
            g.add((x, y, r, h, lf, ls), (x, y, x, y))
        S.g_crown_full = g
    return g.query(bb)


SB_TREE_N = {}       # v61 (G6-10): page -> {species key: n}; "generic" = no supported species


def sb_tree_species(S, x, y, leaf=None, leaf_src=None, r=None, h=None, page=None):
    """v61 (G6-10, Aras 4 Nov 17:54): the species of one existing tree from common/trees.py tree_species() (the rule
    of revision_2026-11-04_round6/plan_findings/tree_species.md: named trees, leaf type, place); returns
    (species_key or None, source_key or None, inferred). None = generic (no invented species). The crown dict
    carries what the rule keys on: position, leaf, leaf_src, zone kind/sub, near the stream."""
    zk, zs = None, None
    try:
        for z in S.zones:
            if bb_hit(z["bb"], (x, y, x, y)) and region_contains(x, y, z["Ps"], z.get("Hs") or []):
                zk, zs = z.get("kind"), z.get("sub")
                break
    except Exception:
        pass
    try:
        ns = bool(near_stream(S, x, y, globals().get("TREE_BANK_M", 15.0)))
    except Exception:
        ns = None
    try:
        ub = any(in_unit(x, y, u) for u in S.g_bld.query((x - 30, y - 30, x + 30, y + 30)))
    except Exception:
        ub = None
    res, key = (None, None, False), None
    if "tree_species" in globals():
        try:                                             # S2 trees.py: tree_species(crown, bank, farm) -> (key, src, inf)
            key, src_, inf_ = tree_species(dict(x=x, y=y, r=r, h=h, leaf=leaf, leaf_src=leaf_src),   # noqa: F821
                                           bank=ns, farm=(zk == "agri" or zs == "orchard"))
            gl_ = None
            if key not in TREE_GENERIC:                                                      # noqa: F821
                gl_ = (TREE_SPECIES.get(key) or {}).get("glyph")                             # noqa: F821
            res = (gl_, src_, inf_)                      # drawable species key, else None = generic primitive
        except Exception:
            res, key = (None, None, False), None
    if page:
        c_ = SB_TREE_N.setdefault(page, {})
        k_ = key or "tree"
        c_[k_] = c_.get(k_, 0) + 1
    return res


def sb_tree_log(page):
    """v61 (G6-10) log line `trees <page> species=<n> generic=<n>` (tree_log of common/trees.py when present)"""
    c_ = SB_TREE_N.get(page) or {}
    if "tree_log" in globals():                          # S2: counts by species key, generic keys counted apart
        try:
            return tree_log(page, dict(c_))                                                  # noqa: F821
        except Exception:
            pass
    return u"trees %s species=0 generic=%d (FLAG: common/trees.py not in this build)" % (page, sum(c_.values()))


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
        return sb_landmark(u["proper"])                  # v59 closing (G-R4-11): a table landmark by its one spelling
    return ""


# v59 (round 4 closing, G-R4-11; was p02_p03's P03_LANDMARK_ALIAS): a landmark as the survey or a source spells it
# (or its English translation) -> its key in common/data/NAMES.py "landmarks". Only forms the names table itself
# records: survey labels named in its "src" (Ulu Camii, Kızıl Avlu, Çizmeciler Arastası, İstiklal Meydanı) and the
# variants round 3 / S1 replaced (Red Hall, Red Basilica, Acropolis, Ulu Cami). Whole names only (lower case, single
# spaces, İ as i). A survey name with no row here prints as surveyed (a Turkish proper name, never translated).
SB_LANDMARK_ALIAS = {u"ulu camii": "ulucami", u"ulu cami": "ulucami", u"ulu camı": "ulucami",
                     u"kızıl avlu": "kizil_avlu", u"kizil avlu": "kizil_avlu", u"red hall": "kizil_avlu",
                     u"red basilica": "kizil_avlu", u"acropolis": "akropol",
                     u"çizmeciler arastası": "cizmeciler_arastasi", u"istiklal meydanı": "istiklal_meydani"}


def sb_landmark(nm):
    """v59 closing (G-R4-11): nm by the names table's one spelling (landmark_name) when it is a landmark the table
    records in another form (SB_LANDMARK_ALIAS), else nm as given"""
    key = SB_LANDMARK_ALIAS.get(u" ".join((nm or u"").split()).lower().replace(u"i\u0307", u"i"))
    return landmark_name(key) if key else nm


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
ADV = {"mono": 0.92, "sans": 0.92}                   # v50 (G2): the body font is Arial too (was Courier, mono 1.05)


def kind_of(font):
    return "mono" if font == FONT_BODY else "sans"


def tw(txt, h, kind="mono", bold=False):
    """v59 (round 4, G-R4-1): the REAL Arial advance width of txt at capital height h, in the units of h
    (common/font_metrics.py, the font the sheet PDFs embed; was len x h x 0.92). A character Arial lacks is measured
    as "?" (the PDF writer cannot show it either); a missing font raises FontMissing."""
    if not txt:
        return 0.0
    pt = h / _PDF_CAP["sans"] / FM_PT
    try:
        return fm_width(txt, pt, bold)
    except ValueError:
        out = 0.0
        for ch in txt:
            try:
                out += fm_width(ch, pt, bold)
            except ValueError:
                out += fm_width(u"?", pt, bold)
        return out


def wrap(txt, width, h, kind="mono", bold=False):
    """v59 (round 4, G-R4-1/G-R4-2): txt broken into lines no wider than width by the REAL widths (tw); a word wider
    than width keeps its own line; no single-word last line (widow): the last word of the line above moves down when
    the two then fit (else the text is left as set, which the page check shows)."""
    words = u"%s" % (txt or u"")
    words = words.split()
    if not words:
        return []
    sp = tw(u" ", h, kind, bold)
    lines, cur, cw = [], [], 0.0
    for w_ in words:
        ww = tw(w_, h, kind, bold)
        if cur and cw + sp + ww > width:
            lines.append(cur)
            cur, cw = [w_], ww
        else:
            cw = cw + (sp if cur else 0.0) + ww
            cur.append(w_)
    lines.append(cur)
    if len(lines) >= 2 and len(lines[-1]) == 1 and len(lines[-2]) >= 3:
        cand = [lines[-2][-1]] + lines[-1]
        if tw(u" ".join(cand), h, kind, bold) <= width:
            lines[-2], lines[-1] = lines[-2][:-1], cand
    return [u" ".join(L) for L in lines]


def short(label):
    return label.split(" · ")[0]


# ============================================================ BOARD MODEL (pure geometry, baked at the end)
class Board(object):
    """Pure-geometry drawing list. Every item remembers its drawing (group) and layer root."""

    def __init__(self):
        self.items = []
        self.group = None
        self.root = "LU_BOARD"
        self.tg = None                                   # v59: the open text group (tgroup); None = one per text
        self._tgn = 0
        self.tags = {}                                   # v61 (G6-9): item index -> "<kind>/<element id>"
        self._kind = None                                # the open element kind (B.kind), None = untagged
        self._eid = None
        self._eidn = {}

    def kind(self, kind, eid=None):
        """v61 (round 6, G6-9, Aras 4 Nov 17:50-17:51): `with B.kind("trees", "0412"):` tags every item drawn inside
        as one element of that kind (eid None = each item its own element, numbered per kind). Kinds: trees, buildings,
        people, plants, water, ground, roads, paths, fields, heritage, hubs, annotations, cuts, levels, labels, legend,
        keymap, frame, other. The booklet export turns the tags into nested groups (drawing > kind > element)."""
        B_ = self

        class _K(object):
            def __enter__(self_):
                self_.prev = (B_._kind, B_._eid)
                B_._kind, B_._eid = kind, (None if eid is None else u"%s" % eid)
                return B_

            def __exit__(self_, *a):
                B_._kind, B_._eid = self_.prev
                return False
        return _K()

    def _tag(self):
        if self._kind is None:
            return
        e_ = self._eid
        if e_ is None:
            n_ = self._eidn.get(self._kind, 0) + 1
            self._eidn[self._kind] = n_
            e_ = u"%04d" % n_
        self.tags[len(self.items) - 1] = u"%s/%s" % (self._kind, e_)

    def tgroup(self, start=True):
        """v59 (round 4, G-R4-1): start (or with False end) one text group: the lines / runs of one word block may
        touch each other in the page check (sb_text_check); two groups never touch. Returns the group id."""
        if start:
            self._tgn += 1
            self.tg = "t%d" % self._tgn
        else:
            self.tg = None
        return self.tg

    def begin(self, group, root):
        self.group, self.root = group, root

    def _lay(self, layer):
        return self.root + layer[len("LU_BOARD"):] if layer.startswith("LU_BOARD") else layer

    def fill(self, polys, color, layer, order):
        polys = [P for P in polys if P and len(P) >= 3]
        if polys:
            self.items.append(("fill", polys, color, self._lay(layer), order, self.group))
            self._tag()

    def line(self, P, color, layer, order, w=0.13):
        if P and len(P) >= 2:
            self.items.append(("line", P, color, self._lay(layer), order, w, self.group))
            self._tag()

    def hatch(self, polys, color, layer, order, spacing, ang=math.radians(45.0), w=0.03):
        """v16.5: parallel hatch lines over the area of polys (outer rings and holes, even-odd), spacing apart in page
        units at angle ang. Baked as a Rhino hatch (pattern "SELINUS lines"); as plain lines where that fails."""
        polys = [P for P in polys if P and len(P) >= 3]
        if polys and spacing > 0:
            self.items.append(("hatch", polys, color, self._lay(layer), order, spacing, ang, w, self.group))
            self._tag()

    def image(self, path, x0, y0, x1, y1, layer, order=5, alpha=None, flip=False):
        """T4 30 Oct (D1 a): a PNG (alpha kept) or JPEG over (x0, y0)-(x1, y1); alpha 0-1 = opacity, flip = mirrored.
        The PDF writer (_pdf_page) embeds each file once per board."""
        self.items.append(("image", path, (x0, y0, x1, y1), self._lay(layer), order, self.group, alpha, flip))
        self._tag()

    def text(self, txt, x, y, h, color, layer, order=40, font=None, bold=False, align="L", angle=0.0, italic=False,
             tg=None):
        """one text (h = capital height, board units). v59: item[13] = its text group (tg, else the open tgroup, else
        its own), read by the page check sb_text_check (every text of a booklet crop is measured there)."""
        if tg is None:
            tg = self.tg
            if tg is None:
                self._tgn += 1
                tg = "t%d" % self._tgn
        self.items.append(("text", txt, (x, y), h, color, self._lay(layer), order, font or FONT_BODY, bold, align,
                           angle, italic, self.group, tg))
        self._tag()

    def para(self, txt, x, y, width, h, color, layer, lead=1.8, font=None, order=40):
        """Wrapped paragraph (real widths, no widow); returns the y below it. v59: its lines are one text group."""
        k = kind_of(font or FONT_BODY)
        g_ = self.tg
        if g_ is None:
            self._tgn += 1
            g_ = "t%d" % self._tgn
        for ln in wrap(txt, width, h, k):
            self.text(ln, x, y, h, color, layer, order, font, tg=g_)
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


class SbX(object):
    """v61 (round 6): the board as the drawing object X the round 6 common modules draw through (annot.py an_cut /
    an_level / an_view / an_north, keymap.py km_draw_to): page-mm sizes in, board units out (k = board units per mm).
      X = SbX(B, layer, order, k, kind=None)
      X.fill(rings, hx, alpha=None, nz=False) · X.line(pts, hx, width_mm=0.13, dash_mm=None, alpha=None)
      X.text(s, xy, size_mm, hx, bold=False, align="L")    size_mm = font size (the Board takes the capital height)
      X.fill_fn / X.line_fn / X.text_fn                  the same, in basemap_draw's argument order
    kind: every item drawn through X is tagged with that G6-9 kind (each call its own element)."""

    def __init__(self, B, layer, order, k, kind=None):
        self.B, self.L, self.o, self.k, self.kd = B, layer, order, k, kind
        self.fill_fn = lambda rings, hx, a=None, nz=False: self.fill(rings, hx, a, nz)
        self.line_fn = lambda P, hx, w=0.13, dash=None, a=None: self.line(P, hx, w, dash, a)
        self.text_fn = lambda s_, p, size_mm, hx, bold=False, align="L": self.text(s_, p, size_mm, hx, bold, align)

    def cb(self):
        """S1's an_* / km_draw_to X = (fill_fn, line_fn, text_fn) in PAGE MM: these take mm points (board / k) and
        draw them on the board. Pair it with T_mm = lambda p: (Tb(p)[0] / k, Tb(p)[1] / k) and a frame in mm."""
        k_ = self.k

        def P(pts):
            return [(q[0] * k_, q[1] * k_) for q in pts]
        return (lambda rings, hx, a=None, nz=False: self.fill([P(R) for R in rings], hx, a, nz),
                lambda pts, hx, w=0.13, dash=None, a=None: self.line(P(pts), hx, w, dash, a),
                lambda s_, p, size_mm, hx, bold=False, align="L": self.text(s_, (p[0] * k_, p[1] * k_), size_mm, hx,
                                                                             bold, align))

    def _c(self, hx, a):
        c = C(hx) if hasattr(hx, "lstrip") else hx
        return c if a is None or a >= 0.999 else mix(c, WHITE, 1.0 - a)

    def _k(self):
        return self.B.kind(self.kd) if self.kd else _SbNoKind()

    def fill(self, rings, hx, alpha=None, nz=False):
        with self._k():
            self.B.fill(rings, self._c(hx, alpha), self.L, self.o)

    def line(self, pts, hx, width_mm=0.13, dash_mm=None, alpha=None):
        with self._k():
            if dash_mm:
                for d_ in r28_pattern(pts, [m * self.k for m in dash_mm]):
                    self.B.line(d_, self._c(hx, alpha), self.L, self.o, bk_lw(width_mm, self.k))
            else:
                self.B.line(pts, self._c(hx, alpha), self.L, self.o, bk_lw(width_mm, self.k))

    def text(self, s_, xy, size_mm, hx, bold=False, align="L"):
        with self._k():
            self.B.text(s_, xy[0], xy[1], size_mm * _PDF_CAP["sans"] * self.k, self._c(hx, None), self.L,
                        order=self.o + 1, font=FONT_TITLE, bold=bold, align=align)


class _SbNoKind(object):
    def __enter__(self):
        return None

    def __exit__(self, *a):
        return False


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
    elif kind == "study":                                # v50 (G8): the study area's dash-dot
        for d in r28_pattern(seg, [m * 0.22 * U for m in R28_STUDY_LINE["dash_mm"]]):      # one dash-dot in the sample
            B.line(d, col, L, 21, 0.45)
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


