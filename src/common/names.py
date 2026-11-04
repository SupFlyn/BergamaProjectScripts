# ---- Names (round 3, A2, 31 Oct 2026; G16 / D9): every printed bridge or place name comes from data/NAMES.py ---------
#   bridge_name(code, short=False)   "K3" -> "Tabak Köprüsü" (short: "Tabak", only where the full name is in the
#                                     same drawing's key or title); unknown code -> KeyError (never print a K-code)
#   bridges_in_order()               the codes upstream first: K1, K2, K4, K3, K5, K6 (lists, keys, rulers)
#   place_name(key)                  "bank_NE" -> "Kale side · north bank", "stream" -> "Selinos stream"
#   cut_end_labels(cid)              ("W3", "W3'") the cut id + prime at its ends (D6)
#   landmark_name(key, descr=None)   round 4 (S1, G-R4-11): "kizil_avlu" -> "Kızıl Avlu"; descr=True adds the table's
#                                     English descriptor ("Kızıl Avlu · Hadrian's temple"), descr="text" adds that text;
#                                     unknown key -> KeyError (never type a landmark name locally)
#   landmark_keys()                  the landmark keys in the table
#   name_key(s)                      round 5 (S2): a name as a match key (single spaces, lower case, İ as i)
#   landmark_match(raw, p=None, r_m=60.0, near_m=150.0)   round 5 (S2, A11): the table key a survey / OSM / typed name
#                                     stands for, or None: the table name or an "alias" (whole name); a joined survey
#                                     label that starts with a table name ("Kızıl Avlu Tapınağı Mısır Tanrıları") when
#                                     p lies within near_m of the row's "at"; an "alias_near" word ("Hamam") only
#                                     within r_m of "at"
#   place_label(raw, p=None)         round 5 (S2): the table's one spelling for raw, or None when the table has no row
#                                     (the caller leaves the name out and logs it: never print an unchecked name)
#   street_label(raw)                round 5 (S2): an OpenStreetMap street name as printed: the table's spelling when
#                                     the table has the street (Kınık Caddesi ...), else the OSM tag as mapped
#   keymap_places(box=None)          round 5 (S2, G-R5-3): [(name, (x, y), key)] the table's key-map places ("at" +
#                                     "km"), best first, inside box (survey m) when given
# Needs data/NAMES.py included before it.


def bridge_name(code, short=False):
    """the one spelling of a bridge by its internal code (K1-K6, any case)"""
    row = NAMES["bridges"][str(code).strip().upper()]
    return row["short"] if short else row["name"]


def bridges_in_order():
    """the bridge codes in stream order, upstream first"""
    b = NAMES["bridges"]
    return sorted(b, key=lambda c: b[c]["order"])


def place_name(key):
    """the one spelling of a place (stream, banks, sides)"""
    return NAMES["places"][key]


def cut_end_labels(cid):
    """D6: the labels at a cut's two ends: the cut id and the id with a prime ("W3", "W3'")"""
    c = str(cid).strip()
    return c, c + u"'"


def landmark_name(key, descr=None):
    """the one (Turkish) spelling of a landmark, optionally followed by an English descriptor"""
    row = NAMES["landmarks"][str(key).strip().lower()]
    if descr is True:
        d = row.get("descr")
        if not d:
            raise KeyError(u"landmark %s has no descriptor in the names table" % key)
    else:
        d = descr or None
    return row["name"] + (u" · " + d if d else u"")


def landmark_keys():
    """the landmark keys in the names table"""
    return sorted(NAMES["landmarks"])


def name_key(s):
    """round 5 (S2): a name as a match key: single spaces, lower case, Turkish İ / I handled (İ -> i, I -> ı)"""
    s = u" ".join((s or u"").split()).replace(u"\u0130", u"i").replace(u"I", u"\u0131")
    return s.lower().replace(u"i\u0307", u"i")


def landmark_match(raw, p=None, r_m=60.0, near_m=150.0):
    """round 5 (S2, A11): the names-table key that raw (a survey label, an OSM tag, a typed literal) stands for, or
    None. Rules, in order: (1) the table name or one of its "alias" forms, whole name; (2) raw starts with the table
    name and p (survey m) lies within near_m of the row's "at" (survey labels inside one footprint are joined, e.g.
    "Kızıl Avlu Tapınağı Mısır Tanrıları"); (3) raw is one of the row's "alias_near" words and p lies within r_m of
    "at" (survey "Hamam" -> Tabaklar Hamamı)."""
    k = name_key(raw)
    if not k:
        return None
    rows = NAMES["landmarks"]
    for key, row in rows.items():
        if k == name_key(row["name"]) or k in [name_key(a) for a in row.get("alias") or ()]:
            return key

    def near(row, r):
        at = row.get("at")
        return p is not None and at is not None and (p[0] - at[0]) ** 2 + (p[1] - at[1]) ** 2 <= r * r
    for key, row in rows.items():
        nk = name_key(row["name"])
        if k.startswith(nk + u" ") and near(row, near_m):
            return key
    for key, row in rows.items():
        if k in [name_key(a) for a in row.get("alias_near") or ()] and near(row, r_m):
            return key
    return None


def place_label(raw, p=None):
    """round 5 (S2, G-R5-11): the table's one spelling for a place name, or None when the table has no row for it"""
    key = landmark_match(raw, p)
    return landmark_name(key) if key else None


def street_label(raw):
    """round 5 (S2, G-R4-11): a street name as printed: the table's spelling when the table records the street, else
    the OpenStreetMap tag as mapped (a public source, Turkish as tagged)"""
    key = landmark_match(raw)
    return landmark_name(key) if key else u" ".join((raw or u"").split())


def keymap_places(box=None):
    """round 5 (S2, G-R5-3): the places a key map may name: [(name, (x, y), key)] for every table row with "at" and
    "km", in "km" order, inside box = (x0, y0, x1, y1) survey m when given"""
    out = []
    for key, row in NAMES["landmarks"].items():
        at, rk = row.get("at"), row.get("km")
        if at is None or rk is None:
            continue
        if box is None or (box[0] <= at[0] <= box[2] and box[1] <= at[1] <= box[3]):
            out.append((rk, row["name"], (float(at[0]), float(at[1])), key))
    out.sort(key=lambda r: r[0])
    return [(n, p, k) for _, n, p, k in out]
