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


def _pla_c(fill, accent=None, stem=None):
    """The colour set of one species: fill, edge, lighter lobes, stem, accent (same in both views)."""
    return dict(fill=fill, edge=SEC["ink2"], lt=_sec_mix(fill, SEC["paper"], 0.35), stem=stem or SEC["trunk"],
                accent=accent)


# one entry per species (species.json species_data + giant reed from the screening); h_range = sourced (lo, hi) m
PLA_SPECIES = {
    "plane": dict(name="Oriental plane", turkish="Doğu çınarı", latin="Platanus orientalis", layer="tree",
                  form="dome", foliage="deciduous (S26)", status="keep",
                  h_range=(None, 30.0), h_m=15.0,            # "up to 30 m" S68, S69
                  crown_m=15.0,                              # "wider than 8 metres" S70: form rule 1.0 x h (>= 8)
                  bloom=[4, 5], leaf=PLA_LEAF_SITE,          # Apr-May S69 (secondary)
                  colours=_pla_c(SEC["crown"])),             # section_style SEC crown
    "ash": dict(name="Narrow-leaved ash", turkish="Dişbudak", latin="Fraxinus angustifolia", layer="tree",
                form="oval", foliage="deciduous (S7)", status="keep",
                h_range=(None, 40.0), h_m=20.0,              # "40-45m" maximum S7 (lower figure)
                crown_m=14.0,                                # "dense, irregular and dome shaped" S7: rule 0.7 x h
                bloom=[], leaf=PLA_LEAF_SITE,                # "early spring or even in autumn" S7: no months
                colours=_pla_c(_sec_mix("727A4E", SEC["paper"], 0.15))),   # CORE green_mid
    "willow": dict(name="White willow", turkish="Ak söğüt", latin="Salix alba", layer="tree",
                   form="weeping", foliage="deciduous (not quoted)", status="keep",
                   h_range=(None, 30.0), h_m=15.0,           # "up to 30 m" S4
                   crown_m=10.5,                             # crown not found: rule 0.7 x h
                   bloom=[], leaf=PLA_LEAF_SITE,             # "spring" catkins S4: no months
                   colours=_pla_c(_sec_mix("8C9969", SEC["paper"], 0.3))),  # CORE green_light, silvered
    "olive": dict(name="Olive", turkish="Zeytin", latin="Olea europaea", layer="tree",
                  form="gnarled", foliage="evergreen (S72)", status="keep",
                  h_range=(8.0, 15.0), h_m=11.5,             # "8-15 m" S72
                  crown_m=10.35,                             # crown not found: rule 0.9 x h
                  bloom=[4], leaf=PLA_ALL_YEAR,              # full bloom 21-24 Apr, ends 29 Apr-1 May S73 (Ege Univ.)
                  colours=_pla_c(SEC["olive"])),             # section_style SEC olive
    "stone_pine": dict(name="Stone pine", turkish="Fıstık çamı", latin="Pinus pinea", layer="tree",
                       form="umbrella", foliage="evergreen conifer (S74)", status="keep (processionary caterpillar)",
                       h_range=(25.0, 30.0), h_m=27.5,       # "25-30 m" S74
                       crown_m=15.1,                         # "umbrella-shaped ... flat and broad" S74: rule 0.55 x h
                       bloom=[], leaf=PLA_ALL_YEAR,          # pollen months not found
                       colours=_pla_c(SEC["pine"])),         # section_style SEC pine
    "tamarisk": dict(name="Tamarisk", turkish="Ilgın", latin="Tamarix smyrnensis", layer="tree",
                     form="feathery", foliage="deciduous (S9b, genus)", status="keep (replaces oleander)",
                     h_range=(4.0, 15.0), h_m=9.5,           # "4-15 m" S9b (genus)
                     crown_m=7.6,                            # "broad, bushy" S9b: rule 0.8 x h
                     bloom=[], leaf=PLA_LEAF_SITE,           # bloom not found for T. smyrnensis
                     colours=_pla_c(_sec_mix("8C9969", SEC["paper"], 0.45))),  # CORE green_light, pale
    "chaste": dict(name="Chaste tree", turkish="Hayıt", latin="Vitex agnus-castus", layer="shrub",
                   form="multistem", foliage="deciduous (S58)", status="keep (replaces oleander, fig, citrus)",
                   h_range=(1.0, 3.0), h_m=2.0,              # "1-3 m" S58
                   crown_m=2.0,                              # "1.5-2.5 m" S67 (RHS, UK)
                   bloom=[6, 7, 8, 9], leaf=PLA_LEAF_SITE,   # "(Apr-)Jun-Sep" S58 (Crete); Apr-May occasional
                   colours=_pla_c(SEC["shrub"], SEC["lav"])),  # flower colour not sourced: section_style lav
    "rosemary": dict(name="Rosemary", turkish="Biberiye", latin="Salvia rosmarinus", layer="shrub",
                     form="mound", foliage="evergreen (S58, S71)", status="keep",
                     h_range=(0.5, 1.0), h_m=0.75,           # "50-100 cm" S58 (Crete)
                     crown_m=0.75,                           # "1.5-2.5 m" S71 for 1.5-2.5 m plants: scaled to h
                     bloom=[1, 2, 3, 4, 5], leaf=PLA_ALL_YEAR,  # "Jan-May, intermittently to Dec" S58
                     colours=_pla_c(_sec_mix("495338", SEC["paper"], 0.35))),  # CORE green_deep
    "lavender": dict(name="French lavender", turkish="Karabaş otu", latin="Lavandula stoechas", layer="ground",
                     form="mound", foliage="evergreen (UNVERIFIED)", status="keep",
                     h_range=(0.3, 0.8), h_m=0.55,           # "30-80 cm" S58
                     crown_m=0.66,                           # crown not found: rule 1.2 x h
                     bloom=[3, 4, 5], leaf=[],               # "Mar-May" S58; evergreen unverified: no leaf months
                     colours=_pla_c(_sec_mix(SEC["olive"], SEC["paper"], 0.1), SEC["lav"])),  # as sec_lavender
    "loosestrife": dict(name="Purple loosestrife", turkish="Aklar otu", latin="Lythrum salicaria", layer="emergent",
                        form="clump", foliage="herbaceous perennial", status="keep, flower heads cut in Sep (D6)",
                        h_range=(0.3, 2.4), h_m=1.35,        # "0.3-2.4 m" S19
                        crown_m=0.75,                        # "5 feet (1.5 m) wide" mature S19: half the maximum
                        bloom=[6, 7, 8, 9], leaf=[],         # "June ... September" S19; cut Sep (D6)
                        colours=_pla_c(SEC["grass"], PLA_PURPLE)),
    "soft_rush": dict(name="Soft rush", turkish="UNVERIFIED", latin="Juncus effusus", layer="emergent",
                      form="clump", foliage="not found", status="new (replaces iris and cattail)",
                      h_range=(0.5, 1.5), h_m=1.0,           # "5-15 dm tall" S59
                      crown_m=0.6,                           # "tufted, cespitose" S59: rule 0.6 x h
                      bloom=[5, 6, 7, 8], leaf=[],           # "late May-Aug, occasionally Sep" S59 (USA)
                      colours=_pla_c(SEC["reed"])),          # section_style SEC reed
    "rush": dict(name="Sharp rush", turkish="Kofa", latin="Juncus acutus", layer="emergent",
                 form="tussock", foliage="not found", status="keep, away from paths and the wading strip",
                 h_range=(0.6, 1.0), h_m=0.8,                # "(40-)60-100 cm" S65
                 crown_m=0.8,                                # "dense tussock" S60, S65: rule 1.0 x h
                 bloom=[], leaf=[],                          # "summer" S65 (NZ): no months
                 colours=_pla_c(_sec_mix(SEC["reed"], "495338", 0.3))),   # SEC reed toward CORE green_deep
    "reed": dict(name="Common reed", turkish="Kamış", latin="Phragmites australis", layer="emergent",
                 form="stand", foliage="deciduous (S2)", status="lined off-line basins only (D2 a): pla_reed_basin",
                 h_range=(None, 6.0), h_m=3.0,               # "may reach 20 feet (6 m)" S2 (booklet drew 1.9-2.2 m)
                 crown_m=None,                               # clonal stand, no crown
                 bloom=[7, 8, 9, 10, 11], leaf=[],           # "July to November" S2 (range-wide); plumes cut before Nov
                 colours=_pla_c(SEC["reed"], SEC["reed_head"])),
    "mint": dict(name="Water mint", turkish="Su nanesi", latin="Mentha aquatica", layer="emergent",
                 form="mound", foliage="deciduous (S57)", status="lined basin cells only (D6): pla_mint_cell",
                 h_range=(0.3, 0.8), h_m=0.55,               # "30-80 cm" S58
                 crown_m=0.75,                               # "spread 0.5-1 m" S57
                 bloom=[5, 6, 7, 8, 9], leaf=[],             # "May-Sep" S58
                 colours=_pla_c(SEC["grass"])),              # section_style SEC grass
    "giant_reed": dict(name="Giant reed", turkish="Kargı", latin="Arundo donax", layer="emergent",
                       form="cane", foliage="not found", status="REMOVE (raises flood risk, S36)",
                       h_range=(None, None), h_m=None, crown_m=None,   # not in species_data: pass h_m and crown_m
                       bloom=[], leaf=[],
                       colours=_pla_c(SEC["beyond"], PLA_REMOVE)),
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


def _pla_cols(sp, beyond):
    c = dict(sp["colours"])
    if beyond:                                  # beyond the cut: paler (as SEC beyond)
        c = dict((k_, _sec_mix(v, SEC["paper"], 0.55) if v else v) for k_, v in c.items())
    return c


def _pla_sec(form, x, gy, h, w, k, c, seed=0):
    """Section silhouette of one form, h tall and w crown wide (m), ground at (x, gy) page mm."""
    import math as _m
    H, R = h * k, w / 2.0 * k
    f, e, lt, st, ac = c["fill"], c["edge"], c["lt"], c["stem"], c.get("accent")
    sh = []
    if form in ("dome", "oval", "weeping", "gnarled", "umbrella"):
        lo = dict(dome=0.3, oval=0.3, weeping=0.25, gnarled=0.3, umbrella=0.65)[form] * H   # clear stem (rule)
        tw = max(0.15, h / 60.0 * k)            # half trunk width: trunk 1/30 of the height (rule)
        yb, yt = gy + lo, gy + H
        Hc = yt - yb
        if form == "gnarled":                   # two twisting stems
            for s_ in (-1, 1):
                sh.append(("poly", [(x + s_ * 0.2 * tw, gy), (x + s_ * 1.6 * tw, gy),
                                    (x + s_ * (0.35 * R + tw * 0.5), yb + 0.3 * Hc),
                                    (x + s_ * (0.35 * R - tw * 0.5), yb + 0.3 * Hc)], st, None, 0.1))
        else:
            lean = 0.03 * H if form == "umbrella" else 0.0
            sh.append(("poly", [(x - tw, gy), (x + tw, gy), (x + lean + tw * 0.6, yb + 0.4 * Hc),
                                (x + lean - tw * 0.6, yb + 0.4 * Hc)], st, None, 0.1))
        if form == "weeping":                   # the hanging curtain behind the crown
            c0 = yb + 0.45 * Hc
            sh.append(("poly", [(x - R, c0), (x - 0.9 * R, gy + 0.2 * H), (x + 0.9 * R, gy + 0.2 * H), (x + R, c0)],
                       lt, None, 0.1))
        if form == "gnarled":                   # low and wide: three irregular masses
            for cx_, cy_, rx_, up_, i in ((x - 0.5 * R, yb + 0.4 * Hc, 0.5 * R, 0.4 * Hc, 0),
                                          (x + 0.5 * R, yb + 0.45 * Hc, 0.5 * R, 0.4 * Hc, 1),
                                          (x, yb + 0.62 * Hc, 0.55 * R, 0.38 * Hc, 2)):
                dn_ = cy_ - yb if i < 2 else 0.38 * Hc
                sh.append(("poly", _pla_crown(cx_, cy_, rx_, up_, dn_, seed + i, 0.18), f, e, 0.08))
        else:
            fr = dict(dome=(0.3, 0.06), oval=(0.5, 0.08), weeping=(0.45, 0.05), umbrella=(0.35, 0.04))[form]
            c0 = yb + fr[0] * Hc
            sh.append(("poly", _pla_crown(x, c0, R, yt - c0, c0 - yb, seed, fr[1]), f, e, 0.08))
            for i, (dx, dy, s_) in enumerate(((-0.4, 0.3, 0.32), (0.35, 0.15, 0.3), (-0.05, 0.6, 0.26))):
                sh.append(("poly", _pla_crown(x + dx * R, c0 + dy * (yt - c0), s_ * R, s_ * (yt - c0) * 0.8,
                                              s_ * (yt - c0) * 0.6, seed + i + 1, 0.1), lt, None, 0.1))
        if form == "weeping":                   # strands
            for i in range(9):
                xs = x - 0.85 * R + i * 1.7 * R / 8.0
                s_ = -1 if xs < x else 1
                yh = gy + (0.2 + 0.08 * _pla_rnd(i, seed)) * H
                y0 = yb + 0.3 * Hc
                sh.append(("line", [(xs, y0), (xs + s_ * 0.04 * R, (y0 + yh) / 2.0), (xs + s_ * 0.06 * R, yh)], e, 0.1))
        if form in ("dome", "oval"):            # a few branches
            for s_, a in ((-1, 55.0), (1, 45.0), (1, 75.0)):
                r_ = _m.radians(a)
                sh.append(("line", [(x, yb + 0.3 * Hc), (x + s_ * _m.cos(r_) * R * 0.5, yb + (0.3 + 0.4 * _m.sin(r_))
                                                         * Hc)], st, max(0.08, tw * 0.5)))
        return sh
    if form == "feathery":                      # tamarisk: slender stems, an airy crown, hanging wisps
        for i in range(4):
            sh.append(("line", [(x + (i - 1.5) * 0.04 * R, gy), (x + (i - 1.5) * 0.3 * R, gy + 0.55 * H)], st, 0.15))
        c0 = gy + 0.55 * H
        ring = _pla_crown(x, c0, R, 0.45 * H, 0.4 * H, seed, 0.14)
        sh.append(("poly", ring, f, None, 0.1))
        for i in range(0, len(ring), 2):
            px, py = ring[i]
            if py > c0 - 0.3 * H:
                sh.append(("line", [(px, py), (px + (px - x) * 0.04, py - 0.1 * H)], e, 0.08))
        return sh
    if form == "multistem":                     # chaste tree: stems fanning from the ground, heads at their ends
        heads = ((-0.7, 0.6, 0.25), (-0.35, 0.68, 0.27), (0.0, 0.72, 0.28), (0.35, 0.66, 0.27), (0.7, 0.58, 0.25))
        for dx, cy_, ry_ in heads:
            sh.append(("line", [(x + dx * 0.1 * R, gy), (x + dx * R, gy + cy_ * H)], st, 0.15))
        for i, (dx, cy_, ry_) in enumerate(heads):
            sh.append(("poly", _pla_crown(x + dx * R, gy + cy_ * H, 0.3 * R, ry_ * H, ry_ * H * 0.8, seed + i, 0.12),
                       f, e, 0.06))
        if ac:
            for dx, cy_, ry_ in heads:
                top = gy + (cy_ + ry_) * H
                sh.append(("line", [(x + dx * R, top - 0.14 * H), (x + dx * R, top - 0.01 * H)], ac, 0.3))
        return sh
    if form == "mound":                         # lavender, rosemary, water mint: a low dome on the ground
        sh.append(("poly", _pla_crown(x, gy + 0.35 * H, R, 0.65 * H, 0.35 * H, seed, 0.1), f, e, 0.06))
        if ac:                                  # flower spikes in the top of the mound
            for d in (-0.5, -0.2, 0.15, 0.45):
                sh.append(("line", [(x + d * R, gy + 0.72 * H), (x + d * R * 1.1, gy + 0.97 * H)], ac, 0.25))
        else:
            for d in (-0.55, -0.25, 0.05, 0.35, 0.6):
                sh.append(("line", [(x + d * R, gy + 0.35 * H), (x + d * R * 1.05, gy + 0.7 * H)], lt, 0.1))
        return sh
    if form in ("clump", "tussock", "cane"):    # rushes and loosestrife: stems from one base; giant reed: canes
        n = dict(clump=13, tussock=21, cane=7)[form]
        for i in range(n):
            t = i / float(n - 1)
            hh = H * (0.82 + 0.18 * _pla_rnd(i, seed + 3))
            bx, tx = x + (2 * t - 1) * R * 0.15, x + (2 * t - 1) * R
            if form == "clump":                 # soft arch
                mx = bx + (tx - bx) * 0.35
                sh.append(("line", [(bx, gy), (mx, gy + 0.55 * hh), (tx, gy + hh)], f, 0.12))
                if ac and i % 2 == 0:           # loosestrife flower spike on the upper stem
                    sh.append(("line", [(mx + (tx - mx) * 0.3, gy + 0.69 * hh), (tx, gy + hh)], ac, 0.35))
            else:
                sh.append(("line", [(bx, gy), (tx, gy + hh)], f, 0.15 if form == "cane" else 0.1))
                if form == "cane":              # leaf blades along the cane
                    for j in range(1, 5):
                        py = gy + hh * j / 5.0
                        px = bx + (tx - bx) * j / 5.0
                        s_ = 1 if (i + j) % 2 else -1
                        sh.append(("line", [(px, py), (px + s_ * 0.35 * R, py - 0.06 * hh)], f, 0.1))
        if form == "cane" and ac:               # marked for removal
            sh.append(("line", [(x - R, gy), (x + R, gy + H)], ac, 0.35))
            sh.append(("line", [(x - R, gy + H), (x + R, gy)], ac, 0.35))
        return sh
    raise ValueError("_pla_sec: unknown form %r" % form)


def _pla_scallop(cx, cy, r, m, depth, n=72):
    """A scalloped circle of radius r (its bumps reach r), m bumps."""
    import math as _m
    return [(cx + r * (1.0 - depth * _m.sin(m * a / 2.0) ** 2) * _m.cos(a),
             cy + r * (1.0 - depth * _m.sin(m * a / 2.0) ** 2) * _m.sin(a))
            for a in [2 * _m.pi * i / n for i in range(n)]]


def _pla_plan(form, cx, cy, w, k, c, seed=0):
    """Top view of one form, crown w wide (m), centre (cx, cy) page mm."""
    import math as _m
    r = w / 2.0 * k
    f, e, lt, st, ac = c["fill"], c["edge"], c["lt"], c["stem"], c.get("accent")
    sh = []
    dot = ("poly", sec_ellipse(cx, cy, max(0.2, 0.04 * r), max(0.2, 0.04 * r), 10), st, None, 0.1)
    if form in ("dome", "oval"):
        m, dp, s_ = (10, 0.1, 0.3) if form == "dome" else (16, 0.06, 0.22)
        sh.append(("poly", _pla_scallop(cx, cy, r, m, dp), f, e, 0.08))
        for i in range(3 if form == "dome" else 4):
            a = 2 * _m.pi * (i / (3.0 if form == "dome" else 4.0) + _pla_rnd(seed, 4))
            sh.append(("poly", _pla_scallop(cx + 0.45 * r * _m.cos(a), cy + 0.45 * r * _m.sin(a), s_ * r, 6, 0.12),
                       lt, None, 0.1))
        return sh + [dot]
    if form == "weeping":
        sh.append(("poly", _pla_scallop(cx, cy, r, 24, 0.04), f, e, 0.08))
        for i in range(20):
            a = 2 * _m.pi * i / 20.0
            sh.append(("line", [(cx + 0.25 * r * _m.cos(a), cy + 0.25 * r * _m.sin(a)),
                                (cx + 0.95 * r * _m.cos(a), cy + 0.95 * r * _m.sin(a))], e, 0.08))
        return sh + [dot]
    if form == "gnarled":                       # three masses, as in section
        for i in range(3):
            a = 2 * _m.pi * (0.25 + i / 3.0)
            sh.append(("poly", _pla_crown(cx + 0.45 * r * _m.cos(a), cy + 0.45 * r * _m.sin(a), 0.55 * r, 0.55 * r,
                                          0.55 * r, seed + i, 0.18), f, e, 0.08))
        return sh + [dot]
    if form == "umbrella":                      # flat disc with needle tufts at the rim
        sh.append(("poly", _pla_scallop(cx, cy, r, 30, 0.03), f, e, 0.08))
        for i in range(30):
            a = 2 * _m.pi * i / 30.0
            sh.append(("line", [(cx + 0.75 * r * _m.cos(a), cy + 0.75 * r * _m.sin(a)),
                                (cx + 0.96 * r * _m.cos(a), cy + 0.96 * r * _m.sin(a))], lt, 0.1))
        return sh + [dot]
    if form == "feathery":
        sh.append(("poly", _pla_crown(cx, cy, r, r, r, seed, 0.14), f, None, 0.1))
        for i in range(28):
            a = 2 * _m.pi * i / 28.0
            sh.append(("line", [(cx + 0.82 * r * _m.cos(a), cy + 0.82 * r * _m.sin(a)),
                                (cx + 0.82 * r * _m.cos(a + 0.12), cy + 0.82 * r * _m.sin(a + 0.12))], e, 0.08))
        return sh + [dot]
    if form == "multistem":                     # five heads, as in section
        for i in range(5):
            a = 2 * _m.pi * (i / 5.0 + 0.05)
            hx, hy = cx + 0.55 * r * _m.cos(a), cy + 0.55 * r * _m.sin(a)
            sh.append(("poly", _pla_crown(hx, hy, 0.45 * r, 0.45 * r, 0.45 * r, seed + i, 0.12), f, e, 0.06))
            if ac:
                sh.append(("poly", sec_ellipse(hx, hy, 0.08 * r, 0.08 * r, 8), ac, None, 0.1))
        return sh
    if form == "mound":
        sh.append(("poly", _pla_crown(cx, cy, r, r, r, seed, 0.1), f, e, 0.06))
        for i in range(6):
            a = 2 * _m.pi * (i / 6.0 + _pla_rnd(seed, 6))
            px, py = cx + 0.5 * r * _m.cos(a), cy + 0.5 * r * _m.sin(a)
            if ac:
                sh.append(("poly", sec_ellipse(px, py, 0.12 * r, 0.12 * r, 8), ac, None, 0.1))
            else:
                sh.append(("line", [(px, py), (px + 0.2 * r * _m.cos(a), py + 0.2 * r * _m.sin(a))], lt, 0.1))
        return sh
    if form in ("clump", "tussock", "cane"):    # stems seen from above: a starburst
        n = dict(clump=13, tussock=21, cane=9)[form]
        for i in range(n):
            a = 2 * _m.pi * (i / float(n) + 0.3 * _pla_rnd(i, seed))
            ll = r * (0.8 + 0.2 * _pla_rnd(i, seed + 2))
            sh.append(("line", [(cx, cy), (cx + ll * _m.cos(a), cy + ll * _m.sin(a))], f, 0.12))
            if ac and form == "clump" and i % 2 == 0:
                sh.append(("poly", sec_ellipse(cx + ll * _m.cos(a), cy + ll * _m.sin(a), 0.08 * r + 0.1,
                                               0.08 * r + 0.1, 8), ac, None, 0.1))
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


def pla_section(key, x, gy, k, h_m=None, crown_m=None, beyond=False, seed=0):
    """A species in section at true size: ground at (x, gy) page mm (gy may be a function of x)."""
    sp = _pla_get(key)
    h, w = _pla_size(key, sp, h_m, crown_m)
    return _pla_sec(sp["form"], x, gy(x) if callable(gy) else gy, h, w, k, _pla_cols(sp, beyond), seed)


def pla_plan(key, cx, cy, k, crown_m=None, beyond=False, seed=0):
    """The same species from above: crown crown_m wide (m) centred on (cx, cy) page mm, same form and colour."""
    sp = _pla_get(key)
    w = crown_m or sp["crown_m"]
    if w is None:
        raise ValueError("plants: %s has no sourced crown: pass crown_m" % key)
    return _pla_plan(sp["form"], cx, cy, w, k, _pla_cols(sp, beyond), seed)


def _pla_crop_size(crop, h_m, crown_m):
    if crop == "olive":                         # orchard trees kept to their in-row spacing (rule); h by the olive ratio
        w = crown_m or PLA_CROPS["olive"]["plant_m"]
        return h_m or w / PLA_FORM_RATIO["gnarled"], w
    if h_m is None or crown_m is None:
        raise ValueError("plants: %s plant size is not sourced: pass h_m and crown_m" % crop)
    return h_m, crown_m


def _pla_crop_sec(crop, x, gy, h, w, k, i, beyond):
    """One crop plant in section."""
    if crop == "olive":
        return _pla_sec("gnarled", x, gy, h, w, k, _pla_cols(PLA_SPECIES["olive"], beyond), i)
    H, R = h * k, w / 2.0 * k
    c = _pla_cols(dict(colours=_pla_c(SEC["grass"])), beyond)
    if crop == "maize":                         # stalk, arching leaves, tassel
        sh = [("line", [(x, gy), (x, gy + H)], c["fill"], 0.2)]
        for j in range(1, 7):
            py, s_ = gy + H * (0.15 + 0.11 * j), (1 if j % 2 else -1)
            sh.append(("line", [(x, py), (x + s_ * R * 0.6, py + 0.08 * H), (x + s_ * R, py - 0.02 * H)], c["fill"],
                       0.12))
        sh.append(("line", [(x, gy + 0.92 * H), (x, gy + H)], SEC["reed_head"], 0.35))
        return sh
    if crop == "cotton":                        # small branched bush with open bolls
        sh = [("line", [(x, gy), (x, gy + 0.5 * H)], c["stem"], 0.12),
              ("poly", _pla_crown(x, gy + 0.55 * H, R, 0.45 * H, 0.3 * H, i, 0.15), c["fill"], c["edge"], 0.06)]
        for d, e_ in ((-0.5, 0.6), (0.1, 0.85), (0.55, 0.55)):
            sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.1 * R + 0.1, 0.1 * R + 0.1, 8), PLA_BOLL,
                       c["edge"], 0.05))
        return sh
    if crop == "tomato":                        # low sprawling plant with fruit
        sh = [("poly", _pla_crown(x, gy + 0.3 * H, R, 0.7 * H, 0.3 * H, i, 0.15), c["fill"], c["edge"], 0.06)]
        for d, e_ in ((-0.45, 0.35), (0.2, 0.5), (0.6, 0.3)):
            sh.append(("poly", sec_ellipse(x + d * R, gy + e_ * H, 0.08 * R + 0.1, 0.08 * R + 0.1, 8), PLA_FRUIT,
                       None, 0.1))
        return sh
    raise ValueError("plants: unknown crop %r" % crop)


