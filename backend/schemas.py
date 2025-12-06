from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


# ---------- USER / AUTH ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    email: EmailStr


# ---------- CHAT ----------

class ChatRequest(BaseModel):
    message: str


class ChatMessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ChatResponse(BaseModel):
    reply: str
    history: List[ChatMessageOut]

    model_config = {
        "from_attributes": True
    }


# ---------- PLANS / SAAS ----------

class PlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    currency: str = "INR"            # "INR" or "USD"
    tokens_per_month: int
    is_active: bool = True


class PlanCreate(PlanBase):
    pass


class PlanUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    tokens_per_month: Optional[int] = None
    is_active: Optional[bool] = None


class PlanOut(PlanBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
