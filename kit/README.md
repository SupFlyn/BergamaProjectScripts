# kit/ = the cloud folder of the board builder

The Grasshopper board builder (`scripts/bergama_build_gh_chain_v3_3.py`) reads this folder on branch `main` at every press.
It downloads `scripts/needed_files.txt` first, then exactly the files on that checklist, to `Downloads/Bergama/<same path>`.

## RULE (Aras, 8 Nov 2026 15:13-15:14 UTC): every script update updates this folder
For every script update, in the same change:
1. Put the new script version in `kit/scripts/` and delete the old version from `kit/scripts/`.
2. Put any new or changed Data file (data .py, assets, photos ...) in `kit/Data/`.
3. Update `kit/scripts/needed_files.txt`: every file any script needs, one per line (`scripts/<file>`, `Data/<path>`, a folder ends in `/`).
4. Update `kit/scripts/board_order.txt` if a script is added, removed or its chain place changes.
5. Merge to `main`. The builder itself is never edited for this.
6. Update `kit/scripts/script_reads.txt` (what each script reads: `<file prefix>: <path under Downloads/Bergama>`, folders end in `/`, `<file prefix>: rhino` for Rhino-layer readers). The builder's `run_after` uses it to run only the scripts whose inputs changed; a script with no lines there always runs. Never write it by hand: test-run the scripts with `tools/trace_reads.py` (records every file each script really opens, lists and writes, and whether it reads the Rhino model) and regenerate it with `python3 tools/make_script_reads.py kit/scripts/script_reads.txt <cold run> <warm run>`.
7. No script may read a later script's results (Aras, 8 Nov 2026): data flows only forward in `board_order.txt` order, so one pass gives the final result, cold or warm.
8. Speed caches: `kit/scripts/cloud_cache.txt` lists the cache folders the builder backs up to the GitHub Release `bergama-cache` (download missing files before the run, upload new/changed after, remove ones gone locally). Cache files must be named so a file is only used when its inputs match (fingerprint in the name or a key check).
