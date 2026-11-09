@echo off
rem Bergama Group 6 - shared masterplan v2 (8 Nov 2026). Double-click, press 1 or 2.
rem 1 Rhino / 2 Illustrator: upload your edits, download all, merge layer by layer, open the combined file in that app.
rem Works from any folder (Desktop too). Needs: setup.bat run once (system Python), Data\shared_settings.txt (token=..., me=...).
if "%~1"=="__run" goto run
title Bergama
echo.
echo    BERGAMA - shared masterplan
echo.
echo    1  Rhino
echo    2  Illustrator
echo.
choice /c 12 /n /m "   Press 1 or 2: "
set "APP="
if errorlevel 2 set "APP=illustrator" & goto go
if errorlevel 1 set "APP=rhino" & goto go
exit /b
:go
powershell -NoProfile -WindowStyle Hidden -Command "Start-Process -WindowStyle Hidden -FilePath $env:ComSpec -ArgumentList '/c','\"%~f0\" __run %APP%'"
exit

:run
rem ---- hidden from here: find the system Python (setup.bat), run Downloads\Bergama\bergama_shared_sync_v2.py ----
set "PYW="
set "PYA="
for /f "delims=" %%p in ('where pyw 2^>nul') do if not defined PYW set "PYW=%%p"
if defined PYW set "PYW=%PYW%" & set "PYA=-3"
if not defined PYW for /f "delims=" %%p in ('where pythonw 2^>nul ^| findstr /v /i "WindowsApps"') do if not defined PYW set "PYW=%%p"
if not defined PYW (
  start "Bergama" powershell -NoProfile -Command "$e=[char]27; Write-Host ($e+'[1;31mBERGAMA: Python not found. Run setup.bat once, then try again.'+$e+'[0m'); Read-Host 'Press Enter to close'"
  exit /b 1
)
set "SYNC=%USERPROFILE%\Downloads\Bergama\bergama_shared_sync_v2.py"
if not exist "%SYNC%" set "SYNC=%~dp0bergama_shared_sync_v2.py"
if not exist "%SYNC%" (
  start "Bergama" powershell -NoProfile -Command "$e=[char]27; Write-Host ($e+'[1;31mBERGAMA: bergama_shared_sync_v2.py not found in Downloads\Bergama'+$e+'[0m'); Read-Host 'Press Enter to close'"
  exit /b 1
)
"%PYW%" %PYA% "%SYNC%" %2
exit /b
