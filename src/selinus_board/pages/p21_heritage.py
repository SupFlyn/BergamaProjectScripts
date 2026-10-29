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
    """v50 (G4): names on a map placed by the shared label_place (place_labels_all, in booklet mm): beside the point,
    else farther out on a thin leader (never across a placed name or symbol), else 0.9 x the size; rank 1 (a heritage
    place, the stream) is left out when it finds no spot (logged), rank 0 (a stop, an arrow) always shows. items:
    dicts lines, x, y (board units), h, col, bold (first line), italic, rank, r0 (the symbol's radius: the leader
    starts at its rim). taken: the symbols' boxes (board units), grown by the names; segs: the loop's lines (no name
    sits on them). Returns the items left out."""
    if not items:
        return []
    pad = 0.35                                            # mm round the words
    tk = [(b[0] / k, b[1] / k, b[2] / k, b[3] / k) for b in taken]
    bd = (bounds[0] / k + 0.6, bounds[1] / k + 0.6, bounds[2] / k - 0.6, bounds[3] / k - 0.6)
    sg = [((p[0] / k, p[1] / k), (q[0] / k, q[1] / k)) for p, q in segs]
    pl = []
    for it in items:
        h, n = it["h"], len(it["lines"])
        w0 = max(her_tw(l_, h, bool(it.get("bold")) and j == 0) for j, l_ in enumerate(it["lines"])) / k
        h0 = (h + (n - 1) * HER_LEAD * h) / k
        pl.append(dict(x=it["x"] / k, y=it["y"] / k, rank=it.get("rank", 0),
                       wh=(lambda a_, b_: (lambda f: (a_ * f + 2.0 * pad, b_ * f + 2.0 * pad)))(w0, h0)))
    got = place_labels_all(pl, tk, bd, sg)
    left = []
    for i, it in enumerate(items):
        if i not in got:
            left.append(it)
            LOG.append(u"Heritage loop: no free spot for the name \"{}\"{}.".format(
                u" / ".join(it["lines"]), u", left out" if it.get("rank", 0) else u" (WARNING: a stop's name)"))
            continue
        b, ldr, f = got[i]
        h = it["h"] * f
        bx = (b[0] * k, b[1] * k, b[2] * k, b[3] * k)
        for j, l_ in enumerate(it["lines"]):
            B.text(l_, bx[0] + pad * k, bx[3] - pad * k - h - j * HER_LEAD * h, h, it["col"], L, order=order,
                   font=FONT_TITLE, bold=bool(it.get("bold")) and j == 0, italic=bool(it.get("italic")))
        if ldr:                                           # the leader from the symbol's rim to the nearer side
            e = lp_leader_end(bx, (it["x"], it["y"]))
            dx, dy = e[0] - it["x"], e[1] - it["y"]
            dl = math.hypot(dx, dy) or 1.0
            r0 = min(it.get("r0", 0.0), 0.8 * dl)
            B.line([(it["x"] + dx * r0 / dl, it["y"] + dy * r0 / dl), e], it["col"], L, order - 1, bk_lw(0.13, k))
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
HER21_DEN = 10000              # the map's scale on the booklet page
HER21_MARGIN_M = 90.0          # m of map round the outermost places (west, south, east)
HER21_TOP_M = 130.0            # m above the main rectangle's northernmost place (room for its name)
HER21_TAB_PAD_M = (160.0, 80.0)    # m: the tab reaches this far west of Akropol / the top station, and north of Akropol
HER21_GAP_MM = 6.0             # mm between the photo columns, the map and the diagram
HER21_PHOTO_MM = 24.0          # mm: the largest photo circle
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
# Turkish name, title = the card's. txt: **Why** / **Use** / **Now** / **Project** (a field without a source is left
# out). Sources (library cards h01 = selinos_bergama_history_context_v1, h02 = selinos_site_history_inaccessible_
# edges_v1, h03 = bergama_history_hubs_research_v1) are noted per place; nothing here is printed as a source.
HER21_PLACES = [
    # h01 §5 P01; h02 §2.9 (inscribed 22.06.2014); h03 Q2 (ICOMOS 2014 s13 p287: tour groups, up by the gondola)
    dict(key="akropol", name=u"Akropol", own=(), alias=(u"akropol", u"acropolis", u"trajaneum"),
         txt=u"**Why** the terraced Hellenistic city on the hill, part of the World Heritage site inscribed in 2014. "
             u"**Use** visitors come mainly in tour groups and most ride up by the Teleferik. **Project** the loop's "
             u"goal on the hill, reached from stop 1."),
    # h01 §5 P33 (2010, 700 m line, s115); h03 Q2 (ICOMOS s13 p287)
    dict(key="teleferik", stop="gondola", name=u"Teleferik", own=(), alias=(u"teleferik", u"gondola", u"cablecar"),
         txt=u"**Why** the cable car of 2010, a 700 m line from the valley up to Akropol. **Use** the way up for "
             u"most visitors, who arrive mainly in tour groups. **Project** stop 1: the loop starts where the "
             u"visitors already arrive."),
    # h01 §5 P02-P04; h02 §2.3 (tunnels, s13), §3 Worship (N rotunda = mosque), §4.3 (closed since 03/2025, aim
    # 2026, s41); h03 Q5 (Kermes 2024 concerts in Kızıl Avlu)
    dict(key="kizilavlu", stop="redhall", name=u"Kızıl Avlu", own=(),
         alias=(u"kizilavlu", u"redhall", u"redbasilica", u"serapis", u"serapeion"),
         txt=u"**Why** Hadrian's temple, built over the stream: the Selinos runs under it in twin Roman tunnels. "
             u"**Use** its north rotunda serves as a mosque; Kermes concerts were held here in 2024. **Now** closed "
             u"for restoration since March 2025, reopening planned for 2026. **Project** stop 2: where the stream "
             u"disappears under the city."),
    # h01 §5 P08; h02 §2.5 (KE s29: Roman 2nd-3rd c., tanneries), E03 (DSİ walls 2020-), §4.6 (tourist signs at K3,
    # s63); h03 Q1 (lines 831-833 at Tabak Köprüsü, s124)
    dict(key="k3", stop="K3", name=u"Tabak Köprüsü (K3)", own=(u"tabak_koprusu_1.jpg", u"tabakhane_1.jpg"),
         alias=(u"tabakkoprusu", u"tabakhanekoprusu", u"tabakhane"),
         txt=u"**Why** Roman bridge of the 2nd-3rd c., named after the tanneries of the Tabakhane quarter. **Use** "
             u"a crossing with tourist signs; village bus lines 831-833 stop here. **Now** the stream runs in the "
             u"walled canal DSİ has rebuilt since 2020. **Project** stop 3: the stream walk starts here."),
    # h01 §5 P06; h02 §2.5 (s31 two spans, Ottoman small arch; KGM plaque 2024-2025, s63); h03 Q1 (Camikebir Cd.)
    dict(key="k4", stop="K4", name=u"Ulucami Önü Köprüsü (K4)", own=(u"ulucami_onu_koprusu_1.jpg",
                                                                    u"ulucami_onu_koprusu_2.jpg"),
         alias=(u"ulucamionukoprusu", u"ulucamionu"),
         txt=u"**Why** probably Roman, on two arches, the small one rebuilt by the Ottomans; it leads to Ulu Cami. "
             u"**Use** village bus lines 831-833 stop on Camikebir Caddesi. **Now** restored by Karayolları "
             u"(KGM) in 2024-25. **Project** stop 4: the stream walk ends here and the loop crosses."),
    # h01 §5 P05 (1398-99, Bayezid I, restored 1905, minaret 1949), P11 (Bergama Müzesi digs 2021-23, s4); h02 §3
    # Worship (Ulu Cami at K4)
    dict(key="ulucami", dot=u"Ulu Cami", name=u"Ulu Cami", own=(u"ulu_cami_1.jpg",), alias=(u"ulucami",),
         notalias=(u"onu", u"koprusu"),
         txt=u"**Why** built in 1398-99 for Bayezid I. **Use** a mosque at the K4 bridge. **Now** restored in 1905, "
             u"minaret of 1949; Bergama Müzesi dug its riverside in 2021-23. **Project** the stream walk ends at "
             u"its precinct gate."),
    # h01 §5 P07; h02 §2.5 (s32: opposite Ulu Cami, named after the tanneries; sign s63: camekan dome survives),
    # §3 Bathing (ruin since the 1842/47 flood, enclosed by 5 houses), §2.9 (s57: municipal survey drawings)
    dict(key="hamam", dot=u"Tabaklar Hamamı", name=u"Tabaklar Hamamı", own=(u"tabaklar_hamami_1.jpg",
                                                                         u"tabaklar_hamami_2.jpg"),
         alias=(u"tabaklarhamami",),
         txt=u"**Why** the Ottoman bath named after the tanneries, facing Ulu Cami across the stream. **Use** out of "
             u"use since a flood in the 1840s. **Now** a ruin enclosed by five houses; its dressing-hall dome "
             u"stands; the municipality has had it surveyed. **Project** seen across the water from stop 4."),
    # h01 §5 P23 (1513; Parchment Museum 2026, s99 s45); h02 §3 (Parchment Museum opened 28.02.2026); h03 Q4
    # (Çınarlı Kahve plane ~380-400 yr, pipe-irrigated, AA 2026), Q5 (Kermes 2024 events at the Arasta, Çınarlı Kahve)
    dict(key="arasta", stop="bazaar", name=u"Arasta", title=u"Arasta (Hacı Hekim)", own=(),
         alias=(u"arasta", u"hacihekim", u"cinarlikahve"),
         txt=u"**Why** Hacı Hekim mosque, arasta and hamam of 1513, in the old bazaar. **Use** Kermes events at the "
             u"Arasta and Çınarlı Kahve (2024). **Now** the hamam is the Parchment Museum (2026); the 380-400-year "
             u"old plane of Çınarlı Kahve is watered by pipe. **Project** stop 5: from the stream into the bazaar."),
    # h01 §5 P09; h02 §2.5 (s30: three arches, repairs altered its character), §2.9 (first stage 1,380 m Kazancı ->
    # Üçkemer, s33 s36), E01 (the tunnels end before K5); h03 Q1 (lines 656, 831-833 at Üç Kemer Köprüsü)
    dict(key="k5", xy=HER21_K5, name=u"Üç Kemer Köprüsü (K5)", own=(), alias=(u"uckemer", u"threearch"),
         txt=u"**Why** Roman bridge of the 2nd-3rd c. on three arches; repairs have changed its character. **Use** "
             u"bus lines 656 and 831-833 stop here. **Now** the end of DSİ's first canal stage, from Kazancı "
             u"Köprüsü. **Project** the masterplan's K5 window, where the stream comes out after Kızıl Avlu."),
    # h01 §5 P24 (1936, archaeology + carpets, s85 s86), §3 Archaeology (museum + DAI digs on the banks 2011-2025)
    dict(key="muze", stop="museum", name=u"Bergama Müzesi", own=(),
         alias=(u"bergamamuzesi", u"bergamamuseum", u"archaeologymuseum", u"muze"),
         txt=u"**Why** the museum of 1936: finds of Pergamon's excavations and the town's carpets. **Use** with the "
             u"German Archaeological Institute it has dug on the stream banks (2011-2025). **Project** stop 6, "
             u"between the bazaar and Asklepion."),
    # h01 §5 P28 (4th c. BC, Hadrianic, sacred spring, s114 s81); h03 Q2 (KTB: car parking; OSM ticket building,
    # paid car park)
    dict(key="asklepion", stop="asklepieion", name=u"Asklepion", own=(), alias=(u"asklep", u"asclep"),
         txt=u"**Why** the healing sanctuary of Asclepius, 4th c. BC, rebuilt under Hadrian, with a sacred spring. "
             u"**Use** an open site with a ticket building and a paid car park. **Project** stop 7, the loop's end."),
]
HER21_FOLD = {u"ı": u"i", u"ş": u"s", u"ğ": u"g", u"ü": u"u", u"ö": u"o", u"ç": u"c", u"â": u"a", u"î": u"i",
              u"û": u"u"}
