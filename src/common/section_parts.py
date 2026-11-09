# ---- section language of the main site board (selinus_board draw_section_strip), shared by the water board and the
# agriculture alternatives (Aras 25 Oct 21:52: their sections drawn "such as we draw in the site sections"): the cut
# ground a shade darker than the page with a fine ink line, water hatched in blue from the bed to its surface, the
# channel above it in a pale wash, whole trees and plants at their stated size. One scale for x and y (Aras 22:02:
# "not stretch anything ever"). Pure geometry: each helper returns shapes, the script's sec_put() draws them.
# Round 5 (S3, section kit v2, G-R5-4.1/4.2): every cut material and the water ONE flat colour (SCT, SCT_WATER), the
# soil in lighter layers going down (SCT_SOIL), no hatch pattern drawn by any function here.
#   ("poly", ring, fill, stroke, lw)    ("line", pts, colour, lw)          page mm, y up


def _sec_mix(a, b, t):
    """hex a -> hex b by t (the board's mix(), on hex strings)."""
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


# palette roles of the board's sections (selinus_board parts 01 and 14: slide khaki, paper, ink, the Selinus' blue)
SEC = dict(paper="F1EDDF", ink="4A3F35", ink2="7A6E60", khaki="BCB794", water="7FA4B3", hatch="3E7DAE",
           tree="7E8A57", pine="5F6B43", olive="8E9A6C", trunk="7A6E60", reed="8E9466", reed_head="B49A6C",
           lav="9F86C0", grass="8F9A68")
SEC["soil"] = _sec_mix(SEC["khaki"], SEC["paper"], 0.42)          # SEC_SOIL: the cut ground
SEC["channel"] = _sec_mix(SEC["water"], SEC["paper"], 0.5)        # SEC_CHANNEL: the water body
SEC["wash"] = _sec_mix(SEC["water"], SEC["paper"], 0.72)          # the channel above the water
SEC["crown"] = _sec_mix(SEC["tree"], SEC["paper"], 0.15)          # SEC_CROWN
SEC["crown_lt"] = _sec_mix(SEC["tree"], SEC["paper"], 0.45)
SEC["shrub"] = _sec_mix(SEC["olive"], SEC["paper"], 0.25)
SEC["beyond"] = _sec_mix(SEC["tree"], SEC["paper"], 0.62)         # things beyond the cut: paler
# round 4 (S2, G-R4-6): the greenery keys above (tree, pine, olive, reed, reed_head, lav, grass, crown, crown_lt, shrub,
# beyond) are NOT plant colours any more: every plant colour comes from plants.py pla_colours (S3). They stay only
# because plants.py (S3) and masterplan p24_detail.py:1836 (S8) still read them; those sessions remove the reads and
# the closing step deletes these keys. The legacy greenery helpers sec_tree / sec_shrub / sec_reeds / sec_tufts /
# sec_lavender were deleted here (no caller left).


def sec_hatch(ring, spacing, ang_deg=45.0):
    """The hatch lines of a closed ring (page mm) at ang_deg, spacing apart: [(p, q), ...] (even-odd scan)."""
    import math as _m
    a = _m.radians(ang_deg)
    ca, sa = _m.cos(a), _m.sin(a)
    R = [(ca * x + sa * y, -sa * x + ca * y) for x, y in ring]       # hatch direction along u
    vs = [p[1] for p in R]
    out = []
    k = _m.ceil(min(vs) / spacing)
    while k * spacing < max(vs):
        v = k * spacing
        us = []
        for i in range(len(R)):
            (u0, v0), (u1, v1) = R[i], R[(i + 1) % len(R)]
            if (v0 <= v < v1) or (v1 <= v < v0):
                us.append(u0 + (u1 - u0) * (v - v0) / (v1 - v0))
        us.sort()
        for j in range(0, len(us) - 1, 2):
            p = (ca * us[j] - sa * v, sa * us[j] + ca * v)
            q = (ca * us[j + 1] - sa * v, sa * us[j + 1] + ca * v)
            out.append((p, q))
        k += 1
    return out


def sec_ellipse(cx, cy, rx, ry, n=28):
    import math as _m
    return [(cx + rx * _m.cos(2 * _m.pi * i / n), cy + ry * _m.sin(2 * _m.pi * i / n)) for i in range(n)]


