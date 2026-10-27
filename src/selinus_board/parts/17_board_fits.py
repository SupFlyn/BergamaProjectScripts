def board_fits(members):
    """v29: whether these drawings make a board within BOARD_MAX_MM on both sides (margins and title included)."""
    k = 1000.0 / PDF_SCALE
    pos, (bw, bh) = board_layout([((r[2] - r[0]) * k, (r[3] - r[1]) * k) for items, r in members], 10.0)
    return bw + 20.0 <= BOARD_MAX_MM and bh + 38.0 <= BOARD_MAX_MM


def board_chunks(members):
    """v29: the drawings of one group split, in order, into as few boards as keep each one within BOARD_MAX_MM."""
    out, cur = [], []
    for m in members:
        if cur and not board_fits(cur + [m]):
            out.append(cur)
            cur = []
        cur.append(m)
    if cur:
        out.append(cur)
    return out


def write_board_pdf(path, title, members):
    """v29: one board = one PDF page holding every (items, frame) in members, each at 1:PDF_SCALE, laid out in rows
    with a 10 mm gap, a 10 mm margin and the board's title at the top."""
    k = 1000.0 / PDF_SCALE                                # mm on the page per model metre
    gap, mg, th = 10.0, 10.0, 6.0                         # mm: gap, margin, title capital height
    pos, (bw, bh) = board_layout([((r[2] - r[0]) * k, (r[3] - r[1]) * k) for items, r in members], gap)
    o = ["%s 0 0 %s 0 0 cm 1 J 1 j" % (_pf(_PT), _pf(_PT))]
    imgs = []
    for (items, r), (px, py) in zip(members, pos):
        _pdf_page(items, r, k, mg + px, mg + py, o, imgs)
    o.append("0.157 0.157 0.157 rg BT /F2 1 Tf %s 0 0 %s %s %s Tm %s Tj ET" % (
        _pf(th / _PDF_CAP["sans"]), _pf(th / _PDF_CAP["sans"]), _pf(mg), _pf(mg + bh + 1.5 * th),
        pdf_str(title).decode("latin-1")))
    stream = "\n".join(o).encode("latin-1")
    r = (0.0, 0.0, (bw + 2 * mg) / k, (bh + 2 * mg + 3.0 * th) / k)     # the page, in model units for the MediaBox
    objs = []

    def add(b):
        objs.append(b)
        return len(objs)
    fonts = [add(("<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding << /Type /Encoding /BaseEncoding "
                  "/WinAnsiEncoding %s >> >>" % (nm, _PDF_DIFF)).encode("latin-1")) for nm in _PDF_FONTS]
    xo = []
    for im_ in imgs:
        w_, h_, data = im_[:3]
        if len(im_) > 3:                                  # v33: a JPEG, embedded as it is
            xo.append(add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace /DeviceRGB "
                           "/BitsPerComponent 8 /Filter /DCTDecode /Length %d >>\nstream\n" % (w_, h_, len(data))
                           ).encode("latin-1") + data + b"\nendstream"))
            continue
        xo.append(add(("<< /Type /XObject /Subtype /Image /Width %d /Height %d /ColorSpace /DeviceRGB "
                       "/BitsPerComponent 8 /Filter /FlateDecode /DecodeParms << /Predictor 15 /Colors 3 "
                       "/BitsPerComponent 8 /Columns %d >> /Length %d >>\nstream\n" % (w_, h_, w_, len(data))
                       ).encode("latin-1") + data + b"\nendstream"))
    data = _zlib.compress(stream, 6)
    cid = add(b"<< /Length " + str(len(data)).encode() + b" /Filter /FlateDecode >>\nstream\n" + data + b"\nendstream")
    pages_id = len(objs) + 2
    res = "/Font << %s >>" % " ".join("/F%d %d 0 R" % (i + 1, f_) for i, f_ in enumerate(fonts))
    if xo:
        res += " /XObject << %s >>" % " ".join("/Im%d %d 0 R" % (i + 1, x_) for i, x_ in enumerate(xo))
    pw, ph = (r[2] - r[0]) * k * _PT, (r[3] - r[1]) * k * _PT
    page = add(("<< /Type /Page /Parent %d 0 R /MediaBox [0 0 %s %s] /Contents %d 0 R /Resources << %s >> >>"
                % (pages_id, _pf(pw), _pf(ph), cid, res)).encode("latin-1"))
    add(("<< /Type /Pages /Kids [%d 0 R] /Count 1 >>" % page).encode("latin-1"))
    cat = add(("<< /Type /Catalog /Pages %d 0 R >>" % pages_id).encode("latin-1"))
    info = add(b"<< /Title " + pdf_str(title) + b" /Producer " + pdf_str(SCRIPT_VERSION + ", scale 1:%d" %
                                                                         int(PDF_SCALE)) + b" >>")
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offs = []
    for i, b in enumerate(objs):
        offs.append(len(out))
        out += ("%d 0 obj\n" % (i + 1)).encode() + b + b"\nendobj\n"
    x_ = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)).encode()
    for o_ in offs:
        out += ("%010d 00000 n \n" % o_).encode()
    out += ("trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (
        len(objs) + 1, cat, info, x_)).encode()
    with open(path, "wb") as fh:
        fh.write(bytes(out))
    return [(mg + px, mg + py) for px, py in pos], bh + 2 * mg + 3.0 * th     # v40: drawings' corners, page height (mm)


def pdf_folder():
    return os.path.join(out_folder(), "selinus_board_pdf")


def board_of(name):
    """v29: (file stem, title) of the board a drawing goes on."""
    nm = str(name)
    head = nm.split(" · ")[0].strip()
    if head.startswith("Page"):
        return ("Selinus_pages", "THE SELINUS SEAM · BOARD PAGES")
    if len(head) >= 2 and head[0] == "T" and head[1].isdigit():
        t_ = head.split(".")[0]
        ttl = dict((n_, t2) for _k, n_, t2 in TSEC_DEF).get(t_, nm.split(" · ")[-1].upper())
        return ("Selinus_%s_%s" % (t_, "_".join(ttl.lower().split())), "%s · %s" % (t_, ttl))
    if "Section" in nm and "key" not in nm.lower():
        return ("Selinus_sections", "THE SELINUS SEAM · SECTIONS")
    return ("Selinus_drawings", "THE SELINUS SEAM · DRAWINGS")


