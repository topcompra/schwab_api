import requests
import numpy as np
from typing import Dict, Optional
import plotly.express as px
import pandas as pd
import logging
from main_login import AuthenticationManager, client_id, client_secret
from schwab_api_endpoints import SchwabAPIClient


def main():

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize the AuthenticationManager
    auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)

    # Initialize the SchwabAPIClient with the AuthenticationManager
    api_client = SchwabAPIClient(authentication_manager=auth_manager)

    # Define the symbol you want to query
    symbol = "$SPX"  

    # Configuration for price history request This example is for 30 years. 1 daily candlesticks. 


    default_config_daily_10years = {
        "periodType": "year",
        "period": 10,  # 30 years of data
        "frequencyType": "daily",  # daily candles
        "frequency": 1,  # 1-day bars
        "needExtendedHoursData": False
    }

    price_history = api_client.get_price_history(symbol=symbol, config=default_config_daily_10years)

    if auth_manager.get_token() and auth_manager.is_token_valid():
        logging.info("Token is valid, proceeding with data retrieval.")
        ranges_high_low, ranges_open_close = store_price_pairs(symbol, price_history)
        if ranges_high_low and ranges_open_close:
            calculate_std_and_plot(ranges_high_low, f'{symbol} Price Range (High - Low)')
            calculate_std_and_plot(ranges_open_close, f'{symbol} Price Range (Open - Close)')
            logging.info("Data retrieval and plotting complete.")
        else:
            logging.warning("No ranges available to plot.")
    else:
        logging.error("Access token is invalid or has expired.")



# Function to store open-close and high-low pairs
def store_price_pairs(symbol: str, price_history: dict):
    logging.info(f"Storing price pairs for symbol: {symbol}")
    
    data = price_history
    
    if data and "candles" in data:
        open_close_pairs, high_low_pairs = [], []
        for candle in data["candles"]:
            open_close_pairs.append((candle["open"], candle["close"]))
            high_low_pairs.append((candle["high"], candle["low"]))
        
        ranges = [(high - low) for high, low in high_low_pairs]
        ranges_open_close = [(close - open) for open, close in open_close_pairs]

        logging.info("Price pairs stored successfully.")
        logging.info(f"total de dias es {len(ranges)}")
        return ranges, ranges_open_close
    else:
        logging.warning("No data available.")
        return []

# Function to calculate std and plot the ranges
def calculate_std_and_plot(ranges, dataset_label):
    logging.info(f"Calculating standard deviation for {dataset_label}.")
    
    mean_range = np.mean(ranges)
    std_range = np.std(ranges)

    sigma_1 = mean_range + std_range
    sigma_2 = mean_range + 2 * std_range

    df = pd.DataFrame({'ranges': ranges})

    # Debugging: Check range stats
    logging.info(f"Min: {min(ranges)}, Max: {max(ranges)}, Mean: {mean_range}, Std: {std_range}")
    
    fig = px.histogram(df, x='ranges', nbins=20, title=f"STDistribution_comp. of {dataset_label}",
                       color_discrete_sequence=['#1f77b4'])

    counts, bins = np.histogram(ranges, bins=20)
    total_counts = len(ranges)

    # Debugging: Check bins and counts
    print(f"Bins: {bins}")
    print(f"Counts: {counts}")
    print(f"Total days: {total_counts}, Total counts sum: {sum(counts)}")

    hover_text = []
    labels = []  
    for i, count in enumerate(counts):
        percentage = (count / total_counts) * 100
        bin_range = f'{bins[i]:.2f} - {bins[i+1]:.2f}'
        hover_text.append(f'Count: {count}<br>Percentage: {percentage:.1f}%<br>Range: {bin_range}')
        labels.append(f'{count} ({percentage:.1f}%)<br>{bin_range}')  

    fig.update_traces(hovertemplate='<b>%{text}</b>', text=hover_text)

    fig.add_vline(x=mean_range, line_dash="dash", line_color="red", line_width=2, 
                  annotation_text=f"Mean = {mean_range:.2f}", annotation_position="bottom left")
    fig.add_vline(x=sigma_1, line_dash="dot", line_color="green", line_width=2, 
                  annotation_text=f"1σ = {sigma_1:.2f}", annotation_position="bottom left")
    fig.add_vline(x=sigma_2, line_dash="dot", line_color="purple", line_width=2, 
                  annotation_text=f"2σ = {sigma_2:.2f}", annotation_position="bottom left")

    fig.update_layout(
        xaxis_title='Price Range (High - Low)',
        yaxis_title='Frequency',
        font=dict(family="Arial", size=12),
        margin=dict(l=50, r=50, t=50, b=50),
        title_x=0.5
    )

    fig.update_traces(text=labels, textposition='outside')

    logging.info(f"Plotting complete for {dataset_label}.")
    fig.show()




# Main function to execute the script
if __name__ == "__main__":
    main()
