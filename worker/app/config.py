import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
    APP_CONFIG_TABLE = os.getenv("APP_CONFIG_TABLE")
    REQUEST_LOG_TABLE = os.getenv("REQUEST_LOG_TABLE")

settings = Settings()

