import boto3
from . import config

dynamodb = boto3.resource(
    "dynamodb",
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    endpoint_url="http://localstack:4566",
)

def get_application_config(app_id):
    table = dynamodb.Table(config.APPLICATIONS_TABLE)
    response = table.get_item(Key={"Application": app_id})
    return response.get("Item")

def log_request(application_id, request_data, status, error=None):
    table = dynamodb.Table(config.REQUEST_LOG_TABLE)
    from datetime import datetime
    table.put_item(Item={
        "Application": application_id,
        "Timestamp": datetime.utcnow().isoformat(),
        "Status": status,
        "Error": error or "None",
        "Request": request_data,
    })

