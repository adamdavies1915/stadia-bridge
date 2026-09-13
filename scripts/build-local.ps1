$ErrorActionPreference = 'Stop'
$app = Join-Path $env:LOCALAPPDATA 'Programs\StadiaBridge'
$project = Split-Path $PSScriptRoot -Parent
Copy-Item (Join-Path $project 'stadia_bridge') $app -Recurse -Force
Copy-Item (Join-Path $project 'run.py') $app -Force
Set-Location $app
& "$app\runtime\python.exe" -m unittest discover -s (Join-Path $project 'tests') -v
if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }
& "$app\runtime\python.exe" -m PyInstaller --noconfirm --clean --onedir --windowed --name StadiaBridge --collect-all vgamepad --hidden-import pygame._sdl2.controller run.py
if ($LASTEXITCODE -ne 0) { throw 'Windows executable build failed' }
$exe = Join-Path $app 'dist\StadiaBridge\StadiaBridge.exe'
$shell = New-Object -ComObject WScript.Shell
foreach ($folder in @([Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('Programs'))) {
    $shortcut = $shell.CreateShortcut((Join-Path $folder 'Stadia Bridge.lnk'))
    $shortcut.TargetPath = $exe
    $shortcut.WorkingDirectory = Split-Path $exe
    $shortcut.Description = 'Use your Stadia controller as an Xbox controller'
    $shortcut.Save()
}
Write-Output "Built executable and shortcuts: $exe"
