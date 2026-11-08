@echo off
rem Bergama Group 6 - setup.bat (8 Nov 2026): run once per PC.
rem Step 1 saves your GitHub settings (who you are + the token) in Downloads\Bergama\Data\shared_settings.txt.
rem Step 2 installs system-wide Python 3.13.17 (all users, on PATH) for Bergama.bat. Uses winget (built into Windows 10/11);
rem without winget it downloads the official python.org installer and checks its SHA-256 (python.org release page) first.
setlocal
title Bergama setup
if "%~1"=="__py" goto py
echo.
echo    BERGAMA SETUP  1/2  GitHub settings
echo.
powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((Get-Content -LiteralPath '%~f0' -Raw) -split ('#'+'POWERSHELL_PART'))[1]"
echo.
echo    BERGAMA SETUP  2/2  Python
set "PYV="
for /f "delims=" %%v in ('py -3 --version 2^>nul') do set "PYV=%%v"
if defined PYV (
  echo.
  echo    Python is already installed: %PYV%. Nothing to do.
  echo.
  pause
  exit /b 0
)
echo    Asking Windows for admin rights to install Python ...
powershell -NoProfile -Command "Start-Process -Verb RunAs -FilePath '%~f0' -ArgumentList '__py'"
exit /b

:py
echo.
echo    Installing Python 3.13.17 for all users ...
where winget >nul 2>&1
if not errorlevel 1 (
  winget install -e --id Python.Python.3.13 --version 3.13.17 --scope machine --source winget --silent --accept-package-agreements --accept-source-agreements
  if not errorlevel 1 goto check
  echo    winget did not finish: trying the python.org installer ...
)
set "URL=https://www.python.org/ftp/python/3.13.17/python-3.13.17-amd64.exe"
set "SHA=5DA012101BA2E17113A9A1CD901E9CE1441086F2B7ECB5DE06EC94163899A190"
set "EXE=%TEMP%\python-3.13.17-amd64.exe"
powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%URL%' -OutFile '%EXE%'; if ((Get-FileHash '%EXE%' -Algorithm SHA256).Hash -ne '%SHA%') { Remove-Item '%EXE%'; exit 1 }"
if errorlevel 1 (
  powershell -NoProfile -Command "$e=[char]27; Write-Host ($e+'[1;31m   The download failed or its checksum did not match python.org: nothing was installed.'+$e+'[0m')"
  pause
  exit /b 1
)
"%EXE%" /quiet InstallAllUsers=1 PrependPath=1 Include_launcher=1 InstallLauncherAllUsers=1 Include_test=0
del "%EXE%" >nul 2>&1
:check
set "PYV="
for /f "delims=" %%v in ('"%SystemRoot%\py.exe" -3 --version 2^>nul') do set "PYV=%%v"
echo.
if defined PYV (
  echo    Done: %PYV% is installed. You can now use Bergama.bat.
) else (
  powershell -NoProfile -Command "$e=[char]27; Write-Host ($e+'[1;31m   Python was not found after the install. Restart the PC and run setup.bat again.'+$e+'[0m')"
)
echo.
pause
exit /b

#POWERSHELL_PART
& {
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$e = [char]27
$f = Join-Path $env:USERPROFILE 'Downloads\Bergama\Data\shared_settings.txt'
$repo = 'SupFlyn/BergamaProjectScripts'
$old = [ordered]@{}
if (Test-Path -LiteralPath $f) {
  foreach ($l in Get-Content -LiteralPath $f -Encoding UTF8) { if ($l -match '^\s*([^=]+?)\s*=\s*(.*)$') { $old[$matches[1].ToLower()] = $matches[2].Trim() } }
}
if ($old['token'] -and $old['me']) {
  Write-Host "   Already saved for '$($old['me'])'. To change it, delete $f and run setup.bat again."
  return
}
Write-Host '   Who are you?   1 aras    2 begum    3 nil'
do { $k = [string][Console]::ReadKey($true).KeyChar } until ('123'.Contains($k) -and $k)
$me = @('aras', 'begum', 'nil')[[int]$k - 1]
Write-Host "   -> $me"
Write-Host ''
Write-Host '   GitHub token:   1 I have the token Aras sent me    2 make a new token (Aras only, on his GitHub account)'
do { $k = [string][Console]::ReadKey($true).KeyChar } until ('12'.Contains($k) -and $k)
if ($k -eq '2') {
  Start-Process 'https://github.com/settings/personal-access-tokens/new?name=Bergama+shared&description=Bergama+shared+masterplan+sync&target_name=SupFlyn&expires_in=366&contents=write'
  Write-Host ''
  Write-Host '   The GitHub page "New fine-grained personal access token" is open in your browser (sign in if asked).'
  Write-Host '   Check or fill in:   Token name: Bergama shared     Expiration: 366 days (or the longest offered)'
  Write-Host '                       Resource owner: SupFlyn        Repository access: Only select repositories > BergamaProjectScripts'
  Write-Host '                       Permissions > Repository > Contents: Read and write'
  Write-Host '   Press "Generate token", copy it, then paste it below. Send it to Begum and Nil privately (not in a chat with Claude).'
}
while ($true) {
  Write-Host ''
  $s = Read-Host '   Paste the token here (Ctrl+V or right-click; it stays hidden) and press Enter' -AsSecureString
  $t = [Runtime.InteropServices.Marshal]::PtrToStringBSTR([Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)).Trim()
  if (-not $t) { continue }
  try {
    $null = Invoke-RestMethod -Uri "https://api.github.com/repos/$repo" -Headers @{ Authorization = "Bearer $t" } -UserAgent 'bergama-setup'
    break
  } catch {
    Write-Host ($e + '[1;31m   That token does not open ' + $repo + ': ' + $_.Exception.Message + ' Try again.' + $e + '[0m')
  }
}
$old['token'] = $t
$old['me'] = $me
$null = New-Item -ItemType Directory -Force -Path (Split-Path $f)
$lines = @("token=$t", "me=$me") + @($old.Keys | Where-Object { $_ -ne 'token' -and $_ -ne 'me' } | ForEach-Object { "$_=$($old[$_])" })
[IO.File]::WriteAllLines($f, [string[]]$lines)
Write-Host ($e + '[1;32m   Saved: ' + $f + ' (me=' + $me + '). The token works with ' + $repo + '.' + $e + '[0m')
}
