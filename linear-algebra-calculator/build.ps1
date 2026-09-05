param(
    [string]$Python = (Join-Path $PSScriptRoot '..\.venv\Scripts\python.exe')
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Python)) {
    throw "Python not found at $Python. Create .venv first, or pass -Python with your Python executable path."
}

$buildDirectory = Join-Path $PSScriptRoot 'build'
$distDirectory = Join-Path $PSScriptRoot 'dist'
$previousCache = $env:PYINSTALLER_CONFIG_DIR
try {
    $env:PYINSTALLER_CONFIG_DIR = Join-Path $buildDirectory 'cache'
    & $Python -B -m PyInstaller `
        --noconfirm `
        --onefile `
        --windowed `
        --name 'Linear Algebra Calculator' `
        --paths $PSScriptRoot `
        --specpath $buildDirectory `
        --workpath (Join-Path $buildDirectory 'work') `
        --distpath $distDirectory `
        (Join-Path $PSScriptRoot 'app\main.py')
    if ($LASTEXITCODE -ne 0) {
        throw 'Build failed. Install build-requirements.txt with this Python environment and retry.'
    }
    Write-Host "App ready: $(Join-Path $distDirectory 'Linear Algebra Calculator.exe')"
}
finally {
    $env:PYINSTALLER_CONFIG_DIR = $previousCache
}
