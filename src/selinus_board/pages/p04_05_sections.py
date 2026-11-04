# p.04-05 sections across the stream (split from parts/14_tsec_wind_arrows.py, parts/15_ndvi_col.py, parts/15c_review_pages.py, parts/15l_r28_site.py on 29 Oct 2026; moved unchanged)
# v51 (revision 29 Oct 2026, WO-T3a-3: package A "Pages 04-05", 02 §3 §4 §6, D4 b, D11, D13): each booklet page is ONE
# drawing that fills the panel (p45_plan, draw_sections_page): the page's key map on top (basemap "topographic", only
# this page's cut lines with their view triangles, inside the frame; draw_sections_key), under it the page's cuts at
# the largest round scale that fits, each beside a column with its name, its reading and its scale bar. Each cut is
# drawn as it really is (p45_strip): its banks and bed from the level module (section_parts: DSİ walls, embankments,
# loose earth; the bed at its level, 100- and 500-year flood levels, terraces), the measured trees at true size and the
# olive rows the survey shows (plants), the buildings at their floors, figures (_p45_fig); under it a segmented strip of
# what the cut crosses, each segment exactly under its part of the cut (R02). Callouts never overlap (one row each).
# The satellite rows, the building types diagram, the per-cut locator and the S4 key map (p14-15 draw their own) are gone.
# Revision 30 Oct 2026 (T6, PG3 p4-5): water at the average yearly flow in every bed (M5 water_section; along the
# stream: the surveyed bed with the registry's flow depth), Q100/Q500 lines from the registry; heights in m (never
# floors); civic halls cut as real profiles (M11 bld_section_profile) and every cut building down to its lowest ground;
# buildings beyond drawn as legible elevations; one callout for two equal banks, looser callout rows; key map from
# M4 keymap_items with its names placed by M2 lp_place; scale bars print the sheet ratio (the booklet re-sets it).
# v56 (round 2, R2-B, G14/U22/D8): houses and trees beyond stand on their own depth layer's ground (sf_back_profile,
# sf_back_house), every tree and person seated on the cut ground (sf_seat_x), wall triangles off (sf_triangles), the
# designed sky behind each cut, people by zone in the one booklet style (fig_place_zones), never in the channel.
# v57 (Aras 31 Oct 12:01 "they look like they are just put there"; R2-C focus): the people on the crossed streets
# who stay look at the stream when it is near (P45_FOCUS_WATER_M), else at each other (their zone's middle).
# v58 (round 3, P04.1 / P04.2 / G15 / G3 / G16 / G2): street names and levels as compact tags in ONE row under each
# cut's strip, a tag with no room a numbered disc on its spot + the key beside the cut (p45_band; no leaders, no
# stacked rows); every sky by cut id (sf_sky cid, birds on); the cut ground through sct_ground (soil gradient + hatch);
# people by zone in front (bank edge fishing/watching over the water level, streets, open ground at the water), trees
# paler behind them, lamps / bollards / bike racks only on the streets the cut crosses (p45_street_kit); bridge and
# bank names from names.py (no K-code printed); one FLAG overlap line per page (p04, p05).
# v61 (round 6, U20, PLAN P-7, BRIEF §6 rows 4-5). LANGUAGE: SITE (every cut S1-S8: these cuts ARE the r06_S04
# target, kept as drawn; only moved / enlarged by the booklet). Each cut is exported as its drawing (sb_sec_sN: title,
# cut, strip, tags, level marks, its scale bar under its left end; the booklet prints the one scale value under it)
# and its note as text-only items (sb_sec_note_sN_n1.., placed level with the cut); key map from keymap.py v3
# (km_keymap, exported, never drawn here); legend in the hue table (G6-6); no zoom insets (not in SON); level values
# spread at the right edge (p45_level_marks); trees by species (G6-10); every element tagged (G6-9); a bridge only
# where the cut crosses one.

P45_KM = {}                       # v60.2: page id -> the page's key map (v61: km_keymap v3 dict), exported by 16d
P45_LEG = {}                      # v60.2: page id -> the page's legend entries [(swatch, text)], exported by 16d
P45_KM_MM = {"p04": (302.0, 53.0), "p05": (311.0, 56.0)}   # mm: v61 (frames_p01-08 §3): the key map's frame
#                                   [7,12 72x18] on p04, [5,9 74x19] on p05 (1 % x = 4.2 mm, 1 % y = 2.97 mm)
P45_DRAW_MM = 300.0               # mm: v61 (frames §3, P-7): a cut's drawing incl. its level marks (zone x 7.0-78.6 %
#                                   = 300.7 mm); the note column right of it is exported apart
P45_PAGES = (("S1", "S2", "S3", "S4"), ("S5", "S6", "S7", "S8"))   # p04, p05 (package A)
P45_ALONG = ("S6",)               # cuts that run along the stream: cropped to the part around their crossings (v59: S5 is across, N4 b)
P45_DENS = (1000, 2000, 2500, 5000)   # the round scales tried, largest first (SCRIPT_STANDARD §8); v59 (P04.1): 1:1,000 first
P45_KEEP = 0.5                    # v59 (P04.1, drawing rule): a cut may be cropped to the part around its stream if at
                                  # least this share stays (bigger sections; was SEC_KEEP 0.7, which ruled 1:1,000 out)
P45_H = BK_AH - 2.0               # mm: the drawing's height on the booklet page (the panel, a 2 mm margin kept)
P45_TXT = dict(head=8.0, call=6.0, minor=5.0, strip=5.0, ctx=6.5)  # booklet pt: names, sentences + callouts, levels
#                                   (v61, U20 "yazilar kucultulcek": one step smaller; >= 4 pt at 0.8 x, 1:2,000 -> 2,500)
P45_NOTE_PT = dict(head=7.0, call=6.0, minor=5.0)   # v61 (U20): the note beside each cut (exported as note items)
P45_COL_MIN = 62.0                # mm: v59 (G-R4-3 LEFT template): the side column = 2 grid columns (29 + 4 + 29)
P45_LEV_MM = 32.0                 # mm: v59 (G-R4-5.4): the margin right of each drawing for its level marks (U44);
#                                   v61: 32 (was 24: "+58.22 mean flow" ran past it)
P45_TITLE_MM = 7.0                # mm: v59 (G-R4-3): the title strip over each drawing (one line, 9 pt)
P45_GAP = 4.0                     # mm: between a cut and its column, and between rows
P45_KEY_MIN = 34.0                # mm: the key map at least this tall (v61: room the scale pick keeps for it)
P45_FIG_STYLE = "a"               # v56: the one human style of the booklet (D1 a; Aras 31 Oct 11:24)
P45_FOCUS_WATER_M = 40.0          # m: v57: people on a street this near a crossing look at the water (drawing rule, as
#                                   P45_NEAR_M), else at each other
P45_NEAR_M = 40.0                 # m: v56 G14: buildings / trees beyond within this are the near depth layer (drawing rule;
#                                   the v55 outline limit)
P45_MATCH_M = 3.0                 # m: a level row is drawn at the crossing whose bed is nearest, within this
P45_WALL_T_M = 0.60               # m: DSİ wall thickness: the value the site board drew (sec_cut chwalls, s +-0.30 m);
#                                   no source found (section_parts asks the caller): see WO-T3a-3 OPEN
P45_STRIP_WORD = {"residential": u"homes", "mixed": u"shops + homes", "commercial": u"shops", "institutional": u"civic",
                  "religious": u"heritage", "industrial": u"workshops", "transport": u"street", "green": u"green",
                  "agri": u"farmland", "vacant": u"vacant", "water": u"stream", "void": u"open ground"}
P45_TREE_ANY = "plane"            # a measured tree with no species (sb_tree_species None): the broadleaf primitive,
#                                   drawn generic and never named (v61, G6-10)
# v61 (G6-6, H1 note 1): the strip's land uses -> (hue code, rank) of the hue table (common/hues.py)
P45_CAT_HUE = {"commercial": ("MOV", 1), "mixed": ("MOV", 2), "residential": ("MOV", 3), "institutional": ("PUB", 2),
               "religious": ("HER", 3), "industrial": ("CTX", 2), "transport": ("CTX", 3), "vacant": ("CTX", 4),
               "void": ("CTX", 5), "green": ("GRN", 3), "agri": ("AGR", 3), "water": ("WAT", 3)}
P45_BANK_WORD = {"dsi_wall": u"a DSİ stone wall", "embankment": u"an embankment", "loose_earth": u"a loose earth bank",
                 "no_crest": u"rising ground"}
P45_END_LIFT = 0.45               # v61: an end level's baseline this many text heights over its ground point
P45_BRIDGE_D = 8.0               # m: v61: a bridge's side line within this of a cut counts as on it (half a deck
#                                   of the town's bridges, 4-12 m wide; drawing rule)
P45_BRIDGE_T_M = 0.50             # m: v61: the deck drawn this thick (sf_bridge's drawing rule; no deck data)
P45_EDGE_M = 3.0                 # m: v58 G15: the bank-top strip where people fish and watch the water (drawing rule)
P45_LAWN_M = 25.0                 # m: v58 G15: open ground this near a bank is used as a lawn (lying, dogs, play;
#                                   drawing rule)
P45_BOLLARD_M = 6.0               # m: v58 G15: a street ending this near a bank top gets a bollard (keeps cars off
#                                   the bank edge; drawing rule)
P45_NUM = [0]                     # v58 (G3): the last number handed out on the page being drawn (reading order)
P45_BOXES = []                    # v58 (G3): text boxes placed on the page being drawn (board units)
P45_COLLECT = [False]             # v58: True while draw_sections_page draws (not the dry measuring runs)


def _p45_tb(x0, x1, y, h):
    """v58 (round 3, G3): note one text line (x0..x1, baseline y, capital height h; board units) for the page's
    overlap test (only while the page is drawn)"""
    if P45_COLLECT[0]:
        P45_BOXES.append((min(x0, x1), y - 0.25 * h, max(x0, x1), y + h))


def _p45_para(B, txt, x, y, width, h, col, L, lead=1.45, bcol=None):
    """v58 (G3): site28_para (txt wrapped to width from baseline y), each line's box noted (_p45_tb); returns the
    next baseline"""
    for ln in site28_lines(txt, width, h):
        site28_draw_line(B, ln, x, y, h, col, L, 40, bcol)
        _p45_tb(x, x + site28_line_w(ln, h), y, h)
        y -= lead * h
    return y


def _p45_disc(B, L, n, cx, y, h, order=40):
    """v58 (G3): number n on its spot: white bold figures on an ink disc centred on cx, baseline y, capital height h;
    returns the disc's half width"""
    # v59 (round 4, G-R4-7): the shared marker (common/marker.py): the figure centred on its ink box, the circle
    # sized to it (two digits a larger circle), white on the ink of the line work it names (banks, places are ink2)
    kb_ = h / bk_hk(P45_TXT["strip"], 1.0) if bk_hk(P45_TXT["strip"], 1.0) else 1.0
    sh, box, r = mk_marker(cx / kb_, (y + 0.5 * h) / kb_, u"%d" % n, "6B645B", size_pt=P45_TXT["strip"])
    _p45_put(B, L, sh, lambda q: (q[0] * kb_, q[1] * kb_), kb_, order)
    _p45_tb(cx - r * kb_, cx + r * kb_, y, h)
    return r * kb_


def _p45_c(c):
    return C(c) if isinstance(c, str) else c


def p45_cat_hex(cat):
    """v61 (G6-6): the hue-table colour ("RRGGBB") of a strip land use (P45_CAT_HUE; an unlisted use: CTX r3)"""
    code, rank = P45_CAT_HUE.get(cat, ("CTX", 3))
    return hue(code, rank)                                                                    # noqa: F821


def p45_kind_of(cat):
    """v61 (G6-9): the element kind of a strip segment (farmland and green "fields", the stream "water", else
    "ground")"""
    return {"agri": "fields", "green": "fields", "water": "water"}.get(cat, "ground")


def p45_tree(B, L, T, kb, key, x_mm, gy, km, h_m, crown_m, seed, beyond=True, layer=0, order=32):
    """v61 (G6-10): one measured tree (species key or None = generic) drawn by pla_section at its MEASURED height:
    existing trees skip the species height range (tree_species.md T3 "Height check G6"): the range is opened for
    the one call (pla_height_ok would move the height and log a line per value). Returns True when the measured
    height lies outside the species' sourced range (counted for one log line per page)."""
    k_ = key or P45_TREE_ANY
    if "PLA_SPECIES" in globals() and k_ not in PLA_SPECIES:                                 # noqa: F821
        k_ = P45_TREE_ANY                                # a species with no plant image (cypress, poplar): generic,
    sp_ = PLA_SPECIES.get(k_) if "PLA_SPECIES" in globals() else None    # named in its group only    # noqa: F821
    hr_ = sp_.get("h_range") if sp_ else None
    out = bool(hr_) and h_m is not None and ((hr_[0] is not None and h_m < hr_[0]) or
                                              (hr_[1] is not None and h_m > hr_[1]))
    try:
        if hr_:
            sp_["h_range"] = (None, None)
        _p45_put(B, L, pla_section(k_, x_mm, gy, km, h_m=h_m, crown_m=crown_m, beyond=beyond, seed=seed,
                                   layer=layer), T, kb, order)
    finally:
        if hr_:
            sp_["h_range"] = hr_
    return out


P45_TREE_OUT = {}                 # v61: page -> measured trees outside their species' height range (one log line)


