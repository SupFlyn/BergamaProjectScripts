# r: pymupdf==1.26.5
# bergama_agriculture_alternatives_v4.py · Thread 3 of the 22 Oct batch: three alternatives for the agriculture analysis
# Runs as delivered in: Grasshopper Python 3 component (press a Button wired to any input), Rhino 8 ScriptEditor
# (Python 3), or plain Python 3. Makes the folder Downloads/Bergama/output/Bergama_agriculture_alternatives by itself and saves ONE
# all-vector A3 PDF there, one page per alternative:
#   1 WHAT EACH CUBIC METRE GROWS   chart: hectares the stored water irrigates, per crop, normal and 1-in-5 dry year
#   2 THE FARMS WE FEED             the site board's plan 01 "What is there" at a round scale with the fields and orchards fed
#   3 ONE PLANT LADDER              the one-way chain and its programme; the ladder by season: water, what people do, plants
#   4 SOURCES                       the numbered key of the [n] marks on pages 1-3
# Storage, water to the farms and the farm areas are read on every run from the water balance script's output
# (bergama_water_balance), so they follow its cost cut-off; the fallback is the shared key-figures file (flagged).
# Notes for Aras: batch_2026-10-22/thread3_agriculture/NOTES.md.
import os, time, json, zlib, math

VERSION = "v4"
# v4 (MIRAQUA 28 Oct, booklet revision v4, pages 18-19; a feature change, so the next whole number):
#   * P18.1 / P19.3 / P19.4 / G11 / G12: every photo through common/plant_photos.py; corn printed as "Corn (Mısır)"
#     (data key "maize" and the Wikimedia file kept); an empty frame says "no photo: <reason>".
#   * P19.1 / G5 / F10: the kicker top left; page 3's top-right corner on the booklet grid (column 8, 4 rows 5.2 mm
#     apart, 7.5 pt): steps 1-5, NEXT -> D The heritage loop (title bold), the chain key; no big page numbers.
#   * P19.2: the ladder's people from common/figures.py at true scale (1.75 m), one colour, no stroke.
#   * G4 / F13: ladder labels placed by common/label_place.py clear of figures, lines, plants and each other;
#     "hub square: dry, step-free" and "wade the strip" now print.
#   * G13: flood heights in m with 2 decimals (values unchanged). Bank depth research 28 Oct §4.5: over the bank top
#     only at S4 (left); K4 before the DSİ walls.
#   * F5: [n] marks only for public online sources; internal pointers out of the printed source list.
#   * G1: page 2's group line removed; page 1's left column on the 14 mm margin.
# v3.1 (bugfix, Aras 27 Oct, booklet Prompt 8 "final check of every page"): plant and crop names "English (Turkish)"
#   from the shared table where pages 1 and 3 still had the English alone: page 3's season row OLIVE (ZEYTİN) HARVEST,
#   its labels (hub square: oriental plane (Doğu çınarı) shade; common reed (Kamış) gold; olive (Zeytin) harvest;
#   olive (Zeytin) trees on the fields) and page 1's "what it replaces" figure. Page 3: "stored winter water" and
#   "site edge: farmland outside" sit at the row's top edge, so they found no free place above it and were left out on
#   every run: they now go under their anchors. The h01 timeline quotes stay word for word. Page 1's "THE STREAM COMES
#   FIRST" block and the step chips: its 6.5 pt words are 7 pt, the smallest size on a booklet page.
# v3 (Aras 27 Oct 17:35, Prompt 6 "water, part 3"; the booklet's p.24-25):
#   * page 1, "THE STREAM COMES FIRST" between the headline and the bars (task 1: "show the defence ON the board"): the
#     priority 1 stream: summer strip -> 2 on-site planting -> 3 farms (the model has no draw of its own for the
#     planting: it lives on the strip's water, so it shares the strip's bar); the design store through a normal and the
#     1-in-5 dry water year as two stacked bars on one scale (strip, farms, left over; the store size dashed across
#     both), read live from the water balance v4 results (design.year_split, one daily run); and the double squeeze in
#     one line, computed: water left for the farms after the strip, the need per hectare and the hectares that water
#     serves, dry year against normal, then why deficit-irrigated olive is the lever. Without year_split (water balance
#     v3 or older) only the priority row is drawn (logged). The bars move down to make room: rows 16.5 mm apart (were
#     19.5), the reading box ends at the 14 mm margin.
#   * pages 1 and 3 say where they sit in the booklet: "C WATER · WHAT WE DO WITH IT" (was "AGRICULTURE ANALYSIS");
#     page 3, the last page of the water theme, closes it top right: what we do with the water in five steps and NEXT
#     D HISTORY AND HERITAGE (rule 7, task 3).
#   * m² and m³ are written as a raised small 2 or 3 (0.6 x the size, as wide as the glyph), which every PDF viewer
#     shows (task 2: "325,000-375,000 m" in some viewers).
# v2 (Aras 27 Oct, Prompt 5, rule 8: "Plant names: English first, Turkish in brackets, no Latin ... Every plant AND every
# crop in the booklet gets a photo of the plant itself ... openly licensed photos ... credited in the sources ... Same
# crop ratio and size for every photo"): every plant and crop name on pages 1 and 3 is "English (Turkish)" from the
# shared table (src/common/plant_photos.py), no Latin names on the pages. Page 3's step columns show each step's plants
# as photos (PHOTO_W x PHOTO_H mm, two side by side) with the name and the photo's [n] credit under each; the giant reed
# under REMOVE. Page 1 adds "THE CROPS" under the timeline: olive, cotton, corn, tomato as photos. The photos come
# from the shared cache Downloads/Bergama/cached/plant_photos/ (the water board shows the same photo of the same
# plant) and go into their frames with PyMuPDF after the PDF is written; a missing one is an empty frame saying "no
# photo", never an error; the log says how many were placed. Room on page 3: the chain sits 4 mm higher, the season rows
# are 50 mm (were 52; 4.5 mm stay above the tallest tree); the plants' reasons are left out under the photos when the
# column would not fit (logged). The Data file changes (STEPS: plant keys instead of botanical names): copy the new one.
# v1.7 (bugfix, Aras 27 Oct 16:05): page 3 crashed ("too many values to unpack": the sketch engine's items now
# carry a 4th value, the label group); the text under the component shows a newly pasted version at once, idle.
# v1.6 (Aras 27 Oct 11:07, booklet p24-26; revision_2026-10-27/PHASE2_SPEC.md): white pages (the beige paper goes); no
# source footers or credit lines on the pages: the [n] marks are numbered once for the sheet and their key is a 4th
# page "Sources" (the booklet's sources page reads it there). Page 1 adds "why the stored water goes to farms": a
# cotton / olive timeline in card h01's words and years, labels placed by measured width. Page 3 rebuilt for option A:
# the one-way chain upstream entry -> K4 -> K3 -> İstiklal -> K5 -> K6 -> downstream -> farmland outside the site,
# hubs and in-bed sub-hubs, programme and historic roots; the ladder drawn three times (high water, low water, olive
# harvest) with what people do on each step; the species under each step. Every label is placed by a collision check
# (Placer): a label with no free place is left out and named in the log.
# v1.5 (Aras 26 Oct 07:06, review of the deck, p.33-34): page 2's map is the site board's own plan 01 ("What is there",
# board v42+, cut from its sheet PDF with PyMuPDF and scaled by one factor, never redrawn) at the largest round scale
# that fits, with only the farms layer drawn on it (fields and orchards fed, their extent), the plan's own key, the
# figures beside it and a context line; v1.4's land cover drawing stays only as a flagged fallback. Page 3's ladder is
# drawn by the proposal sections' sketch engine (the p.23 upstream entry's language): hand ground, washes, winter
# water and summer strip, the faint design-flood reach, level marks, sketch plants and people, rain and sun marks.
# The "# r: pymupdf" line installs PyMuPDF in Rhino 8 on the first run (as the booklet).
# v1.4 (Aras 25 Oct 21:47-22:02, booklet stage 3): the booklet shows crops of this sheet (booklet/CROP_SPEC.md):
# blocks.json lists one crop per panel of the three pages and results.json keeps v1.3's keys; the v1.3 booklet redraws
# are gone. Caveat notes taken off the sheet (labels kept); "stream", never "river". Page 3's ladder drawn in the site
# board's section language (src/common/section_style.py): cut ground with sloped banks, the strip hatched, whole plants,
# one size across and up.
# v1.3 (25 Oct, booklet stage 2, SCRIPT_STANDARD §8): also writes output/<folder>/booklet/: c7_hero.pdf (plant ladder +
# the water board's planting bands A-F), c8_b.pdf (hectares per crop bars), blocks.json (every word a label) and
# results.json (hectares per crop). The A3 sheet is unchanged.
# v1.2 (Aras 25 Oct 17:00, SCRIPT_STANDARD §5b visual first): sentences become pictogram tiles, callouts and tags; method
# and source sentences become [n] marks with one numbered source key in each page's footer; layout and colours kept.
# Flood figures corrected to the surveyed sections (research/rain_river_levels/README.md, v1.1 correction and line 49).
# v1.1 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_agriculture_alternatives_log.txt (next to cached/ and output/), overwritten by each press.
# ---- Bergama folders (Aras 24 Oct 08:28 + 27 Oct 11:07; SCRIPT_STANDARD §9). Every script uses ONLY these. ----
#   Downloads/Bergama/output/<name>/          final PDFs only
#   Downloads/Bergama/logs/                    every log file and log folder
#   Downloads/Bergama/cached/<name>/           caches, results other scripts read, any other working file
#   Downloads/Bergama/cached/booklet/<name>/   the script's booklet assets (blocks.json, results, images);
#                                              the booklet's own leftovers in cached/booklet/
BERGAMA_ROOT = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama")


def bg_output(name):
    return os.path.join(BERGAMA_ROOT, "output", name)


def bg_cache(name):
    return os.path.join(BERGAMA_ROOT, "cached", name)


def bg_booklet(name):
    return os.path.join(BERGAMA_ROOT, "cached", "booklet", name)


def bg_logs(*sub):
    return os.path.join(BERGAMA_ROOT, "logs", *sub)


def bg_first(paths):
    """The first path that exists (new place first, then where older versions wrote it), else the first."""
    for p in paths:
        if os.path.exists(p):
            return p
    return paths[0]


def bg_tidy_output(name, cache_dir=None):
    """output/<name>/ keeps PDFs only: log files and anything in a log folder move to logs/<name>/, every other
    non-PDF file to cached/<name>/from_output/ (or cache_dir: the booklet uses cached/booklet/; moved, never deleted;
    same sub-folders). Empty folders go.
    Returns short log lines (counts, not one line per file)."""
    import shutil as _sh
    root, moved, fail = bg_output(name), {}, []
    if not os.path.isdir(root):
        return []
    for d, subs, files in os.walk(root, topdown=False):
        rel = os.path.relpath(d, root)
        rel = "" if rel == "." else rel
        for fn in files:
            if fn.lower().endswith(".pdf"):
                continue
            is_log = "log" in fn.lower() or any("log" in p.lower() for p in rel.split(os.sep) if p)
            dst = os.path.join(bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output")), rel, fn)
            try:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                if os.path.exists(dst):
                    os.remove(dst)
                _sh.move(os.path.join(d, fn), dst)
                top = bg_logs(name) if is_log else (cache_dir or os.path.join(bg_cache(name), "from_output"))
                moved[top] = moved.get(top, 0) + 1
            except Exception as ex:
                fail.append(u"%s (%s)" % (os.path.join(rel, fn), type(ex).__name__))
        if d != root:
            try:
                os.rmdir(d)                       # only when empty
            except Exception:
                pass
    return ([u"output/%s: %d non-PDF file(s) moved to %s" % (name, n, d) for d, n in sorted(moved.items())] +
            ([u"output/%s: could not move %s" % (name, ", ".join(fail[:5]))] if fail else []))
# ---- plant photos, shared by the water board and the agriculture alternatives (Aras 27 Oct, Prompt 5: "every plant
# AND every crop in the booklet gets a photo of the plant itself. Use openly licensed photos (e.g. Wikimedia Commons)
# credited in the sources, never photos from shop or nursery sites. Same crop ratio and size for every photo").
# MIRAQUA round 28 Oct (G12): every photo is PINNED to one Wikimedia Commons file page (PLANTS), the whole plant or
# crop in its setting, the same file wherever the species shows. No lead image and no search at run time (they gave
# the museum cob and the African olive). Why cards printed "not loaded": Wikimedia answered a burst of 3-4 requests a
# plant with HTTP errors (most likely 429, too many requests) and the code kept asking. Now: ONE batched API call for
# all photos still to fetch, then one 500 px download at a time with a pause, Retry-After honoured once, and after a
# second refusal nothing more this press (remembered 10 min, so a quick second press does not trip it again). The
# user agent names the project and its repository (Wikimedia's user-agent policy).
# Fetched once on Aras's PC (the cloud cannot reach Wikimedia), kept in the cache folder and read from there on every
# later press. Only CC BY, CC BY-SA, CC0 and public-domain files are used. A photo Aras puts into the cache folder
# himself (<key>.jpg with a <key>.json {"file", "credit"}) is used as it is. If the pinned files cannot be fetched,
# an older cached photo of the same plant stays (where its row allows), else the frame says why.
# Credit (Aras 28 Oct 11:38, fault table F15: "no Latin file names"): author, licence, Wikimedia Commons and the page-id
# link that opens exactly that file page; PHOTO_CREDIT_FILE = True adds the file name (brief G12) if that is chosen.
PHOTO_W, PHOTO_H = 28.0, 21.0        # mm on the A3 page, every photo in the booklet (4:3, cover-cropped, never stretched)
PHOTO_PX = 500                       # px wide fetched: a standard Wikimedia thumbnail step (about 450 dpi at PHOTO_W)
PHOTO_CREDIT_FILE = False            # True = the credit names the Commons file too (G12) besides the page-id link (F15)
PLANT_PHOTO_DIR = bg_cache("plant_photos")   # one folder for every script: the same plant shows the same photo
# Every plant and crop the booklet names: key -> (printed name "English (Turkish)", the Commons files to use in order
# (file page titles without "File:"; the first that is free and loads is used), keep_old = an older cached photo of
# this plant may stay when none of them loads). Names: English and Turkish as in research/water_data/04 §1 (species
# matrix), Aras's examples "Common reed (Kamış)", "Oriental plane (Doğu çınarı)"; Kofa = the rush genus Juncus
# (turkiyebitkileri.com, Juncaceae - Kofagiller, Juncus - Kofa). Files: revision_2026-10-28/checks/photos.md §2-3
# (whole plant in its setting; author and licence are read from each file page at the fetch and checked there).
PLANTS = {
    "reed": (u"Common reed (Kamış)", (u"Common Reed (Phragmites australis) (8131465127).jpg",
                                     u"Reed panicle at Brodalen 1.jpg"), True),
    "cattail": (u"Broadleaf cattail (Hasır otu)", (u"Bulrush (Typha latifolia) (8139113636).jpg",), True),
    "mint": (u"Water mint (Su nanesi)", (u"Mentha aquatica Meinerswijk.jpg", u"Mentha aquatica 02.jpg"), True),
    "iris": (u"Yellow flag iris (Sarı süsen)", (u"Yellow Iris, Gunnersbury Triangle.JPG",
                                                u"Iris pseudacorus (yellow flag iris) (Newark, Ohio, USA) 5 (27772297656).jpg"), True),
    "rush": (u"Sharp rush (Kofa)", (u"Juncus acutus2.jpg",), True),
    "loosestrife": (u"Purple loosestrife (Aklar otu)", (u"Lythrum salicaria, field of purple loosestrife, Concord, Massachusetts.jpg",
                                                        u"Purple Loosestrife (Lythrum salicaria) - geograph.org.uk - 950598.jpg"), True),
    "tamarisk": (u"Tamarisk (Ilgın)", (u"A Tamarisk Tree in Israel (5759425470).jpg", u"Tamarix canariensis-Daimiel.jpg"), True),
    "willow": (u"White willow (Ak söğüt)", (u"A big white willow tree (Salix alba) at the bay of lake Juojärvi in Tuusniemi, Finland, 2018 September.jpg",
                                            u"Silberweide (Salix alba).JPG"), True),
    "chaste": (u"Chaste tree (Hayıt)", (u"Vitex-agnus-castus-habitus.jpg", u"Vitex-agnus-castus-habit.JPG"), True),
    "poplar": (u"White poplar (Ak kavak)", (u"Pioppo (populus alba).jpg", u"Daniel Fuchs.CC-BY-SA.Populus alba.jpg"), True),
    "ash": (u"Narrow-leaved ash (Dişbudak)", (u"Fraxinus angustifolia - Israel.JPG", u"Fraxinus-angustifolia.jpg"), True),
    "oleander": (u"Oleander (Zakkum)", (u"Oleander (Nerium oleander) habit.jpg", u"Nerium oleander (Adelfa).jpg"), True),
    "plane": (u"Oriental plane (Doğu çınarı)", (u"Oriental Plane tree - Platanus orientalis - Doğu Çınarı, Arslanköy 04.JPG",
                                                u"TRSTENO ORIENTAL PLANE TREE, CROATIA.jpg"), True),
    "lavender": (u"French lavender (Karabaş otu)", (u"Lavandula stoechas (cantueso).jpg", u"Lavandula stoechas 1.JPG"), True),
    "rosemary": (u"Rosemary (Biberiye)", (u"Large rosemary bush.jpg", u"Rosmarinus officinalis (Italy) 01.jpg"), True),
    "olive": (u"Olive (Zeytin)", (u"Olive trees on Thassos.JPG",), True),       # was the African wild olive (Cape Town)
    "cotton": (u"Cotton (Pamuk)", (u"CottonPlant.JPG",), True),
    "maize": (u"Corn (Mısır)", (u"Maize field, Balcalı 01.jpg", u"A Maize Crop with beautiful Corn.jpg"), False),  # G11, P18.1:
    "tomato": (u"Tomato (Domates)", (u"Solanum lycopersicum in Kaunas.jpg",), True),                       # never the cob
    "giant_reed": (u"Giant reed (Kargı)", (u"Poaceae plant at golden hour near the river in Laos.jpg",
                                           u"Arundo donax 2007.JPG"), True),
}


def plant_name(key):
    """The printed name of a plant: "English (Turkish)"."""
    return PLANTS[key][0]


def plant_photo_of(key, log, state):
    """(jpeg path or None, credit or None, why not) of a plant in PLANTS, from the shared folder."""
    name, files, keep_old = PLANTS[key]
    return plant_photo(key, name, files, keep_old, PLANT_PHOTO_DIR, log, state)


PHOTO_UA = ("MIRAQUA-booklet/3 (https://github.com/SupFlyn/BergamaProjectScripts; Bergama student project, "
            "Yasar University) Python-urllib")
PHOTO_TIMEOUT = 8.0                  # s per request; after one network failure the rest are not tried this press
PHOTO_PAUSE = 1.0                    # s between two downloads
PHOTO_HOLD = 600.0                   # s: after Wikimedia refused twice, no new request for this long (any press)


def jpeg_info(data):
    """(width, height, colour components) of JPEG bytes (baseline or progressive), else None."""
    import struct
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            return None
        m = data[i + 1]
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD7:
            i += 2
            continue
        n = struct.unpack(">H", data[i + 2:i + 4])[0]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return (w, h, data[i + 9]) if data[i + 9] in (1, 3) else None
        i += 2 + n
    return None


def _photo_http(url, state):
    """the bytes at url; an HTTP 429/503 waits for its Retry-After (at most 30 s) and tries once more, a second
    refusal sets state["refused"] (nothing more is fetched this press). A pause before every request but the first."""
    import time
    import urllib.request
    import urllib.error
    for attempt in (0, 1):
        wait = PHOTO_PAUSE - (time.time() - state.get("last", 0.0))
        if wait > 0:
            time.sleep(wait)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": PHOTO_UA})
            with urllib.request.urlopen(req, timeout=PHOTO_TIMEOUT) as r:
                return r.read()
        except urllib.error.HTTPError as ex:
            if ex.code not in (429, 503):
                raise
            if attempt:
                state["refused"] = u"Wikimedia refused (HTTP %d)" % ex.code
                _photo_hold(state["refused"])
                raise
            try:
                ra = float(ex.headers.get("Retry-After") or 5.0)
            except Exception:
                ra = 5.0
            time.sleep(min(30.0, max(1.0, ra)))
        finally:
            state["last"] = time.time()


def _photo_hold(why=None):
    """the refusal memo in the cache folder: written with why, else read: (why, seconds left) or None"""
    import time
    p = os.path.join(PLANT_PHOTO_DIR, "_refused.json")
    try:
        if why:
            os.makedirs(PLANT_PHOTO_DIR, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"why": why, "t": time.time()}, f)
            return None
        with open(p, "r", encoding="utf-8") as f:
            m = json.load(f)
        left = PHOTO_HOLD - (time.time() - float(m["t"]))
        return (m["why"], left) if left > 0 else None
    except Exception:
        return None


def _png_to_jpeg(src, dst):
    """A PNG turned into a JPEG on white by .NET System.Drawing (Rhino on Windows); False where that is missing."""
    try:
        import clr
        clr.AddReference("System.Drawing")
        import System.Drawing as SD
        bmp = SD.Bitmap(src)
        out = SD.Bitmap(bmp.Width, bmp.Height)
        g = SD.Graphics.FromImage(out)
        g.Clear(SD.Color.White)
        g.DrawImage(bmp, 0, 0, bmp.Width, bmp.Height)
        g.Dispose()
        out.Save(dst, SD.Imaging.ImageFormat.Jpeg)
        bmp.Dispose()
        out.Dispose()
        return True
    except Exception:
        return False


def photo_free(lic):
    """True for an open licence: CC BY / CC BY-SA (any version), CC0, public domain."""
    t = (lic or u"").lower()
    if not t or "non-free" in t or "fair use" in t or "-nc" in t or "-nd" in t or " nc" in t or " nd" in t:
        return False
    return t.startswith("cc by") or t.startswith("cc-by") or t.startswith("cc0") or "public domain" in t or \
        t.startswith("pd")


def _photo_meta(info):
    """(author, licence) from a Commons imageinfo record's extmetadata."""
    import re
    md = info.get("extmetadata", {}) or {}
    artist = re.sub(r"<[^>]+>", u"", md.get("Artist", {}).get("value", u"")).strip()
    return re.sub(r"\s+", u" ", artist), md.get("LicenseShortName", {}).get("value", u"").strip()


def _photo_infos(titles, state):
    """ONE Commons API call for up to 50 file titles: {title: imageinfo record + pageid} for the files that exist"""
    import urllib.parse
    out = {}
    for i in range(0, len(titles), 50):
        part = titles[i:i + 50]
        q = json.loads(_photo_http("https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo"
                                   "&iiprop=url|mime|size|user|extmetadata&iiurlwidth={}&titles={}".format(
                                       PHOTO_PX, urllib.parse.quote(u"|".join(u"File:" + t for t in part))),
                                   state).decode("utf-8"))
        qq = q.get("query", {})
        norm = dict((n_.get("to"), n_.get("from")) for n_ in qq.get("normalized", []) or [])
        for pg_ in qq.get("pages", {}).values():
            ii = (pg_.get("imageinfo") or [None])[0]
            if "missing" in pg_ or not ii:
                continue
            t = pg_.get("title", u"")
            t = norm.get(t, t)
            ii["pageid"] = pg_.get("pageid")
            out[t.replace(u"File:", u"", 1)] = ii
    return out


def _photo_safe(s):
    """a name the sheets' fonts can print (WinAnsi + the Turkish letters): other letters lose their accents (Kaunas
    authors etc.), anything still unprintable leaves the name out"""
    import unicodedata
    tr = u"ĞğİıŞş"
    out = u""
    for ch in s or u"":
        try:
            ch.encode("cp1252")
            out += ch
        except Exception:
            if ch in tr:
                out += ch
            else:
                b = unicodedata.normalize("NFKD", ch)[0]
                out += b if ord(b) < 128 else u""
    out = u" ".join(out.split())
    return out if sum(c.isalpha() for c in out) >= 2 else u""


