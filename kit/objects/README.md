# Aras's objects for the Archicad proposal file (27 Nov 2026)

Source files: uploaded by Aras in the thread "Perfect the Archicad model" (27 Nov 2026, 14:39 UTC). Research and picks:
`research/archicad_objects_2026-11-27/ANSWER_archicad_objects_v7.md` in the project files.

| object | his file | here | size (m) |
|---|---|---|---|
| planter | `folke_rectangular_planter.gsm` (native Archicad object) | `folke_rectangular_planter.gsm`, unchanged | 1.8 x 0.7 x 0.72 |
| parasol | `white-outdoor-umbrella.zip` (`white umbrella.fbx`, 1,650 triangles, 2 textures) | `gdl/market_umbrella_white.gdl` (+ `_tex.gdl`, `.png`) | 2.737 x 2.737 x 2.564 |
| kiosk | `food_vendor_kiosk_v2.glb` (232,187 triangles, 115 parts) | `gdl/food_kiosk.gdl`, 30,855 triangles (+ `_tex.gdl`, `.png`) | 2.267 x 2.728 x 2.769 |
| market stall | `U10-16C - Marknadsstånd - Väderskydd - 3D.dwg` (115 solids) | `gdl/market_stall_shelter.gdl`, 11,265 triangles, + `_2d.gdl` | 5.89 x 2.885 x 2.456 |

`gdl/objects.json` is the list AcBuild reads (`_setup_objects`, v2.16ai): per object its part name, files and true size.

`gdl/*.gdl` are GDL 3D scripts (VERT / VECT / EDGE / PGON bodies, one body per colour): sizes in metres, Z up, the
origin at the middle of the footprint on the ground, the long side along X. The kiosk's front (counter and sign)
faces -Y.

Colours:
- Parasol and kiosk: flat colours read from the object's own texture pictures (the mean colour of each triangle,
  grouped). The `_tex.gdl` versions carry the texture as well: every triangle has its own texture coordinates
  (`PGON{3}`), the picture (`.png`; for the kiosk one atlas of its 35 textures) goes into the embedded library as a file beside the part and the script names it. `objects.json` uses these versions.
- Market stall: the .dwg carries NO colours (all solids on one layer, colour by layer). ASSUMED from the look noted
  in the research answer ("Red steel shelter: double-pitched sheet roof on a row of posts with Y-struts, long timber
  table under the ridge"): the two table tops timber (0.72, 0.56, 0.38), everything else red steel (0.62, 0.12,
  0.11). The shades are ASSUMED.

`convert/` holds the scripts that made them (cloud only; they need trimesh, assimp-py, fast-simplification, scipy,
pillow, shapely, ezdwg):
- `conv_parasol.py <fbx> <diffuse png> <out.gdl> <this folder>`
- `conv_kiosk.py <glb> <out.gdl> <this folder> [triangle budget] [atlas px]`: small props are thinned per part
  (budget by the root of the part's surface, at least 48 triangles a part).
- stall: `dwg_solids.py <dwg> solids.pkl`, `sab.py solids.pkl sab.pkl` (the ACIS binary data of each solid),
  `stall_mesh.py sab.pkl <this folder> stall_solids.pkl 30 12` (`acis_mesh.py`: planes and NURBS faces to triangles,
  arcs in 30 degree steps, fillets smaller than 12 mm as one chord a quarter turn; 109 of 115 solids come out closed,
  the other 6 have open edges of about 5 mm at small holes), `conv_stall.py stall_solids.pkl <out.gdl> <out_2d.gdl>
  <this folder>`.

Tested in a scratch Archicad 30 file on the Desktop (27 Nov 2026, logs\check_objects2_2026-11-27.txt): all four go in through AcBuild's `_setup_objects` at these sizes; the textured parasol and kiosk were looked at in the 3D window (lettering readable, the right way round) and keep their flat colours in vector views.
