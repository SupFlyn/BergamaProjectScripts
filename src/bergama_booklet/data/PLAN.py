# ---- BOOKLET PLAN v19 (MIRAQUA 28 Oct, revision_2026-10-28/PLAN.md §3: p.02 side + edge types; p.07 notes beside the
# maps; p.09 index change; S1 senses sheet after the S4 cut; p.20 key map; D1 MERGE_21_22; no spread; N2/F5 sources);
# v18 (Aras 27 Oct 17:35, Prompt 8 final check: sheet pages titled as the sheets print them; empty
# frame pages left out, FRAME_PAGES); v17 (Aras 27 Oct 17:35, Prompt 7: E = open ground, then the spread edge | masterplan at 1:5,000;
# "Why each place" gone, its notes are callouts beside the masterplan); v16 (Aras 27 Oct 20:51: key map on the two S4 pages); v14 (Aras 27 Oct 17:34, Prompt 4: old p13 "How the stream behaves" merged into the water balance
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


# v19 (MIRAQUA 28 Oct, D1, default until Aras answers: merge): True = one filter page "Open ground and where we can
# build" (site board crop drw_filter) instead of "Open ground: the most the masterplan can use" (masterplan crop
# mp_max_area) and "Before the masterplan: the edge and where we can build" (site board crop drw_edge_build_e);
# False keeps those two pages (both scripts still write all three crops)
MERGE_21_22 = True


# sheet = a whole A3 sheet page as it is; rows = panels side by side, rows stacked, one scale for the page
# v11 (Prompt 1): page order = theme cycles (old v10.1 page numbers in the comments: page map
# revision_2026-10-27/prompts/P1_PAGE_MAP.md); merges are frames only, their content comes in later prompts
PAGES = [
    # ---- A SITE AND STREAM EDGE
    # old p2 + p4 -> one page (v12: plan 01 with the bank readings and the land-use ring beside it)
    # v19 (P02.2): the two banks straightened (edge types in the bars' colours, no scale) under the site readings
    dict(part="A", stage="an", title=u"What is there, grain of the town",
         rows=[[SB + "drw_plan01"]], side=[SB + "drw_site_readings", SB + "drw_edge_types"]),
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
    # old p7 (v13: stacked, 1:10,000); v19 (P07.2): each map with its note on why these streets matter, at its right
    dict(part="B", stage="an", title=u"How people use it", rows=[[SB + "drw_movement", SB + "drw_mv_note_1"],
                                                                 [SB + "drw_walking_today", SB + "drw_mv_note_2"],
                                                                 [SB + "drw_driving_today", SB + "drw_mv_note_3"]]),
    dict(part="B", stage="got", title=u"Why shops meet the stream only where it is hidden",   # v18: the sheet's own title
         sheet=CLK + "Bergama_city_link_A3.pdf", page=0),   # old p11
    # old p8 without the heritage loop (moved to D)
    # v19 (P09.3): the commercial spines went (they repeated p.07): walk and car index, today and with the proposal
    dict(part="B", stage="do", title=u"How people will move", rows=[[SB + "drw_proposal"], [SB + "drw_index_change"]]),
    dict(part="B", stage="do", title=u"The streamside spine, hub by hub", sheet=CLK + "Bergama_city_link_A3.pdf", page=1),   # old p18
    # ---- C WATER (one block)
    # old p13 + p12 -> one page (v14, Prompt 4): the water balance sheet v3 opens with "How the stream behaves" (its band
    # beside the title: monthly flow, Jul-Sep dry, flood levels on the surveyed cut at 1:500), so analysis leads, then the
    # answer; the water board's wb_water crop is no longer used
    dict(part="C", stage="an+got", title=u"The water balance",   # v18: the sheet's own title (its band: how the stream behaves)
         sheet=BAL + "Bergama_water_balance_A3.pdf"),
    dict(part="C", stage="do", title=u"Collect, clean, hold", rows=[[WB + "wb_system"]]),   # old p14
    dict(part="C", stage="do", title=u"The proposals in section", rows=[[PS + "ps_all"]]),   # old p19
    # v16 (Aras 27 Oct 20:51 "Move the line"): the board's S4 is the water board's S4, so these pages get its key map
    dict(part="C", stage="do", title=u"Four seasons on one cut", rows=[[WB + "wb_s4_seasons"]],
         key=SB + "sec_sections_key_s4"),   # old p20
    dict(part="C", stage="do", title=u"The S4 cut, north-east bank", rows=[[WB + "wb_s4_ne"]],
         key=SB + "sec_sections_key_s4"),   # old p21
    # v19 (MIRAQUA 28 Oct, S1 + N1): the new senses page right after the S4 cut, both about life with the water
    dict(part="C", stage="do", title=u"The senses and the water", sheet=MP + "Bergama_senses_A3.pdf"),
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
    # v19 (P20.1, D2 default B): one map at 1:10,000 holding every stop; the whole survey as its key map (no scale)
    dict(part="D", stage="do", title=u"The heritage loop", rows=[[SB + "drw_heritage_loop"]],
         key=SB + "drw_heritage_key"),   # from old p8
    # ---- E MASTERPLAN AS THE SYNTHESIS. v19 (MIRAQUA 28 Oct, G7, D1): every map one strip at 1:10,000, so no spread
    # any more (the masterplan is one strip on one page); MERGE_21_22 (above) picks one filter page or the two old ones
] + ([
    # D1 = merge (default): the filter in one strip: frame 150.5 ha -> open ground -> of which open to change, and why
    # (site board crop drw_filter; it replaces "Open ground: the most ..." and "Before the masterplan ...")
    dict(part="E", stage="an+got", title=u"Open ground and where we can build", rows=[[SB + "drw_filter"]]),
] if MERGE_21_22 else [
    dict(part="E", stage="an", title=u"Open ground: the most the masterplan can use",
         rows=[[MP + "mp_max_area"]]),   # old p17 bottom row
    dict(part="E", stage="got", title=u"Before the masterplan: the edge and where we can build",
         rows=[[SB + "drw_edge_build_e"]]),   # Prompt 2's diagram (p.6), the P06.2 hatches
]) + [
    dict(part="E", stage="do", title=u"Masterplan: an ecological corridor",
         rows=[[MP + "mp_plan"]]),   # old p15 + old p16's notes as callouts; v19: one strip + the grouped list
    dict(part="E", stage="do", title=u"The water edge at 1:1,000", rows=[[MP + "dt_upstream", MP + "dt_k5"]]),   # old p17 top row
]

