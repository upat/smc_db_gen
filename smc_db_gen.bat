@echo off
setlocal

cd /d %~dp0
py smc_db_gen.py "%~1"

endlocal
pause
