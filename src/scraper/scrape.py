from io import StringIO

import pandas as pd
import numpy as np
import re
import requests
from bs4 import BeautifulSoup

IGNORE_WORDS = {"sup", "nf", "-", "specialization did not exist", ""}
YEAR_RE = re.compile(r"^\d{4}_(DOM|INT)$")
URL = "https://science.ubc.ca/students/historical-bsc-specialization-admission-information"
HEADERS = {'User-Agent': 'Mozilla/5.0'}


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


def scrape():
    #TODO consider changing schema for notes under major
    soup = _get_soup()
    tables = pd.read_html(StringIO(str(soup)), flavor="bs4")

    dfs = [
        _parse_basic(tables[0]),
        _parse_complex(tables[1]),
        _parse_complex(tables[2]),
    ]

    return pd.concat(dfs, ignore_index=True)


if __name__ == "__main__":
    df = scrape()
    print(df)
