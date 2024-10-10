# This file is the engine for installing all required files to run the Password Manager App

import os
import shutil
import subprocess
import time

# all files required to run app
APP_FILES = [
    "../json_files/config.json",
    "main.py",
    "../json_files/mgr.json",
    "passmgmt.py",
    "../requirements.txt"
]

# windows .bat script to launch app once installed 
STARTUP_SCRIPT = """
@echo off
call app_venv/Scripts/activate.bat
python main.py
"""

def main():
    print("Welcome to the Password Manager setup wizard\n")

    # app files will be stored in user's personal folder
    prefix = rf"C:\Users\{os.getlogin()}"
    dir_input = input(f"""
    Where would you like to store the app's files? (enter `d` for default)
    (default is `.pw_mgr` and parent directory will be `{prefix}`)  
    """)

    # validate input directory name is workable
    while True:
        if dir_input == "d":
            app_dir = os.path.join(prefix, ".pw_mgr")
        else:
            app_dir = os.path.join(prefix, dir_input)
        try:
            os.mkdir(app_dir)
            break
        except FileNotFoundError:
            dir_input = input(f"""
            `{app_dir}` not a valid directory path
            enter a new path or `d` for the default""")

    # copy files over into new directory
    print("\nbuilding app directory")
    for file in APP_FILES:
        file_only = file.split("/")[-1]
        end_path = os.path.join(app_dir, file_only)
        shutil.copy(file, end_path)

    # do the installs 
    os.chdir(app_dir)
    print("\ninstalling packages")

    # make python venv for the app
    subprocess.check_call("python -m venv app_venv", shell=True)

    # use pip to install required libraries into new venv
    pip_exe = r"app_venv\Scripts\pip"
    subprocess.check_call([pip_exe, "-q", "install", "-r", "requirements.txt"])

    # make .bat file to run app
    with open("startup.bat", "w") as file:
        file.write(STARTUP_SCRIPT)

    ## make desktop shortcut
    shortcut_title = input("\nwhat would you like to name the shortcut to start the app?  ")

    # use pywin32 to make shortcut, save it on desktop
    import win32com.client as win32 

    # depending on version of windows, might have OneDrive folder
    onedrive = os.path.isdir(rf"C:\Users\{os.getlogin()}\OneDrive")
    desktop_path = "Desktop" if not onedrive else r"OneDrive\Desktop"

    # make path
    shortcut_path = os.path.join(
        rf"C:\Users\{os.getlogin()}",
        desktop_path,
        f"{shortcut_title}.lnk"
    )

    # build shortcut to launch startup.bat on click
    shell = win32.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = os.path.join(app_dir, "startup.bat")
    shortcut.WorkingDirectory = app_dir
    shortcut.Description = "Password Manager"
    shortcut.save()

    print(f"\nshortcut saved at {shortcut_path}")
    print("exiting...")
    time.sleep(5)
    return

if __name__ == "__main__":
    main()