# v11: panels left out without a placeholder when their script did not write them (v17: none since the notes page went)
OPTIONAL_KEYS = set()

# v18 (Prompt 8 final check): a page whose every drawing is still a frame (SLOT) is left out of the booklet, logged;
# True puts the empty frames back (A "What we do with the edge", D "Heritage along the stream")
FRAME_PAGES = False

# the sheets whose own "Sources by number" keys the [n] marks on these pages refer to (sources page, in this order)
SOURCE_SHEETS = [SB + "Selinus_drawings.pdf", SB + "Selinus_01_what_is_there_axonometric.pdf",
                 CLK + "Bergama_city_link_A3.pdf", BAL + "Bergama_water_balance_A3.pdf",
                 WB + "Bergama_water_board_*.pdf", MP + "Bergama_masterplan_*_A.pdf", MP + "Bergama_senses_A3.pdf",
                 PS + "Bergama_proposal_sections_A.pdf", AG + "Bergama_agriculture_alternatives_A3.pdf"]   # v19: + S1

# ---- v19 (MIRAQUA 28 Oct, F5 = Aras 28 Oct 11:38 answer 5: "every [n] whose source is not public online (research
# cards, notes, decisions, chats, Begüm's page) goes ... a figure left without a public source is reported"): the
# booklet's sources page lists public online sources only. A source text that cites our own working material
# (F5_INTERNAL) and names no public source (F5_PUBLIC) is left out and its marks are taken off the pages (the log
# lists each, under "F5"); a kept text loses the ';' parts that cite only that material and the brackets/register codes
# of F5_STRIP. Our survey and our calculations without such a pointer stay as they are. False = every source as before.
F5_DROP = True
F5_INTERNAL = (
    r"\b[hi]0\d\b",                                       # research cards h01-h03, i01
    r"(?i)\bcards?\b",
    r"DATA_REGISTER",
    r"(?i)DECISIONS(?:\.md)?\b|\bdecisions?\b|\bD\d{1,2}\b(?![\w.])",   # decisions (D8, D10)
    r"(?i)\bREADME\b|\.md\b|CONCEPT_RECORD|\blibrary/|\bresearch/|\bresearch\s+§|\bconcept/|history_phase1",
    u"\\b(?:Aras|Begüm|Nil)\\b",                          # chats and decisions by name, Begüm's page
    r"(?i)\bchats?\b|\bnotes?\b",
    r"\bPR1 board\b",
    u"§\\s?\\d+(?:\\.\\d+)*\\s+Q\\d+\\b",                    # the research files' questions (§0 Q1)
    r"\bs\d{1,3}\b",                                      # the research cards' source codes (s13, s62)
)
F5_PUBLIC = (
    r"(?i)https?://|www\.|\b[\w-]+\.(?:org|com|gov|int|edu|net|info|eu|tr|uk|de|nl|es|fr|it)\b",
    u"OpenStreetMap|\\bOSM\\b|Overture|WorldCover|Copernicus|Sentinel|\\bESA\\b|\\bFAO\\b|\\bMGM\\b|\\bWMO\\b|"
    u"\\bDS[İI]\\b|TÜİK|ERA5|Open-Meteo|Wikipedia|Wikimedia|\\bRHS\\b|\\bJRC\\b|POWO|FEIS|USDA|NRCS|ICOMOS|MITECO|"
    u"Rijkswaterstaat|ESHOT|İZSU|NOAA|Meeus|TAGEM|ÇŞİDB|TMMOB|Danıştay|Resmî Gazete|\\bRG \\d|\\bArt\\. ?\\d|Yön\\.|"
    u"\\bDWA\\b|Ecocrop|Meta/WRI|\\bCLC\\b|Corine|Haskoning|\\bUK EA\\b|Ticaret Borsası|Ajans|\\bAA\\b|\\bEPA\\b|"
    u"IUCN|UNESCO",
    r"(?i)\bpublished\b|\bofficial\b|\bpress\b|\bnews\b",
    # an author and year ("Vymazal 2010", "Kaya et al. 2017", "Somay & Gemici 2015"), never a month or a date
    u"\\b(?!(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\\b)(?!(?:Aras|Begüm|Nil|Fall|Spring)\\b)"
    u"[A-ZÇĞİÖŞÜ][\\w'’-]+(?: et al\\.?| (?:&|and) [A-ZÇĞİÖŞÜ][\\w'’-]+)?,? \\(?(?:19|20)\\d\\d[a-z]?\\b(?![-–/.:]\\d)",
)
F5_STRIP = (
    r"\s*\((?=[^()]*(?:library/|research/|concept/|history_phase1|\.md\b|README|DATA_REGISTER|DECISIONS))[^()]*\)",
    u",?\\s*DATA_REGISTER(?:\\s*§\\s?\\d+)?(?:[\\s,]+[A-Z]{2}[-‐–]?[A-Z]?\\d+[a-z]?)+",
)

