# ---- 04_items (round 5 S6, 2 Nov 2026; G-R5-12 produce first, compose last; addendum 1 Nov 22:37 point 2) ----------
# The masterplan lays out no page and writes no sheet PDF any more. Its three booklet pages are still DRAWN by the
# round 4 functions into a Page (page mm, y up), but that Page is only a recorder: mpx_drawing() turns the part of it
# that is one drawing into ONE item-export drawing (common/item_export.py Ix), true scale, in the drawing's own metres:
#   x_d = origin_m[0] + (x_mm - box[0]) * den / 1000      (y likewise; den = the scale the panel was drawn at)
# so the booklet (S10) can pick any listed scale. Clip regions are resolved here (the booklet's writer has no clip):
# a rectangle clip cuts polygons (Sutherland-Hodgman) and lines (Liang-Barsky) to it; a non-rectangle clip with one
# ring cuts with sc_rings_clip / sc_lines (study_clip.py); the "outside only" clip of the fade halos (rect + rings,
# even-odd: soft_fill, sn_field) becomes a stroke of HALF the width on the ring offset outward by a quarter of it,
# which is exactly the part the clip showed. Line and circle opacity (no alpha in the common writer) is mixed into
# the colour over paper; a translucent circle becomes a 24-gon with its opacity.
# Texts recorded in the Page: role "label" (the default of Page.text) -> an anchored label of the drawing (Ix.layer
# does it: first position exactly where the round 4 code put it, then the 8 compass spots); any other role (title,
# heading, intro, caption, legend, list_item, note, source, badge) -> an unanchored text item of that role in the
# drawing's group, so nothing is burned into the drawing and nothing is placed twice. The pages call Page.text with
# role= where a text is not a label.
#   mpx_start() -> Ix                  the run's exporter (MPX[0]); folder cached/booklet/bergama_masterplan/
#   mpx_flat(items, box=None) -> [shape]   the Page items with every clip resolved, inside box (page mm) if given
#   mpx_drawing(ix, did, page, pg, box, den, origin_m=(0, 0), dkind="plan", north_deg=None, scale_pref=None,
#               layer="drawing", priority=1, group=None, title=None, labels=True) -> D
#         one drawing from the part `box` (x0, y0, x1, y1 page mm) of Page pg; den None = a scale-free diagram in mm
#   mpx_text_role(pg, role) / Page.text(..., role=...)   (role stays in the recorded item, index 9)
#   mpx_sw(sample) -> Ix legend swatch dict from a round 4 legend sample (_sw_fill/_sw_line/_sw_icon ...)
#   mpx_lines() -> [str]               "items bergama_masterplan: ..." + the page lines
# Page ids: round 6 (G6-2, PLAN §2.1): the final 22-page ids; MPX_PAGE maps the code's old page names to them.
# Round 6 (G6-9): Page.group(kind, eid) / Page.endgroup() (or `with mpx_grp(pg, kind, eid):`) mark the element
# groups; mpx_drawing hands each run of shapes to Ix.layer inside ix_group(kind, eid) (common/item_export.py, S2),
# so the booklet writes drawing › kind › element. mpx_X(pg) = the drawing object the round 6 modules draw on:
# it unpacks as (fill_fn, line_fn, text_fn) (S1 annot.py an_*, basemap_draw callbacks: fill(rings, hx, al, nonzero),
# line(pts, hx, lw, dash, al), text(t, xy, size_mm, hx, bold, align)) and has those as methods too.
MPX = [None]
MPX_PAGE = {"p17": "p15", "p23": "p20", "p24": "p21"}     # code page name -> round 6 page id (PLAN §2.1)
MPX_LOG = []
MPX_CLIPPED = []         # v42: texts an inner clip region removed in the last mpx_flat (named in the log)
MPX_PAGES = []           # (option, tag, recorder Page) of this run: only for the Rhino bake (rhino_bake input)
MPX_DROP = ("ruler",)    # recorded roles dropped on export: scale-bar figures (the booklet draws every scale bar)
MPX_PAPER = "FFFFFF"
MPX_ANCHORED = {"label": "label", "level_value": "level_value", "badge": "badge", "marker": "badge", "name": "label",
                "number": "badge", "base_name": "label", "north": "label"}     # recorded role -> anchored text role (the rest become unanchored texts)


