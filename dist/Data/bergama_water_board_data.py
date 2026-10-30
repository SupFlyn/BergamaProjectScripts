# Built-in data of bergama_water_board (made by tools/build.py from src/bergama_water_board/data/; do not edit by hand)

#@@ LEVELS
# ---- Level table for every section cut (H-levels 29 Oct 2026; WO-T2a-2) -----------------------------------------------
# From revision_2026-10-29/T1/levels/levels.json (RESULT.md), with Aras's decision D4 b (29 Oct) applied (below).
# Read it through ../common/levels.py, never directly: include this file first, then levels.py:
#   #@include ../common/data/LEVELS.py
#   #@include ../common/levels.py
# Plain Python data (exec'd into globals by tools/build.py's bergama_data): no imports, no functions, one assignment.
#
# ROWS: one dict per cut crossing, in table order. A cut that crosses the stream once has one row, id = the cut
# ("S1", "W1"); S5 and S6 run along the stream and cross it three times: rows "S5-1".."S5-3", "S6-1".."S6-3"
# (crossing 1, 2, 3 = ①②③ on p05, in levels.json order), each repeating the cut-wide fields (pages, ends, length_m, along).
#   id            row id ("S4", "S5-2", "W3")          cut       the cut ("S5"); json_id   the id in levels.json
#   crossing      1, 2, 3 on S5/S6, else None          name      short name (internal, for messages)
#   pages         booklet pages that draw the cut (strings, as levels.json gives them)
#   ends          value = ((x1, y1), (x2, y2)) survey m, unprimed end first; labels = (label1, label2) ("S1", "S1'";
#                 "SW", "NE" on the W cuts)
#   length_m      cut length (m)       chainage_m   m along the research stream centreline   angle_deg   to the stream
#   walled        True in the walled town reach (DSİ walls, chainage 5,290-6,560)
#   bed           bed level (m a.s.l.)     bed_tin   S3/S6-2/S6-3 only: TIN across the no-bed gap, NOT a bed
#   bed_width_cm  bed width (cm)           bed_width_tin_cm   TIN floor width where the DSİ 20.00 m is used (cm)
#   NE, SW        bank dicts (NE = left bank looking downstream, SW = right bank):
#                   type        "dsi_wall" | "embankment" | "loose_earth" | "no_crest" (ground keeps rising, top None)
#                   top         bank top or DSİ wall top (m a.s.l.; None for no_crest)
#                   height      top above the bed (m)
#                   survey_top  walls only: the survey bank before the walls (m a.s.l.; may be None)
#                   angle_deg   embankments only: slope angle (deg; TIN angles are lower bounds)
#   terraces      list of {side, from_m, to_m, level}: level shelves on the TIN, from_m/to_m = m out across the stream
#   q100, q500    flood water levels (m a.s.l., absolute)
#   avg_flow      (H-B 30 Oct, M8 cut registry) water level at the mean yearly flow (m a.s.l.) = bed + avg_flow_depth:
#                 the level every section draws its water at (G8, never a dry bed). "c" on the six surveyed sections
#                 of research/rain_river_levels (W1-W5, S4), "i" (chainage-interpolated between them) elsewhere
#   avg_flow_depth  depth of that water above the bed (m)
#   location      short text: name, stream chainage, walled / unwalled reach (internal, for messages and registry)
#   booklet_pages booklet page numbers (revision 30 Oct) that draw the cut; "pages" keeps the old sheet numbers
#   aliases       other names of the same line, accepted by level_cut() and never printed (W1 = F1, S4 = F3: PLAN T1)
#   along         S5/S6 only: stretches where the cut runs within 20 m of the stream axis: {from_m, to_m (m along the
#                 cut), chainage_from_m, chainage_to_m, ground = (min, max) m a.s.l., not a bed}
#   note          internal note or None (never printed)
#
# VALUES: every number is a dict {"value": v, "status": s, "source": text} and, only when the source is publicly
# available, "public": the citation to print. Plain numbers are positions only (from_m, to_m, chainage_*_m in along).
#   status  "s" surveyed | "i" interpolated | "a" assumed (a project decision) | "c" calculated  (levels.json's words,
#           shortened). Internal tracking only: no status is ever printed on a page (Aras).
#   source  levels.json's source text as given: internal (survey file, scripts, decisions), never printed.
#   public  absent = not public, nothing printed (Aras 29 Oct: "if something is not publicly available dont give a
#           source to it. Dont write calculated or assumed"). Add it only for a published document (DSİ, SYGM, ...).
# Units: levels and heights m with 2 decimals, widths cm (whole), angles deg with 1 decimal, plan coordinates survey m.
# Line status (ends, length_m): "i" = digitised from the p04/p05 key maps (+-3 m), "s" = S4's exact board line,
# "c" = W1-W5 right-angle cuts computed at their chainage.
#
# D4 b (Aras 29 Oct): the S4 bed is +42.48 everywhere (the site board's value; the survey's low point +43.58 / table
# +43.59 is kept only in S4's note). The site board's bed rule also stays for S1 (+67.80), S7 (+58.06), S8 (+55.13)
# (RESULT.md s.3, "Page" column). Changed for these four (status "a"): the bed; the DSİ wall tops of the walled cuts
# S1, S7 (= bed + 5.00); the bank heights of the unwalled S4, S8 (= table top - bed). Q100/Q500 and the terraces
# are absolute levels and stay as in the table.
#
# HOW TO ADD A ROW (a page thread's new cut, measured with T1/levels/work/sample_cut.py X1 Y1 X2 Y2 --name ...):
#   copy a row of the same kind (a cut row like "S8", or a walled one like "S7"), give it a new unique id and fill
#   every field from the sampler's output: one row per stream crossing ("<id>-1", "<id>-2" when it crosses more than
#   once). Keep the value-dict shape with status and source for every number; leave a field out when the sampler gives
#   nothing (levels.py then returns None). In the walled reach the wall top is bed + 5.00 (status "a"). Add rows here
#   only: levels.py needs no change, and the order here is the order level_ids() returns.