_HER21_PH = {}                 # once per run: the photo of each place, the photos' pixel sizes


class Her21Clip(object):
    """v51: a Board seen through several rectangles of the page (the map's main rectangle and its tab): fills, hatches
    and lines cut to each, words kept where any holds them"""

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


def her21_cross(s, t):
    """v51: do segments s and t cross (inside both)?"""
    def o(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    (a, b), (c, d) = s, t
    return o(a, b, c) * o(a, b, d) < 0 and o(c, d, a) * o(c, d, b) < 0


def her21_order(anchors, pins):
    """v51: which pin each slot of a photo column takes (a permutation): the leaders anchor -> pin cross least,
    then are shortest (at most 7 slots: 5,040 orders)"""
    import itertools as _it
    if len(pins) > 7:                                     # too many orders: top to bottom by the pins' heights
        return sorted(range(len(pins)), key=lambda j: -pins[j][1])
    best = None
    for perm in _it.permutations(range(len(pins))):
        sg = [(anchors[i], pins[j]) for i, j in enumerate(perm)]
        n = sum(1 for a in range(len(sg)) for b in range(a + 1, len(sg)) if her21_cross(sg[a], sg[b]))
        ln = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in sg)
        if best is None or (n, ln) < best[0]:
            best = ((n, ln), perm)
    return best[1] if best else ()


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
    """v51 (R08 idea): the round photo (or an empty round slot with the place's name), its loop number on the rim,
    the place's name and its short text (keywords bold) beside it. No credit for own photos (D13)."""
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
    if num:
        rb = 2.3 * k
        bx = cx + (-0.707 if g["side"] == "L" else 0.707) * r
        by = cy + 0.707 * r
        B.fill([circle_pts(bx, by, rb, 24)], HER_ACC, L, 60)
        B.line(circle_pts(bx, by, rb, 24) + [circle_pts(bx, by, rb, 24)[0]], WHITE, L, 61, bk_lw(0.3, k))
        B.text(str(num), bx, by, bk_hk(HER21_PT["num"], k), WHITE, L, order=62, font=FONT_TITLE, bold=True,
               align="MC")
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


