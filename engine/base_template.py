from utils.init_api import init_api

from utils.fetch import fetch_price_history

def main():
    candles = fetch_price_history()
    if not candles:
        return

    # === Your logic below ===
    # analyze_structure(candles)
    # plot_chart(candles)

if __name__ == "__main__":
    main()