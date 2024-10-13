# password_manager
An app to securely manage your passwords, written in python for Windows.<br>

You will need python installed on your computer to use this app, and I've only built it for use on the `Windows OS` at<br>
this time (if anyone would like a macOS/Linux version just let me know)

To download/install this app, simply download this repo and run the `install.bat` file located in `bat_scripts` <b>from</b><br>
the `bat_scripts` directory.

If you run into problems running the `install.bat` file, just run the `install.py` file with your desired python<br>
executable (only base libraries are used on install).

The security of this app is based on the system access persmissions to your `C:\Users\<your username>` directory, if<br>
you want to build an extra layer of security, move the .key file to a more secure location <b>and</b> update the app's<br>
`meta.json` file with the absolute path to the new .key location.

If you have a newer version of windows, the shortcut to start this app will be saved under<br>
`C:\Users\<your username>\OneDrive\Desktop`, if you don't use the `OneDrive` location as your normal Desktop, just<br>
copy and paste the shortcut from your `OneDrive` folder to your actual Desktop<br>
(the shortcut link will still work as usual).
