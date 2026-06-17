"""
維護紀錄 Repository
"""

from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from models.maintenance import MaintenanceRecord
from repositories.base import BaseRepository


class MaintenanceRepository(BaseRepository[MaintenanceRecord]):
    """維護紀錄資料存取層"""

    def __init__(self, db: Session):
        super().__init__(db, MaintenanceRecord)

    def find_by_asset(self, asset_id: int) -> list[MaintenanceRecord]:
        """依資產查詢維護紀錄"""
        return (
            self.db.query(MaintenanceRecord)
            .filter(MaintenanceRecord.asset_id == asset_id)
            .order_by(MaintenanceRecord.maintenance_date.desc())
            .all()
        )

    def find_by_type(self, maint_type: str) -> list[MaintenanceRecord]:
        """依維護類型查詢（維修/保養/耗材更換）"""
        return (
            self.db.query(MaintenanceRecord)
            .filter(MaintenanceRecord.maintenance_type == maint_type)
            .order_by(MaintenanceRecord.maintenance_date.desc())
            .all()
        )

    def find_upcoming(self, days: int = 30) -> list[MaintenanceRecord]:
        """取得指定天數內即將到期的維護"""
        today = date.today()
        deadline = today + timedelta(days=days)
        return (
            self.db.query(MaintenanceRecord)
            .filter(
                MaintenanceRecord.next_maintenance_date.isnot(None),
                MaintenanceRecord.next_maintenance_date <= deadline,
                MaintenanceRecord.next_maintenance_date >= today,
            )
            .order_by(MaintenanceRecord.next_maintenance_date)
            .all()
        )

    def get_total_cost(self, asset_id: int | None = None) -> Decimal:
        """取得維護總費用（可依資產篩選）"""
        from sqlalchemy import func

        query = self.db.query(func.sum(MaintenanceRecord.cost))
        if asset_id is not None:
            query = query.filter(MaintenanceRecord.asset_id == asset_id)
        return query.scalar() or Decimal(0)
