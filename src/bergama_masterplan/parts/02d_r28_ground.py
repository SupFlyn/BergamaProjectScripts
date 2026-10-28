# ---- MIRAQUA round 28 Oct 2026 (masterplan v27): p.21 open ground and p.23 the masterplan, each ONE strip; the frame
# area (G10); the open ground for the site board's filter sheet (D1) (worker MP-plan). Shared pieces: common/r28_style.py,
# common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v27 (MIRAQUA 28 Oct, MP-plan). Both pages are crops drawn for the booklet panel (BK_W x BK_H = 392 x 238 mm) at 1:1:
#   * G7: the whole analysis frame (site_alan, 2,845 x 529 m) as ONE strip at 1:10,000 (284.5 x 52.9 mm; 1:5,000 would
#     need 569 mm), the water left to right, at the top-left; no halves, no "continues below".
#   * G8: the study area (calisma_alan, both parts) in R28_STUDY_LINE on both, R28_STUDY_NAME in the legend; the strip's
#     edge is the analysis frame, named (R28_FRAME_NAME) only on p.21, where figures are counted over it.
#   * G10: ONE frame figure, the frame polygon's area; the grid counts only cells whose centre lies inside the frame
#     (pl28_frame_stats); every figure on p.21 and in r28_open_ground.json comes from that one count.
#   * P21.1: every open-ground category in its own R28_OPEN colour, the no-plant-cover hatch too; bars in the map's
#     colours.
#   * P23.1 / P23.2: the numbered markers in their R28_MARKERS group colour, placed by common/label_place.py (G4); the
#     list under the strip by group: coloured number, name, one short line. The reasons and source codes go to the
#     booklet's sources page (blocks.json and booklet/results.json "plan_sources"). The areas left as they are (no
#     intervention) get a grey letter on the plan and one line in the list (their two-line notes do not fit at
#     1:10,000).
#   * D1: the masterplan runs before the site board (RUN_GUIDE §2): the site board draws the filter sheet (drw_filter)
#     from r28_open_ground.json, written here next to masterplan_results.json.
PL28_BAND = 8.0                  # mm above and below the strip where a marker may sit, on a leader (p.23)
PL28_TS, PL28_HEAD_TS = 2.65, 2.82   # booklet label 7.5 pt and kicker 8 pt (PLAN §2), mm
PL28_COLS = (0.0, 99.0, 198.0, 297.0)   # the four columns of the list and the figures, mm from the crop's left
PL28_COL_W = 92.0                # one column, mm (7 mm gutters; the last runs to the crop's right edge)
PL28_TOP = 150.0                 # top of the list / the figures, mm from the crop's foot (under the scale bar row)
PL28_MARKS = (0.0, 100.0, 200.0, 500.0)   # the scale bar at 1:10,000, m (50 mm)
PL28_NI_R = 1.6                  # the letters of the areas left as they are, radius mm
PL28_OPEN_JSON = "r28_open_ground.json"   # D1: in cached/bergama_masterplan/, beside masterplan_results.json
PL28_HUB = {u"K4": u"K4 · Ulucami Önü", u"K3": u"K3 · Tabak", u"İstiklal": u"İstiklal Meydanı",
            u"Kızıl Avlu": u"Kızıl Avlu", u"K5": u"K5 · Üç Kemer", u"K6": u"K6"}   # list names (HUB_NAME, sentence case)
PL28_SRC_TAG = re.compile(u"\\s*\\((survey|satellite 2021|satellite check)\\)")   # source tags of the no-go reasons
PL28_SRC_NAME = {u"survey": u"survey (Bergama_Altlik.3dm)", u"satellite 2021": u"ESA WorldCover 2021",
                 u"satellite check": u"satellite check (OPEN_CHECK)"}


# ---------------------------------------------------------------- G10: one frame figure
def pl28_frame_stats(C):
    """v27 (MIRAQUA 28 Oct, G10): C.frame_m2 = the frame polygon's area (shoelace: 150.52 ha for site_alan, the figure
    the site board prints on p.02); C.inF = 1 for each grid cell whose centre lies inside the frame (the grid
    overshoots it by up to one cell on each axis, which made 151 ha); each such cell stands for frame area / cells
    inside (C.cell_m2, within 0.3 % of c x c), so C.stats {0 open, 1 building, 2 road, 3 bed: m2} adds up to the
    frame exactly. One pass over the grid (was four)."""
    G, V, F = C.G, C.V, C.F
    P = list(getattr(V, "frame_P", None) or V.P)          # build_all sets V.frame_P = site_alan
    inF = bytearray(C.N)
    for n in G.poly_cells([V.uv(p) for p in P]):
        inF[n] = 1
    C.frame_m2 = abs(area2(P))
    C.inF = inF
    C.cell_m2 = C.frame_m2 / float(inF.count(1) or 1)
    Fin = bytes(v if i else 9 for v, i in zip(F, inF))
    C.stats = dict((k_, Fin.count(k_) * C.cell_m2) for k_ in (0, 1, 2, 3))


