import duckdb

conn = duckdb.connect("flights.duckdb")

# 1. Quick sanity check
print(conn.execute("SELECT COUNT(*) FROM flights").fetchall())

# 2. Sample rows
print(conn.execute("SELECT * FROM flights LIMIT 5").fetchall())

# 3. Top delayed airlines
print(conn.execute("""
SELECT airline, AVG(departure_delay_min) as avg_delay
FROM flights
WHERE departure_delay_min IS NOT NULL
GROUP BY airline
ORDER BY avg_delay DESC
LIMIT 10
""").fetchall())

# 4. Busiest routes
print(conn.execute("""
SELECT route, COUNT(*) as flights
FROM flights
GROUP BY route
ORDER BY flights DESC
LIMIT 10
""").fetchall())

# 5. Cancellation rate
print(conn.execute("""
SELECT airline,
AVG(is_cancelled::INT) as cancellation_rate
FROM flights
GROUP BY airline
ORDER BY cancellation_rate DESC
LIMIT 10
""").fetchall())