"""
盤點紀錄模型 (InventoryRecord)
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from core.database import Base


class InventoryRecord(Base):
    """盤點紀錄表"""

    __tablename__ = "inventory_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("assets.id"), nullable=True
    )
    asset_code: Mapped[str] = mapped_column(String(20), nullable=False)
    inventory_date: Mapped[date] = mapped_column(Date, nullable=False)
    inventory_person: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    expected_location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    actual_location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    location_match: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="正常")
    exception_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    exception_result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )

    # 關聯
    asset: Mapped[Optional["Asset"]] = relationship(back_populates="inventory_records")

    def __repr__(self) -> str:
        return f"<InventoryRecord {self.asset_code} @ {self.inventory_date}>"