def p45_tree_n(page, key, out=False):
    """v61 (G6-10): count one tree drawn on page (key None = generic) in SB_TREE_N (05_build_terrain, read by
    sb_tree_log), or with out=True one measured height outside its species' range"""
    if not page:
        return
    if out:
        P45_TREE_OUT[page] = P45_TREE_OUT.get(page, 0) + 1
        return
    c_ = SB_TREE_N.setdefault(page, {})                                                       # noqa: F821
    k_ = key or "tree"
    c_[k_] = c_.get(k_, 0) + 1


def _p45_put(B, L, shapes, T, kb, order):
    """the modules' house shapes ("poly", ring, fill, stroke, lw) / ("line", pts, colour, lw[, dash mm]) (booklet mm,
    y up) through T (mm -> board units), line weights in booklet mm; text and image shapes are not used here"""
    for sh in shapes or []:
        if not sh:
            continue
        if sh[0] == "image":                              # v56: style a cutouts (people, plants)
            x0_, y0_ = T((sh[1], sh[2]))
            x1_, y1_ = T((sh[1] + sh[3], sh[2] + sh[4]))
            B.image(sh[5], x0_, y0_, x1_, y1_, L, order=order, alpha=sh[6] if len(sh) > 6 else None,
                    flip=bool(sh[7]) if len(sh) > 7 else False)
            continue
        if sh[0] == "poly":
            pts = [T(p) for p in sh[1]]
            if len(pts) < 3:
                continue
            if sh[2]:
                B.fill([pts], _p45_c(sh[2]), L, order)
            if len(sh) > 3 and sh[3]:
                B.line(pts + [pts[0]], _p45_c(sh[3]), L, order, bk_lw((sh[4] if len(sh) > 4 else None) or 0.1, kb))
        elif sh[0] == "line":
            pts = [T(p) for p in sh[1]]
            dash = sh[4] if len(sh) > 4 and isinstance(sh[4], (list, tuple)) else None
            for d_ in (r28_pattern(pts, [m_ * kb for m_ in dash]) if dash else [pts]):
                B.line(d_, _p45_c(sh[2]), L, order, bk_lw((sh[3] if len(sh) > 3 else None) or 0.1, kb))
        elif sh[0] == "text" and len(sh) >= 8:          # v59 (round 4): module texts (level marks, inset bars,
            q = T((sh[2], sh[3]) if not isinstance(sh[2], (list, tuple)) else sh[2])   # markers): size = em mm
            sz, col, bold, al = (sh[4], sh[5], sh[6], sh[7]) if not isinstance(sh[2], (list, tuple)) else \
                (sh[3], sh[4], sh[5], sh[6])
            if u"%s" % sh[1]:
                B.text(u"%s" % sh[1], q[0], q[1], sz * _PDF_CAP["sans"] * kb, _p45_c(col or "4A3F35"), L,
                       order=order + 1, font=FONT_TITLE, bold=bool(bold), align=al or "L")


def _p45_items(B, L, items, P, kb, order):
    """M11 building items ("fill", rings, hex, alpha, closed) / ("line", pts, hex, lw mm, dash, alpha) in (s, z) m
    through P (s, z) -> board units; text items are not used (the page tags its buildings itself)"""
    for it in items or []:
        if it[0] == "fill":
            B.fill([[P(s, z) for s, z in r] for r in it[1]], _p45_c(it[2]), L, order)
        elif it[0] == "line":
            pts = [P(s, z) for s, z in it[1]]
            for d_ in (r28_pattern(pts, [m_ * kb for m_ in it[4]]) if it[4] else [pts]):
                B.line(d_, _p45_c(it[2]), L, order + 1, bk_lw(it[3] or 0.1, kb))


def _p45_tag(ftype, cat, floors, fl, h, wpx, hm):
    """a cut building's tag in metres (G6, never floors): "old town · 6.40 m" where the building (wpx board units
    wide) holds it, else its height alone, else None; h = its height from its ground to its eaves (m)"""
    tag = typo_label(ftype, cat, floors, fl[0], fl[4] if len(fl) > 4 else "")
    head = tag.rsplit(u" · ", 1)[0] if tag.endswith(u" fl") else tag
    hh = u_height(h)
    for t_ in (head + u" · " + hh, hh):
        if wpx > 0.6 * site28_tw(t_, hm):
            return t_
    return None


def p45_rows_of(nm):
    """the level module's row ids of cut nm (one, or one per crossing on S5/S6); [] without the module"""
    try:
        ids = level_ids()
    except Exception:
        return []
    out = []
    for i in ids:
        try:
            r = level_cut(i)
        except Exception:
            continue
        if i == nm or r.get("cut") == nm:
            out.append(i)
    return out


def p45_sides(sd_):
    """(the bank at the cut's start, the bank at its end) as the level module names them ("NE"/"SW"): the end
    lying further north-east (survey x east, y north) is on the north-east bank"""
    x0, y0, x1, y1 = sd_["line"][:4]
    return ("NE", "SW") if x0 + y0 > x1 + y1 else ("SW", "NE")


def p45_reach(sd_, x_e, dirn, zt, far=60.0):
    """where the surveyed ground, going out from x_e (dirn -1 left, +1 right), first reaches the level zt (relative
    to the cut's base); None within far m"""
    gr = sd_["ground"]
    n = len(gr)
    i = max(0, min(n - 1, int(round(x_e / 0.5))))
    while 0 <= i < n and abs(gr[i][0] - x_e) <= far:
        if gr[i][1] >= zt - 0.02:
            return gr[i][0]
        i += int(dirn)
    return None


def p45_banks(sd_):
    """the cut's stream crossings with a row in the level module (02 §6): [dict(k, rid, a, b, bed, zb, f, along,
    sides)], along = the cut runs along the stream there (its angle under SITE28_CROSS: no bank is cut),
    sides = [left, right] dicts (side, typ, x, dirn, top, zt, h, ang, crest). The bed, the bank and wall tops,
    their types and angles are the level module's (v58, N1 a: S4 on the survey datum, read from levels.py like every
    cut; no level is written in this file); the place of the water on the cut is the site
    board's (its run a..b). A row goes to the crossing whose bed is nearest (P45_MATCH_M), across the stream first.
    Memoised on the cut."""
    if "_p45b" in sd_:
        return sd_["_p45b"]
    out = []
    runs = sd_["water"]
    base = sd_["base"]
    rows = [sd_["p45_cross"]] if sd_.get("p45_cross") else p45_rows_of(sd_["name"])   # v59 (N4 b): S5's one row
    bks = sd_.get("banks") or []
    m = {}
    if len(rows) == 1 and runs:
        m[site28_main_k(sd_)] = rows[0]
    elif rows and runs:
        free = list(range(len(runs)))
        for rid in rows:
            bed = level(rid, "bed")
            if bed is None or not free:
                continue
            j = min(free, key=lambda j_: ((bks[j_] if j_ < len(bks) else {}).get("ang", 90.0) < SITE28_CROSS,
                                          abs(runs[j_][2] + base - bed)))
            if abs(runs[j][2] + base - bed) > P45_MATCH_M:
                continue
            m[j] = rid
            free.remove(j)
    left, right = p45_sides(sd_)
    for k_ in sorted(m):
        rid = m[k_]
        bed = level(rid, "bed")
        if bed is None:
            continue
        a, b = runs[k_][0], runs[k_][1]
        zb = bed - base
        row = level_cut(rid)
        ang_c = level(rid, "angle_deg")
        f = 1.0 / max(0.25, math.sin(math.radians(ang_c))) if ang_c else 1.0   # along the cut, not across the stream
        if sd_.get("p45_cross"):                         # v59 (N4 b): the new S5 is at right angles to the stream
            f = 1.0
        sides = []
        for nm_s, x_e, dirn in ((left, a, -1.0), (right, b, 1.0)):
            typ = (row.get(nm_s) or {}).get("type") or "no_crest"
            top = level(rid, "top", nm_s)
            ang = level(rid, "angle_deg", nm_s)
            zt = None if top is None else top - base
            if typ == "dsi_wall" and zt is None:
                zt = zb + SCT_DSI_WALL_H_M
            crest = None
            if typ == "dsi_wall":
                crest = x_e + dirn * P45_WALL_T_M * f
            elif typ == "embankment" and ang and zt is not None and zt > zb:
                crest = x_e + dirn * (zt - zb) / math.tan(math.radians(ang)) * f
            elif zt is not None:
                crest = p45_reach(sd_, x_e, dirn, zt)
            if crest is not None:
                crest = max(0.0, min(sd_["L"], crest))
            sides.append(dict(side=nm_s, typ=typ, x=x_e, dirn=dirn, top=top, zt=zt, h=level(rid, "height", nm_s),
                              ang=ang, crest=crest))
        along = (bks[k_] if k_ < len(bks) else {}).get("ang", 90.0) < SITE28_CROSS
        out.append(dict(k=k_, rid=rid, a=a, b=b, bed=bed, zb=zb, f=f, along=along, sides=sides))
    sd_["_p45b"] = out
    return out


def p45_ground(sd_):
    """the cut's ground [(s, z)] as drawn: the surveyed ground, and at each crossing of p45_banks the banks as they
    are (a DSİ wall: its water face up to its top and its thickness; an embankment: toe to top at its angle; loose
    earth: the surveyed slope down to the bed) and the bed flat at its level. A crossing along the stream keeps the
    surveyed ground (its bed falls along the cut; no bank is cut). Memoised on the cut."""
    if "_p45g" in sd_:
        return sd_["_p45g"]
    g = list(sd_["ground"])
    for cr in p45_banks(sd_):
        if cr["along"]:
            continue
        l_, r_ = cr["sides"]
        zb = cr["zb"]
        sl = min(cr["a"], l_["crest"] if l_["crest"] is not None else cr["a"])
        sr = max(cr["b"], r_["crest"] if r_["crest"] is not None else cr["b"])
        mid = []
        if l_["typ"] == "dsi_wall":
            mid += [(sl, l_["zt"]), (cr["a"], l_["zt"]), (cr["a"], zb)]
        elif l_["typ"] == "embankment" and l_["crest"] is not None and l_["crest"] < cr["a"]:
            mid += [(sl, l_["zt"]), (cr["a"], zb)]
        else:
            mid += [(s, max(z, zb)) for s, z in sd_["ground"] if sl <= s < cr["a"]] + [(cr["a"], zb)]
        mid.append((cr["b"], zb))
        if r_["typ"] == "dsi_wall":
            mid += [(cr["b"], r_["zt"]), (sr, r_["zt"])]
        elif r_["typ"] == "embankment" and r_["crest"] is not None and r_["crest"] > cr["b"]:
            mid += [(sr, r_["zt"])]
        else:
            mid += [(s, max(z, zb)) for s, z in sd_["ground"] if cr["b"] < s <= sr]
        g = [p for p in g if p[0] < sl - 1e-6] + mid + [p for p in g if p[0] > sr + 1e-6]
        cr["win"] = (sl, sr)
    sd_["_p45g"] = g
    return g


def p45_span(g, c, zq):
    """(s left, s right) to which water at the level zq spreads over the ground g from s = c; None if c is dry"""
    if not g:
        return None
    i = min(range(len(g)), key=lambda j: abs(g[j][0] - c))
    if g[i][1] >= zq:
        return None

    def walk(rng):
        prev = g[i]
        for j in rng:
            q = g[j]
            if q[1] >= zq:
                t = (zq - prev[1]) / (q[1] - prev[1]) if abs(q[1] - prev[1]) > 1e-9 else 0.0
                return prev[0] + t * (q[0] - prev[0])
            prev = q
        return prev[0]
    return walk(range(i - 1, -1, -1)), walk(range(i + 1, len(g)))


def p45_water(sd_, cr, g, km, base):
    """G8 / M5: a crossing's water at the AVERAGE YEARLY FLOW of the cut registry (never dry) as house shapes in mm
    from the cut's origin (k = km mm per m, levels relative to base). Across the stream: water_section over the bed
    and banks as drawn (the bed band, the water body), its Q lines replaced by the 100- and 500-year levels spread
    over the cut ground from the stream's middle (p45_span). Along the stream: the surveyed bed with the registry's
    average-flow depth over the run. Nothing (logged) where the registry has no average flow."""
    rid = cr["rid"]
    avg, bed = level_avg_flow(rid), cr["bed"]
    if avg is None or avg <= bed:
        LOG.append(u"Section {}: {} has no average-flow level in the cut registry: water not drawn.".format(
            sd_["name"], rid))
        return []
    Pa = _wat_pal()
    if cr["along"]:
        dep = avg - bed
        bot = [(s * km, z * km) for s, z in g if cr["a"] <= s <= cr["b"]]
        if len(bot) < 2:
            return []
        top = [(x_, y_ + dep * km) for x_, y_ in bot]
        return [("poly", top + list(reversed(bot)), Pa["sec"], None, 0.1), ("line", top, SEC["hatch"], 0.3)]
    sl, sr = cr.get("win", (cr["a"], cr["b"]))
    prof = [(s * km, z * km) for s, z in g if sl - 1.0 <= s <= sr + 1.0]
    if len(prof) < 3:
        return []
    try:
        wl = water_section(prof, km, lambda lev: (lev - base) * km, cid=rid, fill_ground=False, labels=False,
                           bed_band_m=1.0)
    except ValueError as e:
        LOG.append(u"Section {}: water not drawn ({}).".format(sd_["name"], e))
        return []
    out = [sh for sh in wl.shapes() if not (sh[0] == "line" and len(sh) > 4 and sh[4])]
    c_ = 0.5 * (cr["a"] + cr["b"])
    for key, dash in (("q500", [0.4, 0.5]), ("q100", [1.2, 0.6])):
        q = level(rid, key)
        sp = p45_span(g, c_, q - base) if q is not None else None
        if sp:
            out.append(("line", [(sp[0] * km, (q - base) * km), (sp[1] * km, (q - base) * km)], Pa[key], 0.25, dash))
    return out


