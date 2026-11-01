# ---- Names table (round 3, A2, 31 Oct 2026; G16 / D9 "real names everywhere"): ONE spelling per bridge and place ----
# Read it through ../common/names.py, never directly: include this file first, then names.py:
#   #@include ../common/data/NAMES.py
#   #@include ../common/names.py
# Plain Python data (exec'd by tools/build.py's bergama_data): no imports, no functions, one assignment.
# K-codes stay internal keys only: never printed as a main label. Stream order (upstream first) = "order".
# Spellings (plan_findings/NAMES_SQUIGGLE_TREES.md DATA-3; chosen: the official public name = the bus stop name):
#   K3 Tabak Köprüsü        Kültür Envanteri "Tabak Köprüsü" (library/research/selinos_site_history_inaccessible_edges_v1.md
#                           l.62); survey label "Tabakhane Köprüsü" is the same bridge (selinos_bergama_history_context_v1.md l.143)
#   K4 Ulucami Önü Köprüsü  KGM plaque on site, photo IMG_5804 (inaccessible_edges_v1.md l.217); history_context_v1.md l.141
#   K5 Üç Kemer Köprüsü     Visit İzmir (İzmir BB), Destinasyon 10228 (history_context_v1.md l.270)
#   K6 road bridge          Adnan Menderes Bulvarı (Aras 1 Nov 07:30: "it is bulvar"; inaccessible_edges_v1.md l.176 has "Cd."); no proper name found
#   K1, K2                  no source name: descriptive names (G16)
# Chainage m along the stream: CL code.py:211 (K1 / K2 about 25 m apart upstream; their order unverified).
# Banks (D6, Aras 31 Oct 20:45: "fine that way"; p20 already prints them): NE = left bank looking downstream = north
# bank = the Kale side; SW = south bank = the bazaar side.
# Landmarks (round 4, S1, 1 Nov 2026; G-R4-11 / PALL.3, PLAN §4.6): the TURKISH proper name is printed, never an
# English translation ("Red Hall" -> Kızıl Avlu, "Acropolis" -> Akropol, "Bazaar" -> Arasta); "descr" is an optional
# English descriptor that may FOLLOW the name (landmark_name(key, descr=True) -> "Kızıl Avlu · Hadrian's temple").
# Spellings as the project's sources write them; "src" = where (h01 = library/research/
# selinos_bergama_history_context_v1.md, table §5 row; survey = a label in the course survey). Descriptors are taken
# from texts already in the booklet (p20 heritage cards, city link), nothing new. One spelling of Ulucami (the brief's;
# "Ulu Cami" / "Ulu Camii" drift removed); source TITLES on the Sources page stay as published.
NAMES = {
    "bridges": {
        "K1": {"name": u"side inlet crossing", "short": u"side inlet crossing", "order": 1, "proper": False},
        "K2": {"name": u"small crossing", "short": u"small crossing", "order": 2, "proper": False},
        "K4": {"name": u"Ulucami Önü Köprüsü", "short": u"Ulucami Önü", "order": 3, "proper": True, "chainage_m": 467},
        "K3": {"name": u"Tabak Köprüsü", "short": u"Tabak", "order": 4, "proper": True, "chainage_m": 709},
        "K5": {"name": u"Üç Kemer Köprüsü", "short": u"Üç Kemer", "order": 5, "proper": True, "chainage_m": 1126},
        "K6": {"name": u"Adnan Menderes Bulvarı road bridge", "short": u"road bridge", "order": 6, "proper": False,
               "chainage_m": 1767},
    },
    "places": {
        "stream": u"Selinos stream",
        "bank_NE": u"Kale side · north bank",
        "bank_SW": u"bazaar side · south bank",
        "bank_NE_short": u"north bank",
        "bank_SW_short": u"south bank",
        "side_NE": u"Kale side",
        "side_SW": u"bazaar side",
    },
    "landmarks": {
        "kizil_avlu": {"name": u"Kızıl Avlu", "descr": u"Hadrian's temple",
                       "src": u"survey label 'Kızıl Avlu' (30203.92, 31974.82); h01 §5 P02; Kültür Envanteri 'Kızıl Avlu'"},
        "akropol": {"name": u"Akropol", "descr": u"the Hellenistic city on the hill",
                    "src": u"site board HER_BEYOND (OSM way 1410335587, Trajaneum)"},
        "ulucami": {"name": u"Ulucami", "descr": u"mosque of 1398-99",
                    "src": u"h01 §5 P05 (survey 'Ulu Camii' (29844.2, 32313.3)); Visit İzmir 'Bergama Ulu (Yıldırım) "
                           u"Mosque'; spelling = the brief's (G-R4-11) and K4's name"},
        "tabaklar_hamami": {"name": u"Tabaklar Hamamı", "descr": u"the tanners' bath",
                            "src": u"h01 §5 P07 (survey 'Hamam' (29890.4, 32243.6))"},
        "arasta": {"name": u"Arasta", "descr": u"the old bazaar",
                   "src": u"site board HER_STOPS 'bazaar' (Visit İzmir 'Mevlâna Hacı Hekim Hammam')"},
        "cizmeciler_arastasi": {"name": u"Çizmeciler Arastası", "descr": None,
                                "src": u"survey label (29794.31, 31929.85)"},
        "pabuccular_arastasi": {"name": u"Pabuççular Arastası", "descr": None, "src": u"h02 s32 (city link stop 1)"},
        "istiklal_meydani": {"name": u"İstiklal Meydanı", "descr": u"square",
                             "src": u"h01 §5 P16 (survey label (29990.0, 32030.5))"},
        "adnan_menderes_bulvari": {"name": u"Adnan Menderes Bulvarı", "descr": None,
                                   "src": u"Aras 1 Nov 07:30 ('it is bulvar'); K6 row above"},
        "kinik_caddesi": {"name": u"Kınık Caddesi", "descr": None,
                          "src": u"OpenStreetMap extract of 28 Jul 2026 (common/city_spine.py MAIN_SPINE)"},
        "bankalar_caddesi": {"name": u"Bankalar Caddesi", "descr": None,
                             "src": u"OpenStreetMap extract of 28 Jul 2026 (common/city_spine.py MAIN_SPINE)"},
        "bergama_muzesi": {"name": u"Bergama Müzesi", "descr": u"museum of 1936",
                           "src": u"Kültür Envanteri KE 3946 'Bergama Müzesi' (h01 s86)"},
        "teleferik": {"name": u"Teleferik", "descr": u"cable car (2010)",
                      "src": u"site board HER_STOPS 'gondola' (OSM node 2295928011)"},
        "asklepion": {"name": u"Asklepion", "descr": u"the healing sanctuary",
                      "src": u"h01 §5 P28; KTB 'The Archaeological Site of Asklepion' (h01 s114)"},
    },
}
