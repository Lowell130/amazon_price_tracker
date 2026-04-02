from pydantic import BaseModel, EmailStr
from typing import Optional, List

# User Models
class User(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    telegram_chat_id: Optional[str] = None

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

# AI Article Models
class ArticleModel(BaseModel):
    id: Optional[str] = None
    asin: Optional[str] = None  # Original ASIN from tracker
    keyword: Optional[str] = None
    title: Optional[str] = None
    content_html: Optional[str] = None
    amazon_product_asin: Optional[str] = None
    amazon_product_url: Optional[str] = None
    amazon_product_title: Optional[str] = None
    amazon_product_image_url: Optional[str] = None
    amazon_product_price: Optional[str] = None
    slug: Optional[str] = None
    meta_description: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[str] = "queued"
    created_at: Optional[str] = None
    product: Optional[dict] = None
    product_image_url: Optional[str] = None

class ArticleTrigger(BaseModel):
    keyword: str
    asin: str

class PassiveProductUpdate(BaseModel):
    asin: str
    price: Optional[float] = None
    availability: Optional[str] = "Disponibile"
