def write_city_link_movement(S, R):
    """v34: length-weighted walking potential (index, 100 = busiest street piece today) on the spine pieces with the
    spine, and on the existing streets within 40 m of the main Selinus line today and with the spine."""
    pieces, IDX, xy = R["pieces"], R["IDX"], R["xy"]
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    main = max(streams, key=pl_length) if streams else None

    def mean(ids, key):
        L_ = sum(pieces[i]["L"] for i in ids)
        return sum(IDX[key].get(i, 0.0) * pieces[i]["L"] for i in ids) / L_ if L_ > 0 else None
    sp = [i for i, p in enumerate(pieces) if p["prop"] == "spine"]
    edge = []
    if main:
        segs = list(zip(main[:-1], main[1:]))
        for i, p in enumerate(pieces):
            if p["prop"] or not p["walk"]:
                continue
            m = ((xy[p["a"]][0] + xy[p["b"]][0]) / 2.0, (xy[p["a"]][1] + xy[p["b"]][1]) / 2.0)
            if S.F.inside(m[0], m[1]) and min(_proj(m, a, b)[1] for a, b in segs) <= 40.0:
                edge.append(i)
    out = dict(script=SCRIPT_VERSION, run_time=time.strftime("%Y-%m-%d %H:%M:%S"),
               spine_source=(getattr(S, "city_link", None) or {}).get("src", "curves wired into the board"),
               spine_m=round(sum(pieces[i]["L"] for i in sp)), spine_walk_index=mean(sp, "walk_a") if sp else None,
               edge_m=round(sum(pieces[i]["L"] for i in edge)), edge_walk_today=mean(edge, "walk_b"),
               edge_walk_with=mean(edge, "walk_a"), slope=bool(getattr(pieces, "z", None)),
               bank_votes=getattr(S, "city_link_votes", None) or [],
               note="computed movement potential (routes between buildings and everyday destinations), not counts")
    os.makedirs(SELINUS_RES_DIR, exist_ok=True)
    with open(CITY_LINK_MV, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    LOG.append("city_link_movement.json: spine {} m index {}, stream-edge streets {} m: {} today -> {} with it.".format(
        out["spine_m"], None if out["spine_walk_index"] is None else round(out["spine_walk_index"]), out["edge_m"],
        None if out["edge_walk_today"] is None else round(out["edge_walk_today"]),
        None if out["edge_walk_with"] is None else round(out["edge_walk_with"])))


def mv_runs(S, R, key, F):
    """[(points, (class, value))] of map `key` along the walking (or driving) network, clipped to F."""
    pieces, IDX = R["pieces"], R["IDX"]
    if key.endswith("_d"):
        a_, b_ = IDX[key[:-2] + "_a"], IDX[key[:-2] + "_b"]
        vals = dict((i, a_.get(i, 0.0) - b_.get(i, 0.0)) for i in R["inside"])
    else:
        vals = IDX[key]
    net = ("car" if key.startswith("car") else "walk") + ("_a" if key.endswith(("_a", "_d")) else "_b")

    def val(pi):
        return (MV_CLASS.get(pieces[pi]["tags"].get("highway"), "lane"), round(vals.get(pi, 0.0), 1))
    return _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F)


def draw_mv_streets(B, V, runs, L, order, scale=1.0, div=False, dmax=1.0):
    for P, (cls, v) in sorted(runs, key=lambda r: abs(r[1][1])):
        if div:
            if abs(v) < 0.05:
                continue
            col = mv_ramp(DIV, div_t(v, dmax))
        else:
            col = mv_ramp(SEQ, seq_t(v, 100.0))
        B.line(V.P(P), col, L, order, MV_W[cls] * scale)


def stage_areas(S):
    """The working areas named by place (STAGES): [(name, short, polygon)], upstream to downstream. Read only:
    never drawn as outlines."""
    out = []
    for a in getattr(S, "study_areas", []) or []:
        ks = [k for k, nm, x, y in BRIDGES_K if pip(x, y, a["P"])]
        if a["name"] == "ARAS":
            st = STAGES[0]
        elif a["name"] == "NIL":
            st = STAGES[3]
        elif "K4" in ks:
            st = STAGES[1]
        elif "K5" in ks:
            st = STAGES[2]
        else:
            st = ("middle reach", "mid")
        out.append((st[0], st[1], a))
    order = [s[0] for s in STAGES]
    out.sort(key=lambda s: order.index(s[0]) if s[0] in order else 9)
    return out


def diagrams_engine():
    """The axonometric engine (bergama_diagrams v1.8, cut down), executed once."""
    if not _DG:
        _DG["__name__"] = "bergama_diagrams_engine"
        exec(compile(DIAG_SRC, "bergama_diagrams_engine", "exec"), _DG)    # its functions read and see _DG itself
    return _DG


_DG = {}


def diagram_ctx(S):
    """The engine's context for this site model (places, crowns, walking network), once per run: S.dg = (DG, ctx)."""
    if getattr(S, "dg", None) is not None:
        return S.dg
    DG = diagrams_engine()
    DG["CREDIT"] = CREDIT
    del DG["LOG"][:]
    dirs = []
    try:
        if doc.Path:
            d = os.path.dirname(doc.Path)
            dirs = [d, os.path.dirname(d)]
    except Exception:
        pass
    BP, pal = DG["load_palette"]([DATA_DIR] + dirs)
    ctx = DG["Ctx"](globals(), S, BP, PLACES_PATH or None, bool(ENV_PATH))
    names = dict((id(a), (nm, sh)) for nm, sh, a in stage_areas(S))
    ctx.areas = [a for a in ctx.areas if id(a) in names]
    for a in ctx.areas:
        a["_key"] = names[id(a)][0]
    ctx.areas.sort(key=lambda a: [s[0] for s in STAGES].index(a["_key"]) if a["_key"] in [s[0] for s in STAGES] else 9)
    DG["SHORT"].clear()
    DG["SHORT"].update((names[id(a)][0], names[id(a)][1]) for a in ctx.areas)
    S.dg = (DG, ctx)
    LOG.append("Axonometric engine: palette {}; {} places, {} crowns.".format(pal, len(ctx.places), len(ctx.crowns)))
    return S.dg


