# ==============================================================================
# Damei Suite - One-Click REAPER Deployment Script
# Deploys JSFX Suites to %APPDATA%\REAPER\Effects\Damei
# Deploys Lua ReaScripts to %APPDATA%\REAPER\Scripts\Damei
# ==============================================================================

[CmdletBinding()]
param(
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "      DAMEI AUDIO SUITE - REAPER INSTALLER               " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

$appData = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::ApplicationData)
$reaperDir = Join-Path $appData "REAPER"

if (-not (Test-Path $reaperDir)) {
    Write-Error "REAPER directory not found at '$reaperDir'. Please verify REAPER is installed."
    return
}

$effectsDst = Join-Path $reaperDir "Effects\Damei"
$scriptsDst = Join-Path $reaperDir "Scripts\Damei"

New-Item -ItemType Directory -Force -Path $effectsDst | Out-Null
New-Item -ItemType Directory -Force -Path $scriptsDst | Out-Null

$scriptRoot = $PSScriptRoot
if (-not $scriptRoot) { $scriptRoot = Get-Location }

$effectsSrc = Join-Path $scriptRoot "effects"
$scriptsSrc = Join-Path $scriptRoot "scripts"

Write-Host "`n[1/2] Installing JSFX Effects..." -ForegroundColor Yellow
$effects = @(Get-ChildItem -Path $effectsSrc -Filter "*.jsfx") + @(Get-ChildItem -Path $effectsSrc -Filter "*.jsfx-inc")
foreach ($fx in $effects) {
    $target = Join-Path $effectsDst $fx.Name
    Copy-Item -Path $fx.FullName -Destination $target -Force
    Write-Host "  -> Installed: $($fx.Name)" -ForegroundColor Green
}

Write-Host "`n[2/2] Installing Lua ReaScripts..." -ForegroundColor Yellow
$scripts = Get-ChildItem -Path $scriptsSrc -Filter "*.lua"
foreach ($s in $scripts) {
    $target = Join-Path $scriptsDst $s.Name
    Copy-Item -Path $s.FullName -Destination $target -Force
    Write-Host "  -> Installed: $($s.Name)" -ForegroundColor Green
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host "  INSTALLATION COMPLETE!                                  " -ForegroundColor Green
Write-Host "  In REAPER, press F5 in the FX Browser to reload JSFX,  " -ForegroundColor Cyan
Write-Host "  or open the Action List (Shift+?) and load scripts.     " -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
