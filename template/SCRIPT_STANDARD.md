# Bergama script standard (25 Oct 2026; folders updated 27 Oct)

Every new or edited Grasshopper script follows this. Start a new script from `bergama_script_template.py`, which is in this folder. Each rule names the message from Aras it comes from.

## 1. Folders (all under ~/Downloads/Bergama/)
| folder | holds | rule |
|---|---|---|
| `Data/` | input data files: osm, places, environment, land cover, palette | read from here by default, with no path inputs. An input may still override (25 Oct 09:49) |
| `output/<script folder>/` | FINAL PDFs ONLY (sub-folders allowed, e.g. the board's selinus_board_pdf) | one folder per script (24 Oct 08:28); nothing else, no logs, no JSON, no images (27 Oct 11:07) |
| `cached/<script folder>/` | caches, results JSON other scripts read, rendered images, any other working file | 24 Oct 08:28; results moved here from output/ 27 Oct 11:07 |
| `cached/booklet/<script folder>/` | the script's booklet assets (blocks.json, booklet results, images); the booklet's own leftovers in `cached/booklet/` | 27 Oct 11:07 |
| `logs/` | ONE log per script, `<script base name>_log.txt`, with no version in the name, overwritten by each press; extra log files or log folders in `logs/<script folder>/` | 25 Oct 09:34-09:35, 09:55; 27 Oct 11:07 |

**Paths come from one place (27 Oct):** `src/common/bergama_paths.py` (`bg_output`, `bg_cache`, `bg_booklet`, `bg_logs`, `bg_first`, `bg_tidy_output`), included near the top of every script (the template carries a copy). Never build a Bergama path by hand. Readers look in the new place first and fall back to where older versions wrote (`bg_first`). Every `main()` ends with `bg_tidy_output(OUT_FOLDER)`: anything not a PDF left in output/ is moved (never deleted) to logs/ (log files) or cached/ (the rest), so a later mistake cannot leave clutter in output/.
Folders are created by the script. Nothing is written anywhere else: no temp state files and no copies of the log (25 Oct 09:55). Worker scratch folders for parallel compute are the only exception. Cleanup is ours, because Aras cannot delete folders (24 Oct 08:52).

## 2. Component
- Grasshopper **Python 3 Script**. Paste the whole file.
- The Button goes into an input named **`run`**; any other True bool also works. The log comes out of an output named **`log`** (25 Oct 09:34).
- One press does everything (A and B together). A second press works. Nothing runs before a press.
- Output **`done`**: the text `done HH:MM:SS.ss · N s` after a good run (`ERROR ...` after a failed one, `idle` before), kept until the next run in this Rhino session (25 Oct 10:20). Wired into the next script's `run`, each NEW done text fires that script once (`chain_fire`), so one Button press runs the chain and an error stops it there (10:15). Aras uses a Button, never a Toggle. Never count `done` as a Button.
- No script runs twice in a chain (10:19): a script that needs a later script's result reads that result's last saved file and says in its log if it changed.
- Any Rhino bake uses a separate Boolean Toggle `rhino_bake`, off by default (18 Oct 16:45).
- Never define a function named `run`. In a globals-based script it hides the input (the main function is `main()`).
- Frame input only where a script draws the site; don't force it (25 Oct 07:52).

## 3. Text under the component and log
- Under the component: `Name version · HH:MM · N s` after a run, `Name version · idle` before one, `· ERROR` on an error (25 Oct 09:44). Names are CamelCase with no order numbers (09:45). Current names: ZoneBase, MasterPlan, WaterBalance, MainBoard, CityLink, AgriCulture, WaterBoard.
- The log shows the main destination, one line per file with its time, and the version plus total time. Nothing more.
- Errors go into the `log` panel and the log file; an old log never stays on screen after a failed run (25 Oct 09:52).
- The panel keeps the last log for this Rhino session only (scriptcontext.sticky). If sticky loses it, the script reads its logs/ file back. Nothing is kept across Rhino restarts (25 Oct 09:55).
- A missing or bad file must fall back to built-in data. It must never leave the drawing empty.

## 4. Site file and limits
- ONE Rhino file: `Bergama_Altlik.3dm` (card `library/_index/cards/s01_*`). Results must not depend on which file is open (25 Oct 07:50).
- Layer `site_alan` is the analysis range (a rectangle). Layer `calisma_alan` is the working area, ONE shared area with no per-person split (08:05). Keep a built-in copy of both outlines as a fallback.
- Proposals stay on `calisma_alan`. Anything within SNAP_M = 15 m counts as on it, and nothing is cut (08:10-08:11). Only the site board's plan 01 (green fabric) covers the whole file.
- Every plan, analysis and drawing covers exactly `site_alan`; only individual proposals get zoomed pages (25 Oct 10:07). Exceptions Aras set: plan 01 green fabric over the whole file; the agriculture farm plan shows the farms outside the site.
- Working-area outlines are not drawn (24 Oct batch).

## 5. Output
- PDFs are all-vector, with whole-string text (no letter splitting). Related drawings go on one single-page board.
- No two scripts make the same drawing. An overlap means one merged drawing (24 Oct 05:32).
- Prefer data built into the script over side files. Reuse verified data. Never hard-code a figure another script computes live: read its results JSON.

## 5b. VISUAL FIRST (Aras 25 Oct 17:00, every output)
- Diagrams, pictograms, charts and images instead of sentences. Keywords only where something cannot be drawn. No long sentences on any sheet.
- Pictogram tile = icon + keyword heading + one big figure + `[n]` (the water board v1.6 method, accepted 25 Oct 13:25).
- A figure sits on the chart or drawing where it happens (callout with a leader), not in a note below.
- Method and source sentences become `[n]` marks with ONE numbered source key in the footer. Nothing is lost: every figure and every source stays.
- Legends are drawn samples with plain names, only what the sheet draws (masterplan v17). Never hex codes.
- Keep the layout and look of an accepted sheet: replace text, do not restyle the frame (water board v1.4/v1.5 were rejected for that, 25 Oct 13:12).
- Check before delivery: no visible string on a sheet longer than about 60 characters, except titles of names and the source key.
- No caveat notes on drawings (Aras 25 Oct 21:50-21:51): keep the label, drop the caveat: "clean strip water · intake and lift" stays, ": not designed" goes. Same for "(not verified)", "route not designed", "schematic, not to scale" and the like, on every sheet and booklet page. Open points go to the log, never on the sheet.
- No white-boxed (haloed) labels on maps (Aras 25 Oct 21:41): labels sit on the drawing in plain text, placed where they do not collide.
- No contour / topography lines on any axonometric (Aras 25 Oct 21:42).
- NEVER STRETCH (Aras 25 Oct 22:02, "not stretch anything ever like EVER"): one uniform scale for x and y in every drawing, section and booklet crop; no vertical exaggeration, no one-axis fitting.

## 6. Changing a script
- **Edit in the repo, not in the big file** (Aras 25 Oct 17:27: "as the scripts became too big you kinda warp them each time you edit them"). Source: github.com/SupFlyn/BergamaProjectScripts (saved to the project; backup bundle `scripts_repo/`). Each script is `src/<name>/` (code, `data/` = built-in data, `parts/`, `MAP.md` = function -> file and line) plus `src/common/` (helpers with the same text in 2+ scripts). Steps (repo README): `tools/setup.sh` once per container, then edit the part, `tools/build.py` (-> `dist/`, one self-contained .py as before), `tools/check.py old new` (lost / added / changed / twice-defined functions, new undefined names), `tools/chain.sh` old and new + `tools/compare.sh` (all 8 scripts offline on the real survey, fake Rhino, frozen clock: same files = same product), then commit and copy `dist/` to `scripts/`. A script changed outside the repo goes back in with `tools/split.py` (round trip must give the same bytes). Never test with Rhino MCP / Remote Control (Aras 17:32, too token heavy). A new script from the template is added with `tools/split.py`.
- Built-in data (Aras 25 Oct 21:29, shorter scripts): `tools/build.py` writes each script's data blocks to `dist/Data/<script>_data.py`; the script reads them from `Downloads/Bergama/Data/` (md5-checked, a clear error if missing or from another build). Deliver the script and its Data file together (`scripts/` + `scripts/Data/` + kit zip `Data/`). Heavy results that depend only on the inputs are worked out once and kept (Store cache keyed on inputs + code), never recomputed in the same run (21:29: "check once and cache it").
- A new version gets a new file name `_vN`. Move the old one to `scripts/_superseded/` and delete superseded functions (lesson of 18 Oct 17:33). Small fixes made the same day, before Aras has run the script, may be done in place with the version kept; say so in the reply.
- In the same turn, update: `run_kit_2026-10-25/RUN_GUIDE.md`, then the kit zip, then the `library/START.md` row, then the `library/_index/MASTER_INDEX.md` row, then memory.
- Check that it compiles. Aras runs it in Rhino; never list a run as waiting on him.
- The reply ends with: "If it fails, set Effort to High before you paste the error."

## 7. Change record of 25 Oct 2026 (all seven current scripts)
| time | change | scripts |
|---|---|---|
| 08:02-08:25 | one file `Bergama_Altlik.3dm`; site_alan made a rectangle, calisma_alan snapped onto it | board v36 > v37, zone base v6 > v8, masterplan v12 > v14 |
| 08:05-08:11 | one shared working area; SNAP_M 15 m, nothing cut | zone base, masterplan |
| 09:34-09:35 | Button `run`, output `log`, logs in Bergama/logs/; the board's old `run` text input renamed `mode` | all seven (zone base v8, masterplan v14, water balance v2.2, board v37, city link v1.5, agriculture v1.1, water board v1.3) |
| 09:44-09:45 | text under the component: name, version, last run time and length, idle | all seven |
| 09:49 | data files read from Bergama/Data/ (DATA_DIR); kit zip ships `Data/` with 6 files | board, masterplan, water board (in place) |
| 09:52 | errors always reach the log panel and stay after the Button is released | water balance, city link, agriculture, zone base, masterplan, water board (in place) |
| 09:55 | temp state files removed: sticky for this session only, plus the one logs/ file | zone base, masterplan, water board, board (in place) |
| 10:15-10:20 | output `done` (stays after the run) for the one-click chain (RUN_GUIDE §2b); no double runs: city link warns if the spine bank changed | all seven (in place); board adds `done` itself |
| 10:45 | board PDFs were written into logs/ (out_folder bug from 09:35): now output/selinus_board/; the stray logs/selinus_board_pdf is deleted by the next run | board v37 (in place) |
| 10:07 | masterplan alternative 3 = exactly site_alan; zoom pages margin input zoom_m | masterplan v14 > v15 |
| 12:10 | the canvas's `log` outputs are Grasshopper's renamed `out` (printed text): every script now prints its log; MasterPlan reads ZoneBase's done from sticky when the wire brings Null (seen after a bake) | zone base v8, masterplan v16, water balance v2.2, city link v1.5, agriculture v1.1, water board v1.3, proposal sections v1, board v37 (12:15), template (in place) |
| 14:40 | masterplan sheets get a graphical legend band (samples + plain names, only what is drawn, no hex) | masterplan v16 > v17 |
| 16:35-16:50 | masterplan alt 3: alt 2 zoning in alt 1 tones, spines as zones, riverside function and circulation band | masterplan v17 > v18 |
| 16:41-16:43 | masterplan: one sheet (alt 1 with the v18 changes, PROMENADE band), option A only; project rule: all scripts drop option B | masterplan v18 > v19 |
| 16:43 | option A only, project-wide (Aras): option B removed | zone base v8 > v9, water balance v2.2 > v2.3, water board v1.6 > v1.7, proposal sections v1 > v2, masterplan v19 |
| 17:00 | VISUAL FIRST (§5b) for every output | all output scripts, one at a time from 25 Oct 17:20 (audit: batch_2026-10-25_visual_first/VISUAL_AUDIT.md) |
| 27 Oct 11:07 | output/ = final PDFs only; logs/ = all logs; cached/ = results + working files; cached/booklet/ = booklet assets; one shared path module + bg_tidy_output at the end of every run; no source footers on sheets (each script writes its [n] key to blocks.json "sheet_sources") | zone base v10, masterplan v24, water balance v2.7, board v44, city link v1.11, agriculture v1.6, water board v1.14, proposal sections v7, booklet v10, template |

## 8. A3 BOOKLET (Aras 25 Oct 18:37, every output, drawing, diagram, label and script)
- Format: every page landscape A3, 420 x 297 mm. Everything reads as ONE booklet: one grid, one type system, a logical page order.
- Pipeline: each script writes clean, separate assets (vector drawings + structured text) for its pages; ONE assembly script places them on the A3 pages and writes ONE multi-page PDF. All text stays live and editable (never outlined or rasterised): Aras finishes the pages in Illustrator.
- Content: (1) no repetition, each fact appears once, where it belongs; (2) what belongs together goes together, per page and per block; (3) no personal or internal attributions ("X's idea", "said in a chat", notes); the only sources are publicly checkable online sources; an unsourced claim is rewritten as our own design statement or removed; (4) no filler, keywords where they do the job (with §5b).
- Type, read at 40-60 cm; size follows design importance: page title 36-48 pt; section heading 20-28; subheading 14-16; key statement 12-14; body 9-11 (min 9); captions, labels, sources 7-8 (min 7). Drawing labels meet the same minimums at A3 print size. At most 2 typefaces, few weights; body lines 50-75 characters.
- Grid: one modular grid on every page (12 columns, 12-15 mm margins, 4-5 mm gutters, baseline grid); every element aligned to it; one set of spacing values; neither cramped nor large empty gaps.
- Reading order: one clear order and ONE focal point per page. Top-left = most crucial, bottom-right = least; a contrast-coloured image may be the focal hook anywhere, usually mid-page. Title block, page number, project name and legend sit in the same place on every page.
- SAME DRAWING AS THE SHEET (Aras 25 Oct 21:47): every booklet drawing is a crop of the script's own sheet PDF (the panel's rectangle written to booklet/blocks.json), shown with the sheet's own words (booklet v3, Aras 26 Oct 06:02: never re-set them). No separate booklet redraws. To change a booklet drawing, change the sheet.
- ONE DRAWING, ONE PAGE (Aras 26 Oct 06:35, lasting): never divide one drawing over two booklet pages, and show each drawing only once.
- ROUND SCALES ONLY (Aras 26 Oct 06:35, lasting): every drawing's scale is a round number (1:500, 1:1,000, 1:2,000, 1:2,500, 1:5,000, 1:10,000 ...), never 1:7,329: take the largest round scale that fits; x and y always scaled alike.
- References: library/examples/booklet_boards/ (13 boards, cards there). Theory notes and the booklet's own grid and type values: booklet/ in the project folder (design-language.md).
