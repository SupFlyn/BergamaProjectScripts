# booklet p18 (round 4, S6b): the section engine (cut specs, profiles, depth layers, planting groups) and the two
# p18 pages (p18_page, crops wb_plants_b1 / wb_plants_b2), split out of pages/p17_planting.py on 1 Nov 2026
# (Aras 13:42: "divide the scripts according to the job they do"); included right after it, so nothing moved in
# the built file. Helpers named _p17_* here and there are shared by both pages.

# ---------------------------------------------------------------- page B: the sections at 1:500
P17_WALL_T = 0.60                    # DSİ wall thickness drawn (no source; as p.04-05 and p.13 draw it)
P17_F1_RNG = (4.0, 69.0)             # W1: the part drawn, m from the SW end (the walk, the walls, the basins beyond)
P17_F1_BED = (22.1, 54.7)            # W1: the bed between the walls, m from the SW end (the survey's stream lines)
P17_F1_STRIP = (24.1, 28.9)          # W1: the zone base's strip; round 3 (DATA-1, ask 1 a) only its width is used: the
#                                      strip sits on the surveyed bed's low point (_p17_walled_bed)
P17_F2_RANGE = (36.0, 178.0)         # the part of F2 drawn, m along it
P17_F2_WALLS = (44.6, 67.7)          # F2: the bed between the DSİ walls (sample_cut.py: the survey's stream lines)
P17_F2_CELLS = [("reed", 77.9, 83.9), ("reed", 84.4, 90.4), ("mint", 90.9, 96.9)]   # basin cells in the zone WT
P17_F2_TERR = 7.0                    # rain terrace tread, m (the olive row spacing, plants.py PLA_CROPS)
P17_F4_RANGE = (3.0, 140.0)          # round 5 (S8, N3 a at 1:500): from 12 m back to 3 m (the survey runs 0-151 m) so
#                                      p19 can draw 137 m of F4 (CHK-9: 274 mm at 1:500); group 1 (shade) simply starts there
P17_F4_BED = (73.7, 113.9)           # F4: the bed between the survey's two stream lines, m along the cut
P17_F4_STRIP = (86.7, 90.9)          # the zone base's strip on F4 (ZONE_COPY A-NIL-STRIP-2)
P17_F3_RANGE = (-46.0, 52.0)         # S4: m across from the bed's low point (p.14's coordinates); round 5 (S8, N3 a at
#                                      1:500): the whole of p.14's built profile, street to street (= p14_15_s4.py
#                                      P14_RANGE; written out: that file may be included after this one)
P17_GRAVEL = 0.50
P17_ARM_D, P17_ARM_WL = 0.80, 0.30   # the side arm: channel depth and its water, m (drawing values)
P17_DECK_UP = 0.45                   # the F4 viewing deck over the bank top, m (drawing value: a seat height)
P17_RAMP = 12.0                      # ramp run per m rise (1:12, drawing rule)
P17_TERRACE_W = 4.0                  # the viewing terraces, m (drawing value)
P17_TOPO_D = (160.0, 60.0)           # background topography: survey contours on lines this far behind the cut, m
P17_STONE_UP = 0.15                  # stepping stones' tops over the average-flow water, m (= section_frame.py
#                                      sf_stepping_stones' own drawing rule, passed so the people stand on them)


def _p17_reg(cid):
    """the cut registry entry (M8) with the levels a section needs; a clear stop when one is missing"""
    r = level_registry(cid)
    for key in ("bed", "avg_flow", "q100", "q500"):
        if r.get(key) is None:
            raise RuntimeError(u"{}: '{}' is missing in the cut registry (common/data/LEVELS.py)".format(cid, key))
    return r


def _p17_wall(r):
    """the DSİ wall tops (SW, NE) of a walled cut from the registry"""
    sw, ne = r["walls"]["SW"][1], r["walls"]["NE"][1]
    if sw is None and ne is None:
        raise RuntimeError(u"{}: no wall top in the cut registry".format(r["id"]))
    return (sw if sw is not None else ne), (ne if ne is not None else sw)


def _p17_prof(gz, t0, t1, pieces, step=2.0):
    """the cut's ground [(t, z)] from t0 to t1: the survey (gz) every step m, replaced inside each piece (a, b, pts)
    by the piece's own points (a lane levelled, a channel dug)"""
    out = [(t0, gz(t0))]
    last = t0
    for a, b, pts in sorted(pieces, key=lambda q: q[0]) + [(t1, t1, [(t1, gz(t1))])]:
        s = math.floor(last / step) * step + step
        while s < a - 0.3:
            if s > last + 0.3:
                out.append((s, gz(s)))
            s += step
        out += [p for p in pts if p[0] >= last - 1e-9]
        last = max(last, b)
    return out


def _p17_flat(gz, a, b):
    """a levelled stretch a-b at the mean survey ground (2 decimals): its profile points"""
    n = max(1, int(b - a))
    z = round(sum(gz(a + (b - a) * i / float(n)) for i in range(n + 1)) / (n + 1), 2)
    return (a, b, [(a, gz(a)), (a, z), (b, z), (b, gz(b))]), z


def _p17_lane_txt(name, w_m):
    """a lane's name; round 5 (G-R5-4.6, P19.4): no width ("Bike · 300 cm" -> "Bike"); w_m kept for the callers"""
    return u"{}".format(name)


def _p17_gz(prof, t):
    """the ground of a profile [(t, z)] at t (at a vertical step the upper one)"""
    best = None
    for (a, za), (b, zb) in zip(prof[:-1], prof[1:]):
        if b > a and a - 1e-9 <= t <= b + 1e-9:
            z = za + (zb - za) * (t - a) / (b - a)
            best = z if best is None else max(best, z)
    if best is None:
        return prof[0][1] if t < prof[0][0] else prof[-1][1]
    return best


def _p17_seg_t(A, B, p, q):
    """where the segment p-q crosses A-B: the parameter 0-1 along A-B, or None"""
    d1 = (B[0] - A[0], B[1] - A[1])
    d2 = (q[0] - p[0], q[1] - p[1])
    den = d1[0] * d2[1] - d1[1] * d2[0]
    if abs(den) < 1e-12:
        return None
    w_ = (p[0] - A[0], p[1] - A[1])
    t = (w_[0] * d2[1] - w_[1] * d2[0]) / den
    s = (w_[0] * d1[1] - w_[1] * d1[0]) / den
    return t if 0.0 <= t <= 1.0 and 0.0 <= s <= 1.0 else None


def _p17_topo(cid, t0, t1, log):
    """the background topography of a cut (M8, R16 idea): the survey contours (basemap) met by lines parallel to the cut
    P17_TOPO_D m behind it (the way the section looks, M4 end markers), as ground lines [(t m along, m a.s.l.)], the
    farthest first, each with its distance: [(d, profile)]; [] without contours (one log line)"""
    if "cbb" not in _P17_MEMO:
        D = basemap_load(log=log)
        cs = ((D or {}).get("layers") or {}).get("contours") or []
        _P17_MEMO["cbb"] = [(min(p[0] for p in P), min(p[1] for p in P), max(p[0] for p in P), max(p[1] for p in P),
                             float(z), P) for _mj, z, P in cs if z is not None and len(P) >= 2]
        if not _P17_MEMO["cbb"]:
            log.append(u"p.17 sections: no survey contours in the basemap: drawn without background topography")
    a, b = level_ends(cid)
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
    f = (-u[1], u[0])
    out = []
    for d in P17_TOPO_D:
        A = (a[0] + u[0] * t0 + f[0] * d, a[1] + u[1] * t0 + f[1] * d)
        B = (a[0] + u[0] * t1 + f[0] * d, a[1] + u[1] * t1 + f[1] * d)
        bb = (min(A[0], B[0]), min(A[1], B[1]), max(A[0], B[0]), max(A[1], B[1]))
        pts = []
        for x0_, y0_, x1_, y1_, z, P in _P17_MEMO["cbb"]:
            if x1_ < bb[0] or x0_ > bb[2] or y1_ < bb[1] or y0_ > bb[3]:
                continue
            for p, q in zip(P[:-1], P[1:]):
                s = _p17_seg_t(A, B, p, q)
                if s is not None:
                    pts.append((t0 + s * (t1 - t0), z))
        pts.sort()
        if len(pts) >= 2:
            out.append((d, [(t0, pts[0][1])] + pts + [(t1, pts[-1][1])]))
    return out


def _p17_depth(spec, reg, X, P, gyx, zb, top, k, wl_y, style, log):
    """behind the cut (M8, D9; R16, R19 idea), the farthest layer first: its own ground from the survey contours
    (_p17_topo: layer 2 on the line P17_TOPO_D[0] m behind, layer 1 on P17_TOPO_D[1] m), the basemap houses of the
    band behind the cut (sf_back_buildings, SF_BACK_BAND: data height, else floors x BLD_STOREY; those nearer than the
    band's middle on layer 1, the rest on layer 2) standing on that layer's ground (sf_back_house: real profiles, faded
    by layer, G14 seated; a house whose roof would leave the drawing is left out), then mixed tree
    groups on it (pla_group_section: wet species toward the stream, dry ones outward, none on water, none in a house).
    Layer by layer, so a nearer ground hides what stands behind it. Without contours the trees stand on the cut ground
    (one log line). Returns shapes (page mm of the section)."""
    t0, t1 = spec["rng"]
    W = X(t1)
    xb = X(min(spec["prof"], key=lambda p: p[1])[0])           # the bed's low point
    half = max(xb, W - xb) or 1.0

    def tfun(x):                                               # band 0.25 at the stream to 0.85 at the ends
        return 0.25 + 0.60 * min(1.0, abs(x - xb) / half)
    prs = dict(_p17_topo(reg["id"], t0, t1, log)) if spec.get("topo", True) else {}
    blds = sf_back_buildings(reg["id"], t0, t1, log=log)      # farthest first: [(t_a, t_b, h m, floors, d m behind)]
    dmid = 0.5 * (SF_BACK_BAND[0] + SF_BACK_BAND[1])
    sh, nh = [], 0
    for layer, d in zip((2, 1), P17_TOPO_D):
        g_, hs = gyx, []
        pr = prs.get(d)
        if pr:
            pts = P([(t, min(z, zb + top / k)) for t, z in pr])
            sh += sf_topo_back([pts], 0.0).shapes()
            g_ = sf_gy(pts)
        for ta, tb, h, fl, db in blds:                         # this layer's houses, before its trees
            if (1 if db < dmid else 2) != layer or tb - ta < 3.0:   # a sliver under one bay (sf_back_house's 3.0 m)
                continue
            hh = sf_back_house(X(ta), X(tb), g_, h, k, layer=layer, floors=fl, d_m=db)   # v2: no windows past 30 m
            if not hh or _p17_shp_bb(hh)[3] > top:             # the roof would leave the drawing
                continue
            sh += hh
            hs.append((X(ta), X(tb)))
            nh += 1
        tr, _pl, _gr = pla_group_section(0.0, W, g_, k, t0=tfun, mix=["plane", "ash", "willow", "tamarisk", "olive"],
                                         seed=spec.get("seed", 3) * 7 + layer, layers=(layer,), style=style,
                                         density=0.6, avoid=hs, hires=False, detail=False, water=wl_y)
        sh += tr
    spec["n_houses"] = nh
    return sh


def _p17_group_sec(g, X, gyx, k, wl_y, avoid, style, use=(), lead=False):
    """one planting group of a cut (G9): plants.py pla_group_section over the group's stretch, its band g["t"] from
    one end to the other, mixed species with overlapping crowns, a mid layer (D9 1) behind the cut plane (0), only
    emergent species where the ground lies under the average-flow water. The helper starts its first group up to
    half its widest gap in (PLA_GROUP gap_m): the run starts that far before the stretch and that lead-in is kept
    free, so a narrow stretch still gets its group. Round 3 (G15, K2): where the group reaches a use zone (use, page
    mm, +-2 m) the trees step back: the cut plane keeps the low planting only, the trees stand in layer 1 behind the
    people, paler by the module's layer tone. Returns (back shapes, front shapes, placed [(key, x mm, h, crown,
    layer)]). Round 5 (G-R5-4.5, S3 sf_tree_level): lead=True (the plant pages p18-p20) = the trees lead, they do not
    step back from the use zones."""
    x0, x1 = X(g["a"]), X(g["b"])
    lead = 0.5 * PLA_GROUP["gap_m"][1] * k
    ta, tb = g["t"]
    near = (not lead) and any(ua - 2.0 * k < x1 and ub + 2.0 * k > x0 for ua, ub in use)

    def tf(x):
        return ta + (tb - ta) * min(1.0, max(0.0, (x - x0) / max(1e-9, x1 - x0)))
    out = []
    for layer in (1, 0):
        mix = list(g["mix"])
        if layer == 0 and near:
            mix = [k_ for k_ in mix if not _pla_canopy(k_)]
        if not mix:
            out.append(([], []))
            continue
        sh_, pl_, _gr = pla_group_section(x0 - lead, x1, gyx, k, t0=tf, mix=mix, seed=g["seed"] * 3 + layer,
                                          layers=(layer,), style=style, density=g.get("dens", 1.0),
                                          avoid=list(avoid) + [(x0 - lead - 1.0, x0)], water=wl_y)
        out.append((sh_, pl_))
    return out[0][0], out[1][0], out[0][1] + out[1][1]


