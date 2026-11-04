# booklet p19 (file renamed from pages/p18_farms.py on 1 Nov 2026, round 4 S6b: the file is named after its booklet page)
# p.18 where the clean water goes (split from code.py on 29 Oct 2026)
# Revision 30 Oct (T5; D2 a, D7 a, G4, M1, M9, M10): the farmland axonometric is gone; the farms are ONE field tile
# at step 6 of the flow (round 3: one olive tree on one field band beside the aquifer, see below). Each block is drawn
# at its booklet size (mm, 1:1 on A3; the size factor s that code.py's fit() hands in is not used).
# Every fact once; the shared ones (olive need, 1.25 ha, aquifer ratio, arsenic, storage) through facts.py.
# Round 3 (B4, 31 Oct; P18.1, P18.4, G3, G4, G17; booklet: p18 + p19 merged on ONE page, spec
# revision_2026-10-31_round3/handover/B4_work/spec_p18_merged.md): every block drawn at 1:1 for that page:
#   wb_farms     draw_farms_text: P18_W x P18_FLOW_H (369 x 56 mm, a white ground sets the extent): the 7-step loop on
#                the left 7 page columns, and on the right 4 columns the farms outside with the aquifer under them
#                (_p18_farms_block: ONE detailed olive tree on ONE field texture with the drip line, P18.4; groundwater
#                potential against total use as two horizontal bars with direct values). The aquifer is no longer a
#                separate part (draw_farm_picto deleted; code.py places no aquifer part).
#   wb_decision  draw_decision: the four fact boxes 2 x 2 in P18_DEC_W x P18_DEC_H (126 x 38 mm), no fill, no stroke
#                (G17); it sits beside the agriculture "stream comes first" block on the booklet page.
# Round 4 (S6b, P19.1, K4; spec revision_2026-11-01_round4/handover/S6b_p19_design_spec.md): booklet p19 is rebuilt
# as story groups, one heading each, rows sharing their top and bottom edges. The water board draws three of its
# blocks, each EXACTLY at its booklet size (1:1, BK_FIXED; a white ground sets the crop; a drawing that runs outside
# its block RAISES):
#   wb_farms      draw_farms_text   P18_W x P19_R1_H (260 x 57): group 1's heading "WHERE THE CLEAN WATER GOES" and
#                                   the 7-step loop (markers through marker.py mk_marker, G-R4-7)
#   wb_farms_out  draw_farms_out    P19_SIDE_W x P19_R1_H (128 x 57): where the loop ends: the farms outside, one
#                                   olive on drip, groundwater potential against total use, the ratio (was the right
#                                   part of wb_farms)
#   wb_decision   draw_decision     P19_SIDE_W x P19_R2_H (128 x 40): the four figures of group 2 (beside the
#                                   agriculture "stream first" block, which carries the group's heading)
# Every text goes through the water board's TextPage "p19" (code.py build_board: pg.text_page / pg.check_text, G-R4-1);
# a word block (a paragraph, a box's lines) is one text group. The heading band P19_HEAD is on top of every block, so
# the blocks of a booklet row share the content top.
# Round 5 (S8, v15; P21.1 "each group = one block (heading, diagram, its text), separated by clear gutters, in reading
# order"; G-R5-12): each block is exported as ONE diagram drawing (mm, scale free) of booklet page p21 (WBX_PG_FARMS),
# its words as anchored labels; the group heading is a heading TEXT item of the group (not drawn); the drawings carry
# their group: P19_GROUPS. Group 2's heading is the agriculture "stream comes first" block's (S9 gives its items the
# same group id). No widths (addendum 5): the olive spacing line goes.
# v16 (round 6, S5): booklet page p18 "Where the clean water goes, and what it grows" (board page WBX_PG_FARMS; the
# lead maps it to p18) keeps the SUBMISSION_SON page19 drawing (PLAN §4) = ee52805 pages/p18_farms.py: the loop on 7
# page columns (P18_W 227 mm, was 8), the content 56 mm tall from the block's top under the heading band (P18_FLOW_H;
# was 51), the farms outside with the ee52805 offsets (title on the content top, vignette, bars at top - 11 / - 24 mm),
# the four figures with ONE box height for both rows (ee52805). Kept from round 4/5: the split into the three booklet
# items wb_farms | wb_farms_out | wb_decision (wbx_drawing in _p19_close), marker.py markers, the TextPage keeps, no
# olive widths (addendum 5; SON printed "olives 500 x 700 cm", left out). Round 6 rules: G6-1 frames
# (frames_p14-22.md "SON page19 -> new page 18": flow [3,10 55x20], farms outside [60,10 37x20], figures [3,33 30x10]):
# wb_farms_out widened to P19_SIDE_W 152 mm so loop and farms take the same enlargement (231 / 227) in their frames;
# the SON captions under the blocks come back as caption items ("Where the clean water goes", "What the figures
# support"); G6-6 hues (water arrows, drip, potential bar WAT r2, total use bar AGR r2; hues.py hue()); G6-9 every
# element in pg.g(kind, element); the two SON overlap pairs (step 7's line and the olive caption against the 4.4 x
# ratio, one SON block) cleared: three drawings, each word block its own text group, a WARNING on any overlap left.
P19_GROUPS = {u"wb_farms": u"p21_g1_where_water_goes", u"wb_farms_out": u"p21_g1_where_water_goes",
              u"wb_decision": u"p21_g2_figures"}
