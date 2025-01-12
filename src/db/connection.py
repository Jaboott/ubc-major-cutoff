from dotenv import load_dotenv

from psycopg2 import pool
import os

load_dotenv()

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

connection_pool = None


def start_connection():
    global connection_pool
    connection_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        database=DB_CONFIG["database"]
    )


def get_connection():
    if connection_pool:
        return connection_pool.getconn()
    else:
        raise Exception("Connection pool is not initialized")


def release_connection(connection):
    connection_pool.putconn(connection)


def close_all_connections():
    connection_pool.closeall()


def execute_query(query, params=None):
    try:
        connection = get_connection()

        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            connection.commit()

            if cursor.description:
                return cursor.fetchall()

            return []
    except Exception as e:
        raise Exception(f"Error executing query: {e}")
    finally:
        if connection:
            release_connection(connection)

