#!/bin/bash
set -e

echo "⏳ Bootstrapping AWS services in LocalStack..."

awslocal sqs create-queue --queue-name notifications-queue

awslocal dynamodb create-table \
  --table-name Applications \
  --attribute-definitions AttributeName=Application,AttributeType=S \
  --key-schema AttributeName=Application,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

awslocal dynamodb create-table \
  --table-name RequestLogs \
  --attribute-definitions AttributeName=Application,AttributeType=S \
  --key-schema AttributeName=Application,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

echo "✅ LocalStack bootstrap complete."

