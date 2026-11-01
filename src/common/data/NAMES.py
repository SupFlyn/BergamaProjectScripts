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
}
