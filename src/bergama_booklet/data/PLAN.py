# ---- BOOKLET PLAN v10 (Aras 27 Oct 11:07 review: page list above each entry); v9 (Aras 27 Oct 06:20: proposal sections always two to a page); v8 (Aras 26 Oct 08:27-08:28: masterplan halves on one page; long section along the spine left out, it
# repeated the "What is there" map); v7 (review R7: no half-empty pages: "alone" = the two rows share a page only if both stay >= 3/4
# of their own-page size, else each gets its own page under these titles); v5 (review 26 Oct 07:06: p.07 edge plan, all cuts on <= 2 pages); v4 (Aras 26 Oct 06:02 "sheet pages"; 06:35: never divide a drawing, each drawing once) ----
# Every page is the scripts' OWN sheet: an A3 sheet goes in as it is; a panel of a big sheet is cut out with its own
# words and shown at ONE scale per page (never stretched, nothing rewritten). Keys "<output folder>/<crop id>" name
# the crop blocks in that script's output/<folder>/booklet/blocks.json; every panel goes on its page whole.
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
    dict(part="A", title=u"Heights and enclosure", sheet=SB + "Selinus_01_what_is_there_axonometric.pdf"),
    # v10 (Aras 27 Oct 11:07): building types moved into the sections (board v44), the small map at the bottom out
    dict(part="A", title=u"Grain of the town", rows=[[SB + "drw_key_question", SB + "drw_ground_cover"]]),
    # v10: the edge map alone and large, its edge-type shares inside the same crop; photos with captions on their own page
    dict(part="A", title=u"The stream edge", rows=[[SB + "drw_edge_plan"]]),
    dict(part="A", title=u"Along the stream", rows=[[SB + "drw_photos"]]),
    # v10: the large map + walking / driving today (key roads only); change maps gone
    dict(part="A", title=u"How people use it", rows=[[SB + "drw_movement"],
                                                    [SB + "drw_walking_today", SB + "drw_driving_today"]]),
    # v10: proposal map (from the masterplan's movement), commercial spine (board v19-v32.1, restored), heritage loop
    dict(part="A", title=u"How people will move", rows=[[SB + "drw_proposal"],
                                                       [SB + "drw_commercial_spine", SB + "drw_heritage_loop"]]),
    dict(part="A", title=u"Sections across the stream", rows=[[SB + "sec_sections_1"]], optional=True),
    dict(part="A", title=u"Sections across the stream", rows=[[SB + "sec_sections_2"]], optional=True),
    dict(part="A", title=u"Shops meet the stream where it is hidden", sheet=CLK + "Bergama_city_link_A3.pdf", page=0),
    dict(part="B", title=u"The water balance", sheet=BAL + "Bergama_water_balance_A3.pdf"),
    # v10: old p11-14 condensed to two pages (water board v1.14)
    dict(part="B", title=u"How the stream behaves", rows=[[WB + "wb_water"]]),
    dict(part="B", title=u"Collect, clean, hold", rows=[[WB + "wb_system"]]),
    # v10: masterplan redo (v24): halves stacked at 1:5,000; close-scale plan + maximum potential area proof
    dict(part="C", title=u"Masterplan: an ecological corridor", rows=[[MP + "mp_upstream"], [MP + "mp_downstream"]]),
    # v10.1: the numbered notes the masterplan halves had no room for (only when masterplan v24.1+ writes mp_notes)
    dict(part="C", title=u"Why each place", rows=[[MP + "mp_notes"]], optional=True),
    dict(part="C", title=u"The water edge at 1:1,000", rows=[[MP + "dt_upstream", MP + "dt_k5"], [MP + "mp_max_area"]]),
    dict(part="C", title=u"The spine, stop by stop", sheet=CLK + "Bergama_city_link_A3.pdf", page=1),
    # v10 (Aras 27 Oct: p18-19 into one page): the four sections as one panel
    dict(part="C", title=u"The proposals in section", rows=[[PS + "ps_all"]]),
    dict(part="C", title=u"Four seasons on one cut", rows=[[WB + "wb_s4_seasons"]]),
    dict(part="C", title=u"The S4 cut, north-east bank", rows=[[WB + "wb_s4_ne"]]),
    # v10: plants redo + the green space map from the stream edge page
    dict(part="C", title=u"Which plant goes where", rows=[[WB + "wb_plants"], [SB + "drw_tree_cover"]]),
    dict(part="C", title=u"Where the clean water goes", rows=[[WB + "wb_farms"], [WB + "wb_decision"]]),
    dict(part="C", title=u"What each cubic metre grows", sheet=AG + "Bergama_agriculture_alternatives_A3.pdf", page=0),
    # v10: "The farms we feed" deleted (Aras 27 Oct)
    dict(part="C", title=u"One plant ladder, streambed to field", sheet=AG + "Bergama_agriculture_alternatives_A3.pdf", page=2),
]

# the sheets whose own "Sources by number" keys the [n] marks on these pages refer to (sources page, in this order)
SOURCE_SHEETS = [SB + "Selinus_drawings.pdf", SB + "Selinus_01_what_is_there_axonometric.pdf",
                 CLK + "Bergama_city_link_A3.pdf", BAL + "Bergama_water_balance_A3.pdf",
                 WB + "Bergama_water_board_*.pdf", MP + "Bergama_masterplan_*_A.pdf",
                 PS + "Bergama_proposal_sections_A.pdf", AG + "Bergama_agriculture_alternatives_A3.pdf"]