def p45_bank_word(sd):
    """a bank's callout from the level module: its kind and its top (heights m, 2 decimals)"""
    if sd["top"] is None and sd["typ"] != "dsi_wall":
        return None
    if sd["typ"] == "dsi_wall":
        hw_ = u_height(sd["h"] if sd["h"] is not None else SCT_DSI_WALL_H_M)
        if sd["top"] is None:
            return u"DSİ stone wall · {} high".format(hw_)
        return u"DSİ stone wall · top {} · {} high".format(u_level(sd["top"]), hw_)
    if sd["typ"] == "embankment":
        return u"embankment{} · top {}".format(u" {:.0f}°".format(sd["ang"]) if sd["ang"] else u"", u_level(sd["top"]))
    if sd["typ"] == "loose_earth":
        return u"loose earth bank · top {}".format(u_level(sd["top"]))
    return None


def p45_level_marks(frame_box, levels, y_of, cols=None, page=None, nm=u"", xmax=None):
    """v61 (frames §4 page5, PLAN §2.3 "▽ level values at the right edge, never stacked"): the level marks of one cut
    beside its drawing's right edge (sf_level_marks' marker: dashed line, open ▽, value; booklet mm from the cut's
    origin, y up). The marks stay at their levels; their values are spread vertically so two labels are always at
    least a text height + SF_LEVEL["clear"] apart (pushed apart both ways, kept inside the drawing's height), a thin
    joining line where a value moved. A value that cannot fit (the drawing too low for all of them, or wider than
    xmax) = wn_warn and left out, never piled. Returns shapes."""
    x0, y0, x1, y1 = frame_box
    size = SF_LEVEL["size"]
    rows = _sf_level_rows(levels, y_of, y0, y1, page)                 # (y, key, value, colour), top first
    if not rows:
        return []
    d = size + SF_LEVEL["clear"]                                     # text height + clear: the least gap
    xs = x1 + SF_LEVEL["gap"]
    Ld = sum(SF_LEVEL["dashes"])
    tw_, th_, lw_ = SF_LEVEL["tri_w"], SF_LEVEL["tri_h"], SF_LEVEL["lw"]
    ax = xs + Ld
    xt = ax + 0.5 * tw_ + SF_LEVEL["label_gap"]
    lo_, hi_ = y0 - 0.35 * size, y1 - 1.0 * size                      # label baselines inside the drawing's height
    while rows and len(rows) > 1 and (len(rows) - 1) * d > hi_ - lo_:
        drop = next((r_ for r_ in rows if r_[1] == "roof"), rows[-1])
        wn_warn(page, "levels", u"%s: no room for the value %+.2f %s at the right edge: left out" % (
            nm, drop[2], SF_LEVEL_NAMES.get(drop[1], drop[1])))
        rows = [r_ for r_ in rows if r_ is not drop]
    want = [y - 0.35 * size for y, k_, v_, c_ in rows]               # baselines centred on each mark
    ty = [min(hi_, max(lo_, w_)) for w_ in want]
    for _it in range(60):                                            # push neighbours apart, both ways
        moved_ = False
        for i in range(1, len(ty)):
            gap_ = ty[i - 1] - ty[i]
            if gap_ < d - 1e-6:
                m_ = 0.5 * (d - gap_)
                ty[i - 1] = min(hi_, ty[i - 1] + m_)
                ty[i] = max(lo_, ty[i] - m_)
                moved_ = True
        if not moved_:
            break
    for i in range(1, len(ty)):                                      # exact: the least gap from the top down
        ty[i] = min(ty[i], ty[i - 1] - d)
    sh, n_mv = [], 0
    for (y, key, val, col), t_ in zip(rows, ty):
        col = (cols or {}).get(key) or col
        txt = u"%+.2f %s" % (val, SF_LEVEL_NAMES.get(key, u"%s" % key))
        if t_ < lo_ - 1e-6 or (xmax is not None and xt + site28_tw(txt, size * _PDF_CAP["sans"]) > xmax + 1e-6):
            wn_warn(page, "levels", u"%s: the value %s does not fit at the right edge: left out" % (nm, txt))
            continue
        pos = 0.0
        for i, dd in enumerate(SF_LEVEL["dashes"]):                  # dash, gap, dash, gap, dash
            if i % 2 == 0:
                sh.append(("line", [(xs + pos, y), (xs + pos + dd, y)], col, lw_))
            pos += dd
        sh.append(("poly", [(ax, y), (ax - 0.5 * tw_, y + th_), (ax + 0.5 * tw_, y + th_)], None, col, lw_))
        if abs(t_ - (y - 0.35 * size)) > 0.2:
            n_mv += 1
            sh.append(("line", [(ax + 0.5 * tw_, y), (xt - 0.2, t_ + 0.35 * size)], col, 0.08))
        sh.append(("text", txt, xt, t_, size, col, False, "L"))
    SF_LOG.append(u"levels %s gap ok: %s %d markers at the right edge, %d values spread (gap >= %.1f mm)" % (
        page or u"", nm, len(rows), n_mv, d))
    return sh


def p45_symbols(S, sd_):
    """the survey's tree symbols near the cut: [(s along, d to the left of the cut, kind)], memoised"""
    if "_p45t" in sd_:
        return sd_["_p45t"]
    x0, y0, x1, y1 = sd_["line"][:4]
    Lc = math.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / Lc, (y1 - y0) / Lc
    out = []
    for t in getattr(S, "trees", None) or []:
        tx, ty, kind = t[0], t[1], t[3]
        s = (tx - x0) * ux + (ty - y0) * uy
        d = (tx - x0) * -uy + (ty - y0) * ux
        if -5.0 <= s <= Lc + 5.0 and -8.0 <= d <= 75.0:
            out.append((s, d, kind))
    sd_["_p45t"] = out
    return out


def p45_bridges(S, sd_):
    """v61 (round 5 open row): the bridges the cut CROSSES: [(s0, s1)] m along the cut where it crosses the stream
    (one of its water runs) on a surveyed bridge (S.bridges: the deck's side lines): a bridge line that the cut
    meets, or that lies on both sides of it (its two side lines within P45_BRIDGE_D m, one each side), over a
    water run; span = the bridge lines' extent along the cut. Memoised. Bridges only seen beyond (sd_["bridges"])
    are not drawn."""
    if "_p45br" in sd_:
        return sd_["_p45br"]
    x0, y0, x1, y1 = sd_["line"][:4]
    Lc = math.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / Lc, (y1 - y0) / Lc
    runs = [(a, b) for a, b, bed, lvl in sd_["water"]]
    cand = []
    for P_ in getattr(S, "bridges", None) or []:
        if len(P_) < 2:
            continue
        sv = [(px - x0) * ux + (py - y0) * uy for px, py in P_]
        dv = [-(px - x0) * uy + (py - y0) * ux for px, py in P_]
        s0, s1 = max(0.0, min(sv)), min(sd_["L"], max(sv))
        if s1 - s0 < 1.0 or min(abs(d_) for d_ in dv) > P45_BRIDGE_D:
            continue
        if not any(s0 < b and a < s1 for a, b in runs):
            continue
        hit = min(dv) < 0.0 < max(dv) or any(
            seg_x((x0, y0), (x1 - x0, y1 - y0), a, (b[0] - a[0], b[1] - a[1])) for a, b in zip(P_[:-1], P_[1:]))
        cand.append((s0, s1, 0 if hit else (1 if sum(dv) > 0 else -1)))
    out = []
    for s0, s1, sg in cand:
        if sg == 0:
            span = (s0, s1)
        else:                                            # a side line: crossed only with a side line opposite
            opp = [(t0, t1) for t0, t1, t2 in cand if t2 == -sg and t0 < s1 and s0 < t1]
            if not opp:
                continue
            span = (min([s0] + [t0 for t0, t1 in opp]), max([s1] + [t1 for t0, t1 in opp]))
        if not any(span[0] - 0.5 <= a and b <= span[1] + 0.5 for a, b in out):
            out = [q_ for q_ in out if not (span[0] <= q_[0] and q_[1] <= span[1])] + [span]
    sd_["_p45br"] = sorted(out)
    return sd_["_p45br"]


def p45_segments(sd_, minw):
    """what the cut crosses as segments [[s0, s1, cat]]: runs of one kind merged, slivers under minw m given to a
    neighbour (the stream never)"""
    segs = []
    for a, b, cat in sd_["strip"]:
        if segs and segs[-1][2] == cat:
            segs[-1][1] = b
        else:
            segs.append([a, b, cat])
    out = []
    for sg in segs:
        if out and sg[1] - sg[0] < minw and sg[2] != "water":
            out[-1][1] = sg[1]
        elif out and out[-1][1] - out[-1][0] < minw and out[-1][2] != "water":
            sg[0] = out[-1][0]
            out[-1] = sg
        else:
            out.append(sg)
    res = []
    for sg in out:
        if res and res[-1][2] == sg[2]:
            res[-1][1] = sg[1]
        else:
            res.append(list(sg))
    return res


def p45_end(kb):
    """the room (board units) at both ends of a cut for its end name and end level"""
    hd, hm = bk_hk(P45_TXT["head"], kb), bk_hk(P45_TXT["minor"], kb)
    return max(site28_tw(u"+888.88", hm), site28_tw(u"S8'", hd, True)) + 2.0 * kb


def p45_dep(cr):
    """a crossing's bed in words, from the level module: between DSİ walls, or how deep below the lower open bank"""
    walls = [sd for sd in cr["sides"] if sd["typ"] == "dsi_wall"]
    if len(walls) == 2:
        return u"the bed at {} lies between **DSİ stone walls {} high**".format(
            u_level(cr["bed"]), u_height(max(sd["h"] if sd["h"] is not None else SCT_DSI_WALL_H_M for sd in walls)))
    open_ = [sd for sd in cr["sides"] if sd["top"] is not None and sd["typ"] != "dsi_wall"]
    if open_:
        lo = min(open_, key=lambda sd: sd["top"])
        return u"the bed at {} lies **{} below** the lower bank, {}".format(
            u_level(cr["bed"]), u_height(lo["top"] - cr["bed"]), P45_BANK_WORD.get(lo["typ"], u"a bank"))
    return u"the bed lies at {}".format(u_level(cr["bed"]))


def draw_section_strip(S, B, sd_, x, y, w, ss, U, dry=False, tag="page", scale_txt=None, loc=True):
    """v51: one cut, drawn by p45_strip from y down in a column w wide (the old signature, kept for the core's
    sections_plan, which measures cuts with it); returns the y below. tag, scale_txt and loc are no longer used (the
    page draws the cut's name, reading and scale bar beside it, and one key map)."""
    kb = (sd_.get("_p45") or sd_.get("_txt") or {}).get("k") or 140.0 * U / BK_AW
    return p45_strip(S, B, sd_, x, y, w, ss, kb, U, dry=dry)


