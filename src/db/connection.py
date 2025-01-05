import logging

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


def get_connection():
    connection = psycopg2.connect(
        database=DB_CONFIG["database"],
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        port=DB_CONFIG["port"]
    )

    return connection


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
        connection.close()


