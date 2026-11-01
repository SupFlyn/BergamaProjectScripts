# ---- block.py (round 4, S1, 1 Nov 2026; G-R4-3, PLAN §4.2): ONE section block template (U25 / U27) ---------------------
# A section block = title strip on top + the drawing + its text, laid out on the booklet grid (grid.py: baseline
# GRID_BASE = 4 mm, gutter GRID_GUT = 4 mm, column GRID_COL = 29 mm). No fixed ratios (U27): the caller gives the
# block's box, the template only splits it. Page mm; y_down=False mirrors it for y-up sheets.
#   blk_section(x0, y0, w, h, title, side_w=None, mode="LEFT", why=None, strip_h=None, y_down=True)
#       -> dict(title=box, title_base=(x, y), drawing=box, side=box or None, strip=box or None, mode=mode, title_text)
#   (x0, y0) = the block's visual top-left corner; boxes are (x0, y0, x1, y1)
#   LEFT  (default, U25 left): the title strip on top (one line, heading style, flush with the block's left edge), the
#         drawing below it, a narrow text column on its right sharing the drawing's top and bottom edges (side_w,
#         default one grid column), nothing below. The text column holds the keywords and the numbered list in
#         reading order (G-R4-5.5).
#   RIGHT (wide, short cuts only): the title, the drawing over the full width, a thin strip under it of the same
#         width (strip_h, default 3 baselines = 12 mm). `why` must say why this cut takes RIGHT (the build says why).
#   Title: GRID_TYPE["heading"] (10 pt bold); its baseline sits one baseline (4 mm) below the block's top, and the
#   drawing starts two baselines (8 mm) below it, so drawings and titles stay on the baseline grid.
BLK_TITLE_BASE = 4.0               # mm from the block's top to the title's baseline (one GRID_BASE)
BLK_TITLE_H = 8.0                  # mm from the block's top to the drawing's top (two GRID_BASE)
BLK_STRIP_H = 12.0                 # mm, RIGHT mode's strip under the drawing (three GRID_BASE)


def blk_section(x0, y0, w, h, title, side_w=None, mode="LEFT", why=None, strip_h=None, y_down=True):
    """the boxes of one section block (see the module notes)"""
    mode = str(mode or "LEFT").upper()
    if mode not in ("LEFT", "RIGHT"):
        raise ValueError("blk_section mode %r: LEFT or RIGHT" % mode)
    if mode == "RIGHT" and not (why and str(why).strip()):
        raise ValueError("blk_section %r: RIGHT mode needs `why` (the build says why this cut is not LEFT)" % title)
    gut = GRID_GUT
    sw = float(GRID_COL if side_w is None else side_w)
    st = float(BLK_STRIP_H if strip_h is None else strip_h)
    # visual offsets from the top (t) inside the block, turned into page y at the end
    Y = (lambda t: y0 + t) if y_down else (lambda t: y0 - t)

    def box(xa, ta, xb, tb):
        a, b = Y(ta), Y(tb)
        return (xa, min(a, b), xb, max(a, b))
    x1 = x0 + w
    if mode == "LEFT":
        dx1 = x1 - sw - gut
        if dx1 - x0 < 2 * GRID_COL:
            raise ValueError("blk_section %r: %.1f mm is too narrow for a drawing beside a %.1f mm column" % (
                title, w, sw))
        out = dict(drawing=box(x0, BLK_TITLE_H, dx1, h), side=box(dx1 + gut, BLK_TITLE_H, x1, h), strip=None)
    else:
        if h - BLK_TITLE_H - st - gut < GRID_BASE:
            raise ValueError("blk_section %r: %.1f mm is too low for a drawing over a %.1f mm strip" % (title, h, st))
        out = dict(drawing=box(x0, BLK_TITLE_H, x1, h - st - gut), side=None, strip=box(x0, h - st, x1, h))
    d = out["drawing"]
    out.update(title=box(x0, 0.0, d[2], BLK_TITLE_H - GRID_BASE / 2.0), title_base=(x0, Y(BLK_TITLE_BASE)),
               mode=mode, title_text=title, why=why)
    return out
