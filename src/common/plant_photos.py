# ---- plant photos, shared by the water board and the agriculture alternatives (Aras 27 Oct, Prompt 5: "every plant
# AND every crop in the booklet gets a photo of the plant itself. Use openly licensed photos (e.g. Wikimedia Commons)
# credited in the sources, never photos from shop or nursery sites. Same crop ratio and size for every photo").
# Fetched once on Aras's PC (the cloud cannot reach Wikimedia), kept in the script's cache folder and read from there
# on every later press. First the English Wikipedia article's lead image (a Commons file chosen by the article's
# editors), else a Commons search for the botanical name (used only to find the file, never printed) that skips
# herbarium sheets, drawings and maps. Only CC BY, CC BY-SA, CC0 and public-domain files are used; the credit
# (author, licence, file) goes into the numbered source key. A photo Aras puts into the cache folder himself
# (<key>.jpg with a <key>.json {"file", "credit"}) is used as it is. No network or any failure = an empty frame.
PHOTO_W, PHOTO_H = 28.0, 21.0        # mm on the A3 page, every photo in the booklet (4:3, cover-cropped, never stretched)
PHOTO_PX = 480                       # px wide fetched (about 435 dpi at PHOTO_W)
PLANT_PHOTO_DIR = bg_cache("plant_photos")   # one folder for every script: the same plant shows the same photo
# Every plant and crop the booklet names: key -> (printed name "English (Turkish)", English Wikipedia article, botanical
# name for the Commons search; the botanical name is never printed). Names: English and Turkish as in
# research/water_data/04 §1 (species matrix), Aras's examples "Common reed (Kamış)", "Oriental plane (Doğu çınarı)";
# Kofa = the rush genus Juncus (turkiyebitkileri.com, Juncaceae - Kofagiller, Juncus - Kofa).
PLANTS = {
    "reed": (u"Common reed (Kamış)", u"Phragmites_australis", u"Phragmites australis"),
    "cattail": (u"Broadleaf cattail (Hasır otu)", u"Typha_latifolia", u"Typha latifolia"),
    "mint": (u"Water mint (Su nanesi)", u"Mentha_aquatica", u"Mentha aquatica"),
    "iris": (u"Yellow flag iris (Sarı süsen)", u"Iris_pseudacorus", u"Iris pseudacorus"),
    "rush": (u"Sharp rush (Kofa)", u"Juncus_acutus", u"Juncus acutus"),
    "loosestrife": (u"Purple loosestrife (Aklar otu)", u"Lythrum_salicaria", u"Lythrum salicaria"),
    "tamarisk": (u"Tamarisk (Ilgın)", u"Tamarix_smyrnensis", u"Tamarix smyrnensis"),
    "willow": (u"White willow (Ak söğüt)", u"Salix_alba", u"Salix alba"),
    "chaste": (u"Chaste tree (Hayıt)", u"Vitex_agnus-castus", u"Vitex agnus-castus"),
    "poplar": (u"White poplar (Ak kavak)", u"Populus_alba", u"Populus alba"),
    "ash": (u"Narrow-leaved ash (Dişbudak)", u"Fraxinus_angustifolia", u"Fraxinus angustifolia"),
    "oleander": (u"Oleander (Zakkum)", u"Nerium_oleander", u"Nerium oleander"),
    "plane": (u"Oriental plane (Doğu çınarı)", u"Platanus_orientalis", u"Platanus orientalis"),
    "lavender": (u"French lavender (Karabaş otu)", u"Lavandula_stoechas", u"Lavandula stoechas"),
    "rosemary": (u"Rosemary (Biberiye)", u"Salvia_rosmarinus", u"Salvia rosmarinus"),
    "olive": (u"Olive (Zeytin)", u"Olea_europaea", u"Olea europaea tree"),
    "cotton": (u"Cotton (Pamuk)", u"Gossypium_hirsutum", u"Gossypium hirsutum"),
    "maize": (u"Maize (Mısır)", None, u"Zea mays plant"),        # these two: Commons search for the growing plant
    "tomato": (u"Tomato (Domates)", None, u"Solanum lycopersicum plant"),  # (a lead image may show only the fruit)
    "giant_reed": (u"Giant reed (Kargı)", u"Arundo_donax", u"Arundo donax"),
}


def plant_name(key):
    """The printed name of a plant: "English (Turkish)"."""
    return PLANTS[key][0]


def plant_photo_of(key, log, state):
    """(jpeg path or None, credit or None, why not) of a plant in PLANTS, from the shared folder."""
    name, article, search = PLANTS[key]
    return plant_photo(key, name, article, search, PLANT_PHOTO_DIR, log, state)


PHOTO_UA = "MIRAQUA-studio-booklet/2 (Bergama student project, Yasar University; Python urllib)"
PHOTO_TIMEOUT = 8.0                  # s per request; after one network failure the rest are not tried this press
PHOTO_SKIP = ("herbar", "illustrat", "drawing", "kohler", "köhler", "koehler", "plate", "tafel", "map", "distribution",
              "flora", "botanical", "lithograph", "engraving", "seed", "pollen", "microscop", "stamp", "logo", "diagram",
              "range", "specimen")


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


