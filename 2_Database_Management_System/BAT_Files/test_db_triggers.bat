@echo off
title Retail Store DBMS - Trigger and Integrity Verification
color 0E

echo ===============================================================================
echo   RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - TRIGGER TEST RUNNER
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

echo [INFO] Testing Automated Stock Deduction & Over-Sale Prevention Triggers...
echo.

"%PYTHON_EXE%" test_triggers.py

echo.
echo ===============================================================================
echo   Trigger tests completed. Output saved to Output\trigger_test_output.txt
echo ===============================================================================
pause
