from collections import defaultdict
from datetime import datetime
import logging
#from main_login import AuthenticationManager, client_id, client_secret
from schwab_api_endpoints import SchwabAPIClient
import logging
import pprint



# Main function to execute the script
def main(auth_manager):

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


    # Initialize the SchwabAPIClient with the AuthenticationManager
    api_client = SchwabAPIClient(authentication_manager=auth_manager)


    symbol = "$SPX"  # Define the symbol you want to query

    # Configuration for price history request This example is for 3 years. 1 day candlesticks. 

    default_config_monthly_5years = {
        "periodType": "year",
        "period": 15,  # 20 years of data max.
        "frequencyType": "daily",  # monthly candles
        "frequency": 1,  # 1-month bars
        "needExtendedHoursData": False
    }

    price_history = api_client.get_price_history(symbol=symbol, config=default_config_monthly_5years)


    # Now you can call the method request_access_token() on the instance
    bearer_token = auth_manager.get_token()
    if bearer_token:
        logging.info("Token is valid, proceeding with data retrieval.")
        current_day = store_price_pairs_daily_seasonality(symbol, price_history)
        print(current_day)
        print('\n\n')
        #call the function contained in this file.
    else:
        logging.error("Access token is invalid or has expired.")


def store_price_pairs_daily_seasonality(symbol: str, price_history: dict):
    logging.info(f"Storing daily price pairs for symbol: {symbol}")
    
    data = price_history  # Daily data retrieval
    
    if data and "candles" in data:
        # Extract daily bullish/bearish data
        monthly_summary = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {'count': 0, 'total': 0})))  # Init with count, total
        
        for candle in data["candles"]:
            # Unpack the candle data
            open_price = candle["open"]
            close_price = candle["close"]
            timestamp = candle["datetime"]

            # Parse the timestamp to get date components
            date = datetime.fromtimestamp(timestamp / 1000)
            month_name = date.strftime("%B")
            week_number = date.isocalendar()[1]  # ISO week number
            day_of_week = date.strftime("%A")  # Day of the week
            
            # Determine if the day is bullish or bearish
            is_bullish = 1 if close_price > open_price else 0
            daily_data = monthly_summary[month_name][f'Week {week_number}'][day_of_week]

            # Track bullish days
            daily_data['count'] += is_bullish
            daily_data['total'] += 1
        
        # Create final output with percentages and labels using dictionaries instead of tuples
        final_output = {"months": {}}
        month_order = [
            "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"
        ]
        
        for month in month_order:
            if month in monthly_summary:
                weeks_summary = {}
                for week, days in monthly_summary[month].items():
                    days_summary = {}
                    for day, values in days.items():
                        total_days = values['total']
                        bullish_count = values['count']
                        bullish_percentage = (bullish_count / total_days) * 100 if total_days > 0 else 0
                        bullish_percentage_str = f"{bullish_percentage:.0f}%"
                        overall_label = "Bullish" if bullish_percentage >= 50 else "Bearish"
                        
                        # Append each day result into the days dictionary
                        days_summary[day] = {
                            'percentage': bullish_percentage_str,
                            'trend': overall_label
                        }
                    
                    # Append the week with its days
                    weeks_summary[week] = days_summary
                
                # Append the month with its weeks
                final_output["months"][month] = weeks_summary

        logging.info("Daily seasonality data stored successfully.")
        
        # Get the current date details
        current_date = datetime.now()
        current_day_of_week = current_date.strftime("%A")
        current_week_number = current_date.isocalendar()[1]
        current_month = current_date.strftime("%B")

        # Check if it's the weekend
        if current_day_of_week in ["Saturday", "Sunday"]:
            logging.info("It's the weekend. No trading data available.")
            return 
        
        # Find the corresponding day data in final_output
        current_day_data = None
        if current_month in final_output["months"]:
            weeks = final_output["months"][current_month]
            for week, days in weeks.items():
                week_num = int(week.split()[-1])  # Extract the week number
                if week_num == current_week_number and current_day_of_week in days:
                    current_day_data = {
                        'month': current_month,
                        'week': week,
                        'day': current_day_of_week,
                        'percentage': days[current_day_of_week]['percentage'],
                        'trend': days[current_day_of_week]['trend']
                    }
                    break
        
        if current_day_data:
            logging.info(f"Current day data: ")
            print("\n\n")
            return current_day_data
        else:
            logging.warning("No data available for the current day.")
            return final_output, None

    else:
        logging.warning("No data available.")
        return {}, None


if __name__ == "__main__":
    #if i want to test only this file just uncomment the auth_manager imports and, add main(auth_manager) it to the function as an arg.
    # auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)
    main()
