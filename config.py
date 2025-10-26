# config.py

from dotenv import load_dotenv
import os
# Corrected Imports for the PhonePe SDK
# The client and config classes are often closer to the root of the SDK package
from phonepe.sdk.standard_checkout_client import StandardCheckoutClient # Corrected import path
from phonepe.sdk.pg.common.config import ClientConfig # Corrected import path

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
            # Raise an error or log a warning if keys are missing during startup
            # This helps debug configuration issues early.
            # For now, we'll allow it to proceed, but it will fail later.
            print("WARNING: PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET environment variables are missing.")
            
        config = ClientConfig(
            env=cls.ENVIRONMENT, 
            client_id=cls.CLIENT_ID, 
            client_secret=cls.CLIENT_SECRET
        )
        return StandardCheckoutClient(config)

settings = Settings()
# Initialize the client only if credentials might be present
# Handle the case where initialization might fail if keys are None
try:
    phonepe_client = settings.get_phonepe_client()
except Exception as e:
    # Log the error if client initialization fails (e.g., due to missing keys)
    print(f"ERROR: Could not initialize PhonePe client: {e}")
    phonepe_client = None # Set to None so later code can check if it's available
