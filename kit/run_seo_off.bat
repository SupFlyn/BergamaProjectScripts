@echo off
rem TEST: removes every solid element operation link in the open model (scripts\bergama_seo_off_v1.py). run_acbuild.bat brings them back.
cd /d "%~dp0"
if exist "Project Files\scripts\bergama_seo_off_v1.py" (
  py -3 "Project Files\scripts\bergama_seo_off_v1.py"
) else (
  py -3 "scripts\bergama_seo_off_v1.py"
)