def p45_strip(S, B, sd_, x, ytop, wd, ss, kb, U, dry=False, L="LU_BOARD::Sections"):
    """v51 (WO-T3a-3; package A p04-05, 02 §3 §4 §6, R02): one cut as it really is, from ytop down in a column wd
    wide, its start at x + p45_end (ss board units per metre, kb per booklet mm): behind it the buildings and trees
    beyond (paler); the cut ground (p45_ground) with the banks and bed of the level module through section_parts
    (DSİ walls, embankments, earth, the gravel bed), the 100- and 500-year flood water, the terraces; the cut
    buildings at their floors with their tags; the measured trees at true size (v61: species from sb_tree_species,
    sd_["trees_sp"] / ["btrees_sp"], else generic), the survey's olive rows where the cut crosses them, figures where people stand; its end names and
    levels outside it; under it the segmented strip of what it crosses, each segment under its part of the cut.
    v58: the street names and levels as one row of tags under the strip (p45_band), its numbered words in
    sd_["_p45key"] for the key beside the cut. dry: only what sets the height. Returns the y below."""
    nm = sd_["name"]
    Lm = sd_["L"]
    off = sd_.get("s_off", 0.0)
    base = sd_["base"]
    hd, hc, hm, hst = [bk_hk(P45_TXT[q], kb) for q in ("head", "call", "minor", "strip")]
    end = p45_end(kb)
    km = ss / kb                                          # booklet mm per metre: the modules' k
    crs = p45_banks(sd_)
    g = p45_ground(sd_)
    zmax = max([sd_["zmax"]] + [sd["zt"] + 0.5 for cr in crs for sd in cr["sides"] if sd["zt"] is not None])
    zbot = min(-3.0, min(z for s, z in g) - 1.2) if g else -3.0
    X0 = x + end
    # v61 (frames §4: "+118.87" struck by the ground line, "+50.18" on the "S2" tag): an end's level sits wholly over
    # its ground point, its name a text height over the level (P45_END_LIFT)
    room = max([1.5 * kb] + [P45_END_LIFT * hm + 2.0 * hm + hd + 0.5 * kb - (zmax - g_[1]) * ss
                             for g_ in ((g[0], g[-1]) if g else ())])
    Y0 = ytop - room - zmax * ss                          # the end names over their levels stay under ytop

    def P(px, pz):
        return (X0 + px * ss, Y0 + pz * ss)

    def T(q):                                             # module shapes: booklet mm from the cut's origin
        return (X0 + q[0] * kb, Y0 + q[1] * kb)

    gr = sd_["ground"]

    def g_at(s):
        return gr[max(0, min(len(gr) - 1, int(round(s / 0.5))))][1]

    def gy_mm(xm):
        return g_at(xm / km) * km
    i0_pic = sb_mark(B)                                  # v59 closing (G-R4-1): the texts from here on are the cut's own
    tags_ = []
    zn_ = p45_zones(sd_, crs, Lm)                         # v58 (G15): the use zones (also in the dry run: their tags)
    # v61: the zoom insets are gone (SON shows none; SITE target): no recording Board any more
    pid_ = (sd_.get("_p45") or {}).get("page")
    tsp_ = sd_.get("trees_sp") or []                     # v61 (G6-10): (species, source, inferred) per tree
    btsp_ = sd_.get("btrees_sp") or []
    if not dry:
        # ---- beyond the cut: the buildings as elevations (wall, a hipped roof by convention, outline), the near ones
        # clearly, paler with distance (far first), then the trees beyond
        # v56 (R2-B, G14 / U22, D8): the designed sky first (sf_sky, D8 default a: every section); then two depth
        # layers beyond the cut (near <= P45_NEAR_M, far), each on its OWN ground line through its houses' and trees'
        # surveyed bases (sf_back_profile, drawn as a faded silhouette like sf_topo_back), so no house or tree beyond
        # floats over the cut; houses as elevations with windows and a hipped roof (sf_back_house, M11 convention)
        y_sky = (ytop - Y0) / kb
        if SF_SKY_DEFAULT and y_sky > min(z for s, z in g) * km + 1.0:
            with B.kind("other", u"sky %s" % nm):          # v61 (G6-9)
                _p45_put(B, L, sf_sky(0.0, Lm * km, min(z for s, z in g) * km, y_sky, seed=len(nm) * 7 + int(Lm),
                                      cid=nm, birds=True), T, kb, 9)   # v58 (P04.2 / G15): one sky per cut, birds
        beyond = sd_.get("beyond") or []
        btrees = sd_.get("btrees") or []
        for li, near in ((2, False), (1, True)):           # far layer first
            hs_ = [h_ for h_ in beyond if (h_[5] <= P45_NEAR_M) == near]
            ts_ = [(j_, t_) for j_, t_ in enumerate(btrees) if (t_[5] <= P45_NEAR_M) == near]
            bases = [(h_[0] * km, h_[1] * km, h_[2] * km) for h_ in hs_] + \
                    [((t_[0] - 0.3) * km, (t_[0] + 0.3) * km, t_[1] * km) for j_, t_ in ts_]
            prof = sf_back_profile(bases, 0.0, Lm * km)
            if not prof:
                continue
            tb = 0.75 if li == 2 else 0.55                 # drawing rule: far paler (sf_topo_back's range)
            with B.kind("ground", u"beyond %s" % ("far" if li == 2 else "near")):
                _p45_put(B, L, [("poly", prof + [(Lm * km, zbot * km), (0.0, zbot * km)],
                                 _sec_mix(SEC["soil"], SEC["paper"], tb), None, 0.1),
                                ("line", prof, _sec_mix(SEC["ink2"], SEC["paper"], tb), 0.12)], T, kb, 14 - 2 * li)
            gyl = sf_gy(prof)
            for hi_, (a, b, zb_, zt_, cat, d, floors, annex, fabric, flags, fsrc) in enumerate(
                    sorted(hs_, key=lambda t_: -t_[5])):
                if b - a < 0.5 or zt_ - zb_ < 0.5:
                    continue
                fl_ = int(floors) if isinstance(floors, (int, float)) and floors >= 1 else None
                with B.kind("buildings", u"beyond %d.%d" % (li, hi_)):
                    _p45_put(B, L, sf_back_house(a * km, b * km, gyl, zt_ - zb_, km, layer=li, floors=fl_,
                                                 roof="flat" if annex else "hip", d_m=d), T, kb, 15 - 2 * li)
            for i, (j_, (s, zg, tr, lo, hi, d)) in enumerate(ts_):
                sp_ = (btsp_[j_] if j_ < len(btsp_) else None) or (None, None, False)
                p45_tree_n(pid_, sp_[0])
                with B.kind("trees", u"%s b%d" % (sp_[0] or "tree", j_)):   # v61 (G6-9 / G6-10): species named
                    if p45_tree(B, L, T, kb, sp_[0], s * km, sf_ground_fn(gyl, 0.3 * km), km, hi,
                                max(1.5, 2.0 * tr), i, beyond=True, layer=li, order=15 - 2 * li):
                        p45_tree_n(pid_, None, out=True)   # v56: paler with depth (Aras 31 Oct 11:24)
        # ---- the cut ground: v58 (P04.2 / G15): through sct_ground (the soil gradient, topsoil dark at the surface,
        # lighter with depth, and the earth hatch over it) along the whole cut; its own cut line left out ([:-1]: the
        # page draws the cut line below, broken inside the cut buildings). No flat ground fill here.
        if len(g) >= 2:
            with B.kind("ground", u"cut ground"):          # v61 (G6-9)
                _p45_put(B, L, sct_ground([(s * km, z * km) for s, z in g], zbot * km, km, "earth")[:-1], T, kb, 20)
        for ci_, cr in enumerate(crs):
            if not cr["along"]:
                for sd in cr["sides"]:
                    side = 1.0 if sd["dirn"] > 0 else -1.0
                    with B.kind("ground", u"bank %d %s" % (ci_, sd["side"])):
                        if sd["typ"] == "dsi_wall":
                            sh, _ = sct_bank("dsi_wall", sd["x"] * km, sd["zt"] * km, cr["zb"] * km, side, km,
                                             t_m=P45_WALL_T_M * cr["f"], reach_m=0.3, depth_m=1.0)
                            _p45_put(B, L, sh, T, kb, 24)
                        elif sd["typ"] == "embankment" and sd["crest"] is not None and sd["zt"] is not None \
                                and abs(sd["crest"] - sd["x"]) > 0.2:
                            sh, _ = sct_bank("embankment", sd["x"] * km, sd["zt"] * km, cr["zb"] * km, side, km,
                                             run_m=abs(sd["crest"] - sd["x"]), reach_m=0.3, depth_m=1.0)
                            _p45_put(B, L, sh, T, kb, 24)
            with B.kind("water", u"stream %d" % ci_):
                _p45_put(B, L, p45_water(sd_, cr, g, km, base), T, kb, 23)
            # the level shelves (terraces) the level module finds on the banks (a cut across the stream only)
            c_ = 0.5 * (cr["a"] + cr["b"])
            for t_ in ([] if cr["along"] else (level_cut(cr["rid"]).get("terraces") or [])):
                lv = (t_.get("level") or {}).get("value")
                sd = next((q_ for q_ in cr["sides"] if q_["side"] == t_.get("side")), None)
                if lv is None or sd is None:
                    continue
                sa_, sb_ = [c_ + sd["dirn"] * m_ * cr["f"] for m_ in (t_.get("from_m", 0.0), t_.get("to_m", 0.0))]
                if 0.0 <= min(sa_, sb_) and max(sa_, sb_) <= Lm:
                    with B.kind("ground", u"terrace %d %s" % (ci_, t_.get("side"))):
                        B.line([P(sa_, lv - base), P(sb_, lv - base)], INK, L, 26, bk_lw(0.35, kb))
        # v61 (round 5 open row): a bridge only where the cut crosses one (p45_bridges): its deck over the stream at
        # the higher of the drawn grounds at its ends (no deck level in the data), P45_BRIDGE_T_M thick, railings
        for bi_, (b0_, b1_) in enumerate(p45_bridges(S, sd_)):
            dz_ = max(g_at(b0_), g_at(b1_))
            xa_, xb_ = b0_ * km, b1_ * km
            dy_, rl_ = dz_ * km, SF_RAIL_H * km if "SF_RAIL_H" in globals() else 1.10 * km
            with B.kind("roads", u"bridge %d" % bi_):
                _p45_put(B, L, [("poly", [(xa_, dy_ - P45_BRIDGE_T_M * km), (xb_, dy_ - P45_BRIDGE_T_M * km),
                                          (xb_, dy_), (xa_, dy_)], _sec_mix(SEC["ink2"], SEC["paper"], 0.35),
                                 SEC["ink2"], 0.18),
                                ("line", [(xa_ + 0.1 * km, dy_ + rl_), (xb_ - 0.1 * km, dy_ + rl_)], SEC["ink2"], 0.15),
                                ("line", [(xa_ + 0.1 * km, dy_), (xa_ + 0.1 * km, dy_ + rl_)], SEC["ink2"], 0.15),
                                ("line", [(xb_ - 0.1 * km, dy_), (xb_ - 0.1 * km, dy_ + rl_)], SEC["ink2"], 0.15)],
                         T, kb, 29)
        # ---- cut buildings: each down to its lowest ground (no building floats over a slope), its type's profile
        # (a civic hall: the M11 cut profile, walls, slab, windows, parapet), its tag in m
        for bi_, (a, b, z0, z1, cat, annex, ftype, fl, floors, fsrc) in enumerate(sd_["bld"]):
            kd_ = B.kind("heritage" if ftype in ("monument", "sacred") else "buildings", u"cut %d" % bi_)
            kd_.__enter__()                              # v61 (G6-9): one element per cut building
            try:
                zlo = min([z0] + [z for s, z in gr if a <= s <= b])
                r0, r1 = P(a, zlo), P(b, z1)
                if b - a < 1.2:
                    B.fill([rect(r0[0], r0[1], r1[0], r1[1])], SEC_WALL, L, 28)
                    continue
                heritage = ftype in ("monument", "sacred")
                wall_c = mix(FABRIC[ftype][2], INK, 0.45) if heritage else INK
                if typo_kind(ftype, cat) == "large" and z1 - z0 > 0.5:
                    if z0 - zlo > 0.05:                      # the plinth down to the lowest ground under it
                        B.fill([rect(r0[0], r0[1], r1[0], P(b, z0)[1])], SEC_WALL, L, 27)
                    _p45_items(B, L, bld_section_profile(a, b, z0, z1 - z0, floors, roof="flat"), P, kb, 27)
                    prof = dict(body=[(a, z0), (b, z0), (b, z1 + 0.6), (a, z1 + 0.6)], roof=None)
                else:
                    room = mix(typo_tone(ftype, cat), PAPER, 0.12 + (0.15 if annex else 0.0))
                    prof = bld_profile(ftype, cat, a, b, zlo, z0, z1, floors, fsrc == "published", seed=int(a * 7.0),
                                       ruin=fl[2], minaret=fl[3] if len(fl) > 3 else None)
                    bld_draw_cut(B, L, P, prof, room, wall_c, ss, U, order=27)
                lab_ = None if annex else _p45_tag(ftype, cat, floors, fl, z1 - z0, (b - a) * ss, hm)
                if lab_:
                    top_ = max(z for s_, z in (prof["roof"] or prof["body"]))
                    qx = P(0.5 * (a + b), top_)[0]
                    hw_ = 0.5 * site28_tw(lab_, hm) + 1.2 * kb      # a clear gap of over 2 mm between two tags
                    if not any(x0_ < qx + hw_ and qx - hw_ < x1_ and abs(y_ - P(0, top_)[1]) < 1.6 * hm
                               for x0_, x1_, y_ in tags_):
                        site28_bld_tag(B, L, P, prof, lab_, hm, wall_c, U, tags_)
            finally:
                kd_.__exit__()
        for x0_, x1_, y_ in tags_:                       # v58 (G3): the tags' boxes (site28_bld_tag: baseline y + 0.12 U)
            _p45_tb(x0_ + 0.15 * U, x1_ - 0.15 * U, y_ + 0.12 * U, hm)
        # ---- the cut line, broken inside the cut buildings
        spans = sorted((a, b) for a, b, z0, z1, cat, annex, ftype, fl, floors, fsrc in sd_["bld"])
        run = []
        with B.kind("ground", u"cut line"):                # v61 (G6-9)
            for s, z in g:
                if any(a_ + 0.01 < s < b_ - 0.01 for a_, b_ in spans):
                    if len(run) >= 2:
                        B.line(run, INK, L, 26, bk_lw(0.35, kb))
                    run = []
                    continue
                run.append(P(s, z))
            if len(run) >= 2:
                B.line(run, INK, L, 26, bk_lw(0.35, kb))
        for wi_, (s, zg) in enumerate(sd_["walls"]):     # a surveyed wall: its place on the ground (no height);
            with B.kind("ground", u"wall %d" % wi_):     # v56: [] (U22, walls off)
                _p45_put(B, L, sf_wall_mark(s * km, zg * km, 1.0, fill=SEC["ink2"]), T, kb, 28)
        # ---- planting at true size (02 §4): the measured trees on the cut; olive rows where the survey shows them
        # v61 (G6-10): each tree's species from sb_tree_species (sec["trees_sp"]), else generic; measured height kept
        for i, (s, zg, hw, lo, hi) in enumerate(sd_["trees"]):
            sp_ = (tsp_[i] if i < len(tsp_) else None) or (None, None, False)
            p45_tree_n(pid_, sp_[0])
            with B.kind("trees", u"%s %d" % (sp_[0] or "tree", i)):
                if p45_tree(B, L, T, kb, sp_[0], s * km, sf_ground_fn(gy_mm, 0.3 * km), km, hi,
                            max(1.5, 2.0 * hw), i, beyond=True, order=32):
                    p45_tree_n(pid_, None, out=True)
            # v56 G14: seated; v58 (G15): true size but in the paler tone, so the people in front lead
        for a, b, cat in p45_segments(sd_, 4.0):
            if cat != "agri" or b - a < 10.0:
                continue
            if p45_olives(S, sd_, a, b):
                with B.kind("fields", u"olive rows %.0f" % a):
                    _p45_put(B, L, pla_crop_rows("olive", a * km, b * km, sf_ground_fn(gy_mm, 0.3 * km), km),
                             T, kb, 32)
            elif not sd_.get("_p45_nocrop"):
                sd_["_p45_nocrop"] = True
                LOG.append(u"Section {}: farmland on the cut with no crop in the survey or OpenStreetMap: drawn as "
                           u"field ground only (no rows).".format(nm))
        # ---- figures where people are (02 §3; v56 G14 + G10): at each bank top one person looking at the water, its
        # feet on the lowest cut ground under them (sf_seat_x, never on a wall top in the air); on the streets the cut
        # crosses (the three widest, >= 4 m) people by the walkway set (fig_place_zones: walk, adult with child, a
        # group, watch; varied, seated), at true height (1.75 m), in the booklet's one human style (P45_FIG_STYLE,
        # Aras 31 Oct 11:24: the same style everywhere; cutouts without see-through insides are the module's pick)
        # v58 (round 3, G15): people lead, in front of the trees (order 34 over 32), by zone (fig_place_zones, every
        # figure seated on the drawn cut ground): at each bank top across the stream a water_edge strip P45_EDGE_M
        # wide (fishing, watching, touching; water = that crossing's average-flow level, so the line reaches the
        # water and nobody stands in it); on the streets the cut crosses walkways (walk, run, dog walk, groups); on
        # open ground within P45_LAWN_M of a bank a lawn (lying, dogs, play). Street elements only on those streets
        # (p45_street_kit).
        gyd = sf_gy([(s * km, z * km) for s, z in g])     # the drawn cut ground (banks and walls as drawn)
        ink_f = mix(INK, PAPER, 0.2)

        def foc_(_k, xa_, xb_):                          # v57 (R2-C focus): the near water, else each other
            m_ = 0.5 * (xa_ + xb_) / km
            w_ = [0.5 * (cr["a"] + cr["b"]) for cr in crs if not cr["along"] and
                  min(abs(cr["a"] - m_), abs(cr["b"] - m_)) <= P45_FOCUS_WATER_M]
            return (min(w_, key=lambda c_: abs(c_ - m_)) if w_ else m_) * km
        edges_, walks_, lawns_ = zn_
        for ci, cr in enumerate(crs):
            av_ = level_avg_flow(cr["rid"])
            ez_ = [("water_edge", e0 * km, e1 * km, gyd) for c2, e0, e1, sd in edges_ if c2 == ci]
            if ez_:
                sh_, placed_ = fig_place_zones(ez_, gyd, km, seed=len(nm) * 13 + ci, style=P45_FIG_STYLE,
                                               density=0.6, max_per_zone=2, ink=ink_f, focus=foc_,
                                               water=(av_ - base) * km if av_ is not None else None)
                with B.kind("people", u"bank edge %d" % ci):  # v61 (G6-9)
                    _p45_put(B, L, sh_, T, kb, 34)
        zones_ = sorted([("walkway", a * km, b * km) for a, b in walks_] +
                        [("lawn", a * km, b * km) for a, b in lawns_], key=lambda z_: z_[1])
        if zones_:
            sh_, placed_ = fig_place_zones(zones_, gyd, km, seed=len(nm) * 13, style=P45_FIG_STYLE, density=0.6,
                                           max_per_zone=2, ink=ink_f, focus=foc_)
            with B.kind("people", u"streets and lawns"):
                _p45_put(B, L, sh_, T, kb, 34)
        with B.kind("roads", u"street kit"):
            _p45_put(B, L, p45_street_kit(walks_, [(e0, e1, sd) for c2, e0, e1, sd in edges_], crs, gyd, km),
                     T, kb, 33)
        # v59 (round 4, G-R4-5.2 / D7): the low layer of shrubs and flowers (plants.py PLA_LOW, by wetness) on the
        # bank edges (wet end, never below the crossing's water) and on the open ground near the banks (dry end),
        # behind the people (order 33 under 34)
        for ci, c2, e0, e1, sd in [(i_, q_[0], q_[1], q_[2], q_[3]) for i_, q_ in enumerate(edges_)]:
            av_ = level_avg_flow(crs[c2]["rid"]) if c2 < len(crs) else None
            sh_, _pl = pla_low_section(min(e0, e1) * km, max(e0, e1) * km, gyd, km, t0=0.0, t1=0.45,
                                       seed=len(nm) * 17 + ci, density=1.0,
                                       water=(av_ - base) * km if av_ is not None else None)
            with B.kind("plants", u"bank edge %d" % ci):
                _p45_put(B, L, sh_, T, kb, 33)
        for li_, (a, b) in enumerate(lawns_):
            sh_, _pl = pla_low_section(a * km, b * km, gyd, km, t0=0.55, t1=1.0, seed=len(nm) * 19 + li_,
                                       density=0.8)
            with B.kind("plants", u"lawn %d" % li_):
                _p45_put(B, L, sh_, T, kb, 33)
        # v59 (round 4, G-R4-5.4, U44): bed, mean flow, Q100 and Q500 of the main crossing as marks OUTSIDE the
        # drawing's right edge (sf_level_marks: tick, open inverted triangle, value), nothing across the picture
        # v59 (round 4 closing, G-R4-5.4 / checklist 2): the tallest cut roof's level is one more of these marks
        # (was a filled triangle and its value inside the picture at the eaves)
        k_m = site28_main_k(sd_)
        cm_ = next((c2 for c2 in crs if c2["k"] == k_m and not c2["along"]), None) or \
            next((c2 for c2 in crs if not c2["along"]), None)
        lv_ = []
        if cm_ is not None:
            lv_ = [(kk, level(cm_["rid"], kk)) for kk in ("q500", "q100")] + \
                [("avg", level_avg_flow(cm_["rid"])), ("bed", cm_["bed"])]
        if sd_["bld"]:
            lv_.append(("roof", max(t_[3] for t_ in sd_["bld"]) + base))
        lv_ = [(kk, v_) for kk, v_ in lv_ if v_ is not None]
        if lv_:
            # v61 (frames §4 page5: S5 / S7 / S8 piles): every value at the right edge, spread, never stacked
            fb_ = (0.0, zbot * km, (x + wd - X0) / kb, (ytop - Y0) / kb)
            with B.kind("levels", u"levels %s" % nm):
                _p45_put(B, L, p45_level_marks(fb_, lv_, y_of=lambda lev: (lev - base) * km,
                                               cols={"roof": crop_hex(INK)}, page=pid_, nm=nm,
                                               xmax=(x + P45_DRAW_MM * kb - X0) / kb), T, kb, 37)
    with B.kind("roads", u"streets %s" % nm):           # v61 (G6-9): the streets the cut crosses
        road_calls = draw_sec_roads(S, B, L, P, g_at, sd_["line"], Lm, U, off=off)   # v25: the streets crossed
    # ---- the ends: name over its level, outside the cut (a cropped end: a break, its level only)
    co = sd_.get("crop_of")
    e0_, e1_ = cut_end_labels(nm)                        # v58 (D6): "S4" / "S4'"
    # v61 (frames §4: "+118.87" / "+71.38" / "+48.87" struck by the ground line, "+50.18" on the "S2" tag): the
    # level 1.5 mm out from the end and wholly over its ground point (P45_END_LIFT), the name a text height over it
    for s_, lab, out in ((0.0, e0_, -1.0), (Lm, e1_, 1.0)):
        real = not co or (s_ == 0.0 and co[1] <= 0.01) or (s_ == Lm and co[1] + Lm >= co[0] - 0.01)
        bx, by = P(s_, g[0][1] if s_ == 0.0 else g[-1][1])
        t_ = u_level(g_at(s_) + base)
        xa = bx + out * 1.5 * kb
        yl_ = by + P45_END_LIFT * hm
        with B.kind("levels", u"end %s" % lab):
            _p45_tb(*(site28_text(B, t_, xa, yl_, hm, INK, L, align="L" if out > 0 else "R") + (yl_, hm)))
        if real:
            with B.kind("labels", u"end %s" % lab):
                _p45_tb(*(site28_text(B, u"**{}**".format(lab), xa, yl_ + 2.0 * hm, hd, INK, L,
                                      align="L" if out > 0 else "R") + (yl_ + 2.0 * hm, hd)))
        else:
            with B.kind("cuts", u"break %s" % lab):
                B.line([(bx - 0.6 * kb, by - 2.0 * kb), (bx + 0.6 * kb, by - 0.7 * kb),
                        (bx - 0.6 * kb, by + 0.7 * kb), (bx + 0.6 * kb, by + 2.0 * kb)], INK2, L, 36, bk_lw(0.18, kb))
    # v59 (round 4 closing, G-R4-5.4): the tallest cut roof's level is a level mark outside the frame (above); the
    # filled triangle inside the picture is gone
    # ---- the segmented strip (R02): what the cut crosses, each segment exactly under its part of the cut
    ys = P(0.0, zbot)[1] - 0.6 * kb
    hb = max(1.9 * hst, 2.6 * kb)
    for si_, (a, b, cat) in enumerate(p45_segments(sd_, 1.2 / km)):
        xa_, xb_ = P(a, 0)[0], P(b, 0)[0]
        col = C(p45_cat_hex(cat))                        # v61 (G6-6, H1): the hue table, as the legend
        w_ = P45_STRIP_WORD.get(cat, cat)
        with B.kind(p45_kind_of(cat), u"strip %d %s" % (si_, w_)):   # v61 (G6-9): strip as ground / fields
            B.fill([rect(xa_, ys - hb, xb_, ys)], col, L, 20)
            B.line([(xb_, ys - hb), (xb_, ys)], WHITE, L, 21, bk_lw(0.25, kb))
        if xb_ - xa_ > site28_tw(w_, hst) + 1.2 * kb:
            dark = sum(col[:3]) < 420
            with B.kind("labels", u"strip %d %s" % (si_, w_)):
                B.text(w_, 0.5 * (xa_ + xb_), ys - 0.5 * (hb + hst), hst, WHITE if dark else INK, L, order=22,
                       font=FONT_TITLE, align="C")
            _p45_tb(0.5 * (xa_ + xb_ - site28_tw(w_, hst)), 0.5 * (xa_ + xb_ + site28_tw(w_, hst)),
                    ys - 0.5 * (hb + hst), hst)
    # ---- v58 (round 3, P04.1 / G3 / G4): the street names and levels as compact tags in ONE row under the strip
    # (p45_band): the water and banks (level module) first, then terraces and history, then streets and places;
    # a tag with no room is a numbered disc on its spot, its words in the key beside the cut (sd_["_p45key"]).
    # Levels and heights in m with 2 decimals, widths in cm. The stream at each crossing is the project: no text on it.
    calls = []
    for cr in crs:
        if P45_COLLECT[0] and not dry:
            sl, sr = cr.get("win", (cr["a"], cr["b"]))
            ztop_ = max([cr["zb"] + 0.5] + [sd["zt"] for sd in cr["sides"] if sd["zt"] is not None] +
                        [q_ - base for q_ in (level(cr["rid"], "q500"), level_avg_flow(cr["rid"])) if q_ is not None])
            (wx0, wy0), (wx1, wy1) = P(max(0.0, min(cr["a"], sl)), cr["zb"]), P(min(Lm, max(cr["b"], sr)), ztop_)
            if wx1 > wx0:                                # v59 closing (G-R4-1): the stream at the crossing is the
                sb_keep(B, (wx0, wy0, wx1, wy1), u"%s stream" % nm, "water")   # project: NO text on it (none own)
        # v59 (round 4, P04.2 / G-R4-2 / G-R4-5.4): only what matters: the banks at each crossing (one marker),
        # important places, named streets where they fit. The bed, the mean flow and the flood levels are level
        # marks outside the frame now; terraces are drawn (their line) and not numbered; lawns, generic streets and
        # the zones row are gone
        if not cr["along"]:
            bt = [(sd, p45_bank_word(sd)) for sd in cr["sides"]]
            if len(bt) == 2 and bt[0][1] and bt[0][1] == bt[1][1]:    # two equal banks: one callout
                sd = bt[1][0]
                sx = sd["crest"] if sd["crest"] is not None else sd["x"]
                calls.append((sx, sd["zt"] if sd["zt"] is not None else g_at(sx), bt[0][1] + u" · both banks", 0))
            else:
                for sd, t_ in bt:
                    if t_:
                        sx = sd["crest"] if sd["crest"] is not None else sd["x"]
                        calls.append((sx, sd["zt"] if sd["zt"] is not None else g_at(sx), t_, 0))
    for s_, z_, t_ in road_calls:
        c2 = site28_road_call(t_)
        if c2[1] <= 2:                                   # v59: named streets only
            calls.append((s_, z_, c2[0], c2[1]))
    calls += [(s_, g_at(s_), t_, 1) for s_, t_ in sec_history_calls(S, sd_) if 0.0 <= s_ <= Lm]
    with B.kind("labels", u"tags %s" % nm):            # v61 (G6-9): the tags and discs under the strip
        low, sd_["_p45key"] = p45_band(B, L, P, calls, ys - hb - 0.8 * kb, kb, hst, x, x + wd)
    if P45_COLLECT[0] and not dry:                       # v59 closing (G-R4-1): the cut's picture (its frame, as the
        sb_keep(B, (x, Y0 + zbot * ss, x + wd, ytop), u"%s section" % nm, "section", i0_pic)   # level marks')
    return min(low - 0.4 * hst, ys - hb) - 0.8 * kb      # v58: under the discs' foot (0.35 x h under the baseline)


