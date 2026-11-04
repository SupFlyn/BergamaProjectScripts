# ---- 80_plan (round 5 S10; round 6 S9 v31, G6-1/G6-2): the 22-page booklet plan as FRAMES ---------------------------
# ONE numbering: p01 ... p22 (PLAN §2.1), exported directly by every content script. Each content page: part / stage
# (contents on the cover), title (PLAN §2.1), intro (used only when no script exports a role "intro" text), frames,
# side (the frame key where unlisted items and overflow notes go).
# A frame F(ids, x, y, w, h, **opt): ids = one fnmatch pattern or a tuple of them (item ids of PLAN §2.2 first, then
# the ids the scripts export today, so a page composes before and after the round 6 content sessions); box in % of
# the A3 page, 0,0 top left (PLAN §3: plan_findings/frames_p01-08.md, frames_p09-13.md, frames_p14-22.md, "Target
# frames", est. +-1 %). Options: key (name; default the first pattern), same (frames with one key share one scale /
# factor), note (the frame key where this frame's drawings' attached notes go), foot (% of the page kept under the
# drawings for their notes), split ("row" | "col" for several drawings in one frame), al ("TL" default, "MC", "BL"
# ...), over (may sit on another frame), opt (an empty frame is no WARNING), gap (mm between split cells),
# noscale (no "1:n" printed under a drawing that carries its own scale bar).
# Every frame is inside the one margin set x 3.3-96.7 % (P-6) and above the page number (y <= 94 %).