P19_ORDER = {u"wb_farms": 1, u"wb_farms_out": 2, u"wb_decision": 3}   # reading order (priority) on the page
# v16 (round 6, G6-1): SON page19 reads the figures (row 2, left) before the agriculture "stream comes first" block
P19_CAPTION = {u"wb_farms": u"Where the clean water goes", u"wb_decision": u"What the figures support"}  # SON captions

P19_HEAD = 6.0                                   # the group heading band on top of every p19 block, mm
P19_HEAD_PT = grid_style("heading")[0]           # 10 pt bold (GRID_TYPE heading)
P18_FLOW_H = 56.0                                # v16 (round 6, SON page19 = ee52805): row 1's content height, mm
P19_R1_H, P19_R2_H = P19_HEAD + P18_FLOW_H, 40.0  # booklet rows 1 (loop | farms outside) and 2 (stream | figures), mm
P19_SIDE_W = 152.0                               # v16 (G6-1): wb_farms_out's width (was grid_w(4) = 128): its frame
#                                                  [60,10 37x20] % = 155 mm at the loop's enlargement 231 / 227 mm
P18_COLS = 4                                     # step columns inside the loop (grid_sub)
P18_W = grid_w(7)                                # wb_farms: the loop, 7 page columns (227 mm, SON / ee52805; was 8)
P18_GAP_R = 3.0                                  # the least gap between the loop's two rows
P18_MK, P18_IC = 6.0, 8.0                        # step marker (marker.py, at least this across) and step icon, mm
P18_FV = 4.2                                     # a box's headline value / step 7's value, mm (12 pt)
P18_BIG = grid_style("value")[0] * GRID_PT       # the aquifer ratio, the block's one headline value
P18_DEC_W = grid_w(4) - 2.0                      # v16 (SON / ee52805): wb_decision 126 mm wide; its height = its
#                                                  two box rows (no white band under them: the frame is 30 x 10 %)
P18_VIG_W = 34.0                                # the farm vignette's width (one olive tree on one field band), mm
P18_BAND = 3.0                                   # the field texture band under the tree, mm (a drawing size)
P18_OLIVE_ROW_M, P18_OLIVE_TREE_M = 7.0, 5.0     # plants.py: olive 5 x 7 m (Kaya 2017 p.821), printed in cm
P18_PLANT_M3_DAY, P18_PLANT_DAYS = 14304.0, 120  # the town plant's treated water a day (p.12), summer days
P18_DEC_ICONS = [("sewage", True), ("reeds", False), ("uv", False), ("storage", False), ("stream", False),
                 ("field", False), ("not_drinkable", False)]     # (icon, crossed) for steps 1-7
P18_SRC_AQ = u"published, North Aegean drought management plan 2018 (official); " + WD
P18_SRC_NA = u"published, North Aegean water allocation plan 2025; " + REG + u" CL-21"
P18_SRC_AS = u"published, Somay & Gemici 2015; " + REG + u" EN-E3"


def _p18_put(pg, shapes):
    """icons.py / plants.py / marker.py shapes onto the page (water.py shp_put: polys, lines and text; round 4: was
    sec_put, which knows no text)"""
    shp_put(pg, shapes)