def mpx_start():
    del MPX_LOG[:]
    MPX[0] = Ix(OUT_FOLDER, "bergama_masterplan", VERSION)
    return MPX[0]


def _mpx_box_of(rings):
    xs = [p[0] for r in rings for p in r]
    ys = [p[1] for r in rings for p in r]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else (0.0, 0.0, 0.0, 0.0)


def _mpx_is_rect(R):
    """R is an axis-parallel rectangle (4 or 5 points): its box, else None"""
    P = [tuple(p[:2]) for p in R]
    if len(P) == 5 and abs(P[0][0] - P[-1][0]) < 1e-9 and abs(P[0][1] - P[-1][1]) < 1e-9:
        P = P[:4]
    if len(P) != 4:
        return None
    xs, ys = sorted(set(round(p[0], 6) for p in P)), sorted(set(round(p[1], 6) for p in P))
    if len(xs) == 2 and len(ys) == 2:
        return (xs[0], ys[0], xs[1], ys[1])
    return None


def _mpx_sh_rect(R, b):
    """Sutherland-Hodgman: ring R cut to the box b (x0, y0, x1, y1); [] when nothing is left"""
    out = [tuple(p[:2]) for p in R]
    for edge in range(4):
        if not out:
            return []
        inp, out = out, []

        def ins(p):
            return (p[0] >= b[0], p[1] >= b[1], p[0] <= b[2], p[1] <= b[3])[edge]

        def cut(p, q):
            if edge in (0, 2):
                x = b[0] if edge == 0 else b[2]
                t = (x - p[0]) / (q[0] - p[0])
                return (x, p[1] + t * (q[1] - p[1]))
            y = b[1] if edge == 1 else b[3]
            t = (y - p[1]) / (q[1] - p[1])
            return (p[0] + t * (q[0] - p[0]), y)
        for i in range(len(inp)):
            p, q = inp[i - 1], inp[i]
            if ins(q):
                if not ins(p):
                    out.append(cut(p, q))
                out.append(q)
            elif ins(p):
                out.append(cut(p, q))
    return out if len(out) >= 3 else []


def _mpx_lb_rect(pts, b):
    """Liang-Barsky: a polyline cut to the box b -> [runs]"""
    runs, cur = [], []
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i][:2], pts[i + 1][:2]
        dx, dy = x1 - x0, y1 - y0
        t0, t1, ok = 0.0, 1.0, True
        for p, q in ((-dx, x0 - b[0]), (dx, b[2] - x0), (-dy, y0 - b[1]), (dy, b[3] - y0)):
            if abs(p) < 1e-12:
                if q < 0:
                    ok = False
                    break
                continue
            r = q / p
            if p < 0:
                if r > t1:
                    ok = False
                    break
                t0 = max(t0, r)
            else:
                if r < t0:
                    ok = False
                    break
                t1 = min(t1, r)
        if not ok:
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
            continue
        a = (x0 + t0 * dx, y0 + t0 * dy)
        c = (x0 + t1 * dx, y0 + t1 * dy)
        if cur and (abs(cur[-1][0] - a[0]) > 1e-9 or abs(cur[-1][1] - a[1]) > 1e-9):
            if len(cur) >= 2:
                runs.append(cur)
            cur = []
        if not cur:
            cur = [a]
        cur.append(c)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) >= 2:
        runs.append(cur)
    return runs


