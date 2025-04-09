from .init_api import init_api

def fetch_price_history(symbol=None, config=None):
    from config.settings import SYMBOL, CONFIG

    symbol = symbol or SYMBOL
    config = config or CONFIG

    client = init_api()
    if not client:
        return None

    price_history = client.get_price_history(symbol, config)
    return price_history.get("candles", [])