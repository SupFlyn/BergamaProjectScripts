# ---- 20_scale (composer core, round 5 S1; round 7 v33: no scale list, no picking): drawing -> page mm ---------------
#   sc_size(D, den_or_f) -> (w_mm, h_mm)       the printed size of a drawing's extent
#   v33 (round 7, BRIEF L1/L3): the scale ladder (BK_SCALES, BK_MM_MAX) and every picker (sc_pick, sc_pick_common,
#   sc_factor, sc_inset_den, _sc_allowed) are DELETED: a drawing's scale is read from the page table (82_compose
#   _bk_den), never chosen here.
#   BkT(D, s, x, y)                              the drawing's transform onto the page: s = den ("m") or f ("mm");
#                                               (x, y) = the page mm (y DOWN) of the extent's top-left corner;
#                                               .k (page mm per drawing unit), .pt(x, y), .rect, .den (None for "mm")
def _sc_ext(D):
    e = D["extent"]
    return float(e[2]) - float(e[0]), float(e[3]) - float(e[1])


def sc_size(D, s):
    ew, eh = _sc_ext(D)
    k = (1000.0 / float(s)) if D.get("units", "m") == "m" else float(s)
    return ew * k, eh * k


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
