from utils.init_api import init_api

# === Config ===
SYMBOL = "$SPX"
CONFIG = {
    "periodType": "year",
    "period": 10,
    "frequencyType": "daily",
    "frequency": 1,
    "needExtendedHoursData": False
}


def main():
    client = init_api()
    if not client:
        return

    # === API Call ===
    price_history = client.get_price_history(SYMBOL, CONFIG)
    candles = price_history.get("candles", [])

    # === Your custom logic below ===
    # process_price_history(candles)
    # analyze_structure(price_history)
    # calculate_seasonality(price_history)
    # ...


if __name__ == "__main__":
    main()