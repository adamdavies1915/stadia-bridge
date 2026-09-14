@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe goto failed
.venv\Scripts\python.exe -m pip install pyinstaller==6.11.1
if errorlevel 1 goto failed
.venv\Scripts\python.exe scripts\build_windows.py
if errorlevel 1 goto failed
echo Built dist\single\StadiaBridge.exe and the portable dist\StadiaBridge folder.
exit /b 0
:failed
echo Build failed. Run setup.bat first and review the error above.
exit /b 1
