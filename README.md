# Crypto Price Tracker

A simple, beginner-friendly Python command-line app to track cryptocurrency prices in your terminal.
It shows price changes with arrows, saves price history to a CSV file, and handles API errors gracefully.

---

## Features

- **Track multiple coins** using CoinGecko IDs (e.g. `bitcoin`, `ethereum`, `dogecoin`).
- **Price change indicators**: `↑` when price increases, `↓` when price decreases, space when unchanged or no previous data.
- **CLI arguments** so users can choose:
  - which coins to track
  - how often to refresh
  - where to save the CSV history
- **Price history saved to CSV** (`prices.csv` by default).
- **Graceful API error handling** with simple retries and clear messages.
- **Clean terminal dashboard** that refreshes each interval.

---

## Installation

1. **Clone or download** this project into a folder called `crypto-price-tracker`.

2. Open a terminal in the project folder:

   ```bash
   cd crypto-price-tracker
   ```

3. (Optional but recommended) Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   # source .venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the tracker from the project directory:

```bash
python tracker.py
```

You can customize which coins to track, the refresh interval, and the CSV file path using arguments:

```bash
python tracker.py --coins bitcoin,ethereum,solana --interval 15 --csv my_prices.csv
```

- **`--coins`**: comma-separated CoinGecko IDs of coins to track
  - Default: `bitcoin,ethereum,dogecoin`
- **`--interval`**: refresh interval in seconds
  - Default: `30`
- **`--csv`**: path to the CSV file where price history is saved
  - Default: `prices.csv`

Press **Ctrl+C** to stop the tracker.

---

## Example Output

Example of what you might see in the terminal:

```text
Crypto Price Tracker
----------------------------------------
Coin           Price (USD)        Change
----------------------------------------
bitcoin            67500.1234      ↑
dogecoin               0.1500      ↓
ethereum            3500.0000
----------------------------------------
Press Ctrl+C to exit.
```

Corresponding lines in `prices.csv` will look like:

```text
timestamp,coin,price
2026-03-07 12:00:00,bitcoin,67500.1234
2026-03-07 12:00:00,ethereum,3500.0
2026-03-07 12:00:00,dogecoin,0.15
```

---

## Notes

- Prices are fetched from the public CoinGecko API (`/simple/price` endpoint).
- Make sure your internet connection is working when you run the tracker.
- If the API fails temporarily, the app will retry a few times and display an error message before trying again on the next interval.
