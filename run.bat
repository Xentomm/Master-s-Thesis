@echo off
rem Activate virtual environment
call .env\Scripts\activate.bat

rem Run Python script
python data_application\src\main.py

rem Deactivate virtual environment (optional)
deactivate
