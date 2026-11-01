# ---- bridges.py (round 5, S3, 1 Nov 2026; D8 "bridges in every section possible", G-R5-4.7, N4 a, A15) -------------
# ONE module puts the Selinos bridges into any section: which bridge a cut passes, where it stands along the cut, and
# its shapes, drawn only as far as the sources go. Data: data/BRIDGES.py (positions = the bridge-list points, N4 a;
# facts with their sources). Include after levels.py (+ data/LEVELS.py), section_parts.py and, when present,
# basemap.py (deck outlines) and names.py (printed names):
#   #@include ../common/data/BRIDGES.py
#   #@include ../common/bridges.py
#
#   br_near(cid, look=1, max_m=None, t0=None, t1=None) -> [dict(key, name, t, d, rel, seg_m)]
#         every bridge the cut cid passes: rel "cut" (the cut line runs through it: S6), "beyond" (in view, d m
#         beyond the cut plane, within the drawn span t0..t1), "behind" (behind the viewer: NOT drawn, logged).
#         t = m along the cut from its first end (level_ends), d = m beyond the plane (look: +1 as the site board S
#         cuts / p18-20 / p24 / p12, -1 as the W cuts on p13-14, sf_back_buildings' rule).
#   br_section(cid, X=None, Y=None, look=1, t0=None, t1=None, ground=None, top=None, max_m=None, page=None,
#              into=None) -> {"background": shapes, "structures": shapes, "found": [...]}
#         X(t m) -> drawing x, Y(z m a.s.l.) -> drawing y (default identity = the item-export section convention:
#         x = chainage m, y = elevation m, S1 item_export); ground(t) -> the cut's ground z at t (the bed under a
#         bridge; default the cut's LEVELS bed); top = the road / bank-top level z for bridges with no height source
#         (default the cut's higher LEVELS bank top). A bridge beyond the plane is drawn in elevation in "background"
#         (true size, paler with distance; the cut ground in front hides what lies below the banks); a bridge the
#         cut runs through is drawn cut in "structures" (over the water). into = a WaterLayers: the shapes are added.
#         Logs one `bridge <cid> <name|none>` line per call (br_log_lines).
#   br_log_lines() -> the bridge lines and FLAG lines of this run (sec_look_lines prints them)
#
# Sourced vs drawing rules (A15): the FLAG lines name every part drawn by a rule. Üç Kemer: middle arch span 9.60 m
# and bed-to-keystone 10 m, deck 4.50 x 56.40 m, three round arches on two piers (Visit İzmir) are data; side arch
# size, pier width and masonry over the keystone are the round 4 p12 drawing rules (P12_K5_*, same values). Ulucami
# Önü: two eyes (one round, one smaller pointed; Visit İzmir) and the parapet 7.4-8.6 m over the bed (photo-scaled,
# IMG_5814) are data; the eye sizes are drawing rules. Tabak: two openings (data), no height: the deck at the bank
# top, openings not drawn. K1, K2, K6: no data: the deck at the cut's bank top (the road level), BR_RULE deck_t_m.
# Bridge bed level: not surveyed at any bridge -> the cut's own bed (or ground(t)), FLAG.

BR_NEAR_M = 250.0          # in-code rule already used for "the nearest bridge" (selinus_board 15l_r28_site.py:317)
BR_CUT_M = 6.0             # a cut line passing within this of the bridge point runs THROUGH it (cut ends +-3 m, CHK-8)
BR_DECK_MATCH_M = 40.0     # a survey deck ring (basemap "decks") belongs to a bridge whose point lies this close
BR_RULE = dict(deck_t_m=0.50,      # deck slab thickness: section_frame sf_bridge drawing rule (not sourced)
               crown_m=1.0,        # masonry over the keystone to the deck top: p12 P12_K5_CROWN_M (not sourced)
               pier_m=2.0,         # pier width between two arches: p12 P12_K5_PIER_M (not sourced)
               side_frac=0.6,      # side arch = this x the middle arch's span and height: p12 P12_K5_SIDE (not sourced)
               k4_big_frac=0.55,   # Ulucami Önü: the big eye's share of the clear width between its ends (not sourced)
               k4_small_rise=1.25, # the smaller pointed eye: rise / half span (not sourced)
               fade_far=0.70)      # tone toward the paper at BR_NEAR_M beyond the plane (drawing rule, as sf_topo_back)
BR_COL = dict(stone="A4A1A3", deck="D5D3CE", line="7A6E60", paper="FFFFFF")
BR_LOG = []
BR_FLAGS = []


def _br_flag(msg):
    if msg not in BR_FLAGS:
        BR_FLAGS.append(msg)


def br_name(key):
    """the printed name (names.py bridge_name, G16); the key only when names.py is not included"""
    f = globals().get("bridge_name")
    return f(key) if f else key


