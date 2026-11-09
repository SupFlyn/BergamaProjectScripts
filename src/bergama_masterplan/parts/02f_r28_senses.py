# ---- MIRAQUA round 28 Oct 2026 (masterplan v27): S1 the senses and the water, a new A3 sheet after p.15 (worker MP-senses). Shared pieces: common/r28_style.py,
# common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).

# ================================================================ v27 (MIRAQUA 28 Oct, S1): the senses and the water
# BRIEF v4 §3 (revision_2026-10-28/v4/BRIEF.md; PLAN §3 row S1): a new one-page A3 sheet, Bergama_senses_A3.pdf, with
# its own title, for the booklet right after "The S4 cut". Not analysis: what the fade-out programme areas give the
# senses, from the upstream entry to the downstream end, as SIX SEPARATE STRIPS on one page (never one stacked map):
# the base map (the stream and the fade-out zones, R28_ZONES) and five panels on the SAME strip frame, orientation
# and scale, so they compare side by side. G7: each strip is the whole analysis frame (site_alan) turned so the
# water runs left to right (the View of the corridor), at 1:20,000, the largest standard scale at which six strips
# fit the A3 page (1:10,000 strips are 52.9 mm tall: six need 317 mm of the 243 mm). G8: the calisma_alan outline in
# every strip (R28_STUDY_LINE), named in the base map's legend. Each panel in the language of its reference
# (v4/references): Feeling = emotion blots gathering at the hubs and thinning out (senses_ref1), Sound = one mark
# texture per source (ref5), Smell = contour rings round each source (ref4), Encounters = flow ribbons ending in
# vignettes watch / walk / touch / cross / remember (ref3), History = layered fade fields with one word (ref2); the
# zones as p.24's fade-out fields (p24_ref2, the same zone definitions and colours). Every source sits at a place of
# the masterplan's own data (hubs, sub-hubs, zones, bridges, roads, the corridor's moves, the water board's S4 cut);
# how strong each reads is a design reading (said on the sheet), never a measurement: no numbers on the panels.
SN_NAME = "Bergama_senses_A3.pdf"            # PLAN §3: fixed name, no version (the booklet's sheet page after p.15)
SN_TITLE = u"The senses and the water"
SN_KICKER = u"C   WATER   ·   WHAT WE DO WITH IT"   # the booklet's header line of p.15 (part C, stage "do")
SN_SCALE = 20000.0                           # every strip (R28_SCALES; see above)
SN_K = 1000.0 / SN_SCALE                     # page mm per survey m
SN_PW, SN_PH, SN_ML = 420.0, 297.0, 14.0     # the booklet's A3 page and margin (bergama_booklet PW, PH, ML)
SN_COLX = (14.0, 212.0)                      # the two cell columns: 6 booklet grid columns each (6 x 33 - 4 = 194 mm)
SN_ROWS = (34.0, 115.5, 197.0)               # cell tops, mm from the page top (the last cell ends at 273, the
SN_CW, SN_CH = 194.0, 76.0                   # booklet's footer rule is at 276: its footer stays free)
SN_TOP = 17.5                                # the strip frame's top below its cell's top, mm
SN_SIDE = 148.0                              # the cell's key column from the cell's left edge, mm (46 mm wide)
SN_PT = 25.4 / 72.0                          # mm per point
SN_TS = dict(kicker=8.0, title=24.0, panel=14.0, statement=9.5, label=7.5, small=7.0)   # pt: booklet T sizes
SN_INK, SN_INK2, SN_ACC, SN_RULE, SN_FRAME = "4A3F35", "6B645B", "8B3A3F", "B0AC9C", "D8D5CC"   # booklet colours
SN_DARK, SN_WATER, SN_WATER_MID = "2C2219", R28_OPEN["stream"], "5D7F8D"
# The water board's S4 cut (site board v48 05_build_terrain.py S4_WB, survey m): where its season rows put "Kermes
# stalls in the bed" and "feet in the strip"; the sheet takes the point where it crosses the stream line
SN_S4 = ((30616.354683, 30540.470648), (31489.513378, 31161.826317))
SN_ZONE_SHORT = {"reed": u"Reed basins", "terraces": u"Terraces", "hub": u"Hub squares", "subhub": u"Sub-hubs",
                 "demeter": u"Demeter's Garden", "forest": u"Forest corridor", "wetland": u"Wetland", "cafe": u"Café"}
# Feeling (senses_ref1's circular scale): four poles, active / passive up and down, positive / negative right and
# left; a mood's colour is its angle on the wheel (design readings). New colours for a new meaning, apart from each
# other (dE00 >= 26) and from the base map (>= 16)
# round 6 (G6-6, PLAN §2.6): moods are one category (PUB, public life): one hue, darker = more active / positive
SN_FEEL = ((0.0, hue("PUB", 2)), (90.0, hue("PUB", 1)), (180.0, hue("PUB", 3)), (270.0, hue("PUB", 4)))   # positive, active, negative, passive
SN_MOOD = {"lively": 45.0, "busy": 80.0, "play": 10.0, "calm": 305.0, "tense": 140.0, "hidden": 220.0}
# Sound (senses_ref5): one mark per source; round 6 (G6-6): each source in its category's hue (PLAN §2.6), the
# same hue as that category on every map of the page (reeds = the reed basins' WW r1)
SN_SOUND = (("traffic", u"Traffic", hue("CTX", 1)), ("wind", u"Wind", hue("CTX", 3)),     # legend order = the
            ("water", u"Running water", hue("WAT", 2)), ("reeds", u"Reeds", hue("WW", 1)),   # table's category
            ("birds", u"Birds", hue("GRN", 2)), ("voices", u"Market · Kermes", hue("PUB", 1)),   # order, then
            ("children", u"Children", hue("PUB", 2)))                                       # darker first
# Smell (senses_ref4): every source draws the same rings, so only the colour tells them apart: each source in the
# hue of the category it grows in (round 6, G6-6): reed beds = WW r1 (the reed basins), lavender = the terraces'
# planting GRN r2, Demeter's Garden AGR r2, olive harvest AGR r1, café PUB r3 (as the Zones map)
# v28.1 (D2, D6): reed beds = the lined basins only; water mint left out (it grows only in lined cells, not drawn here)
SN_SMELL = (("reeds", u"Reed beds", hue("WW", 1)),                 # legend order = category, then rank
            ("lavender", u"French lavender", hue("GRN", 2)),   # p.16's plant list (no rosemary there)
            ("olive", u"Olive harvest", hue("AGR", 1)), ("demeter", u"Demeter's Garden", hue("AGR", 2)),
            ("cafe", u"Café", hue("PUB", 3)))
# Encounters: their marks and colours are P16_EXP (pages/p16_senses.py); round 6: the unused SN_EXP / _SN_MK gone
SN_HER = hue("HER", 3)                       # History: round 6 (G6-6, Q5): heritage browns; the light shade unless
                                             # the place has a sourced status (p16 _p16_her_col, HER_RANK)

