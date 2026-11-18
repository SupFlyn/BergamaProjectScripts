@echo off
rem Bergama UE5 render launcher: pick the Archicad FBX, then UE 5.8 opens your project and runs the render script.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_ue5_render.ps1"
if errorlevel 1 pause & exit /b 1
timeout /t 8 >nul
