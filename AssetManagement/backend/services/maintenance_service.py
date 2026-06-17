"""
維護 Service — 維修保養的業務邏輯

職責：
- 維護紀錄 CRUD
- 即將到期的維護查詢（預警功能）
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from core.errors import NotFoundError
from models.maintenance import MaintenanceRecord
from repositories.maintenance_repo import MaintenanceRepository
from schemas.maintenance import MaintenanceCreate


class MaintenanceService:
    """維護管理業務邏輯"""

    def __init__(self, db: Session):
        self.repo = MaintenanceRepository(db)

    def get_by_id(self, record_id: int) -> MaintenanceRecord:
        record = self.repo.get(record_id)
        if not record:
            raise NotFoundError("維護紀錄不存在")
        return record

    def list_records(
        self, asset_id: int | None = None, maintenance_type: str | None = None
    ) -> list[MaintenanceRecord]:
        return self.repo.get_all()

    def create_record(self, data: MaintenanceCreate) -> MaintenanceRecord:
        return self.repo.create(data)

    def update_record(
        self, record_id: int, data: MaintenanceCreate
    ) -> MaintenanceRecord:
        record = self.get_by_id(record_id)
        updated = self.repo.update(record_id, data)
        assert updated is not None
        return updated

    def get_upcoming(self, days: int = 30) -> list[MaintenanceRecord]:
        """取得指定天數內即將到期的維護"""
        return self.repo.find_upcoming(days)
