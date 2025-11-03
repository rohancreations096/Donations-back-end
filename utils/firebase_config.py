import firebase_admin
from firebase_admin import credentials, firestore
import os

# Global Firestore variable
db = None

def init_firebase():
    global db

    try:
        # If Firebase is already initialized, reuse it
        if firebase_admin._apps:
            db = firestore.client()
            print("⚡ Firebase already initialized, reusing instance.")
            return db

        cred_path = "servicekeyaccount.json"  # must match your Render file

        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase initialized successfully using servicekeyaccount.json!")
        else:
            raise FileNotFoundError("❌ servicekeyaccount.json not found in root directory!")

        # Create Firestore client
        db = firestore.client()
        print("✅ Firestore client connected successfully!")

    except Exception as e:
        print("🔥 Firebase initialization failed:", str(e))
        db = None

    return db


# Initialize immediately when the module is imported
init_firebase()
