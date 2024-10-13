# password_manager
An app to securely manage your passwords, written in python for Windows.<br>

You will need python installed on your computer to use this app, and I've only built it<br>
for use on the `Windows OS` at this time (if anyone would like a macOS/Linux version just<br>
let me know)

To download/install this app, simply clone the this repo and run the `install.bat`<br>
file located in `bat_scripts` <b>from</b> the `bat_scripts` directory.

If you run into problems running the `install.bat` file, just run the `install.py`<br>
file with your desired python executable (only base libraries are used on install).

The security of this app is based on the system access persmissions to your<br>
`C:\Users\<your username>` directory, if you want to build an extra layer of<br>
security, move the .key file to a more secure location <b>and</b> update the app's<br>
`meta.json` file with the absolute path to the new .key location.

If you have a newer version of windows, the shortcut to start this app will be saved<br>
under `C:\Users\<your username>\OneDrive\Desktop`, if you don't use the `OneDrive`<br>
location as your normal Desktop, just copy and paste the shortcut from your `OneDrive`<br>
folder to your actual Desktop (the shortcut link will still work as usual).
