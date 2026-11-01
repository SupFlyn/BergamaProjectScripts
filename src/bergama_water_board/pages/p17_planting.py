# p.17 planting and water (water board v6; revision 30 Oct 2026, T7: booklet p16 and p17). Two booklet pages:
#   page A (p17_page, crop wb_plants, booklet p16 "Which plant goes where"): two plan windows at one standard scale on
#        the shared basemap (M3 "detailed": streets, M11 buildings with roof ridges, M5 water), farms and orchards as one
#        field texture and one symbol per area (D7), the water spaces of the zone base, the planting as species
#        areas in wet-to-dry bands (R2-C _p17_drift_plan, R12-R14: drifts, overlapping crowns, no rows), July shade, the
#        four section lines of page B from the cut registry (W1, F2, S4, F4), the hubs and the numbered water spaces;
#        beside them the key map (M4: study-area outline + both windows) and the legend; under them the numbered list,
#        the planting logic (round 3, P16.3: band map, shares, height ranking) and the species catalogue (photo,
#        detailed section and plan from M6, foliage, water, role) with the giant reed "remove" card.
#        Round 4 (S6b, P17.1-P17.7, booklet p17): rebuilt as three rows (handover/S6b_p17_design_spec.md): key map
#        (km_map) over the legend | plan A | plan B at the largest standard scale that fits, each plan with its own
#        list; map_draw layers (muted base, D9 tint, study clip + line), R01 red section lines, north_items, mk_marker;
#        the band map grouped with its key; shrub groups on the open ground (pla_low_plan); every text in the cell's
#        TextPage (build_board text_page / check_text).
#   booklet p18 (round 4, D2, N3 a; p18_page, crops wb_plants_b1 = p18a F2 + F4, wb_plants_b2 = p18b W1 + S4): two
#        whole booklet pages, one cut per row at 1:250 in the LEFT block template (title strip, drawing, side column:
#        key map, numbered keywords, legend, level marks outside the drawing, scale bar); F2 / F4 trimmed to their
#        designed bank parts with break marks; W1's way down drawn (sitting steps, as p13); people (one pen_black set),
#        mixed planting groups + the shrub and flower layer, sky v2, background houses v2; zoom insets at 1:100. Every
#        word through the page's TextPage (G-R4-1).
# build_board calls P17_TITLE, p17_page(pg, box, opt, log) and P18_TITLES[page], p18_page(pg, box, page, opt, log);
# each returns [(crop id, bbox, scale denominator)].

P17_TITLE = u"PLANTING AND WATER · where each plant goes around the water spaces"
P17_W = 377.0                        # the most a page takes, mm (the booklet's A3 panel at 1:1)
P17_CAT = ("reed", "mint", "soft_rush", "loosestrife", "willow", "tamarisk", "chaste", "ash", "plane", "olive",
           "rosemary", "lavender")   # the catalogue, wet to dry: every species the two pages draw
P17_DENS = (1000.0, 2000.0, 2500.0, 5000.0)   # the plan windows: the first standard scale at which both fit
P17_BAR = {1000.0: (0, 10, 20, 50), 2000.0: (0, 20, 50, 100), 2500.0: (0, 20, 50, 100), 5000.0: (0, 50, 100, 200),
           10000.0: (0, 50, 100, 200), 20000.0: (0, 200, 500)}   # labels at least 2 mm apart
P17_FS, P17_HEAD = FS_MIN, 3.4       # label and heading sizes, mm
# round 3 (D2, P16.4): the summer strip is no longer drawn in plan (no squiggle); it is shown in the sections only
P17_ZONE = {"WT": ("CBEDE5", "8DB8AF"), "WD": ("C1D3DB", "889EA8"), "GR": ("EEEADD", "C9C3B0"),
            "WS": ("EEE8D6", "C9BFA6"), "WP": ("E6EEDD", "B9C6A2"), "ARM": ("B9D7DE", "5D7F8D"),
            "WIDEN": ("D3E4E8", "889EA8")}
# July shade: (hours under, colour, label, hatch spacing mm): drawn as an opaque fine hatch (G9: no alpha), so the
# water texture under it stays visible
P17_SHADE = ((2.0, "E6DCC6", u"under 2 h", 2.0), (5.0, "CDBF9F", u"2-5 h", 1.2), (99.0, "A99A78", u"over 5 h", 0.7))
P17_NEAT = 0.09                      # a map's neatline, mm (0.25 pt; D4: the only frame kept)
P17_DENS_PLAN = {"space": 0.65, "bank": 0.5}   # P16.2 (U14 "çok dolu"): plan planting density (drawing rule)
P17_CLEAR_M = 10.0                   # P16.2: an open clearing this far round each place people use (drawing rule)
# the four wet-to-dry bands (P17_BANDS) by the words of the page intro; one colour each (PLAN §2 palette), the same on
# p16 (plans, shares) and p17 (the band row under each section)
P17_BAND_NAME = (u"at the water", u"banks that flood", u"moist ground", u"dry tops")
P17_BAND_COL = ("5C7A86", "A2B6B5", "89986A", "8E8F8A")
P17_BASIN = dict(kerb_h=0.30, depth=1.10, media=0.80, kerb_t=0.15)   # lined basin cell: drawing values (no source)
P17_ARM_W = 3.0                      # the side arm, m either side of its line (masterplan R28DT_ARM_M)
# the side arm the F4 cut crosses, survey m, while the masterplan writes no corridor geometry: its middle part read off
# the masterplan plan (p.23, georeferenced on the analysis frame, +-5 m); masterplan_results.json "corridor" "arms"
# replaces it when present (log line otherwise)
P17_ARM_FALLBACK = [(30666.1, 31215.0), (30680.9, 31177.7), (30722.8, 31141.0), (30768.4, 31113.1),
                    (30804.0, 31090.5), (30834.3, 31057.9), (30869.1, 31026.4), (30894.6, 31025.7),
                    (30918.6, 31043.1)]
# plan planting (G9, M6 niches): the species of each water space and of the stream banks, wet to dry; the band
# position t (0 = the water's edge, 1 = dry upper ground) of the spaces planted as one band; the bank band's width
# round 4 (S6b, P17.1-P17.7): page A rebuilt (drawing rules, never printed)
P17_PAGE = "p17"                     # the booklet page id: TextPage, study clip counts, map_draw log
P17_G = 5.0                          # mm between blocks
P17_LW = 62.0                        # the left column of row 1: key map over the legend, mm
P17_HEADH = 5.0                      # the heading strip over each plan (letter, name, scale), mm
P17_BARH = 6.0                       # the scale-bar row under each plan, mm
P17_LOGIC_H = 40.0                   # the logic band (band map + key, foliage, height chart), mm
P17_KM_MIN = 26.0                    # the key map's least height, mm
P17_BAND_DENS = (5000.0, 10000.0, 20000.0)   # the band map: booklet scales only (the old 2x / 4x gave 1:4,000 / 1:8,000)
P17_BAND_W = 60.0                    # the band map's most width, mm
P17_SHRUB = ("chaste", "rosemary", "lavender")   # P17.6 (D7): open planted ground beyond the bank band, moist to dry
P17_SHRUB_DENS = 0.5                 # their density (plants.py pla_low_plan)


P17_MIX = {"WD": ("soft_rush", "loosestrife"), "GR": ("plane", "ash", "chaste"), "WS": ("olive", "rosemary", "lavender"),
           "WP": ("soft_rush", "loosestrife", "willow", "tamarisk", "chaste", "ash"),
           "ARM": ("soft_rush", "loosestrife", "willow"),
           "BANK": ("soft_rush", "loosestrife", "willow", "tamarisk", "chaste", "ash", "plane", "olive", "rosemary",
                    "lavender")}
P17_MIX_T = {"WD": 0.06, "GR": 0.50, "WS": 0.86}
P17_BAND_M = 35.0                    # the stream-bank planting reaches this far from the water, m (design: the corridor)
P17_WP_M = 60.0                      # the wetland's wet-to-dry band, m from the water (its depth across, zone base WP)
P17_ARM_BAND = 10.0                  # the side arm's planting either side of its water, m (drawing value)
P17_KEYCOL = "8B3A3F"                # key maps: cut lines and windows (COL accent)
P17_WHY = {"wind": u"cuts the wind", "noise": u"cuts street noise", "shade": u"gives shade",
           "corridor": u"ecological corridor", "cleaning": u"cleans the water", "perception": u"helps perception"}
P17_WHY_PLACE = ("wind", "noise")    # purposes the design gives a group by where it stands (street edge, open top),
#                                      not a species property: printed without a species tag (handover: unverified)
# R2-C (31 Oct, R12-R14): the plans draw the planting as species AREAS in four wet-to-dry bands along the water; a
# band's edges lie halfway between the niche centres (plants.py PLA_NICHE) of neighbouring bands (_p17_band_t)
P17_BANDS = (("soft_rush", "loosestrife", "rush"), ("willow", "tamarisk"), ("ash", "plane", "chaste"),
             ("olive", "rosemary", "lavender", "stone_pine"))
P17_SHORT = {"plane": u"plane", "ash": u"ash", "willow": u"willow", "tamarisk": u"tamarisk", "chaste": u"chaste tree",
             "olive": u"olive", "rosemary": u"rosemary", "lavender": u"lavender", "loosestrife": u"loosestrife",
             "soft_rush": u"soft rush", "rush": u"sharp rush", "stone_pine": u"stone pine"}


# ---------------------------------------------------------------- small helpers
def _p17_put(pg, shapes):
    """house shapes (alpha, text and the style a cutout images) on a Page (water.py shp_put)"""
    shp_put(pg, shapes)


def _p17_size(key):
    """(height, crown) m a species is drawn at on its own: plants.py's sourced drawing size, the same in the plans and
    the catalogue"""
    sp = PLA_SPECIES[key]
    return sp["h_m"], sp["crown_m"]


def _p17_area(R):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(R, R[1:] + R[:1]))) / 2.0


def _p17_hit(R, box):
    xs, ys = [p[0] for p in R], [p[1] for p in R]
    return not (max(xs) < box[0] or min(xs) > box[2] or max(ys) < box[1] or min(ys) > box[3])


def _p17_move(items, dx, dy):
    """page items moved by (dx, dy) at 1:1, the cutout images too (xform leaves "image" items out)"""
    out = []
    for it in items:
        if it[0] == "image":
            c = it[8] if len(it) > 8 else None
            out.append(("image", it[1] + dx, it[2] + dy, it[3], it[4], it[5], it[6], it[7],
                        (c[0] + dx, c[1] + dy, c[2] + dx, c[3] + dy) if c else None))
        else:
            out += xform([it], 1.0, dx, dy)
    return out


def _p17_clip(shapes, r):
    """house shapes cut to the rectangle r = (x0, y0, x1, y1); a cutout image keeps its picture, clipped at r"""
    out = []
    for s_ in shapes:
        t = s_[0]
        if t == "poly":
            c = _p14_clip_ring(list(s_[1]), r)
            if c:
                out.append(("poly", c) + tuple(s_[2:]))
        elif t == "line":
            for run in _p14_clip_line(list(s_[1]), r):
                out.append(("line", run) + tuple(s_[2:]))
        elif t == "text":
            if r[0] <= s_[2] <= r[2] and r[1] <= s_[3] <= r[3]:
                out.append(s_)
        elif t == "image":
            x_, y_, w_, h_ = s_[1:5]
            if x_ < r[2] and x_ + w_ > r[0] and y_ < r[3] and y_ + h_ > r[1]:
                out.append(tuple(s_[:8]) + ((max(r[0], x_), max(r[1], y_), min(r[2], x_ + w_), min(r[3], y_ + h_)),))
    return out


def _p17_shp_bb(shapes):
    xs, ys = [], []
    for s_ in shapes:
        if s_[0] in ("poly", "line"):
            xs += [p[0] for p in s_[1]]
            ys += [p[1] for p in s_[1]]
        elif s_[0] == "image":
            c = s_[8] if len(s_) > 8 and s_[8] else (s_[1], s_[2], s_[1] + s_[3], s_[2] + s_[4])
            xs += [c[0], c[2]]
            ys += [c[1], c[3]]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else (0.0, 0.0, 0.0, 0.0)


def _p17_pip(p, ring):
    x, y, ins = p[0], p[1], False
    n = len(ring)
    for i in range(n):
        (xa, ya), (xb, yb) = ring[i], ring[(i + 1) % n]
        if (ya > y) != (yb > y) and x < xa + (y - ya) * (xb - xa) / (yb - ya):
            ins = not ins
    return ins


def _p17_cen(R):
    return (sum(p[0] for p in R) / len(R), sum(p[1] for p in R) / len(R))


