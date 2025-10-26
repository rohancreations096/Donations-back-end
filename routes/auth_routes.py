from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
# Corrected import to point to the file inside the 'utils' folder
from utils.auth import verify_firebase_token, require_auth_optional

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

# This part seems separate and correct
# from fastapi import APIRouter # This import is redundant if already above

# router = APIRouter() # This creates a NEW router, overwriting the old one. Be careful!
# It might be better to keep the test route within the original router above.

@router.get("/test")
async def test_auth():
    return {"message": "Auth route working properly!"}
