# config.py

from dotenv import load_dotenv
import os

# ATTEMPT #9: Using the confirmed PhonePePaymentClient / Env structure
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient 
from phonepe.sdk.pg.env import Env 
from phonepe.sdk.pg.exceptions import PhonePeException # Add this for robust initialization


load_dotenv() 

class Settings:
    # 1. PhonePe Credentials loaded from Environment Variables
    CLIENT_ID: str = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT_NAME: str = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX") 
    SALT_INDEX: int = int(os.getenv("PHONEPE_SALT_INDEX", 1)) # Required for this client version
    BACKEND_URL: str = os.getenv("BACKEND_URL") 
    
    # Map string environment name to the Env enum object
    @classmethod
    def get_env(cls):
        if cls.ENVIRONMENT_NAME.upper() == "PRODUCTION":
            return Env.PROD
        # Default to UAT/SANDBOX if not production or invalid
        return Env.UAT 

    # 2. SDK Initialization
    @classmethod
    def get_phonepe_client(cls) -> PhonePePaymentClient:
        # We need the salt key/index for this client implementation
        SALT_KEY = cls.CLIENT_SECRET # The client uses CLIENT_SECRET as SALT_KEY
        
        # Check if essential credentials are provided
        if not cls.CLIENT_ID or not SALT_KEY:
            print("WARNING: PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET environment variables are missing.")

        return PhonePePaymentClient(
            merchant_id=cls.CLIENT_ID, # Merchant ID is passed as client_id
            salt_key=SALT_KEY, 
            salt_index=cls.SALT_INDEX,
            env=cls.get_env()
        )

settings = Settings()
# Initialize the client.
try:
    phonepe_client = settings.get_phonepe_client()
except PhonePeException as e:
    # Use the specific PhonePeException for clearer error handling
    print(f"ERROR: PhonePe client initialization failed: {e}")
    phonepe_client = None 
except Exception as e:
    # Catch any other error (like KeyError for missing env vars if not handled)
    print(f"ERROR: Could not initialize PhonePe client: {e}")
    phonepe_client = None