# ---------------------------------------------------------------- G7 / G8: the strip and the study area
def pl28_strip(C, k):
    """v27 (G7): the whole analysis frame as ONE strip, the water left to right (View: the upstream end at u0): T
    (world -> strip mm, y up), inP (world point on the strip), its size dw x dh mm."""
    V = C.V

    def T(p):
        u, v = V.uv(p)
        return (u - V.u0) * k, (v - V.v0) * k

    def inP(p):
        u, v = V.uv(p)
        return V.u0 <= u <= V.u1 and V.v0 <= v <= V.v1
    return {"T": T, "inP": inP, "dw": (V.u1 - V.u0) * k, "dh": (V.v1 - V.v0) * k}


def pl28_study(C):
    """G8: the study area's outlines (calisma_alan, both parts; build_all sets V.study), survey m."""
    return [list(P) for P in (getattr(C.V, "study", None) or []) if len(P) >= 3]


def pl28_draw_study(pg, C, T):
    """G8: the study area outline in R28_STUDY_LINE (dash-dot) on a plan page; True when drawn."""
    st = R28_STUDY_LINE
    rs = pl28_study(C)
    for P in rs:
        Q = [T(p) for p in P]
        pg.line(Q + Q[:1], st["colour"], st["width_mm"], list(st["dash_mm"]), cap=0)
    return bool(rs)


def pl28_sw_study():
    """G8: the study area's legend sample."""
    return _sw_line(R28_STUDY_LINE["colour"], R28_STUDY_LINE["width_mm"], list(R28_STUDY_LINE["dash_mm"]))


def pl28_runs(sh, x, y, runs, size, colour):
    """One line of text in runs [(text, bold)] (G5: the bold keyword inside a line); returns its end x."""
    for t, bd in runs:
        if t:
            sh.text(t, x, y, size, colour, bold=bd)
            x += text_w(t, size, bd)
    return x


def pl28_marks(sh, C, x0, y0):
    """v27: the row under a strip, from (x0, y0) up (10 mm): the north arrow (survey +Y turned with the plan), the
    1:10,000 scale bar right beside it (SCRIPT_STANDARD §8: next to every orthogonal drawing) and which way the water
    flows."""
    V = C.V
    nu, nv = V.uv((V.cx, V.cy + 1.0))
    L = math.hypot(nu, nv) or 1.0
    nx_, ny_ = nu / L, nv / L
    ax, ay = x0 + 3.5, y0 + 5.0
    tip = (ax + nx_ * 3.5, ay + ny_ * 3.5)
    sh.poly([[tip, (ax - ny_ * 1.6 - nx_ * 3.0, ay + nx_ * 1.6 - ny_ * 3.0), (ax - nx_ * 1.8, ay - ny_ * 1.8)]],
            fill=COL["ink_dark"])
    sh.poly([[tip, (ax - nx_ * 1.8, ay - ny_ * 1.8), (ax + ny_ * 1.6 - nx_ * 3.0, ay - nx_ * 1.6 - ny_ * 3.0)]],
            fill=COL["white"], stroke=COL["ink_dark"], lw=0.15)
    sh.text(u"N", tip[0] + 1.2, tip[1] - 0.6, 2.6, COL["ink_dark"], bold=True)
    scale_bar(sh, x0 + 12.0, y0 + 2.0, MP_SCALE, PL28_MARKS)
    xs = x0 + 12.0 + PL28_MARKS[-1] * 1000.0 / MP_SCALE + 6.0 + text_w(u"1:{:,.0f}".format(MP_SCALE), 3.4, True) + 8.0
    pl28_runs(sh, xs, y0 + 2.0, [(u"the water flows ", False), (u"left to right", True),
                                 (u", the upstream entry at the left end", False)], PL28_TS, COL["ink2"])


def pl28_legend(sh, groups, x0, x1, y_top, y_min, ncols, warn, pitch=3.6):
    """v27: the legend in ncols columns from x0 to x1, top down from y_top to y_min: each group a bold head, then its
    drawn samples with plain names (only what the page draws); a head never ends a column; rows closer (to 3.0 mm)
    when they would not fit."""
    rows = []
    for head, items in groups:
        if items:
            rows += [(head, None)] + list(items)
    if not rows:
        return
    need = int(math.ceil(len(rows) / float(ncols))) + 1
    pitch = max(3.0, min(pitch, (y_top - y_min) / float(need)))
    R = max(2, int((y_top - y_min) / pitch))
    cols, cur = [], []
    for r_ in rows:
        if cur and (len(cur) >= R or (r_[1] is None and len(cur) >= R - 1)):
            cols.append(cur)
            cur = []
        cur.append(r_)
    cols.append(cur)
    if len(cols) > ncols:
        warn.append(u"legend: {} rows do not fit {} columns beside the strip".format(len(rows), ncols))
    cw = (x1 - x0) / float(ncols)
    for c, col in enumerate(cols):
        cx = x0 + c * cw
        for j, (nm, f) in enumerate(col):
            cy = y_top - j * pitch
            if f is None:
                sh.text(nm, cx, cy - 2.6, PL28_TS, COL["ink_dark"], bold=True)
                continue
            f(sh, cx, cy - 2.9, 6.0, 2.4)
            sh.text(nm, cx + 7.5, cy - 2.6, PL28_TS, COL["ink"])
            if text_w(nm, PL28_TS) > cw - 8.5:
                warn.append(u"legend name runs into the next column: {}".format(nm))


