@echo off
title Retail Store DBMS - Database Setup and Initialization
color 0B

echo ===============================================================================
echo   RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - DATABASE SETUP
echo   Course: 25ITT31 - Database Management Systems (VCET R2025)
echo   Register No: 9, 39, 69, 99
echo ===============================================================================
echo.

cd /d "%~dp0\.."

REM Resolve Python Executable
if exist "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe" (
    set "PYTHON_EXE=C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python312\python.exe"
) else if exist "C:\Program Files\Python312\python.exe" (
    set "PYTHON_EXE=C:\Program Files\Python312\python.exe"
) else if exist "C:\Python312\python.exe" (
    set "PYTHON_EXE=C:\Python312\python.exe"
) else (
    set "PYTHON_EXE=python"
)

echo [INFO] Using Python: %PYTHON_EXE%
echo [INFO] Executing db_builder.py (creating retail_store.db and tables)...
echo.

"%PYTHON_EXE%" db_builder.py

echo.
echo ===============================================================================
echo   Database setup completed successfully. Output saved to Output\db_setup_output.txt
echo ===============================================================================
pause
