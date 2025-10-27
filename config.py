# config.py

from dotenv import load_dotenv
import os

# ATTEMPT #10: Final best guess assuming a simple 'client' and 'config' module structure
# This assumes the client class is StandardCheckoutClient
from phonepe.sdk.pg.client import StandardCheckoutClient 
from phonepe.sdk.pg.config import ClientConfig # Assuming the configuration model is here
# We'll use a standard exception just in case
from phonepe.sdk.pg.exceptions import PhonePeException 


load_dotenv() 

class Settings:
    # 1. PhonePe Credentials loaded from Render Environment Variables
    CLIENT_ID: str = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT_NAME: str = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX") 
    BACKEND_URL: str = os.getenv("BACKEND_URL") 
    
    # The current SDK might not use an Env enum, so we'll pass the string directly if needed.
    
    # 2. SDK Initialization
    @classmethod
    def get_phonepe_client(cls) -> StandardCheckoutClient:
        
        # Check if essential credentials are provided
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            print("WARNING: PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET environment variables are missing on Render.")

        # Instantiate ClientConfig (Assuming it takes the credentials and environment string)
        config = ClientConfig(
            env=cls.ENVIRONMENT_NAME, 
            client_id=cls.CLIENT_ID, 
            client_secret=cls.CLIENT_SECRET
        )
        
        return StandardCheckoutClient(config)

settings = Settings()
# Initialize the client.
try:
    phonepe_client = settings.get_phonepe_client()
except PhonePeException as e:
    # Use the specific PhonePeException for clearer error handling
    print(f"ERROR: PhonePe client initialization failed: {e}")
    phonepe_client = None 
except Exception as e:
    # Catch any general error (ImportError is caught here if path is still wrong)
    print(f"ERROR: Could not initialize PhonePe client: {e}")
    phonepe_client = None
