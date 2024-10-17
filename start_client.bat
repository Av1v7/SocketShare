@echo off
cd /d %~dp0

title Checking Python installation...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! (Go to https://www.python.org/downloads and install the latest version.^)
    echo Make sure it is added to PATH.
    goto ERROR
)

title Checking libraries...
echo Checking 'tkinter' (1/3)
python -c "import tkinter" > nul 2>&1
if %errorlevel% neq 0 (
    echo Tkinter should be included with Python, no need to install separately.
)

echo Checking 'socket' (2/3)
python -c "import socket" > nul 2>&1
if %errorlevel% neq 0 (
    echo Socket should be included with Python, no need to install separately.
)

echo Checking 'json' (3/3)
python -c "import json" > nul 2>&1
if %errorlevel% neq 0 (
    echo JSON should be included with Python, no need to install separately.
)

cls
title Running the SocketShare application...
python main.py
if %errorlevel% neq 0 goto ERROR
exit

:ERROR
color 4 && title [Error]
pause > nul
