@echo off
title BUILDER AUTO START

echo =========================
echo CHIUSURA PORTA 5000
echo =========================

FOR /F "tokens=5" %%a IN ('netstat -ano ^| findstr :5000') DO (
    echo Chiudo processo %%a
    taskkill /PID %%a /F >nul 2>&1
)

timeout /t 1 >nul

echo =========================
echo AVVIO BUILDER
echo =========================

cd /d C:\Users\Ale\Desktop\Realm of Lord\mud_server\builder

python server.py

pause