# ---- BOOKLET PLAN v16 (Aras 27 Oct 20:51: key map on the two S4 pages); v14 (Aras 27 Oct 17:34, Prompt 4: old p13 "How the stream behaves" merged into the water balance
# sheet's page, analysis first); v13 (Aras 27 Oct 17:34, Prompt 3: p.8 the three movement maps stacked, each the site frame at
# 1:10,000); v12 (Aras 27 Oct 17:34, Prompt 2: p.2 plan 01 + site readings side panel; p.6 the stream edge and
# where we can build; a key map on each sections page: "key" = a crop in the title band, "side" = panels at the right
# margin beside the rows); v11 (Aras 27 Oct 17:27, Prompt 1: theme cycles, merge frames); v10 (Aras 27 Oct 11:07 review: page list above each entry); v9 (Aras 27 Oct 06:20: proposal sections always two to a page); v8 (Aras 26 Oct 08:27-08:28: masterplan halves on one page; long section along the spine left out, it
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

# v11 (Aras 27 Oct 17:27, Prompt 1): theme cycles; each theme runs ANALYSIS -> WHAT WE GOT -> WHAT WE DO WITH IT
PARTS = {"A": u"Site and stream edge", "B": u"Movement and the city", "C": u"Water", "D": u"History and heritage",
         "E": u"Masterplan: the synthesis"}
STAGES = {"an": u"Analysis", "got": u"What we got", "an+got": u"Analysis, what we got", "do": u"What we do with it"}

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



def SLOT(text, w=180.0, h=120.0):
    """v11: a frame for a drawing a later prompt makes: a labelled placeholder of w x h mm (never a drawing)"""
    return "slot|%.0f|%.0f|%s" % (w, h, text)


