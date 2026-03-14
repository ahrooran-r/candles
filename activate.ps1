# Ensure script runs from the project root
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

$venvDir = ".venv"
$activateScript = Join-Path $venvDir "Scripts\Activate.ps1"

# Create venv if missing
if (!(Test-Path $venvDir)) {
    Write-Host "Creating virtual environment (.venv)..."
    uv venv
}

# Verify activation script exists
if (!(Test-Path $activateScript)) {
    Write-Error "Activation script not found: $activateScript"
    exit 1
}

# Activate environment
Write-Host "Activating virtual environment..."
. $activateScript

# Install dependencies if lock file exists
if (Test-Path "uv.lock") {
    Write-Host "Syncing dependencies from uv.lock..."
    uv sync
}
else {
    Write-Host "No uv.lock found. Skipping dependency sync."
}