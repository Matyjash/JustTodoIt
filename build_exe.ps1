# Run this script to generate the .exe file using PyInstaller

param(
    [switch]$WithIcon = $true
)

$pyinstaller = pip show pyinstaller
if (-not $pyinstaller) {
    Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
    pip install pyinstaller
}

Write-Host "Building JustTodoIt executable..." -ForegroundColor Cyan

$buildCmd = "pyinstaller --onefile --windowed --name=JustTodoIt --add-data='data;data' app.py"

if ($WithIcon -and (Test-Path "data/icons/app.ico")) {
    $buildCmd += " --icon=data/icons/app.ico"
    Write-Host "Using custom icon..." -ForegroundColor Green
}

Invoke-Expression $buildCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build successful! Executable located at: dist/JustTodoIt.exe" -ForegroundColor Green
} else {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}
