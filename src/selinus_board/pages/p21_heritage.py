# p.21 the heritage loop (split from parts/15f_v46_pages.py, parts/15j_r28_heritage.py on 29 Oct 2026; v51 rebuilt for package G, WO-T3a-6)


def her21_tg(B):
    """v59 (round 4, P20.1 / G-R4-1): a new text-group id for one word block (a name and its halo copies, a card's
    title and lines), without leaving a group open on the Board (sb_text_check: one group may touch itself only)"""
    prev = B.tg
    g = B.tgroup()
    B.tg = prev
    return g


def her21_halo(B, s, x, y, h, col, L, order, k, tg=None, **kw):
    """v58 (round 3, P20.1): a word with a white halo (eight white copies 0.3 mm round it, one order under), so it
    stays legible where it sits on a line, the water or a building. v59 (round 4, P20.1 / G-R4-1): the word and its
    copies are ONE text group (tg, else a new one), so the page check does not read the halo as text on text."""
    tg = tg or her21_tg(B)
    d = 0.3 * k
    for dx, dy in ((1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7),
                   (-0.7, -0.7)):
        B.text(s, x + dx * d, y + dy * d, h, WHITE, L, order=order - 1, tg=tg, **kw)
    B.text(s, x, y, h, col, L, order=order, tg=tg, **kw)


def her_tw(txt, h, bold=False):
    """v50 (G5): the printed width (board units) of txt in Arial at capital height h. v59 (round 4, G-R4-1): the
    REAL Arial width (tw, parts/05_build_terrain.py -> common/font_metrics.py), the one the page check measures
    (was the HER_W table)"""
    return tw(txt, h, "sans", bold)


def her_words(txt):
    """v50 (G5): 'a **b**, c' -> words, each a list of (text, bold) runs; a run with no space before it is glued to the
    word before ('**b**,' is one word of two runs)"""
    words, end_sp = [], True
    for i, part in enumerate(txt.split(u"**")):
        if not part:
            continue
        toks = part.split()
        if not toks:
            end_sp = True
            continue
        glue = bool(words) and not end_sp and not part[0].isspace()
        for j, t_ in enumerate(toks):
            if j == 0 and glue:
                words[-1].append((t_, i % 2 == 1))
            else:
                words.append([(t_, i % 2 == 1)])
        end_sp = part[-1].isspace()
    return words


def her_wrap(txt, h, width):
    """v50 (G5): txt (** = bold) broken into lines of words no wider than width at capital height h. v59 (round 4
    closing, G-R4-2): no single-word last line (text_place.tp_wrap's rule, min_last_words=2, as the core wrap): the
    last word of the line above moves down when that line keeps 2 words and the two then fit (else left as set)"""
    sp = her_tw(u" ", h)
    lines, cur, cw = [], [], 0.0
    for wd in her_words(txt):
        ww = sum(her_tw(t_, h, b_) for t_, b_ in wd)
        if cur and cw + sp + ww > width:
            lines.append(cur)
            cur, cw = [], 0.0
        cw += (sp if cur else 0.0) + ww
        cur.append(wd)
    if cur:
        lines.append(cur)
    if len(lines) >= 2 and len(lines[-1]) == 1 and len(lines[-2]) >= 3:
        cand = [lines[-2][-1], lines[-1][0]]
        if sum(her_tw(t_, h, b_) for wd in cand for t_, b_ in wd) + sp <= width:
            lines[-2], lines[-1] = lines[-2][:-1], cand
    return lines


def her_line(B, words, x, y, h, col, L, order=40, tg=None):
    """v50 (G5): one line of her_wrap, its plain and bold runs each one live text at its measured width; returns the
    x after it. v59 (round 4, G-R4-1): tg = the text group of the block the line belongs to"""
    runs = []
    for i, wd in enumerate(words):
        for j, (t_, b_) in enumerate(wd):
            t_ = (u" " if i > 0 and j == 0 else u"") + t_
            if runs and runs[-1][1] == b_:
                runs[-1][0] += t_
            else:
                runs.append([t_, b_])
    cx = x
    for t_, b_ in runs:
        s_ = t_.lstrip()
        cx += her_tw(t_[:len(t_) - len(s_)], h, b_)      # a space that starts a run: its width, no text
        B.text(s_, cx, y, h, col, L, order=order, font=FONT_TITLE, bold=b_, tg=tg)
        cx += her_tw(s_, h, b_)
    return cx


