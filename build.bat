@echo off
REM Arc Raiders Config Tuner - Build Script for Windows
REM This script builds a standalone .exe that requires no Python installation

echo ============================================
echo Arc Raiders Config Tuner - Build Script
echo ============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check/Install PyInstaller
echo Checking for PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "*.spec" del /q *.spec

REM Build the executable
echo.
echo Building Arc Tuner...
echo.

REM Use python -m PyInstaller to avoid PATH issues
set PYINSTALLER_OPTS=--onefile --windowed --name "ArcRaidersTuner"

REM Add icon if it exists
if exist "icon.ico" set PYINSTALLER_OPTS=%PYINSTALLER_OPTS% --icon "icon.ico"

python -m PyInstaller %PYINSTALLER_OPTS% arc_tuner.py

if errorlevel 1 (
    echo.
    echo BUILD FAILED!
    pause
    exit /b 1
)

echo.
echo ============================================
echo BUILD SUCCESSFUL!
echo ============================================
echo.
echo The executable is located at:
echo   dist\ArcRaidersTuner.exe
echo.
echo You can distribute this single .exe file.
echo No Python or other dependencies required!
echo.
pause
