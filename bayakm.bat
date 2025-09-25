@echo off
cd /d %~dp0
start "" /B /MIN pythonw -m src.gui.main_gui.gui
exit