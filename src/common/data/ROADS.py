# ---- ROADS.py (round 4, S8, 1 Nov 2026; CHK1_2 F1, P09.1): the masterplan's road moves, ONE table --------------------
# Moved from bergama_masterplan/parts/02c_corridor.py (v37.4) unchanged. Included by the masterplan (code.py) and the
# site board (S4), so the site board's street sections (p09) read the same table with no run-order dependency.
# Needs common/data/NAMES.py + common/names.py included before it (bridge_name). Each road: name, change (kept /
# calmed / pedestrian / shared), note, proof (its data source), xy (survey m polyline). TOWN_LINE: the later town
# bus line to the K4 hub. Readers: masterplan Corridor.make_notes / no_go / movement, p21, p22; site board p09.
# Roads (OSM bergama_osm.osm, 28 Jul 2026, highway class and name; survey m by the h01 §0 formula, +-10-30 m). Each
# change is read from data: the OSM class (site board p6 driving map), the site board mark C3 "K4: monument and
# traffic" (p5), and the OSM chainages of the car crossings along the stream (calculated). No traffic count exists
# on these streets (card t01: KGM counts only on 35-04, 35-05, D240): no "relocated" road.
ROADS = [
    dict(name=u"Bergama - Kozak Yolu", change="kept", note=u"kept: through road to Kozak",
         proof=u"OSM secondary (one 11.9 km way)",
         xy=[[29668.6, 32896.0], [29643.3, 32796.0], [29633.4, 32739.9], [29627.0, 32698.6], [29625.9, 32675.0],
             [29627.8, 32656.7], [29636.9, 32624.0], [29648.9, 32599.2], [29667.9, 32549.9], [29687.1, 32517.5],
             [29726.2, 32490.9], [29760.3, 32463.9], [29772.4, 32442.5], [29775.9, 32394.5], [29772.1, 32343.5],
             [29773.3, 32313.3], [29777.8, 32297.2], [29792.2, 32271.3]]),
    dict(name=u"Cami Kebir Caddesi + " + bridge_name("K4"), change="calmed",
         note=u"calmed: monument meets traffic at " + bridge_name("K4"),
         proof=u"edge plan mark C3; OSM secondary",
         xy=[[29854.5, 32289.9], [29843.7, 32252.8], [29873.2, 32232.0], [29934.1, 32225.0], [29960.0, 32218.3],
             [29976.9, 32203.2], [30015.5, 32111.3]]),
    dict(name=u"Tabak Köprüsü", change="calmed", note=u"calmed: hub square and workshops at " + bridge_name("K3"),
         proof=u"H1, H3 (h01/h02); OSM secondary", xy=[[30023.7, 32110.3], [30052.5, 32130.6]]),
    dict(name=u"Kınık Caddesi", change="kept", note=u"kept: main spine, shops",
         proof=u"city link main spine; OSM secondary",
         xy=[[29992.8, 32017.4], [30005.0, 32029.4], [30032.5, 32038.3], [30089.7, 32057.7], [30138.7, 32039.0]]),
    dict(name=u"Kızıl Avlu Çıkmazı", change="pedestrian", note=u"pedestrian: dead end over hidden stream",
         proof=u"OSM living_street, dead end; H2",
         xy=[[30144.3, 31986.1], [30123.6, 31988.0], [30099.4, 31997.7]]),
    dict(name=u"Üç Kemer Köprüsü", change="pedestrian", note=u"pedestrian: car crossings 190-230 m away",
         proof=u"OSM residential; OSM chainage of Kızıl Avlu Cd / next bridge (calc); H1",
         xy=[[30277.2, 31777.9], [30314.7, 31804.7]]),
    dict(name=u"Adnan Menderes Bulvarı", change="kept", note=u"kept: regional road İzmir-Soma at the " + bridge_name("K6"),
         proof=u"OSM primary; h02 E12", xy=[[30609.3, 31239.0], [30695.5, 31266.2]]),
    dict(name=u"bank street, lower reach", change="shared", note=u"shared: local bank street, stream widens",
         proof=u"OSM residential; open ground",
         xy=[[30713.4, 31260.3], [30730.6, 31243.9], [30800.4, 31198.6], [30862.6, 31166.0], [30923.9, 31135.4],
             [30975.8, 31095.9], [31012.3, 31057.8], [31062.1, 30994.1], [31143.6, 30884.2], [31192.5, 30817.8],
             [31216.8, 30791.6]])]
# Aras 12:05: a town-line extension to K4 as a PROPOSED LATER STEP, on the existing streets İstiklal stop -> Kınık Cd
# -> Cami Kebir Cd -> K4 stop (OSM ways 370936581, 1222988932, 371130159, as above)
TOWN_LINE = dict(name=u"town bus line to " + bridge_name("K4"), change=u"proposed later: bus line 651 to " +
                 bridge_name("K4"), note=u"later step: town line on to " + bridge_name("K4"), proof=u"h03 Q1 (town lines stop at İstiklal); K4 stop 35 m",
                 xy=[[29995.4, 32019.8], [30005.0, 32029.4], [30032.5, 32038.3], [30084.6, 32056.0], [30089.7, 32057.7],
                     [30075.0, 32066.0], [30041.0, 32089.8], [30017.4, 32106.8], [30015.5, 32111.3], [29976.9, 32203.2],
                     [29960.0, 32218.3], [29934.1, 32225.0], [29873.2, 32232.0], [29841.0, 32243.7]])
