@echo off

REM Stop on errors
setlocal enabledelayedexpansion
set -e
set -x

REM Use Python virtual environment in Windows
python -m venv env

REM Activate the virtual environment (Command Prompt version)
call env\Scripts\activate.bat

REM Install Python dependencies
pip install -r requirements.txt
pip install -e .

REM Install npm dependencies
npm ci
