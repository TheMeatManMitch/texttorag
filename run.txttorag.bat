@echo off
REM Navigate to the directory where your script is located 
cd /d %~dp0

REM Activate the virtual environment
call .venv\Scripts\activate

REM Run the Python script
python TexttoRAG.py

REM Deactivate the virtual environment after running
deactivate