def _p17_half(ring, a, n):
    """ring clipped to the half plane (p - a) . n >= 0 (Sutherland-Hodgman, one edge)"""
    def f(p):
        return (p[0] - a[0]) * n[0] + (p[1] - a[1]) * n[1]
    out = []
    for i in range(len(ring)):
        p, q = ring[i - 1], ring[i]
        fp, fq = f(p), f(q)
        if fq >= 0:
            if fp < 0:
                t = fp / (fp - fq)
                out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
            out.append(q)
        elif fp >= 0:
            t = fp / (fp - fq)
            out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return out if len(out) >= 3 else None


def _p17_seg_d(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _p17_line_d(p, P):
    return min(_p17_seg_d(p, a, b) for a, b in zip(P[:-1], P[1:])) if len(P) > 1 else 1e9


def _p17_along(P, d):
    """point and unit direction at arc length d along the polyline P (clamped)"""
    acc = 0.0
    for a, b in zip(P[:-1], P[1:]):
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-9:
            continue
        if acc + L >= d or b is P[-1]:
            t = max(0.0, min(1.0, (d - acc) / L))
            return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        acc += L
    a, b = P[-2], P[-1]
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return b, ((b[0] - a[0]) / L, (b[1] - a[1]) / L)


def _p17_cross(a, b, P):
    """where the segment a-b crosses the polyline P first: (point, arc length along P) or None"""
    acc = 0.0
    for p, q in zip(P[:-1], P[1:]):
        L = math.hypot(q[0] - p[0], q[1] - p[1])
        d1 = (b[0] - a[0], b[1] - a[1])
        d2 = (q[0] - p[0], q[1] - p[1])
        den = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(den) > 1e-12:
            w = (p[0] - a[0], p[1] - a[1])
            t = (w[0] * d2[1] - w[1] * d2[0]) / den
            s = (w[0] * d1[1] - w[1] * d1[0]) / den
            if 0.0 <= t <= 1.0 and 0.0 <= s <= 1.0:
                return (a[0] + d1[0] * t, a[1] + d1[1] * t), acc + s * L
        acc += L
    return None


def _p17_mark(pg, n, x, y, code, r_min=1.8, keep_pg=None):
    """round 4 (G-R4-7): a numbered water-space marker (marker.py mk_marker: the glyph centred on its ink box) in the
    colour the space is drawn in (P17_ZONE edge), centred on (x, y); its disc a keep of the page's TextPage (on
    keep_pg when pg is a scratch page), its glyph a text that may sit on that disc only. Returns its box."""
    col = (P17_ZONE.get(code) or P17_ZONE["WP"])[1]
    sh, box, _r = mk_marker(x, y, str(n), col, size_pt=7.0, r_min=r_min)
    MK_N[0] += 1
    nm = u"marker p17 %d" % MK_N[0]
    for s_ in sh:
        if s_[0] == "poly":
            pg.poly([s_[1]], fill=s_[2], stroke=s_[3], lw=s_[4] or 0.1)
            (keep_pg or pg).keep(s_[1], "marker", nm)
        elif s_[0] == "text":
            pg.text(s_[1], s_[2], s_[3], s_[4], s_[5], bold=True, align="L", allow=(nm,))
    return box


def _p17_map_fns(pg, allow=()):
    """round 4: fill / line / text functions drawing basemap-format items onto pg (map_layers, keymap): a fill keeps
    its alpha (D9 tint: transparent), a line with alpha a lighter opaque tone, "M.." text centred on its ink; the
    texts may sit on the keeps named in allow"""
    def fill_fn(rings, hx, alpha=None, nonzero=False):
        a_ = alpha if alpha is not None and alpha < 0.999 else None
        pg.poly([r_ for r_ in rings if len(r_) >= 3], fill=hx, alpha=a_)

    def line_fn(pts, hx, w_mm, dash_mm=None, alpha=None):
        d_ = None
        if dash_mm:
            d_ = list(dash_mm) if isinstance(dash_mm, (list, tuple)) else [dash_mm, dash_mm]
        if alpha is not None and alpha < 0.999:
            hx = _sec_mix(hx, "FFFFFF", 1.0 - max(0.0, float(alpha)))
        pg.line(pts, hx, w_mm, dash=d_)

    def text_fn(s, xy, size_mm, hx, bold=False, align="L"):
        a_ = str(align or u"L").upper()
        size_mm = max(size_mm, 2.12)
        x_, y_ = xy
        if a_[:1] == "M":
            ib = fm_ink_box(s, size_mm / PT, bold)
            y_ -= (ib[1] + ib[3]) / 2.0
        al = a_[-1:] if a_[-1:] in ("L", "C", "R") else "L"
        pg.text(s, x_, y_, size_mm, hx, bold=bold, align=al, allow=allow)
    return fill_fn, line_fn, text_fn


def _p17_tbox(it):
    """the real Arial box (font_metrics fm_box, y up) of a page text item"""
    return fm_box(it[1], it[2], it[3], it[4] / PT, bool(it[6]), it[7] or "L", 0.0, False)


def _p17_free(b, taken, R, pad=0.8):
    """True when box b lies 1 mm inside R and clear (pad) of every box in taken"""
    if not (R[0] + 1.0 <= b[0] and b[2] <= R[2] - 1.0 and R[1] + 1.0 <= b[1] and b[3] <= R[3] - 1.0):
        return False
    return not any(tp_hit(b, t_, pad) for t_ in taken)


def _p17_north_items(cx, cy, nd, size):
    """the north arrow (keymap north_items: arrow + N, no plate) centred on (cx, cy), north along the unit page
    direction nd; (items, box)"""
    ang = math.atan2(nd[1], nd[0]) - math.pi / 2.0
    L = size + 0.75 * max(2.12, 0.42 * size)
    its = north_items(cx - nd[0] * L / 2.0, cy - nd[1] * L / 2.0, ang, size, COL["ink_dark"])
    ps = [q for it in its if it[0] != "text" for R_ in ([it[1]] if it[0] == "line" else it[1]) for q in R_]
    ps += [(it[2][0] + dx, it[2][1] + dy) for it in its if it[0] == "text" for dx in (-1.2, 1.2) for dy in (-1.3, 1.3)]
    xs, ys = [p[0] for p in ps], [p[1] for p in ps]
    return its, (min(xs) - 0.4, min(ys) - 0.4, max(xs) + 0.4, max(ys) + 0.4)


def _p17_north_in(pg, R, nd, size, taken):
    """G-R4-9 (P17.3): the north arrow in the first free inside corner of the map R (top right first), no plate;
    returns its box (added to taken)"""
    m = 1.5 + size * 0.75
    for cx, cy in ((R[2] - m, R[3] - m), (R[0] + m, R[3] - m), (R[2] - m, R[1] + m), (R[0] + m, R[1] + m)):
        its, b = _p17_north_items(cx, cy, nd, size)
        if _p17_free(b, taken, R, 0.6):
            break
    f_, l_, t_ = _p17_map_fns(pg)
    basemap_draw(its, lambda p: p, f_, l_, t_)
    taken.append(b)
    return b


# ---------------------------------------------------------------- data, read once a run
_P17_MEMO = {}


def _p17_zones():
    """the Option A zones (survey m) from the water balance results "zones": [dict(code, label, ring, ...)]"""
    if "zones" not in _P17_MEMO:
        z = _p12_get("zones") or {}
        _P17_MEMO["zones"] = [dict(q, ring=[tuple(p) for p in q["ring"]]) for q in z.get("zones") or []
                              if len(q.get("ring") or []) >= 3]
    return _P17_MEMO["zones"]


def _p17_mp(log):
    """masterplan_results.json (the masterplan's cache folder), read once; {} when missing (logged)"""
    if "mp" not in _P17_MEMO:
        d = {}
        for fn in (os.path.join(bg_cache("bergama_masterplan"), "masterplan_results.json"),
                   os.path.join(bg_output("bergama_masterplan"), "masterplan_results.json")):
            try:
                with open(fn, "r", encoding="utf-8") as f:
                    d = json.load(f)
                break
            except Exception:
                continue
        if not d:
            log.append(u"p.17: no masterplan_results.json: hubs from the four chain places, side arm from its p.23 line")
        _P17_MEMO["mp"] = d
    return _P17_MEMO["mp"]


def _p17_hubs(log):
    """[(name, (x, y))] the hubs of the masterplan's movement, else K4 and K5 of the chain"""
    hs = ((_p17_mp(log).get("movement") or {}).get("hubs")) or []
    out = [(_p17_place_nm(h.get("name") or u""), tuple(h["xy"])) for h in hs if h.get("xy")]
    if out:
        return out
    known = [bridge_name(c_) for c_ in bridges_in_order()]
    return [(_p17_place_nm(n), p) for n, p in P12_PLACES if re.search(u"\\bK[1-6]\\b", n) or n in known]


def _p17_place_nm(n):
    """G16: a hub or place name with any K-code (K1-K6) as its real bridge name (names module)"""
    m = re.search(u"\\bK([1-6])\\b", n or u"")
    return bridge_name(u"K" + m.group(1)) if m else (n or u"")


def _p17_arms(log):
    """the side arms (survey m polylines): masterplan_results.json "corridor" "arms" (a later masterplan writes it),
    else the one read off p.23 that F4 crosses"""
    co = _p17_mp(log).get("corridor") or {}
    arms = [[tuple(p) for p in (a.get("P") if isinstance(a, dict) else a)] for a in co.get("arms") or []]
    if arms:
        return arms
    if "arm_log" not in _P17_MEMO:
        _P17_MEMO["arm_log"] = 1
        log.append(u"p.17: the masterplan writes no corridor geometry: the side arm is the one read off p.23 (+-5 m)")
    return [list(P17_ARM_FALLBACK)]


def _p17_widen(log):
    co = _p17_mp(log).get("corridor") or {}
    return [[tuple(p) for p in (w.get("ring") if isinstance(w, dict) else w)] for w in co.get("widen") or []]


def _p17_shade(log):
    """(cells [(x, y, hours)], daylight h, cell m) from the site board's shade_july.json, read once; None (one log
    line)"""
    if "shade" not in _P17_MEMO:
        r = None
        fn = os.path.join(bg_output("selinus_board"), "shade_july.json")
        try:
            with open(fn, "r", encoding="utf-8") as f:
                d = json.load(f)
            cells = [(float(c[0]), float(c[1]), float(c[2])) for c in (d.get("map") or {}).get("cells") or []]
            if cells:
                r = (cells, float(d.get("daylight_h") or 0.0), float((d.get("map") or {}).get("cell_m") or 5.0))
        except Exception:
            r = None
        if r is None:
            log.append(u"p.17: no shade_july.json ({}): the plans are drawn without July shade (run the site board v51+ "
                       u"with its environment analyses)".format(fn))
        _P17_MEMO["shade"] = r
    return _P17_MEMO["shade"]


def _p17_s4_pt(s):
    """the S4 point s m across the stream from where S4 crosses the Selinos line (north-east +), survey m"""
    if "s4" not in _P17_MEMO:
        a, b = level_ends("S4")
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
        c = _p17_cross(a, b, P12_SELINOS)
        _P17_MEMO["s4"] = ((c[0] if c else ((a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0)), u)
    o, u = _P17_MEMO["s4"]
    return (o[0] + u[0] * s, o[1] + u[1] * s)


def _p17_cut_pt(cid, t):
    """the point t m along a level cut from its first end, survey m"""
    a, b = level_ends(cid)
    L = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    return (a[0] + (b[0] - a[0]) * t / L, a[1] + (b[1] - a[1]) * t / L)


def _p17_ground(cid):
    """the surveyed ground of a T4a cut [(m along, m a.s.l.)] (LEVELS row field "ground")"""
    g = (level_cut(cid).get("ground") or {}).get("value") or []
    if len(g) < 2:
        raise RuntimeError(u"{}: no ground profile in the level module".format(cid))
    return [(float(t), float(z)) for t, z in g]


def _p17_interp(P, t):
    if t <= P[0][0]:
        return P[0][1]
    for (a, za), (b, zb) in zip(P[:-1], P[1:]):
        if a <= t <= b:
            return za + (zb - za) * (t - a) / ((b - a) or 1.0)
    return P[-1][1]


# ---------------------------------------------------------------- page A: the plan windows
def _p17_axis(R):
    """centre, long axis u, its normal v and the half extents along u and v of a ring (principal axes)"""
    c = _p17_cen(R)
    sxx = sum((p[0] - c[0]) ** 2 for p in R)
    syy = sum((p[1] - c[1]) ** 2 for p in R)
    sxy = sum((p[0] - c[0]) * (p[1] - c[1]) for p in R)
    a = 0.5 * math.atan2(2.0 * sxy, sxx - syy)
    u, v = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
    us = [(p[0] - c[0]) * u[0] + (p[1] - c[1]) * u[1] for p in R]
    vs = [(p[0] - c[0]) * v[0] + (p[1] - c[1]) * v[1] for p in R]
    return c, u, v, (min(us), max(us)), (min(vs), max(vs))


def _p17_frame_uv():
    """the analysis frame's long axis (upstream end at the left) and its normal, or None"""
    fr = basemap_frame()
    if not fr:
        return None
    cx, cy = _p17_cen(fr)
    e1 = (fr[1][0] - fr[0][0], fr[1][1] - fr[0][1])
    e2 = (fr[2][0] - fr[1][0], fr[2][1] - fr[1][1])
    u = e1 if math.hypot(*e1) >= math.hypot(*e2) else e2
    L = math.hypot(*u)
    u = (u[0] / L, u[1] / L)
    if (fr[0][0] - cx) * u[0] + (fr[0][1] - cy) * u[1] > 0:
        u = (-u[0], -u[1])
    return u, (-u[1], u[0])


def _p17_win_pts(key, log):
    """the survey points a plan window must hold"""
    pts = []
    zs = _p17_zones()
    if key == "A":
        for cid in ("F2", "W1"):
            pts += list(level_ends(cid))
        pts += [p for z in zs if z.get("study_area") == "aras_alan" and z["code"] != "STRIP" for p in z["ring"]]
    else:
        pts += list(level_ends("F4"))
        pts += [_p17_s4_pt(s) for s in P14_RANGE]
        pts += [p for z in zs if z["code"] == "WP" for p in z["ring"]]
        mid = _p17_cut_pt("F4", 0.5 * level("F4", "length_m"))
        pts += [p for a in _p17_arms(log) for p in a if math.hypot(p[0] - mid[0], p[1] - mid[1]) < 150.0]
    return pts


def _p17_win_fit(pts, den, pad=8.0):
    """the best turn for a window at 1:den: (w mm, h mm, u, v, centre, den) of north-up or along the frame, the smaller"""
    best = None
    k = 1000.0 / den
    turns = [((1.0, 0.0), (0.0, 1.0))]
    fu = _p17_frame_uv()
    if fu:
        turns.append(fu)
    for u, v in turns:
        us = [p[0] * u[0] + p[1] * u[1] for p in pts]
        vs = [p[0] * v[0] + p[1] * v[1] for p in pts]
        w, h = (max(us) - min(us) + 2 * pad) * k, (max(vs) - min(vs) + 2 * pad) * k
        c = ((min(us) + max(us)) / 2.0, (min(vs) + max(vs)) / 2.0)
        if best is None or w * h < best[0] * best[1] - 1e-6:
            best = (w, h, u, v, c, den)
    return best


def _p17_ring_index(rings, cell):
    """rings (page mm) bucketed by the grid cells their boxes touch, so a point-in-any-ring test stays local"""
    idx = {}
    for R_ in rings:
        if len(R_) < 3:
            continue
        xs, ys = [p[0] for p in R_], [p[1] for p in R_]
        bb = (min(xs), min(ys), max(xs), max(ys))
        for i in range(int(math.floor(bb[0] / cell)), int(math.floor(bb[2] / cell)) + 1):
            for j in range(int(math.floor(bb[1] / cell)), int(math.floor(bb[3] / cell)) + 1):
                idx.setdefault((i, j), []).append((bb, R_))
    return idx


def _p17_in(idx, cell, p):
    for bb, R_ in idx.get((int(math.floor(p[0] / cell)), int(math.floor(p[1] / cell))), ()):
        if bb[0] <= p[0] <= bb[2] and bb[1] <= p[1] <= bb[3] and _p17_pip(p, R_):
            return True
    return False


def _p17_edge_index(rings, cell):
    """the edges of several rings (page mm) bucketed by grid cell, for water.py _wat_near_edge"""
    idx = {}
    for R_ in rings:
        if len(R_) >= 3:
            for key_, segs in _wat_edge_index(list(R_), cell).items():
                idx.setdefault(key_, []).extend(segs)
    return idx


def _p17_band_t():
    """the band edges on the wet-to-dry scale t (0 the water's edge .. 1 dry ground): halfway between the last niche
    centre of one P17_BANDS band and the first of the next (plants.py PLA_NICHE), so no new number"""
    out = []
    for a, b in zip(P17_BANDS[:-1], P17_BANDS[1:]):
        out.append(0.5 * (max(PLA_NICHE[k_][0] for k_ in a if k_ in PLA_NICHE) +
                          min(PLA_NICHE[k_][0] for k_ in b if k_ in PLA_NICHE)))
    return out


def _p17_drift_plan(ring, k, tf, mix, seed, density=1.0, avoid=None, max_n=3000, water=None, clear=None, page="p16"):
    """G9 planting in plan as R12-R14 draw it: species AREAS in wet-to-dry bands along the water. t = tf(x, y) (0 the
    water's edge .. 1 dry ground, > 1 nothing) puts a point in its band (P17_BANDS, edges _p17_band_t); each band is
    cut into drifts around irregular centres (5-16 m plus two crowns of the lead species across: plants.py PLA_GROUP
    group_m, a drawing rule), each drift led by one species with a second mixed in and, at its edges, the species of
    the neighbouring band whose niche reaches there (plants.py _pla_pick): interpenetrating, never rows. Crowns
    overlap (trunks 35-75 % of the two crowns apart: PLA_GROUP step), sizes vary (PLA_GROUP size inside the sourced
    range), no straight evenly spaced line (plants.py _pla_rowlike). Each drift is drawn as its area first (the lead
    species' tone, a fine edge: the band edges follow the water), then the low layer, then the crowns, tall on top.
    ring and avoid: page mm. Round 3: water = the water rings (page mm): no area and no plant in them, and every
    placed plant goes through water.py water_clip_points (G8, logged for page); clear = [(x, y, r mm)] open
    clearings round the places people use (P16.2): crowns are left out there, the drift's ground tint stays.
    Returns (shapes, placed [(key, x, y, crown_m)], drifts [(band, lead key, area ring, area mm²)])."""
    keys = [k_ for k_ in mix if k_ in PLA_NICHE]
    if not keys or len(ring) < 3:
        return [], [], []
    edges = _p17_band_t()
    rnd = _pla_rng(seed * 13 + 3)
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    bx0, by0, bw, bh = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    area = _p17_area(ring)
    pools = [[k_ for k_ in keys if k_ in b_] for b_ in P17_BANDS]
    wet_r = [list(r_) for r_ in (water or ()) if len(r_) >= 3]
    wet_ix = _p17_ring_index(wet_r, 6.0) if wet_r else {}   # bucketed: the stream's rings are long

    def band(t):
        return sum(1 for e in edges if t > e)

    def free(x, y):
        return (_p17_pip((x, y), ring) and not any(_p17_pip((x, y), a) for a in (avoid or ())) and
                not (wet_ix and _p17_in(wet_ix, 6.0, (x, y))))

    def in_clear(x, y):
        return any(math.hypot(x - c_[0], y - c_[1]) < c_[2] for c_ in (clear or ()))

    def crown(key):
        return PLA_SPECIES[key]["crown_m"]
    g0, g1 = PLA_GROUP["group_m"]
    drifts = dict((b, []) for b in range(len(P17_BANDS)))      # band -> [(x, y, r mm, lead, second)]

    def nearest(b, x, y):
        best, bd = None, None
        for d_ in drifts[b]:
            q = math.hypot(x - d_[0], y - d_[1]) / d_[2]
            if bd is None or q < bd:
                best, bd = d_, q
        return best, bd
    r_small = (0.5 * g0 + min(crown(k_) for k_ in keys)) * k
    for _i in range(int(min(6000, 12.0 * area / (math.pi * r_small * r_small) + 40))):
        x, y = bx0 + rnd() * bw, by0 + rnd() * bh
        if not free(x, y):
            continue
        t = tf(x, y)
        if t > 1.0:
            continue
        b = band(t)
        if not pools[b]:
            continue
        nb, q = nearest(b, x, y)
        if nb is not None and q < 0.9:
            continue
        cand = [k_ for k_ in pools[b] if nb is None or k_ != nb[3] or len(pools[b]) == 1]
        lead = cand[int(rnd() * len(cand)) % len(cand)]
        other = [k_ for k_ in pools[b] if k_ != lead] or \
            [k_ for bb in (b - 1, b + 1) if 0 <= bb < len(pools) for k_ in pools[bb]]
        second = other[int(rnd() * len(other)) % len(other)] if other else None
        r = (0.5 * (g0 + (g1 - g0) * rnd()) + crown(lead)) * k
        drifts[b].append((x, y, r, lead, second))
    sh, info = [], []
    # the areas: each drift's ground, ray by ray out to its band edge, its neighbour drift or the planted ring
    for b, ds in drifts.items():
        for d_ in ds:
            def inside(p, d_=d_, b=b):
                if not free(p[0], p[1]):
                    return False
                t = tf(p[0], p[1])
                return t <= 1.0 and band(t) == b and nearest(b, p[0], p[1])[0] is d_
            pts = []
            for i in range(40):
                a = 2.0 * math.pi * i / 40.0
                u = (math.cos(a), math.sin(a))
                lo, hi = 0.0, d_[2]
                if inside((d_[0] + u[0] * hi, d_[1] + u[1] * hi)):
                    lo = hi
                else:
                    for _j in range(6):
                        m = 0.5 * (lo + hi)
                        if inside((d_[0] + u[0] * m, d_[1] + u[1] * m)):
                            lo = m
                        else:
                            hi = m
                pts.append((d_[0] + u[0] * lo, d_[1] + u[1] * lo))
            if _p17_area(pts) > 0.5:
                fc = PLA_SPECIES[d_[3]]["colours"]["fill"]
                sh.append(("poly", pts, _sec_mix(fc, SEC["paper"], 0.72), _sec_mix(fc, SEC["paper"], 0.35), 0.1))
                info.append((b, d_[3], pts, _p17_area(pts)))
    # the plants: dart throwing per layer, each species from its drift (lead 62 %, second 24 %, the band's niche rest)
    lo_s, hi_s = PLA_GROUP["step"]
    placed = {True: [], False: []}
    total = 0
    for canopy in (True, False):
        ks_c = [k_ for k_ in keys if _pla_canopy(k_) == canopy]
        if not ks_c:
            continue
        cs = max(crown(k_) for k_ in ks_c) * k * PLA_GROUP["size"][1]
        grid = {}
        r_typ = sum(crown(k_) for k_ in ks_c) / len(ks_c) / 2.0 * k
        for _i in range(int(min(40000, 8.0 * density * area / (math.pi * r_typ * r_typ) + 50))):
            if total >= max_n:
                break
            x, y = bx0 + rnd() * bw, by0 + rnd() * bh
            if not free(x, y):
                continue
            t = tf(x, y)
            if t > 1.0:
                continue
            d_ = nearest(band(t), x, y)[0]
            u = rnd()
            key = None
            if d_ is not None and u < 0.62:
                key = d_[3]
            elif d_ is not None and u < 0.86:
                key = d_[4]
            else:
                key = _pla_pick(t, rnd, keys, None, canopy)
            if key is None or _pla_canopy(key) != canopy:
                alt = [q for q in ((d_[3], d_[4]) if d_ is not None else ()) if q and _pla_canopy(q) == canopy]
                key = alt[0] if alt else None
            if key is None or (canopy and in_clear(x, y)):
                continue
            h, w = _pla_group_size(key, rnd)
            r = w / 2.0 * k
            s_ = lo_s + (hi_s - lo_s) * rnd()
            ci, cj = int(math.floor(x / cs)), int(math.floor(y / cs))
            near = [e for i in (ci - 1, ci, ci + 1) for j in (cj - 1, cj, cj + 1) for e in grid.get((i, j), ())]
            if any(math.hypot(e[0] - x, e[1] - y) < s_ * (r + e[2]) for e in near):
                continue
            if _pla_rowlike((x, y), [(e[0], e[1]) for e in near], 3.0 * cs):
                continue
            e = (x, y, r, key, h)
            placed[canopy].append(e)
            grid.setdefault((ci, cj), []).append(e)
            total += 1
    out = []
    if wet_r:                                            # G8: no crown over the water (one line logged by water.py)
        ok = set(id(e) for e in water_clip_points(placed[False] + placed[True], wet_r, page=page))
        placed = dict((c_, [e for e in placed[c_] if id(e) in ok]) for c_ in (False, True))
    for canopy in (False, True):
        for i, (x, y, r, key, h) in enumerate(sorted(placed[canopy], key=lambda e: e[4])):   # tall crowns on top
            sh += pla_plan(key, x, y, k, crown_m=2.0 * r / k, seed=seed + i * 3 + (7 if canopy else 0))
            out.append((key, x, y, 2.0 * r / k))
    return sh, out, info


def _p17_study(log):
    """round 4 (G-R4-4, CHK-7): the study area rings (study_clip sc_rings: calisma_alan), read once a run"""
    if "st" not in _P17_MEMO:
        st = sc_rings(basemap_load(log=log) or None)
        if not st:
            log.append(u"FLAG p17: no study area in the base map: the plans' proposals are not clipped")
        _P17_MEMO["st"] = st
    return _P17_MEMO["st"]


def _p17_zones_st(log):
    """round 4 (CHK-7): the water spaces (no summer strip, D2) clipped to the study area (sc_rings_clip, page "p17":
    one zone per part it reaches)"""
    if "zs_st" not in _P17_MEMO:
        st = _p17_study(log)
        out = []
        for z in _p17_zones():
            if z["code"] == "STRIP":
                continue
            for r in sc_rings_clip(z["ring"], st, P17_PAGE):
                if len(r) >= 3:
                    out.append(dict(z, ring=[tuple(p) for p in r]))
        _P17_MEMO["zs_st"] = out
    return _P17_MEMO["zs_st"]


def _p17_arms_st(log):
    """round 4: the side arms (masterplan corridor export, else the p.23 line) clipped to the study area"""
    if "arms_st" not in _P17_MEMO:
        st = _p17_study(log)
        _P17_MEMO["arms_st"] = [[tuple(p) for p in run] for a in _p17_arms(log)
                                for run in (sc_lines(a, st, P17_PAGE) if st else [a]) if len(run) >= 2]
    return _P17_MEMO["arms_st"]


def _p17_widen_st(log):
    """round 4: the widened stream (masterplan corridor export) clipped to the study area; logged once when the
    masterplan wrote none (the plans then show the stream as surveyed)"""
    if "widen_st" not in _P17_MEMO:
        st = _p17_study(log)
        ws = _p17_widen(log)
        if not ws:
            log.append(u"p17: the masterplan corridor export has no widened stream: the plans show the surveyed stream")
        _P17_MEMO["widen_st"] = [r for w_ in ws for r in (sc_rings_clip(w_, st, P17_PAGE) if st else [w_])
                                 if len(r) >= 3]
    return _P17_MEMO["widen_st"]


def _p17_space_keys(code):
    """the species the design plants in a water space, catalogue order (P17_MIX; lined cells: reed, water mint)"""
    mix = ("reed", "mint") if code == "WT" else (P17_MIX.get(code) or
                                                 next((s_[3] for s_ in PLANT_SITES if s_[1] == code), ()))
    return [k_ for k_ in P17_CAT if k_ in mix]


def _p17_spaces(fit, log):
    """[(code, name, survey point)] the water spaces whose marker spot (the largest part's centre, the side arm's
    middle) lies 3 mm inside the window fit (the same test for the layout and the drawing)"""
    w, h, u, v, c, den = fit
    k = 1000.0 / den

    def inR(p, m=0.0):
        X = ((p[0] * u[0] + p[1] * u[1]) - c[0]) * k
        Y = ((p[0] * v[0] + p[1] * v[1]) - c[1]) * k
        return abs(X) <= w / 2.0 - m and abs(Y) <= h / 2.0 - m
    zs = [z for z in _p17_zones_st(log) if any(inR(p) for p in z["ring"])]
    arms = [a for a in _p17_arms_st(log) if any(inR(p) for p in a)]
    out = []
    for _n, code, name, _keys in PLANT_SITES:
        if code == "STRIP":
            continue
        at = None
        if code == "ARM":
            if arms:
                a = max(arms, key=len)
                at = _p17_along(a, 0.5 * sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(a[:-1], a[1:])))[0]
        else:
            cand = [z for z in zs if z["code"] == code]
            if cand:
                at = _p17_cen(max(cand, key=lambda z_: _p17_area(z_["ring"]))["ring"])
        if at is not None and inR(at, 3.0):
            out.append((code, name, at))
    return out


def _p17_rows(fit, log, seen, start):
    """the list rows [(n, code, name, species)] of a window: its spaces numbered in reading order from start; a space
    already numbered (seen, window A) keeps its number and is not listed again"""
    w, h, u, v, c, den = fit
    k = 1000.0 / den
    sp_ = _p17_spaces(fit, log)
    pts = [(((p[0] * u[0] + p[1] * u[1]) - c[0]) * k, ((p[0] * v[0] + p[1] * v[1]) - c[1]) * k) for _c, _n, p in sp_]
    rows, n = [], start
    for j in tp_reading_order(pts, y_down=False):
        code, name, _at = sp_[j]
        if code in seen:
            continue
        seen[code] = n
        rows.append((n, code, name, _p17_space_keys(code)))
        n += 1
    return rows


def _p17_window(pg, x0, ytop, key, fit, log, seen):
    """round 4 (P17.1, P17.3, P17.4, P17.6, G-R4-4/7/9): one plan window, its top-left at (x0, ytop), at fit (w, h,
    u, v, centre, den; grown by the layout to fill its column). map_draw order: the muted base (ml_base: light houses
    with closed outlines, light streets, the stream) at the back with the farms and orchards under it (one field
    texture + one crop symbol per area, plants.py); then the D9 footprint tint of what the project changes (ml_tint,
    clipped to the study area); then the project: the widened stream and the side arm (masterplan corridor export),
    the water spaces, July shade, the places people use, the planting (species areas wet to dry, plants.py crowns,
    willow v2), the shrub groups on the open planted ground (P17.6); the study line (BM_STUDY_LINE) over them. Every
    proposal clipped to the study area at its source (sc_*, page "p17"). Over that: the section lines of p18 in the
    R01 red symbol (km_cut_items), the north arrow (north_items, no plate) in a free corner, the hubs and the
    numbered markers (mk_marker, the space's colour), placed clear of each other. Under the frame: the scale bar.
    Returns (bbox, rows [(n, code, name, species)], {code: species}, geo, hubs drawn)."""
    w, h, u, v, c, den = fit
    k = 1000.0 / den
    R = (x0, ytop - h, x0 + w, ytop)
    ox, oy = (R[0] + R[2]) / 2.0, (R[1] + R[3]) / 2.0
    fs = P17_FS

    def T(p):
        return (ox + ((p[0] * u[0] + p[1] * u[1]) - c[0]) * k, oy + ((p[0] * v[0] + p[1] * v[1]) - c[1]) * k)

    def Ti(X, Y):
        a_, b_ = (X - ox) / k + c[0], (Y - oy) / k + c[1]
        return (a_ * u[0] + b_ * v[0], a_ * u[1] + b_ * v[1])
    corners = [Ti(R[0], R[1]), Ti(R[2], R[1]), Ti(R[2], R[3]), Ti(R[0], R[3])]
    sb = (min(p[0] for p in corners), min(p[1] for p in corners), max(p[0] for p in corners),
          max(p[1] for p in corners))

    def inR(p):
        X, Y = T(p)
        return R[0] <= X <= R[2] and R[1] <= Y <= R[3]
    Rr = [(R[0], R[1]), (R[2], R[1]), (R[2], R[3]), (R[0], R[3])]
    st = _p17_study(log)
    st_pg = [[T(p) for p in r_] for r_ in st]
    out = Page(0, 0)                                     # the window, drawn in order, cut to R at the end
    out.poly([rect(*R)], fill=COL["white"])
    D = basemap_load(log=log)
    L = (D or {}).get("layers") or {}
    # farms and orchards (D7 a, P17.4): one field texture and one crop symbol per area, under the base's houses
    fields = []
    lc = L.get("lc") or {}
    farm = list(lc.get("farmland", [])) + [z_["rings"] for z_ in L.get("zones", []) if z_.get("kind") == "agri"]
    for crop, groups in (("olive", lc.get("orchard", [])), ("maize", farm)):
        for g in groups:
            if not g or len(g[0]) < 3 or not _p17_hit(g[0], sb):
                continue
            Pc = _p14_clip_ring([T(p) for p in g[0]], R)
            if not Pc or _p17_area(Pc) < 4.0:
                continue
            fields.append(Pc)
            sh = pla_field_tile(Pc, k, crop=crop, seed=len(fields))
            if _p17_area(Pc) < 140.0:                    # too small for its symbol: the texture alone
                sh = [sh[0]] + [s_ for s_ in sh[1:] if s_[0] == "line" and s_[2] == PLA_ROW]
            _p17_put(out, sh)
    base = []
    if D:
        try:
            base = ml_base(sb, den, D=D, override={"trees": False, "green": False, "fields": False})
        except Exception as ex:
            log.append(u"p17 plan {}: base map not drawn: {}: {}".format(key, type(ex).__name__, ex))
    water = [[T(p) for p in r_] for r_ in basemap_water_rings(base)]
    bld = [[T(p) for p in R_] for b in L.get("buildings", []) for R_ in b["rings"][:b.get("np", len(b["rings"]))]
           if len(R_) >= 3 and _p17_hit(R_, sb)]
    streets = [[T(p) for p in g[0]] for g in L.get("street_areas", []) if g and len(g[0]) >= 3 and _p17_hit(g[0], sb)]
    zs = [z for z in _p17_zones_st(log) if any(inR(p) for p in z["ring"])]
    arms = [a for a in _p17_arms_st(log) if any(inR(p) for p in a)]
    widen = [r for r in _p17_widen_st(log) if any(inR(p) for p in r)]
    sp = Page(0, 0)                                      # the project, drawn by map_draw's order hook
    for r in widen:
        sp.poly([[T(p) for p in r]], fill=P17_ZONE["WIDEN"][0], stroke=P17_ZONE["WIDEN"][1], lw=0.1)
    for z in zs:                                         # the water spaces, flat (planting comes after the shade)
        if z["code"] in P17_ZONE and z["code"] != "WT":
            f_, s_ = P17_ZONE[z["code"]]
            sp.poly([[T(p) for p in z["ring"]]], fill=f_, stroke=s_, lw=0.12)
    arm_bands = []
    for a in arms:
        P = [T(p) for p in a]
        arm_bands.append(_p14_band(P, 2.0 * P17_ARM_W * k))
        sp.poly([arm_bands[-1]], fill=P17_ZONE["ARM"][0], stroke=P17_ZONE["ARM"][1], lw=0.12)
    # July shade on the bed and the water spaces (5 m cells, three classes): an opaque fine hatch
    sh = _p17_shade(log)
    spaces = [[Ti(*p) for p in r_] for r_ in water] + [z["ring"] for z in zs] + widen
    if sh:
        cells, day, cm = sh
        hc = cm / 2.0
        for x, y, hrs in cells:
            if not (sb[0] - cm <= x <= sb[2] + cm and sb[1] - cm <= y <= sb[3] + cm):
                continue
            q = (x, y)
            if not (any(_p17_pip(q, r) for r in spaces) or any(_p17_line_d(q, a) <= P17_ARM_W for a in arms)):
                continue
            col, hs_ = next((cl, hs) for lim, cl, _l, hs in P17_SHADE if hrs < lim)
            for p_, q_ in sec_hatch([T((x - hc, y - hc)), T((x + hc, y - hc)), T((x + hc, y + hc)),
                                     T((x - hc, y + hc))], hs_, 45.0):
                sp.line([p_, q_], col, 0.12)
    # the places people use, from the sections' own programme (stones, footbridge, terraces, sun steps), inside the
    # study area only; their footprints stay unplanted, an open clearing round each
    foot, clear, st_n, st_out = [], [], 0, 0
    for kind, cid, ta, tb, rail in _p17_plan_structs(log):
        pa, pb = _p17_spec_pt(cid, ta), _p17_spec_pt(cid, tb)
        mid = ((pa[0] + pb[0]) / 2.0, (pa[1] + pb[1]) / 2.0)
        if not inR(mid):
            continue
        if st and not sc_inside(mid, st):
            st_out += 1
            continue
        shp, fr = _p17_struct_plan(kind, T(pa), T(pb), rail)
        _p17_put(sp, shp)
        foot.append(fr)
        C = _p17_cen(fr)
        clear.append((C[0], C[1], P17_CLEAR_M * k))
        st_n += 1
    hubs = [(name, T(xy)) for name, xy in _p17_hubs(log) if inR(xy)]
    for _nm, (X, Y) in hubs:
        clear.append((X, Y, P17_CLEAR_M * k))
    # the planting: lined basin cells; each space a mixed scatter at its band; the side arms and the stream banks wet
    # to dry by the distance to the water; never in water, buildings, streets, fields or on the places people use
    cell = 6.0
    wet = water + [[T(p) for p in z["ring"]] for z in zs if z["code"] == "WD"] + arm_bands
    widx = _p17_edge_index(wet, cell)
    wet_in = _p17_ring_index(wet, cell)
    bld_in = _p17_ring_index(bld, cell)
    placed, taken_z, geo = {}, [], []
    ds_, db_ = P17_DENS_PLAN["space"], P17_DENS_PLAN["bank"]

    def note(code, pl, info=()):
        s_ = placed.setdefault(code, [])
        for q in pl:
            if q[0] not in s_:
                s_.append(q[0])
        geo.extend(info)
    for i, z in enumerate(zs):
        Rp = [T(p) for p in z["ring"]]
        code = z["code"]
        try:
            if code == "WT":
                cz, au, av, (a0, a1), _ = _p17_axis(Rp)
                cuts = [a0 + (a1 - a0) * f for f in (1.0 / 3.0, 2.0 / 3.0)]
                cl_ = []
                for j, kind in enumerate(("reed", "reed", "mint")):
                    rr = Rp
                    if j > 0:
                        rr = _p17_half(rr, (cz[0] + au[0] * cuts[j - 1], cz[1] + au[1] * cuts[j - 1]), au)
                    if rr and j < 2:
                        rr = _p17_half(rr, (cz[0] + au[0] * cuts[j], cz[1] + au[1] * cuts[j]), (-au[0], -au[1]))
                    if rr:
                        cl_.append((kind, rr))
                for kind, rr in cl_:
                    _p17_put(sp, pla_cell_plan(kind, rr, k, P17_BASIN["kerb_t"]))
                note("WT", [("reed",), ("mint",)], [(0, kind, rr, _p17_area(rr)) for kind, rr in cl_])
            elif code in P17_MIX_T:
                if code == "WS":                         # the terrace edges along the contours, 7 m apart
                    cz, au, av, (a0, a1), (b0, b1) = _p17_axis(Rp)
                    bb = b0 + 7.0 * k
                    while bb < b1 - 1e-6:
                        seg = [(cz[0] + au[0] * a0 * 1.2 + av[0] * bb, cz[1] + au[1] * a0 * 1.2 + av[1] * bb),
                               (cz[0] + au[0] * a1 * 1.2 + av[0] * bb, cz[1] + au[1] * a1 * 1.2 + av[1] * bb)]
                        for run in _p17_clip_seg(seg, Rp):
                            sp.line(run, "8C8170", 0.3)
                        bb += 7.0 * k
                t_ = P17_MIX_T[code]
                shp, pl, inf = _p17_drift_plan(Rp, k, lambda x_, y_, t_=t_: t_, list(P17_MIX[code]), 40 + 7 * i,
                                               density=ds_, avoid=foot, water=wet, clear=clear, page=P17_PAGE)
                _p17_put(sp, shp)
                note(code, pl, inf)
            elif code == "WP":
                band = P17_WP_M * k

                def t_wp(x_, y_):
                    p_ = (x_, y_)
                    if _p17_in(wet_in, cell, p_) or _p17_in(bld_in, cell, p_):
                        return 9.0
                    return min(1.0, _wat_near_edge(widx, cell, p_, band)[0] / band)
                shp, pl, inf = _p17_drift_plan(Rp, k, t_wp, list(P17_MIX["WP"]), 60 + 7 * i, density=ds_,
                                               avoid=foot, water=wet, clear=clear, page=P17_PAGE)
                _p17_put(sp, shp)
                note(code, pl, inf)
            taken_z.append(Rp)
        except Exception as ex:
            log.append(u"p17 plan {}: {} not planted: {}: {}".format(key, code, type(ex).__name__, ex))
    for i, a in enumerate(arms):                         # the side arm: rushes and loosestrife at its water, willow out
        P = [T(p) for p in a]
        ring = _p14_band(P, 2.0 * (P17_ARM_W + P17_ARM_BAND) * k)

        def t_arm(x_, y_, P=P):
            p_ = (x_, y_)
            if _p17_in(bld_in, cell, p_):
                return 9.0
            return 0.45 * max(0.0, _p17_line_d(p_, P) - P17_ARM_W * k) / (P17_ARM_BAND * k)
        try:
            for j, rg in enumerate(sc_rings_clip(ring, st_pg, P17_PAGE) if st_pg else [ring]):
                shp, pl, inf = _p17_drift_plan(rg, k, t_arm, list(P17_MIX["ARM"]), 90 + i + 5 * j, density=ds_,
                                               avoid=foot, water=wet, clear=clear, page=P17_PAGE)
                _p17_put(sp, shp)
                note("ARM", pl, inf)
                taken_z.append(rg)
        except Exception as ex:
            log.append(u"p17 plan {}: side arm not planted: {}: {}".format(key, type(ex).__name__, ex))
    # the stream banks: P17_BAND_M wide, wet to dry, on the open ground inside the study area
    blk = _p17_ring_index(bld + streets + fields + taken_z, cell)
    band = P17_BAND_M * k
    parts = sc_rings_clip(Rr, st_pg, P17_PAGE) if st_pg else [Rr]

    def t_bank(x_, y_):
        p_ = (x_, y_)
        if _p17_in(wet_in, cell, p_) or _p17_in(blk, cell, p_):
            return 9.0
        d_ = _wat_near_edge(widx, cell, p_, band)[0]
        return d_ / band if d_ < band - 1e-9 else 9.0

    def t_open(x_, y_):                                  # P17.6: beyond the bank band, moist to dry
        p_ = (x_, y_)
        if _p17_in(wet_in, cell, p_) or _p17_in(blk, cell, p_) or \
                any(math.hypot(x_ - c_[0], y_ - c_[1]) < c_[2] for c_ in clear):
            return 9.0
        d_ = _wat_near_edge(widx, cell, p_, 2.0 * band)[0]
        if d_ < band:
            return 9.0
        return 0.5 + 0.4 * min(1.0, (d_ - band) / band)
    n_open = 0
    for j, rg in enumerate(parts):
        try:
            shp, pl, inf = _p17_drift_plan(rg, k, t_bank, list(P17_MIX["BANK"]), (7 if key == "A" else 8) + 11 * j,
                                           density=db_, avoid=foot, water=wet, clear=clear, page=P17_PAGE)
            _p17_put(sp, shp)
            note("BANK", pl, inf)
        except Exception as ex:
            log.append(u"p17 plan {}: stream banks not planted: {}: {}".format(key, type(ex).__name__, ex))
        try:
            shp, pl = pla_low_plan(rg, k, t_open, seed=(17 if key == "A" else 19) + 13 * j, density=P17_SHRUB_DENS,
                                   avoid=foot, mix=P17_SHRUB, max_n=900)
            _p17_put(sp, shp)
            note("OPEN", pl)
            n_open += len(pl)
        except Exception as ex:
            log.append(u"p17 plan {}: shrub groups not drawn: {}: {}".format(key, type(ex).__name__, ex))
    # map_draw: base -> D9 tint -> project (the hook) -> study line, strictly in ML_LAYERS order
    done = [False]

    def hook(layer):
        if not done[0] and layer not in ML_BASE_LAYERS and layer != "proj_tint":
            out.items.extend(sp.items)
            done[0] = True
    f_, l_, t_ = _p17_map_fns(out)
    tint = [z["ring"] for z in zs] + widen + [_p14_band(a, 2.0 * P17_ARM_W) for a in arms]
    map_draw(P17_PAGE, T, f_, l_, t_, base, {"proj_tint": ml_tint(tint, study=st or None, page=P17_PAGE)},
             study=st or None, clip=True, order_fn=hook, log=log)
    if not done[0]:
        out.items.extend(sp.items)
    # the section lines of p18 (cut registry W1, F2, S4, F4) in the R01 red symbol, kept inside the frame
    fr = [Ti(R[0] + 3.0, R[1] + 3.0), Ti(R[2] - 3.0, R[1] + 3.0), Ti(R[2] - 3.0, R[3] - 3.0), Ti(R[0] + 3.0, R[3] - 3.0)]
    cuts = []
    for cid in P17_CUTS:
        try:
            a, b = level_ends(cid)
        except Exception:
            continue
        cuts.append((a, b, tuple(cut_end_labels(level_name(cid))), 1))
    basemap_draw(km_cut_items(cuts, den, frame=fr), T, f_, l_, t_)
    taken = [_p17_tbox(it) for it in out.items if it[0] == "text"]
    taken += [(min(q[0] for q in it[1]), min(q[1] for q in it[1]), max(q[0] for q in it[1]), max(q[1] for q in it[1]))
              for it in out.items if it[0] == "line" and it[2] == KM_CUT["colour"] and len(it[1]) <= 4 and
              max(abs(it[1][-1][0] - it[1][0][0]), abs(it[1][-1][1] - it[1][0][1])) < 6.0]
    # the north arrow, the hubs, the markers
    nd = (T((0.0, 100.0))[0] - T((0.0, 0.0))[0], T((0.0, 100.0))[1] - T((0.0, 0.0))[1])
    nl = math.hypot(*nd) or 1.0
    nd = (nd[0] / nl, nd[1] / nl)
    _p17_north_in(out, R, nd, 6.0, taken)
    for _nm, (X, Y) in hubs:
        _p17_put(out, ico_badge("hub", X, Y, 4.0))
        taken.append((X - 2.0, Y - 2.0, X + 2.0, Y + 2.0))
    rows = []
    pts = [(T(at), code, name) for code, name, at in _p17_spaces(fit, log)]
    n_next = 1 + max([0] + list(seen.values()))
    for j in tp_reading_order([q[0] for q in pts], y_down=False):
        (X, Y), code, name = pts[j]
        if code in seen:
            num = seen[code]
        else:
            num = n_next
            n_next += 1
            seen[code] = num
            rows.append((num, code, name, [k_ for k_ in _p17_space_keys(code) if k_ in (placed.get(code) or
                                                                                          _p17_space_keys(code))]))
        at = None
        for dx, dy in ((0, 0), (0, 5), (0, -5), (5, 0), (-5, 0), (5, 5), (-5, 5), (5, -5), (-5, -5), (0, 9), (0, -9),
                       (9, 0), (-9, 0)):
            b = (X + dx - 2.2, Y + dy - 2.2, X + dx + 2.2, Y + dy + 2.2)
            if _p17_free(b, taken, R):
                at = (X + dx, Y + dy)
                break
        if at is None:
            log.append(u"FLAG p17 plan {}: marker {} has no free spot: drawn on its space".format(key, num))
            at = (X, Y)
        taken.append(_p17_mark(out, num, at[0], at[1], code, keep_pg=pg))
    for name, (X, Y) in hubs:                            # hub names (G-R4-11: real names), beside the icon or left out
        for x_, y_, al in ((X + 2.8, Y - fs * 0.35, "L"), (X - 2.8, Y - fs * 0.35, "R"), (X, Y + 2.8, "C"),
                           (X, Y - 2.8 - fs * 0.75, "C")):
            b = fm_box(name, x_, y_, fs / PT, True, al, 0.0, False)
            if _p17_free(b, taken, R):
                out.text(name, x_, y_, fs, COL["ink_dark"], bold=True, align=al)
                taken.append(b)
                break
        else:
            log.append(u"p17 plan {}: hub name '{}' left out (no free place)".format(key, name))
    pg.items += _p17_clip_items(out.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=P17_NEAT)      # a map keeps a thin neatline (D4)
    bb = _p12_bar(pg, R[0], R[1] - 4.0, den, P17_BAR.get(den, (0, 20, 50, 100)))
    wat_draw_order_lines(page=u"p17 plan " + key, steps=["ground", "water", "structures", "vegetation", "labels"])
    log.append(u"p17 plan {}: 1:{:,.0f}, {:.0f} x {:.0f} mm, {} places drawn in plan ({} outside the study area left "
               u"out), {} markers, {} hubs, shrub groups {} plants".format(key, den, w, h, st_n, st_out, len(pts),
                                                                         len(hubs), n_open))
    return (min(R[0], bb[0]), bb[1], R[2], R[3]), rows, placed, \
        dict(drifts=geo, water=wet, R=R, den=den, nd=nd), len(hubs)


def _p17_specs(log):
    """the four section specs of page B (W1, F2, S4, F4), built once a run: page A draws their places in plan from
    them, so plan and section show the same thing at the same spot"""
    if "specs" not in _P17_MEMO:
        out = {}
        for nm, fn in (("F2", _p17_f2), ("F4", _p17_f4), ("W1", _p17_f1), ("S4", _p17_f3)):
            try:
                out[nm] = fn(log)
            except Exception as ex:
                log.append(u"WARNING p.17 section {} not built: {}: {}".format(nm, type(ex).__name__, ex))
        _P17_MEMO["specs"] = out
    return _P17_MEMO["specs"]


def _p17_spec_pt(cid, t):
    """the survey point of a section spec's coordinate t: S4 m across from the bed's low point (p.14's), the other
    cuts m along from their first end"""
    return _p17_s4_pt(t) if cid == "S4" else _p17_cut_pt(cid, t)


def _p17_plan_structs(log):
    """G10 in plan: [(kind, cut id, t from, t to, rail end)] the stepping stones, footbridges and viewing terraces of
    the section specs, and S4's sun steps (kind "steps")"""
    out = []
    for cid, sp_ in sorted(_p17_specs(log).items()):
        for st in sp_.get("structures", []):
            if st[0] in ("stones", "bridge", "terrace"):
                out.append((st[0], cid, st[1], st[2], st[3] if st[0] == "terrace" else None))
        for pe in sp_.get("people", []):
            if pe[0] == "sun_steps":
                out.append(("steps", cid, pe[1], pe[2], None))
    return out


def _p17_struct_plan(kind, A, B, rail=None):
    """a place people use as a plan symbol from A to B (page mm, along the cut): stones a staggered row of stones,
    bridge a deck with two rails, terrace a deck with its rail at the rail end ("a" = A), steps parallel treads. Sizes
    at least legible at the plan's scale (symbols, explained in the legend; drawing rules, never printed). Returns
    (shapes, footprint ring)."""
    L = math.hypot(B[0] - A[0], B[1] - A[1]) or 1e-6
    d = ((B[0] - A[0]) / L, (B[1] - A[1]) / L)
    n_ = (-d[1], d[0])
    C = ((A[0] + B[0]) / 2.0, (A[1] + B[1]) / 2.0)
    Lp = max(L, {"stones": 3.0, "bridge": 2.6, "terrace": 2.2, "steps": 1.6}[kind])
    half = {"stones": 0.6, "bridge": 0.55, "terrace": 0.75, "steps": 0.9}[kind]

    def at(s, o):
        return (C[0] + d[0] * s + n_[0] * o, C[1] + d[1] * s + n_[1] * o)
    sh = []
    ink = COL["ink_dark"]
    if kind == "stones":
        for i in range(4):
            s = -Lp / 2.0 + Lp * (i + 0.5) / 4.0
            p = at(s, 0.22 if i % 2 else -0.22)
            sh.append(("poly", sec_ellipse(p[0], p[1], 0.36, 0.3, 10), "C9BBA2", COL["ink2"], 0.08))
    elif kind in ("bridge", "terrace"):
        ring = [at(-Lp / 2.0, -half), at(Lp / 2.0, -half), at(Lp / 2.0, half), at(-Lp / 2.0, half)]
        sh.append(("poly", ring, "FFFFFF" if kind == "bridge" else "E7E1D3", ink, 0.12))
        if kind == "bridge":
            for o in (-half, half):
                sh.append(("line", [at(-Lp / 2.0, o), at(Lp / 2.0, o)], ink, 0.22))
        else:
            s = -Lp / 2.0 if rail == "a" else Lp / 2.0
            sh.append(("line", [at(s, -half), at(s, half)], ink, 0.3))
    else:
        for i in range(4):
            s = -Lp / 2.0 + Lp * i / 3.0
            sh.append(("line", [at(s, -half), at(s, half)], ink, 0.14))
    m = 0.4
    foot = [at(-Lp / 2.0 - m, -half - m), at(Lp / 2.0 + m, -half - m), at(Lp / 2.0 + m, half + m),
            at(-Lp / 2.0 - m, half + m)]
    return sh, foot


def _p17_clip_items(items, r):
    """page items cut to the rectangle r (polys, lines, circles, texts)"""
    out = []
    for it in items:
        if it[0] == "poly":
            rings = [c_ for c_ in (_p14_clip_ring(rg, r) for rg in it[1]) if c_]
            if rings:
                out.append(("poly", rings) + tuple(it[2:]))
        elif it[0] == "line":
            for run in _p14_clip_line(it[1], r):
                out.append(("line", run) + tuple(it[2:]))
        elif it[0] == "circle":
            if r[0] <= it[1] <= r[2] and r[1] <= it[2] <= r[3]:
                out.append(it)
        elif it[0] == "text":
            if r[0] <= it[2] <= r[2] and r[1] <= it[3] <= r[3]:
                out.append(it)
    return out


P17_WIN_NAME = {"A": u"Upstream entry", "B": u"Lower reach"}
P17_CUTS = ("W1", "F2", "S4", "F4")    # the sections of page B: cut registry ids, printed as level_name gives them


def _p17_clip_seg(seg, ring):
    """the parts of the segment seg inside ring (sampled every 1/200 of its length)"""
    (ax, ay), (bx, by) = seg
    out, cur = [], None
    n = 200
    for i in range(n + 1):
        t = i / float(n)
        p = (ax + (bx - ax) * t, ay + (by - ay) * t)
        if _p17_pip(p, ring):
            if cur is None:
                cur = [p, p]
            cur[1] = p
        elif cur is not None:
            out.append(cur)
            cur = None
    if cur is not None:
        out.append(cur)
    return [r for r in out if math.hypot(r[1][0] - r[0][0], r[1][1] - r[0][1]) > 0.5]


def _p17_win_corners(fit):
    """the four survey corners of a window fitted by _p17_win_fit"""
    w, h, u, v, c, den = fit
    hw, hh = w / 2.0 * den / 1000.0, h / 2.0 * den / 1000.0
    return [((c[0] + a) * u[0] + (c[1] + b) * v[0], (c[0] + a) * u[1] + (c[1] + b) * v[1])
            for a, b in ((-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh))]


# ---------------------------------------------------------------- key maps (M4 keymap_items: the study-area outline)
# ---------------------------------------------------------------- page A: key map, legend, numbered list, catalogue
def _p17_keymap(pg, box, zooms, log):
    """round 4 (G-R4-9, P17.3): the key map of p17 in box (x0, y0, x1, y1), north up: keymap.py km_map with both plan
    windows as red frames ("A", "B"), the muted base, the study line, the main street and place names (placed clear
    of each other and of the north corner), a thin neatline (D4); the north arrow (north_items, no plate) in its top
    right corner. The map is a keep of the page's TextPage: only its own texts sit on it. Returns its box, or None
    (logged) without basemap data."""
    x0, y0, x1, y1 = box
    name = u"keymap p17"
    nc = 11.0                                            # the north arrow's corner, mm
    try:
        km = km_map([u"A", u"B"], x1 - x0, y1 - y0, zooms=zooms, page=P17_PAGE,
                    legend_box=(x1 - x0 - 8.0, y1 - y0 - nc, x1 - x0, y1 - y0), log=log)
    except Exception as ex:
        log.append(u"FLAG p17 key map not drawn: {}: {}".format(type(ex).__name__, ex))
        return None
    if not km.get("items"):
        log.append(u"FLAG p17 key map not drawn: no basemap data (run the site board once)")
        return None
    R = (x0, y1 - km["h_mm"], x0 + km["w_mm"], y1)
    sp = Page(0, 0)
    sp.tgroup()
    f_, l_, t_ = _p17_map_fns(sp, allow=(name,))
    pg.poly([rect(*R)], fill=COL["white"])
    km_draw(km, lambda q: (R[0] + q[0], R[1] + q[1]), f_, l_, t_, page=P17_PAGE + u" key map", log=log)
    its, _b = _p17_north_items(R[2] - 4.0, R[3] - nc / 2.0, (0.0, 1.0), 6.0)
    basemap_draw(its, lambda p: p, f_, l_, t_)
    sp.tgroup(False)
    pg.items += _p17_clip_items(sp.items, R)
    pg.poly([rect(*R)], fill=None, stroke=COL["ink2"], lw=P17_NEAT)
    pg.keep(R, "map", name)
    return R


def _p17_legend(pg, x, ytop, w, log, hubs=True):
    """the legend of the two plans (G1, G-R4-2 keywords): a drawn sample and a short name for every symbol they
    draw, one column; returns the bottom y of its last text"""
    fs = P17_FS
    pg.text(u"ON THE PLANS", x, ytop - fs, fs, COL["ink_dark"], bold=True)
    y = ytop - fs * 2.45                                 # the first row's baseline
    rows = [("water", place_name("stream") + u", darker = deeper"),
            ("tint", u"what the project changes"),
            ("study", u"study area"),
            ("space", u"water space: number in the list"),
            ("cell", u"lined basin: reed, water mint"),
            ("plant", u"planting, wet to dry"),
            ("shrub", u"shrubs on open ground"),
            ("stones", u"stepping stones"),
            ("bridge", u"footbridge"),
            ("terrace", u"viewing terrace"),
            ("steps", u"sun steps"),
            ("maize", u"farmland: one crop symbol"),
            ("olive", u"orchard: one olive symbol"),
            ("bld", u"building"),
            ("cut", u"section line (p18), the way it looks")]
    if hubs:
        rows.append(("hub", u"hub"))
    if _p17_shade(log):
        rows.append(("shade", u"July shade on the water: " + u", ".join(l_ for _, _, l_, _h in P17_SHADE)))
    pa = _wat_pal()
    low = y
    for kind, lab in rows:
        yy = y - fs * 0.15
        sm = (x, yy - 1.0, x + 6.0, yy + 2.2)
        if kind == "water":
            pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
            pg.line([(x + 1.2, yy + 0.6), (x + 4.8, yy + 0.6)], pa["deep"], 0.2)
        elif kind == "tint":
            pg.poly([rect(*sm)], fill=ML_TINT, alpha=ML_TINT_ALPHA)
        elif kind == "study":
            st_ = BM_STUDY_LINE
            pg.line([(x, yy + 0.6), (x + 6.0, yy + 0.6)], st_["colour"], st_["width_mm"], dash=list(st_["dash_mm"]))
        elif kind == "cell":
            _p17_put(pg, pla_cell_plan("reed", sm, 2.0, 0.15))
        elif kind == "plant":
            fc = PLA_SPECIES["willow"]["colours"]["fill"]
            pg.poly([rect(*sm)], fill=_sec_mix(fc, SEC["paper"], 0.72), stroke=_sec_mix(fc, SEC["paper"], 0.35), lw=0.1)
            _p17_put(pg, pla_plan("willow", x + 1.7, yy + 0.6, 0.45, crown_m=7.0))
            _p17_put(pg, pla_plan("soft_rush", x + 4.6, yy + 0.3, 2.0))
        elif kind == "shrub":
            _p17_put(pg, pla_plan("chaste", x + 1.5, yy + 0.6, 0.8, crown_m=3.0))
            _p17_put(pg, pla_plan("rosemary", x + 3.6, yy + 0.4, 1.2, crown_m=1.2))
            _p17_put(pg, pla_plan("lavender", x + 5.2, yy + 0.9, 1.2, crown_m=0.9))
        elif kind in ("maize", "olive"):
            _p17_put(pg, pla_field_tile(sm, 1.0, crop=kind, symbol_mm=2.6))
        elif kind == "bld":
            pg.poly([rect(*sm)], fill=BLD_COL["fill"], stroke=BLD_COL["edge"], lw=BLD_LW["block"])
        elif kind == "cut":
            cs = KM_CUT
            pg.line([(x + 1.6, yy + 0.6), (x + 6.0, yy + 0.6)], cs["colour"], cs["lw"], dash=list(cs["dash"]))
            pg.line([(x, yy + 0.6), (x + 1.6, yy + 0.6)], cs["colour"], cs["bar_lw"])
            pg.line([(x, yy + 0.6), (x + 1.6, yy + 0.6), (x + 0.8, yy + 2.4), (x, yy + 0.6)], cs["colour"],
                    cs["tri_lw"])
        elif kind == "hub":
            _p17_put(pg, ico_badge("hub", x + 3.0, yy + 0.6, 3.6))
        elif kind in ("stones", "bridge", "terrace", "steps"):
            if kind in ("stones", "bridge"):
                pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
            _p17_put(pg, _p17_struct_plan(kind, (x + 1.2, yy + 0.6), (x + 4.8, yy + 0.6), "a")[0])
        elif kind == "shade":                            # the opaque hatch the plans draw, light to dense
            pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
            for j_, (_l, col, _t, hs_) in enumerate(P17_SHADE):
                xa_ = sm[0] + j_ * 2.0
                for p_, q_ in sec_hatch([(xa_, sm[1]), (xa_ + 2.0, sm[1]), (xa_ + 2.0, sm[3]), (xa_, sm[3])],
                                        hs_ * 0.5, 45.0):
                    pg.line([p_, q_], col, 0.12)
        elif kind == "space":
            f_, s_ = P17_ZONE["WP"]
            pg.poly([rect(*sm)], fill=f_, stroke=s_, lw=0.12)
            _p17_mark(pg, 1, x + 3.0, yy + 0.6, "WP", r_min=1.5)
        ly = r28_para(pg, x + 7.5, y + fs * 1.28, w - 7.5, lab, fs, COL["ink"])
        low = ly
        y = min(y, ly) - fs * 1.45
    return low - fs * 0.35


def _p17_list(pg, x, ytop, w, rows):
    """the numbered water spaces of one plan, under it (G-R4-3: the list next to its drawing): the marker in the
    space's colour, the space's name, the species the design plants there "English (Turkish)" (P17.7), in the
    markers' reading order; returns the bottom y"""
    fs = P17_FS
    y = ytop
    low = ytop
    for n, code, name, keys in rows:
        _p17_mark(pg, n, x + 1.9, y - 1.9, code)
        nms = [_p17_name(k_) for k_ in keys]
        nms = [s_ if i_ == 0 else s_[:1].lower() + s_[1:] for i_, s_ in enumerate(nms)]
        s_ = u"**{}**: {}".format(name, u", ".join(nms)) if nms else u"**{}**".format(name)
        yb = r28_para(pg, x + 4.8, y + fs * 0.2, w - 4.8, s_, fs, COL["ink"])
        low = min(y - 3.8, yb - fs * 0.35)
        y = min(y - 3.8, yb - 0.6)
    return low


def _p17_list_h(rows, w):
    """the height a list takes (measured on a scratch page)"""
    return -_p17_list(Page(0, 0), 0.0, 0.0, w, rows) if rows else 0.0


def _p17_foliage(key):
    t = PLA_SPECIES[key].get("foliage") or u""
    if not t or u"not found" in t or u"UNVERIFIED" in t:
        return None
    return t.split(u" (")[0]


def _p17_height(key):
    """the sourced height range, m with 2 decimals (project rule for heights)"""
    lo, hi = PLA_SPECIES[key].get("h_range") or (None, None)
    if hi is None:
        return None
    if lo is None:
        return u"up to {:.2f} m".format(hi)
    return u"{:.2f}-{:.2f} m".format(lo, hi)


P17_WATER_ICON = {"wet": "water", "moist": "drip", "dry": "drought"}
P17_ROLE_ICON = {"clean": "nutrients", "shade": "shade", "hold the bank": "high_water", "scent": "plants",
                 "flower": "plants", "harvest": "olive"}


def _p17_name(key):
    return plant_name(key) if key in PLANTS else u"{} ({})".format(PLA_SPECIES[key]["name"], PLA_SPECIES[key]["turkish"]) \
        if u"UNVERIFIED" not in PLA_SPECIES[key]["turkish"] else PLA_SPECIES[key]["name"]


def _p17_views(pg, key, x, y, w, h):
    """the species' section silhouette (left) and its top-view crown (right) at ONE size factor, in the box (x, y) -
    (x + w, y + h): the two views of one primitive"""
    half = (w - 1.0) / 2.0
    if key in ("reed", "mint"):
        tall = (PLA_SPECIES[key]["h_m"] or 1.0) + P17_BASIN["depth"] + P17_BASIN["kerb_h"]
        kk = min(h / tall, half / 2.4)
        fl = y + 0.2
        rim = fl + (P17_BASIN["depth"]) * kk
        fn = pla_reed_basin if key == "reed" else pla_mint_cell
        _p17_put(pg, fn(x + 0.4, x + half - 0.4, fl, rim, kk, P17_BASIN["kerb_h"], P17_BASIN["kerb_t"],
                        P17_BASIN["media"]))
        _p17_put(pg, pla_cell_plan(key, (x + half + 1.0, y + h / 2.0 - half / 2.0, x + w, y + h / 2.0 + half / 2.0),
                                   kk, P17_BASIN["kerb_t"]))
        return
    hh, cw = _p17_size(key)
    kk = min(h / hh, half / max(cw, 0.1))
    _p17_put(pg, pla_section(key, x + half / 2.0, y, kk, h_m=hh, crown_m=cw))
    _p17_put(pg, pla_plan(key, x + half + 1.0 + half / 2.0, y + h / 2.0, kk, crown_m=cw))


def _p17_card(pg, x, ytop, w, sp_, photo, photos):
    """one catalogue column (R36): photo, the two views, name with its sources, foliage, water, role (round 3, G4:
    the height is printed once, in the height ranking of the logic diagram). Returns the bottom y."""
    fs = P17_FS
    key = sp_["key"]
    path, credit = photo
    y = ytop
    pg.poly([rect(x, y - PHOTO_H, x + PHOTO_W, y)], fill=C["paper"])     # G17: no frame
    if path:
        photos.append((x, y - PHOTO_H, x + PHOTO_W, y, path))
    y -= PHOTO_H + 1.2
    _p17_views(pg, key, x, y - 15.0, w, 15.0)
    y -= 16.5
    name = _p17_name(key) + u" " + cite(sp_["src"]) + (cite(credit) if credit else u"")
    y = para(pg, x, y, w, name, fs, COL["ink_dark"], bold=True) - 0.4
    fo = _p17_foliage(key)
    if fo:
        y = para(pg, x, y, w, fo, fs, COL["ink"]) - 0.4
    wc, wt = sp_["water"]
    _p17_put(pg, ico_draw(P17_WATER_ICON[wc], x + 1.5, y - 2.45, 3.0))
    y = min(y - 3.3, para(pg, x + 3.6, y, w - 3.6, wt, fs, COL["ink"]) - 0.4)
    ix = x
    for r_ in sp_["role"]:
        _p17_put(pg, ico_draw(P17_ROLE_ICON.get(r_, "plants"), ix + 1.5, y - 2.45, 3.0))
        ix += 3.4
    y = min(y - 3.3, para(pg, ix + 0.4, y, w - (ix - x) - 0.4, u", ".join(sp_["role"]), fs, COL["river_dark"],
                          bold=True) - 0.4)
    return y


def _p17_catalogue(pg, x0, ybot, x1, log, measure=False):
    """the species, wet to dry, one column each, along the foot of page A, then (P16.5, D5) the giant reed card: take
    it out; bottom-aligned at ybot. Returns its box."""
    sps = [s_ for k_ in P17_CAT for s_ in SPECIES if s_["key"] == k_]
    n = len(sps)
    gr = 3.0                                             # the gap before the giant reed card (round 4: 13 photos of
    #                                                      28 mm in 376 mm leave 0.8 mm between columns)
    gap = max(0.6, min(3.0, (x1 - x0 - (n + 1) * PHOTO_W - gr) / max(n - 1, 1)))
    w = PHOTO_W
    if "photos" not in _P17_MEMO:
        state = {}
        out = []
        for s_ in sps:
            p_ = (None, None)
            if PHOTO_ON[0] and s_["key"] in PLANTS:
                path, credit, why = plant_photo_of(s_["key"], log, state)
                p_ = (path, credit)
                if not path:
                    log.append(u"p.17 catalogue: no photo of {} ({})".format(s_["key"], why or u"not loaded"))
            elif s_["key"] not in PLANTS:
                log.append(u"p.17 catalogue: {} has no photo entry in common/plant_photos.py PLANTS".format(s_["key"]))
            out.append(p_)
        _P17_MEMO["photos"] = out
    photos = _P17_MEMO["photos"]
    hmax = max([-_p17_card(Page(0, 0), 0.0, 0.0, w, s_, (None, None), []) for s_ in sps] +
               [-_p17_card_remove(Page(0, 0), 0.0, 0.0, w, log, measure=True)])
    xr = x0 + n * w + (n - 1) * gap + gr
    if measure:
        return (x0, ybot, xr + w, ybot + hmax)
    ytop = ybot + hmax
    for i, (s_, p_) in enumerate(zip(sps, photos)):
        _p17_card(pg, x0 + i * (w + gap), ytop, w, s_, p_, PHOTOS)
    _p17_card_remove(pg, xr, ytop, w, log)
    return (x0, ybot, xr + w, ytop)


def _p17_card_remove(pg, x, ytop, w, log, measure=False):
    """P16.5 (D5): the giant reed (Kargı) as the last card of the species strip: its photo crossed out, its name and
    sources, take it out and why (02 §5: only marked remove). Returns the bottom y."""
    fs = P17_FS
    key, words, src = SPECIES_REMOVE
    path, credit = None, None
    if not measure and PHOTO_ON[0] and key in PLANTS:
        if "photo_remove" not in _P17_MEMO:
            _P17_MEMO["photo_remove"] = plant_photo_of(key, log, {})[:2]
        path, credit = _P17_MEMO["photo_remove"]
    pg.poly([rect(x, ytop - PHOTO_H, x + PHOTO_W, ytop)], fill=C["paper"])   # G17: no frame
    if path:
        PHOTOS.append((x, ytop - PHOTO_H, x + PHOTO_W, ytop, path))
    _p17_put(pg, ico_cross(x + PHOTO_W - 3.5, ytop - 3.5, 5.0, COL["accent"]))
    y = ytop - PHOTO_H - 1.2
    y = para(pg, x, y, w, _p17_name(key) + u" " + cite(src) + (cite(credit) if credit else u""), fs,
             COL["ink_dark"], bold=True) - 0.4
    return r28_para(pg, x, y, w, words, fs, COL["accent"])


P17_FOL_COL = (("evergreen", "3C4733"), ("deciduous", "89986A"), ("herbaceous", "A2B6B5"), (u"not sourced", "DCD9D2"))


def _p17_fol_class(key):
    """evergreen / deciduous / herbaceous from the species' sourced foliage (plants.py), else: not sourced"""
    fo = (_p17_foliage(key) or u"").lower()
    for c_, _col in P17_FOL_COL[:3]:
        if fo.startswith(c_):
            return c_
    return u"not sourced"


def _p17_logic(pg, x0, ytop, x1, h, geos, xb, log):
    """P16.3 / round 4 P17.2: why each plant goes where, one band of three blocks sharing top and bottom edges, from
    the plans' own planting and the species' sourced data only. Block 1 = the planting diagram grouped with its
    legend under ONE title: plan B's planting areas by wet-to-dry band (a booklet scale, P17_BAND_DENS) and, right
    beside it, its key: the bands' share bar and rows (m², %, plans A and B). Block 2: the foliage share bar and rows.
    Block 3, its left edge on plan B's left edge xb when there is room: the species ranked by their sourced maximum
    height at one true scale on one ground line, "English (Turkish)" (P17.7), with the range and the sources.
    Returns its box."""
    fs = P17_FS
    G = P17_G
    yb = ytop - h
    gB = geos.get("B") or {}
    # the shares, plans A and B together (one standard scale, so page mm² / k² = m²)
    bands, fol = [0.0] * len(P17_BANDS), dict((c_, 0.0) for c_, _ in P17_FOL_COL)
    for g_ in geos.values():
        kk = 1000.0 / g_["den"]
        for b, lead, _ring, a in g_.get("drifts") or []:
            bands[b] += a / (kk * kk)
            fol[_p17_fol_class(lead)] += a / (kk * kk)
    rows_b = [(P17_BAND_NAME[i], P17_BAND_COL[i], bands[i]) for i in range(len(P17_BANDS))]
    rows_f = [(c_, col, fol[c_]) for c_, col in P17_FOL_COL]
    log.append(u"p17 logic: bands {} m², foliage {}".format(
        u" / ".join(u"{:,.0f}".format(a) for a in bands),
        u", ".join(u"{} {:,.0f} m²".format(c_, a) for c_, a in sorted(fol.items()) if a > 0)))

    def row_txt(nm, a, tot):
        return u"{} · {:,.0f} m² · {:.0f} %".format(nm, a, 100.0 * a / tot)

    def col_w(rows, title=u""):
        tot = sum(r_[2] for r_ in rows)
        ws = [text_w(row_txt(nm, a, tot), fs) for nm, _c, a in rows if a > 0 and tot > 0]
        return max([3.2 + w_ for w_ in ws] + [text_w(title, fs, True) if title else 0.0, 24.0])
    mtop = ytop - fs * 1.5 - 1.0                         # the top edge the blocks share under their titles

    def shares(x, w, rows):
        tot = sum(r_[2] for r_ in rows)
        y = mtop - 3.6
        xx = x
        for nm, col, a in rows:                          # the 100 % bar
            if tot > 0 and a > 0:
                ww = w * a / tot
                pg.poly([rect(xx, y, xx + ww, y + 3.6)], fill=col)
                xx += ww
        y -= 1.0
        for nm, col, a in rows:                          # its key: chip, name, m², %
            if a <= 0 or tot <= 0:
                continue
            y -= fs * 1.3
            pg.poly([rect(x, y - 0.1, x + 2.4, y + fs * 0.75)], fill=col)
            pg.text(row_txt(nm, a, tot), x + 3.2, y, fs, COL["ink"])
        return y
    # block 1: the band map and its key
    xm = x0 + 1.0                                        # 1 mm in: the scale bar's "0" stays on the page
    xl = xm
    den_m = None
    if gB.get("drifts"):
        R = gB["R"]
        mh = mtop - (yb + 6.0)                           # room under the title, over the scale bar
        den_m = next((d_ for d_ in P17_BAND_DENS if (R[2] - R[0]) * gB["den"] / d_ <= P17_BAND_W and
                      (R[3] - R[1]) * gB["den"] / d_ <= mh), P17_BAND_DENS[-1])
        f = gB["den"] / den_m
        Rm = (xm, mtop - (R[3] - R[1]) * f, xm + (R[2] - R[0]) * f, mtop)

        def M(p):
            return (Rm[0] + (p[0] - R[0]) * f, Rm[1] + (p[1] - R[1]) * f)
        pg.poly([rect(*Rm)], fill=COL["white"])
        pa = _wat_pal()
        for r_ in gB.get("water") or []:
            c_ = _p14_clip_ring(list(r_), R)
            if c_:
                pg.poly([[M(p) for p in c_]], fill=pa["surface"])
        for b, _lead, ring, _a in gB["drifts"]:
            c_ = _p14_clip_ring(list(ring), R)
            if c_:
                pg.poly([[M(p) for p in c_]], fill=_sec_mix(P17_BAND_COL[b], SEC["paper"], 0.25))
        pg.poly([rect(*Rm)], fill=None, stroke=COL["ink2"], lw=P17_NEAT)
        _p12_bar(pg, Rm[0], Rm[1] - 4.0, den_m, P17_BAR.get(den_m, (0, 50, 100, 200)))
        _p17_north_in(pg, Rm, gB.get("nd") or (0.0, 1.0), 4.0, [])
        xl = Rm[2] + 3.0
    t1 = u"PLANTING BANDS · plan B" + (u" · 1:{:,.0f}".format(den_m) if den_m else u"") + u" · m², plans A + B"
    pg.text(t1, xm, ytop - fs, fs, COL["ink_dark"], bold=True)
    wb_ = col_w(rows_b)
    shares(xl, wb_, rows_b)
    # block 2: foliage, beside block 1 (its title clear of block 1's)
    tf = u"FOLIAGE · by the lead species' area"
    xf = max(xl + wb_ + 4.0, xm + text_w(t1, fs, True) + 4.0)
    wf_ = col_w(rows_f, tf)
    pg.text(tf, xf, ytop - fs, fs, COL["ink_dark"], bold=True)
    shares(xf, wf_, rows_f)
    # block 3: the height ranking
    xc = max(xb, xf + wf_ + G)
    if xc > xb + 0.01:
        log.append(u"NOTE p17 logic: the height chart starts {:.0f} mm right of plan B's left edge (the shares need "
                   u"the room)".format(xc - xb))
    wc = x1 - xc
    sps = sorted([k_ for k_ in P17_CAT if (PLA_SPECIES[k_].get("h_range") or (None, None))[1]],
                 key=lambda k_: -PLA_SPECIES[k_]["h_range"][1])
    title = u"HEIGHT · each species' sourced maximum, one scale"
    pg.text(title, xc, ytop - fs, fs, COL["ink_dark"], bold=True)
    ax = 9.0                                             # the axis labels' column
    cw = (wc - ax) / max(1, len(sps))
    src_of = dict((s_["key"], s_["src"]) for s_ in SPECIES)

    def words(pg_, key, xx, yy):
        nm = P17_SHORT.get(key, PLA_SPECIES[key]["name"].lower())
        tr = _p17_tr(key)
        y_ = para(pg_, xx, yy, cw - 1.0, nm + (u" ({})".format(tr) if tr else u""), fs, COL["ink_dark"], bold=True)
        y_ = para(pg_, xx, y_ - 0.3, cw - 1.0, (_p17_height(key) or u"") + u" " + cite(src_of.get(key, u"")), fs,
                  COL["ink"])
        return y_ - fs * 0.3
    tdeep = max(-words(Page(0, 0), k_, 0.0, 0.0) for k_ in sps) if sps else 0.0
    gy = yb + tdeep + 1.0                                # the ground line
    top = mtop - 1.0
    hmax = max(PLA_SPECIES[k_]["h_range"][1] for k_ in sps) if sps else 1.0
    step = 10.0 if hmax > 20.0 else 5.0
    hgrid = step * math.ceil(hmax / step)
    ks = (top - gy) / hgrid                              # mm per m, the same for every species
    if ks <= 0:
        log.append(u"WARNING p17 logic: no room for the height chart ({:.0f} mm)".format(top - gy))
        ks = 0.1
    marks = [0.0] + ([5.0] if 5.0 * ks >= fs * 1.5 and step > 5.0 else []) + \
        [step * i for i in range(1, int(hgrid / step) + 1) if step * i * ks >= fs * 1.5]
    for v_ in marks:
        yy = gy + v_ * ks
        pg.line([(xc + ax, yy), (xc + wc, yy)], COL["faint"] if v_ else COL["ink2"], 0.06 if v_ else 0.15)
        pg.text(u"{:.0f} m".format(v_), xc + ax - 1.0, yy - fs * 0.35, fs, COL["ink2"], align="R")
    for i, key in enumerate(sps):
        xm_ = xc + ax + (i + 0.5) * cw
        hi = PLA_SPECIES[key]["h_range"][1]
        crown = min(PLA_SPECIES[key]["crown_m"] or 1.0, 0.95 * cw / ks)   # a crown never wider than its column
        if key in ("reed", "mint"):                      # these grow only in lined cells: drawn in a small lined cell
            cx0, cx1 = xm_ - 0.4 * cw, xm_ + 0.4 * cw
            cell = pla_reed_basin if key == "reed" else pla_mint_cell
            _p17_put(pg, cell(cx0, cx1, gy - 0.5 * ks, gy, ks, 0.0, h_m=hi))
        else:
            _p17_put(pg, pla_section(key, xm_, gy, ks, h_m=hi, crown_m=crown, seed=i + 3))
        words(pg, key, xc + ax + i * cw + 0.3, gy - 1.0)
    return (x0, yb, x1, ytop)


def _p17_tr(key):
    """the Turkish name of a species as the catalogue prints it ("English (Turkish)"), or None"""
    m = re.search(u"\\(([^()]*)\\)\\s*$", _p17_name(key) or u"")
    return m.group(1) if m else None


def _p17_layout(den, pa, pb, W, H1, leg_h, log, force=False):
    """round 4 (P17.1): the plans' row at 1:den, or None when it does not fit. Columns: key map over the legend
    (P17_LW), plan A, plan B (B takes the width left over: more context, same scale); in each plan column the
    heading strip, the window, the scale bar row and its own numbered list end on one line: each window grows in
    height to fill its column (same scale, more context). Returns dict(den, fa, fb) with the grown fits."""
    G = P17_G
    fa, fb = _p17_win_fit(pa, den), _p17_win_fit(pb, den)
    spare = W - P17_LW - G - fa[0] - G - fb[0]
    if not force and (spare < 0 or H1 - P17_HEADH - leg_h - G < P17_KM_MIN):
        return None
    wa, wb = fa[0], fb[0] + max(0.0, spare)
    ga, gb = fa, (wb,) + tuple(fb[1:])
    hs = None
    for _it in range(4):
        seen = {}
        ra = _p17_rows(ga, log, seen, 1)
        rb = _p17_rows(gb, log, seen, 1 + len(ra))
        ha = H1 - P17_HEADH - P17_BARH - _p17_list_h(ra, wa)
        hb = H1 - P17_HEADH - P17_BARH - _p17_list_h(rb, wb)
        if not force and (ha < fa[1] - 1e-6 or hb < fb[1] - 1e-6):
            return None
        ha, hb = max(ha, fa[1]), max(hb, fb[1])
        ga, gb = (wa, ha) + tuple(fa[2:]), (wb, hb) + tuple(fb[2:])
        if hs == (round(ha, 2), round(hb, 2)):
            break
        hs = (round(ha, 2), round(hb, 2))
    return dict(den=den, fa=ga, fb=gb)


def p17_page(pg, box, opt, log):
    """round 4 (S6b, P17.1-P17.7; booklet p17 "Which plant goes where", crop wb_plants): three rows filling the box.
    Row 1, the plans: the key map (km_map) over the legend at the left, plan A, plan B, at the largest standard
    scale at which the row fits (P17_DENS, one scale for both); each plan with its heading strip (letter, name,
    scale), its scale bar and its own numbered list under it; both plan columns end on one line. Row 2, the logic
    band (_p17_logic: the band map grouped with its key, the foliage shares, the height chart). Row 3, the species
    catalogue along the foot. The box is widened to the cell (3.5 mm each side, 3 mm down: the catalogue's 13 photos
    of 28 mm need it). Every text goes through the cell's TextPage (build_board: text_page / check_text). Returns
    [(crop id, bbox, scale denominator)]."""
    if _P17_MEMO.get("run") != id(pg):                  # a new run reads its data afresh
        _P17_MEMO.clear()
        _P17_MEMO["run"] = id(pg)
    bx0, by0, bx1, by1 = box
    x0, y0, x1, y1 = bx0 - 3.5, by0 - 3.0, bx1 + 3.5, by1
    W = min(x1 - x0, P17_W)
    x1 = x0 + W
    n0 = len(pg.items)
    G = P17_G
    fs = P17_FS
    cb = _p17_catalogue(pg, x0, y0, x1, log, measure=True)
    ch = cb[3] - cb[1]
    ytop = y1
    ylog = y0 + ch + G + P17_LOGIC_H                     # the logic band's top
    yrow = ylog + G                                      # row 1's bottom
    H1 = ytop - yrow
    hubs_any = bool(_p17_hubs(log))
    leg_h = -_p17_legend(Page(0, 0), 0.0, 0.0, P17_LW, log, hubs_any)
    pa, pb = _p17_win_pts("A", log), _p17_win_pts("B", log)
    lay = None
    for den in P17_DENS:
        lay = _p17_layout(den, pa, pb, W, H1, leg_h, log)
        if lay:
            break
    if lay is None:
        lay = _p17_layout(P17_DENS[-1], pa, pb, W, H1, leg_h, log, force=True)
        log.append(u"WARNING p17: the plans do not fit at any standard scale; drawn at 1:{:,.0f} (the page may "
                   u"overflow)".format(lay["den"]))
    den, fa, fb = lay["den"], lay["fa"], lay["fb"]
    xa = x0 + P17_LW + G
    xb = xa + fa[0] + G
    yt = ytop - P17_HEADH                                # the plans' top edge (shared with the key map)
    for key, xk in (("A", xa), ("B", xb)):               # the heading strips: letter, name, scale
        pg.text(u"{} · {} · plan 1:{:,.0f}".format(key, P17_WIN_NAME[key], den), xk, ytop - 3.2, fs,
                COL["ink_dark"], bold=True)
    seen = {}
    ba, ra, sa, ga, hn_a = _p17_window(pg, xa, yt, "A", fa, log, seen)
    bb_, rb, sb_, gb, hn_b = _p17_window(pg, xb, yt, "B", fb, log, seen)
    la = _p17_list(pg, xa, yt - fa[1] - P17_BARH, fa[0], ra)
    lb = _p17_list(pg, xb, yt - fb[1] - P17_BARH, fb[0], rb)
    # the left column: the key map (both windows) over the legend, the legend's foot on row 1's bottom
    kb = None
    if yt - (yrow + leg_h + G) >= 15.0:
        kb = _p17_keymap(pg, (x0, yrow + leg_h + G, x0 + P17_LW, yt),
                         {u"A": _p17_win_corners(fa), u"B": _p17_win_corners(fb)}, log)
    else:
        log.append(u"FLAG p17: no room for the key map over the legend ({:.0f} mm)".format(yt - yrow - leg_h - G))
    ly0 = (kb[1] - G) if kb else yt
    ly = _p17_legend(pg, x0, ly0, P17_LW, log, hn_a + hn_b > 0)
    if min(la, lb, ly) < yrow - 0.5:
        log.append(u"WARNING p17: row 1 runs {:.0f} mm into the logic band".format(yrow - min(la, lb, ly)))
    lgb = _p17_logic(pg, x0, ylog, x1, P17_LOGIC_H, {"A": ga, "B": gb}, xb, log)
    cat = _p17_catalogue(pg, x0, y0, x1, log)            # the species strip at the foot of the box
    for b_, nm in ((ba, u"plan A"), (bb_, u"plan B"), (cat, u"catalogue"), (lgb, u"logic band")):
        pg.block(b_, u"p17 " + nm)
    if kb:
        pg.block((x0, ly, x0 + P17_LW, kb[3]), u"p17 key map and legend")
    placed = dict(sa)
    for c_, ks in sb_.items():
        placed[c_] = list(placed.get(c_, [])) + [k_ for k_ in ks if k_ not in placed.get(c_, [])]
    drawn_ = set(k_ for ks in placed.values() for k_ in ks)
    if drawn_ - set(P17_CAT):
        log.append(u"WARNING p17: drawn but not in the catalogue: {}".format(u", ".join(sorted(drawn_ - set(P17_CAT)))))
    share = (fa[0] * fa[1] + fb[0] * fb[1]) / max(1.0, W * (ytop - y0))
    log.append(u"p17 page: plans 1:{:,.0f} (A {:.0f} x {:.0f}, B {:.0f} x {:.0f} mm, {:.0f} % of the page), species "
               u"planted {}, catalogue {} species, photos {}".format(
                   den, fa[0], fa[1], fb[0], fb[1], 100.0 * share, len(drawn_), len(P17_CAT),
                   sum(1 for p_ in _P17_MEMO.get("photos", []) if p_[0])))
    bbox = items_bbox(pg.items[n0:])
    return [("wb_plants", bbox, den)]
