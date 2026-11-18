# Bergama UE5 render launcher (18 Nov 2026), called by run_ue5_render.bat (keep both in the same folder).
# Pick the Archicad FBX; UE 5.8 opens the project and runs the newest Downloads\Bergama\scripts\bergama_ue5_render_v*.py.
# Asked once and kept in cached\bergama_ue5: the .uproject, and UnrealEditor.exe when not in C:\Program Files\Epic Games\UE_5.8*.
Add-Type -AssemblyName System.Windows.Forms
$bg = Join-Path $env:USERPROFILE 'Downloads\Bergama'
$cu = Join-Path $bg 'cached\bergama_ue5'
New-Item -ItemType Directory -Force -Path $cu | Out-Null
function Pick($title, $filter, $dir) {
    $o = New-Object System.Windows.Forms.OpenFileDialog
    $o.Title = $title; $o.Filter = $filter
    if ($dir -and (Test-Path $dir)) { $o.InitialDirectory = $dir }
    if ($o.ShowDialog() -ne 'OK') { Write-Host 'Cancelled.'; exit 1 }
    return $o.FileName
}
$fbx = Pick 'Pick the Archicad FBX of the model' 'FBX (*.fbx)|*.fbx' (Join-Path $bg 'archicad')
Set-Content -Encoding UTF8 (Join-Path $cu 'fbx_path.txt') $fbx
$pf = Join-Path $cu 'uproject.txt'; $up = $null
if (Test-Path $pf) { $up = (Get-Content $pf -Raw).Trim() }
if (-not $up -or -not (Test-Path $up)) {
    $up = Pick 'Pick your Unreal project (.uproject) - asked once' 'Unreal project (*.uproject)|*.uproject' ([Environment]::GetFolderPath('MyDocuments'))
    Set-Content -Encoding UTF8 $pf $up
}
$ef = Join-Path $cu 'editor.txt'; $ed = $null
if (Test-Path $ef) { $ed = (Get-Content $ef -Raw).Trim() }
if (-not $ed -or -not (Test-Path $ed)) {
    $ed = Get-ChildItem 'C:\Program Files\Epic Games\UE_5.8*\Engine\Binaries\Win64\UnrealEditor.exe' -ErrorAction SilentlyContinue |
          Select-Object -First 1 -ExpandProperty FullName
}
if (-not $ed) { $ed = Pick 'Pick UnrealEditor.exe (UE 5.8) - asked once' 'UnrealEditor.exe|UnrealEditor.exe' 'C:\Program Files\Epic Games' }
Set-Content -Encoding UTF8 $ef $ed
$py = Get-ChildItem (Join-Path $bg 'scripts\bergama_ue5_render_v*.py') -ErrorAction SilentlyContinue |
      Sort-Object LastWriteTime | Select-Object -Last 1 -ExpandProperty FullName
if (-not $py) { Write-Host 'No bergama_ue5_render_v*.py in Downloads\Bergama\scripts.'; exit 1 }
Write-Host "FBX     $fbx"
Write-Host "Project $up"
Write-Host "Editor  $ed"
Write-Host "Script  $py"
Start-Process -FilePath $ed -ArgumentList "`"$up`"", "-ExecutePythonScript=`"$py`""
Write-Host "UE is starting; the renders run inside the editor. Log: $bg\logs\bergama_ue5_log.txt"
