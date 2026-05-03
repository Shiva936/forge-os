<#.SYNOPSIS
  Create repository .venv and install requirements-forge.txt (Forge Python runtime).
.DESCRIPTION
  Run from any directory. Default: create .venv if missing, then pip install -r.
  -Force: remove existing .venv first (clean recreate).
#>
param(
  [switch] $Force
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
Set-Location $RepoRoot

if ($Force -and (Test-Path .venv)) {
  Remove-Item -Recurse -Force .venv
}

if (-not (Test-Path .venv)) {
  if (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 -m venv .venv
  } elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python -m venv .venv
  } else {
    Write-Error 'Could not create venv: install Python 3 and ensure `py -3` or `python` is on PATH.'
  }
  if (-not (Test-Path .venv)) {
    Write-Error 'venv creation failed.'
  }
}

$pip = Join-Path $RepoRoot '.venv\Scripts\pip.exe'
$python = Join-Path $RepoRoot '.venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
  Write-Error ".venv is missing python.exe at $python"
}

& $python -m pip install --upgrade pip
& $pip install -r (Join-Path $RepoRoot 'requirements-forge.txt')

Write-Host "Forge venv ready: $python"
