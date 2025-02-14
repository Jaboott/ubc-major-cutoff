from dotenv import load_dotenv

import psycopg2
import os

load_dotenv()

DB_CONFIG = {
    "database": os.getenv("DB_NAME"),
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

DB_CONNECTION = None


def get_connection():
    global DB_CONNECTION
    if DB_CONNECTION is None:
        try:
            DB_CONNECTION = psycopg2.connect(
                database=DB_CONFIG["database"],
                user=DB_CONFIG["user"],
                password=DB_CONFIG["password"],
                host=DB_CONFIG["host"],
                port=DB_CONFIG["port"]
            )
            return DB_CONNECTION
        except psycopg2.Error as e:
            print(f'Failed to get connection - {e}')
            return None
    else:
        return DB_CONNECTION


def close_connection():
    DB_CONNECTION.close()
