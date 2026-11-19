@echo off
title "Retail Store Data Science - Statistical Modeling and EDA"
color 0E

echo ===============================================================================
echo   RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - STATISTICAL EDA
echo   Course: 25ITC31 - Foundations of Data Science (VCET R2025)
echo   Register No: 9, 39, 69, 99
echo ===============================================================================
echo.

cd /d "%~dp0\..\Python_Source_Code"

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

echo [INFO] Computing Descriptive Statistics and Business Performance Metrics...
echo.

"%PYTHON_EXE%" data_analyzer.py

echo.
echo ===============================================================================
echo   Statistical Analysis completed successfully.
echo ===============================================================================
pause
