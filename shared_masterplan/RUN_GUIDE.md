# Shared masterplan v2: run guide (8 Nov 2026)

One masterplan for Aras, Begüm and Nil. Everyone edits it, mostly in Illustrator and sometimes in Rhino. Every run builds one combined file, layer by layer, from everyone's newest edits. The files are kept on GitHub (repo SupFlyn/BergamaProjectScripts) and opened from one `Bergama.bat`.

## Once per PC
1. Put these files in `Downloads\Bergama\`: `bergama_shared_sync_v2.py`, `bergama_plan_to_rhino_v2.py` and `bergama_planting_analysis_v1.py`.
2. Put `planting_areas_seed.svg` in `Downloads\Bergama\Data\assets\`. `agaclar.svg` must be in the same folder.
3. Put `Bergama.bat` and `setup.bat` anywhere, for example on the Desktop.
4. Double-click `setup.bat`:
   - **Who uses this PC:** press 1 aras, 2 begum or 3 nil. One person can use several PCs.
   - **GitHub token:** Aras presses 2 once and makes the token in the browser page that opens. The settings are: name *Bergama shared*, expiry 366 days, owner SupFlyn, only BergamaProjectScripts, Contents read and write. Aras sends it to Begüm and Nil privately, never in a chat with Claude, and they press 1 and paste it. The token is checked and saved in `Data\shared_settings.txt`.
   - **Python:** Windows asks for admin rights once, then Python 3.13 is installed for all users. Nothing else is ever installed.
5. **Aras only, once:** open Rhino with option 1 one time. This gives the plan's survey placing to everyone's planting analysis.

## Every day
1. Double-click `Bergama.bat`.
2. Press **1 Rhino** or **2 Illustrator**. Any other key does nothing.
3. The window hides and a notification says it's syncing. Your edits go up, everyone's newest edits come down, and the program opens the combined file.
4. Edit and save:
   - **Illustrator:** the file is `Data\shared\my_masterplan.svg`. The first time, use File > Save As > SVG > More Options and set **Decimal Places 7**. After that, Ctrl+S is enough.
   - **Rhino:** just save (Ctrl+S). Your changed layers are written to your shared file automatically.
5. Close the program. It syncs again on its own and uploads your edits.
6. A notification says "Bergama sync done". If something fails, a window opens with the error in bold red. The log is at `Downloads\Bergama\logs\bergama_shared_sync_log.txt`.

## How the merge decides
- Each layer (a top group in the SVG, which is one Rhino layer) carries its own edit date: the time the file was saved, on GitHub's clock.
- If only one person changed a layer, theirs is used. If two or more changed it, the newest save wins.
- Every losing version is saved whole, with its date, in the `conflicts` folder, both in the cloud and in `Data\shared\conflicts\`. Nothing is ever deleted.
- A deleted layer is removed only if the deletion is newer than every edit of that layer.
- Opening and saving without changes keeps the dates.
- The log lists every layer, where it came from, its date (in this PC's time) and who edited it.

## Where things are
| what | where |
|---|---|
| combined file, your folder, Begüm's, Nil's | GitHub > Releases: `bergama-latest`, `bergama-aras`, `bergama-begum`, `bergama-nil` (10 newest versions each) |
| losing versions | GitHub > Releases `bergama-conflicts` and `Data\shared\conflicts\` |
| pictures inside the plan | GitHub > Releases `bergama-images` (stored once, not in every version) |
| layer dates register | `state.json` on branch `shared` |
| your working file | `Data\shared\my_masterplan.svg` (the one before the last sync: `my_masterplan.svg.prev.svg`) |
| planting analysis | `Data\analysis\planting_analysis.svg` and, in Rhino, layer `masterplan::analysis_planting` |

Cloud files are compressed (`.svg.gz`) and their pictures are kept separately, so a file downloaded by hand from GitHub opens without pictures. Use the copies in `Downloads\Bergama` instead.

If a program isn't found, add its path to `Data\shared_settings.txt` as `rhino_exe=` or `illustrator_exe=`. To choose the Rhino file, add `rhino_file=`.

## How you know it works
The notification says the combined file is up to date. The log ends with the layer list and the 10 versions in `latest`. On GitHub, Releases shows `bergama-latest` with the new file.
