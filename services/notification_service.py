import firebase_admin
from firebase_admin import messaging
import os

def send_fcm_to_token(token: str, title: str, body: str, data: dict = None):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=token,
        data={k: str(v) for k, v in (data or {}).items()}
    )
    response = messaging.send(message)
    return response

def send_fcm_to_topic(topic: str, title: str, body: str, data: dict = None):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        topic=topic,
        data={k: str(v) for k, v in (data or {}).items()}
    )
    response = messaging.send(message)
    return response
