# worker/app/sqs_client.py

import boto3
import json
from .config import settings

def get_sqs_client():
    return boto3.client(
        "sqs",
        region_name=settings.AWS_REGION,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        endpoint_url="http://localstack:4566"  
    )

def receive_messages(max_messages=5):
    sqs = get_sqs_client()
    response = sqs.receive_message(
        QueueUrl=settings.SQS_QUEUE_URL,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=10
    )
    return response.get("Messages", [])

def delete_message(receipt_handle):
    sqs = get_sqs_client()
    sqs.delete_message(
        QueueUrl=settings.SQS_QUEUE_URL,
        ReceiptHandle=receipt_handle
    )