# ---------------------------------------------------------------- P23: markers, list, sources
def pl28_note_group(nt):
    """P23.1: the R28_MARKERS group of a numbered note: roads; hubs and transit (the later town bus line too); water
    and ecology (reed basins, terraces, hidden stream, widened stream, side arm, the edges kept); crossings
    (footbridges); heritage and views."""
    k = nt["key"]
    if k[0] == "road":
        return "hubs" if k[1] == TOWN_LINE["name"] else "roads"
    return {"hub": "hubs", "foot": "crossings", "h4": "heritage", "h6": "heritage", "view": "heritage"}.get(k[0], "water")


def pl28_note_entry(C, nt):
    """P23.2: (name, one short line) of a numbered note for the list, in plain words from the note's own data. No
    source codes: they go to the sources page with every reason, whole (pl28_plan_sources)."""
    k = nt["key"]
    less = u"less than {:.0f} m open".format(KEPT_MAX)
    if k[0] == "hub":
        h = next((h_ for h_ in C.hubs if h_["id"] == k[1]), {})
        nm = PL28_HUB.get(k[1], k[1])
        if h.get("role") == "transit":
            return nm + u" · transit hub", u"town bus lines stop here · " + (
                u"square over the culvert" if k[1] == u"İstiklal" else u"by the Red Hall tunnels")
        if k[1] == u"K6":
            return nm + u" · gateway out", u"the primary road is kept · bus stop {} {:.0f} m".format(
                h.get("stop", u""), h.get("stop_m", 0.0))
        extra = {u"K3": u" · workshops, education", u"K5": u" · Demeter's Garden"}.get(k[1], u"")
        sub = u", sub-hub in the bed" if h.get("sub_xy") else u""
        return nm + u" · walking hub", (u"dry square" if extra else u"dry square at the Roman bridge") + sub + extra
    if k[0] == "road":
        if k[1] == TOWN_LINE["name"]:
            return u"Town bus line to K4 · later step", u"on the existing streets from İstiklal to the K4 stop"
        rd = next((r_ for r_ in ROADS if r_["name"] == k[1]), None)
        if rd is not None:
            ch, _, rest = rd["note"].partition(u": ")
            return u"{}{} · {}".format(rd["name"][:1].upper(), rd["name"][1:], ch), rest
    if k[0] == "kept":
        return {"building": (u"Edge kept · buildings", u"buildings stand at the bank, " + less),
                "road": (u"Edge kept · road", u"a road runs at the bank, " + less),
                "frame": (u"Nothing placed", u"the edge of the analysis frame, " + less)}.get(
            k[1], (nt["text"][:1] + nt["text"][1:].lower(), less))
    if k[0] == "view" and C.terrace:
        return u"Viewing terrace", u"a clear sightline to the Trajaneum, {:,.0f} m away".format(C.terrace["d"])
    if k[0] == "widen" and C.widen:
        lo, hi = min(w["fw"][0] for w in C.widen), max(w["fw"][1] for w in C.widen)
        return u"Stream widened", u"room for water and a wetland · {:.0f}-{:.0f} m open beside the bank".format(lo, hi)
    if k[0] == "foot":
        return u"Footbridge" + (u"s" if len(nt["at"]) > 1 else u""), \
            u"{:.0f}+ m of stream without a crossing · both landings open".format(FOOT_GAP_M)
    fixed = {"h4": (u"Step to the water", u"facing Tabaklar Hamamı, a bath ruin 1.5 m from the stream"),
             "h6": (u"Deck over the Roman bank wall", u"a Roman complex with a bank wall of about 120 m"),
             "wt": (u"Reed basins", u"the water is cleaned once · clean-water classroom"),
             "terr": (u"Rain terraces on the contours", u"they hold the rain · overflow to the reed basins"),
             "cov": (u"Hidden stream", u"nothing opened: the water line drawn in the paving"),
             "arm": (u"Reed side arm", u"a reed channel cleans the return water")}
    return fixed.get(k[0], (nt["text"][:1] + nt["text"][1:].lower(), u""))


def pl28_letter(i):
    return u"abcdefghijklmnopqrstuvwxyz"[i] if i < 26 else str(i + 1)


def pl28_spot(x, y, s, taken, bounds, rank):
    """G4: a free s x s box near (x, y): label_spot (common/label_place.py) on the boxes within its reach; else for a
    rank-0 marker the nearest free spot anywhere in bounds, on a leader (place_labels_all); None when there is none."""
    R = 32.0                                             # label_spot's farthest ring (24 mm) + the box + its leader
    near = [t for t in taken if t[2] > x - R and t[0] < x + R and t[3] > y - R and t[1] < y + R]
    got = label_spot(x, y, s, s, near, bounds, pad=0.3)
    if got:
        return got[0]
    if rank:
        return None
    got = place_labels_all([{"x": x, "y": y, "wh": lambda f: (s, s), "rank": 0}], list(taken), bounds, sizes=(1.0,),
                           pad=0.3).get(0)
    return got[0] if got else None


