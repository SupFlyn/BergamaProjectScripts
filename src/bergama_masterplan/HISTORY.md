# bergama_masterplan: notes of older versions (moved out of the script header)

NEW IN v22 (Aras 26 Oct, Rhino log "detail dt_upstream: label not placed: 4 BACK TO THE STREAM"): the water
  route's labels on the detail sheet are never left out. When no spot round the numbered marker is free,
  place_label tries round points along the route, then the free spot nearest the marker anywhere on the panel
  (2 mm grid), with a thin leader; still no overlap with another label. Other labels and the main sheet unchanged.
  Rough volumes (Aras 26 Oct 06:27): the route labels of the reed basins and retention terraces add
  "~ m³" = zone area x depth (reed basins 0.46 m, EPA 832-F-00-024, 2000; terraces: the DSİ Q100 depth over
  them, Q100 level at the nearest cut - (bed + 1 m), Aras 06:32);
  the method is a line in the detail legend.
  Output: Bergama_masterplan_v22_A.pdf, Bergama_masterplan_v22_A_detail.pdf.

NEW IN v21 (Aras 25 Oct 21:38-21:57; booklet/CROP_SPEC.md):
  * PROMENADE beside the stream, no longer over it: on each bank from 10 % of the stream's width inside the water
    edge out to the nearest surveyed street edge (a standing building met first stops it; 15 m where neither lies
    within 60 m); option A's edge wanders at the water only (promenade(), PROM_*).
  * Roads: the survey's street edges over the whole panel as one outlined network in the palette's road role, the
    main road (Bankalar - Kınık Caddesi) in its dark tone and heavier (draw_roads); street faces in the road tone.
  * A second sheet, Bergama_masterplan_v21_A_detail.pdf: the booklet's two 1:1,000 windows (upstream entry; K5 and
    Demeter's Garden) with the channel cuts and site sections, bed and Q100 / Q500 levels at the cuts, the water route
    numbered with the zones' areas, planting band letters and species codes, survey spot levels, terrace steps and
    ramps as abstract sketch marks (02b_detail.py). North arrow and scale bar in every panel.
  * Booklet: no separate drawings any more; booklet/blocks.json holds one crop per panel of both sheets (mp_upstream,
    mp_downstream, dt_upstream, dt_k5); booklet/results.json keeps v20's keys. v20's c1/c3 PDFs are removed.
  * Words: stream, never river, on the sheets; no caveat notes ("NO PROGRAMME YET" gone), no personal credit under
    Demeter's Garden, no haloed labels.

