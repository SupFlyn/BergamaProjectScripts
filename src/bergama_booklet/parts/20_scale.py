# ---- 20_scale (composer core, round 5 S1; G-R5-12, D2, PLAN §3 "Scales"): ONE scale list, drawing -> page mm ---------
# The Bergama list is section_frame's SF_SCALES (PLAN §3; the booklet's own STD_SCALES with 25,000-100,000 is retired),
# insets SF_INSET_SCALES (adds 1:100) at >= 2 x the parent's scale. The values are taken from section_frame.py when it
# is included, else these (the same numbers).
#   sc_size(D, den_or_f) -> (w_mm, h_mm)       the printed size of a drawing's extent
#   sc_pick(D, w, h, allowed=None, min_den=None, page=None) -> den
#         the LARGEST printed size (smallest 1:den) of D's allowed scales (its scale_pref within the list) at which
#         its extent fits w x h mm; none fits -> the smallest size on its list + WARNING "scale" (never a stop)
#   sc_pick_common(Ds, w, h, gap=4.0, stack=True, page=None) -> den
#         one scale for drawings stacked (stack=True: heights + gaps add up) or side by side (widths add up) in w x h
#         (merged pages D7, D9: four cuts at one scale, N3 = 1:500)
#   sc_factor(D, w, h, page=None) -> f          a "mm" drawing (diagram, chart, key map): the largest factor in its
#                                               fit range at which it fits; below the range -> fits anyway + WARNING
#   sc_inset_den(parent_den, D, w, h, page=None) -> den   an inset's scale: >= 2 x the parent (SF_INSET_MIN_ZOOM)
#   BkT(D, s, x, y)                              the drawing's transform onto the page: s = den ("m") or f ("mm");
#                                               (x, y) = the page mm (y DOWN) of the extent's top-left corner;
#                                               .k (page mm per drawing unit), .pt(x, y), .rect, .den (None for "mm")
# v30.3 (Aras 2 Nov 06:20, decision card): the booklet's own round list adds 1:1,500, 1:7,500, 1:15,000 (and 1:25,000
# for the whole-survey plans that overran A3 at 1:20,000), so a map no longer halves in size between two list steps.
# Only maps and sections take a list scale and print it; diagrams, charts and the axo take any size (Aras 06:24
# "diagrams can be at different scales ... dont write scales to diagrams, just maps").
BK_SCALES = (200, 250, 500, 1000, 1500, 2000, 2500, 5000, 7500, 10000, 15000, 20000, 25000)
BK_INSET_SCALES = (100,) + BK_SCALES
BK_MM_MAX = 6.0            # v30.3: a scale-free drawing may grow to 6 x its exported size (was 2 x), room permitting
BK_INSET_ZOOM = 2.0


def _sc_ext(D):
    e = D["extent"]
    return float(e[2]) - float(e[0]), float(e[3]) - float(e[1])


def sc_size(D, s):
    ew, eh = _sc_ext(D)
    k = (1000.0 / float(s)) if D.get("units", "m") == "m" else float(s)
    return ew * k, eh * k


def _sc_allowed(D, allowed=None, inset=False):
    lst = BK_INSET_SCALES if inset else BK_SCALES
    want = allowed or D.get("scale_pref") or lst
    want = [int(v) for v in want]
    if not allowed and want:                 # v30.3: a script's scale_pref is a RANGE on the booklet's list, so the
        lo, hi = min(want), max(want)        # in-between round scales are open to it; 1:20,000 maps may go 1:25,000
        if hi >= 20000:
            hi = max(lst)
        out = sorted(v for v in lst if lo <= v <= hi)
    else:
        out = sorted(v for v in want if v in lst)
    return out or list(lst)


def sc_pick(D, w, h, allowed=None, min_den=None, page=None):
    al = _sc_allowed(D, allowed)
    for den in al:
        if min_den and den < min_den:
            continue
        dw, dh = sc_size(D, den)
        if dw <= w + 1e-6 and dh <= h + 1e-6:
            return den
    den = al[-1]
    dw, dh = sc_size(D, den)
    wn_warn(page or D.get("page"), "scale", u"%s does not fit %.0f x %.0f mm at any of 1:%s; set at 1:%d (%.0f x %.0f mm)"
            % (D.get("id"), w, h, u", 1:".join(str(v) for v in al), den, dw, dh))
    return den


def sc_pick_common(Ds, w, h, gap=4.0, stack=True, page=None):
    al = sorted(set.intersection(*[set(_sc_allowed(D)) for D in Ds])) if Ds else list(BK_SCALES)
    al = al or list(BK_SCALES)
    for den in al:
        sz = [sc_size(D, den) for D in Ds]
        if stack:
            ok = max(s[0] for s in sz) <= w + 1e-6 and sum(s[1] for s in sz) + gap * (len(sz) - 1) <= h + 1e-6
        else:
            ok = max(s[1] for s in sz) <= h + 1e-6 and sum(s[0] for s in sz) + gap * (len(sz) - 1) <= w + 1e-6
        if ok:
            return den
    wn_warn(page, "scale", u"%s do not fit %.0f x %.0f mm together at any common scale; set at 1:%d" % (
        u", ".join(D.get("id", u"?") for D in Ds), w, h, al[-1]))
    return al[-1]


def sc_factor(D, w, h, page=None, hi_max=None):
    ew, eh = _sc_ext(D)
    f = min(w / ew, h / eh)
    lo, hi = (D.get("fit") or (0.5, 2.0))[:2]
    hi = max(float(hi), BK_MM_MAX if hi_max is None else float(hi_max))
    if f > hi:
        return float(hi)
    if f < lo:
        wn_warn(page or D.get("page"), "scale", u"%s needs x%.2f to fit %.0f x %.0f mm, below its x%.2f minimum" % (
            D.get("id"), f, w, h, lo))
    return f


def sc_inset_den(parent_den, D, w, h, page=None):
    al = [d for d in _sc_allowed(D, inset=True) if d * BK_INSET_ZOOM <= parent_den + 1e-6]
    if not al:
        wn_warn(page or D.get("page"), "scale", u"inset %s: no scale >= %.0f x the parent's 1:%d" % (
            D.get("id"), BK_INSET_ZOOM, parent_den))
        al = [min(BK_INSET_SCALES)]
    for den in al:
        dw, dh = sc_size(D, den)
        if dw <= w + 1e-6 and dh <= h + 1e-6:
            return den
    wn_warn(page or D.get("page"), "scale", u"inset %s does not fit %.0f x %.0f mm at any inset scale >= 2 x 1:%d; "
            u"set at 1:%d" % (D.get("id"), w, h, parent_den, al[-1]))
    return al[-1]


class BkT(object):
    """drawing units (y up) -> page mm (y down); see the part notes"""
    def __init__(self, D, s, x, y):
        self.D = D
        self.e = [float(v) for v in D["extent"]]
        self.den = int(s) if D.get("units", "m") == "m" else None
        self.k = (1000.0 / float(s)) if self.den else float(s)
        self.x, self.y = float(x), float(y)
        self.w, self.h = (self.e[2] - self.e[0]) * self.k, (self.e[3] - self.e[1]) * self.k
        self.rect = (self.x, self.y, self.x + self.w, self.y + self.h)

    def pt(self, x, y):
        return self.x + (float(x) - self.e[0]) * self.k, self.y + (self.e[3] - float(y)) * self.k

    def ry(self, y):
        return self.y + (self.e[3] - float(y)) * self.k
