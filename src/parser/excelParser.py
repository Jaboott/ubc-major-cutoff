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


def get_major_id(data):
    if pd.isna(data):
        return None

    # regex to detect 4 digits numbers surrounded by ()
    pattern = r'\(([0-9]{4})\)'
    match = re.search(pattern, data)

    if match:
        id = match.group(1)
        return id
    else:
        return None


def get_major_name(data):
    if pd.isna(data):
        return None

    try:
        major_spec = data.split(": ")
        major_name = major_spec[1]
        pattern = r'^(.*?)\s*(?:\((.*?)\))?$'
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


def build_major_stats(data):
    name = get_major_name(data["Spec"])
    # name = None
    id = get_major_id(data["Spec"])
    type = None
    year = data["Year"]
    max_grade = data["Max grade"]
    min_grade = data["Min Grade"]
    initial_reject = data["Inital Reject \nNumber"]
    final_admit = data["Final Admit \nNumber"]

    major_stats = MajorStats(name, id, type, year, max_grade, min_grade, initial_reject, final_admit)

    return major_stats


if __name__ == '__main__':
    df = read_document()
    print(df.head())

    for i in range(df.shape[0]):
        major_stats = build_major_stats(df.iloc[i])
        print(major_stats)
