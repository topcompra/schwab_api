
import pandas as pd
import logging
from utils import init_api
import sys

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the AuthenticationManager

import logging
import sys
import pandas as pd
from utils import init_api  # Assumes you already defined this

# Define the symbol you want to query
symbol = "$SPX"

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration for 15-minute bars, 180 days
default_config = {
    "periodType": "day",
    "period": 180,
    "frequencyType": "minute",
    "frequency": 15,
    "needExtendedHoursData": True
}

# Function to store price data and save as CSV and XLSX
def store_price_data(symbol, price_history: dict):
    logging.info(f"Storing price data for symbol: {symbol}")
    
    if price_history and "candles" in price_history:
        candles = price_history["candles"]
        df = pd.DataFrame(candles)
        
        # Convert timestamps to readable dates
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

        # Output filenames
        csv_file = f"{symbol}_price_history_15min_180d.csv"
        xlsx_file = f"{symbol}_price_history_15min_180d.xlsx"
        
        # Save to files
        df.to_csv(csv_file, index=False)
        df.to_excel(xlsx_file, index=False)
        
        logging.info(f"✅ Data saved to {csv_file} and {xlsx_file}")
    else:
        logging.warning("⚠️ No candle data available to store.")


if __name__ == "__main__":
    api_client = init_api()

    if api_client is None:
        print("🔒 Authentication failed. Exiting.")
        sys.exit(1)

    # Fetch price history
    price_history = api_client.get_price_history(symbol=symbol, config=default_config)

    # Check token validity before storing
    auth_manager = api_client.authentication_manager
    bearer_token = auth_manager.request_access_token().get("access_token")

    if bearer_token:
        logging.info("✅ Token is valid, proceeding with data retrieval.")
        store_price_data(symbol, price_history)
    else:
        logging.error("❌ Access token is invalid or has expired.")
        sys.exit(1)