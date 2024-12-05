from main_login import AuthenticationManager, client_id, client_secret
import requests
import logging


class SchwabAPIClient:

    def __init__(self, authentication_manager: AuthenticationManager) -> None:
        self.auth_manager = authentication_manager


    def get_price_history(self, symbol: str, config: dict) -> dict:
        token = self.auth_manager.get_token()  # Reuse the token manager
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "symbol": symbol,
            "periodType": config.get("periodType", "year"),
            "period": config.get("period", 10),
            "frequencyType": config.get("frequencyType", "monthly"),
            "frequency": config.get("frequency", 1),
            "needExtendedHoursData": str(config.get("needExtendedHoursData", False)).lower(),
            "needPreviousClose": "false"
        }
        
        response = requests.get("https://api.schwabapi.com/marketdata/v1/pricehistory", headers=headers, params=params)
        return response.json()
    

class OptionChainClient:
    def __init__(self, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager

    def get_option_chain(self, symbol: str, config: dict) -> dict:
        # Retrieve token from auth manager
        token = self.auth_manager.get_token()
        
        # Set up headers for authorization
        headers = {"Authorization": f"Bearer {token}"}
        
        # Build parameters based on the provided configuration
        params = {
            "symbol": symbol,
            "contractType": config.get("contractType", "ALL"),
            "strikeCount": config.get("strikeCount"),
            "includeUnderlyingQuote": str(config.get("includeUnderlyingQuote", False)).lower(),
            "strategy": config.get("strategy", "SINGLE"),
            "interval": config.get("interval"),
            "strike": config.get("strike"),
            "range": config.get("range", "ALL"),
            "fromDate": config.get("fromDate"),
            "toDate": config.get("toDate"),
            "volatility": config.get("volatility"),
            "underlyingPrice": config.get("underlyingPrice"),
            "interestRate": config.get("interestRate"),
            "daysToExpiration": config.get("daysToExpiration"),
            "expMonth": config.get("expMonth", "ALL"),
            "optionType": config.get("optionType"),
            "entitlement": config.get("entitlement"),
        }

        # Make the GET request to the option chain endpoint
        response = requests.get("https://api.schwabapi.com/marketdata/v1/chains", headers=headers, params=params)
        
        # Return the JSON response
        return response.json()

    
def main():

    # Initialize the AuthenticationManager
    client = AuthenticationManager(client_id=client_id, client_secret=client_secret)
    logging.info(f"Logging Client.")
    # Initialize SchwabAPIClient using the AuthenticationManager
    api_client = SchwabAPIClient(authentication_manager=client)
    logging.info(f"Calling the Schwab API endpoint")
    # Example config for the price history request
    config = {
        "periodType": "year",
        "period": 10,
        "frequencyType": "daily",
        "frequency": 1,
        "needExtendedHoursData": False
    }

    # Call the get_price_history method
    price_history = api_client.get_price_history(symbol="$SPX", config=config)
    
    return

if __name__ == "__main__":
    main()

