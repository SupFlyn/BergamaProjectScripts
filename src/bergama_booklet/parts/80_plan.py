# ---- 80_plan (round 7 S7, v33; BRIEF §3 L1-L3, PLAN §3): the 22-page booklet plan as FIXED FRAMES + SON SCALES ---------
# ONE numbering: p01 ... p22 (BRIEF §6), exported directly by every content script. Each content page: part / stage
# (kicker "<letter> <CHAPTER> · <PART>", contents, footer "<letter> <CHAPTER>  <n>"), title, intro (lead; used only when
# no script exports a role "intro" text), frames, side (the frame key where unlisted items go).
# A frame F(ids, x, y, w, h, den=None, f=1.0, **opt): ids = one fnmatch pattern or a tuple of them; x, y, w, h in MM on
# the A3 sheet (420 x 297, origin top left) = the MEASURED SON frame of the block (plan_findings/H4_page_table.md §5,
# §3 key maps; ±0.5 mm on the SON JPG); den = SON's printed scale (true-scale "m" drawings; an int, or a dict id -> den
# in a split frame); f = the size factor of an "mm" drawing (diagram, chart, axo, key map): 1.0 = its exported size
# (BRIEF L1 "keeps SON's size"; producers export at that size). The code never picks, rounds, snaps or fits a scale or
# a frame (L3): a drawing that does not fit = WARNING "<page> <drawing> frame", scale kept. Options: key (name;
# default the first pattern), note (frame key where this frame's drawings' attached notes go), split ("row" | "col":
# several drawings in one frame, set one after the other at their own size, gap mm), al ("TL" default ...), over (may
# sit on another frame: a legend / inset / key map inside a map), opt (an empty frame is no WARNING), noscale (no
# "1:n" printed: SON prints none, or the drawing carries its own bar).
# skip: item id patterns a page does not place (SON has no block for them; logged "skip <page> <id> ...", D4 / F12).


