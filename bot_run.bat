@echo off

call %~dp0Telegram_bot\venv\Scripts\activate

cd %~dp0Telegram_bot

set TOKEN=5302173979:AAHltsq5Bk8auFto6-fMEOrRh4oWaISymKg

python bot_telegram.py

pause