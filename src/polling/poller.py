from dotenv import load_dotenv

import os
import pandas as pd
import hashlib
import time

# Replace with redis server later if implemented
fake_db = {}
load_dotenv()


def read_document():
    # make this into either config.json or env variable
    url = os.getenv('DOCUMENT_URL')

    try:
        df = pd.read_csv(url)
        return df
    except FileNotFoundError:
        print('File not found')

    return None


def init_checksums(data):
    if data is None:
        return None

    fake_db["document_checksum"] = hashlib.sha256(data.to_string().encode('utf-8')).hexdigest()
    fake_db["rows_checksum"] = data.apply(lambda row: hashlib.sha256(row.to_string().encode('utf-8')).hexdigest(),
                                          axis=1).tolist()


def verify_checksums(data):
    if data is None:
        return None

    # document's checksum have been changed
    if hashlib.sha256(data.to_string().encode('utf-8')).hexdigest() != fake_db["document_checksum"]:
        # checksum of newly fetched data
        rows_checksum = set(data.apply(lambda row: hashlib.sha256(row.to_string().encode('utf-8')).hexdigest(), axis=1))
        changed_data = rows_checksum.difference(set(fake_db["rows_checksum"]))
        removed_data = set(fake_db["rows_checksum"]).difference(rows_checksum)
        print(f"Changed data: {changed_data}, Removed data: {removed_data}")


# Use intersect or difference_update


def main():
    data = read_document()
    # init the fake_db if first time running
    if not fake_db:
        init_checksums(data)
    else:
        verify_checksums(data)
    # print(fake_db)


# Computing time
while True:
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
    time.sleep(5)