def photo_credit(name, m):
    """the printed credit of a photo record m {author, licence, pageid, title} (F15: no Latin file names)"""
    link = u"commons.wikimedia.org/?curid={}".format(m["pageid"]) if m.get("pageid") else u"Wikimedia Commons"
    cr = u"photo {}: {}, {}, Wikimedia Commons, {}".format(name, m.get("author") or u"author named on the file page",
                                                            m.get("licence") or u"licence on the file page", link)
    if PHOTO_CREDIT_FILE and m.get("title"):
        cr += u" (File:{})".format(m["title"])
    return cr


def plant_photo(key, name, files, keep_old, photo_dir, log, state):
    """(jpeg path or None, credit or None, why not) for one plant or crop: key = file name in photo_dir, name = the
    printed name, files = its pinned Commons files in order, keep_old = an older cached photo may stay. Cache first
    (when it holds one of the pinned files, or Aras's own photo), then the web (see the header of this part)."""
    meta = os.path.join(photo_dir, key + ".json")
    old = None
    try:
        with open(meta, "r", encoding="utf-8") as f:
            m = json.load(f)
        p = os.path.join(photo_dir, m["file"])
        with open(p, "rb") as f:
            if jpeg_info(f.read(256 * 1024) + b"\x00" * 10):
                if not m.get("source") and not m.get("title"):
                    return p, m["credit"], None                       # Aras's own photo, as it is
                if m.get("title") in files and m.get("pageid"):
                    return p, photo_credit(name, m), None             # one of the pinned files, fetched before
                old = (p, m.get("credit"))                            # fetched by an older version
    except Exception:
        pass

    def fallback(why):
        if old and keep_old:
            log.append(u"photo {}: {}; the older cached photo stays".format(key, why))
            return old[0], old[1], None
        log.append(u"photo {}: {}; pinned file(s): {}".format(key, why, u"; ".join(
            u"commons.wikimedia.org/wiki/File:" + t.replace(u" ", u"_") for t in files)))
        return None, None, why
    if state.get("offline"):
        return fallback(u"offline")
    if "refused" not in state:
        h = _photo_hold()
        if h:
            state["refused"] = u"{}, press again in {:.0f} min".format(h[0], max(1.0, h[1] / 60.0))
    if state.get("refused"):
        return fallback(state["refused"])
    try:
        os.makedirs(photo_dir, exist_ok=True)
        if "infos" not in state:                                      # every photo still to fetch, in one call
            need = []
            for k_, row in PLANTS.items():
                try:
                    with open(os.path.join(photo_dir, k_ + ".json"), "r", encoding="utf-8") as f:
                        m_ = json.load(f)
                    if (m_.get("title") in row[1] and m_.get("pageid")) or not (m_.get("source") or m_.get("title")):
                        continue
                except Exception:
                    pass
                need += [t for t in row[1] if t not in need]
            state["infos"] = {}                                       # a failed call is not repeated this press
            state["infos"] = _photo_infos(need, state)
        ii, why = None, u"file not found on Commons"
        for t in files:
            c = state["infos"].get(t)
            if c is None:
                continue
            artist, lic = _photo_meta(c)
            if not photo_free(lic):
                why = u"licence not open ({})".format(lic or u"none")
                continue
            if c.get("mime") not in ("image/jpeg", "image/png"):
                why = u"not a photo file"
                continue
            ii = (t, c, artist, lic)
            break
        if ii is None:
            return fallback(why)
        t, c, artist, lic = ii
        data = _photo_http(c.get("thumburl") or c["url"], state)
        p = os.path.join(photo_dir, key + ".jpg")
        if jpeg_info(data):
            with open(p, "wb") as f:
                f.write(data)
        else:
            tmp = os.path.join(photo_dir, key + ".src")
            with open(tmp, "wb") as f:
                f.write(data)
            if not _png_to_jpeg(tmp, p):
                return fallback(u"not a JPEG")
        au = _photo_safe(artist) or _photo_safe(c.get("user", u""))
        if artist and au != " ".join(artist.split()):
            log.append(u"photo {}: author '{}' printed as '{}' (the sheets' fonts)".format(key, artist, au))
        m = {"file": os.path.basename(p), "title": t, "pageid": c.get("pageid"), "author": au, "licence": lic,
             "source": c.get("descriptionurl", u""), "size": [c.get("width"), c.get("height")]}
        m["credit"] = photo_credit(name, m)
        with open(meta, "w", encoding="utf-8") as f:
            json.dump(m, f, ensure_ascii=False)
        log.append(u"photo {}: {} · page {} · {} · {} · {} x {} px".format(key, t, c.get("pageid"), au, lic,
                                                                          c.get("width"), c.get("height")))
        return p, m["credit"], None
    except Exception as ex:
        import socket
        import urllib.error
        if isinstance(ex, (urllib.error.URLError, socket.timeout, OSError)) and not isinstance(ex,
                                                                                              urllib.error.HTTPError):
            state["offline"] = True
        log.append(u"photo {}: {}: {}".format(key, type(ex).__name__, ex))
        if isinstance(ex, urllib.error.HTTPError):
            return fallback(state.get("refused") or u"Wikimedia error (HTTP {})".format(ex.code))
        return fallback(u"offline" if state.get("offline") else u"not loaded ({})".format(type(ex).__name__))


def fitz_add_photos(path, photos, page_h=297.0):
    """The photos put into a written PDF with PyMuPDF: photos = [(page index, x0, y0, x1, y1 mm, y up from the page
    foot, jpeg path)]; each JPEG fills its frame, cut to the frame's proportions about its centre (never stretched).
    The file is saved in place. Returns how many were placed."""
    import fitz
    K = 72.0 / 25.4
    doc = fitz.open(path)
    n = 0
    for pi, x0, y0, x1, y1, p in photos:
        try:
            with open(p, "rb") as f:
                data = f.read()
            info = jpeg_info(data)
            if not info or x1 <= x0 or y1 <= y0:
                continue
            iw, ih = float(info[0]), float(info[1])
            tmp = fitz.open()
            tp = tmp.new_page(width=iw, height=ih)
            tp.insert_image(tp.rect, stream=data)
            a = (x1 - x0) / (y1 - y0)
            cw, ch = (ih * a, ih) if iw / ih > a else (iw, iw / a)
            doc[pi].show_pdf_page(fitz.Rect(x0 * K, (page_h - y1) * K, x1 * K, (page_h - y0) * K), tmp, 0,
                                  clip=fitz.Rect((iw - cw) / 2.0, (ih - ch) / 2.0, (iw + cw) / 2.0, (ih + ch) / 2.0))
            tmp.close()
            n += 1
        except Exception:
            continue
    if n:
        t_ = path + ".tmp"
        doc.save(t_, garbage=3, deflate=True)
        doc.close()
        os.replace(t_, path)
    else:
        doc.close()
    return n
# ---- G13 units (MIRAQUA round 28 Oct 2026; Aras 28 Oct 13:21; SCRIPT_STANDARD §8 "UNITS") -----------------------
# Dimensions in cm, areas in m², heights and levels in m with 2 decimals. Where a cm or m² figure would be unreadable,
# one step up (m or km; ha), the same for every drawing of a type, never mixed inside one drawing; every scale bar and
# dimension says its unit. Converting a unit never changes the value. Inputs are always metres / square metres.
def u_num(v, nd=0):
    """1,234,567 / 12.35: thousands with commas, nd decimals"""
    return ("{:,.%df}" % nd).format(v)


def u_dim(m, unit="cm", nd=None, bare=False):
    """a dimension (horizontal or a chain): 3.0 -> '300' (unit 'cm'), '3.00 m', '1.2 km'; bare = no unit (a chain
    whose unit is written once at its end)"""
    if unit == "cm":
        s = u_num(m * 100.0, 0 if nd is None else nd)
    elif unit == "km":
        s = u_num(m / 1000.0, 1 if nd is None else nd)
    else:
        s = u_num(m, 2 if nd is None else nd)
    return s if bare else s + " " + unit


def u_level(m, sign=True):
    """a level or spot height: +47.60 (always 2 decimals)"""
    return ("%+.2f" if sign else "%.2f") % m


def u_height(m):
    """a height or depth: '6.00 m' (always 2 decimals)"""
    return "%.2f m" % m


def u_area(m2, unit="m²", nd=None):
    """an area: '11,524 m²' or '1.15 ha' (1 ha = 10,000 m²)"""
    if unit == "ha":
        return u_num(m2 / 10000.0, (1 if m2 >= 100000.0 else 2) if nd is None else nd) + " ha"
    return u_num(m2, 0 if nd is None else nd) + u" m²"


def u_volume(m3, nd=0):
    return u_num(m3, nd) + u" m³"
# ---- P19.2 / P15.2 (MIRAQUA round 28 Oct 2026): ONE set of architectural human figures ---------------------------
# Silhouettes at true scale (an adult 1.75 m) for every section and diagram that shows people (pp.14, 15, 19 and the
# p.15 occupancy diagram), replacing the stick figures and pictograms. Each pose is a skeleton (joints in metres,
# feet at y = 0, facing +x); fig_polys() turns it into filled outlines: a round-ended band per limb, the torso, the
# head. Draw every outline of a figure filled in one opaque colour (the section's ink or a lane colour), no stroke:
# the overlaps then read as one silhouette. Coordinates in metres; the caller scales them like the drawing.
FIG_LIMB = dict(arm=0.085, fore=0.07, thigh=0.15, shin=0.105, foot=0.07, neck=0.10)
FIG_POSES = {
    # standing, seen from the front
    "stand": dict(head=(0.0, 1.635, 0.105), torso=[(-0.2, 1.46), (0.2, 1.46), (0.17, 1.2), (0.155, 0.93), (-0.155, 0.93), (-0.17, 1.2)],
                  limbs=[("arm", (-0.185, 1.42), (-0.215, 1.13)), ("fore", (-0.215, 1.13), (-0.225, 0.84)),
                         ("arm", (0.185, 1.42), (0.215, 1.13)), ("fore", (0.215, 1.13), (0.225, 0.84)),
                         ("thigh", (-0.085, 0.95), (-0.095, 0.5)), ("shin", (-0.095, 0.5), (-0.095, 0.07)),
                         ("foot", (-0.095, 0.035), (-0.16, 0.035)),
                         ("thigh", (0.085, 0.95), (0.095, 0.5)), ("shin", (0.095, 0.5), (0.095, 0.07)),
                         ("foot", (0.095, 0.035), (0.16, 0.035)), ("neck", (0.0, 1.44), (0.0, 1.54))]),
    # walking, side view
    "walk": dict(head=(0.035, 1.635, 0.105), torso=[(-0.1, 1.45), (0.11, 1.45), (0.12, 1.2), (0.1, 0.92), (-0.12, 0.92), (-0.12, 1.2)],
                 limbs=[("thigh", (0.0, 0.95), (-0.09, 0.53)), ("shin", (-0.09, 0.53), (-0.27, 0.13)),
                        ("foot", (-0.29, 0.1), (-0.13, 0.035)),
                        ("thigh", (0.0, 0.95), (0.13, 0.52)), ("shin", (0.13, 0.52), (0.19, 0.08)),
                        ("foot", (0.15, 0.035), (0.33, 0.035)),
                        ("arm", (0.0, 1.41), (-0.1, 1.15)), ("fore", (-0.1, 1.15), (-0.17, 0.9)),
                        ("arm", (0.0, 1.41), (0.1, 1.15)), ("fore", (0.1, 1.15), (0.2, 0.92)),
                        ("neck", (0.0, 1.44), (0.02, 1.54))]),
    # standing, side view, pointing / watching forward
    "watch": dict(head=(0.03, 1.635, 0.105), torso=[(-0.11, 1.45), (0.11, 1.45), (0.12, 1.2), (0.1, 0.92), (-0.12, 0.92), (-0.12, 1.2)],
                  limbs=[("thigh", (0.0, 0.95), (0.02, 0.5)), ("shin", (0.02, 0.5), (0.0, 0.08)),
                         ("foot", (-0.03, 0.035), (0.16, 0.035)),
                         ("thigh", (-0.02, 0.95), (-0.06, 0.5)), ("shin", (-0.06, 0.5), (-0.08, 0.08)),
                         ("foot", (-0.11, 0.035), (0.08, 0.035)),
                         ("arm", (0.0, 1.41), (0.02, 1.13)), ("fore", (0.02, 1.13), (0.05, 0.86)),
                         ("arm", (0.02, 1.41), (0.22, 1.42)), ("fore", (0.22, 1.42), (0.45, 1.5)),
                         ("neck", (0.0, 1.44), (0.02, 1.54))]),
    # sitting on a step or bench (seat at 0.45 m under the hip), side view
    "sit": dict(head=(0.03, 1.215, 0.105), torso=[(-0.1, 1.03), (0.11, 1.03), (0.12, 0.8), (0.11, 0.48), (-0.12, 0.48), (-0.12, 0.8)],
                limbs=[("thigh", (0.0, 0.52), (0.44, 0.52)), ("shin", (0.44, 0.52), (0.47, 0.08)),
                       ("foot", (0.44, 0.035), (0.62, 0.035)),
                       ("arm", (0.0, 0.99), (0.08, 0.74)), ("fore", (0.08, 0.74), (0.3, 0.62)),
                       ("neck", (0.0, 1.02), (0.02, 1.12))]),
    # crouching at the edge, a hand down to the water, side view
    "touch": dict(head=(0.36, 1.0, 0.105), torso=[(0.12, 0.98), (0.3, 0.9), (0.24, 0.66), (0.02, 0.42), (-0.12, 0.5), (-0.02, 0.8)],
                  limbs=[("thigh", (-0.04, 0.47), (0.24, 0.5)), ("shin", (0.24, 0.5), (0.14, 0.08)),
                         ("foot", (0.1, 0.035), (0.29, 0.035)),
                         ("arm", (0.2, 0.9), (0.36, 0.64)), ("fore", (0.36, 0.64), (0.48, 0.3)),
                         ("neck", (0.22, 0.92), (0.3, 0.96))]),
    # wading: short steps, arms out for balance, side view
    "wade": dict(head=(0.03, 1.635, 0.105), torso=[(-0.11, 1.45), (0.11, 1.45), (0.12, 1.2), (0.1, 0.92), (-0.12, 0.92), (-0.12, 1.2)],
                 limbs=[("thigh", (0.0, 0.95), (0.07, 0.51)), ("shin", (0.07, 0.51), (0.1, 0.08)),
                        ("foot", (0.06, 0.035), (0.24, 0.035)),
                        ("thigh", (0.0, 0.95), (-0.05, 0.51)), ("shin", (-0.05, 0.51), (-0.12, 0.09)),
                        ("foot", (-0.15, 0.04), (0.02, 0.035)),
                        ("arm", (0.0, 1.41), (0.15, 1.2)), ("fore", (0.15, 1.2), (0.32, 1.12)),
                        ("arm", (0.0, 1.41), (-0.15, 1.2)), ("fore", (-0.15, 1.2), (-0.3, 1.1)),
                        ("neck", (0.0, 1.44), (0.02, 1.54))]),
    # cycling (bike way), side view; wheels as rings
    "bike": dict(head=(0.3, 1.56, 0.105), torso=[(0.05, 1.42), (0.23, 1.46), (0.18, 1.2), (-0.12, 0.95), (-0.26, 1.02), (-0.08, 1.28)],
                 limbs=[("thigh", (-0.2, 0.98), (0.12, 0.8)), ("shin", (0.12, 0.8), (0.02, 0.38)),
                        ("foot", (-0.02, 0.36), (0.12, 0.36)),
                        ("arm", (0.15, 1.42), (0.3, 1.2)), ("fore", (0.3, 1.2), (0.45, 1.06)),
                        ("neck", (0.18, 1.44), (0.26, 1.5)),
                        ("frame", (-0.55, 0.34), (-0.2, 0.9)), ("frame", (-0.2, 0.9), (0.0, 0.34)),
                        ("frame", (0.0, 0.34), (-0.55, 0.34)), ("frame", (-0.2, 0.9), (0.42, 0.92)),
                        ("frame", (0.0, 0.34), (0.42, 0.92)), ("frame", (0.42, 0.92), (0.55, 0.34)),
                        ("frame", (0.42, 0.92), (0.46, 1.06))],
                 rings=[(-0.55, 0.34, 0.34), (0.55, 0.34, 0.34)]),
}
FIG_ORDER = ("stand", "walk", "watch", "sit", "touch", "wade", "bike")


def _fig_band(p, q, w, n=5):
    """the outline of a band of width w from p to q with round ends"""
    import math as _m
    dx, dy = q[0] - p[0], q[1] - p[1]
    a = _m.atan2(dy, dx)
    r = w / 2.0
    out = []
    for c, a0 in ((q, a - _m.pi / 2), (p, a + _m.pi / 2)):
        for i in range(n + 1):
            t = a0 + _m.pi * i / n
            out.append((c[0] + r * _m.cos(t), c[1] + r * _m.sin(t)))
    return out


def _fig_circle(cx, cy, r, n=16):
    import math as _m
    return [(cx + r * _m.cos(2 * _m.pi * i / n), cy + r * _m.sin(2 * _m.pi * i / n)) for i in range(n)]


def fig_polys(pose, height=1.75, facing=1):
    """filled outlines of one figure, in metres, feet at (0, 0): pose = a FIG_POSES key; height 1.75 = adult (a child
    about 1.15, the head kept a little larger); facing -1 = mirrored (looking left)"""
    P = FIG_POSES[pose]
    k = height / 1.75
    hk = k ** 0.7 / k if k < 1.0 else 1.0               # a child's head is relatively larger
    f = 1.0 if facing >= 0 else -1.0

    def T(pt):
        return (f * pt[0] * k, pt[1] * k)
    out = [[T(p) for p in P["torso"]]]
    for kind, p, q in P["limbs"]:
        w = FIG_LIMB.get(kind, 0.035)
        out.append(_fig_band(T(p), T(q), w * k))
    for cx, cy, r in P.get("rings", ()):
        ring = _fig_circle(cx, cy, r, 20)
        for i in range(len(ring)):
            out.append(_fig_band(T(ring[i]), T(ring[(i + 1) % len(ring)]), 0.035 * k, 2))
    hx, hy, hr = P["head"]
    out.append(_fig_circle(f * hx * k, hy * k, hr * k * hk))
    return out
# ---- G4 (MIRAQUA round 28 Oct 2026): labels never overlap each other, symbols or important linework ----------------
# Geometry only (page mm, any y direction): the caller measures its text and draws. Order of tries for each label:
# the spots round its point, then farther out on a thin leader (the leader may not cross a placed label), then the
# same at the smaller sizes in `sizes`; a label still without a spot is dropped if its rank allows it (secondary
# labels), else it gets the nearest free spot anywhere in bounds, on a leader. Boxes are (x0, y0, x1, y1).
def lp_hit(a, b, pad=0.0):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def _lp_seg_box(p, q, b):
    """True when the segment p-q passes through box b (Liang-Barsky)"""
    x0, y0 = p
    dx, dy = q[0] - x0, q[1] - y0
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - b[0]), (dx, b[2] - x0), (-dy, y0 - b[1]), (dy, b[3] - y0)):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def lp_leader_end(b, p):
    """the point of box b nearest p (where a leader from p meets the label)"""
    return (min(max(p[0], b[0]), b[2]), min(max(p[1], b[1]), b[3]))


def label_spot(ax, ay, w, h, taken, bounds=None, segs=(), pad=0.5,
               rings=(0.8, 2.5, 5.0, 8.0, 12.0, 17.0, 24.0), n_ang=16):
    """a free box w x h near (ax, ay): (box, leader) or None. taken: placed boxes and symbol boxes; segs: important
    lines [(p, q)] a label may not sit on. leader = True when the box sits off the point (draw a thin leader)."""
    import math as _m

    def free(b):
        if bounds and not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
            return False
        if any(lp_hit(b, t, pad) for t in taken):
            return False
        return not any(_lp_seg_box(p, q, b) for p, q in segs)

    for i_r, d in enumerate(rings):
        for i in range(n_ang):
            a = 2 * _m.pi * (i + 0.5) / n_ang
            cx, cy = ax + _m.cos(a) * (d + w / 2.0), ay + _m.sin(a) * (d + h / 2.0)
            b = (cx - w / 2.0, cy - h / 2.0, cx + w / 2.0, cy + h / 2.0)
            if not free(b):
                continue
            far = i_r >= 2
            if far:
                e = lp_leader_end(b, (ax, ay))
                if any(_lp_seg_box((ax, ay), e, t) for t in taken
                       if not (t[0] <= ax <= t[2] and t[1] <= ay <= t[3])):     # the point's own symbol is passed
                    continue
            return b, far
    return None


def place_labels_all(items, taken, bounds=None, segs=(), sizes=(1.0, 0.9), pad=0.5):
    """items: dicts with x, y (anchor), wh (function size_factor -> (w, h)), rank (0 = must show, 1 = may be
    dropped). Places rank 0 first, then rank 1, each nearest its point. Returns {index: (box, leader, size_factor)}
    for the placed ones; dropped rank-1 labels are left out (the caller may list them in a key). taken grows."""
    out = {}
    order = sorted(range(len(items)), key=lambda i: items[i].get("rank", 0))
    for i in order:
        it = items[i]
        got = None
        for f in sizes:
            w, h = it["wh"](f)
            got = label_spot(it["x"], it["y"], w, h, taken, bounds, segs, pad)
            if got:
                got = (got[0], got[1], f)
                break
        if got is None and it.get("rank", 0) == 0 and bounds:
            w, h = it["wh"](sizes[-1])
            cands = []
            gx = bounds[0]
            while gx + w <= bounds[2]:
                gy = bounds[1]
                while gy + h <= bounds[3]:
                    cands.append((gx, gy))
                    gy += 2.0
                gx += 2.0
            cands.sort(key=lambda c: (c[0] + w / 2.0 - it["x"]) ** 2 + (c[1] + h / 2.0 - it["y"]) ** 2)
            for gx, gy in cands:
                b = (gx, gy, gx + w, gy + h)
                if not any(lp_hit(b, t, pad) for t in taken) and not any(_lp_seg_box(p, q, b) for p, q in segs):
                    got = (b, True, sizes[-1])
                    break
        if got:
            taken.append(got[0])
            out[i] = got
    return out
LOG_DIR = bg_logs()                       # Aras 25 Oct 09:34-09:35: every script's log here


def write_log(text):
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(os.path.join(LOG_DIR, "bergama_agriculture_alternatives_log.txt"), "w", encoding="utf-8") as f:
            f.write(text)
    except Exception:
        pass
    return text

# v1 24 Oct: all files under Downloads/Bergama/ (Aras rule)
OUT_DIR = bg_output("Bergama_agriculture_alternatives")       # final PDFs only (27 Oct)
OUT_PDF = "Bergama_agriculture_alternatives_A3.pdf"
# built-in geometry and tables (survey coordinates, m): around2 extent, site frame, WorldCover classes clipped to the
# extent (outside / inside the site), Selinos and other streams, FAO-56 net irrigation per water year (C1), corridor cover
def bergama_data(name, _c={}):
    """Built-in data kept in Downloads/Bergama/Data/bergama_agriculture_alternatives_data.py (Aras 25 Oct 21:29, scripts shortened): runs its
    section `name` here, as if it were written in this place. The file is read once per run; a missing file or one
    from another version of this script stops the script with a message saying which file to copy."""
    import os as _os, hashlib as _hl
    if not _c:
        p_ = _os.path.join(_os.path.expanduser("~"), "Downloads", "Bergama", "Data", "bergama_agriculture_alternatives_data.py")
        if not _os.path.isfile(p_):
            raise RuntimeError("Data file missing: copy bergama_agriculture_alternatives_data.py from the run kit's Data folder into " + _os.path.dirname(p_))
        with open(p_, encoding="utf-8", newline="") as f_:
            for part_ in f_.read().split("\n#@@ ")[1:]:
                k_, _, b_ = part_.partition("\n")
                _c[k_] = b_
    b_ = _c.get(name)
    if b_ is None or _hl.md5(b_.encode("utf-8")).hexdigest() != {'GEO': '8db5c86b0c11c98efb00cbe4dffb2aff', 'STEPS': '1fda2b774117b9c7a365a61ad6be5ac7', 'SKETCH_SRC': 'd8187f7176a997246aa983a6fdc66cdc'}.get(name):
        raise RuntimeError("Data file bergama_agriculture_alternatives_data.py is not the one made with this script version (part " + name +
                           "): copy it again from the same run kit as the script")
    exec(compile(b_, "bergama_agriculture_alternatives_data.py:" + name, "exec"), globals())


bergama_data("GEO")

