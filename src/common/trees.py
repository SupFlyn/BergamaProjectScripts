# ---- trees.py (round 6, S2, 4 Nov 2026; G6-10, Aras 17:54: "choose species for the trees according to the data that
# exists in our hands ... in a proper way"): ONE rule that gives every EXISTING tree a species, or "unspecified" where
# no data names one. Rule and evidence: revision_2026-11-04_round6/plan_findings/tree_species.md T2 (rows R0-R5).
# No survey crown carries a species. Each crown carries a LEAF TYPE (bergama_environment.json v2 trees rows: leaf
# 0 deciduous, 1 evergreen broadleaf, 2 needle-leaved; leaf_src 1 CLC+ class under the crown, 2 own Sentinel-2
# seasonality, 3 nearest CLC+ pixel). Species come from that leaf type plus where the tree stands, overridden where a
# site photo shows the tree. Every name except "unspecified" is an INFERENCE (inferred=True); the crown keeps its
# measured height and radius (never the species' typical size: pass existing trees as measured to the G6 height check).
#
#   tree_species(crown, bank=None, farm=None) -> (species_key, source_key, inferred)
#        crown = (x, y, r, h, leaf, leaf_src) tuple (env row order; shorter tuples fine) or a dict with those keys;
#        x, y in survey coordinates (the env file's / light DXF's); leaf None = a survey symbol with no crown (R5).
#        bank  = True when the crown is on a stream bank: the caller's near_stream(S, x, y, TREE_BANK_M) (R3a)
#        farm  = True on farmland / orchard / open hill (S.zones kind "agri" or sub "orchard"); False in the built
#                fabric; None unknown (counts as built: no olive claimed) (R2a/R2b)
#   TREE_SPECIES[key] -> dict(name, latin, glyph, leaf, legend, src)   glyph = the plants.py PLA_SPECIES key to draw
#        with, or None = no species drawing exists (draw the generic tree primitive, name it in the group + legend)
#   TREE_SOURCES[key] -> (text, url or None, public)   register with tree_sources(ix) (Sources page)
#   tree_grp(eid, species_key) -> ("trees", "<name> <eid>")   G6-9 group of one tree: ix_tag(*tree_grp(i, sp), shapes)
#   tree_legend(counts) -> [(species_key, legend text)]   counts {key: n} -> rows, named species first, then the
#        unspecified ones (legend swatch: hues GRN r1 for trees, P-3)
#   tree_log(page, counts) -> "trees <page> species=n generic=n"   n = trees with a named species / unspecified ones
TREE_BANK_M = 15.0          # R3a bank band (m from the stream line): INFERRED, no source gives a number (tree_species.md
                            # open item 2); callers pass near_stream(S, x, y, TREE_BANK_M)
TREE_NAMED_M = 5.0          # R0: a crown or symbol this close to a photographed tree takes its species

# R0: trees shown in site photos, matched to survey symbols by photo bearings (tree_species.md T1.3, INFERRED position)
TREE_NAMED = [((29842.0, 32305.0), "plane"),       # Ulu Camii gate N of K4: IMG_5794, IMG_5798 (Nil N5, Begüm B3)
              ((29862.0, 32298.1), "cypress")]     # the two cypresses there (same photos); (29858.7, 32311.7) unresolved
# photographed stands: (camera xy, view bearing deg from north clockwise, reach m, half field of view deg, key)
# reach INFERRED ~60 m (tree_species.md R1); half view 26.5 deg = a 24 mm-equivalent portrait frame (T1.3)
TREE_STANDS = [((29685.5, 32516.6), 235.0, 60.0, 26.5, "stone_pine"),   # IMG_5774 umbrella pine grove above the road
               ((29629.5, 32631.6), 253.0, 60.0, 26.5, "poplar")]       # IMG_5752 poplars by the houses (north end)
TREE_PRECINCT = ((29852.0, 32305.0), 30.0)   # Ulu Camii precinct (centre of the R0 points, radius INFERRED 30 m):
                                             # needle-leaved crowns here = stone pine (desc.json 35, 40, 42)

TREE_SPECIES = {
    "plane": dict(name="Oriental plane", latin="Platanus orientalis", glyph="plane", leaf=0,
                  legend=u"Oriental plane (deciduous, on the banks)", src=("tree_photos", "tree_plane_banks", "clc")),
    "cypress": dict(name="Cypress", latin="Cupressus sp.", glyph=None, leaf=2,
                    legend=u"Cypress (Ulu Camii, site photo)", src=("tree_photos",)),
    "stone_pine": dict(name="Stone pine", latin="Pinus pinea", glyph="stone_pine", leaf=2,
                       legend=u"Stone pine (site photo)", src=("tree_photos", "clc")),
    "poplar": dict(name="Poplar", latin="Populus sp.", glyph=None, leaf=0,
                   legend=u"Poplar (site photo)", src=("tree_photos", "tree_riparian")),
    "olive": dict(name="Olive", latin="Olea europaea", glyph="olive", leaf=1,
                  legend=u"Olive (evergreen broadleaf on farmland)", src=("clc",)),
    "pine": dict(name="Pine, species unspecified", latin="", glyph="stone_pine", leaf=2,
                 legend=u"Needle-leaved, species unspecified", src=("clc",)),
    "evergreen": dict(name="Evergreen broadleaf, species unspecified", latin="", glyph="olive", leaf=1,
                      legend=u"Evergreen broadleaf, species unspecified", src=("clc",)),
    "deciduous": dict(name="Deciduous, species unspecified", latin="", glyph="plane", leaf=0,
                      legend=u"Deciduous, species unspecified", src=("clc",)),
    "tree": dict(name="Tree, species unspecified", latin="", glyph=None, leaf=None,
                 legend=u"Tree (survey symbol), species unspecified", src=("survey",)),
}
TREE_GENERIC = ("pine", "evergreen", "deciduous", "tree")
TREE_ORDER = ("plane", "cypress", "stone_pine", "poplar", "olive", "deciduous", "evergreen", "pine", "tree")
# R4: a crown whose leaf type is only the nearest CLC+ pixel (leaf_src 3, "the weakest evidence") never gets a name
TREE_DROP = dict(plane="deciduous", poplar="deciduous", olive="evergreen", stone_pine="pine")

