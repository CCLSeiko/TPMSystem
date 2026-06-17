"""
維護紀錄 Schema
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class MaintenanceBase(BaseModel):
    asset_id: Optional[int] = None
    asset_code: str
    maintenance_date: date
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[Decimal] = Decimal(0)
    vendor: Optional[str] = None
    person_in_charge: Optional[str] = None
    next_maintenance_date: Optional[date] = None
    notes: Optional[str] = None


class MaintenanceCreate(MaintenanceBase):
    pass


class MaintenanceResponse(MaintenanceBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
