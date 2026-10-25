# Booklet assets: what every script writes for the A3 booklet (25 Oct 2026)

Rules: scripts/_template/SCRIPT_STANDARD.md §8. Grid and type: booklet/design-language.md. Assembler: bergama_booklet_v1.py.

## Where
`~/Downloads/Bergama/output/<script output folder>/booklet/` (inside the script's own folder; nothing else changes):
- `blocks.json` (UTF-8)
- one single-page vector PDF per drawing block, named in `blocks.json`

## Frame size
The assembler writes `~/Downloads/Bergama/output/bergama_booklet/booklet_slots.json`: for every asset key
`<folder>/<block id>` the frame `w_mm`, `h_mm`. A drawing block's PDF page is exactly `w_mm` x (`h_mm` - 5) mm
(5 mm = caption line). Drawn at that size, the drawing is placed 1:1 and its labels print at their set size;
anything else is scaled and logged. Until the assembler has run once, the sizes are in `booklet_slots.json` of the
project folder `booklet/` (same values).

## blocks.json
```json
{
  "script": "WaterBoard", "version": "v1.9",
  "sources": {"mgm17742": {"text": "MGM, Bergama station 17742, climate normals 1991-2020", "url": "https://..."}},
  "blocks": {
    "w1_year": {"type": "drawing", "pdf": "w1_year.pdf", "page": 0,
                "caption": "Rain and river flow by month {src:mgm17742}", "scale_den": null,
                "labels": [{"x": 12.0, "y": 30.5, "text": "619.6 mm/yr", "size": 7.5, "bold": false,
                            "anchor": "L", "colour": "4A3F35"}],
                "legend": [{"kind": "fill", "colour": "91ADB4", "label": "water surface"}]},
    "w1_tiles": {"type": "tiles", "tiles": [{"keyword": "rain", "figure": "619.6", "unit": "mm/yr",
                 "note": "Bergama station {src:mgm17742}", "icon_pdf": "icon_rain.pdf"}]},
    "w1_side":  {"type": "text", "heading": "...", "body": "...", "bullets": ["...", "..."]}
  }
}
```
- **drawing**: vector geometry only. NO text inside the PDF: every word is a `labels` entry (mm from the drawing's
  top-left, y down to the baseline), so the assembler writes it as live text in the booklet font, at 7 pt or more,
  with Turkish letters. Leaders, arrows, scale-bar graphics and north arrows stay in the PDF. `scale_den` (e.g. 5000)
  makes the assembler print the true scale "1:N" after the caption (recomputed if it had to scale).
- **tiles**: pictogram tiles (§5b): keyword + one big figure + unit + short note with `{src:key}`; optional icon PDF
  (12 x 12 mm, no text).
- **text**: heading (14 pt) + body (9.5 pt, keywords and short lines) + bullets. Only what cannot be drawn.
- **image**: `{"type": "image", "image": "<file name in Downloads/Bergama/booklet_images>", "caption": "..."}`.
- `legend` items of every block on a page are joined into the page's legend (footer, same place on every page),
  drawn samples + plain names, only what the page draws.
- Sources: `{src:key}` anywhere in text; the key is defined once in `sources` with a public URL. The assembler numbers
  them once for the whole booklet and prints the list on the last page. A source with no public URL is not allowed
  (SCRIPT_STANDARD §8): the claim becomes our own design statement or goes.
- Live figures: the script writes the number it computed (never hard-coded from another script).

## Content rules for every block
No fact twice in the booklet (the assembler logs any repeated sentence of 25+ characters with both page numbers).
No personal or internal attributions. Keywords over sentences. Visible strings over ~60 characters only in text blocks.

## Where the code goes (25 Oct 19:40, after the repo delivery)
write_pdf/Page stay inside each script (5-6 variants). The booklet output goes in once: `src/common/booklet_assets.py`,
one `#@include ../common/booklet_assets.py` line per script, called from that script's own write step. Edit in `src/`,
then tools/build.py, check.py, chain.sh + compare.sh (repo README); never hand-edit dist/ or scripts/.
