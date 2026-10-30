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
# later press. Any licence is accepted (D8, PHOTO_ANY_LICENCE); credits stay. A photo Aras puts into the cache folder
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
    # H-B 30 Oct (M6, p16 gap): titles from the Commons search index (T1 sourcing §2 and a web search, 30 Oct); not
    # opened from here (Commons blocked in the cloud): UNVERIFIED until the first fetch on Aras's PC logs them.
    # Turkish name of Juncus effusus not verified: the genus name Kofa (as for the sharp rush) is used.
    "soft_rush": (u"Soft rush (Kofa)", (u"Pitrus (Juncus effusus) 07.JPG", u"Pitrus plant (Juncus effusus) (1).jpg",
                                       u"Pitrus (Juncus effusus) 05.JPG", u"JuncusEffusus.jpg"), True),
    "stone_pine": (u"Stone pine (Fıstık çamı)", (u"Stone Pine (Pinus pinea) - Rome, Italy 2024-03-04.jpg",
                                                 u"Pinus pinea.JPG"), True),
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


PHOTO_ANY_LICENCE = True            # D8 (Aras, 30 Oct): licences are not regarded; every source is still credited


def photo_free(lic):
    """True for an open licence: CC BY / CC BY-SA (any version), CC0, public domain; always True while
    PHOTO_ANY_LICENCE (D8)."""
    if PHOTO_ANY_LICENCE:
        return True
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
