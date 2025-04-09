# What you will get:

Feel free to use or extend as you wish.


price_history will be a dict. looking like this:

```
price_history = {
                  "candles": [
                    {
                      "open": 2098.27,
                      "high": 2109.98,
                      "low": 2091.05,
                      "close": 2107.96,
                      "volume": 0,
                      "datetime": 1429678800000
                    },
                    ...
                  ],
                  "empty": false,
                  "symbol": "$SPX",
                  "type": "price"
              }

```
or candles as a list[dict] like this:
```
candles = [
    {
      "open": 2098.27,
      "high": 2109.98,
      "low": 2091.05,
      "close": 2107.96,
      "volume": 0,
      "datetime": 1429678800000
    },
    {
      "open": 2028.27,
      "high": 2059.98,
      "low": 2091.05,
      "close": 2107.96,
      "volume": 0,
      "datetime": 1429678800000
    }
    ...
  ]


```
#  Usage:

### 1. Create .env in root project_folder and add
```
  client_id = "" # your cient_id found in
  client_secret = "" # your secret_key 
```

### 2. Create a new file in `engine/`, for example ( this snippet can be found in engine/base_template.py):

#### * Refer to default_config_examples.txt for examples on how to customize CONFIG to other timeframes.

```bash
from utils.init_api import init_api

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

    price_history = client.get_price_history(SYMBOL, CONFIG)
    candles = price_history.get("candles", [])
    print(f"Loaded {len(candles)} candles for {SYMBOL}")

    # === Your custom logic below ===
    # process_price_history(candles)
    # analyze_structure(price_history)
    # plot_results(candles)
    # ...

if __name__ == "__main__":
    main()
```

# the only folders that matter to keep this working are core and utils.

## run script at root (project_folder)

python -m engine_or_any_folder_you_want.my_script
