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
        _DG["pdf_fonts"] = pdf_fonts                   # G2/G3 28 Oct: the engine's PDF embeds Arial too
        exec(compile(DIAG_SRC, "bergama_diagrams_engine", "exec"), _DG)    # its functions read and see _DG itself
    return _DG


_DG = {}


def diagram_ctx(S):
    """The engine's context for this site model (places, crowns, walking network), once per run: S.dg = (DG, ctx)."""
    if getattr(S, "dg", None) is not None:
        return S.dg
    DG = diagrams_engine()
    DG["CREDIT"] = CREDIT
    # v49.1 (Aras 27 Oct, Prompt 8): the sheet's "Drawn by" line names this version (the engine's own said v40)
    DG["SCRIPT"] = SCRIPT_VERSION.split(" (")[0] + " (axonometric engine from bergama_diagrams v1.8)"
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


CROP_MV = {"walk_b": "walking_today", "car_b": "driving_today", "walk_d": "walking_change", "car_d": "driving_change",
           "comb_d": "combined_change"}                  # v40: crop slugs of plan 07's insets


# ============================================================ v33 AXONOMETRIC ENGINE (bergama_diagrams v1.8, cut down)
#@include ../data/DIAG_SRC.py


CROP_DEFAULT = {"The stream's tree cover": ("tree_cover", u"Tree crown cover along the banks, every 25 m", "riparian"),  # v47
                "Section along the spine": ("spine", u"Long section along the spine", "spine_section")}
# v40: drawings cropped whole below their title when they register no crop themselves (and every section)


def build_sheet(S, B, X, Y, U, rects):
    F = S.F
    del BOARD_KEY[:]                                   # v38: the drawings' numbered sources start at [1] on every run
    try:                                               # v46: the city link's shops plan reads its context from here
        write_city_context(S)
    except Exception:
        LOG.append("WARNING: city_context.json not written (the city link's p.9 plan draws without its context):\n" +
                   traceback.format_exc())
    gap, pad, maxw = 6.0 * U, 1.6 * U, 150.0 * U
    # v33: one plan for what is there (was 01, 05, 06, 08, 10 and the fabric_green map), its tables beside it
    SA = getattr(S, "whole", None) or S                  # v36: plan 01 over the whole file
    if SA is not S:
        SA.sec_lines, SA.sections = S.sec_lines, S.sections
        SA.site = S                                      # v45: plan 01's booklet legend leaves out the ring's colours
    w01 = 120.0 * U * (SA.F.w / context_frame(F).w if SA is not S else 1.0)    # v36: same print scale as the site
    items = [("01 What is there", w01, lambda x, y: draw_what_is_there(SA, B, x, y, w01, U)),
             ("02 Land-use legend", 30.8 * U, lambda x, y: draw_legend(S, B, x, y, 30.8 * U, U)),
             ("03 Distribution", 12.4 * U, lambda x, y: draw_distribution(S, B, x, y, U)),
             ("04 Green, farmland and orchards", 30.8 * U, lambda x, y: draw_green_table(S, B, x, y, 30.8 * U, U)),
             ("05 Readings", 24.0 * U, lambda x, y: draw_readings(S, B, x, y, 24.0 * U, None, U)),
             ("05c Site readings", 40.0 * U, lambda x, y: draw_site_readings(S, B, x, y, 40.0 * U, U)),   # v45
             ("06b The stream edge and where we can build", 120.0 * U,                          # v45
              lambda x, y: draw_edge_build(S, B, x, y, 120.0 * U, U)),
             ("07 How people use it", 120.0 * U, lambda x, y: draw_how_people_use_it(S, B, x, y, 120.0 * U, U)),
             # v50 (MIRAQUA 28 Oct, P09.3): "07b Commercial spines" is gone (drw_index_change under the proposal)
             ("07d City heritage loop", 120.0 * U, lambda x, y: draw_heritage_loop(S, B, x, y, 120.0 * U, U)),   # v46
             ("11b Section key", 30.8 * U, lambda x, y: draw_section_key(B, x, y, 30.8 * U, U)),
             ("11c Building types in the sections", 61.4 * U, lambda x, y: draw_typology_key(S, B, x, y, 61.4 * U, U)),
             ("11 Key question", 30.8 * U, lambda x, y: draw_key_question(S, B, x, y, 30.8 * U, U, cols=1))]
    shade_july_export(S)                                  # v51 (T3a): the shade drawing moved to p.17 (water board)
    # v44: the masterplan's proposal map (only when masterplan_results.json holds "movement") and the walking-effort
    # proof (only with terrain heights on the network); each logs why when it is left out
    at = [nm_ for nm_, w_, f_ in items].index("07d City heritage loop")
    R_ = movement(S).get("R")
    if R_ and getattr(R_["pieces"], "z", None):
        items.insert(at + 1, ("07e Walking effort", 120.0 * U,
                              lambda x, y: draw_walking_effort(S, B, x, y, 120.0 * U, U)))
    M_ = mp_movement()
    if M_ is not None:
        items.insert(at, ("07c Streets before and after", 120.0 * U,
                          lambda x, y: draw_mv_proposal(S, B, x, y, 120.0 * U, U, M_)))
    n_ = 13
    if S.sections:
        # v42 (Aras 26 Oct 07:06, p.09-11): every cut at ONE round scale, rows of whole cuts, at most two booklet pages
        sw = 140.0 * U
        plan_ = p45_plan(S, sw, U)                   # v51: p.04 S1-S4, p.05 S5-S8
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
# one editable text object. v50 (G2/G3): every slot is Arial, embedded by common/pdf_fonts.py (write_board_pdf);
# _PDF_FONTS are the standard fonts a slot falls back to. WinAnsi encoding with the Turkish letters in unused slots.
_PDF_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}
_PDF_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
_PDF_FONTS = ("Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique",
              "Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique")