def p45_free(a, b, taken):
    """v58 (G15): the parts of a..b (m along the cut) that no interval of taken [(a, b)] covers, left to right"""
    out = [(a, b)] if b > a else []
    for t0, t1 in taken:
        nxt = []
        for u0, u1 in out:
            if t1 <= u0 or t0 >= u1:
                nxt.append((u0, u1))
                continue
            if t0 > u0:
                nxt.append((u0, t0))
            if t1 < u1:
                nxt.append((t1, u1))
        out = nxt
    return out


def p45_street_kit(walks, edges, crs, gy, km):
    """v58 (round 3, G15): street elements only on the streets the cut crosses (walks [(a, b)] m along the cut, clear
    of the channel and the bank edges), each for a reason (sizes SF_STREET: drawing rules, never printed as data):
    a lamp at each street 4 m or wider, at its kerb away from the water (the street is lit); a bollard at a street end
    within P45_BOLLARD_M of a bank-top edge (edges [(e0, e1, side)] m; keeps cars off the bank edge); one bike rack
    on the street nearest a crossing, when within P45_FOCUS_WATER_M of it (bikes left where people stop at the
    water). gy: the drawn ground (mm), km mm per m. Returns shapes (mm from the cut's origin)."""
    sh = []
    if not walks:
        return sh

    def y_(xm):
        return sf_seat_x(gy, xm, 0.2 * km)
    cent = [0.5 * (cr["a"] + cr["b"]) for cr in crs if not cr["along"]]
    for a, b in walks:
        near_a = any(min(abs(a - e0), abs(a - e1)) <= P45_BOLLARD_M for e0, e1, sd in edges)
        near_b = any(min(abs(b - e0), abs(b - e1)) <= P45_BOLLARD_M for e0, e1, sd in edges)
        for end_, inward, hit in ((a, 1.0, near_a), (b, -1.0, near_b)):
            if hit:
                xb = (end_ + inward * 0.3) * km
                sh += sf_bollard(xb, y_(xb), km)
        if b - a >= 4.0:
            wa = min([abs(a - c) for c in cent] or [1e9])
            wb = min([abs(b - c) for c in cent] or [1e9])
            xl, sl_ = ((b - 0.6) * km, -1) if wa < wb else ((a + 0.6) * km, 1)   # the kerb away from the water
            sh += sf_lamp(xl, y_(xl), km, side=sl_)
    if cent:
        best = min(walks, key=lambda w: min(abs(0.5 * (w[0] + w[1]) - c) for c in cent))
        c = min(cent, key=lambda c_: abs(0.5 * (best[0] + best[1]) - c_))
        if best[1] - best[0] >= 3.0 and min(abs(best[0] - c), abs(best[1] - c)) <= P45_FOCUS_WATER_M:
            xr, sr_ = ((best[1] - 1.0) * km, -1) if abs(best[1] - c) < abs(best[0] - c) else ((best[0] + 1.0) * km, 1)
            sh += sf_bike_rack(xr, y_(xr), km, side=sr_)
    return sh


