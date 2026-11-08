# -*- coding: utf-8 -*-
# Data for bergama_plan_to_rhino (v1, 8 Nov 2026). Optional: the script has the same table built in.
# SVG top group (its id in Illustrator, without _2 / 1 copies; matched by its start) -> layer under masterplan.
# proposal_<thing> = what the project adds, existing_<thing> = what is on the site (Aras 8 Nov 09:50-09:51 UTC).
# "texts" = the texts group: each text goes to texts_<layer of what it names>. First match wins.
LAYER_MAP = [
    ("green_around_the_zone", "existing_green"),
    ("heritage", "existing_heritage"),
    ("ground", "existing_topography"),
    ("topo", "existing_topography"),
    ("water", "proposal_water"),
    ("duvar", "existing_walls"),
    ("survey_walls", "existing_walls"),
    ("roads", "existing_roads"),
    ("houses", "existing_housing"),
    ("places", "proposal_places"),
    ("walks", "proposal_paths"),
    ("paths", "proposal_paths"),
    ("people", "proposal_people"),
    ("trees", "proposal_green"),
    ("planting", "proposal_green"),
    ("terraces", "proposal_terraces"),
    ("annotations", "proposal_annotations"),
    ("sheet", "sheet"),
    ("texts", "texts"),
]
