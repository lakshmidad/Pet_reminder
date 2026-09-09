Set WshShell = CreateObject("WScript.Shell")
' Run pythonw in background without opening any black command prompt window
WshShell.CurrentDirectory = "c:\Users\mindy\OneDrive\Desktop\Petreminder"
WshShell.Run "pythonw main.py", 0, False
