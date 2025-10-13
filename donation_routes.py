from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from services.payment_service import create_razorpay_order, verify_razorpay_signature
from services.firebase_service import create_donation, update_donation_status, list_donations_for_user
from utils.auth import require_auth

router = APIRouter()

class DonationCreate(BaseModel):
    orphanage_id: str
    amount: float
    currency: str = "INR"
    method: str  # "razorpay" or "upi"
    note: str = ""

@router.post("/create")
async def create_donation_endpoint(payload: DonationCreate, user=Depends(require_auth)):
    """
    1) Create donation document with status 'pending'
    2) If Razorpay -> create order and return order details for client to complete payment
    3) If UPI -> return a UPI intent/information (client handles UPI)
    """
    donation_id = await create_donation({
        "user_id": user["uid"],
        "orphanage_id": payload.orphanage_id,
        "amount": payload.amount,
        "currency": payload.currency,
        "status": "pending",
        "method": payload.method,
        "note": payload.note
    })

    if payload.method == "razorpay":
        order = await create_razorpay_order(amount=int(payload.amount * 100), receipt=donation_id)
        return {"donation_id": donation_id, "razorpay_order": order}
    else:
        # For UPI, the client builds the UPI intent. Return the donation id so you can verify later.
        return {"donation_id": donation_id, "upi": {"note": payload.note}}

@router.post("/razorpay/webhook")
async def razorpay_webhook(request: Request):
    """
    Razorpay will POST payment events here. Verify signature and update donation.
    """
    body = await request.body()
    headers = request.headers
    signature = headers.get("x-razorpay-signature")
    is_valid, payload = verify_razorpay_signature(body, signature)
    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid signature")
    # Example payload processing - update donation based on receipt (we used receipt=donation_id)
    event = payload.get("event")
    data = payload.get("payload", {})
    # Simplified handling:
    payment = None
    if event and "payment" in event:
        # extract payment & receipt
        payment = data.get("payment", {}).get("entity", {})
    if payment:
        receipt = payment.get("notes", {}).get("receipt") or payment.get("order_id")
        txn_id = payment.get("id")
        status = payment.get("status")
        # map to our donation
        if receipt:
            await update_donation_status(receipt, status, txn_id)
    return {"status": "ok"}

@router.get("/me")
async def get_my_donations(user=Depends(require_auth)):
    docs = await list_donations_for_user(user["uid"])
    return {"donations": docs}