# ------------------------------------------------------------------ live numbers from the water balance (Thread 2)
# The water balance script writes its results on every run; this script reads them, so storage and the share covered
# are never typed in here. Searched in this order; the first file found wins.
LIVE_FILES = [os.path.join(bg_cache("Bergama_water_balance_analysis"), "water_balance_results.json"),   # 27 Oct: cached/
              os.path.join(bg_output("Bergama_water_balance_analysis"), "water_balance_results.json"),  # v2.6 and older
              os.path.join(os.path.expanduser("~"), "Downloads", "Bergama_water_balance_analysis", "water_balance_results.json")]   # old place, read fallback
# fallback: the cloud copy research/water_balance/water_balance_results_default.json (default lands, 24 Oct 08:23)
DEFAULT = json.loads('{"cutoff":{"orchard olive + cropland cotton":{"central":{"storage_m3":375000,"covered_pct_1in5_dry":99.2,"delivered_m3_per_year":336093}},"orchard olive + cropland tomato":{"central":{"storage_m3":350000,"covered_pct_1in5_dry":99.7,"delivered_m3_per_year":310094}}},"farm_demand_m3":{"orchard olive + cropland cotton":{"mean":339980,"median":348773,"wet5":315782,"dry5":356580,"dry10":382453,"min":278845,"max":393001,"dry5_year":2006},"orchard olive + cropland tomato":{"mean":311982,"median":319136,"wet5":288317,"dry5":334143,"dry10":343054,"min":251458,"max":362453,"dry5_year":2021}},"net_irrigation_mm":{"olive":{"mean":614.3,"median":619.5,"wet5":519.6,"dry5":720.1,"dry10":725.2,"min":415.2,"max":822.7},"cotton":{"mean":853.2,"median":875.6,"wet5":789.5,"dry5":891.8,"dry10":962.6,"min":703.1,"max":981.9},"maize":{"mean":722.7,"median":740.8,"wet5":675.4,"dry5":761.8,"dry10":816.2,"min":605.7,"max":835.7},"tomato":{"mean":781.0,"median":801.3,"wet5":719.7,"dry5":837.0,"dry10":860.8,"min":632.5,"max":903.1}},"lands":{"cropland_ha":34.9,"orchard_ha":1.34,"cropland_crops":"cotton,tomato"}}')
DEFAULT_NOTE = "water balance default-lands copy, 24 Oct"   # v1.4: the log says when it is used

def live():
    """storage, share covered and need per mix (cost cut-off, central case), farm areas, crops and net need per crop"""
    d, src = None, DEFAULT_NOTE
    for p in LIVE_FILES:
        try:
            with open(p, "r", encoding="utf-8") as f:
                d = json.load(f)
            src = "water balance results of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(p)))
            break
        except Exception:
            d = None
    if d is None: d = DEFAULT
    mixes = [m for m in d["cutoff"] if m in d["farm_demand_m3"]]
    L = dict(storage_m3=[d["cutoff"][m]["central"]["storage_m3"] for m in mixes],
             farm_share_dry5_pct=[d["cutoff"][m]["central"]["covered_pct_1in5_dry"] for m in mixes],
             farm_need_dry5_m3=[d["farm_demand_m3"][m]["dry5"] for m in mixes],
             cropland_ha=d["lands"]["cropland_ha"], orchard_ha=d["lands"]["orchard_ha"],
             crops=[c.strip() for c in str(d["lands"].get("cropland_crops", "")).split(",") if c.strip()],
             net=d["net_irrigation_mm"])
    L["year_split"] = (d.get("design") or {}).get("year_split")      # v3: water balance v4 and newer
    L["design_mix"] = (d.get("design") or {}).get("mix", "")
    return L, src

def span(v):
    return (min(v), max(v)) if isinstance(v, (list, tuple)) else (v, v)

# ------------------------------------------------------------------ colours (palette v1.4 core roles)
C = dict(ground="E2E0D4", paper="EFEDE6", faint="D8D5CC", structure="B0AC9C", ink2="847E75", ink="4A3F35",
         green_deep="495338", green_mid="727A4E", green_light="8C9969", water_deep="5D7F8D", water="91ADB4",
         water_light="C1D3DB", accent="8B3A3F", accent_deep="633131", white="FFFFFF",
         field="BDB57A", orchard="70754C", tree="89986A", grass="C9CDB0", shrub="A2B6B5", olive="5C7A86")

def rgb(h): return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

# ------------------------------------------------------------------ minimal vector PDF (mm units, Helvetica, whole strings)
_HW = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278] + [556] * 10 + \
      [278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778,
       667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556,
       278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334,
       260, 334, 584]

_ENC_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}   # Turkish letters in unused WinAnsi slots
_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
# v3 (Aras 27 Oct, Prompt 6: "325,000-375,000 m"): ² and ³ are drawn as the digit at 0.6 x the size, raised 0.28 x the
# size (then as wide as the ²/³ glyph, 333/1000): the unembedded Helvetica's ²/³ was missing in some viewers
SUP = {u"²": u"2", u"³": u"3"}
SUP_K, SUP_UP = 0.6, 0.28


def sup_runs(s):
    """v3: s cut into (text, raised) runs at ² and ³, which become a plain 2 or 3"""
    out, cur = [], u""
    for ch in s:
        if ch in SUP:
            if cur: out.append((cur, False))
            out.append((SUP[ch], True)); cur = u""
        else:
            cur += ch
    if cur: out.append((cur, False))
    return out

def text_w(s, size, bold=False):
    w = sum(_HW[ord(ch) - 32] if 32 <= ord(ch) < 127 else 556 for ch in s)
    return w / 1000.0 * size * (1.06 if bold else 1.0) * 0.3528      # size in pt -> width in mm


# ---- G2/G3 (MIRAQUA round, 28 Oct 2026): Arial EMBEDDED in every sheet PDF -------------------------------------
# The sheets wrote the PDF standard fonts without embedding (Helvetica, Courier) with the Turkish letters in unused
# WinAnsi slots: the text was right (it copies and searches as İ ğ ş), but viewers without those glyphs drew nothing
# ("stiklal", "De irmen"). Now each font slot is Arial, embedded as a simple TrueType font with the SAME encoding
# (WinAnsi + the six Turkish letters in slots 129/141/143/144/157/158), so the strings, their measuring and the
# booklet's reading of the sheets stay as they were. Arial has Helvetica's widths, so nothing moves; text measured
# as Courier (the old monospace captions) comes out a little shorter. Text stays live for Illustrator.
# The font files are the system's (C:\Windows\Fonts\arial*.ttf, or the user's font folder): read and packed once per
# run. If a file is missing, that slot falls back to the old standard font and PDF_FONT_NOTE says so (for the log).
_PF_EXTRA = {u"Ğ": 0x81, u"ğ": 0x8D, u"İ": 0x8F, u"ı": 0x90, u"Ş": 0x9D, u"ş": 0x9E}
_PF_DIFF = "/Differences [129 /Gbreve 141 /gbreve 143 /Idotaccent 144 /dotlessi 157 /Scedilla 158 /scedilla]"
_PF_FILES = {"R": ("arial.ttf", "ArialMT", "Helvetica"), "B": ("arialbd.ttf", "Arial-BoldMT", "Helvetica-Bold"),
             "I": ("ariali.ttf", "Arial-ItalicMT", "Helvetica-Oblique"),
             "BI": ("arialbi.ttf", "Arial-BoldItalicMT", "Helvetica-BoldOblique")}
_PF_CACHE = {}
PDF_FONT_NOTE = []


def _pf_path(fn):
    import os as _o
    dirs = [_o.path.join(_o.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
            _o.path.join(_o.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"),
            "/Library/Fonts", "/System/Library/Fonts/Supplemental", "/usr/share/fonts/truetype/msttcorefonts"]
    for d in dirs:
        for nm in (fn, fn.capitalize(), fn.upper()):
            p = _o.path.join(d, nm)
            if _o.path.isfile(p):
                return p
    return None


def _pf_metrics(data):
    """widths of codes 32-255 (1000 units per em) and the descriptor numbers, read from the TrueType tables"""
    import struct as _s
    n = _s.unpack(">H", data[4:6])[0]
    tab = {}
    for i in range(n):
        tag, _c, off, ln = _s.unpack(">4sIII", data[12 + 16 * i:28 + 16 * i])
        tab[tag.decode("latin-1")] = (off, ln)
    h = tab["head"][0]
    upm = _s.unpack(">H", data[h + 18:h + 20])[0]
    bbox = _s.unpack(">hhhh", data[h + 36:h + 44])
    hh = tab["hhea"][0]
    asc, desc = _s.unpack(">hh", data[hh + 4:hh + 8])
    nhm = _s.unpack(">H", data[hh + 34:hh + 36])[0]
    hm = tab["hmtx"][0]
    adv = [_s.unpack(">H", data[hm + 4 * i:hm + 4 * i + 2])[0] for i in range(nhm)]
    cm = tab["cmap"][0]
    sub = None
    for i in range(_s.unpack(">H", data[cm + 2:cm + 4])[0]):
        pid, eid, off = _s.unpack(">HHI", data[cm + 4 + 8 * i:cm + 12 + 8 * i])
        if pid == 3 and eid == 1:
            sub = cm + off
    seg = _s.unpack(">H", data[sub + 6:sub + 8])[0] // 2
    ends = _s.unpack(">%dH" % seg, data[sub + 14:sub + 14 + 2 * seg])
    p = sub + 16 + 2 * seg
    starts = _s.unpack(">%dH" % seg, data[p:p + 2 * seg])
    deltas = _s.unpack(">%dh" % seg, data[p + 2 * seg:p + 4 * seg])
    ro_at = p + 4 * seg
    ros = _s.unpack(">%dH" % seg, data[ro_at:ro_at + 2 * seg])

    def gid(u):
        for k in range(seg):
            if starts[k] <= u <= ends[k]:
                if ros[k] == 0:
                    return (u + deltas[k]) & 0xFFFF
                a = ro_at + 2 * k + ros[k] + 2 * (u - starts[k])
                g = _s.unpack(">H", data[a:a + 2])[0]
                return (g + deltas[k]) & 0xFFFF if g else 0
        return 0
    inv = dict((v, k) for k, v in _PF_EXTRA.items())
    widths = []
    for code in range(32, 256):
        try:
            ch = inv.get(code) or bytes([code]).decode("cp1252")
        except Exception:
            ch = None
        g = gid(ord(ch)) if ch else 0
        widths.append(int(round(adv[min(g, nhm - 1)] * 1000.0 / upm)) if g else 0)
    cap, ital, weight = 0.716 * upm, 0.0, 400
    if "OS/2" in tab:
        o = tab["OS/2"][0]
        weight = _s.unpack(">H", data[o + 4:o + 6])[0]
        if _s.unpack(">H", data[o:o + 2])[0] >= 2:
            cap = _s.unpack(">h", data[o + 88:o + 90])[0]
    if "post" in tab:
        o = tab["post"][0]
        ital = _s.unpack(">i", data[o + 4:o + 8])[0] / 65536.0
    k = 1000.0 / upm
    return dict(widths=widths, bbox=[int(round(v * k)) for v in bbox], asc=int(round(asc * k)),
                desc=int(round(desc * k)), cap=int(round(cap * k)), ital=ital, bold=weight >= 600)


def _pf_style(st):
    """(compressed font file, its length, metrics, PostScript name) of one style, or None: read once per run"""
    if st not in _PF_CACHE:
        fn, ps, _std = _PF_FILES[st]
        p, got = _pf_path(fn), None
        if p:
            try:
                import zlib as _z
                with open(p, "rb") as fh:
                    raw = fh.read()
                got = (_z.compress(raw, 6), len(raw), _pf_metrics(raw), ps)
            except Exception as e:
                PDF_FONT_NOTE.append("font %s not read (%s): standard font used" % (fn, e))
        else:
            PDF_FONT_NOTE.append("font %s not found: standard font %s used (Turkish letters may not show)" % (fn, _std))
        _PF_CACHE[st] = got
    return _PF_CACHE[st]


def pdf_fonts(add, styles, content=None):
    """Font objects for a PDF writer: styles = one of "R", "B", "I", "BI" per font slot /F1, /F2 ... in order (a slot
    may repeat a style: the same objects are used). add(bytes) -> object number, as the writers' own add().
    content: the page content (str or bytes); when given, a slot it never uses gets the light standard-font object
    instead of an embedded file. Returns the object numbers, one per slot."""
    if isinstance(content, bytes):
        content = content.decode("latin-1")
    made, out = {}, []
    for i, st in enumerate(styles):
        used = content is None or ("/F%d " % (i + 1)) in content
        key = st if used else "std-" + st
        if key not in made:
            got = _pf_style(st) if used else None
            if got is None:
                made[key] = add(("<< /Type /Font /Subtype /Type1 /BaseFont /%s /Encoding << /Type /Encoding "
                                 "/BaseEncoding /WinAnsiEncoding %s >> >>" % (_PF_FILES[st][2], _PF_DIFF)).encode("latin-1"))
            else:
                data, n, m, ps = got
                ff = add(("<< /Length %d /Length1 %d /Filter /FlateDecode >>\nstream\n" % (len(data), n)).encode("latin-1")
                         + data + b"\nendstream")
                flags = 32 + (64 if "I" in st else 0)
                fd = add(("<< /Type /FontDescriptor /FontName /%s /Flags %d /FontBBox [%s] /ItalicAngle %s /Ascent %d "
                          "/Descent %d /CapHeight %d /StemV %d /FontFile2 %d 0 R >>" % (
                              ps, flags, " ".join(str(v) for v in m["bbox"]), ("%.1f" % m["ital"]), m["asc"], m["desc"],
                              m["cap"], 140 if m["bold"] else 80, ff)).encode("latin-1"))
                made[key] = add(("<< /Type /Font /Subtype /TrueType /BaseFont /%s /FirstChar 32 /LastChar 255 "
                                 "/Widths [%s] /FontDescriptor %d 0 R /Encoding << /Type /Encoding /BaseEncoding "
                                 "/WinAnsiEncoding %s >> >>" % (ps, " ".join(str(w) for w in m["widths"]), fd, _PF_DIFF)
                                 ).encode("latin-1"))
        out.append(made[key])
    return out

class Page:
    def __init__(self, w, h):
        self.w, self.h, self.ops, self.alphas = w, h, [], set()
    def _c(self, h, stroke=False):
        r, g, b = rgb(h); return "%.3f %.3f %.3f %s" % (r, g, b, "RG" if stroke else "rg")
    def rect(self, x, y, w, h, fill=None, stroke=None, lw=0.2):
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, stroke, lw, True)
    def poly(self, P, fill=None, stroke=None, lw=0.2, closed=False, dash=None, alpha=None):
        self.path([P], fill, stroke, lw, closed, dash, alpha)
    def path(self, rings, fill=None, stroke=None, lw=0.2, closed=True, dash=None, alpha=None):
        """several rings in one path; a fill uses even-odd, so holes stay open. v1.5: alpha = opacity 0-1 (sketch washes)"""
        k = 72 / 25.4; o = ["q"]
        if alpha is not None and alpha < 0.995:
            a_ = max(1, int(round(alpha * 100))); self.alphas.add(a_); o.append("/GA%d gs" % a_)
        if fill: o.append(self._c(fill))
        if stroke: o.append(self._c(stroke, True)); o.append("%.3f w 1 J 1 j" % (lw * k))
        if dash: o.append("[%.2f %.2f] 0 d" % (dash[0] * k, dash[1] * k))
        for P in rings:
            o.append("%.2f %.2f m" % (P[0][0] * k, P[0][1] * k))
            o += ["%.2f %.2f l" % (x * k, y * k) for x, y in P[1:]]
            if closed: o.append("h")
        o.append("B*" if fill and stroke else ("f*" if fill else "S")); o.append("Q")
        self.ops.append(" ".join(o))
    def line(self, P, col, lw=0.25, dash=None): self.path([P], None, col, lw, False, dash)
    def circle(self, x, y, r, fill=None, stroke=None, lw=0.2):          # v1.2: for the pictograms
        self.poly([(x + r * math.cos(k * math.pi / 12), y + r * math.sin(k * math.pi / 12)) for k in range(24)], fill, stroke, lw, True)
    def text(self, s, x, y, size, col="4A3F35", bold=False, align="L", halo=None):
        if any(ch in SUP for ch in s):             # v3 (Prompt 6): m² / m³ as a raised small digit (see SUP)
            runs = sup_runs(s)
            ws = [text_w(t, size * (SUP_K if up else 1.0), bold) for t, up in runs]
            x -= {"L": 0.0, "C": sum(ws) / 2.0, "R": sum(ws)}[align]
            for (t, up), w_ in zip(runs, ws):
                self.text(t, x, y + (size * SUP_UP * 0.3528 if up else 0.0), size * (SUP_K if up else 1.0), col, bold,
                          "L", halo)
                x += w_
            return
        if align == "C": x -= text_w(s, size, bold) / 2
        elif align == "R": x -= text_w(s, size, bold)
        k = 72 / 25.4
        b = b"".join(bytes([_ENC_EXTRA[ch]]) if ch in _ENC_EXTRA else ch.encode("cp1252", "replace") for ch in s)   # 25 Oct: ı İ ğ Ğ ş Ş spelt right
        b = b.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)")
        if halo:                                   # v1.5: the sketches' text mask, a halo in the ground's colour
            self.ops.append("q %s %.2f w 1 j BT 2 Tr /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET Q" % (
                self._c(halo, True), size * 0.35, "F2" if bold else "F1", size, self._c(halo), x * k, y * k, b.decode("latin-1")))
        self.ops.append("BT /%s %.2f Tf %s %.2f %.2f Td (%s) Tj ET" % ("F2" if bold else "F1", size, self._c(col), x * k, y * k, b.decode("latin-1")))
    def para(self, s, x, y, w, size, col="4A3F35", bold=False, lead=1.3):
        line, yy = "", y
        for word in s.split(" "):
            t = (line + " " + word).strip()
            if text_w(t, size, bold) > w and line:
                self.text(line, x, yy, size, col, bold); yy -= size * 0.3528 * lead; line = word
            else: line = t
        if line: self.text(line, x, yy, size, col, bold); yy -= size * 0.3528 * lead
        return yy

def write_pdf(pages, path):
    k = 72 / 25.4
    n = len(pages)
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [%s] /Count %d >>" % (" ".join("%d 0 R" % (5 + 2 * i) for i in range(n)), n),
            "", ""]
    extra, first = [], 5 + 2 * n                          # G2/G3 28 Oct: Arial embedded (common/pdf_fonts.py):

    def add(b):                                           # font file + descriptor go after the pages
        extra.append(b.decode("latin-1"))
        return first + len(extra) - 1
    fid = pdf_fonts(add, ("R", "B"))
    objs[2], objs[3] = extra[fid[0] - first], extra[fid[1] - first]   # the font dicts themselves stay objects 3, 4
    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"); offs = []
    for i, o in enumerate(objs):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (i + 1, o)).encode("latin-1")
    for i, pg in enumerate(pages):
        content = zlib.compress("\n".join(pg.ops).encode("latin-1"))
        offs.append(len(out))
        gs = "".join("/GA%d << /Type /ExtGState /ca %.2f /CA %.2f >> " % (a, a / 100.0, a / 100.0) for a in sorted(pg.alphas))
        out += ("%d 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.2f %.2f] /Resources << /Font << /F1 3 0 R /F2 4 0 R >>%s >> /Contents %d 0 R >>\nendobj\n"
                % (5 + 2 * i, pg.w * k, pg.h * k, (" /ExtGState << %s>>" % gs) if gs else "", 6 + 2 * i)).encode("latin-1")
        offs.append(len(out))
        out += ("%d 0 obj\n<< /Length %d /Filter /FlateDecode >>\nstream\n" % (6 + 2 * i, len(content))).encode("latin-1") + content + b"\nendstream\nendobj\n"
    for j, o in enumerate(extra):
        offs.append(len(out)); out += ("%d 0 obj\n%s\nendobj\n" % (first + j, o)).encode("latin-1")
    x = len(out)
    out += ("xref\n0 %d\n0000000000 65535 f \n" % (len(offs) + 1) + "".join("%010d 00000 n \n" % o for o in offs) +
            "trailer\n<< /Size %d /Root 1 0 R /Info << /Title (Bergama agriculture alternatives) >> >>\nstartxref\n%d\n%%%%EOF\n" % (len(offs) + 1, x)).encode("latin-1")
    with open(path, "wb") as f: f.write(out)

# ------------------------------------------------------------------ shared helpers
def fmt(v): return "{:,.0f}".format(v)
def fmt1(v): return "{:,.1f}".format(v)
def rnd(v, step=1000): return int(round(v / step) * step)
EFF = 0.90          # drip application efficiency, as the water balance (key figures "basis": "drip 90 %")

NET = {}            # net irrigation mm per crop from the water balance results (mean, dry5 = 1-in-5 dry year), set in build()

def gross_m3_ha(crop, year):
    if crop == "mix":                  # field crops weighted by their 2025 Bergama areas
        w = {c: TUIK_2025_DA[c] for c in ("cotton", "maize", "tomato") if c in NET}
        return sum(gross_m3_ha(c, year) * v for c, v in w.items()) / sum(w.values())
    return NET[crop]["mean" if year == "normal" else "dry5"] / EFF * 10.0     # 1 mm on 1 ha = 10 m3

SRC_KEY = []          # v1.6: sources printed as [n] on pages 1-3, numbered once for the sheet; the key is page 4
LOG_NOTES = []        # v1.6: what the layout left out (log)

def cite(src):
    """v1.2 (water board v1.6 method): the number of a source in the sheet's key (v1.6: page 4), as "[n]".
    v4 (MIRAQUA 28 Oct, F5): "" for a source that is not public online (F5_OFF): no mark, not in the key."""
    if src in F5_OFF:
        return ""
    if src not in SRC_KEY: SRC_KEY.append(src)
    return "[%d]" % (SRC_KEY.index(src) + 1)


def cited(s, *srcs):
    """v4 (F5): s with its [n] marks after one space, or s alone when none of its sources is public"""
    mk = "".join(cite(q) for q in srcs if q)
    return s + (" " + mk if mk else "")

def wrap(s, size, w, bold=False):
    out, line = [], ""
    for word in s.split(" "):
        t = (line + " " + word).strip()
        if text_w(t, size, bold) > w and line: out.append(line); line = word
        else: line = t
    if line: out.append(line)
    return out

# ------------------------------------------------------------------ v2 (Aras 27 Oct, Prompt 5): plant and crop photos
# The photos and the "English (Turkish)" names come from src/common/plant_photos.py (one cache folder for every script,
# every photo PHOTO_W x PHOTO_H mm). This PDF writer draws only the frame (thin, faint; "no photo" inside when there is
# none); the JPEGs go into the frames after write_pdf (put_photos, PyMuPDF). Each photo's credit is a [n] mark after its
# name, its key on the sources page.
PH_GAP = 2.0                         # mm between two photos side by side
PHOTO_GOT = {}                       # key -> (jpeg path or None, credit or None, why not), read once a press
PHOTO_LOG, PHOTO_STATE = [], {}      # plant_photos' own notes (web fetch) and its offline flag
PHOTO_FR = []                        # frames with a photo: (page index, x0, y0, x1, y1 mm y up, jpeg path)
PHOTO_N = [0]                        # frames drawn, with or without a photo


def photo_get(key):
    """v2: (jpeg path or None, credit or None, why not) of a plant in PLANTS, once a press; never raises"""
    if key not in PHOTO_GOT:
        try:
            PHOTO_GOT[key] = plant_photo_of(key, PHOTO_LOG, PHOTO_STATE)
        except Exception as ex:
            PHOTO_GOT[key] = (None, None, "%s: %s" % (type(ex).__name__, ex))
    return PHOTO_GOT[key]


def photo_mark(key):
    """v2: the [n] of a plant photo's credit (its key on the sources page); "" when there is no photo"""
    p, credit, _ = photo_get(key)
    return cite(credit) if p and credit else ""


