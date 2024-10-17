@echo off

REM Stop on errors
setlocal enabledelayedexpansion
set -e
set -x

REM Run webpack in watch mode in the background
start npx webpack --watch

REM Run Flask app on port 8001 with debugging enabled
flask --app collage --debug run --host 0.0.0.0 --port 8001
