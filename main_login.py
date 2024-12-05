import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import time
import logging
from typing import Dict, Optional


# Load environment variables from .env file
load_dotenv()


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Schwab API OAuth2 credentials
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
callback_url = os.getenv("callback_url")
token_url = 'https://api.schwabapi.com/v1/oauth/token'


class AuthenticationManager:
    """Handles token management and API requests for Schwab."""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_data = None
    
    def request_access_token(self) -> Optional[Dict[str, any]]:
        logging.info('Requesting access token...')
        token_data = {
            'grant_type': 'client_credentials',
            'scope': 'accounts'  # Define scope (modify as needed)
        }
        response = requests.post(
            token_url, 
            data=token_data, 
            auth=HTTPBasicAuth(self.client_id, self.client_secret)
        )
        token_timestamp = time.time()
        
        if response.status_code == 200:
            token_response = response.json()
            logging.info('Access token received successfully.')
            self.token_data = {
                'access_token': token_response.get('access_token'),
                'token_type': token_response.get('token_type', 'Bearer'),
                'expires_in': int(token_response.get('expires_in', 3600)),
                'timestamp': token_timestamp
            }
            return self.token_data
        else:
            logging.error(f"Failed to retrieve access token: {response.content}")
            return None
    
    def is_token_valid(self) -> bool:
        """Checks if the token is still valid."""
        if not self.token_data:
            return False
        current_time = time.time()
        return (current_time - self.token_data['timestamp']) < self.token_data['expires_in']

    def get_token(self):
        if not self.is_token_valid():
            self.request_access_token()
        return self.token_data["access_token"]
    
#not needed but to track


'''
def main():
    client = AuthenticationManager(client_id, client_secret)
    if client.request_access_token() and client.is_token_valid():
        logging.info("Token is valid, proceeding with data retrieval.")
    else:
        logging.error("Access token is invalid or has expired.")
'''
'''
if __name__ == "__main__":
    main()
'''