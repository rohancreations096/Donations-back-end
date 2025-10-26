# config.py

from dotenv import load_dotenv
import os
# Imports for the new PhonePe SDK
from phonepe.sdk.pg.payments.v1.standard_checkout_client import StandardCheckoutClient
from phonepe.sdk.pg.common.configs.client_config import ClientConfig

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
        config = ClientConfig(
            env=cls.ENVIRONMENT, 
            client_id=cls.CLIENT_ID, 
            client_secret=cls.CLIENT_SECRET
        )
        return StandardCheckoutClient(config)

settings = Settings()
phonepe_client = settings.get_phonepe_client()
