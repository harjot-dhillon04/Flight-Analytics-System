import duckdb
from backend.config import DB_PATH

conn = duckdb.connect(DB_PATH)

# 1. Check if DEL exists
print(conn.execute("""
SELECT DISTINCT departure_airport
FROM flights
ORDER BY departure_airport
""").fetchall())

conn.close()
