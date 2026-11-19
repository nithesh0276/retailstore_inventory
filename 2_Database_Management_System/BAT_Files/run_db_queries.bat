@echo off
title Retail Store DBMS - Query Execution and Reporting
color 0A

echo ===============================================================================
echo   RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - SQL QUERY RUNNER
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

echo [INFO] Running SQL queries against retail_store.db...
echo.

"%PYTHON_EXE%" execute_queries.py

echo.
echo ===============================================================================
echo   Queries executed successfully. Output saved to Output\query_execution_output.txt
echo ===============================================================================
pause
