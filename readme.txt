Install docker, docker-compose, aws cli


# Tear everything down

docker-compose down --volumes --remove-orphans
docker system prune -af
docker volume prune -f

#build all the containers
docker-compose build --no-cache
docker-compose up -d

#connect to the queue and get messages

aws --endpoint-url=http://localstack:4566 sqs receive-message \
  --queue-url=http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/notifications-queue
  

# Test messages

## admin register a new app
curl -X POST http://localhost:8001/app \
  -H "Content-Type: application/json" \
  -d '{
    "Application": "App1",
    "App_name": "CHA - Student Platform",
    "Email": "no-reply@cha.com",
    "Domain": "cha.com"
  }'
  

## requester send a new request of type email  
curl -X POST http://localhost:8000/requester \
  -H "Content-Type: application/json" \
  -d '{
    "Application": "App2",
    "Recipient": "user@example.com",
    "Subject": "Test Subject",
    "Message": "Hello, this is a test message!",
    "OutputType": "EMAIL",
    "Interval": {
      "Once": true
    },
    "EmailAddresses": ["user@example.com"]
  }'

## requester send a new request of type SMS   
curl -X POST http://localhost:8000/requester \
  -H "Content-Type: application/json" \
  -d '{
    "Application": "App1",
    "Recipient": "1234567890",
    "Subject": "Test SMS",
    "Message": "This is an SMS test.",
    "OutputType": "SMS",
    "PhoneNumber": "+15555555555",
    "Interval": {
      "Days": [1, 15]
    }
  }'

## requester send a new request of type PUSH   
curl -X POST http://localhost:8000/requester \
  -H "Content-Type: application/json" \
  -d '{
    "Application": "App1",
    "Recipient": "pushUser1",
    "Subject": "New Alert",
    "Message": "You have a new notification!",
    "OutputType": "PUSH",
    "PushToken": "example_token_123",
    "Interval": {
      "Weeks": [2, 4]
    }
  }'


# Tests

📦 1. Check DynamoDB table values
List tables:
aws --endpoint-url=http://localhost:4566 dynamodb list-tables

Scan table:

aws --endpoint-url=http://localhost:4566 dynamodb scan --table-name Applications

📬 2. Check SNS topics

aws --endpoint-url=http://localhost:4566 sns list-topics

📧 3. Check SES domain identities

aws --endpoint-url=http://localhost:4566 ses list-identities

📪 4. Check SQS queue URLs
aws --endpoint-url=http://localhost:4566 sqs list-queues

Read messages:
aws --endpoint-url=http://localhost:4566 sqs receive-message \
  --queue-url http://localhost:4566/000000000000/notifications-queue
  
🪵 5. View logs of running containers

List containers:

docker ps

logs of a specific container (e.g., worker, admin, requestor, localstack):

docker logs worker
docker logs admin
docker logs requestor
docker logs localstack  

