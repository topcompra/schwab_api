
import pandas as pd
import logging
from main_login import AuthenticationManager, client_id, client_secret
from schwab_api_endpoints import SchwabAPIClient


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the AuthenticationManager
auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)

# Initialize the SchwabAPIClient with the AuthenticationManager
api_client = SchwabAPIClient(authentication_manager=auth_manager)

# Define the symbol you want to query
symbol = "$SPX" 
'''
default_config = {
    "periodType": "year",
    "period": 20,  # 20 years of data
    "frequencyType": "daily",  # weekly candles its weekly, naming is just to not make more files.
    "frequency": 1,  # 1-week bars
    "needExtendedHoursData": False
}
'''

default_config = {
    "periodType": "day",
    "period": 180,
    "frequencyType": "minute",
    "frequency": 15,
    "needExtendedHoursData": True
}

price_history = api_client.get_price_history(symbol=symbol, config=default_config)

# Function to store price data and save as CSV and XLSX
def store_price_data(symbol, price_history: dict):
    logging.info(f"Storing price data for symbol: {symbol}")
    
    data = price_history
    
    if data and "candles" in data:
        # Extract price data into a DataFrame
        candles = data["candles"]
        df = pd.DataFrame(candles)
        
        # Convert timestamp to a readable date
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

        # Save data to CSV and XLSX
        csv_file = f"{symbol}_price_history_15min_180d.csv"
        xlsx_file = f"{symbol}_price_history_weekly_15min_180d.xlsx"
        
        df.to_csv(csv_file, index=False)
        df.to_excel(xlsx_file, index=False)
        
        logging.info(f"Data saved successfully as {csv_file} and {xlsx_file}.")
    else:
        logging.warning("No data available.")



# Main function to execute the script
def main(auth_manager: AuthenticationManager):


    # Initialize the SchwabAPIClient with the AuthenticationManager
    api_client = SchwabAPIClient(authentication_manager=auth_manager)

    # Define the symbol you want to query
    symbol = "$SPX" 

    default_config = {
        "periodType": "year",
        "period": 20,  # 20 years of data
        "frequencyType": "weekly",  # weekly candles its weekly, naming is just to not make more files.
        "frequency": 1,  # 1-week bars
        "needExtendedHoursData": False
    }

    price_history = api_client.get_price_history(symbol=symbol, config=default_config)
    # Now you can call the method request_access_token() on the instance
    bearer_token = auth_manager.request_access_token()["access_token"]
    if bearer_token:
        logging.info("Token is valid, proceeding with data retrieval.")
        store_price_data(symbol, price_history)
    else:
        logging.error("Access token is invalid or has expired.")

if __name__ == "__main__":
    auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)
    main(auth_manager)
