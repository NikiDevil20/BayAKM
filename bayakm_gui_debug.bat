@echo off
cd /d %~dp0

call "%~dp0.venv/Scripts/activate.bat"

python -m src.gui.main.gui
pause