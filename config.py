from dotenv import load_dotenv
import os

# ✅ Correct imports for PhonePe SDK v2.1.5
from phonepe.sdk.pg import PhonePePaymentClient, PhonePeEnvironment
from phonepe.sdk.pg.exceptions import PhonePeException

load_dotenv()

class Settings:
    CLIENT_ID = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX")
    BACKEND_URL = os.getenv("BACKEND_URL")

    @classmethod
    def get_phonepe_client(cls):
        """Initialize PhonePe client with current environment."""
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            print("⚠ Missing PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET in environment variables.")

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
            print(f"❌ PhonePe initialization error: {e}")
            raise
        except Exception as e:
            print(f"❌ Unexpected error initializing PhonePe client: {e}")
            raise


settings = Settings()
try:
    phonepe_client = settings.get_phonepe_client()
except Exception:
    phonepe_client = None