_PDF_CAP = {"sans": 0.718, "mono": 0.718}             # capital height / font size; v50 (G2): "mono" prints Arial too
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


# v49.1 (Aras 27 Oct, Prompt 8; as bergama_water_board v3.1 for "hm³ renders as hm"): ² and ³ are shown as the digit at
# 0.6 x the size, raised 0.28 x the size (in Helvetica as wide as the ²/³ glyph, so nothing moves): the unembedded
# standard font's ²/³ was missing in some viewers
PDF_SUP = {u"²": u"2", u"³": u"3"}


def pdf_shows(s_, fi):
    """v49.1: the text-showing operators of s_ in font /F<fi> at size 1 (the text matrix carries the size): plain runs
    as one string each (Tj), ² and ³ as a raised small digit (PDF_SUP)."""
    out, cur = [], u""
    for ch in s_:
        if ch in PDF_SUP:
            if cur:
                out.append(pdf_str(cur).decode("latin-1") + " Tj")
                cur = u""
            out.append("/F%d 0.6 Tf 0.28 Ts (%s) Tj /F%d 1 Tf 0 Ts" % (fi, PDF_SUP[ch], fi))
        else:
            cur += ch
    if cur:
        out.append(pdf_str(cur).decode("latin-1") + " Tj")
    return " ".join(out)


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


