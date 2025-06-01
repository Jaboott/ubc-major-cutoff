from io import StringIO

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

IGNORE_WORDS = {"sup", "nf", "-", "specialization did not exist", ""}
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


def _clean(val) -> float | None:
    if pd.isna(val):
        return None
    txt = str(val).strip().lower()
    if txt in IGNORE_WORDS:
        return None
    return float(re.sub(r"[^\d.]", "", txt))


def _parse_basic(df):
    header = df.iloc[0]
    df = df[1:]
    df.columns = header
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
    print(df)
    return pd.DataFrame({})


def scrape():
    # | Spec | Year | Dom | Min Grade | Notes? |
    #TODO consider changing schema for notes under major
    soup = _get_soup()
    tables = pd.read_html(StringIO(str(soup)), flavor="bs4")

    dfs = [
        _parse_basic(tables[0]),
        _parse_complex(tables[1]),
        _parse_complex(tables[2]),
    ]

    # print(dfs[0])


if __name__ == "__main__":
    scrape()
