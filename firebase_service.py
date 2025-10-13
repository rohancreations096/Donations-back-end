import firebase_admin
from firebase_admin import credentials, firestore, messaging
import os
import asyncio

# initialize in module import
FIREBASE_CRED = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")  # path to service account json
if not firebase_admin._apps:
    if FIREBASE_CRED:
        cred = credentials.Certificate(FIREBASE_CRED)
        firebase_admin.initialize_app(cred)
    else:
        # Try default app init (if running in GCP)
        firebase_admin.initialize_app()

db = firestore.client()

# USERS
async def get_user(uid):
    doc = db.collection("users").document(uid).get()
    if doc.exists:
        return doc.to_dict()
    return None

async def create_or_update_user(uid, data):
    db.collection("users").document(uid).set(data, merge=True)
    return True

# ORPHANAGES
async def list_orphanages():
    docs = db.collection("orphanages").stream()
    result = []
    for d in docs:
        o = d.to_dict()
        o["id"] = d.id
        result.append(o)
    return result

async def get_orphanage_by_id(orphanage_id):
    doc = db.collection("orphanages").document(orphanage_id).get()
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return None

async def create_orphanage(data: dict):
    doc_ref = db.collection("orphanages").add(data)
    # add returns (ref, write_result)
    return doc_ref[0].id

async def update_orphanage(orphanage_id, data: dict):
    ref = db.collection("orphanages").document(orphanage_id)
    if not ref.get().exists:
        return False
    ref.set(data, merge=True)
    return True

# DONATIONS
async def create_donation(data: dict):
    doc_ref = db.collection("donations").add(data)
    return doc_ref[0].id

async def update_donation_status(donation_id, status, txn_id=None):
    ref = db.collection("donations").document(donation_id)
    if not ref.get().exists:
        return False
    update = {"status": status}
    if txn_id:
        update["txn_id"] = txn_id
    ref.set(update, merge=True)
    return True

async def list_donations_for_user(uid):
    docs = db.collection("donations").where("user_id", "==", uid).stream()
    result = []
    for d in docs:
        r = d.to_dict()
        r["id"] = d.id
        result.append(r)
    return result

# URGENT NEEDS (simple functions)
async def post_urgent_need(orphanage_id, description, ts):
    data = {"orphanage_id": orphanage_id, "description": description, "timestamp": ts}
    doc_ref = db.collection("urgent_needs").add(data)
    return doc_ref[0].id

# Note: mixing async and sync firestore calls:
# The firebase-admin SDK is synchronous. Wrapping in coroutine for FastAPI compatibility.
# It's acceptable to call the sync functions directly, but we defined async functions for interface.
