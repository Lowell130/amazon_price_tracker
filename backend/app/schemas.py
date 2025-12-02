from pydantic import BaseModel, EmailStr
from typing import Optional, List

# User Models
class User(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

class UserLogin(BaseModel):
    login: str
    password: str

class UserInDB(User):
    hashed_password: str

# Product Models
class ProductRequest(BaseModel):
    product_url: str
    category: Optional[str] = None

class GuestAlertSubscription(BaseModel):
    email: EmailStr
    asin: str

# Password Reset Models
class PasswordResetRequest(BaseModel):
    email: str

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
