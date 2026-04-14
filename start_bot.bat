@echo off
chcp 65001 > nul
echo ================================
echo    🤖 Telegram Bot Launcher
echo ================================
echo.

REM Python versiyasini tekshirish
py --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [XATO] Python topilmadi!
    echo Python yuklab oling: https://python.org
    pause
    exit /b 1
)

echo [OK] Python topildi!

REM .env faylini tekshirish
if not exist ".env" (
    echo [XATO] .env fayli topilmadi!
    echo .env.example dan nusxa oling va to'ldiring:
    echo   copy .env.example .env
    pause
    exit /b 1
)
echo [OK] .env fayli mavjud!

REM Paketlarni o'rnatish (agar kerak bo'lsa)
echo.
echo [INFO] Paketlar tekshirilmoqda...
py -m pip install -r requirements.txt --quiet
echo [OK] Paketlar tayyor!

echo.
echo [START] Bot ishga tushmoqda...
echo [INFO] To'xtatish uchun: Ctrl+C
echo.
py bot.py

pause
