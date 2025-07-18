import boto3
from .config import settings

def save_app_record(app_record: dict):
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url=settings.AWS_ENDPOINT
    )
    table = dynamodb.Table(settings.APP_CONFIG_TABLE)
    table.put_item(Item=app_record)

def get_all_apps():
    dynamodb = boto3.resource(
        "dynamodb",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    table = dynamodb.Table(settings.APP_CONFIG_TABLE)
    response = table.scan()
    return response.get("Items", [])

