from utils.init_api import init_api
from config.settings import SYMBOL, CONFIG

def main():
    candles = fetch_price_history()
    if not candles:
        return

    # === Your custom logic below ===
    # process_price_history(candles)
    # analyze_structure(candles)
    # plot_chart(candles)

def fetch_price_history():
    client = init_api()
    if not client:
        return None

    price_history = client.get_price_history(SYMBOL, CONFIG)
    return price_history.get("candles", [])

if __name__ == "__main__":
    main()