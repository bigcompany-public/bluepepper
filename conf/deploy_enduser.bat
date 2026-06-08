@echo off

SET BLUEPEPPER_GIT_URL=
SET BLUEPEPPER_GIT_PAT=

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ^
"$ErrorActionPreference='Stop'; ^
if(-Not $env:BLUEPEPPER_GIT_URL){throw 'Please set the BLUEPEPPER_GIT_URL environment variable to you repository url'}; ^
if(-Not $env:BLUEPEPPER_GIT_PAT){throw 'Please set the BLUEPEPPER_GIT_PAT environment variable to the Personal Access Token to connect with'}; ^
$protocol, $_, $website, $user, $repo = $env:BLUEPEPPER_GIT_URL.split('/'); ^
$full_url = $protocol + '//' + $env:BLUEPEPPER_GIT_PAT+ '@' + $website + '/' + $user + '/' + $repo; ^
git clone $full_url; ^
$folder = $repo.split('.')[0]; ^
& ('./' + $folder + '/install_enduser.ps1'); ^
Write-Output 'Installation was successful'"

pause