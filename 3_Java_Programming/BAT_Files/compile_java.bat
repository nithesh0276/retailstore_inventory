@echo off
title "Retail Store Java - Compile Source Code"
color 0B

echo ===============================================================================
echo   RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - JAVA COMPILER
echo   Course: 25ITT32 - Java Programming (VCET R2025)
echo   Register No: 9, 39, 69, 99
echo ===============================================================================
echo.

cd /d "%~dp0\.."

if not exist "bin" mkdir "bin"

echo [INFO] Compiling Java source files...
javac -cp "lib/*" -d bin Source_Code\com\retailstore\model\*.java Source_Code\com\retailstore\exception\*.java Source_Code\com\retailstore\util\*.java Source_Code\com\retailstore\dao\*.java Source_Code\com\retailstore\service\*.java Source_Code\com\retailstore\app\*.java

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ===============================================================================
    echo   [SUCCESS] All Java source files compiled successfully into bin\
    echo ===============================================================================
) else (
    echo.
    echo [ERROR] Java compilation failed with error code %ERRORLEVEL%.
)
pause
