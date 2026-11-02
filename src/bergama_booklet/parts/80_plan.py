# ---- 80_plan (round 5, S10, 2 Nov 2026): the 23-page booklet plan (D7, D9; PLAN §10 S10; BRIEF page map) -------------
# ONE numbering: the 23-page ids of PLAN §4 ("p01" ... "p23"). Scripts that still export 25-page ids are mapped in ONE
# place: 81_ids.py BK_PAGE_IDS (folder -> numbering) + BK_25_TO_23.
# Each content page: title (the round 4 printed title, PAGE_LIST.md; merged pages one title), part / stage (contents),
# intro (used only when the page's scripts export no role "intro" text), share (drawing share of the inner width,
# G-R5-2: ~70 % per Aras's p23 redesign, wider where the drawings were designed at full page width), rows (left drawing
# area, top to bottom; each row = cells side by side; a cell = an exported drawing id or an fnmatch pattern; one row may
# expand to several drawings), common (one scale for every true-scale drawing of the page: merged pages N3 1:500),
# right (drawing ids/patterns set in the right column, small diagrams). Any drawing of the page that no row or right
# entry names still goes in (right column) with a log line, so nothing exported is lost (booklet rules: every output in).
BOOK = dict(
    hook=u"MIRAQUA",
    title=u"From stream corridor to hydrological commons",
    subtitle=u"Selinos stream edge, Bergama",
    course=u"Yaşar University · ARCH 4410 Architectural Design Studio V · 2026-2027 Fall",
    names=[u"Aras Özkaymakcı", u"Begüm Arslan", u"Nil Çetin"],
    date=u"October 2026",             # round 4 value kept (change here if the booklet date moves)
)
PARTS = {"A": u"Site and stream edge", "B": u"Movement and the city", "C": u"Water", "D": u"History and heritage",
         "E": u"Masterplan: the synthesis"}
STAGES = {"an": u"Analysis", "got": u"What we got", "an+got": u"Analysis, what we got", "do": u"What we do with it"}
COVER_IMG = "W01_cover_collage.jpg"          # Downloads/Bergama/Data/ (own work, round 4 P01.2)
COVER_VEIL = 0.82                            # P01.1: white veil over the full-bleed photo = photo at 18 % strength
COVER_TEXT = (u"MIRAQUA turns the walled Selinos stream through Bergama into a landscape that lives in all four seasons. "
              u"Clean water is collected, cleaned and held at the upstream entry, kept in the bed as a summer strip, and "
              u"given to the farms outside the site. Planting follows the days under water, from wet to dry; when the "
              u"water rises, life on the banks pauses and returns as it drops. A streamside spine of five bridge places "
              u"ties the Kale side to the bazaar side.")      # round 4 approved text (BRIEF P01.2 r4), unchanged

