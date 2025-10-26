from fastapi import APIRouter, HTTPException, Depends, Request, Query, status
from pydantic import BaseModel
# 1. UPDATED IMPORT: Use PhonePe functions instead of Razorpay ones
from services.payment_service import initiate_phonepe_payment, check_phonepe_status
from services.firebase_service import create_donation, update_donation_status, list_donations_for_user
from utils.auth import require_auth

router = APIRouter()

class DonationCreate(BaseModel):
    orphanage_id: str
    amount: float
    currency: str = "INR"
    method: str  # "razorpay" or "upi" -> NOW supports "phonepe"
    note: str = ""

# -------------------------------------------------------------
# 1. MODIFIED ENDPOINT: Handles PhonePe Initiation
# -------------------------------------------------------------
@router.post("/create")
async def create_donation_endpoint(payload: DonationCreate, user=Depends(require_auth)):
    """
    1) Create donation document with status 'pending'
    2) If Razorpay -> REMOVED. Now handles PhonePe.
    3) If PhonePe -> initiate order and return redirect URL.
    """
    # Create donation document with status 'pending' (SAME LOGIC)
    donation_id = await create_donation({
        "user_id": user["uid"],
        "orphanage_id": payload.orphanage_id,
        "amount": payload.amount,
        "currency": payload.currency,
        "status": "pending",
        "method": payload.method,
        "note": payload.note
    })

    if payload.method == "phonepe":
        # Amount needs to be an integer (assuming it's in Rupees for the UI)
        amount_int = int(payload.amount)

        # Initiate PhonePe payment using the service function
        payment_info = await initiate_phonepe_payment(
            amount=amount_int, 
            user_id=user["uid"], 
            donation_id=donation_id
        )

        if payment_info.get("success"):
            # Return the payment URL for the client to redirect the user
            return {
                "donation_id": donation_id,
                "merchant_transaction_id": payment_info["merchant_transaction_id"],
                "payment_url": payment_info["payment_url"]
            }
        
        raise HTTPException(status_code=500, detail="PhonePe initiation failed.")
    
    elif payload.method == "razorpay":
        # NOTE: If you must keep Razorpay for backward compatibility, you'd keep this. 
        # But we are assuming the Razorpay service functions are now GONE.
        # If Razorpay functions are GONE, this block should be DELETED or changed to raise an error.
        raise HTTPException(status_code=400, detail="Razorpay is no longer supported. Use 'phonepe'.")

    elif payload.method == "upi":
        # For UPI, the client builds the UPI intent. 
        return {"donation_id": donation_id, "upi": {"note": payload.note}}
    
    else:
        raise HTTPException(status_code=400, detail="Invalid payment method.")

# -------------------------------------------------------------
# 2. REMOVED ENDPOINT: Delete the old /razorpay/webhook endpoint
# -------------------------------------------------------------

# -------------------------------------------------------------
# 3. NEW ENDPOINT: Browser Redirect (User's device)
# -------------------------------------------------------------
@router.get("/phonepe/redirect")
async def handle_phonepe_redirect(merchantTransactionId: str = Query(...)):
    """
    User's browser is redirected here after payment. We check the final status.
    **Note**: You must return a full HTML page here that executes a deep link 
    or redirects the browser to a known URL scheme to return control to the Flutter app.
    """
    status_response = await check_phonepe_status(merchantTransactionId)
    
    # You need to extract the original donation_id from the metadata of the transaction
    # We'll rely on the status to tell the frontend whether to check the app's state.
    
    if status_response.success and status_response.code == "PAYMENT_SUCCESS":
        # Payment successful. Update DB.
        # status_response.data.metadata should contain "donation_id"
        donation_id = status_response.data.metadata.get("donation_id")
        if donation_id:
             await update_donation_status(donation_id, "SUCCESS", status_response.data.transaction_id)
        
        # In a real app, render an HTML page that redirects to your Flutter app deep link
        return {"status": "success", "message": "Payment successful. Redirecting to app..."}
    
    # Payment failed, cancelled, or pending
    # NOTE: You might want to update the status to FAILED/PENDING here too.
    return {"status": "failure", "message": "Payment failed or pending."}


# -------------------------------------------------------------
# 4. NEW ENDPOINT: Server Callback (PhonePe's server)
# -------------------------------------------------------------
@router.post("/phonepe/callback")
async def handle_phonepe_callback(request: Request):
    """
    PhonePe's server-to-server confirmation. This replaces the /razorpay/webhook.
    """
    try:
        # NOTE: PhonePe sends a complex Base64 encoded payload that needs validation.
        # Best practice is to acknowledge receipt (return 200 OK) and immediately
        # perform a server-to-server status check using the SDK (as implemented 
        # in the /phonepe/redirect endpoint).
        
        # We need to parse the request body to extract the merchantTransactionId.
        # Since the payload is complex, we just rely on the fact that the redirect 
        # endpoint handles the status check for finality.

        # ***Crucially, you MUST return a 200 OK to PhonePe to stop retries.***
        # This function primarily serves to trigger a status update in your backend.
        
        # 1. Parse the incoming request body (which contains the base64 payload)
        # In a full implementation, you'd decode and verify this.
        body = await request.body() 
        # 2. Acknowledge receipt
        return {"status": "acknowledged", "message": "Callback received."}
    
    except Exception as e:
        print(f"PhonePe callback processing error: {e}")
        # ALWAYS return 200 OK even on internal error so PhonePe stops sending webhooks
        return {"status": "error", "message": "Internal error"}

# Existing endpoint kept
@router.get("/me")
async def get_my_donations(user=Depends(require_auth)):
    docs = await list_donations_for_user(user["uid"])
    return {"donations": docs}

# Existing test endpoint kept
@router.get("/test")
async def test_donations():
    return {"message": "Donation route working fine!"}
