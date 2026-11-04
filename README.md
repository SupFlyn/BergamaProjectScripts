# bergama-scripts

Source of the Bergama Grasshopper / Rhino 8 scripts, kept as small parts so an edit touches only a few hundred lines.
Aras still gets ONE self-contained `.py` per script (in `dist/`), the same file as before: nothing extra goes in Downloads.

## Layout
| path | what |
|---|---|
| `src/<script>/code.py` | the script's own code. Big built-in data and shared helpers are one `#@include ...` line each |
| `src/<script>/data/*.py` | built-in data (survey copies, land cover, embedded engines): never read these to edit code |
| `src/<script>/MAP.md` | function -> file and line (made by the build) |
| `src/<script>/target.txt` | the delivered file name (`bergama_city_link_v1_6.py`); change it for a new version |
| `src/common/*.py` | helpers whose text is the same in 2+ scripts. Editing one changes every script that includes it (see the `#@include ../common/` lines) |
| `dist/` | built scripts = what goes into `scripts/` and the run kit |
| `tools/` | split, build, check, offline test runs |
| `tools/script_map.py` | refreshes the line numbers in the project's `library/SCRIPT_MAP.md` (which function draws which booklet page / drawing); `tools/build.py` runs it after every build (path: `$BERGAMA_SCRIPT_MAP`, default `/mnt/project-files/library/SCRIPT_MAP.md`) |

## Edit steps (every change)
1. `python3 tools/split.py <latest delivered scripts>` only when a script came from outside the repo (the round trip must give the same bytes, or nothing is written).
2. Edit the part in `src/` (find it in `MAP.md`); for a new version change `VERSION` in code.py and the name in `target.txt`.
3. `python3 tools/build.py` -> `dist/`.
4. `python3 tools/check.py <old delivered> dist/<new>`: functions removed / added / changed, functions defined twice, new undefined names.
5. `tools/chain.sh <old scripts dir> runOld; tools/chain.sh dist runNew; tools/compare.sh runOld runNew`: all 8 scripts offline on the real survey (fake Rhino, frozen clock); same output files = no change to the product. A change that is meant to change a sheet shows only in that sheet's files.
6. `git diff` shows exactly what changed; commit; copy `dist/<new>` to the project `scripts/`, old version to `scripts/_superseded/`.

## Offline test run
`tools/run_gh.py` runs a script as a Grasshopper component would (Button pressed, `rhino_bake` off) with `tools/fakerhino.py` in place of Rhino:
the survey comes from a pickle of `Bergama_Altlik.3dm` (`tools/survey_to_pickle.py`, needs `pip install rhino3dm`), geometry is polylines,
text boxes are points, and anything not written there is a MagicMock. It is for old-vs-new comparison, not a copy of Rhino:
a sheet that looks right here can still fail in Rhino, and the other way round.
Data files: `$BERGAMA_DATA` (the run kit's `Data/` folder). Survey pickle: `$BERGAMA_SURVEY`.
