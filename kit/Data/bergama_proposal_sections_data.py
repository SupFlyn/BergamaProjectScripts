# Built-in data of bergama_proposal_sections (made by tools/build.py from src/bergama_proposal_sections/data/; do not edit by hand)

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
#   depth_month   (round 3, A2, DATA-1; S4 only so far) mean water depth above the bed per month, Jan..Dec (m), value =
#                 {"komurcu": [12], "ilica": [12]} (the two gauge routes of the CSV); read with level_month_depth() /
#                 level_season_depth() (levels.py), never with level(). Depths, so they hold on either S4 datum (N1)
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
# N1 a (Aras 31 Oct 21:37, round 3) SUPERSEDES D4 b for S4: survey datum everywhere (bed +43.59, average flow +43.83,
# Q100 +45.84, Q500 +46.19; bank heights from the survey bed). D4 b below still holds for S1, S7, S8.
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
        'bed': {'value': 43.59, 'status': 's', 'source': "N1 a (Aras 31 Oct 21:37, round 3): survey datum everywhere for S4: levels.json +43.59 (survey TIN low point, tacheometric point 0.3 m away; the datum the Q100/Q500 and average-flow depths were computed on, rain_river README l.25). Replaces D4 b +42.48"},
        'bed_width_cm': {'value': 2600, 'status': 'i', 'source': 'no pair of survey stream lines at this cut: width of the TIN floor within 0.5 m of the bed on the right-angle section'},
        'NE': {
            'type': 'loose_earth',
            'top': {'value': 45.64, 'status': 'i', 'source': 'survey TIN, res_bank_top crest, 31.0 m out across the stream; nearest survey height 5.9 m away'},
            'height': {'value': 2.05, 'status': 'c', 'source': 'bank top 45.64 minus the survey bed 43.59 (N1 a, 31 Oct)'},
        },
        'SW': {
            'type': 'embankment',
            'top': {'value': 47.35, 'status': 's', 'source': 'survey TIN, survey bank-top line SEV_UST (no height on the line: TIN there), 30.3 m out across the stream; nearest survey height 0.9 m away'},
            'height': {'value': 3.76, 'status': 'c', 'source': 'bank top 47.35 minus the survey bed 43.59 (N1 a, 31 Oct)'},
            'angle_deg': {'value': 7.0, 'status': 'i', 'source': "between the survey's slope lines SEV_ALT (toe) and SEV_UST (top) on the cut"},
        },
        'terraces': [
            {'side': 'NE', 'from_m': 1.0, 'to_m': 28.0, 'level': {'value': 44.17, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 0.58 m above the bed'}},
            {'side': 'SW', 'from_m': 33.0, 'to_m': 40.0, 'level': {'value': 47.15, 'status': 'i', 'source': 'level shelf (<= 6 cm per m over >= 4 m) on the survey TIN, 3.56 m above the bed'}},
        ],
        'q100': {'value': 45.84, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q100 205.2 m3/s'},
        'q500': {'value': 46.19, 'status': 'c', 'source': 'Manning n 0.050 on the surveyed right-angle section, DSI Q500 263.33 m3/s'},
        'avg_flow_depth': {'value': 0.24, 'status': 'c', 'source': "research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section S4 detail cut (chainage 7,818 m), its bed +43.59 (N1 a)"},
        'avg_flow': {'value': 43.83, 'status': 'c', 'source': "bed + avg_flow_depth (water level at the mean yearly flow); research/rain_river_levels tables/A3s_monthly_mean_depth_surveyed_sections.csv: Manning n 0.050 normal depth on the surveyed right-angle section, DSİ gauge flows 2016-2021 (Kömürcü D04A063, Ilıca D04A053) area-scaled to the Selinos (101 km²); mean flow ≈ 0.66 m³/s (rain_river README §2); depth read between the two monthly (flow, depth) pairs that bracket it; this cut = the surveyed section S4 detail cut (chainage 7,818 m): survey bed +43.59 + 0.24 (N1 a, 31 Oct)"},
        'depth_month': {'value': {'komurcu': [0.352, 0.345, 0.32, 0.282, 0.212, 0.161, 0.114, 0.073, 0.05, 0.115, 0.143, 0.203],
                                  'ilica': [0.432, 0.35, 0.304, 0.251, 0.159, 0.125, 0.08, 0.036, 0.068, 0.106, 0.165, 0.199]},
                        'status': 'c', 'source': "research/rain_river_levels/tables/A3s_monthly_mean_depth_surveyed_sections.csv rows S4_detail_cut Jan-Dec, columns depth_via_Komurcu_m and depth_via_Ilica_m (Manning n 0.050 normal depth on the surveyed S4 detail cut, DSİ gauge flows 2016-2021 area-scaled to the Selinos, 101 km²; rain_river README §2); below ~0.3 m indicative (README l.36)"},
        'note': 'N1 a (Aras 31 Oct 21:37): survey datum for every S4 level (bed +43.59, avg +43.83, Q100 +45.84, Q500 +46.19); the D4 b bed +42.48 (29 Oct) is retired. Pages draw the bed from the survey profile (water board DETAIL_SRC PROFILE_Z), low point +43.59.',
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

#@@ NAMES
# ---- Names table (round 3, A2, 31 Oct 2026; G16 / D9 "real names everywhere"): ONE spelling per bridge and place ----
# Read it through ../common/names.py, never directly: include this file first, then names.py:
#   #@include ../common/data/NAMES.py
#   #@include ../common/names.py
# Plain Python data (exec'd by tools/build.py's bergama_data): no imports, no functions, one assignment.
# K-codes stay internal keys only: never printed as a main label. Stream order (upstream first) = "order".
# Spellings (plan_findings/NAMES_SQUIGGLE_TREES.md DATA-3; chosen: the official public name = the bus stop name):
#   K3 Tabak Köprüsü        Kültür Envanteri "Tabak Köprüsü" (library/research/selinos_site_history_inaccessible_edges_v1.md
#                           l.62); survey label "Tabakhane Köprüsü" is the same bridge (selinos_bergama_history_context_v1.md l.143)
#   K4 Ulucami Önü Köprüsü  KGM plaque on site, photo IMG_5804 (inaccessible_edges_v1.md l.217); history_context_v1.md l.141
#   K5 Üç Kemer Köprüsü     Visit İzmir (İzmir BB), Destinasyon 10228 (history_context_v1.md l.270)
#   K6 road bridge          Adnan Menderes Bulvarı (Aras 1 Nov 07:30: "it is bulvar"; inaccessible_edges_v1.md l.176 has "Cd."); no proper name found
#   K1, K2                  no source name: descriptive names (G16)
# Chainage m along the stream: CL code.py:211 (K1 / K2 about 25 m apart upstream; their order unverified).
# Banks (D6, Aras 31 Oct 20:45: "fine that way"; p20 already prints them): NE = left bank looking downstream = north
# bank = the Kale side; SW = south bank = the bazaar side.
# Landmarks (round 4, S1, 1 Nov 2026; G-R4-11 / PALL.3, PLAN §4.6): the TURKISH proper name is printed, never an
# English translation ("Red Hall" -> Kızıl Avlu, "Acropolis" -> Akropol, "Bazaar" -> Arasta); "descr" is an optional
# English descriptor that may FOLLOW the name (landmark_name(key, descr=True) -> "Kızıl Avlu · Hadrian's temple").
# Spellings as the project's sources write them; "src" = where (h01 = library/research/
# selinos_bergama_history_context_v1.md, table §5 row; survey = a label in the course survey). Descriptors are taken
# from texts already in the booklet (p20 heritage cards, city link), nothing new. One spelling of Ulucami (the brief's;
# "Ulu Cami" / "Ulu Camii" drift removed); source TITLES on the Sources page stay as published.
# Round 5 S2 (1 Nov 2026; G-R5-3, A11, N6 a): "at" = the survey point of the place (the label or position its "src"
# names; Asklepion, Akropol, Teleferik, Bergama Müzesi = basemap.py BASEMAP_REACH, the heritage loop's positions);
# "km" = rank on key maps (1 first; only rows with "at" and "km" can appear on a key map); "alias" = other spellings
# that name the same place anywhere (whole name, lower case, İ as i); "alias_near" = generic words that name it only
# within 60 m of "at" (survey "Hamam" is a type word elsewhere). Read through landmark_match / place_label.
# N6 b (Aras 1 Nov 22:44): "Papuçcular Arastası" as the survey spells it (key pabuccular_arastasi unchanged).
NAMES = {
    "bridges": {
        "K1": {"name": u"side inlet crossing", "short": u"side inlet crossing", "order": 1, "proper": False},
        "K2": {"name": u"small crossing", "short": u"small crossing", "order": 2, "proper": False},
        "K4": {"name": u"Ulucami Önü Köprüsü", "short": u"Ulucami Önü", "order": 3, "proper": True, "chainage_m": 467},
        "K3": {"name": u"Tabak Köprüsü", "short": u"Tabak", "order": 4, "proper": True, "chainage_m": 709},
        "K5": {"name": u"Üç Kemer Köprüsü", "short": u"Üç Kemer", "order": 5, "proper": True, "chainage_m": 1126},
        "K6": {"name": u"Adnan Menderes Bulvarı road bridge", "short": u"road bridge", "order": 6, "proper": False,
               "chainage_m": 1767},
    },
    "places": {
        "stream": u"Selinos stream",
        "bank_NE": u"Kale side · north bank",
        "bank_SW": u"bazaar side · south bank",
        "bank_NE_short": u"north bank",
        "bank_SW_short": u"south bank",
        "side_NE": u"Kale side",
        "side_SW": u"bazaar side",
    },
    "landmarks": {
        "kizil_avlu": {"name": u"Kızıl Avlu", "descr": u"Hadrian's temple",
                       "src": u"survey label 'Kızıl Avlu' (30203.92, 31974.82); h01 §5 P02; Kültür Envanteri 'Kızıl Avlu'",
                       "at": (30203.92, 31974.82), "km": 1, "alias": (u"red hall", u"red basilica")},
        "akropol": {"name": u"Akropol", "descr": u"the Hellenistic city on the hill",
                    "src": u"site board HER_BEYOND (OSM way 1410335587, Trajaneum)",
                    "at": (30209.0, 33177.0), "km": 4, "alias": (u"acropolis",)},
        "ulucami": {"name": u"Ulucami", "descr": u"mosque of 1398-99",
                    "src": u"h01 §5 P05 (survey 'Ulu Camii' (29844.2, 32313.3)); Visit İzmir 'Bergama Ulu (Yıldırım) "
                           u"Mosque'; spelling = the brief's (G-R4-11) and K4's name",
                    "at": (29844.17, 32313.30), "km": 2, "alias": (u"ulu camii", u"ulu cami", u"ulu camı")},
        "tabaklar_hamami": {"name": u"Tabaklar Hamamı", "descr": u"the tanners' bath",
                            "src": u"h01 §5 P07 (survey 'Hamam' (29890.4, 32243.6))",
                            "at": (29890.4, 32243.6), "km": 8, "alias_near": (u"hamam",)},
        "arasta": {"name": u"Arasta", "descr": u"the old bazaar",
                   "src": u"site board HER_STOPS 'bazaar' (Visit İzmir 'Mevlâna Hacı Hekim Hammam')"},
        "cizmeciler_arastasi": {"name": u"Çizmeciler Arastası", "descr": None,
                                "src": u"survey label (29794.31, 31929.85)",
                                "at": (29794.31, 31929.85), "km": 10},
        "pabuccular_arastasi": {"name": u"Papuçcular Arastası", "descr": None, "src": u"survey label 'Papuçcular Arastası' "
                                       u"(29802.17, 31946.53); h02 s32 (city link stop 1) spells it 'Pabuççular "
                                       u"Arastası' (round 5 N6 b, Aras 1 Nov 22:44: the survey spelling is printed; "
                                       u"the key stays as callers use it)",
                                "at": (29802.17, 31946.53), "km": 9, "alias": (u"pabuççular arastası",)},
        "istiklal_meydani": {"name": u"İstiklal Meydanı", "descr": u"square",
                             "src": u"h01 §5 P16 (survey label (29990.0, 32030.5))",
                             "at": (29990.0, 32030.5), "km": 3},
        "adnan_menderes_bulvari": {"name": u"Adnan Menderes Bulvarı", "descr": None,
                                   "src": u"Aras 1 Nov 07:30 ('it is bulvar'); K6 row above"},
        "kinik_caddesi": {"name": u"Kınık Caddesi", "descr": None,
                          "src": u"OpenStreetMap extract of 28 Jul 2026 (common/city_spine.py MAIN_SPINE)"},
        "bankalar_caddesi": {"name": u"Bankalar Caddesi", "descr": None,
                             "src": u"OpenStreetMap extract of 28 Jul 2026 (common/city_spine.py MAIN_SPINE)"},
        "bergama_muzesi": {"name": u"Bergama Müzesi", "descr": u"museum of 1936",
                           "src": u"Kültür Envanteri KE 3946 'Bergama Müzesi' (h01 s86)",
                           "at": (29560.0, 31358.0), "km": 6},
        "teleferik": {"name": u"Teleferik", "descr": u"cable car (2010)",
                      "src": u"site board HER_STOPS 'gondola' (OSM node 2295928011)",
                      "at": (30720.4, 32370.1), "km": 7},
        "asklepion": {"name": u"Asklepion", "descr": u"the healing sanctuary",
                      "src": u"h01 §5 P28; KTB 'The Archaeological Site of Asklepion' (h01 s114)",
                      "at": (29077.3, 31867.3), "km": 5},
        "trajan_tapinagi": {"name": u"Trajan Tapınağı",
                            "src": u"round 4 closing (G-R4-11): the form masterplan p21 already printed (p23_plan.py "
                                   u"move reason of the viewing terrace); the temple on the Akropol, OSM way 1410335587 "
                                   u"(masterplan 02c_corridor.py TRAJANEUM, h03 Q3); replaces 'Trajaneum' on p22; no "
                                   u"descriptor (none in the booklet's texts)"},
    },
}

#@@ SKETCH_SRC
SKETCH_SRC = r'''# The idea sketches of pr1_drawings v3.1 (concept sections, SKETCH style), run in their own namespace: pr1 baked them
# into Rhino; here the same calls make page items. The draw order is pr1's (bake order plus its lifts Z_*).
# Restored from commit f93d84b (28 Oct 2026, proposal sections v8.1) in round 6 (S6, proposal sections v20, 4 Nov 2026;
# BRIEF Q9, row 12). Round 6 edits: no hatches (marker = flat wash, no bed hatch, no earth strokes; BRIEF §3 common
# rules); every colour a host may set from common/hues.py (the new names below keep the 28 Oct values as defaults, so
# a host that sets nothing draws as before); KINDS records each item's kind and element (G6-9 nested groups);
# BRIDGE(code) gives the bridge's proper name (names table); label positions fixed where the 28 Oct page overlapped.
# Shared: bergama_agriculture_alternatives includes this file read-only (p17 plant ladder); only S6 edits it.
import math
ZP = []
ORDER = [0]
FORM = "A"
PEOPLE = True
NODE = None                                          # set by the board: the element numbers
CITE = None                                          # v3: set by the board: a source's number "[n]" (footer key)
ORIGIN = (0.0, 0.0)                                  # pr1 placed the sketches beside the site map; here at 0
TXT_K = [1.0]                                        # v7: every text (and its pictogram) at this multiple of its size; set by
                                                      # the board so the smallest word prints >= 7 pt on the one booklet page
GROUP = [0]                                          # v7: label group of the items being put (0: none, < 0: fixed, e.g. numbers)
NEXT_G = [0]                                         # v7: last label group number given out
KINDS = {}                                           # v20 (G6-9): ORDER number -> (sub, element) of each item put
SUB = ["other"]                                      # v20: the sub (Rhino layer name of pr1) of the item being put
ELEM = [None]                                        # v20: (kind, element name) while one element is drawn, else None
NEXT_E = [0]                                         # v20: element counter (unnamed elements get "<kind> <n>")
BRIDGE = None                                        # v20: set by the host: bridge code -> proper name (names table)
Q_TEXT = {}                                          # v20: set by the host: the Q500 words of each panel (level table)


def _hexc(c):
    return "%02X%02X%02X" % tuple(c)


def _put(item, z):
    ORDER[0] += 1
    ZP.append((ORDER[0] + z, ORDER[0], item, GROUP[0]))   # v7: + the label group (the board keeps labels apart)
    KINDS[ORDER[0]] = (SUB[0], ELEM[0])                    # v20 (G6-9): kind + element of this item (ZP shape kept)


def elem_open(kind, name=None):
    """v20 (G6-9): the items put from now on belong to one element of `kind` (trees, people, ...), named `name` or
    "<kind> <n>". Returns the previous element, for elem_close."""
    prev = ELEM[0]
    NEXT_E[0] += 1
    ELEM[0] = (kind, name or u"%s %d" % (kind, NEXT_E[0]))
    return prev


def elem_close(prev):
    ELEM[0] = prev


def _group():
    """v7: open a new label group unless one is open. Returns True if this call opened it (then it closes it)."""
    if GROUP[0]:
        return False
    NEXT_G[0] += 1
    GROUP[0] = NEXT_G[0]
    return True


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
    SUB[0] = sub
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
    SUB[0] = sub
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
    h = size_pt * 0.353 * TXT_K[0]
    own = _group()                                    # v7: one text (all its lines) = one label group
    pe = elem_open("labels", s.split("\n")[0][:40]) if ELEM[0] is None else ELEM[0]   # v20: one text = one element
    SUB[0] = sub
    for i, ln in enumerate(s.split("\n")):
        if ln.strip():
            q = P(o, x, y - i * h * 1.35)
            _put(("text", ln, q[0], q[1], h, _hexc(colour), bold, {"left": "L", "right": "R"}.get(just, "C"), None,
                  _hexc(mask) if mask else None), Z_TEXT)      # pr1's text mask: a halo in its colour
    if pe is not ELEM[0]:
        elem_close(pe)
    if own:
        GROUP[0] = 0


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
# v20 (round 6, G6-6): one name per thing the legend keys; defaults = the 28 Oct colours, the host sets the hue table's
ROUTE, SPILL, FAILSAFE_C, FARM_C, HER_C = ACCENT, ACCENT, ACCENT, ACCENT, HERITAGE
DRY_WW, DRY_PUB, DRY_AGR = SUN, SUN, SUN             # the dry tiers: terraces (water works), hub square + steps, garden
SUBHUB_C, BOARD_C, CAFE_C, WALL_C = SEC_PAVE, SEC_PAVE, HOUSE_WALL, STONE
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
    (and slightly turned), over a faint wash of the same colour: the key element of a sketch (example 4).
    v20 (round 6, no hatches): one flat wash in the colour at the strokes' opacity instead of the strokes."""
    wash(o, poly, sub, colour, alpha, z)
    return
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
    sketch(o, ring, "fail-safe", FAILSAFE_C, PEN_FINE, closed=True, over=0.0, amp=0.05, retrace=False, z=Z_LINE)
    sketch(o, [(x - 0.75 * r, y + 0.3 * r), (x - 0.1 * r, y + 0.3 * r), (x - 0.1 * r, y - 0.45 * r), (x + 0.75 * r, y - 0.45 * r)],
           "fail-safe", SKINK, PEN_FINE, over=0.0, amp=0.03, retrace=False, z=Z_LINE)
    hand_arrow(o, (x - 0.55 * r, y + 0.55 * r), (x + 0.25 * r, y - 0.15 * r), FAILSAFE_C, width=0.16, head=0.55, bend=-0.3)

def keyed(o, kind, s, x, y, size_pt, colour=None, sub="text", mask=None):
    """v3: a keyword callout led by a hand pictogram at its first line: "winter" (cloud and rain), "summer" (the
    sun) or "failsafe". The text starts a little to the right of x."""
    h = size_pt * 0.353 * TXT_K[0]
    own = _group()                                    # v7: the pictogram and its words move together
    cx, cy = x + 1.1 * h, y + 0.36 * h
    if kind == "winter":
        cloud_rain(o, cx, cy + 0.15 * h, 0.5 * h)
    elif kind == "summer":
        sun(o, cx, cy, 0.36 * h)
    elif kind == "failsafe":
        failsafe_mark(o, cx, cy, 0.62 * h)
    text(o, s, x + 2.4 * h, y, size_pt, colour, sub, mask=mask)
    if own:
        GROUP[0] = 0

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
    # v20 (round 6, no hatches; flat beige soil, BRIEF §3 SKETCH): the short earth strokes under the line are gone
    return surf

def sketch_tree(o, x, y, h, sp=None):
    """Loose tree: a crown of washes in the board's tree greens, a scribbled outline and a trunk with two limbs.
    v20 (G6-9/G6-10): one element "trees"; sp = the species the sketch names (None: generic, no species invented)."""
    pe = elem_open("trees", sp)
    _sketch_tree(o, x, y, h)
    elem_close(pe)


def _sketch_tree(o, x, y, h):
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
    pe = elem_open("people")
    fill(o, [(x + sg * bx * s, y + by * s) for bx, by in SA_FIGS[kind % len(SA_FIGS)]], "people", SITE_PEOPLE,
         alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)
    hx_, hy_, hr = SA_HEAD
    fill(o, [(x + sg * hx_ * s + hr * s * math.cos(6.283 * i / 12), y + hy_ * s + hr * s * math.sin(6.283 * i / 12))
             for i in range(12)], "people", SITE_PEOPLE, alpha=0.9, boundary=False, z=Z_PEOPLE, hand_=False)
    elem_close(pe)

def sketch_house(o, x0, x1, y, wall=6.0, pipe=False):
    """Context: an old town house beyond the street (board TYPO "traditional": stone base, hipped tile roof, deep
    eaves), generic, not surveyed. pipe=True adds the downpipe that takes its roof water to the street."""
    ev, rise = 0.9, 2.6
    pe = elem_open("buildings", u"house (context)")
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
    elem_close(pe)

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
    # v20 (round 6, no hatches): bed_hatch draws nothing (flat blue water bands, BRIEF §3 SKETCH)
    if line:
        sketch(o, [pts[0], pts[-1]], "water lines", SITE_WATER_D, PEN_FINE, over=0.0, retrace=False, z=Z_LINE)
    return pts

def label2(o, head, body, x, y, size_pt, colour=None, mask=None):
    """v7: a bold name line with plain lines under it, one label group (they move together)."""
    own = _group()
    text(o, head, x, y, size_pt, colour, "labels", bold=True, mask=mask)
    text(o, body, x, y - size_pt * 0.353 * TXT_K[0] * 1.35, size_pt, colour, "labels", mask=mask)
    if own:
        GROUP[0] = 0

def hub_route(o, gs, x0, x1, rise=1.4):
    """v7 (history D10): the walk between the dry walking hub square and the sub-hub in the bed: an accent dashed line
    just over the steps from x0 (hub side) to x1 (sub-hub side), its head at the sub-hub."""
    r = surface_between(gs, min(x0, x1), max(x0, x1), rise)
    if len(r) < 2:
        return
    r = r if x0 < x1 else r[::-1]
    sketch(o, r, "hub route", ROUTE, PEN_MED, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    (ax, ay), (bx, by) = r[-2], r[-1]
    L = math.hypot(bx - ax, by - ay) or 1.0
    hand_arrow(o, (bx - (bx - ax) / L * 4.0, by - (by - ay) / L * 4.0), (bx, by), ROUTE, width=0.4, head=1.6)

def concept_aras_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_aras_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_aras_sketch():
    """PROBLEM: the bed is dry in summer, the winter runoff leaves the streets. MOVE: the bank becomes a cascade that
    holds the winter water, cleans it in reed basins and gives it back to the summer stream. v7: shorter words."""
    o, w = ORIGIN, 200
    g = [(0, 8), (0, 64), (34, 64), (34, 52), (68, 52), (68, 40), (102, 40), (102, 28), (130, 28)] + bank((130, 28), (140, 12))[1:] + \
        [(170, 12), (170, 28), (w, 28), (w, 8)]
    basins = ((40, 52), (74, 40), (108, 28))
    # the summer strip runs in a low-flow channel cut into the bed (v2.8: 150-160, 2.2 deep)
    gs = sketch_ground(o, notch(g, [(x0, x0 + 22, y, 5) for x0, y in basins] + [(150, 160, 12, 2.2)]))
    # winter: rain on the old town's roofs and street (context house generic, not surveyed)
    rain(o, 6, 33, 67.5, 73.5, 16)
    sketch_house(o, 15, 27, 65.3, wall=5.0, pipe=True)
    road(o, 0, 30, 64, "ROAD", ly=61.5, mask=SOIL)          # v5: no caveat word; v20: survey = course file, no mark
    # Q500's reach first (solid wash), so the basins' water and reeds stay on top of it
    for pc in [under_level(gs, 102, w, 31.5)]:
        if pc:
            wash(o, pc, "flood", FLOOD_WASH, FLOOD_ALPHA)
    # the move: the cascade of reed basins (marker band = what holds and cleans the water)
    for x0, y in basins:
        water_level(o, gs, x0 + 11, y - 0.4, W_WIN)
        reeds(o, x0 + 1, x0 + 21, y - 5, 3.2)
    for pc in band(gs, 34, 130, 1.6):
        marker(o, pc, "terraces", DRY_WW, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    sketch_tree(o, 65, 52, 9); sketch_tree(o, 99, 40, 7)    # on the strips between the basins, above Q500's reach
    # (v20: no species named for these two in any source: generic, G6-10)
    # summer: the stream (dry bed today) gets the clean water back
    water_level(o, gs, 155, 19, W_WIN, bed_hatch=True)
    water_level(o, gs, 155, 12, W_EXT, line=False)
    sun(o, 188, 58)
    sketch_person(o, 13, 65.3, kind=1); sketch_person(o, 70.8, 40)               # never inside water or the Q500 reach
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    keyed(o, "winter", "winter flow", 172, 24, 5.6, W_EXT, "water")
    keyed(o, "summer", "low-flow strip\ntoday: dry bed", 172, 19, 5.6, W_EXT, "water")
    sketch(o, [(102, 31.5), (w, 31.5)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 123.8, 31.5, W_EXT, "flood lines")
    # v3 fix (audit problem 3): the surveyed cut keeps Q500 inside the banks; v20: the words come from the host's level
    # table (LEVELS W1, read live: Q_TEXT["up"]); raised 1.4 so the dashed Q500 line no longer crosses the 2nd line
    text(o, Q_TEXT["up"], 126, 37.0, 5.2, W_EXT, "flood")
    hand_arrow(o, (8, 72), (44, 56), SITE_WATER_D, bend=0.12)
    # v20: the 28 Oct rain shares (59.1 %, 7.4 %) are not in a shared data file this script reads: words only (the
    # MGM normals give Nov-Feb most of the year's rain, Jun-Sep almost none); raised 2.6 clear of the runoff arrow
    keyed(o, "winter", "street + roof runoff " + CITE("rain") + "\nmostly Nov-Feb", 6, 80.0, 5.8)
    hand_arrow(o, (126, 31), (150, 20), SITE_WATER_D, bend=-0.15)
    keyed(o, "summer", "summer release " + CITE("rain") + "\nJun-Sep: almost no rain", 109, 47, 5.8)
    for a, b in (((64, 49), (66, 44)), ((98, 37), (100, 32)), ((130, 26), (141, 18))):
        hand_arrow(o, a, b, SPILL, width=0.4, head=1.5, bend=-0.2)
    keyed(o, "failsafe", "FAIL-SAFE · gravity\nfull basin spills to the next", 2, 31, 5.8, FAILSAFE_C, mask=SOIL)
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
    under it let the stream climb: W wet every winter, F only in big floods, D never. K4 stays as it is.
    v7 (history D8, D10, H4): D = the dry, step-free WALKING HUB SQUARE with plane trees (irrigated from storage, h03 Q4); the bed beside the summer strip =
    the floodable SUB-HUB (its floor meets the strip: the water-touching step); a route runs down the steps between
    them. The overtopped bank is the right bank (water board CUTS k4: "right bank 2.1 m: street floods"), the bank card
    h02 gives Tabaklar Hamamı (E08, ~56 m downstream of K4, calculated): named on the lower flood terrace that faces
    it, not drawn (no surveyed outline or height in this script)."""
    o, w = (ORIGIN[0], ORIGIN[1] - 110), 200
    cx, cy = 120.0, 11.9                                           # the v2.8 arc through (98,14) (120,34) (142,14)
    r = math.hypot(98 - cx, 14 - cy)
    t0, t1 = math.atan2(14 - cy, 142 - cx), math.atan2(14 - cy, 98 - cx)
    arc = [(cx + r * math.cos(t0 + (t1 - t0) * i / 30.0), cy + r * math.sin(t0 + (t1 - t0) * i / 30.0)) for i in range(31)]
    sketch(o, arc, "K4 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)  # behind
    text(o, BRIDGE("K4") + "\nbehind · kept", 104, 45, 5.4, INK2)   # v20: the bridge's proper name (names table)
    g = [(0, 8), (0, 62), (40, 62), (40, 50), (62, 50), (62, 40), (84, 40), (84, 30), (90, 30)] + bank((90, 30), (100, 14))[1:] + \
        [(150, 14), (150, 62), (w, 62), (w, 8)]
    gs = sketch_ground(o, notch(g, [(118, 132, 14, 2.5)]))     # summer strip: low-flow channel (v2.8: 118-132, 2.5)
    wall = [(150, 14), (154, 14), (154, 62), (150, 62)]
    marker(o, wall, "wall", WALL_C, angle=45.0, spacing=0.55, thick=0.5, alpha=0.55, base=0.35)
    text(o, "channel wall kept", 156, 65, 5.4)          # v20: concept record = internal, no mark
    # the stream climbing the steps: every winter (W), the design flood (F), never D
    fl = under_level(gs, 40, 150, 52)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 125, 33, W_WIN, bed_hatch=True)
    water_level(o, gs, 125, 14, W_EXT, line=False)
    keyed(o, "winter", "bed under water", 156, 31.8, 5.6, W_EXT, "water")
    keyed(o, "summer", "summer strip\ntoday: dry, pools", 156, 15.3, 5.6, W_EXT, "water")
    for x0, x1 in ((0, 40), (40, 84), (84, 100)):
        for pc in band(gs, x0, x1, 1.5):
            marker(o, pc, "tiers", DRY_PUB, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    # v7: the sub-hub floor in the bed at the strip level, up to the channel edge (the water-touching step)
    fill(o, [(101, 14), (117.6, 14), (117.6, 15.0), (101, 15.0)], "sub-hub", SUBHUB_C)
    reeds(o, 133, 148, 14, 4.5)
    road(o, 0, 16, 62, "ROAD\nbridge deck:\ntraffic", ly=56.5, mask=SOIL)   # v22 (L6, R6 p12 pairs 1-2): short lines over the deck, clear of "steps +"
    sketch_tree(o, 22, 62, 10, "Oriental plane (Doğu çınarı)"); sketch_tree(o, 35, 62, 10, "Oriental plane (Doğu çınarı)")   # D8
    sketch_person(o, 28, 62, kind=1); sketch_person(o, 30.5, 62, kind=2, flip=True); sketch_person(o, 195, 62)
    sketch_person(o, 108, 15.0, kind=0)                                         # sub-hub at low water
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)                      # the cut: the gesture
    sketch(o, wall, "wall lines", SKINK, PEN_BOLD, closed=True, z=Z_LINE)
    sketch(o, [(40, 52), (150, 52)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    tick_dim(o, 43, 52, 62, SKINK)                                                # D: raised clear of the flood
    hand_arrow(o, (138, 34.5), (138, 50.5), SITE_WATER_D, width=0.45, head=1.8)  # the stream climbs in big floods
    level_mark(o, 146, 52, W_EXT, "flood lines")
    hub_route(o, gs, 36, 104)                                                     # hub square -> steps -> sub-hub
    hand_arrow(o, (80, 63.3), (80, 41.6), HER_C, width=0.35, head=1.4)         # label -> the terrace facing the ruin
    text(o, Q_TEXT["k4"], 156, 51, 5.6, W_EXT, "water")
    # v20: "Oriental plane (Doğu çınarı)" on a line of its own (the 28 Oct line broke in the font); internal sources
    # (hub decisions, bank card) carry no mark (public sources only, booklet rule)
    label2(o, "WALKING HUB SQUARE", "street level · step-free\nOriental plane (Doğu çınarı) " + CITE("plane") +
           "\nirrigated from storage", 1, 88, 5.6, SKINK)   # v22 (L6): raised clear of number 9
    label2(o, "TABAKLAR HAMAMI ruin", "~56 m downstream · terrace faces it", 58, 69, 5.6, HER_C)
    # v20: the 28 Oct label ran over the riser at x 62 (target overlap): short lines that end before it
    hd_ = 5.6 * 0.353 * TXT_K[0] * 1.35
    text(o, "steps +\nflood terraces", 41, 47, 5.6, SKINK, "labels", bold=True, mask=SOIL)
    text(o, "wet only\nin big floods", 41, 47 - 2 * hd_, 5.6, SKINK, "labels", mask=SOIL)
    # v20: the 28 Oct label sat on the bed and its ground line ran through "in the bed" (target overlap "SUB-HUB in the
    # bed" over "strip level"): now a caption under the cut, below the sub-hub floor it names
    label2(o, "SUB-HUB in the bed", "strip level · shut in winter floods\nwater-touching step at the strip",
           100, 8.0 - 1.6 * 5.6 * 0.353 * TXT_K[0], 5.6, SKINK)
    text(o, "the stream climbs the steps,\nthe hub square stays dry", 6, 31, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((6, 125, 18), (7, 110, 27), (8, 75, 35.5), (9, 6, 67)):
        NODE(o, x_, y_, n_)

def concept_k5_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_k5_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_k5_sketch():
    """v1.4. Demeter's Garden (card i01) on the dry top of the south-west bank by K5 (zones DG 1-2, tier D). PROBLEM:
    olives and lavender cannot stand waterlogged soil. MOVE: the garden sits on the dry top, above the K5 cut's Q500,
    and the clean stream waters it. Intake, lift and basin volume: not in the card, so not drawn.
    v7 (history D8, D10): the other bank top = the dry, step-free WALKING HUB SQUARE with plane trees (irrigated from storage, h03 Q4); steps down that
    bank to the bed; the stream commons in the bed = the floodable SUB-HUB at the strip level."""
    o, w = ORIGIN, 200
    for c in (108.3, 125.0, 141.7):                                # K5 behind: three arches by its name, schematic
        arc = [(c + 8.0 * math.cos(math.pi * i / 20.0), 20.0 + 8.0 * math.sin(math.pi * i / 20.0)) for i in range(21)]
        sketch(o, arc, "K5 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)
    sketch(o, [(98, 36), (156, 36)], "K5 bridge (existing)", STONE_HATCH, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_TREE)
    text(o, BRIDGE("K5") + "\nbehind · kept", 100, 50, 5.4, INK2)   # v20: proper name (names table)
    stairs = []                                                    # v7: the bank from the bed to the hub as steps
    for k_ in range(1, 7):
        stairs += [(150 + 10.0 * (k_ - 1) / 6.0, 14 + 26.0 * k_ / 6.0), (150 + 10.0 * k_ / 6.0, 14 + 26.0 * k_ / 6.0)]
    g = [(0, 8), (0, 40), (92, 40)] + bank((92, 40), (104, 14))[1:] + [(150, 14)] + stairs + [(w, 40), (w, 8)]
    gs = sketch_ground(o, notch(g, [(56, 68, 40, 3.5), (122, 136, 14, 2.5)]))   # basin by the bridge; summer strip
    fl = under_level(gs, 92, 158, 35)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 129, 22, W_WIN, bed_hatch=True)
    water_level(o, gs, 129, 14, W_EXT, line=False)
    water_level(o, gs, 62, 39.6, W_WIN)                            # the water collection basin (volume: not given)
    for pc in band(gs, 18, 92, 1.5):
        marker(o, pc, "tiers", DRY_AGR, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    for pc in band(gs, 160, w, 1.5):                               # v7: the hub square, dry like the garden
        marker(o, pc, "tiers", DRY_PUB, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    reeds(o, 104, 118, 14, 4.0)
    road(o, 0, 16, 40, "STREET", ly=37.5, mask=SOIL)
    cafe = [(72, 40), (86, 40), (86, 45.5), (72, 45.5)]
    pe_ = elem_open("buildings", u"cafe (Demeter's Garden)")
    wash(o, cafe, "garden", CAFE_C, 0.45)
    sketch(o, cafe, "garden", INK2, LW_FINE, closed=True)
    sketch(o, [(71, 45.5), (87, 45.5), (85, 47.5), (73, 47.5)], "garden", INK2, LW_FINE, closed=True)
    elem_close(pe_)
    sketch_tree(o, 26, 40, 9, "Olive (Zeytin)"); sketch_tree(o, 38, 40, 8, "Olive (Zeytin)")      # olives
    sketch_tree(o, 49, 40, 12, "Stone pine (Fıstık çamı)")                                        # stone pine
    sketch_tree(o, 170, 40, 10, "Oriental plane (Doğu çınarı)")
    sketch_tree(o, 184, 40, 10, "Oriental plane (Doğu çınarı)")          # v7: plane trees on the hub square (D8)
    sketch_person(o, 89, 40, kind=1); sketch_person(o, 31, 40, kind=2, flip=True)
    sketch_person(o, 177, 40); sketch_person(o, 195, 40, kind=2, flip=True); sketch_person(o, 142, 14, kind=0)
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)
    sketch(o, [(95, 35), (158, 35)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 154, 35, W_EXT, "flood lines")
    hub_route(o, gs, 166, 138)                                                    # hub square -> steps -> sub-hub
    h = 5.6 * 0.353 * TXT_K[0]                                                    # one line of 5.6 pt words
    text(o, Q_TEXT["k5"], 160, 64 + 2.9 * h, 5.4, W_EXT, "water")
    label2(o, "WALKING HUB", "street level · step-free\nOriental plane (Doğu çınarı) " + CITE("plane") + "\nirrigated from storage",
           160, 64, 5.6, SKINK)
    text(o, "steps", 141, 27.5, 5.6, SKINK)
    keyed(o, "winter", "bed under water", 162, 31, 5.6, W_EXT, "water", mask=SOIL)
    keyed(o, "summer", "summer strip\ntoday: dry, pools", 162, 17, 5.6, W_EXT, "water", mask=SOIL)
    text(o, "Olive (Zeytin)", 22, 53, 5.2, INK2); text(o, "Stone pine (Fıstık çamı)", 44, 58, 5.2, INK2)
    text(o, "basin", 57, 45, 5.2, INK2); text(o, "cafe", 75, 50, 5.2, INK2)
    # v20: the body in two short lines so it ends before the basin at x 56 (the 28 Oct head ran into it); card i01 is
    # internal: no mark
    label2(o, "DEMETER'S GARDEN", "dry bank top\nall year · DG 1-2", 24, 36.5, 5.6, mask=SOIL)   # v22 (L6): clear of "STREET"
    # v23 (round 8, L6): three short lines (was "Olive (Zeytin), French lavender (Karabaş otu):" on one line, which ran
    # past x 62 into "strip water to the garden"); wording kept
    text(o, "Olive (Zeytin),\nFrench lavender (Karabaş otu):\nno waterlogged soil " + CITE("plants"), 4, 24.5, 5.2,
         FARM_C, mask=SOIL)
    hand_arrow(o, (128, 17), (66, 38.6), SITE_WATER_D, bend=0.15)
    text(o, "strip water to the garden\nintake + lift", 62, 22, 5.2, SITE_WATER_D, mask=SOIL)
    # v3: the card's crop list as two season rows (sun = summer, cloud = winter); every crop kept
    # v8 (Aras 27 Oct 17:34, Prompt 5: plants as "English (Turkish)", no Latin)
    keyed(o, "summer", "cafe beds: Bean (Fasulye) · Tomato (Domates) · Pepper (Biber) · Fig (İncir) · Grape (Üzüm)", 4, 80,
          5.6)
    # v8.1 (Prompt 8): 2.2 lines under the summer row (was 1.5: the cloud touched the sun row's box and, with no free
    # place within DECLUTTER_R inside the drawing's reach, the board's declutter left the whole winter row out)
    keyed(o, "winter", "herbs · greens · Cabbage (Lahana) · Citrus (Narenciye) · Quince (Ayva)", 4,
          80 - 2.2 * h, 5.6)
    for n_, x_, y_ in ((6, 129, 18), (7, 110, 22), (9, 8, 48)):     # v20: 9 raised clear of "STREET" (target overlap)
        NODE(o, x_, y_, n_)
    # v6: the two zones under the cut, and what each water state means for people; v7: the bed is the sub-hub
    yz = 3.0 - 0.75 * h
    for x0, x1, col, lab in ((18, 92, DRY_AGR, "DRY · DEMETER'S GARDEN · bank top"),
                             (95, 158, W_EXT, "WET · COMMONS = SUB-HUB · bed")):
        sketch(o, [(x0, 4.5), (x1, 4.5)], "zones", col, PEN_BOLD, over=0.0, retrace=False, z=Z_LINE)
        for xe in (x0, x1):
            sketch(o, [(xe, 3.2), (xe, 5.8)], "zones", col, PEN_BOLD, over=0.0, retrace=False, z=Z_LINE)
        text(o, lab, x0, yz, 5.6, SKINK, "zones", bold=True)
    keyed(o, "winter", "high water: up in the garden + hub", 18, yz - 1.5 * h, 5.6, INK2)
    keyed(o, "summer", "low water: down to the sub-hub", 95, yz - 1.5 * h, 5.6, W_EXT)

def concept_nil_sketch():
    HAND_TEXT[0] = True
    try:
        _concept_nil_sketch()
    finally:
        HAND_TEXT[0] = False

def _concept_nil_sketch():
    """v1.4. Give back (zones WP 1-2 and the floodable boardwalk, ZONES.md). PROBLEM: the downstream edge is unused
    ground and the summer bed is a trickle. MOVE: the clean stream from the upstream basins feeds floodable planting
    people can walk along; nothing is treated here; surplus goes to the farmland outside the site. v7: shorter words."""
    o, w = ORIGIN, 200
    g = [(0, 8), (0, 62), (30, 62), (46, 30), (110, 30)] + bank((110, 30), (120, 14))[1:] + \
        [(165, 14), (175, 32), (w, 32), (w, 8)]
    gs = sketch_ground(o, notch(g, [(136, 150, 14, 2.2)]))     # summer strip: low-flow channel
    fl = under_level(gs, 110, 178, 27)
    if fl:
        wash(o, fl, "flood", FLOOD_WASH, FLOOD_ALPHA)
    water_level(o, gs, 143, 21, W_WIN, bed_hatch=True)
    water_level(o, gs, 143, 14, W_EXT, line=False)
    for pc in band(gs, 46, 110, 1.6):
        marker(o, pc, "planting", REED, angle=60.0, spacing=0.7, thick=0.6, alpha=0.5, base=0.0)
    reeds(o, 121, 134, 14, 3.5)
    sketch_tree(o, 78, 30, 6); sketch_tree(o, 92, 30, 5.5); sketch_tree(o, 103, 30, 5)
    deck = [(44.5, 33.2), (72, 33.2), (72, 34.2), (44.5, 34.2)]
    fill(o, deck, "boardwalk", BOARD_C)
    for x_ in (50, 58, 66):
        sketch(o, [(x_, 33.2), (x_, 30)], "boardwalk", INK2, LW_EDGE, over=0.0, retrace=False)
    sketch_person(o, 60, 34.2, kind=1); sketch_person(o, 14, 62)
    sketch(o, gs, "ground lines", SKINK, PEN_BOLD, z=Z_LINE)
    sketch(o, [(112, 27), (178, 27)], "flood lines", W_EXT, PEN_FINE, over=0.0, retrace=False, dashed=True, z=Z_LINE)
    level_mark(o, 172, 27, W_EXT, "flood lines")
    text(o, Q_TEXT["down"] + "\nflat end: floods wide + shallow", 150, 60, 5.4, W_EXT, "water")
    keyed(o, "winter", "bed under water", 170, 28.5, 5.6, W_EXT, "water", mask=SOIL)
    keyed(o, "summer", "summer strip\ntoday: trickle " + CITE("gauges"), 170, 23.5, 5.6, W_EXT, "water", mask=SOIL)
    # v20: lowered clear of the ground line under the boardwalk; zone base = internal, no mark
    text(o, "floodable planting · WP 1-2\nclean-stream fed", 48, 25.0, 5.4, mask=SOIL)
    text(o, "floodable boardwalk", 48, 45, 5.4)
    text(o, "slope", 2, 57.0, 5.2, INK2, mask=SOIL)                 # v20: off the ground line
    keyed(o, "failsafe", "FAIL-SAFE\nhigh water\npasses over", 1, 50, 5.6, FAILSAFE_C, mask=SOIL)   # v20: ends before the slope
    hand_arrow(o, (141, 16), (100, 31.5), SITE_WATER_D, bend=0.15)
    text(o, "clean stream + strip\nfeed the planting", 112, 45, 5.6, SITE_WATER_D)
    hand_arrow(o, (184, 35), (196, 44), FARM_C, width=0.4, head=1.5, bend=-0.2)
    text(o, "surplus · farmland outside", 150, 72, 5.6, FARM_C)
    text(o, "arrives clean · no treatment here", 62, 76, 5.6)
    text(o, "clean stream back to a\nwalkable planted edge", 4, 76, 8.0, SKINK, "idea")
    for n_, x_, y_ in ((6, 143, 17.5), (7, 84, 34), (10, 158, 18), (11, 190, 38)):
        NODE(o, x_, y_, n_)

'''
