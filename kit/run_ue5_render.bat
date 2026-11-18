@echo off
rem Bergama UE5 render launcher (lives in Downloads\Bergama; its helper is scripts\run_ue5_render.ps1).
rem Pick the Archicad FBX, then UE 5.8 opens your project and runs the newest scripts\bergama_ue5_render_v*.py.
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\run_ue5_render.ps1"
if errorlevel 1 pause & exit /b 1
timeout /t 8 >nul