def br_fact(key, name):
    """a sourced value of a bridge (data/BRIDGES.py), None when there is none"""
    v = BRIDGES[key].get("facts", {}).get(name)
    return None if v is None else v["value"]


def _br_axis(cid, look, ends=None):
    import math as _m
    a, b = ends if ends else level_ends(cid)
    L = _m.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
    u = ((b[0] - a[0]) / L, (b[1] - a[1]) / L)
    f = (-u[1] * look, u[0] * look)                       # beyond the plane = in view (sf_back_buildings rule)
    return a, u, f, L


def br_near(cid, look=1, max_m=None, t0=None, t1=None, ends=None):
    """the bridges cut cid passes (see the module notes), nearest first; ends = ((x1, y1), (x2, y2)) survey m for a
    cut that is not a LEVELS row (p09 street cuts, p24 D1 / D2 spans, A-A')"""
    import math as _m
    a, u, f, L = _br_axis(cid, look, ends)
    mx = BR_NEAR_M if max_m is None else max_m
    t0 = 0.0 if t0 is None else t0
    t1 = L if t1 is None else t1
    out = []
    for key in sorted(BRIDGES):
        x, y = BRIDGES[key]["xy"]
        dx, dy = x - a[0], y - a[1]
        t = dx * u[0] + dy * u[1]
        d = dx * f[0] + dy * f[1]
        tc = min(max(t, 0.0), L)
        seg = _m.hypot(x - (a[0] + u[0] * tc), y - (a[1] + u[1] * tc))
        if seg <= BR_CUT_M:
            rel = "cut"
        elif abs(d) > mx or t < t0 or t > t1:
            continue
        else:
            rel = "beyond" if d > 0 else "behind"
        out.append(dict(key=key, name=br_name(key), t=t, d=d, rel=rel, seg_m=seg))
    out.sort(key=lambda r: abs(r["d"]))
    return out


def _br_deck_span(key, a, u):
    """(ta, tb) m along the cut covered by the bridge's survey deck ring (basemap decks), or None"""
    import math as _m
    if not globals().get("basemap_load"):
        return None
    try:
        D = basemap_load()
    except Exception:
        return None
    x, y = BRIDGES[key]["xy"]
    best = None
    for R in ((D or {}).get("layers") or {}).get("decks", []) or []:
        if len(R) < 3:
            continue
        cx = sum(p[0] for p in R) / float(len(R))
        cy = sum(p[1] for p in R) / float(len(R))
        dd = _m.hypot(cx - x, cy - y)
        if dd <= BR_DECK_MATCH_M and (best is None or dd < best[0]):
            best = (dd, R)
    if best is None:
        return None
    ts = [(p[0] - a[0]) * u[0] + (p[1] - a[1]) * u[1] for p in best[1]]
    return min(ts), max(ts)


def _br_cut_levels(cid):
    """(bed, higher bank top) of the cut from LEVELS; a cut with several crossings (S5, S6) takes the lowest bed and
    the highest top of its rows"""
    rows = [cid]
    try:
        level_cut(cid)
    except KeyError:
        rows = [r["id"] for r in _lv_cut_rows(cid)]
    if not rows:
        return None, None
    beds = [level(r, "bed") for r in rows]
    tops = [level(r, "top", s) for r in rows for s in ("NE", "SW")]
    beds = [v for v in beds if v is not None]
    tops = [v for v in tops if v is not None]
    return (min(beds) if beds else None), (max(tops) if tops else None)


def _br_arch(tc, half, key_z, bed_z, n=16, half_v=None):
    """an opening: a round arch of half span `half` (m along the cut) with its keystone at key_z, open down to the
    bed: [(t, z)] (springing = key_z - half_v; half_v = the true half span when the face is seen at an angle and its
    spans look shorter along the cut)"""
    import math as _m
    hv = half if half_v is None else half_v
    sp = key_z - hv
    pts = [(tc - half, bed_z), (tc - half, sp)]
    pts += [(tc - half * _m.cos(_m.pi * i / n), sp + hv * _m.sin(_m.pi * i / n)) for i in range(1, n)]
    pts += [(tc + half, sp), (tc + half, bed_z)]
    return pts


def _br_pointed(tc, half, rise, bed_z, sp_z, n=10):
    """a pointed (two-centred) eye: half span `half`, crown `rise` over the springing sp_z"""
    import math as _m
    pts = [(tc - half, bed_z), (tc - half, sp_z)]
    for i in range(1, n):                                  # a simple ogival curve: sine-eased to the crown
        s = i / float(n)
        pts.append((tc - half + half * s, sp_z + rise * _m.sin(0.5 * _m.pi * s) ** 0.8))
    pts.append((tc, sp_z + rise))
    for i in range(n - 1, 0, -1):
        s = i / float(n)
        pts.append((tc + half - half * s, sp_z + rise * _m.sin(0.5 * _m.pi * s) ** 0.8))
    pts += [(tc + half, sp_z), (tc + half, bed_z)]
    return pts


