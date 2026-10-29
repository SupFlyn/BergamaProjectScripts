SPECIES = [  # p.17 (water board v6, revision 29 Oct 2026, T4a WO-T4a-2): the species of the catalogue, from
    # revision_2026-10-29/T1/ecology/species.json "species_data" (water, role; their words shortened, nothing added)
    # with the public sources of their values (T1/ecology/RESULT.md §D, S-numbers in the comments). Foliage, height
    # and months are read from plants.py (PLA_SPECIES, pla_months) at the press. D2: common reed only in lined
    # basins; D6: no yellow flag iris (purple loosestrife + soft rush), water mint only in lined cells.
    # key: plants.py species key; water: (class wet | moist | dry, keywords); role: species.json roles; src: printed
    # through cite() (public sources only)
    dict(key="reed", water=("wet", u"wet ground: lined basins only"), role=["clean"],
         src=u"Gucker 2008, Phragmites australis, FEIS, USDA Forest Service; Robinson 2002, Common Reed: An Invasive "
             u"Wetland Plant, Massachusetts DCR; Korkusuz, Beklioğlu & Demirer 2004, Turkish J. Eng. Env. Sci. 28"),   # S2, S11, S20
    dict(key="mint", water=("wet", u"permanently wet ground"), role=["clean", "scent"],
         src=u"Walker, Mentha aquatica, BSBI Plant Atlas 2020; RHS, Mentha aquatica 'Mandeliensis'; Cretan Flora "
             u"(S. Lenton), Mentha aquatica"),                                                    # S56, S57, S58
    dict(key="soft_rush", water=("wet", u"flooded or fluctuating soils"), role=["clean", "hold the bank"],
         src=u"Stevens 2000, Soft Rush Plant Guide, USDA NRCS"),                                  # S59
    dict(key="loosestrife", water=("wet", u"quite flood tolerant"), role=["clean", "flower"],
         src=u"Munger 2002, Lythrum salicaria, FEIS, USDA Forest Service; Xie et al. 2021, Water 13(21) 2957"),   # S19, S23
    dict(key="willow", water=("wet", u"tolerant to inundation"), role=["hold the bank", "shade", "clean"],
         src=u"Houston Durrant, de Rigo & Caudullo 2016, Salix alba in Europe, European Atlas of Forest Tree Species"),   # S4
    dict(key="tamarisk", water=("moist", u"survives long inundation, drought tolerant"), role=["hold the bank", "shade"],
         src=u"Guerrero Maldonado, López & Caudullo 2016, Tamarix in Europe, European Atlas of Forest Tree Species"),   # S9b
    dict(key="chaste", water=("moist", u"streams that flow in winter only"), role=["scent", "hold the bank"],
         src=u"Cretan Flora (S. Lenton), Vitex agnus-castus; Livne, Vitex agnus-castus, Flowers in Israel; RHS, "
             u"Vitex agnus-castus"),                                                              # S58, S66, S67
    dict(key="ash", water=("moist", u"moist soils, temporary flooding"), role=["shade", "hold the bank"],
         src=u"Caudullo & Houston Durrant 2016, Fraxinus angustifolia in Europe, European Atlas of Forest Tree "
             u"Species"),                                                                         # S7
    dict(key="plane", water=("moist", u"drought-sensitive: watered from storage"), role=["shade"],
         src=u"EUFORGEN, Platanus orientalis; Velikova et al. 2018, Conservation Physiology 6(1); Herbari Virtual del "
             u"Mediterrani Occidental, Platanus orientalis; Mahmiyat, Oriental plane tree; RHS, Platanus orientalis"),   # S26, S27, S68-S70
    dict(key="olive", water=("dry", u"well adapted to drought"), role=["harvest", "shade"],
         src=u"Guerrero Maldonado et al. 2016, Olea europaea in Europe, European Atlas of Forest Tree Species; "
             u"Gültekinoğlu, Acarsoy Bilgin & İsfendiyaroğlu 2025, Bahçe 54(2)"),                  # S72, S73
    dict(key="rosemary", water=("dry", u"well-drained soil"), role=["scent"],
         src=u"Cretan Flora (S. Lenton), Rosmarinus officinalis; RHS, Rosmarinus officinalis"),   # S58, S71
    dict(key="lavender", water=("dry", u"dry ground, survived 17 days flooded"), role=["scent"],
         src=u"Cretan Flora (S. Lenton), Lavandula stoechas; RHS, Waterlogging and Mediterranean plant species"),   # S58, S38
]
SPECIES_REMOVE = (u"giant_reed", u"**remove**: raises **flood risk**, blocks the channel",   # (plant key, words, source)
                  u"Bruno et al. 2019, Water (Segura basin, Arundo donax)")                   # S36