def _mpx_offset(R, d):
    """ring R offset by d (outward for d > 0, whatever its turn): vertex normals of the two edges, mitre capped"""
    P = [tuple(p[:2]) for p in R]
    if len(P) > 2 and abs(P[0][0] - P[-1][0]) < 1e-9 and abs(P[0][1] - P[-1][1]) < 1e-9:
        P = P[:-1]
    n = len(P)
    if n < 3:
        return P
    a2 = sum(P[i][0] * P[(i + 1) % n][1] - P[(i + 1) % n][0] * P[i][1] for i in range(n))
    s = 1.0 if a2 > 0 else -1.0                           # counter-clockwise: outward normal = (dy, -dx)
    out = []
    for i in range(n):
        p0, p1, p2 = P[i - 1], P[i], P[(i + 1) % n]
        nx = ny = 0.0
        for a, b in ((p0, p1), (p1, p2)):
            ex, ey = b[0] - a[0], b[1] - a[1]
            L = math.hypot(ex, ey) or 1.0
            nx += s * ey / L
            ny += -s * ex / L
        L = math.hypot(nx, ny)
        if L < 1e-9:
            out.append(p1)
            continue
        f = min(2.0 / L, 3.0)                              # mitre length 1 / cos(half angle), capped at 3 x d
        out.append((p1[0] + nx / L * d * f, p1[1] + ny / L * d * f))
    return out


def _mpx_circle_ring(cx, cy, r, n=24):
    return [(cx + r * math.cos(2.0 * math.pi * i / n), cy + r * math.sin(2.0 * math.pi * i / n)) for i in range(n)]


def _mpx_clip_one(it, clip):
    """item `it` cut by ONE clip region: [items]"""
    mode, rings, box = clip
    kd = it[0]
    if mode == "outside":                                  # the fade halos: only the part outside the rings showed
        if kd == "line" and len(it[1]) >= 3:
            lw = it[3] or 0.0
            Q = _mpx_offset(it[1], lw * 0.25)
            return [("line", Q + Q[:1], it[2], lw * 0.5) + tuple(it[4:])]
        return [it]
    if kd == "poly":
        out = []
        for R in it[1]:
            if box is not None:
                rb = _mpx_box_of([R])
                if rb[0] >= box[0] and rb[1] >= box[1] and rb[2] <= box[2] and rb[3] <= box[3]:
                    out.append([tuple(p[:2]) for p in R])
                elif not (rb[2] < box[0] or rb[0] > box[2] or rb[3] < box[1] or rb[1] > box[3]):
                    Q = _mpx_sh_rect(R, box)
                    if Q:
                        out.append(Q)
            else:
                out += sc_rings_clip(R, rings)
        return [(kd, out) + tuple(it[2:])] if out else []
    if kd == "line":
        runs = _mpx_lb_rect(it[1], box) if box is not None else sc_lines(it[1], rings)
        return [(kd, r_) + tuple(it[2:]) for r_ in runs if len(r_) >= 2]
    if kd == "circle":
        inside = (box[0] <= it[1] <= box[2] and box[1] <= it[2] <= box[3]) if box is not None else \
            sc_inside((it[1], it[2]), rings)
        return [it] if inside else []
    if kd == "text":
        inside = (box[0] <= it[2] <= box[2] and box[1] <= it[3] <= box[3]) if box is not None else \
            sc_inside((it[2], it[3]), rings)
        return [it] if inside else []
    if kd == "image":
        it = tuple(it) + (None,) * (9 - len(it))
        b = box if box is not None else _mpx_box_of(rings)
        c_ = it[8]
        c2 = (max(b[0], c_[0]), max(b[1], c_[1]), min(b[2], c_[2]), min(b[3], c_[3])) if c_ else b
        if c2[2] <= c2[0] or c2[3] <= c2[1]:
            return []
        return [it[:8] + (c2,)]
    return [it]


def _mpx_region(rings):
    rings = [r for r in rings if len(r) >= 3]
    if not rings:
        return None
    if len(rings) > 1:                                    # rect + rings, even-odd = outside the rings (halo clips)
        b0 = _mpx_is_rect(rings[0])
        if b0 is not None:
            return ("outside", rings[1:], None)
    b = _mpx_is_rect(rings[0]) if len(rings) == 1 else None
    return ("inside", rings, b)


