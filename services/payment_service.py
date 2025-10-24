import os
import razorpay
import hmac
import hashlib
import json

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

client = None
if RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

async def create_razorpay_order(amount: int, receipt: str, currency="INR"):
    """
    amount: in paise (integer)
    receipt: our donation id
    """
    if not client:
        raise Exception("Razorpay client not configured")
    order = client.order.create({
        "amount": amount,
        "currency": currency,
        "receipt": receipt,
        "payment_capture": 1
    })
    return order

def verify_razorpay_signature(body: bytes, signature: str):
    """
    Verify webhook signature using secret
    Razorpay signs body with secret; signature header: X-Razorpay-Signature
    """
    if not RAZORPAY_KEY_SECRET:
        return False, {}
    expected = hmac.new(RAZORPAY_KEY_SECRET.encode(), body, hashlib.sha256).hexdigest()
    # Razorpay provides base64 signature; compare by verifying using razorpay util would be better.
    # We'll do a naive compare; in production use razorpay.utility.verify_signature
    try:
        payload = json.loads(body)
    except:
        payload = {}
    # Use razorpay util if available:
    try:
        from razorpay import utility
        utility.verify_webhook_signature(body.decode(), signature, RAZORPAY_KEY_SECRET)
        return True, payload
    except Exception:
        return False, payload