def export_pdfs(B, rects):
    """v28: every drawing in rects, as vector PDF in pdf_folder(). Each item goes to every drawing its extent
    touches (the frame clips it); display order as in the bake, list order among equals. v29: grouped into boards,
    one single-page PDF per board (board_of). Returns (boards written, failed names)."""
    d_ = pdf_folder()
    if not os.path.isdir(d_):
        os.makedirs(d_)
    for f_ in os.listdir(d_):                             # v29: this folder only holds this script's PDFs
        if f_.lower().endswith(".pdf"):
            try:
                os.remove(os.path.join(d_, f_))
            except Exception:
                pass
    per = [[] for _ in rects]
    for n_, it in enumerate(B.items):
        bb = _item_bb(it)
        if bb is None:
            continue
        o_ = it[6] if it[0] == "text" else it[4]
        try:
            o_ = float(o_)
        except Exception:
            o_ = 0.0
        for i_, (nm, r) in enumerate(rects):
            if bb[2] >= r[0] and bb[0] <= r[2] and bb[3] >= r[1] and bb[1] <= r[3]:
                per[i_].append((o_, n_, it))
    boards, order, names = {}, [], {}
    for i_, (nm, r) in enumerate(rects):
        key = board_of(nm)
        if key not in boards:
            boards[key] = []
            names[key] = []
            order.append(key)
        boards[key].append((sorted(per[i_], key=lambda t_: (t_[0], t_[1])), r))
        names[key].append(nm)
    done, bad = 0, []
    del SHEET_POS[:]
    for key in order:
        stem, title = key
        try:
            parts = board_chunks([([t_[2] for t_ in its], r) for its, r in boards[key]])
            n_ = 0
            for j_, part in enumerate(parts):                 # more than one only if a board would pass 400 x 400 cm
                sfx = "" if len(parts) == 1 else "_%d" % (j_ + 1)
                pos_, ph_ = write_board_pdf(os.path.join(d_, stem + sfx + ".pdf"), title + (
                    "" if len(parts) == 1 else " · %d of %d" % (j_ + 1, len(parts))), part)
                for (px_, py_), (its_, r_) in zip(pos_, part):    # v40: where each drawing sits, for the booklet crops
                    SHEET_POS.append((names[key][n_], stem + sfx + ".pdf", r_, px_, py_, ph_))
                    n_ += 1
                done += 1
        except Exception as ex:
            bad.append("%s (%s)" % (stem, ex))
    return done, bad


# ============================================================ v31: SATELLITE LAND COVER (ESA WorldCover 2021)
ORCH_C = mix(TREE_COLS["orchard"], INK, 0.12)         # v31: orchards (as bergama_fabric_green v5)
FIELD_C = mix(CAT["agri"][1], PAPER, 0.2)              # v31: farmland (fields)
LC_FILE = "bergama_landcover_worldcover2021.json"
LC_CLASSES = [   # (key, legend label, colour): drawn in this order, under the surveyed / OSM ground
    ("grass", "Grassland · satellite", GREEN_SUB["grass"]),          # v32: full colours (were paler, hard to see)
    ("shrub", "Shrubland · satellite", mix(CAT["green"][1], PAPER, 0.3)),
    ("trees", "Tree cover · satellite", GREEN_SUB["wood"]),
    ("farmland", "Farmland · satellite (cropland)", CAT["agri"][1]),
    ("orchard", "Orchards · inferred (olive / fruit symbols)", ORCH_C),
]
LC_CREDIT = ("Land cover outside the surveyed and OSM areas: ESA WorldCover 10 m 2021 v200 (CC BY 4.0, contains "
             "modified Copernicus Sentinel data 2021); orchards inferred from the survey's olive and fruit-tree symbols.")


# v32: data/landcover/bergama_landcover_worldcover2021.json (ESA WorldCover 2021, CC BY 4.0), zlib + base64,
# so the land cover loads with no separate file (a file found by name or landcover_path still wins)
#@include ../data/LC_EMBED.py
# v33: bergama_plant_data_v1.json (2026-10-19) without the NDVI raster: canopy-map crowns, site photos, riparian corridor,
# Landsat heat, section strips; zlib + base64 (seam_pack() reads it)
#@include ../data/SEAM_PACK.py


def landcover_path():
    """v31: the land-cover file: the landcover_path input, else by name next to the env / osm / places files, the
    Grasshopper and Rhino files, or in Downloads, Desktop, Documents."""
    p = clean_path(inp("landcover_path", None), "landcover_path")
    if p and os.path.isfile(p):
        return p
    dirs = [DATA_DIR] + [os.path.dirname(q) for q in (ENV_PATH, OSM_PATH, PLACES_PATH) if q]
    try:
        dirs.append(os.path.dirname(ghenv.Component.OnPingDocument().FilePath))      # noqa: F821
    except Exception:
        pass
    try:
        dirs.append(os.path.dirname(Rhino.RhinoDoc.ActiveDoc.Path))
    except Exception:
        pass
    home = os.path.expanduser("~")
    dirs += [os.path.join(home, d_) for d_ in ("Downloads", "Desktop", "Documents")]
    for d_ in dirs:
        q = os.path.join(d_ or "", LC_FILE)
        if d_ and os.path.isfile(q):
            return q
    return None


def load_landcover(S):
    """v31: S.lc = {key: rings} in survey coordinates and S.lc_area = {key: m2 inside the frame} (rings keep the
    pixel boundaries' orientation, so the signed areas of the clipped rings add up to the area)."""
    S.lc, S.lc_area = {}, {}
    p = landcover_path()
    d = None
    if p:
        try:
            with open(p, encoding="utf-8") as f_:
                d = json.load(f_)
            if not isinstance(d, dict) or not d.get("rings"):
                raise ValueError("no land-cover rings in it")
        except Exception as ex_:                          # v33 (fabric_green v7): a broken file never hides the land cover
            LOG.append("WARNING: the land-cover file {} could not be used ({}); the copy built into this script was "
                       "used instead.".format(p, ex_))
            d = None
    if d is None:                                         # v32: the copy built into this script
        import base64 as _b64
        d = json.loads(_zlib.decompress(_b64.b64decode("".join(LC_EMBED))).decode("utf-8"))
        p = "the copy built into this script"
    for k, _lab, _c in LC_CLASSES:
        rings = [[(q[0], q[1]) for q in r] for r in d.get("rings", {}).get(k, []) if len(r) >= 3]
        rings = [c_ for c_ in (S.F.clip_poly(r) for r in rings) if c_ and len(c_) >= 3]   # v32.1: cut to the frame
        S.lc[k] = rings
        S.lc_area[k] = sum(signed_area(r) for r in rings)
    LOG.append("Land cover (ESA WorldCover 2021) from {}: ".format(p) + "; ".join(
        "{} {:.1f} ha".format(k, S.lc_area.get(k, 0.0) / 1e4) for k, _l, _c in LC_CLASSES) + " inside the site.")


REST_CELL = 2.0                                       # v35: m, raster that splits the frame's unmapped ground
REST_C = mix(PAPER, INK2, 0.22)                       # v35: other unmapped ground


def frame_total(S):
    """v35: the land-use tables' 100 %: the site frame when its unmapped ground is split, else the mapped part."""
    return S.frame_area if getattr(S, "rest", None) else S.total_area


def rest_of(S, *keys):
    """v35: m2 of these satellite classes on the frame's unmapped ground."""
    return sum(a for k, _l, _c, a in (getattr(S, "rest", None) or []) if k in keys)


def green_sat_note(S):
    """v35: the readings' green share counts only mapped green; the satellite's trees, grass and shrubs on the
    unmapped ground are added in a second figure, so the two sources are not mixed silently."""
    g = rest_of(S, "trees", "grass", "shrub")
    if g <= 0.0:
        return ""
    return " With the satellite's tree cover, grass and shrubs on the unmapped ground: {:.0f}%.".format(
        100.0 * (sum(z["A"] for z in S.zones if z["kind"] == "green") + g) / S.frame_area)


def _loop_rows(F, rings, cell, nx, ny):
    """Raster rows of all rings filled together (non-zero winding), so oppositely turning rings stay holes."""
    rows = [0] * ny
    loops = [[F.local(x, y) for x, y in r] for r in rings if len(r) >= 3]
    for j, spans in poly_spans(loops, F.u0, F.v0, cell, nx, ny, nonzero=True):
        m = rows[j]
        for a, b in spans:
            m |= ((1 << (b - a)) - 1) << a
        rows[j] = m
    return rows


