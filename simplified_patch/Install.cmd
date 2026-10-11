@echo off
setlocal
cd /d "%~dp0"
python --version >nul 2>&1
if not errorlevel 1 (
    python "install.py"
    goto done
)
py -3 --version >nul 2>&1
if not errorlevel 1 (
    py -3 "install.py"
    goto done
)
echo Python 3.10 or newer is required. Please install Python and try again.
:done
pause
