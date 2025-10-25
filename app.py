from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
import os
import json

from routes import auth_routes, orphanage_routes, donation_routes, notification_routes

# --- START Firebase Initialization Logic (NEW CODE) ---
SERVICE_ACCOUNT_ENV_VAR = 'FIREBASE_SERVICE_ACCOUNT_KEY' 
key_json_string = os.environ.get(SERVICE_ACCOUNT_ENV_VAR)

if key_json_string:
    try:
        # 1. Load the JSON string from the environment variable
        key_config = json.loads(key_json_string)
        
        # 2. Initialize the Firebase App using the dictionary
        cred = credentials.Certificate(key_config)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully using environment variable.")

    except Exception as e:
        print(f"FATAL ERROR: Failed to initialize Firebase Admin SDK: {e}")
        # In a production app, you might raise an error here to stop startup
else:
    # This warning indicates the deployment team needs to set the variable.
    print(f"WARNING: Firebase credentials environment variable '{SERVICE_ACCOUNT_ENV_VAR}' not found.")
    print("Default credentials will be attempted, which will FAIL on Render without explicit setup.")

# --- END Firebase Initialization Logic ---


app = FastAPI(title="Donation App Backend (Orphanages)")

# CORS - allow flutter web / mobile dev origins as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now, tighten for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(orphanage_routes.router, prefix="/orphanages", tags=["orphanages"])
app.include_router(donation_routes.router, prefix="/donations", tags=["donations"])
app.include_router(notification_routes.router, prefix="/notifications", tags=["notifications"])

@app.get("/")
async def root():
    return {"message": "Donation App Backend - FastAPI is up."}
