@echo off
rem Bergama Axo: axonometric 3D Documents from the open Archicad model (scripts\bergama_axo_v1_0.py)
cd /d "%~dp0"
if exist "Project Files\scripts\bergama_axo_v1_0.py" (
  py -3 "Project Files\scripts\bergama_axo_v1_0.py"
) else (
  py -3 "scripts\bergama_axo_v1_0.py"
)
pause