def mpx_flat(items, box=None):
    """the recorded Page items with every clip resolved (and cut to `box`, page mm, when given); clipline = a line
    clipped to its rings; translucent lines / circles made opaque over paper"""
    stack, out = [], []
    if box is not None:
        stack.append(("inside", [rect(*box)], tuple(box)))
    for it in items:
        kd = it[0]
        if kd == "clip":
            reg = _mpx_region(it[1])
            stack.append(reg)
            continue
        if kd == "unclip":
            if len(stack) > (1 if box is not None else 0):
                stack.pop()
            continue
        if kd == "clipline":
            reg = _mpx_region(it[1])
            its = [("line", it[2], it[3], it[4], None, 1, it[5] if len(it) > 5 else None)]
            if reg is not None:
                its = [j for i_ in its for j in _mpx_clip_one(i_, reg)]
        else:
            its = [it]
        for ri_, reg in enumerate(stack):
            if reg is None:
                continue
            its = [j for i_ in its for j in _mpx_clip_one(i_, reg)]
            if not its:
                if kd == "text" and (box is None or ri_ > 0) and (u"%s" % it[1]).strip():
                    MPX_CLIPPED.append(u"%s" % it[1])     # v42 (L3): a text cut by an inner clip is named in the log
                break
        for j in its:
            if j[0] == "line" and len(j) > 6 and j[6] is not None and j[6] < 0.995:
                j = ("line", j[1], mix(j[2], MPX_PAPER, 1.0 - max(0.0, j[6])), j[3], j[4], j[5], None)
            elif j[0] == "circle" and len(j) > 7 and j[7] is not None and j[7] < 0.995:
                j = ("poly", [_mpx_circle_ring(j[1], j[2], j[3])], j[4], j[5], j[6] or 0.0, None, None, j[7])
            out.append(j)
    return out


def mpx_drawing(ix, did, page, pg, box, den, origin_m=(0.0, 0.0), dkind="plan", north_deg=None, scale_pref=None,
                layer="drawing", priority=1, group=None, title=None, labels=True, items=None):
    """ONE item-export drawing from the part `box` of Page pg (or of the given recorded `items`). Labels (role
    "label") become anchored labels; other recorded roles become unanchored texts of that role (group = the
    drawing's group, default its id). den None: a scale-free diagram in mm (extent = box size)."""
    x0, y0, x1, y1 = [float(v) for v in box]
    if den:
        k = float(den) / 1000.0
        ext = (origin_m[0], origin_m[1], origin_m[0] + (x1 - x0) * k, origin_m[1] + (y1 - y0) * k)
        D = ix.drawing(did, page, ext, scale_pref=scale_pref, units="m", dkind=dkind, north_deg=north_deg,
                       scale_bar=True, priority=priority, group=group or did, title=title)
        org = (origin_m[0] - x0 * k, origin_m[1] - y0 * k)
    else:
        k = 1.0
        D = ix.drawing(did, page, (0.0, 0.0, x1 - x0, y1 - y0), units="mm", dkind=dkind, north_deg=north_deg,
                       scale_bar=False, priority=priority, group=group or did, title=title)
        org = (-x0, -y0)
    del MPX_CLIPPED[:]
    flat = mpx_flat(pg.items if items is None else items, box)
    if MPX_CLIPPED:
        MPX_LOG.append(u"items %s %s: %d text(s) outside the drawing's clip, not exported: %s" % (
            page, did, len(MPX_CLIPPED), u", ".join(sorted(set(MPX_CLIPPED))[:12])))
    shapes, n_lab, n_txt = [], 0, 0
    runs, gst = [[None, shapes]], []                      # round 6 (G6-9): runs of shapes by element group
    for s in flat:
        if s[0] == "grp":
            if s[1] is None:
                if gst:
                    gst.pop()
            else:
                gst.append((s[1], s[2]))
            runs.append([gst[-1] if gst else None, []])
            continue
        if s[0] != "text":
            runs[-1][1].append(s)
            continue
        if not (u"%s" % s[1]).strip():
            continue
        role = s[9] if len(s) > 9 and s[9] else "label"
        if role in MPX_DROP:
            continue
        size_mm = float(s[4]) if s[4] else 2.0
        col = s[5] if isinstance(s[5], str) else None
        al = s[7] if len(s) > 7 and s[7] else "L"
        if role in MPX_ANCHORED:
            if not labels:
                continue
            r5 = MPX_ANCHORED[role]
            pos = ["=" + str(al)] if r5 == "badge" else ["=" + str(al)] + ["E", "NE", "N", "NW", "W", "SW", "S", "SE"]
            ix.text(page, s[1], r5, drawing=D["id"], at=(org[0] + k * s[2], org[1] + k * s[3]), size_pt=size_mm / IX_PT,
                    bold=bool(s[6]), colour=col, positions=pos, group=D["group"], priority=2 if r5 == "badge" else 5)
            n_lab += 1
        else:
            ix.text(page, s[1], role if role in IX_TEXT_ROLES else "note", size_pt=size_mm / IX_PT, bold=bool(s[6]),
                    colour=col, group=D["group"], priority=3 if role in ("title", "heading") else 6)
            n_txt += 1
    ixg = globals().get("ix_group")                      # S2 (common/item_export.py): element group context
    n_sh, kinds, elems, untagged = 0, set(), set(), 0
    for g_, sh_ in runs:
        if not sh_:
            continue
        n_sh += len(sh_)
        if g_ is None or ixg is None:
            untagged += len(sh_) if g_ is None else 0
            ix.layer(D, layer, sh_, k=k, origin=org)
            continue
        kinds.add(g_[0])
        elems.add(g_)
        cm = ixg(g_[0], g_[1])
        if hasattr(cm, "__enter__"):
            with cm:
                ix.layer(D, layer, sh_, k=k, origin=org)
        else:                                             # ix_group as a plain setter: tag, draw, reset
            ix.layer(D, layer, sh_, k=k, origin=org)
            ixg(None, None)
    MPX_LOG.append(u"items %s %s: %d shapes, %d labels, %d texts%s" % (
        page, did, n_sh, n_lab, n_txt, u" · 1:%s" % u"{:,.0f}".format(den) if den else u" · mm"))
    MPX_LOG.append(u"groups %s %s kinds=%d elements=%d untagged=%d" % (page, did, len(kinds), len(elems), untagged))
    if ixg is None:
        MPX_LOG.append(u"FLAG groups %s %s: ix_group missing (common/item_export.py of round 6 not in this build)" %
                       (page, did))
    return D


