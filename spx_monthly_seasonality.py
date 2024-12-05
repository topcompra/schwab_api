import requests
from typing import Dict, Optional
import logging
from collections import defaultdict
from datetime import datetime
#from main_login import AuthenticationManager, client_id, client_secret
from schwab_api_endpoints import SchwabAPIClient
import pprint


# Main function to execute the script
def main(auth_manager):

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize the SchwabAPIClient with the AuthenticationManager
    api_client = SchwabAPIClient(authentication_manager=auth_manager)

    symbol = "$SPX"  # Define the symbol you want to query

    # Configuration for price history request This example is for 3 years. 1 day candlesticks. 

    default_config_monthly_20years = {
        "periodType": "year",
        "period": 20,  # 20 years of data max.
        "frequencyType": "monthly",  # monthly candles
        "frequency": 1,  # 1-month bars
        "needExtendedHoursData": False
    }

    price_history = api_client.get_price_history(symbol=symbol, config=default_config_monthly_20years)


    # Now you can call the method request_access_token() on the instance
    bearer_token = auth_manager.get_token()
    if bearer_token:
        logging.info("Token is valid, proceeding with data retrieval.")
        ranges_high_low = store_price_pairs(symbol, price_history)
        print(f"{ranges_high_low}")
        print("\n\n")       
    else:
        logging.error("Access token is invalid or has expired.")



# Function to store open-close and high-low pairs

def store_price_pairs(symbol: str, price_history: dict):
    logging.info(f"Storing price pairs for symbol: {symbol}")
    
    data = price_history

    if data and "candles" in data:
        open_close_pairs = [(candle["open"], candle["close"], candle["datetime"]) for candle in data["candles"]]
        
        # Extract monthly bullish/bearish data using a dictionary format for fast lookup
        monthly_bull_bear = defaultdict(list)  # Dictionary to store bullish/bearish status per month
        
        # Process each open-close pair
        for open_price, close_price, timestamp in open_close_pairs:
            # Extract the month as a string (e.g., "January", "February")
            month_name = datetime.fromtimestamp(timestamp / 1000).strftime("%B")
            # Determine if the month is bullish or bearish
            is_bullish = 1 if close_price > open_price else 0
            monthly_bull_bear[month_name].append(is_bullish)
        
        # Now calculate the proportion of bullish and bearish months per calendar month
        month_summary = {}
        for month, results in monthly_bull_bear.items():
            total_months = len(results)
            bullish_count = sum(results)  # Count of bullish months
            bearish_count = total_months - bullish_count  # Count of bearish months
            
            # Ensure to avoid division by zero
            if total_months > 0:
                bullish_percentage = (bullish_count / total_months) * 100
            else:
                bullish_percentage = 0
            
            # Create the percentage string
            percentage_str = f"{bullish_percentage:.0f}%"
            
            # Determine the overall label (Bullish or Bearish)
            overall_label = "Bullish" if bullish_percentage >= 50 else "Bearish"

            # Store the month data in dictionary format
            month_summary[month] = {
                'percentage': percentage_str,
                'trend': overall_label
            }

        # Sort the dictionary by month order
        month_order = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        sorted_month_summary = {month: month_summary[month] for month in month_order if month in month_summary}

        # Get the current month
        current_month = datetime.now().strftime("%B")
        current_month_data = sorted_month_summary.get(current_month, None)

        # Format the current month data as per your request
        if current_month_data:
            formatted_current_month_data = {
                "month": current_month,
                "percentage": current_month_data["percentage"],
                "trend": current_month_data["trend"]
            }
        else:
            formatted_current_month_data = {
                "month": current_month,
                "percentage": "N/A",
                "trend": "N/A"
            }

        logging.info(f"Current month data: \n\n\n")
        
        # Return the formatted current month's data and the full month summary
        return formatted_current_month_data

    else:
        logging.warning("No data available.")
        return {}, None

if __name__ == "__main__":
    #if i want to test only this file just uncomment the auth_manager imports and, add main(auth_manager) it to the function as an arg.
    # auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)
    main()