def pla_crop_rows(crop, x0, x1, gy, k, spacing=None, h_m=None, crown_m=None, beyond=False):
    """Crop plants along a cut from x0 to x1 (page mm), spacing m apart (the row spacing for a cut across the rows;
    sourced default only for olive), centred in the stretch; gy a number or a function of x."""
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    sp = spacing or PLA_CROPS[crop]["row_m"]
    if sp is None:
        raise ValueError("plants: %s row spacing is not sourced: pass spacing (m)" % crop)
    h, w = _pla_crop_size(crop, h_m, crown_m)
    n = int((x1 - x0) / (sp * k) + 1e-9)
    off = ((x1 - x0) - n * sp * k) / 2.0
    sh = []
    for i in range(n + 1):
        x = x0 + off + i * sp * k
        sh += _pla_crop_sec(crop, x, gy(x) if callable(gy) else gy, h, w, k, i, beyond)
    return sh


def _pla_ring(rr):
    """A ring from a ring or an (x0, y0, x1, y1) rectangle (page mm)."""
    if len(rr) == 4 and not isinstance(rr[0], (tuple, list)):
        x0, y0, x1, y1 = rr
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return list(rr)


def pla_crop_plan(crop, ring_or_rect, k, row_spacing=None, plant_spacing=None, ang_deg=0.0, crown_m=None,
                  field=True):
    """A field or orchard block in plan: rows at row_spacing (m) at ang_deg; with plant_spacing, single plants along
    each row (true crown with crown_m or for olive, else a fixed 0.25 mm dot). Sourced defaults only for olive."""
    import math as _m
    if crop not in PLA_CROPS:
        raise ValueError("plants: unknown crop %r" % crop)
    ring = _pla_ring(ring_or_rect)
    rs = row_spacing or PLA_CROPS[crop]["row_m"]
    ps = plant_spacing or PLA_CROPS[crop]["plant_m"]
    if rs is None:
        raise ValueError("plants: %s row spacing is not sourced: pass row_spacing (m)" % crop)
    sh = [("poly", ring, PLA_FIELD, None, 0.1)] if field else []
    w = crown_m or (PLA_CROPS["olive"]["plant_m"] if crop == "olive" else None)   # olive: crown = in-row spacing
    for i, (p, q) in enumerate(sec_hatch(ring, rs * k, ang_deg)):
        if ps is None:
            sh.append(("line", [p, q], PLA_ROW, 0.15))
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
                sh += _pla_plan("gnarled", px, py, w, k, _pla_cols(PLA_SPECIES["olive"], False), i * 31 + j)
            elif w:
                sh.append(("poly", _pla_crown(px, py, w / 2.0 * k, w / 2.0 * k, w / 2.0 * k, i * 31 + j, 0.12),
                           SEC["grass"], SEC["ink2"], 0.05))
            else:
                sh.append(("poly", sec_ellipse(px, py, 0.125, 0.125, 8), PLA_ROW, None, 0.1))
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