class mpx_grp(object):
    """round 6 (G6-9): `with mpx_grp(pg, "trees", "plane 12"):` = Page.group / Page.endgroup around a block"""
    def __init__(self, pg, kind, eid=None):
        self.pg, self.kind, self.eid = pg, kind, eid

    def __enter__(self):
        self.pg.group(self.kind, self.eid)
        return self.pg

    def __exit__(self, *a):
        self.pg.endgroup()
        return False


class mpx_X(object):
    """round 6: Page pg as the drawing object of the shared modules (annot.py, keymap.py km_draw_to): fill / line /
    text with the km_draw_to callback signatures; `grp` = (kind, eid) wraps every call in that element group"""
    def __init__(self, pg, grp=None):
        self.pg, self.grp = pg, grp

    def __iter__(self):                                 # S1 annot.py takes X = (fill_fn, line_fn, text_fn)
        return iter((self.fill, self.line, self.text))

    def __getitem__(self, i):
        return (self.fill, self.line, self.text)[i]

    def __len__(self):
        return 3

    def _g(self, on):
        if self.grp:
            if on:
                self.pg.group(self.grp[0], self.grp[1])
            else:
                self.pg.endgroup()

    def fill(self, rings, hx, al=None, nonzero=False):
        self._g(True)
        self.pg.poly([R_ for R_ in rings if len(R_) >= 3], fill=hx, alpha=al)
        self._g(False)

    def line(self, pts, hx, lw, dash=None, al=None):
        self._g(True)
        self.pg.line(pts, hx, lw, list(dash) if dash else None, cap=0 if dash else 1, alpha=al)
        self._g(False)

    def text(self, t_, xy, size, hx, bold=False, align="BL"):
        al = align[-1] if align and align[-1] in "LCR" else "L"
        dy = -0.36 * size if align and align[0] == "M" else (-size if align and align[0] == "T" else 0.0)
        self._g(True)
        self.pg.text(t_, xy[0], xy[1] + dy, size, hx, bold=bold, align=al, role="label")
        self._g(False)


MPX_SW_BOX = (4.0, 2.4)          # mm: the booklet's legend swatch (50_place PL_SW)


