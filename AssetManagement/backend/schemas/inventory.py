"""
盤點紀錄 Schema
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class InventoryBase(BaseModel):
    asset_id: Optional[int] = None
    asset_code: str
    inventory_date: date
    inventory_person: Optional[str] = None
    expected_location: Optional[str] = None
    actual_location: Optional[str] = None
    location_match: Optional[bool] = None
    status: str = "正常"
    exception_description: Optional[str] = None
    exception_result: Optional[str] = None
    notes: Optional[str] = None


class InventoryCreate(InventoryBase):
    pass


class InventoryResponse(InventoryBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
