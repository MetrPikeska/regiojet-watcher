import requests
import os

URL = "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple"
PARAMS = {
    "fromLocationType": "CITY",
    "fromLocationId": "10202002",  # Frýdek-Místek
    "toLocationType": "CITY",
    "toLocationId": "10202000",    # Olomouc
    "departureDate": "2025-10-06"
}
TARGET_TIME = "06:05"  # spoj, který hlídáš

TG_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(msg):
    """Pošle zprávu do Telegramu"""
    if not TG_TOKEN or not TG_CHAT:
        print("⚠️ Telegram není nastavený!")
        return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_CHAT, "text": msg}
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        print("Chyba při odesílání na Telegram:", e)

def main():
    r = requests.get(URL, params=PARAMS, timeout=15)
    data = r.json()
    for route in data.get("routes", []):
        if TARGET_TIME in route.get("departureTime", ""):
            seats = route.get("freeSeatsCount", 0)
            if seats > 0:
                msg = f"🎉 Volné místo! {seats} ks na spoj {TARGET_TIME}. Kup hned: https://regiojet.cz/"
                print(msg)
                send_telegram(msg)
                return
    print("Stále vyprodáno…")

if __name__ == "__main__":
    main()
ss
