# p.21 the heritage loop (split from parts/15f_v46_pages.py, parts/15j_r28_heritage.py on 29 Oct 2026; v51 rebuilt for package G, WO-T3a-6)


def soft_line(B, P, col, k, L, order, w_mm=2.4, t=0.5):
    """v46: a proposal line drawn soft: three multiplying strokes of col, from a pale halo w_mm wide on the booklet
    page to a narrow core (t = how pale the core is): no hard edge, no width that reads as decided."""
    for f, dt in ((1.0, 0.36), (0.6, 0.18), (0.28, 0.0)):
        B.line(P, tint(col, min(0.97, t + dt)), L, order, bk_lw(w_mm * f, k))


def her_tw(txt, h, bold=False):
    """v50 (G5): the printed width (board units) of txt in Arial at capital height h: the font size is h / 0.718, as
    the PDF writer sets it (_PDF_CAP)"""
    w = HER_W[1 if bold else 0]
    return sum(w.get(c, 556) for c in txt) / 1000.0 * h / 0.718


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
    """v50 (G5): txt (** = bold) broken into lines of words no wider than width at capital height h"""
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
    return lines


def her_line(B, words, x, y, h, col, L, order=40):
    """v50 (G5): one line of her_wrap, its plain and bold runs each one live text at its measured width; returns the
    x after it"""
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
        B.text(s_, cx, y, h, col, L, order=order, font=FONT_TITLE, bold=b_)
        cx += her_tw(s_, h, b_)
    return cx


