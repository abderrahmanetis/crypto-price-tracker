import time
import requests

url = "https://api.coingecko.com/api/v3/simple/price"

# List the coins you want to track by their CoinGecko IDs
coins = ["bitcoin", "ethereum", "dogecoin"]

# Simple alert thresholds per coin (edit these)
# If the current price is >= target, an alert will be printed.
alerts = {
    "bitcoin": 70000,   # example target price in USD
    "ethereum": 4000,
    "dogecoin": 0.5,
}

while True:
    params = {
        "ids": ",".join(coins),
        "vs_currencies": "usd",
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("\n--- Latest Prices ---")
    for coin in coins:
        # Each entry looks like: {"bitcoin": {"usd": 12345.67}, ...}
        price = data.get(coin, {}).get("usd")
        if price is not None:
            print(f"The price of {coin.capitalize()} is {price} USD")

            target = alerts.get(coin)
            if target is not None and price >= target:
                print(f"*** ALERT: {coin.capitalize()} has reached {price} USD (target {target} USD) ***")
        else:
            print(f"No price data available for {coin}")

    # Wait 30 seconds before refreshing
    time.sleep(30)