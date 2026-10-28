SPECIES = [  # v1.14 (Aras 27 Oct: "keep only the plants we use most or that are most beneficial"): the nine kept.
    # (band, plant key in PLANTS (src/common/plant_photos.py: the printed name "English (Turkish)", v3, Aras 27 Oct
    #  17:34: "English first, Turkish in brackets, no Latin", and the photo), where (pictogram, keywords), why
    #  [(pictogram, keywords)], their sources, warning). Evidence as in v1.13's list (concept v1 §9.2, research 04) and
    #  DATA_REGISTER PL rows. v4 (MIRAQUA 28 Oct, P16.2): the keywords of where and why in **bold**
    ("E", u"plane", ("tree", u"**dry hub squares** K3 · K4 · K5"),
     [("tree", u"summer **shade** on the hub squares"), ("drop", u"**drought-sensitive**: watered from storage")],
     u"D8 (history_phase1/DECISIONS.md): Ottoman squares with plane trees (ICOMOS, h02 s13 p281); h03 Q4: "
     u"drought-sensitive mesophyte along perennial streams; " + REG + u" PL-13, PL-14", u""),
    ("F", u"olive", ("olive", u"**dry top** · Demeter's Garden K5"),
     [("dry", u"**drought-resistant** · no waterlogging"), ("olive", u"Red Hall: 19th-c. **olive-oil mill**")],
     REG + u" PL-12 (FAO Ecocrop); h02 §1.6: olive-oil machinery in the Red Hall south rotunda, 19th c. (s25)", u""),
    ("F", u"lavender", ("lav", u"**dry top** · above Q500"),
     [("dry", u"**xerophyte** · fast-draining soil"), ("flood", u"17 days flooded: **survived**")],
     u"RHS trial; " + REG + u" PL-11 (RHS)", u"scent layer"),
    ("C", u"tamarisk", ("tree", u"**flood terraces**"),
     [("flood", u"**long inundation** (genus)"), ("native", u"**native** · İzmir")],
     u"JRC Atlas 'can survive prolonged periods of inundation'; " + REG + u" PL-01, PL-10", u""),
    ("C", u"chaste", ("tree", u"**flood terraces**"),
     [("dry", u"**intermittent streams**"), ("native", u"**native** · honey plant")],
     u"Salinas & Cueto 2009; " + REG + u" PL-02, PL-19", u"aromatic"),
    ("C", u"willow", ("tree", u"**willow band** · 50-150 d"),
     [("flood", u"**inundation-tolerant**"), ("clean", u"**cleans** riverbanks")],
     u"JRC Atlas 'noticeably tolerant to inundation'; " + REG + u" PL-17 (phytoremediation of riverbanks); RWS 2023",
     u""),
    ("B", u"reed", ("reed", u"**reed beds** · bed edge"),
     [("clean", u"reed beds: **NH4-N 58-88 %**"), ("flood", u"0.70 m standing water: **dies**")],
     u"Korkusuz et al. 2004 (" + REG + u" PL-09); Song 2021 (PL-06)", u"spreads"),
    ("B", u"iris", ("reed", u"**bed edge**, not where people touch"),
     [("flood", u"**flooded** up to 6 months"), ("clean", u"takes up **N and P**")],
     u"FEIS; " + REG + u" PL-20, PL-21", u"POISONOUS"),
    ("B", u"mint", ("reed", u"**reed beds** · upstream entry"),
     [("clean", u"**COD 71-91 %** removed"), ("clean", u"**microbes > 80 %** removed")],
     u"HSSF wetland, Avelar 2012; " + REG + u" PL-22", u"aromatic"),
]
SPECIES_REMOVE = (u"giant_reed", u"**remove**: raises **flood risk**, blocks the channel",   # v3: (plant key, words, source)
                  u"Bruno et al. 2019 'increased flooding risk'; " + REG + u" PL-25")
