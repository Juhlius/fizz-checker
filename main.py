import time
import requests
from bs4 import BeautifulSoup
import os

URL = "https://www.the-fizz.com/en/student-accommodation/utrecht/#apartment"
TELEGRAM_BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "PUT_YOUR_CHAT_ID_HERE"
STATE_FILE = "last_state.txt"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    })

def read_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return ""

def write_last_state(state):
    with open(STATE_FILE, "w") as f:
        f.write(state)

def check_page():
    response = requests.get(URL, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text()

    no_listing_text = "Currently no Single Studio apartments available."
    current_state = "no_listings" if no_listing_text in text else "new_listing"
    last_state = read_last_state()

    if current_state != last_state:
        if current_state == "new_listing":
            send_telegram("🚨 New listing detected on THE FIZZ Utrecht!")
            print("New listing detected — Telegram sent.")
        write_last_state(current_state)
    else:
        print("No change.")

print("🚀 FIZZ checker started")

while True:
    try:
        check_page()
    except Exception as e:
        print("Error:", e)
    time.sleep(300)