def frame_rest(S):
    """v35: S.rest = [(key, label, colour, m2)]: the frame minus the mapped ground (S.total_area: buildings, OSM
    zones, measured street surfaces, the stream), split by the satellite classes (orchards first, as drawn on top)
    on a REST_CELL raster; the cell shares are scaled to frame area - mapped area, so the table adds up to the frame."""
    S.rest = []
    gap = S.frame_area - S.total_area
    if gap <= 0.0:
        return
    F, cell = S.F, REST_CELL
    nx, ny = int(math.ceil(F.w / cell)), int(math.ceil(F.h / cell))
    free = _loop_rows(F, [F.P], cell, nx, ny)
    mapped = [P for u in S.bld for P in u["parts"]] + list(getattr(S, "road_polys", None) or [])
    mrows = mask_of(F, [P for P in mapped if len(P) >= 3], cell, nx, ny)
    for z in S.zones:
        zr = mask_of(F, z["Ps"], cell, nx, ny, holes=z.get("Hs") or None)
        mrows = [a | b for a, b in zip(mrows, zr)]
    for w_ in (getattr(S, "water", None) or []):
        if len(w_["P"]) >= 3:
            wr = mask_of(F, [w_["P"]], cell, nx, ny, holes=w_.get("H") or None)
            mrows = [a | b for a, b in zip(mrows, wr)]
    free = [a & ~b for a, b in zip(free, mrows)]
    cnt = []
    for k, lab, col in reversed(LC_CLASSES):
        rings = getattr(S, "lc", {}).get(k) or []
        if not rings:
            continue
        m = [a & b for a, b in zip(free, _loop_rows(F, rings, cell, nx, ny))]
        free = [a & ~b for a, b in zip(free, m)]
        cnt.append((k, lab, col, sum(bin(r).count("1") for r in m)))
    cnt.append(("rest", "Other unmapped ground · yards, streets without a measured width, bare or built", REST_C,
                sum(bin(r).count("1") for r in free)))
    n = float(sum(c[3] for c in cnt))
    if n <= 0:
        return
    S.rest = [(k, lab, col, gap * c / n) for k, lab, col, c in cnt if c > 0]
    LOG.append("Unmapped ground of the frame ({:.2f} of {:.2f} ha; raster {:.2f} ha): ".format(
        gap / 1e4, S.frame_area / 1e4, n * cell * cell / 1e4) + "; ".join(
        "{} {:.2f} ha".format(k, a / 1e4) for k, _l, _c, a in S.rest))


def draw_landcover(S, B, V, L, order=2):
    """v31: the land-cover classes, each one fill (even-odd over all its rings), order 2 after the paper."""
    leg = []
    for k, lab, col in LC_CLASSES:
        rings = getattr(S, "lc", {}).get(k)
        if rings:
            for i in range(0, len(rings), 400):
                B.fill(V.Ps(rings[i:i + 400]), col, L, order)
            leg.append(("box", col, lab))
    return leg


# ============================================================ REPORT + RUN (only when the button is pressed)
def report(S):
    st = S.stats
    out = ["Frame {:.0f} x {:.0f} m ({:.1f} ha){}".format(S.F.w, S.F.h, S.F.area / 1e4,
                                                       "" if getattr(S, "frame_src", "survey") == "input"
                                                       else " - the " + S.frame_src
                                                       if getattr(S, "frame_src", "").startswith("analysis range")
                                                       else " - whole survey in the file"),
           "Survey units: {} | floor labels {} (unmatched {}) | sheds {}".format(
               st.get("survey_units", 0), st.get("floor_labels", 0), st.get("labels_unmatched", 0), st.get("sheds", 0)),
           "OSM footprints: {} for unmatched labels, {} infill | floor labels with no closed outline (not drawn): {}".format(
               st.get("osm_fallback", 0), st.get("osm_infill", 0), st.get("labels_open", 0)),
           "Floors: " + ", ".join("{} {}".format(k, v) for k, v in sorted(
               dict((k_, len([u for u in S.bld if u["floors_src"] == k_])) for k_ in
                    set(u["floors_src"] for u in S.bld)).items())) +
           " | neighbour rule tested on {} surveyed: same {:.0f} %, within one floor {:.0f} %".format(
               *getattr(S, "floor_test", (0, 0.0, 0.0))),
           street_note(S) + " " + channel_note(S),
           "Points of interest used: {}".format(len(S.pois))]
    for k in CAT_ORDER:
        if S.area.get(k, 0) > 0:
            out.append("  {:<26s}{:>7.2f} ha {:>6.1f}%".format(short(CAT[k][0]), S.area[k] / 1e4, 100.0 * S.area[k] / S.total_area))
    out.append("Stream: bank analysed {:.0f} m | terrain samples {} ({} from bank and stream lines)".format(
        sum(S.edge_len.values()), S.terrain_n, getattr(S, "terrain_banks", 0)))
    re_ = S.stats.get("river_edges", {})
    if re_:
        tot_ = float(sum(re_.values()))
        out.append("River edges found on: " + ", ".join("{} {:.0f}%".format(k, 100.0 * v / tot_)
                                                         for k, v in sorted(re_.items(), key=lambda kv: -kv[1])))
    out.append("Sections: {}".format(len(S.sections) if S.sections else "none (no section lines)"))
    return "\n".join(out)


def place_board(B, rects, OX, OY, sc):
    """Move the finished layout beside the drawing (and scale it with the drawing, if the drawing was scaled)."""
    P = lambda x, y: (OX + sc * x, OY + sc * y)
    items = []
    for it in B.items:
        if it[0] == "fill":
            items.append(("fill", [[P(x, y) for x, y in poly_] for poly_ in it[1]]) + it[2:])
        elif it[0] == "line":
            items.append(("line", [P(x, y) for x, y in it[1]]) + it[2:])
        elif it[0] == "hatch":
            items.append(("hatch", [[P(x, y) for x, y in poly_] for poly_ in it[1]]) + it[2:5] + (it[5] * sc,) + it[6:])
        elif it[0] == "image":
            r = it[2]
            items.append(("image", it[1], P(r[0], r[1]) + P(r[2], r[3])) + it[3:])
        else:
            items.append(("text", it[1], P(*it[2]), it[3] * sc) + it[4:])
    B.items = items
    for p_ in CROP_PANELS:                                # v40: the booklet crops move (and scale) with the layout
        b_ = p_["bb"]
        p_["bb"] = (OX + sc * b_[0], OY + sc * b_[1], OX + sc * b_[2], OY + sc * b_[3])
        if p_["scale_den"] and sc:
            p_["scale_den"] = int(round(p_["scale_den"] / sc))
    return [(n, (OX + sc * r[0], OY + sc * r[1], OX + sc * r[2], OY + sc * r[3])) for n, r in rects]


def pipeline(RAW_user, frame_pts_user, sec_lines_user, osm_path, places_path, tech_secs_user=None):
    """v18: the run, with the worker processes of the one-core stages started on first use and ended after it."""
    pool_stop()
    pool_allow(True)
    try:
        return pipeline_run(RAW_user, frame_pts_user, sec_lines_user, osm_path, places_path, tech_secs_user)
    finally:
        try:
            pool_report()
        finally:
            pool_stop()
            pool_allow(False)


def _plain_repr(v):
    """repr with sets in sorted order (their order changes between Rhino sessions)."""
    if isinstance(v, (set, frozenset)):
        return "{" + ",".join(sorted(_plain_repr(x) for x in v)) + "}"
    if isinstance(v, dict):
        return "{" + ",".join(_plain_repr(k) + ":" + _plain_repr(x) for k, x in v.items()) + "}"
    if isinstance(v, (list, tuple)):
        return ("[%s]" if isinstance(v, list) else "(%s)") % ",".join(_plain_repr(x) for x in v)
    if type(v).__name__ == "function":                  # by name and bytecode, not by its address in memory
        return "fn:%s:%s" % (v.__qualname__, _hashlib.sha1(v.__code__.co_code).hexdigest())
    return repr(v)