def pl28_plan_markers(sh, C, T, inP, taken, bounds):
    """P23.1 (G4): the numbered markers in their group's colour at each note's places on the strip (the first place
    must show, more places may drop), then a grey letter for each area left as it is (no intervention), on free
    spots (pl28_spot: rings round the point, a thin leader in the marker's colour when moved; the bands above and
    below the strip may hold a marker). Returns (entries, letters): [[note, group, name, line, placed]],
    [[letter, region, placed]]; a lettered region gets r_["placed"]."""
    r, rn = BADGE_R, PL28_NI_R
    mk = dict((k_, hx) for k_, lab, hx in R28_MARKERS)
    items, ents, nis = [], [], []                       # items: (x, y, radius, rank, kind, label, colour, owner)
    for nt in sorted(C.notes, key=lambda nt_: nt_["n"]):
        grp = pl28_note_group(nt)
        nm, line = pl28_note_entry(C, nt)
        ents.append([nt, grp, nm, line, False])
        first = True
        for p in nt["at"]:
            if inP(p):
                x, y = T(p)
                items.append((x, y, r, 0 if first else 1, "n", str(nt["n"]), mk[grp], ents[-1]))
                first = False
    for i, r_ in enumerate(C.nogo):
        nis.append([pl28_letter(i), r_, False])
        p = next((q for q in r_["at"] if inP(q)), None)
        if p is not None:
            x, y = T(p)
            items.append((x, y, rn, 0, "ni", nis[-1][0], COL["ink2"], nis[-1]))
    for i in sorted(range(len(items)), key=lambda i_: items[i_][3]):
        x, y, rr, rank, kind, lab, col, own = items[i]
        b = pl28_spot(x, y, 2.0 * rr, taken, bounds, rank)
        if b is None:
            continue
        taken.append(b)
        cx, cy = (b[0] + b[2]) / 2.0, (b[1] + b[3]) / 2.0
        d = math.hypot(cx - x, cy - y)
        if d > rr + 0.4:                                 # the leader from the place to the marker's edge
            sh.line([(x, y), (cx - (cx - x) / d * rr, cy - (cy - y) / d * rr)], col, 0.18)
            sh.circle(x, y, 0.35, fill=col)
        if kind == "n":
            sh.circle(cx, cy, rr + 0.25, fill=COL["white"])
            sh.circle(cx, cy, rr, fill=col)
            sh.text(lab, cx, cy - BADGE_TS * 0.36, BADGE_TS, COL["white"], bold=True, align="C")
            own[4] = True
        else:
            sh.circle(cx, cy, rr, fill=COL["white"], stroke=col, lw=0.2)
            sh.text(lab, cx, cy - KEY_MIN * 0.36, KEY_MIN, col, bold=True, align="C")
            own[2] = True
            own[1]["placed"] = own[1].get("placed", 0) + 1
    return ents, nis


def pl28_list_head(sh, lab, col, x, y, cw):
    """a group's head in the list: its name in its colour, bold, over a hairline; returns the y under it"""
    y -= PL28_HEAD_TS * 1.18
    sh.text(lab, x, y + PL28_HEAD_TS * 0.2, PL28_HEAD_TS, col, bold=True)
    y -= 1.3
    sh.line([(x, y), (x + cw, y)], col, 0.2, alpha=0.5)
    return y - 2.6


def pl28_list_nogo(sh, nis, x, y, cw):
    """the areas left as they are: grey letter, its size in ha (G13) in bold, why (its source tag goes to the
    sources page); returns the y under it"""
    y = pl28_list_head(sh, u"Left as it is · no intervention", COL["ink2"], x, y, cw)
    rn, tx = PL28_NI_R, x + 2 * BADGE_R + 2.2
    for lt, r_, ok in nis:
        sh.circle(x + BADGE_R, y - rn, rn, fill=COL["white"], stroke=COL["ink2"], lw=0.2)
        sh.text(lt, x + BADGE_R, y - rn - KEY_MIN * 0.36, KEY_MIN, COL["ink2"], bold=True, align="C")
        ha = u_area(r_["ha"] * 1e4, "ha")
        yy = y - PL28_TS * 1.18
        x1 = pl28_runs(sh, tx, yy + PL28_TS * 0.2, [(ha, True), (u" · ", False)], PL28_TS, COL["ink"])
        for i, s_ in enumerate(wrap(PL28_SRC_TAG.sub(u"", r_["why"]), PL28_TS, max(20.0, x + cw - x1))):
            if i:
                yy -= PL28_TS * 1.18
            sh.text(s_, x1, yy + PL28_TS * 0.2, PL28_TS, COL["ink2"])
        y = min(yy, y - 2 * rn) - 1.6
    return y


