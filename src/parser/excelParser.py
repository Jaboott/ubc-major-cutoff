import json

from dotenv import load_dotenv

import os
import re
import pandas as pd

from src.parser.major_stats import MajorStats

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


def load_config():
    path = "src/parser/config.json"

    try:
        with open(path, "r") as file:
            config = json.load(file)
            return config
    except FileNotFoundError:
        raise ValueError("Configuration file not found at 'src/parser/config.json'.")
    except:
        raise ValueError("Configuration file is not a valid JSON.")


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
        major_type = match.group(1).strip()
        return major_type
    else:
        return None


def build_major_stats(data):
    # loading columns mapping and validating keys
    try:
        config = load_config()
        columns = config.get("columns_mapping", {})

        required_keys = ["name", "id", "type", "year", "max_grade", "min_grade", "initial_reject", "final_admit"]

        for key in required_keys:
            if key not in columns:
                raise ValueError(f"Missing required keys in configuration: {key}")
    except Exception as e:
        print(e)
        return None

    name = get_major_name(data.iloc[columns["name"]])
    id = get_major_id(data.iloc[columns["id"]])
    type = get_major_type(data.iloc[columns["type"]])
    year = data.iloc[columns["year"]]
    max_grade = data.iloc[columns["max_grade"]]
    min_grade = data.iloc[columns["min_grade"]]
    initial_reject = data.iloc[columns["initial_reject"]]
    final_admit = data.iloc[columns["final_admit"]]

    # indicating empty row if major_name is missing
    if name is None:
        return None

    major_stats = MajorStats(name, id, type, year, max_grade, min_grade, initial_reject, final_admit)

    return major_stats


if __name__ == '__main__':
    df = read_document()
    print(df.head())

    data = []

    for i in range(df.shape[0]):
        major_stats = build_major_stats(df.iloc[i])
        if major_stats is not None:
            print(major_stats)
            data.append(major_stats)
