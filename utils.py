import csv
import os
import time
from typing import Dict, Tuple

import requests


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
            return True, response.json()
        except requests.RequestException as exc:
            last_error = str(exc)
            # Wait a bit before trying again
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

