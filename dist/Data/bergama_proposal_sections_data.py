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
        'note': 'D4 b (29 Oct): bed +67.80 (site board v50 page value) instead of levels.json +68.57 s.',
    },
    # ---- S2: Cut S2
    {
        'id': 'S2',
        'cut': 'S2',
        'json_id': 'S2',
        'crossing': None,
        'name': 'Cut S2',
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
        'note': None,
    },
    # ---- S3: Cut S3
    {
        'id': 'S3',
        'cut': 'S3',
        'json_id': 'S3',
        'crossing': None,
        'name': 'Cut S3',
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
        'note': None,
    },
    # ---- S4: Cut S4
    {
        'id': 'S4',
        'cut': 'S4',
        'json_id': 'S4',
        'crossing': None,
        'name': 'Cut S4',
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
        'note': 'D4 b (29 Oct): bed +42.48 everywhere. Survey low point +43.58 (levels.json +43.59 s, a tacheometric point 0.3 m away) kept here only as a note, never printed.',
    },
    # ---- S5-1: Cut S5 crossing 1
    {
        'id': 'S5-1',
        'cut': 'S5',
        'json_id': 'S5',
        'crossing': 1,
        'name': 'Cut S5 crossing 1',
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
        'note': 'D4 b (29 Oct): bed +58.06 (site board v50 page value) instead of levels.json +57.93 s.',
    },
    # ---- S8: Cut S8
    {
        'id': 'S8',
        'cut': 'S8',
        'json_id': 'S8',
        'crossing': None,
        'name': 'Cut S8',
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
        'note': 'D4 b (29 Oct): bed +55.13 (site board v50 page value) instead of levels.json +55.76 s.',
    },
    # ---- W1: Upstream entry
    {
        'id': 'W1',
        'cut': 'W1',
        'json_id': 'W1_upstream_entry',
        'crossing': None,
        'name': 'Upstream entry',
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
        'note': None,
    },
    # ---- W2: K4 cut
    {
        'id': 'W2',
        'cut': 'W2',
        'json_id': 'W2_K4',
        'crossing': None,
        'name': 'K4 cut',
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
        'note': None,
    },
    # ---- W3: K5 cut
    {
        'id': 'W3',
        'cut': 'W3',
        'json_id': 'W3_K5',
        'crossing': None,
        'name': 'K5 cut',
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
        'note': None,
    },
    # ---- W4: Downstream reach
    {
        'id': 'W4',
        'cut': 'W4',
        'json_id': 'W4_downstream',
        'crossing': None,
        'name': 'Downstream reach',
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
        'note': None,
    },
    # ---- W5: Flat downstream end
    {
        'id': 'W5',
        'cut': 'W5',
        'json_id': 'W5_flat_end',
        'crossing': None,
        'name': 'Flat downstream end',
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
        'note': None,
    },
]
