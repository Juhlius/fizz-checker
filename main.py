import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# -------------------------
# CONFIGURATION
# -------------------------
TELEGRAM_BOT_TOKEN = "8508989655:AAFjb044Rugm__f-08zudu2ijsopIkaV98E"
TELEGRAM_CHAT_ID = "6760011689"

URL = "https://www.the-fizz.com/en/student-accommodation/utrecht/#apartment"
STATE_DIR = "states"
if not os.path.exists(STATE_DIR):
    os.mkdir(STATE_DIR)

# Button labels
BUTTON_TEXTS = {
    "Single Studio": "Single",
    "Double": "Double"
}

# Placeholder selector for room listings; update when real rooms appear
LISTING_SELECTOR = "div.apartment-listing"

# -------------------------
# TELEGRAM FUNCTION
# -------------------------
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        print(f"[{time.strftime('%H:%M:%S')}] Telegram sent: {message}")
    except Exception as e:
        print(f"Telegram error: {e}")

# -------------------------
# STATE FUNCTIONS
# -------------------------
def read_last_state(key):
    file_path = os.path.join(STATE_DIR, f"{key}.txt")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip()
    return "no"

def write_last_state(key, state):
    file_path = os.path.join(STATE_DIR, f"{key}.txt")
    with open(file_path, "w") as f:
        f.write(state)

# -------------------------
# CHECK ROOM FUNCTION
# -------------------------
def check_room(driver, room_name, button_text):
    try:
        # Click the button based on its visible text
        try:
            button = driver.find_element(By.XPATH, f"//button[text()='{button_text}']")
            button.click()
            time.sleep(1)  # wait for overlay to appear
        except:
            print(f"[{time.strftime('%H:%M:%S')}] Button for {room_name} not found.")

        # Check for room listing elements
        listings = driver.find_elements(By.CSS_SELECTOR, LISTING_SELECTOR)
        found_listing = len(listings) > 0

        last_state = read_last_state(room_name)

        if found_listing and last_state != "yes":
            send_telegram(f"🚨 New {room_name} listing detected on FIZZ Utrecht!")
            write_last_state(room_name, "yes")
        elif not found_listing and last_state != "no":
            write_last_state(room_name, "no")

        print(f"[{time.strftime('%H:%M:%S')}] Checked {room_name}: found={found_listing}")

    except Exception as e:
        print(f"Error checking {room_name}: {e}")

# -------------------------
# MAIN LOOP
# -------------------------
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

print("🚀 FIZZ checker started")
try:
    while True:
        driver.get(URL)
        time.sleep(2)  # wait for page load

        for room_name, button_text in BUTTON_TEXTS.items():
            check_room(driver, room_name, button_text)

        time.sleep(300)  # check every 5 minutes

finally:
    driver.quit()
