# What you will get:

Feel free to use or extend as you wish.


price_history will be a dict. looking like this:

candles as a list[dict] like this:
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
  client_id = "" # your cient_id 
  client_secret = "" # your secret_key 
```

### 2. Create a new file in `engine/`, for example ( this snippet can be found in engine/base_template.py):
## Install requirements.txt

#### * Refer to default_config_examples.txt for examples on how to customize CONFIG to other timeframes.

```bash

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

"you can go to config folder settings.py and update symbol and config or pass them as variables to 
fetch_price_history(symbol = "EXMPL", config  = payload_example)"

payload_example = {
    "periodType": "year",
    "period": 5,
    "frequencyType": "monthly",
    "frequency": 1,
    "needExtendedHoursData": False
}


```

to run try py main.py which contains only that code snippet.

# the only folders that matter to keep this working are core and utils.

## run script at root (project_folder)

python -m engine_or_any_folder_you_want.my_script or to try the code snippet run py main.py in root dir.