def her21_map(S, B, V, Fm, r_all, rs, cut, k, L, xy, num, leaders):
    """v51 (package G): the loop map through the rectangles rs (the main one and the tab): the simple basemap, the
    study area (G8), the legs stop to stop (soft), the Teleferik's line, the stream walk K3-K4 as a path along the
    water (solid band, white dashes) named on the map, the pins (loop stops numbered, other places as rings), the
    Turkish names placed clear of the pins, the lines and the leaders (G4, G6). cut: the corner the tab leaves free
    (no name goes there). Returns the stream walk's length (m)."""
    CB = Her21Clip(B, rs)
    for r_ in rs:
        B.fill([rect(*r_)], WHITE, L, 1)
    items = basemap_items("simple", box=Fm.bb)            # memoised (common/basemap.py)
    if not items:
        LOG.append(u"WARNING: heritage loop: no basemap data (cached/basemap/basemap.json missing): the map shows the "
                   u"loop on white.")
    her21_base(CB, items, V, k, L)
    draw_r28_study(S, CB, V, k, L)                        # G8: the study area's outline
    acc = HER_ACC
    ins = lambda p: any(r_[0] <= p[0] <= r_[2] and r_[1] <= p[1] <= r_[3] for r_ in rs)
    segs, taken, labs = [], [cut], []

    def keep(P):
        for r_ in rs:
            for run in clip_rect_line(list(P), r_):
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
    for a_, b_ in leaders:                                # no name on a leader
        keep([a_, b_])
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
            if not ins(p) or (cut[0] <= p[0] <= cut[2] and cut[1] <= p[1] <= cut[3]):
                continue
            d = min([math.hypot(p[0] - m[0], p[1] - m[1]) for m in marks] + [30.0 * k])
            if best is None or d > best[0] + 1e-9:
                best = (d, p)
        if best:
            labs.append(dict(lines=[u"Bergama Çayı"], x=best[1][0], y=best[1][1], h=hl, col=MPL["water_edge"],
                             italic=True, rank=1))
    her_labels(B, labs, taken, r_all, k, L, segs)
    o = [(r_all[0], r_all[1]), (r_all[2], r_all[1]), (r_all[2], r_all[3])]   # the map's outline (main + tab)
    if rs[1:]:
        o += [(rs[1][0], r_all[3]), (rs[1][0], rs[0][3]), (r_all[0], rs[0][3])]
    else:
        o += [(r_all[0], r_all[3])]
    B.line(o + [o[0]], INK, L, 70, bk_lw(0.25, k))
    return walk_m


