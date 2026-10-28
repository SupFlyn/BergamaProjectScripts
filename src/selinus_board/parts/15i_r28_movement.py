# ---- MIRAQUA round 28 Oct 2026 (site board v50): p.07 street index maps + notes, p.09 proposal map and index change (worker SB-move). Shared pieces: parts/15h_r28_shared.py,
# common/r28_style.py, common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# P07.2 a note beside each of the three p.07 maps (crops drw_mv_note_1..3: why these streets matter, only what the
# board computes); P07.3 walking / driving today with the index on EVERY street piece in five classes (colour and
# line weight), the classes in the crops' legend; P07.4 street names 7 pt. P09.1 the proposal map redrawn: pale base,
# reach on foot as crisp classes on the streets (R28_REACH), road categories as line types, crossings and hubs as
# symbols, numbered callouts without overlaps (label_place); P09.2 the list in three groups under it; P09.3 the walk
# and car index today and with the proposal (drw_index_change) instead of the commercial spines map.
import unicodedata

R28MV_CLS = (2.0, 10.0, 25.0, 50.0, 100.0)    # P07.3: index classes 0-2, 2-10, 10-25, 25-50, 50-100 (the top map's steps)
R28MV_CLS_W = (0.2, 0.32, 0.48, 0.68, 0.95)   # mm on the booklet page: the line weight of each class
R28MV_CLS_COL = [mv_ramp(SEQ, seq_t(v_, 100.0)) for v_ in R28MV_CLS]   # a class = the top map's ramp at its upper step
R28MV_LABEL_PT = 7.0     # P07.4: street names on the walking / driving maps (were 8 pt)
R28MV_NOTE_OF = {"walk_b": 2, "car_b": 3}      # P07.2: the maps' notes, crops drw_mv_note_2 / _3 (_1: the top map)
R28MV_NOTE_W = 100.0     # mm: a note's text width at most; map + gutter + note stay within the booklet width BK_AW
R28MV_GUT = 4.0          # mm between two panels of a booklet row (bergama_booklet GUT)
R28MV_LEAD = 1.75        # baseline to baseline / capital height, notes and lists
R28MV_NEAR_M = 100.0     # m: "comes within ... of the stream" (notes)
R28MV_EDGE_M = 40.0      # m: the streets along the stream (as city_link_movement.json "edge")
R28MV_CAP = 0.718        # capital height / font size of the writer (_PDF_CAP)
# P09.1 road categories: (name, colour, line mm, dash (on, off) mm or None, calming ticks); the colours are the
# masterplan's (ROAD_CHANGE_COL, its p.23 plan), the line types tell them apart (secondary encoding)
R28MV_ROAD = {"kept": (u"kept", C("847E75"), 0.7, None, False),
              "calmed": (u"calmed", C("B5832F"), 0.9, None, True),
              "pedestrian": (u"pedestrian", C("8B3A3F"), 1.25, None, False),
              "shared": (u"shared", C("7F5B7B"), 0.9, (1.6, 0.7), False),
              "relocated": (u"relocated", C("C2603A"), 0.9, (0.6, 0.6), False)}
R28MV_BUS = (u"bus line, later step", C("633131"), 0.45, (1.2, 0.8))    # dashed, 1.05 mm beside its streets
R28MV_REACH_W = (0.5, 0.4, 0.3)     # mm: the three reach classes (R28_REACH) on the streets, the nearest heaviest
R28MV_MK = dict((k_, C(hx_)) for k_, lab_, hx_ in R28_MARKERS)   # callout numbers by group, as p.23's markers
R28MV_BRIDGE = C(R28_OPEN["bridge"])                              # bridge kept
R28MV_DISC = 1.6         # mm: radius of a numbered callout on the map (7 pt number)
R28MV_SYM = 2.0          # mm: half-length of a crossing symbol across the stream
R28MV_HUB_R = 2.1        # mm: hub ring radius
R28MV_GROUPS = (("roads", u"Roads"), ("crossings", u"Bridges and crossings"), ("hubs", u"Hubs"))
R28MV_CHANGE_ORDER = ("pedestrian", "calmed", "shared", "relocated", "kept", "truck", "bus")   # index chart rows

# ------------------------------------------------------------ text: Arial widths, **bold** runs (G5)
# Arial has Helvetica's widths (common/pdf_fonts.py): per 1000 em, codes 32-126, plain and bold
_R28MV_HW = [int(v_) for v_ in (
    "278 278 355 556 556 889 667 191 333 333 389 584 278 333 278 278 556 556 556 556 556 556 556 556 556 556 "
    "278 278 584 584 584 556 1015 667 667 722 722 667 611 778 722 278 500 667 556 833 722 778 667 778 722 667 611 "
    "722 667 944 667 667 611 278 278 278 469 556 333 556 556 500 556 556 278 556 556 222 222 500 222 833 556 556 "
    "556 556 333 500 278 556 500 722 500 500 500 334 260 334 584").split()]
_R28MV_HB = [int(v_) for v_ in (
    "278 333 474 556 556 889 722 238 333 333 389 584 278 333 278 278 556 556 556 556 556 556 556 556 556 556 "
    "333 333 584 584 584 611 975 722 722 722 722 667 611 778 722 278 556 722 611 833 722 778 667 778 722 667 611 "
    "722 667 944 667 667 611 333 278 333 584 556 333 556 611 556 611 556 333 611 611 278 278 556 278 889 611 611 "
    "611 611 389 556 333 611 556 778 556 556 500 389 280 389 584").split()]
_R28MV_SP = {u"ı": 278, u"·": 278, u"–": 556, u"—": 1000, u"²": 333, u"³": 333, u"°": 400, u"’": 278}


def r28mv_tw(txt, h, bold=False):
    """v50 (MIRAQUA 28 Oct, G5): the width (board units) of txt in Arial at capital height h, so that bold and plain
    runs set side by side on one line meet (tw's 0.92 h per letter is a safe upper bound, too wide for that)"""
    tab = _R28MV_HB if bold else _R28MV_HW
    w_ = 0
    for ch in txt:
        o = ord(ch)
        if 32 <= o < 127:
            w_ += tab[o - 32]
        elif ch in _R28MV_SP:
            w_ += _R28MV_SP[ch]
        else:
            b_ = unicodedata.normalize("NFD", ch)[:1]
            w_ += tab[ord(b_) - 32] if b_ and 32 <= ord(b_) < 127 else 556
    return w_ / 1000.0 * h / R28MV_CAP


def r28mv_parse(s):
    """'**bold** plain' -> [(text, bold)]"""
    return [(t_, j % 2 == 1) for j, t_ in enumerate(s.split(u"**")) if t_]


def r28mv_lines(s, width, h):
    """s (with **bold** runs) broken at its spaces into lines no wider than width (board units) at capital height h.
    A line = [(space before, word)], a word = [(text, bold)] (it may change weight inside, e.g. **K4**,)."""
    toks, cur, sp = [], [], False
    for t_, b_ in r28mv_parse(s):
        for j, piece in enumerate(t_.split(u" ")):
            if j > 0:
                if cur:
                    toks.append((sp, cur))
                cur, sp = [], True
            if piece:
                cur.append((piece, b_))
    if cur:
        toks.append((sp, cur))
    sw_ = r28mv_tw(u" ", h)
    lines, line, lw_ = [], [], 0.0
    for sp, word in toks:
        ww = sum(r28mv_tw(t_, h, b_) for t_, b_ in word)
        if line and lw_ + sw_ + ww > width:
            lines.append(line)
            line, lw_ = [], 0.0
        lw_ += (sw_ if line else 0.0) + ww
        line.append((bool(line), word))
    if line:
        lines.append(line)
    return lines