def build_site_key(R, osm, places, F):
    """Fingerprint of everything build_site reads: the survey, the frame, OSM and places, the bytecode of build_site
    and of every function and class it reaches, and the settings those read (LOG, the run's own messages, left out).
    An edit to any of them gives a new key, so an old site model is never reused."""
    g = globals()
    code = _code_print()
    seen, parts, todo = set(), [], ["build_site"]
    while todo:
        nm = todo.pop()
        if nm in seen or nm == "LOG" or nm not in g:
            continue
        seen.add(nm)
        v = g[nm]
        if type(v).__name__ == "function":
            cos = [v.__code__]
            parts.append((nm, code.get(nm), _plain_repr(v.__defaults__)))
        elif isinstance(v, type):
            fs = [f for a, f in sorted(vars(v).items()) if type(f).__name__ == "function"]
            cos = [f.__code__ for f in fs]
            parts.append((nm, sorted((k, h) for k, h in code.items() if k.startswith(nm + ".")),
                          [_plain_repr(f.__defaults__) for f in fs]))
        elif isinstance(v, _types.ModuleType):
            continue
        else:
            parts.append((nm, _plain_repr(v)))
            continue
        while cos:
            c = cos.pop()
            todo.extend(c.co_names)
            cos.extend(k for k in c.co_consts if hasattr(k, "co_code"))
    return fp("site", sorted(parts), _plain_repr(R), _plain_repr(osm), _plain_repr(places), F.P)


def build_site_once(R, osm, places, F):
    """build_site, worked out once and kept (Aras 25 Oct 21:29: "you check once and cache it"): in Rhino's memory for
    this session and in cached/selinus_cache, found again only by build_site_key. Kept as pickled bytes, so later
    changes to the model in a run never reach the kept copy; its log lines are replayed."""
    key = ST = None
    try:
        key = build_site_key(R, osm, places, F)
        ST = Store()
        blob = ST.get("site", key)
    except Exception:
        key = blob = None
    if blob is not None:
        try:
            _ns_register()                                   # the classes are pickled under module selinus_ns
            S, msgs = _pickle.loads(blob)
            LOG.extend(msgs)
            S.F = F
            if hasattr(S, "terrain_smp"):
                S.z_at = terrain_z_at(S, S.terrain_smp)      # a function: made again from its samples, as the workers do
            return S
        except Exception:
            pass
    n0 = len(LOG)
    S = build_site(R, osm, places, F)
    if key is not None:
        try:
            _ns_register()
            z_at = S.__dict__.pop("z_at", None)
            try:
                blob = _pickle.dumps((S, LOG[n0:]), protocol=4)
            finally:
                if z_at is not None:
                    S.z_at = z_at
            ST.put("site", key, blob)
        except Exception:
            pass
    return S


def site_model(RAW_user, frame_pts_user, sec_lines_user, osm_path, places_path, tech_secs_user=None):
    """v20: the site model from what was read from the open file (read_rhino) and the picked frame and lines (file
    coordinates): alignment, survey, frame, section lines, OSM and places, build_site, study areas, fabric types.
    Returns (S, T, I, FR); S.T and S.I are set too. pipeline_run calls it first; other scripts can call it the same
    way (set STUDY_RAW and _SITE_FALLBACK first if they need those)."""
    global SEC_IN
    T = fit_user_transform(RAW_user["texts"])
    if T is None:
        T = dict(IDENTITY)
        LOG.append("Survey labels not recognised: assuming the drawing sits at its original survey position.")
    I = T_inverse(T)
    RAW = register_layers(raw_to_survey(RAW_user, T))
    if not any(RAW["lines"].get(l) for l in DWG["bld"]):
        raise Exception("No survey building layers (BINA_*) found. Is the halihazir DWG open in this file?")
    FR = None
    frame_src = "survey"
    rp = ([T_apply(I, x, y) for x, y in frame_pts_user] if frame_pts_user else
          list(SITE_FRAME_LK))     # v36: no frame wired = the analysis range (recorded site frame), in any file
    if rp:
        mr = min_area_rect(rp)                                   # always a clean rectangle
        if mr is None or min(mr[3] - mr[2], mr[5] - mr[4]) < 1.0:
            LOG.append("WARNING: the frame curve encloses no area (a line or a point?). It was ignored and the whole "
                       "survey was used instead.")
        else:
            _, ang_, u0_, u1_, v0_, v1_ = mr
            c_, s_ = math.cos(ang_), math.sin(ang_)
            FR = Frame([(c_ * u - s_ * v, s_ * u + c_ * v) for u, v in ((u0_, v0_), (u1_, v0_), (u1_, v1_), (u0_, v1_))])
            # kept unless nothing of the survey (no building, no stream bank) lies inside it
            inside = any(FR.inside((s[0] + s[2]) / 2.0, (s[1] + s[3]) / 2.0)
                         for l in list(DWG["bld"]) + DWG["banks"] for s in RAW["lines"].get(l, []))
            if not inside:
                LOG.append("WARNING: the frame curve covers none of the survey's buildings or stream banks (was it drawn "
                           "before the drawing was rotated or moved?). It was ignored and the whole survey was used.")
                FR = None
            else:
                frame_src = (("analysis range (site_alan)" if FRAME_FROM_LAYER[0] else "input") if frame_pts_user
                             else "analysis range (SITE_FRAME_LK)")
    if FR is None:
        FR = frame_from_survey(RAW)
    SEC_IN = [(T_apply(I, a[0], a[1]), T_apply(I, b[0], b[1])) for a, b in sec_lines_user]
    if not SEC_IN and _SITE_FALLBACK.get("section_lines"):
        SEC_IN = list(SECTION_LINES_LK)                         # v20: recorded lines, survey coordinates
    for k in TSEC_KEYS:
        TSEC[k] = [(T_apply(I, a[0], a[1]), T_apply(I, b[0], b[1])) for a, b in (tech_secs_user or {}).get(k, [])]
        if not TSEC[k] and _SITE_FALLBACK.get(k):
            TSEC[k] = list(SECTION_LINES_LK)
    OSM = parse_osm(osm_path) if osm_path else None
    PLACES = parse_places(places_path) if places_path else []
    S = build_site_once(RAW, OSM, PLACES, FR)
    S.osm = OSM                                            # v33: the movement potential reuses it
    try:
        load_landcover(S)                                 # v31: satellite land cover (farmland, orchards, ...)
    except Exception:
        LOG.append("WARNING: land-cover file could not be read:\n" + traceback.format_exc())
        S.lc, S.lc_area = {}, {}
    try:
        frame_rest(S)                                     # v35: the unmapped ground of the frame, by satellite class
    except Exception:
        LOG.append("WARNING: the unmapped ground could not be split (the land-use table shows the mapped part):\n" +
                   traceback.format_exc())
        S.rest = []
    S.frame_src = frame_src
    try:
        S.ctx_lines = context_lines(RAW, FR)                 # v33: quiet context around the frame
    except Exception:
        S.ctx_lines = {}
        LOG.append("WARNING: context around the frame not read:\n" + traceback.format_exc())
    S.study_areas = study_areas_from(STUDY_RAW, I)                          # v19: read only, never drawn (v33)
    S.whole = None
    if RUN_MODE != "technical":
        try:
            S.whole = whole_site(RAW, OSM, PLACES, FR, S)        # v36: plan 01 over the whole file
        except Exception:
            LOG.append("WARNING: the whole-file map (plan 01) could not be built; plan 01 shows the site frame:\n" +
                       traceback.format_exc())
    S.water_pts = [T_apply(I, x, y) + (z,) for x, y, z in WATER_PTS_USER]     # v16.5: measured water levels
    fabric_types(S)
    S.T, S.I = T, I
    return S, T, I, FR


