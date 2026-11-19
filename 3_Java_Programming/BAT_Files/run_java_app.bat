@echo off
title "Retail Store Java - Interactive Point of Sale Application"
color 0E

echo ===============================================================================
echo   RETAIL STORE INVENTORY AND SALES ANALYSIS SYSTEM - INTERACTIVE APP
echo   Course: 25ITT32 - Java Programming (VCET R2025)
echo   Register No: 9, 39, 69, 99
echo ===============================================================================
echo.

cd /d "%~dp0\.."

if not exist "bin\com\retailstore\app\RetailStoreApp.class" (
    echo [INFO] Binaries not found. Running compilation first...
    call "%~dp0compile_java.bat"
)

echo [INFO] Launching RetailStoreApp console dashboard...
echo.

java --enable-native-access=ALL-UNNAMED -cp "bin;lib/*" com.retailstore.app.RetailStoreApp

pause
