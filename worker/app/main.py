import json
from . import sqs_client, dynamodb_client, notifier, logger


def run_worker():
    logger.log("Worker started polling SQS...")
    while True:
        messages = sqs_client.poll_messages()
        for msg in messages:
            try:
                body = json.loads(msg["Body"])
                app_id = body["Application"]
                logger.log(f"Processing message for application: {app_id}")
                cfg = dynamodb_client.get_application_config(app_id)
                if not cfg:
                    raise Exception("App config not found")

                output = body.get("OutputType")
                if output == "EMAIL":
                    notifier.send_email(cfg["SES-Domain-ARN"], body["EmailAddresses"], body["Subject"], body["Message"])
                    logger.log(f"Email sent to {body['EmailAddresses']}")
                elif output in ["SMS", "PUSH"]:
                    notifier.send_sns(cfg["SNS-Topic-ARN"], body["Message"])
                    logger.log(f"Notification sent via {output} to {body['PhoneNumber'] or body['PushToken']}")
                else:
                    raise Exception("Unsupported OutputType")

                dynamodb_client.log_request(app_id, body, "delivered")
                logger.log(f"Message processed successfully: {body}")
                sqs_client.delete_message(msg["ReceiptHandle"])
                logger.log("Message deleted from SQS")
            except Exception as e:
                dynamodb_client.log_request(body.get("Application", "unknown"), body, "failed", str(e))
                logger.log(f"Error: {e}")

if __name__ == "__main__":
    run_worker()