LEVELS = [
    # ---- S1: Cut S1
    {
        'id': 'S1',
        'cut': 'S1',
        'json_id': 'S1',
        'crossing': None,
        'name': 'Cut S1',
        'location': 'Cut S1, stream chainage 5,555 m, walled town reach (DSİ walls)',
        'booklet_pages': ['4'],
        'aliases': [],
        'pages': ['04'],
        'ends': {'value': ((29552.11, 32345.6), (29945.02, 32700.41)), 'labels': ('S1', "S1'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 529.4, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 5555.4, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 86.9, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': True,
        'bed': {'value': 67.8, 'status': 'a', 'source': "D4 b (29 Oct): Aras's decision, bed = the site board v50 page value (p04)"},
        'bed_width_cm': {'value': 1710, 'status': 's', 'source': "between the survey's two stream lines HIDRO_DERE_SULU either side of the stream axis, across the stream"},
        'NE': {
            'type': 'dsi_wall',
            'top': {'value': 72.8, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the D4 b bed (D4 b 29 Oct; Aras 28 Oct 14:12)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 78.78, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, res_bank_top crest, 47.9 m out across the stream; nearest survey height 5.9 m away'},
        },
        'SW': {
            'type': 'dsi_wall',
            'top': {'value': 72.8, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the D4 b bed (D4 b 29 Oct; Aras 28 Oct 14:12)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 74.6, 'status': 's', 'source': 'survey, before the DSİ walls: survey TIN, top of the first steep rise (no level ground behind it), 29.0 m out across the stream; nearest survey height 2.4 m away'},
        },
        'terraces': [],
        'q100': {'value': 72.05, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 72.51, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.30, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'avg_flow': {'value': 68.10, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'note': 'D4 b (29 Oct): bed +67.80 (site board v50 page value) instead of levels.json +68.57 s.',
    },
    # ---- S2: Cut S2
    {
        'id': 'S2',
        'cut': 'S2',
        'json_id': 'S2',
        'crossing': None,
        'name': 'Cut S2',
        'location': 'Cut S2, stream chainage 7,485 m, unwalled reach',
        'booklet_pages': ['4'],
        'aliases': [],
        'pages': ['04'],
        'ends': {'value': ((30691.3, 30992.51), (31123.78, 31300.33)), 'labels': ('S2', "S2'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 530.8, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 7485.1, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 66.2, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 47.3, 'status': 's', 'source': 'survey TIN low point; 10 real heights in the bed band, nearest 4.6 m (z 50.82)'},
        'bed_width_cm': {'value': 4190, 'status': 's', 'source': "between the survey's two stream lines HIDRO_DERE_SULU either side of the stream axis, across the stream"},
        'NE': {
            'type': 'loose_earth',
            'top': {'value': 49.68, 'status': 's', 'source': 'survey TIN, res_bank_top crest, 3.7 m out across the stream; nearest survey height 2.0 m away'},
            'height': {'value': 2.38, 'status': 's', 'source': 'bank top minus bed'},
        },
        'SW': {
            'type': 'loose_earth',
            'top': {'value': 49.74, 'status': 's', 'source': 'survey TIN, survey bank-top line SEV_UST (its own height), 43.4 m out across the stream; nearest survey height 3.1 m away'},
            'height': {'value': 2.44, 'status': 's', 'source': 'bank top minus bed'},
        },
        'terraces': [],
        'q100': {'value': 49.55, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 49.78, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.19, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K5 (0.17 m) and NİL (0.19 m)'},
        'avg_flow': {'value': 47.49, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K5 (0.17 m) and NİL (0.19 m)'},
        'note': None,
    },
    # ---- S3: Cut S3
    {
        'id': 'S3',
        'cut': 'S3',
        'json_id': 'S3',
        'crossing': None,
        'name': 'Cut S3',
        'location': 'Cut S3, stream chainage 5,822 m, walled town reach (DSİ walls)',
        'booklet_pages': ['4'],
        'aliases': [],
        'pages': ['04'],
        'ends': {'value': ((29747.61, 32113.39), (29979.55, 32659.4)), 'labels': ('S3', "S3'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 593.2, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 5821.6, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 77.3, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': True,
        'bed': {'value': 66.84, 'status': 'i', 'source': 'bed not surveyed (no channel heights at 5790-5940): linear along the stream between the surveyed beds +68.05 (ch 5738) and +64.77 (ch 5965); +-1.0 m (UNVERIFIED)'},
        'bed_tin': {'value': 67.88, 'status': 'i', 'source': 'survey TIN across the gap (no real height within 56 m): NOT a bed'},
        'bed_width_cm': {'value': 2000, 'status': 'a', 'source': 'DSİ walled channel, bed width 20.00 m (SYGM 2019 Kuzey Ege TYP Yönetici Özeti PDF p.75, measure 155; bank-depth REPORT s.1); the survey has no stream-line pair here (TIN floor width kept as bed_width_tin)', 'public': 'SYGM 2019 Kuzey Ege TYP Yönetici Özeti, p.75'},
        'bed_width_tin_cm': {'value': 250, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'dsi_wall',
            'top': {'value': 71.84, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 79.7, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, top of the first steep rise (no level ground behind it), 48.8 m out across the stream; nearest survey height 70.1 m away'},
        },
        'SW': {
            'type': 'dsi_wall',
            'top': {'value': 71.84, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 69.34, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, res_bank_top crest, 10.7 m out across the stream; nearest survey height 56.7 m away'},
        },
        'terraces': [],
        'q100': {'value': 69.9, 'status': 'i', 'source': 'interpolated bed + mean Q100 depth of the two anchor cuts (3.55, 2.56 m)'},
        'q500': {'value': 70.19, 'status': 'i', 'source': 'interpolated bed + mean Q500 depth of the two anchor cuts (3.85, 2.84 m)'},
        'avg_flow_depth': {'value': 0.20, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'avg_flow': {'value': 67.04, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'note': None,
    },
    # ---- S4: Cut S4
    {
        'id': 'S4',
        'cut': 'S4',
        'json_id': 'S4',
        'crossing': None,
        'name': 'Cut S4',
        'location': 'Cut S4, stream chainage 7,818 m, unwalled reach',
        'booklet_pages': ['4', '13', '14', '17'],
        'aliases': ['F3'],
        'pages': ['04', '14', '15', '17 (band section)'],
        'ends': {'value': ((30901.21, 30743.18), (31333.72, 31050.96)), 'labels': ('S4', "S4'"), 'status': 's', 'source': 'exact: site board v50 S4_WB = water board DETAIL_SRC S4_A -> S4_B (SECTION_LINES_LK[3], Nilnoktali-BERGAMA_layerekli.3dm sec_lines), trimmed to site_alan (starts 349.6 m along the 1,071.7 m water-board line)'},
        'length_m': {'value': 530.8, 'status': 's', 'source': 'exact: site board v50 S4_WB = water board DETAIL_SRC S4_A -> S4_B (SECTION_LINES_LK[3], Nilnoktali-BERGAMA_layerekli.3dm sec_lines), trimmed to site_alan (starts 349.6 m along the 1,071.7 m water-board line)'},
        'chainage_m': {'value': 7817.6, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 89.4, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 42.48, 'status': 'a', 'source': "D4 b (29 Oct): Aras's decision, bed = the site board v50 page value (p04)"},
        'bed_width_cm': {'value': 2600, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'loose_earth',
            'top': {'value': 45.64, 'status': 'i', 'source': 'survey TIN, res_bank_top crest, 31.0 m out across the stream; nearest survey height 5.9 m away'},
            'height': {'value': 3.16, 'status': 'a', 'source': 'bank top minus the D4 b bed (D4 b 29 Oct)'},
        },
        'SW': {
            'type': 'embankment',
            'top': {'value': 47.35, 'status': 's', 'source': 'survey TIN, survey bank-top line SEV_UST (no height on the line: TIN there), 30.3 m out across the stream; nearest survey height 0.9 m away'},
            'height': {'value': 4.87, 'status': 'a', 'source': 'bank top minus the D4 b bed (D4 b 29 Oct)'},
            'angle_deg': {'value': 7.0, 'status': 'i', 'source': "between the survey's slope lines SEV_ALT (toe) and SEV_UST (top) on the cut"},
        },
        'terraces': [
            {'side': 'NE', 'from_m': 1.0, 'to_m': 28.0, 'level': {'value': 44.17, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 0.58 m above the bed'}},
            {'side': 'SW', 'from_m': 33.0, 'to_m': 40.0, 'level': {'value': 47.15, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 3.56 m above the bed'}},
        ],
        'q100': {'value': 45.84, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 46.19, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.24, 'status': 'c', 'source': "research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section S4 detail cut (chainage 7,818 m); depth added to the D4 b bed +42.48 (the research section's bed is +43.59)"},
        'avg_flow': {'value': 42.72, 'status': 'c', 'source': "bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section S4 detail cut (chainage 7,818 m); depth added to the D4 b bed +42.48 (the research section's bed is +43.59)"},
        'note': 'D4 b (29 Oct): bed +42.48 everywhere. Survey low point +43.58 (levels.json +43.59 s, a tacheometric point 0.3 m away) kept here only as a note, never printed.',
    },
    # ---- S5-1: Cut S5 crossing 1
    {
        'id': 'S5-1',
        'cut': 'S5',
        'json_id': 'S5',
        'crossing': 1,
        'name': 'Cut S5 crossing 1',
        'location': 'Cut S5 crossing 1, stream chainage 7,507 m, unwalled reach',
        'booklet_pages': ['5'],
        'aliases': [],
        'pages': ['05'],
        'ends': {'value': ((31427.59, 30538.66), (30654.07, 31377.08)), 'labels': ('S5', "S5'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 1140.7, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 7506.8, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 16.5, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 47.2, 'status': 's', 'source': 'survey TIN low point; 6 real heights in the bed band, nearest 14.6 m (z 47.26)'},
        'bed_width_cm': {'value': 4790, 'status': 's', 'source': "between the survey's two stream lines HIDRO_DERE_SULU either side of the stream axis, across the stream"},
        'NE': {
            'type': 'loose_earth',
            'top': {'value': 50.51, 'status': 's', 'source': 'survey TIN, res_bank_top crest, 28.0 m out across the stream; nearest survey height 5.0 m away'},
            'height': {'value': 3.31, 'status': 's', 'source': 'bank top minus bed'},
        },
        'SW': {
            'type': 'embankment',
            'top': {'value': 49.98, 'status': 's', 'source': 'survey TIN, survey bank-top line SEV_UST (no height on the line: TIN there), 43.0 m out across the stream; nearest survey height 3.2 m away'},
            'height': {'value': 2.78, 'status': 's', 'source': 'bank top minus bed'},
            'angle_deg': {'value': 15.3, 'status': 'i', 'source': "between the survey's slope lines SEV_ALT (toe) and SEV_UST (top) on the cut"},
        },
        'terraces': [],
        'q100': {'value': 48.99, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 49.22, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.19, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K5 (0.17 m) and NİL (0.19 m)'},
        'avg_flow': {'value': 47.39, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K5 (0.17 m) and NİL (0.19 m)'},
        'along': [
            {'from_m': 132.0, 'to_m': 230.0, 'chainage_from_m': 8176.6, 'chainage_to_m': 8086.7, 'ground': {'value': (39.62, 41.65), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
            {'from_m': 390.0, 'to_m': 852.0, 'chainage_from_m': 7896.6, 'chainage_to_m': 7440.8, 'ground': {'value': (43.43, 49.9), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
        ],
        'note': 'The cut runs along the stream, not across it: the bed changes along it. Values are given at each place it crosses the stream axis (read on a right-angle section there) and as ground ranges where it runs within 20 m of the axis.',
    },
    # ---- S5-2: Cut S5 crossing 2
    {
        'id': 'S5-2',
        'cut': 'S5',
        'json_id': 'S5',
        'crossing': 2,
        'name': 'Cut S5 crossing 2',
        'location': 'Cut S5 crossing 2, stream chainage 7,842 m, unwalled reach',
        'booklet_pages': ['5'],
        'aliases': [],
        'pages': ['05'],
        'ends': {'value': ((31427.59, 30538.66), (30654.07, 31377.08)), 'labels': ('S5', "S5'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 1140.7, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 7841.9, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 7.9, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 42.75, 'status': 's', 'source': 'survey TIN low point; 5 real heights in the bed band, nearest 3.7 m (z 42.57)'},
        'bed_width_cm': {'value': 1100, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'loose_earth',
            'top': {'value': 47.34, 'status': 's', 'source': 'survey TIN, res_bank_top crest, 50.0 m out across the stream; nearest survey height 1.8 m away'},
            'height': {'value': 4.59, 'status': 's', 'source': 'bank top minus bed'},
        },
        'SW': {
            'type': 'embankment',
            'top': {'value': 46.94, 'status': 's', 'source': 'survey TIN, survey bank-top line SEV_UST (no height on the line: TIN there), 17.7 m out across the stream; nearest survey height 1.1 m away'},
            'height': {'value': 4.19, 'status': 's', 'source': 'bank top minus bed'},
            'angle_deg': {'value': 7.0, 'status': 'i', 'source': "between the survey's slope lines SEV_ALT (toe) and SEV_UST (top) on the cut"},
        },
        'terraces': [
            {'side': 'NE', 'from_m': 18.0, 'to_m': 43.0, 'level': {'value': 44.14, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 1.38 m above the bed'}},
            {'side': 'SW', 'from_m': 19.0, 'to_m': 40.0, 'level': {'value': 46.67, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 3.92 m above the bed'}},
        ],
        'q100': {'value': 45.39, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 45.65, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.23, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections S4 detail cut (0.24 m) and NİL flat end (0.12 m)'},
        'avg_flow': {'value': 42.98, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections S4 detail cut (0.24 m) and NİL flat end (0.12 m)'},
        'along': [
            {'from_m': 132.0, 'to_m': 230.0, 'chainage_from_m': 8176.6, 'chainage_to_m': 8086.7, 'ground': {'value': (39.62, 41.65), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
            {'from_m': 390.0, 'to_m': 852.0, 'chainage_from_m': 7896.6, 'chainage_to_m': 7440.8, 'ground': {'value': (43.43, 49.9), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
        ],
        'note': 'The cut runs along the stream, not across it: the bed changes along it. Values are given at each place it crosses the stream axis (read on a right-angle section there) and as ground ranges where it runs within 20 m of the axis.',
    },
    # ---- S5-3: Cut S5 crossing 3
    {
        'id': 'S5-3',
        'cut': 'S5',
        'json_id': 'S5',
        'crossing': 3,
        'name': 'Cut S5 crossing 3',
        'location': 'Cut S5 crossing 3, stream chainage 8,136 m, unwalled reach',
        'booklet_pages': ['5'],
        'aliases': [],
        'pages': ['05'],
        'ends': {'value': ((31427.59, 30538.66), (30654.07, 31377.08)), 'labels': ('S5', "S5'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 1140.7, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 8136.3, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 25.7, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 40.36, 'status': 's', 'source': 'survey TIN low point; 6 real heights in the bed band, nearest 7.5 m (z 40.41)'},
        'bed_width_cm': {'value': 4500, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'loose_earth',
            'top': {'value': 42.88, 'status': 's', 'source': 'survey TIN, first local high > 0.8 m above the bed (levels2), 46.0 m out across the stream; nearest survey height 1.2 m away'},
            'height': {'value': 2.52, 'status': 's', 'source': 'bank top minus bed'},
        },
        'SW': {
            'type': 'no_crest',
            'top': {'value': None, 'status': 'i', 'source': 'no bank crest within 60 m: the ground keeps rising (valley side / hillside)'},
            'height': {'value': None, 'status': 'i', 'source': 'bank top minus bed'},
        },
        'terraces': [
            {'side': 'NE', 'from_m': 17.0, 'to_m': 40.0, 'level': {'value': 41.75, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 1.40 m above the bed'}},
            {'side': 'SW', 'from_m': 36.0, 'to_m': 40.0, 'level': {'value': 40.98, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 0.62 m above the bed'}},
        ],
        'q100': {'value': 42.07, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 42.25, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.12, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; beyond the last surveyed section: the depth of NİL flat end (chainage 8,100 m)'},
        'avg_flow': {'value': 40.48, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; beyond the last surveyed section: the depth of NİL flat end (chainage 8,100 m)'},
        'along': [
            {'from_m': 132.0, 'to_m': 230.0, 'chainage_from_m': 8176.6, 'chainage_to_m': 8086.7, 'ground': {'value': (39.62, 41.65), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
            {'from_m': 390.0, 'to_m': 852.0, 'chainage_from_m': 7896.6, 'chainage_to_m': 7440.8, 'ground': {'value': (43.43, 49.9), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
        ],
        'note': 'The cut runs along the stream, not across it: the bed changes along it. Values are given at each place it crosses the stream axis (read on a right-angle section there) and as ground ranges where it runs within 20 m of the axis.',
    },
    # ---- S6-1: Cut S6 crossing 1
    {
        'id': 'S6-1',
        'cut': 'S6',
        'json_id': 'S6',
        'crossing': 1,
        'name': 'Cut S6 crossing 1',
        'location': 'Cut S6 crossing 1, stream chainage 5,741 m, walled town reach (DSİ walls)',
        'booklet_pages': ['5'],
        'aliases': [],
        'pages': ['05'],
        'ends': {'value': ((30629.06, 31428.05), (29742.13, 32386.34)), 'labels': ('S6', "S6'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 1305.7, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 5741.4, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 38.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': True,
        'bed': {'value': 68.08, 'status': 's', 'source': 'survey TIN low point; 6 real heights in the bed band, nearest 3.5 m (z 68.01)'},
        'bed_width_cm': {'value': 2000, 'status': 'a', 'source': 'DSİ walled channel, bed width 20.00 m (SYGM 2019 Kuzey Ege TYP Yönetici Özeti PDF p.75, measure 155; bank-depth REPORT s.1); the survey has no stream-line pair here (TIN floor width kept as bed_width_tin)', 'public': 'SYGM 2019 Kuzey Ege TYP Yönetici Özeti, p.75'},
        'bed_width_tin_cm': {'value': 500, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'dsi_wall',
            'top': {'value': 73.08, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 72.56, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, top of the first steep rise (no level ground behind it), 27.0 m out across the stream; nearest survey height 26.6 m away'},
        },
        'SW': {
            'type': 'dsi_wall',
            'top': {'value': 73.08, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 71.21, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, res_bank_top crest, 17.0 m out across the stream; nearest survey height 5.6 m away'},
        },
        'terraces': [],
        'q100': {'value': 71.61, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 71.91, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.23, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'avg_flow': {'value': 68.31, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'along': [
            {'from_m': 390.0, 'to_m': 854.0, 'chainage_from_m': 6661.3, 'chainage_to_m': 6202.0, 'ground': {'value': (54.68, 65.39), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
            {'from_m': 1124.0, 'to_m': 1282.0, 'chainage_from_m': 5868.6, 'chainage_to_m': 5718.1, 'ground': {'value': (68.03, 72.01), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
        ],
        'note': 'The cut runs along the stream, not across it: the bed changes along it. Values are given at each place it crosses the stream axis (read on a right-angle section there) and as ground ranges where it runs within 20 m of the axis.',
    },
    # ---- S6-2: Cut S6 crossing 2
    {
        'id': 'S6-2',
        'cut': 'S6',
        'json_id': 'S6',
        'crossing': 2,
        'name': 'Cut S6 crossing 2',
        'location': 'Cut S6 crossing 2, stream chainage 5,849 m, walled town reach (DSİ walls)',
        'booklet_pages': ['5'],
        'aliases': [],
        'pages': ['05'],
        'ends': {'value': ((30629.06, 31428.05), (29742.13, 32386.34)), 'labels': ('S6', "S6'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 1305.7, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 5848.6, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 36.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': True,
        'bed': {'value': 66.45, 'status': 'i', 'source': 'bed not surveyed (no channel heights at 5790-5940): linear along the stream between the surveyed beds +68.05 (ch 5738) and +64.77 (ch 5965); +-1.0 m (UNVERIFIED)'},
        'bed_tin': {'value': 66.82, 'status': 'i', 'source': 'survey TIN across the gap (no real height within 74 m): NOT a bed'},
        'bed_width_cm': {'value': 2000, 'status': 'a', 'source': 'DSİ walled channel, bed width 20.00 m (SYGM 2019 Kuzey Ege TYP Yönetici Özeti PDF p.75, measure 155; bank-depth REPORT s.1); the survey has no stream-line pair here (TIN floor width kept as bed_width_tin)', 'public': 'SYGM 2019 Kuzey Ege TYP Yönetici Özeti, p.75'},
        'bed_width_tin_cm': {'value': 250, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'dsi_wall',
            'top': {'value': 71.45, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 81.47, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, res_bank_top crest, 59.0 m out across the stream; nearest survey height 59.5 m away'},
        },
        'SW': {
            'type': 'dsi_wall',
            'top': {'value': 71.45, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 68.64, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, res_bank_top crest, 13.0 m out across the stream; nearest survey height 77.0 m away'},
        },
        'terraces': [],
        'q100': {'value': 69.51, 'status': 'i', 'source': 'interpolated bed + mean Q100 depth of the two anchor cuts (3.55, 2.56 m)'},
        'q500': {'value': 69.8, 'status': 'i', 'source': 'interpolated bed + mean Q500 depth of the two anchor cuts (3.85, 2.84 m)'},
        'avg_flow_depth': {'value': 0.19, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'avg_flow': {'value': 66.64, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'along': [
            {'from_m': 390.0, 'to_m': 854.0, 'chainage_from_m': 6661.3, 'chainage_to_m': 6202.0, 'ground': {'value': (54.68, 65.39), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
            {'from_m': 1124.0, 'to_m': 1282.0, 'chainage_from_m': 5868.6, 'chainage_to_m': 5718.1, 'ground': {'value': (68.03, 72.01), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
        ],
        'note': 'The cut runs along the stream, not across it: the bed changes along it. Values are given at each place it crosses the stream axis (read on a right-angle section there) and as ground ranges where it runs within 20 m of the axis.',
    },
    # ---- S6-3: Cut S6 crossing 3
    {
        'id': 'S6-3',
        'cut': 'S6',
        'json_id': 'S6',
        'crossing': 3,
        'name': 'Cut S6 crossing 3',
        'location': 'Cut S6 crossing 3, stream chainage 6,294 m, walled town reach (DSİ walls)',
        'booklet_pages': ['5'],
        'aliases': [],
        'pages': ['05'],
        'ends': {'value': ((30629.06, 31428.05), (29742.13, 32386.34)), 'labels': ('S6', "S6'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 1305.7, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 6294.2, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 10.1, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': True,
        'bed': {'value': 59.2, 'status': 'i', 'source': 'bed not surveyed (no channel heights at 6065-6390): linear along the stream between the surveyed beds +61.18 (ch 6025) and +58.46 (ch 6395); +-1.0 m (UNVERIFIED)'},
        'bed_tin': {'value': 62.11, 'status': 'i', 'source': 'survey TIN across the gap (no real height within 85 m): NOT a bed'},
        'bed_width_cm': {'value': 2000, 'status': 'a', 'source': 'DSİ walled channel, bed width 20.00 m (SYGM 2019 Kuzey Ege TYP Yönetici Özeti PDF p.75, measure 155; bank-depth REPORT s.1); the survey has no stream-line pair here (TIN floor width kept as bed_width_tin)', 'public': 'SYGM 2019 Kuzey Ege TYP Yönetici Özeti, p.75'},
        'bed_width_tin_cm': {'value': 1700, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'dsi_wall',
            'top': {'value': 64.2, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': None, 'status': 'i', 'source': 'survey, before the DSİ walls: no bank crest within 60 m: the ground keeps rising (valley side / hillside)'},
        },
        'SW': {
            'type': 'dsi_wall',
            'top': {'value': 64.2, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': None, 'status': 'i', 'source': 'survey, before the DSİ walls: no bank crest within 60 m: the ground keeps rising (valley side / hillside)'},
        },
        'terraces': [
            {'side': 'SW', 'from_m': 1.0, 'to_m': 40.0, 'level': {'value': 62.95, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 0.84 m above the bed'}},
        ],
        'q100': {'value': 62.58, 'status': 'i', 'source': 'interpolated bed + mean Q100 depth of the two anchor cuts (3.97, 2.79 m); tunnels not modelled: levels just upstream of them can be higher (README v1.1)'},
        'q500': {'value': 62.92, 'status': 'i', 'source': 'interpolated bed + mean Q500 depth of the two anchor cuts (3.97, 2.79 m); tunnels not modelled: levels just upstream of them can be higher (README v1.1)'},
        'avg_flow_depth': {'value': 0.16, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K4 (0.15 m) and BEGÜM K5 (0.17 m)'},
        'avg_flow': {'value': 59.36, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K4 (0.15 m) and BEGÜM K5 (0.17 m)'},
        'along': [
            {'from_m': 390.0, 'to_m': 854.0, 'chainage_from_m': 6661.3, 'chainage_to_m': 6202.0, 'ground': {'value': (54.68, 65.39), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
            {'from_m': 1124.0, 'to_m': 1282.0, 'chainage_from_m': 5868.6, 'chainage_to_m': 5718.1, 'ground': {'value': (68.03, 72.01), 'status': 'i', 'source': 'survey TIN along the cut where it runs within 20 m of the stream axis (the cut lies in or beside the channel; not a bed level)'}},
        ],
        'note': 'The cut runs along the stream, not across it: the bed changes along it. Values are given at each place it crosses the stream axis (read on a right-angle section there) and as ground ranges where it runs within 20 m of the axis.',
    },
    # ---- S7: Cut S7
    {
        'id': 'S7',
        'cut': 'S7',
        'json_id': 'S7',
        'crossing': None,
        'name': 'Cut S7',
        'location': 'Cut S7, stream chainage 6,415 m, walled town reach (DSİ walls)',
        'booklet_pages': ['5'],
        'aliases': [],
        'pages': ['05'],
        'ends': {'value': ((30031.85, 31775.78), (30458.68, 32090.31)), 'labels': ('S7', "S7'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 530.2, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 6415.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 84.2, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': True,
        'bed': {'value': 58.06, 'status': 'a', 'source': "D4 b (29 Oct): Aras's decision, bed = the site board v50 page value (p05)"},
        'bed_width_cm': {'value': 2000, 'status': 'a', 'source': 'DSİ walled channel, bed width 20.00 m (SYGM 2019 Kuzey Ege TYP Yönetici Özeti PDF p.75, measure 155; bank-depth REPORT s.1); the survey has no stream-line pair here (TIN floor width kept as bed_width_tin)', 'public': 'SYGM 2019 Kuzey Ege TYP Yönetici Özeti, p.75'},
        'bed_width_tin_cm': {'value': 800, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'dsi_wall',
            'top': {'value': 63.06, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the D4 b bed (D4 b 29 Oct; Aras 28 Oct 14:12)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 59.98, 'status': 's', 'source': 'survey, before the DSİ walls: survey TIN, top of the first steep rise (no level ground behind it), 11.9 m out across the stream; nearest survey height 1.6 m away'},
        },
        'SW': {
            'type': 'dsi_wall',
            'top': {'value': 63.06, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the D4 b bed (D4 b 29 Oct; Aras 28 Oct 14:12)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 65.25, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, first local high > 0.8 m above the bed (levels2), 74.6 m out across the stream; nearest survey height 17.0 m away'},
        },
        'terraces': [
            {'side': 'NE', 'from_m': 25.0, 'to_m': 40.0, 'level': {'value': 61.31, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 3.38 m above the bed'}},
        ],
        'q100': {'value': 61.09, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 61.39, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.16, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K4 (0.15 m) and BEGÜM K5 (0.17 m)'},
        'avg_flow': {'value': 58.22, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K4 (0.15 m) and BEGÜM K5 (0.17 m)'},
        'note': 'D4 b (29 Oct): bed +58.06 (site board v50 page value) instead of levels.json +57.93 s.',
    },
    # ---- S8: Cut S8
    {
        'id': 'S8',
        'cut': 'S8',
        'json_id': 'S8',
        'crossing': None,
        'name': 'Cut S8',
        'location': 'Cut S8, stream chainage 6,638 m, unwalled reach',
        'booklet_pages': ['5'],
        'aliases': [],
        'pages': ['05'],
        'ends': {'value': ((30157.18, 31626.92), (30629.14, 31887.84)), 'labels': ('S8', "S8'"), 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'length_m': {'value': 539.3, 'status': 'i', 'source': "digitised from the booklet key maps (revision package booklet/p04.jpg, p05.jpg; frame = site_alan, 2.75 m per pixel, line fit rms 0.8-1.0 px); checked: cut length and both end levels match the page within 0.1 m (S1-S4, S7, S8; S5 length 1,140 m as printed). +-3 m. Replace with the sec_lines coordinates of Aras's working file when available."},
        'chainage_m': {'value': 6638.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 80.8, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 55.13, 'status': 'a', 'source': "D4 b (29 Oct): Aras's decision, bed = the site board v50 page value (p05)"},
        'bed_width_cm': {'value': 1750, 'status': 's', 'source': "between the survey's two stream lines HIDRO_DERE_SULU either side of the stream axis, across the stream"},
        'NE': {
            'type': 'loose_earth',
            'top': {'value': 63.99, 'status': 's', 'source': 'survey TIN, top of the first steep rise (no level ground behind it), 24.7 m out across the stream; nearest survey height 0.1 m away'},
            'height': {'value': 8.86, 'status': 'a', 'source': 'bank top minus the D4 b bed (D4 b 29 Oct)'},
        },
        'SW': {
            'type': 'loose_earth',
            'top': {'value': 58.04, 'status': 's', 'source': 'survey TIN, top of the first steep rise (no level ground behind it), 25.7 m out across the stream; nearest survey height 1.8 m away'},
            'height': {'value': 2.91, 'status': 'a', 'source': 'bank top minus the D4 b bed (D4 b 29 Oct)'},
        },
        'terraces': [
            {'side': 'NE', 'from_m': 28.0, 'to_m': 33.0, 'level': {'value': 64.27, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 8.51 m above the bed'}},
            {'side': 'SW', 'from_m': 1.0, 'to_m': 22.0, 'level': {'value': 56.36, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 0.60 m above the bed'}},
            {'side': 'SW', 'from_m': 29.0, 'to_m': 33.0, 'level': {'value': 58.37, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 2.61 m above the bed'}},
        ],
        'q100': {'value': 58.72, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 59.12, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.17, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K4 (0.15 m) and BEGÜM K5 (0.17 m)'},
        'avg_flow': {'value': 55.30, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K4 (0.15 m) and BEGÜM K5 (0.17 m)'},
        'note': 'D4 b (29 Oct): bed +55.13 (site board v50 page value) instead of levels.json +55.76 s.',
    },
    # ---- W1: Upstream entry
    {
        'id': 'W1',
        'cut': 'W1',
        'json_id': 'W1_upstream_entry',
        'crossing': None,
        'name': 'Upstream entry',
        'location': 'Upstream entry, stream chainage 5,483 m, walled town reach (DSİ walls)',
        'booklet_pages': ['10', '12', '17', '22'],
        'aliases': ['F1'],
        'pages': ['13 (panel 1)', '24 (upstream window: level mark)', '11 (water balance STREAM_CUT)'],
        'ends': {'value': ((29657.106, 32547.404), (29716.111, 32583.173)), 'labels': ('SW', 'NE'), 'status': 'c', 'source': 'right-angle cut at chainage 5483.2, centre (29693.022, 32569.176) from research levels2_out.json; drawn span u -42..27 m (water board CUTS ground)'},
        'length_m': {'value': 69.0, 'status': 'c', 'source': 'right-angle cut at chainage 5483.2, centre (29693.022, 32569.176) from research levels2_out.json; drawn span u -42..27 m (water board CUTS ground)'},
        'chainage_m': {'value': 5483.2, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 90.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': True,
        'bed': {'value': 70.36, 'status': 's', 'source': 'survey TIN low point; 10 real heights in the bed band, nearest 6.2 m (z 70.63)'},
        'bed_width_cm': {'value': 3260, 'status': 's', 'source': "between the survey's two stream lines HIDRO_DERE_SULU either side of the stream axis, across the stream"},
        'NE': {
            'type': 'dsi_wall',
            'top': {'value': 75.36, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 75.52, 'status': 's', 'source': 'survey, before the DSİ walls: survey TIN, res_bank_top crest, 23.0 m out across the stream; nearest survey height 3.9 m away'},
        },
        'SW': {
            'type': 'dsi_wall',
            'top': {'value': 75.36, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 75.25, 'status': 's', 'source': 'survey, before the DSİ walls: survey TIN, top of the first steep rise (no level ground behind it), 41.0 m out across the stream; nearest survey height 0.7 m away'},
        },
        'terraces': [],
        'q100': {'value': 73.35, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 73.66, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.33, 'status': 'c', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section ARAS (chainage 5,483 m)'},
        'avg_flow': {'value': 70.69, 'status': 'c', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section ARAS (chainage 5,483 m)'},
        'note': None,
    },
    # ---- W2: K4 cut
    {
        'id': 'W2',
        'cut': 'W2',
        'json_id': 'W2_K4',
        'crossing': None,
        'name': 'K4 cut',
        'location': 'K4 cut, stream chainage 5,965 m, walled town reach (DSİ walls)',
        'booklet_pages': ['12'],
        'aliases': [],
        'pages': ['13 (panel 2)'],
        'ends': {'value': ((29940.346, 32186.961), (29966.574, 32291.728)), 'labels': ('SW', 'NE'), 'status': 'c', 'source': 'right-angle cut at chainage 5964.9, centre (29959.774, 32264.566) from research levels2_out.json; drawn span u -80..28 m (water board CUTS ground)'},
        'length_m': {'value': 108.0, 'status': 'c', 'source': 'right-angle cut at chainage 5964.9, centre (29959.774, 32264.566) from research levels2_out.json; drawn span u -80..28 m (water board CUTS ground)'},
        'chainage_m': {'value': 5964.9, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 90.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': True,
        'bed': {'value': 64.77, 'status': 's', 'source': 'survey TIN low point; 7 real heights in the bed band, nearest 2.3 m (z 64.71)'},
        'bed_width_cm': {'value': 2000, 'status': 'a', 'source': 'DSİ walled channel, bed width 20.00 m (SYGM 2019 Kuzey Ege TYP Yönetici Özeti PDF p.75, measure 155; bank-depth REPORT s.1); the survey has no stream-line pair here (TIN floor width kept as bed_width_tin)', 'public': 'SYGM 2019 Kuzey Ege TYP Yönetici Özeti, p.75'},
        'bed_width_tin_cm': {'value': 3000, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'dsi_wall',
            'top': {'value': 69.77, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': None, 'status': 'i', 'source': 'survey, before the DSİ walls: no bank crest within 60 m: the ground keeps rising (valley side / hillside)'},
        },
        'SW': {
            'type': 'dsi_wall',
            'top': {'value': 69.77, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12: photos 1 Oct 2026 win over the survey, range 4-6 m; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 66.85, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, res_bank_top crest, 33.0 m out across the stream; nearest survey height 20.0 m away'},
        },
        'terraces': [],
        'q100': {'value': 67.33, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 67.61, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.15, 'status': 'c', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section BEGÜM K4 (chainage 5,965 m)'},
        'avg_flow': {'value': 64.92, 'status': 'c', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section BEGÜM K4 (chainage 5,965 m)'},
        'note': None,
    },
    # ---- W3: K5 cut
    {
        'id': 'W3',
        'cut': 'W3',
        'json_id': 'W3_K5',
        'crossing': None,
        'name': 'K5 cut',
        'location': 'K5 cut, stream chainage 6,679 m, unwalled reach',
        'booklet_pages': ['12', '22'],
        'aliases': [],
        'pages': ['13 (panel 3)', '24 (K5 window: level mark)'],
        'ends': {'value': ((30303.892, 31663.762), (30376.04, 31700.58)), 'labels': ('SW', 'NE'), 'status': 'c', 'source': 'right-angle cut at chainage 6678.9, centre (30354.663, 31689.671) from research levels2_out.json; drawn span u -57..24 m (water board CUTS ground)'},
        'length_m': {'value': 81.0, 'status': 'c', 'source': 'right-angle cut at chainage 6678.9, centre (30354.663, 31689.671) from research levels2_out.json; drawn span u -57..24 m (water board CUTS ground)'},
        'chainage_m': {'value': 6678.9, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 90.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 55.96, 'status': 's', 'source': 'survey TIN low point; 4 real heights in the bed band, nearest 5.7 m (z 55.94)'},
        'bed_width_cm': {'value': 1960, 'status': 's', 'source': "between the survey's two stream lines HIDRO_DERE_SULU either side of the stream axis, across the stream"},
        'NE': {
            'type': 'loose_earth',
            'top': {'value': 64.05, 'status': 's', 'source': 'survey TIN, top of the first steep rise (no level ground behind it), 30.0 m out across the stream; nearest survey height 1.4 m away'},
            'height': {'value': 8.09, 'status': 's', 'source': 'bank top minus bed'},
        },
        'SW': {
            'type': 'no_crest',
            'top': {'value': None, 'status': 'i', 'source': 'no bank crest within 60 m: the ground keeps rising (valley side / hillside)'},
            'height': {'value': None, 'status': 'i', 'source': 'bank top minus bed'},
        },
        'terraces': [
            {'side': 'SW', 'from_m': 24.0, 'to_m': 40.0, 'level': {'value': 58.4, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 2.44 m above the bed'}},
        ],
        'q100': {'value': 58.41, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 58.75, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.17, 'status': 'c', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section BEGÜM K5 (chainage 6,679 m)'},
        'avg_flow': {'value': 56.13, 'status': 'c', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section BEGÜM K5 (chainage 6,679 m)'},
        'note': None,
    },
    # ---- W4: Downstream reach
    {
        'id': 'W4',
        'cut': 'W4',
        'json_id': 'W4_downstream',
        'crossing': None,
        'name': 'Downstream reach',
        'location': 'Downstream reach, stream chainage 7,629 m, unwalled reach',
        'booklet_pages': ['12'],
        'aliases': [],
        'pages': ['13 (panel 4)'],
        'ends': {'value': ((30959.672, 31012.419), (31016.376, 31059.965)), 'labels': ('SW', 'NE'), 'status': 'c', 'source': 'right-angle cut at chainage 7628.6, centre (30991.856, 31039.404) from research levels2_out.json; drawn span u -42..32 m (water board CUTS ground)'},
        'length_m': {'value': 74.0, 'status': 'c', 'source': 'right-angle cut at chainage 7628.6, centre (30991.856, 31039.404) from research levels2_out.json; drawn span u -42..32 m (water board CUTS ground)'},
        'chainage_m': {'value': 7628.6, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 90.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 45.67, 'status': 's', 'source': 'survey TIN low point; 6 real heights in the bed band, nearest 7.6 m (z 45.65)'},
        'bed_width_cm': {'value': 3250, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'embankment',
            'top': {'value': 49.75, 'status': 's', 'source': 'survey TIN, res_bank_top crest, 50.0 m out across the stream; nearest survey height 1.4 m away'},
            'height': {'value': 4.08, 'status': 's', 'source': 'bank top minus bed'},
            'angle_deg': {'value': 8.9, 'status': 's', 'source': "between the survey's slope lines SEV_ALT (toe) and SEV_UST (top) on the cut"},
        },
        'SW': {
            'type': 'embankment',
            'top': {'value': 50.76, 'status': 's', 'source': 'survey TIN, res_bank_top crest, 16.0 m out across the stream; nearest survey height 4.3 m away'},
            'height': {'value': 5.09, 'status': 's', 'source': 'bank top minus bed'},
            'angle_deg': {'value': 18.1, 'status': 'i', 'source': "between the survey's slope lines SEV_ALT (toe) and SEV_UST (top) on the cut"},
        },
        'terraces': [
            {'side': 'NE', 'from_m': 34.0, 'to_m': 41.0, 'level': {'value': 46.72, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 1.05 m above the bed'}},
        ],
        'q100': {'value': 47.72, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 48.0, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.19, 'status': 'c', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section NİL (chainage 7,629 m)'},
        'avg_flow': {'value': 45.86, 'status': 'c', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section NİL (chainage 7,629 m)'},
        'note': None,
    },
    # ---- W5: Flat downstream end
    {
        'id': 'W5',
        'cut': 'W5',
        'json_id': 'W5_flat_end',
        'crossing': None,
        'name': 'Flat downstream end',
        'location': 'Flat downstream end, stream chainage 8,100 m, unwalled reach',
        'booklet_pages': [],
        'aliases': [],
        'pages': ["water board sheet only (CUTS 'flat'); not on the checked pages"],
        'ends': {'value': ((31247.837, 30628.656), (31302.032, 30740.186)), 'labels': ('SW', 'NE'), 'status': 'c', 'source': 'right-angle cut at chainage 8099.8, centre (31274.935, 30684.421) from research levels2_out.json; drawn span u -62..62 m (water board CUTS ground)'},
        'length_m': {'value': 124.0, 'status': 'c', 'source': 'right-angle cut at chainage 8099.8, centre (31274.935, 30684.421) from research levels2_out.json; drawn span u -62..62 m (water board CUTS ground)'},
        'chainage_m': {'value': 8099.8, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 90.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 41.33, 'status': 's', 'source': 'survey TIN low point; 4 real heights in the bed band, nearest 1.2 m (z 41.31)'},
        'bed_width_cm': {'value': 6900, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'no_crest',
            'top': {'value': None, 'status': 'i', 'source': 'no bank crest within 60 m: the ground keeps rising (valley side / hillside)'},
            'height': {'value': None, 'status': 'i', 'source': 'bank top minus bed'},
        },
        'SW': {
            'type': 'embankment',
            'top': {'value': 45.15, 'status': 's', 'source': 'survey TIN, res_bank_top crest, 54.0 m out across the stream; nearest survey height 0.8 m away'},
            'height': {'value': 3.82, 'status': 's', 'source': 'bank top minus bed'},
            'angle_deg': {'value': 32.0, 'status': 'i', 'source': "between the survey's slope lines SEV_ALT (toe) and SEV_UST (top) on the cut"},
        },
        'terraces': [],
        'q100': {'value': 42.71, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 42.87, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.12, 'status': 'c', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section NİL flat end (chainage 8,100 m)'},
        'avg_flow': {'value': 41.45, 'status': 'c', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section NİL flat end (chainage 8,100 m)'},
        'note': None,
    },
    # ==== rows added by T4a (WO-T4a-2, p17 planting sections, 29 Oct). F1 = the W1 line, F3 = the S4 line (no rows of
    # their own). F2 and F4 are new lines, first end = SW. Two extra fields, read through level_cut(cid) only:
    #   ground  {value: [(m along the cut from the first end, m a.s.l.)] every 2 m, status, source}: the surveyed ground
    #   zones   [(code, from_m, to_m)]: the project's water spaces the cut crosses (zone base codes; ARM = reed side arm)
    # ---- F2: Rain terraces (upstream entry) (T4a, p17)
    {
        'id': 'F2',
        'cut': 'F2',
        'json_id': None,
        'crossing': None,
        'name': 'Rain terraces (upstream entry)',
        'location': 'Rain terraces (upstream entry), stream chainage 5,531 m, walled town reach (DSİ walls)',
        'booklet_pages': ['17'],
        'aliases': [],
        'pages': ['17 (planting section)'],
        'ends': {'value': ((29665.43, 32501.89), (29843.63, 32592.69)), 'labels': ('F2', "F2'"), 'status': 'a', 'source': 'T4a WO-T4a-2 (29 Oct): p17 cut line placed by the page thread across the rain terraces (zone base WS), the shaded walk (GR), the reed basins (WT), the spillway (WD) and the stream at the upstream entry; measured with T1/levels/work/sample_cut.py (29665.43, 32501.89) -> (29843.63, 32592.69)'},
        'length_m': {'value': 200.0, 'status': 'a', 'source': 'T4a WO-T4a-2 (29 Oct): p17 cut line placed by the page thread across the rain terraces (zone base WS), the shaded walk (GR), the reed basins (WT), the spillway (WD) and the stream at the upstream entry; measured with T1/levels/work/sample_cut.py (29665.43, 32501.89) -> (29843.63, 32592.69)'},
        'chainage_m': {'value': 5531.2, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 74.4, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': True,
        'bed': {'value': 68.87, 'status': 's', 'source': 'survey TIN low point; 8 real heights in the bed band, nearest 7.8 m (z 68.80)'},
        'bed_width_cm': {'value': 2220, 'status': 's', 'source': "between the survey's two stream lines HIDRO_DERE_SULU either side of the stream axis, across the stream"},
        'NE': {
            'type': 'dsi_wall',
            'top': {'value': 73.87, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 78.89, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, res_bank_top crest, 49.1 m out across the stream; nearest survey height 6.8 m away'},
        },
        'SW': {
            'type': 'dsi_wall',
            'top': {'value': 73.87, 'status': 'a', 'source': 'DSİ stone wall 5.00 m above the bed (Aras 28 Oct 14:12; research/bank_depth_2026-10-28/REPORT.md s.4-5)'},
            'height': {'value': 5.0, 'status': 'a', 'source': 'wall height above the bed'},
            'survey_top': {'value': 75.35, 'status': 'i', 'source': 'survey, before the DSİ walls: survey TIN, top of the first steep rise (no level ground behind it), 39.5 m out across the stream; nearest survey height 5.9 m away'},
        },
        'terraces': [
            {'side': 'NE', 'from_m': 14.0, 'to_m': 24.0, 'level': {'value': 75.31, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 6.44 m above the bed'}},
            {'side': 'NE', 'from_m': 28.0, 'to_m': 34.0, 'level': {'value': 75.90, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 7.03 m above the bed'}},
        ],
        'q100': {'value': 72.05, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 72.41, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.31, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'avg_flow': {'value': 69.18, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections ARAS (0.33 m) and BEGÜM K4 (0.15 m)'},
        'ground': {'value': [(0.0, 80.79), (2.0, 80.1), (4.0, 79.46), (6.0, 78.84), (8.0, 78.25), (10.0, 77.65), (12.0, 77.02), (14.0, 76.56), (16.0, 76.04), (18.0, 75.84), (20.0, 75.67), (22.0, 75.51), (24.0, 75.45), (26.0, 75.45), (28.0, 75.06), (30.0, 74.66), (32.0, 74.27), (34.0, 73.72), (36.0, 73.15), (38.0, 72.57), (40.0, 71.99), (42.0, 71.41), (44.0, 70.83), (46.0, 70.6), (48.0, 70.44), (50.0, 70.27), (52.0, 70.11), (54.0, 69.95), (56.0, 69.78), (58.0, 69.62), (60.0, 69.46), (62.0, 69.3), (64.0, 69.13), (66.0, 68.97), (68.0, 69.01), (70.0, 69.55), (72.0, 70.1), (74.0, 70.64), (76.0, 71.57), (78.0, 73.15), (80.0, 74.81), (82.0, 75.1), (84.0, 75.22), (86.0, 75.33), (88.0, 75.45), (90.0, 75.42), (92.0, 75.56), (94.0, 75.74), (96.0, 75.83), (98.0, 75.9), (100.0, 75.97), (102.0, 76.26), (104.0, 76.69), (106.0, 77.18), (108.0, 77.66), (110.0, 78.11), (112.0, 78.55), (114.0, 78.85), (116.0, 78.87), (118.0, 78.89), (120.0, 78.91), (122.0, 78.92), (124.0, 78.94), (126.0, 78.97), (128.0, 78.99), (130.0, 79.01), (132.0, 79.03), (134.0, 79.05), (136.0, 79.13), (138.0, 79.26), (140.0, 79.38), (142.0, 79.51), (144.0, 79.63), (146.0, 79.76), (148.0, 79.87), (150.0, 79.98), (152.0, 80.71), (154.0, 81.59), (156.0, 82.44), (158.0, 83.32), (160.0, 83.47), (162.0, 83.54), (164.0, 83.65), (166.0, 83.75), (168.0, 83.84), (170.0, 83.94), (172.0, 84.0), (174.0, 84.0), (176.0, 84.38), (178.0, 84.89), (180.0, 85.43), (182.0, 85.96), (184.0, 86.48), (186.0, 87.03), (188.0, 87.46), (190.0, 87.55), (192.0, 87.63), (194.0, 87.71), (196.0, 87.89), (198.0, 88.81), (199.0, 89.22)], 'status': 'i', 'source': 'survey TIN along the cut every 2 m from the first end (m along the cut, m a.s.l.), sample_cut.py profile'},
        'zones': [('STRIP', 49.2, 54.0), ('WD', 54.1, 75.4), ('WT', 77.7, 97.1), ('GR', 115.6, 135.6), ('WS', 135.6, 177.6)],
        'note': 'T4a: crosses the zone base (ZONE_COPY) at m along the cut: STRIP 49.2-54.0, WD 54.1-75.4, WT 77.7-97.1, GR 115.6-135.6, WS 135.6-177.6 (also in zones). The cut runs within 20 m of the stream axis from 42 to 80 m (angle 74 deg).',
    },
    # ---- F4: Reed side arm (lower reach) (T4a, p17)
    {
        'id': 'F4',
        'cut': 'F4',
        'json_id': None,
        'crossing': None,
        'name': 'Reed side arm (lower reach)',
        'location': 'Reed side arm (lower reach), stream chainage 7,440 m, unwalled reach',
        'booklet_pages': ['17'],
        'aliases': [],
        'pages': ['17 (planting section)'],
        'ends': {'value': ((30789.65, 31065.56), (30867.18, 31195.77)), 'labels': ('F4', "F4'"), 'status': 'a', 'source': 'T4a WO-T4a-2 (29 Oct): p17 cut line placed by the page thread across the reed side arm of the masterplan corridor (C.arms; its middle digitised from the p23 plan, georeferenced on the analysis frame, +-5 m) and the stream below K6; measured with T1/levels/work/sample_cut.py (30789.65, 31065.56) -> (30867.18, 31195.77)'},
        'length_m': {'value': 151.5, 'status': 'a', 'source': 'T4a WO-T4a-2 (29 Oct): p17 cut line placed by the page thread across the reed side arm of the masterplan corridor (C.arms; its middle digitised from the p23 plan, georeferenced on the analysis frame, +-5 m) and the stream below K6; measured with T1/levels/work/sample_cut.py (30789.65, 31065.56) -> (30867.18, 31195.77)'},
        'chainage_m': {'value': 7439.9, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'angle_deg': {'value': 90.0, 'status': 'c', 'source': 'research stream centreline (research/rain_river_levels/scripts/surveyed_sections/cl.pkl), T1 levels work/sample_cut.py'},
        'walled': False,
        'bed': {'value': 47.63, 'status': 's', 'source': 'survey TIN low point; 5 real heights in the bed band, nearest 12.5 m (z 47.66)'},
        'bed_width_cm': {'value': 4020, 'status': 's', 'source': "between the survey's two stream lines HIDRO_DERE_SULU either side of the stream axis, across the stream"},
        'NE': {
            'type': 'loose_earth',
            'top': {'value': 51.11, 'status': 's', 'source': 'survey TIN, res_bank_top crest, 28.0 m out across the stream; nearest survey height 4.2 m away'},
            'height': {'value': 3.48, 'status': 's', 'source': 'bank top minus bed'},
        },
        'SW': {
            'type': 'loose_earth',
            'top': {'value': 51.08, 'status': 'i', 'source': 'survey TIN, res_bank_top crest, 43.0 m out across the stream; nearest survey height 5.1 m away'},
            'height': {'value': 3.45, 'status': 'i', 'source': 'bank top minus bed'},
        },
        'terraces': [],
        'q100': {'value': 49.85, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 50.13, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.18, 'status': 'i', 'source': 'research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K5 (0.17 m) and NİL (0.19 m)'},
        'avg_flow': {'value': 47.81, 'status': 'i', 'source': 'bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; interpolated by chainage between the surveyed sections BEGÜM K5 (0.17 m) and NİL (0.19 m)'},
        'ground': {'value': [(0.0, 52.37), (2.0, 52.39), (4.0, 52.41), (6.0, 52.42), (8.0, 52.42), (10.0, 52.42), (12.0, 52.44), (14.0, 52.46), (16.0, 52.4), (18.0, 52.33), (20.0, 52.26), (22.0, 52.19), (24.0, 52.13), (26.0, 52.08), (28.0, 52.03), (30.0, 51.98), (32.0, 51.91), (34.0, 51.85), (36.0, 51.79), (38.0, 51.72), (40.0, 51.66), (42.0, 51.6), (44.0, 51.54), (46.0, 51.45), (48.0, 51.36), (50.0, 51.26), (52.0, 51.16), (54.0, 51.13), (56.0, 51.1), (58.0, 51.08), (60.0, 51.05), (62.0, 51.02), (64.0, 50.85), (66.0, 50.44), (68.0, 50.01), (70.0, 49.61), (72.0, 49.22), (74.0, 49.05), (76.0, 48.87), (78.0, 48.71), (80.0, 48.56), (82.0, 48.42), (84.0, 48.28), (86.0, 48.13), (88.0, 48.0), (90.0, 47.9), (92.0, 47.85), (94.0, 47.8), (96.0, 47.75), (98.0, 47.7), (100.0, 47.65), (102.0, 47.64), (104.0, 47.65), (106.0, 47.66), (108.0, 47.67), (110.0, 47.81), (112.0, 48.4), (114.0, 48.98), (116.0, 49.57), (118.0, 49.71), (120.0, 49.85), (122.0, 50.05), (124.0, 50.37), (126.0, 50.7), (128.0, 51.02), (130.0, 51.09), (132.0, 51.07), (134.0, 51.06), (136.0, 51.0), (138.0, 50.98), (140.0, 50.93), (142.0, 50.88), (144.0, 50.83), (146.0, 50.78), (148.0, 50.74), (150.0, 50.71), (151.0, 50.7)], 'status': 'i', 'source': 'survey TIN along the cut every 2 m from the first end (m along the cut, m a.s.l.), sample_cut.py profile'},
        'zones': [('ARM', 27.0, 33.0)],
        'note': 'T4a: the side arm (masterplan C.arms, not in the zone base) is crossed at 30 m along the cut (its middle, 66 m from the stream axis on the SW side, digitised from booklet p23 +-5 m); recheck against masterplan_results.json "corridor" when the masterplan exports it.',
    },
]

#@@ FACTS
# ---- Shared facts (H-B 30 Oct 2026, M10): every value printed on more than one page, or printed on one page and
# used by another, has ONE row here. Read it through ../common/facts.py, never directly:
#   #@include ../common/data/FACTS.py
#   #@include ../common/facts.py
# Plain Python data (exec'd into globals by tools/build.py's bergama_data): no imports, no functions, one assignment.
#
# ROW: key -> dict
#   kind        "live" = read on every run from another script's results file (never typed here; no fallback: a
#               missing file gives None and the page prints nothing for it) | "static" = a sourced constant |
#               "derived" = computed from another row (of)
#   file        live: "water_balance" (water_balance_results.json, facts.py FACT_FILES)
#   path        live: the keys into that JSON
#   conv        None | "drip_m3_ha" (net mm / drip efficiency x 10 = m³ per ha at the intake) | "ha_per_10000" (10,000 /
#               value) | "ratio" (value[0] / value[1])
#   value       static: the value (a number, or a tuple for parts that are summed / divided by conv)
#   round       the step the printed value is rounded to (10 -> 8,000; 1 -> 8,705); nd = decimals instead
#   unit, note  printed after the number ("m³ per ha", "(1-in-5 dry year)")
#   ref         the source (internal wording; print only "public")
#   public      the citation a page may print (Sources page), None when not public
#   printed_on  the ONE booklet page that prints the fact (G4 "a fact appears once"); used_by = pages that use the
#               value without printing it (or print it only as part of a derived line)
FACTS = {
    # ---- olive water need: water board OLIVE_M3_HA = FAO-56 net dry5 / drip efficiency (water_board code.py 1519,
    # printed 8,001) and agriculture gross normal..dry (code.py 812, printed 6,830-8,000): same quantity, one rounding (T1)
    "olive_need_m3_ha": dict(
        kind="live", file="water_balance", path=("net_irrigation_mm", "olive", "dry5"), conv="drip_m3_ha",
        round=10, unit=u"m³ per ha", note=u"(1-in-5 dry year)",
        ref=u"FAO-56 soil water balance for Bergama, 34 water years (water balance results, net irrigation olive dry5); "
            u"drip efficiency 90 % (FAO Training Manual 4 ch. 3)",
        public=u"Allen et al. 1998, FAO Irrigation and Drainage Paper 56",
        printed_on="18", used_by=["19"]),
    "olive_need_normal_m3_ha": dict(
        kind="live", file="water_balance", path=("net_irrigation_mm", "olive", "mean"), conv="drip_m3_ha",
        round=10, unit=u"m³ per ha", note=u"(normal year)",
        ref=u"as olive_need_m3_ha, mean year", public=u"Allen et al. 1998, FAO Irrigation and Drainage Paper 56",
        printed_on="19", used_by=[]),
    "olive_ha_per_10000_m3": dict(
        kind="derived", of="olive_need_m3_ha", conv="ha_per_10000", nd=2, unit=u"ha", note=u"of olives per 10,000 m³",
        ref=u"10,000 m³ / olive_need_m3_ha (unrounded)", public=None,
        printed_on="18", used_by=["19"]),
    # ---- lands the water balance serves (water_balance LANDS: around2.pdf farm extent, ESA WorldCover 2021)
    "cropland_ha": dict(
        kind="live", file="water_balance", path=("lands", "cropland_ha"), conv=None, nd=1, unit=u"ha",
        note=u"fields", ref=u"around2.pdf farm extent, ESA WorldCover 2021 cropland (water balance LANDS)",
        public=u"ESA WorldCover 2021", printed_on="9", used_by=["10"]),
    "orchard_ha": dict(
        kind="live", file="water_balance", path=("lands", "orchard_ha"), conv=None, nd=2, unit=u"ha",
        note=u"olive grove", ref=u"orchards within 35 m of survey olive/fruit symbols (water balance LANDS)",
        public=None, printed_on="9", used_by=["10"]),
    # ---- storage (live from the water balance; PLAN T1: never typed)
    "storage_m3": dict(
        kind="live", file="water_balance", path=("design", "central_range_m3"), conv=None, round=1000,
        unit=u"m³", note=u"", ref=u"water balance results, design central range (sequent peak, cost cut-off)",
        public=None, printed_on="10", used_by=["11", "18"]),
    # ---- groundwater (water board AQUIFER, DECISION; research/water_data/03 rows 17 and 19)
    "aquifer_use_ratio": dict(
        kind="static", value=(198.01, 45.4), conv="ratio", nd=1, unit=u"×", note=u"its potential",
        ref=u"Lower Bakırçay: total water use 198.01 hm³ (Tablo 4.3 p.31) / groundwater potential 45.4 hm³ (Tablo 5.3 "
            u"p.36), Kuzey Ege Kuraklık Yönetim Planı 2018 (S10)",
        public=u"Kuzey Ege Havzası Kuraklık Yönetim Planı, 2018", printed_on="18", used_by=["19"]),
    "arsenic_ug_l": dict(
        kind="static", value=10, conv=None, round=1, unit=u"µg/L", note=u"arsenic above (not for drinking)",
        ref=u"Somay & Gemici 2015 (DATA_REGISTER EN-E3)", public=u"Somay & Gemici 2015",
        printed_on="18", used_by=[]),
    # ---- olive area in Bergama: TÜİK 2025, 65,978 + 21,068 da (agriculture code.py 536) = 8,704.6 ha (PLAN T1)
    "olive_area_ha": dict(
        kind="static", value=(65978.0, 21068.0), conv="da_sum_ha", round=1, unit=u"ha", note=u"of olives in Bergama",
        ref=u"TÜİK 2025 district crop areas, MEDAS export (library/research/crops_2026-10-24/"
            u"bergama_crops_irrigation_v1.md §1.25)",
        public=u"TÜİK, Bitkisel Üretim İstatistikleri 2025", printed_on="19", used_by=[]),
    # ---- constants used by the conversions (sourced)
    "drip_efficiency": dict(
        kind="static", value=0.90, conv=None, nd=2, unit=u"", note=u"",
        ref=u"water balance v2 DRIP_EFF (FAO Training Manual 4 ch. 3)", public=None, printed_on=None, used_by=["18", "19"]),
}

#@@ CUTS
CUTS = [  # the channel cut on the main survey: ground every 1 m (m above the bed low point), depths of EVENTS (m above the bed),
          # the width each level covers (from, to; m from the centreline, + = left bank looking downstream), notes
    dict(key="flat", name=u"5 · FLAT DOWNSTREAM END", bed=41.33, u0=-62,
         ground=[3.97, 3.92, 3.88, 3.84, 3.80, 3.78, 3.76, 3.74, 3.72, 3.42, 2.79, 2.16, 1.52, 0.95, 0.89, 0.82, 0.76, 0.70, 0.68, 0.66, 0.64, 0.61, 0.59, 0.57, 0.55, 0.52, 0.50, 0.48, 0.46, 0.44, 0.41, 0.39, 0.37, 0.35, 0.33, 0.32, 0.30, 0.29, 0.27, 0.26, 0.24, 0.23, 0.21, 0.20, 0.19, 0.17, 0.16, 0.14, 0.13, 0.11, 0.10, 0.08, 0.07, 0.06, 0.04, 0.03, 0.01, 0.00, 0.00, 0.01, 0.01, 0.02, 0.02, 0.02, 0.03, 0.03, 0.04, 0.04, 0.05, 0.05, 0.06, 0.06, 0.07, 0.07, 0.08, 0.08, 0.08, 0.09, 0.09, 0.10, 0.09, 0.11, 0.13, 0.16, 0.18, 0.21, 0.24, 0.26, 0.29, 0.32, 0.35, 0.38, 0.41, 0.43, 0.46, 0.49, 0.54, 0.59, 0.64, 0.70, 0.75, 0.80, 0.86, 0.91, 0.96, 1.02, 1.07, 1.12, 1.18, 1.23, 1.28, 1.34, 1.46, 1.65, 1.84, 2.03, 2.22, 2.41, 2.61, 2.80, 2.94, 3.06, 3.17, 3.29, 3.40],
         dep=(0.23, 0.69, 1.14, 1.38, 1.54),
         ext=[(-20.5, 23.5), (-44.0, 36.5), (-49.0, 45.0), (-49.5, 49.0), (-50.0, 50.0)],
         tags=[("slope", u"bed 1.09 %"), ("points", u"3 bed points within 25 m · floor interpolated"), ("spread", u"banks 114 m apart · floods wide and thin"),
               ("road", u"road 3.7 m wide · 52 m off · left bank"), ("pin", u"S4 detail: 280 m upstream")]),
    dict(key="up", name=u"1 · UPSTREAM ENTRY", bed=70.36, u0=-42,
         ground=[5.45, 5.24, 5.17, 5.11, 5.05, 4.99, 4.92, 4.86, 4.55, 4.18, 3.82, 3.45, 3.01, 2.57, 2.21, 2.14, 2.07, 2.00, 1.93, 1.86, 1.80, 1.73, 1.66, 1.59, 1.52, 1.45, 1.38, 1.32, 1.25, 1.19, 1.12, 1.06, 0.99, 0.93, 0.87, 0.80, 0.74, 0.67, 0.61, 0.54, 0.48, 0.41, 0.35, 0.29, 0.22, 0.16, 0.09, 0.03, 0.02, 0.39, 0.75, 1.10, 1.46, 1.82, 2.19, 2.54, 2.86, 3.16, 3.46, 3.75, 3.97, 4.05, 4.24, 4.46, 4.70, 4.94, 5.07, 5.08, 5.12, 5.14],
         dep=(0.64, 1.69, 2.57, 2.99, 3.30),
         ext=[(-4.0, 7.5), (-20.0, 10.5), (-28.5, 13.0), (-29.5, 14.0), (-30.5, 15.0)],
         tags=[("slope", u"bed 0.83 %"), ("points", u"73 bed points within 25 m"), ("road", u"road 6.5 m wide · 38 m off · right bank")]),
    dict(key="k4", name=u"2 · K4 BRIDGE", bed=64.77, u0=-80,
         ground=[3.06, 3.03, 3.01, 2.99, 2.96, 2.94, 2.92, 2.89, 2.87, 2.85, 2.82, 2.80, 2.78, 2.75, 2.73, 2.71, 2.68, 2.66, 2.64, 2.61, 2.59, 2.56, 2.54, 2.52, 2.49, 2.47, 2.45, 2.42, 2.40, 2.38, 2.35, 2.33, 2.31, 2.28, 2.26, 2.24, 2.21, 2.19, 2.17, 2.14, 2.12, 2.10, 2.07, 2.07, 2.07, 2.07, 2.07, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 2.08, 1.77, 1.35, 0.93, 0.51, 0.14, 0.14, 0.13, 0.13, 0.12, 0.12, 0.12, 0.11, 0.11, 0.10, 0.10, 0.09, 0.09, 0.08, 0.08, 0.07, 0.07, 0.06, 0.06, 0.05, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.02, 0.02, 0.14, 0.41, 0.68, 0.99, 1.94, 2.89, 3.84, 4.78, 5.73, 6.68, 7.63, 8.58, 9.53, 10.48, 10.87, 11.07, 11.27],
         dep=(0.28, 0.99, 1.83, 2.56, 2.84),
         ext=[(-16.0, 12.5), (-18.0, 15.0), (-20.0, 15.5), (-58.5, 16.5), (-70.5, 16.5)],
         tags=[("slope", u"bed 0.81 %"), ("flag", u"no stream/bank lines: spot heights + contours · 5 bed points"),
               # v4 (MIRAQUA 28 Oct, bank-depth research REPORT §4.4, Aras 14:12: the survey is the inferior source)
               ("over", u"right bank 2.1 m (survey, before the DSİ walls): street floods"),   # two chips: they wrap
               ("over", u"Q100 0.2-0.4 m · Q500 0.5-0.7 m"),
               ("road", u"road 10-13 m wide · 42-52 m off · right bank")]),
    dict(key="k5", name=u"3 · K5 BRIDGE", bed=55.96, u0=-57,
         ground=[3.12, 3.11, 3.09, 3.08, 3.06, 3.05, 3.02, 2.97, 2.93, 2.89, 2.85, 2.80, 2.76, 2.72, 2.68, 2.63, 2.59, 2.55, 2.51, 2.46, 2.42, 2.38, 2.34, 2.29, 2.25, 2.20, 2.16, 2.11, 2.07, 1.99, 1.89, 1.78, 1.67, 1.56, 1.45, 1.36, 1.26, 1.17, 1.07, 0.95, 0.82, 0.69, 0.58, 0.47, 0.33, 0.19, 0.16, 0.13, 0.09, 0.06, 0.02, 0.00, 0.01, 0.02, 0.03, 0.05, 0.06, 0.07, 0.08, 0.09, 0.11, 0.12, 0.13, 0.14, 0.15, 0.17, 0.32, 1.03, 1.73, 2.43, 3.02, 3.60, 4.18, 4.73, 5.26, 5.77, 6.23, 6.66, 7.08, 7.43, 7.80, 8.09],
         dep=(0.31, 1.09, 1.95, 2.45, 2.79),
         ext=[(-12.5, 8.5), (-19.0, 10.0), (-27.5, 11.0), (-37.5, 12.0), (-45.5, 12.5)],
         tags=[("slope", u"bed 1.07 %"), ("points", u"12 bed points within 25 m"), ("spread", u"right bank rises gently: floods widen")]),
    dict(key="down", name=u"4 · DOWNSTREAM REACH", bed=45.67, u0=-42,
         ground=[4.61, 4.81, 5.00, 4.97, 4.66, 4.35, 4.05, 3.74, 3.44, 3.13, 2.83, 2.50, 2.15, 1.80, 1.45, 1.11, 0.76, 0.41, 0.06, 0.01, 0.02, 0.03, 0.05, 0.06, 0.08, 0.09, 0.10, 0.11, 0.12, 0.12, 0.13, 0.14, 0.15, 0.15, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.16, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.24, 0.43, 0.62, 0.80, 0.86, 0.91, 0.97, 1.02, 1.08, 1.13, 1.19, 1.24, 1.44, 1.81, 2.19, 2.56, 2.93, 3.35, 3.76, 4.06, 4.08, 4.08, 4.05, 4.02, 3.99, 3.95, 3.86],
         dep=(0.31, 0.96, 1.68, 2.05, 2.33),
         ext=[(-24.5, 6.0), (-26.5, 11.5), (-28.5, 18.5), (-29.5, 19.5), (-30.5, 20.0)],
         tags=[("slope", u"bed 0.98 %"), ("points", u"2 bed points within 25 m · bed interpolated"), ("road", u"road 5-9 m wide · 25-30 m off · left bank")]),
    dict(key="dsi", name=u"DSİ PLANNED CHANNEL 20 x 3 m", bed=None, u0=-16,
         ground=[3.0] * 7 + [0.0] * 19 + [3.0] * 7,
         dep=(0.22, 1.07, 2.20, 2.87, 3.39),
         ext=[(-10.0, 10.0)] * 5,
         tags=[]),   # v1.14: its size is printed under the cut (draw_cut, DSI_SRC)
]

#@@ SPECIES
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

#@@ SKETCH_SRC
SKETCH_SRC = r'''# The idea sketches of pr1_drawings v3.1 (concept sections, SKETCH style), run in their own namespace: pr1 baked them
# into Rhino; here the same calls make page items. The draw order is pr1's (bake order plus its lifts Z_*).
import math
ZP = []
ORDER = [0]
FORM = "A"
PEOPLE = True
NODE = None                                          # set by the board: the element numbers
CITE = None                                          # v3: set by the board: a source's number "[n]" (footer key)
ORIGIN = (0.0, 0.0)                                  # pr1 placed the sketches beside the site map; here at 0


def _hexc(c):
    return "%02X%02X%02X" % tuple(c)


def _put(item, z):
    ORDER[0] += 1
    ZP.append((ORDER[0] + z, ORDER[0], item))


def P(o, x, y):
    return (o[0] + x, o[1] + y)


def add_polyline(q):
    out = []
    for p in q:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-6:
            out.append((p[0], p[1]))
    return out if len(out) >= 2 else None


def keep(obj, sub, colour, width=None, dashed=False, alpha=None, z=0):
    if obj is None:
        return None
    _put(("line", obj, _hexc(colour), width if width else 0.13, [1.0, 0.7] if dashed else None, 1), z)
    return obj


def pline(o, pts, sub, colour, width=0.18, closed=False, dashed=False, z=0):
    q = [P(o, x, y) for x, y in pts]
    if closed and q[0] != q[-1]:
        q.append(q[0])
    return keep(add_polyline(q), sub, colour, width, dashed, z=z)


def fill(o, pts, sub, colour, alpha=None, boundary=True, z=0, hand_=None):
    if HAND[0] if hand_ is None else hand_:
        pts = hand_ring(pts, sub)
        boundary = False
    ring = [P(o, x, y) for x, y in pts]
    if len(ring) < 3:
        return None
    _put(("poly", [ring], _hexc(colour), None, 0.1, None, None, alpha), z)
    if boundary:
        pline(o, pts, sub, colour, 0.13, closed=True, z=z)
    return ring


def hatch_lines(o, pts, sub, colour, spacing=1.6, angle=45.0, width=None):
    width = LW_HATCH if width is None else width
    for p0, p1 in clip_segments(pts, spacing, angle):
        keep([P(o, *p0), P(o, *p1)], sub, colour, width)


def text(o, s, x, y, size_pt, colour=None, sub="text", just="left", bold=False, mask=None):
    colour = INK if colour is None else colour
    h = size_pt * 0.353
    for i, ln in enumerate(s.split("\n")):
        if ln.strip():
            q = P(o, x, y - i * h * 1.35)
            _put(("text", ln, q[0], q[1], h, _hexc(colour), bold, {"left": "L", "right": "R"}.get(just, "C"), None,
                  _hexc(mask) if mask else None), Z_TEXT)      # pr1's text mask: a halo in its colour


def _smooth(o, pts):
    """A Catmull-Rom curve through the points (pr1: Rhino's interpolated curve), as a fine polyline."""
    q = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(q) - 2):
        p0, p1, p2, p3 = q[i - 1], q[i], q[i + 1], q[i + 2]
        for k in range(8):
            t = k / 8.0
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t * t
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t ** 3) for j in (0, 1)))
    out.append(pts[-1])
    return add_polyline([P(o, x, y) for x, y in out])


def title(o, h, s):
    text(o, s, 0, h + 4, 7.0, INK, "title", bold=True)

def hx(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

INK, INK2 = hx("4A3F35"), hx("847E75")
SOIL, STONE, ROAD = hx("CDBF9F"), hx("A4A1A3"), hx("3A3A3A")
W_SUM, W_WIN, W_EXT = hx("A9C3CC"), hx("7FA7B8"), hx("5C7A86")
REED, ACCENT, HERITAGE, WHITE = hx("89986A"), hx("BC6F45"), hx("8B2D2D"), (255, 255, 255)
CELL, FARM = hx("DFE6CF"), hx("E7E0C8")
def mix(a, b, t):
    """Plain RGB mix of two palette colours (t = share of b), for hatch and outline tones only."""
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))

SOIL_HATCH = mix(SOIL, INK, 0.30)      # earth hatch over the soil poché
STONE_HATCH = mix(STONE, INK, 0.35)    # masonry hatch, K4 bridge behind
REED_HEAD = mix(REED, INK, 0.35)       # reed plumes
FIGURE = INK2                          # scale figures
# line weights (print width, mm): what the section cuts is heaviest, what is seen beyond it is thin
LW_CUT, LW_PROFILE, LW_EDGE, LW_BEYOND, LW_FINE, LW_HATCH = 0.50, 0.35, 0.25, 0.13, 0.09, 0.05
Z_TREE, Z_LINE, Z_PEOPLE, Z_TEXT = 300000, 400000, 600000, 900000   # draw-order lifts: trees, lines, people, texts
def clip_segments(pts, spacing, angle):
    """The pieces of parallel lines (spacing, angle in degrees) that lie inside a closed outline."""
    segs = []
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    r = [(x * ca + y * sa, -x * sa + y * ca) for x, y in pts]       # outline turned so the hatch runs along x
    if r[0] != r[-1]:
        r.append(r[0])
    ys = [p[1] for p in r]
    k = int(math.floor(min(ys) / spacing)) + 1
    while k * spacing < max(ys):
        yy = k * spacing
        xs = sorted(x1 + (yy - y1) * (x2 - x1) / (y2 - y1) for (x1, y1), (x2, y2) in zip(r[:-1], r[1:])
                    if (y1 <= yy < y2) or (y2 <= yy < y1))
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 0.05:
                p0 = (xs[i] * ca - yy * sa, xs[i] * sa + yy * ca)
                p1 = (xs[i + 1] * ca - yy * sa, xs[i + 1] * sa + yy * ca)
                segs.append((p0, p1))
        k += 1
    return segs

def notch(g, cuts):
    """Ground outline g with rectangular basins cut into its level stretches: cuts = [(x0, x1, y_top, depth)]."""
    out = list(g)
    for x0, x1, y, d in cuts:
        for i in range(len(out) - 1):
            (ax, ay), (bx, by) = out[i], out[i + 1]
            if abs(ay - y) < 1e-9 and abs(by - y) < 1e-9 and min(ax, bx) <= x0 and x1 <= max(ax, bx):
                ins = [(x0, y), (x0, y - d), (x1, y - d), (x1, y)]
                ins = ins if ax < bx else ins[::-1]
                ins = [p for p in ins if p != out[i] and p != out[i + 1]]
                out[i + 1:i + 1] = ins
                break
    return out

def surface_y(surface, x):
    """Height of the ground surface at x (on a vertical step: the lower of the two)."""
    ys = [ay + (by - ay) * (x - ax) / (bx - ax) for (ax, ay), (bx, by) in zip(surface[:-1], surface[1:])
          if bx != ax and min(ax, bx) <= x <= max(ax, bx)]
    return min(ys) if ys else None

def surface_between(surface, x0, x1, dy=0.0):
    """The surface from x0 to x1 (steps inside kept, risers at the two ends dropped), lifted by dy."""
    out = []
    for (ax, ay), (bx, by) in zip(surface[:-1], surface[1:]):
        if max(ax, bx) < x0 or min(ax, bx) > x1:
            continue
        if ax == bx:
            seg = [(ax, ay), (bx, by)]
        else:
            seg = []
            for x in (max(min(ax, bx), x0), min(max(ax, bx), x1)) if ax < bx else (min(max(ax, bx), x1), max(min(ax, bx), x0)):
                seg.append((x, ay + (by - ay) * (x - ax) / (bx - ax)))
        for q in seg:
            if not out or abs(q[0] - out[-1][0]) + abs(q[1] - out[-1][1]) > 1e-9:
                out.append(q)
    while len(out) > 2 and out[0][0] == out[1][0]:
        out.pop(0)
    while len(out) > 2 and out[-1][0] == out[-2][0]:
        out.pop()
    return [(x, y + dy) for x, y in out]

def reeds(o, x0, x1, y, h=3.5, plan=False):
    """Reed clumps at v2.8's spacing and height: a fan of thin arched blades of mixed height, a plume on every third
    clump. plan=True (form plans): a small tuft of radiating leaves seen from above."""
    rnd = _tree_rand(x0 + 0.37 * x1, y)
    n = max(3, int((x1 - x0) / 1.6))
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        if plan:
            m = 6 + int(rnd() * 3)
            for j in range(m):
                t = 6.283 * (j + 0.4 * rnd()) / m
                L = h * 0.38 * (0.6 + 0.4 * rnd())
                keep([P(o, x, y), P(o, x + L * math.cos(t), y + L * math.sin(t))], "planting", REED, LW_FINE)
            continue
        nb = 5 + int(rnd() * 3)
        tall = None
        for j in range(nb):
            s = (j / (nb - 1.0) - 0.5) * 2.0 + (rnd() - 0.5) * 0.35       # -1 .. 1: leaning left .. right
            hh = h * (0.62 + 0.38 * rnd()) * (1.0 - 0.18 * abs(s))
            pts = [(x + 0.12 * s + s * hh * 0.42 * t * t, y + hh * (t - 0.10 * abs(s) * t * t)) for t in (0.0, 0.35, 0.7, 1.0)]
            keep(_smooth(o, pts), "planting", REED, LW_FINE)
            if tall is None or hh > tall[0]:
                tall = (hh, pts)
        if i % 3 == 1 and tall:                    # plume along the tallest blade's tip
            (ax, ay), (bx, by) = tall[1][-2], tall[1][-1]
            L = math.hypot(bx - ax, by - ay) or 1.0
            ux, uy = (bx - ax) / L, (by - ay) / L
            ln, wd = 0.30 * h, 0.05 * h
            cx, cy = bx + ux * ln * 0.5, by + uy * ln * 0.5
            fill(o, [(bx, by), (cx - uy * wd, cy + ux * wd), (bx + ux * ln, by + uy * ln), (cx + uy * wd, cy - ux * wd)],
                 "planting", REED_HEAD, boundary=False)

def bank(p, q, n=24):
    """Edge where the project meets the water: S-curve in form A, one straight facet in form B."""
    if FORM == "B":
        return [p, q]
    out = []
    for i in range(n):
        t = i / (n - 1.0)
        s = (1 - math.cos(t * math.pi)) / 2
        out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * s))
    return out

def road(o, x0, x1, y, label, ly=None, mask=None):
    fill(o, [(x0, y), (x1, y), (x1, y + 1.3), (x0, y + 1.3)], "road", ROAD)
    text(o, label, x0 + 1, ly if ly is not None else y - 2.5, 5.0, ROAD, "road", mask=mask)

def level_mark(o, x, y, colour, sub):
    """Level sign: a small open triangle standing point-down on the level line."""
    pline(o, [(x - 1.0, y + 1.7), (x + 1.0, y + 1.7), (x, y)], sub, colour, LW_BEYOND, closed=True, z=Z_LINE)

HAND_AMP = 0.18          # mm: sideways wobble of a hand line
HAND_WAV = 7.0           # mm: length of one wobble
HAND_OVER = 1.1          # mm: how far a stroke runs past its corner
HAND_FONT = ["Ink Free", "Segoe Print", "Comic Sans MS"]   # first one installed (Windows 10/11 ship Ink Free)
PEN_HAIR, PEN_FINE, PEN_MED, PEN_BOLD = 0.13, 0.20, 0.40, 0.70   # masterplan v9 pens (mm)
SKINK = hx("1E1E1E")                                 # fine-liner black: the line that carries the idea
SUN, SUN_RAY = hx("E8C64A"), hx("C9A227")           # the dry summer (Aras): marker yellow
HAND = [False]                                       # True while a part is drawn by hand (form plans: pline / fill wobble)
HAND_TEXT = [False]                                  # True while texts take the hand font and drop their masks
KHAKI, PAPER, BG_ = hx("BCB794"), hx("F1EDDF"), hx("E6E0C8")
SEC_POCHE = mix(KHAKI, PAPER, 0.62)                  # board: the cut ground
SEC_POCHE_BAND = mix(SEC_POCHE, KHAKI, 0.45)          # the band just under the surface, a little deeper
SEC_PAVE = mix(hx("BC6F45"), BG_, 0.12)              # board: walkable edge, terracotta
SEC_CHANNEL_HATCH = hx("3E7DAE")                     # board: the stream bed's blue hatch
SITE_WATER, SITE_WATER_D, SITE_FLOOD = hx("7FA4B3"), hx("5E8494"), hx("B4CBD2")   # board CAT water, BLUE_D, BLUE_L
FLOOD_WASH, FLOOD_ALPHA = hx("4F9BD9"), 0.09         # the design flood's reach up to Q500: one clear blue, see-through
                                                      # and so faint it takes a moment to see (Nil 17:59: "really really faint blue,
                                                      # almost indistinguishable ... should need a focus to see"); raise FLOOD_ALPHA = stronger
SITE_PEOPLE = mix(hx("7A6E60"), BG_, 0.1)            # board: SA_STYLE_BOARD people
SITE_TREE = (hx("B2C484"), hx("8CA466"), hx("688052"))   # board SA_TREE_PAL["tree"]: light, mid, shadow
SITE_TRUNK = hx("6E625A")                            # board SA_TRUNK
HOUSE_WALL, HOUSE_ROOF = hx("D9B98C"), hx("A86A55")  # board TYPO["traditional"] tone, TYPO_ROOF_C
SA_FIGS = [                                          # board SA_FIGS (m, 1.75 m tall), SA_HEAD
    [(-0.10, 0.0), (-0.06, 0.0), (-0.03, 0.82), (0.03, 0.82), (0.06, 0.0), (0.10, 0.0), (0.12, 0.85), (0.16, 1.38),
     (0.10, 1.47), (0.05, 1.50), (0.05, 1.53), (-0.05, 1.53), (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.12, 0.85)],
    [(-0.30, 0.0), (-0.24, 0.0), (-0.02, 0.78), (0.18, 0.0), (0.25, 0.0), (0.11, 0.86), (0.18, 1.12), (0.12, 1.40),
     (0.06, 1.48), (0.05, 1.53), (-0.05, 1.53), (-0.07, 1.47), (-0.14, 1.38), (-0.20, 1.10), (-0.12, 0.86)],
    [(-0.20, 0.0), (0.20, 0.0), (0.13, 0.62), (0.11, 1.08), (0.15, 1.36), (0.09, 1.45), (0.05, 1.49), (0.05, 1.52),
     (-0.05, 1.52), (-0.05, 1.49), (-0.09, 1.45), (-0.15, 1.36), (-0.11, 1.08), (-0.13, 0.62)],
    [(-0.11, 0.0), (-0.06, 0.0), (-0.02, 0.80), (0.04, 0.80), (0.08, 0.0), (0.13, 0.0), (0.12, 0.86), (0.30, 0.86),
     (0.30, 0.55), (0.40, 0.55), (0.40, 0.95), (0.17, 1.38), (0.10, 1.47), (0.05, 1.51), (0.05, 1.53), (-0.05, 1.53),
     (-0.05, 1.50), (-0.10, 1.47), (-0.16, 1.38), (-0.13, 0.86)],
]
SA_HEAD = (0.0, 1.64, 0.105)

import zlib as _zlib, random as _random
def _seed(*parts):
    return _zlib.crc32(repr([round(float(v), 2) if isinstance(v, float) else v for v in parts]).encode("utf-8")) & 0x7fffffff

def _densify(P, step):
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(math.ceil(math.hypot(b[0] - a[0], b[1] - a[1]) / step)))
        out += [(a[0] + (b[0] - a[0]) * k / float(n), a[1] + (b[1] - a[1]) * k / float(n)) for k in range(1, n + 1)]
    return out

def _normals(a):
    out = []
    for i in range(len(a)):
        p, q = a[max(0, i - 1)], a[min(len(a) - 1, i + 1)]
        d = math.hypot(q[0] - p[0], q[1] - p[1]) or 1e-12
        out.append((-(q[1] - p[1]) / d, (q[0] - p[0]) / d))
    return out

def _noise(n, step, wav, rnd):
    """n values of smooth noise (std about 1), features about wav long (masterplan smooth_noise)."""
    k = max(2, int(math.ceil(n * step / wav)) + 3)
    ctrl = [rnd.gauss(0.0, 1.0) for _ in range(k)]
    out = []
    for j in range(n):
        x = j * step / wav
        i = min(int(x), k - 2)
        f = x - i
        f = f * f * (3 - 2 * f)
        out.append(ctrl[i] * (1 - f) + ctrl[i + 1] * f)
    return out

def hand(P, amp, wav, seed, closed=False, over=0.0):
    """A polyline as a hand draws it (masterplan hand_line): smooth sideways wobble of about amp (at most 2.2 amp),
    an overshoot of `over` at both ends of an open line; a closed ring starts at a random point."""
    a = [(float(p[0]), float(p[1])) for p in P]
    if len(a) < 2:
        return a
    rnd = _random.Random(seed)
    step = max(wav / 6.0, 1e-6)
    if closed:
        if math.hypot(a[0][0] - a[-1][0], a[0][1] - a[-1][1]) < 1e-9:
            a = a[:-1]
        k = rnd.randrange(len(a))
        a = a[k:] + a[:k] + [a[k]]
    a = _densify(a, step)
    if over > 0 and not closed:
        (x0, y0), (x1, y1) = a[0], a[1]
        d = math.hypot(x1 - x0, y1 - y0) or 1e-12
        s = (x0 - (x1 - x0) / d * over, y0 - (y1 - y0) / d * over)
        (x0, y0), (x1, y1) = a[-1], a[-2]
        d = math.hypot(x1 - x0, y1 - y0) or 1e-12
        a = [s] + a + [(x0 - (x1 - x0) / d * over, y0 - (y1 - y0) / d * over)]
    if amp > 0:
        w = [max(-2.2, min(2.2, v)) * amp for v in _noise(len(a), step, wav, rnd)]
        a = [(p[0] + n[0] * v, p[1] + n[1] * v) for p, n, v in zip(a, _normals(a), w)]
    return a

def _strokes(P, closed, turn=28.0):
    """A polyline split at its corners, as a hand draws it: one stroke per straight run."""
    P = list(P) + ([P[0]] if closed and P[0] != P[-1] else [])
    out = [[P[0]]]
    for i in range(1, len(P) - 1):
        a, b, c = P[i - 1], P[i], P[i + 1]
        t1, t2 = math.atan2(b[1] - a[1], b[0] - a[0]), math.atan2(c[1] - b[1], c[0] - b[0])
        out[-1].append(b)
        if abs((math.degrees(t2 - t1) + 180) % 360 - 180) > turn:
            out.append([b])
    out[-1].append(P[-1])
    return [s for s in out if len(s) > 1]

def _crosses(ring):
    """True when a closed ring crosses itself (a hatch from it would fail or fill wrongly)."""
    q = list(ring) + ([ring[0]] if ring[0] != ring[-1] else [])
    E = list(zip(q[:-1], q[1:]))
    box = [(min(a[0], b[0]), max(a[0], b[0]), min(a[1], b[1]), max(a[1], b[1])) for a, b in E]

    def o_(p, r, t):
        return (r[0] - p[0]) * (t[1] - p[1]) - (r[1] - p[1]) * (t[0] - p[0])
    m = len(E)
    for i in range(m):
        a, b = E[i]
        bi = box[i]
        for j in range(i + 2, m):
            if i == 0 and j == m - 1:
                continue
            bj = box[j]
            if bi[1] < bj[0] or bj[1] < bi[0] or bi[3] < bj[2] or bj[3] < bi[2]:
                continue
            c, d = E[j]
            if o_(a, b, c) * o_(a, b, d) < -1e-12 and o_(c, d, a) * o_(c, d, b) < -1e-12:
                return True
    return False

def hand_ring(pts, sub, amp=HAND_AMP, wav=HAND_WAV):
    """A closed outline drawn by hand; where the wobble would make it cross itself (narrow or sharp shapes), a smaller
    wobble, else the true outline."""
    sd = _seed(pts[0][0], pts[0][1], len(pts), sub)
    for k in (1.0, 0.5, 0.25):
        r = hand(pts, amp * k, wav, sd, closed=True)
        if not _crosses(r):
            return r
    return list(pts)

def sketch(o, pts, sub, colour, width=0.25, closed=False, over=HAND_OVER, amp=HAND_AMP, retrace=True, z=0,
           dashed=False):
    """Fine-liner line: each straight run its own stroke, wobbling and running past the corners; long runs are
    traced a second time, lighter and not quite end to end, as a sketch is."""
    for k, s in enumerate(_strokes(pts, closed)):
        sd = _seed(s[0][0], s[0][1], s[-1][0], s[-1][1], k, sub)
        q = hand(s, amp, HAND_WAV, sd, over=over)
        keep(add_polyline([P(o, *p) for p in q]), sub, colour, width, dashed, z=z)
        L = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(s[:-1], s[1:]))
        if retrace and not dashed and L > 6.0:
            rnd = _random.Random(sd + 7)
            q = hand(s, amp * 1.6, HAND_WAV * 0.8, sd + 11, over=over * 0.5)
            i0, i1 = int(len(q) * 0.15 * rnd.random()), len(q) - int(len(q) * 0.25 * rnd.random())
            if i1 - i0 > 1:
                keep(add_polyline([P(o, *p) for p in q[i0:i1]]), sub, colour, width * 0.45, z=z)

def wash(o, poly, sub, colour, alpha=0.5, z=0):
    """Watercolour wash: a see-through fill whose edge wobbles a little past the true outline."""
    ring = hand_ring(poly, sub, HAND_AMP * 1.8, HAND_WAV * 1.6)
    return fill(o, ring, sub, colour, alpha=alpha, boundary=False, z=z, hand_=False)

def marker(o, poly, sub, colour, angle=55.0, spacing=0.75, thick=0.62, alpha=0.55, base=0.22, z=0):
    """Marker fill: parallel strokes laid side by side at a slant, each a little longer or shorter than the shape
    (and slightly turned), over a faint wash of the same colour: the key element of a sketch (example 4)."""
    if base:
        wash(o, poly, sub, colour, base, z)
    rnd = _random.Random(_seed(poly[0][0], poly[0][1], angle, sub))
    for p0, p1 in clip_segments(poly, spacing, angle):
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy)
        if L < 0.2:
            continue
        ux, uy = dx / L, dy / L
        a0, a1 = (rnd.random() - 0.35) * 0.9, (rnd.random() - 0.35) * 0.9
        tw = (rnd.random() - 0.5) * 0.35
        s = (p0[0] - ux * a0, p0[1] - uy * a0)
        e = (p1[0] + ux * a1 - uy * tw, p1[1] + uy * a1 + ux * tw)
        nx, ny = -uy * thick / 2, ux * thick / 2
        fill(o, [(s[0] + nx, s[1] + ny), (e[0] + nx, e[1] + ny), (e[0] - nx, e[1] - ny), (s[0] - nx, s[1] - ny)],
             sub, colour, alpha=alpha, boundary=False, z=z, hand_=False)

def band(surface, x0, x1, depth):
    """Polygons of a band `depth` under the ground surface from x0 to x1 (split at vertical steps)."""
    seg = surface_between(surface, x0, x1)
    pieces, cur = [], [seg[0]] if seg else []
    for q in seg[1:]:
        if abs(q[0] - cur[-1][0]) < 1e-9:
            pieces.append(cur)
            cur = [q]
        else:
            cur.append(q)
    if cur:
        pieces.append(cur)
    return [pc + [(x, y - depth) for x, y in pc[::-1]] for pc in pieces if len(pc) > 1]

def under_level(surface, x0, x1, level):
    """The space between the ground and a level, x0..x1 (what that level puts under water)."""
    bed = [(x, min(level, y)) for x, y in surface_between(surface, x0, x1)]
    return [(x0, level), (x1, level)] + bed[::-1] if len(bed) > 1 else None

def hand_arrow(o, a, b, colour, sub="arrows", width=0.55, head=2.2, z=Z_LINE, bend=0.0):
    """Link arrow in the masterplan v9 manner (head barbs at 38 deg), drawn as filled marker shapes so it reads at
    every zoom and in the viewport, where print widths do not show (Nil 18 Oct 17:55: "the outflow drainage is gone"):
    a hand-wobbled shaft `width` wide that tapers a little towards the tip (bend > 0 bows it), and a solid head."""
    pts = [a, b]
    if bend:
        m = ((a[0] + b[0]) / 2.0 - (b[1] - a[1]) * bend, (a[1] + b[1]) / 2.0 + (b[0] - a[0]) * bend)
        pts = [(a[0] * (1 - t) ** 2 + 2 * m[0] * t * (1 - t) + b[0] * t * t, a[1] * (1 - t) ** 2 + 2 * m[1] * t * (1 - t) + b[1] * t * t)
               for t in [i / 24.0 for i in range(25)]]
    t = math.atan2(b[1] - pts[-2][1], b[0] - pts[-2][0])
    hl = head * math.cos(math.radians(38))                 # the head's length along the shaft
    L = sum(math.hypot(q[0] - p[0], q[1] - p[1]) for p, q in zip(pts[:-1], pts[1:]))
    shaft, acc = [pts[0]], 0.0
    for p, q in zip(pts[:-1], pts[1:]):
        d = math.hypot(q[0] - p[0], q[1] - p[1])
        if acc + d >= L - hl * 0.7:
            f = (L - hl * 0.7 - acc) / (d or 1e-12)
            shaft.append((p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f))
            break
        shaft.append(q)
        acc += d
    sh = hand(shaft, HAND_AMP * 0.5, HAND_WAV, _seed(a[0], a[1], b[0], b[1], sub))
    nm = _normals(sh)
    n = len(sh)
    w_ = [width * (1.0 - 0.3 * i / max(1, n - 1)) / 2.0 for i in range(n)]
    left = [(p[0] + v[0] * w, p[1] + v[1] * w) for p, v, w in zip(sh, nm, w_)]
    right = [(p[0] - v[0] * w, p[1] - v[1] * w) for p, v, w in zip(sh, nm, w_)]
    fill(o, left + right[::-1], sub, colour, boundary=False, z=z, hand_=False)
    tip = (b[0] + math.cos(t) * 0.2, b[1] + math.sin(t) * 0.2)
    wings = [(b[0] - head * math.cos(t + sg * math.radians(38)), b[1] - head * math.sin(t + sg * math.radians(38))) for sg in (1, -1)]
    notch_ = (b[0] - hl * 0.7 * math.cos(t), b[1] - hl * 0.7 * math.sin(t))
    fill(o, [tip, wings[0], notch_, wings[1]], sub, colour, boundary=False, z=z, hand_=False)

def sun(o, x, y, r=2.2):
    """The dry summer: a marker-yellow sun with short hand rays (as in Nil's SNFCC sketch)."""
    disc_ = [(x + r * math.cos(6.283 * i / 20), y + r * math.sin(6.283 * i / 20)) for i in range(20)]
    wash(o, disc_, "sun", SUN, 0.85, z=Z_LINE)
    sketch(o, disc_, "sun", SKINK, PEN_FINE, closed=True, over=0.0, amp=0.08, retrace=False, z=Z_LINE)
    for k in range(9):
        t = 6.283 * (k + 0.3) / 9
        sketch(o, [(x + 1.45 * r * math.cos(t), y + 1.45 * r * math.sin(t)), (x + 2.1 * r * math.cos(t), y + 2.1 * r * math.sin(t))],
               "sun", SKINK, PEN_FINE, over=0.0, amp=0.03, retrace=False, z=Z_LINE)

def cloud_rain(o, x, y, r=1.0):
    """v3: the wet winter, a hand cloud with three rain strokes, centred at (x, y)."""
    pts = []
    for i in range(28):
        a = 6.283 * i / 28
        k = 1.0 + 0.24 * max(0.0, math.sin(a)) * abs(math.sin(3 * a))
        pts.append((x + 1.6 * r * math.cos(a) * k, max(y - 0.5 * r, y + 0.85 * r * math.sin(a) * k)))
    wash(o, pts, "season", SITE_FLOOD, 0.85, z=Z_LINE)
    sketch(o, pts, "season", SKINK, PEN_FINE, closed=True, over=0.0, amp=0.05, retrace=False, z=Z_LINE)
    for dx in (-0.8, 0.0, 0.8):
        sketch(o, [(x + dx * r, y - 0.8 * r), (x + dx * r - 0.35 * r, y - 1.8 * r)], "season", SITE_WATER_D, PEN_FINE,
               over=0.0, amp=0.02, retrace=False, z=Z_LINE)

def failsafe_mark(o, x, y, r=1.4):
    """v3: the fail-safe mark, an accent ring with a step and the water spilling over it."""
    ring = [(x + r * math.cos(6.283 * i / 20), y + r * math.sin(6.283 * i / 20)) for i in range(20)]
    sketch(o, ring, "fail-safe", ACCENT, PEN_FINE, closed=True, over=0.0, amp=0.05, retrace=False, z=Z_LINE)
    sketch(o, [(x - 0.75 * r, y + 0.3 * r), (x - 0.1 * r, y + 0.3 * r), (x - 0.1 * r, y - 0.45 * r), (x + 0.75 * r, y - 0.45 * r)],
           "fail-safe", SKINK, PEN_FINE, over=0.0, amp=0.03, retrace=False, z=Z_LINE)
    hand_arrow(o, (x - 0.55 * r, y + 0.55 * r), (x + 0.25 * r, y - 0.15 * r), ACCENT, width=0.16, head=0.55, bend=-0.3)

def keyed(o, kind, s, x, y, size_pt, colour=None, sub="text", mask=None):
    """v3: a keyword callout led by a hand pictogram at its first line: "winter" (cloud and rain), "summer" (the
    sun) or "failsafe". The text starts a little to the right of x."""
    h = size_pt * 0.353
    cx, cy = x + 1.1 * h, y + 0.36 * h
    if kind == "winter":
        cloud_rain(o, cx, cy + 0.15 * h, 0.5 * h)
    elif kind == "summer":
        sun(o, cx, cy, 0.36 * h)
    elif kind == "failsafe":
        failsafe_mark(o, cx, cy, 0.62 * h)
    text(o, s, x + 2.4 * h, y, size_pt, colour, sub, mask=mask)

def tick_dim(o, x, y0, y1, colour=INK2):
    """Sketch dimension: a vertical line with slashed ticks at both ends (example 4); no figure."""
    sketch(o, [(x, y0), (x, y1)], "dimensions", colour, LW_BEYOND, over=0.9, retrace=False, z=Z_LINE)
    for y in (y0, y1):
        sketch(o, [(x - 0.9, y - 0.9), (x + 0.9, y + 0.9)], "dimensions", colour, LW_EDGE, over=0.0, retrace=False, z=Z_LINE)

def sketch_ground(o, g, sub="ground"):
    """Ground: the board's poché, solid (a see-through ground shows the viewport through it and the band under the
    surface then reads as a gap, Nil 18 Oct 17:46), a slightly deeper band under the surface, and short earth strokes
    just under the line (the surface line itself: drawn by the caller)."""
    surf = g[1:-1]
    wash(o, g, sub, SEC_POCHE, None)
    floor = min(p[1] for p in g)
    for pc in band(surf, surf[0][0], surf[-1][0], 3.0):
        pc = [(x, max(floor, y)) for x, y in pc]           # never below the drawn ground (low-flow channel)
        if not _crosses(pc):
            wash(o, pc, sub, SEC_POCHE_BAND, None)
    rnd = _random.Random(_seed(surf[0][0], surf[-1][0], len(surf)))
    for (ax, ay), (bx, by) in zip(surf[:-1], surf[1:]):
        L = math.hypot(bx - ax, by - ay)
        if L < 3.0 or abs(bx - ax) < 0.5 * L:
            continue
        n = int(L / 3.2)
        for k in range(n):
            t = (k + 0.3 + 0.4 * rnd.random()) / n
            x, y = ax + (bx - ax) * t, ay + (by - ay) * t - 0.7
            sketch(o, [(x, y), (x - 1.1, y - 1.1)], sub + " hatch", INK2, LW_HATCH * 2, over=0.0, amp=0.05, retrace=False)
    return surf

def sketch_tree(o, x, y, h):
    """Loose tree: a crown of washes in the board's tree greens, a scribbled outline and a trunk with two limbs."""
    rnd = _random.Random(_seed(x, y, h))
    cx, cy, rx, ry = x, y + 0.64 * h, 0.36 * h, 0.30 * h
    ph = [rnd.uniform(0, 6.3) for _ in range(3)]
    crown = []
    for q in range(36):                                  # board _sa_lumpy
        a = 6.283 * q / 36
        k = 1.0 + 0.12 * (math.sin(5 * a + ph[0]) + 0.6 * math.sin(8 * a + ph[1]) + 0.4 * math.sin(13 * a + ph[2])) / 2.0
        crown.append((cx + math.cos(a) * rx * k, cy + math.sin(a) * ry * k))
    for (sx, sy, col, al) in ((0.0, 0.0, SITE_TREE[1], 0.55), (-0.18, 0.2, SITE_TREE[0], 0.5), (0.2, -0.22, SITE_TREE[2], 0.35)):
        part = [(cx + (px - cx) * 0.62 + sx * rx, cy + (py - cy) * 0.62 + sy * ry) for px, py in crown]
        wash(o, part if al < 0.55 else crown, "planting", col, al, z=Z_TREE)
    sketch(o, crown, "planting", SITE_TREE[2], LW_FINE, closed=True, over=0.0, amp=0.25, retrace=False, z=Z_TREE)
    sketch(o, [(x, y), (x + 0.15, cy - 0.1 * h)], "planting", SITE_TRUNK, LW_EDGE, over=0.0, retrace=False, z=Z_TREE)
    for s in (-1, 1):
        sketch(o, [(x + 0.1, cy - 0.25 * h), (x + s * 0.22 * h, cy + 0.05 * h)], "planting", SITE_TRUNK, LW_FINE,
               over=0.0, retrace=False, z=Z_TREE)

def sketch_person(o, x, y, h=4.5, kind=0, flip=False):
    """Board scale figure (SA_FIGS) at the drawing's figure height h."""
    s = h / 1.745
    sg = -1.0 if flip else 1.0
    if not PEOPLE:
        return
    fill(o, [(x + sg * bx * s, y + by * s) for bx, by in SA_FIGS[kind % len(SA_FIGS)]], "people", SITE_PEOPLE,
         alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)
    hx_, hy_, hr = SA_HEAD
    fill(o, [(x + sg * hx_ * s + hr * s * math.cos(6.283 * i / 12), y + hy_ * s + hr * s * math.sin(6.283 * i / 12))
             for i in range(12)], "people", SITE_PEOPLE, alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)

def sketch_house(o, x0, x1, y, wall=6.0, pipe=False):
    """Context: an old town house beyond the street (board TYPO "traditional": stone base, hipped tile roof, deep
    eaves), generic, not surveyed. pipe=True adds the downpipe that takes its roof water to the street."""
    ev, rise = 0.9, 2.6
    body = [(x0, y), (x1, y), (x1, y + wall), (x0, y + wall)]
    roof = [(x0 - ev, y + wall), (x1 + ev, y + wall), (x1 - 2.2, y + wall + rise), (x0 + 2.2, y + wall + rise)]
    wash(o, body, "context", HOUSE_WALL, 0.45)
    marker(o, roof, "context", HOUSE_ROOF, angle=-35.0, spacing=0.6, thick=0.5, alpha=0.45, base=0.25)
    sketch(o, body, "context", INK2, LW_FINE, closed=True)
    sketch(o, roof, "context", INK2, LW_FINE, closed=True)
    sketch(o, [(x0, y + 1.0), (x1, y + 1.0)], "context", INK2, LW_HATCH * 2, over=0.4, retrace=False)
    for wx in (x0 + 0.28 * (x1 - x0), x0 + 0.62 * (x1 - x0)):
        sketch(o, [(wx, y + 2.2), (wx + 1.3, y + 2.2), (wx + 1.3, y + 4.6), (wx, y + 4.6)], "context", INK2, LW_HATCH * 2,
               closed=True, over=0.3, retrace=False)
    if pipe:
        sketch(o, [(x1 + 0.6, y + wall), (x1 + 0.6, y + 0.3)], "context", SITE_WATER_D, LW_EDGE, over=0.0, retrace=False)

def rain(o, x0, x1, y0, y1, n=14):
    rnd = _random.Random(_seed(x0, x1, y0, y1))
    for _ in range(n):
        x, y = x0 + rnd.random() * (x1 - x0), y0 + rnd.random() * (y1 - y0)
        sketch(o, [(x, y), (x - 0.5, y - 1.6)], "rain", SITE_WATER_D, LW_FINE, over=0.0, amp=0.04, retrace=False)

def water_body(surface, xs, level):
    """The water standing at `level` around x = xs: from where the ground on the left rises through the level to
    where it does on the right (banks, walls, the low-flow channel), following the bed in between. So the water always
    meets its banks (Nil 18 Oct 17:55: the water did not meet the left bank)."""
    k = None
    for i, ((ax, ay), (bx, by)) in enumerate(zip(surface[:-1], surface[1:])):
        if ax != bx and min(ax, bx) <= xs <= max(ax, bx):
            y = ay + (by - ay) * (xs - ax) / (bx - ax)
            if y < level and (k is None or y < k[1]):
                k = (i, y)
    if k is None:
        return None

    def cross(p, q):                                  # p under the level, q at or over it
        if abs(q[1] - p[1]) < 1e-12:
            return (q[0], level)
        t = (level - p[1]) / (q[1] - p[1])
        return (p[0] + (q[0] - p[0]) * t, level)
    i = k[0]
    left, right = [], []
    j = i
    while j >= 0 and surface[j][1] < level:
        left.append(surface[j])
        j -= 1
    left.append(cross(left[-1] if left else (xs, k[1]), surface[j]) if j >= 0 else (surface[0][0], level))
    j = i + 1
    while j < len(surface) and surface[j][1] < level:
        right.append(surface[j])
        j += 1
    right.append(cross(right[-1] if right else (xs, k[1]), surface[j]) if j < len(surface) else (surface[-1][0], level))
    bed = left[::-1] + right
    out = []
    for p in bed:
        if not out or abs(p[0] - out[-1][0]) + abs(p[1] - out[-1][1]) > 1e-9:
            out.append(p)
    return out                                        # first and last point on the level, the bed between

def water_level(o, surface, xs, level, colour, bed_hatch=False, line=True):
    """Water at `level` around xs, cut exactly to the ground (solid), a hand surface line; bed_hatch: the board's blue
    hatch over the stream bed."""
    pts = water_body(surface, xs, level)
    if not pts or len(pts) < 3:
        return None
    fill(o, pts, "water", colour, boundary=False, hand_=False)
    if bed_hatch:
        hatch_lines(o, pts, "water", SEC_CHANNEL_HATCH, 1.1, 45.0, PEN_HAIR)
    if line:
        sketch(o, [pts[0], pts[-1]], "water lines", SITE_WATER_D, PEN_FINE, over=0.0, retrace=False, z=Z_LINE)
    return pts

def concept_aras_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_aras_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_aras_sketch():
    """PROBLEM: the bed is dry in summer, the winter runoff leaves the streets. MOVE: the bank becomes a cascade that
    holds the winter water, cleans it in reed basins and gives it back to the summer river."""
    o, w = ORIGIN, 200
    title(o, 82, "UPSTREAM ENTRY · collect, clean and hold · form " + FORM)
    g = [(0, 8), (0, 64), (34, 64), (34, 52), (68, 52), (68, 40), (102, 40), (102, 28), (130, 28)] + bank((130, 28), (140, 12))[1:] + \
        [(170, 12), (170, 28), (w, 28), (w, 8)]
    basins = ((40, 52), (74, 40), (108, 28))
    # the summer strip runs in a low-flow channel cut into the bed (v2.8: 150-160, 2.2 deep)
    gs = sketch_ground(o, notch(g, [(x0, x0 + 22, y, 5) for x0, y in basins] + [(150, 160, 12, 2.2)]))
    # winter: rain on the old town's roofs and street (context house generic, not surveyed)
    rain(o, 6, 33, 67.5, 73.5, 16)
    sketch_house(o, 15, 27, 65.3, wall=5.0, pipe=True)
    road(o, 0, 30, 64, "ROAD " + CITE("survey"), ly=61.5, mask=SOIL)
    # Q500's reach first (solid wash), so the basins' water and reeds stay on top of it
    for pc in [under_level(gs, 102, w, 31.5)]:
        if pc:
            wash(o, pc, "flood", FLOOD_WASH, FLOOD_ALPHA)
    # the move: the cascade of reed basins (marker band = what holds and cleans the water)
    for x0, y in basins:
        water_level(o, gs, x0 + 11, y - 0.4, W_WIN)
        reeds(o, x0 + 1, x0 + 21, y - 5, 3.2)
    for pc in band(gs, 34, 130, 1.6):
        marker(o, pc, "terraces", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    sketch_tree(o, 65, 52, 9); sketch_tree(o, 99, 40, 7)    # on the strips between the basins, above Q500's reach
    # summer: the river (dry bed today) gets the clean water back
    water_level(o, gs, 155, 19, W_WIN, bed_hatch=True)
    water_level(o, gs, 155, 12, W_EXT, line=False)
    sun(o, 188, 58)
    sketch_person(o, 13, 65.3, kind=1); sketch_person(o, 70.8, 40)               # never inside water or the Q500 reach
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    keyed(o, "winter", "winter flow", 172, 24, 5.6, W_EXT, "water")
    keyed(o, "summer", "low-flow strip\nregulated release\ntoday: dry bed", 172, 19, 5.6, W_EXT, "water")
    sketch(o, [(102, 31.5), (w, 31.5)], "flood lines", HERITAGE, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 123.8, 31.5, HERITAGE, "flood lines")
    # v3 fix (audit problem 3): the surveyed ARAS cut keeps Q500 inside the banks (rain_river_levels README v1.1
    # line 21); the lowest terrace floods only if it is set below that level
    text(o, "Q500 +73.66 m · 3.30 m · inside the banks " + CITE("levels") + "\nlowest terrace floods only if set below it",
         126, 35.6, 5.0, HERITAGE, "flood")
    hand_arrow(o, (8, 72), (44, 56), SITE_WATER_D, bend=0.12)
    keyed(o, "winter", "street + roof runoff · Nov-Feb 59.1 % of rain " + CITE("rain") + "\nreed basins clean it with stream water",
          6, 77.4, 5.8)
    hand_arrow(o, (126, 31), (150, 20), SITE_WATER_D, bend=-0.15)
    keyed(o, "summer", "regulated release · continuous strip\nJun-Sep 7.4 % of rain " + CITE("rain") + "\nstream below runs clean",
          109, 47, 5.8)
    for a, b in (((64, 49), (66, 44)), ((98, 37), (100, 32)), ((130, 26), (141, 18))):
        hand_arrow(o, a, b, ACCENT, width=0.4, head=1.5, bend=-0.2)
    keyed(o, "failsafe", "FAIL-SAFE\nfull basin: spills to the next\nlast basin: into the channel\nflood flow bypasses the reeds\ngravity · no pumps",
          2, 31, 5.8, ACCENT, mask=SOIL)
    text(o, "hold in winter,\ngive back in summer", 46, 21, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((2, 51, 56), (3, 65, 56), (4, 85, 44), (5, 143, 22), (6, 155, 24)):
        NODE(o, x_, y_, n_)

def concept_begum_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_begum_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_begum_sketch():
    """PROBLEM: the design flood runs over today's bank top. MOVE: the street level D is raised above it and the steps
    under it let the river climb: W wet every winter, F only in big floods, D never. K4 stays as it is."""
    o, w = (ORIGIN[0], ORIGIN[1] - 110), 200
    title(o, 82, "K4 BRIDGE · amphibious heritage threshold · form " + FORM)
    cx, cy = 120.0, 11.9                                           # the v2.8 arc through (98,14) (120,34) (142,14)
    r = math.hypot(98 - cx, 14 - cy)
    t0, t1 = math.atan2(14 - cy, 142 - cx), math.atan2(14 - cy, 98 - cx)
    arc = [(cx + r * math.cos(t0 + (t1 - t0) * i / 30.0), cy + r * math.sin(t0 + (t1 - t0) * i / 30.0)) for i in range(31)]
    sketch(o, arc, "K4 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)  # behind
    text(o, "K4 Roman bridge behind\nexisting · kept untouched", 104, 45, 5.4, INK2)
    g = [(0, 8), (0, 62), (40, 62), (40, 50), (62, 50), (62, 40), (84, 40), (84, 30), (90, 30)] + bank((90, 30), (100, 14))[1:] + \
        [(150, 14), (150, 62), (w, 62), (w, 8)]
    gs = sketch_ground(o, notch(g, [(118, 132, 14, 2.5)]))     # summer strip: low-flow channel (v2.8: 118-132, 2.5)
    wall = [(150, 14), (154, 14), (154, 62), (150, 62)]
    marker(o, wall, "wall", STONE, angle=45.0, spacing=0.55, thick=0.5, alpha=0.55, base=0.35)
    text(o, "east: existing channel wall kept\ndefault · Q1 " + CITE("concept"), 156, 65, 5.4)
    # the river climbing the steps: every winter (W), the design flood (F), never D
    fl = under_level(gs, 40, 150, 52)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 125, 33, W_WIN, bed_hatch=True)
    water_level(o, gs, 125, 14, W_EXT, line=False)
    keyed(o, "winter", "every winter: bed under water", 156, 31.8, 5.6, W_EXT, "water")
    keyed(o, "summer", "continuous strip · regulated\ntoday: dry, pools", 156, 15.3, 5.6, W_EXT, "water")
    for x0, x1, y, lab in ((0, 40, 62, "dry top · in use all year"), (40, 84, 50, "flood terraces · out of\nservice only in big floods"),
                           (84, 100, 30, "bed + lowest\nstep · wet\nin winter")):
        for pc in band(gs, x0, x1, 1.5):
            marker(o, pc, "tiers", SUN, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
        text(o, lab, x0 + 1, y - 3.0, 5.8, mask=SOIL)
    reeds(o, 102, 148, 14, 4.5)
    road(o, 0, 16, 62, "ROAD " + CITE("survey") + "\nK4 deck: traffic", ly=54.5, mask=SOIL)
    sketch_tree(o, 24, 62, 9)                               # only on D: F floods in big floods, W every winter
    sketch_person(o, 31, 62, kind=1); sketch_person(o, 35, 62, kind=2, flip=True); sketch_person(o, 195, 62)  # on dry D / east
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    sketch(o, wall, "wall lines", SKINK, PEN_BOLD, closed=True, z=Z_LINE)
    sketch(o, [(40, 52), (150, 52)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    tick_dim(o, 43, 52, 62, SKINK)                                                # D: raised clear of the flood
    hand_arrow(o, (138, 34.5), (138, 50.5), SITE_WATER_D, width=0.45, head=1.8)  # the river climbs in big floods
    level_mark(o, 146, 52, W_EXT, "flood lines")
    text(o, "Q500 over today's bank top\nK4 cut " + CITE("levels") + "\ndry top raised above it", 156, 51, 5.6, W_EXT, "water")
    text(o, "the stream may climb the steps,\nthe street stays above Q500", 6, 31, 8.0, SKINK, "idea")
    text(o, "tiers " + CITE("tiers") + ": level 1 floods yearly · 2 only in 10-year storms\n"
         "level 3 street: dry, only if set above Q500", 2, 5.5, 5.2, INK2)
    for n_, x_, y_ in ((6, 125, 18), (7, 110, 22), (8, 73, 44), (9, 6, 67)):
        NODE(o, x_, y_, n_)

'''

#@@ DETAIL_SRC
DETAIL_SRC = r'''import math
import os
import random
import tempfile
import time
import json
import zlib

VERSION = "bergama_detail_section v2 (2026-10-19)"
SCRIPT = "bergama_detail_section_v2.py"
SCALE = 75.0                         # 1:75
K = 1000.0 / SCALE                   # page mm per metre
PAGE_W, PAGE_H = 1189.0, 841.0       # A0 landscape; grown if the drawing needs more
FIGURES_IN_FLOOD_REACH = True        # Nil 19 Oct: people on the terraces below the Q500 line too (never in water)
OUT_NAME = "Bergama_detail_section_S4_seasons_1to75.pdf"   # one page per season

# ---------------------------------------------------------------- the cut (survey)
S4_ID = "54d75849-9e70-41b1-8760-c001a59940dd"
S4_A = (30616.354683, 30540.470648)
S4_B = (31489.513378, 31161.826317)
# ground along S4 (TIN of the survey, see header), every 0.25 m from s 520 to 700
PROFILE_S0, PROFILE_DS = 520.0, 0.25
PROFILE_Z = [47.40, 47.40, 47.39, 47.39, 47.39, 47.38, 47.38, 47.37, 47.37, 47.36, 47.36, 47.35, 47.35, 47.34, 47.34, 47.33, 47.33, 47.32, 47.32, 47.32, 47.31, 47.31, 47.30, 47.30, 47.29, 47.29, 47.28, 47.28, 47.27, 47.27, 47.26, 47.26, 47.25, 47.25, 47.25, 47.24, 47.24, 47.23, 47.23, 47.22, 47.22, 47.21, 47.21, 47.20, 47.20, 47.19, 47.19, 47.18, 47.18, 47.18, 47.17, 47.17, 47.16, 47.16, 47.15, 47.15, 47.14, 47.14, 47.13, 47.13, 47.13, 47.13, 47.13, 47.12, 47.12, 47.12, 47.12, 47.12, 47.11, 47.11, 47.11, 47.11, 47.11, 47.11, 47.10, 47.10, 47.10, 47.10, 47.10, 47.10, 47.10, 47.09, 47.09, 47.09, 47.09, 47.09, 47.09, 47.09, 47.09, 47.09, 47.10, 47.10, 47.10, 47.10, 47.11, 47.11, 47.11, 47.12, 47.12, 47.12, 47.12, 47.13, 47.13, 47.13, 47.14, 47.14, 47.14, 47.14, 47.15, 47.15, 47.15, 47.15, 47.16, 47.16, 47.16, 47.17, 47.16, 47.16, 47.15, 47.14, 47.14, 47.13, 47.12, 47.11, 47.11, 47.10, 47.09, 47.09, 47.08, 47.07, 47.07, 47.06, 47.06, 47.06, 47.06, 47.06, 47.06, 47.07, 47.08, 47.09, 47.10, 47.11, 47.12, 47.13, 47.14, 47.15, 47.16, 47.17, 47.18, 47.19, 47.20, 47.21, 47.22, 47.23, 47.24, 47.25, 47.26, 47.27, 47.29, 47.30, 47.31, 47.32, 47.34, 47.35, 47.37, 47.39, 47.38, 47.36, 47.34, 47.31, 47.29, 47.27, 47.25, 47.23, 47.21, 47.19, 47.17, 47.14, 47.10, 47.07, 47.04, 47.00, 46.97, 46.94, 46.90, 46.87, 46.83, 46.80, 46.77, 46.73, 46.70, 46.67, 46.63, 46.60, 46.56, 46.53, 46.50, 46.46, 46.43, 46.40, 46.36, 46.33, 46.29, 46.26, 46.23, 46.19, 46.15, 46.12, 46.08, 46.03, 45.93, 45.84, 45.75, 45.65, 45.56, 45.47, 45.37, 45.28, 45.19, 45.09, 45.00, 44.91, 44.81, 44.72, 44.63, 44.53, 44.44, 44.35, 44.25, 44.16, 44.06, 44.04, 44.03, 44.02, 44.01, 44.01, 44.00, 43.99, 43.98, 43.98, 43.97, 43.96, 43.95, 43.95, 43.94, 43.93, 43.92, 43.92, 43.91, 43.90, 43.89, 43.89, 43.88, 43.87, 43.86, 43.86, 43.85, 43.84, 43.83, 43.83, 43.82, 43.81, 43.80, 43.80, 43.79, 43.78, 43.77, 43.77, 43.76, 43.75, 43.74, 43.74, 43.73, 43.72, 43.71, 43.71, 43.70, 43.69, 43.68, 43.68, 43.67, 43.66, 43.65, 43.65, 43.64, 43.63, 43.62, 43.61, 43.59, 43.59, 43.60, 43.61, 43.62, 43.63, 43.64, 43.66, 43.67, 43.68, 43.69, 43.70, 43.71, 43.72, 43.73, 43.74, 43.75, 43.77, 43.78, 43.79, 43.80, 43.81, 43.82, 43.83, 43.84, 43.85, 43.87, 43.88, 43.89, 43.90, 43.91, 43.92, 43.93, 43.94, 43.95, 43.97, 43.98, 43.99, 44.00, 44.01, 44.02, 44.03, 44.04, 44.05, 44.07, 44.08, 44.09, 44.10, 44.11, 44.12, 44.13, 44.14, 44.15, 44.17, 44.18, 44.19, 44.20, 44.21, 44.22, 44.23, 44.24, 44.25, 44.26, 44.27, 44.28, 44.29, 44.30, 44.31, 44.32, 44.33, 44.34, 44.35, 44.36, 44.37, 44.38, 44.39, 44.40, 44.41, 44.42, 44.43, 44.44, 44.45, 44.46, 44.47, 44.48, 44.48, 44.49, 44.49, 44.49, 44.50, 44.50, 44.51, 44.51, 44.51, 44.52, 44.52, 44.53, 44.53, 44.53, 44.54, 44.54, 44.54, 44.55, 44.55, 44.56, 44.56, 44.56, 44.57, 44.57, 44.58, 44.58, 44.58, 44.61, 44.73, 44.84, 44.96, 45.07, 45.19, 45.30, 45.42, 45.53, 45.64, 45.64, 45.64, 45.64, 45.64, 45.64, 45.64, 45.63, 45.63, 45.63, 45.63, 45.63, 45.63, 45.63, 45.63, 45.63, 45.62, 45.62, 45.62, 45.62, 45.62, 45.62, 45.62, 45.62, 45.62, 45.61, 45.61, 45.61, 45.64, 45.66, 45.69, 45.72, 45.75, 45.77, 45.80, 45.83, 45.86, 45.89, 45.91, 45.94, 45.97, 46.00, 45.96, 45.91, 45.86, 45.83, 45.83, 45.83, 45.83, 45.83, 45.83, 45.84, 45.84, 45.85, 45.85, 45.86, 45.86, 45.87, 45.87, 45.88, 45.89, 45.89, 45.90, 45.90, 45.91, 45.91, 45.92, 45.92, 45.93, 45.93, 45.94, 45.94, 45.95, 45.95, 45.96, 45.96, 45.97, 45.97, 45.98, 45.98, 45.99, 45.99, 46.00, 46.01, 46.02, 46.03, 46.05, 46.06, 46.07, 46.08, 46.09, 46.10, 46.11, 46.13, 46.14, 46.15, 46.16, 46.17, 46.18, 46.19, 46.21, 46.22, 46.23, 46.24, 46.25, 46.26, 46.27, 46.28, 46.30, 46.31, 46.32, 46.33, 46.34, 46.35, 46.36, 46.37, 46.38, 46.39, 46.40, 46.41, 46.42, 46.43, 46.44, 46.45, 46.46, 46.47, 46.48, 46.49, 46.50, 46.51, 46.52, 46.53, 46.54, 46.55, 46.56, 46.57, 46.57, 46.58, 46.58, 46.58, 46.58, 46.57, 46.57, 46.56, 46.56, 46.56, 46.55, 46.55, 46.55, 46.54, 46.54, 46.54, 46.53, 46.53, 46.52, 46.52, 46.52, 46.52, 46.52, 46.53, 46.53, 46.53, 46.54, 46.54, 46.54, 46.54, 46.55, 46.55, 46.55, 46.56, 46.56, 46.56, 46.57, 46.57, 46.57, 46.58, 46.58, 46.58, 46.59, 46.59, 46.59, 46.59, 46.60, 46.60, 46.60, 46.61, 46.61, 46.61, 46.62, 46.62, 46.62, 46.63, 46.63, 46.63, 46.64, 46.63, 46.63, 46.62, 46.61, 46.60, 46.59, 46.59, 46.58, 46.56, 46.55, 46.54, 46.52, 46.51, 46.50, 46.48, 46.47, 46.46, 46.44, 46.43, 46.42, 46.40, 46.39, 46.38, 46.36, 46.35, 46.34, 46.33, 46.31, 46.30, 46.29, 46.27, 46.26, 46.25, 46.23, 46.24, 46.25, 46.26, 46.28, 46.29, 46.31, 46.32, 46.33, 46.35, 46.36, 46.38, 46.39, 46.40, 46.42, 46.43, 46.45, 46.46, 46.47, 46.48, 46.49, 46.49, 46.50, 46.51, 46.52, 46.53, 46.53, 46.54, 46.55, 46.56, 46.57, 46.58, 46.58, 46.59, 46.60, 46.61, 46.62, 46.62, 46.63, 46.64, 46.65, 46.66, 46.66, 46.67, 46.68, 46.69, 46.70, 46.70, 46.71, 46.72, 46.73, 46.74, 46.75, 46.75, 46.76, 46.77, 46.78, 46.79, 46.79, 46.80, 46.82, 46.83, 46.84, 46.84, 46.84, 46.84, 46.83, 46.83, 46.83, 46.83, 46.82, 46.82, 46.82, 46.81, 46.81, 46.81, 46.81, 46.80, 46.80, 46.80, 46.80, 46.80, 46.79, 46.79]
SURVEY_MARKS = [   # (s, what, z or None): crossings of survey lines with S4 and spot heights within 4 m of it
    (549.48, "railing (SINIR_PARMAKLIK)", None),
    (561.86, "bank top (SEV_UST)", None),
    (570.97, "bank toe (SEV_ALT)", None),
    (619.95, "bank toe (SEV_ALT)", None),
    (626.06, "road edge (YOL_SOSE)", None),
    (629.99, "road edge (YOL_SOSE)", None),
    (555.05, "spot height", 46.84),
    (561.93, "spot height", 47.45),
    (571.12, "spot height", 46.21),
    (592.03, "spot height", 43.58),
    (633.49, "spot height", 45.80),
]
THALWEG = (592.03, 43.59)           # lowest ground on the cut (TIN), the bed's low point
Q100, Q500 = 45.84, 46.19           # v1.1: calculated on the surveyed cross-section at this cut (water board W2 note)
STRIP = (590.0, 594.0, 0.30)        # summer water strip: s from, s to, depth (design, case.md section 4)
DRY = 47.60                         # raised walk / promenade / balcony level (design; 1.41 m above Q500 since v1.1)

# ---------------------------------------------------------------- the four seasons (one page each)
# Climate per season: case.md section 1 (rain = WMO normals 1991-2020, MGM 17742, measured; open-water evaporation =
# Hargreaves x 1.05, calculated). River depths: case.md L13-L15 and section 3 (DSI gauges D04A053 Ilica + D04A063 Komurcu,
# WY2016-2021, area-scaled to the Selinos, Manning n 0.050). v1.1: the depths are this cut's own, on its surveyed
# cross-section (rain_river_levels/tables/A3s_*, A4s_*), above its bed low point (+43.59). Operating modes and life on the bands: Selinos riverfront
# design concept v1 (concept/Selinos_riverfront_design_concept_v1.md sections 5.4 and 10.1): DESIGN, ASSUMED/PROVISIONAL.
# water: (level, fill?, label, dash or None) - filled = the water body drawn; not filled = a level line only.
SEASONS = [
    dict(key="winter", name="WINTER", months="DEC - FEB", mode="WINTER · the river runs, storage fills",
         climate=["Rain 285.2 mm (46.0 % of 619.6 mm), 25.1 rain days, mean 7.6 C (measured, WMO 1991-2020).",
                  "Rain minus open-water evaporation +178.7 mm: the only surplus season (calculated, case.md s.1)."],
         river=["Jan-Feb monthly mean up to 0.43 m above the bed on this cut (calculated): +%.2f drawn." % (THALWEG[1] + 0.43),
                "Highest day 2016-2021, 6 Jan 2017: 1.15 m on this cut (calculated): +%.2f line." % (THALWEG[1] + 1.15),
                "Winter water goes into storage (Dec-Apr carries 89 % of the flow, calculated, rain_river README s.0)."],
         life=["Bed: flood channel, viewing only. Marsh: flooded, bird habitat. Terraces open between",
               "storms (concept s.10.1, design). People watch the river from the terrace edges and the balcony."],
         plants="Plane tree bare with its seed balls; reeds cut back after October; iris resting; lavender mound evergreen.",
         water=[(THALWEG[1] + 0.43, True, "Jan-Feb mean %+.2f (0.43 m)", None),
                (THALWEG[1] + 1.15, False, "highest day 6 Jan 2017 %+.2f (1.15 m)", [1.6, 0.6, 0.3, 0.6])],
         strip_held=False,
         people={"1": [(546.6, 0, True), (553.2, 3, False), (556.4, 4, True), (563.4, 1, False), (569.4, 4, False),
                       (570.5, 3, False)],
                 "2": [(647.6, 0, False), (640.6, 1, False), (627.0, 1, False), (618.2, 3, True), (604.4, 4, True),
                       (606.6, 11, True)]},
         bikes={"1": [], "2": [(650.6, True)]}),
    dict(key="spring", name="SPRING", months="MAR - MAY", mode="SPRING · the river runs, storage full by the end of April",
         climate=["Rain 148.6 mm (24.0 %), 17.2 rain days, mean 15.0 C (measured, WMO 1991-2020).",
                  "Rain minus open-water evaporation -207.5 mm: the deficit starts (calculated, case.md s.1)."],
         river=["Jan-Apr monthly means 0.25-0.43 m above the bed on this cut (calculated): Mar-Apr drawn at the",
                "low end 0.25 m (+%.2f), the high end as a line; May 0.16-0.21 m (calculated)." % (THALWEG[1] + 0.25),
                "The strip runs on the river while there is enough flow; storage tops up (design, water loop)."],
         life=["Strip and bed with water again. Marsh greens up, boardwalk open; flowering",
               "meadow and play (concept s.10.1, design). Children and parents at the water's edge."],
         plants="Fresh leaves; reeds green up from the cut stubble; yellow iris and lavender in flower.",
         water=[(THALWEG[1] + 0.25, True, "Mar-Apr, low end of the range %+.2f (0.25 m)", None),
                (THALWEG[1] + 0.43, False, "high end of the Jan-Apr range %+.2f (0.43 m)", [0.4, 0.6])],
         strip_held=True,
         people={"1": [(538.9, 2, False), (546.6, 0, True), (547.6, 1, False), (553.2, 3, False), (555.6, 0, False),
                       (563.0, 1, True), (564.2, 3, False), (569.6, 4, False), (580.2, 3, False), (582.6, 4, False),
                       (583.4, 7, False)],
                 "2": [(647.6, 0, False), (646.4, 2, True), (640.6, 1, False), (635.0, 2, False), (630.0, 0, True),
                       (618.2, 3, True), (599.4, 7, True), (601.0, 11, True), (604.0, 2, True)]},
         bikes={"1": [(543.0, False)], "2": [(650.6, True)]}),
    dict(key="summer", name="SUMMER", months="JUN - AUG", mode="SUMMER · the strip runs on stored water",
         climate=["Rain 28.5 mm (4.6 %), 5.9 rain days, mean 26.5 C (measured, WMO 1991-2020).",
                  "Rain minus open-water evaporation -552.2 mm: the deepest deficit (calculated, case.md s.1)."],
         river=["Natural river Jul-Sep: monthly means 0.04-0.11 m on this cut, a trickle (calculated, indicative: bed",
                "interpolated); bed dry (< 2 cm) about 11 days a year. Drawn: the continuous regulated water strip 400 cm × 0.30 m, topped up from",
                "storage and flowing one way downstream (design, case.md s.4; Aras 17 Oct 22:01, 19 Oct 07:43)."],
         life=["All bands open; the strip used: wading at 0.30 m, cooling, evening lights; dry meadow",
               "as a lie-down lawn (concept s.10.1, design). People sit at the strip edge with their feet in the water."],
         plants="Full leaf; reeds at full height, first plumes; iris in leaf; last lavender spikes; meadow drying.",
         water=[],
         strip_held=True,
         people={"1": [(538.9, 2, False), (546.6, 0, True), (547.6, 1, False), (553.2, 3, False), (555.6, 0, False),
                       (556.4, 4, True), (563.0, 1, True), (564.2, 3, False), (581.5, 9, False), (585.6, 10, False),
                       (588.2, 7, False), (589.85, 8, False)],
                 "2": [(647.6, 0, False), (646.4, 2, True), (640.6, 1, False), (635.0, 2, False), (630.0, 0, True),
                       (627.0, 1, False), (618.2, 3, True), (594.15, 8, False), (595.6, 7, True), (597.4, 4, True),
                       (600.5, 3, True)]},
         bikes={"1": [(543.0, False)], "2": [(650.6, True)]}),
    dict(key="autumn", name="AUTUMN", months="SEP - NOV", mode="AUTUMN · storage low until the rains return",
         climate=["Rain 157.3 mm (25.4 %), 14.1 rain days, mean 17.7 C (measured, WMO 1991-2020).",
                  "Rain minus open-water evaporation -102.5 mm; Nov turns to surplus (calculated, case.md s.1)."],
         river=["Sep 0.05-0.07 m; Oct-Dec monthly means 0.11-0.20 m above the bed on this cut (calculated):",
                "the high end 0.20 m drawn (+%.2f). Design storm 137 mm in one day" % (THALWEG[1] + 0.20),
                "(28 Oct 2025, municipal figure, not MGM-confirmed). The strip runs on the river again after the first storms."],
         life=["First-flush cleaning and maintenance of the strip; marsh seed heads, cut back after October;",
               "events on the meadow after the reset (concept s.10.1, design). People walk the gravel bed to the water."],
         plants="Plane leaves turning; reeds gold with seed heads; iris leaves yellowing; lavender trimmed.",
         water=[(THALWEG[1] + 0.20, True, "Oct-Dec high end %+.2f (0.20 m)", None)],
         strip_held=True,
         people={"1": [(538.9, 2, False), (547.6, 1, False), (553.2, 3, False), (556.4, 4, True), (563.0, 1, True),
                       (569.6, 3, False), (582.0, 2, False), (586.4, 0, False), (588.4, 4, False)],
                 "2": [(647.6, 0, False), (640.6, 1, False), (630.0, 0, True), (618.2, 3, True), (595.4, 3, True),
                       (597.8, 2, True), (602.0, 0, True)]},
         bikes={"1": [(543.0, False)], "2": [(650.6, True)]}),
]
DAYS_WET = "Days a year at or above each height on this cut (mean WY2016-2021, calculated): " \
           "0.10 m 278 d, 0.30 m 69 d, 0.50 m 9 d, 1.00 m under 1 d; bed dry (< 2 cm) about 11 d."

# ---------------------------------------------------------------- the design (all design values)
# surfaces: (s from, s to, level, material, swatch label) left to right as drawn
SECTIONS = [
    dict(key="1", title="SECTION 1-1'", side="SOUTH-WEST BANK", s_from=538.0, s_to=598.0, look="looking north-west (upstream)",
         surfaces=[(538.0, 542.0, 47.15, "veg", "Native vegetation"),
                   (542.0, 544.0, 47.15, "asphalt", "Coloured asphalt"),
                   (544.0, 548.0, 47.15, "concrete", "Concrete walkway"),
                   (548.0, 551.0, 47.20, "lavender", "Lavender bed"),
                   (551.0, 554.0, DRY, "concrete", "Concrete walkway"),
                   (554.0, 557.0, 46.70, "deck", "Wooden deck"),
                   (557.0, 561.0, 45.80, "veg", "Native vegetation"),
                   (561.0, 565.0, 44.90, "deck", "Wooden deck"),
                   (565.0, 571.0, 44.20, "veg", "Native vegetation")],
         regrade=(571.0, 578.0),            # gravel slope from the last terrace down to the existing bed
         band_more=[(571.0, 590.0, "gravel", "Stream gravel"), (590.0, 594.0, "water", "Summer water strip")],
         rails=[(554.0, -1), (565.0, -1)],   # (s, side of the post: -1 = just left of s) single posts at edges
         trees=[(541.0, 3.9, 7.5, "plane")],
         shrubs=[(558.2, 1.3, 1.1), (559.9, 1.5, 1.2), (566.3, 1.7, 1.4), (568.2, 1.9, 1.5), (570.0, 1.5, 1.2)],
         grass=[(538.0, 542.0), (557.0, 561.0), (565.0, 571.0)],
         lavender=[(548.2, 550.8)],
         reeds=[(573.5, 576.5, 1.9), (580.0, 588.5, 2.2), (595.0, 598.0, 2.0)],
         iris=[(576.5, 580.0), (588.5, 589.6)],
         callouts=[(540.0, None, "Oriental plane (Doğu çınarı)"),
                   (543.0, None, "Bike way"),
                   (546.0, None, "Concrete walkway"),
                   (549.5, None, "French lavender (Karabaş otu)"),
                   (552.4, None, "Raised walk +47.60 above Q500"),
                   (553.85, DRY + 1.10, "Handrail corten steel"),
                   (555.5, None, "Multilevel walkway platforms"),
                   (559.0, None, "Flood- and drought-tolerant planting"),
                   (563.2, None, "Floodable boardwalk, open deck"),
                   (567.0, None, "Tamarisk (Ilgın)"),
                   (569.5, None, "Chaste tree (Hayıt)"),
                   (578.2, None, "Yellow flag iris (Sarı süsen)"),
                   (584.0, None, "Common reed (Kamış)"),
                   (592.0, None, "Summer water strip 400 cm × 0.30 m")]),   # v4 (MIRAQUA 28 Oct, G13 / P15.1)
    dict(key="2", title="SECTION 2-2'", side="NORTH-EAST BANK", s_from=652.0, s_to=588.0, look="looking south-east (downstream)",
         surfaces=[(652.0, 649.0, DRY, "asphalt", "Coloured asphalt"),
                   (649.0, 645.0, DRY, "concrete", "Concrete walkway"),
                   (645.0, 642.0, DRY, "veg", "Native vegetation"),
                   (642.0, 638.0, DRY, "concrete", "Concrete walkway"),
                   ("steps", 638.0, 633.5, DRY, 45.35, 5, "concrete", "Concrete steps"),
                   (633.5, 622.5, 45.35, "concrete", "Concrete walkway")],
         regrade=(622.5, 619.95),
         band_more=[(619.95, 594.0, "gravel", "Stream gravel"), (594.0, 590.0, "water", "Summer water strip")],
         rails=[],
         balcony=dict(s0=638.0, s1=617.0, top=DRY, thick=0.35, columns=(631.0, 624.0)),
         pergola=dict(posts=(649.6, 645.4), plates=[(650.6, 644.6, 3.20), (648.4, 643.2, 3.55)]),
         trees=[(643.5, 3.9, 7.5, "plane")],
         shrubs=[(644.5, 1.0, 0.8), (642.4, 0.9, 0.7), (621.3, 1.2, 1.0)],
         grass=[(645.0, 642.0), (622.5, 619.95)],
         lavender=[],
         reeds=[(619.5, 612.0, 2.2), (607.0, 600.0, 1.9)],
         iris=[(612.0, 609.0), (596.5, 595.0)],
         callouts=[(650.5, None, "Bike way"),
                   (648.0, DRY + 3.55, "Shading structures"),
                   (646.4, None, "Walkway"),
                   (643.5, None, "Oriental plane (Doğu çınarı)"),
                   (640.0, None, "Promenade +47.60 above Q500"),
                   (636.0, None, "Amphitheatre toward the stream"),
                   (628.0, None, "Floodable lower walk"),
                   (625.0, DRY + 1.10, "Handrail corten steel"),
                   (619.0, DRY, "Balcony towards the stream (beyond the cut)"),
                   (624.0, 46.40, "Column support"),
                   (615.0, None, "Common reed (Kamış)"),
                   (610.5, None, "Yellow flag iris (Sarı süsen)"),
                   (592.0, None, "Summer water strip 400 cm × 0.30 m")]),   # v4 (MIRAQUA 28 Oct, G13 / P15.1)
]

# ---------------------------------------------------------------- colours (reference language)
INK = "1E1E1E"
INK2 = "5A5A5A"
GREY = "8C8C8C"
DIM = "D0342C"            # the reference's red dimension strings
STIPPLE = "6E6E6E"
CONCRETE = "E3E2DE"
CONCRETE_DOT = "9A9893"
ASPHALT = "A5473C"
DECK = "C8A27A"
DECK_DARK = "8A6A48"
CORTEN = "6B4A36"
WATER = "CFE6F1"
WATER_LINE = "7DB3D3"
FLOOD = "3F86B8"
FIG = "3B3B3B"             # the reference's figure grey-black
GREEN_LINE = "8DAA5C"
GREEN_FILL = "D3E3B1"
REED = "A7A57C"
REED_HEAD = "B49A6C"
LAV = "9F86C0"
IRIS = "6E8F4A"
IRIS_FLOWER = "D9B640"
TEAL = "107C73"           # NIL working area (scripts/study_area_style.md)
TREE_STYLE_REF = dict(dark="9FBA6E", mid="BCD192", light="DCE8C0", trunk="7B8B57", shadow="9FBA6E", shadow_a=0.0,
                      lobes=2.6, blob=0.55)   # the reference's light green, through the v1.8 tree: finer clusters


# ================================================================ traced entourage from Nil's reference
ASSET_B64 = (
    "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"
    "6bxEbtLyZoncRNRLuprnv9qXbycvMSxca+peON5dWx8xLEaJWkHE1mcMi4H4HU14+ZvWFOm8ROzQ8uafGB2t1NNLG25B+w96/C671GaXmirDfc"
    "bCGCU6yyiRW4bGtEA6K3laKc+kpkznkuf8Ew2mlWgwrdTTSxtuQfsPEpYERHJKNCTyeolvnmzwEdGH6JQvb8nFJTqUlfIS3fKlSy7jTwShViII"
    "tVJPL224Be0/6LX+CL8/0ZVbGv0zGuJTEK2CRsmlS0z6htvdLugW5JLuljxvKT3RLelc8uzI0wraBc2Cxj964i9S/kbXe3dGFwhGQy+sjA7uw1"
    "3QLcglnZc8vZSX6JZ0XljspTxBo6Be0tU8/9U+vpvlX6DB12m2Ijjf+W7eBd2CpPXBRl/e1Civa02RzuW93bS8U9/UTXlUrLz9Jc9/tW//4Wre"
    "hT94FnbmIazH5GreBZ2CbkknTOePVwrlJbrlS5dcyGy8Cxr/t6zHt6D9B2XrO3mA/y8YoE9B+5/s0E0YoP9/c0Xvgm5BLulGyXP8Kd1LPa2wWP"
    "+L09r/oIwFMMmXHLzOExzMQ/iZkw/VhYN+6Lsx+HSJjrA1r8LkvMAlfwvHtBW0CuN0rWeit3vt4FXdwm08wJ78+Fi7cCmTBXkXdAtySWclTyvl"
    "JbolnUues5RHNArqJV3N81/t24iv+dhSd+FcHYy2CQ7dHoy6GUV9F3QLckk3Sp6jlDeUsRjpXPLspTyiUVD/B2/sLWj/QclSRI48oiH8QhfcPK"
    "Pwse6CKlerS7pe8uylvES3pPPCMNv+ySk7Cur/4JS9Be0/SOIN579Ag7L4bMXTYwpr5S6oMlpK6+8uee5S3taaIp1Lnl7Kc/EmVNRLuprnv9qX"
    "r5xeGPt6YZTrws6YnEn0BdgF3YKEydBHyXP8YQhswt+X6VzyvKU8olFQL+lqnv9qn/q5/LimtjC1US/ehf3tMV1NaFd2Qbcgl3Sz5DlLeYluSe"
    "eS5yrlLfE0UdRLuprnv9q3VdOTbHdAounZQzU9wuK2/8HpJpoepDslz1PKS3RLOtH07FnKKxFVBfV/cM/dgvYfpLteL7tCL7teL7teL7tQ5VHr"
    "ZdfrZdfrZdfrZdfrZdfrZdcbpbxRdr1Rdr1edr2/PHH7D0pL8/YxSsk6XPSzfFxinUydYB0bykT1h59sBFeaMIshz1nKS3RLOuE8203LEzQK6i"
    "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"
    "Q="
)
PX_PER_M = 46.0 / 1.75              # the reference's adult walker: 46 px tall = 1.75 m
_ASSETS = []


def assets():
    if not _ASSETS:
        import base64
        _ASSETS.append(json.loads(zlib.decompress(base64.b64decode("".join(ASSET_B64))).decode("utf-8")))
    return _ASSETS[0]


def draw_asset(pg, key, X, Y, height_mm=None, flip=False, layer="entourage", tone=None):
    """A traced asset with its anchor (feet / base) at page (X, Y). height_mm None = the reference's own size at
    1:75; tone = one colour for every layer (None = the traced colours)."""
    A = assets()[key]
    ax, ay = A["anchor"]
    h0 = A["bbox"][3] - A["bbox"][1]
    s = (height_mm / h0) if height_mm else K / PX_PER_M
    fx = -1.0 if flip else 1.0
    for fill, op, loops in A["layers"]:
        rings = [[(X + fx * (x - ax) * s, Y + (ay - y) * s) for x, y in loop] for loop in loops]
        pg.poly(rings, fill=tone or fill, stroke=None, layer=layer, alpha=op)


# ================================================================ reused blocks (copied unchanged from bergama_diagrams_v1_8.py)
# ============================================================ TEXT METRICS (Helvetica = Arial metrics)
_MCH = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ\xa0¡¢£¤¥¦§¨©ª«¬\xad®¯°±²³´µ¶·¸¹º»¼½¾¿ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿĞğİıŞş'
_MW0 = [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 278, 278, 584, 584, 584, 556, 1015, 667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 278, 278, 278, 469, 556, 333, 556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500, 334, 260, 334, 584, 556, 222, 556, 333, 1000, 556, 556, 333, 1000, 667, 333, 1000, 611, 222, 222, 333, 333, 350, 556, 1000, 333, 1000, 500, 333, 944, 500, 667, 278, 333, 556, 556, 556, 556, 260, 556, 333, 737, 370, 556, 584, 333, 737, 552, 400, 549, 333, 333, 333, 576, 537, 333, 333, 333, 365, 556, 834, 834, 834, 611, 667, 667, 667, 667, 667, 667, 1000, 722, 667, 667, 667, 667, 278, 278, 278, 278, 722, 722, 778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722, 667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 500, 556, 556, 556, 556, 278, 278, 278, 278, 556, 556, 556, 556, 556, 556, 556, 549, 611, 556, 556, 556, 556, 500, 556, 500, 778, 556, 278, 278, 667, 500]
_MW1 = [278, 333, 474, 556, 556, 889, 722, 238, 333, 333, 389, 584, 278, 333, 278, 278, 556, 556, 556, 556, 556, 556, 556, 556, 556, 556, 333, 333, 584, 584, 584, 611, 975, 722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611, 333, 278, 333, 584, 556, 333, 556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500, 389, 280, 389, 584, 556, 278, 556, 500, 1000, 556, 556, 333, 1000, 667, 333, 1000, 611, 278, 278, 500, 500, 350, 556, 1000, 333, 1000, 556, 333, 944, 500, 667, 278, 333, 556, 556, 556, 556, 280, 556, 333, 737, 370, 556, 584, 333, 737, 552, 400, 549, 333, 333, 333, 576, 556, 333, 333, 333, 365, 556, 834, 834, 834, 611, 722, 722, 722, 722, 722, 722, 1000, 722, 667, 667, 667, 667, 278, 278, 278, 278, 722, 722, 778, 778, 778, 778, 778, 584, 778, 722, 722, 722, 722, 667, 667, 611, 556, 556, 556, 556, 556, 556, 889, 556, 556, 556, 556, 556, 278, 278, 278, 278, 611, 611, 611, 611, 611, 611, 611, 549, 611, 611, 611, 611, 611, 556, 611, 556, 778, 611, 278, 278, 667, 556]
_W = [dict(zip(_MCH, _MW0)), dict(zip(_MCH, _MW1))]
PT = 25.4 / 72.0                      # mm per point
CAP = 0.716                           # cap height / em (Arial, Helvetica)


def text_w(s, size_mm, bold=False):
    w = _W[1 if bold else 0]
    return sum(w.get(c, 556) for c in s) / 1000.0 * size_mm


def area2(P):
    return sum(P[i][0] * P[(i + 1) % len(P)][1] - P[(i + 1) % len(P)][0] * P[i][1] for i in range(len(P))) / 2.0


def pip(x, y, P):
    c = False
    j = len(P) - 1
    for i in range(len(P)):
        if (P[i][1] > y) != (P[j][1] > y) and x < (P[j][0] - P[i][0]) * (y - P[i][1]) / (P[j][1] - P[i][1]) + P[i][0]:
            c = not c
        j = i
    return c
# ============================================================ PAGE (vector items in mm, y up)
class Page(object):
    def __init__(self, pid, title):
        self.pid, self.title, self.items = pid, title, []

    def poly(self, rings, fill=None, stroke=None, lw=0.1, dash=None, layer="drawing", join=1, stripes=None, alpha=None):
        """alpha: opacity 0-1 of fill and stroke (PDF only, in steps of 0.05; None = opaque)."""
        rings = [r for r in rings if len(r) >= 3]
        if rings:
            self.items.append(("poly", rings, fill, stroke, lw, dash, layer, join, stripes, alpha))

    def line(self, pts, stroke, lw=0.1, dash=None, layer="drawing", cap=1):
        if len(pts) >= 2:
            self.items.append(("line", pts, stroke, lw, dash, layer, cap))

    def circle(self, cx, cy, r, fill=None, stroke=None, lw=0.1, layer="drawing"):
        self.items.append(("circle", cx, cy, r, fill, stroke, lw, layer))

    def text(self, s, x, y, size, color, bold=False, align="L", layer="text", mat=None, halo=None):
        """size = em in mm; align L, C or R on the baseline; mat = 2 x 2 text matrix (columns: text x and y axes per
        mm of em) for words lying in a drawing plane."""
        if s:
            self.items.append(("text", s, x, y, size, color, bold, align, layer, mat, halo))


# ============================================================ TREES (self-contained: copy this block as it is)
# Trees in the style of Nil's reference (18 Oct 2026: an isometric water-system diagram with layered, see-through
# canopies), drawn as architectural entourage (fine branches, translucent leaf clusters), not as cartoon blobs. Needs only `math` and a page object with
#     poly(rings, fill=hex, stroke=hex or None, lw=mm, layer=str, alpha=0-1 or None)   rings: [[(X, Y), ...], ...]
#     line(pts, stroke_hex, lw_mm, layer=str)
# draw_tree(pg, P, k, x, y, r, top, style) draws one tree: P(x, y, z) -> page (X, Y) in mm for a parallel
# (orthographic) view with z up, k = page mm per model metre. Light comes from the upper left of the page, as on the
# buildings. Size and height are the data's: crown radius r and top height `top` (m above the ground); the crown starts
# at TREE_CROWN_LO(top), the analyses' convention in selinus_board (crown_lo: 35 % of the top, at least 1.5 m), so the
# crown is an upright ellipsoid r wide and top - lo high (a crown never flatter than half its radius), filled with leaf
# clusters near its surface. Branches and clusters are drawn from (x, y) alone, so the same tree looks the same on every
# page and run.
# Draw trees far to near (painter's order). The colours are the group palette's greens (palette v1.3):
#     tree  (deciduous)             green_mid 727A4E, green_light 8C9969, light = mix(8C9969, road FAF8F1, 0.35)
#     olive (evergreen broadleaf)   mix(727A4E, ink2 847E75, 0.4), mix(8C9969, structure B0AC9C, 0.45), its light
#     pine  (needle-leaved)         green_deep 495338, green_mid 727A4E, mix(727A4E, 8C9969, 0.6)
#     context (pale, not the topic) mix(BCC2A6, 8C9969, 0.3), CONTEXT_3D tree BCC2A6, mix(BCC2A6, FAF8F1, 0.45)
# (mix = the palette's OKLab mix). Shadows: green_deep (context: structure) at 10-16 %.
TREE_STYLES = {
    "tree":    dict(dark="727A4E", mid="8C9969", light="B1BA97", trunk="5B5147", shadow="495338", shadow_a=0.10,
                    lobes=1.0),
    "olive":   dict(dark="797C5E", mid="9CA280", light="BCBFA6", trunk="5B5147", shadow="495338", shadow_a=0.10,
                    lobes=1.0),
    "pine":    dict(dark="495338", mid="727A4E", light="818C5E", trunk="5B5147", shadow="495338", shadow_a=0.12,
                    lobes=1.3),                                    # needles: more, finer leaf clusters
    "context": dict(dark="ADB694", mid="BCC2A6", light="D7DAC7", trunk="A39E90", shadow="B0AC9C", shadow_a=0.16,
                    lobes=1.0),
}
TREE_ALPHA = (0.62, 0.68)                # opacity of the leaf clusters behind and in front of the branches
TREE_MIN_MM = 0.25                       # smallest crown radius drawn on the page, mm


def TREE_CROWN_LO(top):
    return max(1.5, 0.35 * top)


def _tree_rand(x, y):
    """A small repeatable random stream from the tree's position (the same in every Python)."""
    s = [(int(round(x * 100.0)) * 73856093 ^ int(round(y * 100.0)) * 19349663) & 0x7FFFFFFF or 1]

    def nxt():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7FFFFFFF
        return s[0] / 2147483648.0
    return nxt


def tree_shadow(pg, P, k, x, y, r, style, layer="tree_shadows"):
    """The crown's footprint on the ground, pushed to the lower right (light from the upper left). Draw all shadows
    on the ground first (draw_tree(..., shadow=False) then), so no shadow lies over a building."""
    A = max(TREE_MIN_MM, r * k)
    if A < 0.45:
        return
    sh = [P(x + 0.9 * r * math.cos(t), y + 0.9 * r * math.sin(t), 0.0) for t in [2.0 * math.pi * i / 28 for i in range(28)]]
    pg.poly([[(p[0] + 0.30 * A, p[1] - 0.08 * A) for p in sh]], fill=style["shadow"], stroke=None, layer=layer,
            alpha=style["shadow_a"])


def _tree_view(P, k):
    """Rows of the parallel view (page mm per metre / k) and the unit vector pointing away from the viewer."""
    o = P(0.0, 0.0, 0.0)
    e = [P(1.0, 0.0, 0.0), P(0.0, 1.0, 0.0), P(0.0, 0.0, 1.0)]
    u = [(p[0] - o[0]) / k for p in e]
    v = [(p[1] - o[1]) / k for p in e]
    c = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    return u, v, (-c[0], -c[1], -c[2])


def _tree_blob(cx, cy, R, rnd, m):
    """A leaf cluster: a round patch R mm across with a ragged, leafy edge."""
    ph = rnd() * 6.283
    return [(cx + R * (0.80 + 0.28 * rnd()) * math.cos(ph + 6.283 * i / m),
             cy + R * (0.80 + 0.28 * rnd()) * math.sin(ph + 6.283 * i / m)) for i in range(m)]


def draw_tree(pg, P, k, x, y, r, top, style, layer="trees", alpha=TREE_ALPHA, shadow=True):
    """Architectural entourage tree: a fine trunk and branch structure inside a crown built from many see-through
    leaf clusters, lit from the upper left, back clusters behind the branches and front clusters over them."""
    rnd = _tree_rand(x, y)
    st = style
    lo = TREE_CROWN_LO(top)
    a = max(0.5 * r, (top - lo) / 2.0)                     # vertical half-height of the crown
    zc = top - a
    A = r * k                                              # crown half-width on the page, mm
    u, v, d = _tree_view(P, k)
    if A < 0.45:                                           # a speck on the corridor pages: two small clusters
        c = P(x, y, zc)
        R = max(TREE_MIN_MM, A)
        for i in range(2):
            pg.poly([_tree_blob(c[0] + (i - 0.5) * 0.4 * R, c[1] + (0.5 - i) * 0.2 * R, R * (0.95 - 0.2 * i), rnd, 9)],
                    fill=st["mid"] if i else st["dark"], stroke=None, layer=layer, alpha=0.8)
        return
    if shadow:
        tree_shadow(pg, P, k, x, y, r, st, layer)
    full = A >= 1.2
    tw = min(0.30, max(0.06, 0.055 * A))                   # trunk line, mm
    # ---- branch structure (3D points, projected)
    lines = [((x, y, 0.0), (x, y, lo + 0.25 * a), tw)]
    if full:
        nb = 3 + int(rnd() * 3)
        for i in range(nb):
            t = 6.283 * (i + 0.6 * rnd()) / nb
            fr = 0.55 + 0.3 * rnd()
            end = (x + fr * r * math.cos(t), y + fr * r * math.sin(t), zc + (0.1 + 0.4 * rnd()) * a)
            base = (x, y, lo + (0.1 + 0.4 * rnd()) * a)
            lines.append((base, end, tw * 0.55))
            mid = tuple(base[j] + 0.55 * (end[j] - base[j]) for j in range(3))
            for _ in range(2):                             # twigs end inside the crown (70 % of its size at most)
                t2 = t + (rnd() - 0.5) * 1.6
                ez = rnd() * 0.6
                eh = 0.7 * math.sqrt(1.0 - ez * ez)
                lines.append((mid, (x + eh * r * math.cos(t2), y + eh * r * math.sin(t2), zc + 0.7 * ez * a),
                              max(0.04, tw * 0.3)))
    # ---- leaf clusters near the crown's surface, sorted far to near
    n = int(min(36, max(6, 4 + 3.0 * A)) * st.get("lobes", 1.0))
    cl = []
    for _ in range(n):
        ct, phi_ = 2.0 * rnd() - 1.0, 6.283 * rnd()
        sq = math.sqrt(max(0.0, 1.0 - ct * ct))
        f = 0.55 + 0.35 * rnd()
        q = (x + f * r * sq * math.cos(phi_), y + f * r * sq * math.sin(phi_), zc + f * a * ct)
        depth = sum(d[j] * (q[j] - (x, y, zc)[j]) for j in range(3))
        pp = P(*q)
        du, dv = (pp[0] - P(x, y, zc)[0]) / A, (pp[1] - P(x, y, zc)[1]) / max(1e-9, A)
        lit = -0.6 * du + 0.8 * dv - 0.5 * depth / max(r, a)
        cl.append((depth, pp, lit, (0.30 + 0.14 * rnd()) * A * st.get("blob", 1.0)))
    cl.sort(key=lambda c_: -c_[0])
    m = 16 if A > 3.0 else (12 if full else 9)
    back = [c_ for c_ in cl if c_[0] > 0.0]
    front = [c_ for c_ in cl if c_[0] <= 0.0]

    def blobs(lst, al):
        for _, pp, lit, R in lst:
            col = st["light"] if lit > 0.45 else (st["dark"] if lit < -0.25 else st["mid"])
            pg.poly([_tree_blob(pp[0], pp[1], R, rnd, m)], fill=col, stroke=None, layer=layer, alpha=al)
    blobs(back, alpha[0])
    for p0, p1, w in lines:
        pg.line([P(*p0), P(*p1)], st["trunk"], w, layer=layer)
    blobs(front, alpha[1])


# ============================================================ end of TREES


# ================================================================ profile
def prof_z(prof, s):
    s0, ds, Z = prof
    f = (s - s0) / ds
    i = int(math.floor(f))
    if i < 0:
        return Z[0]
    if i >= len(Z) - 1:
        return Z[-1]
    t = f - i
    return Z[i] * (1 - t) + Z[i + 1] * t


def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


class Sec(object):
    """One section: s along S4 -> page x, level -> page y (true 1:75)."""

    def __init__(self, d, prof):
        self.d, self.prof = d, prof
        self.dir = 1.0 if d["s_to"] > d["s_from"] else -1.0
        self.lo, self.hi = min(d["s_from"], d["s_to"]), max(d["s_from"], d["s_to"])
        self.zb = THALWEG[1] - STRIP[2] - 1.9           # bottom of the poche
        self.X0 = self.Y0 = 0.0
        self.build_surface()

    def X(self, s):
        return self.X0 + (s - self.d["s_from"]) * self.dir * K

    def Y(self, z):
        return self.Y0 + (z - self.zb) * K

    def P(self, s, z):
        return (self.X(s), self.Y(z))

    def ex(self, s):
        return prof_z(self.prof, s)

    def build_surface(self):
        """Finished surface as (s, z) vertices in drawing order (left to right), vertical steps at wall lines."""
        d = self.d
        V = []
        self.steps = []          # (s, z_hi, z_lo, high side: -1 left / +1 right in drawing order)
        self.flats = []          # (s_a, s_b, z, material, label)
        prev = None
        for srf in d["surfaces"]:
            if srf[0] == "steps":
                _, sa, sb, za, zb, n, mat, lab = srf
                if prev is not None and abs(prev - za) > 1e-6:
                    V.append((sa, za))
                tr = (sb - sa) / n
                rz = (zb - za) / n
                for i in range(n):
                    V.append((sa + i * tr, za + i * rz))
                    V.append((sa + (i + 1) * tr, za + i * rz))
                V.append((sb, zb))
                self.flats.append((sa, sb, None, mat, lab))
                self.stair = (sa, sb, za, zb, n)
                prev = zb
                continue
            sa, sb, z, mat, lab = srf
            if prev is not None and abs(prev - z) > 1e-6:
                self.steps.append((sa, max(prev, z), min(prev, z), -1 if prev > z else 1))
            V.append((sa, z))
            V.append((sb, z))
            self.flats.append((sa, sb, z, mat, lab))
            prev = z
        ra, rb = d["regrade"]
        V.append((rb, self.ex(rb)))
        n = int(abs(d["s_to"] - rb) / 0.25)
        for i in range(1, n + 1):
            s = rb + (d["s_to"] - rb) * i / n
            V.append((s, self.ex(s)))
        # summer strip: a 4 m low-flow channel cut 0.30 m into the bed at the low point; water flush with the bed
        a, b, dep = STRIP
        W = []
        for p in V:
            if min(a, b) < p[0] < max(a, b):
                continue
            W.append(p)
        out = []
        for i, p in enumerate(W):
            out.append(p)
            if i + 1 < len(W):
                q = W[i + 1]
                lo_, hi_ = sorted((p[0], q[0]))
                if lo_ <= min(a, b) and hi_ >= max(a, b):
                    e1, e2 = (a, b) if self.dir > 0 else (b, a)
                    zt = THALWEG[1]
                    out += [(e1, self.ex(e1)), (e1, zt - dep), (e2, zt - dep), (e2, self.ex(e2))]
        self.V = out
        self.design_end = rb

    def surf(self, s):
        """Surface level at s (the lower side at a vertical step)."""
        V = self.V
        best = None
        for i in range(len(V) - 1):
            a, b = V[i], V[i + 1]
            lo_, hi_ = sorted((a[0], b[0]))
            if lo_ - 1e-9 <= s <= hi_ + 1e-9:
                if abs(b[0] - a[0]) < 1e-9:
                    z = min(a[1], b[1])
                else:
                    z = a[1] + (b[1] - a[1]) * (s - a[0]) / (b[0] - a[0])
                best = z if best is None else min(best, z)
        return best if best is not None else self.ex(s)


# ================================================================ drawing pieces
def rng(*parts):
    return random.Random(zlib.crc32(repr(parts).encode("utf-8")) & 0x7fffffff)


def poche(pg, S):
    """Earth: white, a heavy cut line on top, stipple and pebbles that thin out with depth (as in the reference)."""
    V = S.V
    ring = [S.P(*p) for p in V] + [S.P(V[-1][0], S.zb), S.P(V[0][0], S.zb)]
    pg.poly([ring], fill="FFFFFF", stroke=None, layer="poche")
    r = rng("poche", S.d["key"])
    x0, x1 = sorted((S.X(S.d["s_from"]), S.X(S.d["s_to"])))
    n = int((x1 - x0) * 26.0)
    for _ in range(n):
        s = S.lo + r.random() * (S.hi - S.lo)
        top = S.surf(s)
        z = S.zb + r.random() * (top - S.zb)
        dep = top - z
        keep = (0.22 + 0.78 * math.exp(-dep / 0.9)) * min(1.0, (z - S.zb) / 1.2)
        if r.random() > keep or dep < 0.05:
            continue
        X, Y = S.P(s, z)
        if r.random() < 0.06 and dep > 0.18:                       # pebble
            R = 0.25 + r.random() * 0.55
            m = 4 + int(r.random() * 3)
            ph = r.random() * 6.28
            pts = [(X + R * (0.7 + 0.5 * r.random()) * math.cos(ph + 6.283 * i / m),
                    Y + R * 0.8 * (0.7 + 0.5 * r.random()) * math.sin(ph + 6.283 * i / m)) for i in range(m)]
            pg.poly([pts], fill=None, stroke=STIPPLE, lw=0.09, layer="poche")
        else:
            R = 0.10 + r.random() * (0.18 + 0.22 * math.exp(-dep / 1.5))
            pg.circle(X, Y, R, fill=("4A4A4A", "6E6E6E", "9A9A9A")[int(r.random() * 3)], layer="poche")
    pg.line([S.P(*p) for p in V], INK, 0.5, layer="cut line")


SOIL = "E9E3CF"                     # soft planting ground: a warm, slightly darker tone than the white earth poche
SOIL_DOT = ("B3A386", "C9BC9F", "9C8D70")
SOIL_DEPTH = 0.40                   # topsoil under planting, m (design value)


def soft_ground(pg, S):
    """A soft topsoil layer under every planted stretch (grass, lavender, shrubs, reeds, iris): it follows the finished
    surface, has a soft wavy underside and a fine soil grain; walls and slabs are drawn over it."""
    d = S.d
    spans = [tuple(sorted(x[:2])) for x in d["grass"] + d["lavender"] + d["iris"]]
    spans += [tuple(sorted(x[:2])) for x in d["reeds"]]
    spans += [(s - w / 2.0, s + w / 2.0) for s, h, w in d["shrubs"]]
    spans = sorted((max(a, S.lo), min(b, S.hi)) for a, b in spans if min(b, S.hi) > max(a, S.lo))
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1] + 0.3:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    lo_w, hi_w = sorted(STRIP[:2])
    out = []
    for a, b in merged:                                 # never under the water strip
        if b <= lo_w or a >= hi_w:
            out.append((a, b))
        else:
            if a < lo_w:
                out.append((a, lo_w))
            if b > hi_w:
                out.append((hi_w, b))
    r = rng("soil", d["key"])
    for a, b in out:
        n = max(2, int((b - a) / 0.1))
        ss = [a + (b - a) * i / n for i in range(n + 1)]
        top = [S.P(s, S.surf(s)) for s in ss]
        ph = r.random() * 6.28
        bot = []
        for i, s in enumerate(ss):
            t_ = min(1.0, min(s - a, b - s) / 0.6)          # the layer thins out at its ends
            dep = SOIL_DEPTH * (0.35 + 0.65 * t_) * (1.0 + 0.12 * math.sin(ph + s * 2.3) + 0.06 * math.sin(s * 7.1))
            bot.append(S.P(s, S.surf(s) - dep))
        ring = top + bot[::-1]
        pg.poly([ring], fill=SOIL, stroke=None, layer="soft ground")
        xs = [p[0] for p in ring]
        ys = [p[1] for p in ring]
        area = abs(area2(ring))
        for _ in range(int(area * 1.6)):
            X = min(xs) + r.random() * (max(xs) - min(xs))
            Y = min(ys) + r.random() * (max(ys) - min(ys))
            if pip(X, Y, ring):
                pg.circle(X, Y, 0.06 + r.random() * 0.12, fill=SOIL_DOT[int(r.random() * 3)], layer="soft ground")
        for i in range(0, len(top) - 1, 3):                 # a few root hairs just under the surface
            if r.random() < 0.35:
                X, Y = top[i]
                pg.line([(X, Y - 0.3), (X + (r.random() - 0.5) * 1.2, Y - 1.0 - r.random() * 2.0)], "A39577", 0.05,
                        layer="soft ground")


def concrete(pg, S, ring_m, layer="concrete"):
    ring = [S.P(s, z) for s, z in ring_m]
    pg.poly([ring], fill=CONCRETE, stroke=INK, lw=0.35, layer=layer)
    xs = [p[0] for p in ring]
    ys = [p[1] for p in ring]
    r = rng("conc", round(xs[0], 2), round(ys[0], 2))
    area = abs(area2(ring)) if len(ring) > 2 else 0.0
    for _ in range(int(area * 0.9)):
        X = min(xs) + r.random() * (max(xs) - min(xs))
        Y = min(ys) + r.random() * (max(ys) - min(ys))
        if pip(X, Y, ring):
            R = 0.08 + r.random() * 0.1
            pg.poly([[(X - R, Y - R), (X + R, Y - R), (X, Y + R)]], fill=CONCRETE_DOT, stroke=None, layer=layer)


def walls_and_slabs(pg, S):
    t = 0.30                                    # wall thickness (design)
    for s, zh, zl, side in S.steps:
        if zh - zl < 0.15:                      # a kerb, not a wall
            continue
        # wall on the high side of the step, drawn left to right in drawing order
        sgn = -S.dir if side < 0 else S.dir     # towards the high side, in s
        a, b = s, s + sgn * t
        concrete(pg, S, [(a, zh), (b, zh), (b, zl - 0.55), (a, zl - 0.55)])
        f0, f1 = s + sgn * (t + 0.35), s - sgn * 0.55
        concrete(pg, S, [(f0, zl - 0.55), (f1, zl - 0.55), (f1, zl - 0.85), (f0, zl - 0.85)])
    for sa, sb, z, mat, lab in S.flats:
        if z is None:                           # amphitheatre steps: a stepped concrete slab
            a, b, za, zb, n = S.stair
            tr, rz = (b - a) / n, (zb - za) / n
            top = []
            for i in range(n):
                top += [(a + i * tr, za + i * rz), (a + (i + 1) * tr, za + i * rz)]
            top.append((b, zb))
            concrete(pg, S, top + [(b, zb - 0.30), (a, za - 0.30)])     # stair slab, straight soffit
            continue
        if mat == "concrete":
            concrete(pg, S, [(sa, z), (sb, z), (sb, z - 0.18), (sa, z - 0.18)])
        elif mat == "asphalt":
            pg.poly([[S.P(sa, z), S.P(sb, z), S.P(sb, z - 0.08), S.P(sa, z - 0.08)]], fill=ASPHALT, stroke=INK,
                    lw=0.25, layer="asphalt")
            concrete(pg, S, [(sa, z - 0.08), (sb, z - 0.08), (sb, z - 0.25), (sa, z - 0.25)])
        elif mat == "deck":
            pg.poly([[S.P(sa, z), S.P(sb, z), S.P(sb, z - 0.06), S.P(sa, z - 0.06)]], fill=DECK, stroke=INK,
                    lw=0.25, layer="deck")
            n = max(2, int(abs(sb - sa) / 0.6))
            for i in range(n + 1):
                s = sa + (sb - sa) * (0.04 + 0.92 * i / n)
                X, Y = S.P(s, z - 0.06)
                pg.poly([[(X - 0.55, Y), (X + 0.55, Y), (X + 0.55, Y - 1.6), (X - 0.55, Y - 1.6)]], fill=DECK_DARK,
                        stroke=None, layer="deck")
            concrete(pg, S, [(sa, z - 0.18), (sb, z - 0.18), (sb, z - 0.38), (sa, z - 0.38)])
    # terrace edges below the level of the decks are retained by the walls; edge of the regraded bank: stone toe
    ra, rb = S.d["regrade"]
    zr = S.surf(ra + (rb - ra) * 0.02)
    concrete(pg, S, [(ra, zr), (ra + (rb - ra) * 0.08, zr), (ra + (rb - ra) * 0.08, zr - 0.5), (ra, zr - 0.5)])


BEYOND = "A3A3A3"                   # lines of things standing beyond the cut
BEYOND_FILL = "F5F5F3"
BEYOND_CORTEN = "C4A794"
BEYOND_FIG = "9A9A9A"
OAK = "B88A5A"


def _rrect(x0, y0, x1, y1, rad, n=3):
    """Rounded rectangle (handrail profile)."""
    pts = []
    for cx, cy, a0 in ((x1 - rad, y1 - rad, 0.0), (x0 + rad, y1 - rad, 90.0), (x0 + rad, y0 + rad, 180.0),
                       (x1 - rad, y0 + rad, 270.0)):
        for k_ in range(n + 1):
            a = math.radians(a0 + 90.0 * k_ / n)
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


def handrail(pg, S, s, z):
    """Railing cut by the section (it runs along the river): corten flat-bar post 60 x 15 on a base plate with two
    anchors, corten saddle and oak handrail 70 x 45 (top +1.10 m), bottom rail 40 x 40 at +0.10 m (design values)."""
    X, Y = S.P(s, z)
    k = K
    w = 0.06 * k
    pg.poly([[(X - 0.10 * k, Y), (X + 0.10 * k, Y), (X + 0.10 * k, Y + 0.02 * k), (X - 0.10 * k, Y + 0.02 * k)]],
            fill=CORTEN, stroke=INK, lw=0.05, layer="handrail")                       # base plate 200 x 20
    for dx in (-0.065, 0.065):                                                         # chemical anchors
        pg.line([(X + dx * k, Y), (X + dx * k, Y - 0.12 * k)], INK2, 0.08, dash=[0.3, 0.2], layer="handrail")
    pg.poly([[(X - w / 2, Y + 0.02 * k), (X + w / 2, Y + 0.02 * k), (X + w * 0.4, Y + 1.03 * k),
              (X - w * 0.4, Y + 1.03 * k)]], fill=CORTEN, stroke=INK, lw=0.06, layer="handrail")
    pg.poly([[(X - 0.025 * k, Y + 1.03 * k), (X + 0.025 * k, Y + 1.03 * k), (X + 0.025 * k, Y + 1.055 * k),
              (X - 0.025 * k, Y + 1.055 * k)]], fill=CORTEN, stroke=INK, lw=0.04, layer="handrail")   # saddle
    pg.poly([_rrect(X - 0.035 * k, Y + 1.055 * k, X + 0.035 * k, Y + 1.10 * k, 0.012 * k)], fill=OAK, stroke=INK,
            lw=0.06, layer="handrail")                                                 # oak handrail, cut
    pg.poly([[(X - 0.02 * k, Y + 0.08 * k), (X + 0.02 * k, Y + 0.08 * k), (X + 0.02 * k, Y + 0.12 * k),
              (X - 0.02 * k, Y + 0.12 * k)]], fill=CORTEN, stroke=INK, lw=0.04, layer="handrail")   # bottom rail


def railing_elevation(pg, S, s0, s1, z, beyond=False, layer="handrail"):
    """Railing seen in elevation (parallel to the section plane): posts at most 1.5 m apart, side-fixed to the slab edge
    with a plate and two bolts, corten flat-bar balusters every 0.11 m, bottom rail at +0.10 m, corten top flat bar
    under an oak handrail, top +1.10 m (design values). beyond = drawn light, as standing behind the cut."""
    k = K
    fill = BEYOND_CORTEN if beyond else CORTEN
    line = BEYOND if beyond else INK
    oak = "DCC7AE" if beyond else OAK
    a, b = sorted((S.X(s0), S.X(s1)))
    y0 = S.Y(z)
    yb0, yb1 = y0 + 0.08 * k, y0 + 0.12 * k
    yt0, yt1 = y0 + 0.99 * k, y0 + 1.04 * k
    n_bal = int((b - a) / (0.11 * k))
    for i in range(1, n_bal):                                                          # balusters 12 x 40
        x = a + (b - a) * i / n_bal
        pg.line([(x, yb1), (x, yt0)], fill, 0.16, layer=layer, cap=0)
    pg.poly([[(a, yb0), (b, yb0), (b, yb1), (a, yb1)]], fill=fill, stroke=line, lw=0.05, layer=layer)
    n = max(1, int(math.ceil((b - a) / (1.5 * k))))
    for i in range(n + 1):
        x = a + (b - a) * i / n
        x = min(max(x, a + 0.03 * k), b - 0.03 * k)
        pg.poly([[(x - 0.03 * k, y0 - 0.22 * k), (x + 0.03 * k, y0 - 0.22 * k), (x + 0.03 * k, yt0),
                  (x - 0.03 * k, yt0)]], fill=fill, stroke=line, lw=0.06, layer=layer)    # post 60 x 15
        pg.poly([[(x - 0.06 * k, y0 - 0.24 * k), (x + 0.06 * k, y0 - 0.24 * k), (x + 0.06 * k, y0 - 0.02 * k),
                  (x - 0.06 * k, y0 - 0.02 * k)]], fill=None, stroke=line, lw=0.05, layer=layer)  # side plate
        for yy in (y0 - 0.07 * k, y0 - 0.19 * k):
            pg.circle(x, yy, 0.18, fill="D9D4CC" if not beyond else "EEEEEE", stroke=line, lw=0.03, layer=layer)
    pg.poly([[(a - 0.05 * k, yt0), (b + 0.05 * k, yt0), (b + 0.05 * k, yt1), (a - 0.05 * k, yt1)]], fill=fill,
            stroke=line, lw=0.05, layer=layer)                                         # top flat bar
    pg.poly([_rrect(a - 0.08 * k, yt1, b + 0.08 * k, y0 + 1.10 * k, 0.015 * k)], fill=oak, stroke=line, lw=0.07,
            layer=layer)                                                               # oak handrail
    pg.line([(a - 0.06 * k, y0 + 1.07 * k), (b + 0.06 * k, y0 + 1.07 * k)], "9C7448" if not beyond else "CDB89E",
            0.04, layer=layer)                                                         # grain line


def balcony(pg, S, b, people):
    """The balcony stands just beyond the cut (as in the reference's J-J'): light 'beyond' lines, drawn before the
    cut so the amphitheatre steps, the earth and the people on the lower walk lie over it. People on the balcony stand
    behind its near railing: drawn light, then the railing over them."""
    s0, s1, top, th = b["s0"], b["s1"], b["top"], b["thick"]
    for c in b["columns"]:
        g = S.surf(c)
        pg.poly([[S.P(c - 0.15, top - th), S.P(c + 0.15, top - th), S.P(c + 0.15, g), S.P(c - 0.15, g)]],
                fill=BEYOND_FILL, stroke=BEYOND, lw=0.12, layer="balcony (beyond)")
    pg.poly([[S.P(s0, top - 0.06), S.P(s1, top - 0.06), S.P(s1, top - th), S.P(s0, top - th)]], fill=BEYOND_FILL,
            stroke=BEYOND, lw=0.12, layer="balcony (beyond)")
    pg.poly([[S.P(s0, top), S.P(s1, top), S.P(s1, top - 0.06), S.P(s0, top - 0.06)]], fill="E9DCCB", stroke=BEYOND,
            lw=0.1, layer="balcony (beyond)")
    for s, kind, flip in people:
        X, Y = S.P(s, top)
        draw_asset(pg, FIGS[kind % len(FIGS)], X, Y, flip=flip, layer="people (beyond)", tone=BEYOND_FIG)
    railing_elevation(pg, S, s0, s1, top, beyond=True, layer="balcony (beyond)")


def pergola(pg, S, p):
    for s in p["posts"]:
        X, Y = S.P(s, S.surf(s))
        h = max(pl[2] for pl in p["plates"]) * K
        pg.poly([[(X - 0.6, Y), (X + 0.6, Y), (X + 0.6, Y + h), (X - 0.6, Y + h)]], fill="FFFFFF", stroke=INK, lw=0.25,
                layer="shading")
    for a, b, h in p["plates"]:
        z = S.surf(p["posts"][0]) + h
        pg.poly([[S.P(a, z), S.P(b, z), S.P(b, z + 0.1), S.P(a, z + 0.1)]], fill="F4F4F2", stroke=INK, lw=0.25,
                layer="shading")


def water_rings(S, z):
    """The water body at level z: the finished surface (strip included) clipped below z, closed along z."""
    V = S.V
    runs, cur = [], []
    for i, p in enumerate(V):
        below = p[1] < z - 1e-9
        if i > 0:
            q = V[i - 1]
            if (q[1] < z - 1e-9) != below:
                f = (z - q[1]) / (p[1] - q[1])
                c = (q[0] + f * (p[0] - q[0]), z)
                if below:
                    cur = [c]
                else:
                    cur.append(c)
                    runs.append(cur)
                    cur = []
        if below:
            if not cur:
                cur = [(p[0], z)]
            cur.append(p)
    if cur:
        cur.append((V[-1][0], z))
        runs.append(cur)
    return [[S.P(s, zz) for s, zz in r] for r in runs if len(r) >= 3]


def water(pg, S, z, alpha=0.62):
    """Water at level z: light blue, see-through (stems and the bed show under it), hatch, firm surface line."""
    for ring in water_rings(S, z):
        pg.poly([ring], fill=WATER, stroke=None, layer="water", alpha=alpha)
        ys = [p[1] for p in ring]
        y = min(ys) + 0.7
        while y < max(ys) - 0.3:                                   # horizontal hatch inside the water
            xs = []
            for k_ in range(len(ring)):
                p, q = ring[k_], ring[(k_ + 1) % len(ring)]
                if (p[1] - y) * (q[1] - y) < 0:
                    xs.append(p[0] + (y - p[1]) * (q[0] - p[0]) / (q[1] - p[1]))
            xs.sort()
            for m in range(0, len(xs) - 1, 2):
                if xs[m + 1] - xs[m] > 1.0:
                    pg.line([(xs[m] + 0.4, y), (xs[m + 1] - 0.4, y)], WATER_LINE, 0.1, layer="water")
            y += 0.7
        top = [p for p in ring if abs(p[1] - max(ys)) < 1e-6]
        if len(top) >= 2:
            x0, x1 = min(p[0] for p in top), max(p[0] for p in top)
            pg.line([(x0, max(ys)), (x1, max(ys))], FLOOD, 0.3, layer="water")
            r = rng("ripple", round(x0, 1))
            x = x0 + 1.0
            while x < x1 - 2.0:                                     # small ripples under the surface
                L = 0.8 + r.random() * 1.6
                pg.line([(x, max(ys) - 0.45 - r.random() * 0.5), (x + L, max(ys) - 0.45 - r.random() * 0.5)],
                        FLOOD, 0.08, layer="water")
                x += L + 1.0 + r.random() * 2.0


def level_line(pg, S, z, label, dash, colour=FLOOD):
    """A water level drawn only where it stands above the surface, with its sign and text at the right end."""
    s_l, s_r = S.d["s_from"], S.d["s_to"]
    n = int(abs(s_r - s_l) / 0.1)
    run = []
    runs = []
    for i in range(n + 1):
        s = s_l + (s_r - s_l) * i / n
        if z > S.surf(s) + 0.01:
            run.append(S.P(s, z))
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    for r in runs:
        if len(r) >= 2:
            pg.line([r[0], r[-1]], colour, 0.25, dash=dash, layer="levels")
    X, Y = S.P(s_r, z)
    X -= 3.0
    pg.poly([[(X - 1.3, Y + 1.9), (X + 1.3, Y + 1.9), (X, Y)]], fill=None, stroke=colour, lw=0.2, layer="levels")
    pg.line([(X - 0.8, Y - 0.6), (X + 0.8, Y - 0.6)], colour, 0.2, layer="levels")
    pg.text(label, X - 2.5, Y + 0.6, 2.0, colour, align="R", layer="levels")


# ================================================================ VEGETATION (procedural, high detail; page mm, y up)
# Every plant is built from many small vector pieces: tapered branches and twigs, single leaves (pointed, lobed or
# narrow, each with a midrib on the larger ones), grass and reed blades as tapered curved strips, seed heads of many
# grains. Light comes from the upper left: leaves there are lighter, leaves inside and lower right darker. Colours are
# the reference's light greens. A plant is the same on every run (seeded by its position).
LEAF_TONES = ["E4EDC6", "D3E2A6", "C1D48C", "ABC173", "93AA5E", "7B9450"]   # light .. deep
LEAF_EDGE = "6E8646"
BARK = ("C9CAB8", "A3A690", "6F735F")                                          # light, mid, dark bark
GRASS_TONES = ["B9CC83", "A2B96C", "8BA35A", "C9D99A", "748D49"]
REED_TONES = ["B9B98E", "A6A97A", "C7C59B", "8F9468"]
SEED_TONES = ["C2A779", "AE9165", "D4BD92"]
LAV_TONES = ["8E74B5", "A48CC6", "7A62A0", "B9A6D6"]
STRAW = ["D3C59C", "C2B48A", "DDD2AE", "AE9F78"]
# How the plants look in each season (general habit of the species: Platanus orientalis, Tamarix and Vitex are
# deciduous, Lavandula stoechas is evergreen; reeds cut back after October as in concept s.10.1). Drawing values.
SEASON_LOOK = {
    "winter": dict(tree_leaf=0.0, tree_tones=LEAF_TONES, seed_balls=True, shrub_leaf=0.10,
                   shrub_tones=["C9C3A0", "B7B08B", "A39C78"], grass_tones=GRASS_TONES, reed_h=0.32, reed_tones=STRAW,
                   reed_leaf=0.0, plume=0.0, iris_h=0.35, iris_flower=0.0, iris_tones=["7F8F5A", "8E9A66", "9AA372"],
                   lav_spikes=0),
    "spring": dict(tree_leaf=0.80, tree_tones=["EEF4CF", "E0EDB2", "CFE29A", "BCD585", "A6C46F", "8FAF5C"],
                   seed_balls=False, shrub_leaf=0.85, shrub_tones=["EEF4CF", "DCEBAE", "C8DD93", "B2CE7B", "98B964"],
                   grass_tones=["C4D88A", "ADC774", "96B060", "D3E4A3", "7F9B4E"], reed_h=0.62,
                   reed_tones=["B4C98A", "A3BB78", "C3D59C", "8FAA66"], reed_leaf=0.8, plume=0.0, iris_h=1.0,
                   iris_flower=0.85, iris_tones=["6E8F4A", "7FA057", "5F7E40", "8FB066"], lav_spikes=7),
    "summer": dict(tree_leaf=1.0, tree_tones=LEAF_TONES, seed_balls=False, shrub_leaf=1.0, shrub_tones=LEAF_TONES,
                   grass_tones=["D8CC9A", "C9BB84", "A9B573", "C2C78E", "93A363"], reed_h=1.0, reed_tones=REED_TONES,
                   reed_leaf=1.0, plume=0.35, iris_h=1.0, iris_flower=0.0,
                   iris_tones=["6E8F4A", "7FA057", "5F7E40", "8FB066"], lav_spikes=3),
    "autumn": dict(tree_leaf=0.70, tree_tones=["F1E2B0", "E6CF8C", "D9B86C", "C99E55", "B08445", "8E6B3A"],
                   seed_balls=True, shrub_leaf=0.65, shrub_tones=["E8D9A2", "D6C083", "C2A86A", "A8A066", "8E9458"],
                   grass_tones=["C9C08C", "B4B47E", "9FAA6C", "D1C79A", "8C9B5E"], reed_h=1.0,
                   reed_tones=["D3C08A", "C2AE78", "B49F6C", "A8A27A"], reed_leaf=0.7, plume=0.95, iris_h=0.85,
                   iris_flower=0.0, iris_tones=["A3A266", "B7AE70", "8E9A5E", "C2B478"], lav_spikes=0),
}
SEA = dict(SEASON_LOOK["summer"])


def _bez(p0, p1, p2, n):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]) for t in [i / float(n) for i in range(n + 1)]]


def _strip(path, w0, w1, tip=True):
    """A tapered strip along a path (blade, stem, branch): width w0 at the base to w1 (0 = pointed) at the end."""
    L, R = [], []
    n = len(path)
    for i, p in enumerate(path):
        a = path[min(i + 1, n - 1)]
        b = path[max(i - 1, 0)]
        dx, dy = a[0] - b[0], a[1] - b[1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        t = i / float(n - 1)
        w = (w0 + (w1 - w0) * t) / 2.0
        L.append((p[0] + nx * w, p[1] + ny * w))
        R.append((p[0] - nx * w, p[1] - ny * w))
    return L + R[::-1]


def _leaf(cx, cy, size, ang, kind, r):
    """One leaf, size = length in mm. kind 0 pointed oval, 1 three-lobed (plane), 2 narrow (willow-like)."""
    ca, sa = math.cos(ang), math.sin(ang)
    pts = []
    if kind == 1:
        prof = [(0.0, 0.0), (0.18, 0.22), (0.30, 0.42), (0.42, 0.30), (0.55, 0.38), (0.72, 0.20), (1.0, 0.0)]
    elif kind == 2:
        prof = [(0.0, 0.0), (0.2, 0.09), (0.5, 0.12), (0.8, 0.07), (1.0, 0.0)]
    else:
        prof = [(0.0, 0.0), (0.15, 0.20), (0.45, 0.28), (0.75, 0.18), (1.0, 0.0)]
    wob = 0.85 + 0.3 * r.random()
    side = [(u * size, v * size * wob) for u, v in prof]
    for u, v in side + [(u, -v * (0.9 + 0.2 * r.random())) for u, v in side[-2:0:-1]]:
        pts.append((cx + u * ca - v * sa, cy + u * sa + v * ca))
    return pts


def _tone(lit, r, tones=LEAF_TONES):
    k = (1.0 - lit) * (len(tones) - 1) + (r.random() - 0.5) * 1.6
    return tones[max(0, min(len(tones) - 1, int(round(k))))]


def veg_tree(pg, X, Y, h, w, seed, flip=False, leaf_mm=None, layer="trees"):
    """Broadleaf tree (plane-tree habit): tapered trunk, 4 orders of branches, about 2,000-3,000 leaves on the twig
    tips, back leaves darker, front leaves lighter and sparser so the branch structure reads through the crown."""
    r = rng("tree", seed)
    fx = -1.0 if flip else 1.0
    lo = 0.36 * h
    branches, tips = [], []

    cx, cy = X, Y + lo + (h - lo) * 0.52
    ax, ay = w / 2.0, (h - lo) * 0.52

    def inside(px, py):
        return ((px - cx) / ax) ** 2 + ((py - cy) / ay) ** 2

    def grow(x, y, ang, length, width, depth):
        n = 5
        bend = (r.random() - 0.5) * 0.35
        ex, ey = x + math.cos(ang) * length, y + math.sin(ang) * length
        for _ in range(12):                                     # twigs end inside the crown, never poke out
            if inside(ex, ey) <= 0.78:
                break
            length *= 0.85
            ex, ey = x + math.cos(ang) * length, y + math.sin(ang) * length
        mx = (x + ex) / 2 + math.cos(ang + 1.57) * length * bend * 0.25
        my = (y + ey) / 2 + math.sin(ang + 1.57) * length * bend * 0.25
        path = _bez((x, y), (mx, my), (ex, ey), n)
        branches.append((path, width, width * 0.62, depth))
        if depth >= 3:
            for q in path[2:]:
                tips.append((q[0], q[1], depth - 1))
        if depth >= 5 or length < 0.025 * h:
            tips.append((ex, ey, depth))
            return
        k = 2 + (1 if r.random() < 0.55 else 0)
        for i in range(k):
            sp = (0.42 + 0.25 * r.random()) * (1 if i % 2 else -1) * (1.0 if i < 2 else 0.4)
            na = ang + sp + (r.random() - 0.5) * 0.25
            na = max(0.15, min(math.pi - 0.15, na))           # nothing grows downwards
            grow(ex, ey, na, length * (0.68 + 0.14 * r.random()), width * 0.62, depth + 1)
        tips.append((ex, ey, depth))

    # trunk to the crown base, then the main limbs
    tw = max(1.1, 0.04 * w)
    trunk = _bez((X, Y), (X + fx * 0.04 * w, Y + lo * 0.5), (X - fx * 0.02 * w, Y + lo), 8)
    branches.append((trunk, tw, tw * 0.78, 0))
    for i in range(5):
        a = math.pi / 2 + (i - 2) * 0.30 + (r.random() - 0.5) * 0.15
        grow(X - fx * 0.02 * w, Y + lo, a, (h - lo) * (0.30 + 0.10 * r.random()), tw * 0.70, 1)
    # leaves: around every tip and along the outer branches, inside the crown envelope (an upright ellipse)
    size = leaf_mm or max(0.5, 0.022 * h)
    leaves = []
    for (tx, ty, d) in tips:
        n = 22 if d >= 4 else (10 if d >= 3 else 4)
        for _ in range(n):
            px = tx + r.gauss(0, size * 2.2)
            py = ty + r.gauss(0, size * 1.8) + size * 0.5
            e = inside(px, py)
            if e > 1.0 + 0.08 * r.random():
                continue
            depth = r.random()                                  # 0 = front, 1 = back
            if r.random() > SEA["tree_leaf"]:
                continue
            lit = 0.5 + 0.35 * (-(px - cx) * fx / ax + (py - cy) / ay) / 2 - 0.25 * depth + 0.4 * (1 - e) * 0
            leaves.append((depth, px, py, lit))
    leaves.sort(key=lambda q: -q[0])
    back = [q for q in leaves if q[0] > 0.45]
    front = [q for q in leaves if q[0] <= 0.45 and r.random() < 0.8]

    def draw_leaves(lst, al, dark):
        for depth, px, py, lit in lst:
            ang = r.random() * 6.283
            sz = size * (0.75 + 0.5 * r.random())
            kind = 1 if r.random() < 0.35 else 0
            col = _tone(max(0.0, min(1.0, lit - dark)), r, SEA["tree_tones"])
            leaf = _leaf(px, py, sz, ang, kind, r)
            edge = LEAF_EDGE if sz > 2.2 and r.random() < 0.5 else None
            pg.poly([leaf], fill=col, stroke=edge, lw=0.04, layer=layer, alpha=al)
            if sz > 2.6 and r.random() < 0.6:                  # midrib
                pg.line([(px, py), (px + math.cos(ang) * sz * 0.85, py + math.sin(ang) * sz * 0.85)], LEAF_EDGE, 0.04,
                        layer=layer)

    draw_leaves(back, 0.88, 0.25)
    for path, w0, w1, d in sorted(branches, key=lambda b: b[3]):
        ring = _strip(path, w0, w1)
        pg.poly([ring], fill=BARK[0], stroke=BARK[2], lw=0.06 if d < 2 else 0.04, layer=layer)
        if d <= 1:                                              # bark streaks on trunk and main limbs
            for k_ in range(3):
                off = (k_ - 1) * w0 * 0.22
                pg.line([(p[0] + off, p[1]) for p in path[1:-1]], BARK[1], 0.05, layer=layer)
    draw_leaves(front, 0.82, -0.05)
    if SEA["seed_balls"]:                                       # plane seed balls hang on through winter
        rb_ = rng("balls", seed)
        for (tx, ty, d) in tips:
            if d >= 4 and rb_.random() < 0.10:
                L = size * (1.2 + rb_.random())
                pg.line([(tx, ty), (tx + rb_.gauss(0, 0.3), ty - L)], BARK[2], 0.05, layer=layer)
                pg.circle(tx, ty - L - 0.45, 0.45, fill="8A6F4D", stroke="5E4A33", lw=0.04, layer=layer)


def veg_shrub(pg, X, Y, h, w, seed, kind=0, layer="planting"):
    """Shrub: 5-9 woody stems fanning from the base, 300-700 small leaves on a domed crown (kind 2 = narrow leaves,
    tamarisk / vitex habit)."""
    r = rng("shrub", seed)
    stems = []
    ns = 5 + int(r.random() * 5)
    for i in range(ns):
        a = math.pi / 2 + (i - (ns - 1) / 2.0) * (1.1 / ns) + (r.random() - 0.5) * 0.15
        L = h * (0.65 + 0.3 * r.random())
        end = (X + math.cos(a) * L * 0.9 * (w / h), Y + math.sin(a) * L)
        mid = (X + (end[0] - X) * 0.4, Y + (end[1] - Y) * 0.55)
        path = _bez((X + (r.random() - 0.5) * w * 0.08, Y), mid, end, 6)
        stems.append(path)
    size = max(0.9, 0.11 * h) if kind != 2 else max(1.1, 0.13 * h)
    n = int(140 + 5.5 * w * h / (size * size) * 0.5)
    n = min(n, 900)
    cx, cy = X, Y + h * 0.55
    leaves = []
    for _ in range(n):
        t = r.random()
        st = stems[int(r.random() * len(stems))]
        j = int((0.35 + 0.65 * t) * (len(st) - 1))
        px = st[j][0] + r.gauss(0, size * 1.3)
        py = st[j][1] + r.gauss(0, size * 1.1)
        if py < Y + h * 0.12 or r.random() > SEA["shrub_leaf"]:
            continue
        lit = 0.55 + 0.35 * (-(px - cx) / (w / 2) + (py - cy) / (h / 2)) / 2
        leaves.append((r.random(), px, py, lit))
    leaves.sort(key=lambda q: -q[0])
    for path in stems:
        pg.poly([_strip(path, max(0.18, 0.012 * w), 0.06)], fill=BARK[1], stroke=None, layer=layer)
    for depth, px, py, lit in leaves:
        lk = 2 if kind == 2 else (1 if r.random() < 0.2 else 0)
        sz = size * (0.7 + 0.6 * r.random())
        pg.poly([_leaf(px, py, sz, r.random() * 6.283, lk, r)], fill=_tone(max(0, min(1, lit - 0.3 * depth)), r, SEA["shrub_tones"]),
                stroke=LEAF_EDGE if r.random() < 0.25 else None, lw=0.03, layer=layer, alpha=0.9)


def veg_blade(pg, X, Y, length, ang, width, curl, col, layer="planting"):
    ex, ey = X + math.cos(ang) * length, Y + math.sin(ang) * length
    mx = X + math.cos(ang) * length * 0.5 + math.cos(ang - 1.57) * curl * length
    my = Y + math.sin(ang) * length * 0.5 + math.sin(ang - 1.57) * curl * length
    pg.poly([_strip(_bez((X, Y), (mx, my), (ex, ey), 6), width, 0.0)], fill=col, stroke=None, layer=layer)


def shrub(pg, S, s, h, w):
    X, Y = S.P(s, S.surf(s))
    veg_shrub(pg, X, Y, h * K, w * K, (S.d["key"], round(s, 2)), kind=2 if (h <= 1.6 and s % 2 > 1) else 0)


def tufts(pg, S, s0, s1, h=0.35, colour=None, step=0.35, seed="g"):
    """Meadow grass: dense tapered blades in five greens, clumps of 9-15 blades, short blades filling between."""
    r = rng("tuft", seed, round(s0, 2))
    n = max(1, int(abs(s1 - s0) / (step * 0.55)))
    for i in range(n):
        s = s0 + (s1 - s0) * (i + 0.5 + (r.random() - 0.5) * 0.7) / n
        X, Y = S.P(s, S.surf(s))
        for j in range(9 + int(r.random() * 7)):
            L = h * K * (0.45 + 0.75 * r.random())
            a = math.pi / 2 + (r.random() - 0.5) * 1.3
            veg_blade(pg, X + (r.random() - 0.5) * 1.2, Y, L, a, 0.28 + 0.2 * r.random(), (r.random() - 0.5) * 0.25,
                      SEA["grass_tones"][int(r.random() * len(SEA["grass_tones"]))])


def lavender(pg, S, s0, s1):
    """Lavandula stoechas: grey-green needle leaves in a low mound, flower spikes of many small purple florets."""
    r = rng("lav", round(s0, 2))
    n = max(1, int(abs(s1 - s0) / 0.42))
    for i in range(n):
        s = s0 + (s1 - s0) * (i + 0.5) / n
        X, Y = S.P(s, S.surf(s))
        for j in range(26):
            a = math.pi / 2 + (r.random() - 0.5) * 2.0
            veg_blade(pg, X + (r.random() - 0.5) * 2, Y, (0.18 + 0.2 * r.random()) * K, a, 0.22,
                      (r.random() - 0.5) * 0.2, ["A7B596", "93A383", "BCC7AE"][int(r.random() * 3)])
        for j in range(SEA["lav_spikes"]):
            a = math.pi / 2 + (r.random() - 0.5) * 0.9
            L = (0.32 + 0.16 * r.random()) * K
            ex, ey = X + math.cos(a) * L, Y + math.sin(a) * L
            pg.line([(X, Y), (ex, ey)], "8C9B78", 0.07, layer="planting")
            for k_ in range(9):
                t = 0.72 + 0.28 * k_ / 8.0
                fx_, fy_ = X + math.cos(a) * L * t, Y + math.sin(a) * L * t
                pg.poly([_leaf(fx_ - 0.25, fy_, 0.55, a + (0.6 if k_ % 2 else -0.6), 0, r)],
                        fill=LAV_TONES[int(r.random() * len(LAV_TONES))], stroke=None, layer="planting")
            pg.poly([_leaf(ex, ey, 0.9, a + 0.5, 0, r), _leaf(ex, ey, 0.9, a - 0.5, 0, r)][:1],
                    fill="C7B6E0", stroke=None, layer="planting")


def reeds(pg, S, s0, s1, h):
    """Phragmites: tapered culms, 5-7 long arching leaves each, plumes of 40-60 grains hanging to one side."""
    r = rng("reed", round(s0, 2))
    n = max(2, int(abs(s1 - s0) / 0.2))
    for i in range(n):
        s = s0 + (s1 - s0) * (i + r.random()) / n
        X, Y = S.P(s, S.surf(s))
        H = h * SEA["reed_h"] * (0.7 + 0.35 * r.random()) * K
        lean = (r.random() - 0.5) * 0.18
        top = (X + lean * H, Y + H)
        culm = _bez((X, Y), (X + lean * H * 0.3, Y + H * 0.5), top, 8)
        pg.poly([_strip(culm, 0.38, 0.12)], fill=SEA["reed_tones"][int(r.random() * 4)], stroke=None,
                layer="planting")
        if SEA["reed_h"] < 0.4:                                 # cut stubble: a flat cut top
            pg.line([(top[0] - 0.25, top[1]), (top[0] + 0.25, top[1])], STRAW[3], 0.08, layer="planting")
        for j in range(5 + int(r.random() * 3)):
            if r.random() > SEA["reed_leaf"]:
                continue
            t = 0.12 + 0.7 * j / 7.0
            p = culm[int(t * (len(culm) - 1))]
            side = 1 if (j + i) % 2 else -1
            a = math.pi / 2 - side * (0.5 + 0.5 * r.random())
            veg_blade(pg, p[0], p[1], (0.35 + 0.25 * r.random()) * K, a, 0.55, side * (0.18 + 0.12 * r.random()),
                      SEA["reed_tones"][int(r.random() * 4)] if SEA["plume"] > 0.9 else
                      GRASS_TONES[int(r.random() * len(GRASS_TONES))])
        if r.random() < SEA["plume"]:                           # plume
            side = 1 if r.random() < 0.5 else -1
            for k_ in range(40 + int(r.random() * 20)):
                t = r.random()
                gx = top[0] + side * (0.15 + 1.6 * t) + r.gauss(0, 0.45)
                gy = top[1] - 0.2 - 3.2 * t * t - r.random() * 1.2
                pg.poly([_leaf(gx, gy, 0.55 + 0.3 * r.random(), -math.pi / 2 + side * 0.5 + r.gauss(0, 0.3), 2, r)],
                        fill=SEED_TONES[int(r.random() * 3)], stroke=None, layer="planting")


def iris(pg, S, s0, s1):
    """Iris pseudacorus: fans of 7-10 sword leaves, yellow flowers of three falls and three standards."""
    r = rng("iris", round(s0, 2))
    n = max(1, int(abs(s1 - s0) / 0.4))
    for i in range(n):
        s = s0 + (s1 - s0) * (i + 0.5) / n
        X, Y = S.P(s, S.surf(s))
        for j in range(7 + int(r.random() * 4)):
            a = math.pi / 2 + (j - 4) * 0.11 + (r.random() - 0.5) * 0.08
            veg_blade(pg, X + (j - 4) * 0.25, Y, SEA["iris_h"] * (0.55 + 0.35 * r.random()) * K, a, 0.75,
                      (r.random() - 0.5) * 0.08, SEA["iris_tones"][int(r.random() * len(SEA["iris_tones"]))])
        if r.random() < SEA["iris_flower"]:
            fx_, fy_ = X + (r.random() - 0.5) * 2.5, Y + (0.75 + 0.2 * r.random()) * K
            pg.line([(X, Y), (fx_, fy_)], "6E8F4A", 0.12, layer="planting")
            for k_ in range(3):
                pg.poly([_leaf(fx_, fy_, 1.5, -0.5 - k_ * 1.05 + 0.2, 0, r)], fill="E2C246", stroke="B8952A", lw=0.03,
                        layer="planting")
                pg.poly([_leaf(fx_, fy_, 1.0, 1.2 + k_ * 0.35, 0, r)], fill="F0D66A", stroke=None, layer="planting")


FIGS = ["I_walker_flood_wall", "I_woman_with_bag", "J_woman_walking", "I_photographer", "J_man_and_child",
        "J_photographer_balcony", "J_woman_on_steps", "I_child_on_sand", "J_person_seated", "J_person_sitting",
        "J_cyclist_cheering", "I_cyclist_waving"]          # traced from the reference (J_person_seated = the sitting
#                                                   figure without its chair, anchored at the seat: sits on an edge)


def figure(pg, S, s, kind, flip, z=None):
    g = S.surf(s) if z is None else z
    X, Y = S.P(s, g)
    draw_asset(pg, FIGS[kind % len(FIGS)], X, Y, flip=flip, layer="people", tone=FIG)


def bike(pg, S, s, flip):
    g = S.surf(s)
    X, Y = S.P(s, g)
    k = K
    sg = -1.0 if flip else 1.0
    R = 0.34 * k
    for dx in (-0.55, 0.55):
        pg.circle(X + sg * dx * k, Y + R, R, fill=None, stroke=FIG, lw=0.3, layer="people")
    pg.line([(X - sg * 0.55 * k, Y + R), (X, Y + R), (X + sg * 0.35 * k, Y + 0.85 * k), (X + sg * 0.55 * k, Y + R)],
            FIG, 0.35, layer="people")
    pg.line([(X - sg * 0.1 * k, Y + 0.8 * k), (X, Y + R)], FIG, 0.35, layer="people")
    body = [(-0.18, 0.80), (0.02, 0.80), (0.30, 1.20), (0.40, 1.48), (0.30, 1.52), (0.20, 1.40), (0.36, 0.90),
            (0.10, 0.62), (0.0, 0.40), (-0.06, 0.42), (0.04, 0.68), (-0.10, 0.95), (0.02, 1.45), (-0.10, 1.45)]
    pg.poly([[(X + sg * bx * k, Y + by * k) for bx, by in body]], fill=FIG, stroke=None, layer="people")
    pg.circle(X + sg * 0.30 * k, Y + 1.66 * k, 0.105 * k, fill=FIG, layer="people")




def existing_ground(pg, S):
    """The survey ground, dashed, where the design departs from it by more than 5 cm."""
    s_l, s_r = S.d["s_from"], S.d["s_to"]
    n = int(abs(s_r - s_l) / 0.25)
    run, runs = [], []
    for i in range(n + 1):
        s = s_l + (s_r - s_l) * i / n
        if abs(S.ex(s) - S.surf(s)) > 0.05 and min(S.d["s_from"], S.d["s_to"]) <= s:
            run.append(S.P(s, S.ex(s)))
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    for r in runs:
        if len(r) >= 2:
            pg.line(r, INK2, 0.18, dash=[1.2, 0.8], layer="existing ground")


def survey_marks(pg, S, notes):
    for s, what, z in SURVEY_MARKS:
        if not (S.lo <= s <= S.hi):
            continue
        if z is None:
            X, Y = S.P(s, S.ex(s))
            pg.poly([[(X - 0.9, Y - 1.6), (X + 0.9, Y - 1.6), (X, Y)]], fill=GREY, stroke=None, layer="survey")
            pg.text("%s %.2f" % (what, s), X, Y - 3.6, 1.6, GREY, align="C", layer="survey")
        else:
            X, Y = S.P(s, z)
            pg.line([(X - 0.8, Y), (X + 0.8, Y)], GREY, 0.15, layer="survey")
            pg.line([(X, Y - 0.8), (X, Y + 0.8)], GREY, 0.15, layer="survey")
            pg.text("%.2f" % z, X + 1.0, Y + 0.6, 1.6, GREY, layer="survey")


# ================================================================ callouts, dimensions, band
def place_labels(S, items, size):
    """Rows for the callouts: no overlaps, no leader through a label (greedy, left to right)."""
    placed = []
    for x, y_anchor, txt in sorted(items, key=lambda t: t[0]):
        lines = wrap(txt, 18)
        w = max(text_w(l, size) for l in lines) + 2.0
        for row in range(8):
            x0, x1 = x - w / 2, x + w / 2
            ok = True
            for p in placed:
                if p["row"] == row and not (x1 < p["x0"] or x0 > p["x1"]):
                    ok = False
                if p["row"] > row and x0 - 0.8 <= p["x"] <= x1 + 0.8:
                    ok = False
                if p["row"] < row and p["x0"] - 0.8 <= x <= p["x1"] + 0.8:
                    ok = False
            if ok:
                placed.append(dict(x=x, y=y_anchor, x0=x0, x1=x1, row=row, lines=lines))
                break
    return placed


def callouts(pg, S, placed, ybase, size):
    gap = size * 2 * 1.25 + 3.0
    for p in placed:
        yl = ybase + p["row"] * gap
        for i, l in enumerate(p["lines"]):
            pg.text(l, p["x"], yl + (len(p["lines"]) - 1 - i) * size * 1.2, size, INK, align="C", layer="callouts")
        pg.line([(p["x"], yl - 1.2), (p["x"], p["y"])], INK2, 0.1, dash=[0.5, 0.5], layer="callouts")
        pg.circle(p["x"], p["y"], 0.45, fill=INK, layer="callouts")


def dims(pg, S, y):
    """Bottom chain: the design widths in cm (red; water board v1.14, was mm), ticks at every boundary."""
    bounds = []
    for sa, sb, z, mat, lab in S.flats:
        bounds += [sa, sb]
    ra, rb = S.d["regrade"]
    bounds += [rb, STRIP[0], STRIP[1]]
    bounds = sorted(set(round(b, 3) for b in bounds if S.lo <= b <= S.hi), key=lambda b: S.X(b))
    xs = [S.X(b) for b in bounds]
    pg.line([(xs[0], y), (xs[-1], y)], DIM, 0.12, layer="dimensions")
    for X in xs:
        pg.line([(X - 0.8, y - 0.8), (X + 0.8, y + 0.8)], DIM, 0.2, layer="dimensions")
        pg.line([(X, y - 1.2), (X, y + 1.2)], DIM, 0.1, layer="dimensions")
    for i in range(len(bounds) - 1):          # water board v1.14 (Aras 27 Oct): the widths in cm, 7.5 pt
        cm = abs(bounds[i + 1] - bounds[i]) * 100.0
        pg.text("%d" % round(cm), (xs[i] + xs[i + 1]) / 2, y + 1.0, 2.65, DIM, align="C", layer="dimensions")
    pg.text("cm", xs[-1] + 2.0, y - 0.9, 2.65, DIM, layer="dimensions")


def vdims(pg, S, levels, x):
    """Right chain: level differences in mm, thin red lines from each level, absolute levels beside the ticks."""
    lv = sorted(set(round(z, 3) for z, _ in levels))
    names = dict((round(z, 3), n) for z, n in levels)
    ys = [S.Y(z) for z in lv]
    pg.line([(x, ys[0]), (x, ys[-1])], DIM, 0.12, layer="dimensions")
    for z, Y in zip(lv, ys):
        pg.line([(x - 6.0, Y), (x + 1.2, Y)], DIM, 0.08, layer="dimensions")
        pg.line([(x - 0.8, Y - 0.8), (x + 0.8, Y + 0.8)], DIM, 0.2, layer="dimensions")
        pg.text("%+.2f %s" % (z, names[z]), x + 12.0, Y - 0.6, 1.6, GREY, layer="dimensions")
    for i in range(len(lv) - 1):
        pg.text("%d" % round((lv[i + 1] - lv[i]) * 1000), x + 1.5, (ys[i] + ys[i + 1]) / 2 - 0.7, 1.9, DIM,
                layer="dimensions")


def swatch(pg, x0, x1, y, h, mat, seed):
    ring = [(x0, y), (x1, y), (x1, y + h), (x0, y + h)]
    r = rng("sw", seed, round(x0, 2))
    base = {"veg": "6F8F45", "asphalt": ASPHALT, "concrete": "C9C8C3", "deck": "A97E52", "lavender": "8C7AA8",
            "gravel": "B9B1A2", "water": "9CC7DE"}.get(mat, "CCCCCC")
    pg.poly([ring], fill=base, stroke=None, layer="band")
    area = (x1 - x0) * h
    if mat in ("veg", "lavender"):
        for _ in range(int(area * 1.2)):
            X, Y = x0 + r.random() * (x1 - x0), y + r.random() * h
            col = ["4E6B30", "8DAE5E", "B6CF86", "3E5626"][int(r.random() * 4)]
            if mat == "lavender" and r.random() < 0.35:
                col = "B9A3D8"
            R = 0.25 + r.random() * 0.45
            pg.poly([_tree_blob(X, Y, R, r.random, 6)], fill=col, stroke=None, layer="band")
    elif mat == "deck":
        yy = y + 0.9
        while yy < y + h:
            pg.line([(x0, yy), (x1, yy)], "7E5A38", 0.15, layer="band")
            yy += 1.8
        for _ in range(int(area * 0.15)):
            X, Y = x0 + r.random() * (x1 - x0), y + r.random() * h
            pg.line([(X, Y), (min(x1, X + 3 + r.random() * 6), Y)], "8E6A45", 0.08, layer="band")
    elif mat in ("asphalt", "concrete", "gravel"):
        cols = {"asphalt": ["7E3029", "C46A5B", "93413A"], "concrete": ["AFAEA8", "DDDCD7", "9C9B95"],
                "gravel": ["8E8573", "D2CBBE", "A49A86"]}[mat]
        for _ in range(int(area * (2.5 if mat == "gravel" else 3.0))):
            X, Y = x0 + r.random() * (x1 - x0), y + r.random() * h
            R = 0.12 + r.random() * (0.5 if mat == "gravel" else 0.18)
            pg.poly([_tree_blob(X, Y, R, r.random, 5)], fill=cols[int(r.random() * 3)], stroke=None, layer="band")
    elif mat == "water":
        yy = y + 0.8
        while yy < y + h:
            pg.line([(x0, yy), (x1, yy)], "6FA7C8", 0.12, layer="band")
            yy += 1.4


def band(pg, S, y, h=9.0):
    items = [(sa, sb, mat, lab) for sa, sb, z, mat, lab in S.flats] + list(S.d["band_more"])
    ra, rb = S.d["regrade"]
    items.append((ra, rb, "gravel", "Stream gravel"))
    items.sort(key=lambda t: S.X(t[0]) + S.X(t[1]))
    merged = []
    for a, b, mat, lab in items:                               # neighbours with the same label become one swatch
        if merged and merged[-1][3] == lab and abs(S.X(merged[-1][1]) - S.X(a)) < 0.5:
            merged[-1] = (merged[-1][0], b, mat, lab)
        else:
            merged.append((a, b, mat, lab))
    drop = 0.0                                # water board v1.14: 7.5 pt names, every other one a row lower
    for j, (a, b, mat, lab) in enumerate(merged):
        x0, x1 = sorted((S.X(a), S.X(b)))
        swatch(pg, x0, x1, y, h, mat, S.d["key"])
        lines = wrap(lab, max(6, int((x1 - x0 + 4.0) / 1.5)))
        y0 = y - 3.6 - (drop if j % 2 else 0.0)
        for i, l in enumerate(lines):
            pg.text(l, (x0 + x1) / 2, y0 - i * 3.4, 2.65, INK2, align="C", layer="band")
        if j % 2 == 0:
            drop = len(lines) * 3.4 + 0.8


# ================================================================ one section
def draw_section(pg, S, x_left, y_top, notes, sea):
    d = S.d
    size = 2.65                               # water board v1.14: callouts at 7.5 pt (was 2.3 mm)
    # vertical extents
    tops = [S.surf(t[0]) + t[2] for t in d["trees"]] + [DRY + 1.1]
    if d.get("pergola"):
        tops.append(DRY + max(p[2] for p in d["pergola"]["plates"]) + 0.1)
    z_top = max(tops)
    items = []
    for s, z, txt in d["callouts"]:
        items.append((s, z, txt))
    S.X0 = x_left
    # labels first (rows), positions in page x need X0 only
    tmp = [(S.X(s), 0.0, txt) for s, z, txt in items]
    placed = place_labels(S, tmp, size)
    rows = max(p["row"] for p in placed) + 1
    gap = size * 2 * 1.25 + 3.0
    title_h = 16.0
    label_h = rows * gap + 4.0
    S.Y0 = y_top - title_h - label_h - (z_top - S.zb) * K - 6.0
    # anchors in page y
    by_x = {}
    for s, z, txt in items:
        by_x[round(S.X(s), 3)] = (s, z)
    for p in placed:
        s, z = by_x[round(p["x"], 3)]
        if z is None:
            z = S.surf(s) + 0.02
        p["y"] = S.Y(z)
    # title
    pg.text(d["title"] + "  " + d["side"], x_left, y_top - 6.0, 5.0, INK, bold=True, layer="title")
    pg.text("SCALE 1:%.0f" % SCALE, x_left, y_top - 11.5, 3.6, INK, layer="title")
    pg.text("S4 · s %.0f-%.0f m · %s" % (d["s_from"], d["s_to"], d["look"]), x_left + 34.0, y_top - 11.5, 2.0,
            INK2, layer="title")              # board v1.8: "ground: survey, built: design" is in the notes line
    # back to front
    for s, r_, h, kind in d["trees"]:
        g = S.surf(s)
        if g < Q500 - 1e-6:
            notes.append("Section %s: tree at s %.1f skipped, it would stand below the Q500 line." % (d["key"], s))
            continue
        X, Y = S.P(s, g)
        veg_tree(pg, X, Y, h * K, 2 * r_ * K, (d["key"], round(s, 2)), flip=(S.dir < 0))
    people = list(sea["people"].get(d["key"], []))
    bal = d.get("balcony")
    on_bal = []
    if bal:
        for p in people:
            if p[1] == 3 and min(bal["s0"], bal["s1"]) <= p[0] <= max(bal["s0"], bal["s1"]):
                on_bal.append((p[0], 5, p[2]))
        people = [p for p in people if not (p[1] == 3 and min(bal["s0"], bal["s1"]) <= p[0] <= max(bal["s0"], bal["s1"]))]
    if d.get("pergola"):
        pergola(pg, S, d["pergola"])
    if bal:
        balcony(pg, S, bal, on_bal)
    level_line(pg, S, Q500, "Q500 %+.2f (calculated on this cut)" % Q500, [2.0, 1.0])
    level_line(pg, S, Q100, "Q100 %+.2f (calculated on this cut)" % Q100, [0.8, 0.8])
    filled = [w for w in sea["water"] if w[1]]
    for z, fill_, lab, dash in sea["water"]:
        if not fill_:
            level_line(pg, S, z, lab % z, dash, colour=WATER_LINE)
    poche(pg, S)
    soft_ground(pg, S)
    walls_and_slabs(pg, S)
    existing_ground(pg, S)
    survey_marks(pg, S, notes)
    for a, b in d["grass"]:
        tufts(pg, S, a, b)
    for a, b in d["lavender"]:
        lavender(pg, S, a, b)
    for s, h, w in d["shrubs"]:
        shrub(pg, S, s, h, w)
    for a, b, h in d["reeds"]:
        reeds(pg, S, a, b, h)
    for a, b in d["iris"]:
        iris(pg, S, a, b)
    # the season's water over the bed and the plant feet (see-through), then the people, then the cut railings
    for z, fill_, lab, dash in filled:
        water(pg, S, z)
        level_line(pg, S, z, lab % z, None, colour=FLOOD)
    if sea["strip_held"]:
        water(pg, S, THALWEG[1])
        if not filled:
            level_line(pg, S, THALWEG[1], "continuous strip %+.2f, 0.30 m (design)" % THALWEG[1], None, colour=FLOOD)
    wl = max([THALWEG[1] if sea["strip_held"] else -99.0] + [w[0] for w in filled])
    for s, kind, flip in people:
        g = S.surf(s)
        if g < wl + 0.02 and kind != 8:
            notes.append("%s, section %s: person at s %.1f left out, the ground there is under water." % (
                sea["name"], d["key"], s))
            continue
        if g < Q500 and not FIGURES_IN_FLOOD_REACH:
            continue
        figure(pg, S, s, kind, flip)
    for s, flip in sea["bikes"].get(d["key"], []):
        if S.surf(s) >= Q500 or FIGURES_IN_FLOOD_REACH:
            bike(pg, S, s, flip)
    for s, side in d["rails"]:
        handrail(pg, S, s + side * 0.15 * S.dir, S.surf(s + side * 0.3 * S.dir))
    # callouts
    ybase = S.Y(z_top) + 6.0
    callouts(pg, S, placed, ybase, size)
    # dimensions and the material band
    yd = S.Y(S.zb) - 5.0
    dims(pg, S, yd)
    band(pg, S, yd - 15.0)
    x_r = S.X(d["s_to"]) + 8.0
    lv = [(THALWEG[1], "bed low point (survey)"), (THALWEG[1] - STRIP[2], "strip bottom (design)")]
    lv += [(w[0], "water, %s (calculated)" % sea["key"]) for w in sea["water"]]
    for sa, sb, z, mat, lab in S.flats:
        if z is not None:
            lv.append((z, "design"))
    lv.append((DRY + 1.10, "handrail top (design)"))
    if d.get("pergola"):
        lv.append((DRY + max(p[2] for p in d["pergola"]["plates"]), "shading top (design)"))
    vdims(pg, S, lv, x_r)
    return yd - 15.0 - 9.0


# ================================================================ Rhino side (only when run inside Rhino)
def rhino_inputs(log):
    """S4 from the open file and a fresh cut of the survey ground along it. None where missing."""
    try:
        import Rhino
        import System
    except Exception:
        return None, None, None
    doc = Rhino.RhinoDoc.ActiveDoc
    if doc is None:
        return None, None, None
    A, B = S4_A, S4_B
    found = "embedded coordinates"
    try:
        o = doc.Objects.FindId(System.Guid(S4_ID))
        cands = [o] if o is not None else []
        for L in doc.Layers:
            if L.Name.lower() == "sec_lines" and not L.IsDeleted:
                cands += list(doc.Objects.FindByLayer(L) or [])
        for o in cands:
            c = o.Geometry
            if not hasattr(c, "PointAtStart"):
                continue
            p, q = c.PointAtStart, c.PointAtEnd
            for (u, v) in (((p.X, p.Y), (q.X, q.Y)), ((q.X, q.Y), (p.X, p.Y))):
                if math.hypot(u[0] - A[0], u[1] - A[1]) < 1.0 and math.hypot(v[0] - B[0], v[1] - B[1]) < 1.0:
                    A, B, found = u, v, "the open file (sec_lines)"
                    break
            if found != "embedded coordinates":
                break
    except Exception as e:
        log.append("S4 search failed (%s); embedded coordinates used." % e)
    log.append("Section line S4 taken from %s." % found)
    L = math.hypot(B[0] - A[0], B[1] - A[1])
    ux, uy = (B[0] - A[0]) / L, (B[1] - A[1]) / L

    def su(x, y):
        return (x - A[0]) * ux + (y - A[1]) * uy, -(x - A[0]) * uy + (y - A[1]) * ux

    # ---- survey points along the cut
    names = ["NOKTA_TAKEOMETRI", "EGRI_1M", "EGRI_2M", "EGRI_ARA", "SEV_UST", "SEV_ALT", "HIDRO_DERE_SULU"]
    pts = {}
    count = {}
    try:
        for Ly in doc.Layers:
            if Ly.IsDeleted or Ly.Name not in names:
                continue
            for o in doc.Objects.FindByLayer(Ly) or []:
                g = o.Geometry
                P = []
                if isinstance(g, Rhino.Geometry.Point):
                    P = [g.Location]
                elif isinstance(g, Rhino.Geometry.Curve):
                    ok, pl = g.TryGetPolyline()
                    if ok:
                        P = list(pl)
                    else:
                        nc = g.ToNurbsCurve()
                        P = [cp.Location for cp in nc.Points] if nc.Degree == 1 else \
                            [g.PointAt(t) for t in g.DivideByLength(1.0, True)]
                for p in P:
                    if p.Z <= 1.0:
                        continue
                    s, off = su(p.X, p.Y)
                    if 480.0 <= s <= 740.0 and abs(off) <= 60.0:
                        pts[(round(p.X, 2), round(p.Y, 2))] = p.Z
                        count[Ly.Name] = count.get(Ly.Name, 0) + 1
    except Exception as e:
        log.append("Reading survey heights failed: %s" % e)
    prof = None
    if len(pts) >= 100:
        try:
            import Grasshopper.Kernel.Geometry as GKG
            keys = list(pts.keys())
            nodes = GKG.Node2List()
            for (x, y) in keys:
                nodes.Append(GKG.Node2(x - A[0], y - A[1]))
            faces = GKG.Delaunay.Solver.Solve_Faces(nodes, 1)
            tris = []
            for f in faces:
                a, b, c = keys[f.A], keys[f.B], keys[f.C]
                tris.append((a, b, c))
            Z = []
            s0, ds, n = PROFILE_S0, PROFILE_DS, len(PROFILE_Z)
            cell = {}
            for t in tris:
                xs = [p[0] for p in t]
                ys = [p[1] for p in t]
                for i in range(int(min(xs) // 5), int(max(xs) // 5) + 1):
                    for j in range(int(min(ys) // 5), int(max(ys) // 5) + 1):
                        cell.setdefault((i, j), []).append(t)
            miss = 0
            for i in range(n):
                s = s0 + i * ds
                x, y = A[0] + ux * s, A[1] + uy * s
                z = None
                for (a, b, c) in cell.get((int(x // 5), int(y // 5)), []):
                    det = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
                    if abs(det) < 1e-12:
                        continue
                    l1 = ((b[1] - c[1]) * (x - c[0]) + (c[0] - b[0]) * (y - c[1])) / det
                    l2 = ((c[1] - a[1]) * (x - c[0]) + (a[0] - c[0]) * (y - c[1])) / det
                    l3 = 1.0 - l1 - l2
                    if min(l1, l2, l3) >= -1e-9:
                        z = l1 * pts[a] + l2 * pts[b] + l3 * pts[c]
                        break
                if z is None:
                    miss += 1
                    z = PROFILE_Z[i]
                Z.append(z)
            dmax = max(abs(Z[i] - PROFILE_Z[i]) for i in range(n))
            prof = (s0, ds, Z)
            log.append("Ground cut again from the open file: %d survey heights (%s); largest difference from the "
                       "embedded profile %.3f m%s." % (len(pts), ", ".join("%s %d" % kv for kv in sorted(count.items())),
                                                       dmax, (", %d stations outside the TIN kept embedded" % miss) if miss else ""))
        except Exception as e:
            log.append("Ground re-cut failed (%s); embedded profile used." % e)
    else:
        log.append("Survey height layers not found in the open file (%d heights); embedded profile used "
                   "(cut from Nil's survey DXF)." % len(pts))
    return (A, B), prof
'''
