import duckdb
import json
import os
from datetime import datetime

from backend.config import RAW_DATA_DIR, DB_PATH

conn = duckdb.connect(DB_PATH)

# -----------------------------
# RESET TABLE
# -----------------------------

conn.execute("""
CREATE TABLE if not exists flights (
    flight_number TEXT,
    airline TEXT,
    departure_airport TEXT,
    arrival_airport TEXT,
    scheduled_departure TIMESTAMP,
    actual_departure TIMESTAMP,
    departure_delay_min DOUBLE,
    route TEXT,
    arrival_country TEXT,
    status TEXT,
    is_cancelled BOOLEAN
)
""")

print("Table created successfully")

# -----------------------------
# PARSE FILES
# -----------------------------
def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []

    for flight in data.get("departures", []):
        try:
            dep = flight.get("departure", {})
            arr = flight.get("arrival", {})
            airline = flight.get("airline", {})

            flight_number = flight.get("number")
            airline_name = airline.get("name")

            dep_airport = "YYZ"
            arr_airport = arr.get("airport", {}).get("iata")

            # 🟡 SAFE country extraction (fix)
            arr_country = None
            if arr and arr.get("airport"):
                arr_country = arr["airport"].get("countryCode")

            if not arr_airport:
                continue

            scheduled = dep.get("scheduledTime", {}).get("utc")
            actual = dep.get("runwayTime", {}).get("utc")

            if not scheduled:
                continue

            scheduled_dt = datetime.fromisoformat(scheduled.replace("Z", "+00:00"))
            actual_dt = (
                datetime.fromisoformat(actual.replace("Z", "+00:00"))
                if actual else None
            )

            delay = (
                (actual_dt - scheduled_dt).total_seconds() / 60
                if actual_dt else None
            )

            status = flight.get("status", "Unknown")
            is_cancelled = status.lower() in ["cancelled", "canceled"]

            rows.append((
                flight_number,
                airline_name,
                dep_airport,
                arr_airport,
                scheduled_dt,
                actual_dt,
                delay,
                f"{dep_airport}-{arr_airport}",
                arr_country,
                status,
                is_cancelled
            ))

        except Exception as e:
            print("Parse error:", e)
            continue

    return rows


# -----------------------------
# LOAD ALL FILES
# -----------------------------
all_rows = []

for file in os.listdir(RAW_DATA_DIR):
    if file.endswith(".json"):
        path = os.path.join(RAW_DATA_DIR, file)
        all_rows.extend(parse_file(path))

print("TOTAL ROWS:", len(all_rows))

if len(all_rows) == 0:
    raise Exception("No data loaded — check RAW_DATA_DIR or JSON structure")

# -----------------------------
# INSERT INTO DUCKDB
# -----------------------------
conn.executemany("""
INSERT INTO flights (
    flight_number,
    airline,
    departure_airport,
    arrival_airport,
    scheduled_departure,
    actual_departure,
    departure_delay_min,
    route,
    arrival_country,
    status,
    is_cancelled
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", all_rows)

print(f"Loaded {len(all_rows)} flights into DuckDB")

# -----------------------------
# VERIFY
# -----------------------------
print(conn.execute("PRAGMA table_info(flights)").fetchall())

conn.close()