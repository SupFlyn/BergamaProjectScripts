# ---- round 4 (S3, 1 Nov 2026; D1, D4, D6 states, D7, G-R4-5.2, G-R4-5.8, G-R4-6): ONE vector drawing per species for
# every plan, section, view, axo (pla_axo) and the p17 catalogue: white willow v2, print-quality crowns of two-tone
# leaf masses with gaps, a shrub/flower low layer (pla_low_section / pla_low_plan), season= on every call (None =
# general; month= alias), crops and cells in their season state. Colours = round 3 values, all pending
# research/plant_colours.md (PLA_COLOUR_SRC; log FLAG). No cutouts or high-res silhouettes for plants any more.
# ---- plants (WO-T2b-3, 29 Oct 2026): every species of the revised planting as ONE primitive with two matching views,
# pla_section() (silhouette on the ground) and pla_plan() (top-view crown): same crown width, form and colour. Crops
# as rows at their spacing. Common reed and water mint only inside lined, off-line cells (D2 a, D6), never free.
# Needs section_parts.py (SEC, sec_ellipse, sec_water, _sec_mix, sct_hatch_fill) included before this file.
# Data: revision_2026-10-29/T1/ecology/species.json "species_data" (S-numbers as there) and RESULT.md §A-B.
# Removed by D6 and not offered: yellow flag iris, oleander, broadleaf cattail, white poplar, fig, citrus (and elm).
# Drawing size rules (the sources give ranges or only a maximum; data comments only, never printed):
#   height h_m  = middle of the sourced mature range; half of it where only a maximum is sourced.
#   crown crown_m = middle of the sourced spread; half of a sourced maximum; where no spread is sourced,
#                 h_m x PLA_FORM_RATIO[form] (rule read from the crown words in species.json).
#   clear stem, trunk width, lobes and stem counts: form rules in _pla_sec (drawing rules).
#   ("poly", ring, fill, stroke, lw)    ("line", pts, colour, lw)          page mm, y up; k = page mm per m

PLA_FORM_RATIO = dict(dome=1.0, oval=0.7, weeping=0.7, gnarled=0.9, umbrella=0.55, feathery=0.8, clump=0.6,
                      tussock=1.0, mound=1.2)   # crown / height where no spread is sourced (drawing rule)

PLA_LEAF_SITE = [4, 5, 6, 7, 8, 9, 10, 11]   # leaf-out 16 Apr, leaf-fall 14 Nov: site Sentinel-2 2019-2025 for all
                                             # broadleaved deciduous crowns (selinus_board_v50 LEAF_DOY; RESULT §B)
PLA_ALL_YEAR = list(range(1, 13))

PLA_PURPLE = "8C7088"     # palette SCHEMES D1 institutional / D5 civic: loosestrife purple (RESULT §A "purple, Jun-Sep")
PLA_REMOVE = "8B3A3F"     # palette CORE accent: the 'remove' cross on giant reed
PLA_FIELD = "C6C08D"      # palette MASTERPLAN agriculture light: field ground
PLA_ROW = "948B49"        # palette MASTERPLAN agriculture mid: crop rows
PLA_WET = "CBEDE5"        # palette MASTERPLAN wetland light: lined cell in plan
PLA_BOLL = "FAF8F1"       # palette CORE road: cotton bolls
PLA_FRUIT = "BC6F45"      # palette SCHEMES D1 commercial: tomato fruit
# round 4 (S3, G-R4-6): the greenery colours plants.py read from section_parts SEC, copied here with the same values so
# that no greenery colour lives outside this module (SEC's greenery keys can go at closing). Pending research as all.
PLA_LAV = "9F86C0"        # = SEC lav: chaste tree / French lavender flowers
PLA_REED_HEAD = "B49A6C"  # = SEC reed_head: reed plumes, rush tufts, maize tassels
PLA_CROP_LEAF = "8F9A68"  # = SEC grass: cotton, maize, tomato leaves
PLA_TRUNK = "7A6E60"      # = SEC trunk: stems and trunks
PLA_BEYOND = _sec_mix("7E8A57", SEC["paper"], 0.62)   # = SEC beyond (tree 7E8A57 toward paper): giant reed


def _pla_c(fill, accent=None, stem=None):
    """The colour set of one species: fill, edge, lighter lobes, stem, accent (same in both views)."""
    return dict(fill=fill, edge=SEC["ink2"], lt=_sec_mix(fill, SEC["paper"], 0.35), stem=stem or PLA_TRUNK,
                accent=accent)


# one entry per species (species.json species_data + giant reed from the screening); h_range = sourced (lo, hi) m
PLA_SPECIES = {
    "plane": dict(name="Oriental plane", turkish="Doğu çınarı", latin="Platanus orientalis", layer="tree",
                  form="dome", foliage="deciduous (S26)", status="keep",
                  h_range=(None, 30.0), h_m=15.0,            # "up to 30 m" S68, S69
                  crown_m=15.0,                              # "wider than 8 metres" S70: form rule 1.0 x h (>= 8)
                  bloom=[4, 5], leaf=PLA_LEAF_SITE,          # Apr-May S69 (secondary)
                  colours=_pla_c("637F48")),                  # round 3 species colour (D7; ΔE00 >= 12.7); every colour: PLA_COLOUR_SRC
    "ash": dict(name="Narrow-leaved ash", turkish="Dişbudak", latin="Fraxinus angustifolia", layer="tree",
                form="oval", foliage="deciduous (S7)", status="keep",
                h_range=(None, 40.0), h_m=20.0,              # "40-45m" maximum S7 (lower figure)
                crown_m=14.0,                                # "dense, irregular and dome shaped" S7: rule 0.7 x h
                bloom=[], leaf=PLA_LEAF_SITE,                # "early spring or even in autumn" S7: no months
                colours=_pla_c("3E6C5D")),                # round 3: blue-green
    "willow": dict(name="White willow", turkish="Ak söğüt", latin="Salix alba", layer="tree",
                   form="weeping", foliage="deciduous (not quoted)", status="keep",
                   h_range=(None, 30.0), h_m=15.0,           # "up to 30 m" S4
                   crown_m=10.5,                             # crown not found: rule 0.7 x h
                   bloom=[], leaf=PLA_LEAF_SITE,             # "spring" catkins S4: no months
                   colours=_pla_c("A9B88A")),                   # round 3: silvery light green
    "olive": dict(name="Olive", turkish="Zeytin", latin="Olea europaea", layer="tree",
                  form="gnarled", foliage="evergreen (S72)", status="keep",
                  h_range=(8.0, 15.0), h_m=11.5,             # "8-15 m" S72
                  crown_m=10.35,                             # crown not found: rule 0.9 x h
                  bloom=[4], leaf=PLA_ALL_YEAR,              # full bloom 21-24 Apr, ends 29 Apr-1 May S73 (Ege Univ.)
                  colours=_pla_c("7D8C80")),                  # round 3: grey-green
    "stone_pine": dict(name="Stone pine", turkish="Fıstık çamı", latin="Pinus pinea", layer="tree",
                       form="umbrella", foliage="evergreen conifer (S74)", status="keep (processionary caterpillar)",
                       h_range=(25.0, 30.0), h_m=27.5,       # "25-30 m" S74
                       crown_m=15.1,                         # "umbrella-shaped ... flat and broad" S74: rule 0.55 x h
                       bloom=[], leaf=PLA_ALL_YEAR,          # pollen months not found
                       colours=_pla_c("31432E")),              # round 3: deep green
    "tamarisk": dict(name="Tamarisk", turkish="Ilgın", latin="Tamarix smyrnensis", layer="tree",
                     form="feathery", foliage="deciduous (S9b, genus)", status="keep (replaces oleander)",
                     h_range=(4.0, 15.0), h_m=9.5,           # "4-15 m" S9b (genus)
                     crown_m=7.6,                            # "broad, bushy" S9b: rule 0.8 x h
                     bloom=[], leaf=PLA_LEAF_SITE,           # bloom not found for T. smyrnensis
                     colours=_pla_c("9AA9B3")),                # round 3: glaucous blue-grey
    "chaste": dict(name="Chaste tree", turkish="Hayıt", latin="Vitex agnus-castus", layer="shrub",
                   form="multistem", foliage="deciduous (S58)", status="keep (replaces oleander, fig, citrus)",
                   h_range=(1.0, 3.0), h_m=2.0,              # "1-3 m" S58
                   crown_m=2.0,                              # "1.5-2.5 m" S67 (RHS, UK)
                   bloom=[6, 7, 8, 9], leaf=PLA_LEAF_SITE,   # "(Apr-)Jun-Sep" S58 (Crete); Apr-May occasional
                   colours=_pla_c("928955", PLA_LAV)),       # round 3: khaki; flower colour not sourced: section_style lav
    "rosemary": dict(name="Rosemary", turkish="Biberiye", latin="Salvia rosmarinus", layer="shrub",
                     form="mound", foliage="evergreen (S58, S71)", status="keep",
                     h_range=(0.5, 1.0), h_m=0.75,           # "50-100 cm" S58 (Crete)
                     crown_m=0.75,                           # "1.5-2.5 m" S71 for 1.5-2.5 m plants: scaled to h
                     bloom=[1, 2, 3, 4, 5], leaf=PLA_ALL_YEAR,  # "Jan-May, intermittently to Dec" S58
                     colours=_pla_c("5E6356")),                # round 3: dark grey-green
    "lavender": dict(name="French lavender", turkish="Karabaş otu", latin="Lavandula stoechas", layer="ground",
                     form="mound", foliage="evergreen (UNVERIFIED)", status="keep",
                     h_range=(0.3, 0.8), h_m=0.55,           # "30-80 cm" S58
                     crown_m=0.66,                           # crown not found: rule 1.2 x h
                     bloom=[3, 4, 5], leaf=[],               # "Mar-May" S58; evergreen unverified: no leaf months
                     colours=_pla_c("B6AFC3", PLA_LAV)),      # round 3: lilac grey; flowers as sec_lavender
    "loosestrife": dict(name="Purple loosestrife", turkish="Aklar otu", latin="Lythrum salicaria", layer="emergent",
                        form="clump", foliage="herbaceous perennial", status="keep, flower heads cut in Sep (D6)",
                        h_range=(0.3, 2.4), h_m=1.35,        # "0.3-2.4 m" S19
                        crown_m=0.75,                        # "5 feet (1.5 m) wide" mature S19: half the maximum
                        bloom=[6, 7, 8, 9], leaf=[],         # "June ... September" S19; cut Sep (D6)
                        colours=_pla_c("5C9D74", PLA_PURPLE)),     # round 3: fresh blue-green
    "soft_rush": dict(name="Soft rush", turkish="UNVERIFIED", latin="Juncus effusus", layer="emergent",
                      form="clump", foliage="not found", status="new (replaces iris and cattail)",
                      h_range=(0.5, 1.5), h_m=1.0,           # "5-15 dm tall" S59
                      crown_m=0.6,                           # "tufted, cespitose" S59: rule 0.6 x h
                      bloom=[5, 6, 7, 8], leaf=[],           # "late May-Aug, occasionally Sep" S59 (USA)
                      colours=_pla_c("7C9A2E")),               # round 3: rush green
    "rush": dict(name="Sharp rush", turkish="Kofa", latin="Juncus acutus", layer="emergent",
                 form="tussock", foliage="not found", status="keep, away from paths and the wading strip",
                 h_range=(0.6, 1.0), h_m=0.8,                # "(40-)60-100 cm" S65
                 crown_m=0.8,                                # "dense tussock" S60, S65: rule 1.0 x h
                 bloom=[], leaf=[],                          # "summer" S65 (NZ): no months
                 colours=_pla_c("515B26")),                # round 3: dark olive
    "reed": dict(name="Common reed", turkish="Kamış", latin="Phragmites australis", layer="emergent",
                 form="stand", foliage="deciduous (S2)", status="lined off-line basins only (D2 a): pla_reed_basin",
                 h_range=(None, 6.0), h_m=3.0,               # "may reach 20 feet (6 m)" S2 (booklet drew 1.9-2.2 m)
                 crown_m=None,                               # clonal stand, no crown
                 bloom=[7, 8, 9, 10, 11], leaf=[],           # "July to November" S2 (range-wide); plumes cut before Nov
                 colours=_pla_c("C2A873", PLA_REED_HEAD)),   # round 3: straw (ΔE00 12.4 to the free-planted species)
    "mint": dict(name="Water mint", turkish="Su nanesi", latin="Mentha aquatica", layer="emergent",
                 form="mound", foliage="deciduous (S57)", status="lined basin cells only (D6): pla_mint_cell",
                 h_range=(0.3, 0.8), h_m=0.55,               # "30-80 cm" S58
                 crown_m=0.75,                               # "spread 0.5-1 m" S57
                 bloom=[5, 6, 7, 8, 9], leaf=[],             # "May-Sep" S58
                 colours=_pla_c("5F9C9E")),                # round 3: blue mint green (ΔE00 12.8)
    "giant_reed": dict(name="Giant reed", turkish="Kargı", latin="Arundo donax", layer="emergent",
                       form="cane", foliage="not found", status="REMOVE (raises flood risk, S36)",
                       h_range=(None, None), h_m=None, crown_m=None,   # not in species_data: pass h_m and crown_m
                       bloom=[], leaf=[],
                       colours=_pla_c(PLA_BEYOND, PLA_REMOVE)),
}

# crops: row spacing only where sourced (library/research/crops_2026-10-24, card f506; no other spacing in library/)
PLA_CROPS = {
    "olive": dict(name="Olive orchard", row_m=7.0, plant_m=5.0,   # Kaya et al. 2017 Irrig. Drain. 66(5) p.821:
                  h_m=None, crown_m=None),     # Memecik "planted 5 × 7 m apart" (order of the pair not stated)
    "cotton": dict(name="Cotton", row_m=None, plant_m=None, h_m=None, crown_m=None),   # not found: pass spacing
    "maize": dict(name="Maize (corn)", row_m=None, plant_m=None, h_m=None, crown_m=None),   # not found
    "tomato": dict(name="Tomato (processing)", row_m=None, plant_m=None, h_m=None, crown_m=None),   # not found
}


