import duckdb
from backend.postgres import get_pg_connection

# connect to correct DuckDB file
duck_conn = duckdb.connect("database/flights.duckdb")

# STEP 1: extract + transform (DuckDB)
data = duck_conn.execute("""
    SELECT 
        airline,

        AVG(departure_delay_min) AS avg_delay,

        AVG(
            CASE 
                WHEN departure_delay_min <= 15 THEN 100
                ELSE 0
            END
        ) AS on_time_pct,

        AVG(
            CASE 
                WHEN is_cancelled = TRUE THEN 100
                ELSE 0
            END
        ) AS cancellation_rate

    FROM flights
    GROUP BY airline
""").fetchall()

print("DuckDB sample:", data[:5])

# STEP 2: load into PostgreSQL
pg_conn = get_pg_connection()
cursor = pg_conn.cursor()

cursor.execute("DELETE FROM airline_metrics")

print("Inserting rows into Postgres...")

for row in data:
    print("Inserting:", row)
    cursor.execute("""
        INSERT INTO airline_metrics (airline, avg_delay, on_time_pct, cancellation_rate)
        VALUES (%s, %s, %s, %s)
    """, row)

pg_conn.commit()

cursor.close()
pg_conn.close()
duck_conn.close()

print("ETL completed successfully")