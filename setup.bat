@echo off
setlocal
cd /d "%~dp0"
py -3.12 -m venv .venv
if errorlevel 1 goto failed
.venv\Scripts\python.exe install_dependencies.py
if errorlevel 1 goto failed
echo Setup complete. Run start.bat to open Stadia Bridge.
pause
exit /b 0
:failed
echo Setup failed. Install Python 3.12 x64 from python.org and check your internet connection.
pause
exit /b 1
