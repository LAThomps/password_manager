import os 
import win32com.client as win32 
import sys

# Uses pywin32 to create a shortcut
def main(
        shortcut_path: str, 
        app_dir: str
    ) -> None:
    shell = win32.Dispatch("WScript.shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = os.path.join(app_dir, "startup.bat")
    shortcut.WorkingDirectory = app_dir 
    shortcut.Description = "Password Manager"
    shortcut.save()
    return

if __name__ == "__main__":
    args = sys.argv
    main(args[-2], args[-1])