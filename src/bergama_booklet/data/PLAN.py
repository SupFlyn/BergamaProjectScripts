# ---- BOOKLET PLAN (page order, page titles, key statements, which asset goes in which frame) ----
# One place for page-level text = no repetition. Asset keys are "<script output folder>/<block id>": the block comes from
# that script's output/<folder>/booklet/blocks.json. {src:key} marks become [n] (one numbering for the booklet).
BOOK = dict(
    title=u"From stream corridor to hydrological commons",
    subtitle=u"Selinos stream edge, Bergama",
    project=u"SELİNOS STREAM EDGE · BERGAMA",
    group_line=u"ARCH 4410 Architectural Design Studio V · Group 6",
    course=u"Yaşar University · ARCH 4410 Architectural Design Studio V · 2026-2027 Fall",
    names=[u"Aras Özkaymakcı", u"Begüm Arslan", u"Nil Çetin"],
    date=u"October 2026",
)

PARTS = {"A": u"Site as it is", "B": u"Water", "C": u"Proposal"}

# frames on the 12-column x 4-row grid: (first column, last column, first row, last row)
TEMPLATES = {
    "map":      {"side": (1, 3, 1, 4), "hero": (4, 12, 1, 4)},
    "map_r":    {"hero": (1, 9, 1, 4), "side": (10, 12, 1, 4)},
    "two":      {"a": (1, 6, 1, 3), "b": (7, 12, 1, 3), "strip": (1, 12, 4, 4)},
    "three":    {"a": (1, 4, 1, 3), "b": (5, 8, 1, 3), "c": (9, 12, 1, 3), "strip": (1, 12, 4, 4)},
    "sections": {"s1": (1, 12, 1, 1), "s2": (1, 12, 2, 2), "s3": (1, 12, 3, 3), "s4": (1, 12, 4, 4)},
    "sections2": {"s1": (1, 12, 1, 2), "s2": (1, 12, 3, 4)},
    "grid8":    dict(("g%d" % (i + 1), (1 + 3 * (i % 4), 3 + 3 * (i % 4), 1 + 2 * (i // 4), 2 + 2 * (i // 4))) for i in range(8)),
    "tiles":    {"strip": (1, 12, 1, 1), "hero": (1, 8, 2, 4), "side": (9, 12, 2, 4)},
    "full":     {"hero": (1, 12, 1, 4)},
}

SCRIPT_OF = {   # output folder -> script, named on placeholders and in the log
    "selinus_board": u"selinus_board (MainBoard)",
    "bergama_water_board": u"bergama_water_board (WaterBoard)",
    "Bergama_water_balance_analysis": u"bergama_water_balance (WaterBalance)",
    "bergama_masterplan": u"bergama_masterplan (MasterPlan)",
    "Bergama_city_link_analysis": u"bergama_city_link (CityLink)",
    "Bergama_agriculture_alternatives": u"bergama_agriculture_alternatives (AgriCulture)",
    "bergama_proposal_sections": u"bergama_proposal_sections (ProposalSections)",
}

PLAN_SOURCES = {}   # sources used by page-level text below (scripts bring their own in blocks.json)

PLAN = [
    # ---------------- A  SITE AS IT IS
    dict(id="A1", part="A", template="map", title=u"What is there",
         statement=u"",
         slots={"side": "selinus_board/a1_side", "hero": "selinus_board/plan01"}),
    dict(id="A2", part="A", template="grid8", title=u"Layers of the site",
         statement=u"",
         slots=dict(("g%d" % i, "selinus_board/d%d" % i) for i in range(1, 9))),
    dict(id="A3", part="A", template="map_r", title=u"How people use it",
         statement=u"",
         slots={"hero": "selinus_board/plan07", "side": "selinus_board/a3_side"}),
    dict(id="A4", part="A", template="sections", title=u"The stream edge in section",
         statement=u"",
         slots={"s1": "selinus_board/t1", "s2": "selinus_board/t2", "s3": "selinus_board/t3", "s4": "selinus_board/t4"}),
    dict(id="A5", part="A", template="sections", title=u"The stream edge in section",
         statement=u"",
         slots={"s1": "selinus_board/t5", "s2": "selinus_board/t6", "s3": "selinus_board/t7", "s4": "selinus_board/s1_axo"}),
    dict(id="A6", part="A", template="tiles", title=u"Comfort through the year",
         statement=u"",
         slots={"strip": "selinus_board/climate_tiles", "hero": "selinus_board/t8_utci", "side": "selinus_board/a6_side"}),
    # ---------------- B  WATER
    dict(id="B1", part="B", template="tiles", title=u"The year of the water",
         statement=u"",
         slots={"strip": "bergama_water_board/w1_tiles", "hero": "bergama_water_board/w1_year", "side": "bergama_water_board/w1_side"}),
    dict(id="B2", part="B", template="sections2", title=u"River height at the surveyed cuts",
         statement=u"",
         slots={"s1": "bergama_water_board/w2a_cuts", "s2": "bergama_water_board/w2b_s4"}),
    dict(id="B3", part="B", template="tiles", title=u"How much water to hold",
         statement=u"",
         slots={"strip": "Bergama_water_balance_analysis/tiles", "hero": "Bergama_water_balance_analysis/balance_chart",
                "side": "bergama_water_board/w4_cubes"}),
    dict(id="B4", part="B", template="three", title=u"Collect, clean, hold",
         statement=u"",
         slots={"a": "bergama_water_board/chain", "b": "bergama_water_board/w6_cleaning", "c": "bergama_water_board/w3b_planting",
                "strip": "bergama_water_board/w7_destination"}),
    # ---------------- C  PROPOSAL
    dict(id="C1", part="C", template="full", title=u"Masterplan",
         statement=u"",
         slots={"hero": "bergama_masterplan/whole_site"}),
    dict(id="C2", part="C", template="map", title=u"Masterplan: the water edge",
         statement=u"",
         slots={"side": "bergama_masterplan/zoom_side", "hero": "bergama_masterplan/zoom_1000"}),
    dict(id="C3", part="C", template="map_r", title=u"Connection to the city",
         statement=u"",
         slots={"hero": "Bergama_city_link_analysis/spine_plan", "side": "Bergama_city_link_analysis/stops"}),
    dict(id="C4", part="C", template="two", title=u"Water for the farmland",
         statement=u"",
         slots={"a": "Bergama_agriculture_alternatives/alt1", "b": "Bergama_agriculture_alternatives/alt3",
                "strip": "Bergama_agriculture_alternatives/tiles"}),
    dict(id="C5", part="C", template="sections2", title=u"Proposal sections",
         statement=u"",
         slots={"s1": "bergama_proposal_sections/p1_upstream", "s2": "bergama_proposal_sections/p2_k4"}),
    dict(id="C6", part="C", template="sections2", title=u"Proposal sections",
         statement=u"",
         slots={"s1": "bergama_proposal_sections/p3_k5", "s2": "bergama_proposal_sections/p4_downstream"}),
    dict(id="C7", part="C", template="tiles", title=u"Four seasons",
         statement=u"",
         slots={"strip": "bergama_water_board/season_tiles", "hero": "bergama_water_board/season_matrix",
                "side": "bergama_water_board/season_side"}),
]
