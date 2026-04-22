@echo off

echo =========================
echo KILL PORTA 4000
echo =========================

for /f "tokens=5" %%a in ('netstat -ano ^| findstr :4000') do (
    echo Killing PID %%a
    taskkill /PID %%a /F >nul 2>&1
)

timeout /t 1 >nul

echo =========================
echo AVVIO SERVER
echo =========================

python main.py

pause