def photo_frame(pg, pi, key, x, top, P=None):
    """v2: the frame of a plant's photo, PHOTO_W x PHOTO_H mm, its top-left at (x, top) on page index pi: a thin faint
    outline, and the photo recorded for put_photos, or "no photo" inside the frame. P: a Placer that keeps the frame.
    v4 (MIRAQUA 28 Oct, G12): an empty frame says why, as the water board's cards: "no photo: " + the loader's reason
    (common/plant_photos.py: offline, Wikimedia refused (HTTP 429) press again later, file not found, licence ...),
    7 pt (the booklet's smallest), top left in the frame."""
    p, _cr, why = photo_get(key)
    pg.rect(x, top - PHOTO_H, PHOTO_W, PHOTO_H, stroke=C["faint"], lw=0.2)
    PHOTO_N[0] += 1
    if p:
        PHOTO_FR.append((pi, x, top - PHOTO_H, x + PHOTO_W, top, p))
    else:
        pg.para(u"no photo: " + (why or u"not loaded"), x + 1.5, top - 4.0, PHOTO_W - 3.0, 7, C["ink2"], lead=1.2)
    if P is not None:
        P.boxes.append((x, top - PHOTO_H, x + PHOTO_W, top))


def name_lines(key, mark, size, w, bold=True):
    """v2: a plant's name under its photo: "English (Turkish) [n]" on one line when it fits in w, else the English name
    and "(Turkish) [n]" on two (each wrapped to w if it is longer still)"""
    t = plant_name(key) + ((" " + mark) if mark else "")
    if text_w(t, size, bold) <= w:
        return [t]
    en, _, tr = plant_name(key).partition(" (")
    if not tr:
        return wrap(t, size, w, bold)
    return wrap(en, size, w, bold) + wrap("(" + tr + ((" " + mark) if mark else ""), size, w, bold)


def name_lc(key):
    """v2: a plant's name in running text: "olive (Zeytin)" """
    s = plant_name(key)
    return s[:1].lower() + s[1:]


def name_caps(key):
    """v2: a plant's name in a capitals heading, the Turkish part with the dotted İ: "OLIVE (ZEYTİN)" """
    en, _, tr = plant_name(key).partition(" (")
    return en.upper() + ((" (" + tr.replace(u"i", u"İ").upper()) if tr else "")


def crop_word(key):
    """v4 (MIRAQUA 28 Oct, G11): a crop key as a short printed word, the English name of the shared table: "maize" ->
    "corn", "cotton" -> "cotton"; a key the table does not have stays as it is"""
    return plant_name(key).partition(" (")[0].lower() if key in PLANTS else key


def put_photos(path):
    """v2: the plant and crop photos into their frames on pages 1 and 3 (PyMuPDF, after write_pdf and put_base); a photo
    error never stops the sheet. Returns the log lines: how many were placed, and why each missing one is missing."""
    n, err = 0, ""
    try:
        if PHOTO_FR:
            n = fitz_add_photos(path, PHOTO_FR)
    except Exception as ex:
        err = " · FLAG not placed: %s: %s" % (type(ex).__name__, ex)
    if not err and n < len(PHOTO_FR):
        err = " · %d JPEG(s) could not be read" % (len(PHOTO_FR) - n)
    out = ["photos: %d of %d placed (cached/plant_photos)%s" % (n, PHOTO_N[0], err)]
    out += ["  no photo: %s (%s)" % (plant_name(k), v[2] or "not loaded") for k, v in PHOTO_GOT.items() if not v[0]]
    out += ["  " + t for t in PHOTO_LOG]
    return "\n".join(out)

STAGE_TAG = u"C  WATER  ·  WHAT WE DO WITH IT"   # v3 (Prompt 6, rule 7): the booklet's theme and stage of pages 1 and 3


HEAD_Y = (285.0, 276.5, 269.5)       # v4 (MIRAQUA 28 Oct, P19.1): baselines of the kicker, the title and the subtitle


def header(pg, title, sub, hole=None, tag=None):
    """v4 (MIRAQUA 28 Oct, F10 decision 3, default remove; P19.1): the sheet's big page number before the title is
    gone (it read as a booklet page number); the booklet stage tag (pages 1 and 3) is the kicker over the title, top
    left, where the booklet's own pages carry theirs (8 pt, 12 mm from the top edge); title and subtitle on the 14 mm
    margin (were at 26 behind the number). G1: no "AGRICULTURE ANALYSIS · GROUP 6" line (page 2 had it)."""
    if hole:                                       # v1.5: a window left open for a plan placed under the page
        x0, y0, x1, y1 = hole
        pg.path([[(0, 0), (420, 0), (420, 297), (0, 297)], [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]], fill=C["white"])
    else:                                          # v1.6 (Aras 27 Oct): white, the beige paper goes
        pg.rect(0, 0, 420, 297, fill=C["white"])
    if tag:                                        # v3: pages 1 and 3 name their booklet stage (accent, as its kicker)
        pg.text(tag, 14, HEAD_Y[0], 8, C["accent"], True)
    pg.text(title, 14, HEAD_Y[1], 22, C["ink"], True)
    pg.text(sub, 14, HEAD_Y[2], 11, C["ink2"])

# ------------------------------------------------------------------ v1.2 pictograms and tiles (from water board v1.6/v1.7)
def icon(pg, kind, x, y, sz):
    """a pictogram in the square (x, y - sz)-(x + sz, y), drawn on a 10 x 10 grid. Graphic only."""
    u = sz / 10.0; lw = 0.07 * sz
    P = lambda pts: [(x + a * u, y - sz + b * u) for a, b in pts]
    Q = lambda a0, b0, a1, b1: P([(a0, b0), (a1, b0), (a1, b1), (a0, b1)])
    O = lambda a, b, r, **kw: pg.circle(x + a * u, y - sz + b * u, r * u, **kw)
    pt = lambda mm: mm / 0.3528

    def drop(a, b, r, col):
        pg.poly(P([(a - r * 0.85, b + r * 0.45), (a, b + r * 2.2), (a + r * 0.85, b + r * 0.45)]), fill=col, closed=True)
        O(a, b, r, fill=col)
    ink, ink2, acc = C["ink"], C["ink2"], C["accent"]
    if kind == "nowater":                       # no water-hungry crops
        drop(5.0, 2.6, 2.3, C["water"])
        pg.line(P([(1.2, 1.0), (8.8, 9.2)]), acc, lw * 1.4)
    elif kind == "cotton":
        pg.line(P([(5.0, 0.4), (5.0, 5.0)]), C["green_deep"], lw)
        for a, b in ((3.3, 5.9), (6.7, 5.9), (5.0, 8.1)): O(a, b, 1.9, fill=C["white"], stroke=ink2, lw=lw * 0.6)
    elif kind == "olive":
        pg.poly(Q(4.5, 0.4, 5.5, 4.4), fill=ink2, closed=True)
        O(5.0, 6.2, 3.4, fill=C["green_mid"])
        for a, b in ((3.8, 6.8), (6.0, 5.4), (5.4, 7.8)): O(a, b, 0.5, fill=ink)
    elif kind == "drip":
        pg.poly(Q(0, 7.0, 10, 8.4), fill=ink2, closed=True)
        for a in (2.0, 5.0, 8.0): drop(a, 3.4, 0.8, C["water_deep"])
        pg.poly(Q(0, 0.4, 10, 1.6), fill=C["field"], closed=True)
    elif kind == "cube":                        # storage
        pg.poly(P([(5, 9.8), (9.2, 7.6), (5, 5.4), (0.8, 7.6)]), fill=C["water_light"], closed=True)
        pg.poly(P([(0.8, 7.6), (5, 5.4), (5, 0.4), (0.8, 2.6)]), fill=C["water"], closed=True)
        pg.poly(P([(5, 5.4), (9.2, 7.6), (9.2, 2.6), (5, 0.4)]), fill=C["water_deep"], closed=True)
    elif kind in ("inside", "outside"):         # fields inside / outside the site frame
        if kind == "inside":
            pg.poly(Q(0.6, 0.6, 9.4, 9.4), fill="E8E5DA", stroke=ink, lw=lw, closed=True)
            pg.poly(P([(2.0, 2.0), (6.6, 2.0), (8.0, 6.4), (3.4, 6.4)]), fill=C["field"], closed=True)
        else:
            pg.poly(Q(0.4, 3.4, 5.4, 9.4), fill="E8E5DA", stroke=ink, lw=lw, closed=True)
            pg.poly(P([(4.6, 0.4), (8.6, 0.4), (9.8, 3.6), (5.8, 3.6)]), fill=C["field"], closed=True)
            pg.poly(P([(6.6, 4.6), (9.0, 4.6), (9.8, 8.2), (7.4, 8.2)]), fill=C["field"], closed=True)
    elif kind == "extent":
        pg.poly(P([(0.4, 3.0), (7.4, 0.4), (9.6, 7.0), (2.6, 9.6)]), fill=C["paper"], stroke=ink, lw=lw, closed=True)
        pg.poly(P([(2.4, 3.6), (5.0, 2.6), (5.8, 5.0), (3.2, 6.0)]), fill=C["field"], closed=True)
        O(6.6, 6.4, 1.2, fill=C["orchard"])
    elif kind == "route":                       # a route not drawn yet
        pg.line(P([(0.6, 1.4), (4.0, 4.6), (6.2, 3.6), (9.4, 8.6)]), C["water_deep"], lw, (lw * 2.0, lw * 1.6))
        pg.text("?", x + 7.6 * u, y - sz + 1.0 * u, pt(4.2 * u), acc, True, "C")
    elif kind == "clean":                       # reeds in water
        pg.poly(Q(0, 0, 10, 2.4), fill=C["water"], closed=True)
        for k_ in range(5):
            a = 1.6 + k_ * 1.7; t = 6.4 + (k_ % 2) * 2.4
            pg.line(P([(a, 0.8), (a + 0.3, t)]), C["green_deep"], lw)
            pg.poly(Q(a - 0.25, t - 1.8, a + 0.85, t + 0.2), fill=C["green_mid"], closed=True)
    elif kind == "hold":                        # roots holding the bank
        pg.poly(P([(0, 0.4), (10, 0.4), (10, 6.0), (0, 2.0)]), fill=C["structure"], closed=True)
        for a in (3.0, 6.6):
            b = 2.0 + a * 0.4
            pg.line(P([(a, b), (a, b + 3.2)]), C["green_deep"], lw)
            pg.line(P([(a, b), (a - 1.4, b - 1.6)]), ink, lw * 0.7)
            pg.line(P([(a, b), (a + 1.2, b - 1.8)]), ink, lw * 0.7)
            pg.line(P([(a, b), (a, b - 1.6)]), ink, lw * 0.7)
            O(a, b + 3.6, 1.0, fill=C["green_mid"])
    elif kind == "shade":                       # tree and its shade
        pg.poly(Q(0.6, 0.4, 9.4, 1.4), fill=C["ink2"], closed=True)
        pg.poly(Q(4.5, 1.4, 5.5, 5.2), fill=ink2, closed=True)
        O(5.0, 6.8, 3.0, fill=C["green_deep"])
    elif kind == "scent":                       # flowering shrub and scent lines
        for a in (3.2, 5.0, 6.8):
            pg.line(P([(5.0, 0.4), (a, 5.0)]), C["green_deep"], lw)
            O(a, 5.6, 0.8, fill=acc)
        for a in (2.6, 5.0, 7.4):
            pg.line(P([(a + (0.5 if j % 2 else -0.5), 6.8 + j * 0.8) for j in range(4)]), ink2, lw * 0.7)
    elif kind == "nose":                        # odour, effect not measured
        for k_ in range(3):
            a = 2.0 + k_ * 2.6
            pg.line(P([(a + (0.7 if j % 2 else -0.7), 0.8 + j * 1.6) for j in range(6)]), ink2, lw)
        pg.text("?", x + 8.8 * u, y - sz + 0.6 * u, pt(3.4 * u), acc, True, "C")

def tiles(pg, x, y, w, items, cols=1, s=1.0, fill=None):
    """v1.2 (water board v1.6): facts as tiles: pictogram, keyword heading, the key figure large, short keyword lines and
    the source number. items = [(pictogram, heading, figure or None, [keyword lines], source or None)]. Returns the bottom y."""
    k = 0.3528
    fh, fb, ft = 8.5 * s, 15.0 * s, 7.0 * s
    ic, pad, g = 12.0 * s, 2.2 * s, 2.4 * s
    tw = (w - (cols - 1) * g) / cols
    txw = tw - ic - 3 * pad
    lay = []
    for kind, head, big, lines, ref in items:
        lines = list(lines or [])
        if ref: lines = lines[:-1] + [((lines[-1] + " ") if lines else "") + cite(ref)]
        L3 = (wrap(head, fh, txw, True), wrap(big, fb, txw, True) if big else [], [q for ln in lines for q in wrap(ln, ft, txw)])
        hh = pad * 2 + (len(L3[0]) * fh * 1.25 + len(L3[1]) * fb * 1.15 + len(L3[2]) * ft * 1.3 + (fh * 0.3 if L3[1] else 0)) * k
        lay.append((kind, big, L3, max(hh, ic + 2 * pad)))
    yy = y
    for r0 in range(0, len(lay), cols):
        row = lay[r0:r0 + cols]
        rh = max(t[3] for t in row)
        for c_, (kind, big, L3, _) in enumerate(row):
            tx = x + c_ * (tw + g)
            pg.rect(tx, yy - rh, tw, rh, fill=fill or C["white"], stroke=C["faint"], lw=0.2)
            icon(pg, kind, tx + pad, yy - pad, ic)
            lx, ly = tx + 2 * pad + ic, yy - pad
            for ln in L3[0]:
                ly -= fh * 1.25 * k; pg.text(ln, lx, ly + fh * 0.25 * k, fh, C["ink"], True)
            if L3[1]: ly -= fh * 0.3 * k
            for ln in L3[1]:
                ly -= fb * 1.15 * k
                pg.text(ln, lx, ly + fb * 0.2 * k, fb, C["accent"] if big in FLAGGED else C["green_deep"], True)
            for ln in L3[2]:
                ly -= ft * 1.3 * k; pg.text(ln, lx, ly + ft * 0.3 * k, ft, C["ink"])
        yy -= rh + g
    return yy + g

FLAGGED = ("NOT KNOWN", "not designed")         # big figures that say "no data": in the accent colour

def north(pg, x, y, ang_deg, r=7.0):
    a = math.radians(ang_deg)
    ux, uy = -math.sin(a), math.cos(a)
    px, py = -uy, ux
    tip = (x + ux * r, y + uy * r); bl = (x - ux * r * 0.6 + px * r * 0.45, y - uy * r * 0.6 + py * r * 0.45)
    br = (x - ux * r * 0.6 - px * r * 0.45, y - uy * r * 0.6 - py * r * 0.45)
    pg.poly([tip, bl, (x, y), br], fill=C["ink"], closed=True)
    pg.text("N", tip[0] + ux * 3.0, tip[1] + uy * 3.0 - 1.2, 8, C["ink"], True, "C")

# ------------------------------------------------------------------ page 1: what each cubic metre grows
# v4 (MIRAQUA 28 Oct, F5: public online sources only): the public sources keep their words, the project's own file
# pointers go from the printed key (kept here: NEWS research/water_data/03 §3; TUIK library/research/crops_2026-10-24
# §1.24-1.25; NET_REF research/water_balance/tables/C1). G11: corn, not maize, where printed (data keys stay "maize").
NEWS = "news: Ajans Bakırçay 19.03.2025"
TUIK = "TÜİK Bitkisel Üretim, Bergama 2025"
KAYA = "Kaya et al. 2017, Irrig. Drain. 66(5):820-827, Tables II, III, VI, pp.823-826 (deficit saving: Table II, S0.50 and S0.25 vs control)"
ITB = "İzmir Ticaret Borsası cotton report 2025, p.5"
NET_REF = ("net irrigation: FAO-56 (Allen et al. 1998), MGM/WMO 17742 normals, ERA5 1991-2025 scaled; per ha = FAO-56 "
           "daily soil balance net need (34 water years, Bergama climate) / 0.90 drip (calculated)")
TAGEM = ("check: TAGEM/DSİ 2017 §12 Bergama 17742 station tables (net = ETc - 0.8 rain, our arithmetic): cotton 829 vs our 853 mm, "
         "corn 765 vs 723, tomato 606-825 vs 781, olive 502-603 vs 614")
# v1.2: the context sentences as tiles (pictogram, heading, big figure, keyword lines, source)
# v2 (Aras 27 Oct, Prompt 5): the crops they name as "English (Turkish)"; figures and sources as they were
CONTEXT = [
    ("nowater", "DROUGHT 2025: NO WATER-HUNGRY CROPS", "7,500 ha",
     ["%s, %s, fodder · Bergama villages" % (name_lc("maize"), name_lc("cotton")),
      "no water for second crops · DSİ + Ministry"], NEWS),
    ("cotton", name_caps("cotton") + ": BERGAMA'S BIGGEST CROP", "10,000 ha",
     ["2025 · 37 % of 26,800 ha field crops",
      "%s 6,000 · %s 2,500 · %s 8,700 ha" % (name_lc("maize"), name_lc("tomato"), name_lc("olive"))], TUIK),
    ("olive", name_caps("olive") + " CAN TAKE LESS · MEMECIK, DRIP", "-72 % water",
     ["İzmir station 2008-10 · 175 vs 622 mm a season", "24.9 vs 27.8 kg a tree: no significant loss",
      "highest oil content"], KAYA),
    ("drip", "TODAY'S IRRIGATION ON THE FARMS", None, ["some Bergama growers moved to drip"], ITB),
]
REPLACES = [("cube", "THE WATER BOARD LINE IT REPLACES", "10,000 m³ = 1.22 ha " + name_lc("olive"),   # v3.1: (Zeytin)
             ["was: İzmir crop water use", "now: Bergama climate · rain in the soil · live storage"], None)]
DEFICIT = (1 - 350.0 / 622, 1 - 175.0 / 622)   # olive water saved: S0.50 and S0.25 against the control SC, Kaya et al. 2017 Table II
# Bergama district areas 2025, da (TÜİK MEDAS export, library/research/crops_2026-10-24/bergama_crops_irrigation_v1.md §1.25):
# the share of each crop the water balance models, used for the district mix row
TUIK_2025_DA = dict(cotton=99963, maize=24532 + 35491, tomato=13740 + 11268, olive=65978 + 21068)

COTTON_H = ("h01 §3 'Then vs now', cotton / textiles: \"Tersane cotton (16th c.); ginning 1861; Sümerbank (1954/60–2008)\" "
            "(s18, s106; library/research/selinos_bergama_history_context_v1.md line 111)")
OLIVE_H = ("h01 §2 + §5 P04: \"19th-c. olive-oil machinery in the Red Hall S rotunda\" (s25; "
           "selinos_bergama_history_context_v1.md lines 77, 139)")
# v1.6 (Aras 27 Oct, p24 + spec §3): the farm history behind the farms the water serves, as a timeline, in the
# card's own words and years (h01 §3 line 111, §2 line 77, §5 P04 line 139); today's areas from TÜİK 2025 (above)
HISTORY = [("cotton", "Tersane cotton (16th c.)", 1500, 1600, COTTON_H),
           ("cotton", "ginning 1861", 1861, None, COTTON_H),
           ("cotton", "Sümerbank (1954/60–2008)", 1954, 2008, COTTON_H),
           ("cotton", "2025: %s ha" % fmt(rnd(TUIK_2025_DA["cotton"] / 10.0, 100)), 2025, None, TUIK),
           ("olive", "19th-c. olive-oil machinery · Red Hall S rotunda", 1800, 1900, OLIVE_H),
           ("olive", "2025: %s ha" % fmt(rnd(TUIK_2025_DA["olive"] / 10.0, 100)), 2025, None, TUIK)]


def history_line(pg, x, top, w, floor):
    """a timeline 1500-2030 with the cotton (above) and olive (below) history, labels placed by measured width (no
    overlaps). Left out (and logged) when it does not fit above `floor`. Returns its bottom y or None."""
    if top - 35.0 < floor:
        LOG_NOTES.append("p1 history timeline left out: no room above the 'what it replaces' tile")
        return None
    P = Placer()
    P.text(pg, "WHY THE STORED WATER GOES TO FARMS", x, top, 9, C["accent"], True)
    P.text(pg, "Bergama's %s and %s" % (name_lc("cotton"), name_lc("olive")), x, top - 3.8, 7.5, C["ink"])   # v2
    ya = top - 20.0
    X = lambda yr: x + 2.0 + (w - 4.0) * (yr - 1500) / 530.0
    pg.line([(X(1500), ya), (X(2030), ya)], C["ink"], 0.3)
    for yr in range(1500, 2001, 100):
        pg.line([(X(yr), ya - 0.8), (X(yr), ya + 0.8)], C["ink"], 0.3)
        P.text(pg, str(yr), X(yr) - text_w(str(yr), 7) / 2.0, ya - 3.6, 7, C["ink2"])
    reg = (x, ya - 15.0, x + w, top - 5.5)
    for lane, lab, a, b, ref in HISTORY:
        col, up = (C["accent"], True) if lane == "cotton" else (C["green_deep"], False)
        yb = ya + (1.0 if up else -1.0)
        if b:
            if lab.startswith("Sümerbank"):           # 1954 vs 1960 (card: conflicting dates): dashed until 1960
                pg.line([(X(1954), yb), (X(1960), yb)], col, 1.0, (0.6, 0.4))
                pg.line([(X(1960), yb), (X(2008), yb)], col, 1.0)
            else:
                pg.line([(X(a), yb), (X(b), yb)], col, 1.0)
        else:
            pg.circle(X(a), yb, 0.8, fill=col)
        if P.put(pg, cited(lab, ref), X((a + b) / 2.0 if b else a), yb + (0.6 if up else -0.6), 7, col, False, region=reg,
                 gap=2.0, up=up, lanes=4, lead_col=col, stick=True) is None:
            LOG_NOTES.append("p1 history label left out (no free place): " + lab)
    return ya - 15.0


CROP_ROW = ("olive", "cotton", "maize", "tomato")   # v2 (Aras 27 Oct, Prompt 5): the crops page 1 compares


def crop_row(pg, x, top, w, floor):
    """v2 (Aras 27 Oct, Prompt 5): "THE CROPS": page 1's crops as photos in one row (PHOTO_W x PHOTO_H each, spread
    over w), the name "English (Turkish)" and the photo's credit [n] under each. Left out (and logged) when it would not
    fit above `floor` with two name lines. Returns its bottom y or None."""
    n = len(CROP_ROW)
    gx = (w - n * PHOTO_W) / (n - 1.0)
    if top - 3.0 - PHOTO_H - 2.5 - 2.6 - 0.6 < floor or gx < PH_GAP:
        LOG_NOTES.append("p1 crop photos left out: no room above the 'what it replaces' tile")
        return None
    pg.text("THE CROPS", x, top, 9, C["accent"], True)
    low = top
    for i, key in enumerate(CROP_ROW):
        px = x + i * (PHOTO_W + gx)
        photo_frame(pg, 0, key, px, top - 3.0)
        yy = top - 3.0 - PHOTO_H - 2.5
        for q in name_lines(key, photo_mark(key), 7, PHOTO_W):
            pg.text(q, px, yy, 7, C["ink"], True)
            low = min(low, yy - 0.6); yy -= 2.6
    ag_crop("ag1_crops", 0, x - 1.0, low - 1.0, x + w + 1.0, top + 4.0)
    return low


# ------------------------------------------------------------------ v3 (Prompt 6): the stream comes first
P1_X = 14.0                          # v4 (MIRAQUA 28 Oct, F10): page 1's left column on the 14 mm margin with the title
                                     # (was 26, behind the page number that is gone)
PRIORITY =[(1, "stream: summer strip"), (2, "on-site planting, on the strip's water"), (3, "farms outside the site")]
WE_DO = [(1, "clean once, at the upstream end"), (2, "hold winter water"), (3, "strip first, all summer"),
         (4, "plant each step for the water it gets"), (5, "surplus to the farms outside, never drinking")]


def chip(pg, x, y, n, label, size=7.5):
    """v3: a numbered step: the number white in an accent square, the label after it (baseline y). Returns x after it."""
    pg.rect(x, y - 0.7, 3.6, 3.6, fill=C["accent"])
    pg.text(str(n), x + 1.8, y + 0.15, 7, C["white"], True, "C")   # v3.1: 7 pt, the smallest size (was 6.5)
    pg.text(label, x + 4.8, y, size, C["ink"])
    return x + 4.8 + text_w(label, size)


def step_arrow(pg, x, y):
    """v3: a small arrow, 4 mm long, at the mid-height of a label on baseline y. Returns x after it."""
    ym = y + 1.1
    pg.line([(x, ym), (x + 3.0, ym)], C["ink2"], 0.3)
    pg.poly([(x + 2.9, ym + 0.8), (x + 4.0, ym), (x + 2.9, ym - 0.8)], fill=C["ink2"], closed=True)
    return x + 4.0


