# Built-in data of bergama_booklet (made by tools/build.py from src/bergama_booklet/data/; do not edit by hand)

#@@ PLAN
# ---- BOOKLET PLAN v3 (Aras 26 Oct 06:02: "sheet pages, split to 5 pt") ----
# Every page is the scripts' OWN sheet: an A3 sheet goes in as it is; a panel of a big sheet is cut out with its own
# words and shown at ONE scale per page (never stretched, nothing rewritten). Keys "<output folder>/<crop id>" name
# the crop blocks in that script's output/<folder>/booklet/blocks.json; "/1" ... "/n" after a key = one of the n
# pieces the panel is divided into ("split": (columns, rows)) so its words stay about 5 pt or more.
BOOK = dict(
    hook=u"MIRAQUA",                      # project name, picked by Aras 25 Oct 20:29 (mirage + aqua)
    title=u"From stream corridor to hydrological commons",
    subtitle=u"Selinos stream edge, Bergama",
    project=u"MIRAQUA · SELİNOS STREAM · BERGAMA",
    group_line=u"ARCH 4410 Architectural Design Studio V · Group 6",
    course=u"Yaşar University · ARCH 4410 Architectural Design Studio V · 2026-2027 Fall",
    names=[u"Aras Özkaymakcı", u"Begüm Arslan", u"Nil Çetin"],
    date=u"October 2026",
)

PARTS = {"A": u"Site as it is", "B": u"Water", "C": u"Proposal"}

SCRIPT_OF = {   # output folder -> script, named on placeholders, the sources page and in the log
    "selinus_board": u"Site board",
    "bergama_water_board": u"Water board",
    "Bergama_water_balance_analysis": u"Water balance",
    "bergama_masterplan": u"Masterplan",
    "Bergama_city_link_analysis": u"City link",
    "Bergama_agriculture_alternatives": u"Agriculture alternatives",
    "bergama_proposal_sections": u"Proposal sections",
}

SB, WB, BAL = "selinus_board/", "bergama_water_board/", "Bergama_water_balance_analysis/"
MP, CLK, AG, PS = "bergama_masterplan/", "Bergama_city_link_analysis/", "Bergama_agriculture_alternatives/", \
    "bergama_proposal_sections/"