def her_walk(S, pts):
    """v50 (P20.2): the stream walk K3 -> K4 along the stream's centre line (the longest piece of S.selinus) every
    10 m, and its length along the stream (m); a straight line when the centre line is missing or misses a bridge"""
    a, b = pts[HER_WALK["frm"]], pts[HER_WALK["to"]]
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    main = max(streams, key=pl_length) if streams else None
    if main is None or max(pl_dist(a[0], a[1], main, False), pl_dist(b[0], b[1], main, False)) > HER_SNAP_M:
        LOG.append(u"Heritage loop: the stream's centre line misses {} or {} (over {:.0f} m), so the stream walk is "
                   u"drawn straight.".format(bridge_name(HER_WALK["frm"]), bridge_name(HER_WALK["to"]),
                                            HER_SNAP_M))   # v58 (round 3, G16): names, not codes
        return [a, b], math.hypot(b[0] - a[0], b[1] - a[1])
    s0, s1 = pl_chainage(main, a[0], a[1]), pl_chainage(main, b[0], b[1])
    nn = max(2, int(abs(s1 - s0) // 10.0))
    return [pl_point_at(main, s0 + (s1 - s0) * i / float(nn))[0] for i in range(nn + 1)], abs(s1 - s0)


def her_labels(B, items, taken, bounds, k, L, segs=(), order=66):
    """v58 (round 3, G3 / P20.1; v52 M2): names on a map placed by the shared lp_place (booklet mm) with NO leaders:
    a name sits on or right beside its point (at 1.0, 0.9 or 0.8 x its size) clear of the other names, the symbols
    (taken) and the loop's lines (segs); a name with no such spot becomes a LETTER on the spot (a, b, c ... in reading
    order; letters, since the loop stops already carry numbers), listed in the key beside the map. Every word with a
    white halo (her21_halo). items: dicts lines, x, y (board units), h, col, bold (first line), italic, r0 (the
    symbol's radius). taken grows by the placed boxes. Returns (key [(letter, name)] in letter order, the placed
    boxes in booklet mm)."""
    if not items:
        return [], []
    pad = 0.65                                            # mm round the words; v59 (round 4, G-R4-1): was 0.35,
    # now the 0.3 mm halo + half the page check's 0.6 mm gap, so two names' halos never come within 0.6 mm
    tk = [(b[0] / k, b[1] / k, b[2] / k, b[3] / k) for b in taken]
    bd = (bounds[0] / k + 0.6, bounds[1] / k + 0.6, bounds[2] / k - 0.6, bounds[3] / k - 0.6)
    ln = [[(p[0] / k, p[1] / k), (q[0] / k, q[1] / k)] for p, q in segs]
    pl = []
    for it in items:
        h, n = it["h"], len(it["lines"])
        w0 = max(her_tw(l_, h, bool(it.get("bold")) and j == 0) for j, l_ in enumerate(it["lines"])) / k
        h0 = (h + (n - 1) * HER_LEAD * h) / k
        pl.append(dict(x=it["x"] / k, y=it["y"] / k, rank=it.get("rank", 0), r=it.get("r0", 0.0) / k,
                       wh=(lambda a_, b_: (lambda f: (a_ * f + 2.0 * pad, b_ * f + 2.0 * pad)))(w0, h0)))
    hl = bk_hk(HER21_PT["lab"], k)                        # a letter's capital height (board units)
    got = lp_place(pl, tk, ln, bd, pad=0.5, num_wh=lambda s_: (1.1 * hl / k + 2.0 * pad, hl / k + 2.0 * pad))
    key, boxes = [], []
    for i, it in enumerate(items):
        g = got[i]
        if g is None:                                     # leaders=False never drops a label; kept as a guard
            continue
        b = g["box"]
        bx = (b[0] * k, b[1] * k, b[2] * k, b[3] * k)
        boxes.append(tuple(b))
        if g.get("number"):                               # no spot: its letter on the spot, its name in the key
            c_ = HER21_LETTERS[(g["number"] - 1) % len(HER21_LETTERS)]
            her21_halo(B, c_, 0.5 * (bx[0] + bx[2]), 0.5 * (bx[1] + bx[3]), hl, it["col"], L, order, k,
                       font=FONT_TITLE, bold=True, align="MC")
            key.append((g["number"], c_, u" ".join(it["lines"])))
        else:
            h = it["h"] * g["size"]
            tg = her21_tg(B)                              # v59 (round 4, G-R4-1): a name's lines = one word block
            for j, l_ in enumerate(it["lines"]):
                her21_halo(B, l_, bx[0] + pad * k, bx[3] - pad * k - h - j * HER_LEAD * h, h, it["col"], L, order,
                           k, tg=tg, font=FONT_TITLE, bold=bool(it.get("bold")) and j == 0,
                           italic=bool(it.get("italic")))
        taken.append(bx)
    key.sort(key=lambda t_: t_[0])
    if key:
        LOG.append(u"Heritage loop: {} name(s) with no free spot on the map are letters keyed under it ({}).".format(
            len(key), u", ".join(u"{} {}".format(c_, t_) for n_, c_, t_ in key)))
    return [(c_, t_) for n_, c_, t_ in key], boxes


# ------------------------------------------------------------ v51 (revision 29 Oct 2026, WO-T3a-6, package G)
# p.21 rebuilt (crop drw_heritage_loop; the key map drw_heritage_key is gone):
# - ONE map at 1:10,000, north up, on the shared simple basemap (common/basemap.py, mode "simple", read from the
#   wider extent: survey frame + OpenStreetMap out to Akropol, Teleferik, Bergama Müzesi, Asklepion). The map is
#   shaped to its places: a main rectangle round the loop and a northern tab holding Akropol and the Teleferik's
#   line. No locator: the map itself reaches every place, so the right-hand overview map is removed.
# - Every place: a round photo in a column beside the map, tied to its pin by a straight leader (R07 / R08 idea),
#   with a short text: why it matters, how it is used, its condition, how the project ties it in. Facts only from the
#   library history cards h01-h03 and the sources they cite; a field with no source is left out.
# - In the corner the tab leaves free: how the places feed each other across the Selinos (the stream as the seam
#   between the Kale side and the bazaar side), drawn as a plan diagram (R09 idea: places strung along the water).
# - The stream walk K3-K4 (the project's spine) drawn as a path along the water (v58: explained in the strip under the
#   diagram, no longer named on the map: only place names there, G3).
# - Place names on the map Turkish only (G6, strict). Photos from HER21_PHOTO_DIR: own site photos (no credit, D13)
#   and the Commons set (credit lines from its photos.csv); a missing photo = an empty round slot with the name.
# - Build once (Aras 29 Oct 19:18): basemap_items is memoised; photos.csv, the photo files and their sizes are read
#   once per run (_HER21_PH).
# v52 (revision 30 Oct 2026, PG1 p20): the map is ONE full rectangle (no tab, nothing over it) in its own M1 grid
# cells; the diagram has its own cell above the left card column; the cards say a name + one line and sit in stop
# order beside the map, tied to their pins by the shared badge (numbered stops) or name: no leader crosses the map;
# the map's names are placed by M2 lp_place (short leaders that never cross); no photo credits on the page (they go
# to the booklet's Sources page through her21_credits).
# v59 (round 4, P20.1-P20.4, D3, G-R4-2/4/7/8/9/11): the places diagram (her21_diagram) and the stream-walk strip
# (her21_walk_strip, "Where the loop meets the channel") are removed (D3); the left column holds the four heritage
# places' cards only and gives one grid column to the map (G-R4-2: freed space to the drawing). The map is drawn by
# the shared map_draw (common/map_layers.py): the MUTED base (light houses with closed outlines, contours in the green
# relief ramp BM_HEIGHT_RAMP, lighter = lower) at the back, then the loop (8B2D2D, 1.2 mm, PLAN §4.10), the stream walk
# (clipped to the study area), the study line BM_STUDY_LINE, the pins (mk_marker) and the names in front, by tone AND
# by order. Photos in rectangular windows (no circle, no frame). North arrow = north_items (no plate). Names from the
# names table (landmark_name, bridge_name).
# v60 (round 5, D5 / P22.2, T01): the places diagram and the stream-walk strip are back at the top of the left column
# (restored from 5249425, removed in d16192e); that column is again as wide as the stops' column (the diagram's 95 mm
# design width), the four places' cards under them. Their texts are ordinary Board texts (booklet label items).
HER21_DEN = 10000              # the map's scale on the booklet page
HER21_MARGIN_M = 90.0          # m of map round the outermost places and the Teleferik's top station (every side)
HER21_PHOTO_MM = 22.0          # mm: the tallest photo window (v59: rectangles, was the largest photo circle)
HER21_PHOTO_WMAX = 1.35        # v59 (P20.4): a landscape window at most this x its height wide (the text column's
                               # x is the same for every card of a column: column alignment, G-R4-3)
HER21_PT = dict(name=8.0, txt=7.5, lab=7.5, dia=7.5, title=8.5, num=7.5)   # booklet pt (body minimum 7.5)
# v60 (round 5, D5): restored from 5249425 (removed in d16192e): the diagram sizes above (dia, title) and these
HER21_DIA_MM = (95.0, 80.0)    # mm: the diagram's design width (3 grid columns) and its cell's height
HER21_STRIP_MM = 34.0          # mm: P20.2 the stream-walk strip under the diagram, in the same cell
HER21_OFFER_M = 40.0           # m: a city-link place this close to the stream walk is drawn on the strip
# v58 (round 3): drawing rules of the map (not data)
HER21_LETTERS = u"abcdefghijklmnopqrstuvwxyz"   # G3: map names with no free spot -> a letter on the spot + the key
HER21_LOOP_HEX = "8B2D2D"      # v59 (round 4, P20.1, PLAN §4.10): the heritage loop's colour (palette reference)
HER21_LOOP_C = C(HER21_LOOP_HEX)
HER21_LOOP_MM = 1.2            # v59 (P20.1, PLAN §4.10): the loop's legs, mm on the booklet page
HER21_WALK_MM = 1.5            # mm: the stream walk (the loop's spine), white dashes on it as v58
HER21_CASE_MM = 0.5            # mm: a white casing this much wider than a loop line (separates it from the base)
HER21_NEAT_MM = 0.25 * 25.4 / 72.0     # G17: the map's neatline, 0.25 pt
HER21_NORTH_MM = 5.0           # v59 (G-R4-9): the north arrow's height (north_items, no plate)
# Photos: Downloads/Bergama/Data/heritage_photos/ holds (a) the own site photos by their file names below (copied
# from revision_2026-10-29/T1/photos/files/; no credit, D13) and (b) the Commons set from Aras's other account
# (Bergama_assets_2026-10.zip unpacked here: photos.csv + its photo files, beside it or in photos/). photos.csv
# columns read: file, place, credit (or "credit line"); other columns are ignored. The place column is matched to
# the places below by their aliases (Turkish letters folded).
HER21_PHOTO_DIR = os.path.join(DATA_DIR, "heritage_photos")
HER21_PHOTO_CSV = "photos.csv"
HER21_GONDOLA_TOP = (30460.0, 33003.0)     # Teleferik top station, OSM node 2295928363 (h03 Q3), h01 §0 lat/lon fit
HER21_K5 = (30294.0, 31792.0)              # Üç Kemer Köprüsü (K5), h01 §0 survey frame / §5 P09
HER21_WATER, HER21_BLD = C("91ADB4"), C(BM_MUTED["bld"])   # legend samples: basemap BM_COL water; v59 (P20.2):
                                                           # the muted base's light house tone (was BM_FAINT D3D0CB)
# The places (map pins and cards). stop = HER_STOPS key (its loop number), dot = HER_DOTS name; name = the map's
# Turkish name, title = the card's. txt (v52, PG1 p20): ONE line under the card's name, key words bold (G4); the
# v51 Why / Use / Now / Project texts are cut to it (their facts stay in the cards h01-h03 noted per place). Sources (library cards h01 = selinos_bergama_history_context_v1, h02 = selinos_site_history_inaccessible_
# edges_v1, h03 = bergama_history_hubs_research_v1) are noted per place; nothing here is printed as a source.
# v58 (round 3, P20.3 / G16): the bridges' names (map, cards) by bridge_name, no "(K3)" codes; key, stop, own and
# alias stay as they are (internal keys and photo file keys). v59 (round 4, G-R4-11): every printed name (and the
# "dot" match key, the same call as HER_DOTS) from the names table (landmark_name); keys, aliases, file names kept.
HER21_PLACES = [
    # h01 §5 P01; h02 §2.9 (inscribed 22.06.2014); h03 Q2 (ICOMOS 2014 s13 p287: tour groups, up by the gondola)
    dict(key="akropol", name=landmark_name("akropol"), own=(), alias=(u"akropol", u"acropolis", u"trajaneum"),
         txt=u"**World Heritage** hill city: the loop's goal"),
    # h01 §5 P33 (2010, 700 m line, s115); h03 Q2 (ICOMOS s13 p287)
    dict(key="teleferik", stop="gondola", name=landmark_name("teleferik"), own=(),
         alias=(u"teleferik", u"gondola", u"cablecar"),
         txt=u"**cable car** (2010): the loop starts here"),
    # h01 §5 P02-P04; h02 §2.3 (tunnels, s13), §3 Worship (N rotunda = mosque), §4.3 (closed since 03/2025, aim
    # 2026, s41); h03 Q5 (Kermes 2024 concerts in Kızıl Avlu)
    dict(key="kizilavlu", stop="redhall", name=landmark_name("kizil_avlu"), own=(),
         alias=(u"kizilavlu", u"redhall", u"redbasilica", u"serapis", u"serapeion"),
         txt=u"Hadrian's temple, **built over the stream**"),
    # h01 §5 P08; h02 §2.5 (KE s29: Roman 2nd-3rd c., tanneries), E03 (DSİ walls 2020-), §4.6 (tourist signs at K3,
    # s63); h03 Q1 (lines 831-833 at Tabak Köprüsü, s124)
    dict(key="k3", stop="K3", name=bridge_name("K3"), own=(u"tabak_koprusu_1.jpg", u"tabakhane_1.jpg"),
         alias=(u"tabakkoprusu", u"tabakhanekoprusu", u"tabakhane"),
         txt=u"**Roman bridge**: the stream walk starts"),
    # h01 §5 P06; h02 §2.5 (s31 two spans, Ottoman small arch; KGM plaque 2024-2025, s63); h03 Q1 (Camikebir Cd.)
    dict(key="k4", stop="K4", name=bridge_name("K4"), own=(u"ulucami_onu_koprusu_1.jpg",
                                                         u"ulucami_onu_koprusu_2.jpg"),
         alias=(u"ulucamionukoprusu", u"ulucamionu"),
         txt=u"bridge to **" + landmark_name("ulucami") + u"**: the stream walk ends"),   # v59 (G-R4-11)
    # h01 §5 P05 (1398-99, Bayezid I, restored 1905, minaret 1949), P11 (Bergama Müzesi digs 2021-23, s4); h02 §3
    # Worship (Ulucami at K4)
    dict(key="ulucami", dot=landmark_name("ulucami"), name=landmark_name("ulucami"), own=(u"ulu_cami_1.jpg",), alias=(u"ulucami",),
         notalias=(u"onu", u"koprusu"),
         txt=u"**mosque** of 1398-99 at " + bridge_name("K4")),   # v58 (round 3, G16): no K-code
    # h01 §5 P07; h02 §2.5 (s32: opposite Ulucami, named after the tanneries; sign s63: camekan dome survives),
    # §3 Bathing (ruin since the 1842/47 flood, enclosed by 5 houses), §2.9 (s57: municipal survey drawings)
    dict(key="hamam", dot=landmark_name("tabaklar_hamami"), name=landmark_name("tabaklar_hamami"),
         own=(u"tabaklar_hamami_1.jpg", u"tabaklar_hamami_2.jpg"),
         alias=(u"tabaklarhamami",),
         txt=u"Ottoman **tanners' bath**, now a ruin"),
    # h01 §5 P23 (1513; Parchment Museum 2026, s99 s45); h02 §3 (Parchment Museum opened 28.02.2026); h03 Q4
    # (Çınarlı Kahve plane ~380-400 yr, pipe-irrigated, AA 2026), Q5 (Kermes 2024 events at the Arasta, Çınarlı Kahve)
    dict(key="arasta", stop="bazaar", name=landmark_name("arasta"), title=landmark_name("arasta") + u" (Hacı Hekim)",
         own=(),
         alias=(u"arasta", u"hacihekim", u"cinarlikahve"),
         txt=u"**bazaar** of 1513; its hamam: Parchment Museum"),
    # h01 §5 P09; h02 §2.5 (s30: three arches, repairs altered its character), §2.9 (first stage 1,380 m Kazancı ->
    # Üçkemer, s33 s36), E01 (the tunnels end before K5); h03 Q1 (lines 656, 831-833 at Üç Kemer Köprüsü)
    dict(key="k5", xy=HER21_K5, name=bridge_name("K5"), own=(), alias=(u"uckemer", u"threearch"),
         txt=u"**Roman bridge**: the stream comes out"),
    # h01 §5 P24 (1936, archaeology + carpets, s85 s86), §3 Archaeology (museum + DAI digs on the banks 2011-2025)
    dict(key="muze", stop="museum", name=landmark_name("bergama_muzesi"), own=(),
         alias=(u"bergamamuzesi", u"bergamamuseum", u"archaeologymuseum", u"muze"),
         txt=u"**museum** of 1936: Pergamon's finds"),
    # h01 §5 P28 (4th c. BC, Hadrianic, sacred spring, s114 s81); h03 Q2 (KTB: car parking; OSM ticket building,
    # paid car park)
    dict(key="asklepion", stop="asklepieion", name=landmark_name("asklepion"), own=(), alias=(u"asklep", u"asclep"),
         txt=u"**healing sanctuary**, 4th c. BC: the loop's end"),
]
HER21_FOLD = {u"ı": u"i", u"ş": u"s", u"ğ": u"g", u"ü": u"u", u"ö": u"o", u"ç": u"c", u"â": u"a", u"î": u"i",
              u"û": u"u"}
_HER21_PH = {}                 # once per run: the photo of each place, the photos' pixel sizes


class Her21Clip(object):
    """v51: a Board seen through several rectangles of the page (v52: the map's one rectangle): fills, hatches and
    lines cut to each, words kept where any holds them"""

    def __init__(self, B, rs):
        self.B, self.cs = B, [ClipB(B, r_) for r_ in rs]

    def __getattr__(self, a):
        return getattr(self.B, a)

    def fill(self, *a, **kw):
        for c in self.cs:
            c.fill(*a, **kw)

    def hatch(self, *a, **kw):
        for c in self.cs:
            c.hatch(*a, **kw)

    def line(self, *a, **kw):
        for c in self.cs:
            c.line(*a, **kw)

    def text(self, txt, x, y, h, *a, **kw):
        if any(c.r[0] <= x <= c.r[2] and c.r[1] <= y <= c.r[3] for c in self.cs):
            self.B.text(txt, x, y, h, *a, **kw)


def her21_norm(s):
    """v51: s lower case, Turkish letters folded, letters and digits only ('Kızıl Avlu' -> 'kizilavlu')"""
    t = u"".join(HER21_FOLD.get(c, c) for c in (s or u"").lower())
    return u"".join(c for c in t if c.isalnum())


def her21_xy(pl):
    """v51: a place's survey point: its loop stop's, its heritage dot's, Akropol's (HER_BEYOND) or its own"""
    if pl.get("stop"):
        return [s_["xy"] for s_ in HER_STOPS if s_["key"] == pl["stop"]][0]
    if pl.get("dot"):
        return [q for nm, q in HER_DOTS if nm == pl["dot"]][0]
    if pl["key"] == "akropol":
        return HER_BEYOND[0]["xy"]
    return pl["xy"]


def her21_img(p):
    """v51: (width, height) in pixels of a JPEG or PNG, read once per run; None if it cannot be placed"""
    m = _HER21_PH.setdefault("img", {})
    if p not in m:
        r_ = None
        try:
            r_ = _jpg_rgb(p) or _png_rgb(p)
        except Exception:
            r_ = None
        m[p] = (float(r_[0]), float(r_[1])) if r_ and r_[0] and r_[1] else None
    return m[p]


def her21_photos():
    """v51: {place key: (path, credit or None)} once per run. Own photos (HER21_PLACES own, no credit, D13) first,
    else the first unused row of photos.csv whose place (or file name) matches the place's aliases; its credit
    from the credit / credit line column. Places without a usable file are left out (an empty slot)."""
    if "map" in _HER21_PH:
        return _HER21_PH["map"]
    d, out = HER21_PHOTO_DIR, {}

    def find(f):
        for p in (os.path.join(d, f), os.path.join(d, "own", os.path.basename(f)),
                  os.path.join(d, "photos", os.path.basename(f))):
            if os.path.isfile(p) and her21_img(p) is not None:
                return p
        return None
    own = set(her21_norm(os.path.basename(f)) for pl in HER21_PLACES for f in pl.get("own", ()))
    rows, cp = [], os.path.join(d, HER21_PHOTO_CSV)
    if os.path.isfile(cp):
        try:
            import csv as _csv
            with open(cp, encoding="utf-8-sig", newline="") as f_:
                for r_ in _csv.DictReader(f_):
                    rows.append(dict((her21_norm(k_), (v_ or u"").strip()) for k_, v_ in r_.items() if k_))
        except Exception as e:
            LOG.append(u"Heritage loop: {} could not be read ({}); only the own photos are used.".format(cp, e))
    used = set()
    for pl in HER21_PLACES:
        got = None
        for f in pl.get("own", ()):
            p = find(f)
            if p:
                got = (p, None)
                break
        for r_ in ([] if got else rows):
            fn = r_.get("file", u"")
            if not fn or fn in used:
                continue
            tx = her21_norm(r_.get("place", u"")) + u"|" + her21_norm(os.path.splitext(os.path.basename(fn))[0])
            if not any(a in tx for a in pl["alias"]) or any(a in tx for a in pl.get("notalias", ())):
                continue
            p = find(fn)
            if p is None:
                LOG.append(u"Heritage loop: photos.csv names {} for {}, but the file is missing or unreadable "
                           u"(baseline RGB JPEG or PNG).".format(fn, pl["name"]))
                continue
            used.add(fn)
            cr = r_.get("creditline") or r_.get("credit") or u""
            got = (p, None if her21_norm(os.path.basename(fn)) in own or not cr else cr)
            break
        if got:
            out[pl["key"]] = got
    miss = [pl["name"] for pl in HER21_PLACES if pl["key"] not in out]
    LOG.append(u"Heritage loop photos ({}): {} of {} places have a photo{}.".format(
        d, len(out), len(HER21_PLACES), (u"; empty slots for " + u", ".join(miss)) if miss else u""))
    _HER21_PH["map"] = out
    return out


def her21_credits():
    """v51 (D13; interface for the booklet's Sources page): [(place, credit line)] of the Commons photos the page
    shows, from photos.csv; own photos carry none"""
    ph = her21_photos()
    return [(pl.get("title", pl["name"]), ph[pl["key"]][1]) for pl in HER21_PLACES
            if pl["key"] in ph and ph[pl["key"]][1]]


def her21_mk(B, cx, cy, s, k, L, order=60):
    """v59 (round 4, G-R4-7): one numbered marker by the shared mk_marker (common/marker.py): the glyph centred on
    its ink box, the circle sized to the glyph, in the colour of the thing it names (the loop: mk_colour("p20",
    "loop"), registered by her_loop_page). (cx, cy) board units, k = board units per booklet mm. The disc at order,
    the glyph at order + 1 (its own text group). Returns the marker's outer radius (board units)."""
    sh, box, r = mk_marker(cx / k, cy / k, s, mk_colour("p20", "loop"), size_pt=HER21_PT["num"])
    for s_ in sh:
        if s_[0] == "poly":
            ring = [(p[0] * k, p[1] * k) for p in s_[1]]
            if s_[2]:
                B.fill([ring], C(s_[2]), L, order)
            if s_[3] and s_[4]:
                B.line(ring + [ring[0]], C(s_[3]), L, order, bk_lw(s_[4], k))
        elif s_[0] == "text":                             # size_mm = the font size: the Board takes the capital height
            B.text(s_[1], s_[2] * k, s_[3] * k, s_[4] * _PDF_CAP["sans"] * k, C(s_[5]), L, order=order + 1,
                   font=FONT_TITLE, bold=True, align="L")
    return 0.5 * (box[2] - box[0]) * k


def her21_mk_r(s, k):
    """v59 (round 4, G-R4-7): the outer radius (board units) her21_mk gives the glyph s, before it is placed"""
    b = mk_marker(0.0, 0.0, s, mk_colour("p20", "loop"), size_pt=HER21_PT["num"])[1]
    return 0.5 * (b[2] - b[0]) * k


def her21_geom(pl, ph, x0, x1, cy, pitch, side, k):
    """v59 (round 4, P20.4 / G-R4-8; replaces v51's circle): a card's parts in its slot (x0..x1, centred on cy, pitch
    tall): the photo WINDOW, a rectangle of the picture's own proportions (no circle, no crop mask, no frame), at most
    HER21_PHOTO_MM tall and HER21_PHOTO_WMAX x that wide; an empty slot (no photo) is a square of that height. The
    window sits on the column's map side; the text column starts after the widest window a card of the column may
    have, so every card of a column shares the text's x (G-R4-3). side "L": the window on the right (towards the
    map), "R": on the left."""
    H = max(1.0 * k, min(HER21_PHOTO_MM * k, pitch - 4.0 * k))
    iw = ih = H
    wh = her21_img(ph[0]) if ph else None
    if wh:
        a = wh[0] / wh[1]
        if a < 1.0:                                      # portrait: the full height
            iw, ih = H * a, H
        else:                                            # landscape: at most HER21_PHOTO_WMAX x H wide
            iw = min(H * a, HER21_PHOTO_WMAX * H)
            ih = iw / a
    wb = HER21_PHOTO_WMAX * H
    if side == "L":
        img = (x1 - iw, cy - 0.5 * ih, x1, cy + 0.5 * ih)
        t0, t1 = x0, x1 - wb - 3.0 * k
    else:
        img = (x0, cy - 0.5 * ih, x0 + iw, cy + 0.5 * ih)
        t0, t1 = x0 + wb + 3.0 * k, x1
    return dict(img=img, cy=cy, t0=t0, t1=t1, side=side, pitch=pitch)


def her21_card(B, pl, ph, g, num, k, L, boxes=None):
    """v59 (round 4, P20.4 / G-R4-8, G-R4-7, G-R4-1; replaces v52's round card): the photo in its rectangular window
    (or an empty rectangular slot with the place's name), no frame (r3 G17), no mask; in the window's top corner on
    the map side the badge of its map pin (the loop number by mk_marker, or the ring of a heritage place), inside the
    window; the place's name (wrapped to the text column, bold) and its one line (keywords bold) beside it, ONE text
    group. No credits on the page (G12: the Sources page). boxes (list) gets the card's text boxes in booklet mm."""
    q, cy = g["img"], g["cy"]
    i0_w = sb_mark(B)                                     # v59 closing (G-R4-1): the window's own texts (badge, name)
    if ph:
        B.image(ph[0], q[0], q[1], q[2], q[3], L, order=5)
    else:                                                 # an empty slot: a pale rectangle with the name
        B.fill([rect(q[0], q[1], q[2], q[3])], mix(INK2, WHITE, 0.88), L, 5)
        h = bk_hk(HER21_PT["txt"], k)
        ls = her_wrap(pl["name"], h, (q[2] - q[0]) - 2.0 * k)
        cx = 0.5 * (q[0] + q[2])
        y0 = cy + 0.5 * (len(ls) - 1) * HER_LEAD * h - 0.5 * h
        tg0 = her21_tg(B)
        for j, ln in enumerate(ls):
            s_ = u" ".join(u"".join(t_ for t_, b_ in wd) for wd in ln)
            B.text(s_, cx, y0 - j * HER_LEAD * h, h, INK2, L, order=40, font=FONT_TITLE, align="C", tg=tg0)
    m_ = 0.6 * k                                          # the badge: inside the window's top corner, map side
    if num:
        R = her21_mk_r(str(num), k)
        bx = q[2] - R - m_ if g["side"] == "L" else q[0] + R + m_
        her21_mk(B, bx, q[3] - R - m_, str(num), k, L, order=60)
    else:                                                 # a heritage place: the ring of its pin
        R = 1.6 * k
        bx = q[2] - R - m_ if g["side"] == "L" else q[0] + R + m_
        cb = circle_pts(bx, q[3] - R - m_, R, 24)
        B.fill([cb], WHITE, L, 60)
        B.line(cb + [cb[0]], HER21_LOOP_C, L, 61, bk_lw(0.45, k))
    sb_keep(B, q, u"p20 photo " + pl["name"], "photo", i0_w)   # v59 closing (G-R4-1): no other text on the photo
    hn, h = bk_hk(HER21_PT["name"], k), bk_hk(HER21_PT["txt"], k)
    pt, ptn = HER_PITCH * h, HER_PITCH * hn
    w_ = g["t1"] - g["t0"]
    lt = her_wrap(u"**" + pl.get("title", pl["name"]) + u"**", hn, w_)
    ls = her_wrap(pl["txt"], h, w_)
    bh = hn + (len(lt) - 1) * ptn + 0.6 * pt + len(ls) * pt
    y = min(cy + 0.5 * bh, cy + 0.5 * g["pitch"])
    tg = her21_tg(B)                                      # G-R4-1: the card's words = one word block
    for j, ln in enumerate(lt):
        yb = y - hn - j * ptn
        x_end = her_line(B, ln, g["t0"], yb, hn, INK, L, tg=tg)
        if boxes is not None:
            boxes.append((g["t0"] / k, yb / k, x_end / k, (yb + hn) / k))
    y -= hn + (len(lt) - 1) * ptn + 0.6 * pt
    for ln in ls:
        x_end = her_line(B, ln, g["t0"], y - h, h, INK, L, tg=tg)
        if boxes is not None:
            boxes.append((g["t0"] / k, (y - h) / k, x_end / k, y / k))
        y -= pt
    if bh > g["pitch"] - 1.0 * k:
        LOG.append(u"WARNING: heritage loop card \"{}\": its text is {:.1f} mm tall in a {:.1f} mm slot.".format(
            pl["name"], bh / k, g["pitch"] / k))


def her21_map(S, B, V, Fm, r_all, k, L, xy, num):
    """v59 (round 4, P20.1, P20.2, G-R4-4, G-R4-7; v58 P20.1, G1, G3, G8, G17; v52 PG1 p20): the loop map, ONE full
    rectangle r_all, drawn by the shared map_draw (common/map_layers.py) strictly in its layer order: the MUTED base
    (ml_base: light houses with closed block outlines, light streets, the stream, contours in the green relief ramp
    BM_HEIGHT_RAMP, lighter = lower; orders 2-28), then the project: the loop legs stop to stop (8B2D2D, 1.2 mm, a
    white casing under them), the Teleferik's ticked cable, the stream walk along the water clipped to the study area
    (sc_lines, counted for p20) (proj_lines, order 40, in that sequence), the study line BM_STUDY_LINE (48); over it
    the pins (mk_marker numbers / rings, 60-61) and the place names only, placed by lp_place with no leaders and a
    white halo (65-66); a name with no free spot is a letter on the spot, keyed under the map right of the scale bar
    and north arrow; a 0.25 pt neatline (70). The loop legs join existing places over the existing town and are not
    clipped (only the stream walk is a designed change). Logs map_draw's "layers base→project ok, n_outside_clipped
    <n> (p20: ...)". Returns dict(walk_m, walk (survey m, K3 -> K4), key_bot (y under the key, or None), labels
    (booklet mm boxes of the names, letters and key rows), pins (booklet mm boxes of the pins))."""
    CB = Her21Clip(B, [r_all])
    B.fill([rect(*r_all)], WHITE, L, 1)
    base = ml_base(Fm.bb, HER21_DEN, contours=True)       # memoised (common/basemap.py, mode "muted")
    if not base:
        LOG.append(u"WARNING: heritage loop: no basemap data (cached/basemap/basemap.json missing): the map shows the "
                   u"loop on white.")
    study = [list(P) for P in (getattr(S, "r28_study", None) or [])] or sc_rings()
    if callable(globals().get("wat_draw_order_lines")):  # v58 (round 3, G8): the map's draw order in the log
        wat_draw_order_lines(page="p20", steps=["ground", "water", "structures", "labels"])
    acc, white = HER21_LOOP_HEX, "FFFFFF"
    ink = "%02X%02X%02X" % tuple(INK)
    ins = lambda p: r_all[0] <= p[0] <= r_all[2] and r_all[1] <= p[1] <= r_all[3]
    segs, taken, labs = [], [], []

    def keep(P):
        for run in clip_rect_line(list(P), r_all):
            segs.extend(zip(run[:-1], run[1:]))
    pts = dict((s_["key"], s_["xy"]) for s_ in HER_STOPS)
    order = [s_["key"] for s_ in HER_STOPS]
    walk, walk_m = her_walk(S, pts)
    case, legs = [], []

    def leg(a, b):                                        # survey m; white casing first, every line over every casing
        case.append(("line", [a, b], white, HER21_LOOP_MM + HER21_CASE_MM, None, 1.0))
        legs.append(("line", [a, b], acc, HER21_LOOP_MM, None, 1.0))
        keep([V.p(*a), V.p(*b)])
    for a, b in zip(order[:-1], order[1:]):
        if (a, b) == (HER_WALK["frm"], HER_WALK["to"]):
            continue
        leg(pts[a], pts[b])
    leg(HER21_GONDOLA_TOP, xy["akropol"])                 # top station -> Akropol, on foot
    mpm = HER21_DEN / 1000.0                              # survey m per booklet mm
    ga, gb = xy["teleferik"], HER21_GONDOLA_TOP           # the Teleferik: its cable, ticked every 2.5 mm
    cab = [("line", [ga, gb], ink, 0.25, None, 1.0)]
    dx, dy = gb[0] - ga[0], gb[1] - ga[1]
    dl = math.hypot(dx, dy) or 1.0
    for i in range(1, int(dl / (2.5 * mpm))):
        c = (ga[0] + dx * i * 2.5 * mpm / dl, ga[1] + dy * i * 2.5 * mpm / dl)
        cab.append(("line", [(c[0] - dy / dl * 0.7 * mpm, c[1] + dx / dl * 0.7 * mpm),
                             (c[0] + dy / dl * 0.7 * mpm, c[1] - dx / dl * 0.7 * mpm)], ink, 0.2, None, 1.0))
    keep([V.p(*ga), V.p(*gb)])
    runs = sc_lines(walk, study, page="p20")              # the stream walk: a designed change, inside the study area
    wk = ([("line", R_, white, HER21_WALK_MM + HER21_CASE_MM, None, 1.0) for R_ in runs] +
          [("line", R_, acc, HER21_WALK_MM, None, 1.0) for R_ in runs] +
          [("line", R_, white, 0.3, [1.2, 0.9], 1.0) for R_ in runs])
    for R_ in runs:
        Pw = V.P(R_)
        keep(Pw)
        taken.extend((q[0] - 0.9 * k, q[1] - 0.9 * k, q[0] + 0.9 * k, q[1] + 0.9 * k) for q in Pw[::3] if ins(q))
    st = dict(layer=None, i=0)
    nb = max(1, len(base))
    lay_od = dict(proj_tint=30, proj_water=32, proj_lines=40, proj_vegetation=46, study=48, proj_marks=60,
                  proj_labels=65)

    def od():                                             # base 2-28 in its own sequence; each project layer its order
        if st["layer"] in ML_BASE_LAYERS:
            st["i"] += 1
            return min(28, 2 + int(26.0 * (st["i"] - 1) / nb))
        return lay_od.get(st["layer"], 40)

    def colr(hx, a):
        c = C(hx) if hasattr(hx, "lstrip") else hx
        return c if a is None or a >= 0.999 else mix(c, WHITE, 1.0 - a)

    def fill_fn(rings, hx, a, nz):
        c = colr(hx, a)
        CB.fill(rings, r28_nz(c) if nz else c, L, od())

    def line_fn(P, hx, w, dash, a):
        o = od()
        if dash:                                          # any on/off pattern (the study line's dash-dot too)
            for d_ in r28_pattern(P, [m * k for m in dash]):
                CB.line(d_, colr(hx, a), L, o, bk_lw(w, k))
        else:
            CB.line(P, colr(hx, a), L, o, bk_lw(w, k))

    def order_fn(layer):
        st["layer"] = layer
    map_draw("p20", lambda p: V.p(p[0], p[1]), fill_fn, line_fn, None, base, {"proj_lines": case + legs + cab + wk},
             study=study, clip=False, order_fn=order_fn, log=LOG)
    rr = 1.3 * k
    hl = bk_hk(HER21_PT["lab"], k)
    pins = []                                             # the pins' boxes, booklet mm (FLAG overlap)
    for pl in HER21_PLACES:                               # the pins (proj_marks: over every line)
        p = V.p(*xy[pl["key"]])
        if not ins(p):
            LOG.append(u"WARNING: heritage loop: {} lies outside the map.".format(pl["name"]))
            continue
        n_ = num.get(pl["key"])
        if n_:
            r0 = her21_mk(B, p[0], p[1], str(n_), k, L, order=60)
        else:
            c_ = circle_pts(p[0], p[1], rr, 24)
            B.fill([c_], WHITE, L, 60)
            B.line(c_ + [c_[0]], HER21_LOOP_C, L, 61, bk_lw(0.45, k))
            r0 = rr + 0.25 * k
        taken.append((p[0] - r0, p[1] - r0, p[0] + r0, p[1] + r0))
        pins.append(((p[0] - r0) / k, (p[1] - r0) / k, (p[0] + r0) / k, (p[1] + r0) / k))
        labs.append(dict(lines=[pl["name"]], x=p[0], y=p[1], h=hl, col=INK, bold=True, rank=0, r0=r0))
    sel = [P_ for P_ in (getattr(S, "selinus", None) or []) if len(P_) >= 2]
    if sel:                                               # the stream's Turkish name, clear of the pins
        marks = [V.p(*q) for q in xy.values()]
        best = None
        for q in resample(max(sel, key=pl_length), 40.0):
            p = V.p(*q)
            if not ins(p):
                continue
            d = min([math.hypot(p[0] - m[0], p[1] - m[1]) for m in marks] + [30.0 * k])
            if best is None or d > best[0] + 1e-9:
                best = (d, p)
        if best:
            labs.append(dict(lines=[place_name("stream")], x=best[1][0], y=best[1][1], h=hl, col=MPL["water_edge"],
                             italic=True, rank=1))
    key, lab_boxes = her_labels(B, labs, taken, r_all, k, L, segs)
    key_bot = None
    if key:                                               # G3: the letters' key under the map, beside the north arrow
        ss = V.s
        kx0 = r_all[0] + (1.0 + 10.0 + 8.0) * k + HER_SB_M.get(HER21_DEN, 400.0) * ss
        kx1 = r_all[2]
        hk_ = bk_hk(HER21_PT["txt"], k)
        rows = [(c_, t_, her_tw(c_, hk_, True) + 1.2 * k + her_tw(t_, hk_)) for c_, t_ in key]
        cw_ = max(r_[2] for r_ in rows) + 5.0 * k
        nc = max(1, int((kx1 - kx0 + 5.0 * k) // cw_))
        pt = HER_PITCH * hk_
        y_top = r_all[1] - 2.5 * k
        for i, (c_, t_, w_) in enumerate(rows):           # reading order: left to right, then down
            cx, cy = kx0 + (i % nc) * cw_, y_top - (i // nc) * pt - hk_
            tg = her21_tg(B)                              # v59 (G-R4-1): a key row = one word block
            B.text(c_, cx, cy, hk_, INK, L, order=66, font=FONT_TITLE, bold=True, tg=tg)
            B.text(t_, cx + her_tw(c_, hk_, True) + 1.2 * k, cy, hk_, INK, L, order=66, font=FONT_TITLE, tg=tg)
            lab_boxes.append((cx / k, cy / k, (cx + w_) / k, (cy + hk_) / k))
        key_bot = y_top - ((len(rows) - 1) // nc + 1) * pt - 0.8 * k
    o = [(r_all[0], r_all[1]), (r_all[2], r_all[1]), (r_all[2], r_all[3]), (r_all[0], r_all[3])]
    B.line(o + [o[0]], INK, L, 70, bk_lw(HER21_NEAT_MM, k))   # v58 (round 3, G17): the neatline 0.25 pt
    return dict(walk_m=walk_m, walk=walk, key_bot=key_bot, labels=lab_boxes, pins=pins)


def her21_foot(B, x, yb, ss, k, L, Lm):
    """v59 (round 4, G-R4-9; replaces b_foot on this page): under the map whose bottom edge is at yb, from its left
    edge x: the scale bar as b_foot drew it (draw_scalebar_bk, 1 mm in) and beside it the shared north arrow
    north_items (common/keymap.py: the arrow and "N" only, no plate), north up, HER21_NORTH_MM tall, its "N" 2.5 mm
    under the map. Returns the y below them."""
    x += 1.0 * k
    low = draw_scalebar_bk(B, x, yb - 2.5 * k, ss, Lm, k, L)
    nx = x + Lm * ss + 10.0 * k
    foot = yb - (2.5 + HER21_NORTH_MM + 2.5) * k

    def fill_fn(rings, hx, a, nz):
        B.fill(rings, C(hx), L, 60)

    def line_fn(P, hx, w, dash, a):
        B.line(P, C(hx), L, 60, bk_lw(w, k))

    def text_fn(s_, p, size_mm, hx, bold, align):        # size_mm = the font size: the Board takes the capital height
        B.text(s_, p[0], p[1], size_mm * _PDF_CAP["sans"] * k, C(hx), L, order=61, font=FONT_TITLE, bold=bold,
               align=align)
    basemap_draw(north_items(nx / k, foot / k, 0.0, HER21_NORTH_MM), lambda p: (p[0] * k, p[1] * k), fill_fn,
                 line_fn, text_fn)
    return min(low, foot)


# v60 (round 5, D5): restored from 5249425 (removed in d16192e)
def her21_head(B, a, b, k, col, L, order=63, mm=1.8):
    """v51: a filled arrowhead with its tip at b, pointing from a"""
    dx, dy = b[0] - a[0], b[1] - a[1]
    dl = math.hypot(dx, dy) or 1.0
    ux, uy, s = dx / dl, dy / dl, mm * k
    c = (b[0] - ux * s, b[1] - uy * s)
    B.fill([[b, (c[0] - uy * 0.42 * s, c[1] + ux * 0.42 * s), (c[0] + uy * 0.42 * s, c[1] - ux * 0.42 * s)]], col, L,
           order)


# v60 (round 5, D5): restored from 5249425 (removed in d16192e)
def her21_offers(walk):
    """v58 (round 3, P20.2): what the project offers where the loop meets the channel: the city link's places (its
    results file, else the built-in copy CITY_LINK_DEFAULT, as city_link_spine reads them) within HER21_OFFER_M of
    the stream walk (walk: survey m, K3 -> K4). Returns [(t, name)] in stream order, t = 0 at K4 (upstream) .. 1 at
    K3, measured along the walk. v60 (round 5, D5): a results file's "Red Hall" printed as the names table's
    Kızıl Avlu (G-R4-11, as the built-in copy)."""
    spec = CITY_LINK_DEFAULT
    try:
        with open(CITY_LINK_FILE, "r", encoding="utf-8") as fh:
            spec = json.load(fh)
    except Exception:
        pass
    lw = pl_length(walk) or 1.0
    out = []
    for f in spec.get("functions", []):
        q = f.get("xy")
        if not q or not f.get("name"):
            continue
        x_, y_ = float(q[0]), float(q[1])
        if pl_dist(x_, y_, walk, False) > HER21_OFFER_M:
            continue
        nm_ = f["name"].replace(u"Red Hall", landmark_name("kizil_avlu"))
        out.append((1.0 - min(1.0, max(0.0, pl_chainage(walk, x_, y_) / lw)), nm_))
    out.sort()
    LOG.append(u"Heritage loop: {} city-link place(s) within {:.0f} m of the stream walk: {}.".format(
        len(out), HER21_OFFER_M, u", ".join(n_ for t_, n_ in out) or u"none"))
    return out


# v60 (round 5, D5): restored from 5249425 (removed in d16192e)
def her21_diagram(B, x0, ytop, w, h, k, L, walk_m, num, boxes=None):
    """v52 (PG1 p20.2): how the places meet across the Selinos, a plan diagram (not to scale) in its own grid cell
    above the left card column. The stream is a band (the seam): the Kale side (north bank) above it, the bazaar side
    (south bank) below; on it the bridges K4 and K3 (loop stops, numbered as on the map and the cards), K5, Kızıl Avlu
    over it and the stream walk K4-K3; every other place is a node on its bank with ONE short named link (h01-h03:
    cable car 2010; the bridge to the mosque; the river god Selinos on Roman coins with Asklepios; museum digs on the
    banks 2011-2025; the bath named after the tanneries; the Arasta's hamam is the Parchment Museum 2026; Kermes
    events 2024). Laid out in mm on a 95 x 77 mm design grid (y down); a wider cell only spreads it sideways. v58
    (round 3, G16, G19): the bridges by their names (bridge_name; the short forms of the two walk bridges, whose full
    names stand in the strip under it, her21_walk_strip). boxes (list) gets every word's box in booklet mm.
    v60 (round 5, D5): restored from 5249425 (removed in d16192e) with the round 4 rules: every printed name from
    the names table (landmark_name, place_name, G-R4-11), the loop's colour HER21_LOOP_C (PLAN §4.10), numbered
    stops by the shared marker (her21_mk, G-R4-7), each word block its own text group; no length in the texts (round
    5: no horizontal dimensions); a too-small cell is a wn_warn, not a LOG line. walk_m is kept for the caller."""
    fx = w / (HER21_DIA_MM[0] * k)
    if fx < 0.99 or h < 77.0 * k:                       # the cell is 94.5 mm (crop edges): 0.5 % is fine
        wn_warn("p22", "diagram_cell", u"heritage loop diagram: its cell is {:.0f} x {:.0f} mm, under the 95 x 77 mm "
                u"it is laid out for: names may touch.".format(w / k, h / k))
    P = lambda a, b: (x0 + a * fx * k, ytop - b * k)
    hd, ht = bk_hk(HER21_PT["dia"], k), bk_hk(HER21_PT["title"], k)
    acc, rr = HER21_LOOP_C, 1.3 * k

    def tx(s, a, b, align="L", col=INK, bold=False, italic=False, hh=None):
        p = P(a, b)
        B.text(s, p[0], p[1], hh or hd, col, L, order=66, font=FONT_TITLE, bold=bold, align=align, italic=italic,
               tg=her21_tg(B))
        if boxes is not None:                             # v58: its box (booklet mm)
            tw_ = her_tw(s, hh or hd, bold)
            xl = p[0] - {"C": 0.5 * tw_, "R": tw_}.get(align, 0.0)
            boxes.append((xl / k, p[1] / k, (xl + tw_) / k, (p[1] + (hh or hd)) / k))

    def node(a, b, key):                                  # a loop stop numbered as on the map, else a ring
        p, n_ = P(a, b), num.get(key)
        if n_:
            her21_mk(B, p[0], p[1], str(n_), k, L, order=64)
        else:
            c_ = circle_pts(p[0], p[1], rr, 24)
            B.fill([c_], WHITE, L, 64)
            B.line(c_ + [c_[0]], acc, L, 65, bk_lw(0.45, k))

    def link(pts, head=False, dash=False, col=INK, r0=0.0, r1=0.0):   # r0 / r1 (mm): stop at a node's rim
        Q = [P(*q) for q in pts]
        for i_, j_, r_ in ((0, 1, r0), (-1, -2, r1)):
            if r_:
                a, b = Q[i_], Q[j_]
                dl = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
                Q[i_] = (a[0] + (b[0] - a[0]) * r_ * k / dl, a[1] + (b[1] - a[1]) * r_ * k / dl)
        if dash:
            for d_ in dashes(Q, 1.0 * k, 0.7 * k):
                B.line(d_, col, L, 62, bk_lw(0.25, k))
        else:
            B.line(Q, col, L, 62, bk_lw(0.25, k))
        if head:
            her21_head(B, Q[-2], Q[-1], k, col, L)
    tx(u"How the places meet across the Selinos", 0, 3.5, bold=True, hh=ht)
    tx(place_name("side_NE").upper() + u" · " + place_name("bank_NE_short"), 0, 9.5, col=INK2, bold=True)
    # the stream, downstream to the right; the bridges across it, Kızıl Avlu over it, the stream walk along it
    a, b = P(0, 31), P(95, 37)
    B.fill([rect(a[0], b[1], b[0], a[1])], HER21_WATER, L, 60)
    tx(place_name("stream"), 1.5, 35.0, col=WHITE, bold=True)
    her21_head(B, P(89.5, 34), P(93.5, 34), k, WHITE, L, order=61, mm=2.2)
    a, b = P(30, 34), P(52, 34)
    B.line([a, b], acc, L, 61, bk_lw(1.5, k))
    for d_ in dashes([a, b], 1.2 * k, 0.9 * k):
        B.line(d_, WHITE, L, 61, bk_lw(0.3, k))
    for bx in (30.0, 52.0, 87.0):
        a, b = P(bx - 0.8, 30), P(bx + 0.8, 38)
        B.fill([rect(a[0], b[1], b[0], a[1])], INK, L, 62)
    a, b = P(62, 29.5), P(76, 38.5)
    B.fill([rect(a[0], b[1], b[0], a[1])], acc, L, 62)
    tx(landmark_name("kizil_avlu"), 69, 34.95, "C", WHITE, True)
    node(62, 29.5, "kizilavlu")
    node(30, 34, "k4")
    node(52, 34, "k3")
    # v58 (round 3, P20.3 / G16): names, no K-codes. The walk's two bridges short (full in the strip below, same
    # drawing), set right of their bars; Üç Kemer Köprüsü in full on two lines centred on its bar
    tx(bridge_name("K4", short=True), 31.3, 41.5, "L", bold=True)
    tx(bridge_name("K3", short=True), 53.2, 41.5, "L", bold=True)
    k5a, k5b = (bridge_name("K5").rsplit(u" ", 1) + [u""])[:2]
    tx(k5a, 87, 41.5, "C", bold=True)
    if k5b:
        tx(k5b, 87, 45.0, "C", bold=True)
    tx(u"stream walk", 32, 29.0, "L", acc, True)          # v60 (round 5): no length (no horizontal dimensions)
    # the Kale side
    for key, a_ in (("ulucami", 30), ("akropol", 60), ("teleferik", 88)):
        node(a_, 18, key)
    tx(landmark_name("ulucami"), 30, 14.5, "C", bold=True)
    tx(landmark_name("akropol"), 60, 14.5, "C", bold=True)
    tx(landmark_name("teleferik"), 95, 14.5, "R", bold=True)
    link([(88, 18), (60, 18)], head=True, r0=1.7, r1=1.3)            # Teleferik -> Akropol
    tx(u"cable car, 2010", 74, 22.5, "C", INK2, italic=True)
    link([(30, 34), (30, 18)], r0=1.7, r1=1.3)                       # K4 -> Ulucami
    tx(u"to the mosque", 28.5, 26.0, "R", INK2, italic=True)
    # the bazaar side
    for key, a_ in (("asklepion", 5), ("muze", 26), ("hamam", 44), ("arasta", 74)):
        node(a_, 56, key)
    tx(landmark_name("asklepion"), 0.5, 61.5, "L", bold=True)
    tx(landmark_name("tabaklar_hamami"), 44, 61.5, "C", bold=True)
    tx(landmark_name("arasta") + u" (Hacı Hekim)", 74, 61.5, "C", bold=True)
    link([(26, 57.7), (26, 63.4)], col=INK2)                          # Bergama Müzesi: its name one row lower
    tx(landmark_name("bergama_muzesi"), 26, 66.0, "C", bold=True)
    link([(5, 56), (5, 37)], head=True, r0=1.7)                       # Asklepion -> the stream: Roman coins
    tx(u"Selinos on", 7, 45.0, "L", INK2, italic=True)
    tx(u"Roman coins", 7, 48.5, "L", INK2, italic=True)
    link([(26, 37), (26, 56)], head=True, r1=1.7)                     # the banks' digs -> the museum
    tx(u"digs on", 28, 45.0, "L", INK2, italic=True)
    tx(u"the banks", 28, 48.5, "L", INK2, italic=True)
    link([(51, 37.2), (44, 56)], r1=1.3)                              # the tanneries at K3 -> the tanners' bath
    tx(u"tanneries", 50.5, 47.0, "L", INK2, italic=True)
    link([(44, 56), (74, 56)], head=True, r0=1.3, r1=1.7)             # leather -> parchment
    tx(u"parchment, 2026", 59, 53.8, "C", INK2, italic=True)
    link([(74, 38.5), (74, 56)], dash=True, r1=1.7)                   # Kermes at both
    tx(u"Kermes 2024", 76, 50.5, "L", INK2, italic=True)   # v58: one row lower, under Üç Kemer Köprüsü
    tx(place_name("side_SW").upper() + u" · " + place_name("bank_SW_short"), 95, 71.5, "R", INK2, True)
    tx(u"Not to scale. Numbers: loop stops, as on the map.", 0, 76.0, "L", INK2)


# v60 (round 5, D5): restored from 5249425 (removed in d16192e)
def her21_walk_strip(B, x0, ytop, w, k, L, walk_m, offers, num, boxes=None):
    """v58 (round 3, P20.2): where the loop meets the channel, a strip (not to scale) under the diagram in the same
    cell, HER21_STRIP_MM tall, laid out in mm on the diagram's 95 mm design width (y down): the Selinos band, the
    stream walk on it from Ulucami Önü Köprüsü (upstream, left) to Tabak Köprüsü, the two bridges as bars with their
    loop numbers and full names, and the project's places on the walk (offers: [(t, name)], her21_offers) as squares
    at their place along it, each name under its square (a second row where the first is taken). boxes (list) gets
    every word's box in booklet mm. v60 (round 5, D5): restored from 5249425 (removed in d16192e) with the loop's
    colour HER21_LOOP_C, the shared markers (her21_mk), a text group per word and no length in the texts (round 5:
    no horizontal dimensions); its warnings by wn_warn. walk_m is kept for the caller."""
    fx = w / (HER21_DIA_MM[0] * k)
    P = lambda a, b: (x0 + a * fx * k, ytop - b * k)
    hd, ht = bk_hk(HER21_PT["dia"], k), bk_hk(HER21_PT["title"], k)
    acc = HER21_LOOP_C

    def tx(s_, a, b, align="L", col=INK, bold=False, italic=False, hh=None):
        p = P(a, b)
        B.text(s_, p[0], p[1], hh or hd, col, L, order=66, font=FONT_TITLE, bold=bold, align=align, italic=italic,
               tg=her21_tg(B))
        if boxes is not None:
            tw_ = her_tw(s_, hh or hd, bold)
            xl = p[0] - {"C": 0.5 * tw_, "R": tw_}.get(align, 0.0)
            boxes.append((xl / k, p[1] / k, (xl + tw_) / k, (p[1] + (hh or hd)) / k))
    tx(u"Where the loop meets the channel", 0, 4.0, bold=True, hh=ht)
    xa, xb, yc = 6.0, 89.0, 13.5                          # the walk's ends (K4, K3) and the band's centre line
    a, b = P(0, 11), P(95, 16)                            # the Selinos, downstream to the right (as above)
    B.fill([rect(a[0], b[1], b[0], a[1])], HER21_WATER, L, 60)
    her21_head(B, P(91.0, yc), P(94.5, yc), k, WHITE, L, order=61, mm=2.0)
    a, b = P(xa, yc), P(xb, yc)                           # the stream walk on it
    B.line([a, b], acc, L, 61, bk_lw(1.5, k))
    for d_ in dashes([a, b], 1.2 * k, 0.9 * k):
        B.line(d_, WHITE, L, 61, bk_lw(0.3, k))
    tx(u"stream walk", 0.5 * (xa + xb), 9.0, "C", acc, True)   # v60 (round 5): no length (no horizontal dimensions)
    for bx, key in ((xa, "k4"), (xb, "k3")):              # the two bridges: bars, loop numbers as on the map
        a, b = P(bx - 0.8, 10), P(bx + 0.8, 17)
        B.fill([rect(a[0], b[1], b[0], a[1])], INK, L, 62)
        n_ = num.get(key)
        if n_:
            p = P(bx, yc)
            her21_mk(B, p[0], p[1], str(n_), k, L, order=64)
    sq = 1.1                                              # mm: half a project place's square
    for t_, nm in offers:
        p = P(xa + (xb - xa) * t_, yc)
        B.fill([rect(p[0] - sq * k, p[1] - sq * k, p[0] + sq * k, p[1] + sq * k)], INK, L, 63)
    # the names under the band: the bridges' full names at the two ends, the places under their squares, each in
    # the first row (21, 24.5, 28 mm) where it touches no other name
    rows_y = (21.0, 24.5, 28.0)
    used = [[] for _ in rows_y]                           # per row: (left, right) in design mm
    wmm = lambda s_, bold: her_tw(s_, hd, bold) / (fx * k)
    n4, n3 = bridge_name("K4"), bridge_name("K3")
    tx(n4, 0, rows_y[0], "L", bold=True)
    used[0].append((0.0, wmm(n4, True)))
    tx(n3, 95, rows_y[0], "R", bold=True)
    used[0].append((95.0 - wmm(n3, True), 95.0))
    left = []
    for t_, nm in offers:
        c = xa + (xb - xa) * t_
        ww = wmm(nm, False)
        l0 = min(max(0.0, c - 0.5 * ww), 95.0 - ww)
        for j, yr in enumerate(rows_y):
            if all(l0 + ww + 1.5 <= u0 or u1 + 1.5 <= l0 for u0, u1 in used[j]):
                tx(nm, l0, yr, "L")
                used[j].append((l0, l0 + ww))
                break
        else:
            left.append(nm)
    if left:
        wn_warn("p22", "strip_row", u"heritage loop strip: no row for {}.".format(u", ".join(left)))
    if not offers:
        LOG.append(u"Heritage loop strip: no city-link place lies on the stream walk; the strip shows the walk only.")
    yk = max([rows_y[j] for j in range(len(rows_y)) if used[j]] + [rows_y[0]]) + 4.5
    p = P(0.0, yk - 0.5 * hd / k)                         # the key: the square = a project place
    B.fill([rect(p[0], p[1] - sq * k, p[0] + 2 * sq * k, p[1] + sq * k)], INK, L, 63)
    tx(u"project place on the walk (city link)", 2 * sq + 1.5, yk, "L", INK2)


def her_leg():
    """v51: the page's legend rows (drawn samples, plain names): the loop, the stream walk, the Teleferik, the pins,
    the base, the study area. v59 (round 4, P20.1, P20.2): the loop's colour 8B2D2D, the contours' green ramp, the
    muted base's house tone; the Teleferik's name from the table."""
    return [("line", HER21_LOOP_C, u"Heritage loop, stop to stop"),
            ("thick", HER21_LOOP_C, u"Stream walk {} – {} along the Selinos: the loop's spine (project)".format(
                bridge_name("K4"), bridge_name("K3"))),           # v58 (round 3, G16): names, not codes
            ("line", INK, landmark_name("teleferik") + u" (cable car)"),
            ("dot", HER21_LOOP_C, u"Loop stop, numbered in loop order"),
            ("dot", mix(HER21_LOOP_C, WHITE, 0.6), u"Heritage place"),
            ("line", C(BM_HEIGHT_RAMP[2]), u"Contour, coloured by height: lighter = lower"),
            ("box", HER21_WATER, place_name("stream")), ("box", HER21_BLD, u"Building"),
            R28_STUDY_LEG]


def her_loop_page(S, SA, B, x, top, k, L):
    """v59 (round 4, P20.1-P20.4, D3, G-R4-2; v52 PG1 p20): three M1 grid cells side by side, the crop as wide as the
    booklet's panel area (BK_AW):
      | v60 (round 5, D5): the places diagram (her21_diagram) and the stream-walk strip (her21_walk_strip) at the
        top, the four heritage places' cards under them; as wide as the right column again (round 4 had made it one
        grid column narrower when D3 removed the diagram) |
      | the map, ONE full rectangle at 1:10,000, north up, widened to its whole grid columns (more town, never
        stretched), nothing over it; its scale bar and north arrow (north_items, no plate) under it |
      | the seven loop stops' cards in stop order 1-7, their photos along the map's edge |
    A card: the photo in a rectangular window with the pin's badge in its corner (mk_marker number, or the ring of a
    heritage place), name, one line. Cards and pins are tied by that badge and the name: no leader crosses the map
    (G3). No photo credits on the page (G12): the booklet's Sources page reads them through her21_credits. One crop
    heritage_loop (booklet p20; its texts are checked by sb_text_check). The map's letter key (G3) may move the
    crop's bottom down. Returns the y below."""
    ss = 1000.0 * k / HER21_DEN
    gap = GRID_GUT * k
    mk_register("p20", {"loop": HER21_LOOP_HEX})         # G-R4-7: the markers take the loop's colour
    xy = dict((pl["key"], her21_xy(pl)) for pl in HER21_PLACES)
    num = {}
    for pl in HER21_PLACES:
        if pl.get("stop"):
            num[pl["key"]] = [j + 1 for j, s_ in enumerate(HER_STOPS) if s_["key"] == pl["stop"]][0]
    M = HER21_MARGIN_M
    pts = list(xy.values()) + [HER21_GONDOLA_TOP]
    x0, x1 = min(q[0] for q in pts) - M, max(q[0] for q in pts) + M
    y0, y1 = min(q[1] for q in pts) - M, max(q[1] for q in pts) + M
    nm = grid_cols_for((x1 - x0) * ss / k)                # the map's whole columns; the cards share the rest
    ns = max(1, (GRID_COLS - nm) // 2)                    # the stops' column (right)
    nl = ns                                               # v60 (round 5, D5): the places' column (left) as wide
    # as the stops' column again: the restored diagram's 95 mm design width (v59 P20.3 / G-R4-2 had ns - 1 once D3
    # removed the diagram; that column goes back to it)
    if nm > GRID_COLS - nl - ns:
        LOG.append(u"WARNING: heritage loop: the map needs {} grid columns; it is wider than its {} columns."
                   u"".format(nm, GRID_COLS - nl - ns))
    cwl, cw = (grid_w(nl) - 0.5) * k, (grid_w(ns) - 0.5) * k   # the crop 0.5 mm wider each side = BK_AW
    mw0 = grid_w(GRID_COLS - nl - ns) * k
    ex = 0.5 * (mw0 / ss - (x1 - x0))
    if ex > 0:                                            # the map fills its columns: more town east and west
        x0, x1 = x0 - ex, x1 + ex
    Fm = HerBox(x0, y0, x1, y1)
    mw, mh = Fm.w * ss, Fm.h * ss
    xm = x + cwl + gap
    V = View(Fm, ss, xm, top)
    r_all = (xm, top - mh, xm + mw, top)
    bot = her21_foot(B, xm, r_all[1], ss, k, L, HER_SB_M.get(HER21_DEN, 400.0))
    i0_map = sb_mark(B)                                   # v59 closing (G-R4-1): the map's own texts from here
    mres = her21_map(S, B, V, Fm, r_all, k, L, xy, num)   # dict (walk_m, walk, key_bot, labels, pins)
    sb_keep(B, r_all, u"p20 loop map", "map", i0_map)     # its pins and names may sit on it, no other text
    walk_m = mres["walk_m"]
    if mres["key_bot"] is not None:                       # the letters' key under the map may reach lower
        bot = min(bot, mres["key_bot"])
    tb = []                                               # v58 (G3): every text box of the page, booklet mm
    # v60 (round 5, D5): restored from 5249425 (removed in d16192e): the diagram's own cell at the left column's
    # top, the stream-walk strip under it; their texts are ordinary Board texts (booklet label items), no box list
    dd = HER21_DIA_MM[1] * k                              # the diagram's own cell: left column, top
    dh = dd + HER21_STRIP_MM * k                          # v58 (P20.2): + the stream-walk strip under it
    her21_diagram(B, x, top, cwl, dd, k, L, walk_m, num)
    her21_walk_strip(B, x, top - dd, cwl, k, L, walk_m, her21_offers(mres["walk"]), num)
    xr = xm + mw + gap
    ph = her21_photos()
    stops = sorted([pl for pl in HER21_PLACES if pl["key"] in num], key=lambda pl: num[pl["key"]])
    rest = [pl for pl in HER21_PLACES if pl["key"] not in num]
    cols = [("L", rest, x, x + cwl, top - dh - gap), ("R", stops, xr, xr + cw, top)]   # v60 (D5): under the strip
    pitches = []
    for side, pls, c0, c1, ct in cols:                    # side L: photo on the right (at the map), R: on the left
        if not pls:
            continue
        pitch = (ct - bot) / len(pls)
        pitches.append(pitch / k)
        for i, pl in enumerate(pls):
            g = her21_geom(pl, ph.get(pl["key"]), c0, c1, ct - (i + 0.5) * pitch, pitch, side, k)
            her21_card(B, pl, ph.get(pl["key"]), g, num.get(pl["key"]), k, L, tb)
    right = xr + cw
    crop_panel("heritage_loop", x - 0.5 * k, bot - 0.5 * k, right + 0.5 * k, top + 0.5 * k,
               u"The heritage loop: eleven places on both banks of the Selinos, joined by the stream walk {} – {}"
               u"".format(bridge_name("K4"), bridge_name("K3")),        # v58 (round 3, G16): names, not codes
               crop_scale(ss), crop_legend(her_leg()))
    lp_overlap_flag("p20", tb + mres["labels"], drawing_boxes=mres["pins"],      # v58 (round 3, G3): once per page
                    bounds=((x - 0.5 * k) / k, (bot - 0.5 * k) / k, (right + 0.5 * k) / k, (top + 0.5 * k) / k))
    CROP_PANELS[-1]["bk_w"] = (right - x) / k + 1.0       # its width on the booklet page, mm (the map prints 1:10,000)
    LOG.append(u"Heritage loop (p20, v59): map 1:10,000, {:,.0f} x {:,.0f} m ({:.0f} x {:.0f} mm, {} grid columns; "
               u"v60: the places diagram and the stream-walk strip restored, D5), muted base with coloured contours, loop "
               u"{} {:.1f} mm in front; {} + {} cards in rectangular windows ({} mm slots); stream walk {} – {} "
               u"{:,.0f} m; no photo credits on the page ({} Commons credit line(s) for the Sources page)."
               u"".format(Fm.w, Fm.h, mw / k, mh / k, GRID_COLS - nl - ns, HER21_LOOP_HEX, HER21_LOOP_MM, len(rest),
                          len(stops), u" / ".join(u"{:.0f}".format(p_) for p_ in pitches), bridge_name("K4"),
                          bridge_name("K3"), walk_m, len(her21_credits())))
    return bot


def draw_heritage_loop(S, B, x, y, w, U):
    """v52 (revision 30 Oct 2026, PG1 p20; v51 WO-T3a-6, package G): THE HERITAGE LOOP: her_loop_page (crop
    heritage_loop: v59 (round 4) the map at 1:10,000 on the muted basemap as one full rectangle, the photo cards in
    rectangular windows beside it, no diagram, no credits). Sized for the booklet page: k = board units per booklet mm of
    a drawing 120 U wide, as every theme-B map. Returns the y below."""
    L = "LU_BOARD::HeritageLoop"
    B.text("CITY HERITAGE LOOP", x, y, 1.05 * U, INK, L, font=FONT_TITLE, bold=True)
    k = 120.0 * U / BK_AW
    SA = getattr(S, "whole", None) or S
    ext = globals().get("HER_EXTENT", "loop")            # the core may drop it (WO-T3a-6 core request 1)
    if ext != "loop":
        LOG.append(u"Heritage loop: HER_EXTENT \"{}\" is no longer used (v51: one map on the shared basemap)."
                   u"".format(ext))
    return her_loop_page(S, SA, B, x, y - 1.2 * U, k, L) - 1.0 * U