def pla_months(key):
    """Sourced months (1-12) of a species: bloom, in leaf and flower-head cut (empty lists where not sourced)."""
    sp = PLA_SPECIES[key]
    return dict(bloom=list(sp["bloom"]), leaf=list(sp["leaf"]), cut=[9] if key == "loosestrife" else [])


# ---- round 4 (S3, D6, G-R4-6; PLAN §4.9, §2.1): seasons, states and colours ------------------------------------------
# Every plant call takes season= (None = the general state; "winter" Dec-Feb, "spring" Mar-May, "summer" Jun-Aug,
# "autumn" Sep-Nov); month= (1-12) is kept as an alias that maps to its season. The STATE of a species in a season
# comes from its sourced months only (leaf list, bloom list, flower heads cut; CHK5_6 §4): a deciduous species with no
# leaf month in the season is bare (winter: branches with open gaps, round 3 D7); spring = after leaf-out (fresh
# tint); autumn = before leaf-fall (warm tint); flowers where a bloom month falls in the season and is not a cut
# month. The general state = the species in leaf with its flowers (U69). COLOURS: the round 3 values are kept as they
# are (Aras 1 Nov 11:42, N2 halted till 2 Nov): none is sourced yet, every colour entry carries src = PLA_COLOUR_SRC
# and the log prints "FLAG plant colours pending research". Next round fills PLA_SPECIES colours, the two tints and
# the crop colours from research/plant_colours.md (one data edit here). Never alpha.
PLA_COLOUR_SRC = "pending research/plant_colours.md"
PLA_SEASONS = ("winter", "spring", "summer", "autumn")
PLA_SEASON_MONTHS = dict(winter=(12, 1, 2), spring=(3, 4, 5), summer=(6, 7, 8), autumn=(9, 10, 11))
PLA_SPRING = "B8C77A"      # fresh leaf tint (round 3 drawing rule, kept; colour pending research)
PLA_AUTUMN = "C29A55"      # autumn tint (round 3 drawing rule, kept; colour pending research)
PLA_TINT = dict(spring=PLA_SPRING, autumn=PLA_AUTUMN)
PLA_TINT_T = dict(spring=0.22, autumn=0.35)   # round 3 month tints (Apr .30 May .15 / Sep .15 Oct .35 Nov .55) averaged
PLA_SEASON = dict(season=None)   # pla_season(s): every plant call without season= / month= draws season s
PLA_BARE_DRAWN = set()
# where each species' STATES come from (colours: PLA_COLOUR_SRC for all); the S-numbers as in species.json
PLA_STATE_SRC = dict(
    plane="leaf: site Sentinel-2 leaf-out 16 Apr, leaf-fall 14 Nov (RESULT §B); bloom Apr-May S69",
    ash="leaf: site Sentinel-2; bloom 'early spring or even in autumn' S7 (no months: no flowers drawn)",
    willow="leaf: site Sentinel-2; catkins 'spring' S4 (no months: none drawn)",
    olive="evergreen S72; full bloom 21-24 Apr S73; harvest 6-14 Nov (Kaya 2017)",
    stone_pine="evergreen conifer S74",
    tamarisk="leaf: site Sentinel-2 (deciduous S9b, genus); bloom not sourced",
    chaste="leaf: site Sentinel-2 (deciduous S58); bloom (Apr-)Jun-Sep S58",
    rosemary="evergreen S58, S71; bloom Jan-May S58",
    lavender="evergreen UNVERIFIED; bloom Mar-May S58",
    loosestrife="herbaceous perennial; bloom Jun-Sep S19; heads cut Sep (D6); winter state not sourced",
    soft_rush="bloom late May-Aug S59; winter state not sourced",
    rush="bloom 'summer' S65 (no months); winter state not sourced",
    reed="deciduous S2; plumes Jul-Nov S2, cut before Nov S11",
    mint="deciduous S57; bloom May-Sep S58 (no flower colour)",
    giant_reed="remove (S36)",
)
PLA_SOURCES = dict((k_, dict((s_, dict(colour=PLA_COLOUR_SRC, state=PLA_STATE_SRC.get(k_, "")))
                             for s_ in (None,) + PLA_SEASONS)) for k_ in PLA_SPECIES)


def pla_season_of(season=None, month=None):
    """the season name of season= or month= (a month 1-12 maps to its season); None = the general state"""
    if season is not None:
        if season not in PLA_SEASONS:
            raise ValueError("plants: season is None or one of %s, not %r" % (", ".join(PLA_SEASONS), season))
        return season
    if month:
        m = int(month)
        for s_ in PLA_SEASONS:
            if m in PLA_SEASON_MONTHS[s_]:
                return s_
        raise ValueError("plants: month %r is not 1-12" % month)
    return None


def pla_season(season=None):
    """sets the season (a name, or a month 1-12 = its season; None = general) every plant call without its own
    season= / month= draws in; returns the previous season (pla_season(old) restores it)"""
    old = PLA_SEASON["season"]
    if isinstance(season, (int, float)) and not isinstance(season, bool):
        PLA_SEASON["season"] = pla_season_of(month=season) if season else None
    else:
        PLA_SEASON["season"] = pla_season_of(season or None)
    return old


def _pla_s(season=None, month=None):
    """the season of one call: its own season= / month=, else the one set by pla_season"""
    if season is not None or month:
        return pla_season_of(season, month)
    return PLA_SEASON["season"]


def _pla_deciduous(sp):
    return sp["foliage"].startswith("deciduous") and bool(sp["leaf"])


def pla_state(key, season=None):
    """the sourced state of species `key` in a season: dict(bare, tint, bloom, season) (PLA_STATE_SRC)"""
    sp = PLA_SPECIES[key]
    if season is None:
        return dict(bare=False, tint=None, bloom=bool(sp["colours"].get("accent")), season=None)
    ms = PLA_SEASON_MONTHS[season]
    cut = pla_months(key)["cut"]
    dec = _pla_deciduous(sp)
    bare = dec and not any(m in sp["leaf"] for m in ms)
    tint = season if dec and not bare and season in PLA_TINT else None
    bloom = any(m in sp["bloom"] and m not in cut for m in ms)
    return dict(bare=bare, tint=tint, bloom=bloom, season=season)


def pla_colours(key, season=None, beyond=False, layer=0, month=None):
    """THE plant colour call (G-R4-6): the colour set of species `key` in `season` (None = general; month= alias):
    fill (lit face), shade (mass body), lt (light fleck), edge, stem, bark, accent (flowers; None out of bloom; giant
    reed keeps its 'remove' cross), plus bare (draw the winter structure), bloom, season and src (the colour source:
    PLA_COLOUR_SRC until research/plant_colours.md). beyond / layer: paler beyond the cut and with depth (fig_fade).
    Opaque colours only."""
    sp = PLA_SPECIES[key]
    s_ = _pla_s(season, month)
    st = pla_state(key, s_)
    c = dict(sp["colours"])
    if st["tint"]:
        c["fill"] = _sec_mix(c["fill"], PLA_TINT[st["tint"]], PLA_TINT_T[st["tint"]])
        c["lt"] = _sec_mix(c["fill"], SEC["paper"], 0.35)
    if key != "giant_reed" and c.get("accent") and not st["bloom"]:
        c["accent"] = None
    c["shade"] = _sec_mix(c["fill"], c["edge"], 0.25)
    if beyond:
        c = dict((k_, _sec_mix(v, SEC["paper"], 0.55) if v else v) for k_, v in c.items())
    c = _pla_layer_cols(c, layer)
    bark = _sec_mix(sp["colours"]["fill"], sp["colours"]["stem"] or PLA_TRUNK, 0.6)   # species-tinted twigs
    if beyond:
        bark = _sec_mix(bark, SEC["paper"], 0.55)
    c["bark"] = _pla_layer_cols(dict(b=bark), layer)["b"]
    c.update(bare=st["bare"], bloom=st["bloom"], season=s_, src=PLA_COLOUR_SRC)
    return c


def pla_colour(key, month=None, beyond=False, layer=0, season=None):
    """round 3 name, kept for its callers: = pla_colours(key, season, beyond, layer, month)"""
    return pla_colours(key, season, beyond=beyond, layer=layer, month=month)


def _pla_status(bare_key=None):
    """keeps the one plants status line in PLA_LOG: "plants: no alpha; bare n species (keys)" """
    if bare_key:
        PLA_BARE_DRAWN.add(bare_key)
    ln = u"plants: no alpha; bare %d species%s" % (len(PLA_BARE_DRAWN), (u" (%s)" % u", ".join(sorted(PLA_BARE_DRAWN)))
                                                    if PLA_BARE_DRAWN else u"")
    for i, s_ in enumerate(PLA_LOG):
        if s_.startswith(u"plants: no alpha"):
            PLA_LOG[i] = ln
            return
    PLA_LOG.append(ln)


# bare branch architecture per form (drawing rules): clear stem (fraction of h), main limbs (count, spread deg),
# upward pull, child count, length ratio, pendulous whips
PLA_BARE_FORM = dict(
    dome=dict(lo=0.30, limbs=4, spread=110.0, up=0.15, kids=(2, 3), ratio=(0.62, 0.76)),
    oval=dict(lo=0.30, limbs=3, spread=55.0, up=0.45, kids=(2, 3), ratio=(0.64, 0.78)),
    feathery=dict(lo=0.0, limbs=4, spread=45.0, up=0.35, kids=(2, 2), ratio=(0.60, 0.72)),
    multistem=dict(lo=0.0, limbs=5, spread=70.0, up=0.40, kids=(2, 2), ratio=(0.55, 0.70)),
)


def _pla_bare_sec(form, x, gy, h, w, k, c, seed=0):
    """winter section of a deciduous tree: trunk and recursive branches as tapering lines inside the crown
    envelope, the open gaps between them showing (D7); the willow's winter state is _pla_willow2_sec(bare=True)"""
    import math as _m
    F = PLA_BARE_FORM.get(form, PLA_BARE_FORM["dome"])
    H, R = h * k, w / 2.0 * k
    rnd = _pla_rng(seed * 13 + 5)
    col = c["bark"]
    tw = max(0.12, h / 60.0 * k)
    lo = F["lo"] * H
    ex, ey = x, gy + lo + 0.5 * (H - lo) if lo else gy + 0.55 * H
    erx, ery = R, (0.5 * (H - lo) if lo else 0.45 * H)
    D = 3 if H < 8.0 else (4 if H < 20.0 else 5)
    sh = []

    def inside(px, py):
        return py <= gy + H and ((px - ex) / erx) ** 2 + ((py - ey) / ery) ** 2 <= 1.0 or py < ey and abs(px - ex) <= erx

    def grow(px, py, ang, L, wd, d):
        tx, ty = px + L * _m.cos(ang), py + L * _m.sin(ang)
        n_ = 0
        while not inside(tx, ty) and n_ < 6:
            L *= 0.8
            tx, ty = px + L * _m.cos(ang), py + L * _m.sin(ang)
            n_ += 1
        j = 0.08 * L * (rnd() - 0.5)
        mx, my = px + 0.5 * L * _m.cos(ang) - j * _m.sin(ang), py + 0.5 * L * _m.sin(ang) + j * _m.cos(ang)
        sh.append(("line", [(px, py), (mx, my), (tx, ty)], col, max(0.05, wd)))
        if d >= D:
            return
        nk = F["kids"][0] + (1 if rnd() < 0.4 and F["kids"][1] > F["kids"][0] else 0)
        for i in range(nk):
            off = (i - 0.5 * (nk - 1)) / max(1.0, 0.5 * (nk - 1) + 0.5) * _m.radians(28.0 + 14.0 * rnd())
            a = ang + off
            a = a + F["up"] * (_m.pi / 2.0 - a) * 0.5        # pull toward upright
            r_ = F["ratio"][0] + (F["ratio"][1] - F["ratio"][0]) * rnd()
            grow(tx, ty, a, L * r_, wd * 0.62, d + 1)

    if lo:                                           # trunk up to the first fork, tapering
        fy = gy + lo + 0.08 * (H - lo)
        sh.append(("poly", [(x - tw, gy), (x + tw, gy), (x + 0.6 * tw, fy), (x - 0.6 * tw, fy)], col, None, 0.0))
        base, L0 = (x, fy), 0.42 * (H - lo)
    else:                                            # stems from the ground
        base, L0 = (x, gy), 0.50 * H
    nl = F["limbs"]
    for i in range(nl):
        t = (i / float(nl - 1)) - 0.5 if nl > 1 else 0.0
        a = _m.pi / 2.0 + _m.radians(F["spread"]) * t + _m.radians(10.0) * (rnd() - 0.5)
        grow(base[0] + (0.15 * tw * t if lo else 0.12 * R * t), base[1], a, L0 * (0.85 + 0.25 * rnd()),
             (1.1 * tw if lo else 0.5 * tw), 1)
    return sh


def _pla_bare_plan(cx, cy, r, c, seed=0):
    """winter plan of a deciduous crown: main branches radiating and forking, open between them, the trunk dot"""
    import math as _m
    rnd = _pla_rng(seed * 17 + 3)
    col = c["bark"]
    sh = []

    def grow(px, py, ang, L, wd, d):
        tx, ty = px + L * _m.cos(ang), py + L * _m.sin(ang)
        if _m.hypot(tx - cx, ty - cy) > r:
            s_ = r / _m.hypot(tx - cx, ty - cy)
            tx, ty = cx + (tx - cx) * s_, cy + (ty - cy) * s_
        sh.append(("line", [(px, py), (tx, ty)], col, max(0.05, wd)))
        if d < 3:
            for o in (-0.45, 0.4):
                grow(tx, ty, ang + o + 0.2 * (rnd() - 0.5), L * 0.62, wd * 0.6, d + 1)
    n = 5 + int(rnd() * 2.999)
    for i in range(n):
        grow(cx, cy, 2 * _m.pi * (i + 0.3 * rnd()) / n, 0.45 * r, max(0.08, 0.05 * r), 1)
    sh.append(("poly", sec_ellipse(cx, cy, max(0.2, 0.06 * r), max(0.2, 0.06 * r), 10), col, None, 0.0))
    return sh


