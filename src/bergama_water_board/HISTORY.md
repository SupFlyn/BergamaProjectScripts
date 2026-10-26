# bergama_water_board: notes of older versions (moved out of the script header)

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
