import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DATA_DIR = os.path.join(BASE_DIR, "raw_data")
DB_PATH = os.path.join(BASE_DIR, "database", "flights.duckdb")

API_KEY = os.getenv("API_KEY", "")
BASE_URL = "https://aerodatabox.p.rapidapi.com"

HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "aerodatabox.p.rapidapi.com"
}