def p45_zones(sd_, crs, Lm):
    """v58 (round 3, G15): a cut's use zones in m along it: (edges [(crossing index, s0, s1, bank side dict)]: the
    bank-top strip P45_EDGE_M wide beside each crossing across the stream; walks [(s0, s1)]: the three widest streets
    (>= 4 m) clear of the channels and the edges; lawns [(s0, s1)]: open or green ground within P45_LAWN_M of a bank,
    clear of the rest). Nobody in a channel."""
    taken = [cr.get("win", (cr["a"], cr["b"])) for cr in crs]
    edges = []
    for ci, cr in enumerate(crs):
        if cr["along"]:
            continue
        for sd in cr["sides"]:
            if sd["crest"] is None:
                continue
            e0 = sd["crest"] + sd["dirn"] * 0.5
            e1 = sd["crest"] + sd["dirn"] * (0.5 + P45_EDGE_M)
            e0, e1 = max(0.0, min(e0, e1)), min(Lm, max(e0, e1))
            if e1 - e0 >= 1.0:
                edges.append((ci, e0, e1, sd))
                taken.append((e0, e1))
    st_ = sorted([sg for sg in p45_segments(sd_, 2.0) if sg[2] == "transport" and sg[1] - sg[0] >= 4.0
                  and not any(sg[0] < cr["b"] and cr["a"] < sg[1] for cr in crs)],   # never in the channel (Aras 11:28)
                 key=lambda q_: q_[0] - q_[1])[:3]
    walks = [q_ for a, b, cat in sorted(st_) for q_ in p45_free(a, b, taken) if q_[1] - q_[0] >= 2.0]
    lawns = []
    for a, b, cat in p45_segments(sd_, 2.0):
        if cat not in ("void", "green"):
            continue
        for cr in crs:
            if cr["along"]:
                continue
            sl, sr = cr.get("win", (cr["a"], cr["b"]))
            for a2, b2 in ((max(a, sl - P45_LAWN_M), min(b, sl)), (max(a, sr), min(b, sr + P45_LAWN_M))):
                lawns += [q_ for q_ in p45_free(a2, b2, taken + walks + lawns) if q_[1] - q_[0] >= 3.0]
    return edges, walks, lawns




def p45_band(B, L, P, calls, ytop, kb, lh, xlo, xhi, zcalls=()):
    """v58 (round 3, P04.1 / G3 / G4): a cut's street names and levels as compact tags in ONE row from ytop down,
    under the strip (no stacked rows, no leaders): calls [(s, z, text, priority)] (0 the water: first; 1 banks'
    terraces and history; 2 named streets; 3 other streets and places) each centred under its spot (kept between xlo
    and xhi, its spot inside it) where it clears the tags before it; a tag with no room becomes a numbered disc on its
    spot (or the nearest free place within 4 mm), numbered in the page's reading order (P45_NUM: left to right, cut
    after cut) and listed in the key beside the cut (p45_head). Board units; lh = capital height.
    zcalls (v58, G15 / R07): the use zones' tags [(s, z, text, 4)] ("bank edge · fishing, watching"): a second row
    under the first (ink2) when every one of them fits there under its spot; else folded into the first row (last
    priority). Returns (lowest baseline, [(n, text)])."""
    base_y = ytop - lh
    gap = 1.5 * kb
    row2 = []
    for s, zf, txt, pr in sorted(zcalls, key=lambda q: q[0]):
        fx = P(s, zf)[0]
        w_ = site28_line_w(site28_one(txt, lh), lh)
        half = 0.5 * w_
        cx = min(max(fx, xlo + half), xhi - half)
        if w_ > xhi - xlo or not cx - half <= fx <= cx + half or \
                any(cx - half < r_ + gap and l_ - gap < cx + half for l_, r_, c_, t_ in row2):
            calls, row2 = list(calls) + list(zcalls), []      # no room: fold the zones into the first row
            break
        row2.append((cx - half, cx + half, cx, txt))
    placed, texts, nums = [], [], []
    for s, zf, txt, pr in sorted(calls, key=lambda q: (q[3], q[0])):
        fx = P(s, zf)[0]
        w_ = site28_line_w(site28_one(txt, lh), lh)
        half = 0.5 * w_
        cx = min(max(fx, xlo + half), xhi - half)
        if w_ <= xhi - xlo and cx - half <= fx <= cx + half and \
                not any(cx - half < r_ + gap and l_ - gap < cx + half for l_, r_ in placed):
            placed.append((cx - half, cx + half))
            texts.append((cx, txt))
        elif pr <= 1:                                    # v59 (P04.2): a number only for what matters
            nums.append((fx, txt))
        else:
            LOG.append(u"Sections: tag '{}' left out (no room; named streets are tags only)".format(txt))
    r = 1.15 * lh                                        # v59: the shared marker's radius (two digits), board units
    key = []
    for fx, txt in sorted(nums, key=lambda q: q[0]):
        cx = None
        for d in [0.0] + [sg * j * 0.5 * kb for j in range(1, 41) for sg in (1.0, -1.0)]:   # v59: within 20 mm
            q = min(max(fx + d, xlo + r), xhi - r)
            if not any(q - r < r_ + gap and l_ - gap < q + r for l_, r_ in placed):   # v61 (frames §4: the
                #                               stray disc after "loose earth bank · top +49.74"): a tag's gap clear
                cx = q
                break
        if cx is None:                                   # v59: never piled on another (P04.2): left out, logged
            LOG.append(u"FLAG sections: marker '{}' left out (no free place within 20 mm of its spot)".format(txt))
            continue
        P45_NUM[0] += 1
        placed.append((cx - r, cx + r))
        _p45_disc(B, L, P45_NUM[0], cx, base_y, lh)
        key.append((P45_NUM[0], txt))
    for cx, t_ in texts:
        _p45_tb(*(site28_text(B, t_, cx, base_y, lh, INK, L, align="C") + (base_y, lh)))
    if row2:                                             # the zones' row, under the discs' foot
        base_y -= 1.9 * lh
        for l_, r_, cx, t_ in row2:
            _p45_tb(*(site28_text(B, t_, cx, base_y, lh, INK2, L, align="C") + (base_y, lh)))
    return base_y, key


def p45_olives(S, sd_, a, b):
    """True where the cut's farmland a..b is an olive grove in the data: the survey's olive symbols on it (within
    15 m of the cut) or an OpenStreetMap orchard tagged with olive trees"""
    if any(kind == "olive" and a <= s <= b and abs(d) <= 15.0 for s, d, kind in p45_symbols(S, sd_)):
        return True
    x0, y0, x1, y1 = sd_["line"][:4]
    Lc = math.hypot(x1 - x0, y1 - y0) or 1.0
    sm = 0.5 * (a + b)
    mx, my = x0 + (x1 - x0) * sm / Lc, y0 + (y1 - y0) * sm / Lc
    for z in S.g_agri.query((mx - 1.0, my - 1.0, mx + 1.0, my + 1.0)):
        if (z.get("tags") or {}).get("trees") == "olive_trees" and region_contains(mx, my, z["Ps"], z.get("Hs") or []):
            return True
    return False


def sec_history_calls(S, sd_):
    """v44 (PHASE2_SPEC §3, p.7-8): where a cut crosses the survey's historic city wall line (layer SINIR_TARIHI_SUR,
    S.walls_hist) or the covered course of the stream (OSM tunnel / culvert, S.covered): [(s, text)] along the cut.
    Only what the data holds: the survey layer does not date the wall, so no period is named."""
    x0, y0, x1, y1, nm = sd_["line"]
    Lc = math.hypot(x1 - x0, y1 - y0)
    if Lc <= 0:
        return []
    out = []
    for key, txt in (("walls_hist", u"historic city wall"), ("covered", u"covered stream")):
        for P in getattr(S, key, None) or []:
            for a, b in zip(P[:-1], P[1:]):
                hit = seg_x((x0, y0), (x1 - x0, y1 - y0), a, (b[0] - a[0], b[1] - a[1]))
                if hit:
                    s_ = hit[0] * Lc
                    if all(abs(s_ - q) > 3.0 or t_ != txt for q, t_ in out):
                        out.append((s_, txt))
    return out



def p45_crop(S, sd_, Lmax):
    """the part of a cut Lmax m long around its stream (sec_cropped), once per run"""
    memo = getattr(S, "_p45_crop", None)
    if memo is None:
        memo = {}
        S._p45_crop = memo
    key = (sd_["name"], round(Lmax, 1))
    if key not in memo:
        memo[key] = sec_cropped(S, sd_, Lmax)
        if sd_.get("p45_cross"):                         # v59 (N4 b): the crop keeps S5's one level row
            memo[key]["p45_cross"] = sd_["p45_cross"]
    return memo[key]


def p45_bar_h(kb, U):
    """the height of a cut's scale bar with its numbers (board units)"""
    return 0.38 * U + 0.35 * U + bk_hk(P45_TXT["minor"], kb) + 0.6 * kb


def p45_bar(B, x, y, w, ss, sd_, kb, U, L="LU_BOARD::Sections"):
    """a cut's scale bar (02 §8), its foot at y, in metres (0, half, length, "m"): geometry of the drawing, so it is
    true at whatever scale the booklet prints the cut. v61 (U20 / P-7, frames §6 "1:2,500 under the cut vs 1:2,000 on
    the bar"): NO ratio printed here any more (it printed the sheet ratio crop_scale(ss), 1:2,000, while the booklet
    set the cut at 1:2,500 and printed that under it): the bar sits under the drawing's left end, so the booklet's
    one "1:N" under the drawing (the true printed scale) is the value next to its bar"""
    hm = bk_hk(P45_TXT["minor"], kb)
    sb = nice_floor(max(1.0, min(sd_["L"] / 4.0, 0.5 * w / ss)))
    with B.kind("annotations", u"scale bar %s" % sd_["name"]):
        draw_scalebar(B, x, y, ss, sb, U, L, h=hm / U)
    if P45_COLLECT[0]:                                   # v58 (G3): the bar with its numbers as one text box
        P45_BOXES.append((x, y - 0.25 * hm, x + sb * ss + 0.9 * U + site28_tw(u"m", hm),
                          y + p45_bar_h(kb, U) - 0.6 * kb))