# v19 (N2, G12): source texts listed on the sources page even when no page cites them by a number: the photo credits
# ("photo <English (Turkish)>: author, licence, Wikimedia Commons, commons.wikimedia.org/?curid=N") and the data notes
# (P06.3: OSM building footprints where the survey has none)
ALWAYS_LIST = (r"^photo\s", r"(?i)\bfootprints?\b")

# v19 (MIRAQUA 28 Oct, G10 "one number, one calculation"): figures that must read the same on every page that prints
# them: (name, unit, patterns with the figure as group "v"); the log names every page of each value when they differ
_HA = r"(?P<v>\d{1,3}(?:\.\d{1,2})?) ?ha\b"
_NOT = r"(?:(?!open|ground|chang|build|road|bed|plant|shade|cover)[^\d])"
FIGURE_CHECKS = (
    (u"analysis frame", u"ha", (r"(?i)\bframe\b" + _NOT + r"{0,40}?(?P<v>\d{3}(?:\.\d{1,2})?) ?ha\b",)),
    (u"study area", u"ha", (r"(?i)\bstudy area\b" + _NOT + r"{0,40}?" + _HA,)),
    (u"open ground", u"ha", (r"(?i)\bopen ground\b(?:(?!chang)[^\d]){0,30}?" + _HA,)),
    (u"open to change", u"ha", (r"(?i)\bopen to change\b[^\d]{0,30}?" + _HA,
                                _HA + r"(?:(?!frame|ground)[^\d]){0,24}?\bopen to change\b")),
    (u"Q100 flow", u"m³/s", (u"Q100[^\\d]{0,12}(?P<v>\\d{3}(?:\\.\\d)?) ?m³/s",)),
    (u"Q500 flow", u"m³/s", (u"Q500[^\\d]{0,12}(?P<v>\\d{3}(?:\\.\\d)?) ?m³/s",)),
    (u"rain a year", u"mm", (r"(?P<v>\d{3}(?:\.\d)?) ?mm (?:a|per) year\b", r"(?P<v>\d{3}(?:\.\d)?) ?mm/yr\b")),
)

# v19 (MIRAQUA 28 Oct, P78.ALT): pp.07 + 08 on one page, a separate file next to the booklet (the numbering stays):
# p.07's three maps at one round scale, then the city link's page_why panels (its booklet/blocks.json crops)
ALT_MAPS = [SB + "drw_movement", SB + "drw_walking_today", SB + "drw_driving_today"]
ALT_WHY = [CLK + "cl_why_1", CLK + "cl_why_2", CLK + "cl_why_3"]
ALT_TITLE = u"How people use it, and why shops meet the stream only where it is hidden"
