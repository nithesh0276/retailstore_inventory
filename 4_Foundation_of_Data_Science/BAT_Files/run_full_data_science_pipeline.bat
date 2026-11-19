@echo off
title "Retail Store Data Science - Full Analytics & Visualization Pipeline"
color 0A

echo ===============================================================================
echo   RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - MASTER DATA SCIENCE
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

echo [INFO] Executing Full Data Science Pipeline (Extraction, Preprocessing, EDA, Visualizations)...
echo.

"%PYTHON_EXE%" run_full_analysis.py

echo.
echo ===============================================================================
echo   Pipeline completed! Visualizations saved to Visualizations\
echo   Analysis report saved to Output\data_science_analysis_output.txt
echo ===============================================================================
pause
