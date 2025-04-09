import requests
from typing import Dict, Optional
import logging
from collections import defaultdict
from datetime import datetime
import pprint
from collections import defaultdict
#from main_login import AuthenticationManager, client_id, client_secret
from utils.schwab_api_endpoints import SchwabAPIClient




# Main function to execute the script

def main(auth_manager):

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Initialize the SchwabAPIClient with the AuthenticationManager
    api_client = SchwabAPIClient(authentication_manager=auth_manager)

    # Define the symbol you want to query
    symbol = "$SPX"  

    # Configuration for price history request This example is for 30 years. 1 daily candlesticks. 

    default_config_daily_10years = {
        "periodType": "year",
        "period": 20,  # 20 years of data
        "frequencyType": "daily",  # daily candles
        "frequency": 1,  # 1-day bars
        "needExtendedHoursData": False
    }

    price_history = api_client.get_price_history(symbol=symbol, config=default_config_daily_10years)

    # Now you can call the method request_access_token() on the instance
    bearer_token = auth_manager.get_token()
    if bearer_token:
        logging.info("Token is valid, proceeding with data retrieval.")
        ranges_high_low = store_price_pairs_weekly(symbol, price_history)
        print(f"{ranges_high_low}")
        print("\n\n")
    else:
        logging.error("Access token is invalid or has expired.")


def store_price_pairs_weekly(symbol: str, price_history: dict):
    logging.info(f"Storing weekly price pairs for symbol: {symbol}")
    
    data = price_history  # Weekly data retrieval
    
    if data and "candles" in data:
        #weekly_pairs = [(candle["open"], candle["close"], candle["datetime"]) for candle in data["candles"]]
        
        # Extract weekly bullish/bearish data
        monthly_summary = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'total': 0}))  # Init with count, total
        
        for candle in data["candles"]:
            # Unpack the candle data
            open_price = candle["open"]
            close_price = candle["close"]
            timestamp = candle["datetime"]

            date = datetime.fromtimestamp(timestamp / 1000)
            month_name = date.strftime("%B")
            week_number = date.isocalendar()[1]  # Get ISO week number
            
            # Determine if the week is bullish or bearish
            is_bullish = 1 if close_price > open_price else 0
            weekly_data = monthly_summary[month_name][f'Week {week_number}']

            # Track bullish weeks
            weekly_data['count'] += is_bullish
            weekly_data['total'] += 1
        
        # Create final output with percentages and labels using dictionaries instead of tuples
        final_output = {"months": {}}
        month_order = [
            "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"
        ]
        
        for month in month_order:
            if month in monthly_summary:
                weeks_summary = {}
                for week, values in monthly_summary[month].items():
                    total_weeks = values['total']
                    bullish_count = values['count']
                    bullish_percentage = (bullish_count / total_weeks) * 100 if total_weeks > 0 else 0
                    bullish_percentage_str = f"{bullish_percentage:.0f}%"
                    overall_label = "Bullish" if bullish_percentage >= 50 else "Bearish"
                    
                    # Append each week result into the weeks dictionary
                    weeks_summary[week] = {
                        'percentage': bullish_percentage_str,
                        'trend': overall_label
                    }
                
                # Ensure every month has at least 4 weeks, adding a dummy week if the month ends early
                while len(weeks_summary) < 4:
                    weeks_summary[f'Week {len(weeks_summary) + 1}'] = {'percentage': '0%', 'trend': 'Bearish'}
                
                # Append the month with its weeks
                final_output["months"][month] = weeks_summary

        logging.info("Weekly price pairs and month summary stored successfully.")
        
        # Get the current week number and month
        current_date = datetime.now()
        current_week_number = current_date.isocalendar()[1]
        current_month = current_date.strftime("%B")

        # Find the corresponding week data in final_output
        current_week_data = None
        if current_month in final_output["months"]:
            weeks = final_output["months"][current_month]
            for week, data in weeks.items():
                week_num = int(week.split()[-1])  # Extract the week number
                if week_num == current_week_number:
                    current_week_data = {
                        'month': current_month,
                        'week': week,
                        'percentage': data['percentage'],
                        'trend': data['trend']
                    }
                    break
        
        if current_week_data:
            logging.info(f"Current week data: ")
            print("\n\n")
            return current_week_data
        else:
            logging.warning("No data available for the current week.")
            return final_output, None

    else:
        logging.warning("No data available.")
        return {}, None


if __name__ == "__main__":
    #if i want to test only this file just uncomment the auth_manager imports and, add main(auth_manager) it to the function as an arg.
    # auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)
    main()


