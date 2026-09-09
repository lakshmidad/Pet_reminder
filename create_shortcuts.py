import os
import subprocess

vbs_script = r"c:\Users\mindy\OneDrive\Desktop\Petreminder\start_pet.vbs"
work_dir = r"c:\Users\mindy\OneDrive\Desktop\Petreminder"
appdata = os.environ["APPDATA"]
desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")

startup_lnk = os.path.join(appdata, r"Microsoft\Windows\Start Menu\Programs\Startup\PetReminder.lnk")
desktop_lnk = os.path.join(desktop, "Pet Reminder.lnk")

vbs_creator = f"""
Set WshShell = WScript.CreateObject("WScript.Shell")

Set s1 = WshShell.CreateShortcut("{startup_lnk}")
s1.TargetPath = "wscript.exe"
s1.Arguments = """"{vbs_script}""""
s1.WorkingDirectory = "{work_dir}"
s1.Save

Set s2 = WshShell.CreateShortcut("{desktop_lnk}")
s2.TargetPath = "wscript.exe"
s2.Arguments = """"{vbs_script}""""
s2.WorkingDirectory = "{work_dir}"
s2.Save
"""

creator_path = os.path.join(work_dir, "make_links.vbs")
with open(creator_path, "w", encoding="utf-8") as f:
    f.write(vbs_creator)

subprocess.run(["wscript.exe", creator_path], check=True)
print("Shortcuts created successfully!")
