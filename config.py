# config.py

from dotenv import load_dotenv
import os
# FINAL ATTEMPT: Assuming both classes are exposed directly by the 'pg' module
from phonepe.sdk.pg import StandardCheckoutClient 
from phonepe.sdk.pg import ClientConfig 

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
            print("WARNING: PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET environment variables are missing.")
            
        config = ClientConfig(
            env=cls.ENVIRONMENT, 
            client_id=cls.CLIENT_ID, 
            client_secret=cls.CLIENT_SECRET
        )
        
        return StandardCheckoutClient(config)

settings = Settings()
# Initialize the client only if credentials might be present
try:
    phonepe_client = settings.get_phonepe_client()
except Exception as e:
    print(f"ERROR: Could not initialize PhonePe client: {e}")
    phonepe_client = None
