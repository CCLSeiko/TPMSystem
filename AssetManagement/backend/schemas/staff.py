"""
管理人員 Schema
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class StaffBase(BaseModel):
    name: str
    role: str = "operator"
    department: Optional[str] = None
    responsible_area: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True


class StaffCreate(StaffBase):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class StaffUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    responsible_area: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class StaffResponse(StaffBase):
    id: int
    username: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: StaffResponse
