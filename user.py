from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    uid: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    role: Optional[str] = "donor"  # or "organization"
    language: Optional[str] = "en"
