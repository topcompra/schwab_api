from main_login import AuthenticationManager, client_id, client_secret
from schwab_api_endpoints import SchwabAPIClient
import logging

import plotly.graph_objects as go
import pandas as pd

def plot_candlestick_with_signals(price_history, signals, config):
    # Extract data
    candles = price_history['candles']
    open_prices = [candle['open'] for candle in candles]
    close_prices = [candle['close'] for candle in candles]
    high_prices = [candle['high'] for candle in candles]
    low_prices = [candle['low'] for candle in candles]
    
    # Calculate the Y-axis range
    min_price = min(low_prices)
    max_price = max(high_prices)
    y_min = min_price - 0.05 * min_price
    y_max = max_price + 0.05 * max_price
    
    # Create a date range for the x-axis based on the config
    start_date = pd.to_datetime('2023-01-01')  # Example start date
    periods = config['period'] * 48  # 180 days * 24 hours
    dates = pd.date_range(start=start_date, periods=periods, freq='h')
    
    # Create the candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=dates[:len(candles)],  # Ensure dates match the number of candles
                                         open=open_prices,
                                         high=high_prices,
                                         low=low_prices,
                                         close=close_prices,
                                         name='Candlestick')])
    
    # Example: Add a moving average as an indicator
    df = pd.DataFrame({'Date': dates[:len(candles)], 'Close': close_prices})
    df['MA'] = df['Close'].rolling(window=24).mean()  # Simple moving average over 24 hours
    fig.add_trace(go.Scatter(x=df['Date'], y=df['MA'], mode='lines', name='Moving Average'))
    
    # Plot buy/sell signals
    for signal in signals:
        if signal['type'] == 'buy':
            fig.add_trace(go.Scatter(x=[signal['date']], y=[signal['price']],
                                     mode='markers', marker=dict(color='green', size=10),
                                     name='Buy Signal'))
        elif signal['type'] == 'sell':
            fig.add_trace(go.Scatter(x=[signal['date']], y=[signal['price']],
                                     mode='markers', marker=dict(color='red', size=10),
                                     name='Sell Signal'))
    
    # Update layout with Y-axis range
    fig.update_layout(title='Candlestick Chart with Signals', xaxis_title='Date', yaxis_title='Price')
    fig.update_yaxes(range=[y_min, y_max])
    
    fig.show()

def main(auth_manager: AuthenticationManager):
    # Initialize the SchwabAPIClient with the AuthenticationManager
    
    api_client = SchwabAPIClient(authentication_manager=auth_manager)

    # Define the symbol you want to query
    symbol = "$SPX"

    default_config = {
    "periodType": "day",        # The type of period to request (e.g., day, month)
    "period": 10,              # The number of periods to request (e.g., 180 days)
    "frequencyType": "minute",  # The frequency type (e.g., minute, hour)
    "frequency": 30,            # The frequency of data points (e.g., every 60 minutes for hourly data)
    "needExtendedHoursData": False  # Whether to include extended hours data
    }
    
    # Example usage
    signals = [
        {'date': '2023-01-02 10:00:00', 'price': 5900, 'type': 'buy'},
        {'date': '2023-01-03 15:00:00', 'price': 6100, 'type': 'sell'}
    ]


    price_history = api_client.get_price_history(symbol=symbol, config=default_config)
    print(price_history)


    # Now you can call the method request_access_token() on the instance
    bearer_token = auth_manager.request_access_token()["access_token"]

    if bearer_token:
        logging.info("Token is valid, proceeding with data retrieval.")      
        plot_candlestick_with_signals(price_history, signals, default_config)
        #put functions to execute
    else:
        logging.error("Access token is invalid or has expired.")



if __name__ == "__main__":
    auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)
    main(auth_manager)