def pl28_plan_list(sh, ents, nis, y_top, warn):
    """P23.2: the list under the strip, by group in the markers' order and colours, in four columns (roads | hubs and
    transit | water and ecology | crossings, heritage and views, the areas left as they are): each entry the coloured
    number, its name in bold, one short line in a lighter grey; airy (2.6 mm between entries, 3.4 mm between
    groups)."""
    mk = dict((k_, (lab, hx)) for k_, lab, hx in R28_MARKERS)
    cols = (("roads",), ("hubs",), ("water",), ("crossings", "heritage", "nogo"))
    r = BADGE_R
    for ci, keys in enumerate(cols):
        x = PL28_COLS[ci]
        cw = (BK_W - x) if ci == len(cols) - 1 else PL28_COL_W
        tx, y = x + 2 * r + 2.2, y_top
        for key in keys:
            if key == "nogo":
                y = pl28_list_nogo(sh, nis, x, y, cw) if nis else y
                continue
            rows = [e for e in ents if e[1] == key]
            if not rows:
                continue
            lab, col = mk[key]
            y = pl28_list_head(sh, lab, col, x, y, cw)
            for nt, grp, nm, line, ok in rows:
                sh.circle(x + r, y - r, r, fill=col)
                sh.text(str(nt["n"]), x + r, y - r - BADGE_TS * 0.36, BADGE_TS, COL["white"], bold=True, align="C")
                yy = y
                for s_ in wrap(nm, PL28_HEAD_TS, cw - (tx - x), True):
                    yy -= PL28_HEAD_TS * 1.18
                    sh.text(s_, tx, yy + PL28_HEAD_TS * 0.2, PL28_HEAD_TS, COL["ink"], bold=True)
                for s_ in (wrap(line, PL28_TS, cw - (tx - x)) if line else []):
                    yy -= PL28_TS * 1.18
                    sh.text(s_, tx, yy + PL28_TS * 0.2, PL28_TS, COL["ink2"])
                y = min(yy, y - 2 * r) - 2.6
            y -= 3.4
        if y < 1.0:
            warn.append(u"masterplan list: column {} runs {:.1f} mm below the crop".format(ci + 1, 1.0 - y))


def pl28_src_kind(s):
    """N2 / F5 hint for the booklet's sources page: "public online" (OSM, its bus stops, ESA WorldCover, DSI, EPA),
    "project note" (history cards h01-h03, decisions D/H, register codes P/E), else "booklet analysis" (survey, open
    ground, edge plan, water board cuts, city link)."""
    if re.search(u"\\bOSM\\b|WorldCover|satellite 2021|\\bDSI\\b|\\bEPA\\b|bus stop", s):
        return u"public online"
    if re.search(u"\\b(h0\\d|H\\d|D\\d{1,2}|P\\d{2}|E\\d{2})\\b", s):
        return u"project note"
    return u"booklet analysis"


def pl28_plan_sources(ents, nis):
    """P23.2 / N2: what the list no longer prints, for the booklet's sources page, keyed by the marker numbers (and
    letters) on the masterplan page: every reason of every note, whole, with a kind hint (pl28_src_kind)."""
    return {"crop": "mp_plan", "heading": u"Masterplan: what each numbered move stands on",
            "markers": [{"n": nt["n"], "group": grp, "name": nm, "line": line,
                         "sources": [{"text": s_, "kind": pl28_src_kind(s_)} for s_ in nt["why"]]}
                        for nt, grp, nm, line, ok in ents],
            "left_as_is": [{"id": lt, "ha": round(r_["ha"], 2), "why": PL28_SRC_TAG.sub(u"", r_["why"]),
                            "sources": [PL28_SRC_NAME.get(m_, m_) for m_ in PL28_SRC_TAG.findall(r_["why"])]}
                           for lt, r_, ok in nis]}