def _p17_tone(shapes, f):
    """shapes toned toward the paper by f (0..1): the depth tone of what lies beyond the cut, opaque (G9: no alpha)"""
    out = []
    for s_ in shapes:
        if s_[0] == "poly":
            out.append((s_[0], s_[1], _sec_mix(s_[2], SEC["paper"], f) if s_[2] else s_[2],
                        _sec_mix(s_[3], SEC["paper"], f) if s_[3] else s_[3], s_[4] if len(s_) > 4 else 0.1))
        elif s_[0] == "line" and s_[2]:
            out.append((s_[0], s_[1], _sec_mix(s_[2], SEC["paper"], f)) + tuple(s_[3:]))
        else:
            out.append(s_)
    return out


def _p17_section(spec, style, log, den=None, page=u"p19", inset=False):
    """round 4 (P18.1-P18.6, booklet p18a / p18b), round 5 (S8: p19-20 at 1:500, N3 a): one cut at 1:den (P18_DEN)
    on its own Page, the DRAWING only (its words are booklet items, exported by p18_page). Origin: x 0
    = the start of the drawn part, y 0 = 1 m under its lowest ground; the drawing is cut to (0, 0, W, top). Layers in
    M5's order: the sky v2 (sf_atmosphere, its own variant by cut id) and behind the cut, layer by layer, the survey
    ground, the houses v2 on it (d_m: no windows beyond 30 m) and tree groups (_p17_depth, paler with distance); the
    cut ground with the module's soil gradient, the bed from the surveyed profile, the water at the average yearly
    flow, the Q100 / Q500 lines (water_section, no labels); structures (lanes, terraces, ramp, bridge, stepping stones,
    sitting steps' blocks, benches, lamps, basins, today's wall dashed, railings); the planting groups (G9 mixed,
    trees stepping back where people are) and the shrub and flower layer (plants.py pla_low_section, G-R4-5.2); the
    people of each zone in front (figures.py, the one pen_black set, G-R4-5.1; nobody in water deeper than wading);
    break marks where the drawn part ends inside the cut (N3 a). No arrows, no triangles, no text.
    spec gets: "dbox" (0, 0, W, top), "geo" (k, W, top, X, Y, gyx), "marks" [(kind, name, why, x, y, colour)] the
    places to number (use zones on their ground, planting groups in their crown), "level_rows" [(key, m, y)], and
    "placed" [(pose, m along, half footprint m)] the people of the cut plane. Returns the Page.
    Round 5 (S8, G-R5-5 / G-R5-4): no zoom inset is drawn here any more: p18_page draws an inset as its own drawing,
    calling this again at the inset's own scale (inset=True: 1:100 is allowed, sf_inset_k), the same spec, so the
    same people and plants stand at the same metres; trees lead on the plant pages (sf_tree_level, layer 0, no step
    back); the bridges the cut sees (S3 br_section, look +1); fishing and wading only where sf_activity_ok allows
    (spec "month", "strip_water"). page = the booklet page id ("p19", "p20"; " inset" after it for an inset)."""
    den = float(den or P18_DEN)
    k = sf_inset_k(den) if inset else sf_k(den)
    pid = (u"%s" % page).split()[0] if page else u""
    lead = sf_tree_level(pid)["lead"]
    t0, t1 = spec["rng"]
    prof = spec["prof"]
    reg = _p17_reg(spec["cid"])
    name = level_name(spec["cid"])
    zb = min(z for _t, z in prof) - 1.0
    Y = sf_y_of(zb, 0.0, k)

    def X(t):
        return (t - t0) * k

    def gz(t):
        return _p17_gz(prof, t)

    def gyx(x):
        return Y(gz(x / k + t0))

    def P(pts):
        return [(X(t), Y(z)) for t, z in pts]
    W = X(t1)
    wl_y = Y(reg["avg_flow"])
    stone_y = wl_y + P17_STONE_UP * k
    wl = water_layers()
    # G15 soil: the module's gradient under the cut ground; water_section's flat earth fill is cleared (its hatch and
    # the stone / gravel fills stay)
    surf = P(prof)
    wl.add("ground", sct_soil_gradient(surf, min(p[1] for p in surf) - 1.0 * k, k))
    water_section(surf, k, Y, cid=reg["id"], banks=spec.get("banks", ("earth", "earth")), labels=False, style=style,
                  into=wl)
    wl.L["ground"] = [s_ for s_ in wl.L["ground"] if not (s_[0] == "poly" and s_[2] == SCT["earth"])]
    for ring, mat in spec.get("fills", []):
        wl.add("bed", sct_hatch_fill(P(ring), mat, k, None, 0.1))
    for ring in spec.get("water", []):
        wl.add("water", _wat_sec_body(P(ring), 0.6))
    for kind, a, b, fl, rim in spec.get("cells", []):
        fn = pla_reed_basin if kind == "reed" else pla_mint_cell
        wl.add("structures", fn(X(a), X(b), Y(fl), Y(rim), k, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"],
                                P17_BASIN["media"]))
    for st in spec.get("structures", []):
        kind = st[0]
        if kind == "lane":
            _, a, b, lk = st
            wl.add("structures", sf_lane(X(a), Y(gz((a + b) / 2.0)), b - a, k, kind=lk))
        elif kind == "terrace":                          # rail at the end named ("a" / "b"); z: a raised deck
            _, a, b, rail_at, z = st
            zz = z if z is not None else gz((a + b) / 2.0)
            wl.add("structures", sf_terrace(X(b) if rail_at == "a" else X(a), Y(zz), b - a, k,
                                            side=-1 if rail_at == "a" else 1))
            if z is not None:
                for t_ in (a + 0.15, b - 0.15):
                    wl.add("structures", [("line", [(X(t_), Y(gz(t_))), (X(t_), Y(zz) - 0.25 * k)], SCT["cut"], 0.25)])
        elif kind == "ramp":
            _, a, b, z0, z1 = st
            wl.add("structures", sf_ramp(X(a), Y(z0), b - a, z1 - z0, k)[0])
        elif kind == "bridge":
            _, a, b, z = st
            wl.add("structures", sf_bridge(X(a), X(b), Y(z), k))
        elif kind == "bench":
            _, t_, side = st
            wl.add("structures", sf_bench(X(t_), sf_seat_x(gyx, X(t_), 0.25 * k), k, side=side, back=True))
        elif kind == "lamp":                             # street elements (G15), sizes are drawing rules
            _, t_, side = st
            wl.add("structures", sf_lamp(X(t_), gyx(X(t_)), k, side=side))
        elif kind == "bollard":
            wl.add("structures", sf_bollard(X(st[1]), gyx(X(st[1])), k))
        elif kind == "stones":                           # across the summer strip, on its floor, above the water
            _, a, b = st
            wl.add("structures", sf_stepping_stones(X(a), X(b), sf_ground_min(gyx, X(a), X(b)), wl_y, k,
                                                    above_m=P17_STONE_UP, seed=spec.get("seed", 3)))
        elif kind == "ghost":                            # round 4: today's wall where the design cuts it back, dashed
            _, a, b, z0, z1 = st
            r_ = P([(a, z0), (b, z0), (b, z1), (a, z1), (a, z0)])
            wl.add("structures", [("line", r_, COL["ink2"], 0.18, [0.8, 0.5])])
        elif kind == "rail":                             # round 4: a railing at a floor's edge (SF_RAIL_H)
            _, t_, z = st
            wl.add("structures", [("line", [(X(t_), Y(z)), (X(t_), Y(z + SF_RAIL_H))], SCT["cut"], 0.2),
                                  ("line", [(X(t_) - 0.15 * k, Y(z + SF_RAIL_H)), (X(t_) + 0.15 * k, Y(z + SF_RAIL_H))],
                                   SCT["cut"], 0.2)])
    # the planting groups (G9): mixed groups in two depth layers; the trees step back where people are (G15)
    av = [(X(a), X(b)) for a, b in spec.get("avoid", [])]
    use = [(X(z_[1]), X(z_[2])) for z_ in spec.get("people", [])]
    back, front, trees, grp = [], [], [], []
    for g in spec.get("groups", []):
        if g.get("fixed"):
            pl_ = [(key, X(s), h, w, 0) for key, s, h, w in spec.get("fixed", []) if g["a"] <= s <= g["b"]]
        else:
            b_, f_, pl_ = _p17_group_sec(g, X, gyx, k, wl_y, av, style, use, lead=lead)
            back += b_
            front += f_
        keys = sorted(set(p[0] for p in pl_), key=lambda k_: -PLA_SPECIES[k_]["h_m"])
        tags = [t for t in g.get("why", ()) if t in P17_WHY_PLACE or any(t in pla_purpose(k_) for k_ in keys)]
        trees += [p for p in pl_ if p[4] == 0]
        if keys:
            grp.append((g, keys, tags, pl_))
    fx = [(key, X(s), h, w, 0) for key, s, h, w in spec.get("fixed", []) if t0 + 0.2 <= s <= t1 - 0.2]
    for i, (key, x, h, w, _l) in enumerate(sorted(fx, key=lambda q: -q[2])):   # S4: p.14's own plants, seated
        ly_ = 1 if (not lead) and _pla_canopy(key) and any(ua - 2.0 * k < x < ub + 2.0 * k for ua, ub in use) else 0
        (back if ly_ else front).extend(pla_section(key, x, sf_seat_x(gyx, x, 0.12 * w * k), k, h_m=h, crown_m=w,
                                                    seed=i + 7, style=style, layer=ly_))
    trees += [p for p in fx if p not in trees]
    # round 4 (G-R4-5.2, D7, P18.6): the shrub and flower layer on the soft banks, landings and verges (plants.py's
    # sourced low species by wetness band; spec "low" [(m from, m to, band t from, t to, seed[, species, density])])
    n_low = 0
    for lo in spec.get("low", []):
        a, b = max(lo[0], t0 + 0.2), min(lo[1], t1 - 0.2)
        if b - a < 0.5:
            continue
        sh_, pl_ = pla_low_section(X(a), X(b), gyx, k, lo[2], lo[3], seed=lo[4], density=lo[6] if len(lo) > 6 else 1.2,
                                   avoid=av, water=wl_y, mix=lo[5] if len(lo) > 5 else None)
        front += sh_
        n_low += len(pl_)
    wl.add("vegetation", back + front)
    bad = sf_assert_g6(k, trees=[(p[0], p[1], p[2], p[3]) for p in trees], strict=False)
    if bad:
        log.append(u"WARNING (G6) {} {}: {}".format(page, name, u"; ".join(bad[:3])))
        wn_orange(log[-1][8:])  # v15.1 (closing): this WARNING line also orange (one sink)
    # people doing what each zone is for (G10, G15), in front of the planting: who stays looks at the zone's focus
    fx0 = X(spec["focus"]) if spec.get("focus") is not None else X(min(prof, key=lambda q: q[1])[0])
    # round 5 (S3 sf_activity_ok, PLAN §8): wading and fishing only where the drawn water allows it (depth <= 0.50 m,
    # the season the cut shows: spec "month" None = general, no season; "strip_water" = the summer strip's water is
    # drawn); a refused zone gets nobody (WARNING from the kit). Decided once per spec, so an inset agrees.
    acts = spec.setdefault("_act", {})
    figs, placed = [], []
    fp = dict((a_[0], a_[2]) for v_ in FIG_ACTIVITY.values() for a_ in v_)   # pose -> footprint m (figures.py)
    for j, (zone, a, b, o) in enumerate(spec.get("people", [])):
        o = o or {}
        if zone in ("wading_strip", "water_edge"):
            if j not in acts:
                kd_ = "wade" if zone == "wading_strip" else "fish"
                gmin = min(gyx(X(a + (b - a) * i_ / 10.0)) for i_ in range(11))
                wy_ = wl_y if (kd_ == "fish" or wl_y > gmin + 1e-6) else None
                ok_, why_ = sf_activity_ok(kd_, ground_y=gmin if kd_ == "wade" else None, water_y=wy_, k=k,
                                           month=spec.get("month"), strip=bool(spec.get("strip_water")), page=pid,
                                           what=u"{} {} {:.1f}-{:.1f} m".format(spec["cid"], zone, a, b))
                acts[j] = ok_
                if not ok_:
                    log.append(u"NOTE {} {}: {} {:.1f}-{:.1f} m left empty ({})".format(pid, spec["cid"], zone, a, b,
                                                                                         why_))
            if not acts[j]:
                continue
        gr = stone_y if zone == "stepping_stones" else (Y(o["z"]) if o.get("z") is not None else None)
        sh_, pl_ = fig_place_zones([(zone, X(a), X(b), gr)], gyx, k, seed=31 * j + 5 + 7 * spec.get("seed", 3),
                                   layer=0, style=style, density=o.get("dens", 1.0), water=wl_y,
                                   max_per_zone=o.get("n"), focus=X(o["focus"]) if o.get("focus") is not None else fx0,
                                   **(o.get("p") or {}))
        figs += sh_
        placed += [(q_[1], q_[2] / k + t0, 0.5 * fp.get(q_[1], 0.8)) for q_ in pl_ or () if len(q_) >= 3]
    spec["placed"] = placed
    wl.add("figures", figs)
    # D8 (S3 §2 step 3, §4): the bridges this cut sees, looking +1 (p19-20's rule): beyond the plane in elevation in the
    # background, cut through in the structures; the bed under them = the cut's LEVELS bed (bridges.py FLAG), no
    # height source = the deck at the cut's bank top. One `bridge <cut> ...` line either way.
    try:
        if spec["cid"] == "S4":                         # S4's t is p.14's m from the bed's low point, not the m along
            br_ = br_section("S4", look=1, page=page)   # the cut bridges.py counts: looked up on the whole line only
            if br_.get("found"):                        # (S3 §4: none within 500 m), never drawn at a wrong place
                log.append(u"FLAG {} S4: a bridge was found ({}); not drawn: S4's coordinates are p.14's, not "
                           u"chainage".format(pid, u", ".join(f_["name"] for f_ in br_["found"])))
        else:
            br_ = br_section(spec["cid"], X=X, Y=Y, look=1, t0=t0, t1=t1, page=page, into=wl)
        spec["bridges"] = [] if spec["cid"] == "S4" else \
            [(f_["name"], f_["rel"], round(f_["t"], 1)) for f_ in br_.get("found", [])]
    except Exception as ex:
        BR_LOG.append(u"bridge {} not drawn ({}: {}) ({})".format(spec["cid"], type(ex).__name__, ex, page))
        spec["bridges"] = []
    if not inset and BR_LOG and BR_LOG[-1] not in log:
        log.append(BR_LOG[-1])
    top = _p17_shp_bb(_p17_clip(wl.shapes(), (0.0, -1e4, W, 1e4)))[3] + 1.5
    # behind the cut (D9): the sky (its own variant, birds), the depth layers, people further along, basins beyond
    clipr = (0.0, 0.0, W, top)
    atm = water_layers()
    sf_atmosphere(0.0, W, gyx, top, k, seed=spec.get("seed", 3), sky="d8", trees=False, into=atm, cid=reg["id"])
    wl.add("atmosphere", _p17_clip(atm.L["atmosphere"], clipr))
    wl.add("background", _p17_clip(_p17_depth(spec, reg, X, P, gyx, zb, top, k, wl_y, style, log), clipr))
    bp = []
    for kind, a, b, fl, rim in spec.get("beyond", []):   # beyond the cut: the layer-1 tone (no alpha veil, G9)
        fn = pla_reed_basin if kind == "reed" else pla_mint_cell
        bp += fn(X(a), X(b), Y(fl), Y(rim), k, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"], P17_BASIN["media"])
    if bp:
        wl.add("background", _p17_tone(bp, 0.5))
    for j, (zone, a, b) in enumerate(spec.get("back", [])):
        sh_, _pl = fig_place_zones([(zone, X(a), X(b))], gyx, k, seed=77 + j + spec.get("seed", 3), layer=1,
                                   style=style, density=0.6, water=wl_y, max_per_zone=2, focus=fx0)
        wl.add("background", sh_)
    pg = Page(0, 0)
    _p17_put(pg, _p17_clip(wl.shapes(), clipr))
    # N3 a: a break mark where the drawn part ends inside the cut (the land goes on; the key map shows the whole line)
    for side in spec.get("breaks", ()):
        xb, sg = (0.0, 1.0) if side == "L" else (W, -1.0)
        yt = min(gyx(min(max(xb, 0.01), W - 0.01)) + 0.8 * k, top)
        pg.line([(xb, 0.0), (xb, 0.38 * yt), (xb + sg * 1.4, 0.46 * yt), (xb, 0.54 * yt), (xb, yt)], COL["ink"], 0.25)
    spec["dbox"] = (0.0, 0.0, W, top)
    spec["geo"] = dict(k=k, W=W, top=top, X=X, Y=Y, gyx=gyx, t0=t0, t1=t1, zb=zb)   # y 0 = zb m a.s.l. (origin)
    # the places to number (G-R4-5.5): each use zone on its own ground at its middle (on the stones: their tops),
    # each planting group in the crown of its tallest plant at the cut plane; colour = what the number names (G-R4-7)
    marks = []
    for z_ in spec.get("zones", []):
        a, b = max(z_[0], t0), min(z_[1], t1)
        if b - a < 0.8:
            continue
        xm = X((a + b) / 2.0)
        nm = z_[2]
        ym = stone_y if nm in (u"STONES",) else gyx(xm)
        marks.append(("zone", _p18_zname(nm), z_[3] if len(z_) > 3 else u"", xm, ym,
                      P18_MK_WATER if nm in P18_WATER_ZONES else P18_MK_ZONE))
    for g, keys, tags, pl_ in grp:
        pp = [p for p in pl_ if p[4] == 0 and 0.0 < p[1] < W] or [p for p in pl_ if 0.0 < p[1] < W]
        if not pp:
            continue
        p = max(pp, key=lambda q: q[2])
        nm = u" + ".join(P17_SHORT.get(k_, PLA_SPECIES[k_]["name"].lower()) for k_ in keys[:3])
        why = u", ".join(P17_WHY[t] for t in tags[:2])
        marks.append(("group", nm[:1].upper() + nm[1:], why, p[1], gyx(p[1]) + 0.65 * p[2] * k,
                      pla_colour(keys[0])["fill"]))
    spec["marks"] = marks
    rows = [("q500", reg["q500"]), ("q100", reg["q100"]), ("avg", reg["avg_flow"]), ("bed", reg["bed"])]
    rows += [(t, z) for z, t in spec.get("levels", [])]
    spec["level_rows"] = [(key, z, Y(z)) for key, z in rows]
    log.append(u"{} {}: 1:{:,.0f}, {:.1f}-{:.1f} m drawn ({:.0f} x {:.0f} mm), {} planting groups, {} low plants, {} "
               u"background houses, levels bed {} / avg flow {} / Q100 {} / Q500 {} (registry), trees {}".format(
                   page, name, den, t0, t1, W, top, len(spec.get("groups", [])), n_low, spec.get("n_houses", 0),
                   u_level(reg["bed"]), u_level(reg["avg_flow"]), u_level(reg["q100"]), u_level(reg["q500"]),
                   u"lead (layer 0)" if lead else u"layer 1 near people"))
    return pg


def _p17_walled_bed(gz, ws, wn, width, log, cid):
    """DATA-1 (Aras 31 Oct, ask 1 a): the bed between a walled cut's DSİ walls from the survey ground gz (not flat),
    the summer strip (the low-flow channel, its zone-base width) moved onto the survey's lowest point, where the low
    water runs, cut STRIP_DEPTH under that point. Returns (profile points ws..wn, (st0, st1), strip floor, fills: the
    gravel bed following the floor, the strip's concrete liner)."""
    ts = [ws + 0.25 * i for i in range(int((wn - ws) / 0.25) + 1)]
    tlow = min(ts, key=gz)
    st0 = min(max(tlow - width / 2.0, ws + 0.3), wn - 0.3 - width)
    st1 = st0 + width
    fl = round(min(gz(st0 + (st1 - st0) * i / 8.0) for i in range(9)) - STRIP_DEPTH, 2)
    pts = [(ws, gz(ws))]
    t = math.floor(ws) + 1.0
    while t < st0 - 0.3:
        pts.append((t, gz(t)))
        t += 1.0
    pts += [(st0, gz(st0)), (st0, fl), (st1, fl), (st1, gz(st1))]
    t = math.ceil(st1 + 0.3)
    while t < wn - 0.3:
        pts.append((t, gz(t)))
        t += 1.0
    pts.append((wn, gz(wn)))
    lt = 0.15
    fills = [(pts + [(p[0], p[1] - P17_GRAVEL) for p in reversed(pts)], "gravel"),
             ([(st0 - lt, gz(st0)), (st0 - lt, fl - lt), (st1 + lt, fl - lt), (st1 + lt, gz(st1)), (st1, gz(st1)),
               (st1, fl), (st0, fl), (st0, gz(st0))], "concrete")]
    log.append(u"p.17 {}: bed between the DSİ walls from the survey profile; summer strip moved onto the "
               u"survey's low point at {:.1f}-{:.1f} m (DATA-1, Aras ask 1 a), floor {}".format(
                   cid, st0, st1, u_level(fl)))
    return pts, (st0, st1), fl, fills


def _p17_f2(log):
    """F2 across the stream at the upstream entry (cut registry F2), scenario "step across, clean, look out": the
    walk on the SW wall top, stepping stones across the summer strip (nobody in the walled channel's water), the
    spillway, the lined reed basins, the dry bank, the shaded walk with its bike lane and bench, the rain terraces and
    the viewing terrace on the top one. Round 3 (DATA-1): the bed between the walls from the survey, the strip on its
    low point."""
    r = _p17_reg("F2")
    bed = r["bed"]
    wsw, wne = _p17_wall(r)
    g = _p17_ground("F2")

    def gz(t):
        return _p17_interp(g, t)
    t0, t1 = P17_F2_RANGE
    ws, wn = P17_F2_WALLS
    wtk = P17_WALL_T
    wk, bk = P14_PROM_W
    zone = dict((c_, (a_, b_)) for c_, a_, b_ in level_cut("F2").get("zones") or [])
    for c_ in ("STRIP", "WD", "WT", "GR", "WS"):
        if c_ not in zone:
            raise RuntimeError(u"F2: zone {} is missing in the cut registry (common/data/LEVELS.py)".format(c_))
    floor_pts, (st0, st1), sfl, bed_fills = _p17_walled_bed(gz, ws, wn, zone["STRIP"][1] - zone["STRIP"][0], log,
                                                            u"F2")
    sp0, sp1 = wn + wtk, zone["WD"][1]
    bt0, bt1 = zone["WT"]
    gr0, gr1 = zone["GR"]
    te0, te1 = zone["WS"]
    zp = round(max(gz(bt0 + i) for i in range(int(bt1 - bt0) + 1)), 2)     # the basin platform: the ground's top there
    floor = zp - P17_BASIN["depth"]
    prof = []
    # south-west: the ground held up to the wall top behind the DSİ wall, the survey further out
    t, side = ws - wtk, []
    while t >= t0 - 1e-9:
        side.append((t, wsw if gz(t) < wsw and all(p[1] == wsw for p in side) else gz(t)))
        t -= 2.0
    if side[-1][0] > t0:
        side.append((t0, wsw if gz(t0) < wsw and all(p[1] == wsw for p in side) else gz(t0)))
    prof += side[::-1]
    prof += [(ws - wtk, wsw), (ws, wsw)] + floor_pts + [(wn, wne), (sp0, wne)]
    # the spillway trough from the basins down to the wall top, then the basin platform and the cells
    prof += [(sp0 + 0.3, wne), (sp0 + 0.3, wne - 0.45), (sp1 - 0.3, wne - 0.30), (sp1 - 0.3, wne), (sp1, wne),
             (bt0 - 0.3, zp), (bt0, zp)]
    cells = []
    for kind, a, b in P17_F2_CELLS:
        prof += [(a, zp), (a, floor + P17_BASIN["media"]), (b, floor + P17_BASIN["media"]), (b, zp)]
        cells.append((kind, a, b, floor, zp))
    prof += [(bt1, zp)]
    t = math.ceil(bt1 + 1.0)
    while t < gr0 - 0.3:
        prof.append((t, gz(t)))
        t += 2.0
    pc, zg = _p17_flat(gz, gr0, gr1)                    # the shaded walk, levelled
    prof += pc[2][:3]
    # the rain terraces: level treads P17_F2_TERR wide at the mean ground of each, stone retaining walls
    fills, treads = [], []
    prev, s = zg, te0
    while s + P17_F2_TERR <= te1 + 0.1:
        lv = round(sum(gz(s + j * 0.5) for j in range(int(P17_F2_TERR * 2) + 1)) / (int(P17_F2_TERR * 2) + 1), 2)
        prof += [(s, lv), (s + P17_F2_TERR, lv)]
        fills.append(([(s - 0.4, min(prev, lv) - 0.4), (s, min(prev, lv) - 0.4), (s, max(prev, lv)),
                       (s - 0.4, max(prev, lv))], "stone"))
        treads.append((s, s + P17_F2_TERR, lv))
        prev, s = lv, s + P17_F2_TERR
    prof.append((min(t1, s + 0.6), gz(min(t1, s + 0.6))))
    if prof[-1][0] < t1:
        prof.append((t1, gz(t1)))
    fills = bed_fills + fills
    fills += [([(ws - wtk, wsw), (ws, wsw), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
              ([(wn, wne), (wn + wtk, wne), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone"),
              ([(sp0, wne), (sp0 + 0.3, wne), (sp0 + 0.3, wne - 0.45), (sp1 - 0.3, wne - 0.30), (sp1 - 0.3, wne),
                (sp1, wne), (sp1, wne - 0.5), (sp0, wne - 0.65)], "concrete")]
    water = [[(sp0 + 0.3, wne - 0.45), (sp1 - 0.3, wne - 0.30), (sp1 - 0.3, wne - 0.15), (sp0 + 0.3, wne - 0.25)]]
    wa = (ws - wtk - wk, ws - wtk)                      # the walk on the wall top
    bl = (gr0 + 2.5, gr0 + 2.5 + bk)                    # the shaded walk: bike lane, then the walk
    wl_ = (bl[1] + 2.0, bl[1] + 2.0 + wk)
    ta = treads[-1][0] if treads else te1 - P17_TERRACE_W
    vt = (ta, ta + P17_TERRACE_W)                       # the viewing terrace on the top tread, its rail to the stream
    rush = ("soft_rush", "loosestrife")
    groups = [dict(a=ws + 0.2, b=st0 - 0.3, t=(0.02, 0.06), mix=rush, dens=1.2, why=("cleaning",), seed=21),
              dict(a=st1 + 0.3, b=wn - 0.2, t=(0.06, 0.02), mix=rush, dens=1.2, why=("cleaning",), seed=22),
              dict(a=sp0 + 0.5, b=sp1 - 0.5, t=(0.04, 0.08), mix=rush, dens=0.8, why=("cleaning",), seed=23),
              dict(a=bt1 + 0.5, b=gr0 - 0.3, t=(0.55, 0.85), mix=("chaste", "tamarisk", "olive", "rosemary", "lavender"),
                   why=("perception", "corridor"), seed=24),
              dict(a=gr0 + 0.3, b=gr1 - 0.3, t=(0.48, 0.55), mix=("plane", "ash", "chaste"), why=("shade", "corridor"),
                   seed=25),
              dict(a=te0 + 0.5, b=vt[0] - 0.3, t=(0.78, 0.95), mix=("olive", "rosemary", "lavender"),
                   why=("shade", "perception"), seed=26)]
    groups = [g_ for g_ in groups if g_["b"] - g_["a"] > 0.5]
    bn = bl[1] + 0.7                                    # a bench between the bike lane and the walk
    lp_ = wl_[1] + 0.4                                  # a lamp on the walk's far edge (G15 street element)
    return dict(cid="F2", seed=2, rng=(t0, t1), prof=prof, fills=fills, water=water, cells=cells, groups=groups,
                focus=(st0 + st1) / 2.0,
                avoid=[wa, bl, wl_, vt, (bn - 0.3, bn + 0.8), (lp_ - 0.3, lp_ + 0.3)],
                structures=[("lane", wa[0], wa[1], "walk"), ("lane", bl[0], bl[1], "bike"),
                            ("lane", wl_[0], wl_[1], "walk"), ("terrace", vt[0], vt[1], "a", None),
                            ("stones", st0, st1), ("bench", bn, 1), ("lamp", lp_, -1)],
                people=[("walkway", wa[0], wa[1], None), ("stepping_stones", st0, st1, {"n": 2}),
                        ("bike_lane", bl[0], bl[1], {"n": 1}), ("walkway", wl_[0], wl_[1], None),
                        ("viewing_terrace", vt[0], vt[1], {"n": 3})],   # v10: nobody in the walled channel's water (Aras 11:28)
                back=[("walkway", wa[0], wa[1]), ("walkway", wl_[0], wl_[1])],
                arrows=[([(sp0 + 0.2, wne - 0.2), (sp0 - 0.8, wne - 1.6), (sp0 - 1.2, bed + 0.4)], C["w3"])],
                zones=[(wa[0], wa[1], _p17_lane_txt(u"PATH", wk), u"wall top, above the bed"),
                       (st0, st1, u"STONES", u"cross the summer strip dry-shod"),
                       (sp0, sp1, u"SPILLWAY", u"basin overflow back to the stream"),
                       (bt0, bt1, u"REED BASINS", u"clean run-off before the stream"),
                       (bt1, gr0, u"DRY BANK", u"shrubs hold the slope"),
                       (bl[0], bl[1], _p17_lane_txt(u"BIKE", bk), u"through route, apart from walkers"),
                       (wl_[0], wl_[1], _p17_lane_txt(u"PATH", wk), u"under the trees, out of the sun"),
                       (te0, vt[0], u"RAIN TERRACES", u"level treads hold the rain"),
                       (vt[0], vt[1], u"VIEW TERRACE", u"over the basins to the stream")],
                inset=(st0 - 1.5, st1 + 1.5, u"stepping stones over the summer strip"),
                levels=[(wne, u"DSİ wall")],
                caption=u"F2 · the upstream entry: rain terraces, reed basins and the walled stream")


def _p17_f4(log):
    """F4 across the lower reach (cut registry F4), scenario "play in the water": the path and its bridge over the
    side arm, the bank top, the viewing deck with its ramp, the widened bed with its strip (stones, wading), fishing
    and watching at the water's edge, the north bank, the street-side bike lane and walk with a lamp"""
    r = _p17_reg("F4")
    g = _p17_ground("F4")

    def gz(t):
        return _p17_interp(g, t)
    t0, t1 = P17_F4_RANGE
    zone = dict((c_, (a_, b_)) for c_, a_, b_ in level_cut("F4").get("zones") or [])
    if "ARM" not in zone:
        raise RuntimeError(u"F4: zone ARM is missing in the cut registry (common/data/LEVELS.py)")
    a0, a1 = zone["ARM"]
    b0, b1 = P17_F4_BED
    st0, st1 = P17_F4_STRIP
    wk, bk = P14_PROM_W
    zf = gz((a0 + a1) / 2.0) - P17_ARM_D               # the side arm's floor
    zs = gz((st0 + st1) / 2.0)
    pw = (a0 - 1.0 - wk, a0 - 1.0)                      # the path to the bridge
    br = (a0 - 1.0, a1 + 1.0)                           # the footbridge over the side arm
    zbr = round(max(gz(br[0]), gz(br[1])) + 0.10, 2)
    dk = (62.0 - P17_TERRACE_W, 62.0)                   # the viewing deck at the SW bank's edge (survey: it drops at 62 m)
    rp = (dk[0] - P17_DECK_UP * P17_RAMP, dk[0])        # its ramp, 1:12
    zr0 = gz(rp[0])
    zdk = round(zr0 + P17_DECK_UP, 2)
    bl = (127.0, 127.0 + bk)                            # the street side: bike lane, then the walk
    wl_ = (bl[1] + 1.0, bl[1] + 1.0 + wk)
    pieces = [_p17_flat(gz, pw[0], pw[1])[0], _p17_flat(gz, bl[0], wl_[1])[0],
              (a0, a1, [(a0, gz(a0)), (a0 + 0.8, zf), (a1 - 0.8, zf), (a1, gz(a1))]),
              (st0, st1, [(st0, zs), (st0, zs - STRIP_DEPTH), (st1, zs - STRIP_DEPTH), (st1, zs)])]
    prof = _p17_prof(gz, t0, t1, pieces)
    fills = [([(st0 - 0.15, zs), (st0 - 0.15, zs - STRIP_DEPTH - 0.15), (st1 + 0.15, zs - STRIP_DEPTH - 0.15),
               (st1 + 0.15, zs), (st1, zs), (st1, zs - STRIP_DEPTH), (st0, zs - STRIP_DEPTH), (st0, zs)], "concrete")]
    f = 1.0 - P17_ARM_WL / P17_ARM_D
    water = [[(a0 + 0.8 * f, zf + P17_ARM_WL), (a0 + 0.8, zf), (a1 - 0.8, zf), (a1 - 0.8 * f, zf + P17_ARM_WL)]]
    rush = ("soft_rush", "loosestrife")
    groups = [dict(a=t0 + 0.3, b=pw[0] - 0.3, t=(0.50, 0.56), mix=("plane", "ash", "chaste"), why=("shade",), seed=41),
              dict(a=br[1] + 0.3, b=rp[0] - 0.3, t=(0.50, 0.62), mix=("plane", "ash", "tamarisk", "chaste"),
                   why=("shade", "wind", "corridor"), seed=42),
              dict(a=dk[1] + 0.3, b=b0, t=(0.42, 0.10), mix=("ash", "tamarisk", "willow", "chaste", "loosestrife"),
                   why=("corridor", "shade"), seed=43),
              dict(a=b0 + 0.3, b=st0 - 0.3, t=(0.14, 0.02), mix=rush, dens=0.8, why=("cleaning", "corridor"), seed=44),
              dict(a=st1 + 0.3, b=93.5, t=(0.02, 0.04), mix=rush, dens=0.8, why=("cleaning", "corridor"), seed=45),
              dict(a=b1 + 0.3, b=121.0, t=(0.10, 0.45), mix=("loosestrife", "willow", "tamarisk", "chaste", "ash"),
                   why=("corridor", "shade"), seed=46),
              dict(a=121.0, b=bl[0] - 0.3, t=(0.50, 0.55), mix=("plane", "ash"), why=("shade", "noise"), seed=47)]
    bn = br[1] + 1.0                                    # a bench on the bank top, in the trees' shade
    avg = r["avg_flow"]
    wd = (94.0, 109.5)                                  # the shallow strip people wade and play in
    # the water's edge NE of it: the first ground above the average flow, and a sitting group there facing the water
    # if 3.5 m of dry bank fit before the NE bank's trees (else none, one log line)
    wm = (wd[0] + wd[1]) / 2.0
    e = next((wm + 0.25 * i for i in range(int((121.0 - wm) / 0.25)) if gz(wm + 0.25 * i) > avg), None)
    sit = None
    if e is not None:
        sit = (max(e, wd[1]) + 0.3, max(e, wd[1]) + 3.8)
        if sit[1] > 119.0 or any(gz(sit[0] + 0.25 * i) <= avg for i in range(int((sit[1] - sit[0]) / 0.25) + 1)):
            sit = None
    if sit is None:
        log.append(u"p.17 F4: no dry bank by the shallow strip for the water's edge (none drawn)")
    else:
        groups[5]["a"] = max(groups[5]["a"], sit[1] + 0.3)
    lp_ = wl_[1] + 0.4                                  # a lamp at the street walk, a bollard where the path starts
    bo_ = pw[0] + 0.4
    sw_, ne_ = place_name("bank_SW_short").upper(), place_name("bank_NE_short").upper()
    return dict(cid="F4", seed=4, rng=(t0, t1), prof=prof, fills=fills, water=water, groups=groups,
                focus=(wd[0] + wd[1]) / 2.0,
                avoid=[pw, br, (rp[0], dk[1]), bl, wl_, (bn - 0.3, bn + 0.8), (lp_ - 0.3, lp_ + 0.3)] +
                      ([sit] if sit else []),
                structures=[("lane", pw[0], pw[1], "walk"), ("bridge", br[0], br[1], zbr),
                            ("ramp", rp[0], rp[1], zr0, zdk), ("terrace", dk[0], dk[1], "b", zdk),
                            ("lane", bl[0], bl[1], "bike"), ("lane", wl_[0], wl_[1], "walk"),
                            ("stones", st0, st1), ("bench", bn, 1), ("lamp", lp_, -1), ("bollard", bo_)],
                people=[("walkway", pw[0], pw[1], None),
                        ("bridge_crossing", br[0] + 0.5, br[1] - 0.5, {"z": zbr, "focus": (a0 + a1) / 2.0}),
                        ("viewing_terrace", dk[0], dk[1], {"z": zdk, "n": 3}),
                        ("stepping_stones", st0, st1, {"n": 2}), ("wading_strip", wd[0], wd[1], {"n": 4})] +
                       ([("water_edge", sit[0], sit[1], {"n": 3, "dens": 1.6})] if sit else []) +   # fishing, watching
                       [("bike_lane", bl[0], bl[1], {"n": 1}), ("walkway", wl_[0], wl_[1], None)],
                back=[("walkway", pw[0], pw[1]), ("walkway", wl_[0], wl_[1])],
                zones=[(pw[0], pw[1], _p17_lane_txt(u"PATH", wk), u"along the bank to the footbridge"),
                       (br[0], br[1], u"BRIDGE", u"cross the side arm dry-shod"),
                       (br[1], rp[0], u"BANK TOP", u"a bench in the trees' shade"),
                       (rp[0], dk[1], u"VIEW TERRACE", u"up a ramp, a step-free view"),
                       (dk[1], b0, sw_, u"willows hold the flood bank"),
                       (st0, st1, u"STONES", u"cross the summer strip dry-shod"),
                       (wd[0], wd[1], u"WADING", u"wade, play, cool your feet")] +
                      ([(sit[0], sit[1], u"WATER'S EDGE", u"fish, watch the play")] if sit else []) +
                      [(b1, bl[0], ne_, u"trees between the water and the street"),
                       (bl[0], bl[1], _p17_lane_txt(u"BIKE", bk), u"street side, apart from walkers"),
                       (wl_[0], wl_[1], _p17_lane_txt(u"PATH", wk), u"behind the trees, off the traffic")],
                inset=(wd[0] + 3.0, wd[0] + 11.0, u"wading in the shallow strip"),
                caption=u"F4 · the lower reach: the side arm, the bank top and the widened stream")


def _p17_w1_ground(log):
    """DATA-1: W1's surveyed ground [(m from the SW end, m a.s.l.)] from the board's CUTS row "up" (the surveyed
    section ARAS = the W1 cut, research levels2_out.json: heights over the bed every 1 m from u0 = the SW end), checked
    against the level module (bed, length); None (FLAG line) when missing or not matching"""
    row = next((c_ for c_ in CUTS if c_.get("key") == "up"), None)
    bed = level("W1", "bed")
    ln = level("W1", "length_m")
    if not row or not row.get("ground"):
        log.append(u"FLAG p.17 W1: no surveyed profile (data/CUTS.py \"up\"): the bed is drawn flat at {}".format(
            u_level(bed)))
        return None
    if abs(float(row.get("bed") or 0.0) - bed) > 0.005 or (ln and abs(len(row["ground"]) - 1 - ln) > 1.0):
        log.append(u"FLAG p.17 W1: CUTS \"up\" (bed {}, {} m) does not match the level module (bed {}, {} m): the bed "
                   u"is drawn flat".format(row.get("bed"), len(row["ground"]) - 1, u_level(bed), ln))
        return None
    log.append(u"p.17 W1: ground from the surveyed section (data/CUTS.py \"up\", bed {}, every 1 m)".format(
        u_level(bed)))
    return [(float(i), round(bed + float(v), 2)) for i, v in enumerate(row["ground"])]


def _p17_f1(log):
    """W1 at the inflow (cut registry W1, = F1), scenario "a shaded street-side route, a look over the wall": the
    bike lane and the walk under the planes on the south bank with a lamp, the walled bed from the survey (DATA-1;
    nobody in its water, no blocks in it), the summer strip on its low point, the viewing terrace on the north wall
    top, the reed basins beyond"""
    r = _p17_reg("W1")
    bed = r["bed"]
    wsw, wne = _p17_wall(r)
    t0, t1 = P17_F1_RNG
    ws, wn = P17_F1_BED
    wtk = P17_WALL_T
    wk, bk = P14_PROM_W
    g = _p17_w1_ground(log)
    sw0, sw1 = P17_F1_STRIP
    if g:
        floor_pts, (st0, st1), sfl, fills = _p17_walled_bed(lambda t: _p17_interp(g, t), ws, wn, sw1 - sw0, log,
                                                            u"W1")
    else:                                               # the flat bed (FLAG logged), the zone base's strip
        st0, st1 = sw0, sw1
        floor_pts = [(ws, bed), (st0, bed), (st0, bed - STRIP_DEPTH), (st1, bed - STRIP_DEPTH), (st1, bed), (wn, bed)]
        fills = [([(st0 - 0.15, bed), (st0 - 0.15, bed - STRIP_DEPTH - 0.15), (st1 + 0.15, bed - STRIP_DEPTH - 0.15),
                   (st1 + 0.15, bed), (st1, bed), (st1, bed - STRIP_DEPTH), (st0, bed - STRIP_DEPTH), (st0, bed)],
                  "concrete")]
    prof = [(t0, wsw), (ws - wtk, wsw), (ws, wsw)] + floor_pts + [(wn, wne), (wn + wtk, wne), (t1, wne)]
    fills += [([(ws - wtk, wsw), (ws, wsw), (ws, bed - P17_GRAVEL), (ws - wtk, bed - P17_GRAVEL)], "stone"),
              ([(wn, wne), (wn + wtk, wne), (wn + wtk, bed - P17_GRAVEL), (wn, bed - P17_GRAVEL)], "stone")]
    bl = (t0 + 0.6, t0 + 0.6 + bk)
    wl_ = (bl[1] + 1.4, bl[1] + 1.4 + wk)
    vt = (wn + wtk, wn + wtk + P17_TERRACE_W)
    bx0 = vt[1] + 0.6
    beyond = [("reed", bx0, bx0 + 5.6, wne - P17_BASIN["depth"], wne),
              ("mint", bx0 + 6.2, min(t1 - 0.5, bx0 + 11.0), wne - P17_BASIN["depth"], wne)]
    rush = ("soft_rush", "loosestrife")
    groups = [dict(a=t0 + 0.2, b=ws - wtk - 0.3, t=(0.50, 0.56), mix=("plane", "ash", "chaste"),
                   why=("shade", "corridor"), seed=61),
              dict(a=ws + 0.2, b=ws + 2.0, t=(0.02, 0.05), mix=rush, dens=1.2, why=("cleaning",), seed=62),
              dict(a=wn - 2.0, b=wn - 0.2, t=(0.05, 0.02), mix=rush, dens=1.2, why=("cleaning",), seed=63)]
    bn = bl[1] + 0.5                                    # a bench between the bike lane and the path
    lp_ = wl_[1] + 0.3                                  # a lamp at the path's water side
    return dict(cid="W1", seed=1, rng=(t0, t1), prof=prof, fills=fills, groups=groups, beyond=beyond,
                focus=(st0 + st1) / 2.0,
                avoid=[bl, wl_, (bn - 0.3, bn + 0.8), (lp_ - 0.3, lp_ + 0.3)],
                structures=[("lane", bl[0], bl[1], "bike"), ("lane", wl_[0], wl_[1], "walk"),
                            ("terrace", vt[0], vt[1], "a", None), ("bench", bn, 1), ("lamp", lp_, 1)],
                people=[("bike_lane", bl[0], bl[1], {"n": 1}), ("walkway", wl_[0], wl_[1], None),
                        ("viewing_terrace", vt[0], vt[1], {"n": 2})],
                back=[("walkway", wl_[0], wl_[1])],
                arrows=[([((ws + wn) / 2.0 + 6.0, bed + 0.5), (wn - 1.0, wne - 0.6), (bx0 + 1.0, wne + 0.9)], C["w3"])],
                zones=[(bl[0], bl[1], _p17_lane_txt(u"BIKE", bk), u"through route under the trees"),
                       (wl_[0], wl_[1], _p17_lane_txt(u"PATH", wk), u"shaded by the south bank's trees"),
                       (st0, st1, u"SUMMER STRIP", u"the low flow, on the bed's lowest line"),
                       (vt[0], vt[1], u"VIEW TERRACE", u"on the wall top, over the bed"),
                       (bx0, t1, u"REED BASINS beyond", u"stream water cleaned there")],
                inset=(vt[0] - 1.0, vt[1] + 1.5, u"the viewing terrace on the wall top"),
                levels=[(wne, u"DSİ wall")],
                caption=u"W1 · the walled stream at the inflow, the reed basins beyond")


P17_S4_WHY = {"sw_path": ("shade", "noise"), "sw_slope": ("corridor", "shade"), "bed_sw": ("cleaning",),
              "open": ("cleaning",), "toe": ("cleaning", "corridor"),
              "terr_b": ("corridor", "perception"), "terr_c": ("shade", "corridor"), "prom": ("shade",),
              "fill": ("shade", "noise")}   # what each of p.14's planting zones does on S4 (G9)


def _p17_f3(log):
    """S4 (cut registry S4, = F3), scenario "sit in the sun between the bands": p.14's own cut and planting
    (_p14_geo, _p14_planting; round 3: on the survey datum, the bed from the surveyed profile, N1 a), so the cut is
    the same everywhere: the path, the planting bands of the widened stream by the days water covers the ground
    (PLANT_BANDS, RWS), the stones over the strip, the lower walk, the sun steps, the promenade with its lamp and the
    bike lane. Fills follow the survey: the gravel bed offset under the profile, the strip liner from G["strip_lip"]
    (p14_geo_interface.md)."""
    G = _p14_geo()
    t0, t1 = P17_F3_RANGE
    prof = [(t0, _p14_surf(t0))] + [p for p in G["prof"] if t0 < p[0] < t1] + [(t1, _p14_surf(t1))]
    bed, sfl, shelf, zn = G["bed"], G["sfl"], G["shelf"], G["zones"]
    st0, st1 = zn["strip"]
    lt = P14_LINER
    e0, p0 = zn["steps"]
    p1 = zn["prom"][1]
    p2 = zn["bike"][1]
    w0, w1 = P14_WALK
    tt0, tt1 = zn["terrace"]
    wk, bk = P14_PROM_W
    la, lb = G.get("strip_lip") or (bed, bed)           # the survey ground at the strip's two edges
    b0, b1 = G.get("b0", st0), G.get("b1", st1)
    bedp = [(b0, _p14_surf(b0))] + [p for p in G["prof"] if b0 < p[0] < b1] + [(b1, _p14_surf(b1))]
    fills = [(bedp + [(p[0], p[1] - P17_GRAVEL) for p in reversed(bedp)], "gravel"),   # the bed, under the survey
             ([(tt0, shelf), (tt1, shelf), (tt1, shelf - 0.3), (tt0, shelf - 0.3)], "gravel"),
             ([(st0 - lt, la), (st0 - lt, sfl - lt), (st1 + lt, sfl - lt), (st1 + lt, lb), (st1, lb), (st1, sfl),
               (st0, sfl), (st0, la)], "concrete"),
             ([(w0, shelf), (w1, shelf), (w1, shelf - 0.2), (w0, shelf - 0.2)], "concrete"),
             ([p for p in G["prof"] if e0 - 1e-9 <= p[0] <= p0 + 1e-9 and p[1] >= shelf - 1e-9] +
              [(p0, P14_PROM - 0.35), (e0, shelf - 0.35)], "concrete"),
             ([(p0, P14_PROM), (p2, P14_PROM), (p2, P14_PROM - P14_SLAB), (p0, P14_PROM - P14_SLAB)], "concrete")]
    fn = globals().get("_p14_planting")
    fixed = [tuple(p)[:4] for p in (fn() if callable(fn) else P14_PLANTS)]
    groups = [dict(a=zn[z_][0], b=zn[z_][1], fixed=True, why=P17_S4_WHY.get(z_, ()))
              for z_ in [q[0] for q in globals().get("P14_PLANT_ZONES", [])] if z_ in zn]
    # the bands: the ground's band code every 0.25 m, merged into runs; each run named once
    runs = []
    s = t0
    while s <= t1 + 1e-9:
        c_ = _p14_band_code(s, _p14_surf(s))
        if runs and runs[-1][0] == c_:
            runs[-1][2] = s
        else:
            runs.append([c_, s, s])
        s += 0.25
    bn = dict((b_[0], (b_[1], b_[3])) for b_ in PLANT_BANDS)
    bands, seen = [], set()
    for c_, a, b in runs:
        if b - a < 3.0 or c_ in seen:
            continue
        nm, days = bn.get(c_, (u"", u""))
        lab = (nm.split(u" (")[0].split(u" / ")[0].lower() + u" · " +
               days.replace(u" d/yr", u" d").replace(u"–", u"-").split(u";")[0]).strip(u" ·")
        bands.append((a, b + 0.25, lab, c_))
        seen.add(c_)
    sw = zn["sw_path"]
    return dict(cid="S4", seed=3, rng=(t0, t1), prof=prof, fills=fills, fixed=fixed, groups=groups,
                focus=(st0 + st1) / 2.0,
                structures=[("stones", st0, st1), ("lamp", p0 + 0.6, -1), ("lamp", sw[1] - 0.3, 1)],
                people=[("walkway", max(t0 + 0.5, sw[0]), sw[1], {"n": 2}), ("stepping_stones", st0, st1, {"n": 2}),
                        ("walkway", w0, w1, {"n": 2}), ("sun_steps", e0, p0, {"n": 3}), ("walkway", p0, p1, None),
                        ("bike_lane", p1, p2, {"n": 1})],
                back=[("walkway", p0, p1)],
                zones=[(max(t0, sw[0]), sw[1], u"PATH", u"the south bank walk under the trees"),
                       (st0, st1, u"STONES", u"cross the summer strip dry-shod"),
                       (w0, w1, u"LOWER WALK", u"along the water, between the bands"),
                       (e0, p0, u"SUN STEPS", u"sit in the sun, facing the water"),
                       (p0, p1, _p17_lane_txt(u"PROMENADE", wk), u"top-of-bank walk, shade trees"),
                       (p1, p2, _p17_lane_txt(u"BIKE", bk), u"on the bank top, apart from walkers")],
                inset=(e0 - 0.5, min(p0, e0 + 6.0), u"the sun steps"),
                bands=bands, levels=[(P14_PROM, u"promenade")],
                caption=u"S4 · the planting bands of the widened stream " + cite(P15_BAND_SRC))


# ---------------------------------------------------------------- booklet p19-20: four cuts at 1:500 (round 5)
# Round 4 (D2, N3 a, P18.1-P18.6; design spec handover/S6b_p18_design_spec.md): booklet p18 became two pages at 1:250
# (p18a = F2 + F4 trimmed to 73 m, p18b = W1 + S4), each block a LEFT template laid out on the board.
# Round 5 (S8, D7, N3 a decided by Aras: "1:500 with spans widened to fill the column, detail carried by insets at
# 1:100/1:200/1:250"; CHK-9): p19 and p20 merge into ONE booklet page, which the booklet composes. This page only
# EXPORTS: each cut is its own drawing at 1:500 (den 500, x = chainage m, y = m a.s.l.), with its numbered list
# (anchored at the numbered points), its levels (the booklet draws the U04 markers), its heading and note, its inset
# (its own drawing at 1:100-1:250, framed on the action, G-R5-5); one key map per booklet page id (km_map v2, no
# scale_den); the planting-band and material legends once (p19). The board only records; its layout of the cuts
# (stacked in the cell) does not matter to the booklet. Page ids: p18a = WBX_PG_SECT_A ("p19"), p18b = WBX_PG_SECT_B
# ("p20"); the round 4 tags stay as the keys code.py passes.
P18_DEN = 500.0                      # round 5 (N3 a, CHK-9): the four cuts at 1:500 (k = 2.0 mm/m; was 1:250, D2)
P18_PAGE = (392.0, 234.0)            # the board cell a page is drawn in, mm (code.py sizes its cells from it)
P18_COL_M = 137.0                    # m of cut a 274 mm drawing column holds at 1:500 (CHK-9: 70 % of 392 mm)
P18_ROW_GAP = 4.0                    # mm between two cuts stacked in the board cell (board only)
P18_INSET_BOX = (100.0, 60.0)        # mm: the most an inset may take on the page (design value; sf_inset_frame picks
#                                      the largest listed inset scale >= 2 x 1:500 that fits it: 1:100, 1:200 or 1:250)
P18_INSET_UNDER, P18_INSET_OVER = 0.30, 0.20   # m under the lowest ground / over a person's head kept in an inset's
#                                      focus (design values: the bed and water it shows, the head room)
P18_KM_MM = (110.0, 70.0)            # mm: the most space offered to a key map (km_map v2 fits its frame inside it;
#                                      the right column ~114 mm, CHK-9; design value)
P18_MK_ZONE, P18_MK_WATER = "8B3A3F", "5D7F8D"   # a designed use zone (accent) / a water or bed zone (p12 reads ZONE)
P18_WATER_ZONES = (u"STONES", u"WADING", u"SUMMER STRIP", u"SPILLWAY", u"WATER'S EDGE")
P18_BK_PAGE = {"p18a": WBX_PG_SECT_A, "p18b": WBX_PG_SECT_B}   # round 4 tag -> booklet page id (25-page, wb_items)
P18_W1_MONTH = 8                     # W1 on p20 shows the summer strip with its water (PLAN §8): a summer month (Aug)
# N3 a (round 5, Aras: spans widened to fill the 274 mm column at 1:500, ~137 m; never past the cut's data), m along:
#   F2: 40.6-177.6 m (137 m): the wall-top path (cut 3.4 m in), the walled bed, the spillway, the reed basins, the dry
#       bank, the shaded walk with its bike lane and the rain terraces up to the view terrace on the top tread (the
#       designed part runs 37.0-177.6 m; the survey 0-199 m)
#   F4: 3.0-140.0 m (137 m): the shade trees, the path, the footbridge over the side arm, the bank top, the ramp and
#       deck, the widened bed, the NE bank and the street-side bike lane and walk (survey 0-151 m)
#   S4: -46.0-52.0 m (98 m): p.14's whole built profile street to street (the cut line runs 530.8 m, but the board
#       builds S4's profile only between the two streets: p14_15_s4.py P14_RANGE; never extended here)
#   W1: drawn whole as _p18_w1 builds it (the surveyed section is 0-69 m: CUTS "up"; 69 m = 138 mm)
P18_F2_RNG = (40.6, 177.6)
P18_F4_RNG = (3.0, 140.0)
P18_S4_RNG = (-46.0, 52.0)
# W1's way down (P18.3, G-R4-5.7; ASKS_resolved §2: Aras's own choice, 31 Oct 12:01): the SW DSİ wall cut back into
# sitting steps with planted landings to a floor at the wall foot, exactly the rules of p13's W1 (proposal sections
# PS_W1_SIT, PS_W1_FLIGHTS, PS_W1_LAND, PS_W1_POCKET, PS_W1_FLOOR_W, PS_W1_FLOOR_UP, PS_RAIL_DROP; design rules, not
# data), applied to this cut's surveyed bed (DATA-1). Closing round 4: the water board's one copy of those values;
# p12's band draws the same steps from them (pages/p12_system.py _p12_w1_steps)
P18_W1_SIT = (0.80, 0.45)            # m: sitting step tread, largest riser (seat high)
P18_W1_FLIGHTS = 3                   # flights, a landing between two
P18_W1_LAND = 2.40                   # m: a landing (the way on at its front, a planted pocket at its back)
P18_W1_POCKET = (1.20, 0.60)         # m: the planted pocket on a landing: width, soil depth
P18_W1_FLOOR_W = 1.60                # m: the floor at the wall foot
P18_W1_FLOOR_UP = 0.25               # m: that floor at least this far over the average-flow water
P18_RAIL_DROP = 0.50                 # m: a drop deeper than this gets a railing
# the pages: crop id (the round 4 crop each page's drawings replace), the two cuts, (unused since round 5)
P18_PAGES = {"p18a": ("wb_plants_b1", ("F2", "F4"), 1), "p18b": ("wb_plants_b2", ("W1", "S4"), 0)}
P18_TITLES = {"p18a": u"WHICH PLANT GOES WHERE, IN SECTION · F2 and F4",     # round 5: no scale in a title (the
              "p18b": u"WHICH PLANT GOES WHERE, IN SECTION · W1 and S4"}     # booklet prints 1:den)
P18_CUT_HEAD = {  # a cut's heading (after the cut id) and its note (the scenario, keywords)
    "F2": (u"Upstream entry: the walled stream, the reed basins and the rain terraces",
           u"cross dry-shod, clean the run-off, walk in the shade"),
    "F4": (u"Lower reach: the side arm, the widened stream and its banks", u"wade, play, watch from the deck"),
    "W1": (u"Inflow: the walled stream and the steps down", u"sit down to the water, wade in the summer strip"),
    "S4": (u"The planting bands of the widened stream", u"sit in the sun between the bands")}


def _p18_zname(nm):
    """a zone's name for the list: the banks' place names as the names table spells them, the rest in sentence case"""
    for s_ in ("SW", "NE"):
        try:
            pn = place_name(u"bank_{}_short".format(s_))
        except Exception:
            continue
        if nm == pn.upper():
            return pn
    return nm[:1] + nm[1:].lower()


def _p18_trim(spec, t0, t1, breaks):
    """a copy of a p17 section spec drawn only from t0 to t1 m (N3 a): its profile, planting groups, people, zones
    and structures cut to that part (what lies wholly outside it goes); break marks on the trimmed sides; no arrows
    (G-R4-5.7). The p17 spec itself is not changed (page A draws its plan places from it)."""
    s = dict(spec)
    prof = spec["prof"]
    s["prof"] = [(t0, _p17_gz(prof, t0))] + [p for p in prof if t0 < p[0] < t1] + [(t1, _p17_gz(prof, t1))]
    s["rng"] = (t0, t1)
    s["groups"] = [dict(g, a=max(g["a"], t0 + 0.3), b=min(g["b"], t1 - 0.3)) for g in spec.get("groups", [])
                   if min(g["b"], t1 - 0.3) - max(g["a"], t0 + 0.3) >= 1.0]
    st = []
    for q in spec.get("structures", []):
        if q[0] in ("bench", "lamp", "bollard", "rail"):
            if t0 + 0.5 <= q[1] <= t1 - 0.5:
                st.append(q)
        elif q[2] > t0 and q[1] < t1:
            st.append(q)
    s["structures"] = st
    s["people"] = [(z_[0], max(z_[1], t0), min(z_[2], t1)) + tuple(z_[3:]) for z_ in spec.get("people", [])
                   if min(z_[2], t1) - max(z_[1], t0) >= 1.0]
    s["back"] = [(z_[0], max(z_[1], t0), min(z_[2], t1)) for z_ in spec.get("back", [])
                 if min(z_[2], t1) - max(z_[1], t0) >= 1.0]
    s["zones"] = [(max(z_[0], t0), min(z_[1], t1)) + tuple(z_[2:]) for z_ in spec.get("zones", [])
                  if min(z_[1], t1) - max(z_[0], t0) >= 1.0]
    s.pop("arrows", None)
    s["breaks"] = tuple(breaks)
    return s


def _p18_w1(log):
    """W1 for p18b (= p17's F1 spec, the same registry cut): the walled bed from the survey, the view terrace on the
    NE wall top and the reed basins beyond it as p17 draws them; the SW side redrawn with the way down (P18.3): the
    DSİ wall cut back (today's wall dashed) into sitting steps in P18_W1_FLIGHTS flights with seat-high risers, planted
    landings between them, a floor at the wall foot (railed where the bed drops more than P18_RAIL_DROP), people
    sitting and walking on them; the path and the bike lane behind the steps' head under the south bank's trees.
    The number of steps follows this cut's surveyed bed at the wall foot (p13 places its walls its own way)."""
    base = _p17_specs(log).get("W1")
    if not base:
        raise RuntimeError(u"W1: the p17 section spec was not built (see the WARNING line above)")
    r = _p17_reg("W1")
    wsw, wne = _p17_wall(r)
    ws, wn = P17_F1_BED
    wtk = P17_WALL_T
    wk, bk = P14_PROM_W
    floor_pts = list(base["prof"][3:-3])                # _p17_f1: [(t0, wsw), (ws - wtk, wsw), (ws, wsw)] + bed + 3
    fills = list(base["fills"][:-2]) + [base["fills"][-1]]   # the bed fills and the NE wall (the SW wall is cut back)
    zw = floor_pts[0][1]                                # the bed at the SW wall foot
    fl = math.ceil(max(r["avg_flow"] + P18_W1_FLOOR_UP, zw) * 20.0) / 20.0
    n = int(math.ceil((wsw - fl) / P18_W1_SIT[1] - 1e-9))
    rise = (wsw - fl) / n
    nf = max(1, min(P18_W1_FLIGHTS, n))
    fls = [n // nf + (1 if i < n % nf else 0) for i in range(nf)]
    u, z = ws - P18_W1_FLOOR_W, fl
    steps, blocks, flights, lands = [(ws, fl), (u, fl)], [], [], []
    for i, m in enumerate(fls):                         # flight by flight, climbing to the SW (toward t 0)
        uf = u
        for j in range(m):
            z += rise
            steps.append((u, z))
            if i == nf - 1 and j == m - 1:
                break
            w = P18_W1_LAND if j == m - 1 else P18_W1_SIT[0]
            blocks.append((u - w + (P18_W1_POCKET[0] if j == m - 1 else 0.0), u, z - rise - 0.15, z))
            if j == m - 1:
                flights.append((u, uf))
                lands.append((u - w, u, z))
            u -= w
            steps.append((u, z))
    flights.append((u, uf))
    head = u
    pa = (head - 0.3 - wk, head - 0.3)                  # the path at the steps' head, the bike lane outside it
    bl = (pa[0] - 1.0 - bk, pa[0] - 1.0)
    has_bike = bl[0] - 0.3 >= 0.0
    if not has_bike:
        log.append(u"NOTE p18b W1: the bike lane does not fit between the steps' head ({:.1f} m) and the cut's SW end: "
                   u"not drawn".format(head))
    t0, t1 = max(0.0, (bl[0] if has_bike else pa[0]) - 0.4), P17_F1_RNG[1]
    prof = [(t0, wsw), (head, wsw)] + list(reversed(steps)) + floor_pts + [(wn, wne), (wn + wtk, wne), (t1, wne)]
    fills += [([(ws - wtk, zw - P17_GRAVEL), (ws, zw - P17_GRAVEL), (ws, fl), (ws - wtk, fl)], "stone"),
              ([(ws - P18_W1_FLOOR_W, fl - 0.25), (ws - wtk, fl - 0.25), (ws - wtk, fl), (ws - P18_W1_FLOOR_W, fl)],
               "concrete")]
    fills += [([(a, z0), (b, z0), (b, z1), (a, z1)], "stone") for a, b, z0, z1 in blocks]
    vt = (wn + wtk, wn + wtk + P17_TERRACE_W)
    bx0 = vt[1] + 0.6
    st_ = next(((z_[0], z_[1]) for z_ in base.get("zones", []) if z_[2] == u"SUMMER STRIP"), None)
    st0, st1 = st_ if st_ else (P17_F1_STRIP[0], P17_F1_STRIP[1])
    rush = ("soft_rush", "loosestrife")
    groups = [dict(a=t0 + 0.2, b=head - 0.3, t=(0.50, 0.56), mix=("plane", "ash", "chaste"), why=("shade", "corridor"),
                   seed=61),
              dict(a=ws + 0.2, b=ws + 2.0, t=(0.02, 0.05), mix=rush, dens=1.2, why=("cleaning",), seed=62),
              dict(a=wn - 2.0, b=wn - 0.2, t=(0.05, 0.02), mix=rush, dens=1.2, why=("cleaning",), seed=63)]
    structures = [("lane", pa[0], pa[1], "walk"), ("terrace", vt[0], vt[1], "a", None), ("lamp", head - 0.15, 1),
                  ("ghost", ws - wtk, ws, zw, wsw)]
    avoid = [pa, (head - 0.45, head + 0.15)]
    people = [("walkway", pa[0], pa[1], None)]
    zones = []
    if has_bike:
        bn = bl[1] + 0.2                                # a bench between the bike lane and the path
        structures += [("lane", bl[0], bl[1], "bike"), ("bench", bn, 1)]
        avoid += [bl, (bn - 0.3, bn + 0.8)]
        people.insert(0, ("bike_lane", bl[0], bl[1], {"n": 1}))
        zones.append((bl[0], bl[1], _p17_lane_txt(u"BIKE", bk), u"through route under the trees"))
    if fl - _p17_gz(floor_pts, ws + 0.5) > P18_RAIL_DROP:
        structures.append(("rail", ws - 0.15, fl))
    people += [("sun_steps", fa + 0.05, fb - 0.05, {"p": {"seat_h": rise}, "dens": 1.5}) for fa, fb in flights]
    people += [("walkway", la + P18_W1_POCKET[0] + 0.1, lb - 0.1, {"n": 1}) for la, lb, _z in lands]
    people += [("viewing_terrace", ws - P18_W1_FLOOR_W + 0.1, ws - 0.1, {"n": 2}),
               ("viewing_terrace", vt[0], vt[1], {"n": 2})]
    # round 5 (PLAN §8, W1 on p20: the summer strip with its water): wading on the strip, gated in _p17_section by
    # sf_activity_ok (water drawn there, <= 0.50 m deep, month P18_W1_MONTH with the strip's water)
    people.append(("wading_strip", st0 + 0.2, st1 - 0.2, {"n": 2}))
    zones += [(pa[0], pa[1], _p17_lane_txt(u"PATH", wk), u"shaded by the south bank's trees"),
              (head, ws - P18_W1_FLOOR_W, u"SITTING STEPS",            # G-R5-4.6: no "8 x 41 cm" (a width)
               u"{} seat-high steps in {} flights, planted landings".format(n, nf)),
              (ws - P18_W1_FLOOR_W, ws, u"EDGE FLOOR", u"at the foot of the steps"),
              (st0, st1, u"SUMMER STRIP", u"the low flow, on the bed's lowest line"),
              (vt[0], vt[1], u"VIEW TERRACE", u"on the wall top, over the bed"),
              (bx0, t1, u"REED BASINS beyond", u"stream water cleaned there")]
    log.append(u"p18b W1: way down = sitting steps (p13 W1 rules PS_W1_*): {} steps × {:.0f} cm in {} flights {}, "
               u"edge floor {} at the SW wall foot (bed there {}), steps' head at {:.1f} m".format(
                   n, rise * 100.0, nf, u"/".join(str(f_) for f_ in fls), u_level(fl), u_level(zw), head))
    return dict(cid="W1", seed=1, rng=(t0, t1), prof=prof, fills=fills, groups=groups, beyond=list(base.get("beyond", [])),
                focus=(st0 + st1) / 2.0, avoid=avoid, structures=structures, people=people,
                back=[("walkway", pa[0], pa[1])], zones=zones,
                low=[(la, la + P18_W1_POCKET[0], 0.30, 0.50, 70 + i) for i, (la, lb, _z) in enumerate(lands)],
                inset=(ws - P18_W1_FLOOR_W - 3.0, ws + 1.0, u"sitting steps and the edge floor"),
                levels=[(wne, u"DSİ wall")], breaks=(("L",) if t0 > 1.0 else ()),
                month=P18_W1_MONTH, strip_water=True)


def _p18_specs(log):
    """the four cuts of p19 / p20, built once a run from p17's specs (copies; page A's plan keeps reading p17's):
    F2, F4 and S4 cut to their round 5 spans at 1:500 (N3 a: P18_F2_RNG, P18_F4_RNG, P18_S4_RNG, ~137 m where the
    data reach), W1 with its way down (_p18_w1), drawn whole; each with its shrub and flower layer
    ("low", G-R4-5.2). {cid: spec}; a cut that cannot be built RAISES (closing round 4: a missing section stops the
    run with the cut and the reason, never an empty row)."""
    if "p18specs" in _P17_MEMO:
        return _P17_MEMO["p18specs"]
    base = _p17_specs(log)
    out = {}
    try:
        if "F2" in base:
            s = _p18_trim(base["F2"], P18_F2_RNG[0], P18_F2_RNG[1], ("L", "R"))
            s["low"] = [(z_[0] + 0.5, z_[1] - 0.3, 0.55, 0.85, 124) for z_ in s["zones"] if z_[2] == u"DRY BANK"]
            out["F2"] = s
            log.append(u"FLAG p18a F2: the project data hold no designed way down into F2's walled bed (zone base, p17 "
                       u"F2 spec, old p18): none drawn, and no arrow in its place (P18.3 open for F2)")
        if "F4" in base:
            s = _p18_trim(base["F4"], P18_F4_RNG[0], P18_F4_RNG[1], ("L", "R"))
            sw_, ne_ = place_name("bank_SW_short").upper(), place_name("bank_NE_short").upper()
            s["low"] = [(z_[0] + 0.3, z_[1] - 0.3, 0.42, 0.12, 143) for z_ in s["zones"] if z_[2] == sw_] + \
                       [(z_[0] + 0.3, z_[1] - 0.3, 0.12, 0.50, 146) for z_ in s["zones"] if z_[2] == ne_]
            out["F4"] = s
    except Exception as ex:
        raise RuntimeError(u"p18a F2/F4: the trimmed section specs could not be built: {}: {}".format(
            type(ex).__name__, ex))
    try:
        out["W1"] = _p18_w1(log)
    except Exception as ex:
        raise RuntimeError(u"p18b W1: the section spec could not be built: {}: {}".format(type(ex).__name__, ex))
    if "S4" in base:                                    # p.14's cut and plants; its low layer as p.14 draws it
        s = dict(base["S4"])
        s.pop("arrows", None)
        try:                                            # round 5: p.14's whole built profile (P18_S4_RNG)
            s = _p18_trim(s, P18_S4_RNG[0], P18_S4_RNG[1], ("L", "R"))
        except Exception as ex:
            log.append(u"FLAG p18b S4: not trimmed to {:.0f}-{:.0f} m ({}: {}): drawn whole".format(
                P18_S4_RNG[0], P18_S4_RNG[1], type(ex).__name__, ex))
        r0_, r1_ = s.get("rng") or (-1e9, 1e9)
        zn = _p14_geo()["zones"]
        s["low"] = [(max(zn[z_][0], r0_), min(zn[z_][1], r1_), ta, tb, seed + 60, [k_ for k_ in mix if k_ in PLA_LOW],
                     P14_LOW_DENS * dens)
                    for z_, ta, tb, mix, dens, seed in P14_PLANT_ZONES
                    if z_ in P14_LOW_ZONES and z_ in zn and any(k_ in PLA_LOW for k_ in mix)
                    and min(zn[z_][1], r1_) - max(zn[z_][0], r0_) > 0.5]
        out["S4"] = s
    _P17_MEMO["p18specs"] = out
    return out


def _p18_sp_name(key, log):
    """a species "English (Turkish)" from plants.py (D5); a Turkish name the module marks unverified is left out
    (FLAG once)"""
    sp = PLA_SPECIES[key]
    tr = (sp.get("turkish") or u"").strip()
    if not tr or u"UNVERIFIED" in tr.upper():
        ln = u"FLAG p18 legend: {} has no verified Turkish name in plants.py: English only".format(sp["name"])
        if ln not in _P17_MEMO.setdefault("p18flags", []):
            _P17_MEMO["p18flags"].append(ln)
            log.append(ln)
        return sp["name"]
    return u"{} ({})".format(sp["name"], tr)


def _p18_bands(log):
    """the planting-band legend entries, wet to dry (the four P17_BANDS of p16 / p17, the lined basins' two species):
    [(swatch in the band's colour, "band: species English (Turkish), ...")] (D5)"""
    rows = [(P17_BAND_COL[i], P17_BAND_NAME[i], [k_ for k_ in keys if k_ in P17_CAT])
            for i, keys in enumerate(P17_BANDS)]
    rows.append((P17_ZONE["WT"][1], u"lined basins", [k_ for k_ in ("reed", "mint") if k_ in P17_CAT]))
    return [(wbx_sw("fill", colr), u"{}: {}".format(nm, u", ".join(_p18_sp_name(k_, log) for k_ in keys)))
            for colr, nm, keys in rows if keys]


def _p18_materials():
    """the material and water legend entries (G-R5-4.1: solid colour swatches, S3 sct_material_key; the water body,
    the Q100 / Q500 lines as water_section draws them)"""
    out = list(sct_material_key(("earth", "stone", "concrete", "gravel", "timber")))
    out += [(wbx_sw("fill", SCT_WATER["body"], stroke=SCT_WATER["surface"]), u"Water at the average yearly flow"),
            (wbx_sw("dash", SCT_WATER["flood"], width_pt=round(0.25 / PT, 2), dash_pt=[round(1.2 / PT, 2),
                                                                                        round(0.6 / PT, 2)]),
             u"Q100 flood level"),
            (wbx_sw("dash", SCT_WATER["flood"], width_pt=round(0.25 / PT, 2), dash_pt=[round(0.4 / PT, 2),
                                                                                        round(0.5 / PT, 2)]),
             u"Q500 flood level")]
    return out


def _p18_keymap(page, cids, log):
    """the page's key map (G-R5-3, S2 km_map v2): only the page's cuts, whole, with their own cut labels and look
    arrows; called WITHOUT scale_den (fitted frame, auto turn, its own north arrow, no scale bar), not drawn on the
    board: exported (wbx_keymap), the booklet places it in the right column. A key map that cannot be made is a
    WARNING (the page goes on)."""
    try:
        km = km_map(list(cids), P18_KM_MM[0], P18_KM_MM[1], page=wbx_p(page), log=log)
    except Exception as ex:
        wbx_warn(page, "keymap", u"key map of {} not made: {}: {}".format(u" + ".join(cids), type(ex).__name__, ex))
        return None
    if not km.get("items"):
        wbx_warn(page, "keymap", u"key map of {}: no basemap data (run the site board once)".format(u" + ".join(cids)))
        return None
    wbx_keymap(page, km, item_id=u"wb_km_" + page)
    for ln in KM_LOG[-1:]:
        if ln not in log:
            log.append(ln)
    return km


def _p18_list(page, did, spec, dx, dy, bb):
    """the numbered list of a cut (G-R4-5.5, C4): one row per distinct "Name · reason" in reading order (left to
    right), anchored at the point it names (use zones on their ground, planting groups in their crown; board mm,
    inside the drawing); the booklet sets the numbers and the rows (nothing drawn on the board). Returns the rows."""
    rows, anchors, seen = [], [], set()
    for kind, nm, why, x, y, _colour in sorted(spec.get("marks", []), key=lambda q: q[3]):
        key = (nm, why)
        if key in seen:
            continue
        seen.add(key)
        rows.append(u"{} · {}".format(nm, why) if why else nm)
        anchors.append((min(max(x + dx, bb[0]), bb[2]), min(max(y + dy, bb[1]), bb[3])))
    if rows:
        wbx_list(page, did, rows, numbered=True, anchors_board=anchors, id=did + u"_list")
    return rows


def _p18_levels(page, did, spec):
    """the cut's levels (G-R5-4.3): Q500, Q100, the average flow, the bed (registry) and the cut's own (DSİ wall,
    promenade) as a level item on the drawing's y (m a.s.l.); the booklet draws the U04 markers"""
    rows = [(SF_LEVEL_NAMES.get(key, u"%s" % key), float(z)) for key, z, _y in spec.get("level_rows", [])]
    if rows:
        wbx_levels(page, did, rows, side="R")
    SF_LOG.append(u"levels {} {} gap ok: {} markers exported to the booklet".format(page, spec["cid"], len(rows)))
    return rows


def _p18_inset(pg, page, spec, did, pbb, at, log):
    """the cut's zoom inset v2 (G-R5-5, S3 §2 step 5): framed on the action (sf_inset_frame: the spec's inset stretch
    from its lowest ground - P18_INSET_UNDER to its highest + a person + P18_INSET_OVER, every person of the cut plane
    the frame would cut taken in, at the largest listed inset scale >= 2 x 1:500 that fits P18_INSET_BOX), then the
    SAME spec drawn again at that scale (_p17_section inset=True: the same people and plants at the same metres, the
    kit's detail on), placed on the board with the window's lower left at `at` (board mm; the board's layout does not
    matter), exported as its own drawing (den, origin = (chainage, m a.s.l.) of the window's lower left) and linked
    to its parent (wbx_inset, window in the parent's board mm). Nothing is ever skipped silently (WARNING).
    Returns the child's board box or None."""
    ins = spec.get("inset")
    if not ins:
        return None
    g = spec["geo"]
    t0, t1, zb, kp = g["t0"], g["t1"], g["zb"], g["k"]
    a, b = max(ins[0], t0), min(ins[1], t1)
    if b - a < 0.5:
        wbx_warn(page, "inset", u"{} inset ({}) lies outside the drawn span: not drawn".format(spec["cid"], ins[2]))
        return None
    prof = spec["prof"]
    zs = [_p17_gz(prof, a + (b - a) * i / 20.0) for i in range(21)]
    focus = [(a, min(zs) - P18_INSET_UNDER, b, max(zs) + FIG_ADULT_H + P18_INSET_OVER)]
    ppl = []
    for pose, t, h in spec.get("placed", []):
        zg = _p17_gz(prof, t)
        ppl.append((u"{} at {:.1f} m".format(pose, t), (t - h, zg, t + h, zg + FIG_ADULT_H)))
    lab = u"{} {}".format(spec["cid"], ins[2])
    fr = sf_inset_frame(focus, P18_DEN, box_mm=P18_INSET_BOX, page=page, label=lab)
    if not fr:
        return None
    for _i in range(2):                                 # a person the frame cuts is taken in (U16), then framed again
        w = fr["window"]
        cut = [bx for _n, bx in ppl if not (bx[0] >= w[0] and bx[2] <= w[2] and bx[1] >= w[1] and bx[3] <= w[3]) and
               not (bx[2] <= w[0] or bx[0] >= w[2] or bx[3] <= w[1] or bx[1] >= w[3])]
        if not cut:
            break
        focus += cut
        fr = sf_inset_frame(focus, P18_DEN, box_mm=P18_INSET_BOX, page=page, label=lab) or fr
    w = fr["window"]
    w = (max(w[0], t0), w[1], min(w[2], t1), w[3])      # never past the drawn ground (no extrapolation)
    sf_inset_cut_check(w, ppl, page=page, label=lab)
    child = dict(spec)                                  # the same spec (its "_act" decisions shared), no inset of its own
    child.pop("inset", None)
    try:
        cp = _p17_section(child, "a", log, fr["den"], page + u" inset", inset=True)
    except Exception as ex:
        wbx_warn(page, "inset", u"{}: not drawn: {}: {}".format(lab, type(ex).__name__, ex))
        return None
    kc = child["geo"]["k"]
    cx, cy = at[0] - (w[0] - t0) * kc, at[1] - (w[1] - child["geo"]["zb"]) * kc
    cbb = (at[0], at[1], at[0] + (w[2] - w[0]) * kc, at[1] + (w[3] - w[1]) * kc)
    cdid = did + u"_inset"
    n0 = wbx_mark(pg)
    pg.items += _p17_move(cp.items, cx, cy)
    wbx_drawing(cdid, page, pg, cbb, n0=n0, n1=wbx_mark(pg), den=float(fr["den"]), origin=(w[0], w[1]),
                dkind="section", scale_pref=[int(fr["den"])])
    win = (pbb[0] + (w[0] - t0) * kp, pbb[1] + (w[1] - zb) * kp, pbb[0] + (w[2] - t0) * kp, pbb[1] + (w[3] - zb) * kp)
    wbx_inset(page, did, win, cdid)
    wbx_text(page, ins[2][:1].upper() + ins[2][1:], "caption", did=cdid, group=cdid, id=cdid + u"_cap")
    log.append(u"{} {} inset (G-R5-5): {} at 1:{:,.0f} in its own drawing (parent 1:{:,.0f}, {:.1f} x), window "
               u"{:.1f}-{:.1f} m x {:+.2f}-{:+.2f}, {} people in the cut plane checked against the frame".format(
                   page, spec["cid"], ins[2], fr["den"], P18_DEN, P18_DEN / fr["den"], w[0], w[2], w[1], w[3],
                   len(ppl)))
    return cbb


def p18_page(pg, box, page, opt, log):
    """booklet p19 ("p18a": F2 + F4) or p20 ("p18b": W1 + S4), merged into one booklet page by the booklet (D7):
    round 5 (S8, G-R5-12) the page EXPORTS its cuts, it lays nothing out. Each cut at 1:500 (N3 a) is drawn on the
    board (stacked in box, the cell under its title; the board's layout does not matter) and registered as its own
    drawing (den 500, origin = (chainage at the drawing's left edge, m a.s.l. at its foot), crop = the page's round 4
    crop), with its heading and note (wbx_text), its numbered list anchored at the numbered points (wbx_list), its
    levels (wbx_levels), its inset as its own drawing (_p18_inset); the page's key map (wbx_keymap) and, on p19, the
    planting-band and material legends (wbx_legend, once for the merged page). Nothing here raises on layout: a cut
    that cannot be drawn is a WARNING and the other one still goes. Returns [(crop id, bbox, 500)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    crop, cids, _leg = P18_PAGES[page]
    bpg = P18_BK_PAGE[page]
    x0, y1 = box[0], box[3]
    fig0 = FIG_COUNT[0]
    tri = sf_triangles(walls=False, aggregate=False)
    try:
        specs = _p18_specs(log)
    except Exception as ex:
        specs = {}
        wbx_warn(bpg, "section", u"the section specs could not be built: {}: {}".format(type(ex).__name__, ex))
    y, ybot, dids = y1, y1, []
    ix0, iy = x0 + P18_COL_M * sf_k(P18_DEN) + 2.0 * P18_ROW_GAP, y1   # the insets' board column, right of the cuts
    for cid in cids:
        if cid not in specs:
            why = next((ln for ln in log if ln.startswith(u"WARNING p.17 section {} ".format(cid))), None)
            wbx_warn(bpg, "section", u"{}: no section spec, not drawn ({})".format(cid, why or u"p17 has no spec"))
            continue
        spec = specs[cid]
        try:
            part = _p17_section(spec, "a", log, P18_DEN, bpg)
        except Exception as ex:
            wbx_warn(bpg, "section", u"{}: not drawn: {}: {}".format(cid, type(ex).__name__, ex))
            continue
        W, top = spec["dbox"][2], spec["dbox"][3]
        g = spec["geo"]
        dx, dy = x0, y - top
        bb = (dx, dy, dx + W, y)
        did = u"wb_{}_{}".format(bpg, cid)
        n0 = wbx_mark(pg)
        pg.items += _p17_move(part.items, dx, dy)       # the drawing (no text in it), its origin on bb's corner
        wbx_drawing(did, bpg, pg, bb, n0=n0, n1=wbx_mark(pg), den=P18_DEN, origin=(g["t0"], g["zb"]),
                    dkind="section", crop=crop)
        dids.append(did)
        tt, sc = P18_CUT_HEAD.get(cid, (u"", u""))
        wbx_text(bpg, u"{} · {}".format(cid, tt) + (u" " + cite(P15_BAND_SRC) if cid == "S4" else u""), "heading",
                 did=did, group=did, id=did + u"_head", priority=2)
        try:
            sides = [place_name(u"bank_{}_short".format(s_)) for s_ in level_end_labels(spec["cid"])]
            sc = (sc + u" · " if sc else u"") + u"{} left, {} right".format(sides[0], sides[1])
        except Exception:
            pass
        wbx_text(bpg, sc, "note", did=did, group=did, id=did + u"_note")
        nl = _p18_list(bpg, did, spec, dx, dy, bb)
        nv = _p18_levels(bpg, did, spec)
        cb = _p18_inset(pg, bpg, spec, did, bb, (ix0, iy - P18_INSET_BOX[1]), log)
        if cb:
            iy = cb[1] - P18_ROW_GAP
        log.append(u"{} {}: drawing {} 1:{:,.0f}, {:.1f}-{:.1f} m ({:.0f} m{}), {:.0f} x {:.0f} mm, {} list rows, {} "
                   u"levels, inset {}, bridges {}".format(
                       bpg, cid, did, P18_DEN, g["t0"], g["t1"], g["t1"] - g["t0"],
                       u", {:.0f} % of the {:.0f} m column".format(100.0 * (g["t1"] - g["t0"]) / P18_COL_M, P18_COL_M),
                       W, top, len(nl), len(nv),
                       u"yes" if cb else u"no",
                       u"; ".join(u"{} {} at {:.0f} m".format(*b_) for b_ in spec.get("bridges", [])) or u"none"))
        y = dy - P18_ROW_GAP
        ybot = min(ybot, dy)
    sf_triangles(**tri)
    if dids:
        _p18_keymap(bpg, [c_ for c_ in cids if c_ in specs], log)
        if page == "p18a":                              # once for the merged p19-20 page (the four cuts share them)
            wbx_legend(bpg, dids[0], _p18_bands(log), title=u"Planting bands · wet to dry", id=u"wb_p19_bands")
            wbx_legend(bpg, dids[0], _p18_materials(), title=u"Materials and water", id=u"wb_p19_materials")
    log.append(u"figures set={} {} ({})".format(FIG_SET, FIG_COUNT[0] - fig0, bpg))
    cl = cut_log_line()
    if cl:
        log.append(u"{} {}".format(bpg, cl))
    gl = sf_g14_line()
    if gl:
        log.append(gl)
    for ln in SF_LOG:
        if (ln.startswith(u"inset " + bpg) or ln.startswith(u"levels " + bpg)) and ln not in log:
            log.append(ln)
    log.append(u"{}: {} at 1:{:,.0f} exported as {} drawings (+ insets), the booklet merges p19 and p20 (D7)".format(
        bpg, u" + ".join(cids), P18_DEN, len(dids)))
    return [(crop, (x0, min(ybot, y1 - 1.0), x0 + P18_PAGE[0], y1), P18_DEN)]
