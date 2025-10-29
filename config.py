from dotenv import load_dotenv
import os

# ✅ Correct imports for the official PhonePe SDK (from private repo)
from phonepe_sdk.pg.clients.standard_checkout_client import StandardCheckoutClient
from phonepe.sdk.pg.models.client_config import ClientConfig
from phonepe.sdk.pg.exceptions import PhonePeException

# Load environment variables
load_dotenv()


class Settings:
    CLIENT_ID: str = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT: str = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX")
    BACKEND_URL: str = os.getenv("BACKEND_URL")

    @classmethod
    def get_phonepe_client(cls) -> StandardCheckoutClient:
        """Initialize the PhonePe Standard Checkout Client"""
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            print("⚠ Missing PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET environment variables.")

        env_value = cls.ENVIRONMENT.upper()
        if env_value not in ("SANDBOX", "PRODUCTION"):
            print(f"⚠ Invalid PHONEPE_ENVIRONMENT='{cls.ENVIRONMENT}', defaulting to SANDBOX.")
            env_value = "SANDBOX"

        try:
            config = ClientConfig(
                env=env_value,
                client_id=cls.CLIENT_ID,
                client_secret=cls.CLIENT_SECRET
            )
            return StandardCheckoutClient(config)
        except Exception as e:
            print(f"❌ Error initializing PhonePe client: {e}")
            raise


settings = Settings()

try:
    phonepe_client = settings.get_phonepe_client()
    print("✅ PhonePe client initialized successfully.")
except PhonePeException as e:
    print(f"❌ PhonePe SDK Exception: {e}")
    phonepe_client = None
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    phonepe_client = None
