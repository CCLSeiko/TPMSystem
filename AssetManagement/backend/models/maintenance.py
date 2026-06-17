"""
維護紀錄模型 (MaintenanceRecord)
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, DECIMAL, ForeignKey, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.database import Base


class MaintenanceRecord(Base):
    """維護紀錄表"""

    __tablename__ = "maintenance_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("assets.id"), nullable=True
    )
    asset_code: Mapped[str] = mapped_column(String(20), nullable=False)
    maintenance_date: Mapped[date] = mapped_column(Date, nullable=False)
    maintenance_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cost: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(12, 2), default=0)
    vendor: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    person_in_charge: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    next_maintenance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )

    # 關聯
    asset: Mapped[Optional["Asset"]] = relationship(
        back_populates="maintenance_records"
    )

    def __repr__(self) -> str:
        return f"<MaintenanceRecord {self.asset_code} @ {self.maintenance_date}>"