def pipeline_run(RAW_user, frame_pts_user, sec_lines_user, osm_path, places_path, tech_secs_user=None):
    S, T, I, FR = site_model(RAW_user, frame_pts_user, sec_lines_user, osm_path, places_path, tech_secs_user)
    if RUN_MODE != "technical":
        run_analyses(S)
    if RUN_MODE in ("technical", "all"):
        S.focus_frame = None
        if FOCUS_PTS_USER:
            fp = [T_apply(I, x, y) for x, y in FOCUS_PTS_USER]
            mr = min_area_rect(fp)
            if mr is None or min(mr[3] - mr[2], mr[5] - mr[4]) < 10.0:
                LOG.append("WARNING: the focus curve encloses no area of at least 10 x 10 m (a line?). The densest stretch "
                           "of the stream was used for the radiation sheet instead.")
            else:
                _, ang_, u0_, u1_, v0_, v1_ = mr
                c_, s_ = math.cos(ang_), math.sin(ang_)
                S.focus_frame = Frame([(c_ * u - s_ * v, s_ * u + c_ * v) for u, v in ((u0_, v0_), (u1_, v0_), (u1_, v1_), (u0_, v1_))])
                if not all(FR.inside(x_, y_) for x_, y_ in S.focus_frame.P):
                    LOG.append("WARNING: the focus area reaches beyond the frame; buildings and trees outside the frame "
                               "are not modelled, so that part of the radiation map lacks their shade.")
        del NOISE_PTS_SURVEY[:]
        NOISE_PTS_SURVEY.extend(T_apply(I, x, y) for x, y in NOISE_PTS_USER)
        run_environment(S)
    if RUN_MODE == "board" and any(TSEC[k] for k in TSEC_KEYS):
        LOG.append("Technical section lines are drawn when run is \"technical\" or \"both\" (they need env_path).")
    B, rects = build_layout(S)
    ST_ = getattr(S, "store", None)
    if ST_ is not None:
        kept = len((getattr(S, "env", None) or {}).get("maps_kept", []))
        LOG.append("Results kept between runs: " + (ST_.summary() or "none yet") +
                   ("; {} unchanged maps kept as they were".format(kept) if kept else ""))
    ub = bb_pts([T_apply(T, x, y) for x, y in FR.P])
    rb = raw_bb(RAW_user)                                     # beside the whole drawing, not only the frame
    if rb is not None:
        ub = (min(ub[0], rb[0]), min(ub[1], rb[1]), max(ub[2], rb[2]), max(ub[3], rb[3]))
    rects = place_board(B, rects, ub[2] + 0.25 * (ub[2] - ub[0]), ub[3], T["s"])
    S.T = T
    return S, B, rects


def raw_bb(R):
    """Bounding box of everything read from the drawing (lines, points, texts), or None."""
    xs, ys = [], []
    for lst in R.get("lines", {}).values():
        for s in lst:
            xs += [s[0], s[2]]
            ys += [s[1], s[3]]
    for lst in R.get("points", {}).values():
        for p in lst:
            xs.append(p[0])
            ys.append(p[1])
    for lst in R.get("texts", {}).values():
        for t in lst:
            xs.append(t[1])
            ys.append(t[2])
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys))


def align_note(T):
    if T.get("n", 0) == 0:
        return "Alignment: none (drawing assumed at its survey position)"
    moved = math.hypot(T["tx"], T["ty"])
    if abs(T["th"]) < 1e-6 and moved < 0.01 and abs(T["s"] - 1) < 1e-6:
        return "Alignment: drawing at its original survey position ({} labels matched)".format(T["n"])
    return "Alignment: drawing rotated {:.2f} deg{}, matched by {} labels (median error {:.2f})".format(
        math.degrees(T["th"]), "" if abs(T["s"] - 1) < 1e-4 else ", scaled x{:.4f}".format(T["s"]), T["n"], T["err"])


def gh_message(level, text):
    """Show a balloon on the component itself (visible without a Panel)."""
    try:
        import Grasshopper
        lv = {"error": Grasshopper.Kernel.GH_RuntimeMessageLevel.Error,
              "warning": Grasshopper.Kernel.GH_RuntimeMessageLevel.Warning,
              "remark": Grasshopper.Kernel.GH_RuntimeMessageLevel.Remark}[level]
        ghenv.Component.AddRuntimeMessage(lv, text[:500])
    except Exception:
        pass


def as_curve(x):
    """Read a curve whatever form the input delivers it in: a Curve, a Grasshopper wrapper, a Line, Polyline,
    Rectangle, Circle or Arc, or an object id (from Rhino or from Grasshopper's own document)."""
    if x is None:
        return None
    if hasattr(x, "TryGetPolyline"):
        return x
    g = x
    for _ in range(3):                                     # Grasshopper goo wrappers
        if hasattr(g, "TryGetPolyline") or not hasattr(g, "Value"):
            break
        try:
            g = g.Value
        except Exception:
            break
    if hasattr(g, "TryGetPolyline"):
        return g
    try:
        if isinstance(g, rg.Line):
            return rg.LineCurve(g)
        if isinstance(g, rg.Polyline):
            return rg.PolylineCurve(g)
        if isinstance(g, (rg.Circle, rg.Arc)):
            return rg.ArcCurve(g)
        if isinstance(g, rg.Rectangle3d):
            return g.ToNurbsCurve()
    except Exception:
        pass
    try:
        c = g.ToNurbsCurve()
        if c is not None and hasattr(c, "TryGetPolyline"):
            return c
    except Exception:
        pass
    try:
        gid = g if isinstance(g, System.Guid) else System.Guid(str(g))
        for d_ in (doc, getattr(sc, "doc", None)):
            try:
                o = d_.Objects.FindId(gid) if d_ is not None else None
                geo = o.Geometry if o is not None else None
                if geo is not None and hasattr(geo, "TryGetPolyline"):
                    return geo
            except Exception:
                pass
    except Exception:
        pass
    try:
        import rhinoscriptsyntax as rs
        c = rs.coercecurve(g)
        if c is not None:
            return c
    except Exception:
        pass
    try:
        import Grasshopper
        res = Grasshopper.Kernel.GH_Convert.ToCurve(g, None, Grasshopper.Kernel.GH_Conversion.Both)
        if isinstance(res, tuple) and res[0] and res[1] is not None:
            return res[1]
    except Exception:
        pass
    return None


def as_list(v):
    if v is None:
        return []
    if isinstance(v, (str, bytes)):
        return [v]
    try:
        return [c for c in v if c is not None]
    except TypeError:
        return [v]


def curve_points(c, n=64):
    """Vertices of a polyline-like curve, or n points along any other curve."""
    res = c.TryGetPolyline()
    if isinstance(res, tuple) and res[0]:
        return [(res[1][i].X, res[1][i].Y) for i in range(res[1].Count)]
    ts = c.DivideByCount(n, True) or []
    return [(c.PointAt(t).X, c.PointAt(t).Y) for t in ts]