def chips(pg, x, y, steps, size=7.5):
    """v3: numbered steps in one row, an arrow between two, from x on baseline y"""
    for i, (n, lab) in enumerate(steps):
        if i: x = step_arrow(pg, x + 1.5, y) + 1.5
        x = chip(pg, x, y, n, lab, size)
    return x


def chips_w(steps, size=7.5):
    return sum(4.8 + text_w(lab, size) for _, lab in steps) + 7.0 * (len(steps) - 1)


def squeeze(ys):
    """v3: the double squeeze, dry year against normal, from the water balance's year_split (one daily run of the
    design store): water left for the farms after the strip (carried in + filled - strip), the farms' need per hectare
    (the same fields both years, so their need) and the hectares that water serves = left / need per ha. Fractions."""
    n, d = ys["normal"], ys["dry5"]
    left = lambda q: q["carried_in_m3"] + q["filled_m3"] - q["strip_m3"]
    a = left(d) / max(left(n), 1.0) - 1.0
    b = d["farm_need_m3"] / max(n["farm_need_m3"], 1.0) - 1.0
    return a, b, (1.0 + a) / (1.0 + b) - 1.0


def pc(v):
    """v3: a change as a signed whole percent, "+11 %", "-2 %", "0 %" """
    return "0 %" if abs(v) < 0.005 else "%+.0f %%" % (100.0 * v)


def stream_first(pg, L, src, y_top):
    """v3 (Aras 27 Oct 17:35, Prompt 6 task 1: "the board sends LESS water to farms in a 1-in-5 dry year than storage
    holds ... show the defence ON the board"): the priority as numbered steps; the design store through a normal and the
    1-in-5 dry water year, two stacked bars on one scale from x 70 (the hectare bars' origin): strip (it also waters the
    bed planting: the model has no draw of its own for it), farms (light normal, deep dry, as the bars below), left over
    (carried on, or back to the stream after 365 days), the store size dashed across both; then the double squeeze.
    All from the water balance results (design.year_split); without them only the priority row. Returns the bottom y."""
    yA = y_top - 3.5
    pg.text("THE STREAM COMES FIRST", P1_X, yA, 9, C["accent"], True)
    chips(pg, P1_X + text_w("THE STREAM COMES FIRST", 9, True) + 5.0, yA, PRIORITY)
    ys = L.get("year_split")
    if not (ys and "normal" in ys and "dry5" in ys):
        LOG_NOTES.append("FLAG p1: the water balance results have no year_split (water balance v4 has not run): the "
                         "normal and dry-year bars and the squeeze line are left out")
        ag_crop("ag1_stream", 0, P1_X - 2.0, yA - 2.0, 266.0, y_top + 1.0)
        return yA - 1.0
    mix = L.get("design_mix") or "design mix"
    mix_t = " + ".join(name_lc(w.split()[-1]) if w.split() and w.split()[-1] in PLANTS else w for w in mix.split(" + "))
    SRC_Y = ("normal and 1-in-5 dry year: " + src + "; design store, " + mix_t + "; one daily run of the store over 34 "
             "water years: normal = the year of median farm need, dry = the 1-in-5 dry year of farm need; carried in + "
             "filled = strip + farms + left over; left for farms = carried in + filled - strip; hectares = left for farms "
             "/ need per hectare (calculated)")
    mk = cite(SRC_Y)
    V = float(ys.get("storage_m3") or 0.0)
    YRS = (("normal", "normal year", C["green_light"], C["ink"]), ("dry5", "1-in-5 dry year", C["green_deep"], C["white"]))
    tot = dict((k, ys[k]["carried_in_m3"] + ys[k]["filled_m3"]) for k, _, _, _ in YRS)
    x0, BW = 70.0, 140.0
    kx = BW / max(max(tot.values()), V, 1.0)
    v_t = lambda v: fmt(rnd(v, 1000 if v >= 10000 else 100))
    b1 = yA - 7.0                                  # the normal bar's top; the dry bar 11 mm under it
    for j, (k, lab, fcol, fink) in enumerate(YRS):
        d = ys[k]
        top = b1 - 11.0 * j; bot = top - 6.0
        segs = [(d["strip_m3"], C["water_deep"], C["white"]), (d["farms_m3"], fcol, fink),
                (max(0.0, tot[k] - d["strip_m3"] - d["farms_m3"]), C["faint"], C["ink"])]
        xs, out_x = x0, -1e9                       # out_x: where the last outside value ended (pushed right past it)
        for v, col, ink in segs:
            w_ = kx * v
            if w_ > 0.05:
                pg.rect(xs, bot, w_, 6.0, fill=col)
            t = v_t(v)
            if v >= 0.5:                           # v3.1: the block's small words 7 pt, the smallest size (were 6.5)
                tw_ = text_w(t, 7, True)
                if tw_ + 1.6 <= w_:                # inside, centred
                    pg.text(t, xs + w_ / 2.0, bot + 2.2, 7, ink, True, "C")
                else:                              # outside: over the normal bar, under the dry bar
                    tx = max(xs + w_ / 2.0 - tw_ / 2.0, out_x + 1.5)
                    pg.text(t, tx, top + 0.9 if j == 0 else bot - 2.9, 7, C["ink"], True)
                    out_x = tx + tw_
            xs += w_
        pg.text(lab, x0 - 3.0, top - 2.6, 8, C["ink"], True, "R")
        pg.text("water year " + d["water_year"], x0 - 3.0, bot + 0.6, 7, C["ink2"], align="R")
        pg.text("%s m³ through the store" % v_t(tot[k]), x0 + BW + 4.0, top - 2.4, 7.5, C["ink"], True)
        pg.text("stream's winter flow: %.0f %% of a median year" % d["winter_flow_pct_of_median"], x0 + BW + 4.0,
                bot + 0.6, 7, C["ink2"])
    if V > 0:                                      # the store size, dashed across both bars
        xv = x0 + kx * V
        pg.line([(xv, b1 - 17.8), (xv, b1 + 0.8)], C["ink"], 0.35, (1.0, 0.7))
    lg = b1 - 17.0 - 7.0                           # the legend row, then the squeeze in two lines
    xx = P1_X
    for kind, cols, lab in (("fill", (C["water_deep"],), "strip, also waters the bed planting"),
                            ("fill", (C["green_light"], C["green_deep"]), "farms: normal · dry year"),
                            ("fill", (C["faint"],), "left: carried on, or back to the stream after a year"),
                            ("dash", (C["ink"],), "store %s m³ %s" % (fmt(V), mk))):
        for c_ in cols:
            if kind == "fill":
                pg.rect(xx, lg - 0.3, 3.5, 2.6, fill=c_); xx += 4.0
            else:
                pg.line([(xx + 1.7, lg - 0.6), (xx + 1.7, lg + 2.6)], c_, 0.35, (1.0, 0.7)); xx += 4.0
        pg.text(lab, xx + 0.8, lg, 7, C["ink"])           # v3.1: 7 pt (was 6.5)
        xx += 0.8 + text_w(lab, 7) + 5.0
    a, b, c = squeeze(ys)
    pg.text("1-in-5 dry year vs normal year: left for farms after the strip %s · need per hectare %s · hectares %s %s" % (
        pc(a), pc(b), pc(c), mk), P1_X, lg - 4.0, 7.5, C["accent"], True)
    if b > 0.0 and a <= 0.0:                       # what the run shows, said as it is (the log flags the other cases)
        t2 = "so the hectares fall faster than the volume: why deficit-irrigated %s is the lever" % name_lc("olive")
    elif b > 0.0 and c < 0.0:
        t2 = "the need per hectare outgrows the water left: why deficit-irrigated %s is the lever" % name_lc("olive")
    else:
        t2 = "the hectares hold in this dry year: the store covers it"
    pg.text(t2, P1_X, lg - 7.4, 7.5, C["ink"])
    if a > 0.0 or b <= 0.0:
        LOG_NOTES.append("MODEL p1: the dry year (%s) leaves the farms %s water after the strip and needs %s per hectare: "
                         "the squeeze is %s" % (ys["dry5"]["water_year"], pc(a), pc(b),
                                                "the need per hectare only" if b > 0.0 else "not there this time"))
    n_, d_ = ys["normal"], ys["dry5"]
    LOG_NOTES.append("p1 stream first (%s, store %s m3): normal %s / dry %s: in %s / %s m3 (filled %s / %s), strip %s / %s, "
                     "farms %s / %s of need %s / %s; left for farms %s, need per ha %s, hectares %s; winter flow %.0f / %.0f %% "
                     "of median" % (mix, fmt(V), n_["water_year"], d_["water_year"], fmt(tot["normal"]), fmt(tot["dry5"]),
                                    fmt(n_["filled_m3"]), fmt(d_["filled_m3"]), fmt(n_["strip_m3"]), fmt(d_["strip_m3"]),
                                    fmt(n_["farms_m3"]), fmt(d_["farms_m3"]), fmt(n_["farm_need_m3"]),
                                    fmt(d_["farm_need_m3"]), pc(a), pc(b), pc(c), n_["winter_flow_pct_of_median"],
                                    d_["winter_flow_pct_of_median"]))
    ag_crop("ag1_stream", 0, P1_X - 2.0, lg - 9.0, 266.0, y_top + 1.0)
    return lg - 8.2


def page_cubic(L, src):
    pg = Page(420, 297)
    header(pg, "WHAT EACH CUBIC METRE GROWS",
           "Same storage, different crops: hectares irrigated a season", tag=STAGE_TAG)
    s_lo, s_hi = span(L["storage_m3"]); p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0          # m3 the storage gives the farms in the 1-in-5 dry year
    fed = L["cropland_ha"] + L["orchard_ha"]
    SRC1 = "storage, need and share: " + src + "; water to farms = 1-in-5 dry-year need x share covered (calculated)"
    MIX = ("Bergama mix = cotton, corn and tomato weighted by their 2025 district areas; no map shows what the 34.9 ha grow, "
           "so the mix stands in; water balance crops: %s" % (", ".join(crop_word(c) for c in L["crops"]) or "not set"))
    # key line (v4, F10: on the 14 mm margin with the title, was 26)
    pg.text("%s-%s m³" % (fmt(rnd(s_lo)), fmt(rnd(s_hi))) if rnd(s_lo) != rnd(s_hi) else "%s m³" % fmt(rnd(s_lo)), P1_X, 250, 26, C["water_deep"], True)
    pg.text("storage · cost cut-off " + cite(SRC1), P1_X, 242, 9, C["ink"])
    pg.text("%s-%s m³" % (fmt(rnd(w_lo)), fmt(rnd(w_hi))), 120, 250, 26, C["green_deep"], True)
    pg.text("to farms · 1-in-5 dry year · %s %% of need · strip first" % (("%.0f" % p_lo) if "%.0f" % p_lo == "%.0f" % p_hi else "%.0f-%.0f" % (p_lo, p_hi)), 120, 242, 9, C["ink"])
    # bars: hectares served by W, per crop (v2, Prompt 5: the crop names "English (Turkish)")
    rows = [(plant_name("olive") + ", full irrigation", "olive", None), (plant_name("olive") + ", deficit irrigation", "olive", DEFICIT)] + \
           [(plant_name(c) if c in PLANTS else c.capitalize(), c, None) for c in sorted(NET) if c != "olive"] + [("Bergama mix (TÜİK 2025)", "mix", None)]
    stream_first(pg, L, src, 236.0)                 # v3 (Prompt 6): between the headline and the bars
    x0, y0, gw = 70, 181, 190                       # v3: y0 was 214, the stream-first block sits above
    RP = 16.5                                       # v3: rows 16.5 mm apart (were 19.5)
    yb_ = y0 - (len(rows) - 1) * RP - 13.5           # the last row's dry bar bottom (= the grid's foot, as before)
    vals = []
    for lab, crop, d in rows:
        for yr in ("normal", "dry"):
            g = gross_m3_ha(crop, yr)
            if d: lo, hi = w_lo / (g * (1 - d[0])), w_hi / (g * (1 - d[1]))
            else: lo, hi = w_lo / g, w_hi / g
            vals.append((lab, crop, yr, g, lo, hi, d))
    vmax = max(v[5] for v in vals) * 1.08
    step = 25 if vmax < 160 else (50 if vmax < 400 else 100)
    for t in range(0, int(vmax) + 1, step):
        xx = x0 + gw * t / vmax
        pg.line([(xx, yb_), (xx, y0 + 6)], C["faint"], 0.2)
        pg.text("%d ha" % t, xx, yb_ - 4.5, 7, C["ink2"], align="C")
    xf = x0 + gw * fed / vmax
    pg.line([(xf, yb_), (xf, y0 + 9)], C["accent"], 0.5, (1.5, 1.0))
    pg.text("farms we feed: %s ha" % fmt1(fed), xf + 1.2, y0 + 7.5, 7.5, C["accent"], True)
    for i, (lab, crop, d) in enumerate(rows):
        yy = y0 - i * RP
        pg.text(lab, x0 - 3, yy - 4.5, 10, C["ink"], True, "R")
        if crop in TUIK_2025_DA:
            pg.text("Bergama 2025: %s ha %s" % (fmt(TUIK_2025_DA[crop] / 10.0), cite(TUIK)), x0 - 3, yy - 13.6, 7, C["accent"], align="R")
        for j, yr in enumerate(("normal", "dry")):
            v = [q for q in vals if q[0] == lab and q[2] == yr][0]
            by = yy - j * 7.5
            col = C["green_light"] if yr == "normal" else C["green_deep"]
            pg.rect(x0, by - 6, gw * v[4] / vmax, 6, fill=col)
            if v[5] > v[4] * 1.01:
                pg.rect(x0 + gw * v[4] / vmax, by - 6, gw * (v[5] - v[4]) / vmax, 6, fill=None, stroke=col, lw=0.35)
            t = "%s-%s ha" % (fmt(v[4]), fmt(v[5])) if fmt(v[4]) != fmt(v[5]) else "%s ha" % fmt(v[4])
            pg.text(t, x0 + gw * v[5] / vmax + 2, by - 4.4, 8, C["ink"], True)
        g_n, g_d = gross_m3_ha(crop, "normal"), gross_m3_ha(crop, "dry")
        if d: g_n, g_d = g_n * (1 - d[1]), g_d * (1 - d[0])
        mk = cite(NET_REF) + (cite(TAGEM) if i == 0 else "") + (cite(KAYA) if d else "") + (cite(MIX) if crop == "mix" else "")
        pg.text("%s-%s m³ per ha a season %s" % (fmt(rnd(min(g_n, g_d), 10)), fmt(rnd(max(g_n, g_d), 10)), mk), x0 - 3, yy - 10, 7, C["ink2"], align="R")
    ag_crop("ag1_bars", 0, 13.0, yb_ - 5.5, 277.0, y0 + 11.0,
            legend=[{"kind": "fill", "colour": C["green_light"], "label": "normal year"},
                    {"kind": "fill", "colour": C["green_deep"], "label": "1-in-5 dry year"},
                    {"kind": "line", "colour": C["accent"], "label": "farms we feed"}])
    ag_crop("ag1_headline", 0, P1_X - 2.0, 239.0, 262.0, 261.0)
    # key to the two bars
    ky = yb_ - 10.0
    pg.rect(x0, ky, 6, 3, fill=C["green_light"]); pg.text("normal year (mean of 34)", x0 + 8, ky + 0.5, 7, C["ink"])
    pg.rect(x0 + 52, ky, 6, 3, fill=C["green_deep"]); pg.text("1-in-5 dry year", x0 + 60, ky + 0.5, 7, C["ink"])
    pg.rect(x0 + 92, ky, 6, 3, stroke=C["green_deep"], lw=0.35); pg.text("open bar: range (storage span; deficit 44-72 % saving)", x0 + 100, ky + 0.5, 7, C["ink"])
    # reading
    best = [q for q in vals if q[1] == "olive" and q[6] and q[2] == "dry"][0]     # v2: olive with deficit (not by its label)
    worst = max((q for q in vals if q[1] not in ("olive", "mix") and q[2] == "dry"), key=lambda q: q[3])     # the thirstiest field crop
    pg.rect(14, 14, 250, 59, stroke=C["faint"], lw=0.3)       # v1.6: white page, the box only outlined (v3: 14-73)
    pg.text("THE READING", 20, 65, 10, C["accent"], True)    # v3: the reading 19 mm lower (was 32-92), as the bars
    # v1.2: the conclusion as the two dry-year bars (same scale) and the big ratio between them
    bmax, bx0, bw = best[5] * 1.05, 20, 150
    for k_, (q, lab) in enumerate(((worst, "%s, 1-in-5 dry year" % (plant_name(worst[1]) if worst[1] in PLANTS else worst[1].capitalize())),
                                   (best, best[0] + ", 1-in-5 dry year"))):         # v2: names "English (Turkish)"
        yb = 51 - k_ * 18
        pg.text(lab, bx0, yb + 1.5, 8, C["ink"], True)
        pg.rect(bx0, yb - 7, bw * q[4] / bmax, 7, fill=C["green_deep"])
        if q[5] > q[4] * 1.01:
            pg.rect(bx0 + bw * q[4] / bmax, yb - 7, bw * (q[5] - q[4]) / bmax, 7, fill=None, stroke=C["green_deep"], lw=0.35)
        pg.text("%s-%s ha" % (fmt(q[4]), fmt(q[5])), bx0 + bw * q[5] / bmax + 2, yb - 5.2, 9, C["ink"], True)
    bkx = 192
    pg.line([(bkx - 2, 47.5), (bkx, 47.5), (bkx, 29.5), (bkx - 2, 29.5)], C["accent"], 0.5)
    pg.text("%.1f-%.1f x" % (best[4] / worst[4], best[5] / worst[5]), bkx + 3, 36, 24, C["accent"], True)
    pg.text("as much land, same storage", bkx + 3, 30.5, 7.5, C["ink"])
    pg.text("lever: crop + irrigation method, more than storage", 20, 21, 8, C["ink"], True)
    pg.text("same water: more farmland · same farms: less storage", 20, 17, 8, C["ink"])
    ag_crop("ag1_reading", 0, 18.0, 14.5, 262.0, 62.0)
    # context column
    cx, cy = 280, 250
    pg.text("WHY CROP CHOICE IS THE LEVER", cx, cy, 11, C["ink"], True)
    yb_ = tiles(pg, cx, cy - 6, 126, CONTEXT)
    ag_crop("ag1_context", 0, cx - 1.0, yb_ - 1.0, cx + 127.0, cy - 5.0)
    hb = history_line(pg, cx, yb_ - 7.0, 126.0, 64.0)          # v1.6: why the stored water goes to farms
    if hb:
        ag_crop("ag1_history", 0, cx - 1.0, hb - 1.0, cx + 127.0, yb_ - 3.0)
    crop_row(pg, cx, (hb or yb_) - 7.0, 126.0, 64.0)           # v2 (Prompt 5): the crops as photos, above "what it replaces"
    pg.text("WHAT IT REPLACES", cx, 60, 9, C["accent"], True)
    yb_ = tiles(pg, cx, 57, 126, REPLACES)
    ag_crop("ag1_replaces", 0, cx - 1.0, yb_ - 1.0, cx + 127.0, 58.0)
    return pg

# ------------------------------------------------------------------ page 2: the farms we feed, on the site board's plan 01
# v1.5 (Aras 26 Oct 07:06, deck p.33): "build this map from the 'What is there' plan (p.02): same base, same palette and
# legend". The base is the site board's own plan 01, cut from its sheet PDF and scaled by one factor (never redrawn,
# never stretched; Aras 25 Oct 22:07); this page draws only the farms layer on it. The board (v42+) writes the plan's
# georeference into output/selinus_board/booklet/blocks.json. Without it (or without PyMuPDF) the page falls back to
# v1.4's land cover drawing in the same window, flagged on the page and in the log.
CLS = [("farmland", "Fields (cropland)", C["field"]), ("orchard", "Orchards", C["orchard"]),
       ("trees", "Tree cover", C["tree"]), ("shrub", "Shrubland", C["shrub"]), ("grass", "Grassland", C["grass"])]
BOARD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "Bergama", "output", "selinus_board")
ROUND_DENS = (5000, 10000, 20000, 25000, 50000)    # Aras 26 Oct 06:35: round scales only, the largest that fits
FARM_WIN = (13.0, 20.0, 373.0, 262.0)              # the map window, page mm (x0, y0, x1, y1), y up
FARM_COL = 377.0                                   # the key column, x from here to 406
BASE = {}                                          # the plan 01 cut put under page 2 after write_pdf (put_base)
BASE_OFF = [False]                                 # True: draw the fallback (the base could not be placed)


