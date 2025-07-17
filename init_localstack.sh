#!/bin/bash

echo "[+] Waiting for LocalStack to start..."
sleep 5

echo "[+] Creating DynamoDB table..."
awslocal dynamodb create-table \
  --table-name Applications \
  --attribute-definitions AttributeName=ApplicationID,AttributeType=S \
  --key-schema AttributeName=ApplicationID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

echo "[+] Creating SQS queue..."
awslocal sqs create-queue --queue-name notifications-queue

echo "[+] SES: Verifying domain (mocked)..."
# No actual email sent, just simulated

echo "[✓] LocalStack resources ready!"
