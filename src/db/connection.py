from dotenv import load_dotenv

import psycopg2.pool
import os

load_dotenv()

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

DB_CONNECTION_POOL = None


def get_connection():
    global DB_CONNECTION_POOL
    if DB_CONNECTION_POOL is None:
        try:
            DB_CONNECTION_POOL = psycopg2.pool.SimpleConnectionPool(
                1, 3,
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"],
                database=DB_CONFIG["database"]
            )
            return DB_CONNECTION_POOL.getconn()
        except psycopg2.Error as e:
            print(f'Failed to get connection - {e}')
            return None
    else:
        return DB_CONNECTION_POOL
