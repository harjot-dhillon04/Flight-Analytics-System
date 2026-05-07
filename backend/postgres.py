import psycopg2

def get_pg_connection():
    return psycopg2.connect(
        dbname="flight_data",
        user="postgres",
        password="Rubysandy1_",
        host="host.docker.internal",
        port="5432"
    )