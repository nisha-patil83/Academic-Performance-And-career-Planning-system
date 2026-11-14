# PowerShell script to create a Windows Desktop Shortcut for TKIET EduPlan App
$targetPath = "C:\Users\Nisha Patil\.gemini\antigravity\scratch\academic_career_system\launch_desktop_app.bat"
$workingDir = "C:\Users\Nisha Patil\.gemini\antigravity\scratch\academic_career_system"
$desktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")
$shortcutPath = [System.IO.Path]::Combine($desktopPath, "TKIET EduPlan App.lnk")

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $targetPath
$Shortcut.WorkingDirectory = $workingDir
$Shortcut.Description = "TKIET Warananagar EduPlan AI Desktop Application"
$Shortcut.WindowStyle = 7 # Minimized/Silent
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully at: $shortcutPath" -ForegroundColor Green
