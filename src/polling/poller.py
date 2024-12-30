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


def create_checksums(data):
    return hashlib.sha256(data.to_string().encode('utf-8')).hexdigest()


def init_checksums(data):
    if data is None:
        return None

    fake_db["document_checksum"] = create_checksums(data)
    fake_db["rows_checksum"] = data.apply(lambda row: create_checksums(row), axis=1).tolist()


# TODO does not update data
# TODO use intersect or difference_update
def verify_checksums(data):
    if data is None:
        return None

    # document's checksum have been changed
    if create_checksums(data) != fake_db["document_checksum"]:
        # checksum of newly fetched data
        rows_checksum = set(data.apply(lambda row: create_checksums(row), axis=1))
        changed_data = rows_checksum.difference(set(fake_db["rows_checksum"]))
        removed_data = set(fake_db["rows_checksum"]).difference(rows_checksum)
        print(f"Changed data: {changed_data}, Removed data: {removed_data}")


def main():
    data = read_document()
    # init the fake_db if first time running
    if not fake_db:
        init_checksums(data)
    else:
        verify_checksums(data)
    # print(fake_db)


if __name__ == '__main__':
    # Computing time
    while True:
        start_time = time.time()
        main()
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(5)
