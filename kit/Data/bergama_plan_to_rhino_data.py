# -*- coding: utf-8 -*-
# Data for bergama_plan_to_rhino (v2.1, 9 Nov 2026; same table as built into bergama_plan_to_rhino_v2_1.py). Optional: the script has the same table built in.
# SVG group (its id in Illustrator, without _2 / 1 copies; matched by its start) -> layer under masterplan.
# Wrapper groups (Layer_N, no id) are looked through; an inner group naming another layer gets that layer.
# A Layer_N key matches that exact id only.
# proposal_<thing> = what the project adds, existing_<thing> = what is on the site (Aras 8 Nov 09:50-09:51 UTC).
# "texts" = the texts group: each text goes to texts_<layer of what it names>. First match wins.
LAYER_MAP = [
    ("green_around_the_zone", "existing_green"),
    ("green_corridor", "proposal_green_corridor"),    # v2.1: 25 m green corridor (inside ground_topt)
    ("old_settlement", "proposal_heritage_setting"),  # v2.1: the rings round Kizil Avlu (inside heritage)
    ("heritage_trail", "proposal_heritage_trail"),    # v2.1 (before "heritage")
    ("heritage", "existing_heritage"),
    ("ground", "existing_topography"),
    ("topo", "existing_topography"),
    ("wetland", "proposal_wetland"),                  # v2.1 (inside water_drainage_wall)
    ("selinos", "proposal_water"),                    # v2.1
    ("water", "proposal_water"),
    ("su_duvar", "existing_walls"),                   # v2.1
    ("duvar", "existing_walls"),
    ("survey_walls", "existing_walls"),
    ("roads", "existing_roads"),
    ("houses", "existing_housing"),
    ("buildings", "existing_housing"),                # v2.1
    ("evler", "existing_housing"),                    # v2.1
    ("places", "proposal_places"),
    ("walks", "proposal_paths"),
    ("paths", "proposal_paths"),
    ("seconder", "proposal_park_paths"),              # v2.1: legend "Park paths"
    ("Layer_16", "proposal_plaza"),                   # v2.1: Layer_N keys match that exact id only (event plaza)
    ("circulation", "proposal_route"),                # v2.1: CIRCULATION, route_line / footbridges / arrows
    ("route", "proposal_route"),
    ("ramps", "proposal_ramps"),                      # v2.1
    ("assets", "proposal_assets"),                    # v2.1: his placed asset drawings
    ("people", "proposal_people"),
    ("trees", "proposal_green"),
    ("planting", "proposal_green"),
    ("plan_rosemary", "proposal_green"),              # v2.1
    ("terraces", "proposal_terraces"),
    ("annotations", "proposal_annotations"),
    ("label_around", "texts_existing_context"),       # v2.1: context labels round the site (outlined text)
    ("labels", "texts_proposal_places"),              # v2.1: the 27 place callouts (outlined text)
    ("legend", "sheet"),                              # v2.1
    ("sheet", "sheet"),
    ("texts", "texts"),
]
