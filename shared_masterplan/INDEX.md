# Shared masterplan + planting analysis (8 Nov 2026): read first
| file | what |
|---|---|
| RUN_GUIDE.md | setup once, daily use, where things are |
| Bergama.bat | the launcher: 1 Rhino, 2 Illustrator, 3 AutoCAD (works from any folder) |
| setup.bat | once per PC: your name + GitHub token, then system-wide Python 3.13.17 |
| bergama_shared_sync_v1.py | upload own edits, download all, merge per layer (newest wins, losers to conflicts), DXF export; GH component SharedSync and the script Bergama.bat runs |
| bergama_plan_to_rhino_v2.py | the master SVG into Rhino layers (planting areas as proposal_planting_<species>), full rebake after a merge |
| bergama_planting_analysis_v1.py | the planting board (look of v9) rebuilt from the layers each run; species drawings read live from agaclar.svg |
| planting_areas_seed.svg | first planting areas, traced from board v9 (about ±3 m): goes to Data\assets\ |
