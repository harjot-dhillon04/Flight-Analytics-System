import duckdb
from backend.config import DB_PATH

conn = duckdb.connect(DB_PATH)

# 1. Check if DEL exists
print(conn.execute("""
SELECT DISTINCT departure_airport
FROM flights
ORDER BY departure_airport
""").fetchall())

# 2. Count DEL flights
print(conn.execute("""
SELECT COUNT(*) 
FROM flights
WHERE departure_airport = 'DEL'
""").fetchone())

print(conn.execute("""
SELECT
    COUNT(*) AS total,
    COUNT(departure_delay_min) AS non_null_delays
FROM flights
WHERE departure_airport = 'DXB';
""").fetchone())

conn.close()