def _png_rgba(path):
    """T4 30 Oct (D1 a cutouts): (w, h, zlib RGB, "RAW", zlib alpha or None) of an 8/16-bit non-interlaced PNG of any
    colour type (grey, grey+alpha, RGB, RGBA, palette + tRNS), else None. Pure Python: slow on very large files."""
    try:
        with open(path, "rb") as f_:
            d_ = f_.read()
        if d_[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        i_, idat, hdr, plte, trns = 8, [], None, b"", None
        while i_ + 8 <= len(d_):
            n_ = _struct.unpack(">I", d_[i_:i_ + 4])[0]
            t_, c_ = d_[i_ + 4:i_ + 8], d_[i_ + 8:i_ + 8 + n_]
            i_ += 12 + n_
            if t_ == b"IHDR":
                hdr = _struct.unpack(">IIBBBBB", c_[:13])
            elif t_ == b"PLTE":
                plte = c_
            elif t_ == b"tRNS":
                trns = c_
            elif t_ == b"IDAT":
                idat.append(c_)
            elif t_ == b"IEND":
                break
        if not hdr:
            return None
        w_, h_, bd, ct, _cm, _fm, il = hdr
        ch = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(ct)
        if ch is None or il or bd not in (8, 16) or (ct == 3 and bd != 8):
            return None
        import zlib as _zl
        bpp = ch * bd // 8
        raw = _zl.decompress(b"".join(idat))
        st = w_ * bpp
        out, prev, j_ = bytearray(h_ * st), bytearray(st), 0
        for y_ in range(h_):
            ft, ln = raw[j_], bytearray(raw[j_ + 1:j_ + 1 + st])
            j_ += 1 + st
            if ft == 1:
                for x_ in range(bpp, st):
                    ln[x_] = (ln[x_] + ln[x_ - bpp]) & 255
            elif ft == 2:
                for x_ in range(st):
                    ln[x_] = (ln[x_] + prev[x_]) & 255
            elif ft == 3:
                for x_ in range(st):
                    ln[x_] = (ln[x_] + (((ln[x_ - bpp] if x_ >= bpp else 0) + prev[x_]) >> 1)) & 255
            elif ft == 4:
                for x_ in range(st):
                    a, b = (ln[x_ - bpp] if x_ >= bpp else 0), prev[x_]
                    c = prev[x_ - bpp] if x_ >= bpp else 0
                    p = a + b - c
                    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                    ln[x_] = (ln[x_] + (a if pa <= pb and pa <= pc else (b if pb <= pc else c))) & 255
            out[y_ * st:(y_ + 1) * st] = ln
            prev = ln
        if bd == 16:
            out = out[0::2]
        out, n = bytes(out), w_ * h_
        alpha = None
        if ct == 3:
            pal = bytes(plte) + b"\x00" * (768 - len(plte))
            rgb = bytearray(n * 3)
            for c_ in range(3):
                rgb[c_::3] = out.translate(bytes(pal[3 * q + c_] for q in range(256)))
            if trns:
                alpha = out.translate(bytes(trns) + b"\xff" * (256 - len(trns)))
        elif ct in (0, 4):
            g_ = out if ct == 0 else out[0::2]
            alpha = None if ct == 0 else out[1::2]
            rgb = bytearray(n * 3)
            rgb[0::3], rgb[1::3], rgb[2::3] = g_, g_, g_
        elif ct == 2:
            rgb = out
        else:
            rgb = bytearray(n * 3)
            rgb[0::3], rgb[1::3], rgb[2::3] = out[0::4], out[1::4], out[2::4]
            alpha = out[3::4]
        if alpha is not None and alpha.count(b"\xff") == n:
            alpha = None
        return (w_, h_, _zl.compress(bytes(rgb), 6), "RAW", None if alpha is None else _zl.compress(bytes(alpha), 6))
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

    def blend(bm):                                    # v46: /GM multiplies (a Tint), /GN is normal (write_board_pdf)
        if cur.get("bm", "/GN") != bm:
            cur["bm"] = bm
            A(bm + " gs")

    def col(c_, stroke):
        blend("/GM" if getattr(c_, "mul", False) else "/GN")
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
            A("f" if getattr(it[2], "nz", False) else "f*")   # v50 (MIRAQUA 28 Oct, P06.3): R28NZ fills nonzero
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
            # T4 30 Oct (D1 a): each file once per board (imgs entry: w, h, data, kind, alpha, path); PNG alpha kept
            # (SMask); it[6] opacity 0-1, it[7] mirrored
            n_ = next((j_ + 1 for j_, e_ in enumerate(imgs) if len(e_) > 5 and e_[5] == it[1]), 0)
            if not n_:
                png = _png_rgb(it[1]) or _jpg_rgb(it[1]) or _png_rgba(it[1])   # v33: JPEG photos too
                if png is None:
                    continue
                png = tuple(png) + (None,) * (5 - len(png)) + (it[1],)
                imgs.append(png)
                n_ = len(imgs)
            ix0, iy0, ix1, iy1 = it[2]
            a_ = it[6] if len(it) > 6 else None
            fl_ = bool(it[7]) if len(it) > 7 else False
            blend("/GN")
            iw_ = (ix1 - ix0) * k
            A("q %s%s 0 0 %s %s %s cm /Im%d Do Q" % (
                "/A%02d gs " % max(1, min(19, int(round(a_ * 20)))) if a_ is not None and a_ < 0.975 else "",
                _pf(-iw_ if fl_ else iw_), _pf((iy1 - iy0) * k), _pf((ix0 - x0) * k + (iw_ if fl_ else 0.0)),
                _pf((iy0 - y0) * k), n_))
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
            A("BT /F%d 1 Tf %s %s %s %s %s %s Tm %s ET" % (fi, _pf(ca * size), _pf(sa * size), _pf(-sa * size),
                                                          _pf(ca * size), _pf(px), _pf(py),
                                                          pdf_shows(txt, fi)))     # v49.1: ² ³ raised (pdf_shows)
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