# sheet = a whole A3 sheet page as it is; rows = panels side by side, rows stacked, one scale for the page
PAGES = [
    dict(part="A", title=u"What is there", rows=[[SB + "drw_plan01"]]),
    dict(part="A", title=u"What is there: the stream through the town", rows=[[SB + "drw_plan01"]], split=(2, 3),
         keep=(3, 4)),                                   # the two middle pieces: the town and the stream
    dict(part="A", title=u"Heights and enclosure", sheet=SB + "Selinus_01_what_is_there_axonometric.pdf"),
    dict(part="A", title=u"Grain of the town", rows=[[SB + "drw_building_types"],
                                                    [SB + "drw_key_question", SB + "drw_ground_cover"],
                                                    [SB + "drw_shops_vs_walking"]]),
    dict(part="A", title=u"The stream edge", rows=[[SB + "drw_tree_cover"], [SB + "drw_photos/1"],
                                                  [SB + "drw_photos/2"]], pieces={SB + "drw_photos": 2}),
    dict(part="A", title=u"How people use it", rows=[[SB + "drw_movement"],
                                                    [SB + "drw_walking_today", SB + "drw_driving_today"],
                                                    [SB + "drw_walking_change", SB + "drw_driving_change"],
                                                    [SB + "drw_combined_change"]]),
    dict(part="A", title=u"Sections across the stream", rows=[[SB + "sec_section_s1"], [SB + "sec_section_s2"]], optional=True),
    dict(part="A", title=u"Sections across the stream", rows=[[SB + "sec_section_s3"], [SB + "sec_section_s4"]], optional=True),
    dict(part="A", title=u"Sections across the stream", rows=[[SB + "sec_section_s5"]], optional=True),
    dict(part="A", title=u"Shops meet the stream where it is hidden", sheet=CLK + "Bergama_city_link_A3.pdf", page=0),
    dict(part="B", title=u"The water balance", sheet=BAL + "Bergama_water_balance_A3.pdf"),
    dict(part="B", title=u"The year of the water", rows=[[WB + "wb_year"]]),
    dict(part="B", title=u"How high the stream rises", rows=[[WB + "wb_cuts"]]),
    dict(part="B", title=u"Collect, clean, hold", rows=[[WB + "wb_chain/1"], [WB + "wb_chain/2"], [WB + "wb_chain/3"],
                                                       [WB + "wb_cleaning"]], pieces={WB + "wb_chain": 3}),
    dict(part="B", title=u"How much water to hold", rows=[[WB + "wb_storage"]]),
    dict(part="C", title=u"Masterplan: upstream", rows=[[MP + "mp_upstream"]]),
    dict(part="C", title=u"Masterplan: downstream", rows=[[MP + "mp_downstream"]]),
    dict(part="C", title=u"The water edge at 1:1,000", rows=[[MP + "dt_upstream", MP + "dt_k5"]]),
    dict(part="C", title=u"The spine, stop by stop", sheet=CLK + "Bergama_city_link_A3.pdf", page=1),
    dict(part="C", title=u"Long section along the spine", rows=[[SB + "sec_spine/1"], [SB + "sec_spine/2"]],
         pieces={SB + "sec_spine": 2}),
    dict(part="C", title=u"Upstream entry: collect, clean and hold", rows=[[PS + "ps_upstream"]]),
    dict(part="C", title=u"K4 bridge: the amphibious threshold", rows=[[PS + "ps_k4"]]),
    dict(part="C", title=u"K5 bridge: Demeter's Garden", rows=[[PS + "ps_k5"]]),
    dict(part="C", title=u"Downstream reach: give back", rows=[[PS + "ps_downstream"]]),
    dict(part="C", title=u"Four seasons on one cut", rows=[[WB + "wb_s4_winter"], [WB + "wb_s4_spring"],
                                                          [WB + "wb_s4_summer"], [WB + "wb_s4_autumn"]]),
    dict(part="C", title=u"The S4 cut, north-east bank", rows=[[WB + "wb_s4_ne"]]),
    dict(part="C", title=u"Planting bands by days under water", rows=[[WB + "wb_bands/1"], [WB + "wb_bands/2"]],
         pieces={WB + "wb_bands": 2}),
    dict(part="C", title=u"Species by planting band", rows=[[WB + "wb_species/1"], [WB + "wb_species/2"]],
         pieces={WB + "wb_species": 2}),
    dict(part="C", title=u"Where the clean water goes", rows=[[WB + "wb_farms"], [WB + "wb_decision/1"],
                                                             [WB + "wb_decision/2"], [WB + "wb_decision/3"]],
         pieces={WB + "wb_decision": 3}),
    dict(part="C", title=u"What each cubic metre grows", sheet=AG + "Bergama_agriculture_alternatives_A3.pdf", page=0),
    dict(part="C", title=u"The farms we feed", sheet=AG + "Bergama_agriculture_alternatives_A3.pdf", page=1),
    dict(part="C", title=u"Plants by days under water", sheet=AG + "Bergama_agriculture_alternatives_A3.pdf", page=2),
]

# the sheets whose own "Sources by number" keys the [n] marks on these pages refer to (sources page, in this order)
SOURCE_SHEETS = [SB + "Selinus_drawings.pdf", SB + "Selinus_01_what_is_there_axonometric.pdf",
                 CLK + "Bergama_city_link_A3.pdf", BAL + "Bergama_water_balance_A3.pdf",
                 WB + "Bergama_water_board_*.pdf", MP + "Bergama_masterplan_*_A.pdf",
                 PS + "Bergama_proposal_sections_A.pdf", AG + "Bergama_agriculture_alternatives_A3.pdf"]