def sec_water(ring, spacing=0.6, lw=0.1):
    """A water body (ring, page mm). Round 5 (S3, G-R5-4.1, PLAN §3): ONE flat colour SCT_WATER["body"] and the
    surface line SCT_WATER["surface"] on top; no hatch (spacing / lw kept so old calls run, unused)."""
    sh = [("poly", ring, SCT_WATER["body"], None, 0.0)]
    top = max(p[1] for p in ring)
    xs = [p[0] for p in ring if abs(p[1] - top) < 1e-6]
    if len(xs) >= 2:
        sh.append(("line", [(min(xs), top), (max(xs), top)], SCT_WATER["surface"], SCT_WATER["surface_lw"]))
    return sh


# Round 5 (S3, G-R5-4.1, PLAN §3 "Section materials"): design values, solid colours only. Q100 / Q500 lines in the
# surface colour, dashed (water.py reads these).
SCT_WATER = dict(body="A2B6B5", surface="5C7A86", surface_lw=0.25, flood="5C7A86")


# ---- section parts (WO-T2b-3, 29 Oct 2026; section_style.py now includes this file): the river bank as it is at the
# cut (brief 02 §4): DSİ stone walls at 5.00 m, embankments at their surveyed angle, loose earth banks, railings and
# parapets; stone, concrete, earth and the gravel bed in their own hatch; terraces and steps cut into the bank.
# Real sizes in m placed by k (page mm per m); a bank's surface runs from its toe at the bed landward.

SCT_DSI_WALL_H_M = 5.00   # revision_2026-10-29/T1/levels/RESULT.md line 18: "DSİ stone walls at bed + 5.00 m" (Aras 28 Oct)

# material fills. Round 5 (S3, G-R5-4.1, U23-U25 "dont have hatches in the sections just give proper colours to the
# things that we cut"): every cut material ONE flat true colour (PLAN §3 design values); no hatch pattern anywhere.
# Material key = colour swatches (sct_material_key).
SCT = dict(stone="A4A1A3",                            # stone / masonry
           concrete="D5D3CE",                         # concrete / deck
           earth="C2A383",                            # = SCT_SOIL top layer (G-R5-4.2)
           gravel="B9B6AC",                           # gravel bed
           timber="9C8466",                           # timber deck
           line=SEC["ink2"],                          # joint lines (insets at 1:100-1:250 only, G-R5-5)
           cut=SEC["ink"])                            # the cut line
SCT_NAMES = dict(stone=u"Stone, masonry", concrete=u"Concrete", earth=u"Earth", gravel=u"Gravel bed",
                 timber=u"Timber deck", water=u"Water")
SCT_LOG = dict(solid=0, detail=0)                     # cut rings drawn flat / with inset joint detail this run


def sct_material_key(materials=("earth", "stone", "concrete", "gravel", "timber", "water")):
    """the material key of a section as colour swatches (G-R5-4.1: the hatch legend becomes a colour key):
    [(swatch dict for item_export Ix.legend, name)]"""
    out = []
    for m in materials:
        col = SCT_WATER["body"] if m == "water" else SCT[m]
        out.append((dict(kind="fill", colour=col, stroke=None), SCT_NAMES.get(m, m)))
    return out


def _sct_rnd(i, j):
    """A fixed pseudo-random number in [0, 1) for grid cell (i, j)."""
    import math as _m
    v = _m.sin(i * 12.9898 + j * 78.233) * 43758.5453
    return v - _m.floor(v)


