import time
import requests

url = "https://api.coingecko.com/api/v3/simple/price"

# Let the user choose which coins to track (CoinGecko IDs, e.g. bitcoin, ethereum, solana)
coin_input = input("Enter coins to track (comma-separated, e.g. bitcoin,ethereum,dogecoin): ")
coins = [c.strip().lower() for c in coin_input.split(",") if c.strip()]
if not coins:
    coins = ["bitcoin", "ethereum", "dogecoin"]
    print("Using defaults: bitcoin, ethereum, dogecoin")

# Optional: set alert targets (format: coin:price, e.g. bitcoin:70000,ethereum:4000)
alert_input = input("Enter alert targets (coin:price, comma-separated) or press Enter to skip: ")
alerts = {}
for part in alert_input.split(","):
    part = part.strip()
    if ":" in part:
        coin_id, target_str = part.split(":", 1)
        coin_id = coin_id.strip().lower()
        try:
            alerts[coin_id] = float(target_str.strip())
        except ValueError:
            pass

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