# sheet = a whole A3 sheet page as it is; rows = panels side by side, rows stacked, one scale for the page
# v11 (Prompt 1): page order = theme cycles (old v10.1 page numbers in the comments: page map
# revision_2026-10-27/prompts/P1_PAGE_MAP.md); merges are frames only, their content comes in later prompts
PAGES = [
    # ---- A SITE AND STREAM EDGE
    # old p2 + p4 -> one page (v12: plan 01 with the bank readings and the land-use ring beside it)
    dict(part="A", stage="an", title=u"What is there, grain of the town",
         rows=[[SB + "drw_plan01"]], side=[SB + "drw_site_readings"]),
    dict(part="A", stage="an", title=u"Heights and enclosure", sheet=SB + "Selinus_01_what_is_there_axonometric.pdf"),   # old p3
    dict(part="A", stage="an", title=u"Sections across the stream", rows=[[SB + "sec_sections_1"]], optional=True,
         key=SB + "sec_sections_key_1"),   # old p9
    dict(part="A", stage="an", title=u"Sections across the stream", rows=[[SB + "sec_sections_2"]], optional=True,
         key=SB + "sec_sections_key_2"),   # old p10
    # old p5 + p6 -> one page (v12: the edge every 4 m, ground open to change, photo viewpoints and the photos)
    dict(part="A", stage="got", title=u"The stream edge and where we can build", rows=[[SB + "drw_edge_build"]]),
    dict(part="A", stage="do", title=u"What we do with the edge",
         rows=[[SLOT(u"Edge moves: proposal frame (later prompt)", 380.0, 200.0)]]),
    # ---- B MOVEMENT AND THE CITY
    dict(part="B", stage="an", title=u"How people use it", rows=[[SB + "drw_movement"], [SB + "drw_walking_today"],
                                                                 [SB + "drw_driving_today"]]),   # old p7 (v13: stacked, 1:10,000)
    dict(part="B", stage="got", title=u"Why shops meet the stream where it is hidden",
         sheet=CLK + "Bergama_city_link_A3.pdf", page=0),   # old p11
    # old p8 without the heritage loop (moved to D)
    dict(part="B", stage="do", title=u"How people will move", rows=[[SB + "drw_proposal"], [SB + "drw_commercial_spine"]]),
    dict(part="B", stage="do", title=u"The streamside spine, hub by hub", sheet=CLK + "Bergama_city_link_A3.pdf", page=1),   # old p18
    # ---- C WATER (one block)
    # old p13 + p12 -> one page (v14, Prompt 4): the water balance sheet v3 opens with "How the stream behaves" (its band
    # beside the title: monthly flow, Jul-Sep dry, flood levels on the surveyed cut at 1:500), so analysis leads, then the
    # answer; the water board's wb_water crop is no longer used
    dict(part="C", stage="an+got", title=u"How the stream behaves, and the water balance",
         sheet=BAL + "Bergama_water_balance_A3.pdf"),
    dict(part="C", stage="do", title=u"Collect, clean, hold", rows=[[WB + "wb_system"]]),   # old p14
    dict(part="C", stage="do", title=u"The proposals in section", rows=[[PS + "ps_all"]]),   # old p19
    # v16 (Aras 27 Oct 20:51 "Move the line"): the board's S4 is the water board's S4, so these pages get its key map
    dict(part="C", stage="do", title=u"Four seasons on one cut", rows=[[WB + "wb_s4_seasons"]],
         key=SB + "sec_sections_key_s4"),   # old p20
    dict(part="C", stage="do", title=u"The S4 cut, north-east bank", rows=[[WB + "wb_s4_ne"]],
         key=SB + "sec_sections_key_s4"),   # old p21
    dict(part="C", stage="do", title=u"Which plant goes where",   # old p22; v15: the July shade strip (Prompt 5 3a)
         rows=[[WB + "wb_plants"], [SB + "drw_shade_strip||" + SB + "drw_tree_cover"]]),
    dict(part="C", stage="do", title=u"Where the clean water goes", rows=[[WB + "wb_farms"], [WB + "wb_decision"]]),   # old p23
    dict(part="C", stage="do", title=u"What each cubic metre grows", sheet=AG + "Bergama_agriculture_alternatives_A3.pdf", page=0),   # old p24
    dict(part="C", stage="do", title=u"One plant ladder, streambed to field",
         sheet=AG + "Bergama_agriculture_alternatives_A3.pdf", page=2),   # old p25
    # ---- D HISTORY AND HERITAGE (now spread over old p3, p8, p18, p20: collected here as frames)
    dict(part="D", stage="an+got", title=u"Heritage along the stream",
         rows=[[SLOT(u"Heritage on site: Roman bridges and tunnels, Red Hall, Ulu Cami, tannery quarter (later prompt)", 230.0, 200.0),
                SLOT(u"What history asks of the edge (later prompt)", 146.0, 200.0)]]),
    dict(part="D", stage="do", title=u"The heritage loop", rows=[[SB + "drw_heritage_loop"]]),   # from old p8
    # ---- E MASTERPLAN AS THE SYNTHESIS: one spread (left page even) = masterplan + open ground + new edge diagram
    dict(part="E", stage="do", title=u"Masterplan: an ecological corridor", spread="L",
         rows=[[MP + "mp_upstream"], [MP + "mp_downstream"]]),   # old p15
    # old p17 bottom row (open ground) + new edge diagram + old p16 notes folded in (frame)
    dict(part="E", stage="do", title=u"Masterplan: open ground and the new edge", spread="R",
         rows=[[MP + "mp_max_area", SLOT(u"New edge diagram (later prompt)", 150.0, 110.0)], [MP + "mp_notes"]]),
    dict(part="E", stage="do", title=u"The water edge at 1:1,000", rows=[[MP + "dt_upstream", MP + "dt_k5"]]),   # old p17 top row
]

# v11: panels left out without a placeholder when their script did not write them (the masterplan notes, v24.1+)
OPTIONAL_KEYS = {MP + "mp_notes"}

# the sheets whose own "Sources by number" keys the [n] marks on these pages refer to (sources page, in this order)
SOURCE_SHEETS = [SB + "Selinus_drawings.pdf", SB + "Selinus_01_what_is_there_axonometric.pdf",
                 CLK + "Bergama_city_link_A3.pdf", BAL + "Bergama_water_balance_A3.pdf",
                 WB + "Bergama_water_board_*.pdf", MP + "Bergama_masterplan_*_A.pdf",
                 PS + "Bergama_proposal_sections_A.pdf", AG + "Bergama_agriculture_alternatives_A3.pdf"]
