from pydantic import BaseSettings

class Settings(BaseSettings):
    GOOGLE_APPLICATION_CREDENTIALS: str = None
    RAZORPAY_KEY_ID: str = None
    RAZORPAY_KEY_SECRET: str = None

    class Config:
        env_file = ".env"

settings = Settings()