# ---------------------------------------------------------------- the two pages
def plan_page(C, warn):
    """v27 (MIRAQUA 28 Oct, P23.1-P23.3, G4, G7, G8): the masterplan page (crop mp_plan). Top-left ONE strip of the
    whole analysis frame at 1:10,000 (284.5 x 52.9 mm, PL28_BAND above and below for markers) with every layer of the
    corridor and the study area outline; the numbered markers in their group's colour (R28_MARKERS); the scale bar
    row under the strip; the legend beside it (from COL_X, two columns); under them, from PL28_TOP, the list by group
    in four columns. The reasons and source codes go to the sources page (sh.plan_sources -> plan_sources)."""
    k = 1000.0 / MP_SCALE
    g = pl28_strip(C, k)
    T, inP, dw, dh = g["T"], g["inP"], g["dw"], g["dh"]
    W, H = BK_W, BK_H
    if dw > COL_X - 6.0 or dh > 60.0:
        warn.append(u"the analysis frame at 1:{:,.0f} ({:.0f} x {:.0f} mm) is larger than the strip's room".format(
            MP_SCALE, dw, dh))
    taken = [b for P in pl28_study(C) for b in boxes_along([T(p) for p in P + P[:1]], 1.2)]   # G4: names keep off it
    pg = Page(dw, dh)
    used, _ = draw_corridor(pg, T, k, C, inP, taken, dw, dh)
    if pl28_draw_study(pg, C, T):
        used.add("study")
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    x0, y0 = 0.0, H - PL28_BAND - dh
    sh.clip([rect(x0, y0, x0 + dw, y0 + dh)])
    blit(sh, pg, x0, y0)
    sh.unclip()
    sh.poly([rect(x0, y0, x0 + dw, y0 + dh)], stroke=COL["ink2"], lw=0.25, alpha=0.45)   # the strip's edge = the frame
    Ts = lambda p: (T(p)[0] + x0, T(p)[1] + y0)
    tk = [(b[0] + x0, b[1] + y0, b[2] + x0, b[3] + y0) for b in taken]
    ents, nis = pl28_plan_markers(sh, C, Ts, inP, tk, (x0, y0 - PL28_BAND, x0 + dw, y0 + dh + PL28_BAND))
    for nt, grp, nm, line, ok in ents:
        if not ok:
            warn.append(u"masterplan note {} not placed on the plan (no free spot): {}".format(nt["n"], nt["text"]))
    y_row = y0 - PL28_BAND - 10.0
    pl28_marks(sh, C, x0, y_row)
    pl28_legend(sh, [(u"EXISTING · SURVEY", [(nm, f) for key, nm, f in LEGEND_V24 if key in used and key in EXISTING]),
                     (u"PROPOSED", [(nm, f) for key, nm, f in LEGEND_V24 if key in used and key not in EXISTING])],
                COL_X, W, H, y_row, 2, warn)
    pl28_plan_list(sh, ents, nis, PL28_TOP, warn)
    sh.crop = (0.0, 0.0, W, H)
    sh.key, sh.world, sh.scale, sh.pleg = "plan", bbox(C.V.P), MP_SCALE, None
    sh.bid = ("mp_plan", "c1_s1", u"Masterplan: the ecological corridor of the whole {}".format(R28_FRAME_NAME.lower()))
    sh.plan_sources = pl28_plan_sources(ents, nis)
    C.ni_placed = sum(1 for r_ in C.nogo if r_.get("placed"))
    return sh


def pl28_chart(sh, x, y, w, head, runs, rows):
    """v27 (P21.1): one bar chart in the map's colours: head, one line (G5: bold keyword), bars [(name, m2, fill,
    stripes)] scaled to the largest, values in ha (G13); returns the y under it."""
    y -= PL28_HEAD_TS * 1.18
    sh.text(head, x, y + 0.5, PL28_HEAD_TS, COL["ink_dark"], bold=True)
    y -= PL28_TS * 1.3
    pl28_runs(sh, x, y + 0.5, runs, PL28_TS, COL["ink2"])
    y -= 1.5
    vmax = max([a for _, a, _, _ in rows] + [1.0])
    lab, room = 44.0, w - 44.0 - 20.0
    for nm, a, fill, stripes in rows:
        y -= 5.2
        sh.text(nm, x, y + 0.75, PL28_TS, COL["ink"])
        bw = max(0.3, room * a / vmax)
        sh.poly([rect(x + lab, y, x + lab + bw, y + 3.4)], fill=fill, stroke=COL["ink2"], lw=0.1, stripes=stripes)
        sh.text(u_area(a, "ha"), x + lab + bw + 1.5, y + 0.75, PL28_TS, COL["ink"], bold=True)
    return y


