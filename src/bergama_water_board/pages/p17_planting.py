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
#   Round 5 (S8, booklet p18 "Which plant goes where (plans A, B)", 25-page numbering; WBX_PG_PLANTS): the board only
#        records; p17_page hands its drawings to the booklet (parts/wb_items.py): the key map (km_map v2, no scale_den,
#        wbx_keymap; not drawn here), plan A and plan B (1:den, metres, north_deg from the window's turn; no scale bar,
#        north arrow, neatline or heading drawn), each plan's numbered list (wbx_list, anchored at the markers), the
#        plans' legend (wbx_legend), the band map (P18.3: the same band colours as the plans and the same water-space
#        numbers), the band and foliage share bars with their keys, the height chart, one drawing per catalogue card;
#        crop "wb_plants" on each. P18.2 (G-R5-7): the planned wet-to-dry bands are the cores; the rest of the
#        project (the study area) is planted by the ONE placer (common/planting.py pln_place: fading from the cores,
#        nothing outside the project); the base map's farms and orchards keep their symbol only inside the study area
#        (flat tint outside). G-R5-8: the zone fields are drawn under the stream. A1: greenery colours from pla_green.
#        C10: masterplan_results.json and shade_july.json by bg_result + bg_this_run.
#   v16 (round 6, S5; new booklet page 16 "Which plant goes where", SON page18; export ids p18_* kept): G6-1 the two
#        plan windows sized to the SON target frames (A [20,12 21x29] %, B [42,12 55x36] %) at one scale
#        (_p17_frame_fits); G6-4 the section cuts as an_cut end marks outside each plan (no line across), north by
#        an_north under each plan (booklet north_deg None for A/B, so one arrow); G6-5 the key map by km_keymap (cuts
#        W1 F2 S4 F4 + windows A, B); G6-6 every legend and the fills it keys from the hue table (hue(); bands GRN r1-r4
#        wet to dry, water spaces WW, places people use MOV, hub PUB r1, shade CTX, foliage GRN by layer; legend rows
#        by legend_group); G6-8 no source marks inside the narrow chart / card columns (the SON overlaps): one source
#        line per strip; G6-9 every element drawn under pg.g(kind, eid) (base map by layer, each plant by species).
# The S4 placer is not included by code.py yet: included here (a second include elsewhere is harmless).

P17_TITLE = u"PLANTING AND WATER · where each plant goes around the water spaces"
P17_W = 377.0                        # the most a page takes, mm (the booklet's A3 panel at 1:1)
P17_CAT = ("reed", "mint", "soft_rush", "loosestrife", "willow", "tamarisk", "chaste", "ash", "plane", "olive",
           "rosemary", "lavender")   # the catalogue, wet to dry: every species the two pages draw
P17_DENS = (1000.0, 2000.0, 2500.0, 5000.0, 7500.0, 10000.0, 15000.0, 25000.0)   # v15.2: + booklet 7500-25000; the plan windows: the first standard scale at which both fit
P17_BAR = {1000.0: (0, 10, 20, 50), 2000.0: (0, 20, 50, 100), 2500.0: (0, 20, 50, 100), 5000.0: (0, 50, 100, 200),
           7500.0: (0, 50, 100, 200), 10000.0: (0, 50, 100, 200), 15000.0: (0, 100, 200, 500), 20000.0: (0, 200, 500),
           25000.0: (0, 200, 500)}   # labels at least 2 mm apart
P17_FS, P17_HEAD = FS_MIN, 3.4       # label and heading sizes, mm
# round 3 (D2, P16.4): the summer strip is no longer drawn in plan (no squiggle); it is shown in the sections only
# round 5 (A1): WP (the wetland: planting) from the plant module (pla_green meadow / grass, lightened: design mix);
# the water (WT lined cells, WD spillway, ARM, WIDEN) and ground (GR, WS) colours stay
# v16 (round 6, S5; G6-6, PLAN §2.6, H1 "Which plant goes where"): (fill, edge) from the hue table only: the water
# works WW (reed basins r4 / r3, spillway r3 / r2, dry-top terraces r4 / r1, side arm r3 / r1, widened stream r4 / r2;
# P-4: an r4 tint always with an r1-r3 edge), the shaded walk MOV r4 / r3, the wetland planting GRN r4 / r3
P17_ZONE = {"WT": (hue("WW", 4), hue("WW", 3)), "WD": (hue("WW", 3), hue("WW", 2)), "GR": (hue("MOV", 4), hue("MOV", 3)),
            "WS": (hue("WW", 4), hue("WW", 1)), "WP": (hue("GRN", 4), hue("GRN", 3)),
            "ARM": (hue("WW", 3), hue("WW", 1)), "WIDEN": (hue("WW", 4), hue("WW", 2))}
# July shade: (hours under, colour, label, hatch spacing mm): drawn as an opaque fine hatch (G9: no alpha), so the
# water texture under it stays visible
# v16 (G6-6): the shade classes in the context hue, more shade = darker (CTX r4 / r3 / r2)
P17_SHADE = ((2.0, hue("CTX", 4), u"under 2 h", 2.0), (5.0, hue("CTX", 3), u"2-5 h", 1.2),
             (99.0, hue("CTX", 2), u"over 5 h", 0.7))
P17_NEAT = 0.09                      # a map's neatline, mm (0.25 pt; D4: the only frame kept)
P17_DENS_PLAN = {"space": 0.65, "bank": 0.5}   # P16.2 (U14 "çok dolu"): plan planting density (drawing rule)
P17_CLEAR_M = 10.0                   # P16.2: an open clearing this far round each place people use (drawing rule)
# the four wet-to-dry bands (P17_BANDS) by the words of the page intro; one colour each (PLAN §2 palette), the same on
# p16 (plans, shares) and p17 (the band row under each section)
P17_BAND_NAME = (u"at the water", u"banks that flood", u"moist ground", u"dry tops")
# round 5 (A1, P18.3): the band colours from the plant module (pla_green by the band's plants: rushes, willow /
# tamarisk, plane / ash, olive); the plans' band areas and the band map both fill with _p17_band_fill (one colour
# per band on both, so each band is found on both)
P17_BAND_COL = (pla_green("reed"), pla_green("tree_wet"), pla_green("tree"), pla_green("tree_dry"))
P17_OUTER_DENS = 0.5                 # P18.2: the placer's density beyond the bands (design value; was P17_SHRUB_DENS)
P17_OUTER_MAX = 1500                 # P18.2: the most plants the placer puts in one plan (design value)
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


def _p17_band_fill(b):
    """round 5 (P18.3): the fill of planting band b on the plans, the band map and the band key: one colour.
    v16 (G6-6, H1): GRN r1 (at the water) .. r4 (dry tops), from the hue table (P17_BAND_COL stays the plant-role
    colour p18_sections reads)"""
    return hue("GRN", min(4, b + 1))


def _p17_band_edge(b):
    """v16 (G6-6, P-4): band b's fine edge, one step off its fill in GRN (the r3 / r4 tints edged in r1)"""
    return hue("GRN", (2, 3, 1, 1)[min(3, b)])


def _p17_put_g(pg, groups):
    """v16 (G6-9): [(kind, element id, shapes)] onto pg, each element under its own pg.g group"""
    for kind, eid, shapes in groups:
        with pg.g(kind, eid):
            _p17_put(pg, shapes)


def _p17_regrp(src, dst):
    """v16 (G6-9): the group tag of item src carried onto its cut copy dst (lead's Page tags, code.py _GRP)"""
    g_ = wb_grp_of(src)
    if g_:
        _GRP[id(dst)] = (dst, g_)
    return dst


def _p17_items_bb(items):
    """v16: the box of basemap-format items (fill / line / text: a text counts as a 2 mm square per letter half)"""
    ps = []
    for it in items:
        if it[0] == "fill":
            ps += [q for r_ in it[1] for q in r_]
        elif it[0] == "line":
            ps += list(it[1])
        elif it[0] == "text":
            h_ = 0.6 * len(u"%s" % it[1]) * it[3] + 0.5
            ps += [(it[2][0] - h_, it[2][1] - it[3]), (it[2][0] + h_, it[2][1] + it[3])]
    if not ps:
        return None
    return (min(p[0] for p in ps), min(p[1] for p in ps), max(p[0] for p in ps), max(p[1] for p in ps))