SECTION_INPUTS = ["section_lines", "sound_sections", "heat_sections", "shade_sections", "solar_sections",
                  "wind_sections", "air_sections", "felt_sections"]
LIST_INPUTS = SECTION_INPUTS + ["noise_points", "noise_db"]
INPUT_HELP = {
    "sound_sections": "Lines (Top view) for sound sections: Lden and day, evening, night levels in the section plane",
    "heat_sections": "Lines (Top view) for surface heat sections: Landsat surface temperature along ground and roofs",
    "shade_sections": "Lines (Top view) for shade sections: hours in shade at every point of the section plane",
    "solar_sections": "Lines (Top view) for solar radiation sections: kWh/m2 on ground, roofs and facades",
    "wind_sections": "Lines (Top view) for wind sections: mean wind speed at every height of the section plane",
    "air_sections": "Lines (Top view) for air temperature sections: mean dry bulb at every height of the plane",
    "felt_sections": "Lines (Top view) for felt temperature (UTCI) sections: mean UTCI at every point of the plane",
    "hours": "Hours the wind, air and felt temperature means take: daylight (default), all, or a local range like 10-17",
}


def skey(name):
    """A sticky key of this component only (several components in one session keep their own state)."""
    try:
        return name + ":" + str(ghenv.Component.InstanceGuid)
    except Exception:
        return name


# v16.7: what the component remembers between solutions. With a Button the log of a build vanished the moment the
# button sprang back: Rhino 8's Python 3 component does not always keep scriptcontext.sticky to the next solution.
def mem_get(name, default=None):
    """25 Oct (Aras 09:55): this Rhino session only (sticky); no temp state file. The one copy on disk is the log in
    Downloads/Bergama/logs/, read back only if the session lost the last build's report."""
    k = skey(name)
    try:
        if k in sc.sticky:
            return sc.sticky[k]
    except Exception:
        pass
    if name == "lu_last":
        try:
            with open(log_file_path(), encoding="utf-8") as f_:
                return dict(info=f_.read(), when="from the log file", secs=0)
        except Exception:
            pass
    return default


def mem_set(name, value, disk=True):
    try:
        sc.sticky[skey(name)] = value
    except Exception:
        pass


def log_file_path():
    d_ = os.path.join(BERGAMA_DIR, "logs")                   # v37 (Aras 25 Oct 09:35): every script's log in Bergama/logs
    try:
        if not os.path.isdir(d_):
            os.makedirs(d_)
    except Exception:
        pass
    return os.path.join(d_, "selinus_board_log.txt")


def out_folder():
    """Downloads/Bergama/output/selinus_board: the PDFs (selinus_board_pdf) and pictures. 25 Oct 10:45 (Aras): outputs only
    in output/, logs only in logs/ (09:35 had made this the logs folder by mistake); the cache is in cached/."""
    try:
        os.makedirs(SELINUS_OUT_DIR, exist_ok=True)
        stray = os.path.join(BERGAMA_DIR, "logs", "selinus_board_pdf")      # written there by mistake on 25 Oct: removed
        if os.path.isdir(stray):
            import shutil
            shutil.rmtree(stray, ignore_errors=True)
    except Exception:
        pass
    return SELINUS_OUT_DIR


def fmt_secs(s_):
    """v27: 0.4 s, 8.2 s, 312 s."""
    return "{:.1f} s".format(s_) if s_ < 10.0 else "{:.0f} s".format(s_)


def run_head(secs_, n_draw, ok, t_site=None, t_bake=None, n_obj=None):
    """v27: the masterplan-style opening of the log: when and which version, the result, the output folder, then one
    line per created drawing with its time."""
    import datetime
    n_err = sum(1 for l_ in LOG if str(l_).startswith("ERROR"))
    n_warn = sum(1 for l_ in LOG if str(l_).startswith("WARNING"))
    res_ = ("done in {:.0f} s: {} drawing{}".format(secs_, n_draw, "" if n_draw == 1 else "s") if ok
            else "FAILED after {:.0f} s".format(secs_))
    head = ["Run at {} | {}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), SCRIPT_VERSION),
            "RESULT: {} | {} warning{}, {} error{}".format(res_, n_warn, "" if n_warn == 1 else "s", n_err,
                                                         "" if n_err == 1 else "s"),
            "OUTPUT FOLDER: {} (PDF boards in selinus_board_pdf); log: {}"
            .format(out_folder(), log_file_path())]
    if ok:
        head.append("CREATED (each with the time it took):")
        if t_site is not None:
            head.append("  site model and analyses  {}".format(fmt_secs(t_site)))
        for nm_, s_ in DRAWING_TIMES:
            head.append("  {}  {}".format(nm_, fmt_secs(s_)))
        if t_bake is not None:
            head.append("  bake into Rhino ({} objects)  {}".format(n_obj or 0, fmt_secs(t_bake)))
    head.append("-" * 60)
    return "\n".join(head)


GH_LABEL = "MainBoard"                             # Aras 25 Oct 09:44: name under the component


def gh_status(text):
    """v27: the short text under the component (its Message). Never fails. v37: led by GH_LABEL; a run shows its
    time of day and length, else idle."""
    try:
        ghenv.Component.Message = GH_LABEL + " " + text                # noqa: F821
    except Exception:
        pass


def save_last(info_, out_, secs_):
    """The report of this build: kept in memory with its outputs, on disk with its time (outputs cannot be stored)."""
    import datetime
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mem_set("lu_last_out", out_, disk=False)
    mem_set("lu_last", dict(info=info_, when=stamp, secs=round(secs_, 1)))
    st_ = "v40 · ERROR" if info_.startswith("ERROR") or "RESULT: FAILED" in info_[:400] else \
        "v40 · {} · {:.0f} s".format(__import__("time").strftime("%H:%M"), secs_)
    mem_set("lu_status", st_)
    gh_status(st_)
    try:
        with open(log_file_path(), "w", encoding="utf-8") as f_:
            f_.write(info_ + "\n")                    # v27: the log already opens with its time and version
    except Exception:
        pass


