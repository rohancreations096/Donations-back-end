# config.py

from dotenv import load_dotenv
import os

# ATTEMPT #6: Corrected imports based on standard PhonePe SDK structure
# The client is usually one level deeper (standard_checkout)
from phonepe.sdk.pg.standard_checkout import StandardCheckoutClient 
# Configuration models are often in a 'models' submodule
from phonepe.sdk.pg.models.client_config import ClientConfig 

load_dotenv() 

class Settings:
    # 1. PhonePe Credentials loaded from Environment Variables
    CLIENT_ID: str = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT: str = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX") 
    BACKEND_URL: str = os.getenv("BACKEND_URL") 

    # 2. SDK Initialization
    @classmethod
    def get_phonepe_client(cls) -> StandardCheckoutClient:
        # Check if essential credentials are provided
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            # This is a warning, not a crash, as the import is already done
            print("WARNING: PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET environment variables are missing.")
            
        config = ClientConfig(
            env=cls.ENVIRONMENT, 
            client_id=cls.CLIENT_ID, 
            client_secret=cls.CLIENT_SECRET
        )
        
        return StandardCheckoutClient(config)

settings = Settings()
# Initialize the client. This will run immediately when config.py is loaded.
try:
    phonepe_client = settings.get_phonepe_client()
except Exception as e:
    # This will catch errors during client initialization (e.g., bad credentials/environment value)
    print(f"ERROR: Could not initialize PhonePe client: {e}")
    phonepe_client = None