def _p17_ndeg(nd):
    """north_deg for wbx_drawing: true north's page direction nd as degrees counter-clockwise from +y"""
    return round(math.degrees(math.atan2(-nd[0], nd[1])), 2) if nd else None


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
    """masterplan_results.json, read once; {} when missing (logged). Round 5 (C10): found by bg_result (cached/, then
    cached/from_output/, then output/), its age by bg_this_run (logged; a WARNING when it is not from this run)"""
    if "mp" not in _P17_MEMO:
        d = {}
        fn = bg_result("bergama_masterplan", "masterplan_results.json")
        fresh, note = bg_this_run(fn)
        log.append(u"p17: masterplan_results.json {} ({})".format(note, fn))
        try:
            with open(fn, "r", encoding="utf-8") as f:
                d = json.load(f)
        except Exception:
            d = {}
        if d and not fresh:
            msg = u"masterplan_results.json is {}: the plans' hubs and corridor are from that run".format(note)
            wbx_warn(WBX_PG_PLANTS, "stale", msg)
        if not d:
            wbx_warn(WBX_PG_PLANTS, "data", u"no masterplan_results.json: hubs from the chain places, side arm from "
                                            u"its p.23 line")
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
    line). Round 5 (C10): found by bg_result (the site board moved it to cached/), its age by bg_this_run"""
    if "shade" not in _P17_MEMO:
        r = None
        fn = bg_result("selinus_board", "shade_july.json")
        fresh, note = bg_this_run(fn)
        log.append(u"p17: shade_july.json {} ({})".format(note, fn))
        if os.path.isfile(fn) and not fresh:
            msg = u"shade_july.json is {}: the July shade is from that run".format(note)
            wbx_warn(WBX_PG_PLANTS, "stale", msg)
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
    range), no straight evenly spaced line (plants.py _pla_rowlike). Each drift is drawn as its area first (the
    band's colour _p17_band_fill (round 5, P18.3: as on the band map), a fine edge: the band edges follow the
    water), then the low layer, then the crowns, tall on top.
    ring and avoid: page mm. Round 3: water = the water rings (page mm): no area and no plant in them, and every
    placed plant goes through water.py water_clip_points (G8, logged for page); clear = [(x, y, r mm)] open
    clearings round the places people use (P16.2): crowns are left out there, the drift's ground tint stays.
    Returns (shapes, placed [(key, x, y, crown_m)], drifts [(band, lead key, area ring, area mm²)]).
    v16 (G6-9): shapes = [(kind, element id, shapes)] (put with _p17_put_g): each drift area "plants", each plant
    "trees" (canopy) or "plants" with its designed species in the name (G6-10: proposed planting, no tree_species)"""
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
            if _p17_area(pts) > 0.5:                    # round 5 (P18.3): the band's colour, as on the band map
                sh.append(("plants", u"band %d area %d · %s" % (b + 1, len(info) + 1, P17_BAND_NAME[b]),
                           [("poly", pts, _p17_band_fill(b), _p17_band_edge(b), 0.1)]))
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
            sh.append(_p17_plant_grp(canopy, key, pla_plan(key, x, y, k, crown_m=2.0 * r / k,
                                                           seed=seed + i * 3 + (7 if canopy else 0))))
            out.append((key, x, y, 2.0 * r / k))
    return sh, out, info


