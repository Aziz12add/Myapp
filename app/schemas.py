from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional, Literal
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class KeyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    protocol: Literal["vless", "vmess", "trojan"] = "vless"
    ip: Optional[str] = None  # اگر خالی باشد از pool انتخاب می‌شود


class KeyOut(BaseModel):
    id: int
    name: str
    protocol: str
    ip: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class KeyCreatedResponse(BaseModel):
    """فقط یک بار secret را نشان می‌دهد"""
    key: KeyOut
    secret: str
    config: dict | str