def her_walk(S, pts):
    """v50 (P20.2): the stream walk K3 -> K4 along the stream's centre line (the longest piece of S.selinus) every
    10 m, and its length along the stream (m); a straight line when the centre line is missing or misses a bridge"""
    a, b = pts[HER_WALK["frm"]], pts[HER_WALK["to"]]
    streams = [P for P in (getattr(S, "selinus", None) or []) if len(P) >= 2]
    main = max(streams, key=pl_length) if streams else None
    if main is None or max(pl_dist(a[0], a[1], main, False), pl_dist(b[0], b[1], main, False)) > HER_SNAP_M:
        LOG.append("Heritage loop: the stream's centre line misses K3 or K4 (over {:.0f} m), so the stream walk is "
                   "drawn straight.".format(HER_SNAP_M))
        return [a, b], math.hypot(b[0] - a[0], b[1] - a[1])
    s0, s1 = pl_chainage(main, a[0], a[1]), pl_chainage(main, b[0], b[1])
    nn = max(2, int(abs(s1 - s0) // 10.0))
    return [pl_point_at(main, s0 + (s1 - s0) * i / float(nn))[0] for i in range(nn + 1)], abs(s1 - s0)


def her_labels(B, items, taken, bounds, k, L, segs=(), order=66):
    """v52 (PG1 p20, M2; v50 G4): names on a map placed by the shared lp_place (in booklet mm): beside the point,
    else on a short leader (at most HER21_LEADER_MM where any spot allows) that starts on the symbol's rim and never
    crosses another leader, a name, a symbol or the loop's lines; else 0.9 / 0.8 x the size. Rank 1 (a heritage place,
    the stream) is left out when it finds no spot (logged), rank 0 (a stop, an arrow) always shows. items: dicts
    lines, x, y (board units), h, col, bold (first line), italic, rank, r0 (the symbol's radius). taken: the symbols'
    boxes (board units), grown by the names; segs: the loop's lines (no name sits on them). Returns the items left
    out."""
    if not items:
        return []
    pad = 0.35                                            # mm round the words
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
    got = lp_place(pl, tk, ln, bd, pad=0.5, max_leader=HER21_LEADER_MM)
    left = []
    for i, it in enumerate(items):
        g = got[i]
        if g is None:
            left.append(it)
            LOG.append(u"Heritage loop: no free spot for the name \"{}\"{}.".format(
                u" / ".join(it["lines"]), u", left out" if it.get("rank", 0) else u" (WARNING: a stop's name)"))
            continue
        b, ldr = g["box"], g["leader"]
        h = it["h"] * g["size"]
        bx = (b[0] * k, b[1] * k, b[2] * k, b[3] * k)
        for j, l_ in enumerate(it["lines"]):
            B.text(l_, bx[0] + pad * k, bx[3] - pad * k - h - j * HER_LEAD * h, h, it["col"], L, order=order,
                   font=FONT_TITLE, bold=bool(it.get("bold")) and j == 0, italic=bool(it.get("italic")))
        if ldr:                                           # the leader: the symbol's rim -> the box's nearer side
            B.line([(ldr[0][0] * k, ldr[0][1] * k), (ldr[1][0] * k, ldr[1][1] * k)], it["col"], L, order - 1,
                   bk_lw(0.13, k))
        taken.append(bx)
    return left


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
# - The stream walk K3-K4 (the project's spine) drawn as a path along the water and named on the map.
# - Place names on the map Turkish only (G6, strict). Photos from HER21_PHOTO_DIR: own site photos (no credit, D13)
#   and the Commons set (credit lines from its photos.csv); a missing photo = an empty round slot with the name.
# - Build once (Aras 29 Oct 19:18): basemap_items is memoised; photos.csv, the photo files and their sizes are read
#   once per run (_HER21_PH).
# v52 (revision 30 Oct 2026, PG1 p20): the map is ONE full rectangle (no tab, nothing over it) in its own M1 grid
# cells; the diagram has its own cell above the left card column; the cards say a name + one line and sit in stop
# order beside the map, tied to their pins by the shared badge (numbered stops) or name: no leader crosses the map;
# the map's names are placed by M2 lp_place (short leaders that never cross); no photo credits on the page (they go
# to the booklet's Sources page through her21_credits).
HER21_DEN = 10000              # the map's scale on the booklet page
HER21_MARGIN_M = 90.0          # m of map round the outermost places and the Teleferik's top station (every side)
HER21_PHOTO_MM = 22.0          # mm: the largest photo circle
HER21_DIA_MM = (95.0, 80.0)    # mm: the diagram's design width (3 grid columns) and its cell's height
HER21_LEADER_MM = 6.0          # mm: the longest leader of a name on the map (M2, G3)
HER21_PT = dict(name=8.0, txt=7.5, lab=7.5, dia=7.5, title=8.5, num=7.5)   # booklet pt (body minimum 7.5)
# Photos: Downloads/Bergama/Data/heritage_photos/ holds (a) the own site photos by their file names below (copied
# from revision_2026-10-29/T1/photos/files/; no credit, D13) and (b) the Commons set from Aras's other account
# (Bergama_assets_2026-10.zip unpacked here: photos.csv + its photo files, beside it or in photos/). photos.csv
# columns read: file, place, credit (or "credit line"); other columns are ignored. The place column is matched to
# the places below by their aliases (Turkish letters folded).
HER21_PHOTO_DIR = os.path.join(DATA_DIR, "heritage_photos")
HER21_PHOTO_CSV = "photos.csv"
HER21_GONDOLA_TOP = (30460.0, 33003.0)     # Teleferik top station, OSM node 2295928363 (h03 Q3), h01 §0 lat/lon fit
HER21_K5 = (30294.0, 31792.0)              # Üç Kemer Köprüsü (K5), h01 §0 survey frame / §5 P09
HER21_WATER, HER21_BLD = C("91ADB4"), C("D3D0CB")    # basemap BM_COL water, BM_FAINT bld (legend samples)
# The places (map pins and cards). stop = HER_STOPS key (its loop number), dot = HER_DOTS name; name = the map's
# Turkish name, title = the card's. txt (v52, PG1 p20): ONE line under the card's name, key words bold (G4); the
# v51 Why / Use / Now / Project texts are cut to it (their facts stay in the cards h01-h03 noted per place). Sources (library cards h01 = selinos_bergama_history_context_v1, h02 = selinos_site_history_inaccessible_
# edges_v1, h03 = bergama_history_hubs_research_v1) are noted per place; nothing here is printed as a source.
HER21_PLACES = [
    # h01 §5 P01; h02 §2.9 (inscribed 22.06.2014); h03 Q2 (ICOMOS 2014 s13 p287: tour groups, up by the gondola)
    dict(key="akropol", name=u"Akropol", own=(), alias=(u"akropol", u"acropolis", u"trajaneum"),
         txt=u"**World Heritage** hill city: the loop's goal"),
    # h01 §5 P33 (2010, 700 m line, s115); h03 Q2 (ICOMOS s13 p287)
    dict(key="teleferik", stop="gondola", name=u"Teleferik", own=(), alias=(u"teleferik", u"gondola", u"cablecar"),
         txt=u"**cable car** (2010): the loop starts here"),
    # h01 §5 P02-P04; h02 §2.3 (tunnels, s13), §3 Worship (N rotunda = mosque), §4.3 (closed since 03/2025, aim
    # 2026, s41); h03 Q5 (Kermes 2024 concerts in Kızıl Avlu)
    dict(key="kizilavlu", stop="redhall", name=u"Kızıl Avlu", own=(),
         alias=(u"kizilavlu", u"redhall", u"redbasilica", u"serapis", u"serapeion"),
         txt=u"Hadrian's temple, **built over the stream**"),
    # h01 §5 P08; h02 §2.5 (KE s29: Roman 2nd-3rd c., tanneries), E03 (DSİ walls 2020-), §4.6 (tourist signs at K3,
    # s63); h03 Q1 (lines 831-833 at Tabak Köprüsü, s124)
    dict(key="k3", stop="K3", name=u"Tabak Köprüsü (K3)", own=(u"tabak_koprusu_1.jpg", u"tabakhane_1.jpg"),
         alias=(u"tabakkoprusu", u"tabakhanekoprusu", u"tabakhane"),
         txt=u"**Roman bridge**: the stream walk starts"),
    # h01 §5 P06; h02 §2.5 (s31 two spans, Ottoman small arch; KGM plaque 2024-2025, s63); h03 Q1 (Camikebir Cd.)
    dict(key="k4", stop="K4", name=u"Ulucami Önü Köprüsü (K4)", own=(u"ulucami_onu_koprusu_1.jpg",
                                                                    u"ulucami_onu_koprusu_2.jpg"),
         alias=(u"ulucamionukoprusu", u"ulucamionu"),
         txt=u"bridge to **Ulu Cami**: the stream walk ends"),
    # h01 §5 P05 (1398-99, Bayezid I, restored 1905, minaret 1949), P11 (Bergama Müzesi digs 2021-23, s4); h02 §3
    # Worship (Ulu Cami at K4)
    dict(key="ulucami", dot=u"Ulu Cami", name=u"Ulu Cami", own=(u"ulu_cami_1.jpg",), alias=(u"ulucami",),
         notalias=(u"onu", u"koprusu"),
         txt=u"**mosque** of 1398-99 at the K4 bridge"),
    # h01 §5 P07; h02 §2.5 (s32: opposite Ulu Cami, named after the tanneries; sign s63: camekan dome survives),
    # §3 Bathing (ruin since the 1842/47 flood, enclosed by 5 houses), §2.9 (s57: municipal survey drawings)
    dict(key="hamam", dot=u"Tabaklar Hamamı", name=u"Tabaklar Hamamı", own=(u"tabaklar_hamami_1.jpg",
                                                                         u"tabaklar_hamami_2.jpg"),
         alias=(u"tabaklarhamami",),
         txt=u"Ottoman **tanners' bath**, now a ruin"),
    # h01 §5 P23 (1513; Parchment Museum 2026, s99 s45); h02 §3 (Parchment Museum opened 28.02.2026); h03 Q4
    # (Çınarlı Kahve plane ~380-400 yr, pipe-irrigated, AA 2026), Q5 (Kermes 2024 events at the Arasta, Çınarlı Kahve)
    dict(key="arasta", stop="bazaar", name=u"Arasta", title=u"Arasta (Hacı Hekim)", own=(),
         alias=(u"arasta", u"hacihekim", u"cinarlikahve"),
         txt=u"**bazaar** of 1513; its hamam: Parchment Museum"),
    # h01 §5 P09; h02 §2.5 (s30: three arches, repairs altered its character), §2.9 (first stage 1,380 m Kazancı ->
    # Üçkemer, s33 s36), E01 (the tunnels end before K5); h03 Q1 (lines 656, 831-833 at Üç Kemer Köprüsü)
    dict(key="k5", xy=HER21_K5, name=u"Üç Kemer Köprüsü (K5)", own=(), alias=(u"uckemer", u"threearch"),
         txt=u"**Roman bridge**: the stream comes out"),
    # h01 §5 P24 (1936, archaeology + carpets, s85 s86), §3 Archaeology (museum + DAI digs on the banks 2011-2025)
    dict(key="muze", stop="museum", name=u"Bergama Müzesi", own=(),
         alias=(u"bergamamuzesi", u"bergamamuseum", u"archaeologymuseum", u"muze"),
         txt=u"**museum** of 1936: Pergamon's finds"),
    # h01 §5 P28 (4th c. BC, Hadrianic, sacred spring, s114 s81); h03 Q2 (KTB: car parking; OSM ticket building,
    # paid car park)
    dict(key="asklepion", stop="asklepieion", name=u"Asklepion", own=(), alias=(u"asklep", u"asclep"),
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
        d, len(out), len(HER21_PLACES), (u"; empty round slots for " + u", ".join(miss)) if miss else u""))
    _HER21_PH["map"] = out
    return out


def her21_credits():
    """v51 (D13; interface for the booklet's Sources page): [(place, credit line)] of the Commons photos the page
    shows, from photos.csv; own photos carry none"""
    ph = her21_photos()
    return [(pl.get("title", pl["name"]), ph[pl["key"]][1]) for pl in HER21_PLACES
            if pl["key"] in ph and ph[pl["key"]][1]]


def her21_head(B, a, b, k, col, L, order=63, mm=1.8):
    """v51: a filled arrowhead with its tip at b, pointing from a"""
    dx, dy = b[0] - a[0], b[1] - a[1]
    dl = math.hypot(dx, dy) or 1.0
    ux, uy, s = dx / dl, dy / dl, mm * k
    c = (b[0] - ux * s, b[1] - uy * s)
    B.fill([[b, (c[0] - uy * 0.42 * s, c[1] + ux * 0.42 * s), (c[0] + uy * 0.42 * s, c[1] - ux * 0.42 * s)]], col, L,
           order)


def her21_base(CB, items, V, k, L):
    """v51 (02 §1): the shared basemap's items (survey m) through CB, bottom first, at orders 2-28 (under the loop)"""
    n, i = max(1, len(items)), [0]

    def od():
        i[0] += 1
        return 2 + int(26.0 * (i[0] - 1) / n)

    def col(hx, a):
        c = C(hx)
        return c if a is None or a >= 0.999 else mix(c, WHITE, 1.0 - a)

    def fill_fn(rings, hx, a, nz):
        c = col(hx, a)
        CB.fill(rings, r28_nz(c) if nz else c, L, od())

    def line_fn(P, hx, w, dash, a):
        o = od()
        if dash:
            for d_ in dashes(P, dash[0] * k, dash[1] * k if len(dash) > 1 else dash[0] * k):
                CB.line(d_, col(hx, a), L, o, bk_lw(w, k))
        else:
            CB.line(P, col(hx, a), L, o, bk_lw(w, k))
    return basemap_draw(items, lambda p: V.p(p[0], p[1]), fill_fn, line_fn)


def her21_geom(pl, ph, x0, x1, cy, pitch, side, k):
    """v51: a card's parts in its slot (x0..x1, centred on cy, pitch tall): the photo circle (cx, cy, r), the
    picture's rectangle (cover: the circle filled, the picture kept inside the slot), the text's x range. side "L":
    the photo on the right (towards the map), "R": on the left."""
    D = min(HER21_PHOTO_MM, pitch / k - 4.0) * k
    iw = ih = D
    wh = her21_img(ph[0]) if ph else None
    if wh:
        a = wh[0] / wh[1]
        if a < 1.0:                                      # portrait: keep the picture inside the slot
            D = min(D, (pitch - 1.0 * k) * a)
            iw, ih = D, D / a
        else:
            iw, ih = min(D * a, 1.6 * D), min(D * a, 1.6 * D) / a
    wb = max(iw, D)
    cx = x1 - 0.5 * wb if side == "L" else x0 + 0.5 * wb
    t0, t1 = (x0, x1 - wb - 3.0 * k) if side == "L" else (x0 + wb + 3.0 * k, x1)
    return dict(cx=cx, cy=cy, r=0.5 * D, img=(cx - 0.5 * iw, cy - 0.5 * ih, cx + 0.5 * iw, cy + 0.5 * ih),
                t0=t0, t1=t1, side=side, pitch=pitch)


def her21_card(B, pl, ph, g, num, k, L):
    """v52 (PG1 p20; v51 R08 idea): the round photo (or an empty round slot with the place's name), on its rim the
    badge of its map pin (the loop number of a stop, the ring of a heritage place), the place's name and its one line
    (keywords bold) beside it. No credits on the page (G12: the Sources page)."""
    cx, cy, r = g["cx"], g["cy"], g["r"]
    circ = circle_pts(cx, cy, r, 72)
    if ph:
        q = g["img"]
        B.image(ph[0], q[0], q[1], q[2], q[3], L, order=5)
        m_ = 0.3 * k
        B.fill([rect(min(q[0], cx - r) - m_, min(q[1], cy - r) - m_, max(q[2], cx + r) + m_, max(q[3], cy + r) + m_),
                circ], WHITE, L, 6)                        # the picture outside the circle hidden (even-odd)
        B.line(circ + [circ[0]], INK, L, 7, bk_lw(0.3, k))
    else:
        B.fill([circ], mix(INK2, WHITE, 0.88), L, 5)
        B.line(circ + [circ[0]], INK2, L, 7, bk_lw(0.25, k))
        h = bk_hk(HER21_PT["txt"], k)
        ls = her_wrap(pl["name"], h, 1.6 * r)
        y0 = cy + 0.5 * (len(ls) - 1) * HER_LEAD * h - 0.5 * h
        for j, ln in enumerate(ls):
            s_ = u" ".join(u"".join(t_ for t_, b_ in wd) for wd in ln)
            B.text(s_, cx, y0 - j * HER_LEAD * h, h, INK2, L, order=40, font=FONT_TITLE, align="C")
    bx = cx + (-0.707 if g["side"] == "L" else 0.707) * r   # the badge, on the rim away from the map
    by = cy + 0.707 * r
    if num:
        cb = circle_pts(bx, by, 2.3 * k, 24)
        B.fill([cb], HER_ACC, L, 60)
        B.line(cb + [cb[0]], WHITE, L, 61, bk_lw(0.3, k))
        B.text(str(num), bx, by, bk_hk(HER21_PT["num"], k), WHITE, L, order=62, font=FONT_TITLE, bold=True,
               align="MC")
    else:                                                 # a heritage place: the ring of its pin
        cb = circle_pts(bx, by, 1.6 * k, 24)
        B.fill([cb], WHITE, L, 60)
        B.line(cb + [cb[0]], HER_ACC, L, 61, bk_lw(0.45, k))
    hn, h = bk_hk(HER21_PT["name"], k), bk_hk(HER21_PT["txt"], k)
    pt = HER_PITCH * h
    ls = her_wrap(pl["txt"], h, g["t1"] - g["t0"])
    bh = hn + 0.6 * pt + len(ls) * pt
    y = min(cy + 0.5 * bh, cy + 0.5 * g["pitch"])
    B.text(pl.get("title", pl["name"]), g["t0"], y - hn, hn, INK, L, font=FONT_TITLE, bold=True)
    y -= hn + 0.6 * pt
    for ln in ls:
        her_line(B, ln, g["t0"], y - h, h, INK, L)
        y -= pt
    if bh > g["pitch"] - 1.0 * k:
        LOG.append(u"WARNING: heritage loop card \"{}\": its text is {:.1f} mm tall in a {:.1f} mm slot.".format(
            pl["name"], bh / k, g["pitch"] / k))


def her21_map(S, B, V, Fm, r_all, k, L, xy, num):
    """v52 (PG1 p20; v51 package G): the loop map, ONE full rectangle r_all (nothing over it, no tab): the simple
    basemap, the study area (G8), the legs stop to stop (soft), the Teleferik's line, the stream walk K3-K4 as a path
    along the water (solid band, white dashes) named on the map, the pins (loop stops numbered, other places as
    rings), the Turkish names placed by M2 lp_place clear of the pins and the lines (her_labels: short leaders that
    never cross). No card leaders: the cards beside the map share the pins' badges and names. Returns the stream
    walk's length (m)."""
    rs = [r_all]
    CB = Her21Clip(B, rs)
    B.fill([rect(*r_all)], WHITE, L, 1)
    items = basemap_items("simple", box=Fm.bb)            # memoised (common/basemap.py)
    if not items:
        LOG.append(u"WARNING: heritage loop: no basemap data (cached/basemap/basemap.json missing): the map shows the "
                   u"loop on white.")
    her21_base(CB, items, V, k, L)
    draw_r28_study(S, CB, V, k, L)                        # G8: the study area's outline
    acc = HER_ACC
    ins = lambda p: r_all[0] <= p[0] <= r_all[2] and r_all[1] <= p[1] <= r_all[3]
    segs, taken, labs = [], [], []

    def keep(P):
        for run in clip_rect_line(list(P), r_all):
            segs.extend(zip(run[:-1], run[1:]))
    pts = dict((s_["key"], s_["xy"]) for s_ in HER_STOPS)
    order = [s_["key"] for s_ in HER_STOPS]
    walk, walk_m = her_walk(S, pts)
    for a, b in zip(order[:-1], order[1:]):               # the legs, soft (a proposal), no dashes
        if (a, b) == (HER_WALK["frm"], HER_WALK["to"]):
            continue
        P = [V.p(*pts[a]), V.p(*pts[b])]
        soft_line(CB, P, acc, k, L, 31, w_mm=1.2, t=0.3)
        keep(P)
    Pw = V.P(walk)                                        # the stream walk: a path along the water
    CB.line(Pw, acc, L, 33, bk_lw(1.5, k))
    for d_ in dashes(Pw, 1.2 * k, 0.9 * k):
        CB.line(d_, WHITE, L, 34, bk_lw(0.3, k))
    keep(Pw)
    taken.extend((q[0] - 0.9 * k, q[1] - 0.9 * k, q[0] + 0.9 * k, q[1] + 0.9 * k) for q in Pw[::3] if ins(q))
    mid = Pw[len(Pw) // 2]
    labs.append(dict(lines=[u"Stream walk K3-K4", u"{:,.0f} m along the Selinos".format(walk_m)], x=mid[0], y=mid[1],
                     h=bk_hk(HER21_PT["lab"], k), col=acc, bold=True, rank=0, r0=0.8 * k))
    ga, gb = V.p(*xy["teleferik"]), V.p(*HER21_GONDOLA_TOP)   # the Teleferik: its cable, ticked
    CB.line([ga, gb], INK, L, 32, bk_lw(0.25, k))
    dx, dy = gb[0] - ga[0], gb[1] - ga[1]
    dl = math.hypot(dx, dy) or 1.0
    for i in range(1, int(dl / (2.5 * k))):
        c = (ga[0] + dx * i * 2.5 * k / dl, ga[1] + dy * i * 2.5 * k / dl)
        CB.line([(c[0] - dy / dl * 0.7 * k, c[1] + dx / dl * 0.7 * k), (c[0] + dy / dl * 0.7 * k,
                                                                         c[1] - dx / dl * 0.7 * k)], INK, L, 32,
                bk_lw(0.2, k))
    keep([ga, gb])
    P = [gb, V.p(*xy["akropol"])]                         # top station -> Akropol, on foot
    soft_line(CB, P, acc, k, L, 31, w_mm=1.2, t=0.3)
    keep(P)
    rd, rr = 1.7 * k, 1.3 * k
    hl = bk_hk(HER21_PT["lab"], k)
    for pl in HER21_PLACES:                               # the pins
        p = V.p(*xy[pl["key"]])
        if not ins(p):
            LOG.append(u"WARNING: heritage loop: {} lies outside the map.".format(pl["name"]))
            continue
        n_ = num.get(pl["key"])
        if n_:
            B.fill([circle_pts(p[0], p[1], rd, 24)], acc, L, 60)
            B.text(str(n_), p[0], p[1], hl, WHITE, L, order=61, font=FONT_TITLE, bold=True, align="MC")
            r0 = rd
        else:
            B.fill([circle_pts(p[0], p[1], rr, 24)], WHITE, L, 60)
            c_ = circle_pts(p[0], p[1], rr, 24)
            B.line(c_ + [c_[0]], acc, L, 61, bk_lw(0.45, k))
            r0 = rr
        taken.append((p[0] - r0, p[1] - r0, p[0] + r0, p[1] + r0))
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
            labs.append(dict(lines=[u"Bergama Çayı"], x=best[1][0], y=best[1][1], h=hl, col=MPL["water_edge"],
                             italic=True, rank=1))
    her_labels(B, labs, taken, r_all, k, L, segs)
    o = [(r_all[0], r_all[1]), (r_all[2], r_all[1]), (r_all[2], r_all[3]), (r_all[0], r_all[3])]
    B.line(o + [o[0]], INK, L, 70, bk_lw(0.25, k))
    return walk_m


def her21_diagram(B, x0, ytop, w, h, k, L, walk_m, num):
    """v52 (PG1 p20.2; replaces v51's 200 x 72 mm corner diagram that cropped the map): how the places meet across
    the Selinos, a plan diagram (not to scale) in its own grid cell above the left card column. The stream is a band
    (the seam): the Kale side (north bank) above it, the bazaar side (south bank) below; on it the bridges K4 and K3
    (loop stops, numbered as on the map and the cards), K5, Kızıl Avlu over it and the stream walk K4-K3; every
    other place is a node on its bank with ONE short named link (h01-h03: cable car 2010; the bridge to the mosque;
    the river god Selinos on Roman coins with Asklepios; museum digs on the banks 2011-2025; the bath named after the
    tanneries; the Arasta's hamam is the Parchment Museum 2026; Kermes events 2024). Laid out in mm on a 95 x 77 mm
    design grid (y down): names and captions at fixed sizes, each clear of the others at that width (checked by
    their printed widths); a wider cell only spreads it sideways."""
    fx = w / (HER21_DIA_MM[0] * k)
    if fx < 0.99 or h < 77.0 * k:                       # the cell is 94.5 mm (crop edges): 0.5 % is fine
        LOG.append(u"WARNING: heritage loop diagram: its cell is {:.0f} x {:.0f} mm, under the 95 x 77 mm it is laid "
                   u"out for: names may touch.".format(w / k, h / k))
    P = lambda a, b: (x0 + a * fx * k, ytop - b * k)
    hd, ht = bk_hk(HER21_PT["dia"], k), bk_hk(HER21_PT["title"], k)
    acc, rn, rr = HER_ACC, 1.7 * k, 1.3 * k

    def tx(s, a, b, align="L", col=INK, bold=False, italic=False, hh=None):
        p = P(a, b)
        B.text(s, p[0], p[1], hh or hd, col, L, order=66, font=FONT_TITLE, bold=bold, align=align, italic=italic)

    def node(a, b, key):                                  # a loop stop numbered as on the map, else a ring
        p, n_ = P(a, b), num.get(key)
        if n_:
            c_ = circle_pts(p[0], p[1], rn, 24)
            B.fill([c_], acc, L, 64)
            B.text(str(n_), p[0], p[1], bk_hk(HER21_PT["num"], k), WHITE, L, order=65, font=FONT_TITLE, bold=True,
                   align="MC")
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
    tx(u"KALE SIDE · north bank", 0, 9.5, col=INK2, bold=True)
    # the stream, downstream to the right; the bridges across it, Kızıl Avlu over it, the stream walk along it
    a, b = P(0, 31), P(95, 37)
    B.fill([rect(a[0], b[1], b[0], a[1])], HER21_WATER, L, 60)
    tx(u"Selinos", 1.5, 35.0, col=WHITE, bold=True)
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
    tx(u"Kızıl Avlu", 69, 34.95, "C", WHITE, True)
    node(62, 29.5, "kizilavlu")
    node(30, 34, "k4")
    node(52, 34, "k3")
    tx(u"K4", 30, 41.5, "C", bold=True)
    tx(u"K3", 53.2, 41.5, "L", bold=True)
    tx(u"K5", 87, 41.5, "C", bold=True)
    tx(u"stream walk, {:,.0f} m".format(walk_m), 32, 29.0, "L", acc, True)
    # the Kale side
    for key, a_ in (("ulucami", 30), ("akropol", 60), ("teleferik", 88)):
        node(a_, 18, key)
    tx(u"Ulu Cami", 30, 14.5, "C", bold=True)
    tx(u"Akropol", 60, 14.5, "C", bold=True)
    tx(u"Teleferik", 95, 14.5, "R", bold=True)
    link([(88, 18), (60, 18)], head=True, r0=1.7, r1=1.3)            # Teleferik -> Akropol
    tx(u"cable car, 2010", 74, 22.5, "C", INK2, italic=True)
    link([(30, 34), (30, 18)], r0=1.7, r1=1.3)                       # K4 -> Ulu Cami
    tx(u"to the mosque", 28.5, 26.0, "R", INK2, italic=True)
    # the bazaar side
    for key, a_ in (("asklepion", 5), ("muze", 26), ("hamam", 44), ("arasta", 74)):
        node(a_, 56, key)
    tx(u"Asklepion", 0.5, 61.5, "L", bold=True)
    tx(u"Tabaklar Hamamı", 44, 61.5, "C", bold=True)
    tx(u"Arasta (Hacı Hekim)", 74, 61.5, "C", bold=True)
    link([(26, 57.7), (26, 63.4)], col=INK2)                          # Bergama Müzesi: its name one row lower
    tx(u"Bergama Müzesi", 26, 66.0, "C", bold=True)
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
    tx(u"Kermes 2024", 76, 47.0, "L", INK2, italic=True)
    tx(u"BAZAAR SIDE · south bank", 95, 71.5, "R", INK2, True)
    tx(u"Not to scale. Numbers: loop stops, as on the map.", 0, 76.0, "L", INK2)


def her_leg():
    """v51: the page's legend rows (drawn samples, plain names): the loop, the stream walk, the Teleferik, the pins,
    the simple basemap, the study area"""
    return [("line", mix(HER_ACC, WHITE, 0.3), u"Heritage loop, stop to stop"),
            ("thick", HER_ACC, u"Stream walk K3-K4 along the Selinos: the loop's spine (project)"),
            ("line", INK, u"Teleferik (cable car)"),
            ("dot", HER_ACC, u"Loop stop, numbered in loop order"), ("dot", mix(HER_ACC, WHITE, 0.6), u"Heritage place"),
            ("box", HER21_WATER, u"Selinos stream (Bergama Çayı)"), ("box", HER21_BLD, u"Building"),
            R28_STUDY_LEG]


def her_loop_page(S, SA, B, x, top, k, L):
    """v52 (revision 30 Oct 2026, PG1 p20; replaces v51's map with a tab, diagram in its corner and diagonal photo
    leaders): three M1 grid cells side by side, the crop as wide as the booklet's panel area (BK_AW):
      | the diagram (its own cell, HER21_DIA_MM) over the cards of the other places |
      | the map, ONE full rectangle at 1:10,000, north up, widened to its whole grid columns (more town, never
        stretched), nothing over it; its scale bar and north arrow under it |
      | the seven loop stops' cards in stop order 1-7, their photos along the map's edge |
    A card: round photo with the pin's badge on its rim (numbered stop, or the ring of a heritage place), name, one
    line. Cards and pins are tied by that badge and the name: no leader crosses the map (G3). No photo credits on the
    page (G12): the booklet's Sources page reads them through her21_credits. One crop drw_heritage_loop. Returns the
    y below."""
    ss = 1000.0 * k / HER21_DEN
    gap = GRID_GUT * k
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
    ns = max(1, (GRID_COLS - nm) // 2)
    if nm > GRID_COLS - 2:
        LOG.append(u"WARNING: heritage loop: the map needs {} grid columns; the card columns are one column each."
                   u"".format(nm))
    cw, mw0 = (grid_w(ns) - 0.5) * k, grid_w(GRID_COLS - 2 * ns) * k   # the crop 0.5 mm wider each side = BK_AW
    ex = 0.5 * (mw0 / ss - (x1 - x0))
    if ex > 0:                                            # the map fills its columns: more town east and west
        x0, x1 = x0 - ex, x1 + ex
    Fm = HerBox(x0, y0, x1, y1)
    mw, mh = Fm.w * ss, Fm.h * ss
    xm = x + cw + gap
    V = View(Fm, ss, xm, top)
    r_all = (xm, top - mh, xm + mw, top)
    bot = b_foot(B, Fm, xm, r_all[1], ss, k, L, HER_SB_M.get(HER21_DEN, 400.0))
    walk_m = her21_map(S, B, V, Fm, r_all, k, L, xy, num)
    dh = HER21_DIA_MM[1] * k                              # the diagram's own cell: left column, top
    her21_diagram(B, x, top, cw, dh, k, L, walk_m, num)
    xr = xm + mw + gap
    ph = her21_photos()
    stops = sorted([pl for pl in HER21_PLACES if pl["key"] in num], key=lambda pl: num[pl["key"]])
    rest = [pl for pl in HER21_PLACES if pl["key"] not in num]
    cols = [("L", rest, x, x + cw, top - dh - gap), ("R", stops, xr, xr + cw, top)]
    pitches = []
    for side, pls, c0, c1, ct in cols:                    # side L: photo on the right (at the map), R: on the left
        if not pls:
            continue
        pitch = (ct - bot) / len(pls)
        pitches.append(pitch / k)
        for i, pl in enumerate(pls):
            g = her21_geom(pl, ph.get(pl["key"]), c0, c1, ct - (i + 0.5) * pitch, pitch, side, k)
            her21_card(B, pl, ph.get(pl["key"]), g, num.get(pl["key"]), k, L)
    right = xr + cw
    crop_panel("heritage_loop", x - 0.5 * k, bot - 0.5 * k, right + 0.5 * k, top + 0.5 * k,
               u"The heritage loop: eleven places on both banks of the Selinos, joined by the stream walk K3-K4",
               crop_scale(ss), crop_legend(her_leg()))
    CROP_PANELS[-1]["bk_w"] = (right - x) / k + 1.0       # its width on the booklet page, mm (the map prints 1:10,000)
    LOG.append(u"Heritage loop (PG1 p20): map 1:10,000, {:,.0f} x {:,.0f} m ({:.0f} x {:.0f} mm, {} grid columns), "
               u"simple basemap; diagram {:.0f} x {:.0f} mm in its own cell; {} + {} cards ({} mm slots); stream walk "
               u"K3-K4 {:,.0f} m; no photo credits on the page ({} Commons credit line(s) for the Sources page)."
               u"".format(Fm.w, Fm.h, mw / k, mh / k, GRID_COLS - 2 * ns, cw / k, dh / k, len(rest), len(stops),
                          u" / ".join(u"{:.0f}".format(p_) for p_ in pitches), walk_m, len(her21_credits())))
    return bot


def draw_heritage_loop(S, B, x, y, w, U):
    """v52 (revision 30 Oct 2026, PG1 p20; v51 WO-T3a-6, package G): THE HERITAGE LOOP: her_loop_page (crop
    drw_heritage_loop: the diagram of how the places meet in its own cell, the map at 1:10,000 on the simple basemap
    as one full rectangle, the photo cards beside it in stop order, no credits). Sized for the booklet page: k = board units per booklet mm of
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
