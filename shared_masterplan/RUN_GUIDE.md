# Shared masterplan: run guide (8 Nov 2026)

One master plan for Aras, Begüm and Nil. It's kept on GitHub (repo SupFlyn/BergamaProjectScripts, branch `shared`), merged layer by layer (newest edit wins), and opened in Rhino, Illustrator or AutoCAD from a single `Bergama.bat`.

## Once per PC
1. Copy `bergama_shared_sync_v1.py` to `Downloads\Bergama\`.
2. Copy `planting_areas_seed.svg` to `Downloads\Bergama\Data\assets\`. `agaclar.svg` must also be in that folder.
3. Put `Bergama.bat` anywhere you like, for example on the Desktop. `setup.bat` can go anywhere too.
4. Double-click `setup.bat`.
   - **Who are you:** press 1 aras, 2 begum or 3 nil.
   - **GitHub token:**
     - Aras presses 2 once. The GitHub token page opens in the browser. Use these settings: name *Bergama shared*, expiry 366 days, owner SupFlyn, only BergamaProjectScripts, Contents read and write. Generate the token, then paste it into the setup window (it stays hidden).
     - Send the token to Begüm and Nil privately, never in a chat with Claude. They press 1 and paste it.
     - The token is checked against the repo and saved in `Data\shared_settings.txt`.
   - **Python:** Windows asks for admin rights, then Python 3.13.17 is installed for all users.

## Grasshopper (Rhino 8), once
There are three Python 3 Script components, each with the whole file pasted in, wired as a chain:
`SharedSync` (bergama_shared_sync_v1.py, input `run` = Button) → `done` into `run` of **PlanToRhino v2** (bergama_plan_to_rhino_v2.py, `LineDrawing` = True) → `done` into `run` of **PlantingAnalysis** (bergama_planting_analysis_v1.py).
One press runs all three: upload your Rhino edits, merge, load the master into Rhino, rebuild the planting analysis.

## Every day: double-click Bergama.bat
Press 1, 2 or 3. No other key does anything. After the key the window hides and the work runs in the background. If something goes wrong, a window opens with the error in bold red.

- **1 Rhino:** syncs, then opens Rhino with the newest `.3dm` in `Downloads\Bergama`. To choose the file, add `rhino_file=<path>` to `Data\shared_settings.txt`. In Rhino, press the Button.
- **2 Illustrator:** syncs, then opens `Data\shared\my_masterplan.svg`. Edit it and save. The first time, use File > Save As > SVG and set More Options > **Decimal Places: 7**. After that, Ctrl+S keeps the setting. Close Illustrator and it syncs again on its own.
- **3 AutoCAD:** syncs, then writes `Data\shared\masterplan_latest.dxf` and the folder `masterplan_latest_images\` next to it, and opens AutoCAD. The DXF is an AutoCAD 2010 file with:
  - exact curves
  - transparency
  - dash patterns as linetypes
  - pictures as linked files, so keep the folder next to the DXF
  - clip groups cut to their outline
  - one layer per plan layer, trees as blocks

  AutoCAD edits are not read back yet.

If a program isn't found, add its path to `Data\shared_settings.txt` as `rhino_exe=`, `illustrator_exe=` or `autocad_exe=`.

## Where things are
| what | where |
|---|---|
| combined master + 10-version list | GitHub, branch `shared`, `shared/master/masterplan_latest.svg` (every merge is in the history) |
| each person's latest file | GitHub, `shared/people/<name>/masterplan.svg` |
| edit date + editor of every layer | GitHub `shared/master/state.json`, Rhino layer user text `edited` / `edited_by`, and the log |
| losing versions of a layer | GitHub `shared/master/conflicts/` and `Data\shared\conflicts\` |
| the plan Rhino reads | `Data\assets\plan\masterplan_latest.svg` |
| planting analysis board | `Data\analysis\planting_analysis.svg` (the run before is kept as `_prev`) and Rhino layer `masterplan::analysis_planting` |
| log | `Downloads\Bergama\logs\bergama_shared_sync_log.txt` |

## How you know it works
The notification says "Bergama sync done – master is up to date". The log ends with the list of layer dates and the last versions. On GitHub, branch `shared` holds `shared/master/masterplan_latest.svg`.
