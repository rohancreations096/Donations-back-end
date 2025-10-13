from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.notification_service import send_fcm_to_topic, send_fcm_to_token
from utils.auth import require_auth

router = APIRouter()

class NotifyTopic(BaseModel):
    topic: str
    title: str
    body: str
    data: dict = {}

@router.post("/topic")
async def notify_topic(payload: NotifyTopic, user=Depends(require_auth)):
    await send_fcm_to_topic(payload.topic, payload.title, payload.body, payload.data)
    return {"status": "ok"}

class NotifyToken(BaseModel):
    token: str
    title: str
    body: str
    data: dict = {}

@router.post("/token")
async def notify_token(payload: NotifyToken, user=Depends(require_auth)):
    await send_fcm_to_token(payload.token, payload.title, payload.body, payload.data)
    return {"status": "ok"}
