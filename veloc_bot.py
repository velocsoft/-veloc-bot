import requests
import time
import sys
import io
import json
import uuid
import re
import threading
from datetime import datetime, timedelta

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

TOKEN = "8691625822:AAG6StpBiEuABXedFVTukDqc_-CCjwI_eJU"
API_URL = "https://ch.at/v1/chat/completions"
BASE = f"https://api.telegram.org/bot{TOKEN}"

user_histories = {}
last_msg_time = {}
reminders = []
reminder_id = 0
reminder_lock = threading.Lock()

KEYBOARD = json.dumps({
    "keyboard": [
        [{"text": "API Satın Al"}, {"text": "Kurucu ile iletişime geç"}]
    ],
    "is_persistent": True,
    "resize_keyboard": True
})

PROMPT = """Sen "Veloc" adinda bir yapay zeka asistanisin. Kullaniciya yardimci olmak icin burdasin.

KONUSMA TARZIN:
- Dogal Turkce konus ama AI oldugunu gizleme
- Kisa ve net cevaplar ver
- Samimi ve yardimsever ol
- Gereksiz backstory anlatma
- Sorulan soruya direkt cevap ver
- Kullanici hatirlatici istediyse "Hatirlatici ayarlandi" de ve detay ver

KURALLAR:
- Kisa cevap ver, 2-3 cumle yeter
- Samimi ol ama abartma
- Sorulara direkt cevap ver"""


def hatirlatici_kontrol():
    """Her 10 saniyede bir hatirlaticilari kontrol et"""
    global reminders
    while True:
        time.sleep(10)
        now = time.time()
        with reminder_lock:
            for r in reminders[:]:
                if now >= r["zaman"]:
                    try:
                        requests.get(f"{BASE}/sendMessage", params={
                            "chat_id": r["chat_id"],
                            "text": f"⏰ Hatirlatici: {r['mesaj']}"
                        })
                    except:
                        pass
                    reminders.remove(r)


def hatirlatici_ekle(chat_id, saniye, mesaj):
    """Hatirlatici ekle"""
    global reminder_id
    with reminder_lock:
        reminder_id += 1
        reminders.append({
            "id": reminder_id,
            "chat_id": chat_id,
            "zaman": time.time() + saniye,
            "mesaj": mesaj
        })
    return reminder_id


def hatirlatici_parse(text):
    """Metindeki hatirlaticiyi parse et"""
    t = text.lower()
    # Turkce karakter sorunlarini coz (sadece birim icin)
    for a, b in [("i", "x"), ("ı", "x"), ("ü", "u"), ("ö", "o"), ("ç", "c"), ("ş", "s"), ("ğ", "g")]:
        t = t.replace(a, b)
    t = t.replace("x", "i")
    
    pattern = r"(\d+)\s*(saniye|dakika|saat|sn|dk|sa)\s*(?:sonra|icinde)\s+(.+)"
    match = re.search(pattern, t)
    
    if not match:
        return None
    
    sayi = int(match.group(1))
    birim = match.group(2)
    
    # Mesaji orijinal metinden al
    orj_match = re.search(r"\d+\s*(?:saniye|dakika|saat|sn|dk|sa)\s*(?:sonra|icinde|içinde)\s+(.+)", text, re.IGNORECASE)
    mesaj = orj_match.group(1).strip() if orj_match else match.group(3).strip()
    
    if not mesaj:
        return None
    
    if birim in ("saniye", "sn"): saniye = sayi
    elif birim in ("dakika", "dk"): saniye = sayi * 60
    elif birim in ("saat", "sa"): saniye = sayi * 3600
    else: return None
    
    if saniye < 5: saniye = 5
    if saniye > 86400: saniye = 86400
    
    print(f"[Hatirlatici] {sayi} {birim} sonra: {mesaj}")
    return {"saniye": saniye, "mesaj": mesaj}


def cevap_ver(mesaj, user_id):
    if user_id not in user_histories:
        user_histories[user_id] = []
    history = user_histories[user_id]
    history.append({"role": "user", "content": mesaj})
    
    try:
        r = requests.post(API_URL, json={
            "messages": [
                {"role": "system", "content": PROMPT},
                *history[-10:]
            ],
            "model": "gpt-4o",
            "max_tokens": 512,
            "temperature": 0.9,
            "top_p": 0.9
        }, timeout=20)
        
        if r.status_code == 200:
            data = r.json()
            if "choices" in data and len(data["choices"]) > 0:
                reply = data["choices"][0]["message"]["content"].strip()
                history.append({"role": "assistant", "content": reply})
                if len(history) > 20:
                    user_histories[user_id] = history[-20:]
                return reply
        return "Yav simdi biraz mesgulum ya, sonra yazayim?"
    except:
        return "Off bi sorun var ya, bi daha dener misin?"


# Hatirlatici thread'ini baslat
t = threading.Thread(target=hatirlatici_kontrol, daemon=True)
t.start()

# Webhook temizle
requests.get(f"{BASE}/deleteWebhook?drop_pending_updates=true")
print("Webhook temizlendi.")

