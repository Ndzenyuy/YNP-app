# 📬 Notification System with LocalStack

A microservices-based Python project using FastAPI, Docker, and LocalStack to handle notification requests (EMAIL, SMS, PUSH) through AWS services simulated locally.

## 📦 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (if testing Python scripts outside containers)
- AWS CLI v2
- LocalStack

Install AWS CLI and Docker from [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and [Docker](https://docs.docker.com/get-docker/)

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Ndzenyuy/notification-system.git
cd notification-system
```

### 2. Set up `.env` files for each service

Create `.env` files inside each of the `admin`, `requestor`, and `worker` folders. Here's an example:

```env
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
AWS_REGION=us-east-1
SQS_QUEUE_URL=http://localstack:4566/000000000000/notifications-queue
DYNAMODB_TABLE=Applications
REQUEST_LOG_TABLE=RequestLogs
```

### 3. Build and Run Services

```bash
docker-compose build --no-cache
docker-compose up -d
```

## 🧪 Test the Services

### ✅ Check if Services Are Running

```bash
curl http://localhost:4566/_localstack/health
curl http://localhost:8000/health     # Requestor
curl http://localhost:8001/health     # Admin

```

### 📬 Test Requestor

```bash
curl -X POST http://localhost:8000/requester \
  -H "Content-Type: application/json" \
  -d '{
    "Application": "App1",
    "Recipient": "user@example.com",
    "Subject": "Test Subject",
    "Message": "Hello, this is a test message!",
    "OutputType": "EMAIL",
    "Interval": {
      "Once": true
    },
    "EmailAddresses": ["user@example.com"]
  }'
```

### 🛠 Test Admin (SES/SNS registration)

```bash
curl -X POST http://localhost:8001/admin \
  -H "Content-Type: application/json" \
  -d '{
    "ApplicationID": "App1",
    "AppName": "CHA - Student Platform",
    "Email": "no-reply@cha.com",
    "Domain": "cha.com"
  }'
```

## 🔍 Debugging & Logs

### Access Container Logs

```bash
docker logs worker
docker logs admin
docker logs requestor
```

### Interact with LocalStack Services

```bash
# List queues
aws --endpoint-url=http://localhost:4566 sqs list-queues

# Receive messages
aws --endpoint-url=http://localhost:4566 sqs receive-message \
  --queue-url http://localstack:4566/000000000000/notifications-queue

# Check DynamoDB tables
aws --endpoint-url=http://localhost:4566 dynamodb scan --table-name Applications
aws --endpoint-url=http://localhost:4566 dynamodb scan --table-name RequestLogs
```

## 🔁 Developer Workflow (Auto Refresh on Code Change)

**Clean & Rebuild All**

```bash
docker-compose down --volumes --remove-orphans
docker system prune -af
docker volume prune -f
docker-compose build --no-cache
docker-compose up -d
```

## 📁 Directory Structure

```
├── admin/
│   ├── app/
│   ├── .env
│   ├── Dockerfile
├── requestor/
│   ├── app/
│   ├── .env
│   ├── Dockerfile
├── worker/
│   ├── app/
│   ├── .env
│   ├── Dockerfile
├── localstack/
│   ├── bootstrap.sh
├── docker-compose.yml
├── README.md
└── requirements.txt
```

## ✅ Requirements

```txt
fastapi
boto3
python-dotenv
uvicorn
pydantic==1.10.13
email-validator
```