def plan01_geo():
    """(plan dict, note) of the site board's plan 01: its sheet PDF, crop rect (mm from the sheet's top-left) and the
    survey -> sheet similarity a * w + b (complex, sheet mm with y up, from the four frame corners); (None, why) when
    it is missing."""
    if BASE_OFF[0]:
        return None, "the site board's plan could not be placed under the farms (see the log)"
    try:
        import fitz                                 # PyMuPDF (the "# r:" line at the top installs it in Rhino 8)
    except Exception:
        return None, "PyMuPDF missing: Rhino installs it from the '# r: pymupdf' line on the first run (needs internet)"
    try:
        with open(bg_first([os.path.join(bg_booklet("selinus_board"), "blocks.json"),        # board v44+
                            os.path.join(BOARD_DIR, "booklet", "blocks.json")]), encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return None, "site board output not found (cached/booklet/selinus_board/blocks.json): run the site board first"
    blk = next((v for k, v in sorted(d.get("blocks", {}).items()) if k.lower().endswith("_plan01") and v.get("geo")), None)
    if not blk:
        return None, "the site board output has no plan 01 georeference: run the site board v42 or later"
    nm, pdf = os.path.basename(blk.get("pdf", "")), None
    for dd, _, names in sorted(os.walk(BOARD_DIR)):
        if nm in names:
            pdf = os.path.join(dd, nm)
            break
    if not pdf:
        return None, "the site board sheet %s is not in %s" % (nm, BOARD_DIR)
    r = [float(v) for v in blk["rect_mm"]]
    W = [complex(g[0], g[1]) for g in blk["geo"]["points"]]
    Z = [complex(r[0] + g[2], -(r[1] + g[3])) for g in blk["geo"]["points"]]
    wm, zm = sum(W) / len(W), sum(Z) / len(Z)
    a = sum((z - zm) * (w - wm).conjugate() for w, z in zip(W, Z)) / sum(abs(w - wm) ** 2 for w in W)
    err = max(abs(a * (w - wm) + zm - z) for w, z in zip(W, Z))
    return (dict(pdf=pdf, page=int(blk.get("page", 0)), rect=r, a=a, b=zm - a * wm, err=err, legend=blk.get("legend") or []),
            "site board plan 01 of " + time.strftime("%d %b %H:%M", time.localtime(os.path.getmtime(pdf))))


def key_sample(pg, kind, col, x, y):
    """a legend sample 4 x 2.4 mm, its top-left at (x, y): fill, line, dash, dot or outline"""
    if kind == "fill": pg.rect(x, y - 2.4, 4.0, 2.4, fill=col)
    elif kind == "dot": pg.circle(x + 2.0, y - 1.2, 0.8, fill=col)
    elif kind == "dash": pg.line([(x, y - 1.2), (x + 4.0, y - 1.2)], col, 0.4, (1.0, 0.6))
    elif kind == "outline": pg.rect(x + 0.2, y - 2.2, 3.6, 2.0, stroke=col, lw=0.35)
    elif kind == "outline2": pg.rect(x + 0.3, y - 2.1, 3.4, 1.8, stroke=col, lw=0.7)
    else: pg.line([(x, y - 1.2), (x + 4.0, y - 1.2)], col, 0.5)


def page_farms(L, src):
    pg = Page(420, 297)
    BASE.clear()
    G, gnote = plan01_geo()
    fed = [(key, poly) for key in ("farmland", "orchard") for side in ("out", "in") for poly in GEO["lc"][key][side]]
    F = GEO["frame"]
    rotu = G["a"] / abs(G["a"]) if G else complex(math.cos(-math.atan2(F[1][1] - F[0][1], F[1][0] - F[0][0])),
                                                  math.sin(-math.atan2(F[1][1] - F[0][1], F[1][0] - F[0][0])))
    Q = [complex(p[0], p[1]) * rotu for _, poly in fed for ring in poly for p in ring]   # the plan's own turn
    bx0, bx1 = min(q.real for q in Q), max(q.real for q in Q)
    by0, by1 = min(q.imag for q in Q), max(q.imag for q in Q)
    wx0, wy0, wx1, wy1 = FARM_WIN
    den = next((d_ for d_ in ROUND_DENS if (bx1 - bx0) * 1000.0 / d_ + 4.0 <= wx1 - wx0 and
                (by1 - by0) * 1000.0 / d_ + 4.0 <= wy1 - wy0), ROUND_DENS[-1])
    m = 1000.0 / den                              # page mm per metre
    c = rotu * m
    t = complex((wx0 + wx1) / 2.0, (wy0 + wy1) / 2.0) - complex((bx0 + bx1) / 2.0, (by0 + by1) / 2.0) * m

    def T(p):
        z = complex(p[0], p[1]) * c + t
        return (z.real, z.imag)
    hole = (wx0, wy0, wx1, wy1)
    if G:                                          # the window on the board's sheet, cut to plan 01's own crop
        kk = abs(G["a"]) / m

        def S(x, y):
            z = kk * (complex(x, y) - t) + G["b"]
            return z.real, -z.imag
        (sx0, sy1), (sx1, sy0) = S(wx0, wy0), S(wx1, wy1)
        r = G["rect"]
        cx0, cy0, cx1, cy1 = max(sx0, r[0]), max(sy0, r[1]), min(sx1, r[2]), min(sy1, r[3])
        if cx1 - cx0 > 20.0 * kk and cy1 - cy0 > 20.0 * kk:
            hole = (wx0 + (cx0 - sx0) / kk, wy0 + (sy1 - cy1) / kk, wx1 - (sx1 - cx1) / kk, wy1 - (cy0 - sy0) / kk)
            BASE.update(pdf=G["pdf"], page=G["page"], clip=(cx0, cy0, cx1, cy1), rect=hole, err=G["err"], den=den)
        else:
            G, gnote = None, "the farms lie outside the site board's plan 01"
    BASE["note"] = gnote
    header(pg, "THE FARMS WE FEED", "Fields and orchards the stored water serves, on the site plan \"What is there\"",
           hole=hole if G else None)
    WC = "ESA WorldCover 2021 v200, 10 m (CC BY 4.0)"                # v4 (F5): read from Data/landcover
    NEED2 = "need: FAO-56 soil balance / 0.90 drip, normal and 1-in-5 dry years"
    SRC2 = "farm areas from " + src
    # v4 (MIRAQUA 28 Oct, F5): no [n] for what is not public online: the orchards (course survey symbols
    # SEMBOL_ZEYTINLIK / SEMBOL_MEYVA_BAH), the extent (around2.pdf registered to the survey) and the base (the site
    # board's own plan 01, cut and scaled, not redrawn) are said on the page without a mark
    # context line (review global rule 4): what it shows, why it is here, what to take from it; v4: 0.7 mm lower, under
    # the subtitle's new baseline (header)
    pg.text(cited("The site plan \"What is there\" with the fields and orchards our stored water serves outlined: the "
                  "farms read off the same base, colours and key as the site", None if G else WC),
            14, 264.8, 8.5, C["ink"])
    hx0, hy0, hx1, hy1 = hole
    if not G:                                      # fallback: v1.4's land cover drawing in the window, flagged
        A = GEO["around2"]
        pg.rect(wx0, wy0, wx1 - wx0, wy1 - wy0, fill=C["paper"])
        pg.path([[T(p) for p in A]], fill="E8E5DA")
        pg.path([[T(p) for p in GEO["frame"]]], fill="E8E5DA")
        for side in ("out", "in"):
            for key, lab, col in CLS[::-1]:
                for poly in GEO["lc"][key][side]:
                    pg.path([[T(p) for p in r] for r in poly], fill=col if (side == "out" or key in ("farmland", "orchard")) else "D9D6C8")
        for ln in GEO["streams"]: pg.line([T(p) for p in ln], C["water"], 0.5)
        for ln in GEO["selinos"]: pg.line([T(p) for p in ln], C["water_deep"], 1.1)
        pg.text("FLAG: " + gnote + " · land cover drawn from WorldCover instead", wx0 + 2, wy0 + 2, 7, C["accent"], True)
    # the farms layer: the extent, the fields and orchards we feed as outlines over the plan's own colours
    pg.poly([T(p) for p in GEO["around2"]], stroke=C["ink"], lw=0.35, closed=True, dash=(2.0, 1.2))
    for key, poly in fed:
        pg.path([[T(p) for p in r] for r in poly], stroke=C["accent"] if key == "farmland" else C["accent_deep"],
                lw=0.35 if key == "farmland" else 0.7)
    pg.rect(hx0, hy0, hx1 - hx0, hy1 - hy0, stroke=C["ink"], lw=0.25)
    # key column: north, scale, the farms layer with its figures, then plan 01's own key
    x, y = FARM_COL, 262.0
    north(pg, x + 6.0, y - 9.0, math.degrees(math.atan2(rotu.imag, rotu.real)), 5.0)
    bar = max(v for v in (50, 100, 200, 250, 500, 1000) if v * m <= 27.0)
    pg.rect(x, y - 21.0, bar * m / 2.0, 1.2, fill=C["ink"])
    pg.rect(x + bar * m / 2.0, y - 21.0, bar * m / 2.0, 1.2, stroke=C["ink"], lw=0.25)
    pg.text("0", x, y - 24.0, 6, C["ink"], align="C")
    pg.text("%d m" % bar, x + bar * m, y - 24.0, 6, C["ink"], align="R")
    pg.text("1:{:,} at A3".format(den), x, y - 27.5, 6.5, C["ink"], True)
    y -= 34.0
    fed_c, fed_o = L["cropland_ha"], L["orchard_ha"]
    o_lo = min(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    o_hi = max(gross_m3_ha("olive", "dry"), gross_m3_ha("olive", "normal"))
    cc = [c_ for c_ in L["crops"] if c_ in NET] or [c_ for c_ in NET if c_ != "olive"]
    c_lo = min(gross_m3_ha(c_, y_) for c_ in cc for y_ in ("normal", "dry"))
    c_hi = max(gross_m3_ha(c_, y_) for c_ in cc for y_ in ("normal", "dry"))
    f_in, f_out = GEO["area_ha"]["farmland"][1], GEO["area_ha"]["farmland"][0]
    pg.text("WE FEED", x, y, 8, C["accent"], True)
    y -= 3.0
    rows = [("outline", C["accent"], "fields " + cite(SRC2), "%s ha" % fmt1(fed_c),
             ["%s-%s m³ a season %s" % (fmt(rnd(fed_c * c_lo)), fmt(rnd(fed_c * c_hi)), cite(NEED2)),
              "as " + " / ".join(crop_word(c_) for c_ in cc) + " " + cite(TUIK),   # v4 (G11): corn, not maize
              "inside the site %s ha · outside %s ha %s" % (fmt1(f_in), fmt1(f_out), cite(WC))]),
            ("outline2", C["accent_deep"], "orchards", "%s ha" % fmt1(fed_o),             # v4 (F5): survey, no mark
             ["%s-%s m³ a season" % (fmt(rnd(fed_o * o_lo, 100)), fmt(rnd(fed_o * o_hi, 100))), "as olive"]),
            ("dash", C["ink"], "the extent they lie in", "%s ha" % fmt(L.get("extent_ha", 455.0)), [])]
    for kind, col, lab, big, lines in rows:
        key_sample(pg, kind, col, x, y)
        pg.text(lab, x + 5.5, y - 2.1, 6.5, C["ink"], True)
        y -= 7.0
        pg.text(big, x, y, 12, C["green_deep"], True)
        y -= 3.4
        for ln in lines:
            y = pg.para(ln, x, y, 29.0, 6, C["ink2"], lead=1.2)
        y -= 2.0
    pg.line([(x, y + 0.5), (406.0, y + 0.5)], C["faint"], 0.3)
    y -= 4.0
    if G:
        pg.text("THE SITE PLAN'S KEY", x, y, 7, C["ink"], True)
        y -= 2.5
        for it in G["legend"]:
            key_sample(pg, it.get("kind", "fill"), it.get("colour", "B0AC9C"), x, y)
            y = min(pg.para(it.get("label", ""), x + 5.5, y - 2.0, 23.5, 5.5, C["ink"], lead=1.15) + 0.3, y - 3.4)
    else:
        for key, lab, col in CLS:
            key_sample(pg, "fill", col, x, y)
            pg.text(lab, x + 5.5, y - 2.0, 5.5, C["ink"]); y -= 3.6
    ag_crop("ag2_plan", 1, 13.0, min(y, wy0) - 1.0, 407.0, 267.6, den)   # v4: under the subtitle (269.5 now)
    return pg


def put_base(path):
    """v1.5: the site board's plan 01 under page 2's farms layer, as the booklet places sheets (PyMuPDF
    show_pdf_page): the window cut from its sheet, one scale factor both ways. Returns a log line."""
    if not BASE.get("pdf"):
        return "farms map: FLAG fallback drawing, " + BASE.get("note", "")
    import fitz
    K = 72 / 25.4
    hx0, hy0, hx1, hy1 = BASE["rect"]
    cx0, cy0, cx1, cy1 = BASE["clip"]
    doc, src = fitz.open(path), fitz.open(BASE["pdf"])
    doc[1].show_pdf_page(fitz.Rect(hx0 * K, (297.0 - hy1) * K, hx1 * K, (297.0 - hy0) * K), src, BASE["page"],
                         clip=fitz.Rect(cx0 * K, cy0 * K, cx1 * K, cy1 * K), overlay=False)
    tmp = path + ".tmp"
    doc.save(tmp, garbage=3, deflate=True)
    doc.close(); src.close()
    os.replace(tmp, path)
    return "farms map on %s at 1:{:,} (georeference fit {:.2f} mm)".format(BASE["den"], BASE["err"]) % BASE["note"]

# ------------------------------------------------------------------ page 3: one plant ladder, streambed to field
# zones: interpretation of research/water_data/04 §3 (MITECO bands, 92D0 thickets, USDA NRCS TN-38 zones); depths
# from research/rain_river_levels/README.md "The answers in short" and (Q100/Q500, v1.2) its v1.1 correction of 24 Oct
# (surveyed sections, line 49); today's cover from the satellite corridor bands
# v4 (MIRAQUA 28 Oct, F5): the printed key names the public sources only; the project's own pointers stay here:
# SPECIES research/water_data/04; DEPTH research/rain_river_levels, v1.1 correction of 24 Oct; REUSE quoted in EN-E1;
# HARVEST library/research/crops_2026-10-24/bergama_crops_irrigation_v1.md §4.19
SPECIES = ("species, flood and cleaning evidence: POWO, FEIS, JRC Atlas, Korkusuz et al. 2004, Aydın Temel et al. 2017, "
           "Xie et al. 2021, RHS")
BANDS = "bands = our reading of MITECO, Salinas & Cueto 2009 (92D0), USDA NRCS TN-38"
DEPTH = "depths: DSİ Q100/Q500, calculated on the surveyed sections"
TODAY = "today's cover: ESA WorldCover 2021 by distance from the OSM Selinos centreline"
REUSE = "reuse class B: 2010 communiqué"
# v1.6 (Aras 27 Oct 11:07, p26 "update to match the current project ... how the program changes people's
# interactions"): the programme of option A and its historic roots, each from the project's own record
CHAIN_REF = ("option A water chain: one way, cleaned once upstream in the reed basins, held in the terrace cascade, "
             "summer strip from storage, surplus to existing farmland outside the site (proposal sections v6, "
             "masterplan v23 detail notes)")
PROG = ("MIRAQUA programme and its historic roots: hubs at the Roman bridges K3, K4, K5 (H1) with floodable in-bed "
        "sub-hubs, hidden-stream square at İstiklal Meydanı (H2), tanning reach at K3 (H3), Tabaklar Hamamı at K4 (H4), "
        "Late Antique workshops downstream (H7), plane-tree squares (D8): history decisions D1-D12 / H1-H7, "
        "revision 27 Oct PHASE2_SPEC §3 (cards h01 §5, h02 §5, t02)")
GARDEN = ("card i01: Demeter's Garden (Begüm's page, 25 Oct): Demeter 'the ancient symbol of abundance'; olives; "
          "summer farm-to-table use; winter herbs and greens; seasonal production, education; south-west bank at K5")
KERMES = "h01 §2.8: Kermes first 1937 (s100, s60); 90th edition 29.06-05.07.2026 (s60); in the low-water season"
WB_YEAR = ("water board v1.13, S4 season rows: storage fills (winter), full by end of April (spring), low until the "
           "rains (autumn); reeds gold, seed heads; first-flush cleaning")
HARVEST = "olive harvest month: Kaya et al. 2017, Memecik trees hand-harvested 6 Nov 2008, 10 Nov 2009, 14 Nov 2010"
# v4 (MIRAQUA 28 Oct, F5, Aras 28 Oct 11:38 "remove non-public citations"): these are the project's own record or
# internal research cards (h01, i01, t02, decisions, the spec, Begüm's page, our other sheets), not public online:
# cite() gives them no [n] and they leave the key; their words stay on the page as our own design statement. Facts
# now without a public source (reported): Tersane cotton (16th c.), ginning 1861, Sümerbank (1954/60-2008), the
# 19th-c. olive-oil machinery in the Red Hall S rotunda, Kermes since 1937.
F5_OFF = (COTTON_H, OLIVE_H, CHAIN_REF, PROG, GARDEN, KERMES, WB_YEAR)
JOB_ICON =[("CLEAN", "clean"), ("HOLD", "hold"), ("SHADE", "shade"), ("SCENT", "scent"), ("HARVEST", "olive")]   # v1.2 job pictograms
bergama_data("STEPS")
# v1.6: the bank top as the project has it now (kept here so the Data file stays the v1.5 one): hub squares with plane
# trees at the bridges (spec §3 D8; water board band E) and Demeter's Garden's olives at K5 (card i01; olive "will not
# tolerate waterlogged soils", DATA_REGISTER PL-11)
STEPS[3].update(sub="hub squares at the bridges · Demeter's Garden at K5", job="SHADE + SCENT",
                plant=[("plane", "hub squares: Ottoman squares with plane trees")] + STEPS[3]["plant"] +   # v4: no D8
                      [("olive", "Demeter's Garden (K5): dry top only, no waterlogged soil")])   # v2: PLANTS keys


class Placer:
    """v1.6 (spec §2: no text on another text): every label's box is measured with text_w and kept; a new label takes
    the first free place over its anchor, lane by lane upwards (or downwards), left-, centre- or right-aligned on the
    anchor, inside its region; lifted labels get a hair leader down to the anchor. No free place: the label is left
    out and named in the log (never drawn over another)."""
    def __init__(self):
        self.boxes, self.dropped = [], []

    def free(self, b):
        return all(b[2] <= q[0] or b[0] >= q[2] or b[3] <= q[1] or b[1] >= q[3] for q in self.boxes)

    def box(self, s, x, y, size, bold):
        h = size * 0.3528
        return (x - 0.5, y - 0.28 * h - 0.4, x + text_w(s, size, bold) + 0.5, y + 0.8 * h + 0.4)

    def text(self, pg, s, x, y, size, col, bold=False, halo=None):
        """a fixed label (titles, columns): drawn and blocked"""
        self.boxes.append(self.box(s, x, y, size, bold))
        pg.text(s, x, y, size, col, bold, halo=halo)

    def put(self, pg, s, ax, ay, size, col, bold=False, region=None, gap=1.4, up=True, lanes=9, halo="FFFFFF",
            lead_col=None, stick=False):
        w, lane = text_w(s, size, bold), size * 0.3528 * 1.45
        for k in range(lanes):
            y = ay + (gap + k * lane if up else -gap - size * 0.3528 - k * lane)
            for x in (ax - 0.6, ax - w / 2.0, ax - w + 0.6):
                b = self.box(s, x, y, size, bold)
                if region and (b[0] < region[0] or b[2] > region[2] or b[1] < region[1] or b[3] > region[3]):
                    continue
                if not self.free(b):
                    continue
                end = b[1] + 0.3 if up else b[3] - 0.3
                seg = (ax - 0.25, min(ay, end), ax + 0.25, max(ay, end))
                lead = bool(k) or stick
                if lead and not self.free(seg):
                    continue                           # the leader would cross another label
                self.boxes.append(b)
                if lead:
                    pg.line([(ax, ay), (ax, end)], lead_col or C["ink2"], 0.15)
                    self.boxes.append(seg)
                pg.text(s, x, y, size, col, bold, halo=halo)
                return x, y
        self.dropped.append(s)
        return None


# v1.6: the ladder is drawn three times, one row a season (as the water board's season pages): the same cut, the
# season's water, and what people do on each step, by the proposal sections' sketch engine (p.23 language: hand
# ground, washes, people). A diagram: one size across and up; heights not to scale.
_SK = []
def _tree_rand(x, y):
    """A small repeatable random stream from the tree's position (the same in every Python)."""
    s = [(int(round(x * 100.0)) * 73856093 ^ int(round(y * 100.0)) * 19349663) & 0x7FFFFFFF or 1]

    def nxt():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7FFFFFFF
        return s[0] / 2147483648.0
    return nxt
def sketch_engine():
    if not _SK:
        ns = {"__name__": "pr1_sketches", "_tree_rand": _tree_rand}   # reeds use the trees' random stream
        exec(compile(SKETCH_SRC, "pr1_sketches", "exec"), ns)
        _SK.append(ns)
    return _SK[0]
def xform(items, s, dx, dy):
    """The items scaled by s about the origin, then moved by (dx, dy)."""
    def T(p):
        return (dx + s * p[0], dy + s * p[1])
    out = []
    for it in items:
        k = it[0]
        if k == "poly":
            _, rings, fill, stroke, lw, dash, stripes, alpha = it
            st = (stripes[0], stripes[1] * s, stripes[2] * s) + tuple(stripes[3:]) if stripes else None
            out.append(("poly", [[T(p) for p in r] for r in rings], fill, stroke, lw * s,
                        [d * s for d in dash] if dash else dash, st, alpha))
        elif k == "line":
            _, pts, stroke, lw, dash, cap = it
            out.append(("line", [T(p) for p in pts], stroke, lw * s, [d * s for d in dash] if dash else dash, cap))
        elif k == "circle":
            _, cx, cy, r, fill, stroke, lw = it
            out.append(("circle", dx + s * cx, dy + s * cy, r * s, fill, stroke, lw * s))
        elif k == "text":
            _, t, x, y, size, color, bold, align, mat, halo = it
            out.append(("text", t, dx + s * x, dy + s * y, size * s, color, bold, align, mat, halo))
    return out
bergama_data("SKETCH_SRC")

LAD_W = 200.0                        # sketch units across: 5 steps of 40
LAD_S = LAD_W / 5.0
LAD_X0, LAD_X1 = 106.0, 406.0        # the cut on the page, mm (left of it: the season column)
LAD_F = (LAD_X1 - LAD_X0) / LAD_W    # mm a sketch unit, the same across and up
LAD_GB = 12.0                        # the bottom of the cut ground, sketch units
LAD_GY = (16.0, 21.0, 26.0, 30.0, 33.0)   # ground of each step (bed, lower bank, terrace, bank top, farms)
LAD_Q100, LAD_Q500 = 30.8, 31.6      # over the bank top only at S4 (README v1.1 line 49; K4 only in the survey, before
                                     # the DSİ walls: bank depth research 28 Oct §4.5), under the farms
ROW_H = 50.0                         # mm a season row (v2: was 52; room for the plant photos; the tallest tree, the
                                     # bank top's plane at 41 sketch units, ends 4.5 mm under the row's top)
SUBHUB = (27.0, 36.0)                # the floodable sub-hub in the bed (spec §3 D2/D3/D10), sketch x
HUB = (3 * LAD_S + 2.0, 3 * LAD_S + 17.0)   # the dry hub square on the bank top at the bridges (D2), sketch x
LAD_U = 4.5 / 1.745                  # v4 (MIRAQUA 28 Oct, P19.2): sketch units a metre, up: the sketch engine's own figure
                                     # scale (its 1.745 m figures stood 4.5 units), so the bank top, 14 units over the
                                     # bed, stands 5.4 m (the town reach's walls: 5.0 m) and an adult of 1.75 m
                                     # (common/figures.py) is 4.51 units, 6.8 mm on the page
LAD_SEAT = 0.46                      # m from the feet of the seated figure (fig_polys "sit") to its seat


def _bed(i):
    """the bed's water from STEPS (research/rain_river_levels): 0 = Jul-Sep, 1 = Jan-Apr"""
    return STEPS[0]["water"][i].split(": ", 1)[1]


# the season rows: what the water does (left column) and what people do where (on the cut). acts: (figure pose or
# None, sketch x, sketch y, flip, label, source). Sources: STEPS (water), spec §3 (programme), card i01
# (garden), h01 (Kermes), Kaya 2017 (olive harvest), the water board's season words.
# v4 (MIRAQUA 28 Oct, P19.2): the pose is a common/figures.py pose (stand, walk, watch, sit, touch, wade; was the
# board's four SA_FIGS kinds): the seated one sits on the terrace's sitting step, legs over the edge; the wader stands
# in the summer strip; the gardener crouches over the winter herbs; the picker reaches into the olive tree.
def seasons():
    g0, g1, g2, g3, g4 = LAD_GY
    return [
        dict(key="high", name="HIGH WATER", months="Jan-Apr", mark="winter",
             side=[("bed " + _bed(1) + " deep", DEPTH), ("lower bank under water", None), ("sub-hubs closed", PROG),
                   ("storage fills", WB_YEAR)],
             acts=[("sit", 2 * LAD_S + 1.0, g2, True, "sit at the edge · watch the water", PROG),
                   ("stand", HUB[0] + 4.0, g3, False, "hub square: dry, step-free", PROG),
                   ("watch", HUB[0] + 8.5, g3, True, None, None),
                   (None, sum(SUBHUB) / 2.0, g1 + 1.8, False, "sub-hub under water: closed", PROG)]),
        dict(key="low", name="LOW WATER", months="Jul-Sep", mark="summer",
             side=[("bed " + _bed(0), DEPTH), ("strip 0.30 m all summer (design)", None), ("sub-hubs open", PROG),
                   (STEPS[4]["water"][0], None)],
             acts=[("wade", 19.0, g0 - 2.0, False, "wade the strip", None),   # v4 (MIRAQUA 28 Oct, F13): its label
                   ("walk", 10.5, g0, False, "walk in the bed", PROG),       # is placed first now (was blocked)
                   ("stand", SUBHUB[0] + 3.0, g0 + 0.7, False, "sub-hub open", PROG),
                   (None, 6.0, g0 + 6.0, False, "Kermes (since 1937) in the dry bed", KERMES),
                   ("walk", 2 * LAD_S + 20.0, g2, False, "shade under the trees", None),
                   ("stand", HUB[0] + 4.0, g3, False, "hub square: %s shade" % name_lc("plane"), PROG),   # v3.1: names
                   (None, 3 * LAD_S + 25.0, g3 + 2.0, False, "at K5: Demeter's Garden · café, summer beds", GARDEN),
                   ("walk", 4 * LAD_S + 19.0, g4, False, "fields + %s trees watered from storage" % name_lc("olive"),
                    None)]),
        dict(key="harvest", name=name_caps("olive") + " HARVEST", months="Nov", mark="olive",   # v3.1: (ZEYTİN)
             side=[("%s: hand-picked in Nov" % name_lc("olive"), HARVEST), ("storage low until the rains", WB_YEAR),
                   ("first-flush cleaning", WB_YEAR)],
             acts=[(None, 5.0, g0 + 3.0, False, "%s gold · seed heads" % name_lc("reed"), WB_YEAR),   # the bed's reed
                   ("touch", 3 * LAD_S + 30.0, g3, False, "Demeter's Garden: winter herbs + greens · education", GARDEN),
                   ("watch", 4 * LAD_S + 12.0, g4, False, "%s harvest" % name_lc("olive"), HARVEST),
                   ("walk", 4 * LAD_S + 23.0, g4, True, None, None)])]


def sk_draw(pg, items):
    """sketch-engine page items (already placed with xform) on this script's Page"""
    for it in items:
        if it[0] == "poly":
            _, rings, fill, stroke, lw, dash, _st, alpha = it
            pg.path(rings, fill, stroke, lw, True, dash, alpha)
        elif it[0] == "line":
            _, pts, stroke, lw, dash, _cap = it
            pg.line(pts, stroke, lw, dash)
        elif it[0] == "text":
            _, s, x, y, h, col, bold, align, _m, halo = it
            pg.text(s, x, y, h / 0.3528, col, bool(bold), align or "L", halo)


def ladder_row(sea, mark_xy):
    """One season of the plant ladder in the p.23 sketch language: [(z, order, item)] in sketch units (0..LAD_W
    across). mark_xy: where the season's sun / rain mark goes, sketch units (in the season column). v4: returns
    (items, keep): keep = what its labels keep clear of (sketch units): ground (the cut's surface), lines, boxes,
    soft (the plants), figs (one box or None for each of the season's acts)."""
    E = sketch_engine()
    E["FORM"] = "A"                                   # organic only where the project meets the water
    del E["ZP"][:]
    E["ORDER"][0] = 0
    o, w, gy = (0.0, 0.0), LAD_S, LAD_GY
    g = [(0.0, LAD_GB), (0.0, gy[0])]
    for i in range(1, 5):
        xa = i * w
        if i == 1:                                    # the water's edge: the bank in form A (organic)
            g += E["bank"]((xa - 3.0, gy[0]), (xa + 3.0, gy[1]))
        elif i == 2:                                  # the terrace edge: a sitting step (straight riser)
            g += [(xa - 0.5, gy[1]), (xa + 0.5, gy[2])]
        else:                                         # elsewhere faceted, straight slopes
            g += [(xa - 2.0, gy[i - 1]), (xa + 2.0, gy[i])]
    g += [(LAD_W, gy[4]), (LAD_W, LAD_GB)]
    gs = E["sketch_ground"](o, E["notch"](g, [(13.0, 25.0, gy[0], 2.0)]))   # the summer strip's low-flow channel
    pave = E["SEC_PAVE"]
    E["fill"](o, [(HUB[0], gy[3] - 0.6), (HUB[1], gy[3] - 0.6), (HUB[1], gy[3]), (HUB[0], gy[3])], "paving", pave,
              boundary=False, hand_=False)        # the dry hub square at street level (D2)
    slab = [(SUBHUB[0], gy[0]), (SUBHUB[1], gy[0]), (SUBHUB[1], gy[0] + 0.7), (SUBHUB[0], gy[0] + 0.7)]
    E["fill"](o, slab, "paving", pave, boundary=False, hand_=False)   # the floodable sub-hub in the bed
    if sea["key"] == "high":
        pc = E["under_level"](gs, 0.0, LAD_W, LAD_Q500)   # the design flood's reach (faint, as on p.23)
        if pc:
            E["wash"](o, pc, "flood", E["FLOOD_WASH"], E["FLOOD_ALPHA"])
        E["water_level"](o, gs, 19.0, gy[1] + 1.8, E["W_WIN"], bed_hatch=True)   # winter highs: bed + lower bank
        E["sketch"](o, slab, "paving", E["SKINK"], E["PEN_HAIR"], closed=True, over=0.0, retrace=False,
                    dashed=True, z=E["Z_LINE"])       # the sub-hub under the water
    elif sea["key"] == "low":
        E["water_level"](o, gs, 19.0, gy[0] - 0.8, E["W_EXT"], line=False)       # the summer strip in its channel
    else:
        E["water_level"](o, gs, 19.0, gy[0] - 1.2, E["W_SUM"], line=False)       # autumn: water back in the channel
    # plants by step (graphic sizes): reeds in the bed, rushes and shrubs on the lower bank, trees on the terrace,
    # plane tree + lavender on the bank top, olives and a field crop on the farms
    # v4 (MIRAQUA 28 Oct, G4 / F13): what the row's labels must keep clear of, sketch units: boxes (figures, level
    # marks; never covered), soft (the plants: kept clear when the row has room, see lad_labels) and lines (the cut
    # ground, the site edge, the flood lines, the summer arrow)
    keep = dict(ground=gs, lines=[gs, [(4 * w, gy[3] + 1.5), (4 * w, gy[4] + 11.0)]], boxes=[],
                soft=[(1.5, gy[0], 8.0, gy[0] + 4.2)], figs=[])
    E["reeds"](o, 1.5, 8.0, gy[0] - 0.2, 4.2)
    x_ = w + 4.0
    while x_ < w + 18.0:                              # rushes: short hand tufts
        for d in (-0.5, 0.0, 0.5):
            E["sketch"](o, [(x_, gy[1]), (x_ + d * 0.9, gy[1] + 2.0 - abs(d))], "planting", E["REED"], E["LW_FINE"],
                        over=0.0, amp=0.03, retrace=False, z=E["Z_TREE"])
        x_ += 1.6
    for xs, hs, ws in ((w + 24.0, 5.0, 6.0), (w + 33.0, 4.2, 5.0)):   # shrubs: Tamarix, Salix (domes, washes)
        dome = [(xs + ws / 2.0 * math.cos(math.pi * i / 14.0), gy[1] + hs * math.sin(math.pi * i / 14.0) ** 0.7) for i in range(15)]
        E["wash"](o, dome, "planting", E["SITE_TREE"][1], 0.6, z=E["Z_TREE"])
        E["sketch"](o, dome, "planting", E["SITE_TREE"][2], E["LW_FINE"], closed=True, over=0.0, amp=0.12, retrace=False,
                    z=E["Z_TREE"])
        keep["soft"].append((xs - ws / 2.0, gy[1], xs + ws / 2.0, gy[1] + hs))
    for tx_, ty_, th_ in ((2 * w + 14.0, gy[2], 11.0), (2 * w + 30.0, gy[2], 9.0), (HUB[0] + 7.0, gy[3], 11.0),
                          (3 * w + 34.5, gy[3], 6.0), (4 * w + 6.0, gy[4], 7.0), (4 * w + 15.0, gy[4], 7.0)):
        keep["soft"].append((tx_ - 0.4 * th_, ty_ + 0.3 * th_, tx_ + 0.4 * th_, ty_ + 0.98 * th_))   # the crowns
    keep["soft"].append((4 * w + 26.0, gy[4], LAD_W, gy[4] + 1.6))                                   # the crop rows
    E["sketch_tree"](o, 2 * w + 14.0, gy[2], 11.0)
    E["sketch_tree"](o, 2 * w + 30.0, gy[2], 9.0)
    E["sketch_tree"](o, HUB[0] + 7.0, gy[3], 11.0)   # the hub square's plane tree (D8)
    x_ = 3 * w + 20.0
    while x_ < 3 * w + 31.0:                          # lavender mounds with flower spikes
        mound = [(x_ + 1.2 * math.cos(math.pi * i / 10.0), gy[3] + 1.0 * math.sin(math.pi * i / 10.0)) for i in range(11)]
        E["wash"](o, mound, "planting", E["hx"](C["olive"]), 0.6, z=E["Z_TREE"])
        for d in (-0.5, 0.0, 0.5):
            E["sketch"](o, [(x_ + d, gy[3] + 0.8), (x_ + d * 1.3, gy[3] + 1.9)], "planting", E["hx"]("8E7CC3"), 0.3,
                        over=0.0, amp=0.02, retrace=False, z=E["Z_TREE"])
        x_ += 2.8
    E["sketch_tree"](o, 3 * w + 34.5, gy[3], 6.0)     # Demeter's Garden olive (K5)
    for xs in (4 * w + 6.0, 4 * w + 15.0):            # olives
        E["sketch_tree"](o, xs, gy[4], 7.0)
    x_ = 4 * w + 26.0
    while x_ < LAD_W - 1.0:                           # field crop rows
        E["sketch"](o, [(x_, gy[4]), (x_, gy[4] + 1.6)], "planting", E["hx"](C["field"]), 0.35, over=0.0, amp=0.02,
                    retrace=False, z=E["Z_TREE"])
        x_ += 1.4
    # the site edge: farmland only outside the site
    E["sketch"](o, [(4 * w, gy[3] + 1.5), (4 * w, gy[4] + 11.0)], "site edge", E["INK2"], E["PEN_FINE"], over=0.0,
                retrace=False, dashed=True, z=E["Z_LINE"])
    # people: the season's activities. v4 (MIRAQUA 28 Oct, P19.2): ONE figure set, common/figures.py silhouettes at
    # true scale (an adult 1.75 m, LAD_U units a metre), the section's people colour (the board's SA people tone, as
    # the sketch engine had it), every outline of a figure filled opaque in that one colour, no stroke (was the
    # board's stick-like SA_FIGS at 0.9 opacity and a hand-made seated figure)
    for kind, x, y, flip, _lab, _src in sea["acts"]:
        if kind is None:
            keep["figs"].append(None)
            continue
        yf = y - LAD_SEAT * LAD_U if kind == "sit" else y   # the seated figure's seat on (x, y), its legs hang down
        rings = [[(x + a * LAD_U, yf + b * LAD_U) for a, b in r] for r in fig_polys(kind, 1.75, -1 if flip else 1)]
        for r in rings:
            E["fill"](o, r, "people", E["SITE_PEOPLE"], boundary=False, z=E["Z_PEOPLE"], hand_=False)
        xs_, ys_ = [p[0] for r in rings for p in r], [p[1] for r in rings for p in r]
        keep["figs"].append((min(xs_), min(ys_), max(xs_), max(ys_)))
    keep["boxes"] += [f for f in keep["figs"] if f]
    if sea["key"] == "high":                          # the design flood levels, hand dashed lines and level marks
        xe = 4 * w - 2.0 + 4.0 * (LAD_Q500 - gy[3]) / (gy[4] - gy[3])
        for lv in (LAD_Q500, LAD_Q100):
            E["sketch"](o, [(0.0, lv), (xe, lv)], "flood lines", E["HERITAGE"], E["PEN_FINE"], over=0.0, retrace=False,
                        dashed=True, z=E["Z_LINE"])
            xm = 3 * w + 26.0 if lv == LAD_Q500 else 3 * w + 20.0
            E["level_mark"](o, xm, lv, E["HERITAGE"], "flood lines")
            keep["lines"].append([(0.0, lv), (xe, lv)])
            keep["boxes"].append((xm - 1.0, lv, xm + 1.0, lv + 1.7))
    if sea["key"] == "low":                           # the farms are watered from storage in summer: the one arrow
        a_, b_ = (3 * w + 22.0, gy[4] + 10.0), (4 * w + 9.0, gy[4] + 8.0)
        E["hand_arrow"](o, a_, b_, E["SITE_WATER_D"], bend=-0.15)
        m_ = ((a_[0] + b_[0]) / 2.0 + (b_[1] - a_[1]) * 0.15, (a_[1] + b_[1]) / 2.0 - (b_[0] - a_[0]) * 0.15)   # its bow
        keep["lines"].append([(a_[0] * (1 - t) ** 2 + 2 * m_[0] * t * (1 - t) + b_[0] * t * t,
                               a_[1] * (1 - t) ** 2 + 2 * m_[1] * t * (1 - t) + b_[1] * t * t) for t in
                              (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)])
    if sea["mark"] == "winter":
        E["cloud_rain"](o, mark_xy[0], mark_xy[1], 2.0)
    elif sea["mark"] == "summer":
        E["sun"](o, mark_xy[0], mark_xy[1], 1.7)
    E["sketch"](o, gs, "ground lines", E["SKINK"], E["PEN_BOLD"], z=E["Z_LINE"])   # the cut: the gesture
    return sorted(E["ZP"], key=lambda e: (e[0], e[1])), keep


# v1.6: the one-way chain along the stream, upstream to the farms: (name, marker, programme, historic root, sources).
# Spec §3 / Aras 27 Oct: option A only; hubs at the bridges with in-bed sub-hubs; Demeter's Garden on the SW bank at
# K5; farmland only outside the site.
CHAIN = [("UPSTREAM ENTRY", "reeds", "reed basins clean once · terraces hold", None, (CHAIN_REF,)),
         ("K4", "hub", "hub + sub-hub · water-touching step", "Roman bridge · Tabaklar Hamamı", (PROG,)),
         ("K3", "hub", "hub + sub-hub · craft workshops", "tanning quarter (Tabakhane)", (PROG,)),
         (u"İSTİKLAL MEYDANI", "small", "hidden-stream square", "over the Red Hall tunnels", (PROG,)),
         ("K5", "hub", "hub + sub-hub · Demeter's Garden", "Roman bridge · Demeter, abundance", (PROG, GARDEN)),
         ("K6", "gate", "gateway out", None, (PROG,)),
         ("DOWNSTREAM REACH", "reeds", "floodable planting · boardwalk", "Late Antique workshops", (CHAIN_REF, PROG)),
         ("FARMLAND", "farm", "outside the site · water from storage", "Tersane cotton (16th c.)", (COTTON_H,))]
HUB_COL = "BC6F45"                                   # the sketch engine's walkable edge (terracotta)


def chain_strip(pg, P, y_top):
    """the chain across the page: node names, the one-way water ribbon with hubs and sub-hubs, programme and root
    keywords. Returns the lowest y used."""
    n = len(CHAIN)
    x0, dx = 16.0, (404.0 - 16.0) / n
    yr = y_top - 6.0                                 # the ribbon
    xs = [x0 + 2.0 + i * dx for i in range(n)]
    pg.line([(xs[0], yr), (xs[2], yr)], C["water"], 1.6)
    pg.line([(xs[2], yr), (xs[3] + dx * 0.5, yr)], C["water"], 1.6, (1.6, 1.1))   # the covered reach (H2)
    pg.line([(xs[3] + dx * 0.5, yr), (xs[-1] - 4.0, yr)], C["water"], 1.6)
    pg.poly([(xs[-1] - 4.0, yr + 1.8), (xs[-1] - 0.6, yr), (xs[-1] - 4.0, yr - 1.8)], fill=C["water"], closed=True)
    for i in range(n - 2):                           # one way, with the stream
        ax = (xs[i] + xs[i + 1]) / 2.0 + 4.0
        pg.poly([(ax - 1.2, yr + 1.1), (ax + 0.6, yr), (ax - 1.2, yr - 1.1)], fill=C["water_deep"], closed=True)
    low = yr
    for i, (name, mk, prog, root, refs) in enumerate(CHAIN):
        x = xs[i]
        if mk == "hub":
            pg.rect(x - 1.6, yr - 1.6, 3.2, 3.2, fill=HUB_COL, stroke=C["ink"], lw=0.2)
            pg.circle(x, yr - 3.4, 0.8, fill=C["water_deep"])
        elif mk == "small":
            pg.rect(x - 1.1, yr - 1.1, 2.2, 2.2, fill=C["white"], stroke=HUB_COL, lw=0.4)
        elif mk == "gate":
            pg.line([(x - 1.2, yr + 1.8), (x + 0.8, yr), (x - 1.2, yr - 1.8)], C["ink"], 0.4)
        elif mk == "reeds":
            icon(pg, "clean", x - 2.5, yr + 2.3, 5.0)
        else:
            icon(pg, "outside", x - 2.0, yr + 2.8, 5.6)
        tx = x - 1.5
        P.text(pg, name, tx, yr + 3.6, 8.5, C["ink"], True)
        y = yr - 7.0                               # clear of the sub-hub dot
        mark = "".join(cite(r) for r in refs)
        lines = [(q, C["ink"]) for q in wrap(prog + ("" if root else " " + mark), 7, dx - 3.0)]
        if root:
            lines += [(q, C["accent"]) for q in wrap(root + " " + mark, 7, dx - 3.0)]
        for q, col in lines:
            P.text(pg, q, tx, y, 7, col)
            y -= 2.9
        low = min(low, y + 2.9 - 1.2)
    return low                                       # v4 (P19.1): the key to the markers is in we_do_band now


WE_X = 14.0 + 7 * ((392.0 - 11 * 5.0) / 12.0 + 5.0)   # v4 (P19.1): 245.6 mm, grid column 8 of 12 (14 mm margins,
                                                      # 5 mm gutters, the booklet grid)
WE_Y = (HEAD_Y[0], 279.8, 274.6, HEAD_Y[2])           # baselines: steps 1-3, steps 4-5, NEXT, the chain's key
WE_PT = 7.5                                           # the booklet's label size
# v4 (P19.1, N1): NEXT names the page that really follows in the booklet's order, by its title (the booklet
# renumbers): theme D's first page, "The heritage loop" (bergama_booklet data/PLAN.py; "Heritage along the stream" is
# a frame page the booklet leaves out)
NEXT_PAGE = [(u"D  The heritage loop", C["ink"], True), (u": it starts from the roots in red on this chain", C["ink"], False)]
CHAIN_KEY = [("ribbon", u"one way, with the stream"), ("dash", u"covered reach"), ("hub", u"hub square, dry"),
             ("dot", u"sub-hub in the bed, floodable")]   # in the order the chain shows them, left to right


def we_do_band(pg, P):
    """v3 (Aras 27 Oct 17:35, Prompt 6 task 3 and rule 7: "the last page of the block clearly states 'what we do with
    it' and leads into the next theme"): what we do with the water in five numbered steps (the water board's p.23
    loop and this page's ladder, in brief) and NEXT, which starts from the roots drawn in red on the chain below.
    v4 (MIRAQUA 28 Oct, P19.1: the corner was cramped, five rows 4.5 mm apart on a ragged edge, the key right-aligned
    against the chain): the stage tag is the kicker over the title now (header); the corner is ONE block on the page
    grid, left edge on grid column 8 (WE_X), four rows from the kicker's baseline down to the subtitle's (WE_Y, 5.2 mm
    apart, the chip squares 1.6 mm clear of each other, the key 5 mm clear of the chain): steps 1-3, steps 4-5, NEXT
    and the page that follows, then the chain's key (moved up from over the chain), all at 7.5 pt."""
    x = WE_X
    for k, r in enumerate((WE_DO[:3], WE_DO[3:])):
        chips(pg, x, WE_Y[k], r, WE_PT)
        P.boxes.append((x, WE_Y[k] - 0.8, x + chips_w(r, WE_PT), WE_Y[k] + 3.0))
    yb = WE_Y[2]
    P.text(pg, "NEXT", x, yb, WE_PT, C["accent"], True)
    xx = step_arrow(pg, x + text_w("NEXT", WE_PT, True) + 1.5, yb) + 1.5
    for t, col, b in NEXT_PAGE:
        P.text(pg, t, xx, yb, WE_PT, col, b); xx += text_w(t, WE_PT, b)
    xx, yb = x, WE_Y[3]                              # the chain's key: sample, name; 5 mm between two
    for kind, lab in CHAIN_KEY:
        if kind == "hub":
            pg.rect(xx + 0.6, yb - 0.2, 2.6, 2.6, fill=HUB_COL, stroke=C["ink"], lw=0.2)
        elif kind == "dot":
            pg.circle(xx + 1.9, yb + 1.1, 0.8, fill=C["water_deep"])
        elif kind == "dash":
            pg.line([(xx, yb + 1.1), (xx + 4.0, yb + 1.1)], C["water"], 1.4, (1.2, 0.8))
        else:
            pg.line([(xx, yb + 1.1), (xx + 4.0, yb + 1.1)], C["water"], 1.4)
        P.text(pg, lab, xx + 5.0, yb, WE_PT, C["ink"])
        xx += 5.0 + text_w(lab, WE_PT) + 5.0


LAB_PAD = 0.6                        # v4 (G4): mm kept clear round a ladder label (lines, figures, plants, labels)


def lad_labels(pg, P, labs, keep, X, Y, reg):
    """v4 (MIRAQUA 28 Oct, G4; F13 "the two blocked ladder labels placed": "hub square: dry, step-free" and "wade the
    strip" were left out on every run): a season row's labels placed by common/label_place.py, each in the nearest
    free spot round its point (a figure's head, a level line, a line's end), clear of the other labels, the figures,
    the plants, the level marks and the cut ground (its line and the soil under it), the flood and site-edge lines and
    the summer arrow, LAB_PAD mm round each; farther out on a hair leader; always 7 pt (the booklet's minimum), so a
    label is left out only when its row is full (logged). Two passes: first every label clear of the plants too; the
    ones with no spot near their point then may sit over a plant (white halo), still never over a figure, a level
    mark, a line or a label, and with none there take the nearest free spot in the row on a leader. labs = [(text, x,
    y, size, colour, bold)] page mm, in placing order; keep = the row's sketch geometry (ladder_row); X, Y: sketch
    units -> page mm; reg: the row's box. Returns the texts left out."""
    k = 0.3528
    pm = lambda bs: [(X(b[0]), Y(b[1]), X(b[2]), Y(b[3])) for b in bs]   # sketch units -> page mm
    hard = pm(keep["boxes"])
    g = keep["ground"]
    for (ax_, ay_), (bx_, by_) in zip(g[:-1], g[1:]):          # the soil under the cut line
        if abs(bx_ - ax_) > 1e-6:
            hard.append((X(min(ax_, bx_)), reg[1] - 1.0, X(max(ax_, bx_)), Y(min(ay_, by_))))
    hard += [b for b in P.boxes if lp_hit(b, reg, 1.0)]        # only what lies in the row (speed)
    segs = [((X(p[0]), Y(p[1])), (X(q[0]), Y(q[1]))) for ln in keep["lines"] for p, q in zip(ln[:-1], ln[1:])]
    items = []
    for s, ax, ay, size, col, bold in labs:
        wh = (text_w(s, size, bold) + 1.0 + 2 * LAB_PAD, size * k * 1.08 + 0.8 + 2 * LAB_PAD)
        items.append(dict(x=ax, y=ay, wh=(lambda f, wh=wh: wh), rank=1))
    got = place_labels_all(items, hard + pm(keep["soft"]), bounds=reg, segs=segs, sizes=(1.0,), pad=0.3)   # pass 1
    rest = [i for i in range(len(items)) if i not in got]
    if rest:                                                    # pass 2: over a plant, else anywhere free (rank 0)
        more = place_labels_all([dict(items[i], rank=0) for i in rest], hard + [v[0] for v in got.values()],
                                bounds=reg, segs=segs, sizes=(1.0,), pad=0.3)
        got.update((rest[j], v) for j, v in more.items())
    out = []
    for i, (s, ax, ay, size, col, bold) in enumerate(labs):
        if i not in got:
            out.append(s)
            continue
        b, lead, _f = got[i]
        b = (b[0] + LAB_PAD, b[1] + LAB_PAD, b[2] - LAB_PAD, b[3] - LAB_PAD)   # the text's own box
        if lead:
            pg.line([(ax, ay), lp_leader_end(b, (ax, ay))], C["ink2"], 0.15)
        pg.text(s, b[0] + 0.5, b[1] + 0.4 + 0.28 * size * k, size, col, bold, halo="FFFFFF")
        P.boxes.append(b)
    return out


def page_ladder(L, src):
    pg = Page(420, 297)
    P = Placer()
    header(pg, "ONE PLANT LADDER, STREAMBED TO FIELD",
           "One cut from the stream to the farms, through the year: what the water does and what people do on each step",
           tag=STAGE_TAG)                          # v4 (P19.1): the stage tag is the kicker, as on page 1
    we_do_band(pg, P)                              # v3 (Prompt 6): the water theme closes here, top right
    # 1 the chain: where the ladder sits along the stream, the programme and its roots
    y_chain = chain_strip(pg, P, 264.0)            # v2: 4 mm higher (was 260; its names end 6 mm under the subtitle)
    ag_crop("ag3_chain", 2, 13.0, y_chain - 1.0, 407.0, 266.5)   # v4: top under the subtitle (269.5 now; was 270)
    # 2 the ladder, one row a season
    top = y_chain - 2.0
    for r, sea in enumerate(seasons()):
        T, B = top - r * ROW_H, top - (r + 1) * ROW_H
        y0 = B + 2.0 - LAD_GB * LAD_F                  # page y of the sketch's 0
        mark = ((19.0 - LAD_X0) / LAD_F, (T - 6.0 - y0) / LAD_F)
        items, keep = ladder_row(sea, mark)            # v4: and what the labels keep clear of
        sk_draw(pg, xform([e[2] for e in items], LAD_F, LAD_X0, y0))   # v1.7: (z, order, item, group)
        if sea["mark"] == "olive":
            icon(pg, "olive", 14.0, T - 1.5, 9.0)
        P.text(pg, sea["name"], 26.0, T - 8.0, 12, C["ink"], True)
        P.text(pg, sea["months"], 26.0, T - 13.0, 9, C["accent"], True)
        y = T - 18.5
        for t, ref in sea["side"]:
            for q in wrap(t + ((" " + cite(ref)) if ref else ""), 7.5, LAD_X0 - 30.0):
                P.text(pg, q, 26.0, y, 7.5, C["ink"])
                y -= 3.2
        reg = (LAD_X0, B + 1.0, LAD_X1, T - 0.8)
        Y = lambda v: y0 + v * LAD_F
        X = lambda v: LAD_X0 + v * LAD_F
        # v4 (MIRAQUA 28 Oct, G4, F13): the row's labels, all placed together by lad_labels in this order: the flood
        # levels at their lines, the people's labels at their heads, then the notes that can sit farther off (was
        # Placer.put: upwards over the point only, so "hub square: dry, step-free" and "wade the strip" found no
        # place on every run). G13: heights in m with 2 decimals (values unchanged). Bank depth research 28 Oct §4.5:
        # Q100 / Q500 top the bank only at S4; the survey's K4 bank predates the DSİ walls.
        labs, notes = [], []
        if sea["key"] == "high":
            labs += [(cited(u"Q500 · 263 m³/s · %s-%s m above the bed" % (u_num(2.3, 2), u_num(3.3, 2)), DEPTH),
                      X(1.5), Y(LAD_Q500), 7, "8B2D2D", False),
                     (u"Q100 · 205 m³/s · %s-%s m" % (u_num(2.0, 2), u_num(3.0, 2)), X(1.5), Y(LAD_Q100), 7, "8B2D2D",
                      False)]
            notes += [(u"over the bank top only at S4 (left); K4 before the DSİ walls", X(3 * LAD_S + 3.0),
                       Y(LAD_Q500), 7, "8B2D2D", False),
                      (u"site edge: farmland outside", X(4 * LAD_S), Y(LAD_GY[4] + 11.0), 7, C["ink2"], False)]
        if sea["key"] == "low":                        # at the summer arrow's tail
            notes.append((u"stored winter water", X(3 * LAD_S + 22.0), Y(LAD_GY[4] + 10.0), 7, C["water_deep"], True))
        for (kind, x, yv, flip, lab, ref), f in zip(sea["acts"], keep["figs"]):
            if lab:                                    # a figure's label points at its head
                ax, ay = ((f[0] + f[2]) / 2.0, f[3]) if f else (x, yv)
                labs.append((cited(lab, ref), X(ax), Y(ay), 7, C["ink"], True))
        P.dropped += lad_labels(pg, P, labs + notes, keep, X, Y, reg)
        if r < 2:
            pg.line([(14.0, B), (406.0, B)], C["faint"], 0.3)
    bot = top - 3 * ROW_H
    ag_crop("ag3_seasons", 2, 13.0, bot - 0.5, 407.0, top + 0.5)
    # 3 what grows on each step (one column under each step) and, left, what goes and the odour
    # v2 (Aras 27 Oct, Prompt 5): every plant of a step as a photo, PHOTO_W x PHOTO_H, two side by side (2 x 28 + 2 mm
    # fits the 60 mm column with 2 mm to the next), its name "English (Turkish)" and the photo's credit [n] under it
    # (7 pt, two lines at most); the reasons under the names only when the column still ends above the 14 mm margin
    yt = bot - 3.0                                   # v2: was bot - 4.0
    w = LAD_S * LAD_F
    per = 2 if 2 * PHOTO_W + PH_GAP <= w - 2.0 else 1
    short = []
    for i, st in enumerate(STEPS):
        xa = LAD_X0 + i * w + 1.0
        for brief in (False, True):                  # the species' reasons left out if the column would not fit
            y, ops, pics = yt, [], []
            ops.append((st["name"], xa, y, 8.5, C["ink"], True)); y -= 3.4
            ops.append((st["sub"], xa, y, 7, C["ink2"], False)); y -= 6.4
            tag_y = y
            y -= 4.0
            if st["band"]:
                l_, r_ = GEO["corridor"]["left " + st["band"]], GEO["corridor"]["right " + st["band"]]
                v = [(l_[k] + r_[k]) / 2.0 for k in ("trees", "grass", "farmland")]
                t = "today: trees %.0f %% · grass %.0f %% · fields %.0f %% %s" % (v[0], v[1], v[2], cite(TODAY))
                for q in wrap(t, 7, w - 4.0):
                    ops.append((q, xa, y, 7, C["ink2"], False)); y -= 2.9
            if st["name"] == "FARMS":
                for q in wrap(STEPS[4]["water"][1].replace("{reuse}", cite(REUSE)), 7, w - 4.0):
                    ops.append((q, xa, y, 7, C["ink2"], False)); y -= 2.9
            y -= 1.2
            ops.append(("WE PLANT " + cite(SPECIES) if st["name"] != "FARMS" else "THEY GROW", xa, y, 7, C["accent"], True))
            y -= 1.6                                 # v2: the top of the first row of photos
            low = y
            for r0 in range(0, len(st["plant"]), per):
                n_ = 1
                for c_, (key, why) in enumerate(st["plant"][r0:r0 + per]):
                    px = xa + c_ * (PHOTO_W + PH_GAP)
                    pics.append((key, px, y))
                    L_ = [(q, C["ink"], True) for q in name_lines(key, photo_mark(key), 7, PHOTO_W)]
                    if not brief:
                        L_ += [(q, C["ink2"], False) for q in wrap(why, 7, PHOTO_W)]
                    yy = y - PHOTO_H - 2.5           # the first line's baseline, under the photo
                    for q, col, b in L_:
                        ops.append((q, px, yy, 7, col, b)); yy -= 2.6
                    n_ = max(n_, len(L_))
                low = y - PHOTO_H - 2.5 - 2.6 * (n_ - 1) - 0.6   # the row's lowest ink (descenders)
                y = low - 1.1                        # the next row's top
            if low >= 14.0:
                break
        if brief:
            short.append(st["name"] + ("" if low >= 14.0 else " (FLAG: ends at %.1f mm, under the 14 mm margin)" % low))
        for s_, x_, y_, sz, col, b in ops:
            P.text(pg, s_, x_, y_, sz, col, b)
        for key, px, top_ in pics:                   # v2: the frames; the photos go in after write_pdf (put_photos)
            photo_frame(pg, 2, key, px, top_, P)
        pg.rect(xa, tag_y, text_w(st["job"], 8, True) + 4, 5.2, fill=C["accent"])
        pg.text(st["job"], xa + 2, tag_y + 1.5, 8, C["white"], True)
        jx = xa + text_w(st["job"], 8, True) + 6
        for word, kind in JOB_ICON:                  # the job as pictograms beside the tag
            if word in st["job"]:
                pg.rect(jx, tag_y - 0.4, 6.0, 6.0, fill=C["white"], stroke=C["faint"], lw=0.2)
                icon(pg, kind, jx + 0.5, tag_y + 5.1, 5.0); jx += 7.0
    if short:
        LOG_NOTES.append("p3 plant reasons left out under the photos (no room above the 14 mm margin): " + ", ".join(short))
    # left column: what goes, the odour, how to read the steps
    # v2 (Prompt 5): the giant reed by its name "English (Turkish)", its photo's credit [n] after the name, the photo
    # under the reason (the column is LAD_X0 - 14 = 92 mm wide)
    y = yt
    for t, sz, col, b, mk in ((u"REMOVE: " + plant_name("giant_reed"), 8, C["accent"], True, photo_mark("giant_reed")),
                              ("raises flood risk, blocks bridges", 7, C["accent"], False, "")):
        lines = wrap(t, sz, LAD_X0 - 18.0, b)
        for k_, q in enumerate(lines):
            P.text(pg, q, 14.0, y, sz, col, b)
            if mk and k_ == len(lines) - 1:
                P.text(pg, mk, 14.0 + text_w(q, sz, b) + 1.0, y, 7, C["accent"])
            y -= sz * 0.3528 * 1.35
    photo_frame(pg, 2, "giant_reed", 14.0, y + 1.4, P)
    y -= PHOTO_H + 0.6
    y -= 3.0
    icon(pg, "nose", 14.0, y + 3.0, 6.0)
    for t, b in (("ODOUR: no measured plant effect " + cite(SPECIES), True), ("keep sewage out", False),
                 ("clean once, at the upstream end", False), ("plants: clean nutrients, give scent", False)):
        for q in wrap(t, 7.5, LAD_X0 - 30.0, b):
            P.text(pg, q, 22.0, y, 7.5, C["ink"], b); y -= 3.2
    y -= 3.0
    for t in ("steps = planting bands " + cite(BANDS), "depths above the bed " + cite(DEPTH), "a diagram, not to scale",
              "downstream flat end: Q100 %s, Q500 %s" % (u_height(1.4), u_height(1.5))):   # v4 (G13): 1.40 m, 1.50 m
        for q in wrap(t, 7, LAD_X0 - 18.0):
            P.text(pg, q, 14.0, y, 7, C["ink2"]); y -= 2.9
    ag_crop("ag3_plants", 2, 13.0, 14.0, 407.0, yt + 3.0)       # v2: yt + 3 = bot (yt is bot - 3 now)
    LOG_NOTES.extend("p3 label left out (no free place): " + s for s in P.dropped)
    return pg

# ------------------------------------------------------------------ v1.6: the sources page (Aras 27 Oct: no source footers)
def page_sources():
    """the sheet's one numbered source key, on its own page: the [n] marks on pages 1-3 refer to it, and the
    booklet's sources page reads it from here ("Sources by number:", as the old page footers)."""
    pg = Page(420, 297)
    pg.rect(0, 0, 420, 297, fill=C["white"])
    pg.text("SOURCES", 14, 279, 22, C["ink"], True)
    pg.text("Numbered as the [n] marks on pages 1-3", 14, 271.5, 11, C["ink2"])
    key = "Sources by number: " + "  ".join("[%d] %s" % (i + 1, k) for i, k in enumerate(SRC_KEY))
    pg.para(key, 14, 260, 392, 8, C["ink"], lead=1.35)
    return pg

# ------------------------------------------------------------------ v1.4: A3 booklet = crops of this sheet (booklet/CROP_SPEC.md)
# Aras 25 Oct 21:47: the booklet shows the sheet's own drawings. Each page function records its panels' rects
# (from the same numbers it lays them out with) in AG_CROPS; booklet_export writes them to blocks.json, with
# booklet/results.json (hectares per crop, same keys as v1.3). The v1.3 booklet redraws are gone.
# ---- A3 booklet assets (SCRIPT_STANDARD §8; booklet/ASSET_SPEC.md) ----
# Each booklet frame = one text-free vector PDF drawn at the frame's size + its words as labels in blocks.json.
# The assembler (bergama_booklet) sets every label as live text in the booklet font, never below 7 pt.
BK_MIN_PT = 7.5                              # labels and captions on the booklet (brief: 7-8 pt, minimum 7)
BK_CAPTION_MM = 5.0                          # caption line under every drawing frame


def bk_frame(key, w_default, h_default):
    """(w, h) mm a drawing for asset key "<folder>/<block>" is drawn at: the assembler's booklet_slots.json if it has
    run once, else the defaults given (the plan's frame size). h excludes the caption line."""
    try:
        import json as _j
        with open(bg_first([os.path.join(bg_booklet(""), "booklet_slots.json"),        # 27 Oct: cached/booklet/
                            os.path.join(bg_output("bergama_booklet"), "booklet_slots.json")]), encoding="utf-8") as f:
            s = _j.load(f)[key]
        return float(s["w_mm"]), float(s["h_mm"]) - BK_CAPTION_MM
    except Exception:
        return float(w_default), float(h_default) - BK_CAPTION_MM


def bk_take_text(items, H):
    """Page items (poly/line/circle/text tuples, y up from the bottom, mm) -> (items without text, labels).
    Labels: x, y in mm from the top-left (y to the baseline), size raised to BK_MIN_PT, colour hex."""
    keep, labels = [], []
    for it in items:
        if it[0] != "text":
            keep.append(it)
            continue
        _, s, x, y, size, color, bold, align = it[:8]
        labels.append({"x": round(x, 2), "y": round(H - y, 2), "text": s, "size": max(float(size), BK_MIN_PT),
                       "bold": bool(bold), "anchor": align or "L", "colour": color if isinstance(color, str) else "4A3F35"})
    return keep, labels


class BkBlocks(object):
    """Collects one script's booklet blocks and writes cached/booklet/<folder>/blocks.json (27 Oct, Aras: output/ holds
    final PDFs only; was output/<folder>/booklet/). out_dir = the script's output folder; its name is the folder key."""
    def __init__(self, out_dir, script, version):
        self.dir = bg_booklet(os.path.basename(os.path.normpath(out_dir)))
        os.makedirs(self.dir, exist_ok=True)
        self.d = {"script": script, "version": version, "sources": {}, "blocks": {}}

    def path(self, name):
        return os.path.join(self.dir, name)

    def source(self, key, text, url):
        """A public source: used in any text as {src:key}; numbered once for the whole booklet."""
        self.d["sources"][key] = {"text": text, "url": url}

    def drawing(self, bid, pdf_name, labels, caption="", scale_den=None, legend=None):
        self.d["blocks"][bid] = {"type": "drawing", "pdf": pdf_name, "page": 0, "labels": labels, "caption": caption,
                                 "scale_den": scale_den, "legend": legend or []}

    def crop(self, bid, pdf_name, rect_mm, caption="", scale_den=None, legend=None, page=0, drop=None):
        """A booklet drawing taken from this script's own sheet (Aras 25 Oct 21:47: the booklet shows the sheet's
        drawing, re-laid): pdf_name = the sheet PDF in this script's output folder, rect_mm = (x0, y0, x1, y1) of the
        panel in mm from the sheet page's top-left (y down), scale_den = the sheet's scale at 1:1 print (None if not to
        scale). The assembler scales the crop to its frame and resets the sheet's words inside it as live labels;
        drop = regexes of sheet texts not to carry."""
        self.d["blocks"][bid] = {"type": "crop", "pdf": pdf_name, "page": page,
                                 "rect_mm": [round(float(v), 2) for v in rect_mm], "caption": caption,
                                 "scale_den": scale_den, "legend": legend or [], "drop": drop or []}

    def tiles(self, bid, tiles):
        self.d["blocks"][bid] = {"type": "tiles", "tiles": tiles}

    def text(self, bid, heading="", body="", bullets=None):
        self.d["blocks"][bid] = {"type": "text", "heading": heading, "body": body, "bullets": bullets or []}

    def save(self):
        import json as _j
        p = os.path.join(self.dir, "blocks.json")
        with open(p, "w", encoding="utf-8") as f:
            _j.dump(self.d, f, ensure_ascii=False, indent=1)
        return p
AG_CROPS = []                        # (id, page index, (x0, y0, x1, y1) mm from the page's top-left, y down, den, legend, drop)
AG_CAPTIONS = {"ag1_headline": "Storage and water to the farms", "ag1_bars": "Hectares one storage irrigates, by crop",
               "ag1_reading": "Same storage: how much more land", "ag1_context": "Why crop choice is the lever",
               "ag1_replaces": "What it replaces", "ag1_crops": "The crops",   # v2: the crop photos
               "ag1_stream": "The stream comes first: a normal and a 1-in-5 dry year",   # v3 (Prompt 6)
               "ag2_plan": "The farms we feed, on the site plan",
               "ag3_chain": "One way along the stream: the programme and its roots",
               "ag3_seasons": "One plant ladder through the year: what people do", "ag3_plants": "What grows on each step"}


def ag_crop(cid, page, x0, y0, x1, y1, den=None, legend=None, drop=None):
    """a panel of page `page` (0-2), given as the page's own y-up mm (x0, y0)-(x1, y1)"""
    AG_CROPS.append((cid, page, (round(x0, 2), round(297.0 - y1, 2), round(x1, 2), round(297.0 - y0, 2)), den,
                     legend or [], drop or []))


def ha_results(L):
    """hectares the storage irrigates per crop (page 1's bars): normal year and 1-in-5 dry year, lo-hi over the storage
    span (and the deficit saving range for olive), plus the dry-year ratio olive deficit / cotton."""
    p_lo, p_hi = span(L["farm_share_dry5_pct"]); n_lo, n_hi = span(L["farm_need_dry5_m3"])
    w_lo, w_hi = n_lo * p_lo / 100.0, n_hi * p_hi / 100.0
    rows = [("olive_deficit", "olive", DEFICIT), ("olive_full", "olive", None)] + \
           [(c, c, None) for c in ("maize", "tomato", "cotton") if c in NET]
    out = {}
    for key, crop, dfc in rows:
        if crop not in NET: continue
        out[key] = {}
        for yr, yk in (("normal", "normal"), ("dry", "dry5")):
            g = gross_m3_ha(crop, yr)
            lo, hi = (w_lo / (g * (1 - dfc[0])), w_hi / (g * (1 - dfc[1]))) if dfc else (w_lo / g, w_hi / g)
            out[key][yk] = {"lo": round(lo, 1), "hi": round(hi, 1), "m3_per_ha": round(g, 0)}
    R = {"ha_per_crop": out, "to_farms_dry5_m3": [round(w_lo), round(w_hi)],
         "farms_fed_ha": round(L["cropland_ha"] + L["orchard_ha"], 2)}
    if "olive_deficit" in out and "cotton" in out:
        a, b = out["olive_deficit"]["dry5"], out["cotton"]["dry5"]
        R["ratio_olive_deficit_vs_cotton_dry5"] = {"lo": round(a["lo"] / b["lo"], 2), "hi": round(a["hi"] / b["hi"], 2)}
    ys = L.get("year_split")
    if ys and "normal" in ys and "dry5" in ys:      # v3 (Prompt 6): page 1's double squeeze, dry year against normal
        a_, b_, c_ = squeeze(ys)
        R["stream_first"] = {"water_years": [ys["normal"]["water_year"], ys["dry5"]["water_year"]],
                             "left_for_farms_change_pct": round(100.0 * a_, 1), "need_per_ha_change_pct": round(100.0 * b_, 1),
                             "hectares_change_pct": round(100.0 * c_, 1)}
    return R


def booklet_export(L):
    """blocks.json: one crop per panel of the A3 sheet; results.json: hectares per crop. Returns a log line."""
    bk = BkBlocks(OUT_DIR, "AgriCulture", VERSION)
    for cid, page, r, den, legend, drop in AG_CROPS:
        bk.crop(cid, OUT_PDF, r, caption=AG_CAPTIONS.get(cid, ""), scale_den=den, legend=legend, page=page, drop=drop)
    bk.save()
    R = ha_results(L)
    R.update(script="AgriCulture", version=VERSION)
    with open(bk.path("results.json"), "w", encoding="utf-8") as f:
        json.dump(R, f, ensure_ascii=False, indent=1)
    return "booklet: %d crops, results.json" % len(AG_CROPS)

# ------------------------------------------------------------------ build and run
def build(path):
    BASE_OFF[0] = False
    L, src = live()
    NET.clear(); NET.update(L["net"])
    PHOTO_GOT.clear(); PHOTO_STATE.clear(); del PHOTO_LOG[:]   # v2: the plant photos, read once a press
    for _ in range(2):
        del AG_CROPS[:], SRC_KEY[:], LOG_NOTES[:], PHOTO_FR[:]      # v1.6: one source numbering for the whole sheet
        PHOTO_N[0] = 0
        pages = [page_cubic(L, src), page_farms(L, src), page_ladder(L, src)]
        write_pdf(pages + [page_sources()], path)
        try:                                       # v1.5: the site board's plan 01 under the farms layer
            return src, put_base(path) + "\n" + put_photos(path)   # v2: then the photos (never raises)
        except PermissionError:
            raise
        except Exception as ex:                    # never an empty window: once more with the fallback drawing
            BASE_OFF[0] = True
            err = "farms map: FLAG the site plan could not be placed (%s: %s), fallback drawing" % (type(ex).__name__, ex)
    return src, err + "\n" + put_photos(path)

def main():
    t0 = time.time()
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, OUT_PDF)
    try:
        src, base = build(path)
    except PermissionError:
        return "The PDF is open in another program. Close it and press again: " + path
    try:                                           # v1.3: the A3 booklet frames; an error here never breaks the sheet
        bk = booklet_export(live()[0])
    except Exception as ex:
        bk = "booklet ERROR (sheet saved): %s: %s" % (type(ex).__name__, ex)
    bk = "\n".join([bk] + bg_tidy_output("Bergama_agriculture_alternatives"))   # 27 Oct: output/ = PDFs only
    flag = "".join("\n" + t for t in LOG_NOTES)
    flag += "\nFLAG: water balance results file not found in Downloads; its default-lands copy was used" if src == DEFAULT_NOTE else ""
    return "%s  %s\nfigures: %s%s\n%s\nagriculture alternatives %s, %.1f s\n%s" % (OUT_PDF, time.strftime("%H:%M:%S"), src, flag, base, VERSION, time.time() - t0, bk)

def chain_fire(v, key):
    """25 Oct 10:20 (one-click chain): the previous script's done output is a text "done HH:MM:SS.ss ..." that stays
    after the Button is released; each NEW text fires this script once (the Button still works as before)."""
    if isinstance(v, (list, tuple)):
        v = next((x for x in v if x is not None), None)
    s = str(v) if v is not None else ""
    if not s.startswith("done "):
        return False
    try:
        import scriptcontext as _scx
        try:
            key = key + ":" + str(ghenv.Component.InstanceGuid)              # noqa: F821
        except Exception:
            pass
        if _scx.sticky.get(key) == s:
            return False
        _scx.sticky[key] = s
        return True
    except Exception:
        return False


def done_text(ran, ok, secs):
    """The done output: kept until the next run (this Rhino session)."""
    return ("done " if ok else "ERROR ") + time.strftime("%H:%M:%S") + ".%02d" % int((time.time() % 1) * 100) + \
        " · %.0f s" % secs if ran else None


_gh = "ghenv" in globals()
if _gh:
    import scriptcontext as _sc
    try: _ik = ":" + str(ghenv.Component.InstanceGuid)   # 25 Oct 10:29: each component keeps its own log and done
    except Exception: _ik = ""
    _pressed = any(v is True for k, v in list(globals().items()) if not k.startswith("_") and isinstance(v, bool) and k not in ("True", "False", "done")) or \
        any(chain_fire(v, "bergama_agri_alt_log_chain") for k, v in list(globals().items()) if not k.startswith("_") and k != "done" and isinstance(v, str))
    if _pressed:
        _t0 = time.time()
        try:
            _res = main()
        except Exception as _ex:   # 25 Oct: the error goes into the log panel, the old log never stays
            import traceback as _tb
            _res = "ERROR: %s: %s\n%s" % (type(_ex).__name__, _ex, _tb.format_exc()[-600:])
        _sc.sticky["bergama_agri_alt_log" + _ik] = write_log(_res)
        _sc.sticky["bergama_agri_alt_log_status" + _ik] = ("ERROR" if _sc.sticky["bergama_agri_alt_log" + _ik].startswith(("ERROR", "The PDF is open")) else time.strftime("%H:%M") + " · %.0f s" % (time.time() - _t0))
        _sc.sticky["bergama_agri_alt_log_done" + _ik] = done_text(True, not _sc.sticky["bergama_agri_alt_log_status" + _ik].startswith("ERROR"), time.time() - _t0)
        _sc.sticky["bergama_agri_alt_log_ver" + _ik] = VERSION
    if _sc.sticky.get("bergama_agri_alt_log_ver" + _ik) != VERSION:   # v1.7 (Aras 27 Oct 15:35): a newly pasted version
        for _s in ("", "_status", "_done"):                            # shows itself at once, idle, no old time or log
            _sc.sticky.pop("bergama_agri_alt_log" + _s + _ik, None)
    done = _sc.sticky.get("bergama_agri_alt_log_done" + _ik, "idle")   # 25 Oct 10:20: stays after the run; wire into the next script's run (one-click chain)
    log = _sc.sticky.get("bergama_agri_alt_log" + _ik, "Press the Button to export to " + OUT_DIR)
    print(log)               # 25 Oct 12:10: the canvas's log output is Grasshopper's "out" (printed text): print the log
    try: ghenv.Component.Message = "AgriCulture " + VERSION + " · " + _sc.sticky.get("bergama_agri_alt_log_status" + _ik, "idle")   # Aras 25 Oct 09:44
    except Exception: pass
else:
    print(write_log(main()))
