# services/payment_service.py

# 1. Import the PhonePe client object and required types from your config
from config import phonepe_client, settings
from fastapi import HTTPException
from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
from phonepe.sdk.pg.payments.v1.models.response.pg_pay_response import PgPayResponse
from phonepe.sdk.pg.payments.v1.models.response.pg_transaction_status_response import PgTransactionStatusResponse
from phonepe.sdk.pg.payments.v1.models.request.pg_transaction_status_request import PgTransactionStatusRequest
from uuid import uuid4 # Used for generating a unique transaction ID


async def initiate_phonepe_payment(amount: int, user_id: str, donation_id: str) -> dict:
    """
    Initiates a standard PhonePe payment and returns the redirect URL.
    This replaces create_razorpay_order.
    """
    if not settings.CLIENT_ID or not settings.CLIENT_SECRET:
         raise HTTPException(status_code=500, detail="PhonePe client not configured (Missing ID/Secret)")

    try:
        # Generate a unique Merchant Transaction ID
        merchant_transaction_id = str(uuid4()) 
        
        # NOTE: PhonePe amount is in PAISA, input amount is assumed in Rupees, so multiply by 100
        amount_in_paise = amount * 100 
        
        # Build the redirect and callback URLs using the base backend URL
        # redirect_url: Where the user's browser lands after payment/failure (e.g., /phonepe/redirect)
        # callback_url: Server-to-server confirmation (e.g., /phonepe/callback)
        redirect_url = f"{settings.BACKEND_URL}/donations/phonepe/redirect?merchantTransactionId={merchant_transaction_id}"
        callback_url = f"{settings.BACKEND_URL}/donations/phonepe/callback"
        
        # 2. Construct the Pay Request object required by the SDK
        pay_request = PgPayRequest(
            merchant_id=settings.CLIENT_ID, 
            merchant_transaction_id=merchant_transaction_id,
            amount=amount_in_paise,
            merchant_user_id=user_id,
            callback_url=callback_url,
            redirect_url=redirect_url,
            # Pass custom data that you want back after payment
            metadata={"donation_id": donation_id}, 
        )

        # 3. Use the SDK client to initiate the payment
        response: PgPayResponse = phonepe_client.pay(pay_request)

        if response.success:
            # The SDK response provides the actual URL to redirect the user to
            return {
                "success": True,
                "merchant_transaction_id": merchant_transaction_id,
                "payment_url": response.data.instrument_response.redirect_info.url
            }
        
        # Handle cases where the request to PhonePe succeeded but payment initiation failed
        return {"success": False, "message": response.message}
        
    except Exception as e:
        print(f"PhonePe Payment Initiation Error: {e}")
        # Log the error and raise a generic 500
        raise HTTPException(status_code=500, detail=f"Payment processing failed: {e}")

async def check_phonepe_status(merchant_transaction_id: str) -> PgTransactionStatusResponse:
    """
    Checks the status of a PhonePe transaction using the SDK.
    This replaces webhook verification logic, which PhonePe handles with status checks.
    """
    if not settings.CLIENT_ID:
        raise HTTPException(status_code=500, detail="PhonePe client not configured (Missing ID)")
        
    try:
        status_request = PgTransactionStatusRequest(
            merchant_id=settings.CLIENT_ID,
            merchant_transaction_id=merchant_transaction_id
        )
        
        # Use the SDK client to get the transaction status
        response: PgTransactionStatusResponse = phonepe_client.get_order_status(status_request)
        
        return response
        
    except Exception as e:
        print(f"PhonePe Status Check Error: {e}")
        # Return a failed status response on exception
        raise HTTPException(status_code=500, detail="Internal server error during status check.")
