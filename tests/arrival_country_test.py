import duckdb
from backend.config import DB_PATH

conn = duckdb.connect(DB_PATH)

print(conn.execute("""
SELECT DISTINCT departure_airport
FROM flights
ORDER BY departure_airport
""").fetchall())

conn.close()
