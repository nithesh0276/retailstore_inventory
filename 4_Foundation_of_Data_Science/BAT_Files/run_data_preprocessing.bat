@echo off
title "Retail Store Data Science - Data Preprocessing and Cleaning Pipeline"
color 0B

echo ===============================================================================
echo   RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - DATA PREPROCESSING
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

echo [INFO] Running Data Cleaning, Outlier Detection and Transformation...
echo.

"%PYTHON_EXE%" data_preprocessor.py

echo.
echo ===============================================================================
echo   Preprocessing completed. Cleaned CSV files exported to Data_Preprocessing\
echo ===============================================================================
pause