def her21_diagram(B, x0, ytop, w, h, k, L, walk_m, num):
    """v51 (package G "how the places connect"): a plan diagram, not to scale, of how the places feed each other
    across the Selinos: the stream as a band (the seam), the Kale side (north bank) above, the bazaar side (south
    bank) below, the bridges K4, K3, K5 as bars across it, Kızıl Avlu as a block over it (the twin tunnels
    beneath), the stream walk K4-K3 on it; links named by what passes along them (h01-h03: cable car 2010; the
    bridge to the mosque; tanneries -> the tanners' bath; leather -> the Parchment Museum 2026; Kermes 2024 events;
    museum digs on the banks 2011-2025; Roman coins with Asklepios between the river gods Selinos and Ketios).
    Laid out on a 200 x 72 mm grid stretched to w x h."""
    fx, fy = w / (200.0 * k), h / (72.0 * k)
    P = lambda a, b: (x0 + a * fx * k, ytop + b * fy * k)
    hd, ht = bk_hk(HER21_PT["dia"], k), bk_hk(HER21_PT["title"], k)
    acc, rn = HER_ACC, 1.7 * k

    def tx(s, a, b, align="L", col=INK, bold=False, italic=False, hh=None):
        p = P(a, b)
        B.text(s, p[0], p[1], hh or hd, col, L, order=66, font=FONT_TITLE, bold=bold, align=align, italic=italic)

    def node(a, b, n_=None):
        p = P(a, b)
        c_ = circle_pts(p[0], p[1], rn, 24)
        if n_:
            B.fill([c_], acc, L, 64)
            B.text(str(n_), p[0], p[1], bk_hk(HER21_PT["num"], k), WHITE, L, order=65, font=FONT_TITLE, bold=True,
                   align="MC")
        else:
            B.fill([c_], WHITE, L, 64)
            B.line(c_ + [c_[0]], acc, L, 65, bk_lw(0.45, k))

    def link(pts, head=False, dash=False, col=INK, r_end=0.0):
        Q = [P(*q) for q in pts]
        if r_end:                                         # stop at the node's rim
            a, b = Q[-2], Q[-1]
            dl = math.hypot(b[0] - a[0], b[1] - a[1]) or 1.0
            Q[-1] = (b[0] - (b[0] - a[0]) * r_end / dl, b[1] - (b[1] - a[1]) * r_end / dl)
        if dash:
            for d_ in dashes(Q, 1.0 * k, 0.7 * k):
                B.line(d_, col, L, 62, bk_lw(0.25, k))
        else:
            B.line(Q, col, L, 62, bk_lw(0.25, k))
        if head:
            her21_head(B, Q[-2], Q[-1], k, col, L)
    tx(u"The Selinos is the seam: bridges, crafts and events tie the Kale side to the bazaar side", 0, -4,
       bold=True, hh=ht)
    tx(u"KALE SIDE · north bank", 0, -10, col=INK2, bold=True)
    a, b = P(0, -39), P(200, -33)                         # the stream, downstream to the right
    B.fill([rect(a[0], a[1], b[0], b[1])], HER21_WATER, L, 60)
    tx(u"Selinos (Bergama Çayı)", 3, -37.0, col=WHITE, bold=True)
    her21_head(B, P(190, -36), P(197, -36), k, WHITE, L, order=61, mm=2.2)
    a, b = P(64, -36), P(100, -36)                        # the stream walk on it
    B.line([a, b], acc, L, 61, bk_lw(1.5, k))
    for d_ in dashes([a, b], 1.2 * k, 0.9 * k):
        B.line(d_, WHITE, L, 61, bk_lw(0.3, k))
    for bx in (64.0, 100.0, 184.0):                       # the bridges
        a, b = P(bx - 0.8, -41), P(bx + 0.8, -31)
        B.fill([rect(a[0], a[1], b[0], b[1])], INK, L, 62)
    a, b = P(136, -41.5), P(160, -30.5)                   # Kızıl Avlu over the stream, the twin tunnels beneath
    B.fill([rect(a[0], a[1], b[0], b[1])], acc, L, 62)
    for ty in (-34.0, -36.5):
        for d_ in dashes([P(137, ty), P(159, ty)], 1.0 * k, 0.7 * k):
            B.line(d_, WHITE, L, 63, bk_lw(0.25, k))
    tx(u"Kızıl Avlu", 148, -40.6, "C", WHITE, True)
    node(136, -30.5, num.get("kizilavlu"))
    node(64, -36, num.get("k4"))
    node(100, -36, num.get("k3"))
    for key, a_, b_ in (("ulucami", 64, -16), ("akropol", 146, -16), ("teleferik", 194, -16), ("asklepion", 6, -56),
                        ("muze", 50, -56), ("hamam", 84, -56), ("arasta", 132, -56)):
        node(a_, b_, num.get(key))
    tx(u"Ulu Cami", 64, -12, "C", bold=True)
    tx(u"Akropol", 146, -12, "C", bold=True)
    tx(u"Teleferik", 200, -12, "R", bold=True)
    tx(u"Asklepion", 2, -61, "L", bold=True)
    tx(u"Bergama Müzesi", 50, -61, "C", bold=True)
    tx(u"Tabaklar Hamamı", 81.5, -57, "R", bold=True)
    tx(u"Arasta (Hacı Hekim)", 134.5, -57, "L", bold=True)
    tx(u"Ulucami Önü (K4)", 62, -31.2, "R", bold=True)
    tx(u"Tabak Köprüsü (K3)", 102, -43.6, "L", bold=True)
    tx(u"Tabakhane quarter", 102, -46.9, "L")
    tx(u"Üç Kemer (K5)", 184, -44, "C", bold=True)
    tx(u"stream walk, {:,.0f} m".format(walk_m), 82, -29.6, "C", acc, True)
    link([(192.3, -16), (146, -16)], head=True, r_end=rn)          # Teleferik -> Akropol
    tx(u"cable car, 2010", 170, -20.5, "C", INK2, italic=True)
    link([(64, -31), (64, -16)], r_end=rn)                         # K4 -> Ulu Cami
    tx(u"the bridge leads to the mosque", 66, -25, "L", INK2, italic=True)
    link([(6, -54.3), (6, -39)], head=True)                         # Asklepion -> the stream (coins)
    for j, s_ in enumerate((u"Roman coins show Asklepios", u"between the river gods", u"Selinos and Ketios")):
        tx(s_, 8.5, -43.5 - 3.3 * j, "L", INK2, italic=True)
    link([(50, -39), (50, -56)], head=True, r_end=rn)              # the banks' digs -> the museum
    tx(u"digs on the banks, 2011-2025", 52, -44, "L", INK2, italic=True)
    link([(100, -39), (84, -56)], r_end=rn)                        # tanneries -> the tanners' bath
    tx(u"the tanners' bath", 87, -51.5, "R", INK2, italic=True)
    link([(100, -39), (100, -56), (132, -56)], head=True, r_end=rn)   # leather -> parchment
    tx(u"leather craft lives on: Parchment Museum, 2026", 115, -61, "C", INK2, italic=True)
    link([(142, -41.5), (132, -56)], dash=True, r_end=rn)         # Kermes at both
    tx(u"Kermes events, 2024", 142.5, -49, "L", INK2, italic=True)
    tx(u"BAZAAR SIDE · south bank", 200, -64.5, "R", INK2, True)
    tx(u"Not to scale. Bridges have joined the two banks since antiquity; the project's stream walk joins K4 and K3.",
       0, -70, "L", INK2)


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
    """v51 (WO-T3a-6, package G): photo column | map | photo column, the diagram in the corner the map's tab leaves
    free above the left column. The map at 1:10,000, north up, its scale bar and north arrow under it, the Commons
    photos' credit lines under them (own photos: none, D13). One crop drw_heritage_loop (the key map is gone).
    Returns the y below."""
    ss = 1000.0 * k / HER21_DEN
    gap = HER21_GAP_MM * k
    xy = dict((pl["key"], her21_xy(pl)) for pl in HER21_PLACES)
    num = {}
    for pl in HER21_PLACES:
        if pl.get("stop"):
            num[pl["key"]] = [j + 1 for j, s_ in enumerate(HER_STOPS) if s_["key"] == pl["stop"]][0]
    main = [q for kk, q in xy.items() if kk != "akropol"]
    M = HER21_MARGIN_M
    x0, x1 = min(q[0] for q in xy.values()) - M, max(q[0] for q in xy.values()) + M
    y0, ym = min(q[1] for q in main) - M, max(q[1] for q in main) + HER21_TOP_M
    ak, gt = xy["akropol"], HER21_GONDOLA_TOP
    tx0, y1 = min(ak[0], gt[0]) - HER21_TAB_PAD_M[0], max(ak[1], gt[1]) + HER21_TAB_PAD_M[1]
    if y1 <= ym:                                          # everything in the main rectangle: no tab
        y1, tx0 = ym, x0
    Fm = HerBox(x0, y0, x1, y1)
    mw, mh = Fm.w * ss, Fm.h * ss
    cw = 0.5 * ((BK_AW - 1.0) * k - mw - 2.0 * gap)       # each photo column
    if cw < 80.0 * k:
        LOG.append(u"WARNING: heritage loop: the photo columns are only {:.0f} mm wide (map {:.0f} mm).".format(
            cw / k, mw / k))
    xm = x + cw + gap
    V = View(Fm, ss, xm, top)
    r_all = (xm, top - mh, xm + mw, top)
    mt = V.p(x0, ym)[1]                                   # the main rectangle's top
    r_main = (xm, top - mh, xm + mw, mt)
    xt = V.p(tx0, ym)[0]
    rs = [r_main] + ([(xt, mt, xm + mw, top)] if y1 > ym else [])
    cut = (xm, mt, xt, top) if y1 > ym else (xm, top, xm, top)
    low_map = b_foot(B, Fm, xm, r_all[1], ss, k, L, HER_SB_M.get(HER21_DEN, 400.0))
    bot = low_map
    # the photo columns: the left one under the diagram (beside the main rectangle), the right one the full height
    xr = xm + mw + gap
    Hl, Hr = mt - bot, top - bot
    n = len(HER21_PLACES)
    nl = max(range(2, n - 1), key=lambda i: min(Hl / i, Hr / float(n - i)))
    ph = her21_photos()
    byx = sorted(HER21_PLACES, key=lambda pl: xy[pl["key"]][0])
    cols = [("L", byx[:nl], x, x + cw, mt, Hl / nl), ("R", byx[nl:], xr, xr + cw, top, Hr / (n - nl))]
    cards, leaders = [], []
    for side, pls, c0, c1, ct, pitch in cols:
        cys = [ct - (i + 0.5) * pitch for i in range(len(pls))]
        anchors = [(c1 if side == "L" else c0, cy) for cy in cys]
        pins = [V.p(*xy[pl["key"]]) for pl in pls]
        perm = her21_order(anchors, pins)
        for i, j in enumerate(perm):
            pl = pls[j]
            g = her21_geom(pl, ph.get(pl["key"]), c0, c1, cys[i], pitch, side, k)
            p = pins[j]
            dx, dy = p[0] - g["cx"], p[1] - g["cy"]
            dl = math.hypot(dx, dy) or 1.0
            r0 = (1.7 if pl["key"] in num else 1.3) * k
            a_ = (g["cx"] + dx * (g["r"] + 0.4 * k) / dl, g["cy"] + dy * (g["r"] + 0.4 * k) / dl)
            b_ = (p[0] - dx * r0 / dl, p[1] - dy * r0 / dl)
            cards.append((pl, g))
            leaders.append((a_, b_))
    walk_m = her21_map(S, B, V, Fm, r_all, rs, cut, k, L, xy, num, leaders)
    for (pl, g), (a_, b_) in zip(cards, leaders):
        her21_card(B, pl, ph.get(pl["key"]), g, num.get(pl["key"]), k, L)
        B.line([a_, b_], INK, L, 63, bk_lw(0.2, k))     # the leader, photo -> pin
        B.fill([circle_pts(a_[0], a_[1], 0.45 * k, 12)], INK, L, 63)
    if y1 > ym:                                           # the diagram in the corner the tab leaves free
        her21_diagram(B, x, top, xt - gap - x, top - mt - gap, k, L, walk_m, num)
    low = bot
    cred = her21_credits()
    if cred:                                              # Commons photos only (D13: no credit for own photos)
        h = bk_hk(HER21_PT["txt"], k)
        y = low - 1.0 * k
        for ln in her_wrap(u"Photos: " + u"; ".join(u"{}: {}".format(a_, c_) for a_, c_ in cred) + u".", h, mw):
            her_line(B, ln, xm, y - h, h, INK2, L)
            y -= HER_PITCH * h
        low = y
    right = xr + cw
    crop_panel("heritage_loop", x - 0.5 * k, low - 0.5 * k, right + 0.5 * k, top + 0.5 * k,
               u"The heritage loop: eleven places on both banks of the Selinos, joined by the stream walk K3-K4",
               crop_scale(ss), crop_legend(her_leg()))
    CROP_PANELS[-1]["bk_w"] = (right - x) / k + 1.0       # its width on the booklet page, mm (the map prints 1:10,000)
    LOG.append(u"Heritage loop (WO-T3a-6): map 1:10,000, {:,.0f} x {:,.0f} m ({:.0f} x {:.0f} mm, tab from x {:,.0f}), "
               u"simple basemap; {} + {} photo cards ({:.0f} / {:.0f} mm slots); stream walk K3-K4 {:,.0f} m along "
               u"the stream; {} Commons credit line(s).".format(Fm.w, Fm.h, mw / k, mh / k, tx0, nl, n - nl,
                                                                Hl / nl / k, Hr / (n - nl) / k, walk_m, len(cred)))
    return low


def draw_heritage_loop(S, B, x, y, w, U):
    """v51 (revision 29 Oct 2026, WO-T3a-6, package G; replaces v50's loop map + key map): THE HERITAGE LOOP:
    her_loop_page (crop drw_heritage_loop: the map at 1:10,000 on the simple basemap, the photo cards beside it,
    the diagram of how the places feed each other). Sized for the booklet page: k = board units per booklet mm of
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
