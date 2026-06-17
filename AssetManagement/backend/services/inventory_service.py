"""
盤點 Service — 盤點管理的業務邏輯

職責：
- 盤點紀錄 CRUD
- 異常盤點查詢
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from core.errors import NotFoundError
from models.inventory import InventoryRecord
from repositories.inventory_repo import InventoryRepository
from schemas.inventory import InventoryCreate


class InventoryService:
    """盤點管理業務邏輯"""

    def __init__(self, db: Session):
        self.repo = InventoryRepository(db)

    def get_by_id(self, record_id: int) -> InventoryRecord:
        record = self.repo.get(record_id)
        if not record:
            raise NotFoundError("盤點紀錄不存在")
        return record

    def list_records(
        self, asset_id: int | None = None, status: str | None = None
    ) -> list[InventoryRecord]:
        return self.repo.get_all()

    def create_record(self, data: InventoryCreate) -> InventoryRecord:
        return self.repo.create(data)

    def update_record(
        self, record_id: int, data: InventoryCreate
    ) -> InventoryRecord:
        record = self.get_by_id(record_id)
        updated = self.repo.update(record_id, data)
        assert updated is not None
        return updated

    def get_abnormal_records(self) -> list[InventoryRecord]:
        """取得所有異常盤點"""
        return self.repo.find_abnormal()
