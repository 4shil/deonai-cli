@echo off
REM DeonAi CLI Windows Installer
REM Run this script to install DeonAi on Windows

echo.
echo ========================================
echo    DeonAi CLI Windows Installer
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found!
echo.

REM Install dependencies
echo Installing required packages...
pip install requests
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed!
echo.

REM Create a batch file in user's local bin
set "INSTALL_DIR=%USERPROFILE%\AppData\Local\Microsoft\WindowsApps"
set "SCRIPT_PATH=%~dp0deonai.py"
set "BATCH_FILE=%INSTALL_DIR%\deonai.bat"

echo @echo off > "%BATCH_FILE%"
echo python "%SCRIPT_PATH%" %%* >> "%BATCH_FILE%"

echo [OK] DeonAi installed successfully!
echo.
echo ========================================
echo Next steps:
echo   1. Run: deonai --setup
echo   2. Get API key: https://openrouter.ai/keys
echo   3. Start chatting: deonai
echo ========================================
echo.
pause
