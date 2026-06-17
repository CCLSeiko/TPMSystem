"""
盤點紀錄 Repository
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from models.inventory import InventoryRecord
from repositories.base import BaseRepository


class InventoryRepository(BaseRepository[InventoryRecord]):
    """盤點紀錄資料存取層"""

    def __init__(self, db: Session):
        super().__init__(db, InventoryRecord)

    def find_by_asset(self, asset_id: int) -> list[InventoryRecord]:
        """依資產查詢盤點紀錄"""
        return (
            self.db.query(InventoryRecord)
            .filter(InventoryRecord.asset_id == asset_id)
            .order_by(InventoryRecord.inventory_date.desc())
            .all()
        )

    def find_by_status(self, status: str) -> list[InventoryRecord]:
        """依狀態查詢（正常/異常）"""
        return (
            self.db.query(InventoryRecord)
            .filter(InventoryRecord.status == status)
            .order_by(InventoryRecord.inventory_date.desc())
            .all()
        )

    def find_abnormal(self) -> list[InventoryRecord]:
        """取得所有異常盤點紀錄"""
        return (
            self.db.query(InventoryRecord)
            .filter(InventoryRecord.status == "異常")
            .order_by(InventoryRecord.inventory_date.desc())
            .all()
        )
