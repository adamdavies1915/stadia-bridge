@echo off
setlocal
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe goto failed
.venv\Scripts\python.exe -m pip install pyinstaller==6.11.1
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onedir --windowed --name StadiaBridge --collect-all vgamepad --hidden-import pygame._sdl2.controller run.py
if errorlevel 1 goto failed
echo Built dist\StadiaBridge\StadiaBridge.exe. Distribute the whole StadiaBridge folder.
exit /b 0
:failed
echo Build failed. Run setup.bat first and review the error above.
exit /b 1
