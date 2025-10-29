# config.py

from dotenv import load_dotenv
import os

# Correct imports for the PhonePe SDK version you’re using
from phonepe.sdk.pg.clients.standard_checkout_client import StandardCheckoutClient
from phonepe.sdk.pg.models.client_config import ClientConfig
from phonepe.sdk.pg.exceptions import PhonePeException

load_dotenv()

class Settings:
    CLIENT_ID: str = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT: str = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX")
    BACKEND_URL: str = os.getenv("BACKEND_URL")

    @classmethod
    def get_phonepe_client(cls) -> StandardCheckoutClient:
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            print("⚠ Missing PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET environment variables.")

        # Lowercase or uppercase check for environment may vary
        env_value = cls.ENVIRONMENT.upper()
        if env_value not in ("SANDBOX", "PRODUCTION"):
            print(f"⚠ Unexpected PHONEPE_ENVIRONMENT value '{cls.ENVIRONMENT}', defaulting to SANDBOX.")
            env_value = "SANDBOX"

        # Build config
        config = ClientConfig(
            env=env_value,
            client_id=cls.CLIENT_ID,
            client_secret=cls.CLIENT_SECRET
        )

        return StandardCheckoutClient(config)

settings = Settings()

try:
    phonepe_client = settings.get_phonepe_client()
    print("✅ PhonePe client initialized successfully.")
except PhonePeException as e:
    print(f"❌ PhonePe client initialization failed: {e}")
    phonepe_client = None
except Exception as e:
    print(f"❌ Unexpected error initializing PhonePe client: {e}")
    phonepe_client = None
