import argparse
import time
from typing import Dict, List, Tuple

from utils import (
    clear_screen,
    fetch_prices_with_retry,
    save_prices_to_csv,
    setup_logging,
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for the tracker CLI."""
    parser = argparse.ArgumentParser(
        description="Track cryptocurrency prices in the terminal."
    )

    parser.add_argument(
        "--coins",
        type=str,
        default="bitcoin,ethereum,dogecoin",
        help=(
            "Comma-separated list of CoinGecko IDs to track "
            "(e.g. bitcoin,ethereum,solana). "
            "Default: bitcoin,ethereum,dogecoin"
        ),
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Refresh interval in seconds (default: 30).",
    )

    parser.add_argument(
        "--csv",
        type=str,
        default="prices.csv",
        help="Path to the CSV file for saving price history (default: prices.csv).",
    )

    return parser.parse_args()


def parse_coins(raw: str) -> List[str]:
    """Turn a comma-separated string into a clean list of coin IDs."""
    coins = [c.strip().lower() for c in raw.split(",") if c.strip()]
    if not coins:
        coins = ["bitcoin", "ethereum", "dogecoin"]
    return coins


def build_dashboard(
    prices: Dict[str, float],
    previous_prices: Dict[str, float],
) -> str:
    """Return a formatted dashboard string for the terminal."""
    lines: List[str] = []
    lines.append("Crypto Price Tracker")
    lines.append("-" * 40)
    lines.append(f"{'Coin':<12} {'Price (USD)':>15}  Change")
    lines.append("-" * 40)

    for coin in sorted(prices.keys()):
        price = prices[coin]
        prev_price = previous_prices.get(coin)

        if prev_price is None:
            indicator = " "
        elif price > prev_price:
            indicator = "↑"
        elif price < prev_price:
            indicator = "↓"
        else:
            indicator = " "

        lines.append(f"{coin:<12} {price:>15.4f}  {indicator}")

    lines.append("-" * 40)
    lines.append("Press Ctrl+C to exit.")
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    coins = parse_coins(args.coins)
    setup_logging()

    url = "https://api.coingecko.com/api/v3/simple/price"
    previous_prices: Dict[str, float] = {}

    while True:
        params = {
            "ids": ",".join(coins),
            "vs_currencies": "usd",
        }

        success, prices_or_error = fetch_prices_with_retry(
            url=url,
            params=params,
            retries=3,
            delay_seconds=5,
        )

        if not success:
            clear_screen()
            print("Crypto Price Tracker")
            print("-" * 40)
            print("Error fetching prices after multiple attempts.")
            print(f"Last error: {prices_or_error}")
            print("-" * 40)
            print("Retrying in a few seconds... (Press Ctrl+C to exit)")
            time.sleep(args.interval)
            continue

        # prices_or_error is a dict like {"bitcoin": {"usd": 12345.67}, ...}
        data: Dict[str, Dict[str, float]] = prices_or_error
        current_prices: Dict[str, float] = {}

        for coin in coins:
            current_price = data.get(coin, {}).get("usd")
            if current_price is not None:
                current_prices[coin] = float(current_price)

        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        save_prices_to_csv(args.csv, timestamp, current_prices)

        clear_screen()
        print(build_dashboard(current_prices, previous_prices))

        previous_prices = current_prices
        time.sleep(args.interval)


if __name__ == "__main__":
    main()