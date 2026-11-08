@echo off
rem Bergama Group 6 - shared masterplan (8 Nov 2026). Double-click, press 1, 2 or 3.
rem 1 Rhino / 2 Illustrator / 3 AutoCAD: upload your edits, download all, merge, open the latest file in that app.
rem Works from any folder (Desktop too). Needs: setup.bat run once (system Python), Data\shared_settings.txt (token=..., me=...).
if "%~1"=="__run" goto run
title Bergama
echo.
echo    BERGAMA - shared masterplan
echo.
echo    1  Rhino
echo    2  Illustrator
echo    3  AutoCAD
echo.
choice /c 123 /n /m "   Press 1, 2 or 3: "
set "APP="
if errorlevel 3 set "APP=autocad" & goto go
if errorlevel 2 set "APP=illustrator" & goto go
if errorlevel 1 set "APP=rhino" & goto go
exit /b
:go
powershell -NoProfile -WindowStyle Hidden -Command "Start-Process -WindowStyle Hidden -FilePath $env:ComSpec -ArgumentList '/c','\"%~f0\" __run %APP%'"
exit

:run
rem ---- hidden from here: find the system Python (setup.bat), run Downloads\Bergama\bergama_shared_sync_v1.py ----
set "PYW="
set "PYA="
for /f "delims=" %%p in ('where pyw 2^>nul') do if not defined PYW set "PYW=%%p"
if defined PYW set "PYW=%PYW%" & set "PYA=-3"
if not defined PYW for /f "delims=" %%p in ('where pythonw 2^>nul ^| findstr /v /i "WindowsApps"') do if not defined PYW set "PYW=%%p"
if not defined PYW (
  powershell -NoProfile -Command "$e=[char]27; Write-Host ($e+'[1;31mBERGAMA: Python not found. Run setup.bat once, then try again.'+$e+'[0m'); Read-Host 'Press Enter to close'"
  exit /b 1
)
set "SYNC=%USERPROFILE%\Downloads\Bergama\bergama_shared_sync_v1.py"
if not exist "%SYNC%" set "SYNC=%~dp0bergama_shared_sync_v1.py"
if not exist "%SYNC%" (
  powershell -NoProfile -Command "$e=[char]27; Write-Host ($e+'[1;31mBERGAMA: bergama_shared_sync_v1.py not found in Downloads\Bergama'+$e+'[0m'); Read-Host 'Press Enter to close'"
  exit /b 1
)
"%PYW%" %PYA% "%SYNC%" %2
exit /b