def stream_sky(S, step=10.0, run=60.0, gap=300.0, n_low=3):
    """v33 (Aras 07:05-07:09, Step 4): how enclosed the stream bed is, the height information that could change the
    design: the sky view of the solar-radiation grid (share of the sky vault seen past buildings, crowns in leaf and
    the terrain; sky_pass) every `step` m along the centreline inside the frame, averaged over `run` m. Returns
    dict(mean, cell, run, marks=[(x, y, sky view, "low" | "high")]): the n_low most enclosed stretches at least `gap`
    m apart and the most open one; None without the analyses."""
    if getattr(S, "_sky_bed", 0) != 0:
        return S._sky_bed
    S._sky_bed = None
    rd = (getattr(S, "env", None) or {}).get("rad")
    cl = getattr(S, "river_cl", None)
    if not rd or rd.get("svf") is None or not cl or len(cl) < 2:
        return None
    F = Frame(rd["frame"])
    nx, ny, c = rd["nx"], rd["ny"], rd["cell"]
    sv, roof = np.asarray(rd["svf"]).ravel(), np.asarray(rd["roof"]).ravel()
    pts = []
    for (ax, ay), (bx, by) in zip(cl, cl[1:]):
        k = max(1, int(math.hypot(bx - ax, by - ay) // step))
        pts += [(ax + (bx - ax) * t / k, ay + (by - ay) * t / k) for t in range(k)]
    vals = []
    for x, y in pts:
        u, v = F.local(x, y)
        i, j = int((u - F.u0) / c), int((v - F.v0) / c)
        ok = S.F.inside(x, y) and 0 <= i < nx and 0 <= j < ny and not roof[j * nx + i]
        vals.append(float(sv[j * nx + i]) if ok else None)
    w = max(1, int(round(run / step / 2)))
    sm = []
    for a in range(len(vals)):
        win = [q for q in vals[max(0, a - w):a + w + 1] if q is not None]
        sm.append(sum(win) / len(win) if vals[a] is not None and win else None)
    good = [a for a in range(len(sm)) if sm[a] is not None]
    if not good:
        return None
    marks, used = [], []
    for a in sorted(good, key=lambda a: sm[a]):
        if len(marks) >= n_low:
            break
        if all(abs(a - b) * step >= gap for b in used):
            used.append(a)
            marks.append((pts[a][0], pts[a][1], sm[a], "low"))
    hi = max(good, key=lambda a: sm[a])
    marks.append((pts[hi][0], pts[hi][1], sm[hi], "high"))
    S._sky_bed = dict(mean=sum(vals[a] for a in good) / len(good), cell=c, run=run, marks=marks)
    return S._sky_bed


def export_axonometrics(S):
    """v33 (Aras Q8; Step 4, 07:05-07:09): S1 as a parallel axonometric, one A3 vector PDF beside the board's PDFs
    (S2 has none: its walk table gives each walk's climb). Returns the paths written."""
    import datetime as _dt
    DG, ctx = diagram_ctx(S)
    stamp = _dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    out = []
    if not os.path.isdir(pdf_folder()):
        os.makedirs(pdf_folder())
    del CROP_DIRECT[:]
    for did, fn in (("S1", "Selinus_01_what_is_there_axonometric.pdf"),):
        t0 = time.time()
        ext = ctx.extents[0]
        try:
            spec = DG["SPECS"][did](ctx, ext)
            pg, st = DG["compose"](ctx, spec, ext, stamp)
            p = os.path.join(pdf_folder(), fn)
            DG["write_pdf"]([pg], p)
            out.append((p, time.time() - t0))
            bx, ph = DG["BOX"], DG["PAGE_H"]                 # v40: the booklet crop: the page between the rules (the
            bx = (0.0, bx[1], DG["PAGE_W"], bx[3])            # callouts may sit beyond the drawing box, left and right)
            leg = [(("dot", DG["TREE_STYLES"].get(c_, DG["TREE_STYLES"]["tree"])["mid"]) if k_ == "tree" else (k_, c_))
                   + (t_,) for k_, c_, t_ in spec["legend"]() if c_ is not None]
            CROP_DIRECT.append(("axo_what_is_there", fn, (bx[0], ph - bx[3] - 4.0, bx[2], ph - bx[1] + 4.0),
                                u"What is there · heights, heritage, water, green", None, crop_legend(leg), []))
        except Exception:
            LOG.append("WARNING: the {} axonometric failed:\n{}".format(did, traceback.format_exc()))
    LOG.extend(u"Axonometric engine: " + m for m in DG["LOG"])
    return out


CROP_MV = {"walk_b": "walking_today", "car_b": "driving_today", "walk_d": "walking_change", "car_d": "driving_change",
           "comb_d": "combined_change"}                  # v40: crop slugs of plan 07's insets


def draw_how_people_use_it(S, B, x, y, w, U):
    """S2: how people move and what they reach, on one plan of the frame and CONTEXT_M around it (was 07 commercial
    spines, 09 civic constellations, diagrams D3, D5, D7 and the movement script's panels). Returns the y below."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    F2 = context_frame(F)
    B.text("HOW PEOPLE USE IT · STREETS · SHOPS · SERVICES · WALKS", x, y, 1.05 * U, INK, L,
           font=FONT_TITLE, bold=True)                    # v38: keywords
    V, mw, mh = view_fit(F2, x, y - 1.2 * U, w, 10.0 * w)
    MV = movement(S)
    R = MV.get("R")
    try:
        DG, ctx = diagram_ctx(S)
        D7 = DG["d7_links"](ctx) if ctx.areas else None
    except Exception:
        LOG.append("WARNING: services and walks not drawn:\n" + traceback.format_exc())
        DG, ctx, D7 = None, None, None
    # quiet ground and context
    B.fill([V.P(F2.P)], mix(PAPER, (255, 255, 255), 0.55), L, 1)
    for key, col, wd in (("water", mix(BLUE_D, PAPER, 0.5), 0.06), ("road", mix(INK2, PAPER, 0.62), 0.04),
                         ("bld", mix(INK2, PAPER, 0.45), 0.04)):
        for a, b in (getattr(S, "ctx_lines", None) or {}).get(key, []):
            B.line([V.p(*a), V.p(*b)], col, L, 2, wd)
    mini_base(S, B, V, L, water_col=mix(CAT["water"][1], PAPER, 0.3))
    quiet = mix(INK2, PAPER, 0.72)
    use_cats = ("commercial", "mixed", "institutional", "religious")
    mini_buildings(S, B, V, L, lambda u: CAT[u["cat"]][1] if u["cat"] in use_cats else quiet, order=12)
    # commerce spines: a broad pale band under the street
    cc = CAT["commercial"][1]
    for g in S.corr_primary:
        for P in g["Ps"]:
            B.line(V.P(P), mix(cc, PAPER, 0.45), L, 9, 2.6)
    for g in S.corr_secondary:
        for P in g["Ps"]:
            for d in dashes(V.P(P), 0.6 * U, 0.35 * U):
                B.line(d, mix(cc, PAPER, 0.45), L, 9, 1.6)
    # streets: line width = OSM class, colour = combined movement potential today
    if R:
        draw_mv_streets(B, V, mv_runs(S, R, "comb_b", F), L, 14)
    else:
        road_lines(S, B, V, L, 14, casing=mix(INK, PAPER, 0.55), surface=(255, 255, 255))
    # v34: the proposed riverside spine (wired curves or bergama_city_link) and its stops, over the streets
    sp_c = mix(cc, INK, 0.35)
    sp_props = [P for k_, P, c_ in (MV.get("props") or []) if k_ in ("spine", "spine_car")]
    for P in sp_props:
        for run in F2.clip_line(P):
            B.line(V.P(run), (255, 255, 255), L, 20, 2.2)
            B.line(V.P(run), sp_c, L, 21, 1.3)
    for ax, ay in (MV.get("attr") or []):
        if F2.inside(ax, ay):
            px, py = V.p(ax, ay)
            B.fill([circle_pts(px, py, 0.2 * U, 12)], sp_c, L, 22)
    # civic constellations
    hc = mix(CAT["institutional"][1], INK, 0.2)
    for cl in S.clusters:
        for run in F.clip_line(cl["P"] + [cl["P"][0]]):
            for d in dashes(V.P(run), 0.4 * U, 0.28 * U):
                B.line(d, hc, L, 16, 0.25)
    # services (Overture places, as D5) and the walks to the nearest of each function (as D7)
    fcol = dict((f, hexrgb(c)) for f, let, c, lab in WALK_FUN)
    n_pl = {}
    if ctx is not None:
        for px_, py_, f, nm, conf, cat in [p[:6] for p in ctx.places]:
            if F.inside(px_, py_):
                n_pl[f] = n_pl.get(f, 0) + 1
                cx, cy = V.p(px_, py_)
                B.fill([circle_pts(cx, cy, 0.11 * U, 8)], fcol.get(f, INK2), L, 30)
    walk_c = mix(INK, PAPER, 0.15)
    dest = {}
    if D7:
        for k, best in D7["res"].items():
            for f, r in best.items():
                if r["pts"]:
                    for run in F2.clip_line(r["pts"]):
                        for d in dashes(V.P(run), 0.12 * U, 0.12 * U):
                            B.line(d, walk_c, L, 32, 0.22)
                dest[(f, round(r["x"]), round(r["y"]))] = r
        rr = 0.38 * U
        let_of = dict((f, let) for f, let, c, lab in WALK_FUN)
        for (f, _, _), r in dest.items():
            if F2.inside(r["x"], r["y"]):
                px, py = V.p(r["x"], r["y"])
                roundel(B, px, py, rr, let_of.get(f, "?"), fcol.get(f, INK), (255, 255, 255), L, order=62)
        for nm, sh, a in stage_areas(S):                    # where each walk starts: a name, never an outline
            cx, cy = shoelace(a["P"])[1:]
            px, py = V.p(cx, cy)                          # v40: plain text, no white box (Aras 25 Oct 21:41)
            B.text(nm, px, py, 0.42 * U, INK, L, order=64, font=FONT_TITLE, bold=True, align="C")
    draw_map_annotations(S, B, V, U)
    B.line(V.P(F.P + [F.P[0]]), INK, L, 26, 0.25)
    draw_north_small(B, V, mw, mh, U, L, size=0.7)
    mb = y - 1.2 * U - mh
    draw_scalebar(B, V.X0, mb - 1.4 * U, V.s, nice_floor(F2.w / 8.0), U, L, h=0.32)
    yy = mb - 2.8 * U
    # insets: walking and driving today, only the key streets in colour and named (v44, Aras 27 Oct: "highlight only
    # the key axes and roads"); the change maps are gone from the sheet (the proposal map shows the masterplan's)
    if R:
        keys = [("walk_b", "WALKING TODAY", u"Walking today · the {} busiest named streets"),
                ("car_b", "DRIVING TODAY", u"Driving today · the {} busiest named roads")]
        n = 2
        g = 1.2 * U
        iw = (mw - (n - 1) * g) / n
        low = yy
        for j, (k, title, cap) in enumerate(keys):
            ix = V.X0 + (j % n) * (iw + g)
            iy = yy
            B.text(title, ix, iy, 0.5 * U, INK, L, font=FONT_TITLE, bold=True)
            Vi, iw_, ih_ = view_fit(F, ix, iy - 0.8 * U, iw, 10.0 * iw)
            mini_base(S, B, Vi, L, water_col=mix(CAT["water"][1], PAPER, 0.3))
            mini_buildings(S, B, Vi, L, lambda u: quiet, order=12)
            s_i = bk_s(iw, ih_ * 1.15, crop_scale(Vi.s), share=0.5)    # two side by side on the booklet page
            bnd = (ix, iy - 0.8 * U - ih_, ix + iw, iy - 0.8 * U)
            names_, key_ = draw_mv_key(S, B, Vi, R, MV, k, F, L, bk_h(8.0, s_i), bnd)
            B.line(Vi.P(F.P + [F.P[0]]), INK2, L, 26, 0.1)
            kb = draw_label_key(B, key_, ix, bnd[1] - 0.3 * U, iw, bk_h(7.5, s_i), L) if key_ else bnd[1]
            crop_panel(CROP_MV.get(k, k), ix, kb - 0.2 * U, ix + iw, iy - 0.8 * U,
                       cap.format(len(names_)), crop_scale(Vi.s))     # v40: the booklet crop of the inset
            low = min(low, kb - 0.4 * U)
        yy = low - 0.6 * U
    # walking lengths from each working area (D7), as a small table
    if D7:
        st = [(nm, sh) for nm, sh, a in stage_areas(S) if nm in D7["res"]]
        cw0, cw = 9.0 * U, (mw - 9.0 * U) / max(1, len(st))
        h = 0.36 * U
        r_walk = bcite("Commerce: shopfronts within 30 m of a street (survey, OSM, Overture). Services: Overture/Meta "
                       "places. Walks: the shortest along OSM streets and footways from the edge of each working area, "
                       "rounded to 10 m.")
        B.text("WALK TO THE NEAREST · m along OSM streets and footways " + r_walk, V.X0, yy, 0.42 * U, INK, L,
               font=FONT_TITLE, bold=True)
        yy -= 1.0 * U
        for j, (nm, sh) in enumerate(st):
            B.text("from the " + nm, V.X0 + cw0 + j * cw, yy, h, INK2, L, bold=True)
        yy -= 0.85 * U
        # v33 (Step 4): the climb of every walk on the survey terrain, instead of an axonometric of S2
        walks = [D7["res"].get(nm, {}).get(f) for f, let, c, lab in WALK_FUN for nm, sh in st]
        lines_ = [r["pts"] if r and r["pts"] and not r["inside"] else [] for r in walks]
        ups = DG["walk_climbs"](ctx, lines_ + [p["pts"] for p in D7["pairs"]])
        climb = dict((id(r), u_) for r, u_ in zip(walks, ups) if r)
        for f, let, c, lab in WALK_FUN:
            roundel(B, V.X0 + 0.3 * U, yy + 0.15 * U, 0.3 * U, let, fcol[f], (255, 255, 255), L, order=62)
            B.text(lab, V.X0 + 0.9 * U, yy, h, INK, L)
            for j, (nm, sh) in enumerate(st):
                r = D7["res"].get(nm, {}).get(f)
                up = climb.get(id(r)) if r else None
                t_ = "none in reach" if not r else ("inside" if r["inside"] else DG["m10"](r["L"]) + (
                    ", {} m up".format(up) if up and up >= 5 else ""))
                B.text(t_, V.X0 + cw0 + j * cw, yy, h, INK, L)
            yy -= 0.75 * U
        ups = [u_ for u_, ln in zip(ups, lines_ + [p["pts"] for p in D7["pairs"]]) if u_ is not None and ln]
        yy -= 0.4 * U
    # legend (v38: short names; the method sentences are entries of the Sources key, cited [n])
    r_mv = bcite("Movement potential = the number of shortest routes between every building and every everyday "
                 "destination within {:.0f} m on foot or {:.0f} min by car that use the street (OSM network, Overture "
                 "places, the method of bergama_movement v1); index 100 = the busiest street piece in the frame. A count "
                 "of routes, not of people or vehicles: no count exists for these streets.".format(
                     MV_OPT["r_walk"], MV_OPT["t_car"] / 60.0)) if R else ""
    r_com = bcite("Commerce: shopfronts within 30 m of a street (survey, OSM, Overture). Services: Overture/Meta "
                  "places. Walks: the shortest along OSM streets and footways from the edge of each working area, "
                  "rounded to 10 m.")
    r_sp = bcite("Proposed streamside spine: {}; the city link figures add it to the walking network (joined to every street it "
                 "crosses) and its stops as new destinations. Walking cost follows the slope (Tobler 1993) on the survey "
                 "terrain.".format(getattr(S, "city_link", None) and S.city_link["src"] or "curves wired into the board")
                 ) if sp_props else ""
    leg = [("hdr", None, "STREETS · COLOUR = MOVEMENT POTENTIAL · WIDTH = OSM CLASS " + r_mv)]
    if R:
        for v in (2, 10, 25, 50, 100):
            leg.append(("thick", mv_ramp(SEQ, seq_t(v, 100.0)), "Index {}".format(v)))
    leg += [("hdr", None, "SHOPS AND CIVIC LIFE " + r_com),
            ("thick", mix(cc, PAPER, 0.45), "Primary commercial spine"),
            ("dash", mix(cc, PAPER, 0.45), "Secondary spine")]
    if sp_props:                                          # v34
        leg += [("thick", sp_c, "Proposed streamside spine " + r_sp), ("dot", sp_c, "New stop on the spine")]
    leg += [("box", CAT["commercial"][1], "Commerce"), ("box", CAT["mixed"][1], "Mixed use"),
            ("box", CAT["institutional"][1], "Civic"), ("box", CAT["religious"][1], "Sacred"),
            ("dash", hc, "Constellation · 3+ in 100 m")]
    if ctx is not None:
        leg += [("hdr", None, "SERVICES AND WALKS " + r_com)]
        for f, let, c, lab in WALK_FUN:
            if n_pl.get(f):
                leg.append(("dot", fcol[f], "{} · {} places".format(lab, n_pl[f])))
        leg.append(("dash", walk_c, "Walk to the nearest (letter at the place)"))
    ly = draw_legend_items(B, leg, x, yy - 0.4 * U, mw, U, L, h=0.4)
    crop_panel("movement", V.X0, mb - 1.6 * U, V.X0 + mw, y - 1.2 * U, u"How people use it · streets, shops, services",
               crop_scale(V.s), crop_legend(leg))         # v40: the booklet crop of the plan
    # v38 (visual first): what the numbers say as a tile and two mini-charts (were caption sentences); computed above,
    # nothing measured on the street
    cy0 = ly - 0.4 * U
    low = cy0
    cx = x
    gw, gh = min(30.0 * U, (mw - 4.0 * U) / 3.0), 7.0 * U
    tfill = mix(PAPER, (255, 255, 255), 0.5)
    if R and MV.get("rows"):
        top = MV["rows"][0]
        low = min(low, vis_tiles(B, cx, cy0, gw, [
            ("road", "BUSIEST STREET · WALK + DRIVE", "{} · index {:.0f}".format(top["name"], top["comb_b"]), r_mv)],
            U, L, h=1.3, ink=INK, grey=INK2, fill=tfill, rule=FAINT))
        cx += gw + 2.0 * U
        rw = MV["rho"].get("walk_b")
        big = [r_ for r_ in (MV.get("big") or []) if r_.get("walk_b") is not None]
        if rw is not None and big:                        # scatter: shops per street against walking potential
            B.text("SHOPS vs WALKING POTENTIAL · Spearman {:.2f} {}".format(rw, r_com), cx, cy0 - 0.4 * U, 0.4 * U,
                   INK, L, font=FONT_TITLE, bold=True)
            px0, py0 = cx + 1.4 * U, cy0 - 1.0 * U - gh
            pw_ = gw - 1.4 * U
            xm = max(100.0, max(r_["walk_b"] for r_ in big))
            ym = max(1.0, max(r_["shops"] for r_ in big))
            B.fill([rect(px0, py0, px0 + pw_, py0 + gh)], tfill, L, 20)
            B.line(rect(px0, py0, px0 + pw_, py0 + gh) + [(px0, py0)], FAINT, L, 21, 0.04)
            for r_ in big:
                B.fill([circle_pts(px0 + pw_ * r_["walk_b"] / xm, py0 + gh * r_["shops"] / ym, 0.12 * U, 8)],
                       mix(CAT["commercial"][1], INK, 0.2), L, 22)
            B.text("0", px0, py0 - 0.45 * U, 0.28 * U, INK2, L, align="C")
            B.text("{:.0f}".format(xm), px0 + pw_, py0 - 0.45 * U, 0.28 * U, INK2, L, align="C")
            B.text("{:.0f}".format(ym), px0 - 0.2 * U, py0 + gh - 0.28 * U, 0.28 * U, INK2, L, align="R")
            B.text("walking index · {} streets of 50 m+".format(len(MV["big"])), px0 + pw_ / 2.0, py0 - 0.95 * U,
                   0.28 * U, INK2, L, align="C")
            B.text("shops", px0 - 0.2 * U, py0 + 0.1 * U, 0.28 * U, INK2, L, align="R")
            crop_panel("shops_vs_walking", cx - 0.6 * U, py0 - 1.3 * U, cx + gw, py0 + gh + 0.1 * U,
                       u"More walkers, more shops · Spearman {:.2f}".format(rw))    # v40
            low = min(low, py0 - 1.4 * U)
            cx += gw + 2.0 * U
    if D7 and ups:                                        # the climb of every walk, as bars
        mx = max(ups)
        r_cl = bcite("Climb on the survey terrain: rises summed every {:.0f} m, rounded to 5 m; calculated. The table "
                     "carries the heights that matter for these walks, so S2 has no axonometric.".format(DG["CLIMB_STEP"]))
        B.text("CLIMB OF THE WALKS · " + ("none 5 m or more" if mx < 5 else "most {} m up".format(mx)) + " " + r_cl,
               cx, cy0 - 0.4 * U, 0.4 * U, INK, L, font=FONT_TITLE, bold=True)
        vv = sorted(ups, reverse=True)
        bx0, by0 = cx + 1.4 * U, cy0 - 1.0 * U - gh
        bw_ = (gw - 1.4 * U) / float(len(vv))
        ym = max(5.0, float(mx))
        for i, u_ in enumerate(vv):
            B.fill([rect(bx0 + i * bw_ + 0.1 * bw_, by0, bx0 + (i + 0.9) * bw_, by0 + gh * u_ / ym)],
                   INK2 if u_ >= 5 else FAINT, L, 21)
        for dd in dashes([(bx0, by0 + gh * 5.0 / ym), (bx0 + gw - 1.4 * U, by0 + gh * 5.0 / ym)], 0.3 * U, 0.2 * U):
            B.line(dd, MARK_C, L, 22, 0.06)
        B.text("5 m", bx0 - 0.2 * U, by0 + gh * 5.0 / ym - 0.12 * U, 0.28 * U, MARK_C, L, align="R")
        B.line([(bx0, by0), (bx0 + gw - 1.4 * U, by0)], INK2, L, 22, 0.05)
        B.text("walks, steepest first · m up", bx0 + (gw - 1.4 * U) / 2.0, by0 - 0.55 * U, 0.28 * U, INK2, L, align="C")
        crop_panel("walk_climb", cx, by0 - 0.9 * U, cx + gw, by0 + gh + 0.1 * U, u"Climb of the walks")     # v40
        low = min(low, by0 - 1.0 * U)
    return low - 0.4 * U


# ============================================================ v33 AXONOMETRIC ENGINE (bergama_diagrams v1.8, cut down)
#@include ../data/DIAG_SRC.py


CROP_DEFAULT = {"The stream's tree cover": ("tree_cover", u"Tree cover along the banks, every 25 m", "riparian"),
                "Section along the spine": ("spine", u"Long section along the spine", "spine_section")}
# v40: drawings cropped whole below their title when they register no crop themselves (and every section)


def build_sheet(S, B, X, Y, U, rects):
    F = S.F
    del BOARD_KEY[:]                                   # v38: the drawings' numbered sources start at [1] on every run
    gap, pad, maxw = 6.0 * U, 1.6 * U, 150.0 * U
    # v33: one plan for what is there (was 01, 05, 06, 08, 10 and the fabric_green map), its tables beside it
    SA = getattr(S, "whole", None) or S                  # v36: plan 01 over the whole file
    if SA is not S:
        SA.sec_lines, SA.sections = S.sec_lines, S.sections
    w01 = 120.0 * U * (SA.F.w / context_frame(F).w if SA is not S else 1.0)    # v36: same print scale as the site
    items = [("01 What is there", w01, lambda x, y: draw_what_is_there(SA, B, x, y, w01, U)),
             ("02 Land-use legend", 30.8 * U, lambda x, y: draw_legend(S, B, x, y, 30.8 * U, U)),
             ("03 Distribution", 12.4 * U, lambda x, y: draw_distribution(S, B, x, y, U)),
             ("04 Green, farmland and orchards", 30.8 * U, lambda x, y: draw_green_table(S, B, x, y, 30.8 * U, U)),
             ("05 Readings", 24.0 * U, lambda x, y: draw_readings(S, B, x, y, 24.0 * U, None, U)),
             ("06 The stream's tree cover", 120.0 * U, lambda x, y: draw_riparian(S, B, x, y, 120.0 * U, U)),
             ("06b What meets the water", 120.0 * U, lambda x, y: draw_stream_edge_plan(S, B, x, y, 120.0 * U, U)),
             ("07 How people use it", 120.0 * U, lambda x, y: draw_how_people_use_it(S, B, x, y, 120.0 * U, U)),
             ("07b Commercial spines", 120.0 * U, lambda x, y: draw_commercial_spines(S, B, x, y, 120.0 * U, U)),
             ("07d City heritage loop", 40.0 * U, lambda x, y: draw_heritage_loop(S, B, x, y, 40.0 * U, U)),
             ("11b Section key", 30.8 * U, lambda x, y: draw_section_key(B, x, y, 30.8 * U, U)),
             ("11c Building types in the sections", 61.4 * U, lambda x, y: draw_typology_key(S, B, x, y, 61.4 * U, U)),
             ("11 Key question", 30.8 * U, lambda x, y: draw_key_question(S, B, x, y, 30.8 * U, U, cols=1))]
    # v44: the masterplan's proposal map (only when masterplan_results.json holds "movement") and the walking-effort
    # proof (only with terrain heights on the network); each logs why when it is left out
    at = [nm_ for nm_, w_, f_ in items].index("07d City heritage loop")
    R_ = movement(S).get("R")
    if R_ and getattr(R_["pieces"], "z", None):
        items.insert(at + 1, ("07e Walking effort", 120.0 * U,
                              lambda x, y: draw_walking_effort(S, B, x, y, 120.0 * U, U)))
    M_ = mp_movement()
    if M_ is not None:
        items.insert(at, ("07c The proposal, how people move", 120.0 * U,
                          lambda x, y: draw_mv_proposal(S, B, x, y, 120.0 * U, U, M_)))
    n_ = 13
    if S.sections:
        # v42 (Aras 26 Oct 07:06, p.09-11): every cut at ONE round scale, rows of whole cuts, at most two booklet pages
        sw = 140.0 * U
        plan_ = sections_plan(S, sw, U)
        for k_, pg_ in enumerate(plan_[2]):
            nms = [c_["name"] for r_ in pg_ for c_, w_ in r_ if not c_.get("_types")]
            items.append(("{:02d} Sections across the stream {}".format(12 + k_, nms[0] + (
                "" if len(nms) == 1 else "-" + nms[-1])), sw,
                (lambda k2: (lambda x, y: draw_sections_page(S, B, x, y, sw, U, plan_, k2)))(k_)))
        n_ = 12 + len(plan_[2])
    else:                                                 # v44: no placeholder on the sheet, the log says why
        LOG.append("Sections: the survey has no section lines (layer sec_lines), so no cuts are drawn.")
    if spine_section(S) is not None:                     # v40: the long section along the streamside spine
        items.append(("{:02d} Section along the spine".format(n_), 140.0 * U,
                      lambda x, y: draw_spine_section(S, B, x, y, 140.0 * U, U)))
        n_ += 1
    items.append(("{:02d} Sources".format(n_), 94.8 * U,
                  lambda x, y: draw_footer(S, B, x, y, 94.8 * U, U, h=0.3)))
    B.begin("DRAWINGS · sheet title", "LU_DRAWINGS")
    B.text("SEPARATE DRAWINGS · grouped · framed with a cutting margin", X, Y + 2.2 * U, 0.9 * U, INK,
           "LU_BOARD::Crop frames", font=FONT_TITLE, bold=True)
    x, y, row_bottom = X, Y - 2.0 * U, Y - 2.0 * U
    for name, w, fn in items:
        if x > X and x + w > X + maxw:
            x, y = X, row_bottom - gap
            row_bottom = y
        B.begin("DRAWING · " + name, "LU_DRAWINGS")
        n0 = len(CROP_PANELS)
        bot = fn(x, y)
        box = (x - pad, bot - pad, x + w + pad, y + 1.4 * U + pad)
        dc = CROP_DEFAULT.get(name.split(" ", 1)[-1])
        if dc or (" Section " in name and "key" not in name.lower() and "placeholder" not in name.lower()):   # v40
            crop_default(name, x, bot, x + w, y - 0.45 * U, n0, *(dc or ()))
        B.line(rect(box[0], box[1], box[2], box[3]) + [(box[0], box[1])], INK2, "LU_BOARD::Crop frames", 50, 0.05)
        B.text(name.upper(), box[0], box[3] + 0.35 * U, 0.4 * U, INK2, "LU_BOARD::Crop frames")
        rects.append((name, box))
        row_bottom = min(row_bottom, box[1])
        x = box[2] + gap
    return row_bottom


# ============================================================ SEPARATE DRAWINGS (margins for cutting)
class TimedRects(list):
    """v27: the list of drawings, recording how long each one took (from the previous drawing, or from the start of the
    layout for the first) in DRAWING_TIMES."""

    def __init__(self):
        list.__init__(self)
        self.t = __import__("time").time()

    def append(self, item):
        now = __import__("time").time()
        try:
            DRAWING_TIMES.append((str(item[0]), now - self.t))
        except Exception:
            pass
        self.t = now
        list.append(self, item)


def build_layout(S):
    global MMU
    B = Board()
    F = S.F
    U = max(F.w / 61.4, F.h / 24.0)
    S.U = U
    MMU = SHEET_MM / (PW * U)
    OX, OY = 0.0, 0.0
    rects = TimedRects()                                  # v27: each drawing's time for the log
    del DRAWING_TIMES[:]
    del CROP_PANELS[:]                                    # v40: the booklet crops of this layout
    y = OY
    B_CUR[0] = B
    if RUN_MODE in ("board", "all"):
        y = build_sheet(S, B, OX, y, U, rects) - 14.0 * U          # v33: separate drawings only
    if RUN_MODE in ("technical", "all"):
        build_technical(S, B, OX, y, U, rects)
    return B, rects


# ============================================================ FRAMES
def min_area_rect(pts):
    H = hull(pts)
    if len(H) < 3:
        return None
    best = None
    for i in range(len(H)):
        a, b = H[i], H[(i + 1) % len(H)]
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        c, s = math.cos(-ang), math.sin(-ang)
        us = [c * p[0] - s * p[1] for p in H]
        vs = [s * p[0] + c * p[1] for p in H]
        area = (max(us) - min(us)) * (max(vs) - min(vs))
        if best is None or area < best[0]:
            best = (area, ang, min(us), max(us), min(vs), max(vs))
    return best


def frame_from_survey(R, margin=15.0):
    """The whole survey in the file: tightest rotated rectangle around buildings and stream banks."""
    pts = []
    for lay in list(DWG["bld"]) + DWG["banks"]:
        for s in R["lines"].get(lay, []):
            pts.append((s[0], s[1]))
            pts.append((s[2], s[3]))
    if len(pts) < 3:
        for lst in R["lines"].values():
            for s in lst:
                pts.append((s[0], s[1]))
                pts.append((s[2], s[3]))
    if len(pts) < 3:
        raise Exception("The file holds no survey line work to build a frame from.")
    _, ang, u0, u1, v0, v1 = min_area_rect(pts)
    u0, u1, v0, v1 = u0 - margin, u1 + margin, v0 - margin, v1 + margin
    c, s = math.cos(ang), math.sin(ang)
    W = lambda u, v: (c * u - s * v, s * u + c * v)
    return Frame([W(u0, v0), W(u1, v0), W(u1, v1), W(u0, v1)])


# ============================================================ BAKE (Rhino) - styled vectors, one group per drawing
def _crv(P, closed=False):
    pl = rg.Polyline()
    for x, y in P:
        if pl.Count and abs(pl[pl.Count - 1].X - x) < 1e-7 and abs(pl[pl.Count - 1].Y - y) < 1e-7:
            continue
        pl.Add(x, y, 0.0)
    if closed and pl.Count > 2 and pl[0].DistanceTo(pl[pl.Count - 1]) > 1e-9:
        pl.Add(pl[0])
    return pl.ToPolylineCurve() if pl.Count >= 2 else None


def ensure_layer(path):
    idx = doc.Layers.FindByFullPath(path, -1)
    if idx >= 0:
        return idx
    parent_id = System.Guid.Empty
    cur = ""
    for i, part in enumerate(path.split("::")):
        cur = part if i == 0 else cur + "::" + part
        idx = doc.Layers.FindByFullPath(cur, -1)
        if idx < 0:
            lay = Rhino.DocObjects.Layer()
            lay.Name = part
            lay.Color = sd.Color.FromArgb(*INK)
            if i > 0:
                lay.ParentLayerId = parent_id
            idx = doc.Layers.Add(lay)
        parent_id = doc.Layers[idx].Id
    return idx


SEAM_TAG = ("selinus_seam", "1")         # every object this script bakes carries it; purge removes only those


def purge(roots):
    """Delete what this script baked under the layer trees `roots` (objects carrying its tag), also on hidden or
    locked layers; the user's own objects on these layers stay. A tree this version has not baked into before is
    cleared the old way once (every object on it), so the untagged objects of earlier versions do not stay
    behind. Returns (deleted, failed)."""
    idx = {}
    for lay in list(doc.Layers):
        try:
            if lay.IsDeleted:
                continue
            for root in roots:
                if lay.FullPath == root or lay.FullPath.startswith(root + "::"):
                    idx[lay.Index] = root
        except Exception:
            pass
    legacy = set(r for r in roots if doc.Strings.GetValue("selinus_seam_tagged", r) != "1")
    done = failed = 0
    if idx:
        es = Rhino.DocObjects.ObjectEnumeratorSettings()
        es.HiddenObjects = True
        es.LockedObjects = True
        es.NormalObjects = True
        es.IncludeLights = False
        es.IncludeGrips = False
        for o in list(doc.Objects.GetObjectList(es)):
            try:
                root = idx.get(o.Attributes.LayerIndex)
                if root is None:
                    continue
                if root not in legacy and o.Attributes.GetUserString(SEAM_TAG[0]) != SEAM_TAG[1]:
                    continue
                if doc.Objects.Delete(o, True, True):
                    done += 1
                else:
                    failed += 1
            except Exception:
                failed += 1
    for r in roots:
        doc.Strings.SetString("selinus_seam_tagged", r, "1")
    return done, failed


def make_attrs(li, color, order, weight=None, gi=-1):
    a = Rhino.DocObjects.ObjectAttributes()
    a.LayerIndex = li
    a.ColorSource = Rhino.DocObjects.ObjectColorSource.ColorFromObject
    a.ObjectColor = sd.Color.FromArgb(*color)
    try:
        a.PlotColorSource = Rhino.DocObjects.ObjectPlotColorSource.PlotColorFromDisplay
    except Exception:
        pass
    if weight is not None:
        a.PlotWeightSource = Rhino.DocObjects.ObjectPlotWeightSource.PlotWeightFromObject
        a.PlotWeight = float(weight)
    try:
        a.DisplayOrder = int(order)
    except Exception:
        pass
    if gi >= 0:
        a.AddToGroup(gi)
    a.SetUserString(SEAM_TAG[0], SEAM_TAG[1])
    return a


def bake_text(txt, pt, h, a, font, bold, align, ang, italic):
    pl = rg.Plane(pt, rg.Vector3d(math.cos(ang), math.sin(ang), 0.0), rg.Vector3d(-math.sin(ang), math.cos(ang), 0.0))
    J = {"L": rg.TextJustification.BottomLeft, "C": rg.TextJustification.BottomCenter,
         "R": rg.TextJustification.BottomRight, "MC": rg.TextJustification.MiddleCenter}
    try:
        g = doc.Objects.AddText(txt, pl, h, font, bold, italic, J.get(align, J["L"]), a)
        if g != System.Guid.Empty:
            return g
    except Exception:
        pass
    try:
        te = rg.TextEntity.Create(txt, pl, doc.DimStyles.Current, False, 0.0, 0.0)
        te.TextHeight = h
        te.Justification = J.get(align, J["L"])
        g = doc.Objects.AddText(te, a)
        if g != System.Guid.Empty:
            return g
    except Exception:
        pass
    BAKE_NOTES["dots"] = BAKE_NOTES.get("dots", 0) + 1
    return doc.Objects.AddTextDot(txt, pt, a)


def repair_hatch(curves, solid):
    """A fill Rhino refused: clean the curves and retry, then split them into boolean regions."""
    try:
        fixed = List[rg.Curve]()
        for c in curves:
            d = c.DuplicateCurve()
            try:
                d.RemoveShortSegments(TOL * 5.0)
            except Exception:
                pass
            if not d.IsClosed:
                d.MakeClosed(TOL * 50.0)
            fixed.Add(d)
        hs = rg.Hatch.Create(fixed, solid, 0.0, 1.0, TOL * 5.0)
        if hs:
            return list(hs)
        out = []
        reg = rg.Curve.CreateBooleanRegions(fixed, rg.Plane.WorldXY, True, TOL * 5.0)
        if reg is not None:
            for i in range(reg.RegionCount):
                hs = rg.Hatch.Create(reg.RegionCurves(i), solid, 0.0, 1.0, TOL * 5.0)
                if hs:
                    out += list(hs)
        return out
    except Exception:
        return []


BAKE_NOTES = {}


def baked_copy(path):
    """The picture as baked: a copy named after its content (folder "baked" beside it), so Rhino, which keeps
    embedded pictures by file name, never shows an older one; older copies of the same picture are removed."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        d, base = os.path.split(path)
        stem = base[:-4] if base.lower().endswith(".png") else base
        bd = os.path.join(d, "baked")
        if not os.path.isdir(bd):
            os.makedirs(bd)
        name = "%s_%s.png" % (stem, _hashlib.sha1(data).hexdigest()[:10])
        out = os.path.join(bd, name)
        if not os.path.exists(out):
            with open(out, "wb") as f:
                f.write(data)
        for nm in os.listdir(bd):
            if nm != name and nm.startswith(stem + "_") and nm.endswith(".png") and len(nm) == len(stem) + 15:
                try:
                    os.remove(os.path.join(bd, nm))
                except Exception:
                    pass
        return out
    except Exception:
        return path


def bake_roots():
    """The layer trees this run rebuilds (a technical run leaves the land-use pages and drawings alone)."""
    if RUN_MODE == "technical":
        return ("LU_TECH",)
    if RUN_MODE == "board":
        return ("LU_BOARD", "LU_PAGES", "LU_DRAWINGS", "LU_ENV")
    return ("LU_BOARD", "LU_PAGES", "LU_DRAWINGS", "LU_ENV", "LU_TECH")


def picture_holes(items):
    """Pictures sit a hair below the drawing plane, so in a shaded view any fill drawn at the plane over the same place
    hides them: a background fill (one ring, drawn before the picture) gets a hole where every picture over it lies."""
    imgs = [(it[2], it[4]) for it in items if it[0] == "image"]
    out = {}
    if not imgs:
        return out
    amin = min((r[2] - r[0]) * (r[3] - r[1]) for r, o in imgs)
    for it in items:
        if it[0] != "fill" or len(it[1]) != 1:
            continue
        P = it[1][0]
        xs = [p[0] for p in P]
        ys = [p[1] for p in P]
        bb = (min(xs), min(ys), max(xs), max(ys))
        if (bb[2] - bb[0]) * (bb[3] - bb[1]) < amin:
            continue
        hs = []
        for (x0, y0, x1, y1), order in imgs:
            if order > it[4] and bb[0] < x0 and bb[1] < y0 and x1 < bb[2] and y1 < bb[3] and \
                    all(pip(qx, qy, P) for qx, qy in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))):
                hs.append(rect(x0, y0, x1, y1))
        if hs:
            out[id(it)] = hs
    return out


