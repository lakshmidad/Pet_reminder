Set WshShell = WScript.CreateObject("WScript.Shell")

vbsScript = "c:\Users\mindy\OneDrive\Desktop\Petreminder\start_pet.vbs"
workDir = "c:\Users\mindy\OneDrive\Desktop\Petreminder"
appData = WshShell.ExpandEnvironmentStrings("%APPDATA%")

startupLnk = appData & "\Microsoft\Windows\Start Menu\Programs\Startup\PetReminder.lnk"
desktopLnk = "C:\Users\mindy\OneDrive\Desktop\Pet Reminder.lnk"

Set s1 = WshShell.CreateShortcut(startupLnk)
s1.TargetPath = "wscript.exe"
s1.Arguments = """" & vbsScript & """"
s1.WorkingDirectory = workDir
s1.Save

Set s2 = WshShell.CreateShortcut(desktopLnk)
s2.TargetPath = "wscript.exe"
s2.Arguments = """" & vbsScript & """"
s2.WorkingDirectory = workDir
s2.Save

WScript.Echo "Shortcuts created successfully!"
