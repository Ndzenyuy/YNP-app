import boto3

def send_email(cfg, req):
    ses = boto3.client("ses", region_name=cfg["Region"])
    destination = req["EmailTo"] if isinstance(req["EmailTo"], list) else [req["EmailTo"]]
    return ses.send_email(
        Source=cfg["Email"],
        Destination={"ToAddresses": destination},
        Message={
            "Subject": {"Data": req.get("Subject", "")},
            "Body": {"Text": {"Data": req["Message"]}}
        }
    )

def send_sms(cfg, req):
    sns = boto3.client("sns", region_name=cfg["Region"])
    return sns.publish(
        TopicArn=cfg["SNS-Topic-ARN"],
        Message=req["Message"]
    )

def send_push(cfg, req):
    print(f"Push to {req['PushToken']}: {req['Message']}")
    return {"MessageId": "PUSH-MOCK"}