def _pla_bare_draw(key, sp, x, g, h, w, k, c, seed, plan=False):
    """the winter structure of a species (willow v2 skeleton or the form's branch architecture), counted bare"""
    _pla_status(key)
    if key == "willow":
        return _pla_willow2_plan(x, g, w / 2.0 * k, c, seed, bare=True) if plan else \
            _pla_willow2_sec(x, g, h, w, k, c, seed, bare=True)
    if plan:
        return _pla_bare_plan(x, g, w / 2.0 * k, c, seed)
    return _pla_bare_sec(sp["form"], x, g, h, w, k, c, seed)


def pla_bare(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0, layer=0, month=None, plan=False,
             season=None):
    """D7 winter tree: species `key` without leaves as its branch structure with the open gaps between branches, in
    its species-tinted bark colour, true size (section: ground at (x, gy); plan=True: crown centred on (x, gy) page
    mm), paler beyond / with depth. season / month default winter. Opaque lines and the trunk only. Returns shapes."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    if h_m is not None:
        h = pla_height_ok(key, h)
    s_ = _pla_s(season, month) or "winter"
    c = pla_colours(key, s_, beyond=beyond, layer=layer)
    _pla_count(key, s_)
    if plan:
        return _pla_bare_draw(key, sp, x, gy, h, w, k, c, seed, plan=True)
    sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
    g = gy(x) if callable(gy) else gy
    return _pla_bare_draw(key, sp, x, g, h, w, k * sc, c, seed)


def _pla_rnd(i, s=0):
    """A fixed pseudo-random number in [0, 1)."""
    import math as _m
    v = _m.sin(i * 12.9898 + s * 78.233) * 43758.5453
    return v - _m.floor(v)


def _pla_crown(cx, cy, rx, up, dn, seed=0, wob=0.08, n=40):
    """A lobed crown outline: rx each side, up above and dn below cy; its widest points stay at cx +- rx."""
    import math as _m
    L = 2 * (3 + int(_pla_rnd(seed, 1) * 3))       # even lobe count: full width kept at a = 0 and pi
    out = []
    for i in range(n):
        a = 2 * _m.pi * i / n
        f = 1.0 - wob * _m.sin(L * a / 2.0) ** 2
        s = _m.sin(a)
        out.append((cx + rx * f * _m.cos(a), cy + (up if s > 0 else dn) * f * s))
    return out


# ---- round 4 (S3, D4, G-R4-6): print-quality crowns. Every crown = several overlapping, irregular leaf masses with
# open gaps between them; each mass in tones of its species (shade body with a fine edge, lit face toward the upper
# left, a small light fleck); trunk and main limbs drawn first so they show in the gaps. Plan and section are built
# from the same masses. Counts, sizes, offsets and the light direction are drawing rules, not data.
def _pla_mass(mx, my, rx, up, dn, c, seed, wob=0.2, edge=True):
    """one leaf mass centred (mx, my), rx each side, up above, dn below: shade body, lit face, light fleck"""
    sh = [("poly", _pla_crown(mx, my, rx, up, dn, seed, wob), c["shade"], c["edge"] if edge else None,
           0.06 if edge else 0.0)]
    sh.append(("poly", _pla_crown(mx - 0.12 * rx, my + 0.10 * up, 0.74 * rx, 0.78 * up, 0.55 * dn, seed + 1, wob),
               c["fill"], None, 0.0))
    sh.append(("poly", _pla_crown(mx - 0.30 * rx, my + 0.34 * up, 0.30 * rx, 0.30 * up, 0.24 * dn, seed + 2, wob),
               c["lt"], None, 0.0))
    return sh


def _pla_cloud(cx, cy, rx, ry, n, c, seed, wob=0.2, size=0.46, flat=1.0):
    """a crown of n leaf masses inside the ellipse (cx, cy, rx, ry) (page mm), the upper masses first so the lower
    ones overlap them; returns (shapes, masses [(x, y, rx, ry)])"""
    rnd = _pla_rng(seed * 19 + 7)
    pts = _pla_marks_in(cx, cy, (1.0 - 1.1 * size) * rx, (1.0 - 1.1 * size) * ry, n, rnd)
    ms = []
    for i, (px, py) in enumerate(pts):
        f = 0.82 + 0.36 * rnd()
        ms.append((px, py, size * rx * f, size * ry * f * flat, i))
    ms.sort(key=lambda m_: -m_[1])
    sh = []
    for px, py, mrx, mry, i in ms:
        sh += _pla_mass(px, py, mrx, mry, 0.85 * mry, c, seed * 7 + 3 * i, wob)
    return sh, [(m_[0], m_[1], m_[2], m_[3]) for m_ in ms]


# ---- white willow v2 (round 4, D1, S3): ONE drawing for every section, plan, axo, the p17 catalogue and winter, from
# the p17 catalogue photo (Commons "A big white willow tree (Salix alba) at the bay of lake Juojärvi in Tuusniemi,
# Finland, 2018 September": a massive leaning trunk forking low into heavy spreading limbs). One skeleton
# (_pla_willow2_skel): a stout leaning trunk, four arching limbs, two branches per limb, twigs. In leaf: a leaf mass at
# every branch end (_pla_mass), open gaps where the limbs show, the weeping fringe hanging from each mass. Winter: the
# same skeleton bare with fine hanging whips. Height: drawing size 15 m inside the sourced "up to 30.00 m" [35];
# crown 0.7 x h (rule: no sourced width, flagged). Proportions are drawing rules. Replaces the round 3 willow
# (its section, plan, mass table and the bare "weeping" whips), all deleted.
PLA_WILLOW_LIMBS = ((-0.72, 0.60), (-0.30, 0.84), (0.18, 0.90), (0.68, 0.64))   # limb tips (dx / R, y / H)


def _pla_willow2_skel(x, gy, H, R, seed):
    """the willow skeleton in section, page mm, mirrored on odd seeds: (trunk ring, branches [(pts, lw)],
    ends [(x, y, depth)], twigs [(pts, lw)])"""
    import math as _m
    rnd = _pla_rng(seed * 7 + 11)
    s = -1.0 if seed % 2 else 1.0
    tw = max(0.2, H / 36.0)                         # stout trunk: 1/18 of the height wide at the foot (rule)
    fx, fy = x + s * 0.12 * R, gy + 0.24 * H        # the low fork the trunk leans to
    trunk = [(x - 1.35 * tw, gy), (x + 1.35 * tw, gy), (x + tw + s * 0.04 * R, gy + 0.10 * H),
             (fx + 0.8 * tw, fy), (fx - 0.8 * tw, fy), (x - tw + s * 0.04 * R, gy + 0.10 * H)]

    def cx_(v):
        return max(x - 0.97 * R, min(x + 0.97 * R, v))
    br, ends, twigs = [], [], []
    for dx, ty in PLA_WILLOW_LIMBS:
        lx = cx_(x + s * dx * R * (0.94 + 0.12 * rnd()))
        ly = min(gy + ty * H * (0.95 + 0.08 * rnd()), gy + 0.93 * H)
        mx, my = 0.5 * (fx + lx), 0.5 * (fy + ly) + 0.06 * H     # limbs arch upward
        br.append(([(fx, fy), (mx, my)], 1.1 * tw))
        br.append(([(mx, my), (lx, ly)], 0.65 * tw))
        ends.append((lx, ly, 1))
        o = 1.0 if lx >= fx else -1.0
        px, py = mx + 0.6 * (lx - mx), my + 0.6 * (ly - my)
        for ax, ay in ((0.18, -0.08), (-0.12, 0.10)):           # one branch out and down, one up and in
            bx = cx_(lx + o * ax * R * (0.8 + 0.4 * rnd()))
            by = min(gy + 0.96 * H, ly + ay * H * (0.8 + 0.4 * rnd()))
            br.append(([(px, py), (0.5 * (px + bx), 0.5 * (py + by) + 0.02 * H), (bx, by)], 0.35 * tw))
            ends.append((bx, by, 2))
    for ex, ey, _d in ends:                         # twigs: two or three short ones from every end
        for j in range(2 + int(rnd() * 1.999)):
            a = 1.2 + 0.75 * j + 0.4 * rnd()
            L = (0.07 + 0.06 * rnd()) * R
            twigs.append(([(ex, ey), (cx_(ex + L * (1.0 if j % 2 else -1.0) * abs(_m.cos(a))),
                                     min(gy + H, ey + 0.6 * L))], 0.06))
    return trunk, br, ends, twigs


def _pla_willow2_sec(x, gy, h, w, k, c, seed=0, bare=False):
    """white willow v2 in section, h tall and w wide (m), ground at (x, gy) page mm; bare = the winter state"""
    H, R = h * k, w / 2.0 * k
    trunk, br, ends, twigs = _pla_willow2_skel(x, gy, H, R, seed)
    rnd = _pla_rng(seed * 5 + 3)
    col = c["bark"] if bare else c["stem"]
    sh = [("poly", trunk, col, None, 0.0)] + [("line", p, col, max(0.06, lw)) for p, lw in br]
    if bare:                                        # winter: twigs and fine hanging whips, open gaps between them
        sh += [("line", p, col, lw) for p, lw in twigs]
        for p, _lw in twigs:
            tx, ty = p[-1]
            yb = max(gy + 0.15 * H, ty - (0.15 + 0.15 * rnd()) * H)
            o = 1.0 if tx >= x else -1.0
            sh.append(("line", [(tx, ty), (tx + o * 0.02 * R, 0.5 * (ty + yb)), (tx + o * 0.03 * R, yb)], col, 0.05))
        return sh
    strand = _sec_mix(c["shade"], c["edge"], 0.35)
    ms = []
    for i, (ex, ey, d) in enumerate(ends):
        f = 0.85 + 0.30 * rnd()
        mrx = (0.24 if d == 1 else 0.18) * R * f
        up = (0.11 if d == 1 else 0.09) * H * f
        ey = min(ey, gy + H - up)
        ms.append((ex, ey, mrx, up, i))
    ms.sort(key=lambda m_: -m_[1])                  # upper masses first: the lower ones overlap them
    for mx, my, mrx, up, i in ms:
        sh += _pla_mass(mx, my, mrx, up, 0.8 * up, c, seed * 13 + 3 * i, 0.22)
        n_ = max(4, int(mrx / max(0.3, 0.04 * R)))   # the weeping fringe hanging from the mass
        for j in range(n_):
            t = -0.85 + 1.7 * (j + 0.5 * rnd()) / n_
            px = mx + t * mrx
            top = my - 0.55 * up * (1.0 - t * t) ** 0.5
            yb = max(gy + 0.18 * H, top - (0.10 + 0.15 * rnd()) * H)
            lean = (0.02 + 0.02 * rnd()) * R * (1.0 if px >= x else -1.0)
            if j % 2 == 0:
                wd = 0.05 * mrx + 0.05
                sh.append(("poly", [(px - wd, top), (px + wd, top), (px + lean + 0.15 * wd, yb),
                                    (px + lean - 0.15 * wd, yb)], c["shade"] if j % 4 == 0 else c["fill"], None, 0.0))
            else:
                sh.append(("line", [(px, top), (px + 0.5 * lean, 0.5 * (top + yb)), (px + lean, yb)], strand, 0.06))
    return sh


def _pla_willow2_plan(cx, cy, r, c, seed=0, bare=False):
    """white willow v2 from above, crown radius r (page mm) on (cx, cy): the same four limbs and their branches
    radiating, a leaf mass at every end (outer first, the crown top last), strand ticks round the rim; bare = winter"""
    import math as _m
    rnd = _pla_rng(seed * 5 + 9)
    a0 = 2 * _m.pi * rnd()
    col = c["bark"] if bare else c["stem"]
    lw0 = max(0.10, 0.05 * r)
    sh, ends = [], []
    for i in range(4):
        a = a0 + 2 * _m.pi * (i / 4.0 + 0.10 * (rnd() - 0.5))
        lx, ly = cx + 0.62 * r * _m.cos(a), cy + 0.62 * r * _m.sin(a)
        sh.append(("line", [(cx, cy), (lx, ly)], col, lw0))
        ends.append((lx, ly, 1, a))
        for o in (-0.38, 0.38):
            b = a + o + 0.1 * (rnd() - 0.5)
            bx, by = lx + 0.24 * r * _m.cos(b), ly + 0.24 * r * _m.sin(b)
            sh.append(("line", [(lx, ly), (bx, by)], col, 0.6 * lw0))
            ends.append((bx, by, 2, b))
    if bare:
        for ex, ey, _d, a in ends:
            for o in (-0.3, 0.3):
                sh.append(("line", [(ex, ey), (ex + 0.08 * r * _m.cos(a + o), ey + 0.08 * r * _m.sin(a + o))], col,
                           0.06))
        sh.append(("poly", sec_ellipse(cx, cy, max(0.2, 0.06 * r), max(0.2, 0.06 * r), 10), col, None, 0.0))
        return sh
    for ex, ey, d, a in sorted(ends, key=lambda e_: -e_[2]):     # outer branch ends first
        mr = (0.26 if d == 1 else 0.20) * r * (0.85 + 0.3 * rnd())
        sh += _pla_mass(ex, ey, mr, mr, mr, c, seed * 11 + int(100 * a), 0.22)
        if d == 2:                                  # the fringe seen from above: short ticks past the mass
            for j in range(4):
                b = a + 0.35 * (j - 1.5)
                p0 = (ex + 0.75 * mr * _m.cos(b), ey + 0.75 * mr * _m.sin(b))
                sh.append(("line", [p0, (p0[0] + 0.12 * r * _m.cos(b), p0[1] + 0.12 * r * _m.sin(b))], c["shade"],
                           0.07))
    sh += _pla_mass(cx, cy, 0.30 * r, 0.30 * r, 0.30 * r, c, seed + 7, 0.2)
    return sh


# tree crowns per form (drawing rules): clear stem / h, masses in section, masses in plan, mass size, flatness, limbs
PLA_CROWN = dict(dome=(0.30, 9, 7, 0.44, 1.0, 4), oval=(0.28, 8, 6, 0.46, 1.0, 3),
                 gnarled=(0.30, 7, 6, 0.46, 0.85, 3), umbrella=(0.65, 8, 7, 0.36, 0.80, 4),
                 feathery=(0.0, 9, 8, 0.38, 1.0, 4))


def _pla_tree_sec(form, x, gy, h, w, k, c, seed=0):
    """a tree in section (round 4, D4): trunk and main limbs, then the crown of overlapping two-tone leaf masses
    with open gaps (_pla_cloud); h tall, w crown wide (m), ground at (x, gy) page mm"""
    lo_f, n, _np, size, flat, nl = PLA_CROWN[form]
    H, R = h * k, w / 2.0 * k
    st = c["stem"]
    tw = max(0.15, h / 60.0 * k)                    # half trunk width: trunk 1/30 of the height (rule)
    sh = []
    if form == "feathery":                          # tamarisk: slender stems from the ground into an airy crown
        cy, ry = gy + 0.62 * H, 0.38 * H
        for i in range(4):
            t = (i - 1.5) / 1.5
            sh.append(("line", [(x + t * 0.05 * R, gy), (x + t * 0.25 * R, gy + 0.35 * H),
                                (x + t * 0.55 * R, cy)], st, max(0.08, 0.6 * tw)))
    else:
        yb = gy + lo_f * H
        y0 = yb - 0.05 * (gy + H - yb)              # the crown starts a little below the first fork
        cy, ry = 0.5 * (y0 + gy + H), 0.5 * (gy + H - y0)
        if form == "gnarled":                       # olive: two twisting stems
            for s_ in (-1, 1):
                sh.append(("poly", [(x + s_ * 0.2 * tw, gy), (x + s_ * 1.6 * tw, gy),
                                    (x + s_ * (0.35 * R + 0.5 * tw), cy), (x + s_ * (0.35 * R - 0.5 * tw), cy)],
                           st, None, 0.0))
        else:
            lean = 0.03 * H if form == "umbrella" else 0.0
            sh.append(("poly", [(x - tw, gy), (x + tw, gy), (x + lean + 0.6 * tw, yb), (x + lean - 0.6 * tw, yb)],
                       st, None, 0.0))
        for i in range(nl):                         # main limbs into the crown, a side branch on each
            t = (2.0 * i / (nl - 1) - 1.0) if nl > 1 else 0.0
            ex, ey = x + 0.72 * R * t, cy + 0.45 * ry * (1.0 - abs(t))
            sh.append(("line", [(x, yb), (0.5 * (x + ex), 0.5 * (yb + ey) + 0.1 * ry), (ex, ey)], st,
                       max(0.08, 0.7 * tw)))
            o = 1.0 if t >= 0 else -1.0
            sh.append(("line", [(0.5 * (x + ex), 0.5 * (yb + ey) + 0.1 * ry),
                                (0.5 * (x + ex) + o * 0.2 * R, min(gy + H, ey + 0.4 * ry))], st, max(0.06, 0.4 * tw)))
    cl, ms = _pla_cloud(x, cy, R, ry, n, c, seed, size=size, flat=flat)
    sh += cl
    if form == "feathery":                          # hanging wisps under the masses
        for mx, my, mrx, mry in ms:
            for d in (-0.5, 0.0, 0.5):
                px, py = mx + d * mrx, my - 0.7 * mry
                sh.append(("line", [(px, py), (px + 0.04 * (px - x), py - 0.09 * H)], c["edge"], 0.06))
    return sh


def _pla_sec(form, x, gy, h, w, k, c, seed=0):
    """Section of one form, h tall and w crown wide (m), ground at (x, gy) page mm (round 4: print quality, D4)."""
    H, R = h * k, w / 2.0 * k
    f, e, ac = c["fill"], c["edge"], c.get("accent")
    sh = []
    if form == "weeping":                           # white willow v2 (D1)
        return _pla_willow2_sec(x, gy, h, w, k, c, seed)
    if form in PLA_CROWN:
        return _pla_tree_sec(form, x, gy, h, w, k, c, seed)
    rnd = _pla_rng(seed * 29 + 5)
    if form == "multistem":                         # chaste tree: stems fanning from the ground, a mass on each
        heads = ((-0.68, 0.58), (-0.36, 0.70), (0.0, 0.76), (0.34, 0.69), (0.68, 0.57))
        for dx, cy_ in heads:
            sh.append(("line", [(x + dx * 0.1 * R, gy), (x + dx * 0.55 * R, gy + 0.4 * cy_ * H),
                                (x + dx * R, gy + cy_ * H)], c["stem"], 0.15))
        for i, (dx, cy_) in sorted(enumerate(heads), key=lambda t_: -t_[1][1]):
            up = 0.22 * H * (0.9 + 0.2 * rnd())
            sh += _pla_mass(x + dx * R, gy + cy_ * H, 0.32 * R, up, 0.85 * up, c, seed * 5 + i, 0.16)
        if ac:                                      # flower spikes upright from the top of each mass
            for dx, cy_ in heads:
                top = gy + (cy_ + 0.20) * H
                for d in (-0.12, 0.0, 0.12):
                    px = x + (dx + d) * R
                    sh.append(("line", [(px, top - 0.14 * H), (px + 0.02 * R, top + 0.04 * H)], ac, 0.3))
        return sh
    if form == "mound":                             # lavender, rosemary, water mint: overlapping low masses
        for i, d in enumerate((-0.45, 0.42, 0.0)):
            up = (0.62 if d == 0.0 else 0.52) * H * (0.9 + 0.2 * rnd())
            sh += _pla_mass(x + d * R, gy + 0.36 * H, (0.52 if d == 0.0 else 0.50) * R, up, 0.36 * H, c,
                            seed * 3 + i, 0.12)
        if ac:                                      # flower spikes above the mound, a bract head on each
            for d in (-0.55, -0.25, 0.05, 0.32, 0.58):
                px, top = x + d * R, gy + (0.95 + 0.12 * rnd()) * H
                sh.append(("line", [(px, gy + 0.70 * H), (px + 0.05 * d * R, top)], c["stem"], 0.08))
                sh.append(("poly", sec_ellipse(px + 0.05 * d * R, top, 0.05 * R + 0.08, 0.08 * H + 0.1, 8), ac,
                           None, 0.0))
        else:                                       # needle-leaf strokes in the edge tone
            for d in (-0.55, -0.25, 0.05, 0.35, 0.6):
                sh.append(("line", [(x + d * R, gy + 0.45 * H), (x + d * R * 1.05, gy + 0.78 * H)], e, 0.07))
        return sh
    if form in ("clump", "tussock", "cane"):        # rushes and loosestrife: stems from one base; giant reed: canes
        n = dict(clump=15, tussock=23, cane=7)[form]
        for i in range(n):
            t = i / float(n - 1)
            hh = H * (0.80 + 0.20 * _pla_rnd(i, seed + 3))
            bx, tx = x + (2 * t - 1) * R * 0.15, x + (2 * t - 1) * R
            col = f if i % 3 else c["shade"]        # two tones through the clump
            if form == "clump":                     # soft arch
                mx = bx + (tx - bx) * 0.35
                sh.append(("line", [(bx, gy), (mx, gy + 0.55 * hh), (tx, gy + hh)], col, 0.12))
                if ac and i % 2 == 0:               # loosestrife flower spike on the upper stem
                    sh.append(("line", [(mx + (tx - mx) * 0.3, gy + 0.69 * hh), (tx, gy + hh)], ac, 0.35))
            else:
                sh.append(("line", [(bx, gy), (tx, gy + hh)], col, 0.15 if form == "cane" else 0.1))
                if form == "cane":                  # leaf blades along the cane
                    for j in range(1, 5):
                        py = gy + hh * j / 5.0
                        px = bx + (tx - bx) * j / 5.0
                        s_ = 1 if (i + j) % 2 else -1
                        sh.append(("line", [(px, py), (px + s_ * 0.35 * R, py - 0.06 * hh)], f, 0.1))
        if form == "cane" and ac:                   # marked for removal
            sh.append(("line", [(x - R, gy), (x + R, gy + H)], ac, 0.35))
            sh.append(("line", [(x - R, gy + H), (x + R, gy)], ac, 0.35))
        return sh
    raise ValueError("_pla_sec: unknown form %r" % form)


def _pla_plan(form, cx, cy, w, k, c, seed=0):
    """Top view of one form, crown w wide (m), centre (cx, cy) page mm: the same masses as the section (round 4)."""
    import math as _m
    r = w / 2.0 * k
    f, e, ac = c["fill"], c["edge"], c.get("accent")
    sh = []
    if form == "weeping":                           # white willow v2 (D1)
        return _pla_willow2_plan(cx, cy, r, c, seed)
    if form in PLA_CROWN:
        _lo, _n, n, size, _fl, nl = PLA_CROWN[form]
        for i in range(nl + 1):                     # limbs, seen in the gaps between the masses
            a = 2 * _m.pi * (i / float(nl + 1) + 0.2 * _pla_rnd(seed, 5))
            sh.append(("line", [(cx, cy), (cx + 0.7 * r * _m.cos(a), cy + 0.7 * r * _m.sin(a))], c["stem"],
                       max(0.08, 0.04 * r)))
        cl, _ms = _pla_cloud(cx, cy, r, r, n, c, seed, size=size + 0.04)
        sh += cl
        if form == "umbrella":                      # needle tufts round the flat crown
            for i in range(30):
                a = 2 * _m.pi * i / 30.0
                sh.append(("line", [(cx + 0.80 * r * _m.cos(a), cy + 0.80 * r * _m.sin(a)),
                                    (cx + 0.98 * r * _m.cos(a), cy + 0.98 * r * _m.sin(a))], c["lt"], 0.08))
        elif form == "feathery":                    # feathery sprays at the rim
            for i in range(24):
                a = 2 * _m.pi * i / 24.0
                sh.append(("line", [(cx + 0.82 * r * _m.cos(a), cy + 0.82 * r * _m.sin(a)),
                                    (cx + 0.82 * r * _m.cos(a + 0.12), cy + 0.82 * r * _m.sin(a + 0.12))], e, 0.07))
        return sh
    if form == "multistem":                         # five heads, as in section
        for i in range(5):
            a = 2 * _m.pi * (i / 5.0 + 0.05)
            hx, hy = cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a)
            sh += _pla_mass(hx, hy, 0.45 * r, 0.45 * r, 0.45 * r, c, seed + i, 0.12)
            if ac:
                for d in ((-0.15, 0.1), (0.12, 0.18), (0.0, -0.12)):
                    sh.append(("poly", sec_ellipse(hx + d[0] * r, hy + d[1] * r, 0.07 * r + 0.05, 0.07 * r + 0.05, 8),
                               ac, None, 0.0))
        return sh
    if form == "mound":
        for i, (dx, dy, s_) in enumerate(((-0.35, -0.2, 0.62), (0.32, -0.15, 0.6), (0.0, 0.25, 0.62))):
            sh += _pla_mass(cx + dx * r, cy + dy * r, s_ * r, s_ * r, s_ * r, c, seed + i, 0.1)
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + _pla_rnd(seed, 6))
            px, py = cx + 0.5 * r * _m.cos(a), cy + 0.5 * r * _m.sin(a)
            if ac:
                sh.append(("poly", sec_ellipse(px, py, 0.12 * r, 0.12 * r, 8), ac, None, 0.0))
            else:
                sh.append(("line", [(px, py), (px + 0.2 * r * _m.cos(a), py + 0.2 * r * _m.sin(a))], e, 0.07))
        return sh
    if form in ("clump", "tussock", "cane"):        # stems seen from above: a starburst in two tones
        n = dict(clump=15, tussock=23, cane=9)[form]
        for i in range(n):
            a = 2 * _m.pi * (i / float(n) + 0.3 * _pla_rnd(i, seed))
            ll = r * (0.8 + 0.2 * _pla_rnd(i, seed + 2))
            sh.append(("line", [(cx, cy), (cx + ll * _m.cos(a), cy + ll * _m.sin(a))], f if i % 3 else c["shade"],
                       0.12))
            if ac and form == "clump" and i % 2 == 0:
                sh.append(("poly", sec_ellipse(cx + ll * _m.cos(a), cy + ll * _m.sin(a), 0.08 * r + 0.1,
                                               0.08 * r + 0.1, 8), ac, None, 0.0))
        if form == "cane" and ac:
            d = r * 0.7
            sh += [("line", [(cx - d, cy - d), (cx + d, cy + d)], ac, 0.35),
                   ("line", [(cx - d, cy + d), (cx + d, cy - d)], ac, 0.35)]
        return sh
    raise ValueError("_pla_plan: unknown form %r" % form)


def _pla_get(key):
    if key not in PLA_SPECIES:
        raise ValueError("plants: unknown species %r (removed by D6, or not in species.json)" % key)
    if key in ("reed", "mint"):
        raise ValueError("plants: %s grows only in lined cells: use pla_reed_basin / pla_mint_cell" % key)
    return PLA_SPECIES[key]


def _pla_size(key, sp, h_m, crown_m):
    h, w = h_m or sp["h_m"], crown_m or sp["crown_m"]
    if h is None or w is None:
        raise ValueError("plants: %s has no sourced size: pass h_m and crown_m" % key)
    return h, w


PLA_LOG = []
# round 4 (S3) counters for the log lines (pla_log_lines): plants drawn per species / crop, species per season
PLA_COUNT = {}
PLA_SEASON_KEYS = {}


def _pla_count(key, season):
    PLA_COUNT[key] = PLA_COUNT.get(key, 0) + 1
    PLA_SEASON_KEYS.setdefault(season or "general", set()).add(key)


def pla_log_lines():
    """the plant log lines of this run (sec_look_lines prints them): willow v2 drawn n; plants drawn by species;
    plants season=<season> species n (one per season drawn; 'general' = no season); FLAG plant colours pending
    research (n species: every species and crop, until research/plant_colours.md fills the colours)"""
    out = [u"willow v2 drawn %d" % PLA_COUNT.get("willow", 0),
           u"plants drawn by species: " + (u", ".join(u"%s %d" % kv for kv in sorted(PLA_COUNT.items())) or u"none")]
    for s_ in ("general",) + PLA_SEASONS:
        if s_ in PLA_SEASON_KEYS:
            out.append(u"plants season=%s species %d" % (s_, len(PLA_SEASON_KEYS[s_])))
    n = len(PLA_SPECIES) + len([c_ for c_ in PLA_CROPS if c_ != "olive"])
    out.append(u"FLAG plant colours pending research (%d species): %s" % (n, PLA_COLOUR_SRC))
    return out


def pla_height_ok(key, h_m):
    """h_m (m) moved into the species' sourced range (G6; T1: the olive was drawn 5.0 m against 8-15 m); a change is
    logged once per species and value"""
    lo, hi = PLA_SPECIES[key]["h_range"]
    v = h_m
    if lo is not None and v < lo:
        v = lo
    if hi is not None and v > hi:
        v = hi
    if v != h_m:
        msg = u"Plants: %s asked at %.2f m, drawn %.2f m (sourced %s-%s m)" % (key, h_m, v, lo or "", hi or "")
        if msg not in PLA_LOG:
            PLA_LOG.append(msg)
    return v


def _pla_layer_cols(c, layer):
    f = globals().get("fig_fade")
    if not layer or f is None:
        return c
    return dict((k_, f(v, layer) if v else v) for k_, v in c.items())


def pla_section(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0, hires=True, style="b", layer=0,
                detail=True, month=None, season=None):
    """A species in section at true size: ground at (x, gy) page mm (gy may be a function of x). h_m outside the
    sourced range is moved into it (pla_height_ok). layer: D9 depth layer (0 true size; 1, 2 smaller and paler).
    Round 4 (S3, D4, G-R4-6): ONE vector drawing per species everywhere (print quality: two-tone leaf masses with
    gaps, trunk and limbs); `hires` and `style` are accepted and no longer change the drawing (no cutouts, no
    high-res silhouettes). season (None = general; month= alias) = the season's state and colours (pla_colours), a
    deciduous species out of leaf drawn bare. detail: leaf texture and flower marks (_pla_detail). Never alpha."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    if h_m is not None:
        h = pla_height_ok(key, h)
    g = gy(x) if callable(gy) else gy
    s_ = _pla_s(season, month)
    _pla_status()
    _pla_count(key, s_)
    c = pla_colours(key, s_, beyond=beyond, layer=layer)
    sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
    k = k * sc
    if c["bare"]:
        return _pla_bare_draw(key, sp, x, g, h, w, k, c, seed)
    sh = _pla_sec(sp["form"], x, g, h, w, k, c, seed)
    if detail:
        sh += _pla_detail(key, sp["form"], x, g, h, w, k, c, seed)
    return sh


