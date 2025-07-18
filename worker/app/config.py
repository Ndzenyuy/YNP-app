import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "http://localstack:4566/000000000000/notifications-queue")
APPLICATIONS_TABLE = os.getenv("APPLICATIONS_TABLE")
REQUEST_LOG_TABLE = os.getenv("REQUEST_LOG_TABLE")