def component_setup():
    """Give the component what it needs, once: List Access on the section and noise inputs, the seven technical
    section inputs and an info output. Changes are made between solutions (scheduled), never during one.
    Returns (changed now, inputs that were on item access with data on them)."""
    try:
        import Grasshopper
        from Grasshopper.Kernel import GH_ParamAccess, GH_ParameterSide
        comp = ghenv.Component
    except Exception:
        return [], []
    item_with_data = [p.NickName for p in comp.Params.Input
                      if p.NickName in LIST_INPUTS and p.Access != GH_ParamAccess.list and p.SourceCount > 0]
    want_in = [n for n in INPUT_HELP if n not in [p.NickName for p in comp.Params.Input]]
    want_access = [p.NickName for p in comp.Params.Input if p.NickName in LIST_INPUTS and p.Access != GH_ParamAccess.list]
    want_outs = [n for n in ("log", "done") if n not in [p.NickName for p in comp.Params.Output]]
    want_out = bool(want_outs)
    if not (want_in or want_access or want_out):
        return [], []
    if sc.sticky.get(skey("lu_setup_pending")):
        return [], item_with_data
    sc.sticky[skey("lu_setup_pending")] = True

    def setup(gh_doc):
        done = []
        try:
            for p in comp.Params.Input:
                if p.NickName in LIST_INPUTS and p.Access != GH_ParamAccess.list:
                    p.Access = GH_ParamAccess.list
                    done.append(p.NickName + " -> List Access")
            for name in want_in:
                if name in [p.NickName for p in comp.Params.Input]:
                    continue
                idx = comp.Params.Input.Count
                p = comp.CreateParameter(GH_ParameterSide.Input, idx)
                p.NickName = name
                p.Name = name
                p.Description = INPUT_HELP[name]
                p.Access = GH_ParamAccess.list if name in LIST_INPUTS else GH_ParamAccess.item
                p.Optional = True
                comp.Params.RegisterInputParam(p, idx)
                done.append("input " + name)
            for name, help_ in (("log", "Report of the last build: warnings, timings, what was read"),
                                ("done", "True after a good build: wire into the next script's run")):
                if name in [p.NickName for p in comp.Params.Output]:
                    continue
                idx = comp.Params.Output.Count
                p = comp.CreateParameter(GH_ParameterSide.Output, idx)
                p.NickName = name
                p.Name = name
                p.Description = help_
                comp.Params.RegisterOutputParam(p, idx)
                done.append("output " + name)
            comp.VariableParameterMaintenance()
            comp.Params.OnParametersChanged()
            sc.sticky[skey("lu_setup_done")] = done
        except Exception:
            sc.sticky[skey("lu_setup_done")] = ["could not change the component: " + traceback.format_exc()[-300:]]
        sc.sticky[skey("lu_setup_pending")] = False
        comp.ExpireSolution(False)
    try:
        comp.OnPingDocument().ScheduleSolution(20, Grasshopper.Kernel.GH_Document.GH_ScheduleDelegate(setup))
    except Exception:
        sc.sticky[skey("lu_setup_pending")] = False
        return [], item_with_data
    return (want_access + want_in + want_outs), item_with_data


def read_lines(name, vals):
    """Section lines of one input: endpoints of every readable curve; unreadable items are reported by type."""
    out, bad = [], []
    for c in as_list(vals):
        cv = as_curve(c)
        e = sec_endpoints(cv) if cv is not None else None
        if e is None:
            bad.append(type(c).__name__)
        else:
            out.append(e)
    if bad:
        LOG.append("WARNING: {} item(s) on {} could not be read as curves (they arrived as {}).".format(
            len(bad), name, ", ".join(sorted(set(bad)))))
    return out