def pla_plan(key, cx, cy, k, crown_m=None, beyond=False, seed=0, distinct=True, style="b", month=None, season=None):
    """The same species from above: crown crown_m wide (m) centred on (cx, cy) page mm, built from the same masses
    and colours as its section; distinct: the species' own mark on top (no two species share a plan symbol, M6).
    season (month= alias) = the season's colours, deciduous out of leaf = bare branches. Always opaque."""
    sp = _pla_get(key)
    w = crown_m or sp["crown_m"]
    if w is None:
        raise ValueError("plants: %s has no sourced crown: pass crown_m" % key)
    s_ = _pla_s(season, month)
    _pla_status()
    _pla_count(key, s_)
    c = pla_colours(key, s_, beyond=beyond)
    if c["bare"]:
        return _pla_bare_draw(key, sp, cx, cy, sp["h_m"] or w, w, k, c, seed, plan=True)
    sh = _pla_plan(sp["form"], cx, cy, w, k, c, seed)
    return sh + (_pla_plan_mark(key, cx, cy, w / 2.0 * k, c, seed) if distinct else [])


def pla_axo(key, x, y, k, h_m=None, crown_m=None, beyond=False, seed=0, layer=0, season=None, month=None,
            detail=False):
    """A species standing in an axo (p12, D1 'one drawing everywhere'): the section drawing of the module set upright
    at the projected base point (x, y) page mm, k = page mm per m of height at that point (a billboard, as an axo
    tree is drawn). Same willow v2 / species drawing as every section. Returns shapes (y up)."""
    return pla_section(key, x, y, k, h_m=h_m, crown_m=crown_m, beyond=beyond, seed=seed, layer=layer,
                       detail=detail, season=season, month=month)