def p45_head(S, B, sd_, x, y, w, kb, U, L="LU_BOARD::Sections"):
    """the note beside a cut: v61 (U20, PLAN §2.2 sb_sec_note_sN): its heading "SECTION Sn — Sn'" (one text group:
    note n1), then (one text group: note n2) its key sentence and what on it steers the project (site28_sec_reading,
    as SUBMISSION_SON prints it), the key of the cut's numbered band tags as "n words" (text only: no disc, so the
    note's crop stays text-only and is exported as note items), the public source of the bed as drawn (its width is
    never printed). Smaller text (P45_NOTE_PT, >= 4 pt). Every line's box noted for the overlap test. Returns the y
    below."""
    hd, hc, hm = [bk_hk(P45_NOTE_PT[q], kb) for q in ("head", "call", "minor")]
    # v59.1 (Aras 1 Nov 16:48 log): a block's lines and runs are ONE text group (the export makes one note of each)
    tg_ = getattr(B, "tgroup", None)
    e0_, e1_ = cut_end_labels(sd_["name"])
    yy = y - hd
    with B.kind("labels", u"note %s head" % sd_["name"]):
        if tg_:
            tg_()
        _p45_tb(*(site28_text(B, u"**SECTION {} — {}**".format(e0_, e1_), x, yy, hd, INK, L) + (yy, hd)))
        if tg_:
            tg_(False)
    yy -= 1.0 * hd + 1.0 * hc
    with B.kind("labels", u"note %s" % sd_["name"]):
        if tg_:
            tg_()
        key_, steer_ = site28_sec_reading(S, sd_)
        if key_:
            yy = _p45_para(B, key_, x, yy, w, hc, INK, L, lead=1.45, bcol=INK)
        if steer_:
            yy = _p45_para(B, steer_, x, yy, w, hc, INK2, L, lead=1.45, bcol=INK)
        # v58 (P04.1 / G3): the key of the numbered discs in the band under the cut, in their order
        for n_, t_ in sd_.get("_p45key") or []:
            yy = _p45_para(B, u"**{}** {}".format(n_, t_), x, yy, w, hm, INK, L, lead=1.45)
        srcs = []
        for cr in p45_banks(sd_):
            src = level_public_source(cr["rid"], "bed_width_cm")
            bw = level(cr["rid"], "bed_width_cm")
            if src and bw:
                t_ = u"Bed as drawn: {}".format(src)        # v60.2 (G-R5-4.6): its width is not printed
                if t_ not in srcs:
                    srcs.append(t_)
        for t_ in srcs:
            yy = _p45_para(B, t_, x, yy - 0.2 * hc, w, hm, INK2, L, lead=1.4)   # v58: boxes noted (G3)
        if tg_:
            tg_(False)
    return yy + 0.4 * hc


def p45_title(B, sd_, x, y, w, kb, L="LU_BOARD::Sections"):
    """v59 (round 4, G-R4-3 LEFT template): the title strip over a cut's drawing, one line flush with the block's
    left edge (9 pt): "SECTION S1 — S1' · bazaar side → Kale side" (banks by place, D6), "· part around the stream"
    for a cropped cut; parts that do not fit the drawing's width are left out (the name always stays)"""
    hd = bk_hk(P45_TXT["head"], kb)
    e0_, e1_ = cut_end_labels(sd_["name"])
    t_ = u"SECTION {} — {}".format(e0_, e1_)
    extra = []
    crs_ = p45_banks(sd_)
    if crs_ and not all(c2["along"] for c2 in crs_):
        l_, r_ = p45_sides(sd_)
        extra.append(u"{} – {}".format(place_name("side_" + l_), place_name("side_" + r_)))   # v60 (P04.7): "→"
        #                                                    printed "?" (cp1252); the en dash is in every writer
    if sd_.get("crop_of"):
        extra.append(u"part around the stream")
    while extra and site28_line_w(site28_one(u"**%s · %s**" % (t_, u" · ".join(extra)), hd), hd) > w:
        extra.pop()
    if extra:
        t_ += u" · " + u" · ".join(extra)
    # v61 (frames §4 page4: the S4 subtitle ran into the "S4" tag): ONE bold run, so the booklet keeps it one line
    # (two runs were placed apart and the second wrapped under the first, onto the end tag)
    with B.kind("labels", u"title %s" % sd_["name"]):
        _p45_tb(*(site28_text(B, u"**%s**" % t_, x, y, hd, INK, L) + (y, hd)))


def p45_plan(S, sw, U):
    """v51 (WO-T3a-3, package A "fill the page"): the two sections pages (P45_PAGES: p04 S1-S4, p05 S5-S8), each at
    the largest round scale P45_DENS at which its cuts, the columns beside them and a key map at least P45_KEY_MIN
    tall fit the booklet panel (sw board units = BK_AW mm); a cut longer than the drawing column is cropped to the
    part around the stream (S5, S6 always may be; the others keep >= SEC_KEEP). Returns (dens, sss, pages, P):
    pages as sections_plan's ([[row of (cut, width)]]: the core's page count and names), P the pages' plans
    dict(den, ss, wd, wc, rows=[(cut, height)], need, names). Memoised per run."""
    memo = getattr(S, "_p45_plan", None)
    if memo and memo[0] == sw:
        return memo[1]
    kb = sw / BK_AW
    end = p45_end(kb)
    out = []
    for names in P45_PAGES:
        secs = [sd_ for nm in names for sd_ in S.sections if sd_["name"] == nm]
        if not secs:
            continue
        pick = None
        for den in P45_DENS:
            ss = kb * 1000.0 / den
            wd = (P45_DRAW_MM - P45_LEV_MM) * kb         # v61 (P-7): the drawing column (its level marks right of it
            #                                              fill P45_DRAW_MM: the cut's export at the frames' width)
            Lmax = (wd - 2.0 * end) / ss
            cuts, ok = [], True
            for sd_ in secs:
                if sd_["L"] <= Lmax:
                    cuts.append(sd_)
                elif sd_["name"] in P45_ALONG or sd_["L"] * P45_KEEP <= Lmax:
                    cuts.append(p45_crop(S, sd_, Lmax))
                else:
                    ok = False
                    break
            if not ok:
                continue
            wc = P45_COL_MIN * kb
            rows = []
            n0 = len(LOG)
            for c_ in cuts:
                c_["_p45"] = dict(k=kb, den=den, page=("p04", "p05")[len(out)] if len(out) < 2 else "p%02d" % (4 + len(out)))
                hs_ = -p45_strip(S, Board(), c_, 0.0, 0.0, wd, ss, kb, U, dry=True) + p45_bar_h(kb, U) + 1.0 * kb
                hh_ = -p45_head(S, Board(), c_, 0.0, 0.0, wc, kb, U)     # v61: the bar under the cut's left end
                rows.append((c_, max(hs_, hh_) + P45_TITLE_MM * kb))     # v59: + the title strip
            del LOG[n0:]
            need = sum(h_ for c_, h_ in rows) + len(rows) * P45_GAP * kb + P45_KEY_MIN * kb
            pick = dict(den=den, ss=ss, wd=wd, wc=wc, rows=rows, need=need, names=[c_["name"] for c_ in cuts])
            if need <= P45_H * kb:
                break
        if pick is None:
            LOG.append(u"WARNING: sections {}: no cut fits the page at 1:{:,}; page left out.".format(
                u", ".join(names), P45_DENS[-1]))
            continue
        if pick["need"] > P45_H * kb:
            LOG.append(u"WARNING: sections {}: {:.0f} mm tall at 1:{:,} (the panel holds {:.0f} mm).".format(
                u", ".join(pick["names"]), pick["need"] / kb, pick["den"], P45_H))
        LOG.append(u"Sections {} at 1:{:,} (WO-T3a-3: the largest round scale that fills the page).".format(
            u", ".join(pick["names"]), pick["den"]))
        out.append(pick)
    res = ([p["den"] for p in out], [p["ss"] for p in out], [[[(c_, sw)] for c_, h_ in p["rows"]] for p in out], out)
    S._p45_plan = (sw, res)
    return res


def draw_sections_page(S, B, x, y, sw, U, plan, k):
    """v51 (WO-T3a-3; package A p04-05): page k of the cuts (sw board units = BK_AW mm, P45_H tall). LANGUAGE: SITE
    (every cut; r06_S04: kept as drawn). v61 (round 6, U20 / P-7 / G6-5): no key map on the board (p45_keymap: the
    km_keymap v3 dict goes to the export, P45_KM[pid]), the legend in the hue table (P45_LEG[pid]); each cut
    (p45_strip) with its title over it, its level marks right of it and its scale bar under its left end is its own
    crop sec_sN, P45_DRAW_MM wide; its note (p45_head) beside it, level with it, is its own text-only crop
    sec_note_sN (exported as note items sb_sec_note_sN_n1..). plan is the core's (only its page count is used): the
    layout is p45_plan's. Returns the y below."""
    L = "LU_BOARD::Sections"
    pl = p45_plan(S, sw, U)
    if k >= len(pl[3]):
        LOG.append(u"Sections page {}: no cuts for it (p45_plan).".format(k + 1))
        return y
    pg = pl[3][k]
    kb = sw / BK_AW
    den, ss, wd, wc, rows = pg["den"], pg["ss"], pg["wd"], pg["wc"], pg["rows"]
    names = pg["names"]
    pid = ("p04", "p05")[k] if k < 2 else "p%02d" % (4 + k)
    B.text(u"SECTIONS ACROSS THE STREAM · {} · {}".format(u", ".join(names), pid), x, y, 0.9 * U,
           INK, L, font=FONT_TITLE, bold=True)          # on the sheet only (above the crops)
    # v58 (round 3, G3): the page's numbers start at 1 (reading order: cut after cut, left to right); every text box
    # placed from here on is noted (P45_BOXES)
    P45_NUM[0] = 0
    del P45_BOXES[:]
    P45_COLLECT[0] = True
    top = y - 1.3 * U
    H = P45_H * kb
    gap = P45_GAP * kb
    rows_h = sum(h_ for c_, h_ in rows) + len(rows) * gap
    extra = max(0.0, H - rows_h - P45_KEY_MIN * kb) / (len(rows) + 1.0)
    cats = []
    for c_, h_ in rows:
        for a, b, cat in p45_segments(c_, 1.2 * den / 1000.0):
            if cat not in cats:
                cats.append(cat)
    p45_keymap(S, pid, names)                            # v61 (G6-5): exported only (P45_KM), never drawn here
    p45_legend(pid, cats)                                # v61 (G6-6): P45_LEG in the hue table
    yy = top - gap - extra
    tri_ = sf_triangles(walls=False, aggregate=False)    # v56 (U22): no meaningless triangles in the cuts
    hd_ = bk_hk(P45_TXT["head"], kb)
    cx_ = x + (P45_DRAW_MM + P45_GAP) * kb               # v61: the note column right of the drawing
    for c_, h_ in rows:
        # LANGUAGE: SITE (r06_S04 target, kept as drawn)
        c_["_p45"] = dict(k=kb, den=den, page=pid)
        p45_title(B, c_, x, yy - hd_, wd, kb)
        yd = yy - P45_TITLE_MM * kb
        yl_ = p45_strip(S, B, c_, x, yd, wd, ss, kb, U)
        yb_ = yl_ - p45_bar_h(kb, U) + 0.6 * kb          # v61 (P-7): the bar under the cut's left end; the booklet
        p45_bar(B, x, yb_, 60.0 * kb, ss, c_, kb, U)     # prints the one scale value right under it
        yh_ = p45_head(S, B, c_, cx_, yd, wc, kb, U)
        ybot = min(yy - h_, yb_, yh_) - 0.3 * kb
        nm_ = c_["name"].lower()
        crop_panel("sec_%s" % nm_, x, ybot, x + P45_DRAW_MM * kb, yy + 0.3 * kb, u"", crop_scale(ss), ix_page=pid)
        CROP_PANELS[-1]["bk_w"] = P45_DRAW_MM            # drawn at its booklet width (text sizes as designed)
        crop_panel("sec_note_%s" % nm_, cx_ - 0.5 * kb, ybot, x + sw, yy + 0.3 * kb, u"", ix_page=pid)
        CROP_PANELS[-1]["bk_w"] = (x + sw - cx_ + 0.5 * kb) / kb   # text-only: note items (U20)
        LOG.append(u"section %s %s SITE" % (pid, c_["name"]))
        yy = min(yy - h_, ybot) - gap - extra
    sf_triangles(**tri_)
    for m_ in sf_assert_g6(ss / kb, strict=False):       # v56 G6: figures print 1.75 m at the page scale (trees:
        LOG.append(u"Sections {}: {}".format(u", ".join(names), m_))   # measured, not checked: p45_tree)
    if P45_TREE_OUT.get(pid):
        LOG.append(u"trees %s measured: %d existing trees drawn at their measured height outside their species' "
                   u"sourced range (G6 height check skipped for existing trees, tree_species.md T3)" % (
                       pid, P45_TREE_OUT[pid]))
    LOG.append(sb_tree_log(pid))                         # v61 (G6-10): "trees <page> species=n generic=n"
    g14_ = sf_g14_line()
    if g14_:
        LOG.append(u"Sections {}: {}".format(u", ".join(names), g14_))
    low = min(top - H, yy + gap + extra)
    P45_COLLECT[0] = False
    LOG.append(fig_set_line())                           # v59 (G-R4-5.1): "figures set=pen_black n"
    LOG.append(u"Sections {} ({}): split per cut for the booklet: {} drawings + {} notes + key map + legend".format(
        u", ".join(names), pid, len(rows), len(rows)))
    return low


