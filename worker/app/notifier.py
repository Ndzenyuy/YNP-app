import boto3
from . import config

session = boto3.session.Session(
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.AWS_REGION
)

ses = session.client("ses", endpoint_url=config.ENDPOINT_URL)
sns = session.client("sns", endpoint_url=config.ENDPOINT_URL)
dynamodb = session.resource("dynamodb", endpoint_url=config.ENDPOINT_URL)

def get_app_config(app_id: str):
    table = dynamodb.Table(config.APPLICATIONS_TABLE)
    response = table.get_item(Key={"ApplicationID": app_id})
    return response.get("Item")

def send_notification(app_cfg, payload: dict):
    output = payload.get("OutputType")
    msg = payload["Message"]
    subject = payload.get("Subject", "")

    if output == "EMAIL":
        for email in payload.get("EmailAddresses", []):
            ses.send_email(
                Source=app_cfg["Email"],
                Destination={"ToAddresses": [email]},
                Message={
                    "Subject": {"Data": subject},
                    "Body": {"Text": {"Data": msg}}
                }
            )

    elif output == "SMS":
        sns.publish(
            TopicArn=app_cfg["SNS-Topic-ARN"],
            Message=msg,
            MessageAttributes={
                "AWS.SNS.SMS.SMSType": {
                    "DataType": "String",
                    "StringValue": "Transactional"
                }
            }
        )

    elif output == "PUSH":
        sns.publish(
            TopicArn=app_cfg["SNS-Topic-ARN"],
            Message=msg
        )

