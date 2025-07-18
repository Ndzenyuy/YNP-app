import boto3
from datetime import datetime
from . import config

dynamodb = boto3.resource(
    "dynamodb",
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    endpoint_url=config.AWS_ENDPOINT
)

def log_request(app_id, message, status, error=""):
    table = dynamodb.Table(config.REQUEST_LOG_TABLE)
    table.put_item(Item={
        "ApplicationID": app_id,
        "Timestamp": datetime.utcnow().isoformat(),
        "Status": status,
        "Payload": message,
        "Error": error
    })

