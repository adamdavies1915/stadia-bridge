$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$appDir = Join-Path $env:LOCALAPPDATA 'Programs\StadiaBridge'
$runtime = Join-Path $appDir 'runtime'
New-Item -ItemType Directory -Force $appDir | Out-Null
$python = Join-Path $runtime 'python.exe'
if (-not (Test-Path $python)) {
    $installer = Join-Path $env:TEMP 'stadia-python-3.12.10-amd64.exe'
    Invoke-WebRequest 'https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe' -OutFile $installer
    $signature = Get-AuthenticodeSignature $installer
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notlike '*Python Software Foundation*') {
        throw 'Python installer signature verification failed'
    }
    $options = @('/quiet', 'InstallAllUsers=0', "TargetDir=`"$runtime`"", 'PrependPath=0', 'Include_launcher=0', 'AssociateFiles=0', 'Shortcuts=0', 'Include_test=0', 'Include_doc=0', 'Include_pip=1', 'Include_tcltk=1')
    $process = Start-Process $installer -ArgumentList $options -Wait -PassThru
    if ($process.ExitCode -notin @(0,3010)) { throw "Python install failed: $($process.ExitCode)" }
}
$project = Split-Path $PSScriptRoot -Parent
Copy-Item (Join-Path $project 'stadia_bridge') $appDir -Recurse -Force
Copy-Item (Join-Path $project 'run.py') $appDir -Force
Copy-Item (Join-Path $project 'requirements.txt') $appDir -Force
Copy-Item (Join-Path $project 'install_dependencies.py') $appDir -Force
# The driver is a separate prerequisite; never invoke vgamepad setup without it.
if (-not (Get-Service ViGEmBus -ErrorAction SilentlyContinue)) {
    throw 'Install ViGEmBus from https://github.com/nefarius/ViGEmBus/releases/latest then rerun.'
}
& $python (Join-Path $appDir 'install_dependencies.py')
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
& $python -m pip install pyinstaller==6.11.1
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
Write-Output "Installed app and runtime: $appDir"
