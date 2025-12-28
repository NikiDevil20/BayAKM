@echo off
cd /d "%~dp0"

call "%~dp0.venv\Scripts\activate.bat"
start "" /B /MIN pythonw -m src.gui.main_gui.gui
exit