bot = requests.get(f"{BASE}/getMe").json()
print(f"Bot: {bot['result']['first_name']} (@{bot['result']['username']}) aktif!")
print("Mesajlar bekleniyor... Ctrl+C ile durdur.")
print("=" * 30)

offset = 0
while True:
    try:
        r = requests.get(f"{BASE}/getUpdates", params={
            "offset": offset,
            "timeout": 30
        }, timeout=35)
        
        if r.status_code != 200:
            time.sleep(3)
            continue
            
        updates = r.json().get("result", [])
        
        for update in updates:
            update_id = update["update_id"]
            offset = update_id + 1
            
            if "message" not in update:
                if "my_chat_member" in update:
                    chat = update["my_chat_member"]["chat"]
                    if chat["type"] in ("group", "supergroup"):
                        chat_id = chat["id"]
                        requests.get(f"{BASE}/sendMessage", params={
                            "chat_id": chat_id,
                            "text": "Bu bot sadece ozel mesajlar icindir. Gruba eklenemez."
                        })
                        requests.get(f"{BASE}/leaveChat", params={
                            "chat_id": chat_id
                        })
                continue
                
            msg = update["message"]
            text = msg.get("text", "")
            chat_id = msg["chat"]["id"]
            user_id = msg["from"]["id"]
            name = msg["from"].get("first_name", "Bilinmiyor")
            
            if not text:
                continue
            
            # SPAM KONTROLU
            now = time.time()
            if user_id in last_msg_time:
                fark = now - last_msg_time[user_id]
                if fark < 2:
                    print(f"[SPAM] {name}: {text}")
                    continue
            last_msg_time[user_id] = now
            
            # Komutlar
            if text.startswith("/start"):
                requests.get(f"{BASE}/sendMessage", params={
                    "chat_id": chat_id,
                    "text": f"Aleykum selam {name}. Hos geldin.",
                    "reply_markup": KEYBOARD
                })
                continue
            
            if text.startswith("/help"):
                requests.get(f"{BASE}/sendMessage", params={
                    "chat_id": chat_id,
                    "text": "Ben Veloc, AI asistanin.\n\n"
                            "Hatirlatici: \"10 dakika sonra yemegi hatirlat\"\n"
                            "Sohbet, bilgi, yardim...",
                    "reply_markup": KEYBOARD
                })
                continue
            
            if text == "/reminders":
                with reminder_lock:
                    aktif = [r for r in reminders if r["chat_id"] == chat_id]
                if aktif:
                    cevap = "Hatirlaticilarin:\n"
                    for r in aktif:
                        kalan = int(r["zaman"] - time.time())
                        cevap += f"- {r['mesaj']} ({kalan}sn kaldi)\n"
                else:
                    cevap = "Aktif hatirlaticin yok."
                requests.get(f"{BASE}/sendMessage", params={
                    "chat_id": chat_id,
                    "text": cevap,
                    "reply_markup": KEYBOARD
                })
                continue
            
            # Reply klavye buton kontrolu
            if text == "API Satın Al":
                requests.get(f"{BASE}/sendMessage", params={
                    "chat_id": chat_id,
                    "text": "API satin alma suanda bakimdadir. En kisa surede tekrar aktif olacaktir.\n\nBilgi ve destek icin @VelocSoft",
                    "reply_markup": KEYBOARD
                })
                continue
            
            if text == "Kurucu ile iletişime geç":
                requests.get(f"{BASE}/sendMessage", params={
                    "chat_id": chat_id,
                    "text": "@VelocSoft",
                    "reply_markup": KEYBOARD
                })
                continue
            
            # HATIRLATICI KONTROLU
            hatir = hatirlatici_parse(text)
            if hatir:
                h_id = hatirlatici_ekle(chat_id, hatir["saniye"], hatir["mesaj"])
                
                sure_str = ""
                if hatir["saniye"] >= 3600:
                    sure_str = f"{hatir['saniye']//3600} saat"
                elif hatir["saniye"] >= 60:
                    sure_str = f"{hatir['saniye']//60} dakika"
                else:
                    sure_str = f"{hatir['saniye']} saniye"
                
                requests.get(f"{BASE}/sendMessage", params={
                    "chat_id": chat_id,
                    "text": f"Hatirlatici ayarlandi! {sure_str} sonra sana hatirlatacagim: {hatir['mesaj']}",
                    "reply_markup": KEYBOARD
                })
                
                # AI'a da bildir ama cevap olarak degil
                print(f"[Hatirlatici] {name} - {sure_str} sonra: {hatir['mesaj']}")
                continue
            
            # Normal mesaj
            print(f"[{name}] {text}")
            
            requests.get(f"{BASE}/sendChatAction", params={
                "chat_id": chat_id,
                "action": "typing"
            })
            
            reply = cevap_ver(text, user_id)
            print(f"[Veloc] {reply[:60]}...")
            
            requests.get(f"{BASE}/sendMessage", params={
                "chat_id": chat_id,
                "text": reply,
                "reply_markup": KEYBOARD
            })
        
    except KeyboardInterrupt:
        print("\nBot durduruldu.")
        break
    except Exception as e:
        print(f"Hata: {e}")
        time.sleep(3)