def _sct_inside(ring, p):
    """Even-odd test: is page point p inside the ring."""
    x, y = p
    c = False
    n = len(ring)
    for i in range(n):
        (x0, y0), (x1, y1) = ring[i], ring[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (x1 - x0) * (y - y0) / (y1 - y0):
            c = not c
    return c


def _sct_clip(ring, p, q):
    """The parts of segment p-q inside the ring: [(a, b), ...]."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ts = [0.0, 1.0]
    n = len(ring)
    for i in range(n):
        (x0, y0), (x1, y1) = ring[i], ring[(i + 1) % n]
        ex, ey = x1 - x0, y1 - y0
        den = dx * ey - dy * ex
        if abs(den) < 1e-12:
            continue
        t = ((x0 - p[0]) * ey - (y0 - p[1]) * ex) / den
        s = ((x0 - p[0]) * dy - (y0 - p[1]) * dx) / den
        if 0.0 < t < 1.0 and 0.0 <= s <= 1.0:
            ts.append(t)
    ts.sort()
    out = []
    for a, b in zip(ts[:-1], ts[1:]):
        if b - a < 1e-9:
            continue
        m = (a + b) / 2.0
        if _sct_inside(ring, (p[0] + dx * m, p[1] + dy * m)):
            out.append(((p[0] + dx * a, p[1] + dy * a), (p[0] + dx * b, p[1] + dy * b)))
    return out


SCT_DETAIL_K = 4.0                    # page mm per m from which a ring gets real joints: 1:250 and larger (G-R5-5 insets)
SCT_COURSE_M = 0.50                   # stone course height (drawing rule, as water.py water_axo course_m; not surveyed)
SCT_BOARD_M = 0.14                    # deck board width (drawing rule, as sf_lane timber; not surveyed)


def sct_hatch_fill(ring, material, k, outline=None, lw=0.25, fill=True, hatch_lw=None):
    """A cut ring (page mm) in its material: stone, concrete, earth, gravel, timber or water. Round 5 (S3, G-R5-4.1):
    ONE flat colour (SCT), no hatch pattern; the name stays so every caller gets solid colours unchanged. At
    1:250 and larger (k >= SCT_DETAIL_K, the zoom insets, G-R5-5) stone shows its courses and timber its boards as
    real joints at drawing-rule sizes (SCT_COURSE_M, SCT_BOARD_M): construction lines, not a hatch. fill=False:
    nothing but the outline (the soil gradient under it is the fill). hatch_lw: kept for old calls, unused."""
    if material == "water":
        return sec_water(ring)
    if material not in SCT or material in ("line", "cut"):
        raise ValueError("sct_hatch_fill: unknown material %r" % material)
    sh = [("poly", ring, SCT[material], None, 0.0)] if fill else []
    SCT_LOG["solid"] += 1
    if fill and k >= SCT_DETAIL_K and material in ("stone", "timber"):
        SCT_LOG["detail"] += 1
        ln = _sec_mix(SCT[material], SEC["ink"], 0.35)
        if material == "stone":                   # bed joints every course, head joints staggered (real size)
            c = SCT_COURSE_M * k
            for p, q in sec_hatch(ring, c, 0.0):
                sh.append(("line", [p, q], ln, 0.06))
            ys = [p[1] for p in ring]
            xs = [p[0] for p in ring]
            import math as _m
            j = int(_m.floor(min(ys) / c))
            while j * c < max(ys):
                x = min(xs) + (0.5 * c if j % 2 else 0.0) + 1.6 * c
                while x < max(xs):
                    for a_, b_ in _sct_clip(ring, (x, j * c), (x, (j + 1) * c)):
                        sh.append(("line", [a_, b_], ln, 0.05))
                    x += 1.6 * c                  # stone length 0.80 m (drawing rule)
                j += 1
        else:                                     # deck boards: vertical joints SCT_BOARD_M apart
            for p, q in sec_hatch(ring, SCT_BOARD_M * k, 90.0):
                sh.append(("line", [p, q], ln, 0.04))
    if outline:
        sh.append(("poly", ring, None, outline, lw))
    return sh


# Soil v2 (round 5, S3, G-R5-4.2, U34/U36/U40/U56/U61/U65: "the top layer a lighter brown, each deeper layer lighter
# still; the layering logic stays"): drawing rules, not measured soil data. A topsoil band SCT_SOIL["top_m"] thick
# in layers[0] at the surface, then the other layers in equal bands following the surface down to the cut bottom,
# each lighter (PLAN §3 values). No hatch over the soil (G-R5-4.1). top / bottom / steps / hatch_lw kept for old reads.
SCT_SOIL = dict(layers=("C2A383", "D0B699", "DDC9B0", "E9DDCB"), top="C2A383", bottom="E9DDCB", top_m=0.30, steps=3,
                hatch_lw=0.053)


def sct_soil_gradient(surface, bottom_y, k):
    """G-R5-4.2 soil under a surface polyline (page mm, left to right) down to bottom_y: the topsoil band (SCT_SOIL
    top_m x k deep under every point of the surface) in layers[0], then one band per further layer, each parallel to
    the surface, lighter going down, the last reaching bottom_y. Opaque fills only, no strokes. Returns shapes."""
    S = [(float(x), float(y)) for x, y in surface]
    if len(S) < 2:
        return []
    t = SCT_SOIL["top_m"] * k
    cols = list(SCT_SOIL["layers"])
    n = len(cols) - 1
    b = float(bottom_y)

    def depth_at(y, f):                       # f = 0 at the topsoil's underside .. 1 at the cut bottom
        top = max(b, y - t)
        return top - (top - b) * f

    sh = [("poly", [(x, y) for x, y in S] + [(x, max(b, y - t)) for x, y in reversed(S)], cols[0], None, 0.0)]
    for i in range(n):
        fa, fb = i / float(n), (i + 1) / float(n)
        ring = [(x, depth_at(y, fa)) for x, y in S] + [(x, depth_at(y, fb)) for x, y in reversed(S)]
        sh.append(("poly", ring, cols[i + 1], None, 0.0))
    return sh


def sct_ground(surface, bottom_y, k, material="earth", lw=0.35):
    """Cut ground under a surface polyline (page mm, left to right) down to bottom_y: its solid material and the cut
    line. material "earth": the soil v2 layers (sct_soil_gradient, G-R5-4.2), no hatch (round 5)."""
    ring = list(surface) + [(surface[-1][0], bottom_y), (surface[0][0], bottom_y)]
    if material == "earth":
        return sct_soil_gradient(surface, bottom_y, k) + [("line", list(surface), SCT["cut"], lw)]
    return sct_hatch_fill(ring, material, k) + [("line", list(surface), SCT["cut"], lw)]


def sct_bed(x0, x1, bed_y, k, depth_m=1.0, material="gravel"):
    """The stream bed from x0 to x1 (page mm) as a cut band depth_m deep (drawing rule, not a surveyed depth)."""
    return sct_ground([(x0, bed_y), (x1, bed_y)], bed_y - depth_m * k, k, material)


def _sct_w(x, side, pts):
    """Local bank points (u landward from x, page y) -> page points."""
    return [(x + side * u, v) for u, v in pts]


def _sct_v_at(S, u):
    """Page y of a local surface S (u rising) at u; on a vertical face the upper end."""
    v = S[0][1] if u <= S[0][0] else S[-1][1]
    for (u0, v0), (u1, v1) in zip(S[:-1], S[1:]):
        if u1 > u0 and u0 <= u <= u1:
            v = v0 + (v1 - v0) * (u - u0) / (u1 - u0)
    return v


def _sct_terr(S, u0, steps, k, t):
    """Local: surface S with a flight of (rise_m, tread_m) steps cut in from u0 landward -> (new S, step rings)."""
    u, v = u0, _sct_v_at(S, u0)
    P, blocks = [(u, v)], []
    for rise, tread in steps:
        v2, u2 = v + rise * k, u + tread * k
        P += [(u, v2), (u2, v2)]
        blocks.append([(u, v - t), (u, v2), (u2, v2), (u2, v - t)])      # each step on its own bed, t below
        u, v = u2, v2
    g = _sct_v_at(S, u)
    if g > v + 1e-6:                          # ground still higher: a retaining face closes the flight
        blocks.append([(u, v - t), (u, g), (u + t, g), (u + t, v - t)])
    if abs(g - v) > 1e-6:
        P.append((u, g))
    S2 = [p for p in S if p[0] < u0 - 1e-9] + P + [p for p in S if p[0] > u + 1e-9]
    return S2, blocks


def sct_terraces(surface, x0, steps, side, k, t_m=0.15, material="concrete"):
    """Steps or terraces [(rise_m, tread_m), ...] cut into a bank surface from page x0, climbing landward (side +1 =
    to the right). Returns (new surface, step shapes); fill the ground under the new surface (sct_ground)."""
    xr = surface[0][0]
    S = [(side * (px - xr), py) for px, py in surface]
    S2, blocks = _sct_terr(S, side * (x0 - xr), steps, k, t_m * k)   # t_m: slab bed, drawing rule (not sourced)
    sh = []
    for b in blocks:
        sh += sct_hatch_fill(_sct_w(xr, side, b), material, k, SCT["cut"], 0.25)
    return _sct_w(xr, side, S2), sh


def _sct_need(p, name, kind):
    if p.get(name) is None:
        raise ValueError("sct_bank %s: %s is required (no sourced value)" % (kind, name))
    return float(p[name])


def sct_bank(kind, x, top_y, bed_y, side, k, **p):
    """One river bank at the cut: kind dsi_wall | embankment | earth | railing | parapet. x = toe (water face of a
    wall), side +1 = land to the right of x. Returns (shapes, surface: page points from the toe landward)."""
    import math as _m
    reach = p.get("reach_m", 4.0) * k        # drawing rule: land drawn 4 m behind the crest
    bot = bed_y - p.get("depth_m", 1.0) * k   # drawing rule: cut ground drawn 1 m below the bed
    sh = []
    if kind == "railing":                     # post with the handrail and mid rail in cut (symbols, no sourced sizes)
        h = _sct_need(p, "h_m", kind) * k
        r = max(0.35, 0.03 * k)
        sh = [("line", [(x, top_y), (x, top_y + h)], SCT["cut"], 0.25),
              ("poly", sec_ellipse(x, top_y + h, r, r, 10), SCT["cut"], None, 0.1),
              ("poly", sec_ellipse(x, top_y + h * 0.5, r * 0.6, r * 0.6, 8), SCT["cut"], None, 0.1)]
        return sh, []
    if kind == "parapet":                     # solid wall on the crest, from x landward
        h, t = _sct_need(p, "h_m", kind) * k, _sct_need(p, "t_m", kind) * k
        ring = [(0.0, top_y), (0.0, top_y + h), (t, top_y + h), (t, top_y)]
        sh = sct_hatch_fill(_sct_w(x, side, ring), p.get("material", "stone"), k, SCT["cut"], 0.35)
        return sh, _sct_w(x, side, [(0.0, top_y + h), (t, top_y + h)])
    if kind == "dsi_wall":                    # the DSİ stone wall; thickness t_m not sourced: required
        t = _sct_need(p, "t_m", kind) * k
        if top_y is None:
            top_y = bed_y + SCT_DSI_WALL_H_M * k
        wall = [(0.0, bed_y), (0.0, top_y), (t, top_y), (t, bed_y)]
        back = [(t, top_y), (t + reach, top_y), (t + reach, bot), (0.0, bot), (0.0, bed_y), (t, bed_y)]
        S = [(0.0, bed_y), (0.0, top_y), (t + reach, top_y)]
        sh += sct_hatch_fill(_sct_w(x, side, back), "earth", k)
        sh += sct_hatch_fill(_sct_w(x, side, wall), p.get("material", "stone"), k, SCT["cut"], 0.35)
        W = _sct_w(x, side, S)
        sh.append(("line", W, SCT["cut"], 0.35))
        return sh, W
    if kind in ("embankment", "earth"):       # angle_deg (toe to crest) or run_m required
        if p.get("run_m") is not None:
            run = float(p["run_m"]) * k
        else:
            run = (top_y - bed_y) / _m.tan(_m.radians(_sct_need(p, "angle_deg", kind)))
        if kind == "embankment":
            S = [(0.0, bed_y), (run, top_y), (run + reach, top_y)]
        else:                                 # loose earth: soft toe and rounded crest, same toe, crest and run
            n = 12
            S = [(run * i / n, bed_y + (top_y - bed_y) * (3 * (i / float(n)) ** 2 - 2 * (i / float(n)) ** 3))
                 for i in range(n + 1)] + [(run + reach, top_y)]
        blocks = []
        if p.get("steps"):
            S, blocks = _sct_terr(S, p.get("steps_from_m", 0.0) * k, p["steps"], k, p.get("step_t_m", 0.15) * k)
        sh += sct_hatch_fill(_sct_w(x, side, S + [(S[-1][0], bot), (0.0, bot)]), p.get("material", "earth"), k)
        if p.get("revet") and kind == "embankment" and not blocks:   # pitching on the slope, revet_t_m thick
            tt = _sct_need(p, "revet_t_m", kind) * k
            L = _m.hypot(run, top_y - bed_y)
            nx, ny = (top_y - bed_y) / L * tt, -run / L * tt              # into the bank
            ring = [(0.0, bed_y), (run, top_y), (run + nx, top_y + ny), (nx, bed_y + ny)]
            sh += sct_hatch_fill(_sct_w(x, side, ring), p["revet"], k, SCT["cut"], 0.2)
        for b in blocks:
            sh += sct_hatch_fill(_sct_w(x, side, b), p.get("step_material", "concrete"), k, SCT["cut"], 0.25)
        W = _sct_w(x, side, S)
        sh.append(("line", W, SCT["cut"], 0.35))
        return sh, W
    raise ValueError("sct_bank: unknown kind %r" % kind)


def sct_profile(left, right):
    """One cross-section line, left to right, from the left bank surface (side -1) and the right one (side +1)."""
    return list(reversed(left)) + list(right)


def sct_channel(profile, wl_y, spacing=0.6):
    """The water standing at page y wl_y in a profile (left to right): sec_water shapes, one per wet stretch."""
    sh, run = [], []
    P = list(profile)
    for i, a in enumerate(P):
        if a[1] < wl_y:
            if not run:
                if i > 0:
                    b = P[i - 1]
                    t = (wl_y - b[1]) / (a[1] - b[1])
                    run.append((b[0] + (a[0] - b[0]) * t, wl_y))
                else:
                    run.append((a[0], wl_y))
            run.append(a)
        elif run:
            b = P[i - 1]
            t = (wl_y - b[1]) / (a[1] - b[1])
            run.append((b[0] + (a[0] - b[0]) * t, wl_y))
            sh += sec_water(run, spacing)
            run = []
    if run:
        run.append((P[-1][0], wl_y))
        sh += sec_water(run, spacing)
    return sh
