# bergama_water_board: notes of older versions (moved out of the script header)

NEW IN v1.12 (Aras's booklet review, 26 Oct 07:06): the sheet is a 3 x 3 grid of panels, each the size of one A3
booklet page, so each booklet page is one panel at about 1:1 (drawings whole, at their own round scale):
  * every panel opens with a short context line (what it shows, why, what to take from it), inside its booklet crop;
  * who does what: one continuous stream ribbon with the four stations on it (was three boxes in a row, cut in three);
  * what the figures support: the seven steps clockwise round a rectangle, the red closing arrow = the next winter's
    stream refilling the storage (one way, nothing pumped back);
  * the S4 seasons: one row a season stacked at 1:250 (one crop), titles clear of their colour bars, less soil under
    the cut, the scale bar once;
  * the S4 north-east bank: the same bank at 1:200 in winter with its water and Q100 / Q500 added under the summer cut;
  * the six cuts cropped to the bed with what each level means; the planting bands in the hand-sketch language of the
    concept sections, the species as one list with each warning on its own row.
NEW IN v1.11 (Aras 26 Oct 06:35 "we dont want scales like 1:7329 ... they need to be round numbers"): every drawing
on the sheet takes the largest ROUND scale at which it fits: the six cuts 1:250 / 1:500 / 1:1,000 / 1:2,000 (was up
to 1:400), the S4 seasons 1:250 / 1:500 / 1:1,000, the planting bands 1:200 / 1:250 / 1:500 / 1:1,000, the storage
cubes 1:1,000 / 1:2,000 / 1:2,500 / 1:5,000 (was 1:1,250 or 1:1,500).
NEW IN v1.10 (Aras 25 Oct 21:47-22:02: the booklet = crops of the sheet; no caveat notes; "not stretch anything ever"):
  * Booklet: the separate booklet drawings are gone; output/bergama_water_board/booklet/blocks.json lists one crop per
    panel of this board (rects from the board's own layout) and results.json keeps v1.9's keys.
  * Caveat notes removed from the sheet (labels kept); "stream", never "river", in every visible word.
  * W2 stream height: the six cuts at one true scale, 1:250 across and up (was vertical x8).
  * S4: one row per season (south-west bank and bed, 1:250, drawn by the detail engine in that season's look) with its
    water levels and depths, the season's words on the drawing and one kind of detail per row (winter flood levels,
    spring planting bands + species, summer levels + widths, autumn materials); the north-east bank stays at 1:200.
  * W3b planting bands: drawn on the surveyed S4 ground at 1:250 in the site board's section language (src/common/
    section_style.py): days a year under water along the ground (this cut's own figures), Q100 / Q500, whole plants,
    the bands A-F as bars under the classes their days overlap.

NEW IN v1.9 (25 Oct, A3 booklet, SCRIPT_STANDARD §8): after the board, one press also writes the booklet's drawings to
  output/bergama_water_board/booklet/ (one text-free vector PDF per frame, drawn at the frame's size, its words in
  blocks.json, the figures in results.json). The board is unchanged.

NEW IN v1.7 (Aras 25 Oct 16:43: "the selection of A should be remember in the whole project so all scripts should drop B alternatives"): the board is made for option A only; one press writes
  option A's boards (no B). Nothing else changed.

NEW IN v1.6 (Aras 25 Oct 13:12: "v1.3 was fine about how it looks however it is too much text too little visual we want
more visual heavy output ... just the cube output is better so we can scrape the other part"): built from v1.3 (v1.4 and
v1.5 dropped), same layout and look, sections untouched.
  * Only the cubes boards (A and B): the to-scale storage chart and its note are gone; the note's figures (design storage,
    share of the farms' need, strip losses, seepage rates) moved onto the cubes panel, with the design storage drawn as a
    fourth cube at the same 1:1,000.
  * Text panels turned into pictogram tiles with the key figure large: WHY WE CLEAN (6 tiles), HOW FAR REED BEDS GET
    (4 tiles under the removal and coliform charts), WHERE THE CLEAN WATER GOES (5 tiles beside the aquifer bars); the
    decision row has a pictogram per step.
  * Sources: the long source lines of these panels, the chain and the river-height cuts now print as numbers [n]; the
    numbered key is in the footer, so no source is lost.
  * Chain input falls back to the upstream done text in Rhino's memory when the wire brings Null (as masterplan v16);
    the main function is main() (script standard §2).

NEW IN v1.3 (Aras 25 Oct 09:34-09:35): the same names in every script: the Button goes into an input named run, the log comes out of an output named log, and the log file is Downloads/Bergama/logs/bergama_water_board_log.txt (next to cached/ and output/), overwritten by each press.

NEW IN v1.2 (Aras 25 Oct 08:03-08:18): the chain's K5 box adds DEMETER'S GARDEN (Begum's idea alone, card i01): the
clean strip waters its olives, aromatics and seasonal beds, with a water collection basin by the bridge, and a very
small "(idea: Begum)" after the line. No demand or basin volume is drawn: her PDF gives none and only olive demand has
a source. Nothing else changed.

NEW IN v1.1 (Aras 24 Oct 09:03: "for numbers that are weak or disagree with each other correct with research and find
the factual and correct number and fix it accordingly"):
  * W2 river height: every cut is the surveyed cross-section of the main survey (Bergama Müdahele Alanları (1).dxf),
    not a trapezoid; no borrowed widths or K4 means; bed slope fitted on the surveyed bed. Q500 above the bed: upstream
    entry 3.30 m, K4 2.84 m, K5 2.79 m, downstream reach 2.33 m, flat end 1.54 m (over a 100 m wide floor).
  * S4 detail: one Q500, +46.19 on this cut (was +47.08 with a borrowed 0.21 % slope, and +49.28 from the 12.2 m
    trapezoid: both retired); every season's water is this cut's own.
  * Monthly depths (W1) and days under water on the surveyed sections.
  * Storage, farms and strip figures read from the water balance (Thread 2) results file, as the other scripts do.
  Working-area outlines are not drawn anywhere (batch rule, 22 Oct).
