Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
' Run pythonw in background without opening any black command prompt window
WshShell.CurrentDirectory = scriptDir
WshShell.Run "pythonw main.py", 0, False
