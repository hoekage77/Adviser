@echo off

REM Stop on errors
setlocal enabledelayedexpansion

REM Create virtual environment using Python 3.12
python -m venv env
if %errorlevel% neq 0 (
    echo Error creating virtual environment
    exit /b %errorlevel%
)

REM Activate the virtual environment (Command Prompt version)
call env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error activating virtual environment
    exit /b %errorlevel%
)

REM Install Python dependencies from requirements.txt
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing Python dependencies from requirements.txt
    exit /b %errorlevel%
)

REM Install the current package in editable mode
pip install -e .
if %errorlevel% neq 0 (
    echo Error installing package in editable mode
    exit /b %errorlevel%
)

REM Install npm dependencies
npm ci
if %errorlevel% neq 0 (
    echo Error running npm ci
    exit /b %errorlevel%
)

echo All tasks completed successfully!
