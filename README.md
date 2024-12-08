# How to Use - Schwab OAuth2

## Retrieves price_history as a python dictionary

Note: there has to be a great library out there but i, unfortunately did not find it this straight-forward to use.


Follow these instructions to get etfs and ticker data from schwab under this format: 

```
price_history = {
    "candles": [
        {"open": 100.5, "close": 102.3, "high": 103.0, "low": 100.0},
        {"open": 102.3, "close": 101.8, "high": 103.5, "low": 101.0},
        {"open": 101.8, "close": 104.0, "high": 104.5, "low": 101.5},
        # More candles can follow...
    ]
}
```


## Step 1: Fork the Project

Navigate to the project's repository on GitHub.

Click the "Fork" button in the top-right corner to create a personal copy of the repository in your GitHub account.


## Step 2: Clone the Repository Locally

### Open your terminal or command prompt.

### Clone the repository to your local machine using the following command:

BASH

git clone https://github.com/yourusername/your-repo-name.git


### Navigate into the cloned directory:

BASH

cd your-repo-name


## Step 3: Set Up the Virtual Environment

### Create a new directory for your virtual environment:

BASH

mkdir .venv

### Create a virtual environment within this directory:

BASH

python -m venv .venv

## Step 4: Configure Environment Variables

Within the .venv directory, create a file to store your environment variables ideally called .env if you do not want to overwrite anything. 

### Add the following variables to the file:

client_id=your_client_id
client_secret=your_client_secret
callback_url=your_callback_url
Step 5: Install Requirements

### Activate your virtual environment:

On Windows:

BASH

.venv\Scripts\activate

On macOS/Linux:

BASH

source .venv/bin/activate

### Install the required packages using the requirements.txt file:

BASH

pip install -r requirements.txt


## Step 6: Run the Main Script

### Execute the main script to display data in the command line(to check if everything works):

BASH

python main_daily_checker.py

This will output the data as a dictionary in the command line.


## Step 7: Customize Configuration

### Each file in the project has a similar structure where you can find and modify the following variables:
```
Python

symbol = "$SPX"

default_config = {
    "periodType": "day",
    "period": 180,
    "frequencyType": "minute",
    "frequency": 15,
    "needExtendedHoursData": True
}
```

Update these variables with your desired timeframes and symbols/tickers. To execute any file just cd to the project_folder you forked and just (example: in cmd: py daily_main_checker.py) will execute the files. 

## Last Step: Extract Data for Personal Use

### To extract data for your personal use using the provided code snippets, follow these steps:

Create a file in the same project_folder where daily_main_checker.py is and copy-paste the following code snippet: 

Python

```
from main_login import AuthenticationManager, client_id, client_secret
from schwab_api_endpoints import SchwabAPIClient

def main(auth_manager: AuthenticationManager):
    # Initialize the SchwabAPIClient with the AuthenticationManager
    api_client = SchwabAPIClient(authentication_manager=auth_manager)

    # Define the symbol you want to query
    symbol = "$SPX"

    default_config = {
        "periodType": "year",
        "period": 20,  # 20 years of data
        "frequencyType": "weekly",  # weekly candles
        "frequency": 1,  # 1-week bars
        "needExtendedHoursData": False
    }

    # Extract price history data
    price_history = api_client.get_price_history(symbol=symbol, config=default_config)
    
    # Request an access token
    bearer_token = auth_manager.request_access_token()["access_token"]
    if bearer_token:
        logging.info("Token is valid, proceeding with data retrieval.")
        store_price_data(symbol, price_history)
    else:
        logging.error("Access token is invalid or has expired.")
if __name__ == "__main__":
    auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)
    main(auth_manager)

Python
```

Where the price_history variable will contain data in the following format for you to use:

Python

```

price_history = {
    "candles": [
        {"open": 100.5, "close": 102.3, "high": 103.0, "low": 100.0},
        {"open": 102.3, "close": 101.8, "high": 103.5, "low": 101.0},
        {"open": 101.8, "close": 104.0, "high": 104.5, "low": 101.5},
        # More candles can follow...
    ]
}
```

## Contact
### Francisco Gonzalez - fjgazocar@gmail.com
#### https://topcompra.github.io/fjgazocar/




Note:
Authentication and data cleaning are already handled within the provided code.








Feel free to ignore as this section is for my personal use to have ready in hand:


…or create a new repository on the command line

echo "# schwab_api" >> README.md

git init

git add README.md

git commit -m "first commit"

git branch -M main

git remote add origin https://github.com/topcompra/schwab_api.git

git push -u origin main

…or push an existing repository from the command line

git remote add origin https://github.com/topcompra/schwab_api.git

git branch -M main

git push -u origin main
