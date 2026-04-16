$ErrorActionPreference = "Stop"

# Create file that indicates this repository must not be updated
$editable_mode_file = Join-Path -Path $PSScriptRoot -ChildPath ".editable_mode"
if (-Not (Test-Path $editable_mode_file)) {
    Write-Output "Creating editable mode file : $editable_mode_file"
    New-Item $editable_mode_file -type file | Out-Null
}

# Install virtual environment & dependencies
$install_script = Join-Path -Path $PSScriptRoot -ChildPath "install/install.py"
& python $install_script --reset --update_packages

if ($LASTEXITCODE -ne 0) {
    throw "Python installation script failed with exit code $LASTEXITCODE"
}