NEW IN v20 (Aras 25 Oct 18:37, A3 booklet; SCRIPT_STANDARD §8): the sheet and masterplan_results.json are unchanged.
  The press also writes the booklet's drawings into output/bergama_masterplan/booklet/: c1_s1 and c1_s2 (the whole
  site in two equal halves with 50 m overlap, centred, turned so the stream runs left to right, 1:5,000), c3_a and c3_b (north-up
  1:1,000 windows on the upstream entry and on K5 with Demeter's Garden), each a text-free vector PDF drawn at its
  booklet frame's size, plus blocks.json (every word as a label) and results.json (scales, windows, places). Option
  A only; the streamside spine in E0B67D; the area with no programme yet is plain ground. A booklet error is logged
  and never stops the sheet.

NEW IN v19 (Aras 25 Oct 16:41-16:42: "get rid of alternative 3. And do the changes to alternative one"; "that script
  gonna be producing just a single alternative"; "with the curvy selection ... it should be A"). ONE sheet per press:
  the masterplan, option A (Aras 16:43: option A project-wide, B dropped; the option input is ignored). Alternatives 2 and 3 are gone (draw_masterplan and the
  functions only it used removed); the sections WHAT IT DRAWS above describe the older alternatives.
  The one sheet = alternative 1 with v18's changes: the zones are alternative 2's freely grown pieces (overlaps
  darken) in alternative 1's tones with alternative 1's darker commons on top; the main and riverside spines are
  broad zones; the river band is named PROMENADE (Aras: "find a proper catchy singleword name"), its functions
  scattered on it as keywords (his words of 16:39). Without alternative 3 there are no link arrows and no stop
  roundels on any sheet (the programme diagram rule: no arrows). masterplan_results.json is written for option A.

NEW IN v18 (Aras 25 Oct 16:35-16:36: "combine both alt1 and alt2 on masterplan ... seeable on top of eachother";
  "alternative2s zoning is really really good"; "roads should become zones"; "river zoning is really good i want
  something like that with volume however on a different colour and sits on top of river and goes inline with
  river"). Alternative 3 only; alternatives 1 and 2 are unchanged.
  * The zones are alternative 2's freely grown pieces (growth unchanged), overlapping so the colour darkens where
    they meet, in the same light tones as alternative 1, with alternative 1's darker commons on top. The hand
    outline, verge band and code patterns of the zones are gone (zone_pattern, hand_outline removed).
  * The main spine and the riverside spine are no longer lines: each is one broad zone grown SPINE_ZONE_M either
    side of the same route (city link's data, unchanged), its edge wandering like alternative 2's pieces; the
    deck reaches are part of the zone. Names on the fills.
  * RIVERSIDE FUNCTION AND CIRCULATION (Aras 16:39: "it a function/circulation area. There'll be viewpoints,
    terraces, walkpaths, ramps etc. ... cafes etc. will be located"; his words are its keywords): one broad zone grown RIVER_BAND_M beyond the stream and bank
    lines and the water strip, along the whole corridor, in sage (palette reference 89986A), drawn over the river
    with a soft shadow and an outline for volume. Option A liquid edge, option B faceted (form rule).
  * Widths are graphic defaults, not data. Walks unchanged (to be reworked with Aras). Legend: the new zones added.

NEW IN v17 (Aras 25 Oct 14:40: "we want it as a legend in the diagram itself ... i wanted a graphical explanation"):
  every sheet gets a legend band under the drawing: drawn samples (zone swatches with their pattern and outline,
  context and survey fills, walk and spine lines, the link arrows, a stop roundel) with plain names, and only what
  that sheet draws (collected while drawing, LEG). No hex codes. This replaces the 18 Oct "no legend" rule for the
  masterplan sheets. Alternative 3's old one-line key of arrows, walks and spines (top right) is folded into it;
  the north arrow stays. Nothing else changed.

NEW IN v16 (Aras 25 Oct 11:28, studio brief for 26.10.2026: "a 1/1000 scale master plan covering the Selinos
  Corridor"): the default scale is 1:1,000 (was 1:2,000), so alternative 3 (all of site_alan, 2,845 x 529 m) prints
  about 2.87 x 0.58 m. Every sheet now carries its scale: a 0-50-100-200 m bar and "1:1,000" right of the option
  line (this replaces "no scale" of 18 Oct 19:36 for the masterplan sheets, because the brief asks for the scale).
  Nothing else changed.

NEW IN v15 (Aras 25 Oct 10:07: "Every plan and analysis and drawing we do is to be in site_alan and for indivual proposals we can
  zoom in."): alternative 3 (the whole masterplan) covers exactly the analysis range, layer site_alan (built-in copy
  SITE_COPY when the file has none), turned so its long side runs left to right; the survey is drawn over all of it.
  Alternatives 1 and 2 are the zoomed pages, one per part of calisma_alan; their margin is the input zoom_m (was
  ring_m, which still works).

NEW IN v14 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_masterplan_log.txt (next to cached/ and output/), overwritten by each press.

NEW IN v13 (2026-10-25, Aras 08:03-08:18): DEMETER'S GARDEN, Begum's idea alone (card i01). Zone base v7's zones DG 1
and DG 2 (layer INT_ZONE_DG, south-west bank either side of K5) are named DEMETER'S GARDEN on the fill, with the
keywords of her PDF (olives, stone pine, aromatics, seasonal beds, cafe, water collection basin) and, under the name,
a very small "idea: Begum" credit. Tones: the agriculture family. Reads bergama_zone_base_v7.py first. Nothing else
changed.

NEW IN v12 (2026-10-25, Aras 07:59-08:05: one file, Bergama_Altlik.3dm; "we are working the whole calisma_alan
together now"; "Make sure our proposals stays inside of calisma_alan")
  * Working areas = the curves on layer calisma_alan of the open file (an open outline with ends under 5 m apart counts
    as closed), else the copy CALISMA_COPY (Bergama_Altlik.3dm, 25 Oct). One shared area in two parts: north (UPSTREAM
    ENTRY TO K4 BRIDGE) and south (K5 BRIDGE TO DOWNSTREAM END); no split by person. Alternatives 1 and 2 show the two
    parts side by side; each part has one commons (HUB: the two old commons readings of that part merged, a design
    reading, edit freely). A zone keeps its sourced keywords (NAMES, SUBS, SIG) through its user text study_area.
  * Nothing is cut (Aras 08:10-08:11: small differences do not matter; lines that nearly match count as overlapping,
    the larger area is the true one). Walks, spine and strip are drawn continuous (207 of 4,211 m of walk lie just
    outside; WALK_CLIP = True would cut them); a zone more than SNAP_M (15 m) outside calisma_alan is listed in the log. A zone with corners
    outside calisma_alan is listed in the log (zone base v6 bakes them clipped; this flags later edits).

NEW IN v11 (Thread 5 of the 22 Oct batch, "Masterplan: detail and unity"; notes batch_2026-10-22/thread5_masterplan/)
  * Riverside walks on both banks wherever the survey leaves room, recomputed from the open file on every press
    (river_walks below: the channel edge, then the ground free of buildings behind it; buildings the zone base
    clears do not block). Three kinds: BANK WALK (car-free), STREET WALK (the footway of a surveyed street on the
    edge), BED WALK (no room on the bank, bed at least BED_MIN_W wide: a +1 m terrace in the bed, closed in floods;
    Thread 4 flood rule). Form rule: option A follows the edge, option B is straight facets.
  * The riverside spine of bergama_city_link (Thread 4), read live from
    Downloads/Bergama/output/Bergama_city_link_analysis/city_link_results.json (fallback: the embedded copy), drawn
    on the real edge, on the bank city link chose by data (spine_banks): on the bank walk where there is one, dashed where the bank has no room (a deck is needed),
    and on the street over the covered reach, where it meets the MAIN SPINE (Bankalar - Kınık Caddesi, OpenStreetMap,
    converted with the h01 formula, +-10-30 m). The eight stops as numbered roundels (alternative 3).
  * More detail on alternative 3: the survey's single trees (SEMBOL_TEK_AGAC), channel tops (SEV_SEVUST) and bank
    tops (SEV_UST) with the bank lines; walks and both spines on alternatives 1 and 2 as well.
  * Unity: masterplan_results.json (walks, spine, stops, riverside_walk_m2 per option) for the other scripts; the
    water balance (v2.1) reads riverside_walk_m2 from it instead of its 17,694 m2 placeholder.

NEW IN v10 (Aras 24 Oct 05:48-05:52; MERGE_PLAN.md sections 3, 5, 6 Q14 / Q16, 7)
  * One script, one press, three alternatives per option (above), each its own single-page PDF; the opacity is a
    setting (input opacity); a 100 % opaque white base under every lower-opacity piece in all three alternatives,
    so the site, land cover and context never mix with the zones: only the zones overlap each other.
  * Owner names replaced by stage and place names; working-area outlines and owner colours removed everywhere.
  * v2.3's four per-person sheets and its board are folded into alternatives 1 and 2 (one page each with the four
    working areas): the per-person sheets showed the same pieces and words again, only zoomed.
  * v9's raster sheet (PNG, Photoshop layers, area register, manifest, sheet band) is replaced by the vector page;
    its zones, link rules (link_check, WATER_STEPS), arrow snapping and bold v1.2 arrows are kept in vector.
  * Fixed: the zone base fallback looked for ZONE_DATA, which zone base v5 does not have (it is BASE_DATA), so the
    fallback never worked; the palette file's tones (under "masterplan" > "colours") were never read; a settings
    input could be taken for the Button; the boardwalk's word (PATH_WORDS) was never written.
  * Optional Rhino bake behind the rhino_bake toggle (off by default).
