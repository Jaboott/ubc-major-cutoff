import json
import logging

from dotenv import load_dotenv

import os
import re
import pandas as pd

from src.parser.major_stats import MajorStats

load_dotenv()

COLUMNS_MAPPING = {
    "name": 2,
    "type": 2,
    "id": 2,
    "year": 0,
    "max_grade": 7,
    "min_grade": 8,
    "initial_reject": 5,
    "final_admit": 6,
    "option": 1
  }


def load_config():
    config_path = "src/config.json"
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at {config_path}")

    try:
        with open(config_path, "r") as file:
            config = json.load(file)
            return config
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError: {e}")
    except Exception as e:
        logging.error(e)


def get_major_id(data):
    if pd.isna(data):
        return None

    # regex to detect 4 digits numbers surrounded by ()
    pattern = r'\(([0-9]{4})\)'
    match = re.search(pattern, data)

    if match:
        id = match.group(1).strip()
        return id
    else:
        return None


def get_major_name(data):
    if pd.isna(data):
        return None

    try:
        major_spec = data.split(": ")
        major_name = major_spec[1]
        pattern = r'^(.*?)(?:\s*\(.*)?$'
    except:
        # regex to get the string containing the major name, also get the string that's surrounded by brackets
        pattern = r'^(?:Major|Combined Major|Honours|Combined Honours|)(?: \(\d+\))?[: ]?\s*([^()]+)'
        major_name = data

    match = re.match(pattern, major_name)

    if match:
        name = match.group(1).strip()
        return name
    else:
        return None


def get_major_type(data):
    if pd.isna(data):
        return None

    pattern = r'\b(Major|Combined Major|Honours|Combined Honours)\b'
    match = re.search(pattern, data)

    if match:
        # replace space with _
        major_type = match.group(1).strip().replace(" ", "_")
        return major_type
    else:
        return None


def _is_domestic(data):
    if pd.isna(data):
        return None

    # regex to see if string include "Excluding ... Domestic"
    pattern = r'\bExcluding\b.*\bDomestic\b'
    match = re.search(pattern, data)

    if match:
        return False

    return True


def convert_nan_to_none(value):
    if pd.isna(value):
        return None

    return value


def _build_major_stats(data):
    """
    Cleans the input data then returns an object of MajorStats
    :param data: A row of a data frame with major cutoff
    :return: A MajorStats object
    """
    try:
        name = get_major_name(data.iloc[COLUMNS_MAPPING["name"]])
        id = get_major_id(data.iloc[COLUMNS_MAPPING["id"]])
        type = get_major_type(data.iloc[COLUMNS_MAPPING["type"]])
        year = convert_nan_to_none(data.iloc[COLUMNS_MAPPING["year"]])
        max_grade = convert_nan_to_none(data.iloc[COLUMNS_MAPPING["max_grade"]])
        min_grade = convert_nan_to_none(data.iloc[COLUMNS_MAPPING["min_grade"]])
        initial_reject = convert_nan_to_none(data.iloc[COLUMNS_MAPPING["initial_reject"]])
        final_admit = convert_nan_to_none(data.iloc[COLUMNS_MAPPING["final_admit"]])
        domestic = _is_domestic(data.iloc[COLUMNS_MAPPING["option"]])

        # indicating empty row if major_name is missing
        if name is None or id is None:
            return None

        major_stats = MajorStats(name, id, type, year, max_grade, min_grade, initial_reject, final_admit, domestic)

        return major_stats
    except Exception as e:
        logging.error(e)
        return None


def parse():
    """
    Reads the major cutoff Excel file then cleans + parses the data
    :return: List of major_stats objects
    """
    url = os.getenv('DOCUMENT_URL')
    if url is None:
        print(f'env variable DOCUMENT_URL must be set to the url of major cutoff file')
        return None

    df = pd.read_csv(url)
    res = []

    for _, row in df.iterrows():
        major_stats = _build_major_stats(row)

        if major_stats is not None:
            res.append(major_stats)

    return res


if __name__ == '__main__':
    data = parse()
    for d in data:
        print(d)
