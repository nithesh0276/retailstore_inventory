@echo off
title "Retail Store Java - Automated Verification and Demonstration Runner"
color 0A

echo ===============================================================================
echo   RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - AUTOMATED DEMO
echo   Course: 25ITT32 - Java Programming (VCET R2025)
echo   Register No: 9, 39, 69, 99
echo ===============================================================================
echo.

cd /d "%~dp0\.."

if not exist "bin\com\retailstore\app\AutomatedDemoRunner.class" (
    echo [INFO] Binaries not found. Running compilation first...
    call "%~dp0compile_java.bat"
)

echo [INFO] Executing com.retailstore.app.AutomatedDemoRunner...
echo.

java --enable-native-access=ALL-UNNAMED -cp "bin;lib/*" com.retailstore.app.AutomatedDemoRunner

echo.
echo ===============================================================================
echo   Execution completed. Outputs saved to Output\java_application_output.txt
echo ===============================================================================
pause