def r28mv_line_w(line, h):
    """the width of one line of r28mv_lines"""
    sw_ = r28mv_tw(u" ", h)
    return sum((sw_ if sp else 0.0) + sum(r28mv_tw(t_, h, b_) for t_, b_ in word) for sp, word in line)


def r28mv_draw_line(B, line, x, y, h, col, L, order=66):
    """one line of r28mv_lines at baseline y, each run of one weight as one whole text (live in Illustrator).
    Returns its width."""
    runs = []
    for sp, word in line:
        for j, (t_, b_) in enumerate(word):
            t2 = (u" " if sp and j == 0 else u"") + t_
            if runs and runs[-1][1] == b_:
                runs[-1][0] += t2
            else:
                runs.append([t2, b_])
    cx = x
    for t_, b_ in runs:
        B.text(t_, cx, y, h, col, L, order=order, font=FONT_TITLE, bold=b_)
        cx += r28mv_tw(t_, h, b_)
    return cx - x


def r28mv_para(B, s, x, y, width, h, col, L, order=66):
    """s wrapped to width from the baseline y; returns the baseline after its last line"""
    for ln in r28mv_lines(s, width, h):
        r28mv_draw_line(B, ln, x, y, h, col, L, order)
        y -= R28MV_LEAD * h
    return y


def r28mv_title(s):
    """an upper-case name in title case with its Turkish letters (K4 · ULUCAMİ ÖNÜ -> K4 · Ulucami Önü, İSTİKLAL
    MEYDANI -> İstiklal Meydanı); words with digits and words not in capitals stay as written"""
    out = []
    for w_ in (s or u"").split(u" "):
        if not w_ or any(c_.isdigit() for c_ in w_) or not w_.isupper():
            out.append(w_)
            continue
        lo = w_.replace(u"I", u"ı").replace(u"İ", u"i").lower()
        out.append({u"i": u"İ", u"ı": u"I"}.get(lo[0], lo[0].upper()) + lo[1:])
    return u" ".join(out)


def r28mv_cap(s):
    return (s or u"")[:1].upper() + (s or u"")[1:]


def r28mv_note_text(note, heads):
    """the masterplan's note without its leading "change: " (the change is printed in bold before it)"""
    n_ = (note or u"").strip()
    if u": " in n_ and n_.split(u": ", 1)[0].strip().lower() in heads:
        n_ = n_.split(u": ", 1)[1].strip()
    return n_


def r28mv_entry(name, change, note):
    """a list entry: **name · change** · note"""
    return u"**{}{}**{}".format(name, u" · " + change if change else u"", u" · " + note if note else u"")


def r28mv_src_mv():
    """the movement method's source (the same words as the top map's, so the same [n])"""
    return ("Movement potential = the number of shortest routes between every building and every everyday "
            "destination within {:.0f} m on foot or {:.0f} min by car that use the street (OSM network, Overture "
            "places, the method of bergama_movement v1); index 100 = the busiest street piece in the frame. A count "
            "of routes, not of people or vehicles: no count exists for these streets.".format(
                MV_OPT["r_walk"], MV_OPT["t_car"] / 60.0))


R28MV_SRC_COM = ("Commerce: shopfronts within 30 m of a street (survey, OSM, Overture). Services: Overture/Meta "
                 "places. Walks: the shortest along OSM streets and footways from the edge of each working area, "
                 "rounded to 10 m.")      # = draw_how_people_use_it's r_com (the same [n])


def _r28mv_wh(w_, h_):
    return lambda f: (w_ * f, h_ * f)


# ------------------------------------------------------------ a pale base (G6)
def r28mv_pale(c, t):
    return mix(c, WHITE, t)


class R28Pale(object):
    """v50 (MIRAQUA 28 Oct, P09.1, G6): a drawing target that lays b_base's colours t of the way to white (the water
    t_w) and thins its lines (wf): the pale, recessive base under the proposal. The study area's outline passes as it
    is (G8: one line style everywhere)."""

    def __init__(self, B, t=0.5, t_w=0.3, wf=0.7):
        self.B, self.t, self.t_w, self.wf = B, t, t_w, wf
        self.keep = tuple(C(R28_STUDY_LINE["colour"]))
        self.water = (tuple(MPL["water"]), tuple(MPL["water_edge"]))

    def __getattr__(self, k_):
        return getattr(self.B, k_)

    def _c(self, c):
        c3 = tuple(c[:3])
        if c3 == self.keep:
            return c
        return r28mv_pale(c3, self.t_w if c3 in self.water else self.t)

    def fill(self, polys, color, layer, order):
        self.B.fill(polys, self._c(color), layer, order)

    def hatch(self, polys, color, layer, order, spacing, ang=math.radians(45.0), w=0.03):
        self.B.hatch(polys, self._c(color), layer, order, spacing, ang, w)

    def line(self, P, color, layer, order, w=0.13):
        keep = tuple(color[:3]) == self.keep
        self.B.line(P, self._c(color), layer, order, w if keep else w * self.wf)


def r28mv_base_leg():
    """the pale base's legend rows (b_base's tones as R28Pale draws them) and the study area"""
    return [("box", r28mv_pale(MPL["water"], 0.3), u"Selinos stream"), ("box", r28mv_pale(MPL["bld"], 0.5), u"Building"),
            ("box", r28mv_pale(MPL["her"], 0.5), u"Heritage building"), R28_STUDY_LEG]


# ------------------------------------------------------------ p.07 walking / driving today: every piece graded
def r28mv_class(v):
    """the index class (0-4) of value v"""
    for i, up in enumerate(R28MV_CLS):
        if v < up:
            return i
    return len(R28MV_CLS) - 1


def r28mv_class_streets(B, V, runs, k, L, order):
    """v50 (MIRAQUA 28 Oct, P07.3): every street piece of runs [(points, (OSM class, index))] (mv_runs) in its index
    class: colour (the top map's SEQ ramp at the class's upper step) and line weight (R28MV_CLS_W) by class, the
    busiest drawn last. Returns the length (m) in each class."""
    lens = [0.0] * len(R28MV_CLS)
    for P, (cls, v) in sorted(runs, key=lambda r_: r_[1][1]):
        c_ = r28mv_class(v)
        lens[c_] += pl_length(P)
        B.line(V.P(P), R28MV_CLS_COL[c_], L, order + c_, bk_lw(R28MV_CLS_W[c_], k))
    return lens


def r28mv_class_legend():
    """the five classes as booklet legend rows: sample in the class's colour and line weight (pt)"""
    labs = [u"{:.0f}-{:.0f}".format(a_, b_) for a_, b_ in zip((0.0,) + R28MV_CLS[:-1], R28MV_CLS)]
    return [dict(kind="line", colour=crop_hex(c_), label=u"Walk / car index " + lab, width=round(w_ * 72.0 / 25.4, 2))
            for c_, lab, w_ in zip(R28MV_CLS_COL, labs, R28MV_CLS_W)]