TREE_SOURCES = {
    "clc": (u"Copernicus Land Monitoring Service, CLCplus Backbone 2021 (leaf type of each tree crown)",
            u"https://library.land.copernicus.eu/products/CLCplus_Backbone_2021_PUM_v1.html", True),
    "chm": (u"Meta and World Resources Institute (2024), High Resolution Canopy Height Maps (tree crowns, modelled)",
            u"https://registry.opendata.aws/dataforgood-fb-forests/", True),
    "tree_plane_banks": (u"Pipinis E. (2003), Analysis of stand structure, site requirements and potential "
                         u"utilization of Platanus orientalis, PhD thesis, Aristotle University of Thessaloniki",
                         u"https://phdtheses.ekt.gr/eadd/handle/10442/15084", True),
    "tree_riparian": (u"EU Red List of Habitats, G1.3 Mediterranean and Macaronesian riparian woodland",
                      u"https://projects.eionet.europa.eu/european-red-list-habitats/library/terrestrial-habitats/"
                      u"g.-forests/g1.3-mediterranean-and-macaronesian-riparian-woodland/download/en/1/"
                      u"G1.3%20Mediterranean%20and%20Macaronesian%20riparian%20woodland.pdf", True),
    "tree_photos": (u"Site photos, Group 6 site visit (IMG_5752, IMG_5774, IMG_5794, IMG_5798)", None, False),
    "survey": (u"Site survey, Bergama (course file): single-tree symbols", None, False),
}


def _tree_get(crown, i, key, default=None):
    if isinstance(crown, dict):
        return crown.get(key, default)
    return crown[i] if crown is not None and len(crown) > i else default


def _tree_in_stand(x, y, st):
    import math as _m
    (cx, cy), brg, reach, half = st[0], st[1], st[2], st[3]
    dx, dy = x - cx, y - cy
    d = _m.hypot(dx, dy)
    if d > reach:
        return False
    if d < 1e-6:
        return True
    a = _m.degrees(_m.atan2(dx, dy)) % 360.0        # bearing from north, clockwise
    return abs((a - brg + 180.0) % 360.0 - 180.0) <= half


def tree_species(crown, bank=None, farm=None):
    import math as _m
    x, y = float(_tree_get(crown, 0, "x")), float(_tree_get(crown, 1, "y"))
    leaf, src = _tree_get(crown, 4, "leaf"), _tree_get(crown, 5, "leaf_src")
    for (px, py), key in TREE_NAMED:                                       # R0
        if _m.hypot(x - px, y - py) <= TREE_NAMED_M:
            return key, "tree_photos", True
    if leaf is None:                                                       # R5
        return "tree", "survey", False
    leaf = int(leaf)
    key, sk = None, "clc"
    if leaf == 2:                                                          # R1
        (qx, qy), qr = TREE_PRECINCT
        if _m.hypot(x - qx, y - qy) <= qr or any(_tree_in_stand(x, y, s) for s in TREE_STANDS if s[4] == "stone_pine"):
            key, sk = "stone_pine", "tree_photos"
        else:
            key = "pine"
    elif leaf == 1:                                                        # R2a / R2b
        key = "olive" if farm is True else "evergreen"
    elif leaf == 0:                                                        # R3a / R3b / R3c
        if bank is True:
            key, sk = "plane", "tree_plane_banks"
        elif any(_tree_in_stand(x, y, s) for s in TREE_STANDS if s[4] == "poplar"):
            key, sk = "poplar", "tree_photos"
        else:
            key = "deciduous"
    else:
        return "tree", "survey", False
    if src is not None and int(src) == 3 and key in TREE_DROP:             # R4
        key, sk = TREE_DROP[key], "clc"
    return key, sk, key not in TREE_GENERIC


def tree_grp(eid, species_key):
    return "trees", u"%s %s" % (TREE_SPECIES.get(species_key, TREE_SPECIES["tree"])["name"], eid)


def tree_legend(counts):
    return [(k, TREE_SPECIES[k]["legend"]) for k in TREE_ORDER if counts.get(k)]


def tree_sources(ix, page=None, counts=None):
    """register the PUBLIC sources of the species used (counts None = all) on the Sources page; the team's own photos
    and the course survey are not credited there (standing rule "credit only public sources"); the legend names them"""
    keys = set(["chm"])
    for k in (TREE_ORDER if counts is None else [k for k in TREE_ORDER if counts.get(k)]):
        keys.update(TREE_SPECIES[k]["src"])
    for k in sorted(keys):
        t, u, pub = TREE_SOURCES[k]
        if pub:
            ix.source(k, t, u, page=page)
    return sorted(k for k in keys if TREE_SOURCES[k][2])


def tree_log(page, counts):
    gen = sum(n for k, n in counts.items() if k in TREE_GENERIC)
    sp = sum(n for k, n in counts.items() if k not in TREE_GENERIC)
    return u"trees %s species=%d generic=%d" % (page, sp, gen)
