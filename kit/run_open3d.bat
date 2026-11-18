@echo off
rem Opens the whole Archicad model in 3D one BGA layer at a time (scripts\bergama_open3d_v1.py). Archicad 30 + Tapir with Bergama_site.pln open.
cd /d "%~dp0"
if exist "Project Files\scripts\bergama_open3d_v1.py" (
  py -3 "Project Files\scripts\bergama_open3d_v1.py"
) else (
  py -3 "scripts\bergama_open3d_v1.py"
)
