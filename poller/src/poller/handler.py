from datetime import datetime

from dotenv import load_dotenv

import json, hashlib, time, logging

from src.db.connection import get_connection
from src.parser.excel_parser import parse
from src.scraper.scrape import scrape

load_dotenv()

DB_CONNECTION = get_connection()


def create_checksum(data):
    serialized = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        default=str
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def has_checksum_changed(sheet_data, scrape_data):
    # data is guaranteed to be not None
    try:
        with DB_CONNECTION.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM meta_data;")
            result = cursor.fetchall()
            sheet_checksum = create_checksum(sheet_data)
            scrape_checksum = create_checksum(scrape_data)

            # returns true if table is empty - fresh setup
            if result[0][0] == 0:
                return True

            cursor.execute("SELECT sheet_checksum, scrape_checksum, success FROM meta_data ORDER BY last_updated DESC;")
            db_row = cursor.fetchone()

            if db_row[0] == sheet_checksum and db_row[1] == scrape_checksum and db_row[2]:
                return False

            if db_row[0] != sheet_checksum:
                print("Checksum for sheet have changed")
            elif db_row[1] != scrape_checksum:
                print("Checksum for website have changed")
            else:
                print("Last update has status: failed")

            return True
    except Exception as e:
        print(f'Failed to check for checksum changes with error: {e}')
        return False


def handle_change(sheet_data, scrape_data):
    new_sheet_checksum = create_checksum(sheet_data)
    new_scrape_checksum = create_checksum(scrape_data)
    data = {}
    dt = datetime.now()
    success = True
    print("Re-populating db")

    # for major that appears in both sheet and site, combine them
    for major_stats in sheet_data + scrape_data:
        temp_type = major_stats.type or "Major"
        key = str(major_stats.name + ":" + temp_type + ":" + str(major_stats.year))

        if temp_type in data:
            data[key].merge_with(major_stats)
            print("merged")
        else:
            data[key] = major_stats

    try:
        with DB_CONNECTION.cursor() as cursor:
            # re-populating the db with the new data
            for major_stats in data.values():
                if major_stats.type is None:
                    major_stats.type = "Major"
                try:
                    cursor.execute(
                        """
                        INSERT INTO majors (name, id, type, note)
                        VALUES (%s, %s, %s, %s) 
                        ON CONFLICT (name, type) 
                        DO UPDATE SET 
                            id = EXCLUDED.id,
                            note = EXCLUDED.note
                        RETURNING uid;
                        """,
                        (major_stats.name, major_stats.id, major_stats.type, major_stats.note))

                    uid = cursor.fetchone()[0]
                    cursor.execute(
                        """
                        INSERT INTO admission_statistics 
                        VALUES (%s, %s, %s, %s, %s, %s, %s) 
                        ON CONFLICT (uid, year, domestic) 
                        DO UPDATE SET 
                            max_grade = EXCLUDED.max_grade,
                            min_grade = EXCLUDED.min_grade,
                            initial_reject = EXCLUDED.initial_reject,
                            final_admit = EXCLUDED.final_admit;
                        """,
                        (major_stats.year, major_stats.max_grade, major_stats.min_grade, major_stats.initial_reject,
                         major_stats.final_admit, uid, major_stats.domestic))
                except Exception as e:
                    print(f"Failed to insert {major_stats} to db: {e}")
                    success = False

            if not success:
                DB_CONNECTION.rollback()
                print(f"Failed to populate db")
            else:
                print("Successfully populated db")
            # update the checksum in meta_data
            cursor.execute(
                "INSERT INTO meta_data (sheet_checksum, scrape_checksum, last_updated, success) VALUES(%s, %s, %s, %s);",
                (new_sheet_checksum, new_scrape_checksum, dt, success))
            DB_CONNECTION.commit()
    except Exception as e:
        print(f"Failed to get cursor from connection with error: {e}")

# TODO verify num of rows
def handler(event, context):
    try:
        start_time = time.time()
        sheet_data = parse()
        scrape_data = scrape()

        errors = []
        if sheet_data is None:
            errors.append("sheet_data failed to load")
        if scrape_data is None:
            errors.append("scrape_data failed to load")

        if errors:
            return {
                'status_code': 400,
                'body': {'errors': errors}
            }

        if DB_CONNECTION is None:
            return {
                'status_code': 400,
                'body': {'error': 'Failed to connect to db'}
            }

        if has_checksum_changed(sheet_data, scrape_data):
            handle_change(sheet_data, scrape_data)
            print(f"Populating db took: {str(time.time() - start_time)} milliseconds")
            return {"message": "checksum have changed, db have been updated successfully in " + str(
                time.time() - start_time) + " seconds"}

        print("checksum did not change")
        return {"message": "checksum did not change"}
    except Exception as e:
        logging.error(f"Failed to poll: {e}")
        raise Exception(e)


if __name__ == '__main__':
    handler(None, None)
