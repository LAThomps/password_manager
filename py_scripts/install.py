# This file is the engine for installing all required files to run the Password Manager App

import os
import shutil
import subprocess
import time

# all files required to run app
APP_FILES = [
    "json_files/config.json",
    "py_scripts/main.py",
    "json_files/mgr.json",
    "py_scripts/passmgmt.py",
    "requirements.txt",
    "py_scripts/make_shortcut.py"
]

# windows .bat script to launch app once installed 
STARTUP_SCRIPT = r"""
@echo off
app_venv\Scripts\python main.py
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
        if os.path.isdir(app_dir):
            dir_input = input(f"directory `{app_dir}` already exists, please choose another name:  ")
        else:
            try:
                os.mkdir(app_dir)
                break
            except:
                dir_input = input(f"""
                `{app_dir}` not a valid directory path
                enter a new path or `d` for the default  """)

    # copy files over into new directory
    print("\nbuilding app directory")
    for file in APP_FILES:
        file_only = file.split("/")[-1]
        end_path = os.path.join(app_dir, file_only)
        shutil.copy(file, end_path)

    # do the installs 
    os.chdir(app_dir)
    print("\ninstalling packages")

    # error check for running subprocess
    try:
        # make python venv for the app
        subprocess.check_call("python -m venv app_venv", shell=True)

        # use pip to install required libraries into new venv
        pip_exe = r"app_venv\Scripts\pip"
        subprocess.check_call([pip_exe, "-q", "install", "-r", "requirements.txt"])

        # make .bat file to run app
        with open("startup.bat", "w") as file:
            file.write(STARTUP_SCRIPT)

        # make desktop shortcut
        while True:
            # file title
            shortcut_title = input("\nwhat would you like to name the shortcut to start the app?  ")

            # depending on version of windows, might have OneDrive folder
            onedrive = os.path.isdir(rf"C:\Users\{os.getlogin()}\OneDrive")
            desktop_path = "Desktop" if not onedrive else r"OneDrive\Desktop"

            # make path
            shortcut_path = os.path.join(
                rf"C:\Users\{os.getlogin()}",
                desktop_path,
                f"{shortcut_title}.lnk"
            )
            
            # don't let user try and make a new file with a taken name
            if os.path.isfile(shortcut_path):
                print(f"file already located at {shortcut_path}, choose a different name")
            else:
                # build shortcut to launch startup.bat on click
                subprocess.check_call(
                    [
                        "app_venv/Scripts/python", 
                        "make_shortcut.py", 
                        shortcut_path, 
                        app_dir
                    ]
                )
                break

        print(f"\nshortcut saved at {shortcut_path}")
        print("exiting...")
        time.sleep(5)
    except:
        print("\nexperienced error attempting to build app environment")
        print("ensure you are running this install from a User account with")
        print("admin privileges and that your anti-virus software permits")
        print("subprocess calls from within python scripts")
        time.sleep(20)
        print("exiting...")
    return

if __name__ == "__main__":
    main()