# round 4 (S3, D4, D6): crop states by season from the sourced crop calendars (TAGEM region 28, PLA_CROP_SRC):
# cotton sown mid-Apr, to 21 Oct; maize sown Apr III / 1 May, to 2 Sep (TAGEM to Eki I); tomato (processing) planted
# Apr II / 15 May, to 27 Aug; olive orchard evergreen, harvest 6-14 Nov. Reading taken (drawing states, not data):
# spring = young plants; summer = grown (tomato with fruit, harvest to Aug); autumn = cotton ripe with open bolls
# (harvest to 21 Oct), maize and tomato harvested (stubble); winter = bare field; general = the crop in its character.
PLA_CROP_SRC = ("library/research/crops_2026-10-24/bergama_crops_irrigation_v1.md:388-400, 426-441 (TAGEM region 28);"
                " olive harvest :258 (Kaya 2017)")
PLA_CROP_STATE = dict(
    cotton=dict(general="ripe", winter="bare", spring="seedling", summer="growing", autumn="ripe"),
    maize=dict(general="growing", winter="bare", spring="seedling", summer="growing", autumn="harvested"),
    tomato=dict(general="fruit", winter="bare", spring="seedling", summer="fruit", autumn="harvested"),
    olive=dict(general="tree", winter="tree", spring="tree", summer="tree", autumn="tree"))


def pla_crop_state(crop, season=None, month=None):
    """the drawn state of a crop in a season: tree / bare / seedling / growing / ripe / fruit / harvested"""
    return PLA_CROP_STATE[crop][_pla_s(season, month) or "general"]


def _pla_crop_cols(beyond=False):
    """the crop leaf colours (one set for cotton, maize, tomato; pending research like all plant colours)"""
    c = _pla_c(PLA_CROP_LEAF)
    c["shade"] = _sec_mix(c["fill"], c["edge"], 0.25)
    if beyond:
        c = dict((k_, _sec_mix(v, SEC["paper"], 0.55) if v else v) for k_, v in c.items())
    return c


def _pla_crop_size(crop, h_m, crown_m):
    if crop == "olive":                         # orchard trees kept to their in-row spacing (rule); h by the olive ratio
        w = crown_m or PLA_CROPS["olive"]["plant_m"]
        return pla_height_ok("olive", h_m or w / PLA_FORM_RATIO["gnarled"]), w   # G6: never below the sourced 8 m
    if h_m is None or crown_m is None:
        raise ValueError("plants: %s plant size is not sourced: pass h_m and crown_m" % crop)
    return h_m, crown_m


def _pla_crop_sec(crop, x, gy, h, w, k, i, beyond, state="growing", season=None):
    """One crop plant in section, in its season's state (bare: nothing; harvested: stubble; seedling: young)."""
    if crop == "olive":
        c = pla_colours("olive", season, beyond=beyond)
        return _pla_sec("gnarled", x, gy, h, w, k, c, i)
    c = _pla_crop_cols(beyond)
    if state == "bare":
        return []
    if state == "harvested":                    # stubble: short cut stems (rule 12 % of the height)
        return [("line", [(x + d * w * k * 0.3, gy), (x + d * w * k * 0.32, gy + 0.12 * h * k)], PLA_ROW, 0.1)
                for d in (-0.5, 0.0, 0.5)]
    if state == "seedling":                     # young plant (drawing rule: 30 % height, 40 % width)
        h, w = 0.30 * h, 0.40 * w
    H, R = h * k, w / 2.0 * k
    if crop == "maize":                         # stalk, arching leaves in two tones, tassel when grown
        sh = [("line", [(x, gy), (x, gy + H)], c["shade"], 0.2)]
        for j in range(1, 7):
            py, s_ = gy + H * (0.15 + 0.11 * j), (1 if j % 2 else -1)
            sh.append(("line", [(x, py), (x + s_ * R * 0.6, py + 0.08 * H), (x + s_ * R, py - 0.02 * H)],
                       c["fill"] if j % 2 else c["shade"], 0.14))
        if state != "seedling":
            sh.append(("line", [(x, gy + 0.92 * H), (x, gy + H)], PLA_REED_HEAD, 0.35))
        return sh
    if crop == "cotton":                        # small branched bush (two masses), open bolls when ripe
        sh = [("line", [(x, gy), (x, gy + 0.5 * H)], c["stem"], 0.12)]
        sh += _pla_mass(x - 0.35 * R, gy + 0.55 * H, 0.6 * R, 0.4 * H, 0.3 * H, c, i, 0.15)
        sh += _pla_mass(x + 0.35 * R, gy + 0.6 * H, 0.6 * R, 0.38 * H, 0.3 * H, c, i + 5, 0.15)
        if state == "ripe":
            for d, e_ in ((-0.5, 0.6), (0.1, 0.85), (0.55, 0.55)):
                sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.1 * R + 0.1, 0.1 * R + 0.1, 8), PLA_BOLL,
                           c["edge"], 0.05))
        return sh
    if crop == "tomato":                        # low sprawling plant (two masses), fruit in summer
        sh = _pla_mass(x - 0.3 * R, gy + 0.3 * H, 0.7 * R, 0.6 * H, 0.3 * H, c, i, 0.15)
        sh += _pla_mass(x + 0.35 * R, gy + 0.28 * H, 0.65 * R, 0.55 * H, 0.28 * H, c, i + 5, 0.15)
        if state == "fruit":
            for d, e_ in ((-0.45, 0.35), (0.2, 0.5), (0.6, 0.3)):
                sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.08 * R + 0.1, 0.08 * R + 0.1, 8), PLA_FRUIT,
                           None, 0.0))
        return sh
    raise ValueError("plants: unknown crop %r" % crop)


def pla_crop_rows(crop, x0, x1, gy, k, spacing=None, h_m=None, crown_m=None, beyond=False, season=None, month=None):
    """Crop plants along a cut from x0 to x1 (page mm), spacing m apart (the row spacing for a cut across the rows;
    sourced default only for olive), centred in the stretch; gy a number or a function of x. season (month= alias):
    the crop's state that season (pla_crop_state; winter = bare ground: no plants)."""
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    sp = spacing or PLA_CROPS[crop]["row_m"]
    if sp is None:
        raise ValueError("plants: %s row spacing is not sourced: pass spacing (m)" % crop)
    s_ = _pla_s(season, month)
    state = pla_crop_state(crop, s_)
    _pla_count("crop_" + crop, s_)
    h, w = _pla_crop_size(crop, h_m, crown_m)
    n = int((x1 - x0) / (sp * k) + 1e-9)
    off = ((x1 - x0) - n * sp * k) / 2.0
    sh = []
    for i in range(n + 1):
        x = x0 + off + i * sp * k
        sh += _pla_crop_sec(crop, x, gy(x) if callable(gy) else gy, h, w, k, i, beyond, state, s_)
    return sh


def _pla_ring(rr):
    """A ring from a ring or an (x0, y0, x1, y1) rectangle (page mm)."""
    if len(rr) == 4 and not isinstance(rr[0], (tuple, list)):
        x0, y0, x1, y1 = rr
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return list(rr)


def pla_crop_plan(crop, ring_or_rect, k, row_spacing=None, plant_spacing=None, ang_deg=0.0, crown_m=None,
                  field=True, season=None, month=None):
    """A field or orchard block in plan: rows at row_spacing (m) at ang_deg; with plant_spacing, single plants along
    each row (true crown with crown_m or for olive, else a fixed 0.25 mm dot). Sourced defaults only for olive.
    season (month= alias): bare / harvested fields show their furrows only, young crops small dots."""
    import math as _m
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    ring = _pla_ring(ring_or_rect)
    rs = row_spacing or PLA_CROPS[crop]["row_m"]
    ps = plant_spacing or PLA_CROPS[crop]["plant_m"]
    if rs is None:
        raise ValueError("plants: %s row spacing is not sourced: pass row_spacing (m)" % crop)
    s_ = _pla_s(season, month)
    state = pla_crop_state(crop, s_)
    _pla_count("crop_" + crop, s_)
    cc = _pla_crop_cols()
    sh = [("poly", ring, PLA_FIELD, None, 0.1)] if field else []
    w = crown_m or (PLA_CROPS["olive"]["plant_m"] if crop == "olive" else None)   # olive: crown = in-row spacing
    oc = pla_colours("olive", s_) if crop == "olive" else None
    for i, (p, q) in enumerate(sec_hatch(ring, rs * k, ang_deg)):
        if ps is None or state in ("bare", "harvested"):
            sh.append(("line", [p, q], PLA_ROW, 0.08 if state in ("bare", "harvested") else 0.15))
            continue
        L = _m.hypot(q[0] - p[0], q[1] - p[1])
        if L < 1e-6:
            continue
        ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L
        n = int(L / (ps * k) + 1e-9)
        s0 = (L - n * ps * k) / 2.0
        for j in range(n + 1):
            px, py = p[0] + ux * (s0 + j * ps * k), p[1] + uy * (s0 + j * ps * k)
            if crop == "olive":
                sh += _pla_plan("gnarled", px, py, w, k, oc, i * 31 + j)
            elif w and state != "seedling":
                r = w / 2.0 * k
                sh += _pla_mass(px, py, r, r, r, cc, i * 31 + j, 0.12, edge=False)
            else:
                sh.append(("poly", sec_ellipse(px, py, 0.125, 0.125, 8), cc["fill"], None, 0.0))
    return sh


