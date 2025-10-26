import firebase_admin
from firebase_admin import auth
from fastapi import HTTPException
import os

# Verify Firebase ID tokens sent from the client (Firebase Auth)
async def verify_firebase_token(id_token: str):
    try:
        decoded = auth.verify_id_token(id_token)
        # create or update user record in Firestore (optional)
        user_record = {
            "uid": decoded.get("uid"),
            "email": decoded.get("email"),
            "name": decoded.get("name"),
            "phone": decoded.get("phone_number"),
            "role": "donor"  # clients can set
        }
        from services.firebase_service import create_or_update_user
        await create_or_update_user(decoded.get("uid"), user_record)
        return {"uid": decoded.get("uid"), **user_record}
    except Exception as e:
        return None

async def require_auth(token: str = None, authorization: str = None):
    # FastAPI dependency alternative: client should pass Authorization: Bearer <id_token>
    # For simplicity, we will read from Authorization header in caller function using Depends.
    raise NotImplementedError("Use FastAPI Depends with header in routes.")

# For FastAPI, we'll provide two small wrappers to use as Depends
from fastapi import Header, Depends

async def require_auth(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    token = authorization.split("Bearer ")[-1]
    user = await verify_firebase_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

async def require_auth_optional(authorization: str = Header(None)):
    if not authorization:
        return None
    token = authorization.split("Bearer ")[-1]
    user = await verify_firebase_token(token)
    return user