_RENDERED = []


def rendered_mode():
    """Rhino's Rendered display mode, found once (pictures display with it in every viewport, as the Picture command
    sets them)."""
    if not _RENDERED:
        dm = None
        try:
            for m in Rhino.Display.DisplayModeDescription.GetDisplayModes():
                if (m.EnglishName or "").strip().lower() == "rendered":
                    dm = m
                    break
        except Exception:
            dm = None
        _RENDERED.append(dm)
    return _RENDERED[0]


_LINE_PAT = []


def line_pattern():
    """v16.5: index of the hatch pattern "SELINUS lines" (one family of parallel lines 1 unit apart), made once in the
    file; -1 when this Rhino cannot make it (the hatch is then baked as plain lines)."""
    if _LINE_PAT:
        return _LINE_PAT[0]
    idx = -1
    try:
        hp = doc.HatchPatterns.FindName("SELINUS lines")
        if hp is not None:
            idx = hp.Index
        else:
            hp = Rhino.DocObjects.HatchPattern()
            hp.Name = "SELINUS lines"
            hp.FillType = Rhino.DocObjects.HatchPatternFillType.Lines
            hl = Rhino.DocObjects.HatchLine()
            hl.Angle = 0.0
            hl.BasePoint = rg.Point2d(0.0, 0.0)
            hl.Offset = rg.Vector2d(0.0, 1.0)
            hp.AddHatchLine(hl)
            idx = doc.HatchPatterns.Add(hp)
    except Exception:
        idx = -1
    _LINE_PAT.append(idx)
    return idx


