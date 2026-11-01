# ---- MIRAQUA round 28 Oct 2026 (site board v50): p.20 the heritage loop (worker SB-heritage). Shared pieces: parts/15h_r28_shared.py,
# common/r28_style.py, common/units.py, common/label_place.py, common/figures.py (revision_2026-10-28/PLAN.md).
# v50 (MIRAQUA 28 Oct, P20.1-P20.3, D2, F13; replaces v46/v49.1's draw_heritage_loop in 15f and HER_LOOP / HER_OFF in
# 15d): THE HERITAGE LOOP on the survey, not on the site frame. D2 (asked 28 Oct, default B until Aras answers) is the
# switch HER_EXTENT:
#   "loop"   ONE map at 1:10,000, north up, holding every stop the survey covers, the whole-file survey (S.whole, plan
#            01's model) as quiet context with the study area inside it, the stops numbered in loop order and one short
#            text each under the map (crop drw_heritage_loop); beside it a key map of the survey's whole drawn bulk with
#            the loop map's extent and the study area (NEW crop drw_heritage_key, no scale: a key map). North up, not on
#            the frame axis: both fit the page, but on the frame axis the leg to Akropol would run ~80 mm along the
#            map's top edge; north up it leaves the map ~23 mm from the gondola station.
#   "survey" the survey's whole drawn bulk at 1:20,000 with the loop core (K3-K4, Kızıl Avlu, Ulucami) at 1:5,000 beside
#            it, keyed to it by its frame, each with its own scale bar, the list under the inset (one crop
#            drw_heritage_loop; no key crop).
# Akropol is the one destination the survey does not cover (3dm_checks §3: nearest survey line 259 m): an arrow at
# the map's edge with its straight distance, no long line. The legs are soft lines stop to stop (no dashes), the stream
# walk K3-K4 a broad soft band along the stream's centre line (the spine). Names Turkish from the names table (v59,
# round 4, G-R4-11), texts from public online sources only (F5, HER_SRC), keywords bold (G5), names on the maps placed
# by the shared label_place (G4), base tones as b_base but lighter where they are only context (G6).
HER_EXTENT = "loop"     # D2: "loop" (B, default) or "survey" (A: whole survey 1:20,000 + loop-core inset 1:5,000)
HER_DEN, HER_SV_DEN, HER_IN_DEN = 10000, 20000, 5000      # the loop map, the whole survey, the inset (booklet page)
HER_SB_M = {10000: 400.0, 20000: 1000.0, 5000: 200.0}     # m: the scale bar under each map (four parts)
HER_MAP_BK_W, HER_MAP_BK_H = 226.0, 140.0  # mm: the loop map on the booklet page (crop 227 mm: grid columns 1-7)
HER_KEY_BK_W = 160.0    # mm: the key map (crop 161 mm: grid columns 8-12; at most 190): 227 + 4 + 161 = 392 mm
HER_GUT_MM = 5.0        # mm between the two drawings on the sheet (booklet gutter 4 + the crops' 0.5 mm edges)
HER_GAP_MM = 6.0        # mm: between the list's columns, and between the survey map and its inset column (BK_GAP_MM)
HER_SV_MAX_MM = (270.0, 205.0)   # mm: the most the whole-survey map may take ("survey"), the inset column beside it
HER_IN_BK_H = 100.0     # mm: the inset's height ("survey")
HER_MARGIN_M = 150.0    # m: at least this much survey round the outermost places of the loop map
HER_SNAP_M = 30.0       # m: K3 and K4 lie this close to the stream's centre line, else the walk is drawn straight
HER_CORE = ("redhall", "K3", "K4")             # + Ulucami: the loop core of the inset ("survey")
HER_PT = dict(list=9.0, lab=7.5, dot=7.0)     # booklet pt: stop texts (body minimum), stop names, heritage places
HER_PITCH, HER_LEAD = 1.75, 1.4               # line pitch of the stop texts / of a map name, x the capital height
HER_ACC = C(dict((k_, h_) for k_, n_, h_ in R28_MARKERS)["heritage"])     # R28 "heritage and views" (= MARK_C)
HER_ROAD = mix(MPL["road"], WHITE, 0.4)       # G6: street surfaces and edges lighter than b_base's (context only)
HER_ROAD_EDGE = mix(MPL["road_edge"], WHITE, 0.45)
HER_GREEN_T = 0.45                            # mapped parks, woods and fields this far to white; no satellite cover

