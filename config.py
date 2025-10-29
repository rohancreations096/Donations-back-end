from dotenv import load_dotenv
import os

# ✅ Correct imports for official PhonePe SDK v1.0.4
from phonepe.sdk.pg import PhonePeClient
from phonepe.sdk.pg.env import Env
from phonepe.sdk.pg.exceptions import PhonePeException

load_dotenv()

class Settings:
    CLIENT_ID = os.getenv("PHONEPE_CLIENT_ID")
    CLIENT_SECRET = os.getenv("PHONEPE_CLIENT_SECRET")
    ENVIRONMENT = os.getenv("PHONEPE_ENVIRONMENT", "SANDBOX")
    BACKEND_URL = os.getenv("BACKEND_URL")

    @classmethod
    def get_phonepe_client(cls):
        """Initialize PhonePe client with proper environment."""
        if not cls.CLIENT_ID or not cls.CLIENT_SECRET:
            print("⚠ Missing PHONEPE_CLIENT_ID or PHONEPE_CLIENT_SECRET in environment variables.")

        env = Env.SANDBOX if cls.ENVIRONMENT.upper() == "SANDBOX" else Env.PRODUCTION

        try:
            client = PhonePeClient(
                env=env,
                merchant_id=cls.CLIENT_ID,
                salt_key=cls.CLIENT_SECRET,
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
