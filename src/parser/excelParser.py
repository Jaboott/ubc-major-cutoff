import json
import logging

from dotenv import load_dotenv

import os
import re
import pandas as pd

from src.parser.major_stats import MajorStats

load_dotenv()


def load_config():
    config_path = "src/parser/config.json"
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


def is_domestic(data):
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


def build_major_stats(data):
    # loading columns mapping and validating keys
    try:
        config = load_config()
        columns = config.get("columns_mapping", {})

        required_keys = ["name", "id", "type", "year", "max_grade", "min_grade", "initial_reject", "final_admit", "option"]

        for key in required_keys:
            if key not in columns:
                raise ValueError(f"Missing required keys in configuration: {key}")
    except Exception as e:
        print(e)
        return None

    name = get_major_name(data.iloc[columns["name"]])
    id = get_major_id(data.iloc[columns["id"]])
    type = get_major_type(data.iloc[columns["type"]])
    year = convert_nan_to_none(data.iloc[columns["year"]])
    max_grade = convert_nan_to_none(data.iloc[columns["max_grade"]])
    min_grade = convert_nan_to_none(data.iloc[columns["min_grade"]])
    initial_reject = convert_nan_to_none(data.iloc[columns["initial_reject"]])
    final_admit = convert_nan_to_none(data.iloc[columns["final_admit"]])
    domestic = is_domestic(data.iloc[columns["option"]])

    # indicating empty row if major_name is missing
    if name is None or id is None:
        return None

    major_stats = MajorStats(name, id, type, year, max_grade, min_grade, initial_reject, final_admit, domestic)

    return major_stats
