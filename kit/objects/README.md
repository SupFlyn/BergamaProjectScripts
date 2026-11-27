# Aras's objects for the Archicad proposal file (27 Nov 2026)

Source files: uploaded by Aras in the thread "Perfect the Archicad model" (27 Nov 2026, 14:39 UTC). Research and picks:
`research/archicad_objects_2026-11-27/ANSWER_archicad_objects_v7.md` in the project files.

| object | his file | here |
|---|---|---|
| planter | `folke_rectangular_planter.gsm` (native Archicad object) | `folke_rectangular_planter.gsm`, unchanged |
| parasol | `white-outdoor-umbrella.zip` (`white umbrella.fbx`, 1,650 triangles, 2 textures) | `gdl/market_umbrella_white.gdl` |
| kiosk | `food_vendor_kiosk_v2.glb` (232,187 triangles, 115 parts) | `gdl/food_kiosk.gdl` (30,855 triangles) |
| market stall | `U10-16C - Marknadsstånd - Väderskydd` (.rfa, 3D .dwg with 115 solids) | not converted yet |

`gdl/*.gdl` are GDL 3D scripts (VERT / VECT / EDGE / PGON bodies, one body per colour): sizes in metres, Z up, the
origin at the middle of the footprint on the ground. Colours are flat colours read from the object's own texture
pictures (the mean colour of each triangle, grouped); the texture pictures themselves are not used. The kiosk's
front (counter and sign) faces -Y.

`convert/` holds the scripts that made them (cloud only; they need trimesh, assimp-py, fast-simplification, scipy,
pillow): `conv_parasol.py <fbx> <diffuse png> <out.gdl> <this folder>`, `conv_kiosk.py <glb> <out.gdl> <this folder>
[triangle budget]`. The kiosk's small props are thinned per part (budget by the root of the part's surface, at least
48 triangles a part).

Not yet tested in Archicad when this file was written.