def _br_mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (0, 2, 4)]
    pb = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % int(round(pa[i] + (pb[i] - pa[i]) * t)) for i in range(3))


def br_section(cid, X=None, Y=None, look=1, t0=None, t1=None, ground=None, top=None, max_m=None, page=None,
               into=None, ends=None, bed=None):
    """the bridges of a section (see the module notes); ends as br_near (a cut that is not a LEVELS row then needs
    ground= or bed= and top=)"""
    X = X or (lambda t: t)
    Y = Y or (lambda z: z)
    a, u, f, L = _br_axis(cid, look, ends)
    try:
        bed0, top0 = _br_cut_levels(cid)
    except KeyError:
        bed0, top0 = None, None
    if bed is not None:
        bed0 = bed
    out = {"background": [], "structures": [], "found": []}
    seen = []
    for r in br_near(cid, look, max_m, t0, t1, ends):
        key, nm = r["key"], r["name"]
        if r["rel"] == "behind":
            seen.append(u"%s behind the viewer %.0f m (not seen)" % (nm, -r["d"]))
            continue
        bed = ground(r["t"]) if ground else bed0             # (the `bed` argument was taken into bed0 above)
        if bed is None:
            seen.append(u"%s not drawn: no bed level" % nm)
            continue
        if not ground:
            _br_flag(u"FLAG bridge bed: not surveyed at the bridges; the cut's own bed is used (%s)" % cid)
        B = BRIDGES[key]
        span = _br_deck_span(key, a, u)
        dl = br_fact(key, "deck_l_m")
        dw = br_fact(key, "deck_w_m")
        tc = 0.5 * (span[0] + span[1]) if span else r["t"]     # the survey deck's middle (over the water), else the point
        if r["rel"] == "cut":
            ext = span or ((tc - 0.5 * dw, tc + 0.5 * dw) if dw else None)
        else:                                             # a sourced length wins over the deck ring (which may be only
            ext = (tc - 0.5 * dl, tc + 0.5 * dl) if dl else span    # the part over the water)
        if ext is None:
            seen.append(u"%s not drawn: no deck outline in the survey layers and no sourced length" % nm)
            continue
        ta, tb = ext
        if t0 is not None:
            ta = max(ta, t0)
        if t1 is not None:
            tb = min(tb, t1)
        if tb - ta < 0.5:
            seen.append(u"%s outside the drawn span" % nm)
            continue
        if span is None:
            _br_flag(u"FLAG bridge %s: no survey deck ring found within %.0f m; its sourced length is centred on the "
                     u"bridge-list point" % (nm, BR_DECK_MATCH_M))
        # heights: sourced first, else the drawing rules (FLAG)
        kz = br_fact(key, "keystone_above_bed_m")
        pp = br_fact(key, "parapet_above_bed_m")
        if kz is not None:
            deck_z = bed + kz + BR_RULE["crown_m"]
            _br_flag(u"FLAG %s: masonry over the keystone %.2f m, side arches %.1f x the middle one, piers %.2f m: "
                     u"drawing rules (not sourced, A15)" % (nm, BR_RULE["crown_m"], BR_RULE["side_frac"],
                                                            BR_RULE["pier_m"]))
        elif pp is not None:
            lo, hi = pp
            deck_z = bed + 0.5 * (lo + hi)
            _br_flag(u"FLAG %s: parapet top %.2f m over the bed = the middle of the photo-scaled %.1f-%.1f m (IMG_5814); "
                     u"eye sizes drawing rules (not sourced)" % (nm, 0.5 * (lo + hi), lo, hi))
        else:
            tz = top if top is not None else top0
            if tz is None:
                seen.append(u"%s not drawn: no height source and no bank top" % nm)
                continue
            deck_z = tz
            _br_flag(u"FLAG %s: no height source; deck top drawn at the cut's bank top %+.2f (the road level), slab "
                     u"%.2f m (drawing rule)%s" % (nm, tz, BR_RULE["deck_t_m"],
                                                    u"; its openings are not drawn (no sizes)" if B.get("openings")
                                                    else u""))
        if r["rel"] == "cut":
            sh = _br_cut_shapes(key, ta, tb, bed, deck_z, X, Y)
            out["structures"] += sh
            seen.append(u"%s cut through (%.0f-%.0f m along the cut)" % (nm, ta, tb))
        else:
            fade = BR_RULE["fade_far"] * min(1.0, max(0.0, r["d"] / float(max_m or BR_NEAR_M)))
            sh = _br_elev_shapes(key, ta, tb, tc, bed, deck_z, X, Y, fade, span, dl)
            out["background"] += sh
            seen.append(u"%s %.0f m beyond the cut" % (nm, r["d"]))
        out["found"].append(dict(r, ta=ta, tb=tb, deck_z=round(deck_z, 2), bed=round(bed, 2)))
    line = u"bridge %s %s" % (cid, u"; ".join(seen) if seen else u"none")
    if page:
        line += u" (%s)" % page
    BR_LOG.append(line)
    if into is not None:
        into.add("background", out["background"])
        into.add("structures", out["structures"])
    return out


