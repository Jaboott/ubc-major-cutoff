import requests
import logging
import os
import json
from bs4 import BeautifulSoup


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


def scrape():
    try:
        config = load_config()
        URL = config.get("url", "https://science.ubc.ca/students/historical-bsc-specialization-admission-information")
        page = requests.get(URL)

        soup = BeautifulSoup(page.content, "html.parser")
        print(soup.prettify())

    except Exception as e:
        logging.error(e)
        return None

scrape()