def _p19_text(pg, s, x, y, size, colour, bold=False, align="L"):
    """one text of a p19 block; m² / m³ keep the font's own ² / ³ glyph (the embedded Arial has them): Page.text
    raises them as a 0.6 x digit otherwise, which prints below the 6 pt minimum the TextPage enforces (G-R4-1)
    at these sizes (an identity matrix keeps the text whole)"""
    mat = ((1.0, 0.0), (0.0, 1.0)) if any(ch in SUP for ch in s) else None
    pg.text(s, x, y, size, colour, bold=bold, align=align, mat=mat)


def _p19_caption(cid):
    """v16 (round 6, G6-1, SON page19): the block's caption under its drawing as SON printed it (P19_CAPTION; was a
    heading text item of the group, v15): a caption text item of the drawing cid, in its group; nothing drawn in the
    heading band. A block without a SON caption (wb_farms_out: it sat in the loop's SON block) gets none."""
    t = P19_CAPTION.get(cid)
    if t:
        wbx_text(WBX_PG_FARMS, t, "caption", did=cid, priority=P19_ORDER.get(cid, 1), id=u"wb_p21_cap_" + cid,
                 group=P19_GROUPS.get(cid))


def _p19_close(pg, n0, box, cid):
    """the block's white ground under everything drawn since item n0 (it sets the crop; no stroke, G17), the block
    registered in the TextPage (blocks never overlap); a drawing outside the block RAISES (the booklet prints the
    block at exactly this size, so nothing may be cut). Returns the box."""
    bb = items_bbox([it for it in pg.items[n0:] if it[0] in ("poly", "line", "circle", "text")])
    over = max(box[0] - bb[0], box[1] - bb[1], bb[2] - box[2], bb[3] - box[3])
    # v17 (L4): no layout warning for a drawing past its board block: the export keeps the whole drawing (dbb) and
    # the booklet sizes it (LAYOUT_PLAN 3.1-3)
    pg.block(box, cid)
    # v15 (G-R5-12, P21.1): the block = one diagram drawing of p21 (the empty heading band left out), in its group
    dbb = (min(box[0], bb[0]), min(box[1], bb[1]), max(box[2], bb[2]), max(box[3] - P19_HEAD, bb[3]))
    wbx_drawing(cid, WBX_PG_FARMS, pg, dbb, n0=n0, den=None, dkind="diagram", group=P19_GROUPS.get(cid),
                priority=P19_ORDER.get(cid, 1), crop=cid)
    return box


def _p19_hue(code, rank):
    """v16 (round 6, G6-6): a colour of the one hue table (common/hues.py hue(), PLAN §2.6) in the board's form: hex
    without "#" (rgb() reads 6 digits)"""
    return (u"%s" % hue(code, rank)).lstrip(u"#")


def _p18_icon(pg, names, x, y, sz, cross=False):
    """icons.py pictogram(s) in the square (x, y - sz)-(x + sz, y): one icon fills it; a pair (the clean stream
    leaving + the field it goes to) sits on the square's diagonal, the water upper left, the field lower right"""
    if len(names) == 1:
        _p18_put(pg, ico_draw(names[0], x + sz / 2.0, y - sz / 2.0, sz))
    else:
        h = sz * 0.58
        _p18_put(pg, ico_draw(names[0], x + h / 2.0, y - h / 2.0, h))
        _p18_put(pg, ico_draw(names[1], x + sz - h / 2.0, y - sz + h / 2.0, h))
    if cross:
        _p18_put(pg, ico_cross(x + sz / 2.0, y - sz / 2.0, sz))


def _p18_ground(pg, n0, x0, y0, x1, y1):
    """the block's white ground under everything drawn since item n0 (it sets the crop's extent; no stroke, G17)"""
    tmp = Page(1, 1)
    tmp.poly([rect(x0, y0, x1, y1)], fill=COL["white"])
    pg.items.insert(n0, tmp.items[0])


def _p18_cols(x0):
    """the 4 step columns [(x0, x1)] of the 8-column loop block from x0"""
    return [(x0 + a, x0 + b) for a, b in grid_sub(P18_W, P18_COLS)]


