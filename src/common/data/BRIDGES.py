# ---- Bridges over the Selinos for the sections (round 5, S3, D8 / G-R5-4.7 / N4 a / A15; 1 Nov 2026) ---------------
# Read it through ../common/bridges.py, never directly: include this file first, then bridges.py:
#   #@include ../common/data/BRIDGES.py
#   #@include ../common/bridges.py
# Plain Python data (exec'd into globals by tools/build.py's bergama_data): no imports, no functions, one assignment.
#
# POSITION (N4 a, Aras 1 Nov 22:44): the bridge-list point, survey m = site board / masterplan BRIDGES_K = CONCEPT_RECORD
# 2.1 (src/selinus_board/parts/14_tsec_wind_arrows.py:861-863, src/bergama_masterplan/parts/02c_corridor.py:85-86).
# The bank-depth chainages (K4 5,965, Üç Kemer 6,560) are NOT used for positions (CHK-8 §8.4 conflict, settled by N4).
# Printed names: common/data/NAMES.py through bridge_name(key) (G16), never the K-code.
#
# FACTS: only sourced values; every value a {value, src} dict; a part with no source is absent (the drawing rule that
# replaces it lives in bridges.py BR_RULE and is logged as FLAG, A15). Sources:
#   s204/s205 Visit İzmir (İzmir Büyükşehir) Üç Kemer text: "Büyük kemer; nehir yatağından kemer kilit taşına kadar 10
#       metre yüksekliğinde, kemer genişliği ise 9,60 m'dir." "Köprünün tabyası 4,50 m genişliğinde ve 56,40 m
#       uzunluğundadır." "Köprü; iki ayak üzerine, üç adet yuvarlak kemer atılarak, üç gözlü olarak yapılmıştır."
#       -> research/bank_depth_2026-10-28/outside_research_v1/selinos_bank_depth_v1/REPORT.md:137-146
#   s207 Visit İzmir "Ulu Mosque Bridge": "the big eye of the Bridge has a rounded eye, and the smaller eye has a more
#       pointed arch." No dimensions. -> same REPORT.md:100-106
#   IMG_5814 photo-scaled (1 Oct 2026 site photos, checked with a 75 cm traffic cone): "K4 parapet top to bed
#       7.4-8.6 m" -> research/bank_depth_2026-10-28/REPORT.md:24 (row K4)
#   Tabak: "iki gözlü bir köprüdür" (two openings; Bergama Belediyesi Alan Başkanlığı); no sizes
#       -> research/library_recheck/06_heritage_stream_place.md:34; NOT_FOUND.md:15-16
#   K1, K2, K6: no elevation data at all (CHK-8 §8.3).
BRIDGES = {
    "K1": {"xy": (29628.35, 32630.87), "form": "deck", "openings": None, "facts": {}},
    "K2": {"xy": (29604.93, 32622.02), "form": "deck", "openings": None, "facts": {}},
    "K3": {"xy": (30037.01, 32121.57), "form": "arches", "openings": {"value": 2, "src": "Tabak: iki gözlü (library_recheck/06:34)"},
           "facts": {}},
    "K4": {"xy": (29846.40, 32277.71), "form": "arches",
           "openings": {"value": 2, "src": "s207: big eye rounded, smaller eye more pointed"},
           "eyes": ("round", "pointed"),
           "facts": {"parapet_above_bed_m": {"value": (7.4, 8.6), "src": "IMG_5814 photo-scaled (bank_depth REPORT.md:24)"}}},
    "K5": {"xy": (30293.63, 31792.25), "form": "arches",
           "openings": {"value": 3, "src": "s204: three round arches on two piers"},
           "eyes": ("round", "round", "round"),
           "facts": {"mid_span_m": {"value": 9.60, "src": "s204/s205 Visit İzmir"},
                     "keystone_above_bed_m": {"value": 10.0, "src": "s204/s205 Visit İzmir"},
                     "deck_w_m": {"value": 4.50, "src": "s204/s205 Visit İzmir"},
                     "deck_l_m": {"value": 56.40, "src": "s204/s205 Visit İzmir"}}},
    "K6": {"xy": (30646.94, 31251.65), "form": "deck", "openings": None, "facts": {}},
}