def F(ids, x, y, w, h, **kw):
    return dict(kw, ids=ids, box=(x, y, w, h))


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
    # 2 · SON page2 (G6-1: map x1.035, right column as SON, lower block down 1.5)
    dict(pid="p02", part="A", stage="an", title=u"What is there, grain of the town",
         intro=u"The whole survey area *as it is today*: buildings by *urban fabric*, ground and green, the *Selinos "
               u"stream* with its edges and *six bridges*, and the places where *stream and town clash*.",
         frames=[F("sb_plan01", 3.3, 10.0, 45.2, 59.5, note="plan01_notes"),
                 F(("sb_plan01_*", "sb_p02_legend*", "sb_p02_note*"), 3.3, 70.5, 45.2, 21.0, key="plan01_notes"),
                 F("sb_edge_types", 50.5, 10.0, 46.2, 52.5),
                 F("sb_site_readings", 50.5, 64.0, 46.2, 27.5)],
         side="plan01_notes"),
    # 3 · SON page3 (axo x1.047, bottom zone rebuilt clear of the footer)
    dict(pid="p03", part="A", stage="an", title=u"Heights and enclosure",
         intro=u"Plan 01 as a parallel axonometric: *heights* are what the plan cannot show; the *sky view* from the "
               u"stream bed marks its *most enclosed* stretch.",
         frames=[F("sb_axo_what_is_there", 3.3, 10.0, 93.4, 72.0, key="axo"),
                 F(("sb_axo_what_is_there_legend", "sb_p03_legend*"), 3.3, 83.0, 55.0, 6.5, key="legend"),
                 F(("sb_axo_what_is_there_caption", "sb_axo_*", "sb_p03_*"), 3.3, 90.0, 56.0, 4.0, key="notes")],
         side="notes"),
    # 4 · SON page4 (P-7, U20): one scale for S1-S4, each note level with its cut
    dict(pid="p04", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses.",
         frames=[F(("sb_sec_keymap_p04", "*keymap*"), 7.0, 10.0, 72.0, 19.5, key="km"),
                 F(("sb_sec_legend_p04", "sb_sec_intro*"), 80.0, 10.0, 16.7, 20.0, key="legend"),
                 F("sb_sec_s1", 7.0, 31.0, 72.0, 18.5, same="cuts", note="n1"),
                 F("sb_sec_note_s1*", 80.0, 31.0, 16.7, 18.5, key="n1"),
                 F("sb_sec_s2", 7.0, 51.0, 72.0, 10.5, same="cuts", note="n2"),
                 F("sb_sec_note_s2*", 80.0, 51.0, 16.7, 10.5, key="n2"),
                 F("sb_sec_s3", 7.0, 63.0, 72.0, 18.5, same="cuts", note="n3"),
                 F("sb_sec_note_s3*", 80.0, 63.0, 16.7, 18.5, key="n3"),
                 F("sb_sec_s4", 7.0, 83.0, 72.0, 10.5, same="cuts", note="n4"),
                 F("sb_sec_note_s4*", 80.0, 83.0, 16.7, 10.5, key="n4")],
         side="legend"),
    # 5 · SON page5 (as page 4; inside the one margin set, P-6)
    dict(pid="p05", part="A", stage="an", title=u"Sections across the stream",
         intro=u"Cuts *across the Selinos stream*, each drawn *as it is*: the ground, the *bed and banks*, the "
               u"buildings, trees and fields it crosses.",
         frames=[F(("sb_sec_keymap_p05", "*keymap*"), 3.3, 10.0, 74.0, 18.5, key="km"),
                 F(("sb_sec_legend_p05", "sb_sec_intro*"), 79.0, 10.0, 17.7, 19.0, key="legend"),
                 F("sb_sec_s5", 3.3, 30.0, 74.0, 12.5, same="cuts", note="n5"),
                 F("sb_sec_note_s5*", 79.0, 30.0, 17.7, 12.5, key="n5"),
                 F("sb_sec_s6", 3.3, 44.0, 74.0, 14.5, same="cuts", note="n6"),
                 F("sb_sec_note_s6*", 79.0, 44.0, 17.7, 14.5, key="n6"),
                 F("sb_sec_s7", 3.3, 60.0, 74.0, 18.5, same="cuts", note="n7"),
                 F("sb_sec_note_s7*", 79.0, 60.0, 17.7, 18.5, key="n7"),
                 F("sb_sec_s8", 3.3, 80.0, 74.0, 13.5, same="cuts", note="n8"),
                 F("sb_sec_note_s8*", 79.0, 80.0, 17.7, 13.5, key="n8")],
         side="legend"),
    # 6 · SON page6 (one board drawing: map, cards, photos, right column)
    dict(pid="p06", part="A", stage="got", title=u"The stream edge and where we can build",
         intro=u"Both banks *every 4 m*, and the ground *open to change*: where the project *can build*.",
         frames=[F("sb_edge_build", 3.3, 10.0, 93.4, 80.0, key="edge"),
                 F(("sb_edge_build_*", "sb_p06_*"), 3.3, 90.5, 60.0, 3.5, key="notes")],
         side="notes"),
    # 7 · SON page7 (P-8, U19): maps x1.10 one scale, right column 16.9 %, each note level with its map
    dict(pid="p07", part="B", stage="an", title=u"How people use it",
         intro=u"*Shops* line Kınık Caddesi and Üç Kemer Caddesi, the *primary commercial spines*; *walking* and "
               u"*driving* today, street by street.",
         frames=[F("sb_movement", 3.3, 10.5, 75.0, 26.0, same="maps", note="n1"),
                 F("sb_mv_note_1*", 79.7, 10.7, 17.0, 25.5, key="n1"),
                 F("sb_walking_today", 3.3, 39.0, 75.0, 26.0, same="maps", note="n2"),
                 F("sb_mv_note_2*", 79.7, 39.0, 17.0, 25.5, key="n2"),
                 F("sb_driving_today", 3.3, 67.3, 75.0, 26.0, same="maps", note="n3"),
                 F("sb_mv_note_3*", 79.7, 67.3, 17.0, 25.5, key="n3")],
         side="n3"),
    # 8 · SON page8 (P-9 option A, U18): key map up beside the corridor, R1-R4 strip full width
    dict(pid="p08", part="B", stage="got", title=u"The stream joins the town where the shops already are",
         intro=u"One *corridor*: the shop streets, the *hidden stream* and the project from end to end; *who* comes "
               u"when; each *street cut* today and with the project.",
         frames=[F("cl_p08_corridor", 3.3, 10.0, 67.5, 25.5, note="corr_legend"),
                 F("cl_p08_corridor_legend", 72.0, 10.0, 24.7, 15.5, key="corr_legend"),
                 F(("sb_street_keymap*", "*keymap*"), 72.0, 26.0, 24.7, 7.5, key="km"),
                 F("cl_p08_shops", 72.0, 33.8, 24.7, 2.7, key="shops"),
                 F("cl_p08_who", 3.3, 37.0, 93.4, 31.0, note="who_notes"),
                 F(("cl_p08_who_legend", "cl_p08_who_note"), 3.3, 68.5, 93.4, 4.5, key="who_notes"),
                 F(("sb_street_title_n1", "sb_street_legend*"), 3.3, 73.5, 93.4, 3.5, key="street_legend"),
                 F(("sb_street_R*", "sb_street_sections"), 3.3, 77.5, 93.4, 16.5, key="streets", same="streets",
                   split="row", gap=8.0, foot=1.5)],     # S3: four cuts 8 mm apart at one shared scale
         side="who_notes"),
    # 9 · SON page9 + page10 (P-10, U16, U17): spine x0.69, windows above their cards, bottom band enlarged
    dict(pid="p09", part="B", stage="do", title=u"The streamside spine, hub by hub",
         intro=u"*Five bridge places* on existing bus stops, *walking hubs* with a *sub-hub in the bed*, one *transit "
               u"hub*: the spine along the Selinos, hub by hub.",
         frames=[F("cl_p09_spine", 3.3, 10.0, 48.0, 16.5, key="spine"),
                 F(("cl_p09_legend", "cl_p10_legend"), 53.0, 10.0, 43.7, 16.5, key="legend"),
                 F(("cl_p10_windows_head", "cl_p09_windows_head"), 3.3, 27.0, 60.0, 2.2, key="win_head"),
                 F("cl_p10_win_1", 3.3, 29.5, 17.5, 17.5, same="win"),
                 F("cl_p10_win_2", 22.0, 29.5, 17.5, 17.5, same="win"),
                 F(("cl_p10_win_3a", "cl_p10_win_3b", "cl_p10_win_3*"), 40.8, 29.5, 17.5, 17.5, same="win",
                   split="row", key="win_3"),
                 F("cl_p10_win_4", 59.6, 29.5, 17.5, 17.5, same="win"),
                 F("cl_p10_win_5", 78.4, 29.5, 18.3, 17.5, same="win"),
                 F(("cl_p09_card_K4", "cl_p09_card_1", "cl_p10_hub_1"), 3.3, 48.0, 17.5, 23.5, same="cards"),
                 F(("cl_p09_card_K3", "cl_p09_card_2", "cl_p10_hub_2"), 22.0, 48.0, 17.5, 23.5, same="cards"),
                 F(("cl_p09_card_T", "cl_p09_card_3", "cl_p10_hub_3"), 40.8, 48.0, 17.5, 23.5, same="cards"),
                 F(("cl_p09_card_K5", "cl_p09_card_4", "cl_p10_hub_4"), 59.6, 48.0, 17.5, 23.5, same="cards"),
                 F(("cl_p09_card_K6", "cl_p09_card_5", "cl_p10_hub_5"), 78.4, 48.0, 18.3, 23.5, same="cards"),
                 F("cl_p10_flood", 3.3, 74.0, 46.0, 19.5),
                 F("cl_p10_bank", 51.4, 74.0, 28.6, 19.5),
                 F("cl_p10_market", 82.0, 74.0, 14.7, 19.5)],
         side="legend"),
    # 10 · SON page11 (G6-1: panel 2 chart enlarged; the run stamp leaves, S7)
    dict(pid="p10", part="C", stage="an+got", title=u"The water balance",
         intro=u"How much *winter water* can we hold for the farms' *dry summer*, and at *what cost*?",
         frames=[F("wb_year", 3.3, 10.5, 93.4, 38.0, foot=3.0),
                 F("wb_curve", 3.3, 50.0, 53.0, 28.0, foot=3.0),
                 F("wb_store", 58.3, 50.0, 38.4, 28.0, foot=4.0),
                 F("wb_answer", 3.3, 79.5, 93.4, 14.0)],
         side="wb_answer"),
    # 11 · SON page12 (A-A' SKETCH; map legend off the map into the left column, G6-4)
    dict(pid="p11", part="C", stage="do", title=u"Collect, clean, hold",
         intro=u"*Collect* winter stream water and runoff at the upstream entry, *clean* it once in *lined reed "
               u"basins*, *hold* it in the ground for the dry summer; the clean stream leaves for the *farms outside*.",
         frames=[F(("wb_p12_map_legend", "p12_map_legend", "wb_p12_map_letters", "wb_p12_relief_note"), 3.3, 10.0,
                   13.0, 63.0, key="map_legend"),
                 F("p12_map", 17.0, 10.0, 51.0, 63.0, note="map_legend"),
                 F("p12_zoom", 24.0, 12.0, 26.0, 23.0, over=True),
                 F("p12_steps", 69.5, 10.0, 27.2, 14.5),
                 F("p12_coliforms", 69.5, 26.5, 27.2, 16.0),
                 F("p12_plants", 69.5, 44.0, 27.2, 11.5),
                 F("p12_why", 69.5, 57.0, 27.2, 9.5),
                 F(("wb_p12_conclusion", "p12_conclusion"), 69.5, 68.0, 27.2, 5.0, key="conclusion"),
                 F(("p12_section_head*", "p12_section_list*", "wb_p12_section_key", "p12_section_key*"), 3.3, 74.5,
                   17.0, 18.5, key="aa_list"),
                 F(("p12_section_sketch", "p12_section"), 21.4, 74.5, 35.0, 18.5, key="aa", note="aa_notes"),
                 # S5: the sketch is ~2.7:1, so the cut takes 35 % and its levels / caption / strip note sit beside it
                 F(("wb_p12_section_levels", "wb_p12_section_caption", "wb_p12_strip_note"), 57.5, 74.5, 26.5, 18.5,
                   key="aa_notes"),
                 F(("p12_keymap", "*keymap*"), 84.8, 74.5, 11.9, 7.0, key="km"),
                 F(("wb_p12_section_legend", "p12_section_legend*"), 84.8, 82.0, 11.9, 11.0, key="aa_legend")],
         side="aa_legend"),
    # 12 · SON page13 + page14 = r06_S02 (P-12, P-1): four SKETCH panels, legend strip above the footer
    dict(pid="p12", part="C", stage="do", title=u"The proposals in section",
         intro=u"Four cuts, *upstream to downstream*: each proposal *in section*, the winter water and the summer "
               u"strip, the reach of the *design flood (Q500)*.",
         frames=[F(("ps_panel_1", "ps_W1"), 3.3, 10.0, 46.4, 40.0, same="panels"),
                 F(("ps_panel_2", "ps_W2"), 50.3, 10.0, 46.4, 40.0, same="panels"),
                 F(("ps_panel_3", "ps_W3"), 3.3, 51.0, 46.4, 38.0, same="panels"),
                 F(("ps_panel_4", "ps_W4"), 50.3, 51.0, 46.4, 38.0, same="panels"),
                 F(("ps_caption*", "ps_intro_note*"), 3.3, 89.2, 60.0, 1.6, key="caption", opt=True),
                 F(("ps_legend_strip", "ps_legend"), 3.3, 90.9, 74.0, 2.8, key="legend"),
                 F(("ps_keymap_p12", "ps_keymap_*"), 80.0, 89.2, 16.7, 4.6, key="km")],
         side="legend"),
    # 13 · SON page15 = r06_S03 + animal column (P-11): one row per season, cut at one scale
    dict(pid="p13", part="C", stage="do", title=u"Four seasons on one cut",
         intro=u"*One cut, one viewpoint, four seasons*: the *water level* decides what the place becomes, which "
               u"plants are in *leaf or flower*, and which animals are about.",
         frames=[F("p15_hubkey", 3.3, 10.0, 12.0, 5.5),
                 F("p15_monthbar", 17.0, 10.0, 48.0, 5.5),
                 F("p15_season_winter", 3.3, 16.0, 67.0, 17.5, same="seasons"),
                 F("p15_season_spring", 3.3, 34.0, 67.0, 17.5, same="seasons"),
                 F("p15_season_summer", 3.3, 52.0, 67.0, 17.5, same="seasons"),
                 F("p15_season_autumn", 3.3, 70.0, 67.0, 17.5, same="seasons"),
                 F("p15_feel*", 72.0, 10.0, 13.5, 78.0, key="feel"),
                 F("p15_animals*", 87.0, 10.0, 9.7, 78.0, key="animals"),
                 F(("p15_keymap", "p13_keymap", "*keymap*"), 3.3, 88.5, 12.0, 5.5, key="km"),
                 F(("p15_caption*", "p15_scale*"), 17.0, 88.5, 50.0, 2.0, key="caption", opt=True)],
         side="animals"),
    # 14 · SON page16 (ACCURATE S4 NE; no horizontal dimension row; year chart kept)
    dict(pid="p14", part="C", stage="do", title=u"The S4 cut, north-east bank",
         intro=u"The north-east bank of S4: *seat steps* and a *raised promenade* over Q500 stay; the *planting follows "
               u"the days under water*, the use follows the months.",
         frames=[F(("p16_keymap", "p14_keymap", "*keymap*"), 3.3, 10.5, 30.0, 12.5, key="km"),
                 F("p16_section", 3.3, 24.0, 65.0, 28.5, note="parts"),
                 F("p16_section_inset", 35.0, 10.5, 17.0, 12.5),
                 F(("p16_parts", "p16_groups", "p16_bands"), 69.5, 10.5, 27.2, 42.0, key="parts"),
                 F("p16_year", 3.3, 54.0, 93.4, 39.5, foot=3.0)],
         side="parts"),
    # 15 · SON page17 (G6-1 only): six maps 2 x 3 at one scale, each legend in its column
    dict(pid="p15", part="C", stage="do", title=u"The senses and the water",
         intro=u"The *fade-out zones* and the *senses*, zone by zone, *upstream to downstream*.",
         frames=[F("mp_sn_zones", 3.3, 10.0, 35.7, 27.0, same="sn", note="k_zones"),
                 F("mp_sn_zones_key", 39.5, 10.0, 10.0, 27.0, key="k_zones"),
                 F("mp_sn_feeling", 50.3, 10.0, 35.7, 27.0, same="sn", note="k_feeling"),
                 F("mp_sn_feeling_wheel", 86.5, 10.0, 10.2, 10.0),
                 F("mp_sn_feeling_key", 86.5, 21.0, 10.2, 16.0, key="k_feeling"),
                 F("mp_sn_sound", 3.3, 38.5, 35.7, 27.0, same="sn", note="k_sound"),
                 F("mp_sn_sound_key", 39.5, 38.5, 10.0, 27.0, key="k_sound"),
                 F("mp_sn_smell", 50.3, 38.5, 35.7, 27.0, same="sn", note="k_smell"),
                 F("mp_sn_smell_key", 86.5, 38.5, 10.2, 27.0, key="k_smell"),
                 F("mp_sn_encounters", 3.3, 67.0, 35.7, 26.5, same="sn", note="k_enc"),
                 F("mp_sn_encounters_key", 39.5, 67.0, 10.0, 26.5, foot=16.5, key="k_enc"),
                 # one id for the diagram and the legend (masterplan p16_senses.py:1567 / :1649): diagram on top,
                 # the legend in the foot
                 F("mp_sn_history", 50.3, 67.0, 35.7, 26.5, same="sn", note="k_hist"),
                 F("mp_sn_photo_*", 86.5, 67.0, 10.2, 14.0, key="photos"),
                 F("mp_sn_history_key", 86.5, 82.0, 10.2, 11.5, key="k_hist")],
         side="k_hist"),
    # 16 · SON page18 (G6-1 + 23 overlaps): key map + legend left, plans A/B, middle row, species row
    dict(pid="p16", part="C", stage="do", title=u"Which plant goes where",
         intro=u"*Wet to dry, low to high*: rushes and loosestrife *at the water*, willow and tamarisk on the *banks "
               u"that flood*, shade trees and olives on the *dry tops*; reed and water mint only in *lined basins*.",
         frames=[F(("p18_keymap", "p16_keymap", "*keymap*"), 3.3, 10.5, 16.0, 18.5, key="km"),
                 F(("p18_plans_legend", "p16_plans_legend"), 3.3, 30.0, 16.0, 21.5, key="legend"),
                 F("p18_plan_A", 20.0, 10.0, 21.0, 31.5, same="plans", note="list_A"),
                 F("p18_plan_A_list", 20.0, 42.0, 21.0, 9.5, key="list_A"),
                 F("p18_plan_B", 42.0, 10.0, 54.7, 38.5, same="plans", note="list_B"),
                 F("p18_plan_B_list", 42.0, 49.0, 54.7, 3.0, key="list_B"),
                 F("p18_bands", 3.3, 53.0, 17.0, 14.0, foot=2.5),
                 F("p18_band_shares", 21.0, 53.0, 10.5, 14.0, foot=4.0),
                 F("p18_foliage_shares", 32.0, 53.0, 10.5, 14.0, foot=4.0),
                 F("p18_heights", 43.0, 53.0, 53.7, 14.0),
                 F("p18_card_*", 3.3, 68.0, 93.4, 23.5, key="cards", split="row", same="cards"),
                 F("p18_catalogue_sources", 3.3, 92.0, 70.0, 1.8, key="cat_src")],      # S5: the cards' source marks
         side="legend"),
    # 17 · NEW = r06_S01 (SKETCH plant ladder)
    dict(pid="p17", part="C", stage="do", title=u"One plant ladder, streambed to field",
         intro=u"One cut from the *stream to the farms*, through the year: what the *water* does and what *people* do "
               u"on each step.",
         frames=[F("ag3_chain", 3.3, 9.5, 93.4, 9.8),
                 F("ag3_ladder_high", 3.3, 20.0, 93.4, 15.0, same="ladder"),
                 F("ag3_ladder_low", 3.3, 36.0, 93.4, 15.0, same="ladder"),
                 F("ag3_ladder_harvest", 3.3, 52.0, 93.4, 15.0, same="ladder"),
                 F(("ag3_note*", "ag3_remove*", "ag3_odour*"), 3.3, 69.0, 18.0, 24.5, key="notes"),
                 F("ag3_bands", 23.0, 69.0, 73.7, 24.5)],          # S7: the photos sit inside ag3_bands
         side="notes"),
    # 18 · SON page19 (G6-1 + 16 overlaps): four rows, one right line at x 60
    dict(pid="p18", part="C", stage="do", title=u"Where the clean water goes, and what it grows",
         intro=u"Clean water to *farmland outside the site*, easing an *overused aquifer*, *never drinking water*; "
               u"*same storage, different crops*: the *hectares* each crop irrigates.",
         frames=[F("wb_farms", 3.3, 10.0, 55.0, 20.5, foot=2.5),
                 F("wb_farms_out", 60.0, 10.0, 36.7, 20.5),
                 F("wb_decision", 3.3, 32.0, 30.0, 15.5, foot=2.5),
                 F("ag1_stream", 35.0, 32.0, 61.7, 15.5),
                 F("ag1_bars", 3.3, 49.0, 55.0, 25.0),
                 F("ag1_context", 60.0, 49.0, 36.7, 25.0),
                 F(("ag1_reading*", "ag2_farms"), 3.3, 76.0, 30.0, 17.5, key="reading"),
                 F("ag1_history", 35.0, 76.0, 30.0, 17.5),
                 F("ag1_crops_*", 67.0, 76.0, 29.7, 17.5, key="crops")],
         side="ag1_context"),
    # 19 · SON page20 (heritage symbols in the brown ramp, S3); legends in one row under the board
    dict(pid="p19", part="D", stage="do", title=u"The heritage loop",
         intro=u"The Selinos is the *seam*: *bridges, crafts and events* tie the *Kale side* to the *bazaar side*.",
         frames=[F("sb_heritage_loop", 3.3, 10.0, 93.4, 76.0, key="loop", noscale=True),
                 F(("sb_heritage_loop_legend", "sb_heritage_legend"), 3.3, 87.0, 93.4, 4.5, key="legend"),
                 F(("sb_heritage_loop_caption", "sb_heritage_*"), 3.3, 92.0, 50.0, 1.8, key="caption")],
         side="legend"),
    # 20 · SON page21 (base map kept; legend regrouped by category; proposals drawn, S8)
    dict(pid="p20", part="E", stage="do", title=u"Masterplan: an ecological corridor",
         intro=u"The whole project on one plan: *walking hubs*, *reed basins* and terraces that *hold the rain*, "
               u"*calmed streets*, along the Selinos as an *ecological corridor*.",
         frames=[F("mp_plan_r1", 3.3, 10.0, 69.0, 38.5, same="mp"),
                 F("mp_plan_r2", 3.3, 50.0, 69.0, 39.5, same="mp"),
                 F("mp_plan_legend*", 73.0, 10.0, 23.7, 40.0, key="legend"),      # S8: one legend per category
                 F(("mp_plan_moves_head", "mp_plan_moves"), 73.0, 51.0, 23.7, 18.0, key="moves"),
                 F(("mp_plan_cch*",), 73.0, 70.0, 23.7, 8.0, key="cch"),
                 F(("mp_plan_left*", "mp_plan_places_head", "mp_plan_places"), 73.0, 79.0, 23.7, 10.5, key="places"),
                 F("mp_plan_caption", 3.3, 90.5, 50.0, 1.8, key="caption")],
         side="places"),
    # 21 · SON page22 (P-13, U15): plans, each section as wide as its plan at its own round scale, key map in the band
    dict(pid="p21", part="E", stage="do", title=u"The water edge at 1:1,000",
         intro=u"Two windows, each *plan with its section*: the *upstream entry* (collect, clean, hold) and *Üç Kemer "
               u"Köprüsü* with Demeter's Garden.",
         frames=[F("mp_dt_*upstream", 3.3, 10.0, 45.7, 43.0, key="d1", same="dplans"),
                 F("mp_dt_*k5", 50.0, 10.0, 46.7, 43.0, key="d2", same="dplans"),
                 F("mp_dt_*upstream_sec", 3.3, 54.0, 45.7, 20.0, key="s1", foot=2.5,
                   note="leg1"),
                 F("mp_dt_*k5_sec", 50.0, 54.0, 46.7, 25.0, key="s2", foot=2.5, note="leg2"),
                 F(("mp_dt_keymap", "*keymap*"), 38.0, 75.0, 11.0, 13.0, key="km"),
                 F(("mp_dt_*upstream_leg*", "mp_dt_*upstream_route", "mp_dt_*upstream_why"), 3.3, 75.0, 34.0, 18.0,
                   key="leg1"),
                 F(("mp_dt_*k5_leg*", "mp_dt_*k5_route", "mp_dt_*k5_why"), 50.0, 79.5, 46.7, 14.0, key="leg2")],
         side="leg2"),
    dict(pid="p22", kind="sources", part="E", title=u"Sources"),
]
BK_REF_PAGE = "p13"          # D2 reference fill: "Four seasons on one cut" = round 6 p13 (PLAN §2.1)
