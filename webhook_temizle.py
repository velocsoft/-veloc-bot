import requests
import time

TOKEN = "8691625822:AAG6StpBiEuABXedFVTukDqc_-CCjwI_eJU"

# Webhook'u temizle
print("Webhook temizleniyor...")
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true")
print(r.json())

# Bot bilgilerini kontrol et
print("\nBot kontrol ediliyor...")
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe")
print(r.json())

print("\nTamam! Simdi bot_baslat.bat dosyasina cift tikla.")
time.sleep(3)
