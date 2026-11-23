@echo off
rem One-step AcBuild run (scripts\bergama_build_next_v1.py): newest AcBuild from GitHub main, fresh copy of the newest
rem Bergama_AC_v*.pln, Archicad opened, build, element counts, Archicad closed. Close Archicad on BOTH PCs first.
rem   build_next.bat          the whole run      build_next.bat check     reopen test + element counts only
rem Steps: logs\bergama_build_next_status.txt (last line DONE or ERROR).
cd /d "%~dp0"
if exist "Project Files\scripts\bergama_build_next_v1.py" (
  py -3 "Project Files\scripts\bergama_build_next_v1.py" %1
) else (
  py -3 "scripts\bergama_build_next_v1.py" %1
)
pause
