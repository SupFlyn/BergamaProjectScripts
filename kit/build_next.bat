@echo off
rem One-step AcBuild run (scripts\bergama_build_next_v6.py): newest AcBuild from GitHub main, fresh copy of the newest
rem Bergama_AC_v*.pln, Archicad opened, build, element counts, Archicad closed. Close Archicad on BOTH PCs first.
rem   build_next.bat          the whole run      build_next.bat check     reopen test + element counts only
rem   build_next.bat build --cold   caches moved aside first (v4); BUILT line + timings before the reopen (v5); --empty starts from a new empty project (v6); a split AcBuild builds _proposal, _context, master
rem Steps: logs\bergama_build_next_status.txt (last line DONE or ERROR).
cd /d "%~dp0"
if exist "Project Files\scripts\bergama_build_next_v6.py" (
  py -3 "Project Files\scripts\bergama_build_next_v6.py" %*
) else (
  py -3 "scripts\bergama_build_next_v6.py" %*
)
pause
