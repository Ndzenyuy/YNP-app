import time
import json
from .sqs_client import receive_messages, delete_message
from .db import get_app_config, log_request
from .handlers import send_email, send_sms, send_push
from .config import settings

def run_worker():
    print("[✓] Worker running and polling SQS...")
    while True:
        messages = receive_messages()
        print(f"[✓] Received: {messages}")
        for msg in messages:
            try:
                body = json.loads(msg["Body"])
                app_cfg = get_app_config(body["Application"])
                if not app_cfg:
                    raise Exception("App config not found")

                body["Region"] = settings.AWS_REGION
                if body["OutputType"] == "email":
                    send_email(app_cfg, body)
                elif body["OutputType"] == "sms":
                    send_sms(app_cfg, body)
                elif body["OutputType"] == "push":
                    send_push(app_cfg, body)
                else:
                    raise Exception("Invalid OutputType")

                log_request(body["Application"], body, status="success")
                delete_message(msg["ReceiptHandle"])

            except Exception as e:
                log_request(body.get("Application", "unknown"), body, status="failed", error=str(e))

        time.sleep(2)

if __name__ == "__main__":
    run_worker()

