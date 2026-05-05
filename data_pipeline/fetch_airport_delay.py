import requests
import time
import json
import os
from datetime import datetime, timedelta

from backend.config import BASE_URL, HEADERS

# -----------------------------
# CONFIG
# -----------------------------
AIRPORT = "AMS"   # <- change this per run

START_DATE = datetime(2026, 3, 25)
END_DATE = datetime(2026, 4, 25)

WINDOWS = [
    (0, 12),
    (6, 18),
    (12, 24)
]

BASE_DIR = "raw_data_airport_delay"

airport_dir = os.path.join(BASE_DIR, AIRPORT)
os.makedirs(airport_dir, exist_ok=True)

# -----------------------------
# API CALL
# -----------------------------
def fetch(airport, start, end):
    url = f"{BASE_URL}/flights/airports/iata/{airport}/{start}/{end}"

    params = {
        "direction": "Both",
        "withLeg": "true",
        "withCancelled": "true",
        "withCodeshared": "false",
        "withCargo": "false",
        "withPrivate": "false",
        "withLocation": "false"
    }

    r = requests.get(url, headers=HEADERS, params=params)

    if r.status_code != 200:
        print("ERROR:", r.status_code, r.text)
        return None

    return r.json()

# -----------------------------
# INGESTION LOOP (ONE AIRPORT)
# -----------------------------
current = START_DATE
day_index = 0

while current < END_DATE:

    start_hour, end_hour = WINDOWS[day_index % len(WINDOWS)]

    start = (current + timedelta(hours=start_hour)).strftime("%Y-%m-%dT%H:%M")
    end = (current + timedelta(hours=end_hour)).strftime("%Y-%m-%dT%H:%M")

    print(f"[{AIRPORT}] Day {day_index+1}: {start} → {end}")

    data = fetch(AIRPORT, start, end)

    if data:
        filename = os.path.join(
            airport_dir,
            f"{AIRPORT}_{start_hour}_{start.replace(':','-')}.json"
        )

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print("Saved:", filename)

    time.sleep(1.5)  # rate limiting safety

    current += timedelta(days=1)
    day_index += 1

print("INGESTION COMPLETE")
