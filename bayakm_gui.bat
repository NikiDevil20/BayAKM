@echo off
cd /d %~dp0
start "" /B /MIN pythonw -m src.gui.gui
exit