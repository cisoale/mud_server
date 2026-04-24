@echo off
title MUD Builders (FIXED)

cd /d %~dp0

echo ==========================
echo   AVVIO BUILDERS
echo ==========================

echo.
echo [1] Avvio Builder Classico...
start "Builder Classico" cmd /k "python server.py"

timeout /t 2 >nul

echo.
echo [2] Avvio Visual Builder...
start "Visual Builder" cmd /k "python server_visual.py"

timeout /t 3 >nul

echo.
echo [3] Apertura browser...

start http://127.0.0.1:5000
start http://127.0.0.1:5001/editor_visual

echo.
echo ==========================
echo   TUTTO AVVIATO
echo ==========================

pause