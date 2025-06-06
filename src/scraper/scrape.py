from io import StringIO

import pandas as pd
import numpy as np
import re
import requests
from bs4 import BeautifulSoup

from src.parser.excel_parser import get_major_name, get_major_id, get_major_type, convert_nan_to_none
from src.parser.major_stats import MajorStats

IGNORE_WORDS = {"sup", "nf", "-", "specialization did not exist", ""}
YEAR_RE = re.compile(r"^\d{4}_(DOM|INT)$")
URL = "https://science.ubc.ca/students/historical-bsc-specialization-admission-information"
HEADERS = {'User-Agent': 'Mozilla/5.0'}
COLUMNS_MAPPING = {
    "name": 0,
    "type": 0,
    "id": 0,
    "year": 1,
    "min_grade": 3,
    "option": 2,
    "notes": 4
  }


def _get_soup(url=URL):
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return BeautifulSoup(r.text, 'html.parser')
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP {r.status_code}: {r.reason}")
        raise
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Network problem: {e}")
        raise


def _clean(val):
    if pd.isna(val):
        return None
    txt = str(val).strip().lower()
    if txt in IGNORE_WORDS:
        return None
    return float(re.sub(r"[^\d.]", "", txt))


def _parse_basic(df):
    df.columns = df.iloc[0]
    df = df[1:]
    notes = df.pop("Notes").replace("", pd.NA)
    long = df.melt(id_vars="Specialization", var_name="year", value_name="raw")
    return pd.DataFrame({
        "spec": long["Specialization"].str.strip(),
        "year": long["year"],
        "type": "DOM",
        "min_grade": long["raw"].apply(_clean),
        "notes": notes,
    })


def _parse_complex(df):
    columns = []
    for first, second in zip(df.iloc[0], df.iloc[1]):
        if first == second:
            columns.append(first)
        else:
            columns.append(f"{first}_{second}")

    df.columns = columns
    df = df[2:].copy()

    if "Umbrella" in df.columns:
        df.drop(["Umbrella"], axis=1, inplace=True)

    id_cols = [c for c in df.columns if not YEAR_RE.fullmatch(c)]
    val_cols = [c for c in df.columns if YEAR_RE.fullmatch(c)]

    long = df.melt(id_vars=id_cols, value_vars=val_cols,
                   var_name="year_type", value_name="raw")

    return pd.DataFrame({
        "spec": long["Specialization"].str.strip(),
        "year": long["year_type"].map(lambda x: x.split("_")[0]),
        "type": long["year_type"].map(lambda x: x.split("_")[1]),
        "min_grade": long["raw"].apply(_clean),
        "notes": np.nan,
    })


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
        max_grade = None
        min_grade = convert_nan_to_none(data.iloc[COLUMNS_MAPPING["min_grade"]])
        initial_reject = None
        final_admit = None
        domestic = data.iloc[COLUMNS_MAPPING["option"]].lower() == "dom"
        notes = convert_nan_to_none(data.iloc[COLUMNS_MAPPING["notes"]])

        # indicating empty row if major_name is missing
        if name is None or id is None:
            return None

        major_stats = MajorStats(name, id, type, year, max_grade, min_grade, initial_reject, final_admit, domestic, notes)

        return major_stats
    except Exception as e:
        print(e)
        return None


def scrape():
    """
    Scrapes data from UBC Science for major cutoff
    :return: List of major_stats objects
    """
    soup = _get_soup()
    tables = pd.read_html(StringIO(str(soup)), flavor="bs4")

    dfs = [
        _parse_basic(tables[0]),
        _parse_complex(tables[1]),
        _parse_complex(tables[2]),
    ]

    df = pd.concat(dfs, ignore_index=True)
    res = []

    for _, row in df.iterrows():
        major_stats = _build_major_stats(row)

        if major_stats is not None:
            res.append(major_stats)

    return res


if __name__ == '__main__':
    data = scrape()
    for d in data:
        print(d)
