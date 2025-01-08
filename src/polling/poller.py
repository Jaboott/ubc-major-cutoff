from datetime import datetime

from dotenv import load_dotenv

import os
import pandas as pd
import hashlib
import time
import logging

from src.db.connection import execute_query
from src.parser.excelParser import build_major_stats

load_dotenv()


def read_document():
    # make this into either config.json or env variable
    url = os.getenv('DOCUMENT_URL')

    try:
        df = pd.read_csv(url)
        return df
    except FileNotFoundError:
        logging.error('File not found')

    return None


def create_checksum(data):
    return hashlib.sha256(data.to_string().encode('utf-8')).hexdigest()


def has_checksum_changed(data):
    if data is None:
        return None

    try:
        result = execute_query("SELECT COUNT(*) FROM meta_data;")
        checksum = create_checksum(data)

        # initial setup of checksum
        if result[0][0] == 0:
            dt = datetime.now()
            execute_query("INSERT INTO meta_data (check_sum, last_updated) VALUES(%s, %s);", (checksum, dt))
            return True

        old_checksum = execute_query("SELECT check_sum FROM meta_data ORDER BY last_updated DESC LIMIT 1;")
        if old_checksum[0][0] != checksum:
            return True

    except Exception as e:
        logging.error(e)

    return False


# TODO might still have bugs
def handle_change(data):
    new_checksum = create_checksum(data)
    dt = datetime.now()

    try:
        execute_query("INSERT INTO meta_data (check_sum, last_updated) VALUES(%s, %s);", (new_checksum, dt))
        execute_query("DROP TABLE IF EXISTS admission_statistics, majors;")

        init_tables()

        # re-populating the db with the new data
        for index, row in data.iterrows():
            major_stats = build_major_stats(row)

            if major_stats is None:
                continue

            try:
                execute_query("INSERT INTO majors VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;",
                              (major_stats.name, major_stats.id, major_stats.type))
                execute_query(
                    "INSERT INTO admission_statistics VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;",
                    (major_stats.year, major_stats.max_grade, major_stats.min_grade, major_stats.initial_reject,
                     major_stats.final_admit, major_stats.id, major_stats.type))
            except Exception as e:
                print(major_stats)
                raise Exception("Failed to insert major_stats into db " + str(e))

    except Exception as e:
        logging.error(e)


def init_tables():
    try:
        schema_path = "src/db/schema.sql"
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found at {schema_path}")

        with open(schema_path, "r") as file:
            tables_schema = file.read()
            execute_query(tables_schema)
    except Exception as e:
        logging.error(e)


# TODO verify num of rows
def poll():
    data = read_document()

    init_tables()
    print("DB has started")
    if has_checksum_changed(data):
        print("checksum have changed")
        handle_change(data)


if __name__ == '__main__':
    # Computing time
    while True:
        start_time = time.time()
        poll()
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(5)
