@echo off
echo Bot temizleniyor...
C:\Users\Gamer\AppData\Local\Programs\Python\Python312\python.exe -c "import requests; requests.get('https://api.telegram.org/bot8691625822:AAG6StpBiEuABXedFVTukDqc_-CCjwI_eJU/deleteWebhook?drop_pending_updates=true')"
echo.
echo Bot baslatiliyor...
C:\Users\Gamer\AppData\Local\Programs\Python\Python312\python.exe C:\Users\Gamer\Pictures\Desktop\GMESD\veloc_bot.py
pause
