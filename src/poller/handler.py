from datetime import datetime

from dotenv import load_dotenv

import os
import pandas as pd
import hashlib
import time
import logging

from src.db.connection import get_connection
from src.parser.excelParser import build_major_stats

load_dotenv()

DB_CONNECTION = get_connection()


def read_document():
    url = os.getenv('DOCUMENT_URL')

    if url is not None:
        try:
            df = pd.read_csv(url)
            return df
        except FileNotFoundError:
            print(f'Did not find the major cutoff file from given url: {url}')
    else:
        print(f'env variable DOCUMENT_URL must be set to the url of major cutoff file')

    return None


def create_checksum(data):
    return hashlib.sha256(data.to_string().encode('utf-8')).hexdigest()


def has_checksum_changed(data):
    # data is guaranteed to be not None
    try:
        with DB_CONNECTION.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM meta_data;")
            result = cursor.fetchall()
            checksum = create_checksum(data)

            # returns true if table is empty - fresh setup
            if result[0][0] == 0:
                return True

            cursor.execute("SELECT check_sum FROM meta_data ORDER BY last_updated DESC LIMIT 1;")
            old_checksum = cursor.fetchall()
            return old_checksum[0][0] != checksum
    except Exception as e:
        print(f'Failed to check for checksum changes with error: {e}')
        return False


# TODO might still have bugs
def handle_change(data):
    new_checksum = create_checksum(data)
    dt = datetime.now()
    success = True
    print("Re-populating db")
    try:
        with DB_CONNECTION.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE admission_statistics, majors;")

            # re-populating the db with the new data
            for index, row in data.iterrows():
                major_stats = build_major_stats(row)

                if major_stats is None:
                    continue

                try:
                    cursor.execute("INSERT INTO majors VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
                                   (major_stats.name, major_stats.id, major_stats.type))
                    cursor.execute(
                        "INSERT INTO admission_statistics VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                        (major_stats.year, major_stats.max_grade, major_stats.min_grade, major_stats.initial_reject,
                         major_stats.final_admit, major_stats.id, major_stats.domestic))
                except Exception as e:
                    print(f"Failed to insert {major_stats} to db: {e}")
                    success = False

            if not success:
                DB_CONNECTION.rollback()

            # update the checksum in meta_data
            cursor.execute("INSERT INTO meta_data (check_sum, last_updated, success) VALUES(%s, %s, %s);",
                           (new_checksum, dt, success))
            DB_CONNECTION.commit()
            print("Successfully populated db")
    except Exception as e:
        print(f"Failed to get cursor from connection with error: {e}")


def init_tables():
    try:
        with DB_CONNECTION.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
            num_tables = cursor.fetchall()
            # Create major_type if initial db setup
            if num_tables[0][0] == 0:
                print("Initial db setup")
                cursor.execute("CREATE TYPE major_type AS ENUM('Major', 'Combined_Major', 'Honours', 'Combined_Honours');")

            schema_path = "src/db/schema.sql"
            if not os.path.exists(schema_path):
                raise FileNotFoundError(f"Schema file not found at {schema_path}")

            with open(schema_path, "r") as file:
                tables_schema = file.read()
                cursor.execute(tables_schema)

            DB_CONNECTION.commit()
    except Exception as e:
        logging.error("Failed to initialize tables " + str(e))


# TODO verify num of rows
def handler(event, context):
    try:
        start_time = time.time()
        data = read_document()

        if data is None:
            return {
                'status_code': 400,
                'body': {'error': 'Failed to read major cutoff file'}
            }

        if DB_CONNECTION is None:
            return {
                'status_code': 400,
                'body': {'error': 'Failed to connect to db'}
            }

        init_tables()
        print("DB has started")

        if has_checksum_changed(data):
            print("Checksum have changed")
            handle_change(data)
            print("Time to populate db: " + str(time.time() - start_time))
            return {"message": "checksum have changed, db have been updated successfully in " + str(
                time.time() - start_time) + " seconds"}

        print("checksum did not change")
        return {"message": "checksum did not change"}
    except Exception as e:
        logging.error(f"Failed to poll: {e}")
        raise Exception(e)

