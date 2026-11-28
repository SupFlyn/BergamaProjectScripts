# Handover: Archicad site model (AcBuild), 28 Nov 2026

From the thread "Perfect the Archicad model" (26 to 28 Nov 2026) to the next Archicad thread. Read sections 1 to 3 first; the rest is reference. Older history (v2.00 to v2.16ag): `library/_index/knowhow/archicad_acbuild.md`.

All times UTC. Aras is in Europe/Athens (UTC+2); the Desktop's clock shows UTC+3. Every number below was measured on the Desktop or read in the code, unless it says ASSUMED or NOT KNOWN.

## 1. Start here

| Need | Where |
|---|---|
| Build script | `kit/scripts/bergama_acbuild_v2_16al.py`, GitHub main f64e2be (PR #764 to #775), git blob f1a98d2dd8435c0c09014fcbc6215f7e6eb671d0, 979,303 bytes. Line 40 (`VERSION = ...`) tells every version's changes. |
| Launcher | `kit/scripts/bergama_build_next_v9.py` (blob cc06924b...): `build --from <master.pln> --acbuild <file>`; without `--from` it copies the newest built files. |
| Aras's four objects | `kit/objects/` on main (README there). Working copies and his source files: `/mnt/project-files/archicad_objects_2026-11-27/` (INDEX.md there). |
| Newest checked model | Desktop `Project Files\archicad\Bergama_AC_v2.16al.pln` (master) + `_proposal` + `_context` |
| NOT a source | `Bergama_AC_v2.16aj*` (complete set, but no kiosk and steep spots left out); `Bergama_AC_v2.16ak_proposal.pln` (built, no kiosk) and `v2.16ak_context.pln` (an unbuilt copy); there is no ak master. Never `Bergama_AC_v2.16ae.pln` (town twice). |
| Check logs, Desktop `Project Files\logs\` | `check_v2_16al_2026-11-27.txt`, `check_v2_16al_floaters_2026-11-27.txt`, `check_v2_16ai_2026-11-27.txt`, `check_v2_16ai_ground_2026-11-27.txt`, `check_v2_16ai_slope_2026-11-27.txt`, `check_objects_2026-11-27.txt`, `check_objects2_2026-11-27.txt`, `check_sym_pictures_2026-11-27.txt`, `check_v2_16ah_2026-11-27.txt` |
| Probe scripts, Desktop `Project Files\cached\probe_tool\` | `gr_ai.py`, `gr_ana.py` (ground), `gs_ai.py`, `gs_ana.py`, `mp_paint.py` (slope), `mc_aj.py`, `ak_ana.py`, `al_g.py`, `al_h.py`, `al_i.py` (model check), `fl_read.py`, `fl_ana.py`, `fl_row.py`, `fl_2.py`, `fl_34.py` (floaters), `sym_left.py`, `cmp_logs.py`, `tapir_schemas.json` (790 Tapir commands) |
| Memory notes | project-v216al-state-2026-11-27, project-causes-check-pending-2026-11-28, project-v216aj-todo-2026-11-27, project-objects-delivery-2026-11-27, project-v216ai-state-2026-11-27, project-v216ai-todo-2026-11-27, project-v216ah-state / -code / -plan-2026-11-27, project-symbol-layers-2026-11-27, reference-tapir-stairs-hotlinks-library-2026-11-27 |

Next version name: **v2.16am**. Letters stay until Aras has seen the 3D (his words: "Version name still stays at alphabetic because i havent seen the 3D yet"). Main keeps the last 8 script versions (ae to al now): adding one removes the oldest (`git mv` the oldest to the new name, then copy the newest over it).

## 2. The three open items

### 2.1 Twenty objects float, and their cause check did not finish

Measured in v2.16al with ALL layers of BOTH files (true footprints, exact triangles from `Get3DGeometryOfElements`, log `check_v2_16al_floaters_2026-11-27.txt`). Of 47 suspects 27 stand on something (terrain, a cover mesh, one bench on a boulder, one lounger on the autumn water mesh, one bench on a bin). These 20 really float:

| Group | Where (survey m) | Float |
|---|---|---|
| 5 benches of the river row | 29799.30,32425.10; 29798.36,32427.53; 29797.42,32429.95; 29796.48,32432.38; 29795.54,32434.80 | 0.324, 0.375, 0.565, 0.743, 0.881 m over Mesh "BGA River + water" |
| 4 benches | 30984.90 to 30988.06, 30971.81 to 30978.94 | 0.049, 0.088, 0.093, 0.107 m over Terrain |
| 2 benches | 30691.16,31147.53; 30720.84,31084.87 (the second is a bench beside a single parasol) | 0.138; 0.092 m |
| 2 loungers | 30350.33,31608.76; 30353.20,31606.77 | 0.158; 0.280 m |
| loungers | 31025.32 to 31028.63, 30908.62 to 30929.06 | 0.033 to 0.122 m |
| 1 figure (Woman Walking) | 30354.22,31610.79 | 0.587 m |

What is known about the river row: the benches' bottoms equal the survey (AcBuild's TIN: 71.409, 71.386, 71.395, 71.494, 71.737, 72.119). The built "BGA River + water" mesh top there is 70.59 to 70.91. So the built river ground lies 0.3 to 1.4 m under the survey, and `build_objects` takes the survey (`gz0 = tin.z`, then `on_slab`). AcBuild has a built-ground function, `SEAT_GZ[0]` (`_seat_ground`, `_bed_fn`: the river bed inside his river outline, the survey elsewhere), set before the build steps and used by the seating step.

The cause check was briefed on 27 Nov 19:15 and never reported: the Desktop went offline (28 Nov 07:38: no device listed). Brief it again, read only, log `logs\check_v2_16al_causes_2026-11-27.txt`:
1. River row: are the six bench middles inside his river outline (`SEL` "river" rings), and what does `SEAT_GZ[0]` give there against the built mesh top and the survey? Over the whole proposal file: how many objects of `build_objects` (trees, lamps, furniture, symbol objects, people) lie inside the river outline, and for 30 of them the bottom against the built river mesh top.
2. The 14 and the figure: survey height, built Terrain top and the difference at the footprint points; then why the built ground is lower: (a) triangulation between the tile's own height points, (b) ground lowered on purpose (a cover piece in `COVER_PIECES`: label, mat, solid, plat, low, built or dropped as a small leftover; his slab's cut in `SITE_TOP`; the half-round or river seating dig; a reed dig), (c) something else.
3. Streets meshes BGA-streets-4390d53f (at 51.346) and BGA-streets-75fa0540 (at 53.517) lie 0.9 to 1.8 m under Terrain tops of 52.3 to 54.4 at 30530.91,31291.95; 30540.96,31315.00; 30574.78,31277.19; 30582.47,31268.74. Is that the flat bottom of a body whose top is at the surface elsewhere (no fault), or a buried street?
4. What refuses the parasol at 29706.53,32726.49: replay `_Spread` in the offline harness. It is inside site_alan, the ground is 80.507, and two "Man Waiting" figures stand 0.64 m from the spot.
5. The bench at 29862.82,32251.12 stands half on Slab "BGA Proposal - canopies + our buildings" BGA-buildings-fcb626c2 (top 71.101, terrain 70.59 to 70.66): what is that slab, and does `SITE_TOP` hold it?

Likely fix for the river row, NOT confirmed: `build_objects` takes its ground from `SEAT_GZ[0]` instead of `tin.z`. Measure first (Aras: "solve the problems on the root cause dont implement band aid fixes").

### 2.2 Stall colours are ASSUMED

The stall's 3D drawing (.dwg, 115 solids on one layer) carries no colours. Red steel (0.62, 0.12, 0.11) for everything and timber (0.72, 0.56, 0.38) for the two table tops are ASSUMED from the look described in the research note; the product pictures could not be fetched. Aras was asked on 27 Nov and 28 Nov and has not answered. To change: the two `DEFINE MATERIAL` lines of `kit/objects/gdl/market_stall_shelter.gdl` (lines 2 and 44229), and `RED`, `TIMBER` in `kit/objects/convert/conv_stall.py`. The part is re-sent by itself when its text changes (`_part_same`).

### 2.3 Which way the kiosk faces

It stands at 31276.07,30900.07 at 341.8 degrees (his picture's long side, -18.2 degrees). The part's front is its -Y side; it looks toward plan direction -0.313, -0.950 (south-south-west) onto the terrain mesh, with no path, deck, wall or tree within 10 m in front. His picture ("pazar", 11.33 x 9.53 m, 5 filled rings, not symmetric: painted centroid 0.95 m off the box middle) marks no front. The nearest path or cover edge is 23.34 m away at bearing 39 degrees from +x, roughly behind the kiosk. Aras was asked twice whether it should turn and has not answered. `sym_objects` takes the angle from the picture (`g["ang"]`); a turn needs an extra angle per kind, which does not exist yet.

## 3. Aras's instructions in force (his words)

- 27 Nov 11:40 "While these researches are done on other account please fold in other fixes before aswell"; 11:43 "And solve the problems on the root cause dont implement band aid fixes".
- 27 Nov 11:52 "No only in proposal file, maybe just parks might need furnishing however using low quality lightweight archicad items are fine" (his objects and symbol furniture: proposal file).
- 27 Nov 12:35 "And please also apply those items directly into the archicad file"; 13:07 "Keep the positions around how masterplan is made".
- 27 Nov 14:42 "Apply the fixes back to back dont wait on me also please mix and match the file types to maximise the quality in the archicad file".
- 27 Nov 18:24, decision card "Choose how furniture stands where your ground slopes steeply": he chose "Keep all, set into the ground" (the other options: skip steep spots; leave as built).
- Earlier, still in force: "Lets not do it from empty file"; "please try to keep fixes more bundled together because every archicad build costs time to us"; "Size is totally irrelevant proportions are so little important those are last first prio is the look"; "You can rewrite the script if you feel the need for it. Perfection is onto you. You'll check every entity that comes out of the script for realism and correctness"; "Feel free to change approach where you fail to fix after few trials"; "I am away almost all the time so feel free".
- 28 Nov 07:40 "resolve this thread do all the library work and open new thread in opus 5.5 high effort"; 07:41 "Do all handovers as detailed as you can", "Do the library and indexing and pointing as always".

## 4. Versions of this thread

| Version | PRs | What it changed | Built |
|---|---|---|---|
| v2.16 to v2.16ag | up to #762 | canopy frame, walls without filler pieces, symbol layers as library objects, seating rows + stairs (see archicad_acbuild.md) | yes |
| v2.16ah | #763 | ONE story per file (plans draw the model), house snap rewrite, N2 box moved off his canopy, park shrubs clear of furniture | yes, checked |
| v2.16ai | #764 to #772 | canopy base plates on one deck and columns moved to where a plate fits, Y arms 1.3 m past the column's foot, boulders (81 outlines cleaned), house thin parts; `_setup_objects` + real sizes in `sym_objects`; textures as picture files | yes, checked |
| v2.16aj | #773 | `_stand` (lowest surface under the footprint), `SYM_FALL_M` 0.20 leaves steep spots out, `_cover_up`, `_Spread.free(skip=)`, `SYM_LIB` / `SYM_OFF` / `SYM_BOX` | yes; lost the kiosk; not a source |
| v2.16ak | #774 | Aras's choice: nothing left out for the slope; `SYM_FALL_M` only counts in the log | proposal only, stopped |
| v2.16al | #775 | `OBJ_KIND`: his objects found by the kind in `objects.json`; word search only for the pick-up, tie by name, no picture files | yes, checked: THE CURRENT MODEL |

## 5. Code map of what this thread touched (v2.16al)

- `setup_library` (about line 6356): `_setup_library`, then `_setup_objects`, then `GetAvailableLibraryParts` and `_lib_trees`, `_lib_furn`, `_lib_sym(nms_ - pic_)`.
- `_setup_objects(ac, log)`: only when `SCOPE[0] == "proposal"`. Reads `OBJ_DIR\gdl\objects.json` (`OBJ_DIR` = `Project Files\objects`). A "gsm" item goes in with `AddFilesToEmbeddedLibrary` (type Object, folder `Aras/`); a "script3d" item with `CreateLibraryParts` (name, parentName, path `Aras/<name>.gsm`, script3D, script2D, a, b, parameter ZZYZX), its "picture" first as a Pict file `Aras/<file>.png`. Fills `OBJ_SIZE[name] = (a, b, foot)` and `OBJ_KIND[kind] = name`. `_part_same` / `_part_sent` skip a part whose content is already in the project.
- `_lib_sym(names, log)`: `SYMLIB[kind] = (part, origin offset)` from `SYM_LIB` (library parts), then `OBJ_KIND` (his objects), then the word search `SYM_MISSING` (pick-up only now).
- `sym_plan` builds `SYM_PLAN` (his symbol pictures: kind, middle, L, W, angle, painted shape); `_sym_spots` the grid of spots; `sym_objects(xy, z0, gz, ins, free, log)` places them. Per picture: grid = object + `SYM_GAP_M` 0.6 (ASSUMED); in a `SYM_ROW` picture ("stall_umb") stall and parasol stand side by side across the row; a bench stands beside the parasol foot (`SYM_BENCH_D` 0.65). Per spot: `_stand` height, inside site_alan, footprint not within 0.3 m of another of his objects, then the free-spot test.
- `_stand(gz, c, ang, hx, hy)`: (lowest surface, fall) over 9 points of the support rectangle; a parasol's support is its foot (half width 0.244).
- `build_objects` (about line 6758): `gz0 = tin.z`; `on_slab(p, g)` returns his slab's top where the slab is the surface (`SITE_TOP`), else `g + _cover_up(p)`; `_cover_up` = `COVER_UP` (0.05 on road, pavement, quay_grey, bike, path) of the hard cover piece at p. Park furniture (`_park_items`, about line 6883) uses `_stand` too.
- `_Spread.free(c, r, skip=None)`: registers what it accepts; a bench passes its own parasol as `skip`.
- Canopies: `build_canopies`; constants `CAN_Y_ARM_M`, `CAN_COL_IN`, `CAN_PLATE_CLR`. Houses: `_snap_houses`, `_house_thin`, `_house_overlaps`, `_house_check`. Boulders: `_spikes_out`.

## 6. Aras's four objects

| Object | Part name | Source he uploaded | Made as | Size m (x, y, z) | Triangles |
|---|---|---|---|---|---|
| Planter | folke_rectangular_planter | .gsm | native, added as it is | 1.8 x 0.7 x 0.72 (Archicad's box says 0.1 tall) | 316 polygons |
| Parasol | Market Umbrella White | white-outdoor-umbrella.zip (FBX + 2 textures) | textured GDL mesh, `market_umbrella_white_tex.gdl` + `.png` | 2.737 x 2.737 x 2.564, foot half width 0.244 | 1,650 |
| Market stall | Market Stall Shelter | .rfa + zip with a 3D .dwg (AC1021, 115 3DSOLID) | GDL mesh from the ACIS solids, `market_stall_shelter.gdl` + `_2d.gdl` | 5.89 x 2.885 x 2.456 | 11,265 |
| Kiosk | Food Kiosk | food_vendor_kiosk_v2.glb (232,187 triangles) | textured GDL mesh thinned to 30,855, 2048 px atlas of 35 textures, `food_kiosk_tex.gdl` + `.png` | 2.267 x 2.728 x 2.769, front -Y | 30,855 |

- Conversion scripts: `kit/objects/convert/` (`mesh2gdl.py`, `conv_parasol.py`, `conv_kiosk.py`, `conv_stall.py`, `stall_mesh.py`, `acis_mesh.py`, `sabread.py`, `sab.py`, `dwg_solids.py`, `colors.py`). The .dwg is read with the `ezdwg` wheel's raw records and my own ACIS binary reader; 6 of 115 solids have about 5 mm open edges at small holes (GDL does not need closed bodies).
- GDL shape: per colour `DEFINE MATERIAL`, `BASE`, `VERT`, `VECT`, `EDGE`, `PGON` (textured: `PGON{3}` with u, v per corner), `BODY -1`; texture `DEFINE TEXTURE "<part> tex" "<file>.png", 1, 1, 0, 0`. In the 3D window both textured parts show their textures; vector views keep the flat colours.
- His files are untrusted input: nothing from them is run; Python that reads them runs with `-I` from another folder.
- Counts: v2.16af planned 94 stall and 67 parasol spots with both on one spot. With real sizes and side by side: 52 stalls, 38 parasols (34 beside stalls at 3.41 m, 4 single ones in the "bank" pictures), 39 planters, 1 kiosk. The 40th planter and 4 benches belong to the context file, where his objects are not loaded.
- No download route works from the cloud (gofile and bimobject are blocked by the network policy; the Desktop's safety check refused the gofile script; the Google Drive connector lacks a permission). Aras uploads files in the thread.

## 7. State of v2.16al (measured)

- No errors. FLAG lines (old, unchanged): 1 house outline still crossing itself (v1.78 line; the final house check says 0 crossing), 26 ground tiles over accuracy even at 1 m, 11 reed beds with no spot under the water, trees_rosemary 19 x 1 m ASSUMED. Context and master also say "no library object for kiosk, parasol, planter, stall" (expected: proposal only).
- Elements: proposal 16,369 (Object 9,753), context 42,679, master 59,192, all on story 0. Builds 149 s, 177 s, 409 s; master reopen 77 s, 3D window 35 s. Builds are fast because unchanged elements are kept (same Element ID and data).
- Proposal objects: planter 39, parasol 38, stall 52, kiosk 1, Pick-up 2 (on their picture middles), Outdoor Bench 327, Table with Benches 34, Deck Lounger 50, Bicycle Holder 41, Metal Garden Table 14. The 4 benches beside the single parasols stand 0.10 m from the foot.
- His four kinds: none floats; none within 0.3 m of another object, a column, a tree, a wall or a house; none on water or on a planting bed.
- Set more than 0.20 m into the ground (his choice): stall 25 (1.428 at 29713.47,32716.56; 1.294 at 29706.68,32723.08; 1.022 at 29720.26,32710.03), planter 7 (0.346 at 29749.14,32586.56), Pick-up 1 (0.481), bench 32 (1.025 at 29958.15,32280.26), picnic table 10 (0.786 at 29752.24,32568.97), lounger 13 (0.333), bike holder 8 (1.074 at 29805.72,32461.48), garden table 10 (0.247). At the two deepest stalls the uphill end of the table top is 0.287 and 0.122 m IN the ground; the roof edge is 1.18 and 1.34 m over it.
- Slopes behind that (plane fit): north-west market picture 29703.67,32717.78 (41.2 x 21.7 m, 11 stalls, on his "bisiklet" paint) 9.0 %, ground 78.893 to 82.723; stall pictures beside it 3.8 to 14.5 %; planter pictures 29729 to 29761, 32564 to 32598: 10 to 24.5 %; market 31259.95,30870.52 (20 stalls) 1.4 %; the six benches near 29953 to 29966, 32278 to 32282 stand on a bank of 34 to 98 %. No wall, stair or deck lies in any of those pictures.
- Hard covers: lamps, bins and benches stand within 0 to 3 cm of the cover top.
- Canopies: 28 Y columns on 28 base plates, 0 plates over two decks, 55 arms, no armless column. Boulders: 823 slabs, all valid. Houses: final check 0 crossing, 0 short sides, 0 pairs in each other; context double walls 719 within one house + 8 between two houses (v2.16ah: 721 + 8; survey shapes with sharp corners).
- Master: hotlinks to the two v2.16al files, views N1-P0 to N6-P1 in "Bergama sections" plus Site, publisher sets "1 - Layouts" and "2 - Views".

## 8. Smaller open points

- Park benches (43) are placed by the part's ORIGIN: the bench middle lies 0.90, -0.32 m from the planned point, so the clash and ground tests look at the wrong place.
- Three narrow house strips (rings 206, 892, 1603) that `_house_thin` does not cut: the sliver's mitre grows back over the strip. Tried and dropped: mitre 60, round grow-back, corner-tip test.
- Canopies 2 and 3 share an edge (30430.18,31550.68 to 30448.01,31536.92), each with its own frame member, tops 0.41 to 0.47 m apart, as he drew them. His canopy rings 10/13 (64.6 m2 at 29804.05,32275.93) and 11/14 (55.4 m2 at 29778.76,32386.47) overlap as drawn. Both need his look.
- Node plans are framed views of the one plan. A true cut plan needs the Floor Plan Cut Plane height set by hand per view (NOT tested); Tapir cannot set it.
- Weight of the stalls: 52 x 11,265 triangles is about 0.59 million (calculated); the 3D window time did not change (35 s against 35.1 s in v2.16ah).
- Not yet told to Aras: the kiosk was thinned from 232,187 to 30,855 triangles; node plans are framed views; the river step at 31288,30792 is right flat; build times.

## 9. Working with the Desktop

- One Remote Control session per thread, folder `C:\Users\Administrator\Downloads\Bergama` (environment env_01HweQvdNhiue1RQVM2g3YoH). Brief it in full sentences with the file, its git blob id and size; it fetches from main through the git blob API and checks the id. It does not edit AcBuild.
- A refusal on the PC means stop and report: never another route round it. Approvals count only when Aras types them in the thread. The safety check there refuses to overwrite some existing scripts; new file names are fine.
- One Archicad at a time (shared key); restart it after each run; AutoSave leftovers are moved aside, never deleted; never bring Archicad's main window to the front during start-up; never close the "Student version" dialog by script; no hand fixes in the model; probe copies are never saved; existing `Bergama_AC_v*.pln` files and `_archive` folders stay.
- Builds go into copies of the newest COMPLETE set (`--from`), never `--empty` or `--cold`. A stopped launcher can still start the next Archicad in the same second: check what it left behind.
- A model check that means something: exact triangles (`Get3DGeometryOfElements`) of every slab and mesh under the true footprint, ALL layers of BOTH files. My first float measure left out the water layers and read 10 m of float that was not there; axis-aligned boxes overstate turned objects.
- Tapir facts from this thread: a part made with `CreateLibraryParts` is not editable (`SetLibraryPartPictureImages` fails); `GetAvailableLibraryParts` lists pictures too (documentName "food_kiosk", fileName "food_kiosk.png", type "Image"); `InterpretGDLScript3D` gives the true 3D box, `Get3DBoundingBoxes` takes z from A / B / ZZYZX; `Get3DModelCounts` returns 0; there is no API import of DWG, RFA, FBX or USD; switching the 3D style by API crashes Archicad.
- In the cloud: static checks only (`python3 -W error -m py_compile`, `ruff --select F,E9`: 6 old hits are known); single functions may be tried on made-up numbers, said so in the PR. No offline run of the script. Building libredwg from source was refused by the permission check twice: not to be retried.

## 10. ASSUMED values this thread added

`SYM_GAP_M` 0.6 m (room between his objects), `SYM_FALL_M` 0.20 m (log count only), `SYM_BENCH_D` 0.65 (measured bench depth), stall colours (2.2), picnic table size 2.80 x 2.10 and bike holder 2.6 x 0.25 (calculated from plan boxes), tree trunk radius 0.25 m in the Desktop's clash check.