def p45_keymap(S, pid, names):
    """v61 (G6-5, PLAN §2.5): the page's key map from keymap.py v3 (km_keymap): ONLY this page's cuts, each as
    (S end, S' end (survey m), (Sn, Sn'), look 1: the cut is drawn looking to the left of S -> S', where its
    buildings and trees beyond lie), in the frames' key-map frame (P45_KM_MM); stored in P45_KM[pid] for the export
    (16d: km_export_items, detected by its "study_ring" key); km_keymap logs "keymap <page> module ..." itself.
    Never drawn on the board."""
    cuts = []
    for nm in names:
        sd_ = next((q_ for q_ in S.sections if q_["name"] == nm), None)   # the whole cut (not the drawn crop)
        if sd_ is None:
            continue
        x0, y0, x1, y1 = sd_["line"][:4]
        cuts.append(((x0, y0), (x1, y1), cut_end_labels(nm), 1))
    w_, h_ = P45_KM_MM.get(pid, P45_KM_MM["p04"])
    try:
        P45_KM[pid] = km_keymap(pid, cuts=cuts, w_mm=w_, h_mm=h_, names=("streets", "places"),    # noqa: F821
                                log=LOG)
    except Exception as e:
        P45_KM.pop(pid, None)
        wn_warn(pid, "keymap", u"sections key map not made: %s" % e)


def p45_legend(pid, cats):
    """v61 (G6-6, PLAN §2.6, H1): the page's legend P45_LEG[pid] (exported by 16d as sb_sec_legend_<pid>): the
    strip's land uses grouped by category in the hue table (legend_group: table order, then rank; the strip is
    drawn in the same hues, p45_cat_hex), then the key map's marks (study area ANN 6A4C93 dash, the red cut,
    level mark ink). Logs "legend <page> hues=table" (hue_log). The section drawings' own colours (soil, faded
    buildings, the blue stream) are the SITE target and are not keyed here."""
    ents = []
    for c_ in cats or []:
        code, rank = P45_CAT_HUE.get(c_, ("CTX", 3))
        ents.append(dict(cat=code, rank=rank, label=P45_STRIP_WORD.get(c_, c_), key=c_))
    try:
        ents = legend_group(ents)                                                             # noqa: F821
    except Exception as e:
        wn_warn(pid, "legend", u"legend_group failed (%s): strip uses left in drawing order" % e)
    out = []
    for e_ in ents:
        sw_ = dict(kind="fill", colour=e_.get("hex") or p45_cat_hex(e_["key"]))
        if e_["rank"] >= 4:                              # P-4: a pale tint gets an r1/r2 outline
            sw_["stroke"] = hue(e_["cat"], 2)                                                 # noqa: F821
        if e_.get("cat_name"):
            sw_["group"] = e_["cat_name"]
        out.append((sw_, e_["label"]))
    out += [(dict(kind="dash", colour="6A4C93", group=u"annotations"), R28_STUDY_NAME),
            (dict(kind="line", colour=crop_hex(KM_CUT["colour"]), group=u"annotations"),
             u"cut line · the triangle looks the way the section is drawn"),
            (dict(kind="line", colour="2C2219", group=u"annotations"),
             u"level, m above sea · bed, mean flow, 100- and 500-year flood, tallest roof")]
    P45_LEG[pid] = out
    LOG.append(hue_log(pid))                                                                  # noqa: F821


def site28_title(s):
    """an upper-case name in title case with its Turkish letters (MÜSELLA BAYIRI YOLU -> Müsella Bayırı Yolu); words
    with digits and words not in capitals stay as written. v58 (round 3, G16 / D9): a name led by a bridge code
    ("K4 · ULUCAMİ ÖNÜ", "K6") is printed as the bridge's one name (bridge_name: "Ulucami Önü Köprüsü"), never
    the code"""
    head_ = (s or u"").split(u"·")[0].strip().upper()
    if len(head_) == 2 and head_[0] == u"K" and head_[1].isdigit():
        try:
            return bridge_name(head_)
        except KeyError:
            pass
    out = []
    for w_ in (s or u"").split(u" "):
        if not w_ or any(c_.isdigit() for c_ in w_) or not w_.isupper():
            out.append(w_)
            continue
        lo = w_.replace(u"I", u"ı").replace(u"İ", u"i").lower()
        out.append({u"i": u"İ", u"ı": u"I"}.get(lo[0], lo[0].upper()) + lo[1:])
    return u" ".join(out)


def site28_main_k(sd_):
    """the index of a cut's main stream crossing (its lowest bed), or None"""
    if not sd_["water"]:
        return None
    return min(range(len(sd_["water"])), key=lambda k_: sd_["water"][k_][2])


def site28_bank_of(sd_, k_):
    """(the crossing's bank dict or {}, its bank level m a.s.l. or None) for water run k_"""
    bks = sd_.get("banks") or []
    lv = [l_ for l_ in sd_["levels"] if l_[3] == "bank"]
    return (bks[k_] if k_ < len(bks) else {}) or {}, (lv[k_][2] if k_ < len(lv) else None)


def site28_road_call(t):
    """(text, priority) of a street a cut crosses, from road_label's text: its name and the length the cut runs on
    it in cm (G13), priority 2; an OSM line with no surveyed surface: its name alone, an unnamed street: "street",
    priority 3"""
    nm_, _, rest = t.partition(u" · ")
    nm_ = site28_title(nm_)
    if u"OSM line" in rest:
        return nm_, 3
    try:
        m_ = float(rest.split(u" m")[0])
    except ValueError:
        return nm_, 3
    if nm_.lower() == u"street":                         # v60.2 (G-R5-4.6): the name only, no width in cm
        return u"street", 3
    return nm_, 2


def site28_link(S, px, py, line):
    """what a cut's crossing (px, py) links to in the masterplan (masterplan_results.json "movement", once per run):
    its nearest hub within SITE28_HUB_M, else its nearest crossing within SITE28_XING_M, else a street it changes
    that the cut crosses; without the masterplan's movement the nearest bridge K1-K6 within SITE28_K_M; u"" when none.
    v58 (round 3, G16 / D9): every bridge printed by its one name (site28_title -> bridge_name; BRIDGES_K's 2nd field
    is bridge_name(k)), never its K-code"""
    if not hasattr(S, "_s28_mp"):
        S._s28_mp = mp_movement(static_ok=False)
    M = S._s28_mp
    if M:
        best = None
        for h in M.get("hubs") or []:
            q = _xy1(h.get("xy"))
            d = math.hypot(q[0] - px, q[1] - py) if q else 1e12
            if d <= SITE28_HUB_M and (best is None or d < best[0]):
                best = (d, h)
        if best:
            h = best[1]
            return u"**{}**, {} hub{}".format(site28_title(h.get("name") or u""), u"transit" if h.get("role") ==
                                              "transit" else u"walking", u" · sub-hub in the bed" if h.get("sub_hub")
                                              else u"")
        for c_ in M.get("crossings") or []:
            q = _xy1(c_.get("xy"))
            d = math.hypot(q[0] - px, q[1] - py) if q else 1e12
            if d <= SITE28_XING_M and (best is None or d < best[0]):
                best = (d, c_)
        if best:
            return u"**{}**, {}".format(site28_title(best[1].get("name") or u""), best[1].get("kind") or u"crossing")
        x0, y0, x1, y1 = line[:4]
        for r_ in M.get("roads") or []:
            if r_.get("change") in (None, "", "kept"):
                continue
            P_ = _xy_list(r_.get("xy"))
            if any(seg_x((x0, y0), (x1 - x0, y1 - y0), a_, (b_[0] - a_[0], b_[1] - a_[1])) for a_, b_ in zip(P_, P_[1:])):
                return u"**{}**, {}".format(r_.get("name") or u"street", r_.get("change"))
        return u""
    best = None
    for kk, nm_, bx, by in BRIDGES_K:
        d = math.hypot(bx - px, by - py)
        if d <= SITE28_K_M and (best is None or d < best[0]):
            best = (d, kk, nm_)
    return u"the nearest bridge is **{}**".format(best[2]) if best else u""   # v58 (G16 / D9): the name, no K-code


def site28_sec_reading(S, sd_):
    """v50 (MIRAQUA 28 Oct, P04.2): (key sentence, what steers the project) of a cut, from its own data only, with
    **bold** keywords: whether it crosses or runs along the stream, the bed's depth below the lower bank crest or
    between the DSİ walls, the edges on its banks; then the strongest constraint or chance at the water and its link
    in the masterplan (site28_link). Memoised on the cut (sd_["_read"]). v51 (WO-T3a-3): the bed, banks and walls
    from the level module (p45_banks, p45_dep); no source or status words on the page (D13)."""
    if "_read" in sd_:
        return sd_["_read"]
    x0, y0, x1, y1 = sd_["line"][:4]
    Lc = math.hypot(x1 - x0, y1 - y0) or 1.0
    ux, uy = (x1 - x0) / Lc, (y1 - y0) / Lc
    k_ = site28_main_k(sd_)
    tot = sum(sd_["comp"].values()) or 1.0
    top = sorted(sd_["comp"].items(), key=lambda kv: -kv[1])[:2]
    if k_ is None:
        key = u"The cut **does not cross the stream**" + (u": it runs through " + u" and ".join(
            u"{} ({:.0f}%)".format(short(CAT[c_][0]).lower(), 100.0 * v_ / tot) for c_, v_ in top) if top else u"") + u"."
        cons = u"**{}** over {:.0f}% of the cut".format(short(CAT[top[0][0]][0]).lower(), 100.0 * top[0][1] / tot) \
            if top else u""
        px, py = x0 + ux * 0.5 * Lc, y0 + uy * 0.5 * Lc
    else:
        a, b, bed, lvl = sd_["water"][k_]
        cr, zb = site28_bank_of(sd_, k_)
        # v51 (WO-T3a-3, 02 §6, D4 b, D13): the bed and banks from the level module; no status, no internal source
        crs_ = p45_banks(sd_)
        main = next((c2 for c2 in crs_ if c2["k"] == k_), crs_[0] if crs_ else None)
        wall = bool(main) and any(sd["typ"] == "dsi_wall" for sd in main["sides"])
        if main is not None:
            a, b = main["a"], main["b"]
        if len(crs_) > 1:
            dep = u"it crosses the stream **{} times**, the bed at {}".format(
                len(crs_), u", ".join(u_level(c2["bed"]) for c2 in crs_))
        elif main is None:
            dep = u"it crosses the stream"
        else:
            dep = p45_dep(main)
        if cr.get("ang", 90.0) < SITE28_CROSS:
            key = u"The cut runs **along the stream**, not across it; " + dep
        else:
            key = dep[:1].upper() + dep[1:]
        sides = [(t_, wl_) for s_, t_, wl_, gz_ in sd_["labels"] if abs(s_ - a) < 0.3 or abs(s_ - b) < 0.3]
        sn_ = [p45_sides(sd_)[0 if abs(s_ - a) < 0.3 else 1] for s_, t_, wl_, gz_ in sd_["labels"]
               if abs(s_ - a) < 0.3 or abs(s_ - b) < 0.3]           # v58 (D6): each bank by its place
        ws = [SITE28_EDGE_WORD.get(t_, t_) + SITE28_WL_WORD.get(wl_, u"") for t_, wl_ in sides]
        if len(ws) >= 2 and ws[0] == ws[1]:
            key += u"; {} on both banks".format(ws[0])
        elif len(ws) >= 2 and sn_[0] != sn_[1] and cr.get("ang", 90.0) >= SITE28_CROSS:
            key += u"; {} on the {}, {} on the {}".format(ws[0], place_name("side_" + sn_[0]), ws[1],
                                                         place_name("side_" + sn_[1]))
        elif len(ws) >= 2:
            key += u"; {} on one bank, {} on the other".format(ws[0], ws[1])
        elif ws:
            key += u"; {} at the water".format(ws[0])
        key += u"."
        tys = [t_ for t_, wl_ in sides]
        wls = [wl_ for t_, wl_ in sides]
        if wall and "pedestrian" not in tys:
            hw_ = max([sd["h"] for sd in main["sides"] if sd["typ"] == "dsi_wall" and sd["h"] is not None] or
                      [SCT_DSI_WALL_H_M])
            cons = u"**DSİ walls {} high**, no walkable edge at the water".format(u_height(hw_))
        elif 2 in wls:
            cons = u"an **embanked** bank, cut off from the street"
        elif 1 in wls:
            cons = u"a **walled** bank, cut off from the street"
        else:
            cons = next((t2 for t1, t2 in SITE28_STEER if t1 in tys), u"")
        sm = 0.5 * (a + b)
        px, py = x0 + ux * sm, y0 + uy * sm
    link = site28_link(S, px, py, sd_["line"])
    steer = u""
    if cons or link:
        steer = u"Steers the project: " + cons + ((u" -> " if cons else u"") + link if link else u"") + u"."
    sd_["_read"] = (key, steer)
    return sd_["_read"]
