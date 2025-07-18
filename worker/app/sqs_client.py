import boto3
import json
from . import config

sqs = boto3.client(
    "sqs",
    region_name=config.AWS_REGION,
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    endpoint_url="http://localstack:4566",
)

def poll_messages(max_messages=1):
    response = sqs.receive_message(
        QueueUrl=config.SQS_QUEUE_URL,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=10
    )
    return response.get("Messages", [])

def delete_message(receipt_handle):
    sqs.delete_message(
        QueueUrl=config.SQS_QUEUE_URL,
        ReceiptHandle=receipt_handle
    )

