from datetime import datetime

from dotenv import load_dotenv

import os
import pandas as pd
import hashlib
import time
import logging

from src.db.connection import get_connection, execute_query
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


# TODO complete the db stuff
def handle_change(data):
    new_checksum = create_checksum(data)

    # re-populating the db with the new data
    for i in range(data.shape[0]):
        major_stats = build_major_stats(data.iloc[i])
        if major_stats is not None:
            print(major_stats)

    return


def start_db():
    try:
        schema_path = "src/db/schema.sql"
        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found at {schema_path}")

        with open(schema_path, "r") as file:
            init_tables = file.read()
            execute_query(init_tables)
    except Exception as e:
        logging.error(e)


# TODO
def poll():
    data = read_document()

    start_db()
    print("db started")
    if has_checksum_changed(data):
        print("checksum changed")
        handle_change(data)


if __name__ == '__main__':
    # Computing time
    while True:
        start_time = time.time()
        poll()
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(5)