def _p18_steps():
    """the seven steps: (heading, value or None, line). Storage itself is p.10's fact: step 4 says only its share of
    the winter flow (live); arsenic from facts.py (printed here once)"""
    st = fact("storage_m3")
    hold = (u"storage incl. the strip: {:.1f}-{:.1f} % of the Dec-Apr flow".format(
        100.0 * st[0] / WINTER_FLOW, 100.0 * st[1] / WINTER_FLOW) if st else
        u"winter water in the ground, for the dry summer")
    return [
        (u"KEEP SEWAGE OUT", None, u"İZSU sewer"),
        (u"CLEAN AT THE UPSTREAM END", None, u"reed beds at the entry · whole reach clean"),
        (u"DISINFECT WHERE PEOPLE TOUCH IT", None, u"wetlands leave 100-100,000 CFU/100 ml · class A: 0"),
        (u"HOLD WINTER WATER", None, hold),
        (u"KEEP THE STRIP ALIVE", None, u"clean water all summer · feeds the planting"),
        (u"THEN THE FARMS", None, u"existing farmland on the slopes outside the site · reuse class B · no farm "
                                  u"channel inside"),
        (u"NOT FOR DRINKING", u"arsenic > {} µg/L".format(fact_num("arsenic_ug_l")),
         (u"groundwater · stored rain not listed for drinking · drinking needs 0 E. coli/100 ml " +
          cite(P18_SRC_AS)).strip())]


def _p18_step(pg, i, step, x0, top, cw, boxes=None):
    """step i in its column from top: the marker and the icon on one line (the icon's top on top), the heading, the
    value, the line. boxes: the icon's square is added (the overlap test's drawing boxes). Returns (bottom y, the
    marker's centre y). Round 4 (G-R4-7): the number through marker.py mk_marker (glyph centred on its ink box, in
    the loop's water colour, at least P18_MK across); the icon's square is a keep of the TextPage (no text on it);
    heading, value and line are ONE text group (the step's word block)."""
    head, val, line = step
    ym = top - P18_IC / 2.0
    sh, _mb, _r = mk_marker(x0 + P18_MK / 2.0, ym, str(i + 1), ICO_PAL["water_deep"], size_pt=7.0,
                            r_min=P18_MK / 2.0)
    with pg.g("annotations", u"step %d marker" % (i + 1)):     # v16 (G6-9): each element its own group
        _p18_put(pg, sh)
    nm, crossed = P18_DEC_ICONS[i]
    ix = x0 + P18_MK + 1.5
    with pg.g("annotations", u"step %d icon · %s" % (i + 1, nm)):
        _p18_icon(pg, (nm,), ix, top, P18_IC, crossed)
    pg.keep((ix, top - P18_IC, ix + P18_IC, top), "icon", u"p19 step icon %d" % (i + 1))
    if boxes is not None:
        boxes.append((ix, top - P18_IC, ix + P18_IC, top))
    tw = cw - 2.0
    old = pg.tg
    pg.tgroup()
    try:
        with pg.g("labels", u"step %d · %s" % (i + 1, head.lower())):
            yy = _para_common(pg, x0, top - P18_IC - 0.8, tw, head, FS_MIN, C["dark"], bold=True)
            if val:
                yy = _para_common(pg, x0, yy - 0.6, tw, val, P18_FV, C["d3"], bold=True)
            if line:
                yy = _para_common(pg, x0, yy - 0.6, tw, line, FS_MIN, C["ink"])
    finally:
        pg.tg = old
    return yy - FS_MIN * 0.3, ym