def mpx_sw(sample):
    """a round 4 legend sample -> an Ix legend swatch dict. A sample is a draw function f(pg, x, y, w, h) (_sw_fill,
    _sw_line, _sw_icon, _pl23_sw_* ...): it is drawn into a swatch-sized Page and read back: an image -> kind
    "image"; only lines -> "line"/"dash"; dots -> "dot"; else "fill" (first fill colour, opacity mixed over paper,
    outline as stroke). The full drawing rides along as "shapes" (schema shape dicts in swatch mm, y up from the
    lower-left corner) so the booklet can draw the true sample (icons, plants, gradients) when it reads them."""
    W, H = MPX_SW_BOX
    if isinstance(sample, dict):
        return dict(sample)
    if not callable(sample):
        return dict(kind="fill", colour=sample if isinstance(sample, str) else None)
    pg = Page(W, H)
    try:
        sample(pg, 0.0, 0.0, W, H)
    except Exception as ex:
        MPX_LOG.append(u"WARNING legend swatch not drawn (%s)" % type(ex).__name__)
        return dict(kind="fill", colour=None)
    flat = [s_ for s_ in mpx_flat(pg.items) if s_[0] != "text"]
    ix = MPX[0]
    shapes = [d_ for d_ in (ix._shape(s_, 1.0, (0.0, 0.0)) for s_ in flat) if d_ is not None] if ix else []
    for d_ in shapes:
        d_.pop("_stripes", None)
    imgs = [s_ for s_ in flat if s_[0] == "image"]
    polys = [s_ for s_ in flat if s_[0] == "poly"]
    lines = [s_ for s_ in flat if s_[0] == "line"]
    circs = [s_ for s_ in flat if s_[0] == "circle"]
    if imgs:
        out = dict(kind="image", file=imgs[0][5])
    elif lines and not polys and not circs:
        L = lines[0]
        out = dict(kind="dash" if L[4] else "line", colour=L[2], width_pt=(L[3] or 0.25) / IX_PT,
                   dash_pt=[v / IX_PT for v in L[4]] if L[4] else None)
    elif circs and not polys:
        c_ = circs[0]
        out = dict(kind="dot", colour=c_[4] or c_[5], stroke=c_[5])
    else:
        fills = [p_ for p_ in polys if p_[2]]
        strokes = [p_ for p_ in polys if p_[3]]
        col = None
        if fills:
            f_ = fills[0]
            a_ = f_[7] if len(f_) > 7 and f_[7] is not None else 1.0
            if len(fills) > 1 and all(p_[2] == f_[2] for p_ in fills):      # stacked see-through steps (gradient)
                a_ = 1.0 - (1.0 - a_) ** len(fills)
            col = mix(f_[2], MPX_PAPER, 1.0 - min(1.0, a_)) if a_ < 0.995 else f_[2]
        out = dict(kind="fill", colour=col, stroke=strokes[0][3] if strokes else None,
                   width_pt=(strokes[0][4] or 0.25) / IX_PT if strokes else None)
    out["shapes"] = shapes
    out["box_mm"] = [W, H]
    return out


def mpx_keymap(ix, page, km, item_id=None):
    """the key-map module's items (S2 km_items: drawing in key-map mm + label texts + keymap item) added to the
    export as they are (ids made unique); the booklet places the frame in the right column. Returns the drawing id."""
    its = km_items(km, page, item_id=item_id)
    did = None
    for it in its:
        it = dict(it)
        it["id"] = ix._id(it.get("id"), it.get("kind", "item"))
        it["page"] = page
        if it.get("kind") == "drawing" and did is None:
            did = it["id"]
        elif it.get("anchor") and did is not None:
            it["anchor"] = dict(it["anchor"], drawing=did)
        elif it.get("kind") == "keymap" and did is not None:
            it["drawing"] = did
        ix._put(page, it)
    MPX_LOG.append(u"items %s key map %s: %d items" % (page, did, len(its)))
    return did


def mpx_lines():
    ix = MPX[0]
    return list(MPX_LOG) + ([ix.summary()] if ix is not None else [])
