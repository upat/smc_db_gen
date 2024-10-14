@echo off
setlocal

cd /d %~dp0
py main.py "%~1"

endlocal
pause