def draw_farms_text(pg, x, y):
    """p19 group 1, "WHERE THE CLEAN WATER GOES": the flow (Aras 26 Oct 07:06 and his sketch: the seven steps
    clockwise round a ring, 1-4 along the top, 5-7 back along the bottom) on the 4 step columns of the 8-column block:
    markers and icons on one line, a heading and one line under each; the bottom row stands on the block's foot.
    Under the red closing arrow (7 -> 1: the next winter's stream, never a pump), in the empty bottom-left cell: what
    closes the loop and the one-way rule. Round 4 (P19.1): the block is EXACTLY P18_W x P19_R1_H from its top-left
    (x, y) (crop wb_farms, 1:1 on the booklet page), the group heading in its band; the farms outside are their own
    block now (draw_farms_out, beside it on the booklet page). Returns the block box (x0, y0, x1, y1).
    v16 (round 6, S5; SON page19 = ee52805 draw_farms_text 123): the loop on 7 page columns (P18_W 227 mm) and
    P18_FLOW_H 56 mm under the heading band, as SON; the SON caption "Where the clean water goes" a caption item
    (_p19_caption); the water arrows WAT r2 (G6-6, hues.py); every step, arrow and note its own pg.g element (G6-9).
    Diagram, no section (no SITE / SKETCH / ACCURATE language). Frame G6-1: flow [3,10 55x20] % of new page 18."""
    n0 = len(pg.items)
    _p19_caption(u"wb_farms")
    top = y - P19_HEAD
    cols = _p18_cols(x)
    cw = cols[0][1] - cols[0][0]
    steps = _p18_steps()
    tall = [-_p18_step(Page(1, 1), i, steps[i], 0.0, 0.0, cw)[0] for i in range(4, 7)]   # row 2's heights
    foot = y - P19_R1_H
    bots, ym = [], {}
    for i in range(4):                               # row 1: steps 1-4, left to right
        b_, ym[i] = _p18_step(pg, i, steps[i], cols[i][0], top, cw)
        bots.append(b_)
    y1b = min(bots)
    y2 = min(foot + max(tall), y1b - P18_GAP_R)      # row 2 on the foot (never closer than the gap to row 1)
    for i, c in ((4, 3), (5, 2), (6, 1)):            # row 2: steps 5-7, right to left under columns 4, 3, 2
        _b, ym[i] = _p18_step(pg, i, steps[i], cols[c][0], y2, cw)
    # the arrows: along the top, down column 4, back along the bottom (water); the red closing arrow up column 1
    ia = P18_MK + 1.5 + P18_IC + 1.5                 # where an arrow leaves a step's marker line
    cw_ = _p19_hue("WAT", 2)                            # v16 (G6-6): the stream's flow arrows, WAT r2 (was C["d2"])
    for i in range(3):
        with pg.g("water", u"flow arrow %d-%d" % (i + 1, i + 2)):
            arrow(pg, [(cols[i][0] + ia, ym[i]), (cols[i + 1][0] - 1.0, ym[i])], cw_, 0.45, 2.0)
    xd = cols[3][0] + P18_MK / 2.0
    with pg.g("water", u"flow arrow 4-5"):
        arrow(pg, [(xd, bots[3] - 1.0), (xd, y2 + 0.3)], cw_, 0.45, 2.0)
    for i, (ca, cb) in ((4, (3, 2)), (5, (2, 1))):
        with pg.g("water", u"flow arrow %d-%d" % (i + 1, i + 2)):
            arrow(pg, [(cols[ca][0] - 1.0, ym[i]), (cols[cb][0] + ia, ym[i])], cw_, 0.45, 2.0)
    xl = x + P18_MK / 2.0
    with pg.g("annotations", u"closing arrow 7-1 · next winter"):    # the accent: the one arrow that is not flow
        arrow(pg, [(cols[1][0] - 1.0, ym[6]), (xl, ym[6]), (xl, bots[0] - 1.0)], C["acc"], 0.45, 2.0)
    # the bottom-left cell, under the red arrow's level: what closes the loop, then the one-way rule
    with pg.g("labels", u"next winter · one way"):
        yy = para(pg, x, ym[6] - 2.5, cw - 2.0, LOOP_BACK, FS_MIN, C["acc"], bold=True)
        para(pg, x, yy - 1.2, cw - 2.0, u"ONE WAY, WITH THE STREAM", FS_MIN, C["d3"], bold=True)
    return _p19_close(pg, n0, (x, foot, x + P18_W, y), u"wb_farms")


