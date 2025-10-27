# config.py

from dotenv import load_dotenv
import os

# ATTEMPT #13: Using the corrected import path:
from phonepe.sdk.pg.clients.standard_checkout_client import StandardCheckoutClient 
from phonepe.sdk.pg.models.client_config import ClientConfig # Assuming this path is correct
from phonepe.sdk.pg.exceptions import PhonePeException 


load_dotenv() 

class Settings:
    # 1. PhonePe Credentials loaded from Render Environment Variables
    CLIENT_ID: str = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT: str = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX") 
    BACKEND_URL: str = os.getenv("BACKEND_URL") 

    # 2. SDK Initialization
    @classmethod
    def get_phonepe_client(cls) -> StandardCheckoutClient:
        
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            print("WARNING: PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET environment variables are missing on Render.")
            
        # Instantiate ClientConfig 
        config = ClientConfig(
            env=cls.ENVIRONMENT, 
            client_id=cls.CLIENT_ID, 
            client_secret=cls.CLIENT_SECRET
        )
        
        return StandardCheckoutClient(config)

settings = Settings()
# Initialize the client. This happens when the application starts.
try:
    phonepe_client = settings.get_phonepe_client()
except PhonePeException as e:
    print(f"ERROR: PhonePe client initialization failed: {e}")
    phonepe_client = None 
except Exception as e:
    # Catches the ImportError if the path is still wrong, or other general errors
    print(f"ERROR: Could not initialize PhonePe client: {e}")
    phonepe_client = None