def bake_hatch(it, li, gi, tech):
    """A hatch item: one Rhino hatch of the pattern "SELINUS lines" (scale = spacing, rotated to its angle) over the
    area; where Rhino refuses it, the same lines as curves. Returns the number of objects baked."""
    _, polys, col, layer, order, spacing, ang, w, _g = it
    a = make_attrs(li, col, order, w, gi)
    n = 0
    pat = line_pattern()
    if pat >= 0:
        lst = List[rg.Curve]()
        for P in polys:
            c = _crv(P, True)
            if c is not None:
                lst.Add(c)
        try:
            hs = rg.Hatch.Create(lst, pat, ang, spacing, TOL)
        except Exception:
            hs = None
        if hs:
            for h in hs:
                gid = doc.Objects.AddHatch(h, a)
                n += 1
                if tech:
                    TECH_IDS.append(gid)
            return n
    for seg in hatch_segments(polys, spacing, ang):
        c = _crv(seg)
        if c is not None:
            gid = doc.Objects.AddCurve(c, a)
            n += 1
            if tech:
                TECH_IDS.append(gid)
    return n


def bake(B):
    BAKE_NOTES.clear()
    if not B.items:
        LOG.append("WARNING: nothing to bake: what an earlier press baked was left as it was.")
        return 0
    hp = doc.HatchPatterns.FindName("Solid")
    solid = hp.Index if hp is not None else -1
    if solid < 0:                                     # a file from DWG may have no solid pattern: add Rhino's own
        try:
            solid = doc.HatchPatterns.Add(Rhino.DocObjects.HatchPattern.Defaults.Solid)
        except Exception:
            solid = -1
        if solid < 0:
            solid = 0
            LOG.append("WARNING: no solid hatch pattern in this file; fills use the file's first pattern.")
    gone, stuck = purge(bake_roots())
    if stuck:
        LOG.append("WARNING: {} objects of the previous bake could not be deleted (locked or in a block?); the new "
                   "bake sits on top of them.".format(stuck))
    del TECH_IDS[:]
    holes = picture_holes(B.items)
    lcache, gcache = {}, {}
    count = failed = 0
    refused = []
    doc.Views.RedrawEnabled = False
    try:
        for it in B.items:
            try:
                kind = it[0]
                layer = it[5] if kind == "text" else it[3]
                tech = layer.startswith("LU_TECH")
                group = it[-1]
                if layer not in lcache:
                    lcache[layer] = ensure_layer(layer)
                gi = -1
                if group:
                    if group not in gcache:
                        g = doc.Groups.Find(group)
                        gcache[group] = g if g >= 0 else doc.Groups.Add(group)
                    gi = gcache[group]
                if kind == "fill":
                    lst = List[rg.Curve]()
                    for P in list(it[1]) + holes.get(id(it), []):
                        c = _crv(P, True)
                        if c is not None:
                            lst.Add(c)
                    hs = rg.Hatch.Create(lst, solid, 0.0, 1.0, TOL)
                    if not hs:
                        hs = repair_hatch(lst, solid)
                        if not hs:
                            refused.append(layer)
                    if hs:
                        a = make_attrs(lcache[layer], it[2], it[4], None, gi)
                        for h in hs:
                            gid = doc.Objects.AddHatch(h, a)
                            count += 1
                            if tech:
                                TECH_IDS.append(gid)
                elif kind == "hatch":
                    count += bake_hatch(it, lcache[layer], gi, tech)
                elif kind == "line":
                    c = _crv(it[1])
                    if c is not None:
                        gid = doc.Objects.AddCurve(c, make_attrs(lcache[layer], it[2], it[4], it[5], gi))
                        count += 1
                        if tech:
                            TECH_IDS.append(gid)
                elif kind == "image":
                    _, path, (x0, y0, x1, y1), _, order = it[:5]
                    path = baked_copy(path)
                    # a hair below the drawing plane, so the lines, fills and text drawn over a map or section picture
                    # stay in front in Shaded and Rendered views whatever the display order does
                    pl = rg.Plane(rg.Point3d(x0, y0, -0.5), rg.Vector3d.XAxis, rg.Vector3d.YAxis)
                    gid = doc.Objects.AddPictureFrame(pl, path, False, x1 - x0, y1 - y0, True, True)
                    if gid != System.Guid.Empty:
                        ro = doc.Objects.FindId(gid)
                        a = ro.Attributes.Duplicate()          # keeps the picture's own image material
                        a.LayerIndex = lcache[layer]
                        dm = rendered_mode()
                        if dm is not None:
                            try:
                                a.SetDisplayModeOverride(dm)
                            except Exception:
                                pass
                        a.SetUserString(SEAM_TAG[0], SEAM_TAG[1])
                        try:
                            a.DisplayOrder = int(order)
                        except Exception:
                            pass
                        if gi >= 0:
                            a.AddToGroup(gi)
                        doc.Objects.ModifyAttributes(gid, a, True)
                        count += 1
                        if tech:
                            TECH_IDS.append(gid)
                    else:
                        failed += 1
                else:
                    _, txt, (x, y), h, col, _, order, font, bold, align, ang, italic = it[:12]
                    gid = bake_text(txt, rg.Point3d(x, y, 0.0), h, make_attrs(lcache[layer], col, order, None, gi),
                                    font, bold, align, ang, italic)
                    if gid is None or gid == System.Guid.Empty:
                        failed += 1
                        continue
                    count += 1
                    if tech:
                        TECH_IDS.append(gid)
            except Exception:
                failed += 1
    finally:
        doc.Views.RedrawEnabled = True
        doc.Views.Redraw()
    if failed:
        LOG.append("WARNING: {} items could not be baked.".format(failed))
    if BAKE_NOTES.get("dots"):
        LOG.append("WARNING: {} texts were baked as text dots (Rhino refused them as text).".format(BAKE_NOTES["dots"]))
    if refused:
        LOG.append("WARNING: {} fills could not be hatched by Rhino (layers: {}).".format(
            len(refused), ", ".join(sorted(set(refused))[:6])))
    return count