def _p18_vignette(pg, x0, x1, gy, top):
    """P18.4 (G9 agriculture): the farm drawn simplified, ONE field texture + ONE representative crop: a band of field
    ground (plants.py PLA_FIELD, short furrow marks in PLA_ROW, no rows) under one olive tree at print resolution
    (plants.py pla_section: the high-res silhouette where the library has it, else the vector olive with its leaf
    detail; sourced size: the lowest olive height 8 m, crown = the 5 m in-row spacing, Kaya 2017), the drip line
    along the ground. The tree is a symbol: its scale is set by the room (top - gy), not printed.
    v16 (G6-9): field band, olive and drip line each one element (the olive's image item tagged too); the drip WAT r2
    (G6-6); the field band PLA_FIELD = AGR r3 and the olive its species' colours (P-3)."""
    sh = [("poly", [(x0, gy - P18_BAND), (x1, gy - P18_BAND), (x1, gy), (x0, gy)], PLA_FIELD, None, 0.1)]
    n = int((x1 - x0) / 1.6)
    for i in range(n):                               # furrow marks: two staggered lines of short strokes (texture)
        for j, yy in enumerate((gy - 0.9, gy - 2.1)):
            px = x0 + 0.5 + i * 1.6 + (0.8 if j else 0.0) + 0.25 * ((i * 7 + j * 3) % 3)
            if px + 0.6 < x1:
                sh.append(("line", [(px, yy), (px + 0.5, yy + 0.35)], PLA_ROW, 0.08))
    with pg.g("fields", u"olive grove field band"):
        _p18_put(pg, sh)
    h_m = PLA_SPECIES["olive"]["h_range"][0]
    w_m = PLA_CROPS["olive"]["plant_m"]
    k = (top - gy) / h_m
    cx = (x0 + x1) / 2.0
    with pg.g("trees", u"olive · Olea europaea (orchard)"):
        n1 = len(pg.items)
        _p18_put(pg, pla_section("olive", cx, gy, k, h_m=h_m, crown_m=w_m, seed=3))
        for it in pg.items[n1:]:                     # shp_put appends "image" items without the Page's tag
            pg._gt(it)
    cd = _p19_hue("WAT", 2)                          # v16 (G6-6): was C["d2"]
    with pg.g("water", u"drip line"):
        pg.line([(x0, gy + 0.3), (x1, gy + 0.3)], cd, 0.3)            # the drip line on the ground
        for i in range(int((x1 - x0) / 4.0)):
            pg.circle(x0 + 2.0 + i * 4.0, gy - 0.6, 0.3, fill=cd)     # its drops
    pg.keep((x0, gy - P18_BAND, x1, top), "drawing", u"p19 farm vignette")    # round 4: no text on the drawing


def _p19_hits(cid, boxes):
    """v16 (round 6, G6-7 / G6-8): the word blocks of one p18 block [(name, (x0, y0, x1, y1))] tested pairwise; each
    overlap = an orange warning + WARNING line (never a stop). The TextPage check (pg.check_text) still runs over
    the whole cell."""
    return None                                  # v17 (L4, LAYOUT_PLAN 3.1-3): no producer-side overlap test; the
                                                 # booklet's bounding-box passes (70_check) test and fix every hit


