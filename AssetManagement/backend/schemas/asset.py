"""
資產台帳 Schema
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, field_validator

from schemas.common import ASSET_CODE_LEN, ASSET_CODE_PATTERN, PREFIX_LEN, SERIAL_LEN, YEAR_LEN, VALID_PREFIX_CHARS


class AssetBase(BaseModel):
    asset_code: str
    asset_name: str
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    purchase_date: Optional[date] = None
    purchase_price: Optional[Decimal] = None
    current_value: Optional[Decimal] = None
    department: Optional[str] = None
    location: Optional[str] = None
    custodian: Optional[str] = None
    status: str = "使用中"
    notes: Optional[str] = None
    disposal_reason: Optional[str] = None

    @field_validator("asset_code")
    @classmethod
    def validate_asset_code(cls, v: str) -> str:
        v = v.strip().upper()
        if len(v) != ASSET_CODE_LEN:
            raise ValueError(
                f"資產編號必須為 {ASSET_CODE_LEN} 碼"
                f"（{PREFIX_LEN}碼前綴 + {YEAR_LEN}碼年份 + {SERIAL_LEN}碼流水號），"
                f"目前為 {len(v)} 碼"
            )
        if not ASSET_CODE_PATTERN.match(v):
            raise ValueError(
                "資產編號格式錯誤：前 4 碼須為大寫英文字母（不含 I、O），後 8 碼須為數字"
                f"（例：CMPT26000001）"
            )
        return v


class AssetCreate(AssetBase):
    pass


class AssetResponse(AssetBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
