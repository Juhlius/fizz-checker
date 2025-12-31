import time
import requests
from bs4 import BeautifulSoup
import os

# -------------------------
# CONFIGURATION
# -------------------------
URL = "https://www.the-fizz.com/en/student-accommodation/utrecht/#apartment"
TELEGRAM_BOT_TOKEN = "8508989655:AAFjb044Rugm__f-08zudu2ijsopIkaV98E"
TELEGRAM_CHAT_ID = "6760011689"
STATE_FILE = "last_state.txt"  # file to remember last listing state
TEST_MODE = False  # set to True to force a Telegram test alert, False for normal operation

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/18.0 Safari/605.1.15",
    "Accept-Language": "en-US,en;q=0.9",
}

# -------------------------
# FUNCTION TO SEND TELEGRAM MESSAGE
# -------------------------
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        print(f"[{time.strftime('%H:%M:%S')}] Telegram message sent.")
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Error sending Telegram message:", e)

# -------------------------
# FUNCTIONS TO SAVE/READ LAST STATE
# -------------------------
def read_last_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return ""

def write_last_state(state):
    with open(STATE_FILE, "w") as f:
        f.write(state)

# -------------------------
# CHECK THE PAGE
# -------------------------
def check_page():
    response = requests.get(URL, headers=HEADERS)
    text = response.text

    # 🔍 DEBUG: save HTML that Python actually receives
    with open("debug_page.html", "w", encoding="utf-8") as f:
        f.write(text)

    no_listing_text = "Currently no Single Studio apartments available."
    current_state = "no_listings" if no_listing_text in text else "new_listing"
    last_state = read_last_state()

    if current_state != last_state:
        if current_state == "new_listing":
            send_telegram("🚨 New listing detected on THE FIZZ Utrecht!")
            print("New listing detected — Telegram sent.")
        else:
            print("Listings disappeared again.")

        write_last_state(current_state)
    else:
        print("No change.")

# -------------------------
# MAIN LOOP
# -------------------------
print("🚀 FIZZ checker started")

while True:
    check_page()
    time.sleep(300)  # 5 minutes
