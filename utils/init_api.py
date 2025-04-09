import logging
from core.main_login import AuthenticationManager, client_id, client_secret
from utils.schwab_api_endpoints import SchwabAPIClient

def init_api():
    """Handles auth and initializes SchwabAPIClient."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    auth = AuthenticationManager(client_id=client_id, client_secret=client_secret)
    if not (auth.get_token() and auth.is_token_valid()):
        logging.error("❌ Auth failed.")
        return None

    logging.info("✅ Auth successful. SchwabAPIClient is ready.")
    return SchwabAPIClient(auth)