def ground_page(C, warn):
    """v27 (MIRAQUA 28 Oct, P21.1, P21.2, G7, G8, G10): the open ground (crop mp_max_area; p.21, used when D1 = keep).
    Top-left ONE strip of the analysis frame at 1:10,000, crisp (it is analysis), each category in its own R28_OPEN
    colour (the no-plant-cover hatch too), the study area outline; the scale bar row under it, the legend beside it;
    under them, from PL28_TOP, the figures in the map's colours, all from ONE count (pl28_frame_stats: the frame
    polygon's area, cells inside the frame): the frame's split as one bar across the page, the open ground by distance
    from the water and by land cover on the satellite, the satellite check."""
    k = 1000.0 / MP_SCALE
    g = pl28_strip(C, k)
    T, dw, dh = g["T"], g["dw"], g["dh"]
    O = R28_OPEN
    hatch, since = (O["noplant_hatch"], 0.9, 0.18, 45.0), (COL["ink_dark"], 0.8, 0.2, 45.0)
    W, H = BK_W, BK_H
    pg = Page(dw, dh)
    TL = lambda Ls: [Q for Q in ([T(p) for p in L_] for L_ in Ls) if hit(bbox(Q), (-2.0, -2.0, dw + 2.0, dh + 2.0))]
    pg.poly(TL(C.max_loops), fill=O["open_fill"])
    pg.poly(TL(C.bare_loops), stripes=hatch)
    pg.poly(TL(C.bed_loops), fill=O["stream"])
    for P in C.streams:
        pg.line([T(p) for p in P], COL["river_mid"], 0.15)
    for role in ("building", "housing", "shed", "heritage"):
        pg.poly(TL(C.bld.get(role, [])), fill=O["building"])
    pg.poly(TL(C.built_since), fill=O["building"], stripes=since)
    pg.poly(TL(C.road_loops), fill=O["road"])
    for P in C.bridges:                                  # v27: over the roads (the road fill hid them)
        pg.line([T(p) for p in P], O["bridge"], 0.3)
    study = pl28_draw_study(pg, C, T)
    sh = Page(W, H)
    sh.poly([rect(0, 0, W, H)], fill=COL["paper"])
    x0, y0 = 0.0, H - PL28_BAND - dh                     # the strip where p.23 has it
    sh.clip([rect(x0, y0, x0 + dw, y0 + dh)])
    blit(sh, pg, x0, y0)
    sh.unclip()
    sh.poly([rect(x0, y0, x0 + dw, y0 + dh)], stroke=COL["ink2"], lw=0.25)   # the analysis frame (its figures below)
    y_row = y0 - PL28_BAND - 10.0
    pl28_marks(sh, C, x0, y_row)
    ink, ink2 = COL["ink"], COL["ink2"]
    pl28_legend(sh, [(u"SURVEY · SATELLITE",
                      [(u"Open ground", _sw_fill(O["open_fill"], ink2)),
                       (u"No plant cover (satellite)", _sw_fill(O["open_fill"], ink2, stripes=hatch)),
                       (u"Stream bed", _sw_fill(O["stream"])), (u"Building", _sw_fill(O["building"])),
                       (u"Road", _sw_fill(O["road"], ink2)), (u"Bridge", _sw_line(O["bridge"], 0.3))] +
                      ([(u"Built since survey", _sw_fill(O["building"], stripes=since))] if C.built_since else []) +
                      ([(R28_STUDY_NAME, pl28_sw_study())] if study else []) +
                      [(R28_FRAME_NAME, _sw_line(ink2, 0.25))])], COL_X, W, H, y_row, 1, warn)
    # ---- the figures: ONE count (G10)
    st, tot, F, inF = C.stats, C.frame_m2 or 1.0, C.F, C.inF
    y = PL28_TOP - PL28_HEAD_TS * 1.18
    sh.text(u"{} · {}".format(R28_FRAME_NAME, u_area(tot, "ha")), 0.0, y + 0.5, PL28_HEAD_TS, COL["ink_dark"], bold=True)
    y -= PL28_TS * 1.3
    pl28_runs(sh, 0.0, y + 0.5, [(u"Open ground", True), (u" = no survey building, no survey road ({:.1f} m either side "
                                                          u"of a street edge), not the stream bed · {:.0f} m grid, cells "
                                                          u"inside the frame".format(ROAD_BUF_M, C.G.c), False)],
              PL28_TS, ink)
    y -= PL28_TS * 1.3
    pl28_runs(sh, 0.0, y + 0.5, [(u"Open to change", True), (u" (where we can build) counts only vacant ground, parking "
                                                             u"and yards, and loose ground", False)], PL28_TS, ink2)
    y -= 3.0
    parts = [(u"open ground", O["open_fill"], st[0]), (u"stream bed", O["stream"], st[3]),
             (u"buildings", O["building"], st[1]), (u"roads", O["road"], st[2])]
    xa = 0.0
    for nm, fill, a in parts:                            # the frame's split as one bar across the page
        w_ = W * a / tot
        sh.poly([rect(xa, y - 7.0, xa + w_, y)], fill=fill, stroke=ink2, lw=0.1)
        xa += w_
    y -= 8.8
    for i, (nm, fill, a) in enumerate(parts):
        x = PL28_COLS[i]
        sh.poly([rect(x, y - 2.9, x + 6.0, y - 0.5)], fill=fill, stroke=ink2, lw=0.15)
        pl28_runs(sh, x + 7.5, y - 2.6, [(nm + u" ", False), (u_area(a, "ha"), True),
                                         (u" · {:.0f} %".format(100.0 * a / tot), False)], PL28_TS, ink)
    y -= 3.6 + 8.0
    c2 = C.cell_m2
    by_d, by_lc = [0.0] * 4, {}
    for n in range(C.N):
        if F[n] != 0 or not inF[n]:
            continue
        d = C.Dst[n]
        by_d[0 if d <= 25.0 else (1 if d <= ECO_BANDS[-1] else (2 if d <= DMAX_M else 3))] += c2
        by_lc[C.lc[n]] = by_lc.get(C.lc[n], 0.0) + c2
    of = O["open_fill"]
    y1 = pl28_chart(sh, 0.0, y, 190.0, u"Open ground by distance from the water",
                    [(u"walking", True), (u" through open ground, survey", False)],
                    [(u"0-25 m", by_d[0], of, None), (u"25-{:.0f} m".format(ECO_BANDS[-1]), by_d[1], of, None),
                     (u"{:.0f}-{:.0f} m".format(ECO_BANDS[-1], DMAX_M), by_d[2], of, None),
                     (u"no open way within {:.0f} m".format(DMAX_M), by_d[3], of, None)])
    y2 = pl28_chart(sh, PL28_COLS[2], y, W - PL28_COLS[2], u"Open ground by land cover",
                    [(u"ESA WorldCover 2021", True), (u", satellite, 10 m pixels", False)],
                    [(nm, by_lc.get(code, 0.0), of, hatch if code == 0 else None)
                     for code, nm in ((1, u"cropland"), (5, u"orchards"), (2, u"tree cover"), (3, u"scrub"),
                                      (4, u"grassland"), (0, u"no plant cover"))])
    y = min(y1, y2) - 8.0
    ck = OPEN_CHECK
    y -= PL28_HEAD_TS * 1.18
    if ck.get("imagery"):
        sh.text(u"Satellite check · done", 0.0, y + 0.5, PL28_HEAD_TS, COL["ink_dark"], bold=True)
        s_ = u"{} of {}: {} area{} built on since the survey (dark hatch), out of the open ground".format(
            ck["imagery"], ck.get("date") or u"date not given", len(C.built_since), u"" if len(C.built_since) == 1 else u"s")
    else:
        og = getattr(C, "og_check", {})
        sh.text(u"Satellite check · pending", 0.0, y + 0.5, PL28_HEAD_TS, COL["ink_dark"], bold=True)
        s_ = u"no satellite image could be opened from the cloud (27 Oct 2026) · {} open areas of {:.2f} ha or more to " \
             u"check in Google Earth, {} with no plant cover first (hatched): logs/{}".format(
                 og.get("n", 0), OG_MIN_HA, og.get("flag", 0), OG_KML)
    for ln in wrap(s_, PL28_TS, 190.0):
        y -= PL28_TS * 1.3
        sh.text(ln, 0.0, y + 0.5, PL28_TS, ink2)
    if y < 1.0:
        warn.append(u"open ground page: the figures run {:.1f} mm below the crop".format(1.0 - y))
    sh.crop = (0.0, 0.0, W, H)
    sh.key, sh.world, sh.scale, sh.pleg = "max_area", bbox(C.V.P), MP_SCALE, None
    sh.bid = ("mp_max_area", "mp_max_area", u"Open ground in the {} (survey){}".format(
        R28_FRAME_NAME.lower(), u" · satellite check: {}, {}".format(ck["imagery"], ck.get("date") or u"date not given")
        if ck.get("imagery") else u" · satellite check pending"))
    return sh


