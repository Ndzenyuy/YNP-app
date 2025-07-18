from pydantic import BaseModel
from typing import Optional, List, Union

class NotificationRequest(BaseModel):
    Application: str
    OutputType: str
    Subject: Optional[str]
    Message: str
    Date: Optional[str]
    Time: Optional[str]
    Interval: dict
    EmailAddresses: Optional[Union[str, List[str]]]
    PhoneNumber: Optional[str]
    PushToken: Optional[str]