def draw_mv_key(S, B, V, R, MV, key, F, L, h, bounds):
    """v44: the key streets of the walking / driving map, named. v50 (MIRAQUA 28 Oct, P07.3, P07.4): every street
    piece is drawn graded (r28mv_class_streets), so this names the 5 busiest named streets (mv_key_rows) at h (7 pt),
    "name · index" on its longest run, placed without overlaps (place_labels). Returns (their rows, the key of the
    labels that found no place, {name: every point of its runs})."""
    rows = mv_key_rows(MV, key)
    names = set(r_["name"] for r_ in rows)
    pieces = R["pieces"]
    net = "car_b" if key.startswith("car") else "walk_b"

    def val(pi):
        nm = (pieces[pi]["tags"].get("name") or "").strip()
        return nm if nm in names else None
    best, pts = {}, {}
    for P, nm in _runs(R["chains"][net], pieces, R["xy"], val, set(R["inside"]), F):
        pts.setdefault(nm, []).extend(P)
        if nm not in best or pl_length(P) > pl_length(best[nm]):
            best[nm] = P
    labels = []
    for r_ in rows:
        P = best.get(r_["name"])
        if P:
            q, t = pl_point_at(P, pl_length(P) / 2.0)
            px, py = V.p(q[0], q[1])
            labels.append(([u"{} · {:.0f}".format(r_["name"], r_[key])], px, py, h, INK))
    return rows, place_labels(B, labels, [], L, bounds=bounds), pts


def r28mv_main_stream(S):
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    return max(streams, key=pl_length) if streams else None


def r28mv_edge_means(S, R):
    """v50 (P07.2): today's walking and driving index, length-weighted, on the street pieces whose middle lies within
    R28MV_EDGE_M of the main Selinos line (as city_link_movement.json "edge") and on every piece on the map:
    {"walk_b" | "car_b": (along the stream, all, m along the stream)}; once per run (S._r28mv_edge)."""
    got = getattr(S, "_r28mv_edge", None)
    if got is not None:
        return got
    out, main = {}, r28mv_main_stream(S)
    if main:
        d = R28MV_EDGE_M
        segs = list(zip(main[:-1], main[1:]))
        g = Grid(d)
        for i, (a, b) in enumerate(segs):
            g.add(i, (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1])))
        pieces, xy, IDX = R["pieces"], R["xy"], R["IDX"]
        acc = {"walk_b": [0.0, 0.0, 0.0, 0.0], "car_b": [0.0, 0.0, 0.0, 0.0]}
        for i in R["inside"]:
            p = pieces[i]
            if p["prop"] or p["L"] <= 0:
                continue
            m = ((xy[p["a"]][0] + xy[p["b"]][0]) / 2.0, (xy[p["a"]][1] + xy[p["b"]][1]) / 2.0)
            near = any(seg_dist(m[0], m[1], segs[j][0][0], segs[j][0][1], segs[j][1][0], segs[j][1][1]) <= d
                       for j in g.query((m[0] - d, m[1] - d, m[0] + d, m[1] + d)))
            for key, ok in (("walk_b", p["walk"]), ("car_b", p["cf"] or p["cb"])):
                if not ok:
                    continue
                v = IDX[key].get(i, 0.0) * p["L"]
                a_ = acc[key]
                a_[0] += v
                a_[1] += p["L"]
                if near:
                    a_[2] += v
                    a_[3] += p["L"]
        out = dict((key, (a_[2] / a_[3] if a_[3] else None, a_[0] / a_[1] if a_[1] else None, a_[3]))
                   for key, a_ in acc.items())
    S._r28mv_edge = out
    return out


# ------------------------------------------------------------ p.07 the notes beside the maps (P07.2)
def r28mv_note(B, crop, k, L, num, items, head=u"Why these streets matter"):
    """v50 (MIRAQUA 28 Oct, P07.2): a short note in the empty width right of a p.07 map whose crop is `crop` (board
    units): its heading, then items (lines with one or two **bold** keywords, G5), 9 pt (8.5, 8 where the map's
    height asks for it; the last items left out, logged, where even that does not fit). Crop drw_mv_note_<num>, as
    tall as its text, its top on the map's, drawn for its width on the booklet page (bk_w): the row map + 4 mm +
    note stays within BK_AW, so the map keeps 1:10,000."""
    wmax = BK_AW - R28MV_GUT - (crop[2] - crop[0]) / k - 0.5     # mm the row leaves for the note's crop
    nw = min(R28MV_NOTE_W, wmax - 1.0)                            # mm of text
    if nw < 30.0 or not items:
        LOG.append("Note {} beside the p.07 map not drawn (no width or nothing to say).".format(num))
        return
    hmax = crop[3] - crop[1] - 1.0 * k                            # no taller than its map's crop
    x0 = crop[2] + R28MV_GUT * k
    tx, items, fit = x0 + 0.5 * k, list(items), None
    while items and fit is None:
        for pt in (9.0, 8.5, 8.0):
            h, hh = bk_hk(pt, k), bk_hk(pt + 0.5, k)
            lines = [r28mv_lines(it, nw * k, h) for it in items]
            need = 0.5 * k + hh + (R28MV_LEAD + 0.6) * h + (sum(len(l_) for l_ in lines) - 1) * R28MV_LEAD * h + \
                (len(lines) - 1) * 0.5 * h + 0.4 * h + 0.5 * k
            if need <= hmax:
                fit = (h, hh, lines)
                break
        if fit is None:
            LOG.append(u"Note {} beside the p.07 map: \"{}\" left out (no room).".format(num, items[-1]))
            items = items[:-1]
    if fit is None:
        return
    h, hh, lines = fit
    y = crop[3] - 0.5 * k - hh
    B.text(head, tx, y, hh, INK, L, order=66, font=FONT_TITLE, bold=True)
    y -= (R28MV_LEAD + 0.6) * h
    for j, item in enumerate(lines):
        for ln in item:
            r28mv_draw_line(B, ln, tx, y, h, INK, L)
            y -= R28MV_LEAD * h
        y -= 0.5 * h
    bot = y + R28MV_LEAD * h + 0.5 * h - 0.4 * h
    crop_panel("mv_note_{}".format(num), x0, bot - 0.5 * k, x0 + (nw + 1.0) * k, crop[3], u"")
    CROP_PANELS[-1]["bk_w"] = nw + 1.0


def r28mv_note_top(S, B, crop, k, L, MV, n_pl):
    """v50 (P07.2): drw_mv_note_1, beside the top map: the shops' streets, the busiest street, shops against walking,
    the civic constellations and the services, all as the board computes and prints them on the page."""
    out = []
    prim = [g for g in getattr(S, "corr_primary", None) or [] if g["label"] != "an unnamed street"]
    if prim:
        out.append(u"**Shops** line up on {}: the primary commercial spines {}.".format(
            join_names([u"{} ({} shops)".format(g["label"], g["n"]) for g in prim]), bcite(R28MV_SRC_COM)))
    sec = getattr(S, "corr_secondary", None) or []
    if sec:
        out.append(u"**{} more street{}** with 3 or more shops: the secondary spines.".format(
            len(sec), u"" if len(sec) == 1 else u"s"))
    rows = MV.get("rows") or []
    if rows:
        out.append(u"**Busiest street** on foot and by car together: {}, index {:.0f} (100 = the busiest street "
                   u"piece) {}.".format(rows[0]["name"], rows[0]["comb_b"], bcite(r28mv_src_mv())))
    rho, big = (MV.get("rho") or {}).get("walk_b"), MV.get("big") or []
    if rho is not None and big:
        out.append(u"**Shops and walking**: Spearman {:.2f} over the {} named streets of 50 m or more (1 = the same "
                   u"order).".format(rho, len(big)))
    cl = getattr(S, "clusters", None) or []
    if cl:
        out.append(u"**{} civic constellation{}**: 3 or more civic or sacred places, each within 100 m of the "
                   u"next.".format(len(cl), u"" if len(cl) == 1 else u"s"))
    tot = sum((n_pl or {}).values())
    if tot:
        f, n = max(n_pl.items(), key=lambda kv: kv[1])
        lab = dict((f_, lab_) for f_, let_, c_, lab_ in WALK_FUN).get(f, f)
        out.append(u"**{} services** on the map (Overture places), {} of them {}.".format(tot, n, lab.lower()))
    r28mv_note(B, crop, k, L, 1, out)


