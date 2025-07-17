from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from .aws import setup_app_services
from .db import save_app_record, get_all_apps

app = FastAPI()

class AppRequest(BaseModel):
    App_name: str
    Application: str
    Email: EmailStr
    Domain: str

@app.post("/app")
def register_application(app_req: AppRequest):
    try:
        config = setup_app_services(app_req)
        save_app_record(config)
        return {"status": "created", "application": config}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/apps")
def list_registered_apps():
    try:
        return get_all_apps()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

