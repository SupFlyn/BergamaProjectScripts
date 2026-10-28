# ---- MIRAQUA round 28 Oct 2026: pieces every site-board map of the round shares (revision_2026-10-28/PLAN.md) ----
# G8: the study area = layer calisma_alan (two closed parts, worked as ONE area), drawn on every map in one line style
# (R28_STUDY_LINE, common/r28_style.py) with one legend name (R28_STUDY_NAME). Read only, like STUDY_LAYERS (which
# still only places C5 and the photo areas). The rectangle site_alan stays the analysis frame (the strip's edge).
R28_STUDY_LAYER = "calisma_alan"
R28_STUDY_RAW = {}                                   # what read_rhino found on calisma_alan (set by the main block)
R28_STUDY_GAP = 5.0                                  # m: an outline whose ends are closer than this counts as closed
R28_STUDY_COPY = [                                   # calisma_alan of Bergama_Altlik.3dm (25 Oct 08:25), survey m, as the masterplan's CALISMA_COPY
    [(29696.903, 32800.562), (29872.423, 32572.84), (29880.693, 32496.334), (29818.865, 32475.301), (29825.821, 32398.074), (29923.185, 32344.348), (29904.985, 32311.252), (29997.056, 32290.092), (30053.417, 32139.667), (30004.049, 32108.006), (29954.803, 32210.611), (29792.114, 32247.062), (29761.684, 32302.735), (29754.016, 32451.383), (29678.437, 32447.696), (29632.398, 32496.591), (29665.339, 32526.253), (29612.859, 32696.506), (29600.496, 32719.394)],
    [(30178.18, 31923.887), (30138.072, 31887.655), (30257.694, 31773.217), (30389.686, 31405.252), (30701.152, 30991.252), (30840.053, 31053.865), (31044.852, 30781.877), (31014.2, 30757.409), (31373.442, 30493.066), (31453.175, 30560.194), (31332.978, 30864.179), (31012.679, 31323.349), (30737.856, 31286.66), (30712.87, 31331.891), (30556.09, 31450.103), (30454.629, 31577.301), (30434.156, 31607.332), (30313.613, 31812.92)],
]
R28_STUDY_LEG = ("study", C(R28_STUDY_LINE["colour"]), R28_STUDY_NAME)   # the legend row (draw_symbol / crop_legend kind "study")


def r28_study_from(R, I):
    """the study area's outlines in survey m, the two largest closed parts, north first: from R (read_rhino on
    calisma_alan, file coordinates; I = file -> survey), else the recorded copy"""
    found, src = [], "layer calisma_alan"
    for P in (R.get("plines") or {}).get(R28_STUDY_LAYER, []):
        pts = [T_apply(I, p[0], p[1]) for p in P]
        if len(pts) < 4:
            continue
        gap = math.hypot(pts[0][0] - pts[-1][0], pts[0][1] - pts[-1][1])
        if gap > R28_STUDY_GAP:
            LOG.append("WARNING: a curve on calisma_alan is open ({:.1f} m gap), so it is not drawn.".format(gap))
            continue
        found.append(pts[:-1] if gap < 1e-6 else pts)
    if not found:
        found, src = [list(P) for P in R28_STUDY_COPY], "the recorded copy (Bergama_Altlik.3dm, 25 Oct)"
    found = sorted(found, key=lambda P: -abs(shoelace(P)[0]))[:2]
    found.sort(key=lambda P: -max(p[1] for p in P))
    LOG.append(u"Study area (calisma_alan) from {}: {} ({:,.2f} ha in all).".format(
        src, " + ".join("{:,.2f} ha".format(abs(shoelace(P)[0]) / 1e4) for P in found),
        sum(abs(shoelace(P)[0]) for P in found) / 1e4))
    return found


def r28_pattern(P, pat, limit=20000):
    """the 'on' pieces of the repeating on/off lengths pat (P's units) along the polyline P, in one pass"""
    out, cur, i, left = [], None, 0, pat[0]
    for a, b in zip(P, P[1:]):
        l = math.hypot(b[0] - a[0], b[1] - a[1])
        t = 0.0
        while l - t > 1e-12:
            st = min(left, l - t)
            if i % 2 == 0:
                if cur is None:
                    cur = [(a[0] + (b[0] - a[0]) * t / l, a[1] + (b[1] - a[1]) * t / l)]
                cur.append((a[0] + (b[0] - a[0]) * (t + st) / l, a[1] + (b[1] - a[1]) * (t + st) / l))
            t += st
            left -= st
            if left <= 1e-12:
                if cur is not None and len(cur) > 1:
                    out.append(cur)
                cur, i = None, i + 1
                left = pat[i % len(pat)]
                if len(out) >= limit:
                    return out
    if cur is not None and len(cur) > 1:
        out.append(cur)
    return out


def draw_r28_study(S, CB, V, k, L, order=38):
    """G8: the study area's outline on a booklet map (CB = the map's ClipB or Board, V its View, k = board units per
    booklet mm): dash-dot, R28_STUDY_LINE, printing at its mm sizes on the booklet page"""
    st = R28_STUDY_LINE
    col = C(st["colour"])
    for P in getattr(S, "r28_study", None) or []:
        for d in r28_pattern(V.P(P + [P[0]]), [m * k for m in st["dash_mm"]]):
            CB.line(d, col, L, order, bk_lw(st["width_mm"], k))
