# kit/ = the cloud folder of the board builder

The Grasshopper board builder (`scripts/bergama_build_gh_chain_v3.py`) reads this folder on branch `main` at every press.
It downloads `scripts/needed_files.txt` first, then exactly the files on that checklist, to `Downloads/Bergama/<same path>`.

## RULE (Aras, 8 Nov 2026 15:13-15:14 UTC): every script update updates this folder
For every script update, in the same change:
1. Put the new script version in `kit/scripts/` and delete the old version from `kit/scripts/`.
2. Put any new or changed Data file (data .py, assets, photos ...) in `kit/Data/`.
3. Update `kit/scripts/needed_files.txt`: every file any script needs, one per line (`scripts/<file>`, `Data/<path>`, a folder ends in `/`).
4. Update `kit/scripts/board_order.txt` if a script is added, removed or its chain place changes.
5. Merge to `main`. The builder itself is never edited for this.
