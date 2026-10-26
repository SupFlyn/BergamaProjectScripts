# selinus_board: notes of older versions (moved out of the script header)

NEW IN v39 (2026-10-25, SCRIPT_STANDARD 8, booklet/ASSET_SPEC.md: the A3 booklet):
  * After the board's PDFs: output/selinus_board/booklet/ holds one text-free vector PDF per booklet frame of pages
    A1-A7 (drawn at the frame's size from booklet_slots.json, words as labels in blocks.json), results.json (the
    figures the booklet's A pages print: land use, readings, sky view, movement, bank shares, T1-T8) and
    booklet_log.txt. The site photos are copied to Downloads/Bergama/booklet_images/photo_1..8.jpg. The board's own
    PDFs, maps and log are unchanged; a booklet error is a warning in the log and never stops the board.

NEW IN v38 (2026-10-25, Aras 17:00 "visual first", SCRIPT_STANDARD 5b; audit batch_2026-10-25_visual_first section 6):
  * Sheets show pictures and keywords, not sentences. Readings are pictogram tiles (icon, keyword, ONE big figure,
    [n]) or callouts on the chart; method and source sentences are a numbered [n] key in the sheet's footer.
  * T1-T8 and every technical section sheet: keyword subtitles, the method paragraph as the footer's [n] key, the
    side readings as tiles (WHO 53 dB marked on the T1 stream profile).
  * Plan 01: readings as tiles (solid / void bar, floors histogram, green and fields rings); legend notes as [n].
  * Plan 07: scatter of shops against walking potential with Spearman on it; the climb of the walks as bars; the
    method sentences as [n]. Section key: drawn samples with short names, explanations in the key.
  * The drawings' Sources block is the one numbered key [1]...[n] that plans 01, 02, 04-07 and the section key cite.
  * S1 axonometric: keyword title, numbered source notes. Every figure is still computed live; nothing typed in.

NEW IN v37 (2026-10-25, Aras 09:34-09:35: the same names in every script):
  * The Button goes into an input named run; the old run input (drawings / technical / both) is now named mode.
  * The log comes out of an output named log (the setup adds it; was info) and is written to
    Downloads/Bergama/logs/selinus_board_log.txt (next to cached/ and output/; was selinus_board_last_log.txt in
    output/selinus_board).

NEW IN v36 (2026-10-25, Aras 07:50-07:52: one file for everything, the larger survey "Bergama Müdahele Alanları (1)";
the scripts respect the analysis range and, inside it, the working areas, whatever file is open):
  * No frame wired = the analysis range: the site frame recorded in SITE_FRAME_LK (site_alan of Bergama_Altlik.3dm, a rectangle, 150.52 ha), not the whole survey in
    the file. So the larger survey and the course survey give the same board (checked 25 Oct on both DXFs: inside the
    frame they hold the same survey, 69,556 and 69,791 entities, the differences are pieces cut at the frame edge;
    the larger file also has the 150 m context outside it). Wire a closed curve into frame for another range.
  * The text under the component shows v36 (v35 still showed v33).
  * Bergama_Altlik.3dm (Aras 25 Oct 08:02, the larger survey + layers site_alan and calisma_alan): with nothing wired
    into frame, the frame is the closed curve on layer site_alan of the open file (an end gap up to 5 m counts as
    closed); only when that layer is empty is SITE_FRAME_LK used. The log says which.
  * 01 WHAT IS THERE (the green fabric map) covers the WHOLE FILE (Aras 07:59: "green fabric analysis to be in the
    whole file which shows outside of the area croplands and etc."): a second site model on the whole survey (the
    survey layers this board reads, except NIRENGI, PINDEX, NOKTA_, POLIGON, SCAN, MAH_, YAZI_, layer 0 and the
    *_alan layers, on the site frame's own axes, 15 m margin), at the same print scale as before; the site_alan
    frame is drawn on it as a thin line. Every other drawing stays inside site_alan, as in v35. The built-in
    WorldCover land cover covers the whole file (x 27,318-33,562, y 28,967-34,207). The canopy-map crowns and the
    site photos exist only for the site (data pack), so outside it the map shows the survey's tree symbols only.
  * 04 Green table: one more row, farmland and orchards OUTSIDE the site frame within the whole file (satellite /
    inferred, ha; no % since the % column is of the site frame).
  * C5 marker: with no begum_alan layer it sits at the centroid of the course survey's K5 working area (C5_XY).

NEW IN v35 (2026-10-24, Aras 09:03: "for numbers that are weak or disagree with each other correct with research and
find the factual and correct number"):
  * Crash fixed: v34 used os (Downloads/Bergama paths) before the module imported it; os is now imported at the top.
  * LAND USE now accounts for the whole site frame. The survey and OSM map only part of the frame; the rest is split
    by the ESA WorldCover 2021 classes on a 2 m raster (frame_rest), plus "other unmapped ground" (yards, streets
    without a measured width, bare or built ground the satellite does not class as green). Every % in the land-use
    table, the donut and the green table is now a % of the frame (v34 divided by the mapped part only, so the
    satellite rows of the green table were over-stated). The donut's centre gives the frame's ha.
  * T2 canopy inset: the cover classes are re-binned from the cells (0, 0-10, 10-25, 25-100 %); v34's 50-100 % class
    held 3 cells of 1,502, too few for a mean.

NEW IN v34 (2026-10-24, Thread 4 "connection to the city"):
  * 07 HOW PEOPLE USE IT shows the existing commerce spines AND the proposed riverside spine. With no spine curves
    wired, the spine and the new stops are read from bergama_city_link's city_link_results.json (Downloads/Bergama/
    output/Bergama_city_link_analysis/; built-in copy of 24 Oct if that file is missing, flagged in the log), so the
    change maps (walking and driving before and after) appear on every run. Wired curves still win.
  * Walking cost now follows the slope: Tobler's hiking function (Tobler 1993, NCGIA Technical Report 93-1),
    speed = 6 exp(-3.5 |dh/dx + 0.05|) km/h, applied per street chain (junction to junction) on the survey terrain,
    uphill and downhill separately; 800 m = 800 m of flat-ground walking (5.04 km/h). Flat when there is no terrain.
  * Writes Downloads/Bergama/output/selinus_board/city_link_movement.json (walking potential on the spine and on the
    streets within 40 m of the stream, today and with the spine), which bergama_city_link prints on its page 1.
  * The spine's bank is voted from the board's buildings (Aras 24 Oct 09:08: where people live and modern buildings
    concentrate): per bank within 250 m, home floors and buildings of 3+ floors (spine_bank_vote); the vote goes to
    the log and to city_link_movement.json.

NEW IN v33 (2026-10-24, Thread 1 "merge first, then audit and fix"; Aras's batch of 22 Oct and his answers of 24 Oct):
  ONE site board: the drawings of bergama_fabric_green v10, bergama_diagrams v1.8 and bergama_movement v1 are merged
  in; those three scripts are superseded. Every overlap became one denser drawing; no two drawings repeat each other.
  * Separate drawings only (Q13): the two 16:9 pages are gone; the button always builds the drawings sheet.
  * 01 WHAT IS THERE (one plan, was 01, 05, 06, 08, 10 and fabric_green's map): the frame and 150 m of quiet survey
    context around it (Q1); homes coloured by their grain, other uses by land use; canopy-map crowns by leaf type;
    footpaths; the densest grain outlined; the stream thresholds as thin lines along the banks; bridges K1-K6,
    conflicts C1-C6 and the eight photo viewpoints, with the photos under the map (Q9). Its tables beside it:
    land-use legend, distribution, green, farmland and orchards (fabric_green's table), readings.
  * 06 THE STREAM'S TREE COVER: the plant analysis's corridor chart (crown cover bank by bank, every 25 m).
  * 07 HOW PEOPLE USE IT (one plan, was 07 commercial spines, 09 civic constellations, diagrams D3, D5, D7 and the
    movement script's panels): streets coloured by movement potential today (bergama_movement v1's engine, built in,
    on worker processes), commerce spines, civic constellations, services, the walk from each working area to the
    nearest daily function (table under it), walking and driving insets. Optional inputs spine, spine_car, bridges,
    car_closed, attractors add the change maps with a proposal.
  * S1 "what is there" also as a parallel axonometric on the survey terrain (Q8), one A3 PDF next to the board's
    PDFs, from bergama_diagrams v1.8's engine (cut down, built in), with the sky view of the stream bed (where it is
    enclosed like a well). Step 4 (Aras 07:05-07:09: an axonometric only where height could change the design): S2
    has none; instead its walk table and caption give each walk's climb on the survey terrain.
  * Sections: land cover (CLC+ Backbone 2021) and greenness (Sentinel-2 NDVI, January and July) strips under every
    section, metre by metre (Q11); the section key explains them.
  * T2 surface heat: summer and winter carry the canopy-cover inset (mean surface temperature by canopy cover).
  * NEW T8 COMFORTABLE HOURS: the share of the year's window hours with no thermal stress (UTCI 9-26 °C) on every
    open cell (Q12); sources in the sheet and in batch_2026-10-22/thread1_merge_audit/UTCI_SOURCES.md.
  * Terrain (Step 3, all topography used): the bank tops and toes (SEV_UST, SEV_ALT) and the stream lines
    (HIDRO_DERE_SULU) with heights above 1 m join the survey points, contours and spot heights. BERGAMA.3dm's
    Terrains layer is not used: it sits about 85 m below the survey heights (another datum; Thread 1 note 20).
  * Working-area outlines are never drawn on any drawing (Aras 22/24 Oct); the areas are read only, to name the
    walks by place (upstream entry, K4 bridge, K5 bridge, downstream end; Q16).
  * Data built in (SEAM_PACK, from bergama_plant_data_v1.json): crowns, photos, corridor, heat, section strips.

NEW IN v32.1 (Aras 2026-10-18 20:00): the land cover is cut to the site frame when it is loaded (as in
  bergama_fabric_green v10), so it no longer runs past the frame; its hectares come from the same cut shapes.

NEW IN v32 (2026-10-18): the land cover is BUILT INTO the script (LC_EMBED), so it always loads (v31 needed the
  separate file next to the .3dm and drew nothing without it); a file found by name or landcover_path still wins.
  The satellite classes in full colours (v31 mixed them with the paper). Only these changes; everything else is v31.

NEW IN v31 (2026-10-18, Aras 16:44: the farmland / orchard addition of bergama_fabric_green v5 here too; never bake):
  * Satellite land cover under the land-use plan (pages and separate drawing) and the open-space network diagram:
    farmland (ESA WorldCover 2021 cropland), tree cover, shrubland, grassland, and orchards INFERRED where the
    survey has olive (SEMBOL_ZEYTINLIK) or fruit-tree (SEMBOL_MEYVA_BAH) symbols within 35 m. The surveyed and OSM
    ground stays on top where it exists. Read from bergama_landcover_worldcover2021.json (project data/landcover/):
    the landcover_path input, or by name next to the .3dm / .gh, the env / osm / places files, or in Downloads,
    Desktop, Documents. Without it the drawings are as in v30 and the log says so. The land-use areas and % are
    unchanged (they stay survey + OSM); the log lists the satellite areas inside the frame.
  * The Rhino bake is a toggle (Aras 16:45): add an input rhino_bake and wire a Boolean Toggle to it. False or not
    wired = never bakes, PDFs only; True = also bakes, as before.
  * Only these changes; everything else is v30.

NEW IN v30 (2026-10-18): fix. In v29 the switch for the Rhino bake was read from the input "bake", which is the
  Button itself, so a press still baked. The switch is now its own optional input rhino_bake (default False): a
  press never bakes unless rhino_bake is True.
  * The Button works on any input name or case (bake, build, Build, button, ...): Aras's rule for every script.
  Only these changes; everything else is v29.

NEW IN v29 (2026-10-18, Aras: no Rhino bake, it slows Rhino down; the PDFs grouped into boards, one page each):
  * Nothing is baked into Rhino any more. A press builds the drawings and writes the PDFs only. An earlier bake
    already in the Rhino file is left as it is (delete the LU_ layers by hand if not wanted). Set the optional
    input rhino_bake to True to bake as before (v30; v29 said bake).
  * The PDFs are grouped into boards: each board is ONE PDF with ONE page, its drawings laid out side by side in
    rows (each drawing at 1:10,000, as in v28, with a 10 mm gap and the board's name at the top):
      Selinus_pages.pdf        the board pages (Page 01, 02, the cuts pages)
      Selinus_drawings.pdf     the separate drawings except the sections (plan, legend, panels, keys, sources)
      Selinus_sections.pdf     the separate section drawings (12 Section S1, 13 Section S2, ...)
      Selinus_T1_sound.pdf ... Selinus_T7_felt_temperature.pdf   each technical topic: its map sheet and all its
                               section sheets together (e.g. every felt temperature drawing on one page)
  * No board page is larger than 400 x 400 cm (Aras); a group that would be larger goes on _1, _2 boards.
  * Each press first deletes the PDFs in selinus_board_pdf, so v28's one-file-per-drawing PDFs do not linger.
  * Same writer as v28: all vector, text as whole editable strings, technical maps embedded as pictures.
  * Only this change; everything else is v28.

NEW IN v28 (2026-10-18, Aras: every drawing exported as its own all-vector PDF, at 1:10,000):
  * After the bake, each drawing of the run (every page, every separate drawing, every technical sheet: the same
    list as the drawings output) is written as its own PDF in the folder "selinus_board_pdf" inside the output
    folder (next to selinus_board_last_log.txt), named "NN_<drawing name>.pdf". A press overwrites the PDFs of the
    same names.
  * Scale 1:10,000: 1 m in the model = 0.1 mm on the PDF page; the page is the drawing's frame. Line weights are the
    same print weights in mm as the bake (study areas 1.1 / 0.85 mm, sections 1.5 mm); PDF_LINE_SCALE below scales
    them all if they read too heavy or too light at this size.
  * Vector: fills, lines and hatches are PDF paths (hatches as their single lines). Text is written by the script
    itself, one whole string per label (Helvetica for Josefin Sans, Courier for Courier New, with the Turkish
    letters), as in bergama_diagrams_v1_7.py, so it stays editable in Illustrator and never splits into single
    letters as Rhino's own PDF export does (RH-84424). The only raster parts are the technical analysis maps, which
    the script makes as pictures (PNG); they are embedded unchanged inside the vector PDF, with everything drawn over
    them still vector.
  * The Rhino bake is unchanged (same LU_ layers and objects), so pr1_drawings_rhino.py still finds the sections.
  * Set pdf to False (optional input) to skip the PDFs. Only this change; everything else is v27.

NEW IN v27 (2026-10-18, Aras's log rules for every script):
  * The run log starts like the masterplan script's: run time and script version, RESULT (done in N s, how many
    drawings, warnings and errors), OUTPUT FOLDER (only the main folder: the one holding the log file, the pictures
    folder and the cache; the drawings themselves are baked into Rhino on the LU_ layers), then ONE LINE PER CREATED
    DRAWING with how long it took (e.g. "Page 01 · The fabric at ground  4 s"), the site model and analyses as one
    line before them, and the bake as one line after them. The internal step timings of v26 (environment parts,
    sound workers, section sheets) are left out.
  * The log of the last run stays readable after the Button is released (info output, and
    selinus_board_last_log.txt in the output folder), as in v26.
  * Under the component: the script version and the total time of the last run ("v27 · done 312 s", or
    "v27 · ERROR"), kept while the component is idle.
  * Only this change; everything else is v26.

NEW IN v26 (2026-10-18, Aras's script rules: one Button press bakes every variant, never on top of each other):
  * Defaults: layout empty -> "both" (the pages AND the separate drawings; was "pages"); run empty -> "both" (the
    land-use pages and drawings AND the technical sheets) whenever env_path is given (was: only with the old
    environment switch); without env_path the technical sheets cannot be computed, so it builds the land-use part
    and says so in info. A value typed in layout or set on the run slider still wins (run 2 = both).
  * Unchanged and checked: Python 3 component; nothing runs until the Button is pressed, each press bakes once; the
    pages, the drawings and the technical sheets are laid out one below the other with a gap, never on top of each
    other; each press first deletes this script's earlier bake on its own layers (LU_BOARD, LU_PAGES, LU_DRAWINGS,
    LU_ENV, LU_TECH), so a press replaces the last bake instead of stacking a copy.
  * Only this change; everything else is v25.

NEW IN v25 (2026-10-18, Aras 08:03: "show working area limits in the sections as well with bold thick lines"):
  * Every section (the land-use sections S1-S6, whole or in parts, and the technical sections) shows where its line
    runs through each group working area: a bold band in the area's colour along the ground line over that stretch,
    a bold vertical limit line where the section line crosses the area's boundary, and the owner's name over the
    band. Colours as on the plans (scripts/study_area_style.md); width STUDY_STYLE["lw_section"] = 1.5 mm, on the
    same white casing (1.7 x). The crossings are found exactly on the areas' own polylines; nothing is altered.
  * The roads in every section (Aras 08:07): each street the line crosses is marked over its real extent, a bold ink
    line on the ground over the street surface built from the survey's measured widths (S.road_net, the surfaces the
    plans draw), with its name from OpenStreetMap where it has one (else "STREET") and its width along the line. A
    named OSM street crossed where the survey shows no surface is marked at its OSM centreline only and says so.
  * Only these changes; everything else is v24.

NEW IN v24 (2026-10-18, research recheck batch 2):
  * Olive crowns (evergreen broadleaf) pass 15 % of the direct sun all year, not 3 % (R03-04). The only olive
    measurement found: Castillo-Ruiz et al. 2016, "Olive Crown Porosity Measurement Based on Radiation Transmittance:
    An Assessment of Pruning Effect", Sensors 16(5):723, doi:10.3390/s16050723, Table 3: 13.3-24.6 % PAR
    transmittance (nine variety x date x pruning means, old Hojiblanca and Picual olives in Andalusia). 15 % is the
    value v16 removed, inside that range and near its low end (crowns here are not pruned for the trial). The 3 % of
    needle-leaved crowns and deciduous crowns in leaf, and 46 % for bare ones (Konarska et al. 2014), are unchanged;
    the 3 % for needle-leaved crowns has no measurement of its own (unverified).
  * Crown heights are called modelled, not measured, on every sheet (R03-05): Meta / WRI 1 m canopy height map v1,
    machine-learning estimates from Maxar satellite imagery (Tolan et al. 2024, Remote Sens. Environ. 300:113888;
    mean absolute error 2.8 m).
  * Cached shade, radiation, comfort and section results of earlier versions are not reused (MV versions +1).
  * Only these changes; everything else is v23.

NEW IN v23 (2026-10-17, Aras 19:19: no curve-point markers, colour-code the working areas, thicker lines):
  * Study areas: each working area in its own colour from scripts/study_area_style.md (palette thread, Aras 19:23):
    ARAS 5C48A2 violet, BEGUM 7F3902 rust (both of Begum's areas), NIL 107C73 teal; a near-triad on the hues of each
    owner's idea, kept off the palette's reserved hues (water blue, oxblood accent, planting olive), checked for
    colour-blind viewers. On a white casing 1.7 x the line. Thicker: 1.1 mm on the main plans (was 0.5),
    0.85 mm on the other plans (was 0.3-0.4), twice the v22 width on the small key plans. No corner markers any more;
    the owner's name is printed in the area colour. Still lines only: no fill, no hatch, geometry untouched.
    Shared record for every script: scripts/study_area_style.md.
  * Only this change; everything else is v22.

NEW IN v22 (2026-10-17, Aras chose the heavy share with buses, R01-02):
  * The five KGM-counted road sections now use the RLS-90 / VBUS heavy share p (vehicles over 3.5 t permissible
    gross weight: KGM's OYTT (about 3.5-10 t trucks and 14-25-seat buses) + buses + trucks + articulated trucks,
    over the total), not KGM's printed truck share:
      35-04 s1  (273 + 8 + 149 + 109) / 3,087    = 17.46 %  (was 8)   KGM 2023 provincial roads, project copy il23.txt
      35-05 s3  (363 + 1 + 217 + 43) / 4,069     = 15.34 %  (was 6)   same table, same copy
      240-01 s1 (1,914 + 283 + 1,053 + 1,341) / 22,053 = 20.82 %  (was 11)  KGM 2024 Region-2 state-road volume map
      240-01 s2 (1,168 + 50 + 638 + 1,271) / 14,490    = 21.58 %  (was 13)  (opened by the research recheck, R01-25)
      240-01 s3 (816 + 59 + 628 + 1,424) / 13,683      = 21.39 %  (was 15)
    Counting OYTT as heavy is an assumption (its lightest vehicles may be under 3.5 t). The class counts of 35-04 and
    35-05 rest on the project's copy of the KGM 2023 book (KGM's own page did not open); the 240-01 boxes were read on
    KGM's map, but their assignment to the sections rests on the project's copy of the 2024 table.
  * The streets without a count (CORRELATED and GPG DEFAULT, the group's estimate) keep exactly their v21 traffic:
    correlated streets still take KGM's printed truck share of their source count (p_kgm), and default streets the
    GPG shares. Only the counted sections change.
  * Only this change; everything else is v21.

NEW IN v21 (over v20; same inputs, outputs, layers and site file; corrections from the outside-source recheck of
  2026-10-17, research/library_recheck/corrections_for_library_index.md; the register ids are given)
  * River label in Turkish capitals (R06-07, R08-14): "SELİNOS ÇAYI", not "SELINOS ÇAYI" (tr_upper; Python's upper()
    turns i into an undotted I). The survey stream name on the map uses it too.
  * Sound period labels (R01-07): DAY 06-18 · Ld, EVENING 18-22 · Le, NIGHT 22-06 · Ln, the periods of the VBUS
    Table 2 hourly shares the traffic is split by (34. BImSchV hours). No number changes: the levels never used the
    clock times.
  * Sound method wording (R01-14, R01-26): building screening is an RLS-90-type D_z with the ISO 9613-2 limits (20 /
    25 dB) and sign, not the VBUS screening; VBUS's weather (D_met) and reflection terms are not used. No number
    changes.
  * KGM heavy share wording (R01-02): KGM's "ağır taşıt" share counts trucks and articulated trucks only, no buses.
  * "brussels" palette wording (R01-17): the colour order of the Brussels noise map, extended to 11 DIN-style 5 dB
    classes from 35 to 80 dB(A); not the Brussels classes or colours. The default stays the graded run.
  * Shade sheets (R04-06): the printed sunrise, sunset and daylight are when the sun's centre is above the horizon
    (no -0.8333 deg almanac rule); the labels now say so. Hours unchanged.
  * Air temperature (R05-03): 60 m is PVGIS's point elevation, not the ground of the dry bulb (ERA5-Land 2 m air
    temperature of its grid cell, ground height not reported). It stays the lapse-rate reference, now labelled as an
    assumption; the true reference needs the ERA5-Land orography at the site.
  * Surface heat (R02-06): "late morning", not "near noon". The printed mean time comes from the environment file,
    whose utc_mean drops the seconds (one minute early: 08:49 UTC is right for spring to autumn); not changed here.
  * Sun refraction below -0.575 deg: -20.774 (NOAA), was -20.772 (R04-02; at most 0.2 arcsec, below the horizon).
    Perez extraterrestrial irradiance: Spencer's day angle from day 0 (R04-16; at most 0.059 %).
  * OSM relation 4200394 (ref:whc 1457) is two fenced areas (91 ha), not the inscribed World Heritage boundary
    (332.5 ha, 9 components): relations with ref:whc are never read as areas or labelled (R06-30; v20 did not draw
    it either).

NEW IN v20 (over v19; same inputs, outputs, analyses and drawing rules; the site file changes again)
  Site source from 2026-10-17: the course's "Bergama Müdahele Alanları.3dm" (open it in Rhino without moving or
  scaling it). It holds every survey layer v19 reads, at the same coordinates (134 survey labels within 7 mm), with
  a few more surveyed objects inside the old frame (BINA_MESKEN 18,894 -> 19,010 lines, YOL_SOSE 2,139 -> 2,179 ...),
  the same three study areas (aras_alan, begum_alan, nil_alan: identical areas) and a neighbourhood outline
  (MAH_GOSMANPAŞA, not read). It has NO "site alan" frame and NO "sec_lines" section lines: its "site_alan" layer is
  empty. selinos.gh picks the frame and the six section lines by their ids in Nilnoktali-BERGAMA_layerekli.3dm, so
  in the new file those picks find nothing.
  * When a wired frame or section input finds nothing in the open file, and the file has no curve on "site alan" /
    "site_alan" or "sec_lines", the frame and section lines recorded from Nilnoktali-BERGAMA_layerekli.3dm
    (md5 c7dcc5d18f8ea2092805edb84d0ecce7; SITE_FRAME_LK, SECTION_LINES_LK, in survey coordinates, in selinos.gh's
    order) are used, and the info output says so. The technical section inputs (sound_sections ... felt_sections)
    get the same fallback; v19 gave them none. Pick new curves to override; an unwired frame still means the whole
    survey.
  * Layer names are matched with spaces and underscores alike ("site alan" = "site_alan").
  * BERGAMA.3dm (the course's 3D model: terrain lines and building meshes) is NOT a site file for this script: it
    has no survey layers and sits at local coordinates (survey = model + (30025.4131, 32284.7501), fitted on the
    study-area corners, 0.0 m error).
  * site_model(): the first half of pipeline_run (alignment, survey, frame, section lines, build_site, study areas,
    fabric types) as one function, so the masterplan and render scripts can build the same site; same results.

NEW IN v19 (over v18; same inputs, outputs, analyses, numbers and cached results; the site file changes)
  Site source from 2026-10-16: Nilnoktali-BERGAMA_layerekli.3dm (the same survey, at the same coordinates, plus the
  group's three study areas). Open it in Rhino without moving or scaling it, as before.
  * The group's study areas, the closed curves on the layers aras_alan, begum_alan and nil_alan (STUDY_LAYERS), are
    drawn as bold outlines with square markers at their corners and the owner's name (ARAS, BEGUM, NIL) on every plan:
    the land-use map, the diagram panels, the thresholds map, the section locators, every technical map and the key
    plans. Outlines only, never a fill or hatch, so no analysis colour under them changes; they are drawn over the
    rendered map pictures as lines, so the pictures and the cache are the same as v18's.
  * The areas are only read, never moved, edited or deleted, and they are not part of any analysis or its
    fingerprint. They are kept on the site as S.study_areas (name, layer, outline in survey coordinates, area in m2)
    for later analyses, and the info output lists them.
  * A file without these layers builds exactly as v18.

NEW IN v18 (over v17; same inputs, outputs, layers and numbers, drop-in replacement; only faster on a cold run)
  v17 still ran several long stages on one core whatever the core count (Rhino's Python runs one Python thread at a
  time): the terrain heights of the road pieces and receivers, the shade and solar grids' terrain, the drawings behind
  the technical sections, and one map picture after another. Tested outside Rhino on 4 cores, cold, all technical
  sheets of section line 1: v17 643-658 s, v18 555-597 s; all 40 cached result files and all 60 map images are byte for
  byte identical and the board is identical apart from its output folder name. The gain grows with the core count,
  because those stages now split over every core.
  * Worker processes for those stages: Rhino 8's own Python running THIS component's own code (everything above the
    main block). Before any work, each must show the same bytecode for every function, the same maths fingerprint and
    the same numpy as Rhino; Rhino then computes the first piece of every job itself and compares it bit for bit with
    the worker's. On any difference, error or missing worker the job is done in Rhino as in v17 and the workers are
    not used again that run. The log names the stages that ran on them ("Worker processes: N for ...") or why none
    did. They need the component's code to be readable from Python; if Rhino does not allow that, v18 runs as v17.
  * Terrain heights of many points at once (z_np, the 1 m shade grid and the radiation grid) and the road gradients
    and sound receivers (z_at) run on the workers in pieces; each point's height depends on that point alone.
  * The drawings behind every technical-section row start on the workers before the sheets are drawn (the same calls
    with the same arguments), while Rhino draws the plan sheets.
  * Map pictures (the 17-megapixel shade and solar maps and the others) are made several at a time on threads, as
    many as the cores and half the memory allow (about 1.5 GB each); their index is written afterwards in order.
  * Fixed: on a 2-core computer v17's job threads could wait for each other for ever; nested jobs now use their own
    threads.
  * Switches: PAR_POOL (False = these stages in Rhino, as v17), POOL_MIN_PTS, POOL_START_S, RENDER_GB, and the v17
    switches below. PAR_PROCS = 1 turns off all worker processes.

NEW IN v17 (over v16.7; same inputs, outputs, layers and numbers, drop-in replacement; only faster)
  Every result is computed by the same code in the same order as v16.7. Tested outside Rhino on 4 cores, cold
  (nothing cached), all technical sheets of section line 1: v16.7 1256 s, v17 800 s. All 40 cached result files
  and all 60 map images are byte for byte identical, and the board is identical apart from its output folder name.
  * Every logical core the computer reports is used (12 on a 12-thread laptop, 16 on a 16-thread desktop); v16.6
    and v16.7 stopped at 8. The log says "Cores used: N of N". PAR_MAX = 0 means no cap; a number caps it.
  * The sound model (the slowest pure-Python part) runs on worker processes, one per core, started with Rhino 8's
    own Python. Rhino's Python runs one Python thread at a time, so threads cannot speed this part up but
    processes can. Each worker runs the same code text as Rhino (NOISE_KERNEL, defined once below and run by both)
    and computes whole receivers, so each value is the same number. Before the results are used, the first receiver
    of every worker is computed again in Rhino and must match exactly; a worker's maths fingerprint must match too.
    On any mismatch, error or missing Python the whole job runs in Rhino as in v16.7, with a LOG line saying why.
    The log says "Sound map: N receivers on n worker processes ... (checked against Rhino)".
  * Independent analyses overlap: the sound map and all sound sections start first on the worker processes, while
    Rhino computes shade, comfort and solar radiation on its threads; their results are collected after.
  * Inside one sun position the separate shade groups, solar sky patches and comfort hours run on threads too, each
    summed in the original order (PAR_JOBS). numpy releases Rhino's lock, so these threads do run side by side.
  * The big shade grids (over 1 million points) are limited by memory, not by a fixed 4: about 0.75 GB per thread,
    within half of the computer's RAM (read from Windows).
  * A picked object whose id no longer exists (a re-opened file) no longer stops the build: frame falls back to the
    single closed curve on the "site alan" layer, section_lines to the curves on "sec_lines", with a WARNING.
  * Not used: the graphics card. Rhino 8's Python has no GPU array library (CuPy needs CUDA and a matching install),
    and GPU arithmetic does not give the same last digits as the CPU, so results would no longer be identical.
  * Switches: PAR_PROCS (0 = one worker process per core, 1 = none, as v16.7), PY_WORKER (path of a Python to use,
    "" = Rhino 8's own), PAR_JOBS (False = v16.7 order on one thread), PAR_THREADS (0 = all cores, 1 = one thread),
    PAR_MAX (0 = no cap).

NEW IN v16.7 (over v16.6; same inputs, outputs and layers, drop-in replacement)
  * The river runs on past the Ilica junction bridge to the frame edge. OSM changes the stream's name there
    ("Selinos Cayi" ends, "Bergama Deresi" goes on); v16.6 followed only the first name and stopped. Pieces named
    Selinos/Bergama that touch either end (within 10 m) are now joined into one centre line.
  * The wide dry bed before that bridge is no longer empty: where neither side has an edge within 25-30 m for more
    than 45 m of river, the bed is followed out to RIVER_FAR (80 m) to the nearest slope toe, wall, building front
    or street edge running with the stream (within 40 degrees; streets on a surveyed bridge left out). A side with
    a near edge keeps it, so the rest of the river is unchanged.
  * The strip of paired stream lines north of that junction (survey text "Kestel Deresi"; Nil: not a river bed) is
    no longer filled as river. A stream-line pair is river only within RIVER_PAIR_D (30 m) of the river's centre line.
    Its two lines stay as thin surveyed stream lines.
  * Cut buildings carry their own name instead of their type word where a source names them (survey name text,
    a named OSM outline, a named OSM/places place of worship or civic point inside): "Bergama Ulu Cami", not
    "mosque". Monuments, sacred buildings, civic halls and civic/religious uses only; type words (Cami, Trafo, Depo)
    and garbled spellings are not names; unnamed buildings keep their type word. Named parks and places the line
    crosses (OSM areas) are called out by name in the land-use sections.
  * Street surfaces are one solid colour (ROAD_FILL) in every plan and section, no hatch lines; over the sound maps
    a solid cool grey (ROAD_FILL_OVER). ROAD_SOLID = False restores the v16.6 hatches.
  * The log stays after a Button press: the button's state and the last build's report (with its time) are kept on
    disk as well as in Rhino's sticky memory, which the Python 3 component does not always keep. Each build also
    writes its full report to selinus_board_last_log.txt (in Downloads/Bergama/output/selinus_board, 24 Oct).
  * Every input accepts whatever Grasshopper hands over, with the default "ghdoc Object" type hint: object ids
    (from Rhino or from Grasshopper's own document) are looked up, wrappers unwrapped, data trees flattened. Inputs
    are read from the component's own input list only, so a name the script defines (bake) can never stand in for
    an input that is not connected.

NEW IN v16.6 (over v16.5; same inputs, outputs and layers, drop-in replacement)
  * Solar and shade sections no longer spike at cut buildings. Cause: v16.5 sampled the ground every 1.0 m plus one
    extra point 0.25 m outside every cut wall (the darkest ground of an alley) and joined them by straight lines, so
    every wall drew a sharp V; the more buildings a section cuts, the more V's. Now the ground and roofs are sampled
    evenly every 0.25 m (TSEC_DS_SOLAR), the facades in 0.5 m bands: the values are the same model, nothing smoothed.
    What remains (roofs at ~5, 2-4 m streets at 1-2 kWh/m2 per day; roofs ~0 h, narrow gaps 12 h of shade) is real:
    the graphs keep every value and add a dark blue line, the mean over 10 m of line (TSEC_TREND), on top.
  * Shade sections on their own 0.25 m x 0.25 m field (v16.5: 1 m x 0.5 m); the colours at a wall's foot come from
    the open side alone (v16.5 blended them across the wall with the roof's value: the dark wedges at wall feet).
  * Shade plan (T3) on a 1 m grid (v16.5: 3 m), drawn at 0.3 m pixels; wind, air and felt temperature plans on a 2 m
    grid (v16.5: 3 m); the wind, air and felt section fields every 0.5 m along the line (v16.5: 1 m). Section
    pictures at 450 dpi (v16.5: 300), up to 9000 pixels long.
  * Trees under the analysis: in the sections the tree silhouettes are drawn under the colours (v16.4-v16.5 over
    them); on the technical maps the crowns are thin outlines and the analysis shows whole inside them
    (TECH_TREES_UNDER; v16.5 washed them green).
  * Streets on the sound maps (T1): hatched, with their edges, over the colours; every technical section shows the
    streets it cuts as a hatched band under the ground line, as the land-use sections do.
  * Values with decimals (temperatures, wind, kWh, dB) printed with 2 decimals (VAL_DEC) in notes, legends, contour
    labels and graph axes. Shade keeps h:mm and whole-hour classes.
  * Speed: the sun and sky passes find the obstructions of several sun directions at once on parallel threads
    (par_ordered, PAR_THREADS); identical results, about 3.3 times faster on 4 cores.

NEW IN v16.5 (over v16.4; same outputs and layers; two new optional inputs: water_depth, water_levels)
  * Streets hatched (fine 45-degree lines) in every plan that shows them: the land-use plan, urban fabric, intensity,
    commercial spines (now the streets at their surveyed width, v16.4: centre lines), open space, civic
    constellations and the stream thresholds; and the street surface band in the land-use sections. Baked as Rhino
    hatches (pattern "SELINUS lines", made in the file once); as plain lines where Rhino refuses the pattern.
  * The water in the stream drawn at its depth: hatched blue from the surveyed bed up to the water surface, the
    channel above it in a pale wash, the water line on top. The survey has no water level and no published depth or
    flow figure was found, so the depth is an APPROXIMATE 0.15 m (the Selinus barely flows: the Kestel dam, 1988,
    holds its water and much of it is led into the neighbouring catchment), labelled on every section. New inputs
    replace it: water_depth (m above the bed) or water_levels (points on the water surface, interpolated along the
    stream, so the depth varies).
  * One colour window per analysis (wind, air, felt): the plan's four seasons and every section of every line share
    it, so section 1 and section 2 compare colour for colour (v16.4 stretched every picture to its own values). The
    window is the 0.5-99.5th percentile of all their values, spread over the palette as before. The zoomed legend
    bar carries its minimum and maximum, and marks each picture's own lowest and highest values. The solar section
    graphs share one range too.
  * Solar radiation (T4) over the whole frame, a row per season (v16.4: the densest 420 x 210 m stretch); the focus
    input still limits it to an area.

NEW IN v16.4 (over v16.3; same inputs, outputs and layers, drop-in replacement)
  * Sound map colours: one graded run, pale green (quiet) to deep maroon (loud), every 5 dB band darker than the one
    before. The Brussels colours of v16.3 turned from dark red to blue and violet for the two loudest bands (70-80 dB),
    so the loudest streets read as the quietest strips. The values are unchanged; noise_palette "brussels" brings
    those colours back.
  * Sound model: a building block now screens by the way over its roof AND the two ways round its sides (lateral
    diffraction, ISO 9613-2 7.4, combined by energy); touching buildings form one block. v16.3 treated every house as
    an endless wall, so detached houses cast sharp, too deep sound shadows.
  * Section graphs run on without gaps: ground and roof stretches meet at the walls (v16.3 left a white gap at every
    wall); the solar graph follows the top surface (ground, and the roof where the line crosses a building) instead of
    a broken ground line and a separate red roof line.
  * Colours stretched more the closer a picture's extremes are: every picture that does not fill its scale gets at
    least 75 % of the palette (v16.3: only below 40 % of the scale). Wind takes Windy's colours from calm to 15 m/s
    (blue, teal, green, olive, brown) spread over its own range (v16.3: the 0-5 m/s blues only).
  * Building types drawn in their own tones and features: old town houses (stone ground floor, timber upper floor
    jutting out on brackets, deep-eaved hipped tile roof) now read apart from planned low-rise houses (concrete floor
    bands, wide windows, balcony, low tile roof); mosques with a drum, lead dome, arched windows and a minaret (at the
    survey's minaret symbol, or where the name says cami); monuments in stone and brick bands with arched openings, a
    ruin with a broken top. The far wall's windows show through the cut. Generic, not surveyed, as before.
  * Stream channel hatched in blue from the surveyed bed up to the lower bank top in every section (v16.3: a line at
    the bed). The water level is still not surveyed and not drawn.
  * Trees are never cut: in the technical sections the trees on the line stand whole over the analysis colours
    (v16.3: a dashed box round the cut crown, washed with the field).

NEW IN v16.3 (over v16.2; same inputs, outputs and layers, drop-in replacement)
  * Building types in every section (land-use and technical): each cut building and each building beyond the cut is
    drawn with the silhouette of its fabric type, so old town houses (hipped tile roof, deep eaves, tall windows, stone
    base), planned low-rise houses (pitched roof), apartment blocks (flat roof, parapet, balconies), small irregular
    houses and shacks (low, lean-to corrugated roof), civic halls, industrial halls (sawtooth roof), mosques (dome) and
    monuments (coursed masonry) read apart; shops and mixed use show a shopfront and awning. Cut buildings wide enough
    carry a tag ("old town · 2 fl"). The footprint, use, type and floor count are measured as before and the eaves stay
    at floors x storey height; roofs, windows and shopfronts are GENERIC drawings of the type, not surveyed.
  * Technical section graphs no longer break where the line crosses a building: there they show the value the same
    height above its roof, as the plan shows a building (dashed, over a paler ribbon and a grey roof mark).
  * Terrain horizon in the sections: v16.2 used the PVGIS horizon seen from the ground at every height, so the sky of
    a shade section showed full-height bands. Now the horizon falls with height: the terrain (survey inside the frame,
    PVGIS 100 m DEM out to the grid's edge) is marched every 7.5 degrees of azimuth and the horizon lowered by how
    much it drops between the ground and each height; terrain beyond the grid is taken as far (no drop). Shade, sky,
    solar and comfort sections use it; the plans (ground level) are unchanged.
  * Shade sections: the plan's one-hour class colours blended between whole hours (values unchanged), so minutes
    either side of a whole hour no longer jump a class and draw stripes.
  * Close extremes stretched: where a picture's values cover less than 40 % of the shared scale (air temperature
    above all), its colours are stretched over 75 % of the palette, around where the values sit; the legend shows the
    shared scale with the stretched part bracketed and true-unit ticks (T5-T7 plans; wind, air, felt sections).
  * Road traffic noise: every street now carries traffic (v16.2: only the KGM-counted 35-04). KGM counts where KGM
    counted (35-04 s1, 35-05 s3, D240 s1-s3, the ring road cut at its KGM section boundary); every other street the
    EU WG-AEN GPG v2 default flow of its type, scaled by the nearest KGM count of the same street type (k = counted
    AADT / GPG default). DERIVED, labelled on the sheet with every street type's k, source and km.
  * Stream thresholds: edges drawn 1.5 mm (were 0.7), wall and bank marks 0.6 mm (were 0.28).
  * Urban fabric: types under 0.5 % of the footprint (under construction: 0 %) leave the legend; the caption names
    them with their area.
  * Kept results: section geometry and section fields are recomputed once (cache versions raised).

NEW IN v16.2
  * Sections drawn like architectural sections: behind the cut the buildings beyond (to 120 m, tinted by use, paler
    with distance, a line at every storey), the ground falling away beyond, the trees at their measured height and
    crown by leaf type (deciduous ones bare in the rows of their leafless days) and scale figures; the cut on top as
    crisp vectors. Board sections have their own pages (three a page, one shared scale; a long flat section is
    split in two); technical sections lay the analysis over that drawing as colour, with contours and a graph of
    the pedestrian level.
  * Technical maps and section pictures show in every display mode: the sheet background no longer covers them, and
    every picture displays rendered even in a Wireframe viewport (as Rhino's Picture command does).
  * Streets as surfaces: a street whose width the survey shows is drawn as its two edges with a quiet stone-grey fill
    between them. Each side is measured on its own to the surveyed road edge every 2 m, junctions merge into one
    outline laid on the measured edges, and a street stops at the open water except on a bridge or where it crosses
    the stream. Streets with no surveyed width stay thin centre lines. The sections read the street ground from the
    same surfaces.
  * The river never runs over a building, past a surveyed stream line (a strip on its dry side is cut away) or past a
    kerb running along it; a stretch OSM maps in a tunnel or culvert, where the survey shows no open channel, is drawn
    covered (dashed); the water closes up against its surveyed banks and walls (no wedges of dry ground left in it).