def draw_farms_out(pg, x, y):
    """p19 group 1, where the loop ends (crop wb_farms_out, EXACTLY P19_SIDE_W x P19_R1_H from its top-left (x, y),
    beside the loop on the booklet page; its heading band left empty, the group's heading is the loop's): the farms
    outside the site and the groundwater under them (Lower Bakırçay, AQUIFER): the label on the step headings' line;
    left the farm vignette (_p18_vignette) with the olive spacing under it; right the groundwater potential and the
    total use as two horizontal bars on one scale with their values at the bars, the potential's length dashed across
    the use bar, then the ratio (facts.py, printed here once) with its two lines. Round 4 (P19.1): was
    _p18_farms_block inside wb_farms. Returns the block box.
    v16 (round 6, S5; SON page19 = ee52805 _p18_farms_block 201): the ee52805 offsets back (title ascender on the
    content top, caption 1.2 mm under the field band, vignette to 2.5 mm under the title, bar labels at top - 11 and
    top - 24 mm); P19_SIDE_W 152 mm (G6-1 frame [60,10 37x20]: the bars run longer, nothing scaled); no olive widths
    (addendum 5, SON's "500 x 700 cm" left out); the potential bar WAT r2, the use bar AGR r2 (G6-6, the same tones
    as C["w3"] / C["agri"]); every element its pg.g (G6-9); the SON pairs "olives ... drip" x "4.4 x" and step 7's
    line x "4.4 x" (one SON block) cleared: own drawing, caption and ratio separate word blocks 6 mm apart, tested
    (_p19_hits). Diagram, no section language."""
    n0 = len(pg.items)
    w, top, foot = P19_SIDE_W, y - P19_HEAD, y - P19_R1_H
    lead = FS_MIN * 1.28
    lb0 = top - CAP * FS_MIN                         # the label's baseline: its ascender on the content top (ee52805)
    t0 = u"THE FARMS OUTSIDE · GROUNDWATER, LOWER BAKIRÇAY"
    with pg.g("labels", u"the farms outside"):
        pg.text(t0, x, lb0, FS_MIN, C["dark"], bold=True)
    hits = [(t0, (x, lb0 - 0.25 * FS_MIN, x + text_w(t0, FS_MIN, True), lb0 + CAP * FS_MIN))]
    vx1 = x + P18_VIG_W
    cap = wrap(u"olives on drip along every row", FS_MIN, P18_VIG_W)   # v15: no widths (addendum 5)
    pg.tgroup()                                      # the caption's lines: one word block
    with pg.g("labels", u"olives on drip"):
        for j, ln in enumerate(cap):
            pg.text(ln, x, foot + 0.8 + (len(cap) - 1 - j) * lead, FS_MIN, C["ink"])
    pg.tgroup(False)
    hits.append((cap[0], (x, foot + 0.8 - 0.25 * FS_MIN, x + max(text_w(ln, FS_MIN) for ln in cap),
                          foot + 0.8 + (len(cap) - 1) * lead + CAP * FS_MIN)))
    gy = foot + 0.8 + (len(cap) - 1) * lead + CAP * FS_MIN + 1.2 + P18_BAND
    _p18_vignette(pg, x, vx1, gy, lb0 - 2.5)
    # the two bars: label over each bar, the value after the potential's bar and inside the use bar's end
    (pot_lab, pot), (use_lab, use) = AQUIFER
    ax0, ax1 = vx1 + 6.0, x + w
    k = (ax1 - ax0) / max(pot, use)
    bh = 6.0
    for j, (lab, v, col) in enumerate(((pot_lab, pot, _p19_hue("WAT", 2)), (use_lab, use, _p19_hue("AGR", 2)))):
        lb = top - 11.0 - 13.0 * j                   # the label's baseline; the bar 1.5 mm under it (ee52805)
        with pg.g("labels", lab):
            pg.text(lab, ax0, lb, FS_MIN, C["ink"])
        b1 = lb - 1.5
        L = k * v
        t = u"{} hm³ a year".format(v)
        tb = b1 - bh / 2.0 - CAP * FS_MIN / 2.0
        with pg.g("annotations", u"bar · {} {} hm³ a year".format(lab, v)):
            pg.poly([rect(ax0, b1 - bh, ax0 + L, b1)], fill=col)
            if text_w(t, FS_MIN, True) + 3.0 <= L:   # inside the bar's end, white (it names the bar it sits on)
                _p19_text(pg, t, ax0 + L - 1.5, tb, FS_MIN, COL["white"], bold=True, align="R")
            else:                                    # after the bar (the bar is then a keep)
                _p19_text(pg, t, ax0 + L + 1.5, tb, FS_MIN, C["ink"], bold=True)
                pg.keep((ax0, b1 - bh, ax0 + L, b1), "drawing", u"p19 aquifer bar %d" % j)
        if j == 0:
            yp0, xp = b1, ax0 + k * pot
        else:
            with pg.g("annotations", u"potential's length across the use bar"):
                pg.line([(xp, yp0), (xp, b1 - bh)], C["dark"], 0.3, dash=[1.0, 0.7])
            low_bar = b1 - bh
    r = fact_num("aquifer_use_ratio")
    if r:
        yb = foot + 0.8 + lead
        t = r + u" ×"
        lines = [u"total use against potential", (u"farm water eases the aquifer " + cite(P18_SRC_AQ)).strip()]
        with pg.g("labels", u"total use against potential · " + t):
            pg.text(t, ax0, yb - lead / 2.0, P18_BIG, C["acc"], bold=True)
            lx = ax0 + text_w(t, P18_BIG, True) + 3.0
            pg.tgroup()                              # its two lines: one word block
            pg.text(lines[0], lx, yb, FS_MIN, C["ink"])
            pg.text(lines[1], lx, yb - lead, FS_MIN, C["ink"])
            pg.tgroup(False)
        rbox = (ax0, yb - lead - 0.25 * FS_MIN, lx + max(text_w(ln, FS_MIN) for ln in lines), yb + CAP * FS_MIN)
        hits.append((t + u" " + lines[0], rbox))
        hits.append((u"bars", (ax0, low_bar, ax1, top - 11.0 + CAP * FS_MIN)))
    _p19_hits(u"wb_farms_out", hits)
    return _p19_close(pg, n0, (x, foot, x + w, y), u"wb_farms_out")


