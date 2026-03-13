import csv
import logging
import os
import time
from typing import Dict, Tuple

import requests

LOG_FILE = "tracker.log"
logger = logging.getLogger("crypto_tracker")


def setup_logging(log_file: str = LOG_FILE) -> None:
    """Configure logging to tracker.log. Call once at startup."""
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    )
    logger.addHandler(fh)


def clear_screen() -> None:
    """Clear the terminal screen in a cross-platform way."""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def fetch_prices_with_retry(
    url: str,
    params: Dict[str, str],
    retries: int = 3,
    delay_seconds: int = 5,
) -> Tuple[bool, Dict]:
    """
    Fetch prices from the API with simple retry logic.

    Returns (success, data_or_error_message).
    """
    last_error: str = ""

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            logger.info("API request success")
            return True, response.json()
        except requests.RequestException as exc:
            last_error = str(exc)
            logger.error("API error: %s", last_error)
            time.sleep(delay_seconds)

    return False, last_error


def save_prices_to_csv(
    filename: str,
    timestamp: str,
    prices: Dict[str, float],
) -> None:
    """
    Append the current prices to a CSV file.

    The file will have columns: timestamp, coin, price.
    """
    file_exists = os.path.exists(filename)

    # Make sure the directory exists (if a path is provided)
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(filename, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Write header once if the file is new
        if not file_exists:
            writer.writerow(["timestamp", "coin", "price"])

        for coin, price in prices.items():
            writer.writerow([timestamp, coin, price])
    logger.info("Price updated")