def r28mv_note_today(S, R, MV, key, rows, pts, lens):
    """v50 (P07.2): the lines of drw_mv_note_2 / _3: the busiest named streets, how many of them come close to the
    stream, the index along the stream against all streets, how the network length spreads over the classes, what
    the index counts"""
    walk = key.startswith("walk")
    out = []
    if rows:
        out.append(u"**Busiest**: " + u", ".join(u"{} {:.0f}".format(r_["name"], r_[key]) for r_ in rows) + u".")
    main = r28mv_main_stream(S)
    if main and rows:
        near = [r_ for r_ in rows if pts.get(r_["name"]) and
                min(pl_dist(p[0], p[1], main, False) for p in pts[r_["name"]]) <= R28MV_NEAR_M]
        out.append(u"**{} of the {}** busiest come within {:.0f} m of the stream.".format(len(near), len(rows),
                                                                                         R28MV_NEAR_M))
    em = r28mv_edge_means(S, R).get(key)
    if em and em[0] is not None and em[1] is not None:
        out.append(u"**Along the stream** (streets within {:.0f} m of it): index {:.0f} on average, all streets on the "
                   u"map {:.0f}.".format(R28MV_EDGE_M, em[0], em[1]))
    tot = sum(lens)
    if tot > 0:
        out.append(u"**{:.0f}%** of the {} street length carries index 25 or more, {:.0f}% stays under 2.".format(
            100.0 * (lens[3] + lens[4]) / tot, u"walkable" if walk else u"drivable", 100.0 * lens[0] / tot))
    if walk:
        out.append(u"**On foot**: the shortest routes up to {:.0f} m between every building and the everyday "
                   u"destinations; 100 = the busiest piece today {}.".format(MV_OPT["r_walk"], bcite(r28mv_src_mv())))
    else:
        out.append(u"**By car**: the shortest routes up to {:.0f} min; footways and steps are not on this map "
                   u"{}.".format(MV_OPT["t_car"] / 60.0, bcite(r28mv_src_mv())))
    return out


def draw_mv_today(S, B, x, y, U, R, MV, key, title, cap):
    """v46 (Prompt 3, p.8): walking or driving today as its own map at the theme's one scale: the whole site frame at
    1:10,000, the masterplan base, the scale bar and north arrow under it. v50 (MIRAQUA 28 Oct, P07.3): the index on
    EVERY street piece of its network (mv_runs walk_b / car_b; walking-only pieces stay base street on the driving
    map), graded in five classes by colour and line weight (r28mv_class_streets), the classes in the crop's legend;
    the 5 busiest named streets named at 7 pt (draw_mv_key, P07.4); P07.2: its note beside it (drw_mv_note_2 / _3).
    Returns the y below its crop."""
    L = "LU_BOARD::HowPeopleUseIt"
    F = S.F
    B.text(title, x, y, 0.5 * U, INK, L, font=FONT_TITLE, bold=True)
    V, k, ss, r = b_view(F, x, y - 0.8 * U, U)
    h = bk_hk(R28MV_LABEL_PT, k)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    b_base(S, CB, V, k, L)
    lens = r28mv_class_streets(CB, V, mv_runs(S, R, key, F), k, L, 14)
    rows, key_, pts = draw_mv_key(S, CB, V, R, MV, key, F, L, h, r)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    if key_:
        low = draw_label_key(B, key_, x, low - 0.8 * k, r[2] - x, h, L)
    crop = (x - 0.5 * k, low - 0.5 * k, r[2] + 0.5 * k, r[3] + 0.5 * k)
    crop_panel(CROP_MV.get(key, key), crop[0], crop[1], crop[2], crop[3], cap.format(len(rows)), crop_scale(ss),
               r28mv_class_legend())
    if key in R28MV_NOTE_OF:
        r28mv_note(B, crop, k, L, R28MV_NOTE_OF[key], r28mv_note_today(S, R, MV, key, rows, pts, lens))
    return low - 0.5 * k


