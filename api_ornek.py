"""
Veloc API - Entegrasyon Ornegi
Kullanim: pip install requests
"""

import requests

API_URL = "https://a35823-51ce.e.jrnm.app/chat"
API_KEY = "veloc-XXXXXXXXXXXXXXXX"  # Buraya kendi key'ini yaz

def veloc_chat(mesaj):
    """Veloc AI ile sohbet et"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "message": mesaj
    }

    r = requests.post(API_URL, json=data, headers=headers)
    return r.json()

# Kullanim ornegi
sonuc = veloc_chat("selam nasılsın")
print(sonuc)