def pla_reed_basin(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, step_m=None):
    """Common reed in a lined, root-contained, off-line basin (D2 a) in section: inside x0-x1, floor bed_y, rim rim_y
    (page mm). kerb_t_m 0.15 m and floor slab = drawing rule; stems step_m apart."""
    sp = PLA_SPECIES["reed"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h = h_m or sp["h_m"]
    st = (step_m or 1.0 / 3.0) * k              # 9 seedlings/m² (Korkusuz et al. 2004, S20) = 1/3 m apart
    c = sp["colours"]
    i, x = 0, x0 + st / 2.0
    while x < x1:
        hh = h * k * (0.8 + 0.2 * _pla_rnd(i, 5))
        lean = 0.04 * hh * (1 if i % 2 else -1)
        sh.append(("line", [(x, g), (x + lean, g + hh)], c["fill"], 0.12))
        if i % 3 == 0:                          # plume (cut before seed release in Nov, S11)
            ry = 0.2 * k + 0.2
            sh.append(("poly", sec_ellipse(x + lean, g + hh - ry, 0.06 * k + 0.1, ry, 10), c["accent"], None, 0.1))
        x += st
        i += 1
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_mint_cell(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m=0.15, media_m=None, wl_y=None, h_m=None, crown_m=None):
    """Water mint only in a lined basin cell (D6) in section, same build as pla_reed_basin; mounds side by side."""
    sp = PLA_SPECIES["mint"]
    sh, g = _pla_lined(x0, x1, bed_y, rim_y, k, kerb_h_m, kerb_t_m, media_m, wl_y)
    h, w = h_m or sp["h_m"], crown_m or sp["crown_m"]
    n = max(1, int((x1 - x0) / (w * k)))
    for i in range(n):
        sh += _pla_sec("mound", x0 + (i + 0.5) * (x1 - x0) / n, g, h, min(w, (x1 - x0) / n / k), k,
                       sp["colours"], i)
    return sh + _pla_liner(x0, x1, bed_y, rim_y, k, kerb_h_m)


def pla_cell_plan(kind, ring_or_rect, k, kerb_t_m=0.15):
    """A lined cell in plan, kind 'reed' or 'mint': wet ground, the kerb as a band kerb_t_m wide, the plants."""
    import math as _m
    if kind not in ("reed", "mint"):
        raise ValueError("pla_cell_plan: kind is 'reed' or 'mint'")
    ring = _pla_ring(ring_or_rect)
    sp = PLA_SPECIES[kind]
    sh = [("poly", ring, PLA_WET, None, 0.1)]
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    if kind == "reed":                          # stems on the 1/3 m grid, never denser than 0.9 mm on the page
        d = max(0.9, k / 3.0)
        c = sp["colours"]["fill"]
        for i in range(int((max(xs) - min(xs)) / d) + 1):
            for j in range(int((max(ys) - min(ys)) / d) + 1):
                px = min(xs) + (i + 0.5 * (j % 2) + 0.25) * d
                py = min(ys) + (j + 0.5) * d
                if _sct_inside(ring, (px, py)):
                    sh.append(("line", [(px - 0.2 * d, py - 0.25 * d), (px + 0.2 * d, py + 0.25 * d)], c, 0.1))
    else:
        w = sp["crown_m"] * k
        for i in range(int((max(xs) - min(xs)) / w) + 1):
            for j in range(int((max(ys) - min(ys)) / w) + 1):
                px, py = min(xs) + (i + 0.5) * w, min(ys) + (j + 0.5) * w
                if _sct_inside(ring, (px, py)):
                    sh += _pla_plan("mound", px, py, sp["crown_m"] * 0.9, k, sp["colours"], i * 7 + j)
    sh.append(("poly", ring, None, SCT["line"], max(0.15, kerb_t_m * k)))
    return sh