# ------------------------------------------------------------ p.09 the proposal: symbols
def r28mv_offset(Q, d):
    """the polyline Q moved d (board units) to its left"""
    out, n = [], len(Q)
    for i in range(n):
        a, b = Q[max(0, i - 1)], Q[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        out.append((Q[i][0] - dy / ln * d, Q[i][1] + dx / ln * d))
    return out


def r28mv_road_line(B, Q, st, k, L, order):
    """a road of category style st (R28MV_ROAD) along the page polyline Q: a white casing, the line (dashed where the
    style says), the calmed road's short cross ticks"""
    nm, col, w, dash, ticks = st
    B.line(Q, WHITE, L, order, bk_lw(w + 0.5, k))
    for d in (dashes(Q, dash[0] * k, dash[1] * k) if dash else [Q]):
        B.line(d, col, L, order + 1, bk_lw(w, k))
    if ticks:
        lq, s = pl_length(Q), 0.7 * k
        while s < lq:
            p, t = pl_point_at(Q, s)
            B.line([(p[0] - t[1] * 0.85 * k, p[1] + t[0] * 0.85 * k), (p[0] + t[1] * 0.85 * k, p[1] - t[0] * 0.85 * k)],
                   col, L, order + 2, bk_lw(0.22, k))
            s += 1.4 * k


def r28mv_bus_line(B, Q, k, L, order, dashed=True, side=1.05):
    """the bus line along the page polyline Q, side mm to its left (beside the road it runs on), dashed when later"""
    nm, col, w, dash = R28MV_BUS
    Qo = r28mv_offset(Q, side * k) if side else Q
    for d in (dashes(Qo, dash[0] * k, dash[1] * k) if dashed else [Qo]):
        B.line(d, col, L, order, bk_lw(w, k))


def r28mv_cross(B, px, py, e, kind, k, L, order, s=1.0):
    """a crossing at (px, py), e = the page direction across the stream: bridge kept = two decks with flared ends
    (R28_OPEN bridge), footbridge = one bar with end ticks, stepping stones = four stones (both R28_MARKERS
    crossings), each on a white casing"""
    t = (-e[1], e[0])
    a = R28MV_SYM * k * s

    def pt(fe, ft):
        return (px + e[0] * fe + t[0] * ft, py + e[1] * fe + t[1] * ft)
    col = R28MV_MK["crossings"]
    if kind == "bridge kept":
        for sd in (-0.55, 0.55):
            B.line([pt(-a, sd * k * s), pt(a, sd * k * s)], WHITE, L, order, bk_lw(0.8, k))
        for sd in (-0.55, 0.55):
            fl = math.copysign(0.45, sd) * k * s
            B.line([pt(-a - 0.45 * k * s, sd * k * s + fl), pt(-a, sd * k * s), pt(a, sd * k * s),
                    pt(a + 0.45 * k * s, sd * k * s + fl)], R28MV_BRIDGE, L, order + 1, bk_lw(0.3, k))
    elif kind == "stepping stones":
        for f in (-0.75, -0.25, 0.25, 0.75):
            c_ = pt(f * a, 0.0)
            B.fill([circle_pts(c_[0], c_[1], 0.55 * k * s, 12)], WHITE, L, order)
            B.fill([circle_pts(c_[0], c_[1], 0.36 * k * s, 12)], col, L, order + 1)
    else:                                                 # a footbridge (any other new crossing alike)
        B.line([pt(-a, 0.0), pt(a, 0.0)], WHITE, L, order, bk_lw(1.0, k))
        B.line([pt(-a, 0.0), pt(a, 0.0)], col, L, order + 1, bk_lw(0.55, k))
        for f in (-a, a):
            B.line([pt(f, -0.6 * k * s), pt(f, 0.6 * k * s)], col, L, order + 1, bk_lw(0.3, k))


def r28mv_hub(B, px, py, role, k, L, order, s=1.0):
    """a hub at (px, py): a ring (R28_MARKERS hubs) round its place, which stays visible inside (the bridge it sits
    at); a transit hub with a filled centre"""
    rr = R28MV_HUB_R * k * s
    ring = circle_pts(px, py, rr, 36)
    ring = ring + [ring[0]]
    col = R28MV_MK["hubs"]
    B.line(ring, WHITE, L, order, bk_lw(1.0 * s, k))
    B.line(ring, col, L, order + 1, bk_lw(0.5 * s, k))
    if role == "transit":
        B.fill([circle_pts(px, py, 1.0 * k * s, 20)], col, L, order + 1)


def r28mv_disc(B, cx, cy, n, col, k, L, order, r_mm=R28MV_DISC, pt=7.0):
    """a numbered callout: a disc in its group's colour, the number white, bold, centred by its measured width"""
    B.fill([circle_pts(cx, cy, r_mm * k, 24)], col, L, order)
    h = bk_hk(pt, k)
    t_ = str(n)
    B.text(t_, cx - 0.5 * r28mv_tw(t_, h, True), cy - 0.5 * h, h, WHITE, L, order=order + 1, font=FONT_TITLE,
           bold=True)


def r28mv_dot(B, px, py, col, k, L, order, hollow=False):
    """the index chart's mark: today a ring, with the proposal a dot"""
    rr = 0.85 * k
    if hollow:
        ring = circle_pts(px, py, rr, 16)
        B.fill([ring], WHITE, L, order)
        B.line(ring + [ring[0]], INK2, L, order + 1, bk_lw(0.3, k))
    else:
        B.fill([circle_pts(px, py, rr, 16)], col, L, order + 2)


def r28mv_sample(B, kind, arg, x0, yc, k, L, order=67):
    """a 5 mm key sample of a map symbol, drawn as on the map: road (arg = its style), bus (arg = dashed), truck,
    cross (arg = the crossing's kind, across a short piece of stream), hub (arg = role)"""
    x1 = x0 + 5.0 * k
    if kind == "road":
        r28mv_road_line(B, [(x0, yc), (x1, yc)], arg, k, L, order)
    elif kind == "bus":
        r28mv_bus_line(B, [(x0, yc), (x1, yc)], k, L, order, dashed=arg, side=0.0)
    elif kind == "truck":
        for d in dashes([(x0, yc), (x1, yc)], 2.4 * k, 1.2 * k):
            B.line(d, INK, L, order, bk_lw(0.6, k))
    elif kind == "cross":
        B.fill([rect(x0, yc - 0.9 * k, x1, yc + 0.9 * k)], r28mv_pale(MPL["water"], 0.3), L, order)
        r28mv_cross(B, x0 + 2.5 * k, yc, (0.0, 1.0), arg, k, L, order + 1, s=0.6)
    elif kind == "hub":
        r28mv_hub(B, x0 + 2.5 * k, yc, arg, k, L, order, s=0.7)


def r28mv_list(B, head, keyrow, entries, x0, y, cw, k, L):
    """v50 (MIRAQUA 28 Oct, P09.2): one group of the proposal's list in a column cw wide from y down: its name, the
    key of its symbols as the map draws them (keyrow [(kind, arg, label)]), then each entry [(number or None, colour,
    text)]: the number disc in the group's colour, **name · change** · note, wrapped, 7.5 pt. Returns the y under it."""
    h8, h75, h7 = bk_hk(8.0, k), bk_hk(7.5, k), bk_hk(7.0, k)
    yb = y - h8
    B.text(head.upper(), x0, yb, h8, INK, L, order=66, font=FONT_TITLE, bold=True)
    yb -= 2.1 * h8
    cx = x0
    for kind, arg, lab in keyrow:
        wl = 6.2 * k + r28mv_tw(lab, h7) + 3.0 * k
        if cx > x0 and cx + wl > x0 + cw:
            cx, yb = x0, yb - 2.0 * h7
        r28mv_sample(B, kind, arg, cx, yb + 0.5 * h7, k, L)
        B.text(lab, cx + 6.2 * k, yb, h7, INK, L, order=66, font=FONT_TITLE)
        cx += wl
    yb -= (2.7 if keyrow else 0.6) * h75
    tx, tw_ = x0 + 4.1 * k, cw - 4.1 * k
    last = yb
    for n_, col, txt in entries:
        if n_ is not None:
            r28mv_disc(B, x0 + 1.55 * k, yb + 0.5 * h75, n_, col, k, L, 66, r_mm=1.55)
        for ln in r28mv_lines(txt, tw_, h75):
            r28mv_draw_line(B, ln, tx, yb, h75, INK, L)
            last = yb
            yb -= R28MV_LEAD * h75
        yb -= 0.55 * h75
    return min(last - 0.5 * h75, yb + R28MV_LEAD * h75)


# ------------------------------------------------------------ p.09 the proposal map (P09.1, P09.2)
def draw_mv_proposal(S, B, x, y, w, U, M):
    """v46 (Prompt 3, p.10): THE PROPOSAL, the whole site frame at 1:10,000 on the frame's axes (one strip, G7).
    v50 (MIRAQUA 28 Oct, P09.1, redrawn from scratch: the multiplied green glow buried the streets, the names
    overlapped): one line on what the map shows; a pale base (b_base through R28Pale, G6); reach on foot from the
    masterplan's hubs (mv_reach on the network with the proposal) as thin streets in the three crisp classes of
    R28_REACH, never a glow, never multiplied; the roads by category as line types on a white casing (kept thin,
    calmed with ticks, pedestrian heavy, shared dashed; the bus line dashed beside its streets); the crossings as
    symbols across the stream (bridge kept: two decks, named K1-K6; footbridge: one bar; stepping stones: four
    stones), the hubs as rings (transit: a filled centre); every road, new crossing and hub a numbered disc in its
    group's colour (R28_MARKERS), on a leader where it sits off its point, placed without overlaps (label_place, G4).
    Under the map the scale bar, north arrow and the reach key, then (P09.2) the list in three groups (roads;
    bridges and crossings; hubs), each with the key of its symbols and its entries **name · change** · note, numbered
    upstream to downstream; then (P09.3) the index change chart (r28mv_index_change). Crops drw_proposal and
    drw_index_change. Returns the y below."""
    L = "LU_BOARD::Proposal"
    F = S.F
    B.text(u"THE PROPOSAL · HOW PEOPLE WILL MOVE", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    k = 120.0 * U / BK_AW
    h9, h75, h7 = bk_hk(9.0, k), bk_hk(7.5, k), bk_hk(7.0, k)
    MR = mv_with_masterplan(S, M)
    R2 = MR.get("R") if MR else None
    hubs = [hb for hb in M.get("hubs") or [] if _xy1(hb.get("xy"))]
    hub_xy = [_xy1(hb["xy"]) for hb in hubs]
    rw = R28_REACH[-1][0]
    top = y - 1.2 * U                                     # the crop's top
    mw = F.w * 1000.0 * k / B_DEN
    what = (u"What it shows: **reach on foot** from the {} hubs along today's streets (green), and **the roads, "
            u"crossings and hubs** of the masterplan, numbered as in the list below.").format(len(hub_xy))
    yb = top - 0.5 * k - h9
    for ln in r28mv_lines(what, mw, h9):
        r28mv_draw_line(B, ln, x, yb, h9, INK, L)
        yb -= R28MV_LEAD * h9
    V, k, ss, r = b_view(F, x, yb + R28MV_LEAD * h9 - 2.5 * k, U)
    CB = ClipB(B, r)
    B.fill([rect(*r)], WHITE, L, 1)
    b_base(S, R28Pale(CB), V, k, L)
    # reach on foot: thin streets, three crisp classes (R28_REACH), normal blend
    km = [0.0] * len(R28_REACH)
    src = None
    if R2 and hub_xy:
        cost = mv_reach(R2, hub_xy, rw)
        pieces = R2["pieces"]

        def reach_cls(pi):
            p = pieces[pi]
            if p["prop"]:                                 # the crossings' network joins: drawn as crossings
                return None
            c_ = min(cost.get(p["a"], 1e12), cost.get(p["b"], 1e12))
            return next((j for j, rc in enumerate(R28_REACH) if c_ <= rc[0]), None)
        for P, c_ in sorted(_runs(R2["chains"]["walk_a"], pieces, R2["xy"], reach_cls, set(R2["inside"]), F),
                            key=lambda rr_: -rr_[1]):
            CB.line(V.P(P), C(R28_REACH[c_][2]), L, 20 + len(R28_REACH) - c_, bk_lw(R28MV_REACH_W[c_], k))
            km[c_] += pl_length(P) / 1000.0
        LOG.append(u"Proposal map: reach on foot from {} hubs (Tobler, with the masterplan's crossings): {} km of "
                   u"street and footway in the frame.".format(len(hub_xy), u" / ".join(
                       u"{} {:.1f}".format(lab_, km_) for (lim_, lab_, hx_), km_ in zip(R28_REACH, km))))
        src = bcite("Reach on foot: the shortest walking cost from the nearest masterplan hub along the OSM streets "
                    "and footways and the masterplan's crossings (the board's movement network with the proposal), "
                    "each street piece timed by Tobler (1993) on the survey terrain and given as flat-ground metres, "
                    "in three classes (0-100, 100-400, 400-800 m) to {:.0f} m, the walking radius of the movement "
                    "method (bergama_movement v1). Computed; weakest assumption: every crossing open and every "
                    "footway walkable all year.".format(rw))
    else:
        LOG.append("Proposal map: no street network with the masterplan (OSM) or no hubs, so no reach on foot drawn.")

    def mm(p):                                            # board -> booklet mm from the map's lower-left corner
        return ((p[0] - r[0]) / k, (p[1] - r[1]) / k)
    segs, taken, roads, cross, kept, hubl = [], [], [], [], [], []
    for rd in M.get("roads") or []:                       # the roads by category
        P = _xy_list(rd.get("xy"))
        runs = F.clip_line(P) if len(P) >= 2 else []
        if not runs:
            continue
        ch = rd.get("change", "kept")
        st = R28MV_ROAD.get(ch, R28MV_ROAD["kept"])
        for run in runs:
            Q = V.P(run)
            r28mv_road_line(CB, Q, st, k, L, 30)
            segs += [(mm(a), mm(b)) for a, b in zip(Q[:-1], Q[1:])]
        run = max(runs, key=pl_length)
        q, t = pl_point_at(run, pl_length(run) / 2.0)
        chl = st[0] if ch in R28MV_ROAD else ch
        roads.append(dict(grp="roads", ch=ch, chlab=chl, name=rd.get("name", u""), P=P, at=V.p(q[0], q[1]), col=st[1],
                          text=r28mv_entry(rd.get("name", u""), chl, r28mv_note_text(rd.get("note"), (ch, chl)))))
    tr = M.get("truck_route")
    if tr and len(_xy_list(tr.get("xy"))) >= 2:
        P = _xy_list(tr["xy"])
        runs = F.clip_line(P)
        for run in runs:
            Q = V.P(run)
            for d in dashes(Q, 2.4 * k, 1.2 * k):
                CB.line(d, INK, L, 35, bk_lw(0.6, k))
            segs += [(mm(a), mm(b)) for a, b in zip(Q[:-1], Q[1:])]
        if runs:
            run = max(runs, key=pl_length)
            q, t = pl_point_at(run, pl_length(run) * 0.35)
            roads.append(dict(grp="roads", ch="truck", chlab=u"rerouted", name=tr.get("name", u"truck route"), P=P,
                              at=V.p(q[0], q[1]), col=INK, text=r28mv_entry(r28mv_cap(tr.get("name", u"truck route")),
                                                                            u"rerouted", tr.get("note", u""))))
    else:
        LOG.append("Proposal map: truck route pending in the masterplan (movement.truck_route is null).")
    bus_dash = set()
    for rt in M.get("routes") or []:                      # the town bus line extended to K4, a later step
        P = _xy_list(rt.get("xy"))
        runs = F.clip_line(P) if len(P) >= 2 else []
        if not runs:
            continue
        later = bool(rt.get("later")) or str(rt.get("status", "")).lower() in ("later", "proposed", "future")
        bus_dash.add(later)
        for run in runs:
            Q = V.P(run)
            r28mv_bus_line(CB, Q, k, L, 36, dashed=later)
            segs += [(mm(a), mm(b)) for a, b in zip(Q[:-1], Q[1:])]
        run = max(runs, key=pl_length)
        q, t = pl_point_at(run, pl_length(run) * 0.35)
        chl = u"later step" if later else u"bus line"
        roads.append(dict(grp="roads", ch="bus", chlab=chl, name=r28mv_cap(rt.get("name", u"")), P=P,
                          at=V.p(q[0], q[1]), col=R28MV_BUS[1], text=r28mv_entry(
                              r28mv_cap(rt.get("name", u"")), chl, r28mv_note_text(rt.get("note"), ("later step", "later")))))
    for c in M.get("crossings") or []:                    # crossings, symbols across the stream
        p = _xy1(c.get("xy"))
        if not p or not F.inside(p[0], p[1]):
            continue
        px, py = V.p(p[0], p[1])
        nrm = stream_normal(S, p[0], p[1]) or (0.0, 1.0)
        a_ = V.p(p[0] + nrm[0], p[1] + nrm[1])
        ln_ = math.hypot(a_[0] - px, a_[1] - py) or 1.0
        kind = c.get("kind", "footbridge")
        r28mv_cross(CB, px, py, ((a_[0] - px) / ln_, (a_[1] - py) / ln_), kind, k, L, 40)
        q_ = mm((px, py))
        taken.append((q_[0] - R28MV_SYM - 0.3, q_[1] - R28MV_SYM - 0.3, q_[0] + R28MV_SYM + 0.3, q_[1] + R28MV_SYM + 0.3))
        nm = c.get("name", u"") or u""
        if kind == "bridge kept":
            kept.append((nm.replace(u" bridge", u""), px, py))
        else:
            cross.append(dict(grp="crossings", ch=kind, at=(px, py), text=r28mv_entry(r28mv_cap(nm), u"",
                                                                                     c.get("note", u""))))
    for hb in hubs:                                       # hubs, rings
        p = _xy1(hb["xy"])
        if not F.inside(p[0], p[1]):
            continue
        px, py = V.p(p[0], p[1])
        role = str(hb.get("role", "") or "")
        r28mv_hub(CB, px, py, role, k, L, 50)
        q_ = mm((px, py))
        rr = R28MV_HUB_R + 0.4
        taken.append((q_[0] - rr, q_[1] - rr, q_[0] + rr, q_[1] + rr))
        bits = [u"sub-hub in the bed"] if hb.get("sub_hub") else []
        if hb.get("bus_stop"):
            try:
                bits.append(u"bus stop {}, {:.0f} m".format(hb["bus_stop"], float(hb.get("bus_stop_m"))))
            except Exception:
                bits.append(u"bus stop {}".format(hb["bus_stop"]))
        hubl.append(dict(grp="hubs", ch=role, at=(px, py), text=r28mv_entry(
            r28mv_title(hb.get("name", u"")), (role + u" hub") if role else u"hub", u" · ".join(bits))))
    # numbers: roads (the bus line last), new crossings, hubs, each upstream (left) to downstream
    roads.sort(key=lambda d_: (d_["ch"] in ("bus", "truck"), d_["at"][0]))
    cross.sort(key=lambda d_: d_["at"][0])
    hubl.sort(key=lambda d_: d_["at"][0])
    for n_, d_ in enumerate(roads + cross + hubl):
        d_["n"] = n_ + 1
    # G4: the kept bridges' names, then the numbered discs, each clear of the symbols, the roads and each other
    bounds = (0.3, 0.3, (r[2] - r[0]) / k - 0.3, (r[3] - r[1]) / k - 0.3)
    its = [dict(x=mm((px, py))[0], y=mm((px, py))[1], wh=_r28mv_wh(r28mv_tw(nm, h7, True) / k, h7 / k), rank=0)
           for nm, px, py in kept]
    for i_, (bx, lead, f_) in place_labels_all(its, taken, bounds, segs, sizes=(1.0,), pad=0.3).items():
        nm, px, py = kept[i_]
        B.text(nm, r[0] + bx[0] * k, r[1] + bx[1] * k, h7, INK, L, order=64, font=FONT_TITLE, bold=True)
        if lead:
            e_ = lp_leader_end(bx, mm((px, py)))
            B.line([(px, py), (r[0] + e_[0] * k, r[1] + e_[1] * k)], INK2, L, 63, bk_lw(0.12, k))
    calls = hubl + cross + roads                          # placed in this order: hubs, crossings, roads
    dd = 2.0 * R28MV_DISC
    its = [dict(x=mm(c_["at"])[0], y=mm(c_["at"])[1], wh=_r28mv_wh(dd, dd), rank=0) for c_ in calls]
    got = place_labels_all(its, taken, bounds, segs, sizes=(1.0,), pad=0.35)
    for i_, c_ in enumerate(calls):
        if i_ not in got:
            LOG.append(u"Proposal map: no room for callout {} ({}).".format(c_["n"], r28mv_parse(c_["text"])[0][0]))
            continue
        bx = got[i_][0]
        col = R28MV_MK[c_["grp"]]
        cx, cy = r[0] + 0.5 * (bx[0] + bx[2]) * k, r[1] + 0.5 * (bx[1] + bx[3]) * k
        ax, ay = c_["at"]
        dl = math.hypot(cx - ax, cy - ay)
        if dl > (R28MV_DISC + 0.9) * k:                   # off its point: a leader, from the symbol's edge
            ux, uy = (cx - ax) / dl, (cy - ay) / dl
            s0 = {"hubs": R28MV_HUB_R, "crossings": 0.8}.get(c_["grp"], 0.0) * k
            B.line([(ax + ux * s0, ay + uy * s0), (cx - ux * R28MV_DISC * k, cy - uy * R28MV_DISC * k)], col, L, 62,
                   bk_lw(0.15, k))
            if c_["grp"] == "roads":
                B.fill([circle_pts(ax, ay, 0.4 * k, 12)], col, L, 63)
        r28mv_disc(B, cx, cy, c_["n"], col, k, L, 64)
    b_frame(B, r, k, L)
    low = b_foot(B, F, x, r[1], ss, k, L)
    if src:                                               # the reach key, right of the scale bar and north arrow
        kx, yc = x + B_SB_M * ss + 20.0 * k, r[1] - 3.1 * k
        cx = kx + r28mv_draw_line(B, r28mv_lines(u"**Reach on foot** from the nearest hub, slope counted {}:".format(
            src), 1e9, h75)[0], kx, yc - 0.5 * h75, h75, INK, L) + 2.5 * k
        for (lim_, lab_, hx_), wl in zip(R28_REACH, R28MV_REACH_W):
            B.line([(cx, yc), (cx + 6.0 * k, yc)], C(hx_), L, 66, bk_lw(wl, k))
            B.text(lab_, cx + 7.2 * k, yc - 0.5 * h7, h7, INK, L, order=66, font=FONT_TITLE)
            cx += 7.2 * k + r28mv_tw(lab_, h7) + 4.0 * k
    # P09.2: the list in three groups, each with the key of its symbols
    gap = 6.0 * k
    cw = (mw - 2.0 * gap) / 3.0
    have = set(d_["ch"] for d_ in roads)
    keys = {"roads": [("road", R28MV_ROAD[c_], R28MV_ROAD[c_][0]) for c_ in ("kept", "calmed", "pedestrian", "shared",
                                                                             "relocated") if c_ in have] +
            ([("truck", None, u"truck route, rerouted")] if "truck" in have else []) +
            [("bus", d_, R28MV_BUS[0] if d_ else u"bus line") for d_ in sorted(bus_dash)],
            "crossings": ([("cross", "bridge kept", u"bridge kept")] if kept else []) +
            [("cross", kd, kd) for kd in ("footbridge", "stepping stones") if kd in set(d_["ch"] for d_ in cross)],
            "hubs": [("hub", ro, (ro + u" hub") if ro else u"hub") for ro in ("walking", "transit", "")
                     if ro in set(d_["ch"] for d_ in hubl)]}
    ents = {"roads": [(d_["n"], R28MV_MK["roads"], d_["text"]) for d_ in roads],
            "crossings": ([(None, None, u"**{} · bridges kept** · named on the map".format(u", ".join(
                nm for nm, px, py in sorted(kept, key=lambda q__: q__[1]))))] if kept else []) +
            [(d_["n"], R28MV_MK["crossings"], d_["text"]) for d_ in cross],
            "hubs": [(d_["n"], R28MV_MK["hubs"], d_["text"]) for d_ in hubl]}
    ly = low - 3.0 * k
    lb = ly
    for j, (g_, head) in enumerate(R28MV_GROUPS):
        if keys[g_] or ents[g_]:
            lb = min(lb, r28mv_list(B, head, keys[g_], ents[g_], x + j * (cw + gap), ly, cw, k, L))
    crop_panel("proposal", x - 0.5 * k, lb - 0.5 * k, r[2] + 0.5 * k, top,
               u"How people will move · reach on foot, roads, crossings and hubs of the masterplan", crop_scale(ss),
               crop_legend(r28mv_base_leg()))
    low = lb - 0.5 * k
    if R2 and roads:                                      # P09.3: the index today and with the proposal
        low = r28mv_index_change(S, B, x, low - 8.0 * k, k, L, R2, roads)
    else:
        LOG.append("Index change: no street network with the masterplan (OSM) or no road, so no chart.")
    return low - 0.4 * U


# ------------------------------------------------------------ p.09 walk and car index, today and with the proposal (P09.3)
def r28mv_index_change(S, B, x, ytop, k, L, R2, roads):
    """v50 (MIRAQUA 28 Oct, P09.3; replaces the commercial spines map, which repeated p.07): the walk and car index
    today and with the proposal on each road of the masterplan and on the bus line (mv_line_index on the run with the
    proposal, R2: the length-weighted mean of the street pieces within MV_LINE_D of the line; 100 = the busiest piece
    today, per mode), as two small charts with one 0-100 axis each (today a ring, with the proposal a dot in the
    road's colour), the roads grouped by change and numbered as on the map; under them what the model leaves out:
    calmed and shared roads keep their cars and the bus line is not modelled, so their change comes only through the
    network. Crop drw_index_change, drawn for its width on the booklet page (bk_w). Returns the y below."""
    keys = ("walk_b", "walk_a", "car_b", "car_a")
    rows = [(d_, mv_line_index(R2, d_["P"], keys)) for d_ in roads]
    rank = dict((c_, j) for j, c_ in enumerate(R28MV_CHANGE_ORDER))
    rows.sort(key=lambda rv: (rank.get(rv[0]["ch"], len(rank)), rv[0]["n"]))
    LOG.append(u"Index change (walk today -> with, car today -> with): " + u"; ".join(
        u"{} {} -> {}, {} -> {}".format(d_["name"], *[u"n/a" if v.get(k_) is None else u"{:.0f}".format(v[k_])
                                                      for k_ in keys]) for d_, v in rows))
    h9, h75, h7 = bk_hk(9.0, k), bk_hk(7.5, k), bk_hk(7.0, k)
    W = S.F.w * 1000.0 / B_DEN                            # mm: as wide as the map
    PW, VW, PG = 70.0, 15.0, 6.0                          # mm: a chart's plot, its values, the gap between the two
    X2 = W - PW - VW
    X1 = X2 - PG - PW - VW
    vals = [v_ for d_, v in rows for v_ in v.values() if v_ is not None]
    vmax = max(100.0, 25.0 * math.ceil(max(vals or [0.0]) / 25.0))
    yb = ytop - 0.5 * k - h9
    wt = r28mv_draw_line(B, r28mv_lines(u"**Walk and car index**, today and with the proposal, on the masterplan's roads "
                                        u"{}".format(bcite(r28mv_src_mv())), 1e9, h9)[0], x, yb, h9, INK, L)
    sx = x + wt + 8.0 * k                                 # what the marks are
    r28mv_dot(B, sx, yb + 0.5 * h7, None, k, L, 62, True)
    B.text(u"today", sx + 1.6 * k, yb, h7, INK2, L, order=66, font=FONT_TITLE)
    sx += 1.6 * k + r28mv_tw(u"today", h7) + 4.0 * k
    r28mv_dot(B, sx, yb + 0.5 * h7, INK2, k, L, 62)
    B.text(u"with the proposal, in the road's colour", sx + 1.6 * k, yb, h7, INK2, L, order=66, font=FONT_TITLE)
    yh = yb - 5.5 * k
    B.text(u"Road · change", x + 4.2 * k, yh, h7, INK2, L, order=66, font=FONT_TITLE, bold=True)
    for X, lab in ((X1, u"Walking index"), (X2, u"Driving index")):
        B.text(lab, x + X * k, yh, h75, INK, L, order=66, font=FONT_TITLE, bold=True)
        B.text(u"today / with", x + (X + PW + 2.0) * k, yh, h7, INK2, L, order=66, font=FONT_TITLE)
    y0, rh = yh - 2.0 * k, 5.0 * k
    yend = y0 - len(rows) * rh
    for X in (X1, X2):                                    # the axis: light lines every 25, numbers under the rows
        for g_ in range(0, int(vmax) + 1, 25):
            gx = x + (X + PW * g_ / vmax) * k
            B.line([(gx, y0), (gx, yend)], mix(INK2, WHITE, 0.7), L, 60, bk_lw(0.12, k))
            t_ = u"{}".format(g_)
            B.text(t_, gx - 0.5 * r28mv_tw(t_, h7), yend - 1.2 * k - h7, h7, INK2, L, order=66, font=FONT_TITLE)
    na = False
    nmax = (X1 - 7.0) * k                                 # the name column's width
    for i, (d_, v) in enumerate(rows):
        yc = y0 - (i + 0.5) * rh
        r28mv_disc(B, x + 1.55 * k, yc, d_["n"], R28MV_MK["roads"], k, L, 64, r_mm=1.55)
        ln = r28mv_lines(u"**{}** · {}".format(d_["name"], d_["chlab"]), 1e9, h75)[0]
        hh = max(h7, min(h75, h75 * nmax / max(1e-9, r28mv_line_w(ln, h75))))
        r28mv_draw_line(B, r28mv_lines(u"**{}** · {}".format(d_["name"], d_["chlab"]), 1e9, hh)[0], x + 4.2 * k,
                        yc - 0.5 * hh, hh, INK, L)
        for X, kb, ka in ((X1, "walk_b", "walk_a"), (X2, "car_b", "car_a")):
            b_, a_ = v.get(kb), v.get(ka)
            if b_ is None or a_ is None:
                B.text(u"n/a", x + (X + PW + 2.0) * k, yc - 0.5 * h7, h7, INK2, L, order=66, font=FONT_TITLE)
                na = True
                continue
            xb, xa = x + (X + PW * min(b_, vmax) / vmax) * k, x + (X + PW * min(a_, vmax) / vmax) * k
            B.line([(xb, yc), (xa, yc)], mix(INK2, WHITE, 0.4), L, 61, bk_lw(0.45, k))
            r28mv_dot(B, xb, yc, None, k, L, 62, True)
            r28mv_dot(B, xa, yc, d_["col"], k, L, 62)
            vt = u"{:.0f} / ".format(b_) + (u"**{:.0f}**" if round(a_) != round(b_) else u"{:.0f}").format(a_)
            r28mv_draw_line(B, r28mv_lines(vt, 1e9, h75)[0], x + (X + PW + 2.0) * k, yc - 0.5 * h75, h75, INK, L)
    yn = yend - 1.2 * k - h7 - 4.0 * k - h75
    yn = r28mv_para(B, u"**Not modelled**: calmed and shared roads keep their cars and the bus line is not in the "
                       u"model, so their index moves only through the **network** (cars off the pedestrian roads, the "
                       u"crossings as walking links, the hubs as destinations).", x, yn, W * k, h75, INK2, L)
    yn = r28mv_para(B, u"**Index 100** = the busiest street piece today, per mode; a road = the mean of the street "
                       u"pieces within {:.0f} m of its line, by length{}".format(
                           MV_LINE_D, u"; n/a = none that close." if na else u"."), x, yn - 0.3 * h75, W * k, h75,
                    INK2, L)
    bot = yn + R28MV_LEAD * h75 - 0.5 * h75
    crop_panel("index_change", x - 0.5 * k, bot - 0.5 * k, x + (W + 0.5) * k, ytop,
               u"Walk and car index · today and with the proposal · roads of the masterplan")
    CROP_PANELS[-1]["bk_w"] = W + 1.0
    return bot - 0.5 * k
