import requests
from datetime import datetime, timedelta
from main_login import AuthenticationManager, client_id, client_secret

class OptionChainClient:
    def __init__(self, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager

    def get_option_chain(self, symbol: str, config: dict) -> dict:
        token = self.auth_manager.get_token()
        headers = {"Authorization": f"Bearer {token}"}
        
        params = {
            "symbol": symbol,
            "contractType": config.get("contractType", "ALL"),
            "includeUnderlyingQuote": str(config.get("includeUnderlyingQuote", False)).lower(),
            "strategy": config.get("strategy", "SINGLE"),
            "fromDate": config.get("fromDate"),
            "toDate": config.get("toDate"),
        }

        response = requests.get("https://api.schwabapi.com/marketdata/v1/chains", headers=headers, params=params)
        
        # Log the request for debugging
        print("Request URL:", response.url)
        print("Request Headers:", headers)
        
        if not response.ok:
            print("Error response:", response.json())
        
        return response.json()
    


# Function to get the last two weeks of weekdays (Monday to Friday only)
def get_last_two_weeks_weekdays():
    today = datetime.today()
    two_weeks_ago = today - timedelta(days=7)
    weekdays = []
    for i in range(8):
        day = two_weeks_ago + timedelta(days=i)
        if day.weekday() < 5:  # Monday to Friday only
            weekdays.append(day.strftime("%Y-%m-%d"))
    return weekdays

# Instantiate your auth manager and client
auth_manager = AuthenticationManager(client_id=client_id, client_secret=client_secret)
client = OptionChainClient(auth_manager)

# Loop through the last 2 weeks of weekdays and get the 0DTE options for SPX
for date in get_last_two_weeks_weekdays():
    config = {
        "contractType": "ALL",  # Retrieve both CALL and PUT options
        "includeUnderlyingQuote": False,
        "strategy": "SINGLE",
        "fromDate": date,
        "toDate": date,  # 0DTE, so same date for fromDate and toDate
    }

    # Fetch the option chain for SPX
    option_chain = client.get_option_chain("$SPX", config)
    
    # Print or analyze the results
    print(f"Option chain for SPX on {date}:")
    print(option_chain)