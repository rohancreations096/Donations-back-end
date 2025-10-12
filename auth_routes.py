from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from utils.auth import verify_firebase_token, optionally_verify_firebase_token

router = APIRouter()

class LoginRequest(BaseModel):
    # In practice user registers via client using Firebase SDK.
    # Backend can accept ID token to verify and create user record.
    id_token: str

@router.post("/login")
async def login(req: LoginRequest):
    """
    Verify Firebase ID token, create or update user in Firestore.
    Returns user doc.
    """
    user = await verify_firebase_token(req.id_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user": user}

@router.get("/me")
async def me(authorization: str = Header(None)):
    """
    Returns user info if token provided. Skip auth allowed on client.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    token = authorization.split("Bearer ")[-1]
    user = await verify_firebase_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user": user}
