from fastapi import FastAPI
import duckdb

from backend.config import DB_PATH

app = FastAPI()

def get_connection():
    return duckdb.connect(DB_PATH)

@app.get("/")
def root():
    return {"message": "Flight Analytics API is running"}

@app.get("/yyz/routes/busiest")
def busiest_routes():
    conn = get_connection()

    result = conn.execute("""
        SELECT route, COUNT(*) AS flights
        FROM flights
        WHERE departure_airport = 'YYZ'
        GROUP BY route
        ORDER BY flights DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return [
        {"route": r[0], "flights": r[1]}
        for r in result
    ]

@app.get("/yyz/airlines/delay")
def airline_delays():
    conn = get_connection()

    result = conn.execute("""
        SELECT 
        airline,
        COUNT(*) AS flights,
        ROUND(AVG(departure_delay_min), 2) AS avg_delay
        FROM flights
        WHERE departure_airport = 'YYZ'
        GROUP BY airline
        HAVING COUNT(*) >= 10
        ORDER BY avg_delay DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return [
        {
            "airline": r[0],
            "flights": r[1],
            "avg_delay": r[2]
        }
        for r in result
    ]

@app.get("/yyz/airlines/cancellations")
def cancellations():
    conn = get_connection()

    result = conn.execute("""
        SELECT 
            airline,
            ROUND(SUM(is_cancelled) * 1.0 / COUNT(*) * 100, 1) AS cancel_rate
        FROM flights
        WHERE departure_airport = 'YYZ'
        AND airline NOT IN ('Flexjet', 'AirSprint', 'NetJets Aviation', 'Morningstar Air Express', 'Envoy Air')
        GROUP BY airline
        HAVING COUNT(*) >= 10
        ORDER BY cancel_rate DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return [
        {
            "airline": r[0],
            "cancel_rate": r[1]  # e.g., 4.2 instead of 0.042
        }
        for r in result
    ]

@app.get("/yyz/airlines/on-time")
def on_time():
    conn = get_connection()

    result = conn.execute("""
        SELECT 
            airline,
            COUNT(*) AS total_flights,
            ROUND(
                SUM(CASE WHEN departure_delay_min <= 15 THEN 1 ELSE 0 END) * 1.0 
                / COUNT(*) *100,
                2
            ) AS on_time_rate
        FROM flights
        WHERE departure_airport = 'YYZ'
        AND departure_delay_min IS NOT NULL
        AND is_cancelled = FALSE
        AND airline NOT IN ('Flexjet', 'AirSprint', 'NetJets Aviation', 'Morningstar Air Express', 'Envoy Air', 'BMA')
        GROUP BY airline
        HAVING COUNT(*) >= 13
        ORDER BY on_time_rate DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return [
        {
            "airline": r[0],
            "total_flights": r[1],
            "on_time_rate": r[2]
        }
        for r in result
    ]

@app.get("/yyz/routes/busiest/international")
def busiest_routes_international():
    conn = get_connection()

    result = conn.execute("""
        SELECT 
            route,
            COUNT(*) AS flights
        FROM flights
        WHERE departure_airport = 'YYZ'
          AND arrival_country NOT IN ('us', 'ca')
        GROUP BY route
        ORDER BY flights DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return [
        {"route": r[0], "flights": r[1]}
        for r in result
    ]

@app.get("/yyz/analytics/delay/by-time")
def delay_by_time():
    conn = get_connection()

    result = conn.execute("""
        SELECT
            FLOOR(EXTRACT(HOUR FROM scheduled_departure) / 3) * 3 AS interval_start,
            COUNT(*) AS total_flights,
            ROUND(AVG(departure_delay_min), 2) AS avg_delay
        FROM flights
        WHERE departure_airport = 'YYZ'
          AND departure_delay_min IS NOT NULL
        GROUP BY interval_start
        HAVING interval_start != 3
        ORDER BY interval_start
    """).fetchall()

    conn.close()

    return [
        {
            "time interval": f"{int(r[0]):02d}:00-{int(r[0]+3):02d}:00",
            "total_flights": r[1],
            "avg_delay": r[2]
        }
        for r in result
    ]

@app.get("/yyz/analytics/on-time/by-time")
def on_time_by_time():
    conn = get_connection()

    result = conn.execute("""
        SELECT
            FLOOR(EXTRACT(HOUR FROM scheduled_departure) / 3) * 3 AS interval_start,
            COUNT(*) AS total_flights,
            ROUND(
                (SUM(CASE 
                    WHEN departure_delay_min <= 15 THEN 1 
                    ELSE 0 
                END) * 1.0 / COUNT(*)) * 100,
                2
            ) AS on_time_rate
        FROM flights
        WHERE departure_airport = 'YYZ'
          AND departure_delay_min IS NOT NULL
        GROUP BY interval_start
        HAVING interval_start != 3
        ORDER BY interval_start
    """).fetchall()

    conn.close()

    return [
        {
            "time_interval": f"{int(r[0]):02d}:00-{int(r[0]+3):02d}:00",
            "total_flights": r[1],
            "on_time_rate": r[2]  # already a percentage
        }
        for r in result
    ]
@app.get("/yyz/analytics/route/airlines")
def route_airline_performance(route: str):
    conn = get_connection()

    result = conn.execute("""
        SELECT
            airline,
            COUNT(*) AS total_flights,
            ROUND(AVG(departure_delay_min), 2) AS avg_delay,
            ROUND(
                (SUM(CASE WHEN departure_delay_min <= 15 THEN 1 ELSE 0 END) * 1.0 
                / COUNT(*)) * 100,
                1
            ) AS on_time_rate
        FROM flights
        WHERE departure_airport = 'YYZ'
        AND route = ?
          AND departure_delay_min IS NOT NULL
          AND is_cancelled = FALSE
        AND airline NOT IN ('Flexjet', 'AirSprint', 'NetJets Aviation', 'Morningstar Air Express', 'Envoy Air', 'Solarius Aviation', 'POD', 'NUS')
        GROUP BY airline
        ORDER BY avg_delay ASC
    """, [route]).fetchall()

    conn.close()

    return [
        {
            "airline": r[0],
            "total_flights": r[1],
            "avg_delay": r[2],
            "on_time_rate": r[3]  # already rounded %
        }
        for r in result
    ]

@app.get("/yyz/analytics/routes/worst-delays")
def worst_routes_by_delay():
    conn = get_connection()

    result = conn.execute("""
        SELECT
            route,
            COUNT(*) AS total_flights,
            ROUND(AVG(departure_delay_min), 2) AS avg_delay
        FROM flights
        WHERE departure_airport = 'YYZ'
          AND departure_delay_min IS NOT NULL
          AND is_cancelled = FALSE
        GROUP BY route
        HAVING COUNT(*) >= 14
        ORDER BY avg_delay DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return [
        {
            "route": r[0],
            "total_flights": r[1],
            "avg_delay": r[2]
        }
        for r in result
    ]

@app.get("/airports/global-comparison")
def global_comparison():
    conn = get_connection()

    result = conn.execute("""
        SELECT
            departure_airport AS airport,
            COUNT(*) AS total_flights,
            AVG(departure_delay_min) AS avg_delay,
            SUM(CASE WHEN departure_delay_min <= 15 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS on_time_pct
        FROM flights
        WHERE departure_delay_min IS NOT NULL
          AND is_cancelled = FALSE
        GROUP BY departure_airport
        ORDER BY avg_delay DESC
    """).fetchall()

    conn.close()

    data = [
        {
            "airport": r[0],
            "avg_delay": round(r[2], 2),
            "on_time_pct": round(r[3], 2)
        }
        for r in result
    ]

    # extract YYZ comparison
    yyz = next((x for x in data if x["airport"] == "YYZ"), None)

    # ranking
    sorted_by_delay = sorted(data, key=lambda x: x["avg_delay"], reverse=True)

    yyz_rank = next(
        (i + 1 for i, x in enumerate(sorted_by_delay) if x["airport"] == "YYZ"),
        None
    )

    return {
        "yyz": yyz,
        "yyz_rank_by_delay": yyz_rank,
        "airports": sorted_by_delay
    }

@app.get("/global/worst-time-intervals")
def worst_time_intervals():
    conn = get_connection()

    result = conn.execute("""
        WITH intervals AS (
            SELECT
                departure_airport,
                FLOOR(EXTRACT(HOUR FROM scheduled_departure) / 3) * 3 AS interval_start,
                AVG(departure_delay_min) AS avg_delay
            FROM flights
            WHERE departure_delay_min IS NOT NULL
              AND is_cancelled = FALSE
            GROUP BY departure_airport, interval_start
        ),
        ranked AS (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY departure_airport
                       ORDER BY avg_delay DESC
                   ) AS rank
            FROM intervals
        )
        SELECT
            departure_airport,
            interval_start,
            ROUND(avg_delay, 2) AS avg_delay
        FROM ranked
        WHERE rank = 1
        ORDER BY avg_delay DESC
    """).fetchall()

    conn.close()

    return [
        {
            "airport": r[0],
            "interval": f"{int(r[1]):02d}:00-{int(r[1]+3):02d}:00",
            "avg_delay": r[2]
        }
        for r in result
    ]

@app.get("/global/airports/busiest-interval")
def busiest_interval_per_airport():
    conn = get_connection()

    result = conn.execute("""
        WITH intervals AS (
            SELECT
                departure_airport AS airport,
                FLOOR(EXTRACT(HOUR FROM scheduled_departure) / 3) * 3 AS interval_start,
                COUNT(*) AS total_flights,
                AVG(departure_delay_min) AS avg_delay
            FROM flights
            WHERE scheduled_departure IS NOT NULL
              AND departure_airport != 'DEL'
            GROUP BY 
                departure_airport,
                FLOOR(EXTRACT(HOUR FROM scheduled_departure) / 3) * 3
        ),
        ranked AS (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY airport
                       ORDER BY total_flights DESC
                   ) AS rank
            FROM intervals
        )
        SELECT
            airport,
            interval_start,
            total_flights,
            ROUND(avg_delay, 2) AS avg_delay
        FROM ranked
        WHERE rank = 1
        ORDER BY total_flights DESC;
    """).fetchall()

    conn.close()

    return [
        {
            "airport": r[0],
            "interval": f"{int(r[1]):02d}:00-{int(r[1]+3):02d}:00",
            "avg_delay": r[3]
        }
        for r in result
    ]
@app.get("/global/airports/{airport}/airlines/summary")
def airline_summary_at_airport(airport: str, airline: str):
    conn = get_connection()

    result = conn.execute("""
        WITH airline_stats AS (
            SELECT
                airline,
                COUNT(*) AS total_flights,
                ROUND(AVG(departure_delay_min), 2) AS avg_delay,
                ROUND(
                    SUM(CASE WHEN departure_delay_min <= 15 THEN 1 ELSE 0 END) * 100.0
                    / COUNT(*),
                    2
                ) AS on_time_pct
            FROM flights
            WHERE departure_airport = ?
              AND departure_delay_min IS NOT NULL
              AND is_cancelled = FALSE
            GROUP BY airline
        ),
        ranked AS (
            SELECT *,
                   RANK() OVER (ORDER BY avg_delay DESC) AS delay_rank,
                   COUNT(*) OVER () AS total_airlines_at_airport
            FROM airline_stats
        )
        SELECT *
        FROM ranked
        WHERE airline = ?
    """, [airport.upper(), airline]).fetchone()

    conn.close()

    if not result:
        return {
            "airport": airport.upper(),
            "airline": airline,
            "message": "No data found"
        }

    return {
        "airport": airport.upper(),
        "airline": result[0],
        "total_flights": result[1],
        "avg_delay": result[2],
        "on_time_pct": result[3],
        "delay_rank_at_airport": result[4],
        "total_airlines_at_airport": result[5]
    }

@app.get("/db-test")
def db_test():
    conn = get_connection()
    result = conn.execute("SELECT COUNT(*) FROM flights").fetchone()
    conn.close()
    return {"rows": result[0]}