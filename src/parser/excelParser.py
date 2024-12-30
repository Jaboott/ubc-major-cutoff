from dotenv import load_dotenv

import os
import pandas as pd

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


if __name__ == '__main__':
    df = read_document()
    print(df.head())

