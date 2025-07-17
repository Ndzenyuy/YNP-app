from fastapi import FastAPI, HTTPException
from .models import NotificationRequest
from .sqs_client import send_message_to_queue

app = FastAPI()

@app.post("/notify")
def notify(req: NotificationRequest):
    try:
        response = send_message_to_queue(req.dict())
        return {"message_id": response.get("MessageId"), "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
