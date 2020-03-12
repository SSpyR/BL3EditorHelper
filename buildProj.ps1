# buildProj.ps1

$vnum = read-host "What is the version number (x.x.x)?"

rmdir -Recurse .\__pycache__ -erroraction ignore
rmdir -Recurse .\build -erroraction ignore
rmdir -Recurse .\dist -erroraction ignore
del BL3EditorHelper.spec -erroraction ignore

pyinstaller -y --add-data="C:\Users\lavoiet2\Downloads\Coding\BL3EditorHelper\assets;." --add-data="FilesNaming.txt;." .\partcheck.py

#Open PowerShell as Admin, cd C:\Users\lavoiet2\Downloads\Coding\BL3EditorHelper, .\buildProj.ps1
# (powershell -ExecutionPolicy ByPass -File buildProj.ps1) <- this if not signed


$configstring = @"
;!@Install@!UTF-8!
Title=`"BL3EditorHelper v$($vnum)`"
BeginPrompt="Do you want to install BL3EditorHelper?"
RunProgram="setup.bat"
InstallPath="C:\Program Files\BL3EditorHelper"
MiscFlags="4"
;!@InstallEnd@!
"@
$setupstring = @'
copy "%~dp0BL3EditorHelper.lnk" "%USERPROFILE%\Desktop"
copy "%~dp0BL3EditorHelper.lnk" "C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
ICACLS "C:\Program Files\BL3EditorHelper" /grant Everyone:"(OI)(CI)(F)"
'@


echo $setupstring | out-file -encoding ascii $PSScriptRoot\dist\partcheck\setup.bat
cp $PSScriptRoot\BL3EditorHelper.lnk $PSScriptRoot\dist\partcheck\BL3EditorHelper.lnk


echo $configstring | out-file -encoding ascii $PSScriptRoot\config.txt


7z a -r $PSScriptRoot\installer.7z $PSScriptRoot\dist\partcheck\*

cmd.exe /c copy /b 7zsd_All.sfx+config.txt+installer.7z BL3EditorHelperInstall.exe


rm installer.7z
rm config.txt
rmdir -Recurse .\__pycache__
rmdir -Recurse .\build
rmdir -Recurse .\dist
# Get-ChildItem .\dist -Recurse | Remove-Item -Recurse -Force   #Necessary because even rmdir recurse isn't recursing
del .\partcheck.spec
pause