def _br_cut_shapes(key, ta, tb, bed, deck_z, X, Y):
    """the bridge cut along its width (the cut line runs along the stream through it): solid masonry from the
    opening's crown up to the deck top for an arched bridge with a sourced keystone, else the deck slab"""
    kz = br_fact(key, "keystone_above_bed_m")
    if kz is not None:
        z0 = bed + kz                                     # the cut passes the middle arch: void up to the keystone
        col = BR_COL["stone"]
    else:
        z0 = deck_z - BR_RULE["deck_t_m"]
        col = BR_COL["stone"] if BRIDGES[key].get("form") == "arches" else BR_COL["deck"]
    ring = [(X(ta), Y(z0)), (X(tb), Y(z0)), (X(tb), Y(deck_z)), (X(ta), Y(deck_z))]
    return [("poly", ring, col, BR_COL["line"], 0.25)]


def _br_elev_shapes(key, ta, tb, tc, bed, deck_z, X, Y, fade, span, dl):
    """the bridge in elevation beyond the cut plane: its face from the bed to the deck top over ta..tb with the
    openings the sources name (sizes per the module notes), one flat stone tone faded with distance"""
    B = BRIDGES[key]
    fill = _br_mix(BR_COL["stone"] if B.get("form") == "arches" else BR_COL["deck"], BR_COL["paper"], fade)
    ink = _br_mix(BR_COL["line"], BR_COL["paper"], fade)
    holes = []
    c = 1.0                                               # the cuts that see a bridge in elevation run nearly parallel
    if key == "K5" or (B.get("eyes") and br_fact(key, "mid_span_m")):
        ms, kz = br_fact(key, "mid_span_m"), br_fact(key, "keystone_above_bed_m")
        sf, pm = BR_RULE["side_frac"], BR_RULE["pier_m"]
        half = 0.5 * ms
        off = half + pm + 0.5 * ms * sf
        for dt, hh, kk in ((-off, half * sf, kz * sf), (0.0, half, kz), (off, half * sf, kz * sf)):
            pts = _br_arch(tc + dt * c, hh * c, bed + kk, bed - 0.5, half_v=hh)
            if pts[0][0] > ta and pts[-1][0] < tb:
                holes.append([(X(t), Y(z)) for t, z in pts])
    elif key == "K4":
        w = tb - ta
        clear = w - 2.0 * BR_RULE["pier_m"]
        if clear > 4.0:
            hb = 0.5 * clear * BR_RULE["k4_big_frac"]
            hs = 0.5 * clear * (1.0 - BR_RULE["k4_big_frac"]) - 0.5 * BR_RULE["pier_m"]
            cb = ta + BR_RULE["pier_m"] + hb
            cs = tb - BR_RULE["pier_m"] - hs
            kb = min(deck_z - BR_RULE["crown_m"], bed + 2.0 * hb)
            holes.append([(X(t), Y(z)) for t, z in _br_arch(cb, hb, kb, bed - 0.5)])
            if hs > 0.8:
                sp = bed + max(0.0, kb - bed - hb)
                rise = min(hs * BR_RULE["k4_small_rise"], deck_z - BR_RULE["crown_m"] - sp)
                holes.append([(X(t), Y(z)) for t, z in _br_pointed(cs, hs, rise, bed - 0.5, sp)])
    body = [(X(ta), Y(bed - 0.5)), (X(tb), Y(bed - 0.5)), (X(tb), Y(deck_z)), (X(ta), Y(deck_z))]
    if not holes:                                         # no opening is sourced (K1-K3, K6): the deck slab only,
        body = [(X(ta), Y(deck_z - BR_RULE["deck_t_m"])), (X(tb), Y(deck_z - BR_RULE["deck_t_m"])),   # never a
                (X(tb), Y(deck_z)), (X(ta), Y(deck_z))]                                              # solid wall
        return [("poly", body, fill, ink, 0.12)]
    return [("poly", body, fill, ink, 0.12, None, holes)]


def br_log_lines():
    """the bridge lines (`bridge <cid> <name|none>`) and FLAG lines of this run, each once"""
    out = []
    for ln in BR_LOG + BR_FLAGS:
        if ln not in out:
            out.append(ln)
    return out