# ---------------------------------------------------------------- D1: the open ground for the site board
def pl28_corners(L):
    """a traced cell outline with its straight-through vertices dropped (exact: every step is axis-parallel)"""
    n = len(L)
    out = []
    for i in range(n):
        a, b, c_ = L[i - 1], L[i], L[(i + 1) % n]
        if (b[0] - a[0]) * (c_[1] - b[1]) != (b[1] - a[1]) * (c_[0] - b[0]):
            out.append(b)
    return out


def pl28_open_ground_json(C, path):
    """v27 (MIRAQUA 28 Oct, D1, G10): the masterplan's open ground for the site board's filter sheet (drw_filter; the
    site board runs after the masterplan): {frame_ha (the frame polygon), open_ha, classes {open, building, road, bed:
    {ha, rings}}, definition, cell_m, rings, source}. ha from the ONE count of pl28_frame_stats; rings = the outlines
    of each class's grid cells inside the frame (trace), straight-through vertices dropped, survey m to 0.1 m, holes
    clockwise (fill even-odd). Written compact (no indent). Returns the dict."""
    G, F, V, inF = C.G, C.F, C.V, C.inF
    sets = (set(), set(), set(), set())
    for n in range(C.N):                                 # one pass: the cells inside the frame by class
        if inF[n]:
            sets[F[n]].add(n)
    cls = {}
    for name, code in (("open", 0), ("building", 1), ("road", 2), ("bed", 3)):
        rings_ = []
        for Lp in trace(G, sets[code]):
            Q = pl28_corners(Lp)
            if len(Q) >= 4:
                rings_.append([[round(x, 1), round(y, 1)] for x, y in (V.xy(u, v) for u, v in Q)])
        cls[name] = {"ha": round(C.stats[code] / 1e4, 2), "rings": rings_}
    out = {"frame_ha": round(C.frame_m2 / 1e4, 2), "open_ha": round(C.stats[0] / 1e4, 2), "classes": cls,
           "definition": u"Open ground (masterplan) = every {:.0f} m grid cell of the analysis frame with no survey "
                         u"building, no survey road ({:.1f} m either side of a street edge) and not the stream bed; "
                         u"only cells centred inside the frame count".format(G.c, ROAD_BUF_M),
           "cell_m": round(G.c, 3), "rings": u"survey m; the outlines of each class's grid cells (holes clockwise), "
                                             u"fill even-odd",
           "source": u"{} · {}".format(VERSION, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))}
    with open(path, "w", encoding="utf-8") as f_:
        json.dump(out, f_, ensure_ascii=False, separators=(",", ":"))
    return out