def _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y):
    """A lined, off-line cell in section: walls with a raised kerb, liner closing floor and walls (RESULT §A D2:
    liner on floor and walls, kerb above the rim: our inference there), optional gravel media and water.
    Returns (shapes, planting y)."""
    if kerb_h_m is None:
        raise ValueError("plants: kerb_h_m is required (kerb height not sourced)")
    t, top = kerb_t_m * k, rim_y + kerb_h_m * k
    sh = []
    for a, b in ((x0 - t, x0), (x1, x1 + t)):
        sh += sct_hatch_fill([(a, bed_y), (a, top), (b, top), (b, bed_y)], "concrete", k, SCT["cut"], 0.25)
    sh += sct_hatch_fill([(x0 - t, bed_y - t), (x1 + t, bed_y - t), (x1 + t, bed_y), (x0 - t, bed_y)], "concrete", k,
                         SCT["cut"], 0.25)
    g = bed_y
    if media_m:
        g = bed_y + media_m * k
        sh += sct_hatch_fill([(x0, bed_y), (x1, bed_y), (x1, g), (x0, g)], "gravel", k)
    if wl_y is not None and wl_y > g:
        sh += sec_water([(x0, g), (x1, g), (x1, wl_y), (x0, wl_y)])
    return sh, g


def _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m):
    top = rim_y + kerb_h_m * k
    return [("line", [(x0, top), (x0, bed_y), (x1, bed_y), (x1, top)], SEC["ink"], 0.4)]


def pla_reed_basin(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, step_m=None,
                   season=None, month=None):
    """Common reed in a lined, root-contained, off-line basin (D2 a) in section: inside x0-x1, floor bed_y, rim rim_y
    (page mm). kerb_t_m 0.15 m and floor slab = drawing rule; stems step_m apart in two tones; plumes only in the
    season's state (Jul-Nov S2, cut before Nov S11; general: with plumes)."""
    sp = PLA_SPECIES["reed"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h = h_m or sp["h_m"]
    st = (step_m or 1.0 / 3.0) * k              # 9 seedlings/m² (Korkusuz et al. 2004, S20) = 1/3 m apart
    s_ = _pla_s(season, month)
    _pla_count("reed", s_)
    c = pla_colours("reed", s_)
    i, x = 0, x0 + st / 2.0
    while x < x1:
        hh = h * k * (0.8 + 0.2 * _pla_rnd(i, 5))
        lean = 0.04 * hh * (1 if i % 2 else -1)
        sh.append(("line", [(x, g), (x + lean, g + hh)], c["fill"] if i % 3 else c["shade"], 0.12))
        if i % 3 == 0 and c["accent"]:          # plume
            ry = 0.2 * k + 0.2
            sh.append(("poly", sec_ellipse(x + lean, g + hh - ry, 0.06 * k + 0.1, ry, 10), c["accent"], None, 0.0))
        x += st
        i += 1
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_mint_cell(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, crown_m=None,
                  season=None, month=None):
    """Water mint only in a lined basin cell (D6) in section, same build as pla_reed_basin; mounds side by side in
    the season's colours."""
    sp = PLA_SPECIES["mint"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h, w = h_m or sp["h_m"], crown_m or sp["crown_m"]
    s_ = _pla_s(season, month)
    _pla_count("mint", s_)
    c = pla_colours("mint", s_)
    n = max(1, int((x1 - x0) / (w * k)))
    for i in range(n):
        sh += _pla_sec("mound", x0 + (i + 0.5) * (x1 - x0) / n, g, h, min(w, (x1 - x0) / n / k), k, c, i)
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_cell_plan(kind, ring_or_rect, k, kerb_t_m=0.15, season=None, month=None):
    """A lined cell in plan, kind 'reed' or 'mint': wet ground, the kerb as a band kerb_t_m wide, the plants in the
    season's colours."""
    if kind not in ("reed", "mint"):
        raise ValueError("pla_cell_plan: kind is 'reed' or 'mint'")
    ring = _pla_ring(ring_or_rect)
    sp = PLA_SPECIES[kind]
    s_ = _pla_s(season, month)
    _pla_count(kind, s_)
    c = pla_colours(kind, s_)
    sh = [("poly", ring, PLA_WET, None, 0.1)]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    if kind == "reed":                          # stems on the 1/3 m grid, never denser than 0.9 mm on the page
        d = max(0.9, k / 3.0)
        for i in range(int((max(xs) - min(xs)) / d) + 1):
            for j in range(int((max(ys) - min(ys)) / d) + 1):
                px = min(xs) + (i + 0.5 * (j % 2) + 0.25) * d
                py = min(ys) + (j + 0.5) * d
                if _sct_inside(ring, (px, py)):
                    sh.append(("line", [(px - 0.2 * d, py - 0.25 * d), (px + 0.2 * d, py + 0.25 * d)],
                               c["fill"] if (i + j) % 3 else c["shade"], 0.1))
    else:
        w = sp["crown_m"] * k
        for i in range(int((max(xs) - min(xs)) / w) + 1):
            for j in range(int((max(ys) - min(ys)) / w) + 1):
                px, py = min(xs) + (i + 0.5) * w, min(ys) + (j + 0.5) * w
                if _sct_inside(ring, (px, py)):
                    sh += _pla_plan("mound", px, py, sp["crown_m"] * 0.9, k, c, i * 7 + j)
    sh.append(("poly", ring, None, SCT["line"], max(0.15, kerb_t_m * k)))
    return sh


# ---- purpose tags (G9, M6; H-B 30 Oct 2026): what each plant group does. From the species roles of the water board
# (SPECIES.py role: shade, hold the bank, clean, scent, flower, harvest) mapped onto M6's six words, plus plain
# riparian ecology (marked "?" in PLA_PURPOSE_UNSURE: not from a project source; check before printing as a claim).
PLA_TAGS = ("wind", "noise", "shade", "corridor", "cleaning", "perception")
PLA_PURPOSE = {
    "plane": ("shade", "corridor"),
    "ash": ("shade", "corridor"),
    "willow": ("shade", "cleaning", "corridor"),
    "olive": ("shade", "perception"),
    "stone_pine": ("shade", "wind", "perception"),
    "tamarisk": ("shade", "wind", "corridor"),
    "chaste": ("perception", "corridor"),
    "rosemary": ("perception",),
    "lavender": ("perception",),
    "loosestrife": ("cleaning", "perception", "corridor"),
    "soft_rush": ("cleaning", "corridor"),
    "rush": ("cleaning", "corridor"),
    "reed": ("cleaning", "noise", "corridor"),
    "mint": ("cleaning", "perception"),
}
PLA_PURPOSE_UNSURE = {   # tags assigned from general ecology, not from a project source
    "plane": ("corridor",), "ash": ("corridor",), "willow": ("corridor",), "olive": ("perception",),
    "stone_pine": ("shade", "wind", "perception"), "tamarisk": ("wind", "corridor"), "chaste": ("corridor",),
    "loosestrife": ("corridor",), "soft_rush": ("corridor",), "rush": ("cleaning", "corridor"),
    "reed": ("noise", "corridor"),
}


def pla_purpose(key, sure_only=False):
    """the purpose tags of a species (PLA_TAGS words); sure_only drops the ones from general ecology"""
    t = PLA_PURPOSE.get(key, ())
    return tuple(x for x in t if not (sure_only and x in PLA_PURPOSE_UNSURE.get(key, ())))


# ---- ecological bands (G9): t = 0 at the water's edge (wet, low) to 1 on the dry upper ground (high). Each species
# grows around its niche centre (t, half width, weight): drawing rules from the species' habitat words in
# species.json (emergent / bank / dry slope), not measured distances. Reed and water mint: lined cells only (D2, D6).
PLA_NICHE = {
    "soft_rush": (0.04, 0.12, 1.0), "loosestrife": (0.10, 0.14, 0.9), "rush": (0.14, 0.12, 0.6),
    "willow": (0.24, 0.17, 0.8), "tamarisk": (0.36, 0.22, 0.7), "ash": (0.46, 0.20, 0.6), "plane": (0.52, 0.20, 0.5),
    "chaste": (0.55, 0.24, 0.8), "olive": (0.80, 0.20, 0.6), "rosemary": (0.86, 0.17, 0.8), "lavender": (0.90, 0.15, 0.8),
    "stone_pine": (0.92, 0.12, 0.3),
}


def _pla_canopy(key):
    return PLA_SPECIES[key]["layer"] == "tree"


def _pla_pick(t, rnd, keys, mix, canopy):
    """a species for band position t (weighted by niche), or None for an open gap"""
    import math as _m
    ws = []
    for k_ in keys:
        if _pla_canopy(k_) != canopy:
            continue
        tc, hw, w0 = PLA_NICHE[k_]
        w = (mix.get(k_, w0) if isinstance(mix, dict) else w0) * _m.exp(-((t - tc) / hw) ** 2)
        if w > 0.02:
            ws.append((k_, w))
    tot = sum(w for _k, w in ws)
    if tot < 0.12:                                 # nothing at home here: leave the ground open
        return None
    r = rnd() * tot
    for k_, w in ws:
        r -= w
        if r <= 0:
            return k_
    return ws[-1][0]


def _pla_size_var(key, rnd):
    """(h, crown) of one plant: the drawing size x 0.88-1.08, kept inside the sourced height range"""
    sp = PLA_SPECIES[key]
    f = 0.88 + 0.20 * rnd()
    return pla_height_ok(key, sp["h_m"] * f), sp["crown_m"] * f


def _pla_keys(mix):
    # round 4 (D1, PLAN §4.9): mix=None no longer draws the willow; it is planted only where a mix names it
    keys = list(mix) if mix else [k_ for k_ in PLA_NICHE if k_ != "willow"]
    bad = [k_ for k_ in keys if k_ not in PLA_NICHE]
    if bad:
        raise ValueError("plants scatter: %s not free-planted (cells only, removed or unknown)" % ", ".join(bad))
    return keys


def pla_scatter_section(x0, x1, gy, k, t0=0.0, t1=1.0, mix=None, seed=0, layer=0, style="b", density=1.0,
                        hires=True, avoid=None, detail=True, month=None, season=None, water=None):
    """a mixed, naturalistic planting along a cut from x0 to x1 (page mm), ground gy (number or function of x): the
    band position runs from t0 at x0 to t1 at x1 (0 = water's edge, 1 = dry upper ground; or pass t0 as a function
    of x). Canopy trees and the low layer are spaced independently (crowns overlap, shrubs stand under tree edges),
    each gap random and never equal to the one before (no rows, no repeated clusters). mix: species keys (list) or
    {key: weight}. avoid: [(xa, xb)] page mm where nothing is planted (paths, water, steps). water: page y (or a
    function of x) of the water: where the ground lies under it only emergent species grow. season (month= alias):
    pla_section. Returns (shapes,
    placed [(key, x, h_m, crown_m)]), drawn tall first so the low layer reads in front."""
    keys = _pla_keys(mix)
    rnd = _pla_rng(seed * 7 + 3)
    sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
    K = k * sc

    def tt(x):
        if callable(t0):
            return t0(x)
        return t0 + (t1 - t0) * (x - x0) / float(max(1e-9, x1 - x0))

    def blocked(x, key):
        if any(a <= x <= b for a, b in (avoid or ())):
            return True
        if water is None or PLA_SPECIES[key]["layer"] == "emergent":
            return False
        g_ = gy(x) if callable(gy) else gy
        return g_ < (water(x) if callable(water) else water)
    placed = []
    for canopy in (True, False):
        x, last_gap = x0 + rnd() * 1.5 * K, None
        while x < x1:
            key = _pla_pick(tt(x), rnd, keys, mix, canopy)
            if key is None or blocked(x, key):
                x += (0.8 + rnd()) * K
                continue
            h, w = _pla_size_var(key, rnd)
            placed.append((key, x, h, w))
            f = 0.85 if canopy else 0.75
            gap = f * w * (0.7 + 1.1 * rnd()) / max(0.2, density) * K
            if last_gap is not None and abs(gap - last_gap) < 0.15 * gap:     # never an even rhythm
                gap *= 1.35 if rnd() > 0.5 else 0.72
            last_gap = gap
            x += max(0.3 * K, gap)
    placed.sort(key=lambda p_: -p_[2])
    sh = []
    for i, (key, x, h, w) in enumerate(placed):
        sh += pla_section(key, x, gy, k, h_m=h, crown_m=w, seed=seed + i, hires=hires, style=style, layer=layer,
                          detail=detail, month=month, season=season)
    return sh, placed


# ---- round 4 (S3, D7, G-R4-5.2): the low layer of shrubs and flowers. Only the sourced species already in the
# booklet (D7): chaste tree, rosemary, French lavender, purple loosestrife, soft rush, placed by wetness band
# (PLA_NICHE: loosestrife and soft rush at the water, chaste tree on the moist ground, rosemary and lavender on the
# dry tops). Every section gets one (BRIEF G-R4-5.2), and every undefined planted area in plan (pla_low_plan).
PLA_LOW = ("chaste", "rosemary", "lavender", "loosestrife", "soft_rush")


def pla_low_section(x0, x1, gy, k, t0=0.0, t1=1.0, seed=0, layer=0, density=1.2, avoid=None, water=None,
                    season=None, month=None, mix=None, detail=True):
    """the shrub and flower layer along a cut x0..x1 (page mm), band t0 -> t1 (0 = water's edge, 1 = dry top; or t0
    a function of x), mixed by wetness, never in rows (pla_scatter_section with the PLA_LOW species or `mix`, a
    subset); water / avoid as there. Returns (shapes, placed [(key, x, h_m, crown_m)])."""
    return pla_scatter_section(x0, x1, gy, k, t0, t1, mix=mix or PLA_LOW, seed=seed, layer=layer, density=density,
                               avoid=avoid, detail=detail, month=month, season=season, water=water)


def pla_low_plan(ring, k, gradient, seed=0, density=1.2, avoid=None, season=None, month=None, mix=None, max_n=3000):
    """the shrub and flower layer in an undefined planted area in plan (ring page mm; gradient as pla_scatter_plan),
    the PLA_LOW species (or `mix`, a subset) by wetness. Returns (shapes, placed [(key, x, y, crown_m)])."""
    return pla_scatter_plan(ring, k, gradient, mix=mix or PLA_LOW, seed=seed, density=density, avoid=avoid,
                            max_n=max_n, month=month, season=season)


# ---- G9 mixed groups in section (R2-A 31 Oct 2026) -------------------------------------------------------------------
# Drawing rules (not data): a group is 5-16 m wide with 2-12 m open gaps between groups (both / density), canopy
# trees step 35-75 % of a crown apart (crowns overlap), each plant's height = its drawing size x 0.70-1.10 kept
# inside the sourced range (pla_height_ok); the low layer stands under and around the tree edges.
PLA_GROUP = dict(group_m=(5.0, 16.0), gap_m=(2.0, 12.0), step=(0.35, 0.75), size=(0.70, 1.10))


def _pla_group_size(key, rnd):
    sp = PLA_SPECIES[key]
    lo, hi = PLA_GROUP["size"]
    f = lo + (hi - lo) * rnd()
    return pla_height_ok(key, sp["h_m"] * f), sp["crown_m"] * f


def _pla_other(t, rnd, keys, mix, canopy, not_key):
    """a species other than not_key for band position t (None if nothing else grows here)"""
    for _i in range(8):
        k_ = _pla_pick(t, rnd, keys, mix, canopy)
        if k_ is not None and k_ != not_key:
            return k_
    return None


def pla_group_section(x0, x1, gy, k, t0=0.0, t1=1.0, mix=None, seed=0, layers=(2, 1, 0), style="a", density=1.0,
                      avoid=None, hires=True, detail=True, ground=None, water=None, month=None, season=None):
    """G9 planting in section: mixed groups, never rows. Along x0..x1 (page mm), band t0 -> t1 (0 = water's edge,
    1 = dry upper ground; or t0 = a function of x), each depth layer of `layers` (D9, back first: 2, 1, 0) gets
    groups at irregular places; in a group the canopy trees overlap their crowns and the low layer (shrubs,
    emergent, ground) stands under and around them; species interpenetrate by band (wet to dry, low to high: the
    niche weights of PLA_NICHE) and a group always holds two or more species and three or more plants (never one
    species standing alone, never an identical cluster: sizes and gaps vary). Each plant: a varied height inside its
    sourced range, a cutout variant picked by its seed (style a), mirrored on odd seeds, seated on the lowest ground
    under its base (G14 sf_seat_x). ground = {layer: gy} gives a depth layer its own ground (else gy); water = page
    y or function of x: where the ground lies under the water only emergent species grow; avoid = [(xa, xb)] page
    mm kept free (paths, steps, lanes). Returns (shapes back to front, placed [(key, x, h_m, crown_m, layer)],
    groups [(layer, xa, xb, [keys], purpose tags)]): use groups to say what each group does (G9) and placed for
    sf_assert_g6."""
    keys = _pla_keys(mix)
    rnd = _pla_rng(seed * 11 + 5)
    seat = globals().get("sf_seat_x")
    gfn = globals().get("_sf_fn")

    def tt(x):
        if callable(t0):
            return t0(x)
        return t0 + (t1 - t0) * (x - x0) / float(max(1e-9, x1 - x0))

    def blocked(x):
        return any(a <= x <= b for a, b in (avoid or ()))
    sh, placed, groups, n = [], [], [], 0
    for layer in layers:
        g_ = (ground or {}).get(layer, gy)
        g_ = gfn(g_) if gfn else g_
        sc = globals()["fig_depth"](layer)[0] if layer and globals().get("fig_depth") else 1.0
        K = k * sc

        def wet(x):
            if water is None:
                return False
            w_ = water(x) if callable(water) else water
            return (g_(x) if callable(g_) else g_) < w_

        def ok(key, x):
            return not blocked(x) and (not wet(x) or PLA_SPECIES[key]["layer"] == "emergent")
        x = x0 + rnd() * PLA_GROUP["gap_m"][1] * 0.5 * K
        while x < x1:
            gw = (PLA_GROUP["group_m"][0] + (PLA_GROUP["group_m"][1] - PLA_GROUP["group_m"][0]) * rnd()) * K
            xa, xb = x, min(x1, x + gw)
            mem = []
            xx = xa + 0.1 * rnd() * gw                     # canopy: overlapping crowns
            while xx < xb:
                key = _pla_pick(tt(xx), rnd, keys, mix, True)
                if key is not None and mem and all(m[0] == key for m in mem) and rnd() < 0.6:
                    key = _pla_other(tt(xx), rnd, keys, mix, True, key) or key
                if key is None or not ok(key, xx):
                    xx += (0.6 + rnd()) * K
                    continue
                h, w = _pla_group_size(key, rnd)
                mem.append((key, xx, h, w, True))
                xx += (PLA_GROUP["step"][0] + (PLA_GROUP["step"][1] - PLA_GROUP["step"][0]) * rnd()) * w * K
            nl = 2 + int(rnd() * 4.999)                     # low layer: 2-6, under and around the crowns
            for _i in range(nl):
                xl = xa - 0.1 * gw + 1.2 * gw * rnd()
                if xl < x0 or xl > x1:
                    continue
                key = _pla_pick(tt(xl), rnd, keys, mix, False)
                if key is None or not ok(key, xl):
                    continue
                h, w = _pla_group_size(key, rnd)
                mem.append((key, xl, h, w, False))
            sp = set(m[0] for m in mem)
            if len(sp) == 1 and mem:                       # one species alone: add another that grows here
                for _i in range(3):
                    xl = xa + gw * rnd()
                    for canopy in (False, True):
                        key = _pla_other(tt(xl), rnd, keys, mix, canopy, mem[0][0])
                        if key is not None and ok(key, xl) and xl <= x1:
                            h, w = _pla_group_size(key, rnd)
                            mem.append((key, xl, h, w, canopy))
                            break
                    if len(set(m[0] for m in mem)) > 1:
                        break
            if len(mem) >= 3 and len(set(m[0] for m in mem)) >= 2:
                mem.sort(key=lambda m: -m[2])              # tall first: the low layer reads in front
                ks = sorted(set(m[0] for m in mem))
                tags = sorted(set(t_ for k_ in ks for t_ in pla_purpose(k_, sure_only=True)))
                groups.append((layer, xa, xb, ks, tags))
                for key, xp, h, w, canopy in mem:
                    half = (0.12 if canopy else 0.35) * w * K
                    gyp = seat(g_, xp, half) if seat else (g_(xp) if callable(g_) else g_)
                    sh += pla_section(key, xp, gyp, k, h_m=h, crown_m=w, seed=seed * 1000 + n, hires=hires,
                                      style=style, layer=layer, detail=detail, month=month, season=season)
                    placed.append((key, xp, h, w, layer))
                    n += 1
            x = xb + (PLA_GROUP["gap_m"][0] + (PLA_GROUP["gap_m"][1] - PLA_GROUP["gap_m"][0]) * rnd()) / \
                max(0.2, density) * K
    if not groups:
        msg = u"Plants: no mixed group fits %s (a group needs two or more species growing in its band)" % (
            u", ".join(keys))
        if msg not in PLA_LOG:
            PLA_LOG.append(msg)
    return sh, placed, groups


def _pla_rng(seed):
    s = [int(seed * 2654435761 + 97) & 0x7fffffff]

    def r():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7fffffff
        return s[0] / float(0x7fffffff)
    return r


def _pla_seg_d(p, a, b):
    import math as _m
    dx, dy = b[0] - a[0], b[1] - a[1]
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 < 1e-12 else max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / L2))
    return _m.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)


