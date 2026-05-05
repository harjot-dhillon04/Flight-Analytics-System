import requests
import time
import json
import os
from datetime import datetime, timedelta

from backend.config import BASE_URL, HEADERS, RAW_DATA_DIR

os.makedirs(RAW_DATA_DIR, exist_ok=True)

end_date = datetime(2026, 4, 11)
start_date = end_date - timedelta(days=17)

def fetch(start, end):
    url = f"{BASE_URL}/flights/airports/iata/YYZ/{start}/{end}"

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
        print("ERROR:", r.status_code)
        return None

    return r.json()


current = start_date
day = 0

while current < end_date:

    for hour in [0, 12]:

        start = (current + timedelta(hours=hour)).strftime("%Y-%m-%dT%H:%M")
        end = (current + timedelta(hours=hour + 12)).strftime("%Y-%m-%dT%H:%M")

        print(f"[{day+1}/14] {start} → {end}")

        data = fetch(start, end)

        if data:
            filename = os.path.join(
                RAW_DATA_DIR,
                f"yyz_{start.replace(':','-')}.json"
            )

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

            print("Saved:", filename)

        time.sleep(1.5)

    current += timedelta(days=1)
    day += 1

print("INGESTION COMPLETE")