LAYOUT = str(inp("layout", "drawings")).strip().lower()     # v33: kept as the main block's first line (POOL_KEY)
LAYOUT = "drawings"                                     # v33: the separate drawings only (Aras Q13); pages retired
info = ""
drawings, names, footprints, floors, uses, cuts = [], [], [], [], [], []
if HAVE_RHINO:
    doc = Rhino.RhinoDoc.ActiveDoc
    TOL = doc.ModelAbsoluteTolerance if doc else 0.01
    pressed = (DO_BAKE and not mem_get("lu_bake_prev", False)) or chain_fire(_button_value(), "chain_seen")
    mem_set("lu_bake_prev", bool(DO_BAKE))
    last = mem_get("lu_last")
    _t_build = __import__("time").time()
    changing, partial = component_setup()
    setup_done = sc.sticky.pop(skey("lu_setup_done"), None)
    if setup_done:
        gh_message("remark", "Component set up: " + "; ".join(setup_done))
    if pressed and partial:
        info = ("Not built: {} was on Item Access, so Grasshopper split the lines over separate runs. It is now set "
                "to List Access - press the button again.".format(", ".join(partial)))
        gh_message("warning", info)
    elif not pressed:
        info = "Idle. Nothing is read or computed until you press the button."
        gh_status(mem_get("lu_status") or "v40 · idle")              # v27: version and last total time stay shown
        if changing:
            info += "\nSetting the component up: " + ", ".join(changing) + "."
        if last:
            info += "\n\nLast build ({}{}; full report in {}):\n".format(
                last.get("when", "time not recorded"), ", {:.0f} s".format(last["secs"]) if last.get("secs") else "",
                log_file_path()) + last["info"]
            out_ = mem_get("lu_last_out") or last.get("out")
            if out_:
                drawings, names, footprints, floors, uses, cuts = out_
            for ln in last["info"].split("\n"):
                if ln.startswith("WARNING"):
                    gh_message("warning", ln[9:])
    else:
        try:
            fpts = None
            FRAME_C = as_curve(FRAME_IN)
            _SITE_FALLBACK.clear()
            if FRAME_C is None and picks_missing("frame", FRAME_IN):    # v17: the picked frame is not in this file
                alt_ = doc_layer_curves("site alan", True)
                if len(alt_) == 1:
                    FRAME_C = alt_[0]
                    LOG.append("WARNING: the curve picked for frame is not in this Rhino file; the closed curve on the "
                               "layer 'site alan' was used instead (re-pick frame to choose another).")
                elif not alt_:                               # v20: the course file has no frame
                    _SITE_FALLBACK["frame"] = True
                    LOG.append("WARNING: the curve picked for frame is not in this Rhino file and no layer 'site alan' "
                               "holds one; the frame recorded from Nilnoktali-BERGAMA_layerekli.3dm was used "
                               "(SITE_FRAME_LK; pick a frame to choose another).")
            if FRAME_IN is not None and FRAME_C is None:
                LOG.append("WARNING: the frame input could not be read as a curve (it arrived as {}) and was "
                           "ignored.".format(type(FRAME_IN).__name__))
            if FRAME_C is not None:
                fpts = curve_points(FRAME_C)
                if len(fpts) > 3 and math.hypot(fpts[0][0] - fpts[-1][0], fpts[0][1] - fpts[-1][1]) < 1e-6:
                    fpts = fpts[:-1]
                distinct = set((round(p[0], 3), round(p[1], 3)) for p in fpts)
                if not FRAME_C.IsClosed or len(distinct) < 3:
                    LOG.append("WARNING: the frame input is an open line, not a closed area, so it was ignored and the "
                               "analysis range used (a section line belongs in one of the section inputs).")
                    fpts = None
            FRAME_FROM_LAYER[0] = False
            if fpts is None and FRAME_C is None:          # v36: nothing wired = the closed curve on layer site_alan
                for c_ in doc_layer_curves("site alan"):
                    q_ = curve_points(c_)
                    if len(q_) >= 3 and math.hypot(q_[0][0] - q_[-1][0], q_[0][1] - q_[-1][1]) <= 5.0:
                        if math.hypot(q_[0][0] - q_[-1][0], q_[0][1] - q_[-1][1]) < 1e-6:
                            q_ = q_[:-1]
                        fpts, FRAME_FROM_LAYER[0] = q_, True
                        LOG.append("Frame: the closed curve on layer site_alan of this file (the analysis range).")
                        break
                if fpts is None:
                    LOG.append("Frame: no closed curve on layer site_alan; the recorded site frame SITE_FRAME_LK was used.")
            RAWu = read_rhino(None)                       # the whole file: alignment and fallbacks need it
            STUDY_RAW.clear()
            STUDY_RAW.update(read_rhino(None, STUDY_LAYERS))   # v19: the group's study areas, read only
            del FOCUS_PTS_USER[:]
            fc = as_curve(FOCUS_IN)
            if fc is not None:
                FOCUS_PTS_USER.extend(curve_points(fc))
            del WATER_PTS_USER[:]
            for k_, p_ in enumerate(as_list(WATER_LEVELS_IN)):     # v16.5: points on the water surface
                try:
                    WATER_PTS_USER.append((float(p_.X), float(p_.Y), float(p_.Z)))
                except Exception:
                    LOG.append("water_levels item {} skipped: not a point.".format(k_ + 1))
            del NOISE_PTS_USER[:]
            del NOISE_DB_PAIRED[:]
            pts_in, dbs_in = as_list(NOISE_PTS_IN), as_list(NOISE_DB_IN)
            for k_, p_ in enumerate(pts_in):                  # each point with the value at the same place in noise_db
                try:
                    xy = (float(p_.X), float(p_.Y))
                except Exception:
                    xy = None
                db = to_float(dbs_in[k_], None) if k_ < len(dbs_in) else None
                if xy is None or db is None:
                    LOG.append("noise point {} skipped: {}.".format(k_ + 1, "not a point" if xy is None else
                                                                      "no number at the same place in noise_db"))
                    continue
                NOISE_PTS_USER.append(xy)
                NOISE_DB_PAIRED.append(db)
            if len(dbs_in) > len(pts_in):
                LOG.append("noise_db has {} values for {} noise points: the extra values were ignored.".format(
                    len(dbs_in), len(pts_in)))
            lk_lines = []                                     # v20: inputs given the recorded section lines
            if not SEC_IN and picks_missing("section_lines", SEC_IN):  # v17: the picked lines are not in this file
                SEC_IN[:] = doc_layer_curves("sec_lines", False)
                if SEC_IN:
                    LOG.append("WARNING: the lines picked for section_lines are not in this Rhino file; the {} lines on "
                               "the layer 'sec_lines' were used instead (re-pick to choose others).".format(len(SEC_IN)))
                else:
                    _SITE_FALLBACK["section_lines"] = True
                    lk_lines.append("section_lines")
            for k_ in TSEC_KEYS:
                if not TSEC_IN[k_] and picks_missing(k_, TSEC_IN[k_]):
                    alt_ = doc_layer_curves("sec_lines", False)
                    if alt_:
                        TSEC_IN[k_] = alt_
                        LOG.append("WARNING: the lines picked for {} are not in this Rhino file; the {} lines on the "
                                   "layer 'sec_lines' were used instead.".format(k_, len(alt_)))
                    else:
                        _SITE_FALLBACK[k_] = True
                        lk_lines.append(k_)
            if lk_lines:
                LOG.append("WARNING: the lines picked for {} are not in this Rhino file and no layer 'sec_lines' holds "
                           "any; the {} section lines recorded from Nilnoktali-BERGAMA_layerekli.3dm were used "
                           "(SECTION_LINES_LK; pick lines to choose others).".format(", ".join(lk_lines),
                                                                                   len(SECTION_LINES_LK)))
            secs = read_lines("section_lines", SEC_IN)
            tsecs = dict((k, read_lines(k, v)) for k, v in TSEC_IN.items())
            _t_pipe = __import__("time").time()
            SITE, BOARD, RECTS = pipeline(RAWu, fpts, secs, OSM_PATH, PLACES_PATH, tsecs)
            _t_lay = sum(s_ for nm_, s_ in DRAWING_TIMES)
            _t_site = max(0.0, __import__("time").time() - _t_pipe - _t_lay)
            _t_b0 = __import__("time").time()
            n = bake(BOARD) if BAKE_RHINO else 0               # v29: no Rhino bake unless bake = True
            _t_bake = (__import__("time").time() - _t_b0) if BAKE_RHINO else None
            if PDF_EXPORT:                                    # v28: vector PDFs; v29: one single-page board per group
                try:
                    _np, _bad = export_pdfs(BOARD, RECTS)
                    LOG.append("PDF: {} drawings on {} boards (one page each), vector, 1:{:,}, in {}.".format(
                        len(RECTS), _np, int(PDF_SCALE), pdf_folder()))
                    for p_, s_ in export_axonometrics(SITE):      # v33: S1 as an axonometric
                        LOG.append("PDF: {}  {:.0f} s".format(os.path.basename(p_), s_))
                    if _bad:
                        LOG.append("WARNING: PDF not written for: " + "; ".join(_bad[:6]))
                except Exception as ex_:
                    LOG.append("WARNING: PDF export failed ({}); the bake is done.".format(ex_))
            try:                                              # v40: the booklet crops of the sheets (CROP_SPEC)
                booklet_export(SITE, BOARD, RECTS)
            except Exception:
                LOG.append("WARNING: the booklet assets were not written (the board is done):\n" + traceback.format_exc())
            T = SITE.T
            names = [nm for nm, r in RECTS]
            drawings = [_crv(rect(r[0], r[1], r[2], r[3]), True) for nm, r in RECTS]
            for u in SITE.bld:
                for P in u["parts"]:
                    footprints.append(_crv([T_apply(T, x, y) for x, y in P], True))
                    floors.append(u["floors"])
                    uses.append(short(CAT[u["cat"]][0]))
            cuts = [_crv([T_apply(T, x0, y0), T_apply(T, x1, y1)]) for x0, y0, x1, y1, nm in getattr(SITE, "sec_lines", [])]
            info = align_note(T) + "\n" + (tech_report(SITE) if RUN_MODE == "technical" else report(SITE)) + \
                ("\nBaked {} styled objects ({}). Zoom Extents: they sit right of the drawing." if BAKE_RHINO else
                 "\nNothing baked into Rhino (v29; {} 0 objects); the drawings are in the PDFs.").format(
                    n, {"board": {"both": "pages + separate drawings", "pages": "pages", "drawings": "separate drawings"}[LAYOUT],
                        "technical": "technical sheets", "all": "board + technical sheets"}[RUN_MODE])
            if not OSM_PATH:
                info += "\nNo osm_path: streets, paths, green areas and the stream come from the survey only."
            if not PLACES_PATH:
                info += "\nNo places_path: shops are read from OSM points only."
            if LOG:
                info += "\n\n" + "\n".join(LOG)
            for msg in LOG:
                if msg.startswith("WARNING"):
                    gh_message("warning", msg[9:])
            gh_message("remark", "Baked {} objects. Zoom Extents: the pages sit right of the drawing.".format(n)
                       if BAKE_RHINO else "PDFs written to {} (nothing baked into Rhino).".format(pdf_folder()))
            _secs = __import__("time").time() - _t_build
            info = run_head(_secs, len(RECTS), True, _t_site, _t_bake, n) + "\n" + info     # v27
            save_last(info, (drawings, names, footprints, floors, uses, cuts), _secs)
        except Exception as ex:
            info = "ERROR\n" + traceback.format_exc()
            if LOG:
                info += "\n\n" + "\n".join(LOG)
            info = run_head(__import__("time").time() - _t_build, 0, False) + "\n" + info      # v27
            try:
                tb_ = traceback.extract_tb(ex.__traceback__)
                fr = [f_ for f_ in tb_ if f_.filename == tb_[0].filename][-1]     # the last line of this script
                where = " (script line {}, in {})".format(fr.lineno, fr.name)
            except Exception:
                where = ""
            # a warning, not an error: Grasshopper drops a component's outputs on an error, which hid this report
            gh_message("warning", "Build failed: {}: {}{}. The full report is on the log output.".format(
                type(ex).__name__, ex, where))
            save_last(info, ([], [], [], [], [], []), __import__("time").time() - _t_build)
preview = drawings
log = info                                           # v37: the log output (Aras 25 Oct 09:34)
print(info)                  # 25 Oct 12:15: the canvas's log output is Grasshopper's "out" (printed text): print on every solve
if HAVE_RHINO and globals().get("pressed"):
    mem_set("lu_done", done_text(True, not globals().get("partial") and "ERROR" not in str(mem_get("lu_status") or ""),
                                 __import__("time").time() - _T_START))
done = mem_get("lu_done", "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
