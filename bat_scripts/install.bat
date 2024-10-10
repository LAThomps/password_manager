@echo off

:: check if python is on PATH
where python >nul 2>&1

:: run install if successful
if %errorlevel%==0 (
    cd ..
    install_venv\Scripts\python py_scripts\install.py 
) else (
    echo python not found on system PATH 
    echo if you have not installed python, please install before next attempt
    echo.
    echo if you have python installed, but it is not on PATH, then just run 
    echo the below command from this directory
    echo.
    echo <path_to_your_python.exe> install.py
)

pause