# ============================================================ v28: ONE VECTOR PDF PER DRAWING (no libraries)
# Written like bergama_diagrams_v1_7.py's writer: every label is one whole string (Tj), so Illustrator keeps it as
# one editable text object. Fonts are the PDF standard fonts (no embedding): Helvetica stands in for Josefin Sans,
# Courier for Courier New. WinAnsi encoding with the Turkish letters put in unused slots.
_PDF_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}
_PDF_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
_PDF_FONTS = ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique",
              "Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique")
_PDF_CAP = {"sans": 0.718, "mono": 0.571}             # capital height / font size (Rhino's text height is the capital)
_PT = 72.0 / 25.4


def pdf_str(s_):
    out = bytearray()
    for ch in s_:
        if ch in _PDF_ENC_EXTRA:
            out.append(_PDF_ENC_EXTRA[ch])
            continue
        try:
            b = ch.encode("cp1252")
        except Exception:
            b = b"?"
        if b == b"\x9e":                               # z caron's slot holds s cedilla
            b = b"?"
        out += b
    s2 = bytes(out).replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
    return b"(" + s2.replace(b"\r", b"").replace(b"\n", b" ") + b")"


def _pf(v):
    t_ = "%.3f" % v
    t_ = t_.rstrip("0").rstrip(".")
    return "0" if t_ in ("-0", "") else t_


