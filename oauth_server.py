import requests
from flask import Flask, request, redirect
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("oauth_debug.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs to the console
    ]
)

app = Flask(__name__)

# Step 1: Set the necessary values
client_id = "1wzwOrhivb2PkR1UCAUVTKYqC4MTNYlj"  # Replace with your client_id
client_secret = "YOUR_CLIENT_SECRET"  # Replace with your client_secret
redirect_uri = "http://127.0.0.1:5000/callback"  # Must match what's registered with Schwab
authorization_url = "https://api.schwabapi.com/v1/oauth/authorize"
token_url = "https://api.schwabapi.com/v1/oauth/token"
scope = "readonly"

# Step 2: Create the authorization URL
@app.route("/")
def authorize():
    logging.info("Starting the authorization process.")
    auth_params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope
    }
    auth_url = f"{authorization_url}?{requests.utils.urlencode(auth_params)}"
    logging.info(f"Authorization URL created: {auth_url}")
    return redirect(auth_url)

# Step 3: Handle the callback and retrieve the tokens
@app.route("/callback")
def callback():
    logging.info("Handling callback after user authorization.")
    auth_code = request.args.get("code")
    
    if not auth_code:
        logging.error("Authorization failed or no code received.")
        return "Authorization failed or no code received. Check the logs for details."

    logging.info(f"Authorization code received: {auth_code}")

    # Exchange the authorization code for tokens
    token_params = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }

    logging.info("Exchanging authorization code for tokens.")
    try:
        token_response = requests.post(token_url, data=token_params)
        logging.info(f"Token response status: {token_response.status_code}")
        if token_response.status_code == 200:
            tokens = token_response.json()
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")
            logging.info("Tokens retrieved successfully.")
            logging.debug(f"Access Token: {access_token}")
            logging.debug(f"Refresh Token: {refresh_token}")
            return (
                f"Access Token: {access_token}<br>"
                f"Refresh Token: {refresh_token}<br>"
                "Save these tokens securely!"
            )
        else:
            logging.error(f"Failed to retrieve tokens. Response: {token_response.text}")
            return (
                f"Failed to retrieve tokens.<br>"
                f"Status Code: {token_response.status_code}<br>"
                f"Response: {token_response.text}"
            )
    except Exception as e:
        logging.exception("An error occurred while exchanging the authorization code.")
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    logging.info("Starting Flask server for OAuth process.")
    logging.info("Visit http://127.0.0.1:5000 to start the authorization process.")
    app.run(debug=True)