def _pla_grad_fn(gradient, k):
    """t(x, y) from a function, or from {"wet": polyline page mm, "width_m": band width}: distance to the wet line
    over the band width, 0..1"""
    if callable(gradient):
        return gradient
    wet, wd = gradient["wet"], float(gradient["width_m"]) * k

    def f(x, y):
        d = min(_pla_seg_d((x, y), a, b) for a, b in zip(wet[:-1], wet[1:]))
        return max(0.0, min(1.0, d / wd))
    return f


def _pla_rowlike(c, pts, d_lim):
    """True when c continues a straight, evenly spaced line of two neighbours (a row in the making)"""
    import math as _m
    near = sorted((q for q in pts if _m.hypot(q[0] - c[0], q[1] - c[1]) < d_lim),
                  key=lambda q: (q[0] - c[0]) ** 2 + (q[1] - c[1]) ** 2)[:8]     # the 8 nearest are enough
    for b in near:
        dbc = _m.hypot(c[0] - b[0], c[1] - b[1])
        for a in near:
            if a is b:
                continue
            dab = _m.hypot(b[0] - a[0], b[1] - a[1])
            if dab < 1e-9 or abs(dab - dbc) > 0.2 * dbc:
                continue
            u = ((b[0] - a[0]) / dab, (b[1] - a[1]) / dab)
            v = ((c[0] - b[0]) / dbc, (c[1] - b[1]) / dbc)
            if u[0] * v[0] + u[1] * v[1] > 0.985:        # within about 10 degrees of straight on
                return True
    return False


def pla_scatter_plan(ring, k, gradient, mix=None, seed=0, density=1.0, avoid=None, max_n=3000, month=None,
                     season=None):
    """a mixed planting in plan inside ring (page mm): Poisson-disc style dart throwing, canopy trees first then the
    low layer, each species picked by its niche at t = gradient(x, y) (a function, or {"wet": polyline, "width_m":
    m}); same-layer plants keep 0.8 x (r1 + r2) apart, shrubs may stand under tree edges (0.3 x), candidates that
    would extend a straight evenly spaced line are thrown away: no rows, grids, axes or repeated clusters. avoid:
    rings (page mm) left empty. month: seasonal colours / bare (pla_plan). Returns (shapes, placed [(key, x, y,
    crown_m)]); canopy crowns drawn opaque over the low layer (round 3 D7: no alpha anywhere)."""
    import math as _m
    keys = _pla_keys(mix)
    rnd = _pla_rng(seed * 11 + 5)
    tf = _pla_grad_fn(gradient, k)
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    bx0, by0, bw, bh = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    area = abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(ring, ring[1:] + ring[:1]))) / 2.0
    placed = {True: [], False: []}
    grids = {True: {}, False: {}}
    rmax = {c_: max([PLA_SPECIES[k_]["crown_m"] * 1.08 / 2.0 * k for k_ in keys if _pla_canopy(k_) == c_] or [0.5 * k])
            for c_ in (True, False)}

    def cell(c_, x, y):
        s_ = 2.0 * rmax[c_]
        return int(_m.floor(x / s_)), int(_m.floor(y / s_))

    def near(c_, x, y, dist):
        s_ = 2.0 * rmax[c_]
        n = int(_m.ceil(dist / s_))
        i0, j0 = cell(c_, x, y)
        out = []
        for i in range(i0 - n, i0 + n + 1):
            for j in range(j0 - n, j0 + n + 1):
                out += grids[c_].get((i, j), ())
        return out
    total = 0
    for canopy in (True, False):
        r_typ = (sum(PLA_SPECIES[k_]["crown_m"] for k_ in keys if _pla_canopy(k_) == canopy) /
                 max(1, sum(1 for k_ in keys if _pla_canopy(k_) == canopy))) / 2.0 * k
        if r_typ <= 0:
            continue
        tries = int(min(30000, 6.0 * density * area / (_m.pi * r_typ * r_typ) + 50))
        for _i in range(tries):
            if total >= max_n:
                break
            x, y = bx0 + rnd() * bw, by0 + rnd() * bh
            if not _sct_inside(ring, (x, y)) or any(_sct_inside(a, (x, y)) for a in (avoid or ())):
                continue
            key = _pla_pick(tf(x, y), rnd, keys, mix, canopy)
            if key is None:
                continue
            h, w = _pla_size_var(key, rnd)
            r = w / 2.0 * k
            ok = True
            for (qx, qy, qr, _qk) in near(canopy, x, y, 0.8 * (r + rmax[canopy])):
                if _m.hypot(qx - x, qy - y) < 0.8 * (r + qr) / max(0.3, density) ** 0.5:
                    ok = False
                    break
            if ok and not canopy:
                for (qx, qy, qr, _qk) in near(True, x, y, 0.3 * (r + rmax[True])):
                    if _m.hypot(qx - x, qy - y) < 0.3 * (r + qr):
                        ok = False
                        break
            if ok and canopy:
                for (qx, qy, qr, _qk) in near(False, x, y, 0.3 * (r + rmax[False])):
                    if _m.hypot(qx - x, qy - y) < 0.3 * (r + qr):
                        ok = False
                        break
            if ok and _pla_rowlike((x, y), [(q[0], q[1]) for q in near(canopy, x, y, 3.0 * (r + rmax[canopy]))],
                                   3.0 * (r + rmax[canopy])):
                ok = False
            if not ok:
                continue
            e = (x, y, r, key)
            placed[canopy].append(e)
            grids[canopy].setdefault(cell(canopy, x, y), []).append(e)
            total += 1
    sh, out = [], []
    for canopy in (False, True):
        for i, (x, y, r, key) in enumerate(placed[canopy]):
            sh += pla_plan(key, x, y, k, crown_m=2.0 * r / k, seed=seed + i * 3 + (7 if canopy else 0), month=month,
                           season=season)
            out.append((key, x, y, 2.0 * r / k))
    return sh, out