def F(ids, x, y, w, h, den=None, f=1.0, **kw):
    return dict(kw, ids=ids, mm=(float(x), float(y), float(x) + float(w), float(y) + float(h)), den=den, f=float(f))


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
    # 2 · SON page2 (H4 §5): plan 01 at 1:25,000, its key under it, three strips and the readings on the right
    dict(pid="p02", part="A", stage="an", title=u"What is there, grain of the town",
         intro=u"The whole survey area *as it is today*: buildings by *urban fabric*, ground and green, the *Selinos "
               u"stream* with its edges and *six bridges*, and the places where *stream and town clash*.",
         frames=[F("sb_plan01", 14.0, 30.0, 184.0, 161.0, den=25000, note="plan01_notes"),
                 F(("sb_plan01_*", "sb_p02_legend*", "sb_p02_note*"), 14.0, 193.0, 184.0, 68.5, key="plan01_notes"),
                 F("sb_edge_types", 212.0, 30.0, 194.5, 130.0),
                 F("sb_site_readings", 212.0, 163.0, 194.0, 98.0)],
         side="plan01_notes"),
    # 3 · SON page3: the axonometric at its exported size, numbered list top right, legend + notes in the bottom zone
    dict(pid="p03", part="A", stage="an", title=u"Heights and enclosure",
         intro=u"Plan 01 as a parallel axonometric: *heights* are what the plan cannot show; the *sky view* from the "
               u"stream bed marks its *most enclosed* stretch.",
         frames=[F("sb_axo_what_is_there", 22.5, 57.0, 374.5, 179.0, key="axo"),
                 F(("sb_axo_what_is_there_list*", "sb_p03_list*"), 349.5, 36.0, 56.5, 59.0, key="list", opt=True,
                   over=True),
                 F(("sb_axo_what_is_there_legend", "sb_p03_legend*"), 14.0, 258.0, 219.5, 18.5, key="legend"),
                 F(("sb_axo_what_is_there_caption", "sb_axo_*", "sb_p03_*"), 14.0, 277.5, 234.0, 7.5, key="notes")],
         side="notes"),
    # 4 · SON page4: key map S1-S4 (G7-3, 290.5 x 54.0), cuts at 1:2,500 (N1), notes column x 328.5
    dict(pid="p04", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses.",
         frames=[F(("sb_sec_keymap_p04", "*keymap*"), 29.0, 34.5, 290.5, 54.0, key="km"),
                 F(("sb_sec_legend_p04", "sb_sec_intro*"), 323.0, 34.5, 76.5, 26.5, key="legend"),
                 F("sb_sec_s1", 29.0, 88.5, 234.0, 46.5, den=2500, note="n1"),
                 F("sb_sec_note_s1*", 328.5, 92.5, 70.0, 54.0, key="n1"),
                 F("sb_sec_s2", 28.5, 152.0, 234.0, 28.0, den=2500, note="n2"),
                 F("sb_sec_note_s2*", 328.5, 149.0, 70.0, 30.0, key="n2"),
                 F("sb_sec_s3", 29.0, 197.0, 234.0, 47.0, den=2500, note="n3"),
                 F("sb_sec_note_s3*", 328.5, 180.5, 70.0, 56.0, key="n3"),
                 F("sb_sec_s4", 29.0, 262.0, 234.0, 26.5, den=2500, note="n4"),
                 F("sb_sec_note_s4*", 328.5, 238.5, 70.0, 46.0, key="n4")],
         side="legend"),
    # 5 · SON page5: key map S5-S8 (306.5 x 57.5), cuts at 1:1,500 (N1); SON runs x 7-412 (F9): edges = WARNING
    dict(pid="p05", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses.",
         frames=[F(("sb_sec_keymap_p05", "*keymap*"), 21.0, 27.0, 306.5, 57.5, key="km"),
                 F(("sb_sec_legend_p05", "sb_sec_intro*"), 330.5, 27.0, 81.0, 28.0, key="legend"),
                 F("sb_sec_s5", 17.0, 88.5, 225.0, 50.0, den=1500, note="n5"),
                 F("sb_sec_note_s5*", 343.5, 94.5, 68.0, 36.0, key="n5"),
                 F("sb_sec_s6", 17.0, 141.5, 225.0, 56.0, den=1500, note="n6"),
                 F("sb_sec_note_s6*", 343.5, 131.5, 68.0, 45.0, key="n6"),
                 F("sb_sec_s7", 17.0, 199.5, 225.0, 62.0, den=1500, note="n7"),
                 F("sb_sec_note_s7*", 343.5, 178.0, 68.0, 50.0, key="n7"),
                 F("sb_sec_s8", 17.0, 264.0, 225.0, 28.5, den=1500, note="n8"),
                 F("sb_sec_note_s8*", 343.5, 230.0, 68.0, 55.0, key="n8")],
         side="legend"),
    # 6 · SON page6: one board drawing (map 1:10,000, cards, photos, right column)
    dict(pid="p06", part="A", stage="got", title=u"The stream edge and where we can build",
         intro=u"Both banks *every 4 m*, and the ground *open to change*: where the project *can build*.",
         frames=[F("sb_edge_build", 13.5, 30.0, 392.5, 244.0, den=10000, key="edge"),
                 F(("sb_edge_build_*", "sb_p06_*"), 13.5, 275.0, 250.0, 9.0, key="notes", opt=True)],
         side="notes"),
    # 7 · SON page7: three maps at 1:10,000, each note column level with its map
    dict(pid="p07", part="B", stage="an", title=u"How people use it",
         intro=u"*Shops* line Kınık Caddesi and Üç Kemer Caddesi, the *primary commercial spines*; *walking* and "
               u"*driving* today, street by street.",
         frames=[F("sb_movement", 14.5, 30.0, 286.0, 71.0, den=10000, note="n1"),
                 F("sb_mv_note_1*", 304.0, 30.0, 101.0, 75.0, key="n1"),
                 F("sb_walking_today", 14.5, 107.5, 286.0, 70.5, den=10000, note="n2"),
                 F("sb_mv_note_2*", 304.0, 107.5, 101.0, 75.0, key="n2"),
                 F("sb_driving_today", 14.5, 185.0, 286.0, 70.5, den=10000, note="n3"),
                 F("sb_mv_note_3*", 302.5, 185.0, 103.5, 75.0, key="n3")],
         side="n3"),
    # 8 · SON page8: corridor 1:10,000, its legend, who chart, street cuts R1-R4 at 1:500, key map bottom right (TARGET)
    dict(pid="p08", part="B", stage="got", title=u"The stream joins the town where the shops already are",
         intro=u"One *corridor*: the shop streets, the *hidden stream* and the project from end to end; *who* comes "
               u"when; each *street cut* today and with the project.",
         frames=[F("cl_p08_corridor", 9.0, 30.5, 288.5, 68.0, den=10000, note="corr_legend"),
                 F("cl_p08_corridor_legend", 302.0, 40.0, 83.0, 51.0, key="corr_legend"),
                 F("cl_p08_shops", 302.0, 91.5, 83.0, 8.0, key="shops"),
                 F("cl_p08_who", 14.5, 106.0, 374.0, 92.0, note="who_notes"),
                 F(("cl_p08_who_legend", "cl_p08_who_note"), 14.5, 199.0, 300.0, 15.0, key="who_notes"),
                 F("sb_street_title_n1", 13.0, 229.5, 135.5, 5.0, key="street_title"),
                 F(("sb_street_R1", "sb_street_R2"), 13.0, 234.5, 135.5, 53.5, den=500, split="row", gap=4.0,
                   key="r12"),
                 F("sb_street_R3", 161.0, 243.5, 78.0, 43.5, den=500),
                 F("sb_street_R4", 245.0, 243.0, 60.5, 45.0, den=500),
                 F(("sb_street_keymap", "*keymap*"), 318.3, 217.3, 65.6, 12.4, key="km"),
                 F("sb_street_legend*", 318.0, 231.0, 70.0, 56.0, key="street_legend")],
         side="who_notes"),
    # 9 · SON page9: spine 1:10,000, legend, five hub cards, flood rule (SKETCH), which bank, market; no windows (F13)
    dict(pid="p09", part="B", stage="do", title=u"The streamside spine, hub by hub",
         intro=u"*Five bridge places* on existing bus stops, *walking hubs* with a *sub-hub in the bed*, one *transit "
               u"hub*: the spine along the Selinos, hub by hub.",
         skip=("cl_p10_win_*", "cl_p10_windows_head", "cl_p09_windows_head"),
         frames=[F("cl_p09_spine", 13.5, 31.0, 291.5, 71.0, den=10000, key="spine"),
                 F(("cl_p09_legend", "cl_p10_legend"), 310.0, 41.5, 96.0, 51.0, key="legend"),
                 F(("cl_p09_card_K4", "cl_p09_card_1", "cl_p10_hub_1"), 14.0, 104.0, 75.1, 82.0),
                 F(("cl_p09_card_K3", "cl_p09_card_2", "cl_p10_hub_2"), 92.9, 104.0, 76.4, 82.0),
                 F(("cl_p09_card_T", "cl_p09_card_3", "cl_p10_hub_3"), 171.8, 104.0, 76.5, 82.0),
                 F(("cl_p09_card_K5", "cl_p09_card_4", "cl_p10_hub_4"), 250.4, 104.0, 76.5, 82.0),
                 F(("cl_p09_card_K6", "cl_p09_card_5", "cl_p10_hub_5"), 329.3, 104.0, 76.8, 82.0),
                 F("cl_p10_flood", 13.5, 208.5, 154.5, 62.5, noscale=True),
                 F("cl_p10_bank", 214.5, 209.0, 111.5, 50.5),
                 F("cl_p10_market", 343.5, 210.5, 62.5, 30.0)],
         side="legend"),
    # 10 · SON page11: four chart panels; answer box [14,246.8 392x24.7] under its heading (F10)
    dict(pid="p10", part="C", stage="an+got", title=u"The water balance",
         intro=u"How much *winter water* can we hold for the farms' *dry summer*, and at *what cost*?",
         frames=[F("wb_year", 13.5, 31.0, 393.0, 114.0),
                 F("wb_curve", 13.5, 147.0, 227.5, 78.0),
                 F("wb_store", 244.5, 147.0, 162.0, 78.0),
                 F("wb_answer", 13.5, 235.0, 393.0, 37.0)],
         side="wb_answer"),
    # 11 · SON page12: map (no printed scale, F3) with its zoom and legend inside, right column, A-A' 1:500 (SKETCH);
    # no key map (F11)
    dict(pid="p11", part="C", stage="do", title=u"Collect, clean, hold",
         intro=u"*Collect* winter stream water and runoff at the upstream entry, *clean* it once in *lined reed "
               u"basins*, *hold* it in the ground for the dry summer; the clean stream leaves for the *farms outside*.",
         frames=[F("p12_map", 12.5, 30.0, 272.5, 186.0, key="map", noscale=True, note="map_legend"),
                 F(("wb_p12_map_legend", "p12_map_legend", "wb_p12_map_letters", "wb_p12_relief_note"), 197.0, 32.0,
                   87.0, 113.0, key="map_legend", over=True),
                 F("p12_zoom", 102.0, 35.0, 94.0, 70.0, over=True, noscale=True),
                 F("p12_steps", 291.5, 30.0, 114.5, 47.0),
                 F("p12_coliforms", 291.5, 79.5, 114.5, 49.0),
                 F("p12_plants", 291.5, 130.5, 114.5, 37.0),
                 F("p12_why", 291.5, 169.5, 114.5, 29.0),
                 F(("wb_p12_conclusion", "p12_conclusion"), 291.5, 200.0, 114.5, 17.0, key="conclusion"),
                 F(("p12_section_head*", "p12_section_list*", "wb_p12_section_key", "p12_section_key*"), 12.5, 221.0,
                   73.0, 50.0, key="aa_list"),
                 F(("p12_section_sketch", "p12_section"), 89.5, 221.0, 264.0, 50.0, den=500, key="aa",
                   note="aa_notes"),
                 F(("wb_p12_section_levels", "wb_p12_section_caption", "wb_p12_strip_note", "wb_p12_section_legend",
                    "p12_section_legend*"), 356.0, 221.5, 50.0, 55.0, key="aa_notes")],
         side="aa_notes"),
    # 12 · r06_S02: 4-in-1 SKETCH panels (194.8 x 92.0 drawings, title + purpose above), key map top right (F14:
    # the grid starts under it at y 51), caption + legend strip at the bottom
    dict(pid="p12", part="C", stage="do", title=u"The proposals in section",
         intro=u"Four cuts, *upstream to downstream*: each proposal *in section*, the winter water and the summer "
               u"strip, the reach of the *design flood (Q500)*.",
         frames=[F(("ps_panel_1", "ps_W1"), 13.7, 51.0, 194.8, 104.3),
                 F(("ps_panel_2", "ps_W2"), 211.2, 51.0, 194.8, 104.3),
                 F(("ps_panel_3", "ps_W3"), 13.7, 157.6, 194.8, 104.3),
                 F(("ps_panel_4", "ps_W4"), 211.2, 157.6, 194.8, 104.3),
                 F(("ps_keymap_p12", "ps_keymap_*"), 296.8, 27.0, 109.2, 22.0, key="km"),
                 F(("ps_caption*", "ps_intro_note*"), 13.7, 263.5, 200.0, 5.5, key="caption", opt=True),
                 F(("ps_legend_strip", "ps_legend"), 13.7, 269.5, 322.0, 6.0, key="legend")],
         side="legend"),
    # 13 · r06_S03 + SON page15 animal column and key map: four season rows at 1:500 on one x, FEEL column, animals
    dict(pid="p13", part="C", stage="do", title=u"Four seasons on one cut",
         intro=u"*One cut, one viewpoint, four seasons*: the *water level* decides what the place becomes, which "
               u"plants are in *leaf or flower*, and which animals are about.",
         frames=[F("p15_hubkey", 15.0, 30.0, 38.0, 15.0),
                 F("p15_monthbar", 55.5, 30.0, 148.0, 16.0),
                 F("p15_season_winter", 15.0, 48.5, 187.0, 49.0, den=500),
                 F("p15_season_spring", 15.0, 99.0, 187.0, 49.0, den=500),
                 F("p15_season_summer", 15.0, 149.5, 187.0, 49.0, den=500),
                 F("p15_season_autumn", 15.0, 200.0, 187.0, 49.0, den=500),
                 F("p15_feel*", 204.0, 33.5, 44.0, 218.0, key="feel"),
                 F(("p15_keymap", "*keymap*"), 290.4, 31.2, 94.5, 28.4, key="km"),
                 F("p15_animals*", 351.0, 62.5, 55.0, 190.0, key="animals"),
                 F(("p15_caption*", "p15_scale*"), 14.5, 250.5, 180.0, 6.0, key="caption", opt=True)],
         side="animals"),
    # 14 · SON page16: key map top LEFT (F5), cut 1:250 + zoom 1:100, three text blocks right, year chart
    dict(pid="p14", part="C", stage="do", title=u"The S4 cut, north-east bank",
         intro=u"The north-east bank of S4: *seat steps* and a *raised promenade* over Q500 stay; the *planting follows "
               u"the days under water*, the use follows the months.",
         frames=[F(("p16_keymap", "*keymap*"), 32.7, 37.3, 99.9, 30.0, key="km"),
                 F("p16_section_inset", 180.5, 33.0, 54.0, 36.0, den=100),
                 F("p16_section", 25.0, 69.0, 264.0, 87.0, den=250, note="parts"),
                 F("p16_parts", 290.0, 38.0, 96.0, 41.0, key="parts"),
                 F("p16_groups", 290.5, 81.0, 101.0, 20.5, key="groups"),
                 F("p16_bands", 290.5, 103.5, 101.0, 28.5, key="bands"),
                 F("p16_year", 25.5, 159.0, 369.5, 106.0)],
         side="parts"),
    # 15 · SON page17: six maps at 1:20,000 (2 x 3), each key in its column
    dict(pid="p15", part="C", stage="do", title=u"The senses and the water",
         intro=u"The *fade-out zones* and the *senses*, zone by zone, *upstream to downstream*.",
         frames=[F("mp_sn_zones", 13.5, 30.0, 148.0, 78.0, den=20000, note="k_zones"),
                 F("mp_sn_zones_key", 161.5, 30.0, 45.0, 78.0, key="k_zones"),
                 F("mp_sn_feeling", 211.5, 30.0, 148.0, 78.0, den=20000, note="k_feeling"),
                 F("mp_sn_feeling_wheel", 360.0, 30.0, 46.0, 22.0),
                 F("mp_sn_feeling_key", 360.0, 53.0, 46.0, 55.0, key="k_feeling"),
                 F("mp_sn_sound", 13.5, 112.5, 148.0, 79.0, den=20000, note="k_sound"),
                 F("mp_sn_sound_key", 161.5, 112.5, 45.0, 79.0, key="k_sound"),
                 F("mp_sn_smell", 211.5, 112.5, 148.0, 79.0, den=20000, note="k_smell"),
                 F("mp_sn_smell_key", 360.0, 112.5, 46.0, 79.0, key="k_smell"),
                 F("mp_sn_encounters", 13.5, 195.0, 148.0, 78.0, den=20000, note="k_enc"),
                 F("mp_sn_encounters_key", 162.0, 195.0, 45.0, 78.0, key="k_enc"),
                 F("mp_sn_history", 211.5, 195.0, 148.0, 78.0, den=20000, note="k_hist"),
                 F("mp_sn_history_key", 360.0, 195.0, 46.0, 40.0, key="k_hist"),
                 F("mp_sn_photo_*", 360.0, 236.0, 46.0, 37.0, key="photos", opt=True)],
         side="k_hist"),
    # 16 · SON page18: two stacked key maps (F6), plans legend, plans A/B 1:2,500, bands 1:10,000, heights, cards
    dict(pid="p16", part="C", stage="do", title=u"Which plant goes where",
         intro=u"*Wet to dry, low to high*: rushes and loosestrife *at the water*, willow and tamarisk on the *banks "
               u"that flood*, shade trees and olives on the *dry tops*; reed and water mint only in *lined basins*.",
         frames=[F("p18_keymap", 20.7, 34.1, 63.0, 12.9, key="km"),
                 F("p18_keymap_s4", 20.7, 49.1, 63.0, 14.8, key="km_s4"),
                 F(("p18_plans_legend", "p16_plans_legend"), 20.5, 87.0, 63.5, 61.0, key="legend"),
                 F("p18_plan_A", 88.0, 31.5, 84.0, 101.0, den=2500, note="list_A"),
                 F("p18_plan_A_list", 88.0, 133.0, 84.0, 18.5, key="list_A"),
                 F("p18_plan_B", 176.0, 31.5, 222.0, 108.0, den=2500, note="list_B"),
                 F("p18_plan_B_list", 176.0, 140.0, 222.0, 12.0, key="list_B"),
                 F("p18_bands", 22.0, 157.0, 104.0, 34.5, den=10000),
                 F(("p18_band_shares", "p18_foliage_shares"), 129.5, 157.0, 48.0, 40.0, split="col", gap=1.5,
                   key="shares"),
                 F("p18_heights", 180.0, 157.0, 218.0, 40.0),
                 F("p18_card_*", 21.0, 200.5, 377.0, 71.0, key="cards", split="row", gap=2.0),
                 F("p18_catalogue_sources", 21.0, 272.0, 300.0, 8.0, key="cat_src", opt=True)],
         side="legend"),
    # 17 · r06_S01 (SKETCH plant ladder): chain strip, three ladder rows, bands + photos, notes column
    dict(pid="p17", part="C", stage="do", title=u"One plant ladder, streambed to field",
         intro=u"One cut from the *stream to the farms*, through the year: what the *water* does and what *people* do "
               u"on each step.",
         frames=[F("ag3_chain", 15.0, 30.0, 391.0, 26.0),
                 F("ag3_ladder_high", 13.5, 59.0, 394.5, 47.5),
                 F("ag3_ladder_low", 13.0, 107.0, 395.0, 49.5),
                 F("ag3_ladder_harvest", 13.5, 157.0, 394.5, 48.5),
                 F(("ag3_note*", "ag3_remove*", "ag3_odour*"), 13.5, 207.5, 88.0, 77.0, key="notes"),
                 F("ag3_bands", 106.5, 205.6, 298.9, 80.2)],
         side="notes"),
    # 18 · SON page19: chain + farms outside, figures + stream first, crop bars + why crop choice, reading + history +
    # crop photos; the farms map is not on SON19 (F12): skipped
    dict(pid="p18", part="C", stage="do", title=u"Where the clean water goes, and what it grows",
         intro=u"Clean water to *farmland outside the site*, easing an *overused aquifer*, *never drinking water*; "
               u"*same storage, different crops*: the *hectares* each crop irrigates.",
         skip=("ag2_farms",),
         frames=[F("wb_farms", 25.0, 30.5, 225.0, 61.5),
                 F("wb_farms_out", 266.0, 30.5, 129.0, 56.0),
                 F("wb_decision", 15.0, 100.5, 124.5, 42.5),
                 F("ag1_stream", 146.5, 99.5, 250.5, 44.0),
                 F("ag1_bars", 14.0, 150.5, 227.0, 70.0),
                 F("ag1_context", 245.5, 150.5, 150.5, 70.0),
                 F("ag1_reading*", 15.0, 228.0, 112.0, 34.0, key="reading"),
                 F("ag1_history", 146.5, 227.5, 125.0, 22.0),
                 F("ag1_crops_*", 277.5, 227.5, 128.0, 35.0, key="crops")],
         side="ag1_context"),
    # 19 · SON page20: the heritage board (map 1:10,000, own bar), legends in one row under it, caption
    dict(pid="p19", part="D", stage="do", title=u"The heritage loop",
         intro=u"The Selinos is the *seam*: *bridges, crafts and events* tie the *Kale side* to the *bazaar side*.",
         frames=[F("sb_heritage_loop", 14.0, 32.5, 373.5, 214.0, den=10000, key="loop", noscale=True),
                 F(("sb_heritage_loop_legend", "sb_heritage_legend"), 13.5, 254.5, 240.0, 16.5, key="legend"),
                 F(("sb_heritage_loop_caption", "sb_heritage_*"), 13.5, 271.5, 101.5, 5.0, key="caption")],
         side="legend"),
    # 20 · SON page21 UNCHANGED (D6): masterplan rows 1:5,000 at their SON frames; only the footer number is new
    dict(pid="p20", part="E", stage="do", title=u"Masterplan: an ecological corridor",
         intro=u"The whole project on one plan: *walking hubs*, *reed basins* and terraces that *hold the rain*, "
               u"*calmed streets*, along the Selinos as an *ecological corridor*.",
         frames=[F("mp_plan_r1", 13.5, 29.5, 290.5, 116.5, den=5000),
                 F("mp_plan_r2", 13.5, 147.5, 290.5, 116.5, den=5000),
                 F("mp_plan_legend*", 308.0, 30.0, 98.0, 153.0, key="legend"),
                 F(("mp_plan_moves_head", "mp_plan_moves", "mp_plan_cch*", "mp_plan_left*", "mp_plan_places_head",
                    "mp_plan_places"), 308.5, 185.0, 97.5, 80.0, key="places"),
                 F("mp_plan_caption", 13.5, 269.0, 392.5, 7.0, key="caption")],
         side="places"),
    # 21 · SON page22: plans D1, D2 + sections at 1:1,000; key map inside the D2 plan (F7, north left, S6)
    dict(pid="p21", part="E", stage="do", title=u"The water edge, plan and section",
         intro=u"Two windows, each *plan with its section*: the *upstream entry* (collect, clean, hold) and *Üç Kemer "
               u"Köprüsü* with Demeter's Garden.",
         frames=[F("mp_dt_*upstream", 13.5, 29.5, 194.5, 132.0, den=1000, key="d1"),
                 F("mp_dt_*k5", 212.0, 29.5, 194.0, 132.0, den=1000, key="d2"),
                 F(("mp_dt_keymap", "*keymap*"), 378.1, 30.9, 26.9, 35.9, key="km", over=True),
                 F("mp_dt_*upstream_sec", 13.5, 165.5, 194.5, 45.5, den=1000, key="s1", note="leg1"),
                 F("mp_dt_*k5_sec", 211.5, 165.5, 194.5, 65.0, den=1000, key="s2", note="leg2"),
                 F(("mp_dt_*upstream_leg*", "mp_dt_*upstream_route", "mp_dt_*upstream_why"), 13.5, 212.0, 194.0, 72.0,
                   key="leg1"),
                 F(("mp_dt_*k5_leg*", "mp_dt_*k5_route", "mp_dt_*k5_why"), 211.5, 232.0, 194.5, 52.0, key="leg2")],
         side="leg2"),
    dict(pid="p22", kind="sources", part="E", stage="do", title=u"Sources"),
]
BK_REF_PAGE = "p13"          # D2 reference fill: "Four seasons on one cut" = round 6 p13 (PLAN §2.1)
