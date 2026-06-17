"""
資產類別 Schema
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from schemas.common import PREFIX_LEN


class CategoryBase(BaseModel):
    code: str
    name: str
    prefix: str
    description: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True

    @field_validator("prefix")
    @classmethod
    def validate_prefix(cls, v: str) -> str:
        v = v.strip().upper()
        if len(v) != PREFIX_LEN:
            raise ValueError(f"前綴必須為 {PREFIX_LEN} 碼大寫英文字母，目前為 {len(v)} 碼")
        if not v.isalpha():
            raise ValueError("前綴必須全部為英文字母")
        return v


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
