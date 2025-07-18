import json
import time
from . import sqs, notifier, db

def run_worker():
    print("[✓] Worker started and polling...")

    while True:
        messages = sqs.poll_messages()

        for msg in messages:
            try:
                body = json.loads(msg["Body"])
                app_id = body.get("Application")
                app_cfg = notifier.get_app_config(app_id)

                if not app_cfg:
                    raise Exception(f"App config not found for {app_id}")

                notifier.send_notification(app_cfg, body)
                db.log_request(app_id, body, "delivered")
                sqs.delete_message(msg["ReceiptHandle"])

            except Exception as e:
                db.log_request(body.get("Application", "unknown"), body, "failed", str(e))
                print(f"[✗] Error: {str(e)}")

        time.sleep(3)

if __name__ == "__main__":
    run_worker()

