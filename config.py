from dotenv import load_dotenv
import os

# ✅ Correct imports for latest PhonePe SDK
from phonepe.sdk.pg import PhonePePaymentClient, PhonePeEnvironment
from phonepe.sdk.pg.exceptions import PhonePeException

load_dotenv()

class Settings:
    CLIENT_ID: str = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET: str = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT: str = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX")
    BACKEND_URL: str = os.getenv("BACKEND_URL")

    @classmethod
    def get_phonepe_client(cls) -> PhonePePaymentClient:
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            print("⚠ Missing PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET in environment variables.")

        environment = (
            PhonePeEnvironment.SANDBOX
            if cls.ENVIRONMENT.upper() == "SANDBOX"
            else PhonePeEnvironment.PRODUCTION
        )

        # ✅ Initialize PhonePe client properly
        return PhonePePaymentClient(
            merchant_id=cls.CLIENT_ID,
            salt_key=cls.CLIENT_SECRET,
            environment=environment
        )

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
