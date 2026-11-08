# Style a cutouts (30 Oct 2026)

**People and stall:** two line-drawing sheets from the Selinos board: PB_278-317 (BW pen) and PB_318-342 (grey pen). Two pimpmydrawing "SANAA people" hairline drawings (DW_015, DW_004) fill in walk and child play. Their interiors were filled white.
**Trees:** one watercolour-texture sheet by nilduygu (CS_001-030, muted greens). **Rushes:** CS_084 by eishahakc.

| key | asset_id |
|---|---|
| person_stand | PB_308, PB_322, PB_326 |
| person_walk | PB_321 (couple), DW_015 |
| person_sit_step | PB_298 (on a block) |
| person_sit_chair | PB_294 (cropped) |
- person_wade: removed by the T4 lead (a standing figure cut at the thigh read wrong); drawn as vector.
| person_bike | PB_334 |
| person_child_play | DW_004 (two children) |
| person_stall | PB_306 (buyers; counter cropped off) |
| person_vendor | PB_282 (flower seller) |
| stall | PB_299 (cart with a canopy, front elevation) |
| plane | CS_009, CS_008 |
| ash | CS_001 |
| olive | CS_027 |
| stone_pine | CS_015 |
| tamarisk | CS_023 |
| soft_rush, rush | CS_084 |

h_m for plants = h_m in plants.py. Seated heights (1.30 m) and the stall height (2.60 m) are estimates.

## Left out (drawn as vectors)
- willow: the only weeping tree (CS_149) is pink-brown and clashes with the green sheet.
- chaste, rosemary, lavender: there is no side-view shrub.
- loosestrife: the only flowers are bed bands, not single upright plants.
- person_watch: there is no figure looking down at water (PB_309 points at the sky).
- person_railing: PB_307 is three fishermen with their own railing.
- person_touch: there is no crouching figure reaching down.
- person_adult_child: there is no hand-in-hand pair in this line style (CS_159 is a collage).

## Added 31 Oct (variety; same sheets, same look)
Made by tools/cutouts/prep_library_cutouts.py from revision_2026-10-30/asset_library (trim, people interiors white, 600 px tall).
| key | asset_id |
|---|---|
| plane | + CS_007, CS_011, CS_012, CS_014 |
| ash | + CS_004, CS_006, CS_021 |
| stone_pine | + CS_016, CS_017 |
| olive | + CS_025 |
| tamarisk | + CS_022, CS_024 |
| person_stand | + PB_324 |
| person_adult_child (new key) | PB_303 |
| person_sit_step | + PB_327, PB_292 |

## Depth tones (R2-A 31 Oct 2026)
Every cutout has `<name>_d1.png` and `<name>_d2.png`: colours mixed toward the section paper F1EDDF by 40 % and 62 % (figures.py FIG_DEPTH fades of layers 1 and 2), alpha unchanged, so back figures and trees are paler but never see-through. Made by `tools/cutouts/depth_tones.py`; cutouts.json entries carry `"depth": {"1": ..., "2": ...}`.