def _p17_plant_grp(canopy, key, shapes):
    """v16 (G6-9, G6-10): one proposed plant as a group: (kind, "tree n · Species" / "plant n · Species", shapes);
    the species is the designed one (no tree_species: that rule is for existing survey trees); counted for the
    `trees p16` line"""
    c_ = _P17_MEMO.setdefault("n_plants", {"trees": 0, "plants": 0})
    kind = "trees" if canopy else "plants"
    c_[kind] += 1
    nm = (PLA_SPECIES.get(key) or {}).get("name") or key
    return (kind, u"%s %d · %s" % (u"tree" if canopy else u"plant", c_[kind], nm), shapes)


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
    Round 5 (S8): no north arrow, neatline or scale bar drawn (the booklet draws them; geo "nd" = true north on the
    page); the zone fields under the stream (G-R5-8); the farms' symbols only inside the study area; beyond the
    planned bands the ONE placer (pln_place, P18.2) instead of the shrub scatter; geo "marks" = [(n, code, at)].
    v16 (round 6, S5): G6-4 cut end marks (an_cut) and the north arrow (an_north) outside R; G6-9 groups.
    Returns (drawing box: R grown to hold the outside marks, rows [(n, code, name, species)], {code: species}, geo
    (geo["R"] = the window itself), hubs drawn)."""
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
    # farms and orchards (D7 a, P17.4): one field texture and one crop symbol per area, under the base's houses.
    # Round 5 (P18.2, G-R5-7, CHK-5 :848-863): the texture and the symbol only on the part inside the study area (the
    # project); outside it the field is a flat tint (existing land use, no planting symbol)
    fields = []
    n_flat = 0
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
            fg_ = out.g("fields", u"%s %d" % (u"orchard" if crop == "olive" else u"farmland", len(fields)))   # v16 G6-9
            fg_.__enter__()
            _p17_put(out, pla_field_tile(Pc, k, crop=crop, seed=len(fields), texture=False)[:1])   # the flat tint
            ins = [r_ for r_ in (sc_rings_clip(Pc, st_pg, P17_PAGE) if st_pg else []) if len(r_) >= 3]
            if not ins:
                n_flat += 1
            for r_ in ins:
                if _p17_area(r_) < 4.0:
                    continue
                sh = pla_field_tile(r_, k, crop=crop, seed=len(fields))
                if _p17_area(r_) < 140.0:                # too small for its symbol: the texture alone
                    sh = [sh[0]] + [s_ for s_ in sh[1:] if s_[0] == "line" and s_[2] == PLA_ROW]
                _p17_put(out, sh)
            fg_.__exit__(None, None, None)
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
    sz = Page(0, 0)                                      # round 5 (G-R5-8): the zone fields, drawn UNDER the stream
    for i_, r in enumerate(widen):                       # v16 (G6-9): one group per element
        with sp.g("water", u"widened stream %d" % (i_ + 1)):
            sp.poly([[T(p) for p in r]], fill=P17_ZONE["WIDEN"][0], stroke=P17_ZONE["WIDEN"][1], lw=0.1)
    for i_, z in enumerate(zs):                          # the water spaces, flat (planting comes after the shade)
        if z["code"] in P17_ZONE and z["code"] != "WT":
            f_, s_ = P17_ZONE[z["code"]]
            with sz.g("water", u"water space %s %d" % (z["code"], i_ + 1)):
                sz.poly([[T(p) for p in z["ring"]]], fill=f_, stroke=s_, lw=0.12)
    arm_bands = []
    for a in arms:
        P = [T(p) for p in a]
        arm_bands.append(_p14_band(P, 2.0 * P17_ARM_W * k))
        with sp.g("water", u"side arm %d" % len(arm_bands)):
            sp.poly([arm_bands[-1]], fill=P17_ZONE["ARM"][0], stroke=P17_ZONE["ARM"][1], lw=0.12)
    # July shade on the bed and the water spaces (5 m cells, three classes): an opaque fine hatch
    sh = _p17_shade(log)
    spaces = [[Ti(*p) for p in r_] for r_ in water] + [z["ring"] for z in zs] + widen
    if sh:
        cells, day, cm = sh
        hc = cm / 2.0
        sp.cur_grp = u"annotations/July shade"           # v16 (G6-9): the shade hatch as one element
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
        sp.cur_grp = None
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
        with sp.g("paths", u"%s %s %d" % (P17_STRUCT_NAME.get(kind, kind), cid, st_n + 1)):   # v16 (G6-9)
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
                for j_, (kind, rr) in enumerate(cl_):
                    with sp.g("plants", u"lined basin %d · %s" % (j_ + 1, (PLA_SPECIES.get(kind) or {}).get(
                            "name") or kind)):
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
                            with sp.g("ground", u"terrace edge %d" % (int(round((bb - b0) / (7.0 * k))))):
                                sp.line(run, hue("WW", 2), 0.3)   # v16 (G6-6): the terraces' WW edge
                        bb += 7.0 * k
                t_ = P17_MIX_T[code]
                shp, pl, inf = _p17_drift_plan(Rp, k, lambda x_, y_, t_=t_: t_, list(P17_MIX[code]), 40 + 7 * i,
                                               density=ds_, avoid=foot, water=wet, clear=clear, page=P17_PAGE)
                _p17_put_g(sp, shp)
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
                _p17_put_g(sp, shp)
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
                _p17_put_g(sp, shp)
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

    for j, rg in enumerate(parts):
        try:
            shp, pl, inf = _p17_drift_plan(rg, k, t_bank, list(P17_MIX["BANK"]), (7 if key == "A" else 8) + 11 * j,
                                           density=db_, avoid=foot, water=wet, clear=clear, page=P17_PAGE)
            _p17_put_g(sp, shp)
            note("BANK", pl, inf)
        except Exception as ex:
            log.append(u"p17 plan {}: stream banks not planted: {}: {}".format(key, type(ex).__name__, ex))
    # round 5 (P18.2, G-R5-7, U53-U55): the whole project designed, fading. The cores (S23 red) = the planned bands
    # drawn above (the water spaces, the side arm, the bank band: their drift areas and zone rings); the rest of the
    # project = the study area in this window (the plans' project, as p24_tree_set) planted by the ONE placer
    # (common/planting.py pln_place): copses and shrub drifts whose density fades from the cores' edges (no hard
    # edge), species by the wet-to-dry niche from the water, never on water, buildings, streets, fields, the cores
    # or the places people use; nothing outside the project. Replaces round 4's shrub scatter (t_open, pla_low_plan:
    # no outer limit, lavender everywhere far from the water: the purple dots of S23).
    n_open = 0
    cores = [list(r_) for _b, _l, r_, _a in geo if len(r_) >= 3] + [list(r_) for r_ in taken_z if len(r_) >= 3]
    pj_ix = _p17_ring_index(parts, cell)                 # only what reaches the project is passed (speed)
    near = [r_ for r_ in bld + streets + fields if any(_p17_in(pj_ix, cell, p_) for p_ in r_)]
    avoid = cores + list(foot) + near + [[T(p) for p in r_] for r_ in widen] + \
        [sec_ellipse(c_[0], c_[1], c_[2], c_[2], 16) for c_ in clear]
    pkey = u"p18 plan " + key
    try:
        pl_ = pln_place(parts, cores=cores, outer=(), water=wet, k=k, seed=(17 if key == "A" else 19),
                        mix=list(P17_MIX["BANK"]), density=P17_OUTER_DENS, avoid=avoid, max_n=P17_OUTER_MAX,
                        page=pkey, shrubs=True)
        # v16 (G6-9, G6-10): pln_draw's order and seeds, one group per plant with its designed species
        for i_, q_ in enumerate(pl_.get("shrubs", ())):
            _p17_put_g(sp, [_p17_plant_grp(False, q_[0], pla_plan(q_[0], q_[1], q_[2], k, crown_m=q_[3],
                                                                    seed=i_ * 7 + 3))])
        for i_, q_ in enumerate(sorted(pl_.get("trees", ()), key=lambda t_: t_[3])):
            _p17_put_g(sp, [_p17_plant_grp(True, q_[0], pla_plan(q_[0], q_[1], q_[2], k, crown_m=q_[3],
                                                                   seed=i_ * 11 + 1))])
        note("OPEN", [(q[0],) for q in pl_["trees"] + pl_["shrubs"]])
        n_open = len(pl_["trees"]) + len(pl_["shrubs"])
        log.extend(pln_log_lines(pkey))
        if pl_["counts"].get("outside"):
            wbx_warn(WBX_PG_PLANTS, "planting", u"plan {}: {} plants outside the project".format(
                key, pl_["counts"]["outside"]))
    except Exception as ex:
        log.append(u"p17 plan {}: the planting beyond the bands not placed: {}: {}".format(   # v15.1: one WARNING
            key, type(ex).__name__, ex))
        wbx_warn(WBX_PG_PLANTS, "planting", u"plan {}: the planting beyond the bands not placed ({})".format(
            key, type(ex).__name__))
    # map_draw: base -> D9 tint -> the zone fields -> the base stream ("water") -> project (the hook) -> study line,
    # strictly in ML_LAYERS order. Round 5 (G-R5-8): the zone fields go in just before the stream, so the water lies
    # over them; legend_cols / water_ok for the zones log line (S2)
    done, zdone = [False], [False]

    def hook(layer):
        late = layer not in ML_BASE_LAYERS and layer != "proj_tint"
        out.cur_grp = P17_LAYER_GRP.get(layer, u"other/" + layer)   # v16 (G6-9): the shared base, one group a layer
        if not zdone[0] and (layer == "water" or late):
            out.items.extend(sz.items)
            zdone[0] = True
        if not done[0] and late:
            out.items.extend(sp.items)
            done[0] = True
    f_, l_, t_ = _p17_map_fns(out)
    tint = [z["ring"] for z in zs] + widen + [_p14_band(a, 2.0 * P17_ARM_W) for a in arms]
    leg_cols = [ML_TINT, PLA_FIELD] + [v_[0] for v_ in P17_ZONE.values()] + \
        [_p17_band_fill(b_) for b_ in range(len(P17_BANDS))]
    w_ok = [P17_ZONE[c_][0] for c_ in ("WIDEN", "ARM", "WD", "WT", "WP")]
    map_draw(P17_PAGE, T, f_, l_, t_, base, {"proj_tint": ml_tint(tint, study=st or None, page=P17_PAGE)},
             study=st or None, clip=True, order_fn=hook, log=log, legend_cols=leg_cols, water_ok=w_ok)
    out.cur_grp = None
    if not zdone[0]:
        out.items.extend(sz.items)
    if not done[0]:
        out.items.extend(sp.items)
    # v16 (round 6, S5; G6-4): no cut line across the plan any more (km_cut_items gone): the cuts are an_cut end marks
    # outside the frame, drawn on the board after the window is cut to R (below)
    taken = [_p17_tbox(it) for it in out.items if it[0] == "text"]
    # the hubs, the markers. Round 5: no north arrow drawn (the booklet draws it from north_deg: nd = true north's
    # direction on the page)
    nd = (T((0.0, 100.0))[0] - T((0.0, 0.0))[0], T((0.0, 100.0))[1] - T((0.0, 0.0))[1])
    nl = math.hypot(*nd) or 1.0
    nd = (nd[0] / nl, nd[1] / nl)
    for _nm, (X, Y) in hubs:
        with out.g("hubs", u"hub · " + _nm):             # v16 (G6-6, G6-9): PUB r1, one group per hub
            _p17_put(out, ico_badge("hub", X, Y, 4.0, ink=hue("PUB", 1)))
        taken.append((X - 2.0, Y - 2.0, X + 2.0, Y + 2.0))
    rows, marks = [], []
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
        with out.g("labels", u"marker %d · %s" % (num, name)):
            taken.append(_p17_mark(out, num, at[0], at[1], code, keep_pg=pg))
        marks.append((num, code, at))
    for name, (X, Y) in hubs:                            # hub names (G-R4-11: real names), beside the icon or left out
        for x_, y_, al in ((X + 2.8, Y - fs * 0.35, "L"), (X - 2.8, Y - fs * 0.35, "R"), (X, Y + 2.8, "C"),
                           (X, Y - 2.8 - fs * 0.75, "C")):
            b = fm_box(name, x_, y_, fs / PT, True, al, 0.0, False)
            if _p17_free(b, taken, R):
                with out.g("labels", u"hub name · " + name):
                    out.text(name, x_, y_, fs, COL["ink_dark"], bold=True, align=al)
                taken.append(b)
                break
        else:
            log.append(u"p17 plan {}: hub name '{}' left out (no free place)".format(key, name))
    pg.items += _p17_clip_items(out.items, R)
    # v16 (round 6, S5; G6-4): the section cuts W1, F2, S4, F4 as an_cut end marks just outside the frame R (filled
    # triangle + letter, short dashed stub, no line across), then the plain north arrow (an_north) under the plan's
    # right end, clear of the cut marks; the drawing box grows to hold them (Rx, exported by p17_page)
    fns = _p17_map_fns(pg)
    mk_b = []
    n_cut = 0
    for cid in P17_CUTS:
        try:
            a, b = level_ends(cid)
        except Exception:
            continue
        n1, n2 = cut_end_labels(level_name(cid))
        if not _p14_clip_line([T(a), T(b)], R):
            continue                                     # the cut does not cross this window: no mark
        its = an_cut(None, a, b, n1, R, T=T, look=1, names=(n1, n2), page=u"p16")
        if not its:
            continue
        with pg.g("cuts", u"cut %s-%s" % (n1, n2)):
            basemap_draw(its, lambda q_: q_, *fns)
        mk_b.append(_p17_items_bb(its))
        n_cut += 1
    nb = None
    for xy_ in ((R[2] - 3.0, R[1] - 10.0), (R[2] + 4.0, R[1] + 1.0), (R[0] + 3.0, R[1] - 10.0),
                (R[2] + 4.0, R[3] - 9.0)):
        its = an_north(None, xy_, _p17_ndeg(nd) or 0.0, size_mm=6.0)
        nb = _p17_items_bb(its)
        if nb and not any(m_ and tp_hit(nb, m_, 0.8) for m_ in mk_b):
            break
    else:
        wbx_warn(WBX_PG_PLANTS, "overlap", u"plan {}: the north arrow meets a cut mark at every place tried".format(key))
    with pg.g("annotations", u"north arrow"):
        basemap_draw(its, lambda q_: q_, *fns)
    Rx = R
    for m_ in mk_b + [nb]:
        if m_:
            Rx = (min(Rx[0], m_[0] - 0.5), min(Rx[1], m_[1] - 0.5), max(Rx[2], m_[2] + 0.5), max(Rx[3], m_[3] + 0.5))
    # round 5: no neatline and no scale bar on the board (the booklet frames the drawing and draws its bar)
    wat_draw_order_lines(page=u"p17 plan " + key, steps=["ground", "water", "structures", "vegetation", "labels"])
    log.append(u"p17 plan {}: 1:{:,.0f}, {:.0f} x {:.0f} mm, {} places drawn in plan ({} outside the study area left "
               u"out), {} markers, {} hubs, planting beyond the bands {} plants (placer), fields outside the study "
               u"area flat {}, {} cut marks (an_cut)".format(key, den, w, h, st_n, st_out, len(pts), len(hubs), n_open,
                                                            n_flat, n_cut))
    return Rx, rows, placed, dict(drifts=geo, water=wet, R=R, den=den, nd=nd, marks=marks), len(hubs)


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
                wn_orange(log[-1][8:])  # v15.1 (closing): this WARNING line also orange (one sink)
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
    ink = hue("MOV", 1)                                  # v16 (G6-6, H1): the places people use in MOV (r1 lines)
    if kind == "stones":
        for i in range(4):
            s = -Lp / 2.0 + Lp * (i + 0.5) / 4.0
            p = at(s, 0.22 if i % 2 else -0.22)
            sh.append(("poly", sec_ellipse(p[0], p[1], 0.36, 0.3, 10), hue("MOV", 3), hue("MOV", 2), 0.08))
    elif kind in ("bridge", "terrace"):
        ring = [at(-Lp / 2.0, -half), at(Lp / 2.0, -half), at(Lp / 2.0, half), at(-Lp / 2.0, half)]
        sh.append(("poly", ring, hue("MOV", 4), ink if kind == "bridge" else hue("MOV", 2), 0.12))
        if kind == "bridge":
            for o in (-half, half):
                sh.append(("line", [at(-Lp / 2.0, o), at(Lp / 2.0, o)], ink, 0.22))
        else:
            s = -Lp / 2.0 if rail == "a" else Lp / 2.0
            sh.append(("line", [at(s, -half), at(s, half)], ink, 0.3))
    else:
        for i in range(4):
            s = -Lp / 2.0 + Lp * i / 3.0
            sh.append(("line", [at(s, -half), at(s, half)], hue("MOV", 2), 0.14))
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
                out.append(_p17_regrp(it, ("poly", rings) + tuple(it[2:])))   # v16 (G6-9): the tag rides along
        elif it[0] == "line":
            for run in _p14_clip_line(it[1], r):
                out.append(_p17_regrp(it, ("line", run) + tuple(it[2:])))
        elif it[0] == "circle":
            if r[0] <= it[1] <= r[2] and r[1] <= it[2] <= r[3]:
                out.append(it)
        elif it[0] == "text":
            if r[0] <= it[2] <= r[2] and r[1] <= it[3] <= r[3]:
                out.append(it)
        elif it[0] == "image":                           # round 5 (S4 plants may be images): kept, clipped at r
            x_, y_, w_, h_ = it[1:5]
            if x_ < r[2] and x_ + w_ > r[0] and y_ < r[3] and y_ + h_ > r[1]:
                out.append(_p17_regrp(it, tuple(it[:8]) + ((max(r[0], x_), max(r[1], y_), min(r[2], x_ + w_),
                                                            min(r[3], y_ + h_)),)))
    return out


P17_WIN_NAME = {"A": u"Upstream entry", "B": u"Lower reach"}
# v16 (G6-1): the SON target frames of the plans, mm on A3 (frames_p14-22 "SON page18 -> new page 16": A [20,12 21x29] %,
# B [42,12 55x36] %; 1 % x = 4.2 mm, 1 % y = 2.97 mm): both windows take these shapes at one scale
P17_FR_A = (21.0 * 4.2, 29.0 * 2.97)
P17_FR_B = (55.0 * 4.2, 36.0 * 2.97)
P17_STRUCT_NAME = {"stones": u"stepping stones", "bridge": u"footbridge", "terrace": u"viewing terrace",
                   "steps": u"sun steps"}
# v16 (G6-9): the shared base map's layers (map_draw order hook) as groups of their kind
P17_LAYER_GRP = {"base_ground": u"ground/base ground", "base_contours": u"ground/contours",
                 "base_fills": u"buildings/base fills", "base_water": u"water/Selinos", "water": u"water/Selinos",
                 "base_outlines": u"buildings/outlines", "base_names": u"labels/base names",
                 "structures": u"buildings/bridges and structures", "proj_tint": u"annotations/what the project changes",
                 "study": u"annotations/study area", "proj_marks": u"annotations/marks", "proj_labels": u"labels/project"}
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
    """v16 (round 6, S5; G6-5, PLAN §2.5): the key map of new page 16 by THE module (common/keymap.py v3 km_keymap:
    the p08 strong look, the study area as closed rings, the page's own cuts W1, F2, S4, F4 bold red across with end
    marks, both plan windows A, B as zooms); handed to the booklet with wbx_keymap (item p18_keymap); nothing drawn on
    the board. km_keymap writes the `keymap p16 module ...` line itself. box = the most room offered (x0, y0, x1, y1).
    Returns the fitted frame's box at the box's top-left, or None (logged + warning) without basemap data."""
    x0, y0, x1, y1 = box
    try:
        km = km_keymap(u"p16", cut_ids=list(P17_CUTS) + [u"A", u"B"], zooms=zooms, w_mm=x1 - x0, h_mm=y1 - y0,
                       log=log)
    except Exception as ex:
        log.append(u"FLAG p17 key map not made: {}: {}".format(type(ex).__name__, ex))
        wbx_warn(WBX_PG_PLANTS, "keymap", u"key map not made ({})".format(type(ex).__name__))
        return None
    if not km.get("items"):
        log.append(u"FLAG p17 key map not made: no basemap data (run the site board once)")
        wbx_warn(WBX_PG_PLANTS, "keymap", u"key map not made: no basemap data")
        return None
    wbx_keymap(WBX_PG_PLANTS, km, item_id=u"p18_keymap")
    return (x0, y1 - km["h_mm"], x0 + km["w_mm"], y1)


def _p17_legend_rows(log, hubs=True):
    """the legend rows of the two plans [(kind, text)] (G1, G-R4-2 keywords). Round 5 (P18.3): one row per planting
    band in the band's colour (the band map's key uses the same colours and names); P18.2: the placer's lighter
    planting; farms flat outside the study area. v16 (round 6, S5; G6-6): each row carries its hue-table category
    and rank and the rows come out grouped by category, darkest first (hues.py legend_group; the annotations ANN
    last); G6-4: the cut row shows the end mark, not a line"""
    ents = [dict(cat="WAT", rank=2, kind="water", text=place_name("stream") + u", darker = deeper"),
            dict(cat="ANN", rank=1, kind="tint", text=u"what the project changes"),
            dict(cat="ANN", rank=2, kind="study", text=u"study area"),
            dict(cat="WW", rank=2, kind="space", text=u"water space: number in the list"),
            dict(cat="WW", rank=3, kind="cell", text=u"lined basin: reed, water mint")]
    ents += [dict(cat="GRN", rank=i + 1, kind="band%d" % i, text=u"planting band: " + P17_BAND_NAME[i])
             for i in range(len(P17_BANDS))]
    ents += [dict(cat="GRN", rank=4, kind="outer", text=u"designed planting, lighter away from the bands"),
             dict(cat="MOV", rank=3, kind="stones", text=u"stepping stones"),
             dict(cat="MOV", rank=1, kind="bridge", text=u"footbridge"),
             dict(cat="MOV", rank=2, kind="terrace", text=u"viewing terrace"),
             dict(cat="MOV", rank=2, kind="steps", text=u"sun steps"),
             dict(cat="AGR", rank=3, kind="maize", text=u"farmland: one crop symbol, flat outside the study area"),
             dict(cat="AGR", rank=2, kind="olive", text=u"orchard: one olive symbol, flat outside the study area"),
             dict(cat="CTX", rank=4, kind="bld", text=u"building"),
             dict(cat="ANN", rank=3, kind="cut", text=u"section cut: its letter at each end")]
    if hubs:
        ents.append(dict(cat="PUB", rank=1, kind="hub", text=u"hub"))
    if _p17_shade(log):
        ents.append(dict(cat="CTX", rank=3, kind="shade", text=u"July shade on the water: " +
                         u", ".join(l_ for _, _, l_, _h in P17_SHADE)))
    return [(e["kind"], e["text"]) for e in legend_group(ents)]


def _p17_sw_draw(pg, kind, x, y0, w=6.0, h=3.2):
    """the drawn sample of one legend row in the box (x, y0, x + w, y0 + h) (round 4's samples, w = 6, h = 3.2)"""
    yy = y0 + 1.0
    sm = (x, y0, x + w, y0 + h)
    # v16 (G6-6): every sample in the hue table's colours (the stream WAT r3 / r2 / r1 as the base map's stream)
    pa = dict(surface=hue("WAT", 3), edge=hue("WAT", 2), deep=hue("WAT", 1))
    gk_ = pg.g("legend", u"swatch " + kind)               # v16 (G6-9): one group per sample
    gk_.__enter__()
    try:
        _p17_sw_body(pg, kind, x, y0, w, h, yy, sm, pa)
    finally:
        gk_.__exit__(None, None, None)


def _p17_sw_body(pg, kind, x, y0, w, h, yy, sm, pa):
    """v16: the body of _p17_sw_draw (one legend sample)"""
    if kind == "water":
        pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
        pg.line([(x + 1.2, yy + 0.6), (x + 4.8, yy + 0.6)], pa["deep"], 0.2)
    elif kind == "tint":
        pg.poly([rect(*sm)], fill=ML_TINT, alpha=ML_TINT_ALPHA)
    elif kind == "study":
        st_ = BM_STUDY_LINE
        pg.line([(x, yy + 0.6), (x + 6.0, yy + 0.6)], st_["colour"], st_["width_mm"], dash=list(st_["dash_mm"]))
    elif kind == "cell":                                 # v16 (G6-6, H1): the lined basin WW r4 in its WW r3 kerb
        pg.poly([rect(*sm)], fill=P17_ZONE["WT"][0], stroke=P17_ZONE["WT"][1], lw=0.35)
    elif kind.startswith("band"):                        # v16: GRN r1-r4 with its edge, no plant image on it
        b_ = int(kind[4:])
        pg.poly([rect(*sm)], fill=_p17_band_fill(b_), stroke=_p17_band_edge(b_), lw=0.15)
    elif kind == "outer":                                # v16 (P-3): plant swatches GRN: tree r1, shrub r2
        pg.poly([sec_ellipse(x + 1.8, yy + 0.7, 1.5, 1.5, 16)], fill=hue("GRN", 1))
        pg.poly([sec_ellipse(x + 4.6, yy + 0.3, 0.9, 0.9, 12)], fill=hue("GRN", 2))
    elif kind in ("maize", "olive"):
        _p17_put(pg, pla_field_tile(sm, 1.0, crop=kind, symbol_mm=2.6))
    elif kind == "bld":                                  # v16: the base map's buildings as drawn (shared BLD_COL)
        pg.poly([rect(*sm)], fill=BLD_COL["fill"], stroke=BLD_COL["edge"], lw=BLD_LW["block"])
    elif kind == "cut":                                  # v16 (G6-4): the an_cut end mark, no line across
        st_ = AN_CUT                                     # the module's sizes: dashed stub + filled triangle
        pg.line([(x + 2.4, yy + 0.6), (x + 2.4 + st_["stub_mm"], yy + 0.6)], hue("ANN", "cut"), st_["stub_lw"],
                dash=list(st_["dash"]))
        t_ = st_["tri_mm"]
        pg.poly([[(x + 1.4 + t_ * 0.5, yy + 0.6), (x + 1.4 - t_ * 0.5, yy + 0.6), (x + 1.4, yy + 0.6 + t_ * 0.87)]],
                fill=hue("ANN", "ink"))
    elif kind == "hub":
        _p17_put(pg, ico_badge("hub", x + 3.0, yy + 0.6, 3.6, ink=hue("PUB", 1)))
    elif kind in ("stones", "bridge", "terrace", "steps"):
        if kind in ("stones", "bridge"):
            pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
        _p17_put(pg, _p17_struct_plan(kind, (x + 1.2, yy + 0.6), (x + 4.8, yy + 0.6), "a")[0])
    elif kind == "shade":                                # the opaque hatch the plans draw, light to dense
        pg.poly([rect(*sm)], fill=pa["surface"], stroke=pa["edge"], lw=0.25)
        for j_, (_l, col, _t, hs_) in enumerate(P17_SHADE):
            xa_ = sm[0] + j_ * 2.0
            for p_, q_ in sec_hatch([(xa_, sm[1]), (xa_ + 2.0, sm[1]), (xa_ + 2.0, sm[3]), (xa_, sm[3])],
                                    hs_ * 0.5, 45.0):
                pg.line([p_, q_], col, 0.12)
    elif kind == "space":
        f_, s_ = P17_ZONE["WIDEN"]
        pg.poly([rect(*sm)], fill=f_, stroke=s_, lw=0.12)
        _p17_mark(pg, 1, x + 3.0, yy + 0.6, "WIDEN", r_min=1.5)


def _p17_legend(pg, x, ytop, w, log, hubs=True):
    """the legend of the two plans: a drawn sample and a short name for every symbol they draw, one column; returns
    the bottom y of its last text. Round 5: drawn only on a scratch page (to measure the layout); the booklet gets
    the same rows through _p17_legend_export"""
    fs = P17_FS
    pg.text(u"ON THE PLANS", x, ytop - fs, fs, COL["ink_dark"], bold=True)
    y = ytop - fs * 2.45                                 # the first row's baseline
    low = y
    for kind, lab in _p17_legend_rows(log, hubs):
        yy = y - fs * 0.15
        _p17_sw_draw(pg, kind, x, yy - 1.0)
        ly = r28_para(pg, x + 7.5, y + fs * 1.28, w - 7.5, lab, fs, COL["ink"])
        low = ly
        y = min(y, ly) - fs * 1.45
    return low - fs * 0.35


def _p17_legend_export(did, log, hubs=True):
    """round 5: the plans' legend for the booklet (wbx_legend): every row with its drawn sample as a swatch function"""
    ents = []
    for kind, lab in _p17_legend_rows(log, hubs):
        ents.append(((lambda pg_, x_, y_, w_, h_, kind=kind: _p17_sw_draw(pg_, kind, x_, y_, w_, h_)), lab))
    wbx_legend(WBX_PG_PLANTS, did, ents, title=u"On the plans", id=u"p18_plans_legend")
    return len(ents)


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


def _p17_list_export(did, rows, marks):
    """round 5: a plan's numbered water spaces for the booklet (wbx_list), each row anchored at its marker on the
    plan (board mm): "space: species English (Turkish), ..." (P17.7). Plan B's numbers go on from plan A's, so a list
    that does not start at 1 carries its numbers in the text (numbered=False), as the masterplan's p23 lists do"""
    if not rows:
        return 0
    at = dict((n_, p_) for n_, _c, p_ in marks)
    texts = []
    for n, code, name, keys in rows:
        nms = [_p17_name(k_) for k_ in keys]
        nms = [s_ if i_ == 0 else s_[:1].lower() + s_[1:] for i_, s_ in enumerate(nms)]
        texts.append((u"{}: {}".format(name, u", ".join(nms)) if nms else u"{}".format(name), n))
    ns = [n_ for _t, n_ in texts]
    numbered = ns == list(range(1, len(ns) + 1))
    wbx_list(WBX_PG_PLANTS, did, [(u"" if numbered else u"%d " % n_) + t_ for t_, n_ in texts], numbered=numbered,
             anchors_board=[at.get(n_) for n_ in ns], id=did + u"_list")
    return len(texts)


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
    nm_ = (PLA_SPECIES.get(key) or {}).get("name") or key
    with pg.g("frame", u"photo box · " + nm_):          # v16 (G6-9): one group per card element
        pg.poly([rect(x, y - PHOTO_H, x + PHOTO_W, y)], fill=C["paper"])     # G17: no frame
    if path:
        photos.append((x, y - PHOTO_H, x + PHOTO_W, y, path))
    y -= PHOTO_H + 1.2
    with pg.g("trees" if _pla_canopy(key) else "plants", u"views · " + nm_):
        _p17_views(pg, key, x, y - 15.0, w, 15.0)
    y -= 16.5
    # v16 (round 6, S5; G6-8, SON page18 overlaps "Common reed (Kamış)" x "[39][46] / [44][47] / [42][48]" ...): the
    # source marks no longer end the name lines (they lined up across the cards into one row over the names); they go
    # in the catalogue's one source line (_p17_catalogue)
    with pg.g("labels", u"name · " + nm_):
        y = para(pg, x, y, w, _p17_name(key), fs, COL["ink_dark"], bold=True) - 0.4
    fo = _p17_foliage(key)
    if fo:
        with pg.g("labels", u"foliage · " + nm_):
            y = para(pg, x, y, w, fo, fs, COL["ink"]) - 0.4
    wc, wt = sp_["water"]
    with pg.g("annotations", u"water need · " + nm_):
        _p17_put(pg, ico_draw(P17_WATER_ICON[wc], x + 1.5, y - 2.45, 3.0))
        y = min(y - 3.3, para(pg, x + 3.6, y, w - 3.6, wt, fs, COL["ink"]) - 0.4)
    ix = x
    with pg.g("annotations", u"role · " + nm_):
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
    for i, (s_, p_) in enumerate(zip(sps, photos)):      # round 5: one booklet drawing per card (photo included)
        n0_ = wbx_mark(pg)
        xc_ = x0 + i * (w + gap)
        yl_ = _p17_card(pg, xc_, ytop, w, s_, p_, PHOTOS)
        wbx_drawing(u"p18_card_" + s_["key"], WBX_PG_PLANTS, pg, (xc_, min(yl_, ytop - PHOTO_H) - 0.5, xc_ + w, ytop),
                    n0=n0_, den=None, dkind="diagram", group=u"p18_catalogue", scale_bar=False, crop=u"wb_plants")
    n0_ = wbx_mark(pg)
    yl_ = _p17_card_remove(pg, xr, ytop, w, log)
    wbx_drawing(u"p18_card_remove", WBX_PG_PLANTS, pg, (xr, min(yl_, ytop - PHOTO_H) - 0.5, xr + w, ytop), n0=n0_,
                den=None, dkind="diagram", group=u"p18_catalogue", scale_bar=False, crop=u"wb_plants")
    # v16 (round 6, S5; G6-8): the cards' and the height chart's source marks in ONE line under the strip (the
    # species' source + its photo's credit; the height chart cites the same species sources), so no mark sits in
    # the narrow card or chart columns (SON page18: 23 overlaps, all of them a row of marks across the columns)
    key_r, _w_r, src_r = SPECIES_REMOVE
    cr_r = (_P17_MEMO.get("photo_remove") or (None, None))[1]
    parts_ = [u"{} {}{}".format(P17_SHORT.get(s_["key"], _p17_name(s_["key"])), cite(s_["src"]),
                                 cite(p_[1]) if p_[1] else u"") for s_, p_ in zip(sps, photos)]
    parts_.append(u"{} {}{}".format(_p17_name(key_r), cite(src_r), cite(cr_r) if cr_r else u""))
    wbx_text(WBX_PG_PLANTS, u"Sources, species and photos: " + u"; ".join(parts_) + u".", "source",
             group=u"p18_catalogue", id=u"p18_catalogue_sources")
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
    with pg.g("frame", u"photo box · giant reed"):       # v16 (G6-9)
        pg.poly([rect(x, ytop - PHOTO_H, x + PHOTO_W, ytop)], fill=C["paper"])   # G17: no frame
    if path:
        PHOTOS.append((x, ytop - PHOTO_H, x + PHOTO_W, ytop, path))
    with pg.g("annotations", u"remove cross · giant reed"):
        _p17_put(pg, ico_cross(x + PHOTO_W - 3.5, ytop - 3.5, 5.0, COL["accent"]))
    y = ytop - PHOTO_H - 1.2
    with pg.g("labels", u"name · giant reed"):           # v16 (G6-8): its source marks in the catalogue's source line
        y = para(pg, x, y, w, _p17_name(key), fs, COL["ink_dark"], bold=True) - 0.4
    with pg.g("labels", u"remove · giant reed"):
        return r28_para(pg, x, y, w, words, fs, COL["accent"])


# round 5 (A1): the foliage classes' colours from the plant module (pla_green; roles chosen apart from the four band
# colours so the two keys never share a colour: design choice); "not sourced" stays a neutral grey
# v16 (G6-6, P-3): plant swatches by layer in GRN (evergreen r1, deciduous r2, herbaceous r3); not sourced CTX r4
P17_FOL_COL = (("evergreen", hue("GRN", 1)), ("deciduous", hue("GRN", 2)), ("herbaceous", hue("GRN", 3)),
               (u"not sourced", hue("CTX", 4)))


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
    rows_b = [(P17_BAND_NAME[i], _p17_band_fill(i), bands[i]) for i in range(len(P17_BANDS))]   # P18.3: as on the plans
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

    def shares(x, w, rows, did, title):
        """round 5: the 100 % bar as a chart drawing (did) and its rows as the booklet legend of that drawing (chip,
        name, m², %); returns the y the rows would reach (the board layout)"""
        tot = sum(r_[2] for r_ in rows)
        y = mtop - 3.6
        xx = x
        n0_ = wbx_mark(pg)
        for nm, col, a in rows:                          # the 100 % bar
            if tot > 0 and a > 0:
                ww = w * a / tot
                with pg.g("plants", u"share · " + nm):    # v16 (G6-9)
                    pg.poly([rect(xx, y, xx + ww, y + 3.6)], fill=col)
                xx += ww
        if tot > 0:
            wbx_drawing(did, WBX_PG_PLANTS, pg, (x, y, x + w, y + 3.6), n0=n0_, den=None, dkind="chart",
                        title=title, group=u"p18_logic", scale_bar=False, crop=u"wb_plants")
        y -= 1.0
        ents = []
        for nm, col, a in rows:                          # its key: chip, name, m², %
            if a <= 0 or tot <= 0:
                continue
            y -= fs * 1.3
            ents.append((wbx_sw("fill", col), row_txt(nm, a, tot)))
        if ents:
            wbx_legend(WBX_PG_PLANTS, did, ents, title=title, id=did + u"_key")
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
        n0_ = wbx_mark(pg)
        with pg.g("frame", u"band map ground"):          # v16 (G6-9): one group per element
            pg.poly([rect(*Rm)], fill=COL["white"])
        for j_, r_ in enumerate(gB.get("water") or []):
            c_ = _p14_clip_ring(list(r_), R)
            if c_:
                with pg.g("water", u"water %d" % (j_ + 1)):
                    pg.poly([[M(p) for p in c_]], fill=hue("WAT", 3))   # v16 (G6-6): the stream WAT r3, as the plans
        for j_, (b, _lead, ring, _a) in enumerate(gB["drifts"]):
            c_ = _p14_clip_ring(list(ring), R)
            if c_:
                with pg.g("plants", u"band %d area %d · %s" % (b + 1, j_ + 1, P17_BAND_NAME[b])):
                    pg.poly([[M(p) for p in c_]], fill=_p17_band_fill(b))     # P18.3: the plans' band colour
        n_mk = 0
        for num, code, at in gB.get("marks") or []:      # P18.3: plan B's water-space numbers at the same spots
            if R[0] <= at[0] <= R[2] and R[1] <= at[1] <= R[3]:
                X_, Y_ = M(at)
                with pg.g("labels", u"marker %d" % num):
                    _p17_mark(pg, num, X_, Y_, code, r_min=1.2)
                n_mk += 1
        # round 5: no neatline, scale bar or north arrow drawn: the booklet draws them (north_deg as plan B's)
        wbx_drawing(u"p18_bands", WBX_PG_PLANTS, pg, Rm, n0=n0_, den=den_m, origin=(0.0, 0.0), dkind="plan",
                    title=u"Planting bands, plan B", group=u"p18_logic", north_deg=_p17_ndeg(gB.get("nd")),
                    crop=u"wb_plants")
        log.append(u"p17 band map: 1:{:,.0f}, {} water-space numbers as on plan B, band colours as on the plans"
                   .format(den_m, n_mk))
        xl = Rm[2] + 3.0
    t1 = u"PLANTING BANDS · plan B · m², plans A + B"     # the board's layout only (not drawn)
    wbx_text(WBX_PG_PLANTS, u"Planting bands, wet to dry: plan B; areas of plans A and B", "heading",
             did=u"p18_bands" if den_m else None, group=u"p18_logic", id=u"p18_bands_head")
    wb_ = col_w(rows_b)
    shares(xl, wb_, rows_b, u"p18_band_shares", u"Planting bands, plans A and B")
    # block 2: foliage, beside block 1 (its title clear of block 1's)
    tf = u"FOLIAGE · by the lead species' area"
    xf = max(xl + wb_ + 4.0, xm + text_w(t1, fs, True) + 4.0)
    wf_ = col_w(rows_f, tf)
    shares(xf, wf_, rows_f, u"p18_foliage_shares", u"Foliage, by the lead species' area")
    # block 3: the height ranking
    xc = max(xb, xf + wf_ + G)
    if xc > xb + 0.01:
        log.append(u"NOTE p17 logic: the height chart starts {:.0f} mm right of plan B's left edge (the shares need "
                   u"the room)".format(xc - xb))
    wc = x1 - xc
    sps = sorted([k_ for k_ in P17_CAT if (PLA_SPECIES[k_].get("h_range") or (None, None))[1]],
                 key=lambda k_: -PLA_SPECIES[k_]["h_range"][1])
    title = u"Height: each species' sourced maximum, one scale (sources: the catalogue line)"
    n0h = wbx_mark(pg)
    ax = 9.0                                             # the axis labels' column
    cw = (wc - ax) / max(1, len(sps))

    def words(pg_, key, xx, yy):
        nm = P17_SHORT.get(key, PLA_SPECIES[key]["name"].lower())
        tr = _p17_tr(key)
        y_ = para(pg_, xx, yy, cw - 1.0, nm + (u" ({})".format(tr) if tr else u""), fs, COL["ink_dark"], bold=True)
        # v16 (round 6, S5; G6-8, SON page18: "ash (Dişbudak) up to 40.00" x "[34] / [35] / [36] ..." and 9 more):
        # no source mark under each column (the marks lined up into one row across the chart); the same species
        # sources stand in the catalogue's source line (_p17_catalogue)
        y_ = para(pg_, xx, y_ - 0.3, cw - 1.0, _p17_height(key) or u"", fs, COL["ink"])
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
        wn_orange(log[-1][8:])  # v15.1 (closing): this WARNING line also orange (one sink)
        ks = 0.1
    marks = [0.0] + ([5.0] if 5.0 * ks >= fs * 1.5 and step > 5.0 else []) + \
        [step * i for i in range(1, int(hgrid / step) + 1) if step * i * ks >= fs * 1.5]
    for v_ in marks:
        yy = gy + v_ * ks
        with pg.g("annotations", u"height line {:.0f} m".format(v_)):   # v16 (G6-9)
            pg.line([(xc + ax, yy), (xc + wc, yy)], COL["faint"] if v_ else COL["ink2"], 0.06 if v_ else 0.15)
            pg.text(u"{:.0f} m".format(v_), xc + ax - 1.0, yy - fs * 0.35, fs, COL["ink2"], align="R")
    for i, key in enumerate(sps):
        xm_ = xc + ax + (i + 0.5) * cw
        hi = PLA_SPECIES[key]["h_range"][1]
        crown = min(PLA_SPECIES[key]["crown_m"] or 1.0, 0.95 * cw / ks)   # a crown never wider than its column
        nm_ = (PLA_SPECIES.get(key) or {}).get("name") or key
        gk_ = pg.g("trees" if _pla_canopy(key) else "plants", u"%s · %s" % (u"tree" if _pla_canopy(key) else u"plant",
                                                                            nm_))   # v16 (G6-9, G6-10)
        gk_.__enter__()
        if key in ("reed", "mint"):                      # these grow only in lined cells: drawn in a small lined cell
            cx0, cx1 = xm_ - 0.4 * cw, xm_ + 0.4 * cw
            cell = pla_reed_basin if key == "reed" else pla_mint_cell
            _p17_put(pg, cell(cx0, cx1, gy - 0.5 * ks, gy, ks, 0.0, h_m=hi))
        else:
            _p17_put(pg, pla_section(key, xm_, gy, ks, h_m=hi, crown_m=crown, seed=i + 3))
        gk_.__exit__(None, None, None)
        with pg.g("labels", u"height · " + nm_):
            words(pg, key, xc + ax + i * cw + 0.3, gy - 1.0)
    # round 5: the height chart as one chart drawing (scale free in the booklet: its own metre axis)
    wbx_drawing(u"p18_heights", WBX_PG_PLANTS, pg, (xc, yb, x1, mtop), n0=n0h, den=None, dkind="chart", title=title,
                group=u"p18_logic", scale_bar=False, crop=u"wb_plants")
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


def _p17_frame_fits(pa, pb, den, log):
    """v16 (round 6, S5; G6-1): plan A and plan B at 1:den in the shapes of their SON target frames (P17_FR_A,
    P17_FR_B), both grown by ONE factor until each holds its points (_p17_win_fit, same turn and centre): the two
    plans keep one scale and each fills its panel (more context, nothing shrunk into a corner). Returns (fa, fb)."""
    fa0, fb0 = _p17_win_fit(pa, den), _p17_win_fit(pb, den)
    s_ = max(fa0[0] / P17_FR_A[0], fa0[1] / P17_FR_A[1], fb0[0] / P17_FR_B[0], fb0[1] / P17_FR_B[1])
    fa = (P17_FR_A[0] * s_, P17_FR_A[1] * s_) + tuple(fa0[2:])
    fb = (P17_FR_B[0] * s_, P17_FR_B[1] * s_) + tuple(fb0[2:])
    log.append(u"frame p16 plans: A {:.0f} x {:.0f} mm, B {:.0f} x {:.0f} mm at 1:{:,.0f} on the board (target frames "
               u"A [20,12 21x29] %, B [42,12 55x36] %; booklet factor {:.2f})".format(fa[0], fa[1], fb[0], fb[1], den,
                                                                                    1.0 / s_))
    return fa, fb


def p17_page(pg, box, opt, log):
    """round 4 (S6b, P17.1-P17.7; booklet p17 "Which plant goes where", crop wb_plants): three rows filling the box.
    Row 1, the plans: the key map (km_map) over the legend at the left, plan A, plan B, at the largest standard
    scale at which the row fits (P17_DENS, one scale for both); each plan with its heading strip (letter, name,
    scale), its scale bar and its own numbered list under it; both plan columns end on one line. Row 2, the logic
    band (_p17_logic: the band map grouped with its key, the foliage shares, the height chart). Row 3, the species
    catalogue along the foot. The box is widened to the cell (3.5 mm each side, 3 mm down: the catalogue's 13 photos
    of 28 mm need it). Every text goes through the cell's TextPage (build_board: text_page / check_text). Returns
    [(crop id, bbox, scale denominator)].
    Round 5 (S8, booklet p18, WBX_PG_PLANTS): the board only records; the drawings go to the booklet (wb_items.py),
    each with crop "wb_plants": p18_plan_A, p18_plan_B (1:den, metres, north_deg), their lists (wbx_list at the
    markers), the plans' legend (wbx_legend on p18_plan_A), the key map (wbx_keymap, km_map v2), p18_bands (the band
    map, 1:den_m), p18_band_shares / p18_foliage_shares (bars + legend keys), p18_heights, p18_card_<key> and
    p18_card_remove. The layout below still sizes the plan windows (same scale, more context)."""
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
        lay = _p17_layout(5000, pa, pb, W, H1, leg_h, log, force=True)   # v15.2: the v15.1 fallback scale kept
        # v15.2 (2 Nov run warnings): round 5 prints no board page; the booklet sets p18_plan_A/B at its own scale,
        # so a board row that does not fit is a note, not a page overflow
        log.append(u"FLAG p17: the board row (not printed since round 5) does not fit at any standard scale; plan "
                   u"windows sized at 1:{:,.0f}".format(lay["den"]))
    den, fa, fb = lay["den"], lay["fa"], lay["fb"]
    fa, fb = _p17_frame_fits(pa, pb, den, log)          # v16 (G6-1): the SON target frames' shapes at 1:den
    xa = x0 + P17_LW + G
    xb = xa + fa[0] + G + 10.0                           # v16: + room for plan A's outside marks (an_cut, an_north)
    yt = ytop - P17_HEADH                                # the plans' top edge (shared with the key map)
    # round 5: no heading strips drawn (the booklet sets each drawing's title and prints its 1:den itself)
    seen = {}
    out_ = {}
    for key, xk, fk in (("A", xa, fa), ("B", xb, fb)):
        n0_ = wbx_mark(pg)
        out_[key] = _p17_window(pg, xk, yt, key, fk, log, seen)
        g_ = out_[key][3]
        # v16 (G6-4): the plan draws its own plain north arrow (an_north): north_deg None, so the booklet adds none
        wbx_drawing(u"p18_plan_" + key, WBX_PG_PLANTS, pg, out_[key][0], n0=n0_, den=den, origin=(0.0, 0.0),
                    dkind="plan", title=u"{} · {}".format(key, P17_WIN_NAME[key]), group=u"p18_plans",
                    north_deg=None, crop=u"wb_plants")
        _p17_list_export(u"p18_plan_" + key, out_[key][1], g_.get("marks") or [])
    ba, ra, sa, ga, hn_a = out_["A"]
    bb_, rb, sb_, gb, hn_b = out_["B"]
    la = yt - fa[1] - P17_BARH - _p17_list_h(ra, fa[0])    # the board layout only (lists go to the booklet)
    lb = yt - fb[1] - P17_BARH - _p17_list_h(rb, fb[0])
    # the left column: the key map (both windows) over the legend; round 5: both go to the booklet, not drawn here
    kb = None
    if yt - (yrow + leg_h + G) >= 15.0:
        kb = _p17_keymap(pg, (x0, yrow + leg_h + G, x0 + P17_LW, yt),
                         {u"A": _p17_win_corners(fa), u"B": _p17_win_corners(fb)}, log)
    else:
        log.append(u"FLAG p17: no room for the key map over the legend ({:.0f} mm)".format(yt - yrow - leg_h - G))
    n_leg = _p17_legend_export(u"p18_plan_A", log, hn_a + hn_b > 0)
    an_log(u"p16", log=log)                              # v16 (G6-4): `annot p16 cuts=n levels=0`
    hue_log(u"p16", log=log)                             # v16 (G6-6): `legend p16 hues=table`
    np_ = _P17_MEMO.get("n_plants") or {}
    # v16 (G6-10): every tree drawn here is proposed planting with its designed species (no survey trees on the plans:
    # ml_base trees off), so tree_species() is not called; generic = 0
    log.append(u"trees p16 species={} generic=0 (proposed: {} trees, {} shrubs / ground plants, designed species)"
               .format(np_.get("trees", 0), np_.get("trees", 0), np_.get("plants", 0)))
    lgb = _p17_logic(pg, x0, ylog, x1, P17_LOGIC_H, {"A": ga, "B": gb}, xb, log)
    cat = _p17_catalogue(pg, x0, y0, x1, log)            # the species strip at the foot of the box
    for b_, nm in ((ba, u"plan A"), (bb_, u"plan B"), (cat, u"catalogue"), (lgb, u"logic band")):
        pg.block(b_, u"p17 " + nm)
    log.append(u"p17 export: plans A, B 1:{:,.0f} (north_deg {}, {}), key map {}, legend {} rows, lists {} + {} rows "
               u"(lowest at {:.0f} / {:.0f} mm on the board)".format(
                   den, _p17_ndeg(ga.get("nd")), _p17_ndeg(gb.get("nd")), u"made" if kb else u"none", n_leg, len(ra),
                   len(rb), la, lb))
    placed = dict(sa)
    for c_, ks in sb_.items():
        placed[c_] = list(placed.get(c_, [])) + [k_ for k_ in ks if k_ not in placed.get(c_, [])]
    drawn_ = set(k_ for ks in placed.values() for k_ in ks)
    if drawn_ - set(P17_CAT):
        log.append(u"WARNING p17: drawn but not in the catalogue: {}".format(u", ".join(sorted(drawn_ - set(P17_CAT)))))
        wn_orange(log[-1][8:])  # v15.1 (closing): this WARNING line also orange (one sink)
    share = (fa[0] * fa[1] + fb[0] * fb[1]) / max(1.0, W * (ytop - y0))
    log.append(u"p17 page: plans 1:{:,.0f} (A {:.0f} x {:.0f}, B {:.0f} x {:.0f} mm, {:.0f} % of the page), species "
               u"planted {}, catalogue {} species, photos {}".format(
                   den, fa[0], fa[1], fb[0], fb[1], 100.0 * share, len(drawn_), len(P17_CAT),
                   sum(1 for p_ in _P17_MEMO.get("photos", []) if p_[0])))
    bbox = items_bbox(pg.items[n0:])
    return [("wb_plants", bbox, den)]
