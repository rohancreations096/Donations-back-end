from dotenv import load_dotenv
import os

# ✅ Correct imports for PhonePe SDK 2.1.x
from phonepe.sdk.pg.payments.v1 import PhonePePaymentClient
from phonepe.sdk.pg.env import PhonePeEnvironment
from phonepe.sdk.pg.exceptions import PhonePeException

load_dotenv()

class Settings:
    """Holds all environment-based configurations."""
    CLIENT_ID: str = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT: str = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX")
    BACKEND_URL: str = os.getenv("BACKEND_URL")

    @classmethod
    def get_phonepe_client(cls) -> PhonePePaymentClient:
        """Initialize and return a configured PhonePe client."""
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            print("⚠ Missing PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET in environment variables.")

        # Choose environment based on .env or Render vars
        environment = (
            PhonePeEnvironment.SANDBOX
            if cls.ENVIRONMENT.upper() == "SANDBOX"
            else PhonePeEnvironment.PRODUCTION
        )

        try:
            client = PhonePePaymentClient(
                merchant_id=cls.CLIENT_ID,
                salt_key=cls.CLIENT_SECRET,
                environment=environment,
            )
            print("✅ PhonePe client initialized successfully.")
            return client
        except PhonePeException as e:
            print(f"❌ PhonePe initialization failed: {e}")
            raise
        except Exception as e:
            print(f"❌ Unexpected error initializing PhonePe client: {e}")
            raise


settings = Settings()

# Initialize globally for reuse
try:
    phonepe_client = settings.get_phonepe_client()
except Exception as e:
    print(f"⚠ Client not initialized: {e}")
    phonepe_client = None
