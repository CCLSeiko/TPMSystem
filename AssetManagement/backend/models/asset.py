"""
資產基本資料模型 (Asset)
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Date, DECIMAL, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import foreign

from core.database import Base


class Asset(Base):
    """資產基本資料表"""

    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    asset_code: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False, index=True
    )
    asset_name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100), index=True, nullable=True)
    brand: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    serial_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    purchase_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    purchase_price: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(12, 2), nullable=True
    )
    current_value: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(12, 2), nullable=True
    )
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    custodian: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="使用中", index=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    disposal_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    # 關聯
    category_rel: Mapped[Optional["AssetCategory"]] = relationship(
        back_populates="assets",
        primaryjoin="foreign(Asset.category) == AssetCategory.name",
    )
    inventory_records: Mapped[list["InventoryRecord"]] = relationship(
        back_populates="asset"
    )
    maintenance_records: Mapped[list["MaintenanceRecord"]] = relationship(
        back_populates="asset"
    )

    def __repr__(self) -> str:
        return f"<Asset {self.asset_code}: {self.asset_name}>"
