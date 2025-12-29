import time
import requests
from bs4 import BeautifulSoup
import os

# -------------------------
# 1. CONFIGURE THESE
# -------------------------
URL = "https://www.the-fizz.com/en/student-accommodation/utrecht/#apartment"
TELEGRAM_BOT_TOKEN = "8508989655:AAFjb044Rugm__f-08zudu2ijsopIkaV98E"
TELEGRAM_CHAT_ID = "6760011689"
STATE_FILE = "last_state.txt"  # file to remember last check

# -------------------------
# 2. Send Telegram message
# -------------------------
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})

# -------------------------
# 3. Read/Write last state
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
# 4. Check page
# -------------------------
def check_page():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        current_state = "no_listings" if "Currently no Single Studio apartments available." in text else "new_listing"
        last_state = read_last_state()

        if current_state != last_state:
            if current_state == "new_listing":
                send_telegram("🚨 New listing detected! Check the FIZZ page!")
                print("New listing detected! Telegram sent.")
            else:
                print("No listings currently.")
            write_last_state(current_state)
        else:
            print("No change since last check.")

    except Exception as e:
        print("Error checking page:", e)

# -------------------------
# 5. Main loop: run every 5 minutes
# -------------------------
if __name__ == "__main__":
    while True:
        check_page()
        time.sleep(300)  # 5 minutes