# The loop in its order (P20.2): key, name (English · Turkish, G3), survey m, one short text (P20.3; ** = bold, G5).
# Places: bridges BRIDGES_K; survey labels Kızıl Avlu, Ulu Camii, Hamam, Çizmeciler Arastası (REF_LABELS); lat/lon of
# OpenStreetMap / Visit İzmir -> survey m by the linear fit anchored at K3 (±10-30 m), as v44. Facts: HER_SRC.
HER_STOPS = [
    dict(key="gondola", name=landmark_name("teleferik"), xy=(30720.4, 32370.1),          # OSM node 2295928011
         txt=u"valley station of the **cable car** (2010) up to **" + landmark_name("akropol") + u"**, the Hellenistic "
             u"city on the hill"),          # v59 (round 4, G-R4-11): Turkish names from the table, no translations
    dict(key="redhall", name=landmark_name("kizil_avlu"), xy=(30203.92, 31974.82),      # survey label 'Kızıl Avlu'
         txt=u"Hadrian's **temple**, 2nd c. AD, built **over the stream**: the Selinos runs under it in twin Roman "
             u"tunnels"),
    dict(key="K3", name=bridge_name("K3"), xy=(30037.01, 32121.57),   # BRIDGES_K; v58 (round 3, P20.3 / G16): real name
         txt=u"**Roman bridge** of the 2nd-3rd c., named after the old tanneries; the **stream walk** starts here"),
    dict(key="K4", name=bridge_name("K4"), xy=(29846.40, 32277.71),   # BRIDGES_K; v58 (round 3, P20.3 / G16): real name
         txt=u"the bridge before **" + landmark_name("ulucami") + u"** (1398-99, Bayezid I) and **"
             + landmark_name("tabaklar_hamami") + u"**, the tanners' bath; the loop crosses here"),   # v59 (G-R4-11)
    dict(key="bazaar", name=landmark_name("arasta"), xy=(29926.0, 31855.0),        # Hacı Hekim hamam (Visit İzmir)
         txt=u"Hacı Hekim mosque, **arasta** and hamam of 1513, in the old **bazaar** with Çizmeciler Arastası"),
    dict(key="museum", name=landmark_name("bergama_muzesi"), xy=(29560.0, 31358.0),   # as v44; v59 (G-R4-11)
         txt=u"museum of **1936**: finds from the **excavations** of Pergamon, and the town's carpets"),
    dict(key="asklepieion", name=landmark_name("asklepion"), xy=(29077.3, 31867.3),  # OSM ticket building; v59
         txt=u"the **healing sanctuary** of Asclepius, 4th c. BC, rebuilt under Hadrian, reached by a sacred way, "
             u"the Via Tecta"),
]
# v58 (round 3, P20.3 / G16): the walk's printed name and text by bridge_name (no K-codes; keys frm / to stay codes)
HER_WALK = dict(frm="K3", to="K4", name=u"Stream walk " + bridge_name("K3") + u" – " + bridge_name("K4"),
                txt=u"**{:,.0f} m** along the **Selinos** (Bergama Çayı) from the **Roman bridge** " + bridge_name("K3")
                    + u" to " + bridge_name("K4") + u": the spine of the loop")   # v50: K4's date unsure (h01 §5 P06)
HER_BEYOND = [dict(key="acropolis", frm="gondola", name=landmark_name("akropol"),  # Trajaneum, OSM way 1410335587;
                   xy=(30209.0, 33177.0))]                                         # off the survey drawing (259 m)
# v59 (round 4, G-R4-11): the names from the table (p21_heritage.py's HER21_PLACES "dot" keys read the same calls)
HER_DOTS = [(landmark_name("ulucami"), (29844.17, 32313.30)),          # survey label 'Ulu Camii'
            (landmark_name("tabaklar_hamami"), (29890.4, 32243.6)),      # survey 'Hamam'
            (landmark_name("cizmeciler_arastasi"), (29794.31, 31929.85))]   # survey label
HER_SRC = (u"Heritage loop, the places and their dates (public sources): Wikipedia 'Pergamon' (Acropolis, Trajaneum, "
           u"Asklepieion, Via Tecta) and 'Bergama Acropolis Gondola'; UNESCO World Heritage List 1457 and its ICOMOS "
           u"evaluation (2014, whc.unesco.org/document/152724: the Roman tunnels under Kızıl Avlu); Wikipedia 'Red "
           u"Basilica'; Kültür Envanteri (kulturenvanteri.com) 'Kızıl Avlu', 'Tabak Köprüsü', 'Bergama Müzesi'; Visit "
           u"İzmir (visitizmir.org) 'Bergama Ulu (Yıldırım) Mosque' and 'Mevlâna Hacı Hekim Hammam'; KTB İzmir 'Baths "
           u"(Hamams) in İzmir' (Tabaklar Hamamı, named after the tanneries); KTB Türkiye Müzeleri (turkishmuseums.com) "
           u"'The Archaeological Site of Asklepion'; Wikipedia 'Bergama Museum'; OpenStreetMap (ODbL).")   # v51: public only (D13)

# v59 (round 4, G-R4-1): the Arial width tables HER_MCH / HER_MW0 / HER_MW1 / HER_W are gone: her_tw (pages/
# p21_heritage.py) measures with the real font (tw, common/font_metrics.py), as the page check does.


class HerBox(object):
    """v50 (P20.1): a north-up map rectangle in survey m, used as a Frame by View and draw_north_at (u = east, v =
    north whatever its proportions: a Frame turns its longest side to u, so a tall box would come out on its side)"""

    def __init__(self, x0, y0, x1, y1):
        self.x0, self.y0, self.x1, self.y1 = min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)
        self.cx, self.cy = 0.5 * (self.x0 + self.x1), 0.5 * (self.y0 + self.y1)
        self.w, self.h = self.x1 - self.x0, self.y1 - self.y0
        self.u0, self.u1, self.v0, self.v1 = -0.5 * self.w, 0.5 * self.w, -0.5 * self.h, 0.5 * self.h
        self.ang, self.area = 0.0, self.w * self.h
        self.P = [(self.x0, self.y0), (self.x1, self.y0), (self.x1, self.y1), (self.x0, self.y1)]
        self.bb = (self.x0, self.y0, self.x1, self.y1)

    def local(self, x, y):
        return (x - self.cx, y - self.cy)

    def world(self, u, v):
        return (self.cx + u, self.cy + v)

    def inside(self, x, y):
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1