def _photo_http(url):
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": PHOTO_UA})
    with urllib.request.urlopen(req, timeout=PHOTO_TIMEOUT) as r:
        return r.read()


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


def _photo_pick_lead(article):
    """The article's lead image as a Commons imageinfo record {title, thumburl, extmetadata}, or None."""
    import urllib.parse
    summ = json.loads(_photo_http("https://en.wikipedia.org/api/rest_v1/page/summary/" +
                                  urllib.parse.quote(article)).decode("utf-8"))
    orig = (summ.get("originalimage") or {}).get("source") or (summ.get("thumbnail") or {}).get("source")
    if not orig or "/commons/" not in orig:              # a file kept on Wikipedia itself may be non-free: skipped
        return None
    parts = urllib.parse.urlparse(orig).path.split("/")
    fname = urllib.parse.unquote(parts[-2] if "thumb" in parts else parts[-1])
    q = json.loads(_photo_http("https://commons.wikimedia.org/w/api.php?action=query&format=json&prop=imageinfo"
                               "&iiprop=url|mime|extmetadata&iiurlwidth={}&titles={}".format(
                                   PHOTO_PX, urllib.parse.quote(u"File:" + fname))).decode("utf-8"))
    for pg_ in q.get("query", {}).get("pages", {}).values():
        ii = (pg_.get("imageinfo") or [None])[0]
        if ii:
            ii["title"] = pg_.get("title", u"File:" + fname)
            return ii
    return None


def _photo_pick_search(search):
    """The first openly licensed JPEG photo a Commons file search for `search` finds, skipping herbarium sheets,
    drawings and maps: an imageinfo record, or None."""
    import urllib.parse
    q = json.loads(_photo_http("https://commons.wikimedia.org/w/api.php?action=query&format=json&generator=search"
                               "&gsrnamespace=6&gsrlimit=12&gsrsearch={}&prop=imageinfo&iiprop=url|mime|extmetadata"
                               "&iiurlwidth={}".format(urllib.parse.quote(search + u" filemime:image/jpeg"), PHOTO_PX)
                               ).decode("utf-8"))
    pages = sorted(q.get("query", {}).get("pages", {}).values(), key=lambda p_: p_.get("index", 99))
    for pg_ in pages:
        t = pg_.get("title", u"").lower()
        ii = (pg_.get("imageinfo") or [None])[0]
        if not ii or any(w in t for w in PHOTO_SKIP) or ii.get("mime") != "image/jpeg":
            continue
        if photo_free(_photo_meta(ii)[1]):
            ii["title"] = pg_.get("title")
            return ii
    return None


def plant_photo(key, name, article, search, photo_dir, log, state):
    """(jpeg path or None, credit or None, why not) for one plant or crop: key = file name in photo_dir, name = the
    English name the credit gives, article = English Wikipedia article, search = botanical name for the Commons
    search. Cache first, then the web (see the header of this part)."""
    meta = os.path.join(photo_dir, key + ".json")
    try:
        with open(meta, "r", encoding="utf-8") as f:
            m = json.load(f)
        p = os.path.join(photo_dir, m["file"])
        with open(p, "rb") as f:
            if jpeg_info(f.read(256 * 1024) + b"\x00" * 10):
                return p, m["credit"], None
    except Exception:
        pass
    if state.get("offline"):
        return None, None, u"offline"
    why = u"no open-licence photo found"
    try:
        os.makedirs(photo_dir, exist_ok=True)
        ii = None
        if article:
            try:
                ii = _photo_pick_lead(article)
            except Exception as ex:
                log.append(u"photo {}: lead image of {} not read ({}), Commons search next".format(key, article,
                                                                                                     type(ex).__name__))
            if ii is not None and (not photo_free(_photo_meta(ii)[1]) or ii.get("mime") not in ("image/jpeg",
                                                                                                  "image/png")):
                ii = None
        if ii is None and search:
            ii = _photo_pick_search(search)
        if ii is None:
            log.append(u"photo {}: {}".format(key, why))
            return None, None, why
        artist, lic = _photo_meta(ii)
        data = _photo_http(ii.get("thumburl") or ii["url"])
        p = os.path.join(photo_dir, key + ".jpg")
        if jpeg_info(data):
            with open(p, "wb") as f:
                f.write(data)
        else:
            tmp = os.path.join(photo_dir, key + ".src")
            with open(tmp, "wb") as f:
                f.write(data)
            if not _png_to_jpeg(tmp, p):
                return None, None, u"not a JPEG"
        fname = ii.get("title", u"").replace(u"File:", u"", 1)
        credit = u"photo {}: {}, {}, Wikimedia Commons, File:{}".format(name, artist or u"author not named", lic,
                                                                         fname)
        with open(meta, "w", encoding="utf-8") as f:
            json.dump({"file": os.path.basename(p), "credit": credit, "source": ii.get("descriptionurl", u"")}, f,
                      ensure_ascii=False)
        return p, credit, None
    except Exception as ex:
        import socket
        import urllib.error
        if isinstance(ex, (urllib.error.URLError, socket.timeout, OSError)) and not isinstance(ex,
                                                                                              urllib.error.HTTPError):
            state["offline"] = True
        log.append(u"photo {}: {}: {}".format(key, type(ex).__name__, ex))
        return None, None, u"offline" if state.get("offline") else u"not loaded"


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