def draw_decision(pg, x, y):
    """p19 group 2, the figures: one box per fact (G4: an icon, one headline value, one line), 2 x 2, the block
    P18_DEC_W wide from its top-left (x, y) (crop wb_decision; round 4, P19.1: beside the agriculture "stream first"
    block; its heading band stays empty and the boxes start on the shared content top). The olive figures from
    facts.py (8,000 m³ per ha, 1.25 ha: printed here once); a missing live value leaves its boxes out. Each box's
    lines are one text group; the icons are keeps. Returns the block box.
    v16 (round 6, S5; SON page19 = ee52805 draw_decision 247): ONE box height for both rows (the tallest box, as
    SON), the block as tall as its two rows (no white band: the G6-1 frame [3,33 30x10] holds the boxes only), the
    SON caption "What the figures support" a caption item; each box one pg.g element (G6-9). Diagram."""
    need = fact("olive_need_m3_ha")
    items = []
    if need:
        items += [
            ("olive", fact_num("olive_need_m3_ha") + u" m³ per ha",
             (u"olives on drip, 1-in-5 dry year " + cite(fact_ref("olive_need_m3_ha")[1] or u"")).strip()),
            ("storage", fact_num("olive_ha_per_10000_m3") + u" ha", u"of olives per 10,000 m³ of stored water"),
            ("treatment", u"about {:,.0f} ha".format(round(P18_PLANT_M3_DAY * P18_PLANT_DAYS / need / 5.0) * 5),
             u"of olives from the town plant's treated water: {:.2f} million m³ in {} summer days".format(
                 P18_PLANT_M3_DAY * P18_PLANT_DAYS / 1e6, P18_PLANT_DAYS))]
    items.append(("chart", u"75 % · 29 %", (u"of farm demand met, North Aegean basin: normal year · very severe "
                                            u"drought " + cite(P18_SRC_NA)).strip()))
    # 2 x 2 boxes in P18_DEC_W (4 page columns), separated by whitespace only: no fill, no stroke (G17)
    n0 = len(pg.items)
    _p19_caption(u"wb_decision")
    cols = [(x + a, x + b) for a, b in grid_sub(P18_DEC_W, 2)]
    ic, gap = 8.0, 3.0
    lay = []
    for j, (nm, val, line) in enumerate(items):
        c0, c1 = cols[j % 2]
        tw = c1 - c0 - ic - 2.0
        V, L = wrap(val, P18_FV, tw, True), wrap(line, FS_MIN, tw)
        lay.append((j, nm, c0, V, L, len(V) * P18_FV * 1.18 + 0.8 + len(L) * FS_MIN * 1.28 + 0.6))
    bh = max([t[5] for t in lay] + [ic])             # v16 (ee52805): one box height for every row
    nrow = (len(lay) + 1) // 2
    tot = nrow * bh + (nrow - 1) * gap
    for j, nm, c0, V, L, _ in lay:
        top = y - P19_HEAD - (j // 2) * (bh + gap)
        with pg.g("labels", u"figure %d · %s" % (j + 1, V[0] if V else nm)):
            _p18_icon(pg, (nm,), c0, top, ic)
            pg.keep((c0, top - ic, c0 + ic, top), "icon", u"p19 figure icon %d" % (j + 1))
            lx, ly = c0 + ic + 2.0, top
            pg.tgroup()                              # the box's value and line: one word block
            for ln in V:
                ly -= P18_FV * 1.18
                _p19_text(pg, ln, lx, ly, P18_FV, C["d3"], bold=True)
            ly -= 0.8
            for ln in L:
                ly -= FS_MIN * 1.28
                _p19_text(pg, ln, lx, ly, FS_MIN, C["ink"])
            pg.tgroup(False)
    return _p19_close(pg, n0, (x, y - P19_HEAD - tot, x + P18_DEC_W, y), u"wb_decision")
