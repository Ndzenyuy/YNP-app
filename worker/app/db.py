import boto3
from .config import settings

def get_dynamodb():
    return boto3.resource(
        "dynamodb",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )

def get_app_config(application_id: str):
    table = get_dynamodb().Table(settings.APP_CONFIG_TABLE)
    resp = table.get_item(Key={"Application": application_id})
    return resp.get("Item")

def log_request(application_id: str, payload: dict, status: str, error: str = None):
    table = get_dynamodb().Table(settings.REQUEST_LOG_TABLE)
    item = {
        "Application": application_id,
        "Message": payload["Message"],
        "Status": status,
        "OutputType": payload["OutputType"],
        "EmailAddresses": payload.get("EmailAddresses"),
        "PhoneNumber": payload.get("PhoneNumber"),
        "PushToken": payload.get("PushToken"),
        "Error": error
    }
    table.put_item(Item=item)

