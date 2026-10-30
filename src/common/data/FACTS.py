# ---- Shared facts (H-B 30 Oct 2026, M10): every value printed on more than one page, or printed on one page and
# used by another, has ONE row here. Read it through ../common/facts.py, never directly:
#   #@include ../common/data/FACTS.py
#   #@include ../common/facts.py
# Plain Python data (exec'd into globals by tools/build.py's bergama_data): no imports, no functions, one assignment.
#
# ROW: key -> dict
#   kind        "live" = read on every run from another script's results file (never typed here; no fallback: a
#               missing file gives None and the page prints nothing for it) | "static" = a sourced constant |
#               "derived" = computed from another row (of)
#   file        live: "water_balance" (water_balance_results.json, facts.py FACT_FILES)
#   path        live: the keys into that JSON
#   conv        None | "drip_m3_ha" (net mm / drip efficiency x 10 = m³ per ha at the intake) | "ha_per_10000" (10,000 /
#               value) | "ratio" (value[0] / value[1])
#   value       static: the value (a number, or a tuple for parts that are summed / divided by conv)
#   round       the step the printed value is rounded to (10 -> 8,000; 1 -> 8,705); nd = decimals instead
#   unit, note  printed after the number ("m³ per ha", "(1-in-5 dry year)")
#   ref         the source (internal wording; print only "public")
#   public      the citation a page may print (Sources page), None when not public
#   printed_on  the ONE booklet page that prints the fact (G4 "a fact appears once"); used_by = pages that use the
#               value without printing it (or print it only as part of a derived line)
FACTS = {
    # ---- olive water need: water board OLIVE_M3_HA = FAO-56 net dry5 / drip efficiency (water_board code.py 1519,
    # printed 8,001) and agriculture gross normal..dry (code.py 812, printed 6,830-8,000): same quantity, one rounding (T1)
    "olive_need_m3_ha": dict(
        kind="live", file="water_balance", path=("net_irrigation_mm", "olive", "dry5"), conv="drip_m3_ha",
        round=10, unit=u"m³ per ha", note=u"(1-in-5 dry year)",
        ref=u"FAO-56 soil water balance for Bergama, 34 water years (water balance results, net irrigation olive dry5); "
            u"drip efficiency 90 % (FAO Training Manual 4 ch. 3)",
        public=u"Allen et al. 1998, FAO Irrigation and Drainage Paper 56",
        printed_on="18", used_by=["19"]),
    "olive_need_normal_m3_ha": dict(
        kind="live", file="water_balance", path=("net_irrigation_mm", "olive", "mean"), conv="drip_m3_ha",
        round=10, unit=u"m³ per ha", note=u"(normal year)",
        ref=u"as olive_need_m3_ha, mean year", public=u"Allen et al. 1998, FAO Irrigation and Drainage Paper 56",
        printed_on="19", used_by=[]),
    "olive_ha_per_10000_m3": dict(
        kind="derived", of="olive_need_m3_ha", conv="ha_per_10000", nd=2, unit=u"ha", note=u"of olives per 10,000 m³",
        ref=u"10,000 m³ / olive_need_m3_ha (unrounded)", public=None,
        printed_on="18", used_by=["19"]),
    # ---- lands the water balance serves (water_balance LANDS: around2.pdf farm extent, ESA WorldCover 2021)
    "cropland_ha": dict(
        kind="live", file="water_balance", path=("lands", "cropland_ha"), conv=None, nd=1, unit=u"ha",
        note=u"fields", ref=u"around2.pdf farm extent, ESA WorldCover 2021 cropland (water balance LANDS)",
        public=u"ESA WorldCover 2021", printed_on="9", used_by=["10"]),
    "orchard_ha": dict(
        kind="live", file="water_balance", path=("lands", "orchard_ha"), conv=None, nd=2, unit=u"ha",
        note=u"olive grove", ref=u"orchards within 35 m of survey olive/fruit symbols (water balance LANDS)",
        public=None, printed_on="9", used_by=["10"]),
    # ---- storage (live from the water balance; PLAN T1: never typed)
    "storage_m3": dict(
        kind="live", file="water_balance", path=("design", "central_range_m3"), conv=None, round=1000,
        unit=u"m³", note=u"", ref=u"water balance results, design central range (sequent peak, cost cut-off)",
        public=None, printed_on="10", used_by=["11", "18"]),
    # ---- groundwater (water board AQUIFER, DECISION; research/water_data/03 rows 17 and 19)
    "aquifer_use_ratio": dict(
        kind="static", value=(198.01, 45.4), conv="ratio", nd=1, unit=u"×", note=u"its potential",
        ref=u"Lower Bakırçay: total water use 198.01 hm³ (Tablo 4.3 p.31) / groundwater potential 45.4 hm³ (Tablo 5.3 "
            u"p.36), Kuzey Ege Kuraklık Yönetim Planı 2018 (S10)",
        public=u"Kuzey Ege Havzası Kuraklık Yönetim Planı, 2018", printed_on="18", used_by=["19"]),
    "arsenic_ug_l": dict(
        kind="static", value=10, conv=None, round=1, unit=u"µg/L", note=u"arsenic above (not for drinking)",
        ref=u"Somay & Gemici 2015 (DATA_REGISTER EN-E3)", public=u"Somay & Gemici 2015",
        printed_on="18", used_by=[]),
    # ---- olive area in Bergama: TÜİK 2025, 65,978 + 21,068 da (agriculture code.py 536) = 8,704.6 ha (PLAN T1)
    "olive_area_ha": dict(
        kind="static", value=(65978.0, 21068.0), conv="da_sum_ha", round=1, unit=u"ha", note=u"of olives in Bergama",
        ref=u"TÜİK 2025 district crop areas, MEDAS export (library/research/crops_2026-10-24/"
            u"bergama_crops_irrigation_v1.md §1.25)",
        public=u"TÜİK, Bitkisel Üretim İstatistikleri 2025", printed_on="19", used_by=[]),
    # ---- constants used by the conversions (sourced)
    "drip_efficiency": dict(
        kind="static", value=0.90, conv=None, nd=2, unit=u"", note=u"",
        ref=u"water balance v2 DRIP_EFF (FAO Training Manual 4 ch. 3)", public=None, printed_on=None, used_by=["18", "19"]),
}
