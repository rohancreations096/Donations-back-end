from pydantic import BaseModel
from typing import Optional

class Donation(BaseModel):
    id: Optional[str]
    user_id: str
    orphanage_id: str
    amount: float
    currency: str = "INR"
    status: str = "pending"
    method: str
    txn_id: Optional[str] = None