BK_PAGES = [
    dict(pid="p01", kind="cover"),
    dict(pid="p02", part="A", stage="an", title=u"What is there, grain of the town",
         intro=u"The whole survey area *as it is today*: buildings by *urban fabric*, ground and green, the *Selinos "
               u"stream* with its edges and *six bridges*, and the places where *stream and town clash*.",
         rows=[["sb_plan01"]], right=["sb_site_readings", "sb_edge_types"]),
    dict(pid="p03", part="A", stage="an", title=u"Heights and enclosure",
         intro=u"Plan 01 as a parallel axonometric: *heights* are what the plan cannot show; the *sky view* from the "
               u"stream bed marks its *most enclosed* stretch.",
         rows=[["sb_axo_what_is_there"]], share=0.78),
    dict(pid="p04", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses.", rows=[["sb_sec_s1"], ["sb_sec_s2"], ["sb_sec_s3"], ["sb_sec_s4"]],
         common=True, share=0.82),   # v30.2: one drawing per cut (site board v60.2); key map (role keymap) and legend go right by themselves
    dict(pid="p05", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses.", rows=[["sb_sec_s5"], ["sb_sec_s6"], ["sb_sec_s7"], ["sb_sec_s8"]],
         common=True, share=0.82),   # v30.2: one drawing per cut (site board v60.2); key map (role keymap) and legend go right by themselves
    dict(pid="p06", part="A", stage="got", title=u"The stream edge and where we can build",
         intro=u"Both banks *every 4 m*, and the ground *open to change*: where the project *can build*.",
         rows=[["sb_edge_build"]], share=0.82),
    dict(pid="p07", part="B", stage="an", title=u"How people use it",
         intro=u"*Shops* line Kınık Caddesi and Üç Kemer Caddesi, the *primary commercial spines*; *walking* and "
               u"*driving* today, street by street.",
         rows=[["sb_movement"], ["sb_walking_today"], ["sb_driving_today"]], share=0.75),
    # v30.3: three maps stacked (side by side they were 289 mm in 272 mm: overlaps), 1:10,000 instead of 1:20,000
    dict(pid="p08", part="B", stage="got", title=u"The stream joins the town where the shops already are",
         intro=u"One *corridor*: the shop streets, the *hidden stream* and the project from end to end; *who* comes "
               u"when.", rows=[["cl_p08_corridor"], ["cl_p08_who"]], share=0.75),
    dict(pid="p09", part="B", stage="got", title=u"The streets, before and after",
         intro=u"Each *street* cut *whole*: *where* it is, the *ground*, *people* and *planting*, today and with the "
               u"project.", rows=[["sb_street_sections"]], share=0.82),
    dict(pid="p10", part="B", stage="do", title=u"The streamside spine, hub by hub",
         intro=u"*Five bridge places* on existing bus stops, *walking hubs* with a *sub-hub in the bed*, one *transit "
               u"hub*: the spine along the Selinos, hub by hub.",
         rows=[["cl_p10_win_1", "cl_p10_win_2", "cl_p10_win_3a"], ["cl_p10_win_3b", "cl_p10_win_4", "cl_p10_win_5"],
               ["cl_p10_hub_*"], ["cl_p10_flood", "cl_p10_bank", "cl_p10_market"]],
         common=True),      # v30.3: windows in two rows of three (one row of six was 1:5,000, 38 mm each)      # P10: the windows share one size and one scale (S9 handover §5)
    dict(pid="p11", part="C", stage="an+got", title=u"The water balance",
         intro=u"How much *winter water* can we hold for the farms' *dry summer*, and at *what cost*?",
         rows=[["wb_year"], ["wb_curve", "wb_store"], ["wb_answer"]], share=0.80),    # v30.3: wider charts     # S5 §6: v9's order
    dict(pid="p12", part="C", stage="do", title=u"Collect, clean, hold",
         intro=u"*Collect* winter stream water and runoff at the upstream entry, *clean* it once in *lined reed "
               u"basins*, *hold* it in the ground for the dry summer; the clean stream leaves for the *farms outside*.",
         rows=[["p12_map", "p12_zoom"], ["p12_section", "p12_section_reeds"]],
         right=["p12_steps", "p12_coliforms", "p12_plants", "p12_why"]),
    dict(pid="p13", part="C", stage="do", title=u"The proposals in section",
         intro=u"The four cuts *W1 to W4*, upstream to downstream, each proposal *in section* at *1:500* with a "
               u"*1:100* detail and the *Q500* flood line.",                          # D9 merged, N3 a 1:500
         rows=[["ps_W1", "ps_W1_inset"], ["ps_W2", "ps_W2_inset"], ["ps_W3", "ps_W3_inset"],
               ["ps_W4", "ps_W4_inset"]], common=True),
    dict(pid="p14", part="C", stage="do", title=u"Four seasons on one cut",
         intro=u"*One cut, one viewpoint, four seasons*: the *water level* decides what the place becomes, which "
               u"plants are in *leaf or flower*, and which animals are about.",
         rows=[["p15_rain_%s" % s, "p15_cut_%s" % s, "p15_cut_%s_inset" % s, "p15_view_%s" % s]
               for s in ("winter", "spring", "summer", "autumn")], common=True, share=0.80),
    dict(pid="p15", part="C", stage="do", title=u"The S4 cut, north-east bank",
         intro=u"The north-east bank of S4: *seat steps* and a *raised promenade* over Q500 stay; the *planting follows "
               u"the days under water*, the use follows the months.",
         rows=[["p16_section", "p16_section_inset"], ["p16_year"]]),
    dict(pid="p16", part="C", stage="do", title=u"The senses and the water",
         intro=u"The *fade-out zones* and the *senses*, zone by zone, *upstream to downstream*.",
         rows=[["mp_sn_zones", "mp_sn_feeling"], ["mp_sn_sound", "mp_sn_smell"], ["mp_sn_encounters", "mp_sn_history"]],
         right=["mp_sn_feeling_wheel", "mp_sn_encounters_key"], common=True, share=0.62),
    # v30.3: 3 rows of 2 maps (2 rows of 3 were 440 mm wide in 272 mm: overlaps); wider right column for the legends and
    # the six photos
    dict(pid="p17", part="C", stage="do", title=u"Which plant goes where",
         intro=u"*Wet to dry, low to high*: rushes and loosestrife *at the water*, willow and tamarisk on the *banks "
               u"that flood*, shade trees and olives on the *dry tops*; reed and water mint only in *lined basins*.",
         rows=[["p18_plan_A", "p18_plan_B"], ["p18_bands", "p18_band_shares", "p18_foliage_shares", "p18_heights"],
               ["p18_card_*"]]),
    dict(pid="p18", part="C", stage="do", title=u"Which plant goes where, in section",
         intro=u"Four cuts at *1:500* (F2, F4, W1, S4), each with its detail: the *water*, the *planting band* each "
               u"species needs, and what surrounds it.",                               # D7 merged, N3 a
         rows=[["wb_p19_F2", "wb_p19_F2_inset"], ["wb_p19_F4", "wb_p19_F4_inset"], ["wb_p20_W1", "wb_p20_W1_inset"],
               ["wb_p20_S4", "wb_p20_S4_inset"]], common=True),
    dict(pid="p19", part="C", stage="do", title=u"Where the clean water goes, and what it grows",
         intro=u"Clean water to *farmland outside the site*, easing an *overused aquifer*, *never drinking water*; "
               u"*same storage, different crops*: the *hectares* each crop irrigates.",
         rows=[["wb_farms", "wb_farms_out"], ["ag1_stream", "wb_decision"], ["ag1_bars", "ag1_context"],
               ["ag1_history"]], right=["ag2_farms"]),
    dict(pid="p20", part="D", stage="do", title=u"The heritage loop",
         intro=u"The Selinos is the *seam*: *bridges, crafts and events* tie the *Kale side* to the *bazaar side*.",
         rows=[["sb_heritage_loop"]], share=0.75),
    dict(pid="p21", part="E", stage="do", title=u"Masterplan: an ecological corridor",
         intro=u"The whole project on one plan: *walking hubs*, *reed basins* and terraces that *hold the rain*, "
               u"*calmed streets*, along the Selinos as an *ecological corridor*.",
         rows=[["mp_plan_r1"], ["mp_plan_r2"]], share=0.75),    # v30.3: 1:5,000 fits (was 1:10,000)
    dict(pid="p22", part="E", stage="do", title=u"The water edge, plan and section",
         intro=u"Two windows, each *plan with its section*: the *upstream entry* (collect, clean, hold) and *Üç Kemer "
               u"Köprüsü* with Demeter's Garden.",
         rows=[["mp_dt_*upstream", "mp_dt_*k5"], ["mp_dt_*upstream_sec", "mp_dt_*k5_sec"],
               ["mp_dt_*upstream_sec_zoom", "mp_dt_*k5_sec_zoom"]], common=True, scales=(1000, 1500)),
    # v30.3: plan beside plan, section beside section (plan + section in one row was 388 mm in 272 mm). Two windows do
    # not fit A3 at 1:1,000 (2 x 194 mm plans), so the page takes 1:1,000 when one window is there, else 1:1,500
    dict(pid="p23", kind="sources", title=u"Sources"),
]
BK_REF_PAGE = "p14"          # D2 "p15's fill" = the 25-page p15 "Four seasons on one cut" = 23-page p14 (81_ids)