# ---- field / orchard tile (D7 a, D2 a): one texture + one representative symbol in the middle of the area ----------
def _pla_inner_point(ring):
    """a point well inside the ring: the grid point farthest from the edge (12 x 12 search)"""
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    best, bd = None, -1.0
    for i in range(1, 12):
        for j in range(1, 12):
            p = (min(xs) + (max(xs) - min(xs)) * i / 12.0, min(ys) + (max(ys) - min(ys)) * j / 12.0)
            if not _sct_inside(ring, p):
                continue
            d = min(_pla_seg_d(p, a, b) for a, b in zip(ring, ring[1:] + ring[:1]))
            if d > bd:
                best, bd = p, d
    return best or (sum(xs) / len(xs), sum(ys) / len(ys))


def pla_field_tile(ring_or_rect, k, crop="olive", symbol_mm=None, seed=0, fill=None, texture=True, season=None,
                   month=None):
    """a farm or orchard area simplified (D7 a, r3 #31): the field fill, an even scatter of short furrow marks (one
    texture, no rows) and ONE symbol of the crop in the middle, drawn at print quality in the crop's season state
    (olive: the olive plan symbol; other crops: a two-tone crop tuft, bolls / fruit when ripe, stubble when
    harvested, bare furrows in winter). symbol_mm = the symbol's width on the page (default the true olive crown 5 m
    x k, at least 6 mm: a symbol, not to scale). Returns shapes."""
    import math as _m
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    ring = _pla_ring(ring_or_rect)
    s_ = _pla_s(season, month)
    state = pla_crop_state(crop, s_)
    _pla_count("crop_" + crop, s_)
    sh = [("poly", ring, fill or PLA_FIELD, None, 0.1)]
    if texture:
        rnd = _pla_rng(seed + 17)
        xs, ys = [p[0] for p in ring], [p[1] for p in ring]
        d = 1.6                                      # page mm between marks (texture, not a size)
        nx, ny = int((max(xs) - min(xs)) / d) + 1, int((max(ys) - min(ys)) / d) + 1
        for i in range(nx):
            for j in range(ny):
                px = min(xs) + (i + 0.15 + 0.7 * rnd()) * d
                py = min(ys) + (j + 0.15 + 0.7 * rnd()) * d
                if not _sct_inside(ring, (px, py)):
                    continue
                a = _m.radians(20.0 + 40.0 * rnd())
                L = 0.35 + 0.3 * rnd()
                sh.append(("line", [(px, py), (px + L * _m.cos(a), py + L * _m.sin(a))], PLA_ROW, 0.08))
    cx, cy = _pla_inner_point(ring)
    sm = symbol_mm or max(6.0, PLA_CROPS["olive"]["plant_m"] * k)
    if crop == "olive":
        oc = pla_colours("olive", s_)
        sh += _pla_plan("gnarled", cx, cy, sm / k, k, oc, seed)
        sh += _pla_plan_mark("olive", cx, cy, sm / 2.0, oc, seed)
        return sh
    r = sm / 2.0
    if state in ("bare", "harvested"):              # furrows (and stubble ticks when harvested)
        for j in (-1, 0, 1):
            sh.append(("line", [(cx - r, cy + 0.35 * j * r), (cx + r, cy + 0.35 * j * r)], PLA_ROW, 0.25))
            if state == "harvested":
                for i in range(-3, 4):
                    px = cx + 0.28 * i * r
                    sh.append(("line", [(px, cy + 0.35 * j * r), (px + 0.05 * r, cy + 0.35 * j * r + 0.14 * r)],
                               PLA_ROW, 0.12))
        return sh
    cc = _pla_crop_cols()
    if state == "seedling":
        r *= 0.5
    for i, (dx, dy, s_m) in enumerate(((-0.35, -0.2, 0.6), (0.32, -0.15, 0.58), (0.0, 0.25, 0.6))):
        sh += _pla_mass(cx + dx * r, cy + dy * r, s_m * r, s_m * r, s_m * r, cc, seed + i, 0.12)
    acc = {"ripe": PLA_BOLL, "fruit": PLA_FRUIT}.get(state)
    if crop == "maize" and state == "growing":
        acc = PLA_REED_HEAD                          # tassels
    if acc:
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + 0.08)
            sh.append(("poly", sec_ellipse(cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a), 0.14 * r, 0.14 * r, 8),
                       acc, cc["edge"] if acc == PLA_BOLL else None, 0.05 if acc == PLA_BOLL else 0.0))
    return sh


# ---- species detail (M6 style b: "detailed from the species' photo"): leaf texture and flower marks in the crown, and
# a mark per species in plan so that no two species share a symbol. Mark sizes are page-mm conventions eased with
# the crown size; colours only from the species' own set (flower colours: only where the species row has one).
def _pla_marks_in(cx, cy, rx, ry, n, rnd):
    """n points spread inside an ellipse (jittered sunflower spiral: even, never a grid)"""
    import math as _m
    out = []
    for i in range(n):
        rr = _m.sqrt((i + 0.5) / n)
        a = i * 2.39996 + 0.6 * rnd()
        out.append((cx + rx * rr * _m.cos(a), cy + ry * rr * _m.sin(a)))
    return out


def _pla_detail(key, form, x, gy, h, w, k, c, seed):
    """leaf texture / flower marks of one species in section, over its _pla_sec silhouette"""
    import math as _m
    rnd = _pla_rng(seed * 3 + 1)
    H, R = h * k, w / 2.0 * k
    if R < 0.8:                                     # too small on the page for a texture
        return []
    lo = dict(dome=0.3, oval=0.3, weeping=0.25, gnarled=0.3, umbrella=0.65, feathery=0.55).get(form, 0.0) * H
    cx, cy = x, gy + lo + (H - lo) * (0.55 if form != "mound" else 0.45)
    rx, ry = 0.62 * R, 0.30 * (H - lo) if form != "umbrella" else 0.24 * (H - lo)   # round 4: on the masses, not gaps
    m = max(0.25, min(1.2, 0.045 * R))              # mark length, page mm
    n = int(max(6, min(70, (_m.pi * rx * ry) / (m * m * 9.0))))
    e, lt, ac = c["edge"], c["lt"], c.get("accent")
    sh = []
    pts = _pla_marks_in(cx, cy, rx, ry, n, rnd)
    for i, (px, py) in enumerate(pts):
        if key == "plane":                          # palmate leaves: three short spokes
            for a in (90.0, 30.0, 150.0):
                r_ = _m.radians(a + 20.0 * rnd())
                sh.append(("line", [(px, py), (px + m * _m.cos(r_), py + m * _m.sin(r_))], e, 0.06))
        elif key == "ash":                          # pinnate leaves: a stalk with leaflet pairs
            a = _m.radians(70.0 + 40.0 * rnd())
            ux, uy = _m.cos(a), _m.sin(a)
            sh.append(("line", [(px, py), (px + 1.4 * m * ux, py + 1.4 * m * uy)], e, 0.05))
            for t in (0.45, 0.9):
                bx_, by_ = px + t * 1.4 * m * ux, py + t * 1.4 * m * uy
                sh.append(("line", [(bx_ - 0.35 * m * uy, by_ + 0.35 * m * ux), (bx_ + 0.35 * m * uy, by_ - 0.35 * m * ux)],
                           e, 0.05))
        elif key == "willow":                       # round 3: its streamers and strands are the texture (marks
            pass                                    # spread over the envelope would float in the gaps, G14)
        elif key == "olive":                        # small lance leaves, silver above, dark below
            a = _m.radians(rnd() * 180.0)
            col = lt if i % 3 else e
            sh.append(("line", [(px, py), (px + 0.9 * m * _m.cos(a), py + 0.9 * m * _m.sin(a))], col, 0.08))
        elif key == "stone_pine":                   # needle tufts on the flat crown
            if py > cy - 0.2 * ry:
                for a in (60.0, 90.0, 120.0):
                    r_ = _m.radians(a)
                    sh.append(("line", [(px, py), (px + 0.8 * m * _m.cos(r_), py + 0.8 * m * _m.sin(r_))], lt, 0.05))
        elif key == "tamarisk":                     # scale-leaf sprays: fine stipple
            sh.append(("poly", sec_ellipse(px, py, 0.12 * m + 0.05, 0.12 * m + 0.05, 6), e, None, 0.1))
        elif key == "rosemary":                     # needle leaves
            a = _m.radians(45.0 + 90.0 * (i % 2))
            sh.append(("line", [(px, py), (px + 0.7 * m * _m.cos(a), py + 0.7 * m * _m.sin(a))], e, 0.06))
        elif key in ("lavender", "chaste", "loosestrife") and ac:
            if i % 2 == 0:                          # flowers in the species' own accent
                sh.append(("poly", sec_ellipse(px, py, 0.18 * m + 0.06, 0.28 * m + 0.08, 8), ac, None, 0.1))
        elif key == "soft_rush":                    # brown flower tufts on the side of the stems, near the top
            if py > cy and i % 3 == 0:
                sh.append(("poly", sec_ellipse(px, py, 0.25 * m + 0.08, 0.2 * m + 0.06, 8), PLA_REED_HEAD, None, 0.1))
        elif key == "rush":                         # sharp stem tips
            if py > cy and i % 2 == 0:
                sh.append(("line", [(px, py), (px, py + 0.8 * m)], e, 0.05))
        elif key == "mint":                         # small rounded leaves
            sh.append(("poly", sec_ellipse(px, py, 0.22 * m + 0.05, 0.18 * m + 0.05, 8), lt, None, 0.1))
    return sh


def _pla_plan_mark(key, cx, cy, r, c, seed):
    """the species' own mark on its plan symbol (M6: every species distinct in plan)"""
    import math as _m
    rnd = _pla_rng(seed * 5 + 2)
    e, lt, ac = c["edge"], c["lt"], c.get("accent")
    m = max(0.2, 0.18 * r)
    sh = []
    if key == "plane":                              # palmate stars
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 5, rnd):
            for a in (90.0, 18.0, 162.0, 234.0, 306.0):
                ra = _m.radians(a)
                sh.append(("line", [(px, py), (px + 0.5 * m * _m.cos(ra), py + 0.5 * m * _m.sin(ra))], e, 0.06))
    elif key == "ash":                              # pinnate marks
        for (px, py) in _pla_marks_in(cx, cy, 0.55 * r, 0.55 * r, 4, rnd):
            sh.append(("line", [(px - 0.6 * m, py), (px + 0.6 * m, py)], e, 0.06))
            for t in (-0.3, 0.1, 0.5):
                sh.append(("line", [(px + t * m, py - 0.25 * m), (px + t * m, py + 0.25 * m)], e, 0.05))
    elif key == "olive":                            # silver leaf speckle
        for (px, py) in _pla_marks_in(cx, cy, 0.75 * r, 0.75 * r, 9, rnd):
            sh.append(("poly", sec_ellipse(px, py, 0.12 * m + 0.05, 0.12 * m + 0.05, 6), lt, None, 0.1))
    elif key == "stone_pine":                       # dark ring inside the rim tufts
        sh.append(("poly", sec_ellipse(cx, cy, 0.55 * r, 0.55 * r, 30), None, e, 0.08))
    elif key == "willow":                           # narrow lance leaves, pale side up
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 8, rnd):
            a = _m.radians(rnd() * 180.0)
            sh.append(("line", [(px, py), (px + 0.7 * m * _m.cos(a), py + 0.7 * m * _m.sin(a))], lt, 0.06))
    elif key == "tamarisk":                         # stipple
        for (px, py) in _pla_marks_in(cx, cy, 0.7 * r, 0.7 * r, 14, rnd):
            sh.append(("poly", sec_ellipse(px, py, 0.06 * m + 0.04, 0.06 * m + 0.04, 6), e, None, 0.1))
    elif key == "rosemary":                         # needle crosses
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 6, rnd):
            sh += [("line", [(px - 0.3 * m, py - 0.3 * m), (px + 0.3 * m, py + 0.3 * m)], e, 0.05),
                   ("line", [(px - 0.3 * m, py + 0.3 * m), (px + 0.3 * m, py - 0.3 * m)], e, 0.05)]
    elif key == "soft_rush":                        # an open centre and brown tufts on a ring
        sh.append(("poly", sec_ellipse(cx, cy, 0.25 * r, 0.25 * r, 14), SEC["paper"], None, 0.1))
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + 0.1)
            sh.append(("poly", sec_ellipse(cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a), 0.1 * r + 0.05,
                                           0.1 * r + 0.05, 6), PLA_REED_HEAD, None, 0.1))
    elif key == "rush":                             # spiny tips across the ray ends
        for i in range(8):
            a = 2 * _m.pi * (i / 8.0)
            px, py = cx + 0.9 * r * _m.cos(a), cy + 0.9 * r * _m.sin(a)
            sh.append(("line", [(px - 0.2 * m * _m.sin(a), py + 0.2 * m * _m.cos(a)),
                                (px + 0.2 * m * _m.sin(a), py - 0.2 * m * _m.cos(a))], e, 0.05))
    elif key == "mint":                             # small round leaves
        for (px, py) in _pla_marks_in(cx, cy, 0.6 * r, 0.6 * r, 5, rnd):
            sh.append(("poly", sec_ellipse(px, py, 0.14 * r, 0.14 * r, 8), None, e, 0.05))
    # chaste, lavender, loosestrife: their accent flowers (in _pla_plan) already set them apart
    return sh