def _png_rgb(path):
    """(width, height, IDAT bytes) of an 8-bit RGB, non-interlaced PNG (the kind this script writes), else None."""
    try:
        with open(path, "rb") as f_:
            d_ = f_.read()
        if d_[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        i_, idat, w_, h_ = 8, [], 0, 0
        while i_ + 8 <= len(d_):
            n_ = _struct.unpack(">I", d_[i_:i_ + 4])[0]
            t_ = d_[i_ + 4:i_ + 8]
            c_ = d_[i_ + 8:i_ + 8 + n_]
            if t_ == b"IHDR":
                w_, h_, bd_, ct_, _cm, _fm, il_ = _struct.unpack(">IIBBBBB", c_)
                if bd_ != 8 or ct_ != 2 or il_ != 0:
                    return None
            elif t_ == b"IDAT":
                idat.append(c_)
            elif t_ == b"IEND":
                break
            i_ += 12 + n_
        return (w_, h_, b"".join(idat)) if w_ and idat else None
    except Exception:
        return None


def _jpg_rgb(path):
    """v33: (width, height, file bytes, "DCT") of a baseline RGB JPEG (the site photos), else None."""
    try:
        with open(path, "rb") as f_:
            d_ = f_.read()
        if d_[:2] != b"\xff\xd8":
            return None
        i_ = 2
        while i_ + 9 < len(d_):
            if d_[i_] != 0xFF:
                return None
            m_ = d_[i_ + 1]
            n_ = _struct.unpack(">H", d_[i_ + 2:i_ + 4])[0]
            if m_ in (0xC0, 0xC1, 0xC2):
                h_, w_ = _struct.unpack(">HH", d_[i_ + 5:i_ + 9])
                return (w_, h_, d_, "DCT") if d_[i_ + 9] == 3 else None
            i_ += 2 + n_
    except Exception:
        pass
    return None


def _item_bb(it):
    k_ = it[0]
    if k_ == "text":
        x_, y_ = it[2]
        return (x_, y_, x_, y_)
    if k_ == "image":
        return it[2]
    pts = it[1] if k_ == "line" else [p for P in it[1] for p in P]
    if not pts:
        return None
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def _pdf_page(items, r, k, ox=0.0, oy=0.0, o=None, imgs=None):
    """The content of one drawing: items in display order, model (x, y) -> page mm (x - r[0]) * k + ox, clipped to
    the drawing's frame. v29: appended to o (a board's stream, already in mm) when given."""
    x0, y0 = r[0] - ox / k, r[1] - oy / k
    own = o is None
    if own:
        o = ["%s 0 0 %s 0 0 cm 1 J 1 j" % (_pf(_PT), _pf(_PT))]
        imgs = []
    A = o.append
    A("q %.2f %.2f %.2f %.2f re W n" % (ox, oy, (r[2] - r[0]) * k, (r[3] - r[1]) * k))
    cur = {}

    def col(c_, stroke):
        key = "S" if stroke else "f"
        if cur.get(key) == c_:
            return
        cur[key] = c_
        A("%s %s %s %s" % (_pf(c_[0] / 255.0), _pf(c_[1] / 255.0), _pf(c_[2] / 255.0), "RG" if stroke else "rg"))

    def lw(w_):
        w_ = max(0.01, float(w_) * PDF_LINE_SCALE)
        if cur.get("w") != w_:
            cur["w"] = w_
            A("%s w" % _pf(w_))

    def path(P, close):
        A("%.2f %.2f m" % ((P[0][0] - x0) * k, (P[0][1] - y0) * k))
        for p in P[1:]:
            A("%.2f %.2f l" % ((p[0] - x0) * k, (p[1] - y0) * k))
        if close:
            A("h")

    for it in items:
        kind = it[0]
        if kind == "fill":
            rings = [P for P in it[1] if len(P) >= 3]
            if not rings:
                continue
            col(it[2], False)
            for P in rings:
                path(P, True)
            A("f*")
        elif kind == "line":
            if len(it[1]) < 2:
                continue
            col(it[2], True)
            lw(it[5] if it[5] is not None else 0.13)
            path(it[1], False)
            A("S")
        elif kind == "hatch":
            _, polys, c_, _l, _o, spacing, ang, w_ = it[:8]
            segs = hatch_segments(polys, spacing, ang)
            if not segs:
                continue
            col(c_, True)
            lw(w_)
            for p, q in segs:
                A("%.2f %.2f m %.2f %.2f l" % ((p[0] - x0) * k, (p[1] - y0) * k, (q[0] - x0) * k, (q[1] - y0) * k))
            A("S")
        elif kind == "image":
            png = _png_rgb(it[1]) or _jpg_rgb(it[1])          # v33: JPEG photos too
            if png is None:
                continue
            ix0, iy0, ix1, iy1 = it[2]
            imgs.append(png)
            A("q %s 0 0 %s %s %s cm /Im%d Do Q" % (_pf((ix1 - ix0) * k), _pf((iy1 - iy0) * k), _pf((ix0 - x0) * k),
                                                   _pf((iy0 - y0) * k), len(imgs)))
        else:
            _, txt, (x_, y_), h_, c_, _l, _o, font, bold, align, ang, italic = it[:12]
            txt = str(txt)
            if not txt.strip():
                continue
            kd = kind_of(font)
            hm = h_ * k                                   # capital height on the page, mm
            size = hm / _PDF_CAP[kd]
            w_ = tw(txt, h_, kd) * k                      # the width the layout reserved for it
            fi = (4 if kd == "mono" else 0) + (1 if bold else 0) + (2 if italic else 0) + 1
            dx = {"L": 0.0, "C": -0.5 * w_, "R": -w_, "MC": -0.5 * w_}.get(align, 0.0)
            dy = -0.5 * hm if align == "MC" else 0.0
            ca, sa = math.cos(ang or 0.0), math.sin(ang or 0.0)
            px = (x_ - x0) * k + ca * dx - sa * dy
            py = (y_ - y0) * k + sa * dx + ca * dy
            col(c_, False)
            A("BT /F%d 1 Tf %s %s %s %s %s %s Tm %s Tj ET" % (fi, _pf(ca * size), _pf(sa * size), _pf(-sa * size),
                                                             _pf(ca * size), _pf(px), _pf(py),
                                                             pdf_str(txt).decode("latin-1")))
    A("Q")
    return "\n".join(o).encode("latin-1") if own else None, imgs


def board_layout(sizes, gap):
    """v29: (x, y) of each drawing's lower-left corner on a board (mm, y up from the bottom), in rows from the top
    left, in the given order; and the board's (width, height)."""
    if not sizes:
        return [], (0.0, 0.0)
    wmax = min(BOARD_MAX_MM - 20.0, max(max(w_ for w_, h_ in sizes), 1.5 * math.sqrt(sum(w_ * h_ for w_, h_ in sizes))))
    rows, row, x_ = [], [], 0.0
    for i_, (w_, h_) in enumerate(sizes):
        if row and x_ + w_ > wmax:
            rows.append(row)
            row, x_ = [], 0.0
        row.append((i_, x_))
        x_ += w_ + gap
    rows.append(row)
    W_ = max(sum(sizes[i_][0] for i_, _x in rw) + gap * (len(rw) - 1) for rw in rows)
    hs = [max(sizes[i_][1] for i_, _x in rw) for rw in rows]
    H_ = sum(hs) + gap * (len(rows) - 1)
    pos = [None] * len(sizes)
    top = H_
    for rw, hr in zip(rows, hs):
        for i_, x_ in rw:
            pos[i_] = (x_, top - sizes[i_][1])
        top -= hr + gap
    return pos, (W_, H_)


BOARD_MAX_MM = 4000.0                                 # v29: Aras: a board page never over 400 x 400 cm


