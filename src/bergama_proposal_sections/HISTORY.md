# bergama_proposal_sections: notes of older versions (moved out of the script header)

NEW IN v6 (Aras's deck review 26 Oct 07:06, p.25 + global rules 3-4): every section opens with a context line (what it
  shows, why it is here, how to read it: NOTES) at the top of its drawing box, inside the booklet crop; the sketch sits
  right under it at the same scale and the crop ends under the sketch (no empty foot). K5: why the amphibious stream
  commons and Demeter's Garden sit together (dry garden / wet commons under the cut, who goes where at low and high
  water, Q500 inside the banks keeps the garden dry). No personal credit in titles (booklet rule).

NEW IN v5 (Aras 25 Oct 21:47-21:51, booklet/CROP_SPEC.md): the booklet shows this sheet's own four sections:
  booklet/blocks.json lists one crop per section (the drawing box each panel frame leaves under its title and chips,
  kept in SHEET_BOXES); the separate booklet redraw (parts/90_booklet.py drawers, c4_s1..c5_s2.pdf) is gone. Sheet
  words: the Selinos is a stream (never river), no caveat notes ("schematic", "not to scale", ": not designed",
  "route not designed", "volume: not in the idea", "bridge not modelled"), no personal name inside the K5 drawing.
  Layout and look unchanged.

NEW IN v4 (A3 booklet, SCRIPT_STANDARD §8; booklet/STAGE2_BRIEF.md): after the sheet, booklet_export() writes
  output/bergama_proposal_sections/booklet/: c4_s1, c4_s2, c5_s1, c5_s2 .pdf (the four sections re-laid natively for
  the booklet's 392 x 111 mm frames, same hand-sketch engine, no text inside) + blocks.json (every word a label from the
  plan's list; no personal names, no flood heights: Q500 a named level line). The sheet is unchanged.

NEW IN v3 (Aras 25 Oct 17:00, SCRIPT_STANDARD §5b visual first; audit batch_2026-10-25_visual_first/VISUAL_AUDIT.md §1):
  sentence callouts in the sketches -> short keyword callouts with hand pictograms (winter cloud, summer sun,
  fail-safe mark); garden crops as two season rows; sheet subtitle -> keyword row with the 1-11 flow; panel
  subtitles -> keyword chips with pictograms; source notes -> [n] marks with one numbered key in the footer;
  the four "Schematic section..." notes -> one header tag. Fix (audit accuracy problem 3): the upstream Q500
  label said "lowest terrace floods"; the surveyed ARAS cut keeps Q500 inside the banks (rain_river_levels
  README v1.1 line 21: 3.30 m (+73.66), "inside; the cut is about 5 m deep"), so it now reads
  "Q500 +73.66 m · 3.30 m" and the terrace floods only if set below it. Layout, colours and frames unchanged.

NEW IN v2 (Aras 25 Oct 16:43: "the selection of A should be remember in the whole project so all scripts should drop B alternatives"): option A only, so one sheet per press. Nothing else changed.
